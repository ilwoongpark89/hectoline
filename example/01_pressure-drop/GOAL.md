# GOAL — 01_pressure-drop

## Question
Owner, 2026-11-11: «Build a laminar pipe pressure-drop calculator that reproduces the reference case».

## Stance
a laminar pipe pressure-drop calculator answers its reference case within 1 percent. This room follows RULE.md of hectoline by its link.

## Audience
The owner. The terminal of this room. The 00 session that watches it.

## Goals
Progress = leaves at target ÷ leaves, RULE §5. Done steps ÷ all steps is the work count. Each goal leaf has one measure in this room's measures.py.

| G | goal | parent | measure | target | baseline |
|---|---|---|---|---|---|
| G0 | a laminar pipe pressure-drop calculator answers its reference case within 1 percent | — | leaves at target | 1 of 1 | 0 of 1 |
| G1 | the calculator answers the reference case within 1 percent | G0 | reference cases that calc.py misses by over 1 percent, by measures.py g1 | 0 | no tool |

## Layers and flow
inputs → rules → state → result → view. Rules: RULE.md of hectoline by its link. State: the six ledgers and the log.
