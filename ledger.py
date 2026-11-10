#!/usr/bin/env python3
"""ledger.py — the ledger reads of a hectoline room, P24, the writers follow.
unit.py imported these names until S194 moved them here.
The state boundary: the blocks of UNITS.md and the names of the five tables."""
import datetime
import os
import re
import subprocess

KEYS = [
    'sentence', 'plan', 'delete?', 'modify?', 'duplicate', 'cause',
    'split?', 'tidy-first?', 'check', 'files', 'base', 'lines',
    'added', 'rejected', 'split', 'deleted', 'result', 'review',
    'approval',
]
TYPES = 'structural|behavioral|redesign|audit'
STATES = 'planned|open|waiting|closed|failed'
HEADER = re.compile(rf'^## (U\d{{4}}) · (\d{{4}}-\d{{2}}-\d{{2}}) · ({TYPES}) · ({STATES})$')
PLANNED = {'sentence', 'plan', 'files', 'base', 'lines'}
OPEN = set(KEYS[:12]) - {'approval'}
NEED = {
    'planned': PLANNED, 'open': OPEN, 'waiting': OPEN,
    'closed': set(KEYS), 'failed': OPEN | {'result'},
}
TABLES = {
    'OWNER.md': ('A', 7), 'GOAL.md': ('G', 6), 'PLAN.md': ('S', 7),
    'PRODUCTS.md': ('P', 6), 'RESEARCH.md': ('R', 10),
}
# the five tables, the unit ledger and the log, a redesign chain stops at them, S92
LEDGERS = set(TABLES) | {'UNITS.md', 'RESEARCH.md', 'unit.log'}
STEP = {'todo', 'open', 'done'}


def read(path):
    """The text of a file, empty when it does not exist."""
    if not os.path.exists(path):
        return ''
    with open(path, encoding='utf8', errors='replace') as handle:
        return handle.read()


def blocks(text):
    """Yield (uid, status, keys, values) per block of UNITS.md."""
    for raw in re.split(r'(?m)^(?=## U)', text)[1:]:
        lines = raw.strip().splitlines()
        match = HEADER.match(lines[0])
        if not match:
            yield lines[0][:40], None, [], {}
            continue
        pairs = []
        for line in lines[1:]:
            if ':' in line:
                pairs.append(line.split(':', 1))
        keys = [k.strip() for k, _ in pairs]
        values = {k.strip(): v.strip() for k, v in pairs}
        yield match.group(1), match.group(4), keys, values


# a capital letter outside A G P R S U followed by digits, a number outside the six letters
TOKEN = re.compile(r'(?<![\w/#-])([B-FH-OQTV-Z]\d{1,4})(?![\w-])')
CITED = r'RULE lines? \d|§\d+ line \d'


def schema_of(text):
    """Map each unit id to the schema of the last «## schema N» before it."""
    out = {}
    schema = 1
    for match in re.finditer(r'^## (schema (\d+)|(U\d{4}) ·)', text, re.M):
        if match.group(2):
            schema = int(match.group(2))
        else:
            out[match.group(3)] = schema
    return out


def guard(uid, vals):
    """Schema 3 guards: no stray number in three keys, no clause with odd quotes."""
    faults = []
    for key in ('result', 'added', 'rejected'):
        hits = sorted(set(TOKEN.findall(vals.get(key, ''))))
        if hits:
            names = ' '.join(hits)
            faults.append(f'{uid}: {key} holds a number outside the six letters, {names}')
    clauses = vals.get('check', '').split(' · ')
    for n, clause in enumerate(clauses, 1):
        if clause.count('"') % 2 or clause.count("'") % 2:
            faults.append(f'{uid}: check clause {n} has an odd quote count, the separator sits inside a quoted string')
    return faults


def cites_line(text):
    """True when a text names a RULE line number outside «» quotes, S80."""
    bare = re.sub(r'«[^»]*»', '', text)
    return bool(re.search(CITED, bare))


def budget_over(vals, budget):
    """True when file budgets exceed added plus modified lines."""
    total = 0
    for item in vals.get('files', '').split(' · '):
        found = re.search(r':≤(\d+)', item)
        if found:
            total += int(found.group(1))
    return total > budget


