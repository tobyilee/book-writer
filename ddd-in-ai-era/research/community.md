# 커뮤니티 리서치: AI 에이전틱 코딩 시대의 DDD

> 수집 기간: 2026-05-17
> 수집자: research-lead (community 갈래)
> 대상 독자: DDD를 알고 AI 코딩 도구를 도입 중인 시니어 개발자·테크 리드·아키텍트

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "AI가 만든 코드가 점점 무서워진다 — 유지보수가 안 된다"
- 출처: tech.cloud.nongshim.co.kr (NDS Cloud Tech Blog, Park Jung-hyun, 2026-03-09) — "8년차 AI 엔지니어는 왜 바이브코딩을 포기했나?"
- 핵심 고통: 처음엔 Cursor/Claude Code로 신나게 짰는데, 채팅 기능을 하나 더 추가하려니 기존 코드가 깨졌다. 코드를 검증·수정·이해하는 데 드는 시간이 오히려 늘었다.
- 인용: "코드를 검증하고 수정하고 이해하는 데 드는 시간이 오히려 늘어날 수 있다"
- 인용: "AI는 생산성을 높여주는 도구이지, 나를 대체하는 도구가 아닙니다"
- 보강 데이터: METR 2025 — 경험 많은 개발자가 AI 도구로 **19% 더 느려졌는데** 본인은 "20% 빨라졌다"고 느꼈다는 연구.
- 보안: AI 공저 코드의 보안 취약점 비율이 사람 코드의 **2.74×**.

### 패턴 2: "DDD가 매력적이지만 너무 어렵다 — 그런데 AI 시대엔 더 어려워진다?"
- 출처: velog.io/@carrykim (Kerry Kim, 2026-01-08) — "도메인 주도 설계(DDD), 매력적이지만 어려운 이유"
- 핵심 고통: "도메인 전문가와 개발자가 모여서 하나의 도메인을 분석하고, 서로 같은 언어를 사용하도록 정리하는 것이 현실적으로 어렵다."
- 구체적 장벽: 일정 조율, 부서 간 용어 표준화(개발·디자인·세일즈), 도메인 전문가의 적극 참여, 개발자가 도메인 전문가가 되어야 함.
- 성공 사례: 해당 회사 개발자가 1주일간 SDR 업무를 체험한 후에야 진짜 도메인 이해가 시작됐다.

### 패턴 3: "Vibe coding은 죽었다 / Vibe coding은 미래다" — 양극단의 격돌
- 출처: Medium (Alek Dobrohotov, 2026-02-25) — "Vibe Coding Is Dead. Long Live Agentic Coding."
- 출처: 나무위키 "바이브 코딩" 항목 / brunch.co.kr/@b8f8683a622d44b/193
- 핵심 충돌:
  - 옹호: "6개 AI 에이전트가 3개 프로젝트를 동시에 굴리는데, 5명짜리 팀보다 빨리 짓는다." (Dobrohotov)
  - 비판: "수십, 수백만 줄짜리 프로그램의 유지보수는 전문 프로그래머가 한다" / "안정성·보안·확장성의 한계"
- 인용: "I was building faster than teams of five developers... I just didn't know how slow I actually was." (Dobrohotov, vibe coding을 후행으로 평가)

### 패턴 4: "도메인 모델링은 사람만의 영역인가, AI도 같이 굴릴 수 있나"
- 출처: forum.cursor.com/t/vibe-coding-without-tdd-and-ddd-methodlogy-is/78298 (Cursor 공식 포럼)
- 핵심 토론: cocode("AI 코딩에는 TDD/DDD가 생존 전술이다") vs Zaz("아키텍처·데이터 흐름을 먼저 잘 그려두면 95%를 첫 패스에 완성한다")
- 결국 양쪽 다 "사전 설계·문서·계약이 필수"라는 점에 수렴 — 차이는 정도와 도구.

