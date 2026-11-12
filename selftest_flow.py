"""selftest_flow.py — the gate selftest of the flows, P29, S200.
A flow case turns planned records final, so a compact record gains every key first."""
import hashlib
import os
import re
import sys
import unit
import review_evidence
from review_evidence import review_file_error
from ledger import set_key
from ledger import log
from ledger import KEYS
from ledger import blocks
from ledger import load
from ledger import open_record
from ledger import read
from ledger import set_status
from ledger import write

PLANNED = r'(?ms)^## U\d{4} · \S+ · \w+ · planned$.*?(?=^## |\Z)'
STEPS = '''
| S998 | G9 | x.md | a step, G9 from 1 to 0 | a · b | | todo |
| S997 | G9 | measures.py | the measure of G9, G9 from no tool to 1 | a · b | | todo |
'''


def expand_plans(text):
    """Give each compact planned record every key, its values kept."""
    for uid, status, keys, values in list(blocks(text)):
        full = status != 'planned' or keys == KEYS
        if full:
            continue
        text = open_record(text, uid, values['base'])
        text = set_status(text, uid, 'open', 'planned')
    return text


def planned_block(number, base):
    """One compact planned record under the step S998."""
    head = f'\n\n## U{number:04d} · 2026-01-01 · behavioral · planned\n'
    keys = 'sentence   : x\nplan       : A0001 · S998\nfiles      : x.md\n'
    return head + keys + f'base       : {base}\nlines      : +1\n'


def try_open(copy, uid, plan):
    """Open by the four texts, the exit code returned."""
    texts = ['x', plan, 'x.md', '+1']
    sys.argv = sys.argv[:1] + ['open', uid, copy] + texts
    return settled_open(copy, uid)


def blocked_queue(copy, opened, audit):
    """A queue under a «no tool» leaf opens its measure step alone, S172."""
    units_path = os.path.join(copy, 'UNITS.md')
    plan_path = os.path.join(copy, 'PLAN.md')
    units = read(units_path)
    plan = read(plan_path)
    argv = sys.argv
    last = int(load(copy)[1][-1][0][1:])
    target = f'U{last + 2:04d}'
    queue = set_status(units, opened, 'open', 'closed')
    queue = re.sub(PLANNED, '', queue).rstrip('\n')
    queue += audit.rstrip('\n') + planned_block(last + 1, opened)
    try:
        write(copy, queue)
        with open(plan_path, 'w') as handle:
            handle.write(plan.rstrip('\n') + STEPS)
        stuck = unit.stuck(copy, load(copy)[1])
        work = try_open(copy, target, 'A0001 · S998')
        note = 'A0001 · S997 · S none, a planning unit'
        planning = try_open(copy, target, note)
        measure = try_open(copy, target, 'A0001 · S997')
        records = load(copy)[1]
        states = {r[0]: r[1] for r in records}
        state = states.get(target)
        pattern = rf'^## {target} · \S+ · (\w+) · open$'
        kind = re.search(pattern, read(units_path), re.M)
    finally:
        sys.argv = argv
        write(copy, units)
        with open(plan_path, 'w') as handle:
            handle.write(plan)
    refused = work == 1 and planning == 1
    entered = measure == 0 and state == 'open'
    behavioral = bool(kind) and kind.group(1) == 'behavioral'
    return stuck == {'G9'} and refused and entered and behavioral


def review_key(folder, uid, body):
    """Write one review file, return the key that names it."""
    name = 'agent-review-' + uid.lower() + '-r1.md'
    path = os.path.join(folder, name)
    with open(path, 'w') as handle:
        handle.write(f'# {uid} r1\n{body}\n')
    with open(path, 'rb') as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    return f'r1 pass, x, {path} sha256={digest}'


def review_file_case(copy, opened, tmp):
    """The reader takes the pass from the review file alone, S225."""
    good = review_key(tmp, opened, 'R1 PASS')
    passed = review_file_error(good, opened, copy) == ''
    other = review_file_error(good, 'U0000', copy)
    absent = good.replace('-r1.md', '-r9.md')
    bare = 'r1 pass, x, agent-review-case-r1.md'
    failed = review_key(tmp, opened, 'R1 FAIL')
    inside = review_key(copy, opened, 'R1 PASS')
    keys = (absent, bare, good, failed, inside)
    errors = [review_file_error(k, opened, copy) for k in keys]
    name = 'agent-review-' + opened.lower() + '-r1.md'
    os.remove(os.path.join(copy, name))
    return passed and bool(other) and all(errors)


