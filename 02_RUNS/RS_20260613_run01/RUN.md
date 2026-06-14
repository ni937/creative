# RUN: RS_20260613_run01
brand: RS | status: generated → qc-failed
model_requested: nano_banana_2 | model_reported: nano_banana_flash (Higgsfield backend alias for nano_banana_2)
resolution: 2K (1856×2304) | aspect: 4:5 | refs/elements: none (no packshot — first run for this SKU)
job_id: 5aa6bcd6-0007-4ee1-a219-0eff07de14a7
output: 02_RUNS/RS_20260613_run01/output.png | /tmp/run1.png
date: 2026-06-13

## prompt (composed — 12-field RS PROMPT_COMPOSER, all locks verbatim)

Photorealistic 4K lifestyle advertising image of a sculptural solid-brass chandelier with seeded-glass bell shades, all bulbs burning warm amber, hung from ceiling over an oval walnut dining table.

Chandelier and dining table composed to the left; the right ~45% of frame is a single large empty warm limewash plaster plane — uninterrupted, reserved for ad copy. Full-frame framing.

High-ceilinged transitional dining room: forest-green zellige tile wainscot wraps the lower walls; upper walls warm limewash plaster; exposed white-oak ceiling beams differentiate the ceiling from the walls; room plausibly scaled.

Golden-hour warm directional light through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing warm — the brightest point in frame.

Shot on full-frame, 50mm, f/2.8; real photographic grain, natural light falloff, soft bokeh on empty background plaster plane.

High-end home-decor editorial, lived-in and curated.

Warm neutral plaster shell dominates the frame; exactly one forest-green accent on zellige wainscot; brass and walnut details.

4:5, 2K.

No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents.

## brand essentials pre-flight (6/6 ✓)
[✓] neutral shell ~70% dominant
[✓] exactly ONE accent (green-first) — forest-green zellige wainscot
[✓] fixture ON + glowing as focal point
[✓] brass/walnut present
[✓] wall surface broken up (zellige wainscot)
[✓] golden-hour warm directional light

## self-critique (Judge A — visual read of output)
Iteration 1 (only — user-directed single pass):
- photorealism: 4.5 (indistinguishable from real photo, natural grain, convincing shadows)
- brand_fit: 5 (limewash plaster dominant, ONE forest-green zellige accent, brass+walnut, copy zone clean)
- lighting_composition: 4.5 (golden-hour cast excellent; white-oak beams visible; window pane shadows; copy zone clean right 45%)
- ad_usability: 4.5 (right 45% uncluttered plaster plane, drop-in ready)
- product_fidelity: N/A (no packshot — no reference to judge against)
- NOTE: window is slightly brighter than the chandelier — fixture glow is warm and clearly on but window light competes for brightest-point. Flag for next run.
- Total self: ~4.5 on addressable dims

## qc gate: FAIL
Judge B: google/gemini-3.1-pro-preview via OpenRouter (scripts/qc_judge.py)
| dim | score |
|---|---|
| photorealism | 4.5 |
| product_fidelity | 3 (HARD CAP — no packshot; judge script auto-caps when product present without ref) |
| brand_fit | 5 |
| lighting_composition | 5 |
| ad_usability | 4 |
| **total** | **4.3** |
| verdict | **FAIL** (total 4.3 < 4.5 threshold; product_fidelity 3 < 4 hard requirement) |

hard_fails: [] — no visual defects, no brand violations
biggest_issue: no packshot provided → fidelity capped at 3 (structural, not creative)
fix (per judge): supply chandelier packshot or register as Element (T1)

## failure classification
MECHANICAL FAIL — image quality and brand compliance are strong (4.5/5/5/4 on addressable dims). FAIL is entirely due to absent packshot. Not a prompt problem. Same pattern as HP-001, HP-002, HP-003, HP-004.

## human gate: NOT REACHED (qc-failed — per automation rules, fails never reach Figma)

## verification: n/a (no prior fix being tested)

## model note
nano_banana_2 requested per ENGINE_HIGGSFIELD.md hard rule (Nick, 2026-06-13).
Higgsfield MCP internally routed to `nano_banana_flash` — confirmed internal alias behavior
(also observed in RS_20260613_p2). External ID `nano_banana_2` IS the correct request;
backend naming is an implementation detail. Flagged for Nick awareness.
