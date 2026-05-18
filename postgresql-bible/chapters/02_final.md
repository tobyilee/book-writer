# 2장. MySQL 베테랑이 가장 먼저 부딪히는 여덟 가지

새 언어를 배울 때 가장 무서운 건 모르는 문법이 아니다. *내가 안다고 착각하는* 문법이다. 모르는 건 어차피 사전을 펴게 된다. 그런데 안다고 믿으면 사전을 닫는다. 그 닫힌 사전 위에서 사고가 난다.

MySQL을 오래 쓴 사람이 PostgreSQL로 옮길 때 똑같은 일이 벌어진다. SELECT와 INSERT는 같은 모양이고, 트랜잭션도 같은 단어를 쓰고, 인덱스 추가하는 DDL도 어딘가 비슷하다. 그런데 한 줄 한 줄 똑같이 생긴 문법 아래에서 데이터베이스가 하는 일은 전혀 다르다. 동시에 들어온 두 트랜잭션이 어떻게 동시성을 처리하는지, UPDATE 한 줄이 디스크에 어떤 흔적을 남기는지, 시퀀스가 어떻게 발급되는지, LIMIT 한 줄이 어떤 결과를 돌려주는지. 같은 단어 아래 다른 동사가 숨어 있다.

이 장은 그 다른 동사들의 지도다. 정확히 여덟 군데에서 MySQL 베테랑의 손은 처음으로 미끄러진다. 살펴보자, 어디서 미끄러지는지. 그리고 각 미끄러짐이 책의 어느 장에서 본격적으로 풀리는지도 같이 안내해두자. 그래야 이 장은 책 전체의 입구가 된다.

미리 한 가지 약속을 해두자. 이 장은 "어디서 미끄러지는지의 지도"고, 실제로 미끄러진 사람들의 이야기는 17장의 마이그레이션 실전 챕터에서 다룬다. 4억 row를 옮긴 사람, 47개 쿼리가 timezone 때문에 깨진 사람, 발견된 버그가 127개였던 사람의 이야기를 여기서 풀면 지도가 풍경에 묻혀버린다. 우리는 먼저 지도를 펴고, 풍경은 나중에 함께 보자.

## 2.1 동시성 모델 — thread-per-connection vs fork

MySQL을 운영해본 사람에게 커넥션 수를 물으면 대개 천 단위 숫자가 돌아온다. 2,000, 3,000, 그 이상도 흔하다. 그래도 시스템은 굴러간다. 메모리도 그럭저럭 견딘다. InnoDB가 thread-per-connection 모델을 쓰기 때문이다. 한 커넥션이 들어오면 OS 프로세스 안에 가벼운 스레드 하나가 더 생긴다. 같은 메모리 공간을 공유하고, 컨텍스트 스위치 비용도 상대적으로 가볍다.

같은 머릿속을 들고 PostgreSQL로 와서 max_connections를 2,000으로 잡았다고 해보자. 두 가지가 동시에 일어난다. 메모리가 갑자기 가파르게 올라가고, CPU 사용률은 정상 같은데 응답 시간이 점점 길어진다. 끔찍한 일이다. 도대체 어디서 새는지 모르는 채로 새벽에 호출이 온다.

원인은 단순하다. PostgreSQL은 스레드를 쓰지 않는다. 클라이언트가 접속할 때마다 postmaster라는 부모 프로세스가 `fork()`를 호출해 자식 프로세스를 만든다. **1 connection = 1 OS process**. 이 한 줄이 PostgreSQL 운영의 절반을 결정한다.

```
[클라이언트] ──연결─→ [postmaster]
                         │
                         ├── fork() ──→ [backend process 1]
                         ├── fork() ──→ [backend process 2]
                         ├── fork() ──→ [backend process 3]
                         └── fork() ──→ [backend process N]
```

프로세스 하나마다 자기 메모리 컨텍스트가 있다. work_mem이 4MB라면 정렬·해시 노드가 동시에 여러 개 돌 때 한 프로세스가 그 4MB의 여러 배를 잡을 수도 있다. 거기에 운영체제가 프로세스 컨텍스트 스위치를 해야 하는데, 스레드 스위치보다 본질적으로 더 무겁다.

그렇다면 어떻게 해야 할까? 답은 외부 풀러를 앞에 두는 것이다. PgBouncer나 Pgcat 같은 도구가 애플리케이션과 PostgreSQL 사이에 앉아 실제 PostgreSQL 커넥션 수를 적게 유지한다. 애플리케이션은 풀러에 마음껏 연결하고, 풀러는 그 수많은 클라이언트 연결을 작은 백엔드 프로세스 풀에 다중화한다.

MySQL에서 커넥션 풀이 *비용 절감*의 도구였다면, PostgreSQL에서는 *생존*의 도구다. 표현이 과해 보이지만 실제로 그렇다. 풀러 없이 PG를 production에서 안정적으로 굴리는 일은 작은 규모를 제외하면 거의 없다. 이게 권장이 아니라 사실상 필수라는 말이 나오는 이유다.

이 차이를 발견하는 순간 한 가지 의문이 따라온다. *왜 PostgreSQL은 스레드 모델을 안 쓰는가?* 역사적인 답은 멀티스레드가 흔치 않던 시절의 BSD-style 설계라는 것이고, 실용적인 답은 프로세스 격리가 안정성을 준다는 것이다. 한 프로세스가 죽어도 다른 백엔드는 영향을 받지 않는다. 다만 그 안전성을 누리려면 커넥션 풀러라는 짝꿍을 같이 데려와야 한다.

조금 더 구체적인 숫자로 감을 잡아보자. PostgreSQL 백엔드 프로세스 하나가 기본 상태에서 점유하는 메모리는 대략 5~10MB 수준에서 시작한다. 거기에 work_mem(기본 4MB)을 쿼리의 정렬·해시 노드별로 잡고, temp_buffers·prepared statement 캐시 같은 부수 비용이 붙는다. 복잡한 분석 쿼리가 돌면 한 프로세스가 수십 MB에서 100MB까지 부풀 수 있다. 이 상태로 2,000개 커넥션이 동시에 살아 있다고 계산해보자. 산술은 무서운 결과를 돌려준다.

여기에 운영체제 레벨의 비용이 한 겹 더 올라간다. 프로세스 수가 늘수록 페이지 테이블 크기, 컨텍스트 스위치 비용, 캐시 라인 경쟁이 모두 늘어난다. *CPU 사용률은 낮은데 응답 시간이 길어진다*는 증상이 바로 이 영역에서 나온다. APM이 보여주는 단순한 CPU·메모리 게이지만으로는 안 잡힌다. *왜 느리지?*라는 질문에 답하기까지 한참이 걸린다.

그래서 PostgreSQL 진영의 권장 max_connections는 의외로 작다. *코어 수 × 2~4* 정도의 매우 보수적인 숫자를 기본으로 잡고, 그 위에 PgBouncer 같은 풀러를 얹어 클라이언트 측 동시성을 따로 받는다. 8코어 머신에 max_connections 100, 풀러로 클라이언트 1,000개를 받는 식이다. *수치가 너무 작은 거 아닌가?* 처음엔 의심스럽지만, 실제로 그렇게 운영하는 편이 압도적으로 안정적이다.

여기서 풀러의 모드 이야기를 잠깐 짚어둘 필요가 있다. PgBouncer는 세 가지 풀링 모드를 지원한다. session·transaction·statement. *session*은 클라이언트 연결과 백엔드 연결을 1:1로 묶고 클라이언트가 끊을 때까지 유지한다. *transaction*은 트랜잭션 단위로 백엔드를 빌려준다. *statement*는 statement 단위. 가장 자주 쓰이는 transaction 모드가 가장 효율적이지만, 그 효율 뒤에 함정이 숨어 있다. prepared statement, advisory lock, SET LOCAL이 트랜잭션 경계를 넘어가지 못한다. 이 함정은 21장에서 본격적으로 다룬다. 여기서는 *fork 모델이 풀러를 부르고, 풀러가 다시 모드별 트레이드오프를 부른다*는 사슬만 머리에 그려두자.

