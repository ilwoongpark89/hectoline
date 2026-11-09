# UNITS — 01_task

## U0001 · 2026-11-09 · structural · closed
sentence   : the room exists with its ledgers, its links, this block
plan       : A0001 · S01
delete?    : no, a new folder
modify?    : no, a new folder
duplicate  : the folder did not exist, room.py made it
cause      : state layer of inputs → rules → state → result → view, RULE §0: a numbered folder with the six ledgers and a link to the rule is a room
split?     : no, one room
tidy-first?: no
check      : python3 -I -B unit.py validate . · test -L RULE.md · test -e unit.py
files      : TASK.md · GOAL.md · PLAN.md · PRODUCTS.md · RESEARCH.md · UNITS.md · OWNER.md · RULE.md · unit.py · measure.py · audit.py
base       : none, the first block of this room
lines      : +84 ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py
added      : the six ledgers, the links, the bootstrap commit
rejected   : a copy of the rule or the gate, links
split      : none
deleted    : none
result     : check exits 0 0 0 · the bootstrap commit
review     : written closed by room.py, the review of the room maker unit covers it
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0002 · 2026-11-09 · structural · failed
sentence   : the plan cuts the owner order into three steps with their first blocks
plan       : A0001 · S none, a planning unit carries no step
delete?    : no, the plan holds no step for A0001 yet, deletion leaves the order unplanned
modify?    : no, S01 is closed and names the ledgers, not the fix
duplicate  : grep -c "^| S0" PLAN.md gave 1 at ef6e44c, only S01
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order starts with one planning unit
split?     : no, one plan write, the steps it names are the split
tidy-first?: no
check      : python3 -I -B -c "import re;P=open('PLAN.md').read();U=open('UNITS.md').read();want={'S02':'U0003','S03':'U0004','S04':'U0005'};rows=dict(re.findall(r'(?m)^\| (S0[234]) \| G0 \|[^\n]*\| (U000[345]) \|',P));assert rows==want,rows;blocks={b.split()[0]:b for b in U.split('\n## ')[1:]};assert all(re.search(r'\nsentence   : [^\n]{10,}\nplan       : A0001 [^\n]*'+s+r'\n',blocks[u]) for s,u in want.items()),'sentence or plan';assert all(re.search(r'\nfiles      : [^\n]{10,}\nbase       : [^\n]{2,}\nlines      : [^\n]{2,}\n',blocks[u]) for u in want.values()),'files base lines'"
files      : UNITS.md:23-106 · unit.log:1-148, from git diff -U0 at close
base       : U0001 closed, commit ef6e44c
lines      : +84 ~0 −0 moved 0, by staged tree at close
added      : S02, S03, S04 under G0, the planned blocks U0003, U0004, U0005
rejected   : P rows for sphinx/domains/python.py and sphinx/ext/autodoc/__init__.py, both adopted files stand far over the 500-line leaf cap of RULE §0 and a splitting step is outside this order · a doc step for doc/usage/restructuredtext/domains.rst, the order names the autodoc defect · a research unit, the issue text carries the python version facts
split      : none
deleted    : none
result     : failed after 3 failed verifications, the named paths reverted, the third-fail sentence of RULE §4 · check exits  · UNITS.md +84 −0
review     : r1 fail, «the one check clause only counts three row prefixes in PLAN.md, proving that text exists rather than the sentence's outcome, and never tests the planned first blocks that are 84 of the unit's 87 added lines.», model claude-opus-5, session 8c7a7ef9-223f-4fed-a85e-9f8b815a0608, ../reviews/agent-review-u0002-r1.md · r2 fail, «the check clause pins the transient  planned  and  todo  statuses, which RULE §2 forbids for a planning clause, and it exits 1 once U0003 opens, so the field cannot work.», model claude-opus-5, session 050b05c0-4855-48c0-b23e-1578f8dd718d, ../reviews/agent-review-u0002-r2.md · r3 fail, «the room's first planning unit added no pilot row ( unit.py status  reports  no pilot step 1 ) and no measurable G0 leaf ( 0 / 0 leaves ), so RULE §3 lets none of its three planned blocks open and §2 lets none of S02–S04 ever reach done.», model claude-opus-5, session 0e4e8af8-7dc2-43df-9672-7d48d0805660, ../reviews/agent-review-u0002-r3.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · planned
sentence   : the py:property directive takes a classmethod flag
plan       : A0001 · S02
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : sphinx/domains/python.py:≤10
base       : U0002
lines      : ≤12
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 

