#!/usr/bin/env python3
"""Fail CI if deal YAML is malformed, duplicated, or sloppy."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "developer-tools",
    "laravel-php",
    "design",
    "ui-kits",
    "courses",
    "books",
    "starter-kits",
    "mobile",
    "hosting",
}
REQUIRED = ("name", "url", "category", "offer", "description")
SLOP = re.compile(
    r"chatgpt wrapper|all-in-one ai|10,000\+|waitlist only|coming soon",
    re.I,
)


def parse(path: Path) -> list[dict]:
    deals, cur = [], None
    if not path.exists():
        return deals
    for line in path.read_text().splitlines():
        if line.startswith("  - name:"):
            if cur:
                deals.append(cur)
            cur = {"name": line.split(":", 1)[1].strip().strip('"'), "_file": path.name}
        elif cur and line.startswith("    ") and ":" in line:
            k, v = line.strip().split(":", 1)
            cur[k] = v.strip().strip('"')
    if cur:
        deals.append(cur)
    return deals


def main() -> int:
    errors = []
    deals = []
    for year in ("2025", "2026"):
        deals.extend(parse(ROOT / "deals" / f"{year}.yaml"))

    names, urls = set(), set()
    for d in deals:
        loc = f"{d.get('_file')}: {d.get('name', '?')}"
        for key in REQUIRED:
            if not d.get(key):
                errors.append(f"{loc}: missing {key}")
        url = d.get("url", "")
        if url and not url.startswith("https://"):
            errors.append(f"{loc}: url must be https")
        if d.get("category") not in CATEGORIES:
            errors.append(f"{loc}: invalid category {d.get('category')!r}")
        desc = d.get("description", "")
        if len(desc) > 180:
            errors.append(f"{loc}: description too long ({len(desc)} chars)")
        if SLOP.search(" ".join(d.get(k, "") for k in REQUIRED)):
            errors.append(f"{loc}: looks like slop copy")
        name_key = d.get("name", "").strip().lower()
        if name_key in names:
            errors.append(f"{loc}: duplicate name")
        names.add(name_key)
        # same vendor may list more than one product

    if errors:
        print("validation failed:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"ok: {len(deals)} deals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
