# 책 산출 교훈 (하네스 학습 루프)

오케스트레이터가 책 한 권을 마칠 때마다 한 레코드를 append한다. planner·writer 브리프에 같은 장르의 최근 레코드를 참고 메모로 넣는다.

## 2026-10-03 — cloudflare-developer-cloud

- **topic:** Cloudflare를 개발자의 배포·운영 클라우드로 쓰기 (『Cloudflare를 나의 클라우드로』 v1.0.0)
- **genre:** tech-book · delegation_mode: production
- **챕터 수:** 14장 + 부록 3 (A·C는 editor가 레퍼런스 표에서 기계적으로 작성)
- **분량 준수도:** 계획 153,000자 → 실측 165,479자(+8%). 수락 게이트 수정분으로 8·9·11장이 계획 대비 +22~29%. 1장은 중앙값 대비 71%(계획된 짧은 도입).
- **반복된 사실 이슈:**
  - 레퍼런스에 **설정 문법·API 시그니처**(wrangler 바인딩 키, Hono/D1/DO/Queues API)가 없어 저술가가 코드 블록마다 `(사실 확인 필요)`를 달았다 → fact-checker가 웹 2차로 전부 해소(1~4장 19개, 5~7장 17개, 8~10장 21개, 11~14장 13개). 실습형 tech-book은 리서치 단계에서 "핵심 설정·API 시그니처 표"를 web-researcher 필수 산출로 요구하면 왕복이 준다.
  - 돌려보면 깨지는 코드 오류가 검수에서 잡혔다: Containers `start()`의 `enableInternet` 필수, Queues pull의 JSON base64, vinext legacy deploy 명령, Billable Usage API `BilledCost`→`ContractedCost`, Workers에서 presigned URL은 AWS SDK v3가 아니라 `aws4fetch`(공식 Workers 예제).
  - 빠르게 바뀌는 제품의 정전이 계획 이후에도 움직였다: vinext 1.0(2026-09-28)이 `cf`+`cloudflare.config.ts`를 기본으로, DO 선언이 `migrations`→선언형 `exports`. Phase 3 승인 대기 시간에 갭 보강 리서치를 띄운 것이 유효했다.
- **수락 게이트 BLOCK 사유 (라운드 1):** (f) 약속 미이행 — 4장 인증 없는 R2 업로드 경로가 끝까지 잠기지 않음, presigned URL 권고만 있고 생성 예제 없음. (e) 상호 참조 — 병렬 묶음 간 예제 코드 불일치(큐 메시지 형태, `export default` 중복, 컬럼명, 없는 `published` 열, 스키마와 다른 멱등 키). 라운드 2 ACCEPT.
- **교훈:** 병렬 저술 + 묶음별 fact-check는 장 내부 정확성은 지키지만 **러닝 예제의 장 간 코드 계약**(스키마·메시지 형태·export 구조)은 못 지킨다. planner의 예제 고정 명세에 스키마·바인딩·메시지 타입을 코드 수준으로 박아 두거나, editor 통합 시 "예제 코드 계약 대조"를 명시 항목으로 둘 것. 오케스트레이터가 묶음 보고에서 장 간 플래그를 `integration_flags.md`로 모아 editor에 넘긴 방식은 유효했다.
