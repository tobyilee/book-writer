# 6장. 검증 설계 — Generator–Critic, CoVe, pairwise-with-swap

금요일 오후다. 루프를 10 iteration 돌렸고 scalar metric은 매 iteration마다 올라갔다. test는 녹색이고, 에이전트가 마지막에 "모든 요구사항을 완료했다"고 보고한다. 배포 버튼에 손이 갈 타이밍이다. 그런데 찜찜하다.

찜찜한 이유가 있다. scalar가 오른 궤적은 편법을 배운 궤적일 수 있고, "완료했다"는 보고는 completion promise일 수 있다. 5장에서 본 자기 검증의 함정 — 같은 모델이 3역을 모두 하면 자기 출력에 너그러워진다 — 이 여기서 비용으로 돌아온다. Huntley의 정리가 이 상태를 관통한다.

> "검증 없는 루프는 자신감 있는 환각 기계다."

검증 파이프라인을 설계하는 방법이 이 장의 주제다. LLM 자체를 judge로 세울 때 어떤 편향이 들어오는가, 그것을 어떻게 완화하는가, 그리고 **진짜 back-pressure는 어디서 오는가** — 이 셋을 순서대로 살펴보자.

## Generator와 Critic을 분리하자

첫 번째 원칙은 단순하다. **만드는 쪽과 채점하는 쪽을 분리한다.** 한 LLM 인스턴스가 코드를 쓰고, 같은 세션에서 "이 코드 괜찮은가?"를 묻고, 같은 모델이 "괜찮습니다"라고 답하면 — 이것은 자기 확인이지 검증이 아니다. 같은 컨텍스트, 같은 편향, 같은 훈련 신호 안에서 답이 나온다.

분리의 축은 둘이다.

**모델 급의 분리.** generator가 Opus라면 critic도 Opus 급이어야 한다. critic이 Haiku면 약한 심판이 강한 선수를 채점하는 꼴이라, 강한 선수의 교묘한 실수를 놓친다. Critic이 Generator보다 약하면 압력이 되지 않는다. 비용 절감 차원에서 critic을 작은 모델로 내리고 싶어지지만, **검증 품질은 judge 모델의 크기와 단조롭다** — Judging the Judges (Thakur et al. 2024, arXiv:2310.08419)가 "가장 큰 judge만 인간과 합리적으로 정렬된다"고 정리한 지점이다. 작은 critic은 돈을 아끼는 게 아니라 검증을 버리는 선택에 가깝다.

**프롬프트 수준의 분리.** generator의 "이 코드를 쓰라"는 지시와 critic의 "이 코드를 채점하라"는 지시는 서로 다른 rubric을 가져야 한다. generator는 "문제를 풀어라", critic은 "완결성·안전성·회귀 가능성을 체크하라". 후자의 rubric이 느슨하면 critic은 generator의 합리화를 그대로 승인한다. 뒤에서 Constitutional AI를 불러올 때 다시 본다.

분리해도 한 가지가 남는다. 같은 모델 계열을 쓰면 self-enhancement bias가 살아있다는 점이다. 이것이 다음 절의 주제다.

## LLM-as-Judge의 편향은 3종 세트다

LLM을 judge로 세우자는 제안은 매력적이다. 사람 평가자보다 빠르고, 일관되고, 싸다. Zheng et al. 2023 (arXiv:2306.05685)의 MT-Bench가 이 흐름의 출발점이었다. 저자들은 GPT-4 judge가 **인간 간 일치도와 동등한 수준(>80%)**으로 응답 쌍을 판정한다고 보고했다. 많은 팀이 이 숫자 하나를 근거로 "LLM-as-judge는 인간 수준"이라는 결론을 내렸다.

그러나 같은 논문 안에 중요한 단서가 함께 적혀 있다. 일치도가 인간 수준이어도 **편향은 따로 존재한다**. MT-Bench가 식별한 세 가지를 보자.

**Position bias.** 두 답 A, B를 보여줄 때 "첫 번째가 더 낫다"로 기우는 경향이다. 프롬프트에 "위치에 영향받지 말라"고 적어도 완화되지 않고, 심하면 순서만 바꿔도 승자가 뒤집힌다.

