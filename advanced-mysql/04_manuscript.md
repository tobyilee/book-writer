# DBA처럼 생각하는 스프링 개발자

> MySQL 8.x를 다루는 13가지 관점

**저자:** Toby-AI
**판본:** v1.0.0 · 2026-05-18

---

## 머리말

이 책은 한 가지 풍경에서 시작됐다. 자바 스프링 개발자가 늘어났고, JPA가 SQL을 가려주는 추상의 두께도 두꺼워졌다. 그런데 운영하던 서비스가 어느 정도 자라면 그 두께 너머에서 신호가 올라오기 시작한다. 새벽 두 시의 데드락 알람, 갑자기 10초가 된 결제 목록 쿼리, "Aurora로 옮기자"는 회의의 막연함. 우리는 그 신호 앞에서 시니어를 부르거나, 일단 인덱스를 추가해보거나, 재시도 로직으로 덮어두는 일을 반복한다.

DBA가 되라는 책이 아니다. DBA라는 직업은 따로 있고, 그 책임은 그 사람들에게 맡기는 것이 옳다. 다만 우리도 데이터베이스 앞에 섰을 때 무엇을 물어야 하는지, 어떤 그림을 떠올려야 하는지를 알 필요는 있다. 그것이 이 책이 가려는 자리다 — **DBA처럼 생각하는 스프링 개발자**.

이 책은 다음 네 가지에 시간을 들였다. 첫째, InnoDB라는 엔진의 멘탈 모델. 버퍼풀과 redo 로그, MVCC와 B+Tree가 어떻게 한 그림으로 연결되는지. 둘째, EXPLAIN ANALYZE를 안에서 바깥으로 읽는 절차. 슬로우 쿼리를 받아들고 혼자 분해할 수 있는 손. 셋째, JPA가 만들어주는 편안함과 그 이면의 실제 SQL 사이의 간극. 넷째, RDS와 Aurora, 백업과 DR, 메이저 업그레이드 같은 운영의 의사결정.

각 챕터는 가능한 한 독립적으로 읽을 수 있도록 만들었지만, 1장부터 순서대로 읽었을 때 가장 자연스럽게 맥이 흐른다. 특히 2·3·4장은 책의 뼈대다. 뒤의 모든 장이 이 세 장의 그림 위에서 이야기된다. 경험이 있는 독자라면 서장과 1장을 훑은 뒤 자기 관심사부터 펴 봐도 좋다. JPA가 시급하다면 9·10장으로, 운영이 급하다면 11·12장으로.

이 책은 인용으로 가득하다. 우아한형제들, 토스, LINE, 카카오 같은 한국 엔지니어들이 공개한 경험과, Vlad Mihalcea·Thorben Janssen·Skeema·Percona 같은 글로벌 커뮤니티의 깊이 있는 글들이 본문 곳곳에 녹아 있다. 어느 한 사람의 직관이 아니라 여러 사람의 경험이 만든 합의가 이 책의 단단함이다. 각 챕터 끝의 참고 자료가 그 출처다.

마지막으로 한 가지. 이 책에 적힌 내용은 검증을 거쳤지만 모든 환경에서 같은 결과를 보장하지는 않는다. AWS의 가격, MySQL 9.x의 새 기능, 8.4의 미세한 동작은 시간이 흐르면 변한다. 본문의 수치와 결론은 우리 환경에서 한 번 확인하고 받아들이는 편이 낫다. 책을 따라 EXPLAIN ANALYZE를 한 줄씩 같이 읽는 자세가 이 책을 가장 잘 쓰는 방법이다.

자, 책장을 넘기자.

— Toby-AI, 2026년 봄

---

## 차례

- **서장.** ORM 뒤에 숨어 살던 우리에게
- **1장.** MySQL 8.x가 바꾼 풍경 — 이 책이 *지금* 출간되는 이유
- **2장.** InnoDB라는 엔진을 그림으로 이해하자
- **3장.** 트랜잭션, 격리수준, 그리고 락의 메커니즘
- **4장.** 인덱스 설계는 데이터 구조 설계다
- **5장.** EXPLAIN ANALYZE를 안에서 바깥으로 읽기
- **6장.** SQL의 표현력을 다시 끌어올리자 — 윈도우와 CTE
- **7장.** JSON 데이터 모델링과 인덱싱
- **8장.** 도메인 모델링과 스키마 설계의 만남
- **9장.** JPA로 MySQL 다루기 — 영속성 기본기와 함정
- **10장.** JPA를 넘어 — 성능·동시성·락 패턴·배치
- **11장.** AWS RDS와 Aurora — 인스턴스 선택·복제·분할의 분기점
- **12장.** 운영의 눈 — 관측, 보안, 백업·복구·DR
- **13장.** 통합 사례 — 결제 시스템 한 건을 끝까지 분해해 보자
- **14장.** 업그레이드와 그다음 — 메이저 버전을 넘는 법
- **종장.** 책을 덮으며

---


# 서장. ORM 뒤에 숨어 살던 우리에게

월요일 새벽 두 시, 슬랙 알림이 울렸다고 해보자. "결제 페이지가 안 열려요." 개발자는 반쯤 감긴 눈으로 노트북을 열고 애플리케이션 로그를 뒤진다. 예외 스택 트레이스엔 낯선 메시지가 적혀 있다. `Deadlock found when trying to get lock; try restarting transaction`. 난감하다. 데드락이 뭔지는 안다. 그런데 어디서 터진 건지, 왜 터진 건지, 어떻게 고쳐야 하는지는 모른다. 결국 트랜잭션 범위를 줄이고 재시도 로직을 붙여두는 것으로 그 날을 넘긴다. 찜찜한 채로.

이 장면이 낯설지 않다면, 이 책이 가려는 곳이 우리가 가려는 곳과 같다.

## JPA가 준 선물, 그리고 그 대가

스프링 생태계는 자바 개발자에게 놀라운 선물을 안겨줬다. JPA, 그중에서도 Hibernate. 엔티티 클래스에 어노테이션 몇 줄만 얹으면 테이블이 만들어지고, `save()`와 `findById()` 몇 번이면 데이터가 오간다. SQL을 직접 쓰지 않아도 CRUD가 돌아간다.

그 결과, 많은 스프링 개발자가 MySQL을 "JPA 아래에 있는 무언가"로 인식하기 시작했다. 자세히 알 필요가 없는, 그냥 거기 있어 주면 되는 것. `spring.datasource.url`에 주소 하나 넣고 `ddl-auto: update` 줄 하나 쓰면 동작하는 블랙박스.

이 추상화는 놀랍도록 강력하다. 생산성이 올라가고, 개발 속도가 빨라진다. 그런데 그 편안함에는 대가가 따른다. 서비스가 커지면, 트래픽이 늘면, 이 블랙박스 안에서 무슨 일이 벌어지는지 알아야 할 순간이 반드시 온다.

슬로우 쿼리 알람이 그 첫 신호다. `slow_query_log`에 쌓이는 쿼리들. `EXPLAIN`을 처음 열어봤을 때의 그 막막함. `type: ALL`, 즉 풀 테이블 스캔이라는 두 글자. 인덱스를 어디다 어떻게 걸어야 하는지, 왜 그 인덱스가 안 쓰이는지, 어떤 인덱스를 추가하면 더 나빠지는지 — 아무도 가르쳐주지 않은 것들이 현실로 밀려든다.

그다음은 격리수준이다. `Repeatable Read`와 `Read Committed` 중 무엇을 써야 하는가. 갭 락이 왜 생기는지, 넥스트키 락이 무엇인지, 어떤 상황에서 데드락이 발생하고 어떻게 읽는지. "Aurora로 옮기자"는 회의실 말은 들었는데, RDS와 Aurora의 차이가 뭔지, 어떤 기준으로 선택해야 하는지는 모호하다.

이 모든 것들이, JPA라는 추상화가 감춰두었던 MySQL이라는 실체다.

## 이 책의 약속

이 책은 우리에게 DBA가 되라고 말하지 않는다. DBA는 다른 직업이고, 다른 기술 스택이고, 다른 책임이다. 이 책이 원하는 것은 딱 하나다. **DBA처럼 생각하는 스프링 개발자**가 되는 것.

차이가 있다. DBA처럼 생각한다는 건, 데이터베이스 앞에 섰을 때 무엇을 물어야 하는지 아는 것이다. `EXPLAIN ANALYZE` 트리를 안에서 바깥으로 읽어낼 수 있는 것, 데드락 로그를 받아들고 어느 트랜잭션이 어느 락에 걸렸는지 5분 안에 짚어낼 수 있는 것, RDS와 Aurora 사이에서 우리 워크로드 기준으로 어느 쪽이 더 맞는지 설명할 수 있는 것.

**DBA처럼 생각하는 스프링 개발자**, 그것이 우리가 도달하려는 자리다.

## 우리가 걸어갈 길

여기서 잠깐, 우리가 어디에서 출발해 어디로 가는지를 한 번 짚어두자. 책을 펴 들고 있는 우리 모습이 이런 것 아닐까. 평소엔 IntelliJ에서 엔티티 클래스를 만들고 `@OneToMany`, `@ManyToOne` 같은 어노테이션을 붙이고, `JpaRepository`를 상속받아 `findByUserId` 같은 메서드 시그니처 하나로 쿼리를 만들어내는 일상. CRUD는 익숙하고, 단순한 JOIN도 어색하지 않다. 그런데 슬로우 쿼리 알람이 오면 일단 인덱스부터 추가해보고, 안 되면 옆자리 시니어에게 물어본다. `EXPLAIN`을 열어봐도 출력이 무슨 뜻인지 정확히는 모른다. `type`, `key`, `rows`, `Extra` 컬럼이 다 무슨 말을 하는 건지 어렴풋하다. `Repeatable Read`와 `Read Committed` 중 무엇을 쓰는지 물어보면 "기본값 그대로요"라고 답한다. Aurora로 옮기자는 회의가 잡혀도, 왜 옮기는지보다 옮기고 나서 뭐가 달라지는지가 더 궁금하다. 백업이 잘 되고 있다는 건 알지만, 어떻게 복구하는지는 한 번도 직접 해본 적이 없다 — 이 정도가 출발점일 것이다. 이 책의 마지막 페이지를 덮을 때, 그 풍경이 어떻게 달라져 있어야 하는가. `EXPLAIN ANALYZE`의 트리를 안에서 바깥으로 읽어내고, 데드락 로그가 떠도 5분 안에 어느 락이 어디서 부딪쳤는지 짚어내고, RDS와 Aurora 사이 분기점을 우리 워크로드 기준으로 설명할 수 있다. JPA와 native SQL 사이 경계를 내 손으로 그을 줄 알고, 분기마다 백업·PITR 리허설을 돌릴 수 있다. 메이저 업그레이드 일정이 떨어져도 무엇부터 점검할지 안다. 그 거리만큼이 이 책이 함께 걸어갈 길이다.

## 13개 챕터의 지도

책은 크게 다섯 묶음으로 흐른다.

1장은 지금 시점을 정당화한다. MySQL 8.x, 특히 8.4 LTS가 가져온 변화를 짚는다. 새 버전이 나왔다고 책을 쓰는 게 아니라, 8.0과 8.4의 변화들이 스프링 개발자의 일상을 실제로 어떻게 흔드는지 보여준다.

2·3·4장은 기반을 쌓는다. 2장은 InnoDB 내부 — 버퍼풀, redo 로그, MVCC, B+Tree. 3장은 그 위에 얹힌 트랜잭션과 격리수준, 그리고 락의 메커니즘. 4장은 인덱스 설계. 이 세 장이 책의 뼈대다. 뒤의 모든 장은 이 세 장의 그림 위에서 이야기된다.

5·6·7장은 읽고 다듬는 기술을 쌓는다. 5장에서 `EXPLAIN ANALYZE`로 쿼리를 분해하는 법을, 6장과 7장에서 윈도우 함수·CTE·JSON 인덱싱으로 SQL 표현력을 끌어올리는 법을 다룬다.

8·9·10장은 스프링과의 접점에서 가장 많은 시간을 보낸다. 8장은 도메인 모델링과 스키마 설계의 만남. 9장과 10장은 JPA — 기본기와 함정, 그리고 성능·동시성·락 패턴.

11·12·13장은 운영의 세계로 들어간다. 11장은 RDS와 Aurora 선택, 복제, 파티셔닝. 12장은 관측, 보안, 백업과 DR. 13장은 지금까지 쌓은 것들을 결제 시스템 한 건에 끝까지 적용해보는 통합 사례. 14장과 종장은 메이저 업그레이드와 다음 걸음이다.

읽는 순서에 대해 한 마디 하자. 이 책은 1장부터 순서대로 읽게 설계되어 있다. 특히 2·3·4장은 건너뛰면 뒤에서 반드시 막힌다. 다만 경험이 있는 독자라면 서장을 읽고 1장을 훑은 뒤, 2장부터 꼼꼼히 읽어도 된다. JPA 부분이 시급하다면 8·9·10장을 먼저 보고 필요할 때 2~4장으로 돌아오는 것도 나쁘지 않다.

## 다루지 않는 것들

이 책의 범위를 미리 밝혀두는 편이 낫다. MySQL HeatWave와 Analytics Engine, Lakehouse 같은 OLAP·AI 영역은 다루지 않는다. 이 책의 관심사는 OLTP, 즉 트랜잭션 처리다. NDB Cluster도 다루지 않는다. 한국 시장에서 운영 사례를 거의 찾기 어렵다. MySQL 9.x의 새 기능들도 14장의 "다음에 볼 것" 수준으로만 언급한다. 사례가 아직 쌓이지 않은 기능을 깊이 다루는 건 독자에게 도움이 되지 않는다.

이 경계 안에서, 가능한 한 깊이 들어가는 것이 이 책의 방식이다.

## 마무리

월요일 새벽 두 시의 그 개발자 이야기를 다시 해보자. 이 책을 다 읽은 뒤라면, 그 데드락 로그를 열었을 때 다른 반응이 나온다. `SHOW ENGINE INNODB STATUS`를 열고, 어느 트랜잭션이 어느 레코드에서 대기하고 있는지 읽어낸다. 갭 락인지 레코드 락인지 확인한다. 어떤 순서로 락이 걸렸는지 추적한다. 그리고 근본 원인을 찾아 제대로 고친다. 재시도 로직은 물론 붙이겠지만, 이번엔 근거가 있는 재시도다.

그 차이를 만드는 것이 이 책의 목표다.

자, 지금 이 책이 왜 필요한지 먼저 살펴보자. 1장에서 MySQL 8.x가 바꿔놓은 풍경을 훑어보며 시작한다.


# 1장. MySQL 8.x가 바꾼 풍경 — 이 책이 *지금* 출간되는 이유

"그냥 5.7 쓰던 것처럼 쓰면 되는 거 아닌가요?"

MySQL 8.0이 나온 지 몇 년이 지났는데도 이 질문을 여전히 자주 듣는다. 틀린 말이 아니다. `SELECT`, `INSERT`, `UPDATE`, `JOIN` — 이 기본들은 변하지 않았다. JPA도 잘 돌아간다. 애플리케이션 레이어에서 보면 8.0으로 올라간 뒤에 달라진 게 없어 보인다.

그런데 그건 표면의 이야기다. 안을 들여다보면, 8.0부터 8.4 LTS까지의 변화는 생각보다 크다. 그리고 그 변화들 중 일부는 스프링 개발자의 일상에 직접 부딪히는 것들이다. 그 변화들의 지형을 빠르게 훑어보자. 지금 당장 깊이 이해할 필요는 없다. 좌표를 잡는 것이 이 장의 몫이다 — 우리가 지금 어떤 버전의, 어떤 기능을 갖춘 MySQL과 함께 일하고 있는지를 아는 것.

## 8.0이 가져온 것들

### 드디어 쓸 만해진 SQL — 윈도우 함수와 CTE

5.7 시절, 누적 합계나 순위 같은 걸 쿼리로 내야 할 때 어떻게 했는지 기억하는가. 서브쿼리를 자기 자신과 조인하거나, 애플리케이션 레이어에서 처리하거나, 아니면 복잡한 사용자 변수 핵을 쓰거나. 어느 방법이나 찜찜했다.

8.0부터 윈도우 함수가 도입됐다. `ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`, `SUM() OVER()`. 이것들이 생기자 보고서 쿼리의 모습이 달라졌다. 날짜별 누적 매출, 사용자별 이전 주문과의 금액 차이, 부서 내 급여 순위 — 애플리케이션에서 깎던 것들을 SQL로 내릴 수 있게 됐다. 6장에서 이것들을 충분히 다룰 것이다.

CTE(Common Table Expression)도 함께 왔다. `WITH` 절로 쿼리를 이름을 붙여 쪼개는 방식. 재귀 CTE도 된다 — 계층 구조를 SQL로 탐색할 수 있다. 가독성이 좋아지고, 복잡한 서브쿼리를 펴낼 수 있다. 이것도 6장의 몫이다.

### 히스토그램: 옵티마이저가 더 똑똑해졌다

인덱스가 없는 컬럼의 데이터 분포를 옵티마이저는 어떻게 추정할까. 5.7까지는 일종의 짐작이었다. 테이블 전체 row 수와 균등 분포 가정을 바탕으로 cost를 계산했다. 데이터가 실제로 편중되어 있어도 그 사실을 알 수 없었다.

8.0에서는 히스토그램 통계가 도입됐다. `ANALYZE TABLE t UPDATE HISTOGRAM ON column_name`을 실행하면 MySQL이 그 컬럼의 값 분포를 버킷별로 요약해 저장한다. 이 정보를 이용해 `WHERE status = 'CANCELLED'` 같은 필터의 선택도를 더 정확히 추정할 수 있다. 5장에서 `EXPLAIN ANALYZE`와 `optimizer_trace`를 다루면서 이 히스토그램이 어떻게 옵티마이저 결정에 영향을 주는지 살펴볼 것이다.

### Descending 인덱스와 Functional 인덱스

8.0 이전의 MySQL에는 내림차순 인덱스가 진짜로 존재하지 않았다는 사실, 알고 있었는가? `DESC`라고 선언해도 내부적으로는 오름차순으로 저장하고 역방향으로 스캔하는 방식이었다. `(created_at DESC, id ASC)` 같은 혼합 정렬을 인덱스로 커버하는 게 불가능했다.

8.0부터는 진짜 내림차순 인덱스가 지원된다. 혼합 정렬을 포함한 복합 인덱스가 제대로 작동한다. `ORDER BY created_at DESC, id ASC` 쿼리가 `Using filesort` 없이 인덱스 스캔으로 처리된다. 4장 인덱스 설계 편에서 이 차이를 자세히 볼 것이다.

Functional 인덱스(함수 인덱스)도 왔다. `CREATE INDEX idx ON t ((LOWER(name)))` 같은 형태로, 표현식 결과를 인덱스로 만들 수 있다. JSON 컬럼 안의 특정 경로에 인덱스를 걸 때도 쓰인다. 이 중 JSON functional 인덱스는 7장에서 본격적으로 다룬다.

### EXPLAIN ANALYZE: 추정이 아닌 실행 결과

`EXPLAIN`은 오래전부터 있었다. 쿼리 실행 계획을 보여주는 도구. 그런데 5.7 시절의 `EXPLAIN`은 추정값이었다. 실제로 몇 개의 row를 읽었는지가 아니라, 옵티마이저가 읽을 것이라고 예상하는 값이다.

8.0.18부터 `EXPLAIN ANALYZE`가 생겼다. 쿼리를 실제로 실행하면서 각 노드의 실제 실행 시간과 row 수를 함께 보여준다. 추정과 실제의 괴리를 바로 볼 수 있다. 이 도구 하나로 슬로우 쿼리 분석 방식이 달라졌다. 5장 전체가 이 도구를 충분히 다루는 데 할애된다.

```sql
-- 추정값만 보여주는 EXPLAIN
EXPLAIN SELECT * FROM orders WHERE customer_id = 1;

-- 실제 실행 시간과 row 수까지 보여주는 EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 1;
```

## 8.0.30: redo 로그가 살아있는 동안 크기를 바꿀 수 있게 됐다

운영 측면에서 주목할 만한 변화가 8.0.30에 있었다. redo 로그의 크기를 동적으로 바꿀 수 있게 됐다.

5.7과 8.0.30 이전에는 `innodb_log_file_size`를 바꾸려면 MySQL을 내리고 redo 로그 파일을 직접 삭제한 뒤 다시 시작해야 했다. 운영 중인 서비스에서 이 작업을 하려면 점검 시간이 필요했다. 트랜잭션이 많은 시스템에서 redo 로그가 너무 작으면 쓰기 성능이 저하되는데, 그걸 고치기 위해 서비스를 내려야 했던 것이다.

8.0.30부터는 `innodb_redo_log_capacity` 파라미터 하나로, 서비스를 내리지 않고 동적으로 크기를 조정할 수 있다. 내부적으로 redo 로그 파일이 32개로 분할되어 관리된다. 긴급 상황에서 redo 로그 포화로 성능이 저하되는 것을 점검 없이 대응할 수 있게 됐다.

2장에서 redo 로그가 왜 존재하는지, 어떤 역할을 하는지를 깊이 다룰 것이다. 지금은 "크기를 서비스 중에 바꿀 수 있게 됐다"는 사실만 기억해두자.

## 8.4 LTS: 다섯 가지 놀라움

8.4가 LTS(장기 지원 버전)로 지정됐다. 보통 LTS라고 하면 "더 안정적"이라는 뜻으로 받아들인다. 그런데 8.4에는 이전 버전에서 사용하던 방식이 그대로 통하지 않는 변화들이 포함되어 있다. Skeema 엔지니어들이 정리한 "다섯 가지 놀라움"이 이 변화들을 잘 요약해준다.

### 첫째, Adaptive Hash Index가 기본 OFF가 됐다

Adaptive Hash Index(AHI)는 자주 들어오는 키 조회를 B-Tree 탐색 없이 해시 직접 접근으로 처리해주는 기능이다. 이론적으로는 읽기 성능을 높여준다.

그런데 쓰기가 많은 워크로드에서는 AHI를 관리하는 락이 오히려 경합을 만들어 성능을 떨어뜨리는 일이 있었다. 8.4에서 기본값이 OFF로 바뀐 이유다. 8.0에서 AHI ON으로 튜닝했던 워크로드라면 8.4로 올라갈 때 이 변화를 직접 측정해봐야 한다. 2장에서 AHI의 작동 방식을 더 자세히 살펴볼 것이다.

### 둘째, Change Buffer도 기본 OFF가 됐다

그렇다면 두 번째는 뭘까. Change Buffer다. 세컨더리 인덱스를 즉시 업데이트하는 대신, 페이지가 버퍼풀에 없을 때 그 변경을 모아뒀다가 나중에 일괄 적용하는 기능이다. INSERT/UPDATE/DELETE 시 디스크 IO를 줄여주는 역할을 한다.

이것도 8.4에서 기본 OFF가 됐다. SSD가 보편화된 환경에서 Change Buffer의 효과가 예전만큼 크지 않고, 오히려 크래시 복구 복잡성을 높인다는 판단이 반영된 것으로 보인다. 2장에서 Change Buffer의 역할을 다룰 때 이 배경을 함께 살펴볼 것이다.

### 셋째, 외래키가 더 엄격해졌다

8.4에서 외래키(FK) 검증이 강화됐다. 정확히는, 부모 테이블의 참조 대상이 정확히 일치하는 unique key(또는 PK)가 있어야만 FK를 선언할 수 있도록 바뀌었다. 이전 버전에서는 좀 더 느슨하게 허용됐다.

이 변화가 체감되는 건 주로 자동화된 마이그레이션 스크립트에서다. Flyway나 Liquibase로 8.0 환경에서 잘 돌아가던 마이그레이션 스크립트가 8.4에서 실패하는 경우가 생길 수 있다. 8장 도메인 모델링과 스키마 설계에서 FK 설계와 함께 이 변화를 다시 볼 것이다.

### 넷째, 인증 플러그인이 바뀌었다

8.0에서 기본 인증 플러그인이 `caching_sha2_password`로 바뀌었다. 5.7에서 쓰던 `mysql_native_password`는 더 이상 기본이 아니다. 8.4에서는 이 방향이 더 강화됐다.

애플리케이션 쪽에서는 JDBC 드라이버 버전에 따라 호환 문제가 생길 수 있다. 특히 구 버전 커넥터를 쓰는 레거시 애플리케이션이라면 주의해야 한다. 12장 보안 편에서 인증 플러그인 설정을 다룰 것이다.

### 다섯째, 그 외 디폴트 변경들

위 네 가지 외에도 여러 기본값 변경이 포함됐다. 이 모든 변화의 공통점은 이전 버전에서 ON이었거나 느슨했던 것들이 OFF로 바뀌거나 엄격해졌다는 점이다. Skeema 팀이 이 변화들을 정리한 글에서 지적하듯, 8.0에서 특정 기본값에 의존하던 워크로드는 8.4로 올라갈 때 회귀가 생길 수 있다.

## 8.0 → 8.4: 다운그레이드는 없다

한 가지 짚고 가자. MySQL은 메이저 버전 간 다운그레이드를 지원하지 않는다. 8.4로 올라간 뒤 문제가 생겼을 때 8.0으로 내려올 수 없다.

이것이 실제로 의미하는 바는 무겁다. 8.4로 업그레이드를 결정하기 전에 충분한 검증이 선행돼야 한다. pt-upgrade로 쿼리 호환성을 사전에 확인하고, AWS Blue/Green Deployment나 8.0 리플리카 승격 방식을 쓰는 것이 현실적인 전략이다. 5.7에서 8.0으로 갈 때도 그랬지만, 탈출구(escape hatch)로 구 버전 리플리카를 일정 기간 유지하는 것이 좋다.

14장에서 메이저 업그레이드 체크리스트를 통해 이 절차를 자세히 살펴볼 것이다. 지금은 "올라가면 내려올 수 없다는 무게감"만 느껴두자.

## 이 책이 기준으로 잡는 버전

이 책은 MySQL 8.0.30 이상을 기준으로 한다. 코드 예제의 SQL 문법과 기능들이 여기에 맞춰져 있다. 8.4 LTS의 변화도 중요한 지점에서 별도로 표시한다.

여전히 5.7을 운영 중이라면 이 책의 대부분은 적용 가능하지만, 8.0부터 생긴 기능들(윈도우 함수, CTE, EXPLAIN ANALYZE, 히스토그램 등)이 없는 환경이라는 점을 감안해야 한다. 5.7 지원 종료가 가까워지고 있다는 점도 기억해두자. 업그레이드 계획은 빠를수록 낫다.

자바 쪽 코드 예제는 Spring Boot 3.x, Hibernate 6.x를 기준으로 한다.

## 마무리

여기까지가 변화의 지형이다. 8.0이 가져온 기능들 — 윈도우 함수, CTE, 히스토그램, descending 인덱스, EXPLAIN ANALYZE — 이 것들이 "있다"는 사실을 이제 알았다. 8.4의 다섯 가지 변화들이 어디서 부딪히는지도 예고됐다.

이제 기반을 다질 시간이다. 다음 장인 2장에서는 InnoDB가 내부적으로 어떻게 돌아가는지를 살펴보자. 버퍼풀이 뭔지, redo 로그가 왜 필요한지, MVCC가 어떻게 다중 버전을 만드는지, B+Tree가 어떻게 생겼는지. 그 그림이 잡혀 있어야 3장의 트랜잭션과 락이, 4장의 인덱스 설계가, 나중에 등장하는 모든 튜닝 이야기가 제대로 들린다.

## 참고 자료

- MySQL Dynamic InnoDB Redo Log in MySQL 8.0: https://dev.mysql.com/blog-archive/dynamic-innodb-redo-log-in-mysql-80/
- MySQL Histogram statistics in MySQL: https://dev.mysql.com/blog-archive/histogram-statistics-in-mysql/
- MySQL EXPLAIN ANALYZE 블로그: https://dev.mysql.com/blog-archive/mysql-explain-analyze/
- Skeema — Five Surprises in MySQL 8.4 LTS: https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- Mydbops — Dynamic InnoDB redo log resize 8.0.30: https://www.mydbops.com/blog/dynamic-innodb-redo-log-resize-mysql-8-0-30


# 2장. InnoDB라는 엔진을 그림으로 이해하자

어떤 SQL을 쓰든, 어떤 JPA 어노테이션을 달든, 실제로 일이 벌어지는 곳은 InnoDB다. 우리가 `save()`를 호출하는 순간 무슨 일이 일어나는가. 데이터가 어디에 쓰이고, 어떻게 복구되고, 트랜잭션 간에 서로의 변경을 어떻게 안 보는 척 하는가. 이 그림이 머릿속에 있는 사람과 없는 사람은, 슬로우 쿼리 앞에서 또는 데드락 로그 앞에서 전혀 다른 반응을 보인다.

이 그림이 잡히면 이후 모든 장이 다르게 들린다. 3장의 락 이야기도, 4장의 인덱스 이야기도, 5장의 `EXPLAIN ANALYZE`도 — 모두 이 장의 그림 위에서 이야기된다. 이 장에 시간을 들이는 게 아깝지 않은 이유가 거기 있다.

## 버퍼풀: 디스크를 가능한 한 덜 보자

MySQL에서 가장 중요한 메모리 영역은 버퍼풀이다. 단순하게 말하면, 디스크에 있는 데이터 페이지를 메모리에 올려놓은 캐시다. MySQL이 `SELECT`를 실행할 때 디스크를 직접 읽는 것이 아니라, 먼저 버퍼풀을 확인한다. 거기 있으면 메모리에서 바로 읽는다. 없으면 디스크에서 페이지를 읽어 버퍼풀에 올린다.

왜 이게 중요한가. 디스크는 메모리보다 몇 배에서 수십 배 느리다. SSD가 보편화된 지금도 메모리는 SSD보다 훨씬 빠르다. 같은 데이터를 반복해서 읽을 때 디스크에 갈 때마다 비용을 내는 것과, 처음 한 번만 디스크에서 읽고 이후는 메모리에서 읽는 것은 성능 차이가 크다.

버퍼풀의 크기를 어떻게 잡아야 할까. 실무 휴리스틱은 "가용 RAM의 70~80%"다. 서버가 MySQL 전용이라면 더 넉넉하게 줘도 된다. 설정 파라미터는 `innodb_buffer_pool_size`다. 메모리가 8GB를 넘는다면 `innodb_buffer_pool_instances`도 같이 설정해서 버퍼풀을 여러 인스턴스로 분할하는 것이 좋다. 경합을 나눌 수 있기 때문이다.

운영 중에 버퍼풀이 충분히 작동하고 있는지 확인하는 지표가 히트율이다. `Innodb_buffer_pool_reads`(디스크를 읽은 횟수)와 `Innodb_buffer_pool_read_requests`(읽기 요청 총 횟수)로 계산한다. 99% 이상이면 대부분의 읽기가 메모리에서 처리되고 있다는 의미다. 히트율이 95% 아래로 떨어지면 버퍼풀이 너무 작거나, 워킹셋이 메모리보다 너무 크다는 신호다.

버퍼풀은 InnoDB가 모든 것의 출발점으로 삼는 공간이다. 이후 이야기할 redo 로그, undo 로그, B+Tree 페이지 — 이것들이 버퍼풀을 통해 접근된다.

```
[ 버퍼풀 구조 ]

+-----------------------------------------------+
|               Buffer Pool                     |
|  +----------+  +----------+  +----------+     |
|  | Page 101 |  | Page 205 |  | Page 312 |     |  <- 16KB 페이지 단위
|  | (Hot)    |  | (Warm)   |  | (Cold)   |     |
|  +----------+  +----------+  +----------+     |
|                                               |
|  Free List  |  LRU List  |  Flush List        |
+-----------------------------------------------+
        |                        |
        v                        v
  [ 디스크 - .ibd 파일 ]    [ redo log 파일 ]
```

내부적으로 버퍼풀은 페이지를 LRU 리스트로 관리한다. 자주 쓰이는 페이지는 "hot" 쪽에, 덜 쓰이는 것은 "cold" 쪽에. 공간이 부족하면 cold 쪽 페이지를 밀어낸다. 단, 변경된 적 있는 페이지(dirty page)는 먼저 디스크에 써야 밀어낼 수 있다. 이 쓰기 작업이 flush다.

## WAL: 데이터보다 로그를 먼저 쓴다

InnoDB의 아이디어 하나만 꼽으라면 WAL(Write-Ahead Logging)을 들겠다. 직역하면 "앞서 쓰는 로그". 데이터 페이지에 변경을 반영하기 전에 먼저 redo 로그에 기록한다는 원칙이다.

왜 이렇게 할까. 데이터 페이지는 디스크에 랜덤하게 흩어져 있다. 여러 페이지에 변경을 쓰는 건 느린 랜덤 IO다. 반면 redo 로그는 순차적으로 계속 추가되는 파일이다. 순차 IO가 랜덤 IO보다 훨씬 빠르다. WAL 덕분에 InnoDB는 커밋을 확인할 때 redo 로그에만 쓰고, 실제 데이터 페이지는 나중에 천천히 디스크에 반영한다(checkpoint).

```
[ WAL 흐름 ]

    트랜잭션 커밋
         |
         v
  1. redo log에 기록 (순차 IO — 빠름)
         |
         v
  2. 커밋 완료 응답
         |
         v  (나중에)
  3. 버퍼풀의 dirty page를 디스크에 flush (랜덤 IO — 느리지만 비동기)
```

