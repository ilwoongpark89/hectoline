#!/usr/bin/env python3
"""unit.py — the gate program of the hectoline method. Commands: validate ROOM · open U#### ROOM [sentence plan files lines, appends the planning block] · close U#### ROOM · check ROOM < hook json · status ROOM · pile ROOM · selftest ROOM. close writes files from the diff, stages the named paths, signs the commit. Every open, close, check decision is one unit.log line."""
import datetime, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
from ledger import KEYS, HEADER, PLANNED, OPEN, NEED
from ledger import TABLES, LEDGERS, STEP, read, blocks
from ledger import TOKEN, schema_of, guard, cites_line
from ledger import validate_units, validate_tables, validate
from ledger import git, load, set_key, set_status, log
from ledger import write, rows_of, files_of
from ledger import review_record, verification_failures
from policy import review_decision
from transition import baseline_passes, finalize_unit
from gate import TEST, READER, WRITES, legacy_room, legacy_writes
from gate import HOME, PROTECTED, GATED_HOME, room_key, live
from gate import names_unit, room_paths, owners
from gate import gate_path


def refuse(room, event, uid, msg):
    log(room, event, uid, 'deny', msg)
    return fail(msg)


def stuck(room, bl):
    """Read blocked leaves through the room input adapter."""
    return (sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('base')).stuck(room, bl)

def open_unit(room, uid):
    text, bl = load(room)
    types, busy = dict(re.findall(r'^## (U\d{4}) · \S+ · (\w+) ·', text, re.M)), {s for _, s, _, _ in bl}  # the type of each block and the statuses in the ledger, an audit is not a planning unit
    since = sum(1 for u, s, _, _ in bl[max([i + 1 for i, (u, s, _, _) in enumerate(bl) if types.get(u) == 'audit' and s == 'closed'], default=0):] if s in ('closed', 'failed') and types.get(u) != 'audit')  # non-audit final units after the last closed audit, RULE line 82, S91
    gate = lambda kind, plan: since >= 10 and kind != 'audit' and not (since == 10 and 'S none' in plan)  # after the tenth, open accepts an audit or one planning unit
    policy = (sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('base'))
    repair = policy.repair_ready(room, bl, since, sys.argv)
    if len(sys.argv) > 7 and 'S none, queue repair' in sys.argv[5] and not repair: return refuse(room, 'open', uid, 'queue repair admission refused')
    esc = len(sys.argv) > 7 and 'S none' not in sys.argv[5] and 'planned' in busy and since < 10 and bool(row4 := next((r for r in rows_of(room, 'PLAN.md', 'S') if (st := re.search(r'\bS\d+\b', sys.argv[5])) and r[0] == st.group(0)), None)) and 'measure' in row4[2] + row4[3] and row4[1] in stuck(room, bl)  # the measure step of a leaf that blocks every planned block, S172
    if bl and uid not in types and len(sys.argv) > 7 and uid == f'U{int(bl[-1][0][1:]) + 1:04d}' and not busy & {'open', 'waiting'} and ('planned' not in busy or since >= 10 or esc or repair):
        kind = 'structural' if repair else 'behavioral' if esc else 'audit' if since > 10 or 'planned' in busy else 'structural'  # past ten, or at ten over a planned queue, only an audit can open, so the four texts open it, S91
        step = re.search(r'\bS\d+\b', sys.argv[5]); named = step and re.search(rf'\b{step.group(0)}\b', bl[-1][3].get('plan', '') + ' ' + bl[-1][3].get('added', ''))  # the planning unit names the step the work unit cites, in plan or added, S126
        if not esc and 'S none' not in sys.argv[5] and not (bl[-1][1] == 'closed' and types.get(bl[-1][0]) != 'audit' and 'S none' in bl[-1][3].get('plan', '') and named):  # a work unit on an empty queue waits for a planning unit that names its step, RULE §3, S75 S126
            return refuse(room, 'open', uid, f'{uid}: the planned queue is empty, a planning unit comes first')
        vals = dict(zip(('sentence', 'plan', 'files', 'lines'), sys.argv[4:8]), base=next((u for u, s, _, _ in reversed(bl) if s in ('closed', 'failed')), bl[-1][0]))  # the base is the last final block, open appends the block with the four texts, RULE line 65
        write(room, text.rstrip('\n') + f'\n\n## {uid} · {datetime.date.today()} · {kind} · planned\n' + '\n'.join(f'{k:<11}: {vals.get(k, "")}' for k in KEYS) + '\n')
        text, bl = load(room); types[uid] = kind
    byid = {u: (s, v) for u, s, k, v in bl}
    if uid not in byid or byid[uid][0] != 'planned':
        return refuse(room, 'open', uid, f'{uid}: no planned block')
    if gate(types.get(uid), byid[uid][1].get('plan', '')): return refuse(room, 'open', uid, f'{uid}: {since} non-audit units since the last closed audit, an audit unit comes first')
    if any(s == 'open' for _, s, _, _ in bl):
        return refuse(room, 'open', uid, f'{uid}: another unit is open')  # every refusal of open names its unit, S108
    base = byid[uid][1]['base'].split()[0]
    if byid.get(base, ('', {}))[0] not in ('closed', 'failed'):
        return refuse(room, 'open', uid, f'{uid}: base {base} not final')
    if error := policy.step_error(room, byid[uid][1], bl):
        return refuse(room, 'open', uid, f'{uid}: {error}')
    head = git(room, 'rev-parse', '--short', 'HEAD')
    write(room, set_key(set_status(text, uid, 'planned', 'open'), uid, 'base', f'{base} {byid[base][0]}, commit {head}'))
    log(room, 'open', uid, 'allow', f'queue repair on {head}' if repair else f'on {head}', os.environ.get('CLAUDE_CODE_SESSION_ID') or os.environ.get('CLAUDE_SESSION_ID', ''))
    print(f'{uid} open on {head}')
    print((sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('base')).pack(room, uid))  # the unit pack of RULE §4 «The block exists before the first edit», S161
    return 0



