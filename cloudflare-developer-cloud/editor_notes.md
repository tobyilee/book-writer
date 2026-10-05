# 편집 노트 — Cloudflare를 나의 클라우드로 (Phase 4 통합, 2026-10-03)

- 산출: `04_manuscript.md`, `book_manifest.json`, `length_report.md`, 이 파일. `02_plan.md`는 11장 종료 상태 행·고정 박스 목록·개정 이력만 갱신.
- 원칙: `chapters/*_final.md`는 건드리지 않았다. 모든 본문 수정은 통합 원고에만 들어가 있고, 아래 "변경 기록"이 그 전체 목록이다(정확히 한 곳만 바꾸도록 문자열 단위로 적용). 일부 장을 다시 쓰게 되면 그 장의 final로 원고 섹션을 교체한 뒤 아래 해당 장 항목을 다시 적용하면 된다.
- 미해소: `factcheck_log.md`의 15개 `### 미해소` 절은 모두 `(없음)`. 원고에 `(사실 확인 필요)`·`[리서치 공백]`·`[미완성]`·`[이미지 예정]` 마커 없음.

## 1. 통합 플래그 15건 처리 (`integration_flags.md`)

| # | 플래그 | 처리 |
|---|---|---|
| 1 | 11장 종료 상태가 계획 표와 다름 | `02_plan.md` 11장 행을 원고대로 갱신(`moim-web` Workers Cache + `ctx.cache.purge({tags})` + 상태 문구 HTML `max-age` 60초, `moim-api`는 미적용, 목록 API는 Cache API 30초, 존 캐시·Cache Rules는 Spring 오리진). 2장 비용 메모·"무료를 지키는 세 가지 원칙", 5장 ISR 단락, 12장 가정("11장에서 켰던 Workers Cache는 끈다")이 모두 이 결론과 맞아 본문 수정 없음 |
| 2 | `moim-web` 배포 예외(`npm run deploy`) | 5장의 "8장의 GitHub Actions 배포가 모두 `wrangler deploy` 기준"을 "Wrangler 기준"으로 완화(같은 장 뒤에서 예외를 밝힘). 8장 `wrangler-action` 예제 뒤에 `moim-web`은 `command: deploy` 대신 `npm run deploy` 단계를 두라는 한 문장 추가. 13장 `limits.*` 절에 "`moim-web`은 빌드가 만든 `dist/server/wrangler.json`으로 배포되니 거기에 `limits`가 실렸는지 확인" 추가 — 루트 `wrangler.jsonc`의 `limits`가 빌드 산출물로 전파되는지는 원장에 없어 단정하지 않고 확인 권고로만 둠 |
| 3 | Preview × Containers 서술 불일치 | 7장이 두 1차 출처(Worker Previews 블로그 2026-09-22 ↔ Containers FAQ 2026-10-02)를 병기·한정한 서술을 기준으로, 5장 인용 뒤·13장 설계 규칙·부록 B 항목에 "Containers 쪽은 FAQ와 서술이 엇갈린다(7장)" 단서를 붙임. DO 쪽 서술(프리뷰마다 DO 생성)은 그대로 |
| 4 | 13장·부록 B의 `max_instances` 의존, 14장 `moim-report` | 확인만. 7장 `moim-report`(기본 정책, `standard-1`, `max_instances: 1`, Cron `0 1 1 * *`) ↔ 13장 설계 규칙·부록 B "Containers 이그레스와 인스턴스 수"·14장 그림 1의 `moim-report (Cron) → ReportContainer` 모두 일치. 수정 없음 |
| 5 | 새 박스 `> **논쟁: …**` | 정식 박스로 인정. 계획 자체가 12장 "논쟁 F 박스", 13장 "논쟁 G 박스"를 지시했고 이름만 고정 목록에 없었다. `02_plan.md` 고정 박스 목록에 추가하고, 서문의 "읽기 전에 알아둘 약속"에 박스 다섯 종을 소개. 다른 논쟁(A~E)은 본문 서술 그대로 둠 |
| 6 | 4장 presigned URL → 8장 | 8장에는 원칙(Optimize costs 인용)만 있고 생성 예제가 없다. 원장에도 JS 생성 예제 근거가 없어(Java `S3Presigner` 언급만, web_gaps §4-5) 예제를 새로 쓰지 않음. 대신 4장의 약속을 "presigned URL은 S3 호환 SDK로 만든다. Java `S3Presigner` 구성은 7장, 비용 이유는 8장"으로 고치고 최소 안전장치 박스의 장 번호를 (7·8장)으로 정정 |
| 7 | R2 Java SDK는 7장 담당 | 확인만. 8장은 "7장에서 다뤘다" 한 문장 참조뿐(이번에 "7장의 몫이었으니"로 문형만 변주). 중복 없음 |
| 8 | `ctx.access`와 `moim-web` | 확인만. `ctx.access`는 10장에만 등장하고, 10장이 "정적 자산 Worker·Service binding에는 전달되지 않음 → `moim-web`은 헤더를 `jose`로 직접 검증, `moim-api`가 재검증"으로 서술. 다른 장에 반대 서술 없음 |
| 9 | DO 선언 형식 — `exports`로 통일 | 대체 경로(7장만 `migrations` 유지) 불필요: `research/web_gaps.md` §3(Containers Wrangler configuration 2026-09-29)의 최소 구성이 `exports`(`"type": "durable-object"`, `"storage": "sqlite"`)를 쓴다. 7장 `ReportContainer`·13장 `UsageMeter`를 `exports`로 바꿈. 7장의 "둘 다 허용, 혼용 불가" 설명은 4장과 겹쳐 "4장의 `EventSeats`처럼 선언형 `exports`로 선언, Containers 문서 최소 구성도 같은 형식" 한 문장 콜백으로 축소. 13장 "클래스와 마이그레이션은 최상위에" → "DO 클래스 선언은 최상위에". `moim-api`의 `METER` 바인딩은 `script_name` 참조라 `exports` 불필요 |
| 10 | custom domain vs route | 구조 변경 없음. 3장이 Custom Domains 문서(2026-09-29) 인용으로 "라우트 Worker가 커스텀 도메인 Worker 앞에서 먼저 받는다"를 이미 설명 |
| 11 | kentonv 10GB 발언 오귀속 | 원고 쪽은 문제없음: 4장이 "그가 예로 든 것은 Durable Objects로 SQLite DB를 수백만 개 만드는 방식"이라고 바르게 귀속. 다른 장에 D1 근거로 쓴 곳 없음. 레퍼런스 §3-3 논쟁 B의 오귀속은 원장 문서라 편집자가 고치지 않음(아래 §6) |
| 12 | 테스트 `SELF` → `exports.default.fetch()` | 확인만. `SELF`는 3장에서 deprecated 설명으로만 등장. 다른 장 테스트 예제 없음 |
| 13 | CI 예제 버전 | 확인만. GitHub Actions 예제는 8장 하나(`actions/checkout@v6`, `wrangler-action@v4`, `apiToken`·`accountId`·`command`). 5장은 Workers Builds만 다루고 Actions YAML 없음 |
| 14 | `workers_dev` 기본값 | 모순 없음. 2장의 "배포하면 `workers.dev` 주소를 알려준다"는 라우트가 없는 첫 배포 시점이라 맞고, 9장이 "routes가 있으면 기본 false, 그래도 명시"를 설명. 다만 9장이 "`moim-api`는 `workers.dev`를 닫았는지 확인하지 않았다"고 쓴 것은 3장 설정(`"workers_dev": false`)과 모순이라 콜백으로 정정 |
| 15 | 10장 Access API | 확인만. `await ctx.access.getIdentity()`, `ctx.access.aud`, 정적 자산 Worker·Service binding 미전달 — 다른 장 언급 없음 |

