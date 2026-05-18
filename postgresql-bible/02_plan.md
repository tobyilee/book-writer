# PostgreSQL 종합 바이블 — Phase 2 저술 계획 (v2)

리서치: `01_reference.md` (601줄, 9개 섹션)
스타일 기준: `toby-book-writing-style.md`
계획 일자: 2026-05-18 (v2: 리뷰 라운드 1 반영)

> **v2 변경 요약:** plan-reviewer 라운드 1의 Critical 3건과 자명한 Should 2건을 반영해 본책 22장 → 25장으로 확장. 변경 이력은 `03_review_log.md`에 append. v1은 `02_plan_v1.md`로 백업.

---

## 제목 후보

1. **『PostgreSQL 종합 바이블: v17/v18 시대의 메인 DB 완전 정복』**
   - 톤: 정공법, 기술서. 권위 강조.
   - 포지셔닝: 서점 매대에서 "이거 한 권이면 된다"는 시그널. DBA·개발자 모두에게 어필.
   - 강점: 검색·구매 결정 직관적. "바이블"이 1차 SEO 키워드.
   - 약점: 닳도록 흔한 네이밍. 토비 스타일의 "함께 고민" 톤과는 거리.

2. **『지금, PostgreSQL: MySQL 베테랑이 PG를 메인 DB로 쓰는 법』**
   - 톤: 페르소나 정조준, 실전서. 진입 장벽 명시.
   - 포지셔닝: "MySQL을 오래 썼는데 PG로 가야 하나?" 고민하는 사람의 책장에 꽂힐 책. Phase 2 페르소나 1 정확히 타격.
   - 강점: 부제로 페르소나 명시 → 자기 책임을 한눈에 알아봄. 토비 스타일과 결.
   - 약점: DBA·tech lead 페르소나가 부제에서 빠짐. 종합 바이블이라기엔 좁아 보일 수 있음.

3. **『PostgreSQL을 다시 배우자: 객체-관계형 DB의 진짜 모습』**
   - 톤: 청유형, 철학적. 토비 시그니처.
   - 포지셔닝: "이미 PG 좀 안다"는 사람의 가정을 흔드는 책. MVCC·HOT·SSI·확장성 등 PG의 진짜 정체성에 집중.
   - 강점: 시리즈 책 같은 인상(토비의 스프링·자바 시리즈 톤). 깊이 있는 독자가 집어들 만한 카피.
   - 약점: 입문자에겐 다소 어렵게 들림. "v17/v18" 같은 최신성 시그널이 부족.

**추천: 1번 (메인 제목) + 3번의 정신 (서문·표지 카피)**

- 표지 메인은 1번 — "종합 바이블"이라는 시그널이 DBA·tech lead·개발자 3종 페르소나 모두에게 가닿는다. 700~800페이지 분량을 정당화하는 가장 정직한 네이밍이기도 하다.
- 부제로 페르소나 3종을 명시: "MySQL 베테랑 개발자·DBA·Tech Lead를 위한 v17/v18 실전 가이드". 서점에서 자기 책임을 식별하게 한다.
- 서문과 1장에는 3번의 정신을 녹인다 — "PG를 안다고 생각했지만, 사실은 다시 배워야 한다"는 각성의 톤. 그래야 토비 스타일과 맞는다.

최종 제목 형식: **『PostgreSQL 종합 바이블 — MySQL 베테랑 개발자·DBA·Tech Lead를 위한 v17/v18 실전 가이드』**

---

## 책 특성

| 항목 | 내용 |
|------|------|
| **장르** | 종합 기술서 (입문 ~ 중급/고급, 레퍼런스 겸용) |
| **분량** | 25장 + 부록 1, **약 790페이지** (한글 약 70만 자, 챕터당 평균 28,000자) |
| **난이도** | 중급 (SQL/RDBMS 기본기를 갖춘 독자 가정). 일부 장은 고급(MVCC 내부, HA, 분산, 보안) |
| **판형** | B5(188x257), 본문 2도 인쇄 가정. EPUB은 자동 흐름 |
| **참고문헌** | §8 그대로 부록 A로 이관 (URL 살아 있는 1차 자료) |

### 독자 여정 — 페르소나별 진입·출구 상태

| 페르소나 | 진입 상태 | 출구 상태 |
|---------|----------|----------|
| **MySQL 베테랑 개발자** | InnoDB 사고방식, "JSON도 되네?" 정도의 PG 인식. LIMIT·timezone·MVCC 차이 모름. | PG의 fork 모델·VACUUM·HOT·SSI를 InnoDB와 대비해 설명 가능. JSONB·array·확장성을 시스템 설계에 녹일 수 있음. **마이그레이션 실전(4억 row·127 버그)을 자기 시스템에 매핑할 수 있음.** |
| **DBA** | 운영 관점에서 PG가 낯섦. autovacuum·replication slot·HA 도구를 들어본 적은 있음. | autovacuum 튜닝, XID wraparound 예방, Patroni/pg_auto_failover 선택, pgBackRest 운영, 17 failover slot 의미를 안다. 페일오버 훈련을 설계할 수 있다. **pgaudit·RLS·SSL/TLS·CVE 추적으로 보안 의사결정도 가능.** |
| **Tech Lead** | "PG로 검색·벡터·GIS·이벤트 다 된다더라"는 소문. 실제 경계가 어딘지 모름. | 9개 활용 시나리오에서 "PG로 가도 되는 선"과 "dedicated가 필요한 선"을 근거를 갖고 그을 수 있다. 클라우드 벤더(RDS/Aurora/AlloyDB/Supabase/Neon) 선택을 의사결정표로 정리할 수 있다. **"Aurora는 진짜 PG인가" 논쟁에 자기 답을 갖는다.** |

### Part 구조 (4부 + 부록)

```
Part 1. 만남 — 왜 지금 PostgreSQL인가 (1~3장, ~86p)
Part 2. 정체성 — PG의 진짜 모습 (4~7장, ~125p)
Part 3. 활용 — 9가지 시나리오 (8~16장, ~281p)
Part 4. 운영 — DBA의 일 (17~25장, ~285p)
  ├─ 17장 마이그레이션 실전 (신규, Part 4 시작 가교)
  ├─ 18~21장 코어 운영 (VACUUM/백업/HA/풀러)
  ├─ 22장 보안 (신규)
  ├─ 23장 성능 튜닝 (구 22장 분리)
  ├─ 24장 클라우드 (구 17장 이동 + Aurora 확장)
  └─ 25장 한국 사례·결론 (구 22장 분리)
부록 A. 참고문헌 (~8p)
```

---

## 내러티브 아크 — 왜 이 순서인가 (v2)

이 책은 페르소나가 셋이라 진입 경로도 셋이 되기 쉬운데, 그러면 "종합 바이블"이라는 약속이 깨진다. 그래서 Part 구조를 두되, **공통 진입점은 Part 1·2**로 묶어 셋이 같은 토대 위에 서게 만든다. Part 3와 Part 4는 페르소나에 따라 비중을 달리 읽을 수 있도록 챕터를 독립적으로 설계한다.

**Part 1 (만남)** 은 "왜 지금 PG인가"에 답한다. 1장은 PG의 출생과 DNA, 그리고 2026년 현재의 위상. 2장은 MySQL 베테랑이 가장 먼저 부딪히는 8가지 차이를 모아놓고 책 전체의 지도로 삼는다. 3장은 v17/v18에서 무엇이 새로워졌는지를 한 번에 펼친다. 이 세 장이 끝나면 독자는 "왜 이 책을 더 읽어야 하는지"의 답을 갖는다.