이 주제를 더 깊이 파헤치는 곳은 4장이다. 4장에서 postmaster·백그라운드 프로세스의 풀세트·shared_buffers·WAL buffer의 메모리 모델을 다룬다. 풀러 선택과 transaction pooling의 함정 같은 실전 도구 비교는 21장에서 다시 만난다. 우리는 여기서 이 한 줄만 기억하고 가자 — *PostgreSQL은 fork 위에 서 있다.*

## 2.2 MVCC 저장 방식 — undo log vs append-only

MySQL과 PostgreSQL은 둘 다 MVCC, 즉 다중 버전 동시성 제어를 쓴다고 한다. 같은 이름이다. 그래서 같은 일을 한다고 믿기 쉽다. 그런데 들여다보면 두 시스템은 같은 결과를 *전혀 다른 방식*으로 만든다. 이 차이가 운영의 무게를 결정적으로 바꾼다.

상황을 하나 가정해보자. `users` 테이블의 한 row에서 email 컬럼만 바꿨다. InnoDB는 어떻게 처리할까? 클러스터 인덱스의 그 row를 *그 자리에서* 새 값으로 덮는다. 이전 값은 어디로 갈까? 별도의 **undo log**에 압축적으로 적힌다. 누군가 옛 스냅샷을 봐야 할 때 — 가령 보고 쿼리가 한참 돌고 있다면 — undo log를 거꾸로 거슬러 올라가 옛 값을 재구성한다. 트랜잭션이 끝나면 purge thread가 undo log를 자동으로 청소한다.

PostgreSQL은 다르다. 같은 UPDATE가 들어오면 기존 row는 그 자리에 *그대로* 둔다. 다만 그 row의 `xmax`에 종료 트랜잭션 ID를 표시한다. *이 row는 이 시점부터 죽은 것으로 보세요*라는 표시다. 그리고 새 row를 같은 테이블의 어딘가에 추가한다. 가능하면 같은 데이터 페이지 안에. 두 row는 동시에 디스크에 살아 있다. 한쪽은 옛 버전, 다른 한쪽은 새 버전. 한참 도는 보고 트랜잭션은 옛 버전을 자연스럽게 본다.

여기까지는 두 방식 다 멋져 보인다. 그런데 죽은 row는 누가 치우는가? PostgreSQL에서는 **VACUUM**이라는 별도 프로세스가 그 일을 한다. 자동으로 도는 autovacuum이 표시된 dead tuple을 주기적으로 회수한다.

```
INSERT 한 줄, UPDATE 두 번 후의 한 페이지 모습:

Page #42
┌─────────────────────────────────────┐
│ tuple 1 (xmin=100, xmax=105) ← dead │  ← 처음 INSERT 후 UPDATE된 옛 버전
│ tuple 2 (xmin=105, xmax=110) ← dead │  ← 두 번째 UPDATE된 옛 버전
│ tuple 3 (xmin=110, xmax=∞)   ← live │  ← 현재 유효한 버전
│ ...                                  │
│ 빈 공간                              │
└─────────────────────────────────────┘
```

이 그림이 PostgreSQL MVCC의 거의 전부다. 단순하고 우아하다. 그런데 단순한 만큼 비용이 분명하다.

첫 번째 비용은 **table bloat**다. 죽은 row가 vacuum보다 빨리 쌓이면 데이터 페이지가 부풀어 오른다. 같은 1만 row를 읽는데 디스크에서 읽어야 할 페이지 수가 두 배, 세 배가 된다. 캐시 효율은 곤두박질친다. 쿼리가 갑자기 느려진다.

두 번째 비용은 **index amplification**이다. 새 row 버전이 새로운 디스크 위치에 들어가면, 그 위치를 가리키도록 *모든* secondary index에도 새 entry를 만들어 넣어야 한다. 인덱스 한두 개가 아니라 다섯 개, 열 개 있다면 UPDATE 한 번이 인덱스 다섯 번, 열 번의 쓰기로 증폭된다.

이 두 가지 비용을 두고 카네기 멜런의 Andy Pavlo 교수는 *"PostgreSQL에서 우리가 가장 싫어하는 부분"*이라는 글을 썼다. 표현이 거칠어 보이지만 짚는 지점은 정확하다. Uber가 한때 PostgreSQL에서 MySQL로 돌아간 일이 있었는데, 그 결정의 기술적 핵심이 바로 이 index amplification이었다.

물론 PostgreSQL도 가만히 있지는 않았다. 다음 절에서 짚을 HOT(Heap-Only Tuple) 최적화가 이 비용의 큰 덩어리를 깎는다. fillfactor 설정으로 페이지에 여유 공간을 의도적으로 남겨두기도 한다. 17부터는 vacuum의 메모리 관리가 다시 쓰여 대용량 테이블에서의 vacuum 비용이 눈에 띄게 줄었다.

그래도 본질은 남는다. PostgreSQL의 운명에는 VACUUM이 늘 따라온다. 이것을 운영의 짐으로 느끼느냐, 정상적인 일과로 받아들이느냐는 운영자의 인식 전환에 달려 있다. MySQL 시절에 *purge thread? 그런 게 있었나?* 하는 정도였다면, PostgreSQL에서는 autovacuum이 어떻게 도는지를 매주 한 번은 들여다봐야 한다.

이 차이를 *불편함*이 아니라 *서로 다른 강점*으로 읽는 시각도 있다. append-only 방식은 *long-running 읽기 트랜잭션*에 강하다. 한 시간 짜리 보고 쿼리가 도는 동안 OLTP 트래픽이 계속 row를 갱신해도, 보고 쿼리는 자기 시점의 옛 버전을 그 자리에서 그대로 읽으면 된다. undo log를 거꾸로 재구성할 필요가 없다. 그래서 보고·분석 워크로드와 OLTP가 같은 DB에 섞여 있는 환경에서는 PostgreSQL의 MVCC 방식이 오히려 자연스럽다. *PG가 정확성과 표현력 우선, MySQL이 단순성과 처리량 우선*이라는 한 줄짜리 평가가 이 디테일들의 합으로 만들어진다.

여기 한 가지 함정을 미리 짚어두자. *long-running 트랜잭션*은 PostgreSQL의 강점이기도 하지만, 동시에 가장 큰 적이기도 하다. 오래 살아 있는 트랜잭션 하나가 *VACUUM이 회수하려는 dead tuple*을 *나 아직 그 옛 버전이 필요해요*라고 붙들면, VACUUM은 회수를 못 한다. 회수를 못 하면 bloat가 쌓이고, 쌓이면 또 다른 쿼리가 느려지고, 느려진 쿼리가 또 long-running이 되고. 도미노가 시작된다. *idle in transaction*으로 한참 잠든 세션 하나가 운영 야간 호출의 단골 범인이다. 이 도미노가 어떻게 시작되고 어떻게 끊는지는 5장에서 자세히 풀어둔다.

이 주제의 본격적인 깊이는 5장에서, 그리고 운영 측면의 처방은 18장에서 만난다. 5장은 dead tuple과 bloat이 왜 생기는지, HOT가 어떻게 비용을 깎는지, long-running 트랜잭션이 어떤 도미노를 일으키는지를 다룬다. 18장은 autovacuum 튜닝, XID wraparound 예방, pg_repack과 pg_squeeze 같은 도구를 다룬다. 5장이 *왜 그렇게 되는가*라면 18장은 *그래서 어떻게 손에서 떼지 않을 것인가*다.

## 2.3 클러스터 인덱스의 부재 — heap + 별도 인덱스

MySQL InnoDB를 오래 쓴 사람의 손에 박힌 한 가지 직관이 있다. *프라이머리 키 순서대로 row가 디스크에 깔린다*는 직관이다. InnoDB의 클러스터 인덱스가 그렇게 만든다. PK 자체가 데이터의 물리적 저장 순서를 결정한다. PK로 범위 검색하면 디스크에서 연속된 블록을 읽으므로 빠르다.