크래시가 났을 때 어떻게 될까. MySQL이 재시작되면 redo 로그를 읽어 아직 디스크에 반영되지 않은 변경을 다시 적용한다. 이것이 redo 로그의 존재 이유다. 크래시 복구(crash recovery)를 보장한다.

8.0.30부터는 `innodb_redo_log_capacity`로 redo 로그의 크기를 동적으로 바꿀 수 있게 됐다. 내부적으로 redo 로그는 32개의 파일로 분할되어 순환 방식으로 관리된다. redo 로그가 너무 작으면 flush가 너무 자주 일어나 성능이 저하된다. 반대로 너무 크면 크래시 복구에 오래 걸린다. 워크로드에 맞는 크기를 잡는 것이 중요하다.

## Undo 로그와 MVCC: 같은 row를 여러 시선으로 보는 법

InnoDB의 각 row에는 눈에 보이지 않는 두 개의 컬럼이 더 붙어 있다. `DB_TRX_ID`(6바이트)와 `DB_ROLL_PTR`(7바이트)다.

`DB_TRX_ID`는 이 row를 마지막으로 수정한 트랜잭션 ID다. `DB_ROLL_PTR`은 이 row의 이전 버전이 저장된 undo 로그를 가리키는 포인터다. 이전 버전은 다시 그 이전 버전을 가리키는 포인터를 가지고 있다. 이렇게 연결된 체인이 **버전 체인(version chain)**이다.

```
[ MVCC 버전 체인 ]

현재 row (DB_TRX_ID=100):
  +----------------+-----------+
  | name = "김철수" | ROLL_PTR --|--+
  +----------------+-----------+  |
                                  |
  undo log 버전 (TRX_ID=95):      |
  +----------------+-----------+  |
  | name = "김영수" | ROLL_PTR --|--+--> ...이전 버전들...
  +----------------+-----------+

트랜잭션 A (TRX_ID=90에서 시작):
  - read view: TRX_ID >= 90을 볼 수 없음
  - 버전 체인을 따라가서 TRX_ID=95 이전 버전을 읽음
  -> name = "김영수" (또는 그 이전 버전)를 본다
```

MVCC(Multi-Version Concurrency Control)는 이 구조를 이용해 비잠금 읽기를 가능하게 한다. 트랜잭션이 시작될 때 **read view**를 만든다. 이 read view는 "어느 트랜잭션 ID까지의 변경을 볼 것인가"를 정의한다. `SELECT`를 할 때 현재 row의 `DB_TRX_ID`가 read view 범위 밖에 있으면, `DB_ROLL_PTR`을 따라 undo 로그에서 적절한 버전을 찾아 읽는다.

이것이 InnoDB에서 `SELECT`가 잠금 없이도 안정적인 스냅샷을 볼 수 있는 이유다. 다른 트랜잭션이 행을 수정하는 중이어도, 내 트랜잭션의 read view 기준에 맞는 버전을 버전 체인에서 찾아 읽는다. 쓰기 잠금과 읽기가 서로를 막지 않는다.

단, undo 로그는 영원히 유지되지 않는다. 어떤 read view도 더 이상 그 버전을 필요로 하지 않게 되면 purge 스레드가 삭제한다. 이 때문에 오래 열려 있는 트랜잭션은 undo 로그를 많이 쌓게 하고, 이는 디스크 공간과 성능에 악영향을 준다. 트랜잭션을 짧게 유지하는 것이 중요한 이유 중 하나다.

격리수준이 REPEATABLE READ(RR)냐 READ COMMITTED(RC)냐에 따라 read view를 언제 만드는지가 달라진다. RR에서는 트랜잭션 시작 시 한 번 만들고 끝까지 유지한다. RC에서는 각 `SELECT`마다 새로 만든다. 이것이 두 격리수준의 핵심 차이다. 3장에서 이 차이가 실제로 어떤 결과를 만드는지 자세히 본다.

## B+Tree: 테이블은 사실 정렬된 트리다

InnoDB의 데이터가 어떻게 저장되는지를 이해하려면 B+Tree를 알아야 한다. 이것이 InnoDB가 데이터를 조직하는 기본 자료 구조다.

먼저 B+Tree가 B-Tree와 어떻게 다른지를 짚자. B-Tree는 내부 노드(internal node)에도 데이터를 저장한다. B+Tree는 내부 노드에는 키만 저장하고, 실제 데이터는 리프 노드(leaf node)에만 저장한다. 그리고 B+Tree의 리프 노드들은 서로 연결 리스트로 이어져 있다. 이 차이가 range scan을 효율적으로 만든다 — 특정 범위의 데이터를 읽을 때 리프 노드의 연결 리스트를 따라 순서대로 읽으면 된다.

```
[ B+Tree 구조 (단순화) ]

                   [ 루트 노드 ]
                  | 50 | 100 |
                 /     |     \
        [ 내부 노드 ] [ 내부 ] [ 내부 노드 ]
        | 20 | 30 |            | 110 | 150 |
        /    |    \            /     |     \
       /     |     \          /      |      \
[리프] [리프] [리프]     [리프] [리프] [리프]
|10|20| |25|30| |40|50|  |100|110| |120|150| |160|
   <-->    <-->    <-->       <-->      <-->
   (리프 노드는 연결 리스트로 이어짐)
```

InnoDB의 페이지 크기는 기본 16KB다. 각 페이지 안에 여러 개의 row(또는 key)가 들어간다. 내부 노드에는 키와 자식 페이지 포인터가 들어가고, 리프 노드에는 키와 실제 row 데이터가 들어간다.

**클러스터링 인덱스**가 핵심이다. InnoDB에서 테이블의 주 인덱스는 항상 클러스터링 인덱스다. 그리고 클러스터링 인덱스는 반드시 PK를 키로 한다. 달리 말하면, **InnoDB 테이블은 PK 기준으로 정렬된 B+Tree 그 자체**다. 테이블과 클러스터링 인덱스는 하나다. 테이블을 PK 순서대로 읽는다는 것은 B+Tree의 리프 노드를 순서대로 읽는다는 것이다.

여기서 중요한 함의가 있다. PK가 무작위 값(예: UUID)이면 새 row를 삽입할 때마다 B+Tree의 임의의 위치에 삽입해야 한다. 이는 기존 페이지를 분열시키는(page split) 작업을 자주 일으킨다. 반면 auto_increment PK는 항상 맨 끝에 추가되므로 페이지 분열이 드물고 쓰기 성능이 좋다. PK 선택이 인덱스 설계의 출발점인 이유가 바로 이것이다. 4장에서 더 자세히 다룬다.

**세컨더리 인덱스**는 클러스터링 인덱스 외의 모든 인덱스다. 세컨더리 인덱스의 리프 노드에는 인덱스 키와 함께 해당 row의 PK값이 저장된다. `email` 컬럼으로 세컨더리 인덱스를 만들었다면, 리프 노드에는 `(email, PK)` 쌍이 들어간다.

`WHERE email = 'user@example.com'` 쿼리가 오면 어떻게 되는가. 세컨더리 인덱스 B+Tree에서 해당 email을 찾는다. 거기서 PK를 꺼낸다. 그 PK로 클러스터링 인덱스 B+Tree를 다시 조회한다. 이 두 번째 조회가 **back-to-table**(또는 PK 룩업)이다. 이 비용은 세컨더리 인덱스가 있는 `SELECT`에 항상 포함된다. 커버링 인덱스를 쓰면 이 back-to-table을 없앨 수 있다. 4장에서 자세히 본다.

### 페이지 디렉터리

Jeremy Cole이 정리한 InnoDB 시리즈에서 흥미로운 사실이 있다. 각 페이지 안에는 슬롯(slot) 배열 형태의 페이지 디렉터리가 있다. 이것을 이용해 페이지 내부의 row를 이진 탐색으로 찾는다. 페이지 안의 모든 row를 순서대로 스캔하는 게 아니라, 이 디렉터리로 위치를 빠르게 좁힌다.

이것은 B+Tree 탐색이 루트에서 리프까지 내려온 다음, 페이지 안에서 이진 탐색으로 row를 찾는 두 단계로 이루어진다는 것을 의미한다.

## Adaptive Hash Index: B+Tree를 우회하는 고속도로

AHI(Adaptive Hash Index)는 InnoDB가 자동으로 관리하는 해시 인덱스다. 자주 조회되는 인덱스 키를 감지해서 내부 해시 테이블을 만든다. 이후 그 키로 조회가 오면 B+Tree 트래버스를 건너뛰고 해시 테이블에서 직접 페이지 위치를 찾는다. 단일 키 포인트 조회에서 속도가 빠르다.

```
[ AHI 동작 ]

일반 경로:
  키 → 루트 노드 → 내부 노드 → 내부 노드 → 리프 노드
                  (3~4 레벨 트래버스)

AHI 경로:
  키 → 해시 테이블 → 리프 노드 직접 접근
      (트래버스 없음)
```

그런데 1장에서 언급했듯, 8.4에서 AHI 기본값이 OFF가 됐다. 왜일까. AHI 해시 테이블을 관리하는 것 자체에 비용이 있다. row가 변경될 때마다 AHI도 업데이트해야 한다. 쓰기가 많은 워크로드에서는 이 업데이트 경합이 오히려 성능을 떨어뜨릴 수 있다. 카카오 기술 블로그에서도 쓰기 무거운 환경에서 AHI를 끄자 성능이 개선된 사례를 소개했다.

AHI가 도움이 되는지는 워크로드에 따라 다르다. 읽기가 많고 같은 키를 반복해서 조회하는 패턴이라면 효과가 있다. 쓰기가 많거나 다양한 키를 무작위로 조회하는 패턴이라면 오히려 부담이다. 8.4로 업그레이드할 때 AHI를 켜고 끄면서 워크로드별로 측정해보는 것이 좋다.

## Change Buffer: 세컨더리 인덱스 업데이트를 미루자

INSERT나 UPDATE가 발생할 때, 클러스터링 인덱스는 즉시 업데이트해야 한다. 그런데 세컨더리 인덱스는 어떨까. 세컨더리 인덱스의 해당 페이지가 현재 버퍼풀에 있다면 바로 업데이트하면 된다. 그런데 버퍼풀에 없다면? 디스크에서 페이지를 불러와야 한다. 이게 비용이다.

Change Buffer는 이 비용을 나중으로 미루는 기능이다. 세컨더리 인덱스 업데이트 대상 페이지가 버퍼풀에 없을 때, 그 변경 사항을 Change Buffer에 기록해두고 나중에 그 페이지가 버퍼풀에 올라오면 그때 일괄 적용한다.

```
[ Change Buffer 동작 ]

INSERT 발생:
  1. 클러스터링 인덱스 업데이트 (즉시)
  2. 세컨더리 인덱스 페이지가 버퍼풀에 있는가?
     YES → 즉시 업데이트
     NO  → Change Buffer에 변경 기록 (디스크 IO 없이 빠름)

나중에 그 페이지가 버퍼풀에 로드될 때:
  → Change Buffer의 변경을 병합(merge)하여 적용
```

Change Buffer도 AHI처럼 8.4에서 기본 OFF가 됐다. SSD가 보편화되면서 랜덤 IO 비용이 줄었고, Change Buffer가 절약하는 IO의 가치가 예전보다 낮아진 것이 배경이다. 또한 크래시 복구 시 Change Buffer의 변경을 병합하는 데 시간이 걸리는 복잡성도 있다.

Change Buffer가 도움이 되는 환경은 HDD를 사용하거나, 버퍼풀에 잘 올라오지 않는 세컨더리 인덱스가 많고 쓰기 트래픽이 큰 경우다. SSD 기반 현대 환경에서는 기본 OFF로 두는 것이 합리적인 경우가 많다.

## 이 그림을 들고 앞으로 가자

여기까지가 InnoDB의 여섯 가지 핵심 구조다. 버퍼풀, WAL과 redo 로그, undo 로그와 MVCC, B+Tree 페이지 구조, AHI, Change Buffer. 이것들이 하나로 연결되어 있다는 점을 기억해두자.

- `SELECT`가 오면 → 버퍼풀을 먼저 확인, 없으면 디스크에서 읽어 버퍼풀에 올림
- `INSERT/UPDATE/DELETE`가 오면 → redo 로그에 먼저 기록, 버퍼풀의 페이지 수정, 변경된 페이지(dirty page)는 나중에 flush
- 트랜잭션이 row를 수정하면 → 이전 버전을 undo 로그에 저장, `DB_ROLL_PTR`로 연결
- 다른 트랜잭션이 그 row를 읽으면 → read view와 비교, 버전 체인을 따라 적절한 버전 반환
- 인덱스 조회는 → B+Tree를 루트에서 리프까지 탐색, 자주 쓰이는 키는 AHI가 단축
- 세컨더리 인덱스 업데이트는 → 해당 페이지가 버퍼풀에 없으면 Change Buffer에 기록 후 병합

이 흐름이 잡혀 있으면, 다음 장의 이야기들이 "그래서 그게 거기서 나왔구나" 하고 자연스럽게 연결된다.

## 마무리

이 장에서 InnoDB의 내부 구조를 한 장의 그림으로 만들었다. 솔직히 말하면, 이 그림은 단순화된 버전이다. 실제 InnoDB의 구현은 훨씬 복잡하다. 이 장에서 소개한 각 개념은 모두 책 한 권 분량의 깊이를 가지고 있다. Jeremy Cole의 InnoDB 시리즈나 Real MySQL 8.0 같은 자료가 그 깊이를 채워준다.

그렇지만 이 장에서 잡은 멘탈 모델로도 충분히 실용적인 의사결정을 내릴 수 있다. "버퍼풀이 충분한가?", "redo 로그가 충분한가?", "이 트랜잭션이 undo 로그를 오래 붙들고 있지 않은가?", "이 인덱스가 back-to-table을 발생시키는가?" — 이런 질문들을 물어볼 수 있게 됐다면 충분하다.

다음 장에서는 이 그림 위에 트랜잭션과 격리수준, 그리고 락을 얹는다. InnoDB가 어떤 SQL에 어떤 락을 거는지, 격리수준이 다르면 뭐가 달라지는지, 데드락은 어디서 어떻게 생기는지. MVCC와 B+Tree를 알고 보면 락 이야기가 훨씬 자연스럽게 들린다.

## 참고 자료

- MySQL :: 17.5.1 Buffer Pool — https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html
- MySQL :: 17.6.5 Redo Log — https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- MySQL :: 17.3 InnoDB Multi-Versioning — https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html
- Jeremy Cole — InnoDB series: https://blog.jcole.us/innodb/
- 카카오 — MySQL InnoDB Log 이해: https://tech.kakao.com/posts/721
- 카카오 — InnoDB Adaptive Hash Index 활용: https://tech.kakao.com/posts/319
- Skeema — Five Surprises in MySQL 8.4 LTS: https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- Mydbops — Dynamic InnoDB redo log resize 8.0.30: https://www.mydbops.com/blog/dynamic-innodb-redo-log-resize-mysql-8-0-30


# 3장. 트랜잭션, 격리수준, 그리고 락의 메커니즘

새벽 두 시에 슬랙 알람이 온다. "결제 처리가 안 돼요." 로그를 열면 이런 메시지가 있다.

```
ERROR 1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```

이 메시지를 받았을 때 "재시도하면 되겠지"로 끝내는 개발자와, `SHOW ENGINE INNODB STATUS`를 열어 어떤 트랜잭션이 어떤 레코드에서 서로를 기다리고 있는지를 읽어내는 개발자의 차이는 크다.

그 차이를 만드는 것이 이 장이다. 락의 메커니즘을 다루자. InnoDB가 어떤 락을 언제 어디에 거는가. 애플리케이션 패턴 — 낙관적·비관적·분산락을 코드에서 어떻게 거는지 — 은 10장의 몫이다.

## 격리수준: 어디까지 보여줄 것인가

트랜잭션 격리수준은 "동시에 실행되는 다른 트랜잭션의 변경이 내 트랜잭션에 어디까지 보이는가"를 정한다. SQL 표준은 네 단계를 정의한다.

| 격리수준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|---------|-----------|---------------------|-------------|
| READ UNCOMMITTED | 허용 | 허용 | 허용 |
| READ COMMITTED | 차단 | 허용 | 허용 |
| REPEATABLE READ | 차단 | 차단 | 허용* |
| SERIALIZABLE | 차단 | 차단 | 차단 |

*InnoDB의 RR은 next-key lock으로 phantom을 추가 차단한다.

세 가지 이상 현상이 무엇인지 짚고 가자.

**Dirty Read**: 아직 커밋되지 않은 변경을 읽는 것. 트랜잭션 A가 row를 수정했는데 아직 커밋하지 않았다. 트랜잭션 B가 그 수정된 값을 읽는다. 이후 A가 롤백하면, B는 존재하지 않는 데이터를 읽었던 것이 된다. 끔찍한 일이다.

**Non-Repeatable Read**: 같은 쿼리를 두 번 실행했는데 결과가 다른 것. 트랜잭션 A가 row를 읽었다. 그 사이에 트랜잭션 B가 그 row를 수정하고 커밋했다. A가 같은 row를 다시 읽으면 값이 달라져 있다. "아까 읽었을 때는 10000원이었는데 지금은 9000원이 됐다"는 상황이다.

**Phantom Read**: 같은 범위 쿼리를 두 번 실행했는데 row 수가 달라지는 것. 트랜잭션 A가 `WHERE age > 20`으로 읽었다. 그 사이에 B가 age=25인 row를 추가하고 커밋했다. A가 다시 같은 조건으로 읽으면 row가 하나 더 있다.

### InnoDB의 기본: REPEATABLE READ

MySQL InnoDB의 기본 격리수준은 REPEATABLE READ(RR)다. 2장에서 설명한 MVCC가 이것을 가능하게 한다. 트랜잭션 시작 시 read view를 만들고, 트랜잭션이 끝날 때까지 같은 read view를 유지한다. 그래서 트랜잭션 중에 아무리 다른 트랜잭션이 row를 수정하고 커밋해도, 내 read view 기준의 일관된 스냅샷을 본다.

그런데 MVCC만으로는 phantom을 막을 수 없다. range 조회로 존재하지 않는 row에 대한 INSERT를 막을 방법이 없기 때문이다. InnoDB는 next-key lock으로 이 문제를 추가 해결한다. 이것은 잠시 후 락 메커니즘을 다루면서 본다.

```sql
-- 세션 1: 트랜잭션 시작
START TRANSACTION;
SELECT * FROM orders WHERE amount > 10000;
-- 결과: 3건

-- 세션 2: 이 사이에 실행 (커밋 완료)
INSERT INTO orders (amount) VALUES (15000);
COMMIT;

-- 세션 1: 같은 쿼리 다시 실행
SELECT * FROM orders WHERE amount > 10000;
-- RR: 여전히 3건 (read view가 유지되므로)
-- RC라면: 4건 (새 read view를 만들기 때문에)
```

### READ COMMITTED를 선택하면

RC를 선택하면 무엇을 잃고 무엇을 얻는가.

잃는 것: 같은 트랜잭션 안에서 동일 row를 두 번 읽으면 값이 달라질 수 있다. 트랜잭션 중간에 다른 트랜잭션이 커밋한 변경이 보인다. 데이터의 일관성 스냅샷이 보장되지 않는다.

얻는 것: 갭 락이 거의 없어진다. 갭 락이 줄어들면 동시에 여러 트랜잭션이 삽입할 때 서로 막히는 일이 줄어든다. 데드락도 감소하는 경향이 있다.

실무에서 RC를 선택하는 경우는 주로 두 가지다. 높은 INSERT 동시성이 필요해서 갭 락 경합을 줄여야 할 때, 또는 각 쿼리가 항상 최신 데이터를 봐야 할 때. 많은 OLTP 시스템에서 RC가 충분하고, 오히려 RR보다 더 자연스럽게 동작하는 경우도 있다.

한 가지 주의할 점이 있다. RC에서는 binlog가 반드시 row 포맷이어야 한다. statement 포맷에서 RC를 쓰면 복제 안전성이 보장되지 않는다. 최신 MySQL은 row 포맷이 기본이므로 실제로 문제가 되는 경우는 드물지만, 알고 있는 것이 좋다.

## InnoDB가 거는 락의 종류

이제 락 메커니즘으로 들어가자. InnoDB는 여러 종류의 락을 거는데, 각각이 다른 목적을 가지고 있다.

### 레코드 락: 인덱스 레코드를 잠근다

레코드 락(Record Lock)은 가장 기본적인 락이다. 인덱스 레코드 자체에 거는 잠금이다. 중요한 점은, InnoDB의 레코드 락은 **테이블의 row가 아니라 인덱스 레코드에** 건다는 것이다.

```sql
-- id=1 인 레코드에 대한 레코드 락
SELECT * FROM orders WHERE id = 1 FOR UPDATE;
```

이 쿼리가 실행되면 id=1 인덱스 레코드에 배타적 락(X lock)이 걸린다. 다른 트랜잭션이 같은 레코드를 수정하거나 배타적 락을 걸려고 하면 대기한다.

인덱스가 없는 컬럼으로 조건을 걸면 어떻게 될까. InnoDB는 모든 레코드를 인덱스를 통해 접근한다. 인덱스가 없는 컬럼으로 `FOR UPDATE`를 하면 클러스터링 인덱스의 전체 레코드에 락이 걸릴 수 있다. 이것이 락 범위를 예상보다 훨씬 크게 만드는 흔한 함정이다.

### 갭 락: 없는 곳을 잠근다

갭 락(Gap Lock)은 인덱스 레코드들 사이의 간격(gap)에 거는 잠금이다. 정확히 말하면, 인덱스의 두 레코드 사이, 첫 레코드 이전, 마지막 레코드 이후의 공간이다.

갭 락의 목적은 그 gap에 새 row가 INSERT되는 것을 막는 것이다. phantom을 방지하기 위한 메커니즘이다.

```sql
-- RR에서 이 쿼리는 id가 (10, 20) 사이의 gap에 갭 락을 건다
SELECT * FROM orders WHERE id > 10 AND id < 20 FOR UPDATE;

-- 다른 트랜잭션에서 이 INSERT는 위 갭 락 때문에 대기한다
INSERT INTO orders (id, ...) VALUES (15, ...);
```

갭 락의 중요한 특성이 있다. **갭 락끼리는 서로 호환된다.** 두 트랜잭션이 같은 gap에 각각 갭 락을 걸 수 있다. 갭 락은 INSERT를 막는 것이 목적이지, 다른 트랜잭션의 갭 락 진입을 막는 것이 아니다. 그러나 갭 락을 가진 트랜잭션 두 개가 서로 INSERT를 시도하면 데드락이 생길 수 있다.

RC 격리수준에서는 갭 락이 거의 사용되지 않는다. 이것이 RC에서 INSERT 동시성이 높아지는 이유다.

### 넥스트키 락: 레코드 락 + 갭 락

넥스트키 락(Next-Key Lock)은 레코드 락과 갭 락을 합친 것이다. 레코드 자체와 그 레코드 앞의 gap까지 같이 잠근다. RR 격리수준에서 InnoDB가 range 조회 시 기본적으로 사용하는 락이다.

```
인덱스: [1] [5] [10] [20]
넥스트키 락 범위:
  (-∞, 1]  →  id=1에 대한 넥스트키 락
  (1, 5]   →  id=5에 대한 넥스트키 락
  (5, 10]  →  id=10에 대한 넥스트키 락
  (10, 20] →  id=20에 대한 넥스트키 락
  (20, ∞)  →  마지막 gap(supremum)에 대한 갭 락
```

`SELECT * FROM orders WHERE id > 5 AND id <= 15 FOR UPDATE`를 실행하면 `(5, 10]`과 `(10, 20]` 범위에 넥스트키 락이 걸린다. 즉 id=10, id=20에 레코드 락이, (5,10)과 (10,20) gap에 갭 락이 각각 걸린다.

이것이 RR에서 phantom이 막히는 이유다. 새로운 row가 이 범위 안에 INSERT되려면 갭 락에 막힌다.

그런데 이 넥스트키 락이 때로는 필요 이상으로 넓은 범위에 걸리는 것이 데드락의 원인이 되기도 한다.

### 인텐션 락: 테이블과 행 락의 공존

인텐션 락(Intention Lock)은 테이블 단위 잠금과 행 단위 잠금이 공존할 수 있게 해주는 테이블 수준의 잠금이다. "이 테이블 안에 행 잠금이 있다"는 신호를 테이블 레벨에서 표시한다.

IS(Intention Shared)와 IX(Intention Exclusive) 두 종류가 있다. 행에 공유 락을 걸기 전에 테이블에 IS를, 행에 배타 락을 걸기 전에 테이블에 IX를 건다.

인텐션 락은 테이블 전체에 대한 락(LOCK TABLE ... WRITE 같은)과 행 락이 충돌하지 않도록 조율하는 역할을 한다. 일반 OLTP 쿼리에서 개발자가 직접 신경 쓸 일은 거의 없지만, `SHOW ENGINE INNODB STATUS`의 락 정보를 읽을 때 이 락이 등장하면 혼란스러울 수 있으므로 개념을 알아두자.

### 락 호환성 매트릭스

어떤 락이 어떤 락과 공존할 수 있는지를 정리한 것이 호환성 매트릭스다.

| | IS | IX | S | X |
|--|---|---|---|---|
| **IS** | 호환 | 호환 | 호환 | 충돌 |
| **IX** | 호환 | 호환 | 충돌 | 충돌 |
| **S** | 호환 | 충돌 | 호환 | 충돌 |
| **X** | 충돌 | 충돌 | 충돌 | 충돌 |

(IS: Intention Shared, IX: Intention Exclusive, S: Shared(행), X: Exclusive(행))

핵심을 정리하면:
- 공유 락(S)끼리는 호환된다. 여러 트랜잭션이 같은 row를 읽을 수 있다.
- 배타 락(X)은 모든 것과 충돌한다. X락을 잡은 트랜잭션이 있으면 다른 트랜잭션은 S도 X도 모두 대기해야 한다.
- IX끼리는 호환된다. 여러 트랜잭션이 테이블의 다른 행들을 각각 배타 락으로 잡을 수 있다.

## 어떤 SQL이 어떤 락을 거는가

이제 구체적인 SQL 문장이 어떤 락을 거는지를 살펴보자. 실무에서 가장 자주 부딪히는 부분이다.

### SELECT: 잠금이 없다(기본)

일반 `SELECT`는 잠금을 걸지 않는다. MVCC로 일관된 스냅샷을 읽기 때문에 락 없이도 동시성을 보장한다. 이것이 InnoDB의 강점 중 하나다.

```sql
-- 락 없음 (스냅샷 읽기)
SELECT * FROM orders WHERE customer_id = 1;
```

### SELECT ... FOR SHARE / FOR UPDATE: 잠금 읽기

명시적으로 락을 걸어야 할 때는 `FOR SHARE`(S락)나 `FOR UPDATE`(X락)를 사용한다.

```sql
-- 공유 락 (FOR SHARE = LOCK IN SHARE MODE)
SELECT * FROM orders WHERE id = 1 FOR SHARE;

-- 배타 락
SELECT * FROM orders WHERE id = 1 FOR UPDATE;
```

`FOR UPDATE`는 읽은 row에 X락을 건다. 이 row를 UPDATE나 DELETE하려는 다른 트랜잭션은 대기해야 한다. 재고 차감이나 포인트 사용 같이 "읽고 즉시 수정"하는 패턴에서 쓴다.

조건에 인덱스가 없거나, range 조건이면 락 범위가 커진다는 점을 기억해두자.

### INSERT: 삽입 의도 락

INSERT는 삽입할 위치의 gap에 "삽입 의도 락(Insert Intention Lock)"을 건다. 삽입 의도 락끼리는 호환된다 — 같은 gap에 여러 INSERT가 동시에 들어와도 서로 다른 위치라면 기다리지 않아도 된다.

그런데 그 gap에 이미 갭 락이 있다면? 다른 트랜잭션의 갭 락이 그 위치를 막고 있으면, INSERT는 대기해야 한다.

```sql
-- RR에서 트랜잭션 A가 이 쿼리로 gap 락을 잡으면
SELECT * FROM orders WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- 트랜잭션 B의 이 INSERT는 대기한다
INSERT INTO orders (id, ...) VALUES (15, ...);
```

### UPDATE와 DELETE

조건에 맞는 row들에 X락을 건다. range 조건이면 넥스트키 락이 걸릴 수 있다.

```sql
-- id=5인 row에 X락
UPDATE orders SET status = 'PAID' WHERE id = 5;

-- id > 100 이면서 status='PENDING'인 모든 row와 그 gap에 락
-- (조건에 따라 락 범위가 달라질 수 있다)
UPDATE orders SET status = 'EXPIRED' WHERE id > 100 AND status = 'PENDING';
```

### 외래키 검증

외래키가 있을 때 INSERT나 UPDATE는 추가 락을 유발한다. 자식 테이블에 INSERT할 때 부모 테이블의 해당 row에 S락을 건다. 이것은 부모 row가 외래키 검증 중에 삭제되는 것을 막기 위해서다.

```sql
-- order_items에 INSERT할 때 orders.id에 S락이 걸린다
INSERT INTO order_items (order_id, product_id, quantity)
VALUES (1, 100, 2);
```

이 동작이 때로는 예상치 못한 락 경합을 만든다. 부모 테이블을 DELETE하려는 트랜잭션과 자식 테이블에 INSERT하려는 트랜잭션이 서로 대기하는 상황이 생길 수 있다.

## 데드락: 사이클을 읽어내는 법

데드락은 두 트랜잭션이 서로의 락을 기다리는 순환 대기다. InnoDB는 이 순환을 감지해 한쪽 트랜잭션을 강제로 롤백한다.

### 전형적인 데드락 패턴

```sql
-- 트랜잭션 A
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- A가 row1에 X락
-- 이 시점에 트랜잭션 B가 실행됨

-- 트랜잭션 B
START TRANSACTION;
UPDATE accounts SET balance = balance - 200 WHERE id = 2;  -- B가 row2에 X락
UPDATE accounts SET balance = balance + 200 WHERE id = 1;  -- B가 row1 X락 시도 → A 대기

-- 트랜잭션 A (계속)
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- A가 row2 X락 시도 → B 대기
-- A는 B를 기다리고, B는 A를 기다린다 → 데드락
```

### SHOW ENGINE INNODB STATUS로 읽기

데드락이 발생하면 InnoDB는 마지막 데드락 정보를 내부에 보관한다. `SHOW ENGINE INNODB STATUS`의 LATEST DETECTED DEADLOCK 섹션에서 볼 수 있다.

```sql
SHOW ENGINE INNODB STATUS\G
```

출력의 LATEST DETECTED DEADLOCK 부분에는 두 트랜잭션이 각각 어떤 락을 보유하고 어떤 락을 대기하고 있었는지가 나온다. 읽는 법을 배우자.

```
TRANSACTION 1, ACTIVE 2 sec starting index read
MySQL thread id 15, OS thread handle ...
...
HOLDS THE LOCK(S):
RECORD LOCKS space id 5 page no 4 n bits 72 index PRIMARY
of table `shop`.`orders` trx id 421 lock_mode X locks rec but not gap
Record lock, heap no 2 PHYSICAL RECORD: ...

WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 5 page no 4 n bits 72 index PRIMARY
of table `shop`.`orders` trx id 421 lock_mode X locks rec but not gap
```

중요한 키워드는 `HOLDS THE LOCK(S)`와 `WAITING FOR THIS LOCK TO BE GRANTED`다. 트랜잭션 1이 어떤 락을 잡고 있으면서 어떤 락을 기다리는지, 트랜잭션 2가 어떤 락을 잡고 있으면서 어떤 락을 기다리는지를 읽으면, 두 트랜잭션이 서로를 기다리는 사이클이 보인다.

`lock_mode X locks rec but not gap`은 갭 없는 레코드 락(넥스트키 락이 아닌 순수 레코드 락)이고, `lock_mode X`는 넥스트키 락, `lock_mode X locks gap before rec`는 갭 락이다.

### information_schema로 현재 락 상태 보기

데드락이 아니라 현재 대기 중인 락 상태를 보려면 `performance_schema.data_locks`와 `data_lock_waits`를 쓴다.

```sql
-- 현재 잡혀 있는 락 목록
SELECT
  ENGINE_TRANSACTION_ID,
  OBJECT_SCHEMA,
  OBJECT_NAME,
  INDEX_NAME,
  LOCK_TYPE,
  LOCK_MODE,
  LOCK_STATUS,
  LOCK_DATA
FROM performance_schema.data_locks
WHERE LOCK_STATUS = 'WAITING';

-- 어떤 트랜잭션이 어떤 트랜잭션을 기다리는지
SELECT
  r.REQUESTING_ENGINE_TRANSACTION_ID AS waiting_trx,
  b.BLOCKING_ENGINE_TRANSACTION_ID AS blocking_trx,
  bl.OBJECT_NAME AS table_name,
  bl.LOCK_TYPE,
  bl.LOCK_MODE
FROM performance_schema.data_lock_waits r
JOIN performance_schema.data_locks bl
  ON bl.ENGINE_LOCK_ID = r.BLOCKING_ENGINE_LOCK_ID;
```

이 쿼리들로 락 대기가 왜 생기고 있는지를 실시간으로 볼 수 있다.

### 데드락은 버그가 아니라 신호다

데드락이 떴다고 해서 버그라는 뜻은 아니다. 동시성 높은 시스템에서는 피하기 어렵다. 중요한 것은 두 가지다.

