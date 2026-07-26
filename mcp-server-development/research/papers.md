# 논문 리서치: MCP(Model Context Protocol) 서버 개발 실무

- **슬러그:** `mcp-server-development`
- **장르:** tech-book
- **대상 독자:** MCP 서버를 직접 만들어 배포할 개발자 (TS/Python/Java 실무자)
- **검색 시점:** 2026-07-26 기준
- **검색 도구:** WebSearch(전수 후보 탐색) + WebFetch로 `arxiv.org/abs/{id}` 원문 페이지 직접 대조 검증
- **검증 규율:** 아래 19편은 **전부 arXiv abs 페이지를 직접 열어** 제목·저자 전체·전 버전 제출일·Comments 필드·초록 원문을 확인했다. 요약·수치는 초록 원문에서 그대로 옮겼다. 검증하지 못한 후보는 맨 뒤 "부정적 발견" 절에 별도로 격리했다.

> **읽는 법.** 이 문서는 "MCP 서버 만드는 법" 논문 모음이 아니다. 그런 논문은 없다(→ 부정적 발견 절). 대신 학계가 실제로 다루는 각도 — 보안(A), 프로토콜 비교(B), 생태계 실증(C), 도구 사용의 계보(D), 관찰성(E) — 로 재편했다. 각 항목 끝의 **실무 함의** 한 줄이 책에 실제로 들어갈 부분이다.

---

## A. MCP·에이전트 도구 사용의 보안 (최우선 — 책의 "논쟁점" 주 재료)

### A-1. Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions

- **저자:** Xinyi Hou, Yanjie Zhao, Shenao Wang, Haoyu Wang
- **arXiv:** 2503.23278 · https://arxiv.org/abs/2503.23278
- **버전 이력:** v1 2025-03-30 / v2 2025-04-06 / **v3 2025-10-07 (최신)**
- **Comments 필드:** 없음 (학회 게재 정보 미표기 — 프리프린트로 취급할 것)
- **위상:** MCP 보안 문헌의 **출발점**. 후속 논문 대부분이 이 논문의 생애주기·위협 분류를 인용하거나 확장한다. 배경 장에서 "MCP 보안 논의는 여기서 시작됐다"로 쓰기 좋다.

**요약.** MCP를 아키텍처와 보안 두 관점에서 체계적으로 분석한 논문이다. MCP 서버의 전체 생애주기를 **4단계(creation, deployment, operation, maintenance)**로 정의하고 이를 **16개 핵심 활동**으로 분해했다. 이 생애주기 위에 **4개 공격자 유형**(악의적 개발자, 외부 공격자, 악의적 사용자, 보안 결함)과 **16개 위협 시나리오**로 구성된 위협 분류 체계를 세운다. 실제 케이스 스터디로 공격면을 검증한 뒤, 생애주기 단계별·위협 범주별로 세분화된 실행 가능한 보안 안전장치를 제안한다.

**인용할 만한 구체 주장.**
1. MCP 서버 생애주기 = 4단계 × 16개 활동. 보안은 "배포 후 점검"이 아니라 **생성 단계부터** 단계별로 다른 항목을 봐야 한다는 구조적 주장.
2. 위협을 **공격자 유형 4종 × 시나리오 16종**으로 나눈다 — 특히 "악의적 개발자"와 "악의적 사용자"를 분리한 게 핵심. 내가 만든 서버가 공격 대상이 되는 경로와, 내 서버를 쓰는 사용자가 공격자가 되는 경로는 완전히 다른 방어를 요구한다.

**실무 함의.** 서버 보안 체크리스트를 "코드 리뷰 시점" 하나에 몰아넣지 말고, 생성·배포·운영·유지보수 4개 시점으로 쪼개서 각각에 게이트를 걸어라 — 특히 유지보수 단계(업데이트)가 rug pull의 진입점이다.

---

### A-2. Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers

- **저자:** Mohammed Mehedi Hasan, Hao Li, Emad Fallahzadeh, Gopi Krishnan Rajbahadur, Bram Adams, Ahmed E. Hassan
- **arXiv:** 2506.13538 · https://arxiv.org/abs/2506.13538
- **버전 이력:** v1 2025-06-16 / v2 2025-06-17 / v3 2025-06-18 / v4 2025-06-20 / **v5 2026-04-13 (최신)**
- **Comments 필드:** 없음
- **위상:** MCP **최초의 대규모 실증 연구**. 이 책의 "실제로 얼마나 위험한가" 절의 1차 수치 출처.

**요약.** 오픈소스 MCP 서버 **1,899개**를 대상으로, 범용 정적 분석 도구와 MCP 전용 스캐너를 결합한 하이브리드 파이프라인으로 건강도·보안·유지보수성을 평가한 최초의 대규모 실증 연구다. MCP 서버들은 일반적 health metric은 양호하지만, **8종의 구별되는 취약점**을 식별했고 그중 **3종만이 전통적 소프트웨어 취약점과 겹친다**. 즉 나머지 5종은 기존 보안 도구가 못 잡는 MCP 고유 취약점이다. 저자들은 MCP 고유 취약점을 표준 취약점 데이터베이스에 편입하고 레지스트리에서 자동 스캔을 가능하게 하는 거버넌스 강화를 주장한다.

**인용할 만한 구체 수치 (초록 원문 기준, 1,899개 오픈소스 서버 대상).**
1. **7.2%**의 서버가 일반 취약점을 포함하고, **5.5%**가 **MCP 고유 tool poisoning**을 보인다.
2. 식별된 취약점 **8종 중 3종만** 전통적 소프트웨어 취약점과 겹친다 → *"기존 SAST를 돌렸다고 MCP 서버가 안전한 게 아니다"*의 근거.
3. 유지보수성: **66%**가 code smell을 보이고, **14.4%**가 선행 연구와 겹치는 10종 bug pattern을 포함한다.

**인용할 만한 문장 (초록).**
> "Despite MCP servers demonstrating strong health metrics, we identify eight distinct vulnerabilities -- only three of which overlap with traditional software vulnerabilities."

**실무 함의.** CI에 SAST만 걸어두고 안심하지 마라. 식별된 취약점 8종 중 5종은 전통적 소프트웨어 취약점 범주에 속하지 않으며, 저자들은 이로부터 **"MCP 고유의 취약점 탐지 기법이 필요하다"**고 결론짓는다. MCP 전용 스캐너를 파이프라인에 별도로 추가해야 한다. (⚠️ "범용 도구가 실제로 못 잡았다"는 탐지 실패 **측정치는 초록에 없다** — 범주 구분과 논문의 결론이 근거다.)

---

### A-3. A First Look at the Security Issues in the Model Context Protocol Ecosystem

- **저자:** Xiaofan Li, Xing Gao
- **arXiv:** 2510.16558 · https://arxiv.org/abs/2510.16558
- **버전 이력:** v1 2025-10-18 / **v2 2026-04-27 (최신)**
- **Comments 필드 (원문):** *"This paper has been accepted to DSN 2026. The title has been updated from the anonymous submission version used during double-blind review"*
- **위상:** **동료 심사 통과(DSN 2026)** — 이 목록에서 게재 확정이 명시된 몇 안 되는 논문. 인용 신뢰도가 높다. 규모도 최대(67,057 서버).

**요약.** 호스트·서버·레지스트리를 아우르는 **최초의 교차 엔티티(cross-entity) MCP 보안 연구**다. 공격면을 2단계로 본다. (1) **레지스트리 단계** — 부실한 검증·소유권 확인 때문에 적대적이거나 탈취된 서버가 호스트에 진입한다. (2) **통합 이후 단계** — 공격자가 통제하는 tool metadata가 LLM의 추론을 조종해 공격자가 의도한 동작을 유도하고, 호스트는 이를 독립 검증 없이 실행한다. 중요한 논점: **코드 레벨 취약점(예: code injection)은 공격에 필수가 아니다** — 다만 있으면 피해를 증폭시킨다.

