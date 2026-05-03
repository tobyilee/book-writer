# 12장. Ralph Loop은 어떻게 단순함의 승리가 되었나

## 12.1 솔직해지자

이 챕터는 한 줄에서 시작한다.

> "Ralph is a Bash loop."[^ralph-everything]
>
> *Ralph는 한 줄짜리 bash while 루프다.* — Geoffrey Huntley

이 한 줄에 Geoffrey Huntley가 있다. 호주 시드니의 인디 개발자고, 2025년 한 해 *Everything is a Ralph loop* 같은 글로 코딩 에이전트 커뮤니티의 한 모서리를 흔든 사람이다.[^ralph-everything] [^ralph-ghuntley] 그는 자기 에이전트 패턴을 *심슨 가족*의 등장인물 — Ralph Wiggum — 의 이름으로 불렀다. Ralph는 두뇌가 그다지 명석하지 않은 캐릭터다. 같은 말을 반복하고, 자기가 한 말을 자주 잊는다. Huntley의 농담은 분명했다. **에이전트도 Ralph처럼 굴지 않는가? 그렇다면 *Ralph처럼* 다루자.**

그래서 그가 짠 것은, 한 줄짜리 bash 루프였다.

```bash
while true; do
  cat prompt.md | claude
done
```

이게 끝이다. 다른 줄도 있긴 하지만, 본질은 이 셋이다. 그리고 이 셋만으로 *진짜 에이전트가 도는* 시스템을 그가 운영했고, 다른 사람들이 따라 했고, 2025년 12월에 Anthropic이 *공식 Claude Code 플러그인*으로 채택했다.[^ralph-anthropic] 한 인디 개발자의 농담 비슷한 패턴이 1차 벤더의 공식 product가 됐다.

이 사실 앞에서 솔직해지자. 우리는 그동안 에이전트를 *복잡한 시스템*이라고 생각했다. 멀티에이전트 프레임워크, 그래프 기반 상태머신, 메시지 큐, 분산 메모리. *간단해선 안 될 것 같은* 인상이 우리 머릿속에 박혀 있었다. 그런데 한 줄 bash가 도는 걸 보면, 우리가 짠 LangGraph 다이어그램이 *과한* 것은 아니었나, 살짝 의심스럽다.

이 챕터는 그 의심을 *직시한다*. Ralph Loop이 왜 *단순함의 승리*가 됐는지, 단순함이 어디까지 가고 어디서 멈추는지, 그리고 자기 환경에서 30줄 bash로 Ralph를 한 번 돌려 보는 일이 왜 우리에게 필요한지를 본다.

## 12.2 한 줄 루프의 해부

Huntley의 *Everything is a Ralph loop*가 정리한 골격을 그대로 보자.[^ralph-everything] 본질을 가리지 않는 선에서 옮긴다.

```bash
#!/usr/bin/env bash
set -e

while true; do
  # 1. 입력 프롬프트를 읽는다.
  cat PRD.md AGENTS.md progress.md > /tmp/feed.md

  # 2. 에이전트를 호출한다.
  claude --file /tmp/feed.md --output /tmp/out.md

  # 3. 진전이 있으면 progress를 갱신한다.
  if grep -q "PROGRESS:" /tmp/out.md; then
    cat /tmp/out.md >> progress.md
  fi

  # 4. 컨텍스트가 다 차면 종료, 다시 시작.
  if grep -q "CONTEXT_FULL" /tmp/out.md; then
    continue
  fi

  # 5. 작업이 끝나면 빠진다.
  if grep -q "DONE" /tmp/out.md; then
    break
  fi
done
```

이 30줄이 하는 일을 풀어 보자.

**한 사이클의 구조.** 각 사이클은 (a) 디스크 위 산출물 읽기 → (b) 모델 호출 → (c) 결과 평가 → (d) 디스크 갱신 → (e) 다음 사이클. 11장의 2-Prompt 패턴이 그대로 들어가 있다. 모델은 매번 *깡통 컨텍스트*에서 시작하고, 진행 상태는 디스크 위 progress.md가 잇는다. *한 줄 bash가 자기 자신을 위한 Initializer + Coding의 분리를 강제한다*는 점이 결정적이다.