첫째, **재시도 가능한 구조**. 데드락을 만난 트랜잭션은 처음부터 다시 시도해야 한다. 스프링의 `@Transactional` + `@Retryable` 조합으로 재시도 로직을 만들 수 있다. 재시도할 때 같은 연산을 해도 되는 멱등성이 보장돼야 한다.

둘째, **락 순서 일관성**. 여러 row에 락을 거는 순서가 트랜잭션마다 다르면 순환이 생기기 쉽다. 항상 같은 순서로 잠그면 사이클이 만들어지기 어렵다. 위의 예에서 두 트랜잭션이 모두 "id가 작은 것부터 먼저 잠근다"는 규칙을 지킨다면 데드락이 발생하지 않는다.

## 낙관적·비관적 락: 개념만 짚고 가자

낙관적 락과 비관적 락은 코드 패턴의 이야기다. 10장에서 JPA와 함께 자세히 다룬다. 여기서는 개념만 빠르게 정리하자.

**낙관적 락**: 충돌이 드물다고 가정한다. 잠금 없이 읽고 수정한다. 커밋 시점에 다른 트랜잭션이 먼저 수정했는지를 version 컬럼으로 확인한다. 충돌이 났으면 재시도한다. JPA의 `@Version` 어노테이션이 이를 구현한다.

**비관적 락**: 충돌이 잦다고 가정하거나, 충돌 시 재시도 비용이 크다고 판단할 때 쓴다. 읽는 시점부터 `FOR UPDATE`로 잠근다. JPA의 `@Lock(PESSIMISTIC_WRITE)` 또는 직접 `SELECT ... FOR UPDATE`다.

선택 기준은 간단하다. 충돌 빈도가 낮고 재시도 비용이 크지 않으면 낙관적 락, 그 반대면 비관적 락이 적합하다. 코드 패턴과 스프링 통합은 10장에서 본다.

## 심화: Jepsen과 PostgreSQL 진영의 다른 시각

이 절은 심화 내용이다. 락 메커니즘의 기본이 잡혔다면 읽어보자. 나중에 돌아와도 된다.

Jepsen은 분산 시스템과 데이터베이스의 정합성을 테스트하는 프레임워크다. MySQL 8.0.34 분석(jepsen.io)에서, RR 격리수준 하에서도 여전히 일부 이상 현상 — fractured read, lost update — 이 발생할 수 있음을 보였다.

이게 왜 가능한가. InnoDB의 RR은 MVCC 스냅샷으로 비잠금 읽기를 보호하지만, 잠금 읽기(`FOR UPDATE`)와 비잠금 읽기가 섞이면 일관성이 깨질 수 있다. 트랜잭션 중에 두 번의 읽기를 각각 잠금 없이, 잠금 있이 섞어서 하면 서로 다른 버전을 볼 수 있다.

Jepsen 분석의 결론은: **금전 트랜잭션같이 엄격한 일관성이 필요한 경우라면 RR + 명시적 비관적 락을 조합하거나, SERIALIZABLE을 고려하라**는 것이다.

PostgreSQL 진영의 접근 방식은 다르다. PostgreSQL은 RC를 기본 격리수준으로 쓰면서, 필요할 때 SSI(Serializable Snapshot Isolation)를 통해 완전한 직렬성을 보장한다. MySQL의 RR + 갭 락 방식보다 더 정교한 충돌 감지를 제공하지만, 오버헤드도 있다.

MySQL 진영은 기본 RR을 유지하면서 명시적 락으로 보완하는 방식을 취한다. 어느 쪽이 더 낫다고 단정할 수 없다. 워크로드와 팀의 방식에 따라 맞는 선택이 다르다. Cahill(2009)의 논문이 스냅샷 격리와 직렬성 격리의 관계를 이론적으로 정리한 참고 자료다 — 종장의 참고 문헌 절에서 안내한다.

실무에서는 대부분의 일반 OLTP가 RR 기본값으로 충분하다. 금전 이동, 재고 차감처럼 정합성이 핵심인 로직에서는 명시적 비관적 락(`FOR UPDATE`)을 쓰는 것이 가장 확실하다.

## 마무리

이 장에서 InnoDB의 락 메커니즘을 처음부터 끝까지 살펴봤다. 격리수준 네 단계와 각각이 허용·차단하는 이상 현상, 레코드·갭·넥스트키·인텐션 락의 역할과 호환성, 구체적인 SQL이 어떤 락을 유발하는지, 그리고 데드락 로그를 읽는 방법까지.

기억해두자: 데드락 로그가 찜찜하게 느껴졌던 것은 락 메커니즘의 그림이 없어서였다. 이 그림이 잡히면 그 로그가 전혀 다르게 보인다.

다음 장에서는 인덱스 설계로 넘어간다. B+Tree의 구조와 클러스터링 인덱스의 본질을 알고 있는 지금, 인덱스 이야기가 훨씬 자연스럽게 들릴 것이다.

## 참고 자료

- MySQL :: 17.7.1 InnoDB Locking — https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- MySQL :: 17.7.2.1 Transaction Isolation Levels — https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html
- MySQL :: 17.7.4 Phantom Rows / Next-Key Locking — https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html
- MySQL :: 17.7.5 Deadlocks in InnoDB — https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html
- MySQL :: InnoDB Data Locking Part 3 "Deadlocks" — https://dev.mysql.com/blog-archive/innodb-data-locking-part-3-deadlocks/
- Percona — InnoDB's Gap Locks — https://www.percona.com/blog/innodbs-gap-locks/
- Jepsen — MySQL 8.0.34 분석 — https://jepsen.io/analyses/mysql-8.0.34
- letmecompile.com — MySQL InnoDB lock & deadlock 이해하기 — https://www.letmecompile.com/mysql-innodb-lock-deadlock/
- Bytebase — How to show MySQL locks — https://www.bytebase.com/reference/mysql/how-to/how-to-show-mysql-locks/


# 4장. 인덱스 설계는 데이터 구조 설계다

velog의 한 개발자가 남긴 후기를 보자. `promotion_option` 테이블의 `promotion_id` 컬럼에 인덱스가 없었다. LEFT JOIN을 할 때마다 그 테이블을 풀 스캔했다. 쿼리 실행 시간: 6초. 인덱스 하나 추가했다. 실행 시간: 0.02초. 300배 차이다.

OKKY에도 비슷한 이야기가 있다. 이번엔 인덱스가 아예 없었던 게 아니라 복합 인덱스의 컬럼 순서가 문제였다. 순서를 바꿨더니 11초에서 0.1초로 줄었다.

인덱스 하나, 컬럼 순서 하나. 그런데 그 차이가 300배, 110배다. 왜 그럴까. 인덱스가 어떤 자료 구조이고, 어떤 원리로 쿼리를 빠르게 만드는지를 이해하면 이 질문에 답할 수 있다. 그리고 "이 쿼리에는 어떤 인덱스를 걸어야 하는가"를 직관으로 판단할 수 있게 된다.

## 클러스터링 인덱스: 테이블 자체가 인덱스다

2장에서 봤던 그림을 다시 꺼내자. InnoDB에서 테이블은 PK 기준으로 정렬된 B+Tree 그 자체다. 테이블을 저장하는 방식이 클러스터링 인덱스다. 테이블과 클러스터링 인덱스는 별개가 아니다 — 하나다.

이것이 왜 중요한가. PK로 row를 찾는 것은 B+Tree를 딱 한 번 타고 내려가는 것이다. 루트에서 리프까지. 리프 노드에 실제 row 데이터가 있다. 그 이상의 비용이 없다.

```
PK 조회:
  클러스터링 인덱스 B+Tree
  루트 → 내부 노드 → 내부 노드 → 리프 노드(row 데이터 있음)
  = 1회 B+Tree 탐색으로 데이터 획득
```

PK가 없는 테이블은 어떻게 되는가. InnoDB는 PK가 없으면 NOT NULL인 unique 인덱스를 클러스터링 인덱스로 쓴다. 그것도 없으면 내부적으로 숨겨진 6바이트 row ID를 생성해 클러스터링 인덱스로 사용한다. 이 숨겨진 row ID는 개발자가 접근할 수 없어 JOIN 조건 등에 쓸 수 없다. 그래서 **모든 InnoDB 테이블에는 PK를 명시적으로 정의하는 것이 좋다.**

### PK 선택이 쓰기 성능을 결정한다

PK 값이 무작위(UUID 같은)이면 새 row를 삽입할 때마다 B+Tree의 임의의 위치에 넣어야 한다. 그 위치의 리프 페이지가 꽉 찼다면 페이지를 두 개로 나눈다 — 이게 **page split**이다. 페이지 분열은 새 페이지 할당, 기존 페이지 이동, 상위 노드 업데이트를 포함하는 비용 있는 작업이다. UUID를 PK로 쓰면 이 page split이 빈번하게 일어난다.

auto_increment PK는 항상 맨 끝에 추가된다. B+Tree의 오른쪽 끝 리프 노드에만 삽입된다. page split이 거의 없다. 순차 쓰기는 InnoDB에게 가장 효율적인 패턴이다.

그렇다면 UUID를 전혀 쓰면 안 되는가. 그건 아니다. UUID를 애플리케이션에서 외부 식별자로 쓰되, 실제 PK는 auto_increment로 하고 UUID는 별도 unique 컬럼으로 두는 방식도 많이 쓰인다. ULID나 UUIDv7처럼 시간 순서로 정렬되는 UUID 변형을 쓰면 page split을 상당히 줄일 수 있다. 8장에서 PK 전략을 더 깊이 다룰 것이다.

JPA 엔티티에서는 PK 전략을 어노테이션 한 줄로 표현한다. 어느 쪽을 고르는지가 쓰기 성능을 정한다는 점을 기억해두자.

```java
@Entity
public class Order {
    // 권장: auto_increment 기반 — 순차 삽입으로 page split 최소화
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 외부 식별자가 필요하다면 별도 unique 컬럼으로
    @Column(unique = true, updatable = false, nullable = false)
    private String publicId; // UUID 또는 ULID
}
```

## 세컨더리 인덱스: back-to-table과 그 비용

PK 외의 모든 인덱스가 세컨더리 인덱스다. 세컨더리 인덱스의 리프 노드에는 (인덱스 키, PK) 쌍이 저장된다. PK가 포함되는 이유는 클러스터링 인덱스로 가는 포인터가 필요하기 때문이다.

`SELECT * FROM orders WHERE email = 'user@example.com'`을 실행한다고 해보자. `email` 컬럼에 세컨더리 인덱스가 있다면:

1. 세컨더리 인덱스 B+Tree에서 `email = 'user@example.com'`을 찾는다
2. 거기서 PK 값을 꺼낸다 (예: id = 42)
3. 클러스터링 인덱스 B+Tree에서 id = 42를 찾는다
4. 리프 노드에서 전체 row 데이터를 읽는다

```
세컨더리 인덱스 조회:
  세컨더리 인덱스 B+Tree: email → PK 획득
                           ↓
  클러스터링 인덱스 B+Tree: PK → row 데이터
  = 2회 B+Tree 탐색
```

3번 단계가 **back-to-table**(테이블로 돌아가기, 또는 PK 룩업)이다. 세컨더리 인덱스 조회에는 항상 이 추가 비용이 따른다. `EXPLAIN`의 `type` 컬럼이 `ref`나 `range`로 나오지만 Extra에 `Using index`가 없다면, back-to-table이 일어나고 있다는 뜻이다.

back-to-table 비용이 큰 경우는 주로 range scan으로 많은 row를 읽을 때다. row 수가 많을수록 클러스터링 인덱스를 그만큼 더 많이 찌른다. 이 때문에 옵티마이저가 세컨더리 인덱스 대신 풀 테이블 스캔을 선택하는 경우도 있다 — "인덱스를 쓰나 테이블을 다 뒤지나 비용이 비슷하거나, 어차피 많이 읽어야 하면 순차 스캔이 더 빠를 수 있다"고 판단할 때다.

이 back-to-table을 없애는 방법이 커버링 인덱스다.

## 복합 인덱스: 순서가 운명이다

OKKY 사례의 핵심이 여기서 풀린다. 같은 컬럼으로 복합 인덱스를 만들었는데, 컬럼 순서를 바꿨더니 11초가 0.1초가 됐다.

복합 인덱스(Composite Index)는 여러 컬럼을 하나의 인덱스로 묶은 것이다. `(a, b, c)` 복합 인덱스라고 하면 이 인덱스의 B+Tree는 (a, b, c) 값의 조합을 키로 정렬되어 있다.

### Leftmost Prefix Rule

복합 인덱스 `(a, b, c)`가 활용되는 조건은 **leftmost prefix**다.

```
(a, b, c) 복합 인덱스가 사용되는 쿼리:
  WHERE a = ?                    → 사용 가능
  WHERE a = ? AND b = ?          → 사용 가능
  WHERE a = ? AND b = ? AND c = ? → 사용 가능
  WHERE a = ? AND c = ?          → a 부분만 사용, c는 인덱스 미사용
  WHERE b = ?                    → 사용 불가
  WHERE b = ? AND c = ?          → 사용 불가
```

왜 그런가. 인덱스 B+Tree는 (a, b, c) 순서로 정렬되어 있다. `a`로 먼저 정렬되고, 같은 `a` 값 안에서 `b`로 정렬되고, 같은 `(a, b)` 값 안에서 `c`로 정렬된다. `WHERE b = ?` 조건은 첫 번째 정렬 키 `a`를 건너뛰기 때문에 이 정렬된 구조를 활용할 수 없다.

```
[ (a, b, c) 인덱스의 정렬 ]

a=1, b=2, c=10
a=1, b=2, c=20
a=1, b=3, c=5
a=2, b=1, c=8
a=2, b=2, c=15
...

WHERE b = 2: b가 2인 것이 연속하지 않아서 B+Tree 탐색 불가
WHERE a = 1: a=1인 부분이 연속해 있어서 B+Tree 탐색 가능
```

### Equality → Range → Sort 순서 휴리스틱

복합 인덱스를 설계할 때 컬럼 순서는 어떻게 정해야 하는가. 기본 원칙은 **equality 조건 먼저, range 조건은 그다음, sort 컬럼은 마지막**이다.

쿼리가 `WHERE status = 'PAID' AND created_at > '2024-01-01' ORDER BY created_at`라면:

- `status`: equality (`=`)
- `created_at`: range (`>`) + sort

인덱스 순서는 `(status, created_at)`이 좋다. `status`로 좁힌 다음, `created_at`으로 range scan하면서 정렬까지 처리할 수 있다.

`(created_at, status)`로 하면 어떻게 되는가. `created_at > '2024-01-01'` range로 먼저 좁힌 뒤, 그 안에서 `status = 'PAID'`를 필터링해야 한다. range 이후의 컬럼은 인덱스 탐색이 아니라 필터링이 되므로, 더 많은 레코드를 읽고 버린다.

equality가 여러 개라면 **카디널리티(cardinality, 값의 종류 수)가 높은 것을 앞에** 두는 것이 좋다. `gender (M/F, 카디널리티 2)`보다 `user_id (카디널리티 수천만)`이 먼저 오면 더 잘 좁혀진다.

```
[ Leftmost Prefix와 인덱스 활용 시각화 ]

인덱스: (status, created_at)

쿼리: WHERE status = 'PAID' AND created_at > '2024-01-01'

B+Tree 탐색:
  └─ status = 'PAID' 구간으로 이동
       └─ created_at > '2024-01-01' 범위 스캔
          (인덱스 순방향 스캔 → Using index range)

쿼리: WHERE created_at > '2024-01-01'
  → status 없이 created_at만으로는 위 인덱스 활용 불가
  → 인덱스가 있다면 (created_at) 단독 인덱스가 필요
```

이것이 OKKY 사례의 핵심이었다. 조건 컬럼의 순서가 맞지 않은 복합 인덱스는 효과를 낼 수 없다.

## 커버링 인덱스: back-to-table을 없애자

**커버링 인덱스(Covering Index)**는 쿼리가 필요로 하는 모든 컬럼이 인덱스 안에 들어 있어서, 클러스터링 인덱스(테이블)로 돌아갈 필요가 없는 인덱스다.

```sql
-- users 테이블에 (email) 인덱스가 있다
-- 이 쿼리는 back-to-table 발생
SELECT id, name, email FROM users WHERE email = 'user@example.com';
-- → 세컨더리 인덱스에서 email → PK, 다시 클러스터링 인덱스에서 name 읽기

-- (email, name) 복합 인덱스가 있다
-- 이 쿼리는 커버링 인덱스
SELECT id, name FROM users WHERE email = 'user@example.com';
-- → 세컨더리 인덱스에서 email → (name, PK) 모두 읽기 가능
-- → 클러스터링 인덱스로 돌아갈 필요 없음
```

`EXPLAIN`의 Extra 컬럼에 `Using index`가 나오면 커버링 인덱스가 작동하고 있다는 뜻이다.

커버링 인덱스는 특히 range scan이나 집계 쿼리에서 효과가 크다. 수만 건을 읽어야 하는 range scan에서 back-to-table이 없다는 것은, 수만 번의 클러스터링 인덱스 조회를 하지 않아도 된다는 뜻이다.

커버링 인덱스를 설계할 때는 SELECT 컬럼 목록도 같이 고려해야 한다. "이 쿼리에서 어떤 컬럼이 필요한가"를 확인한 뒤, 그 컬럼들을 모두 인덱스에 포함시킨다.

주의할 점: 인덱스에 포함하는 컬럼이 많아질수록 인덱스 크기가 커지고, INSERT/UPDATE 시 인덱스 업데이트 비용도 증가한다. 트레이드오프를 고려해야 한다.

## 프리픽스·Descending·Functional 인덱스

### 프리픽스 인덱스

VARCHAR나 TEXT 컬럼 전체를 인덱스로 만들면 인덱스 크기가 커진다. 앞 N바이트만 인덱스로 만드는 것이 **프리픽스 인덱스**다.

```sql
CREATE INDEX idx_email_prefix ON users (email(20));
```

장점은 인덱스 크기가 줄어들고, 쓰기 비용이 낮아진다는 것이다. 단점은 카디널리티가 낮아진다는 것이다. 이메일 앞 20자만 인덱스에 있으면, 앞 20자가 같은 이메일들이 인덱스에서 같아 보인다. 커버링 인덱스로 쓸 수 없다 — 실제 값이 인덱스에 완전히 없기 때문에 항상 back-to-table이 필요하다.

긴 텍스트 컬럼에 인덱스가 필요할 때는 적절한 prefix 길이를 찾는 것이 중요하다. `COUNT(DISTINCT LEFT(email, N))` / `COUNT(DISTINCT email)`로 N별 카디널리티 비율을 확인하고, 적절한 N을 찾자.

### Descending 인덱스

8.0부터 지원한다. `ORDER BY a ASC, b DESC` 같이 혼합 정렬을 인덱스로 처리할 수 있다.

```sql
-- (created_at DESC, id DESC) 인덱스 생성
CREATE INDEX idx_created_desc ON orders (created_at DESC, id DESC);

-- 이 쿼리는 Using filesort 없이 인덱스 스캔으로 처리
SELECT * FROM orders ORDER BY created_at DESC, id DESC LIMIT 10;
```

5.7에서는 이런 혼합 정렬을 인덱스로 처리할 수 없어 `Using filesort`가 발생했다. 8.0부터 가능해졌다. 카카오 기술 블로그가 오름차순/내림차순 인덱스 차이를 정리한 글이 이 내용을 잘 설명한다.

### Functional 인덱스

표현식 결과에 인덱스를 걸 수 있게 됐다 — 8.0.13부터다.

```sql
-- LOWER(name)에 인덱스
CREATE INDEX idx_name_lower ON users ((LOWER(name)));

-- 이 쿼리가 인덱스를 쓸 수 있다
SELECT * FROM users WHERE LOWER(name) = 'john';
```

함수를 컬럼에 적용하면 인덱스를 못 쓰는 것이 기본이다. `WHERE LOWER(name) = 'john'`은 `name` 컬럼 인덱스를 쓸 수 없다. Functional 인덱스를 만들어두면 표현식 자체를 인덱스로 쓸 수 있다.

JSON 컬럼의 특정 경로에 인덱스를 걸 때도 쓸 수 있다. 단, JSON 데이터 모델링과 JSON functional 인덱스의 본격적인 풀이는 7장에서 한다. 여기서는 "인덱스 도구함에 JSON functional 인덱스가 있다"는 사실만 기억해두자.

## Invisible 인덱스: 안전하게 인덱스를 제거하자

인덱스가 실제로 사용되고 있는지 확인하지 않고 삭제했다가 갑자기 쿼리가 느려지는 경우가 있다. 난감한 상황이다. 되돌리려면 인덱스를 다시 만들어야 하는데, 대용량 테이블에서 그건 또 시간이 걸린다.

**Invisible 인덱스**를 쓰면 이 위험을 줄일 수 있다. 옵티마이저가 특정 인덱스를 무시하도록 설정하는 기능이다. 인덱스를 실제로 삭제하지 않고, 옵티마이저 입장에서 없는 것처럼 처리한다.

```sql
-- 인덱스를 invisible로 설정 (옵티마이저가 무시)
ALTER TABLE orders ALTER INDEX idx_status INVISIBLE;

-- 이후 서비스를 관찰한다. 느려진다면?
ALTER TABLE orders ALTER INDEX idx_status VISIBLE;  -- 즉시 복구

-- 이상 없으면 진짜로 삭제
ALTER TABLE orders DROP INDEX idx_status;
```

Invisible로 설정해두고 모니터링하는 기간 동안 슬로우 쿼리가 생기지 않는다면, 그 인덱스는 실제로 쓰이지 않는다고 확신할 수 있다. 그때 삭제한다.

인덱스가 invisible 상태여도 인덱스 자체는 유지되므로, INSERT/UPDATE 시 여전히 인덱스를 업데이트한다. 조회 성능 개선이 없는데 쓰기 비용만 내는 상태가 된다. 그러므로 invisible 기간을 너무 길게 유지하는 것은 좋지 않다.

## 인덱스 개수: 3~5개 휴리스틱

인덱스가 많을수록 좋은 것 아닌가. 그렇지 않다.

인덱스는 조회를 빠르게 하지만, 모든 쓰기(INSERT/UPDATE/DELETE)를 느리게 한다. 테이블에 row를 추가하거나 인덱스 컬럼을 수정하면, 관련된 모든 인덱스 B+Tree를 업데이트해야 하기 때문이다. 인덱스가 5개면 쓰기 1번에 B+Tree를 5번 업데이트한다.

또한 인덱스는 디스크 공간과 버퍼풀 공간을 차지한다. 인덱스가 많을수록 버퍼풀에서 인덱스 페이지가 데이터 페이지를 밀어내 버퍼풀 히트율에도 영향을 준다.

실무 휴리스틱: **테이블당 인덱스는 3~5개 수준으로 유지**하는 것이 좋다. 물론 조회 패턴에 따라 달라지지만, 10개가 넘어가면 한 번 검토해볼 필요가 있다. 쓰기가 많은 테이블일수록 인덱스 수를 줄이는 것이 유리하다.

중복 인덱스나 쓰이지 않는 인덱스는 제거하는 편이 낫다. `sys.schema_unused_indexes` 뷰나 `performance_schema.table_io_waits_summary_by_index_usage`로 인덱스별 사용 빈도를 확인할 수 있다.

```sql
-- 사용되지 않는 인덱스 확인
SELECT *
FROM sys.schema_unused_indexes
WHERE object_schema = 'mydb';

-- 인덱스별 조회 횟수
SELECT
  object_schema, object_name, index_name,
  count_read, count_write
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'mydb'
  AND index_name IS NOT NULL
ORDER BY count_read;
```

## INSERT/UPDATE 비용: 쓰기가 많다면 인덱스는 신중하게

쓰기가 많은 테이블에 인덱스를 추가하는 결정은 신중하게 해야 한다. 주문 상태 업데이트가 초당 수천 번 일어나는 테이블이라면, 인덱스 하나를 추가하는 것이 초당 수천 번의 추가 B+Tree 업데이트를 의미한다.

버퍼풀에 인덱스 페이지가 올라와 있다면 메모리에서 처리되지만, 이것도 버퍼풀 경합을 증가시킨다. 2장에서 Change Buffer의 역할을 기억하는가. Change Buffer는 세컨더리 인덱스 업데이트를 나중으로 미뤄 이 비용을 완화해준다. 그런데 8.4에서 기본 OFF가 됐으므로, 8.4에서는 이 완충이 없다.

실제로 인덱스 추가가 쓰기 성능에 얼마나 영향을 주는지는 측정해봐야 안다. 테스트 환경에서 인덱스 추가 전후 INSERT 성능을 비교해보는 것이 가장 확실하다.

## 실제 사례로 돌아가서

velog 사례를 다시 보자. `promotion_option.promotion_id`에 인덱스가 없었다. LEFT JOIN에서 매번 promotion_option 테이블을 풀 스캔했다. 결과 집합이 작아도 promotion_option 테이블이 크다면 전체를 읽어야 했다. 인덱스 하나 추가로 B+Tree 탐색 → 매칭 레코드만 접근으로 바뀌었다. 6초 → 0.02초.

그런데 이야기가 거기서 끝나지 않았다. 인덱스를 추가했더니 이번엔 옵티마이저가 JOIN 컬럼 인덱스를 "너무 우선"해서 다른 인덱스를 무시하는 현상이 생겼다. 이것이 인덱스 추가로 끝이 아닌 이유다. 인덱스를 추가한 뒤 `EXPLAIN`으로 옵티마이저가 어떤 인덱스를 선택했는지, 예상대로 움직이는지를 확인해야 한다. 5장이 이 확인 절차를 다룬다.

OKKY 사례는 복합 인덱스 컬럼 순서의 문제였다. 세부 내용은 공개되어 있지 않지만, equality 조건 컬럼을 앞에, range 조건 컬럼을 뒤에 두는 leftmost prefix 원칙을 지키지 않은 것이 원인이었을 가능성이 높다.

## 마무리

인덱스 설계는 데이터 구조 설계다. B+Tree라는 자료 구조의 정렬 속성을 얼마나 잘 활용하느냐가 핵심이다. 이 장에서 다룬 것들을 요약하자.

- 클러스터링 인덱스 = PK = 테이블. InnoDB에서 테이블은 PK 기준 B+Tree 그 자체다.
- 세컨더리 인덱스 조회는 back-to-table 비용이 포함된다. 커버링 인덱스로 없앨 수 있다.
- 복합 인덱스는 leftmost prefix 규칙을 따른다. equality → range → sort 순서로 컬럼을 배치한다.
- 인덱스는 조회를 빠르게 하지만 쓰기를 느리게 한다. 3~5개 휴리스틱을 기억하자.
- Invisible 인덱스로 안전하게 인덱스 제거를 검증할 수 있다.

다음 장에서는 이 인덱스들이 실제로 어떻게 사용되는지를 `EXPLAIN ANALYZE`로 확인하는 법을 배운다. 인덱스를 만들었다고 해서 항상 쓰이는 것은 아니다. 5장이 그 이유를 파헤친다.

## 참고 자료

- MySQL :: 17.7.1 InnoDB Locking — https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- DEV.to — Understanding Composite Indexes: https://dohost.us/index.php/2025/08/01/the-leftmost-prefix-rule-optimizing-composite-index-usage/
- Red-Gate — Composite B-tree indexes: https://www.red-gate.com/simple-talk/databases/mysql/mysql-index-overviews-composite-b-tree-indexes/
- velog "MySQL 인덱스 성능 개선하기 - 커버링 인덱스": https://velog.io/@rnjsrntkd95/MySQL-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-%EC%BB%A4%EB%B2%84%EB%A7%81-%EC%9D%B8%EB%8D%B1%EC%8A%A4
- velog "슬로우 쿼리 개선기": https://velog.io/@bruni_23yong/%EC%8A%AC%EB%A1%9C%EC%9A%B0-%EC%BF%BC%EB%A6%AC-%EA%B0%9C%EC%84%A0%EA%B8%B0
- velog "쿼리 속도 개선기": https://velog.io/@gkh4302/%EC%BF%BC%EB%A6%AC-%EC%86%8D%EB%8F%84-%EA%B0%9C%EC%84%A0%EA%B8%B0
- 카카오 — Ascending vs Descending index: https://tech.kakao.com/posts/351


# 5장. EXPLAIN ANALYZE를 안에서 바깥으로 읽기

슬랙 알람이 울렸다. "결제 목록 API가 10초 넘게 걸려요." 담당 개발자가 열어보니 쿼리가 하나 있고, 그 쿼리는 지난 6개월 동안 아무도 건드리지 않았다. 데이터가 쌓인 것 외에 달라진 건 없다. 그런데 갑자기 10초다.

EXPLAIN을 실행해 본다. 뭔가 줄줄이 나오는데, 솔직히 어디서부터 읽어야 할지 모르겠다. `rows`가 크면 나쁜 건지, `key`가 NULL이면 다 느린 건지, `Extra`에 `Using filesort`가 보이면 무조건 인덱스를 추가해야 하는 건지. 아는 것 같으면서도 막상 실제 쿼리 앞에서는 손이 멈춘다. 이 찜찜함은 꽤 보편적이다.

EXPLAIN과 EXPLAIN ANALYZE의 차이부터 시작해 실제 슬로우 쿼리 한 건을 처음부터 끝까지 분해해 보자. 목표는 하나다 — 다음번에 슬랙 알람이 울렸을 때 혼자 손을 댈 수 있는 절차를 손에 쥐는 것.

## EXPLAIN과 EXPLAIN ANALYZE — 추정과 현실 사이

MySQL의 EXPLAIN은 오래전부터 있었다. 쿼리 앞에 `EXPLAIN`을 붙이면 옵티마이저가 어떤 실행 계획을 선택했는지를 보여주는데, 여기서 나오는 숫자들 — `rows`, `filtered`, `key_len` 같은 것들 — 은 모두 *추정값*이다. 옵티마이저가 통계 정보를 보고 계산한 예측이지, 실제로 쿼리를 실행해서 나온 측정값이 아니다.

EXPLAIN ANALYZE는 다르다. 8.0.18부터 추가된 이 명령은 쿼리를 *실제로 실행*하면서 각 노드의 소요 시간과 실제 처리 행 수를 함께 수집한다. 출력 형태도 달라진다. EXPLAIN FORMAT=TREE처럼 들여쓰기 된 트리 구조로 나오고, 각 노드마다 두 쌍의 숫자가 붙는다.

```sql
-- EXPLAIN ANALYZE 기본 사용법
EXPLAIN ANALYZE
SELECT o.id, o.amount, u.name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'COMPLETED'
  AND o.created_at >= '2024-01-01'
ORDER BY o.created_at DESC
LIMIT 50;
```

출력에서 각 노드 옆에 붙는 숫자 패턴은 이렇게 생겼다.

```
-> Nested loop inner join  (cost=1234.56 rows=500)
                           (actual time=0.123..45.678 rows=48 loops=1)
```

괄호 두 개가 핵심이다. 첫 번째 괄호 `(cost=... rows=...)` 는 옵티마이저의 추정치고, 두 번째 괄호 `(actual time=0.123..45.678 rows=48 loops=1)` 는 실제 측정값이다. `actual time`의 두 숫자는 '첫 번째 행을 꺼내기까지 걸린 시간'과 '마지막 행까지 전부 처리한 시간'이다. 이 두 값의 차이가 크다면 그 노드가 스트리밍으로 처리되지 않고 중간 어딘가에서 전체 결과를 모아야 했다는 신호다.

## 트리를 안에서 바깥으로 읽는 법

EXPLAIN ANALYZE 트리를 처음 보면 흔히 빠지는 실수가 있다. 위에서 아래로, 즉 바깥 노드부터 읽는 것이다. 이렇게 읽으면 전체적인 실행 흐름은 이해할 수 있지만 "어디서 시간이 가장 많이 쓰였는가"를 파악하기 어렵다.

MySQL의 실행 트리는 안쪽 노드가 먼저 실행된다. 가장 깊이 들여쓰인 노드가 가장 먼저 데이터를 가져오고, 그 결과가 바깥 노드로 올라간다. 마치 함수 호출 스택처럼 — 안쪽이 호출되고, 그 결과가 바깥으로 돌아온다. 그래서 슬로우 쿼리의 원인을 찾으려면 가장 안쪽(들여쓰기가 가장 깊은) 노드부터 읽어야 한다.

예를 들어 이런 트리가 있다고 해보자.

```
-> Limit: 50 row(s)
   (actual time=234.56..234.67 rows=50 loops=1)
    -> Sort: orders.created_at DESC
       (actual time=234.44..234.52 rows=50 loops=1)
        -> Filter: (orders.status = 'COMPLETED')
           (actual time=0.08..233.91 rows=50 loops=1)
            -> Table scan on orders
               (actual time=0.07..180.23 rows=1000000 loops=1)
```

바깥에서 읽으면 `Limit → Sort → Filter → Table scan` 순서처럼 보이지만, 실제 실행은 반대다. `Table scan on orders`가 먼저 실행되어 100만 개 행을 하나씩 꺼내고, 그게 올라와서 `Filter`를 통과하고, 그 다음 `Sort`로 정렬되고, 마지막에 50개를 잘라낸다.

`actual time`을 보면 더 명확하다. `Table scan on orders`에서 이미 180.23ms를 쓰고 있다. 100만 행을 풀스캔하고 있는 것이다. 여기에 인덱스를 추가하거나, 필터 조건을 인덱스가 담당하게 만들어보자.

이 읽는 순서를 몸에 익히는 가장 쉬운 방법은 "들여쓰기가 가장 깊은 곳의 actual time을 먼저 확인하고, 거기서 위로 올라오면서 숫자가 어디서 커지는지 따라가는 것"이다. 시간이 크게 늘어나는 전환점이 병목이다.

