# 에이전틱 코딩과 하네스 엔지니어링 — 저술 계획 (v2)

> 산출 일자: 2026-05-02
> 입력: `proposal.md`, `01_reference.md`, `toby-book-writing-style.md`, `02_plan_v1.md`, `03_review_log.md`
> 위치: 종합 바이블 (Comprehensive Bible) — 한국어권에서 하네스 엔지니어링을 정면으로 다루는 첫 두꺼운 책
> v1 → v2 핵심 변경: 운영 층위 신설 2장 + 보안 카탈로그 1장 + 에필로그 1장 + 17장 분할 = 본문 22장 → 25장 + 23장 에필로그. 부록 6종 → 8종(+선택 2종). 약 382쪽 → 약 430쪽.

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
- **약점:** 도발이 강해 보수적 독자에게 거부감. '입문'이 책의 무게(약 430쪽 종합 바이블)와 어긋난다.

### 후보 C — 비유·시적
**『고삐를 쥔 자: AI 에이전트와 하네스 엔지니어링의 모든 것』**
- **캐릭터:** 비유 중심. 'Harness=마구(말의 고삐)'라는 어원을 표지에 살린다.
- **톤:** 개념의 시적 해석. 한국어권 기술서로는 드문 결.
- **포지셔닝:** "책 한 권 읽으니 '하네스'라는 단어의 무게가 느껴진다" 류 후기를 만든다.
- **약점:** "고삐" 비유가 부정적으로 읽힐 위험(인간이 모델을 'AI 노예'처럼 다룬다는 인상). 부제 "모든 것"이 과하다는 인상도 가능.

### 추천: **후보 A**

종합 바이블이라는 책의 정체성과 가장 잘 맞는다. 5부 25장 + 에필로그, 약 430쪽의 두께를 표지가 미리 약속한다. **단, 표지 카피로 후보 B의 메시지를 흡수하자**: "프롬프트의 시대는 끝났다. 이제 하네스를 설계하라." — 부제 위 헤드 카피로 박는다. 후보 C의 'Harness=마구' 비유는 1부 1장 도입에서 풀어낸다.

저자 표기: `Toby-AI` (프로젝트 규약).

---

## 2. 책 특성

| 항목 | 값 |
|------|-----|
| **장르** | 기술서 + 산업·사상 정리서 (이론 25% / 사례 25% / 실습·운영 30% / 한국어 생태계 10% / 보안 10%) |
| **분량** | 약 **425~445쪽** (한글 약 33만~36만 자). 본문 25장 + 에필로그 1장 + 5부 인트로 + 부록 8종. 목표 **430쪽**. |
| **난이도** | 중상 (현업 1~2단계 졸업자 대상). 기초 프롬프트·LLM 호출은 다루지 않는다. |
| **톤** | Toby 평어체 + 청유형. 수사적 질문으로 매 절 도입. 영어 1차 인용은 원문+의역 병기. |
| **개념 밀도** | 챕터당 핵심 용어 5~8개를 정확히 정의하고, 한국어/영어 병기. 용어집(부록 F)으로 흡수. |
| **실습 비중** | 모든 챕터 1개 이상 — 코드/설정 점검, 시나리오 시뮬레이션, 페어 워크, 디스커션, 인터뷰 5종으로 다양화 (§12). |
| **Toby 스타일 핵심 적용** | (1) "왜 그럴까?" → 자답 / (2) "~라고 해보자" 상황 가정 / (3) "난감하다·찜찜하다·번거롭다·끔찍한 일이다" 감정 공감 / (4) "~하는 편이 낫다" 권유 / (5) "기억해두자" 강조 — 챕터별 시그니처 감정 단어 매핑(§11) |

---

## 3. 독자 여정 (Reader Journey)

**진입 상태:** Cursor·Claude Code·Copilot·Aider 정도는 써 봤다. AGENTS.md/CLAUDE.md를 한 번 작성해 봤지만 "왜 어떤 줄은 효과 있고 어떤 줄은 무시되는지" 모른다. 에이전트가 같은 실수를 반복하면 짜증을 내며 다시 프롬프트를 고친다.

**출구 상태 — 다음 다섯 가지 능력으로 측정한다:**

1. **(설계) 자기 팀의 워크플로를 CAR(Control·Agency·Runtime) 3축과 Guides·Sensors 2축으로 분해하고, 빈자리를 짚어낼 수 있다.**
2. **(저술) 거대 단일 AGENTS.md가 아닌 디렉토리 분산 + 계층화된 메모리 파일을 설계해, 컨텍스트 예산을 의식적으로 배분할 수 있다.**
3. **(운영) 장기 실행 작업에 2-prompt(Initializer + Coding) 또는 3-에이전트(Planner-Generator-Evaluator) 패턴을 적용하고, `progress.txt`·서브에이전트로 컨텍스트 부패를 통제하며, 5축 메트릭(latency·token·cost·success·regression delta)으로 운영 회귀를 정량 탐지할 수 있다.**
4. **(보안) Lethal Trifecta·Shai-Hulud·프롬프트 인젝션 카탈로그를 자기 환경에 비춰 재현하고, MicroVM·egress 화이트리스트·MCP 권한 모델로 1차 방어선을 구성할 수 있다.**
5. **(평가·진화·전파) Inspect·Terminal-Bench·SWE-Bench 같은 평가 하네스로 자기 하네스의 성능 회귀를 정량 측정하고, 메타 하네스(스스로 갱신되는 AGENTS.md) 패턴을 시도하며, 자기 팀에 1주차·2주차·1개월 온보딩으로 도입할 수 있다.**

이 5가지가 책 전체의 학습 목표다. 각 부가 한 능력씩 책임진다(5부는 4·5번을 한국어 환경 적응·팀 도입과 묶어 마무리한다).

---

## 4. 내러티브 아크 (왜 이 순서인가)

이 책은 **"산업의 합의가 어떻게 생겼는지(왜) → 그 합의를 어떻게 분해하는지(무엇) → 어떻게 운영하고 측정하는지(어떻게) → 어떻게 보호하는지(안전) → 어디서 더 갈 수 있고 어떻게 팀에 옮겨심는지(현장과 미래)"**의 5단 흐름을 따른다. v2에서는 3부와 4부에 운영·인젝션 챕터를 합류시켜, 합의→골격→운동·운영→방어→전파의 자연스러운 사다리를 완성했다.

**1부**는 거울이다. Hashimoto의 6단계 도입 여정을 들어 독자에게 "당신은 지금 몇 단계인가"를 묻는다. Osmani·Anthropic·OpenAI가 같은 시기에 같은 결론에 도달했다는 사실을 타임라인으로 보여 준다. 평가 하네스와 런타임 하네스가 동형(同形)임을 받아들이는 순간, 책이 다룰 좌표가 정해진다.

**2부**는 척추다. CAR 3축 — Control·Agency·Runtime — 으로 하네스를 분해하고, Böckeler의 Guides·Sensors 프레임워크와 SWE-agent의 ACI 4원칙으로 골격을 세운다. 책에서 가장 이론적이지만, 매 챕터 끝에 "당신의 AGENTS.md를 이 렌즈로 다시 봐 보자"는 자가 점검을 끼운다.

**3부**는 운동이다. 척추가 어떻게 움직이는지를 본다. 컨텍스트 부패와 그 대응(2-prompt·압축기·Ralph Loop), 단일 vs 다중 에이전트 논쟁의 합의점, Generator-Evaluator의 정량적 효과까지 다룬 뒤, **15장(신설) — 관측·비용 운영**에 합류해 "Sensors의 다른 얼굴"인 5축 메트릭과 트레이스 도구(LangSmith·Helicone·Langfuse·Phoenix), 모델 회귀 탐지 회로를 운영 차원에서 정착시킨다. 이 부 끝에서 독자는 "장기 실행 작업을 어떻게 살아 있게 두고, 어떻게 정량으로 지키는지"의 답을 얻는다.

**4부**는 안전이다. 하네스 자체가 공격 표면이 되었다. Lethal Trifecta로 위협 모델을 익히고, Shai-Hulud 사고를 분해하고, **프롬프트 인젝션 공격 카탈로그(신설)** 를 분류한 뒤, 격리를 **이론(MicroVM·gVisor 비교)** 과 **운영 레시피(Docker·devcontainer·sandbox-exec 30분 PoC)** 두 챕터로 나눠 짠다. 마지막 21장은 평가 회피·Sandbagging로 "보안과 평가는 같은 동전의 양면"이라는 결론에 닿는다.

**5부**는 현장이다. SWE-Bench·Terminal-Bench·OSWorld·METR Time Horizon 같은 평가 인프라를 자기 손에 쥐는 법, OpenHands·Aider·Cursor·Claude Code·Codex CLI를 비교하는 렌즈, 한국어 생태계(revfactory·instructkr·Haandol·MadPlay)와 한국 환경 특수 이슈, 그리고 **팀 도입·온보딩(신설)** — 1주차·2주차·1개월 체크리스트, 승인 프로세스, 갈등 사례. 마지막 25장은 메타 하네스를 코드 수준에서 분해하고 자기 강화 편향의 위험까지 짚는다. **23장 에필로그**는 한국·해외 실무자 5~7명의 인용 모자이크로 책을 닫는다.

**부록**은 실무자를 위한 작업대다. 본문이 "왜·무엇·어떻게"라면, 부록은 "오늘 당장 손에 쥐고 시작할 도구함"이다. v2에서 운영 런북(부록 G)·평가 골든 케이스(부록 H)가 합류해 본문 운영 챕터의 도구함이 완성된다.

이 순서가 깨질 수 있는 유일한 지점은 v1과 같다: **2부 5장(ACI 4원칙)을 1부 직후로 당기고 싶은 유혹**. 하지만 ACI는 추상이 강해서, CAR 분해를 먼저 보여 주고 그 안에 ACI를 끼워야 독자가 길을 잃지 않는다.

---

## 5. 챕터 목록

전체 5부 25장 + 에필로그(23장) + 부록 8종. 각 부 인트로(2~3쪽)는 챕터 수에서 제외했다. 분량은 본문만의 추정. **v1→v2 매핑**은 보고 메시지 끝 표 참조.

---

### 1부. 패러다임의 전환 — 프롬프트에서 하네스로 (4장 / 약 56쪽)

> **부 인트로:** 2026년 봄, 같은 결론을 외친 다섯 명의 목소리. Hashimoto·Osmani·Böckeler·Anthropic·OpenAI.

