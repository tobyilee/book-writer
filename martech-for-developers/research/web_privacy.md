<!-- 검색 시점: 2026-07-25 기준 -->
# 프라이버시·동의·아이덴티티·규제 리서치 (web #3)

검색 수행일: **2026-07-25**
담당 축: E-1 브라우저 정책 / E-2 서버사이드 태깅 / E-3 동의 관리 / E-4 아이덴티티 / E-5 클린룸 / E-6 규제 / E-7 코드에 남는 흔적
슬러그: `martech-for-developers` · 장르: `tech-book` · 대상 독자: 한국 개발자

> **작성 규율 (fact-checker 대조 기준)**
> - 이 문서의 모든 날짜·버전·조문 번호·정책 상태는 **2026-07-25에 실제로 fetch한 페이지**에서만 가져왔다.
> - fetch하지 못한 항목은 `확인 불가 (미조회)` 또는 `조문 원문 미확인`으로 명시했다.
> - 페이지 수집 도구가 요약 모델을 거치므로, **원문 그대로임이 확실한 문장만 따옴표로 인용**했고 나머지는 `요지:`로 표기했다. 챕터에 직접 인용할 때는 `요지:` 항목을 따옴표로 감싸지 마라.
> - **이 축은 2025~2026년에 여러 번 뒤집혔다.** 기억으로 쓰면 거의 틀린다. 아래 "기억과 달랐던 항목"을 먼저 읽어라.

---

## ⚠️ 먼저 읽을 것 — 2026-07-25 기준 "기억과 다른" 핵심 5가지

| # | 흔한 오해 (2024년까지의 상식) | 2026-07-25 기준 실제 |
|---|---|---|
| 1 | "Chrome이 서드파티 쿠키를 없앤다" | **폐지 계획 자체가 철회됐다.** 2025-04-22 Google이 "현재 방식 유지" 발표, 별도 프롬프트도 안 띄운다 |
| 2 | "Privacy Sandbox가 쿠키를 대체한다" | **Privacy Sandbox 광고 API 대부분이 폐기됐다.** 2025-10-17 Topics·Protected Audience·Attribution Reporting 등 은퇴 발표, Chrome 144(2026-01-13)에서 deprecate, M150에서 제거 예정 |
| 3 | "IAB TCF는 v2.2가 최신" | **v2.3.** 2026-03-01부터 `disclosedVendors` 세그먼트 없는 TC String은 무효 |
| 4 | "정보통신망법 스팸 위반은 과태료" | **2026-07-07 시행 개정법(법률 제21305호)으로 과징금 도입** — 매출액 6% 이하 |
| 5 | "EU AI Act는 2026-08-02에 전면 적용" | AI Omnibus로 일부 고위험 규정이 **2027-12-02 / 2028-08-02로 연기**됐다 |

---

## E-1. 서드파티 쿠키·브라우저 정책 현재 상태

### E-1-1. Chrome / Google — 두 번의 대반전

**변화 궤적 (이 책이 개발자에게 설명해야 하는 "왜 이렇게 됐나"):**

```
2020~2023  Privacy Sandbox 제안, 서드파티 쿠키 단계적 폐지 로드맵 발표
2024-01    Chrome 사용자 1%에 서드파티 쿠키 기본 차단 테스트 시작
   ↓
2025-04-22 반전 ①: "폐지 안 한다" — 현재 선택 방식 유지, 별도 프롬프트 없음
   ↓
2025-10-17 반전 ②: Privacy Sandbox 광고 API 대부분 은퇴 (같은 날 영국 CMA도 규제 약속 해제)
   ↓
2026-01-13 Chrome 144 stable — Protected Audience / Private Aggregation / Shared Storage deprecate
   ↓
2026-06-12 Topics API 사용률 4.9% of page loads (blink-dev 스레드 갱신)
   ↓
M150       제거 예정 (Topics, Protected Audience, Private Aggregation)
```

**① 서드파티 쿠키 폐지 철회 (2025-04-22)**
- 출처: <https://privacysandbox.google.com/blog/privacy-sandbox-next-steps> | 발행일 **2025-04-22** | 저자 Anthony Chavez (VP, Privacy Sandbox) | 검색 시점 2026-07-25
- 신뢰성: **최상** (Google 공식 1차 소스)
- 인용:
  > "not be rolling out a new standalone prompt for third-party cookies"
  > "made the decision to maintain our current approach to offering users third-party cookie choice in Chrome"
- 요지: 이유로 업계 이해관계자 간 견해차, 프라이버시 강화 기술 채택 가속, 전 세계 규제 환경 변화를 들었다. Privacy Sandbox API에 대해서는 "may have a different role to play in supporting the ecosystem"이라며 로드맵 재검토를 예고했다.
- **트라젝토리 주의:** 이 글은 "IP Protection을 2025년 3분기에 런칭하겠다"고 했으나, 아래 ②의 상태 페이지에서는 IP Protection이 **Discontinue (Do Not Launch)** 로 뒤집혔다. 6개월 만의 번복 — 이 축을 기억으로 쓰면 안 되는 이유의 교과서적 사례다.
- 관련 섹션: 챕터 오프닝 훅, "왜 서버사이드로 갔나"의 전제

**② Privacy Sandbox 기술 은퇴 (2025-10-17)**
- 출처: <https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies> | 발행일 **2025-10-17** | 저자 Anthony Chavez | 검색 시점 2026-07-25
- 신뢰성: **최상**
- 인용:
  > "After evaluating ecosystem feedback about their expected value and in light of their low levels of adoption, we've decided to retire the following Privacy Sandbox technologies."
  > "We've heard clearly from marketers and publishers the importance of scaled measurement solutions to understand the impact of advertising campaigns."
- **은퇴 목록 (원문 열거):** Attribution Reporting API, IP Protection, On-Device Personalization, Private Aggregation, Shared Storage, Protected Audience, Protected App Signals, Related Website Sets, SelectURL, SDK Runtime, Topics
- **계속 지원:** CHIPS, FedCM, Private State Tokens
- 관련 섹션: "표준 대체재가 사라진 뒤 남은 것" — 이게 서버사이드/퍼스트파티로의 압력을 오히려 키운 지점

**③ 기능별 현재 상태 (공식 status 페이지)**
- 출처: <https://privacysandbox.google.com/overview/status> | 페이지 최종 갱신 **2025-10-17** | 검색 시점 2026-07-25
- 신뢰성: **최상**
- ⚠️ **신선도 주의:** 이 status 페이지의 최종 갱신일은 2025-10-17이다. 2026년 갱신본은 **확인 불가 (미조회)**. 아래 M144/M150 마일스톤은 별도의 2026년 소스(Chrome 릴리스 노트·blink-dev)로 교차 확인했다.

| 구분 | 기능 |
|---|---|
| **계속 지원 (Continue to Support)** | CHIPS (Chrome 114+ 기본 지원), FedCM (Chrome 108 shipped), Fenced Frames (GA), Private State Tokens, Storage/Network State Partitioning, Storage Access API (Chrome 119+ 기본), User-Agent Client Hints, User-Agent Reduction, Bounce Tracking Mitigations |
| **폐기·제거 예정 (Deprecate and Remove)** | Aggregation Service, Attribution Reporting, Private Aggregation, **Protected Audience**, Related Website Sets, Shared Storage, **Topics** |
| **출시 안 함 (Discontinue / Do Not Launch)** | **IP Protection**, Partitioned Popins, Fenced Storage Read, Private Proofs, Probabilistic Reveal Tokens, Script Blocking |
| **Android** | Attribution Reporting, On-Device Personalization, Protected App Signals, Protected Audience, SDK Runtime, Topics — 전부 phaseout 예정 |

**④ 실제 제거 마일스톤 (2026년 소스)**
- 출처: <https://developer.chrome.com/release-notes/144> | Chrome 144 **stable 릴리스 2026-01-13** | 검색 시점 2026-07-25 | 신뢰성 **최상**
  - 요지: Chrome 144 릴리스 노트에 Private Aggregation API, Shared Storage API, Protected Audience API의 deprecation이 명시돼 있다. 세 API 모두 "서드파티 쿠키 현행 유지 발표에 따라 Chrome이 해당 API를 deprecate·remove할 계획"이라는 취지의 동일 문구를 쓴다. ⚠️ 이 문구는 수집 도구가 세 항목을 합쳐 재구성한 것이라 **원문 그대로가 아니다 — 따옴표로 인용하지 마라.** 직접 인용이 필요하면 릴리스 노트를 다시 열어라.
  - ⚠️ Topics, Attribution Reporting, Related Website Sets는 이 릴리스 노트의 deprecation 섹션에는 등장하지 않았다.
- 출처: <https://groups.google.com/a/chromium.org/g/blink-dev/c/_R85yctz4Rs> ("Intent to Deprecate and Remove: Topics API") | 최초 게시 **2025-11-08** | 저자 Yao Xiao | 검색 시점 2026-07-25 | 신뢰성 **최상** (Chromium 공식 프로세스)
  - "Deprecate in M144", "remove in M150"
  - 최초 제안 시점 사용률: "Currently, ~13% of page loads use Topics API"
  - **2026-06-12 갱신 사용률: "Currently the usage is 4.9% of page loads"** ← 2026년 dated 근거
- 출처: <https://groups.google.com/a/chromium.org/g/topics-api-announce/c/iQX7PC3S0Ds> (PSA) | 게시 **2025-12-05** | 저자 Sam Dutton | 신뢰성 **최상**
- **M150의 실제 stable 릴리스 날짜: 확인 불가 (미조회)** — chromiumdash.appspot.com/schedule은 JS 렌더링이라 본문 추출 실패. 챕터에 M150 날짜를 쓰지 마라.

**⑤ 영국 CMA의 규제 약속 해제 (2025-10-17)**
- 출처: <https://www.gov.uk/cma-cases/investigation-into-googles-privacy-sandbox-browser-changes> / 결정문 PDF <https://assets.publishing.service.gov.uk/media/68f213ce06e6515f7914c728/Decision_to_release_the_commitments_previously_accepted_by_the_CMA_in_respect_of_Google_s_Privacy_Sandbox_proposals.pdf> | 결정일 **2025-10-17** | 검색 시점 2026-07-25 | 신뢰성 **최상** (영국 정부 공식) — ⚠️ 결정문 PDF 본문은 미조회, 검색 결과 요약 기준
- 요지: CMA는 2022년 2월 Google의 Privacy Sandbox 관련 약속(commitments)을 수용했으나, Google이 서드파티 쿠키 제한 계획을 철회하면서 원래의 경쟁 우려가 더 이상 성립하지 않는다고 판단, 2025-10-17 약속을 해제했다.
- **개발자용 서사 포인트:** Privacy Sandbox는 "프라이버시 프로젝트"였던 동시에 "경쟁법 감시 대상"이었다. 규제가 풀린 날과 API가 죽은 날이 같은 날이다.
- 관련 섹션: "Martech은 왜 기술만으로 설명되지 않는가"

### E-1-2. Safari / WebKit — ITP

**① ITP 최초 도입 (2017)**
- 출처: <https://webkit.org/blog/7675/intelligent-tracking-prevention/> | 발행 **2017-06-05** | 저자 John Wilander | 신뢰성 **최상**
- 인용:
  > "Intelligent Tracking Prevention is a new WebKit feature that reduces cross-site tracking by further limiting cookies and other website data."
  > "A machine learning model is used to classify which top privately-controlled domains have the ability to track the user cross-site, based on the collected statistics."
- 분류기가 쓰는 세 가지 통계 벡터 (원문): "subresource under number of unique domains, sub frame under number of unique domains, and number of unique domains redirected to"
- 초기 시간 규칙 (원문 인용):
  > "If the user has not interacted with example.com in the last 30 days, example.com website data and cookies are immediately purged."
  > "If the user interacted with example.com the last 24 hours, its cookies will be available when example.com is a third-party."
  > "If the user interacted with example.com the last 30 days but not the last 24 hours, example.com gets to keep its cookies but they will be partitioned."
- ⚠️ **구버전 정보 주의:** 위 24시간/30일 규칙은 2017년 초기 설계다. 2020년 전면 차단으로 대체됐다(아래 ②). 챕터에서는 "초기에는 이랬다"는 역사 서술로만 써라.

**② 서드파티 쿠키 전면 차단 (2020)**
- 출처: <https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/> | 발행 **2020-03-24** | 저자 John Wilander | 신뢰성 **최상**
- 인용:
  > "Cookies for cross-site resources are now blocked by default across the board."
  > "Safari continues to pave the way for privacy on the web, this time as the first mainstream browser to fully block third-party cookies by default."
  > "ITP has aligned the remaining script-writable storage forms with the existing client-side cookie restriction, deleting all of a website's script-writable storage after seven days of Safari use without user interaction on the site."
