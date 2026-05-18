# 22장. 보안과 감사 — pgaudit·RLS·SSL/TLS·CVE 추적

보안은 사고가 나기 전에는 아무도 안 본다는 말이 있다. 운영팀의 책장에서 가장 먼지가 두꺼운 책이 보안 가이드라는 우스개도 같은 맥락이다. 그런데 PostgreSQL을 메인 DB로 쓴다면, 사고가 나기 전에 한 번은 펼쳐 봐야 할 챕터가 있다. 이번이 그 챕터다.

DBA의 자정 호출 중에서 가장 끔찍한 건 백업 실패도, autovacuum 폭주도 아니다. 무언가 빠져나갔다는 통지를 받는 일이다. 그날 밤 가장 먼저 손이 가는 곳이 어딘지 생각해보자. `pg_hba.conf`다. 그 다음이 audit 로그고, 그 다음이 권한 표다. 사고가 나야 손이 가는 그 세 곳을, 사고가 나기 전에 같이 살펴보자.

이번 장은 두 명의 독자를 같이 모신다. 한 명은 야간에 페이지를 받는 DBA고, 다른 한 명은 컴플라이언스 회의에 들어가는 Tech Lead다. 둘 다 의사결정의 근거가 필요하다. "왜 이렇게 설정했는가"에 답하기 위해서다. 8개의 소절은 그 답을 하나씩 채워간다 — 인증과 암호부터 시작해서 전송 보안, 권한, RLS, 감사, CVE 대응, 마스킹, 그리고 마지막에 한 페이지 체크리스트로 닫는다.

한 가지 약속을 먼저 해두자. 이 장은 보안 정책을 강요하지 않는다. 강요할 자격도 없다. 다만 "왜 그렇게 해야 하는지"의 이유를 손에 쥐어주려 한다. 결정은 독자가 한다.

## 22.1 인증과 암호 — scram-sha-256, md5의 퇴장, 그리고 pg_hba.conf

새 PostgreSQL 클러스터를 띄웠다고 해보자. 가장 먼저 만지게 되는 파일이 무엇일까. 십중팔구 `postgresql.conf`고, 그 다음이 `pg_hba.conf`다. 그런데 이 둘 중 사고의 시작점이 어디에 있는지 묻는다면 답은 망설임 없이 `pg_hba.conf`다. "어디서 누가 어떻게 들어올 수 있는가"의 규칙이 모두 그 한 파일에 적혀 있기 때문이다.

### md5는 왜 진작 떠나야 했을까

PostgreSQL은 오랫동안 `md5` 방식의 암호 인증을 기본으로 써왔다. 익숙한 분들은 한숨이 나올 만한 사실 하나를 짚고 가자. md5는 더 이상 안전한 해시가 아니다. 같은 해시를 만드는 입력값을 만들어내기가 너무 쉬워졌다. 그래서 PostgreSQL 진영은 진작부터 `scram-sha-256`으로 옮겨가자고 권해왔고, 버전 18에 이르러서는 md5의 제거가 임박했다는 신호까지 나왔다.

scram-sha-256은 무엇이 다를까. 차이의 핵심은 두 가지다.

첫째, 챌린지-응답 프로토콜이다. 클라이언트가 서버에 진짜 비밀번호를 보내지 않는다. 서버가 던진 난수에 비밀번호로 응답을 만들어 보내고, 서버는 자기가 가진 검증값으로만 확인한다. 그래서 네트워크를 엿보는 공격자가 인증 트래픽을 캡처해봐야 재사용할 수 없다.

둘째, PBKDF2 키 도출이다. 비밀번호에 솔트를 붙이고 수천 번 해시를 반복한다. 저장된 검증값이 유출돼도 원본 비밀번호를 역산하기가 사실상 불가능에 가깝다. md5와는 차원이 다른 안전성이다.

설정은 어렵지 않다. `postgresql.conf`에 한 줄을 바꿔두자.

```conf
password_encryption = scram-sha-256
```

그리고 `pg_hba.conf`의 모든 `md5` 라인을 `scram-sha-256`으로 바꾼다. 끝일까? 아쉽게도 그렇지 않다. 이미 저장된 비밀번호 해시는 md5 형식 그대로 남아 있다. 사용자가 `ALTER USER ... PASSWORD ...`로 다시 설정해야 새 해시가 만들어진다. 즉, scram-sha-256으로 옮기는 일은 한 줄 수정이 아니라 "모든 계정의 비밀번호를 다시 받는" 운영 이벤트다.

### 운영의 현실 — 의존성의 사슬

이 대목에서 "그냥 다 바꾸면 되지" 하고 손을 흔드는 사람을 만난 적이 있다. 실제로 그래본 사람은 안다. 운영 환경에는 수십 개의 의존성이 매달려 있다. 모니터링 도구, 백업 스크립트, 분석 워크로드의 ETL 잡, 그리고 무엇보다 connection pooler가 있다.

PgBouncer는 1.21.0 버전(2023년 말 출시)에 이르러서야 SCRAM을 제대로 지원하기 시작했다. 그 이전 버전을 쓰는 팀은 풀러부터 올려야 한다. 그 다음은 클라이언트 라이브러리다. JDBC, libpq, psycopg, pg, asyncpg — 모두 최근 버전이면 SCRAM을 지원하지만, 회사 안에 박혀 있는 5년 묵은 서비스가 어떤 클라이언트를 쓰는지 한 번 점검할 필요가 있다. 그래서 scram-sha-256 이관은 "한 번에 가지 말자"가 정답에 가깝다. md5와 scram-sha-256은 한동안 공존할 수 있고, `pg_hba.conf`에서 라인별로 인증 방식을 다르게 줄 수 있다. 새 시스템부터, 그리고 트래픽이 작은 서비스부터 옮기는 단계적 전환이 권장된다.

### pg_hba.conf 설계 — host, hostssl, hostnossl

`pg_hba.conf`의 각 라인은 다음 7개 필드로 이뤄진다. 이걸 한 번 외워두는 편이 낫다.

```
# TYPE  DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
hostssl all       app   10.0.0.0/8   scram-sha-256
```

여기서 TYPE이 보안의 첫 번째 관문이다. 셋 중 무엇을 쓰느냐가 그날 새벽의 운명을 가른다.

