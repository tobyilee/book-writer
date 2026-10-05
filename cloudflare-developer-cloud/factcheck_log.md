
## 05장 (라운드 1)

### ❌ 정정
- 레거시 경로 배포 명령 `npx wrangler deploy` (사실 확인 필요) → `npm run deploy` = `vinext-cloudflare deploy --config dist/server/wrangler.json`(Vite 빌드 후 빌드 산출 `dist/server/wrangler.json`으로 Wrangler 배포), `build` = `vite build` — 근거: vinext `packages/vinext/src/init.ts`(레거시 분기 스크립트 생성), `packages/cloudflare/src/deploy.ts`(헤더 "Runs the Vite build / Deploys to Cloudflare Workers via Wrangler", `cloudflare.config.ts` 없으면 wrangler 사용) — GitHub main 2026-10-03 조회, `vinext@1.0.1` 태그의 `init.ts`에서도 동일 문자열 확인. Vite 빌드 시 플러그인이 `.wrangler/deploy/config.json` 리다이렉트를 쓰므로(deploy.ts 주석) Workers Builds 기본 명령 서술은 유지. 루트 `wrangler.jsonc`에 직접 `wrangler deploy`하는 것이 아님을 본문에 명시. Workers Builds 문단의 배포 명령도 `npm run deploy`로 맞추고 "운영 브랜치는 배포 명령(기본값 `wrangler deploy`)"으로 정정.
- `wrangler.jsonc`의 `"main"`·`"assets"` 자리표시 주석 (사실 확인 필요) → 실제 생성값 `"main": "vinext/server/fetch-handler"`, `"assets": { "directory": "dist/client", "not_found_handling": "none", "binding": "ASSETS" }` 기입 — 근거: vinext `init-cloudflare.ts` `generateWranglerConfig()`/`resolveWorkerEntry()` (main 2026-10-03 조회).
- "Wrangler 쪽에서는 [`nodejs_compat`을] 따로 적지 않는다" → 레거시 init이 만드는 `wrangler.jsonc`에도 `compatibility_flags: ["nodejs_compat"]`가 들어가며, 책 예제에서 생략하는 이유(호환성 날짜 2026-08-04+ 기본 ON)로 표현 정정 — 근거: 같은 `generateWranglerConfig()`, 01_reference §0-13.
- OpenNext 지원표가 "`"use cache"`와 Cache Components"를 Supported로 적는다 → 표의 실제 항목은 `"use cache"`(Composable Caching)·PPR, "Next.js 실험 기능" 단서 — 근거: research/web_gaps.md §1-7, 01_reference §3-2 (OpenNext 가이드 2026-08-25).

### ✅ (사실 확인 필요) 해소 — 확인
- Service binding `"services": [{ "binding": "API", "service": "moim-api" }]` — Wrangler configuration 레퍼런스(2026-10-02) 예시와 일치. 주석 제거.
- `"placement": { "mode": "smart" }` — Placement 문서·Wrangler 레퍼런스(2026-10-02)와 일치. "all Workers plans", "up to 15 minutes"도 일치. 주석 제거.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (없음 — vinext·OpenNext·`cf` 관련 서술은 저술가가 이미 날짜를 명기)

### ✅ 확인 (요약)
- OpenNext 이슈 #972/#1049/#1157/#653/#1214 날짜·댓글 수·인용, r/nextjs 5~10KB→약 500KB 및 "build with a better tool…", HN orliesaurus 인용 — research/community.md 패턴 3과 일치.
- vinext: 1.0.0(2026-09-28)·1.0.1(10-01), 가이드 인용 2건·"vinext is in beta"(2026-08-25), 99%·nightly e2e, README 상태 문구·`"use cache"` 부분 구현·이미지 요청 시점 최적화, README 인용(cf 기본·레거시 플래그), PR #3504(2026-09-27 병합), 레거시 시 Vite 플러그인 v1, init 중단 에러 메시지, `cloudflare.config.ts` 골격(재구성 표기 유지), `cf` CLI 인용·`cf migrate`·`npx @vinext/cloudflare deploy`, `create-vinext-app` 스크립트명, `cloudflare:workers`의 `env`, `MemoryCacheHandler`·`kvDataAdapter()`·`workersCacheCdnAdapter()` — research/web_gaps.md §1, 01_reference §0-5·§3-2·§3-11과 일치.
- vinext 반응(thawab·slopinthebag 인용, Vercel 측 취약점 공개, 1.0 이후 후기 부재) — 01_reference §3-2·논쟁 E.
- 가격: Workers 요청 Free 100,000/일(00:00 UTC)·Paid 1,000만/월·$0.30/100만, 정적 자산 무료·무제한, Service binding 추가 요청 요금 없음(CPU 합산), Workers Cache 과금 함정 — 01_reference §2-1·§2-5.
- 같은 존 전역 `fetch()` 실패, `@cloudflare/vite-plugin` React Router v8·TanStack Start SSR(2026-09-30), workerd 로컬 실행 — 01_reference §3-1·§3-2.
- 2026-05-07 변경 기록의 패치 버전(React 19.0.6/19.1.7/19.2.6, Next.js 15.5.16/16.2.5)·vinext 비취약·WAF 인용 — 01_reference §3-2.
- 다모앙 일화(2025-12-13, LA 라우팅, 10~20%, Argo 도메인당 $5) — 01_reference §3-2 (일화 표기 유지).
- Workers Builds 기본 Node.js 24.18.0(2026-07-30), 비운영 브랜치 `wrangler versions upload`, Worker Previews(2026-09-22) 인용 2건·Wrangler 4.135.0+ `wrangler preview` — 01_reference §3-9·§3-11, web_gaps §3-3.

### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- "`sudo cloudflared service install`을 실행하면" → "`sudo cloudflared service install <토큰>`" — 원격 관리 터널의 서비스 설치는 토큰 인자를 받아 `ExecStart … run --token <TOKEN VALUE>`를 만든다. 근거: 01_reference §3-10(운영).
- `server.forward-headers-strategy` "이 역할을 한다" (사실 확인 필요) → 값까지 명시: 지원 클라우드 플랫폼이 아니면 기본 `NONE`, `X-Forwarded-For`/`X-Forwarded-Proto`에는 `native`로 충분 — 근거: Spring Boot 4.1.1 how-to "Running Behind a Front-end Proxy Server"(docs.spring.io/spring-boot/how-to/webserver.html, 2026-10-03 조회), Application Properties 부록.

### ✅ (사실 확인 필요) 해소 — 확인
- 로컬 관리 터널 ingress 마지막 규칙 `service: http_status:404` — Cloudflare One "Configuration file" 문서: "Configuration files that contain ingress rules must always include a catch-all rule"·"The last ingress rule must be a catch-all rule"(2026-10-03 조회). 주석을 "catch-all 필수"로 교체.
- `CF-Connecting-IP` — Fundamentals HTTP headers(2026-05-05): "provides the client IP address connecting to Cloudflare to the origin web server." 주석 제거.
- `server.address` — Spring Boot 4.1.1 Application Properties: "Network address to which the server should bind." `server.address=127.0.0.1`로 값 명시.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (없음 — Tunnel·Quick Tunnels·cloudflared 버전 서술에 날짜가 이미 붙어 있음)

### ✅ 확인 (요약)
- Quick Tunnels: 계정·도메인 불필요, 200 in-flight·429, SSE 미지원, 운영엔 정식 Tunnel(2026-09-30); Protected Quick Tunnels `--allowed-mail`·OTP·용도 문구(2026-10-02); "신기능 아님"(HN 2026-09-18, 844점, noname120 2021 아카이브) — 01_reference §3-10·C-39, community.md 패턴 5.
- `wrangler tunnel quick-start`, `t`/`t+Enter` — 01_reference §3-10.
- Tunnel: 연결 4개·데이터센터 2곳, "Available on all plans"(2026-09-11), 원격 관리 권장·로컬 관리 용도·토큰 경고 인용, Networking > Tunnels·`POST /accounts/$ACCOUNT_ID/cfd_tunnel`·`"config_src": "cloudflare"`·"Published application", `/tunnel/` 독립(Changelog 2026-02-20), `--token-file`↔`TUNNEL_TOKEN_FILE`·`--token`↔`TUNNEL_TOKEN`, 로컬 관리 명령 순서·`credentials-file`, `cfargotunnel.com` CNAME·amluto 인용 — 01_reference §0-4·§3-10.
- Docker 이미지 `cloudflare/cloudflared`, K8s `replicas: 2`·명령줄, replica 25개(연결 100개), 오토스케일링 비권장 인용, "replica는 HA용" — 01_reference §3-10·C-7.
- Free 존 요청 본문 100 MB·413(Workers Limits 2026-09-05), sylens 인용 — C-17. 대용량·비디오 약관 FAQ 인용 — §2-5 #8·C-18.
- cloudflared #491(2021-10, 66댓글, open), lmtr0·ShadiestGoat 우회·경고 — community.md 패턴 5.
- 논쟁: AnonyMD(2026-04-08), jchw TLS 종단 인용, Fränkel(Java Champion, 2026-01-11) 이주 사유·인용, ngrok 창업자(2026-09-18, 이해관계자 표기) — 01_reference 논쟁 C, community.md.
- 운영: 7844 UDP/TCP, 2026.5.2 사전 점검·조기 종료(2026-05-27), 1년 지원, 최신 2026.9.3(2026-09-24), Windows 자동 업데이트 없음, `proxy-dns` 제거(2026-02-02~)→Cloudflare One Client·Mesh node, 2027년 32비트 Windows·Intel macOS 빌드 중단(2026-09-18 공지) — 01_reference §0-2·§0-9·§3-10·§8.
- 참고: 그림 1의 "데이터센터당 아웃바운드 연결 2개" 분배는 문서가 "two data centers에 four connections"까지만 말하므로 도식상 근사로 둔다(본문은 문서 표현 그대로).

### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- `container.start({ env: {...} })` (사실 확인 필요) → `start({ enableInternet: true, env: {...} })` — DO Container API(2026-09-30): "`enableInternet` (`boolean`, required): … Required when you pass `options`." 기본 정책에서 `options`는 선택이고 `env`(`Record<string,string>`)는 허용되나, 옵션 객체를 넘기면 `enableInternet`이 필수. Neon·R2로 나가야 하므로 `true`. 원문 코드는 이 필드 없이는 시작이 거부될 수 있었음.
- `container.setInactivityTimeout(…)` → `await container.setInactivityTimeout(…)` — 시그니처 `setInactivityTimeout(durationMs): Promise<void>` (같은 문서).
- `durable_object` 정책 설명: "그 정책은 Cloudflare 관리 레지스트리의 digest 고정 이미지만 받는다" → 베타임을 명시하고, 이미지는 digest 고정 관리 레지스트리 참조 또는 Wrangler가 빌드·푸시하는 이름 붙은 이미지(`images.<name>.dockerfile`)로 받으며 설정의 `image`·`instance_type`·`max_instances`를 거부한다고 정정. 기본 정책은 이미지·인스턴스 크기를 Wrangler 설정에서 가져온다(`start()` 무옵션 호출 가능). 근거: Wrangler configuration 레퍼런스 "`durable_object` scheduling policy"(2026-10-02: "The `durable_object` policy is in beta… Wrangler rejects every other Container application field for this policy, including `image`, `instance_type`, `max_instances`"), DO Container API `start()`(2026-09-30). **저술가의 설계 판단(기본 정책 + `./Dockerfile` + 설정 파일 `instance_type`)은 유지된다 — 오히려 근거가 강해짐: durable_object 정책을 쓰면 최소 안전장치 2번의 `max_instances`를 쓸 수 없다.** 본문에 이 이유를 한 문장 추가.
- "`start()`의 기본 인스턴스는 `lite`" → "지정하지 않으면 기본 인스턴스는 `lite`(설정 파일 `instance_type`도, durable_object 정책의 `start()`도 기본 `lite`)" — 기본 정책에서는 `start()`가 크기를 받지 않으므로 표현 정정. 근거: Wrangler 레퍼런스 `instance_type` "The default is `"lite"`", DO Container API.
- "Spring 쪽에 `server.shutdown=graceful`을 켜두면" → Spring Boot 4.1에서는 `server.shutdown` 기본값이 이미 `graceful`; 실제 함정은 `spring.lifecycle.timeout-per-shutdown-phase` 기본 30초(긴 리포트는 늘려야 함) — 근거: Spring Boot 4.1.1 Application Properties(docs.spring.io, 2026-10-03 조회: `server.shutdown` 기본 `graceful`, `timeout-per-shutdown-phase` 기본 `30s`).
- Queues HTTP pull 본문 처리: `settlements.apply(m.id(), m.body())` → 본문 base64 디코드 후 처리 — Pull consumers(2026-07-01) "Content types": "For both the `json` and `bytes` content types, … they will be base64-encoded… Your consumer will need to decode the `json` and `bytes` types". 디코드 줄 추가.
- 멱등 키 "메시지 ID로" → "본문의 업무 값(이벤트 종류·행사·회원·시각)" — 같은 문서가 `id`를 "a unique, read-only ephemeral identifier"로 설명하므로 재전달 간 동일성 보장을 기대하기 어렵다고 명시.

### ✅ (사실 확인 필요) 해소 — 확인
- `containers[].instance_type: "standard-1"` — Wrangler 레퍼런스(2026-10-02) 기본 정책 필드, 값 목록 `lite`/`basic`/`standard-1~4`, 기본 `lite`. 주석을 "생략하면 lite(256 MiB)"로 교체.
- `ctx.container.running` — DO Container API: "`running` is `true` when the container is running. It does not confirm that the container is ready." 주석을 그 의미로 교체.
- `env` 전달 형태 — `env` (`Record<string, string>`, optional) 확인(위 ❌의 `enableInternet` 보정과 함께).
- `send(…, { contentType: "json" })` — JS API(QueuesContentType 기본 `json`, 2024-03-18 이후 compat date), Pull consumers "Pull-based consumers cannot decode the `v8` content type". 주석을 "기본값이지만 명시, v8 불가"로 교체.
- `npx wrangler queues consumer http add <queue>` — Pull consumers 문서 명령 일치. 기존 Worker 소비자가 있으면 먼저 제거해야 한다는 단서 추가.
- `POST /accounts/{account_id}/queues/{queue_id}/messages/pull`·`/messages/ack`, 요청 `{ visibility_timeout_ms, batch_size }`, ack `{ acks: [{ lease_id }] }`, 응답 `result.messages[]`의 `id`·`body`·`lease_id`, 가시성 최대 12시간 — Pull consumers(2026-07-01) 일치. 주석 3곳 제거, 응답 형태 주석으로 교체.
- `env.HYPERDRIVE.connectionString` — Hyperdrive Get started 예제(`new Client({ connectionString: env.HYPERDRIVE.connectionString })`) 일치. 주석 제거.

### ⚠️ 약화·삭제
- 빈 큐 폴링 과금 (사실 확인 필요) → "operation은 메시지 단위로 센다. 빈 pull은 빈 응답이 즉시 오는데(long polling 없음) 이를 따로 과금하는지는 가격 문서에 적혀 있지 않다(2026-10 조회) — 대시보드 사용량으로 직접 확인" — Queues Pricing(2026-04-21) "Operations are per message, not per batch", Pull consumers "short polling". 과금/무과금 어느 쪽도 단정하지 않음.
- Containers FAQ "프리뷰 URL이 생성되지 않는다" ↔ 5장 Worker Previews 블로그(2026-09-22) "Containers … separate … instances for every Preview": 문장을 "Workers Builds가 버전마다 만드는 프리뷰 URL"로 한정하고, 브랜치별 Worker Preview는 별개 기능이라 발표됐다는 점과 직접 확인 권고를 병기. **편집자 참고:** 두 1차 출처가 나란히 존재 — 5장·7장·13장의 프리뷰 서술이 서로 모순돼 읽히지 않는지 통합 시 확인.

### 🕒 신선도
- `durable_object` 스케줄링 정책 → "(2026-10 기준 베타)" 추가(71행, 166행).

### ✅ 확인 (요약)
- Containers GA 2026-04-13·인용, Workers Paid 전용, linux/amd64 인용, 인스턴스 타입 표(Limits 2026-09-30), 과금 FAQ 인용, 단가·포함량·이그레스(한국 $0.05/GB·500 GB, Pricing 2026-08-28), 콜드 스타트 1~3초 인용·"6배"는 블로그 주장 표기(C-16), 내장 오토스케일링 없음, 교차 테넌트 취약점(2026-09) — 01_reference §2-1·§3-4.
- 커뮤니티 인용(rozenmd, NicoJuicy, youngbum/walla.my 2026-05, detuks 원문 오타), sliplane $82.44(이해관계자 표기) — community.md 패턴 8.
- 최소 안전장치: `limits.cpu_ms`·`subrequests` 예시, `cpu_ms` 기본 30,000·최대 300,000, 계정 하드캡 없음(C-23), Budget alerts $10 기본(2026-07, C-14)·정보 제공용·하루 지연·기본료 제외 — 01_reference §2-3.
- 공식 예제 Go·Node·Python뿐·JVM 0건, Spring Boot 4.1.1(2026-08-20)·Java 17+, OOM 재시작·스왑 없음, SIGTERM→최대 15분→SIGKILL, `exports`/`migrations` 병용 금지, DO Container API 권장 문구, 포트 준비 별도 확인, `setInactivityTimeout` 범위(0 초과·최대 6시간), `Container` 클래스 `defaultPort`·`sleepAfter`·`startAndWaitForPorts()`, Workers Builds 운영 브랜치 `wrangler deploy` 필요 — web_gaps §2·§3, DO Container API(2026-09-30).
- 비용 계산표: 메모리 $25.70, 디스크 $1.40, CPU 10% $2.14 / 100% $25.47, 합계 $34.24 / $57.57, 배치 3,600 GiB-초(포함량 4%)·매일 시 초과 18,000 GiB-초 ≈ $0.05 — 단가(§2-1)로 재계산해 일치.
- Placement Hints `aws:us-east-1`(2026-01-22), Hyperdrive 생성 명령·바인딩, kentonv 인용(이해관계자), 원본 연결 Free ~20/Paid ~100, 트랜잭션 모드·`RESET`·비지원 기능·직접 연결 권고, 가격(무료·Free 10만 쿼리/일·설정 10/25·60초) — 01_reference §2-1·§3-3·§3-9, web_gaps §4-3.
- Queues 3 operations·Free 10,000/일·Paid 100만/월·$0.40/100만·64 KB 단위, 토큰 권한 2종 — 01_reference §2-1·§3-3.
- R2 Java v2: 엔드포인트·`pathStyleAccessEnabled`·`chunkedEncodingEnabled(false)` 인용(2026-04-21)·`Region.of("auto")`·`auto` 별칭, SDK 2.30.0 CRC32 기본·`WHEN_REQUIRED`는 미확인 처방으로 표기 유지(G-10), `S3Presigner` — web_gaps §4-5.
- Workers VPC 베타 무료·2026-04-29 Hyperdrive 사설 DB 권장, 인바운드 TCP·gRPC 비공개 베타(2026-08-03) — 01_reference §3-4·§3-9.

### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- "캐시가 비어 있는 첫 순간에 Worker는 한 번만 깨어난다" → "데이터센터마다 한 번씩만" — 근거: Workers Cache 문서(2026-09-22) "Collapsing is per cache key, per data center."
- Cache API 한계 인용 묶음의 출처 "(Workers Cache API 문서)" → "(Cache API·Workers Cache 문서)" — "does not collapse concurrent requests" 문장은 Workers Cache 문서의 것
- (확인 필요) `CDN-Cache-Control` 해석 → "존 캐시는 지원, 헤더가 오면 엣지 캐싱 판단은 이것으로, Cache Rules Edge Cache TTL이 우선" — 근거: https://developers.cloudflare.com/cache/concepts/cdn-cache-control/ (2026-04-16)
- (확인 필요) `invalidate_cache` 본문 → "퍼지와 같은 형식(`{"tags":[...]}` 등), 존 캐시 전용이라 Workers Cache에는 닿지 않음" — 근거: https://developers.cloudflare.com/cache/guides/invalidate-cache/ (2026-09-29) "The request body uses the same format as the corresponding purge request" / "Invalidation from the dashboard or the `invalidate_cache` endpoint does not affect Workers Cache."
- (확인 필요) Workers Cache 태그 부착 → "`Cache-Tag: event-42` 헤더, 쉼표 구분" — 근거: https://developers.cloudflare.com/workers/cache/purge/ (2026-08-20) "The `Cache-Tag` header value is a comma-separated list of tags."
- (확인 필요) Cache Rules 캐시 키 플랜 범위 → "쿼리 파라미터를 골라 넣고 빼는 설정은 Enterprise 전용" — 근거: https://developers.cloudflare.com/cache/how-to/cache-rules/settings/ (2026-09-16) "Enterprise customers have these additional options for custom Cache Keys"

### ⚠️ 약화·삭제
- (확인 필요) Free 계정에서 Workers Cache 켤 때 정적 자산의 일일 10만 한도 반영 → "문서에 없으니(2026-10-03 확인) Free라면 켜지 않는 편이 안전" — 가격 문서·Workers Cache 문서·Limits 모두 과금 단가만 명시, 일일 한도 집계 방식 미기재
- Spring `CDN-Cache-Control` 예제 앞에 "HTML이니 Cache Rules로 캐시 대상에 넣어 뒀다고 하자" 전제 추가 — 앞 절의 "HTML 기본 DYNAMIC"과 정합, 헤더만으로 HTML이 엣지 캐시된다는 오독 방지

### 🕒 신선도
- (없음 — 가격·한도 문장에 이미 기준일 표기)

### ✅ 확인 (요약)
- 구조 전제 "Worker가 만든 응답은 존 캐시를 거치지 않고, 존 캐시는 `fetch()` 서브요청 쪽" — Workers Pricing Fine Print "Since Cloudflare Workers runs before the Cloudflare cache…", How the cache works(2026-07-06) "Cloudflare Workers run before the cache"·"interact with a zone's Cloudflare Cache… Cache API or `fetch()`"와 일치
- Workers Cache: 설정 키, 존 설정 미적용, RFC 9111, tiered 기본, 요청 병합, `ctx.cache.purge({tags})`, 과금 원문(HIT·정적 자산·worker-to-worker 표준 단가), Service binding 호출 과금 전환 — Workers Cache 문서(2026-09-22)와 일치
- 가격 $0.30/100만·1,000만 포함, 계산 45,000→585,000, 퍼지 한도 Free 5회/분·800 URLs/초(계정 단위), Cache Rules Free 10, Tiered Cache Free 포함, Cache Reserve 단가·2026-09-28 강제 MISS, SWR 비동기(2026-02-26), invalidate 원문(2026-09-28), Cache Response Rules(2026-03-24), `cf` 옵션·`cf.vary`(2026-06-28) — 01_reference §2-2·§3-8, web.md 8-1~8-3
- RFC 9111/9213(2022-06)·5861(2010-05), Maggs & Sitaraman 74% 인용(CCR 45(3) 2015), Yang 외 SOSP '23 — papers.md 논문 8·9·표준 1과 일치. S3-FIFO 채택 주장 없음(C-34 준수)
- vinext `"use cache"` Known gaps·블로그 "limited support", 캐시 어댑터 이름 — web_gaps.md §1, web.md 4-2
- HN Manchitsanan·mhitza 인용 — community.md와 일치
- `(사실 확인 필요)` 5건 모두 해소

### 미해소
- (없음)

## 01장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "2026년 한 해에만 Pages가 Workers로 수렴하고" → "최근 몇 년 사이 Pages가 Workers로 수렴했고, 2026년에만 WARP Client가…·Browser Rendering이… 이름을 바꿨다" — Pages→Workers 투자 전환은 2025년 이전부터(Bryce Wray 2025-05-27 인용, 01_reference §3-1). 2026년 귀속은 개명 2건(§0-2, C-12)만 유지.
- 그림 2 microVM 칸 주석 "Firecracker 부팅 125ms 미만"(Containers 노드에 연결) → "VM 단위 격리" — 논문의 Firecracker 부팅값이 Containers 콜드 스타트로 읽힐 위험. 공식 Containers 콜드 스타트는 "often be in the 1-3 second range"(C-16). 본문의 논문 수치 서술은 그대로 유지.
### 🕒 신선도
- (없음 — 가격·한도·상태 서술은 이미 "{문서} {날짜} 기준" 표기)
### (사실 확인 필요) 해소
- "Containers가 Firecracker VM 위에서 동작" → ✅ 원문 확인 후 직접 인용으로 교체: "Each container lives inside a dedicated virtual machine powered by the Firecracker virtual machine monitor." — https://blog.cloudflare.com/containers-cross-tenant-vulnerability/ (2026-09-24), 웹 조회 2026-10-03.
### ✅ 확인 (요약)
- 상태·날짜 5건: Containers GA 2026-04-13, Python Workers GA 2026-09-21, Workers 1급 언어 4종(Workers 언어 문서 2026-07-03), Containers Paid 전용, Mesh node(구 WARP Connector) — 01_reference §0·§1-1.
- 가격·한도 6건: Workers Paid 월 최소 $5·존 플랜과 별개(원문 인용 일치), Free 100,000/일·00:00 UTC·CPU 10 ms·Error 1027, Paid 1,000만 요청·$0.30/100만, 정적 자산 무료·무제한, R2 초과분 과금(§2-4 권장 표현), 하드캡 부재(C-23) — §2.
- 논문 인용 6건: New Kids 초록 인용·7개 플랫폼·3,800만 회(arXiv:2604.15916 — arxiv.org에서 제목·저자·v1 2026-04-17/v2 2026-08-14·"seven platforms"·"more than 38 million function calls" 직접 확인), Firecracker 5MB/125ms/150개·§2.1.2 인용 2건, Shahrad 45%/81%·8자릿수·20% 미만→99.6% — papers.md 원문 등급.
- WASI 실험적·스레드 불가 — WebAssembly 문서(2026-04-23).
### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- "`api.moim.example.com`처럼 두 단계로 내려가면 별도 인증서가 필요해질 수 있으니" (커스텀 도메인 문맥) → "커스텀 도메인은 여러 단계 서브도메인에도 인증서(Advanced Certificate)를 자동으로 만들어주지만, 3장의 라우트나 6장의 Tunnel처럼 일반 DNS 레코드 위에 서는 호스트는 Universal SSL 범위에 기댄다" — 근거: Workers Custom Domains 문서(2026-09-29) "This includes multi-level subdomains such as `realms.app.example.com`" (Advanced Certificate 자동 발급). 한 단계 서브도메인·`/api/*` 설계 결론은 유지(02_plan 표기 규칙과 일치).
### ⚠️ 약화·삭제
- "같은 공식 입장에 이런 단서가 붙어 있다"(Pages 문서와 같은 출처처럼 읽힘) → "개발자 Bryce Wray가 블로그에 옮겨 적은 Cloudflare의 입장에는" — 인용문은 Pages 문서(2026-08-25 조회)에 없음, 01_reference §3-1·community.md에서 "Bryce Wray 인용"으로만 확보.
### 🕒 신선도
- Vite 플러그인 `assets.directory` 자동 채움 서술에 "(Vite 플러그인 문서 2026-08-18 기준)" 추가.
- Universal SSL 범위 서술에 "(Universal SSL 문서 2026-04-30 기준)" 추가.
### (사실 확인 필요) 해소 — 4건
- `assets.directory` 키 → ✅ Wrangler 설정 문서(2026-10-02) `"assets": { "directory": "./public", ... }`. 메타 문장 삭제.
- Vite 플러그인 import·연동 → ✅ `import { cloudflare } from "@cloudflare/vite-plugin"`(npm 1.62.5 타입 정의 export 확인), "The `assets.directory` field in this file is automatically populated with the path to your `client` build output."(Vite plugin Static Assets 문서 2026-08-18) — 원문 인용으로 교체.
- `routes`/`custom_domain` 키 → ✅ Wrangler 설정 문서(2026-10-02)·Custom Domains 문서(2026-09-29) `pattern` + `custom_domain = true`. 메타 문장 삭제.
- Universal SSL 루트+1단계 → ✅ "coverage is limited to the root domain … and first-level subdomains"(Universal SSL Limitations 2026-04-30). 단 커스텀 도메인 문맥의 귀결은 위 ❌로 정정.
### ✅ 확인 (요약)
- 커뮤니티 4건: Reddit "Help me understand Workers vs Pages…"(2026-03 무렵, 최다 28점 u/jekadotorg 인용), "moving away from Pages", Bryce Wray 2025-05 "no walk in the park", aperture147 2025-10-15 인용 — community.md.
- 문서 인용 7건: "Start new projects with Workers."(Pages 문서 2026-08-25, 조회로 재확인), Workers Sites v4 폐기·Vite 미지원·"Do not use…"(2026-04-23), 마이그레이션 가이드 인용 2건, `wrangler.jsonc` 권장, "installed locally", React 가이드 SPA 인용 — web.md.
- 버전·한도 7건: C3 2.73.2, vite-plugin 1.62.5, Wrangler 4.147.0, 4.68.0 자동 구성(Changelog 2026-02-25), Vite 플러그인 시 설정 선택 사항(2025-12-08), 정적 자산 파일 수 20,000/100,000(4.34.0+)·25 MiB, `run_worker_first` 429, Workers Cache 과금 — §2-1·§8.
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- (확인 필요) 계정 분리 시 바인딩 → "Service binding으로 두 계정을 묶을 수 없다, 대상 Worker는 'must be on your Cloudflare account'" — 근거: https://developers.cloudflare.com/workers/runtime-apis/bindings/service-bindings/ (2026-08-18)

