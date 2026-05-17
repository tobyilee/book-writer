# 8장. 같은 row를 둘이 동시에 본다 — 락과 isolation의 실전

한 시나리오를 그려보자. 쇼핑몰의 상품 가격 수정 기능이다. 관리자 A가 화면을 연다. 상품의 현재 가격은 10,000원이다. A는 10,500원으로 올릴 작정으로 잠시 생각에 빠진다. 그 사이 관리자 B가 같은 상품을 연다. 화면에는 똑같이 10,000원이 떠 있다. B는 9,000원으로 내릴 생각이다. B가 먼저 저장 버튼을 누른다. DB의 price는 9,000원이 된다. 잠시 후 A가 저장을 누른다. price는 10,500원이 된다.

자, 무엇이 잘못됐는가. 코드도 정상이다. 트랜잭션도 잘 시작되고 잘 끝난다. UPDATE 문도 한 줄씩 멀쩡하게 나간다. 그런데 B의 결정은 흔적 없이 사라졌다. 마치 B가 가격을 내린 적이 없었던 것처럼. 이걸 우리는 lost update라고 부른다. 더 무서운 건, 이 시나리오를 만들기 위해 우리가 "잠시 생각에 빠진다"고 했다는 점이다. 0.5초만 생각해도, 두 트랜잭션이 그 짧은 사이에 겹치는 일이 일어난다. 사용자가 화면을 보고 결정하는 모든 자리, 즉 다중 HTTP 요청을 사이에 둔 모든 워크플로가 이 위험을 안고 있다.

여기까지 읽고 "그건 isolation level을 올리면 되지 않나"라고 생각했다면, 한 번 더 생각해보자. PostgreSQL이 디폴트로 쓰는 Read Committed에서는 위 시나리오를 막지 못한다. MySQL InnoDB의 디폴트인 Repeatable Read를 쓰면 막힐 수도 있는데, 이번엔 다른 문제가 따라온다. 우리가 본 적도 없는 row까지 락에 걸려서, 정작 동시성을 늘리려고 들어간 곳에 데드락이 핀다. 그렇다면 정답은 어디에 있을까. 이 장은 그 답을 찾아 나가는 길이다.

## 동시성 anomaly라는 지도

isolation level을 이야기하려면 먼저 "막아야 할 것"의 이름을 알아야 한다. ANSI SQL 표준과 그 이후 등장한 MVCC 구현이 정리해 둔 동시성 anomaly는 다섯 가지다. 한 번에 다 외우기는 부담스러우니, 우리 도메인에서 어떤 모습으로 나타나는지를 함께 짚어가보자.

**Dirty read.** 트랜잭션 B가 트랜잭션 A의 *아직 커밋되지 않은* 변경을 읽어가는 현상이다. A가 가격을 9,000원으로 잠깐 바꿔두고 나중에 롤백할 작정인데, B가 그 짧은 사이에 9,000원으로 읽어가서 영수증을 출력해 버린다면 끔찍한 일이다. 다행히 우리가 일상에서 쓰는 거의 모든 DB의 거의 모든 isolation level이 이걸 막아준다. Oracle은 아예 Read Uncommitted라는 레벨 자체가 없다. PostgreSQL과 SQL Server의 Read Uncommitted도 사실상 Read Committed처럼 동작한다. 그러니 Dirty read는 일반적으로 걱정거리가 아니다.

**Non-repeatable read.** 같은 트랜잭션 안에서 같은 row를 두 번 읽었는데, 두 결과가 다른 경우다. 한 번 읽고 어떤 검증을 한 다음 다시 읽으니 값이 바뀌어 있다면? 검증의 의미가 사라진다. Read Committed에서는 발생한다. Repeatable Read 이상이면 막힌다.

**Phantom read.** 같은 조건의 쿼리를 두 번 던졌는데, 두 번째에서 row가 새로 나타나거나 사라진 경우다. "WHERE region = 'KR'"로 두 번 SELECT했더니 처음엔 100건, 두 번째엔 101건이라면, 그 사이에 누군가 INSERT한 것이다. Repeatable Read에서도 DB에 따라 발생할 수 있다. MVCC 기반 Snapshot Isolation에서는 막힌다.

**Lost update.** 우리가 도입부에서 본 그 시나리오다. A와 B가 같은 값을 읽고, 각자 계산한 뒤, 각자 UPDATE한다. 한쪽의 변경이 사라진다. Read Committed에서는 *언제든* 발생한다. MySQL InnoDB의 Repeatable Read는 막아주기도 한다(뒤에서 설명한다). Snapshot Isolation 이상이면 막힌다.

**Read/Write skew.** 두 트랜잭션이 같은 데이터를 읽고, 각자 *다른* row를 UPDATE하지만, 그 두 row 사이에 무결성 제약이 있는 경우다. 의사 둘이 동시에 "내가 빠져도 다른 한 명이 당직이지" 하고 둘 다 빠지는 고전적인 예가 이것이다. Snapshot Isolation에서도 발생한다. PostgreSQL의 Serializable Snapshot Isolation(SSI)이라야 막힌다.

이 다섯 가지를 한 표에 모아보자. Vlad Mihalcea가 자기 블로그 시리즈에 정리해 둔 매트릭스인데, 책상 가까운 데 붙여 두면 좋다.

| Anomaly | Read Committed | Repeatable Read | Snapshot Isolation | Serializable |
|---------|----------------|-----------------|--------------------|--------------|
| Dirty read | 방지 | 방지 | 방지 | 방지 |
| Non-repeatable read | **발생** | 방지 | 방지 | 방지 |
| Phantom read | 발생 | DB별 다름 | 방지 (MVCC) | 방지 |
| Lost update | **발생** | 방지 (InnoDB) | 방지 | 방지 |
| Read/Write skew | 발생 | 발생 | 발생 | 방지 (PG SSI) |

