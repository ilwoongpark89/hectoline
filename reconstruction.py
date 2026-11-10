"""Pure reconstruction decisions from explicit evidence."""
import re
IDENTITY_FIELDS = ('version', 'window', 'baseline', 'revision')

def reconstruction_decisions(decisions, before, after, goals, sources, steps):
    """Validate decisions against maps of active product responsibilities."""
    keys = {'product', 'action', 'goal', 'evidence', 'before', 'owner', 'steps'}
    actions = {'keep', 'merge', 'move', 'remove', 'split'}
    products = set(before) | set(after)
    if type(decisions) is not list:
        raise ValueError('product decisions must be a list')
    seen = set()
    required = set()
    for decision in decisions:
        if type(decision) is not dict or set(decision) != keys:
            raise ValueError('unexpected product decision fields')
        for key in ('product', 'action', 'goal', 'before', 'owner'):
            value = decision[key]
            if not isinstance(value, str) or not value.strip():
                raise ValueError('product decision needs text')
        product = decision['product']
        if product not in products or product in seen:
            raise ValueError('unknown or repeated product decision')
        seen.add(product)
        if decision['before'] != before.get(product, 'new'):
            raise ValueError('previous responsibility does not match its source')
        action = decision['action']
        goal = decision['goal']
        if action not in actions or goal not in goals:
            raise ValueError('unknown action or goal')
        owner = decision['owner']
        retained = before.get(product) == after.get(product)
        if action == 'keep' and (owner != product or not retained):
            raise ValueError('retention cannot transfer responsibility')
        removed = action == 'remove'
        if removed and (owner != 'none' or product in after):
            raise ValueError('removal must retire the active responsibility')
        if not removed and owner not in after:
            raise ValueError('resulting responsibility has no owner')
        for key, choices in (('evidence', sources), ('steps', steps)):
            values = decision[key]
            if type(values) is not list:
                raise ValueError('decision references must be lists')
            for value in values:
                if not isinstance(value, str) or value not in choices:
                    raise ValueError('decision reference has no source')
            if len(set(values)) != len(values):
                raise ValueError('decision repeats a reference')
        if not decision['evidence']:
            raise ValueError('product decision has no evidence')
        if action != 'keep' and not decision['steps']:
            raise ValueError('structural change has no migration step')
        required.update(decision['steps'])
    if seen != products:
        raise ValueError('product decisions do not cover the whole product')
    return required


def reconstruction_identity(record, windows):
    """Validate source identity without requiring completion roles."""
    required = set(IDENTITY_FIELDS)
    if type(record) is not dict or set(record) != required:
        raise ValueError('unexpected reconstruction identity fields')
    version = record['version']
    if type(version) is not int or version != 1:
        raise ValueError('unsupported reconstruction version')
    pair = record['window']
    endpoints = [[group[0], group[-1]] for group in windows]
    valid_window = type(pair) is list and pair in endpoints
    if not valid_window:
        raise ValueError('identity does not name one exact window')
    for field in ('baseline', 'revision'):
        value = record[field]
        if not isinstance(value, str):
            raise ValueError('commit must be text')
        if not re.fullmatch(r'[0-9a-f]{40}', value):
            raise ValueError('commit must have its complete identity')
    return tuple(pair)


def reconstruction_receipt(record, windows):
    """Validate completion roles after the shared source identity."""
    required = set(IDENTITY_FIELDS) | {'design', 'migrations', 'proof'}
    if type(record) is not dict or set(record) != required:
        raise ValueError('unexpected receipt fields')
    identity = {key: record[key] for key in IDENTITY_FIELDS}
    window = reconstruction_identity(identity, windows)
    units = record['migrations']
    if type(units) is not list:
        raise ValueError('migrations must be a list')
    roles = [record['design'], *units, record['proof']]
    for uid in roles:
        valid = isinstance(uid, str)
        if not valid or not re.fullmatch(r'U\d{4}', uid):
            raise ValueError('role must name a unit')
    if len(set(roles)) != len(roles):
        raise ValueError('receipt roles must be distinct')
    return window


def reconstruction_windows(blocks, kinds, order):
    """Build disjoint windows in committed finalization order."""
    final = set()
    previous = ''
    statuses = {'planned', 'open', 'waiting', 'closed', 'failed'}
    allowed = {'structural', 'behavioral', 'redesign', 'audit'}
    for uid, status, _, _ in blocks:
        if not re.fullmatch(r'U\d{4}', uid) or uid <= previous:
            raise ValueError('ambiguous unit order')
        previous = uid
        known = status in statuses and kinds.get(uid) in allowed
        if not known:
            raise ValueError('unknown unit state or type')
        if status in ('closed', 'failed'):
            final.add(uid)
    if type(order) is not dict or set(order) != final:
        raise ValueError('finalization order does not cover final units')
    work = []
    for uid, record in order.items():
        if record['kind'] != kinds[uid]:
            raise ValueError('unit type differs from its finalization')
        if kinds[uid] != 'audit':
            work.append(uid)
    windows = []
    for start in range(0, len(work) - 99, 100):
        windows.append(tuple(work[start:start + 100]))
    return windows