## 추정치와 실측치의 괴리 — 통계가 오래됐을 때

EXPLAIN과 EXPLAIN ANALYZE의 숫자가 크게 다를 때가 있다. 추정은 500행인데 실제로는 50만 행을 처리한다든가. 이런 괴리가 생기는 원인은 대부분 *통계 정보가 오래됐거나 부정확*하기 때문이다.

MySQL의 옵티마이저는 테이블의 행 수 분포, 각 컬럼의 값 분포 같은 통계 정보를 보고 cost를 추정한다. 그런데 데이터가 빠르게 쌓이는 테이블은 통계가 실제 분포를 따라잡지 못할 때가 있다. 예를 들어 한 달 전 데이터로 통계를 만들었는데 그 이후 1000만 행이 들어온 경우다.

이때 시도해볼 첫 번째 수단이 `ANALYZE TABLE`이다.

```sql
-- 통계 갱신
ANALYZE TABLE orders;

-- 특정 컬럼에 히스토그램 생성 (8.0 이상)
ANALYZE TABLE orders UPDATE HISTOGRAM ON status, created_at;
```

8.0부터는 히스토그램 통계가 추가됐다. 인덱스가 없는 컬럼에 대해서도 값의 분포를 별도 통계로 관리할 수 있어, 옵티마이저가 더 정확한 cost 추정을 할 수 있게 됐다. `status` 컬럼처럼 카디널리티가 낮지만 특정 값이 압도적으로 많은 경우 — 예를 들어 전체 주문의 95%가 `COMPLETED`인 상황 — 에 히스토그램이 빛을 발한다.

히스토그램을 만들어도 여전히 추정치와 실측치 사이의 차이가 크다면, 더 깊은 곳을 봐야 한다. `optimizer_trace`를 켜면 옵티마이저가 어떤 플랜을 고려했고, 각각의 cost를 어떻게 계산했는지를 JSON 형태로 볼 수 있다.

```sql
-- optimizer_trace 켜기
SET SESSION optimizer_trace = 'enabled=on';
SET SESSION optimizer_trace_max_mem_size = 1000000;

-- 분석할 쿼리 실행
SELECT o.id, o.amount
FROM orders o
WHERE o.status = 'COMPLETED'
  AND o.created_at >= '2024-01-01';

-- 트레이스 확인
SELECT * FROM INFORMATION_SCHEMA.OPTIMIZER_TRACE\G

-- 끄기
SET SESSION optimizer_trace = 'enabled=off';
```

optimizer_trace 출력은 길고 복잡하지만, 핵심은 `considered_execution_plans` 섹션이다. 옵티마이저가 검토한 플랜과 각각의 `cost_info`를 보면 왜 특정 인덱스를 택했는지, 혹은 왜 인덱스를 버리고 풀스캔을 선택했는지를 알 수 있다.

## 인덱스가 안 쓰이는 세 가지 원인

EXPLAIN을 봤더니 `key: NULL`이다. 인덱스가 분명히 존재하는데 쓰이지 않는다. 난감한 상황이다. 원인은 크게 세 가지다.

**첫째, leftmost prefix rule 위반.** 복합 인덱스 `(status, created_at, amount)` 가 있다고 할 때, `WHERE created_at >= '2024-01-01'`만으로는 이 인덱스를 쓸 수 없다. 인덱스는 왼쪽 컬럼부터 순서대로 써야 한다. `status`를 먼저 걸어야 `created_at`을 이어서 쓸 수 있다. 4장에서 다뤘지만 인덱스 설계 실수 중 가장 흔한 패턴이라 여기서도 마주친다.

```sql
-- 인덱스 (status, created_at)가 있을 때

-- 이 쿼리는 인덱스를 쓴다 (leftmost prefix OK)
SELECT * FROM orders WHERE status = 'COMPLETED' AND created_at >= '2024-01-01';

-- 이 쿼리는 인덱스를 못 쓴다 (created_at만 조건에 있음)
SELECT * FROM orders WHERE created_at >= '2024-01-01';
```

**둘째, 컬럼에 함수를 적용한 경우.** 인덱스는 컬럼의 원래 값을 기준으로 만들어진다. 컬럼을 변환하면 인덱스를 쓸 수 없다.

```sql
-- 인덱스를 쓰지 못하는 패턴들
SELECT * FROM orders WHERE YEAR(created_at) = 2024;
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
SELECT * FROM orders WHERE LOWER(user_email) = 'user@example.com';

-- 대신 이렇게 — 컬럼에 함수 없이 범위 조건으로
SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

JPA를 쓰면서 JPQL에 `FUNCTION('YEAR', o.createdAt) = :year` 같은 표현을 넣는 경우를 종종 본다. 그럴 때 실제로 생성되는 SQL이 인덱스를 날리고 있는지 확인하는 편이 낫다.

**셋째, 옵티마이저의 cost 오추정.** 인덱스가 있고, leftmost prefix도 맞고, 함수도 없는데 여전히 인덱스를 안 쓰는 경우다. 옵티마이저가 "인덱스를 쓰는 것보다 풀스캔이 더 빠를 것"이라고 추정하는 상황이다. 이건 틀린 추정일 때도 있다. 통계가 부정확하거나, 인덱스 선택성(selectivity)을 옵티마이저가 잘못 파악할 때 발생한다. 앞서 말한 히스토그램 갱신을 먼저 시도하고, 그래도 나아지지 않으면 `USE INDEX`, `FORCE INDEX` 힌트를 단기 우회책으로 쓸 수 있다. 다만 이건 통계 문제를 근본적으로 해결하지 않는다는 점을 기억해두자.

```sql
-- 인덱스 힌트 (통계 문제가 해결되면 제거하는 편이 좋다)
SELECT * FROM orders USE INDEX (idx_status_created)
WHERE status = 'COMPLETED' AND created_at >= '2024-01-01';
```

## `Using filesort`와 `Using temporary` — 이 신호가 보이면

EXPLAIN의 Extra 컬럼에 `Using filesort`가 나왔다고 해서 무조건 성능이 나쁜 것은 아니다. 단지 MySQL이 결과를 정렬할 때 인덱스의 순서를 그대로 활용하지 못하고 별도의 정렬 작업을 했다는 뜻이다. 정렬 대상이 몇 천 건이라면 `Using filesort`가 있어도 빠를 수 있다.

`Using temporary`는 조금 더 주의를 기울여야 한다. 내부 임시 테이블을 만들어서 중간 결과를 쌓았다는 의미다. `GROUP BY`나 `DISTINCT`, 또는 `ORDER BY`가 들어간 쿼리에서 자주 나온다. 임시 테이블이 메모리 안에 들어가면 그나마 빠르지만, 결과가 커서 디스크 임시 테이블이 만들어지면 갑자기 느려진다.

이 둘이 함께 보이고 `actual time`이 크다면 어떻게 볼까. 대부분의 경우 두 가지를 점검한다.

하나, ORDER BY 컬럼이 인덱스 안에 있는가. ORDER BY에 사용되는 컬럼이 인덱스에 포함되어 있고, WHERE 조건이 그 인덱스를 통해 접근한다면 `Using filesort` 없이 정렬 결과를 낼 수 있다.

```sql
-- 인덱스 (status, created_at)가 있을 때
-- 이 쿼리는 정렬도 인덱스로 처리 가능 (extra: Using index condition)
SELECT id, amount FROM orders
WHERE status = 'COMPLETED'
ORDER BY created_at DESC
LIMIT 50;

-- 반면 이 쿼리는 정렬을 인덱스로 처리 못 함 (status로 걸러낸 뒤 amount로 정렬)
SELECT id, amount FROM orders
WHERE status = 'COMPLETED'
ORDER BY amount DESC
LIMIT 50;
```

둘, GROUP BY 컬럼이 인덱스에 있는가. MySQL은 GROUP BY 컬럼이 인덱스 순서와 일치하면 임시 테이블 없이 처리할 수 있다.

EXPLAIN ANALYZE의 트리에서 `Sort` 노드나 `Aggregate using temporary table` 노드가 안쪽에서 가장 시간을 많이 잡아먹고 있다면, 인덱스 재설계나 커버링 인덱스를 고민할 차례다.

## 커버링 인덱스로 back-to-table을 없애자

`Using index`가 EXPLAIN Extra에 보이면 기뻐할 일이다. 이것은 쿼리가 인덱스만으로 결과를 낼 수 있어서 테이블을 건드리지 않았다는 뜻, 즉 커버링 인덱스가 작동한 것이다.

세컨더리 인덱스는 PK 값을 포인터로 가지고 있다. 인덱스에서 조건에 맞는 PK를 찾고, 다시 그 PK로 테이블(클러스터링 인덱스)을 조회하는 것이 일반적인 흐름이다. 이것이 'back-to-table(또는 double lookup)'이라고도 부르는 과정이다. 조건에 맞는 행이 수백만 개라면 이 왕복 조회가 큰 부담이 된다.

SELECT하는 컬럼들이 인덱스 안에 모두 들어있다면 back-to-table이 필요 없다. 인덱스에서 조건 검색, 거기서 바로 값을 꺼내 반환.

```sql
-- 인덱스 (status, created_at, id) 가 있다면
-- id, created_at만 SELECT하는 이 쿼리는 커버링 인덱스로 처리 가능
-- Extra: Using index
SELECT id, created_at
FROM orders
WHERE status = 'COMPLETED'
  AND created_at >= '2024-01-01'
ORDER BY created_at DESC
LIMIT 50;

-- amount를 추가하면 인덱스에 없으므로 back-to-table 발생
SELECT id, created_at, amount
FROM orders
WHERE status = 'COMPLETED'
  AND created_at >= '2024-01-01'
ORDER BY created_at DESC
LIMIT 50;
```

페이지네이션을 구현할 때는 커버링 인덱스 + 지연 조인(deferred join) 기법을 시도해보자. 커버링 인덱스로 PK만 빠르게 찾은 뒤, 그 PK들에 대해서만 전체 컬럼 조회를 하는 방식이다.

```sql
-- 지연 조인으로 페이지네이션 최적화
SELECT o.id, o.amount, o.user_id, o.created_at
FROM orders o
INNER JOIN (
    SELECT id FROM orders
    WHERE status = 'COMPLETED'
      AND created_at >= '2024-01-01'
    ORDER BY created_at DESC
    LIMIT 50 OFFSET 10000  -- 깊은 페이지
) sub ON o.id = sub.id;
```

서브쿼리 부분은 커버링 인덱스로 빠르게 50개 ID를 찾고, 바깥 조인에서 그 50개에 대해서만 전체 컬럼 조회를 한다. OFFSET 페이지네이션 자체의 한계(깊어질수록 느려지는)는 9장에서 keyset pagination으로 더 근본적인 해법을 본다.

## 실제 슬로우 쿼리 분해 — 처음부터 끝까지

이제 실전 시나리오를 하나 따라가보자. velog에 올라온 슬로우 쿼리 개선 사례를 재구성해 본 것이다.

**상황:** 이벤트 목록 페이지가 갑자기 느려졌다. 쿼리는 이렇게 생겼다.

```sql
-- 문제의 쿼리 (실행 시간 약 6초)
SELECT p.id, p.title, p.discount_rate, po.option_name
FROM promotions p
LEFT JOIN promotion_options po ON p.id = po.promotion_id
WHERE p.is_active = 1
  AND p.end_date >= NOW()
ORDER BY p.created_at DESC
LIMIT 20;
```

**1단계: EXPLAIN ANALYZE 실행**

```sql
EXPLAIN ANALYZE
SELECT p.id, p.title, p.discount_rate, po.option_name
FROM promotions p
LEFT JOIN promotion_options po ON p.id = po.promotion_id
WHERE p.is_active = 1
  AND p.end_date >= NOW()
ORDER BY p.created_at DESC
LIMIT 20\G
```

결과(재구성):

```
-> Limit: 20 row(s)
   (actual time=6123.45..6123.52 rows=20 loops=1)
    -> Sort: p.created_at DESC
       (actual time=6123.23..6123.38 rows=20 loops=1)
        -> Filter: ((p.is_active = 1) and (p.end_date >= now()))
           (actual time=0.15..6120.78 rows=2340 loops=1)
            -> Left hash join (po.promotion_id = p.id)
               (actual time=0.14..5890.34 rows=125000 loops=1)
                -> Table scan on p
                   (cost=2345 rows=45000) (actual time=0.09..23.45 rows=45000 loops=1)
                -> Hash
                    -> Table scan on po
                       (cost=12340 rows=890000) (actual time=0.07..987.23 rows=890000 loops=1)
```

**2단계: 안쪽부터 읽기**

가장 안쪽 노드 두 개를 본다.

- `Table scan on p` — promotions 테이블 풀스캔, 45,000행, 23ms
- `Table scan on po` — promotion_options 테이블 풀스캔, 89만 행, 987ms

promotion_options가 89만 행 풀스캔이다. 여기서 시간이 상당히 간다. 그다음 `Left hash join`에서 두 테이블을 합치면서 125,000행이 되고, 이 처리에 5.8초를 쓴다.

**3단계: 인덱스 확인**

```sql
SHOW INDEX FROM promotion_options;
```

결과를 보니 promotion_options 테이블에는 `id`(PK) 인덱스만 있고 `promotion_id`에는 인덱스가 없다. JOIN 조건 `po.promotion_id = p.id`에서 `po.promotion_id`를 검색해야 하는데 인덱스가 없으니 매번 풀스캔이 일어난다.

**4단계: 인덱스 추가**

```sql
ALTER TABLE promotion_options
ADD INDEX idx_promotion_id (promotion_id);
```

**5단계: 다시 EXPLAIN ANALYZE**

```
-> Limit: 20 row(s)
   (actual time=0.45..0.52 rows=20 loops=1)
    -> Nested loop left join
       (actual time=0.43..0.50 rows=20 loops=1)
        -> Filter: ...
           (actual time=0.12..0.31 rows=20 loops=1)
            -> Index range scan on p using idx_active_enddate
               (actual time=0.09..0.24 rows=20 loops=1)
        -> Index lookup on po using idx_promotion_id (promotion_id=p.id)
           (actual time=0.008..0.009 rows=3 loops=20)
```

6초에서 0.5초로 줄었다. `Table scan on po`가 `Index lookup on po`로 바뀌었고, `Left hash join`이 `Nested loop left join`으로 바뀌었다.

**6단계: promotions 테이블의 인덱스도 확인**

0.5초도 여전히 빠르지는 않다. promotions 테이블의 `is_active`, `end_date`, `created_at` 컬럼에 인덱스가 있는지 확인해보자. `WHERE is_active = 1 AND end_date >= NOW()`로 걸러지는 비율이 높다면 복합 인덱스를 추가할 수 있다.

```sql
-- 복합 인덱스 추가
ALTER TABLE promotions
ADD INDEX idx_active_end_created (is_active, end_date, created_at);
```

이렇게 하면 `is_active = 1 AND end_date >= NOW()`를 인덱스로 처리하고, `ORDER BY created_at DESC`도 인덱스 순서를 따라갈 수 있다. 다시 EXPLAIN ANALYZE를 실행해서 `Using filesort`가 없어졌는지, actual time이 줄었는지 확인하자.

이 사이클 — **슬로우 쿼리 발견 → EXPLAIN ANALYZE로 분해 → 안쪽 노드부터 병목 찾기 → 인덱스/통계 수정 → 재검증** — 이 기본 패턴이다. 한 번 손에 익히면 어떤 쿼리 앞에서도 막히지 않는다.

## estimate와 actual이 크게 다를 때 — 다시 히스토그램으로

한 가지 더 보고 가자. 인덱스를 추가했는데도 여전히 느리고, EXPLAIN ANALYZE를 보니 `rows=500`으로 추정했는데 actual은 `rows=500000`이다. 이렇게 10배, 100배 차이가 나면 통계 문제다.

`status` 같은 컬럼이 이런 상황을 만들기 쉽다. `COMPLETED`, `PENDING`, `CANCELLED` 세 값이 있는데, 데이터의 99%가 `COMPLETED`다. 인덱스 통계만으로는 이 분포를 잘 담지 못할 수 있다.

```sql
-- 히스토그램 생성
ANALYZE TABLE orders UPDATE HISTOGRAM ON status WITH 3 BUCKETS;

-- 히스토그램 확인
SELECT * FROM INFORMATION_SCHEMA.COLUMN_STATISTICS
WHERE TABLE_NAME = 'orders' AND COLUMN_NAME = 'status'\G
```

히스토그램을 만들고 나면 옵티마이저가 `status = 'COMPLETED'`가 99%에 해당한다는 것을 알게 되어, 그 인덱스를 쓰는 것보다 풀스캔이 낫다고 판단하거나 반대로 더 적합한 인덱스를 선택하게 된다.

히스토그램은 인덱스와 달리 DML 성능에 영향을 주지 않는다. 읽기 전용 통계 테이블이기 때문에 자주 갱신해도 부담이 없다. 분포가 치우친 컬럼, 또는 카디널리티가 낮지만 특정 값이 집중된 컬럼에 히스토그램을 추가해두는 편이 낫다.

## 마무리

EXPLAIN ANALYZE는 쿼리 성능 문제의 진단 도구다. 핵심 절차를 정리해두자.

안쪽 노드부터 actual time과 actual rows를 확인하자. estimate와 actual의 차이가 크면 통계를 다시 갱신하거나 히스토그램을 만들어보자. 인덱스가 안 쓰인다면 leftmost prefix 위반, 함수 적용, cost 오추정 세 가지를 순서대로 의심한다. `Using filesort`나 `Using temporary`가 있고 실행 시간이 크다면 ORDER BY와 GROUP BY에 인덱스가 어떻게 걸려 있는지 다시 들여다보자.

진단 도구를 쓸 줄 아는 것과 실제로 쓰는 것 사이에는 습관의 차이가 있다. 슬로우 쿼리가 발생했을 때 바로 EXPLAIN ANALYZE를 실행하는 것을 팀의 기본 절차로 만들어두는 편이 낫다.

6장에서는 이렇게 진단하고 최적화한 쿼리를 SQL 자체의 표현력을 높이는 방향으로 가져가 본다. 윈도우 함수와 CTE로 애플리케이션 레이어에서 처리하던 집계 로직을 SQL 안으로 끌어올리는 방법을 같이 살펴보자.

## 참고 자료

- MySQL :: EXPLAIN ANALYZE 블로그 아카이브 — https://dev.mysql.com/blog-archive/mysql-explain-analyze/
- MySQL :: Histogram statistics in MySQL — https://dev.mysql.com/blog-archive/histogram-statistics-in-mysql/
- MySQL :: 10.9.6 Optimizer Statistics — https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html
- velog "EXPLAIN ANALYZE 해석법" — https://velog.io/@wisepine/MySQL-%EC%8A%AC%EB%A1%9C%EC%9A%B0%EC%BF%BC%EB%A6%AC-%EC%9E%A1%EB%8A%94-%EB%AA%85%EB%A0%B9%EC%96%B4-EXPLAIN-ANALIZE-%ED%95%B4%EC%84%9D%EB%B2%95
- velog "슬로우 쿼리 개선기" — https://velog.io/@bruni_23yong/%EC%8A%AC%EB%A1%9C%EC%9A%B0-%EC%BF%BC%EB%A6%AC-%EA%B0%9C%EC%84%A0%EA%B8%B0
- Alibaba Cloud — Analysis of MySQL Cost Estimator — https://www.alibabacloud.com/blog/analysis-of-mysql-cost-estimator_601201


# 6장. SQL의 표현력을 다시 끌어올리자 — 윈도우와 CTE

어느 날 기획팀에서 요청이 들어왔다. "상품별로 일별 매출과, 그 상품의 최근 7일 누적 매출을 같이 보여주는 화면이 필요해요." 개발자가 쿼리를 짜기 시작한다. 일별 집계는 GROUP BY로 하면 되는데, 7일 누적 합계는 어떻게 하지? 결국 Java 코드에서 결과를 받아다가 날짜 순서대로 반복문을 돌리면서 누적 합계를 계산한다. 쿼리 한 번, 자바 로직 한 번. 일단 동작은 한다.

그런데 이 방식에 찜찜함이 있다. 데이터가 늘어나면 자바 메모리에 얼마나 올라오는지 알 수 없고, 비슷한 집계 요청이 올 때마다 로직이 서비스 레이어에 쌓인다. 데이터를 가장 잘 아는 MySQL이 처리하면 될 일을 어플리케이션이 떠맡는 구조다.

MySQL 8.0은 이 상황을 바꿨다. 윈도우 함수와 CTE가 들어오면서, 애플리케이션에서 반복문으로 쌓던 집계 로직을 SQL 한 쿼리 안에서 표현할 수 있게 됐다. 어디까지 SQL로 할 수 있는지, 어디서 멈추는 게 맞는지를 같이 살펴보자.

## 윈도우 함수 — GROUP BY 없이 집계하기

윈도우 함수를 처음 접하면 개념이 낯설게 느껴진다. `GROUP BY`와 비슷한데 왜 따로 있는 걸까? 차이는 명확하다. `GROUP BY`는 행을 합쳐서 하나로 만드는 반면, 윈도우 함수는 행을 합치지 않고 원본 행을 유지하면서 집계 값을 곁에 붙여준다.

일별 주문 데이터에서 각 행 옆에 그 날의 주문 건수 합계를 붙이는 예를 보자.

```sql
-- GROUP BY는 날짜별로 행을 묶어버린다
SELECT order_date, COUNT(*) AS daily_count
FROM orders
GROUP BY order_date;

-- OVER()를 쓰면 원본 행을 유지하면서 집계 값을 옆에 붙인다
SELECT id, order_date, amount,
       COUNT(*) OVER (PARTITION BY order_date) AS daily_count
FROM orders;
```

`OVER (PARTITION BY order_date)`가 핵심이다. `PARTITION BY`는 GROUP BY처럼 그룹을 나누지만, 그룹으로 묶어버리지 않고 "이 그룹 안에서 집계 계산을 한다"는 의미다.

### ROW_NUMBER, RANK, DENSE_RANK

보고서에서 가장 자주 쓰이는 것들이다. 순위를 매길 때 쓴다.

```sql
-- 사용자별 최근 주문 1건씩 가져오기
SELECT *
FROM (
    SELECT id, user_id, amount, created_at,
           ROW_NUMBER() OVER (
               PARTITION BY user_id
               ORDER BY created_at DESC
           ) AS rn
    FROM orders
    WHERE status = 'COMPLETED'
) ranked
WHERE rn = 1;
```

`ROW_NUMBER()`는 같은 값이 있어도 무조건 다른 번호를 매긴다. 반면 `RANK()`는 같은 값에 같은 순위를 주고 다음 순위를 건너뛰고, `DENSE_RANK()`는 같은 값에 같은 순위를 주되 번호를 건너뛰지 않는다. 상황에 따라 골라 쓰자.

### LAG, LEAD — 앞뒤 행 참조

전일 대비 매출 증감을 구하려면 각 행에서 바로 이전 날의 값이 필요하다. 자바에서 처리하면 리스트를 정렬한 뒤 인덱스로 앞뒤를 참조해야 하는데, SQL에서는 `LAG`와 `LEAD`로 해결한다.

```sql
-- 일별 매출과 전일 대비 증감
SELECT
    order_date,
    daily_revenue,
    LAG(daily_revenue, 1) OVER (ORDER BY order_date) AS prev_day_revenue,
    daily_revenue - LAG(daily_revenue, 1, 0) OVER (ORDER BY order_date) AS revenue_diff
FROM (
    SELECT DATE(created_at) AS order_date,
           SUM(amount) AS daily_revenue
    FROM orders
    WHERE status = 'COMPLETED'
    GROUP BY DATE(created_at)
) daily
ORDER BY order_date;
```

`LAG(daily_revenue, 1, 0)` — 1행 앞의 값을 가져오되 앞이 없으면 0을 쓴다. `LEAD`는 반대로 뒤 행을 참조한다.

### SUM OVER — 누적 합계와 이동 평균

처음 예시에서 나온 7일 누적 매출이다. `ROWS BETWEEN` 구문으로 창(window) 범위를 정의한다.

```sql
-- 일별 매출과 7일 이동 합계
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg
FROM (
    SELECT DATE(created_at) AS order_date,
           SUM(amount) AS daily_revenue
    FROM orders
    WHERE status = 'COMPLETED'
    GROUP BY DATE(created_at)
) daily
ORDER BY order_date;
```

`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`는 현재 행을 포함해 앞 6개, 합쳐서 7개 행을 창으로 잡는다는 의미다. 누적 합계가 필요하면 `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`를 쓴다.

이 쿼리를 자바로 구현한다면? 결과 리스트를 받아 날짜 순서로 정렬, 인덱스 i에서 max(0, i-6)부터 i까지의 합계를 구하는 반복문. 쿼리에서 처리하면 MySQL이 최적화된 방식으로 처리하고 자바 메모리에는 최종 결과만 들어온다.

## CTE — 비재귀부터 시작하자

CTE(Common Table Expression)는 쿼리 안에 이름을 붙인 임시 결과 집합을 만드는 문법이다. `WITH` 절로 시작한다. 비재귀 CTE는 서브쿼리를 읽기 좋게 이름을 붙여 쓰는 것과 비슷한데, 실제로 얻는 이점이 있다.

```sql
-- 서브쿼리 방식 — 같은 서브쿼리가 두 번 나타나야 할 때 번거롭다
SELECT a.user_id, a.total, b.avg_amount
FROM (
    SELECT user_id, SUM(amount) AS total
    FROM orders WHERE status = 'COMPLETED'
    GROUP BY user_id
) a
JOIN (
    SELECT AVG(amount) AS avg_amount
    FROM orders WHERE status = 'COMPLETED'
) b;

-- CTE 방식 — 중간 결과에 이름을 붙여 재사용
WITH completed_orders AS (
    SELECT user_id, amount
    FROM orders
    WHERE status = 'COMPLETED'
),
user_totals AS (
    SELECT user_id, SUM(amount) AS total
    FROM completed_orders
    GROUP BY user_id
),
overall_avg AS (
    SELECT AVG(amount) AS avg_amount
    FROM completed_orders
)
SELECT t.user_id, t.total, a.avg_amount
FROM user_totals t
CROSS JOIN overall_avg a;
```

`completed_orders`를 한 번 정의하고 `user_totals`와 `overall_avg` 양쪽에서 참조했다. 서브쿼리라면 같은 내용을 두 번 써야 했을 것이다. 가독성이 높아지는 건 덤이고, 복잡한 쿼리를 단계별로 나눠 이해하고 검증할 수 있다는 것이 실용적인 이점이다.

MySQL의 비재귀 CTE는 옵티마이저가 내부적으로 뷰나 임시 테이블처럼 처리하는 경우가 있다. 같은 CTE를 여러 번 참조하면 결과를 임시 테이블에 저장해 재사용할 수 있다. 서브쿼리로는 이 재사용이 불가능하다.

## 재귀 CTE — 계층 데이터 탐색

재귀 CTE는 자기 자신을 참조하는 CTE다. 계층 구조 데이터(카테고리 트리, 조직도, 댓글 답글 구조)를 한 쿼리로 탐색할 수 있다.

```sql
-- 카테고리 테이블 (자기 참조)
-- categories: id, parent_id, name