이 표에서 굵게 표시한 두 칸을 보자. Read Committed에서는 Non-repeatable read와 Lost update가 그냥 발생한다. 그런데 PostgreSQL·Oracle·SQL Server의 디폴트가 Read Committed다. 즉 *우리가 의식적으로 무언가 하지 않으면, 우리 시스템은 lost update가 일어나는 상태로 운영되고 있다.* 이 사실 하나만 머릿속에 박아두자.

반대편에 MySQL InnoDB가 있다. 디폴트가 Repeatable Read다. 그래서 lost update가 *기본적으로는* 막힌다. 다행이라고 안심하기엔 이르다. InnoDB가 그걸 막는 메커니즘 자체가 새로운 문제를 만든다. 그 이야기는 뒤에서 따로 한 절을 떼어 다룬다.

여기서 한 번 멈추고 자기 시스템을 돌아보자. 우리 DB는 무엇인가. 그 DB의 디폴트 isolation은 무엇인가. 우리 핵심 트랜잭션은 그 isolation 아래서 lost update를 견딜 수 있는가. 견딜 수 없다면 무엇을 해 두었는가. 답이 즉시 나오지 않는다면, 솔직히 말해서 그 시스템은 운에 기대고 있는 것이다.

## MVCC, 그리고 PostgreSQL의 Repeatable Read라는 묘한 이름

지도를 들고 다음 자리로 가보자. MVCC다. 풀어쓰면 Multi-Version Concurrency Control. 직역하면 다중 버전 동시성 제어인데, 직역만 봐서는 무엇을 푸는 도구인지 잘 안 와 닿는다. 한 줄로 정리하면 이렇다. *read가 write를 막지 않고, write도 read를 막지 않는다.* 그 비결이 "row의 여러 버전을 동시에 들고 있는 것"이다.

조금 더 풀어보자. 옛날식 lock 기반 isolation에서는 어떤 row를 읽는 동안 그 row에 쓰기 락이 걸린 게 있으면 기다려야 한다. 반대로 쓰는 중이라면 읽으려는 쪽이 기다린다. 동시성이 늘면 락 대기가 폭증한다. MVCC는 그 발상을 뒤집는다. UPDATE이 일어나면 새 버전을 만들 뿐 기존 버전을 지우지 않는다. 트랜잭션마다 자기 시작 시점의 "스냅샷"을 들고, 그 시점에 유효했던 버전들만 본다. 그래서 한쪽의 UPDATE이 다른 쪽의 SELECT을 막지 않는다. 두 트랜잭션이 같은 row의 *다른 버전*을 보는 것이기 때문이다.

이 메커니즘으로 자연스럽게 Snapshot Isolation이 만들어진다. 트랜잭션이 시작될 때 찍힌 스냅샷 안에서만 사물을 보니, 그 안에서 같은 row를 두 번 읽으면 당연히 같은 값이 나온다. Non-repeatable read도, Phantom read도 같은 이유로 막힌다. 학술 쪽에서는 HyPer 그룹의 *"Fast Serializable Multi-Version Concurrency Control"* 같은 논문이 MVCC를 거의 영(零) 비용에 가깝게 구현하는 흐름을 정리해 두었다. PostgreSQL·Oracle·SQL Server의 snapshot isolation이 그 이론적 baseline 위에 서 있다.

자, 여기서 이름의 함정 하나를 짚어두자. PostgreSQL에서 `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ`를 하면 무엇이 켜질까. 이름만 보면 "ANSI 표준의 Repeatable Read"가 켜질 것 같다. 실제로는 Snapshot Isolation이 켜진다. ANSI 표준에 정의된 Repeatable Read는 락 기반의 정의인데, PostgreSQL은 MVCC로 동작하니 그 정의로 자기 동작을 묘사할 수가 없다. 그래서 *이름은 Repeatable Read인데 실체는 Snapshot Isolation*인 묘한 상황이 굳어졌다. 이 사실을 모르면 표를 잘못 읽는다. PostgreSQL의 RR에서는 Phantom도, Lost update도 막힌다. ANSI 정의대로라면 막히지 않아야 하는데 막힌다. 이름 대신 실체로 기억해두자.

이걸 알고 나면 한 가지가 자연스럽게 떠오른다. *Hibernate의 PersistenceContext도 비슷한 일을 하고 있지 않나?* 그렇다. 같은 트랜잭션 안에서 같은 PK로 두 번 조회하면, 두 번째는 DB로 나가지 않고 1차 캐시에서 같은 인스턴스를 돌려준다. 즉 application 레벨에서 같은 트랜잭션의 같은 row는 한 번만 본다. 이걸 *application-level repeatable read*라고 부른다. DB가 MVCC로 보장하는 것 위에, Hibernate가 한 번 더 일관성을 두르는 셈이다. 7장에서 1차 캐시를 "캐시"보다 *consistency boundary*로 봐야 한다고 한 게 이 자리와 만난다.

여기서 묘한 안도감을 느낄 수 있다. "그러면 PersistenceContext 안에서는 안전한 거네?" 한쪽 면만 보면 그렇다. 하지만 안도감은 짧다. PersistenceContext는 트랜잭션의 끝과 함께 비워진다. *다음 HTTP 요청*은 새 트랜잭션이고, 새 PersistenceContext다. 사용자가 화면을 0.5초 보는 동안 같은 row를 두 번 보고 두 번 결정하는 그 흐름은 PersistenceContext가 막아주지 않는다. 그게 도입부의 lost update 시나리오다. 그래서 다음 절로 넘어가야 한다.

## `@Version`이 답이 되는 자리

도입부의 시나리오를 다시 그려보자. A와 B가 같은 상품의 가격을 동시에 수정한다. 두 사람의 트랜잭션은 *완전히 분리되어 있다*. 사용자가 화면을 보는 동안에는 트랜잭션이 열려 있지도 않다. 그러니 DB의 isolation level이 무엇이든, MVCC가 어떻게 작동하든, 두 트랜잭션이 같은 row를 읽고 각자 UPDATE하는 흐름 자체는 막아주지 않는다. 한쪽이 보낸 UPDATE이 다른 쪽이 보낸 UPDATE 위에 그대로 덮어쓴다.

