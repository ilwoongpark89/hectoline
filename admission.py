"""Collect room evidence for the pure reconstruction policy."""
import re
from pathlib import Path
import subprocess
from ledger import TABLES, reconstruction_plan
from ledger import blocks, unit_span
from review_evidence import review_record
from review_evidence import reconstruction_review
from policy import review_decision
from ledger import files_of
from ledger import rows_of
from ledger import load, final_commit_order
import reconstruction as cycle


def reconstruction_snapshot(room, revision):
    """Read canonical evidence only from reachable immutable Git objects."""
    if not isinstance(revision, str):
        raise ValueError('revision must be text')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('revision must be a complete commit')
    command = ['git', '-C', room]
    kind = subprocess.check_output(command + ['cat-file', '-t', revision])
    if kind.strip() != b'commit':
        raise ValueError('revision must identify a commit object')
    subprocess.run(
        command + ['merge-base', '--is-ancestor', revision, 'HEAD'],
        check=True, capture_output=True)
    prefix = reconstruction_prefix(room)
    names = sorted(set(TABLES) | {'UNITS.md'})
    snapshot = {}
    for name in names:
        spec = revision + ':' + prefix + name
        body = subprocess.check_output(
            command + ['show', spec], stderr=subprocess.PIPE)
        snapshot[name] = body.decode('utf-8')
    return snapshot


def reconstruction_fact(room, text, order, uid):
    """Bind declared unit facts to their exact committed final record."""
    if uid not in order:
        raise ValueError('unit has no committed finalization')
    entry = order[uid]
    source = reconstruction_snapshot(room, entry['commit'])
    start, end = unit_span(text, uid)
    current = text[start:end].rstrip('\n')
    frozen = source['UNITS.md']
    start, end = unit_span(frozen, uid)
    if frozen[start:end].rstrip('\n') != current:
        raise ValueError('unit body differs from its final commit')
    _, status, _, values = next(blocks(current))
    clauses = values.get('check', '').split(' · ')
    if any(not clause.strip() for clause in clauses):
        raise ValueError('unit has an empty check clause')
    expected = 'check exits ' + ' '.join('0' for _ in clauses)
    result = values.get('result', '').split(' · ')[0]
    if status == 'closed' and result != expected:
        raise ValueError('closed unit lacks successful check evidence')
    verdict, _ = review_decision(review_record(values.get('review', '')))
    plan = values.get('plan', '')
    planning = bool(re.search(r'\bS none\b', plan))
    return dict(
        status=status, verdict=verdict, kind=entry['kind'],
        planning=planning,
        position=list(order).index(uid), commit=entry['commit'],
        values=values, snapshot=source)


def reconstruction_prefix(room):
    """Resolve Git blob paths relative to the declared room."""
    command = ['git', '-C', room, 'rev-parse', '--show-prefix']
    return subprocess.check_output(command).decode().removesuffix('\n')


def plan_state(text, early):
    """Parse one plan revision. An unreadable one counts before the start alone."""
    try:
        return reconstruction_plan(text)
    except ValueError:
        if not early:
            raise
    return None


def start_guard(plan, start, armed):
    """Hold the declared start with the activation across it, S234."""
    declared = plan.get('start') if plan else None
    if declared not in (None, start):
        raise ValueError('history changes its declared start')
    if armed and plan.get('enforce') is not True:
        raise ValueError('declared start disables activated reconstruction')