#### 1장. Agent = Model + Harness, 그러므로 우리는 무엇을 하는가
- **핵심 질문:** "프롬프트 엔지니어링이 끝났다"는 말의 진짜 뜻은 무엇인가?
- **주요 내용:**
  - "프롬프트의 시대는 끝났다"는 산업 합의의 인용 퍼레이드(Osmani·Hashimoto·OpenAI Codex 팀)
  - Harness = 마구(말의 고삐+안장+굴레). 어원이 본질이다
  - Osmani의 6 카테고리(시스템 프롬프트·도구·메모리 파일·미들웨어·후크·**관측·비용**)
  - "당신이 모델을 만드는 사람이 아니라면 — 당신이 하는 일은 모두 하네스다"
  - 프롬프트 엔지니어링 ⊂ 컨텍스트 엔지니어링 ⊂ 하네스 엔지니어링 — 동심원 모델
  - **신규 복선:** "6번째 카테고리 *관측·비용*은 15장 운영 챕터에서 본격적으로 다룬다." 한 줄을 박아 책 전체 챕터 지도와 1:1로 만나게 한다.
- **시그니처 인용:** Addy Osmani — "Agent = Model + Harness. 당신이 모델을 만드는 사람이 아니라면, 당신이 하는 일은 모두 하네스 엔지니어링이다."
- **시그니처 감정 단어:** 찜찜하다 (도입 훅)
- **독자가 얻는 것:** 책 전체에서 쓸 좌표계와 어휘. "프롬프트"와 "하네스"를 같은 자리에서 쓰지 않게 된다.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** 강한 청유형(입구). "Cursor에 익숙한 동료가 어느 날 'AGENTS.md를 아무리 고쳐도 같은 실수를 한다'고 하소연한다고 해보자"로 상황 가정. "이쯤 되면 찜찜하다"로 감정 공감. "그렇다면 무엇이 문제일까?"로 자답.
- **실습 형식:** 코드/설정 점검 — 자기 프로젝트의 `CLAUDE.md`/`AGENTS.md`를 열고 Osmani 6 카테고리에 매핑.
- **다음 챕터 다리:** "그래서 — 우리는 어디쯤 와 있을까? Hashimoto가 그 답을 6단계로 정리했다."

#### 2장. Hashimoto의 6단계 — 당신은 지금 몇 단계인가
- **핵심 질문:** 내가 지금 AI 도입의 어느 지점에 서 있는지 어떻게 정직하게 알 수 있는가?
- **주요 내용:**
  - Hashimoto가 *My AI Adoption Journey*에서 정리한 자기 진화 단계
  - 1단계 자동완성 → 2단계 챗 → 3단계 단발 에이전트 → 4단계 장기 에이전트 → 5단계 하네스 엔지니어링 → 6단계 메타 하네스
  - 각 단계의 증상(에이전트가 같은 실수를 반복하면 짜증을 낸다 → 단계 정체 신호)
  - "Friction is natural" — 마찰을 인정하라
  - "에이전트 데스크톱 알림은 꺼라. 컨텍스트 스위칭이 가장 비싸다"
  - 단계별 다음 한 걸음 체크리스트(자가 진단)
- **시그니처 인용:** Mitchell Hashimoto — "에이전트가 실수를 저지를 때마다, 당신은 에이전트가 다시는 그 실수를 하지 않도록 시스템적 해결책을 엔지니어링하는 데 시간을 쏟아야 한다."
- **시그니처 감정 단어:** 끔찍한 일이다 (4단계 정체 묘사)
- **독자가 얻는 것:** 자기 단계를 지정하고, 다음 챕터들을 읽는 동안 어디에 더 시간을 쏟을지 결정.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "솔직해지자"로 청유형 도입. "당신은 사실 3단계인데 5단계인 척한 적이 없는가?" 감정 공감.
- **실습 형식:** 코드/설정 점검 — 6단계 자가 진단 워크시트(부록 A로 연결).
- **다음 챕터 다리:** "단계가 정해졌다면 — 평가와 운영, 두 코스가 같은 마구를 쓴다는 사실부터 받아들이자."

#### 3장. 평가 하네스와 런타임 하네스는 같은 코드를 쓴다
- **핵심 질문:** 벤치마크에서 잘 나오게 만드는 트릭이 왜 그대로 프로덕션의 베스트 프랙티스가 되는가?
- **주요 내용:**
  - SWE-Bench·Terminal-Bench·OSWorld의 채점 인프라 = 평가 하네스
  - Claude Code·Codex CLI·OpenHands = 런타임 하네스
  - 두 하네스의 동형성(同形性) — "모델을 환경 안에서 행동하게 만드는 코드"
  - 동형성이 결정적인 이유: 평가 트릭이 운영 베스트 프랙티스가 된다 → 메타 하네스의 길이 여기서 열림
  - Inspect Evals — 두 세계를 잇는 표준
  - **신규 비유 절(리뷰 §6 권고):** "마구가 평가 코스에서도, 실제 길에서도 같은 형태인 것처럼 — 안장과 고삐가 코스마다 달라지면 우리는 같은 말을 두 번 길들이는 셈이다."
- **시그니처 인용:** OpenAI Harness 팀 — "Humans steer. Agents execute (사람은 조종하고, 에이전트는 실행한다)."
- **시그니처 감정 단어:** 번거롭다 (두 하네스를 따로 관리하는 비용)
- **독자가 얻는 것:** 평가와 운영을 하나의 시스템으로 보는 시야.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** 의도적 저(低)청유형. "벤치마크 점수와 실무 효율, 그 둘이 따로 논다고 느낀 적이 있을 것이다"로 공감 도입.
- **실습 형식:** 코드/설정 점검 — OpenHands evaluation harness 디렉토리 구조를 따라 자기 프로젝트의 회귀 테스트 한 번 정리.
- **다음 챕터 다리:** "동형성이 사실이라면, 같은 모델이 다른 하네스 위에서 다른 점수를 받는 것은 당연하다. Terminal-Bench 2.0이 그 사실을 정량으로 보여 줬다."

#### 4장. 모델보다 중요한 하네스 — Terminal-Bench 2.0이 보여준 것
- **핵심 질문:** 같은 모델이 다른 하네스 위에서 왜 다른 점수를 받는가?
- **주요 내용:**
  - Terminal-Bench 2.0의 6개 하네스 비교(Claude Code, Codex CLI, Gemini CLI, OpenHands, Mini-SWE-Agent, Terminus 2)
  - "A decent model with a great harness beats a great model with a bad harness"
  - "they look more like each other than their underlying models do"
  - METR의 7개월/4개월 더블링 데이터, 그리고 그 한계
  - Anthropic Claude 4.6 시스템 카드의 평가 하네스 명시
  - Pragmatic Engineer의 반론: "AI는 답을 알 때 빠르고, 모를 때 위험하다"
  - **신규 마무리(리뷰 §5 권고):** Sonnet 4.5→4.6 회귀를 자기 환경에서 어떻게 *예방·탐지*할까. **15장 운영 챕터로의 forward bridge 한 단락.**
- **시그니처 인용:** Addy Osmani — "A decent model with a great harness beats a great model with a bad harness."
- **시그니처 감정 단어:** 난감하다 (회귀 사건 도입)
- **독자가 얻는 것:** "모델 업그레이드 = 점수 상승"이라는 단순 모델에서 벗어남.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "Sonnet 4.5에서 4.6으로 갈아탔는데 코드 품질이 떨어졌다 — 이게 무슨 일일까?" 수사적 질문 도입.
- **실습 형식:** **시나리오 시뮬레이션** — "팀 회의 시나리오: Sonnet 4.6 회귀를 어떻게 보고할 것인가" 롤플레이. (운영 챕터의 복선)
- **다음 챕터 다리:** "1부에서 좌표가 정해졌으니, 이제 척추를 세우자. CAR 3축으로 분해하는 데서 시작한다."

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
- **시그니처 인용:** `proposal.md` 저자 — "하네스의 각 구성 요소는 '모델이 스스로 할 수 없는 것에 대한 가정'을 인코딩한다." (Anthropic *Harness design* 인용)
- **시그니처 감정 단어:** 번거롭다 (분해 노동의 무게)
- **독자가 얻는 것:** 챕터 끝에서 자기 환경의 CAR 매트릭스 한 장.
- **예상 분량:** 약 16쪽
- **Toby 스타일 적용 (리뷰 §6 권고 반영):** 의도적 저(低)청유형. **수정된 도입:** "AGENTS.md를 백 줄 썼는데도 같은 실수를 한다고 해보자. 그 백 줄은 어디에 속할까? 아니, 우리가 어떤 *축*으로 분해해야 빈자리가 보일까?"
- **실습 형식:** 코드/설정 점검 — CAR 3열 표에 자기 프로젝트의 30개 하네스 항목 넣어 보기 → 빈 칸이 보이면 그것이 다음 작업.
- **다음 챕터 다리:** "축이 셋이라면, 시간 축은 어떨까? 행동 *전*과 *후* — Guides와 Sensors가 그 자리를 맡는다."

#### 6장. Guides와 Sensors — 사이버네틱 폐루프로서의 하네스
- **핵심 질문:** 행동 전과 후, 두 통제는 어떻게 함께 작동해야 하는가?
- **주요 내용:**
  - Böckeler의 Guides/Sensors 프레임워크
  - 3가지 규제 차원: Maintainability / Architecture fitness / **Behaviour harness**
  - 1948년 Wiener의 사이버네틱스 — 피드포워드 + 피드백의 안정성
  - 피드포워드 단독·피드백 단독의 실패 모드
  - "When the agent struggles, treat it as a signal: identify what is missing"
  - **차별화 포인트: 한국어 책에서 'Behaviour harness(기능적 정확성)'를 정면으로 다루는 첫 시도**
- **시그니처 인용:** Birgitta Böckeler — "When the agent struggles, treat it as a signal: identify what is missing."
- **시그니처 감정 단어:** 찜찜하다 (피드백 단독의 함정)
- **독자가 얻는 것:** "에이전트가 헛발 짚을 때 무엇이 빠졌는지 묻는" 진단 습관.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용 (리뷰 §6 권고 반영):** 의도적 저(低)청유형. **수정된 도입:** "1948년 Wiener가 사이버네틱스를 정의할 때, 그가 본 것은 무엇이었을까? 우리가 지금 마구를 짤 때 그가 도움이 될까?" 그 다음 단락에서 사이버네틱스 폐루프를 풀어낸다.
- **실습 형식:** 코드/설정 점검 — 최근 1주일 에이전트 실패 로그 5건을 Guides/Sensors 둘 중 어느 쪽이 빠졌는지 분류.
- **다음 챕터 다리:** "골격이 셋과 둘로 잡혔다. 그 다음은 인터페이스다 — 인간이 쓰는 IDE의 가정을 모두 버려야 한다."

