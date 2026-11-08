# Design — SWE-bench Verified under hectoline, first pass of 10 tasks

Written and committed before the first run, 2026-11-09. The caps below are the caps of `design.json`, the file the harness reads.

## The question

On public benchmark tasks with hidden tests, how many does a coding agent fix, how many does it claim to have fixed, and does the 100-line unit method change either? The sentence the result fills: «On 10 SWE-bench Verified tasks the plain agent claimed X fixes and the hidden tests confirmed Y. Under the unit method it claimed X′ and the tests confirmed Y′.»

## The benchmark and the grader

SWE-bench Verified: 500 human-validated GitHub issues from Python repositories, dataset `princeton-nlp/SWE-bench_Verified`, split `test`. The grader is the `swebench` package, version 5.0.2, `swebench eval verified -p predictions.jsonl --run-id <id> -j 2 -t 3600`. It applies each patch inside the instance image of the task and runs the hidden FAIL_TO_PASS and PASS_TO_PASS tests. Only its `report.json` decides «resolved». The agent never sees `patch`, `test_patch`, `FAIL_TO_PASS` or `PASS_TO_PASS`; `tasks.json` carries the statement and the hints only, and the harness never opens the parquet.

## Task selection, fixed before any run

Rule, `harness/select.py`: rows with difficulty «1-4 hours» whose gold patch touches at least two files, sorted by the length of the gold patch, largest first, the first 10 with at most 3 per repository. The unit method is for long work, so the long tasks are the test. The next 20 follow the same sorted list from rank 11 on, with the per-repository cap continuing.

| step | rows |
|---|---|
| rows in the split | 500 |
| difficulty «1-4 hours» | 42 |
| gold patch touches at least 2 files | 23 |
| first 10 with at most 3 per repository | 10 |

| # | instance | repository | gold patch files | gold patch bytes | base commit |
|---|---|---|---|---|---|
| 1 | astropy__astropy-13398 | astropy/astropy | 4 | 13884 | 6500928dc0 |
| 2 | astropy__astropy-14369 | astropy/astropy | 2 | 12099 | fa4e8d1cd2 |
| 3 | django__django-11885 | django/django | 2 | 10818 | 04ac9b45a3 |
| 4 | django__django-16560 | django/django | 2 | 10743 | 51c9bb7cd1 |
| 5 | sympy__sympy-16597 | sympy/sympy | 6 | 10210 | 6fd65310fa |
| 6 | django__django-16263 | django/django | 4 | 9785 | 321ecb40f4 |
| 7 | pylint-dev__pylint-4551 | pylint-dev/pylint | 4 | 6862 | 99589b08de |
| 8 | sphinx-doc__sphinx-9461 | sphinx-doc/sphinx | 3 | 4777 | 939c7bb7ff |
| 9 | pydata__xarray-3993 | pydata/xarray | 2 | 4058 | 8cc34cb412 |
| 10 | sphinx-doc__sphinx-8548 | sphinx-doc/sphinx | 2 | 3907 | dd1615c59d |

The gold patch sizes are selection data only. They stay in `tasks.json` as counts, never as text.

## The two arms

Each run is one fresh folder: the repository fetched at `base_commit` with depth 1, one commit, plus `TASK.md` with the problem statement and the hints. The agent is Claude Code headless, `claude -p`, on the owner's subscription, no API key, with the folder as its working directory. The task text is the same in both arms and stands in `design.json`.

- **Arm A, plain**: the task text, one session.
- **Arm B, hectoline**: the folder is also a hectoline room. `room.py` writes the six ledgers, the harness lays them into the repository root, links `RULE.md`, `measure.py` and `audit.py` to this repository, installs the Claude Code hooks into the folder's `.claude/settings.json` and the git pre-commit, and commits the whole as `U0001`, so every pre-existing line has an owner block and the pile count starts at 0. The task text gains the one paragraph of `design.json`. The room's `unit.py` is a wrapper: on `close` it asks the harness reviewer first, then runs hectoline `unit.py close`. The reviewer is a second `claude -p` session, `harness/review.py`: it receives the block, the diff and `RULE.md`, runs the check clauses itself in the room, and ends with `VERDICT: pass` or `VERDICT: fail` plus one reason. The verdict enters the review key as round `r<n>`; a review key the author writes is overwritten from the harness record, so only the reviewer's verdicts count. A unit closes only on pass; the third failed verification ends it, RULE §4. A second hook denies `unit.py close` by any path but the room's own file and denies a direct `git commit`.
- **Prediction**: `git add -A`, then `git diff --cached <base tree>` with the ledger, link, hook and `TASK.md` paths excluded, written as one line of `predictions.<arm>.jsonl` with `instance_id`, `model_name_or_path` = the arm name, `model_patch`.