FIXTURE_KEY = 'pass, agent-review-x.md'
FILLED = (('rejected', 'x'), ('added', 'x'), ('check', 'true'))
FILLED += (('approval', 'x'),)


def fixture_review():
    """Let the fixture key of the older close cases through the reader."""
    real = review_evidence.review_file_error
    def read_key(text, uid, room):
        if text.strip() == FIXTURE_KEY:
            return ''
        return real(text, uid, room)
    review_evidence.review_file_error = read_key


def review_close_case(copy, opened, tmp):
    """Close refuses a key whose review file no reviewer wrote, S225."""
    units = read(os.path.join(copy, 'UNITS.md'))
    good = review_key(tmp, opened, 'R1 PASS')
    forged = good.replace('-r1.md', '-r9.md')
    text = set_key(units, opened, 'review', forged)
    for key, value in FILLED:
        text = set_key(text, opened, key, value)
    write(copy, text)
    code = unit.close_unit(copy, opened)
    last = read(os.path.join(copy, 'unit.log')).splitlines()[-1]
    write(copy, units)
    named = 'review file is missing' in last and 'sha256=…»' in last
    return code == 1 and named


def nested_case(copy, opened, tmp):
    """The baseline test runs inside an outer confinement, S226."""
    from transition import confined_clause
    tmp = os.path.realpath(tmp)
    here = os.path.dirname(os.path.realpath(__file__))
    code = f'import sys; sys.path.insert(0, "{here}"); import transition as t; '
    code += 'print(t.baseline_state(".", "true · false"))'
    out = os.path.join(tmp, 'nested-s226.txt')
    home = os.path.expanduser('~')
    escape = os.path.join(home, f'.hectoline-escape-{os.getpid()}')
    clause = f"python3 -I -B -c '{code}' > {out}; echo x > {escape}"
    marker = os.path.join(tmp, 'entered-nested')
    confined_clause(tmp, copy, clause, dict(os.environ), marker)
    inner = ''
    if os.path.isfile(out):
        inner = read(out).strip()
    escaped = os.path.exists(escape)
    if escaped:
        os.remove(escape)
    return inner == '([1], [])' and not escaped and wide_case(copy, tmp)


def wide_case(copy, tmp):
    """An outer sandbox wider than the temp folder stops the direct run, S226."""
    import subprocess
    from transition import SANDBOX
    inner = os.path.join(tmp, 'wide-s226')
    os.makedirs(inner)
    profile = '(version 1)(allow default)(deny file-write*)'
    profile += f'(allow file-write* (subpath "{tmp}") (literal "/dev/null"))'
    here = os.path.dirname(os.path.realpath(__file__))
    code = f'import sys; sys.path.insert(0, "{here}"); import transition as t; '
    code += 't.outer_confinement(sys.argv[1])'
    args = [SANDBOX, '-p', profile, sys.executable]
    args += ['-I', '-B', '-c', code, inner]
    env = dict(os.environ, TMPDIR=inner)
    quiet = dict(capture_output=True, text=True, cwd=copy, env=env)
    done = subprocess.run(args, **quiet)
    return done.returncode == 1 and 'no temp-bound outer' in done.stderr


def baseline_case(copy, opened, tmp):
    """A missing command or a timeout at HEAD is no red baseline, S226."""
    from transition import baseline_state
    check = 'true · false · no-such-command-s226 · exit 124'
    classes = baseline_state(copy, check)
    slow = baseline_state(copy, 'sleep 5', timeout=1)
    units = read(os.path.join(copy, 'UNITS.md'))
    probe = os.path.join(copy, 'probe-s226.sh')
    with open(probe, 'w') as handle:
        handle.write('#!/bin/sh\nexit 0\n')
    os.chmod(probe, 0o755)
    text = set_key(units, opened, 'review', FIXTURE_KEY)
    text = set_key(text, opened, 'approval', 'x')
    for key, value in FILLED:
        text = set_key(text, opened, key, value)
    write(copy, set_key(text, opened, 'check', './probe-s226.sh'))
    code = unit.close_unit(copy, opened)
    last = read(os.path.join(copy, 'unit.log')).splitlines()[-1]
    write(copy, units)
    os.remove(probe)
    refused = code == 1 and 'exits 127 on a copy of HEAD' in last
    sorted_out = classes == ([1], [(3, 127), (4, 124)])
    return sorted_out and slow == ([], [(1, 124)]) and refused


