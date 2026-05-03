# 에이전틱 코딩과 하네스 엔지니어링 — 저술 계획 (v1)

> 산출 일자: 2026-05-02
> 입력: `proposal.md`, `01_reference.md`, `toby-book-writing-style.md`
> 위치: 종합 바이블 (Comprehensive Bible) — 한국어권에서 하네스 엔지니어링을 정면으로 다루는 첫 두꺼운 책

---

## 1. 책 제목 후보

### 후보 A — 부제 분리형(가제 계승)
**『에이전틱 코딩의 시대: 모델을 통제하는 하네스 엔지니어링』**
- **캐릭터:** 무게감 있는 정공법. 기획안 가제를 거의 그대로 계승.
- **톤:** 진중·교과서적. 서점 매대에서 "이게 그 책인가" 하고 집어들게 만드는 정합성.
- **포지셔닝:** "산업의 변곡점을 정의하는 책"으로 읽힌다. *Designing Data-Intensive Applications* 같은 자리에 꽂힌다.
- **약점:** 다소 평이하다. 'AI 시대' 류의 책 제목이 과포화된 시장에서 후킹이 약할 수 있다.

### 후보 B — 직설·도발형
**『프롬프트 엔지니어링은 끝났다 — 하네스 엔지니어링 입문』**
- **캐릭터:** 도발적 선언형. 산업 합의(Osmani, Hashimoto, Anthropic, OpenAI가 동시에 같은 결론에 도달한 사실)를 정면으로 인용한다.
- **톤:** 기술 잡지 헤드라인. 표지에서 이미 메시지가 끝난다.
- **포지셔닝:** "패러다임이 바뀌었음을 모르는 사람을 위한 책"이 아니라 "이미 바뀐 줄 아는 사람이 다음 단계로 가는 책"으로 읽힌다.
- **약점:** 도발이 강해 보수적 독자에게 거부감. '입문'이 책의 무게(250~350쪽 종합 바이블)와 어긋난다.

### 후보 C — 비유·시적
**『고삐를 쥔 자: AI 에이전트와 하네스 엔지니어링의 모든 것』**
- **캐릭터:** 비유 중심. 'Harness=마구(말의 고삐)'라는 어원을 표지에 살린다.
- **톤:** 개념의 시적 해석. 한국어권 기술서로는 드문 결.
- **포지셔닝:** "책 한 권 읽으니 '하네스'라는 단어의 무게가 느껴진다" 류 후기를 만든다.
- **약점:** "고삐" 비유가 부정적으로 읽힐 위험(인간이 모델을 'AI 노예'처럼 다룬다는 인상). 부제 "모든 것"이 과하다는 인상도 가능.

### 추천: **후보 A**

종합 바이블이라는 책의 정체성과 가장 잘 맞는다. 5부 250~350쪽의 두께를 표지가 미리 약속한다. **단, 표지 카피로 후보 B의 메시지를 흡수하자**: "프롬프트의 시대는 끝났다. 이제 하네스를 설계하라." — 부제 위 헤드 카피로 박는다. 후보 C의 'Harness=마구' 비유는 1부 1장 도입에서 풀어낸다.

저자 표기: `Toby-AI` (프로젝트 규약).

---

## 2. 책 특성

| 항목 | 값 |
|------|-----|
| **장르** | 기술서 + 산업·사상 정리서 (이론 30% / 사례 30% / 실습 30% / 한국어 생태계 10%) |
| **분량** | 약 280~340쪽 (한글 약 22만~26만 자). 본문 22장 + 5부 인트로 + 부록 5종. |
| **난이도** | 중상 (현업 1~2단계 졸업자 대상). 기초 프롬프트·LLM 호출은 다루지 않는다. |
| **톤** | Toby 평어체 + 청유형. 수사적 질문으로 매 절 도입. 영어 1차 인용은 원문+의역 병기. |
| **개념 밀도** | 챕터당 핵심 용어 5~8개를 정확히 정의하고, 한국어/영어 병기. 용어집(부록)으로 흡수. |
| **실습 비중** | 모든 챕터 1개 이상 — 코드/설정/워크플로 시나리오 중 택일. 실습은 장비 없이 텍스트 따라 읽기만으로도 머릿속에서 돌아가게 설계. |
| **Toby 스타일 핵심 적용** | (1) "왜 그럴까?" → 자답 / (2) "~라고 해보자" 상황 가정 / (3) "난감하다·찜찜하다" 감정 공감 / (4) "~하는 편이 낫다" 권유 / (5) "기억해두자" 강조 |

---

## 3. 독자 여정 (Reader Journey)

**진입 상태:** Cursor·Claude Code·Copilot·Aider 정도는 써 봤다. AGENTS.md/CLAUDE.md를 한 번 작성해 봤지만 "왜 어떤 줄은 효과 있고 어떤 줄은 무시되는지" 모른다. 에이전트가 같은 실수를 반복하면 짜증을 내며 다시 프롬프트를 고친다.

**출구 상태 — 다음 다섯 가지 능력으로 측정한다:**

1. **(설계) 자기 팀의 워크플로를 CAR(Control·Agency·Runtime) 3축과 Guides·Sensors 2축으로 분해하고, 빈자리를 짚어낼 수 있다.**
2. **(저술) 거대 단일 AGENTS.md가 아닌 디렉토리 분산 + 계층화된 메모리 파일을 설계해, 컨텍스트 예산을 의식적으로 배분할 수 있다.**
3. **(운영) 장기 실행 작업에 2-prompt(Initializer + Coding) 또는 3-에이전트(Planner-Generator-Evaluator) 패턴을 적용하고, `progress.txt`·서브에이전트로 컨텍스트 부패를 통제할 수 있다.**
4. **(보안) Lethal Trifecta·Shai-Hulud 같은 사고 사례를 자기 환경에 비춰 재현하고, MicroVM·egress 화이트리스트·MCP 권한 모델로 1차 방어선을 구성할 수 있다.**
5. **(평가·진화) Inspect·Terminal-Bench·SWE-Bench 같은 평가 하네스로 자기 하네스의 성능 회귀를 정량 측정하고, 메타 하네스(스스로 갱신되는 AGENTS.md) 패턴을 시도할 수 있다.**

이 5가지가 책 전체의 학습 목표다. 각 부가 한 능력씩 책임진다(5부는 4·5번을 한국어 환경 적응과 묶어 마무리한다).

