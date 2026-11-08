"""Pure admission decisions from explicit ledger and measurement inputs."""
import re
from decimal import Decimal, InvalidOperation

def review_decision(record, check_failures=0):
    """Return the review verdict and the irreversible failure count."""
    rounds = {}
    for number, verdict, _ in record['rounds']:
        if number > 0:
            rounds.setdefault(number, set()).add(verdict)
    failures = sum('fail' in values for values in rounds.values())
    failures += check_failures
    if failures >= 3:
        return 'limit', failures
    if record['withdrawn']:
        return 'withdrawn', failures
    if not record['valid'] or not rounds:
        return 'unknown', failures
    if any(len(values) != 1 for values in rounds.values()):
        return 'unknown', failures
    if max(rounds) != len(rounds):
        return 'unknown', failures
    latest = rounds[max(rounds)]
    return next(iter(latest)), failures



def binary(sample):
    """Use Git's null-byte test on the first 8000 bytes."""
    return b'\0' in sample[:8000]


def step_request(vals, steps, goals, marker):
    """Return a metadata error or the leaf whose value admission needs."""
    plan = vals.get('plan', '')
    if 'S none' in plan:
        return '', None
    step = re.search(r'\bS\d+\b', plan)
    row = next((r for r in steps if step and r[0] == step.group()), None)
    if not row:
        return 'plan names no existing step', None
    if row[1] not in {g[0] for g in goals}:
        return f'{row[0]} names no existing goal', None
    leaves = {row[1]}
    if row[1] == 'G0':
        for _ in goals:
            leaves.update(g[0] for g in goals if g[2] in leaves)
        leaves -= {g[2] for g in goals} | {'G0'}
    if marker and int(row[0][1:]) >= int(marker[1]) and not any(re.search(rf'\b{g}\b.* from .* to ', row[3]) for g in leaves):
        return f'{row[0]} names no leaf move in its text, RULE §2', None
    return '', row[1] if row[1] != 'G0' and 'measure' not in row[2] + row[3] else None


def measurement_missing(value):
    """Recognize unavailable measurements before admission or target checks."""
    import math
    if isinstance(value, str):
        pattern = r'\b(?:no|not|unknown|unmeasured|pending|stale|error|nan|inf|infinity|none|null)\b'
        found = re.search(pattern, value, re.I)
        return not value.strip() or bool(found)
    if type(value) is float:
        return not math.isfinite(value)
    return type(value) is not int


def measurement_error(leaf, value):
    if not measurement_missing(value):
        return ''
    return f'{leaf} is unmeasured, only its measure step opens under it, RULE §1'


def blocked_leaves(steps, bl, values):
    """Return leaves only when all pending work lacks measurements."""
    out = set()
    for _, status, _, vals in bl:
        if status != 'planned':
            continue
        match = re.search(r'\bS\d+\b', vals.get('plan', ''))
        row = steps.get(match.group()) if match else None
        if not row or row[1] == 'G0':
            return set()
        if 'measure' in row[2] + row[3]:
            return set()
        if not measurement_missing(values.get(row[1])):
            return set()
        out.add(row[1])
    return out


REPAIR_FILES = {'OWNER.md', 'PLAN.md', 'UNITS.md'}


def repair_candidates(bl, since, paths):
    """Return base-ready candidates only inside the ledger-repair boundary."""
    if since >= 10 or any(s in ('open', 'waiting') for _, s, _, _ in bl):
        return []
    if set(paths) != REPAIR_FILES:
        return []
    final = {u for u, s, _, _ in bl if s in ('closed', 'failed')}
    return [v for _, s, _, v in bl if s == 'planned' and v['base'].split()[0] in final]


def repair_invariant(old, prior, uid, bl, paths, changed):
    """Preserve earlier blocks and restrict this transaction to its ledgers."""
    if not old or prior != old.rstrip() or bl[-1][0] != uid:
        return 'queue repair changed an earlier block or added another block'
    if set(paths) != REPAIR_FILES:
        return 'queue repair owns OWNER.md, PLAN.md and UNITS.md only'
    if set(changed) - REPAIR_FILES - {'unit.log', ''}:
        return 'queue repair changed a product path'
    return ''


NUMBER = r'[+-]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?'


def quantity(text):
    match = re.fullmatch(rf'({NUMBER})(?:\.\.({NUMBER}))?(?:\s+(.+))?', text.strip())
    if not match:
        return None
    try: lo, hi = (Decimal(x.replace(',', '')) for x in (match[1], match[2] or match[1]))
    except InvalidOperation: return None
    if not all(x.is_finite() for x in (lo, hi)) or lo > hi:
        return None
    return lo, hi, (match[3] or '').strip().replace('percent', '%')


def at_target(value, target):
    """Accept explicit numeric or coverage targets. Every value in an interval must pass."""
    if measurement_missing(value) or not isinstance(target, str):
        return False
    value, target = str(value).strip(), target.strip()
    parts, observed = target.split(' · '), value.split(' · ')
    if len(parts) > 1:
        return len(parts) == len(observed) and all(at_target(v, t) for v, t in zip(observed, parts))
    fraction = r'(?:(\w[\w -]*?) )?(\d+) of (\d+)(?: (.+))?'
    found, expected = re.fullmatch(fraction, value), re.fullmatch(fraction, target)
    if re.fullmatch(r'N of N(?:, .+)?', target):
        return bool(found and not found[1] and int(found[2]) == int(found[3]) > 0)
    if expected:
        return bool(found and 0 <= int(found[2]) <= int(found[3]) and int(found[3]) > 0 and found.groups()[:3] == expected.groups()[:3]
                    and (not found[4] or found[4] == expected[4]))
    match = re.fullmatch(r'(≤|≥|<=|>=|<|>|=)?\s*(.+)', target)
    limit = quantity(match[2]) if match else None
    if not limit or limit[0] != limit[1]:
        return False
    if match[1] and value == target:
        return True  # Existing qualified readers return their explicit target after validation.
    actual = quantity(value)
    if not actual or actual[2] and actual[2] != limit[2]:
        return False
    lo, hi, _ = actual
    point = limit[0]
    return {'≥': lo >= point, '>=': lo >= point, '≤': hi <= point, '<=': hi <= point,
            '>': lo > point, '<': hi < point, '=': lo == hi == point, None: lo == hi == point}[match[1]]


def leaf_goals(goals):
    parents = {g[2] for g in goals}
    return [g for g in goals if g[0] != 'G0' and g[0] not in parents]

