# PostgreSQL 종합 바이블 — MySQL 베테랑 개발자·DBA·Tech Lead를 위한 v17/v18 실전 가이드

> MySQL 베테랑·DBA·Tech Lead 세 사람을 정조준한 PostgreSQL v17/v18 종합 바이블 — 정체성, 활용 9가지, 운영 9가지를 한 권에 담았다.

- **저자:** Toby-AI
- **버전:** v1.0.0
- **발행일:** 2026-05-18
- **언어:** 한국어 (ko)
- **분량:** 25장 + 부록 1 (Part 4부 구성) / 본문 약 70만 자

## 이 책은 무엇인가

PostgreSQL은 2024년 Stack Overflow 개발자 설문에서 가장 많이 쓰이는 데이터베이스 1위에 올랐다. 한국에서도 공공·금융·플랫폼이 차례로 PG로 옮기고 있고, AWS·GCP·신생 매니지드 벤더들의 로드맵이 모두 Postgres-호환을 향한다. "Just Use Postgres"라는 말이 농담이 아니게 된 시점, 즉 PG로 검색·벡터·GIS·이벤트·OLAP·API 백엔드까지 다 끌고 갈 수 있다는 주장이 정말 현실에서 검증되고 있는 시점에 — 이 책은 그 흐름을 한 권에 정리한다.

다만 이 책은 "Postgres 만세"를 외치는 책이 아니다. 25장 전체에서 일관되게 묻는 질문은 두 가지다. **"PG로 가도 되는 선은 어디까지인가?"** 그리고 **"옮긴 뒤의 운영 무게는 얼마인가?"** 두 질문에 정직하게 답하기 위해 fork 프로세스 모델·append-only MVCC·HOT·WAL·SSI라는 다섯 가지 토대를 정면으로 다루고, 4억 row를 옮긴 한국 후기와 카카오·당근페이·공공의 실제 결정 사례를 본문으로 끌어올렸다.

다른 PostgreSQL 책과의 차이는 두 가지다. 첫째, **MySQL/Oracle 사용 경험을 가진 독자를 기본값으로 가정한다.** InnoDB의 사고방식이 손에 익은 사람이 어디서 처음 미끄러지는지(2장의 여덟 가지 차이)를 책 전체의 지도로 삼는다. 둘째, **v17/v18 시대의 책이다.** failover slot이 logical replication을 production 등급으로 끌어올렸고, planner statistics 보존이 메이저 업그레이드의 성능 절벽을 지웠고, RETURNING OLD/NEW와 temporal constraint와 UUIDv7이 SQL 표현력의 결을 한 단계 더 풍부하게 만들었다. 이 변화들이 작은 신호처럼 본문 곳곳에 박혀 있다.

## 누구를 위한 책인가

세 페르소나를 정조준한다. 책장에 꽂힐 자리가 셋이라는 뜻이다.

- **MySQL을 오래 써온 베테랑 개발자.** 진입 상태는 "InnoDB의 사고방식이 손에 익어 있고, LIMIT·timezone·MVCC의 차이가 마이그레이션 D-1에서 어떻게 폭발하는지는 아직 본 적 없는" 사람. 출구 상태는 PG의 fork 모델·VACUUM·HOT·SSI를 InnoDB와 대비해 설명할 수 있고, JSONB·array·확장성을 시스템 설계에 녹일 수 있으며, 4억 row·127개 버그의 한국 마이그레이션 케이스를 자기 시스템에 매핑할 수 있는 사람.
- **PostgreSQL 운영을 시작하는 DBA.** 진입 상태는 "autovacuum이라는 단어를 들으면 어깨가 한 번 굳고, replication slot의 ghost를 한 번쯤 만나본" 사람. 출구 상태는 autovacuum 튜닝, XID wraparound 예방, Patroni/pg_auto_failover 선택, pgBackRest 운영, 17 failover slot의 의미를 알고 페일오버 훈련을 설계할 수 있으며, pgaudit·RLS·SSL/TLS·CVE 추적으로 보안 의사결정까지 가능한 사람.
- **메인 DB 의사결정을 책임지는 Tech Lead.** 진입 상태는 "'PG로 검색·벡터·GIS·이벤트 다 된다더라'는 소문을 들고 의사결정을 내려야 하는" 사람. 출구 상태는 9개 활용 시나리오에서 "PG로 가도 되는 선"과 "dedicated가 필요한 선"을 근거를 갖고 그을 수 있고, RDS/Aurora/AlloyDB/Supabase/Neon 의사결정을 표로 정리할 수 있으며, "Aurora는 진짜 PG인가" 논쟁에 자기 답을 갖는 사람.

세 사람이 같은 책을 본다는 게 무리한 일이 아니도록, Part 1과 Part 2를 공통의 출발선으로 두었다. Part 3와 Part 4는 페르소나별 추천 경로(각 12~15장)를 1장 마지막 절에 표로 정리해두었다.

## 무엇을 얻게 되는가

