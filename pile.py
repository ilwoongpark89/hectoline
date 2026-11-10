"""Ownership discovery from canonical unit records and Git history."""
import os, re
from ledger import files_of, git, load, read
from policy import binary


def owner_of(subject, done):
    """Return the final unit named by a commit subject."""
    unit = subject.split(' ')[0]
    valid = re.match(r'U\d{4}$', unit)
    return unit if valid and unit in done else None


def pile_paths(room):
    """Select paths with pending changes or unowned commit history."""
    _, blocks = load(room)
    done = {u for u, status, _, _ in blocks
            if status in ('closed', 'failed')}
    query = ('-c', 'core.quotePath=false')
    text = git(room, *query, 'ls-files', '--modified', '--others', '--exclude-standard')
    paths = set(text.split('\n'))
    text = git(room, *query, 'diff', '--cached', '--name-only')
    paths.update(text.split('\n'))
    history = git(room, 'log', '--format=%H %s')
    commits = re.findall(r'^([0-9a-f]{40}) ?(.*)$', history, re.M)
    for commit, subject in commits:
        if owner_of(subject, done):
            continue
        text = git(room, *query, 'show', '-m', '--name-only', '--format=', commit)
        paths.update(text.split('\n'))
        text = git(room, *query, 'log', '-m', '-M', '--diff-filter=R',
                   '--name-only', '--format=', f'{commit}..HEAD')
        paths.update(text.split('\n'))
    return paths - {''}


def line_map(room, only=None):
    """Map each text line or binary blob to its final unit."""
    _, blocks = load(room)
    files = {u: set(files_of(v))
             for u, _, _, v in blocks}
    history = git(room, 'log', '--format=%H %s')
    subjects = dict(line.split(' ', 1)
                    for line in history.splitlines() if ' ' in line)
    head = git(room, 'show', 'HEAD:UNITS.md')
    done = {u for u, status, _, _ in blocks
            if status in ('closed', 'failed')}
    live = [u for u, status, _, _ in blocks
            if status in ('open', 'waiting')]
    for uid, status, _, _ in blocks:
        if status not in ('closed', 'failed'):
            continue
        pattern = rf'^## {uid} · \S+ · \w+ · (closed|failed)$'
        if not re.search(pattern, head, re.M):
            live.append(uid)
    query = ('-c', 'core.quotePath=false', 'ls-files')
    paths = git(room, *query, '--cached', '--others', '--exclude-standard')
    out = {}
    for path in paths.splitlines():
        if path == 'unit.log' or path.startswith('legacy/'):
            continue
        if only is not None and path not in only:
            continue
        full = os.path.join(room, path)
        linked = os.path.islink(full)
        blob = False
        if not linked and os.path.isfile(full):
            with open(full, 'rb') as handle:
                blob = binary(handle.read(8000))
        if blob:
            changed = git(room, 'status', '--porcelain',
                          '--untracked-files=all', '--', path)
            hashes = ['0' * 40]
            if not changed:
                hashes = [git(room, 'log', '-1', '--format=%H', '--', path)]
        else:
            porcelain = git(room, 'blame', '--line-porcelain', '--', path)
            hashes = re.findall(r'^([0-9a-f]{40}) ', porcelain, re.M)
            if not hashes:
                rows = [os.readlink(full)] if linked else read(full).splitlines()
                hashes = ['0' * 40] * len(rows)
        rows = []
        for index, chunk in enumerate(hashes, 1):
            if chunk == '0' * 40:
                unit = next((u for u in live
                             if path in files[u]), '')
            else:
                unit = owner_of(subjects.get(chunk, ''), done)
            valid = (unit and re.match(r'U\d{4}$', unit)
                     and (chunk != '0' * 40 or path in files.get(unit, ())))
            rows.append((index, unit if valid else None))
        out[path] = rows
    return out


def pile(room):
    """Print unowned line counts and return their presence."""
    total = 0
    for path, rows in line_map(room, pile_paths(room)).items():
        bad = [n for n, owner in rows
               if owner is None]
        total += len(bad)
        if bad:
            print(f'{path}: {len(bad)} pile lines, from {bad[:10]}')
    print(f'pile: {total} lines')
    return 1 if total else 0


def pile_count(room):
    """Count unowned lines in the selective ownership map."""
    mapped = line_map(room, pile_paths(room))
    return sum(1 for rows in mapped.values()
               for _, owner in rows if owner is None)
