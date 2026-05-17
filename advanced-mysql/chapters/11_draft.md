# 11장. AWS RDS와 Aurora — 인스턴스 선택·복제·분할의 분기점

"우리 서비스에 Aurora를 써야 할까요, RDS로 충분할까요?"

이 질문은 스프링 개발자가 인프라를 처음 결정할 때 가장 많이 마주치는 질문 중 하나다. 답을 먼저 말하면 — 상황에 따라 다르다. 이렇게 말하면 무책임하게 들릴 수 있지만, 진짜 핵심은 어떤 기준으로 상황을 판단하느냐다. 이 장에서는 그 기준을 네 가지 분기점으로 정리하고, 실제 운영 사례를 통해 각각의 무게를 느껴보자.

---

## RDS for MySQL과 Aurora MySQL — 같은 MySQL, 다른 엔진

이름은 비슷하지만 내부는 상당히 다르다.

**RDS for MySQL**은 MySQL 엔진을 AWS가 관리해주는 서비스다. 일반 MySQL과 아키텍처가 거의 같다. EC2 인스턴스 위에 MySQL이 올라가고, EBS 볼륨이 스토리지를 담당한다. 리플리카는 binlog를 통해 비동기 복제된다.

**Aurora MySQL**은 다르다. MySQL 호환 인터페이스를 제공하지만 스토리지 레이어가 완전히 새로 설계됐다. 3개의 가용 영역(AZ)에 걸쳐 데이터를 6개 복사본으로 분산 저장한다. 이 6-way 복제 스토리지가 Aurora의 핵심이다.

```
Aurora 스토리지 구조:

  Write Instance
       |
  Redo Log만 전송 (바이너리 로그 아님)
       |
  ┌────────────────────────────────────────┐
  │          분산 스토리지 레이어           │
  │  AZ-1       AZ-2        AZ-3          │
  │  [복사본1]  [복사본3]   [복사본5]      │
  │  [복사본2]  [복사본4]   [복사본6]      │
  └────────────────────────────────────────┘
       |             |             |
  Read    Read    Read    Read   ...
  Replica Replica Replica Replica (최대 15개)
```

Aurora는 redo 로그만 스토리지로 전송한다. 리플리카는 같은 분산 스토리지를 공유하므로 binlog 복제가 필요 없다. 그 결과 리플리카 lag이 일반 MySQL 복제의 초~분 단위가 아닌 밀리초 수준에 머문다.

---

## 네 가지 분기점

### 분기점 1: 읽기 확장이 필요한가?

RDS for MySQL은 리플리카를 최대 5개까지 추가할 수 있다. Aurora MySQL은 최대 15개까지 가능하다.

더 중요한 건 lag이다. RDS의 비동기 복제에서는 리플리카가 몇 초씩 뒤처질 수 있다. 이 상태에서 리플리카로 읽기 요청을 보내면 오래된 데이터를 돌려줄 수 있다. Aurora는 밀리초 수준 lag이라 리플리카를 적극적으로 활용할 수 있다.

```sql
-- RDS: 복제 lag 확인
SHOW SLAVE STATUS\G
-- Seconds_Behind_Master: 최대 몇 초 뒤처졌는지

-- Aurora: 버전 토큰 기반 읽기 일관성도 지원
-- (application 레이어에서 aurora_replica_read_consistency 설정 가능)
```

읽기 트래픽이 쓰기의 5~10배 이상이고, 읽기 일관성에 민감하다면 Aurora가 더 맞는 선택이다.

### 분기점 2: 페일오버 RTO가 중요한가?

RTO(Recovery Time Objective)는 장애 발생 후 서비스를 복구하는 데 걸리는 목표 시간이다.

RDS for MySQL의 Multi-AZ 페일오버는 약 60~120초가 걸린다. DNS 업데이트와 새 인스턴스의 MySQL 기동이 포함된다.

Aurora는 15~30초다. 공유 스토리지 덕분에 리플리카를 Writer로 승격할 때 데이터를 다시 동기화할 필요가 없기 때문이다. 리플리카는 이미 최신 데이터를 갖고 있다.

금융 서비스처럼 몇 십 초의 장애도 민감한 영역이라면 Aurora 쪽 RTO가 유리하다. 반면 배치 처리 위주라면 수분 단위 페일오버도 감수할 수 있다.

### 분기점 3: IO 집약적 워크로드인가?

Aurora의 스토리지는 IO 요청마다 비용이 발생한다. 쓰기가 많은 워크로드에서는 I/O 비용이 상당히 올라간다. AWS는 이를 위해 "Aurora I/O-Optimized" 요금 모델을 내놓았는데, IO 비용 대신 인스턴스 요금이 올라가는 구조다. 어느 쪽이 더 저렴한지는 실제 워크로드 패턴과 최신 가격에 따라 달라지니, 직접 AWS 비용 계산기로 확인하는 편이 낫다.

