# 논문·권위 자료 메모: InnoDB·MVCC·B+Tree·옵티마이저

## 1. MVCC / Snapshot Isolation

- **Cahill, M. (2009)** *Serializable Isolation for Snapshot Databases*. PhD thesis, University of Sydney. InnoDB 스토리지 매니저를 직접 패치해 Serializable Snapshot Isolation(SSI)을 구현·평가. SI vs S2PL vs SSI를 sibench, SmallBank, TPC-C++로 벤치마크. https://ses.library.usyd.edu.au/bitstream/handle/2123/5353/michael-cahill-2009-thesis.pdf
- **Neumann, T., Mühlbauer, T., Kemper, A. (2015)** *Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems* (SIGMOD). HyPer 기반 MV2PL의 설계와 벤치. MVCC가 인덱스 트래버스에 미치는 영향(visibility check) 분석. https://db.in.tum.de/~muehlbau/papers/mvcc.pdf
- **Bornea, M., Hodson, O., Elnikety, S., Fekete, A. (2011)** *One-Copy Serializability with Snapshot Isolation under the Hood* (ICDE). Precisely Serializable Snapshot Isolation을 InnoDB 5.1.31에 구현. ESSI, PSSI, SI, S2PL 비교 실험.
- **Larson, P.-Å. 외 (Microsoft Research, 2011)** *High-Performance Concurrency Control Mechanisms for Main-Memory Databases*. MVCC와 OCC의 메인메모리 DB 적용 논의 — InnoDB의 disk 기반 MVCC와 대조 학습 자료. https://www.microsoft.com/en-us/research/wp-content/uploads/2011/12/MVCC-published-revised.pdf
- **Alhomssi, A. 외 (2023)** *Scalable and Robust Snapshot Isolation for High-Performance Storage Engines* (PVLDB Vol. 16). PostgreSQL, InnoDB, WiredTiger, Oracle, SQL Server의 MVCC 구현을 비교하며 garbage collection·long transaction 문제를 다룬다. https://www.vldb.org/pvldb/vol16/p1426-alhomssi.pdf
- **Gomez Ferro, D., Yabandeh, M. (2014)** *A Critique of Snapshot Isolation*. SI가 직렬화 가능성을 어겨 발생하는 anomaly(write skew 등) 정리. https://arxiv.org/pdf/2405.18393

## 2. B+Tree / 인덱스 / 스토리지 엔진

- **Jeremy Cole — InnoDB 시리즈 (2013~)**: InnoDB 내부 페이지·인덱스 구조를 코드 수준에서 해부한 사실상의 정전. 책 한 권 쓸 만한 인용 지점.
  - On learning InnoDB: A journey to the core — https://blog.jcole.us/2013/01/02/on-learning-innodb-a-journey-to-the-core/
  - The physical structure of InnoDB index pages — https://blog.jcole.us/2013/01/07/the-physical-structure-of-innodb-index-pages/
  - The physical structure of records in InnoDB — https://blog.jcole.us/2013/01/10/the-physical-structure-of-records-in-innodb/
  - B+Tree index structures in InnoDB — https://blog.jcole.us/2013/01/10/btree-index-structures-in-innodb/
  - Efficiently traversing InnoDB B+Trees with the page directory — https://blog.jcole.us/2013/01/14/efficiently-traversing-innodb-btrees-with-the-page-directory/
- **Mark Callaghan — Small Datum 블로그**: MySQL/InnoDB와 MyRocks의 sysbench/insert benchmark 결과를 장기 추적. 5.6→8.x의 쓰기 성능 회귀와 write amplification 비교에 인용 가치 큼. http://smalldatum.blogspot.com/
  - MySQL 5.6 thru 9.4: small server, Insert Benchmark — http://smalldatum.blogspot.com/2025/08/mysql-56-thru-94-small-server-insert.html
  - MyRocks vs InnoDB with sysbench — http://smalldatum.blogspot.com/2023/04/myrocks-vs-innodb-with-sysbench.html
  - MySQL regressions: delete vs InnoDB — https://smalldatum.blogspot.com/2024/08/mysql-regressions-delete-vs-innodb.html

## 3. 옵티마이저·통계

- **MySQL Worklog #5066, #8707** — Histogram statistics 도입과 사용 정책의 1차 자료. (공식 dev.mysql.com에서 인덱스 가능)
- **Alibaba Cloud, "Analysis of MySQL Cost Estimator" (2019)** — `server_cost`/`engine_cost` 테이블의 상수 의미와 cost 계산 흐름 정리. https://www.alibabacloud.com/blog/analysis-of-mysql-cost-estimator_601201

## 4. 기준 도서

- **Schwartz, B., Zaitsev, P., Tkachenko, V. (2012)** *High Performance MySQL, 3rd Edition*, O'Reilly. 인덱스·쿼리 튜닝·복제·운영의 사실상 표준 교재.
- **Aubin, J. & Bell, C. (2021)** *High Performance MySQL, 4th Edition*, O'Reilly. 8.0/Group Replication/클라우드 반영판.
- **Bell, C. (2019)** *Introducing the MySQL 8 Document Store*, Apress. JSON·NoSQL 인터페이스 학습.
- **Vitaliy Liptchinsky, "MySQL Internals Manual"** (공식 docs.mysql.com에 일부) — 소스 코드 기반 내부 동작 매뉴얼. https://dev.mysql.com/doc/internals/en/
- **백은빈·이성욱 (2021)** *Real MySQL 8.0* 1·2권, 위키북스. 한국어로 가장 폭넓게 인용되는 MySQL 8 실전서. B+Tree, R-Tree, full-text, function-based index, multi-value index 등을 모두 다룬다. https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=278488709

## 5. 공식 문서 핵심 인용 지점

- Chapter 13.5: The JSON Data Type — https://dev.mysql.com/doc/refman/8.0/en/json.html
- Chapter 15.1.20.9: Secondary Indexes and Generated Columns — https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html
- Chapter 15.2.20: WITH (Common Table Expressions) — https://dev.mysql.com/doc/refman/8.0/en/with.html
- Chapter 17.3: InnoDB Multi-Versioning — https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html
- Chapter 17.5.1: Buffer Pool — https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html
- Chapter 17.6.5: Redo Log — https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- Chapter 17.7.1: InnoDB Locking — https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- Chapter 17.7.2.1: Transaction Isolation Levels — https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html
- Chapter 17.7.4: Phantom Rows / Next-Key Locking — https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html
- Chapter 17.7.5: Deadlocks in InnoDB — https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html
- Chapter 19.4.10: Semisynchronous Replication — https://dev.mysql.com/doc/refman/8.0/en/replication-semisync.html
- Chapter 26: Partitioning — https://dev.mysql.com/doc/refman/8.4/en/partitioning-overview.html
- Chapter 10.9.6: Optimizer Statistics — https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html
- Chapter 27: Stored Programs / Triggers / Events (자료 정합성용)
- MySQL Performance Schema Quick Start — https://dev.mysql.com/doc/refman/8.0/en/performance-schema-quick-start.html
- sys schema overview — https://dev.mysql.com/doc/refman/8.0/en/sys-schema.html