-- 특정 카테고리의 모든 하위 카테고리를 재귀적으로 가져오기
WITH RECURSIVE category_tree AS (
    -- 앵커 부분: 시작점
    SELECT id, parent_id, name, 0 AS depth
    FROM categories
    WHERE id = 1  -- 루트 카테고리

    UNION ALL

    -- 재귀 부분: 앞에서 찾은 결과의 자식을 찾음
    SELECT c.id, c.parent_id, c.name, ct.depth + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT id, parent_id, name, depth
FROM category_tree
ORDER BY depth, id;
```

앵커 부분이 먼저 실행되어 id=1인 행이 들어오고, 재귀 부분이 그 행의 자식들을 찾고, 또 그 자식들의 자식을 찾는 과정을 반복한다. `depth`로 각 항목이 몇 단계 아래에 있는지 알 수 있다.

경로를 문자열로 누적하면 계층 구조의 전체 경로를 표현할 수도 있다.

```sql
WITH RECURSIVE category_path AS (
    SELECT id, name, CAST(name AS CHAR(1000)) AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name,
           CONCAT(cp.path, ' > ', c.name)
    FROM categories c
    INNER JOIN category_path cp ON c.parent_id = cp.id
)
SELECT id, name, path
FROM category_path;
```

### 재귀 CTE의 한계

재귀 CTE는 강력하다. 다만 조심해야 할 곳이 있다. 종료 조건이 없으면 무한 루프가 된다. MySQL은 `cte_max_recursion_depth` 변수로 기본 1000회로 제한하지만, 1000단계 깊이의 계층 트리가 있다면 이 제한에 걸린다.

더 중요한 것은 규모다. Egnyte의 사례를 보면 수십만 노드의 파일 시스템 트리를 재귀 CTE로 탐색했을 때 성능이 크게 떨어졌다. 깊이는 적당해도 너무 넓은 트리나, 수백만 건이 얽힌 그래프는 재귀 CTE로 처리하기 어렵다.

재귀 CTE가 잘 맞는 경우: 계층 깊이가 10~20단계 이하, 노드 수가 수만 이하. 그 이상이라면 계층 경로를 materialized path 패턴(`/1/2/5/` 같은 경로 문자열을 컬럼으로 저장)으로 저장하거나, 별도 계층 테이블을 관리하는 편이 낫다.

## 윈도우 함수 + CTE로 복합 보고서 작성하기

윈도우 함수와 CTE를 같이 쓰면 어떤 그림이 나올까. 보고서 쿼리에서 자주 보이는 패턴 하나를 따라가보자. 상품 카테고리별로 일별 매출을 집계하고, 각 카테고리 안에서 매출 순위를 매기는 쿼리다.

```sql
WITH daily_sales AS (
    SELECT
        p.category_id,
        DATE(o.created_at) AS order_date,
        SUM(oi.amount) AS daily_revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'COMPLETED'
      AND o.created_at >= '2024-01-01'
    GROUP BY p.category_id, DATE(o.created_at)
),
ranked_sales AS (
    SELECT
        category_id,
        order_date,
        daily_revenue,
        RANK() OVER (
            PARTITION BY category_id
            ORDER BY daily_revenue DESC
        ) AS revenue_rank,
        SUM(daily_revenue) OVER (
            PARTITION BY category_id
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue
    FROM daily_sales
)
SELECT *
FROM ranked_sales
WHERE revenue_rank <= 10  -- 카테고리별 매출 상위 10일
ORDER BY category_id, revenue_rank;
```

`daily_sales`에서 집계하고, `ranked_sales`에서 윈도우 함수를 적용해 순위와 누적 합계를 구한다. 마지막에 `WHERE revenue_rank <= 10`으로 각 카테고리에서 매출 상위 10일만 필터링한다.

윈도우 함수는 WHERE 절보다 나중에 실행된다는 점을 기억해두자. 그래서 윈도우 함수 결과로 필터링하려면 CTE나 서브쿼리로 한 번 감싸야 한다. `WHERE revenue_rank <= 10`을 직접 윈도우 함수와 같은 SELECT 수준에 쓰면 오류가 난다.

## 어디서 SQL로, 어디서 애플리케이션으로

윈도우 함수와 CTE로 꽤 많은 것을 SQL 안에서 처리할 수 있다는 걸 알았다. 그렇다면 항상 SQL에서 처리하는 것이 좋을까? 꼭 그렇지는 않다.

SQL에서 처리하는 편이 자연스러운 경우는 이렇다. 집계, 순위, 누적 합계처럼 데이터 전체나 그룹을 한 번에 봐야 하는 연산. 결과를 필터링하기 전에 계산이 먼저 필요한 경우(윈도우 함수는 WHERE보다 나중에 실행되니까). 정렬된 순서에 의존하는 연산(LAG/LEAD, 이동 평균). 네트워크를 통해 수십만 행을 옮기지 않아도 되는 경우.

그렇다면 반대편은 어떤 경우일까. 도메인 로직이 복잡하고 단위 테스트가 필요한 경우라면 애플리케이션 쪽이 더 명료하다. 여러 마이크로서비스의 데이터를 합쳐야 한다면 SQL 한쪽으로 몰 수 없다. SQL로 표현했을 때 지나치게 복잡해져 유지보수가 어려워진다면 애플리케이션이 떠맡는 편이 낫다.

기준은 결국 "DB가 더 잘 아는 일인가, 아니면 애플리케이션이 더 잘 아는 일인가"다. 집계와 순위는 DB가 잘 안다. 비즈니스 규칙 기반의 복잡한 계산은 애플리케이션이 자기 영역이다. 어느 한쪽이 항상 옳은 것이 아니라, 구조를 보고 판단해보자.

## 마무리

윈도우 함수(`ROW_NUMBER`, `LAG/LEAD`, `SUM OVER`)와 CTE(`WITH`, `WITH RECURSIVE`)는 8.0 이후 MySQL이 내놓은 가장 실용적인 기능들이다. 이걸 모르면 자바 코드에 쌓아두게 되는 집계 로직이, 이걸 알면 SQL 한 쿼리 안으로 들어온다.

다음 7장에서는 JSON 타입으로 넘어간다. 관계형 스키마로 표현하기 어려운 데이터를 JSON 컬럼에 넣었을 때 어떻게 인덱싱하고 조회하는지, 그리고 언제 JSON을 쓰고 언제 정규화 테이블을 쓰는지의 경계선을 같이 그어보자.

## 참고 자료

- MySQL :: 15.2.20 WITH (Common Table Expressions) — https://dev.mysql.com/doc/refman/8.0/en/with.html
- Percona — Introduction to MySQL 8.0 Recursive CTE (Part 2) — https://www.percona.com/blog/introduction-to-mysql-8-0-recursive-common-table-expression-part-2/
- Egnyte — Evaluating MySQL Recursive CTE at scale — https://www.egnyte.com/blog/post/12780evaluating-mysql-recursive-cte-at-scale/


# 7장. JSON 데이터 모델링과 인덱싱

상품 상세 정보를 저장한다고 해보자. 의류는 색상, 사이즈, 소재가 있고, 전자제품은 해상도, 배터리 용량, 운영체제 버전이 있고, 식품은 원산지, 알레르기 성분, 영양 성분이 있다. 카테고리마다 속성이 다르다. 관계형 테이블로 다 잡으려면 모든 카테고리의 속성을 합친 거대한 테이블을 만들어야 하거나, 속성 이름과 값을 행으로 저장하는 EAV(Entity-Attribute-Value) 패턴을 써야 하는데 이것도 번거롭긴 마찬가지다.

이때 JSON 컬럼이 매력적으로 보인다. `attributes` 컬럼 하나에 카테고리마다 다른 속성들을 자유롭게 담는 것이다. 문제는 "그래서 이 JSON 컬럼에서 특정 값을 빠르게 찾을 수 있느냐"다.

MySQL 8.0은 이 문제에 구체적인 답을 내놓았다.

## JSON 타입과 기본 사용법

MySQL 5.7부터 JSON이 네이티브 타입으로 들어왔다. 텍스트 컬럼에 JSON 문자열을 저장하는 것과는 다르다. JSON 타입으로 저장하면 MySQL이 파싱해서 최적화된 내부 이진 형식으로 보관한다. 덕분에 JSON 문서 안의 특정 경로를 직접 접근하는 것이 빠르고, 저장 시 문법 유효성 검사도 자동으로 된다.

```sql
-- JSON 컬럼을 포함한 테이블 생성
CREATE TABLE products (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INT NOT NULL,
    attributes JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- JSON 데이터 삽입
INSERT INTO products (name, category_id, attributes) VALUES
('청바지 스키니핏', 1,
 '{"color": "dark_blue", "sizes": ["S", "M", "L", "XL"], "material": "cotton_96"}'),
('갤럭시 S24', 2,
 '{"storage": 256, "ram": 8, "os": "Android14", "battery_mAh": 4000}');
```

### JSON_EXTRACT와 `->>` 연산자

JSON 안의 값을 꺼내는 방법이 여럿 있다.

```sql
-- JSON_EXTRACT 함수: JSON 경로로 값 추출
SELECT name,
       JSON_EXTRACT(attributes, '$.color') AS color,
       JSON_EXTRACT(attributes, '$.storage') AS storage
FROM products;

-- ->> 연산자: JSON_UNQUOTE(JSON_EXTRACT()) 의 짧은 표현
-- 문자열 값에서 따옴표를 제거해 순수 값으로 반환
SELECT name,
       attributes->>'$.color' AS color,
       attributes->>'$.storage' AS storage
FROM products;

-- 배열 인덱스로 접근
SELECT name, attributes->>'$.sizes[0]' AS first_size
FROM products
WHERE category_id = 1;

-- 조건 검색
SELECT * FROM products
WHERE attributes->>'$.storage' = '256';
```

`->`는 JSON 경로로 값을 추출하되 따옴표가 붙고, `->>`는 따옴표를 제거한 순수 값을 반환한다. 숫자를 다룰 때는 `->>`를 쓰는 편이 낫다. 그렇지 않으면 `"256"` 같은 따옴표 달린 문자열로 반환되어 비교가 찜찜해진다.

### JSON_TABLE로 JSON을 관계형으로 펼치기

JSON 안의 배열 데이터를 행으로 펼쳐서 일반 테이블처럼 다루고 싶을 때가 있다.

```sql
-- JSON 배열을 행으로 변환
SELECT p.name, sizes.size
FROM products p,
JSON_TABLE(
    p.attributes,
    '$.sizes[*]' COLUMNS (
        size VARCHAR(10) PATH '$'
    )
) AS sizes
WHERE p.category_id = 1;
```

결과는 `청바지 스키니핏 | S`, `청바지 스키니핏 | M` 같이 배열 요소마다 한 행으로 펼쳐진다. JSON_TABLE을 쓰면 JSON 데이터를 관계형 JOIN이나 GROUP BY와 함께 쓸 수 있다. 다만 내부적으로 임시 테이블을 만드는 방식이라 대용량에서는 부담이 될 수 있다.

## JSON 인덱싱 — 5.7초에서 280ms로

JSON 컬럼 자체에는 인덱스를 직접 걸 수 없다. `CREATE INDEX idx ON products (attributes)` 같은 것은 허용되지 않는다. JSON 문서 전체에 B+Tree 인덱스를 만드는 것 자체가 말이 안 되기 때문이다.

대신 JSON 안의 특정 경로 값을 인덱싱하는 방법이 있다.

### MySQL 5.7 방식: 생성 컬럼 + 세컨더리 인덱스

```sql
-- generated column으로 JSON 경로를 일반 컬럼으로 추출
ALTER TABLE products
ADD COLUMN storage_gb INT GENERATED ALWAYS AS
    (CAST(attributes->>'$.storage' AS UNSIGNED)) VIRTUAL;

-- 그 generated column에 인덱스 생성
ALTER TABLE products
ADD INDEX idx_storage (storage_gb);

-- 이제 이 쿼리가 인덱스를 탄다
SELECT * FROM products WHERE storage_gb = 256;
-- 또는 JSON 경로 조건도 MySQL이 자동으로 인덱스 활용
SELECT * FROM products WHERE attributes->>'$.storage' = '256';
```

VIRTUAL 생성 컬럼은 디스크에 값을 저장하지 않고 조회 시점에 계산한다. 인덱스는 그 계산된 값을 기반으로 만들어진다. 이 방식이 MySQL 5.7에서의 우회 패턴이었다.

### MySQL 8.0.13 이상: 함수형 인덱스

8.0.13부터는 생성 컬럼 없이 바로 인덱스를 정의할 수 있다. 내부적으로는 같은 원리지만 테이블 구조를 건드리지 않아도 된다.

```sql
-- 8.0.13+ 함수형 인덱스
ALTER TABLE products
ADD INDEX idx_storage ((CAST(attributes->>'$.storage' AS UNSIGNED)));
```

```sql
-- EXPLAIN으로 인덱스 활용 확인
EXPLAIN SELECT * FROM products
WHERE (CAST(attributes->>'$.storage' AS UNSIGNED)) = 256;
```

`EXPLAIN`에서 `key: idx_storage`가 보이면 인덱스를 타고 있는 것이다.

1mg(인도 헬스케어 플랫폼)의 사례가 이 효과를 잘 보여준다. 의약품 데이터의 특정 속성을 JSON 컬럼에 저장하고 있었는데, 그 속성으로 검색하는 쿼리가 5.7초가 걸렸다. VIRTUAL 생성 컬럼에 세컨더리 인덱스를 추가한 결과 280ms로 줄었다. 약 20배 개선이다. 8.0.21 이후라면 함수형 인덱스로 같은 효과를 생성 컬럼 없이 낼 수 있다.

여기서 핵심은 JSON 경로와 인덱스 정의의 표현식이 정확히 일치해야 한다는 것이다. `attributes->>'$.storage'`와 `JSON_EXTRACT(attributes, '$.storage')`는 같은 값이지만 인덱스가 어떤 표현식으로 정의됐는지에 따라 둘 중 하나만 인덱스를 탄다. EXPLAIN으로 확인해두는 편이 낫다.

## JSON vs 정규화 — 경계선은 어디인가

JSON 컬럼을 쓰자, 아니다 정규화 테이블이 낫다 — 팀 안에서 한 번쯤 부딪히는 논쟁이다. 정해진 답은 없지만 판단 기준은 있다.

JSON이 어울리는 상황부터 보자. 속성이 카테고리마다 크게 다르고 공통 스키마를 강제하기 어려운 경우. 속성이 자주 바뀌거나 신규 속성 추가가 빈번한 경우(스키마 변경 없이 새 키를 더할 수 있다). 검색·정렬·집계 대상이 되는 속성이 전체의 일부에 불과한 경우(그 속성만 인덱싱해두면 된다). 또는 사용자 설정, 이벤트 메타데이터처럼 문서 지향적인 데이터.

반면 정규화 테이블이 어울리는 상황은 다르다. 해당 컬럼을 기준으로 자주 JOIN하고 집계하고 필터링해야 할 때. 데이터 정합성이 중요하고 FK 제약이나 NOT NULL 제약이 필요할 때. 모든 행이 같은 속성 구조를 가질 때. 이런 데이터라면 JSON에 담을 이유가 없다.

```sql
-- 이렇게 자주 조인하고 집계한다면 정규화 테이블이 낫다
SELECT s.name, COUNT(*) AS product_count
FROM products p
JOIN product_specifications ps ON p.id = ps.product_id
JOIN specifications s ON ps.spec_id = s.id
GROUP BY s.name;

-- JSON으로는 이런 쿼리가 쉽지 않다
SELECT attributes->>'$.color' AS color, COUNT(*)
FROM products
GROUP BY attributes->>'$.color';
-- 이것도 가능하지만 인덱스를 타지 않아 전체 스캔이다
```

하이브리드 접근도 흔하다. 모든 상품에 공통인 속성(이름, 카테고리, 가격, 재고)은 정규화 컬럼으로, 카테고리마다 다른 세부 속성은 JSON 컬럼으로. 자주 검색되는 JSON 속성에만 함수형 인덱스를 추가한다. 이렇게 하면 스키마 유연성과 인덱싱 성능을 같이 챙길 수 있다.

## 마무리

JSON 타입은 관계형 모델의 경직성을 보완하는 도구다. 하지만 도구에는 적합한 용도가 있다. JSON 컬럼에 저장한 데이터를 자주 검색한다면 함수형 인덱스를 추가하는 편이 낫고, 정의한 표현식과 쿼리의 표현식이 정확히 일치해야 인덱스를 탄다는 것을 기억해두자. JSON을 쓸지 정규화를 쓸지의 판단 기준은 "이 데이터를 어떻게 조회하고 필터링할 것인가"에서 나온다.

8장에서는 도메인 모델링과 스키마 설계가 만나는 지점을 본다. DDD의 애그리거트를 테이블로 옮길 때 PK 전략, soft delete, 이력 관리, FK 경계에서 어떤 트레이드오프가 생기는지를 함께 살펴보자.

## 참고 자료

- MySQL :: 13.5 The JSON Data Type — https://dev.mysql.com/doc/refman/8.0/en/json.html
- MySQL :: 15.1.20.9 Secondary Indexes and Generated Columns — https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html
- MySQL :: Indexing JSON documents via Virtual Columns — https://dev.mysql.com/blog-archive/indexing-json-documents-via-virtual-columns/
- Vlad Mihalcea — Index JSON columns in MySQL — https://vladmihalcea.com/index-json-columns-mysql/
- Medium "1mg JSON support virtual columns and indexing" — https://medium.com/1mgofficial/mysql-json-support-virtual-columns-and-indexing-json-31df4cc1aa31


# 8장. 도메인 모델링과 스키마 설계의 만남

도메인 주도 설계(DDD) 책을 읽고 애그리거트를 잘 정의했다. Order, OrderItem, Customer가 있고 Order 안에 OrderItem들이 들어있는 구조다. 그런데 막상 테이블을 만들려고 하면 질문들이 쌓인다. Order와 OrderItem은 다른 테이블인데, PK는 어떻게 잡아야 할까? 삭제된 주문은 테이블에서 지워야 하나, 아니면 `deleted_at` 컬럼을 두어야 하나? 외래 키 제약은 어디까지 걸어야 하나? UUID를 써도 성능이 괜찮을까?

이런 질문은 도메인 모델링과 InnoDB 물리 구조가 만나는 접점에서 나온다. 둘을 따로 보면 각각은 명확한데, 함께 놓으면 트레이드오프가 생긴다. 그 트레이드오프를 같이 살펴보자.

## 애그리거트와 InnoDB 클러스터링 인덱스를 같은 그림에서 보기

DDD에서 애그리거트(Aggregate)는 하나의 일관성 경계다. Order 애그리거트 안에 OrderItem들이 있고, 이 경계 안의 데이터는 항상 일관성 있게 유지된다. 외부에서는 Order라는 루트를 통해서만 내부를 변경할 수 있다.

InnoDB에서는 PK가 클러스터링 인덱스다. 즉, 테이블의 데이터 자체가 PK 순서로 B+Tree에 저장된다. 같은 PK 범위에 있는 행들은 물리적으로 가까운 디스크 페이지에 있다.

이 두 가지를 연결하면 흥미로운 인사이트가 나온다. 애그리거트의 하위 항목들이 물리적으로 가까이 있으면 한 번의 디스크 IO로 많이 읽어올 수 있다.

```sql
-- OrderItem의 PK를 order_id를 포함한 복합 키로 잡으면
-- 같은 주문의 아이템들이 order_id 범위 안에 모인다
CREATE TABLE order_items (
    order_id    BIGINT UNSIGNED NOT NULL,
    item_seq    INT UNSIGNED NOT NULL,   -- 주문 안에서의 순번
    product_id  BIGINT UNSIGNED NOT NULL,
    quantity    INT NOT NULL,
    unit_price  DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (order_id, item_seq),    -- 복합 PK
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

이렇게 하면 `WHERE order_id = ?`로 특정 주문의 아이템을 조회할 때 클러스터링 인덱스 범위 스캔이 일어나고, 관련 행들이 같은 페이지나 인접 페이지에 있으므로 IO가 효율적이다.

반면 auto_increment PK를 단독으로 쓰면 아이템들이 삽입 순서대로 흩어진다. 주문 A의 아이템 1이 page 100에, 주문 B의 아이템 2가 page 101에, 주문 A의 아이템 2가 page 200에 있을 수 있다. `JOIN`으로 주문과 아이템을 같이 조회할 때 여러 페이지를 오가게 된다.

애그리거트 패턴과 InnoDB 클러스터링을 맞추는 것이 항상 가능하지는 않다. 하지만 "하위 엔티티의 PK에 상위 ID를 포함할 수 있는가"를 한 번 검토해보는 것은 가치 있다.

## PK 전략 — auto_increment, UUID, Snowflake

PK 선택은 생각보다 영향이 넓다. 클러스터링 인덱스이기 때문에 삽입 패턴, 조회 패턴, 심지어 배치 처리(10장에서 다룬다)에도 영향을 준다.

### auto_increment — 단순하고 효율적이지만 노출이 찜찜하다

가장 단순한 선택이다. 순차적으로 증가하므로 클러스터링 인덱스의 페이지 분할이 최소화되고, 삽입이 효율적이다.

```sql
CREATE TABLE orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(14,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

단점은 두 가지다. 첫째, 숫자가 외부에 노출되면 총 주문 수를 추정할 수 있고, 순차적인 ID로 크롤링이 쉬워진다. `/api/orders/1`, `/api/orders/2` 패턴은 인증이 없으면 바로 취약점이 된다. 둘째, 분산 환경(샤딩)에서 여러 인스턴스가 중복 없는 ID를 생성하려면 별도 조율이 필요하다.

### UUID v4 — 분산에는 좋지만 클러스터링이 나빠진다

UUID는 전역적으로 유일하고 외부 예측이 불가능하다.

```sql
CREATE TABLE orders (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    -- 또는 BINARY(16)으로 저장하면 크기를 절반으로 줄임
    ...
);
```

문제는 무작위 값이 PK 클러스터링 인덱스에 들어갈 때다. 새 행이 B+Tree의 임의 위치에 삽입되면서 페이지 분할이 자주 일어난다. 기존 페이지를 반으로 쪼개고 데이터를 재분배하는 과정이 삽입마다 반복될 수 있다. 삽입이 많은 테이블에서는 이 비용이 눈에 띈다. 또한 UUID 문자열이 36바이트라서 세컨더리 인덱스마다 36바이트짜리 포인터가 달린다.

UUID를 써야 한다면 `BINARY(16)`으로 저장해 크기를 줄이는 것과, MySQL 8.0이 지원하는 UUID v1(시간 기반, 단조 증가 성질이 있어 순차 삽입에 가깝다)을 고려해보자. `UUID_TO_BIN(UUID(), 1)` — 두 번째 인수 `1`은 타임스탬프 바이트를 앞으로 이동시켜 순차 삽입 최적화를 한다.

```sql
CREATE TABLE orders (
    id BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID(), 1)),
    PRIMARY KEY (id)
);

-- 조회 시 UUID 문자열로 변환
SELECT BIN_TO_UUID(id, 1) AS id_str, * FROM orders WHERE id = UUID_TO_BIN('...', 1);
```

### Snowflake 스타일 — 순차 + 분산

트위터가 만든 Snowflake ID는 타임스탬프 + 워커 ID + 시퀀스를 조합한 64비트 정수다. 시간 순으로 증가하므로 클러스터링 인덱스에 유리하고, 워커 ID로 여러 노드가 충돌 없이 ID를 생성할 수 있다. 분산 환경에서 auto_increment의 한계를 넘으면서도 B+Tree 효율을 유지하는 방법이다.

Java 생태계에서는 Twitter Snowflake와 호환되는 라이브러리가 여럿 있고, Spring Boot 프로젝트에서 ID 생성기로 쓸 수 있다.

```java
// Snowflake ID 생성 예시 (개념 코드)
@Component
public class SnowflakeIdGenerator {
    private final long workerId;
    private long sequence = 0;
    private long lastTimestamp = -1;

    // 41비트 타임스탬프 + 10비트 워커 ID + 12비트 시퀀스
    // 실제 구현은 라이브러리를 활용하는 편이 낫다
}
```

**PK 선택 기준 요약:**
- 단일 DB, 노출 무방 → auto_increment BIGINT
- 외부 노출 금지, 단일 DB → auto_increment + 외부 식별자 별도 (UUID or opaque token)
- 분산 DB, 클러스터링 효율 필요 → Snowflake
- 진정한 글로벌 분산 + 충돌 불가 → UUID v4 (클러스터링 비용 감수)

## Soft Delete 논쟁 — brandur vs Brent Ozar

주문이 취소됐다. 데이터를 어떻게 처리해야 할까? 행을 그냥 DELETE하면 간단하지만 이력이 사라진다. 그래서 많은 팀이 `deleted_at DATETIME NULL` 컬럼을 두고, 삭제할 때 실제로 지우지 않고 `deleted_at = NOW()`로 표시하는 방식을 택한다. 이것이 소프트 딜리트(soft delete)다.

개념은 명쾌한데 구현이 번거롭다. brandur.org는 소프트 딜리트가 "거의 가치 없다"고 단호하게 주장한다. 이유는 명확하다.

첫째, `WHERE deleted_at IS NULL`을 모든 쿼리에 끼워야 한다. 하나라도 빠지면 삭제된 데이터가 조회에 노출된다. 10개 테이블이 있으면 10개 테이블의 모든 쿼리에 이 조건이 들어가야 한다. JPA에서는 `@Where(clause = "deleted_at IS NULL")` 애노테이션으로 자동 적용할 수 있지만, native SQL이나 보고서 쿼리에는 직접 붙여야 한다.

둘째, UNIQUE 제약이 망가진다. MySQL에는 partial unique index가 없다. `email` 컬럼에 UNIQUE 제약을 걸었는데 같은 이메일이 soft delete 됐다가 다시 가입하면 중복 오류가 난다.

```sql
-- 이것은 MySQL에서 지원 안 됨 (partial unique index)
CREATE UNIQUE INDEX idx_email_active
ON users (email) WHERE deleted_at IS NULL;

-- 우회책: 함수 기반 인덱스 (MySQL 8.0.13+)
-- deleted_at이 NULL이면 email, NULL이 아니면 NULL을 인덱싱
CREATE UNIQUE INDEX idx_email_not_deleted
ON users ((CASE WHEN deleted_at IS NULL THEN email ELSE NULL END));
```

셋째, FK 관계가 복잡해진다. orders가 user를 참조하는데 user가 soft delete됐다면, orders는 존재하지 않는 user를 가리킨다. FK 제약은 통과하지만 논리적으로 이상한 상태다.

반면 Brent Ozar는 "감사(audit)나 복원이 필요한 도메인에서는 소프트 딜리트가 유효하다"는 입장이다. 금융 거래, 의료 기록 같은 데이터는 법적으로 보관 의무가 있고, 실수로 삭제한 데이터를 복원해야 하는 경우도 있다.

**절충점은 이렇다.** 소프트 딜리트의 이유가 "이력 보관"이라면, 차라리 이력 테이블을 별도로 두는 편이 낫다.

```sql
-- 실제 삭제 + 이력 테이블 패턴
CREATE TABLE orders_history (
    id              BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED,
    status          VARCHAR(20),
    total_amount    DECIMAL(14,2),
    created_at      DATETIME,
    deleted_at      DATETIME NOT NULL,
    deleted_by      BIGINT UNSIGNED,       -- 누가 삭제했는지
    deletion_reason VARCHAR(500),
    PRIMARY KEY (id, deleted_at)
);

-- 삭제 전 이력으로 복사 후 실제 삭제하는 트리거 또는 서비스 레이어
```

이렇게 하면 `orders` 테이블의 모든 쿼리는 `WHERE deleted_at IS NULL` 없이 작성할 수 있고, UNIQUE 제약도 온전히 작동한다. 이력이 필요하면 `orders_history`를 보면 된다.

소프트 딜리트를 유지해야 한다면, 테이블 전체를 소프트 딜리트로 다루기보다 "활성 상태"를 별도 뷰나 파티션으로 분리해 일반 쿼리가 소프트 딜리트 레코드를 자동으로 보지 않게 하는 방법도 고려해볼 만하다.

## 이력 테이블과 audit log

소프트 딜리트 이야기에서 자연스럽게 이어진다. 도메인 이벤트를 어디에, 어떻게 저장할 것인가.

이력 테이블 패턴은 변경이 일어날 때마다 이전 상태를 별도 테이블에 복사해두는 방식이다. 위의 `orders_history` 같은 것이다.

audit log는 더 일반적인 형태로, 엔티티, 변경 유형(INSERT/UPDATE/DELETE), 변경 전/후 값, 변경자, 시각을 기록한다. JPA의 `@EntityListeners(AuditingEntityListener.class)`로 간단한 audit log를 구현할 수 있다.

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Order {
    @Id
    private Long id;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @CreatedBy
    private Long createdBy;

    @LastModifiedBy
    private Long updatedBy;
}
```

더 세밀한 필드 수준의 변경 이력이 필요하다면 Envers(Hibernate Audit)를 쓰면 된다. Envers는 엔티티 변경마다 자동으로 revision 테이블에 이전 상태를 기록한다.

DDD 관점에서는 도메인 이벤트를 이벤트 소싱 패턴으로 저장하는 방법도 있다. `OrderCreated`, `OrderCancelled` 같은 이벤트를 직렬화해 이벤트 저장소에 쌓는 것이다. 이 방향은 이 책의 범위를 벗어나지만, 이력 보관이 핵심 요구사항이라면 탐색해볼 만하다.

## 캐릭터셋과 콜레이션 — utf8mb4_0900_ai_ci와 NO PAD

작은 것처럼 보이지만 나중에 큰 문제가 되는 부분이다. MySQL 5.7에서 8.0으로 마이그레이션할 때 특히 주의하자.

MySQL의 `utf8`은 실제로 최대 3바이트 UTF-8이었다. 이모지 같은 4바이트 문자(보충 문자, supplementary characters)를 저장하지 못한다. `utf8mb4`가 진짜 UTF-8이고, 이 차이 때문에 이모지를 저장하려다 `Incorrect string value` 오류를 본 팀이 많다. 8.0 이후 신규 테이블은 `utf8mb4`를 쓰는 편이 낫다.

콜레이션(collation)은 문자열 비교와 정렬 방식을 결정한다. 8.0의 기본 콜레이션은 `utf8mb4_0900_ai_ci`다. `ai`는 Accent-Insensitive(악센트 무시), `ci`는 Case-Insensitive(대소문자 무시)를 의미한다. `café`와 `cafe`가 같은 값으로 비교된다.

5.7에서 마이그레이션할 때 한 가지 짚고 가자. 8.0의 `utf8mb4_0900_ai_ci`는 NO PAD 동작을 한다. 5.7의 `utf8mb4_unicode_ci`는 PAD SPACE 동작이다. 이 차이는 문자열 끝의 공백 처리에서 나타난다.

```sql
-- PAD SPACE 방식 (5.7 기본): 'a' = 'a ' → TRUE (공백 채워서 같다고 봄)
-- NO PAD 방식 (8.0 기본): 'a' = 'a ' → FALSE (공백도 의미 있음)

-- 5.7에서 이 쿼리는 아무것도 반환하지 않았는데
-- 8.0에서는 반환할 수 있다 (또는 반대)
SELECT * FROM users WHERE username = 'admin ';  -- 끝에 공백 있음
```

마이그레이션 시 `SHOW CREATE TABLE`로 각 테이블의 캐릭터셋과 콜레이션을 확인하고, 의도치 않은 동작 변화가 없는지 주요 쿼리를 검토해두는 편이 낫다. 5.7 호환성이 필요한 컬럼은 명시적으로 `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`로 지정해두면 된다.

```sql
-- 8.0에서 5.7 콜레이션을 명시적으로 쓰는 경우
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci  -- PAD SPACE 방식, 5.7 호환
        NOT NULL,
    email VARCHAR(200)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_0900_ai_ci  -- NO PAD 방식, 8.0 기본
        NOT NULL
);
```

## FK를 어디까지 둘 것인가 — 8.4 변화의 무게

외래 키(Foreign Key, FK) 제약은 데이터 정합성을 DB 레벨에서 강제한다. `orders.user_id`가 존재하지 않는 user를 가리키는 상황을 막아준다.

그렇다면 항상 FK를 걸어야 할까? 팀마다 입장이 갈린다.

**FK를 적극 사용하는 입장:**
- DB 레벨에서 정합성 보장 — 애플리케이션 버그로 고립된(orphan) 데이터가 생기지 않는다
- 관계를 명시해 스키마 자체가 문서 역할을 한다
- ON DELETE CASCADE, ON UPDATE CASCADE로 연쇄 처리를 자동화할 수 있다

**FK를 줄이거나 없애는 입장:**
- 마이크로서비스 환경에서 다른 서비스의 테이블을 참조하는 FK는 만들 수 없다
- 대용량 데이터 마이그레이션이나 배치 INSERT에서 FK 체크가 성능 부담이 된다
- 샤딩 환경에서는 다른 샤드의 데이터를 참조하는 FK가 불가능하다

MySQL 8.4에서 FK 관련 동작이 더 엄격해졌다. 8.4에서는 FK 제약이 부모 테이블의 정확히 일치하는 UNIQUE KEY를 요구한다. 이전에는 UNIQUE INDEX면 됐는데 이제는 UNIQUE KEY 제약이어야 한다. Skeema가 "Five Surprises"에서 이 변화를 강조한 이유다.

```sql
-- 8.4에서 이런 상황은 FK 생성 실패
CREATE TABLE categories (
    id INT,
    name VARCHAR(100)
);
CREATE UNIQUE INDEX idx_id ON categories (id);  -- UNIQUE INDEX, KEY 제약 아님

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories (id)  -- 8.4에서 오류 가능
);

-- 대신 UNIQUE KEY 제약으로 명시
ALTER TABLE categories ADD UNIQUE KEY uq_id (id);
-- 또는 PK를 명시
ALTER TABLE categories ADD PRIMARY KEY (id);
```

실무적인 접근법은 이렇다. 같은 DB, 같은 스키마 안의 테이블 관계에는 FK를 둔다. 정합성이 중요하고 성능 비용이 수용 가능한 범위다. 마이크로서비스 경계를 넘는 참조나 샤딩된 데이터 사이의 참조에는 FK를 두지 않고 애플리케이션 레이어에서 정합성을 관리하자.

FK를 안 두기로 했다면, 적어도 외래 키 역할을 하는 컬럼에는 인덱스를 명시적으로 만들어두는 편이 낫다. FK가 있으면 MySQL이 자동으로 인덱스를 만들어주지만, FK가 없으면 만들어주지 않는다. `orders.user_id`에 인덱스가 없으면 user를 삭제할 때 (또는 `WHERE user_id = ?` 조건 쿼리에서) 풀스캔이 일어난다.

## 마무리

도메인 모델과 스키마는 서로를 압박한다. 애그리거트 경계를 테이블로 표현하면서 InnoDB의 클러스터링 특성을 활용하면 조회 성능을 얻을 수 있다. PK 전략은 삽입 패턴, 외부 노출 여부, 분산 환경 여부를 고려해 선택한다. Soft delete는 편리해 보이지만 전체 쿼리에 미치는 부담을 따져봐야 하고, 이력 보관이 목적이라면 이력 테이블이 더 명료한 선택일 때가 많다. 캐릭터셋과 콜레이션은 마이그레이션 시 조용히 문제를 일으키므로 변경 사항을 꼭 확인하자.

9장에서는 JPA와 MySQL이 실제로 맞붙는 지점을 본다. N+1 문제, 페이지네이션 함정, 영속성 컨텍스트의 메모리 문제 — JPA가 만들어주는 편안함 뒤에 있는 MySQL과의 간극을 함께 들여다보자.

## 참고 자료

- Baeldung — DDD aggregates and @DomainEvents — https://www.baeldung.com/spring-data-ddd
- brandur.org — Soft Deletion Probably Isn't Worth It — https://brandur.org/soft-deletion
- Brent Ozar — What Are Soft Deletes — https://www.brentozar.com/archive/2020/02/what-are-soft-deletes-and-how-are-they-implemented/
- Cultured Systems — Avoiding the soft delete anti-pattern — https://www.cultured.systems/2024/04/24/Soft-delete/
- Skeema — Five Surprises in MySQL 8.4 LTS — https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- CodeRed — Guide to MySQL Charsets & Collations — https://www.coderedcorp.com/blog/guide-to-mysql-charsets-collations/
- MySQL :: Migrating from older collations — https://dev.mysql.com/blog-archive/mysql-8-0-collations-migrating-from-older-collations/


# 9장. JPA로 MySQL 다루기 — 영속성 기본기와 함정

JPA를 처음 배울 때 느끼는 매력은 명확하다. SQL을 직접 쓰지 않아도 된다. 엔티티를 저장하고 꺼내는 것이 자바 코드처럼 느껴진다. 복잡한 JOIN도 연관 관계 설정으로 해결되는 것 같다. 그런데 실제 서비스를 운영하다 보면 이 편안함의 이면을 하나씩 마주하게 된다.

"N+1이 왜 이렇게 많이 나와요?" "페이지네이션이 갑자기 메모리를 1GB 잡아먹어요." "배치 처리가 왜 이렇게 느리죠?" 각각의 문제는 JPA가 만들어주는 추상과 MySQL이 실제로 실행하는 SQL 사이의 거리에서 나온다.

JPA의 일상 함정을 함께 풀어보자. 배치·동시성·락 패턴은 다음 장의 몫이다.

## JPA + native SQL 하이브리드 — 어디서 무엇을 쓸 것인가

JPA를 쓰면 모든 DB 접근을 JPA로 해야 한다는 의무는 없다. Vlad Mihalcea, Thorben Janssen 같은 JPA 전문가들이 공통으로 권고하는 접근이 있다.

**CRUD와 단일 애그리거트 영속화 → JPA**
엔티티 하나를 저장하고, 수정하고, 삭제하는 것. 또는 단일 애그리거트 루트를 통해 하위 항목들을 같이 다루는 것. JPA의 영속성 컨텍스트와 변경 감지가 여기서 빛을 발한다.

**N개 테이블 조인 + 집계 보고서 → JdbcTemplate 또는 MyBatis**
5개 테이블을 JOIN하고 GROUP BY로 집계하는 보고서 쿼리를 JPA JPQL로 작성하면 어떻게 될까. 가능은 하지만 SQL로 쓰는 것보다 복잡하고, 옵티마이저에 의도를 정확히 전달하기 어려울 때도 있다. 이런 쿼리는 JdbcTemplate로 native SQL을 쓰는 편이 낫다.

**bulk UPDATE/DELETE → JdbcTemplate batchUpdate 또는 native**
JPA로 100만 건을 UPDATE하려면 100만 개 엔티티를 메모리에 올려 각각 변경하고 flush해야 한다. native `UPDATE orders SET status = 'CLOSED' WHERE created_at < ?`가 100배 빠르다.

이 세 가지 구분을 팀 안에서 명시적으로 합의해두면 "JPA로 해야 하나 SQL로 해야 하나"라는 논쟁이 줄어든다.

```java
// CRUD는 JPA Repository
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    // Spring Data JPA 기본 메서드들
    Optional<Order> findByIdAndUserId(Long id, Long userId);
}

// 보고서 쿼리는 JdbcTemplate
@Repository
public class OrderReportRepository {

    private final JdbcTemplate jdbcTemplate;

    public List<DailySalesSummary> findDailySalesSummary(LocalDate from, LocalDate to) {
        String sql = """
            SELECT DATE(created_at) AS order_date,
                   COUNT(*) AS order_count,
                   SUM(total_amount) AS total_revenue
            FROM orders
            WHERE status = 'COMPLETED'
              AND created_at >= ? AND created_at < ?
            GROUP BY DATE(created_at)
            ORDER BY order_date
            """;

        return jdbcTemplate.query(sql,
            (rs, rowNum) -> new DailySalesSummary(
                rs.getDate("order_date").toLocalDate(),
                rs.getInt("order_count"),
                rs.getBigDecimal("total_revenue")
            ),
            from, to.plusDays(1)
        );
    }
}
```

한 트랜잭션에서 JPA와 JdbcTemplate을 함께 쓸 때 주의할 점이 있다. JPA는 영속성 컨텍스트에 변경 사항을 모아두다가 flush 시점에 SQL을 실행한다. JdbcTemplate은 바로 실행한다. 그래서 JPA로 뭔가를 수정하고 JdbcTemplate으로 그 결과를 읽으면 아직 flush가 안 된 변경을 보지 못할 수 있다. 이럴 때는 JdbcTemplate 호출 전에 `entityManager.flush()`를 호출해 JPA pending 쓰기를 먼저 동기화해두는 편이 낫다.

```java
@Service
@Transactional
public class OrderService {

    private final EntityManager entityManager;
    private final OrderRepository orderRepository;
    private final JdbcTemplate jdbcTemplate;

    public void processAndReport(Long orderId) {
        // JPA로 상태 변경
        Order order = orderRepository.findById(orderId).orElseThrow();
        order.complete();  // 상태 변경 — 아직 DB에 안 쓰임

        // JPA pending 쓰기를 DB에 반영
        entityManager.flush();

        // 이제 JdbcTemplate으로 최신 상태 조회 가능
        Long completedCount = jdbcTemplate.queryForObject(
            "SELECT COUNT(*) FROM orders WHERE status = 'COMPLETED' AND user_id = ?",
            Long.class, order.getUserId()
        );
    }
}
```

## N+1 문제 — 진단과 세 가지 도구

N+1 문제. JPA에서 가장 유명한 함정이다. 연관 관계를 LAZY 로딩으로 설정하고 목록을 조회하면, 목록 1번 쿼리 + 각 항목별 연관 엔티티 N번 쿼리, 합쳐서 N+1번 쿼리가 실행된다.

```java
// 이 코드가 N+1을 만드는 전형적인 패턴
@Entity
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)  // 기본 LAZY
    @JoinColumn(name = "user_id")
    private User user;

    // 필드들...
}

// 서비스
@Transactional(readOnly = true)
public List<OrderDto> getRecentOrders() {
    List<Order> orders = orderRepository.findTop50ByOrderByCreatedAtDesc();
    // 여기까지는 쿼리 1번

    return orders.stream()
        .map(order -> new OrderDto(
            order.getId(),
            order.getUser().getName()  // 여기서 각 order마다 user 조회 — 50번 추가 쿼리!
        ))
        .collect(toList());
}
```

50개 주문을 조회하면 주문 목록 1번 + 각 주문의 user 조회 50번 = 51번 쿼리가 된다. 슬로우 쿼리 로그에는 안 잡히는 경우가 많다(개별 쿼리가 빠르기 때문에). Hibernate의 쿼리 로그를 켜거나 APM 도구로 들여다보자.

N+1을 해결하는 도구는 크게 세 가지다.

### 1. Fetch Join

JPQL에서 INNER JOIN FETCH나 LEFT JOIN FETCH로 연관 엔티티를 한 번에 가져온다.

```java
// Repository에서 JPQL fetch join 사용
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o JOIN FETCH o.user ORDER BY o.createdAt DESC")
    List<Order> findRecentOrdersWithUser(Pageable pageable);
}
```

```sql
-- 생성되는 SQL (대략)
SELECT o.*, u.*
FROM orders o
INNER JOIN users u ON o.user_id = u.id
ORDER BY o.created_at DESC
LIMIT 50;
```

쿼리 1번으로 주문과 유저를 같이 가져온다. 단점이 있다. 컬렉션(일대다 관계)을 fetch join하면 중복 행이 생길 수 있어 DISTINCT가 필요하고, Pageable(페이지네이션)과 함께 컬렉션 fetch join은 쓰지 말자 — 이 부분은 뒤에서 자세히 본다.

### 2. EntityGraph

Spring Data JPA 애노테이션으로 fetch join을 선언적으로 지정한다.

```java
// 엔티티에 NamedEntityGraph 정의
@Entity
@NamedEntityGraph(
    name = "Order.withUser",
    attributeNodes = @NamedAttributeNode("user")
)
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    // ...
}

// Repository에서 EntityGraph 적용
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph("Order.withUser")
    List<Order> findTop50ByOrderByCreatedAtDesc();

    // 또는 ad-hoc EntityGraph
    @EntityGraph(attributePaths = {"user", "items"})
    Optional<Order> findByIdWithDetails(Long id);
}
```

EntityGraph는 fetch join과 내부적으로 비슷하게 LEFT OUTER JOIN을 발생시킨다. 인터페이스가 더 선언적이라 읽기 편하다는 장점이 있다.

### 3. @BatchSize

연관 엔티티를 한 번에 N개씩 묶어서 IN 쿼리로 조회한다. fetch join과 달리 컬렉션에도 자연스럽게 쓸 수 있다.

```java
// 전역 설정 (application.yml)
// spring.jpa.properties.hibernate.default_batch_fetch_size: 100

// 또는 엔티티에 직접 설정
@Entity
public class Order {
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    @BatchSize(size = 100)  // 100개씩 IN 쿼리로 묶어 조회
    private List<OrderItem> items;
}
```

```sql
-- @BatchSize(100) 적용 시 생성되는 쿼리
SELECT * FROM order_items WHERE order_id IN (1, 2, 3, ..., 100);
-- N+1이 아니라 N/100+1번으로 줄어든다
```

세 도구 중 무엇을 고를지는 상황 나름이다.

- **단순 다대일(ManyToOne) 조회** → fetch join 또는 EntityGraph
- **컬렉션(일대다) 조회, 페이지네이션 없음** → fetch join 또는 EntityGraph
- **컬렉션 조회 + 페이지네이션** → @BatchSize (이유는 다음 절에서)
- **여러 연관 관계가 복잡하게 얽힌 경우** → JdbcTemplate으로 native SQL이 더 명료할 때도 있다

## 페이지네이션 — OFFSET의 함정과 keyset

페이지네이션은 대부분의 목록 API에 들어간다. Spring Data JPA의 `Pageable`을 쓰면 간단하게 구현할 수 있다.

```java
// 페이지네이션 API 예시
@GetMapping("/orders")
public Page<OrderDto> getOrders(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size
) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
    return orderRepository.findAll(pageable).map(OrderDto::from);
}
```

```sql
-- 생성되는 SQL
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 0;   -- 1페이지
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 20;  -- 2페이지
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 10000;  -- 501페이지
```

1~2페이지는 빠르다. 그런데 501페이지(OFFSET 10000)는? MySQL은 `OFFSET 10000`을 처리하기 위해 10000개 행을 건너뛰고 그다음 20개를 반환한다. "건너뛰기"가 실제로는 처음 10020개 행을 읽고 앞의 10000개를 버리는 것이다. 페이지가 깊어질수록 느려진다. 100페이지가 10페이지보다 10배 느리지 않고, 실제로는 훨씬 더 느려질 수 있다.

무한 스크롤이나 관리자 화면처럼 깊은 페이지가 실제로 사용되는 경우라면 keyset pagination(seek 방식)이 답이다.

```java
// Keyset pagination — JPA JPQL
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // 마지막으로 본 created_at과 id를 기준으로 다음 페이지 조회
    @Query("""
        SELECT o FROM Order o
        WHERE o.status = 'COMPLETED'
          AND (o.createdAt < :lastCreatedAt
               OR (o.createdAt = :lastCreatedAt AND o.id < :lastId))
        ORDER BY o.createdAt DESC, o.id DESC
        """)
    List<Order> findNextPage(
        @Param("lastCreatedAt") LocalDateTime lastCreatedAt,
        @Param("lastId") Long lastId,
        Pageable pageable  // LIMIT만 적용됨, OFFSET은 0
    );
}
```

```sql
-- 생성되는 SQL
SELECT * FROM orders
WHERE status = 'COMPLETED'
  AND (created_at < '2024-01-15 10:30:00'
       OR (created_at = '2024-01-15 10:30:00' AND id < 12345))
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

OFFSET이 없다. 인덱스 `(status, created_at, id)`를 타고 바로 해당 위치로 이동해서 20개를 읽는다. 1페이지든 10000페이지든 속도가 같다.

keyset의 제약도 있다. 이전 페이지로 돌아가기가 어렵고(커서가 단방향이라), 특정 페이지 번호로 직접 이동하는 것이 불가능하다. "다음 페이지", "이전 페이지" 버튼만 있는 무한 스크롤이나 단방향 커서 방식에 어울린다.

Vlad Mihalcea와 Thorben Janssen 모두 깊은 페이지네이션에서 keyset이 절대적으로 유리하다고 강조한다. OFFSET 방식이 편리하지만 데이터가 쌓일수록 내재된 성능 문제가 드러난다.

## `findAll(Pageable)` + 컬렉션 JOIN FETCH의 메모리 페이징 경고

이 조합은 피해야 할 안티패턴이다. 왜 그런지 이해하면 다시는 빠지지 않는다.

```java
// 이것은 위험한 코드다
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.items WHERE o.status = 'COMPLETED'")
    Page<Order> findCompletedOrdersWithItems(Pageable pageable);
    // ← HibernateJpaDialect가 경고를 낸다
}
```

Hibernate는 이 쿼리에서 경고를 발생시킨다.

```
HHH90003004: firstResult/maxResults specified with collection fetch; 
applying in memory
```

무슨 뜻이냐면 — MySQL에 `LIMIT/OFFSET`을 보내지 않고, **전체 결과를 메모리로 올린 다음 Java에서 페이지를 자른다**는 것이다. 테이블에 1000만 건이 있다면 1000만 건을 Java 힙으로 올린 뒤 필요한 20건만 남기고 나머지를 버린다. 메모리 부족 오류(OOM)가 날 수 있고, 났다 하면 새벽에 서버가 다운된다.

왜 이런 동작을 하느냐면, 컬렉션 fetch join은 SQL 수준에서 행 수가 늘어나기 때문이다. 주문 1개에 아이템 3개가 있으면 JOIN 결과는 3행이다. 주문 10개에 각각 3개 아이템이 있으면 30행. MySQL에 `LIMIT 10`을 주면 30행 중 10행만 오는데, 이는 주문 기준 10개가 아닐 수 있다. 그래서 Hibernate는 아예 제한 없이 다 가져온 다음 자바에서 주문 기준으로 페이지를 나누는 것이다.

해결책은 두 가지다.

**1. Pageable은 페이징에, 컬렉션은 별도 BatchSize로**

```java
// OrderRepository — 페이지네이션만
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    Page<Order> findByStatus(String status, Pageable pageable);  // 일반 페이지네이션
}

