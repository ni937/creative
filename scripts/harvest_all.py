#!/usr/bin/env python3
"""creative-os — full RS harvest driver (discovery + harvest, all ACTIVE files).

Reuses scripts/harvest.py helpers. Runs unattended in the background:
  1) discover: depth=2 per file -> pages -> section/frame node ids  (DISCO json)
  2) harvest:  /nodes depth=8 per section batch -> collect FINISHED frames
               (B-schema name AND has a TEXT layer = copy/logo/CTA composited)
  3) dedupe by concept+version+aspect, export PNGs into 01_BRANDS/RS/REFS/<product>/
  4) append image->layout pairs to LAYOUT_PAIRS.md, write per-file summary

Resumable: skips files with a DONE marker. Strong 429 backoff via harvest.api().
Stdlib only. FIGMA_TOKEN from creative-os/.env.
"""
import os, sys, json, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harvest as H  # api, collect_finished, parse_name, slug, text_samples, download, ROOT, REFS, PAIRS, KNOW

KNOW = H.KNOW
REFS = H.REFS
PAIRS = H.PAIRS
LOG = os.path.join(KNOW, "harvest-all.log")
DISCO = os.path.join(KNOW, "harvest-discovery.json")
SUMMARY = os.path.join(KNOW, "HARVEST_RESULT.md")

# brand -> [(label, file_key)] ; ACTIVE rows from HARVEST_SOURCES.md
FILES = [
    ("june",   "jFpdxSDRrkog95AJKiIgvN"),
    ("may",    "RKALaxBpCT1nYPAb1XYI26"),
    ("april",  "Z2LyHxkBaKmNHNqnXwuozD"),
    ("aitest", "vbVULvLhbCfCDIokjTVvNY"),
]