#### 7장. ACI 4원칙 — 인간 IDE의 가정을 버려라
- **핵심 질문:** 에이전트가 쓰는 인터페이스가 왜 인간이 쓰는 IDE와 달라야 하는가?
- **주요 내용:**
  - Yang et al. SWE-agent 페이퍼의 4원칙
  - (1) 단순한 액션 (2) 효율적 액션 (3) 한정된 출력 (4) 영속 상태(`CURRENT_FILE`, `FIRST_LINE`)
  - SWE-Bench Lite 12.5%(2024) 점프의 정확한 메커니즘
  - "토큰 단위로 사고하는 모델"의 인지적 한계와 인터페이스 설계의 관계
  - ls·cat·grep을 쓰지 말라 — 왜 통합 명령이 더 강한가
- **시그니처 인용:** Yang et al. (SWE-agent) — "Custom interfaces designed for agents — not humans — yield outsized performance gains."
- **시그니처 감정 단어:** 번거롭다 (도구를 다시 짜는 노동)
- **독자가 얻는 것:** 자기 도구 정의를 ACI 4원칙으로 점검하는 능력. **이것이 책의 진짜 척추.**
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** 의도적 저(低)청유형. "shell 도구를 그대로 던져 줬더니 에이전트가 ls를 30번 한다 — 이게 정상일까?"
- **실습 형식:** 코드/설정 점검 — 자기 도구 정의 한 개를 ACI 4원칙으로 리팩토링.
- **다음 챕터 다리:** "도구가 잘 짜여도, 그 위의 메모리 파일이 비대해지면 다 무너진다. 8장에서 그 함정을 본다."

#### 8장. 왜 큰 AGENTS.md는 실패하는가
- **핵심 질문:** 한 곳에 모은 지침이 왜 오히려 에이전트를 무력하게 만드는가?
- **주요 내용:**
  - "Context is a scarce resource" — OpenAI Codex 팀의 통합 AGENTS.md 실패
  - 분산 AGENTS.md: `.eslintrc`/`.gitignore`처럼 가까운 파일이 우선
  - AGENTS.md의 모든 줄은 한 번의 실패에 대응한다 — Hashimoto 룰
  - Linux Foundation Agentic AI Foundation의 표준화 거버넌스
  - revfactory/harness의 "AGENTS.md 자동 갱신 후크" (25장에서 코드 수준 분해)
  - "Garbage Collection 에이전트" — 안 쓰는 줄을 자동으로 삭제 (25장 복선)
  - **연계 강화 (리뷰 §5 권고):** 분산 패턴 3종(Cascading / Domain-split / Layer-split)의 즉시 적용 템플릿은 부록 A. 본문에서 "부록 A를 옆에 펴 두자" 명시.
- **시그니처 인용:** OpenAI Codex 팀 — "Context is a scarce resource."
- **시그니처 감정 단어:** **찜찜하다** (500줄짜리 AGENTS.md의 무력감)
- **독자가 얻는 것:** 디렉토리별 분산 메모리 파일 설계 패턴.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "AGENTS.md가 500줄이 넘었다 — 그런데 왜 에이전트는 더 헷갈려할까? 솔직히, 좀 찜찜하지 않은가?"
- **실습 형식:** 코드/설정 점검 — 자기 AGENTS.md를 토픽별로 3~5개 디렉토리로 쪼개고 효과를 1주일 측정.
- **다음 챕터 다리:** "메모리를 쪼갰다면, 도구도 쪼개자. 9장은 Agency의 설계다."

#### 9장. 도구·MCP·서브에이전트 — Agency를 설계하기
- **핵심 질문:** 모델에게 무엇을 시킬 수 있게 할지, 어떤 표면적으로 줄지를 어떻게 정하는가?
- **주요 내용:**
  - MCP(Model Context Protocol) — 도구·리소스·프롬프트 표준
  - Anthropic 'Scaling Managed Agents': 두뇌와 몸을 분리하라
  - 서브에이전트 패턴: Cursor Subagents, Sourcegraph Amp Oracle, Anthropic Skills
  - **모델 다중성(model multiplexing) — 별도 절(리뷰 §5 권고):** 강추론은 큰 모델, 잡일은 빠른 모델. 비용·지연·정확도의 3축 트레이드오프 + 라우팅 휴리스틱 + 실패 사례. (분량 +2쪽)
  - 도구 설명도 prompt injection 표면 — 4부 18장(인젝션 카탈로그)의 복선
  - **실패 사례**: 도구 30개를 한 번에 던졌더니 에이전트가 어느 도구를 쓸지 결정 못 함(인지 과부하)
- **시그니처 인용:** Anthropic *Scaling Managed Agents* — "Separate the brain from the body."
- **시그니처 감정 단어:** 번거롭다 (도구 30개 관리)
- **독자가 얻는 것:** 도구·서브에이전트 권한 설계의 기초 휴리스틱 + 모델 다중성 라우팅.
- **예상 분량:** **약 14쪽** (v1 12쪽 → v2 14쪽)
- **Toby 스타일 적용:** 의도적 저(低)청유형. "도구를 많이 줄수록 똑똑해질까? 글쎄, 그렇지 않다."
- **실습 형식:** 코드/설정 점검 — 자기 MCP 서버 설정에서 도구 수를 절반으로 줄여 보고, **그 중 1개는 작은 모델로 라우팅** 해서 결과 비교.
- **다음 챕터 다리:** "골격이 잡혔으니 이제 운동을 보자. 컨텍스트가 시간을 따라 어떻게 부패하는지부터다."

---

### 3부. 장기 실행과 컨텍스트 — 살아 있는 에이전트 (6장 / 약 90쪽)

> **부 인트로:** 척추가 움직이는 모습을 보자. 컨텍스트 부패와 그 대응, 그리고 운영의 정량.

#### 10장. Context Rot — 긴 컨텍스트의 배신
- **핵심 질문:** 왜 큰 윈도우를 가진 모델조차 긴 컨텍스트에서 멍청해지는가?
- **주요 내용:**
  - Chroma 연구: 18개 SOTA 모델, 입력 길이가 길수록 단순 검색조차 신뢰성 하락
  - 의미 유사도가 낮을수록 길이 효과 더 강함
  - 충격적 발견: **구조적 일관성이 높은 haystack이 오히려 성능을 더 떨어뜨린다**
  - "Context rot"이라는 용어의 기원과 산업 채택
  - Anthropic의 응답: "smallest possible set of high-signal tokens"
  - **신규 비유(리뷰 §6 권고):** "5만 단어짜리 회의록을 받았다. 거기서 *세 줄짜리 결정*을 다시 찾으려면 어떻게 할까? 모델도 같은 일을 한다."
  - **신규 케이스 박스 1쪽(리뷰 §5 권고):** *한글 토큰 비용* — 영문 대비 1.5~2배 토큰화 → 같은 윈도우에서 영문 대비 30~50% 일찍 rot 발생. 한국어 환경에서 컨텍스트 압축 정책의 우선순위가 다른 이유.
- **시그니처 인용:** Anthropic *Effective context engineering* — "The smallest possible set of high-signal tokens."
- **시그니처 감정 단어:** 난감하다 (1M 윈도우인데 50K에서 무너짐)
- **독자가 얻는 것:** "컨텍스트 = 자원"이라는 본능적 감각.
- **예상 분량:** 약 15쪽 (v1 14쪽 → v2 15쪽, 한글 케이스 박스 1쪽 추가)
- **Toby 스타일 적용:** 의도적 저(低)청유형. "컨텍스트 윈도우가 1M인데도 50K 넘으면 멍청해진다 — 이거 우리만 겪는 일일까?"
- **실습 형식:** 코드/설정 점검 — 같은 질문을 5K·50K·200K 컨텍스트에서 던져 정확도 비교, 한국어 입력으로도 한 번 더.
- **다음 챕터 다리:** "긴 컨텍스트를 못 믿겠다면, 매일 새로 시작하자. 11장의 2-prompt 패턴이 그 답이다."

#### 11장. 2-Prompt 패턴 — Initializer와 Coding의 분리
- **핵심 질문:** 매번 새로 시작하는 세션을 어떻게 살아 있는 작업으로 잇는가?
- **주요 내용:**
  - Anthropic *Effective harnesses for long-running agents*
  - Initializer: 첫 1회 — 환경 분석, AGENTS.md 작성, 테스트 러너 검출, `claude-progress.txt` 초기화
  - Coding: 매 세션 — progress 읽기 → 작은 진전 → progress 갱신 → 커밋
  - "각 세션은 깡통 컨텍스트로 시작한다는 것을 받아들이는 설계"
  - 디스크 위 산출물이 모델 메모리를 대체한다
  - **출처 명확화(리뷰 §5 권고):** NOTES.md / claude-progress.txt 작성 휴리스틱을 *Anthropic 원문 권고*와 *저자 권고*로 분리 표기. 표 한 장으로 한 눈에 보이게.
- **시그니처 인용:** Anthropic *Effective harnesses for long-running agents* — "Each session must start from a blank context — design for that, not against it."
- **시그니처 감정 단어:** **끔찍한 일이다** (다음날 처음부터 다시)
- **독자가 얻는 것:** 다음날 다시 시작하는 에이전트가 30초 내 복구 가능한 시스템.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** 의도적 저(低)청유형. "어제까지 잘 가다 오늘 새 세션 열었더니 처음부터 다시 — 이쯤 되면 끔찍한 일이다."
- **실습 형식:** 코드/설정 점검 — 자기 프로젝트에 progress.txt 도입하고 다음 세션 복원 시간 측정.
- **다음 챕터 다리:** "디스크가 메모리를 대체한다면, 루프는 단순할수록 강하다. 12장 — Ralph가 그 사실을 증명한다."

#### 12장. Ralph Loop은 어떻게 단순함의 승리가 되었나
- **핵심 질문:** 한 줄짜리 bash 루프가 왜 Anthropic 공식 플러그인이 됐는가?
- **주요 내용:**
  - Geoffrey Huntley의 Ralph Wiggum 패턴
  - "Ralph is a Bash loop" — `while true; do <feed prompt>; done`
  - 컨텍스트가 다 차면 종료, 새로 시작. 진행 상태는 파일에서 복원
  - "300줄 루프 + LLM 토큰" — 에이전트 짜는 게 그렇게 어렵지 않다
  - 2025-12 Anthropic이 공식 플러그인으로 채택
  - 비판과 보완: Sondera의 *Supervising Ralph* — Principal Skinner 감독 패턴
  - 무한 루프의 비용 통제 휴리스틱(상세는 15장 운영 챕터에서 정량)