- `host` — SSL이 켜져 있든 꺼져 있든 매칭된다. 가장 너그러운 옵션이고, 가장 위험한 옵션이기도 하다.
- `hostssl` — SSL/TLS로 연결한 클라이언트만 매칭된다.
- `hostnossl` — SSL 없이 연결한 클라이언트만 매칭된다.

상상해보자. 운영 클러스터에 `host all all 0.0.0.0/0 scram-sha-256` 같은 라인이 한 줄 들어가 있다고. 인증은 강해 보이지만, 통신은 평문이 될 수 있다. scram-sha-256으로 비밀번호는 보호되지만, 그 뒤에 흐르는 쿼리와 결과는 모두 노출된다. 그래서 운영에서는 `host`가 아니라 `hostssl`을 기본으로 쓰는 것이 바람직하다. 평문 연결을 명시적으로 막고 싶다면 `hostnossl ... reject`를 한 줄 더 넣어 차단을 선언해두자.

또 한 가지 — `0.0.0.0/0` 같은 와일드카드는 사실상 "누구나"라는 뜻이다. 사내망이든 VPC든, 가능한 한 좁은 CIDR로 줄이는 편이 낫다. 매니지드 PG의 보안 그룹과 PG 자체의 `pg_hba.conf`는 별개의 방어선이다. 둘을 다 좁히는 것이 정공법이다.

### 비밀번호 정책

PostgreSQL은 비밀번호 만료, 복잡도, 재사용 금지 같은 정책을 코어에 포함하지 않는다. 의외로 빠진 부분이다. 그래서 보통은 `passwordcheck` 같은 익스텐션을 붙이거나, 매니지드 PG의 계정 정책에 위임한다. 자체 운영이라면 `passwordcheck`의 한국어 환경 호환성을 한 번 확인하고 도입하는 편이 낫다.

비밀번호 만료는 `ALTER USER ... VALID UNTIL` 절로 한 명씩 줄 수 있다. 1년에 한 번 회전하는 정책이라면 이 절을 자동으로 갱신하는 잡 하나면 충분하다. 다만 만료된 계정으로 운영 중인 잡이 있다면 사고가 난다. 만료 직전에 알림을 띄우는 모니터링 한 줄이 같이 필요하다.

기억해두자. `pg_hba.conf`는 "방어의 형식"이고, scram-sha-256은 "방어의 강도"다. 둘을 같이 챙겨야 첫 번째 관문이 닫힌다.

## 22.2 전송 보안 — SSL/TLS, 그리고 verify-full의 진짜 의미

암호 인증이 안전해졌다고 통신까지 안전해진 건 아니다. scram-sha-256은 비밀번호 자체를 지키지만, 그 뒤로 흐르는 SQL과 결과는 별개의 문제다. 그래서 두 번째 관문이 전송 보안이다.

상상해보자. 카페에서 노트북을 열고 운영 DB에 붙는다고. 그 사이의 모든 패킷이 누군가의 와이어샤크에 그대로 잡힌다고 생각하면, 등골이 서늘하다. VPN을 거치면 어느 정도 보호받지만, VPN의 끝에서 PG까지의 구간은 또 다른 이야기다. SSL/TLS는 그 마지막 구간까지 암호화해주는 표준 도구다.

### SSL을 켜는 것만으로는 부족하다

PG에서 SSL을 켜는 일 자체는 어렵지 않다. `postgresql.conf`에 다음 세 줄이면 시작된다.

```conf
ssl = on
ssl_cert_file = '/etc/postgresql/server.crt'
ssl_key_file = '/etc/postgresql/server.key'
```

그런데 여기서 멈추면 "통신은 암호화되는데 상대를 못 알아보는" 상태가 된다. 무슨 말일까. SSL/TLS의 핵심은 두 가지다. 하나는 암호화고, 다른 하나는 인증서로 상대를 확인하는 일이다. 둘 중 하나만 챙기면 중간자(MITM) 공격에 취약해진다.

여기서 등장하는 게 클라이언트의 `sslmode` 옵션이다. libpq 기준으로 여섯 단계가 있다.

| sslmode | 암호화 | 인증서 검증 | 호스트명 검증 |
|---------|--------|-------------|---------------|
| `disable` | X | X | X |
| `allow` | 서버가 요구하면 | X | X |
| `prefer` | 가능하면 | X | X |
| `require` | O | X | X |
| `verify-ca` | O | O | X |
| `verify-full` | O | O | O |

`require`까지만 쓰는 시스템을 종종 본다. 통신은 분명히 암호화된다. 그런데 누구와 연결됐는지는 확인하지 않는다. 누군가 DNS를 가로채 가짜 서버를 띄우면 그 서버에 무방비로 비밀번호를 넘긴다. SCRAM이 비밀번호 자체는 지킨다고 했지만, 가짜 서버는 인증 자체를 가로채 그 뒤를 자기 마음대로 풀 수 있다. 찜찜한 일이다.

그래서 운영 환경의 클라이언트 설정은 `sslmode=verify-full`이 권장된다. verify-full은 두 가지를 보장한다.

1. 서버 인증서가 신뢰할 수 있는 CA에서 발행됐는지 확인한다(`verify-ca`까지의 보장).
2. 서버 인증서의 CN(Common Name)이 접속하려는 호스트명과 일치하는지 확인한다.

이 두 번째 검증이 핵심이다. 서버를 가장한 공격자는 신뢰할 수 있는 CA의 인증서를 가질 수 없고, 가졌더라도 자기 호스트명으로는 우리 운영 PG를 가장할 수 없다.

### 매니지드 PG의 root CA — 다운로드를 잊지 말자

자체 운영이라면 인증서는 자기가 관리한다. 만료 일정을 캘린더에 박아두고, 자동 갱신 스크립트를 걸어두면 된다. 그런데 매니지드 PG는 다르다. AWS RDS, Aurora, GCP Cloud SQL, Azure Database for PostgreSQL — 각 벤더가 자기 root CA로 서명한 인증서를 PG 클러스터에 박아둔다. 클라이언트는 그 root CA를 신뢰해야 verify-full이 성립한다.

여기서 한 가지 자주 잊히는 일이 있다. root CA는 영원하지 않다. AWS는 RDS 인증서를 주기적으로 회전한다. 2024년에 한 차례 갱신이 있었고, 그 다음 큰 회전이 2029~2030년에 예정돼 있다. 회전일이 다가오면 모든 클라이언트가 새 root CA를 받아두지 않으면 인증서 검증이 깨진다. 클라이언트 라이브러리 종속성에 root CA를 박아둔 시스템이라면 그날 새벽이 정신없다.