PostgreSQL에서 같은 직관을 들고 가면 두 가지가 깨진다.

첫째, PostgreSQL의 테이블은 **heap**이다. row가 어느 페이지의 어느 자리에 들어갈지는 INSERT 시점의 빈 공간에 따라 결정된다. PK 순서가 아니다. INSERT한 순서로 대충 쌓이고, UPDATE가 새 row 버전을 만들면 또 빈 공간에 들어간다. 디스크 위에서 PK 순서를 따라가는 보장은 없다.

둘째, PostgreSQL에서 PK는 *별도의 인덱스*다. 정확히 말하면 unique B-tree 인덱스 하나가 PK 제약 뒤에 자동으로 만들어진다. 이 인덱스는 PK 값에서 row의 물리적 위치(ctid)로 가는 포인터를 들고 있다. 다른 모든 인덱스도 마찬가지다. *키 → ctid*의 포인터 묶음이다.

이게 왜 중요한가? InnoDB에서는 secondary index가 *키 → PK*를 들고 있다. 인덱스로 찾은 PK로 다시 클러스터 인덱스를 한 번 더 찾아 들어가야 row를 만난다. 한 번의 인덱스 조회가 두 번의 트리 탐색이 되는 셈이다. 그래서 InnoDB는 PK가 짧을수록 secondary index도 작아진다.

PostgreSQL에서는 인덱스가 모두 *키 → 위치(ctid)*다. PK든 secondary든 같은 모양이다. 인덱스로 찾으면 곧장 heap의 그 위치로 간다. 그래서 secondary index도 PK가 길든 짧든 크기에 직접적인 영향이 없다.

```
InnoDB:
  PK Index:    [pk_value] → [row data 통째]
  Sec. Index:  [col_value] → [pk_value] → (PK Index 재탐색) → [row data]

PostgreSQL:
  PK Index:    [pk_value] → [ctid] → heap의 row
  Sec. Index:  [col_value] → [ctid] → heap의 row
```

이 차이가 만드는 실용적 결과 몇 가지가 있다.

먼저 PK 범위 검색이 InnoDB만큼 빠르다는 보장이 없다. InnoDB는 PK 순서로 쌓여 있으니 1번부터 1000번까지 읽으면 연속 블록이다. PostgreSQL은 INSERT 순서와 PK 순서가 같으면 우연히 비슷한 결과가 나오지만, UPDATE가 잦으면 점점 흐트러진다. 정말 PK 순서대로 물리 정렬을 원한다면 `CLUSTER` 명령을 *명시적으로* 한 번 돌려야 한다. 그것도 한 번 돌리면 그 시점의 정렬일 뿐, 시간이 지나면 다시 흐트러진다.

다음으로, 인덱스 컬럼을 자주 UPDATE하는 일이 더 비싸다. UPDATE가 새 row 버전을 만들면 그 위치를 가리키도록 *모든 인덱스에 새 entry*가 들어가야 한다는 점, 앞서 짚었다. 그래서 PostgreSQL 진영에는 *인덱스 컬럼은 함부로 건드리지 말 것*이라는 격언이 있다.

다행히 PostgreSQL에는 HOT(Heap-Only Tuple)이라는 영리한 최적화가 있다. *변경된 컬럼이 어떤 인덱스에도 속하지 않을 때, 그리고 같은 페이지에 충분한 여유 공간이 있을 때* 새 버전을 같은 페이지에 만들고 인덱스는 건드리지 않는다. ctid 체인으로 옛 버전과 새 버전을 잇는다. 인덱스는 옛 버전을 가리키는 포인터 하나만 두면 된다.

이 HOT가 잘 작동하느냐, 깨지느냐가 OLTP 시스템에서 PostgreSQL 성능의 절반을 결정한다고 해도 과장이 아니다. 6장에서 HOT의 두 조건, ctid 체인의 구조, fillfactor 90→70 트레이드오프, 모니터링하는 법(`n_tup_hot_upd` 컬럼)을 깊게 본다.

여기에서 잠깐 *마이그레이션 직후의 흔한 실수*도 하나 짚어두자. MySQL에서 PostgreSQL로 옮긴 직후, 인덱스를 *옛날 그대로* 가져오는 경우가 많다. 그런데 PostgreSQL에서는 인덱스의 의미가 살짝 다르다. InnoDB에서는 *모든 secondary index가 PK를 키 끝에 묶고 있는 구조*라 PK 컬럼을 인덱스에 한 번 더 넣을 필요가 없다. PostgreSQL에서는 PK 컬럼이 인덱스 키에 자연스럽게 들어가지 않는다. 그래서 *(status, created_at)* 같은 secondary index에 *id*까지 같이 넣어주거나, v11부터 도입된 `INCLUDE` 컬럼으로 *covering index*를 만들어주는 패턴이 더 자주 쓰인다.

```sql
-- PG에서 자주 쓰는 covering index 패턴
CREATE INDEX orders_status_created_idx
  ON orders (status, created_at)
  INCLUDE (id, user_id, total);
```

이렇게 만들면 `WHERE status = 'pending' AND created_at < ...`로 골라낸 row의 *id·user_id·total*까지 인덱스만 읽어 돌려줄 수 있다(*index-only scan*). heap을 안 만져도 되니 빠르고, MVCC visibility map과 협력해 *대부분 쓰기 직후의 row가 아니면* heap 접근을 건너뛴다.

여기서는 한 줄만 잡아두자 — *PostgreSQL의 인덱스는 클러스터가 아니라 항상 별도의 트리이며, HOT가 그 비용을 깎는다.*

## 2.4 데이터 타입 표현력 — array, range, hstore, JSONB

MySQL을 쓰다 PostgreSQL을 처음 만지면, 한 번쯤 *"이런 타입이 있다고?"* 하고 멈추는 순간이 온다. 배열 타입을 컬럼 자료형으로 그냥 선언할 수 있고, 범위 타입이 1급 객체로 있고, 키-값 쌍을 통째로 한 컬럼에 넣을 수 있고, JSON은 두 가지 변종이 있다. 표준 SQL이 보장하는 것을 넘어 *객체-관계형*이라는 PG의 정체성이 드러나는 지점이다.

하나씩 짧게 살펴보자.

**배열 타입.** `INTEGER[]`, `TEXT[]` 같은 타입이 컬럼 자료형으로 그대로 들어간다. *태그 다섯 개를 한 row에 붙이고 싶다*고 해보자. MySQL이라면 별도 테이블을 만들거나 콤마로 구분한 문자열을 쓰거나 JSON 배열을 쓴다. PostgreSQL은 `tags TEXT[]`라고 쓰면 끝이다. 검색은 `WHERE 'urgent' = ANY(tags)`나 GIN 인덱스로 처리한다. 한국의 *맞추다* 팀이 MySQL에서 PG로 옮긴 결정적인 이유 중 하나가 정확히 이 배열 타입이었다.

**범위 타입(range types).** `int4range`, `tsrange`, `daterange` 같은 타입이 있다. *예약 시간 범위가 겹치면 안 된다*는 제약을 데이터 타입 하나로 표현할 수 있다. EXCLUDE 제약과 함께 쓰면 *겹치는 예약은 INSERT 자체를 거부*하는 DB-레벨 비즈니스 규칙을 한 줄로 쓴다. v18에서는 시간 차원의 제약을 더 자연스럽게 표현하는 temporal constraint까지 표준에 가깝게 들어왔다.

**hstore.** 키-값 매핑을 한 컬럼에 넣는 타입이다. 사실상 JSONB 등장 이전의 *작은 문서 DB* 역할이었다. 지금은 JSONB가 거의 모든 시나리오를 흡수했지만 가벼운 메타데이터 저장이 필요하면 여전히 살아 있다.

