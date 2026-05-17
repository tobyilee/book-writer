# 12장. 운영의 눈 — 관측, 보안, 백업·복구·DR

월요일 오전 9시, 슬랙에 알림이 뜬다. "결제 API 응답이 늘었어요." 대시보드를 열면 CPU는 30%대, 메모리도 정상, 에러율도 없다. 그런데 응답 시간이 갑자기 두 배로 올라갔다. 무엇이 문제일까?

DB를 운영해본 사람은 안다. 숫자가 녹색이어도 안심할 수 없다. DB는 말이 없다. 이상 신호를 보내도 우리가 제대로 듣지 못하면 그냥 지나친다. DB가 보내는 신호를 어떻게 듣고, 장애가 일어났을 때 어떻게 복구하며, 그 복구를 일상으로 만드는 방법을 함께 살펴보자.

---

## sys와 performance_schema — 어디서 켜고 어디서 멈출까

MySQL 8.0부터 `performance_schema`(이하 PS)는 기본으로 켜져 있다. 하지만 모든 instrument를 다 ON으로 두면 어떻게 될까? LINE Engineering이 실측한 결과, 전체 instrument를 켰을 때 TPS가 약 15% 하락했다. 운영 환경에서 15%는 작은 숫자가 아니다.

찜찜한 선택을 해야 한다. 다 켜면 정보는 많지만 성능이 줄고, 필요한 것만 켜면 놓치는 신호가 있을 수 있다.

실용적인 원칙은 이렇다. **필요한 것만, 필요한 순간에 켜자.**

```sql
-- 현재 켜진 consumer 확인
SELECT NAME, ENABLED
FROM performance_schema.setup_consumers
ORDER BY NAME;

-- 현재 켜진 instrument 중 일부 확인
SELECT NAME, ENABLED, TIMED
FROM performance_schema.setup_instruments
WHERE NAME LIKE 'wait/lock/%'
ORDER BY NAME;

-- 락 관련 instrument만 켜기 (성능 영향 최소화)
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'wait/lock/innodb/%';

-- statement instrument (슬로우 쿼리 분석용)
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'statement/%';
```

`sys` 스키마는 PS 위에서 사람이 읽기 쉬운 뷰를 제공한다. PS를 직접 쿼리하는 것보다 sys 뷰가 훨씬 편리하다.

```sql
-- 현재 실행 중인 쿼리 (1초 이상 걸리는 것)
SELECT * FROM sys.processlist
WHERE time > 1
ORDER BY time DESC;

-- 가장 오래 실행된 쿼리 TOP 10
SELECT query, exec_count, avg_latency, rows_examined_avg
FROM sys.statement_analysis
ORDER BY avg_latency DESC
LIMIT 10;

-- 테이블별 IO 통계
SELECT table_schema, table_name,
       count_read, count_write,
       sum_timer_read / 1000000000000 AS read_sec,
       sum_timer_write / 1000000000000 AS write_sec
FROM sys.schema_table_statistics
ORDER BY sum_timer_read + sum_timer_write DESC
LIMIT 10;
```

---

## 핵심 지표 — 무엇을 보아야 하는가

대시보드에 지표가 수십 개 있지만, 매일 챙겨야 할 것은 몇 가지로 압축된다.

### 버퍼풀 히트율

버퍼풀 히트율이 99% 아래로 내려가면 디스크 IO가 늘고 있다는 신호다.

```sql
-- 버퍼풀 히트율 계산
SELECT
    (1 - (
        SELECT VARIABLE_VALUE FROM performance_schema.global_status
        WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads'
    ) / (
        SELECT VARIABLE_VALUE FROM performance_schema.global_status
        WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests'
    )) * 100 AS buffer_pool_hit_rate_pct;
```

히트율이 95% 아래라면 버퍼풀 크기를 키우는 것을 고려해볼 수 있다. 가용 RAM의 70~80%가 일반적인 시작점이다. 단, 크기를 무작정 키우기 전에 어떤 쿼리/테이블이 많은 IO를 유발하는지 먼저 파악하는 편이 낫다.

### Threads_running

```sql
-- 현재 실행 중인 스레드 수
SHOW STATUS LIKE 'Threads_running';

-- 정상 범위: 인스턴스 CPU 코어 수 이하
-- 갑자기 급증하면 쿼리 병목 신호
```

`Threads_running`이 CPU 코어 수를 크게 넘으면 대기가 쌓이고 있다는 뜻이다. 이때 `sys.processlist`나 `SHOW PROCESSLIST`로 어떤 쿼리가 오래 실행 중인지 확인해보자.

