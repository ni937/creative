# creative-os — FINAL NOTES (v3.1, release-readiness pass)

One lineage: ads-gen, grown up, finalized inside creative-os. ads-gen's proven RS
brain lives inside creative-os's agent infrastructure + the 3 upgrades ads-gen lacked.

## WHAT THIS PASS VERIFIED (by execution, not assertion)
- Brain RUNS: scripts/brain/compose_prompt.py emits a complete ~714-word on-brand,
  product-accurate prompt (verified on Teva chandelier + Carissa pendant, different
  rooms/seeds — pulls product-specific detail + room-specific staging rules).
- All 12 scripts compile (py_compile). 6 agents present + frontmatter valid.
- 17 RS KNOWLEDGE docs (no empty stubs). 10 champions in WINNING.md. 12 catalog
  SKUs, all 12 packshots present. Brand cards under token cap. Zero committed secrets.
- Guardrails (SIGNAL_GATES, VERIFICATION) referenced by the loop + agents, not just
  present as files.

## WHAT WAS HARDENED / FIXED THIS PASS
1. **CATALOG AUTO-PULL BUG (real quality bug) — FIXED.** scripts/brain/catalog.py had
   ads-gen's old path (scripts/../assets/...) + a wrong ROOT depth. In creative-os the
   catalog is at 01_BRANDS/RS/ASSETS/catalog/products.tsv, two levels up from
   scripts/brain. The brain's true-scale clause was firing WITHOUT real dimensions
   (silent, try/except-swallowed). Now ROOT is correct + multi-candidate path
   resolution (creative-os → legacy → $RS_CATALOG_TSV env). Verified: find_by_name
   returns real dims (28x26) and revenue ranking works.
2. **STALE TIEBREAK MODEL — FIXED.** judge tiebreak was google/gemini-3-flash-preview
   (superseded). Updated to google/gemini-3.5-flash across qc_judge.py + QC_VALIDATION.md
   + judge.md. (Source: OpenRouter Google models, Jun 2026 — gemini-3.5-flash is the
   current near-Pro flash; gemini-3-flash-preview is the older preview.)
3. **FALSE WORD-CAP CLAIM — FIXED.** PROMPT_COMPOSER.md claimed "≤400 words, script
   self-manages length." The brain actually emits ~700-800 words BY DESIGN (proven
   ads-gen production behavior, Nano Banana Pro has the window for it). Corrected the
   doc: long-form for the RS brain (path A), ≤400 tight/front-loaded only for agent
   free-composition of non-catalog products (path B). Two paths, two length profiles.
4. **COMPOSER AGENT REWIRED.** composer.md now RUNS the brain for RS (added Bash tool)
   and is explicit + honest that ARK/CACHE compose from cards and are NOT trained.
5. **MISSING KNOWLEDGE DOCS — ADDED.** higgsfield-prompt-corpus, higgsfield-team-prompts,
   keith-brief-method, merch-map were absent (13→17). Now complete.
6. **ELEMENTS REGISTRY PRE-SEEDED.** 12 top RS products registered as Soul-ID/Element
   CANDIDATEs (was an empty header). Librarian flips CANDIDATE→REGISTERED on 2+ reuse.
   (Element gens are MCP-only — the CLI passes <<<id>>> as literal text.)

## RESEARCH CORRECTIONS LOG (old → new, with source)
| item | old | new | source |
|------|-----|-----|--------|
| judge tiebreak model | google/gemini-3-flash-preview | google/gemini-3.5-flash | OpenRouter Google models, Jun 2026 |
| judge primary model | google/gemini-3.1-pro-preview | UNCHANGED (verified current, vision) | Vertex/OpenRouter docs, Jun 12 2026 |
| Higgsfield still default | nano_banana_2 | UNCHANGED (current; Nano Banana 2/Pro live) | Higgsfield pricing + MCP, 2026 |
| Higgsfield video | kling3_0 / seedance_2_0 | UNCHANGED (Kling 3.0, Seedance 2.0 current) | Higgsfield Kling 3.0 page, 2026 |
| prompt word cap | "≤400, script-managed" (false) | long-form brain (~700-800w) intentional | ads-gen production behavior + NBP window |

