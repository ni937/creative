# VERIFICATION — the loop is closed only when the fix is proven (PV-09 lite)

Every fix shipped after feedback carries:
  verification_status: PENDING | CONFIRMED | FAILED | EXPIRED

- PENDING   fix in a new run, untested
- CONFIRMED a later run shows the failure gone (link the run-id)
- FAILED    same failure on the new run → original diagnosis was WRONG.
            Re-diagnose excluding that hypothesis. Do not re-patch the same field.
- EXPIRED   3+ sessions, no test data → fix may not be cited as evidence

FOUR GATES
1. Only CONFIRMED fixes become KNOWN_WINS.
2. Only CONFIRMED fixes promote prompts to WINNING.md.
3. A regression is cleared only by a CONFIRMED corrective run — never by merely shipping the correction.
4. Session start: report all PENDING. If today's runs touch that template, test the pending fix FIRST.

METRIC: loop_closure_rate = (CONFIRMED+FAILED)/shipped. Below 0.6 = shipping blind. Tracked in 04_KNOWLEDGE/METRICS.md.