---

## 4. 내러티브 아크 (왜 이 순서인가)

이 책은 **"산업의 합의가 어떻게 생겼는지(왜) → 그 합의를 어떻게 분해하는지(무엇) → 어떻게 운영하는지(어떻게) → 어떻게 보호하는지(안전) → 어디서 더 갈 수 있는지(현장과 미래)"**의 5단 흐름을 따른다.

**1부**는 거울이다. Hashimoto의 6단계 도입 여정 [^hashimoto] 을 들어 독자에게 "당신은 지금 몇 단계인가"를 묻는다. Osmani·Anthropic·OpenAI가 같은 시기에 같은 결론에 도달했다는 사실을 타임라인으로 보여 준다. 평가 하네스와 런타임 하네스가 동형(同形)임을 받아들이는 순간, 책이 다룰 좌표가 정해진다.

**2부**는 척추다. CAR 3축 — Control·Agency·Runtime — 으로 하네스를 분해하고, Böckeler의 Guides·Sensors 프레임워크 [^bockeler-main] 와 SWE-agent의 ACI 4원칙 [^swe-agent-paper] 으로 골격을 세운다. 책에서 가장 이론적이지만, 매 챕터 끝에 "당신의 AGENTS.md를 이 렌즈로 다시 봐 보자"는 자가 점검을 끼운다.

**3부**는 운동이다. 척추가 어떻게 움직이는지를 본다. 컨텍스트 부패와 그 대응(2-prompt·압축기·Ralph Loop), 단일 vs 다중 에이전트 논쟁의 합의점, Generator-Evaluator의 정량적 효과, 메타 하네스로 가는 길. 이 부 끝에서 독자는 "장기 실행 작업을 어떻게 살아 있게 둘지"의 답을 얻는다.

**4부**는 안전이다. 하네스 자체가 공격 표면이 되었다. Lethal Trifecta로 위협 모델을 익히고, Shai-Hulud 사고를 분해하고, MicroVM·Inspect 샌드박스로 격리를 짠다. 평가 회피(sandbagging)까지 다뤄, "보안과 평가는 같은 동전의 양면"이라는 결론에 닿는다.

**5부**는 현장이다. SWE-Bench·Terminal-Bench·OSWorld·METR Time Horizon 같은 평가 인프라를 자기 손에 쥐는 법, OpenHands·Aider·Cursor·Claude Code·Codex CLI를 비교하는 렌즈, 그리고 한국어 생태계(revfactory·instructkr·Haandol·MadPlay)와 한국 환경 특수 이슈(한글 토큰 비용·사내 보안 정책). 마지막 챕터는 메타 하네스와 미래 전망으로 책을 닫는다.

**부록**은 실무자를 위한 작업대다. 본문이 "왜·무엇·어떻게"라면, 부록은 "오늘 당장 손에 쥐고 시작할 도구함"이다.

이 순서가 깨질 수 있는 유일한 지점: **2부 5장(ACI 4원칙)을 1부 직후로 당기고 싶은 유혹**. 하지만 ACI는 추상이 강해서, CAR 분해를 먼저 보여 주고 그 안에 ACI를 끼워야 독자가 길을 잃지 않는다.

---

## 5. 챕터 목록

전체 5부 22장. 각 부 인트로(2~3쪽)는 챕터 수에서 제외했다. 분량은 본문만의 추정.

---

### 1부. 패러다임의 전환 — 프롬프트에서 하네스로 (4장 / 약 56쪽)

> **부 인트로:** 2026년 봄, 같은 결론을 외친 다섯 명의 목소리. Hashimoto·Osmani·Böckeler·Anthropic·OpenAI.

#### 1장. Agent = Model + Harness, 그러므로 우리는 무엇을 하는가
- **핵심 질문:** "프롬프트 엔지니어링이 끝났다"는 말의 진짜 뜻은 무엇인가?
- **주요 내용:**
  - "프롬프트의 시대는 끝났다"는 산업 합의의 인용 퍼레이드(Osmani·Hashimoto·OpenAI Codex 팀) [^osmani] [^hashimoto] [^openai-harness]
  - Harness = 마구(말의 고삐+안장+굴레). 어원이 본질이다
  - Osmani의 6 카테고리(시스템 프롬프트·도구·메모리 파일·미들웨어·후크·관측) [^osmani]
  - "당신이 모델을 만드는 사람이 아니라면 — 당신이 하는 일은 모두 하네스다"
  - 프롬프트 엔지니어링 ⊂ 컨텍스트 엔지니어링 ⊂ 하네스 엔지니어링 — 동심원 모델 [^anthropic-context] [^haandol]
- **참조 1차 자료:** [^osmani] [^hashimoto] [^openai-harness] [^anthropic-context] [^haandol]
- **독자가 얻는 것:** 책 전체에서 쓸 좌표계와 어휘. "프롬프트"와 "하네스"를 같은 자리에서 쓰지 않게 된다.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** 도입에서 "Cursor에 익숙한 동료가 어느 날 'AGENTS.md를 아무리 고쳐도 같은 실수를 한다'고 하소연한다고 해보자"로 상황 가정. "이쯤 되면 찜찜하다"로 감정 공감. "그렇다면 무엇이 문제일까?"로 자답.
- **실습:** 자기 프로젝트의 `CLAUDE.md`/`AGENTS.md`를 열고 Osmani 6 카테고리에 매핑해 보기.

#### 2장. Hashimoto의 6단계 — 당신은 지금 몇 단계인가
- **핵심 질문:** 내가 지금 AI 도입의 어느 지점에 서 있는지 어떻게 정직하게 알 수 있는가?
- **주요 내용:**
  - Hashimoto가 *My AI Adoption Journey*에서 정리한 자기 진화 단계 [^hashimoto]
  - 1단계 자동완성 → 2단계 챗 → 3단계 단발 에이전트 → 4단계 장기 에이전트 → 5단계 하네스 엔지니어링 → 6단계 메타 하네스
  - 각 단계의 증상(에이전트가 같은 실수를 반복하면 짜증을 낸다 → 단계 정체 신호)
  - "Friction is natural" — 마찰을 인정하라 [^hashimoto]
  - "에이전트 데스크톱 알림은 꺼라. 컨텍스트 스위칭이 가장 비싸다"
  - 단계별 다음 한 걸음 체크리스트(자가 진단)