순수 읽기 위주(OLTP에서 95% 이상 읽기)이거나, 쓰기가 빈번하면서 비용에 민감하다면 RDS의 예측 가능한 EBS 비용이 더 단순할 수 있다.

### 분기점 4: 벤더 락-인을 감수할 수 있나?

Aurora MySQL은 MySQL 호환을 표방하지만 일부 동작이 다르다. Aurora 고유 함수, 스토리지 파라미터, DDL 동작 등이 표준 MySQL과 미묘하게 다를 수 있다. 나중에 Aurora를 벗어나 다른 MySQL 환경으로 이전해야 한다면 번거로운 일이 생길 수 있다.

단순한 워크로드이고 이식성이 중요하다면 RDS for MySQL이 더 안전한 선택일 수 있다.

---

## Aurora MySQL의 대용량 DDL 약점

Aurora가 모든 면에서 우위인 것은 아니다. 주목할 만한 약점이 있다. 우아한형제들의 경험이 여기서 중요한 참고가 된다.

200GB 테이블에 인덱스를 추가하는 작업이 Aurora MySQL에서 1시간 이상 걸렸다. Aurora의 분산 스토리지 구조가 대용량 DDL에서는 오히려 병목이 됐다는 이야기다. 같은 상황에서 PostgreSQL의 partial index는 약 40분에 끝났다고 한다.

대용량 테이블에 인덱스를 무중단으로 추가해야 한다면 `pt-online-schema-change`나 `gh-ost` 같은 도구를 진지하게 고려해야 한다.

```sql
-- pt-online-schema-change 사용 예시 (Aurora/RDS 모두 가능)
-- 실제 실행은 pt-osc 도구를 CLI에서
-- pt-online-schema-change \
--   --alter "ADD INDEX idx_created_at (created_at)" \
--   --execute \
--   D=mydb,t=orders

-- gh-ost는 binlog 기반으로 동작 (Aurora에서는 binlog 활성화 필요)
-- gh-ost \
--   --host=aurora-cluster.cluster-xxx.ap-northeast-2.rds.amazonaws.com \
--   --database=mydb \
--   --table=orders \
--   --alter="ADD INDEX idx_created_at (created_at)" \
--   --execute
```

Aurora에서 gh-ost를 쓰려면 binlog를 명시적으로 활성화해야 한다. Aurora는 기본적으로 내부 redo 로그만 쓰고 binlog는 선택 사항이다. gh-ost가 binlog를 파싱해 변경을 추적하기 때문에 이 설정이 필요하다.

---

## Aurora vs RDS 백업 모델 차이

백업·복구·PITR 워크플로의 실제 운영은 다음 12장에서 자세히 다룬다. 여기서는 두 서비스의 백업 모델 차이만 짧게 짚고 가자.

**RDS for MySQL**은 자동 백업(1~35일 보관), 수동 스냅샷, binlog 기반 PITR을 제공한다. PITR 복구는 가장 가까운 자동 백업 스냅샷을 기점으로 binlog를 적용하는 방식이다.

**Aurora MySQL**은 자동 백업이 분산 스토리지에 지속적으로 기록된다. 백업 윈도우가 따로 없고, 1초 단위 PITR이 가능하다. 스냅샷도 증분 방식이라 빠르다.

실제 RPO(목표 복구 지점)나 RTO를 측정하는 방법, 분기별 PITR 리허설 워크플로는 12장에서 함께 실습해보자.

---

## 복제: GTID, 반동기, 그룹 복제

### GTID: 복제 위치 추적의 혁신

GTID(Global Transaction Identifier)는 `server_uuid:transaction_number` 형식으로 각 트랜잭션에 전역 고유 식별자를 붙인다. 이전의 binlog 파일명 + 위치 기반 복제에 비해 페일오버가 훨씬 단순해진다.

```sql
-- GTID 기반 복제 설정 확인
SHOW VARIABLES LIKE 'gtid_mode';
-- gtid_mode: ON

SHOW MASTER STATUS;
-- 현재 GTID 위치 확인

-- 리플리카에서 복제 상태 확인
SHOW REPLICA STATUS\G
-- Executed_Gtid_Set: 이미 적용된 GTID 집합
-- Retrieved_Gtid_Set: 소스에서 받은 GTID 집합
```

GTID가 활성화된 환경에서는 리플리카를 새 소스로 승격할 때 binlog 파일명과 위치를 직접 계산할 필요가 없다. 리플리카가 어떤 트랜잭션을 가지고 있는지가 GTID로 명확히 표현되기 때문이다.