// Order 엔티티
@Entity
public class Order {
    @OneToMany(mappedBy = "order")
    @BatchSize(size = 100)  // 페이지 안의 주문들의 아이템을 IN 쿼리로 한 번에
    private List<OrderItem> items;
}
```

이렇게 하면 페이지네이션 쿼리는 `LIMIT/OFFSET`으로 실제 DB에서 페이지를 자르고, 그 페이지 안의 주문들의 아이템은 `@BatchSize`로 IN 쿼리 한 번에 가져온다.

**2. EntityGraph로 대체 (단, Pageable 없이)**

Pageable 없이 특정 주문 하나를 조회할 때는 EntityGraph가 깔끔하다.

```java
@EntityGraph(attributePaths = {"items", "items.product"})
Optional<Order> findByIdWithDetails(Long id);
```

## 영속성 컨텍스트와 1차 캐시 — 만 단위 엔티티를 들고 있을 때

영속성 컨텍스트는 JPA가 관리하는 엔티티들의 저장소다. 같은 트랜잭션 안에서 같은 PK로 엔티티를 두 번 조회하면 두 번째는 DB를 가지 않고 영속성 컨텍스트(1차 캐시)에서 반환한다.

이 1차 캐시가 문제가 될 때가 있다. 배치 처리에서 대량의 엔티티를 처리할 때다.

```java
// 이 코드는 OOM을 일으킬 수 있다
@Transactional
public void processAllOrders() {
    List<Order> orders = orderRepository.findAll();  // 100만 건 모두 조회 + 1차 캐시에 저장
    for (Order order : orders) {
        order.markAsProcessed();  // 변경 감지 대상이 됨
        // 100만 건이 전부 1차 캐시에 쌓이고 변경 감지 대상으로 남아 있음
    }
    // flush 시점에 100만 건 UPDATE
}
```

100만 개 엔티티가 영속성 컨텍스트 안에 들어차면 Java 힙을 가득 채우고, 변경 감지를 위한 dirty checking도 100만 번 일어난다. 이렇게 쓰면 끔찍한 일이 벌어진다.

배치 처리에서는 주기적으로 `flush()`와 `clear()`를 호출해 영속성 컨텍스트를 비우자.

```java
// 올바른 배치 처리 패턴
@Transactional
public void processOrdersInBatch() {
    final int BATCH_SIZE = 1000;
    long lastId = 0;

    while (true) {
        List<Order> batch = orderRepository.findNextBatch(lastId, BATCH_SIZE);
        if (batch.isEmpty()) break;

        for (Order order : batch) {
            order.markAsProcessed();
        }

        entityManager.flush();   // 변경 사항 DB에 반영
        entityManager.clear();   // 영속성 컨텍스트 비우기

        lastId = batch.get(batch.size() - 1).getId();
    }
}
```

`flush()` 후 `clear()`를 하면 영속성 컨텍스트가 비워진다. 다음 배치 조회는 DB에서 다시 가져오지만 그 양이 1000건이라 관리 가능하다.

이 패턴에서 쿼리 메서드도 중요하다. `findAll()`로 전체를 한 번에 가져오지 말고, 커서 기반(lastId를 기준으로 다음 1000건)으로 청크를 가져오는 편이 낫다.

```java
// 청크 기반 조회
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o WHERE o.id > :lastId ORDER BY o.id ASC")
    List<Order> findNextBatch(@Param("lastId") Long lastId, Pageable pageable);
}

// 호출 시
List<Order> batch = orderRepository.findNextBatch(lastId,
    PageRequest.of(0, BATCH_SIZE));
```

## 영속성 컨텍스트의 변경 감지(dirty checking) 이해하기

JPA의 변경 감지는 편리하지만 예상치 못한 쿼리를 만들기도 한다. 엔티티를 조회하고 setter를 호출하면 트랜잭션이 끝날 때 자동으로 UPDATE 쿼리가 나간다. `save()`를 명시적으로 호출하지 않아도.

```java
@Transactional
public void updateOrderStatus(Long orderId, String newStatus) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    order.setStatus(newStatus);
    // save() 없어도 트랜잭션 종료 시 UPDATE 실행
    // 이 동작을 알아야 의도치 않은 UPDATE를 막을 수 있다
}
```

이 변경 감지는 스냅샷 비교로 작동한다. 엔티티를 조회할 때 Hibernate가 원본 상태의 복사본(스냅샷)을 만들어두고, flush 시점에 현재 상태와 비교해 다른 필드가 있으면 UPDATE를 생성한다. 이 스냅샷이 1차 캐시에 함께 저장되므로, 대량의 엔티티를 들고 있으면 그만큼 메모리를 더 쓴다.

읽기 전용 트랜잭션(`@Transactional(readOnly = true)`)을 쓰면 Hibernate가 스냅샷을 만들지 않아 메모리를 아낄 수 있고 성능도 약간 개선된다. 수정이 필요 없는 조회 서비스 메서드에는 `readOnly = true`를 붙여두는 편이 낫다.

```java
// 읽기 전용 트랜잭션 — 스냅샷 없음, dirty checking 없음
@Transactional(readOnly = true)
public List<OrderDto> getOrderList(Long userId, Pageable pageable) {
    return orderRepository.findByUserId(userId, pageable)
        .map(OrderDto::from)
        .getContent();
}
```

## JPQL과 QueryDSL에서 인덱스·옵티마이저 친화적으로 쓰기

> **사이드바:** QueryDSL은 타입 안전 쿼리 빌더다. JPQL의 문자열 기반 쿼리 대신 컴파일 타임에 오류를 잡을 수 있고, 동적 조건 쿼리를 체인 방식으로 작성할 수 있다. 이 책에서 깊이 다루지는 않지만, QueryDSL을 쓸 때 인덱스를 고려해야 하는 포인트들을 짚어보자.

첫째, JPQL이나 QueryDSL에서 컬럼에 함수를 적용하지 말자. 5장에서 본 내용이다.

```java
// 인덱스를 타지 못하는 JPQL
@Query("SELECT o FROM Order o WHERE YEAR(o.createdAt) = :year")
List<Order> findByYear(@Param("year") int year);

// 인덱스를 타는 방식으로 — 범위 조건으로 변환
@Query("SELECT o FROM Order o WHERE o.createdAt >= :from AND o.createdAt < :to")
List<Order> findByDateRange(
    @Param("from") LocalDateTime from,
    @Param("to") LocalDateTime to
);
```

둘째, QueryDSL로 동적 조건을 만들 때 `BooleanExpression`이 null이면 조건에서 빠진다는 점을 활용하되, 결과적으로 생성되는 SQL에 인덱스가 잘 쓰이는지 확인해두는 편이 낫다.

```java
// QueryDSL 동적 쿼리 예시
public List<Order> findOrders(OrderSearchCondition cond) {
    QOrder o = QOrder.order;

    return queryFactory
        .selectFrom(o)
        .where(
            statusEq(o, cond.getStatus()),         // null이면 조건 무시
            userIdEq(o, cond.getUserId()),
            createdAtBetween(o, cond.getFrom(), cond.getTo())
        )
        .orderBy(o.createdAt.desc())
        .limit(cond.getSize())
        .fetch();
}

private BooleanExpression statusEq(QOrder o, String status) {
    return status != null ? o.status.eq(status) : null;
}

private BooleanExpression createdAtBetween(QOrder o,
    LocalDateTime from, LocalDateTime to) {
    if (from == null && to == null) return null;
    if (from == null) return o.createdAt.loe(to);
    if (to == null) return o.createdAt.goe(from);
    return o.createdAt.between(from, to);
}
```

셋째, `fetchJoin()`과 `limit()`을 함께 쓸 때 컬렉션 join이 있으면 앞에서 본 메모리 페이징 경고와 동일한 문제가 생긴다. QueryDSL에서도 컬렉션 join + 페이지네이션 조합은 피하자.

## Spring Data JPA 리포지토리 설계 — 실전 패턴

리포지토리가 왜 이렇게 복잡해질까. 엔티티가 여러 개이고, 각각에 대한 조회 조건이 다양해지면 메서드가 줄줄이 늘어난다. 몇 가지 실전 패턴을 같이 살펴보자.

```java
// 기본 리포지토리 — JpaRepository 상속
@Repository
public interface OrderRepository
        extends JpaRepository<Order, Long>, OrderRepositoryCustom {

    // Spring Data JPA 쿼리 메서드
    Page<Order> findByUserId(Long userId, Pageable pageable);

    @EntityGraph(attributePaths = {"items"})
    Optional<Order> findWithItemsById(Long id);

    // 카운트 최적화 — countQuery를 별도로
    @Query(value = "SELECT o FROM Order o WHERE o.status = :status",
           countQuery = "SELECT COUNT(o) FROM Order o WHERE o.status = :status")
    Page<Order> findByStatus(@Param("status") String status, Pageable pageable);
}

// 커스텀 리포지토리 인터페이스
public interface OrderRepositoryCustom {
    List<Order> searchOrders(OrderSearchCondition cond);
}

// QueryDSL 구현
@Repository
@RequiredArgsConstructor
public class OrderRepositoryImpl implements OrderRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    @Override
    public List<Order> searchOrders(OrderSearchCondition cond) {
        // QueryDSL 구현
    }
}
```

`countQuery`를 별도로 지정하는 것이 중요한 포인트다. `Page<T>` 반환 시 Spring Data JPA는 전체 카운트 쿼리를 자동으로 만든다. 이때 원본 쿼리에 JOIN이 있으면 카운트 쿼리에도 JOIN이 붙어 불필요하게 느려질 수 있다. `countQuery`를 명시하면 JOIN 없는 단순한 COUNT 쿼리를 쓸 수 있다.

## 지연 로딩과 트랜잭션 범위의 함정

JPA의 LAZY 로딩은 트랜잭션 안에서만 작동한다. 트랜잭션이 끝난 뒤 연관 엔티티에 접근하면 `LazyInitializationException`이 발생한다. 스프링에서 자주 보는 패턴이 트랜잭션 서비스에서 엔티티를 반환하고, 컨트롤러나 뷰에서 연관 관계에 접근하려다 예외가 터지는 것이다.

```java
// 서비스 — 트랜잭션 안에서 Order를 반환
@Transactional
public Order getOrder(Long id) {
    return orderRepository.findById(id).orElseThrow();
    // 트랜잭션 종료
}

// 컨트롤러 — 트랜잭션 밖에서 연관 관계 접근
@GetMapping("/orders/{id}")
public OrderResponse getOrder(@PathVariable Long id) {
    Order order = orderService.getOrder(id);
    // 여기서 order.getUser().getName() 호출 시 LazyInitializationException!
    // 트랜잭션이 이미 끝났으므로 LAZY 로딩 불가
}
```

해결책은 두 가지다.

하나, 서비스 레이어에서 DTO로 변환해 반환한다. 엔티티가 아닌 DTO를 컨트롤러로 보내면 연관 엔티티 접근이 트랜잭션 안에서 이루어진다.

```java
@Transactional(readOnly = true)
public OrderDto getOrder(Long id) {
    Order order = orderRepository.findByIdWithDetails(id).orElseThrow();
    return OrderDto.from(order);  // 트랜잭션 안에서 DTO 변환
}
```

둘, OSIV(Open Session In View) 패턴을 쓴다. `spring.jpa.open-in-view=true`로 설정하면 HTTP 요청 전체에 걸쳐 세션을 유지해서 컨트롤러에서도 LAZY 로딩이 가능하다. 기본값이 `true`인데, 이 설정이 있으면 커넥션 풀에서 커넥션을 HTTP 요청 내내 점유해 성능에 부정적일 수 있다. 트래픽이 많다면 `false`로 바꾸고 DTO 변환 패턴을 쓰는 편이 낫다.

```yaml
# application.yml — 비권장 (기본 true)
spring:
  jpa:
    open-in-view: false  # 권장 설정 — 커넥션 점유 최소화
```

## 엔티티 설계 실전 — 양방향 연관 관계의 주의점

양방향 연관 관계는 편리하지만 함정도 같이 따라온다. 어떤 함정일까. 코드부터 같이 살펴보자.

```java
// Order 엔티티
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @OneToMany(mappedBy = "order",
               cascade = CascadeType.ALL,
               orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    // 연관 관계 편의 메서드
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);  // 양방향 동기화
    }

    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }
}

// OrderItem 엔티티
@Entity
@Table(name = "order_items")
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @Column(nullable = false)
    private Integer quantity;

    @Column(nullable = false)
    private BigDecimal unitPrice;
}
```

양방향 연관 관계를 쓸 때 주의할 점들이 있다.

`CascadeType.ALL`과 `orphanRemoval = true`를 동시에 쓰면 Order를 삭제할 때 OrderItem도 자동으로 삭제된다. 이것이 의도한 동작인지 확인하고 쓰자. 의도치 않게 연쇄 삭제가 일어나면 난감하다.

양방향에서 "연관 관계의 주인"은 FK를 가진 쪽이다. `OrderItem.order`에 `@JoinColumn`이 있으므로 OrderItem이 주인이다. `Order.items`의 `mappedBy = "order"`는 읽기 전용이라는 의미다. DB 반영은 `OrderItem.order`를 통해 일어난다. 그래서 `addItem()` 편의 메서드에서 `item.setOrder(this)`를 호출하는 것이 중요하다.

## 영속성 전환 상태와 merge

JPA 엔티티는 네 가지 상태를 가진다.

- **비영속(Transient)**: `new Order()`로 만들었지만 아직 영속성 컨텍스트에 없음
- **영속(Persistent)**: 영속성 컨텍스트가 관리 중. 변경 감지 대상
- **준영속(Detached)**: 영속성 컨텍스트에서 분리됨. 더 이상 변경 감지 안 됨
- **삭제(Removed)**: 삭제 표시됨, flush 시 DELETE

`save()` 메서드의 동작을 이해하면 의도치 않은 merge를 막을 수 있다.

```java
// SimpleJpaRepository의 save() 내부 (개념)
public <S extends T> S save(S entity) {
    if (entityInformation.isNew(entity)) {
        em.persist(entity);  // 새 엔티티 → persist
        return entity;
    } else {
        return em.merge(entity);  // 기존 엔티티 → merge
    }
}
```

ID가 null이면 새 엔티티로 판단해 `persist`를 호출하고, ID가 있으면 기존 엔티티로 판단해 `merge`를 호출한다. `merge`는 준영속 엔티티를 영속성 컨텍스트로 다시 붙이는 것인데, 이때 **모든 필드를 DB 값으로 덮어쓴 새 영속 객체를 반환**한다. 원본 객체는 여전히 준영속 상태다.

```java
// merge의 함정
Order detachedOrder = ...; // 준영속 상태 엔티티
detachedOrder.setStatus("COMPLETED");

Order merged = orderRepository.save(detachedOrder);
// detachedOrder와 merged는 다른 객체!
// detachedOrder는 여전히 준영속
// merged가 영속성 컨텍스트에서 관리되는 새 객체

// 이후 detachedOrder를 수정해도 DB에 반영 안 됨
detachedOrder.setNote("note");  // 이 변경은 DB에 안 감
merged.setNote("note");         // 이래야 DB에 반영됨
```

이런 혼란을 피하려면 준영속 객체를 서비스 레이어 경계 바깥으로 넘기지 않는 편이 낫다. 트랜잭션 안에서 조회하고, 수정하고, DTO로 변환해 반환하자.

## 9장과 10장, 5장 사이의 다리

여기서 한 발 뒤로 물러서서 전체 그림을 보자.

5장에서 EXPLAIN ANALYZE로 쿼리를 진단하는 법을 배웠다. 지금 이 장에서 JPA가 만들어내는 쿼리들이 어떤 함정을 가지는지를 봤다. 그런데 JPA 코드를 작성하다 N+1이 의심되거나 페이지네이션이 느려진다면, 5장의 도구를 다시 꺼내자. `spring.jpa.show_sql=true` 또는 Hibernate 쿼리 로그로 실제 SQL을 확인하고, 그것을 EXPLAIN ANALYZE로 분석한다. JPA 레벨의 진단과 MySQL 레벨의 진단이 항상 함께 가야 한다.

10장에서는 JPA의 다음 단계로 넘어간다. 배치 처리 100배 개선, 수백만 건 UPDATE 청크 분할, `@Version`으로 낙관적 락, `@Lock(PESSIMISTIC_WRITE)`로 비관적 락, MySQL named lock 분산락까지. 영속성 기본기 위에 성능과 동시성의 무기들을 올리는 것이 10장의 주제다. 12장의 운영 관측 도구(슬로우 쿼리 로그, performance_schema)와 연결하면 JPA 코드의 영향이 실제로 DB에서 어떻게 보이는지 전체 그림이 잡힌다.

## 마무리

JPA의 편안함은 진짜다. 하지만 그 편안함 뒤에서 MySQL이 무슨 쿼리를 실행하는지 모르고 쓰는 것은 찜찜하다. 이 장에서 다룬 함정들을 정리해두자.

**N+1**: 기본 LAZY로 인한 연쇄 쿼리. fetch join, EntityGraph, BatchSize로 상황에 맞게 풀어내자.

**컬렉션 fetch join + Pageable**: 메모리 페이징 경고. 컬렉션 fetch join과 Pageable을 함께 쓰지 말자.

**깊은 OFFSET 페이지네이션**: 데이터가 쌓일수록 점점 느려진다. 무한 스크롤이나 깊은 페이지네이션에는 keyset pagination이 답이다.

**영속성 컨텍스트에 만 단위 엔티티**: 배치 처리에서 flush+clear를 주기적으로 호출하자.

**OSIV**: `open-in-view=false`로 설정하고 트랜잭션 안에서 DTO 변환을 완료하는 편이 낫다.

**readOnly 트랜잭션**: 수정이 없는 조회는 `@Transactional(readOnly = true)` — 스냅샷을 만들지 않아 메모리를 아낀다.

이것들을 알고 쓰는 것과 모르고 쓰는 것의 차이는 처음엔 작아 보이지만, 서비스가 커지면서 점점 벌어진다.

## 참고 자료

- Vlad Mihalcea — Keyset Pagination with JPA and Hibernate — https://vladmihalcea.com/keyset-pagination-jpa-hibernate/
- Vlad Mihalcea — SQL Seek/Keyset pagination — https://vladmihalcea.com/sql-seek-keyset-pagination/
- Vlad Mihalcea — JPA First-Level Cache — https://vladmihalcea.com/jpa-hibernate-first-level-cache/
- Vlad Mihalcea — High-Performance Java Persistence, Chapter 13 Flushing — https://vladmihalcea.com/high-performance-java-persistence-chapter-13-flushing/
- Vlad Mihalcea — Java data access technology survey — https://vladmihalcea.com/java-data-access-technology/
- Thorben Janssen — Offset vs Keyset Pagination with Spring Data JPA — https://thorben-janssen.com/offset-and-keyset-pagination-with-spring-data-jpa/
- Baeldung — Optimistic Locking in JPA — https://www.baeldung.com/jpa-optimistic-locking
- DEV.to — Understanding and Solving the N+1 Problem in Spring Data JPA — https://dev.to/sadiul_hakim/understanding-and-solving-the-n1-problem-in-spring-data-jpa-2b6f
- SharpSkill — Spring Data JPA N+1: Fetch Join and EntityGraph — https://sharpskill.dev/en/blog/spring-boot/spring-data-jpa-n-plus-1-fetch-join-entitygraph


# 10장. JPA를 넘어 — 성능·동시성·락 패턴·배치

어느 날 갑자기 배포 슬랙 채널에 메시지가 올라온다. "오늘 오후 정산 배치 돌렸는데 왜 이렇게 오래 걸리죠?" 담당자를 찾아보니 기존엔 3분이면 끝나던 INSERT가 갑자기 37분을 넘겼다. 코드는 어제와 똑같다. DB 서버 CPU는 10%대. 그런데 느리다.

원인을 파고들어 보면 `@GeneratedValue(strategy = GenerationType.IDENTITY)` 한 줄이 문제다. 락의 애플리케이션 패턴을 다룰 차례다. 락 메커니즘은 3장에서 이미 봤다. 9장에서 JPA의 일상 함정들을 살펴봤다면, 이번에는 그 함정을 넘어 성능을 진짜로 뽑아내는 길을 따라가보자. 배치 성능, 수백만 row를 건드리는 UPDATE/DELETE, 트랜잭션 경계 설계, 그리고 named lock을 이용한 분산락 패턴까지 — JPA가 버거워지는 지점에서 우리는 어디로 내려가야 하는지를 함께 살펴보자.

---

## 배치 INSERT 100배 — 세 가지 설정의 합주

배치 INSERT 성능 문제를 한 번이라도 겪어본 사람은 안다. `saveAll()` 한 줄로 리스트를 던졌는데 개별 INSERT가 낱개로 나간다. 1,000건이면 1,000번의 왕복. 찜찜하지 않은가?

우아한형제들 기술블로그에 기록된 사례를 보자. 배치 INSERT 성능을 100배 끌어올린 핵심은 세 가지 설정이었다.

```yaml
# application.yml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
```

```properties
# JDBC URL에 반드시 추가
spring.datasource.url=jdbc:mysql://localhost:3306/mydb?rewriteBatchedStatements=true
```

이 세 가지가 **모두** 켜져야 진짜 배치 INSERT가 일어난다. 하나라도 빠지면 겉보기에는 배치처럼 보여도 실제로는 낱개 INSERT가 나간다. 특히 `rewriteBatchedStatements=true`가 빠지면 JDBC 드라이버가 배치 요청을 개별 `INSERT`로 펼쳐서 보내기 때문에 DB 왕복 횟수가 줄지 않는다.

그런데 여기서 한 가지 난감한 지점이 생긴다. `@GeneratedValue(strategy = GenerationType.IDENTITY)` 전략은 배치와 함께 쓸 수 없다.

### IDENTITY 전략이 배치를 막는 이유

IDENTITY 전략은 INSERT 직후 DB가 생성한 PK를 바로 가져와야 한다. Hibernate는 이 PK를 영속성 컨텍스트에서 즉시 추적해야 하므로, INSERT 직후 `LAST_INSERT_ID()`를 호출해 PK를 알아낸다. 이 흐름 자체가 배치를 불가능하게 만든다 — 배치는 여러 INSERT를 묶어서 한 번에 보내는 것인데, 각 INSERT가 끝날 때마다 PK를 받아야 하니 묶을 수가 없다.

해결책은 SEQUENCE 또는 TABLE 전략으로 바꾸는 것이다. MySQL은 기본 SEQUENCE를 지원하지 않으므로 `TABLE` 전략을 쓰거나, Hibernate의 `pooled` 시퀀스 알로케이터를 직접 구성한다.

```java
// IDENTITY에서 TABLE 전략으로 변경
@Entity
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.TABLE,
                    generator = "order_item_seq")
    @TableGenerator(
        name = "order_item_seq",
        table = "hibernate_sequences",
        pkColumnName = "sequence_name",
        valueColumnName = "next_val",
        allocationSize = 50  // 50개씩 미리 채번
    )
    private Long id;

    // ...
}
```

allocationSize를 50으로 잡으면 DB에 한 번 접근할 때마다 50개의 ID를 미리 채번해 메모리에 들고 있는다. DB 채번 빈도를 줄이면서도 유일성을 보장한다.

### JdbcTemplate으로 더 깔끔하게

JPA 엔티티 매핑이 복잡한 상황이라면 JdbcTemplate의 `batchUpdate()`를 직접 쓰는 편이 낫다.

```java
@Repository
@RequiredArgsConstructor
public class OrderItemBatchRepository {

