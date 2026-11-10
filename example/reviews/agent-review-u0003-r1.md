# U0003 r1 — the planning unit: G1 reads 1, so the pilot step S03 names calc.py with its two units, then the first audit

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: grep -qE '^## U0006 . [0-9-]+ . audit . ' UNITS.md · grep -q '| U0004 U0005 | todo |$' PLAN.md · grep -q '^| S01 | G0 | P01, ' PLAN.md · grep -q '^| P11 | the calculator |' PRODUCTS.md
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4

R1 PASS
