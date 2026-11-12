# PLAN — 01_task · steps

One S row per step, RULE §2. A step makes or changes one product. The interface stands before the first unit of the step opens. Status: todo, open, done. Done ÷ all is the work count. Rows from S02 on name the leaf they move.

## rule 1.1 from S02

| S | parent | product | step | interface: exposes · hides | units | status |
|---|---|---|---|---|---|---|
| S01 | G0 | the six ledgers | this room with its ledgers, links and bootstrap block | the ledger files · the links | U0001 | done |
| S02 | G1 | P10 | the measure tool of this room, G1 from no tool to its first number | the count of G1 · the probe commands | U0002 | done |
| S03 | G1 | P12 | the five acceptance tests of TASK.md enter tests/aggregation/tests.py, three red over the annotations it names, two guards the base already passes, G1 from 0 of 5 to 2 of 5 | the SQL a count query may carry · the models of the suite | U0004 | done |
| S04 | G1 | P13 | `get_refs` reads the annotation names a resolved expression refers to, no behavior change, G1 from 2 of 5 to 2 of 5 | the refs of an expression · the walk over its source expressions | U0005 | done |
| S05 | G1 | P11 | the pilot, one count query end to end with only the annotations its aggregates or its group by reference, G1 from 2 of 5 to 5 of 5 | the annotations a summary query carries · the mask with the subquery | U0006 | done |
| S06 | G1 | P11 | an aggregate that refers to a window or to a subquery annotation keeps its subquery, the fault U0006 left behind, A0001 asks for the fix of TASK.md and this row carries it, G1 from 5 of 5 to 5 of 5 | the test that asks a summary query for its subquery · the refs of its aggregates | U0008 | done |

## Order
The order of the waiting work, RULE §2. A new finding or an owner line redraws it. The open unit rewrites it in place.

1. The audit of RULE §4, due once the goal checks are met, RULE §2 stands it first. It reruns the clauses of U0002 to U0008 on a copy of the room and lists the piles, the duplicates and the structure counts against no previous audit.

U0004 under S03 closed with its three red cases, two of the five stand green at the base as guards of the grouping a prune must keep. U0005 under S04 closed with `get_refs` on the base expression, on a ref, on a where node. U0006 under S05 closed with the mask of `get_aggregation`, G1 5 of 5 and its leaf at target. U0007 cut S06 from the fault that mask left, and U0008 under S06 closed with the two terms of the wrapping test, so no step waits under G1.
