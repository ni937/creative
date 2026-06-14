# HIGGSFIELD_PAIRS entry — RS_20260613_p2
# SRC: higgsfield | Stream B | DO NOT merge into Stream A (Figma harvest)
# Per 00_SYSTEM/PROVENANCE.md — Higgsfield gens are isolated from Figma REFS

---

## Entry

**pair_id:** HP-RS-20260613-p2
**brand:** RS
**date:** 2026-06-13
**src:** higgsfield
**job_id:** adea0822-42ff-4587-a56a-fe5474a70815
**model:** nano_banana_flash
**aspect_ratio:** 4:5
**resolution:** 1K (928×1152)

**product:** Carrara-marble + polished-brass toggle switch plate with outlet cover
**placement:** Wall-mounted hardware — macro vignette beside cased doorway
**output_type:** SCENE (copy zone reserved)
**refs:** none (no packshot, no Element)

**output:** output.png

## Prompt (verbatim)

Photorealistic 4K lifestyle advertising image of a honed Carrara-marble and polished-brass toggle switch plate with matching outlet cover, mounted flush on a warm limewash plaster wall beside a white-painted wood door casing. The marble panel shows natural grey veining; the polished brass toggle is in the ON position, catching the directional golden light with a warm specular gleam — the brightest metallic point in frame. Visible photographic grain and natural light falloff across the plaster surface; material detail sharp and tactile.

Wall-mounted hardware detail — tight eye-level macro vignette at the cased doorway junction. White-painted wood door casing breaks into the left edge of frame. Warm oak plank floor at lower corner.

Product and visual interest composed to the right; the left ~45% of frame a single large unbroken limewash plaster plane — plain, raking-lit, reserved for ad copy. Macro framing.

Golden-hour warm directional light through sheer curtains casting soft window-pane shadows raking across the plaster wall from upper left; the polished brass toggle and marble face catch the warm side-light — the brightest point in frame. No overhead fill; natural falloff into shadow on the right edge.

Shot on full-frame, 50mm, f/2.8. Shallow depth of field softens the door casing; the switch plate is critically sharp. Real photographic grain throughout.

High-end home-decor editorial, lived-in and curated — never showroom.

Warm neutral limewash plaster shell dominates the frame; exactly one sage-green ceramic vessel on a narrow oak ledge just entering lower right — the single color accent; brass and walnut details on the hardware.

4:5, 2K.

No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents.

## QC scores (Judge B — google/gemini-3.1-pro-preview)

| photorealism | product_fidelity | brand_fit | lighting_composition | ad_usability | total |
|---|---|---|---|---|---|
| 4 | 3 | 4 | 5 | 3 | 3.8 |

**verdict:** FAIL
**hard_fail:** warped product details (AI artifacts on outlet holes)

## What worked (reusable)

- Limewash plaster copy zone (left 45%) was clean, uncluttered, and copy-ready — lighting/composition passed (5/5)
- Brass toggle catch-light executed well; hardware hero-lit from golden-hour side-light
- Marble veining rendered plausibly; material grain convincing
- ONE sage accent correctly placed, not competing

## What failed (root cause)

- Outlet plug holes exhibit AI distortion — a known failure mode for electrical hardware without packshot anchoring
- No packshot/Element → product_fidelity capped at 3 by judge protocol
- ad_usability (3) reflects product distortion dragging down drop-in readiness

## Fix path (one field, R6)

flux_kontext inpainting on the outlet plug-hole region → redraw with accurate standard US duplex outlet geometry.
Do NOT regen full scene — lighting/comp/copy-zone all passed.

## Promotion gate

NOT eligible for WINNING.md (total < 5.0, verdict FAIL, fidelity < 5).
Eligible for learning signal only (MEDIUM — judge feedback, structural unchanged).
