# 부록 A — 용어집

이 책 전체에서 같은 정의로 사용한 핵심 용어를 한자리에 모았다.

| 용어 | 정의 | 처음 박은 자리 |
|---|---|---|
| **하네스 (Harness)** | 모델 외 모든 것 — 루프·도구·컨텍스트·메모리·가드레일·추적·오케스트레이션 | 2장 |
| **에이전트 (Agent)** | Model + Harness | 2장 |
| **빌딩블록** | Claude Code의 7개 — CLAUDE.md, settings.json, Hooks, Slash Commands, Skills, Subagents, MCP | 2장 |
| **결정적 자동화** | 모델 출력 품질에 의존하지 않는 예측 가능한 정상화·차단·검증 | 5장 |
| **톱니바퀴 (Ratchet)** | 한 번 명시화되면 뒤로 가지 않는 팀의 누적 학습 메커니즘 | 1장 도입, 7장 명시화 |
| **지휘자 (Conductor)** | 코드 더 쓰는 사람이 아니라 여러 인스턴스와 사람을 동시에 조율하는 테크리드의 새 정체성 | 9장 도입, 10장 회수 |
| **4지선다 결정 프레임** | CLAUDE.md(ALWAYS) / Skill(WHAT) / Subagent(WHO) / 메인+Task(DYNAMIC) — 팀 지식을 어디에 둘지의 핵심 분기 | 7장에서 응축, 부록 D.1 |
| **한 사람의 병렬 vs 한 작업의 협업** | 워크트리 격리(전자) vs 멀티 에이전트 오케스트레이션(후자) — 5–10명 팀의 두 종류 충돌 | 3장 첫 단락에서 분리 |
| **한 시간 온보딩** | 신규 입사자가 월요일 9시에 받는 1시간 절차표 — ratchet의 본질을 절차로 구현 | 7장 마지막 절 |
| **PR 정책 재설계** | AI가 코드를 쓰는 시대의 PR 리뷰 거버넌스 — 승인 수·AI 흔적·자동 머지·intent 공유 | 5장 미니 절, 9장 매트릭스 |

---

# 부록 B — 한 시간 온보딩 워크시트 템플릿

7장에서 다룬 1시간 절차표를 너의 팀 버전으로 적어 쓸 수 있도록 빈 양식으로 둔다.

## 신규 입사자 월요일 9시 ~ 10시 절차

| 시간 | 단계 | 너의 팀 버전 (적어 두자) |
|---|---|---|
| 0–10분 | repo clone + `.claude/` 폴더 trust → Plugin marketplace 자동 설치 | |
| 10–25분 | CLAUDE.md 60줄 통독 → 팀 헌법 학습 | |
| 25–45분 | 첫 작업 실행 — Generator-Verifier 워크플로 체험 | |
| 45–60분 | 발견한 첫 어색함을 CLAUDE.md PR로 추가 — 신입의 첫 ratchet 칸 | |

## 첫날 끝나기 전 새 멤버에게 묻는 두 가지

1. 오늘 이상하게 느낀 한 가지는 무엇인가?
2. 그것을 우리 팀 헌법에 한 줄로 추가한다면 어떻게 적겠는가?

이 두 질문의 답이 바로 그날의 톱니 칸이다.

---

# 부록 C — 결정 트리 7선 (한 페이지 카드)

본문 각 챕터에서 만난 분기를 한 페이지에 모아 둔다. 책을 덮은 다음에도 책상에 놓고 쓸 수 있도록 카드 형식으로 응축했다.

## C.1 4지선다 — 팀 지식을 어디에 둘 것인가 (7장)

```
                  [어떤 지식인가?]
                        |
        ┌───────────────┼───────────────┐
        |               |               |
  항상 적용?         작업 종류        분리된 머리
   (헌법성)          정의?           필요?
        |               |               |
   CLAUDE.md         Skill           Subagent
   (ALWAYS)          (WHAT)           (WHO)
                        |
                  일회성 위임만 필요?
                        |
                  메인 + Task
                  (DYNAMIC)
```

## C.2 Hook vs CLAUDE.md vs Skill — 어디에 박을 것인가 (5장)

```
[매번 반드시 일어나야 하나?]
   YES → Hook (강제)
   NO  → [어떤 작업 종류에서만 일어나나?]
            YES → Skill (조건부 자동 로드)
            NO  → CLAUDE.md (권장)
```