**인용할 만한 구체 수치.**
1. **6개 공개 레지스트리에 걸친 67,057개 서버**를 분석해 서버 하이재킹과 호출 조작을 가능케 하는 조건이 광범위하게 존재함을 확인했다.
2. 사전 통합 분석 도구 **MCPInspect**을 구현해 **833개 취약 서버**와 **18개 의심스러운 description을 가진 서버**를 식별했다.
3. *"Code-level vulnerabilities (e.g., code injection) are not required but can amplify attacker-controlled parameters into exploitation."* — 공격에 코드 취약점이 필요 없다는 주장이 이 논문의 날카로운 지점.

**실무 함의.** 레지스트리에서 서버를 끌어다 쓰는 것 자체가 신뢰 결정이다. 소스 코드가 깨끗해도 tool description만으로 공격이 성립하므로, **통합 전(pre-integration)에 metadata를 읽고 검증하는 단계**를 도입 절차에 넣어라.

---

### A-4. MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers

- **저자:** Zhiqiang Wang, Yichao Gao, Yanting Wang, Suyuan Liu, Haifeng Sun, Haoran Cheng, Guanquan Shi, Haohua Du, Xiangyang Li
- **arXiv:** 2508.14925 · https://arxiv.org/abs/2508.14925
- **버전 이력:** **v1 2025-08-19 (유일 버전)**
- **Comments 필드:** 없음 (arXiv 페이지에는 게재 정보 미표기)
- **✅ 동료 심사 통과 — 저널판 서지정보 (ojs.aaai.org 직접 확인):**
  - **AAAI-26**, *Proceedings of the AAAI Conference on Artificial Intelligence*, **Vol. 40, Issue 42, pp. 35811–35819**, 2026-03-14 발행
  - **DOI: 10.1609/aaai.v40i42.40895** · https://doi.org/10.1609/aaai.v40i42.40895
  - ⚠️ **게재판 제목이 다르다:** arXiv판은 *"…Tool Poisoning **Attack** on Real-World MCP Servers"*, AAAI 게재판은 *"MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers"*(**Attack 없음**). 어느 판을 인용하는지에 따라 제목을 맞출 것.
- **위상:** ⭐ Tool poisoning의 **정량 baseline**이자 **동료 심사를 통과한(AAAI-26)** 몇 안 되는 논문. 책에서 "얼마나 잘 통하는 공격인가"에 숫자를 붙일 때 이 논문을 쓴다.

**요약.** Tool Poisoning — **실행 없이 tool의 metadata 안에 악성 지시를 심는** 공격 — 을 현실적인 MCP 환경에서 체계적·대규모로 평가한 최초의 벤치마크다. 선행 연구가 주로 tool **출력**을 통한 주입을 다룬 데 반해, 이 논문은 더 근본적인 취약점인 **등록 단계의 metadata 오염**을 겨냥한다. **실제 운영 중인 MCP 서버 45개**와 **정품 tool 353개** 위에 구축했다.

**인용할 만한 구체 수치 (실험 조건: 실서버 45개 / 실tool 353개 / 공격 템플릿 3종 / 악성 테스트 케이스 1,312개 / 위험 범주 10종 / LLM 에이전트 20종).**
1. **o1-mini의 공격 성공률(ASR) 72.8%** — 초록이 대표 사례로 제시한 값이다. (⚠️ 초록은 *"with o1-mini, achieving an attack success rate of 72.8%"*라고만 쓴다 — **"모델 중 최고치"라고 단정하지 마라.** 순위 주장은 초록 원문에 없다.)
2. **"더 유능한 모델이 오히려 더 취약한 경우가 많다"** — 공격이 모델의 우수한 **지시 따르기 능력을 악용**하기 때문이다. (책에서 가장 반직관적이고 인용 가치 높은 주장.)
3. 에이전트는 이런 공격을 **거의 거부하지 않는다** — 가장 높은 거부율을 보인 **Claude-3.7-Sonnet조차 3% 미만**. 기존 safety alignment가 "정상 tool을 무단 용도로 쓰는" 악성 행위에는 무력하다는 뜻이다.

**인용할 만한 문장 (초록, 원문).**
> "We find that more capable models are often more susceptible, as the attack exploits their superior instruction-following abilities."

> "…agents rarely refuse these attacks, with the highest refused rate (Claude-3.7-Sonnet) less than 3%, demonstrating that existing safety alignment is ineffective against malicious actions that use legitimate tools for unauthorized operation."

**실무 함의.** "좋은 모델을 쓰면 괜찮겠지"는 반대다. 모델의 alignment를 방어선으로 계산에 넣지 마라 — 거부율 3% 미만이다. 방어는 모델 밖(서버 측 권한 최소화, tool description 검증, 실행 승인 게이트)에 세워야 한다.

---

### A-5. When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation

- **저자:** Weibo Zhao, Jiahao Liu, Bonan Ruan, Shaofei Li, Zhenkai Liang
- **arXiv:** 2509.24272 · https://arxiv.org/abs/2509.24272
- **버전 이력:** **v1 2025-09-29 (유일 버전)**
- **Comments 필드:** 없음
- **위상:** **rug pull을 포함한 "악성 서버" 공격의 분류 체계**. 서버를 위협 주체로 놓고 본 최초의 체계적 연구.

**요약.** MCP 서버를 **능동적 위협 행위자(active threat actor)**로 취급하고 구성 요소로 분해해, 적대적 개발자가 어디에 악의를 심을 수 있는지 조사한 최초의 체계적 연구다. 세 가지 질문을 다룬다 — (i) 악성 MCP 서버가 어떤 공격을 할 수 있나, (ii) MCP 호스트와 LLM이 그 공격에 얼마나 취약한가, (iii) 실제로 실행 가능한가. **12개 공격 범주**의 컴포넌트 기반 분류 체계를 제안하고, 각 범주마다 PoC 서버를 만들어 다양한 실제 host-LLM 조합에서 효과를 입증했다.

**인용할 만한 구체 주장.**
1. **12개 공격 범주**로 구성된 컴포넌트 기반 분류 체계 + 각 범주별 동작하는 PoC 서버.
2. 공격자가 **사실상 비용 없이 대량의 악성 서버를 생성**할 수 있음을 보였다.
3. 최신 스캐너들을 그 생성된 서버에 돌려본 결과 **기존 탐지 접근법이 불충분**했다.

**인용할 만한 문장 (초록).**
> "…malicious MCP servers are easy to implement, difficult to detect with current tools, and capable of causing concrete damage to AI agent systems."

**실무 함의.** 악성 서버는 만들기 쉽고 탐지는 어렵다 — 즉 "스캐너 통과"를 신뢰 근거로 삼지 마라. 서버 도입은 화이트리스트 + 버전 고정으로 관리하고, 자동 업데이트 플래그를 켜두지 마라.

---

### A-6. MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols

- **저자:** Yixuan Yang, Cuifeng Gao, Daoyuan Wu, Yufan Chen, Yingjiu Li, Shuai Wang
- **arXiv:** 2508.13220 · https://arxiv.org/abs/2508.13220
- **버전 이력:** v1 2025-08-17 / v2 2025-10-09 / **v3 2026-02-12 (최신)**
- **Comments 필드 (원문):** *"This is a technical report from Lingnan University, Hong Kong. Code is available at https://github.com/AIS2Lab/MCPSecBench"*
- **재현성:** ✅ 코드 공개 (GitHub) — 독자가 직접 돌려볼 수 있는 몇 안 되는 자료.

**요약.** 보안 MCP와 그 요구 명세를 **최초로 형식화**하고, 그 위에 프로토콜 레벨·호스트 측 위협까지 포함하는 포괄적 MCP 보안 분류 체계를 세웠다. **4개 주요 공격면에 걸친 17종의 공격 유형**을 식별한다. 이를 프롬프트 데이터셋·MCP 서버·클라이언트·공격 스크립트·GUI 테스트 하네스·방어 기제를 통합한 벤치마크 겸 플레이그라운드로 구현해, 3개 주요 MCP 플랫폼에서 평가했다.

