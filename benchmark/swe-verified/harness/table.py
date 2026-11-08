#!/usr/bin/env python3
"""table.py RUNS.jsonl GRADING_DIR OUT.md — the result table of the pilot from the run lines and the grader reports.
Resolved comes from GRADING_DIR/logs/run_evaluation/<run id>/<arm>/<instance>/report.json of the official grader,
claimed from the FIXED line recorded in RUNS.jsonl. No number is typed: every cell is a count over those two files.
The sentence for the application is printed last, with its numbers filled from the same counts."""
import glob, json, os, sys


def resolved_of(grading):
    out = {}
    for path in glob.glob(os.path.join(grading, 'logs', 'run_evaluation', '*', '*', '*', 'report.json')):
        arm, instance = path.split(os.sep)[-3], path.split(os.sep)[-2]
        data = json.load(open(path))
        entry = data.get(instance, data)
        out[(instance, arm)] = bool(entry.get('resolved'))
    return out


def main(runs_path, grading, out):
    runs = [json.loads(l) for l in open(runs_path) if l.strip()]
    resolved = resolved_of(grading)
    arms = ['plain', 'hectoline']
    lines = ['# SWE-bench Verified under hectoline — results', '']
    lines.append('Every cell is a count over runs.jsonl and the report.json files of the official grader. «graded» counts the runs the grader reported on.')
    lines.append('')
    lines.append('| arm | runs | graded | resolved | claimed | claimed & resolved | claimed & not | not claimed & resolved | not claimed & not | false claims / claimed |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|')
    summary = {}
    for arm in arms:
        rows = [r for r in runs if r['arm'] == arm]
        graded = [r for r in rows if (r['instance_id'], arm) in resolved]
        cells = {'cr': 0, 'cn': 0, 'nr': 0, 'nn': 0}
        for r in graded:
            c = r.get('claimed') == 'yes'
            v = resolved[(r['instance_id'], arm)]
            cells['cr' if c and v else 'cn' if c else 'nr' if v else 'nn'] += 1
        res = cells['cr'] + cells['nr']
        cla = cells['cr'] + cells['cn']
        false_rate = f'{cells["cn"]} / {cla}' if cla else '0 / 0'
        summary[arm] = dict(runs=len(rows), graded=len(graded), resolved=res, claimed=cla, **cells)
        lines.append(f'| {arm} | {len(rows)} | {len(graded)} | {res} | {cla} | {cells["cr"]} | {cells["cn"]} | {cells["nr"]} | {cells["nn"]} | {false_rate} |')
    lines += ['', '## Per run', '', '| instance | arm | resolved | claimed | patch lines | patch files | turns | wall, s | timed out | units closed | units failed | audits | review rounds pass / fail | hook denies |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in sorted(runs, key=lambda r: (r['instance_id'], r['arm'])):
        v = resolved.get((r['instance_id'], r['arm']))
        v = 'yes' if v else 'no' if v is False else 'not graded'
        hecto = r['arm'] == 'hectoline'
        lines.append(f"| {r['instance_id']} | {r['arm']} | {v} | {r.get('claimed')} | {r.get('patch_lines')} | {r.get('patch_files')} | {r.get('turns')} | {r.get('wall_s')} | {r.get('timed_out')} | "
                     f"{r.get('units_closed', '') if hecto else '—'} | {r.get('units_failed', '') if hecto else '—'} | {r.get('audits_closed', '') if hecto else '—'} | "
                     f"{str(r.get('reviews_pass', '')) + ' / ' + str(r.get('reviews_fail', '')) if hecto else '—'} | {r.get('log_denies', '') if hecto else '—'} |")
    p, h = summary['plain'], summary['hectoline']
    sentence = (f"On {p['graded']} SWE-bench Verified tasks the plain agent claimed {p['claimed']} fixes and the hidden tests confirmed {p['resolved']}. "
                f"Under the unit method it claimed {h['claimed']} and the tests confirmed {h['resolved']}.")
    lines += ['', '## Sentence', '', sentence, '']
    open(out, 'w', encoding='utf8').write('\n'.join(lines))
    print('\n'.join(lines))
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
