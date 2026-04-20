# 10장. 비용·CI — 자동화된 하네스를 돌리는 엔지니어링

## 월 예산의 50%에서 알람이 오는가

월말에 Anthropic 대시보드를 열었는데 사용량 그래프가 한 달 중반쯤에 이미 절반을 넘어 있는 장면이 떠오른다. 알림은 없었다. 초록색 막대가 노란색으로 바뀌는 순간을 아무도 몰랐고, 그저 누군가가 "이번 달 과금이 좀 많네"라고 Slack에 남긴 메시지로 처음 감지한다. 팀장은 팀원에게 묻고, 팀원은 로그를 뒤진다. 로그 어딘가에 "이 하네스가 돌다가 17,000번 iteration을 돌아서 한나절에 70달러를 태웠다"는 기록이 섞여 있지만 아무도 그 한 줄을 시간축 위에 올려두지 않았다. 난감하다.

앞 장에서는 **위협**을 다뤘다. 외부 공격자와 공급망이 샌드박스 안으로 기어들어 오는 풍경이었다. 이 장은 그 풍경의 안쪽 이야기다. 악의 없는 루프가, 잘 돌아가는 에이전트가, 바로 지금 이 순간에도 **돈을 태우고 있다**는 문제. 위협이 문을 부수는 침입자라면 비용은 수도꼭지에서 밤새 떨어지는 물방울이다. 소리가 안 날 뿐 통장은 마른다.

이 장에서 엮을 세 갈래는 이렇다. 첫째, **어떻게 싸게 돌릴 것인가** — FrugalGPT cascade, RouteLLM, speculative decoding의 공학. 둘째, **어떻게 CI에 태울 것인가** — PR diff에서 하네스를 부르고, iteration cap을 프로세스 레벨로 강제하고, 감사 로그를 시간축 그래프로 읽는 것까지. 셋째, **어떻게 롤백할 것인가** — worktree와 human gate, 그리고 `#29684` 같은 버그가 남기는 고아 커밋을 어떻게 피할지. 세 갈래가 하나의 workflow로 묶이는 순간, 하네스는 "재밌는 장난감"에서 "돌려도 되는 설비"가 된다.

---

## FrugalGPT의 cascade — 왜 계단식이 싸고 맞는가

Chen, Zaharia, Zou의 "FrugalGPT" (2023, arXiv:2305.05176)가 보여주는 그림은 단순하다. **쉬운 질문을 비싼 모델에 보내지 말라**는 것. 저자들은 3가지 절감 전략을 제시하는데(prompt adaptation, LLM approximation, **LLM cascade**), 그중 cascade 한 가지만 잘 써도 특정 과업에서는 GPT-4 수준 품질을 유지하며 비용을 **최대 98% 절감**할 수 있었다고 보고한다. 수치 자체는 데이터셋 의존적이지만, 주장의 구조는 단단하다.

원리는 이렇다. 싼 모델(Haiku급)이 먼저 답을 낸다. 그 답에 대해 **신뢰도 점수**를 계산한다 — 보통은 답변의 log-probability나 별도 scoring 모델이 쓴다. 임계치를 넘으면 그대로 확정. 못 넘으면 한 단계 위 모델(Sonnet)에게 넘긴다. Sonnet도 자신 없으면 Opus가 받는다. 대부분의 쿼리는 첫 단에서 끝난다. 비싼 모델은 **정말로 비싼 값어치를 하는 질문**에서만 호출된다.

하네스에 적용할 때 기억할 점이 있다. cascade는 "어떤 답이 나왔을 때 확정할지"를 결정하는 **judge**가 있어야 동작한다. 6장에서 다뤘던 pairwise-with-swap이나 CoVe와 자연스럽게 맞물린다. 라이브러리가 자동으로 해주지 않는다. 자기 도메인에서 "이 답이 확정할 만한가"를 수치로 답할 수 있어야 1단계 cut-off가 선다.