## C.3 MCP vs CLI — 외부 시스템과 어떻게 말할 것인가 (4장)

```
[해당 작업이 보안/네트워크 경계를 넘어야 하나?]
   YES → MCP (게이트웨이로 활용)
   NO  → [기존 CLI/SDK가 있는가?]
            YES → CLI 호출 (Shankar 패턴)
            NO  → MCP (또는 자체 Skill)
```

## C.4 Block-at-submit vs Hook 적극 — 자동화 강도 (5장)

```
[작업이 plan 단계에서 차단되면 좌절감 큰가?]
   YES → Block-at-submit (commit 시점만 검증)
   NO  → Hook 적극 (PreToolUse부터 차단)
```

## C.5 워크트리 vs 멀티 에이전트 — 어떤 충돌인가 (3장)

```
[누가 누구와 부딪히나?]
   한 사람 / 자기 4탭   → 워크트리 격리 + 브랜치 디시플린
   여러 사람 / main      → PR 게이트 + 자동 머지 정책
```

## C.6 PR 자동 머지 허용 범위 (5장·9장)

```
[변경의 위험 등급은?]
   linter/formatter only      → 자동 머지 OK
   사람 1명 승인 후           → 자동 머지 OK (코드 변경 작은 경우)
   인증·결제·DB 스키마        → 절대 금지 (사람 게이트 의무)
```

## C.7 MCP 추상화 vs 보안 게이트웨이 (4장)

```
[MCP를 무엇으로 다룰 것인가?]
   API 추상화로            → 모든 외부 시스템에 MCP를 두려는 위험
   보안/auth 게이트웨이로  → MCP는 신뢰 경계, 그 안의 변환은 Skill (Willison 입장)
```

각 카드는 4장·5장·7장 본문의 결정 자리에서 "→ 부록 C.N 참조" 표기로 연결된다. 본문이 노후화되면 이 카드부터 갱신하면 된다.

---

# 부록 D — 참고문헌

