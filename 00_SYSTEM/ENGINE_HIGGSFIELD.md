# ENGINE — Higgsfield (the engine; this vault is the brain)

DECISION (inherited from ads-gen, proven 2026-06-05): don't rebuild Higgsfield's
toolchain. Claude composes the prompt from .md; Higgsfield renders.

## ACCESS ROUTE (v1.3.1 — matches Nick's installed setup)
PRIMARY: official Higgsfield CLI + agent skills (installed via
`npm i -g @higgsfield/cli` + `npx skills add higgsfield-ai/skills`).
Skills handle auth/uploads/polling natively — this replaces ads-gen's hf_gen.py.
Skill → system mapping:
  - higgsfield-product-photoshoot → RS product runs (packshot-conditioned scenes)
  - higgsfield-generate           → ARK / CACHE / general stills + video
  - higgsfield-soul-id            → the Elements/consistency layer (TRAINING T1):
                                    register recurring faces/products as Soul IDs
  - higgsfield-marketplace-cards  → not used; ignore unless a card-layout need appears
SECONDARY: Higgsfield MCP (if connected) — same engine, interchangeable.
Invocation in Claude Code: plain language — "generate with higgsfield:
<composed prompt> with ref <packshot>" — the skill routes it.

## Model map (our intent → Higgsfield job type)
DEFAULT MODEL — HARD RULE (Nick, 2026-06-13): every image still defaults to
**nano_banana_2 (Nano Banana Pro) at 2K**. The composer/producer MUST pass
`model=nano_banana_2` explicitly on every generation — do NOT let the engine fall
back to `gpt_image_2` or `nano_banana_flash` (both read as AI/fake and were the
wrong default that shipped the first batch). `gpt_image_2` is allowed ONLY for a
fast throwaway draft when explicitly requested; `nano_banana_flash` is never used
for finals.
- stills / hero / exact aspect → nano_banana_2 (Nano Banana Pro core — same
  model family the FRST persona prompts target)  [DEFAULT — all brands]
- edit / inpaint / relight / change-angle → flux_kontext (edit vocab, not full regen)
- cutout → image_background_remover
- reframe aspect → reframe · upscale → topaz
- video → kling3_0 (Kling 3.0 — kling-prompt-engineering skill applies) / veo3 / seedance_2_0
- consistency → Soul V2 + ELEMENTS (see TRAINING.md)

## Operating rules
1. PRODUCT RUNS: always condition — registered Element (<<<element_id>>>) or
   packshot ref — plus the preservation clause from the brand composer. Never
   synthesize a real SKU from text.
2. EDITS BEAT REGENS: a lighting/angle/crop fix = flux_kontext edit on the
   passing image, not a fresh roll. Cheaper, preserves what already passed QC.
3. COST PREFLIGHT on batches: check credits before multi-image runs; log
   credit spend per run in RUN.md (feeds CAC awareness later).
4. OUTPUT CONTRACT: every generation lands in 02_RUNS/<run-id>/ with RUN.md
   (prompt used, refs/elements, model, settings, status). No orphan images.
5. STATUS FLOW per run: queued → generated → self-passed → qc-passed →
   in-review → approved | changes-requested → final.

## Fidelity tiers (rule of thumb)
- volume/scene → Element or packshot ref in scene mode
- fidelity-sensitive → two-pass: empty background first, then ref-anchored insert
- hero / high-AOV → background mode + composite the REAL packshot (zero
  generative drift on the product). Generative pixels are for the scene. (R7)
