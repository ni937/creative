#!/usr/bin/env python3
"""Image-AWARE ad copy placement — picks the region to put copy by a POSITIVE objective (where copy SHOULD
go), derived from the actual scene, then the caller sizes the text to fill it.

DON'T (avoid) + DO (prefer), combined into one score per candidate region:
  AVOID  — product (brass hue, HARD reject), detail/edges, glowing highlights, saturated color.
  PREFER — large area (the "great free space"), emptiness, uniform/clean tone, NOT bottom-heavy, and the
           side OPPOSITE the product (the blurred space next to the close-up).
score = emptiness^1.4 · area^0.65 · contrast · vbias · comp   (maximize; hard-reject boxes over product)
Box sizes span a wide range so the winning box adapts to the scene's actual empty region. Output is
normalized 0..1 (resolution-independent) + a `text_scale` hint (region is big -> big type).

  python scripts/scene_place.py [--debug] img1 img2 ...
"""
from __future__ import annotations
import argparse, json, math, os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

SW, SH = 200, 250
MARGIN = 0.045
BRASS_MAX = 0.012
# (w,h) fractions — fits the scene's real empty region. Min raised (no sub-0.42w boxes) so the copy block is
# always BIG/confident, never a timid patch ("decent -> great"); scrim + bbox-exclusion keep it clean/off-product.
BOXES = [(0.52, 0.40), (0.60, 0.46), (0.66, 0.40), (0.42, 0.50),
         (0.50, 0.58), (0.58, 0.34), (0.46, 0.62)]


# Product hue band to keep copy OFF (the on-image product). Default = brass/gold. For a non-brass SKU,
# pass its band, or (None, None) to disable the hue mask and rely on edges + highlights only.
PRODUCT_HUE = (0.06, 0.17)

# Local-sharpness gate for the brass-hue mask. The REAL product (sharp dimmer) sits in a high-edge-density
# neighborhood; bokeh brass (out-of-focus pendant, warm wall glow, blurred credenza hardware) is soft =
# low local edge density. In brass-SATURATED scenes the raw hue mask flagged ~28% of the frame as
# "product" (the whole warm-toned blurred half), so the copy box had nowhere clean to land. We require a
# brass pixel to ALSO be in a sharp neighborhood. Threshold is relative to the frame's own edge mean
# (SHARP_K = blur window for the local-edge mean; SHARP_FACTOR = multiple of edges.mean() a pixel must
# clear). Tuned on the dimmer batch so the sharp plate survives but blurred brass is excluded.
SHARP_K = 15
SHARP_FACTOR = 0.85

# Finish -> hue band. Pale/dark finishes ((None,None)) disable the HSV mask and fall back to
# edge-density (see place(finish=...)). Brass/gold/bronze keep the warm band; '' (blank finish in the
# catalog) defaults to the brass band — matches today's brass-first behavior for unlabeled SKUs.
FINISH_HUE = {
    "brass": (0.06, 0.17), "gold": (0.06, 0.17), "bronze": (0.05, 0.12),
    "nickel": (None, None), "chrome": (None, None), "black": (None, None),
    "alabaster": (None, None), "": (0.06, 0.17),
}


def _maps(im, product_hue=PRODUCT_HUE):
    sm = im.resize((SW, SH))
    g = np.asarray(sm.convert("L"), float) / 255.0
    gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1]))
    gy = np.abs(np.diff(g, axis=0, prepend=g[:1, :]))
    edges = np.clip((gx + gy) * 3.5, 0, 1)
    hsv = np.asarray(sm.convert("HSV"), float) / 255.0
    Hh, Ss, Vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    lo, hi = product_hue
    if lo is None:
        product = np.zeros_like(g)                  # pale/dark finish: no hue mask (fallback path intact)
    else:
        brass = (Hh > lo) & (Hh < hi) & (Ss > 0.30) & (Vv > 0.45)
        # local-sharpness gate: real product = brass AND in a sharp neighborhood; bokeh brass = blurred,
        # low local edge density -> excluded. cv2.blur is a fast box filter = local mean of edge magnitude.
        sharp = cv2.blur(edges.astype(np.float32), (SHARP_K, SHARP_K))
        sharp_thr = float(edges.mean()) * SHARP_FACTOR
        product = (brass & (sharp >= sharp_thr)).astype(float)
    highlight = (Vv > 0.86).astype(float)
    avoid = edges * 1.0 + product * 2.0 + Ss * 0.40 + highlight * 0.8
    return avoid, g, product, edges


def _integral(a):
    return np.pad(a, ((1, 0), (1, 0))).cumsum(0).cumsum(1)


def _rm(I, x, y, w, h):
    return (I[y + h, x + w] - I[y, x + w] - I[y + h, x] + I[y, x]) / (w * h)