    private final JdbcTemplate jdbcTemplate;

    // 1,000건씩 청크로 나눠 배치 INSERT
    public void batchInsert(List<OrderItem> items) {
        String sql = "INSERT INTO order_item (order_id, product_id, quantity, price) "
                   + "VALUES (?, ?, ?, ?)";

        List<List<OrderItem>> chunks = partition(items, 1_000);

        for (List<OrderItem> chunk : chunks) {
            jdbcTemplate.batchUpdate(sql,
                new BatchPreparedStatementSetter() {
                    @Override
                    public void setValues(PreparedStatement ps, int i)
                            throws SQLException {
                        OrderItem item = chunk.get(i);
                        ps.setLong(1, item.getOrderId());
                        ps.setLong(2, item.getProductId());
                        ps.setInt(3, item.getQuantity());
                        ps.setBigDecimal(4, item.getPrice());
                    }

                    @Override
                    public int getBatchSize() {
                        return chunk.size();
                    }
                });
        }
    }

    private <T> List<List<T>> partition(List<T> list, int size) {
        List<List<T>> partitions = new ArrayList<>();
        for (int i = 0; i < list.size(); i += size) {
            partitions.add(list.subList(i, Math.min(i + size, list.size())));
        }
        return partitions;
    }
}
```

1,000건 청크로 나눠 각 청크를 하나의 배치 요청으로 보내자. `rewriteBatchedStatements=true`와 조합하면 1,000개의 INSERT 값이 하나의 멀티-row INSERT SQL로 합쳐져 나간다.

---

## 수백만 row UPDATE/DELETE — 청크 분할의 기술

"어제 배포에서 `status = 'EXPIRED'`인 주문 데이터를 정리해야 한다"는 요구가 왔다. 테이블에는 4,500만 건이 있고, 그중 만료된 것이 800만 건쯤 된다. 한 트랜잭션에서 `DELETE FROM order WHERE status = 'EXPIRED'`를 날린다고 생각해보자. 끔찍한 일이다.

왜 끔찍할까? 세 가지 이유가 있다.

첫째, 트랜잭션이 종료되기 전까지 삭제 대상 행 전체에 락이 걸린다. 800만 건에 걸린 레코드 락은 다른 트랜잭션들을 한없이 기다리게 만든다.

둘째, binlog에 800만 건의 DELETE row가 쌓이면 리플리카가 그것을 받아 처리하는 동안 복제 lag이 폭발한다. 운영 중에 리플리카가 수 분씩 뒤처지기 시작하면 읽기 요청을 리플리카로 분산시키는 구조 전체가 흔들린다.

셋째, InnoDB의 undo 로그가 급격히 불어나 버퍼풀을 압박한다.

해결책은 간단하다. 작게 잘라서, 짧은 트랜잭션으로, 천천히.

```java
@Service
@RequiredArgsConstructor
public class OrderCleanupService {

    private final JdbcTemplate jdbcTemplate;

    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void deleteExpiredOrdersInChunks() {
        long lastId = 0;
        int chunkSize = 1_000;
        int totalDeleted = 0;

        while (true) {
            // 각 청크는 별도 트랜잭션으로 처리
            int deleted = deleteChunk(lastId, chunkSize);
            totalDeleted += deleted;

            if (deleted < chunkSize) {
                break; // 더 삭제할 것 없음
            }

            // 다음 청크의 시작 ID 계산
            lastId = getLastDeletedId(lastId, chunkSize);

            // 리플리카 lag 완화를 위한 짧은 대기
            sleepQuietly(50); // 50ms
        }

        log.info("총 {}건 삭제 완료", totalDeleted);
    }

    @Transactional
    public int deleteChunk(long fromId, int limit) {
        return jdbcTemplate.update(
            "DELETE FROM orders WHERE id > ? AND status = 'EXPIRED' "
          + "ORDER BY id LIMIT ?",
            fromId, limit
        );
    }
}
```

`ORDER BY id LIMIT ?` 패턴이 핵심이다. id 순서로 정렬해 앞에서부터 잘라내면 각 DELETE 트랜잭션의 크기가 예측 가능해지고, 락 유지 시간도 짧아진다. 청크 사이 50ms 대기는 리플리카가 따라잡을 시간을 주는 일종의 배려다.

물론 이 방식은 전체 작업 시간이 길어진다. 하지만 운영 중인 서비스를 멈추지 않고 진행할 수 있다는 장점이 그것을 훨씬 압도한다.

---

## 트랜잭션 경계 설계 — 외부 IO를 트랜잭션 밖으로

결제 처리 코드를 보면 이런 패턴이 자주 등장한다.

```java
// 찜찜한 패턴: 외부 API 호출이 트랜잭션 안에 있다
@Transactional
public void processPayment(PaymentRequest request) {
    Order order = orderRepository.findById(request.getOrderId())
        .orElseThrow();
    
    // DB 락을 잡고 있는 상태에서 외부 API 호출!
    PaymentResult result = pgClient.charge(request); // 이게 2초 걸리면?
    
    Payment payment = Payment.of(order, result);
    paymentRepository.save(payment);
    order.complete();
}
```

외부 결제 PG API 호출이 트랜잭션 안에 있다. 만약 PG사 API가 일시적으로 느려져 2초 걸린다면, 그 2초 동안 해당 주문에 대한 DB 락이 유지된다. 동시에 같은 주문에 접근하려는 다른 요청은 2초를 기다려야 한다. 트래픽이 몰리면 대기 중인 트랜잭션이 쌓이고, 커넥션 풀이 고갈된다.

그렇다면 어떻게 해야 할까? 외부 IO를 트랜잭션 바깥으로 빼는 것이 출구다.

```java
// 개선된 패턴: 외부 IO를 트랜잭션 밖으로
@Service
@RequiredArgsConstructor
public class PaymentService {

    private final OrderRepository orderRepository;
    private final PaymentRepository paymentRepository;
    private final PgClient pgClient;

    // 트랜잭션 없이: 외부 API 먼저 호출
    public PaymentResult processPayment(PaymentRequest request) {
        // 1단계: 트랜잭션 없이 외부 API 호출
        PaymentResult result = pgClient.charge(request);
        
        // 2단계: 짧은 트랜잭션으로 DB 처리
        return savePaymentResult(request.getOrderId(), result);
    }

    @Transactional
    protected PaymentResult savePaymentResult(Long orderId, PaymentResult result) {
        Order order = orderRepository.findById(orderId).orElseThrow();
        Payment payment = Payment.of(order, result);
        paymentRepository.save(payment);
        order.complete();
        return result;
    }
}
```

외부 API 호출이 얼마나 걸리든 그것은 DB 트랜잭션과 무관해진다. DB 트랜잭션은 결과를 저장하는 짧은 순간만 유지된다.

### JPA와 JdbcTemplate을 한 트랜잭션에서 손잡기

JPA로 엔티티를 저장하고 같은 트랜잭션 안에서 JdbcTemplate으로 네이티브 SQL을 쓰고 싶을 때가 있다. 이때 주의할 점이 있다. JPA의 변경 감지는 flush 시점에 SQL을 생성하는데, 그 전에 JdbcTemplate으로 같은 테이블을 조회하면 아직 반영되지 않은 상태를 읽어 찜찜해진다.

```java
@Transactional
public void hybridOperation(Long orderId) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    order.updateStatus(OrderStatus.PROCESSING);
    
    // JPA 변경을 DB에 먼저 반영
    entityManager.flush();
    
    // 이제 JdbcTemplate으로 같은 데이터를 정확히 읽을 수 있다
    int relatedCount = jdbcTemplate.queryForObject(
        "SELECT COUNT(*) FROM order_item WHERE order_id = ? AND status = 'ACTIVE'",
        Integer.class, orderId
    );
    
    // relatedCount를 기반으로 추가 처리
    if (relatedCount > 0) {
        jdbcTemplate.update(
            "UPDATE order_item SET status = 'PROCESSING' WHERE order_id = ?",
            orderId
        );
    }
}
```

`entityManager.flush()` 호출이 핵심이다. JPA pending 쓰기를 DB에 반영한 뒤 JdbcTemplate으로 조회하면 최신 상태를 정확히 읽는다. 이 패턴은 JPA와 native SQL이 같은 트랜잭션에서 공존할 수 있게 하는 다리다.

---

## 낙관적 락 — `@Version`과 재시도

충돌이 드문 상황에서는 낙관적 락이 좋은 선택이다. 잠금을 걸지 않으니 대기가 없고, 처리량도 높다. 대신 충돌이 발생하면 예외를 던지므로 재시도 로직이 필요하다.

```java
@Entity
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private int stockQuantity;

    @Version
    private Long version; // 낙관적 락의 버전 컬럼

    public void decreaseStock(int quantity) {
        if (this.stockQuantity < quantity) {
            throw new InsufficientStockException();
        }
        this.stockQuantity -= quantity;
    }
}
```

```java
// 재시도 로직을 @Retryable로 선언
@Service
@RequiredArgsConstructor
public class StockService {

    private final ProductRepository productRepository;

    @Retryable(
        retryFor = OptimisticLockingFailureException.class,
        maxAttempts = 3,
        backoff = @Backoff(delay = 100, multiplier = 2)
    )
    @Transactional
    public void decreaseStock(Long productId, int quantity) {
        Product product = productRepository.findById(productId)
            .orElseThrow();
        product.decreaseStock(quantity); // version 불일치 시 예외
    }

    @Recover
    public void handleOptimisticLockFailure(
            OptimisticLockingFailureException e, Long productId, int quantity) {
        log.error("재고 감소 최종 실패: productId={}, quantity={}", productId, quantity);
        throw new StockUpdateFailedException("재고 업데이트에 실패했습니다. 잠시 후 다시 시도해주세요.");
    }
}
```

낙관적 락의 재시도 페이로드는 **멱등(idempotent)** 이어야 한다. 같은 요청을 세 번 재시도해도 결과가 하나여야 한다는 뜻이다. 재시도마다 새 엔티티를 만들거나 중복 처리를 허용하는 설계라면 낙관적 락과 재시도의 조합이 오히려 위험해진다.

버전 컬럼은 INSERT 시 0으로 시작해 UPDATE마다 1씩 증가한다. 두 트랜잭션이 같은 버전으로 UPDATE를 시도하면 하나만 성공하고 나머지는 `OptimisticLockingFailureException`을 받는다. 이것이 낙관적 락의 전부다.

---

## 비관적 락 — `@Lock(PESSIMISTIC_WRITE)`

충돌이 잦고 재시도 비용이 높다면 비관적 락이 낫다. 읽는 시점부터 독점 락을 걸어 다른 트랜잭션이 기다리게 만든다.

```java
// 레포지토리: 비관적 락으로 조회
public interface ProductRepository extends JpaRepository<Product, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithLock(@Param("id") Long id);

    // 타임아웃 설정 (10초)
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints({
        @QueryHint(name = "jakarta.persistence.lock.timeout", value = "10000")
    })
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithLockAndTimeout(@Param("id") Long id);
}
```

```java
@Service
@RequiredArgsConstructor
public class FlashSaleService {

    private final ProductRepository productRepository;

    @Transactional
    public void processPurchase(Long productId, int quantity) {
        // SELECT ... FOR UPDATE
        Product product = productRepository.findByIdWithLock(productId)
            .orElseThrow(() -> new ProductNotFoundException(productId));

        product.decreaseStock(quantity);
        // 트랜잭션 종료 시 락 해제
    }
}
```

`@Lock(LockModeType.PESSIMISTIC_WRITE)`은 `SELECT ... FOR UPDATE`를 생성한다. 이 트랜잭션이 종료될 때까지 같은 row를 건드리려는 다른 트랜잭션은 기다린다.

비관적 락의 주의점은 **락 획득 대기 시간**이다. 기다리다가 `LockTimeoutException`이 발생할 수 있으므로 타임아웃을 명시하는 편이 낫다. 타임아웃 없이 쓰면 무한 대기가 될 수 있다 — 그것도 꽤 난감한 상황이다.

또 한 가지. 비관적 락은 레코드 단위다. 같은 상품을 여러 트랜잭션이 동시에 구매하려면 이들이 줄 서서 기다린다. 이 대기 시간이 너무 길어지면 커넥션 풀이 고갈된다. 순간 트래픽 집중이 예상된다면 named lock 분산락 패턴을 고려해보자.

---

## MySQL Named Lock — 분산락의 실용 패턴

여러 애플리케이션 인스턴스가 같은 리소스를 동시에 처리하지 않아야 할 때, 가장 간단한 분산락 매개체는 MySQL named lock이다.

`GET_LOCK("ad:campaign:42", 10)`은 "ad:campaign:42"라는 이름의 락을 최대 10초 기다려서 획득한다. 성공하면 1, 실패하면 0을 반환한다. `RELEASE_LOCK("ad:campaign:42")`로 해제한다.

우아한형제들은 광고 시스템에서 이 패턴을 실제로 운영했다. 핵심 인사이트는 두 가지다.

첫째, **락 획득용 커넥션 풀을 비즈니스 로직 풀과 반드시 분리**하는 것이 낫다. named lock은 커넥션에 묶인다. 비즈니스 커넥션 풀로 락을 잡으면 락을 들고 있는 커넥션이 풀을 점유해 다른 비즈니스 처리가 커넥션을 못 얻는 상황이 생긴다.

둘째, MySQL 5.7.5 미만에서는 한 세션에서 하나의 named lock만 유지된다. `GET_LOCK("lock_b")`를 다시 호출하면 이전에 잡은 `lock_a`가 자동으로 해제된다 — 모르고 쓰면 대형 사고다.

```java
// 별도 커넥션 풀 설정
@Configuration
public class LockDataSourceConfig {