그러면 어떻게 해야 할까. 답은 의외로 단순하다. UPDATE 절에 *내가 본 그 버전*을 조건으로 넣는 것이다. "내가 본 row가 아직 그 모습 그대로일 때만 덮어써라"라고 말해주면 된다. JPA가 그걸 자동으로 해주는 장치가 `@Version`이다.

```java
@Entity
public class Product {
    @Id @GeneratedValue
    private Long id;

    @Version
    private Long version;

    private BigDecimal price;
}
```

`version`이라는 컬럼을 하나 두고 `@Version` 어노테이션을 붙이면, Hibernate는 그 엔티티의 UPDATE 문에 자동으로 다음 두 가지를 한다. 첫째, WHERE 절에 `version=?`을 추가한다. 둘째, SET 절에 `version=version+1`을 추가한다. 그러니 SQL이 이렇게 나간다.

```sql
UPDATE product
SET    price = ?, version = ?
WHERE  id = ? AND version = ?
```

WHERE 절의 두 번째 조건이 핵심이다. "내가 읽었을 때 version이 5였으니까, 지금도 5라면 덮어써도 된다"는 뜻이다. 만약 그 사이에 다른 트랜잭션이 같은 row를 먼저 UPDATE했다면 version은 이미 6이 됐을 것이고, 내 UPDATE의 WHERE 조건은 매치되는 row를 찾지 못해 0건 갱신으로 끝난다. JDBC가 `updateCount = 0`을 돌려주면 Hibernate는 그걸 *경합으로* 해석하고 `OptimisticLockException`(예전 이름으로는 `StaleObjectStateException`)을 던진다.

이 메커니즘의 아름다움은 무엇일까. *락이 없다는 점*이다. 어떤 trazaktion도 다른 트랜잭션을 기다리게 만들지 않는다. 그저 자기 차례에 UPDATE을 보내고, 실패하면 알아채고, 어떻게 할지 *애플리케이션 코드가* 결정한다. 동시성을 늘려도 락 경합이 폭증하지 않는다. 그래서 이 방식을 *낙관락(optimistic locking)*이라고 부른다. "충돌이 자주 안 일어날 거라고 낙관하고, 일어났을 때만 대응한다"는 뜻이다.

Vlad의 권고는 한 줄이다. *"낙관락이 디폴트, 비관락은 정당화가 필요한 선택."* 이걸 받아들이고 나면 실무가 한결 단순해진다.

### 다중 HTTP 요청에 걸친 동시성은 사실상 낙관락만이 답

여기서 한 가지 사실을 강조해두자. 사용자가 화면을 보는 동안에는 DB 트랜잭션을 열어둘 수 없다. 만약 그렇게 한다면 어떻게 될까. 사용자가 점심 먹으러 가는 사이 DB 커넥션 하나가 점유된 채로 30분, 1시간이 흐른다. 화면을 천 명이 보면 천 개의 커넥션이 그대로 잠긴다. 끔찍한 일이다. 그래서 표현 계층의 단위는 *하나의 HTTP 요청 = 하나의 짧은 트랜잭션*이다. 그 사이에 락을 들고 있을 수 없다.

비관락은 그래서 다중 HTTP 요청을 사이에 둔 동시성 제어에는 *원리적으로* 답이 될 수 없다. 락을 다음 요청까지 끌고 갈 수 없기 때문이다. 그렇다고 동시성을 포기할 수도 없다. 그래서 남는 답이 낙관락이다. `@Version`은 락을 안 잡고도 "내가 본 시점의 상태"라는 정보를 row에 새겨둔다. 그 정보는 다음 요청까지, 며칠 뒤까지도 유효하다. 여러 HTTP 요청에 걸친 동시성 제어가 가능한 거의 유일한 방법이다.

이 한 줄을 잊지 말자. *비관락은 한 트랜잭션 안에서만 의미가 있다. 화면을 사이에 둔 흐름은 낙관락만이 답이다.*

### `OptimisticLockException`을 만났을 때 무엇을 할까

낙관락의 아름다움 뒤에는 반드시 따라오는 부담이 있다. *예외가 났을 때 어떻게 할 것인가.* `OptimisticLockException`이 던져졌다는 건, 우리 시스템이 사용자에게 "당신이 보고 계신 화면은 이미 낡았습니다"라고 말해야 하는 순간이다. 이걸 무성의하게 처리하면 사용자 경험이 무너진다.

세 가지 선택지가 있다.

**첫째, 재시도(retry).** 똑같은 작업을 다시 보내본다. 단, 무한 재시도는 금물이다. 충돌이 격렬한 자리에서는 retry storm을 만든다. Spring `@Retryable`이나 Resilience4j의 `@Retry`로 횟수와 백오프를 명시하자. 보통 3회 정도가 무난하다. 그리고 *재시도가 자연스러운 작업에만* 적용한다. 사용자가 결정한 가격을 다시 적용하는 건 자연스럽지만, 사용자가 "보낸 메시지"를 자동 재시도하는 건 위험할 수 있다.

**둘째, 사용자에게 알리고 다시 받기.** "방금 다른 분이 먼저 수정하셨습니다. 화면을 새로 받아 확인해주세요." 이게 가장 정직한 대응이다. 가격 수정처럼 *사람의 판단*이 끼는 자리는 거의 이쪽이 옳다.

**셋째, 자동 merge.** 두 변경이 서로 다른 필드라면 application 레벨에서 합칠 수도 있다. A는 가격을 바꾸고 B는 설명을 바꿨다면 둘 다 살리는 식이다. 다만 이건 복잡도가 빠르게 올라간다. 위키처럼 *공동 편집이 본질인 도메인*에서만 정당화된다.