def place(path, product_hue=PRODUCT_HUE, finish=None):
    # Finish-aware: for a pale/dark SKU (alabaster sconce, glass pendant, black-backplate) the brass
    # HSV mask is empty -> pcx=None -> no opposite-side bias and no product-bbox exclusion -> copy can
    # land ON the fixture. Resolve the hue band from the catalog `finish` so non-brass heroes get a
    # usable product region. Only overrides when the caller left product_hue at its default.
    if finish is not None and product_hue == PRODUCT_HUE:
        product_hue = FINISH_HUE.get(finish, PRODUCT_HUE)
    im = Image.open(path).convert("RGB")
    avoid, g, product, edges = _maps(im, product_hue)
    Iav, Il, Il2, Ibr = _integral(avoid), _integral(g), _integral(g * g), _integral(product)
    m = int(MARGIN * SW)
    avn = max(0.25, float(avoid.mean()) * 2.2)        # emptiness normalizer
    ys, xs = np.where(product > 0.5)
    pcx = (xs.mean() / SW) if xs.size > 25 else None    # product centroid x (for "opposite side")
    # Pale/dark fallback: no hue mask -> derive a product side from the highest-edge-density column
    # band, so the comp side-bias term still has a side to oppose (soft bias only; bbox stays off).
    if pcx is None:
        colsum = edges.sum(axis=0)                      # edge density per image column
        if float(colsum.max()) > 0:
            pcx = float(int(np.argmax(colsum))) / SW
    # product bounding box (+pad). The copy box must clear it ENTIRELY — a box can pass the brass-average
    # test yet still clip the plate ("copy obscures product"). -1 sentinels => no product => no exclusion.
    if xs.size > 25:
        pad = int(0.09 * SW)            # product-bbox clearance (widened per batch-4 'copy box on product' signal)
        px0, px1, py0, py1 = xs.min() - pad, xs.max() + pad, ys.min() - pad, ys.max() + pad
    else:
        px0 = px1 = py0 = py1 = -1
    best = best_any = None
    for bwf, bhf in BOXES:
        bw, bh = int(bwf * SW), int(bhf * SH)
        areaP = ((bw * bh) / (SW * SH)) ** 0.65              # area weight (sub-linear; don't over-favor huge boxes)
        for y in range(m, SH - bh - m + 1, 4):
            for x in range(m, SW - bw - m + 1, 4):
                av = _rm(Iav, x, y, bw, bh)
                emp = max(0.0, 1.0 - av / avn)
                lum = _rm(Il, x, y, bw, bh)
                var = max(0.0, _rm(Il2, x, y, bw, bh) - lum * lum)
                contrast = 1.0 / (1.0 + 2.5 * math.sqrt(var))
                cx, cy = (x + bw / 2) / SW, (y + bh / 2) / SH
                vbias = 1.0 - 0.5 * max(0.0, cy - 0.62)     # discourage bottom-heavy
                comp = 1.0
                if pcx is not None:
                    if (cx - 0.5) * (pcx - 0.5) > 0:        # copy on the SAME side as the product -> discourage
                        comp *= 0.78
                    comp *= 1.0 - 0.30 * abs(cx - 0.5)      # prefer horizontally-centered copy (board feedback)
                pf = _rm(Ibr, x, y, bw, bh)                  # fraction of the box sitting on the product
                prod_pen = 1.0 / (1.0 + 30.0 * pf)           # steep: copy must AVOID the product, even in the fallback path
                score = (emp ** 1.4) * areaP * contrast * vbias * comp * prod_pen
                if best_any is None or score > best_any[0]:
                    best_any = (score, x, y, bw, bh, lum, av)
                # product-clear best: must beat current AND fully clear the product bbox AND be low-brass (lazy)
                clears = (x + bw <= px0) or (x >= px1) or (y + bh <= py0) or (y >= py1)
                if (best is None or score > best[0]) and clears and pf <= BRASS_MAX:
                    best = (score, x, y, bw, bh, lum, av)
    _, x, y, bw, bh, lum, av = best or best_any
    box_brass = round(float(_rm(Ibr, x, y, bw, bh)), 4)  # fraction of the chosen copy box that is product/brass
    clear = box_brass <= BRASS_MAX                         # strict (info); the gate uses a looser bokeh-tolerant cap
    cx = (x + bw / 2) / SW
    align = "left" if cx < 0.40 else ("right" if cx > 0.60 else "center")
    light = lum < 0.55
    scrim = round(min(0.5, max(0.0, (av - 0.08) * 1.6)), 2)
    return {
        "scene": path,
        "nx": round(x / SW, 4), "ny": round(y / SH, 4), "nw": round(bw / SW, 4), "nh": round(bh / SH, 4),
        "align": align, "scrim": scrim, "lum": round(lum, 2), "avoid": round(float(av), 3),
        "clear": clear, "box_brass": box_brass,
        "text_rgb": [0.98, 0.97, 0.94] if light else [0.10, 0.09, 0.08],
    }


