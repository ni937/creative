#!/usr/bin/env python3
"""Figma puller — enumerate frames + bulk-export PNGs from the PDP Gallery Lifestyles board.

This is the scalable answer to "get ALL the frames." The MCP page-walk times out on this huge
board; the Figma REST API does not — `?depth=N` lists frames shallowly, and /v1/images bulk-exports
many node IDs in ONE call.

TOKEN (read-only Personal Access Token):
  Put it in credentials.toml as:  [figma]\n  pat = "figd_..."
  OR set env FIGMA_TOKEN, OR pass --token.
  Create one: Figma → Settings → Security → Personal access tokens → scope "File content: read".

USAGE:
  python scripts/figma_pull.py enumerate --depth 2                 # every product frame (id, name, size)
  python scripts/figma_pull.py enumerate --depth 3                 # + scenes inside each product
  python scripts/figma_pull.py children 11148:2029                 # list scenes in one product frame
  python scripts/figma_pull.py export --ids 10178:1035,10670:12 --scale 2 --out assets/figma-library
  python scripts/figma_pull.py pull 11148:2029 --out assets/figma-library/eazer   # all scenes of a product
"""
from __future__ import annotations
import argparse, os, sys, urllib.parse
from pathlib import Path
import requests
try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
FILE_KEY_DEFAULT = "Pf16d4S9nlThp1pAST445A"
API = "https://api.figma.com/v1"


def get_token(arg=None) -> str:
    if arg:
        return arg
    if os.environ.get("FIGMA_TOKEN"):
        return os.environ["FIGMA_TOKEN"]
    for p in (ROOT / "credentials.toml", Path(os.path.expanduser("~/.openclaw/credentials.toml"))):
        if p.exists():
            d = tomllib.load(open(p, "rb"))
            t = (d.get("figma") or {}).get("pat")
            if t:
                return t
    sys.exit("No Figma token. Add [figma].pat to credentials.toml, set FIGMA_TOKEN, or pass --token. "
             "Create one at Figma → Settings → Security → Personal access tokens (File content: read).")


def _h(tok):
    return {"X-Figma-Token": tok}


def get_json(url, tok):
    r = requests.get(url, headers=_h(tok), timeout=120)
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
    return r.json()


def _walk(node, depth, cur=0, pad=""):
    t = node.get("type")
    if t in ("FRAME", "COMPONENT", "INSTANCE", "GROUP", "SECTION"):
        box = node.get("absoluteBoundingBox") or {}
        sz = f' {int(box.get("width", 0))}x{int(box.get("height", 0))}' if box else ""
        print(f'{pad}{node.get("id")}\t{t}\t{node.get("name","")}{sz}')
    if cur < depth:
        for c in node.get("children", []):
            _walk(c, depth, cur + 1, pad + "  ")


def cmd_enumerate(a, tok):
    data = get_json(f"{API}/files/{a.key}?depth={a.depth}", tok)
    _walk(data["document"], a.depth)


def cmd_children(a, tok):
    data = get_json(f"{API}/files/{a.key}/nodes?ids={urllib.parse.quote(a.node)}", tok)
    doc = data["nodes"][a.node]["document"]
    for c in doc.get("children", []):
        box = c.get("absoluteBoundingBox") or {}
        print(f'{c["id"]}\t{c.get("type")}\t{c.get("name")}\t{int(box.get("width",0))}x{int(box.get("height",0))}')


def _img_urls(ids, key, tok, scale):
    """Return {id:url} for a batch, or None if Figma rejects it (too large/many)."""
    q = urllib.parse.quote(",".join(ids))
    r = requests.get(f"{API}/images/{key}?ids={q}&format=png&scale={scale}",
                     headers=_h(tok), timeout=180)
    if r.status_code != 200:
        return None
    return r.json().get("images") or {}


def _export(ids, key, tok, scale, out, chunk=6):
    """Robust bulk export: small chunks, adaptive split on 400, skip-and-continue."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    saved = skipped = 0
    i = 0
    while i < len(ids):
        batch = ids[i:i + chunk]
        urls = _img_urls(batch, key, tok, scale)
        if urls is None:                          # "too large or too many" -> split
            if len(batch) > 1:
                chunk = max(1, chunk // 2)
                continue                          # retry same position, smaller chunk
            print(f"  [skip] {batch[0]} (render rejected)")
            skipped += 1
            i += 1
            continue
        for nid, url in urls.items():
            if not url:
                print(f"  [skip] {nid} (no render)")
                skipped += 1
                continue
            try:
                (out / f'{nid.replace(":", "-")}.png').write_bytes(
                    requests.get(url, timeout=300).content)
                saved += 1
            except Exception as e:                # noqa: BLE001
                print(f"  [skip] {nid} ({e})")
                skipped += 1
        i += len(batch)
        print(f"  ...{saved} saved / {i} processed of {len(ids)}")
    print(f"exported {saved}/{len(ids)} (skipped {skipped})")


def cmd_export(a, tok):
    _export([s.strip() for s in a.ids.split(",") if s.strip()], a.key, tok, a.scale, a.out)


def cmd_pull(a, tok):
    data = get_json(f"{API}/files/{a.key}/nodes?ids={urllib.parse.quote(a.node)}", tok)
    doc = data["nodes"][a.node]["document"]
    kids = [c["id"] for c in doc.get("children", [])
            if c.get("type") in ("FRAME", "COMPONENT", "INSTANCE", "RECTANGLE", "GROUP")
            and not c.get("visible") is False]
    print(f"{len(kids)} children of {a.node}")
    if kids:
        _export(kids, a.key, tok, a.scale, a.out)


def cmd_comments(a, tok):
    """Read pinned comments (human feedback) — maps to frames by node_id. Headless via REST."""
    data = get_json(f"{API}/files/{a.key}/comments", tok)
    rows = data.get("comments", [])
    print(f"# {len(rows)} comments on file {a.key}")
    for c in rows:
        meta = c.get("client_meta") or {}
        node = meta.get("node_id") or ""
        state = "resolved" if c.get("resolved_at") else "OPEN"
        who = (c.get("user") or {}).get("handle", "")
        msg = (c.get("message") or "").replace("\n", " ").strip()
        print(f'{c.get("created_at","")}\t{state}\t{who}\t{node}\t{msg}')


def main():
    ap = argparse.ArgumentParser(description="Figma enumerate + bulk export")
    ap.add_argument("--key", default=FILE_KEY_DEFAULT)
    ap.add_argument("--token")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("enumerate"); e.add_argument("--depth", type=int, default=2)
    c = sub.add_parser("children"); c.add_argument("node")
    x = sub.add_parser("export"); x.add_argument("--ids", required=True); x.add_argument("--scale", type=float, default=2); x.add_argument("--out", default="assets/figma-library")
    p = sub.add_parser("pull"); p.add_argument("node"); p.add_argument("--scale", type=float, default=2); p.add_argument("--out", default="assets/figma-library")
    sub.add_parser("comments")
    a = ap.parse_args()
    tok = get_token(a.token)
    {"enumerate": cmd_enumerate, "children": cmd_children, "export": cmd_export,
     "pull": cmd_pull, "comments": cmd_comments}[a.cmd](a, tok)


if __name__ == "__main__":
    main()
