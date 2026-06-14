#!/usr/bin/env python3
"""Hero-perfect 'real pixels' composite (ATTENDED).

The zero-generative-drift escalation for high-AOV flush/wall heroes: paste the REAL product
packshot onto an empty AI background (from `generate.py --mode background`) so the PRODUCT pixel
is never AI-generated — only the scene is. Use this when --insert's mild mounting/perspective drift
is unacceptable.

Cutout strategy (the hard part): RS packshots sit on warm textured grounds (0/12 have a real alpha
channel), so naive chroma-key can't isolate them. The default `--cutout-mode gemini` asks Gemini to
re-render the product on pure white, then we key white->alpha + feather. `--cutout-mode chroma` is a
direct near-white key for packshots that are already clean.

  # 1) make an empty on-brand background
  python scripts/generate.py --mode background --prompt "<empty scene>, no product" --aspect 4:5
  # 2) paste the real packshot into it with a contact shadow
  python scripts/composite_packshot.py --packshot assets/products/brass-dimmer-switch.png \
      --background 03_ITERATIONS/<bg-run>/image_01.png --x 0.72 --y 0.42 --scale 0.16

Output: ROOT/03_ITERATIONS/<run-id>-composite/ with the PNG + a sidecar .json provenance file.
Visually Read the output (project rule) before trusting it.
"""
from __future__ import annotations
import argparse
import base64
import json
import sys
from pathlib import Path

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
# Hard-depends on generate.py's refactor: _gemini_once + config loaders + run-id/ROOT helpers.
from generate import _gemini_once, load_config, resolve_key, _now_id, ROOT  # noqa: E402

CUTOUT_INSTRUCTION = (
    "Cut out the product only; output ONLY the product on a pure solid-white background; "
    "preserve the product exactly (shape, finish, color, logos, details); remove any contact shadow."
)


def _strip_exif(im: Image.Image) -> Image.Image:
    """Rebuild the image with no EXIF/ICC so nothing carries over into the composite."""
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))
    return clean


def _gemini_cutout(packshot: Path, cfg: dict) -> Image.Image:
    """Re-render the product on pure white via Gemini, return an RGBA Image (still white bg)."""
    mime = "image/png"
    data = base64.b64encode(packshot.read_bytes()).decode("ascii")
    gem_cfg = cfg["models"]["nano-banana-pro"]
    key = resolve_key("nano-banana-pro", cfg)
    raw = _gemini_once(
        [{"inlineData": {"mimeType": mime, "data": data}}, {"text": CUTOUT_INSTRUCTION}],
        gem_cfg, key, aspect="1:1", size="2K",
    )
    import io
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def _white_to_alpha(im: Image.Image, feather: int = 3) -> Image.Image:
    """Key near-white + low-saturation pixels to transparent, then feather the alpha edge."""
    rgba = np.asarray(im.convert("RGBA"), dtype=np.float32)
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn)  # 0..255 absolute saturation spread
    near_white = (mx > 238) & (sat < 18)
    alpha = np.where(near_white, 0.0, 255.0).astype(np.float32)
    # Feather: blur the binary alpha so the cutout edge is soft (hides keying jaggies/halo).
    if feather > 0:
        k = feather * 2 + 1
        alpha = cv2.GaussianBlur(alpha, (k, k), 0)
    out = rgba.copy()
    out[..., 3] = alpha
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def _autocrop_alpha(im: Image.Image, pad: int = 2) -> Image.Image:
    """Crop to the product's alpha bbox so --scale/--x/--y refer to the product, not whitespace."""
    a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 8)
    if xs.size == 0:
        return im
    x0, x1 = max(0, xs.min() - pad), min(im.width, xs.max() + 1 + pad)
    y0, y1 = max(0, ys.min() - pad), min(im.height, ys.max() + 1 + pad)
    return im.crop((x0, y0, x1, y1))


def _shadow(cutout: Image.Image, opacity: float, blur: int, dx: int, dy: int) -> Image.Image:
    """Build a soft black drop-shadow from the cutout's alpha silhouette, offset by (dx,dy)."""
    a = np.asarray(cutout)[..., 3].astype(np.float32)
    sh = np.zeros((cutout.height, cutout.width, 4), dtype=np.float32)
    sh[..., 3] = a * float(opacity)            # black silhouette at the requested opacity
    if blur > 0:
        k = blur * 2 + 1
        sh[..., 3] = cv2.GaussianBlur(sh[..., 3], (k, k), 0)
    shadow_im = Image.fromarray(sh.astype(np.uint8), "RGBA")
    return shadow_im