def reconstruction_history(room, revision):
    """Read the plan changes from the declared start through one frozen revision."""
    frozen = reconstruction_snapshot(room, revision)
    final = reconstruction_plan(frozen['PLAN.md']) or {}
    start = final.get('start')
    prefix = reconstruction_prefix(room)
    command = ['git', '-C', room]
    args = ['log', '--first-parent', '--full-history', '--reverse']
    args += ['--format=%H', revision, '--', 'PLAN.md']
    commits = subprocess.check_output(command + args).decode().splitlines()
    rename_args = ['log', '--first-parent', '--follow', '--format=', '--name-status']
    rename_args += [revision, '--', 'PLAN.md']
    renamed = subprocess.check_output(command + rename_args).decode()
    if re.search(r'(?m)^R\d+\t', renamed):
        raise ValueError('renamed plan needs explicit historical path mapping')
    if start is not None and start not in commits:
        raise ValueError('declared start is no plan revision of this history')
    first = commits.index(start) if start else 0
    history, armed = [], False
    for index, commit in enumerate(commits):
        args = ['ls-tree', commit, '--', 'PLAN.md']
        present = subprocess.check_output(command + args).strip()
        plan = None
        if present:
            spec = commit + ':' + prefix + 'PLAN.md'
            body = subprocess.check_output(
                command + ['show', spec], stderr=subprocess.PIPE)
            plan = plan_state(body.decode('utf-8'), index < first)
        if index < first:
            enabled = bool(plan) and plan.get('enforce') is True
            armed = armed or enabled
            continue
        start_guard(plan, start, armed and index == first)
        history.append((commit, plan))
    return history


def reconstruction_assignment(snapshot, uid, task):
    """Bind declared scope before execution or rollback can narrow it."""
    if uid not in task['units']:
        raise ValueError('unit is not assigned in this task')
    text = snapshot['UNITS.md']
    start, end = unit_span(text, uid)
    body = text[start:end].rstrip('\n')
    _, status, _, values = next(blocks(body))
    plan = values.get('plan', '')
    steps = re.findall(r'\bS\d+\b', plan)
    if 'S none' in plan or steps != [task['step']]:
        raise ValueError('assignment differs from its declared unit step')
    declared = {str(Path(path)) for path in files_of(values)}
    declared -= {'UNITS.md', 'unit.log'}
    products = {str(Path(path)) for path in task['products']}
    if len(products) != len(task['products']):
        raise ValueError('task repeats a canonical product path')
    for path in products | declared:
        value = Path(path)
        if value.is_absolute() or '..' in value.parts:
            raise ValueError('assignment needs an immutable room-relative scope')
    if '.' in products:
        raise ValueError('task scope needs concrete product paths')
    covered = set()
    for scope in declared:
        scope = str(Path(scope))
        matching = set()
        for path in products:
            child = scope == '.' or path.startswith(scope + '/')
            if path == scope or child:
                matching.add(path)
        if not matching:
            raise ValueError('declared scope is outside its frozen task')
        covered.update(matching)
    if not covered:
        raise ValueError('assignment has no source-bound product scope')
    return dict(
        unit=uid, step=task['step'], role=task['role'],
        products=covered, status=status, body=body, values=values)


def reconstruction_catalog(snapshot):
    """Normalize frozen source identities without executing room code."""
    tables = {}
    for name, shape in TABLES.items():
        letter, width = shape
        rows = rows_of('.', name, letter, snapshot[name])
        mapped = {}
        for row in rows:
            if not re.fullmatch(letter + r'\d+', row[0]):
                raise ValueError('frozen table has an invalid identity')
            if len(row) != width or row[0] in mapped:
                raise ValueError('frozen table has ambiguous rows')
            mapped[row[0]] = row
        tables[letter] = mapped
    products = {}
    paths = {}
    for pid, row in tables['P'].items():
        if row[4] == 'none':
            continue
        products[pid] = ' | '.join(row[1:])
        paths[pid] = set(re.split(r',\s*', row[4]))
    steps = {}
    for sid, row in tables['S'].items():
        steps[sid] = dict(
            products=set(re.split(r',\s*', row[2])),
            units=re.findall(r'\bU\d{4}\b', row[5]))
    units = {}
    records = list(blocks(snapshot['UNITS.md']))
    for uid, status, keys, values in records:
        if status is None or uid in units:
            raise ValueError('frozen unit identity is invalid or repeated')
        if len(keys) != len(set(keys)):
            raise ValueError('frozen unit repeats a field')
        found = re.findall(r'\bS\d+\b', values.get('plan', ''))
        units[uid] = found[0] if len(found) == 1 else None
    sources = set(tables['A']) | set(tables['R']) | set(units)
    return dict(
        products=products, paths=paths, steps=steps, units=units,
        sources=sources, goals=set(tables['G']), blocks=records)


