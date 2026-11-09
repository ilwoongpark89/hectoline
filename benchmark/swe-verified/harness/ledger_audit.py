#!/usr/bin/env python3
"""ledger_audit.py RESULTS [OUT.md] — which closed units of the hectoline arm closed on a reviewer's pass, from the ledgers alone.

For every results/ledgers/<instance>/UNITS.md, each closed block after U0001 is matched against results/review-events.jsonl:
a unit counts as reviewed when a round event of that run and unit holds verdict pass. A closed unit without such an event
closed on a review key the author wrote itself, which the harness of the first six tasks did not prevent when the
reviewer session returned no verdict. Also counted per run: failed units, open units at the end, audit units closed,
reviewer rounds pass, fail and none. Every number is a count over those two files."""
import json, os, re, sys


def main(results, out=None):
    events = [json.loads(l) for l in open(os.path.join(results, 'review-events.jsonl'), encoding='utf8') if l.strip()]
    passes = {}
    for e in events:
        if e.get('kind') == 'round' and e.get('verdict') == 'pass':
            passes.setdefault(os.path.basename(os.path.dirname(e['run'])), set()).add(e['uid'])
    rows = ['| instance | closed | closed on a reviewer pass | closed without one | failed | open at end | audits | rounds pass / fail / none |', '|---|---|---|---|---|---|---|---|']
    totals = dict(closed=0, reviewed=0, self=0, failed=0, open=0, audits=0)
    ledgers = os.path.join(results, 'ledgers')
    for instance in sorted(os.listdir(ledgers)):
        path = os.path.join(ledgers, instance, 'UNITS.md')
        if not os.path.exists(path):
            continue
        text = open(path, encoding='utf8').read()
        heads = re.findall(r'^## (U\d{4}) · \S+ · (\w+) · (\w+)$', text, re.M)
        closed = [u for u, t, s in heads if s == 'closed' and u != 'U0001' and t != 'audit']
        audits = [u for u, t, s in heads if s == 'closed' and t == 'audit']
        failed = [u for u, t, s in heads if s == 'failed']
        opened = [u for u, t, s in heads if s in ('open', 'waiting')]
        reviewed = [u for u in closed if u in passes.get(instance, set())]
        mine = [e for e in events if os.path.basename(os.path.dirname(e['run'])) == instance and e.get('kind') == 'round']
        counts = [sum(e.get('verdict') == v for e in mine) for v in ('pass', 'fail', 'none')]
        rows.append(f'| {instance} | {len(closed)} | {len(reviewed)} | {len(closed) - len(reviewed)} | {len(failed)} | {len(opened)} | {len(audits)} | {counts[0]} / {counts[1]} / {counts[2]} |')
        for k, v in (('closed', len(closed)), ('reviewed', len(reviewed)), ('self', len(closed) - len(reviewed)), ('failed', len(failed)), ('open', len(opened)), ('audits', len(audits))):
            totals[k] += v
    rows.append(f'| all | {totals["closed"]} | {totals["reviewed"]} | {totals["self"]} | {totals["failed"]} | {totals["open"]} | {totals["audits"]} | |')
    body = '# Ledger audit of the hectoline arm\n\nClosed units after the bootstrap, matched against the harness reviewer record. «closed without one» means the review key was written by the author while the reviewer had given no verdict; the harness closed that path after task 6.\n\n' + '\n'.join(rows) + '\n'
    if out:
        open(out, 'w', encoding='utf8').write(body)
    print(body)
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:3]))
