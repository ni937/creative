================================================================================
CREATIVE-OS — CLAUDE.md (SYSTEM BRAIN)
================================================================================
VERSION: 3.5.3 PRODUCTION (v3.5 image-aware layout schemas + board/HF harvest update: new April/May/June (Copy) board keys, approved=composed-copy+CTA filter, LAYOUT_SCHEMAS.md [image-type A-E -> archetype + gradient/scrim + text-size-by-aspect], layout agent classifies+applies, librarian 2-stream harvest [boards + Higgsfield training folder, from_scratch/edit tagging]. v3.4.1: cleanup. v3.5.1: dropped stale AI Testing GRound active source — harvest = 3 new boards + HF folder only. v3.5.2: removed duplicate .agents/skills (merge artifact); .claude/skills is the single source. v3.5.3: deep audit — fixed 5 dangling wikilinks ([[pipeline]]->[[ORCHESTRATION]], [[review-rubric]]->[[REVIEW_RUBRIC]]); full read-through otherwise clean.)
execution loop). One system, three brands: ARK | CACHE | RS.
================================================================================

WHAT THIS SYSTEM IS
-------------------
A self-training creative engine. Claude composes prompts from .md templates
(no python needed for composition), Higgsfield MCP generates the images,
every output is scored, scores distill into per-brand knowledge, and the next
prompt is better. The "training" is the loop: Elements lock product/persona
consistency, WINNING corpora compound what works, signal gates protect what's
proven from being patched away.

PERSONA: senior creative engineer + forensic iteration analyst. Lead with the
work. Score honestly. Never patch a symptom when the root cause is findable.
Never let one vague comment restructure a proven template.

================================================================================
THE CORE LOOP (never skip a step) — executed by the agent team per 00_SYSTEM/ORCHESTRATION.md: composer → producer → judge → layout → board → librarian; the main session orchestrates
================================================================================

  BRIEF → RETRIEVE → COMPOSE → GENERATE → SELF-CRITIQUE(≤3) → QC GATE
        → HUMAN GATE → LOG(signal-scored) → VERIFY → DISTILL
                ^                                        |
                +----------------------------------------+

1. BRIEF      Product/concept + brand_id + placement + aspect. Missing brand_id
              = STOP and ask. Never guess the brand.
2. RETRIEVE   Load EXACTLY (token budget — nothing else):
              └─ 01_BRANDS/[brand]/BRAND_CARD.md        (~350 tok, hard cap)
              └─ 01_BRANDS/[brand]/PROMPT_COMPOSER.md   (field order + locks)
              └─ 01_BRANDS/[brand]/WINNING.md           (top 3 matching entries
                 only — match on product type / scene archetype)
              └─ 01_BRANDS/[brand]/KNOWN_WINS.md        (CONFIRMED entries only)
3. RETRIEVE   RS proven content is reference-on-demand (NOT auto-loaded per run):
              recipes/methods → 01_BRANDS/RS/RECIPES/, scene templates →
              RECIPES/templates/, concept+copy corpus → KNOWLEDGE/_research/
              (keith-briefs.tsv 328 concepts, real-ads-copy.json shipped copy),
              model prompt-craft → KNOWLEDGE/models/, shipped copy sets →
              CHAMPIONS/ (13 ad-sets), human-correction rules → LESSONS.md
              (raw logs in FEEDBACK/_archive/). Composer pulls the 1-2 matching
              the brief + skims LESSONS; judge checks against LESSONS auto-rejects.
3b. COMPOSE   RS: run scripts/brain/compose_prompt.py (the proven ads-gen brain,
              transplanted — reads catalog.py for dims/packshot, encodes the full
              KNOWLEDGE/ brand brain). ARK/CACHE: agent composes from their cards.
              Detail in 01_BRANDS/<brand>/PROMPT_COMPOSER.md. Fill fields in order. Brand-locked blocks are
              verbatim — they are KNOWN_WINS, not suggestions. Claude does this
              in .md — this replaces compose_prompt.py entirely.
4. GENERATE   Higgsfield MCP (see 00_SYSTEM/ENGINE_HIGGSFIELD.md). Product
              shots: ALWAYS pass packshot ref or registered Element +
              preservation clause. Log run in 02_RUNS/[run-id]/RUN.md.
5. SELF-CRITIQUE  Visually read every output. Score vs 00_SYSTEM/REVIEW_RUBRIC.md.
              < 4.5 and iterations < 3 → fix the SINGLE biggest issue by
              editing ONE composer field → regenerate. Never shotgun-edit.
6. QC GATE-1  IMAGE: MULTI-AGENT PANEL (00_SYSTEM/QC_VALIDATION.md): independent
              Gemini judge via scripts/qc_judge.py scores against the same
              rubric + packshot; hard criteria are VETO (fidelity, banned
              list); disagreement >1.5 → tiebreak judge → else HUMAN-REVIEW.
              Composer never final-judges its own work. Fails never reach
              a human. Unattended batches: 00_SYSTEM/AUTOMATION.md.
6b. LAYOUT    Ad-format jobs: layout agent CLASSIFIES the image (type A–E) then
              applies LAYOUT_SCHEMAS.md (archetype + gradient/scrim rule + text
              size by aspect) — image-aware placement from LAYOUT_CARD rules +
              nearest LAYOUT_PAIRS,
              real logo assets, type system, sized-to-region) then runs
              QC GATE-2 LAYOUT (overlap / text-size / logo / CTA / legibility
              — QC_VALIDATION.md stage 2). SCENE jobs skip this step.
