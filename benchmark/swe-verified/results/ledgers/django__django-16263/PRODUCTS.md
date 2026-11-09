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
| P10 | the measures of this room, one per goal leaf | P01 | inputs | measures.py | P05 |
