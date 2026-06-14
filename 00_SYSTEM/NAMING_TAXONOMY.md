# NAMING TAXONOMY — frame names ARE training labels

Every harvested frame name gets parsed into structured tags. Tags drive REFS
foldering, LAYOUT_PAIRS image features, and retrieval. Names are labels, not
decoration.

## THE TAG SCHEMA (what every image resolves to)
  product      e.g. brass-dimmer-switch, fylux-wall-lamp, corium-chandelier
  variant      color/finish/spec: brass, matte-black, aged-bronze
  angle        macro | close-up | three-quarter | top-shot | eye-level | low
  shot_type    detail | vignette | half-room | establishing | lifestyle
  subject      none | girl | guy | hands | couple   (person present in frame)
  format       4x5 | 9x16 | 2x1 | 1x1
  extras       free tokens kept verbatim (room, mood, campaign code)

## PARSE RULES (delimiter-agnostic — handle their dialects)
1. Nick's scheme: tokens in name map directly — product first, then variant/
   color, then angle/shot descriptor, then subject if present.
   e.g. "Brass Dimmer - Aged Bronze - Macro Top Shot - Girl" →
   product=brass-dimmer variant=aged-bronze angle=top-shot shot_type=macro subject=girl
2. RS ads dialect (B22 boards): B22_C<concept>_V<n>_<Product>_Keith_<Designer>_
   <type>_<Modern|Heritage>_<tier>_<theme>_<Offer|Story|Review|Testimonial>_<aspect>
   → product, layout family, format archetype, designer, aspect all from name.
3. UNNAMED / GARBLED names: VISUALLY READ the image and fill the tags yourself —
   never skip tagging, never trust a bad name over your eyes. Log name_quality:
   PARSED | INFERRED so we know which labels are ground truth.
4. Conflicts (name says girl, image shows none): the IMAGE wins; note the mismatch.

## GENERATION-SIDE RULE (keep the boards consistent)
Every frame WE push to Figma is named in the same scheme:
  <Brand> | <product> | <variant> | <angle/shot> | <subject if any> | <run-id>
Our outputs train future harvests the same way theirs train us.
