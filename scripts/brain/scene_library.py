#!/usr/bin/env python3
"""Scene library + auto-rank — the self-improve ledger IS the library; this ranks it.

Reads 03_ITERATIONS/_selfimprove_ledger.jsonl, keeps gate-passed scenes, and ranks them by
(score desc, acceptance-ok, least product in copy zone) so future rounds can PICK a proven scene
instead of re-generating. Optionally renders the top-N to one contact sheet (local images, no Figma).

  python scripts/scene_library.py --top 15
  python scripts/scene_library.py --room kitchen --top 5 --sheet
Writes 03_ITERATIONS/_scene_library.json (ranked index).
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "03_ITERATIONS/_selfimprove_ledger.jsonl"
OUT = ROOT / "03_ITERATIONS/_scene_library.json"


def load():
    if not LEDGER.exists():
        sys.exit(f"no ledger at {LEDGER} — run selfimprove_loop first")
    rows = []
    for ln in LEDGER.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            rows.append(json.loads(ln))
    return rows


def rank(rows, room=None):
    pool = [r for r in rows if r.get("gate_pass") and r.get("rid")]
    if room:
        pool = [r for r in pool if r.get("room") == room]
    # best first: higher score, acceptance ok, then least brass in the copy zone
    pool.sort(key=lambda r: (r.get("score", 0), 1 if r.get("acc_ok") else 0, -r.get("box_brass", 1)), reverse=True)
    return pool


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--sheet", action="store_true")
    a = ap.parse_args()
    ranked = rank(load(), a.room)
    top = ranked[:a.top]
    OUT.write_text(json.dumps([{k: r.get(k) for k in
                   ("rid", "room", "shot", "palette", "score", "acc_ok", "box_brass", "nw", "nh")}
                   for r in ranked], indent=1), encoding="utf-8")
    print(f"library: {len(ranked)} gate-passed scenes  (wrote {OUT.name})")
    for r in top:
        print(f"  {r.get('score',0):>2}  {('OK ' if r.get('acc_ok') else 'acc')}  "
              f"{r.get('room',''):8}/{r.get('shot',''):5} p{r.get('palette','?')}  {r.get('rid','')}")
    if a.sheet:
        from PIL import Image
        sys.path.insert(0, str(ROOT / "scripts"))
        from board_diff import montage, BOARD
        imgs = []
        for r in top:
            p = ROOT / "03_ITERATIONS" / r["rid"] / "image_01.png"
            if p.exists():
                imgs.append((f"{r.get('score',0)} {r.get('room','')}/{r.get('shot','')} p{r.get('palette','?')}",
                             Image.open(p).convert("RGB")))
        sheet = montage(imgs, cols=5, tw=300)
        if sheet:
            BOARD.mkdir(parents=True, exist_ok=True)
            out = BOARD / "library_top.png"
            sheet.save(out)
            print(f"sheet: {out}")


if __name__ == "__main__":
    main()
