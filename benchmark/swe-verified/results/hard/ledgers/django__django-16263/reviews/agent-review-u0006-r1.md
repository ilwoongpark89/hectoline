# U0006 r1

model claude-opus-5 · session 8b9c1673-ec49-4fd7-b26e-12256c61e429 · turns 18 · wall 144.2 s · exit 0

## Answer

Review complete. What I ran and verified in `repo`:

**Check clauses** (all three, exit 0 with the unit):
- `python3 -B measures.py g1 | head -1 | grep -qx 'G1 5 of 5'` → 0
- `... grep -qx '  test_unreferenced_annotation_pruned pass'` → 0
- `... grep -qx '  test_referenced_group_by_annotation_kept pass'` → 0

**Baseline** (`git archive 44b319f` into a clean tree): `G1 2 of 5`, with `test_unreferenced_annotation_pruned fail` and `test_referenced_group_by_annotation_kept fail` — all three clauses red at base, none exits 127/124.

**Clauses prove the outcome, not text existence**: `tests/aggregation/tests.py:2090` asserts `sql.count("select") == 1` and `full_name` absent; `:2129` asserts `pages_mod` present and `mod_count` absent in the count SQL.

**Keys against the files**
- duplicate: `git grep -c "existing_annotations" 44b319f -- django tests` → `django/db/models/sql/query.py:3`, one file — true.
- result counts: `git diff --numstat HEAD` → GOAL.md 2/2, PLAN.md 3/3, UNITS.md 17/3, query.py 51/14 — every count matches; 51 added ≤ the 100 cap and the `:≤55` budget.
- cause key's two SQL claims reproduced verbatim: `SELECT COUNT(*) AS "__count" FROM "aggregation_book"` and the subquery keeping `pages_mod` in its `GROUP BY`.
- approval quote matches `OWNER.md:7` A0001 verbatim; status `open` is in the set; deleted key's comment quote is in the base text.

**Product read** (`get_aggregation`, django/db/models/sql/query.py:438–560): the whole change sits inside that one function — `has_existing_aggregation` from aggregate annotations plus `having`, `qualify` added to the subquery test, the inner annotation mask from aggregates + refs of group by/aggregates/having, and the inline-plus-mask in the plain branch. It stays behind the S05 interface ("the annotations a summary query carries · the mask with the subquery"); no second home, no helper added.

**Regression**: `aggregation aggregation_regress annotations expressions_window` → 333 tests OK (10 skipped); `queries expressions expressions_case lookup ordering filtered_relation db_functions prefetch_related` → 1358 tests OK (39 skipped, 3 expected failures).

One note, not a fail grade: GOAL.md's `baseline` column was overwritten with the current number (0 of 5 → 5 of 5) rather than kept as the pre-work value, which U0004 did not do for its own move; the written number is nonetheless the true output of the named measure command.

VERDICT: pass — every check clause exits 0 with the unit and is red at base 44b319f, all nine verdict keys and the counts are true of the diff, and the change stays inside `get_aggregation` behind the S05 interface with no regression across 1691 related Django tests.

R1 PASS
