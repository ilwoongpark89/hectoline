#!/usr/bin/env python3
"""example/build.py TOP [--snapshot] — build the sample room 01_pressure-drop under TOP with the real gate.
room.py makes the room. Every later change enters through `unit.py open` and `unit.py close`, so each
commit is one unit, each block is written by the tool, and the pre-commit hook runs on every commit.
Six units: the bootstrap, a planning unit, the measure, a second planning unit, the calculator, one audit.
--snapshot copies the finished room into example/01_pressure-drop without .git, the log and the caches.
Needs macOS with sandbox-exec, git with a user name and email, Python 3.11 or later."""
import datetime, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from ledger import KEYS, load, read, set_key, write

NAME = '01_pressure-drop'
G0 = 'a laminar pipe pressure-drop calculator answers its reference case within 1 percent'
QUOTE = 'Build a laminar pipe pressure-drop calculator that reproduces the reference case'
REVIEW = 'pass r1, the diff and the nine verdict keys read, example/reviews/agent-review-{u}.md'
APPROVAL = f'«{QUOTE}», the A0001 row'
PY = [sys.executable, '-I', '-B']

MEASURES = '''#!/usr/bin/env python3
"""measures.py — the measure of 01_pressure-drop, RULE §5. g1 = reference cases the calculator misses by over 1 percent.
The reference: water at 20 degrees C, viscosity 1.0e-3 Pa s, pipe length 2 m, diameter 0.01 m, flow 1.0e-5 m3/s.
Hagen-Poiseuille gives 81.487 Pa. Reynolds number 1273, laminar. Usage: measures.py g1 [ROOM]."""
import os, subprocess, sys

CASES = [((1.0e-3, 2.0, 0.01, 1.0e-5), 81.487)]


def g1(room=None, bl=None):
    """Reference cases the calculator misses by over 1 percent. A missing calculator misses every case."""
    room = room or os.path.dirname(os.path.abspath(__file__))
    calc = os.path.join(room, 'calc.py')
    if not os.path.isfile(calc):
        return len(CASES)
    missed = 0
    for args, want in CASES:
        run = subprocess.run([sys.executable, '-I', '-B', calc, *map(str, args)], capture_output=True, text=True)
        try:
            got = float(run.stdout.strip())
        except ValueError:
            missed += 1
            continue
        missed += abs(got - want) / want > 0.01
    return missed


if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'g1'
    print(name, globals()[name](sys.argv[2] if len(sys.argv) > 2 else None))
'''

CALC = '''#!/usr/bin/env python3
"""calc.py MU L D Q — the pressure drop of laminar pipe flow by Hagen-Poiseuille, in Pa.
MU viscosity in Pa s, L length in m, D inner diameter in m, Q volume flow in m3/s."""
import math, sys


def pressure_drop(mu, length, diameter, flow):
    """128 mu L Q / (pi D^4), the laminar relation."""
    return 128 * mu * length * flow / (math.pi * diameter ** 4)


if __name__ == '__main__':
    mu, length, diameter, flow = map(float, sys.argv[1:5])
    print(f'{pressure_drop(mu, length, diameter, flow):.3f}')
'''

REVIEW_NOTE = '''# agent-review-{u} — {sentence}

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: {check}
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4
- verdict: pass r1
'''


def sh(*args, cwd=None, check=True):
    run = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and run.returncode:
        sys.exit(f'{" ".join(map(str, args))}\n{run.stdout}{run.stderr}')
    return run.stdout


def fill(room, uid, **vals):
    text = load(room)[0]
    for key, value in vals.items():
        text = set_key(text, uid, key, value)
    write(room, text)


def planned(uid, kind, sentence, plan, files, base, lines):
    vals = dict(sentence=sentence, plan=plan, files=files, base=base, lines=lines)
    return f'\n## {uid} · {datetime.date.today()} · {kind} · planned\n' + '\n'.join(f'{k:<11}: {vals.get(k, "")}' for k in KEYS) + '\n'


def review(top, uid, sentence, check):
    folder = os.path.join(top, 'reviews')
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f'agent-review-{uid.lower()}.md'), 'w', encoding='utf8') as f:
        f.write(REVIEW_NOTE.format(u=uid.lower(), sentence=sentence, check=check))
    return REVIEW.format(u=uid.lower())


def edit(path, old, new):
    text = read(path)
    assert text.count(old) == 1, (path, old)
    with open(path, 'w', encoding='utf8') as f:
        f.write(text.replace(old, new))


