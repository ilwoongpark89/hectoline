#!/usr/bin/env python3
"""run.py TASKS.json WORK RESULTS [--task ID]... [--arm plain|hectoline] [--setup-only] [--pybin DIR]

One run = one task × one arm: a fresh folder with the repository fetched at base_commit and a TASK.md,
one headless Claude Code session with the caps of design.json, then the prediction (the diff of the
repository against the base tree, ledger files excluded) and one line in RESULTS/runs.jsonl.
Both arms of a task run together, two sessions at once, so an interruption leaves matched pairs.
The hectoline arm makes the folder a room: the six ledgers, the links to RULE.md and the tools, a
unit.py that asks the harness reviewer at each close request, the Claude Code hooks in the folder's
.claude/settings.json and the git pre-commit. The task text of both arms is in design.json.
The harness holds no gold patch and no hidden test; tasks.json carries the statement and the hints only."""
import datetime, json, os, re, shutil, signal, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.realpath(__file__))
BENCH = os.path.dirname(HERE)
HECTOLINE = os.path.dirname(os.path.dirname(BENCH))
CONFIG = json.load(open(os.path.join(BENCH, 'design.json')))
sys.path.insert(0, HECTOLINE)
sys.path.insert(0, os.path.join(HECTOLINE, 'hooks'))

G0 = 'the issue in TASK.md is fixed in this repository'
QUOTE = 'Fix the issue in TASK.md in this repository'
WRAPPER = '''#!/usr/bin/env python3
"""unit.py — the gate entry of this room. close asks the independent reviewer of the harness first, then runs hectoline unit.py close.
Every other command passes through to hectoline unit.py unchanged."""
import os, subprocess, sys
HECTOLINE = {hectoline!r}
REVIEW = {review!r}
RUN = {run!r}
args = sys.argv[1:]
if len(args) >= 2 and args[0] == 'close':
    room = os.path.dirname(os.path.abspath(__file__))
    code = subprocess.run([sys.executable, '-B', REVIEW, 'review', args[1], room, RUN]).returncode
    if code:
        sys.exit(code)
os.execv(sys.executable, [sys.executable, '-B', os.path.join(HECTOLINE, 'unit.py'), *args])
'''


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def sh(args, cwd=None, env=None, check=True, timeout=None, text=True):
    run = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=text, timeout=timeout)
    if check and run.returncode:
        raise RuntimeError(f'{" ".join(map(str, args))}\n{run.stdout}{run.stderr}')
    return run.stdout


def log(results, line):
    stamp = f'{now()} {line}'
    print(stamp, flush=True)
    with open(os.path.join(results, 'harness.log'), 'a', encoding='utf8') as f:
        f.write(stamp + '\n')


def load_now():
    cpu = float(sh(['sh', '-c', "ps -Ao %cpu | awk '{t+=$1} END {print t}'"]).strip() or 0)
    mem = sh(['sh', '-c', 'memory_pressure | tail -1']).strip()
    free = int(re.search(r'(\d+)%', mem).group(1)) if re.search(r'(\d+)%', mem) else 100
    return cpu, free


def wait_for_load(results):
    while True:
        cpu, free = load_now()
        if cpu < CONFIG['cpu_limit_percent'] and free > CONFIG['memory_free_min_percent']:
            log(results, f'load ok: cpu {cpu:.0f} % of {CONFIG["cpu_limit_percent"]}, memory free {free} %')
            return cpu, free
        log(results, f'load high: cpu {cpu:.0f} %, memory free {free} %, waiting 60 s')
        time.sleep(60)


def pybin(work, given=None):
    """A folder whose python3, python, pip and pip3 are the harness interpreter, first on the PATH of every session."""
    folder = given or os.path.join(work, 'pybin')
    os.makedirs(folder, exist_ok=True)
    target = os.path.realpath(sys.executable)
    base = os.path.dirname(target)
    for name in ('python3', 'python', 'pip', 'pip3'):
        link = os.path.join(folder, name)
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(os.path.join(base, name) if os.path.exists(os.path.join(base, name)) else target, link)
    return folder


