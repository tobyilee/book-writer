# 웹 리서치 — 공식 프롬프트 엔지니어링 가이드 & eval 도구

> 검색 시점: 2026-06-01. 1차 소스(공식 문서·공식 발표) 우선 수집.

## 0. 모델 버전 확인 (1차 소스)

| 사용자 표기 | 실제 확인된 명칭 | 릴리스 | 1차 소스 | 비고 |
|---|---|---|---|---|
| Claude Opus 4.8 | **Claude Opus 4.8** (`claude-opus-4-8`) | 2026-05-28 | anthropic.com/news/claude-opus-4-8 | ✅ 정확. 가격 $5/$25 per Mtok, fast mode $10/$50 |
| GPT-5.5 | **GPT-5.5** (variants: Thinking/Pro 4/23, Instant 5/5) | 2026-04-23 (API 4/24) | openai.com/index/introducing-gpt-5-5, en.wikipedia.org/wiki/GPT-5.5, developers.openai.com/api/docs/models/gpt-5.5 | ✅ 정확. context 1,050,000 tok, max output 128k, knowledge cutoff 2025-12-01 |
| Gemini 3.5 Flash | **Gemini 3.5 Flash** | 2026-05-19 (I/O 2026) | blog.google/innovation-and-ai/.../gemini-3-5, deepmind.google/models/gemini/flash | ✅ 정확. Gemini 3 Flash(상위 빠른 모델)와 3.5 Flash 구분 존재. 3.5 Flash가 현재 Gemini 앱 기본 |

세 모델명 모두 **2026-06-01 기준 실재·현행**으로 1차 소스 확인됨. 정정 필요 없음.

주의: OpenAI의 **현행 최신 플래그십은 GPT-5.2**(`reasoning_effort` 기본 `none`)로, GPT-5.5는 ChatGPT 기본 모델 라인. 공식 cookbook의 "최신 모델 가이드"는 GPT-5 → 5.1 → 5.2 순으로 갱신됨. GPT-5.5 전용 cookbook 가이드는 별도 확인 안 됨 — API docs가 `/api/docs/guides/latest-model`로 안내. (사실 확인 필요: GPT-5.5 ↔ GPT-5.2 계보 관계)

---

## 1. Anthropic / Claude 공식 가이드

출처: platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/ (overview + claude-prompting-best-practices). 발행: 현행 docs(상시 갱신), 검색 2026-06-01.

### 일반 원칙 (general principles)
- **Be clear and direct**: "brilliant but new employee" 비유. Golden rule — "동료에게 프롬프트를 보여줘 헷갈리면 Claude도 헷갈린다."
- **Add context/motivation**: 이유를 설명하면 일반화한다. 예: "NEVER use ellipses" → "TTS 엔진이 읽으므로 생략부호 금지."
- **Use examples (few-shot/multishot)**: 3–5개 권장. relevant·diverse·structured. `<example>`/`<examples>` 태그로 감싼다.
- **XML 태그로 구조화**: `<instructions>`, `<context>`, `<input>` 등. 일관·서술적 태그명, 자연 계층은 중첩.
- **Role 부여**: system 프롬프트에 한 문장이라도. 예 `system="You are a helpful coding assistant specializing in Python."`
- **Long context (20k+ tokens)**: 긴 문서를 **프롬프트 상단**에 배치(쿼리는 끝에 — 응답 품질 최대 30%↑). 각 문서를 `<document>`/`<document_content>`/`<source>` 태그로. "관련 부분을 먼저 인용(quote)하게" 시켜 노이즈 절감.

### Opus 4.8 특이사항
- **out of the box**: 기존 Opus 4.7 프롬프트에 잘 동작.
- **Verbosity**: 작업 복잡도에 맞춰 길이를 스스로 조절. 고정 verbosity 아님. 줄이려면 "Provide concise, focused responses..." 추가. **부정 예시보다 긍정 예시가 효과적**.
- **effort 파라미터** (intelligence ↔ token/속도 트레이드오프): `low / medium / high / xhigh / max`.
  - 코딩·에이전트: `xhigh` 권장. intelligence-sensitive: 최소 `high`.
  - `max`: 일부 향상되나 overthinking 위험·수확 체감.
  - `low/medium`: 작업 범위를 요청대로만 한정(under-thinking 위험). 얕은 추론 보이면 prompt로 우회하지 말고 effort를 올려라.
  - "effort는 이전 어떤 Opus보다 중요하다 — 업그레이드 시 적극 실험하라."
- **Thinking**: 기본 OFF. `thinking: {type: "adaptive"}` 명시해야 켜짐. adaptive 트리거는 promptable. 큰 system 프롬프트로 과하게 thinking하면 가이드로 억제.
- **Tool use 트리거**: 추론을 도구 호출보다 선호하는 경향. 도구 사용 늘리려면 effort↑(high/xhigh) 또는 명시적 지시.
- **More literal instruction following**: 지시를 문자 그대로 해석, 자동 일반화 안 함. 범위를 명시("Apply to every section, not just the first").
- **prefill 폐기**: Claude 4.6+/Mythos부터 마지막 assistant 턴 prefill 미지원(400). 대안: Structured Outputs, 직접 지시, tool calling.
- **adaptive thinking 마이그레이션**: 구 `budget_tokens` → `effort`로. 코드 예시 `output_config={"effort": "high"}`.
- **markdown 억제**: "하지 말 것"보다 "할 것"으로. `<smoothly_flowing_prose_paragraphs>` 같은 XML 지시. LaTeX 기본 출력 → 평문 원하면 명시.

