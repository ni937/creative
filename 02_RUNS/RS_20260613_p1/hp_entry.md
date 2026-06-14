# HIGGSFIELD_PAIRS entry — RS_20260613_p1
# SRC: higgsfield  (stream B — isolated, no cross-contamination with stream A / Figma refs)
# Status: QC FAIL — do NOT promote to HIGGSFIELD_PAIRS.md without re-run PASS

---

**pair_id:** RS_20260613_p1  
**brand:** RS  
**date:** 2026-06-13  
**src:** higgsfield  
**qc_verdict:** FAIL  
**qc_total:** 3.2  
**judge_model:** google/gemini-3.1-pro-preview  

---

## PROMPT

```
Photorealistic 4K lifestyle advertising image of an unlacquered solid-brass bridge kitchen faucet with cross-handle levers, installed on a white fireclay apron-front farmhouse sink set into a honed Calacatta marble countertop; raw brass showing warm natural depth and tonal variation.

Product and visual interest composed to the right side of the frame; the left 45% of the frame is a single large empty plane of bare limewash plaster wall — clean and unbroken — reserved for ad copy.

Kitchen environment: limewash plaster walls in warm greige; one recessed walnut open shelf in the upper background holding a few sage-glazed ceramic vessels; honed marble counter with a thin waterfall edge; aged wood ceiling beam differentiating the ceiling from the walls; room plausibly scaled, no clutter.

Golden-hour warm directional light rakes in from a small window, casting soft window-pane shadow geometry across the marble counter. The brass faucet is the hero-lit focal point — catching the warm low sun in a concentrated highlight, the brightest and most luminous element in frame; natural light falloff dims the background.

Shot on full-frame camera, 50mm lens, f/2.8, shallow depth of field softening the background shelving into warm bokeh. Visible film grain, natural chromatic texture, real-photo weight.

Warm neutral limewash plaster shell dominates the frame (~70%); exactly one sage/olive accent on ceramic vessels on the walnut shelf; brass and walnut details throughout.

Style: high-end home-decor editorial, lived-in and curated, Kinfolk-adjacent. Real photo texture: visible material grain, natural light falloff, slight vignette. 4:5.

No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents.
```

---

## REFS USED

none — no packshot or Element registered for this SKU

---

## OUTPUT

- **file:** output.png (880×1168, 3:4, 1K)  
- **job_id:** f4f7b347-a309-462a-bbf4-19d5b1e80507  
- **model:** gpt_image_2  

---

## QC SCORES

| dim | score |
|-----|-------|
| photorealism | 4.5 |
| product_fidelity | 3 |
| brand_fit | 2 |
| lighting_composition | 4.5 |
| ad_usability | 2 |
| **total** | **3.2** |
| verdict | FAIL |

hard_fails: `fixture OFF in hero shot`

---

## LEARNINGS (for next run)

- **WHAT WORKED:** Window-pane shadow geometry on marble counter; limewash plaster copy zone; sage ceramic vessels; brass warm-catch in directional light; photorealism near indistinguishable from real photo
- **WHAT FAILED:** No ref = product_fidelity hard-fail. "Fixture ON" not met — faucet dry. Resolution 1K/low.
- **NEXT PROMPT DELTA:** Add `water flowing from the faucet spout, catching the warm light` + pass packshot ref + set quality high

---

_Entry created: 2026-06-13 | Not eligible for HIGGSFIELD_PAIRS.md promotion until QC PASS_
