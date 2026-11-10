#!/usr/bin/env python3
"""measure.py — the measures of a hectoline room: one computed number per goal leaf, the composition block, the status table. unit.py imports it, `unit.py status` stays the command. A room computes its leaves in its own measures.py, run in a confined worker. A room without one reads «no tool» per leaf."""
import importlib.util, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
from pile import line_map
from ledger import read, TABLES, LEDGERS, rows_of, load
from policy import at_target, binary, leaf_goals


def measures(room, bl, goals=None, fresh=False):
    """Return requested goals, optionally bypassing caches for a fresh phase."""
    selected = tuple(goals) if goals is not None else tuple(g[0] for g in rows_of(room, 'GOAL.md', 'G') if g[0] != 'G0')
    if fresh:
        return _measures(room, bl, selected, fresh=True)
    cached = _MEASURES.setdefault(os.path.realpath(room), {})
    missing = set(selected) - cached.keys()
    if missing:
        cached.update(_measures(room, bl, missing))
    return {g: cached[g] for g in selected}


def _measures(room, bl, goals=None, fresh=False):
    """The adapter of the room computes each leaf. A room without measures.py reads «no tool»."""
    selected = tuple(goals) if goals is not None else tuple(g[0] for g in rows_of(room, 'GOAL.md', 'G') if g[0] != 'G0')
    own = os.path.join(room, 'measures.py')
    if os.path.exists(own):
        return confined_adapter(room, bl, selected)
    return {g: 'no tool' for g in selected}


def met(value, target):
    """Use the shared explicit goal-acceptance policy."""
    return at_target(value, target)


def method_counts(room, bl, fresh=False):
    """The method counts of a room, RULE §5, S143: unmeasured leaves, open or todo steps under a leaf at target, final units whose files key names ledgers alone, R rows no non-ledger file cites, no pilot step, 100 levels overdue."""
    key = os.path.realpath(room)
    if not fresh and key in _COUNTS:
        return _COUNTS[key]
    try:
        m = measures(room, bl, fresh=fresh)
    except Exception as error:
        m = {}
        message = f'measures of {os.path.basename(room)}'
        message += f' raised {type(error).__name__}, every leaf reads unmeasured'
        print(message, file=sys.stderr)
    g_rows = leaf_goals(rows_of(room, 'GOAL.md', 'G'))
    unmeasured = sum(1 for g in g_rows if str(m.get(g[0], 'no tool')).startswith('no '))
    at = {g[0] for g in g_rows if g[0] in m and met(m[g[0]], g[4])}
    steps = rows_of(room, 'PLAN.md', 'S'); at_target = sum(1 for s in steps if s[-1] in ('todo', 'open') and s[1] in at)
    ledgers = {'UNITS.md', 'OWNER.md', 'PLAN.md', 'GOAL.md', 'PRODUCTS.md', 'RESEARCH.md', 'PROMPT.md', 'unit.log'}
    final = [v for u, s, _, v in bl if s in ('closed', 'failed')]
    ledger_only = sum(1 for v in final if (f := [x.split(':')[0].strip() for x in v.get('files', '').split(' · ') if x.strip()]) and set(f) <= ledgers)
    cited = set(re.findall(r'\bR\d{2,4}\b', ''.join(read(os.path.join(room, f)) for f in subprocess.run(['git', '-C', room, 'ls-files'], capture_output=True, text=True).stdout.split('\n') if f not in ledgers and os.path.isfile(os.path.join(room, f)) and not os.path.islink(os.path.join(room, f)))))
    uncited = sum(1 for r in rows_of(room, 'RESEARCH.md', 'R') if r[0] not in cited)
    pilot = 0 if any('pilot' in s[3] for s in steps) else 1
    types = unit_types(room)
    n_final = [u for u, s, _, _ in bl if s in ('closed', 'failed') and types.get(u) != 'audit']
    hundred = sum(1 for k in range(100, len(n_final) + 1, 100) if not any(types.get(u) == 'audit' and s == 'closed' and re.search(r'100 level|full inspection', v.get('sentence', '') + v.get('added', '')) for u, s, _, v in bl[bl.index(next(b for b in bl if b[0] == n_final[k - 1])):]))
    counts = {
        'unmeasured leaves': unmeasured,
        'steps under a leaf at target': at_target,
        'ledger-only units': ledger_only,
        'uncited R rows': uncited,
        'no pilot step': pilot,
        '100 levels overdue': hundred,
    }
    if not fresh:
        _COUNTS[key] = counts
    return counts


