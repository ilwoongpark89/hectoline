"""selftest.py — the gate selftest of a hectoline room, P17. `python3 -I -B unit.py selftest ROOM` imports it. It replays every deny case of check on a scratch copy of the room, S85. The redesign of U0130: the total is counted, never typed, and the copy's own state cannot fail a case."""
import os, re, sys
from unit import check, close_unit
from selftest_flow import settled_open as open_unit
from pile import line_map, pile_count, pile_paths
from gate import owners
from gate import HOME
from ledger import read, validate_units, files_of, load, log
from ledger import set_key, set_status, write


def queue_step_checks(repair=False):
    """Exercise planning close and pilot eligibility on a disposable room."""
    import contextlib, io, subprocess, tempfile
    from unittest.mock import patch
    import base, room as maker, unit
    with tempfile.TemporaryDirectory() as folder:
        texts = maker.ledgers('99_probe', 'A measured pilot', 'fixture', '')
        texts['GOAL.md'] += '| G1 | child | G0 | count | 2 | 0 |\n'
        texts['PLAN.md'] += '## rule 1.1 from S2\n| S2 | G1 | x.md | missing movement | x · y | U0003 | todo |\n'
        for name, text in texts.items():
            open(os.path.join(folder, name), 'w').write(text)
        run = lambda *args: subprocess.run(['git', '-C', folder, *args], capture_output=True, check=True)
        run('init', '-q')
        run('add', '.')
        run('-c', 'user.name=fixture', '-c', 'user.email=fixture@local', 'commit', '-qm', 'U0001 fixture')
        run('config', 'user.name', 'fixture')
        run('config', 'user.email', 'fixture@local')
        open(os.path.join(folder, 'x.md'), 'w').write('fixture\n')
        seed = load(folder)[1][0][3]
        for uid, status, plan in [('U0002', 'open', 'A0001 · S none'), ('U0003', 'planned', 'A0001 · S2')]:
            vals = dict(seed, sentence='plan the pilot', plan=plan, base='U0001', files='UNITS.md · PLAN.md · x.md', check='test -f x.md', review='pass agent-review-fixture.md')
            block = f'\n## {uid} · 2026-11-05 · structural · {status}\n' + '\n'.join(f'{k}: {vals[k]}' for k in unit.KEYS)
            open(os.path.join(folder, 'UNITS.md'), 'a').write(block + '\n')
        with patch('measure.measures', return_value={'G1': 1}), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            if repair:
                write(folder, set_status(read(os.path.join(folder, 'UNITS.md')), 'U0002', 'open', 'closed'))
                run('add', '.')
                run('commit', '-qm', 'U0002 blocked queue fixture')
                args = ['unit.py', 'open', 'U0004', folder, 'repair queue', 'A0001 · S none, queue repair', 'OWNER.md · PLAN.md · UNITS.md', '+≤100']
                with patch.object(sys, 'argv', args):
                    write(folder, read(os.path.join(folder, 'UNITS.md')).replace('· planned', '· closed'))
                    assert open_unit(folder, 'U0004') == 1
                    run('checkout', 'HEAD', '--', 'UNITS.md')
                    assert open_unit(folder, 'U0004') == 0
                raw = read(os.path.join(folder, 'UNITS.md'))
                forged = unit.set_key(raw, 'U0004', 'files', args[6] + ' · x.md')
                forged = unit.set_key(forged, 'U0004', 'plan', 'A0001 · S none')
                write(folder, forged)
                assert not unit.check(folder, {'tool_name': 'Edit', 'tool_input': {'file_path': 'x.md'}})[0]
                path = os.path.join(folder, 'PLAN.md')
                fixed = read(path).replace('missing movement', 'G1 from 1 to 2')
                open(path, 'w').write(fixed)
                fields = dict(seed, sentence='repair queue', plan=args[5], files=args[6], check="grep -q 'G1 from 1 to 2' PLAN.md", review='pass agent-review-fixture.md')
                for key, value in fields.items():
                    if key != 'base': raw = unit.set_key(raw, 'U0004', key, value)
                write(folder, raw.replace('## U0001', '## U0099'))
                assert close_unit(folder, 'U0004') == 1 and 'earlier block' in read(os.path.join(folder, 'unit' + '.log'))
                write(folder, raw)
                assert close_unit(folder, 'U0004') == 0, read(os.path.join(folder, 'unit' + '.log'))
                assert open_unit(folder, 'U0003') == 0
                return True
            assert close_unit(folder, 'U0002') == 1
            assert 'leaf move' in read(os.path.join(folder, 'unit.log'))
            assert load(folder)[1][1][1] == 'open'
            before = read(os.path.join(folder, 'PLAN.md'))
            valid = before.replace('missing movement', 'G1 from 1 to 2')
            write(folder, set_status(read(os.path.join(folder, 'UNITS.md')), 'U0002', 'open', 'closed'))
            assert open_unit(folder, 'U0003') == 1
            open(os.path.join(folder, 'PLAN.md'), 'w').write(valid.replace('| S2 | G1 |', '| S2 | G0 |'))
            assert open_unit(folder, 'U0003') == 0
            write(folder, set_status(read(os.path.join(folder, 'UNITS.md')), 'U0003', 'open', 'planned'))
            open(os.path.join(folder, 'PLAN.md'), 'w').write(valid.replace('G1 from', 'G99 from'))
            assert open_unit(folder, 'U0003') == 1
    return True


