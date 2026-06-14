# AUTOMATION — the unattended loop + the one-shot path (v1.3)

## What "fully automated" means here (honest definition)
Everything between BRIEF and the Figma push runs unattended:

  QUEUE → COMPOSE → GENERATE → SELF-CRITIQUE(≤3, Judge A) → PANEL QC (Judge B,
  Judge C tiebreak) → push PASS frames to Figma → auto-ingest verdicts later

The HUMAN GATE stays — by design, not laziness. Human approvals are the
training data (T4 harvest, judge calibration, HIGH-signal feedback). Remove
the gate and the system stops learning and the judges drift unchecked. The
goal isn't "no human ever" — it's "humans only see finished work, ~30 seconds
per approval."

## The queue (how to run a batch unattended)
02_RUNS/_QUEUE.md — one line per job:
  `[ ] BRAND | product/concept | scene archetype | aspect | refs/element`
The operator (Claude session or scheduled agent) processes top-to-bottom:
each job = full loop to figma-push, then next. Checked off with run-id linked.

## ONE-SHOT — the system's north-star metric
one_shot_rate = runs where iteration 1 passes the FULL panel / total runs.
This is what "training" buys you. The causal chain:
  more approved frames → richer REFS + WINNING corpus → composer starts from
  proven DNA → fewer self-critique cycles → one-shot.
Expected trajectory (set expectations, don't lie to yourself):
  cold brand (ARK/CACHE day 1): ~20–40% · 25 approved frames: ~60% ·
  mature corpus (RS inherits one): 70–85%. Below trajectory after 50 runs =
  composer locks are wrong → aesthetic-model pass, don't brute-force retries.
Tracked per brand in METRICS.md. ONE-SHOT IS EARNED BY THE CORPUS, NOT BY
LOOSENING THE GATE. Never trade pass-threshold for one-shot rate.

## Stop conditions (the loop halts itself — no runaway spend)
1. CREDIT CAP per batch (set in _QUEUE.md header; default 200 credits) — hit
   it, stop, report.
2. KILL RULE (R8): panel total < 2.5 twice on same approach → skip job, log.
3. OSCILLATION: same composer field edited 3+ times in one run → halt job,
   flag HUMAN-REVIEW (the fix isn't wording — something structural is wrong).
4. JUDGE OUTAGE: Judge B unreachable after retries → batch pauses at
   `generated`. NOTHING auto-passes on a single judge.
5. CONSECUTIVE FAILS: 5 jobs in a row fail panel → stop batch (likely a
   systemic issue: bad ref, wrong card version, engine change).

## Scheduled cadence (once MCPs are wired)
- Per batch (any time): process _QUEUE.md unattended → Figma push → report:
  jobs done, one-shot rate, credits, anything flagged HUMAN-REVIEW.
- Daily: ingest Figma verdicts → resolve PENDING verifications → harvest
  approved frames to REFS/ → log feedback entries.
- Weekly (~20 min human): TRAINING.md cadence + METRICS row + judge_agreement
  check.

## Failure honesty
Automation amplifies whatever the system is — including its mistakes. The
gates above are what make unattended safe. Disabling any of them to "go
faster" is how you wake up to 800 credits of beige chandeliers.
