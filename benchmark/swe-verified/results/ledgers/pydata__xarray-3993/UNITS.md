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
sentence   : the plan holds the G1 leaf of the coord rename with its measure step
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the leaf, the step, the product do not exist yet
modify?    : no, S01 is done, its product is the ledgers
duplicate  : grep -c integrate GOAL.md PLAN.md PRODUCTS.md → 0 0 0 at 9c43bf5 · grep -c measures.py GOAL.md PRODUCTS.md → 1 0 at 9c43bf5
cause      : state layer of inputs → rules → state → result → view, RULE §3: the rows of an owner statement enter before its work units
split?     : no, one plan
tidy-first?: no, the ledger shape stands
check      : grep -q '^| S02 | G1 | P10 |' PLAN.md · grep -q '^| G1 |' GOAL.md · grep -q '^| P10 |' PRODUCTS.md · grep -q 'S02' OWNER.md
files      : UNITS.md:23-64 · unit.log:1-130, from git diff -U0 at close
base       : U0001 closed, commit 9c43bf5
lines      : +42 ~0 −0 moved 0, by staged tree at close
added      : the G1 leaf with its measure, the S02 measure step, the P10 measure product, the U0003 planned block
rejected   : the pilot step with its own blocks, no step moves an unmeasured leaf, RULE §1 · a whats-new entry, the doc product carries no step yet · a rename with no deprecation, it breaks every dim caller at once · a change to Dataset.integrate, its keyword already reads coord
split      : none
deleted    : none
result     : failed after 3 failed verifications, the named paths reverted, the third-fail sentence of RULE §4 · check exits  · UNITS.md +42 −0
review     : r1 fail, «the  lines  key reports  +63 ~1  as "by numstat of this diff" while numstat gives +67 ~1, omitting the four PLAN.md and PRODUCTS.md rows the block's own  added  key names.», model claude-opus-5, session bf2c8c52-4383-437b-9639-0035bbceb730, ../reviews/agent-review-u0002-r1.md · r2 pass, «every check clause fails at 9c43bf5 and passes now, the r1 lines finding is corrected to the numstat value +67 ~1, and all remaining keys verify true against the ledgers and the tree.», model claude-opus-5, session e8b767d9-836e-44ac-ae91-d972ad363f7c, ../reviews/agent-review-u0002-r2.md · r3 fail, «the check clause  test -f stray.md  proves nothing the sentence claims and only passes by leaving an unowned pile, while  result  reports four exit codes for one clause and  plan  cites a nonexistent A0013.», model claude-opus-5, session 5a65e54d-83ab-4112-b2d7-5a0947620067, ../reviews/agent-review-u0002-r3.md · r4 fail, «. So the highest numbered round is r3 fail, not r2 pass, and the key omits it — the block presents a pass as its terminal verdict while the record it points at holds a later failure.», model claude-opus-5, session b11e6c6d-09b9-490a-903b-91d1b4cac21e, ../reviews/agent-review-u0002-r4.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · redesign · closed
sentence   : the plan holds the G1 leaf of the coord rename with its measure step
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the leaf, the step, the product do not exist yet
modify?    : no, S01 is done, its product is the ledgers
duplicate  : grep -c integrate GOAL.md PLAN.md PRODUCTS.md → 0 0 0 at 9746cb4 · grep -c measures.py GOAL.md PRODUCTS.md → 1 0 at 9746cb4
cause      : state layer of inputs → rules → state → result → view, RULE §4: the redesign of a failed planning unit takes a planned block of that unit as its own block
split?     : no, one plan, the first verdict of a redesign
tidy-first?: no, the ledger shape stands
check      : grep -q '^| S02 | G1 | P10 |' PLAN.md · grep -q '^| G1 |' GOAL.md · grep -q '^| P10 |' PRODUCTS.md · grep -q 'S02' OWNER.md
files      : GOAL.md:17-18 · OWNER.md:7 · PLAN.md:10 · PRODUCTS.md:16 · UNITS.md:45-66,77 · unit.log:131-165, from git diff -U0 at close
base       : U0002 failed, commit 9746cb4
lines      : +24 ~4 −0 moved 0, by staged tree at close
added      : the G1 leaf with its measure, the S02 measure step, the P10 measure product, the U0004 planned block
rejected   : the pilot step with its own blocks, no step moves an unmeasured leaf, RULE §1 · a whats-new entry, the doc product carries no step yet · a rename with no deprecation, it breaks every dim caller at once · a change to Dataset.integrate, its keyword already reads coord
split      : none
deleted    : the U0002 block, failed after three failed verifications, RULE §4 · the five keys of the planned block it left under U0003, re-pointed to this redesign before open, since the gate opens no block whose plan key names a reverted step
result     : check exits 0 0 0 0 · GOAL.md +2 −1 · OWNER.md +1 −1 · PLAN.md +1 −0 · PRODUCTS.md +1 −0 · UNITS.md +23 −2
review     : r1 pass, «every check clause fails at 9746cb4 and passes now, and the nine verdict keys verify true against the ledgers and the tree, including the lines count that failed U0002.», model claude-opus-5, session f476496a-f716-4839-bafa-4ae558b4eabe, ../reviews/agent-review-u0003-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · behavioral · closed
sentence   : measures.py computes the G1 number of this room
plan       : A0001 · S02
delete?    : no, no file of this room computes a leaf number
modify?    : no, measure.py of the gate reads this file by its name, RULE §5
duplicate  : git cat-file -e HEAD:measures.py → absent at 61ff0b6 · grep -c 'def g1' measure.py audit.py → 0 0 at 61ff0b6
cause      : result layer of inputs → rules → state → result → view, RULE §5: one computed number per goal leaf
split?     : no, one function
tidy-first?: no, the adapter contract of measure.py stands
check      : grep -q 'def g1(room, blocks)' measures.py · python3 -I -B unit.py status . | grep -q '| G1 | integrate signatures that read coord | 2 of 2 | 1 of 2 |'
files      : UNITS.md:66,69-85 · measures.py:1-19 · unit.log:166-192, from git diff -U0 at close
base       : U0003 closed, commit 61ff0b6
lines      : +19 ~18 −0 moved 0, by staged tree at close
added      : the g1 function of the G1 leaf, the SOURCES tuple of the two source files it reads
rejected   : an import of xarray in the worker, the parse of the two files needs none · a count of the dim keyword, the goal names the coord argument · a measure in audit.py, measure.py reads measures.py by name
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −18 · measures.py +19 −0
review     : r1 fail, «the result key reports  check exits 1 1 at 61ff0b6  while clause 1 exits 2 there, a false field in a verdict key.», model claude-opus-5, session f7fce887-c7f3-4188-884e-e316a5684b18, ../reviews/agent-review-u0004-r1.md · r2 pass, «the r1 false field is corrected and verified, both clauses exit non-zero at 61ff0b6 and zero now with the status row computing G1 as  1 of 2 , and every verdict key reads true against the tree and the ledgers.», model claude-opus-5, session a00da2a3-2718-4ce6-9e20-f9f6df933ab7, ../reviews/agent-review-u0004-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-09 · structural · closed
sentence   : the plan holds the pilot step of the coord rename with its two blocks
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the pilot step, its product, its blocks do not exist yet
modify?    : no, S02 is the measure step, its product is measures.py
duplicate  : grep -c integrate PLAN.md PRODUCTS.md → 0 0 at 59a2498 · grep -c dataarray.py PRODUCTS.md → 0 at 59a2498
cause      : state layer of inputs → rules → state → result → view, RULE §3: the step of a statement stands before the units under it
split?     : no, one plan
tidy-first?: no, the ledger shape stands
check      : grep -q '^| S03 | G1 | P11 |' PLAN.md · grep -q '^| P11 |' PRODUCTS.md · grep -q '^| S02 .*| done |' PLAN.md · grep -q 'S03' OWNER.md
files      : OWNER.md:7 · PLAN.md:10-11 · PRODUCTS.md:17 · UNITS.md:86-148 · unit.log:193-204, from git diff -U0 at close
base       : U0004 closed, commit 59a2498
lines      : +65 ~2 −0 moved 0, by staged tree at close
added      : the S03 pilot step with its interface, the P11 integrate product, the U0006 planned block, the U0007 planned block
rejected   : a step of its own for the regression cases, one step makes one product, RULE §0 · one block for the rename with its cases, a test file enters no unit that touches code outside tests, RULE §4 · a whats-new entry, the doc product carries no step yet
split      : none
deleted    : none
result     : check exits 0 0 0 0 · OWNER.md +1 −1 · PLAN.md +2 −1 · PRODUCTS.md +1 −0 · UNITS.md +63 −0
review     : r1 pass, «every check clause fails at base 59a2498 and passes now, and each verdict key, line count and file range reads true against the ledger diff.», model claude-opus-5, session 06377364-abc4-43c9-9865-db5ff51cf4ef, ../reviews/agent-review-u0005-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0006 · 2026-11-09 · behavioral · closed
sentence   : DataArray.integrate takes coord in place of dim
plan       : A0001 · S03
delete?    : no, the dim keyword stays one deprecation cycle
modify?    : no, no block of this room owns the integrate signature yet
duplicate  : git grep -c "dim is not None and coord is not None" db526f5 -- xarray → 0 files at db526f5 · git grep -c "def integrate" db526f5 -- xarray/core/dataarray.py xarray/core/dataset.py → 1 1 at db526f5
cause      : inputs layer of inputs → rules → state → result → view, RULE §0: the keyword a caller passes enters at the signature
split?     : no, one signature with its guard
tidy-first?: no, the signature keeps its place
check      : grep -q 'coord: Union\[Hashable, Sequence\[Hashable\]\] = None' xarray/core/dataarray.py · python3 -I -B unit.py status . | grep -q '| G1 | integrate signatures that read coord | 2 of 2 | 2 of 2 |' · ! /tmp/xrvenv/bin/python -W error::FutureWarning -c "import numpy as np, xarray as xr; xr.DataArray(np.arange(4), dims=['x'], coords={'x': [0, 0.1, 1.1, 1.2]}).integrate(dim='x')" · /tmp/xrvenv/bin/python -W error::FutureWarning -c "import numpy as np, xarray as xr; xr.DataArray(np.arange(4), dims=['x'], coords={'x': [0, 0.1, 1.1, 1.2]}).integrate(coord='x')"
files      : UNITS.md:108,111-127 · unit.log:205-252 · xarray/core/dataarray.py:3484-3488,3493,3498,3500-3501,3537-3552, from git diff -U0 at close
base       : U0005 closed, commit db526f5
lines      : +21 ~22 −0 moved 0, by staged tree at close
added      : the coord argument of DataArray.integrate, the keyword-only dim argument behind it, the FutureWarning that dim raises, the guard that refuses both keywords
rejected   : a rename with no deprecation, it breaks every dim caller at once · a positional dim kept beside coord, one argument carries one positional name · a rename of the Dataset keyword, it already reads coord · a whats-new entry, the doc product carries no step yet
split      : none
deleted    : none
result     : check exits 0 0 0 0 · UNITS.md +18 −18 · xarray/core/dataarray.py +25 −4
review     : r1 pass, «every check clause exits non-zero at db526f5 and zero now, and each verdict key, line count and file range reads true against the diff while the change stays inside S03's interface.», model claude-opus-5, session 845616d8-fa95-401b-9163-73b4d7c11a07, ../reviews/agent-review-u0006-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0007 · 2026-11-09 · behavioral · open
sentence   : the test suite states the coord keyword of DataArray.integrate
plan       : A0001 · S03
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : xarray/tests/test_dataset.py:≤12 · xarray/tests/test_units.py:≤2
base       : U0006 closed, commit 9a63705
lines      : ≤14
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 