def validate_units(text):
    """The faults of UNITS.md: headers, keys, sentences, statuses, sizes."""
    faults = []
    last = 0
    open_count = 0
    schema = schema_of(text)
    for uid, status, keys, vals in blocks(text):
        if schema.get(uid, 1) >= 3:
            faults += guard(uid, vals)
        if status is None:
            faults.append(f'{uid}: header outside the form')
            continue
        if int(uid[1:]) <= last:
            faults.append(f'{uid}: number not increasing')
        last = int(uid[1:])
        compact = [k for k in KEYS if k in PLANNED]
        accepted = (KEYS, compact) if status == 'planned' else (KEYS,)
        if keys not in accepted:
            faults.append(f'{uid}: {len(keys)} keys or wrong order')
        if ' and ' in vals.get('sentence', ''):
            faults.append(f'{uid}: sentence holds «and»')
        live = status in ('open', 'waiting')
        if live and cites_line(' '.join(vals.values())):
            faults.append(f'{uid}: cites a RULE line number, name the § and the first words of the line')
        for key in NEED[status]:
            if not vals.get(key):
                faults.append(f'{uid}: {key} empty while {status}')
        match = re.match(r'\+≤?(\d+)(?: ~≤?(\d+))?', vals.get('lines', ''))
        total = 0
        if match:
            added = int(match.group(1))
            total = added + int(match.group(2) or 0)
        if total > 100:
            faults.append(f'{uid}: {total} lines over 100')
        if status == 'open' and match and budget_over(vals, total):
            faults.append(f'{uid}: the file budgets sum past the lines budget')
        open_count += status == 'open'
    if open_count > 1:
        faults.append(f'{open_count} open blocks')
    return faults


def live_row(letter, parts):
    """An open or todo S row, or an active A row, S80."""
    if letter == 'S':
        return parts[-1] in ('open', 'todo')
    return letter == 'A' and 'active' in parts[-1]


def validate_tables(room):
    """The faults of the five tables: cell counts, step statuses, line cites."""
    faults = []
    for name, (letter, cells) in TABLES.items():
        for row in read(os.path.join(room, name)).splitlines():
            if not re.match(r'\| ' + letter + r'\d', row):
                continue
            cells_raw = row.strip().strip('|').split('|')
            parts = [p.strip() for p in cells_raw]
            if len(parts) != cells:
                faults.append(f'{name} {parts[0]}: {len(parts)} cells, not {cells}')
                continue
            if letter == 'S' and parts[-1] not in STEP:
                faults.append(f'{name} {parts[0]}: status {parts[-1]}')
                continue
            if live_row(letter, parts) and cites_line(row):
                faults.append(f'{name} {parts[0]}: cites a RULE line number, name the § and the first words of the line')
    return faults


def validate(room):
    """Print the faults of the room, exit 1 when any."""
    faults = validate_units(read(os.path.join(room, 'UNITS.md')))
    faults += validate_tables(room)
    print('\n'.join(faults) if faults else 'validate: 0 faults')
    return 1 if faults else 0


def git(room, *args):
    """The stdout of one git command in the room, stripped."""
    args = ['git', '-C', room, *args]
    done = subprocess.run(args, capture_output=True, text=True, errors='replace')
    return done.stdout.strip()


def load(room):
    """The text of UNITS.md and its blocks as a list."""
    text = read(os.path.join(room, 'UNITS.md'))
    return text, list(blocks(text))


def reconstruction_plan(text):
    """Read the single reconstruction object from the existing plan."""
    pattern = r'^## Reconstruction(?:\n|\Z)(.*?)(?=^## |\Z)'
    sections = re.findall(pattern, text, re.M | re.S)
    if not sections:
        return None
    if len(sections) != 1:
        raise ValueError('multiple current reconstruction plans')
    body = sections[0].strip()
    found = re.fullmatch(r'```json\n(.*)\n```', body, re.S)
    if not found:
        raise ValueError('reconstruction plan needs one JSON block')
    return strict_object(found[1])


def strict_object(text):
    """Decode one object without ambiguous keys or nonfinite values."""
    import json
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate object key')
            result[key] = value
        return result
    def constant(value):
        raise ValueError('nonfinite JSON value')
    def number(value):
        parsed = float(value)
        if abs(parsed) == float('inf'):
            constant(value)
        return parsed
    if not isinstance(text, str):
        raise ValueError('object source must be text')
    value = json.loads(
        text, object_pairs_hook=pairs,
        parse_constant=constant, parse_float=number)
    if type(value) is not dict:
        raise ValueError('record must be an object')
    return value


def final_commit_order(room, blocks):
    """Read final-state transitions along the canonical Git ancestry."""
    current = {}
    for uid, status, _, _ in blocks:
        if status in ('closed', 'failed'):
            current[uid] = status
    history = git(
        room, 'log', '--first-parent', '--reverse',
        '--format=commit %H', '--diff-merges=first-parent',
        '-p', '-U0', '--', 'UNITS.md')
    order = {}
    commit = ''
    for line in history.splitlines():
        found = re.fullmatch(r'commit ([0-9a-f]{40})', line)
        if found:
            commit = found[1]
        if not line or line[0] not in '+-':
            continue
        header = HEADER.fullmatch(line[1:])
        if not header or header[4] not in ('closed', 'failed'):
            continue
        uid = header[1]
        if line[0] == '-' or uid in order:
            raise ValueError('final unit history was rewritten')
        if not commit or current.get(uid) != header[4]:
            raise ValueError('final unit differs from committed state')
        order[uid] = {'commit': commit, 'kind': header[3]}
    if set(order) != set(current):
        raise ValueError('final unit has no committed transition')
    return order


