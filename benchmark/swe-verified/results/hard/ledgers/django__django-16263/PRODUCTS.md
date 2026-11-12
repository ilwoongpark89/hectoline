# PRODUCTS — 01_task · the P tree

One P row per product, RULE §0. Hand columns: name, parent, layer, files, uses.

| P | name | parent | layer | files | uses |
|---|---|---|---|---|---|
| P01 | ledgers, the state of the room | — | folder | the six ledger files | — |
| P02 | the unit ledger | P01 | state | UNITS.md | — |
| P03 | the owner statements of this room | P01 | state | OWNER.md | — |
| P04 | the plan | P01 | state | PLAN.md | P05 |
| P05 | the goal page | P01 | inputs | GOAL.md | — |
| P06 | this product tree | P01 | state | PRODUCTS.md | — |
| P07 | the research claims | P01 | state | RESEARCH.md | — |
| P08 | the rule, the hectoline file by link | — | rules | RULE.md | — |
| P09 | the gate, the measures and the audit, hectoline files by links | — | result | unit.py, measure.py, audit.py | P02 P08 |
| P10 | the measure of this room | — | result | measures.py | P05 |
| P11 | the summary query of django, which annotations a count or an aggregate carries | — | rules | django/db/models/sql/query.py | P13 |
| P12 | the acceptance tests of the issue of TASK.md | — | view | tests/aggregation/tests.py | P11 |
| P13 | the refs of an expression, the annotation names it names | — | rules | django/db/models/expressions.py, django/db/models/sql/where.py | — |

P11, P12 and P13 are files of the django project this room adopts in place, RULE §4. Their line counts are the recorded baseline, not lines this room wrote, so the composition reads them over the 500 cap from the first unit. A0001 asks for the fix of TASK.md, no split of django's modules, and no unit of this room may rest on that size.