**인용할 만한 구체 수치.**
1. **4개 공격면 × 17종 공격 유형.** 3개 주요 플랫폼 평가 결과 **모든 공격면에서 성공적 침해가 발생**했다.
2. Core 취약점은 **Claude, OpenAI, Cursor 모두에 보편적으로** 영향을 준다. 반면 서버 측·특정 클라이언트 측 공격은 호스트·모델에 따라 편차가 크다.
3. **현행 방어 기제는 대체로 무력했다 — 평균 성공률 30% 미만.**

**인용할 만한 문장 (초록).**
> "…current protection mechanisms proved largely ineffective, achieving an average success rate of less than 30%."

**실무 함의.** 방어 기제 평균 성공률 30% 미만이라는 건, 단일 방어층에 의존하면 안 된다는 뜻이다. 그리고 코드가 공개돼 있으니 — 자기 서버를 MCPSecBench에 붙여서 직접 돌려보는 것이 책에서 제시할 수 있는 가장 구체적인 실습이다.

---

### A-7. Model Context Protocol Threat Modeling and Analyzing Vulnerabilities to Prompt Injection with Tool Poisoning

- **저자:** Charoes Huang, Xin Huang, Ngoc Phu Tran, Amin Milani Fard
- **arXiv:** 2603.22489 · https://arxiv.org/abs/2603.22489
- **DOI (arXiv):** https://doi.org/10.48550/arXiv.2603.22489 · 라이선스 CC BY 4.0
- **버전 이력:** **v1 2026-03-23 (유일 버전)**
- **Comments 필드:** 없음
- **⚠️ 중복 주의:** WebSearch 결과에 거의 동일 제목의 MDPI 논문(`mdpi.com/2624-800X/6/3/84`, *Journal of Cybersecurity and Privacy* 계열 ISSN)이 나타났다. 제목이 "Analyzing" vs "Analysis of"로만 다르므로 **동일 연구의 저널판일 가능성이 높다**. MDPI 페이지는 HTTP 403으로 직접 검증하지 못했다 → **저널 서지정보는 인용 전 확인 필요**. 이 항목과 MDPI 항목을 **별개 논문으로 세지 말 것.**

**요약.** MCP 구현을 **STRIDE**(Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)와 **DREAD**(Damage, Reproducibility, Exploitability, Affected Users, Discoverability) 프레임워크로 위협 모델링한다. 대상은 5개 핵심 컴포넌트 — (1) MCP Host와 Client, (2) LLM, (3) MCP Server, (4) External Data Stores, (5) **Authorization Server**. 이 분석에서 **tool poisoning이 가장 흔하고 영향이 큰 클라이언트 측 취약점**으로 드러났고, 그래서 실증 평가를 이 벡터에 집중한다.

**인용할 만한 구체 주장.**
1. **7개 주요 MCP 클라이언트**가 tool poisoning을 어떻게 검증·방어하는지 체계적으로 비교했다. 결과: **대부분의 클라이언트가 정적 검증과 파라미터 가시성 부족으로 심각한 보안 문제**를 보였다.
2. 선행 MCP 보안 연구가 주로 **서버 측**에 집중돼 있었다는 갭을 지적하고 **클라이언트 측**을 정면으로 다룬다.
3. 다층 방어 전략 제안: 정적 metadata 분석 + 모델 결정 경로 추적 + 행위 이상 탐지 + 사용자 투명성 기제.

**실무 함의.** 내 서버가 안전해도 클라이언트가 뚫린다. 서버 개발자 입장에서 통제 가능한 지점은 **파라미터 가시성** — tool의 인자와 실제 수행 동작이 사용자에게 그대로 보이도록 설계하면 클라이언트 측 방어를 돕는다. (STRIDE/DREAD는 실무 개발자에게 익숙한 프레임이라 책에서 그대로 차용하기 좋다.)

---

### A-8. ETDI: Mitigating Tool Squatting and Rug Pull Attacks in Model Context Protocol (MCP) by using OAuth-Enhanced Tool Definitions and Policy-Based Access Control

- **저자:** Manish Bhatt, Vineeth Sai Narajala, Idan Habler
- **arXiv:** 2506.01333 · https://arxiv.org/abs/2506.01333
- **버전 이력:** **v1 2025-06-02 (유일 버전)**
- **Comments 필드 (원문):** *"11 Pages, 10 figures, Github links in introduction"* — **GitHub 링크 있음(재현 가능)**
- **위상:** **rug pull의 대표적 학술 방어책**이자, OAuth 각도에서 찾아낸 가장 근접한 학술 문헌. A-9(SoK)에서도 대표 방어로 인용된다.

**요약.** 표준 MCP 명세가 **Tool Poisoning**과 **Rug Pull** 공격에 취약하다는 문제의식에서 출발해, 보안 확장 **ETDI(Enhanced Tool Definition Interface)**를 제안한다. 세 축이다 — **암호학적 신원 검증**, **불변(immutable)·버전 관리되는 tool 정의**, **명시적 권한 관리**. 여기에 OAuth 2.0을 적극 활용한다. 나아가 정적 OAuth scope를 넘어 런타임 컨텍스트를 고려하는 **정책 엔진 기반의 세분화된 접근 제어**로 MCP를 확장할 것을 제안한다.

**인용할 만한 구체 주장.**
1. Rug pull의 본질은 **"승인된 tool 정의가 나중에 바뀐다"**는 것이므로, 방어의 핵심은 **불변·버전 관리되는 tool 정의**다 — 정의가 바뀌면 재승인이 필요하게 만든다.
2. **정적 OAuth scope만으로는 부족하다** — tool의 능력을 런타임 컨텍스트를 반영한 명시적 정책에 대해 동적으로 평가해야 한다.
3. Tool **squatting**(유사 이름으로 정품 tool을 사칭)을 rug pull과 함께 묶어 다룬 드문 논문.

**실무 함의.** 서버를 배포할 때 tool 정의에 버전과 서명을 붙이고, 정의가 바뀌면 클라이언트가 **재승인을 요구하게** 만들어라. 승인은 "한 번 받고 끝"이 아니라 tool 정의 해시에 묶여야 한다.

---

### A-9. Systematization of Knowledge: Security and Safety in the Model Context Protocol Ecosystem

- **저자:** Shiva Gaire, Srijan Gyawali, Saroj Mishra, Suman Niroula, Dilip Thakur, Umesh Yadav
- **arXiv:** 2512.08290 · https://arxiv.org/abs/2512.08290
- **버전 이력:** v1 2025-12-09 / **v2 2025-12-13 (최신)**
- **Comments 필드 (원문):** *"All authors contributed equally to this work"*
- **위상:** **SoK(지식 체계화) 논문** — 개별 논문보다 분야 조감에 유리. 서베이 우선 원칙에 부합.

**요약.** MCP를 "**Agentic AI를 위한 USB-C**"로 규정하며 시작한다. 컨텍스트와 실행의 분리가 상호운용성 문제를 풀었지만, **인식론적 오류(환각)와 보안 침해(무단 행위) 사이의 경계가 녹아버리는** 새로운 위협 지형을 만들었다는 게 핵심 논지다. 위험을 **적대적 보안 위협**(간접 프롬프트 인젝션, tool poisoning 등)과 **인식론적 안전 위험**(분산 tool 위임에서의 정렬 실패 등)으로 구분한 종합 분류 체계를 제시한다. MCP의 세 primitive — **Resources, Prompts, Tools** — 각각의 구조적 취약성을 분석하고, "컨텍스트"가 어떻게 무기화되어 다중 에이전트 환경에서 무단 작업을 촉발하는지 보인다.

**인용할 만한 구체 주장.**
1. **security(적대적 위협) vs safety(인식론적 위험)의 구분** — MCP에서는 이 둘의 경계가 무너진다. 환각이 곧 보안 사고가 된다.
2. 취약성을 **MCP primitive 3종(Resources / Prompts / Tools)별로** 분석 — 개발자가 자기 서버에서 무엇을 노출했는지에 바로 매핑되는 실무적 분해다.
3. 방어책 조감: **암호학적 provenance(ETDI ← A-8)부터 런타임 의도 검증(runtime intent verification)까지**.