**컨텍스트 부패에 대한 응답.** "CONTEXT_FULL" 신호가 오면 그냥 *다시 시작*한다. 컨텍스트 압축도, 요약도, 어떤 영리한 처리도 없다. 그냥 닫고 새로 연다. 10장에서 본 *깡통이 전제*라는 사실의 가장 솔직한 구현이다.

**종료 조건.** "DONE"이 떨어지면 빠진다. 무한 루프가 *진짜로 무한*은 아니다. 단, 종료 조건을 모델 출력에 의존한다는 점에 주의가 필요하다. 모델이 "DONE"을 안 쓰면 영원히 돈다. 12.4에서 다시 본다.

이 30줄에 *복잡한 것*이 없다. 큐도, 락도, 분산 상태도, 멀티프로세싱도 없다. 한 프로세스가 한 모델을 한 줄로 부른다. 그게 끝이다.

## 12.3 "300줄 + LLM 토큰"이라는 농담

Huntley가 다른 글에서 한 표현이 있다.

> "It's not that hard to build a coding agent. 300 lines of code running in a loop with LLM tokens."[^ralph-everything]
>
> *코딩 에이전트 짜는 게 그렇게 어렵지 않다. 300줄 코드 + LLM 토큰을 루프에 던지면 된다.*

이 문장이 이 책의 척추 한 줄과 마주 보고 있다. **"Agent = Model + Harness."** 1장에서 만난 Addy Osmani의 정의다.[^osmani] *그저 그런 모델 + 좋은 하네스가 좋은 모델 + 나쁜 하네스를 이긴다*는 명제가, Huntley의 한 줄 bash가 도는 것을 보면 더 선명해진다. **하네스가 30줄로 충분하다면, 우리가 그동안 짜던 그 거대한 프레임워크는 무엇이었나.**

그렇다고 LangGraph가 다 쓸데없다는 뜻이 아니다. 14장에서 다시 다루겠지만, *읽기 위주 병렬 가능 작업*에서는 그래프 기반 멀티에이전트가 정당하다. 그러나 *쓰기 위주 코딩 작업*의 95%는 — 솔직해지자 — 한 줄 bash + 한 모델 + 디스크 한 파일로 충분하다. 우리가 LangGraph 다이어그램을 그리고 있을 때, 정말로 우리 작업의 본질이 그 그래프인지 의심해 보자.

이 의심이 Huntley의 패턴이 산업에 박힌 가장 큰 이유다. *복잡함이 정당화될 자리*와 *단순함으로 충분한 자리*를 가르는 자가 됐다. 자기 작업이 후자에 속한다는 사실을 — 우리 대부분이 — 받아들이고 싶어 하지 않을 뿐이다.

## 12.4 무한 루프의 비용 — 그리고 Principal Skinner

한 줄 bash의 단점은 명백하다. **무한 루프는 비용을 무한히 먹는다.**

각 사이클이 모델 한 번 호출이고, 한 호출이 토큰을 먹고, 토큰이 돈이다. 사이클당 평균 5,000 토큰을 먹고 사이클이 1초 도는데, 한 시간을 돌리면 1,800만 토큰이다. Sonnet 4.6 기준 입력+출력 평균 단가로 계산하면 *수십 달러* 단위가 한 시간에 사라진다. 작업이 끝나는 신호("DONE")가 안 떨어지면 — 모델이 정직하지 않다는 게 아니라, *작업이 끝나지 않는 종류*면 — 우리는 잠든 사이 청구서를 *깨운다*.

이 문제를 정면으로 다룬 글이 Sondera의 *Supervising Ralph: Why Every Wiggum Loop Needs a Principal Skinner*다.[^ralph-supervisor] 제목이 농담을 두 번 친다. Ralph가 심슨 가족이면, *Principal Skinner*는 그가 다니는 학교의 교장이다. Wiggum 루프에는 *교장*이 필요하다 — 라는 농담.

Sondera의 핵심 제안은 단순하다.