def session_env(work, bin_dir):
    env = dict(os.environ)
    env['PATH'] = bin_dir + os.pathsep + env.get('PATH', '')
    rooms = os.path.join(work, 'rooms-empty')
    os.makedirs(rooms, exist_ok=True)
    env['HECTOLINE_ROOMS'] = rooms
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def fetch(task, folder, subject):
    """The repository at base_commit as one commit with TASK.md, the history behind it left out."""
    os.makedirs(folder)
    git = lambda *a: sh(['git', '-C', folder, *a])
    git('init', '-q')
    git('remote', 'add', 'origin', f'https://github.com/{task["repo"]}.git')
    git('fetch', '-q', '--depth', '1', 'origin', task['base_commit'])
    git('checkout', '-q', '-b', 'work', 'FETCH_HEAD')
    git('config', 'user.name', 'agent')
    git('config', 'user.email', 'agent@localhost')
    with open(os.path.join(folder, '.git', 'info', 'exclude'), 'a', encoding='utf8') as f:
        f.write('\n'.join(CONFIG['git_exclude']) + '\n')
    hints = task.get('hints_text') or '(none)'
    with open(os.path.join(folder, 'TASK.md'), 'w', encoding='utf8') as f:
        f.write(f'# Task\n\nRepository {task["repo"]} at commit {task["base_commit"]}.\n\n## Problem statement\n\n{task["problem_statement"].strip()}\n\n## Hints\n\n{hints.strip()}\n')
    git('add', 'TASK.md')
    git('commit', '-q', '--amend', '-m', subject)
    return git('rev-parse', 'HEAD').strip()


def make_room(task, folder, run, env):
    """The ledgers of room.py, written into the repository folder, the links, the wrapper, the hooks, one bootstrap commit."""
    top = os.path.join(run, 'roomsrc')
    sh([sys.executable, '-I', '-B', os.path.join(HECTOLINE, 'room.py'), '01_task', G0, QUOTE, '--top', top], env=env)
    src = os.path.join(top, '01_task')
    for name in ('GOAL.md', 'OWNER.md', 'PLAN.md', 'PRODUCTS.md', 'RESEARCH.md', 'UNITS.md', 'unit.log'):
        if os.path.exists(os.path.join(folder, name)):
            raise RuntimeError(f'{name} exists in the repository, the room cannot be laid over it')
        shutil.copy(os.path.join(src, name), os.path.join(folder, name))
    units = os.path.join(folder, 'UNITS.md')
    text = open(units, encoding='utf8').read()
    text = text.replace('test -L unit.py', 'test -e unit.py').replace(' · .gitignore', '').replace('the room 01_task exists', 'the room exists')
    text = text.replace('files      : GOAL.md', 'files      : TASK.md · GOAL.md')
    open(units, 'w', encoding='utf8').write(text)
    for name in ('RULE.md', 'measure.py', 'audit.py'):
        os.symlink(os.path.join(HECTOLINE, name), os.path.join(folder, name))
    with open(os.path.join(folder, 'unit.py'), 'w', encoding='utf8') as f:
        f.write(WRAPPER.format(hectoline=HECTOLINE, review=os.path.join(HERE, 'review.py'), run=run))
    os.chmod(os.path.join(folder, 'unit.py'), 0o755)
    settings = os.path.join(folder, '.claude', 'settings.json')
    os.makedirs(os.path.dirname(settings), exist_ok=True)
    import install
    install.claude_hooks(settings)
    data = json.load(open(settings))
    data['hooks'].setdefault('PreToolUse', []).append({'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': f'python3 -I -B {os.path.join(HERE, "review.py")} hook', 'timeout': 30}]})
    json.dump(data, open(settings, 'w'), indent=2)
    git = lambda *a: sh(['git', '-C', folder, *a], env=env)
    git('add', 'GOAL.md', 'OWNER.md', 'PLAN.md', 'PRODUCTS.md', 'RESEARCH.md', 'UNITS.md', 'unit.log', 'RULE.md', 'measure.py', 'audit.py', 'unit.py', 'TASK.md')
    git('commit', '-q', '--amend', '-m', 'U0001 the room exists with its ledgers, its links, this block')
    os.symlink(os.path.join(HECTOLINE, 'hooks', 'pre-commit'), os.path.join(folder, '.git', 'hooks', 'pre-commit'))
    validate = sh([sys.executable, '-I', '-B', os.path.join(folder, 'unit.py'), 'validate', folder], env=env, check=False).strip().splitlines()[-1]
    pile = sh([sys.executable, '-I', '-B', os.path.join(folder, 'unit.py'), 'pile', folder], env=env, check=False).strip().splitlines()[-1]
    return git('rev-parse', 'HEAD').strip(), validate, pile