**JSON과 JSONB.** 둘이 다르다는 점이 중요하다. `JSON`은 텍스트 그대로 저장한다. `JSONB`는 바이너리 표현으로 저장한다. 검색·인덱싱·키 액세스 비용이 압도적으로 다르다. *PG에서 JSON을 쓴다*고 말할 때는 거의 모두 JSONB를 가리킨다.

JSONB가 진짜로 빛나는 지점은 GIN 인덱스다. 키 기반 검색을 GIN으로 가속할 수 있고, `jsonb_path_ops`라는 좁은 연산자 집합을 쓰면 인덱스 크기를 더 줄이면서 자주 쓰는 패턴은 더 빠르게 만들 수도 있다. 거기에 *expression index*나 *partial index*로 특정 키만 골라 인덱싱하는 길도 있다. v17에서는 `JSON_TABLE`이 들어와 JSON을 SQL의 FROM 절에 펼쳐 일반 테이블처럼 쓸 수 있게 됐다.

```sql
-- 배열 타입
CREATE TABLE posts (
  id        BIGSERIAL PRIMARY KEY,
  title     TEXT NOT NULL,
  tags      TEXT[] NOT NULL DEFAULT '{}'
);
CREATE INDEX posts_tags_gin ON posts USING GIN (tags);

-- 범위 타입 + EXCLUDE
CREATE TABLE reservations (
  room_id   INT NOT NULL,
  during    TSRANGE NOT NULL,
  EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);

-- JSONB + 인덱스
CREATE TABLE events (
  id        BIGSERIAL PRIMARY KEY,
  payload   JSONB NOT NULL
);
CREATE INDEX events_payload_gin ON events
  USING GIN (payload jsonb_path_ops);
```

이 풍부함이 그냥 *기능 자랑*은 아니다. 모델링의 자유도가 달라지면 시스템의 아키텍처 그림도 달라진다. MongoDB를 따로 띄울지 말지, 캐시에 어떤 형태로 저장할지, ETL이 필요한지 — 이런 결정이 다른 출발선에서 시작된다.

물론 *PG에 JSONB가 있으니 MongoDB는 필요 없다*는 단순한 결론은 위험하다. GIN은 쓰기 부담이 크다. 복합 multi-key 인덱스(country + product + created_at) 같은 패턴은 MongoDB가 여전히 깔끔하다. 갱신이 매우 잦은 거대 JSONB는 GIN write overhead가 부담이 된다. 1.25M row를 넘어가는 어떤 워크로드에서는 GIN이 seq scan보다 느려진다는 보고도 있다(워크로드 의존성이 크니 확인 필요).

조금 더 실용적으로 살펴보자. JSONB로 *키-값 형태의 메타데이터*를 한 컬럼에 넣는 패턴은 PostgreSQL을 쓰는 시스템에서 가장 흔한 풍경 중 하나다. *상품 속성*, *이벤트 페이로드*, *사용자 프로필 추가 필드*, *워크플로 상태 머신의 컨텍스트* 같은 것들. 스키마가 정해지지 않거나 자주 바뀌는 영역이다. 이런 데이터를 별도 *attributes 테이블* 같은 EAV 패턴으로 풀면 join이 폭증하고 쿼리가 끔찍해진다. JSONB 한 컬럼이면 그 폭증이 사라진다. 검색이 자주 일어나는 키는 GIN 인덱스로, 한두 개 자주 쓰는 키는 expression index로 골라 가속한다.

다만 그렇다고 JSONB가 *RDB 모델링의 자리를 대신*하지는 않는다. 자주 쓰는 필드를 1급 컬럼으로 두고 *덜 정형화된 보조 필드만* JSONB에 넣는 *하이브리드 패턴*이 가장 자주 추천된다. *모든 걸 JSONB로*는 결국 *모든 걸 hash map으로*와 같은 함정이 된다. 타입 안전성·인덱스 효율·EXPLAIN 가독성을 한꺼번에 잃는다.

배열 타입도 비슷한 균형이 필요하다. *태그 다섯 개*는 배열로 자연스럽지만 *주문 항목 50개*를 한 row의 배열로 묶으면 갱신·검색·EXCLUDE 제약이 모두 어색해진다. *기수가 작고 거의 같이 다니는 묶음*에 배열을 쓰는 편이 낫다. 그 경계를 넘으면 별도 테이블이 정답이다.

이런 균형 감각은 책 한 권을 다 봐야 손에 잡히는 영역이다. 그래서 9장에서 *PG로 충분한 80%*와 *MongoDB가 여전히 유리한 20%*를 의사결정표로 정리한다. 2장에서 우리는 한 가지만 짚자 — *PostgreSQL의 데이터 타입은 RDB의 '정해진 칸'을 넘어선다.* 모델링을 시작할 때 칸 모양부터 다르다는 인식 전환이 먼저다.

## 2.5 트랜잭션 DDL이 진짜로 된다

운영 중인 DB에 컬럼을 하나 추가하고 인덱스도 하나 만들고 새 테이블도 하나 더 붙이는 마이그레이션 스크립트를 짠다고 해보자. 다섯 줄짜리 DDL이다. 중간의 어느 한 줄이 실패하면? MySQL에서는 *이미 통과한 DDL은 그대로 적용된 채로 멈춘다*. 롤백이 없다. 트랜잭션 안에 DDL을 넣어도 마찬가지다. 끔찍한 일이다. *이미 적용된 일부는 운영 상태이고, 적용 안 된 나머지는 코드 기대와 다르고, 둘이 어긋난 채로 다음 배포 사이클까지 가야 한다*는 상황이 벌어진다.

PostgreSQL에서는 대부분의 DDL이 트랜잭션 안에 들어간다. `BEGIN`으로 열고, 다섯 줄 DDL을 다 돌리고, 마지막에 `COMMIT`을 한다. 중간에 어디서 실패하면? `ROLLBACK`이 깔끔하게 도는 것처럼, 이미 통과한 DDL도 *적용 안 된 것처럼* 돌아간다. 다섯 줄을 한 단위로 처리한다.

이게 얼마나 큰 차이를 만드는가? 마이그레이션 도구를 짤 때 *각 DDL을 한 트랜잭션으로 감싸자*라는 단순한 규칙으로 운영의 안전망이 한 단계 두꺼워진다. 실패하면 깨끗하게 원상복구되고, 성공하면 한 번에 적용된다. 부분 적용이라는 *반쯤 옳은* 상태가 사라진다.

```sql
BEGIN;

ALTER TABLE orders ADD COLUMN cancelled_at TIMESTAMPTZ;
CREATE INDEX CONCURRENTLY orders_cancelled_at_idx
  ON orders (cancelled_at);  -- 이건 트랜잭션 밖에서만
ALTER TABLE order_items ADD COLUMN refund_amount NUMERIC(12,2);
CREATE TABLE refund_logs (...);

COMMIT;
```

물론 모든 DDL이 트랜잭션 안에 들어가지는 않는다. 위 예시의 `CREATE INDEX CONCURRENTLY`는 트랜잭션 밖에서 단독으로 돌아야 한다. 큰 테이블에 락 없이 인덱스를 만들기 위해 의도된 예외다. 시스템 카탈로그를 건드리는 일부 명령도 트랜잭션 안에서 동작이 달라진다. 그래도 *DDL 다섯 줄을 BEGIN-COMMIT으로 묶을 수 있다*는 기본 보장만으로도 마이그레이션의 안정성이 다른 차원이다.

여기에 PostgreSQL은 한 가지를 더 얹는다. **SAVEPOINT**다. 트랜잭션 안에서 *여기까지는 살리고, 이후만 롤백*하는 부분 롤백이 가능하다. 복잡한 마이그레이션이나 배치 처리에서 *어떤 단계는 best-effort로 시도하고 실패해도 전체는 살리고 싶다*는 패턴을 깔끔하게 표현한다.