- **7일 삭제 대상 스토리지:** IndexedDB, LocalStorage, Media keys, SessionStorage, Service Worker registrations and cache
- 요지: ITP 분류기는 계속 동작하며 bounce tracker, tracker collusion, link decoration tracking을 탐지한다. delayed bounce tracking 탐지 로직도 추가됐다.
- **개발자 함의:** `localStorage`에 넣은 익명 방문자 ID가 7일 뒤 사라진다. 이게 "왜 우리 재방문 식별률이 계속 떨어지나"의 기술적 정답이다.

**③ CNAME 클로킹 방어 (2020)**
- 출처: <https://webkit.org/blog/11338/cname-cloaking-and-bounce-tracking-defense/> | 발행 **2020-11-12** | 저자 John Wilander | 신뢰성 **최상**
- 인용:
  > "CNAME stands for canonical name record and maps one domain name to another as part of the Domain Name System, or DNS."
  > "ITP now detects third-party CNAME cloaking requests and caps the expiry of any cookies set in the HTTP response to 7 days."
- 요지: 사이트 소유자가 서브도메인을 서드파티 도메인으로 CNAME 매핑하면, 그 서드파티가 퍼스트파티와 같은 권한을 얻는다. WebKit은 연구에서 "1,762 websites CNAME cloaking 56 trackers in total"이 확인됐다고 밝혔고, 프라이버시뿐 아니라 보안 문제도 지적했다 — "250 websites of banks, healthcare companies, restaurant chains, and civil rights groups had been compromised" (CNAME 레코드 관리 부실).
- 탐지 조건 요지: 퍼스트파티 서브리소스의 CNAME이 퍼스트파티 도메인과도, top frame host의 CNAME과도 다를 때 적용된다.
- **이게 E-2 서버사이드 태깅의 CNAME 논쟁에 대한 브라우저 벤더의 공개 입장이다.** 서버사이드 태깅을 CNAME으로 구현하면 Safari에서 쿠키 수명이 7일로 잘린다.
- 관련 섹션: E-2와 반드시 교차 참조

### E-1-3. Firefox — Total Cookie Protection

- 출처: <https://blog.mozilla.org/en/products/firefox/firefox-rolls-out-total-cookie-protection-by-default-to-all-users-worldwide/> | 발행 **2022-06-14** (업데이트 2024-08-28) | 신뢰성 **최상**
- 인용:
  > "creating a separate 'cookie jar' for each website you visit"
  > "Any time a website, or third-party content embedded in a website, deposits a cookie in your browser, that cookie is confined to the cookie jar assigned to only that website."
- 요지: 2022년 6월 전 세계 Firefox 데스크톱 사용자에게 기본값으로 롤아웃됐다. 차단이 아니라 **파티셔닝**이다 — 쿠키를 없애는 게 아니라 사이트별 항아리에 가둬 크로스사이트 연결을 끊는다.
- ⚠️ `support.mozilla.org/en-US/kb/total-cookie-protection`은 로드 실패 — Firefox **버전 번호는 확인 불가 (미조회)**. 또한 위 발표는 **데스크톱** 기준이다. Android·iOS Firefox의 현재 기본값은 **확인 불가**. 챕터에서 "Firefox는 기본으로 파티셔닝한다"고 쓸 때 플랫폼을 한정하라.
- **개발자 함의:** Chrome의 CHIPS(`Partitioned` 쿠키 속성)와 같은 방향. "서드파티 쿠키가 있냐 없냐"가 아니라 "파티션 키가 뭐냐"로 문제가 옮겨갔다.

### E-1-4. Apple — ATT / SKAdNetwork / AdAttributionKit

**① App Tracking Transparency**
- 출처: <https://developer.apple.com/app-store/user-privacy-and-data-use/> | 신뢰성 **최상** | 발행일 표기 없음 (상시 갱신 정책 페이지) | 검색 시점 2026-07-25
- **Apple의 "tracking" 정의 (원문 인용) — 이 정의가 챕터의 핵심 인용이다:**
  > "Tracking refers to the act of linking user or device data collected from your app with user or device data collected from other companies' apps, websites, or offline properties for targeted advertising or advertising measurement purposes. Tracking also refers to sharing user or device data with data brokers."
- tracking 예시 (원문 인용):
  > "Placing a third-party SDK in your app that combines user data from your app with user data from other developers' apps to target advertising or measure advertising efficiency, even if you don't use the SDK for these purposes."
- 요구사항 (원문 인용):
  > "In iOS 14.5, iPadOS 14.5, and tvOS 14.5 or later, you need to receive the user's permission through the AppTrackingTransparency (ATT) framework in order to track them or access their device's advertising identifier."
  > "Unless you receive permission from the user to enable tracking, the device's advertising identifier value will be all zeros and you may not track them as described above."
- **개발자 함의:** 거부 시 IDFA가 `00000000-0000-0000-0000-000000000000`. null이 아니라 **0으로 채워진 유효한 형태의 UUID**다. 이걸 그대로 ID 그래프에 넣으면 전 세계 거부 사용자가 한 사람으로 병합된다 — E-4의 over-merge 사례로 그대로 쓸 수 있다.

**② ATT 프레임워크 API**
- 출처: <https://developer.apple.com/documentation/apptrackingtransparency> (JSON: `/tutorials/data/documentation/apptrackingtransparency.json`) | 신뢰성 **최상** | 검색 시점 2026-07-25
- 인용:
  > "Request user authorization to access app-related data for tracking the user or the device."
  > "You must use the AppTrackingTransparency framework if your app collects data about end users and shares it with other companies for purposes of tracking across apps and web sites."
- API: `requestTrackingAuthorization(completionHandler:)`, `trackingAuthorizationStatus`
- Info.plist 키: `NSUserTrackingUsageDescription` — "A message that informs the user why an app is requesting permission to use data for tracking the user or the device."
- 플랫폼 가용성 (공식 표): iOS 14.0 / iPadOS 14.0 / Mac Catalyst 14.0 / macOS 11.0 / tvOS 14.0 / visionOS 1.0