def review_state(room, uid, vals):
    """Combine review evidence with this unit's persisted check failures."""
    record = review_record(vals.get('review', ''))
    attempts = verification_failures(room, uid)
    return review_decision(record, attempts)


def record_check_failure(room, uid, vals, message):
    """Persist one failed verification before deciding whether work can continue."""
    refuse(room, 'close', uid, message)
    _, failures = review_state(room, uid, vals)
    return failures

def close_unit(room, uid):
    text, bl = load(room)
    found = [(s, v) for u, s, k, v in bl if u == uid and s in ('open', 'waiting')]
    if not found:
        return refuse(room, 'close', uid, f'{uid}: not open or waiting')
    status, vals = found[0]
    verdict, fails = review_state(room, uid, vals)
    if verdict not in ('pass', 'limit', 'withdrawn'):
        message = f'{uid}: review is {verdict}, no closing verdict'
        return refuse(room, 'close', uid, message)
    error = (sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('base')).repair_error(room, uid, bl)
    if error: return refuse(room, 'close', uid, error)
    final = 'closed' if verdict == 'pass' else 'failed'
    ended = f'withdrawn after {fails} failed verifications'
    if fails >= 3:
        ended = f'failed after {fails} failed verifications'
    empty = [k for k in (('review',) if final == 'failed' else ('review', 'approval', 'rejected', 'added')) if not vals.get(k)]
    if empty:
        return refuse(room, 'close', uid, f'{uid}: {" ".join(empty)} empty')
    if final == 'closed' and 'agent-review-' not in vals.get('review', ''):  # the review log file is the proof of an outside review, RULE line 74, S61
        return refuse(room, 'close', uid, f'{uid}: the review key names no agent-review file')
    if final == 'closed':
        here = os.path.dirname(os.path.realpath(__file__))
        sys.path.insert(0, here)
        linked = os.path.islink(os.path.join(room, 'RULE.md'))
        bad = 0 if linked else __import__('lines').diff_count(room)
        if bad:
            return refuse(room, 'close', uid, f'{uid}: {bad} added code lines fail the line rule, RULE §1')
    exits = []
    if final == 'closed':
        for clause in vals['check'].split(' · '):
            result = subprocess.run(
                clause.strip(), shell=True, cwd=room, capture_output=True)
            exits.append(result.returncode)
    if any(exits) and final == 'closed':
        message = f'{uid}: check exits {exits}'
        fails = record_check_failure(room, uid, vals, message)
        if fails < 3:
            return 1
        final = 'failed'
        ended = f'failed after {fails} failed verifications'
    if final == 'closed': print((sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('base')).impact(room))  # the impact list of RULE §4 «`unit.py close` refuses a failing check», before the commit, S162
    held = []
    if final == 'closed':
        held = baseline_passes(room, vals['check'])
    if held:
        message = f'{uid}: clause {held[0]} passes on a copy of HEAD'
        fails = record_check_failure(room, uid, vals, message)
        if fails < 3:
            return 1
        final = 'failed'
        ended = f'failed after {fails} failed verifications'
    addon = addon_rows(room, bl)
    if addon and final == 'closed': return refuse(room, 'close', uid, f'{uid}: {addon[0]} is a new todo row under a met leaf with no A row in its text, RULE §2 of 1.1')  # the add-on path closes at the ledger, S139
    if final == 'closed' and (past := (sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('base')).planned_errors(room, bl, uid)): return refuse(room, 'close', uid, f'{uid}: planned work is not eligible: {past[0]}')  # S173
    paths = room_paths(room, vals)
    kind = dict(re.findall(r'^## (U\d{4}) · \S+ · (\w+) ·', text, re.M)).get(uid)  # the removed lines keep their owners at HEAD, the chain of RULE §4, S96
    gone = [(p, int(a), int(b or 1)) for p in paths if p not in LEDGERS and git(room, 'ls-files', '--', p) for a, b in re.findall(r'^@@ -(\d+)(?:,(\d+))? ', git(room, 'diff', '-U0', 'HEAD', '--', p), re.M) if b != '0']  # the removed hunks by their @@ ranges, S103
    chained = [p for p, a, n in gone if any(len(owners(room, p, '', 'HEAD', (a + i, 1))) >= 3 for i in range(n))]  # each line of the hunk on its own, the chain counts per line
    if chained and kind != 'redesign' and final == 'closed': return refuse(room, 'close', uid, f'{uid}: {chained[0]}: a removed line has two earlier owners, redesign only')
    return finalize_unit(
        room, uid, status, final, vals, text,
        paths, exits, ended, refuse)


