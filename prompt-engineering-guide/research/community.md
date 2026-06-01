# 커뮤니티 리서치 — 실무자 프롬프트·코딩 에이전트·eval 경험담

> 검색 시점: 2026-06-01. 커뮤니티·블로그 소스는 신뢰도 낮음 — 공식 문서와 교차검증 필요한 항목은 (확인 필요) 표시.

## 1. 코딩 에이전트 프롬프트 (Claude Code / Cursor / Codex)

출처: agensi.io 설정 가이드(2026), sankalp's blog(Claude Code 2.0), Hannah Stulberg(30 tips), github VoltAgent/awesome-agent-skills, yzhao062/agent-style, shanraisshan/claude-code-best-practice. 검색 2026-06-01.

### 설정 레이어 (실무 합의)
2026년 코딩 에이전트 설정은 **5계층**으로 수렴:
1. **Custom instructions / CLAUDE.md** — 항상 켜진 컨텍스트. 수백 단어 권장(가볍게). 코딩 스타일·네이밍·프로젝트 컨텍스트·팀 표준·개인 선호.
2. **SKILL.md (Agent Skills)** — 온디맨드 전문성. 특정 작업군용 플레이북(지시·템플릿·컨텍스트).
3. **MCP servers** — 외부 도구 접근.
4. **.cursorrules / Cursor rules** — 에디터 특화.
5. **AGENTS.md** — 레포 루트의 프로젝트 컨텍스트(아키텍처·배포 절차). 버전관리·팀 공유.

### 실무 팁(커뮤니티 합의 수준)
- CLAUDE.md는 **짧고 고밀도**로. 거대 규칙 더미는 역효과 — 공식 가이드의 "over-prompting 억제"와 일치.
- **SKILL.md 보편 포맷**이 Claude Code/Codex/Gemini CLI/Cursor에 호환(2026-03 기준 공식+서드파티+커뮤니티 수천 개).
- "Claude Code가 CLI 코딩 UX를 주도, Codex·OpenCode·Amp·Cursor가 영향을 받음 — Claude Code 학습이 타 툴로 전이"된다는 주장(블로그, 확인 필요/주관적).
- agent-style 레포: AI 코딩·작성 에이전트용 "21 writing rules" 드롭인.

### 공식 가이드와 연결되는 코딩 에이전트 베스트프랙티스
- 첫 턴에 task·intent·constraints를 충분히 명시 → 자율성·토큰효율↑ (Anthropic Opus 4.8 "interactive coding products" 가이드와 정확히 일치).
- 코딩은 effort `xhigh`/`high` + auto 모드, 인간 개입 최소화 (Anthropic 공식).
- GPT-5/Cursor: `verbosity: low` 글로벌 + 코드는 verbose, context-gathering 과잉 제거 (OpenAI cookbook 사례).

## 2. 프롬프트 eval 실전 경험담

출처: promptfoo 가이드/qaskills(2026 complete guide)/nerdleveltech(CI 튜토리얼)/DataCamp 튜토리얼, aipmguru(Anthropic Console 첫 eval), learn-prompting(Claude evals guide). 검색 2026-06-01.

- **Promptfoo가 실무 표준**으로 자리. 선언적 YAML로 프롬프트/모델 비교, CI에 물려 회귀 방지. 실무자들이 "프롬프트도 코드처럼 테스트"하는 워크플로 정착.
- **LLM-as-judge는 단일 강한 judge 모델 고정**이 컨센서스(Promptfoo 권장과 일치). judge 모델을 테스트 대상과 분리.
- 실전 패턴: deterministic assertion(정규식·포함·JSON schema) 먼저 → 애매한 품질만 LLM-rubric. 비용·신뢰성 균형.
- Anthropic Console 첫 eval: 성공 기준 → `{{변수}}` 프롬프트 → 테스트 케이스 생성 → side-by-side 5점 채점 → 버전 반복(실무 글 다수).
- 주의(커뮤니티): LLM judge의 verbosity/position 편향을 직접 겪었다는 보고 다수 — 학술(Zheng 2023)과 일치. A/B 시 위치 무작위화·길이 정규화 권장.

## 3. awesome-prompt / 레지스트리

- github **VoltAgent/awesome-agent-skills**: 1000+ agent skill 큐레이션(Claude Code/Codex/Gemini CLI/Cursor 호환).
- "250 Best Claude Prompts for Developers"(mindwiredai, 2026-05 갱신) 등 프롬프트 라이브러리 — 품질 편차 큼, 출처 신뢰도 낮음(확인 필요).
- 공식 cookbook 레포(openai/openai-cookbook, anthropics/prompt-eng-interactive-tutorial)가 가장 신뢰할 보조 자료.

## 4. 활용 시나리오별 커뮤니티 신호
- **일상용**: 역할 부여 + 구체 맥락 + 출력 형식 지정의 3종 세트가 반복 추천. 모델별로 Gemini 3는 간결 기본·conversational은 명시 필요, Claude는 길이 자동조절.
- **학습용**: "초보에게 설명하듯", "단계별로", "예시와 함께", "이해도 확인 질문" 패턴. CoT를 학습 보조로 쓰는 글 다수.
- **코딩 에이전트**: 위 1절. 명시적 행동 지시("change this" vs "suggest"), 테스트 우선, scope 한정.

## 5. 리서치 한계 (커뮤니티)
- Reddit(r/LocalLLaMA·r/ChatGPT)·HN 스레드 본문 직접 인용은 US-only 검색·캐시 한계로 충분히 수집 못함 — 블로그/큐레이션 레포로 대체. 익명 주장은 (확인 필요) 표시.
- 세 신규 모델(특히 GPT-5.5·Gemini 3.5 Flash) 전용 실전 경험담은 릴리스가 최근(2026-04~05)이라 양이 적음 — 직전 모델(GPT-5/5.2, Gemini 3) 경험에서 외삽된 내용 많음.

## 참고 URL
- agensi.io/learn/ai-agent-configuration-guide-2026
- sankalp.bearblog.dev (Claude Code 2.0)
- github.com/VoltAgent/awesome-agent-skills
- promptfoo.dev/docs/guides/llm-as-a-judge ; qaskills.sh/blog/promptfoo-complete-guide-2026
- aipmguru.substack.com (첫 AI eval, Anthropic Console)
- github.com/openai/openai-cookbook ; github.com/anthropics/prompt-eng-interactive-tutorial
