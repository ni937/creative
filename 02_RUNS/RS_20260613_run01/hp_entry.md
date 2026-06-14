# HIGGSFIELD_PAIRS entry — RS_20260613_run01
# SRC: higgsfield | Stream B | ISOLATED — DO NOT merge into Stream A (Figma harvest)
# Per 00_SYSTEM/PROVENANCE.md — Higgsfield gens are isolated from Figma REFS

## Metadata
- pair_id: HP-005 (appended to 01_BRANDS/RS/HIGGSFIELD_PAIRS.md)
- run_id: RS_20260613_run01
- brand: RS
- date: 2026-06-13
- src: higgsfield
- stream: B
- job_id: 5aa6bcd6-0007-4ee1-a219-0eff07de14a7
- model_requested: nano_banana_2
- model_reported: nano_banana_flash (Higgsfield backend alias)
- aspect_ratio: 4:5
- resolution: 2K (1856×2304)
- output: 02_RUNS/RS_20260613_run01/output.png
- SRC tag: SRC: higgsfield | RS_20260613_run01 | nano_banana_2 (reported: nano_banana_flash) | FAIL (fidelity-cap) | 2026-06-13

## Prompt (verbatim, as composed)

Photorealistic 4K lifestyle advertising image of a sculptural solid-brass chandelier with seeded-glass bell shades, all bulbs burning warm amber, hung from ceiling over an oval walnut dining table.

Chandelier and dining table composed to the left; the right ~45% of frame is a single large empty warm limewash plaster plane — uninterrupted, reserved for ad copy. Full-frame framing.

High-ceilinged transitional dining room: forest-green zellige tile wainscot wraps the lower walls; upper walls warm limewash plaster; exposed white-oak ceiling beams differentiate the ceiling from the walls; room plausibly scaled.

Golden-hour warm directional light through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing warm — the brightest point in frame.

Shot on full-frame, 50mm, f/2.8; real photographic grain, natural light falloff, soft bokeh on empty background plaster plane.

High-end home-decor editorial, lived-in and curated.

Warm neutral plaster shell dominates the frame; exactly one forest-green accent on zellige wainscot; brass and walnut details.

4:5, 2K.

No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents.

## Reference Inputs
- packshot: none (no packshot or Element registered for this SKU — first run)
- scene_ref: none

## QC Scores (Judge B — google/gemini-3.1-pro-preview via OpenRouter)
| dimension | score |
|---|---|
| photorealism | 4.5 |
| product_fidelity | 3 (packshot-absent auto-cap) |
| brand_fit | 5 |
| lighting_composition | 5 |
| ad_usability | 4 |
| **total** | **4.3** |
| verdict | FAIL (packshot-absent only — no hard fails, no visual defects) |

hard_fails: []
biggest_issue: no packshot for fidelity verification
fix: supply chandelier packshot or register as Higgsfield Element (T1)

## What Worked (reusable)
- Forest-green zellige wainscot + limewash plaster + white-oak beams = RS transitional dining room archetype executed cleanly on first shot — brand_fit 5/5
- Right ~45% clean empty plaster plane fully usable as copy zone — ad_usability 4/5
- Chandelier visibly ON with warm amber glow; brass and walnut materials correctly dominant
- Real photographic grain, natural light falloff, soft bokeh — photorealism 4.5/5
- ONE forest-green accent (zellige only), zero competing pops — brand rule held
- Composition (chandelier + table to left, empty right) hits the FULL_AD ad-format layout correctly

## What to Improve (next run)
- Provide chandelier packshot OR register as Element (T1) to unlock fidelity scoring
- Window pane on left is slightly brighter than fixture — consider reducing window prominence or adding a dimmer instruction to make fixture the unambiguous "brightest point"
- Seeded-glass shades rendered slightly conical rather than bell-shaped — note for packshot comparison when available

## Archetype Tags
overhead-hero | chandelier | dining-room | transitional | forest-green-zellige | brass-walnut | copy-zone-right | golden-hour | oak-beams

## Promotion Gate
NOT eligible for WINNING.md — verdict FAIL, total 4.3 < 5.0, fidelity < 5.
Learning signal: MEDIUM (judge feedback; structural unchanged; corroborates pattern from HP-001/002/003/004).
Next required action: Element registration (T1) or packshot supply → rerun.
