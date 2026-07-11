# 커뮤니티 리서치: Learning in the harness — AI와 함께 일하며 함께 성장하는 개발자

> **검색 시점 메타:** 2026-07-11 기준 수집. 플랫폼: Hacker News(Algolia API로 추천수·댓글수·날짜 검증), 한국 커뮤니티(GeekNews·velog·OKKY), 회사/전문 매체 블로그(Fastly·CIO·Red Hat·The New Stack).
> **신뢰성 규율:** 아래 인용은 대부분 **익명/개인의 일화적 근거(anecdotal)**다. 통계가 아니라 '현장의 온도'와 '챕터 오프닝 공감 재료'로 쓴다. 사실 주장(수치·연구 결과)은 별도 표시했고 fact-checker/web·paper 리서처가 1차 출처로 교차 검증해야 한다.
> **개별 댓글 추천수 주의:** Hacker News Algolia item API는 **댓글 단위 추천수를 제공하지 않는다**(null). 따라서 아래 HN 인용은 **스레드 전체 점수/댓글수만 검증됨**이며, 개별 댓글은 "대표 발언"으로 표기했다. 개별 추천수를 사실처럼 쓰지 말 것.
> **한국어/영어 병기:** 대상 독자(한국 현업·주니어)의 언어에 맞춘 국내 재료를 English 재료와 나란히 확보했다.

---

## 1. 실력 정체 불안 (챕터 오프닝 소재 — 가장 강력)

### 패턴 1-A: "AI 쓰니 편한데 내가 바보가 되는 것 같다" — 자기고백형 불안

이 패턴은 HN에서 반복적으로, 그리고 **점점 더 큰 규모로** 터진다. 시기순으로 규모가 커지는 게 눈에 띈다(2025-01 → 2026-06).

- **Hacker News — "AI is making me dumb"** (블로그 자기고백 제출)
  - URL: https://news.ycombinator.com/item?id=48139148
  - 날짜: 2026-05-14 · **556 points · 댓글 300** (Algolia 검증)
  - 대표 발언 (anecdotal):
    - `blain`: *"I catch myself asking AI wondering about random things that pop into my head, reading it, maybe using that knowledge once and later no longer remembering what it was. ... sometimes it seems like there is not enough space in my brain for things AI is learning me."* — **"내 뇌에 AI가 나에게 가르치는 것들을 넣을 공간이 부족한 것 같다"** — 책의 '절차 기억/생성 효과' 논지에 정확히 맞는 날것의 문장.
    - `voncheese`: *"Relatable! ... Things that help me feel smarter are * actually writing more on my own ... * upleveling my thinking ... * leverage my experience — guide (or sometimes force) the AI assistant ... * learning new things — rather than let AI just replace things I can do, I use AI to help me learn new things faster."* — 처방(4장)의 실무자판.
    - `weezing` (냉소): *"You are doing this to yourself."* — "네가 자초한 거다" (자기규율 강조 진영)

- **Hacker News — "Is AI ruining our skills? Early results are in – and they're not good"**
  - URL: https://news.ycombinator.com/item?id=48601286
  - 날짜: 2026-06-19 · **253 points · 댓글 318** (Algolia 검증)
  - 대표 발언 (anecdotal — ★챕터 오프닝 1순위 후보):
    - `iLoveOncall`: *"The two senior engineers in my org (in a FAANG) who vibe-code the most have lost literally all of their skills. Their code has become terrible and their judgment even worse."* — **시니어조차 vibe coding 과다로 판단력이 무너진다는 현장 증언.** '역량의 착각'을 시니어에게도 적용하는 강력한 재료. (단, 익명 1인 관찰 = anecdotal, 일반화 금지)
    - `georgemcbay`(사회적 위험 프레임): *"The real threat isn't that we'll all lose our skills and then lose access to AI ... it is that AI will remain at roughly current levels and we'll dull our skills due to reliance on it and innovation will stall because we've offloaded too much of the thinking to the non-innovative machine."* — 개인이 아니라 '혁신 정체'라는 사회 수준 위험.

