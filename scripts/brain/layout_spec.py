#!/usr/bin/env python3
"""Layout SPEC library — the real RS ad-layout archetypes (extracted from the live Ads_May_26 boards) +
a sampler that jitters knobs to produce diverse candidates for the layout tournament.

The tournament holds the SCENE + COPY fixed (per the scene's manifest entry) and varies LAYOUT. Each
archetype is a template (no text); make_spec() injects the scene's copy and jitters typography / logo
variant+placement / CTA / scrim so the critic sees real layout variety, and bucket() groups candidates
so champions are kept PER archetype family (diversification — pairwise H2H alone would converge to one).

Grounding (what the real boards do — see assets/layout-bar/, 04_KNOWLEDGE/real-layout-system.md):
  - Two families: MODERN (copy top-left/bottom, serif caps, thin rule motif, wordmark) and HERITAGE
    (monogram top-center, serif mixed-case H1 + Allura script sub, copy bottom).
  - Logo VARIES: monogram (top-center/left) or stacked wordmark (bottom-right/top-center). Not one logo.
  - CTA pill ONLY on promo/collection ads; product/story ads run NO button (headline is the hook).
  - Scrim is minimal — text sits on naturally dark scene regions.
"""
from __future__ import annotations
import random

LOGO_VARIANTS = ["monogram", "wordmark", "wordmark-dark"]

# Each archetype is a base spec WITHOUT copy text. make_spec() fills eyebrow/h1/sub/cta text + jitters.
ARCHETYPES = {
    # MUNIRA: copy top-left, big serif caps H1 + small serif sub, wordmark bottom-right, no eyebrow/CTA.
    "modern-topleft": {
        "anchor": "top-left", "align": "left",
        "logo": {"variant": "wordmark", "pos": "bottom-right", "scale": 0.050},
        "eyebrow": {"font": "raleway", "size": 0.020, "track": 0.16, "show": False},
        "h1": {"font": "cormorant", "size": 0.066, "leading": 1.0, "upper": True},
        "sub": {"font": "cormorant", "size": 0.030},
        "cta": {"style": "none"},
        "rule": "none", "scrim": "soft", "color": "auto", "margin": 0.065,
    },
    # HARDWARE: eyebrow (NEW ARRIVAL) + rule + huge serif caps H1, wordmark bottom-right, no CTA.
    "modern-eyebrow": {
        "anchor": "top-left", "align": "left",
        "logo": {"variant": "wordmark", "pos": "bottom-right", "scale": 0.050},
        "eyebrow": {"font": "raleway", "size": 0.020, "track": 0.15, "show": True},
        "h1": {"font": "cormorant", "size": 0.072, "leading": 1.0, "upper": True},
        "sub": {"font": "none"},
        "cta": {"style": "none"},
        "rule": "above-h1", "scrim": "none", "color": "auto", "margin": 0.065,
    },
    # OLAN: monogram top-center, eyebrow caps + serif mixed-case H1, copy bottom-left, no CTA.
    "heritage-bottomleft": {
        "anchor": "bottom-left", "align": "left",
        "logo": {"variant": "monogram", "pos": "top-center", "scale": 0.055},
        "eyebrow": {"font": "raleway", "size": 0.018, "track": 0.18, "show": True},
        "h1": {"font": "cormorant", "size": 0.052, "leading": 1.05, "upper": False},
        "sub": {"font": "none"},
        "cta": {"style": "none"},
        "rule": "none", "scrim": "soft", "color": "auto", "margin": 0.065,
    },
    # WAMBLE: monogram top-center, serif caps H1 + Allura script sub, centered bottom, no CTA.
    "heritage-bottomcenter": {
        "anchor": "bottom-center", "align": "center",
        "logo": {"variant": "monogram", "pos": "top-center", "scale": 0.055},
        "eyebrow": {"font": "raleway", "size": 0.018, "track": 0.18, "show": False},
        "h1": {"font": "cormorant", "size": 0.052, "leading": 1.04, "upper": True},
        "sub": {"font": "allura", "size": 0.046},
        "cta": {"style": "none"},
        "rule": "none", "scrim": "soft", "color": "auto", "margin": 0.07,
    },
    # ALABASTER-style promo: wordmark top-center, serif H1, PILL CTA, centered bottom.
    "promo-pill": {
        "anchor": "bottom-center", "align": "center",
        "logo": {"variant": "wordmark", "pos": "top-center", "scale": 0.048},
        "eyebrow": {"font": "raleway", "size": 0.019, "track": 0.16, "show": False},
        "h1": {"font": "cormorant", "size": 0.050, "leading": 1.04, "upper": False},
        "sub": {"font": "none"},
        "cta": {"style": "pill", "font": "raleway", "size": 0.018},
        "rule": "none", "scrim": "soft", "color": "auto", "margin": 0.07,
    },
    # TRADE: monogram top-left, eyebrow + serif H1 + underline CTA, copy bottom-left.
    "modern-bottomleft-cta": {
        "anchor": "bottom-left", "align": "left",
        "logo": {"variant": "monogram", "pos": "top-left", "scale": 0.050},
        "eyebrow": {"font": "raleway", "size": 0.018, "track": 0.15, "show": True},
        "h1": {"font": "cormorant", "size": 0.048, "leading": 1.05, "upper": False},
        "sub": {"font": "none"},
        "cta": {"style": "underline", "font": "raleway", "size": 0.018},
        "rule": "none", "scrim": "soft", "color": "auto", "margin": 0.065,
    },
}
ARCH_NAMES = list(ARCHETYPES.keys())


