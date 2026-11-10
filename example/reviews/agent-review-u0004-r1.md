# U0004 r1 — calc.py prints the laminar pressure drop of a pipe from four inputs

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: test "$(python3 -I -B measures.py g1)" = "g1 0" · test "$(python3 -I -B calc.py 1.0e-3 2 0.01 1e-5)" = "81.487" · grep -q "^| S03 | .* | U0004 | done |$" PLAN.md
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4

R1 PASS
