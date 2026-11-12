#!/usr/bin/env python3
"""audit.py — the audit of a hectoline room from its ledgers, RULE §4 line 71. `python3 -I -B audit.py N ROOM [RECEIPT]` prints the audit N, each section with its count or its list. The reruns walk a copy of the room, the room itself does not change."""
import atexit, os, re, shutil, subprocess, sys, tempfile
import hashlib, json, time
folder = os.path.dirname(os.path.realpath(__file__))  # python -I drops the script folder, the room links unit.py and measure.py beside this file
sys.path.insert(0, folder)
from pile import line_map
from ledger import read, load, rows_of, files_of, validate
from measure import measures, composition


def rerun(copy, clause):
    """Run one audit clause on its own confined copy: the exit, the output tail."""
    from transition import confined_clause, clean_env
    parent = os.path.realpath(os.path.dirname(copy))
    env = clean_env(copy)
    with tempfile.TemporaryDirectory(dir=parent) as scratch:
        fresh = os.path.join(scratch, 'room')
        shutil.copytree(copy, fresh, symlinks=True)
        marker = os.path.join(scratch, 'entered')
        said = os.path.join(scratch, 'said')
        text = f'exec > "{said}" 2>&1\n' + clause.strip()
        try:
            code = confined_clause(scratch, fresh, text, env, marker)
        except subprocess.TimeoutExpired:
            code = 124
        tail = ''
        if os.path.isfile(said):
            tail = open(said, errors='replace').read()
    return code, tail[-800:].replace('\n', ' ')


def rerun_all(copy, clauses, old):
    """Print one receipt line for each clause it is given: the exits by unit.
    A clause with an exit to carry is not rerun, its line holds that exit, so the next audit reads it.
    A clause whose exit differs from old, the last audit, gets a line «turned:»."""
    exits = {}
    for count, (uid, k, clause, carry) in enumerate(clauses, 1):
        code, tail = carry, 'carried from the last audit, not rerun'
        if carry is None:
            code, tail = rerun(copy, clause)
        print(f'clause {count} {uid} {k}: exit {code}', flush=True)
        if code:
            print('detail:', tail, flush=True)
        if old.get((uid, k), code) != code:
            print(f'turned: {uid} {k} {old[uid, k]} -> {code}', flush=True)
        exits.setdefault(uid, []).append(code)
    print('total clauses:', len(clauses), flush=True)
    return exits


def pack(copy):
    """Pack every object of the baseline copy: a clause copy then holds few files."""
    from transition import clean_env
    git = ['git', '-C', copy]
    form = '--batch-check=%(objectname)'
    quiet = dict(check=True, capture_output=True, env=clean_env(copy))
    listing = git + ['cat-file', '--batch-all-objects', form]
    names = subprocess.run(listing, **quiet).stdout
    target = os.path.join(copy, '.git', 'objects', 'pack', 'pack')
    subprocess.run(git + ['pack-objects', '-q', target], input=names, **quiet)
    subprocess.run(git + ['prune-packed'], **quiet)


def control(copy):
    """The paired control: writes outside a clause copy fail, one inside holds."""
    outside = os.path.join(os.path.dirname(copy), 'control.txt')
    roads = [f'echo x >> {outside}', f'echo x > {outside}', f'rm {outside}']
    roads.append(f'python3 -c "open(\'{outside}\', \'w\').write(\'x\')"')
    held = 0
    for road in roads:
        open(outside, 'w').write('kept')
        code = rerun(copy, road)[0]
        kept = os.path.isfile(outside) and read(outside) == 'kept'
        held += bool(code and kept)
    inside = rerun(copy, 'echo x > ok && test -s ok')[0]
    line = f'## confinement control: {held} of {len(roads)} writes outside a clause copy denied'
    print(line + f' · a write inside exits {inside}', flush=True)
    return held == len(roads) and inside == 0


