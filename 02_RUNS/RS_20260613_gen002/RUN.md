# RUN: RS_20260613_gen002
brand: RS | status: qc-failed (fidelity — no packshot)
model: gpt_image_2 | refs/elements: none | aspect: 3:4 (closest to 4:5) | job-id: 53099e82-f520-4766-abe0-3d88bcd420fb
SRC: higgsfield | RS_20260613_gen002 | gpt_image_2 | FAIL | 2026-06-13

## prompt (as composed — 12 fields, brand-locked)
Photorealistic 4K lifestyle advertising image of a sculptural solid-brass 5-arm chandelier with
seeded-glass bell shades, all five bulbs glowing warm amber, hung from ceiling centered above an
oval walnut dining table. High-ceilinged transitional dining room; forest-green zellige tile
wainscot rising 36 inches; warm limewash plaster walls above; ceiling differentiated by exposed
white-oak beams; tall arched window with sheer linen curtains. Chandelier and dining setting
composed to the right; the left ~45% of frame a single large empty plane — plain warm plaster
wall — reserved for ad copy; camera at seated eye level. Golden-hour warm directional light
through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing
warm — the brightest point in frame. Shot on full-frame, 50mm, f/3.2. High-end home-decor
editorial, lived-in and curated; real photographic texture — visible material grain, natural
light falloff. Warm neutral plaster shell dominates the frame; exactly one forest-green accent
on the zellige tile wainscot; brass and walnut details. 4:5, 2K. No distorted logos, no warped
labels, no extra text, no watermark, no extra products, no clutter, no people, no warped
perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color
accents.

## brand compliance check (6/6 at compose time)
- [x] neutral shell ~70% dominant — plaster left wall + upper walls dominate
- [x] exactly ONE accent (green-first) — forest-green zellige wainscot
- [x] fixture ON + glowing as focal point — all five shades glowing amber; visually brightest point
- [x] brass/walnut present — brass chandelier, walnut round table + chairs
- [x] wall surface broken up — zellige wainscot + limewash plaster above + exposed wood ceiling beams
- [x] golden-hour warm directional light — locked field 6 verbatim

## self-critique (visual inspection of output.png)
Photorealism: 5/5 — real editorial photograph feel; visible grain, natural DOF, plausible scale.
Brand fit: 5/5 — all six essentials confirmed in the rendered image.
Lighting/composition: 5/5 — ~45% left plane clean and empty, window shadows soft, fixture the
  clear brightest point.
Ad usability: 5/5 — copy space generous and clean.
Product fidelity: 3/5 — chandelier visible and plausible RS brass style; HARD-CAPPED because no
  packshot ref supplied (per R7 and KNOWN_WIN KW-RS-002; same penalty as HP-001).
No iteration needed — fidelity cap is structural, not fixable by prompt editing alone.

## qc gate: FAIL
Judge: google/gemini-3.1-pro-preview via OpenRouter
Verdict: FAIL | photorealism 5 | product_fidelity 3 (HARD FAIL — no packshot) | brand_fit 5 |
  lighting_composition 5 | ad_usability 5 | total 4.6
hard_fails: [] (no banned-list hits, no distortion — pure missing-ref penalty)
biggest_issue: No packshot provided to verify the hero chandelier's accuracy, capping fidelity at 3.
fix: register chandelier as Higgsfield Element OR supply packshot ref on next run.

## human gate: not reached (qc-failed)
## verification: n/a
## notes
This run was a deliberate test of the scene-composition prompt without a product ref.
Soft scores (photorealism, brand_fit, lighting_composition, ad_usability) all 5/5 — the prompt
template is operating at ceiling on everything the scene controls. The ONLY gate standing between
this run and a PASS is R7 / T1: a registered product Element or packshot ref. Next step: register
the chandelier SKU as an Element (T1) and re-run — the scene prompt needs zero changes.