**Part 2 (정체성)** 는 PG의 내부를 연다. fork 모델·MVCC·HOT·WAL·SSI를 차례로 다룬다. 여기를 건너뛰면 Part 3·4의 설명이 "왜 그렇게 해야 하는지" 근거가 비어버린다. 4장은 프로세스 모델과 메모리, 5장은 MVCC와 VACUUM의 운명적 짝(인덱스 증폭, bloat의 기원, **bloat가 운영에서 어떻게 보이는지의 결말까지**), 6장은 HOT과 fillfactor, 7장은 WAL과 SSI. 이 4개 장이 책의 가장 단단한 뼈대다.

**Part 3 (활용)** 는 9개 시나리오를 챕터당 1개씩 다룬다. 순서는 "전통적인 것 → 새로운 것"으로 배치 — 8장 SQL 표준과 트랜잭션, 9장 JSON/문서 DB 대체, 10장 전문 검색, 11장 GIS, 12장 벡터/RAG, 13장 이벤트·큐·실시간, 14장 FDW·CDC·동기화, 15장 분석·OLAP·시계열, 16장 API 백엔드. 각 장은 독립적으로 읽을 수 있어 tech lead가 관심 시나리오만 골라 읽어도 손해가 없다. 단, 장마다 "PG로 가도 되는 선"과 "dedicated가 필요한 선"을 명확히 그어 "Just Use Postgres"의 함정도 같이 짚는다.

**Part 4 (운영)** 는 DBA 페르소나의 책장이다 — v2에서 가장 크게 재구성됐다.

- **17장 (신규) 마이그레이션 실전**은 Part 4의 진입 가교다. MySQL 베테랑 페르소나가 Part 1·2·3에서 PG의 정체성과 활용을 모두 본 뒤, "그래서 우리 4억 row를 어떻게 옮기는가"라는 질문에 답할 챕터를 운영의 출발점에 두었다. 부록에 묻혀 있던 마이그레이션 실전(4억 row·6개월·다운타임 18시간·127 버그·LIMIT·timezone·47개 쿼리)과 한국 후기 4건(@melon03090, @peace_e, 맞추다, iting.co.kr)을 본 챕터로 끌어올렸다. 부록 직전이 아니라 Part 4 시작에 둔 이유는 — 마이그레이션 후의 운영(VACUUM·HA·풀러·보안)이 18~22장이기 때문에, "옮긴 뒤 어떻게 운영하는가"의 인과 사슬이 자연스럽게 이어진다.
- **18~21장**은 코어 운영 4종이다. 18장 VACUUM과 XID wraparound, 19장 백업·복구·PITR, 20장 HA와 페일오버, 21장 connection pooling과 모니터링.
- **22장 (신규) 보안과 감사**는 페르소나 2(DBA)·3(Tech Lead)의 핵심 의사결정 영역인데 v1에서 부록 끝 한 페이지로 처리됐던 항목을 본 챕터로 승격한 결과다. pgaudit, SSL/TLS, scram-sha-256, role/grant 설계, RLS 운영(16장은 멀티테넌트 응용 패턴, 22장은 운영 보안), CVE 추적, audit log 보관 정책을 다룬다.
- **23장 성능 튜닝**은 v1 22장의 "성능 튜닝 종합" 부분을 단독 챕터로 분리한 결과다. 인덱스 매트릭스·EXPLAIN·함정 6가지·병렬 쿼리·파티셔닝·OS 레벨 체크리스트를 충분한 분량으로 다룬다.
- **24장 클라우드**는 v1 17장(Part 4 첫머리에 있던)을 Part 4 끝쪽으로 이동한 결과다. 매니지드 PG 의사결정은 vacuum/HA/익스텐션 운영 원리를 알아야 해석되므로 18~23장 뒤에 두는 것이 인과적으로 맞다. Aurora "진짜 PG인가" 논쟁은 24장 안에서 별도 절(24.2)로 확장 — PG-호환의 기술적 의미, disaggregated storage가 VACUUM/wraparound/replication slot에 미치는 영향, OpenAurora SIGMOD 2024 paper의 측정 결과를 3꼭지로.
- **25장 한국 사례·결론**은 v1 22장의 "한국 사례 + 결론" 부분을 단독 챕터로 분리한 결과다. 카카오 클린플랫폼 CDC, 카카오스타일 Bedrock, 당근페이 BroQuery, 공공 Oracle→PG 4건을 각각 깊이 다루고, 책 전체의 지식이 의사결정에서 어떻게 합쳐지는지로 책을 닫는다. 한국 페르소나를 마지막에 다시 한 번 정조준하는 시그널.

부록 A는 참고문헌만 남는다. v1 부록 A의 마이그레이션 체크리스트는 17장 본문으로 흡수됐고, 17장 17.7에 "한 페이지 체크리스트" 형태로 부록의 가치를 보존했다.

### 페르소나별 추천 경로 (v2)

- **MySQL 베테랑 개발자:** 1 → 2 → 3 → 4 → 5 → 6 → 8 → 9 → 16 → **17 (마이그레이션 실전)** → 22 (보안) → 25 (12장 분량). 17장이 추가되면서 페르소나 1의 서사 곡선이 완성된다 — "들어와서 정체성 알고 활용 보고 옮기는" 경로. 운영은 19·20·21장만 골라 읽어도 충분.
- **DBA:** 1 → 4 → 5 → 6 → 7 → **17 (마이그레이션 실전)** → 18 → 19 → 20 → 21 → **22 (보안)** → 23 (성능 튜닝) → 24 (클라우드) → 25 (한국 사례) (13장 분량). Part 3는 9·15장만 운영 관점에서 훑으면 됨. 22장 보안과 24장 클라우드가 DBA에게는 별책처럼 쓰일 수 있는 묶음.
- **Tech Lead:** 1 → 2 → 3 → 7 → Part 3 전체(8~16) → **17 (마이그레이션 실전)** → 22 (보안 의사결정만) → **24 (클라우드, Aurora 절 포함)** → 25 (결론부) (15장 분량). Part 2의 4·5·6장은 결론만 빠르게. 24장 클라우드와 25장 한국 사례가 Tech Lead 페르소나의 결론 챕터.

---

## 챕터 목록

> 각 챕터의 "토비 진입점"은 1장 첫 문단 또는 첫 절의 도입 문장이다. 수사적 질문·상황 가정으로 독자의 사고를 끌어들이는 시그니처 톤을 미리 박아둔다.

---

### Part 1. 만남 — 왜 지금 PostgreSQL인가

#### 1장. PostgreSQL은 어떻게 데이터베이스의 중심으로 왔나
- **핵심 질문:** 2026년 현재, 왜 새 시스템의 메인 DB로 PostgreSQL이 선택되고 있는가?
- **주요 내용:**
  - 1.1 1986년 버클리에서 시작된 객체-관계형 DB의 DNA (Stonebraker)
  - 1.2 2024 StackOverflow 1위, 2년 연속 가장 많이 쓰는 DB
  - 1.3 한국 시장의 움직임 — 공공·금융·플랫폼 채택 가속 (다음 뉴스 2026-01)
  - 1.4 "Postgres is eating the database world" — Pigsty의 주장과 그 한계
  - 1.5 이 책을 읽는 세 종류의 독자에게
- **독자가 얻는 것:** "PG는 그냥 한 옵션"이라는 관성이 깨지고, 이 책을 끝까지 읽을 동기.
- **토비 진입점:** *"DB를 새로 고른다고 해보자. 후보가 셋이라면 그중 둘은 무난한 선택이고, 하나는 모험이다. 2020년까지 PostgreSQL은 그 모험 쪽에 있었다. 2026년은 어떨까?"*
- **예상 분량:** 24,000자 / ~27p