def fingerprints(room):
    """The digest of each tracked file of the room, logs apart."""
    args = ['git', '-C', room, 'ls-files']
    names = subprocess.check_output(args, text=True).splitlines()
    out = {}
    for name in names:
        path = os.path.join(room, name)
        if os.path.isfile(path) and not name.endswith('.log'):
            data = open(path, 'rb').read()
            out[path] = hashlib.sha256(data).hexdigest()
    return out


def baseline(room):
    """A packed copy of the room for the clauses. Room links stay links, a hub clause tests them.
    The git hook links become files, so no clause writes through them into the room.
    A worktree has .git as a file, a leaf room inside the hub repo has none: no hooks, no pack."""
    copy = os.path.join(tempfile.mkdtemp(), 'room')
    atexit.register(shutil.rmtree, os.path.dirname(copy), ignore_errors=True)
    skip = shutil.ignore_patterns('__pycache__')
    shutil.copytree(room, copy, symlinks=True, ignore=skip)
    hooks = os.path.join(copy, '.git', 'hooks')
    links = os.scandir(hooks) if os.path.isdir(hooks) else ()
    for entry in links:
        if entry.is_symlink():
            target = os.path.realpath(entry.path)
            os.unlink(entry.path)
            shutil.copy2(target, entry.path)
    if os.path.isdir(os.path.join(copy, '.git')):
        pack(copy)
    return copy


def last_exits(bl, types, path):
    """The exits of the last closed audit by unit with clause number, read from its receipt.
    Empty when path is not the receipt whose digest that audit block binds: the run is then full."""
    bound = ''
    for uid, status, _, vals in bl:
        if status == 'closed' and types.get(uid) == 'audit':
            bound = vals.get('added', '')
    if not bound or not os.path.isfile(path):
        return {}
    data = open(path, 'rb').read()
    if hashlib.sha256(data).hexdigest() not in bound:
        return {}
    form = r'^clause \d+ (U\d{4}) (\d+): exit (-?\d+)$'
    out = {}
    text = data.decode(errors='replace')
    found = re.findall(form, text, re.M)
    for uid, k, code in found:
        out[uid, int(k)] = int(code)
    return out


def chosen(final, types, old):
    """Each clause of each closed non-audit unit: unit, number in the check, text, exit to carry.
    A clause red in old, the last audit, carries that exit, it is not rerun: any exit but 0 or 124.
    A clause at 0 runs. A clause at 124 was not read, it runs. A clause that old does not hold runs."""
    out = []
    for uid, status, vals in final:
        work = status == 'closed' and types.get(uid) != 'audit'
        if work and vals.get('check'):
            parts = vals['check'].split(' · ')
            for k, clause in enumerate(parts, 1):
                was = old.get((uid, k), 0)
                carry = None if was in (0, 124) else was
                out.append((uid, k, clause, carry))
    return out


