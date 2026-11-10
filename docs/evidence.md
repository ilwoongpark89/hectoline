# Evidence

Three cases from the author's rooms. Each carries its date and its count. Each names the command that produced the count and the ledger lines that hold it. The rooms themselves are private. Every quoted line is verbatim from the ledger named. Counted on 2026-11-08.

## 1. The rule kept to the letter: 23 sentences on one line, audits of 18 lines

The rule room ran the method on itself. Its `RULE.md` is product P08 with a cap of 500 lines, RULE §0 «A leaf P holds at most 500 lines».

### The rule file

| date | commit | RULE.md lines | most sentences on one line | that line |
|---|---|---|---|---|
| 2026-11-05 | d01d02b | 104 | 23 | 66, §4 «The block exists before the first edit …» |
| 2026-11-05 | 225e25a | 104 | 23 | 66 |
| 2026-11-07 | 1dee0eb | 104 | 23 | 66 |
| 2026-11-07 | 136da77 | 104 | 23 | 66 |

Command, run on each commit of the private rule room:

```sh
git show $COMMIT:RULE.md | wc -l
git show $COMMIT:RULE.md | python3 -I -c "
import sys, re
for i, l in enumerate(sys.stdin.read().split(chr(10)), 1):
    t = re.sub(r'«[^»]*»', '«»', l); t = re.sub(r'\x60[^\x60]*\x60', 'C', t)
    n = len([s for s in re.split(r'(?<=[.!?])\s+', t.strip()) if s.strip()])
    if n > 20: print(n, 'sentences on line', i)"
```

Output on each of the four commits: `23 sentences on line 66`. The line begins «- The block exists before the first edit of any file it names. `unit.py open` appends the block from four texts, sentence, plan, files and lines, or turns its planned block open. That edit is the block.» and runs to «The author reads the pack and greps the ledgers, never the ledgers whole.» The public `RULE.md` here keeps that line at 23 sentences.

The excuse audit of 2026-11-07 12:00, `result.rule-excuses.txt`, read every line of the 104 and classed each sentence. Its legend: «classes: E enforced by a tool · R judged by a reviewer · P proxy, passable by form · N no mechanism, never fired · L declared done by a label». Count by `grep -c '^N '` → 14 lines. Quoted fragments on those lines by `grep '^N ' | grep -o '«[^»]*»' | wc -l` → 29. The owner row A0117 of 2026-11-07 that ordered the audit reads in its refined cell: «The excuse audit of RULE.md, result.rule-excuses.txt: 27 sentences without a mechanism, 6 proxies, the six numbers of §0 all violated. Each gets a tool or leaves the rule.»

### The audits

The four audit units closed between 2026-11-05 and 2026-11-07. The counts come from `git show --numstat --format= $COMMIT` in the private rule room. The keys of their `UNITS.md` blocks confirm them:

| unit | date | commit | UNITS.md added, deleted | other files | lines key | result key |
|---|---|---|---|---|---|---|
| U0286 | 2026-11-05 | d01d02b | 18, 18 | the log, 136 appended | `+0 ~18 −0 moved 0, by numstat at close` | `check exits 0 0 · UNITS.md +18 −18` |
| U0297 | 2026-11-05 | 225e25a | 18, 18 | the log, 68 appended | `+0 ~18 −0 moved 0, by numstat at close` | `check exits 0 · UNITS.md +18 −18` |
| U0310 | 2026-11-07 | 1dee0eb | 21, 0 | the log, 140 appended | `+21 ~0 −0 moved 0, by numstat at close` | `check exits 0 0 0 · UNITS.md +21 −0` |
| U0321 | 2026-11-07 | 136da77 | 18, 18 | the log, 63 appended | `+0 ~18 −0 moved 0, by numstat at close` | `check exits 0 0 0 · UNITS.md +18 −18` |

