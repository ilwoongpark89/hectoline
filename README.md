# hectoline

The 100-line unit method for work with coding agents. One open unit at a time. At most 100 added or modified lines per unit. One check that fails before the unit and passes after it. One independent review. One commit. An audit every ten units. Hooks deny every edit tool call outside the open unit. They deny every shell write to a .md, .py, .json or .toml file there. The pile check blocks any other changed line at the commit and at the end of the turn.

The rule is `RULE.md`. The gate is `unit.py`. The ledgers are six Markdown files in each room. This repository is the public version of the folder that has run the author's projects since 2026-10-31.

## Quick start

```sh
git clone <this repository> hectoline && cd hectoline
python3 -B example/build.py /tmp/rooms
python3 -B unit.py selftest /tmp/rooms/01_pressure-drop
python3 -B unit.py status /tmp/rooms/01_pressure-drop
python3 -B room.py 02_myroom "the outcome in one sentence" "the owner line" --top /tmp/rooms --accept "the check that shows the outcome"
```

Requirements: macOS with `sandbox-exec`, git with a user name and email, Python 3.11 or later. The close step clones the room and runs each check clause in a write-denied sandbox. Rooms live beside this folder by default. The variable `HECTOLINE_ROOMS` names another folder. With `--accept`, the first commit of a room holds its first goal leaf with two steps. They are the measure step and the pilot step. The commit also holds the planned measure unit. The first call of a new author is then `unit.py open U0002 ROOM`.

## Rooms and ledgers

A room is a folder with six ledgers and its own git repository. `OWNER.md` holds the owner statements, the A rows. `GOAL.md` holds the goals, the G rows, each with one measure and a target. `PLAN.md` holds the steps, the S rows. `UNITS.md` holds the units, the U blocks. `PRODUCTS.md` holds the product tree, the P rows. `RESEARCH.md` holds the source claims, the R rows. The chain is one way: A → G → S → U → P. A row without a parent in the layer above cannot exist. `room.py` makes a room with links to the rule and the tools in this folder.

## The unit life cycle

1. Open. `unit.py open U#### ROOM sentence plan files lines` appends the block or turns a planned block open. The block exists before the first edit of any file it names. Open prints the unit pack: the leaf, the step, the owner quotes and the last units on each file.
2. Check. The check key holds shell clauses. Each clause must exit non-zero on a copy of HEAD and zero after the unit. A clause that passes at the base is refused.
3. Review. A second session reads the diff and the nine verdict keys. It writes its log to a file outside the room. The first line of that file names the unit. Its last line reads `R1 PASS` or `R1 FAIL`. The review key names the file by its path with its sha256, and it records every round. Close reads the verdict from the file. The edit gate denies the author of the unit a write to a file named `agent-review-u####-rN.md` for that unit. It does so in a numbered room directly inside `HECTOLINE_ROOMS`. It binds only the session that opened the unit. The third failed round ends the unit and reverts its lines.
4. Close. `unit.py close U#### ROOM` reruns the check and runs the baseline. It counts the lines from the staged tree and commits under the unit number. Every count in the block is the output of the command, never typed.

## The audit

After every tenth unit, `unit.py open` accepts only an audit unit or one planning unit. `audit.py N ROOM` reruns every closed check on a copy of the room. It lists piles, duplicate lines, unused definitions, steps without a move and goal leaves without a unit. At 100 units the audit remeasures the goal table and lists the restructuring.

## The hooks

`hooks/install.py` installs three gates. Claude Code hooks call `unit.py check` before and after each edit and deny with exit 2. Codex hooks deny with a permission decision. The git pre-commit runs validate and pile. A commit holds exactly one unit that turns final, and the pre-commit judges that commit itself. It reads the review file, reruns the check with its baseline test and compares the index with the files key. A status word turned closed by hand commits only with a passing review file outside the room. Its check must be red on HEAD and green in the tree. A room whose `unit.py` is gone is still judged, since the hook runs the tools beside its own file. A review file must carry the name of its unit. The commit hook records each tree it passes under the git folder. Each hooked tool call sets HEAD back from a commit whose tree is not in that record. Hooked calls are an edit, a write, a shell line, a web call and an agent call. So a commit that skips the hook by accident does not stay. A probe on fresh rooms tried the short flag `-n`, a changed hooks path and a replaced hook link. Each commit was undone at the next hooked tool call. This holds while a hooked session makes a next call. Under a copied hook a hand close was refused. Three roads stay open at this commit. A shell line that the edit gate does not read can write a review file of the right name. A review key can name an older passing review file of the same unit number. The files in `example/reviews/` are such files. The author can also write the record itself. One shell line that commits past the hook and then removes or extends the record keeps its commit. The same holds for the log with its shadow copy. A push in that same line carries the commit to the remote. Each is a deliberate road in the words of `RULE.md` §8. The structure stops drift, not an author who aims at it. A pile is a line that no unit block names. A pile blocks the commit and the end of the turn. The log is append-only by `ledger.py`, which keeps a shadow copy under the git folder. Each hooked tool call restores a log that differs from that copy. No text rule on a shell line guards the commit or the log in this version. A web search outside a research unit is denied too.

## Gates