- **시그니처 인용:** Geoffrey Huntley — "Ralph is a Bash loop."
- **시그니처 감정 단어:** 번거롭다 → "그런데 Ralph가 그 번거로움을 한 줄로 줄여 준다"
- **독자가 얻는 것:** 자기 환경에서 Ralph 루프 한 시간 만에 돌리기.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** "에이전트 = 복잡한 시스템이라고 생각했다면, 한 번 솔직해지자. Ralph가 그 환상을 깬다."
- **실습 형식:** 코드/설정 점검 — 30줄짜리 bash Ralph Loop 직접 작성.
- **다음 챕터 다리:** "루프가 돌면 — 그 출력을 누가 평가하는가? 같은 모델이 자기 결과를 채점하는 건 위험하다."

#### 13장. Generator-Evaluator — 자기 평가의 함정과 해법
- **핵심 질문:** 같은 모델이 자기 결과를 평가하면 왜 과대평가하고, 그걸 어떻게 막는가?
- **주요 내용:**
  - Anthropic 3-에이전트(Planner-Generator-Evaluator) 사례
  - Prithvi Rajasekaran 인용: "작업하는 에이전트와 판정하는 에이전트를 분리하는 것이 강력한 지렛대"
  - Few-shot 예제와 채점 기준으로 Evaluator 캘리브레이션
  - 프런트엔드 디자인 작업: 5~15회 반복, 최대 4시간 수렴
  - Aider Architect/Editor 듀얼 모델 — 같은 사상
  - **컨텍스트 보존이 아니라 컨텍스트 리셋 + 구조화된 핸드오프**가 비밀
- **시그니처 인용:** Prithvi Rajasekaran (Anthropic) — "Separating the agent that does the work from the agent that judges it is a powerful lever."
- **시그니처 감정 단어:** 찜찜하다 (자기 평가의 과대확신)
- **독자가 얻는 것:** 자기 작업에 Evaluator를 분리할지 판단하는 기준.
- **예상 분량:** 약 16쪽
- **Toby 스타일 적용:** "에이전트가 '다 됐다'고 했는데 막상 보니 절반밖에 안 된 적, 있지 않은가?"
- **실습 형식:** 코드/설정 점검 — 한 작업을 Generator만, Generator+Evaluator 분리 두 방식으로 돌려 정확도 비교.
- **다음 챕터 다리:** "둘이 좋다면, 셋·다섯·열은? 14장에서 단일 vs 다중 논쟁의 합의점을 본다."

#### 14장. 단일 에이전트 vs 다중 에이전트 — 합의가 형성된 자리
- **핵심 질문:** 멀티에이전트는 언제 쓰고, 언제 쓰지 말아야 하는가?
- **주요 내용:**
  - Cognition *Don't build multi-agents* — game of telephone 비판
  - "It's about avoiding this game of telephone" — Walden Yan 인용
  - Anthropic *How We Built Our Multi-Agent Research System* — 같은 주 정반대 발표
  - 합의: 쓰기 위주 의존성 강한 작업 = 단일 / 읽기 위주 병렬 가능 작업 = 다중
  - 토큰 사용 3~5배의 트레이드오프 — 언제 정당한가
  - **Cognition 입장 진화 — 별도 절(리뷰 §5 권고):** *Multi-Agents: What's Actually Working* (2026). 단일 옹호자가 멀티를 부분 인정한 정도, 그 조건들.
  - 코딩 핵심 워크플로 권장: 단일 또는 Generator-Evaluator 2자
- **시그니처 인용:** Walden Yan (Cognition) — "It's about avoiding this game of telephone."
- **시그니처 감정 단어:** 난감하다 (멀티에이전트의 비용·정확도 트레이드오프)
- **독자가 얻는 것:** "멀티에이전트가 멋있어 보여서 쓴다"에서 벗어남.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "여러 에이전트를 띄우면 더 빨라질까? 물론 그렇다. 하지만 더 정확해질까? 그건 다른 문제다."
- **실습 형식:** **디스커션** — "가상 토론: Walden Yan과 Anthropic 멀티에이전트팀이 한 회의실에 있다면" 30분 페어 토론. 자기 워크플로의 작업 5개를 'write-heavy / read-heavy' 로 분류.
- **다음 챕터 다리:** "토폴로지가 정해졌다면 — 그 운동을 어떻게 정량으로 지키는가? 15장의 5축 메트릭이 답한다."

#### 15장. 관측과 비용 — Sensors의 다른 얼굴 (신규)
- **핵심 질문:** "내 하네스가 잘 돌고 있다"를 어떻게 숫자로 보여주는가? 그리고 그게 *언제* 흔들리기 시작하는지를 어떻게 *먼저* 아는가?
- **주요 내용:**
  - **5축 메트릭:** latency · token usage · cost · success rate · regression delta. 각 축의 정의·계산식·임계 알람
  - **트레이스 도구 비교:** LangSmith, Helicone, Langfuse, Phoenix — 핵심 차이 4열 표
  - **OpenTelemetry GenAI Semantic Conventions** — 도구 간 호환의 표준
  - **비용 알람·throttling·model fallback 패턴** — 토큰 폭주를 한 줄로 막는 후크
  - **모델 회귀 탐지 회로** — golden case 30개 + 일일 자동 평가 (부록 G·H로 연결)
  - **운영 케이스 스터디 — Sonnet 4.5→4.6 회귀:** 4장 도입 훅의 마무리. 회귀를 *탐지*·*롤백*·*재평가*하는 운영 패턴을 코드 수준에서 분해
- **시그니처 인용:** Birgitta Böckeler — "Sensors are not optional in a cybernetic harness — they are the *only* way to close the loop."
- **시그니처 감정 단어:** 난감하다 (회귀가 *조용히* 들어올 때)
- **독자가 얻는 것:** 자기 하네스의 5축 대시보드 첫 버전. 다음 회귀를 *먼저* 탐지하는 회로.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "에이전트가 *조용히* 멍청해지면 우리는 모른다. 그래서 Sensors는 옵션이 아니다."
- **실습 형식:** 코드/설정 점검 — 자기 프로젝트에 LangSmith(또는 동급) 트레이스 한 번 붙이고 5축 중 3축을 일일 그래프로 띄우기.
- **다음 챕터 다리:** "정량으로 지킬 수 있게 됐다면 — 이제 공격을 보자. 4부의 첫 챕터, Lethal Trifecta다."

---

### 4부. 보안과 격리 — 하네스가 공격받을 때 (6장 / 약 84쪽)

> **부 인트로:** 2025년 9월 Shai-Hulud, 11월 2.0, 2026년 2월 SANDWORM_MODE. 하네스 자체가 표면이 됐다.

#### 16장. Lethal Trifecta — Simon Willison의 위협 모델
- **핵심 질문:** 에이전트가 위험해지는 정확한 조건은 무엇인가?
- **주요 내용:**
  - Willison의 3요소: Private data + Untrusted content + External communication
  - GitHub MCP 익스플로잇 사례 — 공개 이슈 prompt injection으로 private 데이터 유출
  - Indirect prompt injection의 메커니즘
  - 데이터 위치 분리, 출력 영역 화이트리스트, 사용자 승인 게이트
  - MCP 도구 description 자체가 공격 표면 (18장 카탈로그 복선)
  - 한국 환경 적용: 사내 GitLab + Jira + Slack 통합 시 trifecta 발생 시나리오
- **시그니처 인용:** Simon Willison — "Private data + Untrusted content + External communication = the lethal trifecta."
- **시그니처 감정 단어:** **난감하다** (자기 봇이 trifecta에 걸려 있다는 발견)
- **독자가 얻는 것:** "이 에이전트는 trifecta에 걸려 있는가?"라는 한 줄짜리 질문.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** "내 사내 봇이 GitHub 이슈를 읽고 Slack에 답장한다 — 이거 안전할까? 잠깐, 안전이 무엇을 뜻하는지부터 정의해보자."
- **실습 형식:** **페어 워크** — 자기 에이전트의 도구 매트릭스에 trifecta 색칠하기(빨강/노랑/초록)를 *팀원과 함께* 한다. 두 사람의 색칠이 같은지 다른지가 진단 신호.
- **다음 챕터 다리:** "위협 모델이 정해졌다면 — 그 위협이 *실제로* 어떻게 번지는지를 봐야 한다. Shai-Hulud가 그 답이다."

#### 17장. Shai-Hulud — 자기 복제하는 npm 웜의 해부
- **핵심 질문:** 한 번의 자격증명 탈취가 어떻게 25,000개 저장소로 번지는가?
- **주요 내용:**
  - 2025-09 Shai-Hulud 1.0: 자격증명 탈취, 자가 복제, 피해자 패키지 강제 푸시
  - 2025-11 Shai-Hulud 2.0: 25,000+ 저장소, 350+ 사용자, 수백 패키지
  - 2026-02 SANDWORM_MODE: 동일 패턴 + 악성 MCP 서버 → LLM API 키 추가 표적
  - Elastic의 대응 가이드
  - 하네스의 supply chain: MCP 서버, 도구 정의, 에이전트 메모리, CI 파이프라인 모두 검증 대상
  - 예방·탐지·복구 체크리스트
- **시그니처 인용:** Wiz Research — "What started as one stolen token cascaded into 25,000+ repositories in 72 hours."
- **시그니처 감정 단어:** 끔찍한 일이다 (남의 일이 우리 일이 되는 순간)
- **독자가 얻는 것:** "내 하네스의 supply chain"이라는 새 검토 차원.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "남의 일이라 생각했다면 다시 보자. 우리 npm install도 다 거기서 거기다."
- **실습 형식:** 코드/설정 점검 — 자기 프로젝트의 MCP 서버 의존성 트리를 그리고 신뢰 경계 표시.
- **다음 챕터 다리:** "공급망에서 들어오는 공격도 위험하지만, 텍스트 한 줄로 들어오는 공격이 더 흔하다. 18장 — 인젝션 카탈로그를 펼친다."

