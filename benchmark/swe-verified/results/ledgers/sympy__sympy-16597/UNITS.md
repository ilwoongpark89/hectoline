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
sentence   : the plan of the TASK.md fix stands with its goal leaf, its steps, its first blocks
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, the fix has no plan row yet, deletion reaches nothing
modify?    : no, S01 is done and names the room, not the TASK.md fix
duplicate  : grep -c "^| S0" PLAN.md → 1 at HEAD, S01 alone · grep -c "even.*->.*finite" sympy/core/assumptions.py → 0 at HEAD
cause      : rules layer of inputs → rules → state → result → view, RULE §3: an owner order opens with one planning unit that writes its goal leaf, its steps, its first blocks
split?     : no, one planning unit serves one owner order, RULE §3
tidy-first?: no, the six ledgers keep their shape
check      : grep -c "^| S0[23] | G1 |" PLAN.md | grep -qx 2
files      : GOAL.md:17-18 · OWNER.md:7 · PLAN.md:10-11 · PRODUCTS.md:16-17 · UNITS.md:23-64 · unit.log:1-134, from git diff -U0 at close
base       : U0001 closed, commit c35dc04
lines      : +47 ~2 −0 moved 0, by staged tree at close
added      : the G1 leaf with its measure, S02 and S03 with their interfaces, P10 and P11, the planned block U0003
rejected   : a planned block for S03, RULE §1 opens only the measure step under an unmeasured leaf, so S03 stays a todo row · one goal leaf per probe, one leaf carries the whole fix · a new case inside sympy/core/tests/test_assumptions.py, that file holds 1064 lines over the 500 cap of RULE §0 and no split of it serves this order, so measures.py carries the probes · a rule line «integer -> finite», the order names the even symbol and the wider line reaches the infinite integer symbols of the suite
split      : none
deleted    : none
result     : check exits 0 · GOAL.md +2 −1 · OWNER.md +1 −1 · PLAN.md +2 −0 · PRODUCTS.md +2 −0 · UNITS.md +42 −0
review     : r1 pass, «every field is true against the files, the check is red at c35dc04 and green in the tree, and the diff stays inside the ledgers a planning unit owns.», model claude-opus-5, session 52d0bcc6-d3a8-4943-a334-11fe3eba3f4b, ../reviews/agent-review-u0002-r1.md · r2 pass, «every verdict key reproduces against the files by its own command, the check is red at c35dc04 and green in the tree, and the diff touches only the ledgers a planning unit owns.», model claude-opus-5, session 53a5311b-d987-48e4-aa39-b8df2d32c15d, ../reviews/agent-review-u0002-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · closed
sentence   : measures.py computes the probe count of G1
plan       : A0001 · S02
delete?    : no, this room holds no measure tool, deletion reaches nothing
modify?    : no, measure.py of the method reads a tool the room must hold itself
duplicate  : git ls-tree HEAD --name-only | grep -c "^measures.py$" → 0 at HEAD · grep -rl "def g1" --include="*.py" . | wc -l → 1, this new file alone
cause      : result layer of inputs → rules → state → result → view, RULE §5: the number of a goal leaf is computed by a tool of the room, never typed
split?     : no, one tool carries the one leaf of this room
tidy-first?: no, measure.py already reads measures.py of a room through its confined worker
check      : python3 -B -c "import measures; print(measures.g1('.', []))" | grep -qxE "[0-3] of 3"
files      : PLAN.md:10 · UNITS.md:45,48-64 · measures.py:1-25 · unit.log:135-311, from git diff -U0 at close
base       : U0002 closed, commit 4c7877f
lines      : +25 ~19 −0 moved 0, by staged tree at close
added      : measures.py with g1 and its three probes, the base key of this block in the form the gate reads
rejected   : a probe that runs the sympy suite, the confined worker of measure.py holds 30 seconds · the status output as the clause, line_map blames the whole sympy tree and the clause then runs over 60 seconds, over the audit timeout · the queue repair gate of RULE §4 for the base key of this block, it refuses admission while no planned block is base-ready, so the author filled that key as RULE §2 gives it at open
split      : none
deleted    : none
result     : check exits 0 · PLAN.md +1 −1 · UNITS.md +18 −18 · measures.py +25 −0
review     : r1 fail, «U0003 is still a planned block with an empty check, blank open-time verdict keys, and no diff, and the  measures.py  its sentence names does not exist, so no clause can prove the claimed outcome.», model claude-opus-5, session ae4b339d-cc6b-4127-86c8-dddd1c855f18, ../reviews/agent-review-u0003-r1.md · r2 fail, «the  lines  key reports  ~18  where numstat over the same diff gives 19 modified lines by this room's own counting convention, so a verdict key is false.», model claude-opus-5, session 15fbd725-05d0-4e27-995c-6c8440cd782e, ../reviews/agent-review-u0003-r2.md · r3 pass, «every clause of the check runs red at 4c7877f and green in the tree, all nine verdict keys reproduce against the files by their own commands, and the diff adds only  g1  behind the interface S02 declares.», model claude-opus-5, session 31f5068c-3ed9-4606-9cb4-fb3b2ba6573f, ../reviews/agent-review-u0003-r3.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · structural · closed
sentence   : the queue carries the pilot block of S03
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, S03 has no block in the queue, deletion reaches nothing
modify?    : no, the three closed blocks are final, RULE §2
duplicate  : grep -c "^plan       : A0001 .* S03$" UNITS.md → 0 at HEAD · grep -c "^| S03 |" PLAN.md → 1 at HEAD, the step stands since U0002
cause      : state layer of inputs → rules → state → result → view, RULE §3: the planning unit runs over an empty queue and cuts the next block from the first step
split?     : no, one block enters the queue
tidy-first?: no, S03 with its product and its interface stands since U0002
check      : grep -c "^plan       : A0001 .* S03$" UNITS.md | grep -qx 1
files      : UNITS.md:65-106 · unit.log:312-369, from git diff -U0 at close
base       : U0003 closed, commit e122851
lines      : +42 ~0 −0 moved 0, by staged tree at close
added      : the planned block U0005 of S03, its base in the first-token form the gate reads at open
rejected   : a second planned block for a regression case inside sympy/core/tests/test_assumptions.py, that file holds 1064 lines over the 500 cap of RULE §0 · a new A row, A0001 still carries this order · a new S row, S03 stands since U0002 with its interface
split      : none
deleted    : none
result     : check exits 0 · UNITS.md +42 −0
review     : r1 pass, «every check clause runs red at e122851 and green in the tree, all nine verdict keys reproduce against the files by their own commands, and the diff stays inside the ledger a planning unit owns.», model claude-opus-5, session 4beb93be-8dea-43ce-83d9-6fdc1709f9a3, ../reviews/agent-review-u0004-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-09 · behavioral · open
sentence   : an even symbol implies a finite symbol in the core assumption rules
plan       : A0001 · S03
delete?    : no, an implication enters the rule set, deletion reaches nothing
modify?    : no, no line of _assume_rules carries this implication, the zero line binds zero alone
duplicate  : git show HEAD:sympy/core/assumptions.py | grep -c "even.*->.*finite" → 0 at HEAD · git show HEAD:sympy/core/assumptions.py | grep -c "finite" → 8 at HEAD, none of them the even line
cause      : rules layer of inputs → rules → state → result → view, TASK.md: a number is finite before it is even, so the fact rule set carries the implication, never a handler
split?     : no, one implication enters the one rule set that holds the others
tidy-first?: no, FactRules reads the new line in place
check      : python3 -B -c "import measures; print(measures.g1('.', []))" | grep -qx "3 of 3"
files      : sympy/core/assumptions.py:178-179 · UNITS.md:87-106 · PLAN.md:11, the ranges at close
base       : U0003 closed, commit 6756829
lines      : +2 ~19 −0 moved 0, by numstat at close
added      : the rule line «even           ->  finite» in _assume_rules of sympy/core/assumptions.py
rejected   : «integer -> finite», it turns every integer symbol finite, wider than the even symbol the problem statement names · «odd -> finite», it turns Symbol(integer=True, finite=False) into InconsistentAssumptions · the oo.is_even case of sympy/core/tests/test_assumptions.py, a test file beside code outside tests is denied in one unit, RULE §4
split      : none
deleted    : none
result     : check exits 1 at HEAD, 0 in the tree, the clause prints «3 of 3» · bin/test sympy/core: 1499 passed 2 failed here against 1501 passed 0 failed at HEAD, the two are oo.is_even and (-oo).is_even, None at HEAD and False now, RULE §4 denies their test file beside this line in one unit
review     : r1 fail, «the  rejected  key states that  integer -> finite  moves no probe, but that rule alone makes  measures.g1  print  3 of 3 , so the key is a false field under RULE §4.», model claude-opus-5, session b6003273-3e2d-4a4a-ba26-76529a945ed6, ../reviews/agent-review-u0005-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row
