# U0004 r1

model claude-opus-5 · session 8df38a63-d721-40e3-91f0-b10981eec29f · turns 15 · wall 168.3 s · exit 0

## Answer

I ran every clause and verified each key against the files it names.

**Product read first** — `tests/delete/test_combined_fast_delete.py` (20 lines, one class, one case): creates `Origin`/`Referrer`/`SecondReferrer` at base definitions (`tests/delete/models.py:135,139,145`, both FKs `CASCADE`, the second via `to_field='unique_field'`), then asserts 2 queries around `referrer.delete()` and the two rows gone. No skip, no term before its home, no repeat, no seam. facts: `SecondReferrer` reaches `Referrer` through `referrer_id` and `other_referrer_id`; the delete issues one DELETE per foreign key today; `P11` in PRODUCTS.md already declares this file.

**Check clauses, run by me**
- `grep -q 'def test_one_query_per_related_table' …` → 0 here; 2 on the clone of `0c9c7d8` (file absent).
- `… measures.py delete.test_combined_fast_delete | grep -q '3 queries executed, 2 expected'` → 0 here; 1 on the clone (module missing → error, not 127/124). Here the case prints `AssertionError: 3 != 2 : 3 queries executed, 2 expected` with exactly three DELETE statements — two on `delete_secondreferrer`, one on `delete_referrer`. The second clause runs the case, so it proves the outcome the sentence claims, not merely that text exists.

**Keys** — `duplicate`: `git grep -c "assertNumQueries" 0c9c7d8 -- tests/delete` prints `tests.py:20`, true. `modify?`: `tests.py` is 584 lines at base, true. `base`: U0003 is closed at `0c9c7d8`, true. `files`: test file 20 ≤ 25, UNITS.md 16+2=18 ≤ 22. `lines`: 38 added+modified ≤ 45 and ≤ 100. `result`: confirmed independently, including `measures.py --g1` → `1 of 2`. `approval`: verbatim against the A0001 row. The diff touches only the test module and the ledger, so it stays behind the S03 interface (query count exposed, the fields that reach the table hidden) and adds no refusal site to the product.

Two notes, each correctable by one command and neither a fail grade: PLAN.md keeps S03 at `todo` while its first unit is open, and the `cause` key calls this the result layer while PRODUCTS.md P11 is declared state. The §6 paraphrase in `cause` is loose — this case is red by design rather than a behavior-as-it-stands recording — but `rejected`, `added` and `result` all state that plainly and consistently with U0002's CASES, so the record is honest.

VERDICT: pass — every clause exits 0 at this tree and non-zero on the clone of 0c9c7d8, the running case proves the three-query cascade the sentence names, and each key is true against the files it cites.

R1 PASS