운영 안전망으로 두 가지를 권한다.

- root CA 파일은 클라이언트 측에 명시적으로 두자. 시스템 신뢰 저장소에 넣는 대신 `sslrootcert=/path/to/rds-ca.pem`처럼 직접 지정하는 편이 추적이 쉽다.
- 인증서 회전 일정을 모니터링에 박아두자. "60일 후 만료" 알림을 띄우는 한 줄이면 충분하다.

### 클라이언트 인증서까지 가야 할 때

흔하지는 않지만, 비밀번호 인증을 아예 빼고 클라이언트 인증서로 인증하는 시스템도 있다. 결제·의료·정부 시스템처럼 강한 보장이 필요한 경우다. `pg_hba.conf`에 `clientcert=verify-full`을 명시하면, 서버가 클라이언트 인증서의 CN과 PG role을 매칭한다.

```
hostssl all all 10.0.0.0/8 cert clientcert=verify-full
```

비밀번호 자체가 없으니 유출 위험도 없다. 다만 운영 비용이 크다. 모든 클라이언트에 개별 인증서를 배포하고 회전해야 한다. 자체 PKI를 운영할 여력이 있는 조직에만 권한다.

기억해두자. SSL을 켜는 것과 SSL을 제대로 쓰는 것은 다른 일이다. `sslmode=verify-full`까지 가야 두 번째 관문이 진짜로 닫힌다.

## 22.3 권한 모델 — role, GRANT, 그리고 계정 분리의 정공법

세 번째 관문은 "들어온 다음에 무엇을 할 수 있는가"의 문제다. PostgreSQL의 권한 모델은 role 한 가지로 통일돼 있다. user도 role이고, group도 role이다. 둘을 구분하지 않고 속성으로만 다룬다. 이 단순함이 PG 권한 모델의 강점이다.

### role의 계층 — INHERIT의 우아함

role끼리 상속이 된다. `GRANT role_a TO role_b` 한 줄이면 b가 a의 권한을 물려받는다. 이걸 잘 쓰면 권한 관리가 깔끔해진다.

예를 들어 멀티테넌트 SaaS에서 다음 계층을 만든다고 해보자.

```sql
-- 권한 그룹(로그인 불가)
CREATE ROLE app_read NOLOGIN;
CREATE ROLE app_write NOLOGIN;
CREATE ROLE app_admin NOLOGIN;

-- 권한 부여
GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_read;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_write;
GRANT app_read TO app_write;
GRANT app_write, CREATE ON SCHEMA app TO app_admin;

-- 실제 로그인 계정
CREATE ROLE svc_api LOGIN PASSWORD '...';
GRANT app_write TO svc_api;

CREATE ROLE svc_analytics LOGIN PASSWORD '...';
GRANT app_read TO svc_analytics;
```

계정마다 직접 GRANT하지 않고 그룹 role을 거쳐 권한이 흐른다. 새 테이블이 추가되면? 그룹 role에 한 번 GRANT하면 모든 하위 계정에 전파된다. 새 계정이 들어오면? 그룹 role 하나만 GRANT하면 된다. 관리 비용이 한 자리 수 줄어든다.

### default privileges — 잊기 쉬운 한 줄

위 예제에는 함정이 하나 숨어 있다. `GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_read`는 "지금 있는" 테이블에만 적용된다. 내일 만들 테이블에는 자동으로 적용되지 않는다. 마이그레이션을 돌리고 "왜 새 테이블에 권한이 없지?"라고 한참 헤매본 사람이 적지 않을 것이다. 난감한 일이다.

해결책은 `ALTER DEFAULT PRIVILEGES`다.

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA app
  GRANT SELECT ON TABLES TO app_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA app
  GRANT INSERT, UPDATE, DELETE ON TABLES TO app_write;