### 에이전트/코딩 팁 (Claude)
- 장기 작업·멀티 컨텍스트 윈도: tests.json·progress.txt·git로 상태 추적. context awareness(토큰 예산 인지).
- **overengineering 억제**: scope/documentation/defensive coding/abstractions 4항목 가이드 블록.
- **테스트 통과 집착·하드코딩 방지** 프롬프트, **hallucination 억제**(`<investigate_before_answering>`).
- 병렬 tool call `<use_parallel_tool_calls>` 블록.
- 코드리뷰 하네스: "only high-severity" 지시를 Opus 4.8이 더 충실히 따라 recall↓처럼 보일 수 있음 → "Report every issue... goal is coverage" 권장.

### Eval (Anthropic)
- 출처: docs.anthropic.com/en/docs/test-and-evaluate/develop-tests, .../eval-tool, anthropic.com/news/evaluate-prompts.
- **Claude Console 평가 도구**: 프롬프트 side-by-side 비교, 5점 척도 품질 채점, 프롬프트 버저닝·재실행. `{{변수}}` 더블 브레이스 필수. 테스트 케이스 수동/자동생성/CSV import.
- 원칙: "성공 기준 정의 → 평가 설계"가 프롬프트 엔지니어링의 핵심 사이클.
- **code-based grading**: 빠르고 신뢰성↑ 그러나 뉘앙스 부족. **LLM-based grading**: 유연·확장·복잡 판단 적합.
- 프롬프트 생성기/개선기(prompt improver) 콘솔 제공. 인터랙티브 튜토리얼: github.com/anthropics/prompt-eng-interactive-tutorial.

---

## 2. OpenAI / GPT-5.x 공식 가이드

출처: developers.openai.com/cookbook/examples/gpt-5/ (gpt-5, gpt-5-1, gpt-5-2 prompting guides), API docs models/gpt-5.5. 검색 2026-06-01.

### 핵심 파라미터
- **`reasoning_effort`**: GPT-5.5 API 기준 `none / low / medium(기본) / high / xhigh`. GPT-5.2는 `none / minimal / low / medium / high / xhigh`, 기본 `none`.
- **`verbosity`**: 최종 답변 길이를 추론 길이와 독립적으로 제어. 자연어 오버라이드 가능(글로벌 low + "코딩 툴은 high verbosity").
- API 기본은 Markdown 미사용 → 필요 시 "Use Markdown only where semantically correct" 지시. 긴 대화에서 준수 저하 → 3–5 메시지마다 재명시.

### GPT-5 prompting guide 핵심
- **Agentic eagerness 제어**: 줄이려면 reasoning_effort↓ + 명시적 early-stop 기준("Top hits converge ~70% on one area"). 늘리려면 effort↑ + persistence 프롬프트("You are an agent—keep going until the query is completely resolved...").
- **Tool preambles**: "사용자 목표를 먼저 재진술 → 구조화된 plan outline" 권장.
- **Responses API + `previous_response_id`**: 추론 컨텍스트 보존 → eval 73.9%→78.2% 향상.
- **Minimal reasoning**: 지연 민감 시. GPT-4.1식 명시 프롬프트 필요(짧은 사고 요약, preamble, 도구 지시 명확화).
- **Instruction following "surgical precision"**: 모순·모호 프롬프트가 더 해롭다. 명확한 instruction hierarchy 필요. prompt optimizer 도구로 점검.
- **Metaprompting**: GPT-5에게 프롬프트 개선을 시키는 패턴.
- **Cursor 사례**: `verbosity: low` 글로벌 + 코드엔 verbose 지시. context-gathering 과잉 강조 제거.

### GPT-5.2 (현행 플래그십) 변경점
- 더 신중한 scaffolding, 낮은 verbosity, 강한 instruction adherence. 기본 더 간결.
- 길이 제약 명시 권장: "3–6 sentences or ≤5 bullets" 베이스라인.
- 마이그레이션 3단계: ①프롬프트 변경 없이 모델 교체 ②reasoning_effort를 이전 지연 프로필에 맞춰 pin(4o/4.1→none, 기존 GPT-5의 minimal→none) ③eval로 baseline 후 회귀 시만 조정.
- 추출은 structured schema, scope discipline 블록(extra features 금지), 긴 컨텍스트(>10k)는 내부 outline·제약 재명시, 법률/금융은 self-check 단계.

