# SWE-bench Verified under hectoline — results

Every cell is a count over runs.jsonl and the report.json files of the official grader. «graded» counts the runs the grader reported on.

| arm | runs | graded | resolved | claimed | claimed & resolved | claimed & not | not claimed & resolved | not claimed & not | false claims / claimed |
|---|---|---|---|---|---|---|---|---|---|
| plain | 10 | 10 | 7 | 9 | 7 | 2 | 0 | 1 | 2 / 9 |
| hectoline | 10 | 10 | 1 | 0 | 0 | 0 | 1 | 9 | 0 / 0 |

## Per run

| instance | arm | resolved | claimed | patch lines | patch files | turns | wall, s | timed out | units closed | units failed | audits | review rounds pass / fail | hook denies |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| astropy__astropy-13398 | hectoline | no | none | 148 | 2 | None | 4205.2 | True | 1 | 0 | 0 | 7 / 0 | 26 |
| astropy__astropy-13398 | plain | yes | yes | 713 | 10 | 77 | 991.8 | False | — | — | — | — | — |
| astropy__astropy-14369 | hectoline | no | none | 55 | 1 | 151 | 3311.1 | False | 1 | 0 | 0 | 5 / 1 | 13 |
| astropy__astropy-14369 | plain | no | yes | 171 | 5 | 77 | 785.1 | False | — | — | — | — | — |
| django__django-11885 | hectoline | no | no | 0 | 0 | 125 | 1927.7 | False | 0 | 0 | 0 | 0 / 0 | 109 |
| django__django-11885 | plain | yes | yes | 235 | 6 | 73 | 850.5 | False | — | — | — | — | — |
| django__django-16263 | hectoline | no | none | 256 | 5 | None | 3600.9 | True | 3 | 0 | 0 | 0 / 0 | 91 |
| django__django-16263 | plain | no | yes | 306 | 5 | 76 | 1025.5 | False | — | — | — | — | — |
| django__django-16560 | hectoline | no | no | 0 | 0 | 146 | 1954.5 | False | 0 | 0 | 0 | 0 / 1 | 50 |
| django__django-16560 | plain | yes | yes | 565 | 6 | 49 | 291.2 | False | — | — | — | — | — |
| pydata__xarray-3993 | hectoline | yes | none | 119 | 4 | 151 | 3022.1 | False | 4 | 1 | 0 | 5 / 4 | 13 |
| pydata__xarray-3993 | plain | yes | yes | 124 | 4 | 34 | 207.6 | False | — | — | — | — | — |
| pylint-dev__pylint-4551 | hectoline | no | none | 0 | 0 | 151 | 3542.5 | False | 0 | 2 | 0 | 0 / 6 | 102 |
| pylint-dev__pylint-4551 | plain | yes | yes | 312 | 7 | 37 | 209.4 | False | — | — | — | — | — |
| sphinx-doc__sphinx-8548 | hectoline | no | none | 53 | 1 | 151 | 3047.9 | False | 2 | 0 | 0 | 4 / 2 | 7 |
| sphinx-doc__sphinx-8548 | plain | yes | yes | 557 | 7 | 122 | 1434.1 | False | — | — | — | — | — |
| sphinx-doc__sphinx-9461 | hectoline | no | none | 0 | 0 | 151 | 3301.7 | False | 0 | 1 | 0 | 2 / 5 | 29 |
| sphinx-doc__sphinx-9461 | plain | yes | yes | 309 | 9 | 90 | 978.2 | False | — | — | — | — | — |
| sympy__sympy-16597 | hectoline | no | none | 44 | 2 | None | 3600.6 | True | 3 | 0 | 0 | 4 / 3 | 33 |
| sympy__sympy-16597 | plain | no | none | 9933 | 12 | None | 3600.6 | True | — | — | — | — | — |

## Sentence

On 10 SWE-bench Verified tasks the plain agent claimed 9 fixes and the hidden tests confirmed 7. Under the unit method it claimed 0 and the tests confirmed 1.