def reconstruction_tasks(tasks, steps, units, required):
    """Validate assignments while retaining every unassigned obligation."""
    roles = {'research', 'characterization', 'migration', 'proof'}
    if type(tasks) is not list:
        raise ValueError('reconstruction tasks must be a list')
    seen, assigned, covered, pending = set(), set(), set(), set()
    work = {role: [] for role in roles}
    proof_steps = set()
    for task in tasks:
        keys = {'step', 'role', 'products', 'units'}
        if type(task) is not dict or set(task) != keys:
            raise ValueError('unexpected reconstruction task fields')
        step, role = task['step'], task['role']
        if not isinstance(step, str) or not isinstance(role, str):
            raise ValueError('task ownership needs text')
        if step not in steps or role not in roles:
            raise ValueError('unknown task step or role')
        if (step, role) in seen:
            raise ValueError('duplicate task responsibility')
        seen.add((step, role))
        scope = steps[step]
        paths = task['products']
        if type(paths) is not list or not paths:
            raise ValueError('task needs product paths')
        for path in paths:
            known = isinstance(path, str)
            if not known or path not in scope['products']:
                raise ValueError('task exceeds its step product scope')
        if len(set(paths)) != len(paths):
            raise ValueError('task repeats a product path')
        selected = task['units']
        if type(selected) is not list:
            raise ValueError('task assignments must be a list')
        if not selected:
            pending.add((step, role))
        target = work[role]
        if role == 'proof':
            proof_steps.add(step)
        elif role == 'migration':
            covered.add(step)
        for uid in selected:
            if not isinstance(uid, str) or units.get(uid) != step:
                raise ValueError('unit does not belong to its task step')
            if uid in assigned or uid not in scope['units']:
                raise ValueError('unit assignment is repeated or undeclared')
            assigned.add(uid)
            target.append(uid)
    if required - covered:
        raise ValueError('a product decision has no execution task')
    if len(proof_steps) != 1 or len(work['proof']) > 1:
        raise ValueError('reconstruction needs one proof task')
    return dict(work, unassigned=pending)


def reconstruction_assigned(assignments):
    """Require every obligation and exactly one proof assignment."""
    return not assignments['unassigned'] and len(assignments['proof']) == 1


def reconstruction_execution(assignments, facts, design, revision, require_proof=True):
    """Use one prerequisite policy before proof and at completion."""
    if type(require_proof) is not bool:
        raise ValueError('proof mode must be a boolean')
    if not reconstruction_assigned(assignments):
        raise ValueError('reconstruction has unassigned obligations')
    proof = assignments['proof'][0]
    work = []
    for role in ('research', 'characterization', 'migration'):
        work.extend(assignments[role])
    required = [design, revision, *work]
    if require_proof:
        required.append(proof)
    for uid in required:
        if uid not in facts:
            raise ValueError('assigned unit has no verified artifact')
        fact = facts[uid]
        if fact['status'] != 'closed' or fact['verdict'] != 'pass':
            raise ValueError('assigned work lacks reviewed closure')
        if fact['kind'] == 'audit':
            raise ValueError('discovery audit cannot replace required work')
        position = fact['position']
        if type(position) is not int or position < 0:
            raise ValueError('unit position is invalid')
    initial, frozen = facts[design], facts[revision]
    if not initial['planning'] or not frozen['planning']:
        raise ValueError('design and revision need reviewed planning')
    first = initial['position']
    if first > frozen['position']:
        raise ValueError('frozen assignments must follow design')
    for uid in assignments['migration']:
        if facts[uid]['position'] <= first:
            raise ValueError('migration must follow design')
    if not require_proof:
        return proof
    last = facts[proof]['position']
    if frozen['position'] >= last:
        raise ValueError('proof must follow design and frozen assignments')
    for uid in work:
        if facts[uid]['position'] >= last:
            raise ValueError('required work must precede proof')
    return proof


def reconstruction_models(context):
    """Validate every frozen model against its own source catalog."""
    record = context['record']
    identity = {key: record[key] for key in IDENTITY_FIELDS}
    window = reconstruction_identity(identity, context['windows'])
    states = context['states']
    if not states or states[-1]['commit'] != record['revision']:
        raise ValueError('model history has no exact frozen endpoint')
    if 'design' in record and states[0]['unit'] != record['design']:
        raise ValueError('receipt design differs from initial authority')
    baseline = context['baseline']
    before = {row[0]: row[1] for row in baseline['blocks']}
    windows = {group[0]: group for group in context['windows']}
    for uid in windows[window[0]]:
        if before.get(uid) not in {'closed', 'failed'}:
            raise ValueError('baseline precedes its complete window')
    expected = dict(identity)
    del expected['revision']
    models, active = [], False
    for index, state in enumerate(states):
        plan, catalog = state['plan'], state['catalog']
        models.append(reconstruction_model(
            plan, baseline, catalog, expected, index == 0, active))
        active = active or plan['enforce']
    return models


def reconstruction_model(plan, baseline, catalog, expected, initial, active):
    """Validate one proposed model from validated identity and source catalogs."""
    modes = type(initial) is bool and type(active) is bool
    if not modes:
        raise ValueError('model history modes must be booleans')
    fields = {'version', 'window', 'baseline', 'decisions', 'tasks', 'enforce'}
    widest = fields | {'amendments', 'start'}
    valid = type(plan) is dict
    if not valid or not fields <= set(plan) <= widest:
        raise ValueError('unexpected reconstruction model fields')
    typed = type(plan['version']) is int
    typed = typed and type(plan['enforce']) is bool
    if not typed:
        raise ValueError('model version and activation need exact types')
    actual = {key: plan[key] for key in expected}
    if actual != expected:
        raise ValueError('model changes its frozen source identity')
    amendments = plan.get('amendments', [])
    if type(amendments) is not list:
        raise ValueError('model amendments must be a list')
    if initial and amendments:
        raise ValueError('model has invalid initial amendment evidence')
    if active and not plan['enforce']:
        raise ValueError('model cannot disable activated reconstruction')
    needed = reconstruction_decisions(
        plan['decisions'], baseline['products'], catalog['products'],
        catalog['goals'], catalog['sources'], catalog['steps'])
    return reconstruction_tasks(
        plan['tasks'], catalog['steps'], catalog['units'], needed)
