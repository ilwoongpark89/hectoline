# U0007 r1

model claude-opus-5 · session f91ad885-c5e0-4397-9280-a9a98459e83f · turns 16 · wall 204.8 s · exit 0

## Answer

## Review of U0007

**facts read from the product:** PLAN.md now carries S06 under G1 on P11 with the interface two lines and U0008 todo; «Order» rank 1 is U0008 under S06, rank 2 the audit of RULE §4; GOAL.md shows G1 target 5 of 5, baseline 5 of 5, G0 1 of 1.

What holds:
- All three check clauses exit 0 in the working tree and exit 1 against `git show 78385cd:PLAN.md` (no clause passes at the base).
- The duplicate key is true: `git grep -c "refs_window\|refs_subquery" 78385cd -- django` and `git grep -c "contains_over_clause" 78385cd -- django/db/models/sql/query.py` both give 0 hits.
- The fault is real and is the one U0006 left: `Book.objects.annotate(w=Window(Avg("pages"), partition_by=F("publisher"))).aggregate(Sum("w"))` raises `OperationalError: misuse of window function AVG()`. The U0006 diff replaced the `existing_annotations` subquery trigger with `has_existing_aggregation`, and a `Window` carries `contains_aggregate` false, so the subquery is lost. The crash text in «Order» is verbatim.
- Product diff empty, no untracked files, approval quote verbatim against the A0001 row, planned U0008 holds the five keys of a planned block, S06 names its leaf move (G1 from 5 of 5 to 5 of 5).

The fault:
- `PLAN.md:22` (the «Order» section, rank 1 and rank 2) puts a due audit second. `python3 -B measures.py g1` prints `G1 5 of 5` and GOAL.md targets are 5 of 5 and 1 of 1, so every goal check is met; `grep -nE '· audit ·' UNITS.md` finds no audit unit, so the audit RULE §4 makes due "once when goal checks are met" has never run. The base PLAN.md itself stood it at rank 1 as due, and this block calls it "the due audit" twice. RULE §2 says "A due audit stands first, then the most basic cause", and RULE §3 says "A due audit still comes first" with "An audit due" as rank two of five, overridden by nothing but a redesign forced by a fail — an explicit owner order overrides only the last two ranks, so A0001 does not lift S06 over it. The planned U0008 takes base U0007, so the queue this plan draws opens the repair ahead of the audit. The rejected key states RULE §2 correctly and then overrides it by argument; RULE §4 admits a change to the method only as an A row or an audit finding, and neither was taken. This is the unit's central decision in the home it touched, not a style note.

VERDICT: fail — the «Order» the unit rewrites puts the due goal-checks-met audit at rank two behind U0008, against RULE §2 "A due audit stands first" and RULE §3's rank two, with no A row or audit finding permitting the deviation.

R1 FAIL