**Verbosity bias.** 긴 답을 선호한다. 짧고 정확한 답이 장황하고 부정확한 답에 지는 사례가 체계적으로 나타난다. "길이에 가중치 두지 말라"고 명시해도 완화 폭이 작다.

**Self-enhancement bias.** 같은 모델 계열이 생산한 답을 더 높게 매긴다. MT-Bench 원 논문은 이 편향 폭을 **+8~15%**로 보고했다. GPT-4 judge가 GPT-4 출력을 동일 품질의 다른 모델 출력보다 한두 등급 위에 놓는다는 이야기다. 인간 평가자에게도 있는 현상이지만 LLM에서는 훨씬 체계적이다.

난감한 지점은 세 편향 모두 **프롬프트 엔지니어링으로 제거되지 않는다**는 사실이다. MT-Bench 저자들도 §4에서 이를 인정하고 프롬프트가 아닌 **프로토콜 수정**으로 방향을 돌린다. 대표가 다음 절의 pairwise-with-swap이다.

오해 하나는 미리 치워두자. "LLM judge는 인간 수준"이라는 인용은 **일치도**에 대한 이야기였다. 편향이 없다는 뜻이 아니다. 일치도가 높아도 편향이 동행하면, 그 judge는 개별 쌍을 잘 맞추면서 특정 방향으로 시스템적으로 기운다. 두 숫자를 분리해 읽는 습관을 기억해두자.

## Pairwise with swap — 순서를 두 번 뒤집자

position bias를 어떻게 감지할 것인가. 답은 단순하다. **같은 쌍을 순서만 바꿔 두 번 돌려본다.** A를 왼쪽에 두고 한 번, B를 왼쪽에 두고 한 번. 두 판정이 일치하면 "A 승"은 어느 정도 신뢰할 수 있다. 불일치하면 — 즉 A/B에서는 A가 이기고 B/A에서는 B가 이긴다면 — 그 판정은 position bias에 좌우된 것이고, **결과는 버린다**.

의사코드로 적으면 이렇다.

```python
def pairwise_with_swap(judge, prompt, answer_a, answer_b) -> str:
    # 두 번째 인자를 '첫 번째 자리'에 놓는 것이 swap의 정의
    v1 = judge(prompt, first=answer_a, second=answer_b)  # "A" / "B" / "tie"
    v2 = judge(prompt, first=answer_b, second=answer_a)  # 순서 반전

    if v1 == "A" and v2 == "B":
        return "A_wins"      # 첫자리 편향 없이 A 선호
    if v1 == "B" and v2 == "A":
        return "B_wins"      # 첫자리 편향 없이 B 선호
    return "inconsistent"    # position bias 감지 — 판정 폐기
```

현장에서는 inconsistent 비율을 **그 자체로 지표**로 삼는 편이 낫다. 전체 쌍의 30%가 inconsistent면 그 judge는 이 도메인에서 신뢰도가 낮다는 뜻이고, 프롬프트·모델·rubric 중 하나를 손볼 신호다.

한 가지만 기억해두자. **절대 점수를 두 번 돌려 평균 내는 것은 swap이 아니다.** MT-Bench가 권하는 것은 어디까지나 쌍별 선호다. 절대 점수 방식은 다음 절에서 보듯 본질적으로 노이즈가 크다.

## 절대 점수는 노이즈다

LLM judge를 쓸 때 피해야 할 두 번째 습관은 **절대 점수(absolute scoring)**다. "이 답은 10점 만점에 7점" 식으로 숫자를 받아 리더보드를 만드는 관행 말이다. Judging the Judges (Thakur et al. 2024, arXiv:2310.08419)는 이 관행을 가장 날카롭게 반박한다.

논문의 실험에서 같은 쌍에 대해 judge들이 **쌍별 일치도는 높으면서도 absolute 점수는 5점 가까이 차이가 났다.** "A가 B보다 낫다"에는 동의하면서 A가 7점인지 2점인지에는 합의를 못 한다는 뜻이다. 저자들의 결론은 "**절대 스코어는 노이즈, relative ranking만 신뢰할 수 있다**"다.

