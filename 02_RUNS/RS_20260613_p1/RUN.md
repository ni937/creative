# RUN: RS_20260613_p1
**Date:** 2026-06-13  
**Brand:** RS (Residence Supply)  
**Product:** Unlacquered solid-brass bridge kitchen faucet  
**Placement:** Fireclay farmhouse sink, honed-marble counter, limewash plaster kitchen  
**Aspect:** 4:5 (rendered 3:4 / 880×1168, 1K low quality)  
**Run type:** SCENE (copy zone reserved, no in-image text)  
**Model:** gpt_image_2  
**Job ID:** f4f7b347-a309-462a-bbf4-19d5b1e80507  
**Output:** output.png  
**Refs passed:** none (no packshot or Element for this SKU)

---

## PROMPT USED

Photorealistic 4K lifestyle advertising image of an unlacquered solid-brass bridge kitchen faucet with cross-handle levers, installed on a white fireclay apron-front farmhouse sink set into a honed Calacatta marble countertop; raw brass showing warm natural depth and tonal variation.

Product and visual interest composed to the right side of the frame; the left 45% of the frame is a single large empty plane of bare limewash plaster wall — clean and unbroken — reserved for ad copy.

Kitchen environment: limewash plaster walls in warm greige; one recessed walnut open shelf in the upper background holding a few sage-glazed ceramic vessels; honed marble counter with a thin waterfall edge; aged wood ceiling beam differentiating the ceiling from the walls; room plausibly scaled, no clutter.

Golden-hour warm directional light rakes in from a small window, casting soft window-pane shadow geometry across the marble counter. The brass faucet is the hero-lit focal point — catching the warm low sun in a concentrated highlight, the brightest and most luminous element in frame; natural light falloff dims the background.

Shot on full-frame camera, 50mm lens, f/2.8, shallow depth of field softening the background shelving into warm bokeh. Visible film grain, natural chromatic texture, real-photo weight.

Warm neutral limewash plaster shell dominates the frame (~70%); exactly one sage/olive accent on ceramic vessels on the walnut shelf; brass and walnut details throughout.

Style: high-end home-decor editorial, lived-in and curated, Kinfolk-adjacent. Real photo texture: visible material grain, natural light falloff, slight vignette. 4:5.

No distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents.

---

## BRAND_ESSENTIALS CHECK (composer pre-flight)

- [x] neutral shell ~70% dominant (limewash plaster)
- [x] exactly ONE accent green-first (sage/olive ceramic vessels on walnut shelf)
- [~] fixture ON + glowing as focal point — brass hero-lit by directional sun; faucet dry (no water flow)
- [x] brass/walnut present
- [x] wall surface broken up (walnut open shelf)
- [x] golden-hour warm directional light

**Note:** "Fixture ON" was interpreted as brass hero-lit, not water-flowing. Judge disagreed — see below.

---

## CLAUDE SELF-CRITIQUE (visual inspection)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Photorealism | 4.5 | Window-pane shadows on marble counter superb; plaster grain reads real; minor AI softness in shelf detail |
| Product fidelity | n/a | No packshot ref provided; bridge faucet form and brass finish are accurate to brief |
| Brand fit | 4.5 | All brand essentials present visually; sage accent subtle but correct |
| Lighting & composition | 4.5 | Directional warm raking light excellent; left 45% plaster copy zone clean and unbroken |
| Ad usability | 4.0 | Copy zone excellent; lower res (1K) limits print use; crop is tight/usable |

**Self-critique total: ~4.4**  
Biggest WIN: The window-pane shadow cast across the marble counter is editorial gold — very real, very RS.  
Biggest issue: Faucet is not running water — "fixture OFF" by strict brand-card reading.  
Next fix: Add water flowing from spout OR frame this as "unlacquered brass hero-lit" with explicit water-on instruction.

---

## QC GATE-1 — JUDGE B (Gemini 3.1 Pro via OpenRouter)

**Judge JSON:** judge.json  
**Model:** google/gemini-3.1-pro-preview

| Dimension | Score |
|-----------|-------|
| Photorealism | 4.5 |
| Product fidelity | 3 ← HARD FAIL (no packshot ref; <4 veto) |
| Brand fit | 2 |
| Lighting & composition | 4.5 |
| Ad usability | 2 |
| **Total** | **3.2** |

**Hard fails:** `banned-list hit: fixture OFF in hero shot`  
**Verdict:** FAIL  
**Judge's biggest issue:** Faucet is off; no water flowing — violates "fixture ON" rule.  
**Judge's fix:** image2image + render water flowing from faucet spout.

---

## VERDICT: FAIL

**Reason 1 (hard fail):** product_fidelity = 3 < 4 threshold. No packshot ref was used; judge cannot confirm fidelity. This is a structural limitation — no RS brass-faucet Element exists yet.  
**Reason 2 (hard fail):** `fixture OFF` banned-list hit. The "fixture ON, glowing" rule was written for lighting products; applied literally to a faucet it means water flowing. Composer adapted to "hero-lit brass" — judge does not accept this interpretation.

**Does NOT proceed to Figma or human gate.**  
**Iteration count:** 0 used (single shot as requested).

---

## ROOT CAUSE + NEXT RUN GUIDANCE

1. **No Element for this SKU.** Register the brass bridge faucet as a Higgsfield Element (or provide a packshot ref) before re-running. This alone unlocks product_fidelity ≥4.
2. **"Fixture ON" for non-lighting products.** For hardware (faucets, knobs), composer must add explicit `water flowing from spout` or `faucet running` to satisfy the "ON" rule. Add to PROMPT_COMPOSER plumbing notes.
3. **Resolution.** gpt_image_2 defaulted to 1K/low. Set quality: high or request upscale for ad-ready output.

**Approach status:** NOT killed (single attempt, first run on this archetype). Retry with packshot ref + water-running clause.

---

## VERIFICATION STATUS: N/A (run failed — not shipped)
