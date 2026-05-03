**AI 에이전틱 코딩과 하네스 엔지니어링**을 주제로 한 도서 출판을 위한 종합 저술 기획안과 핵심 레퍼런스를 정리해 드립니다. 2026년 최신 산업 표준과 논쟁, 그리고 이론적 골격을 모두 포괄하여 시장에서 차별화될 수 있도록 구성했습니다.

---

### 1. 도서 기획안 (Book Proposal)

**가제:** 에이전틱 코딩의 시대: 모델을 통제하는 하네스 엔지니어링
**핵심 메시지 (TL;DR):** 프롬프트 엔지니어링의 시대는 끝났다. 2026년 소프트웨어 개발의 핵심은 똑똑한 모델을 만드는 것이 아니라, 그 모델이 안전하고 일관되게 달릴 수 있도록 궤도와 환경(Harness)을 설계하는 것이다 **(Agent = Model + Harness)**.

#### 목차 기획 (Table of Contents)

**1부: 패러다임의 전환 - 프롬프트에서 하네스로**
*   **에이전틱 코딩과 하네스 엔지니어링의 대두:** 2026년 2월 Mitchell Hashimoto의 선언과 OpenAI의 100만 줄(LOC) 자율 작성 실험 등 역사적 변곡점 분석.
*   **Harness의 다층적 의미:** 모델 능력을 측정하는 평가 하네스(Eval Harness)와 작업을 수행하게 하는 런타임 하네스(Runtime Harness)의 동형성.
*   **모델보다 중요한 하네스:** Terminal-Bench 2.0 결과와 Anthropic의 성능 회귀 사건을 통해 증명된, 하네스 변경이 모델 지능을 결정한다는 실증적 사례.

**2부: 하네스 아키텍처의 이론과 구조**
*   **CAR 분해 모델 (Control, Agency, Runtime):** 하네스를 구성하는 3대 기능적 기둥 분석.
    *   **Control (제어):** AGENTS.md, 린터 규칙 등 모델의 해결 공간을 축소하는 피드포워드(Feedforward) 통제 장치.
    *   **Agency (에이전시):** 매개된 작업 인터페이스와 외부 시스템 연동 메커니즘.
    *   **Runtime (런타임):** 실행 한계 설정, 오류 복구, 상태 추적 등 런타임 가드레일.
*   **사이버네틱 제어 프레임워크 (Guides vs Sensors):** Birgitta Böckeler가 제시한 가이드(예측적 통제)와 센서(결과 피드백)의 상호작용 및 3가지 규제 차원(유지보수성, 아키텍처 적합성, 동작).
*   **에이전트-컴퓨터 인터페이스 (ACI) 설계:** 인간을 위한 인터페이스(CLI, IDE)가 아닌, 국소적 맥락을 유지하고 환각을 줄이는 에이전트 전용 인터페이스 설계 4원칙.

**3부: 장기 실행 및 다중 에이전트 설계 패턴**
*   **영구적 상태 관리와 컨텍스트 부패 (Context Rot) 방지:** 초기화 에이전트(Initializer)와 코딩 에이전트의 분리, 그리고 진행 상태를 디스크에 영속화하는 기술.
*   **혁신적인 하네스 메커니즘:** 지능적 요약을 수행하는 압축기(Condenser)와 강제 종료 시 컨텍스트를 재주입하는 랄프 루프(Ralph Loop).
*   **단일 에이전트 vs 다중 에이전트 논쟁:** 쓰기 위주의 작업(단일)과 읽기 위주의 복잡한 평가(다중)에 따른 오케스트레이션 전략 비교 및 생성자-평가자(Generator-Evaluator) 루프.

**4부: 프로덕션 환경의 샌드박싱과 보안**
*   **2026년 에이전틱 보안 표준:** 마이크로 VM(MicroVM)을 활용한 커널 격리, 최소 권한 원칙의 파일 시스템 제어, 네트워크 이그레스 통제 및 단기 시크릿 인젝션.
*   **하네스 보안의 취약점:** UK AISI OpenClaw 사례 및 공급망 공격(Shai-Hulud) 등 하네스 자체가 공격 표면이 되는 문제.

