# agent-review-u0004 r1

model claude-opus-5 · session 4baebc0b-8e5d-4433-8d33-46a1982ecf2e · turns 7 · wall 61.6 s · exit 0

## Answer

## U0004 리뷰 결과

**첫 번째 check 절이 작업 트리에서 exit 1 이다.** 블록은 닫을 수 없다.

- **원인**: check 키 자체가 UNITS.md:75 에 리터럴 `## U0005` 를 두 번 담는다. `u.split('## U0005')[1]` 은 U0005 블록이 아니라 check 줄의 나머지 텍스트를 돌려준다. 그 조각은 `" ' in u;b=u.split('"` 이다.
- **결과**: `assert 'A0001 · S03' in b` 와 `assert 'astropy/units/format/cds.py' in b` 가 둘 다 False 다. 확인한 값: `h: True`, `plan: False`, `cds: False`, `nsplit: 4`.
- **고칠 방법**: 절이 헤더 문자열을 리터럴로 담지 않게 한다. 예로 정규식 `re.split(r'^## U0005 ', u, flags=re.M)[-1]` 을 쓰거나, 번호를 변수로 조립한다. 그러면 자기 자신의 텍스트에 걸리지 않는다.
- **두 번째 절은 정상**: 작업 트리에서 exit 0, base 0c40533 에서 exit 1 이다. PLAN.md:11 의 S03 행이 U0005 를 가리킨다.
- **다른 키**: base, duplicate, plan, approval 은 모두 성립한다. base 에서 `grep -c "· planned$" UNITS.md` 는 0 을 출력한다. diff 는 PLAN.md 1 줄, UNITS.md 42 줄로 예산 안에 있다. rejected 의 «4 final units» 는 닫힐 때의 수이며, 지금 최종 블록은 3 개다. 이것만으로는 실패가 아니다.

RULE §4 의 실패 등급 중 «a rule or field that cannot work» 와 §2 의 «each exits non-zero before, 0 after» 에 걸린다.

VERDICT: fail — the first check clause can never pass because its own text puts the literal `## U0005` into UNITS.md, so the split lands inside the check line and both of its asserts fail on the working tree.
