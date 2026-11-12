# U0003 r2

model claude-opus-5 · session 99459353-ff62-4967-bab7-018236c02613 · turns 12 · wall 152.0 s · exit 0

## Answer

I ran every clause and verified the keys. Here is what I found.

**Checks (all run):**

| clause | with unit | at d144671 |
|---|---|---|
| `grep -qE '^\| S05 \| G1 \| P11 \|.*pilot.*0 of 5 to 5 of 5' PLAN.md` | 0 | 1 |
| `grep -qE '^\| P11 \| the summary query of django' PRODUCTS.md` | 0 | 1 |
| `sed -n '/^## Order/,$p' PLAN.md \| grep -q '^1\. U0004 under S03'` | 0 | 1 |

The `result` key is true: 0 0 0 with the unit, 1 1 1 at the base. No clause passes at the base.

**Keys that verify true:** `duplicate` reproduces exactly (`django/db/models/query.py:1`, `django/db/models/sql/query.py:16`, 2 files). `lines` matches numstat (PLAN +10 −1, PRODUCTS +5 −0, UNITS +42 −0 → +56 ~1 −0, 57 ≤ 100). `files` ranges are now exact (UNITS.md 45–86 against an 86-line file; PLAN.md 11–20 against a 20-line file). `approval` quotes the A0001 row verbatim. `rejected` is true of the files — `Query.exists` does call `clear_select_clause()` at `django/db/models/sql/query.py:569`, and `get_refs` does not yet exist in django. `deleted` correctly names the bootstrap S03 row. The review log digest matches: `f47c5d38…9127b`.

**The fault.** `unit.log` records this sequence:

- `00:28:58` — the r1 review log and `u0003.json` are written, verdict pass.
- `00:29:04` — `close | U0003 | deny | ... S03 names no leaf move in its text, RULE §2: write «G1 from its number to its number» in the step text`.
- `00:29:14` — PLAN.md is edited (two `check | PLAN.md in U0003` lines; PLAN.md mtime is `00:29:14`).

So `PLAN.md:11` — the S03 step text, now reading `G1 from 0 of 5 to 0 of 5` — was changed **after** the only review round passed, in answer to a tool refusal. r1 never read the S03 row that stands now; its log describes S03 only as "S03/S04/S05 with products P12/P13/P11" and its clause table covers S05, P11 and the Order rank. No check clause binds S03 either, as r1 itself noted as debt, so nothing in the check catches the edit.

RULE §4 lets an author correct a wrong count or pointer after a pass line only when "the correction changes nothing of the product or of the plan" — the files-range fix r1 asked for qualifies, this one does not: a step's text is the plan. The block still carries one round. Under §4 a field that reports a review of something that was not read stays a false field, so the `review` key is false for the product as it now stands. This is a correctable fault — an r2 round over the current PLAN.md would resolve it — but it cannot be waived by me.

VERDICT: fail — the S03 step text in PLAN.md was changed at 00:29:14 in answer to the close deny at 00:29:04, after the r1 pass line was written at 00:28:58, so the single review round in the review key read a plan that no longer stands and no check clause binds that row.

R2 FAIL
