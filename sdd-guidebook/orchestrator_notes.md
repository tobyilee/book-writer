# 오케스트레이터 메모 — editor 통합 시 정리할 교차 묶음 항목

## 묶음 B (4·5장, 부록 B) 저술가 보고
- 5장 Superpowers 계획 발췌에서 정전 밖 이름을 정함: 패키지 `com.bookshop.orders.refund`, 클래스 `RefundWindowPolicy`, 메서드 `isWithinWindow(Instant, Instant)`. 10장과 이름이 다르면 통일.
- 4장 Kiro `bugfix.md` 예: C0 오타("환뷸")가 기간 경과 거절 메시지에 있다고 가정, 보존 동작 `422 REFUND_WINDOW_EXPIRED`. 11장의 C0 서술과 맞출 것.
- 4장 cc-sdd 발췌의 EARS `Where` 패턴 "주문 단위 쿠폰 기능이 포함되면" — 3장 EARS 설명과 정합 확인.
- 5장 소절 순서 변경("설치하기 전에"를 "이 책의 선택" 앞으로) — 의도된 변경.
- mermaid: 4장 `timeline`, 5장 `quadrantChart` — 빌드 렌더 확인 필요.

## 묶음 A (1~3장) 저술가 보고
- EARS 주어 표기 불일치: 3장·6장은 `the 주문 서비스`, 4장은 `the 환불 서비스`/`THE Refund_Service`. 하나로 통일 (4장 Kiro 원형 재현 발췌는 원문 표기 유지 여부 판단).
- 1장에서 "참고 보고서"(sdd-report.md) 용어 도입 — 용어 표기에 반영.
- 3장 결정 기록은 "delivered_at부터 168시간"을 일부러 뺌(6장에서 공백 발견용). 3장 EARS 재작성에는 168시간 사용.

## 묶음 D (9~12장, 부록 A) 저술가 보고
- 11장 네 벌 비교 ①(SPEC.md EARS)·②(OpenSpec 델타) 발췌는 정전에서 재구성 — 6·8장 final 문장으로 교체할 것. 비교표 "스펙 분량" 행 ①② 칸에 실제 줄 수 기입. `<!-- 편집: ... -->` 주석 2곳 제거.
- 부록 A의 A.1~A.3 프롬프트를 6·7장 final 문구와 일치시킬 것.
- 정전 밖 세부(D가 정함): Gradle(`./gradlew test`, `bootRun`), Java 21·Spring Boot 3, 패키지 `com.bookshop.orders.refund`, 클래스 `RefundAmountCalculator`·`RefundWindowPolicy`·`RefundService`·`RefundController`, 마이그레이션 `src/main/resources/db/migration/`, 12장 `CLAUDE.md`의 `docs/specs/`·`plans/`. 6~8장과 다르면 통일.
- 부록 A EARS 주어 "the Refund Service" — 위 EARS 주어 통일 항목에 포함.
- 정전에서 끌어낸 결정: PG 실패 뒤 재요청은 새 Idempotency-Key, 환불 내역 조회도 자기 서점만(아니면 403), 정확히 168시간은 기간 안, 계약 `reason` 필수, C1 문자 수·trim 규칙(11장 한정). 6~8장과 충돌 여부 확인.
- 앞 장 참조 가정: 6장(검사 질문 세 개, Ran the Builder 인가 관찰), 7장(TestSuiteBench, Netguru 규칙, skip style 경고, 부팅 실패 사례), 5장(설치 전 점검표 셋째 항목 = hooks/hooks.json 읽기), 2장(파일 수 세기 과제, Tessl), 1장(클로징 질문). 실제 앞 장에 있는지 확인, 없으면 참조 문장 수정.
- 9장 산문 약 8% 초과(10,759자).