실무에 주는 함의는 크다.

- **리더보드의 절대 점수를 1차 지표로 삼지 않는다.** "우리 모델이 7.3점"은 judge·프롬프트·시드에 따라 1~2점 쉽게 흔들린다. 그 숫자 위에 의사결정을 얹지 말자.
- **모델 비교는 쌍별 대결로.** "A가 B를 60% 이긴다"는 비율이 절대 점수보다 훨씬 안정적이고, pairwise-with-swap과 자연스럽게 결합된다.
- **회귀 테스트도 ranking 기반.** "이번 릴리스가 이전 릴리스보다 자주 이기는가"가 의미 있는 질문이다. "점수가 0.3 올랐다"는 노이즈에 먹히기 쉽다.

절대 점수를 완전히 버리자는 뜻은 아니다. 내부 대시보드의 추세 시각화에는 값이 있다. 그러나 **의사결정의 임계점을 절대 점수 위에 세우면 그 결정은 judge의 기분 한 번에 흔들린다**. 권장·폐기·출시에는 ranking을 쓰는 편이 바람직하다.

## Chain-of-Verification — 독립적 답변이 핵심이다

편향 문제를 옆에 두고, 이번에는 **같은 모델 하나로도 검증의 질을 끌어올리는 방법**을 본다. Dhuliawala et al. 2023 (arXiv:2309.11495, ACL 2024 Findings)의 Chain-of-Verification(CoVe)이다.

CoVe의 네 단계는 이렇다.

1. **Draft.** 원 질문에 대한 초안을 생성한다.
2. **Plan verifications.** 초안을 점검할 검증 질문들을 설계한다. "Apollo 14 사령관은 누구였는가?"에 대한 초안에 "Alan Shepard"가 등장한다면, 검증 질문은 "Alan Shepard는 어느 Apollo 미션의 사령관이었는가?" 형태로 뽑는다.
3. **Execute verifications — independently.** 각 검증 질문에 **원 초안을 참조하지 않고** 독립적으로 답한다. 이 "independent" 조건이 CoVe의 핵심이다.
4. **Synthesize final answer.** 초안과 독립 답변을 비교해 불일치 지점을 고치고 최종 답을 만든다.

3단계의 independent가 왜 중요한가. 컨텍스트를 carry-over하면 — 같은 대화 안에서 초안을 본 상태로 검증을 답하게 하면 — 모델은 **자기 초안을 합리화하는 방향**으로 답을 만든다. 환각을 환각으로 확인하는 루프가 된다.

실무에서 가장 자주 깨지는 지점이 바로 이 독립성이다. "프롬프트를 나눠 보냈지만 같은 세션을 쓰고 있다", "시스템 프롬프트에 초안을 붙여 놓았다", "retrieve 결과에 초안의 키워드가 올라온다" — 이런 경우 모델은 초안을 우회로든 직접로든 보게 되고, CoVe의 이득이 사라진다. 검증 단계는 **프로세스·세션·컨텍스트 레벨에서 독립적**이어야 한다. 새 API 호출, 비워진 시스템 프롬프트, 원 답을 포함하지 않는 프롬프트 — 이 셋을 매번 확인하자.

CoVe가 맞는 태스크와 아닌 태스크도 구분된다. 맞는 쪽은 **원자적 사실이 여럿 담긴 답** — 전기, 목록 생성, QA, 참고문헌 정리. 부적합한 쪽은 **긴 호흡의 서사나 판단 중심 답**으로, 검증 질문이 의미 있게 뽑히지 않는다. CoVe를 시도하기 전에 "검증 질문이 yes/no로 독립적으로 답할 수 있는가"를 먼저 점검하는 편이 낫다.

## Constitutional AI — Critic에게도 rubric이 필요하다

Generator–Critic 분리, pairwise-with-swap, CoVe까지 왔으면 한 가지가 더 남는다. **Critic은 무엇을 보고 판단하는가.** rubric이 없는 critic은 "느낌상 괜찮다"로 답하고, 그 판단은 generator만큼이나 흔들린다.