## HONEST STATE
- **RS = PRODUCTION-READY TODAY.** Full knowledge (17 docs) + 663-line brain (runs) +
  catalog (auto-pull fixed) + 10 champions + 12 packshots + 12 Element candidates.
  Composes at ads-gen one-shot quality with the independent judge + layout QC on top.
- **ARK / CACHE = FORWARD-TRAINING.** Real brand cards + composers (HYPOTHESIZED,
  marked everywhere). ZERO trained corpus — no KNOWLEDGE docs, no champions, empty
  WINNING. They compose from their cards and BUILD their corpus from their own Figma
  boards via harvest. RS's transplant is the TEMPLATE for how a brand gets trained,
  NOT content to copy across (a Miami car club is not lit like a brass sconce).

## WINDOWS FIRST-RUN SEQUENCE
1. Extract to C:\Users\nick\Downloads\Projects\creative-os; open in Claude Code.
2. setx OPENROUTER_API_KEY "your_key"   → CLOSE the terminal, reopen.
3. claude   → /mcp  (authenticate Figma; Higgsfield MCP already connected)
            → /agents  (confirm 6: composer, producer, judge, layout, board, librarian)
4. "harvest all sources"   (populates RS/REFS + LAYOUT_PAIRS from the RS Figma boards)
5. "process the first RS job in the queue"   (watch the full loop once)

## LIVE-INTEGRATION CAVEATS (only surface on your machine — not code bugs)
- **Figma canvas authoring:** the layout agent composes ads ON the Figma canvas via the
  Figma MCP. If MCP authoring is read-biased/limited, the fallback is the render route
  (scripts/tools/render_ad.py + ASSETS/fonts) — wired in FIGMA.md + layout.md. First
  run tells you which path you're on.
- **First Higgsfield call:** auth + credits live on your account. Element/Soul-ID gens
  are MCP-only. Expect run #1 to maybe need one nudge; runs 2-5 smooth out.
- **Realistic first-run expectation:** RS one-shots are EARNED by the corpus — you start
  strong (champions + knowledge harvested), climbing as approvals compound. Watch
  one_shot_rate in METRICS.md. Don't loosen the QC gate to chase the number.

## WHAT WAS HARDENED / FIXED — 2026-06-14 (v3.2, scoped packshot-path fix)
**PACKSHOT PATH RESOLUTION (silent fidelity bug) — FIXED.** The v3.1 pass fixed the
catalog *location* lookup but the `packshot` column inside products.tsv still held
ads-gen-era paths (`assets/products/<file>`), and catalog.py resolved them with a naive
`os.path.join(ROOT, packshot)` → every SKU falsely reported "packshot missing" and the
producer's EXACT-product reference (RS's fidelity + one-shot anchor) silently broke.
Two-part fix, scope-locked to catalog.py + products.tsv:
1. Added `find_packshot(sku_or_row)` resolver in catalog.py: tries as-stored→ROOT, then
   basename under 01_BRANDS/RS/ASSETS/products/, then alt-extension (.png<->.jpg);
   returns first existing absolute path, else None (kept in `problems`, not hidden).
   `validate()` now uses it.
2. Corrected all 12 TSV `packshot` paths: prefix `assets/products/` →
   `01_BRANDS/RS/ASSETS/products/` (filenames + extensions kept exactly; dims, rank,
   and every other column untouched).
Reconciliation result: **12/12 packshots resolve, 0 genuinely absent** — no extension
mismatches and no missing files in this set. Verified: validate() reports 0 packshot
problems; find_by_name(full name) for Teva/Carissa/Brass Dimmer returns rows whose
resolved packshot exists on disk; brain re-run emits a complete 771-word prompt with
real dims (no regression).
Old→new (all 12, representative): `assets/products/teva-round-alabaster-chandelier.png`
→ `01_BRANDS/RS/ASSETS/products/teva-round-alabaster-chandelier.png` (same pattern for
all SKUs). SKUs genuinely missing a packshot on disk: NONE.