def log(m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def discover(key):
    """depth=2 -> document/pages/(sections|frames). Returns (name, pages, all_child_ids)."""
    data = H.api(f"https://api.figma.com/v1/files/{key}?depth=2")
    name = data.get("name")
    pages, ids = [], []
    for page in data.get("document", {}).get("children", []):
        kids = page.get("children", []) or []
        kid_ids = [c["id"] for c in kids]
        ids += kid_ids
        pages.append({
            "page": page.get("name"),
            "n_children": len(kids),
            "types": sorted({c.get("type") for c in kids}),
            "child_ids": kid_ids,
        })
    return name, pages, ids


def harvest_file(label, key, section_ids):
    """Fetch sections at depth=8, collect finished frames, dedupe, export, write pairs."""
    finished = []
    B = 6  # sections per /nodes call
    for i in range(0, len(section_ids), B):
        chunk = section_ids[i:i + B]
        q = ",".join(chunk)
        data = H.api(f"https://api.figma.com/v1/files/{key}/nodes?ids={q}&depth=8")
        for nid, node in (data.get("nodes") or {}).items():
            if node and node.get("document"):
                H.collect_finished(node["document"], finished)
        log(f"  [{label}] sections {i+len(chunk)}/{len(section_ids)} -> finished so far {len(finished)}")
        time.sleep(1.5)

    # dedupe by (concept, version, aspect)
    seen, uniq = {}, []
    for fr in finished:
        tg = H.parse_name(fr["name"])
        k = (tg["concept"], tg["version"], tg["aspect"])
        if k in seen:
            continue
        seen[k] = 1
        uniq.append((fr, tg))
    log(f"  [{label}] finished={len(finished)} unique={len(uniq)}")

    # batch PNG export
    id_list = [fr["id"] for fr, _ in uniq]
    url_map = {}
    for i in range(0, len(id_list), 20):
        chunk = id_list[i:i + 20]
        r = H.api(f"https://api.figma.com/v1/images/{key}?ids={','.join(chunk)}&format=png&scale=1")
        url_map.update(r.get("images", {}) or {})
        log(f"  [{label}] export urls {i+len(chunk)}/{len(id_list)}")
        time.sleep(1)

    exported = 0
    products, concepts = set(), set()
    pairs_out = []
    for fr, tg in uniq:
        prod_slug = H.slug(tg["product"] or "misc")
        d = os.path.join(REFS, prod_slug)
        os.makedirs(d, exist_ok=True)
        fid = fr["id"].replace(":", "-")
        img_rel = f"REFS/{prod_slug}/{fid}.png"
        u = url_map.get(fr["id"])
        if u and H.download(u, os.path.join(d, f"{fid}.png")):
            exported += 1
        products.add(tg["product"]); concepts.add(tg["concept"])
        copy = H.text_samples(fr, [])
        pairs_out.append(
            f"- **{tg['product'] or '?'}** (C{tg['concept']} V{tg['version']} · "
            f"{tg['style'] or '?'} · {tg['aspect'] or '?'}) [{label}]\n"
            f"  - image: `{img_rel}`\n"
            f"  - copy: {' | '.join(copy[:4]) if copy else '(none read)'}\n"
            f"  - name: `{tg['raw']}`\n"
        )

    with open(PAIRS, "a") as f:
        f.write(f"\n\n## Harvest: {label} ({len(pairs_out)} pairs)\n\n")
        f.write("".join(pairs_out))

    return {
        "label": label, "key": key,
        "finished": len(finished), "unique": len(uniq),
        "exported": exported,
        "products": sorted(p for p in products if p),
        "concepts": sorted(c for c in concepts if c),
    }


def main():
    open(LOG, "a").close()
    log("=== harvest_all start ===")

    # 1) discovery (resumable cache)
    disco = {}
    if os.path.exists(DISCO):
        disco = json.load(open(DISCO))
    for label, key in FILES:
        if key in disco:
            log(f"discover [{label}] cached ({len(disco[key]['section_ids'])} sections)")
            continue
        log(f"discover [{label}] {key} ...")
        name, pages, ids = discover(key)
        disco[key] = {"label": label, "name": name, "pages": pages, "section_ids": ids}
        json.dump(disco, open(DISCO, "w"), indent=2)
        log(f"discover [{label}] '{name}': {sum(p['n_children'] for p in pages)} top nodes across {len(pages)} pages")
        time.sleep(2)

    # 2) harvest each
    results = []
    for label, key in FILES:
        done_marker = os.path.join(KNOW, f".harvest-done-{label}")
        if os.path.exists(done_marker):
            log(f"harvest [{label}] already DONE, skipping")
            results.append(json.load(open(done_marker)))
            continue
        ids = disco[key]["section_ids"]
        if not ids:
            log(f"harvest [{label}] NO sections, skipping")
            continue
        log(f"harvest [{label}] {len(ids)} sections ...")
        res = harvest_file(label, key, ids)
        json.dump(res, open(done_marker, "w"), indent=2)
        results.append(res)

    # 3) summary
    lines = ["# HARVEST RESULT\n", f"_generated {time.strftime('%Y-%m-%d %H:%M')}_\n\n",
             "| file | name | finished | unique | exported | products | concepts |\n",
             "|------|------|----------|--------|----------|----------|----------|\n"]
    tot_u = tot_e = 0
    for r in results:
        nm = disco.get(r["key"], {}).get("name", "?")
        lines.append(f"| {r['label']} | {nm} | {r['finished']} | {r['unique']} | "
                     f"{r['exported']} | {len(r['products'])} | {len(r['concepts'])} |\n")
        tot_u += r["unique"]; tot_e += r["exported"]
    lines.append(f"\n**TOTAL unique:** {tot_u} · **exported PNGs:** {tot_e}\n")
    with open(SUMMARY, "w") as f:
        f.write("".join(lines))
    log(f"=== DONE total_unique={tot_u} exported={tot_e} -> {SUMMARY} ===")


if __name__ == "__main__":
    main()
