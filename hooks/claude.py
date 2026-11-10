#!/usr/bin/env python3
"""hooks/claude.py — Claude Code hook for PreToolUse, PostToolUse, Stop. Reads the hook JSON on stdin, finds the room, calls unit.py check, exits 2 to deny.
Outside a room, a folder whose git root holds no RULE.md and UNITS.md, every call allows."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from gate import WRITES, legacy_room, legacy_writes
from gate import review_calls


def room_of(path):
    """The git root above path when it holds RULE.md and UNITS.md, else ''."""
    probe = path if os.path.isdir(path) else os.path.dirname(path) or '.'
    while not os.path.isdir(probe):  # a new file, or a new folder under the room
        probe = os.path.dirname(probe) or '.'
    root = subprocess.run(['git', '-C', probe, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    return root if root and os.path.exists(os.path.join(root, 'RULE.md')) and os.path.exists(os.path.join(root, 'UNITS.md')) else ''


def rooms_of(payload, cwd):
    """The rooms a call touches: the file_path's room, or for a shell command the room of every write target resolved against cwd, S40."""
    inp = payload.get('tool_input', {})
    if payload.get('tool_name') not in ('Bash', 'shell'):
        return [r for r in [room_of(inp.get('file_path') or cwd) or (inp.get('file_path') and legacy_room(inp['file_path']))] if r]
    paths = [p for m in WRITES.findall(inp.get('command', '')) for p in m.split() if re.search(r'\.(md|py|json|toml)$|\.git/hooks', p)]
    return sorted({r for r in [room_of(cwd)] + [room_of(os.path.realpath(os.path.join(cwd, os.path.expanduser(p)))) or legacy_room(os.path.join(cwd, os.path.expanduser(p))) for p in paths] if r})  # the cwd room stays, its Bash gates run on every command


def main():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    event = payload.get('hook_event_name', '')
    cwd = payload.get('cwd') or os.getcwd()
    room = room_of(cwd)
    if event == 'Stop' and not room:
        return 0
    if event == 'Stop':
        pile = subprocess.run([sys.executable, '-I', '-B', os.path.join(room, 'unit.py'), 'pile', room], capture_output=True, text=True)
        if pile.returncode:
            print((pile.stdout.strip().splitlines() or ['pile: unit.py pile failed'])[-1], file=sys.stderr)
            return 2
        return 0
    if event in ('PreToolUse', 'PostToolUse') and payload.get('tool_name') in ('Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'Bash', 'WebSearch', 'WebFetch', 'Agent'):
        writes = [(r, dict(payload, tool_name='Write', tool_input={'file_path': p})) for r, p in (legacy_writes(payload.get('tool_input', {}).get('command', ''), cwd) if payload.get('tool_name') == 'Bash' else [])]  # a shell write of any file type under a legacy target meets that room's gate as a Write, S118
        writes += review_calls(payload, cwd)
        for room, one in [(r, payload) for r in rooms_of(payload, cwd)] + writes:  # each room checks its own targets, a call that touches no room passes
            res = subprocess.run([sys.executable, '-I', '-B', os.path.join(room, 'unit.py'), 'check', room], input=json.dumps(one), capture_output=True, text=True)
            if res.returncode:
                print(res.stdout.strip(), file=sys.stderr)
                return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
