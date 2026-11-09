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

## U0002 · 2026-11-09 · structural · closed
sentence   : the plan gains the pilot step for the direct ITRS to Observed transform
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, no S row covers the ITRS to Observed path, nothing to remove
modify?    : no, S01 is done, its product is the six ledgers, not the transform
duplicate  : grep -rlE 'ITRS, (AltAz|HADec)' astropy/coordinates | wc -l = 1 at HEAD, the one hit is a test file, no transform exists · grep -cE '^\| S0' PLAN.md = 1 at HEAD
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order enters as plan rows before any work unit opens
split?     : no, one plan for one owner order
tidy-first?: no, these rows carry no code
check      : grep -qE '^\| G1 \|.* \| G0 \| .*measures\.py g1 \| 4 of 4 \| 0 of 4 \|' GOAL.md · grep -qE '^\| S03 \| G1 \| P10 \|.*pilot' PLAN.md · python3 -c "cells={r[0]:r for r in ([c.strip() for c in l.strip('|\n ').split('|')] for l in open('PLAN.md') if l.startswith('| S'))}; g=open('GOAL.md').read(); p=open('PRODUCTS.md').read(); rows=[cells['S02'],cells['S03'],cells['S04']]; assert all(('| '+r[1]+' |') in g for r in rows); assert all(('| '+r[2]+' |') in p for r in rows); assert all(chr(183) in r[4] for r in rows); assert all('G1' in r[3] for r in rows); assert all(chr(8594) in r[3] for r in rows)"
files      : GOAL.md:17-26 · OWNER.md:7 · PLAN.md:10-12 · PRODUCTS.md:16-17 · UNITS.md:23-64 · unit.log:1-436, from git diff -U0 at close
base       : U0001 closed, commit 6d44ad4
lines      : +56 ~2 −0 moved 0, by staged tree at close
added      : G1 the goal leaf with its four acceptance checks, the G0 target 1 of 1, S02 the measure step, S03 the pilot, S04 refraction, P10 the transform product, P11 the measure product, the planned block U0003, the A0001 row now names the steps
rejected   : a leaf without a measure, RULE §1 leaves it unmeasured, so G1 carries accept.py and measures.py from its own step · planned blocks for U0004 U0005, their steps sit under a leaf that no tool measures yet, so the gate refuses them, RULE §3 asks for at most three · a step for the astropy documentation, the owner order names the issue of TASK.md, not the docs · a test file under astropy/coordinates/tests, RULE §4 denies a test file beside code in one unit, accept.py stands in the room instead
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +10 −1 · OWNER.md +1 −1 · PLAN.md +3 −0 · PRODUCTS.md +2 −0 · UNITS.md +42 −0
review     : r1 pass, «every check clause fails at base 6d44ad4 and passes now, each field I could test is true, and the plan rows add the pilot step the sentence claims without touching any code.», model claude-opus-5, session 9b739eaf-ea3f-427a-900c-d0cca8115b90, ../reviews/agent-review-u0002-r1.md · r2 pass, «every check clause exits non-zero at base 6d44ad4 and 0 now, every field I could run is true, and the diff adds only the plan, product and owner rows the sentence claims without touching any code.», model claude-opus-5, session 77dac644-d6ba-4e2e-9f81-b3ee759c1698, ../reviews/agent-review-u0002-r2.md · r3 pass, «every check clause exits non-zero at base 6d44ad4 and 0 in the working tree, each field I could run is true, and the diff adds only the goal, plan, product and owner rows the sentence claims, touching no code.», model claude-opus-5, session b08bcf20-8faa-4970-81f3-de6834988126, ../reviews/agent-review-u0002-r3.md · r4 pass, «every check clause exits non-zero at base 6d44ad4 and 0 in the working tree, each field I could run is true, and the diff adds only the goal, plan, product and owner rows the sentence claims, touching no code.», model claude-opus-5, session 98e56166-63b6-4621-871b-b6f957d81a17, ../reviews/agent-review-u0002-r4.md · r5 pass, «every check clause exits non-zero at base 6d44ad4 and 0 in the working tree, each field I could run is true, and the diff adds only the goal, plan, product and owner rows the sentence claims, touching no code.», model claude-opus-5, session 30a278d4-35be-4803-8d35-6f8bd9b5d68d, ../reviews/agent-review-u0002-r5.md · r6 pass, «every check clause exits non-zero at base 6d44ad4 and 0 in the working tree, each field I could run is true, and the diff adds only the goal, plan, product and owner rows the sentence claims, touching no code.», model claude-opus-5, session eb5e8b0f-3778-4c00-9dad-e0e7224641c3, ../reviews/agent-review-u0002-r6.md · r7 pass, «every check clause exits non-zero at base 6d44ad4 and 0 in the working tree, each field I could run is true, and the diff adds only the goal, plan, product and owner rows the sentence claims, touching no code.», model claude-opus-5, session 7043d488-f4eb-4d06-bca9-ef32f3ffca7d, ../reviews/agent-review-u0002-r7.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · open
sentence   : measures.py computes the four acceptance checks of leaf G1 for unit.py status
plan       : A0001 · S02
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : measures.py:≤40 · accept.py:≤90 · GOAL.md:≤2
base       : U0002 closed, commit ba6636c
lines      : ≤100
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 