### 락 대기 지표

```sql
-- 락 대기 평균 시간
SHOW STATUS LIKE 'Innodb_row_lock_time_avg';

-- 현재 락 대기 중인 트랜잭션
SELECT
    r.trx_id AS waiting_trx_id,
    r.trx_mysql_thread_id AS waiting_thread,
    r.trx_query AS waiting_query,
    b.trx_id AS blocking_trx_id,
    b.trx_mysql_thread_id AS blocking_thread,
    b.trx_query AS blocking_query
FROM information_schema.innodb_lock_waits w
JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;
```

`Innodb_row_lock_time_avg`가 높아지면 락 경합이 증가하고 있다는 신호다. 어떤 쿼리가 서로를 막고 있는지 위 쿼리로 확인할 수 있다.

### 복제 lag

```sql
-- 8.0 이전 방식 (덜 정확)
SHOW REPLICA STATUS\G
-- Seconds_Behind_Source 값

-- 8.0+ PS 기반 (더 정확)
SELECT
    channel_name,
    applying_transaction,
    applying_transaction_original_commit_timestamp,
    applying_transaction_immediate_commit_timestamp,
    TIMESTAMPDIFF(
        SECOND,
        applying_transaction_original_commit_timestamp,
        NOW()
    ) AS lag_seconds
FROM performance_schema.replication_applier_status_by_worker;
```

`Seconds_Behind_Source`는 허점이 있다. 리플리카가 SQL thread를 멈추면 0으로 보이거나, 네트워크 지연에 의한 lag과 SQL 처리 지연을 구분하지 못한다. PS의 `replication_applier_status_by_worker`에서 timestamp를 비교하는 방식이 더 정확하다.

---

## 슬로우 쿼리 로그와 pt-query-digest

슬로우 쿼리 로그는 운영에서 가장 중요한 진단 도구 중 하나다.

```sql
-- 슬로우 쿼리 로그 설정 확인
SHOW VARIABLES LIKE 'slow_query_log%';
SHOW VARIABLES LIKE 'long_query_time';

-- 동적으로 켜기 (재시작 없이)
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;        -- 1초 이상
SET GLOBAL log_queries_not_using_indexes = 'ON';  -- 인덱스 미사용 쿼리도
```

슬로우 쿼리 로그가 쌓이면 `pt-query-digest`로 분석해보자. 이 도구는 같은 패턴의 쿼리를 그룹핑해 실행 횟수, 평균 시간, 최대 시간, 실행 시간 합계를 보여준다.

```bash
# pt-query-digest 분석 예시
pt-query-digest /var/lib/mysql/slow.log \
  --limit 10 \
  --since "2024-01-15 09:00:00" \
  --until "2024-01-15 10:00:00"

# 분석 결과 구조:
# Profile
# Rank  Query ID  Response time  Calls  R/Call  ...
# 1     0xABCD    45.32 (32%)    1243   0.0365  SELECT orders WHERE ...
# 2     0xEFGH    38.11 (27%)    891    0.0428  UPDATE payment WHERE ...
```

응답 시간 합계가 높은 쿼리가 1순위 개선 대상이다. `EXPLAIN ANALYZE`로 분해하고(5장 도구 호출), 인덱스를 추가하거나 쿼리를 재작성한다.

---

## 백업·복구·PITR — 일상 운영 워크플로

백업을 한 번도 복구해보지 않은 사람은 백업이 있다고 할 수 없다.

이 문장이 과하게 들린다면, 실제로 백업 파일이 있는데 복구를 시도하니 mysqldump 포맷이 맞지 않아 임포트가 안 됐다는 이야기, 자동 백업이 켜져 있다고 생각했는데 보존 기간이 1일로 설정돼 있었다는 이야기를 주변에서 꽤 많이 들을 수 있다. 백업은 복구 테스트를 해봐야 진짜 백업이다.

### mysqldump 기반 논리 백업

```bash
# 전체 DB 덤프 (논리 백업)
mysqldump \
  --single-transaction \     # InnoDB: 일관된 스냅샷 (FLUSH TABLES WITH READ LOCK 최소화)
  --routines \               # 스토어드 프로시저/함수 포함
  --triggers \               # 트리거 포함
  --hex-blob \               # BLOB을 헥스로
  -u root -p mydb \
  > mydb_backup_20240115.sql

# 복구
mysql -u root -p mydb < mydb_backup_20240115.sql
```

