# Community Research — PostgreSQL Bible

실무자·운영자 목소리. Hacker News, Reddit, 한국 기술 블로그, Medium 운영기, Korean PostgreSQL User Group.

## 1. 글로벌: MySQL→PostgreSQL 마이그레이션 통증

- **400M row 마이그레이션 후기 (Medium, 2026-03)**
  - 6개월 작업, 다운타임 18시간, 발견 버그 127개.
  - LIMIT 절 문법 차이로 모든 쿼리 수정 필요.
  - timezone 처리 차이로 47개 쿼리 깨짐.
  - 출처: <https://medium.com/@codewar_with_me/postgresql-vs-mysql-i-migrated-400m-rows-heres-what-actually-broke-7b7978051c35>

- **HN: “Leaving MySQL” (2021)** — Notion, Stripe 등 사례 토론.
  - <https://news.ycombinator.com/item?id=29455852>

- **HN: “Anyone made the jump from MySQL to PostreSQL?” (2019)**
  - 가장 자주 언급: 데이터 타입 풍부, json/jsonb, 윈도우 함수, CTE.
  - <https://news.ycombinator.com/item?id=20449731>

- **Rick Branson, “10 Things I Hate About PostgreSQL” (Medium)**
  - 인기 비판 글. MVCC bloat, replication 설정 복잡, secondary index amplification, connection 모델, upgrade pain.
  - 출처: <https://rbranson.medium.com/10-things-i-hate-about-postgresql-20dbab8c2791>

## 2. 글로벌: HOT incident & XID wraparound

- **HN: “PostgreSQL production incident caused by transaction ID wraparound”** (2025)
  - autovacuum이 일부 테이블에 명시적으로 꺼져 있어 wraparound protection 진입, 전체 클러스터 read-only. 수동 VACUUM FREEZE + long-running tx 종료로 복구. PG의 “알아서 잘 돌아간다”는 가정의 파탄 사례로 공유됨.
  - <https://news.ycombinator.com/item?id=47819305>, <https://www.sqlservercentral.com/articles/i-too-have-a-production-story-a-downtime-caused-by-postgres-transaction-id-wraparound-problem>

## 3. 글로벌: “Postgres가 세계를 먹어치우고 있다”

- Vonng/Pigsty의 ‘Postgres is eating the database world’가 HN에서 두 차례 frontpage(2024-03).
  - <https://news.ycombinator.com/item?id=39711863>, <https://news.ycombinator.com/item?id=39759539>
  - 토론 요지: ① “Just Use Postgres” 진영의 단순화 주장(MySQL+Kafka+RabbitMQ+ES+Mongo+Redis → 전부 PG로), ② “현실은 그 정도 단순하지 않다”는 반론(특히 Kafka 같은 throughput, ES 같은 검색 품질), ③ 확장 생태계가 PG의 진짜 moat라는 점에는 광범위한 합의.

## 4. 글로벌: 벡터 DB / RAG

- 사용자 보고: pgvector + HNSW로 5M 벡터 이하는 충분히 production. pgvectorscale로 50M까지 가능. dedicated 벡터 DB 없이도 RAG 시작 가능하다는 의견 다수.
  - 출처: <https://medium.com/@DataCraft-Innovations/postgres-vector-search-with-pgvector-benchmarks-costs-and-reality-check-f839a4d2b66f>, <https://dev.to/polliog/postgresql-as-a-vector-database-when-to-use-pgvector-vs-pinecone-vs-weaviate-4kfi>

- 반론: Pinecone/Qdrant는 hybrid filter + concurrency에서 여전히 우위. 10M+ 벡터 + 다중 필터면 dedicated 검토. 단, 가격 우위는 Postgres가 압도(75% 감소 사례).

## 5. 한국: 마이그레이션 경험담

