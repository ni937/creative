# ORCHESTRATION — orchestrator + subagents (Claude Code native)

The MAIN Claude Code session IS the orchestrator. It reads this vault's
CLAUDE.md, owns 02_RUNS/_QUEUE.md, and dispatches the team in .claude/agents/:

  composer → producer → judge(image QC) → layout(compose in Figma + layout QC)
  → board(push for human) ... [human approves] ... board(ingest) → librarian

ORCHESTRATOR RULES
1. Per queue job, dispatch in sequence: composer → producer → judge. Image
   PASS + job is an ad format → dispatch layout (compose + layout QC). SCENE-
   only jobs skip layout. layout-passed → collect for board push (batch ≤5). FAIL with fix → ONE recompose→regen cycle
   max, then HUMAN-REVIEW. Judge HUMAN-REVIEW → straight to flagged list.
2. PARALLELISM: dispatch up to 3 queue jobs concurrently (3 composer→producer→
   judge pipelines). Same-brand jobs parallelize safely (read-only brand files).
   NEVER two librarians at once (only writer of knowledge files).
3. ROLE SEPARATION IS LOAD-BEARING: judge never sees composer reasoning;
   producer never final-verdicts; only librarian edits brand knowledge. Do not
   "save time" by collapsing roles into the main thread — that recreates the
   self-grading flaw v1.3 was built to kill.
4. STOP CONDITIONS (AUTOMATION.md) are enforced by the orchestrator: credit cap,
   5-consecutive-fail breaker, oscillation halt, judge-outage hold.
5. End of batch, report: jobs run, one-shot rate, pass/fail, credits, flags.
   Then dispatch librarian for ingest/harvest when the human has reviewed.
