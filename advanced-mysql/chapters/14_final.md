# 14장. 업그레이드와 그다음 — 메이저 버전을 넘는 법

"8.0에서 8.4로 올려야 한다는 메일이 왔어요. 얼마나 걸릴까요?"

이 질문을 처음 받으면 솔직히 당황스럽다. "얼마나 걸릴지"보다 "무엇이 깨질지"를 먼저 물어야 하기 때문이다. 메이저 업그레이드는 단순한 버전 숫자 변경이 아니다. 동작이 바뀌고, 기본값이 달라지고, 한 번 올라가면 내려올 수 없다.

MySQL 메이저 업그레이드를 어떻게 준비하고 실행하는지, 그리고 이 책을 덮은 다음에 어디로 가야 하는지를 함께 살펴보자.

---

## 다운그레이드 불가의 무게

가장 먼저 이 사실을 마음에 새겨두자. **MySQL 8.0에서 8.4로 한 번 올리면 다시 내릴 수 없다.** 데이터 딕셔너리 포맷, redo 로그 구조, 일부 시스템 테이블 스키마가 변경되기 때문에 이전 버전 mysqld로 같은 데이터 파일을 열 수 없다.

이것이 업그레이드 전 철저한 준비가 필요한 핵심 이유다. "일단 올려보고 문제 있으면 내려야지"가 통하지 않는다.

5.7에서 8.0으로 올린 경험이 있다면 이 무게를 이미 알 것이다. 업그레이드 후 예상치 못한 쿼리 회귀를 발견하고 롤백하려 했지만 할 수 없었던 상황, 정말 난감하지 않았는가.

---

## 메이저 업그레이드 체크리스트

체크리스트는 순서가 있다. 건너뛰면 나중에 다시 처음부터 해야 하는 경우가 생긴다.

### 1단계: pt-upgrade로 쿼리 호환성 확인

`pt-upgrade`는 두 MySQL 인스턴스에 같은 쿼리를 실행해 결과와 실행 시간을 비교한다. 업그레이드 전 8.0 환경과 업그레이드 대상 8.4 환경에서 슬로우 쿼리 로그에 쌓인 실제 쿼리를 돌려보는 것이다.

```bash
# pt-upgrade: 두 인스턴스에서 실제 쿼리 비교
pt-upgrade \
  h=mysql-8.0.prod.internal,u=readonly,p=xxx \
  h=mysql-8.4.test.internal,u=readonly,p=xxx \
  /var/log/mysql/slow.log \
  --type slowlog \
  --max-class-size 5000

# 출력 예시:
# Query class: SELECT ... WHERE status = ? ORDER BY ...
#   Count: 245
#   Avg response time: 0.0023s vs 0.0089s (8.4에서 3.8배 느림!)
#   Differences: rows examined (45 vs 320)
```

결과에서 주의 깊게 봐야 할 것은 세 가지다. 결과가 달라졌는가(데이터 정합성 문제), 실행 시간이 크게 달라졌는가(옵티마이저 회귀), 에러가 발생했는가(문법/함수 호환성).

실전 예시 하나를 들자. 어느 팀이 pt-upgrade를 돌렸더니 보고서 쿼리 한 건이 8.4에서 3.8배 느려진다는 결과가 나왔다. 원인을 파보니 `IN (...)` 절의 cost 추정 휴리스틱이 바뀐 탓이었다. 8.0에서는 인덱스를 탔던 쿼리가 8.4에서는 풀스캔을 선택하고 있었다. 운영 전환 전에 발견해 인덱스 힌트를 명시하는 식으로 대응할 수 있었다 — 운영 후 발견했다면 사용자가 먼저 알았을 것이다.

### 2단계: 인증 플러그인 호환성 확인

MySQL 8.4 LTS에서 `mysql_native_password` 인증 플러그인은 기본적으로 비활성화된다. 이 플러그인을 쓰는 사용자 계정과 이를 지원하는 드라이버가 있다면 업그레이드 전에 정리해두는 편이 낫다.

