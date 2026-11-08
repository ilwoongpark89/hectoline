#!/usr/bin/env python3
"""room.py NAME G0 QUOTE [HUB] [--top DIR] — one command makes a room under the rooms folder, S74: the folder, the links to this room's rule and tools, the hub link, the six ledgers from the texts given, the bootstrap block, git, the pre-commit link and the first commit."""
import datetime, os, re, subprocess, sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
from gate import ROOMS
KEYS = ['sentence', 'plan', 'delete?', 'modify?', 'duplicate', 'cause', 'split?', 'tidy-first?', 'check', 'files', 'base', 'lines', 'added', 'rejected', 'split', 'deleted', 'result', 'review', 'approval']


def ledgers(name, g0, quote, hub):
    """The six ledgers of a new room, RULE §0: one G0, one A row, one S row, the P rows of the ledgers and links, no R row, the bootstrap block."""
    today, link = datetime.date.today().isoformat(), ' · hub' if hub else ''
    texts = {
        'GOAL.md': f'# GOAL — {name}\n\n## Question\nOwner, {today}: «{quote}».\n\n## Stance\n{g0}. This room follows RULE.md of hectoline by its link.\n\n## Audience\nThe owner. The terminal of this room. The 00 session that watches it.\n\n## Goals\nProgress = leaves at target ÷ leaves, RULE §5. Done steps ÷ all steps is the work count. Each goal leaf has one measure in this room\'s measures.py.\n\n| G | goal | parent | measure | target | baseline |\n|---|---|---|---|---|---|\n| G0 | {g0} | — | leaves at target | 0 of 0 | 0 of 0 |\n\n## Layers and flow\ninputs → rules → state → result → view. Rules: RULE.md of hectoline by its link. State: the six ledgers and the log.\n',
        'OWNER.md': f'# OWNER — {name} · owner statements, A rows\n\nOne row per owner statement about this room, RULE §3. Quotes are verbatim.\n\n| A | date | kind | quote | refined goal | parent | status |\n|---|---|---|---|---|---|---|\n| A0001 | {today[5:]} | order | «{quote}» | {g0} | — | active · S01 · U0001 |\n',
        'PLAN.md': f'# PLAN — {name} · steps\n\nOne S row per step, RULE §2. A step makes or changes one product. The interface stands before the first unit of the step opens. Status: todo, open, done. Done ÷ all is the work count. Rows from S02 on name the leaf they move.\n\n## rule 1.1 from S02\n\n| S | parent | product | step | interface: exposes · hides | units | status |\n|---|---|---|---|---|---|---|\n| S01 | G0 | the six ledgers | this room with its ledgers, links and bootstrap block | the ledger files · the links | U0001 | done |\n',
        'PRODUCTS.md': f'# PRODUCTS — {name} · the P tree\n\nOne P row per product, RULE §0. Hand columns: name, parent, layer, files, uses.\n\n| P | name | parent | layer | files | uses |\n|---|---|---|---|---|---|\n| P01 | ledgers, the state of the room | — | folder | the six ledger files | — |\n| P02 | the unit ledger | P01 | state | UNITS.md | — |\n| P03 | the owner statements of this room | P01 | state | OWNER.md | — |\n| P04 | the plan | P01 | state | PLAN.md | P05 |\n| P05 | the goal page | P01 | inputs | GOAL.md | — |\n| P06 | this product tree | P01 | state | PRODUCTS.md | — |\n| P07 | the research claims | P01 | state | RESEARCH.md | — |\n| P08 | the rule, the hectoline file by link | — | rules | RULE.md | — |\n| P09 | the gate, the measures and the audit, hectoline files by links | — | result | unit.py, measure.py, audit.py | P02 P08 |\n',
        'RESEARCH.md': f'# RESEARCH — {name} · R rows\n\nOne R row per source claim, RULE §7.\n\n| R | date | question | source | quote | pages | support | counter | verdict | user |\n|---|---|---|---|---|---|---|---|---|---|\n',
        '.gitignore': '__pycache__/\n', 'unit' + '.log': ''}
    n = sum(t.count('\n') for t in texts.values()) + 22 + 4 + bool(hub)  # the numstat of the bootstrap commit: these files, the 22-line UNITS.md, one line per link
    block = dict(sentence=f'the room {name} exists with its ledgers, its links, this block', plan='A0001 · S01', **{'delete?': 'no, a new folder', 'modify?': 'no, a new folder', 'split?': 'no, one room', 'tidy-first?': 'no'},
                 duplicate='the folder did not exist, room.py made it', cause='state layer of inputs → rules → state → result → view, RULE §0: a numbered folder with the six ledgers and a link to the rule is a room',
                 check='python3 -I -B unit.py validate . · test -L RULE.md · test -L unit.py', files='GOAL.md · PLAN.md · PRODUCTS.md · RESEARCH.md · UNITS.md · OWNER.md · RULE.md · unit.py · measure.py · audit.py · .gitignore' + link,
                 base='none, the first block of this room', lines=f'+{n} ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py', added='the six ledgers, the links, the bootstrap commit', rejected='a copy of the rule or the gate, links',
                 split='none', deleted='none', result='check exits 0 0 0 · the bootstrap commit', review='written closed by room.py, the review of the room maker unit covers it', approval=f'owner {today[5:]} «{quote}», the A0001 row')
    texts['UNITS.md'] = f'# UNITS — {name}\n\n## U0001 · {today} · structural · closed\n' + '\n'.join(f'{k:<11}: {block[k]}' for k in KEYS) + '\n'
    return texts