`--single-transaction`은 InnoDB에서 일관된 스냅샷을 덤프하기 위한 핵심 옵션이다. REPEATABLE READ 격리수준에서 읽기 전용 트랜잭션을 열어 덤프하기 때문에 다른 쓰기 트랜잭션을 차단하지 않는다. MyISAM 테이블이 없는 한 이 옵션을 항상 켜두는 편이 낫다.

### Binlog 기반 PITR

자동 백업 스냅샷 이후에 발생한 변경을 복구하려면 binlog가 필요하다.

```bash
# binlog에서 특정 시점까지 이벤트 추출
mysqlbinlog \
  --start-datetime="2024-01-15 09:00:00" \
  --stop-datetime="2024-01-15 09:45:00" \
  /var/lib/mysql/binlog.000123 \
  > pitr_replay.sql

# 특정 위치까지 추출
mysqlbinlog \
  --start-position=4 \
  --stop-position=1234567 \
  /var/lib/mysql/binlog.000123 \
  > pitr_replay.sql

# 추출한 이벤트 적용
mysql -u root -p < pitr_replay.sql
```

실수로 `DROP TABLE`이나 `DELETE FROM` 을 날렸다면 어떻게 복구할까. 절차는 이렇다.

1. 스냅샷에서 복구 인스턴스를 만든다
2. 해당 스냅샷 이후의 binlog를 찾는다
3. 실수 발생 직전 시점까지만 `mysqlbinlog`로 추출해 적용한다

이 과정이 머릿속에 그려지는 사람과 그렇지 않은 사람은 장애 상황에서 완전히 다른 반응을 보인다.

### AWS 자동 백업과 PITR

AWS RDS/Aurora 환경에서는 자동 백업이 지속적으로 쌓이고, 콘솔에서 원하는 시점으로 복원할 수 있다.

```bash
# AWS CLI로 특정 시점 복원 (RDS)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier mydb-prod \
  --target-db-instance-identifier mydb-restored \
  --restore-time 2024-01-15T09:45:00Z \
  --db-instance-class db.r6g.xlarge

# 복원 완료 대기
aws rds wait db-instance-available \
  --db-instance-identifier mydb-restored
```

복원에 걸리는 시간을 한 번이라도 재봐야 RTO를 약속할 수 있다. "AWS가 알아서 해준다"고 믿는 것과 실제로 측정해본 것은 다르다.

### 분기별 PITR 리허설 워크플로

잊지 말아야 할 점이 있다. 백업을 분기마다 실제로 복구 테스트해보는 것은 의무다.

다음은 분기마다 실행하는 리허설 체크리스트다.

```
# PITR 리허설 체크리스트 (분기 1회)

□ 1. 테스트 시나리오 선정
   - 실수로 특정 테이블 데이터 삭제
   - 스냅샷 기준 시점 + N분 후까지 복구

□ 2. 복구 인스턴스 생성
   - 최신 스냅샷에서 새 인스턴스 생성
   - 또는 RDS/Aurora PITR API 사용

□ 3. binlog 적용 (자체 관리 MySQL)
   - 스냅샷 이후 binlog 추출
   - 목표 시점 직전까지만 적용

□ 4. 데이터 검증
   - 복구 대상 테이블 row 수 확인
   - 애플리케이션 단위 테스트 실행

□ 5. RTO/RPO 측정
   - 복구 시작 → 완료까지 시간 기록
   - 마지막 커밋 → 복구 데이터 간격 기록

□ 6. 결과 기록
   - 이슈 발견 시 다음 분기 전 해결
   - 측정값 변화 추세 관리
```

이 워크플로를 처음 실행했을 때 예상치 못한 문제를 발견하는 경우가 많다. 백업 보존 기간이 짧았거나, binlog가 제대로 쌓이지 않았거나, 복구에 예상보다 4배가 걸리거나. 장애 때 처음 알게 되는 것과 리허설에서 알게 되는 것은 완전히 다른 상황이다.

---

## 다중 리전 DR 토폴로지

토스는 SLASH 21에서 자사의 MySQL HA/DR 토폴로지를 공유했다. 24/7 금융 서비스가 어떻게 데이터베이스 장애를 설계하는지를 잘 보여주는 사례다.

GTID 기반 복제로 여러 리전에 리플리카를 배치하고, 장애 시 MHA(Master High Availability)나 orchestrator로 자동 페일오버를 수행하는 구조다. 핵심은 두 가지다.

첫째, **페일오버 자동화**. 사람이 새벽 3시에 직접 명령어를 치지 않아도 시스템이 스스로 판단하고 새 Writer를 선출한다.

둘째, **페일오버 후 무결성 확인**. 자동으로 페일오버됐어도 데이터 손실이 없는지, 이전 Writer에서 커밋되지 않은 트랜잭션이 있는지를 orchestrator가 점검한다.

