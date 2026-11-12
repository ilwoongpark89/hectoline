# UNITS — 01_task

## U0001 · 2026-11-12 · structural · closed
sentence   : the room exists with its ledgers, its links, this block
plan       : A0001 · S01
delete?    : no, a new folder
modify?    : no, a new folder
duplicate  : the folder did not exist, room.py made it
cause      : state layer of inputs → rules → state → result → view, RULE §0: a numbered folder with the six ledgers and a link to the rule is a room
split?     : no, one room
tidy-first?: no
check      : python3 -I -B unit.py validate . · test -L RULE.md · test -e unit.py
files      : TASK.md · GOAL.md · PLAN.md · PRODUCTS.md · RESEARCH.md · UNITS.md · OWNER.md · RULE.md · unit.py · measure.py · audit.py
base       : none, the first block of this room
lines      : +95 ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py
added      : the six ledgers, the links, the bootstrap commit, the leaf G1 with S02, S03, the planned U0002, unread until the review of U0002, a pipe sign of the check reads ¦ in the leaf
rejected   : a copy of the rule or the gate, links
split      : none
deleted    : none
result     : check exits 0 0 0 · the bootstrap commit
review     : written closed by room.py, the review of the room maker unit covers it
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0002 · 2026-11-12 · behavioral · closed
sentence   : measures.py computes the count of G1
plan       : A0001 · S02
delete?    : no, the room computes no number of G1 yet
modify?    : no, no tool of the room computes a number
duplicate  : `git grep -c "measures.py\|def g1" 49e854d -- .` → 3 files, GOAL.md 2, PRODUCTS.md 1, UNITS.md 2, all ledger mentions, no code
cause      : result layer of inputs → rules → state → result → view, RULE §1: the leaf G1 is unmeasured, its measure step opens first. intent: the room reads one number for G1, through its confined adapter and by hand. result: the adapter of measure.py returns «0 of 5» for G1 and `python3 -B measures.py g1` prints that line with one line per acceptance test
split?     : no, one tool with one number
tidy-first?: no, the file is new
check      : python3 -B -c "import measure;print(measure.measures('.',[],['G1'])['G1'])" | grep -qx '0 of 5' · python3 -B measures.py g1 | head -1 | grep -qx 'G1 0 of 5' · python3 -B measures.py g1 | grep -qx '  test_unreferenced_annotation_pruned missing'
files      : GOAL.md:18 · PLAN.md:10 · UNITS.md:24,27-44 · measures.py:1-71 · unit.log:1-111, from git diff -U0 at close
base       : U0001 closed, commit 49e854d
lines      : +86 ~6 −0 moved 0, by staged tree at close
added      : measures.py with `g1(room, bl)` for the confined adapter of measure.py and a `g1` command for the hand, the five acceptance test names, django started on an in-memory database so the adapter writes no file, the mark pass, fail or missing per test, the G1 baseline 0 of 5 in GOAL.md, S02 done in PLAN.md
rejected   : a `g1()` that only prints, round 1 of the review: the adapter calls `g1(room, bl)` and reads its return, so the leaf stayed unmeasured · a subprocess run of tests/runtests.py, it makes a temporary directory and the confinement denies every write · a parse of the suite summary line, it cannot tell a missing test from a failing one · a probe script with its own models, the django suite already carries the models of the issue
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +1 −1 · PLAN.md +1 −1 · UNITS.md +19 −4 · measures.py +71 −0
review     : r1 fail, «measures.py  defines  g1()  with no parameters and only prints, so the room's adapter ( measure.py , which calls  g1(room, bl)  and reads its return) reports G1 as  no value: TypeError  and the leaf stays unmeasured, leaving the step's named move undone while PLAN.md already marks S02 done.», model claude-opus-5, session d013c5a9-4b58-4d98-84d2-c5693123d08e, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0002-r1.md sha256=9b840a7307dea196e8b43bb245735e40059422f62772b5722bc0d1cd4d6a949c · r2 pass, «the adapter now returns the count ( measure.measures  reads  0 of 5 ), all three clauses exit 0 with the unit and 1 1 1 at 49e854d, and every verified key holds except the stale  PLAN.md:17  pointer, which RULE §4 classes as a correctable note.», model claude-opus-5, session 9b0a33cc-cb34-40c4-848d-9d8d96acdc7e, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0002-r2.md sha256=4ca95aa5dac29621411bcceae236264e2b5d95742b8486b670f079400604b5e8
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-13 · structural · closed
sentence   : the plan cuts A0001 into the steps with the planned blocks that fix the issue of TASK.md
plan       : A0001 · S none, a planning unit carries no step, RULE §3
delete?    : no, the plan holds one step for G1 without its product
modify?    : yes, S03 of the bootstrap becomes the pilot row S05 with its product P11
duplicate  : `git grep -c "get_aggregation\|annotation_select_mask" d144671 -- django tests` → 2 files, django/db/models/query.py 1, django/db/models/sql/query.py 16, one home for the decision, no second one
cause      : state layer of inputs → rules → state → result → view, RULE §3: an owner order with an empty queue opens a planning unit. intent: the steps with the queue that carry A0001 to G1 at target. result: S03, S04, S05 with P11, P12, P13, the section «Order», the planned U0004, U0005, U0006
split?     : no, the plan of one statement
tidy-first?: no, the rows are new
check      : grep -qE '^\| S05 \| G1 \| P11 \|.*pilot.*G1 from 0 of 5 to 5 of 5' PLAN.md · grep -cE '^\| S0[34] \| G1 \| P1[23] \|.*G1 from 0 of 5 to 0 of 5' PLAN.md | grep -qx 2 · grep -qE '^\| P11 \| the summary query of django' PRODUCTS.md · sed -n '/^## Order/,$p' PLAN.md | grep -q '^1\. U0004 under S03'
files      : PLAN.md:11-20 · PRODUCTS.md:17-21 · UNITS.md:45-86 · unit.log:112-157, from git diff -U0 at close
base       : U0002 closed, commit d144671
lines      : +56 ~1 −0 moved 0, by staged tree at close
added      : S03 with P12 for the red acceptance tests, S04 with P13 for `get_refs`, S05 with P11 for the pruned summary query, the section «Order» with its three ranks, P11, P12, P13 with the note that django's files are the adopted baseline of RULE §4, the planned U0004, U0005, U0006
rejected   : a step for `exists()`, the hint of TASK.md: `Query.exists` already masks every annotation through `clear_select_clause`, so no unit of this room moves it · a step that splits django/db/models/sql/query.py under its 500 cap, A0001 asks for the fix, the size is the adopted baseline · a fourth planned block for the release note, the queue holds at most three, RULE §3 · one block for `get_refs` with the prune, two design decisions in one unit
split      : none
deleted    : the S03 row of the bootstrap without its product, replaced by S03, S04, S05 with theirs
result     : check exits 0 0 0 0 · PLAN.md +10 −1 · PRODUCTS.md +5 −0 · UNITS.md +42 −0
review     : r1 pass, «every clause exits 0 with the unit and non-zero at d144671, and each verdict key is true of the files, with only a correctable off-by-one in the files ranges.», model claude-opus-5, session 40608b14-47e7-4e6f-b982-a937737b243f, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0003-r1.md sha256=f47c5d3840dead3237618eb67fd0b7020a1da461437c2f84a741c435e319127b · r2 fail, «the S03 step text in PLAN.md was changed at 00:29:14 in answer to the close deny at 00:29:04, after the r1 pass line was written at 00:28:58, so the single review round in the review key read a plan that no longer stands and no check clause binds that row.», model claude-opus-5, session 99459353-ff62-4967-bab7-018236c02613, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0003-r2.md sha256=4f7d6078cd2476e7c395c180997e92212f4a6174ab7560fe41d7254c35383cf5 · r3 pass, «every clause exits 0 with the unit and non-zero at d144671 including the new clause that binds the S03 row r2 found unbound, and each verdict key is true of the files, leaving only a one-command undercount in the result key that §4 calls a note.», model claude-opus-5, session 39af3252-2c3e-4ba4-8545-e32337d6fa3d, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0003-r3.md sha256=43ba25892d815ad4502c2d1cffa6baeddb59248b02cd282001da88e694d4708c
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-13 · behavioral · closed
sentence   : the five acceptance tests of TASK.md enter tests/aggregation/tests.py
plan       : A0001 · S03
delete?    : no, no test of the suite reads the annotations a count query carries
modify?    : no, the five cases are new, `AggregateTestCase` holds the models they need
duplicate  : `git grep -n "captured_queries\[0\]\[.sql.\]" 0a3ea0e -- tests/aggregation` → 2 hits, tests.py:541 reads «SELECT COUNT(*) » of `aggregate(n=Count("*"))`, tests.py:1033 reads «for update» of a select_related aggregate, neither one reads the annotations a count query carries
cause      : view layer of inputs → rules → state → result → view, RULE §3: the pilot needs its red first. intent: five cases read the SQL a count or an aggregate emits. result: three fail at the base over the annotations TASK.md names, two pass as guards of the grouping a prune must keep
split?     : no, one case per claim of TASK.md in one class
tidy-first?: no, the cases append to the class the measure names
check      : python3 -B measures.py g1 | head -1 | grep -qx 'G1 2 of 5' · python3 -B measures.py g1 | grep -qx '  test_unreferenced_annotation_pruned fail' · python3 -B measures.py g1 | grep -qx '  test_referenced_group_by_annotation_kept fail'
files      : PLAN.md:11,18-21 · UNITS.md:66-67,69-85 · tests/aggregation/tests.py:36,38,2089-2138 · unit.log:158-204, from git diff -U0 at close
base       : U0003 closed, commit 0a3ea0e
lines      : +67 ~9 −0 moved 0, by staged tree at close
added      : `Concat` with `Mod` in the imports, five cases on `AggregateTestCase`: an annotation no one refers to, an aliased aggregate, an aggregate annotation, an aggregate over an annotation, a group by over an annotation, each one reading the SQL the query emitted, S03 done in PLAN.md with the section «Order» redrawn
rejected   : a class of its own with two books, `AggregateTestCase` already holds the six books the cases count, a second class would ask the measure of U0002 to name it · an assertion on the whole SQL text, it binds the spelling of the backend, not the annotations the query carries · a case for `exists()`, `Query.exists` already masks every annotation
split      : none
deleted    : none
result     : check exits 0 0 0 · PLAN.md +5 −4 · UNITS.md +19 −5 · tests/aggregation/tests.py +52 −0
review     : r1 pass, «every clause exits 0 with the unit and 1 at 0a3ea0e, the nine verdict keys are true of the files, and the five cases stay behind the S03 interface, leaving only a one-command line count and two stale step baselines as notes.», model claude-opus-5, session 86fed8a7-99e1-4408-9fef-6cef0d8f352b, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0004-r1.md sha256=8b5dc93f0ee7fdb0d8bfb7a2c94cc25edc67bcd52398f5c9dbbc009898536e0a
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-13 · structural · closed
sentence   : `get_refs` returns the annotation names a resolved expression refers to
plan       : A0001 · S04
delete?    : no, nothing in django reads the refs of an expression
modify?    : no, `get_group_by_cols` answers about columns, `_gen_cols` walks to `Col` through a `Ref`, neither one names the annotation
duplicate  : `git grep -n "get_refs" 3eb3825 -- django` → 0 hits, the name is free, no second home
cause      : rules layer of inputs → rules → state → result → view, RULE §1: the mask of U0006 keeps an annotation only when it can name the refs of an aggregate. intent: one question an expression answers about itself. result: `Func(Ref('a', …), Ref('b', …)).get_refs()` reads `{'a', 'b'}`, a `WhereNode` folds the refs of its children
split?     : no, one question with one answer, the three homes are the base expression, the one that holds a ref, the node that holds children
tidy-first?: no, the methods are new
check      : PYTHONPATH=/private/tmp/hectoline-hard-work-2/pydeps python3 -B -c "from django.db.models.expressions import Func, Ref, Value;print(sorted(Func(Ref('a', Value(1)), Ref('b', Value(2))).get_refs()))" | grep -qx "\['a', 'b'\]" · PYTHONPATH=/private/tmp/hectoline-hard-work-2/pydeps python3 -B -c "from django.db.models.sql.where import WhereNode;from django.db.models.expressions import Ref, Value;print(sorted(WhereNode([WhereNode([Ref('c', Value(1))])]).get_refs()))" | grep -qx "\['c'\]"
files      : PLAN.md:12-13,18,20 · UNITS.md:87,90-106 · django/db/models/expressions.py:431-436,1169-1171 · django/db/models/sql/where.py:190-195 · unit.log:205-238, from git diff -U0 at close
base       : U0004 closed, commit 3eb3825
lines      : +29 ~8 −1 moved 0, by staged tree at close
added      : `BaseExpression.get_refs`, which folds the refs of its source expressions, `Ref.get_refs`, which returns its own name, `WhereNode.get_refs`, which folds the refs of its children because a node is no expression, S04 done in PLAN.md with the section «Order» redrawn
rejected   : one method on `Query._gen_cols`, it walks to a `Col` through a `Ref` and loses the name the mask needs · a guard `getattr(expr, "get_refs", None)` in the fold, every source of a resolved expression is an expression or a where node, both carry the method now · a `get_refs` on `F`, an unresolved name reaches no mask
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +4 −5 · UNITS.md +18 −4 · django/db/models/expressions.py +9 −0 · django/db/models/sql/where.py +6 −0
review     : r1 pass, «every check clause exits 0 with the unit and non-zero at base 3eb3825, the nine verdict keys and the files ranges are true of the diff, and the three added methods stay behind the S04 interface with no behavior change (924 tests, only U0004's three base-red acceptance tests fail), leaving only a cor», model claude-opus-5, session 359be019-ef4a-47cd-8cb9-2f77afde9232, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0005-r1.md sha256=f6394d56bd773fed0e864291b132a6f9277edb201c5d86aefa6a267d09877736
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0006 · 2026-11-13 · behavioral · closed
sentence   : a summary query keeps only the annotations its aggregates or its group by reference
plan       : A0001 · S05
delete?    : no, deleting the subquery branch would lose the grouping the two guard cases of U0004 need
modify?    : yes, `Query.get_aggregation` is that block, this unit changes its mask in place and opens no second home
duplicate  : `git grep -c "existing_annotations" 44b319f -- django tests` → 1 file, django/db/models/sql/query.py 3, one home for the decision, no second one
cause      : rules layer of inputs → rules → state → result → view, RULE §8: `get_aggregation` decides which annotations a summary query carries, the annotation nothing refers to rides along from there. intent: a summary query carries the annotations its aggregates, its group by or its having refer to, no other. result: `Book.objects.annotate(full_name=Concat("name", Value(" "), "isbn")).count()` emits `SELECT COUNT(*) AS "__count" FROM "aggregation_book"`, one select, no `full_name`, while `values(pages_mod=Mod("pages", 10)).annotate(mod_count=Count("*")).count()` keeps `pages_mod` in its subquery
split?     : no, one decision with one home, the mask of the subquery and the inline of the plain query are the two halves of that decision
tidy-first?: no, U0005 moved the structure first, `get_refs` already stands on the expression and on the where node
check      : python3 -B measures.py g1 | head -1 | grep -qx 'G1 5 of 5' · python3 -B measures.py g1 | grep -qx '  test_unreferenced_annotation_pruned pass' · python3 -B measures.py g1 | grep -qx '  test_referenced_group_by_annotation_kept pass'
files      : GOAL.md:17-18 · PLAN.md:13,18,20 · UNITS.md:108,111-127 · django/db/models/sql/query.py:444-450,453-463,466-468,477-478,500,505-518,552-564 · unit.log:239-377, from git diff -U0 at close
base       : U0005 closed, commit 44b319f
lines      : +51 ~23 −0 moved 0, by staged tree at close
added      : `has_existing_aggregation`, which reads the aggregate annotations and the having clause of `self.where.split_having_qualify()`, so a plain annotation no longer forces the subquery, `qualify` in the subquery test, which keeps the subquery for a filter over a window function, the annotation mask of the inner query, built from the aggregates with the refs of the group by, of each aggregate and of the having, and the inline of an existing annotation into its aggregate with `set_annotation_mask` in the plain branch, G1 5 of 5 in GOAL.md, S05 done in PLAN.md with the section «Order» redrawn
rejected   : a prune in `Query.exists`, `clear_select_clause` already masks every annotation there, the hint of TASK.md asks for nothing more · a mask that drops every annotation the aggregates do not name, the group by of a `values().annotate()` count refers to one and test_referenced_group_by_annotation_kept turns red · a `has_existing_aggregation` read from `annotation_select`, an `alias()` aggregate carries no select, escapes the test and its count loses the grouping · the mask under a `qualify`, a filter over a window function needs the realiasing the inner query cannot do · a `Query.prune_annotations` helper, `get_aggregation` is the one home of the decision and a second name would split it
split      : none
deleted    : the comment «we aren't smart enough to remove the existing annotations», the local `has_existing_aggregate_annotations` of the inner branch, the list form of `existing_annotations`
result     : check exits 0 0 0 · GOAL.md +2 −2 · PLAN.md +3 −3 · UNITS.md +18 −4 · django/db/models/sql/query.py +51 −14
review     : r1 pass, «every check clause exits 0 with the unit and is red at base 44b319f, all nine verdict keys and the counts are true of the diff, and the change stays inside  get_aggregation  behind the S05 interface with no regression across 1691 related Django tests.», model claude-opus-5, session 8b9c1673-ec49-4fd7-b26e-12256c61e429, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0006-r1.md sha256=08afb04d263c116ec95d252529c3284ef2a6b801f8e1baecec5135a5b0dcf302
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0007 · 2026-11-13 · structural · closed
sentence   : the plan takes the fault of U0006 into a step with its planned block
plan       : A0001 · S none, a planning unit carries no step over an empty queue, RULE §3
delete?    : no, no row of the plan removes the fault, the step that repairs it is new
modify?    : no, S05 is done and its number moved, a done step takes no further unit
duplicate  : `git grep -c "refs_window\|refs_subquery" 78385cd -- django` → 0 hits, `git grep -c "contains_over_clause" 78385cd -- django/db/models/sql/query.py` → 0 hits, no home of the summary query asks what an aggregate refers to
cause      : state layer of inputs → rules → state → result → view, RULE §3: the queue is empty and a fault stands in the product, so a planning unit cuts the next work. intent: the plan names the repair of the fault U0006 left, behind the audit RULE §2 stands first. result: S06 under G1 with P11 and the planned U0008, the section «Order» with the due audit in rank one and the repair in rank two
split?     : no, one step with one planned block
tidy-first?: no, the rows are new
check      : grep -qE '^\| S06 \| G1 \| P11 \|.*window or to a subquery annotation keeps its subquery' PLAN.md · sed -n '/^## Order/,$p' PLAN.md | grep -q '^1\..*lists the fault U0006 left' · sed -n '/^## Order/,$p' PLAN.md | grep -q '^2\. U0008 under S06'
files      : PLAN.md:14,19-20 · UNITS.md:129-156 · unit.log:378-445, from git diff -U0 at close
base       : U0006 closed, commit 78385cd
lines      : +30 ~1 −0 moved 0, by staged tree at close
added      : S06 under G1 with P11 for the subquery an aggregate over a window or over a subquery annotation needs, its text citing A0001 as RULE §2 of 1.1 asks of a new row under a met leaf, the planned U0008 with its four texts, the section «Order» redrawn with the due audit in rank one, which now also lists the fault, and the repair in rank two
rejected   : a redesign of U0006, RULE §4 gives a redesign to a failed unit, U0006 closed with its three clauses green and its review passed, so the repair takes a step of its own · the repair in rank one, round 1 of the review read RULE §2 «A due audit stands first» and the rank two of RULE §3 against it, no A row and no audit finding permits that deviation, so the audit took rank one · a planned block for the audit, an audit unit carries no step and its four texts open it, RULE §4, so no block of the queue holds it · a test step before the repair, S03 already carries the acceptance tests of TASK.md and the check of U0008 reads the crash from the shell in one command · a second A row for the fault, A0001 already asks for the fix and no owner line followed it
split      : none
deleted    : none
result     : check exits 0 0 0 · PLAN.md +3 −1 · UNITS.md +28 −0
review     : r1 fail, «the  Order  the unit rewrites puts the due goal-checks-met audit at rank two behind U0008, against RULE §2 "A due audit stands first" and RULE §3's rank two, with no A row or audit finding permitting the deviation.», model claude-opus-5, session f91ad885-c5e0-4397-9280-a9a98459e83f, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0007-r1.md sha256=8fc5d2998680f7c8a4d8afd5cfc734228816cbccad91bf3864bb16313f24b242 · r2 pass, «the r1 finding is repaired with the due audit at rank one, and every check clause is red at base 78385cd and green now, with each verdict key true of the files I read.», model claude-opus-5, session d3f6cd44-2e9d-40e2-8d9e-44f48a7878a7, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0007-r2.md sha256=fbb5f9aa05c789298d21fc06ff585c203cdb5cda0491c915f5eb9bc0f1bfcad1 · r3 pass, «from a session distinct from r1 and from the author.», model claude-opus-5, session 4d808cc3-f5bb-4835-94ef-f552737b7d47, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0007-r3.md sha256=1a122abcd1eed105c3321b87400bc7effd157740297f3c981cc406db5b651d79
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0008 · 2026-11-13 · behavioral · closed
sentence   : an aggregate that refers to a window or to a subquery annotation keeps its subquery
plan       : A0001 · S06
delete?    : no, the fault is a missing test in the wrapping decision, no line of `get_aggregation` removes it, and dropping the mask of U0006 would return the annotation nothing refers to
modify?    : yes, the wrapping test of `get_aggregation` is that block, two terms enter it in place and no second home opens
duplicate  : `git grep -c "refs_window\|contains_over_clause" aba6110 -- django/db/models/sql/query.py` → 0 hits, no home of the summary query asks what an aggregate refers to
cause      : rules layer of inputs → rules → state → result → view, RULE §4: the fault stands in the home U0006 touched, the wrapping test reads `contains_aggregate` alone, so an aggregate inlines what it cannot inline. intent: an aggregate that refers to a window or to a subquery annotation keeps the subquery it needs. result: `Book.objects.annotate(w=Window(Avg("pages"), partition_by=F("publisher"))).aggregate(s=Sum("w"))` emits two selects where sqlite answered «misuse of window function AVG()», the aggregate over a `Subquery` annotation emits three
split?     : no, one decision, what an aggregate cannot inline, the window and the subquery are its two cases
tidy-first?: no, `get_refs` of U0005 already names the refs the loop reads
check      : PYTHONPATH=/private/tmp/hectoline-hard-work-2/pydeps python3 -B -c "import measures;measures.start(measures.ROOM);from django.db import connection;from django.db.models import Sum, Avg, F, Window;from aggregation.models import Book;from django.test.utils import CaptureQueriesContext;ctx=CaptureQueriesContext(connection);ctx.__enter__();Book.objects.annotate(w=Window(Avg('pages'), partition_by=F('publisher'))).aggregate(s=Sum('w'));ctx.__exit__(None,None,None);print(ctx.captured_queries[0]['sql'].lower().count('select'))" | grep -qx 2 · PYTHONPATH=/private/tmp/hectoline-hard-work-2/pydeps python3 -B -c "import measures;measures.start(measures.ROOM);from django.db import connection;from django.db.models import Count, Sum, OuterRef, Subquery;from aggregation.models import Author;from django.test.utils import CaptureQueriesContext;q=Author.book_set.through.objects.values('author').filter(author=OuterRef('pk')).annotate(total=Count('book'));ctx=CaptureQueriesContext(connection);ctx.__enter__();Author.objects.annotate(t=Subquery(q.values('total'))).aggregate(s=Sum('t'));ctx.__exit__(None,None,None);print(ctx.captured_queries[0]['sql'].lower().count('select'))" | grep -qx 3
files      : PLAN.md:14,19,21 · UNITS.md:150,153-169 · django/db/models/sql/query.py:30,465-474,489-490 · unit.log:446-548, from git diff -U0 at close
base       : U0007 closed, commit aba6110
lines      : +27 ~7 −1 moved 0, by staged tree at close
added      : `refs_subquery` with `refs_window`, read from the refs of each aggregate and tested beside `has_existing_aggregation`, `Subquery` in the imports of the module, S06 done in PLAN.md with the section «Order» redrawn
rejected   : a `subquery = True` attribute on `Subquery` in expressions.py, which `getattr(annotation, "subquery", False)` would read, a unit touches one product, RULE §1, and this unit stands in P11 · a walk into the source expressions of the annotation, a nested `Coalesce(Subquery(...))` inlines into valid SQL and the deeper walk would carry no case of this fault · a line that masks the window annotation in the inner query, `aggregate.get_refs()` already keeps it there · a case in tests/aggregation/tests.py, a test file and code outside tests cannot share one unit, RULE §4, so the two clauses read the SQL from the shell
split      : none
deleted    : none
result     : check exits 0 0 · PLAN.md +3 −4 · UNITS.md +18 −4 · django/db/models/sql/query.py +13 −0
review     : r1 pass, «both clauses are red at base aba6110 and green now, the change is exactly the two-term wrapping test the sentence names inside S06's interface, and every verdict key is true of the files I read.», model claude-opus-5, session e485d590-228f-48d2-8fed-9f0068d1efac, /private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/reviews/agent-review-u0008-r1.md sha256=664b26446581a1f02616138030b57c7bf9fb696d65d7cebf01ec08d93ba22390
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0009 · 2026-11-13 · audit · open
sentence   : the first audit reruns the clauses of the eight closed units on a confined copy
plan       : A0001 · S none, an audit unit carries no step, RULE §3
delete?    : yes, an audit deletes only, RULE §1, and this one deletes the Order line of the work it is
modify?    : no, no block of UNITS.md holds an audit, the periodic check of RULE §4 has no home in this room yet
duplicate  : `git grep -c "· audit ·" 3e4a796 -- UNITS.md` → 0 files, exit 1, no audit block stands, `git grep -c audit 3e4a796 -- UNITS.md PLAN.md` → UNITS.md 5, PLAN.md 1, all of them rejected keys and the Order line that asks for this unit
cause      : result layer of inputs → rules → state → result → view, RULE §4: an audit is due once the goal checks are met, G1 reached 5 of 5 in U0006 and the ledger holds no audit, so RULE §2 stands it first in the Order. intent: the room reads the exits of every clause it closed, rerun on a confined copy, with the structure counts of its first audit. result: the receipt the added key binds by its digest holds the 4 of 4 denied writes of the control, the exit of each clause of U0002 to U0008 and the sections RULE §4 «Audit every 10 units, every 100, every 1000» asks for
split?     : no, one audit at the 10 level over eight closed units
tidy-first?: no, audit.py stands beside the room and runs it unchanged
check      : d=$(python3 -B -c "import hashlib;print(hashlib.sha256(open('/private/tmp/hectoline-hard-work-2/django__django-16263/hectoline-hard/receipts/audit-10-u0009.txt','rb').read()).hexdigest())"); grep -q "sha256=$d" UNITS.md · f=$(grep -o '/private[^ ]*audit-10-u0009.txt' UNITS.md | head -1); grep -q '^## confinement control: 4 of 4 writes outside a clause copy denied' "$f" · f=$(grep -o '/private[^ ]*audit-10-u0009.txt' UNITS.md | head -1); grep -q '^## check rerun on a copy: 0 of 8 closed units fail a clause now' "$f"
files      : UNITS.md:≤40 · PLAN.md:≤4
base       : U0008 closed, commit 3e4a796
lines      : ≤60
added      : 
rejected   : 
split      : 
deleted    : 
result     : 
review     : 
approval   : 