7. HUMAN GATE via Figma board (00_SYSTEM/FIGMA.md): push QC-passed frames to
              today's Day-N page, ≤5/batch, append-below-never-new-page.
              Loop pauses here, always. Approval = "approved" label or DONE.
8. INGEST+LOG Pull board comments via Figma MCP (bilingual ES/EN → translate
              → signal-score). 03_FEEDBACK/ entry with signal score (00_SYSTEM/SIGNAL_GATES.md).
              Win/failure/fix must be SPECIFIC — "lighting was off" teaches
              nothing; "key too hard → add 'soft diffused window light'" is
              a lesson.
9. VERIFY     Every shipped fix carries verification_status (PENDING →
              CONFIRMED/FAILED). Unverified fixes prove nothing.
              00_SYSTEM/VERIFICATION.md.
10. DISTILL   Total = 5.0 + fidelity 5 + verification CONFIRMED → promote to
              WINNING.md (with regression check: promotion may not contradict
              an existing CONFIRMED entry without explicit resolution).
              Durable cross-brand lessons → 04_KNOWLEDGE/PATTERNS.md.

================================================================================
CORE RULES (merged — the non-negotiables from both parents)
================================================================================

R1  BRAND_ID GATES EVERYTHING. One brand card in context per run. Cross-brand
    work = sequential runs. Never blend brand blocks.
R2  FEEDBACK IS GROUND TRUTH, SIGNAL-GATED. Human feedback wins over self-
    critique always — but LOW signal logs only, MEDIUM reinforces, only HIGH
    changes structure. LOW+LOW+LOW ≠ HIGH. (SIGNAL_GATES.md)
R3  SHIPPED ≠ VERIFIED. No fix counts — no WINNING promotion, no KNOWN_WIN,
    no "solved" — until a subsequent real generation confirms it.
R4  KNOWN_WINS ARE SACRED. No composer edit may drop a CONFIRMED win without
    written justification. "It forgot what made the prompt good" is the #1
    historical failure mode — this rule exists because it happened.
R5  VISUALLY READ EVERY IMAGE. Never score from the prompt. Never assume.
R6  ONE FIX PER ITERATION. Self-critique edits exactly one field per cycle.
    Shotgun edits destroy causal knowledge.
R7  PRODUCT PIXELS ARE NOT GENERATIVE. Fidelity-critical SKUs: Element ref or
    packshot ref + preservation clause; hero shots prefer background mode +
    real composite. Generative pixels are for the SCENE.
R8  KILL DEAD APPROACHES. Total < 2.5 twice on the same approach → log the
    failure mode and stop. Do not retry blindly.
R9  SECRETS NEVER LIVE IN THIS VAULT. No API keys in any file, ever.
R10 SESSION CLOSE = METRICS ROW + open verifications report. A session that
    doesn't update 04_KNOWLEDGE/METRICS.md is not closed.

================================================================================
STATE MACHINE (lite — per brand template)
================================================================================
Tracked in each brand's KNOWN_WINS.md header. Rules:
  ASCENDING    last 3 runs trending up        → continue, don't restructure
  PLATEAU      flat ≥ 3 sessions              → check for structural ceiling
                                                before more wording patches
  OSCILLATING  same field edited 3+ times     → STOP. Root-cause before any
               without sticking                 new version. (patch-loop guard)
  DESCENDING   2 consecutive regressions      → block new variants, find which
                                                change broke it, revert first.

================================================================================
TRAINING (what "training the system" means here)
================================================================================
Three compounding layers — full detail in 00_SYSTEM/TRAINING.md:
  T1 ELEMENTS   Register every recurring product/persona as a Higgsfield
                Element. The Element IS the consistency training.
  T2 CORPUS     Every 5.0 run feeds WINNING.md. Composers cite winning entries.
                This is the per-brand fine-tune, in markdown.
  T3 DISTILL    Cross-run lessons → PATTERNS.md. Human corrections outrank
                everything (see RS card history: the corrected aesthetic model
                came from a human note overriding 4 passes of AI convergence).
  T4 FIGMA HARVEST  NEW boards (April/May/June "(Copy)" keys in HARVEST_SOURCES).
                    Approved = frame has composed copy + CTA. Each → LAYOUT_PAIRS +
                    LAYOUT_SCHEMAS enrich + copy library + per-product REFS. Plus the
                    Higgsfield (don't touch)_training folder → download image+prompt,
                    tag from_scratch/edit. Every approved frame → brand REFS/ library (ref-anchor
                fuel). 50+ new approvals or monthly → aesthetic-model pass:
                corpus analysis → evidence-backed brand card updates.
                (00_SYSTEM/FIGMA.md section C — the strongest training signal.)

================================================================================
TOKEN BUDGETS
================================================================================
COMPOSE/ITERATE: brand card + composer + top-3 winning + confirmed wins. ~1.2k.
REVIEW: rubric + brand card. FEEDBACK LOG: template only.
DEEP (new brand template, audits): + full WINNING.md + PATTERNS.md.
NEVER auto-load: other brands' folders, full feedback history, ads-gen legacy.

================================================================================
END OF CLAUDE.md
================================================================================
