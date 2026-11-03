# 커뮤니티 리서치: Insider One·Braze로 하는 기업 CRM 마케팅 (한국 주니어 마케터 대상)

- 검색 시점: 2026-11-03
- genre: tech-book / slug: insider-braze-marketing
- 수집 건수: 22건 (리뷰 플랫폼 묶음 6, 실무자 블로그·매거진 6, 벤더 공식 고객 사례 4, 기업 데이터팀 블로그 1, 커뮤니티 포럼 1, 강의 수강평·소개 2, 업계 기사 2)
- **라벨 규칙:** 아래 모든 주장은 **커뮤니티 의견, 검증 필요**. 벤더 게재 사례(Braze·Insider 고객 사례 페이지)의 수치는 "벤더 게재 수치"로 따로 표시했다. 리뷰 인용 중 일부는 페이지를 직접 열지 못하고 검색 스니펫으로만 확인했다. 해당 항목에는 `[스니펫]` 표시를 붙였다. fact-checker 대조나 책 인용 전에 원문을 다시 확인해야 한다.

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "기본 캠페인은 금방인데, 그다음부터 벽이 있다" (학습 곡선)
두 제품 모두 "쉽다"는 평과 "가파르다"는 평이 같이 나온다. 갈리는 지점은 사용 단계다. 단발 푸시·이메일 발송은 쉽다는 쪽이고, 캔버스/여정·이벤트 데이터·동적 콘텐츠로 넘어가면 어렵다는 쪽이다.
- 출현 예시:
  - Braze / AWS Marketplace 리뷰 (Bret C., 2026-10-26): "Because Braze is so feature-dense, configuring campaigns can feel overly complicated." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=9
  - Braze / AWS Marketplace 리뷰 (Yashaswi J., QA, 2026-10-28): "It is very easy to understand and use for day-to-day promotional and transactional communications." 같은 리뷰어의 단점은 "The UI for the features needs to be simpler" — 같은 페이지
  - Braze / Capterra (CRM 직무 리뷰어) `[스니펫]`: "there is a steep learning curve that makes getting use to it difficult" / 다른 리뷰어: "steeper learning curve and more time required during the initial implementation than other plug-and-play marketing automation platforms like Pardot and Marketo. But it is so worth it." — https://www.capterra.com/p/155423/Appboy/reviews?page=2
  - Braze / Capterra 요약 `[스니펫]`: "for non-technical teams, some of the advanced features (events, integrations, dynamic content, liquid templating) can have a learning curve" / "can feel overwhelming if you have a lean team" — 같은 소스
  - Insider One / G2·Gartner 리뷰 (AWS Marketplace 집계, 여행업, 2026-10-29): "There was a steeper learning curve than we expected, and the implementation process could have been smoother." / 패션업 (2026-10-29): "there is a big learning curve and the platform is complex." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97
  - Insider One / G2 집계 `[스니펫]`: Insider One 리뷰 약 81건이 "steep learning curve"를, 약 37건이 "time-consuming setup"을 단점으로 꼽았다. — https://g2.com/products/insider/reviews?page=4 , https://www.g2.com/survey_responses/insider-review-5133670
- 추정 원인 (커뮤니티가 공유하는 진단): 기능이 많아서라기보다, 고급 기능이 전부 **데이터 모델(이벤트·속성) 이해**를 전제하기 때문이다. 팀이 작으면(lean team) 이 부담이 더 크다.
- 책 활용 아이디어: 1장 오프닝으로 "첫 주에 푸시는 보냈다. 그런데 캔버스를 여는 순간 막혔다" 같은 장면을 쓸 수 있다.

