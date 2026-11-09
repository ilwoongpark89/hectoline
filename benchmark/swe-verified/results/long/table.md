# SWE-bench Verified under hectoline — results

Every cell is a count over runs.jsonl and the report.json files of the official grader. «graded» counts the runs the grader reported on.

| arm | runs | graded | resolved | claimed | claimed & resolved | claimed & not | not claimed & resolved | not claimed & not | false claims / claimed |
|---|---|---|---|---|---|---|---|---|---|
| plain | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| hectoline | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 / 0 |

## Per run

| instance | arm | resolved | claimed | patch lines | patch files | turns | wall, s | timed out | units closed | units failed | audits | review rounds pass / fail | hook denies |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| astropy__astropy-13398 | hectoline | yes | none | 567 | 11 | 151 | 21106.3 | True | 13 | 0 | 1 | 0 / 0 | 20 |

## Sentence

On 0 SWE-bench Verified tasks the plain agent claimed 0 fixes and the hidden tests confirmed 0. Under the unit method it claimed 0 and the tests confirmed 1.
