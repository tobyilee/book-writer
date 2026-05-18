# Paper Research — PostgreSQL Bible

학술 자료 위주. SIGMOD, VLDB, arXiv. PG 자체 + PG 기반 시스템(Citus, Aurora) + 핵심 알고리즘(MVCC, HNSW, DiskANN).

## 1. MVCC 일반

- Wu et al., **"An Empirical Evaluation of In-Memory Multi-Version Concurrency Control,"** VLDB 2017. PVLDB Vol.10.
  - URL: <https://www.vldb.org/pvldb/vol10/p781-Wu.pdf>
  - 핵심: MVCC 변종(append-only, time-travel, delta) 비교. PG의 append-only는 long-running read에 강하지만 garbage collection이 병목.

- Freitag et al., VLDB 2022 (PVLDB Vol.15) — MVCC 변종 평가/제안.
  - URL: <https://www.vldb.org/pvldb/vol15/p2797-freitag.pdf>

- Pavlo (CMU) — “The Part of PostgreSQL We Hate the Most” (블로그/2023, 학술 비평).
  - URL: <https://www.cs.cmu.edu/~pavlo/blog/2023/04/the-part-of-postgresql-we-hate-the-most.html>
  - 비판 4가지: ① 컬럼 하나만 바뀌어도 row 전체 복제(MySQL/Oracle은 delta), ② 데드 튜플 누적 → 테이블 bloat, ③ 모든 secondary index에 새 entry → write amplification, ④ autovacuum 튜닝 어려움·long-running tx에 막힘. Uber의 PG→MySQL 회귀 사례를 예로 듦.

## 2. HOT 업데이트

- 공식 문서: <https://www.postgresql.org/docs/current/storage-hot.html>
- 운영 해설: <https://stormatics.tech/umairs-planet-postgresql/improving-update-query-performance-using-heap-only-tuples-hot>, <https://boringsql.com/posts/hot-updates/>
- 메커니즘: 인덱스 컬럼 미변경 + 같은 페이지 free space → 새 row를 ctid 체인으로 연결, 인덱스 재기록 생략. write amp 완화 핵심 최적화.

## 3. Citus 분산 PostgreSQL

- Cubukcu et al., **"Citus: Distributed PostgreSQL for Data-Intensive Applications,"** SIGMOD 2021.
  - URL: <https://dl.acm.org/doi/pdf/10.1145/3448016.3457551>
  - 핵심: ① hash partition으로 distribution column으로 분산 → 동일 column 필터면 단일 worker로 라우팅, ② 분산 쿼리 엔진은 SELECT/DML/DDL을 worker로 push, ③ co-location 통한 join 최소화, ④ multi-tenant SaaS에 적합. citus 12에서 schema-based sharding 추가.

## 4. Aurora PostgreSQL

- Verbitski et al., **"Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases,"** SIGMOD 2017.
  - URL: <https://web.stanford.edu/class/cs245/readings/aurora.pdf>

- Verbitski et al., **"Amazon Aurora: On Avoiding Distributed Consensus for I/Os, Commits, and Membership Changes,"** SIGMOD 2018.
  - URL: <https://pages.cs.wisc.edu/~yxy/cs839-s20/papers/aurora-sigmod-18.pdf>

- Wang et al., **"Understanding the Performance Implications of Storage-Disaggregated Database Design,"** SIGMOD 2024.
  - URL: <https://www.cs.purdue.edu/homes/csjgwang/pubs/SIGMOD24_OpenAurora.pdf>
  - 핵심: Aurora는 redo log만 6 copies / 3 AZ로 비동기 복제, 합의 회피. log-structured shared storage가 컴퓨트와 분리. 빠른 crash recovery·replica.

## 5. Vector / ANN

- Malkov & Yashunin, **"Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs,"** IEEE TPAMI 2020 (arXiv:1603.09320).
  - HNSW: 멀티레이어 그래프, 각 노드가 최근접 이웃과 연결. 위층은 sparse, 아래층은 dense. pgvector의 핵심.

- Jayaram Subramanya et al., **"DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node,"** NeurIPS 2019.
  - SSD 친화 graph index. pgvectorscale이 이를 구현 + Statistical Binary Quantization (SBQ).

- arXiv 서베이·비평:
  - Han et al., **"Survey of Vector Database Management Systems,"** arXiv:2310.14021.
  - **"Worst-case Performance of Popular ANN,"** arXiv:2310.19126.
  - **"Towards Robustness: A Critique of Current Vector DB Assessments,"** arXiv:2507.00379.
  - **"Filtered ANN in Vector Databases,"** arXiv:2602.11443 (filter+ANN 시스템 디자인).
  - **"Optimizing SSD-Resident Graph Indexing for High-Throughput Vector Search,"** arXiv:2602.22805.

## 6. AlloyDB (Google)

- VLDB/SIGMOD에 공식 paper는 아직 미발견(2025-05 기준 — 검색 결과 없음, 한계로 명시).
- Google Cloud 기술 블로그: <https://cloud.google.com/blog/products/databases/alloydb-for-postgresql-columnar-engine>
- 핵심: 자동 row↔column 데이터 재구성, ML이 어떤 컬럼을 컬럼 포맷으로 옮길지 학습. 분석 쿼리 최대 100배.

## 7. PostgreSQL 직렬화 가능성

- Ports & Grittner, **"Serializable Snapshot Isolation in PostgreSQL,"** VLDB 2012 (PVLDB Vol.5).
  - SSI(Serializable Snapshot Isolation) 구현 — PG 9.1 도입.
  - 참고: <https://wiki.postgresql.org/wiki/Serializable>

## 8. PostgreSQL 자체 역사

- Stonebraker & Rowe, **"The Design of POSTGRES,"** SIGMOD 1986.
- Stonebraker et al., **"The Implementation of POSTGRES,"** IEEE TKDE 1990.
- POSTGRES → Postgres95 → PostgreSQL로 이어진 academic origin이 풍부한 데이터 타입·익스텐션 친화 설계의 기원.

## 9. 한계

- Aurora의 “PostgreSQL-compat이지만 진짜 PG가 아닌” 부분은 SIGMOD 2024 (OpenAurora) 평가에서 분리된 스토리지의 latency 특성을 정량화. 본문에 직접 인용 자료로 활용 가능.
- Citus의 cross-shard transaction 한계, AlloyDB의 클로즈드 컬럼 엔진 등은 paper로만 다루기 어렵고 벤더 문서 + 커뮤니티 의견 보강 필요.