## 2. 통권 읽기에서 따로 잡은 것

- **묶음 경계 전환.** 4→5: 5장 서두에 "4장까지 `moim-api`가 D1과 DO를 갖추며 자라는 동안 `moim-web`은 여전히 SPA"라는 이음 추가. 7→8: 8장 서두가 이미 7장 종료 상태를 정확히 되짚고 있어 손대지 않음. 10→11: 11장에 "만들고, 잇고, 지키는 일을 마쳤으니 4부로" 전환 문장 추가. 부 경계인 5→6에도 6장 오프닝(상황 가정)을 해치지 않는 한 문장 이음 추가.
- **지킬 수 없는 앞 장 약속 정리.** 6장 "8장에서 Protected Quick Tunnel을 다시 쓴다" ↔ 8장 "이메일 PIN은 Stripe 서버 호출을 통과 못 한다" — 6장 문장을 "어디까지 통하는지 다시 따져본다"로. 4장 코드 주석 "9·10장에서 발표자만 올릴 수 있게 막기 전까지" — 9·10장이 업로드 인증을 다루지 않아 장 번호 약속 제거.
- **회수되지 않던 콜백.** 3장 "웹 표준 API 성질은 14장 출구 전략에서 다시 쓸모가 생긴다" → 14장 출구 절에 한 문장으로 회수.
- **중복 인용.** 12장이 1장의 Shahrad 인용 블록을 그대로 반복해 콜백 + 수치 요약으로 바꿈(수치·출처 동일). 5장 `cf` 전망 박스가 3장 박스와 제목·정의 인용이 같아 "vinext와 `cf` 경로"로 좁히고 3장 콜백.
- **7장 마무리 순서.** `### 이 장의 핵심` 뒤에 `---`와 의사결정 표가 오던 것을, 다른 장(3·4·10·11·13장)처럼 본문(의사결정 표) → 핵심 순으로 재배열. `---` 제거.
- **오독 표기.** 14장 "13장에 걸쳐" → "열세 장에 걸쳐".

## 3. 용어·박스 결정

계획 "용어 표기"를 기준으로 했고, 계획에 없던 흔들림은 아래처럼 정했다(서문 "읽기 전에 알아둘 약속"에 공지, `02_plan.md` 개정 이력에 기록).

- **프리뷰 / 미리보기:** Worker Previews와 그 주소는 "프리뷰"(최다 표기). 5장 서두의 "링크 미리보기가 텅 빈다"는 메신저 링크 미리보기라 유지.
- **changelog / 체인지로그 / 변경 기록:** 묶음별로 갈려 있었다(2~4·11~13 / 8~10 / 5~6). 본문은 "changelog", 괄호 출처 표기는 원장과 같은 "Changelog YYYY-MM-DD" 유지.
- **레이트 리밋 → 레이트 리미팅**(8·13장, 계획 표기). **무료 플랜 → Free 플랜**(9장의 존 요금제 지칭). 10장의 "Teams 무료 플랜 발표" 같은 역사적 명칭과 5장 다모앙 일화 인용은 유지.
- **"워커"** 8회(11장)는 모두 브라우저의 "서비스 워커"라 유지.
- **WARP 병기:** 1·6·10장 각 장 첫 등장에만 "(구 WARP …)" — 계획 규칙대로이며 반복 없음.
- **12장 표의 `同上`** → "위와 같음".
- **박스 형식 통일:** 8~10장 묶음이 쓰던 인라인형 `> **비용 메모** — 본문`을 다른 장과 같은 블록형(제목 줄 + 본문 줄)으로 바꿈(8장 비용 메모·다른 쓰임 3개, 9·10장 비용 메모). 7장 "전망 상자" → "전망 박스".
- **박스 종류(최종):** 비용 메모 / 최소 안전장치(4·7장) / 다른 쓰임 / 전망 / 논쟁(12·13장). 장 고유 박스 두 개는 유지 — 2장 "Pages → Workers 이전 요점"(계획의 이전 박스, 바로 위 소절 제목과 같던 이름을 바꿈), 3장 "isolate는 안전한가"(계획의 Spectre 박스).

