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
sentence   : the room plans the direct ITRS to Observed transform work
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, the room holds no step for the owner order yet
modify?    : no, S01 made the ledgers, it cannot carry the transform work
duplicate  : git show HEAD:PLAN.md | grep -c "^| S0" gives 1 at HEAD, S01 alone
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order starts with one planning unit that adds the goal leaf, its steps, the first planned blocks
split?     : no, one planning unit per owner order
tidy-first?: no, the six ledgers already carry the shape
check      : python3 -B -c "import measure, base, ledger; text, bl = ledger.load('.'); bad = [e for u, s, k, v in bl if s == 'planned' for e in [base.step_error('.', v, bl)] if e]; print(len(bad), sum(s == 'planned' for u, s, k, v in bl))" | grep -q "^0 3$" · python3 -B -c "import measure, ledger; rows = ledger.rows_of('.', 'PLAN.md', 'S'); print(sum('pilot' in r[3] for r in rows), len(rows))" | grep -q "^1 3$" · python3 -B -c "import measure, ledger; rows = ledger.rows_of('.', 'GOAL.md', 'G'); print(len(rows), rows[-1][0], measure.measures('.', [], ['G1'])['G1'])" | grep -q "^2 G1 no tool$"
files      : GOAL.md:17-18 · OWNER.md:7 · PLAN.md:10-11 · UNITS.md:23-106 · unit.log:1-321, from git diff -U0 at close
base       : U0001 closed, commit 11b06f8
lines      : +87 ~2 −0 moved 0, by staged tree at close
added      : G1 with its acceptance measure, S02 the measure step, S03 the pilot step, the planned blocks U0003 U0004 U0005
rejected   : a leaf per frame pair, one leaf covers the four transforms · a research unit, the issue text carries the source code · a step for the documentation, the module docstring carries it · refraction as its own step, S03 owns the whole module
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +2 −1 · OWNER.md +1 −1 · PLAN.md +2 −0 · UNITS.md +84 −0
review     : r1 fail, «the round gave no verdict, the reviewer session stopped at its turn cap with exit 1», model claude-opus-5, session fb67a243-8483-41a2-8881-60e48966afe3, ../reviews/agent-review-u0002-r1.md · r2 pass, «every check clause fails at 11b06f8 and passes now through real step-eligibility and measure outcomes, and every field holds against the files it names.», model claude-opus-5, session 4872f093-aab9-47ee-9fc0-a2f1cb024360, ../reviews/agent-review-u0002-r2.md · r3 pass, «every check clause fails at the base and passes now through real step-eligibility and measure outcomes, and every field holds against the files and logs it names.», model claude-opus-5, session 317d40e3-e46b-485f-8bf3-08a6dd562bc7, ../reviews/agent-review-u0002-r3.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · closed
sentence   : measures.py answers the failing acceptance case count of the direct ITRS to Observed transforms
plan       : A0001 · S02
delete?    : no, the room owns no measure tool, G1 reads no tool
modify?    : no, measure.py is the hectoline adapter by link, it reads the room tool
duplicate  : ls measures.py gives no such file at 5bf27e0, the room holds no measure tool
cause      : result layer of inputs → rules → state → result → view, RULE §5: each goal leaf carries one number the room computes
split?     : no, one leaf needs one function
tidy-first?: no, the adapter interface already exists in measure.py
check      : grep -q "^def g1" measures.py · python3 -I -B measures.py g1 . | grep -q "^g1 3$" · python3 -B -c "import measure, ledger; print(measure.measures('.', ledger.load('.')[1], ['G1'])['G1'])" | grep -q "^3$"
files      : GOAL.md:18 · PLAN.md:10 · UNITS.md:45,48-64 · measures.py:1-75 · unit.log:322-483, from git diff -U0 at close
base       : U0002 closed, commit 5bf27e0
lines      : +75 ~20 −0 moved 0, by staged tree at close
added      : g1 with its six acceptance cases, the G1 baseline 3 in GOAL.md, S02 done in PLAN.md
rejected   : an astropy import inside the confined worker, the worker interpreter holds no numpy, the cases run in a child under .venv · pytest as the case runner, the room measures one number, not a test report · a case per frame attribute, six cases cover the two frames and the air · a tolerance of zero on the millimetre cases, the geoid round trip carries float noise
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +1 −1 · PLAN.md +1 −1 · UNITS.md +18 −18 · measures.py +75 −0
review     : r1 pass, «every clause fails at 5bf27e0 and passes now through the real acceptance cases and the confined adapter, and each field holds against the file it names.», model claude-opus-5, session 8c0235cc-3cd2-4063-bafe-25079703120c, ../reviews/agent-review-u0003-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · behavioral · open
sentence   : the frame graph gains four direct ITRS to Observed transforms
plan       : A0001 · S03
delete?    : no, no ITRS to Observed transform exists, the graph routes through the GCRS
modify?    : no, intermediate_rotation_transforms.py owns the GCRS route, this route leaves it untouched
duplicate  : git ls-files astropy/coordinates/builtin_frames/ | grep observed gives 2 at 7ef66fa, cirs_observed_transforms.py and icrs_observed_transforms.py, neither starts in the ITRS
cause      : rules layer of inputs → rules → state → result → view, the frame graph decides the route, a direct edge replaces the GCRS detour that applies geocentric aberration
split?     : no, the four transforms share one matrix rule
tidy-first?: no, the module is new, the sibling observed transform modules set its shape
check      : grep -q "^def itrs_to_observed" astropy/coordinates/builtin_frames/itrs_observed_transforms.py · python3 -I -B measures.py g1 . | grep -q "^g1 1$" · .venv/bin/python -B -c "from astropy.coordinates import AltAz, HADec, ITRS; from astropy.coordinates.baseframe import frame_transform_graph as g; pairs = [(ITRS, AltAz), (ITRS, HADec), (AltAz, ITRS), (HADec, ITRS)]; print(sum(1 for a, b in pairs if len(g.get_transform(a, b).transforms) == 1))" | grep -q "^4$"
files      : astropy/coordinates/builtin_frames/itrs_observed_transforms.py:≤80 · astropy/coordinates/builtin_frames/__init__.py:≤1 · PLAN.md:≤2 · UNITS.md:≤16
base       : U0003 closed, commit 7ef66fa
lines      : +≤85 ~≤14
added      : itrs_to_altaz_mat, itrs_to_hadec_mat, itrs_to_observed_mat, itrs_to_observed, observed_to_itrs, the import line of the module, S03 open in PLAN.md
rejected   : an obstime check between the two frames, the module docstring states that the output obstime is adopted · a guard on a location of None or on a unit sphere, the frame attribute error already names the missing piece · aberration, a target that carries geocentric aberration goes through the ICRS, the docstring says so · a direct AltAz to HADec edge, it would drop aberration from a route that needs it
split      : none
deleted    : none
result     : 
review     : 
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-09 · behavioral · planned
sentence   : the direct ITRS to Observed transforms carry refraction
plan       : A0001 · S03
delete?    : 
modify?    : 
duplicate  : 
cause      : 
split?     : 
tidy-first?: 
check      : 
files      : astropy/coordinates/builtin_frames/itrs_observed_transforms.py:≤60 · PLAN.md:≤2 · UNITS.md:≤16
base       : U0004
lines      : +≤65 ~≤15
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 