Each files key names `UNITS.md` and the log only. The U0286 key: `files      : UNITS.md:5994,5997-6013 · unit.log:18406-18541, from git diff -U0 at close`. Each audit reran every closed check on a copy and listed its findings in the added key. None changed a rule line or a tool. On 2026-11-08 the ledger of the rule room held 393 unit blocks and 34 closed audit blocks. Its repository held 392 commits. The commands: `grep -c '^## U' UNITS.md`, `grep -c '· audit · closed$' UNITS.md` and `git log --oneline | wc -l`.

## 2. The landing page: 5,570 dead lines of 6,487

The landing-page room of the author's web project froze the shipped landing page and measured it on 2026-11-07. `GOAL.md` line 7, the total:

> «landing-page/: 34 files, 6,487 lines of tsx, css and ts (`find legacy/landing-page -type f \( -name '*.tsx' -o -name '*.css' -o -name '*.ts' \) -print0 | xargs -0 cat | wc -l`). The route app/page.tsx reaches 6 files, 1,846 lines: page.tsx 17, relaunch.tsx 541, relaunch.module.css 945, sections/install.tsx 44, sections/install.module.css 23, landing-shared.module.css 276. The other 28 files, 4,641 lines, are reached by nothing: the landing before the relaunch of 2026-10-08.»

`GOAL.md` line 8, the catalogs:

> «i18n: ko/landing.ts 1,242 lines, en/landing.ts 1,040. The reachable files read the namespaces relaunch and cta only (`git grep -l -P "landing\.NS(\.|\b)"` per namespace on 9921f74bf). The nine others, nav, hero, pain, showcases, realtime, features, security, midCta and heroDemo, are 563 ko + 366 en = 929 dead lines, each catalog's closing «};» line being its tail, not a namespace line. Dead lines in all: 4,641 + 929 = 5,570.»

`GOAL.md` line 31, the goal row:

> «| G1 | no dead line ships | G0 | lines of the shipped landing that the route app/page.tsx does not reach, files by the import walk, catalog lines by the namespaces the reached files read, by measures.py g1 | 0 | 5,570, U0004 |»

The tool is `measures.py` of that room, entered by unit U0004 on 2026-11-07, commit b83b2c2. Its measure:

```python
def g1(room=None, bl=None):  # lines of the shipped landing the route does not reach: files by the import walk, catalog lines by namespace
    live, tree = reached(room)
    read = {m for rel in live for m in re.findall(r'landing\.(\w+)', tree[rel])}
    dead = sum(t.count('\n') for rel, t in tree.items() if rel not in live and not rel.startswith('app/lib/i18n'))
    return dead + sum(n for rel, t in tree.items() if rel.startswith('app/lib/i18n') for name, n in namespaces(t) if name not in read)
```

Command and output, 2026-11-07 in the U0004 check clause and again on 2026-11-08:

```sh
python3 -I -B measures.py g1   # g1 5570
python3 -I -B measures.py g2   # g2 5, files over 500 lines
```

The target is 0. The count stands at 5,570 on 2026-11-08.

## 3. The document built from 23 % of its 184 sources

The author's company room holds a wiki of source digests, one node file per source. On 2026-11-07 its unit U0525, commit bfbd685, recorded in its cause key: «all 184 node files match «# <id> · » at HEAD, 184 header ids sit in a row». Count on 2026-11-08:

```sh
find wiki -path '*nodes*' -name '*.md' | wc -l                       # 185
grep -l '^# [A-Za-z0-9]* · ' $(find wiki -path '*nodes*' -name '*.md') | wc -l   # 184
```

On 2026-11-07 the agent of that room was asked to write the company document from the 184 digests it had prepared. The owner ledger of the application room records the exchange as row A0028 of 2026-11-07, in its English cells:

> «with a pasted cooling-company exchange: the agent proposed re-reading 184 sources with 8 agents, then admitted it had used only the answer cell, 23 % of the nodes, and blamed the sources»

> «Evasion by manufactured difficulty is the same mechanism …»

Count: 184 sources prepared, 23 percent used, one proposal to read all 184 again.

## The one shape

In each case the loop closed on a signal the agent produced itself. A rule file under its cap. An audit that exited zero. A document delivered. The counts above are what an outside reader can check.