대부분의 일반 비즈니스 도메인에서는 첫째와 둘째 사이를 오간다. 셋째는 신중하게 가자.

여기서 한 번 점검해보자. 우리 코드에서 동시 수정이 가능한 엔티티에 `@Version`이 붙어 있는가. 사용자가 화면을 보고 결정하는 자리, 즉 *"읽기 → 사람 결정 → 쓰기"* 흐름이 있는 모든 엔티티가 후보다. 한 번 훑어보면 빠진 자리가 생각보다 많다. 잊지 말자, Read Committed의 디폴트 환경에서는 `@Version`이 *유일한* 안전망이라는 사실을.

### `FORCE_INCREMENT`: 자식의 변경을 부모로 전파한다

`@Version`을 도입하다 보면 한 가지 미묘한 자리에 부딪힌다. *연관 엔티티의 변경을 부모 엔티티에 어떻게 알릴까?* 예를 들어 `Post`가 있고 그 자식 `PostComment`가 있다고 해보자. 댓글이 새로 달리는 일은 `Post`의 row를 직접 건드리지 않는다. `PostComment` 테이블에 INSERT 한 줄이 나갈 뿐이다. 그런데 도메인적으로는 "이 Post의 상태가 바뀌었다"고 보고 싶다면 어떻게 해야 할까.

이 자리에 두 가지 락 모드가 마련되어 있다.

```java
Post post = em.find(Post.class, postId, LockModeType.OPTIMISTIC_FORCE_INCREMENT);
PostComment c = new PostComment("새 댓글");
post.addComment(c);
```

`OPTIMISTIC_FORCE_INCREMENT`는 *현재 트랜잭션 끝에서* `Post`의 version을 강제로 증가시킨다. UPDATE 한 방으로 version 체크와 증가가 묶여 나가고, 만약 그 사이 다른 트랜잭션이 같은 `Post`를 건드렸다면 트랜잭션 끝에서 `OptimisticLockException`이 난다. 부모 row에 다른 변경이 동시에 일어났는지를 자식 변경이 들어가는 자리에서 감지할 수 있다.

`PESSIMISTIC_FORCE_INCREMENT`는 한 발 더 나간다. *즉시* `SELECT ... FOR UPDATE` 비슷한 락과 함께 version을 증가시키고, 그 결과를 현재 트랜잭션 안에서 곧바로 알 수 있다. 충돌이 잦거나, 자식 변경의 비용이 큰 경우(예: 외부 결제 호출이 끼어 있어서 *나중에 롤백*하는 게 비싼 경우)에 쓴다.

두 모드의 차이는 한 줄로 기억해두자. *옵티미스틱은 트랜잭션 끝까지 미루고, 페시미스틱은 지금 당장 결정한다.* 어느 쪽이든 자식 변경의 일관성을 부모 버전으로 끌어올리는 장치다.

### Hibernate Envers를 곁들인 메모

`@Version` 자체는 변경 *이력*을 남기지 않는다. 누가 언제 무엇을 바꿨는지 추적이 필요하면 Hibernate Envers 같은 별도 도구가 자리를 차지한다. 둘은 충돌하지 않는다. 오히려 함께 두면 *"이 변경이 누구의 손에 의해, 어떤 버전에서 시작됐는지"*까지 깔끔하게 추적된다. 단, Envers는 이 장의 주제는 아니므로 이름만 적어두자.

## 비관락이 정당화되는 자리

낙관락이 디폴트라는 합의에 도달했으니, 그렇다면 비관락은 언제 정당화될까. 무조건 낙관락만 쓰면 되지, 왜 비관락이라는 도구가 있을까. 한 번 들여다보자.

비관락이 사용할 수 있는 곳은 *하나의 트랜잭션 안*이다. 그 안에서 어떤 row를 *읽는 순간* 다른 트랜잭션이 그 row를 못 건드리게 하고 싶을 때 쓴다. JPA에서는 `LockModeType.PESSIMISTIC_READ`와 `PESSIMISTIC_WRITE`가 있다. 내려가서 보면 각각 `SELECT ... FOR SHARE`와 `SELECT ... FOR UPDATE`다.

```java
Account account = em.find(
    Account.class,
    accountId,
    LockModeType.PESSIMISTIC_WRITE
);
account.withdraw(amount);
```

이 코드를 만나면 DB가 해당 row에 락을 걸고, 락이 풀릴 때까지 다른 트랜잭션의 동일 row UPDATE을 막는다. 트랜잭션이 커밋되거나 롤백될 때까지 그 락은 유지된다.

언제 이 도구가 *정당화*될까. 세 가지 자리를 떠올리자.

**충돌 빈도가 매우 높아 retry가 의미를 잃는 자리.** 낙관락은 충돌이 드물 거라는 가정 위에 서 있다. 그런데 어떤 자리에서는 동시 접근이 *극도로* 잦아서 retry를 깔아두면 100번 중 30번이 재시도가 된다. 그러면 retry storm이 발생하고, 오히려 비관락이 차분히 줄을 세우는 게 시스템 전체에 부담이 적다. 대표적인 예가 *재고 차감*이다. 한정 수량 이벤트 상품을 1초에 천 명이 누른다면, 낙관락의 retry는 시스템을 마비시킨다. 비관락이 줄을 세우고, 줄이 너무 길면 빨리 손절시키는 편이 낫다.

**원자성이 중요한 결제 처리.** 결제 트랜잭션에서 잔액을 읽고, 검증하고, 차감하는 짧은 critical section을 생각해보자. 이 흐름 안에서는 잔액 row가 절대 다른 트랜잭션의 손에 닿으면 안 된다. 낙관락으로도 막을 수 있지만, 코드 흐름이 복잡해진다. 비관락으로 잠가두면 *코드가 짧고 단순해진다*. 단, 그 critical section이 짧다는 전제가 있어야 한다. 외부 결제 PG 호출이 끼면 비관락은 위험해진다. 외부 호출이 1초 걸리는 동안 그 row가 잠긴다는 뜻이니까. 그래서 *외부 호출 직전에 락을 풀고, 응답을 받은 뒤 다시 잡는다*는 패턴을 쓰기도 한다.