def main(argv):
    top = argv[argv.index('--top') + 1] if '--top' in argv else ROOMS
    args = [a for i, a in enumerate(argv) if a != '--top' and (i == 0 or argv[i - 1] != '--top')]
    if len(args) < 3 or not re.fullmatch(r'\d\d(_\d\d)*_[A-Za-z][\w-]*', args[0]):
        print('room.py NAME G0 QUOTE [HUB] [--top DIR], NAME = a two-digit prefix, an underscore and a word', file=sys.stderr); return 2
    name, g0, quote, hub = args[0], args[1], args[2], args[3] if len(args) > 3 else ''
    room = os.path.join(top, name)
    if os.path.exists(room):
        print(f'{room} exists, a room is made once', file=sys.stderr); return 1
    os.makedirs(room)
    for f in ('RULE.md', 'unit.py', 'measure.py', 'audit.py'):
        os.symlink(os.path.join(HERE, f), os.path.join(room, f))  # the rule and the tools stay in the rule room, RULE §0
    if hub:
        os.symlink(os.path.abspath(hub), os.path.join(room, 'hub'))
    for f, text in ledgers(name, g0, quote, hub).items():
        open(os.path.join(room, f), 'w', encoding='utf8').write(text)
    git = lambda *a: subprocess.run(['git', '-C', room, *a], capture_output=True, text=True)
    git('init', '-q'); os.symlink(os.path.join(HERE, 'hooks', 'pre-commit'), os.path.join(room, '.git', 'hooks', 'pre-commit'))  # the git gate, RULE §4, before the first commit, S115
    git('add', '-A'); r = git('-c', 'user.name=hectoline', '-c', 'user.email=hectoline', 'commit', '-q', '-m', f'U0001 the room {name} exists with its ledgers, its links, this block')
    if r.returncode:  # the gate refused the first commit, no half room stays under the top folder, the room table would list it
        __import__('shutil').rmtree(room, ignore_errors=True); print(r.stderr.strip() or r.stdout.strip(), file=sys.stderr); os.path.exists(room) and print(f'{room} stays, remove it by hand', file=sys.stderr); return 1  # a partial removal is said, S121
    print(f'{room} · {git("rev-parse", "--short", "HEAD").stdout.strip()} · ' + subprocess.run([sys.executable, '-I', '-B', os.path.join(room, 'unit.py'), 'validate', room], capture_output=True, text=True).stdout.strip().splitlines()[-1])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