_COUNTS, _MEASURES = {}, {}


def generation_markers(vals):
    """Check recognized record markers, without claiming provenance."""
    counts = vals.get('lines', '')
    formats = ('by numstat at close', 'by staged tree at close')
    if not any(marker in counts for marker in formats):
        return False
    fields = {
        'result': 'check exits',
        'base': 'commit ',
        'files': 'at close',
    }
    return all(marker in vals.get(key, '')
               for key, marker in fields.items())


def composition(room, bl, piles=True):
    """The composition block of RULE §5: one row per item, a number or no value with its reason."""
    home, final = os.path.expanduser('~'), [(u, v) for u, s, _, v in bl if s in ('closed', 'failed')]
    try:
        groups = sum(1 for v in json.load(open(f'{home}/.claude/settings.json')).get('hooks', {}).values() for g in v if 'hooks/claude.py' in str(g))
    except (OSError, ValueError):
        groups = 'no value, no settings.json'
    codex = open(f'{home}/.codex/config.toml').read().count('hectoline hooks begin') if os.path.exists(f'{home}/.codex/config.toml') else 'no value, no config.toml'
    link = os.path.islink(os.path.join(room, '.git/hooks/pre-commit'))
    ledgers = set(TABLES) | {'UNITS.md', 'RESEARCH.md', 'unit.log'}  # the ledgers and the log grow without a cap
    caps = {f: 500 for r in rows_of(room, 'PRODUCTS.md', 'P') for f in r[4].split(', ') if f not in ledgers and (f.endswith(('.py', '.md')) or '/' in f)}  # every product file of PRODUCTS.md, S59
    blobs = {f: os.path.getsize(os.path.join(room, f)) for r in rows_of(room, 'PRODUCTS.md', 'P') for f in r[4].split(', ') if os.path.isfile(os.path.join(room, f)) and binary(open(os.path.join(room, f), 'rb').read(8000))}
    sizes = {f: sum(1 for _ in open(os.path.join(room, f), errors='ignore')) for f in caps if os.path.isfile(os.path.join(room, f)) and f not in blobs}  # binary bytes have no text-line cap
    over = [u for u, v in final if (m := re.match(r'\+(\d+) ~(\d+)', v.get('lines', ''))) and int(m[1]) + int(m[2]) > 100]
    missing = [u for u, v in final
               if int(u[1:]) >= 2 and not generation_markers(v)]  # the bootstrap block of room.py carries no markers
    marker_summary = f'{len(missing)} final blocks since the tool'
    marker_summary += ' ' + ' '.join(missing)
    rounds = sum(len(re.findall(r'r\d+ (?:fail|pass)', v.get('review', ''))) for u, v in final)
    log = read(os.path.join(room, 'unit.log'))
    return [('hooks active', ', '.join([f'{groups} Claude Code groups' if isinstance(groups, int) else groups, f'{codex} Codex block' if isinstance(codex, int) else codex, f'pre-commit link {link}'])),
            ('product sizes against caps', ' '.join(f'{f} {n}/{caps[f]}' for f, n in sizes.items()) + f' · over: {[f for f, n in sizes.items() if n > caps[f]]} · not found: {[f for f in caps if not os.path.exists(os.path.join(room, f))]} · binary bytes: {blobs}'),
            ('units over 100 lines', f'{len(over)} {" ".join(over)}'.strip()),
            ('missing generation markers', marker_summary.strip()),
            ('failed units', f'{sum(1 for u, s, _, _ in bl if s == "failed")}'),
            ('review rounds', f'{rounds} over {len(final)} final units'),
            ('denies', f'{sum(1 for l in log.splitlines() if "| deny |" in l)} in the log' if log else 'no value, no log'),
            ('piles', f'{sum(1 for rows in line_map(room).values() for _, u in rows if u is None)}' if piles else 'no value, not counted for the room table'),  # the count blames every file, the room table skips it, S120
            ('audits', f'{len(re.findall(r"^## U\d{4} · \S+ · audit · (?:closed|failed)$", read(os.path.join(room, "UNITS.md")), re.M))} of {len(final)} final')]