def ownership_paths_check(folder):
    """Compare selective ownership with full blame after an unowned rename."""
    import subprocess
    def git(*args):
        command = ['git','-C',folder,'-c','user.name=x']
        command += ['-c','user.email=x@x',*args]
        return subprocess.run(command,capture_output=True,check=True)
    first = os.path.join(folder,'s1.md')
    second = os.path.join(folder,'s2.md')
    with open(first,'w') as handle:
        handle.write('a\n')
    git('add','s1.md')
    git('commit','-qn','-m','stray')
    git('mv','s1.md','s2.md')
    git('commit','-qn','-m','U0001 x')
    full = sum(1 for rows in line_map(folder).values()
               for _,owner in rows if owner is None)
    paths = pile_paths(folder)
    valid = full > 0 and pile_count(folder) == full
    valid = valid and 's2.md' in paths
    valid = valid and 'RULE.md' not in paths
    git('reset','-q','HEAD~2')
    for path in [first,second]:
        if os.path.exists(path):
            os.remove(path)
    return valid


def binary_checks():
    """Close a generated binary through the real hook, then detect unowned edits."""
    import contextlib, io, subprocess, tempfile
    from pathlib import Path
    import unit, room as maker, measure
    with tempfile.TemporaryDirectory() as folder:
        root, source = Path(folder), Path(unit.__file__).resolve().parent
        texts = maker.ledgers('99_binary', 'Govern generated artifacts', 'fixture', '')
        texts['PRODUCTS.md'] += '| P10 | generated sample | — | result | output/sample.bin, output/alias.bin | — |\n'
        for name, text in texts.items():
            (root / name).write_text(text)
        for name in ('RULE.md', 'unit.py', 'measure.py', 'audit.py'):
            (root / name).symlink_to(source / name)
        run = lambda *args: subprocess.run(['git', '-C', folder, *args], capture_output=True, check=True)
        run('init', '-q')
        run('config', 'user.name', 'fixture')
        run('config', 'user.email', 'fixture@local')
        run('add', '.')
        run('commit', '-qm', 'U0001 fixture')
        (root / '.git/hooks/pre-commit').symlink_to(source / 'hooks/pre-commit')
        seed = unit.load(folder)[1][0][3]
        vals = dict(seed, sentence='Generate one binary artifact', plan='A0001 · S none', base='U0001', files='UNITS.md · output/sample.bin · output/alias.bin', check='test -s output/sample.bin', review='pass agent-review-fixture.md')
        block = '\n## U0002 · 2026-11-05 · behavioral · open\n' + '\n'.join(f'{k}: {vals[k]}' for k in unit.KEYS) + '\n'
        unit.write(folder, unit.read(str(root / 'UNITS.md')) + block)
        (root / 'output').mkdir()
        artifact = root / 'output/sample.bin'
        artifact.write_bytes(b'generated\0\n' + b'row\n' * 600)
        (root / 'output/alias.bin').symlink_to('sample.bin')
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            assert unit.close_unit(folder, 'U0002') == 0
            assert pile_count(folder) == 0
        final = unit.load(folder)[1][-1][3]
        assert 'output/sample.bin:binary' in final['files']
        assert line_map(folder)['output/sample.bin'] == [(1, 'U0002')]
        sizes = dict(measure.composition(folder, unit.load(folder)[1], piles=False))['product sizes against caps']
        assert 'over: []' in sizes and 'binary bytes:' in sizes and 'output/sample.bin' in sizes
        assert 'output/alias.bin' in sizes
        assert line_map(folder)['output/alias.bin'] == [(1, 'U0002')]
        artifact.write_bytes(b'changed\0\n')
        assert line_map(folder)['output/sample.bin'] == [(1, None)]
        (root / 'orphan.txt').write_text('unowned\n')
        assert line_map(folder)['orphan.txt'] == [(1, None)]
        (root / 'orphan.txt').unlink()
        artifact.unlink()
        (root / 'output/alias.bin').unlink()
        vals.update(sentence='Remove the generated artifact', base='U0002', check='test ! -e output/sample.bin')
        block = '\n## U0003 · 2026-11-05 · behavioral · open\n' + '\n'.join(f'{k}: {vals[k]}' for k in unit.KEYS) + '\n'
        unit.write(folder, unit.read(str(root / 'UNITS.md')) + block)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            assert unit.close_unit(folder, 'U0003') == 0
        artifact.write_bytes(b'recreated\0\n')
        run('config', 'status.showUntrackedFiles', 'no')
        assert line_map(folder)['output/sample.bin'] == [(1, None)]
    return True