```

이 한 줄을 박아두면 앞으로 그 스키마에 만들어지는 모든 테이블에 자동으로 권한이 따라붙는다. 신규 클러스터의 D+0 체크리스트에 빠지지 않게 적어두자.

### 계정 분리 — 읽기·쓰기·관리의 삼분

운영에서 가장 자주 보는 함정 하나. 모든 애플리케이션이 superuser 계정으로 붙는 시스템이다. 개발 편의를 위해 그렇게 시작했다가, 운영까지 그대로 가버린 케이스다. 그런데 superuser는 RLS를 우회하고, audit 로그를 우회하고, `pg_hba.conf`의 일부 검증도 우회한다. 사고가 났을 때 "누가 무엇을 했는가"의 추적이 거의 불가능해진다. 끔찍한 일이다.

대안은 단순하다. 애플리케이션마다 권한이 다른 계정을 분리한다.

- **읽기 전용 계정** — 분석, 대시보드, 백업 검증, BI 도구
- **쓰기 계정** — 본 애플리케이션, 백오피스
- **DDL/관리 계정** — 마이그레이션, 운영 스크립트
- **백업/복제 계정** — `REPLICATION` 속성만 가진 전용 계정

각 계정의 비밀번호는 vault에서 동적으로 발급하는 편이 낫다. HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager 등이 PG의 동적 자격 증명 발급을 지원한다. 비밀번호가 평생 한 번 정해지는 것이 아니라 24시간마다 회전한다고 생각해보자. 유출의 위협이 시간 단위로 줄어든다.

### 스키마 격리 — 잊지 말 public

PostgreSQL에는 모든 사용자가 기본으로 접근 가능한 `public` 스키마가 있다. 버전 15 이전에는 `public`에 CREATE 권한도 디폴트로 주어졌다. 그래서 누구나 `public`에 테이블을 만들 수 있었고, 그 테이블에 다른 사용자가 마음대로 데이터를 넣을 수도 있었다. 보안 관점에서는 위험한 디폴트였다.

PG 15부터 `public`의 CREATE 권한이 기본으로 빠졌다. 다행이다. 그래도 자체 운영이라면 한 번 더 확인하는 편이 낫다.

```sql
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO authenticated;
```

그리고 애플리케이션 데이터는 `public`이 아닌 자기 스키마에 두자. `app`, `tenant_x`, `analytics` 같은 이름으로 격리하면, 권한 부여도 깔끔해지고 마이그레이션도 안전해진다.

## 22.4 RLS 운영 보안 — 16장이 끝난 자리에서 다시 시작하기

16장에서 RLS의 멀티테넌트 패턴을 봤다. `tenant_id`를 모든 테이블에 두고, 세션 변수로 현재 테넌트를 박고, USING 절로 정책을 거는 그 패턴이다. 16장이 "어떻게 설계하는가"였다면, 이번 절은 "운영에서 무엇이 깨지는가"다. 같은 RLS이지만 보는 각도가 다르다.

### 함정 하나 — RLS는 owner를 막지 못한다

RLS의 가장 큰 함정이 여기다. `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`를 켜고, 정책을 잘 만들어두고, 다 됐다고 안심한다. 그런데 그 테이블의 owner는 여전히 모든 행을 볼 수 있다. 정책을 무시한다. 왜? PG는 owner가 자기 테이블에 RLS의 제약을 받는 게 부자연스럽다고 봤기 때문이다. 그게 디폴트다.

상상해보자. 마이그레이션 계정이 모든 테이블의 owner라고. 그 계정이 운영 트래픽에 잘못 쓰이면 어떻게 될까. 모든 테넌트의 데이터가 한 계정으로 흘러나간다. 끔찍한 일이다.

해법은 `FORCE ROW LEVEL SECURITY`다.

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

두 번째 줄을 빠뜨리지 말자. 이걸 켜면 owner도 정책을 따른다. owner가 RLS를 우회하고 싶다면, 명시적으로 `BYPASSRLS` 속성을 가진 별도 role로 전환해야 한다. 그래서 "정책을 우회하는 행위"가 명시적인 권한 이동으로 가시화된다. 감사 가능성이 높아진다.

### BYPASSRLS — 명시적 우회의 자리

운영하다 보면 RLS를 우회해야 할 때가 있다. 데이터 마이그레이션, 전체 통계 집계, 사고 복구 같은 상황이다. 그럴 때 superuser로 들어가지 말자. 추적이 안 된다. 대신 `BYPASSRLS` 속성을 가진 전용 role을 만들어둔다.

```sql
CREATE ROLE rls_admin BYPASSRLS NOLOGIN;
GRANT rls_admin TO mig_user;
```

`mig_user`는 평소엔 일반 권한으로 일하다가, 필요할 때만 `SET ROLE rls_admin`으로 전환한다. 그리고 그 전환을 audit 로그에 남긴다. "왜 RLS를 우회했는가"의 흔적이 남는다. 사고 후 조사가 가능해진다.

### EXPLAIN에 정책이 보이는지 확인하기

RLS의 두 번째 운영 함정은 성능이다. RLS 정책은 SQL 술어로 들어간다. PG가 쿼리를 풀 때 자동으로 그 술어를 WHERE 절에 추가한다. 좋은 일이지만, 술어가 인덱스를 못 타면 끔찍해진다.

EXPLAIN을 떠보는 습관을 들이자.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE order_id = $1;
```

출력에 다음 같은 라인이 보여야 한다.

```
Filter: ((tenant_id = current_setting('app.current_tenant'::text)::uuid)
         AND (order_id = $1))
Index Cond: (order_id = $1)
```

`Filter`에 정책 술어가 들어가 있다. 그런데 `Index Cond`에는 `order_id`만 있고 `tenant_id`가 없다. 인덱스가 `(order_id)`로만 만들어졌다면, 다른 테넌트의 행까지 일단 읽어들인 다음 필터로 거른다. 행이 많지 않다면 괜찮지만, 다른 테넌트의 행이 수백만 건이라면 단순 조회 한 번에 수백만 행을 스캔한다.

처방은 인덱스를 `(tenant_id, order_id)` 같은 복합 인덱스로 만드는 것이다. 그러면 PG가 정책 술어를 인덱스 조건으로 끌어올린다.

```
Index Cond: ((tenant_id = current_setting('app.current_tenant'::text)::uuid)
             AND (order_id = $1))
```

EXPLAIN에 정책 술어가 `Index Cond`로 올라왔는지 확인하는 일이 RLS 운영의 일상이다. 잊지 말자.

### admin bypass의 감사 — 정책을 우회한 자국 남기기

마지막 운영 관심사는 감사다. RLS는 데이터 접근을 막지만, audit 로그를 막지는 않는다. 오히려 RLS가 잘 작동하는지 검증하기 위해서라도 audit이 같이 가야 한다.

audit 트리거를 다음 패턴으로 만들어둘 수 있다.

```sql
CREATE TABLE audit.access_log (
  ts TIMESTAMPTZ DEFAULT now(),
  user_name TEXT DEFAULT current_user,
  tenant_id UUID DEFAULT current_setting('app.current_tenant', true)::uuid,
  table_name TEXT,
  op TEXT,
  row_id UUID,
  bypass_rls BOOLEAN DEFAULT
    (SELECT rolbypassrls FROM pg_roles WHERE rolname = current_user)
);
```

`bypass_rls` 컬럼이 핵심이다. 누가, 언제, 어떤 테이블의 어떤 행을, 그리고 RLS를 우회한 권한으로 접근했는지를 기록한다. 사고 후에 "정책이 우회된 자국"을 찾을 수 있는 곳이 여기다.

기억해두자. RLS는 정책을 만들었다고 끝나지 않는다. `FORCE`로 owner까지 묶고, `BYPASSRLS`로 우회 통로를 가시화하고, EXPLAIN으로 인덱스 효율을 확인하고, audit으로 모든 흔적을 남긴다. 네 가지를 다 채워야 RLS가 운영급으로 작동한다.

## 22.5 감사 — pgaudit, 로그의 무게, SIEM의 시작점

PostgreSQL은 기본 로그에 쿼리를 남길 수 있다. `log_statement = 'all'`을 켜면 모든 쿼리가 로그 파일에 떨어진다. 그런데 이걸로 충분한가? 운영 한 달만 돌려보면 안다. 충분하지 않다.

이유는 두 가지다. 첫째, 기본 로그는 누가 그 쿼리를 실행했는지의 맥락이 약하다. 어떤 role로, 어떤 세션 변수로, 어떤 RLS 정책 아래에서 실행했는지를 따로 따라가야 한다. 둘째, 출력이 너무 많다. `log_statement = 'all'`을 켜둔 운영 클러스터의 로그는 정말 끔찍하다. 디스크가 며칠 만에 차고, 정작 의미 있는 라인을 찾기 어렵다.