- **Hacker News — "Ask HN: Did AI make you a worse programmer?"**
  - URL: https://news.ycombinator.com/item?id=42614392
  - 날짜: 2025-01-06 · **16 points · 댓글 12** (Algolia 검증 — 소규모지만 원형적 질문)
  - 대표 발언 (anecdotal):
    - OP `alex5207`: *"AI had sneaked in on me: It had made me unlearn syntax that used to be second nature."* — **"AI가 나도 모르게 스며들었다. 예전엔 제2의 천성이던 문법을 잊게 만들었다."**
    - `Oia1`(반증 겸 희망): *"I recently stopped using AI directly in my code editor ... However I have noticed I regain the lost syntax knowledge very fast."* — 껐더니 빠르게 회복하더라 → '가역적'이라는 낙관.

### 패턴 1-B: 한국 — "뇌는 편하면 기억하지 않는다" (논지와 가장 정확히 겹치는 국내 글)

- **velog(개인 블로그) — "AI 코딩 시대, 더이상 성장하지 않는 개발자들"** (evan-moon)
  - URL: https://evan-moon.github.io/2026/04/18/developers-who-stopped-growing-in-ai-era/
  - 날짜: 2026-04-18 · (좋아요/조회 미확인 — "확인 필요")
  - 핵심 인용 (저자 블로그 = 정리된 주장이나 현업 개발자 1인의 견해 = anecdotal 논증):
    - **"10년을 일해도 1년짜리 경험을 10번 반복하는 것은 10년의 경험이 아니다"**
    - **"뇌는 편하면 기억하지 않는다 ... 뇌가 열심히 일할수록 기억이 단단하게 저장되고 편하게 받아들인 정보는 편하게 사라진다"**
    - **"AI를 가장 잘 활용할 수 있는 개발자는, AI 없이도 코드를 판단할 수 있는 개발자다"**
    - **"30분 동안 끙끙대며 직접 짠 코드가 AI가 3초 만에 생성한 코드보다 기억에 더 깊이 남는다"**
    - **"고통은 피하고 싶은 것이지만, 성장의 관점에서 보면 선택이 아니라 조건에 가깝다"**
  - 비고: 책 seed 에세이의 '생성 효과·절차 기억' 논지와 거의 1:1 대응하는 **국내 독자용 최강 공감 재료.** 단 이 블로그의 사실 주장(예: 특정 연구 인용)은 web/paper 리서처가 재확인 권장.

- **velog — "AI 시대의 개발자: 현업 개발자의 솔직한 이야기"** (teo.v / 테오)
  - URL: https://velog.io/@teo/ai-and-developer
  - 날짜: 2025-11-03
  - 핵심 인용 (현업 개발자 관점 = anecdotal):
    - **"미디어를 볼 때는 'AI가 나를 대체하면 어쩌지?'라고 불안한데 막상 현실에서 AI를 쓰다 보면 '아니! 제발 좀 답답하네'"** — 불안(담론)과 실무(체감)의 간극을 유머러스하게 포착. ★오프닝 후보.
    - **"AI가 나 대신 공부하고, 나 대신 고민하고, 나 대신 코딩하게 두는 순간, 우리는 막막한 문제를 붙들고 씨름하며 얻어내는 개발자 고유의 문제 해결 능력을 잃게 됩니다."**
    - 결론: **"기술적으로 대체되는 것이 아니라, 스스로 생각하기를 포기함으로써 대체당하는 것"** — 책 맺음말("생각을 안 하는 것이 위험")과 공명.

**추정 원인(커뮤니티 공유 진단):** 통증 없이 받아들인 정보는 남지 않는다(생성 효과). '읽어서 이해됨 ≠ 백지에서 생성 가능'의 간극이 디버깅/장애 상황에서 드러난다. → 책의 seed 논지가 커뮤니티 언어로 이미 유통 중.

---

## 2. 시니어-주니어 격차 논쟁