def review_route_case(copy, opened, tmp):
    """The hook sends a review file write to the room of its unit, S225."""
    import json
    import subprocess
    home = os.path.join(tmp, 'routehome')
    os.makedirs(os.path.join(home, 'claude'))
    os.symlink(copy, os.path.join(home, 'claude', '00_room'))
    log(copy, 'open', opened, 'allow', 'fixture', 's2')
    path = os.path.join(tmp, f'agent-review-{opened.lower()}-r2.md')
    here = os.path.dirname(os.path.realpath(__file__))
    hook = os.path.join(here, 'hooks', 'claude.py')
    args = [sys.executable, '-I', '-B', hook]
    env = dict(os.environ, HOME=home)
    env['HECTOLINE_ROOMS'] = os.path.join(home, 'claude')
    quiet = dict(capture_output=True, text=True, env=env)
    def code(name, **more):
        call = dict(tool_name='Write', tool_input={'file_path': name}, **more)
        call.update(hook_event_name='PreToolUse', cwd=tmp, session_id='s2')
        return subprocess.run(args, input=json.dumps(call), **quiet).returncode
    plain = os.path.join(tmp, 'plain.md')
    codes = code(path), code(path, agent_id='a1'), code(plain)
    return codes == (2, 0, 0)


def review_write_case(copy, opened, tmp):
    """The author of the open unit cannot write its review file, S225."""
    from gate import opener
    path = os.path.join(tmp, f'agent-review-{opened.lower()}-r1.md')
    log(copy, 'open', opened, 'allow', 'fixture', 's1')
    author = opener(copy, opened)
    write_call = dict(tool_name='Write', tool_input={'file_path': path})
    shell = {'command': f'echo R1 PASS > {path}'}
    shell_call = dict(tool_name='Bash', tool_input=shell, cwd=tmp)
    denied = []
    for call in (write_call, shell_call):
        call = dict(call, session_id=author)
        denied.append(unit.check(copy, call)[0])
    agent = dict(write_call, session_id=author, agent_id='a1')
    stranger = dict(write_call, session_id=author + 'x')
    other = dict(write_call, session_id=author)
    other['tool_input'] = {'file_path': path.replace(opened.lower(), 'u0000')}
    passing = (agent, stranger, other)
    allowed = [unit.check(copy, c)[0] for c in passing]
    link = os.path.join(tmp, 'notes.md')
    os.symlink(path, link)
    linked = dict(tool_name='Write', session_id=author)
    linked['tool_input'] = {'file_path': link}
    denied.append(unit.check(copy, linked)[0])
    log(copy, 'open', opened, 'allow', 'fixture', '')
    allowed.append(unit.check(copy, write_call)[0])
    return not any(denied) and all(allowed)


def hand_close_case(tmp):
    """A hand-written closed status cannot be committed, S233."""
    import subprocess
    here = os.path.dirname(os.path.realpath(__file__))
    top = os.path.join(tmp, 'hand')
    room = os.path.join(top, '98_hand')
    tool = [sys.executable, '-I', '-B']
    quiet = dict(capture_output=True, text=True)
    def run(*args):
        return subprocess.run(args, **quiet)
    maker = tool + [os.path.join(here, 'room.py')]
    made = run(*maker, '98_hand', 'g', 'q', '--top', top)
    own = tool + [os.path.join(room, 'unit.py')]
    plan = 'A0001 · S none, the planning unit'
    sizes = ['UNITS.md:≤30', '≤30']
    run(*own, 'open', 'U0002', room, 'Plan x', plan, *sizes)
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:8] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    probe = 'grep -q U0002 UNITS.md'
    text = set_key(text, 'U0002', 'check', probe)
    write(room, set_status(text, 'U0002', 'open', 'closed'))
    git = ['git', '-C', room, '-c', 'user.name=x']
    git += ['-c', 'user.email=x@x']
    run(*git, 'add', 'UNITS.md')
    plain = run(*git, 'commit', '-qm', 'U0002 by hand')
    run(*git, 'reset', '-q')
    proof = review_key(top, 'U0002', 'R1 PASS')
    write(room, set_key(text, 'U0002', 'review', proof))
    closed = run(*own, 'close', 'U0002', room)
    said = 'holds no round, commit through' in plain.stderr
    refused = plain.returncode == 1 and said
    passed = not made.returncode and not closed.returncode
    return refused and passed