### ⚠️ 약화·삭제
- (확인 필요) Service binding 호출의 Free 일일 한도 집계 → "추가 요청 요금 없음, 가격 문서는 처음 불린 Worker의 요청 1건으로 셈. Free 일일 한도도 같은지는 문서에 없음" — Workers Pricing(2026-10-02) Service bindings 절 "billed as: One request (for the initial invocation of Worker A)". 일일 한도 집계는 Limits·Service bindings 문서 모두 미기재
- (확인 필요) 오리진 없는 Worker의 fail open → 문서 원문 "Requests behave as if no Worker is configured." 인용 + "받아줄 오리진이 없으면 사용자를 구해주지 못한다" — Workers Limits(2026-09-05) Daily requests 표. fail 모드는 라우트 토글로만 문서화(커스텀 도메인 Worker는 "treated as an origin")

### 🕒 신선도
- (없음 — 한도 문장에 기준일 표기됨)

### ✅ 확인 (요약)
- Free 한도: Workers 10만/일(00:00 UTC=KST 09:00)·1027·CPU 10 ms·1102, KV 10만/1,000, D1 500만/10만·2026-09-01 실패+이메일·에러 문구, DO 10만, Queues 1만 ops·3 ops/메시지 원문·2026-02-04 Free 포함, Workflows 3,000 steps·저장 1 GB, Hyperdrive 10만, Workers AI 10,000 Neurons, Images 9422·"You will not be charged", Observability 0.5 GB/일 수집 중단(2026-12-01~), Workers Logs 20만/3일, 위젯 "current day on Free plans", 정적 자산 20,000파일·25 MiB, Turnstile·Tunnel·Access 50명·Cron 5·Email Routing, AE "Currently, you will not be billed" — 01_reference §2-1·§2-2·§2-3
- R2 "초과분 과금"을 권장 표현 그대로 사용(§2-4, C-37), 401 비과금·삭제 무료 — 일치
- Paid 포함량(1,000만 요청·D1 250억 행·DO 100만·Queues 100만)·$5 최소 — 일치
- 시나리오 산술(121,800·약 5만 PV·3,000만·250 PV·12억·3,030·1,530·5,400·약 3,300건) — 재계산 일치
- Shahrad et al. 45%/81% 인용·99.6% — papers.md 일치. simonw·helloacm($48, 1억 634만, Free 플랜 이전 대응)·eliasoliedev·neya·kugelblitz·Shakahs·$120k 카지노 맥락 — community.md 일치
- 계정 단위 하드캡 관련 서술 없음(13장으로 넘김), Free "청구 대신 에러"에서 R2 예외 명시 — 기준 준수
- `(사실 확인 필요)` 3건 모두 해소

### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- 테스트 코드 `import { SELF } from "cloudflare:test"` + `SELF.fetch(...)` → `import { exports } from "cloudflare:workers"` + `exports.default.fetch(...)` — 근거: Vitest 통합 "Migrate from Vitest 3 to Vitest 4" 가이드(2026-08-20) "The `env` and `SELF` exports from `cloudflare:test` are deprecated in favor of `cloudflare:workers`." / "The deprecated exports still work, so this change is recommended rather than required." / "`exports.default.fetch()` behaves the same as `SELF.fetch()`, except that it does not expose Assets." 및 Write your first test(2026-08-20)의 예제. 본문에 deprecated·Assets 차이 서술 추가. (ch5–14 초고에 `SELF` 사용 없음 — grep 확인)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- `ctx.waitUntil()`에 "HTTP 요청이라면 응답을 보낸 뒤 최대 30초, Context 문서 2026-09-28 기준" 추가 — "For HTTP-triggered Workers, `ctx.waitUntil()` can extend execution for up to 30 seconds after the response is sent or the client disconnects."
### (사실 확인 필요) 해소 — 7건
- `ctx.waitUntil()` → ✅ Context 문서(2026-09-28). 위 🕒 반영.
- Spectre 타이머·멀티스레딩 → ✅ Kenton Varda, "Spectre research with TU Graz"(Cloudflare Blog 2021-10-12): Workers 런타임은 "designed to prevent a Worker from measuring its own execution time", "other forms of non-deterministic behavior like multithreading that could be used in place of a timer"를 막음 — 출처 귀속 문장으로 교체(세부 메커니즘 단정은 피함).
- Hono 시그니처 → ✅ `c.req.param()`·`c.req.json()`(hono.dev Request 문서), `json<T = any>(): Promise<T>`(hono npm 타입 정의), `c.json(obj, status)`, `export default app`. 메타 문장 삭제.
- `main`·`routes`·`zone_name` → ✅ Wrangler 설정 문서(2026-10-02) `"main"`, `"routes": [{ "pattern", "zone_name", "custom_domain" }]`. 메타 문장 삭제.
- **커스텀 도메인 vs 라우트 우선순위 (구조 점검) → ✅ 설계 그대로 동작.** Custom Domains 문서(2026-09-29): "A Worker running on a Custom Domain is treated as an origin. Any Workers running on routes before your Custom Domain can optionally call the Worker registered on your Custom Domain by issuing `fetch(request)`." → `moim.example.com/api/*` 라우트의 `moim-api`가 커스텀 도메인 `moim-web`보다 먼저 실행되고, `fetch(request)`로 넘기지 않으면 그대로 응답. 그 외 경로는 `moim-web`. 본문을 이 설명+원문 인용으로 교체. 참고: 이 "라우트→커스텀 도메인 `fetch(request)`"는 문서화된 경로이고, 같은 문단 뒤의 "같은 존 Worker를 전역 `fetch()`로 부르면 실패"(Workers Limits)는 반대 방향(`moim-web` 코드 → `moim-api` URL) 서술이라 충돌하지 않음.
- `wrangler dev` → ✅ Wrangler 명령. 메타 문장 삭제.
- vitest `SELF`/`cloudflare:test` → ❌ 위 정정.
### ✅ 확인 (요약)
- 런타임 인용 4건: "Threading is not possible in Workers. Each Worker runs in a single thread, and the Web Worker API is not supported."(WebAssembly 문서 2026-04-23 원문 조회로 뒷부분까지 확인), WASI 실험적, Node.js 호환 기본 ON(2026-08-04+)·폴리필 shim 인용·끄기 플래그(Node.js 문서 2026-08-12), Service binding 인용 — web.md.
- 한도 표 8행: CPU 10 ms/30초·최대 5분, 128 MB 공유, 서브리퀘스트 50/1,000·10,000/최대 1,000만, 동시 연결 6개(Changelog 2026-04-09 인용 2건), 시작 1초(2025-10), 64 MiB(2026-09-04), 100,000/일, Error 1102/1027 — §2-1·C-13·C-15.
- 비용 메모 2건: Workers Paid 포함량·단가, Workers Logs 현행·Observability 2026-12-01 전환(§2-1, §9 🕒 표기 유지).
- 도구 6건: Wrangler 4.147.0, `wrangler types --check`(2026-01), remote bindings GA 2025-09·인용, vitest-plugin 1.3.6(npm 확인)·개명 인용·codemod·`@msw/cloudflare`, Miniflare 5.x 알파, `cf` CLI 베타 2026-09-28·인용·약 280개 작업·`cf migrate`.
- 논문 2건: Firecracker §2.1.2 인용, Schwarzl et al. ESORICS 2022 저자 순서(C-33)·분당 2비트·DyPrIs 0.61% 초록 인용 — papers.md.
- 기타: ECMA-429 2025-12 1판(C-31 권장 범위), Kotlin/Wasm Beta(C-8), TeaVM 2024-08 인용, Python Workers GA 2026-09-21·WSGI 2026-09-02.
### 미해소
- (없음)

## 04장 (라운드 1)

