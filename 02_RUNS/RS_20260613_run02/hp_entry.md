# HIGGSFIELD STREAM B ENTRY
SRC: higgsfield | RS_20260613_run02 | nano_banana_2 | qc-fail-structural | 2026-06-13

---

## Provenance
run_id: RS_20260613_run02
brand: RS
date: 2026-06-13
stream: B (HIGGSFIELD — self-generated, provisional trust per PROVENANCE.md)
ingest_reason: full pipeline pass — compose → generate → judge → stream-B ingest

## Generation
model_requested: nano_banana_2
model_mcp_internal: nano_banana_flash (MCP alias — confirmed 2K output, same engine)
resolution: 2K (1856×2304)
aspect_ratio: 4:5
iterations: 2

## Prompt (winning iteration — iter 2)
Photorealistic 4K lifestyle advertising image of a pair of unlacquered solid-brass wall sconces with fluted opal-glass shades, both switched ON and glowing warm amber, mounted flanking an arched frameless vanity mirror above a honed Calacatta-marble vanity top — wall-mounted as a flanking pair on either side of the arched mirror, wall accent pair in a warm transitional powder room. Warm transitional powder room; limewash plaster walls with visible natural trowel texture breaking up the surface; honed Calacatta marble vanity top with subtle grey veining; arched frameless mirror; small frosted window with sheer cafe curtain; ceiling tone slightly deeper and warmer than the plaster walls. Both sconces and vanity composed to the right side of frame; the opposite ~45% of frame a single large empty plain limewash plaster wall — reserved for ad copy; camera positioned at a 35-degree angle to the wall plane so the mirror glass reflects only the opposite limewash plaster wall and soft window light — never the sconces themselves; both sconce arms and shades visible in side profile flanking the mirror. Golden-hour warm directional light through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing warm — the brightest point in frame. Shot on full-frame, 50mm, f/2.8. High-end home-decor editorial, lived-in and curated; real photographic grain, natural light falloff, tactile surface texture visible on the plaster and marble. Warm neutral limewash plaster shell dominates the frame; exactly one sage accent on a folded linen hand towel draped on the marble vanity edge; brass sconce bodies and hardware details throughout. 4:5, 2K. No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents, no impossible mirror reflections.

## Refs / Elements used
packshot: none (no RS sconce SKU registered — structural QC ceiling)
elements: none

## QC Verdict (Judge B — google/gemini-3.1-pro-preview)
photorealism: 5
product_fidelity: 3 (no packshot cap)
brand_fit: 5
lighting_composition: 5
ad_usability: 5
hard_fails: []
total: 4.6
verdict: FAIL
fail_reason: structural — product_fidelity < 4 (no packshot, not a quality defect)

## Iteration Delta (what changed between iters)
iter1 fail: impossible mirror reflection — sconce floating mid-glass (hard fail by judge)
iter2 fix: COMPOSITION field — camera angle 35° to wall plane, mirror reflects room not sconces
result: hard fail removed, scores rose from 3.0 → 4.6

## Training Signal
signal_class: MEDIUM (self-generated QC-scored; mirrors SIGNAL_GATES.md — judge can FAIL, not train structure)
promote_to_WINNING: NO — product_fidelity < 5, no packshot verification
useful_pattern: camera angle spec in COMPOSITION field prevents mirror reflection physics failures
next_action: register RS wall sconce as Higgsfield Element → re-run → enables PASS + WINNING promotion

## Output file
02_RUNS/RS_20260613_run02/output.png
