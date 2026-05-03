# 3부. 장기 실행과 컨텍스트 — 살아 있는 에이전트

> **부 인트로**

척추가 움직이는 모습을 보자.

2부에서 우리는 척추를 세웠다. CAR로 책임을 갈랐고, Guides와 Sensors로 폐루프를 닫았다. ACI 4원칙으로 인터페이스를 다시 그렸고, AGENTS.md가 왜 비대해지면 무력해지는지를 봤다. 도구·MCP·서브에이전트로 Agency의 표면을 깎아 봤다.

그러나 척추는 *서 있는* 것만으로는 부족하다. 걷고, 넘어지고, 일어나야 한다. 3부의 자리가 그곳이다.

장기 실행 에이전트는 한 가지 잔인한 사실 위에 서 있다. **컨텍스트는 시간이 갈수록 부패한다.** Chroma의 *Context Rot* 연구가 18개 SOTA 모델을 동시에 굴려 보여 준 것이 이 사실이다.[^chroma-rot] 1M 윈도우를 가진 모델이 50K 토큰에서 무너지기 시작한다. 단순 검색조차 신뢰가 떨어진다. 게다가 의미 유사도가 낮을수록, 그리고 — 놀랍게도 — *구조적 일관성이 높을수록* 더 떨어진다. 깨끗한 회의록이 더 나쁜 결과를 낸다는 뜻이다. 이 사실을 받아들이지 않으면 우리가 짜는 어떤 하네스도 며칠을 못 버틴다.

그래서 3부는 그 부패에 맞서는 여섯 가지 응답을 차례로 본다.

10장 — **Context Rot.** 적을 먼저 안다. 1M 윈도우의 약속이 왜 50K에서 깨지는지, 한국어 환경에서 그 50K가 왜 30~35K로 더 빨리 오는지를 본다. 컨텍스트를 *희소 자원*으로 다루는 본능을 만들자. 여기서 시그니처 한 문장을 박는다. "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."[^anthropic-context]

11장 — **2-Prompt 패턴.** 한 번 부패가 일어난다는 사실을 받아들이면, 매 세션이 *깡통 컨텍스트*에서 시작한다는 설계가 자연스러워진다. Anthropic이 *Effective harnesses for long-running agents*에서 정리한 Initializer + Coding 분리, 그리고 디스크 위 산출물(`claude-progress.txt`)이 모델 메모리를 대체하는 메커니즘을 본다.[^anthropic-harness1]

12장 — **Ralph Loop.** 깡통 컨텍스트를 인정하면 루프는 단순할수록 강하다. Geoffrey Huntley의 한 줄 — "Ralph is a Bash loop." — 이 어떻게 2025년 12월 Anthropic 공식 플러그인이 됐는지를 본다.[^ralph-everything] [^ralph-anthropic] 그리고 Sondera의 *Supervising Ralph* — Principal Skinner 감독 패턴을 곁들인다.[^ralph-supervisor]

13장 — **Generator-Evaluator.** 루프가 돌면, 그 출력은 누가 채점하는가. 같은 모델이 자기 결과를 평가하면 왜 과대평가하는지, Anthropic이 Planner-Generator-Evaluator로 나눠 5~15회 반복으로 4시간을 수렴시킨 메커니즘을 분해한다.[^anthropic-harness2] [^infoq-3agent] 비밀은 컨텍스트 보존이 아니라 *컨텍스트 리셋 + 구조화된 핸드오프*다.

14장 — **단일 vs 다중.** 둘이 좋다면 셋·다섯·열은. Cognition이 *Don't Build Multi-Agents*로 못을 박은 같은 주에 Anthropic이 멀티에이전트 리서치 시스템 사례를 발표한 그 모순,[^cognition-dontbuild] 그리고 그 사이에 형성된 합의 — 쓰기 위주 의존성 강한 작업은 단일, 읽기 위주 병렬 가능 작업은 다중 — 을 본다. Cognition이 한 해 뒤 *Multi-Agents: What's Actually Working*에서 입장을 어떻게 진화시켰는지도 같이 본다.[^cognition-working]

15장 — **관측과 비용.** 토폴로지가 정해졌다면, 그 운동을 어떻게 *숫자*로 지킬까. 5축 메트릭 — latency·token·cost·success rate·regression delta — 을 정의하고, OpenTelemetry GenAI 시맨틱 컨벤션 위에서 LangSmith·Helicone·Langfuse·Phoenix가 어떻게 다른지 본다. 4장에서 유보한 Sonnet 4.5→4.6 회귀 사건을 운영 케이스 스터디로 마무리한다.

3부의 흐름은 이렇게 직선이다. **부패를 인정한다 → 매 세션을 깡통으로 본다 → 루프를 단순하게 만든다 → 평가자를 분리한다 → 토폴로지를 골라낸다 → 숫자로 지킨다.** 한 챕터씩 끝낼 때마다 우리 손에 남는 것이 늘어난다. 9장까지가 *서 있는* 척추였다면, 3부 끝에는 *걷는* 척추가 남는다.

함께 걸어 보자. 10장에서 가장 잔인한 사실부터 시작한다.

[^chroma-rot]: Chroma Research, *Context Rot: How Increasing Input Tokens Impacts LLM Performance*. https://research.trychroma.com/context-rot
[^anthropic-context]: Anthropic Engineering, *Effective context engineering for AI agents*. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[^anthropic-harness1]: Anthropic Engineering, *Effective harnesses for long-running agents*, 2025-11. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
[^ralph-everything]: Geoffrey Huntley, *Everything is a Ralph loop*. https://ghuntley.com/loop/
[^ralph-anthropic]: Anthropic Claude Code, *Ralph Wiggum Plugin*. https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md
[^ralph-supervisor]: Sondera, *Supervising Ralph: Why Every Wiggum Loop Needs a Principal Skinner*. https://blog.sondera.ai/p/ralph-wiggum-principal-skinner-agent-reliability
[^anthropic-harness2]: Anthropic Engineering, *Harness design for long-running application development*, 2026-03. https://www.anthropic.com/engineering/harness-design-long-running-apps
[^infoq-3agent]: InfoQ, *Anthropic Designs Three-Agent Harness Supports Long-Running Full-Stack AI Development*. https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/
[^cognition-dontbuild]: Cognition AI, *Don't Build Multi-Agents*, 2025-06-12. https://cognition.ai/blog/dont-build-multi-agents
[^cognition-working]: Cognition AI, *Multi-Agents: What's Actually Working*. https://cognition.ai/blog/multi-agents-working
