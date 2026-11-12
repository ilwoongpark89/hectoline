#!/usr/bin/env python3
"""example/build.py TOP [--snapshot] — build the sample room 01_pressure-drop under TOP with the real gate.
room.py makes the room with its acceptance check, so the first call is `unit.py open U0002 ROOM`.
Every later change enters through `unit.py open` and `unit.py close`, so each commit is one unit,
each block is written by the tool, and the pre-commit hook judges every commit.
Six units: the bootstrap with the leaf G1, the measure, a planning unit, the formula, its command line, one audit.
Each review file stands outside the room, under TOP/reviews, and the review key holds its sha256.
--snapshot copies the finished room into example/01_pressure-drop without .git, the log and the caches.
Needs macOS with sandbox-exec, git with a user name and email, Python 3.11 or later."""
import datetime, hashlib, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from ledger import KEYS, load, read, set_key, write

NAME = '01_pressure-drop'
G0 = 'a laminar pipe pressure-drop calculator answers its reference case within 1 percent'
QUOTE = 'Build a laminar pipe pressure-drop calculator that reproduces the reference case'
ACCEPT = 'the calculator answers the reference case within 1 percent'
REVIEW = 'r1 pass, the build session, {path} sha256={digest}'
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

FORMULA = '''#!/usr/bin/env python3
"""calc.py — the pressure drop of laminar pipe flow by Hagen-Poiseuille, in Pa.
MU viscosity in Pa s, L length in m, D inner diameter in m, Q volume flow in m3/s."""
import math


def pressure_drop(mu, length, diameter, flow):
    """128 mu L Q / (pi D^4), the laminar relation."""
    return 128 * mu * length * flow / (math.pi * diameter ** 4)
'''

COMMAND = '''

if __name__ == '__main__':
    mu, length, diameter, flow = map(float, sys.argv[1:5])
    print(f'{pressure_drop(mu, length, diameter, flow):.3f}')
'''