    @Bean(name = "lockDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.lock")
    public DataSource lockDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name = "lockJdbcTemplate")
    public JdbcTemplate lockJdbcTemplate(
            @Qualifier("lockDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```

```yaml
# application.yml: 락 전용 커넥션 풀
spring:
  datasource:
    lock:
      url: jdbc:mysql://localhost:3306/mydb?rewriteBatchedStatements=true
      username: app_user
      password: secret
      hikari:
        pool-name: lock-pool
        maximum-pool-size: 10  # 비즈니스 풀보다 훨씬 작게
        minimum-idle: 2
```

```java
@Component
@RequiredArgsConstructor
public class MysqlNamedLockManager {

    @Qualifier("lockJdbcTemplate")
    private final JdbcTemplate lockJdbcTemplate;

    private static final int DEFAULT_TIMEOUT_SECONDS = 10;

    // 락 획득 후 작업 실행, 반드시 해제
    public <T> T executeWithLock(String lockName, Supplier<T> task) {
        return executeWithLock(lockName, DEFAULT_TIMEOUT_SECONDS, task);
    }

    public <T> T executeWithLock(String lockName, int timeoutSeconds, Supplier<T> task) {
        boolean acquired = acquireLock(lockName, timeoutSeconds);
        if (!acquired) {
            throw new LockAcquisitionException("락 획득 실패: " + lockName);
        }
        try {
            return task.get();
        } finally {
            releaseLock(lockName); // 예외가 나도 반드시 해제
        }
    }

    private boolean acquireLock(String lockName, int timeoutSeconds) {
        Integer result = lockJdbcTemplate.queryForObject(
            "SELECT GET_LOCK(?, ?)",
            Integer.class, lockName, timeoutSeconds
        );
        return Integer.valueOf(1).equals(result);
    }

    private void releaseLock(String lockName) {
        lockJdbcTemplate.queryForObject(
            "SELECT RELEASE_LOCK(?)",
            Integer.class, lockName
        );
    }
}
```

```java
// 사용 예시: 광고 캠페인 예산 차감
@Service
@RequiredArgsConstructor
public class AdBudgetService {

    private final MysqlNamedLockManager lockManager;
    private final CampaignRepository campaignRepository;

    public void deductBudget(Long campaignId, BigDecimal amount) {
        String lockName = "ad:campaign:" + campaignId;

        lockManager.executeWithLock(lockName, () -> {
            Campaign campaign = campaignRepository.findById(campaignId)
                .orElseThrow();
            campaign.deductBudget(amount);
            campaignRepository.save(campaign);
            return null;
        });
    }
}
```

`Supplier<T>` 콜백으로 작업을 감싸면 락 획득/해제 책임이 `MysqlNamedLockManager`에 집중된다. 비즈니스 코드는 락이 어떻게 구현됐는지 신경 쓸 필요 없이 콜백만 건네면 된다.

락 이름은 리소스를 고유하게 식별해야 한다. `"ad:campaign:42"`처럼 도메인 + 구분자 + ID 조합이 좋다. 락 이름이 너무 짧거나 범용적이면 의도하지 않은 충돌이 생긴다.

### Named Lock vs Redis Redlock

MySQL named lock과 Redis Redlock은 둘 다 분산락이지만 성격이 다르다.

| 관점 | MySQL Named Lock | Redis Redlock |
|------|-----------------|---------------|
| 일관성 | DB 트랜잭션과 묶임 → 보수적 | 분리된 저장소 → 별도 관리 |
| 속도 | DB 왕복 비용 있음 | 메모리 기반 → 빠름 |
| 운영 복잡도 | 이미 MySQL 있으면 추가 인프라 없음 | Redis 별도 운영 필요 |
| 락 만료 | 세션 종료 시 자동 해제 | TTL 기반 자동 만료 |
| 장애 내성 | MySQL이 단일 장애점 | Redis 클러스터로 HA 가능 |

이미 MySQL을 쓰고 있고, 락 빈도가 높지 않으며, 일관성을 더 중요하게 여긴다면 MySQL named lock이 간단하고 안전한 선택이다. 반면 락 빈도가 높고 성능이 중요하다면 Redis Redlock 쪽으로 기울여볼 수 있다. 어느 쪽이 "더 낫다"고 단정하기보다, 우리 워크로드의 특성을 먼저 파악하는 편이 낫다.

---

## 락 순서 일관성 — 데드락 사이클 차단

코드에 비관적 락을 쓰는 곳이 여러 군데 있다면 락 순서를 일관되게 유지하자. 3장에서 데드락 메커니즘을 보았듯이, 두 트랜잭션이 서로 다른 순서로 락을 획득하려 하면 사이클이 생긴다.

고전적인 예시다. 트랜잭션 A는 먼저 계좌 1을 잠그고 그다음 계좌 2를 잠그려 한다. 트랜잭션 B는 먼저 계좌 2를 잠그고 그다음 계좌 1을 잠그려 한다. 이들이 동시에 실행되면 사이클이 생긴다.

```java
// 데드락 위험: 락 순서가 보장되지 않음
@Transactional
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    Account from = accountRepository.findByIdWithLock(fromId).orElseThrow();
    Account to = accountRepository.findByIdWithLock(toId).orElseThrow();
    from.withdraw(amount);
    to.deposit(amount);
}

// 개선: 정렬된 순서로 락 획득
@Transactional
public void transferSafe(Long fromId, Long toId, BigDecimal amount) {
    // ID가 작은 쪽을 먼저 잠근다
    Long firstId = Math.min(fromId, toId);
    Long secondId = Math.max(fromId, toId);

    Account first = accountRepository.findByIdWithLock(firstId).orElseThrow();
    Account second = accountRepository.findByIdWithLock(secondId).orElseThrow();

    Account from = fromId.equals(firstId) ? first : second;
    Account to = toId.equals(firstId) ? first : second;

    from.withdraw(amount);
    to.deposit(amount);
}
```

항상 id가 작은 계좌를 먼저 잠그면, 어떤 두 트랜잭션이 같은 두 계좌를 건드리더라도 같은 순서로 락을 획득한다. 데드락 사이클 자체가 생기지 않는다.

이 원칙을 더 넓게 적용하면 "여러 리소스를 동시에 잠가야 할 때는 항상 정렬된 순서로"가 된다. 주문 → 재고 → 계좌 순서를 애플리케이션 전체에서 일관되게 유지하면 이 종류의 데드락은 원천 차단된다.

---

## 영속성 컨텍스트와 배치 처리 — flush/clear의 타이밍

배치 처리 중 만 단위 엔티티가 영속성 컨텍스트에 쌓이면 어떻게 될까? 힙 메모리가 폭발하거나, 1차 캐시에서 같은 엔티티를 계속 찾느라 처리 속도가 떨어진다.

```java
@Service
@RequiredArgsConstructor
public class ProductSyncService {

    private final EntityManager entityManager;
    private final ProductRepository productRepository;

    @Transactional
    public void syncProducts(List<ProductData> dataList) {
        int batchSize = 100;

        for (int i = 0; i < dataList.size(); i++) {
            ProductData data = dataList.get(i);
            Product product = Product.from(data);
            entityManager.persist(product);

            // 100건마다 flush + clear
            if (i % batchSize == 0) {
                entityManager.flush();  // DB에 반영
                entityManager.clear();  // 1차 캐시 비움
            }
        }

        // 남은 것 처리
        entityManager.flush();
    }
}
```

`flush()`와 `clear()`를 100건 단위로 주기적으로 호출하면 영속성 컨텍스트에 쌓이는 엔티티 수를 통제할 수 있다. `flush()`는 변경을 DB에 반영하고, `clear()`는 1차 캐시를 비운다. 이 둘이 한 쌍이다. `clear()` 없이 `flush()`만 하면 엔티티가 메모리에서 계속 쌓인다.

기억해두자. 배치 처리 중 `OutOfMemoryError`가 난다면 십중팔구 주기적인 `flush()`와 `clear()`가 빠졌기 때문이다.

---

## 마무리

JPA는 편리하다. 하지만 그 편리함의 이면을 알아야 한계를 현명하게 넘을 수 있다.

배치 INSERT 100배 개선은 세 가지 설정의 합주였다. `jdbc.batch_size`, `order_inserts`, `rewriteBatchedStatements`가 모두 켜져야 한다. IDENTITY 전략은 배치의 적이다. 수백만 row를 지워야 한다면 한 방에 날리지 말고 청크로 나누는 편이 낫다. 외부 IO는 트랜잭션 밖으로 빼두자.

낙관적 락은 충돌이 드물 때, 비관적 락은 충돌이 잦을 때. 두 인스턴스 이상에서 같은 리소스를 건드린다면 named lock을 고려해보자. 그때 커넥션 풀 분리를 빠뜨리면 락이 비즈니스 커넥션을 잡아먹는다.

락 순서는 애플리케이션 전체에서 일관되게 유지해야 데드락 사이클이 생기지 않는다. 배치 중 영속성 컨텍스트가 폭발하지 않으려면 `flush()`와 `clear()`를 주기적으로 호출하자.

다음 장에서는 데이터베이스 인프라로 시야를 넓힌다. AWS RDS와 Aurora 사이의 분기점 — 어떤 워크로드에서 어떤 선택이 맞는지를 함께 따져보자.

---

## 참고 자료

- 우아한형제들 — 하이버네이트 배치 설정: https://techblog.woowahan.com/2695/
- 우아한형제들 — MySQL을 이용한 분산락: https://techblog.woowahan.com/2631/
- 권남이 위키 — MySQL User Lock: https://kwonnam.pe.kr/wiki/database/mysql/user_lock
- haon.blog — MySQL 네임드 락으로 분산 환경에서의 동시성 이슈 해결: https://haon.blog/database/named-lock/
- Baeldung — Optimistic Locking in JPA: https://www.baeldung.com/jpa-optimistic-locking
- CodeWiz — Locking strategies in Spring Boot: https://codewiz.info/blog/locking-strategies-spring-boot/
- Medium — Spring Boot JPA Bulk Insert Performance by 100 times: https://dev.to/amrutprabhu/spring-boot-jpa-bulk-insert-performance-by-100-times-fn4


# 11장. AWS RDS와 Aurora — 인스턴스 선택·복제·분할의 분기점

"우리 서비스에 Aurora를 써야 할까요, RDS로 충분할까요?"

이 질문은 스프링 개발자가 인프라를 처음 결정할 때 가장 많이 마주치는 질문 중 하나다. 답을 먼저 말하면 — 상황에 따라 다르다. 이렇게 말하면 무책임하게 들릴 수 있지만, 진짜 핵심은 어떤 기준으로 상황을 판단하느냐다. 그 기준을 네 가지 분기점으로 정리하고, 실제 운영 사례를 통해 각각의 무게를 느껴보자.

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

읽기 트래픽이 쓰기의 5~10배 이상이고 읽기 일관성에 민감하다면, Aurora 쪽으로 기울이는 편이 자연스럽다.

### 분기점 2: 페일오버 RTO가 중요한가?

RTO(Recovery Time Objective)는 장애 발생 후 서비스를 복구하는 데 걸리는 목표 시간이다.

RDS for MySQL의 Multi-AZ 페일오버는 약 60~120초가 걸린다. DNS 업데이트와 새 인스턴스의 MySQL 기동이 포함된다.

Aurora는 15~30초다. 공유 스토리지 덕분에 리플리카를 Writer로 승격할 때 데이터를 다시 동기화할 필요가 없기 때문이다. 리플리카는 이미 최신 데이터를 갖고 있다.

금융 서비스처럼 몇 십 초의 장애도 민감한 영역이라면 Aurora 쪽 RTO가 유리하다. 반면 배치 처리 위주라면 수분 단위 페일오버도 감수할 수 있다.

### 분기점 3: IO 집약적 워크로드인가?

Aurora의 스토리지는 IO 요청마다 비용이 발생한다. 쓰기가 많은 워크로드에서는 I/O 비용이 상당히 올라간다. AWS는 이를 위해 "Aurora I/O-Optimized" 요금 모델을 내놓았는데, IO 비용 대신 인스턴스 요금이 올라가는 구조다. 어느 쪽이 더 저렴한지는 실제 워크로드 패턴과 최신 가격에 따라 달라지니, 직접 AWS 비용 계산기로 확인해보는 편이 낫다.

순수 읽기 위주(OLTP에서 95% 이상 읽기)이거나, 쓰기가 빈번하면서 비용에 민감하다면 RDS의 예측 가능한 EBS 비용이 더 단순하게 느껴질 수 있다.

### 분기점 4: 벤더 락-인을 감수할 수 있나?

Aurora MySQL은 MySQL 호환을 표방하지만 일부 동작이 다르다. Aurora 고유 함수, 스토리지 파라미터, DDL 동작 등이 표준 MySQL과 미묘하게 다를 수 있다. 나중에 Aurora를 벗어나 다른 MySQL 환경으로 이전해야 한다면 번거로운 일이 생길 수 있다.

단순한 워크로드이고 이식성이 중요하다면 RDS for MySQL이 더 안전한 선택일 수 있다.

---

## Aurora MySQL의 대용량 DDL 약점

Aurora가 모든 면에서 우위인 것은 아니다. 주목할 만한 약점이 있다. 우아한형제들의 경험이 여기서 중요한 참고가 된다.

200GB 테이블에 인덱스를 추가하는 작업이 Aurora MySQL에서 1시간 이상 걸렸다. Aurora의 분산 스토리지 구조가 대용량 DDL에서는 오히려 병목이 됐다는 이야기다. 같은 상황에서 PostgreSQL의 partial index는 약 40분에 끝났다고 한다.

대용량 테이블에 인덱스를 무중단으로 추가해야 한다면 `pt-online-schema-change`나 `gh-ost` 같은 도구를 진지하게 고려해보자.

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

Aurora에서 gh-ost를 쓰려면 binlog를 명시적으로 활성화해두는 편이 낫다. Aurora는 기본적으로 내부 redo 로그만 쓰고 binlog는 선택 사항이다. gh-ost가 binlog를 파싱해 변경을 추적하기 때문에 이 설정이 필요하다.

---

## Aurora vs RDS 백업 모델 차이

백업·복구·PITR 워크플로의 실제 운영은 다음 12장에서 자세히 다룬다. 여기서는 두 서비스의 백업 모델 차이만 짧게 짚고 가자.

**RDS for MySQL**은 자동 백업(1~35일 보관), 수동 스냅샷, binlog 기반 PITR을 제공한다. PITR 복구는 가장 가까운 자동 백업 스냅샷을 기점으로 binlog를 적용하는 방식이다.

**Aurora MySQL**은 자동 백업이 분산 스토리지에 지속적으로 기록된다. 백업 윈도우가 따로 없고, 1초 단위 PITR이 가능하다. 스냅샷도 증분 방식이라 빠르다.

실제 RPO(목표 복구 지점)나 RTO를 측정하는 방법, 분기별 PITR 리허설 워크플로는 12장에서 함께 실습해보자.

---

## 복제: GTID, 반동기, 그룹 복제

### GTID — 복제 위치 추적의 혁신

리플리카가 어디까지 따라왔는지 어떻게 알 수 있을까? 옛 방식은 binlog 파일명(`mysql-bin.000123`)과 그 안의 바이트 위치(`Position: 4567`)로 추적했다. 페일오버 상황이 되면 새 Writer의 binlog 파일명과 위치를 모든 리플리카에 다시 알려줘야 했다. 이 계산이 미묘하게 어긋나면 데이터가 중복되거나 누락된다. 끔찍한 일이다.

GTID(Global Transaction Identifier)는 이 문제를 정면으로 풀었다. `server_uuid:transaction_number` 형식으로 각 트랜잭션에 전역 고유 식별자를 붙인다. 어느 서버의 몇 번째 트랜잭션인지가 식별자 자체에 들어 있다.

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

GTID가 활성화된 환경에서는 리플리카를 새 소스로 승격할 때 binlog 파일명과 위치를 직접 계산할 필요가 없다. 리플리카가 어떤 트랜잭션을 가지고 있는지가 GTID로 명확히 표현되기 때문이다. orchestrator나 MHA 같은 자동 페일오버 도구도 GTID 환경을 전제로 설계됐다.

그렇다면 GTID에는 단점이 없을까? 제약이 몇 가지 있다. `CREATE TABLE ... SELECT`나 일부 비트랜잭션 명령은 GTID와 충돌할 수 있다. 또 임시 테이블을 트랜잭션 안에서 만들면 GTID 추적이 어긋난다. 레거시 코드에 이런 패턴이 있다면 마이그레이션 전에 점검하는 편이 낫다.

### 반동기 복제 — 데이터 손실과 성능의 균형

그렇다면 비동기 복제는 어떤 경우에 부족할까. 기본 비동기 복제는 빠르지만, 소스 장애 시 아직 리플리카에 전달되지 않은 트랜잭션을 잃을 수 있다. 결제처럼 한 트랜잭션도 잃으면 안 되는 도메인이라면 찜찜한 일이다.

반동기 복제(semi-synchronous replication)는 최소 하나의 리플리카가 트랜잭션을 받았다는 ACK를 응답할 때까지 커밋을 기다린다. 완전 동기는 아니다 — 리플리카가 적용까지 마칠 때까지 기다리지는 않는다. 받았다는 사실까지만 확인한다. 그 사이의 균형이다.

```sql
-- 반동기 복제 플러그인 확인
SHOW PLUGINS;
-- rpl_semi_sync_source_enabled (소스)
-- rpl_semi_sync_replica_enabled (리플리카)

-- 타임아웃 설정 (1000ms)
SET GLOBAL rpl_semi_sync_source_timeout = 1000;
-- 타임아웃 초과 시 비동기로 폴백

-- 반동기 통계
SHOW STATUS LIKE 'Rpl_semi_sync%';
-- Rpl_semi_sync_source_status: ON (반동기 활성)
-- Rpl_semi_sync_source_tx_avg_wait_time: 평균 대기 시간 (ms)
-- Rpl_semi_sync_source_yes_tx: 반동기로 커밋된 트랜잭션 수
-- Rpl_semi_sync_source_no_tx: 비동기로 폴백된 트랜잭션 수
```

반동기의 타임아웃 폴백을 기억해두자. 리플리카가 느리거나 네트워크가 불안정하면 타임아웃 후 비동기로 자동 전환된다. 이 폴백을 모르고 있으면 "반동기 설정했는데 왜 데이터가 사라졌죠?"라는 당황스러운 상황을 만날 수 있다. 운영 중에는 `Rpl_semi_sync_source_no_tx` 카운트를 주기적으로 봐두는 편이 낫다.

### 그룹 복제(MGR)와 InnoDB Cluster

반동기에서 한 발 더 나가면 그룹 복제(MGR, Group Replication)다. Paxos 합의 알고리즘으로 여러 노드가 합의하에 커밋한다. 자동 페일오버를 기본으로 지원하고, 멀티-마스터 모드(단, 충돌 감지 있음)도 가능하다. 노드 하나가 죽어도 다수결이 유지되면 클러스터가 자동으로 새 Primary를 뽑는다.

InnoDB Cluster는 MGR + MySQL Shell + MySQL Router를 묶은 솔루션으로, 클러스터 관리와 애플리케이션 라우팅을 패키지로 제공한다. MySQL Shell의 `dba.createCluster()` 명령 한 줄로 클러스터를 초기화할 수 있을 정도로 운영 자동화가 잘 돼 있다.

물론 좋은 점만 있는 것은 아니다. MGR에는 몇 가지 무거운 제약이 있다.

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

MGR은 최대 9개 노드까지만 지원하고, 합의 비용 때문에 피크 처리량이 반동기보다 낮을 수 있다. 자동 페일오버 자체가 강한 요건이고 운영 자동화가 우선이라면 고려해볼 만하다. 반면 단일 노드의 처리량이 절대적으로 중요한 워크로드라면 반동기 + orchestrator 조합이 더 단단할 수 있다.

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

그렇다면 파티셔닝으로 충분한지, 샤딩이 필요한지의 기준은 어디일까. 단일 인스턴스의 IOPS나 스토리지 한계에 닿았는지, 쿼리 패턴이 파티션 키를 항상 포함하는지, 파티션 키로 자연스럽게 범위를 나눌 수 있는지 — 이 세 가지가 모두 맞다면 파티셔닝이 더 단순한 출발점이다.

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

복제는 GTID가 페일오버를 단순화하고, 반동기는 데이터 손실 위험을 줄이지만 타임아웃 폴백을 잊지 말자. MGR은 자동 페일오버가 매력이지만 PK 강제와 노드 수 제약이 따라온다. 파티셔닝은 단일 인스턴스 안에서 테이블을 나누는 것이고, 샤딩은 인스턴스를 나누는 것이다 — 이 경계를 명확히 인식하고 필요에 따라 단계적으로 접근하는 편이 낫다.

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


# 13장. 통합 사례 — 결제 시스템 한 건을 끝까지 분해해 보자

"이론은 알겠는데, 실제로는 어떻게 짜야 하죠?"

책을 읽으면서 이 질문을 한 번쯤 했을 것이다. 인덱스 설계는 4장에서 배웠고, 락 패턴은 10장에서, 복제는 11장에서, 관측과 백업은 12장에서. 그런데 이 조각들이 실제 서비스에서 어떻게 맞물려 돌아가는지는 다른 이야기다.

가상의 결제 시스템을 처음부터 끝까지 분해해보자. 도메인 모델링, 스키마, 인덱스, 트랜잭션 경계, 동시성 처리, 슬로우 쿼리 대응, PITR 복구까지 — 앞 챕터들의 도구들이 한 줄로 연결되는 감각을 함께 느껴보자.

---

## 결제 도메인 — 4개 애그리거트

결제 시스템은 크게 네 개의 애그리거트로 나눌 수 있다.

- **주문(Order)**: 사용자가 무엇을 얼마에 구매하는지
- **결제(Payment)**: 실제 금액 이동, PG와의 인터페이스
- **정산(Settlement)**: 판매자에게 얼마를 언제 정산할지
- **포인트(Point)**: 사용자 포인트 적립/사용

각 애그리거트는 자신의 트랜잭션 경계를 가진다. "주문 하나에 결제·정산·포인트를 한 트랜잭션에서 처리해야 하나요?" — 이 질문을 처음 받으면 당황스럽다. 정답은 없지만 기준은 있다.

DDD 원칙에서 애그리거트 간 트랜잭션은 결과적 일관성(eventual consistency)으로 가는 편이 낫다. 한 트랜잭션이 길어질수록 락이 오래 유지되고, 실패 시 롤백 범위가 커진다.

---

## 도메인 모델링에서 스키마까지

### 스키마 설계

```sql
-- 주문 애그리거트
CREATE TABLE orders (
    id              BIGINT          NOT NULL AUTO_INCREMENT,
    user_id         BIGINT          NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    total_amount    DECIMAL(10, 2)  NOT NULL,
    created_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                                    ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX idx_user_status (user_id, status),        -- 사용자별 주문 목록
    INDEX idx_created_at (created_at)               -- 날짜 범위 조회
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 주문 상품 (주문 애그리거트 내부)
CREATE TABLE order_items (
    id          BIGINT          NOT NULL AUTO_INCREMENT,
    order_id    BIGINT          NOT NULL,
    product_id  BIGINT          NOT NULL,
    quantity    INT             NOT NULL,
    unit_price  DECIMAL(10, 2)  NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_order_id (order_id),              -- 주문별 상품 조회
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 결제 애그리거트
CREATE TABLE payments (
    id              BIGINT          NOT NULL AUTO_INCREMENT,
    order_id        BIGINT          NOT NULL,
    pg_transaction_id VARCHAR(100)  NULL,           -- PG사 트랜잭션 ID
    status          VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    amount          DECIMAL(10, 2)  NOT NULL,
    method          VARCHAR(20)     NOT NULL,        -- CARD, TRANSFER, POINT
    paid_at         DATETIME(6)     NULL,
    created_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE INDEX idx_pg_transaction_id (pg_transaction_id),  -- PG 트랜잭션 중복 방지
    INDEX idx_order_id (order_id),
    INDEX idx_status_created (status, created_at)   -- 상태별 정산 대상 조회
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 정산 애그리거트
CREATE TABLE settlements (
    id              BIGINT          NOT NULL AUTO_INCREMENT,
    seller_id       BIGINT          NOT NULL,
    payment_id      BIGINT          NOT NULL,
    amount          DECIMAL(10, 2)  NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    settled_at      DATE            NULL,
    created_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX idx_seller_status (seller_id, status, settled_at),
    INDEX idx_payment_id (payment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 포인트 원장
CREATE TABLE point_ledger (
    id          BIGINT          NOT NULL AUTO_INCREMENT,
    user_id     BIGINT          NOT NULL,
    amount      DECIMAL(10, 2)  NOT NULL,            -- 양수: 적립, 음수: 사용
    type        VARCHAR(20)     NOT NULL,             -- EARN, USE, EXPIRE
    ref_id      BIGINT          NOT NULL,             -- 참조 ID (order_id 등)
    ref_type    VARCHAR(20)     NOT NULL,             -- 참조 유형
    created_at  DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX idx_user_created (user_id, created_at)     -- 사용자 포인트 이력
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

포인트 잔액을 별도 `user_points` 테이블에 두고 싶은 충동이 생긴다. 빠르게 현재 잔액을 알 수 있으니. 하지만 원장(ledger) 패턴이 더 안전하다. 각 거래를 append-only로 기록하고, 잔액은 sum으로 계산한다. 원장이 있으면 어느 시점의 잔액이든 재계산할 수 있고, 감사 추적도 된다.

> **다른 도메인으로 옮긴다면** — 이커머스 재고 도메인에서는 `stock_ledger`로 같은 패턴을 쓸 수 있다. 입고(+), 출고(-), 취소(+) 이벤트를 append-only로 쌓으면 재고 이력 추적과 시점별 재고 계산이 모두 된다. 단, 재고 조회 빈도가 매우 높다면 materialized view나 별도 `current_stock` 테이블로 최신 값을 캐싱하는 것을 고려해보자.

---

## 동시성 시나리오 — 같은 상품 결제 폭주

인기 상품 한정 판매 이벤트를 상상해보자. 1,000명이 동시에 같은 상품을 결제하려 한다. 재고는 100개. 이 상황에서 어떤 락 전략을 써야 할까?

충돌이 매우 빈번하다. 낙관적 락이라면 `@Retryable`과 결합하더라도 900건이 실패를 경험하고 재시도한다. 이 와중에 DB에 불필요한 부하가 집중된다.

비관적 락이 맞는 선택이다. 하지만 단순히 `@Lock(PESSIMISTIC_WRITE)`로 상품을 잠그면, 1,000개의 커넥션이 그 락을 기다리며 커넥션 풀을 잡는다. 그 상황이 얼마나 번거로운지 상상해보자.

Named lock이 적절하다. 락을 비즈니스 커넥션 풀과 분리하고, 락을 얻은 요청만 처리하도록 설계한다.

```java
// 결제 처리 서비스: named lock으로 상품별 직렬화
@Service
@RequiredArgsConstructor
public class PaymentProcessingService {

    private final MysqlNamedLockManager lockManager;
    private final ProductRepository productRepository;
    private final OrderRepository orderRepository;
    private final PaymentRepository paymentRepository;

    public PaymentResult processPayment(PaymentCommand command) {
        String lockName = "payment:product:" + command.getProductId();

        return lockManager.executeWithLock(lockName, 5, () -> {
            // 락 안에서: 재고 확인 → 차감 → 주문 생성 → 결제 생성
            return doProcessPayment(command);
        });
    }

    @Transactional
    protected PaymentResult doProcessPayment(PaymentCommand command) {
        // 재고 확인 및 차감 (락 안에서 안전)
        Product product = productRepository.findByIdWithLock(command.getProductId())
            .orElseThrow();

        if (product.getStockQuantity() < command.getQuantity()) {
            throw new InsufficientStockException("재고가 부족합니다.");
        }
        product.decreaseStock(command.getQuantity());

        // 주문 생성
        Order order = Order.create(command.getUserId(), product, command.getQuantity());
        orderRepository.save(order);

        // 결제 레코드 생성 (PG 호출은 트랜잭션 밖에서)
        Payment payment = Payment.pending(order, command);
        paymentRepository.save(payment);

        return PaymentResult.of(order, payment);
    }
}
```

named lock 안에서 `@Transactional` 메서드를 호출한다. 락이 있으니 같은 상품에 대한 동시 결제 요청은 직렬화된다. 각 요청은 재고를 정확히 확인하고 차감한다.

PG API 호출은 이 코드에 없다. 결제 레코드는 `PENDING` 상태로 만들고, 실제 PG 호출은 별도의 단계에서 트랜잭션 밖에서 처리한다. 10장에서 배운 외부 IO를 트랜잭션 밖으로 패턴이다.

> **다른 도메인으로 옮긴다면** — SaaS 멀티테넌시에서 테넌트별 리소스 한도 초과를 막아야 할 때도 같은 패턴이 쓰인다. `"quota:tenant:{tenantId}"` named lock으로 동시 요청을 직렬화하고, 현재 사용량을 확인한 뒤 한도 내에서만 처리한다. 테넌트 수가 많을수록 락 이름이 세분화되어 락 경합이 줄어든다.

---

## 보고서 — 일별 정산 쿼리

매일 밤 정산 배치가 돌아간다. 판매자별로 당일 결제된 금액을 집계하고, 수수료를 계산해 정산 레코드를 만든다.

```sql
-- 일별 판매자 정산 집계 (윈도우 함수 + CTE)
WITH daily_payments AS (
    -- 오늘 완료된 결제
    SELECT
        s.seller_id,
        p.id AS payment_id,
        p.amount,
        p.paid_at
    FROM payments p
    JOIN settlements s ON s.payment_id = p.id
    WHERE p.status = 'COMPLETED'
      AND DATE(p.paid_at) = CURDATE()
),
seller_daily_summary AS (
    -- 판매자별 일별 집계
    SELECT
        seller_id,
        SUM(amount)                        AS total_amount,
        COUNT(*)                           AS payment_count,
        SUM(amount) * 0.032                AS commission,    -- 수수료 3.2%
        SUM(amount) * (1 - 0.032)          AS net_amount
    FROM daily_payments
    GROUP BY seller_id
),
seller_cumulative AS (
    -- 이번 달 누적 (윈도우 함수)
    SELECT
        s2.seller_id,
        s2.net_amount AS today_net,
        SUM(s2.net_amount) OVER (
            PARTITION BY s2.seller_id
            ORDER BY DATE(s2.created_at)
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS monthly_cumulative
    FROM settlements s2
    WHERE MONTH(s2.created_at) = MONTH(CURDATE())
      AND s2.status = 'COMPLETED'
)
SELECT
    ds.seller_id,
    ds.total_amount,
    ds.payment_count,
    ds.commission,
    ds.net_amount,
    sc.monthly_cumulative
FROM seller_daily_summary ds
LEFT JOIN seller_cumulative sc ON sc.seller_id = ds.seller_id
ORDER BY ds.net_amount DESC;
```

이 쿼리가 EXPLAIN ANALYZE에서 어떻게 실행되는지 확인해보자. `settlements.seller_id + status + created_at` 복합 인덱스가 없다면 `seller_cumulative` CTE의 집계가 풀스캔을 한다. 6장의 윈도우 함수 패턴과 5장의 EXPLAIN ANALYZE를 함께 적용하는 순간이다.

```sql
-- 정산 집계 쿼리의 실행 계획 확인
EXPLAIN ANALYZE
WITH daily_payments AS (
    SELECT s.seller_id, p.amount
    FROM payments p
    JOIN settlements s ON s.payment_id = p.id
    WHERE p.status = 'COMPLETED'
      AND DATE(p.paid_at) = CURDATE()
)
SELECT seller_id, SUM(amount)
FROM daily_payments
GROUP BY seller_id;
-- actual rows와 estimated rows 괴리가 크면 ANALYZE TABLE 재실행
```

> **다른 도메인으로 옮긴다면** — B2B 대용량 배치에서는 이런 집계를 야간 배치로 처리한다. Spring Batch의 `JdbcCursorItemReader`로 대량 데이터를 청크 단위로 읽고, `JdbcBatchItemWriter`로 집계 결과를 쓰는 구조다. 청크 사이즈(예: 500~1,000)와 커밋 간격을 조율해 메모리 사용량과 락 유지 시간을 균형 있게 설정한다.

---

## 운영 시나리오 — 슬로우 쿼리 알람에서 인덱스 추가까지

월요일 아침 9시. 슬로우 쿼리 알람이 뜬다. 정산 조회 API의 p99 응답시간이 12초다.

`pt-query-digest`를 돌려보니 문제 쿼리가 잡힌다.

```sql
-- 문제 쿼리: 판매자 정산 목록 조회
SELECT s.*, p.amount, p.paid_at
FROM settlements s
JOIN payments p ON p.id = s.payment_id
WHERE s.seller_id = 1234
  AND s.status = 'PENDING'
ORDER BY s.created_at DESC
LIMIT 20;
```

`EXPLAIN ANALYZE`로 확인해보자.

```sql
EXPLAIN ANALYZE
SELECT s.*, p.amount, p.paid_at
FROM settlements s
JOIN payments p ON p.id = s.payment_id
WHERE s.seller_id = 1234
  AND s.status = 'PENDING'
ORDER BY s.created_at DESC
LIMIT 20;

-- 출력 예시:
-- -> Limit: 20 row(s)  (actual time=8234.5..8234.5 rows=20 loops=1)
--   -> Sort: settlements.created_at DESC  (actual rows=45000 loops=1)
--     -> Filter: (s.status = 'PENDING')  (actual rows=45000 loops=1)
--       -> Index scan on settlements using idx_seller_id
--                 (actual rows=89000 loops=1)
```

안쪽 노드부터 읽어보자. `idx_seller_id`를 써서 seller_id=1234인 행 89,000개를 읽고, status='PENDING'으로 필터링해 45,000개가 남고, 전부 정렬한 다음 20개를 돌려준다. 8초가 걸린 이유가 보인다.

복합 인덱스 `(seller_id, status, created_at)`을 추가하면 세 조건이 모두 인덱스에서 처리된다.

```sql
-- Invisible index로 먼저 테스트 (운영 영향 없이)
ALTER TABLE settlements
ADD INDEX idx_seller_status_created (seller_id, status, created_at) INVISIBLE;

-- 세션에서 invisible index 강제 사용
SET SESSION optimizer_switch = 'use_invisible_indexes=on';

EXPLAIN ANALYZE
SELECT s.*, p.amount, p.paid_at
FROM settlements s
JOIN payments p ON p.id = s.payment_id
WHERE s.seller_id = 1234
  AND s.status = 'PENDING'
ORDER BY s.created_at DESC
LIMIT 20;
-- 실행 시간이 얼마나 줄었는지 확인

-- 효과 확인 후 visible로 전환
ALTER TABLE settlements
ALTER INDEX idx_seller_status_created VISIBLE;
```

Invisible index로 실제 운영 쿼리에 영향 없이 새 인덱스의 효과를 확인하고, 그 다음 visible로 전환하는 4장의 패턴이 여기서 빛난다.

그런데 한 가지 더 확인할 게 있다. 새 인덱스를 추가하면 기존 `idx_seller_id` 단순 인덱스가 필요 없어질 수 있다. 사용되지 않는 인덱스는 INSERT/UPDATE 부하만 늘린다.

```sql
-- 인덱스 사용 통계 확인
SELECT INDEX_NAME, COUNT_READ, COUNT_WRITE
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA = 'mydb' AND OBJECT_NAME = 'settlements'
ORDER BY COUNT_READ DESC;
-- COUNT_READ가 0이거나 매우 낮은 인덱스는 Invisible로 비활성화 후 제거 검토
```

> **다른 도메인으로 옮긴다면** — 이커머스 재고 도메인에서 창고별·카테고리별 재고 조회가 느릴 때도 같은 절차를 따른다. EXPLAIN ANALYZE로 병목 노드를 찾고, 복합 인덱스 설계로 해결하고, Invisible index로 검증 후 적용한다.

---

## 월요일 새벽 백업 검증 실패 → PITR 리허설

밤새 자동으로 돌아야 할 PITR 리허설 배치가 슬랙에 실패 알림을 남겼다. "스냅샷 복원 완료됐는데 binlog 적용 중 오류."

실제 장애가 아니라 다행이지만, 이 신호를 무시하면 진짜 장애 때 망연자실하게 된다.

```bash
# 원인 파악: binlog 연속성 확인
mysqlbinlog --verbose /var/lib/mysql/binlog.000789 | head -50
# ERROR: Could not read entry at offset 4:
#   Error in log format or read error.
# -> binlog 파일 손상

# Aurora RDS라면: binlog 연속성을 AWS가 관리
# 자체 관리 MySQL이라면: binlog 보존 정책 확인
SHOW VARIABLES LIKE 'binlog_expire_logs_seconds';
-- binlog_expire_logs_seconds: 86400 (1일)
-- 너무 짧으면 PITR 윈도우가 1일로 제한됨

-- 더 긴 보존 기간으로 변경
SET GLOBAL binlog_expire_logs_seconds = 604800; -- 7일
```

이 경우 binlog 만료 기간이 너무 짧아 연속성이 끊겼다. 리허설에서 발견했으니 다행이다. 다음 분기 리허설 전에 만료 기간을 7일로 늘리고 binlog가 정상적으로 누적되는지 재확인하자.

Aurora RDS라면 자동 백업 보존 기간이 7~35일 범위에서 설정된다. "1일로 설정돼 있는데 아무도 몰랐다"는 일이 생각보다 흔하다. 설정을 한 번은 직접 확인해두는 편이 낫다.

```bash
# AWS CLI로 자동 백업 보존 기간 확인
aws rds describe-db-instances \
  --db-instance-identifier mydb-prod \
  --query 'DBInstances[0].BackupRetentionPeriod'
# 1 이면 너무 짧다

# 7일로 변경
aws rds modify-db-instance \
  --db-instance-identifier mydb-prod \
  --backup-retention-period 7 \
  --apply-immediately
```

> **다른 도메인으로 옮긴다면** — SaaS 멀티테넌시에서는 테넌트별 데이터 복구 요청이 올 수 있다. "3시간 전 상태로 돌려주세요"가 특정 테넌트의 데이터만 의미할 때, 전체 PITR이 아니라 테넌트 파티션만 복구하는 방법이 필요하다. 이때 논리 파티셔닝(테넌트 ID 기반 테이블 분리)이나 binlog 이벤트를 테넌트 기준으로 필터링하는 도구를 검토해보자.

---

## 인프라 — Aurora 클러스터 설계

결제 시스템의 인프라 구성을 한 줄씩 따져보자.

**Aurora 클러스터 선택**. 결제 서비스는 페일오버 RTO에 민감하다. 수십 초 장애도 결제 실패로 이어지지 않는가. Aurora의 15~30초 페일오버가 RDS의 60~120초보다 낫다는 사실, 이 도메인에서는 무겁다. 읽기 트래픽도 높으니 리플리카를 적극 활용할 수 있는 Aurora가 자연스러운 선택이다.

**읽기 리플리카 분산**. Writer는 주문 생성·결제 처리·포인트 차감 등 쓰기 중심으로, Reader는 판매자 정산 조회·사용자 주문 이력 조회로 분산한다.

```java
// Spring Boot에서 읽기/쓰기 DB 라우팅
@Configuration
public class DataSourceConfig {

    @Primary
    @Bean("writerDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.writer")
    public DataSource writerDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean("readerDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.reader")
    public DataSource readerDataSource() {
        return DataSourceBuilder.create().build();
    }
}

// 읽기 전용 트랜잭션은 리플리카로
@Service
public class SettlementQueryService {

    @Transactional(readOnly = true)  // readOnly=true → Reader 라우팅
    public List<SettlementDto> findBySellerAndDate(Long sellerId, LocalDate date) {
        // ...
    }
}
```

**파티셔닝 정책**. `payments` 테이블은 날짜 기반 RANGE 파티셔닝을 검토해볼 수 있다. 정산은 주로 최근 7~30일 데이터를 조회하므로 오래된 파티션을 아카이빙하거나 읽기 전용으로 전환하는 것이 가능하다.

```sql
-- payments 테이블 RANGE 파티셔닝 (연도 기반)
ALTER TABLE payments
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 오래된 파티션을 별도 테이블로 분리해 아카이빙
ALTER TABLE payments EXCHANGE PARTITION p2022
WITH TABLE payments_archive_2022;
```

**페일오버 RTO 측정**. Aurora의 페일오버를 실제로 테스트해보는 편이 낫다. AWS는 "장애 주입 테스트" 기능을 제공한다.

```bash
# AWS Fault Injection Simulator로 Aurora 페일오버 테스트
aws fis start-experiment \
  --experiment-template-id <template_id>

# 또는 Aurora 콘솔에서 "Failover" 버튼 클릭
# 페일오버 시작 시간 → 연결 재수립 시간 측정
```

실측한 RTO를 운영팀과 공유하고, SLA에 명시된 목표치와 비교해보자.

---

## 카카오 MRTE식 트래픽 미러링 — 변경 검증

인덱스를 추가하거나 쿼리를 수정하기 전에 실제 운영 트래픽으로 검증하고 싶다면 어떻게 할까?

카카오의 MRTE(MySQL Realtime Traffic Emulator)는 운영 트래픽을 새 환경에 미러링해 실제 동작을 미리 본다. MySQL 업그레이드나 대형 튜닝 전에 "미러 환경에서 운영 트래픽을 한 주 돌려보고 판단"하는 방식이다.

같은 원칙을 스테이징 환경에서 부분적으로 흉내 내볼 수 있다. 프록시 레이어(HAProxy, ProxySQL)에서 읽기 쿼리의 일부를 스테이징 DB로 복제해 실행 계획 차이를 비교한다.

결제 도메인처럼 데이터 정합성이 중요한 시스템에서는 쓰기 트래픽을 미러링하기 어렵지만, 읽기 쿼리 미러링만으로도 인덱스 변경의 효과를 사전 검증하는 데 충분하다.

---

## 마무리 — 도구함을 하나로 연결하는 감각

결제 시스템을 분해하면서 앞 챕터들의 도구들이 어떻게 연결되는지 봤다.

도메인 모델링(8장)이 스키마를 만들고, 인덱스 설계(4장)가 조회 성능을 결정한다. 동시성 처리는 낙관적 락과 named lock(10장)을 워크로드에 맞게 선택하는 문제다. 슬로우 쿼리가 뜨면 EXPLAIN ANALYZE(5장)로 분해하고 Invisible index(4장)로 안전하게 테스트한다.

정산 보고서는 윈도우 함수와 CTE(6장)로 SQL 안에서 처리하는 편이 애플리케이션 코드보다 깔끔하다. 백업 검증 실패 신호는 무시하지 않고, PITR 리허설(12장)로 대응 능력을 유지한다.

각 절의 "다른 도메인으로 옮긴다면" 단락에서 강조하고 싶었던 것은 이것이다. 결제가 아니더라도 같은 원칙이 적용된다. 도메인이 다르면 구체적인 구현은 달라지지만, 애그리거트 경계 → 스키마 → 인덱스 → 동시성 → 운영이라는 사고의 순서는 변하지 않는다.

다음 장에서는 메이저 업그레이드를 다룬다. MySQL 8.0에서 8.4로 넘어갈 때 무엇부터 점검해야 하는지, 다운그레이드 불가의 무게를 어떻게 준비하는지 함께 살펴보자.

---

## 참고 자료

- 우아한형제들 — MySQL을 이용한 분산락: https://techblog.woowahan.com/2631/
- 카카오 — MRTE (MySQL Realtime Traffic Emulator): https://tech.kakao.com/posts/311
- Baeldung — DDD aggregates and @DomainEvents: https://www.baeldung.com/spring-data-ddd
- 토스 SLASH 21 — MYSQL HA & DR Topology: https://toss.im/slash-21/sessions/2-3
- MySQL — Invisible Indexes: https://dev.mysql.com/doc/refman/8.0/en/invisible-indexes.html
- Vlad Mihalcea — Keyset Pagination with JPA and Hibernate: https://vladmihalcea.com/keyset-pagination-jpa-hibernate/


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


# 종장. 책을 덮으며

오래전 이야기다. 슬로우 쿼리 알람을 처음 받았을 때, 어디서부터 손대야 할지 몰라 DBA 동료 자리로 달려갔다. 그는 몇 줄의 EXPLAIN 출력을 보고 5분 안에 원인을 짚었다. "인덱스가 여기서 안 타요." 그때 그 사람이 보는 것을 나는 왜 못 보는지가 부러웠다. 기술의 차이라기보다 관점의 차이였다.

이 책은 그 관점을 배우는 책이었다.

---

## 13개 챕터의 의사결정 카드

책 전체를 한 장의 카드로 요약해보자.

| 챕터 | 핵심 질문 | 기억할 판단 기준 |
|------|-----------|-----------------|
| 1장 | 왜 지금 갈무리하는가 | 8.4 LTS의 default 변경이 우리 워크로드에 영향을 주는지 |
| 2장 | InnoDB 안에서는 무슨 일이 | 버퍼풀이 클수록 디스크 IO가 줄고, undo 로그가 늘수록 MVCC 비용이 오른다 |
| 3장 | 어떤 락이 어디에 걸리나 | RR은 next-key lock으로 phantom을 막고, RC는 gap lock이 없어 데드락이 줄지만 phantom은 허용한다 |
| 4장 | 어떤 인덱스를 어떤 순서로 | equality → range → sort, 고카디널리티 앞. 커버링 인덱스로 back-to-table 제거 |
| 5장 | EXPLAIN ANALYZE를 어디서 읽나 | 안쪽 노드부터. estimate와 actual 괴리가 크면 통계 갱신 |
| 6장 | SQL이 할 수 있는 것 | 윈도우 함수와 CTE로 집계를 SQL 안에서 처리하면 왕복이 줄고 가독성도 오른다 |
| 7장 | JSON을 어디까지 쓸 수 있나 | functional index 또는 generated column으로 JSON path도 인덱싱 가능 |
| 8장 | 스키마와 도메인의 거리 | PK 전략, soft delete, FK 범위는 도메인 요구와 MySQL 제약 사이의 절충이다 |
| 9장 | JPA가 보여주는 것과 실제 SQL | N+1은 fetch graph로, 깊은 페이지는 keyset으로, 배치는 JdbcTemplate batchUpdate로 |
| 10장 | JPA 한계 너머 | 배치 INSERT 3종 세트, 청크 분할 UPDATE, named lock 커넥션 풀 분리 |
| 11장 | RDS vs Aurora 분기점 | 읽기 확장·페일오버 RTO·IO 집약도·락-인 여부, 네 가지 기준으로 판단 |
| 12장 | 운영의 신호를 어떻게 듣나 | 버퍼풀 히트율, Threads_running, 락 대기, 복제 lag. 백업은 복구 테스트가 진짜 백업 |
| 13장 | 모든 도구를 어떻게 연결하나 | 도메인 → 스키마 → 인덱스 → 동시성 → 운영의 순서는 도메인이 달라도 변하지 않는다 |
| 14장 | 메이저 업그레이드를 넘는 법 | pt-upgrade → 인증 플러그인 → default 변경 → Blue/Green → escape hatch |

---

## 다음 주 월요일, 세 가지 실험

책을 읽는 것과 적용하는 것 사이에는 언제나 거리가 있다. 그 거리를 줄이는 가장 빠른 방법은 지금 당장 작은 것을 하나 해보는 것이다.

다음 주 월요일, 세 가지 중 하나를 해보자. 세 가지 다 할 필요는 없다. 하나만 해도 충분하다.

**실험 1: 슬로우 쿼리 로그를 켜고 pt-query-digest를 돌려보자.**

운영 서비스에 슬로우 쿼리 로그가 켜져 있지 않다면 지금 켜보자. `long_query_time = 1`로 설정하고 하루 쌓인 로그를 `pt-query-digest`로 분석해보자. 가장 실행 시간 합계가 높은 쿼리 하나를 `EXPLAIN ANALYZE`로 분해해보자. 예상과 다른 실행 계획을 발견하면 그것이 시작이다.

**실험 2: 배치 INSERT 성능을 측정해보자.**

애플리케이션에서 `saveAll()`을 쓰는 코드가 있다면, 세 가지 설정(`jdbc.batch_size`, `order_inserts`, `rewriteBatchedStatements=true`)이 모두 켜져 있는지 확인하자. ID 전략이 IDENTITY라면 그것도 확인하자. 설정 전후의 실행 시간을 비교해보자. 차이가 없다면 왜 없는지 확인하는 것도 좋은 공부다.

**실험 3: PITR 리허설을 한 번 해보자.**

스테이징 환경에서 백업 스냅샷으로부터 복구하는 것을 한 번 실제로 해보자. RDS/Aurora라면 AWS 콘솔에서 "restore to point in time"을 클릭해보자. 복구에 얼마나 걸리는지 시간을 재보자. 그것이 우리 서비스의 실제 RTO다.

---

## 감사의 말과 참고 문헌 안내

이 책은 많은 엔지니어들의 공개된 경험 위에 서 있다.

우아한형제들이 named lock 분산락과 배치 INSERT 개선 경험을 기술블로그에 공유하지 않았다면 10장이 지금처럼 생생하지 않았을 것이다. 토스 SLASH 21에서 DR 토폴로지를 설명해준 발표자, LINE Engineering에서 performance_schema의 실제 영향을 측정한 엔지니어들에게 감사한다. 카카오 테크 블로그의 InnoDB 내부 시리즈도 큰 도움이 됐다.

이 책에서 자주 인용한 Vlad Mihalcea의 "High-Performance Java Persistence"는 JPA를 진지하게 다루는 모든 개발자에게 권하는 책이다.

더 깊은 곳을 향해 가고 싶다면 다음 참고 문헌들이 기다리고 있다.

**도서**
- Schwartz, B. 외 (2012) *High Performance MySQL, 3rd Edition*, O'Reilly
- Aubin, J., Bell, C. (2021) *High Performance MySQL, 4th Edition*, O'Reilly
- 백은빈·이성욱 (2021) *Real MySQL 8.0* 1·2권, 위키북스

**학술 논문 — 트랜잭션 고급 독자에게**
- Cahill, M. (2009) "Serializable Isolation for Snapshot Databases" — MySQL의 RR이 진정한 직렬성이 아닌 이유, Snapshot Isolation의 수학적 기반
- Neumann, T. 외 (2015) "Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems" (SIGMOD) — MVCC 구현의 현대적 접근
- Jepsen 분석 (MySQL 8.0.34) — https://jepsen.io/analyses/mysql-8.0.34

---

## 마지막으로

책을 덮고 나면 잊어버릴 것들이 있다. 괜찮다. 기억나지 않을 때 다시 꺼내 보면 된다. 하지만 한 가지만 마음에 남겨두자.

**데이터베이스는 말이 없다.** 우리가 먼저 물어봐야 대답한다. 슬로우 쿼리 로그를 켜고, EXPLAIN ANALYZE를 돌리고, 복제 lag을 확인하고, 분기마다 PITR을 리허설하는 것 — 이것이 DB에게 먼저 말을 거는 방법이다.

DBA가 되지 않아도 된다. DBA처럼 생각하는 스프링 개발자이면 충분하다. 그 생각의 출발점은 "왜 그럴까?"라는 질문 하나다.

부디 다음 주 월요일의 실험이 이 책의 진짜 마지막 챕터가 되길 바란다.

---

## 참고 자료

- Cahill, M. (2009) *Serializable Isolation for Snapshot Databases*: https://ses.library.usyd.edu.au/bitstream/handle/2123/5353/michael-cahill-2009-thesis.pdf
- Jepsen — MySQL 8.0.34 분석: https://jepsen.io/analyses/mysql-8.0.34
- 백은빈·이성욱 (2021) *Real MySQL 8.0*: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=278488709
- Vlad Mihalcea — High-Performance Java Persistence: https://vladmihalcea.com/books/high-performance-java-persistence/


---

## 판권

**DBA처럼 생각하는 스프링 개발자 — MySQL 8.x를 다루는 13가지 관점**

- 저자: Toby-AI
- 초판: 2026년 5월 18일
- 판본: v1.0.0
- 라이선스: CC BY-NC-SA 4.0 — 저작자 표시·비상업적 이용·동일조건 변경허락
- 더 보기: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko
- 식별자: book:advanced-mysql:v1.0.0

이 책은 Toby-AI 하네스 v1.2.0으로 저술되었다. 하네스 출처: https://github.com/tobyilee/book-writer

본 책의 콘텐츠는 위 라이선스에 따라 자유롭게 공유·인용·번역할 수 있으며, 상업적 이용과 변경 시 동일 라이선스 적용이 요구된다.
