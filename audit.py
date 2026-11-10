#!/usr/bin/env python3
"""audit.py — the audit of a hectoline room from its ledgers, RULE §4 line 71. `python3 -I -B audit.py N ROOM` prints the audit N, each section with its count or its list. The reruns walk a copy of the room, the room itself does not change."""
import atexit, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))  # python -I drops the script folder, a room reaches this file by its link, the modules stand beside the real file
from pile import line_map
from ledger import read, load, rows_of, files_of
from measure import measures, composition


def rerun(copy, clause):
    """Run one audit clause with bounded descendants and native confinement."""
    from transition import confined_clause
    parent = os.path.realpath(os.path.dirname(copy))
    env = dict(os.environ)
    args = ['git', '-C', copy, 'rev-parse', '--local-env-vars']
    local = subprocess.check_output(args).decode().splitlines()
    for name in local:
        env.pop(name, None)
    with tempfile.TemporaryDirectory(dir=parent) as scratch:
        marker = os.path.join(scratch, 'entered')
        try:
            return confined_clause(parent, copy, clause.strip(), env, marker)
        except subprocess.TimeoutExpired:
            return 124


def audit(room, n):
    text, bl = load(room)
    final = [(u, s, v) for u, s, _, v in bl if s in ('closed', 'failed')]
    types = dict(re.findall(r'^## (U\d{4}) · \S+ · (\w+) ·', text, re.M))
    copy = os.path.join(tempfile.mkdtemp(), 'room'); atexit.register(shutil.rmtree, os.path.dirname(copy), ignore_errors=True)
    shutil.copytree(room, copy, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))  # the room links stay links, a hub clause tests them
    hooks = os.path.join(copy, '.git', 'hooks')  # a worktree has .git as a file, a leaf room inside the hub repo has none
    for h in os.scandir(hooks) if os.path.isdir(hooks) else ():  # the git hook links become files, so no clause writes through them into the room, RULE line 71
        if h.is_symlink():
            target = os.path.realpath(h.path); os.unlink(h.path); shutil.copy2(target, h.path)
    print(f'# audit {n} · {len(bl)} blocks · {len(final)} final · {sum(1 for _, s, _ in final if s == "failed")} failed')
    checked = [(u, v) for u, s, v in final if s == 'closed' and v.get('check') and types.get(u) != 'audit' and not os.environ.get('HECTOLINE_AUDIT')]
    fails = {u: e for u, v in checked for e in [[rerun(copy, c) for c in v['check'].split(' · ')]] if any(e)}
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
    return 0


if __name__ == '__main__':
    sys.exit(audit(sys.argv[2] if len(sys.argv) > 2 else '.', sys.argv[1] if len(sys.argv) > 1 else '?'))