#### 2장. MySQL 베테랑이 가장 먼저 부딪히는 여덟 가지
- **핵심 질문:** InnoDB에 익숙한 손은 PostgreSQL의 어디서 처음으로 미끄러지는가?
- **주요 내용:**
  - 2.1 동시성 모델 — thread-per-connection vs fork
  - 2.2 MVCC 저장 방식 — undo log vs append-only
  - 2.3 클러스터 인덱스의 부재 — heap + 별도 인덱스
  - 2.4 데이터 타입 표현력 — array, range, hstore, JSONB
  - 2.5 트랜잭션 DDL이 진짜로 된다
  - 2.6 시퀀스·IDENTITY·UUIDv7(v18 내장)
  - 2.7 LIMIT·timezone·SQL 표준 차이 — 마이그레이션의 첫 신호
  - 2.8 확장성 — extension은 사이드 카가 아니라 코어
  - 2.9 8가지 차이가 만드는 사고방식의 전환
- **독자가 얻는 것:** 책 전체의 지도. 어떤 장이 자기 통증과 직결되는지 한눈에 보인다.
- **토비 진입점:** *"새 언어를 배울 때 가장 무서운 건 모르는 문법이 아니라, '내가 안다고 착각하는' 문법이다. MySQL을 오래 쓴 사람이 PostgreSQL로 옮길 때도 똑같다. 살펴보자, 어디서 미끄러지는지."*
- **분리 메모:** 2장은 "어디서 미끄러지는지의 지도", 17장(마이그레이션)은 "실제로 미끄러진 사람들의 이야기". 2.7은 신호만, 실전 비용은 17장.
- **예상 분량:** 28,000자 / ~32p (지도 역할, v1의 30,000자에서 2,000자 다이어트 — 마이그레이션 실전 부분이 17장으로 이동했으므로)

#### 3장. v17과 v18, 무엇이 바뀌었나
- **핵심 질문:** 최신 버전에서 무엇이 새로워졌고, 그것이 왜 중요한가?
- **주요 내용:**
  - 3.1 v17 — vacuum 메모리 재작성, failover slot, JSON_TABLE, MERGE의 RETURNING
  - 3.2 v18 — RETURNING OLD/NEW, temporal constraint, UUIDv7, planner statistics 보존
  - 3.3 업그레이드 직후 성능 절벽이 사라진다는 것의 의미
  - 3.4 17부터 logical replication이 진짜 production-ready가 된 이유 (failover slot)
  - 3.5 벤치마크 — pgbench 16→17→18 추이와 HammerDB 회귀 토론
- **독자가 얻는 것:** "올려야 하는가, 미뤄도 되는가"의 판단 기준.
- **토비 진입점:** *"새 버전이 나왔다는 소식은 늘 있다. 진짜 질문은 따로 있다. 운영 중인 시스템을 멈춰서까지 올릴 만한가? v17과 v18을 그 기준으로 다시 보자."*
- **분리 메모:** 3장은 release note 톤(왜 올려야 하는가). 8장은 표현력 깊이(SQL로 무엇이 가능해지는가). 같은 기능(MERGE·JSON_TABLE·RETURNING·temporal)이라도 3장은 "올려야 하는 이유", 8장은 "그 기능으로 뭘 쓰는가"로 분리.
- **예상 분량:** 22,000자 / ~25p

---

### Part 2. 정체성 — PostgreSQL의 진짜 모습

#### 4장. 프로세스 모델과 메모리 — fork가 만드는 모든 것
- **핵심 질문:** PG가 connection마다 OS process를 띄운다는 사실이 왜 시스템 설계 전체를 바꾸는가?
- **주요 내용:**
  - 4.1 postmaster와 fork — 1 connection = 1 process
  - 4.2 백그라운드 프로세스 풀세트 (BG writer, checkpointer, WAL writer, autovacuum launcher…)
  - 4.3 shared_buffers·WAL buffer·work_mem 메모리 모델
  - 4.4 max_connections를 함부로 올리면 안 되는 이유
  - 4.5 PG에 풀러가 필수인 이유 — fork 모델의 결과로서의 당위성
- **독자가 얻는 것:** "왜 PG에는 풀러가 필수인가"의 근본적 결론. 도구 선택은 21장에서.
- **분리 메모:** 4장은 "fork 모델의 결과로서의 풀러 당위성"(왜 필요한가), 21장은 "풀러 도구 선택과 함정"(무엇을 어떻게 쓰는가). 중복 없는 layered coverage.
- **토비 진입점:** *"커넥션 풀이 왜 필요한지 누군가 묻는다고 해보자. MySQL에서는 '비용 절감'이 답이지만, PostgreSQL에서는 '생존'이 답이다. 차이가 어디서 오는지 들여다보자."*
- **예상 분량:** 26,000자 / ~30p

#### 5장. MVCC와 VACUUM — append-only가 치르는 값
- **핵심 질문:** PG의 MVCC는 왜 VACUUM을 운명처럼 데리고 다니는가?
- **주요 내용:**
  - 5.1 row versioning — xmin·xmax·ctid
  - 5.2 InnoDB undo log와의 비교
  - 5.3 dead tuple과 table bloat의 기원
  - 5.4 index amplification — Uber가 PG를 떠난 진짜 이유
  - 5.5 Andy Pavlo가 짚은 4가지 통증
  - 5.6 long-running tx가 가져오는 도미노 (vacuum이 못 회수)
  - 5.7 **bloat가 운영에서 어떻게 보이는가 (18장 예고)** — query 느려짐, 디스크 사용 폭증, vacuum의 burst, 18장 처방의 미리보기
- **독자가 얻는 것:** PG 운영의 모든 통증의 근원을 한 챕터에 잡아 둔다. 5장이 끝나면 "왜 18장을 안 건너뛰면 안 되는지"의 답이 손에 잡힌다.
- **토비 진입점:** *"같은 'MVCC'라는 이름 아래 PostgreSQL과 MySQL은 전혀 다른 일을 한다. 한쪽은 새 버전을 옆에 적고, 다른 쪽은 따로 떼서 적는다. 이 작은 차이가 운영의 무게 전체를 바꾼다."*
- **예상 분량:** 34,000자 / ~38p (v1 32,000자 + 5.7 신설 2,000자)

#### 6장. HOT과 fillfactor — 비용을 깎는 단일 최적화
- **핵심 질문:** 인덱스 증폭이라는 청구서를 어떻게 줄일 수 있는가?
- **주요 내용:**
  - 6.1 HOT의 두 조건 — 인덱스 컬럼 미변경 + 페이지 free space
  - 6.2 ctid chain과 인덱스가 살아남는 방식
  - 6.3 fillfactor 90→70의 트레이드오프
  - 6.4 HOT을 깨는 흔한 실수들
  - 6.5 모니터링 — pg_stat_user_tables의 n_tup_hot_upd
- **독자가 얻는 것:** "인덱스 컬럼은 함부로 건드리지 말라"는 격언의 진짜 이유.
- **토비 진입점:** *"한 번의 UPDATE가 인덱스 전체를 흔들어놓는다고 상상해보자. 끔찍한 일이다. 그런데 그 일은 매일 일어난다. PostgreSQL의 HOT가 이 비용을 어떻게 깎는지 알아보자."*
- **예상 분량:** 22,000자 / ~25p

#### 7장. WAL과 SSI — 모든 기능의 토대
- **핵심 질문:** 복제·CDC·PITR·직렬화 가능성은 어떻게 한 가지 메커니즘에서 나오는가?
- **주요 내용:**
  - 7.1 WAL — Write-Ahead Log의 형식과 흐름
  - 7.2 WAL이 떠받치는 5가지 — 복구, streaming 복제, logical 복제, PITR, CDC
  - 7.3 v17의 WAL writer 메모리 개선
  - 7.4 SSI(Serializable Snapshot Isolation)의 이론적 토대 (Ports & Grittner, VLDB 2012)
  - 7.5 잠금 없이 직렬화 가능성을 보장하는 방식 — 충돌 탐지와 abort
  - 7.6 금융·결제 시스템이 PG를 고르는 이론적 근거