**비가역적인 외부 작업의 보호.** 한 번 보낸 이메일을 되돌릴 수 없듯, 어떤 작업은 *해버린 다음 롤백이 안 된다*. 그런 작업을 트랜잭션 안에서 보호할 때 비관락이 자연스럽다. "내가 이 작업을 진행하는 동안에는 다른 누구도 같은 row를 건드릴 수 없다"를 보장해야 한다.

이 세 자리가 비관락의 정당한 영역이다. 이 외에는 *기본적으로* 낙관락으로 시작하자. Vlad의 한 줄이 여기서도 들어맞는다. *"낙관락이 디폴트, 비관락은 정당화가 필요한 선택."*

### `SKIP LOCKED`로 만드는 가벼운 job queue

비관락의 응용 중 하나를 짚고 가자. PostgreSQL이 8.4부터 가진 `SELECT ... FOR UPDATE SKIP LOCKED`다. MySQL도 8.0부터 지원한다. 이름 그대로 *이미 락이 걸린 row는 건너뛰고* 그렇지 않은 row만 가져오는 옵션이다. 이걸로 무엇을 만들 수 있을까. 그렇다, *RDB만으로 job queue를 만들 수 있다.*

```sql
SELECT *
FROM   job
WHERE  status = 'PENDING'
ORDER  BY created_at
LIMIT  10
FOR UPDATE SKIP LOCKED;
```

이 SQL을 worker 여러 개가 동시에 던지면 어떻게 될까. 워커 A가 처음 10건을 잡고, 그 사이에 던진 워커 B는 *그 10건을 건너뛰고* 다음 10건을 잡는다. 같은 job을 둘이 처리할 위험이 없다. 그리고 워커가 죽으면 트랜잭션이 롤백되고 락이 풀려, 자연스럽게 다른 워커가 그 job을 다시 잡는다. Kafka·RabbitMQ까지 안 가도 어지간한 규모의 비동기 작업은 이걸로 해결된다.

JPA에서 이걸 어떻게 쓸까. Spring Data JPA의 `@Lock` + 쿼리 힌트로 표현할 수 있다.

```java
public interface JobRepository extends JpaRepository<Job, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints({
        @QueryHint(name = "jakarta.persistence.lock.timeout",
                   value = "-2") // SKIP LOCKED
    })
    @Query("select j from Job j where j.status = 'PENDING' order by j.createdAt")
    List<Job> claimPending(Pageable pageable);
}
```

힌트 값 `-2`가 `SKIP LOCKED`에 매핑된다. Hibernate 6의 표준화된 값이다. (예전 버전이거나 환경이 묘하면 `org.hibernate.timeout` 힌트를 써야 할 수도 있다. 자기 환경에서 한 번 SQL이 어떻게 찍히는지 확인해두자.) `0`은 `NOWAIT`이다. 기다리지 않고 즉시 실패하라는 뜻이다. 이 두 값을 의식적으로 구분해두자. 비관락을 쓰면서 락 대기를 그냥 두는 건 무책임에 가깝다.

`SKIP LOCKED`는 비관락의 단점을 절묘하게 회피한다. 락이 걸려 있어도 *대기하지 않으니* 응답이 빠르고, *건너뛰니* 데드락 위험이 줄어든다. 가벼운 워크플로의 동시 처리에 잘 어울린다. 한 번쯤 우리 시스템의 비동기 자리에 도입을 검토해볼 만하다.

## MySQL InnoDB의 gap lock — 안전망인가 함정인가

이제 가장 까다로운 자리로 가보자. MySQL InnoDB의 Repeatable Read와 gap lock 이야기다. 이 자리는 한국 개발자들이 가장 자주 발을 헛디디는 곳이기도 하다. 자기 시스템이 MySQL이라면 특히 천천히 읽어주기를 권한다.

먼저 디폴트의 차이부터 다시 짚어두자.

| DB | 디폴트 isolation |
|----|-----------------|
| PostgreSQL | Read Committed |
| Oracle | Read Committed |
| SQL Server | Read Committed |
| **MySQL InnoDB** | **Repeatable Read** |

MySQL만 다르다. 이게 무슨 뜻인지 곰곰이 생각해보자. PostgreSQL과 Oracle을 쓰던 사람이 MySQL로 옮기면, 같은 SQL이 *완전히 다른 격리 수준*에서 실행된다. 그 반대도 마찬가지다. 이 차이를 모르고 SQL을 옮기다 보면 한쪽에서는 잘 돌던 코드가 다른 쪽에서 데드락이 나거나, 한쪽에서는 lost update가 나던 코드가 다른 쪽에서는 잘 막힌다. 묘하다.

### Next-key lock의 정체

MySQL InnoDB의 RR이 Phantom read를 어떻게 막을까. 답은 *gap lock*이다. row 락만으로는 부족하다. 새 row가 INSERT 되어 들어오는 걸 막아야 Phantom이 사라지기 때문이다. 그래서 InnoDB는 *이미 존재하는 row 사이의 빈 공간*에도 락을 건다. 이걸 gap lock이라 부른다. 그리고 row 락과 gap lock을 합친 것을 next-key lock이라 부른다.

예를 들어 인덱스에 5, 10, 15, 20이라는 키가 있는 테이블을 생각해보자. `SELECT ... WHERE id > 10 AND id <= 20 FOR UPDATE`를 던지면 어떤 락이 걸릴까. 직관적으로는 15와 20 두 row에만 걸릴 것 같다. 실제로는 다르다. (10, 15], (15, 20] 구간 전체가 잠긴다. 즉 11, 12, 13, 14, 16, 17 같은 *존재하지 않는 키*에 누군가 INSERT하는 것도 막힌다. Phantom read를 막기 위함이다.