REVIEW_NOTE = '''# {uid} r1 — {sentence}

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: {check}
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4

R1 PASS
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
    path = os.path.join(os.path.realpath(folder), f'agent-review-{uid.lower()}-r1.md')
    note = REVIEW_NOTE.format(uid=uid, sentence=sentence, check=check)
    with open(path, 'w', encoding='utf8') as f:
        f.write(note)
    return REVIEW.format(path=path, digest=hashlib.sha256(note.encode('utf8')).hexdigest())


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
    keys = {'delete?': 'no, nothing exists to delete', 'modify?': 'no, no earlier block covers it',
                       'duplicate': f'grep -c "{sentence.split(",")[0]}" UNITS.md before this block: 0', 'cause': cause,
                       'split?': 'no, one change', 'tidy-first?': 'no', 'check': check, 'added': added, 'rejected': rejected,
                       'split': 'none', 'deleted': 'none', 'review': review(top, uid, sentence, check), 'approval': APPROVAL}
    if kind == 'audit':  # the audit runner reads a room that validates, so the keys stand before it runs
        fill(room, uid, **keys)
    body()
    fill(room, uid, **keys)
    print(sh(*PY, 'unit.py', 'close', uid, room, cwd=room).strip().splitlines()[-1])


def build(top):
    os.makedirs(top, exist_ok=True)
    room = os.path.join(top, NAME)
    print(sh(*PY, os.path.join(ROOT, 'room.py'), NAME, G0, QUOTE, '--top', top, '--accept', ACCEPT).strip())
    goal, plan, prods, units = (os.path.join(room, f) for f in ('GOAL.md', 'PLAN.md', 'PRODUCTS.md', 'UNITS.md'))

    def measure():
        with open(os.path.join(room, 'measures.py'), 'w', encoding='utf8') as f:
            f.write(MEASURES)
        edit(goal, '| acceptance checks passing in measures.py | all | no tool |',
             '| reference cases that calc.py misses by over 1 percent, by measures.py g1 | 0 | no tool |')
        edit(plan, '| U0002 | todo |', '| U0002 | done |')
    unit(room, top, 'U0002', 'measures.py computes the count of G1', 'A0001 · S02', 'measures.py · GOAL.md · PLAN.md · UNITS.md', '+≤70', measure,
         'test "$(python3 -I -B measures.py g1)" = "g1 1" · grep -q "^| S02 | .* | U0002 | done |$" PLAN.md',
         'result layer: the reference case and its analytic answer enter as data, the measure counts the misses, RULE §5',
         'measures.py with one reference case, 81.487 Pa, and g1 · the measure and the target 0 of G1 · S02 done',
         'a tolerance below 1 percent: the target of G1 is the 1 percent of the owner line · a second case: one case is the pilot')

    def plan1():
        edit(plan, '| S03 | G1 | the product, named by its planning unit | the pilot, one instance of the final product end to end, G1 from its first number to its target | the first passing instance · its parts | | todo |',
             '| S03 | G1 | calc.py | the pilot, the calculator by Hagen-Poiseuille end to end, G1 from 1 to 0 | the pressure drop from four inputs · the formula | U0004 U0005 | todo |')
        edit(plan, '| S01 | G0 | the six ledgers |', '| S01 | G0 | P01, the six ledgers |')
        with open(prods, 'a', encoding='utf8') as f:
            f.write('| P11 | the calculator | — | result | calc.py | — |\n| P12 | the audit records | — | result | audits/ | — |\n')
        with open(units, 'a', encoding='utf8') as f:
            f.write(planned('U0004', 'behavioral', 'calc.py holds the laminar pressure drop of a pipe as one function', 'A0001 · S03', 'calc.py · UNITS.md', 'U0003', '+≤40'))
            f.write(planned('U0005', 'behavioral', 'calc.py prints the pressure drop from four inputs on its command line', 'A0001 · S03', 'calc.py · PLAN.md · UNITS.md', 'U0004', '+≤40'))
            f.write(planned('U0006', 'audit', 'the audit of the first five units: rerun every closed check on a copy, list piles, duplicates, unused definitions', 'A0001 · S none, the audit of RULE §4', 'audits/audit-06.txt · UNITS.md', 'U0005', '+≤40'))
    unit(room, top, 'U0003', 'the planning unit: G1 reads 1, so the pilot step S03 names calc.py with its two units, then the first audit',
         'A0001 · S none, the planning unit of RULE §3 over an empty queue', 'PLAN.md · PRODUCTS.md · UNITS.md', '+≤40', plan1,
         "grep -qE '^## U0006 . [0-9-]+ . audit . ' UNITS.md · grep -q '| U0004 U0005 | todo |$' PLAN.md · grep -q '^| S01 | G0 | P01, ' PLAN.md · grep -q '^| P11 | the calculator |' PRODUCTS.md",
         'inputs layer of inputs → rules → state → result → view: the queue is empty after U0002, G1 reads 1 by measures.py, so the two work units of S03 and the audit after them are planned, RULE §3',
         'S03 names calc.py with U0004 and U0005 · S01 names its product P01 · P11 and P12 · the planned blocks U0004 and U0005 under S03 and U0006 the audit',
         'a redesign of measures.py: g1 reads 1 as the plan says · a second leaf for the Reynolds number: the reference case holds it')

    def formula():
        with open(os.path.join(room, 'calc.py'), 'w', encoding='utf8') as f:
            f.write(FORMULA)
    probe = "import sys; sys.path.insert(0, '.'); import calc; print(round(calc.pressure_drop(1.0e-3, 2, 0.01, 1e-5), 3))"
    unit(room, top, 'U0004', 'calc.py holds the laminar pressure drop of a pipe as one function', 'A0001 · S03', 'calc.py · UNITS.md', '+≤40', formula,
         f'test "$(python3 -B -c "{probe}")" = "81.487"',
         'result layer: the formula enters as one function before any caller exists, RULE §1 one behavior',
         'calc.py with pressure_drop · G1 still at 1, the measure calls the command line of the next unit', 'the command line in this unit: a second behavior, the next unit holds it')

    def command():
        path = os.path.join(room, 'calc.py')
        edit(path, '"""calc.py — the pressure drop', '"""calc.py MU L D Q — the pressure drop')
        edit(path, 'import math\n', 'import math, sys\n')
        with open(path, 'a', encoding='utf8') as f:
            f.write(COMMAND)
        edit(plan, '| U0004 U0005 | todo |', '| U0004 U0005 | done |')
    unit(room, top, 'U0005', 'calc.py prints the pressure drop from four inputs on its command line', 'A0001 · S03', 'calc.py · PLAN.md · UNITS.md', '+≤40', command,
         'test "$(python3 -I -B measures.py g1)" = "g1 0" · test "$(python3 -I -B calc.py 1.0e-3 2 0.01 1e-5)" = "81.487" · grep -q "^| S03 | .* | U0004 U0005 | done |$" PLAN.md',
         'result layer: the command line calls the one function, G1 moves from 1 to 0, RULE §1 one behavior',
         'the command line of calc.py with its usage line · S03 done · G1 at 0', 'a turbulent branch: the reference case is laminar, a second case would carry it · input checks: the measure covers the one case')

    def audit():
        os.makedirs(os.path.join(room, 'audits'), exist_ok=True)
        out = sh(*PY, 'audit.py', '6', '.', cwd=room)
        with open(os.path.join(room, 'audits', 'audit-06.txt'), 'w', encoding='utf8') as f:
            f.write(out)
    unit(room, top, 'U0006', 'the audit of the first five units: rerun every closed check on a copy, list piles, duplicates, unused definitions', 'A0001 · S none, the audit of RULE §4',
         'audits/audit-06.txt · UNITS.md', '+≤40', audit, "grep -q '^## piles: 0' audits/audit-06.txt · grep -q '^## check rerun on a copy: ' audits/audit-06.txt",
         'result layer: audit.py runs on a copy of the room, its output is the record, RULE §4 «Audit every 10 units», here once at the end of the pilot',
         'audits/audit-06.txt: the check rerun, the piles, the duplicates, the unused definitions, the measures', 'a fix inside the audit: an audit lists, a later unit fixes', kind='audit')
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
