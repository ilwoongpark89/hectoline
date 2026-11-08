#!/usr/bin/env python3
"""base.py — the structural base of a hectoline room, A0096, RULE §4 «The block exists before the first edit». `python3 -I -B base.py map ROOM` prints the room map from the ledgers at each call and never stores it, S160. `base.py pack U#### ROOM` prints the unit pack, S161. `base.py impact ROOM` prints the impact list, S162."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from ledger import read, files_of, git, load, rows_of
from transition import hunks

HEAD = 'the ledgers win over this map'


def cut(text, n=90):
    """The text on one line, at most n characters."""
    t = ' '.join(text.split()); return t if len(t) <= n else t[:n - 1] + '…'


def citers(room):
    """Each A, G, S, R, U or P id with the files that cite it, tracked or new, the basic citer graph of R55, S160 S162."""
    out = {}
    for f in subprocess.run(['git', '-C', room, 'ls-files', '-co', '--exclude-standard'], capture_output=True, text=True).stdout.split():  # tracked files and new ones not yet added
        for i in set(re.findall(r'\b[AGSRUP]\d{1,4}\b', read(os.path.join(room, f)) if os.path.isfile(os.path.join(room, f)) else '')): out.setdefault(i, set()).add(f)  # a link to a folder, the legacy link of RULE §6, is no text
    return out


def map_text(room, budget=300):
    """The room map: the active A rows, then each goal leaf with its steps, A rows, R rows and citer counts. An open or todo step shows its P and U ids as nodes with heads, a done step keeps them in its line. Done steps with the fewest citers leave first when the map passes budget lines, R42, S160."""
    cite, users, steps = citers(room), {}, rows_of(room, 'PLAN.md', 'S'); n = lambda i: len(cite.get(i, ()))
    prod = {f.strip(): (p[0], p[1]) for p in rows_of(room, 'PRODUCTS.md', 'P') for f in p[4].split(',')}; blocks = {u: (st, v.get('sentence', '')) for u, st, _, v in load(room)[1]}
    for r in rows_of(room, 'RESEARCH.md', 'R'): users.setdefault(r[-1], []).append(r[0])
    lines = [f'# {HEAD}. Read the row before you act on it. The map holds ids and heads, no verdict.']
    lines += [f'{a[0]} · {a[2]} · {cut(a[4])} · citers {n(a[0])}' for a in rows_of(room, 'OWNER.md', 'A') if a[6].startswith('active')]
    done = []
    for g in rows_of(room, 'GOAL.md', 'G'):
        lines.append(f'{g[0]} · {cut(g[1])} · target {g[4]} · citers {n(g[0])}')
        for s in sorted((s for s in steps if s[1] == g[0]), key=lambda s: (s[-1] == 'done', -n(s[0]))):
            a, r = ' '.join(sorted(set(re.findall(r'\bA\d{4}\b', s[3])))), users.get(s[0], [])
            lines.append(f'  {s[0]} · {s[-1]} · {s[-2] or "no unit"} · {s[2]} · {cut(s[3], 70)}' + (f' · {a}' if a else '') + (f' · {r[0]} to {r[-1]}' if len(r) > 1 else f' · {r[0]}' if r else '') + f' · citers {n(s[0])}')
            if s[-1] == 'done': done.append((n(s[0]), len(lines) - 1)); continue
            lines += [f'    {prod[f][0]} · {cut(prod[f][1], 60)} · {f} · citers {n(prod[f][0])}' for f in (x.strip() for x in s[2].split(',')) if f in prod]
            lines += [f'    {u} · {blocks[u][0]} · {cut(blocks[u][1], 70)} · citers {n(u)}' for u in s[-2].split() if u in blocks]
    drop = {k for _, k in sorted(done)[:max(0, len(lines) + 1 - budget)]}
    return '\n'.join([l for k, l in enumerate(lines) if k not in drop] + ([f'{len(drop)} done steps left out by the budget, PLAN.md holds them'] if drop else []))


def pack(room, uid):
    """The unit pack of RULE §4 «The block exists before the first edit»: the leaf, the step, the A quotes, the R rows that name the step or that it cites, each file of the files key with its last three final units and their fail notes, S161."""
    bl = load(room)[1]; v = next((v for u, _, _, v in bl if u == uid), None)
    if v is None: return f'{uid}: no block'
    plan = v.get('plan', ''); step = next((s for s in rows_of(room, 'PLAN.md', 'S') if re.search(rf'\b{s[0]}\b', plan)), None)
    out = [f'# unit pack of {uid}. The ledgers win over this pack.', f'{uid} · {v.get("sentence", "")}']
    out += [f'{g[0]} · {g[1]} · measure {g[3]} · target {g[4]}' for g in rows_of(room, 'GOAL.md', 'G') if step and g[0] == step[1]]
    out += [f'{step[0]} · {step[-1]} · {step[2]} · {step[3]}'] if step else ['no step, the plan key names none']
    out += [f'{a[0]} · {a[3]} · {a[4]}' for a in rows_of(room, 'OWNER.md', 'A') if re.search(rf'\b{a[0]}\b', plan)]
    out += [f'{r[0]} · {r[8]}' for r in rows_of(room, 'RESEARCH.md', 'R') if step and (r[-1] == step[0] or re.search(rf'\b{r[0]}\b', step[3]))]  # the rows that name the step, and the rows its text cites
    final = [(u, w) for u, s, _, w in bl if s in ('closed', 'failed')]
    for f in files_of(v):
        last = [(u, w) for u, w in final if f in files_of(w)][-3:]
        notes = lambda w: [cut(n.split(' · ')[0], 100) for n in re.split(r'(?=\br\d+ fail)', w.get('review', '')) if re.match(r'r\d+ fail', n)] or ['no fail']
        out.append(f'{f} · ' + (' · '.join(f'{u}: ' + ' / '.join(notes(w)) for u, w in last) if last else 'no earlier unit'))
    return '\n'.join(out)


def impact(room, rev='HEAD'):
    """The impact list of RULE §4 «`unit.py close` refuses a failing check»: every A, G, S, R and P id whose row the diff against rev changes, with each file that cites it, S162."""
    diff = subprocess.run(['git', '-C', room, 'diff', '-U0', rev, '--', 'OWNER.md', 'GOAL.md', 'PLAN.md', 'RESEARCH.md', 'PRODUCTS.md'], capture_output=True, text=True).stdout
    ids, cite = sorted(set(re.findall(r'^[+-]\| ([AGSRP]\d{1,4}) \|', diff, re.M)), key=lambda i: (i[0], int(i[1:]))), citers(room)
    return '\n'.join(['# impact list. The ledgers win over this list. Read each citer.'] + ([f'{i} · cited in ' + (', '.join(sorted(cite.get(i, ()))) or 'no file') for i in ids] or ['no A, G, S, R or P row changed']))




def addon_rows(room, bl):
    """Reject new unapproved steps under goals that already meet their targets."""
    old = set(re.findall(r'^\| (S\d+) ', git(room, 'show', 'HEAD:PLAN.md'), re.M))
    new = [l[1:] for l in git(room, 'diff', '-U0', 'HEAD', '--', 'PLAN.md').splitlines() if l.startswith('+| S') and l.split('|')[1].strip() not in old]
    rows = [[x.strip() for x in r.strip().strip('|').split('|')] for r in new]
    candidates = [c for c in rows if len(c) > 6 and c[-1] == 'todo' and not re.search(r'\bA\d{4}\b', c[3])]
    if not candidates:
        return []
    import measure
    leaves = {g[0]: g for g in measure.leaf_goals(rows_of(room, 'GOAL.md', 'G'))}
    needed = {c[1] for c in candidates} & leaves.keys()
    values = measure.measures(room, bl, needed)
    return [c[0] for c in candidates if c[1] in needed and measure.met(values.get(c[1]), leaves[c[1]][4])]


def step_error(room, vals, bl):
    """Read room inputs for the shared step policy."""
    import policy
    marker = re.search(r'^## rule 1\.1 from S(\d+)', read(os.path.join(room, 'PLAN.md')), re.M)
    error, leaf = policy.step_request(vals, rows_of(room, 'PLAN.md', 'S'), rows_of(room, 'GOAL.md', 'G'), marker)
    if error or not leaf:
        return error
    try:
        value = __import__('measure').measures(room, bl, [leaf]).get(leaf, 'no tool')
    except Exception:
        value = 'no tool'
    return policy.measurement_error(leaf, value)


def stuck(room, bl):
    """Compute only measures needed by the blocked-leaf policy."""
    import policy
    steps = {r[0]: r for r in rows_of(room, 'PLAN.md', 'S')}
    needed = policy.blocked_leaves(steps, bl, {})
    if not needed:
        return set()
    try:
        values = __import__('measure').measures(room, bl, needed)
    except Exception:
        values = {}
    return policy.blocked_leaves(steps, bl, values)

def planned_errors(room, bl, uid=None):
    """Check each newly planned block after the closing planning unit."""
    head = subprocess.run(['git', '-C', room, 'show', 'HEAD:UNITS.md'], capture_output=True, text=True).stdout
    at = next((k for k, b in enumerate(bl) if b[0] == uid), -1)
    new = [v for u, s, _, v in bl[at + 1:] if s == 'planned' and f'## {u} ·' not in head]
    return [error for v in new if (error := step_error(room, v, bl))]


from policy import REPAIR_FILES  # keep the existing caller interface


def repair_ready(room, bl, since, args):
    """Read candidate errors for the pure repair admission boundary."""
    from policy import repair_candidates
    if len(args) < 8 or 'S none, queue repair' not in args[5]:
        return False
    ready = repair_candidates(bl, since, files_of({'files': args[6]}))
    return bool(ready) and all(step_error(room, v, bl) for v in ready)


def repair_baseline(room, uid):
    pattern = rf' \| open \| {uid} \| allow \| queue repair on ([0-9a-f]+) \|'
    found = re.search(pattern, read(os.path.join(room, 'unit.log')))
    return found[1] if found else ''


def repair_error(room, uid, bl):
    """Preserve the admitted repair boundary before terminal rollback."""
    from ledger import review_record, verification_failures
    from policy import repair_invariant, review_decision
    baseline = repair_baseline(room, uid)
    if not baseline:
        return ''
    old = git(room, 'show', f'{baseline}:UNITS.md')
    path = os.path.join(room, 'UNITS.md')
    prior = read(path).split(f'## {uid} ·', 1)[0].rstrip()
    vals = next(
        v for u, _, _, v in bl
        if u == uid)
    changed = git(
        room, 'diff', '--name-only', '-z', baseline).split('\0')
    untracked = git(
        room, 'ls-files', '--others', '--exclude-standard', '-z')
    changed += untracked.split('\0')
    error = repair_invariant(
        old, prior, uid, bl, files_of(vals), changed)
    if error:
        return error
    record = review_record(vals.get('review', ''))
    failures = verification_failures(room, uid)
    verdict, _ = review_decision(record, failures)
    if verdict in ('limit', 'withdrawn'):
        return ''
    for _, status, _, planned in bl:
        if status != 'planned':
            continue
        error = step_error(room, planned, bl)
        if error:
            return error
    return ''


if __name__ == '__main__':
    if sys.argv[1:2] == ['map']: print(map_text(sys.argv[2] if len(sys.argv) > 2 else '.')); sys.exit(0)
    if sys.argv[1:2] == ['pack'] and len(sys.argv) > 2: print(pack(sys.argv[3] if len(sys.argv) > 3 else '.', sys.argv[2])); sys.exit(0)
    if sys.argv[1:2] == ['impact']: print(impact(sys.argv[2] if len(sys.argv) > 2 else '.')); sys.exit(0)
    print('usage: base.py map [ROOM] · base.py pack U#### [ROOM] · base.py impact [ROOM]'); sys.exit(2)
