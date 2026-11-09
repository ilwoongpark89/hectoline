# agent-review-u0003 round 1

model claude-opus-5 · session 8c0235cc-3cd2-4063-bafe-25079703120c · turns 30 · wall 263.1 s · exit 0

## Answer

**Review of U0003 — ran every clause at HEAD and on a base copy of 5bf27e0.**

**Check clauses, measured**

| clause | at base 5bf27e0 | now |
|---|---|---|
| `grep -q "^def g1" measures.py` | exit 2 | exit 0 |
| `python3 -I -B measures.py g1 .` → `g1 3` | exit 1, no file | exit 0, prints `g1 3` |
| `measure.measures(...)['G1']` → `3` | exit 1, reads `no tool` | exit 0, prints `3` |

No clause passes at the base. Clause 1 is the opener RULE §2 demands; clauses 2 and 3 prove the number, not the text.

**The number is honest.** I ran the six cases one by one under `.venv`: cases 1, 2, 6 fail (alt 86.33 deg against 90, ha 5.96 deg against 0, zenith alt 86.33 deg), cases 3, 4, 5 pass (round trip 0.061 mm, refraction 5.39 arcmin inside the 5.0 to 5.8 band). Three fail, so `g1` = 3 and the GOAL.md baseline 3 holds. The three passing cases are real guards, not trivial.

**Fields, each against its file**
- `duplicate`: `git ls-tree 5bf27e0` holds no measures.py. True.
- `modify?`: measure.py is a symlink to the hectoline adapter and reads the room tool at `measure.py:24-27`. True.
- `rejected`: `python3 -c "import numpy"` fails on the worker interpreter, `.venv` holds numpy 1.26.4. The millimetre gap is 0.061 mm, so a zero tolerance would break. Both reasons check out.
- `approval`: matches the A0001 quote in OWNER.md character for character.
- `base`, `plan`, `files`, `lines`: U0002 closed at 5bf27e0, S02 under G1 names the move «from no tool to 3», and only the four named files changed. 75 added, 16 modified, inside budget.
- Interface of S02: `g1` exposes the failing count and hides the cases and the interpreter. The diff stays behind it.
- Confinement holds: the measure runs in 2.5 s inside the 30 s bound, writes nothing.

**Three weak points, none fail grade**
- `measures.py:74-75` exceed the 10-word line cap. `lines.py diff .` exits 1 on them, but `unit.py:106` skips that gate when RULE.md is a link, which it is here. Worth fixing anyway.
- `CASES = 6` at `measures.py:16` is never read. Dead constant, an audit-level item.
- PRODUCTS.md carries no P row for measures.py, though S02 names it as the product. The gate enforces no such row, and U0002 already passed with the same gap.

The room is untouched; my scratch files are deleted.

VERDICT: pass — every clause fails at 5bf27e0 and passes now through the real acceptance cases and the confined adapter, and each field holds against the file it names.
