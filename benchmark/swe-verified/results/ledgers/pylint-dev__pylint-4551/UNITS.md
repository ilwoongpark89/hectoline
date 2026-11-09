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
sentence   : the pilot step of this room stands in the plan under the leaf it moves
plan       : A0001 · S02
delete?    : no, the plan held one step, the room maker left no pilot step
modify?    : yes, GOAL.md gains the leaf, PLAN.md gains the step, PRODUCTS.md gains two products, UNITS.md gains the planned queue
duplicate  : no, S01 made the room, no step of the plan names the issue of TASK.md
cause      : state layer of inputs → rules → state → result → view, RULE §2: the step with its interface stands before the first unit of the step opens, so the gate refuses every open while the planned queue is empty
split?     : no, one product, the plan of the work on TASK.md
tidy-first?: no
check      : python3 -B unit.py status . | grep -q '^| G1 '
files      : UNITS.md:23-85 · unit.log:1-281, from git diff -U0 at close
base       : U0001 closed, commit c1bf708
lines      : +63 ~0 −0 moved 0, by staged tree at close
added      : the leaf G1 with its measure, the pilot step S02 with its interface, the products P10 P11, the planned blocks of U0003 U0004
rejected   : a step hung on G0, RULE §2 asks the leaf a step moves; a measure of G1 inside measure.py, that file is a link of the method, not a file of this room
split      : none
deleted    : none
result     : failed after 3 failed verifications, the named paths reverted, the third-fail sentence of RULE §4 · check exits  · UNITS.md +63 −0
review     : r1 fail, «the check only proves the file runs, and measures.py prints the typed literal  0 of 1  instead of counting anything, so the change is not what the sentence says.», model claude-opus-5, session a305eed2-31de-473e-bf6a-c6c49dbb6255, ../reviews/agent-review-u0002-r1.md · r2 fail, «the diff carries planning work beyond its sentence (the S02 step, the P11 product row, the planned U0003 block, admitted in  result  as hand-written before the block existed), and the  split?  and  modify?  fields are false against it.», model claude-opus-5, session 2aa0a10c-5fd5-4fb7-8ba8-3ebe685124b5, ../reviews/agent-review-u0002-r2.md · r3 fail, «the check greps only the added G1 goal row and never the plan, while the room's own measure still reports "no pilot step 1" and the diff touches no product of the S02 step it claims.», model claude-opus-5, session 2bf8d22b-8ee4-4822-b0bf-0ab2f6995559, ../reviews/agent-review-u0002-r3.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · structural · failed
sentence   : measures.py counts the hinted attributes that show their hint in the class diagram
plan       : A0001 · S02
delete?    : no, the room holds no measure of a goal leaf yet
modify?    : yes, GOAL.md gains the leaf G1, PLAN.md gains the pilot step S02 of this measure with S03 of the work under it, PRODUCTS.md gains P10 P11, UNITS.md carries this block
duplicate  : no, measure.py measures the method of the room, no leaf of this goal
cause      : result layer of inputs → rules → state → result → view, RULE §1: the leaf of the step needs its measure, so the step that opens under an unmeasured leaf is the step of its measure
split?     : no, one product, the measure of G1
tidy-first?: no
check      : /tmp/pyrevenv/bin/python -B measures.py | grep -qE '^[0-9]+ of 3$'
files      : UNITS.md:45,49,51,54-63,68 · unit.log:282-347, from git diff -U0 at close
base       : U0002 failed, commit ce9b0ae
lines      : +0 ~14 −0 moved 0, by staged tree at close
added      : measures.py with its three cases, the leaf G1 of GOAL.md, the pilot step S02 of this measure with the step S03 of the reader under it, the products P10 of this measure with P11 of the reader it reads
rejected   : a measure that parses the dot file of a pyreverse run, the diagram object answers in process; a measure inside measure.py, that file is a link of the method, not a file of this room; a check that only runs the file, this one asks it for a count over the three cases
split      : none
deleted    : none
result     : failed after 3 failed verifications, the named paths reverted, the third-fail sentence of RULE §4 · check exits  · UNITS.md +14 −14
review     : r1 fail, «the diff makes the measure product P10 under step S02, whose declared product and interface are the annotation reader of pyreverse, and P10's uses field names P05 instead of the P11 files the script actually imports.», model claude-opus-5, session 6ab978e8-2e06-45e5-88e1-345ce3d2813d, ../reviews/agent-review-u0003-r1.md · r2 fail, «lines.py diff .  exits 1 on  measures.py:44 , an added line over the 10-word cap, so RULE §4 forces  unit.py close  to refuse this diff.», model claude-opus-5, session f663ffd6-9216-4cf2-afa9-653a5402a674, ../reviews/agent-review-u0003-r2.md · r3 fail, «the P11 product row this diff adds separates its files with   ·  , which  measure.py  cannot parse, so  unit.py status  reports the three pyreverse files as one not-found path and the §0 line cap stops covering them.», model claude-opus-5, session ea047760-33c2-42e1-a6eb-716fdf00a912, ../reviews/agent-review-u0003-r3.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · behavioral · open
sentence   : pyreverse labels an attribute with the type hint of its argument or of its assignment
plan       : A0001 · S02
delete?    : no, nothing in pyreverse reads an annotation today
modify?    : yes, utils.py gains the reader, inspector.py asks it, diagrams.py prints the name it gives, GOAL.md PLAN.md PRODUCTS.md gain the rows of the step
duplicate  : no, the inference of the assigned value is the only type source today, it prints NoneType
cause      : rules layer of inputs → rules → state → result → view, the annotation of an argument or of an assignment names the type of the attribute, PEP 484
split?     : no, one product, the annotation reader
tidy-first?: no
check      : /tmp/pyrevenv/bin/python -m pytest tests/unittest_pyreverse_inspector.py -k annotation -q
files      : pylint/pyreverse/utils.py · pylint/pyreverse/inspector.py · pylint/pyreverse/diagrams.py · tests/unittest_pyreverse_inspector.py · GOAL.md · PLAN.md · PRODUCTS.md · UNITS.md
base       : U0003 failed, commit 9640a0a
lines      : +80 ~6 −0 moved 0
added      :
rejected   :
split      :
deleted    :
result     :
review     :
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row