```sql
BEGIN;
  -- 핵심 작업
  UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';

  SAVEPOINT try_notification;
    -- 실패해도 송금은 살리고 싶은 부수 작업
    INSERT INTO notifications (...) VALUES (...);
  -- 실패하면 ROLLBACK TO try_notification, 성공하면 RELEASE

  UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';
COMMIT;
```

MySQL에도 SAVEPOINT는 있다. 하지만 DDL이 트랜잭션 밖에 사실상 격리된 환경에서는 *트랜잭션의 안정성*이라는 무기가 둔하게 쓰일 수밖에 없다. PostgreSQL에서는 DDL·DML·SAVEPOINT가 모두 한 트랜잭션의 같은 안전망 안에 있다.

이 한 줄이 마이그레이션 스크립트 작성 문화를 바꾼다. *각 마이그레이션 파일은 한 트랜잭션으로 묶는다*는 규칙이 어느 PG 진영 마이그레이션 도구에서나 디폴트인 이유다. 한국의 마이그레이션 후기들에서도 *DDL이 한 단위로 묶이는 안정성*이 PostgreSQL 전환의 숨은 매력으로 자주 꼽힌다.

한 가지 더 짚어두자. 트랜잭션 DDL이 가능하다는 것과 *온라인 DDL이 자유롭다*는 것은 다른 이야기다. `ALTER TABLE ... ADD COLUMN ... DEFAULT some_value` 같은 명령은 PG 11부터 빠른 메타데이터 변경으로 처리되지만, *조건이 안 맞는 형태*의 ALTER는 여전히 ACCESS EXCLUSIVE 락을 잡고 테이블 전체를 다시 쓴다. 100GB 테이블에 그런 락이 걸리면 *읽기 한 줄도 못 하는* 시간이 한참 이어진다. 끔찍한 일이다.

PostgreSQL 운영의 관행은 *온라인 DDL을 의도적으로 설계*하는 쪽으로 굳어졌다. *컬럼 추가는 NULL 허용으로 먼저*, *기본값은 나중에 별도 트랜잭션으로 채우기*, *NOT NULL 제약은 데이터가 다 채워진 다음에*, *인덱스는 `CREATE INDEX CONCURRENTLY`로*, *외래키는 `NOT VALID`로 먼저 걸고 `VALIDATE CONSTRAINT`로 나중에 검증*. 이런 단계적 패턴이 *PG 운영자의 마이그레이션 문법*처럼 자리잡았다. *트랜잭션 DDL은 안전망이지, 무중단 보장은 아니다*라는 점을 잊지 말자.

```sql
-- 큰 테이블에 컬럼 추가, 락 최소화 패턴
ALTER TABLE big_table ADD COLUMN status TEXT;  -- 빠른 메타데이터 변경

UPDATE big_table SET status = 'pending' WHERE status IS NULL;
-- 배치로 나눠서. 한 번에 다 하면 long-running tx가 됨

ALTER TABLE big_table ALTER COLUMN status SET DEFAULT 'pending';
ALTER TABLE big_table ALTER COLUMN status SET NOT NULL;
```

표현력의 깊이는 8장에서 더 본다. 트랜잭션 DDL과 SAVEPOINT가 단지 *안전장치*가 아니라 마이그레이션·배포 *전략*의 부품으로 어떻게 쓰이는지를 거기서 풀어둔다.

## 2.6 시퀀스·IDENTITY·UUIDv7 — PK를 발급하는 세 가지 길

MySQL에서 PK 발급은 거의 한 가지 답으로 통일돼 있다. `AUTO_INCREMENT`. 컬럼에 붙이면 INSERT 때마다 자동으로 1씩 늘어난다. 단순하다. 단순한 만큼 운영의 모든 무게가 그 단순함에 기대 있다.

PostgreSQL에는 세 가지 길이 있다. 그리고 v18에서 한 가지가 더 정식으로 추가됐다.

**첫째, `SEQUENCE`.** 명시적으로 시퀀스 객체를 만들고, 컬럼의 DEFAULT로 `nextval('seq')`를 건다. 가장 오래된 방식이고 가장 유연하다. 시퀀스를 여러 테이블이 공유할 수도 있고, 시퀀스의 cache 크기·증가 폭·최댓값을 마음대로 조정할 수 있다.

```sql
CREATE SEQUENCE users_id_seq;

CREATE TABLE users (
  id    BIGINT PRIMARY KEY DEFAULT nextval('users_id_seq'),
  name  TEXT NOT NULL
);
```

**둘째, `SERIAL` / `BIGSERIAL`.** 위의 패턴을 한 단어로 축약한 옛 문법이다. `BIGSERIAL`이라고 쓰면 PostgreSQL이 알아서 시퀀스를 만들고 DEFAULT를 걸어준다. MySQL 출신에게 친숙한 *AUTO_INCREMENT스러운* 모양이다.

```sql
CREATE TABLE users (
  id    BIGSERIAL PRIMARY KEY,
  name  TEXT NOT NULL
);
```

**셋째, `GENERATED AS IDENTITY`.** SQL 표준이 정한 자동 증가 컬럼 문법이다. PG 10부터 권장 방식으로 자리잡았다. SERIAL과 거의 같은 일을 하지만 표준이라는 점이 다르고, `OVERRIDING SYSTEM VALUE` 같은 더 명시적인 제어를 제공한다. 새 시스템을 짠다면 이쪽이 무난하다.

```sql
CREATE TABLE users (
  id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  TEXT NOT NULL
);
```

여기까지가 *순차 정수 PK*의 세계다. 그런데 분산 시스템·이벤트 소싱·multi-region 같은 시나리오에서는 순차 정수가 거꾸로 짐이 되기도 한다. 시퀀스 발급을 위한 round-trip이 필요하고, 분산 환경에서 충돌 없이 발급하기 위한 추가 인프라(snowflake, sonyflake 등)가 필요하다. 그래서 **UUID**가 자주 등장한다.

여기서 PostgreSQL v18의 새 카드가 등장한다. **UUIDv7이 내장됐다.** 기존 UUIDv4는 완전 랜덤이라 인덱스에 친화적이지 않다. INSERT가 B-tree의 무작위 위치에 들어가 페이지 분할이 잦아지고, 인덱스 캐시 효율도 떨어진다. UUIDv7은 *상위 비트에 시간 정보, 하위 비트에 랜덤*이라는 구조다. 시간순으로 *대략 정렬된* 채로 INSERT되므로 B-tree 친화적이다. 분산 환경의 충돌 회피와 인덱스 친화성을 동시에 잡는다.

