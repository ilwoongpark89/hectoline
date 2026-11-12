"""selftest_roads.py — the selftest cases that walk a road on a fresh room of room.py, P35, S237."""
import hashlib
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


def tool_away_case(tmp):
    """The hook judges a room whose unit.py or UNITS.md was moved away, S233."""
    made, top, room, run, own, git = fresh(tmp, 'away')
    plan = 'A0001 · S none, the planning unit'
    run(*own, 'U0002', room, 'Plan x', plan, 'UNITS.md:≤30', '≤30')
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:9] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    write(room, set_status(text, 'U0002', 'open', 'closed'))
    link = os.path.join(room, 'unit.py')
    os.rename(link, os.path.join(top, 'unit.py'))
    run(*git, 'add', 'UNITS.md')
    hand = run(*git, 'commit', '-qm', 'U0002 by hand')
    run(*git, 'rm', '-q', '--cached', 'UNITS.md')
    gone = run(*git, 'commit', '-qm', 'no ledger')
    said = 'commit through unit.py close' in hand.stderr
    made, top, room, run, own, git = fresh(tmp, 'copy')
    hook = os.path.join(room, '.git', 'hooks', 'pre-commit')
    body = read(os.path.realpath(hook))
    os.unlink(hook)
    with open(hook, 'w', encoding='utf8') as handle:
        handle.write(body)
    os.chmod(hook, 0o755)
    run(*own, 'U0002', room, 'Plan x', plan, 'UNITS.md:≤30', '≤30')
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:8] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    text = set_key(text, 'U0002', 'check', 'grep -q U0002 UNITS.md')
    proof = review_key(top, 'U0002', 'R1 PASS')
    write(room, set_key(text, 'U0002', 'review', proof))
    real = run(*own[:-1], 'close', 'U0002', room).returncode
    link = os.path.join(room, 'unit.py')
    os.rename(link, os.path.join(top, 'unit.py'))
    lost = run(*git, 'commit', '-qam', 'x').stderr
    held = not real and 'unit.py is missing, restore its link' in lost
    held = held and hand.returncode == 1
    return said and held and gone.returncode == 1


def alias_case(tmp):
    """Close reads a review file only under the name of its unit, S233."""
    made, top, room, run, own, git = fresh(tmp, 'alias')
    plan = 'A0001 · S none, the planning unit'
    run(*own, 'U0002', room, 'Plan x', plan, 'UNITS.md:≤30', '≤30')
    text = read(os.path.join(room, 'UNITS.md'))
    for key in KEYS[2:8] + KEYS[12:]:
        text = set_key(text, 'U0002', key, 'x')
    text = set_key(text, 'U0002', 'check', 'grep -q U0002 UNITS.md')
    codes = []
    for name in ('agent-review-u0000-r1.md', 'agent-review-hub-u0002.md'):
        path = os.path.join(top, name)
        with open(path, 'w', encoding='utf8') as handle:
            handle.write('# U0002 r1' + chr(10) + 'R1 PASS' + chr(10))
        digest = hashlib.sha256(read(path).encode()).hexdigest()
        key = f'r1 pass, x, {path} sha256={digest}'
        write(room, set_key(text, 'U0002', 'review', key))
        done = run(*own[:-1], 'close', 'U0002', room)
        codes.append((done.returncode, done.stderr))
    said = 'not named for its unit, name it agent-review-u0002-rN.md' in codes[0][1]
    kept = codes[0][0] == 1 and codes[1][0] == 0
    return said and kept


def log_heal_case(tmp):
    """A write of the log by any spelling is undone at the next call, S243."""
    import ledger
    made, top, room, run, own, git = fresh(tmp, 'heal')
    path = os.path.join(room, 'unit.log')
    ledger.log(room, 'test', '', 'allow', 'seed')
    writes = ['echo x >> L', ': > unit.lo?', 'sed -i "" 1d L', 'rm -f L', 'truncate -s 0 L']
    writes += ['git checkout HEAD -- L', 'cat L > ./unit.l*', 'echo L | xargs rm', 'chmod 000 L']
    writes += ["python3 -c \"open('L', 'a').write('x')\"", 'rm L; ln -s RULE.md L', 'rm L; mkdir L']
    writes += ['rm L; ln -s /dev/null L', 'rm L; mkfifo L', 'rm L; mkdir L; chmod 000 L']
    quiet = dict(shell=True, cwd=room, capture_output=True, executable='/bin/bash')
    held = []
    for line in writes:
        before = ledger.read(path)
        subprocess.run(line.replace('L', 'unit.log'), **quiet)
        ledger.heal(room)
        after = ledger.read(path)
        notes = after[len(before):].count('restored')
        held.append(after.startswith(before) and notes == 1)
    line = 'sed -n 1p RULE.md; grep -c deny unit.log; awk 1 unit.log'
    reads = dict(tool_name='Bash', tool_input=dict(command=line))
    passed = __import__('unit').check(room, reads)[0]
    copy = ledger.shadow(room)
    os.remove(copy)
    tool = os.path.join(room, 'unit.py')
    run(sys.executable, '-I', '-B', tool, 'validate', room)
    quiet = not os.path.exists(copy)  # a read-only command writes no shadow, audit520
    return all(held) and passed and quiet


