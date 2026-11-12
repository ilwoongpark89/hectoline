# UNITS — 01_task

## U0001 · 2026-11-12 · structural · closed
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
lines      : +95 ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py
added      : the six ledgers, the links, the bootstrap commit, the leaf G1 with S02, S03, the planned U0002, unread until the review of U0002, a pipe sign of the check reads ¦ in the leaf
rejected   : a copy of the rule or the gate, links
split      : none
deleted    : none
result     : check exits 0 0 0 · the bootstrap commit
review     : written closed by room.py, the review of the room maker unit covers it
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0002 · 2026-11-12 · behavioral · closed
sentence   : measures.py computes the count of G1
plan       : A0001 · S02
delete?    : no, the room has no tool that counts the checks of G1
modify?    : no, measures.py does not exist, the room reads «no tool» per leaf
duplicate  : git grep -lE '^def g1' 6f3cd9a -- '*.py' · 0 hits · git grep -lE 'ascii.cds|format=.cds.' 6f3cd9a -- '*.py' ':!astropy/*' · 0 hits
cause      : result layer of inputs → rules → state → result → view, RULE §5: a goal leaf carries one number the room computes, and G1 had none, so the leaf stood unmeasured and only its measure step could open. intent: count how many of the three acceptance checks of TASK.md the room's astropy passes. result: 0 of 3, the two units of the MRT example and the table read from it all come out wrong
split?     : no, one number for one leaf
tidy-first?: no, measures.py is a new file of the room
check      : python3 -I -B measures.py | grep -E '^[0-3] of 3$' · python3 -B unit.py status . | grep -E '^\| G1 \|.*\| [0-3] of 3 \|$'
files      : GOAL.md:18 · PLAN.md:10 · UNITS.md:24,27-44 · measures.py:1-40 · unit.log:1-152, from git diff -U0 at close
base       : U0001 closed, commit 6f3cd9a
lines      : +55 ~6 −0 moved 0, by staged tree at close
added      : measures.py, g1 with the probe that holds the three acceptance checks of TASK.md, the sample read from the MRT block of TASK.md, the first number of G1 in GOAL.md, S02 done in PLAN.md
rejected   : a pytest file in the room, a test file opens its own unit, RULE §4 · a second copy of the MRT example inside measures.py, the probe reads the block of TASK.md itself · astropy built inside the room, its build artefacts would stand as piles
split      : none
deleted    : none
result     : check exits 0 0 · GOAL.md +1 −1 · PLAN.md +1 −1 · UNITS.md +19 −4 · measures.py +40 −0
review     : r1 pass, «both clauses run green now and red at the base, and the number they prove is really computed by  measures.py  from the room's own astropy source through the linked format package.», model claude-opus-5, session fc394b52-c0d9-4df8-9aa3-93d2f4a99dcf, /private/tmp/hectoline-hard-work-1/astropy__astropy-14369/hectoline-hard/reviews/agent-review-u0002-r1.md sha256=2e9a467f44566e331b305d88e5507c7ea17859468fa68498fe213622545f0aea
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-13 · structural · closed
sentence   : the plan of S03 names its product with the unit that repairs it
plan       : A0001 · S none, a planning unit over an empty queue, RULE §3
delete?    : no, S03 stands without a product, a deletion leaves G1 unreachable
modify?    : yes, the S03 row of PLAN.md changes in place, no second row enters
duplicate  : git grep -ci cds 8603102 -- PRODUCTS.md · 0 hits · git grep -ci 'cds\|format' 8603102 -- PLAN.md PRODUCTS.md · 0 hits
cause      : state layer of inputs → rules → state → result → view, RULE §3: the queue stood empty, S03 named no product, so no work unit could open under G1. intent: name the product of S03 with the one unit that moves G1 to its target. result: S03 carries P11, the CDS unit format of astropy, with U0004 planned under it and first in the Order
split?     : no, one step takes one product here
tidy-first?: no, the rows exist, their cells change
check      : grep -E '^\| S03 \| G1 \| P11 \|.*0 of 3 to 3 of 3' PLAN.md · grep -E '^\| P11 \|.*astropy/units/format/cds.py' PRODUCTS.md · sed -n '/^## Order/,$p' PLAN.md | grep -E '^1\. U0004, the division'
files      : PLAN.md:11-16 · PRODUCTS.md:17 · UNITS.md:45-72 · unit.log:153-180, from git diff -U0 at close
base       : U0002 closed, commit 8603102
lines      : +34 ~1 −0 moved 0, by staged tree at close
added      : P11 in PRODUCTS.md, the product of S03 · the S03 row with its interface and its move of G1 · the section Order of PLAN.md · the planned block of U0004
rejected   : a second step for the parse table, ply writes it from the grammar of the same file, one step holds both · a research unit on the CDS standard, TASK.md carries the owner's quote of it with the expected reading · astropy/io/ascii/cds.py as the product, it hands its unit string to this grammar and reads back what the grammar returns
split      : none
deleted    : none
result     : check exits 0 0 0 · PLAN.md +6 −1 · PRODUCTS.md +1 −0 · UNITS.md +28 −0
review     : r1 pass, «every check clause is red at base 8603102 and green now, each field matches the files I read, and the diff stays inside the plan rows the sentence names.», model claude-opus-5, session e5791a54-bd66-4e80-8e2b-66d4cfe3992b, /private/tmp/hectoline-hard-work-1/astropy__astropy-14369/hectoline-hard/reviews/agent-review-u0003-r1.md sha256=e7784416e429c1142bd18fd4c8c48bcd56b9f008a000ff71b1998e8e495fc477
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-13 · behavioral · closed
sentence   : the division of the CDS grammar reads from left to right
plan       : A0001 · S03
delete?    : no, the grammar keeps a rule for division, its one production for the right side changes
modify?    : yes, p_division_of_units changes in place, the rule for division stays one rule
duplicate  : git grep -lE 'p_division_of_units' d1c9534 -- 'astropy/units/format/*.py' · 2 hits, cds.py with the table ply writes from it · git grep -cE 'division_of_units' d1c9534 -- astropy · cds.py 3, cds_parsetab.py 5
cause      : rules layer of inputs → rules → state → result → view, RULE §0: the CDS grammar says what a unit string means, and its production unit_expression DIVISION combined_units put every further division inside the right side, so 10+3J/m/s/kpc2 read as J/(m/(s/kpc2)). intent: let a second division take the units already divided as its left side, the reading of the CDS standard the owner quotes. result: 10+3J/m/s/kpc2 reads 1000 J / (kpc2 m s), 10-7J/s/kpc2 reads 1e-07 J / (kpc2 s), the table of TASK.md carries both
split?     : no, one production of one grammar rule
tidy-first?: no, the rule stands in its own function already
check      : python3 -I -B measures.py | grep -E '^3 of 3$' · python3 -B -c "import measures, subprocess as s; probe = 'import sys; sys.path.insert(1, sys.argv[1]); from astropy import units as u; print(u.Unit(\"W/m/s/K\", format=\"cds\") == u.W / u.m / u.s / u.K)'; print(s.run([measures.PYTHON, '-I', '-B', '-c', probe, measures.RUNNER], capture_output=True, text=True).stdout.strip())" | grep -E '^True$' · grep -E 'division_of_units DIVISION unit_expression' astropy/units/format/cds.py · grep -E 'division_of_units DIVISION unit_expression' astropy/units/format/cds_parsetab.py
files      : PLAN.md:11,15 · UNITS.md:66,69-85 · astropy/units/format/cds.py:185-186 · astropy/units/format/cds_parsetab.py:20,22,31,41-68 · unit.log:181-226, from git diff -U0 at close
base       : U0003 closed, commit d1c9534
lines      : +16 ~37 −1 moved 0, by staged tree at close
added      : the production division_of_units DIVISION unit_expression, a second division takes the first as its left side · the production unit_expression DIVISION unit_expression, the first division of a string · the table ply writes from that grammar, by rm astropy/units/format/cds_parsetab.py then an import of astropy.units.format.cds.CDS._parser in the runner · S03 done in PLAN.md with the Order rewritten
rejected   : unit_expression DIVISION combined_units kept beside the new productions, the old reading would stay reachable and the table would hold a conflict · a left side of a product after a division, J/m.s, the CDS standard reads one term after each slash, and the grammar now says so by raising instead of guessing · the table left stale with the grammar changed, ply loads the committed table in optimize mode and the change would not reach a reader · the table deleted instead of written, ply would write it into the package at first use, and a read-only install raises there
split      : none
deleted    : the production unit_expression DIVISION combined_units of p_division_of_units, with the rows ply wrote from it in cds_parsetab.py
result     : check exits 0 0 0 0 · PLAN.md +2 −3 · UNITS.md +18 −4 · astropy/units/format/cds.py +2 −1 · astropy/units/format/cds_parsetab.py +31 −30
review     : r1 pass, «every check clause is red at the base and green now, the grammar change and the regenerated table are exactly what the sentence says and stay inside S03's interface, and each field I could test is true.», model claude-opus-5, session 7f074cbc-68b9-4826-bc20-1a2bda570274, /private/tmp/hectoline-hard-work-1/astropy__astropy-14369/hectoline-hard/reviews/agent-review-u0004-r1.md sha256=fe878d052ad308f6b3109ebfd189f6e32ab0267cf7fb74bc90eef589128bab60
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

