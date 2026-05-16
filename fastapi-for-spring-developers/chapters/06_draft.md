<!-- 개정: 2026-05-16 라운드 1 가디언 피드백 반영 (Should 1: Matthew Brown 인용 형식 — 옵션 b 채택, 번역임을 명시) -->

# 6장. 트랜잭션 — `@Transactional`이 없는 세상에서 살아남기

송금 API 하나를 Spring으로 짠다고 해보자. `TransferService.transfer(from, to, amount)` 메서드가 머릿속에 그려진다. 출금 계좌의 잔액을 차감하고, 입금 계좌의 잔액을 증가시키고, 거래 내역을 한 줄 남긴다. 세 줄짜리 로직이다. 그리고 이 메서드 위에는 모두가 알다시피 `@Transactional` 한 줄이 박혀 있다. 출금이 성공한 뒤 입금에서 예외가 나면 출금까지 자동으로 롤백된다. 우리 손이 닿기 전에 Spring이 알아서 한다.

이 자동의 무게는 평소에는 잘 의식되지 않는다. 그런데 `@Transactional`을 빼본 사람이라면 안다 — 그 한 줄이 사라지면 코드 곳곳에 `try/catch`와 명시적 롤백이 흩뿌려지고, 누군가는 분명히 빼먹는다. 그렇게 빠진 자리에서 *부분 실패*가 새어 나간다. 어떤 계좌에서는 돈이 빠졌는데, 다른 계좌에는 들어가지 않는다. 끔찍한 일이다.

이제 같은 송금을 FastAPI로 짜본다고 해보자. SQLAlchemy 2.0의 비동기 세션을 쓰고, 라우트는 `Depends(get_db)`로 세션을 주입받는다. 그런데 `@Transactional`을 어디에 달지? 답은 — **없다.** FastAPI/SQLAlchemy에는 `@Transactional` 어노테이션 자체가 없다. 손이 잠시 멈춘다. "그럼 트랜잭션은 누가 시작하고 누가 닫지?" 살짝 난감하다. 이 난감함이 이 챕터의 출발점이다.

핵심 질문은 둘이다. **`@Transactional` 한 줄이 사라진 자리에 무엇을 놓아야 같은 안전성을 얻는가?** 그리고 **한 요청 안의 트랜잭션 경계를 어디에 그어야 하는가?** 둘 다 이론이 아니라 손에 잡히는 회로의 문제다. 책에서 가장 큰 인지 전환이 일어나는 자리이기도 하다. 한 발 한 발 함께 그려보자.

## 왜 흉내 내지 않았는가 — 명시성의 철학

먼저 묻고 가자. SQLAlchemy도 Python에 어노테이션 비슷한 데코레이터가 있고, FastAPI도 `Depends`로 횡단관심사를 처리할 줄 안다. 그런데 왜 둘 다 `@Transactional`을 안 만들었을까? 안 만든 게 아니라 *의도적으로 안 만든* 쪽에 가깝다.

이유를 한 줄로 정리하면 — **명시성의 철학**이다. Python 진영에는 "Explicit is better than implicit"(명시적인 게 암묵적인 것보다 낫다)이라는 PEP 20의 한 줄이 통주저음처럼 깔려 있다. Spring의 `@Transactional`은 강력하지만, 그 강력함 뒤에는 *숨겨진 동작*이 잔뜩 깔려 있다. 프록시 객체를 만들어 메서드 호출을 가로채고, 같은 클래스 안의 호출은 프록시를 통하지 않아 트랜잭션이 *조용히* 적용되지 않는다. 전파(propagation) 옵션은 `REQUIRED`/`REQUIRES_NEW`/`NESTED` 등 일곱 가지가 있고, 어느 게 켜져 있는지 코드만 봐서는 안 보인다. 익숙하면 편리하지만, 처음 들어온 사람에게는 마법처럼 보이는 자리다.

SQLAlchemy는 그 마법을 일부러 걷어냈다. 트랜잭션은 *눈에 보이는 구문*으로 시작하고 닫는다. `session.begin()`을 호출하는 자리가 트랜잭션의 시작이고, `commit()` 또는 `rollback()`이 끝이다. 컨텍스트 매니저를 쓰면 `with` 블록의 들여쓰기가 곧 트랜잭션의 범위다. 코드 한눈에 *어디서 시작해 어디서 닫히는지*가 보인다.

