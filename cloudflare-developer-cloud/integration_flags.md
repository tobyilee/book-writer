# 통합 시 확인할 교차 장 플래그 (오케스트레이터 수집, 2026-10-03)

editor가 통합할 때 처리한다. 각 항목의 출처 보고자를 괄호로 적었다.

1. **11장 종료 상태가 계획 표와 다름** (11~14 저술가) — Worker 렌더 HTML은 존 캐시를 거치지 않으므로 `moim-web`은 Workers Cache + `ctx.cache.purge({tags})` + 60초 `max-age`. 존 캐시·Cache Rules는 Spring 오리진 경로에서 시연. `02_plan.md`의 장별 종료 상태 표 11장 행을 갱신하고, 앞 장(2·5장)의 캐싱 예고가 이와 맞는지 확인.
2. **`moim-web` 배포 예외** (5~7 fact-checker) — vinext legacy 경로라 `moim-web`은 루트 `wrangler.jsonc`에 대한 `wrangler deploy`가 아니라 `npm run deploy`(= `vinext-cloudflare deploy --config dist/server/wrangler.json`)로 배포. 8장(GitHub Actions)·13장(`limits.*` 규약)에서 `moim-web`을 다룰 때 이 예외와 맞는지 확인.
3. **Preview × Containers 서술 불일치 가능성** (5~7 fact-checker) — Worker Previews 블로그(2026-09-22, 5장 인용)는 프리뷰마다 Containers 인스턴스가 생긴다고, Containers FAQ(2026-10-02, 7장 인용)는 Containers Worker에 preview URL이 생성되지 않는다고 읽힌다. 7장은 Workers Builds 버전별 preview URL로 한정했다. 5·7·13장 서술이 서로 모순되지 않게 맞춘다.
4. **13장·부록 B의 `max_instances` 의존** (11~14 저술가) — 7장 final의 Containers 설정(`instance_type`·`max_instances`, 기본 정책)과 일치해야 한다. 14장 아키텍처 그림의 `moim-report` Cron Worker도 7장과 일치 확인.
5. **새 박스 유형 `> **논쟁: …**`** (12·13장) — 계획의 고정 박스 이름에 없음. 통일 여부 결정.
6. **4장 presigned URL** (1~4 저술가) — 4장은 가리키기만 하고 생성법은 8장. 8장에 실제로 생성 예제가 있는지 확인.
7. **R2 Java SDK는 7장 담당** (8~10 저술가) — 8장은 한 문장 참조. 중복 없는지 확인.
8. **`ctx.access` 구조** (8~10 저술가) — `moim-web`(정적 자산 Worker)에서는 `ctx.access`를 못 쓰므로 10장은 `Cf-Access-Jwt-Assertion`을 jose로 직접 검증, Service binding 호출에 헤더를 실어 `moim-api`가 재검증. 다른 장에서 `ctx.access`를 `moim-web`에 쓴다고 서술한 곳이 없는지 확인.
9. **Durable Object 선언 형식 — 오케스트레이터 결정: 책 전체를 선언형 `exports`로 통일** (1~4 fact-checker) — Wrangler 설정 문서(2026-10-02)가 `migrations`를 "legacy"로 표기하고 "For new Workers, prefer the declarative exports field"라 적으며 `exports`는 2026-07 GA. 4장은 이미 `"exports": { "EventSeats": { "type": "durable-object", "storage": "sqlite" } }`로 바뀌었다. 7장(`ReportContainer`, 07_final.md 약 160행)·13장(`UsageMeter`, 13_final.md 약 217행)의 `migrations`/`new_sqlite_classes`를 `exports`로 바꾸고, 7장 본문의 "둘 다 허용, 혼용 불가" 설명은 4장 설명과 겹치지 않게 짧은 참조로 줄인다. Containers의 DO 클래스에 `exports` 형식이 그대로 적용되는지(키 이름) `research/web_gaps.md` §3·Wrangler 문서로 확인하고, 확인 못 하면 7장만 `migrations`로 두고 그 이유를 한 문장 밝힌다.
10. **custom domain vs route 판정: 설계 그대로 동작, 구조 변경 없음** (1~4 fact-checker) — 라우트 Worker(`moim-api`, `/api/*`)가 커스텀 도메인 Worker(`moim-web`) 앞에서 먼저 받는다(Custom Domains 문서 2026-09-29).
11. **kentonv 10GB 발언은 D1이 아니라 Durable Objects SQLite DB에 관한 것** (1~4 fact-checker) — 레퍼런스 §3-3 논쟁 B에도 오귀속이 있다. 다른 장에서 D1 근거로 쓴 곳이 있으면 고친다.
12. **3장 테스트는 `cloudflare:test`의 `SELF`(deprecated) 대신 `exports.default.fetch()`** — 다른 장의 테스트 예제가 `SELF`를 쓰면 맞춘다.
13. **CI 예제 버전 통일** (8~10 fact-checker) — 8장은 Cloudflare 문서 예제에 맞춰 `actions/checkout@v6`. 5장(Workers Builds·CI) 등 다른 장의 GitHub Actions 예제가 `@v4`면 맞춘다. `wrangler-action` 입력명은 `apiToken`·`accountId`·`command`.
14. **`workers_dev` 기본값** (8~10 fact-checker) — `routes`가 있으면 기본 `false`(Wrangler 설정 문서 2026-10-02). 9장은 "명시적으로 끄고 `preview_urls`도 확인"으로 서술. 2·3·12·13장·부록 B의 `workers.dev` 서술(예: "기본으로 켜져 있다")이 이와 모순되지 않게 맞춘다.
15. **10장 Access API** — 신원은 `await ctx.access.getIdentity()`, AUD는 `ctx.access.aud`. `moim-web`(정적 자산 Worker)·Service binding에는 전달되지 않음(문서 원문 확인). 다른 장의 `ctx.access` 언급과 일치 확인.