- **Velog @melon03090** — Oracle → PostgreSQL 공공 시스템 고도화. 핵심 통증: Oracle 전용 문법(`DECODE`, `(+)` 외부 조인, `CONNECT BY`)을 명시적으로 PG에 맞게 전환. 단순 DDL 변환보다 SQL semantics 변환이 진짜 작업.
  - <https://velog.io/@melon03090/Oracle%EC%97%90%EC%84%9C-PostgreSQL%EB%A1%9C-%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98%ED%95%98%EB%A9%B0-%EA%B2%AA%EC%9D%80-%EB%AC%B8%EC%A0%9C%EC%A0%90-%EC%A0%95%EB%A6%AC>

- **Velog @peace_e** — 사이드 프로젝트를 MySQL → PostgreSQL.
  - 동기: 가게 DB가 늘어날 것 같아서 + JSONB와 인덱스 표현력. 쿼리만 바꿔도 성능 개선.
  - <https://velog.io/@peace_e/...>

- **Velog @this_summer** — “Part 1. PostgreSQL, 내가 널 왜 써야 하니?”
  - <https://velog.io/@this_summer/Part-1.-Postgresql-%EB%82%B4%EA%B0%80-%EB%84%90-%EC%99%9C-%EC%8D%A8%EC%95%BC-%ED%95%98%EB%8B%88>

- **Medium @맞추다(Julie)** — MySQL → PostgreSQL, array 타입을 쓰기 위해 전환.
  - <https://medium.com/%EB%A7%9E%EC%B6%94%EB%8B%A4-%ED%8C%80%EB%B8%94%EB%A1%9C%EA%B7%B8/mysql%EC%97%90%EC%84%9C-postgresql%EC%9C%BC%EB%A1%9C-%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98%ED%95%98%EA%B8%B0-b10c3abec312>

## 6. 한국: 카카오·기업 사례

- **tech.kakao.com (finn.h)** — “PostgreSQL to ES: (1) Kafka Connect CDC 파이프라인 구성”
  - 카카오 클린플랫폼 팀이 컨텐츠 모니터링 시스템에서 PG → Elasticsearch 동기화에 Kafka Connect + CDC를 도입한 사례.
  - 본문 인용은 한계(WebFetch가 nav만 받음). 제목·존재 사실까지만 인용 가능.
  - <https://tech.kakao.com/posts/776>

- **AWS 기술블로그(한국)** — 카카오스타일 Bedrock 활용, 당근페이 BroQuery(Text-to-SQL). PG 자체보다 PG 데이터 위 분석 사례.
  - <https://aws.amazon.com/ko/blogs/tech/kakaostyle-leverage-genai-with-amazon-bedrock/>
  - <https://aws.amazon.com/ko/blogs/tech/daangnpay-text-to-sql-1/>

- **GG FACTORY Tech** — PostgreSQL GUI 도구 소개 등 일반 글.
  - <https://www.kakao.gg/blog/tech/postgresql%EC%9D%84-%EC%9C%84%ED%95%9C-gui%EA%B7%B8%EB%9E%98%ED%94%BD-%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4-%ED%88%B4-%EC%86%8C%EA%B0%9C>

- **iting.co.kr** — re:Invent 2025 정리: Oracle → Aurora PostgreSQL 마이그레이션 핵심 가이드. AWS DMS, Babelfish, SCT 사용 노하우.
  - <https://iting.co.kr/reinvent-techblog-2025-post-111/>

- **EDB 코리아 블로그** — 레거시 DB(특히 Oracle) → PostgreSQL 마이그레이션 변화 관리.
  - <https://edbkorea.com/blog/...>

- **컴퓨터월드 기고** — “오픈소스 DB 전성시대, PostgreSQL을 선택해야 하는 이유”. 2024 StackOverflow 49% 1위 등 시장 통계.
  - <https://www.comworld.co.kr/news/articleView.html?idxno=51049>

- **다음 뉴스(2026-01)** — “오라클 중심 DB 시장에 균열…포스트그레SQL이 만든 변화” — 국내 매체 보도.
  - <https://v.daum.net/v/20260120141615146>

