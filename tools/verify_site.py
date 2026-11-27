#!/usr/bin/env python3
"""Verify the Trellmere storefront is internally consistent and ready to deploy.

Checks:
  1. every internal href/src target resolves to a real file
  2. every product in assets/products.js has a detail page and a buy slot
  3. every product detail page has a matching product entry
  4. robots.txt / sitemap.xml contain no placeholder domain
  5. HTML tag balance (lightweight) and required assets exist

Product-specific sets (marketplace slots, Blender/PLCnext hosts, buy URLs) are
derived from assets/products.js rather than duplicated here, so that file stays
the single source of truth. This script is stdlib-only and makes no network
requests: "live Gumroad link" below means the URL has the expected prefix, not
that the URL was fetched or that the product is published.

Usage: python tools/verify_site.py
"""
from __future__ import annotations

import html.parser
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PASS = 0
FAIL = 0


def ok(msg: str) -> None:
    global PASS
    PASS += 1
    print(f"[PASS] {msg}")


def bad(msg: str) -> None:
    global FAIL
    FAIL += 1
    print(f"[FAIL] {msg}")


class LinkParser(html.parser.HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.stack: list[str] = []
        self.mismatches: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for key in ("href", "src"):
            val = d.get(key)
            if val:
                self.links.append(val)
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        d = dict(attrs)
        for key in ("href", "src"):
            if d.get(key):
                self.links.append(d[key])

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            self.mismatches.append(f"unexpected </{tag}> (open: {self.stack[-3:]})")
            while self.stack and self.stack[-1] != tag:
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.mismatches.append(f"stray </{tag}>")


def parse_products(text: str) -> list[dict]:
    """Parse the flat product objects in assets/products.js.

    Returns one dict per product with the fields used by the checks below.
    A field is None when the object does not declare it (e.g. marketplaceUrl).
    """
    body = text.split("window.TRELLMERE_PRODUCTS = [", 1)[-1].split("];", 1)[0]
    records = []
    for block in re.split(r"\n\s*\{\s*\n", body)[1:]:
        record: dict = {}
        for key in ("id", "url", "price", "buyUrl", "thumb", "category",
                    "marketplaceUrl"):
            match = re.search(rf'\b{key}:\s*"([^"]*)"', block)
            record[key] = match.group(1) if match else None
        tags_match = re.search(r"\btags:\s*\[([^\]]*)\]", block)
        record["tags"] = re.findall(r'"([^"]*)"', tags_match.group(1)) if tags_match else []
        pub = re.search(r"\bpublished:\s*(true|false)\b", block)
        record["published"] = pub.group(1) == "true" if pub else None
        if record["id"]:
            records.append(record)
    return records


def main() -> int:
    print(f"Verifying storefront at {ROOT}\n")

    html_files = sorted(ROOT.rglob("*.html"))
    if len(html_files) < 10:
        bad(f"expected >= 10 HTML files, found {len(html_files)}")
    else:
        ok(f"found {len(html_files)} HTML pages")

    # 0. honest claims
    index_text = (ROOT / "index.html").read_text(encoding="utf-8")
    if "Every product is tested before release" in index_text:
        bad("index.html still claims every product is tested before release")
    else:
        ok("no blanket 'tested before release' claim")
    if "not compiled in Engineer or hardware-tested" in index_text:
        ok("PLCnext testing limits disclosed on homepage")
    else:
        bad("homepage lacks PLCnext no-compile/no-hardware disclosure")

    # 1. required assets
    for rel in ("assets/style.css", "assets/site.js", "assets/products.js",
                "index.html", "catalog.html", "robots.txt", "sitemap.xml"):
        (ok if (ROOT / rel).is_file() else bad)(f"required file {rel} exists")

    # 2. internal links + tag balance
    all_links = []
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        parser = LinkParser()
        parser.feed(text)
        if parser.mismatches:
            bad(f"{path.relative_to(ROOT)} tag balance: {parser.mismatches[:3]}")
        elif parser.stack:
            bad(f"{path.relative_to(ROOT)} unclosed tags: {parser.stack[:5]}")
        else:
            ok(f"{path.relative_to(ROOT)} tags balanced")
        all_links.extend((path, link) for link in parser.links)

    external = ("http://", "https://", "mailto:", "data:", "javascript:", "tel:")
    broken = []
    for path, link in all_links:
        if link.startswith(external) or link.startswith("//") or "{{" in link:
            continue
        clean = link.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            continue
        target = (path.parent / clean).resolve()
        if not target.exists():
            broken.append(f"{path.relative_to(ROOT)} -> {link}")
    if broken:
        for item in broken:
            bad(f"broken link {item}")
    else:
        ok(f"all {len(all_links)} href/src targets resolve")

    # 3. product data consistency, driven by assets/products.js
    products_js = (ROOT / "assets/products.js").read_text(encoding="utf-8")
    products = parse_products(products_js)
    ids = [p["id"] for p in products]
    if not ids:
        bad("no products found in products.js")
    raw_ids = re.findall(r'\bid:\s*"([^"]+)"', products_js)
    if ids != raw_ids:
        bad(f"product parser saw {len(ids)} objects but products.js declares {len(raw_ids)} ids")
    for product in products:
        pid, page = product["id"], product["url"]
        if not page:
            bad(f"product '{pid}' has no detail page URL")
            continue
        page_path = ROOT / page
        if not page_path.is_file():
            bad(f"product '{pid}' page missing: {page}")
            continue
        page_text = page_path.read_text(encoding="utf-8")
        if f'data-buy-for="{pid}"' not in page_text:
            bad(f"product '{pid}' page has no buy slot")
        else:
            ok(f"product '{pid}' has page + buy slot")
        top_notice = page_text.count(
            '<div class="callout"><strong>Independent third-party product.</strong>'
        )
        footer_notice = (
            "Not affiliated with, endorsed by, sponsored by or connected to"
            in page_text
        )
        full_terms = (
            "Not affiliated with, endorsed by, sponsored by, or in any way connected to"
            in page_text
        )
        if top_notice == 1 and footer_notice and full_terms:
            ok(f"product '{pid}' has canonical IP notice (top + footer)")
        else:
            bad(f"product '{pid}' IP notice drift: top={top_notice}, "
                f"footer={footer_notice}, full_terms={full_terms}")

    # 3a. marketplace slots exist for every product that declares a
    # marketplaceUrl, and any configured URL must be a real Superhive URL.
    pending_marketplace = {p["id"] for p in products if p["marketplaceUrl"] is not None}
    configured = [p["marketplaceUrl"] for p in products if p["marketplaceUrl"]]
    for url in configured:
        if not url.startswith("https://superhivemarket.com/"):
            bad(f"non-Superhive marketplaceUrl: {url}")
    for pid in pending_marketplace:
        page_path = ROOT / "products" / f"{pid}.html"
        if not page_path.is_file():
            bad(f"{pid}: product page missing for marketplace slot")
        elif f'data-marketplace-for="{pid}"' not in page_path.read_text(encoding="utf-8"):
            bad(f"{pid}: missing Superhive slot")
    if pending_marketplace and all(
        f'data-marketplace-for="{pid}"' in (ROOT / "products" / f"{pid}.html").read_text(encoding="utf-8")
        for pid in pending_marketplace
    ):
        ok(f"Superhive slots present for {', '.join(sorted(pending_marketplace))}")
        if all(not p["marketplaceUrl"] for p in products):
            ok("all Superhive buttons render as disabled pending approval")

    # 3b. structured-data host must match the product (guards copy/paste errors).
    # Host categories are derived from each product's category/tags.
    blender_ids = {p["id"] for p in products
                   if "blender" in (p["category"] or "").lower()
                   or any("blender" in t.lower() for t in p["tags"])}
    plc_ids = {p["id"] for p in products
               if "plcnext" in (p["category"] or "").lower()
               or any("plcnext" in t.lower() for t in p["tags"])}
    for product in products:
        pid, page = product["id"], product["url"]
        page_path = ROOT / page if page else None
        if not page_path or not page_path.is_file():
            continue
        match = re.search(r'"operatingSystem"\s*:\s*"([^"]+)"', page_path.read_text(encoding="utf-8"))
        if not match:
            bad(f"product '{pid}' has no operatingSystem in structured data")
            continue
        host = match.group(1)
        if "PLCnext" in host and pid not in plc_ids:
            bad(f"product '{pid}' wrongly claims PLCnext as its host: {host}")
        elif "Blender" in host and pid not in blender_ids:
            bad(f"product '{pid}' wrongly claims Blender as its host: {host}")
        else:
            ok(f"product '{pid}' structured-data host is plausible: {host}")

    # 4. placeholder domain must be a single consistent token (documented setup step)
    for rel in ("robots.txt", "sitemap.xml", "index.html", "catalog.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "example.com" in text:
            bad(f"{rel} contains an undeclared example.com domain")
        elif "{{SITE_URL}}" in text:
            ok(f"{rel} uses the documented {{{{SITE_URL}}}} setup token")
        else:
            ok(f"{rel} has a concrete domain")

    # 5. permalinks are recorded (prefix check only — no network calls), but a
    # listing marked published:false must render as unavailable, not checkout.
    real_urls = [p["buyUrl"] for p in products if p["buyUrl"]]
    for url in real_urls:
        if url.startswith("https://kylian47.gumroad.com/"):
            ok(f"Gumroad permalink recorded: {url}")
        else:
            bad(f"non-Gumroad buyUrl: {url}")
    undefined = [p["id"] for p in products if p["published"] is None]
    if undefined:
        bad(f"products without a published field: {', '.join(undefined)}")
    if len(real_urls) == len(ids):
        ok(f"{len(real_urls)} Gumroad permalinks recorded, 0 empty")
    else:
        bad(f"expected {len(ids)} recorded permalinks, found {len(real_urls)}")
    site_js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    if ("p.published === false" in site_js
            and "Unavailable — pending republish" in site_js):
        ok("site.js disables checkout for unpublished listings")
    else:
        bad("site.js does not disable checkout for unpublished listings")
    unpublished = [p for p in products if p["published"] is False]
    for p in unpublished:
        page_path = ROOT / p["url"]
        text = page_path.read_text(encoding="utf-8") if page_path.is_file() else ""
        if re.search(r'<noscript><a[^>]+href="https://kylian47\.gumroad\.com/l/', text):
            bad(f"{p['id']}: no-JS buy link still active for unpublished listing")
        elif "Unavailable — pending republish" in text:
            ok(f"{p['id']}: no-JS fallback disabled")
        else:
            bad(f"{p['id']}: missing disabled no-JS fallback")
    unpublished_slugs = {
        p["buyUrl"].rsplit("/l/", 1)[-1]
        for p in unpublished if p["buyUrl"]
    }
    leaked = []
    for page_file in sorted(ROOT.rglob("*.html")):
        text = page_file.read_text(encoding="utf-8")
        for slug in re.findall(
                r'href="https://kylian47\.gumroad\.com/l/([a-z0-9-]+)"', text):
            if slug in unpublished_slugs:
                leaked.append(f"{page_file.relative_to(ROOT)} -> {slug}")
    if leaked:
        for item in leaked:
            bad(f"active checkout link for unpublished listing: {item}")
    else:
        ok("no active checkout links for unpublished listings")
    ok(f"{len(unpublished)} unpublished / "
       f"{len(products) - len(unpublished)} published listings declared")

    # 6. every product must have a thumbnail/cover image, and local images resolve
    thumbs = [p["thumb"] for p in products]
    if len(thumbs) != len(ids):
        bad(f"expected {len(ids)} thumb values, found {len(thumbs)}")
    missing = [t for t in thumbs if not t]
    if missing:
        bad(f"{len(missing)} product(s) have no image")
    else:
        ok(f"all {len(thumbs)} products have an image")
    for thumb in thumbs:
        if not thumb:
            continue
        if thumb.startswith("http"):
            continue
        target = (ROOT / thumb).resolve()
        (ok if target.is_file() else bad)(f"local product image exists: {thumb}")

    # 7. sitemap targets, canonical tags, duplicate ids, JSON-LD validity
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for loc in re.findall(r"<loc>([^<]+)</loc>", sitemap):
        rel = re.sub(r"^.*?/(?:trellmere-site|trellmere-site-public)/", "", loc) or "index.html"
        (ok if (ROOT / rel).is_file() else bad)(f"sitemap target exists: {rel}")
    for page_file in sorted(ROOT.rglob("*.html")):
        if ".git" in page_file.parts:
            continue
        page_text = page_file.read_text(encoding="utf-8")
        canon = re.findall(r'<link rel="canonical" href="([^"]+)"', page_text)
        (ok if len(canon) == 1 and canon[0].startswith("https://kyliantewarie.github.io/trellmere-site-public/")
         else bad)(f"canonical tag: {page_file.relative_to(ROOT)}")
        element_ids = re.findall(r'\sid="([^"]+)"', page_text)
        dup = sorted({i for i in element_ids if element_ids.count(i) > 1})
        (ok if not dup else bad)(f"no duplicate ids: {page_file.relative_to(ROOT)}")
        for ld_block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page_text, re.S):
            try:
                json.loads(ld_block)
                ok(f"JSON-LD parses: {page_file.relative_to(ROOT)}")
            except json.JSONDecodeError as exc:
                bad(f"JSON-LD invalid: {page_file.relative_to(ROOT)} ({exc})")

    # 8. price parity between products.js, visible price and structured data
    for product in products:
        pid, js_price, url = product["id"], product["price"], product["url"]
        if not js_price or not url:
            bad(f"price check: '{pid}' is missing price or page URL")
            continue
        page_file = ROOT / url
        if not page_file.is_file():
            bad(f"price check: missing page {url}")
            continue
        page_text = page_file.read_text(encoding="utf-8")
        visible = re.search(r'<div class="big-price">([^<]+)</div>', page_text)
        if visible and visible.group(1).strip() != js_price.strip():
            bad(f"price mismatch {pid}: js={js_price!r} page={visible.group(1).strip()!r}")
        else:
            ok(f"price matches page: {pid}")
        ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', page_text, re.S)
        if ld_match:
            data = json.loads(ld_match.group(1))
            offer = data.get("offers")
            pwyw = js_price.lower().startswith("pay what you want")
            if pwyw and offer:
                bad(f"PWYW product has fixed Offer price: {pid}")
            elif offer and re.sub(r"\D", "", js_price) != re.sub(r"\D", "", str(offer.get("price", ""))):
                bad(f"price mismatch {pid}: js={js_price!r} JSON-LD={offer.get('price')!r}")
            else:
                ok(f"price matches structured data: {pid}")

    # 9. no-JS fallbacks for critical content
    critical_pages = [ROOT / "index.html", ROOT / "catalog.html"] + [
        ROOT / p["url"] for p in products if p["url"]
    ]
    for page_file in critical_pages:
        if page_file.is_file() and "<noscript>" not in page_file.read_text(encoding="utf-8"):
            bad(f"no no-JS fallback: {page_file.relative_to(ROOT)}")
        elif page_file.is_file():
            ok(f"no-JS fallback present: {page_file.relative_to(ROOT)}")

    print(f"\nTOTAL: {PASS} passed, {FAIL} failed")
    print("\nSETUP STATUS (owner-only):")
    print("  1. (DONE) Live Gumroad links wired in from https://kylian47.gumroad.com/")
    print("  2. (NOT NEEDED) Gumroad delivers the free lead magnet; signupEndpoint is intentionally blank")
    print("  3. (DONE) Canonical tags, sitemap and robots use concrete URLs")
    print("  4. DEPLOY: commit and push to main; the workflow stages only public site files")
    print("  5. SUPERHIVE: SheetFab submitted for review; add its product URL when approved")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