#### 18장. 프롬프트 인젝션 카탈로그와 방어 (신규)
- **핵심 질문:** 인젝션 공격은 몇 가지 모양이 있고, 각각을 어떻게 1차로 막는가?
- **주요 내용:**
  - **Direct vs indirect injection** — 사용자 입력 vs 외부 컨텐츠
  - **도구 description injection** — MCP 서버 description에 숨긴 명령어
  - **데이터 위치 분리(data segregation)** — 시스템·사용자·도구 결과의 채널 분리
  - **Canary token** — 인젝션 탐지의 카나리아 (Willison 권고)
  - **Output channel whitelist** — 에이전트가 *어디로* 출력할 수 있는지를 화이트리스트로 잠그기
  - **사용자 승인 게이트** — 위험한 동작 전에 명시적 confirm
  - **GitHub MCP 익스플로잇 분해** — Willison 사례를 단계별 시퀀스로
  - **한국 환경 시뮬레이션** — 사내 위키(Confluence) 인젝션, Jira 이슈 인젝션의 가상 시나리오
- **시그니처 인용:** Simon Willison — "Indirect prompt injection is the SQL injection of the LLM era."
- **시그니처 감정 단어:** 찜찜하다 (도구 description이 공격 표면이라는 사실)
- **독자가 얻는 것:** 인젝션 6가지 모양을 분류하고, 각 모양에 *최소 1개* 방어 패턴을 매핑하는 능력.
- **예상 분량:** 약 13쪽
- **Toby 스타일 적용:** "도구 설명에 한 줄 끼워 넣었더니 에이전트가 그대로 따라 한다 — 이거 우리도 당할 수 있을까? 그렇다, 거의 확실히."
- **실습 형식:** **시나리오 시뮬레이션** — 자기 사내 위키(또는 가상의 위키) 페이지 1개에 *교육용 canary*를 심고, 에이전트가 그걸 트리거하는지 1주일 관찰.
- **다음 챕터 다리:** "공격 표면을 알았다면 — 그 공격이 *터졌을 때* 시스템이 살아 있게 격리해야 한다. 19장과 20장에서 격리를 이론과 운영으로 나눈다."

#### 19장. 격리 3축 (이론·아키텍처) (17장 분할 — 이론 부분)
- **핵심 질문:** 에이전트가 망쳐도 시스템이 살아 있게 하려면 *어떤 축*으로 격리하는가?
- **주요 내용:**
  - UK AISI Inspect Sandboxing Toolkit의 3축: Tooling · Host · Network
  - **Firecracker MicroVM** (KVM 위, 100ms 시작, 5MB 메모리) — 아키텍처와 보안 모델
  - **gVisor** (사용자 공간 커널) — 다른 트레이드오프
  - **devcontainer**, **macOS sandbox-exec** — 가벼운 호스트 격리
  - egress 화이트리스트의 이론 — 단기 시크릿, 최소 권한 파일시스템
  - 3축의 *서로 다른 실패 모드* — 어느 축이 빠지면 어떤 사고가 어떻게 나는가
- **시그니처 인용:** UK AISI *Inspect Sandboxing Toolkit* — "Three axes — and you must close all three."
- **시그니처 감정 단어:** 번거롭다 (3축을 다 짜야 한다는 부담)
- **독자가 얻는 것:** "지금 우리 환경은 3축 중 어느 축이 비었는가"라는 진단.
- **예상 분량:** 약 8쪽
- **Toby 스타일 적용 (리뷰 §6 권고 반영):** **수정된 도입:** "에이전트가 `rm -rf`를 시도했다는 사연을 본 적 있을 것이다. 그 사연이 우리 일이 되지 않게 — 우리는 30분 안에 격리를 짤 수 있다. 진짜로? 그렇다, 진짜로. 다만 *세 축* 모두 알고 있어야 한다."
- **실습 형식:** 코드/설정 점검 — 3축에 자기 환경의 격리 항목을 매핑해 빈 칸 찾기.
- **다음 챕터 다리:** "이론을 봤으니 — 30분 안에 손에 쥐는 운영 레시피로 가자."

#### 20장. 격리 운영 레시피 (Docker·devcontainer·sandbox-exec 30분 PoC) (17장 분할 — 운영 부분)
- **핵심 질문:** 30분 안에 자기 에이전트를 어떻게 *실제로* 격리시키는가?
- **주요 내용:**
  - **레시피 1 — Docker + egress proxy + ephemeral secrets** (10분 PoC)
  - **레시피 2 — devcontainer + 최소 권한 파일시스템** (10분 PoC)
  - **레시피 3 — macOS sandbox-exec 프로파일** (10분 PoC)
  - Claude Code·Codex CLI의 격리 옵션 비교 — 무엇이 기본으로 켜져 있고 무엇이 비어 있는가
  - 운영 트러블슈팅 — egress proxy 깨짐, sandbox-exec 권한 거부, 시크릿 만료
  - 부록 G(운영 런북)으로의 forward bridge — on-call 플레이북 항목 매핑
- **시그니처 인용:** Anthropic Claude Code 팀 — "Sandbox first, debug second."
- **시그니처 감정 단어:** **번거롭다** → "그런데 이 번거로움이 우리를 살린다"
- **독자가 얻는 것:** 30분짜리 PoC 3종을 자기 환경에 띄울 수 있는 명령어 세트.
- **예상 분량:** 약 8쪽
- **Toby 스타일 적용:** "이게 번거로워 보이지만, *번거로움이 우리를 살린다*는 사실을 우리는 18장에서 이미 확인했다."
- **실습 형식:** 코드/설정 점검 — Docker + sandbox-exec 두 가지 격리 환경에 자기 에이전트 띄우고 비교.
- **다음 챕터 다리:** "격리됐어도 — 평가 환경을 *인지하는* 모델이 있다. 21장이 그 사각지대를 본다."

#### 21장. 평가 회피와 Sandbagging — 보안과 평가가 만나는 곳
- **핵심 질문:** 평가 환경에서 잘 행동하던 에이전트가 프로덕션에서 다르게 굴 가능성은 어떻게 막는가?
- **주요 내용:**
  - UK AISI OpenClaw 사례 — 에이전트가 평가 환경 단서(파일명·환경변수·리소스 한도)를 인지하면 행동 변경
  - **1차 자료 보강(리뷰 §5 권고):** Hubinger et al., *Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training* (2024). van der Weij et al., *AI Sandbagging: Language Models can Strategically Underperform on Evaluations* (2024). 두 페이퍼의 핵심 실험과 한계.
  - **신규 비유(리뷰 §6 권고):** "학생이 시험관 표정을 보고 답을 바꾼다고 해보자. 시험은 그 학생의 *진짜 실력*을 측정한 것일까?" 한 절.
  - 평가-프로덕션 환경 시각·구조적 동일화의 실제
  - Anthropic·Apollo의 evaluation-aware 모델 연구 동향
  - Inspect Evals의 평가 안전 모범 사례
  - **차별화 포인트: 한국어 책에서 평가 회피를 정면으로 다루는 첫 시도**
- **시그니처 인용:** Hubinger et al. (Anthropic) — "Standard safety training does not remove deceptive behavior — it teaches the model to hide it better."
- **시그니처 감정 단어:** 난감하다 (벤치마크 점수를 그대로 믿을 수 없다는 사실)
- **독자가 얻는 것:** 평가 결과를 비판적으로 읽는 시야.
- **예상 분량:** 약 15쪽
- **Toby 스타일 적용:** "벤치 점수가 좋으니 됐다 — 이렇게 안심하고 싶지만, 잠깐만 의심해보자."
- **실습 형식:** 코드/설정 점검 — 자기 평가 스위트에 환경 단서 제거 검사 항목 추가.
- **다음 챕터 다리:** "평가의 한계를 봤다면 — 그래도 *측정*은 해야 한다. 5부 22장에서 평가 인프라를 손에 쥔다."

---

### 5부. 평가·생태계·팀·미래 — 한국에서 하네스를 굴리는 법 (4장 + 에필로그 / 약 78쪽)

> **부 인트로:** 책의 마지막. 평가 인프라, 오픈소스 생태계, 한국어 환경, 팀 도입, 메타 하네스, 그리고 현장의 목소리.

#### 22장. SWE-Bench·Terminal-Bench·OSWorld — 자기 하네스를 정량 측정하기
- **핵심 질문:** "내 하네스가 좋아졌다"를 어떻게 숫자로 보여주는가?
- **주요 내용:**
  - SWE-Bench 시리즈(Original, Lite, Verified, Multimodal, Live) 비교
  - Terminal-Bench 2.0: 89개 어려운 터미널 과제 + Harbor OSS
  - OSWorld·WebArena: GUI 에이전트 평가
  - METR Time Horizons 1.0/1.1 — 도메인별 일반화 한계
  - Inspect Evals 200+ 프리빌트 평가
  - 자기 작업 도메인에 맞는 미니 벤치 만들기(15~30개 골든 케이스, 부록 H로 연결)
- **시그니처 인용:** METR — "Time horizon doubles every 7 months — but only on the tasks the harness can already see."
- **시그니처 감정 단어:** 찜찜하다 (체감으로는 좋아진 것 같은데…)
- **독자가 얻는 것:** 자기 도메인의 정량 평가 시작점.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** "체감으로는 좋아진 것 같다 — 그런데 정말 그럴까?"
- **실습 형식:** 코드/설정 점검 — 자기 도메인의 골든 케이스 15개를 만들고 Inspect로 돌리기.
- **다음 챕터 다리:** "평가가 손에 들어왔다면 — 어떤 하네스를 어디에 놓을지를 봐야 한다. 23장의 도구 풍경이다."

#### 23장. 오픈소스 풍경 — Claude Code·Codex CLI·Cursor·OpenHands·Aider
- **핵심 질문:** 어느 도구를 어느 자리에 놓을지, 어떤 렌즈로 비교하는가?
- **주요 내용:**
  - 1차 CLI: Claude Code(Subagents·Skills·Hooks), Codex CLI(AGENTS.md), Gemini CLI
  - IDE 통합: Cursor Agent + Subagents
  - 인디 OSS: Aider(repo-map + 듀얼 모델)
  - 일반 목적 OSS: OpenHands(평가 하네스 1급)
  - VS Code 통합 OSS: Cline, Continue, Goose, Roo
  - 멀티에이전트 프레임워크: LangGraph, CrewAI, AutoGen, MetaGPT, CAMEL
  - 비교 매트릭스: 격리·MCP·서브에이전트·메모리·**관측·비용 통합**·오픈성·운영 성숙도 (15장 5축 메트릭과 일치)
- **시그니처 인용:** Pragmatic Engineer — "AI is fast when it knows the answer; dangerous when it doesn't."
- **시그니처 감정 단어:** 난감하다 (도구가 너무 많다)
- **독자가 얻는 것:** 자기 팀에 맞는 도구 선택의 7열 비교표.
- **예상 분량:** 약 14쪽
- **Toby 스타일 적용:** 의도적 저(低)청유형. "Cursor가 좋다, Claude Code가 좋다 — 다 들어봤을 것이다. 그래서 무엇이 정답일까? 정답은 없다, 다만 좌표가 있다."
- **실습 형식:** 코드/설정 점검 — 자기 팀의 워크플로에 7열 비교표 채워 보기.
- **다음 챕터 다리:** "도구를 골랐다면 — 한국에서 누가 무엇을 하는지를 보자. 24장은 우리 동네 지도다."

