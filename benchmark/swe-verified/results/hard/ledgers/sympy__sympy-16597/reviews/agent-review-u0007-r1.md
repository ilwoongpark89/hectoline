# U0007 r1

model claude-opus-5 · session f2c25ba4-f924-453a-95cd-f0bfba0aad0f · turns 23 · wall 321.0 s · exit 0

## Answer

I ran every clause and the block's factual claims. Full record:

**Product read (the plan with its «Order»)** — facts: S05 names P12 (`sympy/core/tests/test_assumptions.py`, 1064 lines) with the interface "the value each case records · the rule that derives it"; `measures.py` reads g1 `3 of 3` and g2 `0 of 2`; the working tree touches only `PLAN.md`, `UNITS.md`, `unit.log` — no product file.

**What holds**
- Both clauses green now (exit 0, 0) and red at base `1c8811f` (exit 1, 1), neither 127 nor 124.
- `duplicate`: `git show 1c8811f:PLAN.md | grep -c 'U0008'` → `0`, as written.
- The Order line's substance is true and corrects U0005's wrong "derives False": at HEAD the first failures are `oo.is_integer is None` (line 101) and `mm.is_integer is None` (line 128), and the rules now derive values for exactly integer, rational, noninteger, irrational, even, odd on both, plus composite on `oo` — 13 lines, matching U0008's `≤14` budget. `algebraic`/`transcendental` stay `None` and are correctly left out.
- `rejected` reproduces: 6 final units (first audit at 10), no failed unit, g1 3 of 3, g2 0 of 2, no unmeasured leaf, and U0005's rejected key does give the adopted-upstream-file reason for P12 that this block cites. `gates.py` exists in the rule room reached by the `RULE.md` link, and the diff adds no code, so "no refusal site" is true.
- `approval` quote matches OWNER.md A0001 verbatim; base, status, budgets, and the queue-empty ground for «S none» all hold.

**The fault**

Check clause 1 pins the S05 row's status to `todo`:

```
grep -q '^| S05 | ... | U0008 | todo |' PLAN.md
```

RULE §2 says plainly: "A clause on an S row accepts open or done." This clause accepts neither — it requires `todo`. S row statuses do move here: `git show "35ae0ea:PLAN.md"` reads `| S04 | ... | U0006 | todo |` and at `1c8811f` the same row reads `done`. So S05 leaves `todo` as soon as U0008 — the very unit this plan names — runs, and the clause is red from then on. Demonstrated on a copy: with only `todo` → `done` in that row, the clause exits 1. The 10-level audit of RULE §4 reruns the clauses of units since the last closed audit, so this clause arrives at the first audit (due at 10, two units out) already red.

This is not weak style: the field is one of the nine verdict keys, it contradicts a rule line the block's own layer rests on, and it stops working one unit from now. The correct form was available and would still be red at base, since base reads `U0007` — ending the pattern at `| U0008 |` and dropping ` todo |` gives red at base, green now, and durable afterwards. Everything else in the block stands, so one clause edit and a rerun should clear it.

VERDICT: fail — check clause 1 pins the S05 row to status `todo`, which RULE §2 forbids ("A clause on an S row accepts open or done") and which goes red as soon as U0008 moves that row, as the copy test shows.

R1 FAIL
