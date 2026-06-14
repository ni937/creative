# FIGMA — review round-trip + training harvest (Figma MCP)

Figma is BOTH the human gate AND a training data source. Conventions below are
ported from the proven ads-gen round-trip (validated 2026-06-05/06 on a live
board with 5,276 comments) — adapted to Figma MCP instead of python scripts.

## A. PUSH (human gate delivery) — QC-passed frames only
1. Board convention: reviewers work off **Day-N pages**. Append new batches as
   a labeled row/block BELOW the current content on TODAY's Day-N page.
   **NEVER create a new page per batch** — page sprawl is the #1 reviewer
   complaint. New Day pages only at day rollover, canvas background set to
   dark charcoal (#1E1E1E) so ads pop.
2. ≤5 frames per push. Frame name = `<Brand> | <Product/Concept> | <run-id>`
   — the name IS the label reviewers see.
3. Resize frames to true image aspect (4:5 → 432×540), image fill = FILL,
   laid out in a clean row. Sloppy boards get sloppy feedback.
4. Push only `qc-passed` runs. Humans never see QC failures (loop rule).

## B. INGEST (feedback collection) — per frame, via Figma MCP comments
- Approval = **"approved" label OR a "DONE" comment reply.** Anything else
  with content = feedback.
- Feedback is **bilingual (ES/EN)** — translate first, then signal-score per
  SIGNAL_GATES.md. Board comments default MEDIUM until they name a specific
  element + fix direction (then HIGH).
- Comments are pinned to node_ids; node_ids are stable when frames are moved,
  so comments follow relocations — safe to reorganize boards.
- Every ingested comment becomes a 03_FEEDBACK entry linked to its run-id.
  Fixes shipped from board feedback get verification_status: PENDING and are
  re-pushed to the SAME Day page block for confirmation (closes the loop in
  the reviewer's own view).

## C. TRAINING HARVEST (Figma as training data) — this is the new layer
The approved-frame corpus is ground truth. Two harvest mechanics:

H1 — REFS LIBRARY + LAYOUT GRAMMAR (immediate, per-approval):
  TWO extractions per approved frame, not one:
  (a) the scene image → REFS/<product>/ (ref-anchor fuel)
  (b) the LAYOUT read → logo variant + position, type roles present, copy
      placement archetype, CTA presence, aspect — tallied into the brand's
      LAYOUT_CARD archetype frequencies, AND written as a full image→layout
      PAIR in the brand's LAYOUT_PAIRS.md: image features (shot type, angle,
      product position, empty-plane location) → layout chosen (archetype, copy
      position, sizes, logo variant, CTA) + the one-line WHY. Pairs are the
      training data that teaches WHY a layout fits an image — the layout agent
      retrieves nearest pairs before composing. Frame names are parsed into the tag schema per 00_SYSTEM/NAMING_TAXONOMY.md (product/variant/angle/shot/subject) — tags drive REFS foldering and the IMAGE half of every pair. Unnamed frames get visually tagged, never skipped. Frame names often encode the system
      (e.g. RS: B22_C<concept>_V<n>_..._<Modern|Heritage>_<format>_<aspect>) —
      parse them. This is how ARK/CACHE layout cards get filled and how RS's
      stays current.
  REFS power the REF-ANCHOR method (packshot + approved frame as dual refs =
  highest proven fidelity, 5.0 on Fylux). An approval isn't just a ship signal
  — it's three training assets (scene ref + layout tally + pair). No approved
  frame goes unharvested.

H2 — AESTHETIC MODEL PASS (periodic, per-brand):
  Trigger: 50+ new approved frames OR monthly, whichever first.
  Method: pull the brand's approved corpus via Figma MCP → analyze pattern
  frequencies (palette dominance, accent color ranking, lighting setups,
  composition, fixture state, materials) → diff against the BRAND_CARD rules
  → propose card updates with frame-count evidence.
  Precedent: RS's "one rule" came exactly this way — a 549-frame corpus
  analysis corrected 4 passes of AI convergence. This is the highest-quality
  training signal the system has.
  RULE: aesthetic-model updates to a brand card are HIGH signal but still
  carry verification — the updated rule is HYPOTHESIZED until the next 3
  approved runs under it, then CONFIRMED.

## D. WHAT NEVER HAPPENS
- No pushing to boards outside the agreed review file/pages.
- No resolving or deleting reviewer comments — ingest only.
- No treating an unanswered frame as approved. Silence = pending, not yes.
- No new review pages per batch (worth repeating — it's the #1 complaint).
