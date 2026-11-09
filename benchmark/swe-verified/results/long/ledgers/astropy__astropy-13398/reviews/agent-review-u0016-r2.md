# agent-review-u0016 r2

model claude-opus-5 · session acef880f-c3f9-4e84-8238-65d1f9ae80ff · turns 19 · wall 392.5 s · exit 0

## Answer

All five check clauses verified by me directly.

**Check key, run at the tree and at base `0c5e7a5` (fresh read-only clone):**

| clause | tree | base |
|---|---|---|
| U0017 sentence line in UNITS.md | 0 | 1 |
| `base       : U0016` | 0 | 1 |
| S06 row `… U0015 \| done` in PLAN.md | 0 | 1 |
| `unit.py status` → `G1 … 4 of 4 \| 4 of 4` | 0 | 1 (base prints `3 of 4`) |
| `unit.py status` → `G0 … 1 of 1 \| 1 of 1` | 0 | 1 (base prints `0 of 1`) |

No clause passes at the base, so `result : check exits 0 0 0 0 0` holds and the baseline is red.

**Fields reproduced from the repo:**
- `git diff --numstat` → `PLAN.md 1 1`, `UNITS.md 42 0`; lines key `+42 ~1 −0`, 43 ≤ 100, result key `PLAN.md +1 −1 · UNITS.md +42 −0` — both exact.
- `git diff -U0` hunks `@@ -14 +14 @@` and `@@ -295,0 +296,42 @@` → files key `PLAN.md:14 · UNITS.md:296-337` is exact (296+42−1 = 337).
- duplicate key reproduces at `0c5e7a5`: planned `0`, `| todo |` `0`, `· audit ·` `2`.
- base `U0015 closed, commit 0c5e7a5` matches `git log`; status `open` is in the §2 set; approval quote matches the A0001 row of OWNER.md verbatim.
- rejected count holds: 13 non-audit finals now, 14 at close of U0016, so the twenty audit is not due; `status` prints `progress 100 %`, G0 `1 of 1`, G1 `4 of 4`, which is the §4 "once when the goal checks are met" trigger the cause key names. S06 is legitimately `done` — its one unit U0015 is closed and its number moved.
- clauses 4 and 5 prove an outcome (the measure moved), not merely that text exists; clauses 1–3 pin the ledger rows that are this unit's product and grep no planned status and no own status.
- the working tree touches only PLAN.md, UNITS.md and the tool-written `unit.log`; no product file changes, so the ledger-only interface of a §3 planning unit holds.

Two weak-style points, neither a fail grade: the files key omits the `unit.log` range that U0014 and U0015 listed, and the r1 review log is 27 lines against the 20 of §4 — a reviewer-side cap, not one of the nine grades.

VERDICT: pass — every check clause fails at base `0c5e7a5` and exits 0 on the tree, and each reported range, count and quote reproduces from the repo while the diff stays inside the ledger-only interface of a §3 planning unit.