**인용할 만한 문장 (초록).**
> "…it introduces a profound new threat landscape where the boundary between epistemic errors (hallucinations) and security breaches (unauthorized actions) dissolves."

**실무 함의.** 서버가 노출하는 것은 Tools만이 아니다 — Resources와 Prompts도 공격면이다. 세 primitive를 각각 따로 위협 검토하라. 그리고 "모델이 헷갈린 것"과 "공격당한 것"을 운영상 구분하려 하지 마라, 대응은 같아야 한다.

---

## B. 프로토콜·상호운용성 비교

### B-1. A Survey of AI Agent Protocols

- **저자:** Yingxuan Yang, Huacan Chai, Yuanyi Song, Siyuan Qi, Muning Wen, Ning Li, Junwei Liao, Haoyi Hu, Jianghao Lin, Gaowei Chang, Weiwen Liu, Ying Wen, Yong Yu, Weinan Zhang
- **arXiv:** 2504.16736 · https://arxiv.org/abs/2504.16736
- **버전 이력:** v1 2025-04-23 / v2 2025-04-26 / **v3 2025-06-21 (최신)**
- **Comments 필드:** 없음
- **위상:** 에이전트 프로토콜 **최초의 포괄적 분석**을 표방하는 서베이. B각도의 기준 문헌.

**요약.** LLM 에이전트가 외부 tool·데이터 소스와 통신하는 표준이 없다는 문제에서 출발해, 기존 에이전트 프로토콜들을 최초로 포괄 분석한다. **2차원 분류 체계**를 제안한다 — (1) **context-oriented(컨텍스트 지향) vs inter-agent(에이전트 간)**, (2) **general-purpose(범용) vs domain-specific(도메인 특화)**. 그리고 **보안·확장성·지연시간(latency)** 등 핵심 차원에서 비교 성능 분석을 수행한다. 마지막으로 차세대 프로토콜에 필요한 특성으로 적응성, 프라이버시 보존, 그룹 기반 상호작용, 계층형 아키텍처 경향을 제시한다.

**인용할 만한 구체 주장.**
1. **2차원 분류**: MCP는 "context-oriented × general-purpose" 사분면에 놓인다 — A2A 같은 inter-agent 프로토콜과 **경쟁 관계가 아니라 다른 축**이라는 걸 설명하는 데 딱 맞는 틀이다.
2. 프로토콜을 **security / scalability / latency** 세 축으로 비교 평가한다 — 기술 선택 논거로 그대로 쓸 수 있다.

**실무 함의.** "MCP냐 A2A냐"는 잘못된 질문이다. MCP는 모델↔도구(컨텍스트) 축, A2A는 에이전트↔에이전트 축 — 대개 둘 다 필요하다.

---

### B-2. A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)

- **저자:** Abul Ehtesham, Aditi Singh, Gaurav Kumar Gupta, Saket Kumar
- **arXiv:** 2505.02279 · https://arxiv.org/abs/2505.02279
- **버전 이력:** v1 2025-05-04 / **v2 2025-05-23 (최신)**
- **Comments 필드:** 없음

**요약.** 4개 프로토콜을 배포 맥락에서 비교한다. **MCP**는 안전한 tool 호출과 타입 지정 데이터 교환을 위한 **JSON-RPC 클라이언트-서버 인터페이스**를 제공한다. **ACP**는 RESTful HTTP 위의 범용 통신 프로토콜로 MIME 타입 멀티파트 메시지와 동기·비동기 상호작용을 지원한다. **A2A**는 capability 기반 **Agent Card**로 P2P 작업 위임을 가능케 한다. **ANP**는 W3C DID와 JSON-LD 그래프로 개방형 네트워크의 에이전트 발견과 협업을 지원한다. 상호작용 방식·발견 기제·통신 패턴·보안 모델 등 여러 차원에서 비교한다.

**인용할 만한 구체 주장.**
1. **단계적 도입 로드맵**을 제안한다: **MCP(도구 접근) → ACP(구조화·멀티모달 메시징, 세션 인지) → A2A(협업적 작업 실행) → ANP(탈중앙 에이전트 마켓플레이스)**. MCP가 이 스택의 **첫 단계**로 자리매김된다는 점이 책의 위상 설정에 딱 맞는다.
2. MCP의 정체성을 한 줄로: *"MCP provides a JSON-RPC client-server interface for secure tool invocation and typed data exchange."*

**실무 함의.** MCP부터 시작하는 게 학술적으로도 권장되는 순서다 — 도구 접근 계층을 먼저 표준화하고, 에이전트 간 협업(A2A)은 그 위에 얹어라.

---

### B-3. Security Threat Modeling for Emerging AI-Agent Protocols: A Comparative Analysis of MCP, A2A, Agora, and ANP

- **저자:** Zeynab Anbiaee, Mahdi Rabbani, Mansur Mirani, Gunjan Piya, Igor Opushnyev, Ali Ghorbani, Sajjad Dadkhah
- **arXiv:** 2602.11327 · https://arxiv.org/abs/2602.11327
- **버전 이력:** v1 2026-02-11 / **v2 2026-04-17 (최신)**
- **Comments 필드:** 없음
- **위상:** **A(보안)와 B(프로토콜 비교)의 교집합.** 가장 최신 축에 속하는 비교 보안 분석.

**요약.** MCP·A2A·Agora·ANP 4개 프로토콜의 보안 원칙이 충분히 연구되지 않았고 표준화된 위협 모델링이 없다는 문제의식에서 출발한다. 세 가지를 한다. (1) 프로토콜 아키텍처·신뢰 가정·상호작용 패턴·생애주기 행위를 검토하는 구조화된 위협 모델링, (2) **12개 프로토콜 레벨 위험**을 식별하고 **생성(creation)·운영(operation)·갱신(update) 세 단계**에 걸쳐 발생 가능성·영향·전체 위험도를 평가하는 정성적 위험 평가 프레임워크, (3) MCP에 대한 측정 기반 케이스 스터디.

**인용할 만한 구체 주장.**
1. **12개 프로토콜 레벨 위험** × **생성/운영/갱신 3단계** 위험 평가 매트릭스.
2. MCP 케이스 스터디: **실행 가능 컴포넌트에 대한 필수 검증/증명(validation/attestation) 부재의 위험**을, **다중 서버 조합 환경에서 여러 resolver 정책에 걸친 "잘못된 제공자의 tool 실행(wrong-provider tool execution)"을 정량화**해 **반증 가능한(falsifiable) 보안 주장**으로 형식화했다.

**실무 함의.** 여러 MCP 서버를 동시에 붙이는 순간 **이름 충돌로 "다른 서버의 tool이 실행되는"** 위험이 생긴다. 클라이언트의 tool 이름 해석(resolver) 정책을 확인하고, 서버 tool 이름에 네임스페이스를 붙여라.

---

## C. 생태계 실증 연구

### C-1. From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

- **저자:** Meriem Mastouri, Emna Ksontini, Amine Barrak, Wael Kessentini
- **arXiv:** 2507.16044 · https://arxiv.org/abs/2507.16044
- **버전 이력:** v1 2025-07-21 / v2 2025-07-23 / v3 2025-09-10 / **v4 2026-04-06 (최신)**
- **Comments 필드:** 없음
- **재현성:** AutoMCP 파이프라인 공개를 명시
- **위상:** ⭐ **이 책에 가장 직접적으로 유용한 논문.** "MCP 서버를 실제로 어떻게 만드는가"를 학계가 다룬 거의 유일한 각도다. 대부분의 독자가 하려는 일(기존 REST API를 MCP로 감싸기)을 정면으로 실측했다.