- **독자가 얻는 것:** 책의 나머지 절반(Part 3·4)이 어떤 단일 메커니즘 위에 서 있는지 본다.
- **토비 진입점:** *"PostgreSQL의 거의 모든 자랑은 WAL 하나로 거슬러 올라간다. 복제도, CDC도, PITR도, 진짜 직렬화도 다 거기서 나온다. 한 번 제대로 들여다볼 만하지 않을까?"*
- **예상 분량:** 28,000자 / ~32p

---

### Part 3. 활용 — 아홉 가지 시나리오

#### 8장. SQL 표준과 트랜잭션 — RDB 정통의 깊이
- **핵심 질문:** PG가 "SQL 표준 준수"라고 말할 때 그것이 어떤 무기인가?
- **주요 내용:**
  - 8.1 윈도우 함수·CTE·WITH RECURSIVE
  - 8.2 MERGE와 RETURNING (15·17의 진화) — **표현력 관점, 3.1과 분리**
  - 8.3 JSON_TABLE (17) — JSON을 FROM 절에 펼치기, **활용 예제 위주**
  - 8.4 RETURNING OLD/NEW (18)와 trigger 단순화 — **trigger 리팩토링 사례**
  - 8.5 temporal constraint (18) — **이력 테이블 설계 예제**
  - 8.6 트랜잭션 DDL과 SAVEPOINT — 마이그레이션의 안전망
- **독자가 얻는 것:** "표준 SQL이 PG의 진짜 경쟁력"이라는 감각.
- **분리 메모:** 3장이 release note(왜 올려야 하는가)였다면 8장은 표현력 깊이(SQL로 무엇이 가능해지는가). 같은 기능을 다루지만 톤이 다름.
- **토비 진입점:** *"애플리케이션 로직 절반이 SQL로 해결되는 경우를 본 적 있을 것이다. 그게 가능한 DB와 불가능한 DB의 차이는 표현력에서 온다. 표현력의 정체를 살펴보자."*
- **예상 분량:** 26,000자 / ~30p

#### 9장. JSON DB로서의 PostgreSQL — MongoDB를 대체할 수 있는가
- **핵심 질문:** 문서 DB 워크로드를 PG로 가져갈 때 어디까지 가능하고, 어디서 멈춰야 하는가?
- **주요 내용:**
  - 9.1 JSONB의 바이너리 저장 모델
  - 9.2 GIN 인덱스와 jsonb_path_ops
  - 9.3 expression index·부분 인덱스로 특정 키만 가속
  - 9.4 JSON_TABLE로 SQL과 문서를 잇기
  - 9.5 한계 — GIN write overhead, 복합 multi-key 인덱스, 1.25M row 이상 워크로드
  - 9.6 "PG로 충분한 80%"와 "MongoDB가 여전히 유리한 20%"
- **독자가 얻는 것:** 의사결정표 1장.
- **토비 진입점:** *"MongoDB를 쓰는 시스템을 PostgreSQL로 옮길 수 있을까? 80%는 가능하다고들 한다. 그런데 그 80%는 누구의 80%인가? 자기 워크로드의 어디쯤인지 확인해보자."*
- **예상 분량:** 28,000자 / ~32p

#### 10장. 전문 검색 — Elasticsearch 없이 가는 길
- **핵심 질문:** PG로 한국어 전문 검색까지 잘 하려면 어떤 익스텐션 조합이 필요한가?
- **주요 내용:**
  - 10.1 내장 tsvector/tsquery의 강점과 한국어 한계
  - 10.2 pg_trgm — fuzzy match, 비ASCII 제약
  - 10.3 PGroonga — 한국어·일본어·중국어 zero-ETL
  - 10.4 ParadeDB / pg_search — BM25, Tantivy 기반, ES와 비슷한 성능
  - 10.5 Tiger Data pg_textsearch — 17 access method API의 경쟁
  - 10.6 한국어 시나리오 의사결정 — PGroonga 또는 PGroonga + pg_search
- **독자가 얻는 것:** 한국어 검색 스택 선택 가이드.
- **토비 진입점:** *"검색이 필요해서 Elasticsearch를 또 하나 세운다고 해보자. 운영팀이 한숨을 쉴 것이다. 그 한숨을 줄일 수 있는지, PostgreSQL 진영의 도구들을 차례로 살펴보자."*
- **예상 분량:** 26,000자 / ~30p

#### 11장. GIS와 PostGIS — 공간 데이터의 표준
- **핵심 질문:** 공간 데이터를 다루는 시스템에서 PostGIS가 사실상 표준이 된 이유는 무엇인가?
- **주요 내용:**
  - 11.1 GEOMETRY·GEOGRAPHY 타입과 SRID
  - 11.2 GiST·SP-GiST 공간 인덱스
  - 11.3 ST_* 함수군과 토폴로지·라우팅(pgRouting)
  - 11.4 production 사례 — State Farm, NIBIO, Telkom Kenya
  - 11.5 한국 운영기 — 공간 쿼리 성능 이슈와 EXPLAIN 개선
  - 11.6 성능 튜닝 — 인덱스 선택, ST_DWithin과 GIST의 궁합
- **독자가 얻는 것:** GIS가 필요할 때 망설임 없이 PostGIS를 고를 수 있는 근거.
- **토비 진입점:** *"지도 위에 점을 찍고 거리·면적·교차를 묻는 일이 얼마나 흔한지 생각해보자. 그 모든 질문에 답하는 표준이 한 익스텐션 안에 들어 있다."*
- **예상 분량:** 26,000자 / ~30p

#### 12장. 벡터 DB와 RAG 백엔드 — pgvector·pgvectorscale
- **핵심 질문:** dedicated 벡터 DB 대신 PG를 쓰는 선은 어디까지인가?
- **주요 내용:**
  - 12.1 pgvector — HNSW와 IVFFlat
  - 12.2 pgvectorscale — DiskANN + Statistical Binary Quantization
  - 12.3 벤치마크 — Pinecone 대비 75% 절감, Qdrant 대비 11.4배
  - 12.4 알고리즘 배경 — HNSW(arXiv:1603.09320), DiskANN(NeurIPS 2019)
  - 12.5 의사결정 — 10M 이하 단일 필터 vs 10M+ 복합 메타데이터
  - 12.6 2026 트렌드 — relational + vector 통합으로 가는 방향
- **독자가 얻는 것:** RAG 시스템 스택 선택 가이드.
- **토비 진입점:** *"OpenAI 임베딩을 받아 어딘가에 저장한다고 해보자. 그 어딘가가 또 하나의 DB여야 할까? 같은 트랜잭션 안에 둘 수 있다면 무엇이 달라질까?"*
- **예상 분량:** 28,000자 / ~32p

#### 13장. 이벤트·큐·실시간 — Kafka를 미루는 법
- **핵심 질문:** PG 안에서 메시지 버스를 어디까지 흉내낼 수 있는가?
- **주요 내용:**
  - 13.1 LISTEN/NOTIFY — payload 8KB의 가벼운 알림
  - 13.2 logical decoding (wal2json·pgoutput) — Debezium의 토대
  - 13.3 pg_cron + pgmq — 스케줄링과 영속 큐
  - 13.4 Outbox + logical replication 패턴
  - 13.5 "Just Use Postgres" — Kafka 도입을 미루는 의사결정
  - 13.6 카카오 클린플랫폼 CDC 파이프라인 케이스 — **패턴 시연만, 의사결정 디테일은 25장**
