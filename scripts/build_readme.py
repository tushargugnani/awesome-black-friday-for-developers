#!/usr/bin/env python3
"""Regenerate README.md from deals/*.yaml."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path("/workspace")))
# inline copy of renderer so the published repo is self-contained

CATEGORIES = [
    ("developer-tools", "Developer Tools"),
    ("laravel-php", "Laravel & PHP"),
    ("design", "Design Tools"),
    ("ui-kits", "UI Kits & Templates"),
    ("courses", "Courses"),
    ("books", "Books"),
    ("starter-kits", "Starter Kits"),
    ("mobile", "Mobile"),
    ("hosting", "Hosting & DevOps"),
]


def parse(path: Path) -> list[dict]:
    deals, cur = [], None
    if not path.exists():
        return deals
    for line in path.read_text().splitlines():
        if line.startswith("  - name:"):
            if cur:
                deals.append(cur)
            cur = {"name": line.split(":", 1)[1].strip().strip('"')}
        elif cur and line.startswith("    ") and ":" in line:
            k, v = line.strip().split(":", 1)
            v = v.strip().strip('"')
            cur[k] = True if v == "true" else v
    if cur:
        deals.append(cur)
    return deals


def md_table(deals: list[dict]) -> str:
    rows = ["| Name | What it is | Offer |", "| --- | --- | --- |"]
    for d in deals:
        rows.append(
            f"| [{d['name'].replace('|', '/')}]({d['url']}) | {d['description'].replace('|', '/')} | {d['offer'].replace('|', '/')} |"
        )
    return "\n".join(rows)


def render(deals_2025: list[dict], deals_2026: list[dict]) -> str:
    by_cat = {k: [] for k, _ in CATEGORIES}
    for d in deals_2025:
        by_cat.setdefault(d["category"], []).append(d)
    toc = []
    for key, label in CATEGORIES:
        n = len(by_cat.get(key, []))
        if n:
            toc.append(f"- [{label}](#{key}) ({n})")
    featured = [d for d in deals_2025 if d.get("featured") is True][:6]
    if len(featured) < 3:
        featured = deals_2025[:3]
    feat = " | ".join(f"**[{d['name']}]({d['url']})**<br>{d['offer']}" for d in featured[:3])
    sections = []
    for key, label in CATEGORIES:
        items = by_cat.get(key) or []
        if items:
            sections.append(f"### {label}\n\n<a id=\"{key}\"></a>\n\n{md_table(items)}\n")
    if deals_2026:
        y2026 = md_table(deals_2026)
    else:
        y2026 = (
            "Nothing live yet. Black Friday 2026 is **Friday 27 November**.\n\n"
            "Want in? Open a pull request with your product (see [CONTRIBUTING.md](CONTRIBUTING.md)). "
            "We review every submission. AI slop, waitlist landing pages, and week-old wrappers get closed.\n"
        )
    return f"""# Awesome Black Friday & Cyber Monday Deals for Developers and Designers 2026

A curated list of **software, design tools, UI kits, and courses** on sale for Black Friday / Cyber Monday.

Maintained by [blackfridaydeals.dev](https://blackfridaydeals.dev). Small on purpose. Every row is reviewed.

[![PRs welcome](https://img.shields.io/badge/PRs-welcome-orange)](CONTRIBUTING.md)
[![Deals](https://img.shields.io/badge/2025%20archive-{len(deals_2025)}%20deals-black)](#2025-archive)

## Why this list

Most GitHub BFCM lists are first-come dumps. This one is not.

- **Software and learning for people who build things.** Developers and designers. No Amazon gadgets.
- **Reviewed.** One product per pull request. We reject AI wrappers, empty landing pages, and copy-paste “all-in-one” tools.
- **Last year is the archive.** Codes below are what actually ran in 2025, so you can see who discounts and by how much. 2026 deals go in their own section when they drop.
- **The website is the live catalog.** This repo is the public, star-able, PR-able index. Full listings stay on [blackfridaydeals.dev](https://blackfridaydeals.dev).

Star the repo if you want a reminder when 2026 deals start landing.

## Featured from 2025

| {feat} |
| :---: | :---: | :---: |

## 2026 deals

{y2026}

## Submit a deal

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Add your product to [`deals/2026.yaml`](deals/2026.yaml) (one product per PR).
3. Run `python3 scripts/validate.py && python3 scripts/build_readme.py`.
4. Open the pull request. We merge quality. We close slop.

If you would rather skip GitHub, [submit on blackfridaydeals.dev](https://blackfridaydeals.dev).

## 2025 archive

These offers ran last Black Friday. Codes are probably expired. Useful as a preview of who shows up and how hard they discount.

{chr(10).join(toc)}

{chr(10).join(sections)}
## Affiliate note

Some links use our referral codes, including links that go through [blackfridaydeals.dev](https://blackfridaydeals.dev). It is how the site stays up. It does not change the discount.

## License

[CC0 1.0](LICENSE) (public domain dedication). Product names and trademarks belong to their owners.
"""


def main() -> int:
    d25 = parse(ROOT / "deals" / "2025.yaml")
    d26 = parse(ROOT / "deals" / "2026.yaml")
    text = render(d25, d26)
    readme = ROOT / "README.md"
    if "--check" in sys.argv:
        if readme.read_text() != text:
            print("README.md is stale. Run python3 scripts/build_readme.py")
            return 1
        print("README.md up to date")
        return 0
    readme.write_text(text)
    print(f"wrote README.md ({len(d25)} in 2025, {len(d26)} in 2026)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