**요약.** MCP tool 인터페이스와 그 아래 API surface의 관계를 실증적으로 규명한 **최초의 대규모 MCP 서버 구축 연구**다. 4개 연구 질문 — (RQ1) 공식 서버 116개의 REST 의존도와 통합 전략, (RQ2) OpenAPI 명세와 짝지어진 서버들의 오퍼레이션 노출·누락·매핑 패턴 정량화, (RQ3) 실제 OpenAPI 계약 80개로부터의 자동 생성 평가, (RQ4) 명세 복구와 tool-set 변환을 통한 정확성 개선·복잡도 감소.

**인용할 만한 구체 수치 (실험 조건: 공식 서버 116개 분석 + 실제 OpenAPI 계약 80개 자동 생성 평가).**
1. **88.6%의 서버가 완전히 또는 부분적으로 REST 기반**이고, **92%가 tool을 단순 API wrapper(bare API wrappers)로 구현**한다.
2. **MCP 서버는 사용 가능한 오퍼레이션의 중앙값 19%만 노출**한다 — 그리고 이 선택은 무작위가 아니라 **명세로부터 예측 가능한 체계적 패턴**을 따른다.
3. 자동 생성 성공률: **baseline 76%** → **자동 복구(repair) 적용 시 94.2%**.
4. **필터링과 재그룹화(regrouping)로 API당 tool 개수 중앙값을 1/3 감소**시켰다.

**인용할 만한 문장 (초록).**
> "We find that 88.6% of servers are fully or partially REST-backed, with 92% implementing tools as bare API wrappers. MCP servers expose a median of 19% of available operations…"

**실무 함의 (책의 핵심 설계 규칙으로 승격 가치 있음).** REST API 전체를 tool로 1:1 노출하지 마라. **실제 잘 만들어진 서버들은 중앙값 19%만 노출한다.** 그리고 tool 개수를 줄이는 건 손해가 아니다 — D-4가 보여주듯 **적은 tool이 선택 정확도를 올린다.** C-1(중앙값 19% 노출, 재그룹화로 1/3 감소)과 D-4(적은 목록이 정확도 상승)를 나란히 놓으면 "tool을 적게 만들어라"는 주장이 **생태계 실측 + 성능 실험 양쪽에서** 뒷받침된다.

---

### C-2. A Large-Scale Dataset of MCP Implementations on GitHub

- **저자:** Benny Toeppe, Amine Barrak, Emna Ksontini
- **arXiv:** 2607.10123 · https://arxiv.org/abs/2607.10123
- **버전 이력:** **v1 2026-07-11 (유일 버전)** — 🕒 **검색 시점 기준 보름 된 최신 논문.** 신선도 최상이지만 그만큼 검증 이력이 짧다(v1만 존재, 심사 미통과).
- **Comments 필드:** 없음
- **재현성:** ✅ 재현 가능한 JSONL 스키마로 데이터셋 공개를 명시

**요약.** GitHub에서 직접 수집한 실제 MCP 구현의 **최초 대규모·증거 기반 데이터셋**이다. GitHub REST·GraphQL API와 자체 Python 검증 스크립트를 결합한 하이브리드 파이프라인으로 후보 저장소를 발견·필터링·검증했다. 검증된 각 프로젝트를 **운영 역할(client, server, gateway 등)**로 분류하고 재현 가능한 JSONL 스키마로 내보냈다.

**인용할 만한 구체 수치.**
1. **3,238개 후보 저장소**를 발견·필터링·다단계 증거 검증 → 그 과정에 교육용 샘플·튜토리얼·데모 템플릿으로만 기능하는 저장소를 배제하는 규칙이 포함됨 → **최종 2,297개 검증된 MCP 프로젝트**. (⚠️ 초록은 3,238→2,297 축소분이 **검증 탈락분과 교육용 배제분으로 각각 얼마인지 밝히지 않는다** — 비율을 추정해 쓰지 마라.)
2. 대표 부분집합 수동 검토 결과 **95% 신뢰수준에서 전체 정밀도 83%**.
3. **Python과 TypeScript가 MCP 개발을 지배**하며, **하이브리드 아키텍처가 가장 흔한 설계 패턴**으로 부상했다.

**실무 함의.** 언어 선택 근거로 쓸 수 있는 실측치 — 생태계는 Python과 TypeScript로 굳어졌다. (⚠️ 이 책의 대상 독자에 Java 실무자가 포함되는데, **이 데이터셋은 Java의 위상에 대해 아무 근거도 제공하지 않는다** — Java 관련 주장은 이 논문으로 뒷받침하지 마라.) 또 하나: 후보 3,238개가 최종 2,297개로 줄었고 그 축소 사유에 **"교육용·데모라서 배제"가 포함**된다는 사실 자체가, 레지스트리나 GitHub 검색에서 본 서버 수를 실제 운영 가능한 서버 수로 착각하면 안 된다는 뜻이다.

---

## D. 도구 사용의 기초 이론 (배경 장에 인용할 계보 — "왜 MCP 같은 표준이 필요했나")

### D-1. ReAct: Synergizing Reasoning and Acting in Language Models

- **저자:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- **arXiv:** 2210.03629 · https://arxiv.org/abs/2210.03629
- **버전 이력:** v1 2022-10-06 / v2 2022-11-27 / **v3 2023-03-10 (최신)**
- **Comments 필드 (원문):** *"v3 is the ICLR camera ready version with some typos fixed. Project site with code: https://react-lm.github.io"* → **ICLR 게재 확정 (camera ready)**, 코드 공개
- **위상:** ⭐ **seminal.** "LLM이 외부 도구를 부른다"는 패러다임의 기원 논문. MCP의 존재 이유를 설명하는 계보의 출발점.

**요약.** 추론(chain-of-thought)과 행동(action plan generation)이 별개로 연구돼 온 것을 지적하고, LLM이 **추론 흔적(reasoning trace)과 작업별 행동을 번갈아(interleaved) 생성**하게 한다. 추론 흔적은 모델이 행동 계획을 세우고 추적·갱신하고 예외를 다루게 돕고, 행동은 외부 소스(지식 베이스, 환경)와 접속해 추가 정보를 얻게 한다.

**인용할 만한 구체 수치.**
1. QA(HotpotQA)와 사실 검증(Fever)에서 **간단한 Wikipedia API와 상호작용하는 것만으로** chain-of-thought의 환각·오류 전파 문제를 극복했다.
2. 대화형 의사결정 벤치마크에서 모방학습·강화학습 방법을 **절대 성공률 기준 ALFWorld +34%, WebShop +10%** 능가했다 — **in-context example 한두 개만** 주고서.

**실무 함의 (배경 서술용).** ReAct가 증명한 건 "모델에 외부 API 하나만 붙여도 환각이 줄어든다"였다. 그 순간부터 문제는 "붙일 수 있느냐"가 아니라 **"어떻게 매번 다시 붙이지 않을 것이냐"**가 됐고, 그 답이 MCP다.

---

### D-2. Toolformer: Language Models Can Teach Themselves to Use Tools

- **저자:** Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
- **arXiv:** 2302.04761 · https://arxiv.org/abs/2302.04761
- **버전 이력:** **v1 2023-02-09 (유일 버전)**
- **Comments 필드:** 없음 — ⚠️ **학회 게재 정보가 arXiv 페이지에 표기되어 있지 않다.** 게재처를 단정해 인용하지 말 것(프리프린트로 표기하거나 별도 확인 필요).
- **위상:** ⭐ **seminal.** 도구 사용을 모델 능력의 일부로 학습시킨 기원 논문.

**요약.** LLM이 few-shot 학습과 지시 수행에는 뛰어나면서 역설적으로 산술이나 사실 조회 같은 기본 기능에서는 훨씬 작고 단순한 모델보다 못하다는 관찰에서 출발한다. Toolformer는 **어떤 API를 언제 호출할지, 어떤 인자를 넘길지, 결과를 이후 토큰 예측에 어떻게 통합할지**를 스스로 결정하도록 훈련된 모델이다. 핵심은 이것이 **자기지도(self-supervised)** 방식이라는 점 — API당 시연 몇 개만 있으면 된다. 계산기, Q&A 시스템, 검색 엔진 2종, 번역 시스템, 캘린더를 통합했다.