> "Hibernate는 Session 인스턴스를 SessionFactory로 만든다. SQLAlchemy는 unit-of-work 개념에 더 집중하는데, 처음엔 이해·사용이 어렵지만 나중에 우연한 commit-타이밍 버그를 거의 0으로 줄여주는 가치를 깨닫게 된다." — QuietShark 블로그(reference §2.4)

이 평가가 핵심을 짚는다. 처음에는 *번거롭게* 느껴지지만, 시간이 지나면 *우연한 버그를 줄이는* 자리로 돌아온다는 것. Spring 출신이 처음 6장을 읽으면 "한 줄로 끝나던 일을 왜 이렇게 길게 풀어 쓰지?"라고 묻게 된다. 답은 — **길어진 게 아니라 *드러난* 것이다.** Spring에서는 보이지 않던 *시작과 끝*이 FastAPI에서는 코드 위에 명시적으로 드러난다.

기억해두자. 이 챕터의 모든 패턴은 같은 약속을 향한다 — *트랜잭션은 우리가 시작하고 우리가 닫는다.* 손이 잠시 더 가지만, 그 손길이 곧 안전망이다.

## 흔한 안티패턴 — `get_db()` finally에서 commit

처음 SQLAlchemy 트랜잭션 코드를 짜는 사람이 흔히 빠지는 함정 하나를 짚고 가자. 인터넷을 뒤지면 다음과 비슷한 의존성 함수가 의외로 자주 보인다.

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()         # ← 안티패턴
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

"세션을 의존성에서 만들고, 함수가 끝나면 자동으로 commit이나 rollback이 나가게 한다"는 발상 자체는 자연스럽다. Spring의 `@Transactional`이 자동으로 해주던 일을 의존성의 `try/finally`에서 흉내 내는 셈이다. 그런데 이 코드는 *조용히 잘못 동작한다*.

문제의 핵심은 FastAPI의 의존성 라이프사이클에 있다. `yield`로 세션을 흘려준 뒤 *돌아오는* 코드는 라우트 함수가 *반환된 뒤*, 그리고 응답이 클라이언트로 *나간 뒤*에 실행된다. 무슨 뜻이냐면 — `await session.commit()`이 호출되는 순간 클라이언트는 이미 "성공"이라는 200 응답을 받았다는 뜻이다. 그런데 그 `commit()`이 실패하면? 데이터베이스에는 아무것도 안 들어갔는데, 사용자는 성공 응답을 받은 상태다. 정확히 부분 실패의 끔찍한 형태다.

> "의존성의 `finally` 절에서 `commit`을 할 수 없다 — 그 코드는 경로 함수가 끝나고 결과가 클라이언트에 반환된 **뒤에** 실행된다. 그때 발생하는 예외는 응답에 영향을 주지 않지만 트랜잭션은 실패한 상태가 된다." — GitHub: Request-scoped transactions(reference §2.3)

문장이 길지만 핵심은 한 줄이다. **`commit`은 응답이 나가기 *전에* 일어나야 한다.** 의존성의 `finally`는 응답이 나간 *뒤*다. 둘 사이에는 메우기 어려운 시간 간격이 있다.

그래서 의존성 함수는 "세션을 열고 닫는" 일만 한다. commit과 rollback은 *라우트 안*에서 명시적으로. 다음이 그 원형이다.

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
        # commit은 여기서 하지 않는다. 라우트 또는 서비스 레이어에서 명시한다.