### 패턴 2: "사수가 없다" — 한국 주니어 CRM 마케터의 독학 문제
- 출현 예시:
  - 인프런 Braze 강의 소개 (현직 CRM 마케터 강사): "CRM 마케터의 채용 공고 자격요건/우대사항 등에는 브레이즈 활용 역량이 포함되어 있습니다. 그러나 마땅히 배울 곳도, 알려줄 수 있는 사람도 많지 않은 것이 현실입니다." — https://www.inflearn.com/course/crm-마케팅-브레이즈?cid=329457 (강의 판매 페이지라 홍보 성격이 있다)
  - 같은 강의 수강평 (sihyun park, 2022-11-12, 3점): 정확한 절차 없이 "이렇게 입력하라"는 식으로만 설명하고, CSV 업로드 예시에 파일 형식 안내가 없다는 불만. 수강 동기는 "Braze 강의 중 가장 저렴해서"였다. — https://www.inflearn.com/community/reviews/105541 → **학습 자료 자체가 부족하고 품질도 고르지 않다**는 신호로 읽힌다.
  - 채용 공고 (리멤버·아이보스): "Braze를 활용해 앱 푸시, 인앱 팝업, 카카오 메시지 등 다양한 채널의 CRM 캠페인을 기획하고 운영해요" 같은 문구가 반복된다. 시니어 공고에는 "주니어 멤버의 업무를 리뷰하고 성장을 지원합니다"가 들어간다. — https://career.rememberapp.co.kr/job/posting/324537 , https://www.i-boss.co.kr/ab-2795-7339
  - 패스트캠퍼스 강의 제목: "물경력 NO! 몸값 올리는 AI CRM 완전 정복 : Liquid 커스텀·API 개인화 캠페인(w. Braze & Claude Code)" — https://fastcampus.co.kr/mktg_online_AiBraze → "물경력" 불안이 시장에서 마케팅 소재로 쓰이고 있다.
- 추정 원인: 한국에서 Braze 도입 기업이 늘어난 속도(야놀자·크몽·우아한형제들·리디 등이 쓴다고 강의 페이지가 주장하지만, 각사 공식 확인은 안 됨)에 비해 사내 교육과 공개 실무 글이 따라오지 못했다. Insider는 한국어 독립 후기 자체를 거의 찾지 못했다.
- 책 활용 아이디어: 서문에 "이 책이 당신의 사수다"라는 포지셔닝 근거로 쓸 수 있다.

### 패턴 3: 개발자·데이터 의존 — "마케터 혼자 다 할 수 있다"는 약속과 현실의 차이
- 출현 예시:
  - Braze / AWS Marketplace (Sung N., 2026-10-24): "Connecting API endpoints and setting up team workspace permission roles required unexpected workarounds." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=32
  - Braze / AWS Marketplace (matias d., 2026-10-31): "we had to develop a whole workaround." (구독 관리 기능 관련) — 같은 페이지
  - Insider One / AWS Marketplace 집계 (Victor Adolfo G., 2026-10-06): "the initial setup still required developer help for custom API integrations" / (Kevin V., 2026-09-25): "We also had some questions during the integration, so we weren't fully independent there." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97
  - 반대 증언 (Insider, 금융업, 2026-09-22): "my team could build and optimize journeys fully independently without heavy technical support." — 같은 페이지
  - The Grow Getter 뉴스레터 (전 Braze 사용자, 2023-11-10): 실시간 인사이트에는 "complex tech integration - that takes a lot of engineering resources"가 필요하다. 플랫폼에 "1 engineer/marketing-tech specialist"를 3~4개월 붙일 수 있어야 한다. "Not all CRMs are created equal. Some are more implementation heavy than others." "P.S: I still love Braze." — https://thegrowthspurt98.beehiiv.com/p/why-are-high-growth-scaleups-going
  - 디지털인사이트 기고 (마티니 아이오, Braze 리셀러라 이해관계 있음): "마케터의 고충 역시 데이터로부터 비롯되는 경우가 많다. 최근엔 데이터 리터러시로 인한 '데이터 갈증'을 호소하는 마케터가 늘고 있다." "메시지 발송을 위해 두 명의 마케터 혹은 개발자와 데이터 분석가 각각 한 명이 필요하다." — https://ditoday.com/?p=82062
  - 아이보스 (이벤트 택소노미 글): "이벤트 택소노미가 잘 구축되어 있으면 필요한 데이터가 빠짐없이 일관되게 쌓이기 때문에 여러 팀이 공통된 지표를 신뢰하며 소통할 수 있습니다." — https://www.i-boss.co.kr/ab-6141-68205
- 추정 원인: 세그먼트·트리거·개인화의 재료는 모두 **SDK가 심은 이벤트와 속성**이다. 그런데 이것을 정하고 심는 일은 개발 조직의 백로그에 들어간다. 마케터의 자율성은 도입 초기 데이터 설계 품질에 비례한다는 것이 커뮤니티의 진단이다.
- 책 활용 아이디어: 데이터·이벤트 설계 장의 오프닝으로 "세그먼트를 만들려는데 필요한 이벤트가 없다. 개발팀 지라 티켓은 3주 뒤" 같은 장면을 쓸 수 있다.

