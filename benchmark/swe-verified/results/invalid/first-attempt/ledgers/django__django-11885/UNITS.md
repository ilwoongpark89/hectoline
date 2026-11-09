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

## U0002 · 2026-11-09 · structural · open
sentence   : the plan of the TASK fix stands as one pilot step with its product
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, the step row of the fix does not exist yet
modify?    : no, S01 is the closed bootstrap step of the ledgers
duplicate  : grep -c "^| S0" PLAN.md gives 1 at HEAD, S01 alone · grep -c "pilot" PLAN.md gives 0 at HEAD
cause      : rules layer of inputs → rules → state → result → view, the step row rules which product a unit may touch
split?     : no, one step with one product
tidy-first?: no, PLAN.md holds the row shape already
check      : python3 -I -B -c "r=[l.split('|') for l in open('PLAN.md').read().splitlines() if l.startswith('| S')];n=[x for x in r if x[1].strip()=='S02'];assert len(n)==1;x=n[0];assert x[2].strip()=='G0';assert ('| '+x[3].strip()+' |') in open('PRODUCTS.md').read();assert 'pilot' in x[4];assert 'U0003' in x[6]"
files      : PLAN.md:≤3 · PRODUCTS.md:≤2 · UNITS.md:≤50
base       : U0001 closed, commit 222bfaa
lines      : ≤60
added      : the pilot step S02 of G0, the product row P10, the two planned blocks of the step
rejected   : a leaf goal G1 with its own measures.py, the room measures no leaf today and a new leaf would open its measure step first · a product row for django/contrib/admin/utils.py, that file holds 543 lines over the 500 cap, so U0003 touches its override as a caller line · a product row for tests/delete/tests.py, that file holds 584 lines over the 500 cap
split      : none
deleted    : none
result     : 
review     : r1 pass, «every check clause fails at base 222bfaa and passes now, and each field, quote and cross-file claim of the block is true as verified in the room.», model claude-opus-5, session a06cffaa-758f-4ec2-9547-2c79e6ffb3fd, ../reviews/agent-review-u0002-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · structural · planned
sentence   : the collector reads the related objects of one model through a list of fields
plan       : A0001 · S02
files      : django/db/models/deletion.py:≤40 · django/contrib/admin/utils.py:≤4 · UNITS.md:≤25
base       : U0002, the planning unit of this step
lines      : ≤70

## U0004 · 2026-11-09 · behavioral · planned
sentence   : the collector combines the fast delete of one related model into one query
plan       : A0001 · S02
files      : django/db/models/deletion.py:≤35 · UNITS.md:≤25
base       : U0003, the structural unit of this step
lines      : ≤60