def settled_open(folder, uid):
    """Open on a fixture whose ledger HEAD holds, S233."""
    import subprocess
    git = ['git', '-C', folder, '-c', 'user.name=x']
    git += ['-c', 'user.email=x@x']
    quiet = dict(capture_output=True)
    subprocess.run(git + ['add', 'UNITS.md'], **quiet)
    subprocess.run(git + ['commit', '-qnm', 'fixture'], **quiet)
    tree = subprocess.run(git + ['write-tree'], **quiet).stdout
    record = os.path.join(folder, '.git', 'unit-trees')
    if os.path.exists(record):  # the fixture commit stands as passed, S243
        open(record, 'ab').write(tree)
    return unit.open_unit(folder, uid)


def loose_open_case(tmp):
    """Open reads a hand-written closed status as open, S233."""
    import subprocess
    here = os.path.dirname(os.path.realpath(__file__))
    top = os.path.join(tmp, 'loose')
    room = os.path.join(top, '98_loose')
    tool = [sys.executable, '-I', '-B']
    quiet = dict(capture_output=True, text=True)
    def run(*args):
        return subprocess.run(args, **quiet)
    maker = tool + [os.path.join(here, 'room.py')]
    run(*maker, '98_loose', 'g', 'q', '--top', top)
    own = tool + [os.path.join(room, 'unit.py'), 'open']
    plan = 'A0001 · S none, the planning unit'
    texts = ['Plan x', plan, 'UNITS.md:≤30', '≤30']
    first = run(*own, 'U0002', room, *texts)
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:8] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    probe = 'grep -q U0002 UNITS.md'
    text = set_key(text, 'U0002', 'check', probe)
    proof = review_key(top, 'U0002', 'R1 PASS')
    text = set_key(text, 'U0002', 'review', proof)
    write(room, set_status(text, 'U0002', 'open', 'closed'))
    second = run(*own, 'U0003', room, *texts)
    said = 'U0002, set its status back to open' in second.stderr
    same = read(os.path.join(room, 'UNITS.md')).count('## U')
    refused = second.returncode == 1 and said and same == 2
    write(room, text)
    closer = own[:-1] + ['close', 'U0002', room]
    third = run(*closer).returncode + run(*own, 'U0003', room, *texts).returncode
    return not first.returncode and refused and not third


def index_case(tmp):
    """The index of a final commit holds what its block claims, S233."""
    import subprocess
    here = os.path.dirname(os.path.realpath(__file__))
    top = os.path.join(tmp, 'index')
    room = os.path.join(top, '98_index')
    tool = [sys.executable, '-I', '-B']
    quiet = dict(capture_output=True, text=True)
    def run(*args):
        return subprocess.run(args, **quiet)
    maker = tool + [os.path.join(here, 'room.py')]
    run(*maker, '98_index', 'g', 'q', '--top', top)
    own = tool + [os.path.join(room, 'unit.py'), 'open']
    plan = 'A0001 · S none, the planning unit'
    sizes = ['RESEARCH.md:≤2 · /nowhere/x.md:≤1 · UNITS.md:≤30', '≤30']
    git = ['git', '-C', room, '-c', 'user.name=x']
    git += ['-c', 'user.email=x@x']
    said = []
    for uid, status in (('U0002', 'closed'), ('U0003', 'failed')):
        run(*own, uid, room, 'Plan x', plan, *sizes)
        with open(os.path.join(room, 'RESEARCH.md'), 'a') as handle:
            handle.write('note ' + uid + chr(10))
        text = read(os.path.join(room, 'UNITS.md'))
        for key in KEYS[2:8] + KEYS[12:]:
            text = set_key(text, uid, key, 'x')
        text = set_key(text, uid, 'check', 'grep -q U0002 RESEARCH.md')
        proof = review_key(top, uid, 'R1 PASS')
        text = set_key(text, uid, 'review', proof)
        write(room, set_status(text, uid, 'open', status))
        run(*git, 'add', 'UNITS.md')
        part = run(*git, 'commit', '-qm', uid + ' by hand')
        said.append(part.stderr)
        done = run(*git, 'commit', '-qam', uid + ' whole')
        said.append(done.stderr + str(done.returncode))
    loose = 'RESEARCH.md differs between the tree' in said[0]
    whole = said[1] == '0' and 'RESEARCH.md is staged with a failed' in said[3]
    kept = 'RESEARCH.md of a failed unit differs from HEAD' in said[2]
    return loose and whole and kept