## 4. 통권 변주 점검표

오프닝·클로징은 계획의 통권 변주 배정표와 모두 일치한다. 인접 장 오프닝 중복 없음, 상황 가정 3/14(3·6·12장, 상한 4 이내), 클로징 14종 모두 다름. 말버릇 수는 통합 원고 기준 grep 값(편집 후).

| 장 | 오프닝 기법 | 클로징 형태 | 최다 반복 말버릇 (편집 후) | 편집 |
|----|------------|------------|-----------------|------|
| 1 | 정의 뒤집기 (CDN 회사라는 통념) | 열린 질문 ("이 지도에서 내 서비스는 어디에?") | 그런데·하나씩·해보자 (각 3) | — |
| 2 | 인용·일화 (r/CloudFlare Workers vs Pages) | 적용 과제 (확인할 세 가지) | 편이 낫다 (3) | 셈이다 4→2 |
| 3 | 상황 가정 (Spring 개발자의 static 캐시·스레드 풀) | 습관 대조표 → 핵심 | 여기서 (4) | — |
| 4 | 실패 장면 (에러 0개 KV 레이트 리미터) | 결정 플로차트 → 핵심 | 그런데 (4) | — |
| 5 | 수사적 질문 (Vercel 밖 Next.js) | 한 문장 여운 ("프레임워크는 바뀌고, 어댑터는 늦는다") | 다만·여기서 (각 5) | 4→5 이음 |
| 6 | 상황 가정 (금요일 저녁 데모) | 운영 명령 세 줄 | 그렇다면 (3) | `---` 제거, 1부→2부 이음 |
| 7 | 앞 장 콜백 (Tunnel 뒤 서버 전원이 꺼지면?) | 의사결정 표 → 핵심 | 다만 (8→5) | 다만 3회 변주, 순서 재배열 |
| 8 | 인용·일화 (HN "Too many ways…") | 원칙 한 줄 압축 | 그런데·여기서 (각 4~6) | 하나씩·"여기서는" 틀 변주, "다음에 할 일" 제거 |
| 9 | 실패 장면 (`workers.dev`로 WAF 우회한 봇) | 공격자 시점 되짚기 | 그런데 (5) | 그런데 1회 변주 |
| 10 | 정의 뒤집기 (NIST SP 800-207) | 자가 진단 질문 세 개 → 핵심 | 다만 (6→4) | 다만 2회 변주 |
| 11 | 인용·일화 (HN stale HTML) | 오해 정정 ("캐시를 켜면 싸진다") → 핵심 | 여기서 (4) | 3부→4부 이음 |
| 12 | 상황 가정 (커뮤니티 1면) | 계산 결과 (월간 사용량 표) | 여기서 (5) | 1장 인용 반복 제거 |
| 13 | 충격적 수치 ($34,895) | 오늘 밤 할 일 다섯 가지 + 부록 B → 핵심 | 짚어두자 (2) | — |
| 14 | 인용·일화 (GeekNews 장애 댓글) | 닫는 매듭 (나의 클라우드의 뜻, "출시 버튼을 누르자") | 다만 (2) | 출구 전략 콜백 |

- **통권 과포화 후보:** 본문 14장 기준 "다만"(37→32), "그런데"(38→37)는 한국어 기본 접속어라 책 전체로는 띠 안이지만 7·10장에 몰려 있어 그 장만 줄였다. 공감 표현(난감·찜찜·아찔·끔찍)은 모든 장이 1~2회로 띠 안.
- **"다음 장에서는 ~" 공식 클로징:** 없음. 8·9장이 연달아 "다음에 할 일/다음 차례"로 끝나던 것만 8장 쪽을 걷어냄(9장 서두 "8장에서 돈이 오가기 시작했으니"가 이음을 받음).
- **구분선 코다:** 5·6·7장(같은 묶음)이 연달아 `---` 뒤에 클로징을 두던 형식을 5장에만 남김.

## 5. 앞·뒤 부속

