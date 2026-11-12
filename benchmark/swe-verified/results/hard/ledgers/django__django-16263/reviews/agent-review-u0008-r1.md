# U0008 r1

model claude-opus-5 · session e485d590-228f-48d2-8fed-9f0068d1efac · turns 20 · wall 161.3 s · exit 0

## Answer

I ran every clause myself and read the product in the home it touched.

**Check clauses — base aba6110 (extracted to a clean tree) vs working tree**
- Clause 1 (window): base → `OperationalError: misuse of window function AVG()`, grep exit 1; now → `2`, exit 0. Real error, not 127/124.
- Clause 2 (Subquery annotation): base → `2`, grep -qx 3 exit 1; now → `3`, exit 0.

**Product**
- The two terms enter the one wrapping decision of `get_aggregation` (`query.py:465-475`, `489-490`), beside `has_existing_aggregation`, reading `aggregate.get_refs()` from U0005 — behind the S06 interface («the test that asks a summary query for its subquery · the refs of its aggregates»), no new home.
- Outcome, not just select counts: `Sum` over the window annotation returns 300.0 for two 100/200-page books (avg 150 per row), plain `F` annotation and a bare `Count` are unchanged.
- `aggregation aggregation_regress annotations expressions_window` 333 tests OK, `queries expressions aggregation_regress` 721 tests OK; `measures.marks` still 5 of 5 for G1.
- `isinstance(annotation, Subquery)` matches the upstream attribute's reach (`Exists` is a `Subquery` subclass; checked), and the `contains_over_clause` default mirrors the `contains_aggregate` line above it.

**Keys**
- `duplicate`: `git grep -c "refs_window\|contains_over_clause" aba6110 -- django/db/models/sql/query.py` → no output, exit 1, i.e. 0 hits as written.
- `base`: U0007 is `closed` at line 129 and aba6110 is its commit.
- `approval`: verbatim against `OWNER.md:7` A0001.
- `files`/`lines`: query.py +13 insertions only (≤20, no line with earlier owners modified), PLAN.md 4 changed (≤4), UNITS.md 18 (≤26).
- `rejected` holds: nested `Coalesce(Subquery(...))` inlines without error, so leaving the deeper walk out carries no case of this fault.
- PLAN.md S06 → done and «Order» redrawn with the due audit at rank one, matching the added key. No test file in this unit; the diff adds no refusal site, so §8's six tests do not apply.

VERDICT: pass — both clauses are red at base aba6110 and green now, the change is exactly the two-term wrapping test the sentence names inside S06's interface, and every verdict key is true of the files I read.

R1 PASS
