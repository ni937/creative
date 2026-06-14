# RUN: RS_20260613_p4

## Brief
Product: Antique-brass picture light mounted above gilt-framed oil painting, switched ON.
Brand: RS | Placement: wall-mounted art accent | Format: 4:5 (ad scene)
Intent: lifestyle SCENE with ~45% left-side copy plane reserved for ad copy.

## Composed Prompt (12-field RS PROMPT_COMPOSER)
**TASK** Photorealistic 4K lifestyle advertising image of  
**SUBJECT** antique-brass picture light mounted above a large gilt-framed oil painting, switched ON, casting a warm amber wash across the canvas and surrounding plaster wall  
**PLACEMENT** wall-mounted art accent in a moody study interior; picture light directly above the painting; macro framing, fixture and painting filling the right two-thirds of frame  
**ENVIRONMENT** intimate study; smooth warm plaster walls; wainscot paneling below dado rail breaks up wall surface; wood-beam ceiling differentiated from walls; edge of antique walnut bookcase partially visible; one olive-velvet armchair as single color accent  
**COMPOSITION** product and painting to the right two-thirds; opposite ~45% of frame a single large empty plane (soft warm plaster in bokeh) reserved for ad copy; macro framing, slight three-quarter angle  
**LIGHTING** 🔒 Golden-hour warm directional light through sheer curtains casting soft window-pane shadows; the fixture is switched ON, glowing warm — the brightest point in frame  
**CAMERA** full-frame, 50mm, f/2.8; shallow depth of field; visible photographic grain; natural light falloff  
**STYLE** high-end home-decor editorial, lived-in and curated; real photographic texture throughout (plaster grain, brass patina, oil-painting impasto, fabric weave)  
**MOOD/COLOR** 🔒 Warm neutral plaster shell dominates the frame; exactly one olive accent on the velvet armchair upholstery; brass and walnut details  
**OUTPUT** 4:5, 2K  
**EXCLUSIONS** 🔒 no distorted logos, no warped labels, no extra text, no watermark, no extra products, no clutter, no people, no warped perspective, no CGI/3D-render look, no illustration, no flat beige scene, no competing color accents  
**TEXT** none

## Generation
- Model: gpt_image_2 (aspect_ratio adjusted to 3:4, resolution 1k)
- Job ID: 7ae6e6e1-63aa-42c2-890c-ae3feb136faf
- Output URL: https://d8j0ntlcm91z4.cloudfront.net/user_351PcLsaCFYLgx02Flw3rHfIWkq/hf_20260614_013512_7ae6e6e1-63aa-42c2-890c-ae3feb136faf.png
- output.png: saved locally (2.2 MB)

## Visual Assessment (self-critique)
- Fixture ON and glowing warm amber: ✅ — brightest point in frame, glow pools on canvas and wall
- Antique-brass picture light: ✅ — clearly visible above painting, patina present
- Gilt-framed oil painting: ✅ — landscape canvas with heavy gilt frame
- Neutral plaster shell dominates: ✅ — ~70% warm plaster, moody and recessive
- ONE accent (olive): ✅ — olive-sage velvet armchair, bottom-left, no competing accent
- Brass + walnut: ✅ — brass fixture, bookcase spine at left edge
- Wall broken up: ✅ — wainscot paneling below dado rail clearly visible
- Golden-hour directional light: ✅ — window shadows cast across wall
- Copy plane ~45% left: ✅ — large soft-bokeh plaster empty plane on left
- No CGI look: ✅ — photorealistic grain, natural light falloff
- No people / no text / no clutter: ✅

BRAND_ESSENTIALS compliance: 6/6 ✅

## QC Gate-1 (OpenRouter Gemini judge)
```json
{
  "photorealism": 5,
  "product_fidelity": 3,
  "brand_fit": 5,
  "lighting_composition": 5,
  "ad_usability": 5,
  "hard_fails": [],
  "biggest_issue": "A product (picture light) is featured but no packshot was provided for verification, capping product fidelity at 3.",
  "fix": "Provide a reference packshot of the picture light to allow for full product fidelity scoring.",
  "verdict": "FAIL",
  "total": 4.6,
  "model": "google/gemini-3.1-pro-preview"
}
```

**Verdict interpretation:** FAIL is packshot-absent only. No hard_fails. No visual defects. All other scores are 5/5. Product fidelity capped at 3 by policy because no packshot reference was supplied — this is a SCENE job for a generic product archetype (no registered Element or packshot exists for this SKU). Mean excluding fidelity cap = 5.0. If a packshot is supplied on a future run, this pass/fail boundary will shift.

## Status
- verification_status: PENDING (no follow-up gen yet)
- Eligible for Figma human gate: YES (no hard fails, strong visual quality)
- Eligible for WINNING promotion: NO (product_fidelity < 4, no packshot to verify against)