```sql
-- v18 내장 UUIDv7
CREATE TABLE events (
  id         UUID PRIMARY KEY DEFAULT uuidv7(),
  payload    JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

MySQL에서 PK 결정을 *AUTO_INCREMENT인가 아닌가*의 이분법으로 해왔다면, PostgreSQL에서는 *순차 정수가 맞는 시스템인가, UUID가 맞는 시스템인가, UUID라면 v4인가 v7인가*라는 세 갈래 질문으로 바뀐다. 시스템의 분산 정도, 인덱스 설계, multi-region 여부에 따라 답이 달라진다.

한 가지 주의해두자. 시퀀스는 트랜잭션의 ACID 보장 밖에 있다. `nextval`이 발급한 값은 트랜잭션이 ROLLBACK돼도 *돌려놓지 않는다*. 1, 2, 3이 발급된 뒤 트랜잭션 두 개가 롤백되면 다음에 발급되는 값은 4가 아니라 6이다. 시퀀스 값에 *빈 칸이 있어도 정상*이라는 점, 머리에 박아두자. 이걸 *결번이 있으면 안 된다*는 비즈니스 규칙으로 잘못 묶으면 마이그레이션도 운영도 끔찍해진다.

MySQL `AUTO_INCREMENT`도 사실 같은 특성을 갖지만, MySQL의 일부 구버전·설정에서는 *gap을 메우는 방향*의 동작이 가능했다. *MySQL과 결과적으로 같은 모양인데 어떤 엣지 케이스에서는 다르게 동작한다*는 영역이 늘 그렇듯, 이 부분도 마이그레이션 직후 영수증 번호·계약 번호·송장 번호 같은 *결번 민감한 도메인*에서 종종 사고로 이어진다. *번호 발급은 시퀀스 위에 별도 보장을 한 겹 더 얹는다*는 설계 원칙이 PostgreSQL에서는 더 자연스럽다. 영수증 번호가 정말 연속이어야 한다면 별도 테이블에 카운터를 두고 `SELECT FOR UPDATE`로 직렬화하는 식의 패턴이 더 안전하다.

발급 전략의 깊은 설계는 시스템 아키텍처 영역이라 이 책에서 한 챕터로 따로 다루지는 않는다. 다만 17장 마이그레이션 챕터에서 *MySQL `AUTO_INCREMENT`를 PostgreSQL의 어떤 길로 매핑할지*의 의사결정 표를 만난다. 우리는 여기서 한 줄을 가져가자 — *PG의 PK 발급은 한 가지 답이 아니라, 시스템의 모양에 맞춰 고르는 답이다.*

## 2.7 LIMIT·timezone·SQL 표준 — 마이그레이션의 첫 신호

마이그레이션을 실제로 해본 사람들이 한입 모아 말하는 한 가지가 있다. *DDL 변환은 쉽다. semantics 변환이 어렵다.* 이 말의 가장 빠른 증거가 LIMIT과 timezone이다.

MySQL의 LIMIT는 표준에서 살짝 비켜선 자체 확장이다. 가장 흔히 쓰는 `LIMIT n` 자체는 같지만, 그 옆에 붙는 변종들이 다르다. `LIMIT offset, count` 같은 형식, OFFSET을 LIMIT 안에 넣는 문법, 서브쿼리나 UPDATE/DELETE에 LIMIT을 자유롭게 붙이는 관행, 이런 것들이 MySQL 코드 베이스에 자연스럽게 깔려 있다.

PostgreSQL은 SQL 표준을 충실히 따른다. `LIMIT n OFFSET m` 또는 `OFFSET m FETCH FIRST n ROWS ONLY`. MySQL 스타일의 `LIMIT m, n`은 받지 않는다. 게다가 PostgreSQL에서는 UPDATE/DELETE에 직접 LIMIT을 붙일 수 없다 — *어떤 row를 먼저 지울지*가 표준 SQL에서 모호하기 때문이다. 우회하려면 서브쿼리·CTE로 PK를 골라 IN 조건으로 받는 패턴을 써야 한다.

이 한 가지 차이가 마이그레이션에서 어떤 모습으로 나타날까? 한국 velog 후기 중 하나는 *LIMIT 절을 모두 수정했다*고 짧게 적었다. *모두*라는 한 단어가 의미하는 부피를 짐작해보자. 수백 개의 쿼리, 수십 개의 마이그레이션 스크립트, 운영 도구 코드까지. DDL 변환만 보던 사람에게는 깜짝 놀랄 양의 일이다.

timezone은 더 음흉하다. MySQL의 `DATETIME`은 timezone 정보가 없다. 그냥 *어떤 시각의 숫자*다. timezone은 세션 변수에 따라 표시·해석이 달라진다. PostgreSQL에는 두 가지 타입이 있다. `TIMESTAMP WITHOUT TIME ZONE`과 `TIMESTAMP WITH TIME ZONE`(약칭 `TIMESTAMPTZ`). 둘은 *전혀 다른 의미*다.

`TIMESTAMPTZ`는 입력 시점의 timezone 정보를 받아 UTC로 정규화해서 저장하고, 조회 시 세션 timezone에 맞춰 변환해서 돌려준다. *그 순간 지구 어느 곳에서 일어난 사건의 절대 시각*을 다룬다. `TIMESTAMP WITHOUT TIME ZONE`은 그저 *연·월·일·시·분·초*의 묶음이다. *어떤 시계의 표시값*을 다룬다. 이 둘 사이의 캐스트, 비교, 집계는 미묘하게 다른 결과를 낸다.

MySQL의 `DATETIME`을 어느 쪽으로 매핑할지는 데이터의 *의미*가 결정한다. 사용자 가입 시각이라면 `TIMESTAMPTZ`가 자연스럽다. 예약 시간(*매주 화요일 오전 10시* 같은 *벽시계 시각*)이라면 `TIMESTAMP WITHOUT TIME ZONE`이 맞을 수 있다. 이 매핑을 잘못하면 어떻게 될까? 같은 후기에서 *47개 쿼리가 timezone 차이로 깨졌다*는 보고가 나온다. 47개라는 숫자가 어떤 풍경인지는 17장에서 다시 만나자.

그 외에도 SQL 표준에서 살짝씩 빗나간 MySQL의 관행이 몇 가지 더 있다.

- **암묵적 캐스트.** MySQL은 `WHERE varchar_col = 123` 같은 조건도 친절하게 해석해준다. PostgreSQL은 타입 안전성을 더 엄격하게 본다. 인덱스가 죽거나 에러가 나거나 둘 중 하나다.
- **`GROUP BY`의 SELECT 컬럼 자유도.** MySQL은 GROUP BY에 없는 컬럼을 SELECT에서 그대로 받는다(과거 기본값). PostgreSQL은 표준대로 *집계 함수 또는 GROUP BY 컬럼*만 받는다.
- **`NULL` 처리의 미묘함.** MySQL의 `IFNULL`, PostgreSQL의 `COALESCE` 같은 함수 이름 차이부터, NULL을 포함한 비교의 결과 처리 관행까지.
- **백틱 vs 큰따옴표.** MySQL은 식별자에 백틱(`` ` ``)을 쓴다. PostgreSQL은 SQL 표준대로 큰따옴표(`"`)를 쓴다. 그리고 PostgreSQL에서 큰따옴표로 감싼 식별자는 *대소문자가 보존*된다. `"UserName"`은 `username`과 다른 이름이다.

이 모든 것이 *DDL이 아니라 semantics*다. CREATE TABLE 한 줄을 옮기는 일은 도구로 자동화할 수 있다. 그런데 `WHERE created_at >= ...` 한 줄이 timezone 차이로 다른 row를 돌려주는 일은 자동화로 못 잡는다. 사람이 한 줄씩 의미를 다시 본다.

한 가지 더 음흉한 게 있다. **NULL 정렬 순서**다. MySQL은 ORDER BY에서 NULL을 *작은 값*으로 본다. ASC면 맨 앞, DESC면 맨 뒤. PostgreSQL은 표준대로 NULL을 *큰 값*으로 본다. ASC면 맨 뒤, DESC면 맨 앞. 같은 `ORDER BY updated_at DESC LIMIT 10`이 두 DB에서 *다른 10개*를 돌려줄 수 있다. 페이지 매김에서 *어제까지 본 마지막 항목*과 *오늘 새로 보이는 첫 항목*이 일치하지 않는 식의 미묘한 사고로 이어진다. 명시적으로 `NULLS FIRST`나 `NULLS LAST`를 붙여 정렬 순서를 강제하는 편이 안전하다.

여기에 **DECODE / (+) 외부조인 / CONNECT BY** 같은 Oracle 계열 문법까지 끼면 마이그레이션의 풍경은 더 복잡해진다. MySQL은 이런 문법을 처음부터 안 받지만, Oracle에서 직접 PostgreSQL로 가는 시스템에서는 *DDL 변환은 끝났는데 쿼리 한 줄 한 줄이 다른 모양으로 다시 써져야 하는* 영역이 생긴다. `DECODE`는 `CASE`로, `(+)` 외부조인은 `LEFT JOIN`으로, `CONNECT BY` 계층 쿼리는 `WITH RECURSIVE` CTE로 — 변환 규칙 자체는 분명한데 *모든 쿼리에 손이 가야 한다*는 양적인 부담이 진짜 비용이다.

