# Trellmere storefront

A dependency-free static marketing site for the Trellmere product catalogue.
No frameworks, no build step, no runtime, no dependencies for the site itself.

Gumroad store: https://kylian47.gumroad.com/

> **Availability:** products are temporarily unavailable while compliance work
> is completed. The free K-Factor & Bend Allowance cheat sheet is available now.
> Follow the Gumroad store for release updates.

## Catalogue (EUR, planned)

| Product | Gumroad | Price | Status |
|---|---|---|---|
| SheetFab | `/l/sheetfab` | €27 | Unavailable |
| SplitForge | `/l/splitforge` | €11 | Unavailable |
| DraftForge | `/l/draftforge` | €27 | Unavailable |
| Backup Guardian | `/l/kgbmhi` | Pay what you want | Unavailable |
| Smart Appliance Privacy Shield | `/l/vamzm` | Pay what you want | Unavailable |
| VoltWise Pro | `/l/nsfwqe` | €24 | Unavailable |
| IEC 61131-3 Function Block Library | `/l/sdjow` | €25 | Unavailable |
| Control Library for PLCnext | `/l/hikaxs` | €45 | Unavailable |
| EdgeStack for PLCnext | `/l/jvzcmc` | €45 | Unavailable |
| IIoT Pro | `/l/iiot-pro` | €89 | Unavailable |
| K-Factor cheat sheet | `/l/k-factor-cheat-sheet` | Free | Available |

`assets/products.js` is the single source of truth for product data used by the
site. Prices there are EUR.

## What is here

| Path | Purpose |
|---|---|
| `index.html` | Homepage: hero, catalogue links, free cheat sheet CTA, guides |
| `catalog.html` | Product catalog (renders from `assets/products.js`) |
| `products/*.html` | SEO product pages |
| `guides/*.html` | Technical articles (sheet metal, HA backups, appliance privacy) |
| `lead-magnets/` | Free K-Factor cheat sheet (HTML + printable PDF) |
| `assets/products.js` | Product data and config |
| `assets/site.js`, `assets/style.css` | Rendering and responsive dark theme |
| `.github/workflows/deploy.yml` | Verify and deploy public site files to GitHub Pages |
| `tools/verify_site.py` | Local integrity checks (stdlib-only, no network calls) |
| `sitemap.xml`, `robots.txt` | Search indexing |

## Adding a product

Add one object to `window.TRELLMERE_PRODUCTS` and one `products/<id>.html` page.
The catalog and homepage update automatically. Add the page to `sitemap.xml`.
Use a clearly marked placeholder URL while a product is unpublished.

## Verification

```powershell
python tools/verify_site.py
python -m http.server 8000   # http://localhost:8000
```

The GitHub Actions workflow runs the same verifier before deploying. It stages
only `index.html`, `catalog.html`, `robots.txt`, `sitemap.xml`, `.nojekyll` and
the `assets`, `guides`, `lead-magnets` and `products` directories.