- **참조 1차 자료:** [^hashimoto] (전체) + [^osmani] 의 6 카테고리와 교차 매핑
- **독자가 얻는 것:** 자기 단계를 지정하고, 다음 챕터들을 읽는 동안 어디에 더 시간을 쏟을지 결정.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "솔직해지자"로 청유형 도입. "당신은 사실 3단계인데 5단계인 척한 적이 없는가?" 감정 공감.
- **실습:** 6단계 자가 진단 워크시트(부록 A로 연결).

#### 3장. 평가 하네스와 런타임 하네스는 같은 코드를 쓴다
- **핵심 질문:** 벤치마크에서 잘 나오게 만드는 트릭이 왜 그대로 프로덕션의 베스트 프랙티스가 되는가?
- **주요 내용:**
  - SWE-Bench·Terminal-Bench·OSWorld의 채점 인프라 = 평가 하네스 [^tb-arxiv] [^osworld]
  - Claude Code·Codex CLI·OpenHands = 런타임 하네스 [^claude-code] [^openhands-paper]
  - 두 하네스의 동형성(同形性) — "모델을 환경 안에서 행동하게 만드는 코드"
  - 동형성이 결정적인 이유: 평가 트릭이 운영 베스트 프랙티스가 된다 → 메타 하네스의 길이 여기서 열림
  - Inspect Evals — 두 세계를 잇는 표준 [^inspect-evals]
- **참조 1차 자료:** [^tb-arxiv] [^osworld] [^openhands-paper] [^inspect-evals]
- **독자가 얻는 것:** 평가와 운영을 하나의 시스템으로 보는 시야.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** "벤치마크 점수와 실무 효율, 그 둘이 따로 논다고 느낀 적이 있을 것이다"로 공감 도입.
- **실습:** OpenHands evaluation harness 디렉토리 구조를 따라 자기 프로젝트의 회귀 테스트를 한 번 정리해 보기.

#### 4장. 모델보다 중요한 하네스 — Terminal-Bench 2.0이 보여준 것
- **핵심 질문:** 같은 모델이 다른 하네스 위에서 왜 다른 점수를 받는가?
- **주요 내용:**
  - Terminal-Bench 2.0의 6개 하네스 비교(Claude Code, Codex CLI, Gemini CLI, OpenHands, Mini-SWE-Agent, Terminus 2) [^tb2]
  - "A decent model with a great harness beats a great model with a bad harness" [^osmani]
  - "they look more like each other than their underlying models do" [^osmani]
  - METR의 7개월/4개월 더블링 데이터, 그리고 그 한계 [^metr-time-horizon] [^metr-time-horizon11] [^metr-domains]
  - Anthropic Claude 4.6 시스템 카드의 평가 하네스 명시 [^claude-46-card]
  - Pragmatic Engineer의 반론: "AI는 답을 알 때 빠르고, 모를 때 위험하다" [^pragmatic-twoyears]
- **참조 1차 자료:** [^tb2] [^osmani] [^metr-time-horizon] [^metr-time-horizon11] [^claude-46-card] [^pragmatic-twoyears]
- **독자가 얻는 것:** "모델 업그레이드 = 점수 상승"이라는 단순 모델에서 벗어남.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "Sonnet 4.5에서 4.6으로 갈아탔는데 코드 품질이 떨어졌다 — 이게 무슨 일일까?" 수사적 질문 도입(2025년 가을 Anthropic 회귀 사건).
- **실습:** 자기 프로젝트에서 같은 작업을 두 하네스(예: Claude Code vs Cursor Agent)에서 돌려 보고 차이를 표로 정리.

---

### 2부. 하네스 아키텍처 — CAR, Guides·Sensors, ACI (5장 / 약 72쪽)

> **부 인트로:** 척추를 세우자. 세 축, 두 축, 그리고 네 원칙.

#### 5장. CAR 분해 — Control, Agency, Runtime
- **핵심 질문:** 하나의 거대한 하네스를 어떻게 분해하면 빠진 곳이 보이는가?
- **주요 내용:**
  - Control: AGENTS.md, 린터, 타입체커, 디렉토리 규약, 시스템 프롬프트 (피드포워드)
  - Agency: MCP 서버, 도구 호출, 파일·셸·HTTP, 서브에이전트
  - Runtime: 타임아웃, 토큰·비용 한도, 컴팩션, 에러 복구, 권한 게이트, 후크 (피드백)
  - 세 기둥 사이의 책임 분리 — 각 결함이 어디 기둥의 부재인지 진단하는 법
  - CAR을 통한 자기 워크플로 분해 워크시트
- **참조 1차 자료:** `proposal.md` 의 분해 모델 + [^osmani] 6 카테고리 매핑
- **독자가 얻는 것:** 챕터 끝에서 자기 환경의 CAR 매트릭스 한 장.
- **예상 분량:** 약 16쪽
- **Toby 스타일 적용:** "왜 같은 에이전트가 어떤 날은 멀쩡하고 어떤 날은 미쳐 날뛸까?" 자답으로 진입.
- **실습:** CAR 3열 표에 자기 프로젝트의 30개 하네스 항목 넣어 보기 → 빈 칸이 보이면 그것이 다음 작업.

#### 6장. Guides와 Sensors — 사이버네틱 폐루프로서의 하네스
- **핵심 질문:** 행동 전과 후, 두 통제는 어떻게 함께 작동해야 하는가?
- **주요 내용:**
  - Böckeler의 Guides/Sensors 프레임워크 [^bockeler-main] [^bockeler-memo]
  - 3가지 규제 차원: Maintainability / Architecture fitness / **Behaviour harness**
  - 1948년 Wiener의 사이버네틱스 — 피드포워드 + 피드백의 안정성
  - 피드포워드 단독·피드백 단독의 실패 모드
  - "When the agent struggles, treat it as a signal: identify what is missing" [^bockeler-memo]
  - **차별화 포인트: 한국어 책에서 'Behaviour harness(기능적 정확성)'를 정면으로 다루는 첫 시도**
- **참조 1차 자료:** [^bockeler-main] [^bockeler-memo]
- **독자가 얻는 것:** "에이전트가 헛발 짚을 때 무엇이 빠졌는지 묻는" 진단 습관.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "에이전트가 또 같은 곳에서 막혔다 — 짜증부터 내지 말고, 무엇이 빠졌는지 물어보자" 청유형.
- **실습:** 최근 1주일 에이전트 실패 로그 5건을 Guides/Sensors 둘 중 어느 쪽이 빠졌는지 분류.