```sql
-- 현재 mysql_native_password를 쓰는 계정 확인
SELECT user, host, plugin
FROM mysql.user
WHERE plugin = 'mysql_native_password'
  AND user NOT IN ('root');

-- 계정별로 인증 플러그인 변경
ALTER USER 'app_user'@'%'
    IDENTIFIED WITH caching_sha2_password BY 'new_password';

-- JDBC 드라이버 버전 확인 (8.0.17 이상이면 caching_sha2_password 지원)
-- MySQL Connector/J 8.0.17+
-- Python mysql-connector-python 8.0.17+
```

애플리케이션에서 쓰는 JDBC 드라이버 버전을 먼저 확인하자. 드라이버가 `caching_sha2_password`를 지원하지 않는다면 업그레이드 전에 드라이버를 먼저 올리는 편이 낫다.

실전 팁 하나. 애플리케이션이 여러 마이크로서비스로 쪼개져 있다면 각 서비스가 어떤 드라이버 버전을 쓰는지 한눈에 보기 어렵다. CI 파이프라인의 의존성 그래프에서 `mysql-connector-java` 버전을 한 번에 추출해두면 누락 없이 점검할 수 있다.

### 3단계: 8.4 default 변경 영향 측정

Skeema 블로그가 정리한 "8.4의 다섯 가지 놀라움" 중 운영에 영향이 큰 것들이다.

**Adaptive Hash Index(AHI) 기본 OFF**. 8.0까지는 기본 ON이었다. 쓰기 부하가 높은 환경에서 AHI가 락 경합을 늘렸기 때문이다. 단일 키 lookup 성능에 의존하던 워크로드라면 8.4 업그레이드 후 속도 저하를 경험할 수 있다.

```sql
-- AHI 현황 확인 (8.0 환경)
SHOW ENGINE INNODB STATUS\G
-- INSERT BUFFER AND ADAPTIVE HASH INDEX 섹션에서 hash index hits 비율 확인

SHOW VARIABLES LIKE 'innodb_adaptive_hash_index';
-- ON이면 AHI를 쓰고 있다는 뜻

-- 8.4 업그레이드 후 AHI를 다시 켜고 싶다면
SET GLOBAL innodb_adaptive_hash_index = ON;
```

**Change Buffer 기본 OFF**. 세컨더리 인덱스 업데이트를 지연 처리해 IO를 줄이는 기능이다. 쓰기 위주 워크로드에서 효과적이었지만 8.4에서 기본 OFF가 됐다. 쓰기 부하가 높고 Change Buffer에 의존하던 워크로드라면 성능 변화를 확인해두자.

**FK 부모 키 엄격성 강화**. 8.4에서 FK의 부모 테이블은 정확히 일치하는 고유 키가 있어야 한다. 8.0에서는 접두사(prefix)가 일치하는 키도 허용했는데 이제 그렇지 않다. 스키마에 이런 패턴이 있다면 업그레이드 전에 한 번 점검해보자.

```sql
-- FK 관계에서 부모의 인덱스 확인
SELECT
    kcu.TABLE_NAME,
    kcu.COLUMN_NAME,
    kcu.REFERENCED_TABLE_NAME,
    kcu.REFERENCED_COLUMN_NAME,
    rc.CONSTRAINT_NAME
FROM information_schema.KEY_COLUMN_USAGE kcu
JOIN information_schema.REFERENTIAL_CONSTRAINTS rc
    ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
WHERE kcu.TABLE_SCHEMA = 'mydb'
ORDER BY kcu.TABLE_NAME;
```

실전 예시. 8.0 시절에 누군가 `parent` 테이블에 `(a, b)` UNIQUE 인덱스만 만들어두고, 자식 테이블에서 `FOREIGN KEY (a) REFERENCES parent(a)`로 단일 컬럼 FK를 걸어둔 적이 있다. 8.0에서는 `(a, b)`의 접두사 `a`로 동작했지만, 8.4 업그레이드 시점에 이 FK가 "유효한 부모 키 없음" 오류로 거부된다. 사전에 발견해 `parent.a`에 단일 UNIQUE를 추가하면 깔끔하게 해결된다.

### 4단계: Blue/Green 배포 또는 리플리카 승격 패턴

업그레이드 자체는 두 가지 전략이 있다.