이 책 본문은 [W#] / [P#] / [C#] 식별자로 인용했다. 식별자별 출처는 다음과 같다. 모든 URL은 2026-04-26 기준 접근 확인.

## 웹 (W)

- **[W1]** Skill Issue: Harness Engineering for Coding Agents — HumanLayer Blog. https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
- **[W2]** Effective harnesses for long-running agents — Anthropic Engineering. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **[W3]** Developer's guide to multi-agent patterns in ADK — Google Developers Blog. https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
- **[W4]** Harness engineering for coding agent users — Martin Fowler / Birgitta Böckeler 외. https://martinfowler.com/articles/harness-engineering.html
- **[W5]** Anthropic Best Practices for Agentic Coding. https://www.anthropic.com/engineering/claude-code-best-practices
- **[W6]** Beyond Prompts and Context: Harness Engineering for AI Agents — MadPlay. https://madplay.github.io/en/post/harness-engineering
- **[W7]** Agent Harness Engineering — AddyOsmani.com. https://addyosmani.com/blog/agent-harness-engineering/
- **[W8]** The Anatomy of an Agent Harness — Avi Chawla. https://blog.dailydoseofds.com/p/the-anatomy-of-an-agent-harness
- **[W9]** What is an agent harness? — Parallel Web Systems. https://parallel.ai/articles/what-is-an-agent-harness
- **[W10]** Awesome Harness Engineering. https://github.com/ai-boost/awesome-harness-engineering
- **[W11]** Governing Claude Code: Secure Agent Harness Rollouts with Kong AI Gateway. https://konghq.com/blog/engineering/claude-code-governance-with-an-ai-gateway
- **[W12]** Claude Code: Hooks, Subagents, and Skills — Complete Guide (ofox.ai). https://ofox.ai/blog/claude-code-hooks-subagents-skills-complete-guide-2026/
- **[W13]** Manage costs effectively — Claude Code Docs. https://code.claude.com/docs/en/costs · Best Ways to Monitor Claude Code Token Usage and Costs in 2026 — DEV. https://dev.to/kuldeep_paul/best-ways-to-monitor-claude-code-token-usage-and-costs-in-2026-5j3 · Branch8: How We Cut Claude Code Costs 70%. https://branch8.com/posts/claude-code-token-limits-cost-optimization-apac-teams
- **[W14]** Hooks reference — Claude Code Docs. https://code.claude.com/docs/en/hooks · Claude Code Hooks Guard (Zenn). https://zenn.dev/tmasuyama1114/articles/claude_code_hooks_guard_bash_command
- **[W15]** Three AI coding agents leaked secrets through a single prompt injection — VentureBeat. https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026 · AI slop PRs — DEV. https://dev.to/adioof/ai-slop-prs-are-ruining-code-review-for-everyone-56ip · GitHub Kill Switch Discussion (HN). https://news.ycombinator.com/item?id=46884471
- **[W17]** Agent Harness Engineering — The Rise of the AI Control Plane (Adnan Masood). https://medium.com/@adnanmasood/agent-harness-engineering-the-rise-of-the-ai-control-plane-938ead884b1d
- **[W18]** Observability with OpenTelemetry — Claude Agent SDK Docs. https://code.claude.com/docs/en/agent-sdk/observability · SigNoz Claude Code Monitoring. https://signoz.io/blog/claude-code-monitoring-with-opentelemetry/
- **[W19]** AI Agent Harness, 3 Principles for Context Engineering (Hugo Bowne-Anderson). https://hugobowne.substack.com/p/ai-agent-harness-3-principles-for
- **[W21]** Agentic Harness Engineering: LLMs as the New OS — Decoding AI. https://www.decodingai.com/p/agentic-harness-engineering
- **[W22]** Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support — arXiv 2511.15755. https://arxiv.org/abs/2511.15755
- **[W23]** Claude Code vs Codex CLI vs Aider vs OpenCode vs Pi vs Cursor — thoughts.jock.pl. https://thoughts.jock.pl/p/ai-coding-harness-agents-2026 · Builder.io: Claude Code vs Cursor. https://www.builder.io/blog/cursor-vs-claude-code · 2026 Guide to Coding CLI Tools — Tembo. https://www.tembo.io/blog/coding-cli-tools-comparison
- **[W24]** Claude Skills vs Subagent — eesel AI. https://www.eesel.ai/blog/skills-vs-subagent · Stop Adding New Claude Skills. https://buildtolaunch.substack.com/p/claude-skills-not-working-fix · Skills explained — Anthropic. https://claude.com/blog/skills-explained
- **[W25]** Claude Skills are awesome, maybe a bigger deal than MCP — Simon Willison. https://simonwillison.net/2025/Oct/16/claude-skills/
- **[W26]** Dive into Claude Code: The Design Space (arXiv 2604.14228). https://arxiv.org/abs/2604.14228 · Anthropic Managed Agents — InfoQ. https://www.infoq.com/news/2026/04/anthropic-managed-agents/ · Geoffrey Litt "Code like a surgeon" (Oct 2025). https://www.geoffreylitt.com/
- **[W27]** Equipping agents for the real world with Agent Skills — Anthropic Engineering. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills · Skill authoring best practices. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- **[W28]** Create and distribute a plugin marketplace — Claude Code Docs. https://code.claude.com/docs/en/plugin-marketplaces · Cowork and plugins for teams. https://claude.com/blog/cowork-plugins-across-enterprise · Building a Private Claude Code Plugin Marketplace. https://dominic-boettger.com/blog/claude-code-private-plugin-marketplace-guide/
- **[W29]** How Anthropic teams use Claude Code — Anthropic blog. https://claude.com/blog/how-anthropic-teams-use-claude-code
- **[W30]** How I Use Every Claude Code Feature — Shrivu Shankar. https://blog.sshh.io/p/how-i-use-every-claude-code-feature
- **[W31]** anthropics/claude-code-security-review GitHub Action. https://github.com/anthropics/claude-code-security-review · Code Review docs. https://code.claude.com/docs/en/code-review · Automate security reviews — Anthropic blog. https://claude.com/blog/automate-security-reviews-with-claude-code · Deriv automated security code reviews. https://derivai.substack.com/p/automated-security-code-reviews-claude-code-github-actions
- **[W32]** Claude Code: Anthropic's Agent in Your Terminal — Latent Space (Cat Wu, Boris Cherny). https://www.latent.space/p/claude-code · Why Anthropic Thinks AI Should Have Its Own Computer — Felix Rieseberg. https://www.latent.space/p/felix-anthropic
- **[W33]** Can Claude Code Replace a Junior Developer? — DEV. https://dev.to/themachinepulse/can-claude-code-replace-a-junior-developer-i-tested-it-f5i · The Senior Developer's New Role. https://www.tech-reader.blog/2026/04/the-secret-life-of-claude-code-senior.html
- **[W34]** 개발자 AI 지원, 어디까지 왔나 — CIO Korea (Anthropic·Toss·올리브영 라운드테이블). https://www.cio.com/article/4111488/
- **[W35]** Karpathy 2025 LLM Year in Review. https://karpathy.bearblog.dev/year-in-review-2025/ · Closing the Loop: Coding Agents, Telemetry — Arize. https://arize.com/blog/closing-the-loop-coding-agents-telemetry-and-the-path-to-self-improving-software/
- **[W36]** Claude Code Context Window: Optimize Your Token Usage. https://claudefa.st/blog/guide/mechanics/context-management · Practical Lessons From the Claude Code Leak — Generative Programmer. https://generativeprogrammer.com/p/practical-lessons-from-the-claude

## 논문 (P)

- **[P1]** Liu J, Zhao X, Shang X, Shen Z. *Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems.* arXiv:2604.14228 (2026.04). https://arxiv.org/abs/2604.14228
- **[P2]** *Prompt Injection Attacks on Agentic Coding Assistants.* arXiv:2601.17548 (2026.01). https://arxiv.org/abs/2601.17548
- **[P3]** *Indirect Prompt Injections: Are Firewalls All You Need?* arXiv:2510.05244 (2025.10). https://arxiv.org/abs/2510.05244
- **[P4]** *AgentForge: Execution-Grounded Multi-Agent LLM Framework.* arXiv:2604.13120 (2026). https://arxiv.org/abs/2604.13120
- **[P5]** Shinn N et al. *Reflexion: Language Agents with Verbal Reinforcement Learning.* arXiv:2303.11366 (NeurIPS 2023). https://arxiv.org/abs/2303.11366
- **[P6]** Wang G et al. *Voyager: An Open-Ended Embodied Agent.* https://voyager.minedojo.org/
- **[P7]** *The Landscape of Agentic Reinforcement Learning for LLMs.* arXiv:2509.02547 (2025). https://arxiv.org/abs/2509.02547
- **[P8]** Ferdowsi M et al. *From Teacher to Colleague: How Coding Experience Shapes Developer Perceptions of AI Tools.* arXiv:2504.13903 (2025.04). https://arxiv.org/abs/2504.13903
- **[P9]** *Human-AI Experience in Integrated Development Environments.* arXiv:2503.06195 (2025). https://arxiv.org/abs/2503.06195
- **[P10]** *Examining the Use and Impact of an AI Code Assistant on Developer Productivity.* CHI 2025 EA. https://dl.acm.org/doi/10.1145/3706599.3706670
- **[P11]** *SWE-Bench Pro.* arXiv:2509.16941 (2025). https://arxiv.org/abs/2509.16941
- **[P12]** Liu X et al. *AgentBench.* arXiv:2308.03688 (2023). https://arxiv.org/abs/2308.03688
- **[P13]** *SWE-EVO: Long-Horizon Software Evolution Benchmark.* arXiv:2512.18470 (2026). https://arxiv.org/abs/2512.18470
- **[P14]** *A Survey on Code Generation with LLM-based Agents.* arXiv:2508.00083 (2025). https://arxiv.org/abs/2508.00083
- **[P15]** *Architectural Design Decisions in AI Agent Harnesses.* arXiv:2604.18071 (2026). https://arxiv.org/html/2604.18071v1
- **[P16]** *The Design Space of LLM-Based AI Coding Assistants.* UCSD/VLHCC 2025. https://lau.ucsd.edu/pubs/2025_analysis-of-90-genai-coding-tools_VLHCC.pdf
- **[P17]** *Rethinking Software Development Considering Collaboration with AI Assistants.* ICSE 2025 Companion. https://dl.acm.org/doi/10.1109/ICSE-Companion66252.2025.00045
- **[P18]** *Multi-Agent LLM Orchestration for Incident Response.* arXiv:2511.15755 (2025). https://arxiv.org/abs/2511.15755
- **[P19]** AgenticSE Workshop @ ASE 2025. https://agenticse.github.io/

## 커뮤니티 (C)

- **[C1]** Claude Code로 5명 팀처럼 개발하는 법 — GeekNews. https://news.hada.io/topic?id=22716
- **[C2]** 일상적으로 사용하는 Claude Code 팁과 모범 사례 50가지 — GeekNews. https://news.hada.io/topic?id=27677
- **[C3]** Reddit r/ClaudeAI subagent/skill 논의 (간접 — eesel·Verdent·Towards Data Science 정리, [W24]에서 인용)
- **[C4]** Claude Code 사용기 — velog (laply 외). https://velog.io/@laply/Claude-Code-사용기
- **[C5]** AI와 함께하는 DevOps: Claude Code로 생산성 10배 — Yonghyun Kim, Medium (IMWEB 인프라팀). https://medium.com/@baramboys0615/
- **[C6]** Claude Code 6주 사용기 — GeekNews. https://news.hada.io/topic?id=22375 · Claude Code 2주 사용 후기. https://news.hada.io/topic?id=22053
- **[C7]** Claude로 코드리뷰 경험 개선하기 — velog. https://velog.io/@kwonhl0211/Claude로-코드리뷰-경험-개선하기
- **[C8]** Anthropic팀은 어떻게 Claude Code를 사용하는가? — velog. https://velog.io/@euisuk-chung/Anthropic-Claude-Code-케이스-스터디
- **[C9]** How I'm Productive with Claude Code — Hacker News. https://news.ycombinator.com/item?id=47494890
- **[C10]** Effective harnesses for long-running agents — Hacker News. https://news.ycombinator.com/item?id=46081704
- **[C11]** Claude Code introduces specialized sub-agents — Hacker News. https://news.ycombinator.com/item?id=44686726
- **[C12]** A Guide to Claude Code 2.0 — sankalp. https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/
- **[C13]** 실제 경험: Claude Code와 Cursor — velog (takuya). https://velog.io/@takuya/실제-경험-Claude-Code와-Cursor-일주일-사용-후-알게-된-진짜-비용-효율
- **[C14]** Claude Code 마스터하기: AI 시대 API 개발 효율화 테크닉 34선 — velog. https://velog.io/@takuya/ai-api-workflow-claude-code-efficiency-tips
- **[C15]** Awesome Claude Code Subagents — VoltAgent. https://github.com/VoltAgent/awesome-claude-code-subagents
- **[C16]** Awesome Claude Skills — travisvn. https://github.com/travisvn/awesome-claude-skills

## 본문에서 사용한 § 표기

본문에 등장한 [§N.M] 표기는 모두 이 책 쓰기 단계의 리서치 종합본 내부 섹션 참조다. 독자가 직접 따라가야 할 필요는 없으며, 동일 사실은 위의 [W#]/[P#]/[C#] 출처에서 확인할 수 있다. 핵심 매핑은 다음과 같다.

- §1, §2 (개념·정의·빌딩블록 표) → W1, W7, W8, W17, P1, P15
- §3.1 (안전·권한) → W11, W14, W15, P1, P2, P3
- §3.2 (자동화) → W14, W30, W31, C2
- §3.3 (멀티 에이전트) → W2, W3, W22, W26, P4, P5, P6, P18
- §3.4 (관측·비용) → W13, W18, W32, C13
- §3.5 (도메인 지식 코드화) → W7, W24, W25, W27, W28, W30, C2
- §4 (도입과 거버넌스) → W11, W33, W34, P8, P9, P10
- §5 (사례) → W26, W29, W34, C1, C5, C6, C7, C8
- §6 (안티패턴) → W15, W24, W36, C2, C13
- §7 (생태계·미래) → W23, W26, W32, W33, W35, P11, P13, P19
- §8.1 (Subagent 분할) → W2, W24, W30, C11
- §8.2 (Hook 강제) → W14, W30
- §8.3 (자동 머지) → W30, W31, W34
- §8.4 (CLAUDE.md 자동/수동) → W7, W30
- §8.5 (모델 vs 하네스) → W1, W19, W21, W35
- §8.6 (시니어/주니어) → W33, W34, P8, P10
- §8.7 (도구 다중화) → W23, C13
- §8.8 (MCP의 역할) → W11, W25, W30