1. **루프 *밖*에 감독자(supervisor)를 둔다.** Ralph는 자기가 무엇을 했는지 모를 수 있다. 감독자는 N 사이클마다 progress.md를 읽고, *진전이 있는지*를 *별도 모델 호출*로 판정한다.
2. **진전이 없는 K 사이클이 누적되면 루프를 멈춘다.** "Ralph가 같은 자리를 맴돌고 있다"고 감독자가 판정하면, 사이클을 강제 종료하고 사람을 호출한다.
3. **예산 상한을 *절대값*으로 박는다.** "이 작업에 $50까지 쓴다." 토큰 예산이 다 차면 — 작업이 끝났든 안 끝났든 — 감독자가 종료시킨다.

Principal Skinner 패턴이 주는 본능적 함의는 이거다. **단순함은 *통제* 위에서만 단순함이다.** 한 줄 bash가 한 줄로 충분한 것은, 우리가 그 한 줄을 *언제든 멈출 수 있는* 회로 위에 올려 둘 때다. 그 회로 — 시간 상한, 비용 상한, 진전 감독 — 가 빠지면 단순함은 위험이 된다.

15장에서 비용·throttling·model fallback을 본격적으로 다루겠지만, 12장의 결론 한 줄로는 이거다. **Ralph는 한 줄, 그러나 그 한 줄을 둘러싼 *예산 회로*는 따로*.

## 12.5 Anthropic이 받아 준 자리 — 2025년 12월

2025년 12월, Anthropic이 *Ralph Wiggum Plugin*을 Claude Code 공식 플러그인 카탈로그에 등재했다.[^ralph-anthropic] 한 인디 개발자가 만든 패턴이 1차 모델 벤더의 공식 product가 된 자리다. 이 사건이 의미하는 바는 두 가지다.

**첫째 — 산업이 단순함을 인정했다.** 멀티에이전트 프레임워크 진영이 정교한 그래프와 메시지 패싱을 정의하는 동안, Anthropic이 *bash 한 줄*을 공식 채택했다는 사실은 *어느 쪽이 정답인가*에 대한 1차 벤더의 답변에 가깝다. 정답은 *작업에 따라 다르다*이지만, *코딩 핵심 워크플로*에서는 단순함이 이긴다 — 가 그 답변의 본질이다.

**둘째 — Ralph가 *플러그인 모델*에 적합했다.** Claude Code의 플러그인은 슬래시 커맨드, 서브에이전트, 스킬, 후크의 조합이다. Ralph는 그 모든 것을 *bash 한 줄*로 묶을 수 있는 wrapper였다. 작은 표면적이 큰 호환성을 만든다는 — 8장에서 본 ACI 4원칙의 *작은 표면적* 원칙 — 이 여기서도 작동했다.[^anthropic-harness1]

이 채택의 *교훈*은 우리에게 직접 적용된다. 자기 도구를 짤 때 — 그게 작은 사내 스크립트든 OSS든 — *플러그인 가능한 단순함*을 우선하자. 큰 프레임워크보다 *bash 한 줄*이 다른 사람에게 *옮겨 가기 쉽다*. 옮겨 가는 자리에서 표준이 만들어진다.

## 12.6 Ralph가 *못* 하는 일

단순함의 승리 이야기를 이어 가는 동안, *Ralph가 잘 못 하는 일*도 분명히 짚자.

**하나 — 분기 결정.** Ralph는 한 사이클에 한 가지 일을 한다. 두 갈래 중 하나를 골라야 하는 상황 — "라이브러리 A를 쓸까 B를 쓸까" — 에서 Ralph는 답을 *고를 수는* 있지만, 그 결정이 정합한지 *검증할 자기 평가*가 없다. 13장의 Generator-Evaluator가 그 빈자리를 채운다.

**둘 — 다중 작업 병렬.** Ralph는 직선적이다. 한 작업이 끝나야 다음 작업이다. 동시에 두 가지를 굴려야 하는 상황 — "테스트는 백그라운드, 구현은 포그라운드" — 에서 Ralph 한 개로는 부족하다. 14장의 단일 vs 다중 논의가 여기 들어간다.

