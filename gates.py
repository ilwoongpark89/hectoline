"""gates.py — the gate list of hectoline. `gates.py [ROOM ...]` prints every refusal site of the tool code
with the count of its text in the deny lines of the room logs: the numbered rooms under ROOMS, each ROOM given."""
import ast
import os
import sys
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
from gate import numbered_rooms
from lines import read


def kind(node):
    """The refusal kind of one statement, or empty."""
    value = getattr(node, 'value', None)
    call = getattr(node, 'exc', value)
    name = getattr(getattr(call, 'func', None), 'id', '')
    if isinstance(node, ast.Raise):
        return 'raise' if name in ('ValueError', 'RuntimeError') else ''
    if not isinstance(node, ast.Return):
        return ''
    if isinstance(value, ast.Tuple):
        first = value.elts[:1]
        head = ast.dump(first[0]) if first else ''
        return 'deny' if 'value=False' in head else ''
    return 'refuse' if name in ('refuse', 'fail') else ''


def fragment(node):
    """The longest literal text of a statement."""
    texts = ['']
    for part in ast.walk(node):
        text = getattr(part, 'value', None)
        if isinstance(part, ast.Constant) and isinstance(text, str):
            texts.append(text)
    return max(texts, key=len)


def sites():
    """Every refusal site of the tool code as file, line, kind, text."""
    out = []
    names = [n for n in os.listdir(HERE) if n.endswith('.py')]
    hooks = os.listdir(os.path.join(HERE, 'hooks'))
    names += ['hooks/' + n for n in hooks if n.endswith('.py')]
    for name in sorted(names) + ['hooks/pre-commit']:
        if name.startswith('selftest'):
            continue
        tree = ast.parse(read(os.path.join(HERE, name)))
        for node in ast.walk(tree):
            if kind(node):
                row = name, node.lineno, kind(node), fragment(node)
                out.append(row)
    return sorted(out)


def denies(more):
    """The reasons of the deny lines of the room logs."""
    out = []
    for room in numbered_rooms(ledger=True) + list(more):
        path = os.path.join(room, 'unit.log')
        for line in read(path).splitlines():
            cells = line.split(' | ')
            if len(cells) > 4 and cells[3] == 'deny':
                out.append(cells[4])
    return out


def main(argv):
    reasons = denies(argv)
    rows = sites()
    silent = 0
    for name, line, found, text in rows:
        hits = [r for r in reasons if text in r]
        fired = len(hits) if len(text) > 7 else 0
        silent += not fired
        print(f'{name}:{line} · {found} · {fired} · {text[:60]}')
    raises = [row for row in rows if row[2] == 'raise']
    total = f'gates: {len(rows)} sites · {silent} with no deny line, {len(raises)} raise sites reach no log'
    print(total + f' · {len(reasons)} deny lines')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
