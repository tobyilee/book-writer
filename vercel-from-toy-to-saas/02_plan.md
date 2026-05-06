# Vercel 입문서 — 저술 계획

## 책 제목 후보

1. **토이부터 SaaS까지, Vercel과 함께 자라기** — 부제: *Next.js 개발자가 한 단계씩 올라설 때 Vercel을 어떻게 쓰고, 언제 의심해야 하는가*
   - 톤: 따뜻한 성장 내러티브. "함께 자란다"는 동반자 비유가 책 전체의 페이싱과 일치한다.
   - 포지셔닝: 입문자가 자기 위치를 확인하고 다음 단계를 그릴 수 있게 돕는 안내서.

2. **Vercel 성장 매뉴얼: 첫 배포부터 청구서 폭탄까지** — 부제: *토이·사이드·스타트업·SaaS 단계별로 켜고 끄고 갈아타는 법*
   - 톤: 실전 매뉴얼. "청구서 폭탄"이라는 단어로 후반부의 비판적 시선을 미리 약속한다.
   - 포지셔닝: 단계별 체크리스트가 강한, 운영 의식 있는 입문서.

3. **`vercel deploy`를 누른 다음** — 부제: *프론트엔드 클라우드와 함께 토이 프로젝트를 SaaS로 키우는 4단계 여정*
   - 톤: 코드·터미널 친화적. 한 줄 명령으로 시작해 그 너머로 데려간다는 인상.
   - 포지셔닝: 실무 워크플로 중심, 코드 예시 많은 톤. 개발자 정체성에 가까운 제목.

**추천: 1번 — *토이부터 SaaS까지, Vercel과 함께 자라기***
이유: (a) 책의 척추인 4단계 성장 내러티브가 제목 한 줄에 그대로 실린다, (b) 부제에서 "어떻게 쓰고, 언제 의심해야 하는가"로 후반부의 함정·대안 챕터까지 약속한다, (c) "함께 자라기"라는 동반자 메타포는 Toby 스타일의 청유형·공감 톤과 결이 맞는다, (d) 입문자에게 위협적이지 않으면서도 토이로 끝나는 책이 아님을 분명히 한다.

---

## 책 특성

- **장르**: 실용 입문서 (에세이형 기술서). 단순 레퍼런스가 아니라 "성장하는 개발자의 동반자" 형식. 챕터 도입은 공감·상황 가정으로 시작하고, 본문은 명령·설정·트레이드오프를 다루며, 마지막은 "이 단계에서 다음 단계로 넘어가는 신호"로 닫는다.
- **분량**: 본문 9개 챕터 + 서문·에필로그·부록. 챕터 평균 16~24페이지(한글 약 8,000~12,000자), 전체 본문 약 200페이지(약 100,000자). 부록·서문·에필로그 포함 약 240페이지. 챕터별 합: 14+16+18+22+26+22+24+22+24 = **208p**(±5p 허용).
- **난이도**: 초·중급. JS/TS, React, Next.js의 기본 문법과 빌드 흐름은 안다고 가정한다. 클라우드·서버리스·CDN 개념은 모르거나 흐릿하다고 가정하고 매번 짧게 풀어준다.
- **학습 목표 (다 읽고 나면 독자가 할 수 있는 것)**:
  1. 자기 프로젝트가 어느 성장 단계(토이/사이드/스타트업/SaaS)에 있는지 진단하고, 그 단계에 맞는 Vercel 설정을 적용할 수 있다.
  2. Vercel의 핵심 추상화(빌드 파이프라인, 함수 런타임, 렌더링 전략, 엣지 네트워크)를 자기 언어로 설명하고 트레이드오프를 따져볼 수 있다.
  3. 청구서 폭탄·preview 노출·시크릿 누출 같은 대표 함정을 사전에 차단하는 가드레일을 자기 프로젝트에 켤 수 있다.
  4. Cloudflare·자가호스팅·OpenNext 같은 대안의 위치를 이해하고, 비상 탈출(`output: "standalone"`) 빌드를 평소에 손에 둘 수 있다.
  5. "이 기능을 켜야 할까?"라는 질문에 비용·보안·운영 부담 세 축으로 답할 수 있다.