마이그레이션 도구가 이 변환의 일부를 도와준다. `pgloader`는 MySQL → PG 자동화의 사실상 표준이고, `ora2pg`는 Oracle → PG 진영의 표준이다. AWS DMS·SCT도 같은 영역에서 일한다. 그런데 이 도구들이 *DDL과 데이터 이관은 잘 해주지만 SQL semantics 변환은 결국 사람의 일*이라는 한계가 분명하다. 자동화가 가져다 주는 것은 *전체 일의 30~50%*, 나머지는 application 코드와 쿼리를 한 줄씩 다시 보는 사람의 노동이다.

마이그레이션의 두 번째 음흉함은 *테스트 환경과 운영 환경의 격차*다. 테스트 DB에서 100GB로 검증한 마이그레이션이 운영 4TB에서는 *전혀 다른 시간 곡선*을 그린다. 인덱스 빌드 시간, vacuum 회수 시간, 통계 수집 시간이 모두 비선형으로 늘어난다. *우리는 테스트에서 30분 걸렸으니 운영에서도 비슷할 거야* 같은 직관은 자주 무너진다. *작은 데이터로 검증된 절차*와 *운영 데이터에서 검증된 절차*는 다른 절차다.

다시 한 번 약속하자. 이 절은 *신호*만 보여준다. 실전 비용 — 4억 row, 다운타임 18시간, 발견된 버그 127개, 47개 깨진 쿼리, dual-write로 3개월 운영, 어떤 쿼리를 어떻게 고쳤는지의 세부 — 는 17장의 마이그레이션 챕터에서 깊이 다룬다. 지금은 *어디서 신호가 켜지는지*만 잡아두자. 그래야 이 책의 17장이 어떤 챕터가 될지 미리 보인다.

## 2.8 확장성 — extension은 사이드 카가 아니라 코어

마지막 차이는 사실 *차이*라기보다 *세계관*에 가깝다. PostgreSQL을 다른 RDBMS와 구분짓는 단 한 가지를 고르라면, MVCC도 트랜잭션 DDL도 아닌 *익스텐션 시스템*이다.

MySQL에도 플러그인이 있다. 스토리지 엔진 플러그인, 인증 플러그인 등. 그런데 그 자리는 코어 옆의 *사이드 카* 정도다. 무엇을 새로 만들 수 있는지의 범위가 좁다.

PostgreSQL의 익스텐션은 다른 무게를 가진다. `CREATE EXTENSION` 한 줄로 새 데이터 타입, 새 인덱스 접근 방식, 새 함수, 새 트리거, 새 시스템 카탈로그까지 추가할 수 있다. 그래서 PostgreSQL 위에 거의 *별도의 DB 같은* 시스템들이 익스텐션 형태로 올라간다. 몇 개만 짚어보자.

**PostGIS.** 공간 데이터의 표준이다. `GEOMETRY`와 `GEOGRAPHY` 타입을 데이터 타입 시스템에 새로 등록하고, ST_* 함수군을 수백 개 추가하고, GiST·SP-GiST 공간 인덱스를 인덱스 시스템에 꽂는다. PostgreSQL을 GIS 데이터베이스로 *바꾼다*. State Farm의 재난 클레임 처리, NIBIO의 노르웨이 전국 토지 토폴로지, Telkom Kenya의 영업 영역 추적 같은 production 시스템이 PostGIS 위에서 돌아간다.

**pgvector / pgvectorscale.** 벡터 임베딩을 위한 데이터 타입과 인덱스(HNSW, IVFFlat, DiskANN)를 추가한다. RAG 시스템의 백엔드를 PostgreSQL이 맡을 수 있게 만든다. pgvectorscale 기준으로 50M 벡터·99% recall에서 Qdrant 대비 11.4배 QPS, Pinecone 대비 75% 비용 절감이라는 측정치가 보고된다(워크로드 의존성은 늘 따져봐야 한다).

**Citus.** PostgreSQL을 분산 DB로 만든다. hash partition으로 데이터를 노드에 분산하고, co-located join을 자동 라우팅한다. Microsoft에 인수된 후에도 OSS로 유지된다.

**TimescaleDB.** 시계열을 위한 hypertable, continuous aggregate, native columnstore. *시계열 전용 DB로 따로 가야 하나?*의 답을 PostgreSQL 안에 둔다.

**PGroonga.** 한국어·일본어·중국어 zero-ETL 전문 검색. Supabase에 공식 익스텐션으로 포함돼 있다. *Elasticsearch를 또 하나 세워야 하나?*의 답을 PostgreSQL 안에 둘 수 있게 한다.

**pg_partman.** declarative partitioning의 자동 운영을 맡는다. 시간 기반 파티션의 생성·삭제를 BGW로 자동화한다.

**pg_cron.** PostgreSQL 안에 cron job 같은 스케줄링을 넣는다. ETL·정기 청소·리포트 생성을 *외부 스케줄러 없이* 한다.

**PostgREST / pg_graphql.** 스키마에서 REST/GraphQL API를 자동으로 띄운다. *DB가 백엔드*라는 패턴을 가능하게 한다.

**pgaudit.** 감사 로그를 자세하게 남긴다. *어느 사용자가 어느 시각에 어느 쿼리를 돌렸는지*의 추적 가능성을 확보한다. 보안·컴플라이언스 시나리오의 필수에 가깝다.

이 목록은 *대표 몇 개*에 불과하다. PostgreSQL 익스텐션 카탈로그는 수백 개가 넘는다. 새 데이터 도메인이 나타날 때마다 *코어를 바꿀 필요 없이* 익스텐션으로 들어온다.

이게 왜 *세계관*인가? 시스템을 설계할 때 *추가되는 데이터 도메인마다 새 DB를 띄울 것인가, 같은 PostgreSQL에 익스텐션으로 얹을 것인가*라는 질문이 매번 생기기 때문이다. 검색이 필요해졌다? Elasticsearch를 띄울 수도 있지만 PGroonga나 pg_search를 얹는 길도 있다. 지리 데이터가 들어왔다? 전용 GIS DB가 아니라 PostGIS다. RAG를 시작했다? Pinecone·Qdrant·Weaviate가 아니라 pgvector(+scale)도 후보다.

물론 *모든 걸 PostgreSQL 하나로*는 그 자체로 함정이 될 수 있다. Vonng의 *"Postgres is eating the database world"*가 흥미로운 주장이지만 그 안의 함정도 분명하다. Kafka 수준의 100MB/s+ 메시지 throughput, Elasticsearch 수준의 한국어 검색 품질, ClickHouse 수준의 순수 컬럼 분석 성능 — 이런 극단의 워크로드에서는 dedicated 시스템이 여전히 유리하다. *PG로 가도 되는 선*과 *dedicated가 필요한 선*을 매번 정직하게 그어야 한다.

그 선을 어디에 그을지의 의사결정을 책의 Part 3 전체(8~16장)가 9가지 시나리오로 풀어둔다. 9장 JSON·문서 DB, 10장 전문 검색, 11장 GIS, 12장 벡터·RAG, 13장 이벤트·큐, 14장 FDW·CDC, 15장 OLAP·시계열, 16장 API 백엔드. 각 장의 끝에 *PG로 가도 되는 선*과 *dedicated가 필요한 선*을 명확히 그어둔다.

여기에 한 가지 운영 측면을 미리 짚어두자. *익스텐션이 코어*라는 말의 그림자는 *매니지드 PG의 익스텐션 지원 목록이 결정적 변수*가 된다는 점이다. RDS·Aurora·Cloud SQL·AlloyDB·Supabase·Neon·Crunchy·Tembo가 각자 다른 익스텐션 셋을 지원한다. *PostGIS는 거의 다 되지만 PGroonga는 한정적*, *pg_search는 일부 매니지드만*, *pgvectorscale은 Tiger Data의 매니지드 위주*, *pg_cron은 RDS에서 일부 제약*. 평가 단계에서 *우리가 쓸 익스텐션 목록*을 만들고 *각 매니지드 PG의 지원 매트릭스*를 그어보지 않으면, 이관 D-1일에 *우리가 쓸 익스텐션 하나가 지원 안 됨* 같은 끔찍한 발견이 나온다.