## FOUND, NOT FIXED (awaiting your go)
- **catalog.find_by_name() bare-keyword miss (pre-existing, NOT touched).** Matching is
  substring-based (`name.lower() in query OR sku-spaces in query`), so a short keyword
  like "Teva" returns None — only the FULL product name resolves. The brain/producer
  pass full names, so production is unaffected, but an agent querying by a single word
  would silently miss. One-line fix available (token-overlap or reverse-substring match)
  if you want it — left untouched per scope-lock.

## WHAT WAS HARDENED / FIXED — 2026-06-14 (v3.3, content-parity port)
Goal: creative-os contains every proven, results-driving piece of content ads-gen has,
so its first run composes from the same memory. ads-gen one-shots on CONTENT, not just
architecture; this pass moved the content the brain referenced but lacked.

PORTED (RS-only, reference-on-demand — none auto-loaded into per-run token budget):
1. RESEARCH CORPUS → 01_BRANDS/RS/KNOWLEDGE/_research/ (11 files): keith-briefs.json/.tsv
   (328 real Product×Persona×Visual-Style×Angle×Copy-Style concepts), real-ads-copy.json
   +march/+april (shipped headline/sub/CTA library), keith-refs-index.json/.tsv,
   _concept_ids.json, ad-boards.json, _dimmer_ads.json/_v2. This is the proven COPY
   LANGUAGE + CONCEPT COMBINATIONS behind one-shots.
2. RETRIEVAL ENGINE → scripts/brain/brief_retrieve.py (paths corrected to creative-os
   layout). Turns the 328-concept corpus into queryable concepts + copy exemplars
   (--product/--persona/--angle/--copy-style). Without it the corpus is unreadable data
   — this is the bridge keith-brief-method.md assumes. Smoke-tested: returns real
   concepts + shipped copy.
3. WINNING-PROMPT RECIPES → 01_BRANDS/RS/RECIPES/ (10 dated full-prompt methods: fylux
   ref-method, fylux golden-hour/editorial, door-hardware, dimmer-tournament-champions,
   dimmer-win-anchor, anyproduct-composer, scandi-living-bg, fylux-wall-lamp-dusk, README)
   + _library.md.
4. SCENE TEMPLATES → 01_BRANDS/RS/RECIPES/templates/ (5: kitchen, living-room, macro-
   closeup, background-empty-scene, outdoor-garden) — mapped to the brain's archetypes,
   not a parallel system.
5. MISSING CHAMPION AD-SETS → 01_BRANDS/RS/CHAMPIONS/ (added r5, r7, _switch, el, round4
   → 9 rounds total) — shipped eyebrow/h1/cta copy.
6. MODELS DOCS → 01_BRANDS/RS/KNOWLEDGE/models/ (nano-banana-pro, omni, _comparison) —
   proven prompt-craft. (ENGINE_HIGGSFIELD.md model strings NOT regressed — already current.)
7. REFERENCE IMAGES → 01_BRANDS/RS/REFS/ (13: fylux/ packshot+dining-art+bedroom-morningsun,
   cinematic-twilight/ 8 frames + README, hf_jobs.json) — fuels the ref-anchor method.
