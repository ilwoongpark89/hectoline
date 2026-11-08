#!/usr/bin/env python3
"""review.py — the independent reviewer of the hectoline arm, and the harness hook.

review.py review U#### ROOM RUN   the room's unit.py calls this at each close request. It starts a second
                                  Claude Code session that reads the diff, the nine keys and RULE.md, runs the
                                  check, and answers pass or fail with one reason. The verdict enters the review
                                  key of the block as round r<n>; the reviewer log goes to RUN/reviews/. Exit 0
                                  when a verdict was recorded, 3 when the reviewer did not answer.
review.py hook                    a Claude Code PreToolUse hook: denies a Bash line that runs unit.py close by a
                                  path other than the room's own unit.py, or a git commit outside unit.py close.
                                  Exit 2 denies. Every other call passes.
The harness never shows the reviewer the gold patch or the hidden tests; it holds neither."""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG = json.load(open(os.path.join(HERE, '..', 'design.json')))
HECTOLINE = os.path.realpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HECTOLINE)
from ledger import load, set_key, write, review_record  # noqa: E402

PROMPT = '''You are the independent reviewer of one unit in a hectoline room. The author is another agent session. You decide whether the unit may close. Read the unit block, the diff and the rule text below. Then, in the room folder {room}, run every clause of the check key yourself with Bash and read any file you need. Do not edit, write, move or delete any file, and do not run git commands that change the repository.

Fail grades, from RULE.md §4: a rule or field that cannot work; a false field; a false claim about another file; a quote that is not verbatim; a status outside the set; a check that passes at the base; a step that names no leaf move; a check clause that only proves that text exists; a change that is not what the sentence says; a diff that leaves the interface of its step. Weak style never fails a unit. Also ask: does the change stay behind the interface of its step, and does the check prove the outcome the sentence claims?

Your last line must be exactly one of:
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
    """One Claude Code session, read-only by instruction and by the room hooks, with the caps of design.json."""
    cmd = ['claude', '-p', prompt, '--model', CONFIG['model'], '--max-turns', str(CONFIG['reviewer_max_turns']),
           '--output-format', 'json', '--permission-mode', 'dontAsk',
           '--allowedTools', 'Read', 'Glob', 'Grep', 'Bash',
           '--disallowedTools', 'Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'WebSearch', 'WebFetch', 'Agent',
           '--setting-sources', 'project', '--no-session-persistence']
    start = time.time()
    try:
        proc = subprocess.run(cmd, cwd=room, capture_output=True, text=True, timeout=CONFIG['reviewer_wall_s'])
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


def review(uid, room, run):
    room = os.path.abspath(room)
    text, bl = load(room)
    vals = next((v for u, s, _, v in bl if u == uid), None)
    if vals is None:
        print(f'review: {uid} not in UNITS.md', file=sys.stderr)
        return 3
    record = review_record(vals.get('review', ''))
    rounds = {n for n, _, _ in record['rounds'] if n > 0}
    state_path = os.path.join(run, 'reviews', f'{uid.lower()}.json')
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    state = json.load(open(state_path)) if os.path.exists(state_path) else {'uid': uid, 'rounds': []}
    n = max(max(rounds, default=0), len(state['rounds'])) + 1
    diff, untracked = diff_of(room)
    rule = open(os.path.join(HECTOLINE, 'RULE.md'), encoding='utf8').read()
    prompt = PROMPT.format(room=room, uid=uid, block=block_of(room, uid), diff=diff or '(empty)', untracked=untracked, rule=rule)
    data = ask(room, prompt)
    result = str(data.get('result', ''))
    found = re.search(r'VERDICT:\s*(pass|fail)\s*[—-]*\s*(.*)', result, re.I)
    log = os.path.join(run, 'reviews', f'agent-review-{uid.lower()}-r{n}.md')
    with open(log, 'w', encoding='utf8') as f:
        f.write(f'# agent-review-{uid.lower()} round {n}\n\nmodel {CONFIG["model"]} · session {data.get("session_id", "?")} · turns {data.get("num_turns", "?")} · wall {data.get("wall_s")} s · exit {data.get("exit_code")}\n\n## Answer\n\n{result}\n')
    entry = {'round': n, 'session': data.get('session_id'), 'wall_s': data.get('wall_s'), 'turns': data.get('num_turns'), 'log': log}
    if not found:
        state['rounds'].append(dict(entry, verdict='none'))
        json.dump(state, open(state_path, 'w'), indent=1)
        print(f'review: round {n} gave no verdict, close refused, ask again', file=sys.stderr)
        return 3
    verdict = found.group(1).lower()
    reason = re.sub(r'[«»`\n]+', ' ', found.group(2)).strip()[:300] or 'no reason given'
    state['rounds'].append(dict(entry, verdict=verdict, reason=reason))
    json.dump(state, open(state_path, 'w'), indent=1)
    # the review key is rebuilt from the harness record alone, so an author-written verdict never counts
    key = ' · '.join(f'r{r["round"]} {r["verdict"]}, «{r.get("reason", "no verdict")}», model {CONFIG["model"]}, session {r.get("session")}, {os.path.relpath(r["log"], room)}'
                     for r in state['rounds'] if r['verdict'] in ('pass', 'fail'))
    write(room, set_key(load(room)[0], uid, 'review', key))
    print(f'review: round {n} {verdict}, {reason}')
    return 0


def hook():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    if payload.get('hook_event_name') != 'PreToolUse' or payload.get('tool_name') != 'Bash':
        return 0
    cmd = payload.get('tool_input', {}).get('command', '')
    if re.search(r'\S*/\S*unit\.py\s+close\b', cmd):
        print('deny: unit.py close runs only as the room\'s own «python3 -B unit.py close U#### .», the harness reviewer answers there', file=sys.stderr)
        return 2
    if re.search(r'\bgit\b[^|;&\n]*\bcommit\b', cmd) and 'unit.py' not in cmd:
        print('deny: only unit.py close commits in this room, RULE §4', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'hook':
        sys.exit(hook())
    if len(sys.argv) == 5 and sys.argv[1] == 'review':
        sys.exit(review(sys.argv[2], sys.argv[3], sys.argv[4]))
    sys.exit(print(__doc__) or 2)