- **독자 여정 (Before → After)**:
  - **Before**: `vercel deploy` 한 줄로 첫 배포는 해봤다. 작동은 한다. 그런데 환경 변수는 어디 두는지, ISR이 뭔지, 청구서가 갑자기 왜 늘어나는지, 뉴스에서 본 보안 사고가 내 일인지, 다른 플랫폼도 봐야 하는지 — 어느 것 하나 자신 있게 답할 수 없다. Vercel 문서는 너무 방대해 어디부터 봐야 할지 모른다.
  - **After**: 자기 프로젝트의 단계를 안다. 그 단계에서 켜야 할 가드레일과 끄지 말아야 할 기능을 안다. 청구서를 미리 시뮬레이션할 수 있다. preview·시크릿·DDoS 시나리오를 머릿속에서 미리 한 번씩 굴려본 적이 있다. 다음 단계가 오면 무엇을 점검해야 하는지, 언제 Vercel을 떠나야 하는지에 대한 자기 기준이 있다.

---

## 챕터 구성

### Chapter 1. 처음 막힌 자리에서 시작하자
- **핵심 질문**: 첫 배포는 왜 그렇게 쉬웠고, 그 다음은 왜 갑자기 어려운가?
- **주요 내용**:
  - "vercel을 처음 써본 새벽"의 공감 도입 — 5분 만에 배포된 황홀함과, 그 다음 마주한 환경 변수·도메인·청구 화면의 막막함
  - 이 책이 답하려는 질문 4개 (개념·운영·비용·탈출)
  - 책의 척추: 토이 → 사이드 → 초기 스타트업 → SaaS의 4단계와, 각 단계가 던지는 다른 질문
  - **독자 위치 진단 체크리스트 강화판**: PV·결제 여부·팀원 수·시크릿 민감도에 더해 "한 달 cron 횟수, 이미지 처리량, 글로벌 사용자 비중, AI 호출 여부" 4축 추가 — 자기 좌표를 5분 안에 찍을 수 있게
  - 이 책을 읽는 두 가지 방법: 처음부터 쭉 / 자기 단계 챕터부터
  - **이 책이 답하지 *않는* 것** 한 단락 — Next.js 문법, RSC 깊이, AWS 일반 비교, Cloudflare 자체 학습. 9장 대안 비교의 무게를 명확히 하기 위한 사전 못박음
  - 코드 표기·인용·기준 시점(2026-05)·가격 변동성에 대한 약속
- **예상 분량**: 14페이지 / 약 7,000자
- **Ref**: §0(서문 격), §3 전체 윤곽, §10 (기준 시점·변동성 환기)

### Chapter 2. Vercel을 한 번 더 정의해 보자 — 개념 지도
- **핵심 질문**: "Frontend Cloud"라는 말 뒤에 실제로 어떤 추상화가 묶여 있는가?
- **역할 약속**: 이 장은 **추상화 지도**다. 각 추상화를 "이런 게 있다 + 책의 어디서 자세히 다룬다"의 깊이로만 다룬다. 심층 비교·메커니즘은 후속 챕터에서.
- **주요 내용**:
  - Vercel = Git push 한 번으로 묶이는 빌드·배포·CDN·SSL·preview·서버리스 함수의 매니지드 PaaS
  - 엣지 네트워크와 PoP — 왜 글로벌 사용자에게 빠른가, 그리고 왜 항상 빠른 건 아닌가 (Edge가 정말 빠른가의 *조건부* 논쟁은 9장에서)
  - 빌드 파이프라인의 한 장 흐름도 (push → preview URL → main merge → production)
  - 함수 런타임 3종 **개요만** (Node / Edge / Fluid가 무엇이고 언제 등장하는지). **심층 비교(Node API 제약, Fluid I/O 무료, AI 워크로드 이득)는 6장 SaaS 시뮬레이션과 7장 과금에서**
  - 렌더링 전략 4종 (SSG / SSR / ISR / PPR) — 이름과 한 줄 정의. `revalidate = 60`의 흔한 오해는 9장 함정에서 다시
  - Preview Deployment의 정체와 폭발 반경 — *위험*은 8장에서
  - Next.js와 Vercel의 관계 — "왜 Next.js만 first-class처럼 보이는가" (Lock-in 논쟁의 본격 분석은 9장)
  - **장 마지막 한 장: "도구 분담 표"** — Sensitive 플래그·Spend Management·WAF·BotID·Edge Middleware·Fluid·Cron Jobs·AI Gateway가 각각 어느 챕터에서 *처음 등장하고* 어디서 *깊이* 다뤄지는지를 한 표로 못박음 (HIGH 2 반영)