한계도 분명하다. FrugalGPT의 98%는 **분류 과제와 일부 QA**에서 나온 수치다. 판단이 계속 갈리는 창의적 task나 멀티턴 대화에서는 이 정도로 극단적이지 않다. 그리고 cascade를 붙이면 latency가 늘어난다. 첫 모델이 실패 판정을 내리기까지의 시간은 어차피 소비된다. "싸고 느린" 경로가 기본값이 되는 순간을 견딜 수 있는 workflow인지 점검해야 한다. 실시간 채팅이라면 부담스럽고, CI 백그라운드 태스크라면 손해가 없다.

> **반대 신호 (Contrarian evidence):**
> "하나의 강한 모델이면 다 된다"는 말은 현장에서 가장 비싼 습관이다. Chen et al.의 FrugalGPT(arXiv:2305.05176)는 cascade만으로 특정 태스크에서 98% 절감을, Ong et al.의 RouteLLM(arXiv:2406.18665)은 라우터로 2×+ 절감을, Snell et al.(arXiv:2408.03314)은 test-time compute 할당 최적화로 14× 큰 모델과 대등한 결과를 각각 보고했다. 세 논문의 공통된 함의는 하나다 — **모델 선택은 요청 단위의 엔지니어링 변수**이며, 변수로 다루는 팀은 대부분의 경우 90%+ 절감 구간으로 들어간다. "강한 모델로 통일"은 엔지니어링의 포기 선언에 가깝다.

---

## RouteLLM — 학습된 라우터의 자리

cascade가 "일단 싼 쪽부터 두드려보자"라면, Ong et al.의 "RouteLLM" (2024, arXiv:2406.18665)은 **두드리기 전에 분류해서 보내자**는 쪽이다. ChatBot Arena의 사람 선호 데이터로 라우터를 학습시켜 어떤 쿼리를 Sonnet에 보내고 어떤 쿼리를 Opus에 보낼지 결정하게 한다. 저자들은 품질을 유지하면서 비용을 **2배 이상** 절감했다고 보고하고, 라우터가 학습된 모델 쌍을 넘어서도 전이가 된다는 점을 흥미로운 결과로 제시한다.

cascade와 무엇이 다른가. Cascade는 "답을 본 뒤 판단"이고 라우터는 "질문만 보고 판단"이다. Cascade는 judge가 필요하고, 라우터는 학습된 분류기가 필요하다. 비용으로 치면 라우터 쪽이 정적이라 예산 추정이 쉽다. 첫 모델을 꼭 호출할 필요가 없으니 latency 손해도 적다. 대신 분류가 틀리면 바로 비싼 모델을 잘못 호출하거나 어려운 질문을 싼 모델에 떠넘기는 실패가 난다.

실무 감각으로 말하면 두 가지는 **섞어 쓸 수 있다**. 라우터가 쿼리 분류를 1차로 하고, 애매한 중간 구간에만 cascade를 돌리는 구성이 흔하다. 자기 도메인에서 "딱 보면 쉬운 것 / 딱 보면 어려운 것 / 애매한 것"의 세 무더기로 트래픽이 갈리면 라우터 이득이 크고, 난이도가 연속 스펙트럼이면 cascade 이득이 크다. 시작은 라우터 하나로 **Haiku↔Opus** 이분 분류부터 거는 편이 낫다. 본문 말미 `[연쇄 4시간]` 실습에서 이 첫 단을 workflow에 얹는다.

주의 한 가지. RouteLLM 저자들의 전이 주장은 "같은 데이터로 학습한 라우터가 다른 모델 쌍에도 쓸 만하다"는 의미다. 모델 버전이 바뀔 때마다 라우터를 새로 학습해야 한다는 뜻은 아니다. 그래도 프로덕션에선 **분기별로 라우팅 정확도를 재측정**해두는 편이 낫다. 하네스의 다른 지표와 마찬가지로, 라우터 성능도 시간에 따라 drift 한다.

---

## Speculative Decoding — 에이전트 루프에서 왜 유효한가

