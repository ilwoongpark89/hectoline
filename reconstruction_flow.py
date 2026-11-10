"""Reconstruction revision flow from explicit evidence."""


def reconstruction_amendments(
        previous, current, prior, unit, facts, blocks,
        pending=False, routes=None, bindings=None):
    """Bind keyed amendments and reviewed task replacements."""
    from policy import replacement_chain
    if type(pending) is not bool:
        raise ValueError("pending mode must be a boolean")
    routes = {} if routes is None else routes
    declarations = facts if bindings is None else bindings
    edges = []
    changed = reconstruction_changes(previous, current)
    amendments = current.get('amendments', [])
    if type(amendments) is not list:
        raise ValueError('amendments must be a list')
    seen = set()
    for amendment in amendments:
        keys = {'kind', 'key', 'prior', 'unit', 'reason'}
        if type(amendment) is not dict or set(amendment) != keys:
            raise ValueError('unexpected amendment fields')
        for value in amendment.values():
            if not isinstance(value, str):
                raise ValueError('amendment fields must be text')
        key = amendment['kind'], amendment['key']
        if key not in changed or key in seen:
            raise ValueError('unrelated or repeated amendment')
        seen.add(key)
        if amendment['prior'] != prior or amendment['unit'] != unit:
            raise ValueError('amendment does not bind adjacent revisions')
        if not amendment['reason'].strip():
            raise ValueError('amendment needs its reason')
        old, new = changed[key]
        if key[0] != 'task' or not old:
            continue
        selected = new['units'] if new else []
        omitted = set(old['units']) - set(selected)
        if omitted and new and old['products'] != new['products']:
            raise ValueError('replacement must preserve its original task scope')
        for uid in omitted:
            needed = declarations.get(uid, {}).get('products', set())
            scope = set(old['products'])
            replacements = {}
            for task in current['tasks']:
                if task['role'] != old['role']:
                    continue
                task_scope = set(task['products'])
                allowed = scope & task_scope
                if task['step'] != old['step'] and old['role'] == 'migration':
                    prefix = old['step'], task['step']
                    authorized = lambda p: (*prefix, p) in routes
                    allowed = set(filter(authorized, allowed))
                for target in task['units']:
                    products = declarations.get(target, {}).get('products', set())
                    if products and products <= task_scope:
                        contribution = products & allowed
                        if contribution:
                            replacements[target] = contribution, task_scope
            if not needed or not needed <= scope or not replacements:
                raise ValueError('replacement needs its known original scope')
            edges.append(dict(
                unit=uid, role=old['role'], step=old['step'],
                products=set(needed), targets=set(replacements), authority=unit,
                coverage=replacements))
            covered = set()
            for replacement in replacements:
                fact = facts.get(replacement, {})
                valid = fact.get('status') == 'closed' and fact.get('verdict') == 'pass'
                scope, current_scope = replacements[replacement]
                products = fact.get('products', set())
                valid = valid and bool(products) and products <= current_scope
                if valid and uid in replacement_chain(blocks, [replacement]):
                    covered.update(products & scope)
            if not pending and not needed <= covered:
                raise ValueError('omitted assignment lacks reviewed replacement')
    if seen != changed.keys():
        raise ValueError('changed obligation has no matching amendment')
    return edges if pending else None


def reconstruction_chronology(revisions, facts, obligations, bindings):
    """Qualify affected work from validated current assignment bindings."""
    if not revisions:
        raise ValueError('reconstruction has no reviewed design history')
    positions = {}
    previous = -1
    for uid, commit in revisions:
        fact = facts.get(uid, {})
        valid = fact.get('status') == 'closed' and fact.get('verdict') == 'pass'
        planning = fact.get('planning') is True
        planning = planning and fact.get('kind') != 'audit'
        valid = valid and fact.get('commit') == commit
        if not valid or not planning:
            raise ValueError('revision has no matching reviewed planning authority')
        position = fact.get('position')
        if type(position) is not int or position <= previous:
            raise ValueError('revision order is not canonical')
        positions[uid] = position
        previous = position
    pending = set()
    for key, authority in obligations.items():
        if authority not in positions:
            raise ValueError('affected scope has no reviewed structural authority')
        step, path = key
        covered = False
        for uid, binding in bindings.items():
            if binding['step'] != step or binding['role'] != 'migration':
                continue
            fact = facts.get(uid, {})
            valid = fact.get('status') == 'closed' and fact.get('verdict') == 'pass'
            if fact.get('kind') == 'audit' or fact.get('planning'):
                continue
            position = fact.get('position')
            if not valid or type(position) is not int:
                continue
            later = position > positions[authority]
            scope = binding['products'] & fact.get('products', set())
            if later and path in scope:
                covered = True
                break
        if not covered:
            pending.add(key)
    return dict(authorities=positions, pending=pending)


