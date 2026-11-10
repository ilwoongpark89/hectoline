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


def reconstruction_declarations(text):
    """Normalize explicit document declarations for the shared round policy."""
    lines, fence, quoted = [], '', False
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            closed = marker and marker[1][0] == fence[0]
            closed = closed and len(marker[1]) >= len(fence)
            if closed and not marker[2].strip():
                fence = ''
            continue
        quoted = line.lstrip().startswith('>') or quoted and line.strip()
        if quoted:
            continue
        inline = marker and marker[1][0] == '`'
        if inline and '`' in marker[2]:
            marker = None
        if marker:
            fence = marker[1]
            continue
        lines.append(line)
    if fence:
        raise ValueError('review artifact has an unclosed example fence')
    plain = '\n'.join(lines)
    mask = lambda match: re.sub(r'[^\n]', ' ', match[0])
    plain = re.sub(r'«[^«»]*»', mask, plain)
    spans = r'(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)'
    plain = re.sub(spans, mask, plain)
    if any(char in plain for char in '«»`'):
        raise ValueError('review artifact has an unclosed quote')
    direct = r'(?:Final\s+)?(r\S*)\s+(?:verdict:\s*)?(pass|fail)(?=$|[\s,;:·]|\.(?=$|\s))'
    reverse = r'(pass|fail)\s+(r\S*)'
    declaration = r'(?:Final\s+)?(r\S*)\s+(?:verdict\b|pass|fail)|(?:pass|fail)\S*\s+(r\S*)'
    def declared(line):
        match = re.match(declaration, line, re.I)
        if not match:
            return False
        label = next(filter(None, match.groups())).rstrip(',;:·')
        return round_number(label) is not None
    declarations = []
    for line in plain.splitlines():
        if line.startswith(('    ', '\t')):
            continue
        line = line.strip()
        if not declared(line):
            continue
        match = re.match(direct, line, re.I)
        if match:
            label, verdict = match[1], match[2]
        else:
            match = re.match(reverse, line, re.I)
            if match:
                label, verdict = match[2], match[1]
        if not match or round_number(label) == 0:
            raise ValueError('review artifact has a malformed declaration')
        declarations.append(label + ' ' + verdict)
        tail = re.sub(r'^[\s,;:·.]+', '', line[match.end():])
        if declared(tail):
            raise ValueError('review artifact mixes declarations on one line')
    return review_record('\n'.join(declarations))


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


def reconstruction_review(text, uid, workspace):
    """Verify one scoped artifact against committed review declarations."""
    record = review_record(text)
    if review_decision(record)[0] != 'pass':
        raise ValueError('review declaration has no passing verdict')
    quoted = r'((?:/|dispatch/)[^\x60"]*agent-review-[^\x60"]*\.md)'
    pattern = '\x60' + quoted + '\x60|' + '"' + quoted + '"|'
    pattern += r'((?:/|dispatch/)[^\s,;\x60"]*agent-review-[^\s,;\x60"]*\.md)'
    references = set()
    notes = [row[2] for row in sorted(record['rounds'])]
    for note in notes or [text]:
        matches = re.findall(pattern, note)
        current = {next(filter(None, match)) for match in matches}
        if not current and not references:
            raise ValueError('review round has no prior explicit artifact')
        references.update(current)
    workspace = Path(workspace).resolve()
    boundary = (workspace / 'dispatch').resolve()
    paths = set()
    for reference in references:
        path = Path(reference)
        path = path if path.is_absolute() else workspace / path
        path = path.resolve()
        if not path.is_relative_to(boundary):
            raise ValueError('review artifact leaves its declared boundary')
        paths.add(path)
    if len(paths) != 1:
        raise ValueError('review needs one unambiguous explicit artifact')
    digests = re.findall(r'\bsha256=([^\s,;]+)', text)
    valid = len(digests) == 1 and re.fullmatch(r'[0-9a-f]{64}', digests[0])
    if not valid:
        raise ValueError('review needs one complete artifact digest')
    path = next(iter(paths))
    if not path.is_file():
        raise ValueError('review artifact is not a regular file')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digests[0]:
        raise ValueError('review artifact differs from its bound digest')
    body = data.decode('utf-8')
    if not re.match(r'^(?:#+\s+)?' + re.escape(uid) + r'\b', body):
        raise ValueError('review artifact belongs to another unit')
    observed = reconstruction_declarations(body)
    if review_decision(observed)[0] != 'pass':
        raise ValueError('review artifact has no passing verdict')
    expected = {row[:2] for row in record['rounds']}
    actual = {row[:2] for row in observed['rounds']}
    if actual != expected:
        raise ValueError('review artifact has different round evidence')
    return dict(path=str(path), digest=digests[0], rounds=actual)