- fork 프로세스 모델·append-only MVCC·HOT·WAL·SSI라는 PG 정체성의 다섯 토대를 정면으로 다룬다.
- JSON·검색·GIS·벡터·이벤트·OLAP·API 백엔드까지 9가지 활용 시나리오를 "PG로 가도 되는 선"과 함께 그어준다.
- 4억 row·6개월·다운타임 18시간·발견 버그 127개의 한국 마이그레이션 케이스를 분해해, 자기 시스템에 매핑할 수 있게 만든다.
- autovacuum·XID wraparound·페일오버·CVE 추적까지 DBA의 야간 호출 영역을 운영 매뉴얼로 잡아준다.
- RDS·Aurora·AlloyDB·Supabase·Neon 등 매니지드 PG 의사결정 트리와 "Aurora는 진짜 PG인가" 논쟁의 정직한 결론을 담는다.
- 카카오 클린플랫폼 CDC, 카카오스타일 Bedrock, 당근페이 BroQuery, 공공 Oracle→PG 4건 등 한국 현장 사례를 본문으로 끌어올린다.

## 차례

### Part 1. 만남 — 왜 지금 PostgreSQL인가

1. PostgreSQL은 어떻게 데이터베이스의 중심으로 왔나 — 1986년 버클리에서 2026년 메인 DB 자리까지, 그 30년의 궤적.
2. MySQL 베테랑이 가장 먼저 부딪히는 여덟 가지 — InnoDB 사고방식이 처음 미끄러지는 지점을 한 장의 지도로.
3. v17과 v18, 무엇이 바뀌었나 — failover slot·planner statistics 보존·UUIDv7이 만든 운영 무게의 재정의.

### Part 2. 정체성 — PostgreSQL의 진짜 모습

4. 프로세스 모델과 메모리 — fork가 만드는 모든 것을 PgBouncer 의존성까지 따라간다.
5. MVCC와 VACUUM — append-only가 치르는 값, bloat의 기원과 운영 결말까지.
6. HOT과 fillfactor — 비용을 깎는 단일 최적화의 원리와 한계.
7. WAL과 SSI — 모든 기능의 토대인 두 메커니즘을 정직하게.

### Part 3. 활용 — 아홉 가지 시나리오

8. SQL 표준과 트랜잭션 — RDB 정통의 깊이, 그리고 PG가 표준을 어떻게 해석하는가.
9. JSON DB로서의 PostgreSQL — MongoDB를 대체할 수 있는 선과 없는 선.
10. 전문 검색 — Elasticsearch 없이 갈 수 있는 거리와 그 끝.
11. GIS와 PostGIS — 공간 데이터의 산업 표준이 된 이유.
12. 벡터 DB와 RAG 백엔드 — pgvector·pgvectorscale로 만드는 한 트랜잭션 RAG.
13. 이벤트·큐·실시간 — LISTEN/NOTIFY로 Kafka를 미루는 법과 한계.
14. FDW·CDC·동기화 — 데이터 경계를 허무는 세 가지 방식.
15. 분석·OLAP·시계열 — Citus·TimescaleDB·DuckDB와의 역할 분담.
16. API 백엔드 — DB가 백엔드가 되는 PostgREST·Supabase·pg_graphql 패턴.

### Part 4. 운영 — DBA의 일

17. MySQL/Oracle → PostgreSQL 마이그레이션 실전 — 4억 row·6개월·다운타임 18시간·127 버그의 해부.
18. VACUUM과 XID wraparound — 진짜로 멈추는 사고와 예방 매뉴얼.
19. 백업·복구·PITR — pgBackRest·Barman·WAL-G 운영 비교.
20. HA와 페일오버 — Patroni·pg_auto_failover·v17 failover slot의 의미.
21. Connection pooling과 모니터링 — PgBouncer·pg_stat_statements 표준 셋업.
22. 보안과 감사 — pgaudit·RLS·SSL/TLS·scram-sha-256·CVE 추적.
23. 성능 튜닝 종합 — 인덱스 매트릭스·EXPLAIN·함정 6가지·파티셔닝.
24. 클라우드 PostgreSQL — 벤더 매트릭스와 "Aurora는 진짜 PG인가" 절.
25. 한국 사례와 다음 한 걸음 — 카카오·당근페이·공공의 결정을 의사결정 표로.

### 부록

- 부록 A. 참고문헌 — URL이 살아 있는 1차 자료 모음.

## 저자 소개

Toby-AI는 book-writer 하네스 위에서 동작하는 AI 저자 페르소나다. 리서치(웹·논문·커뮤니티)·계획·리뷰·챕터 저술·스타일 점검·편집·표지 디자인·EPUB 빌드를 멀티 에이전트로 조율한 결과를 하나의 저자명으로 묶는다. 이 책의 본문은 *toby-book-writing-style.md*에 정의된 평어체 기반 한국어 스타일을 따르며, 청유형·수사적 질문·상황 가정·감정적 공감 표현을 적극 활용해 독자와 함께 사고하는 톤을 지향한다.

## 책 정보

- 파일: `PostgreSQL-종합-바이블-—-MySQL-베테랑-개발자·DBA·Tech-Lead를-위한-v17v18-실전-가이드-v1.0.0.epub`
- 형식: EPUB 3 (ko)
- 라이선스: Creative Commons BY-NC-SA 4.0
- 식별자: `urn:uuid:c5e65a05-c213-49b6-9af3-bff72a2d0b71`
- 하네스 버전: book-writer v1.2.0
- 표준 검증: epubcheck 통과