## 7. 한국: 사용자 모임 / 자료

- **PostgreSQL Korea (postgresql.kr)** — 공식 한국 커뮤니티. PGDay.Seoul 시리즈(2019, 2024…). 한국어 매뉴얼 번역.
  - <https://postgresql.kr/>, <https://pgday.postgresql.kr/>

- **PostgreSQL-Korea/pgdoc-kr (GitHub)** — 한국어 안내서.
  - <https://github.com/PostgreSQL-Korea/pgdoc-kr>

- **SKAI Worldwide Tech Blog** — 비트나인 인수합병 후의 한국 PG 전문기업. 강점/오라클 사용자 가이드/커뮤니티 버전 기술지원 필요성 시리즈 다수.
  - <https://blog.skaiworldwide.com/516>, <https://blog.skaiworldwide.com/550>, <https://blog.skaiworldwide.com/589>, <https://blog.skaiworldwide.com/616>

- **PGTS (비트나인)** — 한국 PG 기술지원 상용 서비스.
  - <https://bitnine.net/pgts/>

- **투이컨설팅** — “클라우드에서는 오픈소스 DBMS를 [1부] PostgreSQL 소개” — 컨설팅 관점.
  - <https://2e.co.kr/news/articleView.html?idxno=210373>

## 8. 한국: 분산/스케일링 사례

- **Medium @scalalang2 (취미로 논문 읽는 그룹)** — Citus 소개. 익스텐션 API로 PG 호환 유지하면서 분산. e-commerce/IoT/analytics에 적합.
  - <https://medium.com/rate-labs/citus-postgres-%EB%B6%84%EC%82%B0-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-a-z-%EC%86%8C%EA%B0%9C-8f2fe3dd3428>

- **postgresql.kr 블로그** — 자료 분산 처리 Sharding 이야기.
  - <https://postgresql.kr/blog/postgresql-sharding.html>

- **Medium @blog.thecloer (당근마켓 클론)** — 당근마켓 비즈니스 ERD 분석 (실제 당근마켓 운영 사례는 아님, 클론).
  - <https://blog.thecloer.com/14>

## 9. 한국: PostGIS / 지도

- **Velog @dailylifecoding** — PostGIS 성능 이슈 개선 사례 기록(1).
  - <https://velog.io/@dailylifecoding/PostGIS-%EC%84%B1%EB%8A%A5-%EC%9D%B4%EC%8A%88-%EA%B0%9C%EC%84%A0-%EC%82%AC%EB%A1%80-%EA%B8%B0%EB%A1%9D1>

- **Velog @octo-5** — 당근마켓 클론에서 지역 정보 DB 선택 — PostGIS 채택 이유.
  - <https://velog.io/@octo-5/...>

## 10. 한국: HA / 운영

- **Velog @kr_jkjung** — PostgreSQL HA 솔루션 비교 (Patroni, repmgr, pg_auto_failover).
  - <https://velog.io/@kr_jkjung/PostgreSQL-%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1HA-%EC%86%94%EB%A3%A8%EC%85%98-%EB%B9%84%EA%B5%90>

## 11. 한계

- 토스/우아한형제들/네이버/라인의 PG 도입에 대한 공식 1차 후기는 본 리서치 라운드에서 직접 발견 못함. 후속 라운드에서 각 사 기술 블로그(`techblog.lycorp.co.kr`, `techblog.woowahan.com`, `toss.tech`, `medium.com/naverpay`) 직접 사이트 검색 필요.
- 카카오의 PG→ES CDC 글은 본문 본격 인용 못함. 후속에 직접 페이지를 다른 경로로 가져와 wal2json/pgoutput 선택 근거 확인 필요.
- Reddit `r/PostgreSQL`은 일반 토론 위주라 specific quotable thread는 본 라운드에서 제한적.
- pgsql-general mailing list 인용은 본 라운드에서 미수집 — 라이브 thread URL 필요.