- **독자가 얻는 것:** 메시지 인프라 도입 의사결정의 새로운 옵션.
- **분리 메모:** 13장 13.6은 "CDC 패턴이 이렇게 생겼다"의 기술 시연, 25장은 "카카오가 왜 그 결정을 했고 무엇이 남았는가"의 케이스 분석. 중복 없는 분리.
- **토비 진입점:** *"메시지 큐 하나 쓰자고 새 클러스터를 띄우는 일이 늘 정답일까? 작은 팀이라면, 또 다른 답이 있을 수 있다."*
- **예상 분량:** 26,000자 / ~30p

#### 14장. FDW·CDC·동기화 — 데이터 경계를 허무는 법
- **핵심 질문:** 여러 DB가 흩어진 환경에서 PG를 데이터 허브로 쓸 수 있는가?
- **주요 내용:**
  - 14.1 postgres_fdw — 다른 PG를 외부 테이블로
  - 14.2 80+ FDW 카탈로그 — MySQL, Oracle, Mongo, Kafka, ClickHouse, DuckDB
  - 14.3 Debezium PostgreSQL CDC — pgoutput vs wal2json 선택
  - 14.4 v17 failover slot의 의미 — 페일오버 후에도 CDC 컨슈머 생존
  - 14.5 pglogical과 내장 logical replication의 경계
- **독자가 얻는 것:** 마이그레이션·통합 시나리오의 도구 셋. 17장 마이그레이션의 인프라 준비.
- **토비 진입점:** *"DB가 여러 개로 흩어진 회사에서 일해본 사람은 안다. 한쪽에서 다른 쪽으로 데이터를 옮기는 일이 얼마나 번거로운지. PostgreSQL의 FDW와 logical replication이 그 번거로움을 얼마나 줄여주는지 살펴보자."*
- **예상 분량:** 24,000자 / ~27p

#### 15장. 분석·OLAP·시계열 — Citus·TimescaleDB·DuckDB
- **핵심 질문:** ClickHouse를 따로 세우지 않고 어디까지 갈 수 있는가?
- **주요 내용:**
  - 15.1 윈도우 함수 + CUBE/ROLLUP + materialized view (기본기)
  - 15.2 Citus — hash partition 분산, co-located join, **postgresql.kr sharding 자료의 일반론도 1꼭지**
  - 15.3 TimescaleDB — hypertable, continuous aggregate, native columnstore
  - 15.4 Hydra — Citus columnar fork, ClickBench 상위
  - 15.5 AlloyDB columnar engine — 자동 row↔column 변환, 최대 100배
  - 15.6 pg_duckdb / pg_analytics — DuckDB 엔진을 PG 안에서
  - 15.7 ClickBench 비교표와 그 해석 — "익스텐션 composability가 진짜 moat"
- **독자가 얻는 것:** OLTP+OLAP 혼합 환경의 설계 옵션 매트릭스.
- **토비 진입점:** *"분석은 빠른 DB로, 운영은 정확한 DB로 — 그렇게 둘로 갈라야 한다고 누가 정했을까? 한 쪽으로 합칠 수 있는 길을 같이 찾아보자."*
- **예상 분량:** 32,000자 / ~36p

#### 16장. API 백엔드 — DB가 백엔드다
- **핵심 질문:** PostgREST·pg_graphql·Supabase가 가능하게 만든 "DB-as-backend" 패턴은 어디서 빛나고 어디서 위험한가?
- **주요 내용:**
  - 16.1 PostgREST — 스키마에서 REST API 자동 생성
  - 16.2 pg_graphql — Supabase 작성, 스키마 reflect
  - 16.3 Hasura — 멀티 DB GraphQL/REST/gRPC
  - 16.4 Supabase 풀스택 — Auth·Storage·Realtime·Edge Functions
  - 16.5 RLS 멀티테넌트 패턴 — tenant_id, current_setting, USING 정책 (**응용 패턴 위주, 운영 보안은 22장**)
  - 16.6 RLS 운영 주의 — EXPLAIN에 정책 술어, admin bypass 감사 (22장 참조)
  - 16.7 lock-in 트레이드오프
- **독자가 얻는 것:** 풀스택 의사결정 — "DB가 백엔드"라는 선택의 비용과 효용.
- **분리 메모:** 16장 RLS는 멀티테넌트 SaaS 응용 패턴(어떻게 설계하는가), 22장은 운영 보안(어떻게 감사·검증하는가). 같은 RLS지만 결이 다름.
- **토비 진입점:** *"백엔드 코드의 절반이 CRUD 매핑이라는 사실을 인정하고 나면, '그걸 DB가 해주면 안 되나'라는 질문이 자연스럽다. 그 답을 찾아보자."*
- **예상 분량:** 30,000자 / ~34p

---

### Part 4. 운영 — DBA의 일

#### 17장. (신규) MySQL/Oracle → PostgreSQL 마이그레이션 실전
- **핵심 질문:** 4억 row·6개월·다운타임 18시간·127개 버그를 거친 사람들이 무엇을 배웠고, 그것을 우리 시스템에 어떻게 적용할 것인가?
- **주요 내용:**
  - 17.1 마이그레이션 의사결정 매트릭스 — "왜 옮기는가"의 답이 없으면 시작하지 말 것 (비용·기능·생태계·lock-in 4축)
  - 17.2 쿼리 semantics 변환 — DDL이 아니라 의미가 깨지는 지점들 (LIMIT/OFFSET, timezone, DECODE/CASE, (+) 외부조인, CONNECT BY, NULL 처리, 묵시적 캐스트)
  - 17.3 데이터 타입 매핑 표 — MySQL `TINYINT(1)`→`BOOLEAN`, `DATETIME`→`TIMESTAMP WITH/WITHOUT TIME ZONE`, `AUTO_INCREMENT`→`IDENTITY`/`SEQUENCE`/`UUIDv7`(v18), Oracle `NUMBER`→`NUMERIC` 정밀도 함정
  - 17.4 이관 도구 — pgloader(MySQL), ora2pg(Oracle), Debezium CDC + dual-write, AWS DMS·SCT의 한계
  - 17.5 4억 row 한국 케이스 분석 — @melon03090 ("LIMIT 절 전부 수정, 47개 쿼리 timezone 깨짐, 발견 버그 127개"), @peace_e (3개월 dual-run), 맞추다 (단계적 cutover), iting.co.kr re:Invent 2025 — 4건의 공통 패턴과 차이점 추출
  - 17.6 다운타임 최소화 패턴 — dual-write·logical replication 기반 무중단(14장 참조)·짧은 freeze window·롤백 시나리오
  - 17.7 마이그레이션 직후 운영 체크리스트 (구 부록 A 1페이지) — autovacuum 튜닝(18장)·max_connections(4·21장)·extension 지원 확인(매니지드 PG)·통계 재수집·planner stats 보존(v18) 점검
  - 17.8 매니지드 PG 익스텐션 지원 매트릭스 — RDS·Aurora·Cloud SQL·AlloyDB·Supabase·Neon에서 PostGIS·pgvector·pgaudit·pg_partman 등의 가용성 (24장과 cross-reference)
  - 17.9 함정 모음 — "테스트는 100GB로 했는데 운영은 4TB", "통계 안 모은 채 cutover", "익스텐션 누락 발견 D-1", "롤백 시나리오 없음"
- **독자가 얻는 것:** "MySQL 베테랑이 시작해서 마이그레이션으로 도착하는" 서사 곡선의 도착점. 부제의 약속을 실제로 받는다.
- **토비 진입점:** *"4억 row를 옮기는 데 6개월이 걸렸다고 누가 말했다. 다운타임 18시간, 발견 버그 127개. 그 숫자를 들으면 두 가지 반응이 나뉜다. '우리는 더 잘할 수 있다'와 '우리도 그렇게 될 것이다'. 둘 다 절반만 맞다. 그 안의 진짜 교훈을 같이 따라가보자."*
- **레퍼런스 매핑:** §2 본문(8가지 차이 + 4억 row 사례) + §7.2 한국 후기 4건 + §8.6 마이그레이션 자료 흡수.
- **예상 분량:** 24,000자 / ~28p

