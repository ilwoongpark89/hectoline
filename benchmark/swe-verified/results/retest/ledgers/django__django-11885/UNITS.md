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
delete?    : no, this room holds no measure tool, deletion leaves G1 unmeasured
modify?    : no, no block of this room holds a number of G1
duplicate  : git grep -c "def g1" ec02d49 -- '*.py' ¦ wc -l prints 0, no measure of G1 at the base
cause      : result layer of inputs → rules → state → result → view, RULE §5: a goal leaf carries one number its own tool computes, so the acceptance cases of A0001 become that count. intent: G1 reads a number in place of «no tool». result: G1 reads 1 of 2, the delete suite of django green, the combined fast delete case not written yet
split?     : no, one file holds the count with the runner that produces it
tidy-first?: no, measures.py enters as a new file
check      : grep -q '^def g1' measures.py · python3 -B measures.py --g1 | grep -qE '^[0-9]+ of 2$' · grep -q '| G1 |.*| 2 of 2 | 1 of 2 |' GOAL.md
files      : GOAL.md:18 · PLAN.md:10 · UNITS.md:24,27-44 · measures.py:1-49 · unit.log:1-75, from git diff -U0 at close
base       : U0001 closed, commit ec02d49
lines      : +64 ~6 −0 moved 0, by staged tree at close
added      : measures.py with g1, its interpreter probe and its one-label runner · the G1 row with target 2 of 2 and first number 1 of 2 · S02 done
rejected   : tests/runtests.py of django as the runner, it writes a temp directory and the confined worker of RULE §5 denies every write · the whole django suite as the case list, A0001 names the deletion collector alone · asgiref with sqlparse vendored into the room, third-party lines that no block can hold
split      : none
deleted    : none
result     : check exits 0 0 0 · GOAL.md +1 −1 · PLAN.md +1 −1 · UNITS.md +19 −4 · measures.py +49 −0
review     : r1 pass, «every clause exits 0 at this tree and red at ec02d49, each field is true against the files, and the only defect is the  lines  count, a note-grade slip that one numstat command corrects.», model claude-opus-5, session bf4b0c55-2df4-483d-a993-097e992287bb, /private/tmp/hectoline-retest-work/django__django-11885/hectoline-retest/reviews/agent-review-u0002-r1.md sha256=85ac0270c6cb6b5934827cee67c908d8da3555cdec0ea4fbe91a1b0e5b56f125
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0003 · 2026-11-12 · structural · closed
sentence   : the plan of A0001 cuts the fix of the TASK.md issue into its units
plan       : A0001 · S none, a planning unit of RULE §3 carries no step
delete?    : no, the plan of S03 names no product, no deletion reaches the issue of TASK.md
modify?    : yes, the S03 row of PLAN.md changes in place, no new step row enters
duplicate  : git grep -n "P11" 0d1f3d9 -- PLAN.md PRODUCTS.md ¦ wc -l prints 0, no step of this room names the product yet
cause      : rules layer of inputs → rules → state → result → view, RULE §3: the pilot step stands before its first work unit with its product, its interface, its units. intent: the three units of the fix stand in order with their budgets. result: S03 names P11 with U0004, U0005, U0006, the section «Order» holds that order
split?     : no, one plan with one product
tidy-first?: no, the S03 row waits for its product since U0001
check      : grep -qE '^\| S03 \| G1 \| P11 \|.*1 of 2 to 2 of 2.*U0004 U0005 U0006' PLAN.md · grep -qE '^\| P11 \|.*deletion.py' PRODUCTS.md · sed -n '/^## Order/,$p' PLAN.md | grep -q 'U0004, the acceptance case of A0001'
files      : PLAN.md:11-19 · PRODUCTS.md:17 · UNITS.md:45-86 · unit.log:76-99, from git diff -U0 at close
base       : U0002 closed, commit 0d1f3d9
lines      : +51 ~1 −0 moved 0, by staged tree at close
added      : the S03 row with P11, its interface, its three units · the P11 row of PRODUCTS.md · the section «Order» of PLAN.md · the planned U0004, U0005, U0006
rejected   : a step of its own for the acceptance case, its number would not move, RULE §2 asks a move of each closed step · a fourth planned block for django/contrib/admin/utils.py, U0005 reaches its call line as the caller of P11 · a new A row, A0001 stands active with no new owner statement · tests/delete/tests.py as the home of the case, 584 lines stand over the 500 of RULE §0
split      : none
deleted    : none
result     : check exits 0 0 0 · PLAN.md +9 −1 · PRODUCTS.md +1 −0 · UNITS.md +42 −0
review     : r1 pass, «every check clause exits 0 at this tree and non-zero at the base, each key is true against the files it names, and the diff is exactly the planning move of §3 with no product change.», model claude-opus-5, session 2ae0a8b4-813c-4e38-9f6f-318b8916f8bf, /private/tmp/hectoline-retest-work/django__django-11885/hectoline-retest/reviews/agent-review-u0003-r1.md sha256=8251ab48657d60ede3ea68fe0aae6441f2b0aa79ff6653ea53a3538f0ba69671
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0004 · 2026-11-12 · behavioral · closed
sentence   : one case counts the queries of a cascade delete through two foreign keys to one table
plan       : A0001 · S03
delete?    : no, no case of this room counts the queries of a cascade delete, deletion reproduces nothing
modify?    : no, tests/delete/tests.py of django could hold the case, its 584 lines stand over the 500 of RULE §0
duplicate  : git grep -c "assertNumQueries" 0c9c7d8 -- tests/delete prints tests.py:20, no case of them counts a cascade that reaches one table through two foreign keys
cause      : result layer of inputs → rules → state → result → view, RULE §6: a characterization case records the behavior as it stands before the unit that repairs it. intent: the issue of TASK.md is reproduced inside this room. result: the case runs, 3 queries where 2 are expected, so the case stays red until U0006
split?     : no, one case in one module
tidy-first?: no, the module enters as a new file
check      : grep -q 'def test_one_query_per_related_table' tests/delete/test_combined_fast_delete.py · PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:tests:/tmp/hl-deps /usr/bin/python3 -B measures.py delete.test_combined_fast_delete 2>&1 | grep -q '3 queries executed, 2 expected'
files      : UNITS.md:66,69-85 · tests/delete/test_combined_fast_delete.py:1-20 · unit.log:100-117, from git diff -U0 at close
base       : U0003 closed, commit 0c9c7d8
lines      : +34 ~4 −0 moved 0, by staged tree at close
added      : the module tests/delete/test_combined_fast_delete.py with CombinedFastDeleteTests · the case test_one_query_per_related_table, the first case of CASES in measures.py · the receipt of the issue, 3 queries where 2 are expected, which U0006 replaces with the green case in its own check
rejected   : a case inside tests/delete/tests.py, 584 lines over the 500 cap of RULE §0 · a case that records 3 queries as the outcome, the issue of TASK.md names one query per table as the outcome · an assertion on the SQL text of the combined query, the query count is what the issue states
split      : none
deleted    : none
result     : check exits 0 0 · UNITS.md +18 −4 · tests/delete/test_combined_fast_delete.py +20 −0
review     : r1 pass, «every clause exits 0 at this tree and non-zero on the clone of 0c9c7d8, the running case proves the three-query cascade the sentence names, and each key is true against the files it cites.», model claude-opus-5, session 8df38a63-d721-40e3-91f0-b10981eec29f, /private/tmp/hectoline-retest-work/django__django-11885/hectoline-retest/reviews/agent-review-u0004-r1.md sha256=c86a0179a7211eb6f094eda61658694d7e581cea6bd913acab3ece4cb5a94c4f
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0005 · 2026-11-12 · structural · closed
sentence   : related_objects of the collector takes the related model with the fields that reach it
plan       : A0001 · S03
delete?    : no, the one-field signature carries no second field, deletion removes the cascade query itself
modify?    : yes, the two definitions change in place with the three call lines that reach them
duplicate  : git grep -n "related_objects(self" 7b4e2c6 -- django prints 10 lines, the collector owns 2 of them, deletion.py:252 with admin/utils.py:185
cause      : state layer of inputs → rules → state → result → view, RULE §1 tidy-first: one query over several fields needs the related model with its fields at the interface, so the signature moves before any behavior enters. intent: related_objects takes the fields that reach one related model. result: Collector and its NestedObjects subclass read (related_model, related_fields, objs), the 320 cases of eight suites run as before
split?     : no, two definitions with their call lines are one interface move
tidy-first?: yes, this unit is that structural move, the combination of U0006 enters on it
check      : PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/hl-deps /usr/bin/python3 -B -c "import inspect; from django.db.models.deletion import Collector; print(inspect.signature(Collector.related_objects), inspect.signature(Collector.get_del_batches))" | grep -q '(self, related_model, related_fields, objs) (self, objs, fields)' · PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/hl-deps /usr/bin/python3 -B -c "import inspect; from django.contrib.admin.utils import NestedObjects; print(inspect.signature(NestedObjects.related_objects))" | grep -q '(self, related_model, related_fields, objs)'
files      : UNITS.md:87,90-106 · django/contrib/admin/utils.py:185-187 · django/db/models/deletion.py:1,3,8,164,168,170,227,229,255,257,259-263 · unit.log:118-145, from git diff -U0 at close
base       : U0004 closed, commit 7b4e2c6
lines      : +19 ~17 −0 moved 0, by staged tree at close
added      : the signature related_objects(related_model, related_fields, objs) of Collector · the field list of get_del_batches with its field_names · the predicate of query_utils.Q reduced by operator.or_, one field gives the filter of the base · the call lines of collect with [field] · the override of NestedObjects with select_related over the field names
rejected   : a second method beside related_objects for the many-field query, two homes for one query · the grouping of the fast deletes by table, U0006 owns that behavior · django/contrib/admin/utils.py as a P row of PRODUCTS.md, its 543 lines stand over the 500 cap of RULE §0, P11 names it as the caller that follows the interface
split      : none
deleted    : the one-field filter of related_objects, replaced in place by the reduced predicate
result     : check exits 0 0 · UNITS.md +18 −4 · django/contrib/admin/utils.py +3 −3 · django/db/models/deletion.py +15 −10
review     : r1 pass, «both clauses exit 0 at this tree and non-zero on the clone of 7b4e2c6, the signature move reaches all three call lines behind the S03 interface with the 320 cases failing exactly as they do at the base, and every field is true against the files it cites.», model claude-opus-5, session ff46a878-b319-42b5-9aa6-b032db45a67c, /private/tmp/hectoline-retest-work/django__django-11885/hectoline-retest/reviews/agent-review-u0005-r1.md sha256=ea55061de4bc95a9a53f86710869605197167477ece918d40f781e4698bd229d
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