**AWS Blue/Green Deployment**는 Blue(현재 운영)와 Green(업그레이드된) 환경을 별도로 만들고, 검증 후 트래픽을 전환하는 방식이다.

```bash
# AWS RDS Blue/Green 배포 생성
aws rds create-blue-green-deployment \
  --blue-green-deployment-name "mysql-84-upgrade" \
  --source mydb-prod \
  --target-engine-version "8.4.0"

# 상태 확인
aws rds describe-blue-green-deployments \
  --blue-green-deployment-identifier <id>

# Green 환경 검증 후 전환
aws rds switchover-blue-green-deployment \
  --blue-green-deployment-identifier <id>
```

Blue/Green의 장점은 언제든 Blue로 돌아갈 수 있다는 것이다. 단, 전환 시점에 몇 초의 연결 재수립이 필요하다. 결제처럼 한 트랜잭션도 끊기면 안 되는 도메인이라면 이 몇 초의 무게를 사전에 가늠해두자 — 애플리케이션 레이어에 재시도 + 멱등 처리가 마련돼 있어야 한다.

**리플리카 승격 패턴**은 업그레이드된 8.4 리플리카를 먼저 만들고, 검증 후 이것을 새 Writer로 승격하는 방식이다.

```
업그레이드 전:
  [8.0 Writer] → [8.0 Replica 1] → [8.0 Replica 2]

단계 1: 8.4 리플리카 추가
  [8.0 Writer] → [8.0 Replica 1] → [8.4 Replica]

단계 2: 8.4 리플리카에서 검증 (읽기 쿼리, pt-upgrade)

단계 3: 8.4 리플리카를 Writer로 승격
  [8.4 Writer] → [8.0 Replica 1] (일정 기간 유지)

단계 4: 8.0 리플리카 교체
  [8.4 Writer] → [8.4 Replica 1] → [8.4 Replica 2]
```

### 5단계: 5.7 리플리카 escape hatch

만약 5.7에서 8.4로 바로 올린다면(권장하지 않지만), 또는 8.0에서 8.4로 올린 뒤 문제가 생겼을 때 롤백할 방법이 없다. 그래서 8.0 리플리카를 일정 기간 유지하는 "escape hatch" 패턴을 쓴다.

8.4로 올린 후 2~4주간 8.0 리플리카를 살려둔다. 8.4에서 8.0으로 복제는 되지 않으므로, 전환 시점의 binlog를 보관해두고 만약 문제가 생기면 8.0 인스턴스를 다시 Writer로 쓰는 방식이다. 물론 이 과정에서 데이터 손실이 일어날 수 있다. 그래서 사전 검증을 더 단단히 해두는 편이 낫다.

실전 팁. escape hatch 기간 동안 8.0 리플리카는 읽기 트래픽을 받지 않더라도 binlog가 정상적으로 흘러가는지 확인해야 한다. `SHOW REPLICA STATUS`로 `Seconds_Behind_Source`가 0에 가깝게 유지되는지, `Last_IO_Error`가 비어 있는지를 일 1회 체크하는 정도면 충분하다.

### 6단계: MRTE 카카오식 트래픽 미러링

카카오의 MRTE를 활용할 수 있다면, 운영 트래픽을 8.4 환경에 미러링해 실제 동작을 사전에 보는 것이 가장 확실한 검증이다. MySQL Realtime Traffic Emulator는 binlog를 파싱해 실제 쿼리를 다른 환경에서 재실행한다.

전용 도구 없이도 프록시 레이어에서 읽기 트래픽의 일부를 8.4 스테이징 환경으로 복제해 비교하는 방식으로 부분적으로 구현할 수 있다. ProxySQL의 `mirror_hostgroup` 기능을 쓰면 한 쿼리를 두 호스트그룹에 동시에 보낼 수 있다. 응답 자체는 운영 쪽에서만 받고, 미러 쪽은 실행 시간과 에러를 로깅하는 식이다.

---

## 책 이후의 길 — 다음에 무엇을 볼까

이 책은 OLTP 워크로드를 다루는 스프링 개발자를 위한 MySQL 8.x 기반서다. 의도적으로 다루지 않은 영역들이 있다. 그 지도를 마지막으로 그려보자.

