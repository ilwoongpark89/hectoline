# SWE-bench Verified under hectoline — results

Every cell is a count over runs.jsonl and the report.json files of the official grader. «graded» counts the runs the grader reported on.

| arm | runs | graded | resolved | claimed | claimed & resolved | claimed & not | not claimed & resolved | not claimed & not | false claims / claimed |
|---|---|---|---|---|---|---|---|---|---|
| plain | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 / 0 |
| hectoline | 2 | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 / 0 |

## Per run

| instance | arm | resolved | claimed | patch lines | patch files | turns | wall, s | timed out | units closed | units failed | audits | review rounds pass / fail | hook denies |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| django__django-11885 | hectoline | yes | none | 224 | 4 | None | 3601.2 | True | 4 | 0 | 0 | 4 / 0 | 1 |
| scikit-learn__scikit-learn-25102 | hectoline | yes | none | 172 | 3 | None | 3601.3 | True | 2 | 0 | 0 | 3 / 1 | 2 |
| scikit-learn__scikit-learn-25102 | plain | yes | none | 181 | 4 | None | 3601.0 | True | — | — | — | — | — |

## Sentence

On 1 SWE-bench Verified tasks the plain agent claimed 0 fixes and the hidden tests confirmed 1. Under the unit method it claimed 0 and the tests confirmed 2.