#### 18장. VACUUM과 XID wraparound — 진짜로 멈추는 사고
- **핵심 질문:** autovacuum을 어떻게 길들이고, wraparound 사고를 어떻게 막을 것인가?
- **주요 내용:**
  - 18.1 autovacuum 트리거 — threshold + scale_factor
  - 18.2 대용량 테이블에서 기본값이 위험한 이유
  - 18.3 모니터링 — n_dead_tup, last_autovacuum, n_mod_since_analyze
  - 18.4 XID wraparound — 7.5개월의 시한폭탄
  - 18.5 wraparound 사고 케이스 — 한 달 만에 클러스터 read-only
  - 18.6 예방과 복구 — relfrozenxid 모니터링, postgres_get_av_diag (AWS)
  - 18.7 Bloat 처리 — VACUUM FULL, pg_repack, pg_squeeze 비교
- **독자가 얻는 것:** DBA의 가장 큰 야간 호출 두 가지를 예방하는 운영서. 5장 5.7의 예고가 여기서 실제 처방으로 닫힌다.
- **토비 진입점:** *"autovacuum을 꺼두고 싶었던 적이 있는가? 잠깐의 성능 문제가 있을 때 그 유혹은 강하다. 그런데 그 한 번의 결정이 한 달 뒤에 클러스터를 read-only로 만든다고 해보자. 끔찍한 일이다."*
- **예상 분량:** 30,000자 / ~34p

#### 19장. 백업·복구·PITR — pgBackRest·Barman·WAL-G
- **핵심 질문:** 복구 가능성을 어떻게 확보하고, 실제로 작동하는지 어떻게 검증하는가?
- **주요 내용:**
  - 19.1 pg_basebackup — 내장의 한계
  - 19.2 pgBackRest — 사실상 표준, full/diff/incremental, multi-TB
  - 19.3 Barman — EDB, 멀티 서버 중앙관리
  - 19.4 WAL-G — Go, 클라우드 네이티브
  - 19.5 PITR 시나리오 — 사고 시각 1분 전으로 되돌리기
  - 19.6 백업 검증 — "백업이 있다"와 "복구된다"는 다른 일
  - 19.7 클라우드별 백업 전략
- **독자가 얻는 것:** "백업은 있는데 복구가 안 된다"는 야간 사고를 막는 운영서.
- **토비 진입점:** *"백업이 있다고 안심하던 팀이 막상 복구를 시도하다 손이 멈춘 적이 있다. 백업과 복구는 다른 일이다. 둘을 같은 일로 만드는 도구들을 살펴보자."*
- **예상 분량:** 26,000자 / ~30p

#### 20장. HA와 페일오버 — Patroni·pg_auto_failover·17 failover slot
- **핵심 질문:** 가용성을 자동화하는 도구들의 트레이드오프와 베스트 프랙티스는 무엇인가?
- **주요 내용:**
  - 20.1 streaming replication 기초 — 동기 vs 비동기
  - 20.2 Patroni — etcd/Consul, REST API, 자동화 표준
  - 20.3 pg_auto_failover — monitor 1대의 단순함, SPoF 트레이드오프
  - 20.4 최소 3노드 — primary + 2 standby
  - 20.5 라우팅 — PgBouncer/HAProxy, /primary health check
  - 20.6 분기별 페일오버 훈련 — **시나리오 한 개 깊이 (스크립트·체크리스트·통과 기준)**
  - 20.7 v17 failover slot — logical replication도 HA 안에서 연속성
- **독자가 얻는 것:** HA 도구 선택과 페일오버 훈련 설계의 실행 매뉴얼.
- **토비 진입점:** *"가용성을 자동화하는 도구를 설치했다고 가용성이 보장되지는 않는다. 실제로 작동하는지 확인할 단 한 가지 방법이 있다. 정기적으로 일부러 죽이는 것이다."*
- **예상 분량:** 30,000자 / ~34p (v1 28,000자 + 20.6 페일오버 훈련 절 +2,000자)

#### 21장. Connection pooling과 모니터링 — PgBouncer·pg_stat_statements
- **핵심 질문:** 풀러는 어떻게 고르고, 모니터링은 어디서 시작해야 하는가?
- **주요 내용:**
  - 21.1 PgBouncer — session·transaction·statement 모드 (**4장에서 "왜 필요한가"는 이미 답했음 — 21장은 도구 선택**)
  - 21.2 transaction pooling의 함정 — prepared statement·advisory lock·SET LOCAL
  - 21.3 Pgcat — 멀티스레드, read/write split
  - 21.4 Odyssey — Yandex 엔터프라이즈 라인
  - 21.5 pg_stat_statements — 가장 먼저 켤 익스텐션
  - 21.6 pg_stat_activity·pg_stat_user_tables·pg_stat_user_indexes
  - 21.7 pg_stat_monitor (Percona) + pg_stat_kcache + auto_explain — 통합 옵저버빌리티
  - 21.8 postgres_exporter → Prometheus → Grafana 스택
- **독자가 얻는 것:** 운영 가시성을 갖춘 PG 클러스터의 모습.
- **분리 메모:** 4.5는 "왜 풀러가 필수인가", 21.1~21.4는 "무엇을 어떻게 고르는가". 중복 없는 layered coverage.
- **토비 진입점:** *"느린 쿼리를 찾고 싶다면 어디서 시작해야 할까? 누군가는 로그를 뒤지자 하고, 누군가는 APM부터 깔자 한다. 그런데 PG에는 더 가까운 답이 있다."*
- **예상 분량:** 26,000자 / ~30p

#### 22장. (신규) 보안과 감사 — pgaudit·RLS·SSL/TLS·CVE 추적
- **핵심 질문:** 종합 바이블이라 부르려면 보안·감사·취약점 대응을 부록이 아니라 챕터로 다뤄야 한다. DBA·Tech Lead가 의사결정에 쓸 수 있는 깊이는 무엇인가?
- **주요 내용:**
  - 22.1 인증과 암호 — scram-sha-256(기본), md5 deprecation, password 정책, `pg_hba.conf` 설계 (host/hostssl/hostnossl)
  - 22.2 전송 보안 — SSL/TLS 강제, 인증서 관리, `sslmode=verify-full`의 의미, 매니지드 PG에서의 root CA 배포
  - 22.3 권한 모델 — role 계층, GRANT/REVOKE, default privileges, schema-level 격리, 애플리케이션 계정 분리(읽기/쓰기/관리)
  - 22.4 RLS 운영 보안 — 16장 멀티테넌트 패턴의 운영 관점 (EXPLAIN에 정책 술어 보이는지, BYPASSRLS, FORCE ROW LEVEL SECURITY, admin bypass 감사 로그)
  - 22.5 감사(audit) — pgaudit 설치·설정, OBJECT vs SESSION 모드, audit log 보관·로테이션 정책, SIEM 연동 (Splunk/ELK/CloudWatch)
  - 22.6 CVE 추적과 패치 정책 — security.postgresql.org, CPM(Continuous Patch Management), 매니지드 PG의 minor upgrade 정책, 자체 운영 시 패치 윈도우 설계
  - 22.7 데이터 마스킹·익명화 — `anon` extension, dump 시점 마스킹, GDPR/PIPA 대응
  - 22.8 보안 베이스라인 체크리스트 — 신규 클러스터 D+0 / 운영 분기점검 / 사고 대응 3단계
