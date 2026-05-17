# 커뮤니티 리서치 메모: 한국·일본·영문 실무자 경험담

## 1. 우아한형제들 기술블로그

- **MySQL을 이용한 분산락으로 여러 서버에 걸친 동시성 관리** — `GET_LOCK()`/`RELEASE_LOCK()` 함수로 user-level named lock 분산락 구현. 락 획득용 커넥션 풀과 비즈니스 로직용 커넥션 풀을 **분리**하는 패턴이 핵심 학습 포인트. SELECT FOR UPDATE는 record 자체를 잠그므로 다른 로직과 락 충돌을 일으킬 수 있는 반면, named lock은 record와 무관해 자유도가 높음. MySQL 5.7 이전에서는 동시에 여러 GET_LOCK 호출 시 이전 락이 해제되는 버그 주의. https://techblog.woowahan.com/2631/
- **MySQL 환경의 스프링부트에 하이버네이트 배치 설정해 보기** — `jdbc.batch_size`, `order_inserts`, `rewriteBatchedStatements=true`까지 켜야 진짜로 batch INSERT가 만들어진다는 점, IDENTITY ID 전략으로는 batch가 동작하지 않는다는 교훈을 실측 그래프와 함께 정리. https://techblog.woowahan.com/2695/
- **Aurora MySQL vs Aurora PostgreSQL** — 200GB 테이블 인덱스 생성 시 Aurora MySQL은 1시간 이상, Aurora PostgreSQL은 40분 안에 완료. PostgreSQL의 Partial Index가 부분 인덱스로 크기·관리 부담을 줄여준다는 비교가 흥미로움. 운영 관점에서 Aurora MySQL의 large index DDL은 여전히 부담. https://techblog.woowahan.com/6550/

## 2. 카카오 / 카카오엔터 tech.kakao.com

- **MySQL InnoDB의 Adaptive Hash Index 활용** — B-Tree 한계(특히 randon single-key lookup)를 보완하는 AHI의 작동 원리와 효과. AHI를 끄면 ‘메인 키’ lookup이 느려지는 워크로드가 존재. https://tech.kakao.com/posts/319
- **MySQL InnoDB Log에 대한 이해** — redo log/checkpoint 흐름과 commit latency, `innodb_flush_log_at_trx_commit`에 따른 trade-off. https://tech.kakao.com/posts/721
- **MySQL Ascending index vs Descending index** — 8.0의 descending index 지원으로 ORDER BY a ASC, b DESC 같은 혼합 정렬을 인덱스로 처리 가능. https://tech.kakao.com/posts/351
- **MySQL ALTER DDL 수행 방식에 대한 이해 / Instant DDL Algorithm** — `INPLACE`, `COPY`, `INSTANT` 알고리즘 비교. 8.0.12부터 컬럼 추가가 메타데이터만 변경하면 끝나는 INSTANT DDL의 한계(테이블 마지막에만 추가 가능 등) 학습. https://tech.kakao.com/posts/703 , https://tech.kakao.com/posts/731
- **kakao 오픈소스 MRTE — MySQL Realtime Traffic Emulator** — 운영 트래픽을 다른 환경으로 미러링해 업그레이드/튜닝을 안전하게 검증하는 도구. 메이저 업그레이드를 다루는 챕터에서 인용. https://tech.kakao.com/posts/311

## 3. 토스 (toss.tech / slash 컨퍼런스)

- **MYSQL HA & DR Topology — SLASH 21** — 토스의 MySQL 다중 리전 DR 구성, GTID 기반 페일오버, MHA/orchestrator 활용을 발표. https://toss.im/slash-21/sessions/2-3
- (참고) toss.tech에는 MySQL 단독 글보다는 결제·송금 서비스의 DB 운영기·동시성 사례가 산재. 검색 시 SLASH 발표 영상에서 더 풍부한 정보가 나옴.

## 4. LINE Engineering