A gate is any check that can refuse work. A hook rule, a tool refusal, a check clause and a forbidding sentence of the rule are gates. `RULE.md` §8 limits them. A gate enters on an owner request that names it. It also enters for a fault that occurred, when no change of structure prevents that fault. A unit that adds or changes a gate shows six tests, each with its command. The gate refuses a planted fault. Its reference comes from outside the thing it tests. Form alone does not pass it. The correct work it blocked is counted. Its refusal text names the form that passes. No other gate catches the same fault, or the two merge. At each 50-unit boundary every gate takes the six tests again. Before the six tests the review asks where the gate comes from. A gate with no owner line, no fault and no research row behind it is a candidate of anchoring. A text match on a shell line holds no reference, since another spelling passes it. `docs/gates-research.md` lists the sources behind these rules. `gates.py` lists every refusal site of the tool code. Version 1.1 held 207 sites and this version holds 53. Of the 207, 151 stood in code that only the selftest reached, never a room command. The sites that a room command could reach fell from 56 to 53. That count does not rise between two reviews.

## The example

`example/01_pressure-drop/` is the snapshot of one run of `example/build.py`. `room.py --accept` made the room with its goal leaf G1. Every later change entered through `unit.py open` and `unit.py close`. The tool wrote every block. The pre-commit hook judged every commit. The room holds six units. They are the bootstrap, the measure, a planning unit, the formula, its command line and one audit. The goal leaf G1 moved from unmeasured to 1 to 0. The audit output is `audits/audit-06.txt`. Its check rerun lists two units with a clause bound to the state at their close. The measure unit asserted g1 at 1, which turned false when the command line entered. The reviews in `example/reviews/` were written by the session that built the room. They show the form of a review, not an independent one. Each review key holds the path of its file on the machine that built the snapshot.

## The measured failure

The method was audited on its own room between 2026-11-05 and 2026-11-07. The rule file held 104 lines, under its 500-line cap. One of those lines held 23 sentences. Four audits ran on schedule. Three of them changed 18 lines of their own ledger and one changed 21. No audit changed a rule or a tool. An audit of the rule text on 2026-11-07 found 14 rule lines with 29 quoted sentences that no tool or reviewer enforced. The counts, the commands and the ledger lines are in [docs/evidence.md](docs/evidence.md). The same page holds two larger cases. A landing page kept 5,570 dead lines of 6,487. A document used 23 % of its 184 sources.

## The pilot

A pilot ran 10 SWE-bench Verified tasks with one model, under this method and without it. The record is in `benchmark/swe-verified/`. Without the method the agent claimed 9 fixes and the hidden tests confirmed 7. Under the method it claimed 0 and the tests confirmed 1. The room logs of those 10 runs hold 473 refusals. 357 of them repeat a text that the same run had already shown. The most frequent text, 191 of the 473, named no call that would pass. In 4 of the 10 runs no unit closed. In one run 3 units closed with no reviewer pass.

So the method was turned on its own gates. Each refusal now names the call or the text that passes. Every gate was asked where it came from and was tested with a planted fault. Text matches on command lines left, and structure took their place. The refusal sites fell from 207 to 53, by `gates.py` on the tags `v1.1` and `v1.2`. 151 of the 207 stood in three modules and their helpers that only the selftest reached. The method had piled up gates that no room command ran. Three sites that a room command could reach left too. The tool code with its selftest fell from 5,300 lines to 4,440. The sources behind the gate rules are in `docs/gates-research.md`. The selftest reads 102 of 102 on the sample room.

A re-test then ran two tasks under version 1.2, one session of one hour each. The record is in `benchmark/swe-verified/results/retest/`. On django__django-11885 the pilot run held 109 refusals, no closed unit and no patch. The re-test run held 1 refusal and 4 closed units, and the hidden tests confirmed its patch. Nobody had read scikit-learn__scikit-learn-25102 before the run. Its log held 2 refusals, and the hidden tests confirmed its patch. All 6 closed units have a reviewer pass in the record. Both sessions ended at the one-hour cap with the confirming change in the last, open unit.

A fourth run took the three pilot tasks that the agent without the method had not solved, with up to six sessions for each arm. The record is in `benchmark/swe-verified/results/hard/`. By the hidden tests the agent without the method ended 2 of the 3 correct and the method ended 1 of the 3. Each arm made one claim that the tests refused. The method closed 17 units, and all 17 have a reviewer pass. On sympy__sympy-16597 neither arm solved the task in six sessions. The agent without the method claimed a fix there, and the method made no claim. On django__django-16263 one hidden test refused the method's patch. That test asserts a query form that Django named a regression five days after its merge, in commit 10037130c123. Django's corrected test class passes 4 of 4 on the method's patch and fails 1 of 4 on the other patch, which counts 3 books where 2 exist. The final text of the session without the method names the hidden test and that later commit. Both patches reuse test names of the upstream commit. `benchmark/swe-verified/design.md` holds the table and both counts.

## Why

The author works under this method every day. It keeps work in small, reviewed units and records what failed. It also shows where it falls short. Every failure in the record had one shape. The loop closed on a signal the agent had produced itself. A check that exits zero, a block marked closed, a report sent. Agents add checks nobody asked for. They bypass or game those checks, then report the work complete. One document was delivered with 23 % of its sources used. In the pilot the method's own refusals stalled the agent. One run met 109 refusals, and 76 of them were one text that named no call that would pass. So the method keeps its gates to a reasoned minimum. Each refusal names the form that passes. Each gate must stop a planted fault, with a reference from outside the thing it tests. Every 50 units all gates take those tests again, and duplicates merge. A passed gate does not show a solved problem.

## Changes from the private folder

This tree is a cut of a private room at its unit U0615. Owner quotes, personal paths, references to other rooms, the report page and the owner ledgers of that room left. The internal name changed to hectoline. The built-in self-measures of the private room left with its goal table. A room computes its leaves in its own `measures.py`. `gates.py` reads the tool code of its own folder. Selftest cases bound to the private room left or run on a fresh room. The git history holds the earlier cuts.

## License

MIT, Il Woong Park.