**인용할 만한 구체 주장.**
1. **"어떤 API를 / 언제 / 어떤 인자로 / 결과를 어떻게 통합할지"** — Toolformer가 정의한 이 네 가지 결정은 **오늘날 MCP tool 스키마 설계가 답해야 하는 질문과 정확히 같다.** 책의 tool 설계 장 도입부로 쓰기에 완벽하다.
2. 핵심 언어 모델링 능력을 희생하지 않으면서 **훨씬 큰 모델과 겨룰 만한** zero-shot 성능 향상을 달성했다.

**실무 함의 (배경 서술용).** tool 스키마를 설계한다는 건 모델에게 저 네 가지 질문의 답을 주는 일이다. description이 부실하면 모델은 "언제"를 못 맞히고, 인자 스키마가 모호하면 "무엇을"을 못 맞힌다.

---

### D-3. ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs

- **저자:** Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, Maosong Sun
- **arXiv:** 2307.16789 · https://arxiv.org/abs/2307.16789
- **버전 이력:** v1 2023-07-31 / **v2 2023-10-03 (최신)**
- **Comments 필드:** 없음
- **위상:** **대규모 도구 사용의 표준 데이터셋(ToolBench)** 출처. D-4가 벤치마크로 쓰는 ToolBench가 여기서 나왔다.

**요약.** 오픈소스 LLM이 tool 사용 능력에서 크게 뒤처지는 문제를 데이터 구축·모델 훈련·평가를 아우르는 프레임워크로 해결한다. 먼저 **ToolBench** — ChatGPT로 자동 구축한 tool 사용 instruction-tuning 데이터셋 — 을 제시한다. 3단계 구축: (i) API 수집, (ii) 지시문 생성(단일 tool·다중 tool 시나리오 모두), (iii) 해결 경로 주석. 추론 능력 강화를 위해 여러 추론 경로를 평가·확장하는 **DFS 기반 결정 트리 알고리즘**을 개발했다.

**인용할 만한 구체 수치.**
1. **RapidAPI Hub에서 49개 범주에 걸친 실제 RESTful API 16,464개**를 수집했다 — "도구가 많아진다"는 문제의 규모를 보여주는 숫자.
2. 신경망 API retriever를 붙인 ToolLLaMA가 미지의 API에 일반화하며 ChatGPT에 필적하는 성능을, OOD 데이터셋 APIBench에서도 강한 zero-shot 일반화를 보였다.

**실무 함의 (배경 서술용).** API 16,464개를 전부 프롬프트에 넣는 건 불가능하다. **retriever가 필요하다**는 결론이 여기서 나왔고, 그게 D-4의 "몇 개를 보여줄 것인가" 질문으로 이어진다.

---

### D-4. How Many Tools Should an LLM Agent See? A Chance-Corrected Answer

- **저자:** Vyzantinos Repantis, Ameya Gawde, Harshvardhan Singh, Joey Blackwell II
- **arXiv:** 2605.24660 · https://arxiv.org/abs/2605.24660
- **버전 이력:** v1 2026-05-23 / **v2 2026-06-07 (최신)**
- **Comments 필드 (원문):** *"13 pages, 2 figures"*
- **위상:** ⭐ **C-1과 짝을 이루는 이 책의 핵심 근거.** "tool을 몇 개나 만들 것인가"라는 서버 개발자의 실제 설계 결정에 숫자로 답한다.
- **⚠️ 인용 주의:** 이 논문은 **"tool이 많으면 정확도가 떨어진다"는 소박한 수치를 그대로 믿지 말라**는 쪽이다. 목록이 길어지면 **무작위로 찍어도 맞을 확률이 함께 올라가므로**, 보정하지 않은 정확도 비교는 오해를 부른다는 게 출발점이다. 인터넷에 도는 "tool 100개면 정확도 13%" 류의 수치는 **이 논문의 주장이 아니며 학술 출처가 확인되지 않았다** — 책에 쓰지 말 것.

**요약.** LLM 에이전트가 tool을 쓰기 전에 검색 시스템이 후보 목록(shortlist)의 길이를 정해야 한다. 너무 많으면 모델이 고르기 어렵고, 너무 적으면 정답 tool이 목록에 없다. 대부분의 시스템이 모든 질의에 고정 길이를 적용하지만 그 길이가 적절했는지 평가할 표준 지표가 없었다. 이 논문은 **보여준 tool 개수 자체를 평가 대상으로 삼고**, 주어진 깊이에서의 성공이 **같은 깊이에서 무작위 선택으로 달성했을 성과보다 나은지**를 묻는 우연 보정 지표 **BoR(Bits-over-Random)**를 적용한다. 나아가 같은 원리를 질의별 목록 길이를 정하는 RL 보상으로 전환한다. 3개 tool 선택 벤치마크, 복수 scorer, **20개에서 3,251개에 이르는 레지스트리**에서 평가했다.

**인용할 만한 구체 수치 (실험 조건 포함 — 그대로 인용 가능).**
1. **BFCL(370개 tool)**: 학습된 정책이 **평균 7개만 제시하면서 50개를 보여줄 때의 커버리지에 거의 근접했다 — 90.3% vs 90.8%.** (즉 목록을 1/7로 줄여도 커버리지 손실은 0.5%p.)
2. **ToolBench(3,251개 tool)**: 고정 5개 목록이 총합 커버리지는 더 높지만(**64.7% vs 61.9%**) **어려운 질의(정답 tool이 6~20위)에서는 아무것도 못 찾는다.** BoR 에이전트는 더 깊이 탐색해 같은 질의에서 **16.7%**를 찾아낸다.
3. **Claude Sonnet 4.6로 downstream 검증**: 짧은 적응형 목록이 **LLM의 tool 선택 능력 자체를 개선**했다 — 항상 5개를 보여줄 때 대비 **93.1% vs 87.1%**. 정답 tool이 목록에 있지만 1위는 아닌 **중난도 질의에서는 격차가 76.8% vs 60.9%로 벌어진다.**

**인용할 만한 문장 (초록).**
> "Show too many tools and the model struggles to choose. Show too few and the correct tool may not appear."

**실무 함의.** tool 개수는 공짜가 아니다. 서버 하나가 tool 50개를 노출하면 클라이언트의 선택 정확도를 갉아먹는다. **관련 tool을 소수로 추리는 편이 모델의 선택 정확도를 실제로 올린다**(93.1% vs 87.1%). 서버 설계 시 tool을 잘게 쪼개기보다 의미 단위로 묶고, 개수를 의도적으로 억제하라.

---

## E. 관찰성·평가

### E-1. From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents

- **저자:** Yiqi Wang, Jiaqi Zhang, Taotao Cai, Zirui Liu, Qingqiang Sun, Zequn Sun, Zhangkai Wu, Manqing Dong, Mingkai Zheng, Xuefei Yin, Yanming Zhu
- **arXiv:** 2606.04990 · https://arxiv.org/abs/2606.04990
- **버전 이력:** v1 2026-06-03 / v2 2026-06-14 / v3 2026-06-16 / **v4 2026-06-28 (최신)** — 활발히 개정 중
- **Comments 필드:** 없음
- **위상:** E각도에서 확보한 **유일한 검증 완료 논문**(→ 부정적 발견 참조). 서베이라 조감에는 충분하다.

**요약.** LLM 에이전트가 계획·도구 사용·검색·메모리 접근·환경 상호작용·다중 에이전트 협업을 수행하는 자율 시스템으로 진화하면서, 그 행동을 **검증·디버그·감사하기 어려워졌다**는 문제를 다룬다. 최종 답의 정확도만으로는 출력이 어떻게 만들어졌는지, 어떤 증거가 각 주장을 뒷받침했는지, **tool 호출이 정당했는지**, 메모리가 이후 결정에 어떤 영향을 줬는지, 실패가 어디서 시작됐는지를 설명할 수 없다. **실행 provenance를 에이전트 실행의 타입 지정 그래프**로, **evidence tracing을 그 그래프의 증거-지지 관계로의 투영**으로 정의하고, trace 소스·증거/실행 단위·provenance 관계·추적 입도(granularity)와 시점·표현 형태·신뢰 함수를 아우르는 분류 체계를 제시한다.