### 다음 단계 도구들

**Vitess/ProxySQL/MaxScale** — 샤딩 미들웨어. 단일 MySQL 인스턴스의 한계를 넘어 여러 인스턴스에 데이터를 분산시킬 때 필요한 레이어다. Vitess는 YouTube에서 시작해 CNCF 프로젝트가 됐고, 한국에서도 대규모 트래픽 서비스에서 검토되기 시작했다.

**Spring Batch** 심화 — 이 책의 10장에서 배치 INSERT 패턴을 다뤘지만, Spring Batch의 `JpaItemWriter`/`JdbcBatchItemWriter` 비교, Chunk Processing과 트랜잭션 경계 세밀한 설계, Partitioned Step으로 병렬 배치 처리하는 방법은 별도 공부가 필요하다.

**jOOQ** — JPA보다 SQL에 더 가까운 타입 세이프 SQL 빌더. QueryDSL과 비교할 때 DB 스키마에서 자바 코드를 생성하는 방식이 다르다. SQL 자유도가 중요한 팀에서는 jOOQ가 매력적인 선택이 될 수 있다.

**MySQL HeatWave** — MySQL과 OLAP/벡터 검색을 통합한 AWS 서비스. OLTP와 분석 워크로드를 같은 MySQL 인스턴스에서 처리하고 싶다면 HeatWave가 답일 수 있다. 단, 이 책의 범위(순수 OLTP) 밖이다.

**MySQL 9.x** — 이 책이 쓰인 시점에는 8.4 LTS가 기준이었다. 9.x는 JavaScript stored procedure, 벡터 함수 등 새로운 기능들이 추가됐지만 아직 LTS가 아니다. 사례가 충분히 쌓이고 LTS가 나오면 업그레이드를 검토해볼 만하다.

### 학술 논문으로의 길

더 깊이 가고 싶다면 트랜잭션·동시성 제어의 기반 논문들이 기다리고 있다.

Cahill (2009) "Serializable Isolation for Snapshot Databases" (종장의 참고문헌 안내 참조) — MySQL의 RR이 왜 진정한 직렬성이 아닌지, Snapshot Isolation이 어떻게 구현되는지를 수학적으로 다룬다. Jepsen 분석이 MySQL 8.0.34에서 발견한 이상 현상들을 이 논문을 읽으면 더 깊이 이해할 수 있다.

---

## 마무리

메이저 업그레이드는 한 번 가면 돌아올 수 없는 길이다. 그래서 체크리스트가 중요하다.

pt-upgrade로 쿼리 호환성을 먼저 확인하고, 인증 플러그인을 정비하고, 8.4 default 변경의 영향을 측정하자. Blue/Green 배포나 리플리카 승격 패턴으로 전환하고, 일정 기간 8.0 인스턴스를 escape hatch로 유지하는 편이 낫다. 카카오 MRTE식 트래픽 미러링으로 사전 검증을 더할 수 있다면 더 좋다.

다운그레이드 불가의 무게를 알면 사전 준비에 투자하는 이유가 명확해진다. 이 체크리스트가 다음 분기 업그레이드 일정을 받았을 때 당황하지 않고 대응할 수 있는 기반이 되길 바란다.

이제 종장이다. 책 전체를 되돌아보고, 다음 주 월요일부터 시도해볼 실험 세 가지를 챙겨가자.

---

## 참고 자료

- Skeema — Five Surprises in MySQL 8.4 LTS: https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- Percona — Upgrade MySQL to 8.0: Avoid Disaster: https://www.percona.com/blog/upgrade-mysql-to-8-0-yes-but-avoid-disaster/
- Severalnines — Tips for upgrading to MySQL 8: https://severalnines.com/blog/tips-for-upgrading-mysql-5-7-to-mysql-8/
- AWS — Major version upgrades for RDS for MySQL: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.Major.html
- AWS — Aurora MySQL major version upgrade: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.MajorVersionUpgrade.html
- 카카오 — MRTE (MySQL Realtime Traffic Emulator): https://tech.kakao.com/posts/311