def hunks(room, paths):
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    return __import__('base').hunks(room, paths)


def fail(msg):
    print(msg, file=sys.stderr)
    return 1




def check(room, payload):
    """Return (allowed, reason) for one hook payload of the form {tool_name, tool_input, session_id}."""
    tool, inp = payload.get('tool_name', ''), payload.get('tool_input', {})
    text, bl = load(room)
    if tool == 'Bash':
        cmd = inp.get('command', '')
        if re.search(r'--no-verify|git commit[^|;&]* -[a-zA-Z]*n[a-zA-Z]*\b|core\.hooksPath|\bgit(?:\s+-[cC]\s+\S+)*\s+(?:commit-tree|update-ref|cherry-pick|merge|revert|am|rebase|pull|fast-import)(?![\w-])(?!\s+--(?:abort|quit)\b)', cmd):  # a git command that writes a commit without the pre-commit hook is a bypass too, S134
            return False, 'git bypass flag'
        if 'unit.log' in cmd and not READER.fullmatch(cmd):  # a line that names the log passes only as a read pipeline, S57
            return False, 'unit.log is append-only by unit.py, a read passes alone as one grep, tail, head, wc or cat line, or from Python'  # the deny names the forms that pass, S133
        cwd = payload.get('cwd', '')
        at = re.match(r'\s*(?:\w+=\S*[; ]+\s*)*cd\s+(\S+)\s*&&', cmd) if len(re.findall(r'\bcd\b', cmd)) == 1 else None  # one leading cd, after variable assignments too, moves the folder the relative targets resolve against, a second cd could lead back in, S84 S101
        env = dict(((k, re.sub(r'\$\{?PWD\}?', lambda m: cwd, v)) for k, v in re.findall(r'(\w+)=([^\s;]*)[; ]', cmd[:at.start(1)])), PWD=cwd) if at else {}  # the assignments before the cd give the folder its value, «P=.» and «$PWD» lead back in, S101
        cwd = os.path.join(cwd, os.path.expanduser(re.sub(r'\$\{?(\w+)\}?', lambda m: env.get(m.group(1), m.group(0)), at.group(1).strip('"\'')))) if at else cwd
        targets = [p for m in WRITES.finditer(cmd) for ops in [[t for t in re.split(r'\s?\d*[<>]', m.group(1))[0].split() if not t.startswith('-')]] for p in (ops[-1:] if m.group(0).lstrip().startswith('cp') else ops) + re.findall(r'\d*>>?\s*([^\s|;&<>]+)', m.group(1)) if (re.search(r'\.(md|py|json|toml)$|\.git/hooks', p) or room_key(room, p if os.path.isabs(os.path.expanduser(p)) else os.path.join(cwd, p)).startswith('legacy/')) and '$' not in p and not ('$' in cwd and not os.path.isabs(os.path.expanduser(p)))]  # the operands end at a redirect, every cp operand but the last is a source, S84 S86; an operand under legacy/ passes the type filter, a folder too, S119; a shell variable path is outside, the hook cannot expand it, S72
        verdicts = [gate_path(room, p if not cwd or os.path.isabs(os.path.expanduser(p)) else os.path.join(cwd, p), '', text, bl, delete=any(p in (m.group(1).split() if m.group(0).lstrip().startswith('rm') else m.group(1).split()[:-1] if m.group(0).lstrip().startswith('mv') else []) for m in WRITES.finditer(cmd))) for p in targets]  # an rm operand or an mv source is a deletion, RULE §6 allows it under the legacy link, S117  # a relative path resolves against the cwd of the call, S72
        hint = ', a «cd DIR;» is not read, the paths resolve against the session folder, write «cd DIR &&»' if re.search(r'\bcd\s+\S+\s*;', cmd) else ''  # the deny names the form the gate reads, S133
        return next(((ok, why + hint) for ok, why in verdicts if not ok), verdicts[0] if verdicts else (True, 'no file'))
    if tool in ('WebSearch', 'WebFetch', 'Agent'):  # search or dispatch only inside a research unit, Agent also for the review of a live unit, RULE §7, S76
        live = [(u, v) for u, s, _, v in bl if s in ('open', 'waiting')]
        research = any(any(os.path.basename(f) == 'RESEARCH.md' for f in files_of(v)) and v.get('sentence', '').rstrip().endswith('?') for _, v in live)  # the question with its R rows
        if research or (tool == 'Agent' and any(re.search(rf'agent-review-(\w+-)?{u.lower()}\b', inp.get('prompt', '')) for u, _ in live)):  # a room infix as in agent-review-hub-u0007
            return True, 'a research unit is live, or the review dispatch of a live unit'
        return False, f'{tool} outside a research unit, RULE §7'
    if not inp.get('file_path'):
        return True, 'no file'
    return gate_path(room, inp['file_path'], inp.get('old_string', ''), text, bl)


