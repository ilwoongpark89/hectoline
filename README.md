# hectoline

The 100-line unit method for work with coding agents. One open unit at a time. At most 100 added or modified lines per unit. One check that fails before the unit and passes after it. One independent review. One commit. An audit every ten units. Hooks deny every edit outside the open unit.

The rule is `RULE.md`. The gate is `unit.py`. The ledgers are six Markdown files in each room. This repository is the public version of the folder that has run the author's projects since 2026-10-31.

## Quick start

```sh
git clone <this repository> hectoline && cd hectoline
python3 -B example/build.py /tmp/rooms
python3 -B unit.py selftest /tmp/rooms/01_pressure-drop
python3 -B unit.py status /tmp/rooms/01_pressure-drop
python3 -B room.py 02_myroom "the outcome in one sentence" "the owner line" --top /tmp/rooms
```

Requirements: macOS with `sandbox-exec`, git with a user name and email, Python 3.11 or later. The close step clones the room and runs each check clause in a write-denied sandbox. Rooms live beside this folder by default. The variable `HECTOLINE_ROOMS` names another folder.

## Rooms and ledgers

A room is a folder with six ledgers and its own git repository. `OWNER.md` holds the owner statements, the A rows. `GOAL.md` holds the goals, the G rows, each with one measure and a target. `PLAN.md` holds the steps, the S rows. `UNITS.md` holds the units, the U blocks. `PRODUCTS.md` holds the product tree, the P rows. `RESEARCH.md` holds the source claims, the R rows. The chain is one way: A → G → S → U → P. A row without a parent in the layer above cannot exist. `room.py` makes a room with links to the rule and the tools in this folder.

## The unit life cycle

1. Open. `unit.py open U#### ROOM sentence plan files lines` appends the block or turns a planned block open. The block exists before the first edit of any file it names. Open prints the unit pack: the leaf, the step, the owner quotes and the last units on each file.
2. Check. The check key holds shell clauses. Each clause must exit non-zero on a copy of HEAD and zero after the unit. A clause that passes at the base is refused.
3. Review. A second session reads the diff and the nine verdict keys and writes its log. The review key records every round. The third failed round ends the unit and reverts its lines.
4. Close. `unit.py close U#### ROOM` reruns the check and runs the baseline. It counts the lines from the staged tree and commits under the unit number. Every count in the block is the output of the command, never typed.

## The audit

After every tenth unit, `unit.py open` accepts only an audit unit or one planning unit. `audit.py N ROOM` reruns every closed check on a copy of the room. It lists piles, duplicate lines, unused definitions, steps without a move and goal leaves without a unit. At 100 units the audit remeasures the goal table and lists the restructuring.

## The hooks

`hooks/install.py` installs three gates. Claude Code hooks call `unit.py check` before and after each edit and deny with exit 2. Codex hooks deny with a permission decision. The git pre-commit runs validate and pile and lets only `unit.py close` commit. A pile is a line that no unit block names. A pile blocks the commit and the end of the turn. The hooks also deny `--no-verify`, a changed hooks path and a write to the log. A web search outside a research unit is denied too.

## The example

`example/01_pressure-drop/` is the snapshot of one run of `example/build.py`. Every change after the bootstrap entered through `unit.py open` and `unit.py close`. The tool wrote every block. The pre-commit hook ran on every commit. The room holds six units. They are the bootstrap, a planning unit, the measure, a second planning unit, the calculator and one audit. The goal leaf G1 moved from unmeasured to 1 to 0. The audit output is `audits/audit-06.txt`. Its check rerun shows one state-bound clause: the measure unit asserted g1 at 1, which turned false when the calculator entered. The reviews in `example/reviews/` were written by the session that built the room. They show the form of a review, not an independent one.

## The measured failure

The method was audited on its own room between 2026-11-05 and 2026-11-07. The rule file held 104 lines, under its 500-line cap. One of those lines held 23 sentences. Four audits ran on schedule. Three of them changed 18 lines of their own ledger and one changed 21. No audit changed a rule or a tool. An audit of the rule text on 2026-11-07 found 14 rule lines with 29 quoted sentences that no tool or reviewer enforced. The counts, the commands and the ledger lines are in [docs/evidence.md](docs/evidence.md). The same page holds two larger cases. A landing page kept 5,570 dead lines of 6,487. A document used a quarter of its 184 sources.

## Why

Every failure in the record had one shape. The loop closed on a signal the agent had produced itself. A check that exits zero, a block marked closed, a report sent. The rule was kept to the letter. A gate on the form of work does not reach the work. The next step puts a reviewer in front of the product instead of the diff. Then each signal is scored by how often it agrees with a ground truth the agent cannot produce.

## Changes from the private folder

Owner quotes, personal paths, references to other rooms, the report page and the owner ledgers of the rule room left. The internal name changed from unit100 to hectoline. `base.py` stays because `unit.py` imports it. Two never-called selftest functions left. Two selftest cases that compared against older close texts now compare against the current ones. The built-in self-measures of the private rule room left with its goal table. A room computes its leaves in its own `measures.py`.

## License

MIT, Il Woong Park.
