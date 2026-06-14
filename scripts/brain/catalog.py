#!/usr/bin/env python3
"""RS product catalog — single source of truth for category, real dimensions, and revenue rank.

Backed by assets/catalog/products.tsv. Consumed by:
  - qc_gate.py   -> real dims for the SCALE check (is the product 3-5x too big?)
  - fixture_swap.py -> top-revenue SKU per category (swap candidates)
  - compose_prompt.py / hf_gen.py -> dims for true-scale prompts + merch injection (replaces hard-coded MERCH)

Revenue figures are the team's curated Shopify gross_sales (90d/365d) from 02_FEEDBACK_LOG + merch-map.
`catalog.py rank` re-ranks per category from the tsv; `catalog.py refresh` is the hook to repull from
Shopify analytics (per-product net sales) when that query path is wired — until then it preserves the
curated seed values (real, not fabricated) and only re-ranks.

CLI:
  python scripts/catalog.py validate              # schema + packshot existence + dims presence
  python scripts/catalog.py rank                  # re-rank per category by gross_sales, write back
  python scripts/catalog.py top <category> [n]    # top-N SKUs by revenue in a category
  python scripts/catalog.py get <sku>             # one row
"""
from __future__ import annotations
import csv, os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))            # scripts/brain
ROOT = os.path.dirname(os.path.dirname(_HERE))                 # repo root
# creative-os location first (catalog moved here in the transplant), then legacy
# ads-gen layout, then env override. First existing path wins.
_CANDIDATES = [
    os.environ.get("RS_CATALOG_TSV", ""),
    os.path.join(ROOT, "01_BRANDS", "RS", "ASSETS", "catalog", "products.tsv"),
    os.path.join(_HERE, "..", "assets", "catalog", "products.tsv"),   # legacy
]
TSV = next((p for p in _CANDIDATES if p and os.path.exists(p)),
           os.path.join(ROOT, "01_BRANDS", "RS", "ASSETS", "catalog", "products.tsv"))
COLS = ["sku", "name", "category", "dims_in", "dims_source", "revenue_rank",
        "gross_sales_usd", "period", "packshot", "active", "finish"]

# Canonical on-disk packshot dir in creative-os (the transplant moved assets here).
PRODUCTS_DIR = os.path.join(ROOT, "01_BRANDS", "RS", "ASSETS", "products")


def find_packshot(sku_or_row, rows: list[dict] | None = None):
    """Resolve a SKU (or row dict) to the REAL absolute packshot path on disk.

    Tries, in order, until one EXISTS:
      a) the stored `packshot` path joined to ROOT  (legacy ads-gen layout)
      b) the stored basename under PRODUCTS_DIR      (creative-os layout)
      c) the basename with the other common ext (.png<->.jpg) under PRODUCTS_DIR
    Returns the first existing absolute path, else None (caller logs the miss).
    """
    row = sku_or_row if isinstance(sku_or_row, dict) else get(sku_or_row, rows)
    if not row:
        return None
    stored = (row.get("packshot") or "").strip()
    if not stored:
        return None
    base = os.path.basename(stored)
    stem, ext = os.path.splitext(base)
    other = ".jpg" if ext.lower() == ".png" else ".png"
    for cand in (
        os.path.join(ROOT, stored),                 # a) as-stored
        os.path.join(PRODUCTS_DIR, base),           # b) basename in canonical dir
        os.path.join(PRODUCTS_DIR, stem + other),   # c) alt extension
    ):
        if cand and os.path.exists(cand):
            return os.path.abspath(cand)
    return None


def load(path: str = TSV) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = [dict(r) for r in csv.DictReader(f, delimiter="\t")]
    for r in rows:
        r["_active"] = r.get("active", "1").strip() == "1"
        r["_gross"] = float(r["gross_sales_usd"]) if r.get("gross_sales_usd", "").strip() else 0.0
        r["_rank"] = int(r["revenue_rank"]) if r.get("revenue_rank", "").strip() else 999
        r["_dims"] = parse_dims(r.get("dims_in", ""))
    return rows