단, GTID 환경에서는 제약도 있다. `CREATE TABLE ... SELECT`나 일부 비트랜잭션 명령은 GTID와 충돌할 수 있다. 레거시 코드에 이런 패턴이 있다면 마이그레이션 전에 점검해야 한다.

### 반동기 복제: 데이터 손실과 성능의 균형

기본 비동기 복제는 빠르지만 소스 장애 시 아직 리플리카에 전달되지 않은 트랜잭션을 잃을 수 있다. 반동기 복제는 최소 하나의 리플리카가 트랜잭션을 받았다는 ACK를 응답할 때까지 커밋을 기다린다.

```sql
-- 반동기 복제 플러그인 확인
SHOW PLUGINS;
-- rpl_semi_sync_source_enabled (소스)
-- rpl_semi_sync_replica_enabled (리플리카)

-- 타임아웃 설정 (1000ms)
SET GLOBAL rpl_semi_sync_source_timeout = 1000;
-- 타임아웃 초과 시 비동기로 폴백
```

반동기의 타임아웃 폴백이 중요하다. 리플리카가 느리거나 네트워크가 불안정하면 타임아웃 후 비동기로 자동 전환된다. 이 폴백을 모르고 있으면 "반동기 설정했는데 왜 데이터가 사라졌죠?"라는 당황스러운 상황을 만날 수 있다.

### 그룹 복제(MGR)와 InnoDB Cluster

그룹 복제는 Paxos 합의 알고리즘으로 여러 노드가 합의하에 커밋한다. 자동 페일오버와 멀티-마스터(단, 충돌 감지 있음) 모드를 지원한다.

InnoDB Cluster는 MGR + MySQL Shell + MySQL Router를 묶은 솔루션으로, 클러스터 관리와 애플리케이션 라우팅을 패키지로 제공한다.

단, MGR에는 몇 가지 제약이 있다.

```sql
-- MGR 전제 조건 확인
-- 1. 모든 테이블에 PK 필수
SELECT t.TABLE_SCHEMA, t.TABLE_NAME
FROM information_schema.TABLES t
LEFT JOIN information_schema.TABLE_CONSTRAINTS tc
    ON t.TABLE_SCHEMA = tc.TABLE_SCHEMA
    AND t.TABLE_NAME = tc.TABLE_NAME
    AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
WHERE t.TABLE_TYPE = 'BASE TABLE'
    AND t.TABLE_SCHEMA NOT IN ('mysql', 'sys', 'information_schema', 'performance_schema')
    AND tc.CONSTRAINT_NAME IS NULL;
-- PK 없는 테이블은 MGR에서 허용되지 않는다

-- 2. InnoDB 스토리지 엔진만 지원
SELECT TABLE_SCHEMA, TABLE_NAME, ENGINE
FROM information_schema.TABLES
WHERE ENGINE != 'InnoDB'
    AND TABLE_SCHEMA NOT IN ('mysql', 'sys', 'information_schema', 'performance_schema');
```

MGR은 최대 9개 노드까지만 지원하고, 피크 처리량은 반동기보다 낮을 수 있다. 자동 페일오버 자체가 목적이고 단순성보다 고가용성이 더 중요하다면 고려해볼 만하다.

---

## 파티셔닝 vs 샤딩 — 경계선 이해하기

테이블이 수억 건을 넘어가면 "파티션을 나눠야 할까, 샤딩을 해야 할까?"는 자연스러운 고민이다. 이 둘의 경계를 명확히 하자.

**파티셔닝**은 단일 인스턴스 안에서 테이블을 물리적으로 분할한다. 애플리케이션은 여전히 같은 테이블 이름으로 접근하고, MySQL이 파티션 키를 보고 어느 파티션으로 갈지 라우팅한다.

**샤딩**은 여러 인스턴스에 데이터를 나눠 저장한다. 애플리케이션이나 미들웨어(ProxySQL, Vitess 등)가 어느 인스턴스로 요청을 보낼지 결정한다.

```sql
-- RANGE 파티셔닝 예시: 날짜 기반
CREATE TABLE orders (
    id        BIGINT NOT NULL,
    user_id   BIGINT NOT NULL,
    created_at DATETIME NOT NULL,
    status    VARCHAR(20) NOT NULL,
    amount    DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id, created_at)  -- 파티션 키는 PK에 포함되어야 함
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 파티션 정보 확인
SELECT PARTITION_NAME, TABLE_ROWS, DATA_LENGTH
FROM information_schema.PARTITIONS
WHERE TABLE_SCHEMA = 'mydb' AND TABLE_NAME = 'orders';
```

파티션 pruning이 작동하려면 WHERE 절에 파티션 키가 반드시 들어와야 한다. `WHERE created_at >= '2024-01-01'`이면 p2024 파티션만 접근한다. 하지만 `WHERE user_id = 123`처럼 파티션 키가 없으면 모든 파티션을 풀스캔한다.