def head_settle_case(tmp):
    """A commit around the hook is undone at the next call, its change stays, S243."""
    made, top, room, run, own, git = fresh(tmp, 'settle')
    tool = [sys.executable, '-I', '-B', os.path.join(room, 'unit.py')]
    ask = dict(input='{}')
    subprocess.run(tool + ['check', room], text=True, capture_output=True, **ask)
    head = run(*git, 'rev-parse', 'HEAD').stdout
    with open(os.path.join(room, 'GOAL.md'), 'a') as page:
        page.write('x\n')
    run(*git, 'commit', '-n', '-qam', 'x')
    moved = run(*git, 'rev-parse', 'HEAD').stdout != head
    subprocess.run(tool + ['check', room], text=True, capture_output=True, **ask)
    back = run(*git, 'rev-parse', 'HEAD').stdout == head
    kept = run(*git, 'diff', '--cached', '--name-only').stdout
    notes = read(os.path.join(room, 'unit.log')).count('passed no hook')
    held = moved and back and 'GOAL.md' in kept
    return held and notes == 1


def child_room_case(tmp):
    """The room list reads one level inside a numbered folder, no deeper."""
    import gate
    top = os.path.join(tmp, 'home', 'claude')
    rooms = ['01_a', '01_a/01_02_b', '03_c/03_01_d']
    other = ['03_c', '01_a/x_e', '01_a/01_02_b/01_02_03_z']
    for name in rooms + other:
        os.makedirs(os.path.join(top, name), exist_ok=True)
    for name in rooms + other[1:]:
        open(os.path.join(top, name, 'UNITS.md'), 'w').close()
    open(os.path.join(top, '01_a', '01_note.html'), 'w').close()
    kept = gate.ROOMS  # the public tree reads its rooms under ROOMS
    gate.ROOMS = top
    found = gate.numbered_rooms(True), gate.numbered_rooms()
    gate.ROOMS = kept
    rel = os.path.relpath
    held = [rel(path, top) for path in found[0]]
    every = [rel(path, top) for path in found[1]]
    return held == rooms and every == sorted(rooms + other[:1])

SHAPES = [  # name, the recorded history, the place to keep, the commits around the hook
    ('one line', '', 'HEAD', 'new x'),
    ('merge of a recorded branch with a newer tip', 'git checkout -qb s; ok a; git checkout -q -; ok b; git checkout -q s; sleep 1; ok c; git checkout -q -', 'HEAD', 'git merge -q --no-ff s -m m'),
    ('merge made on a side branch', 'ok a; ok b', 'HEAD', 'git checkout -qb s HEAD~2; new c; git merge -q --no-ff - -m m; git checkout -q -; git reset -q --hard s'),
    ('rebase onto a recorded branch', 'git checkout -qb s; ok a; git checkout -q -; ok b', 'HEAD', 'git rebase -q s'),
    ('commit put on a second branch', 'git checkout -qb s; ok a; git checkout -q -', 's', 'put; git checkout -q s'),
    ('detached HEAD', 'ok a', 'HEAD', 'git checkout -q --detach; new x'),
    ('amend with a change', 'ok a', 'HEAD', 'echo y > a.txt; git commit -qn --amend -am y'),
    ('branch named as a file', 'git checkout -qb RULE.md; ok a', 'HEAD', 'new x'),
    ('new branch from a commit around the hook', 'ok a', 'HEAD', 'new x; git checkout -qb w'),
    ('orphan branch', 'ok a', 'HEAD', 'git checkout -q --orphan o; new x'),
]