def check_cmd(room):
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    ok, reason = check(room, payload)
    named = re.findall(r'\bU\d{4}\b', reason)  # the unit that decided, the last one the reason names, else the first live unit, S47
    opened = named[-1] if named else next((u for u, s, _, _ in load(room)[1] if s in ('open', 'waiting')), '-')
    log(room, 'check', opened, 'allow' if ok else 'deny', reason, payload.get('session_id', ''))
    print(('allow: ' if ok else 'deny: ') + reason)
    return 0 if ok else 1


def addon_rows(room, bl):
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    return __import__('base').addon_rows(room, bl)

def owner_of(subject, done):
    """The unit a commit subject names when that unit is final, else None: a commit without a final unit is a pile, RULE §4, S127."""
    unit = subject.split(' ')[0]; return unit if re.match(r'U\d{4}$', unit) and unit in done else None


def pile_paths(room):
    """The paths that can hold a pile: the uncommitted ones, those of commits without a final unit, renames since, merges by -m in both, S127."""
    _, bl = load(room); done = {u for u, s, _, _ in bl if s in ('closed', 'failed')}; q = ('-c', 'core.quotePath=false')
    paths = set(git(room, *q, 'ls-files', '--modified', '--others', '--exclude-standard').split('\n')) | set(git(room, *q, 'diff', '--cached', '--name-only').split('\n'))  # the uncommitted paths, staged or not
    for h in [h for h, s in re.findall(r'^([0-9a-f]{40}) ?(.*)$', git(room, 'log', '--format=%H %s'), re.M) if not owner_of(s, done)]:
        paths |= set(git(room, *q, 'show', '-m', '--name-only', '--format=', h).split('\n')) | set(git(room, *q, 'log', '-m', '-M', '--diff-filter=R', '--name-only', '--format=', f'{h}..HEAD').split('\n'))
    return paths - {''}


