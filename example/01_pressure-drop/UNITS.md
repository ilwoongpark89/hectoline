# UNITS — 01_pressure-drop

## U0001 · 2026-11-12 · structural · closed
sentence   : the room 01_pressure-drop exists with its ledgers, its links, this block
plan       : A0001 · S01
delete?    : no, a new folder
modify?    : no, a new folder
duplicate  : the folder did not exist, room.py made it
cause      : state layer of inputs → rules → state → result → view, RULE §0: a numbered folder with the six ledgers and a link to the rule is a room
split?     : no, one room
tidy-first?: no
check      : python3 -I -B unit.py validate . · test -L RULE.md · test -L unit.py
files      : GOAL.md · PLAN.md · PRODUCTS.md · RESEARCH.md · UNITS.md · OWNER.md · RULE.md · unit.py · measure.py · audit.py · .gitignore
base       : none, the first block of this room
lines      : +95 ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py
added      : the six ledgers, the links, the bootstrap commit, the leaf G1 with S02, S03, the planned U0002, unread until the review of U0002, a pipe sign of the check reads ¦ in the leaf
rejected   : a copy of the rule or the gate, links
split      : none
deleted    : none
result     : check exits 0 0 0 · the bootstrap commit
review     : written closed by room.py, the review of the room maker unit covers it
approval   : owner 11-12 «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0002 · 2026-11-12 · behavioral · closed
sentence   : measures.py computes the count of G1
plan       : A0001 · S02
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "measures.py computes the count of G1" UNITS.md before this block: 0
cause      : result layer: the reference case and its analytic answer enter as data, the measure counts the misses, RULE §5
split?     : no, one change
tidy-first?: no
check      : test "$(python3 -I -B measures.py g1)" = "g1 1" · grep -q "^| S02 | .* | U0002 | done |$" PLAN.md
files      : GOAL.md:18 · PLAN.md:10 · UNITS.md:24,27-44 · measures.py:1-30 · unit.log:1-3, from git diff -U0 at close
base       : U0001 closed, commit be74c6e
lines      : +45 ~6 −0 moved 0, by staged tree at close
added      : measures.py with one reference case, 81.487 Pa, and g1 · the measure and the target 0 of G1 · S02 done
rejected   : a tolerance below 1 percent: the target of G1 is the 1 percent of the owner line · a second case: one case is the pilot
split      : none
deleted    : none
result     : check exits 0 0 · GOAL.md +1 −1 · PLAN.md +1 −1 · UNITS.md +19 −4 · measures.py +30 −0
review     : r1 pass, the build session, /private/tmp/hectoline-example/reviews/agent-review-u0002-r1.md sha256=f6f52b3b44ebb183bdaf4418e70b8565235dec23e7f6e80a01f1b3b6647facda
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0003 · 2026-11-12 · structural · closed
sentence   : the planning unit: G1 reads 1, so the pilot step S03 names calc.py with its two units, then the first audit
plan       : A0001 · S none, the planning unit of RULE §3 over an empty queue
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "the planning unit: G1 reads 1" UNITS.md before this block: 0
cause      : inputs layer of inputs → rules → state → result → view: the queue is empty after U0002, G1 reads 1 by measures.py, so the two work units of S03 and the audit after them are planned, RULE §3
split?     : no, one change
tidy-first?: no
check      : grep -qE '^## U0006 . [0-9-]+ . audit . ' UNITS.md · grep -q '| U0004 U0005 | todo |$' PLAN.md · grep -q '^| S01 | G0 | P01, ' PLAN.md · grep -q '^| P11 | the calculator |' PRODUCTS.md
files      : PLAN.md:9,11 · PRODUCTS.md:17-18 · UNITS.md:45-128 · unit.log:4-5, from git diff -U0 at close
base       : U0002 closed, commit d4fa121
lines      : +86 ~2 −0 moved 0, by staged tree at close
added      : S03 names calc.py with U0004 and U0005 · S01 names its product P01 · P11 and P12 · the planned blocks U0004 and U0005 under S03 and U0006 the audit
rejected   : a redesign of measures.py: g1 reads 1 as the plan says · a second leaf for the Reynolds number: the reference case holds it
split      : none
deleted    : none
result     : check exits 0 0 0 0 · PLAN.md +2 −2 · PRODUCTS.md +2 −0 · UNITS.md +84 −0
review     : r1 pass, the build session, /private/tmp/hectoline-example/reviews/agent-review-u0003-r1.md sha256=c0162fbe6cd8e5b67298f04d3d6e2a285040d7d0d227f19cfd8965c3b1275961
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row