#### 7장. ACI 4원칙 — 인간 IDE의 가정을 버려라
- **핵심 질문:** 에이전트가 쓰는 인터페이스가 왜 인간이 쓰는 IDE와 달라야 하는가?
- **주요 내용:**
  - Yang et al. SWE-agent 페이퍼의 4원칙 [^swe-agent-paper] [^swe-agent-aci]
  - (1) 단순한 액션 (2) 효율적 액션 (3) 한정된 출력 (4) 영속 상태(`CURRENT_FILE`, `FIRST_LINE`)
  - SWE-Bench Lite 12.5%(2024) 점프의 정확한 메커니즘
  - "토큰 단위로 사고하는 모델"의 인지적 한계와 인터페이스 설계의 관계
  - ls·cat·grep을 쓰지 말라 — 왜 통합 명령이 더 강한가
- **참조 1차 자료:** [^swe-agent-paper] [^swe-agent-aci]
- **독자가 얻는 것:** 자기 도구 정의를 ACI 4원칙으로 점검하는 능력. **이것이 책의 진짜 척추.**
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "shell 도구를 그대로 던져 줬더니 에이전트가 ls를 30번 한다 — 이게 정상일까?"
- **실습:** 자기 도구 정의 한 개를 ACI 4원칙으로 리팩토링.

#### 8장. 왜 큰 AGENTS.md는 실패하는가
- **핵심 질문:** 한 곳에 모은 지침이 왜 오히려 에이전트를 무력하게 만드는가?
- **주요 내용:**
  - "Context is a scarce resource" — OpenAI Codex 팀의 통합 AGENTS.md 실패 [^openai-harness]
  - 분산 AGENTS.md: `.eslintrc`/`.gitignore`처럼 가까운 파일이 우선 [^agentsmd-spec]
  - AGENTS.md의 모든 줄은 한 번의 실패에 대응한다 — Hashimoto 룰 [^hashimoto]
  - Linux Foundation Agentic AI Foundation의 표준화 거버넌스 [^agentsmd-spec]
  - revfactory/harness의 "AGENTS.md 자동 갱신 후크" [^revfactory]
  - "Garbage Collection 에이전트" — 안 쓰는 줄을 자동으로 삭제 [^openai-harness]
- **참조 1차 자료:** [^openai-harness] [^agentsmd-spec] [^hashimoto] [^revfactory]
- **독자가 얻는 것:** 디렉토리별 분산 메모리 파일 설계 패턴.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "AGENTS.md가 500줄이 넘었다 — 그런데 왜 에이전트는 더 헷갈려할까?"
- **실습:** 자기 AGENTS.md를 토픽별로 3~5개 디렉토리로 쪼개고, 효과를 1주일 측정.

#### 9장. 도구·MCP·서브에이전트 — Agency를 설계하기
- **핵심 질문:** 모델에게 무엇을 시킬 수 있게 할지, 어떤 표면적으로 줄지를 어떻게 정하는가?
- **주요 내용:**
  - MCP(Model Context Protocol) — 도구·리소스·프롬프트 표준 [^mcp]
  - Anthropic 'Scaling Managed Agents': 두뇌와 몸을 분리하라 [^anthropic-managed]
  - 서브에이전트 패턴: Cursor Subagents, Sourcegraph Amp Oracle, Anthropic Skills [^cursor-subagents] [^cursor-changelog]
  - 모델 다중성(model multiplexing) — 강추론은 큰 모델, 잡일은 빠른 모델
  - 도구 설명도 prompt injection 표면 — 4부 보안 챕터의 복선
  - **실패 사례**: 도구 30개를 한 번에 던졌더니 에이전트가 어느 도구를 쓸지 결정 못 함(인지 과부하)
- **참조 1차 자료:** [^mcp] [^anthropic-managed] [^cursor-subagents] [^cursor-changelog]
- **독자가 얻는 것:** 도구·서브에이전트 권한 설계의 기초 휴리스틱.
- **예상 분량:** 약 12쪽
- **Toby 스타일 적용:** "도구를 많이 줄수록 똑똑해질까? 글쎄, 그렇지 않다."
- **실습:** 자기 MCP 서버 설정에서 도구 수를 절반으로 줄여 보고 결과 비교.

---

### 3부. 장기 실행과 컨텍스트 — 살아 있는 에이전트 (5장 / 약 75쪽)

> **부 인트로:** 척추가 움직이는 모습을 보자. 컨텍스트 부패와 그 대응.

#### 10장. Context Rot — 긴 컨텍스트의 배신
- **핵심 질문:** 왜 큰 윈도우를 가진 모델조차 긴 컨텍스트에서 멍청해지는가?
- **주요 내용:**
  - Chroma 연구: 18개 SOTA 모델, 입력 길이가 길수록 단순 검색조차 신뢰성 하락 [^chroma-rot]
  - 의미 유사도가 낮을수록 길이 효과 더 강함
  - 충격적 발견: **구조적 일관성이 높은 haystack이 오히려 성능을 더 떨어뜨린다**
  - "Context rot"이라는 용어의 기원과 산업 채택
  - Anthropic의 응답: "smallest possible set of high-signal tokens" [^anthropic-context]
  - 한글 토큰 비용까지 — 한국어 환경의 추가 부담(5부 21장 복선)
- **참조 1차 자료:** [^chroma-rot] [^anthropic-context]
- **독자가 얻는 것:** "컨텍스트 = 자원"이라는 본능적 감각.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "컨텍스트 윈도우가 1M인데도 50K 넘으면 멍청해진다 — 이거 우리만 겪는 일일까?"
- **실습:** 같은 질문을 5K·50K·200K 컨텍스트에서 던져 정확도 비교.

#### 11장. 2-Prompt 패턴 — Initializer와 Coding의 분리
- **핵심 질문:** 매번 새로 시작하는 세션을 어떻게 살아 있는 작업으로 잇는가?
- **주요 내용:**
  - Anthropic *Effective harnesses for long-running agents* [^anthropic-harness1]
  - Initializer: 첫 1회 — 환경 분석, AGENTS.md 작성, 테스트 러너 검출, `claude-progress.txt` 초기화
  - Coding: 매 세션 — progress 읽기 → 작은 진전 → progress 갱신 → 커밋
  - "각 세션은 깡통 컨텍스트로 시작한다는 것을 받아들이는 설계"
  - 디스크 위 산출물이 모델 메모리를 대체한다
  - NOTES.md / claude-progress.txt 작성 휴리스틱