Leviathan, Kalman, Matias의 "Fast Inference from Transformers via Speculative Decoding" (2022, arXiv:2211.17192)은 latency 쪽의 반전 카드다. 작은 draft 모델이 K 토큰을 미리 제안하고, 큰 타깃 모델이 그 제안을 **병렬로 검증**한다. 수학적으로 출력 분포가 변하지 않는다는 점을 증명했고, T5-XXL에서 **2~3배 속도**를 보고했다. 품질은 그대로, 시간이 반 이하로.

에이전트 루프와 무슨 상관인가. 루프는 한 번에 한 문장을 기다리는 작업이 아니라 **수십 번의 호출이 직렬로 쌓이는 구조**다. Thought → Action → Observation이 한 iteration이고, 한 태스크에 iteration이 수십 개 붙는다. 모델 호출 한 번에 2배 빨라지면 전체 루프는 수배 빨라진다. 이 계산이 production 지연시간과 만나는 지점이 speculative decoding의 실질 이득이다.

실무에서 기억할 점 두 가지. 첫째, speculative decoding은 **모델 제공자가 내부에서 켜주는 기능**에 가깝다. 사용자는 대부분 직접 구현하지 않는다. Anthropic·OpenAI의 고속 변형 모델이 이미 이 기법을 흡수하고 있다. 하네스 설계에서 할 일은 "latency가 문제라면 speculative 혹은 그에 준하는 fast-path 변형을 쓸 수 있는지"를 제공자 문서에서 확인하는 정도다. 둘째, speculative decoding은 **분포를 바꾸지 않는다**. 품질 저하를 걱정할 필요는 없지만, 그만큼 품질이 저절로 올라가지도 않는다. 이 기법은 비용보다 **시간**의 카드라는 점을 기억해두는 편이 낫다.

---

## `MAX_THINKING_TOKENS`를 팀 표준으로 승격하기

2장에서 `MAX_THINKING_TOKENS=8000`을 걸어 토큰 소비 감소를 시연했었다. 거기서는 **개인 세팅 시연**이었다. 여기서는 같은 변수를 **팀·조직 표준 기본값**으로 승격하는 이야기다. 역할이 다르다.

개별 개발자 한 사람이 자기 셸에서 `export MAX_THINKING_TOKENS=8000`을 치는 건 실험이다. 실험은 재현되지 않는다. 옆자리 동료가 같은 태스크를 돌릴 때는 extended thinking이 full로 켜지고, 같은 CI 러너가 같은 workflow로 돌 때마다 토큰 소비가 2배씩 튄다. 팀 예산 그래프가 들쭉날쭉한 이유는 대부분 이 **"환경 변수가 사람마다 다르다"** 한 문장이다. 찜찜하다.

승격의 방법은 단순하다. 세 층에 박아둔다.

첫째, 공유 `AGENTS.md` 또는 `CLAUDE.md`에 **기본 사용 지침**을 명시한다. "이 레포에서는 `MAX_THINKING_TOKENS=8000`을 권장한다. 더 깊은 사고가 필요하면 PR에 근거를 남긴 뒤 임시 override 한다." 이 한 문단이 있어야 동료가 자기 설정을 의심한다.

둘째, CI workflow의 `env:` 블록에 값을 **고정**한다. 개인 머신은 몰라도 CI 러너에서만큼은 예산이 예측 가능해진다. 한 줄이면 충분하다.

셋째, 팀에 따라 managed policy — Claude Code의 엔터프라이즈 설정 스코프 — 에 **override-불가 값**으로 박아둘 수 있다. 팀 예산을 지켜야 하는 조직이라면 이 층까지 내려가는 게 낫다. 개인의 의지에 의존하지 않게 된다.

