# 종장. 책을 덮으며

오래전 이야기다. 슬로우 쿼리 알람을 처음 받았을 때, 어디서부터 손대야 할지 몰라 DBA 동료 자리로 달려갔다. 그는 몇 줄의 EXPLAIN 출력을 보고 5분 안에 원인을 짚었다. "인덱스가 여기서 안 타요." 그때 그 사람이 보는 것을 나는 왜 못 보는지가 부러웠다. 기술의 차이라기보다 관점의 차이였다.

이 책은 그 관점을 배우는 책이었다.

---

## 13개 챕터의 의사결정 카드

책 전체를 한 장의 카드로 요약해보자.

| 챕터 | 핵심 질문 | 기억할 판단 기준 |
|------|-----------|-----------------|
| 1장 | 왜 지금 갈무리하는가 | 8.4 LTS의 default 변경이 우리 워크로드에 영향을 주는지 |
| 2장 | InnoDB 안에서는 무슨 일이 | 버퍼풀이 클수록 디스크 IO가 줄고, undo 로그가 늘수록 MVCC 비용이 오른다 |
| 3장 | 어떤 락이 어디에 걸리나 | RR은 next-key lock으로 phantom을 막고, RC는 gap lock이 없어 데드락이 줄지만 phantom은 허용한다 |
| 4장 | 어떤 인덱스를 어떤 순서로 | equality → range → sort, 고카디널리티 앞. 커버링 인덱스로 back-to-table 제거 |
| 5장 | EXPLAIN ANALYZE를 어디서 읽나 | 안쪽 노드부터. estimate와 actual 괴리가 크면 통계 갱신 |
| 6장 | SQL이 할 수 있는 것 | 윈도우 함수와 CTE로 집계를 SQL 안에서 처리하면 왕복이 줄고 가독성도 오른다 |
| 7장 | JSON을 어디까지 쓸 수 있나 | functional index 또는 generated column으로 JSON path도 인덱싱 가능 |
| 8장 | 스키마와 도메인의 거리 | PK 전략, soft delete, FK 범위는 도메인 요구와 MySQL 제약 사이의 절충이다 |
| 9장 | JPA가 보여주는 것과 실제 SQL | N+1은 fetch graph로, 깊은 페이지는 keyset으로, 배치는 JdbcTemplate batchUpdate로 |
| 10장 | JPA 한계 너머 | 배치 INSERT 3종 세트, 청크 분할 UPDATE, named lock 커넥션 풀 분리 |
| 11장 | RDS vs Aurora 분기점 | 읽기 확장·페일오버 RTO·IO 집약도·락-인 여부, 네 가지 기준으로 판단 |
| 12장 | 운영의 신호를 어떻게 듣나 | 버퍼풀 히트율, Threads_running, 락 대기, 복제 lag. 백업은 복구 테스트가 진짜 백업 |
| 13장 | 모든 도구를 어떻게 연결하나 | 도메인 → 스키마 → 인덱스 → 동시성 → 운영의 순서는 도메인이 달라도 변하지 않는다 |
| 14장 | 메이저 업그레이드를 넘는 법 | pt-upgrade → 인증 플러그인 → default 변경 → Blue/Green → escape hatch |

---

## 다음 주 월요일, 세 가지 실험

책을 읽는 것과 적용하는 것 사이에는 언제나 거리가 있다. 그 거리를 줄이는 가장 빠른 방법은 지금 당장 작은 것을 하나 해보는 것이다.

다음 주 월요일, 세 가지 중 하나를 해보자. 세 가지 다 할 필요는 없다. 하나만 해도 충분하다.

**실험 1: 슬로우 쿼리 로그를 켜고 pt-query-digest를 돌려보자.**

운영 서비스에 슬로우 쿼리 로그가 켜져 있지 않다면 지금 켜보자. `long_query_time = 1`로 설정하고 하루 쌓인 로그를 `pt-query-digest`로 분석해보자. 가장 실행 시간 합계가 높은 쿼리 하나를 `EXPLAIN ANALYZE`로 분해해보자. 예상과 다른 실행 계획을 발견하면 그것이 시작이다.

