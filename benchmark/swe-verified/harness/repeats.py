#!/usr/bin/env python3
"""repeats.py [RESULTS] — the refusal counts of a results folder, from its room logs and its reviewer record.

Prints the refusals per run, and how many of them repeat a text the same run had already shown.
A refusal is a deny line of the room log. Two refusals hold the same text when they are equal
after every unit number and every digit is masked. Then the reviewer rounds with their minutes,
for the runs of runs.jsonl, and the session minutes of the hectoline arm."""
import json, os, re, sys

HERE = os.path.dirname(os.path.realpath(__file__))
RESULTS = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'results')
LOG = 'unit' + '.log'


def refusals(path):
    """The masked refusal texts of one room log, in order."""
    texts = []
    for line in open(path, encoding='utf8', errors='replace'):
        parts = line.rstrip('\n').split(' | ')
        if len(parts) > 4 and parts[3] == 'deny':
            texts.append(re.sub(r'\d', '#', re.sub(r'U\d{4}', 'U####', parts[4])))
    return texts


def main():
    total = repeated = 0
    folder = os.path.join(RESULTS, 'ledgers')
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name, LOG)
        if not os.path.isfile(path):
            continue
        texts, seen, again = refusals(path), set(), 0
        for text in texts:
            again += text in seen
            seen.add(text)
        print(f'{name}: {len(texts)} refusals, {again} repeat an earlier text of the run')
        total += len(texts)
        repeated += again
    print(f'all runs: {total} refusals, {repeated} repeat an earlier text of their run')
    runs = [json.loads(l) for l in open(os.path.join(RESULTS, 'runs.jsonl'), encoding='utf8') if l.strip()]
    mine = [r for r in runs if str(r.get('arm', '')).startswith('hectoline')]
    print(f'hectoline arm: {len(mine)} runs, {sum(r.get("wall_s") or 0 for r in mine) / 60:.1f} session-minutes')
    events = os.path.join(RESULTS, 'review-events.jsonl')
    if os.path.isfile(events):
        ids = {r['instance_id'] for r in mine}
        rounds = [json.loads(l) for l in open(events, encoding='utf8') if l.strip()]
        rounds = [e for e in rounds if e.get('kind') == 'round' and 'long' not in str(e.get('log', '')) and any(i in str(e.get('run', '')) for i in ids)]
        print(f'reviewer: {len(rounds)} rounds, {sum(e.get("wall_s") or 0 for e in rounds) / 60:.1f} minutes')


if __name__ == '__main__':
    main()