def parse_dims(s: str):
    """'2.75x4.5x0.3' (in) -> {'w':2.75,'h':4.5,'d':0.3}. Returns None if unparseable."""
    s = (s or "").strip().lower().replace("in", "").replace('"', "")
    if not s:
        return None
    try:
        parts = [float(p) for p in s.split("x")]
    except ValueError:
        return None
    keys = ["w", "h", "d"]
    return {keys[i]: parts[i] for i in range(min(len(parts), 3))}


def by_category(rows: list[dict] | None = None) -> dict[str, list[dict]]:
    rows = rows if rows is not None else load()
    out: dict[str, list[dict]] = {}
    for r in rows:
        if r["_active"]:
            out.setdefault(r["category"], []).append(r)
    for cat in out:
        out[cat].sort(key=lambda r: (-r["_gross"], r["_rank"]))
    return out


def top_in_category(category: str, n: int = 50, rows: list[dict] | None = None) -> list[dict]:
    """Top-N SKUs by revenue in a category — the swap-candidate list for fixture_swap.py."""
    return by_category(rows).get(category, [])[:n]


def get(sku: str, rows: list[dict] | None = None) -> dict | None:
    rows = rows if rows is not None else load()
    return next((r for r in rows if r["sku"] == sku), None)


def find_by_name(name: str, rows: list[dict] | None = None) -> dict | None:
    """Resolve a product name OR a distinctive keyword to its SKU row.

    Order: (1) exact name/sku match; (2) the stored name/sku contained in the query
    (the original full-name behavior — e.g. brain passes the full product name);
    (3) the query contained in a stored name/sku (bare-keyword path — "Teva",
    "Carissa"). For (3), if the keyword matches MORE THAN ONE SKU it is ambiguous →
    return None rather than guessing. Signature + return shape unchanged.
    """
    rows = rows if rows is not None else load()
    nl = name.lower().strip()
    if not nl:
        return None

    def sku_words(r):
        return r["sku"].replace("-", " ").lower()

    # (1) exact match on name or spaced-sku
    for r in rows:
        if r["name"].lower() == nl or sku_words(r) == nl:
            return r
    # (2) stored name/sku appears inside the query (full-name callers)
    for r in rows:
        if r["name"].lower() in nl or sku_words(r) in nl:
            return r
    # (3) query appears inside a stored name/sku (bare keyword) — only if UNAMBIGUOUS
    hits = [r for r in rows if nl in r["name"].lower() or nl in sku_words(r)]
    if len(hits) == 1:
        return hits[0]
    return None


def validate(rows: list[dict] | None = None) -> tuple[int, list[str]]:
    rows = rows if rows is not None else load()
    problems = []
    for r in rows:
        if not r.get("sku") or not r.get("category"):
            problems.append(f"{r.get('sku','?')}: missing sku/category")
        if r["_dims"] is None:
            problems.append(f"{r['sku']}: unparseable dims_in '{r.get('dims_in')}'")
        pk = find_packshot(r)
        if not r.get("packshot") or pk is None:
            problems.append(f"{r['sku']}: packshot missing ({r.get('packshot')})")
    return len(rows), problems


def rank(path: str = TSV):
    """Re-rank revenue_rank within each category by gross_sales (desc); write back."""
    rows = load(path)
    cats = by_category(rows)
    rankmap = {}
    for cat, items in cats.items():
        for i, r in enumerate(items, 1):
            rankmap[r["sku"]] = i
    for r in rows:
        if r["sku"] in rankmap:
            r["revenue_rank"] = str(rankmap[r["sku"]])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return rankmap


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "validate"
    if cmd == "validate":
        n, probs = validate()
        print(f"catalog: {n} SKUs, {len(probs)} problems")
        for p in probs:
            print("  -", p)
        cats = by_category()
        print("categories:", {c: len(v) for c, v in cats.items()})
        sys.exit(1 if probs else 0)
    elif cmd == "rank":
        rm = rank()
        print("re-ranked:", json.dumps(rm, indent=2))
    elif cmd == "top":
        cat = args[1]; n = int(args[2]) if len(args) > 2 else 50
        for r in top_in_category(cat, n):
            print(f"{r['revenue_rank']:>2}  {r['name']:<34} ${r['_gross']:>8.0f}  {r['packshot']}")
    elif cmd == "get":
        r = get(args[1])
        print(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}, indent=2) if r else "not found")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
