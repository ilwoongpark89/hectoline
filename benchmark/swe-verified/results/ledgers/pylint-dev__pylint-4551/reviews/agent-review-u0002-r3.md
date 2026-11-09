# agent-review-u0002 r3

model claude-opus-5 · session 2bf8d22b-8ee4-4822-b0bf-0ab2f6995559 · turns 8 · wall 154.8 s · exit 0

## Answer

Checks run and evidence gathered:

- `python3 -B unit.py status . | grep -q '^| G1 '` → exit 0 now; at base `git show c1bf708:GOAL.md | grep -c '^| G1 '` → 0, so the clause does fail at base.
- numstat matches the `lines` key (GOAL 1, PLAN 1, PRODUCTS 2, UNITS 63 = +67).

Two fail-grade findings:

1. **The change is not what the sentence says, and the check does not prove its outcome.** The sentence claims "the pilot step of this room stands in the plan under the leaf it moves." The room's own tool disagrees: `measure.py:49` computes `pilot = 0 if any('pilot' in s[3] for s in steps) else 1`, and `unit.py status` still prints `| no pilot step | 1 |` after this diff — S02's step text reads "moves G1 from 0 of 3 to 3 of 3, the measure of G1 stands in measures.py" and never names a pilot, and its parent is G1 while §3 puts the pilot as the first step under G0. The single check clause greps the **G1 goal row of GOAL.md** out of the status print; it says nothing about PLAN.md, S02, or a pilot, so it proves only that a row of text was added, not the outcome the sentence asserts (RULE §2, "a check that only proves that text exists is not a check").

2. **The diff leaves the interface of its step.** The `plan` key is `A0001 · S02`, and PLAN.md lists U0002 as S02's first unit, but S02's product is P11 (`pylint/pyreverse/utils.py · inspector.py · diagrams.py`) with interface "the hint of an attribute · the inference under it." The diff touches no product of S02 at all — only P02/P04/P05/P06 ledger rows — and it is the diff that creates the S02 row it claims to stand under, contradicting the §2 line the block's own `cause` key quotes ("the step with its interface stands before the first unit of the step opens"). Planning work of this shape carries `S none` under §3; as written the `plan` field is false against the diff, which is r2's finding unfixed.

Secondary (not the basis of the verdict): `duplicate` carries no command and no count written by the script that ran it, as §2 requires; GOAL.md's G1 measure and PRODUCTS.md P10 both name `measures.py`, which does not exist (status lists it under "not found", and G1's now column reads "no tool").

VERDICT: fail — the check greps only the added G1 goal row and never the plan, while the room's own measure still reports "no pilot step 1" and the diff touches no product of the S02 step it claims.