### Eval (OpenAI)
- 출처: github.com/openai/evals, developers.openai.com/api/docs/guides/evals, cookbook getting_started_with_openai_evals.
- **openai/evals**: LLM·LLM 시스템 평가 프레임워크 + 벤치마크 레지스트리. 템플릿 사용 시 코드 작성 불필요 — JSON 데이터 + YAML 파라미터.
- 커스텀: `evals.Eval` 상속, `eval_sample`/`run` 오버라이드. (현재 custom code eval은 PR 미접수, model-graded YAML은 가능.)
- **Model grading 2단계**: 모델이 답 → 다른 모델이 정답 여부 판정. 프로그래매틱 + LLM grader 병행이 견고.
- Evals API로 회귀 테스트·MCP 평가 가능.

---

## 3. Google / Gemini 공식 가이드

출처: ai.google.dev/gemini-api/docs/prompting-strategies, .../gemini-3, .../whats-new-gemini-3.5, docs.cloud.google.com/.../gemini-3-prompting-guide. 검색 2026-06-01.

### Prompt design strategies (일반)
1. **Clear & specific instructions**. 2. **few-shot 항상 포함**("few-shot 없는 프롬프트는 덜 효과적"). 3. **context 추가**. 4. **constraints & response format**(할 것/하지말 것, 표·불릿). 5. **partial input completion**(접두로 패턴 유도). 6. **복잡 프롬프트 분해**(chaining/aggregation). 7. **파라미터 실험**(temperature/topK/topP/max tokens/stop).
- 구조화: XML 태그 또는 Markdown 헤더 — 한 프롬프트 안에선 한 형식만 일관 사용. **중요 지시는 앞에**.

### Gemini 3 / 3.5 특이사항 (1차 소스)
- **`thinking_level`**: `minimal / low / medium / high(기본)`. 빠른 응답엔 `low`. 복잡 추론엔 `high`. CoT 강제 프롬프트 대신 `thinking_level: "high"` + 단순 프롬프트로 대체 권장.
- **`media_resolution`**: 이미지 `media_resolution_high`(1120 tok), PDF `medium`(560), 비디오 `low/medium`(70 tok/frame).
- **Temperature = 1.0 유지 강력 권장**. 낮추면 looping·성능 저하(특히 수학·추론).
- **Verbosity**: Gemini 3는 기본적으로 덜 verbose·직접적. conversational 원하면 명시 steer.
- **Be precise and direct**, 입력 프롬프트 간결.
- 마이그레이션(2.5→3): temperature 설정 제거, media_resolution_high 테스트, CoT 강제 제거.

### Gemini 3.5 Flash 강점 (블로그)
- agent·coding 프런티어 성능, long-horizon 작업. 멀티모달 이해 선두(CharXiv Reasoning 84.2%). output tok/s 기준 타 프런티어 대비 4배 빠름. 리치·인터랙티브 웹 UI 생성.

---

## 4. eval 도구 횡단 정리 (서드파티)

### Promptfoo
출처: promptfoo.dev/docs/guides/llm-as-a-judge, .../configuration/expected-outputs, github.com/promptfoo/promptfoo. 검색 2026-06-01.
- 2026 사실상 표준 LLM 앱 평가 프레임워크. 선언적 YAML config + CLI + CI/CD. "Used by OpenAI and Anthropic."
- 기능: deterministic assertions, LLM-as-judge(`llm-rubric`, `g-eval`, `factuality`, `select-best`, multi-judge voting), 모델 비교, RAG eval, agent test, red teaming.
- `llm-rubric`: 기준 제공 → 모델이 출력 채점. grader는 환경 API 키로 자동 선택, assertion-level `provider`로 지정 가능. temperature/max_tokens pin 가능.
- 베스트프랙티스: judge는 테스트 대상과 무관하게 강한 단일 모델 고정.

### LangSmith / 기타
- (검색 시점 보조 — LangSmith는 LangChain의 trace·dataset·eval 플랫폼으로 회귀 테스트·LLM-as-judge 지원. 1차 문서 미수집, 추가 확인 필요.)

---

## 참고 URL (발행/검색 메타)
- Claude Opus 4.8 발표 — anthropic.com/news/claude-opus-4-8 (2026-05-28)
- Anthropic prompting best practices — platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices (현행 docs, 검색 2026-06-01)
- Anthropic eval tool — docs.anthropic.com/en/docs/test-and-evaluate/eval-tool, .../develop-tests; anthropic.com/news/evaluate-prompts
- GPT-5.5 소개 — openai.com/index/introducing-gpt-5-5 (2026-04-23); API docs developers.openai.com/api/docs/models/gpt-5.5
- GPT-5 / 5.2 prompting guide — developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide, .../gpt-5-2_prompting_guide
- OpenAI Evals — github.com/openai/evals; developers.openai.com/api/docs/guides/evals
- Gemini 3.5 발표 — blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5 (2026-05-19)
- Gemini prompt strategies — ai.google.dev/gemini-api/docs/prompting-strategies; .../gemini-3
- Promptfoo — promptfoo.dev/docs/guides/llm-as-a-judge; github.com/promptfoo/promptfoo