한 가지 경계. velog @justn-hyeok의 한국어 진단 글이 기록한 증상 — Claude Code가 "최근 이상하다"는 감각의 배후에 adaptive thinking과 effort 다운그레이드가 있었다는 — 은 이 변수의 반대 측면이다. 너무 조이면 **필요한 사고를 깎아낸다**. 8,000이라는 숫자는 "일상 태스크의 상한"으로서 제안값이지 성역이 아니다. 팀 값으로 박되 **override 경로는 PR 기반으로 열어두는 편이 낫다**. 고정과 우회가 모두 감사 가능한 상태, 그 균형이 팀 표준값이 뜻하는 바다.

---

## CI 통합 — PR diff에서 하네스까지

CI에 하네스를 태우는 일은 생각보다 작은 레버다. 한 번 걸어두면 **"사람이 수동으로 하던 실험"이 인프라로 전환**된다. 틀은 이렇다. PR이 열린다 → 변경된 파일 목록을 뽑는다 → 하네스에게 diff를 컨텍스트로 넘긴다 → 하네스가 점검/보강/리팩터링을 시도한다 → 결과를 PR 코멘트로 남긴다. 이 과정 전체가 `.github/workflows/*.yml` 한 장에 들어간다.

구성 예시 하나를 살펴본다. Claude Code를 CI에서 돌리는 한 가지 방식이다.

```yaml
# .github/workflows/harness-on-pr.yml
name: harness-on-pr
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  harness:
    runs-on: ubuntu-latest
    timeout-minutes: 25           # iteration cap = CI timeout
    env:
      MAX_THINKING_TOKENS: 8000
      HARNESS_ITERATION_CAP: 20
      HARNESS_TOKEN_BUDGET: 200000
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: diff-context
        run: |
          git diff --name-only origin/${{ github.base_ref }}...HEAD \
            > .harness/changed-files.txt

      - name: run-harness
        run: |
          .harness/run.sh \
            --changed-files .harness/changed-files.txt \
            --router haiku-then-opus \
            --log .harness/audit.jsonl
        timeout-minutes: 20

      - name: comment-result
        if: always()
        run: .harness/comment.sh .harness/audit.jsonl

      - name: upload-audit
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: harness-audit
          path: .harness/audit.jsonl
```

이 workflow 한 장에 설계 원칙이 여럿 박혀 있다. 하나씩 짚어둔다.

**iteration cap = CI timeout.** 하네스 루프가 자체 종료 조건으로 iteration 수를 세는 건 당연하지만, 프로세스가 종료되지 않을 가능성은 늘 있다. 모델이 "하나만 더" 하려 하고, 감사 로그는 비어 있는데 시간은 흐른다. 이럴 때 **프로세스 레벨 강제**가 유일한 안전망이다. GitHub Actions의 `timeout-minutes`는 OS 시그널로 프로세스를 끝낸다. 하네스의 자체 카운터가 어긋나도 이 벽은 부서지지 않는다. `HARNESS_ITERATION_CAP=20`과 `timeout-minutes: 20`을 **함께** 걸어두는 이유가 이것이다. 둘 중 하나가 죽어도 다른 하나가 깨우러 온다.

**감사 로그를 artifact로 올린다.** 결과 코멘트는 사람용이고, `audit.jsonl`은 기계용이다. 뒤에서 설명할 Observability 절에서 이 JSONL을 시간축 그래프로 굽는 이야기를 한다. artifact로 안 올리면 CI 러너가 끝날 때 같이 사라진다. 이 한 스텝이 빠지면 관측의 뿌리가 없어진다.

**라우터를 CI 스텝 인자로 받는다.** 개발 중에는 전체 Opus로 돌리다가, merge 게이트로 들어오면 Haiku→Opus cascade로 전환하는 식의 스위치가 workflow 바깥에서 가능해진다.

