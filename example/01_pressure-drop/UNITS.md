# UNITS — 01_pressure-drop

## U0001 · 2026-11-08 · structural · closed
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
lines      : +84 ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py
added      : the six ledgers, the links, the bootstrap commit
rejected   : a copy of the rule or the gate, links
split      : none
deleted    : none
result     : check exits 0 0 0 · the bootstrap commit
review     : written closed by room.py, the review of the room maker unit covers it
approval   : owner 11-08 «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0002 · 2026-11-08 · structural · closed
sentence   : the planning unit: G1 with its measure, the steps S02 S03, the products P10 to P12, the planned measure unit
plan       : A0001 · S none, the planning unit of RULE §3
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "the planning unit: G1 with its measure" UNITS.md before this block: 0
cause      : inputs layer of inputs → rules → state → result → view: the A0001 order becomes one leaf, two steps and three products, RULE §3
split?     : no, one change
tidy-first?: no
check      : grep -q '^| G1 |' GOAL.md · grep -q '^| S03 | G1 | calc.py |' PLAN.md · grep -q '^| P11 | the calculator |' PRODUCTS.md
files      : GOAL.md:17-18 · PLAN.md:10-11 · PRODUCTS.md:16-18 · UNITS.md:23-64 · unit.log:1, from git diff -U0 at close
base       : U0001 closed, commit 0ebdc61
lines      : +48 ~1 −0 moved 0, by staged tree at close
added      : G1 and its target, S02 the measure step and S03 the calculator, P10 to P12, the planned block U0003 under S02
rejected   : a planned block for S03 now: G1 is unmeasured until S02 closes, so only its measure step may open, RULE §1 · a second leaf for the Reynolds number: the reference case holds it
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +2 −1 · PLAN.md +2 −0 · PRODUCTS.md +3 −0 · UNITS.md +42 −0
review     : pass r1, the diff and the nine verdict keys read, example/reviews/agent-review-u0002.md
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0003 · 2026-11-08 · behavioral · closed
sentence   : measures.py computes g1, the reference cases the calculator misses
plan       : A0001 · S02
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "measures.py computes g1" UNITS.md before this block: 0
cause      : result layer: the reference case and its analytic answer enter as data, the measure counts the misses, RULE §5
split?     : no, one change
tidy-first?: no
check      : test "$(python3 -I -B measures.py g1)" = "g1 1" · grep -q "^| S02 | .* | U0003 | done |$" PLAN.md
files      : PLAN.md:10 · UNITS.md:45,48-64 · measures.py:1-30 · unit.log:2-3, from git diff -U0 at close
base       : U0002 closed, commit 8f707c1
lines      : +30 ~19 −0 moved 0, by staged tree at close
added      : measures.py with one reference case, 81.487 Pa, and g1 · S02 done
rejected   : a tolerance below 1 percent: the target of G1 is the 1 percent of the owner line · a second case: one case is the pilot
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +1 −1 · UNITS.md +18 −18 · measures.py +30 −0
review     : pass r1, the diff and the nine verdict keys read, example/reviews/agent-review-u0003.md
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0004 · 2026-11-08 · structural · closed
sentence   : the second planning unit: G1 is measured at 1, so S03 gets its unit, then the first audit
plan       : A0001 · S none, the planning unit of RULE §3 over an empty queue
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "the second planning unit: G1 is measured at 1" UNITS.md before this block: 0
cause      : inputs layer: the queue is empty after U0003, G1 reads 1 by measures.py, so the work unit of S03 and the audit after it are planned, RULE §3
split?     : no, one change
tidy-first?: no
check      : grep -qE '^## U0006 . [0-9-]+ . audit . ' UNITS.md · grep -q '| U0005 | todo |$' PLAN.md
files      : PLAN.md:11 · UNITS.md:65-127 · unit.log:4-5, from git diff -U0 at close
base       : U0003 closed, commit 7e07499
lines      : +63 ~1 −0 moved 0, by staged tree at close
added      : the planned blocks U0005 under S03 and U0006 the audit · S03 names U0005
rejected   : a redesign of measures.py: g1 reads 1 as the plan says · a third step: G1 has two steps and one leaf
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +1 −1 · UNITS.md +63 −0
review     : pass r1, the diff and the nine verdict keys read, example/reviews/agent-review-u0004.md
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0005 · 2026-11-08 · behavioral · closed
sentence   : calc.py prints the laminar pressure drop of a pipe from four inputs
plan       : A0001 · S03
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "calc.py prints the laminar pressure drop of a pipe from four inputs" UNITS.md before this block: 0
cause      : result layer: the formula enters as one function, the command line prints it, G1 moves from 1 to 0, RULE §1 one behavior
split?     : no, one change
tidy-first?: no
check      : test "$(python3 -I -B measures.py g1)" = "g1 0" · test "$(python3 -I -B calc.py 1.0e-3 2 0.01 1e-5)" = "81.487" · grep -q "^| S03 | .* | U0005 | done |$" PLAN.md
files      : PLAN.md:11 · UNITS.md:87,90-106 · calc.py:1-14 · unit.log:6-7, from git diff -U0 at close
base       : U0004 closed, commit 017ecf2
lines      : +14 ~19 −0 moved 0, by staged tree at close
added      : calc.py with pressure_drop and its command line · S03 done · G1 at 0
rejected   : a turbulent branch: the reference case is laminar, a second case would carry it · input checks: the measure covers the one case
split      : none
deleted    : none
result     : check exits 0 0 0 · PLAN.md +1 −1 · UNITS.md +18 −18 · calc.py +14 −0
review     : pass r1, the diff and the nine verdict keys read, example/reviews/agent-review-u0005.md
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row

## U0006 · 2026-11-08 · audit · closed
sentence   : the audit of the first five units: rerun every closed check on a copy, list piles, duplicates, unused definitions
plan       : A0001 · S none, the audit of RULE §4
delete?    : no, nothing exists to delete
modify?    : no, no earlier block covers it
duplicate  : grep -c "the audit of the first five units: rerun every closed check on a copy" UNITS.md before this block: 0
cause      : result layer: audit.py runs on a copy of the room, its output is the record, RULE §4 «Audit every 10 units», here once at the end of the pilot
split?     : no, one change
tidy-first?: no
check      : grep -q '^## piles: 0' audits/audit-06.txt · grep -q '^## check rerun on a copy: ' audits/audit-06.txt
files      : UNITS.md:108,111-127 · audits/audit-06.txt:1-14 · unit.log:8-9, from git diff -U0 at close
base       : U0005 closed, commit 812f5e7
lines      : +14 ~18 −0 moved 0, by staged tree at close
added      : audits/audit-06.txt: the check rerun, the piles, the duplicates, the unused definitions, the measures
rejected   : a fix inside the audit: an audit lists, a later unit fixes
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −18 · audits/audit-06.txt +14 −0
review     : pass r1, the diff and the nine verdict keys read, example/reviews/agent-review-u0006.md
approval   : «Build a laminar pipe pressure-drop calculator that reproduces the reference case», the A0001 row