### 패턴 4: Liquid 템플릿 — 강력하지만 QA 부담과 '코드 공포'가 크다
- 출현 예시:
  - Braze / G2 리뷰 `[스니펫]`: Liquid 의존 탓에 "steep learning curve and heavy QA burden"이 있다. — https://www.g2.com/survey_responses/braze-review-3176630 (직접 열람 403, 검색 요약으로만 확인)
  - Braze / AWS Marketplace (Yashaswi J., QA, 2026-10-28) 긍정 쪽: "it gives me a straightforward way to check the Liquid scripting by previewing it with different values" — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=9
  - Braze 리뷰 (검색 요약) `[스니펫]`: Connected Content 같은 기능을 익혀야 하고, Liquid·HTML을 알면 좋으며, API·웹훅 기본 지식이 있으면 최대 활용에 도움이 된다. — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=51
  - Braze 에이전시 Mavlers 블로그 (이해관계 있음): 브랜드가 개인화 확장에서 겪는 장벽으로 "limited developer time, steep Liquid learning curves, and delays in A/B testing"을 든다. — https://www.mavlers.com/blog/brazeai-liquid-assistant-lifecycle-marketing/
  - Braze Bonfire 커뮤니티 (스레드 "Using Liquid to identify users in a segment") `[스니펫]`: 답변 요지는 "The easiest way to do this is add a custom attribute to users in your segment then use liquid to insert your content based on that attribute." — https://community.braze.com/discussions/orchestration/using-liquid-to-identify-users-in-a-segment/4812/replies/4813 (본문 렌더 실패, 검색 요약만 확인)
  - Phiture 블로그 (Alejandra Escobal, 2023-06-20): 이름이 없을 때 처리로 "If there's no first name, we make sure we don't have any blank spaces."를 든다. API 트리거 캠페인에서는 "the CRM manager takes care of all the settings except the actual sending." 그리고 "CRM teams typically have limited resources" — https://phiture.com/mobilegrowthstack/how-to-deploy-liquid-code-crm/
    - 이 글의 예제 코드 자체에도 변수명 불일치(`order_ide`/`order_id`, `product_link`/`product_url`, `favoriteProduct`/`favoriteProducts`)가 있다. 전문가 글에서도 Liquid 오타가 나온다는 사실이 QA 장의 재밌는 실례가 될 수 있다. (본 리서처 관찰, 원문 재확인 필요)