def selftest(room):
    """Replay every deny case of check, four of them on another ledger state, pile and validate on a scratch copy of the room, then count the log lines written there."""
    import shutil, tempfile
    if os.environ.get('HECTOLINE_SELFTEST'): print('selftest: nested, skipped'); return 1  # a check clause inside the copy that calls the selftest stops here, loud, S107
    os.environ['HECTOLINE_SELFTEST'] = '1'
    passed = total = 0
    def expect(ok): nonlocal passed, total; passed += bool(ok); total += 1  # one gate case counts itself, so a new case is one line
    src, tags, seen = read(__file__).splitlines(), {}, {}  # each S mark of a case line counts its passes and its total, S104
    def mark(ok, n): [tags.__setitem__(m, [tags.get(m, [0, 0])[0] + bool(ok), tags.get(m, [0, 0])[1] + 1]) for m in re.findall(r'\bS\d{2,3}\b', src[n - 1].split('#')[-1])]
    def expect(ok, _e=expect): _e(ok); n = sys._getframe(1).f_lineno; loop = src[n - 2].lstrip().startswith('for '); top = next(i for i in range(n, 0, -1) if src[i - 1].rstrip().endswith('= [')) if loop else 0; mark(ok, top + 1 + seen.get(n, 0) if loop else n); seen[n] = seen.get(n, 0) + 1  # the case line is the caller's line, or the k-th entry of the table above a loop
    with tempfile.TemporaryDirectory() as tmp:
        copy = os.path.join(tmp, 'room')
        shutil.copytree(room, copy, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))  # the room links stay links, a leaf's hub link is a folder otherwise, S92
        text, bl = load(copy)
        from selftest_flow import expand_plans
        from selftest_flow import blocked_queue
        from selftest_flow import review_file_case
        from selftest_flow import review_write_case
        from selftest_flow import fixture_review, review_close_case
        from selftest_flow import review_route_case
        from selftest_flow import baseline_case
        from selftest_flow import nested_case
        from selftest_flow import history_case
        from selftest_flow import hand_close_case
        from selftest_flow import loose_open_case
        from selftest_roads import door_check_case
        from selftest_flow import index_case
        from selftest_roads import queue_text_case
        from selftest_roads import entry_case
        from selftest_roads import leaf_text_case
        from selftest_roads import third_fail_case
        fixture_review()
        write(copy, expand_plans(text))
        text, bl = load(copy)
        AUDIT = '\n\n## U9980 · 2026-01-01 · audit · closed\n' + '\n'.join(f'{k:<11}: x' for k in __import__('unit').KEYS) + '\n'  # an explicit audit state for the step-policy cases, the ten-count of the live room does not reach them, S179
        opened = next((u for u, s, _, _ in bl if s == 'open'), None)
        if not opened:  # the selftest needs an open unit, so it turns the newest block open on the copy
            opened = bl[-1][0]
            text = set_status(text, opened, bl[-1][1], 'open')
        vals = dict((u, v) for u, _, _, v in bl)[opened]
        text = re.sub(r'^(## U\d{4} · \S+ · \w+ · )waiting$', r'\1closed', re.sub(rf'^(## {opened} · \S+ · )\w+( · open)$', r'\1structural\2', text, flags=re.M), flags=re.M)  # the copy's unit is structural, a redesign is exempt from the owner chain, and no waiting block locks files or the queue
        write(copy, set_key(set_key(text, opened, 'files', vals.get('files', '') + ' · RULE.md'), opened, 'approval', 'none'))
        write(copy, set_key(read(os.path.join(copy, 'UNITS.md')), opened, 'plan', 'A0013 · S none'))  # the opened block takes the plan of a waiting audit block, the shape the hub's U0061 had, S99
        other = next(f for f in ('GOAL.md', 'OWNER.md', 'PRODUCTS.md', 'RESEARCH.md') if f not in files_of(vals))
        cases = [
            ({'tool_name': 'Bash', 'tool_input': {'command': 'git commit --no-verify -m x'}}, 'git bypass flag'),
            ({'tool_name': 'Bash', 'tool_input': {'command': 'echo x >> unit.log'}}, 'unit.log is append-only'),
            ({'tool_name': 'Edit', 'tool_input': {'file_path': other}}, 'not in the files key'),
            ({'tool_name': 'Edit', 'tool_input': {'file_path': 'RULE.md'}}, 'is protected, no owner line'),
            ({'tool_name': 'Bash', 'tool_input': {'command': f'sed -i s/a/b/ {other}'}}, 'not in the files key'),
            ({'tool_name': 'Edit', 'tool_input': {'file_path': 'unit.log'}}, 'unit.log is append-only'),
            ({'tool_name': 'Bash', 'tool_input': {'command': f'cp a.txt \\\n {other}'}}, 'not in the files key'),  # a backslash continues the operands, S55
            ({'tool_name': 'Bash', 'tool_input': {'command': 'python3 -c "open(\'unit.log\', \'a\').write(\'x\')"'}}, 'unit.log is append-only'),  # a python write to the log, S57
            ({'tool_name': 'Bash', 'tool_input': {'command': 'git checkout HEAD -- unit.log'}}, 'unit.log is append-only'),  # a git write to the log, S57
            ({'tool_name': 'Bash', 'tool_input': {'command': 'grep -c deny unit.log\nrm -f unit.log'}}, 'unit.log is append-only'),  # a read line followed by a write line, S57
            ({'tool_name': 'WebSearch', 'tool_input': {'query': 'x'}}, 'outside a research unit'),  # S76
            ({'tool_name': 'Agent', 'tool_input': {'prompt': 'x'}}, 'outside a research unit'),  # S76
            ({'tool_name': 'Edit', 'tool_input': {'file_path': f'{HOME}/.claude/CLAUDE.md'}}, 'not in the files key'),  # the common rules file stays gated, S72
            ({'tool_name': 'Bash', 'tool_input': {'command': f'cd {tmp} && cd {copy} && printf x >> {other}'}, 'cwd': copy}, 'not in the files key'),  # a second cd leads back in, S84
        ]
        for payload, want in cases:
            expect(not check(copy, payload)[0] and want in check(copy, payload)[1])
        base, edit = read(os.path.join(copy, 'UNITS.md')), {'tool_name': 'Edit', 'tool_input': {'file_path': 'RULE.md'}}  # four denies that need another ledger state
        row = next(l for l in read(os.path.join(copy, 'PLAN.md')).splitlines() if l.startswith('| S0'))
        code = next((f for f in sorted(os.listdir(room)) if f.endswith('.py') and not os.path.islink(os.path.join(room, f))), None); line = read(os.path.join(copy, code)).splitlines()[0] if code else ''; own = owners(copy, code, line)[:1] if code else []; owner, code = (own[0], code) if own else ('', None)  # the first non-link code file of the room, if any and committed, its first line's owner gains two replaced units, S92
        variants = [
            (set_status(base, opened, 'open', 'waiting'), edit, 'belongs to waiting'),
            (set_status(base, opened, 'open', 'planned'), edit, 'no open unit'),
            (set_key(base, opened, 'files', 'tests/t.py · report.py'), {'tool_name': 'Edit', 'tool_input': {'file_path': 'report.py'}}, 'mixes a test file with code'),
            *([(set_key(set_key(base, opened, 'files', code), owner, 'deleted', 'replaces U0098 replaces U0099'), {'tool_name': 'Edit', 'tool_input': {'file_path': code, 'old_string': line}}, 'two earlier owners')] if code else []),  # a room with no code file skips it
        ]
        for state, payload, want in variants:
            write(copy, state); expect(not check(copy, payload)[0] and want in check(copy, payload)[1])
        write(copy, base); log(copy, 'selftest', opened, 'allow', f'{len(cases) + len(variants)} check denies replayed')
        piles = pile_count(copy); open(os.path.join(copy, 'stray.md'), 'w').write('x\n'); expect(pile_count(copy) == piles + 1)
        piles = pile_count(copy); os.symlink(tmp, os.path.join(copy, 'dirlink')); expect(pile_count(copy) == piles + 1); os.remove(os.path.join(copy, 'dirlink'))  # an untracked directory link is one pile row by its target, not a read of the folder, S113
        expect(ownership_paths_check(copy))  # S127
        made = not os.path.lexists(os.path.join(copy, 'legacy')) and (os.symlink(tmp, os.path.join(copy, 'legacy')) or True); f = os.path.join(os.path.realpath(os.path.join(copy, 'legacy')), 'frozen.md'); expect('is frozen' in check(copy, {'tool_name': 'Write', 'tool_input': {'file_path': f}})[1] and 'is frozen' not in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': 'r' + 'm ' + f}, 'cwd': copy})[1]); made and os.remove(os.path.join(copy, 'legacy'))  # a write under the legacy target is denied as frozen, a deletion is not, RULE §6, S117
        made = not os.path.lexists(os.path.join(copy, 'legacy')) and (os.symlink(tmp, os.path.join(copy, 'legacy')) or True); expect('no file' not in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': 'm' + 'v ' + os.path.join(os.path.realpath(os.path.join(copy, 'legacy')), 'sub') + ' documents/'}, 'cwd': copy})[1]); made and os.remove(os.path.join(copy, 'legacy'))  # a folder operand under the legacy target reaches the files key gate, not «no file», S119
        expect(validate_units(load(copy)[0].replace('tidy-first?:', 'tidyfirst?:', 1)))
        expect(validate_units(set_key(load(copy)[0], opened, 'cause', 'see RULE line 40')))  # a live block that cites a RULE line number faults, S80
        expect(__import__('unit').names_unit(copy, opened, '«approve ' + opened + '»') and not __import__('unit').names_unit(copy, opened, '«approve all»'))  # an owner line names the unit when its quote holds the number, RULE §2, S71
        r = __import__('subprocess').run([sys.executable, '-I', '-B', os.path.join(copy, 'unit.py'), 'selftest', copy], capture_output=True, text=True); expect(r.returncode == 1 and 'nested, skipped' in r.stdout)  # a nested selftest stops at once, placed before the failed close at the first run, when HEAD had no guard yet, S107
        os.mkfifo(os.path.join(copy, 'fifo')); write(copy, set_key(set_key(set_key(set_key(base, opened, 'review', 'pass, agent-review-x.md'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'test -f stray.md')); n = sum(f.startswith('hectoline-') for f in os.listdir(tempfile.gettempdir())); r = __import__('subprocess').run([sys.executable, '-I', '-B', os.path.join(copy, 'unit.py'), 'close', opened, copy], capture_output=True, text=True); os.remove(os.path.join(copy, 'fifo')); expect(r.returncode != 0 and sum(f.startswith('hectoline-') for f in os.listdir(tempfile.gettempdir())) == n); write(copy, base)  # a refused close with a FIFO in the room leaves no temp folder behind, S110
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cat > /tmp/x.txt <<EOF\n# files {other}\nEOF'}})[0])  # a heredoc body is no write target, S55
        expect(all('git bypass flag' in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': c}})[1] for c in ('T=$(git commit-tree X -p HEAD)', 'git -C r update-ref refs/heads/main X', 'git cherry-pick side', 'git merge --no-ff side', 'git revert --no-edit HEAD', 'git am p.patch', 'git rebase main', 'git pull origin main', 'git fast-import')) and not any('git bypass flag' in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': c}})[1] for c in ('git merge-base HEAD side', 'git log --merges --grep=merge', 'git amend-check', 'git status', 'git fetch', 'git merge --abort', 'git rebase --abort')))  # a git command that writes a commit without the pre-commit hook is a bypass, a read or an abort is not, S134
        expect('grep, tail' in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': 'echo x >> unit.log'}})[1] and 'cd DIR &&' in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cd {tmp}; printf x >> {other}'}, 'cwd': copy})[1] and 'cd DIR &&' not in check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cd {tmp} && printf x >> {other}'}, 'cwd': copy})[1])  # the deny texts name the read forms that pass and the «&&» form of cd, S133
        r = os.path.join(tmp, 'applied'); os.makedirs(r); os.symlink(os.path.join(copy, 'RULE.md'), os.path.join(r, 'RULE.md')); open(os.path.join(r, 'GOAL.md'), 'w').write(read(os.path.join(copy, 'GOAL.md'))); m = __import__('measure').measures(r, []); mc0 = __import__('measure').measures(copy, load(copy)[1]); expect(m and set(m.values()) == {'no tool'} and mc0 and all(v != 'no tool' for v in mc0.values()))  # a room without measures.py reads «no tool» per leaf, a room with one computes each leaf, S152
        expect(__import__('measure').met(19, '≤ 19') and not __import__('measure').met(20, '≤ 19') and __import__('measure').met('6 of 6', '6 of 6') and not __import__('measure').met('no tool', '≤ 19'))  # a «≤ N» target holds up to N, a fraction target needs its fraction, «no tool» meets nothing, S158
        bm = __import__('base').map_text(copy); bn = len(bm.splitlines()) - 2; bs = __import__('base').map_text(copy, budget=bn).splitlines(); expect(bm.splitlines()[0].startswith('# the ledgers win over this map') and all(f'\n{g[0]} · ' in bm for g in __import__('unit').rows_of(copy, 'GOAL.md', 'G') if g[0] != 'G0') and len(bm.splitlines()) <= 300 and len(bs) <= bn and bs[-1].endswith('PLAN.md holds them') and ('\n    P' in bm and '\n    U' in bm) == any(s[-1] != 'done' for s in __import__('unit').rows_of(copy, 'PLAN.md', 'S')))  # the room map heads with «the ledgers win», holds every leaf, shows the P and U nodes of open and todo steps, keeps its budget by leaving out done steps, S160
        pk = __import__('base').pack(copy, opened).splitlines(); ov = next(v for u, s, _, v in load(copy)[1] if u == opened); expect(pk[0] == f'# unit pack of {opened}. The ledgers win over this pack.' and all(any(l.startswith(f + ' · ') for l in pk) for f in files_of(ov)) and __import__('base').pack(copy, 'U9999') == 'U9999: no block')  # the unit pack heads with «the ledgers win», gives every file of the files key, an unknown unit has no block, S161
        gp = os.path.join(copy, 'GOAL.md'); g0 = read(gp); g1 = next(l for l in g0.splitlines() if l.startswith('| G1 |')); open(gp, 'w').write(g0.replace(g1, g1.replace(' | G0 | ', ' x | G0 | ', 1))); open(os.path.join(copy, 'hidden.md'), 'w').write('a note that leans on G1\n'); im = __import__('base').impact(copy).splitlines(); open(gp, 'w').write(g0); os.remove(os.path.join(copy, 'hidden.md')); expect(im[0].startswith('# impact list. The ledgers win') and any(l.startswith('G1 · cited in ') and 'hidden.md' in l for l in im) and __import__('base').impact(copy).splitlines()[1:] != im[1:])  # the impact list names a changed G row with a hidden new file that cites it, S162
        u0 = read(os.path.join(copy, 'UNITS.md')); write(copy, set_status(u0, opened, 'open', 'planned')); ro = __import__('subprocess').run([sys.executable, '-I', '-B', os.path.join(copy, 'unit.py'), 'open', opened, copy], capture_output=True, text=True); write(copy, u0); expect(f'{opened} open on ' in ro.stdout and f'# unit pack of {opened}. The ledgers win over this pack.' in ro.stdout)  # open prints the unit pack after «open on», the U0261 weak line, S161
        gp9 = read(gp); open(gp, 'w').write(gp9.rstrip('\n') + '\n| G9 | a probe leaf | G0 | count | 0 | 1 |\n')  # a leaf without a tool for the two step-policy cases below, S172 S173
        expect(blocked_queue(copy, opened, AUDIT))  # a queue whose every planned block sits under a «no tool» leaf opens the measure step of that leaf by the four texts as behavioral, no other step and no planning unit, S172
        u1, p1 = read(os.path.join(copy, 'UNITS.md')), read(os.path.join(copy, 'PLAN.md')); open(os.path.join(copy, 'PLAN.md'), 'w').write(p1.rstrip('\n') + '\n| S998 | G9 | x.md | a step, G9 from 1 to 0 | a · b | | todo |\n| S997 | G9 | measures.py | the measure of G9, G9 from no tool to 1 | a · b | | todo |\n'); plant = lambda st: write(copy, u1.rstrip('\n') + f'\n\n## U9990 · 2026-01-01 · behavioral · planned\nsentence   : x\nplan       : A0001 · {st}\nfiles      : x.md\nbase       : {opened}\nlines      : +1\n') or (__import__('base').planned_errors(copy, load(copy)[1], opened), __import__('base').planned_errors(copy, load(copy)[1], 'U9990')); pw, pm = plant('S998'), plant('S997'); write(copy, u1); open(os.path.join(copy, 'PLAN.md'), 'w').write(p1); expect(any('unmeasured' in x for x in pw[0]) and pw[1] == [] and pm[0] == [])  # a new planned block under a «no tool» leaf is named for the close refusal, its measure step is not, S173
        open(gp, 'w').write(gp9)  # the probe leaf leaves
        mc = __import__('measure').method_counts(copy, load(copy)[1]); expect(set(mc) == {'unmeasured leaves', 'steps under a leaf at target', 'ledger-only units', 'uncited R rows', 'no pilot step', '100 levels overdue'} and all(isinstance(v, int) for v in mc.values()) and mc['ledger-only units'] > 0)  # the six method counts of a room are integers, S143
        pl = read(os.path.join(copy, 'PLAN.md')); gl = read(os.path.join(copy, 'GOAL.md')); write_file = lambda n, t: open(os.path.join(copy, n), 'w').write(t)
        write_file('PLAN.md', pl.rstrip('\n') + '\n| S999 | G1 | x | a step with no move | a · b | | todo |\n| S998 | G1 | x | G1 from 1 to 0 | a · b | | todo |\n| S997 | G1 | x | G1 from 1 to 0, A0001 | a · b | | todo |\n'); write(copy, set_status(base, opened, 'open', 'closed').rstrip('\n') + AUDIT); open(os.path.join(copy, 'UNITS.md'), 'a').write('\n## U9990 · 2026-01-01 · structural · planned\nsentence   : x\nplan       : A0001 · S999\nfiles      : x.md\nbase       : ' + opened + '\nlines      : +1\n\n## U9991 · 2026-01-01 · structural · planned\nsentence   : y\nplan       : A0001 · S998\nfiles      : x.md\nbase       : ' + opened + '\nlines      : +1\n')
        r1 = __import__('subprocess').run([sys.executable, '-I', '-B', os.path.join(copy, 'unit.py'), 'open', 'U9990', copy], capture_output=True, text=True); r2 = __import__('subprocess').run([sys.executable, '-I', '-B', os.path.join(copy, 'unit.py'), 'open', 'U9991', copy], capture_output=True, text=True); a1 = __import__('unittest.mock', fromlist=['patch']).patch('measure.measures', return_value={'G1': next(g[4] for g in __import__('unit').rows_of(copy, 'GOAL.md', 'G') if g[0] == 'G1')})(lambda _m: __import__('unit').addon_rows(copy, load(copy)[1]))(); expect('names no leaf move' in r1.stdout + r1.stderr and 'open on' in r2.stdout and 'S999' in a1 and 'S998' in a1 and 'S997' not in a1); write(copy, base); write_file('PLAN.md', pl); write_file('GOAL.md', gl)  # a work unit opens only on a row that names its leaf move, a new todo row under a met leaf needs an A row, S139
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': 'grep -c deny unit.log'}})[0])  # a read of the log passes, S57
        expect(check(copy, {'tool_name': 'Agent', 'tool_input': {'prompt': f'review, log agent-review-{opened.lower()}.md'}})[0])  # the review dispatch of the live unit passes, S76
        expect(check(copy, {'tool_name': 'Agent', 'tool_input': {'prompt': f'review, log agent-review-hub-{opened.lower()}.md'}})[0])  # with a room infix too, S76
        expect(check(copy, {'tool_name': 'Edit', 'tool_input': {'file_path': f'{HOME}/.claude/memory/x.md'}})[0])  # a HOME dot path is outside, S72
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp a.txt $S/{other}'}})[0])  # a shell variable path is outside, S72
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp a.txt {other}'}, 'cwd': tmp})[0])  # a relative path from an outside cwd is outside, S72
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cd {tmp} && cp a.txt {other}'}, 'cwd': copy})[0])  # a leading cd moves the relative target outside, S84
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp {other} /tmp/x.md'}})[0])  # the cp source is no write, S84
        expect(not check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp -f a.txt {other}'}})[0])  # a flagged cp keeps its operands, S86
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp {other} RULE.md /tmp/x/'}})[0])  # every cp operand but the last is a source, S86
        expect(not check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp a.txt {other} 2>/dev/null'}})[0])  # a redirect after the target is no operand, S86
        expect(not check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp {other} /tmp/x.md > {other}'}})[0])  # a redirect inside the cp tail is a target, S86
        expect(not check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cp a.txt \\\n -f {other}>/dev/null'}})[0])  # a flag after a backslash break, a redirect glued to the target, S86
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cd $S && printf x > {other}'}, 'cwd': copy})[0])  # a cd into a shell variable folder puts the relative targets outside, S72
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'cd "{tmp}" && cp a.txt {other}'}, 'cwd': copy})[0])  # a quoted absolute folder after cd loses its quotes, S101
        expect(check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'P={tmp}; cd $P && cp a.txt {other}'}, 'cwd': copy})[0])  # an assignment before the cd still leads outside, S101
        expect(not check(copy, {'tool_name': 'Bash', 'tool_input': {'command': f'P=.; cd "$P" && cp a.txt {other}'}, 'cwd': copy})[0])  # an assignment that names the room leads back in, the folder resolves from the line, S101
        write(copy, set_key(base, opened, 'files', vals.get('files', '') + ' · RESEARCH.md')); expect(not check(copy, {'tool_name': 'WebSearch', 'tool_input': {'query': 'x'}})[0])  # R rows with a plain sentence stay denied, S76
        write(copy, set_key(set_key(base, opened, 'files', vals.get('files', '') + ' · RESEARCH.md'), opened, 'sentence', 'which?')); expect(check(copy, {'tool_name': 'WebSearch', 'tool_input': {'query': 'x'}})[0])  # a research unit passes, S76
        write(copy, set_key(set_key(set_key(set_key(base, opened, 'review', 'pass, no log file named'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'true'))  # check true, so a broken refusal cannot recurse into this selftest
        expect(close_unit(copy, opened) == 1 and 'names no agent-review file' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])  # close wants the review proof, S61
        expect(history_case(tmp))  # the reconstruction history reads from its declared start, an unreadable revision before it passes, a start that disables an activated plan is refused, S234
        expect(nested_case(copy, opened, tmp))  # the baseline test runs inside an outer confinement, a write outside the outer scratch stays denied, S226
        expect(baseline_case(copy, opened, tmp))  # a clause that exits 127 or 124 on the clone of HEAD is refused as no red baseline, a timeout counts as 124, S226
        expect(review_route_case(copy, opened, tmp))  # the Claude hook sends a review file write in a folder outside every room to the room of its unit, S225
        expect(review_close_case(copy, opened, tmp))  # close refuses a review key whose file no reviewer wrote, the refusal ends with the key form, S225
        expect(review_write_case(copy, opened, tmp))  # the edit gate denies the author of the open unit a write to its review file, a subagent call passes, S225
        expect(review_file_case(copy, opened, tmp))  # the reader takes the pass from the review file alone, a key the author wrote gives an error, S225
        expect(hand_close_case(tmp))  # a closed status written by hand is refused at the commit for its missing review file, a fresh room makes its first commit, unit.py close commits through the hook, S233
        expect(loose_open_case(tmp))  # open reads a closed status that HEAD does not hold as an open unit, the refusal names the unit with unit.py close, no block is appended, S233
        expect(door_check_case(tmp))  # a hand close under a true review file is refused at the commit for a failing check with for a check that passes on HEAD, a red check that turns green commits, S233
        expect(index_case(tmp))  # a hand close that stages the ledger alone is refused for the path the index lacks, the whole commit passes, a failed block that stages a product path is refused, S233
        expect(queue_text_case(tmp))  # the refusals «the planned queue is empty» with «no planned block» name the planning call, the call they name opens the unit, S227
        expect(entry_case(tmp))  # a room made with its acceptance check holds its leaf, two steps with a planned measure unit in a clean first commit, the measure unit opens in one call, the pilot before it is refused, a room without the check keeps the old road, S228
        expect(leaf_text_case(tmp))  # the refusal «names no leaf move» gives the text that passes, a step row that holds that text opens its unit, S227
        expect(third_fail_case(tmp))  # three failed rounds end a unit of a fresh room: status failed, the result names the count, its product reverted, the commit carries the unit, RULE §4, S79
        done = re.sub(r'^(## U\d{4} · \S+ · \w+ · )planned$', r'\1closed', set_status(base, opened, 'open', 'closed'), flags=re.M); nxt = f'U{int(bl[-1][0][1:]) + 1:04d}'  # every block final, the queue empty
        done = set_key(done, opened, 'plan', 'A0001 · S01')  # the done state gives the block a work plan, a closed «S none» block would read as a planning unit, S99
        argv, sys.argv = sys.argv, sys.argv[:1] + ['open', nxt, copy, 'x', 'A0001 · S01', 'UNITS.md', '+1']  # a work unit on an empty queue, S75
        write(copy, done); expect(open_unit(copy, nxt) == 1 and 'planned queue is empty' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])
        write(copy, set_key(re.sub(rf'^(## {bl[-1][0]} · \S+ · )\w+( · )closed$', r'\1audit\2closed', done, flags=re.M), bl[-1][0], 'plan', 'A0013 · S none'))  # a closed audit is not a planning unit
        expect(open_unit(copy, nxt) == 1 and 'planned queue is empty' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])
        plan = set_key(re.sub(rf'^(## {bl[-2][0] if len(bl) > 1 else "U0000"} · \S+ · )\w+( · )closed$', r'\1audit\2closed', done, flags=re.M), bl[-1][0], 'plan', 'A0001 · S none'); write(copy, set_key(plan, bl[-1][0], 'added', 'none')); expect(open_unit(copy, nxt) == 1 and (write(copy, set_key(plan, bl[-1][0], 'added', 'planned S01')) or open_unit(copy, nxt) == 0)); write(copy, done)  # a closed planning unit opens the next work unit by four texts only when it names the step cited, the block before it an audit so the ten-count does not refuse, S126
        sys.argv[5] = 'A0080 · S none'; expect(open_unit(copy, nxt) == 0); sys.argv = argv  # a planning unit passes the four-text path
        mk = lambda n, t, s: f'\n\n## U{n:04d} · 2026-01-01 · {t} · {s}\n' + '\n'.join(f'{k:<11}: {"U%04d" % (n - 1) if k == "base" else "x"}' for k in vals) + '\n'  # a synthetic block for the audit gate cases, S91
        n0 = int(bl[-1][0][1:]) + 1; ten = done + mk(n0, 'audit', 'closed') + ''.join(mk(n0 + i, 'structural', 'closed') for i in range(1, 11))  # one closed audit, then ten non-audit units
        write(copy, ten + mk(n0 + 11, 'structural', 'planned')); expect(open_unit(copy, f'U{n0 + 11:04d}') == 1 and 'since the last closed audit' in read(os.path.join(copy, 'unit.log')).splitlines()[-1]); sys.argv = sys.argv[:1] + ['open', f'U{n0 + 12:04d}', copy, 'x', 'A0013 · S none', 'UNITS.md', '+1']; expect(open_unit(copy, f'U{n0 + 12:04d}') == 0 and re.search(rf'^## U{n0 + 12:04d} · \S+ · audit · open$', read(os.path.join(copy, 'UNITS.md')), re.M))  # the eleventh work unit is refused, the four-text audit opens over it
        sys.argv = sys.argv[:1] + ['open', f'U{n0 + 11:04d}', copy, 'x', 'A0080 · S none', 'UNITS.md', '+1']; write(copy, ten); expect(open_unit(copy, f'U{n0 + 11:04d}') == 0)  # one planning unit passes as the eleventh
        write(copy, set_status(read(os.path.join(copy, 'UNITS.md')), f'U{n0 + 11:04d}', 'open', 'closed') + mk(n0 + 12, 'structural', 'planned')); expect(open_unit(copy, f'U{n0 + 12:04d}') == 1 and 'since the last closed audit' in read(os.path.join(copy, 'unit.log')).splitlines()[-1]); sys.argv[1:3] = ['open', f'U{n0 + 13:04d}']; expect(open_unit(copy, f'U{n0 + 13:04d}') == 0 and re.search(rf'^## U{n0 + 13:04d} · \S+ · audit · open$', read(os.path.join(copy, 'UNITS.md')), re.M)); sys.argv = argv  # a work unit right after it is refused, the four-text audit opens past it
        write(copy, done + mk(n0, 'audit', 'closed') + mk(n0 + 1, 'structural', 'planned') + mk(n0 + 2, 'structural', 'planned')); expect(open_unit(copy, f'U{n0 + 2:04d}') == 1 and 'not final' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])  # open refuses a base that is not final, S68
        write(copy, done + mk(n0, 'audit', 'closed') + mk(n0 + 1, 'structural', 'open') + mk(n0 + 2, 'structural', 'planned')); expect(open_unit(copy, f'U{n0 + 2:04d}') == 1 and f'U{n0 + 2:04d}: another unit is open' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])  # open refuses while another unit is open, the refusal names the unit, S68 S108
        write(copy, set_key(set_key(set_key(set_key(base, opened, 'review', 'pass, agent-review-x.md'), opened, 'added', 'x'), opened, 'check', 'true'), opened, 'rejected', '')); expect(close_unit(copy, opened) == 1 and 'rejected empty' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])  # close refuses an empty key, S68
        write(copy, set_key(set_key(set_key(set_key(set_key(base, opened, 'review', 'pass, agent-review-x.md'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'test -f stray.md'), opened, 'sentence', 'a and b')); expect(close_unit(copy, opened) == 1 and 'do not validate' in read(os.path.join(copy, 'unit.log')).splitlines()[-1]); write(copy, base)  # close refuses ledgers that do not validate, S68
        write(copy, set_key(base, opened, 'files', vals.get('files', '') + ' · selftest.py · hooks/claude.py'))  # the gate's own files need an owner line, S89
        expect(not check(copy, {'tool_name': 'Edit', 'tool_input': {'file_path': 'selftest.py'}})[0] and 'is protected' in check(copy, {'tool_name': 'Edit', 'tool_input': {'file_path': 'selftest.py'}})[1])
        expect(not check(copy, {'tool_name': 'Edit', 'tool_input': {'file_path': 'hooks/claude.py'}})[0] and 'is protected' in check(copy, {'tool_name': 'Edit', 'tool_input': {'file_path': 'hooks/claude.py'}})[1])
        lead = owners(copy, 'PLAN.md', row)[:1]  # the row's blame unit, none while the live terminal holds the row uncommitted
        if lead: write(copy, set_key(base, lead[0], 'deleted', 'replaces U0098 replaces U0099')); expect(len(owners(copy, 'PLAN.md', row)) == 1); write(copy, base)  # a ledger row keeps one owner past a replaces chain, S92
        if code: write(copy, set_key(base, owner, 'deleted', 'replaces U0098 replaces U0099')); expect(len(owners(copy, code, line)) >= 3); write(copy, base)  # a code line reaches its chain, S92
        if code: write(copy, set_key(set_key(set_key(set_key(set_key(set_key(base, owner, 'deleted', 'replaces U0098 replaces U0099'), opened, 'files', code), opened, 'review', 'pass, agent-review-x.md'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'test -f stray.md')); t = read(os.path.join(copy, code)).replace(line, line + ' ', 1); open(os.path.join(copy, code), 'w').write(t); expect(close_unit(copy, opened) == 1 and 'two earlier owners' in read(os.path.join(copy, 'unit.log')).splitlines()[-1]); write(copy, base)  # close refuses a changed line with a chain, S96
        if code: write(copy, set_key(base, owner, 'deleted', 'replaces U0098 replaces U0099')); expect(owners(copy, code, '', 'HEAD', (1, 1)) == owners(copy, code, line, 'HEAD') and len(owners(copy, code, '', 'HEAD', (1, 1))) >= 3); write(copy, base)  # the range route of line 1 reads the chain as the text route does, S103
        own = [owners(copy, code, '', 'HEAD', (i, 1)) for i in range(1, 13)] if code else []; pair = next((i for i in range(1, len(own)) if own[i - 1] and own[i] and own[i - 1] != own[i]), None)  # two adjacent lines of different owners, S103
        if pair: t = read(os.path.join(copy, code)).replace(line + ' ', line, 1); open(os.path.join(copy, code), 'w').write(t); write(copy, set_key(set_key(set_key(base, own[pair - 1][0], 'deleted', 'replaces U0098'), own[pair][0], 'deleted', 'replaces U0099'), opened, 'files', code)); expect(check(copy, {'tool_name': 'Edit', 'tool_input': {'file_path': code, 'old_string': '\n'.join(read(os.path.join(copy, code)).splitlines()[pair - 1:pair + 1])}})[0]); write(copy, base)  # a two-line anchor over two single owners with one replace each passes, the chain counts per line, S105
        if pair: write(copy, set_key(set_key(set_key(set_key(set_key(set_key(set_key(base, own[pair - 1][0], 'deleted', 'replaces U0098'), own[pair][0], 'deleted', 'replaces U0099'), opened, 'files', code), opened, 'review', 'pass, agent-review-x.md'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'test -f stray.md')); t = '\n'.join(l + ' ' if i in (pair, pair + 1) else l for i, l in enumerate(read(os.path.join(copy, code)).splitlines(), 1)) + '\n'; open(os.path.join(copy, code), 'w').write(t); close_unit(copy, opened); last = read(os.path.join(copy, 'unit.log')).splitlines()[-1]; expect('two earlier owners' not in last and ('git hook' in last or 'do not validate' in last)); write(copy, base)  # one chain each on two adjacent lines, the per-line test lets close pass to its stop, S103 S104
        write(copy, set_key(set_key(set_key(set_key(base, opened, 'review', 'pass, agent-review-x.md'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'true')); expect(close_unit(copy, opened) == 1 and 'passes on a copy of HEAD' in read(os.path.join(copy, 'unit.log')).splitlines()[-1])  # a clause that passes before the unit is refused, S73
        write(copy, set_key(set_key(set_key(set_key(base, opened, 'review', 'pass, agent-review-x.md'), opened, 'rejected', 'x'), opened, 'added', 'x'), opened, 'check', 'test -f stray.md')); close_unit(copy, opened); last = read(os.path.join(copy, 'unit.log')).splitlines()[-1]; expect('passes on a copy' not in last and ('git hook' in last or 'do not validate' in last)); write(copy, base)  # a clause that fails on the copy goes on to its stop, S73
        written = len(read(os.path.join(copy, 'unit.log')).splitlines()) - len(read(os.path.join(room, 'unit.log')).splitlines())
        print(f'selftest: {passed} of {total} gate cases pass · {written} log lines written on the copy')
        print('tags: ' + ' '.join(f'{m} {p} of {t}' for m, (p, t) in sorted(tags.items(), key=lambda kv: int(kv[0][1:]))))  # one count per S mark, a clause binds its own, RULE line 54, S104
        return 0 if passed == total else 1