**셋 — 사람 개입 자리의 모호성.** Ralph는 정직한 종료 신호("DONE")를 모델에게 의존한다. 모델이 *모호한 자리*에서 사람에게 물어봐야 하는 경우, 그 신호가 progress.md의 "미해결 질문" 섹션에만 남고, 우리는 그것을 *다음 날 아침에서야* 본다. 실시간으로 *사람을 깨우는* 자리가 없다. Sondera의 Principal Skinner가 이 빈자리에 들어간다.[^ralph-supervisor]

이 셋을 인정하면 Ralph가 *어디까지가 정당한 단순함*인지가 분명해진다. 코딩 핵심 워크플로 + 종료 조건 명확 + 사람 개입 빈도 낮음 = Ralph 적합. 그 조건 셋 중 어느 하나가 깨지면, 우리는 Ralph 위에 *얇은 한 겹*을 더해야 한다.

## 12.7 시그니처 인용 박스

> ### 시그니처 인용
>
> > "Ralph is a Bash loop."
> >
> > *Ralph는 한 줄짜리 bash while 루프다.*
> >
> > — Geoffrey Huntley, *Everything is a Ralph loop* [^ralph-everything]
>
> 한 줄이 우리에게 강제하는 네 가지:
> 1. **에이전트는 *복잡할 필요*가 없다.** 한 줄 bash + 한 모델 + 디스크 한 파일로 충분한 작업이 우리 작업의 다수다.
> 2. **단순함은 *통제* 위에서만 단순함이다.** 시간·비용·진전 감독 회로가 따로 있어야 한다(12.4).
> 3. **깡통 컨텍스트가 *전제*면 한 줄 루프가 자연스럽다.** 11장의 2-Prompt 패턴이 12장의 Ralph로 자연 진화한다.
> 4. **Ralph가 *못* 하는 일도 분명하다.** 분기 결정, 병렬, 사람 개입 — 그 자리에 13·14장의 도구가 들어간다.

## 12.8 실습 — 30줄짜리 Ralph 직접 굴리기

> ### 실습: 30줄 bash Ralph Loop을 자기 환경에서 한 시간 안에 굴리기
>
> **목적:** 한 줄 bash가 *진짜로* 도는 모습을 자기 손으로 본다. *복잡함의 환상*을 한 번 깨자.
>
> **준비물.**
> - Claude Code (또는 Codex CLI, Cursor의 CLI 모드 — 명령줄 호출 가능한 에이전트라면 무엇이든).
> - bash. (zsh도 OK.)
> - 작은 작업 한 개. 예: "이 디렉토리의 README.md를 한국어로 번역해서 README.ko.md로 저장하라."
> - **시간 상한**: 30분. **비용 상한**: $5. (이 두 줄이 Principal Skinner다.)
>
> **절차 (60분).**
>
> 1. **(10분) PRD.md를 짠다.** 한 페이지짜리 작업 명세. "무엇을 한다", "끝났다는 신호는 무엇이다", "어떤 파일이 디스크에 남으면 끝이다." `DONE`이라는 단어가 어디서 떠야 하는지 명시.
>
> 2. **(15분) 30줄 bash 스크립트를 짠다.** 12.2의 골격을 자기 환경에 맞게 베끼자. 핵심 셋:
>    - `cat PRD.md AGENTS.md progress.md > /tmp/feed.md`
>    - `claude --file /tmp/feed.md --output /tmp/out.md`
>    - `grep -q "DONE" /tmp/out.md && break`
>    - **반드시** 추가: 시간 상한 (`SECONDS` 변수로 30분 카운트). 비용 상한은 OS 레벨로는 어렵지만, *사이클 수 상한*(예: 50 사이클)으로 근사.
>
> 3. **(30분) 실행하고 *지켜본다*.** 진짜로 지켜보자. 잘 도는지, 컨텍스트가 차서 다시 시작하는지, "DONE"이 정직하게 떨어지는지, 진전 없이 같은 자리를 도는지.
>
> 4. **(5분) 결과 한 줄 메모.**
>    ```
>    Ralph 첫 시도, Sonnet 4.6, 30분 상한, 18 사이클에 DONE,
>    progress.md에 12 항목, 비용 ~$2.4. 한 자리 맴도는 사이클은 3·4번째에서 발생.
>    ```
>
> **무엇을 보는가.**
> - 한 줄 bash가 *진짜로* 도는 모습을 본 후 — 우리가 평소 짜던 프레임워크의 *복잡함이 정당했는지* 다시 본다.
> - "DONE"이 정직하게 떨어졌는가, 아니면 우리가 *수동으로* 멈췄는가.
> - 같은 자리 맴도는 사이클이 있었는가. 있었다면 12.4의 Principal Skinner가 들어갈 자리.
>
> **확장 — 5분.** 같은 작업을 *한국어 PRD*로 한 번 더 돌려 보자. 사이클 수가 다른가? 토큰 사용량이 1.5~2배 많은가? 10장의 한국어 토큰 비용이 Ralph 위에서 어떻게 나타나는지 본다.