DR 설계 시 고려해두어야 할 RTO/RPO 약속의 두 축이 있다.

- **RPO(Recovery Point Objective)**: 데이터를 어디까지 잃어도 되는가. 0이면 데이터 손실 없음, 30초면 30초치 데이터는 잃을 수 있다는 뜻.
- **RTO(Recovery Time Objective)**: 장애 후 서비스를 얼마나 빨리 복구해야 하는가. 60초면 장애 발생 후 60초 안에 서비스가 다시 정상이어야 한다.

이 두 값을 서비스 팀과 명확히 합의하고 문서화해두는 편이 낫다. 장애 현장에서 "RTO가 얼마죠?"를 처음 논의하면 난감하다.

```sql
-- GTID 기반 페일오버 상태 확인
-- 현재 Writer의 GTID 위치
SHOW MASTER STATUS;
-- File: binlog.000456
-- Position: 789012
-- Executed_Gtid_Set: aaaa-bbbb-cccc:1-12345

-- 리플리카의 GTID 적용 상태
SHOW REPLICA STATUS\G
-- Executed_Gtid_Set: aaaa-bbbb-cccc:1-12340  ← 5 트랜잭션 뒤처짐
```

---

## 평시에 메이저 업그레이드를 결심하게 만드는 신호

여기서는 메이저 업그레이드 절차를 다루지 않는다(14장이 그 몫이다). 다만 업그레이드를 언제 결심해야 하는지의 신호는 운영 일상에서 만난다.

**통계 갱신 빈도가 높다.** 데이터 분포가 변했는데 통계가 따라가지 못하면 옵티마이저가 잘못된 실행 계획을 잡는다. 8.4 LTS의 히스토그램 통계가 이 문제를 부분적으로 해결한다.

**옵티마이저 회귀가 의심된다.** 코드 변경이 없는데 특정 쿼리가 갑자기 느려졌다면 통계 갱신이나 패치 레벨 변경이 원인일 수 있다. 이런 패턴이 빈번해지면 현 버전이 한계에 왔다는 신호다.

**인증 플러그인 경고.** `mysql_native_password` 폐기 예고가 뜨거나, 클라이언트 드라이버가 지원하지 않는 인증 방식을 요구하면 업그레이드 타이밍을 검토해보자.

```sql
-- 현재 인증 플러그인 확인
SELECT user, host, plugin
FROM mysql.user
WHERE user NOT IN ('root', 'mysql.sys', 'mysql.infoschema', 'mysql.session')
ORDER BY user;
-- plugin: mysql_native_password가 있으면 8.4에서 기본 비활성화됨

-- 통계 현황
SELECT TABLE_SCHEMA, TABLE_NAME, LAST_ANALYZED
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'mydb'
ORDER BY LAST_ANALYZED ASC;
-- 오래된 테이블은 ANALYZE TABLE 재실행 고려
```

이 신호들이 쌓이면 14장의 업그레이드 체크리스트를 펼칠 때가 온 것이다.

---

## TLS와 인증 — 기본 중의 기본

**TLS 강제**

```sql
-- TLS 요구 사용자 설정
ALTER USER 'app_user'@'%' REQUIRE SSL;

-- 연결에 TLS가 사용되는지 확인
SHOW STATUS LIKE 'Ssl_cipher';
-- Ssl_cipher: TLS_AES_256_GCM_SHA384 (암호화됨)
-- Ssl_cipher: '' (암호화 안 됨)
```

애플리케이션이 DB에 연결할 때 TLS를 쓰지 않으면 네트워크에서 패킷을 볼 수 있다. AWS VPC 안이라도 TLS를 끄는 것은 찜찜하다.

**인증 플러그인**

8.0부터 기본 인증 플러그인은 `caching_sha2_password`다. MySQL Connector/J 8.0.17 이상, Python mysql-connector 8.0.17 이상은 이미 지원한다. 하지만 레거시 드라이버를 쓰는 시스템이라면 업그레이드 전에 한 번 확인해두는 편이 낫다.

**감사 로그**

누가 언제 어떤 SQL을 실행했는지 기록하는 것은 보안 요건이기도 하고 사고 분석에도 필요하다.

```sql
-- Percona Audit Plugin 설치 확인
SHOW VARIABLES LIKE 'audit_log_file';

-- 감사 대상 설정 (예: 특정 사용자)
SET GLOBAL audit_log_include_accounts = 'admin@%';
```

MySQL Enterprise Audit과 Percona Audit Plugin이 대표적이다. 어느 쪽이든 로그 파일 크기가 빠르게 커질 수 있으니 보존 정책을 함께 정의해두자.