**③ SKAdNetwork ↔ AdAttributionKit**
- ⚠️ **정밀도 낮음.** `developer.apple.com/documentation/adattributionkit/adattributionkit-skadnetwork-interoperability` 본문 추출 실패 (SPA). 아래는 developer.apple.com 도메인 한정 검색 결과 요약 수준이다.
- 요지 (신뢰성 **중** — 원문 미확인): AdAttributionKit은 SKAdNetwork를 대체(deprecate)하는 게 아니라 그 위에 얹혀 상호운용된다. SKAdNetwork에 이미 등록된 광고 네트워크는 별도 등록이 필요 없다고 안내된다. AdAttributionKit은 WWDC24에서 소개됐다(<https://developer.apple.com/videos/play/wwdc2024/10060/>).
- **챕터에 SKAdNetwork의 deprecation 여부·버전 번호·conversion value 비트 수를 쓰지 마라. 전부 확인 불가 (미조회).**

### E-1-5. 이 변화가 만든 기술적 귀결 — ⚠️ 오독 금지

Privacy Sandbox가 죽었다고 **서드파티 쿠키가 정상으로 돌아온 게 아니다.** 2026-07-25 기준 실제 상태:

- Safari: 서드파티 쿠키 **기본 전면 차단** (2020년부터, 변함 없음)
- Firefox: **사이트별 파티셔닝** 기본값 (2022년부터, 변함 없음)
- Chrome: 폐지는 안 하지만 **1% 테스트 그룹과 사용자 선택 UI는 유지**, CHIPS로 파티션 쿠키 표준화
- Privacy Sandbox: 표준화된 **대체 API가 사라졌다**

→ 결론: **문제는 그대로인데 표준 해법만 없어졌다.** 그래서 압력은 오히려 커졌다 — 퍼스트파티 데이터, 로그인 기반 식별, 서버사이드 수집, 벤더 종속적 클린룸으로. 이게 E-2~E-5가 존재하는 이유다.

---

## E-2. 서버사이드 태깅 / 수집 아키텍처

### E-2-1. Google Tag Manager 서버사이드

- 출처: <https://developers.google.com/tag-platform/tag-manager/server-side> | 신뢰성 **최상** | 발행일 표기 없음 | 검색 시점 2026-07-25
- 인용:
  > "Server-side tagging is a way to instrument your tags to measure user activity wherever it happens."
  > "Server containers use the same tag, trigger, and variable model that you're used to, while also providing new tools."
- 공식이 내세우는 세 가지 이점 (원문 항목): "Improve page performance", "Unlock more detailed user privacy controls", "Improve data quality"

- 출처: <https://developers.google.com/tag-platform/tag-manager/server-side/send-data> | 신뢰성 **최상**
- **client 정의 (원문 인용) — 서버사이드 태깅의 핵심 개념:**
  > "Clients are adapters between the software running on a user's device and your server-side Tag Manager container. They receive measurement data from a device, transform that data into one or more events, process the data in the container, and package the results to be sent back to the device."
- 퍼스트파티 도메인 관련 (원문 인용):
  > "To send data in a true first-party context, you need to serve Google scripts, such as the Google Analytics library, from your own servers."
- 전송 방식 요지: GA4 태그는 Image pixel, Fetch API, XHR, 그리고 서버 컨테이너 도메인에서 로드된 iframe 안에서 도는 Service Worker를 transport로 지원한다.

**개발자 관점 정리:**
- 브라우저 → **내 도메인**(태깅 서버) → Google/Meta/기타 벤더. 브라우저는 서드파티 도메인을 직접 안 본다.
- 그래서 광고 차단기의 도메인 블록리스트와 ITP의 서드파티 규칙을 우회한다 — 그리고 **바로 그 이유로 CNAME 클로킹 논쟁이 붙었다**(E-1-3 참조).

### E-2-2. Meta Conversions API

- 출처: <https://developers.facebook.com/docs/marketing-api/conversions-api> | 신뢰성 **최상** | 검색 시점 2026-07-25
- 인용:
  > "designed to create a connection between an advertiser's marketing data...from an advertiser's server, website platform, mobile app, or CRM to Meta systems"
- 요지: 서버 이벤트는 Meta Pixel이나 iOS/Android SDK로 보낸 이벤트와 "processed like events sent using the Meta Pixel"이라고 명시된다.
- ⚠️ **정직한 표기:** 이 공식 문서 페이지에는 "광고 차단기 때문에 만들었다"는 문장이 **없다**. 브라우저 제약을 CAPI의 존재 이유로 쓸 때는 Meta 공식 진술이 아니라 업계 통설로 표기하라. (`(사실 확인 필요)` 마커 대상)

### E-2-3. 중복 제거 (dedup) — 개발자가 실제로 짜는 부분

- 출처: <https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events> | 신뢰성 **최상** | 검색 시점 2026-07-25
- **권장 방식 (원문 인용):**
  > "We determine if events are identical based on their **ID** and **name**. So, for an event to be deduplicated:
  > 1. In corresponding events, a Meta Pixel's `eventID` must match the Conversion API's `event_id`.
  > 2. In corresponding events, a Meta Pixel's `event` must match the Conversion API's `event_name`."
- **폴백 방식 (원문 인용):**
  > "If you have configured the `external_id` and/or `fbp` parameters to be passed via both browser and server, we take care to remove duplicate events automatically."
- **시간 창 (원문 인용) — 이 48시간이 챕터에 쓸 구체 수치다:**
  > "If we find the same server key combination (`event_id` and `event_name`) **and** browser key combination (`eventID` and `event`) sent to the same Pixel ID within 48 hours, we discard the subsequent events."
  > "events are only deduplicated if they are received within 48 hours of when we receive the first event with a given `event_id`"

**챕터에 쓸 개발자 서사:**
> 브라우저에서도 보내고 서버에서도 보낸다. 둘 다 보내는 이유는 브라우저 쪽이 30~40% 잘려나가기 때문이고, 둘 다 보내면 같은 구매가 두 번 카운트된다. 그래서 주문 ID 같은 걸로 `event_id`를 만들어 양쪽에 똑같이 실어 보낸다 — 이게 martech 백엔드 개발자가 입사 첫 주에 만나는 코드다. 48시간 창을 넘기는 지연 배치 잡을 짜면 중복이 그대로 통과한다.

**어떤 걸 브라우저에서, 어떤 걸 서버에서 보내나 (설계 원칙 정리 — 출처 없는 저자 정리로 표기할 것):**
- 브라우저만 아는 것: 페이지 URL, referrer, 클릭 ID(`fbclid`/`gclid`), 브라우저 쿠키(`_fbp`), 화면·UA
- 서버만 아는 것: 확정된 주문 금액, 결제 성공 여부, 환불, 로그인 사용자 ID, 오프라인 전환
- 양쪽에 필요한 것: `event_id` (dedup 키), 동의 상태

### E-2-4. 상충 지점 — 서버사이드 태깅의 "프라이버시 강화" 주장

- Google 공식 문서는 서버사이드 태깅의 이점으로 "Unlock more detailed user privacy controls"를 든다.
- WebKit은 CNAME 클로킹을 **추적 회피 수법**으로 규정하고 쿠키 수명을 7일로 캡한다.
- **두 입장은 정면으로 충돌한다. 병기하고 결론 내지 마라.** 챕터에서는 "같은 아키텍처가 벤더 문서에서는 프라이버시 강화로, 브라우저 벤더 블로그에서는 회피 수법으로 불린다"는 긴장 자체를 보여주는 게 정직하다.

---

## E-3. 동의 관리 (CMP)

### E-3-1. IAB Europe TCF — 현재 v2.3

- 출처: <https://iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/> | 발행 **2025-06-19** | 신뢰성 **최상** (IAB Europe 공식)
- **현재 버전: v2.3** (기억이 흔히 "v2.2"라고 답하는 지점)
- 핵심 변경 요지: 벤더가 Special Purposes와 Legitimate Interest 기반 Purposes를 동시에 선언할 때, LI 비트가 0이면 "공개 안 함"인지 "사용자가 거부함"인지 구분이 안 되는 모호성이 있었다. v2.3은 **`disclosedVendors` 세그먼트를 필수화**해 이 모호성을 해소한다.
- **날짜 (원문 인용):**
  > "Starting 1st March, 2026: Any TC String created without the disclosedVendor segment will be deemed invalid."
  - 전환 기간 종료: **2026-02-28**. 이후 생성된 `disclosedVendors` 없는 TC String은 무효.
- v2.2 배경 (출처: <https://iabeurope.eu/tcf/>, <https://iabeurope.eu/tcf-2-2-launches-all-you-need-to-know/> | 신뢰성 최상 | 발행 2023):
  - v2.2 출시일 **2023-05-16**. 벨기에 DPA가 검증한 Action Plan을 반영한 개정.
  - 요지: Purpose 3·4·5·6(개인화 광고/콘텐츠 프로필 생성·이용)에 대해 **Legitimate Interest를 법적 근거로 선택할 수 없게** 하고 consent만 허용. 법률 용어를 사용자 친화적 설명 + 실사용 예시로 교체. 벤더는 수집 데이터 범주·보유 기간·정당한 이익을 추가 공개. CMP는 첫 화면에 법적 근거를 구하는 **벤더 총수**를 표시. "모두 동의" 원클릭 버튼이 있으면 재방문 시 **"모두 철회" 원클릭**도 동등하게 제공해야 함.
- 관련 섹션: "동의는 UI가 아니라 프로토콜이다" — TC String이라는 인코딩된 문자열이 광고 요청에 실려 다닌다는 걸 개발자에게 보여주는 대목

### E-3-2. Google Consent Mode

- 출처: <https://developers.google.com/tag-platform/security/concepts/consent-mode> | 신뢰성 **최상** | 검색 시점 2026-07-25
- ⚠️ **버전 표기 주의:** 이 공식 개요 문서는 파라미터를 나열할 뿐 "v2"라는 버전 라벨을 문서 제목에서 쓰지 않는다. 챕터에서 "Consent Mode v2"라고 쓸 거면 "2023년 11월에 `ad_user_data`·`ad_personalization` 두 파라미터가 추가된 개정"이라는 사실 기준으로 쓰는 게 안전하다.
- **파라미터 전체 (공식 문서 원문 정의):**

| 파라미터 | 원문 정의 |
|---|---|
| `ad_storage` | "Enables storage, such as cookies (web) or device identifiers (apps), related to advertising." |
| `ad_user_data` | "Sets consent for sending user data to Google for online advertising purposes." |
| `ad_personalization` | "Sets consent for personalized advertising." |
| `analytics_storage` | "Enables storage, such as cookies (web) or device identifiers (apps), related to analytics, for example, visit duration." |
| `functionality_storage` | "Enables storage that supports the functionality of the website or app, for example, language settings" |
| `personalization_storage` | "Enables storage related to personalization, for example, video recommendations" |
| `security_storage` | "Enables storage related to security such as authentication functionality, fraud prevention, and other user protection" |

- 추가 신호: `ads_data_redaction` — 요지: 사용자가 동의를 거부했을 때 저장된 광고 데이터를 삭제하도록 하는 설정
- **Basic vs Advanced (원문 인용) — 개발자가 실제로 고르는 갈림길:**
  - Basic: "Prevent Google tags from loading until a user interacts with a consent banner", "no data transferred to Google prior to user interaction" → "general model (less detailed modeling)"
  - Advanced: "Google tags load when a user opens the website or app", 동의 전에도 기본 동의 설정 하에서 "measurements without cookies"를 전송 → "advertiser-specific model (more detailed modeling)"
- **챕터 포인트:** Advanced 모드는 "동의 안 했는데도 뭔가 보낸다"이고, 그 대가로 더 정교한 전환 모델링을 받는다. 이 트레이드오프를 개발자가 코드 한 줄로 정하게 되는 게 martech의 특징적 긴장이다. (EEA 트래픽에 대한 EU user consent policy 요구사항은 <https://support.google.com/tagmanager/answer/13695607> — ⚠️ 본문 미조회)

### E-3-3. Global Privacy Control (GPC)

- 출처: <https://www.w3.org/TR/gpc/> | **Working Draft, 발행일 2026-06-11** | 신뢰성 **최상** (W3C 공식) | 검색 시점 2026-07-25
- **상태: W3C Working Draft** (Recommendation 아님). 2024년 11월 W3C Privacy Working Group의 공식 work item으로 채택돼 표준화 진행 중. (work item 채택 시점은 검색 결과 기반 — 신뢰성 중)
- **HTTP 헤더 (원문 인용):**
  > "The `Sec-GPC` header field is a mechanism for expressing a person's general universal preference for a do-not-sell-or-share interaction in HTTP requests (for any request method)."
  ```
  Sec-GPC-field-name  = "Sec-GPC"
  Sec-GPC-field-value = "1"
  ```
- **DOM 프로퍼티 (원문 인용):**
  > "The `globalPrivacyControl` property enables a client-side script to determine what `Sec-GPC` header field value was sent when loading the top-level browsing context's active document."
  - `Navigator`와 `WorkerNavigator` 양쪽에 readonly boolean으로 노출.
- **개발자 함의:** DNT(Do Not Track)와 달리 GPC는 **법적 구속력이 있다** — 캘리포니아에서는 반드시 존중해야 한다(E-6-5). 즉 `req.headers['sec-gpc'] === '1'` 한 줄이 법적 의미를 갖는 첫 헤더다. 챕터에서 DNT의 실패와 대비시키면 좋다.

### E-3-4. 개발자가 실제로 구현하는 것 (저자 정리 — 출처 없음, 사실 주장 아님)

- 동의 신호를 **어디까지 전파해야 하나**: 브라우저 태그 → 서버 컨테이너 → 이벤트 스트림 → 웨어하우스 → 다운스트림 활성화(광고 플랫폼 오디언스 싱크). 한 곳이라도 빠지면 "동의 철회했는데 광고가 계속 따라온다"가 된다.
- **동의 철회 시 이미 수집된 데이터**: 스트림(Kafka 등)에 이미 흘러간 이벤트, 웨어하우스 파티션, 벤더 쪽에 이미 싱크된 오디언스, 백업 스냅샷 — 네 군데를 다 처리해야 한다. E-7에서 이어감.
- ⚠️ 위 두 항목은 이 리서치에서 **1차 출처로 확인한 사실이 아니다.** 챕터에서 수치나 단정 없이 설계 서술로만 쓰라.

---

## E-4. 아이덴티티 레졸루션 / ID 그래프

### E-4-1. 결정적 vs 확률적 매칭

- 출처: <https://liveramp.com/uk/blog/probabilistic-vs-deterministic-matching>, <https://docs.liveramp.com/connect/en/deterministic-matching.html>, <https://segment.com/blog/identity-resolution/> | 신뢰성 **중~최상** (벤더 공식 문서 + 벤더 블로그) | ⚠️ **본문 미조회 — 검색 결과 요약 기준. 아래 문구를 따옴표로 인용하지 마라.**
- **결정적(deterministic) 요지:** 이미 알고 있는 식별자(이메일, 전화번호, 디바이스 ID, 사용자 ID)의 일치로 병합한다. 관측된 데이터에 근거하므로 "이 사용자가 그걸 했다"를 확신할 수 있다. 정밀도(precision)가 높다.
- **확률적(probabilistic) 요지:** 예측 알고리즘으로 "아마 같은 사람일 것"을 추정한다. 디바이스 핑거프린팅, IP 매칭, 화면 해상도, OS, 위치, Wi-Fi 네트워크, 행동·브라우징 데이터를 통계 모델에 넣어 일정 신뢰수준에서 묶는다. 정밀도는 낮지만 결정적 데이터가 없을 때 **커버리지(scale)**를 얻는다.
- **한 줄 대비 (저자 정리 — 인용 아님):** 결정적은 *이 사용자가 그걸 했다*(관측·확실), 확률적은 *이 사용자가 그걸 할 것이다*(추정·신뢰구간).
- **개발자 번역 (저자 정리):** 결정적 매칭은 조인 키가 있는 `JOIN`이고, 확률적 매칭은 유사도 임계값이 있는 `fuzzy match`다. 후자는 임계값 하나 잘못 잡으면 서로 다른 사람이 한 프로필로 합쳐진다.

### E-4-2. ID 그래프 자료구조 관점 (저자 정리 — 1차 출처 없음)

⚠️ 아래는 이번 리서치에서 벤더 문서로 확인한 내용이 **아니다.** 개발자 독자를 위한 설계 서술로만 쓰고, 수치나 "업계 표준" 같은 단정은 붙이지 마라.

- ID 그래프는 노드(식별자: 쿠키 ID, 디바이스 ID, 이메일 해시, 로그인 ID, 전화번호)와 엣지(관측된 동시 등장)로 이루어진 그래프다. 프로필 하나 = 연결 컴포넌트 하나.
- 병합은 사실상 **union-find(disjoint set)**다. 새 관측이 들어오면 두 컴포넌트를 union한다.
- **union은 되돌리기 어렵다** — 이게 실무 위험의 핵심이다. 잘못 합쳐진 두 사람을 다시 떼려면 병합 이력 전체를 재생(replay)해야 한다. 그래서 성숙한 시스템은 병합 결과가 아니라 **관측 이벤트 원장**을 진실의 원천으로 두고 그래프를 파생물로 재계산한다.
- **오병합(over-merge)의 대표 트리거:**
  - 공용 기기 (가족 태블릿, 매장 키오스크, 사무실 공용 PC)
  - 널·플레이스홀더 식별자 — ATT 거부 시의 all-zero IDFA(E-1-4), `null` 문자열, `test@example.com`
  - 이메일 별칭·역할 계정 (`info@`, `noreply@`)
  - 기기 초기화 후 광고 ID 재발급
- **미병합(under-merge)의 대표 트리거:** 익명 세션에서 장바구니에 담고 로그인 후 결제 — 로그인 순간 익명 프로필과 회원 프로필을 잇지 못하면 "첫 구매 고객"으로 잘못 분류된다.
- **익명 → 로그인 전환 시 프로필 병합**이 martech 개발자가 가장 자주 만나는 실전 문제다. 로그인 콜백에서 익명 ID와 회원 ID를 alias 이벤트로 묶고, 그 전에 쌓인 이벤트를 소급 재귀속(backfill)할지 말지를 정해야 한다.

### E-4-3. 대체 식별자 — UID2

- 출처: <https://unifiedid.com/docs/intro> | **문서 최종 갱신 2026-07-23** (검색 시점 이틀 전 — 매우 신선) | 신뢰성 **최상** (프로젝트 공식 문서)
- 인용:
  > "UID2 is a framework that enables deterministic identity for advertising opportunities on the open internet"
- 요지: 웹사이트·모바일 앱·CTV를 아우르며, 인증된 통합 경로(certified integration paths)로 토큰을 관리·교환한다. 프로젝트는 활발히 유지되고 있고 다수의 통합 가이드·SDK·엔드포인트가 제공된다.
- 라이선스 (원문 인용): "All work and artifacts are licensed under the Apache License, Version 2.0"
- ⚠️ **미확인 항목 — 챕터에 쓰지 마라:** raw UID2가 이메일/전화번호에서 어떻게 파생되는지(해싱·솔팅 절차), 토큰의 정의와 회전 주기, RampID의 현재 상태. 전부 **확인 불가 (미조회)**. `unifiedid.com/docs/intro`의 개요 섹션에는 해당 설명이 없었다.
- **이메일 해시(SHA-256)의 현재 상태: 확인 불가 (미조회).** 챕터에서 "SHA-256 이메일 해시가 업계 표준 식별자다"라고 단정하지 마라. 다만 UID2가 스스로를 "deterministic identity" 프레임워크로 규정한다는 사실은 인용 가능하다.
- **개발자용 논점 (저자 정리):** 이메일을 SHA-256으로 해싱해도 그건 익명화가 아니라 **가명화**다. 같은 이메일은 항상 같은 해시가 되므로 여전히 조인 키다. 이 구분이 E-6의 가명정보 논의와 바로 연결된다.

---

## E-5. 데이터 클린룸

### E-5-1. AWS Clean Rooms — 가장 상세하게 문서화된 1차 소스

- 출처: <https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html> | 신뢰성 **최상** | 발행일 표기 없음 (상시 갱신 문서) | 검색 시점 2026-07-25
- **정의 (원문 인용):**
  > "AWS Clean Rooms helps you and your partners analyze and collaborate on your collective datasets to gain new insights without revealing underlying data to one another."
  > "When you run queries or jobs, AWS Clean Rooms reads data from that data's original location and applies built-in analysis rules to help you maintain control over that data."
- **내장 통제 수단 (원문 목록 인용):**
  > - "Analysis rules to restrict SQL queries and provide output constraints."
  > - "Cryptographic Computing for Clean Rooms to keep data encrypted, even as queries are processed, to comply with stringent data handling policies."
  > - "Analysis logs to review queries and jobs in AWS Clean Rooms and help support audits."
  > - "Differential privacy to protect against user-identification attempts. AWS Clean Rooms Differential Privacy is a fully-managed capability that protects the privacy of your users with mathematically-backed techniques and intuitive controls that you can apply in a few steps."
  > - "AWS Clean Rooms ML to allow two parties to identify similar users in their data without the need to share their data with each other."
- **동작 방식 (원문 인용) — 개발자가 이해할 워크플로:**
  > "In AWS Clean Rooms, you create a collaboration and add the AWS accounts that you want to invite, or create a membership to join a collaboration that you've been invited to. You then link the data resources needed for your use case: configured tables for event data, configured dataset associations for ML training and inference data, configured models for ML modeling, or ID namespaces for entity resolution. You have the option to create or approve analysis templates to agree in advance on the exact queries and jobs that you want to allow in a collaboration."
- **주목:** "ID namespaces for entity resolution" — 클린룸과 아이덴티티 레졸루션(E-4)이 같은 제품 안에서 만난다. AWS Entity Resolution과의 연동도 명시돼 있다.
- **PSI(Private Set Intersection): 이 문서에는 명시되지 않았다.** 대신 "Cryptographic Computing for Clean Rooms"라는 이름으로 암호화 상태 질의를 제공한다. 챕터에서 AWS Clean Rooms가 PSI를 쓴다고 쓰지 마라 — `확인 불가 (미조회)`.

### E-5-2. Google Ads Data Hub — 유일하게 구체 임계값이 공개된 소스

- 출처: <https://developers.google.com/ads-data-hub/guides/intro>, <https://developers.google.com/ads-data-hub/guides/privacy-checks> | 신뢰성 **최상** | 검색 시점 2026-07-25
- 정의 (원문 인용):
  > "Ads Data Hub enables customized analysis that aligns with your specific business objectives, while protecting user privacy and upholding Google's high standards of data security."
  > "Ads Data Hub ensures end-user privacy by enforcing privacy checks and aggregating Google data before it leaves the Google-owned Google Cloud project."
- 결과 저장: "Results from the queries you run using Ads Data Hub are written to BigQuery datasets in a Google Cloud project that you own."
- **프라이버시 메커니즘 (원문 인용):** "static checks, data access budgets, aggregation checks, difference checks, and noise injection to enforce privacy"
- **구체 임계값 (원문 인용) — 이 숫자들이 챕터의 핵심 팩트다:**
  > "Noise injection requires approximately 20 unique users per result row. Difference checks require approximately 50 unique users per result row. Queries of only click and conversion data require approximately 10 unique users per result row."
- 부가 (원문 인용):
  > "Rows omitted from results due to privacy restrictions" → filtered rows
  > "events with zeroed or null user IDs don't count toward the aggregation threshold"
  > "don't attempt to disaggregate data to disambiguate sets of users that don't meet our aggregation requirements"
- data access budget 소진 경고 메시지 타입: `DATA_ACCESS_BUDGET_IS_NEARLY_EXHAUSTED`
- **개발자 서사:** "SQL은 쓸 수 있는데 `SELECT`가 20명 미만이면 행이 그냥 사라진다." 쿼리 결과가 조용히 비어 있는 걸 디버깅하는 게 클린룸 엔지니어링의 일상이다. 그리고 `events with zeroed or null user IDs don't count` — E-1-4의 all-zero IDFA가 여기서 다시 등장한다.

### E-5-3. Amazon Marketing Cloud

- 출처: <https://advertising.amazon.com/solutions/products/amazon-marketing-cloud> | 신뢰성 **최상** (Amazon 공식 제품 페이지) | 발행일 표기 없음 | 검색 시점 2026-07-25
- 인용:
  > "Amazon Marketing Cloud (AMC) is a secure, privacy-safe, and cloud-based clean room solution in which advertisers can easily perform analytics and build audiences across pseudonymized signals"
  > "AMC only accepts pseudonymized information"
  > "You can only access aggregated, anonymous outputs from AMC."
  > "with built-in aggregation thresholds ensuring user privacy"
- 요지: "Built on AWS Clean Rooms"라고 명시된다.
- ⚠️ **AMC의 구체적 집계 임계값 수치는 이 페이지에 없다. 확인 불가 (미조회).** Ads Data Hub의 20/50/10 숫자를 AMC에 전용하지 마라.

### E-5-4. Snowflake Data Clean Rooms

- 출처: <https://docs.snowflake.com/en/user-guide/cleanrooms/introduction> | 신뢰성 **최상** | 검색 시점 2026-07-25
- 요지: collaboration이 resources(data offerings, templates, code specs)를 담고, "All resources, and the collaboration itself, are defined by YAML specifications."
- **데이터를 복사하지 않는 방식 (원문 인용):**
  > "A live view of the source data, not a snapshot, and its specification controls which columns are exposed and what policies apply."
- 명시된 프라이버시 통제: **differential privacy**만 이 개요 페이지에서 확인됨.
- ⚠️ 집계 임계값, join policy, projection policy는 이 개요 페이지에 **명시되지 않았다 — 확인 불가 (미조회)**.

### E-5-5. 기술 기반 정리 (교차 확인 결과)

| 기법 | 공식 문서에서 명시적으로 확인된 곳 |
|---|---|
| **차등 프라이버시 (Differential Privacy)** | AWS Clean Rooms ✅ (원문 인용 확보), Snowflake ✅ |
| **집계 임계값 (aggregation threshold)** | Ads Data Hub ✅ (20/50/10 명시), AMC ✅ (수치 없이 존재만 명시) |
| **노이즈 주입 (noise injection)** | Ads Data Hub ✅ |
| **difference check** | Ads Data Hub ✅ |
| **암호화 상태 연산** | AWS Clean Rooms ✅ ("Cryptographic Computing for Clean Rooms") |
| **PSI (Private Set Intersection)** | ❌ **어느 벤더 공식 문서에서도 그 이름으로 확인하지 못했다 — 확인 불가 (미조회)** |
| **k-anonymity** | ❌ **어느 벤더 공식 문서에서도 그 용어를 확인하지 못했다.** "집계 임계값"과 k-익명성을 등치시켜 쓰려면 저자 해석임을 명시하라 |

⚠️ **fact-checker 주의:** 클린룸을 설명할 때 "PSI와 k-익명성을 쓴다"는 문장은 이번 리서치에서 **1차 출처로 뒷받침되지 않는다.** 학술 개념으로 소개하는 건 가능하나, 특정 벤더 제품이 그걸 쓴다고 쓰지 마라.

---

## E-6. 규제 (한국 / EU / 미국)

### E-6-1. 한국 개인정보 보호법 [조문 확인 여부: **부분 확인**]

**법령 메타 (law.go.kr 원문 확인 ✅)**
- 출처: <https://www.law.go.kr/LSW/lsInfoP.do?lsId=011357&ancYnChk=0> | 신뢰성 **최상** (법제처 국가법령정보센터) | 검색 시점 2026-07-25
- **시행일: 2025. 10. 2.**
- **법률 제20897호, 2025. 4. 1., 일부개정**

**조문 원문 확인 ✅ (law.go.kr에서 실제로 본문을 읽은 조문)**

| 조 | 제목 | 확인된 내용 |
|---|---|---|
| **제15조** | 개인정보의 수집ㆍ이용 | "개인정보처리자는 다음 각 호의 어느 하나에 해당하는 경우에는 개인정보를 수집할 수 있으며 그 수집 목적의 범위에서 이용할 수 있다." — 각 호 요지: 정보주체 동의 / 법률상 특별 규정·법령상 의무 / 공공기관 소관 업무 / 계약 이행·계약 체결 전 요청 조치 / 급박한 생명·신체·재산 이익 / 개인정보처리자의 정당한 이익 / 공중위생 등 공공의 안전 |
| **제16조** | 개인정보의 수집 제한 | "개인정보처리자는 그 목적에 필요한 최소한의 개인정보를 수집하여야 한다." + 최소 수집이라는 입증책임은 개인정보처리자가 부담 |
| **제24조** | 고유식별정보의 처리 제한 | "개인정보처리자는 다음 각 호의 경우를 제외하고는 고유식별정보를 처리할 수 없다." — 정보주체의 **별도 동의** 또는 법령의 명시적 요구 |
| **제30조** | 개인정보 처리방침의 수립 및 공개 | 제1항 각 호(아래 별도 인용), 제2항 공개 의무, 제3항 "개인정보 처리방침의 내용과 개인정보처리자와 정보주체 간에 체결한 계약의 내용이 다른 경우에는 정보주체에게 유리한 것을 적용한다.", 제4항 보호위원회 작성지침 |
| **제37조의2** | 자동화된 결정에 대한 정보주체의 권리 등 | 아래 별도 인용 |
| **제75조** | 과태료 | 아래 별도 인용 |

**제30조 제1항 각 호 (law.go.kr 원문 인용) — 개인정보 처리방침에 반드시 들어가는 것:**
> 1. 개인정보의 처리 목적
> 2. 개인정보의 처리 및 보유 기간
> 3. 개인정보의 제3자 제공에 관한 사항(해당되는 경우에만 정한다)
> 3의2. 개인정보의 파기절차 및 파기방법
> 3의3. 민감정보의 공개 가능성 및 비공개를 선택하는 방법(해당되는 경우에만 정한다)
> 4. 개인정보처리의 위탁에 관한 사항(해당되는 경우에만 정한다)
> 4의2. 가명정보의 처리 등에 관한 사항(해당되는 경우에만 정한다)
> 5. 정보주체와 법정대리인의 권리·의무 및 그 행사방법에 관한 사항
> 6. 개인정보 보호책임자의 성명 또는 연락처
> 7. 인터넷 접속정보파일 등 자동수집 장치에 관한 사항(해당하는 경우에만 정한다)
> 8. 그 밖에 대통령령으로 정한 사항

- **개발자 함의:** 7호 "인터넷 접속정보파일 등 자동수집 장치" — **쿠키·픽셀·SDK가 법령 문언에 직접 등장하는 지점**이다. 태그 하나 붙일 때마다 처리방침을 고쳐야 하는 법적 근거가 여기다.

**제37조의2(자동화된 결정에 대한 정보주체의 권리 등) — law.go.kr 원문 확인 ✅**
- 출처: <https://law.go.kr/LSW/lsLinkCommonInfo.do?ancYnChk=&chrClsCd=010202&lsJoLnkSeq=1029334889> | 신뢰성 **최상**
- 제1항 요지: 정보주체는 "완전히 자동화된 시스템으로 개인정보를 처리하여 이루어지는 결정"이 자신의 권리에 중대한 영향을 미치는 경우 **그 결정을 거부**할 수 있다.
- 제2항 (원문 인용): "정보주체는 개인정보처리자가 자동화된 결정을 한 경우에는 그 결정에 대하여 설명 등을 요구할 수 있다."
- 제3항 요지: 개인정보처리자는 정당한 사유가 없는 한 자동화된 결정을 적용하지 않거나 "인적 개입에 의한 재처리ㆍ설명 등 필요한 조치"를 해야 한다.
- 제4항 (원문 인용): "개인정보처리자는 자동화된 결정의 기준과 절차, 개인정보가 처리되는 방식 등을 정보주체가 쉽게 확인할 수 있도록 공개하여야 한다."
- **시행일: ⚠️ 검색 결과는 2024-03-15 시행이라고 나오나, law.go.kr 원문의 부칙으로 확인하지 못했다 — `조문 원문 미확인 (시행일)`.** 챕터에 시행일을 쓰려면 별도 확인 필요.
- **개발자 함의 — 이게 martech에 걸리는 지점:** 추천 알고리즘, 자동 등급 산정, 알고리즘 기반 가격 차등, 자동 심사 거절. 제4항의 "기준과 절차, 처리 방식 공개" 의무는 곧 **모델 카드/설명 문서를 제품 안에 넣으라는 요구**다.

**개인정보 보호법 시행령 제17조(동의를 받는 방법) — law.go.kr 원문 확인 ✅**
- 출처: <https://www.law.go.kr/LSW/lsLawLinkInfo.do?lsJoLnkSeq=1000572094&chrClsCd=010202> | 신뢰성 **최상**
- ⚠️ **주의: 이건 법률 제17조가 아니라 시행령 제17조다. 혼동하지 마라.**
- 제1항 각 호 (원문 인용) — 동의가 유효하려면 **네 조건을 모두** 충족해야 한다:
  > 1. 정보주체가 자유로운 의사에 따라 동의 여부를 결정할 수 있을 것
  > 2. 동의를 받으려는 내용이 구체적이고 명확할 것
  > 3. 그 내용을 쉽게 읽고 이해할 수 있는 문구를 사용할 것
  > 4. 동의 여부를 명확하게 표시할 수 있는 방법을 정보주체에게 제공할 것
- **개발자 함의:** 이 네 조건이 **다크 패턴 금지의 법적 근거**다. "동의" 버튼만 크게 하고 "거부"를 흐리게 하면 1호·4호 위반이다. CMP UI 구현은 디자인 문제가 아니라 컴플라이언스 문제다.

**제75조(과태료) — law.go.kr 원문 확인 ✅**
- 출처: <https://law.go.kr/LSW/lsLinkCommonInfo.do?ancYnChk=&chrClsCd=010202&lsJoLnkSeq=1020398445> | 신뢰성 **최상**
- 과태료 구간 (원문 확인): **제1항 5천만원 이하** (고정형/이동형 영상정보처리기기 위반) / **제2항 3천만원 이하** (27개 호) / **제3항 2천만원 이하** (국내대리인 지정 관련 4개 호) / **제4항 1천만원 이하** (자료 제출·동의·정책 공개 관련 12개 호)
- 제5항 (원문 인용): "제1항부터 제4항까지에 따른 과태료는 대통령령으로 정하는 바에 따라 보호위원회가 부과ㆍ징수한다"
- **제2항 각 호 중 martech 직결 항목 (원문 인용) — 이 한 줄이 동의 UX 설계를 규정한다:**
  > "제16조제3항ㆍ제22조제5항을 위반하여 재화 또는 서비스의 제공을 거부한 자"
  - 요지: **선택적 동의를 거부했다는 이유로 서비스 제공을 거부하면 과태료 대상**이다. 즉 "마케팅 수신 동의 안 하면 가입 불가"는 위법이다. 이건 CMP·회원가입 폼 구현에 직접 걸린다.
  - ⚠️ 제16조 제3항과 제22조 제5항의 **조문 원문 자체는 미확인**. 제75조 제2항에서 그 존재와 취지만 확인했다.

**개인정보 보호법 시행령 제31조(개인정보 처리방침의 내용 및 공개방법 등) — law.go.kr 원문 확인 ✅**
- 출처: <https://www.law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=900079801&chrClsCd=010202> | 신뢰성 **최상**
- 제1항 각 호 (원문 인용) — 법 제30조 제1항 8호의 "대통령령으로 정한 사항":
  > 1. 처리하는 개인정보의 항목
  > 2. 법 제28조의8제1항 각 호에 따라 개인정보를 국외로 이전하는 경우 국외 이전의 근거와 같은 조 제2항 각 호의 사항
  > 3. 제30조에 따른 개인정보의 안전성 확보 조치에 관한 사항
  > 4. 국외에서 국내 정보주체의 개인정보를 직접 수집하여 처리하는 경우 개인정보를 처리하는 국가명
- **여기서 얻는 두 가지:**
  1. **제28조의8이 국외 이전 조문임을 법령 원문(시행령 인용)으로 간접 확인했다.** 다만 제28조의8 본문 자체는 여전히 미확인.
  2. **4호는 역외 적용이다** — 해외 서비스가 한국 정보주체의 개인정보를 직접 수집하면 처리 국가명을 처리방침에 밝혀야 한다. Martech SaaS를 해외에서 쓰는 한국 기업, 또는 한국 사용자를 받는 해외 서비스 양쪽에 걸린다.
- 제2항 (원문 인용): "개인정보처리자는 법 제30조제2항에 따라 수립하거나 변경한 개인정보 처리방침을 개인정보처리자의 인터넷 홈페이지에 지속적으로 게재하여야 한다."
- 제3항 요지: 홈페이지 게재가 불가능하면 사업장 게시 / 관보·신문·인터넷신문 게재 / 연 2회 이상 발행 간행물 게재 / 계약서 등에 실어 발급 — 넷 중 하나 이상.

**조문 원문 미확인 항목 (⚠️ 챕터에 조문 번호를 쓰기 전 반드시 재확인)**

아래는 law.go.kr 본문을 열지 못해 **조문 원문 미확인**이다. 검색 결과·2차 자료에서 나온 내용이며, 조문 번호가 맞는지 별도 검증이 필요하다.

| 추정 조 | 주제 | 확인 수준 | 비고 |
|---|---|---|---|
| 제17조 | 개인정보의 제공 (제3자 제공) | 조문 원문 미확인 | 검색 요지: 제3자 제공 시 고지 후 동의, 고지 사항 변경 시 재동의 |
| 제22조 | 동의를 받는 방법 | 조문 원문 미확인 | 검색 요지: 동의 사항을 구분해 명확히 인지하도록 알리고 각각 동의를 받아야 함 |
| 제28조의2~제28조의7 | 가명정보 처리 특례 (제3절) | 조문 원문 미확인 | 검색 요지: 제28조의2 통계작성·과학적 연구·공익적 기록보존 목적 시 **동의 없이** 가명정보 처리 가능 / 제28조의3 서로 다른 처리자 간 가명정보 결합은 보호위원회 지정 **전문기관**이 수행 / 제28조의4 추가정보 분리 보관 등 안전조치 / 제28조의5 특정 개인 식별 목적 처리 금지. 2020-02-04 개정 도입 |
| 제28조의8, 제28조의9 | 개인정보의 국외 이전 / 국외 이전 중지 명령 | 조문 원문 미확인 (조문 번호는 **시행령 제31조 제1항 2호 인용으로 간접 확인 ✅**) | 검색 요지: 원칙적으로 국외 이전 금지, 예외로 ① 정보주체의 **별도 동의** ② 법률·조약·국제협정의 특별 규정 ③ 계약 체결·이행에 필요한 처리위탁·보관으로서 일정 요건 충족. 개정으로 보호위원회가 **본법과 실질적으로 동등한 수준**의 보호를 한다고 인정한 국가·국제기구로의 이전이 추가됨. 위반 시 국외 이전 중지 명령 |
| 제35조 / 제36조 / 제37조 | 열람 / 정정·삭제 / 처리정지 | 조문 원문 미확인 | 조문 번호 자체를 확인하지 못했다 |
| 제35조의2 | 개인정보 전송요구권 (마이데이터) | 조문 원문 미확인 | 검색 요지: 2025-03-13 시행, 에너지정보는 2026-06-01까지 유예. 시행령이 전송자를 보건의료·통신·에너지 정보전송자로 구분 |
| 제64조의2 | 과징금의 부과 | 조문 원문 미확인 | 검색 요지: **전체 매출액의 3% 이하**, 매출액 산정이 곤란하면 **20억원 이하**. 위반행위와 무관한 매출은 제외. ⚠️ "중대 위반 시 10%" 언급도 별개 검색에서 나왔으나 상충 — 아래 상충 섹션 참조. **과태료(제75조)와는 별개의 제재다** |

**PIPC 공식 안내서 (2026년 최신 목록 — pipc.go.kr 확인 ✅)**
- 출처: <https://www.pipc.go.kr/np/cop/bbs/selectBoardList.do?bbsId=BS217&mCode=D010030000> | 신뢰성 **최상** (개인정보보호위원회 공식) | 검색 시점 2026-07-25

| 안내서 | 발행 |
|---|---|
| **개인정보 전송요구권 제도 안내서 (전 분야 마이데이터)** | **2026-06-25** ← 가장 최신, martech 직결 |
| 개인정보 처리방침 작성지침 | 2026-04 |
| **가명정보 처리 가이드라인** | **2026-03** ← martech 직결 |
| 개인정보 처리방침 표준(안) | 2026-02 |
| 보건의료데이터 활용 가이드라인 | 2025-12 |
| 개인정보 질의응답 모음집 | 2025-12 |
| 개인정보의 안전성 확보조치 기준 안내서 | 2025-11 |
| 개인정보 영향평가 수행안내서 | 2025-10 |
| 생성형 인공지능(AI) 개발·활용을 위한 개인정보 처리 안내서 | 2025-08 |
| 개인정보 안내서 전체 목록 | 2025-08-19 |

- ⚠️ **"온라인 맞춤형 광고" 또는 "행태정보" 라는 제목의 독립 안내서는 이 목록에서 확인되지 않았다.** 과거에 그런 가이드라인이 있었다고 기억하더라도, 2026-07-25 기준 PIPC 안내서 목록에서는 확인 불가다. 챕터에서 언급하려면 별도 확인 필요.
- ⚠️ 위 안내서들의 **본문은 미조회**. 제목과 발행 시점만 확인했다.

### E-6-2. 정보통신망법 — 영리목적 광고성 정보 전송 [조문 확인 여부: **원문 확인 ✅**]

**법령 메타 (law.go.kr 원문 확인 ✅)**
- 출처: <https://www.law.go.kr/LSW/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000688185&lsId=000030&print=print> | 신뢰성 **최상** (법제처) | 검색 시점 2026-07-25
- **시행일: 2026. 7. 7.** ← 검색 시점 기준 **18일 전 시행된 따끈한 개정법**
- **법률 제21305호, 2026. 1. 6., 일부개정**

**제50조(영리목적의 광고성 정보 전송 제한) — law.go.kr 원문 인용 ✅**

> **제1항** "누구든지 전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려면 그 수신자의 명시적인 사전 동의를 받아야 한다."

> **제2항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 제1항에도 불구하고 수신자가 수신거부의사를 표시하거나 사전 동의를 철회한 경우에는 영리목적의 광고성 정보를 전송하여서는 아니 된다."

> **제3항 (야간 시간대 제한 — 단서 포함 전문, law.go.kr 원문 확인 ✅)** "오후 9시부터 그 다음 날 오전 8시까지의 시간에 전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 제1항에도 불구하고 그 수신자로부터 별도의 사전 동의를 받아야 한다. **다만, 대통령령으로 정하는 매체의 경우에는 그러하지 아니하다.**"

> **제4항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하는 자는 대통령령으로 정하는 바에 따라 다음 각 호의 사항 등을 광고성 정보에 구체적으로 밝혀야 한다. 1. 전송자의 명칭 및 연락처 2. 수신의 거부 또는 수신동의의 철회 의사표시를 쉽게 할 수 있는 조치"

> **제5항 (요지)** 수신거부 회피·방해 조치, 자동 번호생성, 기망을 통한 수신동의 취득 등 금지 행위 열거

> **제6항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하는 자는 수신자가 수신거부나 수신동의의 철회를 할 때 발생하는 전화요금 등의 금전적 비용을 수신자가 부담하지 아니하도록 대통령령으로 정하는 바에 따라 필요한 조치를 하여야 한다."

> **제7항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 수신자가 제1항 및 제3항에 따른 수신동의, 제2항에 따른 수신거부 또는 수신동의 철회에 관한 의사를 표시할 때에는 해당 수신자에게 대통령령으로 정하는 바에 따라 처리 결과를 알려야 한다."

> **제8항** "제1항 또는 제3항에 따라 수신동의를 받은 자는 대통령령으로 정하는 바에 따라 정기적으로 광고성 정보 수신자의 수신동의 여부를 확인하여야 한다."

**야간 시간대: 오후 9시 ~ 다음 날 오전 8시 — law.go.kr 원문으로 확인했다. ✅** (**11시간 창**)

⚠️ **단서를 빼먹지 마라 — 이게 개발자에게 결정적이다.**
제3항에는 "다만, 대통령령으로 정하는 매체의 경우에는 그러하지 아니하다"는 단서가 **있다**(원문 확인 ✅). 즉 **모든 채널에 11시간 창이 똑같이 적용되는 게 아니다.**
- **어느 매체가 면제되는지는 시행령 원문으로 확인하지 못했다 — `시행령 원문 미확인`.** (`lspttninfSeq=81509` 시도했으나 시행령 제62조의3만 반환)
- 2차 자료(신뢰성 **중**)는 면제 매체가 **전자우편**이라고 한다. 즉 문자·전화·팩스에는 야간 별도 동의가 필요하고 이메일에는 필요 없다는 취지.
- **챕터에서 "밤 9시 이후엔 아무것도 보내면 안 된다"고 쓰지 마라.** 푸시·문자·이메일을 한 규칙으로 묶지 말고, "채널마다 다르며 면제 매체는 시행령이 정한다"까지만 쓴 뒤 `(사실 확인 필요)`를 붙여라. 앱 푸시가 어디에 속하는지는 **확인 불가**.

**2026-07-07 시행 개정의 martech 관련 변경 (⚠️ 신뢰성 중 — 법무법인 뉴스레터·업계 매체 기준, law.go.kr 원문 미확인)**
- 출처: <https://www.bkl.co.kr/law/insight/newsletter/6642>, <https://www.lexology.com/library/detail.aspx?g=def8b7ab-62c2-4807-93aa-fad326ef4612> | 검색 시점 2026-07-25
- 요지 ①: **과징금 도입** — 제50조 등 광고성 정보 전송 규정 위반 시 시행령으로 정하는 **매출액의 6% 이하** 범위에서 과징금 부과 가능
- 요지 ②: **전송 위탁 제한** — 광고성 정보 전송을 위탁할 때는 전기통신사업법 제22조의11 제1항에 따라 방송미디어통신위원회의 **전송자격인증**을 받은 자에게만 위탁 가능
- ⚠️ **6% 수치와 위탁 조문 번호는 law.go.kr 원문으로 확인하지 못했다.** 챕터에 쓸 경우 `(사실 확인 필요)` 마커를 붙이고 fact-checker가 재확인하게 하라. **이 개정은 시행 18일차라 2차 자료 자체가 아직 얇다.**

**챕터에 쓸 개발자 서사:**
> 마케팅팀이 "오후 10시에 푸시 보내면 열람률이 두 배"라고 한다. 개발자는 그때 스케줄러에 시간을 넣는 사람이다. 정보통신망법 제50조 제3항은 오후 9시부터 다음 날 오전 8시까지 광고성 정보를 보내려면 **별도의 사전 동의**를 받으라고 한다. 일반 수신동의로는 안 되고, 야간 전송에 대한 동의를 따로 받아야 한다. 즉 동의 테이블에 컬럼이 하나가 아니라 둘이다.
> 그런데 같은 조항에 단서가 붙어 있다 — 대통령령이 정하는 매체는 예외다. 그래서 "밤 9시 이후 금지"는 채널마다 다르다. 스케줄러 하나에 시간 조건 하나를 박는 순간 틀린다. 채널별 정책 테이블이 필요하다. (어떤 매체가 면제인지는 시행령 소관 — 구현 전에 반드시 확인할 것)
> 그리고 제8항 — 정기적으로 수신동의 여부를 재확인해야 한다. 동의는 한 번 받고 끝나는 boolean이 아니라 **만료되는 상태**다.

### E-6-3. GDPR [조문 확인: **EUR-Lex 원문 기준 ✅, 다만 축약 인용**]

- 출처: <https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng> | 신뢰성 **최상** (EU 공식 관보) | 검색 시점 2026-07-25
- ⚠️ 수집 도구의 인용 길이 제한으로 조문 전문을 그대로 확보하지 못했다. 아래는 규정 자체의 문구를 조각으로 확인한 것이다. 챕터에서 긴 인용이 필요하면 EUR-Lex를 직접 다시 열어라.

**Article 6(1) — 처리의 적법 근거 6가지 (규정 문언 기준)**

| 근거 | 문언 |
|---|---|
| (a) 동의 | "the data subject has given consent to the processing of his or her personal data" |
| (b) 계약 | "processing is necessary for the performance of a contract to which the data subject is party" |
| (c) 법적 의무 | "processing is necessary for compliance with a legal obligation to which the controller is subject" |
| (d) 중대한 이익 | "processing is necessary in order to protect the vital interests of the data subject or of another natural person" |
| (e) 공익 임무 | "processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority" |
| (f) **정당한 이익** | "processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party" |

- **martech의 핵심 쟁점: (a) 동의 vs (f) 정당한 이익.** 광고 타겟팅을 정당한 이익으로 처리할 수 있느냐가 오랜 논쟁이고, IAB TCF v2.2가 Purpose 3·4·5·6에서 LI를 아예 뺀 것(E-3-1)이 그 논쟁의 실무적 결론이다. 이 두 사실을 챕터에서 연결하면 강한 대목이 된다.

**Article 22 — 자동화된 개별 의사결정 (프로파일링 포함)**
- 제1항 요지: 개인은 "a decision based solely on automated processing...which produces legal effects concerning him or her or similarly significantly affects him or her"의 대상이 되지 않을 권리를 갖는다.
- 제2항 예외 3가지 (문언 조각):
  1. "necessary for entering into, or performance of, a contract between the data subject and a controller"
  2. "authorised by Union or Member State law to which the controller is subject"
  3. "the data subject has given his or her explicit consent"
- **한국 개인정보 보호법 제37조의2와 대응 관계**다. 챕터에서 나란히 놓으면 "한국법이 GDPR을 어떻게 참조했나"가 보인다.

**정보주체 권리 조문 번호 (EUR-Lex 확인 ✅)**

| 권리 | 조 |
|---|---|
| 열람 (Right of access) | Article 15 |
| 삭제 (Right to erasure) | Article 17 |
| 처리 제한 (Right to restriction) | Article 18 |
| 데이터 이동권 (Data portability) | Article 20 |
| 반대권 (Right to object) | Article 21 |
| 국외 이전 | **Chapter V (Articles 44–50)** |

### E-6-4. CCPA / CPRA [조문 확인: **부분 — 캘리포니아 법무장관실 페이지 기준**]

- 출처: <https://oag.ca.gov/privacy/ccpa> | 신뢰성 **최상** (California Attorney General 공식) | 발행일 표기 없음 | 검색 시점 2026-07-25
- **"sharing" 정의 (원문 인용):**
  > "sharing for cross-context behavioral advertising, which is the targeting of advertising to a consumer based on the consumer's personal information obtained from the consumer's online activity across numerous websites"
- **opt-out 권리 (원문 인용):**
  > "may request that businesses stop selling or sharing your personal information"
  > businesses "cannot sell or share your personal information after they receive your opt-out request unless you later provide authorization allowing them to do so again"
- **GPC 존중 의무 (원문 인용) — 이게 개발자에게 중요한 문장이다:**
  > "Under law, it must be honored by covered businesses as a valid consumer request to stop the sale or sharing of personal information."
- 요지: 온라인 요청을 받는 사업자는 최소 두 가지 제출 방법을 제공해야 하며, 그중 하나로 "via a user-enabled global privacy control, like the GPC"가 인정된다.
- ⚠️ **"sale"의 법문 정의와 Civil Code 조문 번호(1798.120, 1798.135 등)는 이 페이지에서 확인하지 못했다 — `조문 원문 미확인`.** cppa.ca.gov 규정 페이지는 규칙제정 문서 링크만 있고 조문 전문이 없었다.
- **EU vs 미국 모델 대비 (챕터 핵심 프레임):**
  - GDPR/한국: **opt-in** — 동의를 받아야 처리 가능
  - CCPA/CPRA: **opt-out** — 처리하다가 소비자가 거부하면 중단
  - 그래서 같은 코드베이스로 두 지역을 서비스하려면 **동의 모델 자체가 지역별로 분기**된다. 이게 E-7의 데이터 레지던시 논의로 이어진다.

### E-6-5. EU AI Act [적용 일정: **EU 공식 서비스데스크 확인 ✅**]

- 출처: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act> | 신뢰성 **최상** (European Commission 공식) | 페이지 최종 갱신일 표기 없음 | 검색 시점 2026-07-25

⚠️ **아래 표 전체에 대한 경고:** 이 페이지에는 최종 갱신일 표기가 없다. 2026년 7월 발효된 AI Omnibus가 이 표에 반영됐는지 **확인하지 못했다.** 챕터에 날짜를 옮길 때는 반드시 "2026-07-25 조회 기준"을 병기하라.

| 날짜 | 적용 내용 |
|---|---|
| 2024-08-01 | 발효 (entry into force) |
| 2025-02-02 | "General provisions (definitions & AI literacy) and prohibitions apply" — **금지 관행(Article 5)과 AI 리터러시 의무 적용 시작** |
| 2025-08-02 | 범용 AI(GPAI) 제공자 의무 개시. 회원국의 관할당국 지정·제재 체계 도입, EU 차원 거버넌스(AI Board, Scientific Panel, Advisory Forum) 설치 |
| **2026-08-02** | 투명성 규칙 적용 개시, 혁신 지원 조치 발효. GPAI 모델·금지 관행·투명성 요건·AI 리터러시에 대한 **집행 개시** |
| 2026-12-02 | 비동의 성적 딥페이크·아동 착취물 관련 신규 금지 발효. 2026-08-02 이전 시장 출시된 일부 합성 콘텐츠 제공자에 대한 경과 준수 기한 |
| 2027-08-02 | 회원국은 최소 1개 AI 규제 샌드박스를 운영해야 함 |
| **2027-12-02** | "Rules for high-risk AI systems in Annex III apply" |
| **2028-08-02** | "Rules for high-risk AI embedded in regulated products covered by Annex I apply" |

- **AI Omnibus로 인한 연기 ⚠️ (신뢰성 중 — EU 공식 페이지에서 직접 확인 못 함, 검색 결과 기준):**
  - 요지: 'AI omnibus' 간소화 제안이 2025-11-19 채택, 2026-05-07 정치적 합의, 최종 규정이 **2026년 7월 발효**. 그 결과 Annex I 규제 제품 내장 고위험 AI 규정의 전환기간이 **2028-08-02까지 연장**됐다.
  - 챕터에 쓸 때는 "2026년 중 AI Omnibus로 일정이 완화됐다"는 수준으로 쓰고, 구체 날짜에는 `(사실 확인 필요)` 마커를 붙여라. **이 항목은 검색 시점 기준으로도 진행 중이다.**
- **마케팅 AI에 걸리는 지점 (⚠️ Article 5 원문 미조회 — artificialintelligenceact.eu 요약 기준, 신뢰성 중):**
  - Article 5는 조작적(manipulative)·착취적(exploitative) 관행과 사회적 점수화(social scoring)를 목적으로 하는 AI 시스템의 출시·서비스·사용을 금지한다. 감정 인식과 생체 분류도 포함된다.
  - **마케팅과의 접점:** 취약 집단을 겨냥한 조작적 개인화, 감정 인식 기반 광고 타겟팅. 다만 **일반적인 광고 개인화·리타겟팅이 Article 5에 걸린다는 근거는 이번 리서치에서 확인하지 못했다 — `확인 불가`.**
  - **Article 50(투명성 규칙)이 마케팅에 더 직접적일 가능성이 있으나, 원문 미조회 — `확인 불가 (미조회)`.**
- ⚠️ **챕터에서 "AI Act가 마케팅 타겟팅을 규제한다"고 단정하지 마라.** 확인된 건 일정표와 Article 5의 금지 범주 개요뿐이다.

---

## E-7. 규제가 코드·데이터 모델에 남기는 흔적

⚠️ **이 섹션은 위 1차 출처들에서 도출한 저자 정리다. 개별 문장에 1차 출처가 붙지 않는다.** 챕터에서 수치나 "반드시 이래야 한다"는 단정 없이 설계 서술로 써라. 각 항목이 어느 법조문·문서에서 파생됐는지만 표기했다.

| 코드·데이터 모델에 남는 것 | 파생 근거 (이 문서 안에서 확인된 것) |
|---|---|
| **동의 필드가 boolean 하나가 아니다** | Consent Mode 파라미터 7종(E-3-2) + 정보통신망법 제50조 제1항/제3항이 요구하는 **두 개의 별도 동의**(E-6-2). 최소한 `{목적, 지역, 채널, 시간대}` 축으로 쪼개진다 |
| **동의가 만료된다** | 정보통신망법 제50조 제8항 "정기적으로 광고성 정보 수신자의 수신동의 여부를 확인하여야 한다"(E-6-2). → 동의 레코드에 `verified_at`이 필요하고, 만료 재확인 배치가 필요하다 |
| **동의에 이력이 필요하다** | 제50조 제2항 철회 시 전송 금지 + 제7항 처리 결과 통지 의무. → 현재 상태만이 아니라 **append-only 동의 이벤트 로그** |
| **다크 패턴 금지가 UI 코드 제약이 된다** | 개인정보 보호법 시행령 제17조 제1항 4개 조건(E-6-1). TCF v2.2의 "모두 동의 버튼이 있으면 모두 철회 버튼도"(E-3-1) |
| **"동의 안 하면 가입 불가"를 못 짠다** | 개인정보 보호법 제75조 제2항 — "제16조제3항ㆍ제22조제5항을 위반하여 재화 또는 서비스의 제공을 거부한 자"에 과태료(E-6-1). → 선택 동의 체크박스는 **미체크 상태로도 가입 플로우가 끝까지 통과해야** 한다 |
| **처리방침에 데이터가 어느 나라에 있는지 써야 한다** | 개인정보 보호법 시행령 제31조 제1항 2호·4호(E-6-1). → 벤더 리전을 바꾸면 처리방침을 고쳐야 한다. 인프라 결정이 법무 문서에 물려 있다 |
| **처리방침이 코드 배포와 연동된다** | 개인정보 보호법 제30조 제1항 7호 "인터넷 접속정보파일 등 자동수집 장치"(E-6-1). → 태그 하나 추가 = 처리방침 개정 |
| **보존 기간(TTL)이 스키마의 일부다** | 개인정보 보호법 제30조 제1항 2호 "개인정보의 처리 및 보유 기간", 제16조 최소 수집 원칙(E-6-1) |
| **삭제 요청이 파이프라인 전체를 관통한다** | GDPR Article 17 삭제권(E-6-3) + 한국법 삭제권. 지워야 할 곳: OLTP DB, 이벤트 스트림의 리텐션 구간, 웨어하우스 파티션, 컬럼 지향 포맷(Parquet/Iceberg — 행 단위 삭제가 비싸다), 백업 스냅샷, 검색 인덱스, **그리고 이미 벤더에 싱크된 오디언스** |
| **가명화는 삭제가 아니다** | 개인정보 보호법 제28조의4 요지 — 추가정보를 분리 보관해야 가명정보다(⚠️ 조문 원문 미확인). SHA-256 이메일 해시는 여전히 조인 키다(E-4-3) |
| **감사 로그가 제품 기능이다** | AWS Clean Rooms "Analysis logs ... help support audits"(E-5-1) + 개인정보 보호법 제37조의2 제4항 자동화 결정 공개 의무(E-6-1) |
| **지역별 분기가 런타임에 존재한다** | opt-in(EU/한국) vs opt-out(캘리포니아)(E-6-4) + GDPR Chapter V 국외 이전 + 한국법 제28조의8 국외 이전(⚠️ 조문 원문 미확인). → 요청 지역에 따라 **다른 동의 모델, 다른 저장 리전** |
| **GPC는 헤더 한 줄인데 법적 구속력이 있다** | W3C `Sec-GPC: 1`(E-3-3) + 캘리포니아 AG "it must be honored"(E-6-4) |
| **널·플레이스홀더 ID가 프라이버시 사고를 만든다** | ATT 거부 시 all-zero IDFA(E-1-4) + Ads Data Hub "events with zeroed or null user IDs don't count toward the aggregation threshold"(E-5-2) + ID 그래프 over-merge(E-4-2) |
| **48시간 dedup 창이 배치 잡 설계를 제약한다** | Meta CAPI dedup 48시간(E-2-3) |
| **7일 스토리지 캡이 익명 식별을 무너뜨린다** | Safari ITP 7일 script-writable storage 삭제(E-1-2), CNAME 쿠키 7일 캡(E-1-3) |

---

## 상충·불확실 항목 (스스로 결론 내지 않고 병기)

1. **서버사이드 태깅은 프라이버시 강화인가 회피인가**
   - Google 공식: 서버사이드 태깅이 "Unlock more detailed user privacy controls"를 제공한다 (E-2-1)
   - WebKit 공식: CNAME 클로킹은 추적 방지를 우회하는 수법이며, 쿠키 수명을 7일로 캡한다 (E-1-3)
   - → 병기하라. 같은 아키텍처가 두 진영에서 정반대로 불린다.

2. **개인정보 보호법 과징금 상한 — 3%인가 10%인가**
   - 검색 결과 A: 제64조의2, **전체 매출액의 3% 이하** (위반과 무관한 매출 제외), 매출액 산정 곤란 시 **20억원 이하**
   - 검색 결과 B: 반복·중대 위반(고의·중과실) 시 **10%까지** 가능
   - → **둘 다 law.go.kr 조문 원문으로 확인하지 못했다.** A가 여러 2차 자료에서 더 일관되게 나오지만, 확정하지 마라. 챕터에 수치를 쓰지 말거나, 쓴다면 `(사실 확인 필요)`를 붙여라.
   - **부수 주의: 과징금(제64조의2)과 과태료(제75조)는 다른 제재다.** 제75조는 원문으로 확인했다(5천만/3천만/2천만/1천만원 이하 4구간). 둘을 섞어 쓰지 마라. 정보통신망법의 6% 과징금(E-6-2)과도 별개다.

3. **Privacy Sandbox status 페이지 vs Chrome 144 릴리스 노트**
   - status 페이지(2025-10-17): Topics·Attribution Reporting·Related Website Sets 포함 7개가 "Deprecate and Remove"
   - Chrome 144 릴리스 노트(2026-01-13): deprecation 섹션에 Private Aggregation, Shared Storage, Protected Audience 세 개만 명시
   - blink-dev(2025-11-08, 2026-06-12 갱신): Topics는 M144 deprecate, M150 remove
   - → 세 소스가 서로 다른 커버리지를 보인다. **"Chrome 144에서 무엇이 deprecate됐다"를 단정하지 말고 API별로 소스를 달리 인용하라.**

4. **IP Protection의 운명**
   - 2025-04-22 Google 블로그: 2025년 3분기 런칭 예정
   - 2025-10-17 status 페이지: Discontinue (Do Not Launch)
   - → 이건 상충이 아니라 **번복**이다. 궤적으로 서술하면 챕터의 가장 좋은 사례가 된다.

5. **EU AI Act의 최종 일정**
   - EU 공식 서비스데스크 타임라인은 확인했으나, AI Omnibus의 최종 변경 내역이 그 페이지에 반영됐는지 확인하지 못했다. 페이지 자체에 최종 갱신일이 없다.
   - → 챕터에 AI Act 일정을 쓸 때는 "2026년 7월 기준"임을 명시하라.

6. **정보통신망법 제50조 제3항 야간 제한의 적용 범위**
   - 법 원문: 오후 9시~오전 8시 별도 동의 필요 **+ 대통령령이 정하는 매체는 예외** (둘 다 원문 확인 ✅)
   - 2차 자료: 예외 매체 = 전자우편 (신뢰성 중, 시행령 원문 미확인)
   - → **"11시간 창"만 떼어 쓰면 절반만 맞는 서술이 된다.** 반드시 단서와 함께 서술하라.

7. **PIPC의 온라인 맞춤형 광고 가이드라인 존재 여부**
   - 2026-07-25 기준 PIPC 안내서 목록에서 해당 제목의 문서를 확인하지 못했다.
   - → 있었다가 통합·폐지됐을 수 있고, 다른 게시판에 있을 수도 있다. **존재를 단정하지 마라.**

---

## 확인 불가 목록 (챕터에 쓰지 말 것 / 별도 확인 필요)

**E-1**
- Chrome M150의 실제 stable 릴리스 날짜 (chromiumdash JS 렌더링 실패)
- Privacy Sandbox status 페이지의 2026년 갱신본 존재 여부
- Firefox Total Cookie Protection이 기본값이 된 정확한 Firefox 버전 번호 (support.mozilla.org 로드 실패)
- SKAdNetwork의 deprecation 여부, 버전, conversion value 스펙 (Apple 문서 SPA 추출 실패)
- AdAttributionKit ↔ SKAdNetwork 상호운용의 정확한 문언 및 iOS 버전 요건
- CMA 결정문 PDF 본문 (요약만 확보)

**E-2**
- Meta가 CAPI를 만든 이유로 브라우저 제약·광고 차단기를 공식적으로 언급했는지 (공식 페이지에는 없음)
- GTM 서버사이드의 CNAME/서브도메인 설정에 대한 Google 공식 권고 문언

**E-4**
- raw UID2의 파생 절차 (해싱·솔팅), 토큰 정의·회전 주기
- RampID의 현재 상태
- 이메일 SHA-256 해시가 업계 표준 식별자인지에 대한 1차 근거
- LiveRamp/Adobe/Salesforce의 deterministic·probabilistic 정의 **원문** (검색 요약만 확보 — 따옴표 인용 금지)

**E-5**
- Snowflake Data Clean Rooms의 집계 임계값·join policy·projection policy
- Amazon Marketing Cloud의 구체적 집계 임계값 수치
- **어느 벤더도 PSI(Private Set Intersection)나 k-anonymity를 그 이름으로 명시하지 않았다**

**E-6**
- 개인정보 보호법 제16조제3항·제17조·제22조·제22조제5항·제28조의2~제28조의9·제35조·제35조의2·제36조·제37조·제64조의2 **조문 원문** (law.go.kr 본문 프레임 접근 실패). 제28조의8과 제16조제3항·제22조제5항은 **다른 조문의 인용을 통해 존재와 취지만 간접 확인**했다
- 제37조의2의 시행일 (부칙 미확인)
- 정보통신망법 2026-07-07 개정의 과징금 6% 수치 및 전송 위탁 조문 (law.go.kr 원문 미확인)
- **정보통신망법 제50조 제3항 단서의 "대통령령으로 정하는 매체"가 무엇인지** — 단서의 존재는 원문 확인했으나 시행령 원문 미확인. 2차 자료는 **전자우편**이라고 하나 미검증. **앱 푸시가 면제 대상인지는 확인 불가** (martech 구현에 가장 중요한 미결 항목)
- 개인정보 보호법 제16조 제3항·제22조 제5항 원문 (제75조 제2항의 인용으로 취지만 확인)
- CCPA "sale"의 법문 정의 및 Civil Code 조문 번호
- EU AI Act Article 5·Article 50 원문
- AI Omnibus 최종 규정의 공식 텍스트
- PIPC 안내서 각 문서의 **본문** (제목·발행 시점만 확보)

---

## 신선도 원장

| 소스 | URL | 발행일 / 갱신일 | 검색 시점 | 관련 항목 | 신뢰성 |
|---|---|---|---|---|---|
| Google Privacy Sandbox — 3PC 유지 결정 | privacysandbox.google.com/blog/privacy-sandbox-next-steps | 2025-04-22 | 2026-07-25 | E-1-1 | 최상 |
| Google Privacy Sandbox — 기술 은퇴 | privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies | 2025-10-17 | 2026-07-25 | E-1-1 | 최상 |
| Privacy Sandbox feature status | privacysandbox.google.com/overview/status | 2025-10-17 (페이지 최종 갱신) | 2026-07-25 | E-1-1 | 최상 ⚠️ 2026 갱신 미확인 |
| Chrome 144 릴리스 노트 | developer.chrome.com/release-notes/144 | stable 2026-01-13 | 2026-07-25 | E-1-1 | 최상 |
| blink-dev — Intent to Deprecate/Remove Topics | groups.google.com/a/chromium.org/g/blink-dev/c/_R85yctz4Rs | 2025-11-08, 갱신 2026-06-12 | 2026-07-25 | E-1-1 | 최상 |
| topics-api-announce PSA | groups.google.com/a/chromium.org/g/topics-api-announce/c/iQX7PC3S0Ds | 2025-12-05 | 2026-07-25 | E-1-1 | 최상 |
| UK CMA — Privacy Sandbox 사건 | gov.uk/cma-cases/investigation-into-googles-privacy-sandbox-browser-changes | 결정 2025-10-17 | 2026-07-25 | E-1-1 | 최상 ⚠️ PDF 본문 미조회 |
| WebKit — ITP 최초 도입 | webkit.org/blog/7675/ | 2017-06-05 | 2026-07-25 | E-1-2 | 최상 ⚠️ 구버전 정보 |
| WebKit — Full 3rd-Party Cookie Blocking | webkit.org/blog/10218/ | 2020-03-24 | 2026-07-25 | E-1-2 | 최상 |
| WebKit — CNAME Cloaking Defense | webkit.org/blog/11338/ | 2020-11-12 | 2026-07-25 | E-1-3, E-2 | 최상 |
| Mozilla — Total Cookie Protection | blog.mozilla.org/en/products/firefox/firefox-rolls-out-total-cookie-protection... | 2022-06-14 (업데이트 2024-08-28) | 2026-07-25 | E-1-3 | 최상 |
| Apple — User Privacy and Data Use | developer.apple.com/app-store/user-privacy-and-data-use/ | 표기 없음 | 2026-07-25 | E-1-4 | 최상 |
| Apple — AppTrackingTransparency | developer.apple.com/documentation/apptrackingtransparency | 표기 없음 | 2026-07-25 | E-1-4 | 최상 |
| Google — Server-side tagging | developers.google.com/tag-platform/tag-manager/server-side | 표기 없음 | 2026-07-25 | E-2-1 | 최상 |
| Google — Send data to server container | developers.google.com/tag-platform/tag-manager/server-side/send-data | 표기 없음 | 2026-07-25 | E-2-1 | 최상 |
| Meta — Conversions API | developers.facebook.com/docs/marketing-api/conversions-api | 표기 없음 | 2026-07-25 | E-2-2 | 최상 |
| Meta — Deduplicate Pixel & Server Events | developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events | 표기 없음 | 2026-07-25 | E-2-3 | 최상 |
| IAB Europe — TCF v2.3 전환 | iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/ | 2025-06-19 | 2026-07-25 | E-3-1 | 최상 |
| IAB Europe — TCF v2.2 | iabeurope.eu/tcf/, iabeurope.eu/tcf-2-2-launches-all-you-need-to-know/ | 2023 (v2.2 출시 2023-05-16) | 2026-07-25 | E-3-1 | 최상 |
| Google — Consent mode overview | developers.google.com/tag-platform/security/concepts/consent-mode | 표기 없음 | 2026-07-25 | E-3-2 | 최상 |
| W3C — Global Privacy Control | w3.org/TR/gpc/ | **2026-06-11 (Working Draft)** | 2026-07-25 | E-3-3 | 최상 |
| LiveRamp / Segment — identity resolution | liveramp.com/uk/blog/probabilistic-vs-deterministic-matching, segment.com/blog/identity-resolution/ | 표기 없음 | 2026-07-25 | E-4-1 | 중 ⚠️ 본문 미조회 |
| Unified ID 2.0 문서 | unifiedid.com/docs/intro | **최종 갱신 2026-07-23** | 2026-07-25 | E-4-3 | 최상 |
| AWS Clean Rooms — What is | docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html | 표기 없음 | 2026-07-25 | E-5-1 | 최상 |
| Google Ads Data Hub — Intro | developers.google.com/ads-data-hub/guides/intro | 표기 없음 | 2026-07-25 | E-5-2 | 최상 |
| Google Ads Data Hub — Privacy checks | developers.google.com/ads-data-hub/guides/privacy-checks | 표기 없음 | 2026-07-25 | E-5-2 | 최상 |
| Amazon Marketing Cloud | advertising.amazon.com/solutions/products/amazon-marketing-cloud | 표기 없음 | 2026-07-25 | E-5-3 | 최상 |
| Snowflake Data Clean Rooms | docs.snowflake.com/en/user-guide/cleanrooms/introduction | 표기 없음 | 2026-07-25 | E-5-4 | 최상 |
| **법제처 — 개인정보 보호법** | law.go.kr/LSW/lsInfoP.do?lsId=011357 | **시행 2025-10-02, 법률 제20897호 (2025-04-01 일부개정)** | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 조문 (제15·16·24·30조) | law.go.kr/LSW//lsLawLinkInfo.do?...lsJoLnkSeq=900078586..., ...lsJoLnkSeq=1020398697 | 상동 | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 제37조의2 | law.go.kr/LSW/lsLinkCommonInfo.do?...lsJoLnkSeq=1029334889 | 상동 | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 제75조 (과태료) | law.go.kr/LSW/lsLinkCommonInfo.do?...lsJoLnkSeq=1020398445 | 상동 | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 시행령 제17조 | law.go.kr/LSW/lsLawLinkInfo.do?lsJoLnkSeq=1000572094 | — | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 시행령 제31조 (처리방침·국외이전 고지) | law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=900079801 | — | 2026-07-25 | E-6-1, E-7 | 최상 |
| **법제처 — 정보통신망법 제50조** | law.go.kr/LSW/lsLawLinkInfo.do?...lsJoLnkSeq=1000688185...&print=print | **시행 2026-07-07, 법률 제21305호 (2026-01-06 일부개정)** | 2026-07-25 | E-6-2 | 최상 |
| 정보통신망법 2026 개정 해설 (법무법인) | bkl.co.kr/law/insight/newsletter/6642 | 2026 | 2026-07-25 | E-6-2 | 중 |
| **PIPC 안내서 목록** | pipc.go.kr/np/cop/bbs/selectBoardList.do?bbsId=BS217&mCode=D010030000 | 최신 항목 **2026-06-25** | 2026-07-25 | E-6-1 | 최상 |
| EUR-Lex — GDPR | eur-lex.europa.eu/eli/reg/2016/679/oj/eng | 2016-04-27 | 2026-07-25 | E-6-3 | 최상 |
| California AG — CCPA | oag.ca.gov/privacy/ccpa | 표기 없음 | 2026-07-25 | E-6-4 | 최상 |
| EU — AI Act 이행 타임라인 | ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act | 표기 없음 | 2026-07-25 | E-6-5 | 최상 |

---

## 참고문헌

**브라우저·플랫폼 정책 (1차)**
1. Anthony Chavez, "Next steps for Privacy Sandbox and tracking protections in Chrome", Google, 2025-04-22. https://privacysandbox.google.com/blog/privacy-sandbox-next-steps
2. Anthony Chavez, "Update on Plans for Privacy Sandbox Technologies", Google, 2025-10-17. https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies
3. "Privacy Sandbox feature status", Google, 2025-10-17. https://privacysandbox.google.com/overview/status
4. "Chrome 144 release notes", Chrome for Developers, stable 2026-01-13. https://developer.chrome.com/release-notes/144
5. Yao Xiao, "Intent to Deprecate and Remove: Topics API", blink-dev, 2025-11-08 (갱신 2026-06-12). https://groups.google.com/a/chromium.org/g/blink-dev/c/_R85yctz4Rs
6. Sam Dutton, "PSA: Topics API deprecation and removal", topics-api-announce, 2025-12-05. https://groups.google.com/a/chromium.org/g/topics-api-announce/c/iQX7PC3S0Ds
7. Competition and Markets Authority, "Investigation into Google's 'Privacy Sandbox' browser changes" (결정 2025-10-17). https://www.gov.uk/cma-cases/investigation-into-googles-privacy-sandbox-browser-changes
8. John Wilander, "Intelligent Tracking Prevention", WebKit, 2017-06-05. https://webkit.org/blog/7675/intelligent-tracking-prevention/
9. John Wilander, "Full Third-Party Cookie Blocking and More", WebKit, 2020-03-24. https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
10. John Wilander, "CNAME Cloaking and Bounce Tracking Defense", WebKit, 2020-11-12. https://webkit.org/blog/11338/cname-cloaking-and-bounce-tracking-defense/
11. Mozilla, "Firefox rolls out Total Cookie Protection by default to all users worldwide", 2022-06-14 (업데이트 2024-08-28). https://blog.mozilla.org/en/products/firefox/firefox-rolls-out-total-cookie-protection-by-default-to-all-users-worldwide/
12. Apple, "User Privacy and Data Use". https://developer.apple.com/app-store/user-privacy-and-data-use/
13. Apple, "AppTrackingTransparency". https://developer.apple.com/documentation/apptrackingtransparency

**수집 아키텍처 (1차)**
14. Google, "Server-side tagging". https://developers.google.com/tag-platform/tag-manager/server-side
15. Google, "Send data to a server container". https://developers.google.com/tag-platform/tag-manager/server-side/send-data
16. Meta, "Conversions API". https://developers.facebook.com/docs/marketing-api/conversions-api
17. Meta, "Deduplicate Pixel and Server Events". https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events

**동의 (1차)**
18. IAB Europe, "All You Need to Know About the Transition to TCF v2.3", 2025-06-19. https://iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/
19. IAB Europe, "The Transparency & Consent Framework (TCF) v2.2". https://iabeurope.eu/tcf/
20. Google, "Consent mode overview". https://developers.google.com/tag-platform/security/concepts/consent-mode
21. W3C, "Global Privacy Control (GPC)", Working Draft, 2026-06-11. https://www.w3.org/TR/gpc/

**아이덴티티 (1차·2차)**
22. Unified ID 2.0 documentation (최종 갱신 2026-07-23). https://unifiedid.com/docs/intro
23. LiveRamp, "Probabilistic vs Deterministic Matching". https://liveramp.com/uk/blog/probabilistic-vs-deterministic-matching ⚠️ 본문 미조회
24. Twilio Segment, "Identity resolution: what it is and how it works". https://segment.com/blog/identity-resolution/ ⚠️ 본문 미조회

**클린룸 (1차)**
25. AWS, "What is AWS Clean Rooms?". https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html
26. Google, "Ads Data Hub introduction". https://developers.google.com/ads-data-hub/guides/intro
27. Google, "Privacy checks in Ads Data Hub". https://developers.google.com/ads-data-hub/guides/privacy-checks
28. Amazon Ads, "Amazon Marketing Cloud". https://advertising.amazon.com/solutions/products/amazon-marketing-cloud
29. Snowflake, "Snowflake Data Clean Rooms introduction". https://docs.snowflake.com/en/user-guide/cleanrooms/introduction

**규제 (1차)**
30. 법제처 국가법령정보센터, 「개인정보 보호법」 (시행 2025-10-02, 법률 제20897호). https://www.law.go.kr/LSW/lsInfoP.do?lsId=011357&ancYnChk=0
31. 법제처 국가법령정보센터, 「정보통신망 이용촉진 및 정보보호 등에 관한 법률」 제50조 (시행 2026-07-07, 법률 제21305호). https://www.law.go.kr/LSW/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000688185&lsId=000030&print=print
32. 개인정보보호위원회, 안내서 목록. https://www.pipc.go.kr/np/cop/bbs/selectBoardList.do?bbsId=BS217&mCode=D010030000
33. EUR-Lex, Regulation (EU) 2016/679 (GDPR). https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
34. California Attorney General, "California Consumer Privacy Act (CCPA)". https://oag.ca.gov/privacy/ccpa
35. European Commission AI Act Service Desk, "Timeline for the Implementation of the EU AI Act". https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act

**규제 (2차 — 신뢰성 중, 교차 확인 필요)**
36. 법무법인(유) 태평양, "정보통신망법 시행령 일부개정: 주요 내용과 시사점". https://www.bkl.co.kr/law/insight/newsletter/6642

---

## 수집 한계

- **law.go.kr 프레임 구조**: 국가법령정보센터는 프레임/SPA 기반이라 `법령/{법령명}` 경로로는 본문이 추출되지 않았다. `lsLawLinkInfo.do?...&print=print`와 `lsLinkCommonInfo.do?lsJoLnkSeq=` 패턴만 본문을 반환했다. 이 패턴은 조문별 `lsJoLnkSeq` 값을 알아야 해서, 검색으로 발견한 조문만 원문 확인이 가능했다. **후속 리서치자를 위한 팁: 이 두 URL 패턴을 쓰라.**
- **Apple 개발자 문서**: SPA라 일반 URL로는 추출 실패. `developer.apple.com/tutorials/data/documentation/{path}.json` 엔드포인트는 성공했다. 상시 HTML인 `developer.apple.com/app-store/...` 경로도 성공.
- **chromestatus.com, chromiumdash.appspot.com**: JS 렌더링 의존으로 추출 실패.
- **EUR-Lex 장문 인용**: 수집 도구의 인용 길이 제한으로 GDPR 조문 전문 확보 실패. 조각 문언과 조문 번호만 확보.
- **의도적 제외**: 커뮤니티(Reddit/HN/OKKY), 논문, 벤더 마케팅 블로그의 수치 주장. 다른 에이전트 담당이거나 신뢰성이 낮다.
- **날짜 없는 공식 문서**: 다수 벤더 문서(Google/Meta/AWS/Apple)에 발행일 표기가 없다. "표기 없음 / 검색 시점 2026-07-25"로 기록했다. **이 항목들은 6개월 뒤 재확인이 필요하다.**