- **예상 분량**: 16페이지 / 약 8,000자 (기존 22p → 16p로 압축, 심층 비교 후속 이전)
- **Ref**: §1.1, §1.2, §1.3, §1.4(개요), §1.5(개요), §1.6, §6.4·§6.5는 9장으로 이전

### Chapter 3. 토이 단계 — 무료로 살아남기
- **핵심 질문**: 무료 플랜으로 무엇까지 할 수 있고, 어디서부터 위험해지는가?
- **주요 내용**:
  - Hobby 플랜의 한도 (Bandwidth 100GB / Invocations 1M / Active CPU 4h / Memory 360 GB-hrs)
  - "비상업적 용도"의 진짜 경계 — AdSense 한 줄, Stripe, 후원 링크가 만드는 ToS 신호
  - 토이에서 반드시 켜야 할 5가지: Git 자동 배포, 기본 도메인, Sensitive env 플래그, robots.txt, Deployment Protection
  - 결제 카드를 일부러 등록하지 않는 가드레일 전술
  - Cron Job 1일 1회 한도가 답답해지는 시점의 의미 — 사이드/스타트업에서 cron이 실제로 무엇을 돌리는지(scheduled fetch·ISR 갱신·DB 정리)는 4·5장에서
  - 토이 단계에서 비용·보안은 어떻게 다루는가 (질문을 단순화하기)
  - "다음 단계로 넘어가는 신호" 체크리스트
- **예상 분량**: 18페이지 / 약 9,000자
- **Ref**: §3.1, §4.1(Hobby 행), §4.5(가드레일), §5.1(Sensitive), §5.2(Preview 노출), §6.9(비상업 ToS), §1.6

### Chapter 4. 사이드 단계 — Pro로 올라가는 순간
- **핵심 질문**: 첫 결제, 첫 팀원, 첫 cron — 무엇이 트리거이고 무엇을 먼저 켜야 하는가?
- **분담 규칙**: 이 장에서 Spend Management·Sensitive 플래그·Edge Middleware는 **"언제·왜 켜는가"** 한 문단까지. 임계 알림 설정 페이지·시크릿 회전 절차·미들웨어 폭주 사례는 7·8장에서.
- **주요 내용**:
  - Pro로 올라가는 4가지 트리거 (결제 / 회사 명함 / cron 다회 / 팀원)
  - Pro 플랜 구조 ($20/seat, 1TB, 10M edge requests, ~1,000 GB-hrs)
  - **Spend Management — 만들자마자 켜는 한 가지** (디폴트 OFF의 함정 — *왜* 켜는가만, 임계·웹훅 설정은 7장)
  - 환경별 시크릿 분리 (Production / Preview / Development) 실전 워크플로의 시작
  - `vercel env pull`과 `.env.local` 동기화 패턴 — 사용법 중심으로
  - Sensitive 플래그 — 의심 시 모두 켜는 규칙 (사고 해부와 회전 절차는 8장)
  - **Cron Jobs 다회 사용 패턴**: scheduled DB 정리, 외부 API 폴링, ISR `revalidatePath` 트리거, 알림 발송 — 함수 quota 차감의 비용 함의 한 단락
  - **OG Image Generation**: Next.js `ImageResponse` API + Vercel 엣지로 동적 OG 카드 만들기 — 사이드 단계 SEO/공유 차별화
  - Web Analytics·Speed Insights는 정말 필요할 때만 — 프로젝트당 $10이 쌓이는 산수
  - Edge Middleware로 Basic Auth·rate limit·redirect 룰 짜기 (무거운 로직 금지 원칙은 8장)
  - 사이드 단계의 비용·보안 미니 점검표
- **예상 분량**: 22페이지 / 약 11,000자
- **Ref**: §3.2, §4.1(Pro 행), §4.5, §5.1, §5.3(Edge Middleware), §2.3(env), §2.5(CLI), §2.8(Analytics·Speed Insights·OG Image·Cron Jobs)

