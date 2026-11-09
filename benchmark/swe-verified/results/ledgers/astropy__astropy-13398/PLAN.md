# PLAN — 01_task · steps

One S row per step, RULE §2. A step makes or changes one product. The interface stands before the first unit of the step opens. Status: todo, open, done. Done ÷ all is the work count. Rows from S02 on name the leaf they move.

## rule 1.1 from S02

| S | parent | product | step | interface: exposes · hides | units | status |
|---|---|---|---|---|---|---|
| S01 | G0 | the six ledgers | this room with its ledgers, links and bootstrap block | the ledger files · the links | U0001 | done |
| S02 | G1 | P11 | the measure step of this room: accept.py runs the four acceptance checks of GOAL.md, measures.py counts them, G1 0 of 4 → 1 of 4, leaf G1 moves from 0 of 4 to 1 of 4 | exposes g1 of this room to unit.py status, G1 0 of 4 → 1 of 4 · hides the room venv, the sandbox of the worker | U0003 | todo |
| S03 | G1 | P10 | the pilot, one direct ITRS to Observed path end to end, G1 1 of 4 → 3 of 4, leaf G1 moves from 1 of 4 to 3 of 4, an ITRS position near the observer reaches AltAz, HADec, each way | exposes ITRS to AltAz, ITRS to HADec, each way, in the frame graph, G1 1 of 4 → 3 of 4 · hides the rotation matrices, the subtraction of the observer position | U0004 | todo |
| S04 | G1 | P10 | refraction inside the direct path, G1 3 of 4 → 4 of 4, leaf G1 moves from 3 of 4 to 4 of 4, the observed frame that carries pressure bends the elevation | exposes the two frame pairs under pressure, G1 3 of 4 → 4 of 4 · hides the erfa refraction constants, the A tan z model | U0005 | todo |
