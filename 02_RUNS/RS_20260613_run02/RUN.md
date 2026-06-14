# RUN: RS_20260613_run02
date: 2026-06-13
brand: RS
status: qc-fail (structural — no packshot; quality 4.6/5.0)
placement: wall sconce pair, powder room, 4:5

## Model
requested: nano_banana_2 (per ENGINE_HIGGSFIELD.md mandate)
mcp-reported: nano_banana_flash (MCP internal alias for nano_banana_2 — confirmed same engine, 2K output)
resolution: 2K (1856×2304)
note: nano_banana_pro tested as alternative → job failed. nano_banana_2 request is correctly routed by MCP.

## Prompt (final — iteration 2)
Photorealistic 4K lifestyle advertising image of a pair of unlacquered solid-brass wall sconces with fluted opal-glass shades, both switched ON and glowing warm amber, mounted flanking an arched frameless vanity mirror above a honed Calacatta-marble vanity top — wall-mounted as a flanking pair on either side of the arched mirror, wall accent pair in a warm transitional powder room. Warm transitional powder room; limewash plaster walls with visible natural trowel texture breaking up the surface; honed Calacatta marble vanity top with subtle grey veining; arched frameless mirror; small frosted window with sheer cafe curtain; ceiling tone slightly deeper and warmer than the plaster walls. Both sconces and vanity composed to the right side of frame; the opposite ~45% of frame a single large empty plain limewash plaster wall — reserved for ad copy; camera positioned at a 35-degree angle to the wall plane so the mirror glass reflects only the opposite limewash plaster wall and soft window light — never the sconces themselves; both sconce arms and shades visible in side profile flanking the mirror. Golden-hour warm directional light through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing warm — the brightest point in frame. Shot on full-frame, 50mm, f/2.8. High-end home-decor editorial, lived-in and curated; real photographic grain, natural light falloff, tactile surface texture visible on the plaster and marble. Warm neutral limewash plaster shell dominates the frame; exactly one sage accent on a folded linen hand towel draped on the marble vanity edge; brass sconce bodies and hardware details throughout. 4:5, 2K. No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents, no impossible mirror reflections.

## Iterations
| iter | job_id | change | self-score | judge total | verdict |
|------|--------|--------|------------|-------------|---------|
| 1 | aa7467b3-90b5-43b7-860a-5ae79d73f2da | initial | ~3.5 | 3.0 | FAIL — impossible mirror reflection (sconce floating mid-glass) |
| 2 | f47077ab-6874-4840-821b-adb77383a177 | COMPOSITION: camera 35° angle to wall so mirror reflects room not sconces | ~4.3 | 4.6 | FAIL (structural: no packshot → product_fidelity capped at 3) |

## Judge Verdict (iteration 2 — final)
judge_model: google/gemini-3.1-pro-preview
photorealism: 5
product_fidelity: 3 (capped — no packshot; judge: "no hard fails on product design")
brand_fit: 5
lighting_composition: 5
ad_usability: 5
hard_fails: none
total: 4.6
verdict: FAIL
reason: product_fidelity < 4 (structural — no packshot to verify; not a quality failure)

## QC Notes
- Brand compliance: 6/6 BRAND_ESSENTIALS ✓
- Iteration 1 failure mode: impossible mirror reflection — sconce visible mid-glass in physically impossible position
- Iteration 2 fix: camera angle 35° to wall plane → mirror now shows room reflection (window + opposite wall) with left sconce physically plausible at edge
- Structural blocker: no RS sconce packshot or registered Element available → product_fidelity hard-capped at 3 → QC PASS unreachable without a ref
- Quality is high (4.6 fused) — this run is eligible for Stream B ingest and can inform future runs

## Files
output: 02_RUNS/RS_20260613_run02/output.png  (iteration 2 final, 1856×2304)
judge_json: 02_RUNS/RS_20260613_run02/output.png.judge.json
/tmp/run2.png (ephemeral copy per brief requirement)

## Learnings
- COMPOSITION FIX that works: specify exact camera angle (35°) to wall plane in the COMPOSITION field to prevent impossible mirror reflections — adds physically plausible geometry constraint the model can follow
- Mirror reflections in sconce/vanity scenes are a hard failure risk in iteration 1 — always add angle spec when a mirror is in frame
- No packshot = no QC PASS on product-present images (structural ceiling at product_fidelity=3). Next run: register RS sconce as Element or pass packshot ref.
