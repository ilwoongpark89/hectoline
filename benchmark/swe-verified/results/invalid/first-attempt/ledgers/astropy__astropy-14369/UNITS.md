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
sentence   : the plan of the CDS division order fix enters with its goal leaf, its two steps, its planned blocks
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, the room holds no plan for the fix yet
modify?    : no, S01 carries the bootstrap of the room, not the fix
duplicate  : grep -ci cds PLAN.md PRODUCTS.md OWNER.md GOAL.md at 9d9307e prints 0 0 0 0
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order starts with one planning unit that writes its leaf with its steps
split?     : no, one plan
tidy-first?: no
check      : python3 -B -c "import re;p=open('PLAN.md').read();d=open('PRODUCTS.md').read();g=open('GOAL.md').read();r=[l.split('|') for l in p.splitlines() if re.match(r'\| S0[23] ',l)];assert len(r)==2;assert all('| '+x[2].strip()+' |' in g for x in r);assert all('| '+x[3].strip()+' |' in d for x in r)" · python3 -B -c "import re;p=open('PLAN.md').read();u=open('UNITS.md').read();r=[l.split('|') for l in p.splitlines() if re.match(r'\| S02 ',l)][0];assert '## '+r[6].strip()+' ' in u" · grep -qE "^\| G01 \| the CDS unit format parser" GOAL.md · grep -qE "^\| S03 \| G01 \| P10 \| pilot" PLAN.md
files      : GOAL.md:17-18 · OWNER.md:7 · PLAN.md:10-11 · PRODUCTS.md:16-17 · UNITS.md:23-64 · unit.log:1-214, from git diff -U0 at close
base       : U0001 closed, commit 9d9307e
lines      : +47 ~2 −0 moved 0, by staged tree at close
added      : G01 with its measure, S02, S03 with its pilot, P10, P11, the planned block U0003
rejected   : a planned block for S03, G01 stays unmeasured until U0003 closes, RULE §1 · a step for the io.ascii MRT reader, it calls P10 without a line of its own · a step for the astropy changelog, the owner order names the issue alone · a third step for a pytest module, the measure of G01 parses the two strings of TASK.md itself
split      : none
deleted    : none
result     : check exits 0 0 0 0 · GOAL.md +2 −1 · OWNER.md +1 −1 · PLAN.md +2 −0 · PRODUCTS.md +2 −0 · UNITS.md +42 −0
review     : r1 pass, «every check clause fails at 9d9307e and passes now, and every key fact, quote and cross-file claim of the block holds.», model claude-opus-5, session 0887646d-db08-4790-a028-bf8da0990b97, ../reviews/agent-review-u0002-r1.md · r2 pass, «every check clause fails at 9d9307e and passes now, the r1 budget finding is fixed, and every key fact, quote and cross-file claim of the block holds.», model claude-opus-5, session 4e36b575-5340-4a3c-8566-62dc3f6d0377, ../reviews/agent-review-u0002-r2.md · r3 fail, «the first check clause exits 1 on the working tree because PLAN.md S03 names unit U0004 and UNITS.md holds no U0004 block.», model claude-opus-5, session fb311b1c-6f2f-4fbd-9ac3-d76f6aaaf90a, ../reviews/agent-review-u0002-r3.md · r4 pass, «every check clause fails at the base and passes now, the r3 finding does not reproduce, and every field, quote and cross-file claim of the block holds.», model claude-opus-5, session 2e7f6187-bdac-4057-b0ee-e1949e309389, ../reviews/agent-review-u0002-r4.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · structural · closed
sentence   : the measure of G01 enters as measures.py
plan       : A0001 · S02
delete?    : no, the room computes no leaf number yet
modify?    : no, measure.py of hectoline reads a measures.py of the room, the room holds none
duplicate  : git grep -c "def g01" f24de0e -- "*.py" prints 0 files · git grep -l "10+3J/m/s/kpc2" f24de0e prints TASK.md alone
cause      : result layer of inputs → rules → state → result → view, RULE §5: the number of a goal leaf comes from the measures.py of its room
split?     : no, one leaf asks for one function
tidy-first?: no
check      : python3 -B -c "import re, measures; v = measures.g01('.', []); assert re.fullmatch(r'[012] of 2', v)" · python3 -B unit.py status . | grep -qE "^\| G01 \|.*\| 2 of 2 \| [012] of 2 \|$"
files      : PLAN.md:10 · UNITS.md:45,48-64 · measures.py:1-43 · unit.log:215-276, from git diff -U0 at close
base       : U0002 closed, commit f24de0e
lines      : +43 ~19 −0 moved 0, by staged tree at close
added      : measures.py with g01, the MRT table of TASK.md, the probe of the two unit strings, S02 turns done
rejected   : an import of astropy inside measures.py, the gate runs on a python without numpy · a measure of the parse alone, the issue reports the MRT reader · a clause pinned to 0 of 2, the audit reruns it after the fix
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +1 −1 · UNITS.md +18 −18 · measures.py +43 −0
review     : r1 pass, «both check clauses exit 0 now and non-zero at f24de0e, every field and cross-file claim of the block holds, and the change stays behind the S02 interface within its budgets.», model claude-opus-5, session 8d8cbdaf-b62a-4fcd-8023-a93f05ae51e4, ../reviews/agent-review-u0003-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · structural · closed
sentence   : the planned block of the CDS parser fix enters over the empty queue
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, the queue of planned blocks is empty
modify?    : no, U0003 is closed, a final block never changes
duplicate  : grep -c "· planned$" UNITS.md at 0c40533 prints 0
cause      : state layer of inputs → rules → state → result → view, RULE §3: the planning unit runs over an empty planned queue
split?     : no, one block
tidy-first?: no
check      : python3 -B -c "import re;u=open('UNITS.md').read();b=re.split(r'^## U0005 ', u, flags=re.M)[-1];assert re.search(r'plan +: A0001 \S+ S03', b);assert 'astropy/units/format/cds.py' in b" · python3 -B -c "p=open('PLAN.md').read();r=[l.split('|') for l in p.splitlines() if l.startswith('| S03 ')][0];assert r[6].strip()=='U0005'"
files      : PLAN.md:11 · UNITS.md:65-106 · unit.log:277-328, from git diff -U0 at close
base       : U0003 closed, commit 0c40533
lines      : +42 ~1 −0 moved 0, by staged tree at close
added      : the planned block U0005 under S03, the S03 row that names it
rejected   : a redesign, no unit failed · an audit, the room holds 4 final units under the 10 level · an A in conflict, A0001 stands alone · a measure step, U0003 gives G01 its number 0 of 2 · a step for a pytest module of astropy, the measure of G01 guards the division order already
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +1 −1 · UNITS.md +42 −0
review     : r1 fail, «the first check clause can never pass because its own text puts the literal  ## U0005  into UNITS.md, so the split lands inside the check line and both of its asserts fail on the working tree.», model claude-opus-5, session 4baebc0b-8e5d-4433-8d33-46a1982ecf2e, ../reviews/agent-review-u0004-r1.md · r2 pass, «both check clauses exit 0 on the working tree and non-zero at base 0c40533, r1's finding is fixed, and every field of the block holds against OWNER.md, PLAN.md, measures.py and the budgets.», model claude-opus-5, session 42eb9bb5-cd48-40eb-b483-76721e8e2f24, ../reviews/agent-review-u0004-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-09 · behavioral · closed
sentence   : the CDS unit format parser divides from the left
plan       : A0001 · S03
delete?    : no, a grammar without a division rule reads no CDS unit
modify?    : no, every block of the room is final, the grammar line carries no block
duplicate  : git grep -l "DIVISION combined_units" 2007f37 prints astropy/units/format/cds.py with its table alone · ogip.py line 197 already divides from the left
cause      : inputs layer of inputs → rules → state → result → view, RULE §2: the unit string enters astropy through this grammar, so the order of its divisions is a rule of the grammar
split?     : no, two productions of one grammar
tidy-first?: no, the grammar holds both productions already
check      : python3 -B -c "import measures; assert measures.g01('.', []) == '2 of 2'" · .venv/bin/python -c "import warnings;warnings.simplefilter('ignore');from astropy import units as u;assert u.Unit('erg/s/cm2/nm',format='cds')==u.Unit(u.erg/u.s/u.cm**2/u.nm);assert u.Unit('J/m.s',format='cds')==u.Unit(u.J/(u.m*u.s))"
files      : PLAN.md:11 · UNITS.md:87,90-106 · astropy/units/format/cds.py:174,185 · astropy/units/format/cds_parsetab.py:20,22,31,41-67 · unit.log:329-401, from git diff -U0 at close
base       : U0004 closed, commit 2007f37
lines      : +0 ~51 −0 moved 0, by staged tree at close
added      : the left-recursive division production, the product production that binds tighter than a division, the regenerated LALR table of ply
rejected   : a semantic fix under the old right-recursive production, the order of the parse then lives outside the grammar · a delete of cds_parsetab.py, astropy ships that table with the package · a drop of optimize in astropy/utils/parsing.py, every other format pays for one grammar · a left-recursive product production, a product reads the same either way · a test module for astropy, the measure of G01 reads the MRT table of TASK.md already
split      : none
deleted    : the production "unit_expression DIVISION combined_units" of p_division_of_units, cds.py:185 at 2007f37 · the LALR rows of the old grammar, cds_parsetab.py lines 20-67 at 2007f37
result     : check exits 0 0 · PLAN.md +1 −1 · UNITS.md +18 −18 · astropy/units/format/cds.py +2 −2 · astropy/units/format/cds_parsetab.py +30 −30
review     : r1 pass, «both check clauses fail at base 2007f37 and exit 0 now, the diff changes only the grammar of combined units behind the S03 interface with the table regenerated identically by ply, 1192 related astropy tests pass, and every verdict key holds against OWNER.md, PLAN.md, GOAL.md and the budgets.», model claude-opus-5, session 1dc84dab-3cb4-4a40-b1ff-88b9b4335f7f, ../reviews/agent-review-u0005-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0006 · 2026-11-09 · audit · open
sentence   : the audit of the met goal checks runs over this room
plan       : A0001 · S none, an audit unit carries no step, RULE §3
delete?    : yes, this unit deletes the build tree of setup.py, RULE §1 names an audit as deletions only
modify?    : no, an audit unit never changes a final block
duplicate  : grep -cE "^## U\d{4} · \S+ · audit ·" UNITS.md at da70d99 prints 0
cause      : state layer of inputs → rules → state → result → view, RULE §4: an audit runs once when the goal checks are met
split?     : no, one audit
tidy-first?: no
check      : python3 -B -c "import os, measures;assert not os.path.isdir('build');assert measures.g01('.', []) == '2 of 2'"
files      : UNITS.md:≤25
base       : U0005 closed, commit da70d99
lines      : ≤30
added      : 
rejected   : a delete of .venv, measures.py parses the two strings of TASK.md through it · a delete of the in-place .so files of astropy, the measure imports them · a delete of measures.py g01 from the unused def list, measure.py calls it by getattr · a finding on the 2000 astropy files no files key names, the room adopted them as its baseline, RULE §4
split      : none
deleted    : the build tree of setup.py build_ext, 14 MB, no block of this room names it
result     : 
review     : 
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row
