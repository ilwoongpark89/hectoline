# GOAL — 01_task

## Question
Owner, 2026-11-09: «Fix the issue in TASK.md in this repository».

## Stance
the issue in TASK.md is fixed in this repository. This room follows RULE.md of hectoline by its link.

## Audience
The owner. The terminal of this room. The 00 session that watches it.

## Goals
Progress = leaves at target ÷ leaves, RULE §5. Done steps ÷ all steps is the work count. Each goal leaf has one measure in this room's measures.py.

| G | goal | parent | measure | target | baseline |
|---|---|---|---|---|---|
| G0 | the issue in TASK.md is fixed in this repository | — | leaves at target | 1 of 1 | 0 of 1 |
| G1 | a subclass shows the instance attributes it inherits, each with the docstring its base class carries | G0 | the acceptance checks of G1 that hold, g1 of measures.py | 2 of 2 | 0 of 2 |

G1 carries two acceptance checks, one point each, baseline 0 of 2 at commit 53a25bb. The first: get_class_members of autodoc reads one module analyzer per class of the mro, so the attribute docstrings of a base class reach the subclass. The second: the autoclass suite holds two regression cases over a fixture whose subclass inherits an instance attribute.

## Layers and flow
inputs → rules → state → result → view. Rules: RULE.md of hectoline by its link. State: the six ledgers and the log.