Flaky loop의 retry 정책도 정해두는 편이 낫다. 외부 네트워크·rate limit 때문에 하네스가 실패하는 일은 흔하다. 단, **무조건 재시도는 위험하다** — 실패 원인이 "비결정적 모델 응답"이라면 재시도가 비용만 2배로 태운다. 적정선은 **최대 2회, 그리고 iteration 총량은 합산**이다. 1차에 15 iteration을 썼다면 2차는 5까지만. GitHub Actions의 `retry` 액션이나 step-level try-catch로 짜 두되, 카운터는 workflow 환경변수 하나에 몰아둔다. 감사 로그에 `retry_n: 1` 필드도 꼭 포함한다. 나중에 "재시도만 성공률 80%인 태스크"를 골라낼 수 있다. 그런 태스크는 대체로 테스트가 flaky한 것이지 모델이 똑똑해서 두 번째에 풀리는 게 아니다.

---

## 롤백과 회복 — worktree, human gate, 그리고 anthropic/claude-code#29684

하네스가 자율적으로 코드를 쓴다는 말은 **하네스가 잘못 쓸 수도 있다**는 말과 같다. 이때 작동하는 원칙은 하나로 요약된다. **절대 main에 직접 쓰지 말 것.**

실무 구성은 이렇다. 하네스가 실행되는 순간 `.harness/worktrees/session-<id>/` 같은 격리된 git worktree를 만들고, 모든 변경은 그 worktree 안에서 일어난다. 작업이 끝나면 diff가 올라가고, 사람이(혹은 2차 검증 하네스가) **merge 전에 봐야** main이 움직인다. 이 "human gate"가 한 번이라도 비는 팀은 조만간 부끄러운 커밋을 main에서 발견한다.

왜 이렇게까지 조심해야 하는지는 **GitHub Issue anthropic/claude-code#29684** 한 건이면 충분하다. Mid-chat rollback 버그라고 불리는 이 사례는 Claude Code가 대화 중 특정 응답을 rollback 했을 때, **대화 이력은 되돌려지지만 side effect(커밋·파일 변경)는 그대로 남는** 문제였다. 결과는 고아 커밋(orphaned commits) — 대화상으로는 존재하지 않는 커밋이 git에는 박혀 있는 상태. 아무도 기억하지 못하는 변경이 레포에 조용히 남는다. 끔찍한 일이다.

worktree 격리가 이 문제의 1차 방어막이다. Rollback이 일어나도 영향 범위가 격리된 디렉터리 안이다. 2차 방어막은 **merge 전 human gate**. 대화 이력이 아니라 **diff와 감사 로그**를 기준으로 판단하게 만든다. "Claude가 여기서 뭘 했다고 말했다"가 아니라 "git이 뭘 보여주느냐"를 신뢰 기준으로 세우는 편이 낫다. 대화는 거짓말할 수 있고 diff는 거짓말을 못 한다.

회복 절차도 미리 정해두는 편이 낫다. 하네스 세션이 실패했을 때의 기본 동작은 **worktree 폐기**다. `git worktree remove`로 통째로 날린다. 그리고 감사 로그는 보관한다. 다음 실행은 깨끗한 상태에서 시작한다. 이 한 줄짜리 정책이 있으면 "반쯤 간 상태에서 이어서 하려다 더 꼬이는" 흔한 함정을 피한다. 재시도는 **새 worktree에서** 해야 한다. 찜찜한 상태를 이어서 쓰는 것은 버그를 상속하는 지름길이다.

---

## 감사 로깅 스키마 — 한 줄 JSON이 쌓이는 방식

감사 로그는 나중에 "이 한 줄이 있었으면 좋겠다"고 후회하는 지점에서 태어난다. 미리 박아두는 편이 낫다. 하네스가 iteration을 돌 때마다 JSON 한 줄씩 쌓는 JSONL 포맷이 가장 다루기 쉽다. 최소 필드는 다음과 같다.

```json
{
  "ts": "2026-04-20T14:22:01Z",
  "session_id": "hss-9c4a2",
  "iteration": 7,
  "input_hash": "sha256:3f2a...e1",
  "output_hash": "sha256:a11c...09",
  "model": "claude-sonnet-4-7",
  "tokens_in": 12480,
  "tokens_out": 3120,
  "cost_usd": 0.058,
  "duration_ms": 9420,
  "exit_reason": "ok",
  "actor": "ci@repo/pr-842",
  "policy_version": "harness-0.9.3"
}
```

