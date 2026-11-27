# Brand deployment — Trellmere

Status: **prepared locally, not deployed**. The live site still serves the
pre-rebrand identity; canonical URLs in this repository already use
`trellmere-site`.

## What is already done locally

- All active site copy, canonical URLs, sitemap, robots, JS globals
  (`TRELLMERE_PRODUCTS`, `TRELLMERE_CONFIG`) and User-Agent now use Trellmere.
- Blanket claim "Every product is tested before release" replaced with an
  honest, per-product disclosure; homepage now states PLCnext products are
  structurally validated and simulation-reviewed, **not compiled in Engineer
  or hardware-tested**.
- `verify_site.py`: **151 passed, 0 failed**.
- Local git remote changed to:
  `https://github.com/kyliantewarie/trellmere-site.git`

## What I cannot do without access

1. **GitHub**: rename the repository `toolform-site` → `trellmere-site`, or
   create the new repo and configure Pages. Then commit and push `main`.
   A GitHub token or authenticated git session is required.
2. **GitHub Pages**: ensure `trellmere-site` is published. Current live check:
   - `https://kyliantewarie.github.io/trellmere-site-public/` → **404**
   - `https://kyliantewarie.github.io/toolform-site/` → **200, still Toolform**
3. **Superhive**: change the creator slug from `creators/toolform` to
   `creators/trellmere` in account settings. Current check for
   `creators/trellmere` returns the generic marketplace page, not your store.
4. **Gumroad**: verify published state, prices, currency, variants and
   descriptions with a fresh access token. No token is present in the workspace.
   If you provide one, I will use it and delete it immediately.

## Verification after deployment

```
verify: https://kyliantewarie.github.io/trellmere-site-public/ returns 200 with Trellmere branding
verify: old toolform-site URL redirects or is retired
verify: https://superhivemarket.com/creators/trellmere shows your products
python passive-income-site/tools/verify_site.py  # expects 151 passed, 0 failed
gumroad products list --all --json               # published state matches CRA_PRODUCT_STATUS.md
```

## Important

Do not publish any PLCnext product until the CRA Art. 14 gates in
`../gumroad/profile-refresh/CRA_RESOLUTION_PLAN.md` are complete.