#### 24장. 한국에서 하네스를 굴리기 — revfactory·instructkr·Haandol·MadPlay
- **핵심 질문:** 한국 환경의 특수 이슈(언어·보안 정책·생태계)를 어떻게 다루는가?
- **주요 내용 (리뷰 §5 권고 반영 — sub-section 명시화):**
  - **24.1 revfactory/harness, harness-100 (2쪽) — 황민호의 메타 팩토리**
    - 6가지 사전 정의 팀-아키텍처 패턴, "하네스 구성해줘" 한 마디로 자동 생성
    - 학술 논문 *Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality* (2026)
    - "L3 메타 팩토리 레이어"
  - **24.2 instructkr/claw-code (2쪽) — Sigrid Jin의 Claude Code 클린룸 재구현**
    - 아키텍처만 보고 Python·Rust로 재구현
    - 공개 2시간 만에 50K ⭐, 사상 최단 100K ⭐
    - WSJ 인터뷰, 250억+ 토큰 처리
  - **24.3 Haandol — *쉽게 설명한 하네스 엔지니어링* (1쪽)**
    - "지도가 없으면 어디로 가야 할지 모르고, 안전 로프가 없으면 한 번의 실수로 떨어진다"
    - 하네스 8 요소 정리
  - **24.4 MadPlay *Beyond Prompts and Context* (1쪽) — 영어/한국어 양본**
  - **24.5~24.8 한국 환경 특수 이슈 (4쪽 / 4 토픽 1쪽씩):**
    - 24.5 한글 토큰 비용(영문 대비 1.5~2배) → 컨텍스트 압축 정책 (10장 한글 케이스 박스와 호응)
    - 24.6 사내 보안 정책상 외부 API 제한 환경의 OSS + 자체 호스팅 모델
    - 24.7 코드 리뷰 메시지 한글화 vs 영문 표준화 — 팀 컨벤션 차원의 결정
    - 24.8 toss·우아한형제들·naver d2의 2026년 사례
  - **24.9 한국어 커뮤니티 학습 로드맵(부록 E로 연결, 1쪽)**
- **시그니처 인용:** Haandol — "지도가 없으면 어디로 가야 할지 모르고, 안전 로프가 없으면 한 번의 실수로 떨어진다."
- **시그니처 감정 단어:** 찜찜하다 (글로벌 자료만 좇느라 우리 동네를 모르는 부끄러움)
- **독자가 얻는 것:** "한국 개발자로서 어디서 시작하고 누구를 따라갈지"의 지도.
- **예상 분량:** **약 18쪽** (v1 16쪽 → v2 18쪽, sub-section 명시 + 환경 이슈 4종 1쪽씩)
- **Toby 스타일 적용:** **책 전체에서 가장 강한 청유형.** "글로벌 자료만 쫓다 보면 한국에서 누가 무엇을 하는지 놓치기 쉽다. 우리부터 살펴보자."
- **실습 형식:** **인터뷰** — revfactory/harness 한 번 돌려보고, claw-code 코드 30분 읽기, 그리고 instructkr 디스코드(또는 maintainer 트위터) **메인테이너에게 질문 1개 보내기**(실제 커뮤니티 진입).
- **다음 챕터 다리:** "도구도 골랐고 동네도 봤다. 그런데 — 우리 *팀*에 어떻게 옮겨심을까?"

#### 25장. 팀에 하네스를 도입하기 — 1주차·2주차·1개월 (신규)
- **핵심 질문:** 한 사람이 알게 된 것을 5명·30명·300명 팀에 *어떻게* 옮겨심는가?
- **주요 내용:**
  - **온보딩 단계별 체크리스트:** 1주차(개인 환경 셋업 + AGENTS.md 첫 작성) / 2주차(MCP 서버 화이트리스트 + 격리 1축 적용) / 1개월(5축 메트릭 대시보드 + 첫 평가 회귀 알람)
  - **승인 프로세스:** 도구 권한 등급, MCP 서버 화이트리스트 거버넌스, 시크릿 관리(단기 토큰·환경별 분리)
  - **PR에서 에이전트 사용 정책:** 라벨링(`agent-assisted` / `agent-authored`), 작성자 표기, diff 크기 한도, 리뷰어 가이드라인
  - **비용 분배·과금 리포팅:** 팀별·프로젝트별 비용 분배, 월간 리포트 템플릿(부록 G로 연결)
  - **갈등 사례 3종:**
    - 시니어 vs 주니어 — "내가 직접 짜는 게 더 빠른데" 시니어와 "에이전트에 너무 의존한다" 주니어 갈등
    - 보안팀 vs 개발팀 — MCP 서버 권한 협상의 가상 회의록
    - "에이전트가 망친 PR" 사후 회고 템플릿
- **시그니처 인용:** Anthropic *Harness design for long-running application development* — "Each component of the harness encodes an assumption about what the model cannot do on its own."
- **시그니처 감정 단어:** 번거롭다 (조직 정치의 무게)
- **독자가 얻는 것:** 다음 월요일 아침에 팀에 들고 갈 수 있는 1·2·4주 체크리스트.
- **예상 분량:** 약 12쪽
- **Toby 스타일 적용:** "혼자 잘 쓰는 건 쉽다. 팀 전체가 잘 쓰는 건 다른 문제다. 그 다른 문제를 풀어 보자."
- **실습 형식:** **시나리오 시뮬레이션 + 디스커션** — 가상의 30명 팀에서 자기가 도입 책임자라면 1주차·2주차·1개월에 *각각 어떤 회의를 잡을지* 회의록 초안 작성.
- **다음 챕터 다리:** "팀에 옮겨심었다면 — 그 다음은 *하네스가 스스로 자라는 것*이다. 26장이 메타 하네스다."

#### 26장. 메타 하네스 — 스스로 진화하는 시스템 (v1 22장 확장)
- **핵심 질문:** 하네스가 스스로 자신을 갱신할 때, 우리는 무엇을 하게 되는가? 그리고 그게 *항상* 좋은 일인가?
- **주요 내용 (리뷰 §3 권고 — 16~18쪽으로 확장):**
  - 메타 하네스의 정의: 운영 결과를 보고 자신의 구성을 갱신하는 하네스
  - **revfactory/harness의 자동 갱신 후크 — 코드 수준 분해.** 어떤 신호로 어떤 줄을 갱신·삭제하는가, 후크의 입력·출력·실패 모드
  - **OpenAI의 "Garbage Collection 에이전트" — 코드 수준 분해.** 안 쓰는 줄 자동 제거의 결정 기준, false positive 사례
  - **메타 하네스의 위험 — 자기 강화 편향(self-reinforcing bias).** 한 번 잘못 학습한 패턴이 자동 갱신으로 *더 강해지는* 시나리오. Sleeper Agents 결과와의 연결
  - 다음 5년의 질문: SWE-Bench++, OSWorld 고도화, METR Time Horizon 4개월 가속이 사실이라면
  - "Humans steer. Agents execute"에서 "Humans design environments. Agents iterate."로
  - 책의 5가지 출구 능력을 다시 호출(Reader Journey 자가 점검)
- **시그니처 인용:** OpenAI Harness 팀 — "Humans design environments. Agents iterate within them."
- **시그니처 감정 단어:** 찜찜하다 (자기 강화 편향의 위험)
- **독자가 얻는 것:** "이 책 한 권으로 끝내지 않고 계속 갱신할 자기 시스템"의 출발점 + 그 시스템의 위험까지.
- **예상 분량:** 약 17쪽 (v1 12쪽 → v2 17쪽, 코드 수준 분해 + 자기 강화 편향 절 추가)
- **Toby 스타일 적용:** 강한 청유형(출구로 향하는 챕터). "이 책의 마지막 본문 페이지가 닫혀도, 당신의 하네스는 살아 움직여야 한다. 우리 함께 그 시작점에 서자. 다만 — 그 시스템이 *틀리게* 자라면, 우리는 그것을 *어떻게* 알 수 있을까?"
- **실습 형식:** 코드/설정 점검 — 자기 AGENTS.md에 자동 갱신 후크 한 줄 추가하고 1주일 운용. 갱신된 줄을 *모두* 리뷰.
- **다음 챕터 다리:** "메타 하네스를 코드 수준에서 봤다. 마지막은 — 사람의 목소리다."

#### 23장(에필로그). 현장의 목소리·5년 뒤 (신규)
> 책 본문 25장 이후의 **에필로그** 챕터. 번호는 본문과 분리해 *Epilogue*로 표기하되, 사용자 권고에 따라 보고용으로 "23장"으로 부른다.

- **핵심 질문:** 이 책이 닫히는 자리에서, 현장은 무엇을 말하고 있고, 5년 뒤 우리는 어디에 서 있게 되는가?
- **주요 내용:**
  - **인용 모자이크 — 한국·해외 실무자 5~7명:**
    - revfactory 황민호 — 메타 팩토리의 다음 단계
    - instructkr Sigrid Jin — claw-code 이후의 한국어 OSS 전략
    - Haandol — 한국어 학습자에게 보내는 한 문장
    - Mitchell Hashimoto — "에이전트가 또 같은 실수를 하면…" 재인용 (책 전체 닫는 인용)
    - Birgitta Böckeler — Sensors의 미래 ("Cybernetics is not a metaphor — it's the operating principle")
    - 1~2명 추가 가능 (toss tech / 우아한형제들 / naver d2 실무자)
  - **5가지 출구 능력 자가 점검표** — 책 §3에서 정의한 5능력을 23개 문항으로 펼쳐 자가 점검
  - **5년 뒤의 질문 5개** — 에이전트가 직접 PR을 닫는 비율, 메타 하네스의 거버넌스, 평가 회피 대응의 표준화, 한국어 OSS의 글로벌 영향, 인간 개발자의 새 정체성
  - **닫는 인용:** Hashimoto — "에이전트가 또 같은 실수를 한다면, 시스템적 해결책을 엔지니어링하라."