## U0006 · 2026-11-12 · behavioral · open
sentence   : the fast deletes of one related table combine into one query
plan       : A0001 · S03
delete?    : no, no line of the collector holds the extra queries, the grouping by table has to enter
modify?    : yes, the related branch of collect changes in place, no new method enters
duplicate  : git grep -c "defaultdict" c139423 -- django/db/models/deletion.py prints nothing, no grouping of the fast deletes stands at the base
cause      : state layer of inputs → rules → state → result → view, RULE §1 behavioral: the collector decides which querysets it collects, so the grouping by table enters where it collects them. intent: one fast delete query per related table in place of one per foreign key. result: the acceptance case counts 2 queries, G1 reads 2 of 2, the 1715 cases of 16 suites green
split?     : no, the grouping enters the one place that collects the related objects of a table
tidy-first?: no, U0005 moved the interface that carries the fields
check      : grep -q 'model_fast_deletes\[related_model\].append(field)' django/db/models/deletion.py · PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:tests:/tmp/hl-deps /usr/bin/python3 -B measures.py delete.test_combined_fast_delete · python3 -B measures.py --g1 | grep -qx '2 of 2'
files      : django/db/models/deletion.py:≤30 · PLAN.md:≤8 · UNITS.md:≤24
base       : U0005 closed, commit c139423
lines      : ≤62
added      : model_fast_deletes of collect, the fields of one related table under their model · the can_fast_delete call on the related model class, objs._meta.model reads a class as it reads an instance · one fast delete queryset per related table, batched by get_del_batches over its fields · S03 done with its note in «Order», the queue stands empty
rejected   : the OR filter built in delete() over the collected querysets, the collector decides the grouping where it collects · a mapping in place of the fast_deletes list, delete() reads a list of querysets · can_fast_delete(sub_objs) kept on the queryset, it reads nothing but the model while hiding that the class decides · the baseline of G1 raised to 2 of 2, a baseline is the number the leaf started from
split      : the related loop of collect into two loops, the per-field loop with the per-table fast delete loop
deleted    : the if/else that appended one fast delete queryset per foreign key, its else body moves one level left with no change of its 14 lines
result     : check exits 0 0 0 at this tree, each clause non-zero on the clone of c139423 by the baseline test of close · the case of U0004 prints «Ran 1 test» «OK», the three DELETE statements of its receipt are two · PYTHONPATH=/tmp/hl-deps:. /usr/bin/python3 -B tests/runtests.py admin_views admin_changelist admin_inlines auth_tests queries many_to_many m2m_regress model_inheritance model_inheritance_regress generic_relations_regress signals delete delete_regress admin_utils proxy_models contenttypes_tests prints «Ran 1715 tests» «OK (skipped=43, expected failures=3)» · G1 reads 2 of 2, by python3 -B measures.py --g1
review     : 
approval   : owner 11-12 «Fix the issue in TASK.md in this repository», the A0001 row

