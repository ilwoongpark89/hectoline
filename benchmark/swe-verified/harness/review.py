#!/usr/bin/env python3
"""review.py — the independent reviewer of the hectoline arm, and the harness hook.

review.py review U#### ROOM RUN   the room's unit.py calls this at each close request. It starts a second
                                  Claude Code session that reads the diff, the nine keys and RULE.md, runs the
                                  check, and answers pass or fail with one reason. The reviewer log goes to
                                  RUN/reviews/agent-review-u####-r<n>.md, outside the room: its first line names the
                                  unit, its last line reads «R<n> PASS» or «R<n> FAIL». The review key of the block
                                  names that file by its path with its sha256, the form unit.py close reads. Exit 0
                                  when a verdict was recorded, 3 when the reviewer did not answer. A session that
                                  ends without a verdict is kept under no_verdict and takes no round number.
                                  Every event also goes to RESULTS/review-events.jsonl, outside the run folder;
                                  the review key is rebuilt from that record, so an edit of the state file by the
                                  author changes nothing and is reported as a tamper event.
review.py hook                    a Claude Code PreToolUse hook for both arms: denies a Bash line that runs unit.py
                                  close by a path other than the room's own unit.py, every git commit typed in a
                                  room, since unit.py close commits there, every write or command that names a
                                  review file, since the reviewer of this harness writes those, and any read or
                                  write of a path under the pilot folder that is not the session's own folder,
                                  which keeps the harness and the reviewer record out of reach.
                                  Exit 2 denies. Every other call passes.
The harness never shows the reviewer the gold patch or the hidden tests; it holds neither."""
import hashlib, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.realpath(__file__))
BENCH = os.path.dirname(HERE)
CONFIG = json.load(open(os.path.join(BENCH, 'design.json')))
HECTOLINE = os.path.dirname(os.path.dirname(BENCH))
PILOT = os.path.dirname(HECTOLINE)
EVENTS = os.environ.get('HECTOLINE_EVENTS') or os.path.join(BENCH, 'results', 'review-events.jsonl')  # the room wrapper names the events file of its results folder
sys.path.insert(0, HECTOLINE)
from ledger import load, set_key, write  # noqa: E402

PROMPT = '''You are the independent reviewer of one unit in a hectoline room. The author is another agent session. You decide whether the unit may close. Read the unit block, the diff and the rule text below. Then, in the room folder {room}, run every clause of the check key yourself with Bash and read any file you need. Do not edit, write, move or delete any file, and do not run git commands that change the repository.

Fail grades, from RULE.md §4: a rule or field that cannot work; a false field; a false claim about another file; a quote that is not verbatim; a status outside the set; a check that passes at the base; a step that names no leaf move; a check clause that only proves that text exists; a change that is not what the sentence says; a diff that leaves the interface of its step. Weak style never fails a unit. Also ask: does the change stay behind the interface of its step, and does the check prove the outcome the sentence claims?

You have at most {turns} tool calls. Spend them on the check clauses and the files the block names, not on exploration. If a clause cannot run inside that budget, the verdict is fail with that reason. Your last message must end with exactly one of these two lines, and you must write it before the budget ends:
VERDICT: pass — <one reason, one sentence>
VERDICT: fail — <one reason, one sentence>

## Unit {uid}
{block}

## Diff of the working tree against HEAD, ledger files excluded
{diff}

## Untracked files
{untracked}

## RULE.md
{rule}
'''


def git(room, *args):
    return subprocess.run(['git', '-C', room, *args], capture_output=True, text=True).stdout


def block_of(room, uid):
    text = load(room)[0]
    found = re.search(rf'^## {uid} · .*?(?=^## U\d{{4}} · |\Z)', text, re.M | re.S)
    return found.group(0).strip() if found else ''


def diff_of(room):
    ledgers = ['UNITS.md', 'GOAL.md', 'PLAN.md', 'PRODUCTS.md', 'RESEARCH.md', 'OWNER.md', 'unit.log']
    diff = git(room, 'diff', 'HEAD', '--', '.', *[f':(exclude){p}' for p in ledgers])
    others = [p for p in git(room, 'ls-files', '--others', '--exclude-standard').splitlines() if p]
    parts = []
    for p in others[:20]:
        try:
            body = open(os.path.join(room, p), encoding='utf8', errors='replace').read()
        except OSError:
            body = '(unreadable)'
        parts.append(f'### {p}\n```\n{body[:6000]}\n```')
    if len(others) > 20:
        parts.append(f'... {len(others) - 20} more untracked files')
    return diff[:120000], '\n'.join(parts) or 'none'