- **독자가 얻는 것:** DBA 페르소나의 보안 의사결정 표 1장. Tech Lead의 컴플라이언스·감사 답변 자료.
- **토비 진입점:** *"보안은 사고가 나기 전에는 아무도 안 본다는 말이 있다. 그런데 PostgreSQL을 메인 DB로 쓴다면, 사고가 나기 전에 한 번은 펼쳐 봐야 할 챕터가 있다. 이번이 그 챕터다."*
- **레퍼런스 매핑:** §9.7 (한계로 자기 인식됐던 항목 — Phase 3에서 paper-research·web-research 보강 1회 권장) + §3.9 RLS 응용(16장 cross-reference) + §4.x 매니지드 PG 보안 정책.
- **리서치 보강 메모:** §9.7에 자기 인식된 한계 — pgaudit·CVE 추적 자료가 표면적. Phase 3 진입 전에 web-research·paper-research 한 라운드를 보안 키워드 한정으로 추가 권장 (목표 자료: pgaudit 공식 docs, security.postgresql.org CVE feed, AWS/GCP/Azure 보안 백서, 한국 PG 보안 가이드라인).
- **예상 분량:** 24,000자 / ~28p

#### 23장. 성능 튜닝 종합 — 인덱스부터 파티셔닝까지
- **핵심 질문:** 책에서 배운 것들을 성능 튜닝의 의사결정에서 어떻게 합쳐 쓸 것인가?
- **주요 내용:**
  - 23.1 인덱스 선택 매트릭스 — B-tree·Hash·GIN·GiST·SP-GiST·BRIN의 각각 어디서 쓰는가, 복합 인덱스 컬럼 순서, INCLUDE column, partial index
  - 23.2 EXPLAIN ANALYZE 읽기 — estimate vs actual의 갭, Buffers의 의미, BUFFERS·SETTINGS 옵션, **explain.depesz.com / pg_explain 시각화 도구 사이드바**
  - 23.3 흔한 함정 6가지 — 함수 감싸기로 인덱스 무력화, 암시적 캐스트, OR 조건의 인덱스 선택, LIKE의 leading wildcard, 통계 미수집, max_connections 과대 설정
  - 23.4 Parallel query — `parallel_workers_per_gather`, parallel-safe 함수, EXPLAIN VERBOSE 읽기
  - 23.5 Partitioning과 pg_partman 5.x — range/list/hash, 파티션 pruning, native vs declarative
  - 23.6 OS·하드웨어 레벨 체크리스트 — Linux dirty_ratio·dirty_background_ratio, transparent huge pages off, NUMA 정책, NVMe scheduler, swappiness, ext4 vs xfs (Nice 3 반영)
  - 23.7 튜닝 의사결정 흐름도 — "느린 쿼리 발견 → 21장 도구로 식별 → 23장 진단 → 5·6장 원리로 해석 → 처방"의 한 페이지 정리
- **독자가 얻는 것:** 책 전체의 성능 지식을 한 의사결정으로 합치는 경험. 23장이 끝나면 EXPLAIN 출력 한 장을 받고 "다음 한 수"를 말할 수 있다.
- **토비 진입점:** *"느린 쿼리 하나를 받았다고 해보자. 누군가는 인덱스부터 추가하자 하고, 누군가는 EXPLAIN부터 보자 한다. 둘 다 옳다. 그런데 그 두 답 사이에 있는 작은 단계들을 한 번 같이 밟아보자."*
- **예상 분량:** 28,000자 / ~32p

#### 24장. 클라우드 PostgreSQL — 벤더 매트릭스와 의사결정
- **핵심 질문:** RDS·Aurora·AlloyDB·Supabase·Neon·Crunchy·Tembo·Xata 중 어떤 기준으로 무엇을 고를 것인가?
- **주요 내용:**
  - 24.1 AWS 진영 — RDS for PostgreSQL(표준 매니지드, minor upgrade 정책)
  - 24.2 **Aurora PostgreSQL 깊이 분석** (Should 2 확장 — Aurora가 단일 절로 격상)
    - 24.2.1 PG-호환의 기술적 의미 — fork 모델·MVCC·HOT는 동일, 그런데 storage는 다르다
    - 24.2.2 disaggregated storage가 운영에 미치는 영향 — VACUUM 비용 모델, XID wraparound는 어떻게 보이는가, replication slot 동작 차이, failover slot 호환성
    - 24.2.3 OpenAurora SIGMOD 2024 paper 측정 결과 — write throughput·latency·storage cost의 실측 vs 마케팅
    - 24.2.4 "Aurora는 진짜 PG인가" 논쟁의 정직한 결론 — 어떤 워크로드에 답이고, 어떤 워크로드에 함정인가
  - 24.3 GCP 진영 — Cloud SQL(표준)과 AlloyDB(columnar engine, HTAP)
  - 24.4 Azure Database for PostgreSQL (Flexible)
  - 24.5 Supabase — 풀스택 BaaS, 무료 티어, RLS 친화
  - 24.6 Neon — 서버리스, branching, CI 친화
  - 24.7 Crunchy Bridge / Tembo / Xata — 모던 매니지드 라인
  - 24.8 의사결정 트리 — 마이그레이션 단순성(17장 참조) → write 처리량 → 분석 혼합 → 익스텐션 지원 → lock-in 허용도 순으로 가지치기
  - 24.9 함정 — 익스텐션 지원 목록 D-1 발견, minor upgrade 정책 vs 자체 운영, 비용 모델의 비교 불가 (request·storage·IOPS·egress가 벤더마다 다른 단위)
- **독자가 얻는 것:** 벤더 선택 의사결정 트리. Tech Lead 페르소나의 결론 챕터 1편.
- **토비 진입점:** *"매니지드 PostgreSQL을 고르는 일이 식당 메뉴 고르듯 쉬워 보일 때가 있다. 그런데 6개월 뒤에 후회하지 않으려면, 사진보다 재료부터 봐야 한다. 그리고 그 재료는 우리가 18~23장에서 이미 다 본 것이다."*
- **위치 이동 사유:** v1에서 17장이었으나 Part 4 끝으로 이동. 매니지드 PG 의사결정은 vacuum(18장)·HA(20장)·익스텐션(15·22장)·튜닝(23장) 운영 원리를 알아야 해석 가능하기 때문.
- **예상 분량:** 32,000자 / ~36p (v1 30,000자 + Aurora 절 확장 +2,000자)

#### 25장. 한국 사례와 다음 한 걸음
- **핵심 질문:** 한국 회사들이 PostgreSQL로 어떤 결정을 내렸고, 그것이 우리에게 어떤 다음 걸음을 가리키는가?
- **주요 내용:**
  - 25.1 카카오 클린플랫폼 CDC — 의사결정 디테일 (13장 패턴 시연의 분석편), 왜 Debezium, 무엇이 어려웠고 무엇을 얻었나
  - 25.2 카카오스타일 Bedrock — RAG + pgvector 운영, 12장 의사결정의 실제 결말
  - 25.3 당근페이 BroQuery — 분석 워크로드 PG 집중화, 15장 의사결정의 실제 결말
  - 25.4 공공 Oracle → PostgreSQL — 17장 마이그레이션의 공공 버전 (제도·감사·라이선스 차원의 결정)
  - 25.5 4건의 공통 패턴 추출 — "왜 PG였는가"의 답 4개, "무엇이 위험했는가"의 답 4개
  - 25.6 책을 덮으며 — PG와 함께 걸어갈 다음 한 걸음 (커뮤니티·KPUG·국제 컨퍼런스·기여 시작점·v19로 가는 길)