그래서 등장한 것이 `pgaudit`다. 감사 목적에 특화된 로그를 따로 뽑아주는 익스텐션이다.

### 두 가지 모드 — SESSION과 OBJECT

`pgaudit`의 가장 큰 결정 사항은 두 가지 모드 중 무엇을 쓸지다.

**SESSION 모드**는 분류된 카테고리 단위로 모든 쿼리를 로그에 남긴다. 카테고리는 다음과 같다.

| 클래스 | 내용 |
|--------|------|
| `READ` | SELECT, COPY ... TO |
| `WRITE` | INSERT, UPDATE, DELETE, TRUNCATE |
| `FUNCTION` | 함수 호출 |
| `ROLE` | GRANT, REVOKE, CREATE/ALTER/DROP ROLE |
| `DDL` | 모든 DDL |
| `MISC` | DISCARD, FETCH 등 기타 |
| `ALL` | 위 전부 |

`pgaudit.log = 'ddl, role, write'` 같이 잡으면, DDL과 권한 변경, 쓰기 작업만 로그에 떨어진다. 매우 자주 실행되는 READ는 빠진다. 양이 줄어든다.

**OBJECT 모드**는 더 세밀하다. 특정 role이 권한을 가진 객체에 대해서만 로그를 남긴다. `pgaudit.role`에 audit 전용 role을 지정하고, 그 role에 감사하려는 테이블만 권한을 부여한다. 이렇게 하면 "민감한 테이블 다섯 개에 대해서만 모든 접근을 기록"하는 정밀 감사가 가능해진다.

```sql
CREATE ROLE auditor NOLOGIN;
GRANT SELECT, INSERT, UPDATE, DELETE ON members, payments, kyc_documents TO auditor;
```

```conf
shared_preload_libraries = 'pgaudit'
pgaudit.role = 'auditor'
pgaudit.log = 'read, write'
```

이 설정으로 `members`, `payments`, `kyc_documents` 세 테이블에 대해서만 모든 READ와 WRITE가 로그에 떨어진다. 다른 테이블은 무시한다. 신호 대비 잡음 비가 폭발적으로 좋아진다.

### 어느 모드를 고를까

처음에 어느 쪽을 골라야 할지 혼란스러울 수 있다. 경험에서 나온 권장은 이렇다.

- **컴플라이언스 외부 감사가 명시적으로 요구되는 시스템(금융·결제·의료)**: OBJECT 모드 + SESSION의 `ddl, role` 조합. 민감 테이블은 OBJECT로 정밀하게, 권한·DDL 변경은 SESSION으로 누락 없이.
- **일반 SaaS·내부 시스템**: SESSION 모드 `ddl, role, write`. 변경 흔적과 권한 흔적만 모은다. READ는 보통 의미 있게 감사하기 어렵다.
- **개발·스테이징**: 켜지 말거나, `log` 없이 깔아만 둔다. 운영에서 어떤 로그가 나올지 미리 보기 위한 검증용으로만.

OBJECT와 SESSION을 동시에 쓸 수도 있다. SESSION으로 넓게 잡고, OBJECT로 깊게 잡는 조합이다. 다만 양쪽에서 같은 쿼리가 로그에 두 번 들어갈 수 있다는 점은 알아두자.

### 로그의 무게 — 보관과 로테이션

audit 로그는 일반 PG 로그와 같은 파일에 떨어진다. 그래서 PG 로그 로테이션 설정이 audit 로그 운명도 함께 결정한다.

```conf
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_rotation_age = 1d
log_rotation_size = 1GB
log_truncate_on_rotation = on
```

운영 권장은 다음과 같다.

- 로컬 디스크에 7~14일치만 두고, 그 이상은 외부로 옮긴다.
- 외부 저장소는 S3 같은 객체 스토리지 + Glacier 같은 콜드 스토리지로 단계화한다.
- 보관 기간은 컴플라이언스 요구를 따른다. 일반적으로 1년, 금융은 5년 이상.

### SIEM 연동 — 로그를 의미 있게 만드는 마지막 단계

audit 로그가 디스크에만 쌓이는 시스템은 사고 후 분석에서 한계가 빠르다. 의미 있는 운영은 로그를 SIEM(Splunk, ELK, CloudWatch Logs Insights, Datadog 등)에 흘려보내고, 그 위에 알람과 대시보드를 얹는다.

연결 방식은 셋 중 하나다.

1. **로그 수집 에이전트** — Fluentd, Vector, Filebeat 같은 도구를 PG 호스트에 깔고 audit 로그를 파싱해 SIEM으로 전송한다. 가장 보편적인 방식.
2. **syslog로 흘려보내기** — `log_destination = 'syslog'`로 PG가 직접 syslog에 떨어뜨리고, syslog 서버에서 라우팅한다. 인프라가 이미 syslog 중심이라면 자연스럽다.
3. **매니지드 PG의 통합** — RDS는 CloudWatch Logs로, Cloud SQL은 Cloud Logging으로, Azure는 Log Analytics로 흘려보낸다. 매니지드의 가장 큰 장점 중 하나.

SIEM에서 다음과 같은 알람을 미리 만들어두는 편이 낫다.

- `BYPASSRLS` role 사용 횟수가 분 단위 한도를 넘으면 알림
- 운영 시간 외 DDL 발생 시 알림
- 같은 IP에서 인증 실패가 N분에 M회 이상이면 알림
- `pg_dump`나 `COPY ... TO` 같은 대량 내보내기 발생 시 알림

알람의 일부는 노이즈겠지만, 진짜 사고는 그중 한 두 개가 잡아낸다.

기억해두자. 감사는 "로그를 남기는 것"이 아니라 "필요할 때 답을 주는 것"이다. pgaudit는 도구일 뿐이고, 도구를 어디까지 책임지게 만들지가 운영의 일이다.

## 22.6 CVE 추적과 패치 정책 — 사고 전에 알고, 사고 후에 빠르게

PostgreSQL 진영은 보안 이슈를 비교적 잘 다룬다. 자체 CVE Numbering Authority(CNA)로 등록돼 있어서, CVE 번호 발급부터 패치 공개까지를 일관된 절차로 처리한다. Red Hat이 root CNA로 위에 있다. 외부에 흩어진 보안 보고를 한 곳으로 모으는 구조다.

그런데 그 절차가 잘 돌아간다고 우리 클러스터가 안전해지지는 않는다. 알고, 평가하고, 패치하는 일이 우리 몫이다.