### Chapter 5. 초기 스타트업 단계 — 한도가 처음 흔들릴 때
- **핵심 질문**: 트래픽이 만 단위를 넘기 시작하면 비용 곡선은 왜 꺾이는가, 어떻게 펴는가? 그리고 AI 기능을 붙일 때 Vercel은 어떤 위치에 서는가?
- **분담 규칙**: 비용 폭증 메커니즘은 *현상과 외부 보강*까지. 함수 과금 3축 손계산·DDoS 회색 지대는 7장에서. WAF/BotID는 *언제 켜는가*만, Managed Ruleset 깊이는 8장에서.
- **주요 내용**:
  - 비용이 폭증하는 5대 항목 다시 보기 (Bandwidth, Image, Edge Requests, Seat, Add-on) — 사이드와 무엇이 다른가
  - 청구서 폭탄 케이스 스터디 1: $20 → $700 → $120 (caching 도입) — *원인 분류*까지, 손계산은 7장
  - 청구서 폭탄 케이스 스터디 2: LLM 봇 크롤링 + Image API
  - 외부 보강 패턴 1: 이미지를 외부 CDN(Cloudflare R2 / ImgIX / Bunny)으로 분리 — 80% 절감 사례
  - 외부 보강 패턴 2: 도메인 → Cloudflare → Vercel — WAF·DDoS 흡수와 ISR 캐시 헤더 호환 주의
  - 외부 보강 패턴 3: DB는 Marketplace Storage(Neon, Upstash, Supabase) 또는 직접
  - Edge Config로 read-mostly 메타데이터 분리 (피처 플래그·차단 IP·리다이렉트)
  - Turborepo Remote Cache로 빌드 시간 줄이기
  - **AI 기능을 붙일 때 — Vercel AI SDK·AI Gateway**: 다수 모델(OpenAI / Imagen / Flux / Recraft) 단일 API 라우팅, 인증·응답 포맷 자동, 토큰 기반 + Vercel 마진의 *추정 한계*. 스타트업 단계에서 AI를 빠르게 붙일 때의 DX 이득과 가격 투명도 비판을 균형 있게 (HIGH 1 반영)
  - 이 단계의 보안 룰북 *시작*: WAF Custom Rules, BotID, Attack Challenge Mode를 *언제 켜는가* (메커니즘은 8장)
- **예상 분량**: 26페이지 / 약 13,000자 (AI 절 추가)
- **Ref**: §3.3, §4.3, §4.4, §4.5, §2.6(Turborepo), §2.7(외부 CI), §2.8(Edge Config·WAF·BotID·AI Gateway), §5.4, §5.5, §8.1

### Chapter 6. SaaS 단계 — Pro 한도를 넘는 순간의 결정들
- **핵심 질문**: Enterprise로 갈까, 멀티 호스트로 분산할까, 셀프호스트로 내려갈까?
- **분담 규칙**: 이 장은 *결정의 장*이다. **함수 런타임 3종의 심층 비교(2장에서 미뤄둔 것)와 Fluid의 메커니즘**을 여기서 본격적으로 다룬다 — SaaS 비용·운영 결정에 직접 결합되기 때문.
- **주요 내용**:
  - SaaS 단계의 신호 (bandwidth 5TB+, 함수 GB-hours 수천, 팀원 10명+, 컴플라이언스 요구, 99.99% SLA)
  - Enterprise가 더해주는 것 — SCIM·SSO·Audit Log·Secure Compute·HIPAA·24/7
  - 컴플라이언스 지도 (SOC 2 Type 2 / ISO 27001 / PCI DSS / HIPAA / GDPR / DORA)
  - **함수 런타임 3종 심층 비교 (2장에서 미뤄둔 것)**: Node API 전체 vs Edge 제약(no fs, no `require()`, fetch/crypto.subtle/Web Streams 한정) vs Fluid의 단일 인스턴스 다중 요청·bytecode 최적화·pre-warming 메커니즘
  - **Fluid compute가 AI 워크로드에 주는 진짜 이득**: I/O 대기 시간 무료 과금 → AI 에이전트·외부 API 폴링·LLM 스트리밍에서의 비용 곡선 변화. 5장 AI Gateway 절과 직결
  - 함수 비용 3축으로 시뮬레이션하기 (Invocations / CPU-hour / Memory) — *시나리오 적용*까지, 손계산 기초는 7장에서 다시 정리
  - 분기점 점검 3종: 비용 vs 인프라 엔지니어 인건비 / 데이터 주권(EU·HIPAA) / Vercel-only 기능 의존도
  - **Enterprise 컨택 시 준비 자료** (한도 협상 → 좁힌 절): 현재 사용량 dump, 예상 성장 곡선, 컴플라이언스 요건 목록, 비상 탈출 옵션 — 1차 자료 없는 협상 노하우 대신 "준비물 체크리스트"로 (리뷰 MED 6 반영)
  - 이 단계의 운영 의식: OpenTelemetry 연동, 함수별·라우트별 사용량 분해