def prompt_of(arm):
    text = CONFIG['task_text']
    if arm == 'hectoline':
        text += '\n\n' + CONFIG['hectoline_text']
    return text


def session(folder, arm, env, out_path):
    cmd = ['claude', '-p', prompt_of(arm), '--model', CONFIG['model'], '--max-turns', str(CONFIG['max_turns']),
           '--output-format', 'json', '--permission-mode', 'dontAsk',
           '--allowedTools', *CONFIG['allowed_tools'], '--disallowedTools', *CONFIG['disallowed_tools'],
           '--setting-sources', 'project']
    start = time.time()
    with open(out_path + '.stderr', 'w') as err:
        proc = subprocess.Popen(cmd, cwd=folder, env=env, stdout=subprocess.PIPE, stderr=err, text=True, start_new_session=True)
        timed_out = False
        try:
            out, _ = proc.communicate(timeout=CONFIG['wall_s'])
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                out, _ = proc.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                out, _ = proc.communicate()
    wall = round(time.time() - start, 1)
    try:
        data = json.loads(out)
    except ValueError:
        data = {'result': out or '', 'parse_error': True}
    data.update(wall_s=wall, timed_out=timed_out, exit_code=proc.returncode)
    json.dump(data, open(out_path, 'w'), indent=1)
    return data


def claimed_of(result):
    lines = [l.strip() for l in str(result).strip().splitlines() if l.strip()]
    found = re.search(r'FIXED:\s*(yes|no)\b', lines[-1], re.I) if lines else None
    return found.group(1).lower() if found else 'none'


def prediction(folder, base, arm, task, results):
    """git add -A, then the diff of the index against the base tree, ledger and harness paths excluded; the index is reset after."""
    git = lambda *a: sh(['git', '-C', folder, *a])
    git('add', '-A')
    excludes = [f':(exclude){p}' for p in CONFIG['ledger_paths']]
    patch = git('diff', '--cached', '--no-color', base, '--', '.', *excludes)
    git('reset', '-q')
    os.makedirs(os.path.join(results, 'patches'), exist_ok=True)
    with open(os.path.join(results, 'patches', f'{task["instance_id"]}.{arm}.diff'), 'w', encoding='utf8') as f:
        f.write(patch)
    with open(os.path.join(results, f'predictions.{arm}.jsonl'), 'a', encoding='utf8') as f:
        f.write(json.dumps({'instance_id': task['instance_id'], 'model_name_or_path': arm, 'model_patch': patch}) + '\n')
    return patch


def room_measures(folder, run):
    """Units closed, units failed, audits closed, failed review rounds, hook denies, from the ledgers and the log alone."""
    from ledger import load, review_record
    text, bl = load(folder)
    types = dict(re.findall(r'^## (U\d{4}) · \S+ · (\w+) ·', text, re.M))
    out = {'units_closed': 0, 'units_failed': 0, 'audits_closed': 0, 'units_open': 0, 'reviews_pass': 0, 'reviews_fail': 0, 'reviews_none': 0}
    for uid, status, _, vals in bl:
        if uid == 'U0001':
            continue
        if status == 'closed' and types.get(uid) == 'audit':
            out['audits_closed'] += 1
        elif status == 'closed':
            out['units_closed'] += 1
        elif status == 'failed':
            out['units_failed'] += 1
        elif status in ('open', 'waiting'):
            out['units_open'] += 1
    reviews = os.path.join(run, 'reviews')
    if os.path.isdir(reviews):
        for name in os.listdir(reviews):
            if name.endswith('.json'):
                for r in json.load(open(os.path.join(reviews, name)))['rounds']:
                    out['reviews_' + (r['verdict'] if r['verdict'] in ('pass', 'fail') else 'none')] += 1
    history = open(os.path.join(folder, 'unit.log'), encoding='utf8').read().splitlines() if os.path.exists(os.path.join(folder, 'unit.log')) else []
    out['log_denies'] = sum(1 for l in history if ' | deny | ' in l)
    out['log_lines'] = len(history)
    return out


