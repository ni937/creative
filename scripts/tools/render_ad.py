#!/usr/bin/env python3
"""Local ad RENDERER — composite a finished 4:5 ad PREVIEW (scene + logo + copy + CTA) from a layout SPEC.

Candidate generator for the LAYOUT tournament (layout_loop.py): holds the SCENE + COPY fixed and varies
LAYOUT (typography, logo variant + placement, CTA style + placement, copy anchor, scrim, rule motif) so the
pairwise critic judges layout, not scene aesthetics. Mirrors the live Figma assembler (figma_ad.ad_placed):
same roles (eyebrow caps / serif H1 / script accent), same image-aware placement (scene_place), same
fit-to-box shrink so copy never overflows onto the product — but every knob is a parameter, rendered locally
with Google-font fallbacks (Cormorant/EB Garamond serif, Raleway eyebrow, Allura script). The WINNING spec
is then applied in figma_ad for the crisp Optima/Allura board render on a Mac; fonts here preview STRUCTURE.

  python scripts/render_ad.py <scene.png> --spec spec.json --out preview.png
  python scripts/render_ad.py --demo <scene.png>     # one of each archetype -> 03_ITERATIONS/_layout/
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene_place  # noqa: E402

FW, FH = 1080, 1350
FONTS = ROOT / "assets" / "fonts"
LIGHT = (250, 247, 240)
DARK = (26, 23, 20)
GAP = int(0.016 * FH)
MAX_BRASS = 0.15            # same cap as scene_place.acceptance

FONT_FILES = {
    "cormorant": ("Cormorant.ttf", "SemiBold"),
    "ebgaramond": ("EBGaramond.ttf", "SemiBold"),
    "raleway": ("Raleway-Medium.ttf", "Medium"),
    "marcellus": ("Marcellus-Regular.ttf", None),
    "allura": ("Allura-Regular.ttf", None),
}
LOGOS = {
    "monogram": ROOT / "assets" / "brand" / "rs-monogram.png",
    "wordmark": ROOT / "assets" / "brand" / "rs-wordmark.png",
    "wordmark-dark": ROOT / "assets" / "brand" / "rs-wordmark-dark.png",
}
_FONT_CACHE: dict = {}


def font(role, px):
    fn, inst = FONT_FILES.get(role, FONT_FILES["cormorant"])
    key = (fn, inst, px)
    if key not in _FONT_CACHE:
        f = ImageFont.truetype(str(FONTS / fn), px)
        if inst:
            try:
                f.set_variation_by_name(inst)
            except Exception:
                pass
        _FONT_CACHE[key] = f
    return _FONT_CACHE[key]


def _text_w(d, s, f, track_px=0):
    if not s:
        return 0
    return int(sum(d.textlength(ch, font=f) for ch in s) + track_px * max(0, len(s) - 1))


def _draw_tracked(d, xy, s, f, fill, track_px, anchor_l):
    w = _text_w(d, s, f, track_px)
    x, y = xy
    if anchor_l == "ma":
        x -= w / 2
    elif anchor_l == "ra":
        x -= w
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track_px


def _wrap(d, s, f, maxw):
    lines = []
    for chunk in s.replace("\n", "|").split("|"):
        words = chunk.split()
        if not words:
            continue
        cur = words[0]
        for w in words[1:]:
            if d.textlength(cur + " " + w, font=f) <= maxw:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines or [""]


def _crop_45(im):
    w, h = im.size
    if abs(w / h - FW / FH) < 0.01:
        return im.resize((FW, FH), Image.LANCZOS)
    target = FW / FH
    if w / h > target:
        nw = int(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize((FW, FH), Image.LANCZOS)


def _scrim(base, box, mode, strength):
    if mode == "none" or strength <= 0:
        return base
    bx, by, bw, bh = box
    pad = int(bw * 0.45)
    a = int(min(0.55, strength) * 255)
    if mode == "radial":
        yy, xx = np.mgrid[0:FH, 0:FW]
        cx, cy = bx + bw / 2, by + bh / 2
        rx, ry = bw / 2 + pad, bh / 2 + pad
        r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        ov = Image.fromarray((np.clip(1 - r, 0, 1) ** 1.3 * a).astype("uint8"), "L")
    else:
        ov = Image.new("L", (FW, FH), 0)
        ImageDraw.Draw(ov).rounded_rectangle([bx - pad, by - pad, bx + bw + pad, by + bh + pad],
                                             radius=pad, fill=a)
        ov = ov.filter(ImageFilter.GaussianBlur(pad * 0.8))
    return Image.composite(Image.new("RGB", (FW, FH), (0, 0, 0)), base, ov)


def _draw_line(d, s, f, xy, fill, anchor_l):
    d.text(xy, s, font=f, fill=fill, anchor=anchor_l)


def _paste_logo_at(canvas, logo, ax, y, align):
    v = logo.get("variant", "none")
    if v == "none" or v not in LOGOS:
        return
    lg = Image.open(LOGOS[v]).convert("RGBA")
    h = int(logo.get("scale", 0.06) * FH)
    w = int(h * lg.width / lg.height)
    lg = lg.resize((w, h), Image.LANCZOS)
    x = ax if align == "left" else (ax - w if align == "right" else ax - w // 2)
    canvas.paste(lg, (int(x), int(y)), lg)


def _paste_logo_corner(canvas, logo):
    v = logo.get("variant", "none")
    if v == "none" or v not in LOGOS or logo.get("pos") == "with-copy":
        return
    lg = Image.open(LOGOS[v]).convert("RGBA")
    h = int(logo.get("scale", 0.06) * FH)
    w = int(h * lg.width / lg.height)
    lg = lg.resize((w, h), Image.LANCZOS)
    m = int(0.06 * FH)
    pos = logo.get("pos", "top-left")
    x = m if "left" in pos else (FW - w - m if "right" in pos else (FW - w) // 2)
    y = m if "top" in pos else (FH - h - m)
    canvas.paste(lg, (int(x), int(y)), lg)


def _draw_cta(d, c, f, ax, y, align, col):
    text, style = c["text"], c.get("style", "text")
    tw = d.textlength(text, font=f)
    al = {"left": "la", "center": "ma", "right": "ra"}[align]
    if style == "pill":
        padx, pady = int(f.size * 0.9), int(f.size * 0.5)
        pw, ph = tw + 2 * padx, f.size + 2 * pady
        x0 = ax if align == "left" else (ax - pw if align == "right" else ax - pw // 2)
        d.rounded_rectangle([x0, y, x0 + pw, y + ph], radius=ph // 2, outline=col, width=3)
        d.text((x0 + pw / 2, y + ph / 2), text, font=f, fill=col, anchor="mm")
    elif style == "underline":
        tx = ax if align == "left" else (ax - tw if align == "right" else ax - tw / 2)
        d.text((ax, y), text, font=f, fill=col, anchor=al)
        d.line([(tx, y + f.size * 1.18), (tx + tw, y + f.size * 1.18)], fill=col, width=2)
    else:
        d.text((ax, y), text, font=f, fill=col, anchor=al)


def render(scene_path, spec, out_path, finish=None):
    import layout_spec
    base = _crop_45(Image.open(scene_path).convert("RGB"))
    R = layout_spec.resolve_layout(scene_path, spec, finish=finish)          # shared geometry+color+logo-tone
    nx, ny, nw, nh = R["box"]
    bx, by, bw, bh = round(nx * FW), round(ny * FH), round(nw * FW), round(nh * FH)
    align, relocated = R["align"], R["relocated"]
    anchor = spec.get("anchor", "auto")
    col = LIGHT if R["color"] == "light" else DARK

    base = _scrim(base, (bx, by, bw, bh), R["scrim_mode"], R["scrim_strength"] if R["scrim_mode"] != "none" else 0)
    canvas = base.convert("RGB")
    d = ImageDraw.Draw(canvas)
    anchor_l = {"left": "la", "center": "ma", "right": "ra"}[align]
    ax = bx if align == "left" else (bx + bw if align == "right" else bx + bw // 2)

    eb, h1, sub, cta = spec.get("eyebrow", {}), spec.get("h1", {}), spec.get("sub", {}), spec.get("cta", {})
    logo = R["logo"]
    logo_with = logo.get("pos") == "with-copy" and logo.get("variant", "none") != "none"

    def build(scale):
        """parts = list of (kind, payload, height, gap). Also returns total height + max content width."""
        parts, total, maxw = [], 0, 0
        if logo_with:
            lh = int(logo.get("scale", 0.06) * FH * scale)
            parts.append(("logo", None, lh, int(0.018 * FH)))
            total += lh + int(0.018 * FH)
        if eb.get("show", True) and eb.get("text"):
            ef = font(eb.get("font", "raleway"), max(11, int(eb.get("size", 0.022) * FH * scale)))
            tr = int(eb.get("track", 0.16) * ef.size)
            maxw = max(maxw, _text_w(d, eb["text"].upper(), ef, tr))
            parts.append(("eyebrow", (ef, tr), int(ef.size * 1.25), GAP))
            total += int(ef.size * 1.25) + GAP
        if spec.get("rule") == "above-h1":
            parts.append(("rule", None, 2, int(0.018 * FH)))
            total += 2 + int(0.018 * FH)
        hpx = max(22, int(h1.get("size", 0.06) * FH * scale))
        hf = font(h1.get("font", "cormorant"), hpx)
        ht = h1.get("text", "")
        if h1.get("upper"):
            ht = ht.upper()
        lines = _wrap(d, ht, hf, bw)
        lead = int(hpx * h1.get("leading", 1.06))
        maxw = max([maxw] + [d.textlength(ln, font=hf) for ln in lines])
        parts.append(("h1", (hf, lines, lead), lead * len(lines), int(0.02 * FH)))
        total += lead * len(lines) + int(0.02 * FH)
        if sub.get("text") and sub.get("font", "none") != "none":
            role = "allura" if sub.get("font") == "allura" else h1.get("font", "cormorant")
            sf = font(role, max(14, int(sub.get("size", 0.044) * FH * scale)))
            sl = _wrap(d, sub["text"], sf, bw)
            maxw = max([maxw] + [d.textlength(ln, font=sf) for ln in sl])
            sh = int(sf.size * 1.18) * len(sl)
            parts.append(("sub", (sf, sl), sh, GAP))
            total += sh + GAP
        if cta.get("style", "none") != "none" and cta.get("text"):
            cf = font(cta.get("font", "raleway"), max(12, int(cta.get("size", 0.02) * FH * scale)))
            cw = d.textlength(cta["text"], font=cf) + (int(cf.size * 1.8) if cta["style"] == "pill" else 0)
            maxw = max(maxw, cw)
            ch = int(cf.size * 1.2) + (int(cf.size) if cta["style"] == "pill" else 0)
            parts.append(("cta", (cf, cta), ch, 0))
            total += ch
        return parts, total, maxw

    parts, total, maxw = build(1.0)
    avail_h = bh - int(0.03 * FH)
    scale = 1.0
    if total > avail_h or maxw > bw:
        scale = max(0.5, min(avail_h / max(1, total), bw / max(1, maxw)))
        parts, total, maxw = build(scale)

    y = by + max(int(0.01 * FH), (bh - total) // 2)
    for kind, payload, h, gap in parts:
        if kind == "logo":
            _paste_logo_at(canvas, logo, ax, y, align)
        elif kind == "eyebrow":
            ef, tr = payload
            _draw_tracked(d, (ax, y), eb["text"].upper(), ef, col, tr, anchor_l)
        elif kind == "rule":
            rw = int(bw * 0.34)
            rx = ax if align == "left" else (ax - rw if align == "right" else ax - rw // 2)
            d.line([(rx, y), (rx + rw, y)], fill=col, width=2)
        elif kind == "h1":
            hf, lines, lead = payload
            for ln in lines:
                _draw_line(d, ln, hf, (ax, y), col, anchor_l)
                y += lead
            y -= lead
        elif kind == "sub":
            sf, lines = payload
            for ln in lines:
                _draw_line(d, ln, sf, (ax, y), col, anchor_l)
                y += int(sf.size * 1.18)
            y -= int(sf.size * 1.18)
        elif kind == "cta":
            cf, c = payload
            _draw_cta(d, c, cf, ax, y, align, col)
        y += h + gap

    if not logo_with:
        _paste_logo_corner(canvas, logo)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)
    frac = scene_place.box_product_fraction(scene_path, (bx / FW, by / FH, bw / FW, bh / FH), finish=finish)
    return {"out": str(out_path), "archetype": spec.get("name"), "anchor": anchor, "align": align,
            "relocated": relocated, "scale": round(scale, 2), "color": "light" if col == LIGHT else "dark",
            "block": [round(bx / FW, 3), round(by / FH, 3), round(bw / FW, 3), round(bh / FH, 3)],
            "product_frac": frac, "acc_ok": frac <= MAX_BRASS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("--spec")
    ap.add_argument("--out", default="03_ITERATIONS/_layout/preview.png")
    ap.add_argument("--finish", default=None)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        import layout_spec
        copy = {"eyebrow": "The Brass Switch", "h1": "Form Meets|Everyday Function", "cta": "Choose Your Finish"}
        for k, name in enumerate(layout_spec.ARCH_NAMES):
            s = layout_spec.make_spec(name, copy, k)
            r = render(a.scene, s, f"03_ITERATIONS/_layout/demo_{name}.png", a.finish)
            print(f'{name:24} acc={r["acc_ok"]} scale={r["scale"]} {r["block"]} {"reloc" if r["relocated"] else ""}')
        return
    spec = json.load(open(a.spec, encoding="utf-8")) if a.spec else {}
    print(json.dumps(render(a.scene, spec, a.out, a.finish), indent=1))


if __name__ == "__main__":
    main()
