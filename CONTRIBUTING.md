# Contributing

Thanks for helping keep this list actually useful.

## What we take

Software, design tools, UI kits, courses, and books that developers or designers pay for.

Your product should:

- Have been **publicly available for at least 6 months**, or come from a company people already know
- Have a **pricing page** (or a clear one-time price)
- Be a **real product**, not a waitlist, Notion doc, or “ChatGPT wrapper launched last month”
- Offer a **real Black Friday / Cyber Monday discount** (percent off, a code, or a named sale window)

## What we close without merging

- AI slop: generic landing pages, “10,000+ AI tools in one”, no changelog, no customers
- Hardware, gadgets, and Amazon listings
- Duplicate products (search the YAML first)
- PRs that edit the README by hand (README is generated)
- More than one product in a single PR
- Broken links, missing offer, or missing description

## How to add a deal

1. Fork the repo.
2. Add **one** entry to `deals/2026.yaml` (or `deals/2025.yaml` only if you are correcting last year).

```yaml
  - name: Your Product
    url: https://yourproduct.com
    category: developer-tools
    offer: 40% OFF with code BFCM2026
    description: One sentence on what it does. No marketing fluff.
```

Valid `category` values:

- `developer-tools`
- `laravel-php`
- `design`
- `ui-kits`
- `courses`
- `books`
- `starter-kits`
- `mobile`
- `hosting`

3. From the repo root:

```bash
python3 scripts/validate.py
python3 scripts/build_readme.py
```

4. Commit the YAML **and** the regenerated `README.md`.
5. Open a pull request. Title it `Add Your Product`.

We usually review within a few days. If we decline, it is not personal. The bar is the point of this list.

Merged deals may also be picked up for [blackfridaydeals.dev](https://blackfridaydeals.dev).