- 추정 원인: Liquid는 문법보다 **"값이 없을 때"(nil/blank) 처리와 발송 전 미리보기 QA**에서 사고가 난다. 한 번 나간 메시지는 되돌릴 수 없다(패턴 5의 고구마팜 인용 참고). 그리고 Braze는 Shopify Liquid를 100% 지원하지 않는다(Braze 공식 FAQ, https://braze.com/docs/user_guide/messaging/design_and_edit/personalize/liquid/faq — web 리서치와 대조 필요).
- 최근 흐름: Braze의 BrazeAI Liquid Assistant와 Claude Code를 쓰는 강의처럼, AI로 Liquid 작성을 돕는 쪽으로 해법이 이동하는 중이다. (2025~2026 흐름, 버전·기능명은 web 리서치에서 1차 소스로 확인 필요)

### 패턴 5: 메시지 피로도 — "자주 보내면 성과가 오른다"는 착각
- 출현 예시:
  - 고구마팜 (갱언니, 2022-04-25): 즉시 구매를 유도하는 푸시는 "발송 빈도가 너무 잦으면 안 돼요." 자주 보내면 할인 직후 구매한 고객이 불쾌해하고, 할인만 기다리는 고객이 생긴다. 치명적 실수로는 "행동 기반의 유저 활동을 분석하지 않거나 브랜딩 메시지 없이 무작정 CRM 채널을 확장하고" 앱 푸시 고도화에만 매달리는 것을 꼽았다. — https://gogumafarm.kr/crm-마케팅의-기본-공식-feat-푸시-메시지/
  - 같은 글: "실제 발송 가능한 모수를 파악하는 게 가장 중요해요." 그리고 "고객의 반응을 확인하는 과정을 무한 반복하는 거죠"
  - 이오플래닛 (헨리퀀, 2022-06-16): "CRM 마케팅의 업무를 단순히 push 메세지 보내는 것으로 생각한다." "Push 발송은 Action item 중의 하나이다." "다른 마케팅 업무 보다 가장 많은 고민이 필요하다고 느꼈다." — https://eopla.net/magazines/1248
  - 실무 요약 글 (아이보스·고구마팜 등, 검색 요약) `[스니펫]`: "발송된 CRM 메시지는 되돌릴 수 없으므로 철저한 여정 설계와 테스트가 필요하다", "처음부터 너무 세분화하기보다 적정한 모수를 먼저 확보하는 것이 중요하다" — https://www.i-boss.co.kr/ab-6141-67309&PB_1499924161=33
  - Airship (벤더, 2026-08) `[스니펫]`: 과다 발송된 유저는 서서히 무시하지 않는다. 푸시 수신 거부, OS 알림 권한 해제, 앱 삭제처럼 단호하게 행동한다. — https://www.airship.com/?p=28399
  - Braze 블로그 (벤더) `[스니펫]`: 주간 전체 상한과 채널별 상한(예: 하루 푸시 상한)을 겹쳐 쓰라고 권한다. 상한 override가 잦으면 상한이 너무 낮게 잡힌 신호라고 본다. — https://www.braze.com/resources/articles/dont-bury-customers-notifications.md
- 추정 원인: 캠페인 단위 성과(CTR)만 보면 더 보낼수록 이득처럼 보인다. 피로도 비용(수신 거부·앱 삭제)은 캠페인 리포트에 잡히지 않는다. 여러 팀이 각자 보내면 전역 빈도 상한이 없다는 점이 드러난다.
- 한국 특수성: 앱푸시 외에 알림톡·친구톡·LMS 비용 구조가 있고, 정보통신망법 광고성 정보 규정(야간 발송·수신 동의)도 있다. 실무 글에 따르면 "플러스친구와 LMS는 비용이 비싸고, 앱푸시·인앱·eDM은 비용이 적은 편"이다 `[스니펫]`. 법규는 web 리서치 및 KISA 1차 소스와 대조해야 한다.

### 패턴 6: "그래서 이 메시지가 매출을 올렸나?" — 성과 측정·증분(incrementality)
- 출현 예시:
  - Monzo 데이터 블로그 (Rodrigo Baptista, Senior Data Scientist, 2025-09-03): 유저의 2.5%를 6개월간 CRM 메시지에서 무작위로 제외하는 유니버설 홀드아웃을 운영한다. 어트리뷰션 모델은 "tend to claim too much" 하므로 홀드아웃 기준으로 하향 보정한다(예: 홀드아웃 기준 100건, 어트리뷰션 200건이면 계수 0.5). "Individual experiment uplifts are non additive." — https://monzo.com/blog/beyond-the-last-click-how-monzo-measures-crms-true-impact
  - Insider One / AWS Marketplace 집계 (리테일, 2026-10-30): "The dashboard analytics still feel limited and not very flexible" / (여행업): "Sometimes it's hard to dig up the analytics we are looking for." / (금융업): "Third-party integrations, revenue analytics, and campaign analytics are very weak for me." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97
  - Braze / AWS Marketplace (Bret C.) 긍정 쪽: "the dashboard makes it simple to see what's working at a glance." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=9
  - KakaoStyle(지그재그) Braze 사례 (벤더 게재): 툴 안 리포트 대신 Braze Currents로 메시지 참여 이벤트를 S3로 스트리밍한다. 내부 회원 등급·연령·구매 이력과 합쳐 QuickSight로 분석한다. "our app traffic has jumped by 35%" (벤더 게재 수치) — https://www-origin.braze.com/customers/kakaostyle-case-study
- 추정 원인: 툴 대시보드는 열람·클릭 중심이다. "보내지 않았으면 어땠을까"는 대조군 설계 없이는 답할 수 없다. 성숙한 팀은 툴 밖(DW·BI)으로 데이터를 빼서 측정한다. 주니어는 CTR만 보고, CTR을 성과로 착각하기 쉽다.
- 책 활용 아이디어: 성과 측정 장의 오프닝으로 "CTR 12%를 보고했더니 팀장이 물었다. '안 보냈으면 몇 명이 샀을까?'" 같은 장면을 쓸 수 있다.

### 패턴 7: 비용 구조 불투명 — 데이터 포인트·메시지 크레딧
- 출현 예시:
  - Braze / AWS Marketplace (matias d., 2026-10-31): "The billing is tricky to understand because I have to work out how many message credits I need" — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=9
  - The Grow Getter (2023-11-10): "Braze is very expensive. Period." 비용은 데이터 포인트 추가, SMS(Twilio), 콘텐츠 카드 같은 애드온으로 늘어난다. — https://thegrowthspurt98.beehiiv.com/p/why-are-high-growth-scaleups-going
  - Fivetran 블로그 인용 고객 / G2 리뷰 `[스니펫]`: "The cost for data usage limits us from importing all of our data." — https://www.fivetran.com/blog/data-api-costs-braze-fivetran-activations (Fivetran은 이해관계 있음)
  - Insider / PeerSpot (reviewer2908521, 2026-10-08): "The price is not very cheap for Insider, especially when compared to other platforms" — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97
- 주니어 관점의 함의: "모든 데이터를 다 넣자"가 공짜가 아니다. 어떤 속성·이벤트를 보낼지가 비용 결정이 된다. 마케터가 이 사실을 모르면 개발·데이터팀과의 대화가 엇갈린다. (가격 정책 세부는 web 리서치·Braze 공식 data points 문서와 대조 필요: https://braze.com/docs/ko/user_guide/data/infrastructure/data_points/)

### 패턴 8: 캔버스/여정이 커지면 '스파게티'가 된다
- 출현 예시:
  - Braze 리뷰 (검색 요약) `[스니펫]`: "캔버스 빌더가 매우 제한적이며, 예를 들어 복사·붙여넣기 기능이 없다", "캔버스가 분기와 복제가 많아 복잡해지면 전체 구조를 파악하기 어렵다" — https://trustradius.com/reviews/braze-2024-04-12-09-11-34 및 Capterra (직접 열람 403)
  - Insider / Gartner 리뷰 `[스니펫]`: Architect가 "without asking engineers every time" 여정을 짤 수 있다는 호평이 있다. 2024년 3.0점 리뷰는 "steep initial learning curve"를 지적했다. — https://www.gartner.com/reviews/market/multichannel-marketing-hubs/vendor/insider-one
  - Insider / AWS 집계 (리테일, 2026-10-30): "we still can't combine audience filters with dynamic segments." / (Victor Adolfo G.): "Initial segment rules also needed manual adjustments to filter out already purchased items." — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97
- 추정 원인: 여정 설계를 문서화(목표·진입 조건·이탈 조건·전환 이벤트)하지 않고 툴 위에서 바로 그리면, 분기가 쌓이면서 아무도 전체를 이해하지 못하게 된다. "이미 구매한 사람 제외" 같은 exit 조건 누락이 대표적인 사고다.

---

## 실무 휴리스틱

### 휴리스틱 1: 세그먼트를 처음부터 잘게 쪼개지 말고, 발송 가능한 모수부터 확인하라
- 출처: https://gogumafarm.kr/crm-마케팅의-기본-공식-feat-푸시-메시지/ (2022-04-25)
- 원문:
  > "실제 발송 가능한 모수를 파악하는 게 가장 중요해요."
- 보강 `[스니펫]`: "처음부터 너무 세분화하기보다 적정한 모수를 먼저 확보하는 것이 중요하다" (아이보스 계열 실무 글)
- 동조 반응: 크몽 CRM 마케터 강의도 RFM·코호트로 고객을 먼저 분류한 뒤 Braze 세그먼트를 설정하는 순서를 제시한다(데이터 설계가 먼저). — https://comento.kr/class/pt/content/braze를-활용한-crm-마케팅-개인화/76

### 휴리스틱 2: Liquid 분기에는 "값이 없을 때"를 반드시 설계하고, 여러 값으로 미리보기하라
- 출처: Phiture(2023-06-20), AWS Marketplace Braze 리뷰(Yashaswi J., QA, 2026-10-28)
- 원문:
  > "If there's no first name, we make sure we don't have any blank spaces."
  > "it gives me a straightforward way to check the Liquid scripting by previewing it with different values"
- 동조 반응: Braze 공식 FAQ도 Liquid가 들어간 메시지는 발송 전에 모두 테스트하라고 권한다(공식 문서, web 리서치 대조).

### 휴리스틱 3: Liquid로 복잡하게 세그먼트를 판별하지 말고, 세그먼트를 커스텀 속성으로 '굳혀서' 참조하라
- 출처: Braze Bonfire 커뮤니티 답변 `[스니펫]` — https://community.braze.com/discussions/orchestration/using-liquid-to-identify-users-in-a-segment/4812/replies/4813
- 원문:
  > "The easiest way to do this is add a custom attribute to users in your segment then use liquid to insert your content based on that attribute."

### 휴리스틱 4: 전체 CRM 효과는 유니버설 홀드아웃으로, 개별 메시지 기여는 어트리뷰션을 홀드아웃에 맞춰 보정해서 봐라
- 출처: Monzo (2025-09-03) — https://monzo.com/blog/beyond-the-last-click-how-monzo-measures-crms-true-impact
- 원문:
  > 어트리뷰션 모델은 "tend to claim too much"
  > "Individual experiment uplifts are non additive"
- 보강 (CRM 실험 강의, 검색 요약) `[스니펫]`: 캠페인 한 번의 대조군으로는 빈도·피로도 효과를 볼 수 없다. 발송 주기(cadence)는 따로 실험하고 글로벌 홀드아웃을 유지하라. — https://www.datainterview.com/courses/marketing-ads-analytics/crm-lifecycle-experiments
- 한국 사례: 잡코리아는 랜덤 샘플 사전 테스트와 대조군 대비 CVR 비교를 썼다(아래 사례 2).

### 휴리스틱 5: 도입 전에 '마케팅 테크 담당 1명'을 몇 달 붙일 수 있는지부터 확인하라
- 출처: The Grow Getter (2023-11-10) — https://thegrowthspurt98.beehiiv.com/p/why-are-high-growth-scaleups-going
- 원문:
  > "1 engineer/marketing-tech specialist" (3~4개월, 다른 프로젝트를 방해하지 않고)
  > 실시간 커뮤니케이션 의존도가 낮으면 다른 CRM을 고려하라 ("heavily reliant on real time communications" 여부가 선택 기준)
- 동조 반응: Braze 리뷰의 "implementation requires technical/data/engineering resources" `[스니펫]`, Insider 리뷰의 "required developer help for custom API integrations"

### 휴리스틱 6: CRM은 푸시가 아니라 "why·what·how"부터 정하는 일이다
- 출처: 이오플래닛 헨리퀀 (2022-06-16) — https://eopla.net/magazines/1248
- 원문:
  > "실행을 위한 \"why, what, how\" 가 정말 중요하다."
  > "언제, 어떤 내용으로, 무엇을 유저에게 제공할 지에 따라" 고객 경험이 좋아지거나 이탈이 생긴다.

---

## 실제 캠페인 사례 (현장 소재)

> 이 절의 성과 수치는 모두 **벤더 게재 수치**다. 기준값·표본·유의성이 공개되지 않았다. 책에서는 "회사 측 발표에 따르면"으로 표기하고 fact-checker 대조를 권한다.

### 사례 1: 잡코리아 × Braze — 가입 경과일 Liquid 개인화 + 이력서 완성 슬라이드업
- 출처: https://www.braze.com/ko/customers/jobkorea-case-study (게재일 미표기, 캠페인은 2023-11 전후, 2024 상반기 계획 언급)
- 문제: 지원 이후 단계(서류·면접·결과)를 추적할 수 없었다. 프로필·이력서 작성 전에는 신입/경력을 구분하지 못했다. 경력자에게 구직 활동은 민감할 수 있어 푸시 타이밍이 어려웠다. 웹 푸시는 리소스 대비 효과가 불명확해 보류했다.
- 실행: 마케터가 개발 도움 없이 세그먼트를 만들었다. 커스텀 속성은 캔버스·실시간·CSV 일회성 업로드로 갱신했다. Liquid로 가입일을 날짜 형식으로 바꿔 경과 일수를 계산해 넣었고, 기업명·직무·희망 직무·경력 연수로도 개인화했다. 이력서 미등록자 대상 슬라이드업 인앱 메시지 예: "잡코리아에 가입한 n일동안, 경쟁자들은 연봉 UP하고 있어요!" 랜덤 샘플 사전 테스트와 색상·크리에이티브·아이콘(로고·마스코트) A/B 테스트도 했다.
- 담당자 발언: "CRM 담당자인 제가 다양한 시도를 할 수 있었던 배경에는 Braze가 있었습니다."
- 성과(벤더 게재): "이전과 비슷한 모수여도 평균 CTR이 4~5배 수준이나 오를 정도로 좋은 유입 성과", 슬라이드업 CTR 두 자릿수 근접(같은 목표의 다른 인앱 대비 약 4%p↑), 대조군 대비 CVR↑, "CTR을 5%p 이상 향상"
- 책 활용: Liquid 개인화 장의 대표 실습 사례로 쓸 수 있다(날짜 계산 → 문구 삽입). 패턴 3(마케터 자율성)의 긍정 사례이기도 하다.

### 사례 2: 카카오스타일(지그재그) × Braze — Currents로 참여 데이터를 사내 DW와 결합
- 출처: https://www-origin.braze.com/customers/kakaostyle-case-study (게재일 미표기)
- 실행: Braze Currents로 메시지 참여 이벤트를 AWS S3에 실시간 스트리밍했다. 회원 등급·연령·구매 이력과 결합해 QuickSight 대시보드를 만들고, 어떤 세그먼트가 어떤 크리에이티브에 반응하는지 찾아 프로모션 팀에 공유했다. 채널은 푸시·인앱·카카오톡 채널이다.
- 성과(벤더 게재): "our app traffic has jumped by 35%"
- 책 활용: 성과 측정 장에서 "툴 밖으로 데이터를 빼야 진짜 분석이 된다"는 예시로 쓸 수 있다.

### 사례 3: 레노버 코리아 × Insider — 고관여 제품 여정 자동화
- 출처: https://useinsider.com/assets/media/2023/10/Lenovo-Korean-Case-Study.pdf (2023-10 게시, 검색 요약으로만 확인 `[스니펫]`)
- 요지: 자사몰에서 오디언스별 맞춤 경험을 제공했다. 담당자는 고관여 제품군에 고객 여정 자동화를 추천한다고 코멘트했다. 구체 수치는 미확인.
- 참고: Insider 한국어 고객 페이지(https://insiderone.com/ko/customers/)에는 "웹사이트 개인화 캠페인으로 전환율 최대 78% 개선" 같은 수치가 있지만 브랜드·조건이 불분명하다(벤더 게재).

### 사례 4: Braze 한국 시장 — 카카오톡 채널·국내 데이터센터 (도구 환경 변화)
- 출처: 벤처스퀘어 (2026-04-08) — https://www.venturesquare.net/fr/1074745/
- 요지: AWS 기반 국내 데이터센터를 운영해 전화번호 등 개인정보를 국내에 저장한다. 카카오톡 채널을 출시해 노코드 작성, 실시간 타깃 발송, 타 채널과 연결된 여정을 지원한다. 카카오 AD 도메인 전현수 리드가 인용됐다.
- 맥락: Braze 리셀러 마티니 아이오는 "3년만에 300억 매출"을 냈다(바이라인네트워크, 2025-12-04, https://byline.network/2025/12/4-374/). 국내 도입이 확산 중이라는 신호다.
- Insider 쪽: 2024-11 시리즈E 5억 달러 유치와 함께 2027년까지 한국에 1,500억 원 투자, 일자리 60개 창출 계획을 발표했다(벤더 발표, https://insiderone.com/ko/news/insider-kr-invest-1500-krw-create-60-jobs-following-500m-usd-series-e).
- 책 활용: 한국 주니어가 실제로 만나는 채널 조합(앱푸시 + 카카오톡)이 두 툴 모두에서 일급 기능이 되어 가고 있다. 기능 존재 여부·출시 시점은 web 리서치 1차 소스로 확인해야 한다.

---

## 논쟁점

### 논쟁 A: "비기술 마케터도 혼자 쓸 수 있다" vs "개발·데이터 리소스 없이는 반쪽짜리"
- 관점 1 (혼자 가능):
  - Braze / Capterra (라이프사이클 마케터) `[스니펫]`: 크로스채널 오케스트레이션과 실시간 세그먼트 때문에 골랐고, SQL이 필요 없었다. — https://capterra.com/p/155423/Appboy/reviews/
  - Insider / 금융업 (2026-09-22): "my team could build and optimize journeys fully independently without heavy technical support."
  - 잡코리아: 마케터가 개발 도움 없이 세부 세그먼트를 구성했다.
- 관점 2 (리소스 필수):
  - The Grow Getter: "complex tech integration - that takes a lot of engineering resources."
  - Insider / Victor Adolfo G.: "the initial setup still required developer help for custom API integrations"
  - Braze / Sung N.: "required unexpected workarounds."
- 화해 지점: 양쪽 다 맞다. **도입·연동 단계는 개발 의존, 데이터가 잘 깔린 뒤 운영 단계는 마케터 자율**이다. 주니어가 들어가는 시점(이미 도입된 회사인지)에 따라 체감이 정반대가 된다.

### 논쟁 B: Insider One vs Braze — 어느 쪽이 쉬운가, 무엇에 강한가
- 관점 1 (Insider가 쉽다·웹 개인화 강점): CleverTap 비교 글(경쟁사라 편향)에서 리뷰어들은 Insider가 셋업·지원에서 높은 점수를 받는다고 정리했다 `[스니펫]`. G2 평점은 Insider One 4.8(약 1,413건), Braze 4.5(약 1,685건) — 검색 시점 스니펫이며 fact-checker 확인이 필요하다. Insider 리뷰는 "the human customer service stands out and has been remarkable"(여행업, 2026-10-29). — https://clevertap.com/blog/braze-vs-insider/ , https://www.g2.com/compare/braze-vs-insider-vs-iterable
- 관점 2 (Braze가 복잡 여정·앱 중심에 강함): 같은 비교에서 Braze는 복잡한 캔버스 기반 여정에 강하다는 평. Insider도 셋업이 "overwhelming"할 수 있다는 지적이 있다 `[스니펫]`.
- 주의: 비교 콘텐츠 대부분이 벤더(Insider 자사 블로그, CleverTap)가 쓴 것이다. 독립적인 실무자 비교 토론(Reddit 등)은 확보하지 못했다.

### 논쟁 C: AI 기능 — 생산성 도구인가, 아직 미덥지 않은가
- 관점 1: Insider 금융업 리뷰어 (2026-10-19): "I find the AI Agent really helpful, especially since I can now use prompts to create gamified pop-ups." BrazeAI Liquid Assistant는 개발자 개입 없이 Liquid를 쓰게 한다는 주장이다(에이전시 주장).
- 관점 2: Insider 리뷰 (Kevin V., 2026-09-25): "On the AI side, it's not always consistent" / (금융업, 2026-09-22): "The AI feels only average overall: accuracy, consistency, explainability, controls, and trust are all just mid-level." / (PeerSpot, 2026-10-08): "I did not enjoy using Insider AI to generate copies" — https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97
- 책 활용: AI 기능 장에서 "AI가 써준 Liquid·카피도 결국 QA는 사람이 한다"는 균형 잡힌 톤의 근거로 쓸 수 있다.

### 논쟁 D: 발송량 vs 관련성 — 피로도 관리의 단위
- 관점 1 (빈도 상한 중심): Braze 권고처럼 전역·채널별 빈도 상한을 겹쳐 쓴다(벤더).
- 관점 2 (관련성 중심): Airship은 발송 수보다 관련성이 중요하다고 본다(벤더). 고구마팜은 "브랜딩 메시지 없이 무작정 CRM 채널을 확장"하는 것을 실수로 꼽는다.
- 관점 3 (측정 중심): 피로도는 캠페인 단위 실험으로 보이지 않으므로 cadence 실험과 글로벌 홀드아웃이 필요하다(CRM 실험 강의, Monzo).

---

## 수집 한계
- **미접근 플랫폼:** Reddit(r/marketing, r/emailmarketing, r/ProductManagement)은 WebFetch 차단, 검색 엔진도 Reddit 스레드를 반환하지 않았다. 원문 토론은 0건이다. G2·Capterra·TrustRadius 개별 페이지는 403이라 검색 스니펫과 AWS Marketplace(G2·PeerSpot 리뷰 신디케이션)로 대체했다. LinkedIn은 미접근. Braze Bonfire는 스레드 본문 렌더 실패로 스니펫 1건만 확인했다. 브런치·velog·요즘IT·커리어리에서는 Braze/Insider 도입기를 검색으로 찾지 못했다.
- **언어·제품 편중:** Braze 쪽 자료가 Insider보다 훨씬 많다. Insider는 한국어 독립 후기가 사실상 0건이고, 영어 리뷰(AWS 집계)와 벤더 사례에 의존했다. 한국 자료는 실무 매거진(고구마팜·이오플래닛·아이보스·디지털인사이트)과 벤더 사례가 중심이며, 개인 실무자의 날것 후기는 적다.
- **이해관계 소스:** 마티니 아이오(Braze 리셀러), Mavlers(Braze 에이전시), CleverTap·Insider 비교 글(경쟁사), Fivetran·RudderStack(연동 벤더)은 편향 가능성이 있다. 해당 항목에 표기했다.
- **신선도:** AWS Marketplace 리뷰는 2026-09~10 작성분이라 최신이다. 한국 실무 글은 2022년 작성분이 많다. 툴 기능(BrazeAI Liquid Assistant, Braze 카카오톡 채널, Insider AI Agent)은 2025~2026 변화가 커서 web 리서치 1차 소스 대조가 필요하다.
- **보강 권고:** 운영자 계정으로 Reddit·LinkedIn·커리어리를 직접 검색하는 것, Braze Bonfire 스레드 원문을 확보하는 것, Insider 한국 지사 사례집을 받는 것.