def reconstruction_changes(previous, current):
    """Identify semantic amendments between validated adjacent plans."""
    for key in ('version', 'window', 'baseline'):
        if previous[key] != current[key]:
            raise ValueError('reconstruction identity changed')
    changed = {}
    for kind, field in (('product', 'decisions'), ('task', 'tasks')):
        def key(item):
            if kind == 'product':
                return item['product']
            return item['step'] + '/' + item['role']
        before = {key(item): item for item in previous[field]}
        after = {key(item): item for item in current[field]}
        sizes = len(before), len(after)
        if sizes != (len(previous[field]), len(current[field])):
            raise ValueError('reconstruction repeats an obligation key')
        for name in before.keys() | after.keys():
            old, new = before.get(name), after.get(name)
            if old == new:
                continue
            if kind == 'task' and old and new:
                old_scope = dict(old, units=[])
                new_scope = dict(new, units=[])
                growth = set(old['units']) <= set(new['units'])
                if old_scope == new_scope and growth:
                    continue
            changed[(kind, name)] = (old, new)
    return changed


def reconstruction_routes(previous, current, paths, authority, routes=None):
    """Retain reviewed responsibility routes through assignment cleanup."""
    result = dict(routes or {})
    before = {item['product']: item for item in previous['decisions']}
    for decision in current['decisions']:
        old = before.get(decision['product'])
        if old is None:
            continue
        added = set(decision['steps']) - set(old['steps'])
        for source in old['steps']:
            for target in added:
                for path in paths.get(decision['product'], set()):
                    origins = {source}
                    for start, end, item in list(result):
                        if end == source and item == path:
                            origins.add(start)
                    for origin in origins:
                        result[(origin, target, path)] = authority
    return result

def reconstruction_history(context):
    """Fold reviewed responsibility authority and actual execution."""
    from reconstruction import reconstruction_models
    models = reconstruction_models(context)
    states, facts = context['states'], context['facts']
    bindings, records = context['bindings'], context['blocks']
    routes, obligations, edges, revisions = {}, {}, [], []
    routing_paths, routing_scope = {}, {}
    previous = None
    for state in states:
        plan, unit = state['plan'], state['unit']
        revisions.append((unit, state['commit']))
        paths = {}
        for catalog in [context['baseline'], state['catalog']]:
            for product, scope in catalog['paths'].items():
                paths.setdefault(product, set()).update(scope)
                routing_paths.setdefault(product, set()).update(scope)
        for decision in plan['decisions']:
            product, owner = decision['product'], decision['owner']
            scope = routing_scope.setdefault(product, set())
            scope.update(routing_paths.get(product, set()))
            scope.update(routing_paths.get(owner, set()))
        old = previous['plan'] if previous else {'decisions':[]}
        if previous:
            routes = reconstruction_routes(old, plan, routing_scope, unit, routes)
            edges.extend(reconstruction_amendments(
                old, plan, previous['unit'], unit, facts, records,
                pending=True, routes=routes, bindings=bindings))
        migrations = {}
        for task in plan['tasks']:
            for uid in task['units']:
                binding = bindings.get(uid, {})
                key = binding.get('step'), binding.get('role')
                if key != (task['step'], task['role']):
                    raise ValueError('assignment has no matching original binding')
                scope = binding.get('products', set())
                if not scope or not scope <= set(task['products']):
                    raise ValueError('assignment has no valid original scope')
            if task['role'] == 'migration':
                migrations[task['step']] = set(task['products'])
        affected = {}
        old_items = {d['product']:d for d in old['decisions']}
        for decision in plan['decisions']:
            before = old_items.get(decision['product'], {})
            fields = ('action','owner','goal')
            changed = any(
                before.get(k) != decision[k] for k in fields)
            scope = paths.get(decision['product'], set())
            scope = scope | paths.get(decision['owner'], set())
            covered = set()
            for step in decision['steps']:
                assigned = scope & migrations[step]
                covered.update(assigned)
                reset = changed or step not in before.get('steps', [])
                for path in assigned:
                    key = decision["product"], step, path
                    affected[key] = unit if reset else obligations.get(key, unit)
            if decision['steps'] and (not scope or scope - covered):
                raise ValueError('migration omits its responsibility scope')
        obligations, previous = affected, state
    selected = (task['units'] for task in states[-1]['plan']['tasks'])
    current = {uid:bindings[uid]
               for group in selected for uid in group}
    required = reconstruction_authorities(obligations, facts)
    chronology = reconstruction_chronology(revisions, facts, required, current)
    return dict(assignments=models[-1], revisions=revisions,
        obligations=required, routes=routes, edges=edges,
        bindings=current, chronology=chronology)

