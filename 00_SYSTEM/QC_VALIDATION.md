# QC_VALIDATION — multi-agent judge panel (v1.3)

## Why a panel
v1.2's self-critique had a structural flaw: the composer (Claude) graded its
own homework. Same-model judging inherits the same blind spots that produced
the image. Fix: independent judges from a DIFFERENT model family. Research-
backed: diverse judge panels beat any single judge and cancel intra-model bias.

## The panel
| Judge | Model | Role | Cost |
|-------|-------|------|------|
| A | Claude vision (in-loop) | self-critique during iteration (≤3 fixes) | free in-session |
| B | Gemini 3.1 Pro — `google/gemini-3.1-pro-preview` via OpenRouter | independent QC verdict (scripts/qc_judge.py) | ~$0.01–0.03/image |
| C (tiebreak only) | `google/gemini-3.5-flash` | fired only when A and B disagree >1.5 on any dimension | ~$0.002/image |

Judge ≠ composer. Judge B never sees Claude's scores before scoring (no
anchoring). Temperature 0, forced JSON, same rubric for everyone.

## What each judge receives
1. The generated image
2. The product packshot / Element ref (fidelity is checked AGAINST it, not from memory)
3. The brand's BRAND_ESSENTIALS checklist (verbatim from the brand card)
4. The REVIEW_RUBRIC dimensions + output schema
Never: the prompt's intent narrative, the other judge's scores, prior run history.

## Fusion rules (how verdicts combine)
- **HARD criteria = VETO.** Product fidelity < 4 OR any brand banned-list hit
  from ANY judge → run FAILS. No averaging can rescue a warped logo.
- **SOFT criteria = mean** across judges per dimension.
- **Disagreement > 1.5** on any dimension → Judge C tiebreaks that dimension;
  if still split, the run is flagged HUMAN-REVIEW, never silently averaged.
  Disagreement is information — log it.
- **PASS = no vetoes AND fused total ≥ 4.5.** Only PASS runs reach Figma.

## Signal discipline (unchanged, critical)
ALL judge feedback caps at MEDIUM signal. A judge can fail a run and suggest
the fix; only a HUMAN approval/comment reaches HIGH and trains structure.
This is what stops judge noise from rewriting proven templates.

## Judge calibration (the judges get trained too)
Every Figma human verdict is compared to the panel's verdict for that run →
`judge_agreement` in METRICS.md. If Judge B disagrees with humans ≥30% over
20+ runs: fix the judge PROMPT (rubric wording, examples), never loosen the
gate. A judge that passes what humans reject is worse than no judge.

## Failure handling
- Judge API error after 3 retries → run holds at `generated`, never auto-passes.
- A FAIL verdict includes `biggest_issue` + `fix` (one composer field) →
  feeds the next self-critique iteration. Same one-fix-per-cycle rule (R6).
- Total < 2.5 from the panel twice on the same approach → KILL (R8), log it.

## STAGE 2 — LAYOUT QC (after layout composition, before human review)
Run by the layout agent on a screenshot of the COMPOSED frame (image + text).
Named hard checks — each alone fails the layout (these are the two historical
complaints plus their cousins):
  TEXT_TOO_SMALL   H1 must fill its copy region (~17% of region width, type-
                   scale clamped). The #1 board complaint. FAIL → resize.
  WRONG_LOGO       Must be the real asset file from ASSETS/brand/, correct
                   variant for the archetype, correct position. Text stubs,
                   redrawn marks, wrong variant = FAIL.
  OVERLAP          Text/logo over product, faces, or clutter = FAIL.
  CTA_VIOLATION    Pill on a non-promo ad (RS) / urgency CTA (CACHE) = FAIL.
  ILLEGIBLE        Insufficient contrast on the actual region = FAIL.
≤2 fix cycles per layout, then HUMAN-REVIEW. A layout pass does NOT reopen the
image verdict — stage 1 and stage 2 are independent gates.
