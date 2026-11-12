"""Commit metadata and state transitions for a governed room."""
import subprocess
import re
from ledger import set_key, set_status, write, validate
from ledger import git, log, read, put, aside


def settle(room):
    """Set HEAD back to the last commit whose tree the commit hook passed, S243."""
    folder = git(room, 'rev-parse', '--absolute-git-dir')
    tree = git(room, 'log', '-1', '--format=%T')  # empty before the first commit
    record = folder + '/unit-trees'
    aside(record, record)  # a record path that is no plain file leaves
    passed = read(record).split()
    if tree in passed or not tree:
        return
    head = git(room, 'log', '-1', '--format=%h')
    name = git(room, 'symbolic-ref', '-q', 'HEAD') or 'HEAD'  # the full name, a short one can name a file
    rows = git(room, 'log', '-g', '--format=%h %T', name).splitlines()  # where this branch stood, the newest first
    rows += git(room, 'log', '-g', '--format=%h %T').splitlines()  # then where HEAD stood, for a branch with no passed place
    trees = [row.split()[1] for row in rows]
    known = [one in passed for one in trees]
    if True not in known:  # this branch never stood on a passed tree, its history is taken once
        put(record, git(room, 'log', '--all', '--format=%T') + '\n')
        return log(room, 'record', '', 'allow', f'history to {head} taken as passed')
    good = rows[known.index(True)].split()[0]  # the last place of the branch with a passed tree
    git(room, 'reset', '--soft', good)
    log(room, 'head', '', 'deny', f'HEAD {head} passed no hook, set back to {good}')


def git_bytes(room, *args, env=None):
    """Read checked Git output without changing path delimiters."""
    return subprocess.check_output(['git', '-C', room, *args], env=env)