## 묶음 C (6~8장) 저술가 보고 — 예제 세부의 기준
6장 `SPEC.md`가 책 전체 예제의 정본이다. 다른 장의 정전 밖 세부가 아래와 다르면 아래 쪽으로 통일한다.
- 경로·번호: `docs/specs/partial-refund/SPEC.md`, 규칙 R1~R10, 수용 기준 AC1~AC9, 결정 D1~D5.
- API: 성공 `201` + 본문(`refundId`, `amount`, `status`, `items`), 요청 형식 오류는 기존 API와 같은 400, 오류 본문 `code` 필드. `reason` 필수 자유 입력.
- 기준 시각: `delivered_at` = 2026-11-02T10:00:00+09:00, 11-09T10:00:00 수락, 10:00:01 거절 (정확히 168시간은 기간 안 — D와 일치).
- D2: `delivered_at` 없는 주문은 `422 REFUND_WINDOW_EXPIRED`. D3: PG 실패 뒤 재요청은 새 Idempotency-Key (D와 일치).
- 7장: `scripts/verify-refund.sh`, `scripts/db.sh`, 마이그레이션 `migrations/012_add_partial_refund.up/down.sql` ← D(9장)의 `src/main/resources/db/migration/`과 충돌. 하나로 통일 (Spring Boot 관례상 Flyway 경로를 쓰려면 7장도 바꿀지 editor 판단; 어느 쪽이든 책 전체 일관).
- `docs/plans/`(`plansDirectory`) ← D(12장 `CLAUDE.md`)의 `plans/`와 통일. Gradle `./gradlew`(D와 일치), 시드 주문 1001.
- 8장: 능력 `refunds`, 변경 `add-partial-refund`(아카이브 2026-11-19), `extend-refund-window`(2027-02-18), C2 델타 요구 11개·시나리오 15개, REMOVED 대상 "환불 사유". C3 필드 `reasonCode`, `memo`; 336시간 경계 2026-11-16T10:00:00.
- 6장 검사관 보고의 줄 번호(30, 70, 100, 105–106, 131)는 실린 SPEC.md 전문 줄과 연동 — 전문 수정 시 함께 수정.
- 8장 산문 약 7% 초과.
- 11장 네 벌 비교 ①②는 6·8장 final 문장으로 교체 (묶음 D 메모 참조).

## 묶음 D 사실 확인 후 editor 이관
- 11장 네 벌 비교는 6·8장 **draft** 기준으로 맞춤 — 6·8장 final에서 SPEC.md R2·D4 문장, 8장 `Requirement: 환불 기간` 시나리오, 줄 수(132/116/76/50)가 바뀌었으면 다시 맞출 것. 편집 주석 1개 남음(제거).
- 부록 A A.1~A.3 프롬프트 선택지 개수 "2~3개" vs 6·7장 "2~4개" 등 문구 차이 — 6·7장 final 기준으로 통일.
- 9장 그림 2(analyze = 만들기 전 관문, 공식) vs 12장 오프닝 GPTers 회고(analyze = 만든 뒤 전용) — 독자가 충돌로 읽지 않게 12장에 한 구절 보완.
- `isWithinWindow` 시그니처: 5장 `(Instant, Instant)` vs 10장 `(Instant deliveredAt)` — 통일.

## 묶음 C 사실 확인 후 editor 이관
- 6장 SPEC.md 확정판은 132줄(초안 130줄). 11장 비교표 줄 수와 네 벌 비교 ①②를 06·08 **final** 기준으로 다시 맞출 것.
- 8장 그림 2·캡션이 바뀜: MODIFIED에서 시나리오를 빠뜨리면 v1.17.0 `validate`가 오류, `archive`가 병합 거부. 11·12장 등에서 "시나리오가 소리 없이 사라진다"류 서술이 있으면 맞출 것.
- 8장 메인 스펙 제목 줄은 `# refunds Specification`.
- 부록 B: v1.17.0 실제 스킬 폴더 이름 `openspec-sync-specs`, `openspec-verify-change` 반영 검토.

## 표지 (epub-builder 참고)
- cover.png 완료 (HTML→headless Chrome 렌더, 원본 cover_source.html).
- 매니페스트 `cover_alt` 값: "어두운 청색 블루프린트 격자 위에 스펙 문서의 요구사항 줄이 앰버색 선을 따라 코드 줄로 이어지는 그림과 제목 '스펙 주도 개발'"