### 사실 데이터(설문) — anecdotal 아님, 하지만 1차 출처 재확인 권장

- **Fastly 블로그 — "Vibe Shift in AI Coding: Senior Developers Ship 2.5x More Than Juniors"**
  - URL: https://www.fastly.com/blog/senior-developers-ship-more-ai-code
  - 날짜: 2025-08-27 · 저자 Alina Lehtinen-Vela · **표본 n=791 프로 개발자, 조사기간 2025-07-10~14**
  - 핵심 수치(fact — fact-checker 대조 대상): 시니어(10년+)의 **32%**가 "출하 코드의 절반 이상이 AI 생성"이라고 답 vs 주니어(0–2년) **13%** → 약 **2.5배**.
  - 진단 인용: 시니어는 *"better equipped to catch and correct AI's mistakes"* — AI가 "그럴듯하지만 틀린" 코드를 낼 때 시니어가 더 빨리 잡아낸다.
  - 주니어 목소리 (anecdotal): *"It's always hard when AI assumes what I'm doing and that's not the case, so I have to go back and redo it myself."*

### 논쟁 — 한국 커뮤니티의 양쪽 진영 (댓글 원문)

- **GeekNews — "AI가 주니어 개발자를 쓸모없게 만들고 있다"** (원문 beabetterdev.com)
  - URL: https://news.hada.io/topic?id=27162
  - 날짜: 게시 약 4달 전(2026년 상반기 추정 — "확인 필요") · **49P · 댓글 20**
  - 원글 요지(정리된 주장): AI가 주니어에게 '얕은 역량'만 쌓게 한다. 시니어의 진짜 가치는 코딩 속도가 아니라 **실패 패턴 인식**. 처방: 의도적 고군분투, 장애 사례 학습, 이해 못한 코드 배포 금지, AI를 답변기 아닌 **튜터**로.
  - 상반된 댓글 (anecdotal):
    - 【정체 우려】 `snisper`: **"결국 10년후에는 10년차 주니어(powered by AI)가 되는겁니다."** — 1절 evan-moon의 "1년 경험 10번"과 정확히 공명. ★격차 논쟁 오프닝 후보.
    - 【낙관】 `j2sus91`: *"어짜피 과거 공부하던 주니어 개발자라면 AI시대 때에는 더빠른 속도로 시니어급 개발자로 성장할겁니다."*
    - 【협력 프레임】 `skageektp`: *"AI도 실패를 하기 때문에 'AI와 함께 실패하고 함께 극복하는' 사람이 되지 않을까요."*
    - 【도구 아닌 태도 문제】 `kimjoin2`: **"단순 복붙하는 주니어 개발자는 스택오버플로우 시대 때에도 쓸모가 없었습니다."** — "AI 탓이 아니라 자세 문제"라는 반론.
    - 【균형】 `clash4970`: *"결국 사용하는 사람이 어떻게 생각하고 활용하느냐가 중요할 것 같습니다."*

**진단(커뮤니티 합의에 가까운 지점):** 격차 자체보다 **'상호작용 방식'이 결과를 가른다**는 데 양 진영이 은근히 수렴. AI를 오라클로 쓰는 주니어 vs 검증 가능한 조수로 쓰는 시니어. (책 4-3 '위임 다이얼'과 대응)

---

## 3. Java → Python·FastAPI 전환 후기

> **수집 한계 명시:** 이 각도가 가장 얇다. Reddit(r/java·r/Python) 스레드는 WebSearch(US-only)에서 직접 링크 노출이 잘 안 됐다. 아래는 블로그 후기 중심이며, 커뮤니티 raw 토론은 추가 수집 권장("확인 필요").