def status(room):
    text, bl = load(room)
    steps = rows_of(room, 'PLAN.md', 'S')
    done = sum(1 for s in steps if s[-1] == 'done')
    g_rows = rows_of(room, 'GOAL.md', 'G')
    leaves = leaf_goals(g_rows)
    m = measures(room, bl)
    at = sum(met(m.get(g[0]), g[4]) for g in leaves)
    print(f'progress {round(100 * at / len(leaves)) if leaves else 0} %, {at} / {len(leaves)} leaves')
    print(f'work count {done} / {len(steps)} steps · {len(bl)} units')
    print('\n| G | measure | target | now |\n|---|---|---|---|')
    for g in leaves:
        if g[0] in m:
            print(f'| {g[0]} | {g[3]} | {g[4]} | {m[g[0]]} |')
    print(f'| G0 | leaves at target | {len(leaves)} of {len(leaves)} | {at} of {len(leaves)} |')
    print('\n| composition | value |\n|---|---|')
    for name, value in composition(room, bl):
        print(f'| {name} | {value} |')
    print('\n| method count | value |\n|---|---|')
    for name, value in method_counts(room, bl).items():
        print(f'| {name} | {value} |')
    print('\n| U | type | status | step | lines | review |\n|---|---|---|---|---|---|')
    for u, s, _, v in bl[-10:]:
        step = re.search(r'S\d{2}|S none', v.get('plan', '')) or ''
        print(f'| {u} | {text.split(f"## {u} · ")[1].split(" · ")[1]} | {s} | {step.group(0) if step else ""} | {v.get("lines", "")[:22]} | {v.get("review", "")[:40]} |')
    if len(bl) % 5 == 0:
        print('\n| G | steps done / all |\n|---|---|')
        for g in g_rows[1:]:
            own = [s for s in steps if s[1] == g[0]]
            print(f'| {g[0]} | {sum(1 for s in own if s[-1] == "done")} / {len(own)} |')
    return 0


def unit_types(room):
    """The type of each unit, by its header line."""
    text = read(os.path.join(room, 'UNITS.md'))
    pattern = r'^## (U\d{4}) · \S+ · (\w+) ·'
    return dict(re.findall(pattern, text, re.M))


def confined_adapter(room, bl, selected, timeout=30):
    """Run external measurements with product writes and network denied."""
    import shutil
    import signal
    if not selected:
        return {}
    room = os.path.realpath(room)
    try:
        sandbox = shutil.which('sandbox-exec')
        if not sandbox:
            raise RuntimeError('confinement unavailable')
        env = dict(os.environ)
        for key in ('HECTOLINE_MEASURES', 'HECTOLINE_COUNTS'):
            env.pop(key, None)
        env['GIT_OPTIONAL_LOCKS'] = '0'
        with tempfile.TemporaryFile() as request:
            request.write(json.dumps([room, bl, selected]).encode())
            request.seek(0)
            with tempfile.NamedTemporaryFile() as output:
                path = os.path.realpath(output.name)
                profile = '(version 1)(allow default)(deny network*)'
                profile += '(deny file-write*)(allow file-write*'
                profile += ' (literal "/dev/null") (literal '
                profile += json.dumps(path) + '))'
                entry = os.path.join(HERE, 'measure.py')
                args = [sandbox, '-p', profile, sys.executable]
                args += ['-I', '-B', entry, '--adapter-worker']
                proc = subprocess.Popen(
                    args, cwd=room, env=env, stdin=request,
                    stdout=output, stderr=subprocess.DEVNULL,
                    start_new_session=True)
                try:
                    proc.wait(timeout=timeout)
                finally:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait()
                if proc.returncode:
                    raise RuntimeError('worker failed')
                output.seek(0)
                values = json.load(output)
        json.dumps(values, allow_nan=False)
        if not isinstance(values, dict):
            raise ValueError('invalid result type')
        if set(values) != set(selected):
            raise ValueError('invalid result keys')
        return values
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        reason = f'no value: adapter {type(error).__name__}'
        return {goal: reason for goal in selected}


def adapter_worker(room, bl, selected):
    """Read adapter results inside the confined worker only."""
    import contextlib
    if not selected:
        return {}
    own = os.path.join(room, 'measures.py')
    spec = importlib.util.spec_from_file_location('measures', own)
    mod = importlib.util.module_from_spec(spec)
    values = {}
    with contextlib.redirect_stdout(sys.stderr):
        spec.loader.exec_module(mod)
        for goal in selected:
            try:
                function = getattr(mod, goal.lower(), None)
                value = function(room, bl) if function else 'no tool'
                json.dumps(value, allow_nan=False)
            except Exception as error:
                value = f'no value: {type(error).__name__}'
            values[goal] = value
    return values


if __name__ == '__main__' and sys.argv[1:] == ['--adapter-worker']:
    import resource
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))
    request = json.load(sys.stdin)
    print(json.dumps(adapter_worker(*request), allow_nan=False))
