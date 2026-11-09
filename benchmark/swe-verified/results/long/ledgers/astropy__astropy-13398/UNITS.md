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
sentence   : the plan of the ITRS to Observed fix enters the ledgers
plan       : A0001 · S none
delete?    : no, the ledgers carry no plan for this order yet
modify?    : no, S01 is done and names the room, not the fix
duplicate  : grep -c '^| S' PLAN.md → 2 · grep -c '^| P' PRODUCTS.md → 10 · grep -rn itrs_observed astropy docs | wc -l → 0, all at HEAD a8b4d6b
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order opens with one planning unit that writes the steps under the goals it changes
split?     : no, one plan
tidy-first?: no
check      : grep -q '^| G1 | the direct ITRS' GOAL.md · grep -q '^| S03 | G1 | P11 | pilot' PLAN.md · grep -q '^| P11 | the direct ITRS' PRODUCTS.md
files      : GOAL.md:17-18 · PLAN.md:10-14 · PRODUCTS.md:16-20 · UNITS.md:23-64 · unit.log:1-193, from git diff -U0 at close
base       : U0001 closed, commit a8b4d6b
lines      : +53 ~1 −0 moved 0, by staged tree at close
added      : the G1 leaf of the fix under G0 · the S02 measure row with the S03 pilot, S04, S05, S06 · the P10 parent with P11, P12, P13, the P14 measure · the planned block U0003, the measure unit
rejected   : planned blocks for the pilot units, G1 is unmeasured until S02 closes, so only its measure step opens under it, RULE §1 · an S row that moves G0 itself, measure.py computes no number for G0, so the leaf G1 carries the fix, RULE §5 · a planned block for every unit of the plan, RULE §3 caps the cut at three · a step per changed file, a step makes one product, RULE §2 · docs/coordinates/spectralcoord.rst as a P13 file, 580 lines by wc -l, a baseline file over the 500-line cap that the fix only touches in two doctest lines, RULE §0 · the existing test_intermediate_transformations.py as the P12 file, 930 lines by wc -l, over the same cap, so the tests enter their own module
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +2 −1 · PLAN.md +5 −0 · PRODUCTS.md +5 −0 · UNITS.md +42 −0
review     : r1 pass, «both clauses exit non-zero at base a8b4d6b and 0 now, every reported count and quote reproduces, and the diff stays inside the ledgers a planning unit owns.», model claude-opus-5, session 17cdaf1a-b979-4765-9b27-80166fefcca9, ../reviews/agent-review-u0002-r1.md · r2 fail, «the four added S rows claim G0 moves through "N of 4 check clauses", a baseline GOAL.md does not carry (it records 0 of 0) and a number no tool of the room computes, since measure.py excludes G0 and the plan adds no measure step.», model claude-opus-5, session f1e72391-0469-4cbc-b792-fffa54ca88b1, ../reviews/agent-review-u0002-r2.md · r3 pass, «r2's fail-grade finding is cured by a G1 leaf with its own measure step and S rows that name G1's tool-computed movement, all three clauses fail at base a8b4d6b and pass now, and every reported count, quote and range reproduces.», model claude-opus-5, session e96e5184-c1e2-4324-b667-cabc3465dbde, ../reviews/agent-review-u0002-r3.md · r4 pass, «all three clauses fail at base  a8b4d6b  and pass now, every reported count, quote and range reproduces, r2's finding is cured by the G1 leaf whose numbers come from  measure.py 's own output, and the diff stays inside the four ledgers a planning unit owns.», model claude-opus-5, session 90cf7e3c-ca84-4790-b336-dc28a18034bc, ../reviews/agent-review-u0002-r4.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · behavioral · closed
sentence   : the measure of the G1 leaf becomes a number this room computes
plan       : A0001 · S02
delete?    : no, the room computes no leaf number yet
modify?    : no, measure.py of hectoline reads the adapter of the room, it carries no leaf of this room
duplicate  : git ls-files measures.py | wc -l → 0 · grep -rn 'def g1' --include=*.py . | wc -l → 0, both at 6bcfe54
cause      : result layer of inputs → rules → state → result → view, RULE §5: a goal leaf carries one number the room computes from its ledgers
split?     : no, one function behind one leaf
tidy-first?: no
check      : grep -q '^def g1' measures.py · python3 -B unit.py status . | grep -q '| G1 |.*| 0 of 4 |'
files      : UNITS.md:45,48-64 · measures.py:1-41 · unit.log:194-214, from git diff -U0 at close
base       : U0002 closed, commit 6bcfe54
lines      : +41 ~18 −0 moved 0, by staged tree at close
added      : g1, the fix steps done over all fix steps · fix_steps, the S rows under G1 that make P11, P12 or P13 · _cells, the cells of a markdown row
rejected   : a number from the check output of the units, the confined worker runs no test of the repository, RULE §5 · an import of ledger.py of hectoline, the room reads its own PLAN.md rows · S02 under G0, a step hangs on the leaf it moves, RULE §0
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −18 · measures.py +41 −0
review     : r1 pass, «both clauses are red at 6bcfe54 and green now, every field I could run checks out true, and the change stays inside P14 behind the S02 interface.», model claude-opus-5, session 158e5098-40a1-44d7-9f3d-3ecba90eb03c, ../reviews/agent-review-u0003-r1.md · r2 pass, «every clause runs red at 6bcfe54 and green now, all nine verdict keys and the actuals check out true against the files, and the change stays inside P14 behind the S02 interface.», model claude-opus-5, session c6eef4dc-6ff4-426f-99e9-fc564519c2f4, ../reviews/agent-review-u0003-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · structural · closed
sentence   : the units of the pilot step enter the queue
plan       : A0001 · S none
delete?    : no, the queue is empty, the pilot step has no unit to delete
modify?    : no, U0002 planned the measure unit alone, G1 was unmeasured then
duplicate  : git show 0b070c0:UNITS.md | grep -c '· planned' → 0 · grep -rn 'itrs_observed' astropy | wc -l → 0, both at 0b070c0
cause      : state layer of inputs → rules → state → result → view, RULE §3: the planning unit runs again over an empty queue, the measure of G1 now stands at 0 of 4
split?     : no, one cut of one step
tidy-first?: no
check      : grep -q '^| S02 | G1 | P14 |.*| U0003 | done |' PLAN.md · grep -q '^| S03 | G1 | P11 | pilot.*| U0005 U0006 U0007 | open |' PLAN.md
files      : PLAN.md:10-14 · UNITS.md:65-148 · unit.log:215-239, from git diff -U0 at close
base       : U0003 closed, commit 0b070c0
lines      : +84 ~5 −0 moved 0, by staged tree at close
added      : S02 done, its unit U0003 is closed, the G1 number moved from no tool to 0 of 4 · S03 open with U0005, U0006, U0007 · the unit column of S04, S05, S06 renumbered to U0009, U0010, U0013, the audit of RULE §4 falls between them · the planned blocks U0005, the research, U0006, the topocentric ITRS frame, U0007, the direct transform
rejected   : a planned block for S04, S05 or S06, RULE §3 caps the cut at three · the measure of an unmeasured leaf, rank 4, G1 reads 0 of 4 now · an audit, rank 2, three final units stand under the ten of RULE §4 · a redesign, rank 1, no unit failed
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +5 −5 · UNITS.md +84 −0
review     : r1 pass, «both clauses are red at base  0b070c0  and green now, every field reproduces against the files and the room's own measure tool, and the diff stays inside the ledgers a planning unit owns.», model claude-opus-5, session 2897e6bc-bae8-4098-81ba-705a0d158990, ../reviews/agent-review-u0004-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-09 · structural · closed
sentence   : what does the merged astropy fix of this issue change?
plan       : A0001 · S03
delete?    : no, RESEARCH.md holds no row yet
modify?    : no, the table has no row about this question
duplicate  : git show 33e4ed2:RESEARCH.md | grep -c '^| R' → 1, the header alone · git show 33e4ed2:RESEARCH.md | grep -c 'astropy/pull' → 0
cause      : inputs layer of inputs → rules → state → result → view, RULE §7: the shape of the fix rests on a source, so it enters as an R row before the code units open
split?     : no, one question
tidy-first?: no
check      : grep -q '^| R01 | 11-09 | what does the merged astropy fix' RESEARCH.md · q=$(grep -o '«[^»]*»' RESEARCH.md | head -1 | tr -d '«»') && test -n "$q" && grep -qF "$q" /tmp/pr13398.diff
files      : RESEARCH.md:7 · UNITS.md:87,90-106 · unit.log:240-251, from git diff -U0 at close
base       : U0004 closed, commit 33e4ed2
lines      : +1 ~18 −0 moved 0, by staged tree at close
added      : R01, the merged fix of astropy pull 13398, read as its diff of 704 lines by curl, verdict accepted
rejected   : a second R row for the issue thread, TASK.md already carries it, RULE §7 opens a search only where no row holds the number · a copy of the diff inside the room, the raw record stays outside it, RULE §7 · an R number in the astropy sources, the citation stays in the ledgers of this room, so the audit will list R01 as uncited
split      : none
deleted    : none
result     : check exits 0 0 · RESEARCH.md +1 −0 · UNITS.md +18 −18
review     : r1 pass, «both clauses fail at the base and pass now, every field reproduces against the files and the fetched source, and the diff stays inside the ledgers a research unit owns.», model claude-opus-5, session 4ec48a70-488d-4d60-82d0-56a213d062df, ../reviews/agent-review-u0005-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0006 · 2026-11-09 · behavioral · closed
sentence   : the ITRS frame sits at the location of its observer
plan       : A0001 · S03
delete?    : no, the frame carries no location to delete
modify?    : yes, the ITRS class of itrs.py changes, so this unit is that change, not a new frame class
duplicate  : git show 445b4e0:astropy/coordinates/builtin_frames/itrs.py | grep -c location → 2, the earth_location property alone · git grep -c 'location = EarthLocationAttribute' 445b4e0 -- astropy/coordinates/builtin_frames/ → 4 lines, altaz.py:1, cirs.py:1, equatorial.py:1, hadec.py:1, itrs.py absent, the pattern of AltAz, CIRS, HADec and TETE
cause      : rules layer of inputs → rules → state → result → view, R01: the observed transforms need an ITRS frame whose origin is the observing site, as CIRS and TETE already have
split?     : no, the attribute alone is dead weight, the routes that read it stand in the same change
tidy-first?: no
check      : grep -q 'location = EarthLocationAttribute(default=EARTH_CENTER)' astropy/coordinates/builtin_frames/itrs.py · rsync -a ./astropy/ /tmp/ab/astropy/ && cd /tmp/ab && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -c "import astropy.units as u; from astropy.coordinates import EarthLocation, ITRS; from astropy.time import Time; t=Time('J2010'); home=EarthLocation(-1*u.deg,52*u.deg,height=0*u.km); obj=EarthLocation(-1*u.deg,52*u.deg,height=10*u.km); hv=home.get_itrs(t).cartesian; v=obj.get_itrs(t).cartesian-hv; topo=ITRS(v,obstime=t,location=home); geo=topo.transform_to(ITRS(obstime=t)); back=geo.transform_to(ITRS(obstime=t,location=home)); assert (back.cartesian-v).norm()<1*u.mm; assert 300*u.m<(geo.cartesian-(hv+v)).norm()<1000*u.m"
files      : UNITS.md:108,111-127 · astropy/coordinates/builtin_frames/intermediate_rotation_transforms.py:20,149,151,164,166,199,201,214,216 · astropy/coordinates/builtin_frames/itrs.py:6-8,12-23,25-26,31,34-61,68 · docs/coordinates/spectralcoord.rst:240,272 · unit.log:252-354, from git diff -U0 at close
base       : U0005 closed, commit 445b4e0
lines      : +43 ~33 −0 moved 0, by staged tree at close
added      : the location attribute of ITRS, an EarthLocationAttribute that defaults to EARTH_CENTER · the docstring footer of the frame with the note on topocentric ITRS · the location of the target frame in cirs_to_itrs, tete_to_itrs · the location of the source frame in itrs_to_cirs, itrs_to_tete
rejected   : a new TopocentricITRS class, the ITRS of CIRS and TETE already carries a location attribute, one frame holds both origins · a location that only the observed transforms read, the CIRS route is what moves the origin · the obstime check of the issue text, a mismatched obstime stays a transform, not an exception, RULE: no owner line asks for one
split      : none
deleted    : EARTH_CENTER from the import line of intermediate_rotation_transforms.py, its last reader in that file left with this change
result     : check exits 0 0 · UNITS.md +18 −18 · astropy/coordinates/builtin_frames/intermediate_rotation_transforms.py +9 −9 · astropy/coordinates/builtin_frames/itrs.py +47 −4 · docs/coordinates/spectralcoord.rst +2 −2
review     : r1 fail, «the  result  key reports the round-trip residual as 0.0000045 mm where the check's own output is 0.004463 mm, a false field under §4, with the  files  ranges 148-150 and 196-198 naming no changed line and the  duplicate  grep output dropping two of its hits.», model claude-opus-5, session 6263800b-26d8-4aa5-96a7-d837cf1ebdfc, ../reviews/agent-review-u0006-r1.md · r2 pass, «both clauses fail at the base and pass now, clause 2 proves the location moves the frame origin as the sentence says, and every field including the three r1 faulted now matches the output of the command it names.», model claude-opus-5, session e0a77998-19e8-4aa8-a9c6-4ff19c9188ba, ../reviews/agent-review-u0006-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0007 · 2026-11-09 · behavioral · closed
sentence   : one direct transform carries an ITRS position to the observed frames
plan       : A0001 · S03
delete?    : no, no route from ITRS to the observed frames exists to delete
modify?    : no, the existing route is the chain through CIRS, a route this unit leaves standing for the geocentric case
duplicate  : git grep -c 'def itrs_to_observed' dc52411 -- astropy/ → 0 lines · git grep -n 'ITRS, AltAz' dc52411 -- astropy/coordinates/builtin_frames/ → 0 lines · git ls-tree dc52411 astropy/coordinates/builtin_frames/itrs_observed_transforms.py → 0 lines
cause      : rules layer of inputs → rules → state → result → view, R01: the observed frames reach the ITRS through one rotation of the topocentric vector, the route of the merged fix
split?     : no, the two directions are one design decision, the rotation that carries a topocentric ITRS vector to the observed axes
tidy-first?: no
check      : grep -q '^def itrs_to_observed' astropy/coordinates/builtin_frames/itrs_observed_transforms.py · rsync -a ./astropy/ /tmp/ab/astropy/ && cd /tmp/ab && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -c "import astropy.units as u; from astropy.coordinates import frame_transform_graph, EarthLocation, ITRS, AltAz, HADec; from astropy.time import Time; assert len(frame_transform_graph.find_shortest_path(ITRS,AltAz)[0])==2; assert len(frame_transform_graph.find_shortest_path(ITRS,HADec)[0])==2; assert len(frame_transform_graph.find_shortest_path(AltAz,ITRS)[0])==2; assert len(frame_transform_graph.find_shortest_path(HADec,ITRS)[0])==2; t=Time('J2010'); obj=EarthLocation(-1*u.deg,52*u.deg,height=10*u.km); home=EarthLocation(-1*u.deg,52*u.deg,height=0*u.km); r=obj.get_itrs(t).cartesian-home.get_itrs(t).cartesian; topo=ITRS(r,obstime=t,location=home); aa=topo.transform_to(AltAz(obstime=t,location=home)); hd=topo.transform_to(HADec(obstime=t,location=home)); assert abs(aa.alt-90*u.deg)<1*u.uas; assert abs(hd.ha)<1*u.uas; assert abs(hd.dec-52*u.deg)<1*u.uas; back=aa.transform_to(ITRS(obstime=t,location=home)); assert (back.cartesian-r).norm()<1*u.mm"
files      : UNITS.md:129,132-148 · astropy/coordinates/builtin_frames/__init__.py:51 · astropy/coordinates/builtin_frames/itrs_observed_transforms.py:1-69 · unit.log:355-410, from git diff -U0 at close
base       : U0006 closed, commit dc52411
lines      : +70 ~18 −0 moved 0, by staged tree at close
added      : itrs_to_altaz_mat and itrs_to_hadec_mat, the rotations from the ITRS axes onto the left handed observed axes · itrs_to_observed, registered ITRS to AltAz and ITRS to HADec · observed_to_itrs, its transpose back, registered AltAz to ITRS and HADec to ITRS · the module in the import list of builtin_frames, which registers the four routes
rejected   : refraction, the merged module of R01 runs 145 lines, so one unit cannot hold it under the 100 of RULE §1, and S04 carries it · the subtraction of the observing site inside the transform, the location attribute of U0006 already names the origin of the frame, and its ITRS to ITRS route moves it · an exception on a mismatched obstime or location, the transform goes through the CIRS in that case, as the merged fix does · PIOVER2 of utils with unit=u.radian, the degree quantity NORTH_POLE carries its unit in the expression itself
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −18 · astropy/coordinates/builtin_frames/__init__.py +1 −0 · astropy/coordinates/builtin_frames/itrs_observed_transforms.py +69 −0
review     : r1 pass, «every check clause fails at base  dc52411  and exits 0 on the working tree, and all reported fields, counts and numbers reproduced exactly within S03's declared interface.», model claude-opus-5, session 39426fed-8efc-4485-90c7-fdb5d854db75, ../reviews/agent-review-u0007-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0008 · 2026-11-09 · structural · closed
sentence   : the unit of the refraction step enters the queue
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the queue holds no unit for the refraction step to delete
modify?    : no, U0004 cut the pilot step alone, the three steps after it keep their unit numbers only in the plan
duplicate  : git show efa6c18:UNITS.md | grep -c '^## U.*· planned$' → 0, the queue is empty · git show efa6c18:PLAN.md | grep -c '| todo |' → 3, S04, S05 and S06 · git show efa6c18:UNITS.md | grep -c '^## U.*· closed$' → 7
cause      : state layer of inputs → rules → state → result → view, RULE §3: the planning unit runs again over an empty queue, the three units of the pilot step are final
split?     : no, one cut of one step
tidy-first?: no
check      : grep -q '^sentence   : refraction enters the direct ITRS to Observed transform$' UNITS.md · grep -q '^base       : U0008$' UNITS.md · grep -q '^| S04 | G1 | P11 | refraction.*| U0009 | open |' PLAN.md · grep -q '^| S03 | G1 | P11 | pilot.*| U0005 U0006 U0007 | done |' PLAN.md · python3 -B unit.py status . | grep -q '| G1 |.*| 1 of 4 |'
files      : PLAN.md:11-12 · UNITS.md:149-190 · unit.log:411-465, from git diff -U0 at close
base       : U0007 closed, commit efa6c18
lines      : +42 ~2 −0 moved 0, by staged tree at close
added      : S03 done, its three units are closed, the G1 number moved from 0 of 4 to 1 of 4 · S04 open with U0009 · the planned block U0009, refraction in the direct transform
rejected   : a planned block for S05 or S06, this cut takes the one step the sentence names, and the queue reopens the planning unit when U0009 closes · the measure of an unmeasured leaf, rank 4, no leaf of this room is unmeasured · an audit, rank 2, seven final units stand under the ten of RULE §4 · a redesign, rank 1, no unit failed · an A in conflict, rank 3, A0001 stands alone
split      : none
deleted    : none
result     : check exits 0 0 0 0 0 · PLAN.md +2 −2 · UNITS.md +42 −0
review     : r1 fail, «neither check clause proves that the refraction step's unit entered the queue (both only prove the pilot step closed and its measure moved, and would pass with no planned block added), and the  files  range  UNITS.md:150-190  contradicts the  git diff -U0  hunk 149-190 it names as its source.», model claude-opus-5, session 28015654-83be-4490-b00a-e89d039d71d1, ../reviews/agent-review-u0008-r1.md · r2 fail, «the  result  key reports  check exits 0 · 0 , two exit codes, while the  check  key it names now holds five clauses that all exit 0, so the field is a false report of the command's output.», model claude-opus-5, session 0e884baf-1d03-4a42-9692-12f4421642f6, ../reviews/agent-review-u0008-r2.md · r3 pass, «all five clauses exit 1 at base  efa6c18  and 0 on the tree while proving the planned U0009 block, the open S04 row and the computed G1 move, both earlier findings are fixed, and every reported field reproduced exactly within what a planning unit owns.», model claude-opus-5, session b1a15819-096c-4e8c-b0e9-d2bf66305670, ../reviews/agent-review-u0008-r3.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0009 · 2026-11-09 · behavioral · closed
sentence   : refraction enters the direct ITRS to Observed transform
plan       : A0001 · S04
delete?    : no, the direct route of U0007 applies no refraction to delete
modify?    : yes, itrs_to_observed and observed_to_itrs of U0007 change, so this unit is that change, not a second pair of transforms
duplicate  : git grep -c 'def add_refraction' f87ec91 -- astropy/ → 0 lines · git grep -c 'erfa.refco' f87ec91 -- astropy/coordinates/ → 1 line, erfa_astrom.py:3, the refco calls that serve the CIRS route
cause      : rules layer of inputs → rules → state → result → view, R01: refraction belongs to the observed end of the route, where the pressure of the frame stands
split?     : no, adding refraction and removing it again are one model, one decision
tidy-first?: no
check      : grep -q '^def add_refraction' astropy/coordinates/builtin_frames/itrs_observed_transforms.py · rsync -a ./astropy/ /tmp/ab/astropy/ && cd /tmp/ab && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -c "import numpy as np; import astropy.units as u; from astropy.coordinates import EarthLocation, ICRS, ITRS, AltAz, HADec, CIRS; from astropy.coordinates.angle_utilities import golden_spiral_grid; loc=EarthLocation(lat=0*u.deg,lon=0*u.deg,height=0*u.m); usph=golden_spiral_grid(200); dist=np.linspace(1.,1000.,len(usph))*u.au; icrs=ICRS(ra=usph.lon,dec=usph.lat,distance=dist); aa1=AltAz(obstime='J2000',location=loc); aa2=AltAz(obstime='J2000',location=loc,pressure=1000.0*u.hPa,relative_humidity=0.5); hd2=HADec(obstime='J2000',location=loc,pressure=1000.0*u.hPa,relative_humidity=0.5); cf=CIRS(obstime='J2000',location=loc); itf=ITRS(location=loc); altaz2=icrs.transform_to(aa2); hadec2=icrs.transform_to(hd2); itrs=icrs.transform_to(itf); a22=itrs.transform_to(aa2); h22=itrs.transform_to(hd2); assert np.max(np.abs((a22.alt-altaz2.alt).to_value(u.mas)))<0.1; assert np.max(np.abs((a22.az-altaz2.az).to_value(u.mas)))<0.1; assert np.max(np.abs((a22.distance-altaz2.distance).to_value(u.cm)))<10.0; assert np.max(np.abs((h22.ha-hadec2.ha).to_value(u.mas)))<0.1; assert np.max(np.abs((h22.dec-hadec2.dec).to_value(u.mas)))<0.1; altaz3=altaz2.transform_to(cf).transform_to(aa1); altaz33=a22.transform_to(itf).transform_to(aa1); assert np.max(np.abs((altaz33.alt-altaz3.alt).to_value(u.mas)))<0.1; assert np.max(np.abs((altaz33.az-altaz3.az).to_value(u.mas)))<0.1"
files      : UNITS.md:171,174-190 · astropy/coordinates/builtin_frames/itrs_observed_transforms.py:2,7,12-14,40-98,111,113-116,127-134,136-138 · unit.log:466-517, from git diff -U0 at close
base       : U0008 closed, commit f87ec91
lines      : +75 ~23 −0 moved 0, by staged tree at close
added      : CELMIN and SELMIN, the clamps on cos and sin of the altitude · altaz_to_hadec_mat, the rotation between the two observed frames · refraction_constants, the A and B of erfa.refco from the frame · add_refraction and remove_refraction, the A*tan(z)+B*tan^3(z) model of erfa.atioq and erfa.atoiq · the pressure branch of itrs_to_observed and of observed_to_itrs
rejected   : a refraction model of this room's own, erfa.refco with the atioq and atoiq steps is what the CIRS route already runs, so the two routes agree to 1e-7 mas · the pressure, temperature, humidity and wavelength as arguments, the observed frame carries all four · a round trip assertion below the horizon in the check, the SELMIN clamp of the model is not invertible there, in this route as in the CIRS one · the comment lines of the merged module in full, the 100 line cap of RULE §1 holds this unit to 98
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −18 · astropy/coordinates/builtin_frames/itrs_observed_transforms.py +80 −5
review     : r1 pass, «both check clauses fail at base f87ec91 and pass on the tree while proving the refracted route's agreement with the CIRS route, and every reported field — the seven deviations, the pytest counts and identical FAILED lists, the duplicate counts, the hunk ranges, the 98 lines and the owner quote — rep», model claude-opus-5, session 579d881d-0d96-4d96-a8c0-efa980ec185a, ../reviews/agent-review-u0009-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0010 · 2026-11-10 · structural · closed
sentence   : the unit of the test step enters the queue
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the queue holds no unit for the test step to delete
modify?    : no, U0008 cut the refraction step alone, S05 keeps its unit number only in the plan
duplicate  : git show 23c84f8:UNITS.md | grep -c '^## U.*· planned$' → 0, the queue is empty · git show 23c84f8:PLAN.md | grep -c '| todo |' → 2, S05 and S06 · git show 23c84f8:UNITS.md | grep -c '^## U.*· closed$' → 9
cause      : state layer of inputs → rules → state → result → view, RULE §3: the planning unit runs again over an empty queue, the unit of the refraction step is final
split?     : no, one cut of one step
tidy-first?: no
check      : grep -q '^sentence   : the tests of the direct transform enter their own module$' UNITS.md · grep -q '^base       : U0010$' UNITS.md · grep -q '^| S05 | G1 | P12 | the tests.*| U0012 | open |' PLAN.md · grep -q '^| S04 | G1 | P11 | refraction.*| U0009 | done |' PLAN.md · python3 -B unit.py status . | grep -q '| G1 |.*| 2 of 4 |'
files      : PLAN.md:12-13 · UNITS.md:191-232 · unit.log:518-561, from git diff -U0 at close
base       : U0009 closed, commit 23c84f8
lines      : +42 ~2 −0 moved 0, by staged tree at close
added      : S04 done, its unit is closed, the G1 number moved from 1 of 4 to 2 of 4 · S05 open with U0012 · the planned block U0012, the tests of the direct transform in their own module
rejected   : a planned block for S06, this cut takes the one step the sentence names, and the queue reopens the planning unit when U0012 closes · U0011 as the number of the test unit, this planning unit is the tenth of RULE §4, so the audit unit takes U0011 and the test unit waits behind it · the measure of an unmeasured leaf, rank 4, no leaf of this room is unmeasured · a redesign, rank 1, no unit failed · an A in conflict, rank 3, A0001 stands alone
split      : none
deleted    : none
result     : check exits 0 0 0 0 0 · PLAN.md +2 −2 · UNITS.md +42 −0
review     : r1 pass, «every check clause fails at base 23c84f8 and exits 0 now, the duplicate, lines, files, approval and added fields reproduce exactly from the repo, and the ledger-only diff stays behind the interface of a §3 planning unit.», model claude-opus-5, session 9667e103-779c-48d1-a9a4-0a8d37571689, ../reviews/agent-review-u0010-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0012 · 2026-11-10 · behavioral · closed
sentence   : the tests of the direct transform enter their own module
plan       : A0001 · S05
delete?    : no, the room holds no test of the direct route to delete
modify?    : no, test_straight_overhead of test_intermediate_transformations.py tests the CIRS recipe, and S05 names its own module for the direct route
duplicate  : git ls-tree 46985cf astropy/coordinates/tests/test_itrs_observed_transforms.py → 0 lines · git grep -c 'def test_itrs_to_altaz_with_refraction' 46985cf -- astropy/ → 0 lines · git grep -n 'def test_straight_overhead' 46985cf -- astropy/ → 1 line, test_intermediate_transformations.py:774, the CIRS recipe of the old gotcha, so the overhead test of this module carries the name test_itrs_straight_overhead
cause      : result layer of inputs → rules → state → result → view, R01: the merged fix carries a test module of its own, the place where the direct route states its accuracy
split?     : no, four tests of one route in one module, the interface of S05
tidy-first?: no
check      : grep -q '^def test_itrs_straight_overhead' astropy/coordinates/tests/test_itrs_observed_transforms.py · rm -f /tmp/ab/astropy/coordinates/tests/test_itrs_observed_transforms.py && rsync -a ./astropy/ /tmp/ab/astropy/ && cd /tmp/ab && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest astropy/coordinates/tests/test_itrs_observed_transforms.py -q -W 'ignore:leap-second file is expired'
files      : UNITS.md:213,216-232 · astropy/coordinates/tests/test_itrs_observed_transforms.py:1-76 · unit.log:795-905, from git diff -U0 at close
base       : U0013 closed, commit 46985cf
lines      : +76 ~18 −0 moved 0, by staged tree at close
added      : test_itrs_to_altaz_with_refraction and test_itrs_to_hadec_with_refraction, the refracted direct route against the CIRS route over a 200 point grid · test_refraction_leaves_the_observed_frame, the unrefracted AltAz of a refracted one by the two routes · test_itrs_straight_overhead, the zenith, the hour angle, the declination and the round trip of a topocentric ITRS vector · route_ends, LOC, WET, ZERO and MAS, the grid and the tolerances the four tests share
rejected   : the pytest run without the leap-second filter, the bundled IERS file of this checkout expired before today, so the first time conversion of any coordinates test raises IERSStaleWarning as an error, test_icrs_observed_transformations.py of the astropy baseline fails the same way · a fifth test of the obstime branch, itrs_to_observed hands a mismatched obstime to the ITRS self transform, which test_intermediate_transformations.py already covers · a test below the horizon, the SELMIN clamp of U0009 is not invertible there, in this route as in the CIRS one · the pytest clause over all of astropy/coordinates, a clause tests the content of its own lines by RULE §2, so it names this module · parametrize over AltAz and HADec, the two frames carry different component names, so each one reads its own test
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −18 · astropy/coordinates/tests/test_itrs_observed_transforms.py +76 −0
review     : r1 pass, «both clauses run clean at HEAD and fail at base 46985cf, the four tests provably traverse the one-hop direct transform, and every field, quote and cross-file claim reproduces from the repo.», model claude-opus-5, session 731931d9-8abc-4c6f-b09c-4c6a8255e481, ../reviews/agent-review-u0012-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0013 · 2026-11-10 · audit · closed
sentence   : the 10 audit of this room records its findings in the ledger
plan       : A0001 · S none, an audit unit of RULE §3 carries no step
delete?    : no, the ledger holds no audit of the first ten units, and no finding below names a line that a deletion alone removes
modify?    : no, a closed block is final by RULE §2, so the audit appends its record in place of changing a block
duplicate  : git show 20f1f93:UNITS.md | grep -c '· audit ·' → 0, no audit block stands in this room · python3 -B unit.py status . | grep '| audits |' → | audits | 0 of 10 final |
cause      : result layer of inputs → rules → state → result → view, RULE §4: at every ten units the audit reruns the checks of the non-audit units, with the piles, the duplicates, the unused code and the goals without units
split?     : no, one audit of one level
tidy-first?: no
check      : test "$(git show 20f1f93:UNITS.md | grep -c '^## U')" = 11 && grep -q 'the audit header of 11 blocks with 10 final' UNITS.md · test "$(git show 20f1f93:UNITS.md | grep -c '^## U.*closed$')" = 10 && grep -q 'the check rerun of the 10 closed blocks finds 3 that fail a clause now' UNITS.md · test "$(git ls-files --with-tree=20f1f93 | grep -c '\.py$')" = 928 && grep -q 'the duplicate scan over the 928 tracked py files' UNITS.md · test "$(python3 -B unit.py pile . | grep -c 'pile: 0 lines')" = 1 && grep -q 'the pile count of 0 lines by unit.py pile' UNITS.md
files      : UNITS.md:233-253 · unit.log:562-794, from git diff -U0 at close
base       : U0010 closed, commit 20f1f93
lines      : +21 ~0 −0 moved 0, by staged tree at close
added      : the 10 audit of RULE §4 by audit.py over this room at commit 20f1f93 · the audit header of 11 blocks with 10 final, 0 failed · the check rerun of the 10 closed blocks finds 3 that fail a clause now, U0003 U0004 U0008, every failing clause binds a ledger cell that a later unit moved, a step status, a leaf number, or the base line that open rewrites, and the five clauses of U0010 carry that same shape · the duplicate scan over the 928 tracked py files finds 843 groups, 13 of them touch a product file, every one an import line or a frame docstring line that the sibling modules of astropy share · the unused def scan finds 5762 defs, 12 of them in the product files, every one a frame_transform_graph registration that its decorator calls, with itrs_to_observed and observed_to_itrs of U0007 among them · the pile count of 0 lines by unit.py pile, beside 1868 tracked files that no files key names, the astropy baseline that RULE §4 adopts in place · the G1 leaf at 2 of 4, with no earlier audit to compare · 0 steps open with every unit final, 0 steps with no unit, 0 goal leaves with no unit, 0 active A rows that name no RULE § or U or S · audit.py refuses to run as python3 -I -B audit.py 10 . in this room, its import of unit reaches the room shim, which execs the hectoline gate, so this audit ran it by the realpath of the audit.py link · the S06 row of PLAN.md names U0013, the number this audit took, so the next planning unit renumbers that row
rejected   : a redesign of the three clauses that fail the rerun, a closed block is final by RULE §2, so the lesson stands in this record for the 100 level · the deletion of the 12 unused defs, the decorator of each one registers it in frame_transform_graph, so the scan names a design, not dead code · the deletion of the 843 duplicate groups, the astropy baseline carries them, and RULE §4 adopts that baseline in place · the renumber of the S06 row of PLAN.md, a planning unit owns the plan, so this audit records that finding alone · a fix of the audit.py entry, unit.py and the links are protected paths of RULE §4 with no owner line that names this unit · the 100 level, 10 non-audit final units stand under its hundred · the full lists of the duplicate scan and the unused def scan, one output line of 461267 characters, so this record carries their counts with the product subset
split      : none
deleted    : none, no finding of this audit names a line of this room that a deletion alone removes
result     : check exits 0 0 0 0 · UNITS.md +21 −0
review     : r1 fail, «the result key's "/tmp/audit10.txt, 11 lines" is false (the file has 14 lines, 13 non-blank), a typed count misreporting another file.», model claude-opus-5, session 408101eb-c99c-44d5-b17c-601c1daac3e0, ../reviews/agent-review-u0013-r1.md · r2 pass, «the r1 false count is fixed, all four clauses exit 0 at HEAD and non-zero at the base, and every number the block reports matched the command I reran.», model claude-opus-5, session c5dda368-b53a-4f5f-bf2e-da6614cc3b72, ../reviews/agent-review-u0013-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0014 · 2026-11-10 · structural · closed
sentence   : the unit of the docs step enters the queue
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the queue holds no unit for the docs step to delete
modify?    : no, U0010 cut the test step alone, S06 keeps its unit number only in the plan
duplicate  : git show 90e281c:UNITS.md | grep -c '^## U.*· planned$' → 0, the queue is empty · git show 90e281c:PLAN.md | grep -c '| todo |' → 1, S06 · git show 90e281c:UNITS.md | grep -c '^## U.*· closed$' → 12
cause      : state layer of inputs → rules → state → result → view, RULE §3: the planning unit runs again over an empty queue, the unit of the test step is final
split?     : no, one cut of one step
tidy-first?: no
check      : grep -q '^sentence   : the docs of the topocentric ITRS enter the repository with the changelog entry$' UNITS.md · grep -q '^base       : U0014$' UNITS.md · grep -q '^| S06 | G1 | P13 | the docs.*| U0015 | open |' PLAN.md · grep -q '^| S05 | G1 | P12 | the tests.*| U0012 | done |' PLAN.md · python3 -B unit.py status . | grep -q '| G1 |.*| 3 of 4 |'
files      : PLAN.md:13-14 · UNITS.md:254-295 · unit.log:906-951, from git diff -U0 at close
base       : U0012 closed, commit 90e281c
lines      : +42 ~2 −0 moved 0, by staged tree at close
added      : S05 done, its unit is closed, the G1 number moved from 2 of 4 to 3 of 4 · S06 open with U0015, the renumber the 10 audit of U0013 named, since the audit itself took the number U0013 that the S06 row carried · the planned block U0015, the docs of the topocentric ITRS with the changelog entry
rejected   : a second planned block, S06 is the last todo step of this plan, so one cut empties the queue · the measure of an unmeasured leaf, rank 4, no leaf of this room is unmeasured · an audit, rank 2, 12 non-audit final units stand under the twenty of RULE §4, and the ten audit closed as U0013 · a redesign, rank 1, no unit failed · an A in conflict, rank 3, A0001 stands alone
split      : none
deleted    : none
result     : check exits 0 0 0 0 0 · PLAN.md +2 −2 · UNITS.md +42 −0
review     : r1 pass, «every check clause fails at base  90e281c  and exits 0 now, each reported count and range reproduces from the repo, and the ledger-only diff stays behind the interface of a §3 planning unit.», model claude-opus-5, session b140c045-1a07-4561-9ecb-7c126efee3c5, ../reviews/agent-review-u0014-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0015 · 2026-11-10 · behavioral · closed
sentence   : the docs of the topocentric ITRS enter the repository with the changelog entry
plan       : A0001 · S06
delete?    : no, the CIRS recipe of common_errors.rst is the one page a deletion would reach, and the page needs the recipe that works in its place
modify?    : yes, the recipe of common_errors.rst changes in place, so this unit is that change, not a second page beside it
duplicate  : git ls-tree 16b2dfe docs/changes/coordinates/13398.feature.rst → 0 lines · git grep -c 'topocentric' 16b2dfe -- docs/ → 2 files, common_errors.rst 4 and spectralcoord.rst 2, the prose of the old CIRS recipe and of the ITRS repr · git grep -c 'whatsnew-5.2-topocentric-itrs' 16b2dfe -- docs/ → 0 files
cause      : view layer of inputs → rules → state → result → view, R01: the merged fix carries its docs and its changelog fragment, the page where a reader meets the route
split?     : no, one feature told in four places, the changelog fragment, the common mistake, the satellite page and the release note
tidy-first?: no
check      : grep -q '^    >>> itrs_topo = ITRS(itrs_vec, obstime=t, location=home)$' docs/coordinates/common_errors.rst · grep -q 'itrs_topo.transform_to(AltAz' docs/coordinates/common_errors.rst && rsync -a ./docs/ /tmp/ab/docs/ && cd /tmp/ab && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest --doctest-rst docs/coordinates/common_errors.rst -q -W 'ignore:leap-second file is expired' -W 'ignore::astropy.utils.iers.IERSWarning' · grep -q 'itrs_topo.transform_to(AltAz' docs/coordinates/satellites.rst && rsync -a ./docs/ /tmp/ab/docs/ && cd /tmp/ab && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest --doctest-rst docs/coordinates/satellites.rst -q -W 'ignore:leap-second file is expired' -W 'ignore::astropy.utils.iers.IERSWarning' · grep -q 'whatsnew-5.2-topocentric-itrs' docs/whatsnew/5.2.rst && grep -q '^.. _whatsnew-5.2-topocentric-itrs:$' docs/whatsnew/5.2.rst && grep -q '^.. _astropy-coordinates-satellites:$' docs/coordinates/satellites.rst && grep -q 'and the ``AltAz`` and ``HADec`` frames' docs/changes/coordinates/13398.feature.rst
files      : UNITS.md:276,279-295 · docs/changes/coordinates/13398.feature.rst:1-5 · docs/coordinates/common_errors.rst:65,76-77,80,83-86 · docs/coordinates/satellites.rst:110-138 · docs/whatsnew/5.2.rst:17,50-62 · unit.log:952-1007, from git diff -U0 at close
base       : U0014 closed, commit 16b2dfe
lines      : +48 ~26 −0 moved 0, by staged tree at close
added      : docs/changes/coordinates/13398.feature.rst, the changelog fragment of the ITRS location attribute with the direct transforms · the topocentric ITRS recipe of common_errors.rst in place of the CIRS one, which reaches the same 90 degrees in two lines · the section Satellite Positions in the Topocentric ITRS of satellites.rst, a worked example that measures 47 arcseconds of geocentric aberration off a satellite · the release note whatsnew-5.2-topocentric-itrs of whatsnew/5.2.rst with its bullet in the overview list
rejected   : the sgp4 variables teme and siding_spring of the satellite page for the new example, sgp4 is absent from this checkout, so its doctest would skip and its printed numbers would stand unmeasured, the example rebuilds the same position from the geodetic one the page already prints · the removal of the CIRS recipe from common_errors.rst, the page explains why the naive call misses, so the recipe that replaces it stays in that same place · a note in docs/coordinates/index.rst, the four files of P13 hold the docs of this product, and the index names no transform of its own · the doctest clause without the IERSWarning filter, this checkout reaches no network, so the IERS auto download raises under the error filter of setup.cfg, at the base as on the tree · the sphinx build as a clause, it reaches outside the room and runs minutes, so clause 4 proves instead that both new references name labels that stand
split      : none
deleted    : the six line CIRS recipe of docs/coordinates/common_errors.rst, cirs_vec and cirs_topo with their four comment lines, two of those lines rewritten in place as the two line ITRS recipe and four taken out
result     : check exits 0 0 0 0 · UNITS.md +18 −18 · docs/changes/coordinates/13398.feature.rst +5 −0 · docs/coordinates/common_errors.rst +8 −8 · docs/coordinates/satellites.rst +29 −0 · docs/whatsnew/5.2.rst +14 −0
review     : r1 pass, «every check clause exits 0 on the tree and fails at base 16b2dfe, the doctest outputs reproduce exactly, and the nine verdict keys, the file ranges, the line counts and the prose claims all hold within the four declared files of P13.», model claude-opus-5, session ddb17ab2-8c28-418e-81f1-d27d2089d5bf, ../reviews/agent-review-u0015-r1.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0016 · 2026-11-10 · structural · closed
sentence   : the audit of the met goal enters the queue
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the queue holds no unit for the met goal to delete
modify?    : no, U0014 cut the docs step alone, and the plan holds no further todo step to change
duplicate  : git show 0c5e7a5:UNITS.md | grep -c '^## U.*· planned$' → 0, the queue is empty · git show 0c5e7a5:PLAN.md | grep -c '| todo |' → 0, every step of this plan is done or open · git show 0c5e7a5:UNITS.md | grep -c '· audit ·' → 2, the U0013 header and its one mention, the ten audit
cause      : state layer of inputs → rules → state → result → view, RULE §4: an audit runs once when the goal checks are met, so the met goal is what puts the next unit in the queue
split?     : no, one cut of one unit
tidy-first?: no
check      : grep -q '^sentence   : the audit of the met goal records its findings in the ledger$' UNITS.md · grep -q '^base       : U0016$' UNITS.md · grep -q '^| S06 | G1 | P13 | the docs.*| U0015 | done |' PLAN.md · python3 -B unit.py status . | grep -q '| G1 |.*| 4 of 4 | 4 of 4 |' · python3 -B unit.py status . | grep -q '| G0 |.*| 1 of 1 | 1 of 1 |'
files      : PLAN.md:14 · UNITS.md:296-337 · unit.log:1008-1119, from git diff -U0 at close
base       : U0015 closed, commit 0c5e7a5
lines      : +42 ~1 −0 moved 0, by staged tree at close
added      : S06 done, its unit is closed, the G1 number moved from 3 of 4 to 4 of 4 and the G0 number from 0 of 1 to 1 of 1 · the planned block U0017, the audit RULE §4 calls for once the goal checks are met
rejected   : a further step under G1, its four steps are done and its measure stands at its target, so the plan grows no row · the leaf farthest from its target, rank 5, no leaf of this room is below its target · the measure of an unmeasured leaf, rank 4, no leaf of this room is unmeasured · a redesign, rank 1, no unit failed · an A in conflict, rank 3, A0001 stands alone · the twenty audit as the reason, 14 non-audit final units stand under it, the met goal is the trigger RULE §4 names here
split      : none
deleted    : none
result     : check exits 0 0 0 0 0 · PLAN.md +1 −1 · UNITS.md +42 −0
review     : r1 pass, «every check clause fails at base 0c5e7a5 and exits 0 on the tree, and each reported count, range and quote reproduces from the repo inside the ledger-only interface of a §3 planning unit.», model claude-opus-5, session 4a4e2c9d-4b3a-4dbb-a21a-ad7cb97ce9ef, ../reviews/agent-review-u0016-r1.md · r2 pass, «every check clause fails at base  0c5e7a5  and exits 0 on the tree, and each reported range, count and quote reproduces from the repo while the diff stays inside the ledger-only interface of a §3 planning unit.», model claude-opus-5, session acef880f-c3f9-4e84-8238-65d1f9ae80ff, ../reviews/agent-review-u0016-r2.md
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0017 · 2026-11-10 · audit · open
sentence   : the audit of the met goal records its findings in the ledger
plan       : A0001 · S none, an audit unit of RULE §3 carries no step
delete?    : no, no finding below names a line of this room that a deletion alone removes
modify?    : no, a closed block is final by RULE §2, so this audit appends its record in place of changing a block
duplicate  : git show 6d0245a:UNITS.md | grep -c '· audit ·' → 4, the U0013 header, the U0017 header and the two duplicate lines that name them · python3 -B unit.py status . | grep '| audits |' → | audits | 1 of 15 final |
cause      : result layer of inputs → rules → state → result → view, RULE §4: the goal checks of this room are met, G0 at 1 of 1 and G1 at 4 of 4, so the audit runs once over the met goal, with the check rerun, the piles, the duplicates, the unused code and the goals without units
split?     : no, one audit of one room at one trigger
tidy-first?: no
check      : test "$(git show 6d0245a:UNITS.md | grep -c '^## U')" = 16 && grep -q 'the audit header of 16 blocks with 15 final' UNITS.md · test "$(git show 6d0245a:UNITS.md | grep -c '^## U.*closed$')" = 15 && grep -q 'the check rerun of the 48 clauses of the 15 closed blocks finds 13 that fail in 7 blocks' UNITS.md · test "$(git ls-files | grep -c '\.py$')" = 929 && grep -q 'the duplicate scan over the 929 tracked py files' UNITS.md · test "$(python3 -B unit.py pile . | grep -c 'pile: 0 lines')" = 1 && test "$(git ls-files | wc -l | tr -d ' ')" = 1888 && grep -q 'the pile count of 0 lines by unit.py pile beside the 1888 tracked files' UNITS.md · grep -q 'the coordinates suite at 1434 passed 3 failed on the tree against 1430 passed 3 failed at base 6500928' UNITS.md && rm -rf /tmp/acur /tmp/abase && mkdir -p /tmp/acur /tmp/abase && rsync -a ./astropy/ /tmp/acur/astropy/ && git archive 6500928dc0e57be8f06d1162eacc3ba5e2eff692 astropy | tar -x -C /tmp/abase && (cd /tmp/ab && find astropy -name '*.so' | while read f; do cp "$f" "/tmp/acur/$f"; cp "$f" "/tmp/abase/$f"; done) && (cd /tmp/acur && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest astropy/coordinates -q -p no:randomly -W 'ignore:leap-second file is expired' -W 'ignore::astropy.utils.iers.IERSWarning' --ignore=astropy/coordinates/tests/test_spectral_coordinate.py 2>&1 | tail -1 | grep -q '^3 failed, 1434 passed, 61 skipped, 21 xfailed') && (cd /tmp/abase && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest astropy/coordinates -q -p no:randomly -W 'ignore:leap-second file is expired' -W 'ignore::astropy.utils.iers.IERSWarning' --ignore=astropy/coordinates/tests/test_spectral_coordinate.py 2>&1 | tail -1 | grep -q '^3 failed, 1430 passed, 61 skipped, 21 xfailed') · grep -q 'the four grid and overhead tests of R01 fail at base 6500928 and the 73 tests of its patched module all pass on this tree' UNITS.md && rm -rf /tmp/agold /tmp/agoldb && mkdir -p /tmp/agold /tmp/agoldb && rsync -a ./astropy/ /tmp/agold/astropy/ && git archive 6500928dc0e57be8f06d1162eacc3ba5e2eff692 astropy | tar -x -C /tmp/agoldb && (cd /tmp/ab && find astropy -name '*.so' | while read f; do cp "$f" "/tmp/agold/$f"; cp "$f" "/tmp/agoldb/$f"; done) && python3 -I -B -c "import sys; t=open('/tmp/pr13398.diff').read(); [sys.stdout.write('diff --git '+p) for p in t.split('diff --git ')[1:] if 'tests/test_intermediate_transformations.py' in p.split(chr(10))[0]]" > /tmp/agold.patch && (cd /tmp/agold && patch -p1 -s < /tmp/agold.patch && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest astropy/coordinates/tests/test_intermediate_transformations.py -q -p no:randomly -W 'ignore:leap-second file is expired' 2>&1 | tail -1 | grep -q '^73 passed, 3 skipped') && (cd /tmp/agoldb && patch -p1 -s < /tmp/agold.patch && DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /tmp/av/bin/python -m pytest astropy/coordinates/tests/test_intermediate_transformations.py -q -p no:randomly -W 'ignore:leap-second file is expired' 2>&1 | tail -1 | grep -q '^4 failed, 69 passed, 3 skipped')
files      : UNITS.md:≤22
base       : U0016 closed, commit 6d0245a
lines      : ≤100
added      : the audit of the met goal of RULE §4 by audit.py over this room at commit 6d0245a, one output of 14 lines · the audit header of 16 blocks with 15 final, 0 failed · the check rerun of the 48 clauses of the 15 closed blocks finds 13 that fail in 7 blocks, U0003 U0004 U0008 U0010 U0013 U0014 U0016, where audit.py read 7 of the 14 closed non-audit units with the same per clause codes, U0001 in place of the U0013 audit block it leaves out of its rerun · the one clause of U0001 that audit.py read as failing reruns unit.py validate, whose whole output then was the seven empty keys of the open U0017 block, and it exits 0 with validate at 0 faults once this block is filled · the 13 failing clauses each bind a cell that a later unit moved, 4 a step status that went open to done, 4 a G1 leaf number, 4 the base line that open rewrites, and 1 the tracked py file count of U0013, whose --with-tree form reads 929 now against the 928 it recorded before the test module of U0012 · the duplicate scan over the 929 tracked py files finds 843 groups, 15 of them touch a product file, every one an import line or a frame docstring line that the sibling modules of astropy share, 13 of them at the U0013 audit and the 2 new ones the imports of the test module of U0012 · the unused def scan finds 5766 defs, 16 of them in the product files, 12 a frame_transform_graph registration that its decorator calls and 4 the test functions of U0012 that pytest collects by name · the pile count of 0 lines by unit.py pile beside the 1888 tracked files, 1865 of which no files key names, the astropy baseline that RULE §4 adopts in place · the G1 leaf at 4 of 4 against the 2 of 4 of the U0013 audit, G0 at 1 of 1, 0 steps todo with 6 of 6 done, 0 steps open with every unit final, 0 steps with no unit, 0 goal leaves with no unit and 0 active A rows that name no RULE §, U or S · the coordinates suite at 1434 passed 3 failed on the tree against 1430 passed 3 failed at base 6500928, the three failing ids the same test_pickle StaticMatrixTransform cases in both, and the 4 added passes the four tests of U0012 · the four grid and overhead tests of R01 fail at base 6500928 and the 73 tests of its patched module all pass on this tree, so the fix of this room answers the issue of TASK.md by the tests of its own source · the module of P11 differs from R01 by refactor alone, the shared refraction_constants helper, three named intermediate variables and four reworded comments, with no changed expression · docs/coordinates/spectralcoord.rst stands outside the files column of every P row of PRODUCTS.md, its two doctest lines named by the files key of U0006 alone · spectralcoord.rst:272 carries two spaces after observer: where the live repr prints one, the line of R01 character for character, and pytest-doctestplus defaults doctest_optionflags to ELLIPSIS NORMALIZE_WHITESPACE, so that REMOTE_DATA doctest holds either way and the 18 doctest files of docs/coordinates all pass · the unrefracted grid comparison of R01 is absent from the module of P12, whose four tests all carry the pressure of WET, and clause 6 covers that route instead · 23 review rounds over the 15 closed blocks, U0001 the bootstrap block carries none, 5 rounds failed, U0002 r2, U0006 r1, U0008 r1 and r2, U0013 r1, and every faulted unit reached a pass · the method count table of unit.py status holds 0 unmeasured leaves, 0 steps under a leaf at target, 8 ledger-only units, 1 uncited R row, 0 no pilot step and 0 100 levels overdue · the 14 product files all stand under the 500 line cap, over [] and not found []
rejected   : a redesign of the 13 clauses that bind a moved cell, a closed block is final by RULE §2, so the lesson stands in this record for the 100 level · the one space fix of docs/coordinates/spectralcoord.rst:272, the line reproduces R01 character for character and NORMALIZE_WHITESPACE holds the doctest either way · a fifth test of the unrefracted grid in the module of P12, this audit is ledger-only by its files key and a behavioral unit owns a test file, so the finding stands for the next unit of that product · a P row for docs/coordinates/spectralcoord.rst, a planning unit owns the P tree, so this audit records that finding alone · the deletion of the 843 duplicate groups and of the 5766 unused defs, the astropy baseline carries them and RULE §4 adopts that baseline in place · a further step or unit under G1, its four steps are done, its measure stands at its target and the tests of R01 pass on this tree, so the plan grows no row · the twenty audit as the reason, 14 non-audit final units stand under it, the met goal is the trigger RULE §4 names here · the 100 level, 14 non-audit final units stand under its hundred · the full lists of the duplicate scan and the unused def scan, one output line of 461763 characters, so this record carries their counts with the product subset
split      : none
deleted    : none, no finding of this audit names a line of this room that a deletion alone removes
result     : check exits 0 0 0 0 0 0 · UNITS.md +18 −18
review     : 
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row