### 패턴 5: "AI를 잘 쓸수록 내 실력이 정체된다"
- 출처: evan-moon.github.io (Evan Moon, 2026-04-18) — "AI 코딩 시대, 더이상 성장하지 않는 개발자들"
- 핵심 고통: 시니어든 주니어든 AI에 의존할수록 코드 판단 능력의 청크(chunk)가 형성되지 않는다.
- 인용: "뇌는 편하면 기억하지 않는다"
- 인용: "AI를 가장 잘 활용할 수 있는 개발자는, AI 없이도 코드를 판단할 수 있는 개발자다"
- 인용: "30분 동안 끙끙대며 직접 짠 코드가 AI가 3초 만에 생성한 코드보다 기억에 더 깊이 남는다"
- 함의: 시니어가 AI에게 도메인 모델링을 통째로 위임하면, 도메인 직관 자체가 마모된다.

### 패턴 6: "DDD는 과대평가됐다 / DDD는 과소평가됐다" — Hacker News 영구 떡밥
- 출처: HN — "DDD Is Overrated" (item 26312652)
- 비판 측: "단순 CRUD API인데 DDD 적용해서 추상화 계층만 잔뜩 생긴 악몽이 됐다", "3년 이상 진화시킬 비전이 없으면 DDD는 가성비가 안 나온다", "Anemic Domain은 비판받지만 실용적이다"
- 옹호 측: "DDD는 underrated이고 underused다", "전략적 DDD가 anemic 모델의 한계를 해결한다"
- AI 시대 적용: 같은 논쟁이 "에이전트가 알아서 짠 코드를 굳이 DDD 패턴으로 정리할 가치가 있나?"로 변형되어 계속됨.

### 패턴 7: "프롬프트가 spaghetti가 됐다"
- 출처: Nikita Golovko 강연 (gitnation.com)
- 핵심 고통: 처음엔 깔끔하던 3개 에이전트가 6개월 후 토큰 3,000+ 짜리 프롬프트가 됐고, 그 중 ~85%가 도메인 로직이 아니라 파싱·통합 로직이다.

### 패턴 8: "ChatGPT 답변을 일관되게 받고 싶다 — 컨텍스트 엔지니어링이 새로운 vibe coding"
- 출처: HN — "Context engineering is the new vibe coding" (item 44740930, 본문은 직접 접근 불가했으나 검색 결과 공유)
- 출처: Anthropic — "Effective context engineering for AI agents"
- 핵심 전환: "에이전트가 원하는 걸 이해 못해" → "에이전트에게 필요한 컨텍스트가 없어"

## 실무 휴리스틱

- **DDD glossary를 `docs/glossary.md`로 살아있는 문서화**, 에이전트가 모든 산출물에서 이를 따르도록 한다. (Paul Iusztin, decodingai.com 2026-05-12)
- **코드는 파일 타입이 아니라 bounded context(=actionability) 기준으로 조직**한다 — 에이전트 reasoning이 좋아진다. (동일 출처)
- **휴먼 체크포인트 2개 + 재시도 상한 5회**로 에이전트 폭주를 막는다. (동일 출처)
- **"코드 짠 에이전트가 정합성 판정하지 않는다"** — 책임 분리. (동일 출처)
- **Knowledge Priming → Design-First → 팀 표준 encoding → Context Anchoring → Feedback Flywheel** 다섯 가지 패턴. (Rahul Garg, Thoughtworks, martinfowler.com 2026-04-08)
- **에이전트당 토큰 ~500 + 도메인 로직 90% 비중**을 지표로 삼는다. 그 이상이면 bounded context 분할 신호. (Golovko, gitnation.com)
- **자연어 API 대신 스키마(Pydantic 등)**를 에이전트 간 계약으로. (동일 출처)
- **Anti-Corruption Layer를 에이전트 사이의 의미적 방화벽**으로 활용 — 같은 단어가 컨텍스트마다 다른 의미일 때. (동일 출처)
- **Context Map을 다이어그램이 아니라 실행 가능한 코드**로 — 컨텍스트 간 upstream/downstream, contract version, adapter 명시. (동일 출처)
- **Spec Ambiguity Resolver 류 도구**로 모호어를 사람이 정의 후 진행, AI는 의미를 자율 결정하지 않는다. (Daniel Schleicher, 2026-01-04)
- **시니어는 AI 사용 전에 자기 설계안을 먼저 작성**해 생성 효과(generation effect)를 활용. (Evan Moon, 2026-04-18)
- **AI 코딩 직전 단계로 "vibe modeling"**(시각적 도메인 이벤트 보드)을 두고, 그 산출물을 Claude Code/Cursor의 컨텍스트로 export. (vibemodeling.app)