## U0004 · 2026-11-09 · behavioral · planned
sentence   : the property documenter documents a classmethod property member
plan       : A0001 · S03
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : sphinx/ext/autodoc/__init__.py:≤45
base       : U0003
lines      : ≤45
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 

## U0005 · 2026-11-09 · structural · planned
sentence   : the regression tests cover the class property
plan       : A0001 · S04
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : tests/test_ext_autodoc_autoproperty.py:≤20 · tests/test_domain_py.py:≤25 · tests/roots/test-ext-autodoc/target/properties.py:≤8
base       : U0004
lines      : ≤50
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 

## U0006 · 2026-11-09 · structural · open
sentence   : the queue repair writes the three steps the waiting blocks cite
plan       : A0001 · S none, queue repair after U0002 failed
delete?    : no, the rollback of U0002 took back every step row its three blocks cite, deletion leaves the queue unopenable
modify?    : no, S01 is closed and names the ledgers, not the fix
duplicate  : grep -c "^| S0" PLAN.md gave 1 at fc9b75a, only S01
cause      : state layer of inputs → rules → state → result → view, RULE §4: the queue repair gate admits one planning block over a queue whose base-ready block fails step eligibility
split?     : no, one plan write, the three rows it adds are the split
tidy-first?: no
check      : python3 -B -c "import re;P=open('PLAN.md').read();U=open('UNITS.md').read();rows={m[0]:m[1:] for m in re.findall(r'(?m)^\| (S0\d) \| G0 \|[^|]*\|([^|]*)\|[^|]*\| (U000\d) \| (\w+) \|',P)};want={'S02':'U0003','S03':'U0004','S04':'U0005'};assert all(s in rows and rows[s][1]==u for s,u in want.items()),rows;assert all(re.search(r'moves G1 from \d of 3 to \d of 3',rows[s][0]) for s in want),rows;assert all(rows[s][2] in ('todo','open','done') for s in want),rows;blocks={b.split()[0]:b for b in U.split('\n## ')[1:]};assert all(re.search(r'\nplan       : A0001 [^\n]*'+s+r'\n',blocks[u]) for s,u in want.items()),'plan keys'"
files      : OWNER.md:7 · PLAN.md:10-12 · UNITS.md:107-128
base       : U0002 failed, commit fc9b75a
lines      : +25 ~1 −0 moved 0, by git diff --numstat of OWNER.md, PLAN.md and UNITS.md, the one changed owner row counted as modified
added      : S02, S03, S04 under G0, one row for each waiting block of the failed U0002
rejected   : parent G1 and a row for the goal page, RULE §4 keeps a queue repair to OWNER.md, PLAN.md and its own block, so the G1 row and the steps under it enter with the planning unit that RULE §3 opens over the empty queue · planned blocks, the same restriction lets a repair add none · re-pointing U0003, U0004, U0005, the same restriction, each row carries the product its block already names
split      : none
deleted    : none
result     : the check clause exits 0, it reads the three rows against the three blocks that cite them
review     : r1 fail, «the plan key cites a nonexistent A0013, the sole check clause  test -f stray.md  only proves a pile file exists, and the diff re-points no planned block at all, so the unit's sentence, check and parent row are each false.», model claude-opus-5, session 517bd683-ee54-4b50-9437-cd9d6c377e87, ../reviews/agent-review-u0006-r1.md · r2 pass, «every clause runs, fails at the base and passes now while proving the planned row and its serving block together, and each field matches the files I read.», model claude-opus-5, session 0827ca45-13e4-432f-961e-99ad612dc9b5, ../reviews/agent-review-u0006-r2.md · r3 pass, «every clause runs, fails at the base and passes now while proving the five rows against the blocks they serve, the repair stays inside OWNER.md, PLAN.md and its own block, and each field matches the files I read.», model claude-opus-5, session efc8a1f1-cc2e-41f8-a9d8-7e854345964d, ../reviews/agent-review-u0006-r3.md · r4 fail, «the review key passes a diff that does not exist, S05's units cell names a U0007 block absent from UNITS.md, and the sole clause only reads back the row the unit wrote while S02–S04 remain cited by planned blocks and absent from PLAN.md.», model claude-opus-5, session a1769f02-cb49-4ed0-ba87-1701e80a9325, ../reviews/agent-review-u0006-r4.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