- **Medium — "FastAPI for Java Developers: Transition from Spring Boot to Python"** (Shaik Reshma)
  - URL: https://medium.com/@shaikreshma21082000/fastapi-for-java-developers-transition-from-spring-boot-to-python-fe2d44d3c623
  - 날짜: 2025-09-01
  - 인용 (전환 문화충격, verbatim):
    - **"FastAPI does not dictate a strict project structure or provide built-in tools like Spring Boot does."** — 스프링의 강한 규약에 익숙한 자바 개발자가 첫 번째로 겪는 충격.
    - *"I felt the need to get comfortable with it, so that the programming language itself never becomes a barrier in my growth."*
    - AI 역할(낙관): *"This is where AI shines: personalized learning that complements your workflow. AI doesn't take your job; it just makes you wonder, how can I use it smarter in my work?"*

- **velog — "FastAPI 써 본 후기"** (koeunyeon)
  - URL: https://velog.io/@koeunyeon/FastAPI-써-본-후기
  - 날짜: "확인 필요"
  - 내용(WebSearch 요약 기반 — **원문 직접 인용 아님, paraphrase**, verbatim 인용 시 재확인 필수):
    - Spring은 규약이 복잡해 누구나 비슷한 형태의 코드를 쓰게 되는 반면, **파이썬은 '코딩 스탠다드'가 없거나 약해 개발자마다 스타일이 크게 갈린다**는 대비.
    - 동적 타입 언어인데도 **타입 힌트(3.5+)**가 IDE 자동완성 등에서 실질적 이점을 준다는 실감.
  - 비고: "타입 없는 세계"의 자유와 불안을 동시에 보여주는 국내 자바 배경 개발자 시각. **원문 정확 인용은 fact-check 후 사용.**

**진단:** 자바 개발자의 전환 통증은 문법이 아니라 **'규약의 부재'와 '타입 안전망의 부재'**에 집중된다. seed 에세이의 TypeScript/타입=공짜 checker 논지와 정확히 반대편 경험 — Python으로 갈 때 잃는 그 checker를 무엇으로 메우나(타입 힌트·Pydantic·테스트)가 학습 포인트.

---

## 4. 주니어 성장 성공·실패 사례

### 성공/의욕 진영 (anecdotal)

- **GeekNews 27162 댓글** `j2sus91`(§2 재인용): 의욕 있는 주니어는 AI로 더 빨리 시니어급으로 → "AI는 의도를 증폭한다"(HN gchamonlive와 동일 논리).
- **velog — "비전공자 AI 엔지니어 부트캠프 후기"** (윤승호)
  - URL: https://velog.io/@yoonsnowdev/251015 · 날짜: 2025-10-17
  - ※ 주의: 이 글은 **AI-'assisted coding'이 아니라 'AI/ML 엔지니어링'을 배우는 부트캠프** 후기다. 각도 4에는 '학습의 고통·정답 부재'의 온도 재료로만 제한 사용.
  - 인용(고군분투의 날것 — anecdotal):
    - **"자다가도 디버깅 생각에 눈이 벌떡 떠지는 병이 생겼고"**
    - *"하루에 5~6시간 자면서 매주 90~100시간을 쏟았는데도 진도를 따라잡을 수가 없었다"*
    - **"인공지능은 진짜 엄청 매우 굉장히 아주 미치도록 어렵다"**
    - **"정답이 제공되지 않았다 ... 내가 개발을 제대로 한 것인지 객관적으로 판단할 수 있는 지표가 없어 답답했다"** — 학습에 '검증 피드백'이 없을 때의 답답함 = 책의 '피드백 환경' 논지와 공명.

### 실패/정체 진영 (anecdotal)

- **GeekNews 27162 댓글** `snisper`: "10년차 주니어(powered by AI)" (§2 재인용) — 정체의 대표 이미지.
- **OKKY(글 목록, 본문 미추출 — 제목/URL만 확보, "본문 확인 필요"):**
  - "Vibe 코딩과 개발자 종말론, 주니어 개발자의 성장 방향에 대한 생각" — https://okky.kr/articles/1530645
  - "요즘 개발자 분들, 특히 주니어 개발자 분들은 이런 고민 많이…" — https://okky.kr/articles/1535768
  - "본 중 제일 실력없는 개발자 썰 좀" — https://okky.kr/questions/1487948
  - ※ OKKY는 SPA/로그인 벽으로 WebFetch 본문 추출 실패. 인용하려면 브라우저 도구로 재수집 필요.