def ask(room, prompt):
    """One Claude Code session, read-only by its tool list, with the caps of design.json. It runs from the run folder beside
    the room, not inside it, so the room's hooks, the pile check at Stop among them, do not act on the reviewer."""
    run = os.path.dirname(room)
    cmd = ['claude', '-p', prompt, '--model', CONFIG['model'], '--max-turns', str(CONFIG['reviewer_max_turns']),
           '--output-format', 'json', '--permission-mode', 'dontAsk',
           '--allowedTools', 'Read', 'Glob', 'Grep', 'Bash',
           '--disallowedTools', 'Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'WebSearch', 'WebFetch', 'Agent',
           '--setting-sources', 'project', '--no-session-persistence']
    start = time.time()
    try:
        proc = subprocess.run(cmd, cwd=run, capture_output=True, text=True, timeout=CONFIG['reviewer_wall_s'])
        out, err, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
        err, code = 'timeout', 124
    wall = round(time.time() - start, 1)
    try:
        data = json.loads(out)
    except ValueError:
        data = {'result': out, 'raw_stderr': err[-2000:]}
    data['wall_s'], data['exit_code'] = wall, code
    return data


def events_of(run, uid):
    """The harness record of this unit's reviewer sessions, from the append-only events file."""
    rounds, none = [], []
    if os.path.exists(EVENTS):
        for line in open(EVENTS, encoding='utf8'):
            if not line.strip():
                continue
            e = json.loads(line)
            if e.get('run') != run or e.get('uid') != uid or e.get('kind') != 'round':
                continue
            (rounds if e['verdict'] in ('pass', 'fail') else none).append(e)
    return rounds, none