### 알아두면 좋은 채널

다음 셋을 RSS·메일·Slack 어디든 한 곳에 모아두는 편이 낫다.

- **security.postgresql.org** — 공식 CVE 발표 페이지. 가장 권위 있고 가장 빠르다.
- **pgsql-announce 메일링 리스트** — minor 릴리스 발표. CVE 패치가 포함된 릴리스도 여기로 통지된다.
- **벤더 보안 공지** — RDS, Aurora, Cloud SQL, AlloyDB, Azure 각각의 보안 페이지. 매니지드 PG의 minor 업그레이드 일정이 여기서 결정된다.

### 최근 사례로 본 CVE의 무게

추상적으로 말하면 와닿지 않으니, 최근 사례 몇 개를 같이 보자.

**CVE-2024-10976** — RLS 정책이 서브쿼리에서 user ID 변경을 인식하지 못해 일부 행을 더 보여줄 수 있다. 멀티테넌트 시스템에 직격탄이 될 수 있는 이슈다. 패치 전에는 정책이 충분히 강하다고 안심할 수 없다.

**CVE-2024-10977** — libpq가 중간자(MITM)로부터 받은 에러 메시지를 그대로 남겨, 클라이언트 측에 가짜 진단 정보가 흘러들 수 있다. verify-full을 안 쓰는 클라이언트라면 영향이 크다.

**CVE-2025-1094** — `psql`의 SQL injection 취약점. 운영에서 `psql -c "..."`로 임의 입력을 실행하는 스크립트가 있다면 위험하다.

**CVE-2025-8713 / 8714 / 8715** — 2025년 8월 14일에 PG 13~17에 동시에 적용된 긴급 패치. `pg_dump`의 객체 이름에 개행 문자가 들어가면 백업을 복원하는 시점에 임의 코드 실행이 가능했다. 백업 파일을 신뢰하지 못하는 환경에서 복원하는 시스템이라면 정말 끔찍한 시나리오다.

이런 이슈들이 평균 분기마다 한 번 정도는 등장한다고 보면 된다. 그래서 패치를 빠르게 적용할 수 있는 운영 체계가 필요하다.

### 패치 정책 — CPM의 관점

대규모 운영은 보통 CPM(Continuous Patch Management) 정책을 가진다. 정책의 골격은 이렇다.

1. **Severity 분류** — Critical / High / Medium / Low로 나눈다.
2. **SLA 매핑** — Critical은 72시간 이내, High는 2주 이내, Medium은 다음 정기 패치 윈도우, Low는 분기 패치 윈도우.
3. **검증 단계** — 스테이징에서 minor 업그레이드를 먼저 돌리고, 회귀 테스트를 본다.
4. **운영 적용** — 정기 패치 윈도우(보통 한 달에 한 번, 트래픽이 적은 시간대)에 일괄 적용.
5. **롤백 계획** — 패치가 문제를 일으키면 30분 내 이전 minor 버전으로 롤백하는 절차.

자체 운영이라면 위 절차를 자기 손으로 만들어야 한다. minor 업그레이드는 PG가 binary 호환을 보장하므로 in-place 업그레이드가 가능하다. major 업그레이드만큼 두렵지 않다.

### 매니지드 PG의 minor 업그레이드 — 자동인가 수동인가

매니지드 PG는 minor 업그레이드를 자동으로 적용하는 옵션을 제공한다. 듣기엔 편해 보이지만, 운영에서는 트레이드오프가 있다.

**자동 minor 업그레이드의 장점:**
- CVE 패치가 출시되면 며칠 내로 자동 반영
- 운영팀의 관리 부담이 감소

**자동 minor 업그레이드의 단점:**
- 업그레이드 시점이 벤더가 정한 maintenance window 안. 항상 우리 트래픽 최저점은 아님.
- 회귀가 발생해도 롤백이 어려움. 매니지드 PG는 보통 이전 minor 버전으로의 다운그레이드를 지원하지 않음.
- 익스텐션이 minor 업그레이드와 함께 자동 갱신되지 않는 경우가 있어, 버전 mismatch가 생길 수 있음.

권장은 다음과 같다.

- 일반 SaaS·내부 시스템: 자동 minor 업그레이드 켜두고, 벤더의 maintenance window를 사내 트래픽 저점으로 설정.
- 결제·금융·의료처럼 큰 영향이 있는 시스템: 자동을 꺼두고, 사내 변경 관리 절차를 거쳐 수동으로 적용. 다만 SLA를 사내 정책으로 정하고 어기지 않는다.

major 업그레이드는 어떤 경우에도 자동을 권하지 않는다. v17→v18처럼 큰 변화가 있는 업그레이드는 호환성 점검과 회귀 테스트, 페일오버 시점 계획이 모두 필요하다.

기억해두자. CVE는 "남이 만든 문제"가 아니라 "내가 운영하는 시스템의 문제"다. 채널을 한 곳에 모으고, 패치 SLA를 미리 정해두는 그 두 가지만으로 사고의 절반은 줄어든다.

## 22.7 데이터 마스킹과 익명화 — anon 익스텐션의 자리

여기까지의 7할은 "들어오는 길"의 보안이었다. 마지막 두 절은 "나가는 데이터"의 보안이다.

상상해보자. 개발팀이 운영 DB의 일부 복제본을 받아서 분석 환경에서 쿼리를 돌린다고. 또는 외부 분석 회사에 일부 데이터를 넘긴다고. 또는 개발 환경에 실제 데이터를 복사해 테스트한다고. 셋 다 흔하다. 그런데 그 데이터에 주민등록번호, 이메일, 휴대전화, 신용카드 정보가 들어 있다면? 한 번 빠져나가면 회수가 불가능하다.

GDPR이든 개인정보보호법(PIPA)이든 이 영역에 명시적인 요구를 둔다. 개인을 식별할 수 있는 정보는 가능한 한 노출을 줄이고, 불가피하면 가명화·익명화 처리를 거치라는 원칙이다.

### PostgreSQL Anonymizer — 마스킹의 표준

PG 진영의 표준 도구가 `postgresql_anonymizer`(줄여서 anon) 익스텐션이다. 마스킹 규칙을 DDL로 선언하고, PG 안에서 직접 처리한다. 외부 도구로 데이터를 빼내서 마스킹하는 방식보다 노출 면적이 훨씬 좁다.