**진단:** 성공/실패를 가르는 변수로 커뮤니티가 반복 지목하는 것은 재능이 아니라 **'AI를 답변기로 쓰나 튜터로 쓰나'** — GeekNews 원글의 처방과 HN 43791474의 휴리스틱이 일치.

---

## 5. 하네스·에이전틱 코딩 실전 팁 (실무 휴리스틱)

- **Hacker News — "Avoiding skill atrophy in the age of AI"**
  - URL: https://news.ycombinator.com/item?id=43791474
  - 날짜: 2025-04-25 · **373 points · 댓글 317** (Algolia 검증)
  - 휴리스틱 (대표 발언, anecdotal):
    - `gchamonlive`: **"LLM changed nothing though. It's just boosting people's intention. If your intention is to learn, you are in luck!"** — "AI는 의도를 증폭할 뿐" ★ 책 전체를 관통하는 한 줄. 오프닝/맺음말 후보.
    - `bsaul`(AI를 검증기로): *"It helps me verify my solution is correct, and when it's not, where is my mistake."* — 답을 받지 말고 **내 답을 먼저 만들고 AI로 검증**(seed 4-1 '선설계 후생성'과 동일).
    - `globnomulous`(교사): 스스로 막다른 길을 헤매는 *"messy process of discovering other avenues, hitting dead ends"*가 학습을 만든다 — 완제 답변은 그걸 건너뛴다.
    - `m000`: 미래 세대가 **"experience required to use AI as a helper, but not depend on it"**을 못 갖출 위험.

- **개인 블로그 — "The day I taught AI to understand code like a Senior Developer"** (Namanyay Goel)
  - URL: https://nmn.gl/blog/ai-understand-senior-developer · 날짜: 2025-04-07
  - 팁: 코드베이스를 평면 파일이 아니라 **계층적 지식 그래프**로 AI에 먹이기(RRS/PRRS — 아키텍처·데이터흐름·보안 렌즈별 요약). 
  - 인용: **"Senior developers focus on 'why' and 'what if'—they maintain a mental model of the entire system and anticipate ripple effects of changes."** — 인간이 유지해야 할 '멘탈 모델'을 명시.

- **evan-moon(§1 재인용):** **"AI 없이도 코드를 판단할 수 있는 개발자"**가 AI를 가장 잘 쓴다 → CLAUDE.md/훅으로 '설명 동봉 요구·설명 가능성 게이트'를 인코딩하라는 seed 4-1과 직접 연결.

- **HN 48139148 `voncheese`(§1 재인용):** 실무자가 실제로 쓰는 4개 습관 리스트(스스로 더 쓰기 / 사고 격상 / 내 경험을 AI에 강제 주입 / AI로 새 기술 더 빨리 학습) — 4장 처방의 야생 버전.

**휴리스틱 요약(반복 등장):** ① 내 답 먼저 → AI로 검증(생성 효과 보존) ② "왜/대안 기각 이유" 설명 동봉 요구 ③ 이해 못한 diff는 배포 금지 ④ AI에 멘탈 모델·컨텍스트를 내가 주입(오라클 취급 금지).

---

## 6. 채용·커리어 불안

### 사실 데이터(매체 보도) — fact-checker 대조 대상

