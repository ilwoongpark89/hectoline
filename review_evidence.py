import re
import hashlib
from pathlib import Path
from policy import review_decision


def round_number(token):
    """Return a positive round, zero for malformed rounds, or no round."""
    word = token.lower().removesuffix('.')
    if not word.startswith('r'):
        return None
    tail = word[1:]
    identifier = tail.isalpha() or re.fullmatch(
        r'[a-z_]\w+(?:-[a-z_]\w*)*(?:\(\))?', tail)
    if identifier and len(tail) > 1:
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
        gap = plain[left.end():right.start()]
        original = text[left.end():right.start()]
        multiline = any(c in original for c in '\r\n')
        if not gap.isspace() or multiline:
            continue
        first = left[0].lower().removesuffix('.')
        second = right[0].lower().removesuffix('.')
        prefix = first in ('pass', 'fail')
        if prefix and not left[0].endswith('.'):
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


ARTIFACT = r'(/[^\s,;`"]*agent-review-[^\s,;`"]*\.md)'
DIGEST = r'\bsha256=([0-9a-f]{64})(?![0-9a-f])'


REVIEW_FILE = r'agent-review-(?:\w+-)?(u\d{4})\b'


def review_file_error(text, uid, room):
    """Read the pass of the highest round from its file outside the room."""
    rounds = sorted(review_record(text)['rounds'])
    if not rounds:
        return 'the review key holds no round'
    number, _, note = rounds[-1]
    paths = set(re.findall(ARTIFACT, note))
    digests = re.findall(DIGEST, note)
    if len(paths) != 1 or len(digests) != 1:
        return 'the highest round names no single file with its sha256'
    path = Path(paths.pop()).resolve()
    inside = path.is_relative_to(Path(room).resolve())
    if inside or not path.is_file():
        return 'the review file is missing or stands inside the room'
    named = re.findall(REVIEW_FILE, path.name.lower())
    if uid.lower() not in named:
        form = 'agent-review-' + uid.lower() + '-rN.md'
        return 'the review file is not named for its unit, name it ' + form
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digests[0]:
        return 'the review file differs from its sha256'
    body = data.decode('utf-8', 'replace')
    if not re.match(r'(?:#+\s+)?' + re.escape(uid) + r'\b', body):
        return 'the review file opens with another unit'
    last = (body.strip().splitlines() or [''])[-1].strip()
    if last.upper() != f'R{number} PASS':
        return f'the review file does not end with «R{number} PASS»'
    return ''