def composite(packshot: Path, background: Path, out: Path, x: float, y: float, scale: float,
              shadow_opacity: float, shadow_blur: int, shadow_dx: int, shadow_dy: int,
              cutout_mode: str, strip_exif: bool, cfg: dict) -> dict:
    bg = Image.open(background).convert("RGBA")
    if strip_exif:
        bg = _strip_exif(bg)
    FW, FH = bg.size

    # 1) CUTOUT — product on transparent.
    if cutout_mode == "gemini":
        cut = _gemini_cutout(packshot, cfg)
    else:
        cut = Image.open(packshot).convert("RGBA")
    cut = _white_to_alpha(cut)
    cut = _autocrop_alpha(cut)

    # 2) RESIZE cutout to scale*FW preserving aspect.
    target_w = max(1, int(scale * FW))
    target_h = max(1, int(round(target_w * cut.height / cut.width)))
    cut = cut.resize((target_w, target_h), Image.LANCZOS)

    px, py = int(x * FW), int(y * FH)

    # 3) SHADOW under the product, offset.
    canvas = bg.copy()
    sh = _shadow(cut, shadow_opacity, shadow_blur, shadow_dx, shadow_dy)
    canvas.alpha_composite(sh, (px + shadow_dx, py + shadow_dy))
    # 4) COMPOSITE the product on top.
    canvas.alpha_composite(cut, (px, py))

    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out, "PNG")
    meta = {
        "packshot": str(packshot),
        "background": str(background),
        "out": str(out),
        "placement": {"x": x, "y": y, "scale": scale,
                      "shadow": {"opacity": shadow_opacity, "blur": shadow_blur,
                                 "dx": shadow_dx, "dy": shadow_dy}},
        "cutout_mode": cutout_mode,
        "frame": [FW, FH],
    }
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def _run_dir() -> Path:
    """ROOT/03_ITERATIONS/<ts>-composite[-NN] — suffix avoids the 1s-granularity collision when a
    composite writes while the loop is also stamping run dirs in the same second."""
    base = ROOT / "03_ITERATIONS"
    rid = _now_id() + "-composite"
    d = base / rid
    n = 1
    while d.exists():
        d = base / f"{rid}-{n:02d}"
        n += 1
    return d


def main():
    ap = argparse.ArgumentParser(description="composite a real packshot onto an empty AI background")
    ap.add_argument("--packshot", required=True, help="real product photo (the pixels that stay real)")
    ap.add_argument("--background", required=True, help="empty scene from generate.py --mode background")
    ap.add_argument("--out", default=None, help="output PNG path (default: a new run dir)")
    ap.add_argument("--x", type=float, default=0.72, help="normalized top-left x (0..1)")
    ap.add_argument("--y", type=float, default=0.42, help="normalized top-left y (0..1)")
    ap.add_argument("--scale", type=float, default=0.16, help="cutout width as a fraction of frame width")
    ap.add_argument("--shadow-opacity", type=float, default=0.22)
    ap.add_argument("--shadow-blur", type=int, default=18)
    ap.add_argument("--shadow-dx", type=int, default=6)
    ap.add_argument("--shadow-dy", type=int, default=10)
    ap.add_argument("--cutout-mode", choices=["gemini", "chroma"], default="gemini")
    ap.add_argument("--no-strip-exif", action="store_true", help="keep EXIF/ICC (default strips them)")
    a = ap.parse_args()

    cfg = load_config()
    out = Path(a.out) if a.out else (_run_dir() / "image_01.png")
    meta = composite(
        Path(a.packshot), Path(a.background), out,
        a.x, a.y, a.scale, a.shadow_opacity, a.shadow_blur, a.shadow_dx, a.shadow_dy,
        a.cutout_mode, not a.no_strip_exif, cfg,
    )
    print(json.dumps({"out": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),
                      "cutout_mode": meta["cutout_mode"], "frame": meta["frame"]}, indent=2))


if __name__ == "__main__":
    main()