def audit(room, n, receipt=''):
    """Print the audit n of the room: the rerun of its checks, then its structure sections."""
    if validate(room):
        print('audit refused: the room does not validate')
        return 1
    before, started = fingerprints(room), time.monotonic()
    print('fingerprints:', json.dumps(before, sort_keys=True), flush=True)
    text, bl = load(room)
    final = [(u, s, v) for u, s, _, v in bl if s in ('closed', 'failed')]
    types = dict(re.findall(r'^## (U\d{4}) · \S+ · (\w+) ·', text, re.M))
    copy = baseline(room)
    print(f'# audit {n} · {len(bl)} blocks · {len(final)} final · {sum(1 for _, s, _ in final if s == "failed")} failed')
    nested = os.environ.get('HECTOLINE_AUDIT')  # inside a clause of an outer audit: no clause, no control
    old = last_exits(bl, types, receipt)
    hundred = str(n).endswith('00')  # the 100 level reruns every clause
    cut = {} if hundred else old
    clauses = [] if nested else chosen(final, types, cut)
    run = [clause[3] for clause in clauses].count(None)
    print(f'## clauses rerun: {run} of {len(clauses)}', flush=True)
    checked = {clause[0] for clause in clauses}
    sound = bool(nested) or control(copy)
    exits = rerun_all(copy, clauses, old)
    fails = {}
    for u, e in exits.items():
        if any(e):
            fails[u] = e
    print(f'\n## check rerun on a copy: {len(fails)} of {len(checked)} closed units fail a clause now · cmd: unit.load + subprocess per clause in a copy · ' + ' '.join(f'{u}{e}' for u, e in sorted(fails.items())))
    sep = [u for u, s, v in final if any(' · ' in c for c in re.split(r' · (?=\[|grep|python3|d=|echo|test|cd |printf|f=|HOME=)', v.get('check', '')))]
    print(f'## clauses that hold the separator by the split heuristic: {len(sep)} · {" ".join(sep)} · the validate guard is the rule')
    named = {f for _, _, _, v in bl for f in files_of(v)}
    tracked = subprocess.run(['git', '-C', room, 'ls-files'], capture_output=True, text=True).stdout.split()
    print(f'## tracked files no files key names: {len([f for f in tracked if f not in named])} · cmd: git ls-files minus files keys')
    m = measures(room, bl); print('## goal measures by unit.py status: ' + ' · '.join(f'{g} {m[g]}' for g in sorted(m)))
    print('## composition: ' + ' · '.join(f'{k} {v}' for k, v in composition(room, bl)))
    a_rows = rows_of(room, 'OWNER.md', 'A')
    print(f'## active A rows that name no RULE §, U or S: {" ".join(r[0] for r in a_rows if "active" in r[6] and not re.search(r"RULE §|U\d{4}|S\d{2}", r[6])) or 0}')
    steps = rows_of(room, 'PLAN.md', 'S'); status = {u: s for u, s, _, _ in bl}
    print(f'## steps open with every unit final: {" ".join(s[0] for s in steps if s[-1] == "open" and s[-2] and all(status.get(x) in ("closed", "failed") for x in s[-2].split())) or 0}')
    print(f'## steps with no unit: {" ".join(s[0] for s in steps if not s[-2]) or 0}')
    g_rows = rows_of(room, 'GOAL.md', 'G')
    print(f'## goal leaves with no unit under any step: {" ".join(g[0] for g in g_rows if g[0] != "G0" and not any(s[1] == g[0] and s[-2] for s in steps)) or 0}')
    py = {f: read(os.path.join(room, f)) for f in tracked if f.endswith('.py')}  # the 10 level of RULE §4, duplicates and unused code, S81
    seen = {}
    for f, t in py.items():
        for l in t.splitlines():
            if len(l.strip()) > 60 and not l.strip().startswith('#'): seen.setdefault(l.strip(), set()).add(f)
    dup, allpy = [sorted(fs) for fs in seen.values() if len(fs) > 1], '\n'.join(py.values())
    unused = [f'{f}:{n}' for f, t in py.items() for n in re.findall(r'^\s*def (\w+)\(', t, re.M) if len(re.findall(rf'\b{n}\b', allpy)) == 1]
    print(f'## duplicate lines over 60 characters in two or more .py files: {len(dup)} {" ".join(",".join(fs) for fs in dup)} · unused defs, named once in every .py: {len(unused)} {" ".join(unused)} · cmd: a count over git ls-files *.py')
    print(f'## piles: {sum(1 for rows in line_map(room).values() for _, u in rows if u is None)} · cmd: unit.py pile')
    print(f'## non-audit final units: {sum(1 for u, s, v in final if types.get(u) != "audit")} · audits: {" ".join(u for u, s, v in final if types.get(u) == "audit")}')
    after = fingerprints(room)
    same = lambda p: before[p] == after.get(p)
    changed = [p for p in before if not same(p)]
    print(f'live fingerprint changes: {len(changed)} of {len(before)} files')
    print('elapsed seconds:', round(time.monotonic() - started, 1))
    return 0 if sound and not changed else 1


if __name__ == '__main__':
    given = dict(enumerate(sys.argv[1:]))
    label, room = given.get(0, '?'), given.get(1, '.')
    receipt = given.get(2, '')  # of the last closed audit, for the cut
    sys.exit(audit(room, label, receipt))
