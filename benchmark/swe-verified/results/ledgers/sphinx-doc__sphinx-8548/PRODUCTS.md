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
| P10 | the class member collection of autodoc | — | rules | sphinx/ext/autodoc/importer.py | — |
| P11 | the autoclass regression cases of the class member collection | — | result | tests/test_ext_autodoc_autoclass.py, tests/roots/test-ext-autodoc/target/instance_variable.py | P10 |
| P12 | the leaf numbers of this room | — | view | measures.py | P10 P11 |