세 가지 사용 패턴이 있다.

**1. 동적 마스킹(Dynamic Masking)** — 운영 데이터는 그대로 두고, 특정 role로 로그인했을 때 마스킹된 값을 보여준다.

```sql
SECURITY LABEL FOR anon ON COLUMN users.email
  IS 'MASKED WITH FUNCTION anon.fake_email()';
SECURITY LABEL FOR anon ON COLUMN users.ssn
  IS 'MASKED WITH FUNCTION anon.partial(ssn, 6, ''*******'', 0)';
SECURITY LABEL FOR ROLE analyst IS 'MASKED';
```

`analyst` role로 들어오면 `users.email`은 가짜 이메일로, `users.ssn`은 앞 6자리만 보이는 부분 마스킹으로 나온다. 다른 role은 그대로 본다. 운영 DB 위에서 분석을 돌리는 시나리오에 잘 맞는다.

**2. 정적 마스킹(Static Masking)** — 데이터 자체를 마스킹된 값으로 교체한다. 되돌릴 수 없다.

```sql
SELECT anon.anonymize_database();
```

별도 분석 환경이나 개발 환경에 운영 데이터의 복제본을 넘기기 전에 한 번 돌린다. 이렇게 처리한 데이터는 외부로 나가도 위험이 훨씬 줄어든다.

**3. 익명 덤프(Anonymous Dumps)** — `pg_dump` 시점에 마스킹을 적용한다.

```sh
pg_dump_anon --host=prod --dbname=app --file=anon.sql
```

운영 DB의 무결성을 건드리지 않고, 덤프 파일만 가명화된 채로 나온다. 외부 공유용으로 가장 안전하다.

### 어떤 마스킹 함수를 쓸까

anon은 다양한 마스킹 전략을 함수로 제공한다.

- `anon.fake_email()`, `anon.fake_first_name()`, `anon.fake_phone()` — 그럴듯한 가짜값으로 교체. 분석의 의미가 어느 정도 유지된다.
- `anon.random_int_between(a, b)`, `anon.random_date_between(d1, d2)` — 범위 안의 랜덤값.
- `anon.partial(value, prefix, mask, suffix)` — 일부만 가린다. `010-****-1234` 같은 형태.
- `anon.pseudo_email(value)` — 같은 입력에 항상 같은 가짜 출력. 분석에서 조인이 가능하다.
- `anon.noise(value, ratio)` — 숫자에 노이즈 추가. 통계의 형태는 유지되면서 개인 식별성은 줄어든다.

여기서 한 가지 짚어두자. GDPR은 가명화(pseudonymization)와 익명화(anonymization)를 구분한다. 가명화는 "되돌릴 수 있는" 처리고, 익명화는 "되돌릴 수 없는" 처리다. GDPR은 가명화된 데이터를 여전히 "개인 데이터"로 본다. 그래서 가명화만으로 GDPR이 요구하는 보호를 다 했다고 안심할 수 없다. 분석의 의미를 보존해야 하는 경우엔 가명화로 가되, 외부 노출이라면 익명화 쪽이 안전하다.

### 운영 패턴 — 어디서 마스킹을 거는가

자주 보는 패턴 셋이다.

**개발 환경 데이터 동기화:**
1. 운영 백업을 받는다.
2. 스테이징 환경에 복원한다.
3. anon 익스텐션을 설치하고 마스킹 라벨을 적용한다.
4. `anonymize_database()`로 정적 마스킹을 돌린다.
5. 그 결과를 개발 환경으로 다시 복제한다.

5단계가 번거롭게 보이지만, 4번 단계에서 운영 데이터의 원본이 개발 환경으로 직접 가지 않는다는 보장이 핵심이다.

**외부 분석사 데이터 공유:**
1. 별도 분석용 PG 인스턴스를 운영의 streaming replica로 띄운다.
2. 그 인스턴스에 anon을 깔고 동적 마스킹을 적용한다.
3. 외부 사용자는 마스킹된 role로만 접근.

**GDPR 삭제 요청 대응:**
GDPR의 "삭제권" 요청이 들어오면 단순 DELETE로는 부족하다. WAL, 백업, 로그, audit 로그에 모두 남아 있을 수 있기 때문이다. anon의 익명화 함수로 해당 행을 가짜값으로 덮어쓰고, 백업의 보관 기간이 지나도록 기다리는 패턴이 일반적이다. 단순한 일이 아니지만 적어도 운영 DB 안에서는 식별 가능성이 사라진다.

기억해두자. 마스킹은 "노출을 줄이는 일"이지 "보안을 만드는 일"이 아니다. 다만 그 줄이는 일이 GDPR과 PIPA의 명시적인 요구이고, 사고가 났을 때의 피해 규모를 한 자리 수 단위로 줄여준다.

## 22.8 보안 베이스라인 체크리스트 — D+0, 분기점검, 사고 대응

여기까지 일곱 절을 통해 본 항목들을 의사결정 표로 모아두자. 머릿속에 흩어진 것을 손에 잡히는 한 페이지로 만드는 일이다.

### 신규 클러스터 D+0 체크리스트

새 클러스터를 띄우는 날 무엇을 끝내야 할까. 다음 항목을 빠뜨리지 말자.

**인증과 암호**
- [ ] `password_encryption = scram-sha-256` 설정 확인
- [ ] `pg_hba.conf`에서 `md5` 라인 제거 또는 `scram-sha-256`으로 교체
- [ ] `host` 라인을 `hostssl`로 교체 (또는 `hostnossl ... reject` 명시)
- [ ] CIDR 범위를 최소 필요 범위로 축소 (`0.0.0.0/0` 제거)
- [ ] superuser 비밀번호 vault에 저장, 평소 로그인 금지

**전송 보안**
- [ ] `ssl = on`, 인증서·키 파일 설치
- [ ] 인증서 만료일을 모니터링에 등록 (60일 알림)
- [ ] 클라이언트 측 `sslmode=verify-full` 표준 적용
- [ ] root CA 파일을 클라이언트 측에 명시적으로 배포
- [ ] (매니지드 PG) 벤더 root CA 회전 일정 캘린더 등록

**권한 모델**
- [ ] 그룹 role 계층 설계 (`app_read`, `app_write`, `app_admin`)
- [ ] `ALTER DEFAULT PRIVILEGES` 설정으로 신규 객체 자동 권한
- [ ] 애플리케이션 계정 분리 (읽기·쓰기·관리·복제)
- [ ] `public` 스키마의 CREATE 권한 회수 (PG 15 이하)
- [ ] 모든 운영 비밀번호 vault 발급으로 전환

