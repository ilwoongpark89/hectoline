# U0004 r1

model claude-opus-5 · session 86fed8a7-99e1-4408-9fef-6cef0d8f352b · turns 15 · wall 229.5 s · exit 0

## Answer

**Review of U0004**

Check key, run in the room:

| clause | working tree | base 0a3ea0e (fresh clone) |
|---|---|---|
| `… head -1 \| grep -qx 'G1 2 of 5'` | 0 | 1 |
| `… grep -qx '  test_unreferenced_annotation_pruned fail'` | 0 | 1 |
| `… grep -qx '  test_referenced_group_by_annotation_kept fail'` | 0 | 1 |

Measure output with the unit: `G1 2 of 5`, with `test_unreferenced_annotation_pruned fail`, `test_unreferenced_aggregate_annotation_pruned fail`, `test_unused_aliased_aggregate_pruned pass`, `test_referenced_aggregate_annotation_kept pass`, `test_referenced_group_by_annotation_kept fail`. At the base: `G1 0 of 5`, all five missing. The result key is exactly that — three red over the annotations TASK.md names, two green guards. No clause passes at the base.

Keys verified: `duplicate` — the grep gives 2 hits, tests.py:541 is `test_count_star` reading the SQL of `aggregate(n=Count("*"))`, tests.py:1033 reads `"for update"` of a select_related aggregate; neither reads a count query's annotations. `approval` — «Fix the issue in TASK.md in this repository» is verbatim in the A0001 row of OWNER.md. `files` — 33-43 is exactly the `functions` import block that gained `Concat` and `Mod`, 2089-2138 is exactly the appended block in a 2138-line file, PLAN.md:11,18-20 and UNITS.md:66-86 match. `base` — U0003 is closed at 0a3ea0e. The diff touches only the test file and the ledger files, so the §4 test-file rule holds, and the cases stay behind the S03 interface: they read emitted SQL and use the models `AggregateTestCase` already loads, no product code.

Notes, not fail grades, for the author to correct:
- `lines : +51 ~5 −0` does not come out of numstat under the convention U0003 used (non-log files, adds minus dels): numstat now reads tests.py 52/0, PLAN.md 5/4, UNITS.md 19/5, i.e. +67 ~9. §4 calls a wrong count a note; no reading comes near the 100 cap.
- The unit rewrote the S03 row's expected move to 0→2 of 5, which is true, but left S04 and S05 reading «G1 from 0 of 5», contradicting the new Order line that has U0006 going 2 of 5 → 5 of 5.
- The check binds four of the five cases (two through the `2 of 5` total, two pinned red); `test_unreferenced_aggregate_annotation_pruned` is the one case no clause would catch if it went missing.

VERDICT: pass — every clause exits 0 with the unit and 1 at 0a3ea0e, the nine verdict keys are true of the files, and the five cases stay behind the S03 interface, leaving only a one-command line count and two stale step baselines as notes.

R1 PASS