## 12.9 마무리 — 단순함이 도착한 자리

이 챕터에서 우리가 얻은 것은 한 가지 *환상에서의 해방*이다. 에이전트가 복잡한 시스템이라는 환상. Geoffrey Huntley의 한 줄 bash가, 그 환상을 깨면서 동시에 *정당한 단순함의 조건*을 분명하게 만들었다. 깡통 컨텍스트가 전제이고, 디스크가 메모리이고, 종료 조건이 명확하다면 — 한 줄 bash로 충분하다. 그 단순함을 둘러싼 *예산 회로*만 따로 있으면 된다.

이 단순함이 2025년 12월에 Anthropic의 공식 플러그인이 됐다. 한 인디 개발자의 농담 비슷한 패턴이 1차 벤더의 공식 product로 받아들여진 그 자리가 의미하는 바를 다시 보자. **코딩 핵심 워크플로에서, 단순함이 정답이다.** 그렇지 않다고 생각한다면 — 우리가 짠 그래프 다이어그램이 정말로 우리 작업의 본질인지, 한 번 솔직하게 물어보자.

기억해두자. Ralph는 한 줄이지만, *통제 회로 위의 한 줄*이다. 시간 상한, 비용 상한, 진전 감독. 이 셋 없이 도는 Ralph는 단순함이 아니라 무방비다. Sondera의 Principal Skinner가 그래서 농담이 아니다.

이제 다음 자리로 가자. Ralph가 한 줄로 작업을 굴려 결과를 만들면 — 그 결과는 누가 채점하는가. 같은 모델이 자기 결과를 평가하면 *과대평가*하는 경향이 있다는 사실을 Anthropic이 정량적으로 보였다.[^anthropic-harness2] [^infoq-3agent] 그래서 *작업하는 에이전트와 판정하는 에이전트를 분리*하는 패턴이 산업의 한 표준이 됐다. 13장 — Generator-Evaluator로 간다.

[^ralph-everything]: Geoffrey Huntley, *Everything is a Ralph loop*. https://ghuntley.com/loop/
[^ralph-ghuntley]: Geoffrey Huntley, *Ralph Wiggum as a "software engineer"*. https://ghuntley.com/ralph/
[^ralph-anthropic]: Anthropic Claude Code, *Ralph Wiggum Plugin*. https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md
[^ralph-supervisor]: Sondera, *Supervising Ralph: Why Every Wiggum Loop Needs a Principal Skinner*. https://blog.sondera.ai/p/ralph-wiggum-principal-skinner-agent-reliability
[^osmani]: Addy Osmani, *Agent Harness Engineering*. https://addyosmani.com/blog/agent-harness-engineering/
[^anthropic-harness1]: Anthropic Engineering, *Effective harnesses for long-running agents*, 2025-11. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
[^anthropic-harness2]: Anthropic Engineering, *Harness design for long-running application development*, 2026-03. https://www.anthropic.com/engineering/harness-design-long-running-apps
[^infoq-3agent]: InfoQ, *Anthropic Designs Three-Agent Harness Supports Long-Running Full-Stack AI Development*. https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/
