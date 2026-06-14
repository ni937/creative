#!/usr/bin/env python3
"""creative-os — Figma harvest (RS training corpus).

Deterministic, rate-limit-aware harvest of FINISHED ad frames from a Figma board:
  - fetch section nodes (depth-limited; full-file endpoint 429s)
  - keep schema-named frames that contain a TEXT layer (finished = copy/logo/CTA on it)
  - dedupe by concept+version+aspect
  - export rendered PNGs (batched) into 01_BRANDS/RS/REFS/<product-slug>/
  - parse names -> tags, append image->layout pairs, tally layout archetypes
  - checkpoint as it goes (resumable)

Stdlib only. FIGMA_TOKEN read from creative-os/.env.

Usage:
  python scripts/harvest.py --file RKALaxBpCT1nYPAb1XYI26 --page "Page 1" \
      --sections 4:1970,8:8,8:19,8:30,8:41,1442:8 --label may
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "01_BRANDS/RS/REFS")
PAIRS = os.path.join(ROOT, "01_BRANDS/RS/LAYOUT_PAIRS.md")
KNOW = os.path.join(ROOT, "04_KNOWLEDGE")
SCHEMA = re.compile(r'^B\d+[_-]C\d')
ASPECTS = ("2x1", "2X1", "4x5", "4X5", "9x16", "9X16", "2x5", "1x1", "FAB")

def token():
    for line in open(os.path.join(ROOT, ".env")):
        if line.startswith("FIGMA_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("no FIGMA_TOKEN in .env")

TOK = token()

def api(url, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"X-Figma-Token": TOK})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 25 + i * 10
                print(f"  429, backoff {wait}s", flush=True); time.sleep(wait); continue
            raise
    raise SystemExit(f"gave up: {url}")

def download(url, path, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
            return True
        except Exception as e:
            time.sleep(5 + i * 5)
    return False

def has_text(n):
    for c in n.get("children", []):
        if c.get("type") == "TEXT" or has_text(c):
            return True
    return False

def text_samples(n, out):
    for c in n.get("children", []):
        if c.get("type") == "TEXT" and c.get("characters"):
            out.append(c["characters"].strip().replace("\n", " ")[:60])
        text_samples(c, out)
    return out

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40] or "misc"

def parse_name(name):
    parts = [p.strip() for p in name.split("_")]
    tags = {"raw": name, "batch": "", "concept": "", "version": "", "product": "",
            "style": "", "aspect": "", "fields": parts}
    if parts:
        m = re.match(r'B(\d+)', parts[0])
        if m: tags["batch"] = m.group(1)
    m = re.search(r'C(\d+)', name)
    if m: tags["concept"] = m.group(1)
    m = re.search(r'_V(\d+)_', "_" + name + "_")
    if m: tags["version"] = m.group(1)
    for a in ASPECTS:
        if name.endswith("_" + a) or name.endswith(a):
            tags["aspect"] = a.lower(); break
    for s in ("Modern", "Heritage", "Traditional", "Midcentury", "Minimalist", "Timeless"):
        if s in parts: tags["style"] = s; break
    # product = field after V<n> if present, else field index 3
    prod = ""
    for i, p in enumerate(parts):
        if re.fullmatch(r'V\d+', p) and i + 1 < len(parts):
            prod = parts[i + 1]; break
    if not prod and len(parts) > 3:
        prod = parts[3]
    tags["product"] = prod
    return tags

def collect_finished(node, acc):
    for c in node.get("children", []):
        t = c.get("type")
        nm = (c.get("name") or "").strip()
        if t in ("FRAME", "COMPONENT", "INSTANCE") and SCHEMA.match(nm):
            if has_text(c):
                acc.append(c)
        collect_finished(c, acc)
    return acc

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--sections", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--page", default="")
    a = ap.parse_args()

    os.makedirs(KNOW, exist_ok=True)
    ckpt = os.path.join(KNOW, f"harvest-progress-{a.label}.md")

    ids = a.sections
    print(f"fetching sections {ids} of {a.file} ...", flush=True)
    data = api(f"https://api.figma.com/v1/files/{a.file}/nodes?ids={ids}&depth=8")
    finished = []
    for nid, node in data["nodes"].items():
        if node and node.get("document"):
            collect_finished(node["document"], finished)
    print(f"finished frames found: {len(finished)}", flush=True)

    # dedupe by concept+version+aspect (keep first); keep map id->meta
    seen = {}
    uniq = []
    for fr in finished:
        tg = parse_name(fr["name"])
        key = (tg["concept"], tg["version"], tg["aspect"])
        if key in seen:
            continue
        seen[key] = fr["id"]
        uniq.append((fr, tg))
    print(f"unique (concept+version+aspect): {len(uniq)}", flush=True)

    # batch image export
    id_list = [fr["id"] for fr, _ in uniq]
    url_map = {}
    B = 20
    for i in range(0, len(id_list), B):
        chunk = id_list[i:i + B]
        q = ",".join(chunk)
        r = api(f"https://api.figma.com/v1/images/{a.file}?ids={q}&format=png&scale=1")
        url_map.update(r.get("images", {}) or {})
        print(f"  export {i+len(chunk)}/{len(id_list)}", flush=True)
        time.sleep(1)

    pairs_out = []
    exported = 0
    products = set(); concepts = set()
    for idx, (fr, tg) in enumerate(uniq):
        prod_slug = slug(tg["product"] or "misc")
        d = os.path.join(REFS, prod_slug)
        os.makedirs(d, exist_ok=True)
        u = url_map.get(fr["id"])
        fid = fr["id"].replace(":", "-")
        img_rel = f"REFS/{prod_slug}/{fid}.png"
        if u and download(u, os.path.join(d, f"{fid}.png")):
            exported += 1
        products.add(tg["product"]); concepts.add(tg["concept"])
        copy = text_samples(fr, [])
        pairs_out.append(
            f"- **{tg['product'] or '?'}** (C{tg['concept']} V{tg['version']} · {tg['style'] or '?'} · {tg['aspect'] or '?'})\n"
            f"  - image: `{img_rel}`\n"
            f"  - copy: {' | '.join(copy[:4]) if copy else '(none read)'}\n"
            f"  - name: `{tg['raw']}`\n"
        )
        if (idx + 1) % 25 == 0:
            with open(ckpt, "w") as f:
                f.write(f"# harvest {a.label}\nprocessed {idx+1}/{len(uniq)} | exported {exported}\nlast: {fr['name']}\n")
            print(f"  processed {idx+1}/{len(uniq)} exported {exported}", flush=True)

    # append pairs
    with open(PAIRS, "a") as f:
        f.write(f"\n\n## Harvest: {a.label} ({len(pairs_out)} pairs)\n\n")
        f.write("".join(pairs_out))
    with open(ckpt, "w") as f:
        f.write(f"# harvest {a.label} DONE\nunique {len(uniq)} | exported {exported}\n"
                f"products {len(products)} | concepts {len(concepts)}\n")
    print(f"DONE {a.label}: unique {len(uniq)} exported {exported} "
          f"products {len(products)} concepts {len(concepts)}", flush=True)

if __name__ == "__main__":
    main()