- **CIO — "Demand for junior developers softens as AI takes over"** (Grant Gross)
  - URL: https://www.cio.com/article/4062024/demand-for-junior-developers-softens-as-ai-takes-over.html
  - 날짜: 2025-09-24
  - 수치(fact, 재확인 권장): 최근 CS 졸업자 실업률 6.1%, 컴퓨터공학 7.5%(전체 4.3% 대비 높음). GitHub Copilot ≈ $10/월 vs 주니어 연봉 ≈ $90K 대비 프레임.
  - 인용 (전문가 발언 — 실명이나 예측/의견):
    - `Chirag Agrawal`(시니어 엔지니어): **"Why hire a junior for $90K when GitHub Copilot costs $10?"** ★ 채용 불안 오프닝 후보(단, 도발적 프레임 = 개인 의견).
    - 같은 인물의 처방: **"I'm not trying to out-code AI. I'm making myself essential by leading it with judgment."** — 책의 '최종 판단력' 논지와 공명.
    - `Zeel Jadia`(CEO): *"Fewer people will choose coding as a career, and those who do will command premium pay, like lawyers today."*
    - `Raymond Kok`(Mendix CEO): *"People will move away from being coders to being what I call composers."*
  - 반론(균형): **US BLS는 2024–2034 소프트웨어 개발 직군 15% 성장 전망** — 단기 압박 ≠ 장기 소멸.

### 한국 — 인재 사다리 붕괴 논쟁

- **GeekNews — "주니어 채용 위기: 인재 사다리의 붕괴"** (원문 people-work.io)
  - URL: https://news.hada.io/topic?id=24811
  - 날짜: 약 7달 전(2024 하반기~2025 초 추정, "확인 필요") · **33P · 댓글 6**
  - 댓글 (anecdotal):
    - `scmoon119`: **"10년 후 더 이상 10년 경력자가 없을 때는 사회가 어떻게 될지 궁금하네요."** — OKKY 대표 노상범의 "신입이 없으면 시니어도 없다"와 같은 구조적 우려.
    - `coremaker`: *"이제는 회사나 선배들의 노력을 벗어나, 법이 만들어져야 하는 상황"*
  - 원글이 소개한 국제 토론의 반론: **"AI 채용 둔화는 2024년 이후지만, 주니어 채용 둔화는 2022년에 시작됐다"** → 금리·과잉채용 되돌림 등 거시 교란변수(seed 2절의 Stanford 데이터 해석과 동일한 신중론).

- **추가 국내 소스(제목/URL만, 본문 재수집 필요):**
  - OKKY — "AI 때문에 오늘 해고당함. AI가 슬롭이든 아니든…" — https://okky.kr/articles/1549593 (raw 해고 경험담 — 인용 시 본문 확인 필수)
  - GeekNews — "취업과 소프트웨어는 망했다" — https://news.hada.io/topic?id=30767
  - GeekNews — "AI가 소프트웨어 엔지니어를 대체하지 않은 이유, 그리고 앞으로도 대체하지 못할 이유" — https://news.hada.io/topic?id=30421 (반대 진영)
  - The New Stack — "'AI is disrupting everything': Where do entry-level tech jobs go now?" (Paul Sawers, 2026-06-11) — https://thenewstack.io/ai-junior-developer-hiring/ (본문 미추출)
  - Medium — "AI vs 주니어 그리고 가불기 걸린 카카오" (Jinhwan Kim) — https://jhk0530.medium.com/... (제목만)

---

## 상충하는 목소리 정리 (양 진영 병기 — 책의 '논쟁의 온도')

### 논쟁 A: "AI가 실력을 망친다" vs "그냥 추상화 계층이 올라갈 뿐"
- **망친다 진영:**
  - `iLoveOncall`(HN): "FAANG의 vibe-code 많이 하는 시니어 둘이 스킬을 다 잃었다."
  - `alex5207`(HN): "제2의 천성이던 문법을 잊었다."
  - evan-moon: "뇌는 편하면 기억하지 않는다."
- **괜찮다/추상화 진영:**
  - `largbae`(HN): *"My compiler writing skills atrophied with the advent of high-level languages, but in exchange I got more done."* — 컴파일러 작성 능력 잃었지만 세상은 더 부유해졌다.
  - `devolving-dev`(HN): *"I'm sure people got worse at arithmetic after the invention of the calculator."*
  - `pton_xd`(HN): *"We'll just move to a higher level of abstraction; thinking will be like efficiently coding in assembly, no longer necessary."*
  - `runjake`(HN 42614392): *"No. It's made me a much better and more effective programmer, by a huge amount."*