- **독자가 얻는 것:** 책 전체의 지식이 실제 한국 의사결정에서 어떻게 합쳐졌는지의 케이스 분석. 한국 페르소나를 마지막에 다시 한 번 정조준.
- **토비 진입점:** *"이제 책이 끝나간다. 머릿속에 흩어진 조각들을 한 자리에 모아보자. 실제 한국 회사들이 PostgreSQL로 어떤 결정을 내렸는지 같이 따라가면서. 그리고 그 결정의 무게를 우리 손에 가져와보자."*
- **레퍼런스 매핑:** §7.2 한국 후기 4건 + §7.x 카카오 사례 + §9.1·9.2 한계 — Phase 3 진입 전 한국 사례 보강 리서치 1회 권장 (archive.org 인용 보강 포함).
- **예상 분량:** 22,000자 / ~26p

---

### 부록 A. 참고문헌
- `01_reference.md` §8 그대로 이관 (공식 문서·논문·벤더 블로그·한국 자료·HN/Reddit)
- v1의 부록 A "MySQL → PostgreSQL 마이그레이션 체크리스트"는 17장 본문(특히 17.2 쿼리 semantics, 17.3 데이터 타입 매핑, 17.7 직후 운영 체크리스트, 17.8 매니지드 익스텐션 매트릭스)으로 흡수됨. 부록으로 별도 유지하지 않음.
- 예상 분량: 8p

---

## 분량 합계 검증 (v2)

| 구분 | 챕터 수 | 글자 수 | 페이지 |
|------|--------|--------|--------|
| Part 1 | 3 | 74,000 | ~84p (v1 76k에서 2장 다이어트 -2k) |
| Part 2 | 4 | 110,000 | ~125p (v1 108k + 5.7 신설 +2k) |
| Part 3 | 9 | 246,000 | ~281p (v1과 동일) |
| Part 4 | 9 | 242,000 | ~278p (v1 170k + 신규 17장·22장 +48k + 22장 분리·확장 +24k) |
| 부록 | 1 | 참고문헌만 | ~8p |
| **합계** | **25장 + 부록 1** | **약 672,000자** | **약 776p** |

목표(600~900p) 범위 안. 챕터별로 ±15% 변동을 허용하면 최종 분량은 720~830p. v1의 702p보다 약 74p 증가 — Critical 3건 반영의 자연스러운 결과이며, 종합 바이블 약속을 채우는 데 정당화되는 분량 증가.

---

## v1 → v2 변경 요약 (3장 정도 더 길어진 책이 무엇을 산다)

| 구분 | v1 | v2 | 변경 사유 |
|------|-----|-----|----------|
| 챕터 수 | 22장 + 부록 2 | 25장 + 부록 1 | Critical 3건 반영 |
| 보안 | 부록 끝 1p | **22장 본 챕터 24,000자** | Critical 1 — DBA·Tech Lead 페르소나 약속 |
| 마이그레이션 | 부록 A 8,000자 | **17장 본 챕터 24,000자 (Part 4 시작 가교)** | Critical 3 — MySQL 베테랑 서사 도착점 |
| 22장 (구) | 성능+한국+결론 1챕터 30k | **23장 성능 28k + 25장 한국·결론 22k** | Critical 2 — 3주제 1챕터 밀도 과다 해소 |
| 클라우드 (구 17장) | Part 4 시작 | **24장 (Part 4 끝)** | Should 1 — 운영 원리 후 의사결정 인과 정합 |
| Aurora | 17.9 한 항목 | **24.2 단일 절 4꼭지 +3,000자** | Should 2 — 자료 두께와 Tech Lead 의사결정 무게 |
| 5장 bloat 결말 | 없음 | **5.7 +2,000자** | Should 4 — 5장과 18장의 인과 사슬 닫기 |
| 4장 풀러 결론 | "21장 예고편" | **4.5 fork 모델 결과로서의 풀러 당위성** | Nice 1 — 4장과 21장 분리 기준 본문화 |
| 3장↔8장 분리 기준 | 미명시 | **챕터 메모에 명시 (release note vs 표현력 깊이)** | Nice 2 — 챕터 저술 단계 가이드 |
| 페일오버 훈련 (20.6) | 한 줄 | **시나리오 한 개 깊이 +2,000자** | 챕터별 코멘트 반영 |
| OS 튜닝 (23.6) | 없음 | **신설 1절** | Nice 3 — DBA 야간 호출 영역 |
| sharding 일반론 (15.2) | Citus만 | **postgresql.kr 자료의 sharding 일반론 1꼭지** | 누락 토픽 표 5번 |
| EXPLAIN 시각화 (23.2) | 없음 | **사이드바 추가** | 누락 토픽 표 6번 |
| pg_stat_kcache·auto_explain (21.7) | 미명시 | **21.7에 흡수** | 누락 토픽 표 7번 |

미반영(Nice 또는 자료 부족 항목): Patroni vs Stolon vs repmgr 비교 확장(20장 안에서 챕터 저술 단계 결정), PostgresML(12장 짧은 언급 유지).

---

## 자기 점검 — book-planning 체크리스트 (v2)

- [x] 모든 챕터가 핵심 질문에 답하고 있는가? — 25장 전부 핵심 질문 명시
- [x] 챕터 순서에 맥이 흐르는가? — Part 구조로 진입→정체성→활용→운영. 9개 시나리오는 전통→신규 순. Part 4는 마이그레이션(가교)→코어 운영(VACUUM/백업/HA/풀러)→보안→튜닝→클라우드→결론으로 인과 사슬 명확
- [x] 대상 독자 수준에 맞는가? — 중급 기본, 일부 고급. 페르소나별 추천 경로 v2 갱신 완료 (3종 모두 신규 17·22·24·25장 반영)
- [x] 레퍼런스의 주요 자료가 빠짐없이 배치되는가? — §1~§7 모두 챕터에 매핑. §9.7 보안 한계는 22장 본 챕터로 승격(Phase 3 보강 리서치 1회 권장 메모). §2·§7.2 마이그레이션 자료는 17장으로 승격
- [x] 챕터 간 중복이 없는가? — 분리 메모를 5쌍에 명시 (2장↔17장, 3장↔8장, 4장↔21장, 5장↔18장, 13.6↔25.1, 16.5↔22.4)
- [x] 각 챕터 예상 분량 합계가 목표 분량에 부합하는가? — 약 776p, 목표 600~900p 안

---

## 리서치 보강이 필요한 챕터 (Phase 3 진입 전)

v2에서 신설된 챕터 또는 자료 한계가 명시된 챕터:

| 챕터 | 보강 키워드 | 우선순위 | 비고 |
|------|------------|---------|------|
| 17장 (마이그레이션 신규) | "한국 PG 마이그레이션 후기" 추가 4건, archive.org 카카오 본문, ora2pg 최신 베스트 프랙티스 | 높음 | 신규 챕터, 케이스 두께 필요 |
| 22장 (보안 신규) | pgaudit 공식 docs, security.postgresql.org CVE feed, AWS/GCP/Azure 보안 백서, 한국 PG 보안 가이드라인 | 높음 | 신규 챕터, §9.7 한계 직접 보강 |
| 25장 (한국 사례) | 카카오 클린플랫폼 본문(archive), 토스·우아한형제들·네이버·라인 PG 자료 | 중 | §9.1·9.2 한계 보강 |
| 13장 (이벤트·큐) | 카카오 CDC 본문 일부 인용 보강 | 중 | §9.2 한계 |
| 24장 (클라우드, Aurora 확장) | OpenAurora SIGMOD 2024 본문, AWS re:Invent 2024·2025 Aurora 세션 노트 | 중 | Should 2 확장에 필요한 깊이 |

Phase 3 챕터 저술 진입 시 각 챕터를 쓰기 직전에 키워드 한정 web-research·community-research·paper-research 1라운드씩 권장.