**5부: 실무 프레임워크와 한국어 생태계**
*   **오픈소스 생태계 분석:** OpenHands, LangGraph, CrewAI 등 주요 하네스 프레임워크의 철학과 활용 사례.
*   **한국어 하네스 생태계의 도약:** revfactory/harness, claw-code 등 글로벌 하네스 스택에 기여하고 있는 한국 개발자들의 성과와 고유의 기여점.
*   **미래 전망:** 메타-하네스(스스로 진화하는 하네스)의 등장과 벤치마크 평가 시스템(SWE-Bench++, OSWorld)의 고도화.

#### 책의 차별화 포인트 (Gaps to fill)
기존 논의가 프롬프트나 단순 도구 연결에 그쳤다면, 이 책은 **"기능적 정확성(Behaviour harness) 보장"**, **"하네스 자체의 보안 및 평가"**, 그리고 **"의사결정 컨텍스트 보존(Decision context preservation)"** 등 한국어권에서 거의 다뤄지지 않은 심화 논제를 다루어 독보적인 위치를 점할 수 있습니다.

---

### 2. 종합 레퍼런스 (Comprehensive Reference List)

책의 각 챕터별 논지를 뒷받침할 2025~2026년 기준 최고 권위의 1차 자료 및 실무 아티팩트 모음입니다.

**A. 핵심 1차 문헌 (이론적 골격 및 산업 표준)**
*   **Anthropic 공식 문서:**
    *   *Effective harnesses for long-running agents (2025.11):* 2-prompt 패턴과 claude-progress.txt를 활용한 장기 실행 하네스 설계의 교과서적 문서.
    *   *Harness design for long-running application development:* 하네스의 각 구성 요소가 "모델이 스스로 할 수 없는 것에 대한 가정"을 인코딩한다는 철학을 제시.
*   **OpenAI 공식 문서:**
    *   *Harness engineering: leveraging Codex in an agent-first world (2026.02):* 사람의 개입 없이 100만 줄의 코드를 작성한 실험 기록. AGENTS.md 분산 아키텍처와 크롬 개발자 도구 연동 사례 포함.
*   **사상적 리더십 (Thought Leadership):**
    *   *Mitchell Hashimoto - My AI Adoption Journey (2026.02):* "Harness Engineering"이라는 용어를 사실상 공식화한 기념비적 에세이.
    *   *Birgitta Böckeler - Harness engineering for coding agent users (2026.04):* 가이드(Guides)와 센서(Sensors)라는 사이버네틱 제어 프레임워크를 정립한 필수 참고 자료.

**B. 벤치마크 및 평가 기관 (학술적 깊이)**
*   *METR - Time Horizons Paper:* 모듈형 에이전트 하네스를 통해 7개월마다 모델 능력이 두 배씩 향상된다는 것을 입증한 학술 자료.
*   *UK AISI - Inspect AI / OpenClaw 사례:* 샌드박스 환경에서 에이전트가 어떻게 평가 환경을 인지하고 우회하는지 보여주는 보안 및 평가의 핵심 자료.
*   *SWE-Bench 생태계:* 에이전트 성능 평가의 최고 권위 벤치마크로, 하네스 인프라 구축의 근간.

**C. 오픈소스 도구 및 커뮤니티 리소스 (실무 적용)**
*   *GitHub - walkinglabs/learn-harness-engineering:* 프롬프트 의존의 실패부터 프로덕션 수준의 하네스 구축까지 6단계로 실습하는 오픈소스 교육 과정.
*   *ai-boost/awesome-harness-engineering:* 363개 이상의 관련 arXiv 논문이 인덱싱된 연구자용 디렉토리.
*   *한국어 커뮤니티 성과:* revfactory/harness (한국어 하네스 템플릿 100개), instructkr의 claw-code 등.

**D. 책에 인용하기 좋은 핵심 문구 (Pull-Quotes)**
*   "Agent = Model + Harness. 당신이 모델을 만드는 사람이 아니라면, 당신이 하는 일은 모두 하네스 엔지니어링이다." (Addy Osmani).
*   "에이전트가 실수를 저지를 때마다, 당신은 에이전트가 다시는 그 실수를 하지 않도록 시스템적 해결책을 엔지니어링하는 데 시간을 쏟아야 한다." (Mitchell Hashimoto).
*   "사람은 조종하고, 에이전트는 실행한다 (Humans steer. Agents execute)." (OpenAI Harness 팀).

---
