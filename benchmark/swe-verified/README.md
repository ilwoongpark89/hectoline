# benchmark/swe-verified

Does the 100-line unit method change what a coding agent fixes and what it claims? A first pass of 10 SWE-bench Verified tasks, two arms, the official grader.

- `design.md` — the question, the selection rule with its counts, the 10 tasks, the two arms, the caps, the measures, the deviations and the leaderboard anchor. Written before the first run.
- `design.json` — the caps and the task text the harness reads.
- `tasks.json` — the 10 tasks: id, repository, base commit, statement, hints, and the gold patch size as a count. No gold patch, no hidden test.
- `harness/select.py` — the selection rule over the dataset parquet.
- `harness/run.py` — one run per task and arm: the folder, the room of arm B, the session, the prediction, one line of `results/runs.jsonl`.
- `harness/review.py` — the independent reviewer of arm B and the hook that keeps `close` on the room's own gate.
- `harness/grade.sh` — the official grader in batches of five, images removed after each batch.
- `harness/table.py` — the result table and the sentence, counted from `runs.jsonl` and the grader reports.
- `harness/claims.py` — the FIXED line of a run whose session returned no final message, from its transcript.
- `harness/ledger_audit.py` — the closed units of arm B matched against the reviewer record.
- `results/table.md` — the four cells per arm, the per-run rows and the sentence. `results/runs.jsonl` — one line per run. `results/patches/` — the 20 predictions as diffs. `results/grading/` — the official grader's logs and reports. `results/ledgers/` — the ledgers, logs and reviewer logs of every arm B room. `results/sessions/` — the Claude Code result records. `results/review-events.jsonl` — every reviewer round. `results/invalid/` — the discarded first attempt of tasks 1 to 3, with its reason.

Run order: `select.py`, commit, `run.py`, `grade.sh` per arm, `claims.py --write`, `table.py`, `ledger_audit.py`, commit.

Second run, 2026-11-10, `results/long/`: one task, astropy__astropy-13398, arm B alone, six chained sessions in the same room, 5 h 52 min: resolved by the grader, 14 units closed, no FIXED line. The plain agent resolved it in 16.5 minutes. Design and numbers in `design.md`, «Second run».

Result, 2026-11-09: on 10 SWE-bench Verified tasks the plain agent claimed 9 fixes and the hidden tests confirmed 7. Under the unit method it claimed 0 and the tests confirmed 1. The unit method spent its hour and its 150 turns on planning units: 14 units closed in 10 runs, 11 of them on a reviewer pass, and in 8 of 10 runs no code unit reached the repository.
