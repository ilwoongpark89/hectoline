#!/usr/bin/env python3
"""gate.py — the edit gate of a hectoline room, P25, the rules boundary.
unit.py held these names until S195 moved them here."""
import glob
import os
import re
from ledger import rows_of, files_of, git, read, load, LEDGERS
from ledger import verification_failures
from review_evidence import review_record
from policy import review_decision, replacement_chain

HERE = os.path.dirname(os.path.realpath(__file__))
# the folder that holds the rooms: the parent of this folder, or HECTOLINE_ROOMS
ROOMS = os.environ.get('HECTOLINE_ROOMS') or os.path.dirname(HERE)

def owns_path(vals, path):
    """Match one declared path scope without a sibling-prefix collision."""
    target = os.path.normpath(path)
    outside = target == '..' or target.startswith('../')
    if outside:
        return False
    for declared in files_of(vals):
        scope = os.path.normpath(declared)
        if scope == '.' and not os.path.isabs(target):
            return True
        if target == scope or target.startswith(scope + os.sep):
            return True
    return False


def editable_waiting(room, bl):
    """Select waiting units with a complete, nonterminal failed review."""
    editable = set()
    for uid, status, _, vals in bl:
        if status != 'waiting':
            continue
        record = review_record(vals.get('review', ''))
        failures = verification_failures(room, uid)
        verdict, _ = review_decision(record, failures)
        if verdict == 'fail':
            editable.add(uid)
    return editable


def waiting_owner(bl, rel, editable):
    """Find a waiting unit whose review keeps this product locked."""
    if rel == 'UNITS.md':
        return ''
    for uid, status, _, vals in bl:
        if status != 'waiting' or not owns_path(vals, rel):
            continue
        if uid not in editable:
            return uid
    return ''


def gate_path(room, path, old, text, bl, delete=False):
    """Apply ownership, review, protected-path, and redesign checks to one path."""
    key = room_key(room, path)
    absolute = os.path.isabs(os.path.expanduser(path))
    if not key and not absolute:
        return False, 'relative path leaves the room'
    rel = key or os.path.normpath(os.path.expanduser(path))
    if os.path.basename(rel) == 'unit.log':
        return False, 'unit.log is append-only by ledger.py, a changed log is restored from its shadow copy'
    if key.startswith('legacy/') and not delete:
        return False, f'{key}: the legacy folder is frozen, RULE §6, import the item through a hub unit with an owner line'
    if not key and os.path.isabs(rel):
        return True, f'{os.path.relpath(rel, room)}: outside the room'
    editable = editable_waiting(room, bl)
    locked = waiting_owner(bl, rel, editable)
    if locked:
        return False, f'{rel} belongs to waiting {locked}'
    units = live(bl, rel, editable)
    if not units:
        return False, f'{rel}: no open unit'
    uid, vals = units[0]
    for candidate, values in units:
        if owns_path(values, rel):
            uid, vals = candidate, values
            break
    allowed = {'OWNER.md', 'PLAN.md', 'UNITS.md'}
    import base
    if base.repair_baseline(room, uid) and rel not in allowed:
        return False, 'queue repair owns ledger paths only'
    if not owns_path(vals, rel):
        return False, f'{rel}: not in the files key of {uid}'
    target = os.path.realpath(os.path.join(room, rel))
    canonical = room_key(room, target) if not delete else rel
    protected = any(
        key == prefix.rstrip('/') or key.startswith(prefix)
        for key in (rel, canonical)
        for prefix in PROTECTED)
    if protected:
        approved = names_unit(room, uid, vals.get('approval', ''))
        if not approved:
            return False, f'{rel} is protected, no owner line names {uid}'
    code = []
    paths = files_of(vals) + [rel]
    for scope in files_of(vals):
        full = os.path.join(room, scope)
        scope_key = room_key(room, full)
        directory = scope.endswith('/') or os.path.isdir(full)
        if directory and scope_key and not scope_key.startswith('legacy/'):
            paths.extend(room_paths(room, {'files': scope}))
    for filename in set(paths):
        if filename in LEDGERS or filename.endswith('/'):
            continue
        if os.path.isdir(os.path.join(room, filename)):
            continue
        if not filename.endswith('.md'):
            code.append(filename)
    tests = any(TEST.search(f) for f in code)
    other = any(not TEST.search(f) for f in code)
    if tests and other:
        return False, f'{uid} mixes a test file with code'
    pattern = r'^## (U\d{4}) · \S+ · (\w+) ·'
    kind = dict(re.findall(pattern, text, re.M)).get(uid)
    source = os.path.join(room, rel)
    body = ''
    if old and os.path.isfile(source):
        body = read(source)
    start = 0
    if old and old in body:
        start = body[:body.index(old)].count('\n') + 1
    if start and kind != 'redesign':
        for offset in range(old.count('\n') + 1):
            chain = owners(room, rel, '', '', (start + offset, 1))
            if len(chain) >= 3:
                return False, f'{rel}: line has two earlier owners, redesign only'
    return True, f'{rel} in {uid}'