## 논쟁점

### 논쟁 A: DDD는 AI 시대에 더 중요해지는가, 사라지는가?
- **더 중요해진다** (Khosravi, Subramani, Wijesekare, Golovko, Iusztin, Croft, Schleicher, Mimul): 에이전트가 만들어내는 코드량 폭증, 예측 불가능한 호출 시퀀스, 의미 모호성 증폭 — 모두 DDD의 경계와 ubiquitous language가 직접 해결한다.
- **사라진다 / 변형된다**:
  - 솔로 창업자나 단일 도메인 expert가 모든 역할을 겸할 때는 BMAD/SDD가 충분 (Westheide 인용의 negative case).
  - AI가 ubiquitous language 자체를 자동 추출하는 시대(arXiv:2509.00140)에는 사람의 모델링 단계가 줄어든다.
  - Vibe coding 옹호자(초기 Karpathy 이미지)는 "굳이 정리 안 해도 작동한다"는 입장.

### 논쟁 B: Vibe coding은 죽었나?
- 사망 선고: Dobrohotov, NDS Cloud Tech Blog 박정현, medevel.com — 모두 "production에서 안 된다"
- 부활론: "여전히 prototyping·소규모 자동화에는 최고", 나무위키 항목도 "느낌 코딩"을 정의로 인정.
- 새로운 이름: Agentic coding / Context engineering / Harness engineering — 본질은 "사람이 더 깊이 관여"로 회귀.

### 논쟁 C: AI가 만든 코드도 "Clean code"여야 하나?
- Kief Morris (Fowler 사이트, 2026-03-04): "If the LLMs can write and change code without us, do we care whether the code is 'clean'?" — 진지한 질문으로 제기.
- 그러나 같은 글의 결론: humans **on** the loop이 정답 — 즉 깨끗해야 한다, 사람이 검토·진화시켜야 하기 때문.

### 논쟁 D: BMAD/SDD vs DDD
- Westheide: "BMAD는 DDD의 조급한 사촌일 뿐. 조직 문제는 도구로 못 푼다."
- BMAD 옹호: "리얼타임 spec 협업이 폭포수 인터뷰보다 낫다"
- 합의 가능 지점: SDD는 small team / solo에 강하고, 큰 조직에서는 DDD의 emergent modeling이 여전히 필수.

### 논쟁 E: 시니어의 새 역할 — "조율자/orchestrator"인가 "harness engineer"인가
- Anthropic 2026 Trends Report: "엔지니어는 코드 작성에서 에이전트 조율로 이동"
- Kief Morris: "Humans on the loop" — harness 엔지니어링이 시니어의 새 핵심.
- Martin Fowler: 결국 "experienced developer가 AI를 amplifier로 쓴다" — 판단·도메인 이해·아키텍처가 시니어의 핵심.
- 합의: 코드 한 줄 한 줄 짜기보다 시스템·도메인·에이전트 행동을 설계하는 일이 중심.

## 한국 실무자 관점

- **DDD는 한국에서도 매력적이지만 어렵다** — 같은 고통이 반복된다. 최범균 책 "DDD Start!"와 강의가 표준 입문. (Joonghyeon Kim, medium myrealtrip)
- **카카오헤어샵 사례**: Entity/Value Object/Service/Repository/Factory를 JPA로 구현했지만, Bounded Context는 완전히 못 나누고 패키지 기반 구분에 머물렀다 — DDD 도입 초반의 흔한 패턴. (cg4jins, 2018) — "소프트웨어의 본질은 기술이 아니라 도메인의 문제를 해결하는 것"
- **한국형 ubiquitous language**: 예약 상태 코드(READY/OK/CANCELED/WAIT_CANCEL/COMPLETED/NO_SHOW)를 비즈니스 운영진이 쓰는 용어 그대로 가져왔다 — ACL 없이 raw 비즈니스 어휘를 코드까지 통과시킨 사례.
- **AI 코딩 시대의 정체된 개발자**: Evan Moon이 정밀하게 진단. "AI 없이도 코드를 판단할 수 있어야 AI를 잘 쓴다"는 역설.
- **8년차 AI 엔지니어의 바이브 코딩 포기**: "코드 검증·수정·이해 시간이 오히려 늘었다"는 현장 증언.
- **AI-DLC 한국어 백서**(Seungwoo321 GitHub repo): AWS 원본의 한국어 번역. AI가 자율적으로 Aggregate/VO/Entity/Domain Event/Repository/Factory를 생성하는 워크플로 명시 — 즉 **국내 AI 자동화 방법론에서도 DDD 패턴이 1급 시민**.
- **번역어 분기**: Bounded Context = 컨텍스트/제한된 맥락/경계 컨텍스트로 혼용. Aggregate = 애그리거트(주류) vs 집합체. Domain Event = 도메인 이벤트(거의 통일).
- **국내 컨퍼런스/스터디**: 인프런 "도메인 주도 설계 마이크로서비스" 강의가 여전히 인기. 우아한형제들·카카오·SK 등 사례가 popit, brunch에 산재.

