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
| G1 | the two MRT unit strings of TASK.md parse to the units they name | G0 | g1 of measures.py, unit strings parsed as named | 2 of 2 | 0 of 2 |

The two strings stand in the byte-by-byte block of TASK.md. g1 counts the strings whose parsed unit equals the unit the string names: `10+3J/m/s/kpc2` names `1000 J / (kpc2 m s)`, `10-7J/s/kpc2` names `1e-07 J / (kpc2 s)`. At ddd56a5 the CDS grammar reads a chain of slashes right to left, it returns `1000 J s / (kpc2 m)` for the first string, so the baseline is 0 of 2.

The interpreter is .venv/bin/python of this room, gitignored, made by `python3 -m venv .venv`, then pip numpy 1.26.4 pyerfa PyYAML packaging cython extension-helpers setuptools 68.2.2, then `SETUPTOOLS_USE_DISTUTILS=local .venv/bin/python setup.py build_ext --inplace`.

## Layers and flow
inputs → rules → state → result → view. Rules: RULE.md of hectoline by its link. State: the six ledgers and the log.