def run_one(task, arm, work, results, env, setup_only=False):
    run = os.path.join(work, task['instance_id'], arm)
    folder = os.path.join(run, 'repo')
    if os.path.exists(run):
        shutil.rmtree(run)
    os.makedirs(run)
    line = {'instance_id': task['instance_id'], 'repo': task['repo'], 'arm': arm, 'model': CONFIG['model'], 'max_turns': CONFIG['max_turns'], 'wall_cap_s': CONFIG['wall_s'], 'started': now()}
    subject = f'base {task["base_commit"]} with TASK.md'
    base = fetch(task, folder, subject)
    if arm == 'hectoline':
        base, validate, pile = make_room(task, folder, run, env)
        line.update(room_validate=validate, room_pile=pile)
        log(results, f'{task["instance_id"]} {arm}: room at {base[:10]}, {validate}, {pile}')
    line['base'] = base
    if setup_only:
        line['ended'] = now()
        return line
    out_path = os.path.join(results, 'sessions', f'{task["instance_id"]}.{arm}.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    log(results, f'{task["instance_id"]} {arm}: session start')
    data = session(folder, arm, env, out_path)
    patch = prediction(folder, base, arm, task, results)
    line.update(ended=now(), wall_s=data.get('wall_s'), timed_out=data.get('timed_out'), exit_code=data.get('exit_code'),
                turns=data.get('num_turns'), session_id=data.get('session_id'), cost_usd=data.get('total_cost_usd'),
                claimed=claimed_of(data.get('result', '')), result_tail=str(data.get('result', '')).strip()[-300:],
                patch_lines=len(patch.splitlines()), patch_files=len(re.findall(r'^diff --git ', patch, re.M)),
                is_error=data.get('is_error'), terminal_reason=data.get('terminal_reason'))
    if arm == 'hectoline':
        line.update(room_measures(folder, run))
        keep = os.path.join(results, 'ledgers', task['instance_id'])
        os.makedirs(keep, exist_ok=True)
        for name in ('UNITS.md', 'GOAL.md', 'PLAN.md', 'PRODUCTS.md', 'OWNER.md', 'RESEARCH.md', 'unit.log'):
            if os.path.exists(os.path.join(folder, name)):
                shutil.copy(os.path.join(folder, name), os.path.join(keep, name))
        if os.path.isdir(os.path.join(run, 'reviews')):
            shutil.copytree(os.path.join(run, 'reviews'), os.path.join(keep, 'reviews'), dirs_exist_ok=True)
    with open(os.path.join(results, 'runs.jsonl'), 'a', encoding='utf8') as f:
        f.write(json.dumps(line) + '\n')
    log(results, f'{task["instance_id"]} {arm}: done, claimed {line["claimed"]}, turns {line["turns"]}, wall {line["wall_s"]} s, patch {line["patch_lines"]} lines')
    return line


def main(argv):
    tasks_path, work, results = (os.path.abspath(a) for a in argv[:3])
    rest = argv[3:]
    only = [rest[i + 1] for i, a in enumerate(rest) if a == '--task']
    arms = [rest[i + 1] for i, a in enumerate(rest) if a == '--arm'] or ['plain', 'hectoline']
    setup_only = '--setup-only' in rest
    given = next((rest[i + 1] for i, a in enumerate(rest) if a == '--pybin'), None)
    os.makedirs(work, exist_ok=True)
    os.makedirs(results, exist_ok=True)
    env = session_env(work, pybin(work, given))
    tasks = [t for t in json.load(open(tasks_path))['tasks'] if not only or t['instance_id'] in only]
    done = set()
    runs = os.path.join(results, 'runs.jsonl')
    if os.path.exists(runs) and not setup_only:
        done = {(json.loads(l)['instance_id'], json.loads(l)['arm']) for l in open(runs) if l.strip()}
    log(results, f'harness start: {len(tasks)} tasks, arms {arms}, model {CONFIG["model"]}, max-turns {CONFIG["max_turns"]}, wall {CONFIG["wall_s"]} s, {len(done)} runs already recorded')
    for task in tasks:
        todo = [a for a in arms if (task['instance_id'], a) not in done]
        if not todo:
            continue
        if not setup_only:
            wait_for_load(results)
        threads, errors = [], []

        def go(arm):
            try:
                run_one(task, arm, work, results, env, setup_only)
            except Exception as e:  # one failed run never stops its pair
                errors.append((arm, repr(e)))
                log(results, f'{task["instance_id"]} {arm}: ERROR {e!r}')
        for arm in todo[:CONFIG['parallel_runs']]:
            t = threading.Thread(target=go, args=(arm,))
            t.start()
            threads.append(t)
            time.sleep(5)
        for t in threads:
            t.join()
    log(results, 'harness end')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