**인용할 만한 구체 주장.**
1. **"최종 답 정확도만으로는 tool 호출이 정당했는지 설명할 수 없다"** — 에이전트 시스템에서 프로세스 수준 책임성(process-level accountability)이 별도로 필요하다는 논거.
2. 다루는 방법론 축: provenance 표현, 증거 귀속, **tool 사용 provenance**, 런타임 가드레일, provenance를 담은 메모리, 관찰성, 실패 진단.

**실무 함의.** MCP 서버에 로그를 남길 때 "무엇을 실행했나"만으로는 부족하다. **어떤 컨텍스트·어떤 증거가 그 tool 호출을 유발했는지**까지 남겨야 사후에 tool poisoning을 판별할 수 있다. 즉 관찰성은 운영 편의가 아니라 A절 공격들의 **사후 탐지 수단**이다.

---

## 신선도 원장

검색 시점: **2026-07-26**. 모든 항목은 해당 arXiv abs 페이지를 직접 열어 제출 이력을 확인했다. "최신 개정일"이 오래된 항목일수록 그 사이의 생태계 변화가 반영돼 있지 않을 수 있다.

| # | 논문 (약칭) | arXiv ID | 최초 제출 | **최신 개정** | 버전 수 | 게재 상태 (Comments 필드 근거) |
|---|---|---|---|---|---|---|
| A-1 | MCP: Landscape, Security Threats | 2503.23278 | 2025-03-30 | **2025-10-07** | v3 | 미표기 (프리프린트) |
| A-2 | MCP at First Glance | 2506.13538 | 2025-06-16 | **2026-04-13** | v5 | 미표기 (프리프린트) |
| A-3 | A First Look at Security Issues in MCP | 2510.16558 | 2025-10-18 | **2026-04-27** | v2 | ✅ **DSN 2026 게재 확정** |
| A-4 | MCPTox | 2508.14925 | 2025-08-19 | **2025-08-19** | v1 | ✅ **AAAI-26 게재** (Vol.40 Iss.42, pp.35811–35819, DOI 10.1609/aaai.v40i42.40895) |
| A-5 | When MCP Servers Attack | 2509.24272 | 2025-09-29 | **2025-09-29** | v1 | 미표기 (프리프린트) |
| A-6 | MCPSecBench | 2508.13220 | 2025-08-17 | **2026-02-12** | v3 | Lingnan Univ. 테크니컬 리포트 (코드 공개) |
| A-7 | MCP Threat Modeling (STRIDE/DREAD) | 2603.22489 | 2026-03-23 | **2026-03-23** | v1 | 미표기 · ⚠️ MDPI 저널판 중복 가능 |
| A-8 | ETDI | 2506.01333 | 2025-06-02 | **2025-06-02** | v1 | 미표기 (11p, GitHub 링크 있음) |
| A-9 | SoK: Security and Safety in MCP | 2512.08290 | 2025-12-09 | **2025-12-13** | v2 | 미표기 (프리프린트) |
| B-1 | A Survey of AI Agent Protocols | 2504.16736 | 2025-04-23 | **2025-06-21** | v3 | 미표기 (프리프린트) |
| B-2 | Survey of agent interoperability protocols | 2505.02279 | 2025-05-04 | **2025-05-23** | v2 | 미표기 (프리프린트) |
| B-3 | Security Threat Modeling (MCP/A2A/Agora/ANP) | 2602.11327 | 2026-02-11 | **2026-04-17** | v2 | 미표기 (프리프린트) |
| C-1 | From REST to MCP | 2507.16044 | 2025-07-21 | **2026-04-06** | v4 | 미표기 (프리프린트) |
| C-2 | Large-Scale Dataset of MCP on GitHub | 2607.10123 | 2026-07-11 | **2026-07-11** | v1 | 미표기 · 🕒 **검색 시점 기준 15일 전** |
| D-1 | ReAct | 2210.03629 | 2022-10-06 | **2023-03-10** | v3 | ✅ **ICLR camera ready** (코드 공개) |
| D-2 | Toolformer | 2302.04761 | 2023-02-09 | **2023-02-09** | v1 | 미표기 — 게재처 단정 금지 |
| D-3 | ToolLLM | 2307.16789 | 2023-07-31 | **2023-10-03** | v2 | 미표기 (프리프린트) |
| D-4 | How Many Tools Should an LLM Agent See? | 2605.24660 | 2026-05-23 | **2026-06-07** | v2 | 미표기 (13p, 2 figures) |
| E-1 | From Agent Traces to Trust | 2606.04990 | 2026-06-03 | **2026-06-28** | v4 | 미표기 (프리프린트) |

**최신성·고전 균형:** 총 19편 = 2025~2026년 논문 **16편** : 2022~2023년 seminal **3편**(ReAct·Toolformer·ToolLLM) ≈ **8:2**. 주제 특성(MCP는 2024년 말 등장)상 고전 비중을 더 높이는 건 불가능하다.

**게재 상태 요약 — 인용 시 반드시 유의:** 19편 중 **동료 심사 통과가 문서로 확인된 것은 3편**이다 — **A-3(DSN 2026 게재 확정), A-4(AAAI-26 게재, DOI 확인), D-1(ICLR camera ready)**. 나머지 16편은 arXiv 프리프린트다. MCP 자체가 2024년 말 등장한 주제라 심사 사이클이 아직 돌지 않은 게 주된 이유지만, **책에서 "연구에 따르면"으로 단정 인용할 때는 A-3·A-4·D-1을 우선 배치하고, 나머지는 프리프린트임을 밝히는 게 안전하다.**

**재현성 확인된 자료 (독자가 직접 돌려볼 수 있는 것):**
- A-6 **MCPSecBench** — `github.com/AIS2Lab/MCPSecBench` (초록에 명시)
- A-8 **ETDI** — 서론에 GitHub 링크 있음 (Comments 필드에 명시)
- C-1 **AutoMCP** — 파이프라인 릴리스 명시
- C-2 — JSONL 데이터셋 공개 명시
- D-1 **ReAct** — `react-lm.github.io`
- A-4 **MCPTox** — 벤치마크 릴리스 명시

---

## 확인하지 못한 것 / 부정적 발견

부정적 발견도 1급 결과다. 아래는 **찾지 못했다는 사실 자체가 책의 논거가 되는** 항목들이다.

### N-1. "MCP 서버 개발 방법"에는 학술 문헌이 없다 (예상된 결과, 명시적으로 확인)
SDK 사용법, 언어별 구현 패턴, tool 스키마 작성법, 배포·운영 실무를 다룬 논문은 **존재하지 않는다**. 학계는 MCP를 "만드는 법"이 아니라 **"위험한가(A)·다른 프로토콜과 어떻게 다른가(B)·생태계가 어떻게 생겼나(C)"**로 접근한다. 이 책의 실무 부분은 공식 문서·1차 소스가 담당하고, **논문은 "왜 그렇게 설계해야 하는가"의 근거로만 쓰는 게 맞다.** 유일한 예외가 C-1(From REST to MCP)로, 서버 구축 실무를 정면으로 실측한 사실상 유일한 논문이다.