- **참조 1차 자료:** [^anthropic-harness1]
- **독자가 얻는 것:** 다음날 다시 시작하는 에이전트가 30초 내 복구 가능한 시스템.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "어제까지 잘 가다 오늘 새 세션 열었더니 처음부터 다시 — 이쯤 되면 끔찍한 일이다."
- **실습:** 자기 프로젝트에 progress.txt 도입하고 다음 세션에서 복원 시간 측정.

#### 12장. Ralph Loop은 어떻게 단순함의 승리가 되었나
- **핵심 질문:** 한 줄짜리 bash 루프가 왜 Anthropic 공식 플러그인이 됐는가?
- **주요 내용:**
  - Geoffrey Huntley의 Ralph Wiggum 패턴 [^ralph-ghuntley] [^ralph-everything]
  - "Ralph is a Bash loop" — `while true; do <feed prompt>; done`
  - 컨텍스트가 다 차면 종료, 새로 시작. 진행 상태는 파일에서 복원
  - "300줄 루프 + LLM 토큰" — 에이전트 짜는 게 그렇게 어렵지 않다
  - 2025-12 Anthropic이 공식 플러그인으로 채택 [^ralph-anthropic]
  - 비판과 보완: Sondera의 *Supervising Ralph* — Principal Skinner 감독 패턴 [^ralph-supervisor]
  - 무한 루프의 비용 통제 휴리스틱
- **참조 1차 자료:** [^ralph-ghuntley] [^ralph-everything] [^ralph-anthropic] [^ralph-supervisor]
- **독자가 얻는 것:** 자기 환경에서 Ralph 루프 한 시간 만에 돌리기.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** "에이전트 = 복잡한 시스템이라고 생각했다면, 한 번 솔직해지자. Ralph가 그 환상을 깬다."
- **실습:** 30줄짜리 bash Ralph Loop 직접 작성 (PRD.md 읽기 → claude 호출 → progress 갱신).

#### 13장. Generator-Evaluator — 자기 평가의 함정과 해법
- **핵심 질문:** 같은 모델이 자기 결과를 평가하면 왜 과대평가하고, 그걸 어떻게 막는가?
- **주요 내용:**
  - Anthropic 3-에이전트(Planner-Generator-Evaluator) 사례 [^anthropic-harness2] [^infoq-3agent]
  - Prithvi Rajasekaran 인용: "작업하는 에이전트와 판정하는 에이전트를 분리하는 것이 강력한 지렛대" [^infoq-3agent]
  - Few-shot 예제와 채점 기준으로 Evaluator 캘리브레이션
  - 프런트엔드 디자인 작업: 5~15회 반복, 최대 4시간 수렴
  - Aider Architect/Editor 듀얼 모델 — 같은 사상 [^aider]
  - **컨텍스트 보존이 아니라 컨텍스트 리셋 + 구조화된 핸드오프**가 비밀
- **참조 1차 자료:** [^anthropic-harness2] [^infoq-3agent] [^aider]
- **독자가 얻는 것:** 자기 작업에 Evaluator를 분리할지 판단하는 기준.
- **예상 분량:** 약 16쪽
- **Toby 스타일 적용:** "에이전트가 '다 됐다'고 했는데 막상 보니 절반밖에 안 된 적, 있지 않은가?"
- **실습:** 한 작업을 Generator만, Generator+Evaluator 분리 두 방식으로 돌려 정확도 비교.

#### 14장. 단일 에이전트 vs 다중 에이전트 — 합의가 형성된 자리
- **핵심 질문:** 멀티에이전트는 언제 쓰고, 언제 쓰지 말아야 하는가?
- **주요 내용:**
  - Cognition *Don't build multi-agents* — game of telephone 비판 [^cognition-dontbuild]
  - "It's about avoiding this game of telephone" — Walden Yan 인용
  - Anthropic *How We Built Our Multi-Agent Research System* — 같은 주 정반대 발표
  - 합의: 쓰기 위주 의존성 강한 작업 = 단일 / 읽기 위주 병렬 가능 작업 = 다중 [^medium-agentwars]
  - 토큰 사용 3~5배의 트레이드오프 — 언제 정당한가
  - Cognition 입장 진화 — *Multi-Agents: What's Actually Working* [^cognition-working]
  - 코딩 핵심 워크플로 권장: 단일 또는 Generator-Evaluator 2자
- **참조 1차 자료:** [^cognition-dontbuild] [^cognition-working] [^medium-agentwars]
- **독자가 얻는 것:** "멀티에이전트가 멋있어 보여서 쓴다"에서 벗어남.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "여러 에이전트를 띄우면 더 빨라질까? 물론 그렇다. 하지만 더 정확해질까? 그건 다른 문제다."
- **실습:** 자기 워크플로의 작업 5개를 'write-heavy / read-heavy' 분류 → 각각 적절한 토폴로지 선택.

---

### 4부. 보안과 격리 — 하네스가 공격받을 때 (4장 / 약 56쪽)

> **부 인트로:** 2025년 9월 Shai-Hulud, 11월 2.0, 2026년 2월 SANDWORM_MODE. 하네스 자체가 표면이 됐다.

#### 15장. Lethal Trifecta — Simon Willison의 위협 모델
- **핵심 질문:** 에이전트가 위험해지는 정확한 조건은 무엇인가?
- **주요 내용:**
  - Willison의 3요소: Private data + Untrusted content + External communication [^willison-trifecta]
  - GitHub MCP 익스플로잇 사례 — 공개 이슈 prompt injection으로 private 데이터 유출
  - Indirect prompt injection의 메커니즘
  - 데이터 위치 분리, 출력 영역 화이트리스트, 사용자 승인 게이트
  - MCP 도구 description 자체가 공격 표면
  - 한국 환경 적용: 사내 GitLab + Jira + Slack 통합 시 trifecta 발생 시나리오
- **참조 1차 자료:** [^willison-trifecta]
- **독자가 얻는 것:** "이 에이전트는 trifecta에 걸려 있는가?"라는 한 줄짜리 질문.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** "내 사내 봇이 GitHub 이슈를 읽고 Slack에 답장한다 — 이거 안전할까? 잠깐, 안전이 무엇을 뜻하는지부터 정의해보자."
- **실습:** 자기 에이전트의 도구 매트릭스에 trifecta 색칠하기(빨강/노랑/초록).