이게 왜 위험할까. 우리가 "이 두 row만 잠가놓겠다"고 생각한 SQL이 *훨씬 넓은 범위*를 잠가놓기 때문이다. 다른 트랜잭션이 12나 17 같은 키로 INSERT을 시도하면 우리 락이 풀릴 때까지 기다린다. 동시성 처리량이 갑자기 떨어진다.

### `@Lock` + `LIMIT` 조합의 함정

한국 커뮤니티에서 보는 사고 패턴 하나를 옮겨두자. job queue를 JPA로 만들려고 다음과 비슷한 코드를 짠 적이 있다.

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("select j from Job j where j.status = 'PENDING' order by j.id")
List<Job> claimNext(Pageable pageable);
```

`Pageable.ofSize(10)`을 넘기면 SQL에 `LIMIT 10`이 붙는다. 의도는 "PENDING인 job 중 가장 오래된 10개를 잡고 처리한다"였다. PostgreSQL에서는 잘 돌았다. MySQL에서 운영에 올리니 어느 새벽부터 데드락 알림이 쌓이기 시작했다.

무슨 일이 벌어졌을까. MySQL InnoDB의 RR에서 `SELECT ... LIMIT 10 FOR UPDATE`는 *10개 row만 잠그지 않는다*. 옵티마이저가 인덱스를 스캔하면서 만난 모든 row에 대해 락을 잡아둔다. 그리고 그 row들 사이의 gap에도 락을 건다. 워커가 여러 개 동시에 이 SQL을 던지면, 각 워커가 *서로 다른 LIMIT 10*을 받지만 그 과정에서 *겹치는 gap*에 동시 접근한다. 데드락이 안 날 수가 없는 구조였다.

이 경험이 우리에게 가르쳐주는 게 무엇일까. 첫째, *MySQL의 비관락은 PostgreSQL의 비관락과 다르게 동작한다*. 둘째, `LIMIT`과 `FOR UPDATE`의 조합은 직관과 어긋난다. 셋째, 모르고 쓰는 isolation은 모르고 들고 있는 칼이다.

### 트레이드오프: READ COMMITTED로 내려보기

해법은 두 갈래가 있다.

**갈래 ①: isolation을 Read Committed로 내린다.** MySQL InnoDB도 Read Committed로 동작할 수 있다. `SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED` 또는 application 레벨에서 트랜잭션을 시작할 때 명시한다. RC에서는 gap lock이 *거의* 사라진다(외래키 검증 등 일부 경우에만 남는다). next-key lock도 row lock으로 좁아진다. 데드락이 크게 줄어든다. 트레이드오프는 명확하다. Phantom read와 Non-repeatable read가 다시 살아난다. 우리 트랜잭션이 그걸 견딜 수 있는지 점검해야 한다.

대부분의 OLTP 워크로드에서는 RC가 더 자연스럽다. PostgreSQL이 디폴트로 RC인 데에는 이유가 있다. 다만 *기존 코드가 RR에 의존한 부분이 어디인지*를 먼저 헤아려야 한다. 가장 흔한 의존이 lost update에 대한 자동 방지인데, 그 자리는 `@Version`이 메워준다. 그래서 *Read Committed로 내리되 `@Version`을 깐다*는 조합이 실무적으로 가장 안정된 답이다.

**갈래 ②: RR을 유지하되 SQL과 인덱스를 가다듬는다.** 락 범위를 최소화하는 방향으로 쿼리를 다시 짜고, 인덱스를 정밀하게 만든다. WHERE 조건이 *유니크 인덱스*의 점 조회로 들어가면 gap lock이 안 잡힌다. 그래서 PK나 유니크 키로 정확히 잡는 패턴이 우선이다. range scan은 가능한 한 피한다. 그리고 *진짜 필요한 범위*만 잠그도록 ORDER BY와 LIMIT을 조심스럽게 쓴다.

어느 갈래를 택할지는 워크로드의 모양에 따라 다르다. 다만 *모르고 들고 있는 RR*보다는 *알고 내린 RC*가 훨씬 낫다는 점은 분명하다. 의식적으로 선택하고, 그 선택의 이유를 코드 어디엔가 적어두자.

### `innodb_locks_unsafe_for_binlog`의 옛이야기

이 자리에서 한 번쯤 들어두면 좋은 옛이야기가 있다. MySQL 5.0 시절, `innodb_locks_unsafe_for_binlog`라는 변수가 있었다. 이름이 무섭다. 이 변수를 켜면 gap lock이 꺼지는 효과가 있었지만, statement 기반 binary log를 쓰는 replication 환경에서 데이터가 어긋날 위험이 있다는 의미였다. 그래서 켜기가 무서웠고, 결국 거의 안 썼다.

이 변수는 MySQL 8.0에서 deprecated 되었다. 같은 효과를 *isolation을 Read Committed로 내려서* 얻을 수 있고, row-based binary log를 쓰면 statement 기반의 안전 문제도 없기 때문이다. 즉 현대적인 MySQL 환경에서 gap lock을 피하는 표준 답은 RC이고, 옛 변수는 *역사로만* 남았다.

이 이야기가 우리에게 주는 교훈은 무엇일까. *MySQL이 gap lock을 디폴트로 갖는 데에는 이유가 있다.* 그 이유는 statement 기반 replication 환경에서 일관성을 보장하기 위함이었다. 시대가 바뀌어 row-based replication이 표준이 됐다. 그런데도 디폴트는 그대로 RR이다. 호환성 때문이다. *디폴트가 무엇이든, 의식적으로 자기 환경에 맞춰 선택할 책임은 우리에게 있다.* 이 자리에서 어느 한 번이라도 RR과 RC 사이의 트레이드오프를 점검해본 적이 있는지, 자기 코드베이스를 한 번 돌아보자.

## 결제와 재고 — 비관락이 정당화되는 두 가지 자리

낙관·비관 논쟁을 한국 커뮤니티에서 따라가다 보면 두 가지 도메인이 늘 떠오른다. 결제와 재고다. 이 두 자리는 비관락이 정당화되는 대표적인 자리이기도 하다. 한 번 들여다보고 가자.

### 재고 차감 — 비관락이 단순함을 준다

이벤트성 한정 수량 상품을 떠올려보자. 1초에 천 명이 누른다. 재고는 100개다. 어떻게 해야 정확히 100명만 결제되고 나머지는 *재고 부족*으로 안내될까.

낙관락으로 짜본다.

```java
@Transactional
public void deduct(Long productId, int quantity) {
    Product p = em.find(Product.class, productId);
    if (p.getStock() < quantity) {
        throw new OutOfStockException();
    }
    p.setStock(p.getStock() - quantity);
}
```

`@Version`이 붙어 있으니, 두 트랜잭션이 동시에 99에서 98로 차감하면 한쪽은 `OptimisticLockException`이 난다. 좋다. 그런데 천 명이 동시에 누르면? *대부분의 시도가 충돌한다*. retry를 깔면 retry storm이 생기고, retry 없이 그냥 실패시키면 운 좋은 일부만 성공한다. 어느 쪽도 만족스럽지 않다.

비관락으로 짜본다.

```java
@Transactional
public void deduct(Long productId, int quantity) {
    Product p = em.find(Product.class, productId,
                        LockModeType.PESSIMISTIC_WRITE);
    if (p.getStock() < quantity) {
        throw new OutOfStockException();
    }
    p.setStock(p.getStock() - quantity);
}
```

이제 천 명의 요청이 *줄을 선다*. row 락이 직렬화한다. 첫 사람부터 100명까지는 성공하고, 그 뒤는 `OutOfStockException`을 받는다. 동시성 처리량은 떨어지지만, *코드가 단순하고 결과가 예측 가능하다*. 한정 수량 이벤트처럼 *충돌이 본질인* 도메인에서는 이 단순함이 큰 가치가 된다.

물론 진짜로 1초에 천 건의 동시 요청을 단일 row의 비관락으로 받아내는 건 한계가 있다. 그래서 더 큰 규모로 가면 Redis로 사전 차감을 하거나, 재고를 여러 row로 *샤딩*하거나, 메시지 큐로 비동기 처리하는 식으로 넘어간다. 다만 *RDB만으로 처리할 수 있는 규모 안에서는* 비관락이 가장 단순한 답이다. "낙관락이 디폴트"라는 합의에서 *예외가 정당화되는* 자리다.

### 결제 처리 — 짧은 critical section 안의 직렬화

결제 처리의 코어 흐름을 그려보자. 잔액을 읽고, 검증하고, 차감하고, 거래 기록을 남긴다. 이 흐름은 *원자적으로* 일어나야 한다. 잔액이 1만 원이고 두 결제 요청이 각 7,000원씩이라면, 둘 중 하나만 성공해야 한다. 둘 다 성공하면 잔액이 -4,000원이 된다. 끔찍한 일이다.

낙관락도 이 자리에 답이 된다. `@Version`이 있으면 두 트랜잭션 중 늦은 쪽은 실패한다. 다만 결제처럼 *비즈니스적으로 충돌이 자주 일어나는* 자리에서는 비관락이 더 자연스럽다. 짧은 critical section을 줄을 세워 통과시키는 모양이다.

```java
@Transactional
public void pay(Long accountId, BigDecimal amount) {
    Account a = em.find(Account.class, accountId,
                        LockModeType.PESSIMISTIC_WRITE);
    if (a.getBalance().compareTo(amount) < 0) {
        throw new InsufficientFundsException();
    }
    a.withdraw(amount);
    paymentLogRepository.save(new PaymentLog(accountId, amount));
}
```

여기서 주의할 것 하나. 이 트랜잭션 안에서 *외부 결제 PG 호출이 일어나면 안 된다*. PG 호출은 네트워크에 따라 100밀리초가 될 수도, 5초가 될 수도 있다. 그 시간 동안 `Account` row가 잠긴다. 다른 사용자의 결제가 그 5초 동안 줄을 선다. 끔찍한 일이다.

해법은 *외부 호출과 DB 트랜잭션을 분리하는 것*이다. 짧은 비관락 트랜잭션으로 잔액을 잠가두고 결제 *시도* 상태로 만들어두고, 트랜잭션을 끊는다. 그 다음 PG를 호출한다. 응답이 오면 새 트랜잭션을 열어 결과에 따라 *확정* 또는 *롤백 보상*을 한다. 트랜잭션이 짧다는 전제가 비관락의 안전성을 떠받친다. *외부 I/O 동안 락을 들고 있는 코드는 사고로 가는 지름길이다.*

### 두 도메인에서 배우는 한 가지 — *짧고 정당하다면 비관*

결제와 재고가 우리에게 가르쳐주는 한 가지를 정리해두자. *비관락이 옳은 자리는 짧고 정당한 자리뿐이다.* 짧다는 건 critical section이 ms 단위라는 뜻이고, 정당하다는 건 *충돌 자체가 도메인의 본질*이라는 뜻이다. 이 두 조건을 못 채우면 일단 낙관락으로 돌아가자. 그게 시스템 전체에 가장 부드러운 답이다.

## 합의 — 낙관이 디폴트, 비관은 정당화 필요

긴 길을 함께 걸어왔다. 마지막으로 합의를 한 줄로 굳혀두자.

*낙관락이 디폴트, 비관락은 정당화가 필요한 선택.*

이 합의를 풀어 쓰면 이렇다. 사용자가 화면을 보고 결정하는 모든 자리, 즉 *다중 HTTP 요청*을 사이에 두는 워크플로는 *낙관락만이 답*이다. 비관락은 들고 갈 수가 없다. 한편 하나의 트랜잭션 안의 짧은 critical section, *충돌이 본질인* 자리에서는 비관락이 정당화된다. 결제와 재고가 대표적이다. 그 외에는 의심부터 해보자.

이 합의를 받아들이고 나면 새 도메인을 만났을 때 첫 질문이 단순해진다. "이 자리에 트랜잭션이 *사람의 결정*을 사이에 두고 있는가?" 그렇다면 낙관락이다. "이 자리가 *충돌이 본질인 짧은 critical section*인가?" 그렇다면 비관락도 검토한다. 두 질문이 우리를 적절한 도구로 데려간다.

### MVCC와 PersistenceContext 한 번 더

8장의 시작에서 본 두 층의 일관성을 한 번 더 짚어두자. *DB의 MVCC*가 한 트랜잭션 안의 read consistency를 받쳐주고, *Hibernate의 PersistenceContext*가 application 레벨에서 같은 일관성을 두른다. 우리가 짠 코드가 한 트랜잭션 안에서 같은 row를 두 번 보면 *같은 인스턴스가 나오리라*는 직관은 그래서 옳다. 두 층이 동시에 받쳐주기 때문이다.

그런데 그 일관성은 *트랜잭션의 경계 안에서만* 유효하다. 다음 요청은 새 트랜잭션이고 새 PersistenceContext다. 화면을 사이에 둔 두 결정은 *서로 다른 두 세상*에서 일어난다. 그 두 세상을 묶어주는 끈이 `@Version`이다. 끈이 없으면 lost update가 일어난다. 7장의 PersistenceContext와 8장의 `@Version`이 한 줄로 이어진다.

## 내 코드 점검 — 세 가지 체크리스트

이 장의 끝에서 우리 코드를 직접 들여다보자. 세 가지만 확인해보자.

**하나, 동시 수정이 가능한 엔티티에 `@Version`이 있는가.** "사용자가 화면을 보고 수정 버튼을 누르는" 흐름이 닿는 모든 엔티티가 후보다. 한 번 grep해보자.

```bash
grep -r "@Version" src/main/java/
```

리스트가 짧다면 의심해봐야 한다. 일반적인 비즈니스 도메인에서 `@Version`이 붙어야 할 엔티티는 *훨씬* 많기 마련이다. 회원의 프로필, 상품, 주문, 게시글, 댓글 — 사람이 동시에 손댈 수 있는 거의 모든 핵심 엔티티가 후보다. 빠진 자리가 보이면 *지금 당장 PR을 올리는 편이 낫다*. 그 자리가 운영에서 lost update를 일으키기 전에.

**둘, MySQL을 쓴다면 핵심 트랜잭션의 isolation을 확인해본 적 있는가.** 결제, 재고, 잔액 같은 핵심 트랜잭션 한두 개를 골라, 그 트랜잭션이 *실제로* 어떤 isolation에서 돌아가는지 확인해보자.

```sql
SELECT @@transaction_isolation;
```

기본은 `REPEATABLE-READ`다. 만약 이 isolation이 *의식적으로 선택된 게 아니라 디폴트라서* 그렇다면, 한 번 가만히 멈춰보자. 우리 트랜잭션이 RR의 next-key lock과 친한가? 우리 시스템이 *Phantom을 막아야* 잘 도는가? 아니면 *그저 디폴트라서* 그 자리에 있는가? 디폴트라는 답이라면, Read Committed로 내리고 `@Version`으로 보완하는 조합을 진지하게 검토해보자. Phantom을 막아야 하는 자리라면 그 자리만 명시적으로 RR로 두는 편이 낫다. 의식적인 선택이 답이다.

**셋, `SELECT ... FOR UPDATE`를 쓰는 곳이 있다면, gap lock의 범위를 추적해본 적 있는가.** 코드에서 `@Lock(LockModeType.PESSIMISTIC_WRITE)`나 native query의 `FOR UPDATE`를 찾아보자.

```bash
grep -r "PESSIMISTIC_WRITE\|FOR UPDATE" src/main/java/
```

각 자리에서 다음을 묻자. *이 SELECT의 WHERE 절은 어떤 인덱스를 타는가? 그 인덱스의 범위는 어디부터 어디까지인가? MySQL이라면 그 범위 전체에 gap lock이 잡힌다는 사실을 알고 있었는가?* 한 자리라도 답이 흐릿하면, EXPLAIN을 한 번 떠보자. 잠기는 범위가 의도와 다르면 *쿼리를 다시 쓰거나, isolation을 RC로 내리거나, 인덱스를 정밀하게 만든다*. 알고 들고 있는 칼이 모르고 들고 있는 칼보다 안전하다.

이 세 점검을 마치고 나면 우리 시스템의 동시성 안전성에 대한 *자기 확신*이 한 단계 올라간다. 그 자신감은 결국 사용자에게 정확한 결과를 돌려주는 것으로 이어진다.

## 다음 장 예고

이 장에서 우리는 동시성을 다루는 두 도구 — 낙관락과 비관락 — 을 손에 쥐었다. 한 가지 토대가 깔렸다. *읽기와 쓰기가 동시에 일어나는 모든 자리*에 우리는 이제 의식적으로 답할 수 있다.

그런데 우리가 다룬 모든 흐름은 한 가지 가정 위에 서 있었다. *한 번에 한 row, 또는 비교적 적은 수의 row를 다룬다*는 가정이다. 만약 한꺼번에 30만 건을 INSERT해야 한다면? 한꺼번에 10만 건을 UPDATE해야 한다면? 그때는 단일 row의 락 이야기가 아니라, *대량 처리의 모양*을 다시 그려야 한다.

다음 장에서는 그 자리로 간다. JDBC batch, `flush()`+`clear()` 루프, StatelessSession, 벌크 UPDATE — 대량 write를 견디게 만드는 도구들을 한 번에 풀어본다. 30분 걸리던 INSERT을 1분 안에 끝내는 그 한 줄짜리 설정이 무엇인지, 왜 그게 켜지지 않은 코드가 아직도 운영에 잔뜩 굴러다니는지, 함께 살펴보자.
