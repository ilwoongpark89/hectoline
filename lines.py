#!/usr/bin/env python3
"""lines.py — the line measure of a hectoline room, P23, G11.
A code line is one statement of at most 10 words, RULE §1.
Words are the name, number and string tokens of tokenize.
`lines.py FILE...` prints each failing line, exit 1 when any fails.
`lines.py room ROOM` prints the failing line count of the product .py files.
`lines.py diff ROOM` prints the added .py lines of the diff that fail, exit 1 when any."""
import ast
import io
import os
import re
import subprocess
import sys
import tokenize

CAP = 10
WORDS = (tokenize.NAME, tokenize.NUMBER, tokenize.STRING)


def read(path):
    with open(path, encoding='utf8', errors='replace') as handle:
        return handle.read()


def words_per_line(source):
    """The words that start on each physical line."""
    counts = {}
    reader = io.StringIO(source).readline
    for token in tokenize.generate_tokens(reader):
        if token.type in WORDS:
            line = token.start[0]
            counts[line] = counts.get(line, 0) + 1
    return counts


def starts_per_line(source):
    """The statements that start on each physical line."""
    counts = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.stmt):
            counts[node.lineno] = counts.get(node.lineno, 0) + 1
    return counts


def failing(source):
    """The numbers of the lines that fail the cap."""
    try:
        starts = starts_per_line(source)
    except SyntaxError as error:
        return [error.lineno or 1]
    words = words_per_line(source)
    total = len(source.splitlines())
    out = []
    for line in range(1, total + 1):
        dense = words.get(line, 0) > CAP
        if dense or starts.get(line, 0) > 1:
            out.append(line)
    return out


def product_files(room):
    """The .py files of the PRODUCTS.md files column, present, no links."""
    out = set()
    for row in read(os.path.join(room, 'PRODUCTS.md')).splitlines():
        if not re.match(r'\| P\d', row):
            continue
        cells = row.strip('|').split('|')
        for name in cells[4].split(','):
            full = os.path.join(room, name.strip())
            if name.strip().endswith('.py') and os.path.isfile(full):
                if not os.path.islink(full):
                    out.add(name.strip())
    return sorted(out)


def room_count(room):
    """G11: the failing lines over the product .py files."""
    total = 0
    for name in product_files(room):
        total += len(failing(read(os.path.join(room, name))))
    return total


def added_lines(room):
    """Added .py line numbers against HEAD, untracked files whole."""
    args = ['git', '-C', room, 'diff', '-U0', 'HEAD', '--', '*.py']
    text = subprocess.run(args, capture_output=True, text=True).stdout
    out = {}
    path = ''
    for line in text.splitlines():
        if line.startswith('+++ b/'):
            path = line[6:]
        if line.startswith('+++ /dev/null'):
            path = ''
        hunk = re.match(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', line)
        if hunk and path:
            start = int(hunk.group(1))
            count = int(hunk.group(2) or 1)
            out.setdefault(path, set()).update(range(start, start + count))
    args = ['git', '-C', room, 'ls-files', '--others', '--exclude-standard']
    text = subprocess.run(args, capture_output=True, text=True).stdout
    for path in text.split():
        if path.endswith('.py'):
            out[path] = None
    return out


def diff_count(room):
    """The added code lines of the diff that fail, printed."""
    total = 0
    for path, numbers in added_lines(room).items():
        full = os.path.join(room, path)
        if not os.path.isfile(full):
            continue
        source = read(full)
        bad = failing(source)
        if numbers is not None:
            bad = [n for n in bad if n in numbers]
        for n in bad:
            print(f'{path}:{n}: {source.splitlines()[n - 1].strip()[:80]}')
        total += len(bad)
    print(f'diff: {total} added code lines fail the cap')
    return total


def main(argv):
    if argv[:1] == ['diff']:
        room = argv[1] if len(argv) > 1 else '.'
        return 1 if diff_count(room) else 0
    if argv[:1] == ['room']:
        print(room_count(argv[1] if len(argv) > 1 else '.'))
        return 0
    if not argv:
        print(__doc__)
        return 2
    total = 0
    for path in argv:
        source = read(path)
        for line in failing(source):
            print(f'{path}:{line}: {source.splitlines()[line - 1].strip()[:80]}')
            total += 1
    print(f'lines: {total} fail the cap in {len(argv)} files')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