def reconstruction_sources(room, revision, uid, task, order, workspace):
    """Bind original assignment and current committed execution separately."""
    valid = isinstance(uid, str)
    if not valid or not re.fullmatch(r'U\d{4}', uid):
        raise ValueError('assignment needs a canonical unit identity')
    frozen = reconstruction_snapshot(room, revision)
    unit_span(frozen['UNITS.md'], uid)
    command = ['git', '-C', room]
    args = ['log', '--first-parent', '--reverse', '--format=%H']
    args += ['--diff-merges=first-parent']
    args += ['-G', '^## ' + uid + ' ', revision, '--', 'UNITS.md']
    commits = subprocess.check_output(command + args).decode().splitlines()
    if not commits:
        raise ValueError('assignment has no immutable declaration history')
    prefix = reconstruction_prefix(room)
    first = commits[0]
    args = ['log', '--first-parent', '--reverse', '--format=%H']
    args += [first + '..' + revision, '--', 'UNITS.md']
    later = subprocess.check_output(command + args).decode().splitlines()
    binding = None
    for commit in [first, *later]:
        spec = commit + ':' + prefix + 'UNITS.md'
        body = subprocess.check_output(command + ['show', spec]).decode()
        start, end = unit_span(body, uid)
        _, status, _, values = next(blocks(body[start:end]))
        if status not in {'planned', 'open', 'waiting'}:
            break
        scope = {str(Path(path)) for path in files_of(values)}
        if scope <= {'UNITS.md', 'unit.log'}:
            continue
        binding = reconstruction_assignment({'UNITS.md': body}, uid, task)
        binding['commit'] = commit
        break
    if binding is None:
        raise ValueError('assignment has no valid pre-execution scope')
    if uid not in order:
        return binding, None
    text = (Path(room) / 'UNITS.md').read_text()
    fact = reconstruction_fact(room, text, order, uid)
    fact['products'] = set()
    if fact['status'] == 'closed':
        paths = files_of(fact['values'])
        changed = {str(Path(path)) for path in paths}
        changed -= {'UNITS.md', 'unit.log'}
        if changed:
            actual = reconstruction_assignment(fact['snapshot'], uid, task)
            products = actual['products']
            if not products <= binding['products']:
                raise ValueError('execution exceeds its original declaration')
            fact['products'] = products
        review = fact['values']['review']
        fact['artifact'] = reconstruction_review(review, uid, workspace)
    return binding, fact


def reconstruction_context(room, record, workspace):
    """Collect one frozen reconstruction graph from immutable sources."""
    text, records = load(room)
    order = final_commit_order(room, records)
    pattern = r'^## (U\d{4}) · \S+ · (\w+) ·'
    kinds = dict(re.findall(pattern, text, re.M))
    windows = cycle.reconstruction_windows(records, kinds, order)
    identity = type(record) is dict
    identity = identity and set(record) == set(cycle.IDENTITY_FIELDS)
    validate = cycle.reconstruction_identity if identity else cycle.reconstruction_receipt
    window = validate(record, windows)
    baseline = reconstruction_snapshot(room, record['baseline'])
    history = reconstruction_history(room, record['revision'])
    states, facts, bindings = [], {}, {}
    active = False
    for commit, plan in history:
        enabled = plan is not None
        enabled = enabled and plan.get('enforce') is True
        if active and not enabled:
            raise ValueError('history cannot disable activated reconstruction')
        active = active or enabled
        same = plan is not None
        same = same and plan.get('window') == list(window)
        if not states and not same:
            continue
        if not same:
            raise ValueError('frozen cycle history loses its reconstruction record')
        matches = lambda uid: order[uid]['commit'] == commit
        authorities = list(filter(matches, order))
        if len(authorities) != 1:
            raise ValueError('revision needs one canonical final authority')
        authority = authorities[0]
        fact = reconstruction_fact(room, text, order, authority)
        fact['artifact'] = reconstruction_review(fact['values']['review'], authority, workspace)
        facts[authority] = fact
        catalog = reconstruction_catalog(reconstruction_snapshot(room, commit))
        for task in plan['tasks']:
            for uid in task['units']:
                if uid in bindings:
                    continue
                binding, execution = reconstruction_sources(
                    room, commit, uid, task, order, workspace)
                bindings[uid] = binding
                if execution is not None:
                    facts[uid] = execution
        states.append(dict(
            unit=authority, commit=commit, plan=plan, catalog=catalog))
    if not states or states[-1]['commit'] != record['revision']:
        raise ValueError('frozen revision does not end its reviewed plan history')
    args = ['git', '-C', room, 'merge-base', '--is-ancestor']
    endpoints = order[window[-1]]['commit'], record['baseline']
    pairs = [endpoints, (record['baseline'], states[0]['commit'])]
    for pair in pairs:
        subprocess.run(args + list(pair), check=True, capture_output=True)
    return dict(
        record=record, windows=windows, blocks=records,
        baseline=reconstruction_catalog(baseline),
        states=states, facts=facts, bindings=bindings)


