#!/usr/bin/env python3
"""select.py PARQUET OUT.json [N] — the fixed task selection of the SWE-bench Verified pilot.
Rule: rows with difficulty «1-4 hours» whose gold patch touches at least two files, sorted by the length
of the gold patch, largest first, the first N (default 10) with at most 3 per repo. Prints the count at each step.
The output holds instance_id, repo, base_commit, difficulty, patch_files, patch_len, problem_statement and hints_text only.
The gold patch, test_patch, FAIL_TO_PASS and PASS_TO_PASS never leave the parquet."""
import json, re, sys
import pyarrow.parquet as pq


def select(parquet, n=10, per_repo=3, difficulty='1-4 hours', min_files=2):
    table = pq.read_table(parquet).to_pylist()
    steps = [('rows in the split', len(table))]
    rows = [r for r in table if r['difficulty'] == difficulty]
    steps.append((f'difficulty {difficulty}', len(rows)))
    for r in rows:
        r['patch_files'] = len(re.findall(r'^diff --git ', r['patch'], re.M))
        r['patch_len'] = len(r['patch'])
    rows = [r for r in rows if r['patch_files'] >= min_files]
    steps.append((f'gold patch touches at least {min_files} files', len(rows)))
    rows.sort(key=lambda r: (-r['patch_len'], r['instance_id']))
    chosen, count = [], {}
    for r in rows:
        if count.get(r['repo'], 0) >= per_repo:
            continue
        count[r['repo']] = count.get(r['repo'], 0) + 1
        chosen.append(r)
        if len(chosen) == n:
            break
    steps.append((f'first {n} with at most {per_repo} per repo', len(chosen)))
    keep = ('instance_id', 'repo', 'base_commit', 'difficulty', 'patch_files', 'patch_len', 'problem_statement', 'hints_text')
    return steps, [{k: r[k] for k in keep} for r in chosen]


if __name__ == '__main__':
    parquet, out = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    steps, tasks = select(parquet, n)
    json.dump({'rule': __doc__.split('\n')[1].strip() + ' ' + __doc__.split('\n')[2].strip(), 'steps': steps, 'tasks': tasks}, open(out, 'w'), indent=1)
    for name, count in steps:
        print(f'{count:5d}  {name}')
    for t in tasks:
        print(f"{t['instance_id']:45s} {t['repo']:28s} files {t['patch_files']:2d} patch {t['patch_len']:6d} {t['base_commit'][:10]}")
