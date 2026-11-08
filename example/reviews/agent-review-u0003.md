# agent-review-u0003 — measures.py computes g1, the reference cases the calculator misses

Reviewer: the same session that built the room through example/build.py. This log shows the form of a review. It is not an independent review.

- check: test "$(python3 -I -B measures.py g1)" = "g1 1" · grep -q "^| S02 | .* | U0003 | done |$" PLAN.md
- read: the diff of the files key, the nine verdict keys, RULE §1 §2 §4
- verdict: pass r1
