#!/usr/bin/env python3
"""hooks/install.py [--home DIR] [--roots DIR...] — install the three gates: the Claude Code hooks into HOME/.claude/settings.json,
the Codex hooks into HOME/.codex/config.toml, the pre-commit into .git/hooks of every room under the roots. Idempotent. Prints configured counts."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from gate import ROOMS
CLAUDE = os.path.join(HERE, 'claude.py')
CODEX = os.path.join(HERE, 'codex.py')
PRE = os.path.join(HERE, 'pre-commit')


def claude_hooks(path):
    """One command hook per event, keyed by our script path, replacing an older copy of itself."""
    d = json.load(open(path, encoding='utf8')) if os.path.exists(path) else {}
    hooks = d.setdefault('hooks', {})
    for event, matcher in (('PreToolUse', 'Edit|Write|MultiEdit|NotebookEdit|Bash|WebSearch|WebFetch|Agent'), ('PostToolUse', 'Edit|Write|MultiEdit|NotebookEdit|Bash'), ('Stop', None)):
        groups = [g for g in hooks.get(event, []) if not any(CLAUDE in h.get('command', '') for h in g.get('hooks', []))]
        group = {'hooks': [{'type': 'command', 'command': f'python3 -I -B {CLAUDE}', 'timeout': 60}]}
        if matcher:
            group['matcher'] = matcher
        hooks[event] = groups + [group]
    json.dump(d, open(path, 'w', encoding='utf8'), indent=2, ensure_ascii=False)
    return 3


def codex_hooks(path):
    """Add missing events inside our block. Preserve existing definitions and trust."""
    text = open(path, encoding='utf8').read() if os.path.exists(path) else ''
    found = re.search(r'(?m)^# hectoline hooks begin\n[\s\S]*?^# hectoline hooks end(?:\n|$)', text)
    block = found[0] if found else '# hectoline hooks begin\n# hectoline hooks end\n'
    for event in ('PreToolUse', 'PostToolUse', 'Stop'):
        if re.search(r'^\[\[hooks\.' + event + r'\]\]$', block, re.M):
            continue
        group = f'[[hooks.{event}]]\n'
        if event != 'Stop':
            group += 'matcher = "Bash|apply_patch|Edit|Write|Agent"\n'
        group += f'[[hooks.{event}.hooks]]\ntype = "command"\ncommand = "python3 -I -B {CODEX}"\ntimeout = 60\n'
        block = block.replace('# hectoline hooks end', group + '# hectoline hooks end')
    updated = text[:found.start()] + block + text[found.end():] if found else text + ('\n' if text and not text.endswith('\n') else '') + block
    if updated != text:
        open(path, 'w', encoding='utf8').write(updated)
    return 3


def rooms(roots):
    for root in roots:
        for d, dirs, files in os.walk(root):
            if '.git' in dirs and 'RULE.md' in files and 'UNITS.md' in files:
                yield d
            dirs[:] = [x for x in dirs if x not in ('.git', 'node_modules', '_archive', '_legacy')]


def pre_commit(room):
    target = os.path.join(room, '.git', 'hooks', 'pre-commit')
    if os.path.islink(target) or os.path.exists(target):
        os.remove(target)
    os.symlink(PRE, target)
    return 1


def main(argv):
    home = argv[argv.index('--home') + 1] if '--home' in argv else os.path.expanduser('~')
    roots = argv[argv.index('--roots') + 1:] if '--roots' in argv else [ROOMS]
    n = claude_hooks(os.path.join(home, '.claude', 'settings.json')) + codex_hooks(os.path.join(home, '.codex', 'config.toml'))
    done = [pre_commit(r) for r in rooms(roots)]
    print(f'configured: {n} agent hook definitions, {sum(done)} pre-commit hooks in {len(done)} rooms · review new Codex definitions with /hooks')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