- **예상 분량**: 24페이지 / 약 12,000자 (런타임 심층 비교 흡수)
- **Ref**: §3.4, §4.1(Enterprise), §4.2, §4.6, §1.4(Fluid 본격), §6.5(Edge 제약), §5.7(컴플라이언스), §2.4(팀·역할)

### Chapter 7. 비용 — 청구서가 폭발하기 전에
- **핵심 질문**: 어떤 항목이 폭증하는가, 어떻게 미리 본다, 어떻게 자동으로 막는가?
- **도입 콜백**: "지금까지 단계마다 한 페이지씩 비용을 이야기했다. 4장의 Spend Management '왜 켜는가', 5장의 Bandwidth·Image 폭증 사례, 6장의 Fluid 시뮬레이션 — 이제 그 페이지들을 한 자리에 놓고 손으로 계산해 보자." (리뷰 MED 4 반영)
- **주요 내용**:
  - 단계 챕터에서 흩어진 비용 메모 한 장 모음 (4장 Spend ON / 5장 5대 항목·외부 보강 / 6장 함수 3축·Fluid)
  - 플랜 구조 한 장 정리 (Hobby / Pro / Enterprise)와 단계 매핑
  - 함수 과금 3축 ($0.60/1M invocations, $0.128/CPU-hour, $0.0106/GB-hour) 손으로 계산해 보기 — 6장 시뮬레이션의 *기초 산수*판
  - **Fluid 과금의 손계산**: I/O 대기 무료가 실제 청구서에 미치는 차이 — AI 에이전트 시나리오 한 페이지
  - Bandwidth가 가장 빨리 새는 이유 — 1TB는 20-50만 PV, 바이럴 한 번이면 끝
  - Image Optimization 폭증 메커니즘과 LLM 크롤러 시대
  - Edge Requests / Seat / Add-on의 누적 패턴
  - **Spend Management 임계 알림 + 자동 일시정지 + 웹훅** 설정 한 페이지 가이드 (4장의 약속을 여기서 결판)
  - **Attack Challenge Mode** — 무료, 챌린지 차단 트래픽은 미과금
  - DDoS 청구 사례와 mitigation 발동 전 처리분의 회색 지대
  - "legitimate mistake forgive" 정책의 한계 — 명시 SLA가 없다는 사실
  - 매주·매월 점검할 모니터링 루틴
- **예상 분량**: 22페이지 / 약 11,000자
- **Ref**: §4 전체, §5.5(DDoS), §8.1(케이스), §1.4(Fluid 과금)