- **책의 활용법:** 이 논쟁이 seed 3절의 반론("모델 좋아지면 인간 검증 불필요") 및 3답변과 정확히 대응. 커뮤니티가 논쟁의 살아있는 온도를 제공.

### 논쟁 B: "AI로 즐거움을 잃는다" vs "지루함을 위임해 즐거움만 남는다"
- `SirMaster`(HN 43381215): *"I actually like writing the code myself. Like how someone might enjoy knitting... Using AI to generate my code just takes all the fun out of it for me."*
- `popularrecluse`(HN 43381215): *"I've embraced working with LLMs. ... it inspires me to start when I feel in a rut."*
- `Quarrelsome`(HN 48139148): **"I get paid more these days to write less code. ... Im not coding it, but im still thinking it. That's the important part, ain't it? Is it dumb or just clever delegation?"** — ★"바보인가 영리한 위임인가"라는 질문 자체가 책의 핵심 프레임. 오프닝 강력 후보.

### 논쟁 C: 주니어 위기 — "AI 탓" vs "구조/거시경제 탓" vs "자세 탓"
- AI 탓: `snisper`("10년차 주니어"), CIO Agrawal("$10 Copilot").
- 거시/구조 탓: "주니어 둔화는 2022년부터"(GeekNews 24811), BLS 15% 성장 전망.
- 자세 탓: `kimjoin2`("복붙 주니어는 스택오버플로우 시대에도 쓸모없었다").

---

## 챕터 오프닝용 강력 인용 Top 3 (선별)

1. **`Quarrelsome`(HN "AI is making me dumb", 556pt, 2026-05):** *"I get paid more these days to write less code. ... Im not coding it, but im still thinking it. That's the important part, ain't it? Is it dumb or just clever delegation?"* — 책 제목의 질문("바보가 되는가, 함께 성장하는가")을 실무자가 스스로 던진다.
2. **evan-moon(velog, 2026-04):** **"10년을 일해도 1년짜리 경험을 10번 반복하는 것은 10년의 경험이 아니다"** + **"뇌는 편하면 기억하지 않는다"** — 국내 독자용, 논지 1:1 대응.
3. **`gchamonlive`(HN "Avoiding skill atrophy", 373pt, 2025-04):** **"LLM changed nothing though. It's just boosting people's intention."** — AI는 학습 의도를 증폭할 뿐. 처방(다이얼)의 철학적 앵커.

---

## 수집 한계 (정직한 명시)

- **Reddit 직접 스레드 미확보:** WebSearch(US-only)에서 r/ExperiencedDevs·r/cscareerquestions·r/java·r/Python·r/learnprogramming 개별 스레드 URL이 거의 노출되지 않았다. Reddit raw 인용은 **미수집** — 브라우저/전용 도구(agent-reach 등)로 보강 권장. (Red Hat 기사가 재인용한 Reddit 문장 *"AI is still just soooooo stupid and it will fix one thing but destroy 10 other things"* — https://developers.redhat.com/articles/2026/02/17/uncomfortable-truth-about-vibe-coding — 는 2차 인용이므로 원 스레드 추적 필요.)
- **OKKY 본문 미추출:** SPA/로그인 벽으로 WebFetch 실패. 제목·URL만 확보. 인용하려면 재수집 필수(위 §4·§6에 "본문 확인 필요" 표시).
- **HN 개별 댓글 추천수 비공개:** Algolia item API 한계. 스레드 점수만 검증됨.
- **날짜 불확실 항목:** GeekNews "약 N달 전" 상대표기 → 절대 날짜는 "확인 필요"로 표시.
- **언어/플랫폼 편중:** HN(영어)과 velog/GeekNews(한국)에 집중. Lobsters·Mastodon·X·Discord/Slack·커리어리는 이번 라운드 미수집.
- **전 항목 공통:** 익명 개인 주장 = anecdotal. '현장의 온도/공감 재료'로만 쓰고, 수치·연구 인용은 web/paper 리서처·fact-checker가 1차 출처로 교차검증할 것.
