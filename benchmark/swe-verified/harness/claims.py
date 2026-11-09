#!/usr/bin/env python3
"""claims.py RUNS.jsonl WORK [--write] — recover the FIXED line of a run whose session ended without a final message.

A session killed at the wall cap, or whose Stop was refused by the room's pile hook, returns an empty result, so
run.py records «claimed: none». The session transcript under ~/.claude/projects/ still holds the last assistant
message. This reads it and sets claimed from the last «FIXED: yes|no» line found there, with claimed_source =
transcript; a run whose result already held the line keeps claimed_source = result. Without --write it only prints
what would change. Run it after the harness has ended, never beside it: it rewrites RUNS.jsonl."""
import glob, json, os, re, sys

PROJECTS = os.path.expanduser('~/.claude/projects')


def project_dir(folder):
    name = re.sub(r'[/_.]', '-', os.path.realpath(folder))
    path = os.path.join(PROJECTS, name)
    if os.path.isdir(path):
        return path
    hits = glob.glob(os.path.join(PROJECTS, name.replace('--', '-')))
    return hits[0] if hits else ''


def last_fixed(transcript):
    found = None
    for line in open(transcript, encoding='utf8', errors='replace'):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get('type') != 'assistant':
            continue
        content = d.get('message', {}).get('content', [])
        for c in content if isinstance(content, list) else []:
            if c.get('type') == 'text':
                m = re.findall(r'FIXED:\s*(yes|no)\b', c['text'], re.I)
                if m:
                    found = m[-1].lower()
    return found


def recover(run, work):
    folder = os.path.join(work, run['instance_id'], run['arm'], 'repo')
    pdir = project_dir(folder)
    if not pdir:
        return None, 'no project dir'
    files = [os.path.join(pdir, f'{run["session_id"]}.jsonl')] if run.get('session_id') else []
    files = [f for f in files if os.path.exists(f)] or sorted(glob.glob(os.path.join(pdir, '*.jsonl')), key=os.path.getmtime)
    if not files:
        return None, 'no transcript'
    return last_fixed(files[-1]), os.path.basename(files[-1])


def main(argv):
    runs_path, work = argv[0], argv[1]
    write = '--write' in argv
    rows = [json.loads(l) for l in open(runs_path) if l.strip()]
    changed = 0
    for r in rows:
        r.setdefault('claimed_source', 'result' if r.get('claimed') in ('yes', 'no') else 'none')
        if r.get('claimed') in ('yes', 'no'):
            continue
        value, where = recover(r, work)
        print(f'{r["instance_id"]} {r["arm"]}: result had none, transcript {where}: {value}')
        if value:
            r['claimed'], r['claimed_source'] = value, 'transcript'
            changed += 1
    if write:
        open(runs_path, 'w', encoding='utf8').write(''.join(json.dumps(r) + '\n' for r in rows))
    print(f'{changed} runs {"rewritten" if write else "would change"}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
