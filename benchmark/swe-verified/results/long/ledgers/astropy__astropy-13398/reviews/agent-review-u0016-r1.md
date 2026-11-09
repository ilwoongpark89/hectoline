# agent-review-u0016 r1

model claude-opus-5 · session 4a4e2c9d-4b3a-4dbb-a21a-ad7cb97ce9ef · turns 11 · wall 312.7 s · exit 0

## Answer

All five check clauses verified at the working tree and at the base commit:

| clause | at base `0c5e7a5` | at tree |
|---|---|---|
| U0017 sentence line | 1 | 0 |
| `base       : U0016` | 1 | 0 |
| S06 … `U0015 | done` | 1 | 0 |
| status `G1 … 4 of 4` | 1 (base shows `3 of 4`) | 0 |
| status `G0 … 1 of 1` | 1 (base shows `0 of 1`) | 0 |

Fields verified against the repo:
- `git diff --numstat`: `PLAN.md 1 1`, `UNITS.md 42 0` → lines key `+42 ~1 −0`, 43 ≤ 100, and result key `PLAN.md +1 −1 · UNITS.md +42 −0` both hold.
- `git diff -U0` hunks: `@@ -14 +14 @@` PLAN.md and `@@ -295,0 +296,42 @@` UNITS.md → files key `PLAN.md:14 · UNITS.md:296-337` is exact.
- Duplicate key reproduces: planned `→ 0`, todo `→ 0`, `· audit ·` `→ 2` (U0013 header line 234 plus its mention at line 239) — the gloss is true.
- Approval quote matches the A0001 row in OWNER.md verbatim; base `U0015 closed, commit 0c5e7a5` matches `git log`; status `open` is in the set.
- Rejected-key count checks out: 15 finals at close minus the one audit U0013 = 14 non-audit finals, so the twenty audit is not the trigger; `unit.py status` now prints `progress 100 %`, G0 `1 of 1` and G1 `4 of 4`, so RULE §4's "once when the goal checks are met" is the trigger the cause key names.
- Diff touches only PLAN.md, UNITS.md and the tool-written `unit.log` — no product code, so a §3 planning unit with `S none` stays behind its interface, matching the closed precedent U0014.

Two notes that are style, not grade: the files key omits the `unit.log` range that U0014 listed, and clause 3 pins `done` rather than accepting open-or-done — but pinning `done` is what makes it fail at base, which the stronger rule requires.

VERDICT: pass — every check clause fails at base 0c5e7a5 and exits 0 on the tree, and each reported count, range and quote reproduces from the repo inside the ledger-only interface of a §3 planning unit.