# Per-aspect minimum copy-box size. 4:5 is the calibrated baseline (50-cycle dimmer ledger) and is
# byte-identical to the old global (0.40, 0.30). Taller 9:16 lets a shorter band pass; wider 1:1 demands
# a wider/taller band so copy isn't cramped. Explicit min_w/min_h still override.
ACCEPT_MIN = {"4:5": (0.40, 0.30), "9:16": (0.40, 0.22), "1:1": (0.46, 0.34)}


def acceptance(p, aspect="4:5", min_w=None, min_h=None, max_brass=0.15):
    """Pre-publish gate: a frame must pass ALL of these (deterministic) before it reaches human review —
    stops shipping the known failure modes (copy ON the product, timid/tiny copy, broken scrim). max_brass
    tolerates incidental BOKEH brass (sconces/art) but catches copy sitting on the switch. Returns (ok, reasons)."""
    dmw, dmh = ACCEPT_MIN.get(aspect, ACCEPT_MIN["4:5"])
    if min_w is None:
        min_w = dmw
    if min_h is None:
        min_h = dmh
    reasons = []
    bb = p.get("box_brass", 0.0)
    if bb > max_brass:
        reasons.append(f"copy box on product (brass {bb:.2f} > {max_brass})")
    if p["nw"] < min_w:
        reasons.append(f"copy too narrow ({p['nw']:.2f} < {min_w})")
    if p["nh"] < min_h:
        reasons.append(f"copy too short ({p['nh']:.2f} < {min_h})")
    if not (0.0 <= p["scrim"] <= 0.5):
        reasons.append(f"scrim out of range ({p['scrim']})")
    return (not reasons, reasons)


def product_bbox(path, product_hue=PRODUCT_HUE, finish=None):
    """Normalized (x0,y0,x1,y1) of the detected product, or None if none found. Reuses place()'s
    hue+local-sharpness mask so a fixed-anchor layout can be gated against the real product box
    (copy must clear it). Same finish->hue resolution as place()."""
    if finish is not None and product_hue == PRODUCT_HUE:
        product_hue = FINISH_HUE.get(finish, PRODUCT_HUE)
    im = Image.open(path).convert("RGB")
    _, _, product, _ = _maps(im, product_hue)
    ys, xs = np.where(product > 0.5)
    if xs.size <= 25:
        return None
    return (round(float(xs.min()) / SW, 4), round(float(ys.min()) / SH, 4),
            round(float(xs.max()) / SW, 4), round(float(ys.max()) / SH, 4))


def box_product_fraction(path, box, product_hue=PRODUCT_HUE, finish=None):
    """Fraction of a normalized box (x,y,w,h in 0..1) that overlaps the product mask — same primitive as
    place()'s box_brass, exposed for a fixed-anchor layout to gate itself against the product (cap 0.15)."""
    if finish is not None and product_hue == PRODUCT_HUE:
        product_hue = FINISH_HUE.get(finish, PRODUCT_HUE)
    im = Image.open(path).convert("RGB")
    _, _, product, _ = _maps(im, product_hue)
    Ibr = _integral(product)
    x = min(max(0, int(box[0] * SW)), SW - 1)
    y = min(max(0, int(box[1] * SH)), SH - 1)
    w = max(1, min(int(box[2] * SW), SW - x))
    h = max(1, min(int(box[3] * SH), SH - y))
    return round(float(_rm(Ibr, x, y, w, h)), 4)


def debug_overlay(path, p):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    scale = 360 / W
    d = im.resize((int(W * scale), int(H * scale))).convert("RGBA")
    ov = Image.new("RGBA", d.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    dw, dh = d.size
    bx = (p["nx"] * dw, p["ny"] * dh, (p["nx"] + p["nw"]) * dw, (p["ny"] + p["nh"]) * dh)
    dr.rectangle(bx, fill=(0, 200, 255, 70), outline=(0, 220, 255, 255), width=3)
    dr.text((bx[0] + 4, bx[1] + 4), f'{p["align"]} scrim{p["scrim"]}', fill=(255, 255, 255, 255))
    out = Image.alpha_composite(d, ov).convert("RGB")
    name = os.path.basename(os.path.dirname(path)) or os.path.basename(path)
    op = f"03_ITERATIONS/_zoom/place_{name}.png"
    out.save(op)
    return op


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes", nargs="+")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args()
    res = []
    for s in a.scenes:
        p = place(s)
        if a.debug:
            p["_overlay"] = debug_overlay(s, p)
        res.append(p)
    sys.stdout.write(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