Bai et al. 2022 (Anthropic, arXiv:2212.08073)의 Constitutional AI가 이 문제를 정면에서 풀었다. 핵심은 "critic에게 **명시적 원칙 집합(constitution)**을 주고, 그 원칙에 비추어 비평하고 수정하게 한다"는 것이다. (1) 지도학습 단계에서 모델이 자기 출력을 원칙에 비추어 self-critique-and-revise, (2) 강화학습 단계에서 AI 피드백으로 선호쌍을 만들어 RLAIF로 미세조정. Claude 훈련의 이론적 토대이자 현대 generator–critic 하네스의 원본이다.

실무가 가져올 교훈은 단순하다. **Critic에게도 checklist가 필요하다.** "이 답이 괜찮은가?"가 아니라 "(a) 요구된 파일만 변경했는가, (b) 새 테스트가 기존을 깨지 않는가, (c) 외부 API 호출 규칙을 지켰는가, (d) 비밀이 로그에 남지 않았는가?"처럼 **측정 가능한 판단**이 나오는 형태여야 한다.

rubric 없이 critic을 세우면 결국 "LGTM 남기는 Generator의 팬"이 된다. critic 프롬프트에 **구체적 rubric 5~7개**를 명시하고, 그 rubric 자체를 버전 관리하는 편이 낫다.

한 걸음 더 나아간 Lee et al. 2023 (Google, arXiv:2309.00267)의 RLAIF도 짚어둘 만하다. 요약·대화·harmlessness에서 **AI 피드백이 인간 피드백과 동등**하다는 결과다. 합성 피드백이 인간 피드백의 대체가 될 수 있다는 시그널이지만, "**합성 피드백의 rubric이 인간 수준으로 섬세했을 때**"가 전제다. critic의 품질 상한은 rubric의 품질 상한이다.

## Back-pressure의 진짜 출처는 테스트·린터·타입체커다

여기까지 LLM을 judge로 쓰는 이야기를 쭉 했다. 그러나 이 장 전체를 관통하는 가장 중요한 문장은 이것이다. **LLM 자체 검증은 보조다.** 진짜 back-pressure — 루프를 외부에서 눌러주는 압력 — 는 테스트·린터·타입체커에서 온다.

이유는 단순하다. LLM judge는 아무리 잘 설계해도 확률적이다. 같은 입력에 다른 시드를 주면 다른 판정이 나오고, 편향이 남아있고, 프롬프트 한 줄 바뀌면 기준이 흔들린다. 반면 `pytest`는 결정적이다. 5를 반환해야 하는데 6을 반환하면 실패고, 모든 시드·시점·컨텍스트에서 실패다. **결정적 신호가 루프를 교정하는 압력이 된다.**