필드 하나하나가 뒷날을 버틴다. `input_hash`와 `output_hash`는 **민감 데이터를 본문으로 남기지 않기 위한 장치**다. PR diff에 비밀 키가 섞여 들어가도 로그에는 해시만 남는다. 재현이 필요한 순간에는 해시로 원본 location을 찾되, 로그 저장소 자체는 비밀을 모른 채로 유지된다. 9장에서 깔았던 보안 원칙 — "샌드박스 안에 비밀을 넣지 말 것" — 의 로깅 쪽 대응이 이것이다.

`model`과 `policy_version`이 둘 다 있어야 한다. 모델 버전이 바뀌었을 때의 drift와 하네스 정책이 바뀌었을 때의 drift는 **다른 문제**다. 두 축을 같이 기록해야 나중에 "언제부터 비용이 뛰었는가"를 분해할 수 있다. `exit_reason`은 enum으로 관리하는 편이 낫다 — `ok / iter_cap / timeout / cost_cap / policy_deny / error`. 자유 텍스트로 두면 한 달 뒤 자기가 뭘 적었는지 알아볼 수 없다.

9장 "기업 컨텍스트" 절에서 다뤘던 SOC2/ISO27001 요건과 이 스키마는 그대로 맞물린다. `actor`와 `session_id`와 `policy_version`이 있으면 "누가 언제 어떤 정책 버전으로 뭘 했는가"를 재구성할 수 있다. 감사 요건 CC 6.1/7.2가 요구하는 사용자 활동 추적과 동일한 뼈대다. 필드를 빠뜨리면 나중에 보안팀을 설득하러 갈 때 "다시 수집해 오겠다"는 말을 하게 된다. 미리 박아두는 편이 낫다.

한 가지 경계. 로그가 너무 길어지면 보안이 줄어든다. input 원문은 해시로만, 혹시 본문을 남겨야 한다면 **PII redaction을 통과한 버전**만 저장한다. 해시도 content-addressed storage의 키로 쓰면 원본 조회가 감사 흔적을 남긴다. 이 계단도 팀 정책으로 박아두는 편이 낫다.

---

## Observability ≠ 일기쓰기

JSONL을 잘 쌓아두는 것만으로는 모자라다. 하루에 수천 줄이 쌓이면 사람 눈으로 훑는 건 불가능하고, 중요한 신호는 **시간축 그래프 위**에서야 보인다. 월 예산의 50% 지점에서 알람이 오려면, 비용이 시간에 따라 쌓이는 곡선을 누군가(혹은 무언가)가 보고 있어야 한다. 로그만 쌓아두는 건 일기를 쓰는 것이지 관측하는 게 아니다.

실무 권장은 prometheus/pushgateway 스타일이다. 하네스가 iteration을 돌 때마다 `cost_usd`, `tokens_in/out`, `duration_ms`, `exit_reason`을 metric으로 push 하고, Grafana 같은 대시보드에서 시간축으로 읽는다. 그 위에 **예산 50%, 80%, 100%의 수평선 3개**를 긋는다. 50%에서 Slack 알람, 80%에서 팀장 소환, 100%에서 CI가 하네스를 스스로 정지하도록 워크플로 게이트를 걸어둔다. 이 세 단 라인 하나가 9장에서 소개한 "위협 모델"과 쌍을 이룬다. 위협은 침입이고, 비용은 출혈이다. 둘 다 **그래프로 보고 있어야 대응이 가능**하다.

기억해둘 점이 하나 있다. Observability의 최소 요건은 "로그가 있다"가 아니라 **"지금 이 순간의 값이 그래프 위에 있다"**다. 하루 뒤에 로그를 뒤져서 알게 되는 사실은 관측이 아니라 부검이다.

---

## 실습과 체크포인트

