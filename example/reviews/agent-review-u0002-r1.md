# U0002 r1 — measures.py computes the count of G1

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: test "$(python3 -I -B measures.py g1)" = "g1 1" · grep -q "^| S02 | .* | U0002 | done |$" PLAN.md
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4

R1 PASS
