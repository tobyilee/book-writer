# Braze 분석 화면·리포트·Global Control Group / Insider One 전역 대조군 (수락 게이트 f 보강)

- 조사: fact-checker, 검색 시점 2026-11-03. 모두 벤더 공식 문서(1차). 페이지에 발행·수정일 표기 없음 → "2026-11 기준"으로 쓴다.
- 정확한 화면 문구·메뉴 이름은 UI 개편으로 바뀔 수 있다. 본문에서는 "2026-11 기준 Braze Docs" 정도의 시점 표기를 권한다.

## A. Braze Canvas 분석 (확인)
출처: https://www.braze.com/docs/user_guide/engagement_tools/canvas/testing_canvases/measuring_and_testing_with_canvas_analytics/

- 상단 요약(Canvas Details): 발송 메시지 수(Messages sent), 총 진입(Total entries), 전환 수·전환율, 총 매출(Total Revenue — Canvas에 진입한 사용자가 전환 기간 안에 낸 매출), 총 이탈(Total exits), 예상 오디언스(Reachable users). 팀 편집 이력을 여는 "Changes Since Last Viewed"도 있음.
- 단계(컴포넌트)별: 진입·다음 단계 이동·이탈 사용자 수, 노출(impressions)·고유 수신자(unique recipients)·전환 수·매출. 컴포넌트를 누르면 채널별 성과. "Show Revenue Breakdown"은 단계별 매출과 "Not attributed to a step" 행.
- 변형별(Analyze Variants 탭): 변형별 총 진입·총 발송·총 매출, 전환 이벤트마다 전환 수·전환율, 대조 변형 대비 상승(Uplift against the control variant)과 통계적 신뢰도(confidence). CSV 다운로드.
- 같은 Analyze 화면에 Canvas Funnel Report·Canvas Retention Report 탭.
- 주의(문서 명시): 전환은 Canvas 진입당 전환 이벤트별 1회만 센다. 전환은 가장 최근에 받은 메시지에 귀속 — 메시지를 받기 전 전환하면 Canvas 수준에는 잡히고 단계 수준에는 안 잡힌다. 매출은 기본 전환 이벤트와 무관하게 귀속 기간 안 구매면 총 매출에 포함.
- 이 페이지는 Canvas 요약에 unique opens/clicks를 나열하지 않는다(채널 지표는 컴포넌트·채널 화면에서). 본문에 "Canvas 상단에 고유 열람이 뜬다"고 쓰지 말 것.

## B. Braze 캠페인 분석 (확인)
출처: https://www.braze.com/docs/user_guide/analytics/reporting/ (개요), https://www.braze.com/docs/user_guide/messaging/ab_testing/analytics , https://www.braze.com/docs/user_guide/data_and_analytics/report_metrics (지표 용어집)

- 캠페인 분석: 캠페인별 결과를 메시징 채널별로 나눠 보여 줌(개요 페이지 설명).
- 채널 지표 예(용어집): Unique Opens(이메일은 7일 창, 사용자당 1회; Unique Open Rate = Unique Opens / Deliveries. Apple MPP 때문에 Other Opens·Estimated Real Opens도 별도 제공), Unique Clicks(7일 창), Primary Conversions(캠페인 설정 시 정한 이벤트, 추가 이벤트는 Conversions B·C·D). 비인앱 채널 전환율 = Primary Conversions / Unique Recipients.
- 변형·대조군: 수동 배분 다변량 캠페인은 변형별 성과를 대조군 대비로 표시. "Confidence will only appear if you have a control group." 비합동(unpooled) 두 비율 Z-검정, 95% 이상이면 의미 있는 차이로 안내. Optimize with BrazeAI 사용 시 실험 창 이후 개요에 uplift, Personalized Variant는 "Projected lift" 카드.

## C. Braze 리포트 기능 목록 (확인, 2026-11 기준 Reports 개요)
출처: https://www.braze.com/docs/user_guide/analytics/reporting/ , https://www.braze.com/docs/user_guide/analytics/reporting/report_builder/
- Campaign analytics / Canvas analytics (위 A·B)
- Report Builder: 여러 캠페인·Canvas 결과를 비교. 행 = 캠페인, Canvas, 캠페인+Canvas, 채널, 태그, 국가(Shopify Markets), 세그먼트. 드릴다운 = 채널·날짜·변형·캠페인/Canvas·국가·세그먼트. 지표 = 전환·진입·발송·고유 수신자·고유 노출·매출 등. CSV, 예약 이메일, 대시보드에 추가 가능. 현재 문서는 "Report Builder (New)"이고 "Report Builder (legacy)"가 따로 있음. 베타/GA 표기 없음.
- Dashboard Builder: Report Builder 리포트를 모아 대시보드 구성(Report Builder 문서에 언급). 베타/GA 표기 확인 안 함.
- Query Builder: Braze 데이터(Snowflake)에 SQL 또는 템플릿.
- Engagement reports: 선택한 캠페인·Canvas의 참여 통계를 정기 CSV로 내보내기.
- Custom events report, Revenue report.
- Funnel reports: 캠페인·Canvas 이후 사용자 경로와 이탈 지점.
- Retention reports: 캠페인·Canvas가 최대 30일 동안 사용자를 얼마나 다시 불러오는지.
- 개요 페이지는 어느 리포트에도 베타 표기를 하지 않는다 → 본문에 GA/베타를 단정하지 말 것.