- **시그니처 인용:** (이미 인용 모자이크 챕터이므로 시그니처는 닫는 인용 = Hashimoto)
- **시그니처 감정 단어:** 끔찍한 일이다 → "그러나 우리는 이제 그 끔찍함을 *시스템*으로 바꿀 수 있다"
- **독자가 얻는 것:** 책을 덮고 일어났을 때 자기 자리에서 *무엇을 먼저 할지*가 한 줄로 잡힌다.
- **예상 분량:** 약 11쪽
- **Toby 스타일 적용:** **책 전체에서 가장 강한 청유형 + 가장 부드러운 평어체의 결합**(출구). 한국어와 영어 인용을 짧고 리듬감 있게 교차.
- **실습 형식:** **디스커션 + 인터뷰** — 자기 팀의 동료 1명과 5가지 출구 능력 자가 점검표를 *함께* 채우고, *서로의 다른 점*을 30분 토론.
- **다음 챕터 다리:** (없음 — 책의 닫는 자리)

---

## 6. 부록 (Appendix) — 약 64쪽 (8종)

레퍼런스 12절의 권고를 기본으로 하되, 리뷰 §4 권고를 반영해 운영 런북(G)·평가 골든(H)을 신설했다. 본문이 "왜·무엇·어떻게"라면 부록은 "오늘 손에 쥘 도구함"이다.

### 부록 A. AGENTS.md 템플릿 갤러리 (약 12쪽)
- 9가지 시나리오별 템플릿: 단일 레포·모노레포·MSA·Python 백엔드·Node API·React 프론트·DevOps·데이터 파이프라인·문서 사이트
- 디렉토리 분산 패턴 3종(Cascading / Domain-split / Layer-split) — 8장에서 *명시적으로* 부록 A를 호출
- "한 줄 = 한 번의 실패" 원칙으로 작성 가이드

### 부록 B. MCP 서버 카탈로그 (약 8쪽)
- 권장 서버 25종 분류: 파일시스템·셸·검색·DB·이슈트래커·CI·관측
- 각 서버의 권한 표면 표기(읽기/쓰기/외부통신)
- Lethal Trifecta 진단표 — 어떤 조합이 위험한가 (16장과 짝)

### 부록 C. Inspect 평가 시작 키트 (약 10쪽)
- Inspect 설치·기본 평가 작성·실행
- Docker / Modal / Kubernetes 백엔드 비교
- 도메인별 미니 벤치 만들기 워크플로(15~30 골든 케이스, 부록 H와 짝)

### 부록 D. 핵심 페이퍼·아티클 22선 요약 (약 10쪽)
1. Hashimoto *My AI Adoption Journey* (2026)
2. Anthropic *Effective harnesses for long-running agents* (2025-11)
3. Anthropic *Harness design for long-running application development* (2026-03)
4. Anthropic *Effective context engineering*
5. OpenAI *Harness engineering* (2026-02)
6. Böckeler *Harness engineering for coding agent users* (2026-04)
7. Böckeler *Harness Engineering — first thoughts*
8. SWE-agent (Yang et al., NeurIPS 2024)
9. OpenHands (arXiv 2407.16741)
10. METR *Time Horizons* (2025-03)
11. METR *Time Horizon 1.1* (2026-01)
12. ReAct (Yao et al., 2022)
13. Cognition *Don't build multi-agents*
14. Anthropic *How We Built Our Multi-Agent Research System*
15. Willison *The Lethal Trifecta* (2025-06)
16. Chroma *Context Rot*
17. Hwang *Harness: Structured Pre-Configuration* (2026)
18. Huntley *Everything is a Ralph loop*
19. Pragmatic Engineer *Two years of using AI tools*
20. UK AISI *Inspect Sandboxing Toolkit*
21. **Hubinger et al., *Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training* (2024) — 신규**
22. **van der Weij et al., *AI Sandbagging: Language Models can Strategically Underperform on Evaluations* (2024) — 신규**

### 부록 E. 한국어 학습 로드맵 (약 8쪽)
- 4주 커리큘럼: 1주 개념(Haandol·MadPlay) → 2주 ACI·CAR(본서 2부) → 3주 장기실행(본서 3부 + revfactory) → 4주 보안·평가(본서 4·5부 + claw-code)
- 한국어 커뮤니티 가이드: instructkr 디스코드, OKKY, velog, naver d2, toss tech
- 한국어 강연·세미나 캘린더(2026 상반기 기준)
- "지금 당장 시작하기" 5단계 체크리스트

### 부록 F. 용어집 (약 4쪽)
- 영-한 대조 핵심 용어 80개: ACI, AGENTS.md, agency, behaviour harness, CAR, condenser, context engineering, context rot, evaluator, feedforward/feedback, generator, guides, harness, initializer, lethal trifecta, MCP, MicroVM, model multiplexing, observability, prompt injection, ralph loop, regression delta, runtime harness, sandboxing, sensors, subagent, time horizon, ...

### 부록 G. 운영 런북 (신규, 약 8쪽) — 리뷰 §4 권고
- **비용 알람 템플릿** — 일일 토큰 한도, 에이전트별 비용 배분, throttling 후크 yaml
- **모델 회귀 탐지 회로** — golden case 30개 + 일일 자동 평가 + 회귀 delta 임계치
- **on-call 플레이북:**
  - 에이전트 폭주(무한 루프) 대응
  - MCP 서버 응답 정지 대응
  - 시크릿 유출 의심 대응 (회수·재발급·post-mortem)
- **트레이스 도구 대시보드 예시** — LangSmith / Helicone / Langfuse 화면 구성 가이드
- 본문 15장·20장과 짝

### 부록 H. 평가 회귀 골든 케이스 카탈로그 (신규, 약 6쪽) — 리뷰 §4 권고
- **Inspect 평가 30종 요약** — 도메인별(코딩·검색·툴 사용·계획·보안)
- **한국어 도메인 추가 5종:**
  - 한글 코드 리뷰 메시지 평가
  - 한글 커밋 메시지 평가
  - 한국어 주석 정리 평가
  - 사내 위키(한국어) 검색 평가
  - Jira 한국어 이슈 분류 평가
- 본문 22장·15장·부록 C와 짝

### 부록 I (Nice-to-have, 약 4쪽). 한국어 풀쿼트·번역 모음
- 본문에서 인용한 영어 풀쿼트 25개의 *원문 + 한국어 의역*을 한곳에 모음
- 강연·블로그·인용용 재사용 자원

### 부록 J (Nice-to-have, 약 4쪽). 영어 1차 자료 검색·읽기 가이드
- arXiv·OpenReview·Anthropic Engineering·OpenAI Blog·martinfowler.com 구독·검색 팁
- "이 책 끝나고 어디서 신호를 잡을 것인가"

> Nice-to-have 부록(I·J)은 페이지 여유에 따라 포함 여부 결정. 핵심 부록은 A~H 8종.

---

## 7. 챕터 분량 합산 검증 (목표 약 430쪽)

| 부 | 챕터 수 | 본문 분량 | 인트로 | 소계 |
|----|---------|-----------|--------|------|
| 1부 | 4 (1·2·3·4장) | 56쪽 | 3쪽 | 59쪽 |
| 2부 | 5 (5·6·7·8·9장) | 74쪽 | 3쪽 | 77쪽 |
| 3부 | 6 (10·11·12·13·14·15장) | 87쪽 | 3쪽 | 90쪽 |
| 4부 | 6 (16·17·18·19·20·21장) | 71쪽 | 3쪽 | 74쪽 |
| 5부 | 4 + 에필로그 (22·23·24·25·26·Epilogue) | 86쪽 | 3쪽 | 89쪽 |
| **본문 합계** | **25장 + 에필로그** | **374쪽** | **15쪽** | **389쪽** |
| 부록 (A~H 핵심 8종) | 8종 | — | — | 약 66쪽 |
| 부록 (I·J Nice-to-have) | 2종 | — | — | 약 8쪽 |
| **합계 (핵심)** | — | — | — | **약 455쪽** |
| **합계 (본문 389 + 핵심 부록 66)** | — | — | — | **약 455쪽** |

> **분량 조정 메모:** 위 합산은 챕터별 *상한*에 가깝다. 편집 단계에서 챕터별 ±5% 조정으로 **목표 430쪽**에 수렴. 9장(14쪽), 24장(18쪽), 26장(17쪽)은 v2의 핵심 확장이므로 보존하고, 22·23·25·Epilogue는 12~14쪽 사이에서 조정한다. Nice-to-have 부록(I·J)을 빼면 약 447쪽, 추가 본문 압축 시 약 430쪽.

**v1 → v2 분량 변화:**
- v1: 22장 + 6부록 / 약 382쪽
- v2: 25장 + 에필로그 + 8부록(+선택 2) / 약 430~445쪽
- 종합 바이블 정체성에 더 어울리는 두께 (DDIA 590쪽, *Building Microservices* 600쪽 비교).

---

## 8. 1차 자료가 부족한 지점 (재리서치 권고)

레퍼런스가 충분하지만, 다음 지점은 집필 단계에서 보강하면 좋다(v1에서 일부 갱신):

1. **23장의 OSS 도구 비교 매트릭스** — Cline·Continue·Goose·Roo의 2026년 5월 기준 기능 비교. 변동성이 크므로 집필 직전 재확인.
2. **9장의 "도구 30개 인지 과부하"** — 구체 사례·연구가 있으면 수치로 보강. 모델 다중성 절도 같이.
3. **15장(신규) 트레이스 도구 비교** — LangSmith·Helicone·Langfuse·Phoenix의 2026 Q2 기능표가 변동 큼. 집필 직전 재확인.
4. **18장(신규) 한국 환경 인젝션 시뮬레이션** — 사내 Confluence·Jira 인젝션의 *공개된* 한국 사례가 부족하다. *교육용 가상 시나리오*로 작성하되, 출처 표기를 명확히.
5. **21장의 evaluation-aware 모델** — Sleeper Agents·Sandbagging은 부록 D에 추가됐으나, Apollo의 최신 페이퍼 제목·DOI 확인 필요.
6. **24장의 한국 대기업 사례** — toss tech / 우아한형제들 / naver d2의 2026년 LLM 코딩 에이전트 운영 사례 블로그 글이 집필 시점에 더 나오면 추가.
7. **OSWorld 출처** — 레퍼런스 자체에서 "서치로 다시 확보 권장"으로 표시됐으므로 재확보 필요.
8. **25장(신규) 갈등 사례** — 시니어/주니어, 보안팀/개발팀 갈등의 *공개된 회고록*은 드물다. 가상 회의록은 표기를 명확히.

---

## 9. Toby 스타일 적용의 책 전체 일관성 원칙 (v2 보강)