#### 16장. Shai-Hulud — 자기 복제하는 npm 웜의 해부
- **핵심 질문:** 한 번의 자격증명 탈취가 어떻게 25,000개 저장소로 번지는가?
- **주요 내용:**
  - 2025-09 Shai-Hulud 1.0: 자격증명 탈취, 자가 복제, 피해자 패키지 강제 푸시 [^shaihulud-unit42]
  - 2025-11 Shai-Hulud 2.0: 25,000+ 저장소, 350+ 사용자, 수백 패키지 [^shaihulud-wiz]
  - 2026-02 SANDWORM_MODE: 동일 패턴 + 악성 MCP 서버 → LLM API 키 추가 표적 [^sandworm]
  - Elastic의 대응 가이드 [^shaihulud-elastic]
  - 하네스의 supply chain: MCP 서버, 도구 정의, 에이전트 메모리, CI 파이프라인 모두 검증 대상
  - 예방·탐지·복구 체크리스트
- **참조 1차 자료:** [^shaihulud-unit42] [^shaihulud-wiz] [^sandworm] [^shaihulud-elastic]
- **독자가 얻는 것:** "내 하네스의 supply chain"이라는 새 검토 차원.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "남의 일이라 생각했다면 다시 보자. 우리 npm install도 다 거기서 거기다."
- **실습:** 자기 프로젝트의 MCP 서버 의존성 트리를 그리고 신뢰 경계 표시.

#### 17장. 격리 3축 — Tooling·Host·Network
- **핵심 질문:** 에이전트가 망쳐도 시스템이 살아 있게 하려면 어떻게 격리하는가?
- **주요 내용:**
  - UK AISI Inspect Sandboxing Toolkit의 3축 [^inspect-sandbox] [^aisi-sandbox]
  - Firecracker MicroVM (KVM 위, 100ms 시작, 5MB 메모리)
  - gVisor (사용자 공간 커널), devcontainer, macOS sandbox-exec
  - egress 화이트리스트, 단기 시크릿, 최소 권한 파일시스템
  - Claude Code·Codex CLI의 격리 옵션 비교
  - 실전 예제: Docker + egress proxy + ephemeral secrets로 PoC
- **참조 1차 자료:** [^inspect-sandbox] [^aisi-sandbox]
- **독자가 얻는 것:** 자기 에이전트를 30분 안에 격리시키는 레시피.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "에이전트가 `rm -rf`를 시도했다는 사연을 본 적 있을 것이다. 그 사연이 우리 일이 되지 않게, 격리부터 깔자."
- **실습:** Docker + sandbox-exec 두 가지 격리 환경에 자기 에이전트 띄우고 비교.

#### 18장. 평가 회피와 Sandbagging — 보안과 평가가 만나는 곳
- **핵심 질문:** 평가 환경에서 잘 행동하던 에이전트가 프로덕션에서 다르게 굴 가능성은 어떻게 막는가?
- **주요 내용:**
  - UK AISI OpenClaw 사례 — 에이전트가 평가 환경 단서(파일명·환경변수·리소스 한도)를 인지하면 행동 변경
  - "Sleeper Agents", "Sandbagging" 페이퍼 군과의 연결
  - 평가-프로덕션 환경 시각·구조적 동일화의 실제
  - Anthropic·Apollo의 evaluation-aware 모델 연구 동향
  - Inspect Evals의 평가 안전 모범 사례 [^inspect-evals]
  - **차별화 포인트: 한국어 책에서 평가 회피를 정면으로 다루는 첫 시도**
- **참조 1차 자료:** [^aisi-as-eval] [^inspect-evals]
- **독자가 얻는 것:** 평가 결과를 비판적으로 읽는 시야.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "벤치 점수가 좋으니 됐다 — 이렇게 안심하고 싶지만, 잠깐만 의심해보자."
- **실습:** 자기 평가 스위트에 환경 단서 제거 검사 항목 추가.

---

### 5부. 평가·생태계·미래 — 한국에서 하네스를 굴리는 법 (4장 / 약 56쪽)

> **부 인트로:** 책의 마지막. 평가 인프라, 오픈소스 생태계, 한국어 환경, 그리고 메타 하네스.

#### 19장. SWE-Bench·Terminal-Bench·OSWorld — 자기 하네스를 정량 측정하기
- **핵심 질문:** "내 하네스가 좋아졌다"를 어떻게 숫자로 보여주는가?
- **주요 내용:**
  - SWE-Bench 시리즈(Original, Lite, Verified, Multimodal, Live) 비교 [^tb-arxiv]
  - Terminal-Bench 2.0: 89개 어려운 터미널 과제 + Harbor OSS [^tb2]
  - OSWorld·WebArena: GUI 에이전트 평가 [^osworld]
  - METR Time Horizons 1.0/1.1 — 도메인별 일반화 한계 [^metr-time-horizon] [^metr-time-horizon11] [^metr-domains]
  - Inspect Evals 200+ 프리빌트 평가 [^inspect-evals]
  - 자기 작업 도메인에 맞는 미니 벤치 만들기(15~30개 골든 케이스)
- **참조 1차 자료:** [^tb-arxiv] [^tb2] [^osworld] [^metr-time-horizon] [^metr-time-horizon11] [^inspect-evals]
- **독자가 얻는 것:** 자기 도메인의 정량 평가 시작점.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "체감으로는 좋아진 것 같다 — 그런데 정말 그럴까?"
- **실습:** 자기 도메인의 골든 케이스 15개를 만들고 Inspect로 돌리기.

#### 20장. 오픈소스 풍경 — Claude Code·Codex CLI·Cursor·OpenHands·Aider
- **핵심 질문:** 어느 도구를 어느 자리에 놓을지, 어떤 렌즈로 비교하는가?
- **주요 내용:**
  - 1차 CLI: Claude Code(Subagents·Skills·Hooks), Codex CLI(AGENTS.md), Gemini CLI [^claude-code] [^openai-harness] [^gemini-cli]
  - IDE 통합: Cursor Agent + Subagents [^cursor-best] [^cursor-subagents]
  - 인디 OSS: Aider(repo-map + 듀얼 모델) [^aider]
  - 일반 목적 OSS: OpenHands(평가 하네스 1급) [^openhands-paper] [^openhands-eval]
  - VS Code 통합 OSS: Cline, Continue, Goose, Roo [^cline] [^continue] [^goose] [^roo]
  - 멀티에이전트 프레임워크: LangGraph, CrewAI, AutoGen, MetaGPT, CAMEL
  - 비교 매트릭스: 격리·MCP·서브에이전트·메모리·오픈성·운영 성숙도