def unit(room, top, uid, sentence, plan, files, lines, body, check, cause, added, rejected, kind=None):
    """Open a unit by four texts or from its planned block, let body() edit the files, fill the keys, close."""
    _, bl = load(room)
    if not any(u == uid for u, _, _, _ in bl):
        print(sh(*PY, 'unit.py', 'open', uid, room, sentence, plan, files, lines, cwd=room).splitlines()[0])
    else:
        print(sh(*PY, 'unit.py', 'open', uid, room, cwd=room).splitlines()[0])
    body()
    fill(room, uid, **{'delete?': 'no, nothing exists to delete', 'modify?': 'no, no earlier block covers it',
                       'duplicate': f'grep -c "{sentence.split(",")[0]}" UNITS.md before this block: 0', 'cause': cause,
                       'split?': 'no, one change', 'tidy-first?': 'no', 'check': check, 'added': added, 'rejected': rejected,
                       'split': 'none', 'deleted': 'none', 'review': review(top, uid, sentence, check), 'approval': APPROVAL})
    print(sh(*PY, 'unit.py', 'close', uid, room, cwd=room).strip().splitlines()[-1])


def build(top):
    os.makedirs(top, exist_ok=True)
    room = os.path.join(top, NAME)
    print(sh(*PY, os.path.join(ROOT, 'room.py'), NAME, G0, QUOTE, '--top', top).strip())
    goal, plan, prods, units = (os.path.join(room, f) for f in ('GOAL.md', 'PLAN.md', 'PRODUCTS.md', 'UNITS.md'))

    def plan1():
        edit(goal, '| G0 | ' + G0 + ' | — | leaves at target | 0 of 0 | 0 of 0 |\n',
             '| G0 | ' + G0 + ' | — | leaves at target | 1 of 1 | 0 of 1 |\n'
             '| G1 | the calculator answers the reference case within 1 percent | G0 | reference cases that calc.py misses by over 1 percent, by measures.py g1 | 0 | no tool |\n')
        with open(plan, 'a', encoding='utf8') as f:
            f.write('| S02 | G1 | measures.py | the measure of G1, G1 from no tool to 1: one reference case with its analytic answer | the number g1 · the case data | U0003 | todo |\n'
                    '| S03 | G1 | calc.py | the calculator, G1 from 1 to 0: laminar pipe pressure drop by Hagen-Poiseuille | the pressure drop from four inputs · the formula | | todo |\n')
        with open(prods, 'a', encoding='utf8') as f:
            f.write('| P10 | the measure of G1 | — | result | measures.py | P05 |\n| P11 | the calculator | — | result | calc.py | — |\n| P12 | the audit records | — | result | audits/ | — |\n')
        with open(units, 'a', encoding='utf8') as f:
            f.write(planned('U0003', 'behavioral', 'measures.py computes g1, the reference cases the calculator misses', 'A0001 · S02', 'measures.py · PLAN.md · UNITS.md', 'U0002', '+≤40'))
    unit(room, top, 'U0002', 'the planning unit: G1 with its measure, the steps S02 S03, the products P10 to P12, the planned measure unit',
         'A0001 · S none, the planning unit of RULE §3', 'GOAL.md · PLAN.md · PRODUCTS.md · UNITS.md', '+≤40', plan1,
         "grep -q '^| G1 |' GOAL.md · grep -q '^| S03 | G1 | calc.py |' PLAN.md · grep -q '^| P11 | the calculator |' PRODUCTS.md",
         'inputs layer of inputs → rules → state → result → view: the A0001 order becomes one leaf, two steps and three products, RULE §3',
         'G1 and its target, S02 the measure step and S03 the calculator, P10 to P12, the planned block U0003 under S02',
         'a planned block for S03 now: G1 is unmeasured until S02 closes, so only its measure step may open, RULE §1 · a second leaf for the Reynolds number: the reference case holds it')

    def measure():
        with open(os.path.join(room, 'measures.py'), 'w', encoding='utf8') as f:
            f.write(MEASURES)
        edit(plan, '| U0003 | todo |', '| U0003 | done |')
    unit(room, top, 'U0003', 'measures.py computes g1, the reference cases the calculator misses', 'A0001 · S02', 'measures.py · PLAN.md · UNITS.md', '+≤40', measure,
         'test "$(python3 -I -B measures.py g1)" = "g1 1" · grep -q "^| S02 | .* | U0003 | done |$" PLAN.md',
         'result layer: the reference case and its analytic answer enter as data, the measure counts the misses, RULE §5',
         'measures.py with one reference case, 81.487 Pa, and g1 · S02 done', 'a tolerance below 1 percent: the target of G1 is the 1 percent of the owner line · a second case: one case is the pilot')

    def plan2():
        edit(plan, '| the pressure drop from four inputs · the formula | | todo |', '| the pressure drop from four inputs · the formula | U0005 | todo |')
        with open(units, 'a', encoding='utf8') as f:
            f.write(planned('U0005', 'behavioral', 'calc.py prints the laminar pressure drop of a pipe from four inputs', 'A0001 · S03', 'calc.py · PLAN.md · UNITS.md', 'U0004', '+≤40'))
            f.write(planned('U0006', 'audit', 'the audit of the first five units: rerun every closed check on a copy, list piles, duplicates, unused definitions', 'A0001 · S none, the audit of RULE §4', 'audits/audit-06.txt · UNITS.md', 'U0005', '+≤40'))
    unit(room, top, 'U0004', 'the second planning unit: G1 is measured at 1, so S03 gets its unit, then the first audit', 'A0001 · S none, the planning unit of RULE §3 over an empty queue',
         'PLAN.md · UNITS.md', '+≤40', plan2, "grep -qE '^## U0006 . [0-9-]+ . audit . ' UNITS.md · grep -q '| U0005 | todo |$' PLAN.md",
         'inputs layer: the queue is empty after U0003, G1 reads 1 by measures.py, so the work unit of S03 and the audit after it are planned, RULE §3',
         'the planned blocks U0005 under S03 and U0006 the audit · S03 names U0005', 'a redesign of measures.py: g1 reads 1 as the plan says · a third step: G1 has two steps and one leaf')

    def calc():
        with open(os.path.join(room, 'calc.py'), 'w', encoding='utf8') as f:
            f.write(CALC)
        edit(plan, '| U0005 | todo |', '| U0005 | done |')
    unit(room, top, 'U0005', 'calc.py prints the laminar pressure drop of a pipe from four inputs', 'A0001 · S03', 'calc.py · PLAN.md · UNITS.md', '+≤40', calc,
         'test "$(python3 -I -B measures.py g1)" = "g1 0" · test "$(python3 -I -B calc.py 1.0e-3 2 0.01 1e-5)" = "81.487" · grep -q "^| S03 | .* | U0005 | done |$" PLAN.md',
         'result layer: the formula enters as one function, the command line prints it, G1 moves from 1 to 0, RULE §1 one behavior',
         'calc.py with pressure_drop and its command line · S03 done · G1 at 0', 'a turbulent branch: the reference case is laminar, a second case would carry it · input checks: the measure covers the one case')

    def audit():
        os.makedirs(os.path.join(room, 'audits'), exist_ok=True)
        out = sh(*PY, 'audit.py', '6', '.', cwd=room)
        with open(os.path.join(room, 'audits', 'audit-06.txt'), 'w', encoding='utf8') as f:
            f.write(out)
    unit(room, top, 'U0006', 'the audit of the first five units: rerun every closed check on a copy, list piles, duplicates, unused definitions', 'A0001 · S none, the audit of RULE §4',
         'audits/audit-06.txt · UNITS.md', '+≤40', audit, "grep -q '^## piles: 0' audits/audit-06.txt · grep -q '^## check rerun on a copy: ' audits/audit-06.txt",
         'result layer: audit.py runs on a copy of the room, its output is the record, RULE §4 «Audit every 10 units», here once at the end of the pilot',
         'audits/audit-06.txt: the check rerun, the piles, the duplicates, the unused definitions, the measures', 'a fix inside the audit: an audit lists, a later unit fixes')
    return room


def snapshot(room):
    target = os.path.join(HERE, NAME)
    if os.path.exists(target):
        shutil.rmtree(target)
    skip = shutil.ignore_patterns('.git', 'unit.log', '__pycache__')
    shutil.copytree(room, target, symlinks=True, ignore=skip)
    for name in os.listdir(target):  # the links point at this repository, relative to the snapshot
        path = os.path.join(target, name)
        if os.path.islink(path):
            real = os.path.realpath(os.path.join(room, name))
            os.unlink(path)
            os.symlink(os.path.relpath(real, target), path)
    reviews = os.path.join(os.path.dirname(room), 'reviews')
    if os.path.isdir(reviews):
        shutil.rmtree(os.path.join(HERE, 'reviews'), ignore_errors=True)
        shutil.copytree(reviews, os.path.join(HERE, 'reviews'))
    print(f'snapshot: {target}')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--snapshot']
    if not args:
        sys.exit(__doc__)
    built = build(os.path.abspath(args[0]))
    if '--snapshot' in sys.argv:
        snapshot(built)
