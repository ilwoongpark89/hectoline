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
sentence   : the plan names the leaf G1 with the measure step that opens it
plan       : A0001 · S none, a planning unit carries no step
delete?    : no, nothing to remove, the plan holds no step under a leaf yet
modify?    : no, S01 is done, these steps hang under a new leaf
duplicate  : git grep -c '^| G1 |' HEAD -- GOAL.md · 0 hits at HEAD, exit 1
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order opens with one planning unit that writes the goals it changes with the steps under them, the leaf row it adds to GOAL.md sits in the inputs layer
split?     : no, one leaf with its two steps
tidy-first?: no, the ledger tables hold the rows this unit writes
check      : grep -qE '^\| G1 \| the two MRT unit strings' GOAL.md · grep -qE '^\| S02 \| G1 \| P11' PLAN.md · grep -qE '^\| S03 \| G1 \| P10' PLAN.md · grep -qE '^\| P11 \|' PRODUCTS.md · grep -qE '^#+ U0003 .* behavioral' UNITS.md
files      : GOAL.md:17-22 · PLAN.md:10-11 · PRODUCTS.md:16-17 · UNITS.md:23-64 · unit.log:1-384, from git diff -U0 at close
base       : U0001 closed, commit ddd56a5
lines      : +51 ~1 −0 moved 0, by staged tree at close
added      : the leaf row G1 in GOAL.md with its two unit strings, the measure step S02 with the pilot step S03 in PLAN.md, the rows P10 P11 in PRODUCTS.md, the planned block U0003
rejected   : a planned block under S03, G1 is unmeasured, only its measure step opens under it, RULE §1, close refused it · a leaf row without a measure tool, the leaf would stay unmeasured · a second step for the MRT reader of astropy/io/ascii/cds.py, it already hands its unit string to P10 · a step for the CDS writer, TASK.md names reading only
split      : none
deleted    : none
result     : check exits 0 0 0 0 0 · GOAL.md +6 −1 · PLAN.md +2 −0 · PRODUCTS.md +2 −0 · UNITS.md +42 −0
review     : r1 fail, «the added S02 row and the rejected key claim a G0 movement "from 0 of 1 checks met to 1 of 1" that GOAL.md and the room's own  unit.py status  ( 0 of 0 , zero leaves) contradict, so the pilot step names no real leaf move.», model claude-opus-5, session 410555f8-65c1-4d2d-bb9c-322353bb4b6a, ../reviews/agent-review-u0002-r1.md · r2 pass, «the r1 finding is fixed, every check clause exits 1 at base and 0 now, and the pilot step names a verified red-to-green goal check consistent with GOAL.md and the room's own status.», model claude-opus-5, session b485dd10-a02b-4f47-af8e-9c571ff7a643, ../reviews/agent-review-u0002-r2.md · r3 pass, «every check clause exits 1 at the base and 0 now, each field and cross-file claim in the block checks out, and the pilot step names a verified red-to-green goal movement consistent with GOAL.md.», model claude-opus-5, session f7721215-3173-4e65-a815-645de0d3f24c, ../reviews/agent-review-u0002-r3.md · r4 pass, «every check clause exits 1 at the base and 0 now, each field and cross-file claim verifies against the files, and the pilot step names a goal movement I confirmed red at the base while the diff stays inside the ledgers of its step.», model claude-opus-5, session 3b4dd439-2a3c-4cf4-873b-a0dab1e3e078, ../reviews/agent-review-u0002-r4.md · r5 pass, «every check clause exits 1 at the base and 0 now, each field and cross-file claim verifies against the files, the r1 finding is fixed, and the diff stays inside the ledgers a planning unit owns while S03 names a leaf move I confirmed red at the base.», model claude-opus-5, session e51165d0-c745-4d26-874b-d3405a3263f2, ../reviews/agent-review-u0002-r5.md · r6 pass, «every check clause exits 1 at the base and 0 now, each field and cross-file claim verifies against the files, and S03 names a leaf move I confirmed red at the base while the diff stays inside the ledgers a planning unit owns.», model claude-opus-5, session e81eee95-3811-43e8-bf2c-dfc133a3d532, ../reviews/agent-review-u0002-r6.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · open
sentence   : measures.py gives the room the number of its leaf G1
plan       : A0001 · S02
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : measures.py:≤45
base       : U0002 closed, commit b2c2bdf
lines      : ≤45
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 
