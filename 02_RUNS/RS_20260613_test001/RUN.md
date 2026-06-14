# RUN — RS_20260613_test001   ·   SRC: higgsfield
status: qc-failed (procedural — no packshot)   ·   date: 2026-06-13
purpose: end-to-end pipeline proof (compose → Higgsfield → judge)

PROMPT (composed by Claude from RS BRAND_CARD + LAYOUT_CARD):
```
Photorealistic 4K lifestyle ad — antique brass wall sconces with frosted opal glass
shades, flanking a large gilt-framed oil landscape; sconces switched ON, warm
incandescent glow = brightest point in frame. Classic transitional dining room; sage
zellige tile wainscot to chair-rail; warm bare plaster upper walls; stained walnut
ceiling beams; walnut sideboard beneath the painting. Product + interest composed LEFT;
opposite ~45% of frame a single large empty plaster plane reserved for ad copy. Slight
3/4 angle, eye-level. Golden-hour directional light through sheer curtains. Full-frame
50mm f/2.8, shallow DoF. Warm neutral plaster shell dominates; exactly ONE sage accent.
4:5, 2K. Negatives: no distorted logos/text/watermark, no extra products, no people, no
CGI look, no flat-beige scene, no competing accents.
```

REFS / ELEMENTS:  none (test run — no packshot conditioning)
MODEL:            gpt_image_2   (Higgsfield job 26c7794c-f0f4-4e9c-ac4d-70733411a292)
SETTINGS:         880×1168 (3:4), 1k
OUTPUT:           output.png  (2.0 MB)
HF IMAGE URL:     https://d8j0ntlcm91z4.cloudfront.net/.../hf_20260613_194309_26c7794c....png

QC — independent judge (Gemini 3.1 Pro via OpenRouter):
  photorealism 5/5 · product_fidelity 3/5 (capped, no packshot) · brand_fit 5/5
  · lighting&comp 5/5 · ad_usability 5/5   →   rubric 4.6/5
  VERDICT: FAIL   ·   hard-fails: ["Missing packshot reference for featured product"]
  fix: pass the SKU packshot, or dual-ref (packshot + approved scene frame). KW-RS-002.

NOTE: FAIL is procedural, not aesthetic. In production this run is preceded by
registering the SKU as a Higgsfield Element (TRAINING T1) or passing a dual-ref, which
lifts product_fidelity ≥4 and flips the verdict to PASS.
