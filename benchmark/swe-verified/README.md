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
- `results/` — empty at the design commit. The runs fill it.

Run order: `select.py`, commit, `run.py`, `grade.sh` per arm, `table.py`, commit.