## D. Braze Global Control Group (확인)
출처: https://www.braze.com/docs/user_guide/engagement_tools/testing/global_control_group/
- 존재: 있음. Audience > Global Control Group에서 비율을 입력하고 저장하면 전체 사용자 중 그 비율을 무작위로 배정, 이 사용자들은 캠페인·Canvas를 받지 않는다.
- 비율: 1~15의 정수만. 권장은 최소 1,000명, 전체 오디언스의 10% 이하. 사용자 1만 명 미만이면 1,000명을 채우려 비율을 올려도 되지만 15%가 상한.
- 신규 사용자는 같은 무작위 버킷이면 자동 편입 → 사용자 기반 대비 일정 비율 유지.
- 예외(Exclusion settings): 태그를 지정하면 그 태그가 붙은 캠페인·Canvas는 대조군을 무시하고 전원에게 발송 — 거래성(transactional) 메시지 예외에 쓰라고 안내. API 캠페인은 대조군 사용자에게도 발송되지만, API 트리거 Content Card 캠페인은 예외가 아니다.
- 재무작위화: 크기를 직접 바꿀 수 없다. 비활성화 후 새로 만들어야 하고, 그때 구성원이 다시 섞인다. 비활성화 즉시 기존 구성원이 메시지 대상이 되며 복구 불가 → 먼저 CSV로 내보내라고 안내. 셔플은 대략 월 1회 이하, 실험 기간은 약 3개월로 시작·1개월보다 짧게 하지 말라고 권장.
- 제약: 워크스페이스당 Global Control Group 1개 + 처리군 샘플 1개. 개별 사용자 제거 불가. 대조군 구성원은 피처 플래그·피처 플래그 실험에 등록 불가. 메시지별 대조군과 함께 쓸 수 있음.
- Global Control Group Report (Analytics > Global Control Group Report): 세션 또는 커스텀 이벤트와 기간을 골라 실행, 대조군과 비슷한 크기의 처리군 샘플을 비교하고 신뢰도(%) 표시. 지표 = Change from Control(전환율 상대 차이), Incremental Uplift(이벤트 총수 차), Incremental Uplift Percent, Conversion Rate(총 이벤트 / 일별 그룹 크기 합), Estimated Group Size(기간 중 최대 인원), Total Number of Events(고유 사용자 아님), Events Per User.

Monzo 방식(2.5%·6개월, research/community.md C-휴4)과의 비교 포인트: Braze는 1~15% 정수·권장 ≤10%, 셔플 월 1회 이하·실험 3개월 시작 권장, 거래성 메시지는 태그로 예외 — "정보성 메시지 제외"를 태그 예외로 구현하는 셈.

## E. Insider One 전역(유니버설) 대조군 — 확인되지 않음
- Academy(academy.insiderone.com / academy.useinsider.com) 검색에서 "Global Control Group"·"Universal Control Group"에 해당하는, 모든 캠페인·여정에서 사용자를 빼 두는 기능 문서를 찾지 못했다(2026-11-03).
- 확인된 것: 캠페인 단위 대조군 분석. Executive Summary Dashboard의 "OnSite Campaigns with Control Group Analytics"(증분 매출 = 변형과 대조군의 차, 전환율 상승). Architect 섹션에는 대조군 언급 없음. https://academy.insiderone.com/docs/executive-summary-dashboard-details
- Insider One 블로그(벤더 2차) "Journey orchestration pilot metrics"는 비오케스트레이션 코호트와 비교하는 홀드아웃을 직접 만들고 방법을 문서화하라고 권한다: https://insiderone.com/journey-orchestration-pilot-metrics/ — 전용 기능이 있다는 근거는 아님.
- 본문 권장 표현: "Insider One은 2026-11 기준 Academy 문서에서 전역 대조군 기능을 확인하지 못했다 — 여정 단위 A/B·대조군과 직접 만든 홀드아웃 세그먼트로 대신한다" 수준. "기능이 없다"고 단정하지 말 것.