def line_map(room, only=None):
    """Every tracked line of the room to its unit by git blame: {path: [(line_no, unit or None)]}. With only, those paths alone, S127."""
    binary = (sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) or __import__('policy')).binary
    _, bl = load(room)
    files = {u: set(files_of(v)) for u, _, _, v in bl}
    subjects = dict(l.split(' ', 1) for l in git(room, 'log', '--format=%H %s').splitlines() if ' ' in l)
    head = git(room, 'show', 'HEAD:UNITS.md')  # uncommitted lines belong to the open or waiting unit, else to the block that turns final in this commit
    done = {u for u, s, _, _ in bl if s in ('closed', 'failed')}  # a commit whose unit is not final is a pile, RULE §4
    live = [u for u, s, _, _ in bl if s in ('open', 'waiting')] + [u for u, s, _, _ in bl if s in ('closed', 'failed') and not re.search(rf'^## {u} · \S+ · \w+ · (closed|failed)$', head, re.M)]  # the closing block owns its lines beside a live unit too
    out = {}
    for path in git(room, '-c', 'core.quotePath=false', 'ls-files', '--cached', '--others', '--exclude-standard').splitlines():
        if path == 'unit.log' or path.startswith('legacy/') or only is not None and path not in only:
            continue
        if not os.path.islink(p := os.path.join(room, path)) and os.path.isfile(p) and binary(open(p, 'rb').read(8000)):
            changed = git(room, 'status', '--porcelain', '--untracked-files=all', '--', path)
            hashes = ['0' * 40] if changed else [git(room, 'log', '-1', '--format=%H', '--', path)]
        else:
            porcelain = git(room, 'blame', '--line-porcelain', '--', path)
            hashes = re.findall(r'^([0-9a-f]{40}) ', porcelain, re.M) or ['0' * 40] * len([os.readlink(p)] if os.path.islink(p) else read(p).splitlines())  # links own one row, not their target contents
        rows = []
        for i, chunk in enumerate(hashes, 1):
            unit = next((u for u in live if path in files[u]), '') if chunk == '0' * 40 else owner_of(subjects.get(chunk, ''), done)
            rows.append((i, unit if unit and re.match(r'U\d{4}$', unit) and (chunk != '0' * 40 or path in files.get(unit, ())) else None))  # a committed line belongs to the final unit of its commit
        out[path] = rows
    return out


def pile(room):
    """List every line no block names, by path, with its first ten line numbers. Exit 1 if any."""
    total = 0
    for path, rows in line_map(room, pile_paths(room)).items():
        bad = [n for n, u in rows if u is None]
        total += len(bad)
        if bad:
            print(f'{path}: {len(bad)} pile lines, from {bad[:10]}')
    print(f'pile: {total} lines')
    return 1 if total else 0


def pile_count(room):
    return sum(1 for rows in line_map(room, pile_paths(room)).values() for _, u in rows if u is None)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    room = sys.argv[3] if len(sys.argv) > 3 else '.'
    if cmd == 'validate':
        sys.exit(validate(sys.argv[2] if len(sys.argv) > 2 else '.'))
    if cmd == 'pile':
        sys.exit(pile(sys.argv[2] if len(sys.argv) > 2 else '.'))
    if cmd == 'selftest':
        sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))  # the real file's folder, the applied rooms link unit.py and not selftest.py, S85
        from selftest import selftest  # selftest.py imports unit, so the import waits for the command
        sys.exit(selftest(sys.argv[2] if len(sys.argv) > 2 else '.'))
    if cmd == 'status':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I drops the script folder
        from measure import status  # measure.py imports unit, so the import waits for the command
        sys.exit(status(sys.argv[2] if len(sys.argv) > 2 else '.'))
    if cmd == 'check':
        sys.exit(check_cmd(sys.argv[2] if len(sys.argv) > 2 else '.'))
    if cmd in ('open', 'close') and len(sys.argv) > 2:
        sys.exit({'open': open_unit, 'close': close_unit}[cmd](room, sys.argv[2]))
    sys.exit(print(__doc__) or 2)
