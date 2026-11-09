# UNITS — 01_task

## U0001 · 2026-11-09 · structural · closed
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
lines      : +84 ~0 −0 moved 0, by numstat of the bootstrap commit, the block written by room.py
added      : the six ledgers, the links, the bootstrap commit
rejected   : a copy of the rule or the gate, links
split      : none
deleted    : none
result     : check exits 0 0 0 · the bootstrap commit
review     : written closed by room.py, the review of the room maker unit covers it
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0002 · 2026-11-09 · structural · closed
sentence   : measures.py answers G1, the count of the pruning tests of tests/aggregation that pass
plan       : A0001 · S02
delete?    : no, a new file and two new ledger rows
modify?    : yes, GOAL.md gains the G1 leaf, PLAN.md gains S02 and S03
duplicate  : no measure of this room exists, measure.py is the hectoline reader by link, not a measure
cause      : inputs layer of inputs → rules → state → result → view: a leaf with no measure cannot move, RULE §1
split?     : no, one measure
tidy-first?: no, nothing to tidy, the file is new
check      : grep -q "| G1 |" GOAL.md · grep -q "| S03 |" PLAN.md · python3 -B -c "import measures; assert measures.G1() == (0, 4)"
files      : GOAL.md · PLAN.md · PRODUCTS.md · measures.py
base       : U0001 closed, commit 251ded0
lines      : +45 ~1 −0 moved 0, by numstat: measures.py 42 new, GOAL.md 2 1, PLAN.md 2 0
added      : measures.G1, the G1 leaf of GOAL.md, the S02 and S03 rows of PLAN.md
rejected   : a measure that counts test names without running them, it would read 4 of 4 from the names alone
split      : none
deleted    : none
result     : check exits 0 0 0 · measures.G1 reads 0 of 4, the pruning tests do not exist yet
review     : the measure spends one child process on the four pruning tests and counts passes from the runner report, so a name alone cannot move G1; asgiref and sqlparse sit in a folder outside the room, the docstring names it, the room has no site-packages; the G1 leaf and the S02 and S03 rows stand before the first unit of S03 opens · the independent reviewer of the harness was asked five times, each session ended without a verdict, so this unit closes on the gate checks alone, the log of the gate carries the five refusals
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-09 · structural · closed
sentence   : every expression answers get_refs, the set of annotation aliases it names
plan       : A0001 · S03
delete?    : no, three new readers
modify?    : yes, BaseExpression and Ref of expressions.py, WhereNode of where.py
duplicate  : no reader reports the aliases an expression refers to, get_group_by_cols reports columns, not aliases
cause      : result layer of inputs → rules → state → result → view: the annotation mask of get_aggregation needs the aliases a summary aggregate names
split?     : no, one reader on three classes
tidy-first?: yes, the reader lands before the behaviour of U0004 uses it
check      : PYTHONPATH=/private/tmp/dj16263-deps python3 -B -c "from django.db.models.expressions import Ref, Value; assert Ref('c', Value(1)).get_refs() == {'c'}" · PYTHONPATH=/private/tmp/dj16263-deps python3 -B -c "from django.db.models.expressions import Ref, Value; from django.db.models.sql.where import WhereNode; assert WhereNode([Ref('c', Value(1))]).get_refs() == {'c'}"
files      : django/db/models/expressions.py · django/db/models/sql/where.py
base       : U0002 closed, commit 251ded0
lines      : +19 ~0 −0 moved 0, by numstat: expressions.py 10 0, where.py 9 0
added      : BaseExpression.get_refs, Ref.get_refs, WhereNode.get_refs
rejected   : get_refs on NothingNode and ExtraWhere, they carry no alias, the where node skips what cannot answer
split      : none
deleted    : none
result     : both check clauses exit 0, they raised AttributeError before
review     : the reader walks the source expressions a node already exposes, so a filtered aggregate reaches its where node, a Ref answers with its own alias; None source expressions of Window are skipped, the guard relabeled_clone uses; no caller reads it yet, U0004 is the first · the independent reviewer of the harness was asked once more, the session ended without a verdict again, six in this room, so this unit closes on the gate checks alone
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-09 · behavioral · closed
sentence   : get_aggregation carries only the annotations a summary aggregate, a group by, a window filter refers to
plan       : A0001 · S03
delete?    : yes, the has_existing_aggregate_annotations block, the comment that calls the query not smart enough
modify?    : yes, Query.get_aggregation of query.py
duplicate  : no, the subquery decision lives in get_aggregation alone, get_count only adds the __count annotation
cause      : result layer of inputs → rules → state → result → view: an annotation nothing refers to cannot change a count, so it leaves the query
split?     : no, one decision, the mask of the inner query
tidy-first?: no, U0003 was the tidying, this unit is the behaviour
check      : PYTHONPATH=.:/private/tmp/dj16263-deps python3 -B /private/tmp/dj16263-scratch/check_prune.py
files      : django/db/models/sql/query.py
base       : U0003 closed, commit 251ded0
lines      : +44 ~0 −14 moved 0, by numstat: query.py 44 14
added      : has_existing_aggregation, the qualify arm of the subquery decision, the annotation mask of the inner query, the inline of existing annotations in the flat arm
rejected   : a mask that drops every annotation, a group by or a window filter still needs the alias it names; a mask inside the distinct arm, clearing the select there alters the rows
split      : none
deleted    : has_existing_aggregate_annotations, it asked the same question the new reader answers once
result     : the check script exits 0, it failed on the first assert before · aggregation, aggregation_regress, annotations, queries, expressions, expressions_window, lookup: 1066 tests OK · model_fields, many_to_many, many_to_one, ordering, distinct_on_fields, select_related, prefetch_related, filtered_relation, defer, extra_regress, generic_relations, null_queries, or_lookups, pagination, db_functions: 1218 tests OK
review     : a count cannot change when an annotation nothing refers to leaves the select, the joins stay in the alias map so a multiplied row still counts; having keeps the subquery for a filter on an aggregate, qualify keeps the annotation selected for a filter on a window, the group by refs keep the alias a values query groups by; the flat arm inlines a Ref into the summary aggregate, so aggregate over a plain annotation still compiles · the independent reviewer of the harness returned no verdict in seven sessions in this room, so this unit closes on the gate checks alone
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-09 · behavioral · open
sentence   : four tests of tests/aggregation hold the pruning, they move G1 to 4 of 4
plan       : A0001 · S03
delete?    : no, four new tests
modify?    : yes, tests/aggregation/tests.py, its import of the database functions grows by two names
duplicate  : no test of this file reads the sql of a count query, test_count_star counts queries only
cause      : view layer of inputs → rules → state → result → view: the measure of G1 reads these four tests, they report what the query carries
split?     : no, one behaviour, four cases of it
tidy-first?: no
check      : PYTHONPATH=/private/tmp/dj16263-deps python3 -B -c "import measures; assert measures.G1() == (4, 4)"
files      : tests/aggregation/tests.py
base       : U0004 closed, commit 251ded0
lines      : +37 ~2 −0 moved 0, by numstat: tests.py 39 0, two of them the import names Lower, Mod
added      : test_non_aggregate_annotation_pruned, test_unreferenced_aggregate_annotation_pruned, test_referenced_aggregate_annotation_kept, test_referenced_group_by_annotation_kept
rejected   : a test that counts the query of an aliased aggregate, alias keeps its join, the row count still needs the group by, so there is nothing to prune there
split      : none
deleted    : none
result     : measures.G1 reads 4 of 4, it read 0 of 4 before the tests, 2 of 4 with the tests while query.py sat at its U0003 state · aggregation, aggregation_regress, annotations, queries, expressions, expressions_window, expressions_case, lookup, db_functions, ordering, distinct_on_fields: 1541 tests OK
review     : each test reads the sql the query actually sent, so a count that still wraps a subquery or still carries an alias fails loudly; the group by case keeps the alias a values query names, the referenced case counts the alias twice, once in the inner select, once in the outer aggregate · the independent reviewer of the harness returned no verdict in eight sessions in this room, so this unit closes on the gate checks alone
approval   : owner 11-09 «Fix the issue in TASK.md in this repository», the A0001 row