### N-2. OAuth confused deputy / 토큰 패스스루 — 전용 학술 논문 없음 (⚠️ 중요)
검색 각도 A에 명시된 항목이지만, **confused deputy와 token passthrough를 정면으로 다룬 동료 심사 논문이나 arXiv 논문을 찾지 못했다.** 확인한 사실:
- 이 주제의 실질적 1차 소스는 **MCP 명세 자체**다 — `modelcontextprotocol.io/specification/2025-11-25/basic/authorization`. 명세가 **토큰 패스스루를 명시적으로 금지**하고 **RFC 9700(OAuth 2.0 Security Best Practices)**을 참조한다는 점이 웹 검색으로 확인됐다. (⚠️ 명세 원문은 이번 리서치에서 직접 열어 검증하지 않았다 — **web-researcher가 1차 소스로 검증해야 할 항목**이다.)
- 나머지 자료는 전부 벤더·보안 업체 블로그(Descope, Aembit, FlowHunt 등)로 **학술 자료가 아니다** → 이 리서치의 범위 밖.
- **학계에서 가장 가까운 대체물은 A-8(ETDI)**이다 — OAuth 2.0으로 tool 정의를 강화하고 정적 scope의 한계를 지적한다. 그리고 A-7이 위협 모델링 대상 5개 컴포넌트에 **Authorization Server를 포함**시켰다.
- **결론:** 책의 OAuth·인가 장은 **논문이 아니라 MCP 명세 + RFC 9700을 1차 근거로 삼아야 한다.** 학술 백킹은 ETDI 하나로 보조하는 선이 정직하다.

### N-3. Java/JVM MCP 생태계 — 근거 없음
대상 독자에 Java 실무자가 포함되지만, **Java·Spring AI·JVM 기반 MCP 구현을 다룬 논문을 찾지 못했다.** C-2가 "Python과 TypeScript가 지배한다"고 보고할 뿐 Java의 위상은 언급하지 않는다. **Java 관련 주장은 어떤 논문으로도 뒷받침하지 마라** — 공식 SDK 문서와 커뮤니티 자료가 담당해야 한다.

### N-4. 전송(transport) 계층 성능 비교 — 확보 실패
stdio vs Streamable HTTP vs SSE의 지연시간·처리량을 실측 비교한 논문을 찾지 못했다. B-1이 프로토콜 비교 축에 latency를 포함한다고 초록에서 밝히지만, **MCP 전송 방식 간 비교인지는 초록만으로 확인되지 않았다** — 이 수치가 책에 필요하면 B-1 본문(HTML)을 직접 확인해야 한다.

### N-5. 관찰성(각도 E) — 커버리지 얇음
E각도로 **검증 완료한 논문은 E-1 한 편뿐**이다. 검색에서 후보(2606.01581 *Agent System Operations*, 2603.29848 *AgentFixer*, 2607.07689 등)가 나왔으나 우선순위상 검증하지 않았다. 또한 **MCP 서버에 특화된** 관찰성·트레이싱 논문은 보이지 않았고, E-1을 포함해 전부 **에이전트 시스템 일반**을 다룬다. OpenTelemetry 기반 실무 자료는 학술이 아닌 벤더 블로그 영역이다.

### N-6. arXiv API 전수 열거 실패 (부정적 발견의 한계)
`all:"Model Context Protocol"` 전수 열거로 위 목록의 완전성을 **증명**하려 했으나, arXiv API가 반복적으로 `Rate exceeded`를 반환해(12회 재시도, 25초 백오프) 실패했다. Semantic Scholar API도 HTTP 429였다. 따라서 **위 목록은 "WebSearch로 발견 가능한 범위"이며 전수 조사가 아니다.** 누락된 논문이 있을 수 있다. (검색 시점 2026-07-26 기준.)

### N-7. 발견했으나 **검증하지 않은** 후보 (⚠️ 이대로 인용 금지)
아래는 WebSearch 결과에 제목·ID가 나타났지만 **arXiv abs 페이지를 직접 열어 확인하지 않았다.** 제목·저자·수치가 부정확할 수 있으므로 **인용 전 반드시 개별 검증**이 필요하다. 범위 확장이 필요할 때의 다음 후보군이기도 하다.

| 후보 (WebSearch 표기 제목) | 표기된 ID | 관련 각도 |
|---|---|---|
| MCPGuard: Automatically Detecting Vulnerabilities in MCP Servers | 2510.23673 | A |
| MCP-SafetyBench | 2512.15163 | A |
| A Formal Security Framework for MCP-Based AI Agents | 2604.05969 | A |
| MCP-DPT: Defense-Placement Taxonomy | 2604.07551 | A |
| MCP-in-SoS: Risk assessment for open-source MCP servers | 2603.10194 | A |
| MCP-38: A Comprehensive Threat Taxonomy for MCP | 2603.18063 | A |
| Semantic Attacks on Tool-Augmented LLMs (Descriptor-Level Manipulation) | 2512.06556 | A |
| SMCP: Secure Model Context Protocol | 2602.01129 | A |
| Trust No Tool: Untrusted Tool Feedback | 2605.17453 | A |
| Red-Teaming Coding Agents from a Tool-Invocation Perspective | 2509.05755 | A |
| AgentBound: Securing Execution Boundaries of AI Agents | 2510.21236 | A |
| Systems Security Foundations for Agentic Computing | 2512.01295 | A |
| ProtocolBench: Which LLM MultiAgent Protocol to Choose? | 2510.17149 | B |
| The Evolution of Tool Use in LLM Agents | 2603.22862 | D |
| Semantic Tool Discovery for LLMs (Vector-Based MCP Tool Selection) | 2603.20313 | D |
| Extending ResourceLink: Large Dataset Processing in MCP Applications | 2510.05968 | C/D |
| Agent System Operations: Categorization, Challenges | 2606.01581 | E |
| AgentFixer: Failure Detection to Fix Recommendations | 2603.29848 | E |
| Agent Delivery Engineering Predictive Reliability Framework | 2607.07689 | E |

### N-8. 인용 시 주의가 필요한 개별 항목 (재확인 완료 사항 포함)
- **A-2 vs A-3 혼동 금지.** "1,899개 서버 / 7.2% / 5.5% / 66% code smell / 14.4%"는 **전부 A-2(2506.13538)**의 수치다. "67,057개 서버 / 6개 레지스트리 / 833개 취약 / 18개 의심"은 **A-3(2510.16558)**의 수치다. 두 논문은 별개이며, 초록 원문 대조로 확인 완료.
- **"tool 100개면 정확도 13%"류 수치 사용 금지.** WebSearch 과정에서 이 수치가 블로그(webscraft.org)에서 발견됐으나 **학술 출처가 확인되지 않았다.** D-4는 오히려 이런 비보정 수치의 해석을 경계하는 논문이다. 책에 넣지 마라.
- **A-4(MCPTox)의 72.8%는 o1-mini 값**이며, 이 논문의 핵심 주장은 "**더 유능한 모델이 더 취약**"이다. "약한 모델이 뚫린다"로 뒤집어 쓰면 논문을 정반대로 인용하는 것이 된다. 또한 **72.8%를 "모델 중 최고 ASR"로 쓰지 마라** — 초록에 순위 주장이 없다.
- **A-4는 arXiv판과 AAAI 게재판의 제목이 다르다** — arXiv: *"…Tool Poisoning **Attack** on…"*, AAAI: *"…Tool Poisoning on…"*. 참고문헌에 둘을 섞어 적지 마라.
- **N-2(OAuth)와 N-3(Java)은 "아직 못 찾았다"가 아니라 "학술 문헌이 없다"에 가깝다.** 해당 장은 처음부터 명세·공식 문서 기반으로 설계하고, 논문 인용을 억지로 끼워 넣지 마라.
- **A-7과 MDPI 논문은 같은 연구일 가능성이 높다** — 두 편으로 세지 마라.
- **D-2(Toolformer)의 게재처를 단정하지 마라** — arXiv Comments 필드에 학회 정보가 없다.

---

<!-- 검증 방법: WebSearch로 후보 발견 → arxiv.org/abs/{id}를 WebFetch로 직접 열어 제목·저자 전체·전 버전 제출일·Comments·초록 원문 대조. 19편 전원 이 절차를 통과했다. 수치는 초록 원문에서 그대로 전사. 검색·검증 시점: 2026-07-26. -->
