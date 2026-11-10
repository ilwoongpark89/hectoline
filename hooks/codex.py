#!/usr/bin/env python3
"""Codex tool checks and Stop pile feedback use their event-specific contracts."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from gate import WRITES, legacy_room, legacy_writes, ROOMS
from gate import review_calls
from ledger import read
from hooks.install import rooms
WORKSPACE = ROOMS

PATCH_PATH = re.compile(r'^\s*\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$', re.M)


def room_of(path):
    probe = path
    while not os.path.isdir(probe):  # a new file, or a new folder under the room
        probe = os.path.dirname(probe) or '.'
    root = subprocess.run(['git', '-C', probe, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    return root if root and os.path.exists(os.path.join(root, 'RULE.md')) and os.path.exists(os.path.join(root, 'UNITS.md')) else ''


def payloads(payload, cwd):
    """One check payload per touched path, each with an absolute file_path: an apply_patch splits into Edit payloads, a shell command into one payload per write target, other tools pass as is."""
    if payload.get('tool_name') in ('shell', 'Bash'):  # the write targets of the command, each resolved against cwd, so every room checks its own, S40
        paths = [p for m in WRITES.findall(payload.get('tool_input', {}).get('command', '')) for p in m.split() if re.search(r'\.(md|py|json|toml)$|\.git/hooks', p)]
        return [payload] + [dict(payload, tool_name='Bash', tool_input=dict(payload.get('tool_input', {}), file_path=os.path.realpath(os.path.join(cwd, os.path.expanduser(p))))) for p in paths]  + [dict(payload, tool_name='Write', tool_input={'file_path': p}) for _, p in legacy_writes(payload.get('tool_input', {}).get('command', ''), cwd)]  # any file type under a legacy target, S118  # the command itself first, so the Bash gates of check run
    if payload.get('tool_name') != 'apply_patch':
        return [payload]
    paths = [os.path.realpath(os.path.join(cwd, p.strip())) for p in PATCH_PATH.findall(payload.get('tool_input', {}).get('command', ''))]
    return [dict(payload, tool_name='Edit', tool_input={'file_path': p}) for p in paths]


def deny(event, reason):
    if event == 'PreToolUse':
        output = {'hookSpecificOutput': {'hookEventName': event, 'permissionDecision': 'deny', 'permissionDecisionReason': reason}}
    else:
        output = {'decision': 'block', 'reason': reason}
    print(json.dumps(output))
    return 0


def checked(room, one):
    """The refusal of one room for one call, empty when the room allows."""
    tool = os.path.join(room, 'unit.py')
    args = [sys.executable, '-I', '-B', tool, 'check', room]
    quiet = dict(capture_output=True, text=True)
    done = subprocess.run(args, input=json.dumps(one), **quiet)
    return done.stdout.strip() if done.returncode else ''


def stop_rooms(cwd, session):
    """Use the current room or rooms already recorded for this workspace session."""
    room = room_of(cwd)
    if room:
        return [room]
    if os.path.realpath(cwd) != os.path.realpath(WORKSPACE) or not session:
        return []
    roots = [os.path.join(WORKSPACE, d) for d in sorted(os.listdir(WORKSPACE))
             if re.match(r'^\d\d_', d) and os.path.isdir(os.path.join(WORKSPACE, d)) and not os.path.islink(os.path.join(WORKSPACE, d))]
    return [r for r in rooms(roots) if any(line.endswith(' | ' + session) for line in read(os.path.join(r, 'unit.log')).splitlines())]


def main():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    event = payload.get('hook_event_name')
    cwd = payload.get('cwd') or os.getcwd()
    if event == 'Stop':
        for room in stop_rooms(cwd, payload.get('session_id', '')):
            res = subprocess.run([sys.executable, '-I', '-B', os.path.join(room, 'unit.py'), 'pile', room], capture_output=True, text=True)
            if res.returncode:
                return deny(event, room + ': ' + (res.stdout.strip() or 'Work gate could not verify the room pile'))
        return 0
    if event not in ('PreToolUse', 'PostToolUse'):
        return 0
    ones = payloads(payload, cwd)
    if not ones and room_of(cwd) and payload.get('tool_name') == 'apply_patch':
        return deny(event, 'deny: apply_patch names no file')
    routed = []
    for one in ones:
        routed += review_calls(one, cwd)
    for room, call in routed:
        flaw = checked(room, call)
        if flaw:
            return deny(event, flaw)
    for one in ones:
        fp = one.get('tool_input', {}).get('file_path'); room = room_of(fp or cwd) or (fp and legacy_room(fp))
        if not room:
            continue
        res = subprocess.run([sys.executable, '-I', '-B', os.path.join(room, 'unit.py'), 'check', room], input=json.dumps(one), capture_output=True, text=True)
        if res.returncode:
            return deny(event, res.stdout.strip() or 'deny: unit.py check failed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