- **Performance impact of MySQL performance-schema-instruments** — `innodb_metrics`는 ON/OFF가 TPS에 거의 영향 없지만 `performance_schema`의 모든 instrument를 ON으로 켜면 TPS가 약 15% 떨어진다는 실측. 운영에서 PS를 어떻게 선택적으로 켤지에 대한 가이드. https://engineering.linecorp.com/en/blog/mysql-research-performance-schema-instruments
- **MySQLエキスパートyoku0825 인터뷰** — DBA로서 커리어 패스와 DBA-개발자 분업 트렌드 변화. 운영 챕터 도입부 이야기 소재로 활용 가능. https://engineering.linecorp.com/en/interview/mysql-yoku0825

## 5. velog / 개인 블로그 — 한국 실무자 경험담

- **MySQL 인덱스 성능 개선하기 - 커버링 인덱스** (rnjsrntkd95) — `SELECT *` 대신 인덱스 컬럼만 SELECT해 covering index로 만들면 같은 인덱스라도 IO가 급감하는 실험. https://velog.io/@rnjsrntkd95/MySQL-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-%EC%BB%A4%EB%B2%84%EB%A7%81-%EC%9D%B8%EB%8D%B1%EC%8A%A4
- **슬로우 쿼리 개선기** (bruni_23yong) — promotion_option 테이블 promotion_id에 인덱스가 없어 LEFT JOIN 풀스캔 → 인덱스 추가로 6초 → 0.02초. 옵티마이저가 JOIN 컬럼에 만든 인덱스 우선 사용해 다른 인덱스를 무시한 사례까지 포함. https://velog.io/@bruni_23yong/%EC%8A%AC%EB%A1%9C%EC%9A%B0-%EC%BF%BC%EB%A6%AC-%EA%B0%9C%EC%84%A0%EA%B8%B0
- **MySQL 성능 개선을 위한 프로파일링 1편: 슬로우 쿼리 로그** (breadkingdom) — `long_query_time`, `log_queries_not_using_indexes`, mysqldumpslow/pt-query-digest 활용 흐름. https://velog.io/@breadkingdom/MySQL-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%EC%9D%84-%EC%9C%84%ED%95%9C-%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%A7%81-1
- **EXPLAIN ANALYZE 해석법** (wisepine) — 실측 자료 기반 EXPLAIN ANALYZE 트리 읽기. 한국어 학습자에게 친절. https://velog.io/@wisepine/MySQL-%EC%8A%AC%EB%A1%9C%EC%9A%B0%EC%BF%BC%EB%A6%AC-%EC%9E%A1%EB%8A%94-%EB%AA%85%EB%A0%B9%EC%96%B4-EXPLAIN-ANALIZE-%ED%95%B4%EC%84%9D%EB%B2%95
- **MySQL Explain 인덱스 추가 및 QueryDSL 쿼리 튜닝** (geon_km) — QueryDSL이 만든 SQL을 EXPLAIN으로 검증하고 인덱스 힌트/조회 컬럼 조정으로 튜닝한 실전기. JPA 사용자에게 직접 와닿는 케이스. https://velog.io/@geon_km/MySQL-Explain-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%B6%94%EA%B0%80-%EB%B0%8F-QueryDSL-%EC%BF%BC%EB%A6%AC-%ED%8A%9C%EB%8B%9D
- **MySql의 Named Lock을 활용한 동시성 이슈 해결하기** (komment), **MySQL 네임드 락으로 분산 환경에서의 동시성 이슈를 해결해보자!** (haon.blog) — 우아한형제들 패턴을 자기 프로젝트에 적용하며 만난 함정(connection 누수, lock timeout) 정리. https://haon.blog/database/named-lock/
- **MySQL InnoDB lock & deadlock 이해하기 — Knowledge Logger** — gap lock·next-key lock 시나리오 한국어 정리, REPEATABLE READ vs READ COMMITTED 비교 그림 풍부. https://www.letmecompile.com/mysql-innodb-lock-deadlock/