def unit_span(text, uid):
    """Locate one unit without including the next section."""
    pattern = r'(?m)^## ' + re.escape(uid)
    pattern += r' ·[^\n]*(?:\n|$)'
    matches = list(re.finditer(pattern, text))
    if len(matches) != 1:
        raise ValueError('unit header is missing or ambiguous')
    header = matches[0]
    following = re.search(r'(?m)^## ', text[header.end():])
    end = len(text)
    if following:
        end = header.end() + following.start()
    return header.start(), end


def set_key(text, uid, key, value):
    """Change one existing field within its unit only."""
    if '\n' in value or '\r' in value:
        raise ValueError('field value must be one line')
    start, end = unit_span(text, uid)
    pattern = r'^(' + re.escape(key) + r' *:).*$'
    fill = lambda match: match.group(1) + ' ' + value
    expression = re.compile(pattern, re.M)
    block, count = expression.subn(fill, text[start:end])
    if count != 1:
        raise KeyError(key)
    return text[:start] + block + text[end:]


def open_record(text, uid, base):
    """Expand one planned record without changing adjacent records."""
    start, end = unit_span(text, uid)
    body = text[start:end]
    record = next(blocks(body))
    found, status, keys, values = record
    if found != uid or status != 'planned':
        raise ValueError('record is not the requested planned unit')
    compact = [key for key in KEYS if key in PLANNED]
    if keys not in (KEYS, compact):
        raise ValueError('planned fields are not canonical')
    raw = body.splitlines()
    fields = [line for line in raw[1:] if line.strip()]
    if len(fields) != len(keys):
        raise ValueError('record has unexpected content')
    if any(not values.get(key) for key in PLANNED):
        raise ValueError('required planned field is empty')
    bad_base = not base.strip() or '\n' in base
    if bad_base or '\r' in base:
        raise ValueError('base must be one line')
    values['base'] = base
    header = raw[0].removesuffix('planned') + 'open'
    rows = [header]
    for key in KEYS:
        rows.append(f'{key:<11}: {values.get(key, "")}')
    expanded = '\n'.join(rows) + '\n\n'
    return text[:start] + expanded + text[end:]


def set_status(text, uid, old, new):
    """UNITS.md text with the header status of one block changed."""
    pattern = r'^(## ' + uid + r' · \S+ · \w+ · )' + old + '$'
    swap = r'\g<1>' + new
    return re.compile(pattern, re.M).sub(swap, text, 1)


def log(room, event, uid, verdict, reason, session=''):
    """Append one line to the log: time, event, unit, verdict, reason, session."""
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    path = os.path.join(room, 'unit.log')
    with open(path, 'a', encoding='utf8') as handle:
        handle.write(f'{stamp} | {event} | {uid} | {verdict} | {reason} | {session}\n')


def write(room, text):
    """Write the text of UNITS.md."""
    path = os.path.join(room, 'UNITS.md')
    with open(path, 'w', encoding='utf8') as handle:
        handle.write(text)


def rows_of(room, name, letter, text=None):
    """The rows of one table as lists of stripped cells."""
    if text is None:
        text = read(os.path.join(room, name))
    rows = []
    for row in text.splitlines():
        if re.match(r'\| ' + letter + r'\d', row):
            cells = row.strip().strip('|').split('|')
            rows.append([c.strip() for c in cells])
    return rows


def files_of(vals):
    """The paths of a files key, expanded, without their ranges."""
    paths = []
    for item in vals.get('files', '').split(' · '):
        if item.strip():
            paths.append(os.path.expanduser(item.split(':')[0].strip()))
    return paths

def verification_failures(room, uid):
    """Count rejected result or baseline checks for one unit."""
    history = read(os.path.join(room, 'unit.log'))
    count = 0
    for line in history.splitlines():
        fields = line.split(' | ', 5)
        if len(fields) != 6:
            continue
        if fields[1:4] != ['close', uid, 'deny']:
            continue
        reason = fields[4]
        result = reason.startswith(f'{uid}: check exits ')
        baseline = reason.startswith(f'{uid}: clause ')
        baseline = baseline and 'passes on a copy of HEAD' in reason
        count += bool(result or baseline)
    return count