def staged_changes(room):
    """Describe one immutable index tree with complete source and destination paths."""
    base = git_bytes(room, 'rev-parse', 'HEAD').decode().strip()
    tree = git_bytes(room, 'write-tree').decode().strip()
    raw = git_bytes(
        room, 'diff', '--numstat', '-z', '--find-renames', base, tree)
    entries = git_bytes(room, 'ls-tree', '-r', '-z', tree)
    blobs = {}
    for entry in entries.split(b'\0'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            blobs[path.decode()] = meta.split()[2].decode()
    tokens = iter(raw.decode().split('\0'))
    rows = []
    for token in tokens:
        if not token:
            continue
        added, deleted, path = token.split('\t', 2)
        previous = ''
        if not path:
            previous, path = next(tokens), next(tokens)
        kind = 'binary' if added == '-' else 'text'
        size = 0
        if path not in blobs:
            kind = 'deleted'
        elif kind == 'text':
            body = git_bytes(room, 'cat-file', 'blob', blobs[path])
            size = body.count(b'\n')
            size += bool(body and not body.endswith(b'\n'))
        add = None if added == '-' else int(added)
        remove = None if deleted == '-' else int(deleted)
        moved = size - add if previous and kind == 'text' else 0
        rows.append({
            'path': path, 'previous': previous,
            'added': add, 'deleted': remove,
            'lines': size, 'kind': kind,
            'moved': moved, 'base': base, 'tree': tree,
        })
    return rows


def hunks(room, paths):
    """Report actual staged ranges, including moved sources and complete destinations."""
    fields = []
    for row in staged_changes(room):
        path, old = row['path'], row['previous']
        selected = not paths or path in paths
        selected = selected or old in paths
        if not selected:
            continue
        kind, size = row['kind'], row['lines']
        spans = []
        if kind != 'text':
            spans = [kind]
        elif old:
            spans = [f'1-{size}' if size > 1 else str(size)]
            if not size:
                spans = ['empty']
        else:
            diff = git_bytes(
                room, 'diff', '-U0', row['base'], row['tree'], '--', f':(literal){path}')
            pattern = rb'^@@ -\S+ \+(\d+)(?:,(\d+))? @@'
            for start, count in re.findall(pattern, diff, re.M):
                start, count = int(start), int(count or 1)
                span = str(start)
                if count > 1:
                    span = f'{start}-{start + count - 1}'
                spans.append(span)
        if not spans:
            spans = ['metadata' if size else 'empty']
        if old:
            fields.append(f'{old}:renamed')
        fields.append(f'{path}:{",".join(spans)}')
    return ' · '.join(fields)

SANDBOX = '/usr/bin/sandbox-exec'


def writable(folder):
    """Create one probe file in a folder, then remove it."""
    import os
    path = os.path.join(folder, f'.hectoline-probe-{os.getpid()}')
    try:
        os.close(os.open(path, os.O_CREAT | os.O_EXCL))
    except OSError:
        return False
    os.remove(path)
    return True


def outer_confinement(parent):
    """True when an outer confinement bounds writes to the temp folder, S226.
    Else sandbox-exec must work, or the caller stops."""
    import os
    import tempfile
    probe = [SANDBOX, '-p', '(version 1)(allow default)', '/usr/bin/true']
    if subprocess.run(probe, capture_output=True).returncode != 71:
        return False
    scratch = os.path.realpath(tempfile.gettempdir())
    def inside(path):
        real = os.path.realpath(path)
        return real.startswith(scratch + os.sep)
    samples = [os.path.expanduser('~'), os.getcwd()]
    samples.append(os.path.dirname(scratch))
    samples.append(os.path.dirname(os.path.realpath(__file__)))
    outside = [s for s in samples if not inside(s)]
    leaks = [s for s in outside if writable(s)]
    if leaks or not inside(parent):
        raise RuntimeError('no temp-bound outer confinement, sandbox-exec fails')
    return True


def confined_clause(parent, target, clause, env, marker, timeout=60):
    """Run one clause inside its caller-owned scratch boundary."""
    import json
    import os
    import signal
    profile = '(version 1)(allow default)(deny network*)'
    profile += '(deny file-write*)(allow file-write*'
    profile += ' (subpath ' + json.dumps(parent) + ')'
    profile += ' (literal "/dev/null"))'
    if not os.path.isfile(SANDBOX):
        raise RuntimeError('baseline write confinement is unavailable')
    env.update(TMPDIR=parent, HECTOLINE_AUDIT='1')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    launch = ': > "$1" || exit 125\nexec /bin/sh -c "$2"'
    args = [SANDBOX, '-p', profile, '/bin/sh', '-c', launch]
    if outer_confinement(parent):
        args = ['/bin/sh', '-c', launch]
    args += ['baseline', marker, clause]
    proc = subprocess.Popen(
        args, cwd=target, env=env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=True)
    try:
        proc.communicate(timeout=timeout)
    finally:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        proc.wait()
    if not os.path.isfile(marker):
        raise RuntimeError('baseline sandbox did not start the clause')
    return proc.returncode

def baseline_passes(room, check):
    """Return clauses that pass on isolated HEAD."""
    return baseline_state(room, check)[0]


def clean_env(room):
    """The environment without the names git sets for a hook."""
    import os
    env = dict(os.environ)
    local = git_bytes(room, 'rev-parse', '--local-env-vars')
    for name in local.decode().splitlines():
        env.pop(name, None)
    return env


def clause_exits(room, check):
    """The exit code of each check clause run in the room, S233."""
    how = dict(shell=True, cwd=room, capture_output=True)
    how['env'] = clean_env(room)
    exits = []
    for clause in check.split(' · '):
        done = subprocess.run(clause.strip(), **how)
        exits.append(done.returncode)
    return exits


def baseline_state(room, check, timeout=60):
    """Return held and broken clauses on isolated HEAD, external writes forbidden.
    A clause that exits 127 or 124 there is broken, no red baseline, S226."""
    import os
    import tempfile
    env = clean_env(room)
    with tempfile.TemporaryDirectory(prefix='hectoline-baseline-') as parent:
        parent = os.path.realpath(parent)
        target = os.path.join(parent, 'room')
        source = os.path.abspath(room)
        git_bytes(room, 'clone', '--quiet', '--no-hardlinks',
                  '--no-checkout', '--', source, target, env=env)
        git_bytes(target, 'reset', '--hard', 'HEAD', env=env)
        held, broken = [], []
        for number, clause in enumerate(check.split(' · '), 1):
            marker = os.path.join(parent, f'entered-{number}')
            run = parent, target, clause, env, marker, timeout
            try:
                code = confined_clause(*run)
            except subprocess.TimeoutExpired:
                code = 124
            if code == 0:
                held.append(number)
            if code in (124, 127):
                broken.append((number, code))
        return held, broken


def prepare_rollback(room, paths, temporary, backups):
    """Save original products before restoring the committed state."""
    import os
    import shutil
    for number, path in enumerate(paths):
        source = os.path.join(room, path)
        parent = os.path.realpath(os.path.dirname(source))
        root = os.path.realpath(room)
        if os.path.commonpath([root, parent]) != root:
            raise ValueError('rollback path leaves the room')
        saved = os.path.join(temporary, f'backup-{number}')
        present = os.path.lexists(source)
        missing = []
        parent = os.path.dirname(os.path.abspath(source))
        while not os.path.lexists(parent):
            missing.append(parent)
            parent = os.path.dirname(parent)
        if present:
            shutil.copy2(source, saved, follow_symlinks=False)
        backups.append((source, saved, present, missing))
    for path in paths:
        source = os.path.join(room, path)
        literal = ':(literal)' + path
        tracked = git_bytes(room, 'ls-tree', '--name-only',
                            'HEAD', '--', literal)
        if tracked:
            git_bytes(room, 'restore', '--source=HEAD',
                      '--worktree', '--', literal)
        elif os.path.lexists(source):
            os.unlink(source)


def restore_backups(backups):
    """Restore product bytes, link targets, modes, and prior directory absence."""
    import os
    import shutil
    for source, saved, present, missing in backups:
        if os.path.lexists(source):
            os.unlink(source)
        if present:
            os.makedirs(os.path.dirname(source), exist_ok=True)
            shutil.copy2(saved, source, follow_symlinks=False)
        for parent in missing:
            try:
                os.rmdir(parent)
            except OSError:
                pass


def finalize_unit(
    room, uid, status, final, vals, text,
    paths, exits, ended, refuse,
):
    """Commit only this unit and restore its ledger when no commit succeeds."""
    import os
    import tempfile
    from pathlib import Path
    record = Path(room) / 'UNITS.md'
    original = record.read_bytes()
    specs = [':(literal)' + path for path in paths]
    transaction = {'committed': False, 'pathspecs': specs}
    backups = []
    previous = os.environ.get('GIT_INDEX_FILE')
    with tempfile.TemporaryDirectory(prefix='hectoline-index-') as temporary:
        try:
            os.environ['GIT_INDEX_FILE'] = os.path.join(temporary, 'index')
            git_bytes(room, 'read-tree', 'HEAD')
            if final == 'failed':
                records = {'unit.log', 'UNITS.md'}
                named = [p for p in paths
                         if p not in records]
                prepare_rollback(room, named, temporary, backups)
                paths = ['UNITS.md', 'unit.log']
                transaction['pathspecs'] = [':(literal)' + path for path in paths]
            return write_final_unit(
                room, uid, status, final, vals, text,
                paths, exits, ended, refuse, transaction)
        finally:
            if previous is None:
                os.environ.pop('GIT_INDEX_FILE', None)
            else:
                os.environ['GIT_INDEX_FILE'] = previous
            if transaction['committed']:
                git_bytes(room, 'reset', '-q', 'HEAD', '--', *specs)
            else:
                record.write_bytes(original)
                restore_backups(backups)


def write_final_unit(
    room, uid, status, final, vals, text,
    paths, exits, ended, refuse, transaction,
):
    """Write final metadata and attempt the normal commit."""
    text = set_status(text, uid, status, final)
    for key in ('result', 'lines', 'files'):
        text = set_key(text, uid, key, '-')
    write(room, text)
    git_bytes(room, 'add', '--', *transaction['pathspecs'])
    locations = hunks(room, paths) + ', from git diff -U0 at close'
    text = set_key(text, uid, 'files', locations)
    text = set_status(text, uid, final, status)
    write(room, set_status(text, uid, status, final))
    git_bytes(room, 'add', '--', ':(literal)UNITS.md')
    rows = []
    for row in staged_changes(room):
        if row['path'] == 'unit.log':
            continue
        if row['path'] in paths or row['previous'] in paths:
            rows.append(row)
    add = dele = mod = moved = 0
    details = []
    for row in rows:
        name = row['path']
        if row['previous']:
            name = f'{row["previous"]} -> {name}'
        if row['added'] is None:
            details.append(f'{name} binary')
            continue
        a, d = row['added'], row['deleted']
        add += a
        dele += d
        mod += min(a, d)
        moved += row['moved']
        details.append(f'{name} +{a} −{d}')
    outcome = f'check exits {" ".join(map(str, exits))}'
    if final == 'failed':
        reason = f'{ended}, the named paths reverted'
        outcome = reason + ', the third-fail sentence of RULE §4 · ' + outcome
    text = set_key(text, uid, 'result', ' · '.join([outcome] + details))
    counts = f'+{add - mod} ~{mod} −{dele - mod} moved {moved}'
    text = set_key(text, uid, 'lines', counts + ', by staged tree at close')
    write(room, set_status(text, uid, status, final))
    if validate(room):
        return refuse(room, 'close', uid, f'{uid}: ledgers do not validate, close refused')
    git_bytes(room, 'add', '--', ':(literal)UNITS.md')
    message = f'{uid} {vals["sentence"]}'
    if final == 'failed':
        message = f'{uid} {ended}, {vals["sentence"]}'
    args = ['git', '-C', room, 'commit', '-q', '-m', message]
    result = subprocess.run(args, capture_output=True)
    if result.returncode:
        reason = f'{uid}: the commit was refused by the git hook'
        reason += f', status back to {status}'
        return refuse(room, 'close', uid, reason)
    transaction['committed'] = True
    head = git(room, 'rev-parse', '--short', 'HEAD')
    log(room, 'close', uid, 'allow', f'{final} {head}')
    print(f'{uid} {final}, {git(room, "rev-parse", "--short", "HEAD")}')
    return 0