```sql
-- 파티션 pruning 확인
EXPLAIN SELECT * FROM orders WHERE created_at >= '2024-01-01';
-- partitions: p2024,p_future  ← pruning 작동

EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- partitions: p2022,p2023,p2024,p_future  ← 모든 파티션 접근!
```

파티셔닝의 또 다른 제약은 FK를 쓸 수 없다는 점이다. 파티셔닝된 테이블은 FK 제약의 부모나 자식이 될 수 없다. 도메인 정합성을 FK로 보장하던 설계라면 파티셔닝 도입 시 이 부분을 애플리케이션 레이어에서 처리해야 한다.

반면 샤딩은 단일 인스턴스의 CPU/메모리/스토리지 한계를 넘을 수 있다는 장점이 있다. 하지만 크로스-샤드 조인, 분산 트랜잭션, 샤드 키 선택의 복잡성이 운영 비용을 크게 높인다.

파티셔닝으로 충분한지, 샤딩이 필요한지의 기준으로는 다음을 생각해보자. 단일 인스턴스의 IOPS나 스토리지 한계에 닿았는가? 쿼리 패턴이 파티션 키를 항상 포함하는가? 파티션 키로 자연스럽게 범위를 나눌 수 있는가? 이 세 가지가 모두 맞다면 파티셔닝이 더 단순한 출발점이다.

---

## 의사결정 카드 — 우리 서비스의 분기점 정리

이 장 내용을 의사결정 표로 정리해보자. 이 표를 우리 서비스의 실제 수치로 채워보는 것이 이 장의 가장 실용적인 연습이다.

| 분기점 | 우리 워크로드 | RDS | Aurora |
|--------|--------------|-----|--------|
| 읽기 확장 | 리플리카 몇 개? lag 허용 범위? | 최대 5개, 수 초 lag | 최대 15개, ms lag |
| 페일오버 RTO | 허용 다운타임? | 60~120초 | 15~30초 |
| IO 집약도 | 초당 쓰기 건수? | EBS IOPS 예측 가능 | I/O 비용 또는 I/O-Optimized |
| 벤더 락-인 | 이식성 중요? | MySQL 표준 | Aurora 고유 동작 있음 |

이 표에 우리 서비스의 수치를 채워보면 답이 보이기 시작한다. "Aurora가 좋다"거나 "RDS면 충분하다"는 식의 단정은 피하자. 워크로드를 모르고 내리는 결론은 장담할 수 없다.

---

## 마무리

RDS와 Aurora는 같은 MySQL 호환이지만 아키텍처가 다르다. 읽기 확장, 페일오버 RTO, IO 패턴, 락-인 감수 여부 — 이 네 가지를 우리 서비스 맥락에서 따져보면 선택의 윤곽이 나온다.

Aurora의 6-way 분산 스토리지는 읽기 확장과 빠른 페일오버라는 강점을 주지만, 대용량 DDL에서는 약점이 있다. 200GB 테이블 인덱스 추가는 `pt-online-schema-change`나 `gh-ost`로 무중단 처리하는 것이 안전하다.

복제는 GTID가 페일오버를 단순화하고, 반동기는 데이터 손실 위험을 줄이지만 타임아웃 폴백을 잊지 말자. 파티셔닝은 단일 인스턴스 안에서 테이블을 나누는 것이고, 샤딩은 인스턴스를 나누는 것이다 — 이 경계를 명확히 인식하고 필요에 따라 단계적으로 접근하는 편이 낫다.

다음 장에서는 운영의 눈을 키운다. 데이터베이스가 보내는 이상 신호를 어떻게 듣는지, 백업과 DR을 어떻게 일상으로 만드는지를 함께 살펴보자.

---

## 참고 자료

- Mydbops — AWS MySQL RDS vs Aurora performance: https://www.mydbops.com/blog/aws-mysql-rds-vs-aurora-vs-serverless-performance
- Bytebase — Aurora vs RDS engineering guide 2025: https://www.bytebase.com/blog/aurora-vs-rds/
- Percona — Aurora vs RDS: https://www.percona.com/blog/when-should-i-use-amazon-aurora-and-when-should-i-use-rds-mysql/
- 우아한형제들 — Aurora MySQL vs Aurora PostgreSQL: https://techblog.woowahan.com/6550/
- AWS Aurora features: https://aws.amazon.com/rds/aurora/features/
- AWS Major version upgrades for RDS for MySQL: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.Major.html
- MySQL — Group Replication: https://dev.mysql.com/doc/refman/8.0/en/group-replication.html
- Percona — The Ultimate Guide to MySQL Partitions: https://www.percona.com/blog/what-is-mysql-partitioning/
