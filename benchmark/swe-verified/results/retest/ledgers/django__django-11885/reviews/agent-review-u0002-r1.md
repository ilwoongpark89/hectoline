# U0002 r1

model claude-opus-5 · session bf4b0c55-2df4-483d-a993-097e992287bb · turns 12 · wall 272.0 s · exit 0

## Answer

I ran every clause of the check key and verified each field against the tree.

**Check key, at this tree** (in `repo/`):
- `grep -q '^def g1' measures.py` → 0
- `python3 -B measures.py --g1 | grep -qE '^[0-9]+ of 2$'` → 0, printing `1 of 2`
- `grep -q '| G1 |.*| 2 of 2 | 1 of 2 |' GOAL.md` → 0

**Baseline** (`git archive ec02d49` into a fresh dir, no change to the repo): the three clauses exit 2, 1, 1 — all red, none 127 or 124. `measures.py` is absent at `ec02d49` and the base `GOAL.md:18` reads `| all | no tool |`, so clause 3 is red for a real reason, not a missing file.

**Fields.** `duplicate`: `git grep -c "def g1" ec02d49 -- '*.py' | wc -l` prints `0` ✓. `approval`: matches the A0001 quote in OWNER.md verbatim ✓. `plan`: A0001 and S02 both exist; S02's product P10 is the `measures.py` row already in PRODUCTS.md ✓. `files`: `measures.py` is exactly 49 lines; GOAL.md:18 and PLAN.md:10 are the two changed rows; the U0002 block occupies UNITS.md:24-43 ✓. `cause`/`result` claim "the delete suite green, the combined fast delete case not written yet" — I reproduced g1's probe: the selected pair is `/usr/bin/python3` with `/tmp/hl-deps`, where `delete.tests` exits 0 and `delete.test_combined_fast_delete` exits 1, and `tests/delete/` holds only `__init__.py`, `models.py`, `tests.py`. True field, and `1 of 2` is that count, not a typed number.

**Product read.** `measures.py` parts each have one home: the module docstring states the three invocation modes; `g1` the count or the no-tool reason; `run` one subprocess exit code; `case` one label on an in-memory sqlite database; the `__main__` guard the dispatch. `not run(...)` counts exit 0 as green correctly, and a missing module label lands as a failure, so the red case cannot read green. No write leaves the copy: `:memory:` database, `-B` and `PYTHONDONTWRITEBYTECODE`. The diff touches only `measures.py` and the three ledger rows the block names — no django product file — so it stays behind the S02 interface "the count of G1 · the probe commands", exposing `g1` and hiding `PYS`, `DEPS` and the probe.

**One note, not a fail grade.** The `lines` key reads `+67 ~2 −3 moved 0, by numstat at close`, but `git diff --numstat ec02d49` (excluding the tool-written `unit.log`) gives `measures.py 49/0`, `GOAL.md 1/1`, `PLAN.md 1/1`, `UNITS.md 19/4` — 70 added, 6 deleted, and no line in the diff is deleted without a replacement, so `−3` is unsupportable under any reading and the closest true rendering is `+68 ~2 −4` (or `+64 ~6 −0`). RULE §4 classes a wrong count that one command corrects, and whose correction changes nothing of the product or the plan, as a note: added plus modified is 69 or 70 either way, well under the cap of 100. Correct that key with the numstat output before close.

`/tmp/hl-deps` carries the third-party lines the rejected key declines to vendor, and the file never says so; the author may want one word in the docstring. That is style, and it fails nothing.

VERDICT: pass — every clause exits 0 at this tree and red at ec02d49, each field is true against the files, and the only defect is the `lines` count, a note-grade slip that one numstat command corrects.

R1 PASS
