"""Read task metadata and decide eligibility from supplied values."""
import os, re
from ledger import git, read, rows_of
from policy import measurement_error, step_request


def step_input(room, vals):
    """Return the metadata error and requested measurement leaf."""
    path = os.path.join(room, 'PLAN.md')
    marker = re.search(r'^## rule 1\.1 from S(\d+)',
                       read(path), re.M)
    steps = rows_of(room, 'PLAN.md', 'S')
    goals = rows_of(room, 'GOAL.md', 'G')
    return step_request(vals, steps, goals, marker)


def step_error(room, vals, values):
    """Check one step using only its supplied measurement."""
    error, leaf = step_input(room, vals)
    if error or not leaf:
        return error
    return measurement_error(leaf, values.get(leaf))


def addon_candidates(room):
    """Select new unapproved todo steps from the current plan diff."""
    old = re.findall(r'^\| (S\d+) ',
                     git(room, 'show', 'HEAD:PLAN.md'), re.M)
    diff = git(room, 'diff', '-U0', 'HEAD', '--', 'PLAN.md')
    rows = []
    for line in diff.splitlines():
        if not line.startswith('+| S'):
            continue
        body = line[1:].strip().strip('|')
        cells = [part.strip() for part in body.split('|')]
        if cells[0] in old or len(cells) <= 6:
            continue
        approved = re.search(r'\bA\d{4}\b', cells[3])
        if cells[-1] == 'todo' and not approved:
            rows.append(cells)
    return rows


def eligibility_requests(room, bl, candidates=(), blocked=False, addons=False):
    """Collect only leaves required by the selected eligibility decisions."""
    from policy import blocked_leaves, leaf_goals
    needed = set()
    for vals in candidates:
        error, leaf = step_input(room, vals)
        if not error and leaf:
            needed.add(leaf)
    if blocked:
        rows = rows_of(room, 'PLAN.md', 'S')
        steps = {r[0]:r for r in rows}
        needed.update(blocked_leaves(steps, bl, {}))
    if addons:
        goals = rows_of(room, 'GOAL.md', 'G')
        leaves = {row[0] for row in leaf_goals(goals)}
        added = {row[1] for row in addon_candidates(room)}
        needed.update(added & leaves)
    return needed