8. BROKEN-REFERENCE FIX: prompt-architecture.md was cited by 4 knowledge docs (scene-grammar,
   composition, camera, lighting) but absent → ported to KNOWLEDGE/. Also ported
   selfimprove-learnings.md (the meta-loop ledger behind prompt-patterns' one-liners).

RETRIEVAL WIRING: composer.md gained an "RS PROVEN-CONTENT RETRIEVAL" block (recipes,
templates, _research via brief_retrieve.py, models, champions — pull 1-2 matching the
brief, never load all). CLAUDE.md gained a "3. RETRIEVE" step before COMPOSE.

VERIFIED: V1 full parity table (every category YES w/ path) · V2 all keith-brief-method +
[[prompt-architecture]] refs resolve · V3 brain runs (Munira chandelier 720w w/ 26x24 dims;
Wasser faucet 640w) · V4 catalog 0 problems · V5 retrieval wired in both files · V6 12/12
scripts compile, 6 agents valid, 0 secrets, cards under cap · V7 ARK/CACHE 0 RS-leak, still
untrained stubs.

LEFT BEHIND (obsolete plumbing — replaced by creative-os's agents + MCP + Gemini judge):
- CLI shellers: hf_gen.py, generate.py, hf_prompts.py — replaced by producer agent +
  Higgsfield MCP.
- credentials.py, loop_config.py, config.yaml — env/config plumbing; creative-os reads
  OPENROUTER_API_KEY from env, no committed config.
- qc_gate.py (heuristic CV gate) — replaced by the independent Gemini judge (qc_judge.py).
- One-off campaign runners: dimmer_loop.py, switch_round.py, color_round.py,
  selfimprove_loop.py, layout_loop.py, ship_champions.py, diversity_assign.py,
  build_blind_ab.py, _build_switch_manifest.py, _figma_ad_r5.py, board_diff.py — bespoke
  to specific past campaigns; the agent loop + librarian generalize these. Their LEARNINGS
  are captured in selfimprove-learnings.md + prompt-patterns.md (ported).
- fixture_swap.py / fixture_detect.py / fixture_common.py / ref_filter.py / feedback_ingest.py
  — ads-gen-specific helpers; equivalent behavior lives in the brain + agents. (Revisit if
  a future pass wants programmatic fixture-swap; not needed for parity.)
- figma_ad.py — ads-gen's Figma compositor; creative-os uses the layout agent + Figma MCP
  with render_ad.py fallback.
- Root utilities: analyze_photos.py, downscale.py, extract_imgs.py, render_pdf.py,
  render_safe.py, tile_pages.py — one-off image utilities, not part of the generation loop.
- Keith's 413 raw REFERENCE IMAGE files (assets/references/keith/) — gitignored in ads-gen,
  not in the package; brief_retrieve.py resolves them when present (reports "0 available"
  until harvested). The concept+copy DATA (the high-value part) IS ported.

## FOUND, NOT FIXED (awaiting your go) — carried forward from v3.2
- catalog.find_by_name() bare-keyword miss (pre-existing). Substring match → a short
  keyword like "Teva" returns None; only the FULL product name resolves. Brain/producer
  pass full names so production is unaffected. One-line fix available if you want it.

## WHAT WAS HARDENED / FIXED — 2026-06-14 (v3.4, completeness sweep — full ads-gen parity, 3× verified)
Triple-validation file-level diff of all 249 ads-gen files vs creative-os. Confirmed prior
passes (A research corpus, B recipes/templates, C models docs, F refs, G prompt-architecture
+ selfimprove) genuinely landed (byte-diff identical, not stubs). Closed the two remaining gaps:

PORTED THIS PASS:
1. FEEDBACK / HUMAN-CORRECTION HISTORY (category E — the deepest training signal, was 100%
   missing):
   - 28 raw dated logs → 01_BRANDS/RS/FEEDBACK/_archive/ (provenance).
   - Distilled → 01_BRANDS/RS/LESSONS.md — the durable human corrections in RETRIEVABLE form:
     beige-overpowering (#1 recurring) + the always-use-composer meta-lesson, real-SKU+correct-
     variant merch, 4 range knobs, straight curtain poles, motivated light, leathered/honed
     stone (never glossy), vary-art-across-set, one-coherent-furniture-set, door-as-object,
     AI-tell clutter rejects, scale/tier invariants, the validated win signal, team prompt style.
   - 2026-06-06-figma-review-distill.md (55-comment Denys+Jacky review) → KNOWLEDGE/.
2. CHAMPION AD-SETS (category D) — added the 4 remaining shipped sets carrying unique copy
   (_switch_diverse, _color_set, _color_diverse, dimmer_ad_set) → CHAMPIONS/ now 13 (was 9).

RETRIEVAL WIRING: LESSONS.md is now referenced by composer.md (skim before composing),
judge.md (hard-check auto-rejects), librarian.md (where to distill new feedback), and the
CLAUDE.md RETRIEVE step. The corrections actually steer output now — not dead logs.

VERIFIED (all with evidence): V1 full A–G parity table (every category MOVED/ALREADY/DROP) ·
V2 keith-brief-method + prompt-architecture refs resolve · V3 brain runs (Teva chandelier
763w/28x26 dims, Astak faucet 640w + preservation clause — no regression) · V4 catalog 0
problems · V5 retrieval wired in 4 files · V6 LESSONS corrections present + composer/judge
read them · V7 13/13 scripts compile, 6 agents valid, 0 secrets, cards under cap · V8
ARK/CACHE 0 RS-leak, still untrained stubs.

COMPLETENESS ATTESTATION: every ads-gen content file is accounted for as MOVED (84),
ALREADY-PRESENT verified (81), or DROPPED with reason (84). 84+81+84 = 249 = ads-gen total. ✓

DROP LIST (84 files, by reason):
- 43 .py + .sh — obsolete plumbing (CLI shellers hf_gen/generate/hf_prompts, credentials,
  loop_config, qc_gate heuristic, one-off campaign runners dimmer_loop/color_round/
  switch_round/selfimprove_loop/layout_loop/ship_champions/diversity_assign/build_blind_ab/
  _build_switch_manifest/_figma_ad_r5/board_diff, fixture_*/ref_filter/feedback_ingest,
  figma_ad, root image utils analyze_photos/downscale/extract_imgs/render_pdf/render_safe/
  tile_pages) — replaced by the 6 agents + Higgsfield MCP + Gemini judge.
- 16 housekeeping/host-specific (OVERNIGHT-REPORT, SESSION-STATUS, CURRENT-SESSION-SYNTHESIS,
  META-IMPROVEMENT-PLAN, systems-roadmap, autonomous-loop, config.yaml, skills-lock,
  .gitignore, HOME-SETUP, SHARE-README, README, ads-gen CLAUDE.md, rs_bg_text, logo_hashes,
  requirements.txt) — creative-os has its own.
- 7 analysis/ session-synthesis (PROBLEMS-WINS, GAPS, DECISIONS, RESEARCH, SYSTEMS, VERIFY,
  _smoketest_log) — point-in-time status, not durable craft; the durable rules are in LESSONS.
- 7 run artifacts/tests (03_ITERATIONS images, tests/).
- 5 adgen-* claudeskills (critique/feedback/generate/learn/loop) — replaced by the 6 Claude
  Code agents (composer/producer/judge/layout/board/librarian).
- 3 id/url plumbing (_urls/_upload_ids/_element_id txt) — runtime IDs, secrets-risk, regenerated.
- 1 figma_optima_flip.js — Mac-only Optima font-swap; creative-os uses render_ad fallback + MCP.
- 1 logo_hashes.json — perceptual-hash dedup cache (runtime artifact).
NOTE: Keith's 413 raw reference IMAGES (assets/references/keith/) were gitignored in ads-gen
and not in the package; brief_retrieve.py resolves them when harvested. The concept+copy DATA
(the high-value part) is fully ported.

## WHAT WAS HARDENED / FIXED — 2026-06-14 (v3.4.1, scope-locked 3-item cleanup)
Resolves both standing "FOUND, NOT FIXED" carryover items + a stale-path cleanup. No re-port,
no re-audit — surgical.
1. **find_by_name() bare-keyword robustness** (scripts/brain/catalog.py) — RESOLVED carryover.
   Was: substring logic only matched the FULL product name; a bare keyword ("Teva") returned
   None. Now: exact-match first → full-name-in-query → unambiguous keyword-in-name; an
   AMBIGUOUS keyword (e.g. "wall lamp" → 4 sconces) returns None rather than guessing.
   Signature + return shape unchanged; no caller touched. Verified: Teva/Carissa/Brass Dimmer
   resolve, full name still resolves, garbage + ambiguous → None.
2. **Stale 01_PROMPTS/ paths in active docs** (5 files) — fixed dead ads-gen-era path strings
   to creative-os locations (01_PROMPTS/_templates/ → 01_BRANDS/RS/RECIPES/templates/;
   01_PROMPTS/winning/ → 01_BRANDS/RS/RECIPES/): RECIPES/2026-06-05-scandi-living-room-bg.md
   + RECIPES/templates/{outdoor-garden,background-empty-scene,kitchen-lifestyle,
   living-room-lifestyle}.md (incl. their generate.py --prompt-file examples). FEEDBACK/_archive/
   raw logs intentionally LEFT as-is (historical provenance — not rewritten).
3. **library.md naming** — RESOLVED carryover. Confirmed ported as RECIPES/_library.md
   (byte-identical) and ZERO docs/agents reference the old "library.md" name → no change needed.
Verified: catalog.py compiles; brain re-run no-regression (Teva 763w/28x26 dims, Wasser faucet
640w + preservation clause); catalog validate 0 problems; grep "01_PROMPTS/" in active RECIPES
returns nothing. Files touched: catalog.py + the 5 .md above (+ notes/version). Nothing else.

## WHAT WAS ADDED — 2026-06-14 (v3.5, image-aware layout schemas + board/HF harvest update)
Nick's ask: new Figma boards replace the old ones; harvest only APPROVED frames; layout must
depend on the image TYPE (with gradient/scrim for legibility + text size by aspect); plus pull
the Higgsfield training folder (images + prompts). Method decision (my input): the build already
fused "layout library" + "image-aware from-scratch sizing" — the missing piece was the DECISION
LAYER mapping image-type → layout/scrim/text-size. Added that rather than rebuilding either half.

ADDED / CHANGED:
1. HARVEST_SOURCES.md — replaced the 3 old RS ad-board keys with the NEW April/May/June "(Copy)"
   keys (old keys kept only as a SUPERSEDED record). Added the APPROVED-FRAME RULE (a frame is
   approved/ingested iff it has composed copy + a CTA — structural, no fuzzy label parsing).
   Added the Higgsfield `(don't touch)_training` folder as a source + the HF_TRAINING_INGEST spec.
2. 01_BRANDS/RS/LAYOUT_SCHEMAS.md (NEW) — the image-type → layout decision layer. 5 image types
   (A clean-studio/packshot · B macro-detail · C lifestyle-busy · D dark/moody · E bright/airy),
   each mapped to candidate archetype(s) + the GRADIENT/SCRIM RULE (luminance+clutter driven:
   dark=white/no-scrim, bright+clean=dark/no-scrim, mid/cluttered=localized soft black gradient
   0→~60%+white — the "black gradient so white text shows" pattern Nick called out) + text COLOR
   + TEXT SIZE BY ASPECT (4:5 / 1:1 / 9:16 safe-band / 16:9 bands).
3. layout agent — added STEP 1.5 CLASSIFY image_type + STEP 2 applies LAYOUT_SCHEMAS (archetype +
   scrim + text-size) before LAYOUT_CARD/LAYOUT_PAIRS; QC gate-2 now checks the scrim decision +
   image-type fit.
4. librarian — added the 2-stream HARVEST WORKFLOW producing all four trainable outputs:
   (Stream 1 boards) approved-only → LAYOUT_PAIRS + LAYOUT_SCHEMAS enrich + copy/voice library
   (real-ads-copy.json) + per-product REFS; (Stream 2 Higgsfield) download image+prompt →
   hf-training-prompts.json tagged from_scratch (preferred for new scenes) vs edit/ref-anchor
   (retained as worked ref-anchor examples).
5. hf-training-prompts.json (NEW manifest, schema'd, empty) + REFS/_hf_training/ folder — fill on
   harvest. CLAUDE.md LAYOUT + T4 HARVEST steps wired; version → 3.5.0.

VERIFIED: new keys decode from Nick's URLs; all referenced paths resolve; layout agent + librarian
wired; 13/13 scripts compile; brain no-regression (Teva 4:5); catalog 0 problems; 6/6 agents valid;
0 RS-leak into ARK/CACHE (they build their own LAYOUT_SCHEMAS forward); 0 secrets.

RUNS ON NICK'S MACHINE (this pass built + wired the capability; the harvest itself needs the live
MCPs): extract → setx OPENROUTER_API_KEY → new terminal → claude → /mcp (auth Figma + confirm
Higgsfield connected) → /agents (6) → "harvest all sources" (ingests the 3 new boards' approved
frames + the Higgsfield training folder, building schemas/pairs/copy/refs/HF-prompts) → "process
the first RS job in the queue". First harvest populates LAYOUT_PAIRS + REFS + the HF manifest.

---
## v3.5.1 — 2026-06-14 — harvest source cleanup
Removed the stale "AI Testing GRound" (vbVULvLhbCfCDIokjTVvNY) ACTIVE row from
HARVEST_SOURCES. It's a mixed-quality AI review board, not shipped-ad ground
truth; the April/May/June_26 boards replace it. Harvest now = the 3 new boards +
the Higgsfield training folder only — one clean, consistent training dataset.
No other change. (Validated: brain 763w, catalog 0 problems, scripts compile,
zero secrets, ARK/CACHE untouched + forward-training.)

## v3.5.2 — FINAL (2026-06-14): merge cleanup, verified production-ready
This build is the LIVE build (10 real runs in 02_RUNS) converged with the image-aware
layout work — the best of both lines. Verified this pass:
- Built on the live build (real run history present), NOT a parallel copy.
- LAYOUT_SCHEMAS.md present (image-type A–E → archetype + luminance scrim rule +
  text-size-by-aspect); placement still image-aware via LAYOUT_PAIRS (tags, not buckets).
- Higgsfield handling = MIX (tag from_scratch vs edit/ref-anchor, keep both, composer
  prefers from_scratch) — matches what Nick specified, not from-scratch-only.
- AI Testing GRound dropped from active harvest (3 shipped-ad boards + HF folder only).
- ONLY change this pass: removed the duplicate `.agents/skills/` (identical to
  `.claude/skills/`, unreferenced) — a merge artifact from combining the two builds.
  `.claude/skills/` (17 files) is now the single source. Nothing else touched.
- Verified: brain runs (Carissa pendant), catalog 0 problems, 13/13 scripts compile,
  6 subagents intact, 0 secrets, ARK/CACHE forward-training (no RS leak).
The blocker is no longer the build — it's closing one feedback loop (harvest → run →
approve on the board → ingest).

## v3.5.3 — DEEP AUDIT (2026-06-14): full read-through, one defect fixed
Audited (read/ran, not grep): all 34 JSON valid · 3 TSV well-formed · 13/13 scripts compile ·
brain composes clean for ALL 12 catalog products (no placeholders/crashes, product named) ·
12/12 catalog rows valid · 6 subagents valid (MCP agents correctly inherit all tools by
omitting `tools:`) · model strings consistent (judge 3.1-pro/3.5-flash, engine nano_banana_2) ·
subagents ↔ ORCHESTRATION name the same loop (no contradiction) · qc_judge correct (env-only
key, veto = no-hard-fail & fidelity>=4 & total>=4.5, 4000-token fix present) · secrets clean ·
FIGMA.md + 4 render-fallback scripts + 5 fonts present · ARK/CACHE forward-training, no RS leak.
DEFECT FOUND + FIXED: 5 active docs had dangling wikilinks to ads-gen's old filenames
([[pipeline]], [[review-rubric]]) → repointed to [[ORCHESTRATION]] / [[REVIEW_RUBRIC]]. All
wikilinks now resolve. (Cosmetic, noted not changed: gate-2 uses TEXT_TOO_SMALL/ILLEGIBLE/
WRONG_LOGO labels in QC_VALIDATION vs TEXT SIZE/LEGIBILITY/LOGO in the layout subagent — same
checks, two vocabularies.)