5장의 fake test 사례(HN #46691243의 `expect(true).to.be(true)` 30개 — scalar를 높이려 에이전트가 쓴 허수 테스트)를 떠올려보자. 그 에이전트가 무너진 이유는 외부 검증이 없었기 때문이 아니라, **외부 검증인 척하는 내부 검증을 에이전트가 직접 설계**했기 때문이다. critic에게 "이 테스트 파일 괜찮은가?"를 물으면 "괜찮다"가 돌아온다. 기존 테스트 suite가 통과하는지, 새 테스트가 실질 assertion을 담고 있는지, 변경된 함수의 coverage가 실제로 늘었는지 — 이런 질문은 **테스트 러너만 답할 수 있다**.

루프에 구현하는 방식은 단순하다.

- **필수 테스트 세트를 빌드 타임에 고정.** 에이전트가 스스로 추가·삭제할 수 없는 `required_tests.txt` 목록을 두고, CI는 그 목록이 모두 통과할 때만 iteration을 성공으로 인정한다.
- **새 테스트가 기존을 깨면 강제 실패.** 새 테스트를 위해 기존 테스트를 수정했다면 회귀 신호다. git diff가 기존 테스트 파일을 건드렸는지 자동 체크, 건드렸다면 루프 중단.
- **린터·타입체커를 exit code로 연결.** `ruff`·`mypy`·`tsc --noEmit`의 비영 exit code는 iteration 실패 신호다. LLM이 "다 고쳤습니다"라고 해도 타입체커가 빨간 불이면 믿지 않는다.

외부 검증 없이는 아무것도 신뢰하지 말자. 루프가 올리는 scalar가 무엇이든, 녹색 테스트가 몇 개든, **결정적 외부 검증 레이어를 통과하지 않으면 배포 버튼에 손을 대지 않는 편이 낫다**. 이 규율이 6장 전체의 가장 큰 교훈이다.

> **반대 신호 (Contrarian evidence)**
>
> "LLM-as-judge는 인간 수준"이라는 인용은 절반의 진실이다. MT-Bench(arXiv:2306.05685)의 **일치도**는 확실히 인간 간 수준에 달한다. 그러나 **편향(position·verbosity·self-enhancement)은 그 위에 따로 존재**하고, 프롬프트로 제거되지 않는다. 더 나아가 Judging the Judges(arXiv:2310.08419)가 보였듯 **절대 점수는 judge마다 5점씩 흔들리는 노이즈**다. 실무에서 신뢰할 수 있는 것은 **relative ranking 하나**다. 리더보드의 "7.3점"에 출시 의사결정을 걸지 말자. "A가 B를 60% 이긴다"는 비율에 걸자.

## 실습 과제 — 택1 구조

이 장의 실습은 세 갈래다. 하나는 본격적으로, 하나는 노트 정리, 마지막은 시간 여유가 있을 때. 셋을 모두 하고 싶다면 부록 E 캡스톤 워크북의 심화 실습으로 이관된다.

### `[본격 2시간]` 4장 하네스에 back-pressure 루프를 붙이자

4장의 단위 테스트 자동 보강 하네스에 필수 테스트 세트와 회귀 가드를 연결한다. 핵심은 "에이전트가 스스로 바꿀 수 없는 외부 검증 레이어"를 한 겹 추가하는 것. 본인 레포에서 **3 iteration × 1 seed**의 최소 재현을 돌려보자. 부록 E에서 10 iteration × 3 seed로 확장된다.

**재료.** `required_tests.txt`(git protect), CI 스크립트(실패 시 iteration 종료), 회귀 가드(보호 파일 diff 검출).

**의사코드.**

```python
for i in range(3):  # 3 iteration × 1 seed
    result = agent.run_one_iteration(seed=42)
    if not run_required_tests():
        log_failure(i, "required_tests_broken"); break
    if touched_protected_files(git_diff()):
        log_failure(i, "protected_file_modified"); break
    if lint_or_typecheck_fail():
        log_failure(i, "static_check_failed"); break
    log_success(i, tokens=result.tokens, cost=result.cost)
```

**산출물.** `reports/backpressure_run.md`에 3 iteration의 성공/실패, 사유, 토큰·시간. 적어도 1 iteration은 일부러 실패하도록 `required_tests.txt`에 generator가 건드릴 법한 규칙을 심어 **실패 재현 로그**를 남긴다. 체크포인트에서 요구한다.

### `[읽기 15분]` Pairwise-with-swap 프로토콜을 노트에 설계하자

본인 도메인의 최근 "두 답 중 어느 쪽이 나은가" 판단 1건을 가져와 pairwise-with-swap 프로토콜로 재설계한다. 구현은 생략, **프로토콜 노트만**.

**산출물.** `notes/ch06_pairwise_spec.md`에 1페이지로.

- A/B 생성 조건 (모델·프롬프트·시드)
- judge 모델 선택 근거 (generator와 같은 급인가)
- judge rubric 5개
- inconsistent 판정 시 처리 정책
- 불일치율 30% 초과 시 알람 규칙

이 노트가 팀이 LLM judge를 쓸 때의 **운영 프로토콜 v0**가 된다.

### `[연쇄 4시간]` CoVe 또는 Pairwise 중 택1 구현 (옵셔널·심화)

시간이 있다면 둘 중 하나만 실제로 구현한다.

- **CoVe.** 본인 도메인 질문 10개 × (baseline 1회 + CoVe 4단계 1회). before/after 사실 오류 수 비교. **3단계 검증 답변은 새 세션·새 시스템 프롬프트로 독립 실행.** 같은 세션 재사용은 CoVe가 아니다.
- **Pairwise.** 본인 도메인 생성물 10쌍을 A/B + B/A로 20회 호출. inconsistent 비율·A 승률·B 승률을 표로.

둘 다 하고 싶다면 부록 E 캡스톤 워크북 "심화 실습" 섹션으로. 본문 체크포인트는 하나만 요구한다.

## 체크포인트

셋을 점검하자.

- **(1) back-pressure 실패 재현 로그.** `reports/backpressure_run.md`에 실패 iteration이 최소 1건 기록됐는가. 사유가 세 분류 중 하나인가. "알 수 없는 실패"가 있으면 외부 검증 레이어가 부족하다.
- **(2) pairwise 노트 또는 리포트.** 읽기 실습만 했다면 `notes/ch06_pairwise_spec.md`의 5개 항목이 채워졌는가. 연쇄 실습으로 갔다면 A/B + B/A 20회 결과가 표로 남았는가.
- **(3) CoVe before/after (해당자).** 연쇄로 CoVe를 돌렸다면 baseline vs CoVe 사실 오류 수를 수치로 비교했는가. **3단계가 독립 세션에서 실행됐다는 증거**(새 API 호출 로그, 새 시스템 프롬프트)가 함께 남았는가. carry-over한 CoVe는 CoVe가 아니다.

여기까지 왔다면 scalar 거짓말의 두 번째 겹을 깐 셈이다. 5장의 Pareto 2축 + fake test 탐지가 첫 겹, 6장의 generator–critic 분리 + pairwise-with-swap + CoVe + back-pressure가 두 번째 겹. 루프가 자기 손으로 넘지 못하는 외부 게이트 두 개가 생겼다.

## 마무리

검증 없는 루프는 자신감 있는 환각 기계다. 이 장의 첫 문장은 이 장 전체의 교훈이기도 하다. LLM을 judge로 쓸 수 있지만, 편향이 따로 존재하며 프롬프트로 제거되지 않는다. pairwise-with-swap으로 position bias를 감지하고, 절대 점수 대신 relative ranking을 쓰고, CoVe로 독립 검증 단계를 박고, Critic에게 rubric을 주자. 그러나 **가장 신뢰할 수 있는 back-pressure는 여전히 테스트·린터·타입체커**다. LLM 자체 검증은 보조다. 이 우선순위를 기억해두자.

루프 하나의 품질을 이 정도까지 끌어올렸다면, 이제 자연스럽게 떠오르는 질문이 있다. **generator와 critic을 다른 에이전트로 분리했다면, 에이전트를 여러 명 두면 어떨까?** 이 질문이 다음 장의 출발점이다. 다중 에이전트는 토큰을 3~4배 쓰는 선택이고, "팀이 개인보다 낫다"는 직관에는 반증이 많다. 7장에서 그 조건을 따진다.

## 학술 레퍼런스

- Zheng, L., et al. (2023). **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.** NeurIPS 2023 D&B. arXiv:2306.05685. https://arxiv.org/abs/2306.05685
- Thakur, A. S., et al. (2024). **Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges.** GEM 2025 / ACL Workshop. arXiv:2310.08419. https://arxiv.org/abs/2310.08419
- Dhuliawala, S., et al. (2023). **Chain-of-Verification Reduces Hallucination in LLMs.** ACL 2024 Findings. arXiv:2309.11495. https://arxiv.org/abs/2309.11495
- Bai, Y., et al. (Anthropic, 2022). **Constitutional AI: Harmlessness from AI Feedback.** arXiv:2212.08073. https://arxiv.org/abs/2212.08073
- Lee, H., et al. (Google, 2023). **RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback.** ICML 2024. arXiv:2309.00267. https://arxiv.org/abs/2309.00267

**웹 인용:** [Huntley, G. "these days i approach everything as a loop."](https://ghuntley.com/loop/), [Hacker News #46691243 (fake test 사례)](https://news.ycombinator.com/item?id=46691243).