**실험 2: 배치 INSERT 성능을 측정해보자.**

애플리케이션에서 `saveAll()`을 쓰는 코드가 있다면, 세 가지 설정(`jdbc.batch_size`, `order_inserts`, `rewriteBatchedStatements=true`)이 모두 켜져 있는지 확인하자. ID 전략이 IDENTITY라면 그것도 확인하자. 설정 전후의 실행 시간을 비교해보자. 차이가 없다면 왜 없는지 확인하는 것도 좋은 공부다.

**실험 3: PITR 리허설을 한 번 해보자.**

스테이징 환경에서 백업 스냅샷으로부터 복구하는 것을 한 번 실제로 해보자. RDS/Aurora라면 AWS 콘솔에서 "restore to point in time"을 클릭해보자. 복구에 얼마나 걸리는지 시간을 재보자. 그것이 우리 서비스의 실제 RTO다.

---

## 감사의 말과 참고 문헌 안내

이 책은 많은 엔지니어들의 공개된 경험 위에 서 있다.

우아한형제들이 named lock 분산락과 배치 INSERT 개선 경험을 기술블로그에 공유하지 않았다면 10장이 지금처럼 생생하지 않았을 것이다. 토스 SLASH 21에서 DR 토폴로지를 설명해준 발표자, LINE Engineering에서 performance_schema의 실제 영향을 측정한 엔지니어들에게 감사한다. 카카오 테크 블로그의 InnoDB 내부 시리즈도 큰 도움이 됐다.

이 책에서 자주 인용한 Vlad Mihalcea의 "High-Performance Java Persistence"는 JPA를 진지하게 다루는 모든 개발자에게 권하는 책이다.

더 깊은 곳을 향해 가고 싶다면 다음 참고 문헌들이 기다리고 있다.

**도서**
- Schwartz, B. 외 (2012) *High Performance MySQL, 3rd Edition*, O'Reilly
- Aubin, J., Bell, C. (2021) *High Performance MySQL, 4th Edition*, O'Reilly
- 백은빈·이성욱 (2021) *Real MySQL 8.0* 1·2권, 위키북스

**학술 논문 — 트랜잭션 고급 독자에게**
- Cahill, M. (2009) "Serializable Isolation for Snapshot Databases" — MySQL의 RR이 진정한 직렬성이 아닌 이유, Snapshot Isolation의 수학적 기반
- Neumann, T. 외 (2015) "Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems" (SIGMOD) — MVCC 구현의 현대적 접근
- Jepsen 분석 (MySQL 8.0.34) — https://jepsen.io/analyses/mysql-8.0.34

---

## 마지막으로

책을 덮고 나면 잊어버릴 것들이 있다. 괜찮다. 기억나지 않을 때 다시 꺼내 보면 된다. 하지만 한 가지만 마음에 남겨두자.

**데이터베이스는 말이 없다.** 우리가 먼저 물어봐야 대답한다. 슬로우 쿼리 로그를 켜고, EXPLAIN ANALYZE를 돌리고, 복제 lag을 확인하고, 분기마다 PITR을 리허설하는 것 — 이것이 DB에게 먼저 말을 거는 방법이다.

DBA가 되지 않아도 된다. DBA처럼 생각하는 스프링 개발자이면 충분하다. 그 생각의 출발점은 "왜 그럴까?"라는 질문 하나다.

부디 다음 주 월요일의 실험이 이 책의 진짜 마지막 챕터가 되길 바란다.

---

## 참고 자료

- Cahill, M. (2009) *Serializable Isolation for Snapshot Databases*: https://ses.library.usyd.edu.au/bitstream/handle/2123/5353/michael-cahill-2009-thesis.pdf
- Jepsen — MySQL 8.0.34 분석: https://jepsen.io/analyses/mysql-8.0.34
- 백은빈·이성욱 (2021) *Real MySQL 8.0*: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=278488709
- Vlad Mihalcea — High-Performance Java Persistence: https://vladmihalcea.com/books/high-performance-java-persistence/
