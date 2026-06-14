# RUN: RS_20260613_p3
date: 2026-06-13
brand: RS | Residence Supply
product: Turned solid-brass table lamp, pleated oatmeal-linen shade, lamp ON
placement: Console/nightstand — surface accent, transitional entryway
aspect: 4:5 (rendered 3:4 / 880×1168 — closest match)
model: gpt_image_2 (Higgsfield)
job_id: 5ec3e064-eee8-4e30-8163-84de433e2523
output: 02_RUNS/RS_20260613_p3/output.png  |  /tmp/p3.png
cdn: https://d8j0ntlcm91z4.cloudfront.net/user_351PcLsaCFYLgx02Flw3rHfIWkq/hf_20260614_013509_5ec3e064-eee8-4e30-8163-84de433e2523.png
refs: none (no packshot — scene-template run; R7 cap applies)
iterations: 1 (first-shot)

## Composed prompt (field-by-field)
1. TASK: Photorealistic 4K lifestyle advertising image of
2. SUBJECT: a turned solid-brass table lamp with a pleated oatmeal-linen shade, lamp switched ON casting warm amber glow — the brightest point in frame.
3. PLACEMENT: surface accent on a walnut console table with turned legs in a transitional residential entryway. One small olive-glaze ceramic vessel beside the lamp as the single color accent.
4. ENVIRONMENT: bead-board wainscot paneling below chair rail painted soft white; upper walls warm plaster in pale greige tone; ceiling differentiated — off-white with classic crown molding; herringbone oak plank floor. Plausibly scaled room. No clutter.
5. COMPOSITION: product and visual interest composed to the right side of frame; the opposite ~45% of the frame is a single large empty plane — the warm plaster wall — reserved for ad copy. Macro editorial framing filling the 4:5 frame.
6. LIGHTING 🔒: Golden-hour warm directional light through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing warm — the brightest point in frame. Real photographic light falloff, natural film grain visible in shadow areas, material texture fully present: linen weave in shade, machined-brass ridges on the turned base.
7. CAMERA: shot on full-frame, 50mm, f/2.8. Shallow depth of field softening background.
8. STYLE: high-end home-decor editorial, lived-in and curated. Kinfolk-adjacent warmth, never showroom sterility.
9. MOOD/COLOR 🔒: Warm neutral plaster shell dominates ~70% of frame; exactly one olive-green accent on the ceramic vessel; brass lamp base and walnut console as material anchors.
10. OUTPUT: 4:5, 2K
11. EXCLUSIONS 🔒: no text, no watermark, no logos, no warped perspective, no CGI or 3D-render look, no illustration, no flat dead beige, no people, no clutter, no competing color accents, no extra products.
12. TEXT: none (SCENE output)

## Brand essentials compliance (pre-generate check)
- [x] neutral shell ~70% dominant
- [x] exactly ONE accent (olive ceramic vessel — green-first)
- [x] fixture ON + glowing as focal point
- [x] brass/walnut present
- [x] wall surface broken up (bead-board wainscot)
- [x] golden-hour warm directional light
Compliance: 6/6 ✅

## Self-critique (visual read)
Image matches brief precisely. Turned brass base with pleated linen shade is clearly rendered and switched ON — warm amber glow radiates from the shade as the brightest point. Bead-board wainscoting and warm plaster upper wall are both present. Large (~45%) empty plaster plane on the left is clean and ad-ready. Window-pane shadow pattern on the left wall is a genuine premium signal — reads as real photography. Olive-glaze ceramic vessel is the sole accent, flanking the lamp on the console. Herringbone floor and crown molding visible at edges. No clutter, no people, no text, no CGI look. Photorealism is convincing: film grain and natural falloff are present.

| dimension            | self | judge (gemini-3.1-pro) |
|----------------------|------|------------------------|
| photorealism         | 5    | 5                      |
| product_fidelity     | 3    | 3 (capped — no packshot, per script L99-102) |
| brand_fit            | 5    | 5                      |
| lighting_composition | 5    | 5                      |
| ad_usability         | 5    | 5                      |
| **TOTAL**            | **4.6** | **4.6**            |

judge_model: google/gemini-3.1-pro-preview
hard_fails: []
biggest_issue: No packshot supplied — fidelity capped at 3 by script design (R7). Creative has no issues.
fix: Register lamp SKU as Higgsfield Element (T1) or supply packshot ref on next run.
verdict: FAIL (mechanical — fidelity cap; creative is PASS-quality at 5/5 on all soft dims)

## QC artifact
02_RUNS/RS_20260613_p3/output.png.judge.json

## Next action
Creative is first-shot excellent. Unblock with a packshot ref or Element registration.
verification_status: PENDING