### Chapter 8. 보안 — 시크릿·Preview·사고에서 살아남기
- **핵심 질문**: 환경 변수·preview·도메인·DDoS — 어디가 가장 새기 쉽고 무엇을 바꿔야 하는가?
- **도입 콜백**: "3장에서는 Sensitive 플래그를 켰다. 4장에서는 의심 시 모두 켜는 규칙을 정했다. 5장에서는 WAF·BotID를 *언제 켜는가*만 결정했다. 이제 그 결정들 뒤에 어떤 메커니즘과 어떤 사고가 있었는지 본다." (리뷰 MED 4 반영)
- **주요 내용**:
  - 단계 챕터에서 흩어진 보안 메모 한 장 모음 (3장 Sensitive 켜기 / 4장 의심 시 모두 / 5장 WAF·BotID 켜기)
  - 환경 변수의 두 종류 — Sensitive vs non-sensitive의 *구조적 차이* (decrypt 가능 여부)
  - 2026년 4월 Vercel 사고 해부 (Context.ai 직원 PC → Lumma Stealer → Google Workspace OAuth → Vercel 내부 → non-sensitive env enumerate·decrypt)
  - 사고에서 배운 것: non-sensitive에도 비밀이 살고 있다(DB URL·signing key), 회전 + 재배포가 정답
  - 시크릿 회전 절차 — 모든 환경에서 재배포가 왜 필수인가
  - Preview 환경 폭발 반경 통제 — production 시크릿 재사용 금지의 실전
  - `*.vercel.app` 인덱싱 차단 (robots.txt + Deployment Protection: SSO·Password·Allowlist)
  - 도메인·SSL 자동화의 안전망 (Let's Encrypt 자동 갱신·5일 전 백업 발급)과 사람이 챙겨야 할 것 (외부 등록 도메인 갱신)
  - WAF Managed Rulesets·BotID·Attack Challenge Mode의 *메커니즘* (5장의 *언제 켜는가* 결판)
  - Edge Middleware에 무거운 로직을 넣지 말아야 하는 이유 — fetch/헤더 조작 전용, 그 이상은 Route Handler로
  - **컴플라이언스가 비기술 의사결정에 들어오는 두 시나리오**: (a) B2B 엔터프라이즈 계약 — 보안 questionnaire에서 SOC 2 Type 2 / ISO 27001 요구, (b) 의료 SaaS — HIPAA + Secure Compute(Enterprise 전용) 강제 (리뷰 LOW 9 반영)
- **예상 분량**: 22페이지 / 약 11,000자
- **Ref**: §5 전체, §6.8, §8.3, §2.3, §2.2

### Chapter 9. 함정·대안·비상 탈출 — 의심하는 법
- **핵심 질문**: Vercel을 잘 쓰면서도 언제든 떠날 수 있는 능력은 어떻게 갖추는가?
- **주요 내용**:
  - 자주 빠지는 함정 정리: 런타임 한도(Edge 25/300s, Node 800s, body 4.5MB), Cold Start, Turborepo 캐시 invalidation, **ISR `revalidate` 오해(2장에서 미뤄둔 것)**, **Edge Node API 제약(2장에서 미뤄둔 것 — pdfkit·sharp·bcrypt 등)**
  - Vendor Lock-in 논쟁 두 관점 — "사실상 종속"(eduardoboucas, dev.to) vs "70%가 외부에서 운영"(Vercel anti-lock-in)
  - Next.js 16.2 stable Adapter API가 바꾼 풍경 (Cloudflare·Netlify·Amplify·Google·OpenNext 공동 설계)
  - 대안 한 줄 매트릭스 — Cloudflare / Netlify / AWS Amplify / Render / Fly.io / 자가호스팅(Coolify·Dokku·CapRover)
  - 결정 휴리스틱 4줄 (글로벌 트래픽 / AWS 통합 / 비용 통제 / Next.js 풀 기능)
  - 비상 탈출 능력: `output: "standalone"` Docker 이미지 100-200MB 빌드 평소에 익혀두기
  - OpenNext의 위치와 한계 (Image Optimization·ISR·Middleware의 reduced fidelity)
  - Edge가 정말 빠른가 — DB 위치·placement-cost-latency triangle (Cassel et al. 2025, Pinto et al. 2023)
  - 학술 백본 한 페이지 (Mahmoudi 2024 cold start 메타분석, RFC 5861, Firecracker NSDI '20)
  - **그래도 Vercel이 빛나는 자리**: Claude.ai 운영 사례, AI Gateway가 다중 모델 통합을 한 줄로 끝내는 DX, PPR이 50ms 미만 TTFB와 부분 동적성을 동시에 달성하는 첫 모델인 이유 — 비판으로만 닫지 않기 위한 옹호 한 절 (리뷰 LOW 8 반영)
  - 기준 시점 환기 — 가격·기능·기본값은 변한다, 출간 시점에 다시 검증할 것
  - **닫는 글: 다시 그 새벽으로 — 같은 한 줄, 다른 무게**: 1장의 `vercel deploy` 새벽 장면을 호명하며, 이제 같은 명령 뒤에 4단계 척추·과금 3축·시크릿 두 종류·탈출 옵션이 함께 보이는 자리에서 책을 닫는다 (리뷰 MED 5 반영)
- **예상 분량**: 24페이지 / 약 12,000자
- **Ref**: §6 전체, §7 전체, §8.2(Lock-in 논쟁), §8.4(Edge 논쟁), §8.6(학술), §10(리서치 한계)

### 부록 (선택)
- A. Vercel CLI 치트시트 (`vercel`, `vercel dev`, `vercel env pull`, `vercel deploy --prebuilt`, `vercel link`)
- B. 단계별 가드레일 체크리스트 (토이/사이드/스타트업/SaaS 한 장 요약)
- C. 청구서 폭탄 응급 대응 플로우차트
- D. 참고 문헌·URL 모음 (Reference §9 전체)

---

## 도구 분담 표 (2장 끝에 본문으로 삽입)

각 도구는 **단계 챕터에서 *언제·왜* 켜는가**까지 다루고, **메커니즘·설정 페이지·사고 분석은 home 챕터**에서 다룬다. 이 규칙으로 같은 도구가 여러 번 등장해도 독자가 깊이를 헷갈리지 않게 한다.

| 도구 | 처음 등장 | Home (깊이) | 핵심 한 줄 |
|------|-----------|-------------|-----------|
| Sensitive 환경 변수 플래그 | 3장 (켜기) | **8장** (구조·사고·회전 절차) | UI에서 다시 못 읽는 게 단점이 아니라 보안 자산 |
| Spend Management | 4장 (왜 켜는가, 디폴트 OFF) | **7장** (임계·자동 일시정지·웹훅 설정) | Pro 만들자마자 켜는 한 가지 |
| Cron Jobs | 3장 (한도 한계) | **4장** (실제 쓰임 패턴·quota 차감) | 함수 quota를 차감한다는 비용 함의 |
| OG Image Generation | — | **4장** (사이드 SEO/공유) | Next.js `ImageResponse` + Vercel 엣지의 동적 카드 |
| Edge Middleware | 4장 (Basic Auth·rate limit·redirect) | **8장** (무거운 로직 금지·메커니즘) | fetch/헤더 조작 전용, 그 이상은 Route Handler |
| Edge Config | 5장 (read-mostly 메타데이터 분리) | **5장** | p50 1ms 미만, 피처 플래그·차단 IP·리다이렉트 룰 |
| Turborepo Remote Cache | 5장 | **5장** | 모노레포 affected 빌드, invalidation 함정은 9장 |
| WAF Custom Rules | 5장 (켜기) | **8장** (Managed Ruleset·BotID 메커니즘) | Bot/AI Bot/BotID/Custom 4종 |
| BotID | 5장 (켜기) | **8장** | invisible fingerprint, Middleware metadata로 rate limit 결합 |
| Attack Challenge Mode | 5장 (켜기) | **7장** (무료·차단 트래픽 미과금) | 모든 플랜 무료 가드레일 |
| AI Gateway / AI SDK | **5장** (스타트업의 AI 붙이기) | **5장** + 6장 호명 (Fluid I/O 무료의 AI 이득) | 다수 모델 단일 API + 마진 투명도 비판 |
| Fluid compute | 2장 (개요) | **6장** (메커니즘 심층) + 7장 (과금 손계산) | I/O 대기 무료, AI 워크로드 비용 곡선 변화 |
| 함수 런타임 3종 | 2장 (개요) | **6장** (심층 비교) | Node API 전체 vs Edge 제약 vs Fluid 다중 처리 |
| Deployment Protection | 3장 (켜기) | **8장** (SSO·Password·Allowlist·preview 인덱싱 차단) | preview를 production-급 폭발 반경으로 만들지 말기 |
| Image Optimization | 3장 (`<Image>` 등장) | **5장** (외부 CDN 분리 80% 절감) + 7장 (LLM 크롤러 폭증) | 가장 폭증하기 쉬운 단일 항목 |

---

## 내러티브 아크

이 책의 척추는 **"한 명의 개발자가 자기 프로덕트를 키우면서 Vercel과 어떻게 관계 맺는지"**의 4단계 여정이다. 챕터는 기능별로 나뉘지 않고, **독자의 위치별**로 나뉜다.

**1막 — 자리 잡기 (1~2장)**: 책은 독자의 "처음 막힌 순간"에서 시작한다. 5분 만에 배포가 끝난 황홀함 다음에 마주하는 막막함을 환기하고, 책의 4단계 척추와 핵심 질문 4가지(개념·운영·비용·탈출), 그리고 *이 책이 답하지 않는 것*까지 못박는다. 2장은 한 발 물러서서 Vercel의 추상화 지도를 그린다 — **단, "지도" 깊이까지만**. 함수 런타임 3종의 심층 비교는 6장 SaaS의 비용 결정과 결합해서 다루는 게 자연스럽고, ISR·Edge 제약의 함정은 9장에서 결판을 본다. 2장 마지막에는 **도구 분담 표**가 들어가 독자가 "어디서 무엇을 깊게 다루는지" 한눈에 알게 한다. **이 두 장은 어느 단계 독자에게도 공통이다.**

**2막 — 단계별 여정 (3~6장)**: 토이 → 사이드 → 초기 스타트업 → SaaS 순으로 한 챕터씩 간다. 각 챕터는 같은 구조를 따른다 — (a) 이 단계의 트리거 신호, (b) 플랜과 한도, (c) 켜야 할 가드레일·운영 패턴, (d) 이 단계에서 비용·보안은 어떻게 다른가, (e) 다음 단계로 넘어가는 신호. 같은 리듬을 반복하기에 독자는 자기 위치만 잡으면 어디로 점프해도 길을 잃지 않는다. 단계가 올라갈수록 다루는 도구의 수가 아니라 **운영 의식의 깊이**가 깊어진다. 토이에서는 "켜기"가 중심이고, 사이드에서는 "분리하기 + Cron·OG Image 활용", 스타트업에서는 "외부 보강 + AI 기능 붙이기", SaaS에서는 "분기 결정 + 런타임/Fluid 메커니즘"이 중심이다. 비용·보안 도구는 단계 챕터에서 *언제·왜 켜는가*까지만 다루고, 메커니즘·설정·사고는 7·8장을 위해 아낀다 (도구 분담 표 참고).

**3막 — 횡단 주제 (7~8장)**: 비용과 보안은 단계 챕터에서 부분적으로만 다뤘다. 두 장 모두 **첫 절을 명시적 콜백**으로 연다 — "지금까지 단계마다 한 페이지씩 비용/보안을 이야기했다. 그 페이지들을 한 자리에 놓고 결판을 보자." 7장은 4장의 "Spend 왜 켜는가", 5장의 5대 항목·외부 보강, 6장의 Fluid 시뮬레이션을 모아 함수 과금 3축을 손으로 계산하고 Spend Management 설정 페이지까지 보여준다. 8장은 3장의 "Sensitive 켜기", 4장의 "의심 시 모두", 5장의 "WAF·BotID 켜기"를 모아 2026년 4월 사고를 해부하고 메커니즘과 절차를 결판 낸다. 이 두 장은 **운영 의식의 두 기둥**을 굳힌다.

**4막 — 의심하기 (9장)**: 마지막 장은 톤이 바뀐다. 그동안 Vercel을 어떻게 잘 쓰는지 배웠다면, 이제 **언제 Vercel을 떠날 수 있는가**를 묻는다. 함정·런타임 한도·Cold Start·ISR 오해·Edge Node API 제약·Lock-in 논쟁·대안 매트릭스·비상 탈출 빌드까지. 다만 비판으로만 닫지 않기 위해 후반에 **"그래도 Vercel이 빛나는 자리"** 한 절을 두어 Claude.ai 운영, AI Gateway DX, PPR 같은 옹호 사례로 균형을 맞춘다. 이 장은 비판이 아니라 **자기 결정권의 회복**이다. 그래야 1장에서 약속한 네 번째 질문 — "탈출" — 이 닫힌다. 마지막 절 **"닫는 글: 다시 그 새벽으로 — 같은 한 줄, 다른 무게"** 가 1장의 새벽 장면을 호명하며, 같은 `vercel deploy` 한 줄이 이제 다르게 보이는 자리에서 책을 닫는다.

**페이싱 (총 208p)**: 1장 14p — 짧고 가볍게, 진단 체크리스트와 "답하지 않는 것" 단락 추가. 2장 16p — 22→16으로 *압축*해 입문자가 3장 진입 전 지치지 않도록 하고, 함수 런타임 심층 비교는 6장으로 이전. 3장 18p — 토이의 가드레일. 4장 22p — 사이드의 분리·Cron·OG Image. 5장 26p — 가장 길다, 외부 보강 3종 + AI Gateway 절 흡수. 6장 24p — SaaS 결정 + 런타임 심층 + Fluid 메커니즘. 7장 22p — 비용 결판 + Fluid 손계산. 8장 22p — 보안 결판 + 컴플라이언스 시나리오. 9장 24p — 함정·대안·옹호·닫는 글까지 가장 길지만 톤이 가벼운 형식이라 부담이 덜.

**연결과 콜백**: 각 단계 챕터의 "다음 단계 신호"는 다음 챕터의 도입과 자연스레 이어진다. 7·8장은 **첫 절에서 명시적 콜백**(4·5·6장의 어떤 절을 모았는지)으로 열어 "약속과 시작이 어긋나는" 위험을 차단한다. 5장의 AI Gateway 절은 6장의 Fluid I/O-bound 메커니즘과 7장의 Fluid 손계산으로 두 번 다시 호명된다. 9장의 마지막 절은 **항목으로 명시된 1장 콜백** ("닫는 글: 다시 그 새벽으로")으로 책의 수미상관을 보장한다. 챕터를 건너뛰며 읽어도 손해가 적고, 처음부터 읽으면 같은 개념이 점점 깊어지는 나선형 학습이 된다.
