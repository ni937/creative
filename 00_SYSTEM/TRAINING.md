# TRAINING — how this system actually learns (no fine-tuning required)

"Training" = three compounding layers. Run all three and the system measurably
improves; skip them and it's just a prompt folder.

TWO ISOLATED SOURCES (00_SYSTEM/PROVENANCE.md): all learning is tagged by origin —
`SRC: figma` (real approved ads = ground truth) vs `SRC: higgsfield` (our own
generations + QC = hypotheses). The streams are kept in separate files and merged
ONLY at retrieval, so a Higgsfield-side regression can never silently corrupt the
Figma-grounded behavior, and either source can be rolled back without touching the
other. On conflict: figma > higgsfield.

## T1 — ELEMENTS (consistency training)
Register every recurring asset as a Higgsfield Element:
- Each RS product (packshot → Element) · each ARK fleet car / lounge space ·
  each Cache garment · each FRST persona face.
Reference via <<<element_id>>> in prompts. This is what locks identity/product
across hundreds of generations — the single highest-leverage "training" act.
Maintain the registry: 04_KNOWLEDGE/ELEMENTS_REGISTRY.md (id, asset, brand,
date registered, packshot path).

## T2 — CORPUS (per-brand prompt training)
WINNING.md per brand = the trained weights, in markdown. Entry format:
  [W-###] scene archetype | product type | full winning prompt | score |
  run-id | what made it win (1 line) | date
Composers RETRIEVE top-3 matching winners before composing — every new prompt
starts from proven DNA, not from zero. Promotion gate: rubric 5.0 + fidelity 5
+ verification CONFIRMED + no contradiction with existing entries.

## T3 — DISTILL (cross-brand pattern training)
Durable lessons → 04_KNOWLEDGE/PATTERNS.md (engine quirks, composition physics,
lighting rules that hold across brands). Brand-specific lessons stay in the
brand folder. HUMAN CORRECTIONS OUTRANK AI CONVERGENCE — precedent: RS's
aesthetic model converged wrong over 4 AI passes and was fixed by one human
note ("neutral shell dominates, ONE accent, fixture ON"). When a human
correction lands, it supersedes immediately and the old rule is marked
SUPERSEDED, never deleted (history teaches).

## Training cadence (weekly, ~20 min)
1. Sweep the week's runs: promote qualifying winners (T2)
2. Resolve PENDING verifications (close the loop)
2b. Harvest the week.s approved Figma frames into REFS/ (FIGMA.md H1)
3. Register new Elements for any recurring asset used 2+ times (T1)
4. One PATTERNS.md pass: anything proven across 2+ brands? (T3)
5. Append METRICS.md row. Check loop_closure_rate ≥ 0.6.
