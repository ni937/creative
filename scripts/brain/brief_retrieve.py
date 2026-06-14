#!/usr/bin/env python3
"""Retrieval over Keith's extracted brief corpus — the bridge from his method to our generation.

Given a target (product / persona / angle / visual-style / copy-style), return:
  - matching real CONCEPTS (their on-image copy = tone/voice exemplars), and
  - the actual REFERENCE IMAGE files Keith anchored those concepts on (for --ref).

Backed by 04_KNOWLEDGE/_research/keith-briefs.json (328 concepts) + keith-refs-index.json (413 refs,
tagged with each concept's persona/angle/style; image files in assets/references/keith/, gitignored).

CLI:
  python scripts/brief_retrieve.py --product switch                  # concepts + refs for a product
  python scripts/brief_retrieve.py --product dimmer --angle "Find Your Style"
  python scripts/brief_retrieve.py --persona A1-Homemaker --copy-style Editorial --limit 8
  python scripts/brief_retrieve.py --product switch --refs-only       # just existing ref file paths (for --ref)
"""
from __future__ import annotations
import argparse, json, os

_HERE = os.path.dirname(os.path.abspath(__file__))            # scripts/brain
ROOT = os.path.dirname(os.path.dirname(_HERE))                 # repo root
# creative-os layout: research corpus lives under the RS brand; refs under RS/REFS.
R = os.path.join(ROOT, "01_BRANDS", "RS", "KNOWLEDGE", "_research")
REFDIR = os.path.join(ROOT, "01_BRANDS", "RS", "REFS", "keith")


def _load(name):
    with open(os.path.join(R, name), encoding="utf-8") as f:
        return json.load(f)


def find_concepts(product=None, persona=None, angle=None, visual_style=None, copy_style=None,
                  filled_copy=False, briefs=None):
    briefs = briefs if briefs is not None else _load("keith-briefs.json")
    def hit(b):
        if product and product.lower() not in (b.get("product_name", "").lower()): return False
        if persona and persona.lower() not in (b.get("persona", "").lower()): return False
        if angle and angle.lower() not in (b.get("angle", "").lower()): return False
        if visual_style and visual_style.lower() not in (b.get("visual_style", "").lower()): return False
        if copy_style and copy_style.lower() not in (b.get("copy_style", "").lower()): return False
        if filled_copy and not (b.get("copy1", "").strip()): return False
        return True
    return [b for b in briefs if hit(b)]


def refs_for(concepts, refs=None, existing_only=True):
    """Ref image file paths for the given concepts (joined by page+concept)."""
    refs = refs if refs is not None else _load("keith-refs-index.json")
    keys = {(c["page"], c["concept"]) for c in concepts}
    out = []
    for r in refs:
        if (r["page"], r["concept"]) in keys and r.get("file"):
            p = os.path.join(REFDIR, r["file"])
            if (not existing_only) or os.path.exists(p):
                out.append(p)
    return out


def best_refs(product=None, persona=None, angle=None, visual_style=None, n=4):
    """Top-N ref image paths for a generation target — widen the net until we have refs."""
    for filt in (dict(product=product, persona=persona, angle=angle, visual_style=visual_style),
                 dict(product=product, angle=angle),
                 dict(product=product, visual_style=visual_style),
                 dict(product=product),
                 dict(angle=angle, visual_style=visual_style)):
        filt = {k: v for k, v in filt.items() if v}
        if not filt:
            continue
        rfs = refs_for(find_concepts(**filt))
        if rfs:
            return rfs[:n]
    return []


def main():
    ap = argparse.ArgumentParser(description="Retrieve Keith concepts + reference images for a target")
    ap.add_argument("--product"); ap.add_argument("--persona"); ap.add_argument("--angle")
    ap.add_argument("--visual-style", dest="visual_style"); ap.add_argument("--copy-style", dest="copy_style")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--refs-only", action="store_true", help="print only existing ref file paths (for --ref)")
    a = ap.parse_args()
    cs = find_concepts(a.product, a.persona, a.angle, a.visual_style, a.copy_style)
    rfs = refs_for(cs)
    if a.refs_only:
        print("\n".join(rfs))
        return
    print(f"== {len(cs)} concepts, {len(rfs)} reference images available ==")
    for b in cs[:a.limit]:
        print(f"\n[{b['page']}/{b['concept']}] {b['product_name']}  |  {b['persona']} · {b['visual_style']} · {b['angle']} · {b['copy_style']}")
        for k in ("copy1", "copy2", "copy3"):
            if b.get(k, "").strip():
                print("   • " + b[k].replace("\n", " / ")[:90])
    if rfs:
        print(f"\n-- reference images ({len(rfs)}) --")
        for p in rfs[:a.limit]:
            print("   " + os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
