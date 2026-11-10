# U0004 r1 — calc.py holds the laminar pressure drop of a pipe as one function

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: test "$(python3 -B -c "import sys; sys.path.insert(0, '.'); import calc; print(round(calc.pressure_drop(1.0e-3, 2, 0.01, 1e-5), 3))")" = "81.487"
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4

R1 PASS
