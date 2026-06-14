# PROVENANCE — two isolated training streams, merged only at query

Reason this exists (Nick, 2026-06-13): the Figma-grounded training already works.
Higgsfield self-generated training is NEW. If the two mix, a regression introduced
by Higgsfield learning could silently corrupt the Figma-grounded behavior and we
would not be able to tell where the issue came from. So the streams are kept
**physically isolated and provenance-tagged**, and merged ONLY at retrieval —
never written into the same record.

## The two streams

### STREAM A — FIGMA  (ground truth: real, human-approved shipped ads)
Source: approved frames harvested from the Figma boards (FIGMA.md H1).
Trust: HIGH — a human approved and shipped these.
Files (FIGMA-owned — Higgsfield logic may NEVER write here):
  - 01_BRANDS/<brand>/LAYOUT_PAIRS.md   (image→layout pairs)
  - 01_BRANDS/<brand>/LAYOUT_CARD.md    (typography / placement grammar)
  - 01_BRANDS/<brand>/REFS/             (approved scene images)
Record tag:  `SRC: figma | <board> | <frame name> | <date>`

### STREAM B — HIGGSFIELD  (self-generated, QC-scored — hypotheses, not truth)
Source: our own generations — the (prompt → reference images → output → QC
verdict) tuple for every run.
Trust: PROVISIONAL — only as good as the QC that scored it.
Files (HIGGSFIELD-owned — Figma harvest may NEVER write here):
  - 01_BRANDS/<brand>/HIGGSFIELD_PAIRS.md   (prompt→output→QC, one per gen)
  - 02_RUNS/<run-id>/RUN.md                 (full run record + QC)
  - 04_KNOWLEDGE/HIGGSFIELD_LEARNINGS.md    (cross-gen distilled patterns)
Record tag:  `SRC: higgsfield | <run-id> | <model> | <qc verdict> | <date>`

## Isolation guarantees (hard rules)
1. A write tagged `SRC: higgsfield` NEVER modifies a Stream-A file, and vice versa.
2. The librarian is the only writer; it routes by source and refuses cross-writes.
3. Either stream can be quarantined or rolled back wholesale without touching the
   other — stop reading the HIGGSFIELD_* files and you are instantly back to the
   Figma-only baseline.

## Merge — only at retrieval
Composer / layout agents retrieve from BOTH streams, but every retrieved item
keeps its `SRC` tag, so the agent always knows whether a pattern came from a real
approved ad or from one of our own generations.

## Precedence on conflict (mirrors TRAINING.md T3)
  figma (real approved ad)  >  higgsfield (self-gen, QC-passed)  >  higgsfield (QC-failed → kept only as a negative example)

A Higgsfield learning may NOT contradict a CONFIRMED Figma pair without an explicit
human resolution. Higgsfield learnings are how the system EXPLORES; Figma pairs are
the ground it is not allowed to drift off of.

## Debuggability (the whole point)
If generation quality drops after a Higgsfield training pass: disable Stream B
(skip the HIGGSFIELD_* files + 02_RUNS retrieval). If quality returns to the
Figma-only baseline, the regression is isolated in Stream B — fix or quarantine it
there, having never touched the Figma knowledge that works.