def reconstruction_verdict(room, record, workspace, receipt=None):
    """Return one source-bound phase or an explicit unknown result."""
    from ledger import strict_object
    from reconstruction_flow import reconstruction_phase
    head = None
    try:
        head_args = ['git', '-C', room, 'rev-parse', 'HEAD']
        head = subprocess.check_output(head_args).decode().strip()
        if receipt is not None:
            bound, completion = reconstruction_receipt_fact(room, receipt, workspace)
            if record is not None and record != bound:
                raise ValueError('receipt differs from requested reconstruction')
            record = bound
        if record is None:
            args = ['git', '-C', room, 'log', '-1', '--first-parent', '--format=%H']
            args += ['--', 'PLAN.md']
            revision = subprocess.check_output(args).decode().strip()
            snapshot = reconstruction_snapshot(room, revision)
            plan = reconstruction_plan(snapshot['PLAN.md'])
            if plan is None:
                raise ValueError('no current reconstruction model')
            record = {key:plan[key]
                      for key in ('version','window','baseline')}
            record['revision'] = revision
        context = reconstruction_context(room, record, workspace)
        evidence = None
        tasks = context['states'][-1]['plan']['tasks']
        for task in tasks:
            if task['role'] != 'proof':
                continue
            for uid in task['units']:
                fact = context['facts'].get(uid, {})
                if fact.get('status') == 'closed':
                    evidence = strict_object(fact['values']['added'])
        result = reconstruction_phase(context, evidence)
        if receipt is not None:
            if result['phase'] != 'receipt-ready':
                raise ValueError('receipt has unfinished reconstruction prerequisites')
            proof = context['facts'][record['proof']]
            if completion['position'] <= proof['position']:
                raise ValueError('receipt must follow committed proof')
            result['phase'] = 'complete'
            result['receipt'] = dict(unit=receipt, commit=completion['commit'])
        current = subprocess.check_output(head_args).decode().strip()
        if current != head:
            raise ValueError('source HEAD changed during reconstruction validation')
        result.update(head=head, record=record, context=context)
        result['reason'] = 'verified source evidence'
        return result
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        return dict(phase='unknown', head=head, reason=str(error))


def reconstruction_receipt_fact(room, uid, workspace):
    """Read one immutable reviewed completion declaration."""
    from ledger import strict_object
    text, records = load(room)
    order = final_commit_order(room, records)
    fact = reconstruction_fact(room, text, order, uid)
    valid = fact['status'] == 'closed' and fact['verdict'] == 'pass'
    if not valid:
        raise ValueError('receipt lacks reviewed closure')
    fact['artifact'] = reconstruction_review(
        fact['values']['review'], uid, workspace)
    record = strict_object(fact['values']['added'])
    return record, fact