## U0004 · 2026-11-12 · behavioral · closed
sentence   : calc.py holds the laminar pressure drop of a pipe as one function
plan       : A0001 · S03
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "calc.py holds the laminar pressure drop of a pipe as one function" UNITS.md before this block: 0
cause      : result layer: the formula enters as one function before any caller exists, RULE §1 one behavior
split?     : no, one change
tidy-first?: no
check      : test "$(python3 -B -c "import sys; sys.path.insert(0, '.'); import calc; print(round(calc.pressure_drop(1.0e-3, 2, 0.01, 1e-5), 3))")" = "81.487"
files      : UNITS.md:67,70-86 · calc.py:1-9 · unit.log:6-7, from git diff -U0 at close
base       : U0003 closed, commit 285780e
lines      : +9 ~18 −0 moved 0, by staged tree at close
added      : calc.py with pressure_drop · G1 still at 1, the measure calls the command line of the next unit
rejected   : the command line in this unit: a second behavior, the next unit holds it
split      : none
deleted    : none
result     : check exits 0 · UNITS.md +18 −18 · calc.py +9 −0
review     : r1 pass, the build session, /private/tmp/hectoline-example/reviews/agent-review-u0004-r1.md sha256=050832c175cff85ba14d0aeea7ec35e4ff34057e582844b92d5013dba8577e78
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0005 · 2026-11-12 · behavioral · closed
sentence   : calc.py prints the pressure drop from four inputs on its command line
plan       : A0001 · S03
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "calc.py prints the pressure drop from four inputs on its command line" UNITS.md before this block: 0
cause      : result layer: the command line calls the one function, G1 moves from 1 to 0, RULE §1 one behavior
split?     : no, one change
tidy-first?: no
check      : test "$(python3 -I -B measures.py g1)" = "g1 0" · test "$(python3 -I -B calc.py 1.0e-3 2 0.01 1e-5)" = "81.487" · grep -q "^| S03 | .* | U0004 U0005 | done |$" PLAN.md
files      : PLAN.md:11 · UNITS.md:88,91-107 · calc.py:2,4,10-14 · unit.log:8-9, from git diff -U0 at close
base       : U0004 closed, commit 815c4dc
lines      : +5 ~21 −0 moved 0, by staged tree at close
added      : the command line of calc.py with its usage line · S03 done · G1 at 0
rejected   : a turbulent branch: the reference case is laminar, a second case would carry it · input checks: the measure covers the one case
split      : none
deleted    : none
result     : check exits 0 0 0 · PLAN.md +1 −1 · UNITS.md +18 −18 · calc.py +7 −2
review     : r1 pass, the build session, /private/tmp/hectoline-example/reviews/agent-review-u0005-r1.md sha256=44e4916025397b6d6d78d656fe9d73d64b427144447e7a710d367b9f86e71000
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0006 · 2026-11-12 · audit · closed
sentence   : the audit of the first five units: rerun every closed check on a copy, list piles, duplicates, unused definitions
plan       : A0001 · S none, the audit of RULE §4
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "the audit of the first five units: rerun every closed check on a copy" UNITS.md before this block: 0
cause      : result layer: audit.py runs on a copy of the room, its output is the record, RULE §4 «Audit every 10 units», here once at the end of the pilot
split?     : no, one change
tidy-first?: no
check      : grep -q '^## piles: 0' audits/audit-06.txt · grep -q '^## check rerun on a copy: ' audits/audit-06.txt
files      : UNITS.md:109,112-129 · audits/audit-06.txt:1-36 · unit.log:10-11, from git diff -U0 at close
base       : U0005 closed, commit 2a92153
lines      : +37 ~18 −0 moved 0, by staged tree at close
added      : audits/audit-06.txt: the check rerun, the piles, the duplicates, the unused definitions, the measures
rejected   : a fix inside the audit: an audit lists, a later unit fixes
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +19 −18 · audits/audit-06.txt +36 −0
review     : r1 pass, the build session, /private/tmp/hectoline-example/reviews/agent-review-u0006-r1.md sha256=8654147c74f3f4c96928edf009d59ea14f211b85e1d8e6846a88fbb6073f18fb
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

