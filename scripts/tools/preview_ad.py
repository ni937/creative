#!/usr/bin/env python3
"""Local finished-ad PREVIEW renderer — a PIL replica of figma_ad.ad_placed().

The real board push (figma_ad.py -> assemble.js) needs the interactive Figma MCP (use_figma +
upload_assets). When that MCP is absent, this renders the SAME composition locally so the round is
reviewable now: scene (FILL 1080x1350) + localized blurred scrim + RS monogram + eyebrow (caps) +
2-line serif H1 + script CTA, dropped into the exact scene_place.place() region the board would use.

    python scripts/preview_ad.py --ads 03_ITERATIONS/_switch_ad_set.json --out 03_ITERATIONS/_preview

Fonts fall back to Windows system faces (Georgia / Gabriola / Candara) since the board's Amarna/
Optima/Allura aren't installed locally — so this is a faithful LAYOUT preview, not a font-exact proof.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import scene_place  # noqa: E402

FW, FH = 1080, 1350
COL = (250, 247, 240)
LOGO = ROOT / "assets" / "brand" / "rs-monogram.png"
WF = Path("C:/Windows/Fonts")


def _font(names, size):
    for n in names:
        p = WF / n
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def SER(sz):  # serif H1
    return _font(["georgiab.ttf", "timesbd.ttf", "constanb.ttf"], sz)


def SCR(sz):  # script CTA
    return _font(["gabriola.ttf", "segoesc.ttf", "BRUSHSCI.TTF"], sz)


def EYE(sz):  # eyebrow (humanist sans, Optima-ish)
    return _font(["candara.ttf", "segoeui.ttf", "calibri.ttf"], sz)


def _fill_cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def _text_h(draw, s, font):
    # multiline height via bbox
    b = draw.multiline_textbbox((0, 0), s, font=font, spacing=max(2, font.size // 8))
    return b[3] - b[1]


def render_one(ad, out_path):
    scene = Image.open(ROOT / ad["scene_path"]).convert("RGB")
    fr = _fill_cover(scene, FW, FH)
    p = scene_place.place(ad["scene_path"])
    bx, by = round(p["nx"] * FW), round(p["ny"] * FH)
    bw, bh = round(p["nw"] * FW), round(p["nh"] * FH)
    align, scrim = p["align"], float(p["scrim"])
    right, center = align == "right", align == "center"

    # localized blurred scrim behind the copy region
    if scrim > 0.04:
        a = min(0.5, scrim + 0.04)
        ov = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        pd = round(bw * 0.55)
        od.rounded_rectangle([bx - pd // 2, by - pd // 2, bx + bw + pd // 2, by + bh + pd // 2],
                             radius=pd // 2, fill=(0, 0, 0, int(a * 255)))
        ov = ov.filter(ImageFilter.GaussianBlur(60))
        fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")

    d = ImageDraw.Draw(fr)
    eyebrow = ad.get("eyebrow", "").upper()
    h1 = ad.get("h1", "")
    cta = ad.get("cta", "")

    # mirror ad_placed's fit loop: shrink H1 until the whole stack fits bh
    h1size = max(52, min(120, round(bw * 0.19)))
    for _ in range(6):
        LH = round(h1size * 0.7); LW = round(LH * 0.89)
        ebf, hf, cf = EYE(round(h1size * 0.30)), SER(h1size), SCR(round(h1size * 0.78))
        eh, hh, ch = _text_h(d, eyebrow, ebf), _text_h(d, h1, hf), _text_h(d, cta, cf)
        total = LH + 14 + eh + 14 + hh + 18 + ch
        if total <= bh - 12 or h1size <= 44:
            break
        h1size = max(44, int(h1size * (bh - 12) / total))

    y = by + max(6, (bh - total) // 2)

    # logo (monogram, FIT into LWxLH)
    if LOGO.exists():
        lg = Image.open(LOGO).convert("RGBA")
        s = min(LW / lg.width, LH / lg.height)
        lg = lg.resize((max(1, round(lg.width * s)), max(1, round(lg.height * s))), Image.LANCZOS)
        lx = (bx + bw - lg.width) if right else (bx + (bw - lg.width) // 2 if center else bx)
        fr.paste(lg, (lx, y), lg)
    y += LH + 14

    def put(s, font, yy):
        anchor = "ra" if right else ("ma" if center else "la")
        xx = (bx + bw) if right else (bx + bw // 2 if center else bx)
        d.multiline_text((xx, yy), s, font=font, fill=COL, anchor=anchor,
                         spacing=max(2, font.size // 8),
                         align="right" if right else ("center" if center else "left"))

    put(eyebrow, ebf, y); y += eh + 14
    put(h1, hf, y); y += hh + 18
    put(cta, cf, y)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fr.save(out_path)
    return fr


def montage(imgs, cols=3, tw=360, pad=16):
    cells = [(n, im.resize((tw, round(im.height * tw / im.width)))) for n, im in imgs]
    ch = max(c.height for _, c in cells)
    rows = (len(cells) + cols - 1) // cols
    W, H = cols * tw + (cols + 1) * pad, rows * (ch + 26) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    dr = ImageDraw.Draw(sheet)
    f = EYE(16)
    for i, (n, c) in enumerate(cells):
        r, col = divmod(i, cols)
        x, yy = pad + col * (tw + pad), pad + r * (ch + 26 + pad)
        dr.text((x, yy), n, fill=(225, 225, 225), font=f)
        sheet.paste(c, (x, yy + 20))
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ads", required=True)
    ap.add_argument("--out", default="03_ITERATIONS/_preview")
    a = ap.parse_args()
    ads = json.load(open(ROOT / a.ads, encoding="utf-8")) if not Path(a.ads).is_absolute() else json.load(open(a.ads, encoding="utf-8"))
    outdir = ROOT / a.out
    imgs = []
    for ad in ads:
        name = ad.get("room", ad.get("scene_path"))
        fr = render_one(ad, outdir / f"{name}.png")
        imgs.append((name, fr))
        print(f"[preview] {name}", flush=True)
    sheet = montage(imgs)
    sheet.save(outdir / "_contact_sheet.png")
    print(f"=== preview sheet -> {outdir / '_contact_sheet.png'} ===", flush=True)


if __name__ == "__main__":
    main()