def _clone(d):
    import copy
    return copy.deepcopy(d)


def make_spec(arch_name, copy, i=0):
    """Concrete spec = archetype template + this scene's copy + per-index knob jitter (reproducible by i).
    copy = {"eyebrow","h1","cta","product"}. h1 may contain '|' or newlines for line breaks."""
    rng = random.Random(i * 131 + hash(arch_name) % 997)
    s = _clone(ARCHETYPES[arch_name])
    s["name"] = arch_name
    # inject copy
    h1 = (copy.get("h1") or "").replace("\n", "|")
    s["h1"]["text"] = h1
    if s.get("eyebrow", {}).get("show"):
        s["eyebrow"]["text"] = copy.get("eyebrow", "")
    # sub text: for script/serif sub archetypes, use the CTA line as the evocative sub (team uses script subs);
    # for the no-sub archetypes leave it off.
    if s.get("sub", {}).get("font", "none") != "none":
        s["sub"]["text"] = copy.get("cta", "") if arch_name == "heritage-bottomcenter" else copy.get("eyebrow", "")
    # cta text
    if s.get("cta", {}).get("style", "none") != "none":
        s["cta"]["text"] = copy.get("cta", "")
    # --- jitter knobs (kept within tasteful bands)
    s["h1"]["size"] = round(s["h1"]["size"] * rng.uniform(0.92, 1.10), 4)
    s["logo"]["scale"] = round(s["logo"]["scale"] * rng.uniform(0.9, 1.15), 4)
    if s.get("eyebrow", {}).get("show"):
        s["eyebrow"]["track"] = round(s["eyebrow"]["track"] * rng.uniform(0.85, 1.25), 3)
    # occasionally swap the logo variant within the family's tone (keeps brand, adds variety)
    if rng.random() < 0.35:
        s["logo"]["variant"] = rng.choice(LOGO_VARIANTS)
    # occasionally drop the scrim (team uses little) to test cleaner placement
    if s["scrim"] == "soft" and rng.random() < 0.4:
        s["scrim"] = "none"
    # occasionally use the image-aware auto anchor instead of the fixed one
    if rng.random() < 0.25:
        s["anchor"] = "auto"
    return s


def resolve_logo_tone(variant, lum):
    """Pick a logo variant that CONTRASTS the copy region (fixes dark-logo-on-dark + cream-on-bright).
    lum = copy-region luminance from scene_place (0..1); <0.55 => dark region (light type/logo)."""
    bright = lum >= 0.55
    if variant in (None, "", "auto"):
        return "wordmark-dark" if bright else "wordmark"
    if bright and variant in ("monogram", "wordmark"):
        return "wordmark-dark"        # no dark monogram exists -> swap to the dark wordmark for contrast
    if not bright and variant == "wordmark-dark":
        return "wordmark"             # dark logo on a dark region is invisible -> swap to the light wordmark
    return variant


def resolve_layout(scene_path, spec, finish=None):
    """Scene-dependent layout decisions shared by BOTH renderers (render_ad PIL preview + figma_ad Figma
    vector): copy-block geometry (fixed anchor or image-aware, product-gated), text color, and a
    contrast-correct logo variant. Returns a NORMALIZED box so each renderer scales to its frame.
    Single source of truth so the production board matches the tournament preview."""
    import scene_place
    p = scene_place.place(scene_path, finish=finish)
    margin = spec.get("margin", 0.065)
    anchor = spec.get("anchor", "auto")
    relocated = False
    if anchor == "auto":
        nx, ny, nw, nh, align = p["nx"], p["ny"], p["nw"], p["nh"], p["align"]
    else:
        wide = "center" in anchor
        nw, nh = (0.80 if wide else 0.56), 0.46
        nx = margin if "left" in anchor else (1 - nw - margin if "right" in anchor else (1 - nw) / 2)
        ny = margin if "top" in anchor else (1 - nh - margin if "bottom" in anchor else (1 - nh) / 2)
        align = "center" if wide else ("right" if "right" in anchor else "left")
        if scene_place.box_product_fraction(scene_path, (nx, ny, nw, nh), finish=finish) > 0.15:
            nx, ny, nw, nh, align = p["nx"], p["ny"], p["nw"], p["nh"], p["align"]
            relocated = True
    cmode = spec.get("color", "auto")
    color = cmode if cmode in ("light", "dark") else ("light" if p["lum"] < 0.55 else "dark")
    logo = dict(spec.get("logo", {}))
    logo["variant"] = resolve_logo_tone(logo.get("variant", "auto"), p["lum"])
    return {"box": [round(nx, 4), round(ny, 4), round(nw, 4), round(nh, 4)], "align": align,
            "color": color, "logo": logo, "relocated": relocated, "lum": round(p["lum"], 3),
            "scrim_mode": spec.get("scrim", "none"),                       # lighter scrim than the old radial
            "scrim_strength": round(min(0.34, p["scrim"] * 0.7 + 0.02), 3)}


def bucket(spec):
    """Diversification bucket key — keep a champion PER family so the loop yields a varied set."""
    return spec.get("name", "?")


def sample_specs(copy, n, start=0):
    """n concrete specs for one scene's copy, cycling archetypes so every family is represented."""
    return [make_spec(ARCH_NAMES[(start + k) % len(ARCH_NAMES)], copy, start + k) for k in range(n)]
