# RUN: RS_20260613_p2

| Field | Value |
|-------|-------|
| run_id | RS_20260613_p2 |
| brand | RS |
| date | 2026-06-13 |
| product | Carrara-marble + brass toggle switch plate & outlet cover |
| placement | Wall-mounted hardware, macro vignette beside cased doorway |
| output_type | SCENE (copy zone reserved, empty) |
| aspect | 4:5 |
| model | nano_banana_flash (submitted as nano_banana_2, routed to flash) |
| job_id | adea0822-42ff-4587-a56a-fe5474a70815 |
| status | qc-failed |

## Prompt used

```
Photorealistic 4K lifestyle advertising image of a honed Carrara-marble and polished-brass toggle switch plate with matching outlet cover, mounted flush on a warm limewash plaster wall beside a white-painted wood door casing. The marble panel shows natural grey veining; the polished brass toggle is in the ON position, catching the directional golden light with a warm specular gleam — the brightest metallic point in frame. Visible photographic grain and natural light falloff across the plaster surface; material detail sharp and tactile.

Wall-mounted hardware detail — tight eye-level macro vignette at the cased doorway junction. White-painted wood door casing breaks into the left edge of frame. Warm oak plank floor at lower corner.

Product and visual interest composed to the right; the left ~45% of frame a single large unbroken limewash plaster plane — plain, raking-lit, reserved for ad copy. Macro framing.

Golden-hour warm directional light through sheer curtains casting soft window-pane shadows raking across the plaster wall from upper left; the polished brass toggle and marble face catch the warm side-light — the brightest point in frame. No overhead fill; natural falloff into shadow on the right edge.

Shot on full-frame, 50mm, f/2.8. Shallow depth of field softens the door casing; the switch plate is critically sharp. Real photographic grain throughout.

High-end home-decor editorial, lived-in and curated — never showroom.

Warm neutral limewash plaster shell dominates the frame; exactly one sage-green ceramic vessel on a narrow oak ledge just entering lower right — the single color accent; brass and walnut details on the hardware.

4:5, 2K.

No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents.
```

## Refs / Elements
- packshot: none (no registered SKU Element for this product yet)

## QC Gate-1 Verdict (Judge B — google/gemini-3.1-pro-preview)

| Dimension | Score |
|-----------|-------|
| photorealism | 4 |
| product_fidelity | 3 |
| brand_fit | 4 |
| lighting_composition | 5 |
| ad_usability | 3 |
| **TOTAL** | **3.8** |

**Verdict: FAIL**

hard_fails: warped product details (AI artifacts on outlet holes)

biggest_issue: No packshot was provided to verify the product, and the electrical outlet exhibits clear AI warping on the plug holes.

fix: Inpainting → redraw the electrical outlet to have accurate, standard plug holes (ONE composer field change → inpainting pass via flux_kontext on the outlet region).

## Self-critique (Judge A)

Lighting and composition are strong — the limewash plaster copy zone is clean and the brass toggle catch-light reads well. The marble veining is plausible. The outlet holes exhibit the characteristic AI distortion common on electrical hardware. Fix path: flux_kontext inpainting on the outlet region, or register a packshot Element for this SKU and re-anchor the product.

Brand compliance:
- [x] neutral shell ~70% dominant
- [x] ONE accent (sage ceramic), green-first
- [x] brass hero-lit as focal point
- [x] brass present
- [x] wall broken up by door casing
- [x] golden-hour light
- [ ] product_fidelity ≥ 4 NOT met (outlet AI artifacts, no packshot anchor)

## Next iteration

Per R6 (one fix per cycle): fix = inpainting pass on outlet plug holes via flux_kontext.
Do not regen from scratch — lighting/composition/copy-zone passed. Preserve everything else.

## Files

- output.png — generated image (928×1152 px, 1K)
- output.png.judge.json — full judge verdict
- hp_entry.md — HIGGSFIELD_PAIRS-format training entry (SRC higgsfield)