TEST = re.compile(r'(^|/)(tests/|test_[^/]*$|[^/]*_test\.[^/]*$)')
# a write verb and its operands, flags dropped, S86; a heredoc body is no target, S55
WRITE_VERBS = r'(?:>>?|\bsed -i\S*|\btee\b(?: -a)?|\bcp\b|\bmv\b|\brm\b)'
WRITES = re.compile(WRITE_VERBS + r'(?:[ \t]|\\\n)+((?:[^\s|;&]+(?:[ \t]|\\\n)*)+)')


def numbered_rooms(ledger=False):
    """The numbered folders under ROOMS with those one level inside each, sorted; with a ledger when asked."""
    top = ROOMS
    mark = '/[0-9][0-9]_*'
    paths = glob.glob(top + mark) + glob.glob(top + mark + mark)
    rooms = []
    for path in sorted(paths):
        has = os.path.isfile(os.path.join(path, 'UNITS.md'))
        if os.path.isdir(path) and (has or not ledger):
            rooms.append(path)
    return rooms


def legacy_room(path):
    """The room whose legacy link target holds the real path, else ''.
    A write there is frozen, RULE §6, the hooks route it to that room, S118 S124."""
    real = os.path.realpath(path)
    for room in numbered_rooms():
        link = os.path.join(room, 'legacy')
        if not os.path.islink(link):
            continue
        target = os.path.realpath(link)
        if (real + '/').startswith(target + '/'):
            return room
    return ''


def write_operands(cmd):
    """(verb, operands) per write verb of a shell line, flags dropped."""
    out = []
    for match in WRITES.finditer(cmd):
        verb = match.group(0).lstrip()[:2]
        head = re.split(r'\s?\d*[<>]', match.group(1))[0]
        tokens = head.split()
        operands = []
        for token in tokens:
            if not token.startswith('-'):
                operands.append(token)
        out.append((verb, operands))
    return out


def legacy_writes(cmd, cwd):
    """The (room, path) pairs a shell write touches under a legacy target.
    None for rm, the last operand for cp and mv, every one for the rest, S118 S124."""
    pairs = []
    for verb, operands in write_operands(cmd):
        if verb == 'rm':
            targets = []
        elif verb in ('cp', 'mv'):
            targets = operands[-1:]
        else:
            targets = operands
        for target in targets:
            full = os.path.join(cwd, os.path.expanduser(target))
            path = os.path.realpath(full)
            room = legacy_room(path)
            if room:
                pairs.append((room, path))
    return pairs


HOME = os.path.expanduser('~')
# The ten protected paths declared in RULE §4.
PROTECTED = (
    'RULE.md', 'unit.py', 'ledger.py', 'gate.py', 'selftest.py', 'hooks/', '.git/hooks/',
    'review_evidence.py',
    f'{HOME}/.claude/settings.json', f'{HOME}/.codex/config.toml',
)
# the HOME files a unit must name: the agent rule files, S72
GATED_HOME = PROTECTED + (f'{HOME}/.claude/CLAUDE.md', f'{HOME}/.codex/AGENTS.md')


def room_key(room, path):
    """The key of a path inside the room, relative; empty outside it.
    A dot folder under HOME is outside, except the gated HOME files, S72.
    A path under the legacy target reads legacy/..., frozen, RULE §6, S117."""
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.abspath(room), path)
    folder = os.path.realpath(os.path.dirname(path))
    leaf = os.path.basename(path)
    real = os.path.normpath(os.path.join(folder, leaf))
    for gated in GATED_HOME:
        if not os.path.isabs(gated):
            continue
        parent = os.path.realpath(os.path.dirname(gated))
        canonical = os.path.join(parent, os.path.basename(gated))
        if real.startswith(canonical):
            return gated + real[len(canonical):]
    if real.startswith(os.path.realpath(HOME) + '/.'):
        return ''
    link = os.path.join(room, 'legacy')
    frozen = os.path.realpath(link)
    under = (real + '/').startswith(frozen + '/')
    if os.path.islink(link) and under:
        return 'legacy/' + os.path.relpath(real, frozen)
    rel = os.path.relpath(real, os.path.realpath(room))
    return '' if (rel + '/').startswith('../') else rel


def live(bl, rel, editable):
    """Return open units plus waiting units with editable products.
    Waiting units always retain their ledger edit path."""
    out = []
    ordered = sorted(bl, key=lambda b: b[1] != 'open')
    for uid, status, _, vals in ordered:
        if status == 'open':
            out.append((uid, vals))
        elif status == 'waiting' and (rel == 'UNITS.md' or uid in editable):
            out.append((uid, vals))
    return out