```

`async with AsyncSessionLocal()`이 세션을 열고, 블록이 끝나면 자동으로 `close()`를 호출한다. 트랜잭션 *시작*과 *종료*는 일부러 빈 자리로 남겨둔다. Spring 출신이 보면 "허전하지 않나?" 싶지만, 이 허전함이 의도다. *허전한 자리에 우리 손이 들어간다.*

## 권장 패턴 — `async with session.begin():`

이제 진짜 트랜잭션 경계를 그리는 자리로 가자. 다음 코드를 보자.

```python
@router.post("/transfers")
async def create_transfer(
    payload: TransferCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TransferRead:
    async with db.begin():
        src = await db.get(Account, payload.from_id, with_for_update=True)
        dst = await db.get(Account, payload.to_id, with_for_update=True)
        if src.balance < payload.amount:
            raise InsufficientBalance(payload.from_id)
        src.balance -= payload.amount
        dst.balance += payload.amount
        db.add(Transfer(from_id=src.id, to_id=dst.id, amount=payload.amount))
    return TransferRead(...)
```

핵심은 `async with db.begin():` 블록이다. 들여쓰기로 묶인 네 줄이 곧 *한 트랜잭션*이다. 블록을 정상적으로 빠져나오면 `commit()`이 호출되고, 블록 안에서 예외가 발생하면 `rollback()`이 자동으로 호출된다. Spring의 `@Transactional`이 메서드 경계로 트랜잭션을 그렸다면, FastAPI/SQLAlchemy는 *들여쓰기로* 그린다.

이 패턴이 왜 안전한가를 짚어보자. 첫째, *시작과 끝이 한눈에 보인다.* 메서드 안에 다른 메서드 호출이 끼어들어도 트랜잭션 범위가 흐려지지 않는다. 둘째, 예외가 발생하면 *자동 롤백*이 보장된다 — Spring의 unchecked 자동 롤백과 사실상 같은 안전망이다. 셋째, `commit`이 *응답이 나가기 전*에 호출된다. `with` 블록의 종료는 라우트 함수의 *반환 직전*이라, commit이 실패하면 그 자리에서 예외가 터져 적절한 5xx 응답으로 변환된다.

비교를 위해 Spring 코드를 같은 자리에 놓아보자.

```kotlin
// Spring (Kotlin)
@Service
class TransferService(private val accountRepo: AccountRepository, ...) {

    @Transactional
    fun transfer(fromId: Long, toId: Long, amount: BigDecimal) {
        val src = accountRepo.findByIdForUpdate(fromId)
        val dst = accountRepo.findByIdForUpdate(toId)
        if (src.balance < amount) throw InsufficientBalanceException(fromId)
        src.balance -= amount
        dst.balance += amount
        transferRepo.save(Transfer(src.id, dst.id, amount))
    }
}
```

두 코드를 옆에 놓고 보면 차이가 분명하다. Spring은 `@Transactional` 한 줄이 메서드 전체를 감싸 트랜잭션 범위로 만든다. FastAPI/SQLAlchemy는 `async with db.begin():` 들여쓰기가 같은 역할을 한다. 표현이 *어노테이션 대신 블록*이라는 점만 다르다. 같은 안전망이 다른 모양으로 표현된 셈이다.

그렇다면 의문이 하나 남는다. *블록의 위치*는 어디에 두는 게 좋을까? 라우트일까, 서비스 레이어일까? 이게 다음 절의 주제다.

## 트랜잭션 경계를 어디에 그을지

위 예제에서는 트랜잭션 블록이 라우트 함수 안에 있었다. 학습용으로는 한눈에 들어와서 좋지만, 도메인이 커지면 *서비스 레이어*로 옮기는 게 보통이다. Spring에서 `@Transactional`을 컨트롤러가 아니라 서비스 메서드에 다는 관행과 정확히 같은 이유다.

서비스 레이어로 옮긴 모양은 다음과 같다.

```python
# services/transfer_service.py
class TransferService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def transfer(self, payload: TransferCreate) -> Transfer:
        async with self._db.begin():
            src = await self._db.get(Account, payload.from_id, with_for_update=True)
            dst = await self._db.get(Account, payload.to_id, with_for_update=True)
            if src.balance < payload.amount:
                raise InsufficientBalance(payload.from_id)
            src.balance -= payload.amount
            dst.balance += payload.amount
            transfer = Transfer(from_id=src.id, to_id=dst.id, amount=payload.amount)
            self._db.add(transfer)
            return transfer
```

```python
# routers/transfer_router.py
@router.post("/transfers")
async def create_transfer(
    payload: TransferCreate,
    svc: Annotated[TransferService, Depends(get_transfer_service)],
) -> TransferRead:
    transfer = await svc.transfer(payload)
    return TransferRead.model_validate(transfer)
```

라우트는 *얇아지고*, 서비스가 *진짜 일*을 한다. 트랜잭션 경계는 서비스 메서드 안에 그어졌다. 라우트는 그 위에서 입력 검증과 응답 변환만 책임진다. Spring의 컨트롤러-서비스 분리와 같은 모양이다.

여기서 한 가지 약속을 두고 가자. **트랜잭션은 서비스 레이어에서 시작하고 닫는다.** 라우트는 트랜잭션을 의식하지 않는다. 이 약속은 책 전체에서 그대로 들고 간다 — 9장(예외·관측성)도 이 가정을 전제로 도메인 예외를 짠다.

물론 이 약속에는 *생각해볼 만한 함정*이 하나 있다. 한 요청 안에서 *여러 서비스 메서드*가 호출되면, 각자 자기 트랜잭션을 열기 때문에 *전체로는 트랜잭션이 분리된다.* Spring의 전파(`REQUIRED`)가 자동으로 해결해주던 일을 FastAPI는 *조용히 분리해서* 처리한다. 사용자가 의도한 게 한 트랜잭션이라면, 명시적으로 묶어야 한다. 다음과 같이.

```python
async def transfer_with_audit(self, payload: TransferCreate, audit: AuditLog) -> Transfer:
    async with self._db.begin():
        transfer = await self._transfer_core(payload)   # 같은 세션, 같은 트랜잭션
        await self._audit_log(audit)                    # 같은 세션, 같은 트랜잭션
        return transfer
```

핵심은 *같은 세션을 공유*하고 *바깥에 트랜잭션 블록 하나*를 두는 것이다. 그 안의 내부 메서드들은 트랜잭션을 *시작하지 않는다* — 단지 그 안에서 동작할 뿐이다. Spring의 `Propagation.REQUIRED`가 처리하던 일을 *세션 공유 + 최상위 블록*이라는 단순한 회로로 명시한다. 보이지 않던 게 보이는 자리로 옮겨왔다.

## Unit of Work — Matthew Brown의 비판과 대안

여기까지 따라오면 한 가지 의문이 든다. "세션을 매번 `Depends(get_db)`로 받아서 서비스에 넘기는 게 깔끔한가? Spring의 `@PersistenceContext`처럼 *암묵적으로* 잡혀 있으면 안 되나?" 자연스러운 질문이고, 같은 질문을 한 사람이 이미 있다.

> Matthew Brown의 글이 같은 문제를 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *DI로 long-lived 세션을 라우트 전체에 노출하는 흔한 패턴이 요청-내 longtail 트랜잭션을 만든다*. — "FastAPI database session dependency injection considered harmful" (reference §4.2)

*요청-내 longtail 트랜잭션*. 이 표현이 정확하다. 의존성으로 받은 세션을 라우트 한참 위에서 열고, 라우트 한참 아래에서 닫으면, 그 사이의 모든 시간이 트랜잭션 안에 들어간다. 그 시간 동안 데이터베이스의 락이 잡혀 있고, 다른 요청들이 그 락 뒤에 줄을 선다. 한두 요청이면 모르지만, 트래픽이 늘면 *조용한 성능 하락*으로 돌아온다. 찜찜한 일이다.

Brown의 대안은 *Unit of Work 객체*다. 라우트는 세션을 직접 받지 않고, *Unit of Work 컨텍스트*를 받는다. 그 컨텍스트 안에서만 트랜잭션이 열리고 닫힌다. 코드로 보자.

```python
class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._factory = session_factory

    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._factory()
        await self._session.begin()
        self.accounts = AccountRepository(self._session)
        self.transfers = TransferRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()
        await self._session.close()
```

라우트는 *세션 대신 UoW*를 의존성으로 받는다.

```python
async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork(AsyncSessionLocal) as uow:
        yield uow

@router.post("/transfers")
async def create_transfer(
    payload: TransferCreate,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> TransferRead:
    src = await uow.accounts.get(payload.from_id, lock=True)
    dst = await uow.accounts.get(payload.to_id, lock=True)
    if src.balance < payload.amount:
        raise InsufficientBalance(payload.from_id)
    src.balance -= payload.amount
    dst.balance += payload.amount
    await uow.transfers.add(Transfer(from_id=src.id, to_id=dst.id, amount=payload.amount))
    return TransferRead.model_validate(...)
```

`with` 블록이 사라진 자리에 *UoW의 컨텍스트 매니저*가 들어와 있다. 트랜잭션의 시작과 끝은 UoW의 `__aenter__`/`__aexit__`에 캡슐화됐다. 라우트에서 보면 트랜잭션 시작 구문이 사라진 것처럼 보이지만, *사라진 게 아니라 한 군데로 모아둔 것이다.*

물론 이 패턴에도 비판이 있다. "또 하나의 추상화 레이어를 만들 만한 가치가 있는가?" 작은 프로젝트라면 `async with session.begin()` 직접 쓰는 편이 낫다. 도메인이 셋·넷으로 늘고, 트랜잭션 경계 규칙이 팀 차원의 약속이 되면, UoW가 그 약속을 *코드로* 강제하는 자리에 들어간다. *지금 당장*이 아니라 *언제쯤* UoW로 옮기면 좋을지를 기억해두자 — 보통 도메인 수가 다섯을 넘고, 한 요청 안에서 두 도메인 이상이 같이 변경되는 시나리오가 잦아지는 시점이다.

## 격리·롤백·savepoint

다음으로 짚을 자리는 *트랜잭션의 세 가지 손잡이*다. 격리 수준(isolation level), 롤백, savepoint. Spring 출신이라면 `@Transactional(isolation = Isolation.REPEATABLE_READ)` 같은 코드를 본 적이 있을 것이다. 같은 손잡이가 SQLAlchemy에도 있다 — 그저 어노테이션이 아니라 *연결 옵션*으로 노출돼 있을 뿐이다.

격리 수준부터 보자. Spring의 다섯 가지(`DEFAULT`/`READ_UNCOMMITTED`/`READ_COMMITTED`/`REPEATABLE_READ`/`SERIALIZABLE`)는 데이터베이스 표준의 격리 수준 그대로다. SQLAlchemy에서는 `engine`을 만들 때 또는 *연결 단위로* 격리 수준을 지정한다.

```python
# 엔진 전역 기본값
engine = create_async_engine(DB_URL, isolation_level="REPEATABLE READ")

# 특정 트랜잭션에만 적용 — 연결 옵션을 그 자리에서 바꿈
async with engine.connect() as conn:
    conn = await conn.execution_options(isolation_level="SERIALIZABLE")
    async with conn.begin():
        ...
```

Spring처럼 *메서드 단위*로 격리 수준을 다르게 거는 패턴도 가능하다 — 단지 `@Transactional(isolation=...)` 대신 `execution_options(isolation_level=...)`을 직접 호출하면 된다. 보이지 않던 손잡이가 *눈에 보이는 함수 호출*로 나왔다.

롤백은 어떨까? 이게 Spring 출신이 가장 자주 부딪히는 차이 중 하나다.

> Spring 기본 정책: **unchecked 예외(`RuntimeException` 계열)는 자동 롤백**, checked 예외는 자동 롤백 *안 함*(설정으로 바꿀 수 있음).

SQLAlchemy/Python 진영에는 checked/unchecked 구분이 없다. 모든 예외는 그냥 `Exception`이다. 그래서 SQLAlchemy의 정책은 단순하다 — **`async with session.begin()` 블록 안에서 발생한 모든 예외는 롤백된다.** 블록을 정상 종료하면 commit, 예외가 새어 나가면 rollback. 손에 그리기 쉽다.

savepoint도 그대로 있다. 트랜잭션 안에서 일부만 롤백하고 싶을 때 `begin_nested()`를 쓴다.

```python
async with db.begin():
    await create_user(user)
    try:
        async with db.begin_nested():     # savepoint
            await send_welcome_email_in_db(user)
    except EmailQueueFull:
        # savepoint까지만 롤백, 사용자 생성은 유지
        pass
```

Spring `@Transactional(propagation = Propagation.NESTED)`과 같은 자리다. SQLAlchemy는 savepoint를 *별도의 컨텍스트 매니저*로 노출했다 — 트랜잭션 안의 트랜잭션이 어디서부터 어디까지인지 들여쓰기로 표현된다.

여기서 한 가지 정리를 두자. Spring의 `@Transactional` 한 줄에는 *전파·격리·롤백 규칙·timeout·readOnly* 등 옵션이 잔뜩 박힐 수 있다. SQLAlchemy는 같은 옵션을 *서로 다른 자리에* 분산시켰다. 처음에는 손이 더 많이 가지만, 옵션이 *어디서 적용됐는지* 코드에서 정확히 추적된다. 강점이자 부담이다.

타임아웃과 readOnly는 어떻게 옮겨갈까? `statement_timeout`은 PostgreSQL의 경우 연결 수준에서 `SET LOCAL statement_timeout = '5s'`를 한 줄 실행해주면 된다. readOnly는 SQLAlchemy의 트랜잭션에는 직접 대응되는 플래그가 없지만, *세션 자체를 읽기 전용 엔진*에 묶거나 트랜잭션 시작 후 `SET TRANSACTION READ ONLY` 한 줄을 호출하는 패턴이 일반적이다. Spring처럼 어노테이션 한 줄로 끝나는 우아함은 없다 — 대신 *어떤 SQL이 실제로 실행되는지*가 한눈에 보인다. 어느 쪽이 더 좋은가는 취향이지만, *디버깅이 필요한 순간*에는 두 번째 쪽이 훨씬 친절하다.

한 가지 더. **`with_for_update`로 거는 비관적 락**은 트랜잭션의 손잡이 중 가장 자주 쓰는 자리다. 송금 같이 *두 행을 동시에 잠가야* 안전한 시나리오에서는 락 *순서*도 신경 써야 한다. 두 트랜잭션이 같은 두 계좌를 반대 순서로 잠그면 데드락이 난다. Spring/Hibernate에서도 같은 문제가 있어서 *계좌 ID 오름차순으로 락을 거는* 관행이 굳어 있다. SQLAlchemy도 똑같다 — `payload.from_id`와 `payload.to_id` 중 *작은 쪽을 먼저* 잠그는 게 안전하다. 다음과 같이.

```python
first_id, second_id = sorted([payload.from_id, payload.to_id])
first = await db.get(Account, first_id, with_for_update=True)
second = await db.get(Account, second_id, with_for_update=True)
```

이 한 줄을 빼먹으면 *부하가 늘었을 때* 조용히 데드락이 일어난다. PostgreSQL은 친절하게 한 트랜잭션을 죽이고 에러를 던지지만, 그 시간 동안 사용자는 *느린 응답*을 받는다. 끔찍한 일은 아닌데 *번거롭다.* 송금 코드를 짤 때마다 락 순서를 의식하는 습관을 들여두자.

## 예외와 롤백 — 자동의 자리에 명시가 들어선다

좀 더 풀어보자. Spring의 unchecked 자동 롤백은 우리가 평소에 의식하지 않는 안전망이다. 컨트롤러 메서드 안에서 `IllegalArgumentException`이 터지면, Spring이 알아서 트랜잭션을 롤백하고 예외를 위로 던진다. 우리가 한 일은 *예외를 던진 것뿐*이다.

FastAPI/SQLAlchemy에서 같은 시나리오를 따라가보자.

```python
@router.post("/transfers")
async def create_transfer(payload: TransferCreate, svc: ...) -> TransferRead:
    transfer = await svc.transfer(payload)
    return TransferRead.model_validate(transfer)
```

서비스 안에서 `InsufficientBalance` 예외가 던져졌다고 하자.

```python
async def transfer(self, payload: TransferCreate) -> Transfer:
    async with self._db.begin():
        ...
        if src.balance < payload.amount:
            raise InsufficientBalance(payload.from_id)
        ...
```

`raise InsufficientBalance(...)`가 호출되면 `async with self._db.begin():` 블록의 `__aexit__`가 예외와 함께 호출된다. SQLAlchemy는 *예외가 있으면 rollback*이라는 단순한 규칙으로 트랜잭션을 정리한다. 그리고 예외는 라우트로 다시 던져진다. 라우트는 9장에서 다룰 `@app.exception_handler(InsufficientBalance)`로 이 예외를 잡아 적절한 4xx 응답으로 변환한다. 한 줄도 자동인 게 없다 — 그런데 *모두 추적 가능하다.*

비교를 이렇게 정리하자. Spring은 *기본값이 안전*이다. 예외를 던지면 롤백된다. 손이 닿지 않으면 기본 정책이 작동한다. SQLAlchemy는 *명시가 안전*이다. `with` 블록 안에서 예외가 새어 나가면 롤백되고, 블록 바깥에서 발생하면 트랜잭션조차 시작되지 않은 상태다. 둘 다 결과는 같은 안전망인데 *어느 쪽이 책임지는가*가 다르다.

여기서 흔히 빠지는 함정 하나. 다음 코드를 보자.

```python
# 잘못된 패턴
async def transfer(self, payload: TransferCreate) -> Transfer:
    src = await self._db.get(Account, payload.from_id)   # 블록 바깥
    async with self._db.begin():
        if src.balance < payload.amount:
            raise InsufficientBalance(payload.from_id)
        ...
```

`db.get(Account, ...)`가 *블록 바깥*에 있다. SQLAlchemy의 비동기 세션은 자동으로 *기본 트랜잭션*을 시작하기도 하지만, 명시적인 `begin()` 블록 바깥의 쿼리가 *어느 트랜잭션*에 속하는지는 종종 헷갈린다. 권장하는 건 *모든 쿼리를 begin 블록 안*에 두는 것이다. 손에 익으면 자연스럽지만 처음에는 *어디까지 안에 둬야 할지* 살짝 헷갈리니, 한 번 머리에 새겨두자.

## 테스트에서의 트랜잭션 — 자동 롤백의 빈자리

Spring 출신이 첫 FastAPI 테스트를 짤 때 한 번은 멈칫하는 자리가 있다. 테스트 사이에 *DB 상태*가 어떻게 정리되는가?

Spring에서 `@SpringBootTest @Transactional`을 메서드에 달면 테스트가 끝날 때 자동으로 롤백된다. 한 테스트가 만든 데이터는 다음 테스트에 안 보인다. 깔끔하다. FastAPI/pytest는 그 자동을 *기본값으로 안 준다.* 무방비로 짜면 첫 테스트가 만든 데이터가 두 번째 테스트로 새어 나간다. 찜찜하고 디버깅이 까다로워진다.

대안은 두 가지다.

**첫째, savepoint 기반 fixture.** 각 테스트가 *외부 트랜잭션* 안에서 실행되고, 테스트 안의 `commit()`은 *savepoint commit*으로 가도록 한다. 테스트가 끝나면 외부 트랜잭션을 통째로 롤백한다.

```python
@pytest_asyncio.fixture
async def db_session():
    async with engine.connect() as conn:
        await conn.begin()
        async with AsyncSession(bind=conn, join_transaction_mode="create_savepoint") as session:
            yield session
        await conn.rollback()
```

`join_transaction_mode="create_savepoint"`가 핵심이다. 세션의 `commit()`이 *진짜 commit*이 아니라 *savepoint commit*으로 매핑된다. 테스트가 끝나면 외부 connection의 `rollback()`이 *모든 것을* 되돌린다. Spring의 `@Transactional` 테스트와 같은 효과다.

**둘째, truncate 기반.** 매 테스트 후에 모든 테이블을 truncate한다. 단순하지만, 테이블이 많아지면 느려진다. CI에서 테스트 수가 수백 개를 넘으면 첫 번째 패턴이 낫다.

자세한 픽스처 패턴은 10장(테스트)에서 다시 다룬다. 이 챕터에서 짚어둘 건 한 가지다 — **테스트에서의 자동 롤백도 *우리가 짜는 자리*다.** Spring이 무료로 주던 안전망이 FastAPI에서는 한 번의 픽스처 설계로 옮겨왔다. 한 번 잘 짜두면 그다음 모든 테스트가 그 위에서 안전해진다.

## 송금 시나리오 — 양면 페이지 대조

지금까지의 모든 조각을 모아 송금 API를 두 프레임워크로 짠 모습을 양면 페이지에 두고 보자. 같은 도메인, 같은 안전성, 다른 표현.

**Spring (Kotlin):**

```kotlin
@Service
class TransferService(
    private val accountRepo: AccountRepository,
    private val transferRepo: TransferRepository,
) {
    @Transactional
    fun transfer(fromId: Long, toId: Long, amount: BigDecimal): Transfer {
        val src = accountRepo.findByIdForUpdate(fromId)
            ?: throw AccountNotFound(fromId)
        val dst = accountRepo.findByIdForUpdate(toId)
            ?: throw AccountNotFound(toId)
        if (src.balance < amount) {
            throw InsufficientBalance(fromId)
        }
        src.balance -= amount
        dst.balance += amount
        return transferRepo.save(Transfer(src.id, dst.id, amount))
    }
}

@RestController
@RequestMapping("/transfers")
class TransferController(private val service: TransferService) {

    @PostMapping
    fun create(@RequestBody @Valid req: TransferRequest): TransferResponse {
        val transfer = service.transfer(req.fromId, req.toId, req.amount)
        return TransferResponse.from(transfer)
    }
}
```

`@Transactional` 한 줄이 메서드 전체를 감싸 트랜잭션 범위로 만든다. 비즈니스 로직 다섯 줄이 안전망 안에 들어간다.

**FastAPI:**

```python
# services/transfer_service.py
class TransferService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def transfer(self, payload: TransferCreate) -> Transfer:
        async with self._db.begin():
            src = await self._db.get(Account, payload.from_id, with_for_update=True)
            if src is None:
                raise AccountNotFound(payload.from_id)
            dst = await self._db.get(Account, payload.to_id, with_for_update=True)
            if dst is None:
                raise AccountNotFound(payload.to_id)
            if src.balance < payload.amount:
                raise InsufficientBalance(payload.from_id)
            src.balance -= payload.amount
            dst.balance += payload.amount
            transfer = Transfer(
                from_id=src.id, to_id=dst.id, amount=payload.amount,
            )
            self._db.add(transfer)
            await self._db.flush()
            return transfer


# routers/transfer_router.py
@router.post("", response_model=TransferRead, status_code=201)
async def create_transfer(
    payload: TransferCreate,
    svc: Annotated[TransferService, Depends(get_transfer_service)],
) -> Transfer:
    return await svc.transfer(payload)
```

`async with self._db.begin():` 블록이 같은 안전망을 그린다. `with_for_update=True`가 Spring의 비관적 락(`findByIdForUpdate`)과 정확히 같은 일을 한다. 블록 안에서 던진 모든 예외는 자동으로 롤백되고, 블록을 정상 종료하면 commit이 나간다.

두 코드를 옆에 놓고 보면 어디가 같고 어디가 다른지 한눈에 잡힌다. **트랜잭션의 시작과 끝**: Spring은 메서드 시그니처 위의 어노테이션, FastAPI는 들여쓰기로 묶인 블록. **락**: Spring은 레포지토리 메서드 이름(`findByIdForUpdate`), FastAPI는 쿼리 옵션(`with_for_update=True`). **롤백**: Spring은 unchecked 예외 자동, FastAPI는 블록 안 예외 자동. **commit 시점**: Spring은 메서드 반환 직후, FastAPI는 `with` 블록 종료 직후 — 둘 다 응답이 나가기 전이다.

이 평행성을 손에 익히면 6장의 모든 패턴이 *Spring의 자리에 무엇이 들어가는지* 같은 회로로 옮겨진다. **자동의 자리에 명시가 들어선다.** 이 한 줄을 가슴에 새겨두자.

## 한 호흡으로 정리

머리에 박혀야 할 건 셋이다.

**첫째, 트랜잭션은 우리가 시작하고 우리가 닫는다.** `@Transactional`이 자동으로 그리던 경계를 `async with session.begin():` 블록의 들여쓰기로 직접 그린다. *어디서 시작하고 어디서 닫히는지*가 코드 위에 드러나는 게 SQLAlchemy의 명시성 철학이다. 손이 잠시 더 가지만, 그 손길이 곧 안전망이다.

**둘째, 의존성 `finally`에서 `commit`하지 말자.** 응답이 이미 나간 *뒤*다. `get_db()`는 세션을 열고 닫는 일만 하고, commit과 rollback은 *라우트 또는 서비스 레이어 안*에서 명시한다. 이 한 줄이 부분 실패의 가장 흔한 함정을 막는다. 그리고 트랜잭션 경계는 *서비스 레이어*에 둔다는 약속을 책 전체에서 들고 간다.

**셋째, Spring의 옵션은 SQLAlchemy의 *서로 다른 자리*로 분산됐다.** 전파는 *세션 공유 + 최상위 블록*, 격리는 `execution_options(isolation_level=...)`, savepoint는 `begin_nested()`. 보이지 않던 손잡이가 *눈에 보이는 함수 호출*로 나왔다. 처음에는 *어디 있나 찾는* 부담이 있지만, 익숙해지면 *옵션이 어디서 적용됐는지* 정확히 추적된다.

다음 장은 인증·인가다. `@Transactional`이 사라진 자리에 `async with session.begin():`이 들어선 것처럼, 7장에서는 `@PreAuthorize("hasRole('ADMIN')")`이 사라진 자리에 `Depends(require_scope("admin"))`이 들어선다. 6·7장이 공유하는 통주저음은 한 단어다 — **명시성.** Spring Security가 무료로 막아주던 안전망을 *어떻게 명시적으로 그릴지*를 같은 회로로 풀어보자. 손에 익은 6장의 감각이 그대로 7장의 안전망 그리는 데 쓰인다. 기억해두자 — 자동의 자리에 명시가 들어선다. 이 한 줄이 책의 6·7장을 연결하는 다리다.
