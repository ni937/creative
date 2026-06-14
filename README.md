# creative-os — quickstart (anyone on the team can run this)

One brain, three brands (ARK / CACHE / RS). Claude composes prompts from .md
templates, Higgsfield MCP generates, every output is scored and the system
gets smarter. No python required to operate.


## HOW TO USE IT — day one to trained

**Day 1 — wire it (30 min, once)**
1. Open this folder in Claude (desktop/Code) so CLAUDE.md loads as the brain.
2. Engine: official Higgsfield CLI + skills (`npm i -g @higgsfield/cli` →
   `higgsfield auth login` → `npx skills add higgsfield-ai/skills`). Figma MCP for Claude Code (one-time, from your terminal):
   `claude mcp add --transport http figma https://mcp.figma.com/mcp`
   then `/mcp` inside the session to authenticate. (claude.ai connectors do
   NOT carry into Claude Code — it has its own registry.)
3. QC judge key — Windows: `setx OPENROUTER_API_KEY "your_key"` (then restart
   the terminal/Claude Code). Mac/Linux: `export OPENROUTER_API_KEY=...`.
   Key lives in your env, NEVER in these files.
4. Create the review file in Figma: "AI Review" with a Day-1 page,
   dark-charcoal canvas (#1E1E1E).

**Day 1 — first run (proves the machine)**
Say: "run the first RS job in the queue." Watch the full loop once:
compose → generate → self-critique → panel QC (`scripts/qc_judge.py`) →
Figma push. Approve or comment on the board. Then say "ingest the board" —
your verdict gets logged, the approved frame harvested to REFS/.

**Week 1 — train it (this is the actual training)**
- Run 5–10 jobs per brand through the queue. EVERY approval = training data.
- Be specific in comments: "accent should be olive not navy" trains;
  "looks off" doesn't.
- End of week: run the TRAINING.md cadence (~20 min) — promote winners,
  resolve verifications, register Elements for anything used twice, metrics row.

**Steady state**
Fill _QUEUE.md → "process the queue" → review the board when convenient →
weekly training pass. Watch one_shot_rate climb in METRICS.md — that number
IS the system getting smarter. ARK/CACHE composer locks auto-confirm after
their first 3 approved runs.

## Run a generation (the whole job)
1. Open Claude (Higgsfield MCP connected) with this folder as context.
2. Say: "Generate [what you need] for [BRAND]" — e.g. "RS chandelier hero,
   dining room, 4:5". Claude does the rest: retrieves the brand card +
   composer + winning entries → composes → generates → self-scores →
   shows you only QC-passed images.
3. Review happens on the Figma board (Day page). Approve with the "approved" label or a DONE reply; otherwise comment on the frame — ES or EN both work. Be specific — "make the accent green not
   navy" trains the system; "looks off" doesn't.
4. Done. Approved winners get promoted automatically; your feedback is
   logged and verified on the next run.

## Rules even humans follow
- Never mix two brands in one request.
- Product shots always use the real packshot/Element — never "close enough".
- If Claude says a fix is PENDING verification, test that first.

## Weekly training pass (~20 min — see 00_SYSTEM/TRAINING.md)
Promote winners → resolve pending verifications → register repeat assets as
Elements → one metrics row. That's how it stays smart.

## Folders
00_SYSTEM rules · 01_BRANDS cards+composers+corpus · 02_RUNS every generation
· 03_FEEDBACK scored feedback · 04_KNOWLEDGE metrics+patterns+elements