**RLS (해당하는 경우)**
- [ ] 멀티테넌트 테이블에 `ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL SECURITY` 둘 다 적용
- [ ] `BYPASSRLS` 전용 role 분리, 일상 사용 금지
- [ ] 인덱스에 `tenant_id` 선행 포함 (`(tenant_id, ...)`)
- [ ] 주요 쿼리에 대해 EXPLAIN으로 정책 술어 인덱스 적용 확인
- [ ] RLS 우회 사용을 audit 로그에 기록하는 트리거 설치

**감사**
- [ ] `pgaudit` 설치 (`shared_preload_libraries`)
- [ ] OBJECT 또는 SESSION 모드 선택, `pgaudit.log` 설정
- [ ] 로그 로테이션 정책 적용 (7~14일 로컬)
- [ ] 외부 저장소(S3·GCS·Azure Blob)로 archival
- [ ] SIEM 연동 + 기본 알람 4종 설치 (BYPASSRLS, 시간 외 DDL, 인증 실패 burst, 대량 export)

**CVE 추적**
- [ ] `pgsql-announce` 메일링 구독
- [ ] security.postgresql.org RSS를 Slack/메일에 연동
- [ ] minor 업그레이드 SLA 사내 문서화 (Critical 72시간, High 2주)
- [ ] 매니지드 PG의 maintenance window를 트래픽 저점으로 설정

**마스킹**
- [ ] 개인정보 컬럼 카탈로그화
- [ ] 개발·분석 환경 데이터 동기화에 정적 마스킹 적용
- [ ] 외부 공유 시 익명 덤프 사용 정책 문서화

### 분기점검 체크리스트

분기마다 한 번씩, 다음 항목들을 한 시간 안에 훑는 점검 시간을 마련하자.

- 미사용 계정 발견 — 지난 90일 로그인 없음, `pg_stat_activity`와 audit 로그 교차 확인
- 권한 변화 추적 — 분기 동안 GRANT/REVOKE 이력 검토, 의도하지 않은 권한 확장이 있는지 확인
- 인증서 만료 임박 점검 — 90일 안에 만료되는 인증서 목록 작성
- minor 업그레이드 누락 점검 — 운영 중인 minor 버전과 최신 minor 버전의 갭 확인, 갭이 두 단계 이상이면 점검 일정 잡기
- audit 로그 무결성 점검 — SIEM에서 audit 로그가 끊긴 구간이 없는지, 일일 라인 수 추세 확인
- BYPASSRLS 사용 횟수 추세 — 비정상적인 증가가 있는지 확인
- 백업 마스킹 정책 적용 확인 — 외부에 나간 덤프 파일이 마스킹된 버전인지 한 건 샘플링
- 매니지드 PG 익스텐션 버전 확인 — pgaudit, pg_anonymizer, 기타 보안 관련 익스텐션의 버전과 가용성

### 사고 대응 체크리스트

사고 의심이 들어왔다. 무엇부터 할까. 다음 흐름이 일반적이다.

**1. 초동 격리 (0~30분)**
- 의심 계정·IP에서의 접근 차단 — `pg_hba.conf`에 reject 라인 추가하고 `pg_reload_conf()`
- 진행 중인 위험 세션 종료 — `pg_terminate_backend(pid)`
- 매니지드 PG라면 보안 그룹에서 해당 IP 즉시 차단

**2. 증거 보존 (30분~2시간)**
- 현재 audit 로그를 스냅샷으로 별도 저장 — 로그 로테이션이 덮어쓰기 전에
- `pg_stat_activity`, `pg_stat_user_tables`, `pg_locks` 현재 상태 저장
- WAL 보관 기간을 임시로 연장
- 운영 PG의 일관된 스냅샷 생성 (포렌식용 별도 백업)

**3. 영향 분석 (2시간~)**
- audit 로그에서 의심 계정·세션의 모든 행위 추출
- READ 흔적이 있다면 어떤 테이블·행을 읽었는지
- WRITE 흔적이 있다면 어떤 변경이 일어났는지
- BYPASSRLS 사용 흔적이 있다면 우선순위 최상

**4. 복구와 통지**
- 변경이 일어났다면 PITR(19장 참조)로 사고 직전 시점으로 복원 또는 부분 복구
- 영향받은 사용자에게 통지 (GDPR은 72시간, PIPA는 24시간 이내)
- 사후 분석 문서화 (RCA), 같은 사고가 재발하지 않도록 체크리스트 갱신

**5. 사후 강화**
- 사고 유형에 맞는 신규 알람 추가
- D+0 체크리스트에 누락된 항목 보강
- 분기점검 항목 추가

사고 대응이 잘 굴러가는 팀은 한 가지 공통점이 있다. 위 흐름을 한 페이지로 인쇄해 두고, 분기마다 한 번씩 모의 훈련을 한다. 진짜 사고가 났을 때 첫 30분의 손이 멈추지 않는다. 그게 가장 큰 차이다.

## 마무리 — 보이지 않는 일에 대한 인정

보안과 감사는 보이지 않는 일이다. 잘 굴러갈 때는 아무도 인정해주지 않고, 사고가 났을 때만 책임을 묻는다. 그래서 운영팀이 가장 외로운 영역이기도 하다.

그럼에도 이 장의 항목들을 D+0에 박아두고 분기마다 점검하는 시스템은 분명한 차이를 만든다. PostgreSQL이라는 도구는 강한 보안 기능을 다 갖췄다. 다만 그 기능들이 디폴트로 켜져 있지 않을 뿐이다. 켜는 일, 그리고 켜진 채로 유지하는 일이 우리 몫이다.

이제 책의 운영 파트가 후반부에 들어선다. 다음 장에서는 성능 튜닝의 종합 정리를 다룬다. 인덱스 선택, EXPLAIN 읽기, 흔한 함정 여섯 가지, 병렬 쿼리, 파티셔닝, 그리고 OS 레벨 체크리스트까지. 보안이 "안전하게 굴러가는 시스템"이라면, 다음 장은 "빠르게 굴러가는 시스템"이다. 둘이 동시에 만족돼야 진짜 운영급이라고 부를 만하다. 같이 살펴보자.
