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
sentence   : the plan holds the goal leaf with the steps that make autodoc show inherited instance attributes
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, GOAL.md carries no leaf under G0 for the order of A0001 yet
modify?    : no, S01 is done, it built the room
duplicate  : git show 53a25bb:PLAN.md | grep -c pilot -> 0, git show 53a25bb:PLAN.md | grep -c "^| S" -> 2, the header row with S01
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order opens with one planning unit that writes the A rows, the goals the statement changes, then the steps with their products
split?     : no, one plan over one order
tidy-first?: no, the ledgers already carry the shape of a goal row and a step row
check      : python3 -c 'p=open("PLAN.md").read();g=open("GOAL.md").read();d=open("PRODUCTS.md").read();r=[l for l in p.splitlines() if l.startswith("| S02 |")];assert len(r)==1,r;c=[x.strip() for x in r[0].strip("|").split("|")];assert ("| %s |"%c[1]) in g,c;assert ("| %s |"%c[2]) in d,c;print("S02 serves",c[1],"on",c[2])'
files      : GOAL.md:17-20 · PLAN.md:10-12 · PRODUCTS.md:16-18 · UNITS.md:23-64 · unit.log:1-234, from git diff -U0 at close
base       : U0001 closed, commit 53a25bb
lines      : +51 ~1 −0 moved 0, by staged tree at close
added      : the goal leaf G1 with its two acceptance checks, S02 the measure step with P12, S03 the pilot with P10, S04 the regression step with P11, the planned block U0003
rejected   : steps under G0 with no goal leaf below it, policy.step_request reads the descendant leaves of G0 and refuses every row from S02 on while that set stays empty · planned blocks for S03 and S04 inside this unit, base.step_error asks measures.py for the number of G1 at close, that file arrives with U0003, so the next planning unit cuts them · a measure that runs a sphinx build, the confined worker of measure.py starts sys.executable, which carries no docutils here, so measures.py reads the files of the room instead · a changelog entry, that file holds 5804 lines by wc -l, a product row naming it would stand over the 500 line cap of RULE §0 · a step for the class attribute of the issue text or for the uninitialized annotation of a base class, the problem statement names the cached docstring search key of an attribute, which is the instance attribute case of S03
split      : none
deleted    : none
result     : check exits 0 · GOAL.md +4 −1 · PLAN.md +3 −0 · PRODUCTS.md +3 −0 · UNITS.md +42 −0
review     : r1 fail, «the rejected key states CHANGES  stands at 2800 lines  while the file holds 5804 at HEAD and at the base commit, a false field under RULE §4.», model claude-opus-5, session 725f5998-f7e9-4bf4-9973-6bdf21c238ff, ../reviews/agent-review-u0002-r1.md · r2 pass, «the sole r1 finding is repaired with a verified count, the check fails at the base and passes at HEAD proving the S02 row resolves to a real goal and product, and every other field holds as written.», model claude-opus-5, session 37ef5f24-a5b3-49ec-a291-fe5c2c418259, ../reviews/agent-review-u0002-r2.md · r3 pass, «every clause and field verifies against the room, the check fails at 53a25bb and passes at HEAD proving the S02 row resolves to a real goal leaf and product, and the r1 count finding is repaired with the true 5804.», model claude-opus-5, session 0e0e7139-ed16-4470-89b8-ff0b61e5b92d, ../reviews/agent-review-u0002-r3.md · r4 pass, «every clause runs, the check fails at 53a25bb and passes now with the output the result key quotes, and each field, quote and cross-file claim checks out against the files themselves.», model claude-opus-5, session 5a2b951d-40c0-4739-9ed5-75c7312535ce, ../reviews/agent-review-u0002-r4.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · closed
sentence   : measures.py gives G1 its number, the acceptance checks of G1 that hold
plan       : A0001 · S02
delete?    : no, the room holds no measures.py, so G1 reads no tool
modify?    : no, measure.py of the gate already looks for a room file of this name
duplicate  : git ls-tree -r --name-only HEAD | grep -c "^measures.py$" -> 0, git show HEAD --stat | grep -c measures.py -> 0
cause      : view layer of inputs → rules → state → result → view, RULE §5: each goal leaf carries one number the room computes, the status prints it
split?     : no, one leaf with one number
tidy-first?: no, measure.py calls a room adapter by this name already
check      : python3 -B unit.py status . | grep -qE "^\| G1 \|.*\| 0 of 2 \|$"
files      : UNITS.md:45,48-64 · measures.py:1-47 · unit.log:235-273, from git diff -U0 at close
base       : U0002 closed, commit aa550d0
lines      : +47 ~18 −0 moved 0, by staged tree at close
added      : g1 with its two acceptance checks, mro_analyzer over the mro loop of get_class_members, regression_cases over the autoclass suite with its fixture, text_of under both
rejected   : a measure that imports sphinx and calls get_class_members, the confined worker of measure.py starts sys.executable, which carries no docutils here, so the import raises and the leaf reads no value · a measure that runs pytest, the worker denies every write but /dev/null and its own protocol file, a sphinx build writes an output tree · a number read from the ledger alone, the closed unit count moves with the work, not with the behavior of autodoc
split      : none
deleted    : none
result     : check exits 0 · UNITS.md +18 −18 · measures.py +47 −0
review     : r1 fail, «the lines key reports ~15 modified lines while the command it names,  git diff --numstat  over the two files, reports 17, a false field under §4.», model claude-opus-5, session 29dc7812-88fc-4d7a-98d6-f7a48b5c8930, ../reviews/agent-review-u0003-r1.md · r2 pass, «every check clause ran, the G1 row prints a number that only measures.py can supply, the clause exits 1 at aa550d0 and 0 now, and r1's false lines field is corrected to the 18 its own command reports.», model claude-opus-5, session 4a8ef372-f004-48a4-abbe-b4886ff4536a, ../reviews/agent-review-u0003-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · structural · open
sentence   : the plan cuts its two remaining steps into one block each
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : PLAN.md:≤6 · UNITS.md:≤50
base       : U0003 closed, commit b4fbf9c
lines      : ≤100
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 

## U0005 · 2026-11-09 · behavioral · planned
sentence   : get_class_members reads the attribute docstrings of every class of the mro, not of the documented class alone
plan       : A0001 · S03
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : sphinx/ext/autodoc/importer.py:≤45 · UNITS.md:≤25
base       : U0004 the planning unit that cuts this block
lines      : ≤100
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 

## U0006 · 2026-11-09 · structural · planned
sentence   : the autoclass suite holds the two regression cases over an inherited instance attribute
plan       : A0001 · S04
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : tests/test_ext_autodoc_autoclass.py:≤60 · tests/roots/test-ext-autodoc/target/instance_variable.py:≤12 · UNITS.md:≤25
base       : U0005 the unit that makes the behavior these cases expect
lines      : ≤100
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 
