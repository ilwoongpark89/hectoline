# SWE-bench Verified under hectoline — results

Every cell is a count over runs.jsonl and the report.json files of the official grader. «graded» counts the runs the grader reported on.

| arm | runs | graded | resolved | claimed | claimed & resolved | claimed & not | not claimed & resolved | not claimed & not | false claims / claimed |
|---|---|---|---|---|---|---|---|---|---|
| plain | 3 | 3 | 2 | 3 | 2 | 1 | 0 | 0 | 1 / 3 |
| hectoline | 3 | 3 | 1 | 2 | 1 | 1 | 0 | 1 | 1 / 2 |

## Per run

| instance | arm | resolved | claimed | patch lines | patch files | turns | wall, s | timed out | units closed | units failed | audits | review rounds pass / fail | hook denies |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| astropy__astropy-14369 | hectoline | yes | yes | 145 | 3 | 134 | 3394.6 | False | 3 | 0 | 0 | 3 / 0 | 2 |
| astropy__astropy-14369 | plain | yes | yes | 164 | 5 | 61 | 943.7 | False | — | — | — | — | — |
| django__django-16263 | hectoline | no | yes | 314 | 5 | 37 | 14404.2 | True | 7 | 0 | 0 | 9 / 3 | 9 |
| django__django-16263 | plain | yes | yes | 285 | 5 | 49 | 486.9 | False | — | — | — | — | — |
| sympy__sympy-16597 | hectoline | no | none | 153 | 3 | None | 21605.8 | True | 7 | 0 | 0 | 9 / 4 | 7 |
| sympy__sympy-16597 | plain | no | yes | 946 | 9 | 16 | 21605.4 | True | — | — | — | — | — |

## Sentence

On 3 SWE-bench Verified tasks the plain agent claimed 3 fixes and the hidden tests confirmed 2. Under the unit method it claimed 2 and the tests confirmed 1.