from review_evidence import REVIEW_FILE


def opener(room, uid):
    """The session of the last allowed open of a unit, from the log."""
    session = ''
    for line in read(os.path.join(room, 'unit.log')).splitlines():
        cells = [c.strip() for c in line.split('|')]
        if cells[1:4] == ['open', uid, 'allow']:
            session = cells[-1]
    return session


def review_write_error(room, payload, bl, path):
    """Deny the author of a live unit a write to its review file, S225."""
    real = os.path.realpath(path)
    name = os.path.basename(path) + ' ' + os.path.basename(real)
    found = re.findall(REVIEW_FILE, name, re.I)
    units = {u.upper() for u in found}
    session = payload.get('session_id', '')
    if payload.get('agent_id') or not session:
        return ''
    for uid, status, _, _ in bl:
        named = uid in units and status in ('open', 'waiting')
        if named and opener(room, uid) == session:
            return f'{name}: the reviewer writes it, the session that opened {uid} cannot'
    return ''


def live_named(room, text):
    """The open or waiting units of a room that a file name carries."""
    found = re.findall(REVIEW_FILE, text, re.I)
    units = {u.upper() for u in found}
    out = []
    for uid, status, _, _ in load(room)[1]:
        if uid in units and status in ('open', 'waiting'):
            out.append(uid)
    return out


def review_calls(payload, cwd):
    """One Write call per room whose live unit a written review file names."""
    inp = payload.get('tool_input', {})
    paths = [inp.get('file_path') or '']
    for match in WRITES.findall(inp.get('command') or ''):
        paths.extend(match.split())
    calls = []
    for path in filter(None, paths):
        full = os.path.join(cwd, os.path.expanduser(path))
        real = os.path.basename(os.path.realpath(full))
        both = os.path.basename(full) + ' ' + real
        if not re.search(REVIEW_FILE, both, re.I):
            continue
        one = dict(payload, tool_name='Write', tool_input={'file_path': full})
        for room in numbered_rooms(ledger=True):
            if live_named(room, both):
                calls.append((room, one))
    return calls


def names_unit(room, uid, approval):
    """RULE §2: an owner line names the unit when its quote holds the number."""
    return bool(re.search(r'«[^»]*' + uid + r'[^»]*»', approval))


def room_paths(room, vals):
    """Resolve declared scopes to owned current and committed file names."""
    import subprocess
    root = os.path.realpath(room)
    out = []
    seen = set()
    commands = [
        ('ls-files', '-co', '--exclude-standard', '-z'),
        ('ls-tree', '-r', '--name-only', '-z', 'HEAD'),
    ]
    for path in files_of(vals):
        if os.path.isabs(path):
            continue
        actual = os.path.join(room, path)
        parent = os.path.realpath(os.path.dirname(actual))
        if os.path.commonpath([root, parent]) != root:
            raise ValueError('declared path leaves the room')
        literal = ':(literal)' + path
        candidates = []
        if os.path.isfile(actual) or os.path.islink(actual):
            candidates.append(path)
        for command in commands:
            args = ['git', '-C', room, *command, '--', literal]
            output = subprocess.check_output(args)
            names = output.decode('utf-8', 'surrogateescape')
            candidates.extend(names.split(chr(0)))
        for candidate in candidates:
            if not candidate or candidate in seen:
                continue
            source = os.path.join(room, candidate)
            parent = os.path.realpath(os.path.dirname(source))
            if os.path.commonpath([root, parent]) != root:
                raise ValueError('declared path leaves the room')
            seen.add(candidate)
            out.append(candidate)
    return out + ['unit.log']


def blame_units(room, blame):
    """Read unit owners from blame commit subjects."""
    units = set()
    for line in blame:
        if not line:
            continue
        commit = line.split()[0]
        subject = git(room, 'log', '-1', '--format=%s', commit)
        uid = subject.split(' ')[0]
        if re.match(r'U\d{4}$', uid):
            units.add(uid)
    return units


def owners(room, path, text, rev='', at=None):
    """Return line owners and their declared replacement chain."""
    if rev:
        body = git(room, 'show', f'{rev}:{path}') + '\n'
    else:
        body = read(os.path.join(room, path))
    if at is None and text not in body:
        return []
    if at is None:
        start = body[:body.index(text)].count('\n') + 1
        at = start, text.count(chr(10)) + 1
    start, count = at
    revision = [rev] if rev else []
    span = f'-L{start},{start + count - 1}'
    blame = git(room, 'blame', '-l', span, *revision, '--', path)
    units = blame_units(room, blame.splitlines())
    if path in LEDGERS:
        return sorted(units)
    return replacement_chain(load(room)[1], units)