def event(**e):
    os.makedirs(os.path.dirname(EVENTS), exist_ok=True)
    e['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(EVENTS, 'a', encoding='utf8') as f:
        f.write(json.dumps(e) + '\n')


def review(uid, room, run):
    room = os.path.abspath(room)
    text, bl = load(room)
    vals = next((v for u, s, _, v in bl if u == uid), None)
    if vals is None:
        print(f'review: {uid} not in UNITS.md', file=sys.stderr)
        return 3
    rounds, none = events_of(run, uid)
    state_path = os.path.join(run, 'reviews', f'{uid.lower()}.json')
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    if os.path.exists(state_path):
        try:
            shown = json.load(open(state_path))
        except ValueError:
            shown = None
        mine = {'uid': uid, 'rounds': [strip(r) for r in rounds], 'no_verdict': [strip(r) for r in none]}
        if shown != mine:
            event(kind='tamper', run=run, uid=uid, note='the state file differs from the harness record, the record wins')
    n = len(rounds) + 1
    diff, untracked = diff_of(room)
    rule = open(os.path.join(HECTOLINE, 'RULE.md'), encoding='utf8').read()
    prompt = PROMPT.format(room=room, uid=uid, turns=CONFIG['reviewer_max_turns'], block=block_of(room, uid), diff=diff or '(empty)', untracked=untracked, rule=rule)
    data = ask(room, prompt)
    result = str(data.get('result', ''))
    found = re.search(r'VERDICT:\s*(pass|fail)\s*[—-]*\s*(.*)', result, re.I)
    tag = f'r{n}' if found else f'none{len(none) + 1}'
    log = os.path.join(run, 'reviews', f'agent-review-{uid.lower()}-{tag}.md')
    with open(log, 'w', encoding='utf8') as f:
        last = f'R{n} {found.group(1).upper()}' if found else 'NO VERDICT'  # unit.py close and the pre-commit read the verdict from this last line
        f.write(f'# {uid} {tag}\n\nmodel {CONFIG["model"]} · session {data.get("session_id", "?")} · turns {data.get("num_turns", "?")} · wall {data.get("wall_s")} s · exit {data.get("exit_code")}\n\n## Answer\n\n{result}\n\n{last}\n')
    entry = dict(kind='round', run=run, uid=uid, round=n if found else None, session=data.get('session_id'), wall_s=data.get('wall_s'), turns=data.get('num_turns'), exit_code=data.get('exit_code'), log=log)
    if not found:
        entry['verdict'] = 'none'
        event(**entry)
        none.append(entry)
        json.dump({'uid': uid, 'rounds': [strip(r) for r in rounds], 'no_verdict': [strip(r) for r in none]}, open(state_path, 'w'), indent=1)
        if not rounds:  # the key is rebuilt here too, so an author-written verdict never stands while the reviewer has not answered
            write(room, set_key(load(room)[0], uid, 'review', f'no verdict yet: {len(none)} reviewer session(s) ended without an answer, close waits for a round'))
        print(f'review: the reviewer session ended without a verdict ({len(none)} so far), close refused, ask again', file=sys.stderr)
        return 3
    entry['verdict'] = found.group(1).lower()
    entry['reason'] = re.sub(r'[«»`\n]+', ' ', found.group(2)).replace('sha256=', 'sha256 ').replace('agent-review', 'agent review').strip()[:300] or 'no reason given'
    entry['sha256'] = hashlib.sha256(open(log, 'rb').read()).hexdigest()
    event(**entry)
    rounds.append(entry)
    json.dump({'uid': uid, 'rounds': [strip(r) for r in rounds], 'no_verdict': [strip(r) for r in none]}, open(state_path, 'w'), indent=1)
    # the review key is rebuilt from the harness record alone, so an author-written verdict never counts
    key = ' · '.join(f'r{r["round"]} {r["verdict"]}, «{r.get("reason", "no reason")}», model {CONFIG["model"]}, session {r.get("session")}, {os.path.realpath(r["log"])} sha256={r.get("sha256") or hashlib.sha256(open(r["log"], "rb").read()).hexdigest()}' for r in rounds)
    write(room, set_key(load(room)[0], uid, 'review', key))
    print(f'review: round {n} {entry["verdict"]}, {entry["reason"]}')
    return 0


def strip(r):
    return {k: v for k, v in r.items() if k not in ('kind', 'run', 'time') and v is not None}


def hook():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    if payload.get('hook_event_name') != 'PreToolUse':
        return 0
    tool, inp = payload.get('tool_name', ''), payload.get('tool_input', {})
    room = os.path.realpath(payload.get('cwd') or os.getcwd())
    fences = [PILOT, os.path.dirname(os.path.dirname(room))]  # the harness folder and the run folder WORK/<task>, which holds the reviewer record
    outside = lambda p: any(p.startswith(f + os.sep) for f in fences) and not (p + os.sep).startswith(room + os.sep)
    if tool in ('Read', 'Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'Glob', 'Grep'):
        for key in ('file_path', 'path', 'notebook_path'):
            p = inp.get(key)
            if p and tool not in ('Read', 'Glob', 'Grep') and 'agent-review-' in p:
                print('deny: a review file is written by the harness reviewer alone', file=sys.stderr)
                return 2
            if p and outside(os.path.realpath(os.path.join(room, os.path.expanduser(p)))):
                print(f'deny: {p} is outside this folder, the task text says so', file=sys.stderr)
                return 2
        return 0
    if tool != 'Bash':
        return 0
    cmd = inp.get('command', '')
    if 'agent-review-' in cmd:
        print('deny: a review file is written by the harness reviewer alone, a command does not name one', file=sys.stderr)
        return 2
    for m in re.finditer(re.escape(PILOT) + r'\S*', cmd):
        if outside(os.path.realpath(m.group(0).rstrip('/\'"`;)'))):
            print(f'deny: {m.group(0)} is outside this folder, the task text says so', file=sys.stderr)
            return 2
    if re.search(r'\S*/\S*unit\.py\s+close\b', cmd):
        print('deny: unit.py close runs only as the room\'s own «python3 -B unit.py close U#### .», the harness reviewer answers there', file=sys.stderr)
        return 2
    if re.search(r'\bgit\b[^|;&\n]*\bcommit\b', cmd) and os.path.exists(os.path.join(room, 'UNITS.md')):
        print('deny: only unit.py close commits in this room, RULE §4', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'hook':
        sys.exit(hook())
    if len(sys.argv) == 5 and sys.argv[1] == 'review':
        sys.exit(review(sys.argv[2], sys.argv[3], sys.argv[4]))
    sys.exit(print(__doc__) or 2)