### RLS — 뷰와 애플리케이션으로

MySQL은 PostgreSQL의 Row Level Security(RLS)처럼 DB 레벨에서 행 단위 접근 제어를 네이티브로 지원하지 않는다. 대신 두 가지 대안이 있다.

첫 번째는 뷰 + 스토어드 함수 패턴이다.

```sql
-- 현재 세션 사용자를 기반으로 필터링하는 뷰
CREATE VIEW orders_view AS
SELECT o.*
FROM orders o
WHERE o.tenant_id = (
    SELECT tenant_id FROM session_users
    WHERE session_user = CURRENT_USER()
);

-- 애플리케이션은 orders_view만 접근하도록 권한 제어
GRANT SELECT ON mydb.orders_view TO 'app_user'@'%';
REVOKE SELECT ON mydb.orders TO 'app_user'@'%';
```

두 번째는 애플리케이션 레이어에서 처리하는 방식이다. 멀티테넌시 SaaS에서 가장 흔히 쓰는 방법으로, 모든 쿼리에 `WHERE tenant_id = :currentTenantId` 조건을 자동으로 붙인다. Spring Data JPA에서는 `@Filter`나 Hibernate Multi-tenancy 기능으로 구현할 수 있다.

AWS는 Aurora/RDS for MySQL에 대한 RLS 패턴 블로그도 제공하니 SaaS 구조라면 참고해볼 만하다.

### 비밀번호 평문 노출 차단

```sql
-- general log에 쿼리가 기록될 때 평문 비밀번호가 노출되는 경우 방지
-- my.cnf에 추가
-- [mysqld]
-- log-raw=OFF  (기본값, 명시적으로 확인)

-- .my.cnf 평문 저장 대신 mysql_config_editor 사용
-- mysql_config_editor set --login-path=local --host=localhost \
--   --user=root --password
-- 이후 mysql --login-path=local 으로 접근
```

로그에 `SET PASSWORD` 같은 쿼리가 남으면 비밀번호가 그대로 찍힌다. `--log-raw=OFF`가 기본값이지만 명시적으로 확인해두는 편이 낫다. `.my.cnf`에 비밀번호를 평문으로 저장하는 관행도 `mysql_config_editor`로 대체하자.

---

## 마무리

데이터베이스가 보내는 신호를 듣는 것은 기술이기도 하지만 습관이기도 하다.

버퍼풀 히트율과 `Threads_running`을 매일 챙기자. 슬로우 쿼리 로그를 켜두고 주기적으로 `pt-query-digest`로 분석해보자. 복제 lag은 `Seconds_Behind_Source`보다 PS의 timestamp 비교가 더 정확하다.

백업은 복구 테스트를 해봐야 진짜 백업이다. 분기마다 PITR 리허설을 실행하고 RTO를 실제로 측정해두자. DR 설계는 RPO와 RTO를 서비스 팀과 명확히 합의하는 것에서 시작한다.

TLS를 강제하고, 감사 로그를 켜고, 비밀번호가 로그에 남지 않게 하는 것은 번거롭지 않다. 이 습관이 사고 이후의 후회를 막는다.

다음 장에서는 지금까지 배운 모든 도구를 한 시스템에서 짜맞춰보자. 가상의 결제 시스템 한 건을 도메인 모델링부터 운영 시나리오까지 끝까지 분해해보는 시간이다.

---

## 참고 자료

- LINE Engineering — performance-schema-instruments 영향: https://engineering.linecorp.com/en/blog/mysql-research-performance-schema-instruments
- 토스 SLASH 21 — MYSQL HA & DR Topology: https://toss.im/slash-21/sessions/2-3
- AWS — Implement row-level security in Amazon Aurora MySQL and Amazon RDS for MySQL: https://aws.amazon.com/blogs/database/implement-row-level-security-in-amazon-aurora-mysql-and-amazon-rds-for-mysql/
- MySQL Performance Schema Quick Start: https://dev.mysql.com/doc/refman/8.0/en/performance-schema-quick-start.html
- hackmysql — Monitoring replication lag with Performance Schema: https://hackmysql.com/monitoring-replication-lag-with-performance-schema/
- Percona Audit Plugin: https://www.percona.com/software/mysql-database/percona-server/audit-log-plugin
- velog — 성능 개선을 위한 프로파일링 1편: 슬로우 쿼리 로그: https://velog.io/@breadkingdom/MySQL-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%EC%9D%84-%EC%9C%84%ED%95%9C-%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%A7%81-1
