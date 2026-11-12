# U0005 r1

model claude-opus-5 · session 359be019-ef4a-47cd-8cb9-2f77afde9232 · turns 15 · wall 157.3 s · exit 0

## Answer

Verification done. Results:

**Check clauses** (run in the room repo)
- Clause 1 → exit 0 with the unit; exit 1 on a clean export of base `3eb3825` (`AttributeError: 'Func' object has no attribute 'get_refs'`).
- Clause 2 → exit 0 with the unit; exit 1 at the base (`WhereNode` has no `get_refs`).
Both clauses call the added definition and assert its value, so they prove the sentence's outcome, not mere text presence, and neither passes at the base.

**Keys against the files**
- `duplicate`: `git grep -n "get_refs" 3eb3825 -- django` → 0 hits, confirmed; HEAD is `3eb3825`, so the base key is true.
- `files`: `django/db/models/expressions.py:431-435` and `:1169-1170`, `django/db/models/sql/where.py:190-194` all land exactly on the added defs; `PLAN.md:12,18-20` matches the S04 row, the «Order» item and the closing paragraph; the U0005 block is `UNITS.md:87-106` (+ the blank 107).
- `result`: the suite claim reproduces exactly — `Ran 924 tests`, `failures=3`, and the three are `test_unreferenced_*_pruned`, the U0004 acceptance tests red at the base. Pure addition to django (+15, −0), no caller added, so no behavior change.
- Step interface: S04 exposes "the refs of an expression", hides "the walk over its source expressions"; P13 is declared over both `expressions.py` and `where.py` in PRODUCTS.md, so the `WhereNode` method stays inside the step's product.
- `rejected`, `split`, `deleted`, `cause`, `split?`, `tidy-first?`, `modify?`, `delete?` all hold against the diff; status `open` is in the set; the approval quote matches the A0001 row cited in the earlier blocks.

**Note, not a fail grade** (RULE §4, a wrong count one command corrects): the `lines` key reads `+22 ~3 −0`, but by the room's own numstat convention — adds minus deletes, excluding `unit.log` (verified against U0003 `+56 ~1` and U0004 `+67 ~9`) — the tree gives adds 37 (PLAN 4, UNITS 18, expressions 9, where 6), deletes 9, i.e. `+28 ~9 −0`. Still far under the 100 cap, and it changes nothing of the product or the plan; the author recomputes it at close.

VERDICT: pass — every check clause exits 0 with the unit and non-zero at base 3eb3825, the nine verdict keys and the files ranges are true of the diff, and the three added methods stay behind the S04 interface with no behavior change (924 tests, only U0004's three base-red acceptance tests fail), leaving only a correctable `lines` numstat count as a note.

R1 PASS