또 한 가지 — *익스텐션은 코어 변경 없이 들어온다*는 표현의 그늘이다. 익스텐션 자체의 코드 품질·릴리스 주기·CVE 대응이 익스텐션마다 다르다. 잘 관리되는 익스텐션(PostGIS, pgvector, pg_partman 같은 메이저)이 있는가 하면, 1인 개발자가 산발적으로 업데이트하는 익스텐션도 있다. *PostgreSQL 메이저 버전 업그레이드를 했더니 어떤 익스텐션이 새 버전을 아직 안 냈다*는 식의 막힘은 흔한 풍경이다. 그래서 익스텐션을 고를 때도 *메인테이너 활동성·릴리스 주기·매니지드 PG의 채택 여부* 같은 지표를 같이 본다.

여기서 우리는 한 가지를 잡아 가자 — *PostgreSQL의 익스텐션은 옵션이 아니라 정체성이다.* 그래서 매니지드 PG를 고를 때도 *어떤 익스텐션을 지원하는가*가 사실상의 결정 기준이 된다. 이건 24장 클라우드 챕터에서 다시 만난다.

## 2.9 여덟 가지 차이가 만드는 사고방식의 전환

여기까지 여덟 군데를 짚었다. 다시 한 줄씩 모아보자.

1. **동시성 모델.** thread-per-connection이 아니라 fork. 풀러가 필수다.
2. **MVCC 저장 방식.** undo log가 아니라 append-only. VACUUM이 운명처럼 따라온다.
3. **클러스터 인덱스의 부재.** PK도 별도 인덱스. HOT가 비용을 깎는다.
4. **데이터 타입 표현력.** 배열·범위·JSONB·hstore. 모델링의 첫 칸이 다르다.
5. **트랜잭션 DDL.** BEGIN-COMMIT 안에 DDL이 들어온다. 마이그레이션의 안전망이 한 층 두꺼워진다.
6. **PK 발급.** AUTO_INCREMENT 하나가 아니라 SEQUENCE·IDENTITY·UUIDv7의 세 갈래.
7. **LIMIT·timezone·SQL 표준.** semantics 차이가 마이그레이션의 진짜 무게다.
8. **확장성.** 익스텐션이 옵션이 아니라 코어. 시스템 그림 자체를 바꾼다.

여덟 가지를 따로따로 보면 *각각의 차이* 같다. 그런데 한자리에 놓고 보면 그 위에 한 가지 *사고방식*이 떠오른다.

MySQL을 쓸 때의 사고방식은 대개 *단순함과 처리량*에 무게가 있다. *DB는 데이터를 빠르게 받고 빠르게 돌려주는 단순한 도구*라는 그림. AUTO_INCREMENT 하나, 클러스터 인덱스 하나, undo log 하나, 표준에서 살짝 벗어난 편의 문법들. 운영 부담이 적고 학습 곡선이 완만하다. 그래서 작은 팀, 빠른 출시, 예측 가능한 OLTP에 어울린다.

PostgreSQL을 쓸 때의 사고방식은 *정확성과 표현력*에 무게가 옮겨간다. *DB는 데이터를 표현하고 보장하는 도구*라는 그림. 데이터 타입을 정밀하게 고르고, MVCC와 vacuum의 운영 비용을 받아들이고, 트랜잭션 DDL의 안전망을 깔고, 익스텐션으로 데이터 도메인을 흡수한다. 복잡한 쿼리, 혼합 워크로드, 강한 정합성, 풍부한 모델링이 필요한 시스템에 어울린다.

어느 한쪽이 *절대로* 옳다는 말이 아니다. 두 시스템은 다른 사고방식 위에 서 있고, 그래서 각자가 잘 하는 일이 다르다. *대부분 워크로드에서 성능 차이는 ±30% 이내*라는 합의가 커뮤니티에 있다. 진짜 선택의 축은 성능이 아니라 *데이터 타입 표현력 + 익스텐션 생태계*와 *운영 단순성* 사이다.

그렇다면 MySQL 베테랑이 PostgreSQL로 옮길 때 진짜 해야 할 일은 무엇인가? 문법을 외우는 일이 아니다. 도구를 익히는 일도 아니다. *사고방식을 한 단계 다시 그려넣는 일*이다. *내가 알고 있다고 생각한 한 줄*이 다른 동사 위에 서 있다는 사실을 인정하고, 그 새 동사를 손에 익히는 일.

이 사고방식의 전환에서 가장 흔한 두 가지 함정이 있다. 잠깐 짚어두자.

**첫 번째 함정 — MySQL의 직관을 그대로 옮기는 것.** *VACUUM이 알아서 돌겠지*, *max_connections 그냥 2000으로*, *DATETIME을 TIMESTAMP로 바꾸면 끝*, *AUTO_INCREMENT는 SERIAL로 바꾸면 같은 거지*. 이런 1:1 매핑이 가장 위험하다. 같은 모양 아래의 다른 동사가 한 달 뒤, 6개월 뒤에 사고로 돌아온다.

**두 번째 함정 — PostgreSQL의 풍부함을 다 쓰려는 것.** *배열도 쓰자, JSONB도 쓰자, 익스텐션 다 깔자, RLS로 멀티테넌트 설계도, 시퀀스 대신 UUIDv7으로, 분석은 pg_duckdb로*. 풍부함을 쓰는 일에도 비용이 있다. 처음 옮길 때는 *PostgreSQL의 기본기*만 단단히 잡고, 풍부한 기능은 한 번에 하나씩 들이는 편이 낫다.

두 함정 사이의 좁은 길이 *PG에 맞는 사고방식*이다. 그 길은 한 권의 책으로 정확히 따라갈 수 있다. 그래서 이 책의 나머지가 있다.

기억해두자. 이 여덟 가지는 *외울 항목*이 아니라 *책을 읽는 지도*다. 운영 중에 어떤 증상이 나타날 때마다 이 지도의 어느 좌표에 해당하는지를 떠올릴 수 있다면, 그 다음의 진단과 처방은 책의 해당 챕터로 가는 길이 자연스럽게 보인다. *느린 쿼리가 안 풀린다*면 5장의 MVCC와 6장의 HOT, 23장의 EXPLAIN을. *야간에 클러스터가 read-only가 됐다*면 18장의 wraparound를. *마이그레이션 직전에 무엇을 챙길지 모르겠다*면 17장 전체를. *매니지드 PG를 어떻게 고를지 막막하다*면 24장을. *보안 감사를 어떻게 받을지 떨린다*면 22장을. 지도를 들고 가면 길을 잃지 않는다.

마지막으로 한 가지만 더. 이 장에서 짚은 여덟 가지가 *PG의 단점 목록*처럼 읽혔다면 균형을 잡아둘 필요가 있다. fork 모델, append-only MVCC, 트랜잭션 DDL, 풍부한 데이터 타입, 익스텐션 — 이 모두는 *비용*인 동시에 *능력*이다. 비용만 보면 부담스럽고, 능력만 보면 환상적으로 보인다. 둘 다 정직하게 인정하는 시각이 *베테랑*의 시각이다. 그래서 이 장은 *어느 한쪽으로 결론짓지 않는* 채로 마친다. 그 결론은 책을 다 읽은 독자가 자기 시스템 앞에서 스스로 내릴 일이다.

다음 장에서 우리는 또 한 번 멈춘다. *그래서, 최신 버전에서는 무엇이 달라졌는가?* PostgreSQL 17과 18에서 vacuum 메모리 재작성, failover slot, JSON_TABLE, RETURNING OLD/NEW, temporal constraint, UUIDv7, planner statistics 보존 같은 굵직한 진화가 있었다. *운영 중인 시스템을 멈춰서까지 올릴 만한가*의 판단 기준을 거기서 같이 세워보자.

지도를 한 번 다 본 셈이다. 이 지도를 손에 들고 책 안으로 더 깊이 들어가자.
