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
| reviewer | the same model, 40 turns, 900 s per round, as `design.json` holds. This row read 20 turns and 600 s until version 1.1. Every counted run used 40 and 900 |
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

6. Work folders. The first attempt put the run folders under the owner's `~/claude` tree. Claude Code loads every `CLAUDE.md` on the path from the working directory to the root, so each session of tasks 1 to 3, in both arms, carried the owner's two instruction files. Those six runs are discarded and kept under `results/invalid/first-attempt/` with the reason. The runs that count use `/private/tmp/hectoline-pilot-work`, where a test session lists no instruction file. The first attempt also found two harness defects, repaired before the rerun: a reviewer session that ended without a verdict consumed a round number and left the review key unparseable, which the arm B author of task 1 repaired itself by reading the harness and editing the reviewer's state files; and the session's own folder was not fenced, which that same reading shows. Now a no-verdict session takes no round number, the reviewer record lives outside the run folder and rebuilds the review key, and a hook in both arms denies any read or write under the pilot folder outside the session's own folder.

7. The reviewer's seat. Until task 6 the reviewer session ran inside the room, so the room's Stop hook, which refuses a stop while a pile exists, acted on the reviewer too: in task 6 all seven reviewer sessions ended with an empty answer, and the author closed three units on review keys it had written itself, because the harness rewrote the key only when a verdict came. From task 7 the reviewer runs from the run folder beside the room, and a session without a verdict rewrites the key to «no verdict yet», so close waits. `results/ledger-audit.md` counts, per run, the closed units that match a reviewer pass in the harness record and those that do not: 3 of 14 closed units do not, all in task 6.
8. The FIXED line of a refused stop. The same Stop hook refused the author's own stop in arm B, so a session could end at its turn cap with an empty result although its last message held the line. `harness/claims.py` reads the session transcript for runs whose result was empty and records `claimed_source` = transcript; it recovered one line, «FIXED: no» for django__django-16560. Runs killed at the wall cap hold no final message in either arm.
9. Arm B patches may carry the room's `measures.py`, the measure the method asks for; it is a new standalone file and the grader applied every such patch.

## Second run: one task to the end, chained sessions

Owner, 2026-11-09: «핵토라인은 정해진 시간동안 하는게 아니고 시간을 많이 주고 틀리지 않는건데?» and «2번 먼저 해». The first run capped both arms alike, which measured the method's entry cost and not its promise. The second run measures the promise on one task, astropy__astropy-13398, the largest gold patch of the ten, where arm B closed one planning unit in 70 minutes: arm B runs in the same room through sessions of 150 turns and 3600 s each; when a session ends without a FIXED line, the next session starts in the same folder with the same task text plus one paragraph that names the earlier sessions and the ledgers, up to 6 sessions. The run ends at the first FIXED line. Measures: resolved by the grader, claimed, sessions used, total wall-clock and turns, units closed, reviewer rounds, and whether each later session continued from the ledgers rather than starting over, read from its transcript. Results go to `results/long/`, label `hectoline-long`, so the 20-run table stays as it is. `harness/run.py --chain 6 --label hectoline-long`.

Result, 2026-11-10 04:24: resolved by the grader, all 4 FAIL_TO_PASS tests pass and no PASS_TO_PASS test broke. Six sessions, 5 h 52 min of session time, five ended at the wall cap and one at its turn cap; no FIXED line, the sixth session was inside the second audit unit when the cap fell. Units: 13 work units and 1 audit closed, 0 failed, 1 audit open at the end, 16 blocks in the ledger. Reviewer rounds 23, 18 pass 5 fail 0 without a verdict, 89 reviewer-minutes. Hook denies 20. Patch 567 lines over 11 files, among them a new frame module, its tests, four documentation pages and the room's `measures.py`; the gold patch has 4 files. Every later session opened by reading the six ledgers, the log tail and `git status` before its first edit. The plain agent resolved the same task in one session of 16.5 minutes and 77 turns. One task, one run: the method reached a correct end through chained sessions at about 21 times the plain agent's session time.

## Third run: the re-test of version 1.1

Written before the run. Version 1.1 is the cut of the private room at its unit U0561. The first run showed where the minutes went. Of 525.2 session-minutes in the ten hectoline runs, 191.1 were refusals and the retries after them, 141.4 were waits for the reviewer, 92.0 were planning units. 394 of 459 gate refusals repeated a text the run had already shown. In one run three units stood closed with no reviewer pass.

What changed for a candidate. The three queue refusals name the call or the text that passes. `room.py --accept` writes the leaf G1, its measure step, the pilot step and the planned block U0002 into the first commit, so the first call is `unit.py open U0002`. Close reads the verdict from the reviewer's file by path and sha256. The pre-commit hook judges the commit of a final unit itself, so a status word turned closed by hand does not commit. No change touches the reviewer wait.

Tasks. Five, in `tasks-retest.json`. Three are the tasks that failed fastest in the first run: django__django-11885, django__django-16560, pylint-dev__pylint-4551. Their logs were read to design the changes. Two were never read by anyone before the run: scikit-learn__scikit-learn-25102 and sympy__sympy-14248, ranks 11 and 12 of `harness/select.py`, picked by that rule before any task text was opened. The hectoline arm runs all five with `--chain 3`. The plain arm runs the two unread tasks in one session each. The plain numbers of the three read tasks are those of the first run.

Measures per task: minutes to the first closed code unit, refusals per closed unit, refusals that repeat an earlier text, units closed, units closed with no reviewer pass, resolved by the official grader, claimed, sessions used. The model and the caps per session equal the first run. The command-line client is a later version, recorded in the run folder.

Verdict rule, fixed here. One unit closed with no reviewer pass fails the re-test. A change counts as an effect only where the two unread tasks move the same way as the three read tasks. Minutes and refusals are compared with the first session of the first run. A resolution in a second or third session is reported with its session count, since the first run gave these three tasks one session.

## Size

A first pass of 10 tasks, no held-out set, one run per cell. The table reports counts, not rates with intervals. The selection rule and the harness are written so that the next 20 tasks follow the same rule.