## 링크 모음

- https://tech.cloud.nongshim.co.kr/blog/aws/ai/3854/ — 8년차 AI 엔지니어 바이브 코딩 포기 (한국, 2026-03-09)
- https://velog.io/@carrykim/도메인-주도-설계DDD-매력적이지만-어려운-이유 — DDD가 어려운 이유 (한국, 2026-01-08)
- https://evan-moon.github.io/2026/04/18/developers-who-stopped-growing-in-ai-era/ — AI 시대 정체된 개발자 (한국, 2026-04-18)
- https://www.mimul.com/blog/ai-coding-style/ — 도메인 중심 코딩 원칙 12개 (한국, 2026-01-29, 업데이트 04-26)
- https://github.com/Seungwoo321/aidlc-docs/blob/main/ai-dlc-whitepaper-ko.md — AI-DLC 한국어 백서
- https://brunch.co.kr/@cg4jins/7 — 카카오헤어샵 DDD (한국, 2018-05-03)
- https://medium.com/myrealtrip-product/what-is-domain-driven-design-f6fd54051590 — 최범균 DDD 강의 후기 (한국, 2020-06-09)
- https://forum.cursor.com/t/vibe-coding-without-tdd-and-ddd-methodlogy-is/78298 — Cursor 포럼 vibe coding + TDD/DDD
- https://news.ycombinator.com/item?id=26312652 — HN "DDD Is Overrated" 영구 떡밥 (HTTP 429로 본문 직접 미접근, 검색 요약 사용)
- https://news.ycombinator.com/item?id=44740930 — HN "Context engineering is the new vibe coding" (HTTP 429)
- https://news.ycombinator.com/item?id=45821587 — HN "From vibe coding to context engineering: 2025"
- https://medium.com/@aleksandardobrohotov/vibe-coding-is-dead-long-live-agentic-coding-b3957833f55d — Vibe coding 사망 선고 (2026-02-25)
- https://www.decodingai.com/p/squid-my-agentic-coding-setup-may-2026 — 6-agent Claude Code team (2026-05-12)
- https://www.vibemodeling.app/what-is-vibe-modeling/ — Vibe modeling 정의
- https://www.itworld.co.kr/article/3967678/... — "개발자, 바이브 코딩을 배우거나 은퇴하거나" (한국 IT World)
- https://namu.wiki/w/바이브%20코딩 — 나무위키 정의

## 리서치 한계 (커뮤니티 갈래)

- HN 본문 일부가 HTTP 429 등으로 직접 fetch 실패 → 검색 요약을 통한 간접 인용으로 대체.
- Reddit r/programming, r/softwarearchitecture, r/AskComputerScience 등의 raw thread는 검색 결과 페이지를 통한 간접 수집에 머물렀다. 직접 thread URL을 hit 하지 못한 부분.
- OKKY 라이브 토론, 네이버 카페(자바스칸 등), 디스코드 공개 로그는 표본이 적음 — 한국 커뮤니티 갈래의 보강 여지.
- Vaughn Vernon의 최근(2025-2026) AI 관련 발언은 LinkedIn 포스트 위주 — 직접 quote 수집 어려움. 향후 인터뷰·트윗 보강 필요.