def reconstruction_authorities(obligations, facts):
    """Project each responsibility onto its latest shared execution requirement."""
    result = {}
    for (_, step, path), authority in obligations.items():
        key = step, path
        before = result.get(key, authority)
        later = facts[authority]['position'] > facts[before]['position']
        result[key] = authority if later else before
    return result


def reconstruction_replacements(history, facts, blocks, proof=None):
    """Discharge retained omissions through authorized current descendants."""
    from policy import replacement_chain
    current, edges = history['bindings'], history['edges']
    statuses = {uid:status for uid, status, _, _ in blocks}
    chains = {uid:set(replacement_chain(blocks, [uid])) for uid in current}
    def follow(origin, node, path, role, seen):
        if node in seen:
            raise ValueError('replacement routing contains a cycle')
        reached = set()
        if node in current:
            binding = current[node]
            valid = binding['role'] == role
            valid = valid and path in binding['products']
            valid = valid and origin in chains[node]
            reached = {node} if valid else set()
        for edge in edges:
            if edge['unit'] != node or edge['role'] != role:
                continue
            if path not in edge['products']:
                continue
            for target, scopes in edge['coverage'].items():
                if path in scopes[0] and path in scopes[1]:
                    reached.update(follow(
                        origin, target, path, role, seen | {node}))
        return reached
    pending, deferred = set(), set()
    for edge in edges:
        for path in edge['products']:
            origin, role = edge['unit'], edge['role']
            targets = follow(origin, origin, path, role, set())
            closed, waiting = False, False
            for uid in targets:
                fact = facts.get(uid, {})
                valid = fact.get('status') == 'closed'
                valid = valid and fact.get('verdict') == 'pass'
                valid = valid and fact.get('kind') != 'audit'
                valid = valid and not fact.get('planning')
                actual = fact.get('products', set())
                scope = current[uid]['products']
                closed |= valid and path in actual and actual <= scope
                nonfinal = statuses.get(uid) in {'planned','open','waiting'}
                known = nonfinal and not fact
                waiting |= uid == proof and role == 'proof' and known
            if not closed:
                key = origin, path
                if waiting:
                    deferred.add(key)
                else:
                    pending.add(key)
    return dict(pending=pending, deferred=deferred)


def reconstruction_proof(evidence, record, task):
    """Validate explicit proof evidence without inventing committed execution."""
    fields = {'window', 'revision', 'task', 'outcome'}
    if type(evidence) is not dict or set(evidence) != fields:
        raise ValueError('proof has unexpected fields')
    for key in ('window', 'revision'):
        if evidence[key] != record[key]:
            raise ValueError('proof names another reconstruction')
    if evidence['task'] != task:
        raise ValueError('proof names another assigned task')
    outcome = evidence['outcome']
    if not isinstance(outcome, str) or not outcome.strip():
        raise ValueError('proof needs a concrete outcome')
    return outcome


def reconstruction_phase(context, evidence=None):
    """Compose readiness from retained obligations and verified execution."""
    from reconstruction import reconstruction_execution, reconstruction_assigned
    history = reconstruction_history(context)
    result = dict(phase='incomplete', history=history)
    assignments = history['assignments']
    facts, states = context['facts'], context['states']
    statuses = {row[0]:row[1]
                for row in context['blocks']}
    roles = ('research', 'characterization', 'migration')
    work = [u for role in roles
            for u in assignments[role]]
    for uid in work + assignments['proof']:
        status = statuses.get(uid)
        if status not in {'planned','open','waiting','closed','failed'}:
            raise ValueError('assigned work has unknown current status')
        if status in {'closed', 'failed'} or uid in facts:
            if facts.get(uid, {}).get('status') != status:
                raise ValueError('final work has missing or contradictory evidence')
    if not reconstruction_assigned(assignments):
        return result
    proof = assignments['proof'][0]
    unfinished = any(statuses[u] != 'closed' for u in work)
    if unfinished or statuses[proof] == 'failed':
        return result
    design, revision = states[0]['unit'], states[-1]['unit']
    reconstruction_execution(assignments, facts, design, revision, False)
    if history['chronology']['pending']:
        return result
    omissions = reconstruction_replacements(
        history, facts, context['blocks'], proof)
    if omissions['pending']:
        return result
    status = statuses[proof]
    if status in {'planned','open','waiting'}:
        result['phase'] = 'proof-ready'
        return result
    reconstruction_execution(assignments, facts, design, revision)
    if omissions['deferred']:
        raise ValueError('completed proof retains deferred obligations')
    record = context['record']
    task = history['bindings'][proof]['step']
    reconstruction_proof(evidence, record, task)
    if 'design' in record:
        if record['design'] != design or record['proof'] != proof:
            raise ValueError('receipt names unrelated authority or proof')
        if set(record['migrations']) != set(assignments['migration']):
            raise ValueError('receipt migrations differ from assignments')
    result['phase'] = 'receipt-ready'
    return result
