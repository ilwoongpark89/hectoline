# hectoline

The 100-line unit method for work with coding agents. One open unit at a time. At most 100 added or modified lines per unit. One check that fails before the unit and passes after it. One independent review. One commit. An audit every ten units. Hooks deny every edit outside the open unit.

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
3. Review. A second session reads the diff and the nine verdict keys. It writes its log to a file outside the room. The first line of that file names the unit. Its last line reads `R1 PASS` or `R1 FAIL`. The review key names the file by its path with its sha256, and it records every round. Close reads the verdict from the file. The edit gate denies the author of the unit a write to that file. The third failed round ends the unit and reverts its lines.
4. Close. `unit.py close U#### ROOM` reruns the check and runs the baseline. It counts the lines from the staged tree and commits under the unit number. Every count in the block is the output of the command, never typed.

## The audit

After every tenth unit, `unit.py open` accepts only an audit unit or one planning unit. `audit.py N ROOM` reruns every closed check on a copy of the room. It lists piles, duplicate lines, unused definitions, steps without a move and goal leaves without a unit. At 100 units the audit remeasures the goal table and lists the restructuring.

## The hooks

`hooks/install.py` installs three gates. Claude Code hooks call `unit.py check` before and after each edit and deny with exit 2. Codex hooks deny with a permission decision. The git pre-commit runs validate and pile and lets only `unit.py close` commit. It judges the commit of a unit that turns final. It reads the review file, reruns the check with its baseline test and compares the index with the files key. A status word turned closed by hand does not commit. A pile is a line that no unit block names. A pile blocks the commit and the end of the turn. The hooks also deny `--no-verify`, a changed hooks path and a write to the log. A web search outside a research unit is denied too.

## Gates

A gate is any check that can refuse work. A hook rule, a tool refusal, a check clause and a forbidding sentence of the rule are gates. `RULE.md` §8 limits them. A gate enters on an owner request that names it. It also enters for a fault that occurred, when no change of structure prevents that fault. A unit that adds or changes a gate shows six tests, each with its command. The gate refuses a planted fault. Its reference comes from outside the thing it tests. Form alone does not pass it. The correct work it blocked is counted. Its refusal text names the form that passes. No other gate catches the same fault, or the two merge. At each 50-unit boundary every gate takes the six tests again. `gates.py` lists every refusal site of the tool code, 206 in this version. That count does not rise between two reviews.

## The example

`example/01_pressure-drop/` is the snapshot of one run of `example/build.py`. `room.py --accept` made the room with its goal leaf G1. Every later change entered through `unit.py open` and `unit.py close`. The tool wrote every block. The pre-commit hook judged every commit. The room holds five units. They are the bootstrap, the measure, a planning unit, the calculator and one audit. The goal leaf G1 moved from unmeasured to 1 to 0. The audit output is `audits/audit-05.txt`. Its check rerun lists three units with a clause bound to the state at their close. The measure unit asserted g1 at 1, which turned false when the calculator entered. The reviews in `example/reviews/` were written by the session that built the room. They show the form of a review, not an independent one. Each review key holds the path of its file on the machine that built the snapshot.

## The measured failure

The method was audited on its own room between 2026-11-05 and 2026-11-07. The rule file held 104 lines, under its 500-line cap. One of those lines held 23 sentences. Four audits ran on schedule. Three of them changed 18 lines of their own ledger and one changed 21. No audit changed a rule or a tool. An audit of the rule text on 2026-11-07 found 14 rule lines with 29 quoted sentences that no tool or reviewer enforced. The counts, the commands and the ledger lines are in [docs/evidence.md](docs/evidence.md). The same page holds two larger cases. A landing page kept 5,570 dead lines of 6,487. A document used 23 % of its 184 sources.

## The pilot and version 1.1

A pilot ran 10 SWE-bench Verified tasks with one model, under this method and without it. The record is in `benchmark/swe-verified/`. Without the method the agent claimed 9 fixes and the hidden tests confirmed 7. Under the method it claimed 0 and the tests confirmed 1. The room logs of those 10 runs hold 473 refusals. 191 of them read «the planned queue is empty, a planning unit comes first». 70 hold «no planned block» and 14 hold «names no leaf move». None of the three texts said what would pass. In 4 of the 10 runs no unit closed. In one run 3 units closed with no reviewer pass.

Version 1.1 answers those counts with five changes.

- Each of the three refusal texts ends with the call or the text that passes.
- `room.py --accept` writes the first leaf, its measure step, its pilot step and the planned measure unit. The first call of a new author opens that unit.
- Close reads the review verdict from the reviewer's file. The pre-commit refuses a status word turned closed by hand.
- The baseline test refuses a clause that exits 127 or 124 on the clone of HEAD. A missing command or a timeout is no red baseline.
- `RULE.md` §8 sets the entry of a gate, its six tests and the review of every gate at each 50-unit boundary.

No task has run under version 1.1 at this commit.

## Why

The author works under this method every day. It keeps work in small, reviewed units and records what failed. It also shows where it falls short. Every failure in the record had one shape. The loop closed on a signal the agent had produced itself. A check that exits zero, a block marked closed, a report sent. Agents add checks nobody asked for. They bypass or game those checks, then report the work complete. One document was delivered with 23 % of its sources used. In the pilot the method's own refusals stalled the agent. One run met 109 refusals, and 76 of them repeated one text that never said what would pass. So version 1.1 keeps its gates to a reasoned minimum. Each refusal names the form that passes. Each gate must stop a planted fault, with a reference from outside the thing it tests. Every 50 units all gates take those tests again, and duplicates merge.

## Changes from the private folder

Owner quotes, personal paths, references to other rooms, the report page and the owner ledgers of the rule room left. The internal name changed from unit100 to hectoline. `base.py` stays because `unit.py` imports it. Two never-called selftest functions left. Two selftest cases that compared against older close texts now compare against the current ones. The built-in self-measures of the private rule room left with its goal table. A room computes its leaves in its own `measures.py`. Version 1.1 is the cut of the private room at its unit U0561. Eight modules entered with it: admission, eligibility, pile, reconstruction, reconstruction_flow, review_evidence, selftest_flow and selftest_roads. `gates.py` reads the tool code of its own folder. `audit.py` finds its modules through the room link. Two selftest cases bound to the private room left. The third-fail case runs on a fresh room, because the pre-commit now refuses a block closed by hand.

## License

MIT, Il Woong Park.