### ❌ 정정
- **DO 클래스 선언 `"migrations": [{ "tag": "v1", "new_sqlite_classes": ["EventSeats"] }]` → `"exports": { "EventSeats": { "type": "durable-object", "storage": "sqlite" } }`** — 근거: Wrangler 설정 문서(2026-10-02) "migrations is the legacy imperative configuration for managing Durable Object class lifecycle. For new Workers, prefer the declarative exports field. migrations and Durable Object entries in exports are mutually exclusive." / Changelog "declarative DO class exports"(슬러그 2026-06-30, 게시 2026-07-04, GA) "Existing Workers using the legacy `migrations` array continue to work unchanged." / DO migrations 문서(2026-09-28) "Once a Worker has been deployed with `exports`, subsequent deploys cannot return to the legacy `migrations` array." 본문에 구 표기·레거시 상태·혼용 불가·비가역성 서술 추가. ⚠ 01_reference §0-11은 `exports`를 모름 — **ch7:160(`ReportContainer`)·ch13:217(`UsageMeter`)도 같은 구 표기 사용 → 교차 장 통일 필요(오케스트레이터 보고).**
- kentonv 인용의 맥락: "같은 스레드에서 … kentonv는 [D1의] 설계 의도를 설명했다" → "이 글에 단 답글에서 … 그가 예로 든 것은 Durable Objects로 SQLite 데이터베이스를 수백만 개 만드는 방식이었지만, 생각의 뼈대는 D1에도 그대로 통한다" — 근거: HN item 47696640 원문(parent 47696317 = keeda 글, HN API 조회 2026-10-03) "With Durable Objects[0], you can create and orchestrate millions of sqlite databases … The 10GB limit applies to one database, but …". 원문은 D1이 아니라 DO를 가리킴. 인용문·Hyperdrive 언급은 유지. (01_reference §3-3·논쟁 B도 같은 오귀속 — 다른 장에서 kentonv의 10GB 발언을 D1 설계 의도로 쓰면 같은 정정 필요. ch5–14 초고 grep 결과 해당 사례 없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- KV 전파: "공식 문서의 상한 문구는 재확인이 필요하다(사실 확인 필요)" → KV 문서(How KV works, 2026-04-21) 원문 인용 "Changes may take up to 60 seconds or more to be visible in other global network locations as their cached versions of the data time out." + "60초도 보장된 상한은 아니다" + 부정 조회 캐시("Negative lookups … are also cached") 반영. 결론 문장 "몇 초에서 수십 초까지" → "몇 초에서 1분 넘게까지"(문서의 "or more"에 맞춤). C-25 해소.
- DO 동시성 서술에 "(Rules of Durable Objects 2026-08-20 기준)" 기준일 부여.
### 기계적 수정
- 297행 코드 펜스 닫힘(```) 뒤에 본문이 같은 줄로 붙어 있던 것 → 줄바꿈 분리(렌더링 깨짐 방지, 문장 변경 없음).
### (사실 확인 필요) 해소 — 7건
- 바인딩 설정 키 → ✅ Wrangler 설정 문서(2026-10-02): `d1_databases`(binding·database_name·database_id), `kv_namespaces`(binding·id), `durable_objects.bindings`(name·class_name), `r2_buckets`(binding·bucket_name), `queues.producers`(binding·queue)·`consumers`(queue), `workflows`(name·binding·class_name). `migrations`만 위 ❌ 정정.
- D1 마이그레이션·클라이언트 API → ✅ 기본 `migrations/` 폴더(D1 Migrations 문서 2026-06-08), `wrangler d1 migrations apply`, `--local`/`--remote` 플래그(Wrangler D1 명령 문서 2026-04-23), `prepare().bind().all()/run()`·`all<T>()`(@cloudflare/workers-types `D1PreparedStatement`). 기본 대상(로컬/원격)은 문서에 명시가 없어 단정 대신 "플래그로 대상을 분명히" 서술.
- KV `get<T>(key, "json")` → ✅ workers-types `get<ExpectedValue = unknown>(key, type: "json"): Promise<ExpectedValue | null>`. 메타 문장 삭제.
- KV 전파 상한 → 🕒 위 반영.
- DO SQL·RPC·동시성 → ✅ Rules of DO(2026-08-20): "Input gates block new events (incoming requests, fetch responses) while synchronous JavaScript execution is in progress. Awaiting async operations … opens the input gate" / "Multiple storage writes without intervening `await` calls are automatically batched into a single atomic implicit transaction." / "Public methods are automatically exposed as RPC endpoints". `sql.exec().toArray()/.one()`(workers-types `SqlStorageCursor`). 본문에 근거 서술로 교체.
- R2 `put` 옵션 → ✅ R2 Workers API(2026-07-31) `put(key, value: ReadableStream | …, options?: R2PutOptions)`, `httpMetadata.contentType`. 메타 문장 삭제.
- Queues·Workflows API → ✅ Workflows Workers API(2026-09-28) import 3종 from "cloudflare:workers", `step.do(name, cb)`, `step.sleepUntil(name, timestamp: Date | number)`, `create({ id, params })`; Queues JS API(2026-07-06) `queue(batch, env, ctx)`, `MessageBatch<Body>`, `message.ack()`, `send(body)`. 메타 문장 삭제.
### ✅ 확인 (요약)
- 커뮤니티 6건: Kuryzhev Dev.to 2026-07-01 제목·인용 2건·약 40%(본인 주장 표기 유지), fastball 2025-04, kpozin 2025-04, keeda 2026-04-08(원문 HN API 확인), R2 카드 등록 Reddit(2026-03 무렵, VPS 복귀) — community.md.
- 가격·한도 25건 이상: D1·KV·KV Instant(건당 $0.10, 수만 배 = 약 2만 배로 산술 일치)·DO(128 MB Duration·$0.15·$12.50·Hibernation 인용)·R2(Standard 포함량·단가·IA 제외·단위 올림 인용·401 무과금)·Queues(3 ops 인용·64 KB·10,000/일→약 3,333통)·Workflows(Free/Paid 포함량·단가·"no earlier than August 10, 2026"·보존 7일 C-4·64 MiB C-3)·Free 존 본문 100 MB·413·Budget alerts(C-14) — 01_reference §2·§7.
- 상태·날짜: KV Instant 비공개 베타 2026-10-01(성능 수치 원문 일치), 신규 DO SQLite 전용 2026-07-09, DO 저장 과금 예고(C-5 권장 표현), KV·R2·D1 자동 프로비저닝 2025-10, D1 read replication "2025년"(C-22), D1 Free 한도 강제 2026-09-01.
- 논문 3건: Gaffney et al. PVLDB 2022 인용, Bailis et al. PBS 인용(PBS 수치를 KV에 쓰지 않는 경고 준수), Orleans 인용·"유사한 모델"(C-34 준수).
- presigned URL 인용(Optimize costs 2026-05-04, web.md).
### 미해소
- (없음)

## 13장 (라운드 1)

### ❌ 정정
- (확인 필요) Billable Usage API 응답 필드 `BilledCost` → `ContractedCost` (코드 타입·reduce 수정) — 근거: https://blog.cloudflare.com/billable-usage-api/ (2026-08-03) "ContractedCost — what that period cost" / 응답 예시 `"ContractedCost": 0.75`, `CumulatedContractedCost`. `BilledCost`는 응답에 없음
- (확인 필요) 엔드포인트 자리표시자 → `https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/billable-usage`, 토큰 권한 Billing Read, 기본 응답은 이번 청구 기간 — 같은 블로그 원문 curl·"Grab an API token with the Billing Read permission"
- (확인 필요) 프리뷰에서 DO 바인딩 빼는 문법 → "`previews` 블록에 적은 것만 쓰며 `previews.durable_objects.bindings`를 적지 않으면 DO 바인딩 없음, 클래스·마이그레이션은 최상위" — 근거: https://developers.cloudflare.com/workers/previews/configuration/ (2026-09-22) "Previews do not inherit production settings" / "Add `previews.durable_objects.bindings` only if your code reads the binding from `env`."
- (확인 필요) 요청까지 끊는 API → 라우트 삭제 `DELETE /zones/{zone_id}/workers/routes/{route_id}`, 규칙 수정 `PATCH /{accounts_or_zones}/{id}/rulesets/{ruleset_id}/rules/{rule_id}` 명시 + "Cloudflare가 자동 차단 패턴으로 문서화한 것은 아님" 유지 — 근거: Cloudflare API 레퍼런스(Workers Routes delete, Rulesets Rules edit), 01_reference §2-3 #3 [추론] 경계
- (확인 필요) `script_name` DO 바인딩 + RPC → 확인, 주석을 단정형으로 교체 — 근거: Wrangler configuration "`script_name`… The name of the Worker where the Durable Object is defined, if it is external to this Worker", DO stubs 문서 "compatibility date ≥ 2024-04-03 … prefer RPC" (예제 compatibility_date 2026-09-01)
- "정지 상태에서도 요청은 100만 건당 $0.30씩 계속 과금" → "(포함량을 넘으면 100만 건당 $0.30)" — Paid 1,000만/월 포함

### ⚠️ 약화·삭제
- "지금 같은 사고가 난다면 적어도 하루 늦게라도 알림은 온다" → "예산 알림이 걸려 있는 계정에는" 조건 추가 — 기본 $10 알림은 적격 Pay-as-you-go 계정에 코호트 순차 적용(C-14)
- "Free 계정은 한도에서 멈추지만" → "(R2를 빼면)" 추가 — §2-4, R2는 Free 초과분 과금

### 🕒 신선도
- `max_instances` 상한 문장에 "(베타 `durable_object` 스케줄링 정책은 이 항목을 받지 않는다)" 추가 — 07_final.md·web_gaps.md §3(Containers configuration 2026-09-29)과 정합. 기본 정책에서 `max_instances`가 동시 인스턴스 상한이라는 서술은 유지, 내장 오토스케일링 없음은 §3-4 FAQ 원문과 일치

### ✅ 확인 (요약)
- **계정 단위 하드캡 없음(2026-10 현재)** 서술 — §2-3·C-23과 일치, 출간 직전 재확인 고지 포함. 알림(Budget alerts·Billable Usage·Usage-based billing 이메일·Threshold billing) vs 차단(`limits.*`=호출 단위, WAF·`ratelimit`=유입 트래픽, AI Gateway spend limits=AI Gateway 트래픽 한정) 범위 구분 정확
- Budget alerts 원문 3문장(2026-05-29)·기본 $10·2026-07-20 게시·코호트·Enterprise 제외, Billable Usage 2026-04-21·원문, API 2026-08-03 "updated daily", mathoff, Threshold billing 원문(2026-06-16), `limits.cpu_ms` 원문·30,000/300,000, 2026-02-11 subrequests 원문·10,000 — 01_reference §2-3
- $34,895: 인용 4개·날짜·타임라인·결말 미확인 처리(C-20 준수, 면제 언급 없음). $4,868: 48.3억·$1,411.40·$4,586.64 면제 18일·r/CloudFlare 인용(블로그 경유 표기)·"billing department" 인용, 산술 $4,830 — community.md·§2-5 일치. 한국 사례는 C-27 일반화 표현 준수
- Worker Previews 블로그 인용(2026-09-22), DO Duration 128 MB·Hibernation 원문, DO SQLite 과금 예고 표현(C-5), Queues 64 KB, Workflows "no earlier than August 10, 2026"·$0.80/10만, Observability 원문, Containers 이그레스 한국 $0.05/500 GB, KV Instant $0.10 per operation — §2-1·§2-5·§9 일치
- Little Bear 3단(70/90/100%, KV TTL 1시간, ~30초), Show HN 3mins.news·photobombastic, simonw·jacobmei(2026-04-27)·woodylondon 인용 — community.md 일치
- `(사실 확인 필요)` 5건 모두 해소

### 미해소
- (없음)

## 14장 (라운드 1)

### ❌ 정정
- 베타 지도 "Containers 인바운드 TCP·gRPC" → "Workers 인바운드 TCP(Spectrum)·Containers gRPC" — 근거: 01_reference §3-4(blog 2026-08-03) "connect(socket) — a new handler in the Workers runtime… provided by Spectrum" / "gRPC from Cloudflare Containers". 07_final.md 전망 박스와 정합

### ⚠️ 약화·삭제
- "2026년에만 Pages가 Workers로 수렴했고" → "Pages 문서는 새 프로젝트를 Workers로 시작하라고 안내한다" — §0-6은 Pages 문서(2026-08-25)의 현재 안내만 근거로 함. 수렴 시점이 2026년이라는 근거 없음. WARP→Cloudflare One Client(2026-04-14)·Browser Run(2026년, 월 단정 없음 C-12)은 유지

### 🕒 신선도
- (없음 — 베타 지도 전체에 2026-10-03 기준 표기, Workflows 과금은 "예고"로 §9와 일치)

### ✅ 확인 (요약)
- 장애: 2025-11-18 HN 1465점·916댓글, binarymax "28M 500 errors/sec…", otterley·SerCe·mixedbit(2025-12-05)·lionkor·miki123211(2025-11-24)·vasco 인용, 원인 3건(Bot Management feature file·WAF 전역 설정·BYOIP API), R2 2026-08-08 minraws 인용, 데이터 유실 판단 유보(C-24), GeekNews princox 인용 — community.md 패턴 2·§4 논쟁 A 일치
- 관측: OTel 원문·`persist: false`·`head_sampling_rate` 기본 1·Traces 오픈 베타(2026-10-02) 범위, Observability 2026-12-01 가격(0.5 GB/일·7일, 50 GB·12 GB-월, $0.25·$0.10, 원문) — §2-1·§3-11 일치
- Turnstile 원문, Tunnel FAQ 비디오 원문(C-18), vinext 1.0 블로그 인용, Worker 크기 64 MiB(C-13), Orleans는 "닮았지만 같지 않다"(C-34 준수), JWT RFC 7519
- 베타 지도: vinext(C-1)·`cf` CLI·Workers VPC·KV Instant·Email Sending·DO SQLite 과금(C-5)·Access strict 2026-10-05·**계정 단위 하드캡 없음**(C-23)·AE·OAuth 2.1 draft-16(C-32)·`cloudflared` 2027 폐기 — §9 일치
- `(사실 확인 필요)` 주석 없음

### 미해소
- (없음)

## 08장 (라운드 1)

### ❌ 정정
- Stripe 이벤트 "`checkout.session.completed`는 결제 방식에 따라 달라지니 … 고르자(사실 확인 필요)" → `checkout.session.completed` + 지연 결제 수단의 `checkout.session.async_payment_succeeded`/`_failed`, `payment_status` 확인으로 명시. 코드 조건에 `async_payment_succeeded` 추가 — 근거: docs.stripe.com/checkout/fulfillment (stripe-hosted, 2026-10-03 확인)
- Email `EMAIL` 바인딩 키 "확인하지 못했다(사실 확인 필요)" → `"send_email": [{ "name": "EMAIL" }]` 스니펫 추가, `send()` 인자(`to`·`from`·`subject`·`text`/`html`)·반환(`messageId`)·에러(`code`, `E_SENDER_NOT_VERIFIED`) 명시 — 근거: Email Sending Workers API (dateModified 2026-09-16)
- `actions/checkout@v4` → `@v6` — Cloudflare GitHub Actions 문서 예제(2026-09-18)와 일치
- Pulumi Java 골격: 메서드만 있던 조각을 `import com.pulumi.cloudflare.R2Bucket/R2BucketArgs/D1Database/D1DatabaseArgs` + `class App`으로 보정(클래스·빌더 이름은 원안 그대로 확인) — 근거: Pulumi Registry Cloudflare R2Bucket·D1Database (provider v6.x, 2026-09)

### ⚠️ 약화·삭제
- "Supabase는 … 대시보드에서 풀러를 거치는 연결 문자열을 먼저 보여준다" → "풀러를 거치는 연결 문자열도 함께 보여준다" — '먼저' 순서 근거 없음

### 🕒 신선도 / 마커 해소
- [리서치 공백] Supabase 직접 연결 네트워크 조건 → 해소: 직접 연결은 기본 IPv6, IPv4는 유료 애드온; 공유 풀러는 IPv4 전용, 세션 5432·트랜잭션 6543, 트랜잭션 모드는 prepared statement 미지원 (supabase.com/docs/guides/database/connecting-to-postgres, 2026-10-03 확인). Hyperdrive Supabase 문서(2026-04-21)는 IPv6 언급 없음 → "도입 전 실제 연결 확인" 권고로 마무리
- (사실 확인 필요) MySQL 바인딩 필드명 → ✅ `host/user/password/database/port` + `disableEval: true` 문서 예제와 일치, `mysql2` 3.13.0 이상 요구 추가 (Hyperdrive mysql2 2026-04-21)
- (사실 확인 필요) Workers eval 제한 → ✅ `eval()`·`new Function` 금지 (Workers Web standards 2026-04-23); mysql2 `disableEval`은 `generate-function`(코드 생성 파서) 경로를 끄는 옵션 (node-mysql2 소스)
- (사실 확인 필요) Protected Quick Tunnel과 Stripe → ✅ 저술가 추론 확인: "Email authentication requires an interactive browser session. It does not support non-interactive clients." (Quick Tunnels 2026-09-30) 인용으로 교체, 단락 유지
- (사실 확인 필요) Email `send()` 인자 형태 → ✅ 코드 그대로 맞음, 주석 제거
- (사실 확인 필요) Sippy → ✅ "R2에 있으면 R2에서, 없으면 원본에서 응답하며 동시에 R2로 복사" 동작 서술 추가 (Sippy 2026-09-18)
- (사실 확인 필요) Pulumi 클래스·인자 → ✅ (위 정정 참조), "provider 6.x 기준(2026-10)" 시점 표기
- (사실 확인 필요) wrangler-action 입력 이름 → ✅ `apiToken`·`accountId`·`command` (cloudflare/wrangler-action action.yml)

### ✅ 확인 (요약)
- HN "Cloudflare's AI Psychosis"(2026-08-15, 120점)·hasyimibhar 반박 — community.md 일치
- Hyperdrive: 지원 범위 인용, Neon serverless 드라이버 인용, Supabase Direct connection 인용, RDS 공개 접근·IP 허용, Workers VPC 권장(2026-04-29)·베타 무료, PlanetScale 청구(2026-06-18), MySQL GA(2026-08-07), 트랜잭션 모드·RESET·prepared statement·비지원 기능·두 번째 직접 연결 권고(2026-08-20/09-30), 한도 60초·50 MB·~20/~100 — 01_reference §2-1·§3-9, web_gaps §4 일치
- OpenNext #1214·2026-09-18 재보고·우회책 — community.md 일치
- Stripe: raw body 인용, 서명 HMAC-SHA256, stripe-node v23.0.0(2026-10-01) `workerd` 조건·SubtleCrypto 에러 문구, 중복 인용, 3일 재시도·순서 미보장·리다이렉트=실패 인용, `@worker-tools/stripe-webhook` 취약점 — web_gaps §4-4 일치
- Email: 공개 베타(2026-04-16), 3,000통/$0.35, Free 제한, SMTP(2026-06-08, smtp.mx.cloudflare.net:465, `api_token`), 5 MiB·50명, 일일 할당량, Queues 이벤트(2026-07-15), Routing Wrangler(2026-09-04) — §2-1·§3-5 일치
- R2 region `auto`/`us-east-1`, presigned URL 권고(2026-05-04), Sippy Azure·S3 호환(2026-07-24), Free 초과 과금 표현 — §2-4·§3-9 일치
- AI Gateway·Workers AI·Browser Run·Images 수치 — §2-1 일치
- 고정 출구 IP(Smart Shield 2026-04-16, ZT 애드온 2026-09-04, connect() 미적용), Tunnel 호스트명 라우팅(2025-09-18), VPC Network 바인딩 egress(2026-06-05) — §3-9 일치
- 장애 날짜(2025-11·12, 2026-02, R2 2026-08-08), Terraform v5.27.0·2025-10-09, wrangler-action v4.1.3(2026-09-24) — §4·§8 일치

### 미해소
- (없음)

## 부록 B (라운드 1)

### ❌ 정정
- (없음)

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- Containers `max_instances` 항목에 "(기본 스케줄링 정책 기준, 베타 `durable_object` 정책은 이 항목을 받지 않는다)" 추가 — 07_final.md·web_gaps.md §3(Containers configuration 2026-09-29), 13장 정정과 정합
- 프리뷰 항목을 13장 정정과 맞춤: "운영 설정을 물려받지 않는 `previews` 블록에 DO 바인딩을 넣지 않는다" — Worker Previews 설정 문서(2026-09-22)

### ✅ 확인 (요약)
- 계정 단위 하드캡 없음(2026-10 현재), 하드캡을 암시하는 항목 없음 — C-23
- [알림]/[차단]/[설계] 분류와 범위: Budget alerts·Billable Usage·Usage 이메일·Threshold billing = 알림(정보 제공·하루 지연·기본료 제외·임계치 변경 불가), `limits.*` = 호출 단위 차단, WAF Rate limiting(Free 1개·10초/10초)·`ratelimit`·Turnstile·`workers.dev` 끄기 = 유입 경로 차단, AI Gateway spend limits = AI Gateway 트래픽만, Free 계정 분리 = R2 제외 차단, 자작 차단기 = 보호 기능만·하루 지연 범위 명시 — 01_reference §2-2·§2-3과 일치
- R2 "무료 포함량을 넘으면 차단 없이 과금"·단위 올림·401 비과금 — §2-4·§2-5 일치
- 수치: Paid CPU 기본 30초·최대 5분, subrequests 10,000, D1 쓰기 $1.00/100만·천 배, KV Instant 건당 $0.10, Queues 64 KB, Workflows "no earlier than August 10, 2026", DO 128 MB·Hibernation, 한국 이그레스 $0.05·500 GB, Observability 2026-12-01, $4,586.64·18일·자동 정지 — §2-1·§2-5·§5 일치
- `(사실 확인 필요)` 주석 없음

### 미해소
- (없음)

## 09장 (라운드 1)

### ❌ 정정
- "커스텀 도메인으로만 서비스하는 Worker라면 `workers.dev`를 끈다. 이것이 기본값이다." → 실천 원칙으로 명확화 + "설정에 `routes`가 있으면 `workers_dev` 기본값도 `false`(Wrangler 설정 2026-10-02)", 미리보기 주소는 별도 `preview_urls` 설정 — 근거: developers.cloudflare.com/workers/wrangler/configuration (dateModified 2026-10-02)
- `.dev.vars` 위치 "프로젝트 루트" → "Wrangler 설정 파일과 같은 폴더" — 근거: Secrets 문서 (2026-07-03)

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도 / 마커 해소
- (사실 확인 필요) `ratelimits` 설정 형식 → ✅ `name`/`namespace_id`(정수를 문자열로)/`simple.limit`/`simple.period`(10 또는 60) 문서와 일치, 주석 교체·`namespace_id` 공유 규칙 추가 (Rate Limiting binding, dateModified 2026-04-23)
- (사실 확인 필요) 카운트가 위치별 근사치인지 → 해소: 위치(데이터센터)별 로컬 한도, "permissive, eventually consistent, and intentionally designed to not be used as an accurate accounting system" 인용 (同 문서 Locality·Accuracy 절). 저술가 결론(정확한 좌석 수는 DO) 유지
- (사실 확인 필요) Turnstile 스크립트 주소·클래스 → ✅ `https://challenges.cloudflare.com/turnstile/v0/api.js`, `cf-turnstile`, `data-sitekey` 일치; 숨은 필드 `cf-turnstile-response` 명시, "api.js 프록시·캐시 금지" 주석 (Embed the widget 2026-06-17)
- (사실 확인 필요) siteverify 엔드포인트·필드 → ✅ `POST https://challenges.cloudflare.com/turnstile/v0/siteverify`, `secret`·`response`, 응답 `success`; JSON·FormData(공식 예제) 모두 가능, 토큰 300초 유효·1회용 추가 (Validate the token 2026-09-16)
- (사실 확인 필요) 필수 시크릿 선언 형식 → ✅ `"secrets": { "required": [...] }` 형식 일치; 동작을 "deploy/versions upload가 누락 이름을 나열하며 실패, 로컬은 목록 키만 로드·누락 경고"로 확정 (Wrangler 설정 2026-10-02, Secrets 2026-07-03)

### ✅ 확인 (요약)
- HN white_viel(2026-02-25)·kentonv 인용(원문 오타 'rule son'·'wranlger' 보존) — community.md·§2-3 #9 일치
- 계정 전체 Worker 비공개 옵션(2026-08-14) — §3-7 일치
- Free Managed Ruleset 인용·Managed Ruleset의 부분집합·Free 기본 배포 — web.md 5-7 일치
- React/Next.js 체인지로그(2026-05-07) 두 인용 — §3-2 일치
- Rate limiting rule Free 1·10초·10초·Path/Verified Bot·IP, Pro 2/Business 5/Ent 100, 종량형 폐지 — §2-2 일치
- `ratelimit` 바인딩 GA(2025-09-19) 인용 — §3-7 일치
- Turnstile 두 단계 인용·대시보드 플래그·Free 20 위젯/10 호스트명/무제한/7일·독립 사용·Spin GA(2026-08-10) — §2-2·§3-7 일치
- Wrangler 키체인(2026-06-03)·프로필(2026-07-02)·디바이스 플로(2026-08-04)·secrets(2026-03-25) — §3-11 일치
- mTLS 100 인증서(2026-09-08)·RFC 9440(2026-03-27)·BYOCA Enterprise·API Shield Enterprise 애드온 — web.md 5-6 일치
- Jonker et al. IMC '17(/24 약 1/3, 웹사이트 약 3%), "약 2,100만 건" 미사용 — §3-7·C-30 준수

### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- `ctx.access` 코드: `handleAdmin(request, env, ctx.access)` + "ctx.access에서 이메일·그룹을 읽는다" → `const identity = await ctx.access.getIdentity(); identity?.email`, 본문에 `getIdentity()`(비동기)·`ctx.access.aud` 명시 — 근거: Workers > Cloudflare Access (dateModified 2026-08-18)
- SSH 출처 "2026년 4월 HN 사용자가 공유한 방식" → 1차 문서(SSH with cloudflared 2026-04-17) 기준으로 교체, HN은 보조 언급. 접속 명령 `ssh ssh.example.com` → `ssh <사용자명>@ssh.example.com`(문서 형태), 클라이언트 측 `cloudflared` 설치 필요 명시

### ⚠️ 약화·삭제
- "`/admin/*`과 `/api/admin/*`을 한 앱으로 묶어" → "같은 정책으로 보호한다" — 대시보드에서 한 앱에 경로 두 개를 넣는 절차는 확인한 문서에 명시 없음

### 🕒 신선도 / 마커 해소
- (사실 확인 필요) 경로 단위 앱 구성 → 해소: 호스트명 뒤 경로·`*` 와일드카드, `/admin/*`은 `/admin` 자체를 덮지 않음, 더 구체적 경로 규칙 우선 (Application paths 2026-04-17)
- (사실 확인 필요) Require Access protection 범위 → 해소: 설정명 "Block traffic to all domains in this account", 계정의 모든 호스트명 대상, 미보호 호스트명은 Error 1050, 공개 호스트명은 "Hostnames to Exempt" 또는 Bypass 정책 앱으로 열어야 함 (Require Access protection 2026-04-21). 경로 단위 앱만 있는 호스트명의 나머지 경로 처리는 문서에 없어 "예외 목록에 넣고 켠 뒤 직접 확인"으로 안내
- "Make all Workers private by default"에 보완: 공개 Worker는 Worker 단위 bypass 필요, Worker 단위 규칙은 라우트·커스텀 도메인·`workers.dev`·미리보기에 함께 적용, "Previews only" 선택지 (Workers Cloudflare Access 2026-08-18)
- (사실 확인 필요) `ctx.access` 신원 필드 → 해소 (위 정정). 저술가의 구조적 발견(정적 자산 Worker의 라우터가 `ctx.access` 미전달, Service binding HTTP·RPC로 미전파)은 문서 원문과 일치 ✅
- [리서치 공백] Nimbus JWKS 캐시 → 해소(소스 기준): Spring Security 7.1.1(`NimbusJwtDecoder.JwkSetUriJwtDecoderBuilder.jwkSource()` — 기본 `NoOpCache`면 Nimbus 캐시 사용, `rateLimited(false)`) + Nimbus JOSE+JWT 10.9.1(`JWKSourceBuilder.DEFAULT_CACHE_TIME_TO_LIVE = 5분`, `JWKSetBasedJWKSource`가 kid 미스 시 즉시 재조회). "소스 판독이며 실행 검증 아님" 명시, 스테이징 회전 점검 권고 유지
- [리서치 공백] Free 플랜 Gateway 세부 → 해소: Free는 DNS·HTTP·Network·Access 로그 24시간, 관리자 로그 18개월, Standard 30일 (Zero Trust logs 2026-04-17). 3자 사이트의 "물리 위치 3곳" 등은 1차 미확인으로 미사용
- (사실 확인 필요) Tunnel ingress SSH 표기 → 해소: 대시보드 Published application, Service 유형 SSH + `localhost:22`; 로컬 설정 파일 `service: ssh://localhost:22` (SSH with cloudflared 2026-04-17, Tunnel configuration file 문서)

### ✅ 확인 (요약)
- NIST SP 800-207(2020-08) 두 인용, BeyondCorp(2014-12) 초록 인용 — papers.md·§1-3 일치
- Access 좌석: Free "$0 forever"/"50 user limit", PAYG "$7 per user/month (paid annually)", Contract, 2020-10 Teams 무료 50석, Mesh "50 nodes and 50 users" 구분 — §3-6·C-35 일치
- 좌석 관리 인용(2026-05-01), 계정 한도(앱 500·IdP 50·토큰 50·이메일 1,000·Gateway 정책 500) — §3-6 일치
- Cloudflare IdP 기본(2026-06-18), OTP·generic OIDC, Auth0/Clerk 가이드 미확인 — §3-7 일치
- Require Access protection(2026-01-22) 인용, 2025-10 체인지로그 JWT 인용, `Cf-Access-Jwt-Assertion`·쿠키 권고(2026-05-06), `ctx.access` 인용 3건, 로컬 `access.dev` — §3-7 일치
- Spring Boot 4.1.1·Security 7.1.1(2026-08-20, Java 17+), `DefaultBearerTokenResolver` Bearer 접두어 요구·`HeaderBearerTokenResolver`, `jwk-set-uri`/`issuer-uri` 인용, RS256 기본·60초 skew, Nimbus validator 조합 — web_gaps §2 일치
- 키 회전 6주·7일, `public_cert` 경고, AUD 위치·불변, 서비스 토큰 `sub` 빈 문자열·`common_name`, 커스텀 클레임 ~1 KB — web_gaps §2-5 일치
- 서비스 토큰 헤더·단일 헤더 대안, strict 모드(2026-10-02)·2026-10-05 이후 기본 ON, 50개, 2026-08-25/08-26/09-22 기능 — §3-7 일치
- TIPSIO(HN 2026-09-18), Mesh(Networking > Mesh, 2026-04), 호스트명 라우팅(2025-09-18, GA 2026-08-11 제목 확인), RBI·전용 egress 애드온, OAuth 2.1 draft-16(2026-09-03), jorams 인용 — §3-6·§3-7·§1-6 일치

### 미해소
- (없음)

## 수락 게이트 수정 라운드 1 재검증

<!-- 2026-10-03 · 대상 04_manuscript.md (통합 원고 직접 정정, chapters/*_final.md 미변경) · 범위: editor_notes.md "수락 게이트 수정 라운드 1"의 30건 변경 + fact-checker 확인 대상 15건, diff 04_manuscript_v1.md 대조 · 웹 조회: developers.cloudflare.com 원문 markdown(index.md), honojs/website·honojs/hono GitHub main -->

### ❌ 정정
- **8장 `presign.ts` 라이브러리 교체 (확인 대상 1)** — AWS SDK for JavaScript v3(`@aws-sdk/client-s3`+`@aws-sdk/s3-request-presigner`) → `aws4fetch`. R2 Upload objects 문서(2026-07-29)의 "Presigned URLs (Workers)" 절이 Worker 안 presigned PUT 발급 예제를 `aws4fetch`의 `AwsClient` + `url.searchParams.set("X-Amz-Expires", …)` + `sign(new Request(url, { method: "PUT" }), { aws: { signQuery: true } })` → `signed.url`로 제시. aws4fetch 예제 페이지(2026-04-21)는 이 패키지가 "uses the `fetch` and `SubtleCrypto` APIs which you will be familiar with when working in browsers or with Cloudflare Workers"라고 적고, `Content-Type` 헤더를 서명 요청에 넣는 PUT 예제와 `service: "s3", region: "auto"`("Required by SDK but not used by R2")를 보여줌. aws-sdk-js-v3 예제 페이지(2026-04-21)·Presigned URLs 페이지(2026-08-22)의 SDK 예제는 Workers 실행을 언급하지 않음 → 문서화된 Workers 경로는 aws4fetch로 판정. 함수는 `async`, 반환은 `signed.url`(문자열)이라 9장 호출부 `url: await presignSlideUpload(c.env, key, contentType)`는 그대로 성립. 경로형 URL `https://<ACCOUNT_ID>.r2.cloudflarestorage.com/moim-uploads/<key>`, `X-Amz-Expires=300`. 도입 문장도 "Presigned URLs 페이지 예제는 AWS SDK v3, Workers 예제는 aws4fetch"로 정정.
- **8장 Content-Type 서명 서술 (확인 대상 2)** — "`ContentType`을 지정하면"(SDK 파라미터 표현) → "서명할 요청에 `Content-Type` 헤더를 넣으면 그 값이 서명에 포함되어" — aws4fetch 예제 "Specify the Content-Type header in the request when signing", 출력 예 `X-Amz-SignedHeaders=content-type%3Bhost`; `403/SignatureDoesNotMatch`는 Presigned URLs(2026-08-22) 원문 그대로.
- **8장 `wrangler dev` 문장 (확인 대상 5)** — 인용은 aws-sdk-js-v3 예제 페이지 원문("Currently, you cannot use AWS S3-compatible API while developing locally via `wrangler dev`.")과 일치하나, 예제가 aws4fetch로 바뀌어 출처 페이지를 명시("aws-sdk-js-v3 예제 2026-04-21 기준"). 서명이 R2와 통신하지 않는다는 근거("Presigned URLs are generated server-side with no communication with R2", Presigned URLs 2026-08-22)를 붙여, 로컬에서 만든 URL이 로컬 `UPLOADS` 시뮬레이션 버킷이 아니라 실제 버킷을 가리킨다고 정정.
- **4장 R2 절** — "presigned URL은 S3 호환 SDK로 만든다" → "S3 호환 SDK나 서명 라이브러리로 만든다"(8장이 SigV4 서명 라이브러리 aws4fetch를 쓰므로; Presigned URLs 문서 "an implementation of the AWS Signature Version 4 signing algorithm").

### ⚠️ 약화·삭제
- 8장 "R2 문서의 SDK 예제는 Worker 안에서의 실행을 따로 다루지 않으니 배포한 뒤 URL을 하나 발급해 실제로 PUT해보는 편이 안전하고" — 전제가 틀림(Workers 공식 예제 존재) → 삭제.

### ✅ 확인 (확인 대상별)
1. AWS SDK v3 Worker 실행 — 위 정정으로 대체(❌→aws4fetch). `nodejs_compat` 쟁점은 소멸(aws4fetch는 `fetch`+SubtleCrypto만 사용).
2. presigned URL 성질 — 만료 "1 second to 7 days (604,800 seconds)", "work with the S3 API domain (`<ACCOUNT_ID>.r2.cloudflarestorage.com`) and cannot be used with custom domains", Content-Type 서명 → `403/SignatureDoesNotMatch`, 브라우저 사용 시 CORS 규칙, "Treat presigned URLs as bearer tokens" — Presigned URLs(2026-08-22) 원문 일치.
3. CORS — "Without a CORS policy, browser-based uploads and downloads using presigned URLs will fail", 대시보드 Settings → CORS Policy → JSON 탭, 예시 `AllowedOrigins`/`AllowedMethods: ["PUT"]`/`AllowedHeaders: ["Content-Type"]` — CORS 문서(2026-09-23) 일치.
4. R2 API 토큰 — 권한표 "Object Read & Write"(읽기·쓰기·목록), "If you select the Object Read and Write or Object Read permissions, you can scope your token to a set of buckets", "You will not be able to access your Secret Access Key again after this step" — R2 Authentication(2026-10-01) 일치. Object Read only로는 PUT 불가하므로 9장 최소 권한 서술도 정합.
5. `wrangler dev` 제한 — 원문 일치(출처 명시로 정정, 위).
6. PutObject = Class A — R2 Pricing(2026-10-01) "Class A Operations include … `PutObject` …" 일치.
7. R2 바인딩 — `get(key, options?): Promise<R2ObjectBody | R2Object | null>`, 없으면 `null`, `R2ObjectBody.body: ReadableStream`, `httpMetadata: R2HTTPMetadata` — Workers API reference(2026-07-31) 일치. 옵션 없는 호출이므로 `.body` 접근 정합.
8. Hono `c.json(object, status?, headers?)` — `src/context.ts` `JSONRespond` 시그니처(object, status, headers: HeaderRecord) 일치.
9. Web Crypto HMAC — Workers Web Crypto 지원표 HMAC: importKey·sign·verify 지원(2026-09-30). `importKey("raw", …, { name: "HMAC", hash: "SHA-256" }, false, ["verify"])`·`verify("HMAC", key, sig, data)` 표준 형태. 만료값 `exp`도 서명 데이터에 포함되어 위조 불가.
10. 큐 핸들러 — `async queue(batch, env, ctx)`(Queues JavaScript APIs 2026-07-06) 일치. 4장 `export default { fetch: app.fetch, queue: consumeMail }` 그대로 성립.
11. DO RPC `taken()` — 4장 `reserve`와 같은 `this.ctx.storage.sql.exec(...).one().n` 동기 패턴, public 메서드 RPC + `await` 호출 — 4장 서술(Rules of Durable Objects 2026-08-20)과 정합.
12. D1 `.all<T>()` + `results[0]` — 4장 Workflow 예제와 같은 패턴. 정합.
13. `stripe_events (id TEXT PRIMARY KEY, type TEXT NOT NULL)` + `INSERT … ON CONFLICT(id) DO NOTHING` — PRIMARY KEY가 충돌 대상이 되므로 SQLite 문법상 성립. 정합.
14. 새 경로·시크릿·var 이름 — 저자 작성 식별자. 8·9장 사이 표기 일치(`presignSlideUpload`, `SPEAKER_LINK_SECRET`·`R2_ACCESS_KEY_ID`·`R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID`).
15. Rate limiting rule 범위 — 9장 규칙 서술("경로가 `/api/events/`로 시작하는 요청")과 `POST /api/events/:id/slides/upload-url` 정합.

### ✅ 장간 정합 (우선순위 4)
- 메시지 형태 `MailJob { eventId, email, kind }` — 4장 정의 = 8장 `consumeMail`·4장 Workflow `MAIL_QUEUE.send` 일치.
- `export default` 단일 결합 — 4장 L985 `{ fetch: app.fetch, queue: consumeMail }`, 8장 Stripe 추가분·`jobs.ts`는 "export default는 4장 그대로" 주석으로 정합. 별도 `new Hono`/`type Env` 잔존 없음.
- 컬럼 — 5장 단건 조회·8장 소비자·11장 Cache API 조회 모두 `starts_at`·`capacity` 사용, `published` 컬럼 참조 없음(grep 0건).
- `UNIQUE (event_id, email)` + `ON CONFLICT (event_id, email) DO NOTHING` — 4장 `0001_init.sql`·`saveRsvp` = 13장 콜백 일치.
- 9장 신청 폼 JSON 필드 `name`·`email` = 3장 핸들러 `c.req.json<Partial<Rsvp>>()`가 읽는 필드와 일치.
- 11장 좌석 API `GET /api/events/:id/seats` → `taken()` = 5장에서 추가한 `EventSeats.taken()`과 일치. 8장 그림 1의 `SPK -->|presigned PUT| R2`는 기존 `R2` 노드에 연결됨.
- 13장 "사실상의 하드캡(R2 제외)" — R2 무료 포함량 초과분 과금(01_reference §2-4), 부록 B 맺음말의 "자작 차단기 몇 분 / 예산 알림 다음 날(정보 전용)" — 13장 `moim-guard`(L3567)·4장 예산 알림 서술과 정합.

### 🕒 신선도
- 새로 인용한 문서 날짜를 본문에 명기: R2 Upload objects 2026-07-29, aws4fetch 예제 2026-04-21, aws-sdk-js-v3 예제 2026-04-21.

### 참고
- 뒷부속 참고문헌은 이번 라운드에서 손대지 않음(원장 그대로 원칙). 8장이 새로 인용한 R2 페이지(Presigned URLs·CORS·Authentication·Upload objects·aws4fetch·aws-sdk-js-v3)는 목록에 없음 — 추가 여부는 editor 판단.
- `(사실 확인 필요)` 잔존 0건.

### 미해소
- (없음)
