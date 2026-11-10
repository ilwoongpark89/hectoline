"""selftest_roads.py — the selftest cases that walk a road on a fresh room of room.py, P35, S237."""
import os
import subprocess
import sys
from ledger import KEYS
from ledger import read
from ledger import set_key
from ledger import set_status
from ledger import write
from selftest_flow import review_key


def fresh(tmp, name, *more):
    """A fresh room of room.py with a runner, its open call, its git call."""
    here = os.path.dirname(os.path.realpath(__file__))
    top = os.path.join(tmp, name)
    room = os.path.join(top, '98_' + name)
    tool = [sys.executable, '-I', '-B']
    quiet = dict(capture_output=True, text=True)
    def run(*args):
        return subprocess.run(args, **quiet)
    maker = tool + [os.path.join(here, 'room.py')]
    made = run(*maker, '98_' + name, 'g', 'q', '--top', top, *more)
    own = tool + [os.path.join(room, 'unit.py'), 'open']
    git = ['git', '-C', room, '-c', 'user.name=x']
    git += ['-c', 'user.email=x@x']
    return made, top, room, run, own, git


def door_check_case(tmp):
    """A hand close under a true review file meets the check at the commit, S233."""
    made, top, room, run, own, git = fresh(tmp, 'door')
    plan = 'A0001 · S none, the planning unit'
    run(*own, 'U0002', room, 'Plan x', plan, 'UNITS.md:≤30', '≤30')
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:8] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    proof = review_key(top, 'U0002', 'R1 PASS')
    text = set_key(text, 'U0002', 'review', proof)
    text = set_status(text, 'U0002', 'open', 'closed')
    git = git + ['commit', '-qam', 'U0002 by hand']
    said = []
    for probe in ('test -f absent.md', 'true'):
        write(room, set_key(text, 'U0002', 'check', probe))
        said.append(run(*git).stderr)
    red = 'check exits [1], commit through' in said[0]
    held = 'clauses [1] [] are not red' in said[1]
    write(room, set_key(text, 'U0002', 'check', 'grep -q U0002 UNITS.md'))
    return red and held and not run(*git).returncode


def queue_text_case(tmp):
    """The two queue refusals of open name the call that passes, S227."""
    made, top, room, run, own, git = fresh(tmp, 'queue')
    sizes = ['PLAN.md:≤2 · UNITS.md:≤30', '≤30']
    work = run(*own, 'U0002', room, 'Build x', 'A0001 · S01', *sizes)
    bare = run(*own, 'U0007', room)
    form = "'A#### · S none, the planning unit'"
    said = form in work.stderr and 'planned queue is empty' in work.stderr
    said = said and 'the next unit is U0002' in bare.stderr
    said = said and form in bare.stderr
    plan = 'A0001 · S none, the planning unit'
    passed = run(*own, 'U0002', room, 'Plan x', plan, *sizes)
    text = read(os.path.join(room, 'UNITS.md'))
    write(room, set_status(text, 'U0002', 'open', 'waiting'))
    held = run(*own, 'U0003', room).stderr
    said = said and 'U0002 waits for its review: unit.py close U0002' in held
    return said and not passed.returncode


def entry_case(tmp):
    """A room made with its acceptance check opens its measure unit in one call, S228."""
    extra = ['--accept', 'exit 0 | the tests pass']
    made, top, room, run, own, git = fresh(tmp, 'entry', *extra)
    clean = run(*git, 'status', '--porcelain').stdout
    valid = run(*own[:-1], 'validate', room).stdout
    stat = run(*git, 'show', '--numstat', '--format=', 'HEAD').stdout
    rows = stat.splitlines()
    count = sum(int(row.split()[0]) for row in rows)
    text = read(os.path.join(room, 'UNITS.md'))
    true = f'lines      : +{count} ' in text and '0 faults' in valid
    block = text.split('## U0002')[1].replace('S02', 'S03')
    write(room, text.split('\n## U0002')[0] + '\n## U0003' + block)
    pilot = run(*own, 'U0003', room).stderr
    write(room, text)
    first = run(*own, 'U0002', room)
    plain = fresh(tmp, 'plain')[2]
    old = 'G1' not in read(os.path.join(plain, 'GOAL.md'))
    bad = fresh(tmp, 'bad', '--accept', '--top')[0].returncode
    held = 'G1 is unmeasured' in pilot and not clean
    held = held and old and bad == 2
    return true and held and not first.returncode