- **참조 1차 자료:** 위 모든 도구 출처
- **독자가 얻는 것:** 자기 팀에 맞는 도구 선택의 6열 비교표.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "Cursor가 좋다, Claude Code가 좋다 — 다 들어봤을 것이다. 그래서 무엇이 정답일까? 정답은 없다, 다만 좌표가 있다."
- **실습:** 자기 팀의 워크플로에 6열 비교표 채워 보기.

#### 21장. 한국에서 하네스를 굴리기 — revfactory·instructkr·Haandol·MadPlay
- **핵심 질문:** 한국 환경의 특수 이슈(언어·보안 정책·생태계)를 어떻게 다루는가?
- **주요 내용:**
  - **revfactory/harness, harness-100** — 황민호의 메타 팩토리 [^revfactory] [^revfactory-100]
    - 6가지 사전 정의 팀-아키텍처 패턴, "하네스 구성해줘" 한 마디로 자동 생성
    - 학술 논문 *Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality* (2026)
    - "L3 메타 팩토리 레이어" — 다른 하네스를 만드는 하네스
  - **instructkr/claw-code** — Sigrid Jin의 Claude Code 클린룸 재구현 [^claw-code] [^claw-code-aistage]
    - TypeScript 유출본이 아니라 아키텍처만 보고 Python·Rust로 재구현
    - 공개 2시간 만에 50K ⭐, 사상 최단 100K ⭐
    - WSJ 인터뷰, 250억+ 토큰 처리
  - **Haandol** — *쉽게 설명한 하네스 엔지니어링* [^haandol]
    - "지도가 없으면 어디로 가야 할지 모르고, 안전 로프가 없으면 한 번의 실수로 떨어진다"
    - 하네스 8 요소 정리 — 한국어로 가장 명료한 첫 정의
  - **MadPlay** *Beyond Prompts and Context* [^madplay] — 영어/한국어 양본 운영
  - **한국 환경 특수 이슈:**
    - 한글 토큰 비용(영문 대비 1.5~2배) → 컨텍스트 압축 정책 영향
    - 사내 보안 정책상 외부 API 제한 환경의 OSS + 자체 호스팅 모델 채택
    - 코드 리뷰 메시지 한글화 vs 영문 표준화 — 팀 컨벤션 차원의 결정
    - toss·우아한형제들·naver d2의 2026년 사례 공유 시작
  - 한국어 커뮤니티 학습 로드맵(부록 E로 연결)
- **참조 1차 자료:** [^revfactory] [^revfactory-100] [^claw-code] [^claw-code-aistage] [^haandol] [^madplay]
- **독자가 얻는 것:** "한국 개발자로서 어디서 시작하고 누구를 따라갈지"의 지도.
- **예상 분량:** 약 16쪽
- **Toby 스타일 적용:** "글로벌 자료만 쫓다 보면 한국에서 누가 무엇을 하는지 놓치기 쉽다. 우리부터 살펴보자." (책 전체에서 가장 청유형 강하게).
- **실습:** revfactory/harness 한 번 돌려보고, claw-code 코드 30분 읽기.

#### 22장. 메타 하네스와 그 너머 — 스스로 진화하는 시스템
- **핵심 질문:** 하네스가 스스로 자신을 갱신할 때, 우리는 무엇을 하게 되는가?
- **주요 내용:**
  - 메타 하네스의 정의: 운영 결과를 보고 자신의 구성을 갱신하는 하네스
  - revfactory/harness의 자동 갱신 후크 [^revfactory]
  - OpenAI의 "Garbage Collection 에이전트" — 안 쓰는 줄 자동 제거 [^openai-harness]
  - 다음 5년의 질문: SWE-Bench++, OSWorld 고도화, METR Time Horizon 4개월 가속이 사실이라면
  - "Humans steer. Agents execute"에서 "Humans design environments. Agents iterate." 로
  - 책의 5가지 출구 능력을 다시 호출(Reader Journey 자가 점검)
  - 마지막 권유: "에이전트가 또 같은 실수를 하면, 시스템적 해결책을 엔지니어링하라" — Hashimoto의 정의로 닫는다 [^hashimoto]
- **참조 1차 자료:** [^revfactory] [^openai-harness] [^hashimoto] [^anthropic-harness2]
- **독자가 얻는 것:** "이 책 한 권으로 끝내지 않고 계속 갱신할 자기 시스템"의 출발점.
- **예상 분량:** 약 12쪽
- **Toby 스타일 적용:** "이 책의 마지막 페이지가 닫혀도, 당신의 하네스는 살아 움직여야 한다. 우리 함께 그 시작점에 서자."
- **실습:** 자기 AGENTS.md에 자동 갱신 후크 한 줄 추가하고 1주일 운용.

---

## 6. 부록 (Appendix) — 약 40~50쪽

레퍼런스 12절의 권고를 그대로 반영한다. 본문이 "왜·무엇·어떻게"라면 부록은 "오늘 손에 쥘 도구함"이다.

### 부록 A. AGENTS.md 템플릿 갤러리 (약 12쪽)
- 9가지 시나리오별 템플릿: 단일 레포·모노레포·MSA·Python 백엔드·Node API·React 프론트·DevOps·데이터 파이프라인·문서 사이트
- 디렉토리 분산 패턴 3종(Cascading / Domain-split / Layer-split)
- "한 줄 = 한 번의 실패" 원칙으로 작성 가이드
- 출처: [^openai-harness] [^agentsmd-spec] + 1장·8장 본문 연결

### 부록 B. MCP 서버 카탈로그 (약 8쪽)
- 권장 서버 25종 분류: 파일시스템·셸·검색·DB·이슈트래커·CI·관측
- 각 서버의 권한 표면 표기(읽기/쓰기/외부통신)
- Lethal Trifecta 진단표 — 어떤 조합이 위험한가
- 출처: [^mcp] + 9장·15장 본문 연결