**`[연쇄 4시간]` CI + 라우터 + 알람을 하나의 workflow로.** 본인 레포에 4장에서 만들어둔 하네스를 CI에 연결한다. 단계는 이렇다.

1. `.github/workflows/harness-on-pr.yml`을 앞 예시 틀로 복사. `timeout-minutes`·`HARNESS_ITERATION_CAP`·`HARNESS_TOKEN_BUDGET`을 자기 레포 규모에 맞춰 조정.
2. 하네스 실행 스크립트에 **Haiku→Opus cascade 1단** 라우팅 추가. 첫 호출은 Haiku, 신뢰도 임계 미만이면 Opus로 승격. 라우팅 결정도 감사 로그 한 줄로 남긴다.
3. Per-iteration 감사 로그 JSONL을 앞의 스키마로 작성. 최소 필드 11개 중 자기 레포에 의미 없는 필드는 빼도 좋다. 단, `session_id / iteration / model / cost_usd / exit_reason`은 반드시.
4. 월 예산 시뮬레이션 알람 — cron 한 방이면 된다. 주 1회 `audit.jsonl`을 합산해 **누적치가 월예산 50%를 넘었는지** 판정, Slack webhook(또는 echo로 대체)을 친다. 실제 Slack이 없다면 workflow 로그에 `::warning ::` 한 줄로 찍어도 검증이 된다.

산출물: `.github/workflows/harness-on-pr.yml` 1개, `.harness/run.sh` 수정본, 첫 PR에서 생성된 `audit.jsonl` 1개, 알람 발동 증거 1건(스크린샷·Slack 메시지·workflow 로그 중 하나). 책 저장소에 완성 레퍼런스 workflow를 둘 테니, 실행이 막히면 바닥부터 베끼는 편이 낫다.

**`[읽기 15분]` 라우터 전후 토큰 로그 추정.** CI까지 붙일 시간이 없다면 이 쪽이라도 실행하는 편이 낫다. 자기 팀의 최근 1주일치 LLM 호출 로그(대시보드 export면 된다)를 받아, **단순/복잡 쿼리 비율**을 눈대중으로 나눠본다. 70%를 Haiku, 30%를 Opus로 라우팅했다고 가정하고 비용을 재계산. "만약 우리가 라우터를 붙였다면" 숫자 하나가 나온다. 1페이지 노트로 정리해 팀 채널에 붙인다. 다음 스프린트의 설득 자료가 된다.

**체크포인트.** `[연쇄]`를 돌린 독자는 — workflow 1개 + 알람 발동 증거 1건이 손에 있는가? `[읽기]`만 한 독자는 — 라우터 전후 월 예산 추정 1페이지가 commit 되어 있는가? 둘 중 한 쪽만 있어도 이 장은 통과다. 둘 다 없다면 다음 장으로 넘어가지 않는 편이 낫다. 팀에 이 장을 전할 수 있는 실물 하나는 있어야 한다.

## 마무리

이 장에서 깔린 것은 "비용을 설계 변수로 다룬다"는 한 문장이다. Cascade·router·test-time compute·`MAX_THINKING_TOKENS` 정책·iteration cap·감사 로그 — 이 여섯 개가 한 workflow로 엮이면 하네스는 처음으로 **재무적으로 설명 가능**해진다. 월말 대시보드에서 숫자를 보고 놀라는 대신, 월 중반의 그래프에서 알람이 먼저 온다. 이 전환이 오늘의 결론이다.

다음 장에서는 이 엔지니어링 규율을 **조직**으로 끌고 올라간다. 같은 하네스를 팀이 쓰기 시작할 때, PR 리뷰는 어떻게 바뀌어야 하는가. 공유 `AGENTS.md`는 누가 관리하는가. 신입에게 하네스를 30분 안에 건네주려면 뭐가 준비돼 있어야 하는가. 그리고 에이전트가 프로덕션 사고를 냈을 때 팀의 role과 타임라인은 어떻게 짜이는가. 개인의 하네스가 팀의 설비로 굳는 과정을, 11장에서 이어간다.
