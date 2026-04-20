# 4장. 루프의 해부학 — Ralph·ReAct·Plan&Execute·Reflexion

금요일 오후에 하네스 하나를 넘겨받았다고 상상해보자. 본체는 `while :; do cat PROMPT.md | claude-code; done` 한 줄. 옆은 T-A-O 반복, 또 옆은 계획 먼저 뽑고 단계별 실행, 마지막은 매 시도 반성문.

네 개 다 "에이전트 루프"다. 섞으면 이상한 일이 벌어진다. Ralph 무한 루프에 ReAct 도구 호출을 끼우면 종료 지점이 흐려지고, Plan-and-Execute 위에 Reflexion 메모리를 얹으면 계획이 뒤집힌다. 찜찜하다. 필요한 건 "더 정교한 루프"가 아니라 **한 루프에 한 가지 역할만** 두는 습관이다.

## Huntley의 진짜 메시지 복원

가장 자주 호출되는 이름은 Geoffrey Huntley의 **Ralph Loop**이다. 커뮤니티 밈은 "무한 루프를 돌리면 모델이 알아서 완성한다"에 가깝다. [Huntley, Ralph Wiggum as a Software Engineer](https://ghuntley.com/ralph/)는 셋을 못 박는다.

첫째, **한 루프에 한 가지만.** *"operator must trust the LLM to decide what's the most important thing."* 나머지는 다음 iteration으로.

둘째, **PLAN/BUILD 분리.** PLANNING은 스펙·코드 갭을 TODO로만 만든다(구현 금지). BUILDING은 계획을 가정하고 구현·테스트·커밋까지 연쇄한다. 한 파일에 밀어 넣으면 모델은 계획을 세우자마자 구현에 손대고 테스트를 건너뛴다.

셋째, **back-pressure가 뼈대다.** 테스트·린터·타입체커가 실패를 되먹이는 구조 위에서만 Ralph가 작동한다. LLM이 쓴 "완료했습니다"는 신호가 아니다.

Ralph Loop의 요지는 무한 루프 찬미가가 아니라 **PLAN/BUILD 분리 + back-pressure**다. "Ralph Wiggum"은 심슨 가족의 천진한 캐릭터 — 멍청한 루프여도 계획과 백프레셔가 받쳐주면 생산적이라는 자조적 선언이다. 기억해두자.

## 4개 루프 패턴 비교

**Ralph Loop.** 동일 프롬프트(PLAN/BUILD) 반복. 상태는 파일·git, 복잡성은 프롬프트·테스트·훅으로 외재화. 적합: refactor·migration·cleanup·conformance처럼 **스크립트로 성공 판별 가능한** 작업.

**ReAct** (Yao et al. 2022, arXiv:2210.03629). Thought-Action-Observation 인터리브. ALFWorld에서 imitation/RL baseline 대비 34%p 개선. 적합: 도구 많은 탐색·분석.

**Plan-and-Execute.** 계획 **1회** + 실행 **N회**. LangChain이 대중화. 적합: 단계가 많고 서로 의존하는 작업.

**Reflexion** (Shinn et al. 2023, arXiv:2303.11366). 시도 → 자기 비평 → 에피소드 메모리 → 다음 시도. 자연어 반성문만으로 HumanEval pass@1 91%. 적합: **피드백이 가능한** 작업.

| 패턴 | 본질 | 대표 출처 | 적합 태스크 | 부적합 신호 |
|------|------|-----------|-------------|------------|
| **Ralph** | PLAN/BUILD + 프롬프트 반복 | Huntley | refactor·migration·cleanup | 사람 눈으로만 판별 |
| **ReAct** | T-A-O 교차 | arXiv:2210.03629 | 도구 많은 탐색 | 도구 호출 거의 없음 |
| **Plan-and-Execute** | 계획 1 + 실행 N | LangChain | 다단 의존 작업 | 요구사항 급변 |
| **Reflexion** | 자기 비평 + 메모리 | arXiv:2303.11366 | 피드백 있는 반복 | 채점기·테스트 부재 |

**작업 유형이 패턴을 고르지, 패턴이 작업을 고르지 않는다.** 도구 호출 없는 리팩토링에 ReAct를 씌우면 Thought만 쏟아지고, 테스트 없는 코드베이스의 Reflexion 반성문은 "다음엔 더 잘하겠습니다"가 된다.

Self-Refine(Madaan et al. 2023, arXiv:2303.17651)은 Reflexion의 사촌뻘(자기 채점 편향은 6장). Tree of Thoughts(Yao et al. 2023, arXiv:2305.10601)는 Game of 24에서 CoT 4% 대 ToT 74%를 보고하지만 비용도 폭발한다. 둘은 5장 "test-time compute"에서 다시 등장한다.

## Karpathy 3요소 재강조

공통 뼈대는 1장의 Andrej Karpathy 3요소([karpathy/autoresearch](https://github.com/karpathy/autoresearch)) — editable asset, scalar metric, time-box. 네 루프 전부가 이 셋 위에 앉는다. Ralph=파일 트리+테스트 통과율+`--max-iterations`, ReAct=workspace+success rate+step 상한, Plan-and-Execute=계획+단계 결과+walltime, Reflexion=에피소드 메모리+pass@1+max_trials.

"어떤 루프"보다 세 요소가 정의됐는지가 먼저다. editable asset이 애매하면 파일을 랜덤하게 건드리고, scalar가 없으면 "잘된 것 같은데"에서 멈추며, time-box가 없으면 예산이 녹을 때까지 돈다. Karpathy의 *"Demo is works.any(), product is works.all()"* 이 이 지점을 찌른다.

## Ralph 적합·부적합 matrix

Ralph는 매우 좁은 영역에서만 강력하다. 가로축 "스크립트로 성공 판별 가능?", 세로축 "판단 의존도가 낮은가?"로 그린다.

|   | **스크립트 판별 가능** | **스크립트 판별 불가** |
|---|---|---|
| **판단 의존도 낮음** | 🟢 **Ralph 최적**<br/>refactor·migration·cleanup | 🟡 Ralph 가능, 검증자 필요<br/>포맷팅·맞춤법 |
| **판단 의존도 높음** | 🟡 Ralph 부분 가능<br/>테스트 보강(커버리지 델타) | 🔴 **Ralph 부적합**<br/>greenfield·UX·아키텍처 판단 |

좌상단 초록칸이 Ralph의 자리다. TypeScript 업그레이드, 폐기된 API 일괄 치환, 코딩 컨벤션 적용처럼 실패·성공 모두 스크립트가 판정하는 작업. 여기서는 Ralph가 밤새 돌며 수백 파일을 고친다.

문제는 우하단이다. [HN #46672413 "Ralph Wiggum Doesn't Work"](https://news.ycombinator.com/item?id=46672413)의 작성자는 greenfield에 Ralph를 붙여 **수백 달러를 태우고 실패**했다. 성공 기준이 스크립트로 정의되지 않았기 때문이다. [HN #46750937 "What Ralph loops are missing"](https://news.ycombinator.com/item?id=46750937)은 Ralph에 **계획·보안·데이터 모델링·성능 체크리스트가 구조적으로 결여**됐다고 지적한다. 무용론이 아니라 "아무 데나 붙이지 말라"는 경고다.

좌하단(테스트 보강 등)은 **scalar를 잘 정의하면** 초록칸으로 당길 수 있다 — 커버리지 델타 + 기존 테스트 통과 guard. 매트릭스는 판결표가 아니라 **내 태스크가 어느 칸에 찍히는지 확인하고 가능하면 scalar 설계로 초록칸으로 당겨 오라**는 운영 지도다.

## 실패 모드 분류

Huntley 커뮤니티·Leanware.co·alteredcraft의 어휘를 현상·원인·대처로 정리한다.

**Overcooking.** scalar는 오르는데 품질은 퇴화. 원인: 루프가 metric을 만족시키려 우회로를 찾는다. 대처: Pareto 2축(5장).

**Undercooking.** 반쪽 기능. 원인: exit hook이 성급히 발동 — 짧은 `--max-iterations`·단일 조건. 대처: exit 조건 복수화(테스트 통과 AND 커버리지 델타 ≥ X), 최소 iteration 하한.

**Completion promise.** 모델이 "완료"를 선언했는데 실제로는 바뀐 게 없거나 잘못된 상태. 원인: LLM 자체 판단을 검증 신호로 썼다. 대처: 외부 검증만 신호로 — 테스트·린터·타입체커·git diff.

**Context pollution.** iteration이 갈수록 반응이 둔해진다. 원인: 3장의 **50% 컨텍스트 규칙** 위반 — Cline 텔레메트리로 200k 광고 컨텍스트라도 실효 품질은 약 100k에서 꺾인다. 대처: 요약·트런케이션·Focus Chain.

네 가지는 따로 오지 않는다. Overcooking이 길어지면 Context pollution이 따라오고, Completion promise가 반복되면 Undercooking이 굳어진다. 이름을 붙여야 대처가 따라온다.

## Exit hook 설계

루프는 언제 멈춰야 할지 모르므로 바깥에서 강제한다. 최소 3종 — 이터레이션 상한, 토큰 상한, 델타 정체.

```bash
MAX_ITERATIONS=20; MAX_TOKENS=150000; DELTA_PATIENCE=3
iter=0; tokens=0; last=0; stagnant=0
while [ $iter -lt $MAX_ITERATIONS ] && [ $tokens -lt $MAX_TOKENS ]; do
  iter=$((iter+1))
  out=$(claude-code --prompt PROMPT.md)
  tokens=$((tokens + $(echo "$out" | jq .usage.total_tokens)))
  pytest -q || { echo "iter=$iter fail: tests red"; continue; }
  scalar=$(coverage report --format=total)
  delta=$((scalar - last)); last=$scalar
  if [ $delta -le 0 ]; then
    stagnant=$((stagnant+1))
    [ $stagnant -ge $DELTA_PATIENCE ] && { echo "exit=stagnation"; break; }
  else stagnant=0; fi
done
echo "exit: iter=$iter tokens=$tokens scalar=$last"
```

`MAX_ITERATIONS`는 Undercooking을 피하려 높게·Overcooking을 피하려 무한 아니게. `MAX_TOKENS`는 예산 상한(10장). 델타 정체는 "수치는 제자리인데 iteration만 돈다"는 overcooking 초기 신호를 잡는다. 패턴이 바뀌어도 구조는 같다 — ReAct는 step 상한, Plan-and-Execute는 단계 walltime, Reflexion은 `max_trials`.

> **반대 신호 (Contrarian evidence): "Ralph Loop 최신·최강"이라는 밈**
>
> **주류:** 돌려두면 알아서 된다.
> **반증:** [HN #46672413](https://news.ycombinator.com/item?id=46672413)은 greenfield Ralph에서 **수백 달러를 태우고 실패**했다고 보고한다. [HN #46750937](https://news.ycombinator.com/item?id=46750937)은 계획·보안·모델링·성능 체크리스트 부재를 구조적 결함으로 지목. Ralph는 "스크립트로 성공 판별 가능한" 영역에서만 강력하다.
> **다룰 방식:** Ralph를 네 패턴 중 하나로만 자리매김, 매트릭스 초록칸에서만 호출. 나머지는 ReAct·Plan-and-Execute·Reflexion 또는 사람의 판단을 섞는다.

## 실습

**실습 1. `[읽기 15분]` 4패턴 매트릭스 매핑.** 자주 돌리는 워크플로 3개를 매트릭스에 점 찍고, 네 패턴 중 무엇을 쓰는지 적어 일치 여부를 확인한다. 산출물: `harness/LOOP_MAP.md`. 체크포인트: "초록칸 Ralph"가 몇 개인가. 나머지는 어떤 검증 신호를 추가해야 당겨 올 수 있는가.

**실습 2. `[본격 2시간]` 단위 테스트 자동 보강 하네스.** editable asset=`tests/`, scalar=커버리지 델타 + 통과 guard, time-box=3분 또는 15k 토큰. 앞 코드 블록을 출발점으로. 산출물: `harness/ralph-test-augment.sh` + `run.log`. 체크포인트: iteration당 몇 줄 추가됐는가. exit 조건 셋 중 무엇이 먼저 발동했는가. Completion promise(`expect(true)` 등)가 발생했는가.

**실습 3. `[읽기 15분]` Reflexion 의사코드 스케치.** 위 하네스를 Reflexion으로 바꾸면 어떻게 달라질지 의사코드로만(실구현은 부록 E). 힌트: iteration 끝에 반성문 한 단락을 `memory/reflections.md`에 append, 다음 프롬프트에 최근 3개만 주입, 반성문 상한 200자. 산출물: `harness/reflexion-sketch.md` 10~15줄. 체크포인트: 공허한 선언을 피하려면 무엇을 주입해야 하는가.

## 체크포인트

세 산출물은 남긴다.

1. **4패턴 매핑** — 실습 1의 `LOOP_MAP.md`.
2. **Ralph vs Reflexion 비교 수치** — 실습 2의 `run.log` + 실습 3 스케치로 토큰·시간·커버리지 델타 추정 한 문단.
3. **Exit hook 발동 로그 1건** — `exit=stagnation`/`max_iterations`/`max_tokens` 중 실제 찍힌 줄. 없다면 조건이 느슨한 것이므로 조여 다시 돌린다.

## 마무리

네 루프의 공통점은 editable asset·scalar·time-box, 차이는 **작업 유형이 패턴을 고른다**는 한 줄. Ralph를 아무 데나 붙이면 돈이 녹는다. 초록칸 바깥이라면 ReAct 또는 Plan-and-Execute로 옮기는 편이 낫다.

다음 질문이 따라온다. scalar 하나로 충분한가. Overcooking에서 봤듯 단일 scalar는 루프가 편법으로 올리는 방향으로 진화한다. Goodhart 법칙과 Pareto 2축 필수성은 5장에서 이어진다.

## 학술 레퍼런스

- Yao, S., et al. (2022). *ReAct*. ICLR 2023. arXiv:2210.03629.
- Shinn, N., et al. (2023). *Reflexion*. NeurIPS 2023. arXiv:2303.11366.
- Madaan, A., et al. (2023). *Self-Refine*. NeurIPS 2023. arXiv:2303.17651.
- Yao, S., et al. (2023). *Tree of Thoughts*. NeurIPS 2023. arXiv:2305.10601.
- Huntley, G. *Ralph Wiggum as a Software Engineer*. https://ghuntley.com/ralph/
- Karpathy, A. *autoresearch*. https://github.com/karpathy/autoresearch
- HN #46672413, #46750937.