- **서문:** 문제의식(어디에 둘까 / Spring은 어디에 / 청구서), 대상 독자, 4부 구성과 골라 읽기 경로, "읽기 전에 알아둘 약속"(시점·예제 규약·박스·용어·인용). 본문에 이미 있는 사실만 가리킨다(하드캡 부재, 기준일, Spring Boot 4.1.1·Security 7.1.1 등).
- **에필로그:** 두지 않았다. 계획에 에필로그가 없고, 14장이 종합 정리형 + 닫는 매듭(여정 회고·다섯 질문·"나의 클라우드"의 뜻)으로 그 역할을 이미 한다. 뒤에 에필로그를 더하면 같은 회고가 두 번 나온다.
- **부록 A:** `01_reference.md` §2-1·§2-2에서 행 단위로 옮겼다. "Free 초과 시" 열은 원장에 동작이 적힌 칸만 "차단/과금"으로 채우고, 원장 칸이 비어 있는 Queues·Cron Triggers·Workers Cache·Durable Objects·Browser Run·Analytics Engine·Workers Logs는 "문서 미확인"으로 남겼다(짐작으로 "차단"을 쓰지 않음). KV Instant는 "미공지", Containers·Email Sending·Trace Events Logpush는 "Free 불가". R2는 "과금"(§2-4·C-37 권장 표현). 모든 행에 기준 문서·날짜, 날짜 표기가 없는 문서(Access 제품 페이지·WAF·Cache Rules·Tiered Cache·Cache Reserve)는 "검색 시점 2026-10-03". 함정 3개(Workers Cache·KV Instant·R2)는 표 아래 주석. Vectorize(문서 간 충돌 C-2, 본문 미사용)·Pages·일반 Logpush는 뺐다고 명시. 표의 DO 스토리지 단가 옆에 "개시 확정 공지 미확인"(C-5) 병기.
- **부록 B:** `appendix_b_final.md` 그대로 + 플래그 3 단서 한 곳.
- **부록 C:** §0 명칭·상태 표(독자용 축약 — 본문에 등장하지 않는 "Developer Week → Agents Week" 행은 뺐고, §0-14 CLI 방침은 "Workers CLI는 Wrangler 하나 → Wrangler v4 + `cf` 베타" 행으로 바꿔 적음) + factcheck_log 근거 두 행(`SELF`→`exports.default.fetch()`, `migrations`→`exports`) + §8 도구 버전 + `research/web_gaps.md` §2-1·2-2의 Spring Boot 4.1.1 / Spring Security 7.1.1 / Spring Framework 7.0.9(2026-08-20, Java 17+). `cf` CLI 버전은 원장대로 "수집하지 못했다".
- **참고문헌:** `01_reference.md` §10-1~10-4 항목을 그대로 옮김(서지·`[갭필]`·`[원문]`/`[초록]`/`[요약]` 라벨 유지, 원장 순서). §10-4 끝의 "검토 후 제외" 줄과 §10-1 끝의 "한국어판 공식 블로그 HTTP 200" 메모는 항목이 아니라 제외. 본문이 인용했는데 §10에 없던 1차 출처는 `research/web_gaps.md`·`factcheck_log.md`에 URL·날짜가 있는 것만 "보강 조사" 절로 추가(vinext README·릴리스·PR #3504, Containers API·Wrangler 설정, Spring Boot·Security 릴리스와 레퍼런스, Stripe 문서, Supabase 연결 문서, Wrangler 설정·Worker Previews 설정 등 23건). 새로 만든 항목 없음.
- **콜로폰:** 라이선스 정식 코드 `CC BY-NC-SA 4.0`을 지면에 그대로 표기(매니페스트 `license`는 비워 빌드 기본값과 같음), 하네스 v2.0.0, 식별자 `urn:uuid:7ae484e4-06ae-4ec0-8308-d14c91014f75`(신규 발급, 재빌드 시 보존).
- **매니페스트:** `title`은 주제목만, `subtitle` 분리, `license`·`rights`는 비움(빌드가 기본값으로 채움). `cover_alt`는 기본 패턴 — 표지가 만들어지면 cover-designer가 실제 표지 묘사로 갈음하면 좋다.

## 6. 사용자 판단이 필요하거나 알려둘 것 (구조·내용 제안 — 원고에는 반영하지 않음)

1. **presigned URL 생성 예제가 책에 없다.** 4·7·8장 모두 "presigned URL을 쓰자"고 권하지만 JS 쪽 생성 코드는 없다(원장에 근거가 없어 편집 단계에서 쓰지 않음). 실습 완결성을 원하면 8장에 AWS SDK for JavaScript 기반 예제를 추가하고 fact-checker 확인을 거치는 것을 제안한다.
2. **발표 자료 업로드 경로의 인증이 책 어디에도 없다.** 4장 `PUT /api/events/:id/slides/:name`은 "인증을 붙이기 전까지 공개 배포하지 말라"는 주석으로 끝난다. 9장(앱 로그인 경계)이나 10장(Access)에서 한 단락으로 매듭지을지 결정이 필요하다.
3. **프리뷰 × Containers는 1차 출처끼리 충돌한다.** Worker Previews 블로그(2026-09-22)와 Containers FAQ(2026-10-02). 원고는 양쪽을 병기하고 직접 확인을 권하는 선에서 맞췄다. 출간 직전 재확인 항목에 넣는 것을 권한다.
4. **`moim-web`의 `limits.*` 전파.** 루트 `wrangler.jsonc`의 `limits`가 vinext 빌드 산출물(`dist/server/wrangler.json`)에 실리는지 원장 근거가 없다. 13장은 "확인해두자"로만 썼다.
5. **레퍼런스 원장의 오귀속.** `01_reference.md` §3-3 논쟁 B가 kentonv의 10 GB 발언을 D1 근거로 적고 있다(실제로는 DO SQLite DB 이야기). 원고(4장)는 바르게 귀속했다. 원장 정정은 리서치 단계 소관.
6. **11·13장 소절 수**가 계획의 5~8개를 넘는다(12·11개). 분량은 계획 ±20% 안이라 구조를 바꾸지 않았다.
7. **Spring 예제 언어는 Java**(계획 승인 시 결정). Kotlin 전환을 원하면 7·10장 예제와 서문 약속 문구가 대상이다.

## 7. 변경 기록 (통합 원고에만 적용, 47건 + 기계적 일괄 처리 2종 + 재배열 1건)

일괄 처리: ① 8~10장 인라인 박스 → 블록형, ② 본문 "체인지로그" → "changelog". 재배열: 7장 의사결정 표를 `### 이 장의 핵심` 앞으로 옮기고 `---` 제거.

- **2장** — 말버릇 '셈이다' 장내 4회 → 2회로 변주
- **2장** — 말버릇 '셈이다' 변주
- **2장** — 박스 제목이 바로 위 소절 제목과 같아 이름을 구분 ("Pages → Workers 이전 요점")
- **4장** — 9·10장이 발표자 업로드 인증을 실제로 다루지 않아 지킬 수 없는 앞 장 약속을 제거
- **4장** — 플래그 6: 8장에 생성 예제가 없어 약속을 실제 내용(7장 S3Presigner, 8장 비용 원칙)에 맞춤
- **4장** — 플래그 6: 장 번호 콜백 정정 (8장 → 7·8장)
- **5장** — 4→5 묶음 경계 전환: 4장의 데이터 계층에서 5장의 프런트로 넘어가는 이음 추가
- **5장** — 플래그 2: 같은 장 뒤에서 moim-web은 npm run deploy로 배포한다고 밝히므로 'wrangler deploy 기준'을 완화
- **5장** — 3장과 같은 제목·같은 정의 인용의 전망 박스가 반복돼 5장 박스는 vinext 경로로 좁히고 3장을 콜백
- **5장** — 용어: 본문의 changelog 표기 통일
- **5장** — 플래그 3: 5·7·13장 프리뷰×Containers 서술 정합 — 5장에 7장 콜백
- **5장** — 용어: Worker Preview는 '프리뷰'로 통일
- **6장** — 1부→2부 전환: 5장까지의 완결 상태에서 Cloudflare 밖으로 나가는 이음 추가
- **6장** — 용어: changelog 표기 통일
- **6장** — 8장이 이메일 PIN은 Stripe 서버 호출을 통과하지 못한다고 밝히므로 6장의 앞 장 약속을 사실에 맞춤
- **6장** — 통권 변주: 5·6·7장이 연달아 `---` 구분선 뒤 클로징을 두던 형식 중 6장 것을 정리(7장은 재배열에서 정리)
- **7장** — 박스 명칭 통일(전망 박스)
- **7장** — 말버릇 '다만' 장내 과포화(8회) 완화
- **7장** — 플래그 9: DO 선언을 선언형 exports로 통일 (Containers Wrangler 설정 2026-09-29 최소 구성이 같은 형식, research/web_gaps.md §3)
- **7장** — 플래그 9: 4장 설명과 겹치던 '둘 다 허용, 혼용 불가' 설명을 짧은 콜백으로 축소
- **7장** — 말버릇 '다만' 변주
- **7장** — 말버릇 '다만' 변주
- **8장** — 말버릇 '하나씩' 장내 과포화 완화
- **8장** — 말버릇 '하나씩' 변주
- **8장** — 용어: '레이트 리미팅'(계획 용어 표기)
- **8장** — 플래그 2: moim-web 배포 예외를 CI 예제에 명시
- **8장** — 통권 변주: 8·9장이 연달아 '다음 차례/다음에 할 일'로 닫혀 8장 쪽 공식을 제거(9장 서두가 이음을 받음)
- **8장** — 말버릇: 8장의 'N장에서 다뤘다. 여기서는 ~' 틀 반복(3회) 변주
- **8장** — 말버릇: 'N장에서 다뤘다. 여기서는' 틀 변주
- **9장** — 3장 moim-api 설정에 이미 workers_dev:false가 있어 '확인하지 않았다'는 서술이 앞 장과 모순 — 콜백으로 정정
- **9장** — 말버릇 '그런데' 변주
- **9장** — 용어: 요금제 이름 'Free' 고정
- **10장** — 용어: 프리뷰 통일
- **10장** — 용어: 프리뷰 통일
- **10장** — 말버릇 '다만' 장내 6회 완화
- **10장** — 말버릇 '다만' 변주
- **11장** — 10→11 묶음 경계(3부→4부) 전환 문장 추가
- **12장** — 표기: 한자 '同上'을 한국어로
- **12장** — 1장과 같은 인용 블록이 반복돼 12장은 1장 콜백 + 수치 요약으로 교체(수치·출처 동일)
- **13장** — 플래그 2: moim-web 배포 예외와 limits.* 규약 연결(빌드 전파 동작은 원장에 없어 확인 권고로만)
- **13장** — 용어: 레이트 리미팅
- **13장** — 플래그 9: exports 통일에 맞춰 '마이그레이션' 표현 정리
- **13장** — 플래그 3: 프리뷰×Containers 단정을 7장 서술과 맞춤
- **13장** — 플래그 9: UsageMeter DO 선언을 exports로 통일
- **14장** — '13장에 걸쳐'가 '13장에서'로 오독돼 표기 변경
- **14장** — 3장이 '14장 출구 전략에서 다시 쓴다'고 한 약속(웹 표준 API)을 회수하는 콜백
- **부록 B** — 플래그 3: 부록 B의 단정을 7장 서술과 맞춤

## 수락 게이트 수정 라운드 1

<!-- 2026-10-03 · 단일 담당(chapter-writer 겸 editor) · 대상 04_manuscript.md (백업 04_manuscript_v1.md), chapters/*_final.md는 손대지 않음 · 행 번호는 05_acceptance.md의 원 행 기준 -->

산문 순증 약 2,700자(코드 블록 제외, 공백 제외). 오케스트레이터 결정 1~4를 모두 반영했다.

### 수정 목록

| # | 위치(원 행) | 기준 | 변경 |
|---|---|---|---|
| 1 | 4장 R2 절(899~910) | (f)(e) | 인증 없는 `PUT /api/events/:id/slides/:name` 삭제 → 바인딩으로 읽는 `GET /api/events/:id/slides/:name` 예제로 교체, 코드 주석에 "올리는 경로는 아직 열지 않는다 — 발표자 확인은 9장, presigned URL 발급은 8장". 뒤 문단을 "올리는 쪽은 사정이 다르다"로 고쳐 100 MB 한도 → presigned URL → JS 발급 8장·Java 7장·발표자 자물쇠 9장으로 연결 |
| 2 | 4장 최소 안전장치(922~923) | (e) | #2 "Worker 바인딩으로만 접근" → "읽기는 Worker 바인딩으로"(쓰기가 S3 API로 가므로). #3 "(7·8장)" → "발급 전에 상대 확인, 발급 코드는 8장·발표자 확인은 9장" |
| 3 | 5장 단건 라우트(1193~1209, 1222) | (e) | `GET /api/events/:id`를 실제 코드로: 4장 조회 + `WHERE id`, `.all()`+`results[0]`, `EventSeats.taken()` 메서드 추가 후 `seatsLeft = capacity - taken`. `MoimEvent`를 응답 그대로(`id: number`, `starts_at`, `capacity`, `seatsLeft`)로, 페이지의 `event.startsAt` → `event.starts_at` |
| 4 | 7장 1900 | (e) | "JS 쪽 presigned URL" → "JS로 presigned URL을 발급하는 코드"(8장에 실제로 생김) |
| 5 | 8장 1951·2155 | (d) | 예고형 "따져보겠다"·"배치하겠다" → 평서 |
| 6 | 8장 Stripe 핸들러(2030~2079) | (e) | 별도 `type Env`·`new Hono`·`export default app` 제거 → "(추가분) 같은 app에 라우트를 더한다. export default는 4장 그대로" 주석, Env 필드는 `wrangler types`로 재생성한다고 명시, `stripe_events` 표 정의(0002 마이그레이션)를 주석으로 추가 |
| 7 | 8장 메일 2094·2100~2115 | (e) | 2094 "로그만 남기거나 검증된 내 주소로만…" → "로그만 남겼다", "보낼 차례다" 제거. 소비자를 4장 `consumeMail(batch, env)` 개정판으로: `MailJob {eventId,email,kind}`를 받고 제목은 D1에서 조회, `kind === "reminder"`면 제목·본문 분기. 4장 `queue: consumeMail` 연결은 그대로라는 설명 1문단 |
| 8 | 8장 그림 1 | (e) | `발표자 브라우저 -->|presigned PUT| R2` 화살표 추가 |
| 9 | 8장 "업로드 경로도 다시 보자"(2153) | (f) | AWS SDK for JavaScript v3 presigned PUT 예제(`presign.ts`, `presignSlideUpload`) + 성질 다섯 가지 한 문단(만료 1초~7일, S3 API 도메인 전용, Content-Type 서명 포함, 브라우저용 CORS 규칙, bearer token) + R2 API 토큰 문단(Object Read & Write·버킷 한정·Secret 1회 표시, Worker 안 실행은 1차 문서 미기재 → 배포 후 실제 PUT 확인 권고, `wrangler dev` 로컬 S3 API 불가) |
| 10 | 9장 2273 | (d) | "미리보기용" → "프리뷰용" |
| 11 | 9장 문 목록(2281~2287) | (f) | "세어볼 차례다" → "센다". 다섯 번째 문 `POST /api/events/:id/slides/upload-url` 추가(무인증이면 R2 쓰기 과금), 자물쇠 요약 문장에 "발표자만 여는 문에는 서명한 링크" |
| 12 | 9장 신청 폼(2370~2377) | (e) | 기본 폼 전송 → `fetch`로 JSON(`name`·`email`·`token`) 전송 스크립트, 설명 문장 정정 |
| 13 | 9장 신설 절 "발표자만 여는 문 — 서명한 링크와 presigned URL"(시크릿 절 앞) | (f) | 오케스트레이터 결정 1: Access 좌석 대신 운영자(`/admin`, 10장 Access 뒤)가 발급하는 HMAC 서명 링크(행사·발표자·만료, hex 서명, Workers 시크릿), `crypto.subtle.verify`로 검증 후 8장 presigned PUT(5분) 발급, 브라우저 직접 PUT. 1회용은 D1 기록으로 확장 가능, `/api/events/` Rate limiting rule이 함께 적용됨을 한 줄 |
| 14 | 9장 시크릿(2402·2406~2410·2419·2425) | (e) | 비밀 값 목록·`wrangler secret put`·`secrets.required`에 `SPEAKER_LINK_SECRET`·`R2_ACCESS_KEY_ID`·`R2_SECRET_ACCESS_KEY` 추가, 토큰 범위 문단에 "R2 API 토큰은 `moim-uploads` 하나의 Object Read & Write만". 2427 "살펴보겠다" → 평서 |
| 15 | 9장 2438 | (d) | "이어 받겠다" → "13장의 방어선으로 이어진다" |
| 16 | 9장 2444 | (e) | 고객 로그인: "`moim-core`의 기존 Spring 로그인을 그대로" → `moim.example.com` 쪽 앱이 처리, Spring 회원 로직은 `moim-api`가 서비스 토큰으로 내부 API 호출(고객은 `core`에 직접 오지 않음, 10장) |
| 17 | 9장 공격자 되짚기(2448) | (f)(d) | 업로드 경로 공격 한 단계 추가("서명된 발표자 링크가 없으니 presigned URL을 받지 못한다"), "다음 차례다" 공식 삭제 → 되짚기 안에서 `/admin/*`을 공격자가 가장 오래 두드릴 문으로 닫음(계획 클로징 기법 유지) |
| 18 | 10장 2517 | (e) | `core.example.com` 앱에 고객 정책을 두지 않는 이유 한 문장(회원 로그인은 `moim.example.com` 쪽, Spring 회원 로직은 `moim-api`가 서비스 토큰으로) |
| 19 | 10장 2515·2578 | (d) | "넣어두자" → "넣는다", "`moim-core`의 차례다" → "다음은 `moim-core`다" |
| 20 | 11장 2744·2786 | (d) | 수사 대구 2회 → 평서("규칙은 제대로 적었다. 다만…", "캐시 동작은 Worker의 응답 헤더로 바꾼다") — 장내 3회 |
| 21 | 11장 Cache API 예제(2805) | (e) | `WHERE published = 1` 삭제 → 4장과 같은 `SELECT id, title, starts_at, capacity FROM events ORDER BY starts_at` |
| 22 | 11장 Workers Cache 결정 뒤(2870 다음) | (e) | 5장 페이지의 `남은 좌석` 줄을 HTML에서 빼고 `GET /api/events/:id/seats`(`moim-api`, `Cache-Control: no-store`, D1 없이 `EventSeats.taken()`만)로 브라우저가 받으며 `capacity - taken`은 브라우저가 계산, 5장 단건 라우트의 `taken()` 호출도 걷어냄 — 12장 계산(페이지뷰당 DO 1회·D1 10행)과 일치함을 명시. 2949 "클라이언트가 캐시하지 않는 API" → 해당 라우트를 지목 |
| 23 | 13장 멱등 예제(3184~3194) | (e) | `member_id` 인덱스 신설 → 4장 `UNIQUE (event_id, email)` + `ON CONFLICT (event_id, email) DO NOTHING`을 "4장부터 들어 있다"로 콜백 |
| 24 | 13장 3206 | 하드캡 | "사실상의 하드캡(R2 제외)" |
| 25 | 14장 출시 전 점검 보안 문단(3544) | (f) | "발표 자료 업로드 경로가 서명된 발표자 링크를 확인한 뒤에만 presigned URL을 내주는지(9장)" 추가 |
| 26 | 부록 B R2 항목 | (f) | "presigned URL은 확인된 사람에게만 짧은 만료로 발급" 추가, 장 표기에 9장 |
| 27 | 부록 B 맺음말(3800) | 하드캡 | "하루 안에 알게 되고" → 자작 차단기는 몇 분, 예산 알림은 늦어도 다음 날(정보 전용) |
| 28 | 6장 1408 | (d) | "반드시 … 믿어야 한다" → 권장 어조 + 이유 |
| 29 | 8장 1994·2096·2174, 10장 2515 | (d) | 연달아 붙은 청유형 일부 평서로 |
| 30 | 9장 문 목록 읽기 경로 문장(2283) | (f) | #1에서 생긴 4장 `GET /api/events/:id/slides/:name`을 읽기 경로로 명시(요청마다 R2 읽기 요금) — 공개 표면 지도 누락 재발 방지 |

에필로그: 오케스트레이터가 생략 사유를 수용 — 조치 없음.

### fact-checker 확인 대상 (새로 쓰거나 바꾼 사실·코드)

조회일은 모두 2026-10-03. 원장(`01_reference.md`·`research/*.md`)에 없는 항목이 대부분이라 갭필 대조가 필요하다.

1. **AWS SDK v3를 Worker 런타임에서 실행** — 8장 `presign.ts`. R2 1차 문서(AWS SDK v3 예제, 페이지 갱신 2026-04-21; Presigned URLs, 갱신 2026-08-22)는 Node 기준이고 Workers 안 실행·`nodejs_compat` 필요 여부를 적지 않는다. 본문은 "1차 문서가 따로 다루지 않으니 배포 후 실제 PUT으로 확인"으로 단정 회피. 근거는 3자 글뿐 — 최우선 확인.
2. **presigned URL 성질 다섯 가지**(developers.cloudflare.com/r2/api/s3/presigned-urls/, 갱신 2026-08-22): 만료 "1 second to 7 days (604,800 seconds)", "work with the S3 API domain (`<ACCOUNT_ID>.r2.cloudflarestorage.com`) and cannot be used with custom domains", Content-Type 서명 포함 시 다른 값이면 "403/SignatureDoesNotMatch", 브라우저 사용 시 CORS 필요, "Treat presigned URLs as bearer tokens". JS 예제 형태(`S3Client({ region: "auto", endpoint, credentials })`, `getSignedUrl(S3, new PutObjectCommand({ Bucket, Key, ContentType }), { expiresIn })`).
3. **CORS**(developers.cloudflare.com/r2/buckets/cors/, 갱신 2026-09-23): presigned URL 브라우저 사용 시 CORS 필요, 대시보드 CORS 정책 JSON의 `AllowedOrigins`·`AllowedMethods: ["PUT"]`·`AllowedHeaders: ["Content-Type"]` 형태. 본문은 대시보드 경로만 제시(`wrangler r2 bucket cors set --file`의 파일 형식은 대시보드 JSON과 다를 수 있어 쓰지 않음).
4. **R2 API 토큰**(developers.cloudflare.com/r2/api/tokens/, 갱신 2026-10-01): Object Read & Write 권한, 버킷 범위 한정 가능, Secret Access Key는 생성 직후 한 번만 표시.
5. **`wrangler dev` 로컬에서 S3 호환 API 불가** — AWS SDK v3 예제 페이지(2026-04-21)의 "Currently, you cannot use AWS S3-compatible API while developing locally via wrangler dev."
6. **R2 업로드(PutObject)가 Class A 연산** — 8장 "업로드 한 번도 쓰기 연산으로 센다". 4장 Class A=쓰기류 서술과 일치하나 PutObject→Class A 명시 확인.
7. **R2 바인딩 읽기 API** — 4장 `UPLOADS.get(key)`가 없으면 `null`, 있으면 `.body`·`.httpMetadata?.contentType`. 원장에 시그니처 없음.
8. **Hono `c.json(body, status, headers)` 3인자 형태** — 11장 좌석 라우트. 원장에 없음.
9. **Web Crypto HMAC** — 9장 `crypto.subtle.importKey("raw", …, { name: "HMAC", hash: "SHA-256" }, false, ["verify"])`, `crypto.subtle.verify("HMAC", key, sig, data)`. Workers Web Crypto 지원 범위로 확인.
10. **Queue 핸들러 두 번째 인자 `env`** — 8장 "큐 핸들러는 두 번째 인자로 `env`를 받으니 `queue: consumeMail` 연결은 그대로". `queue(batch, env, ctx)` 시그니처 확인.
11. **DO RPC `taken()`** — 5장. 4장 `reserve`와 같은 동기 SQL API 패턴(`.one().n`), RPC로 `await` 호출.
12. **D1 `.all<T>()`+`results[0]`** — 5장·8장(4장 Workflow 예제와 같은 패턴, 확인 부담 낮음).
13. **`stripe_events` 스키마**(`id TEXT PRIMARY KEY, type TEXT NOT NULL`)와 `ON CONFLICT(id)` 정합 — 저자 작성.
14. **새 경로 이름**(저자 작성, 사실 주장 아님): `GET /api/events/:id/slides/:name`, `POST /api/events/:id/slides/upload-url`, `GET /api/events/:id/seats`, `presignSlideUpload`, 시크릿 `SPEAKER_LINK_SECRET`·`R2_ACCESS_KEY_ID`·`R2_SECRET_ACCESS_KEY`, var `R2_ACCOUNT_ID`.
15. **9장 "Rate limiting rule이 `/api/events/`로 시작하는 경로에 걸려 있으니 업로드 경로도 함께 지킨다"** — 같은 장의 규칙 서술과 내적 정합만 확인.

- 2026-10-03 참고문헌 보강: 8장이 수락 게이트 수정 라운드 1에서 새로 인용한 R2 문서 중 URL·갱신일이 로그(editor_notes·factcheck_log)에 있는 3건(Presigned URLs 2026-08-22, CORS 2026-09-23, Authentication(API tokens) 2026-10-01)을 "보강 조사 — 1차 문서·소스"에 추가. Upload objects·aws4fetch 예제·aws-sdk-js-v3 예제는 로그와 8장 본문에 URL이 없어 보류(aws-sdk-js-v3 URL은 research/web.md 599행에만 있음).
- (오케스트레이터) 참고문헌에 R2 aws-sdk-js-v3 예제 페이지 추가 — URL은 research/web.md 원장, 날짜는 factcheck_log 재검증 섹션. Upload objects·aws4fetch 페이지는 원장에 URL이 없어 본문 인용(제목·날짜)으로만 둔다.

## 수락 후 마감 패스

2026-10-03, editor. 수락 게이트 라운드 2(ACCEPT)의 낮음 조치를 `04_manuscript.md`에 직접 반영했다. 행 번호는 반영 뒤 기준이다. 새 사실 주장은 넣지 않았다.

1. 14장 그림 1(3642): `speaker[발표자 브라우저] -- presigned PUT --> UPLOADS` 추가. 화살표는 엣지를 거치지 않고 R2로 바로 간다(8장 그림과 같은 경로). `mmdc`로 `htmlLabels:false` 설정(build_epub.sh와 같은 값) 렌더 확인, `foreignObject` 0건.
2. 9장 시크릿 절 `moim-api/wrangler.jsonc` 예시(2522): `"vars": { "R2_ACCOUNT_ID": "<계정 ID>" }` 한 줄과 "식별자일 뿐 비밀이 아니니 vars에 — 8장 presign.ts가 읽는다" 주석 추가. 8장 2187 주석이 가리키는 선언이 생겼다.
3. 9장 링크 예시(2470): `exp=1767225600`(2026-01-01 UTC) → `exp=1798761600`(2027-01-01 UTC). 옆에 사람이 읽는 날짜 표기는 없다.
4. 11장(2980): "정원 `capacity`는 행사 정보와 함께 HTML에 남으니" → "줄을 빼는 자리에 정원 `capacity`를 `data-capacity={event.capacity}` 속성으로 남겨 두면". 5장 페이지는 그대로 두었다(`MoimEvent` 타입에 이미 `capacity`가 있다). 좌석 API·"D1은 읽지 않는다" 주석·12장 계산은 바뀌지 않는다.
5. 9장 "발표자만 여는 문"(2497·2499): 서명 쪽 한 문장(링크를 만드는 코드도 같은 `SPEAKER_LINK_SECRET`을 `["sign"]`으로 가져와 같은 메시지를 `crypto.subtle.sign("HMAC", …)`으로 서명, 16진수로 `sig`에) 추가. 이어서 문단 하나를 나눠, 보여준 코드는 링크 만료 전까지 `fileName`을 바꿔 가며 presigned URL을 계속 받게 두고 그만큼 쓰기 연산과 저장 용량이 청구된다는 위험, 링크 만료를 행사 직전까지 짧게 잡고 한 번 쓰기는 사용한 `sig`를 D1에 기록해야 한다는 대책을 묶었다. 그 기록은 코드에 없다고 밝히고 위험의 범위("만료 전까지, 그 발표자 자리에")를 적었다. 원래 chapter-writer 담당 항목이었으나 이번 패스에서 처리했다.
6. `length_report.md`: `04_manuscript.md`를 장별로 잘라 `length_report.py`로 다시 쟀다. 합계 165,479자, 중앙값 11,981자, 1장 71%~8·10장 129%로 모두 70~150% 안이다. "±150자" 문장은 지웠다. 계획 대비 8장 +29%·9장 +27%·11장 +22%는 수락 게이트 수정분이라고 적었다.

남은 조치: 8장이 인용한 "R2 Upload objects"·"aws4fetch 예제"의 참고문헌 등재는 오케스트레이터/사용자 결정 사항(fact-checker의 URL 기록이 먼저)이라 이번 패스에서 손대지 않았다.