def shape_case(tmp):
    """In each shape of history a commit around the hook is set back to the last passed place of its branch, S243."""
    lead = 'git config user.name x; git config user.email x@x; '
    lead += 'ok() { new $1; git write-tree >> .git/unit-trees; }; '  # a commit the hook passed
    lead += 'new() { echo $1 > $1.txt; git add -A; git commit -qnm $1; }; '
    lead += 'put() { export GIT_INDEX_FILE=.git/i; git read-tree s; '  # a tree of s with one more file
    lead += 'git update-index --add --cacheinfo 100644,$(echo z | git hash-object -w --stdin),z.txt; '
    lead += 't=$(git write-tree); unset GIT_INDEX_FILE; '
    lead += 'git update-ref refs/heads/s $(git commit-tree -p s -m x $t); }; '
    held = {}
    for number, (name, past, keep, around) in enumerate(SHAPES):
        made, top, room, run, own, git = fresh(tmp, f'shape{number}')
        shell = dict(shell=True, cwd=room, capture_output=True, text=True)
        tool = os.path.join(room, 'unit.py')
        check = [sys.executable, '-I', '-B', tool, 'check', room]
        subprocess.run(check, input='{}', **shell | dict(shell=False))
        subprocess.run(lead + past, **shell)
        want = run(*git, 'rev-parse', keep).stdout
        subprocess.run(lead + around, **shell)
        moved = run(*git, 'rev-parse', 'HEAD').stdout != want
        subprocess.run(check, input='{}', **shell | dict(shell=False))
        held[name] = moved and run(*git, 'rev-parse', 'HEAD').stdout == want
    return held

def urgent_case(tmp):
    """A planning unit opens in front of a planned queue on the word urgent, not without it."""
    extra = ['--accept', 'exit 0 | the tests pass']
    made, top, room, run, own, git = fresh(tmp, 'urgent', *extra)
    texts = ['Plan x', 'A0002 · S none, the planning unit', 'UNITS.md:≤30', '≤30']
    plain = run(*own, 'U0003', room, *texts)
    texts[1] = 'A0002 · S none, urgent, the owner line'
    front = run(*own, 'U0003', room, *texts)
    text = read(os.path.join(room, 'UNITS.md'))
    born = '## U0003 · ' in text and ' · structural · open' in text
    queued = ' · planned\n' in text  # the block of the queue stands
    held = plain.returncode == 1 and not front.returncode
    return held and born and queued


def audit_copy_case(tmp):
    """Each audit clause runs on its own copy: the next clause sees no file that one left, S229."""
    import audit
    import shutil
    made, top, room, run, own, git = fresh(tmp, 'auditcopy')
    copy = os.path.join(tmp, 'auditcopy-base', 'room')
    shutil.copytree(room, copy, symlinks=True)
    left = audit.rerun(copy, 'echo said > stray.txt; cat stray.txt; exit 3')
    seen = audit.rerun(copy, 'test ! -e stray.txt')
    return left == (3, 'said ') and seen[0] == 0


def audit_pack_case(tmp):
    """The packed baseline keeps each object with no loose file, the control holds, S229."""
    import audit
    import shutil
    made, top, room, run, own, git = fresh(tmp, 'auditpack')
    copy = os.path.join(tmp, 'auditpack-base', 'room')
    shutil.copytree(room, copy, symlinks=True)
    audit.pack(copy)
    count = run('git', '-C', copy, 'count-objects').stdout
    whole = run('git', '-C', copy, 'fsck', '--full').returncode == 0
    inside = os.environ.get('HECTOLINE_AUDIT')  # inside an audit clause no finer confinement runs
    held = bool(inside or audit.control(copy))
    return count.startswith('0 objects') and whole and held


def audit_cut_case(tmp):
    """The cut carries the exit of a clause red at the last audit, it reruns 0, 124 with a new one, S229."""
    import audit
    vals = {'check': 'a · b · c · d'}
    final = [('U0002', 'closed', vals), ('U0003', 'closed', {'check': 'e'})]
    exits = enumerate((0, 1, 124, 127), 1)
    old = {('U0002', k): code for k, code in exits}
    every = audit.chosen(final, {}, old)
    got = [c[:2] + c[3:] for c in every]
    carries = enumerate((None, 1, None, 127), 1)
    want = [('U0002', k, carry) for k, carry in carries]
    want.append(('U0003', 1, None))
    block = [('U0001', 'closed', None, {'added': 'sha256=none'})]
    path = os.path.join(tmp, 'receipt-cut.txt')
    open(path, 'w').write('clause 1 U0002 2: exit 1\n')
    unbound = audit.last_exits(block, {'U0001': 'audit'}, path)
    return got == want and unbound == {}


def fixture(bl):
    """The block the selftest turns open: the first planned block on a final base, else the newest."""
    final = set()
    for block in bl:
        if block[1] in ('closed', 'failed'):
            final.add(block[0])
    for block in bl:
        base = block[3].get('base', '').split()[:1]
        ready = base and base[0] in final
        if block[1] == 'planned' and ready:
            return block
    return bl[-1]
