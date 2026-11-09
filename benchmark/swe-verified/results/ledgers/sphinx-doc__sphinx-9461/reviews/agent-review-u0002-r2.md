# agent-review-u0002 r2

model claude-opus-5 · session 050b05c0-4855-48c0-b23e-1578f8dd718d · turns 10 · wall 103.5 s · exit 0

## Answer

I ran every clause and checked each field against the files.

**What holds**
- The check exits 1 on the base (`ef6e44c` copies of PLAN.md/UNITS.md: `AssertionError: {}`) and exits 0 in the working tree — it does not pass at the base.
- `lines : +87` matches `git diff --numstat ef6e44c -- PLAN.md UNITS.md` (3 + 84). `files : PLAN.md:10-12` are exactly the three new S rows; `UNITS.md:24-106` covers this block and the three planned blocks.
- `duplicate` is true: `grep -c "^| S0" PLAN.md` at `ef6e44c` is 1.
- `approval` is verbatim against OWNER.md A0001 «Fix the issue in TASK.md in this repository».
- S02–S04 each name a G0 leaf move; no product file is touched, as a planning unit requires. The r1 gap is partly addressed: the new clause now reads each planned block's own `sentence` and `plan` line and binds it to the step's `units` cell.

**Why it fails**

The check key now rests on transient statuses, which RULE §2 forbids on this key: "A planning clause greps no planned status." The regex anchors on `## (U000[345])[^\n]*planned` and on `\| (U000[345]) \| todo \|`, so the clause asserts U0003–U0005 are still `planned` and S02–S04 are still `todo`. r1 named this bar explicitly and said a clause on the `sentence` or `plan` line was available and legal; the new clause takes those lines but pins the status word anyway.

That makes it a field that cannot work. With U0003's header status changed from `planned` to `open` and nothing else touched, the same clause exits 1: `AssertionError: {'S03': 'U0004', 'S04': 'U0005'}`. So the check stops passing the moment the first planned unit it describes opens, and the §4 audit rerun of every non-audit unit's check will fail on it even though this unit's outcome — three S rows with three planned blocks bound to them — is still intact in the ledgers. The fix is mechanical: drop `planned` and `todo` from the two patterns (match the header as `## (U000[345]) · [^\n]*\n` and the row cell as `\| (U000[345]) \|`), keeping the content assertions that r1 asked for.

Not graded, carried from r1: PLAN.md's product column for S02–S04 names products with no P row in PRODUCTS.md, which stops at P09; closed S01 uses the same prose form, so I leave it as a note.

VERDICT: fail — the check clause pins the transient `planned` and `todo` statuses, which RULE §2 forbids for a planning clause, and it exits 1 once U0003 opens, so the field cannot work.