## 6. OKKY / 한국어 Q&A

- **OKKY: mysql 인덱스 중복으로 걸려 있는건가요?** — 복합 인덱스와 단일 인덱스 중복 설계 질문. 실무자가 자주 빠지는 함정. https://okky.kr/articles/710070
- velog "쿼리 속도 개선기" 게시물은 OKKY에서 답을 얻어 11초 → 0.1초로 단축한 사례를 공유 — 복합 인덱스 컬럼 순서 조정이 답이었다는 결론. https://velog.io/@gkh4302/%EC%BF%BC%EB%A6%AC-%EC%86%8D%EB%8F%84-%EA%B0%9C%EC%84%A0%EA%B8%B0

## 7. 영문 커뮤니티 — Reddit / Hacker News / Skeema

- **Skeema: Five Surprises in MySQL 8.4 LTS (2024)** — 8.4 LTS에서 adaptive hash index, change buffer 기본 OFF, foreign key가 unique key 정확 일치 요구 등 깜짝 변경. 8.4로 업그레이드하기 전 반드시 체크할 항목. https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- **Jepsen: MySQL 8.0.34 분석** — REPEATABLE READ에서 fractured read, lost update 같은 anomaly가 여전히 발생함을 실험으로 보임. 비즈니스 크리티컬 트랜잭션에서 READ COMMITTED + 명시적 락 / SERIALIZABLE을 고려해야 하는 근거. https://jepsen.io/analyses/mysql-8.0.34 (HN 토론: https://news.ycombinator.com/item?id=38695750)
- **Medium "Unlocking MySQL: Locks and deadlock"** — INSERT ON DUPLICATE KEY UPDATE의 흔한 데드락 케이스와 회피 패턴(고정 정렬, lock 순서) 정리. https://medium.com/@carolyn_chen/unlocking-mysql-real-case-studies-on-deadlocks-and-their-causes-2faab5bc0920

## 8. 일본 / Qiita 계열 (간접 인용)

- yoku0825(요쿠하치)·MySQL Casual 슬랙 등에서 운영 사례가 활발. LINE 인터뷰가 대표적이며, Qiita에서는 `gh-ost`, `pt-online-schema-change`로 무중단 DDL을 다룬 글이 풍부.

## 9. 안티패턴/논쟁 모음

- **Soft Delete 논쟁** — brandur.org는 "거의 가치 없다", Brent Ozar/Cultured Systems는 "조건부 적용 가능". 합의점: 도메인 요구가 명확할 때만, 그리고 unique/FK 무결성을 다룰 도구가 있을 때만. https://brandur.org/soft-deletion , https://www.brentozar.com/archive/2020/02/what-are-soft-deletes-and-how-are-they-implemented/
- **JPA만 쓸까 vs native SQL 적극 활용** — Vlad Mihalcea, Thorben Janssen은 "JPA로 도메인, native로 보고서/대량처리" 하이브리드를 권고. 반대 극단은 JPA를 버리고 JdbcTemplate/MyBatis만 쓰는 SQL-mapper 진영. https://vladmihalcea.com/java-data-access-technology/
- **JPA에서 페이지네이션** — JOIN FETCH + Pageable 안티패턴이 가장 자주 인용. EntityGraph + keyset 페이지네이션이 모범. https://thorben-janssen.com/offset-and-keyset-pagination-with-spring-data-jpa/
- **RDS vs Aurora 선택 기준 논쟁** — Percona/Bytebase는 "Aurora가 자동 페일오버·읽기 확장에 절대적 우위지만 IO 비용 모델/락-인을 감수해야 함", devrocks 등은 "단순 워크로드는 RDS로 충분, Aurora는 오버스펙"이라는 입장. 분기점은 (1) 읽기 트래픽 비대칭, (2) 페일오버 RTO 요구, (3) IO bound 워크로드 여부. https://www.percona.com/blog/when-should-i-use-amazon-aurora-and-when-should-i-use-rds-mysql/
