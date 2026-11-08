#!/usr/bin/env python3
"""ledger.py — the ledger reads of a hectoline room, P24, the writers follow.
unit.py imported these names until S194 moved them here, A0110.
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
        if keys != KEYS:
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


def set_key(text, uid, key, value):
    """UNITS.md text with one key of one block set to value."""
    head, rest = text.split(f'## {uid} ·', 1)
    pattern = r'^(' + re.escape(key) + r' *:).*$'
    fill = lambda m: m.group(1) + ' ' + value
    rest = re.compile(pattern, re.M).sub(fill, rest, 1)
    return head + f'## {uid} ·' + rest


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


def rows_of(room, name, letter):
    """The rows of one table as lists of stripped cells."""
    rows = []
    for row in read(os.path.join(room, name)).splitlines():
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

def round_number(token):
    """Return a positive round, zero for malformed rounds, or no round."""
    word = token.lower().removesuffix('.')
    if not word.startswith('r'):
        return None
    tail = word[1:]
    if tail.isalpha() and len(tail) > 1:
        return None
    return int(tail) if tail.isdecimal() else 0


def review_record(text):
    """Read complete neighboring tokens before interpreting round evidence."""
    mask = lambda match: ' ' * len(match[0])
    plain = re.sub(r'«[^»]*»|`[^`]*`', mask, text)
    valid = text.count('«') == text.count('»')
    valid = valid and text.count('`') % 2 == 0
    tokens = list(re.finditer(r'[^\s,;:·]+', plain))
    labels = []
    for left, right in zip(tokens, tokens[1:]):
        if labels and left.start() < labels[-1][1]:
            continue
        if not plain[left.end():right.start()].isspace():
            continue
        first = left[0].lower().removesuffix('.')
        second = right[0].lower().removesuffix('.')
        if first in ('pass', 'fail'):
            number, verdict = round_number(right[0]), first
        elif second in ('pass', 'fail'):
            number, verdict = round_number(left[0]), second
        else:
            continue
        if number is None:
            continue
        if number <= 0:
            valid = False
            continue
        start, end = left.start(), right.end()
        labels.append((start, end, number, verdict))
    events = []
    for index, (_, end, number, verdict) in enumerate(labels):
        stop = len(text)
        if index + 1 < len(labels):
            stop = labels[index + 1][0]
        note = text[end:stop].strip(' ,;·')
        events.append((number, verdict, note))
    withdrawn = re.match(r'^\s*fail,\s*withdrawn\b', plain, re.I)
    if not labels and not withdrawn and valid:
        legacy = re.match(r'^\s*(pass|fail)\b', plain, re.I)
        if legacy:
            verdict = legacy[1].lower()
            events.append((1, verdict, text[legacy.end():].strip()))
    return {
        'rounds': events,
        'valid': bool(valid),
        'withdrawn': bool(withdrawn),
    }


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