## Caps, the same in both arms

| cap | value |
|---|---|
| model | `claude-opus-5` |
| max turns per session | 150 |
| wall-clock per session | 3600 s, then the process group is ended and the run is recorded as timed out |
| reviewer | the same model, 20 turns, 600 s per round |
| sessions at once | 2, the two arms of one task |
| load gate before each pair | CPU sum under 600 % of 1000 %, free memory over 20 %, by `ps` and `memory_pressure` |
| disk floor | 150 GB free on `/`, by `diskutil info /`, checked before each grading batch |
| runs | 10 tasks × 2 arms = 20, one run per task per arm |

Tools of the candidate: Bash, Edit, Write, Read, Glob, Grep, MultiEdit, NotebookEdit, TodoWrite; WebSearch, WebFetch and Agent are denied. The reviewer has Read, Glob, Grep and Bash. Both arms run with `--setting-sources project`, so the owner's user settings, hooks and memory files stay out; arm B's hooks come from the room's own `.claude/settings.json`.

## Measures

Per run: resolved by the grader, yes or no; claimed, the last line `FIXED: yes` or `FIXED: no`, or none; patch lines and files; wall-clock; turns; timed out; for arm B, units closed, units failed, audits closed, review rounds passed and failed, hook denies in `unit.log`. Per arm: resolved of 10, claimed of 10, false claims of claimed, and the four cells claimed × resolved. `harness/table.py` counts every cell from `runs.jsonl` and the grader's `report.json` files. No number is typed.

## Harness commands

```sh
python3 harness/select.py verified.parquet tasks.json 10
python3 harness/run.py tasks.json WORK results                       # both arms, task by task, two sessions at once
sh harness/grade.sh results/predictions.plain.jsonl plain results/grading
sh harness/grade.sh results/predictions.hectoline.jsonl hectoline results/grading
python3 harness/table.py results/runs.jsonl results/grading results/table.md
```

The harness Python is a standalone CPython 3.12 installed with `uv`; `run.py` puts it first on the PATH of every session as `python3` and `pip`.

## The leaderboard anchor

The official leaderboard at swebench.com carries no Claude 5 model on the Verified split; its latest Anthropic entry is Claude 4.5 Opus (high) with mini-SWE-agent at 76.8 %, 2026-02-17. Vals AI ran Claude Opus 5 with Mini-SWE-agent on the full 500 and reports 97.00 % as of 2026-09-01, https://www.vals.ai/benchmarks/swebench, a benchmark it has since archived as saturated. That number places the 10 tasks: they are the 10 largest multi-file «1-4 hours» tasks, the hard tail of a split the model resolves almost whole.

## Deviations from the written prompt, and why

1. Permission flags. The prompt names `--dangerously-skip-permissions`. The harness uses `--permission-mode dontAsk` with an explicit tool allow list instead: the same autonomy for the listed tools, no blanket bypass. The session's command classifier refused the blanket flag.
2. Python. The Homebrew Pythons of this Mac load `pyexpat` against a system `libexpat` that lacks a symbol, so their `pip` cannot reach an index. The harness and the sessions use a standalone CPython 3.12 from `uv`, first on the PATH. Both arms see the same interpreter.
3. Images. `swebench` 5.0.2 has `--task-repo` for local builds, but no task repository is published with the package. The grader pulls the official `x86_64` instance images and Docker Desktop runs them under amd64 emulation, which the test `docker run --platform linux/amd64 alpine uname -m` confirmed. The grading timeout is 3600 s per instance for that reason.
4. History. The repository is fetched with depth 1 at `base_commit`, so the room's pile rule sees one owner commit. The tree equals the base tree plus `TASK.md`; the prediction diff is taken against that tree.
5. The owner's own settings. Every session runs with `--setting-sources project`, so the owner's global hooks and memory files do not reach the candidate. The method's hooks enter arm B through the folder.

## Size

A first pass of 10 tasks, no held-out set, one run per cell. The table reports counts, not rates with intervals. The selection rule and the harness are written so that the next 20 tasks follow the same rule.