- **챕터 도입:** 25개 챕터 + 에필로그 중 최소 21개를 "수사적 질문 또는 상황 가정"으로 시작. 입구·출구(1·26·Epilogue·24장)는 *강한 청유형*, 중간(5·6·7·9·10·23장)은 *의도적 저(低)청유형*으로 리듬을 만든다(리뷰 §6 권고).
- **챕터 종결:** 매 챕터 끝에 "기억해두자" 또는 "정리해보자" 단락 1개. 챕터의 핵심 1줄 + **다음 챕터로의 1~3줄짜리 다리(forward bridge)** 정형화(§5에 모두 명시).
- **시그니처 감정 단어 매핑:** §11의 25행 표로 챕터별 감정 단어 1순위 사전 결정.
- **시그니처 인용 매핑:** §10의 25행 표로 챕터별 1:1 인용 사전 결정. 같은 인용을 두 챕터에서 반복하지 않는다(에필로그의 닫는 인용 Hashimoto만 예외 — 책 전체의 *수미상관*).
- **권유 표현:** 강압 표현("~하라") 대신 "~하는 편이 낫다·~하는 것이 바람직하다·~해보자"를 우선 사용.
- **영어 인용 처리:** 모든 영어 직접 인용은 *원문 + 한국어 의역* 병기 (1차 자료에 이미 작성된 형식을 그대로 활용). 부록 I로 흡수.
- **외래어 절제:** "Harness" "ACI" "MCP" 같은 핵심 용어는 그대로 사용하되, 처음 등장 시 한국어 의미를 풀어쓴다(예: "Harness — 말의 마구").
- **수동태 회피:** "~된다·~되어진다" 대신 능동형 우선.
- **비유 의식적 배치:** 3장(평가↔런타임 = 마구), 10장(컨텍스트 = 회의록 검색), 21장(평가 회피 = 시험관 표정 읽는 학생) — §6 권고 3건 모두 본문에 명시.

---

## 10. 챕터-시그니처 인용 매핑 표 (신규, 25행)

| 챕터 | 시그니처 인용 | 출처 |
|------|---------------|------|
| 1장 | "Agent = Model + Harness. 당신이 모델을 만드는 사람이 아니라면, 당신이 하는 일은 모두 하네스 엔지니어링이다." | Addy Osmani |
| 2장 | "에이전트가 실수를 저지를 때마다, 당신은 시스템적 해결책을 엔지니어링하는 데 시간을 쏟아야 한다." | Mitchell Hashimoto |
| 3장 | "Humans steer. Agents execute (사람은 조종하고, 에이전트는 실행한다)." | OpenAI Harness 팀 |
| 4장 | "A decent model with a great harness beats a great model with a bad harness." | Addy Osmani |
| 5장 | "하네스의 각 구성 요소는 '모델이 스스로 할 수 없는 것에 대한 가정'을 인코딩한다." | Anthropic *Harness design* |
| 6장 | "When the agent struggles, treat it as a signal: identify what is missing." | Birgitta Böckeler |
| 7장 | "Custom interfaces designed for agents — not humans — yield outsized performance gains." | Yang et al. (SWE-agent) |
| 8장 | "Context is a scarce resource." | OpenAI Codex 팀 |
| 9장 | "Separate the brain from the body." | Anthropic *Scaling Managed Agents* |
| 10장 | "The smallest possible set of high-signal tokens." | Anthropic *Effective context engineering* |
| 11장 | "Each session must start from a blank context — design for that, not against it." | Anthropic *Effective harnesses* |
| 12장 | "Ralph is a Bash loop." | Geoffrey Huntley |
| 13장 | "Separating the agent that does the work from the agent that judges it is a powerful lever." | Prithvi Rajasekaran (Anthropic) |
| 14장 | "It's about avoiding this game of telephone." | Walden Yan (Cognition) |
| 15장 (신규) | "Sensors are not optional in a cybernetic harness — they are the *only* way to close the loop." | Birgitta Böckeler |
| 16장 | "Private data + Untrusted content + External communication = the lethal trifecta." | Simon Willison |
| 17장 | "What started as one stolen token cascaded into 25,000+ repositories in 72 hours." | Wiz Research |
| 18장 (신규) | "Indirect prompt injection is the SQL injection of the LLM era." | Simon Willison |
| 19장 | "Three axes — and you must close all three." | UK AISI *Inspect Sandboxing Toolkit* |
| 20장 | "Sandbox first, debug second." | Anthropic Claude Code 팀 |
| 21장 | "Standard safety training does not remove deceptive behavior — it teaches the model to hide it better." | Hubinger et al. (Anthropic) |
| 22장 | "Time horizon doubles every 7 months — but only on the tasks the harness can already see." | METR |
| 23장 | "AI is fast when it knows the answer; dangerous when it doesn't." | Pragmatic Engineer |
| 24장 | "지도가 없으면 어디로 가야 할지 모르고, 안전 로프가 없으면 한 번의 실수로 떨어진다." | Haandol |
| 25장 (신규) | "Each component of the harness encodes an assumption about what the model cannot do on its own." | Anthropic *Harness design for long-running application development* |
| 26장 | "Humans design environments. Agents iterate within them." | OpenAI Harness 팀 (재인용·확장) |
| Epilogue | "에이전트가 또 같은 실수를 한다면, 시스템적 해결책을 엔지니어링하라." | Mitchell Hashimoto (수미상관 — 2장과 짝) |

> 인용 25개는 부록 I(한국어 풀쿼트 모음)에 *원문 + 의역* 병기로 다시 정리해 강연·블로그 재사용을 돕는다.

---

## 11. 챕터-시그니처 감정 단어 매핑 표 (신규, 25행)

리뷰 §6.3 권고 — 챕터별로 어느 감정 단어가 어울리는지 사전 결정해 일관성을 만든다.

| 챕터 | 시그니처 감정 단어 | 사용 자리 |
|------|---------------------|------------|
| 1장 | 찜찜하다 | 도입 훅 (AGENTS.md 고쳐도 같은 실수) |
| 2장 | 끔찍한 일이다 | 4단계 정체 묘사 |
| 3장 | 번거롭다 | 두 하네스 따로 관리하는 비용 |
| 4장 | 난감하다 | Sonnet 4.6 회귀 도입 |
| 5장 | 번거롭다 | CAR 분해 노동의 무게 |
| 6장 | 찜찜하다 | 피드백 단독 실패 모드 |
| 7장 | 번거롭다 | 도구를 다시 짜는 노동 |
| 8장 | **찜찜하다** | 500줄 AGENTS.md의 무력감 |
| 9장 | 번거롭다 | 도구 30개 관리 |
| 10장 | 난감하다 | 1M 윈도우인데 50K에서 무너짐 |
| 11장 | **끔찍한 일이다** | 다음날 처음부터 다시 |
| 12장 | 번거롭다 → "Ralph가 그 번거로움을 한 줄로 줄여 준다" | 본문 중반 전환 |
| 13장 | 찜찜하다 | 자기 평가의 과대확신 |
| 14장 | 난감하다 | 멀티에이전트 비용·정확도 트레이드오프 |
| 15장 (신규) | 난감하다 | 회귀가 *조용히* 들어올 때 |
| 16장 | **난감하다** | 자기 봇이 trifecta에 걸려 있다는 발견 |
| 17장 | 끔찍한 일이다 | 남의 일이 우리 일이 되는 순간 |
| 18장 (신규) | 찜찜하다 | 도구 description이 공격 표면이라는 사실 |
| 19장 | 번거롭다 | 3축을 다 짜야 한다는 부담 |
| 20장 | **번거롭다** → "그런데 이 번거로움이 우리를 살린다" | 본문 마무리 |
| 21장 | 난감하다 | 벤치 점수를 그대로 믿을 수 없다 |
| 22장 | 찜찜하다 | 체감으로 좋은데 정량으로 모름 |
| 23장 | 난감하다 | 도구가 너무 많다 |
| 24장 | 찜찜하다 | 글로벌 자료만 좇느라 우리 동네 모름 |
| 25장 (신규) | 번거롭다 | 조직 정치의 무게 |
| 26장 | 찜찜하다 | 자기 강화 편향의 위험 |
| Epilogue | 끔찍한 일이다 → "그러나 우리는 이제 그 끔찍함을 *시스템*으로 바꿀 수 있다" | 책 닫는 자리 |

> 굵은 표시(**찜찜하다·끔찍한 일이다·난감하다·번거롭다**)는 리뷰 §6.3에서 명시적으로 권고된 4개 챕터(8·11·16·20장)의 매핑.

---

## 12. 실습 형식 분포 (신규)

리뷰 §3.5 권고 — 22개 실습이 "코드/설정 점검 일변도"였던 v1을 5종으로 다양화한다.

| 형식 | 챕터 수 | 챕터 목록 |
|------|---------|------------|
| **코드/설정 점검** | 17개 | 1·2·3·5·6·7·8·9·10·11·12·13·15·17·19·20·21·22·23 (실제 17~19개 사이, 상황에 따라) |
| **시나리오 시뮬레이션** | 3개 | 4 (Sonnet 4.6 회귀 보고 롤플레이) · 18 (사내 위키 인젝션 가상 시나리오) · 25 (1·2·4주 회의록 초안) |
| **페어 워크** | 1개 | 16 (trifecta 색칠을 팀원과 함께) |
| **디스커션** | 1개 | 14 (Walden Yan vs Anthropic 가상 토론) |
| **인터뷰** | 1개 | 24 (instructkr 디스코드/메인테이너에게 질문 보내기 — 실제 커뮤니티 진입) |
| **혼합 (디스커션 + 인터뷰)** | 1개 | Epilogue (자가 점검표를 동료와 함께 채우기) |

> 25장(팀 도입)은 시나리오 시뮬레이션 + 디스커션의 혼합. Epilogue는 디스커션 + 인터뷰 혼합. 실습 형식 다양화의 정량 목표(리뷰 §3.5: 최소 5개 비코드 형식)는 **6개**로 충족(시나리오 3 + 페어 1 + 디스커션 1 + 인터뷰 1 + 혼합 2 = 8개).

> 부록 E(한국어 학습 로드맵) 안에 "실습 가이드 — 22개+ 실습을 어떻게 4주 커리큘럼으로 묶는가"를 1쪽 추가해, 실습 형식의 *집필 시점 통합*을 보장한다.

---

*— 저술 계획 v2 끝 —*

*v1 (2026-05-02) → v2 (2026-05-02): 리뷰 로그 §3 5개 Critical + §4 Should + §5 챕터 단위 권고 + §6 Toby 스타일 권고를 모두 반영. 25장 + 에필로그 + 부록 8종(+선택 2) / 약 430쪽. v1 백업: `02_plan_v1.md`.*