def leaf_text_case(tmp):
    """The leaf move refusal names the text that passes, S227."""
    extra = ['--accept', 'the tests pass']
    made, top, room, run, own, git = fresh(tmp, 'leaf', *extra)
    path = os.path.join(room, 'PLAN.md')
    plan = read(path) + chr(10) + '## rule 1.1 from S02' + chr(10)
    move = ', G1 from no tool to its first number'
    with open(path, 'w', encoding='utf8') as handle:
        handle.write(plan.replace(move, ''))
    bare = run(*own, 'U0002', room).stderr
    form = 'G1 from its number to its number'
    with open(path, 'w', encoding='utf8') as handle:
        handle.write(plan.replace(move, ', ' + form))
    said = 'write «' + form + '» in the step text' in bare
    opened = run(*own, 'U0002', room).returncode
    made, top, room, run, own, git = fresh(tmp, 'bare')
    step = '| S02 | G0 | x | the measure tool of this room | a · b | U0002 | todo |'
    path = os.path.join(room, 'PLAN.md')
    mark = chr(10) + '## rule 1.1 from S02' + chr(10)
    plan = read(path) + step + chr(10) + mark
    with open(path, 'w', encoding='utf8') as handle:
        handle.write(plan)
    block = chr(10) + '## U0002 · 2026-01-01 · behavioral · planned' + chr(10)
    block += 'sentence   : x' + chr(10) + 'plan       : A0001 · S02' + chr(10)
    block += 'files      : x.py:≤9' + chr(10) + 'base       : U0001' + chr(10) + 'lines      : ≤9' + chr(10)
    write(room, read(os.path.join(room, 'UNITS.md')) + block)
    none = 'GOAL.md holds no leaf under G0' in run(*own, 'U0002', room).stderr
    return said and none and not opened


def third_fail_case(tmp):
    """Three failed review rounds end a fresh unit with its product reverted, S79."""
    made, top, room, run, own, git = fresh(tmp, 'third')
    plan = 'A0001 · S none, the planning unit'
    run(*own, 'U0002', room, 'Plan x', plan, 'UNITS.md:≤30 · x.md:≤2', '≤30')
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:8] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    rounds = 'r1 fail class 1, x · r2 fail · r3 fail'
    text = set_key(text, 'U0002', 'review', rounds)
    write(room, set_key(text, 'U0002', 'check', 'true'))
    product = os.path.join(room, 'x.md')
    with open(product, 'w', encoding='utf8') as handle:
        handle.write('x' + chr(10))
    run(*own[:-1], 'close', 'U0002', room)
    text = read(os.path.join(room, 'UNITS.md'))
    failed = '## U0002 · ' in text and ' · failed' + chr(10) in text
    named = 'failed after 3 failed verifications' in text
    subject = run(*git, 'log', '-1', '--format=%s').stdout
    kept = subject.startswith('U0002 ') and not os.path.exists(product)
    return failed and named and kept


def temp_clean_case(copy, opened, base, tmp):
    """A refused close that reached the baseline clone leaves no temp folder, S110."""
    import tempfile
    def count():
        names = os.listdir(tempfile.gettempdir())
        return sum(name.startswith('hectoline-') for name in names)
    text = set_key(base, opened, 'review', review_key(tmp, opened, 'R1 PASS'))
    for key, value in (('rejected', 'x'), ('added', 'x')):
        text = set_key(text, opened, key, value)
    write(copy, set_key(text, opened, 'check', 'test -f stray.md'))
    stray = os.path.join(copy, 'stray.md')
    kept = os.path.exists(stray)
    with open(stray, 'a') as handle:
        handle.write('' if kept else 'x\n')
    before = count()
    args = [sys.executable, '-I', '-B', os.path.join(copy, 'unit.py')]
    done = subprocess.run(args + ['close', opened, copy], capture_output=True, text=True)
    if not kept:
        os.remove(stray)
    last = read(os.path.join(copy, 'unit' + '.log')).splitlines()[-1]
    write(copy, base)
    reached = 'refused by the git hook' in last
    return done.returncode == 1 and reached and count() == before