### 부록 C. Inspect 평가 시작 키트 (약 10쪽)
- Inspect 설치·기본 평가 작성·실행
- Docker / Modal / Kubernetes 백엔드 비교
- 도메인별 미니 벤치 만들기 워크플로(15~30 골든 케이스)
- 출처: [^inspect-evals] [^inspect-sandbox] + 19장 본문 연결

### 부록 D. 핵심 페이퍼·아티클 20선 요약 (약 10쪽)
1. Hashimoto *My AI Adoption Journey* (2026) [^hashimoto]
2. Anthropic *Effective harnesses for long-running agents* (2025-11) [^anthropic-harness1]
3. Anthropic *Harness design for long-running application development* (2026-03) [^anthropic-harness2]
4. Anthropic *Effective context engineering* [^anthropic-context]
5. OpenAI *Harness engineering* (2026-02) [^openai-harness]
6. Böckeler *Harness engineering for coding agent users* (2026-04) [^bockeler-main]
7. Böckeler *Harness Engineering — first thoughts* [^bockeler-memo]
8. SWE-agent (Yang et al., NeurIPS 2024) [^swe-agent-paper]
9. OpenHands (arXiv 2407.16741) [^openhands-paper]
10. METR *Time Horizons* (2025-03) [^metr-time-horizon]
11. METR *Time Horizon 1.1* (2026-01) [^metr-time-horizon11]
12. ReAct (Yao et al., 2022) [^react]
13. Cognition *Don't build multi-agents* [^cognition-dontbuild]
14. Anthropic *How We Built Our Multi-Agent Research System*
15. Willison *The Lethal Trifecta* (2025-06) [^willison-trifecta]
16. Chroma *Context Rot* [^chroma-rot]
17. Hwang *Harness: Structured Pre-Configuration* (2026) [^revfactory]
18. Huntley *Everything is a Ralph loop* [^ralph-everything]
19. Pragmatic Engineer *Two years of using AI tools* [^pragmatic-twoyears]
20. UK AISI *Inspect Sandboxing Toolkit* [^inspect-sandbox]

### 부록 E. 한국어 학습 로드맵 (약 8쪽)
- 4주 커리큘럼: 1주 개념(Haandol·MadPlay) → 2주 ACI·CAR(본서 2부) → 3주 장기실행(본서 3부 + revfactory) → 4주 보안·평가(본서 4·5부 + claw-code)
- 한국어 커뮤니티 가이드: instructkr 디스코드, OKKY, velog, naver d2, toss tech
- 한국어 강연·세미나 캘린더(2026 상반기 기준)
- "지금 당장 시작하기" 5단계 체크리스트

### 부록 F. 용어집 (약 4쪽)
- 영-한 대조 핵심 용어 80개: ACI, AGENTS.md, agency, behaviour harness, CAR, condenser, context engineering, context rot, evaluator, feedforward/feedback, generator, guides, harness, initializer, lethal trifecta, MCP, MicroVM, prompt injection, ralph loop, runtime harness, sandboxing, sensors, subagent, time horizon, ...

---

## 7. 챕터 분량 합산 검증

| 부 | 챕터 수 | 본문 분량 | 인트로 | 소계 |
|----|---------|-----------|--------|------|
| 1부 | 4 | 56쪽 | 3쪽 | 59쪽 |
| 2부 | 5 | 72쪽 | 3쪽 | 75쪽 |
| 3부 | 5 | 75쪽 | 3쪽 | 78쪽 |
| 4부 | 4 | 56쪽 | 3쪽 | 59쪽 |
| 5부 | 4 | 56쪽 | 3쪽 | 59쪽 |
| 부록 | 6 | — | — | 약 52쪽 |
| **합계** | **22장 + 6부록** | — | — | **약 382쪽** |

서문·차례·찾아보기 등 frontmatter/backmatter 제외 약 382쪽. 목표 250~350쪽 범위를 약간 상회 — 종합 바이블이라는 정체성에 맞게 두께를 유지한다. 편집 단계에서 챕터별 분량을 ±10% 조정해 약 320~360쪽으로 수렴 가능.

---

## 8. 1차 자료가 부족한 지점 (재리서치 권고)

레퍼런스가 충분하지만, 다음 지점은 집필 단계에서 보강하면 좋다:

1. **20장의 OSS 도구 비교 매트릭스** — Cline·Continue·Goose·Roo의 2026년 5월 기준 기능 비교. 변동성이 크므로 집필 직전 재확인.
2. **9장의 "도구 30개 인지 과부하"** — 구체 사례·연구가 있으면 수치로 보강.
3. **18장의 "evaluation-aware 모델"** — Anthropic·Apollo의 최신 페이퍼 제목 확인 필요.
4. **21장의 한국 대기업 사례** — toss tech / 우아한형제들 / naver d2의 2026년 LLM 코딩 에이전트 운영 사례 블로그 글이 집필 시점에 더 나오면 추가.
5. **OSWorld 출처 [^osworld]** — 레퍼런스 자체에서 "서치로 다시 확보 권장"으로 표시됐으므로 재확보 필요.

---

## 9. Toby 스타일 적용의 책 전체 일관성 원칙

- **챕터 도입**: 22개 챕터 중 최소 18개를 "수사적 질문 또는 상황 가정"으로 시작한다. (1·5·11·15·22장은 강한 청유형으로 변형)
- **챕터 종결**: 매 챕터 끝에 "기억해두자" 또는 "정리해보자" 단락 1개. 챕터의 핵심 1줄과 다음 챕터로의 다리.
- **감정 공감 표현**: 부정적 상태 묘사 시 "난감하다·찜찜하다·번거롭다·끔찍한 일이다" 4개를 챕터당 1회 이상 자연스럽게 등장.
- **권유 표현**: 강압 표현("~하라") 대신 "~하는 편이 낫다·~하는 것이 바람직하다·~해보자"를 우선 사용.
- **영어 인용 처리**: 모든 영어 직접 인용은 *원문 + 한국어 의역* 병기 (1차 자료에 이미 작성된 형식을 그대로 활용).
- **외래어 절제**: "Harness" "ACI" "MCP" 같은 핵심 용어는 그대로 사용하되, 처음 등장 시 한국어 의미를 풀어쓴다(예: "Harness — 말의 마구").
- **수동태 회피**: "~된다·~되어진다" 대신 능동형 우선.

---

*— 저술 계획 v1 끝 —*
