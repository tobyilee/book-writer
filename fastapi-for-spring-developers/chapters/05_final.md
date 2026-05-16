# 5장. 데이터 접근 — JPA에서 SQLAlchemy 2.0으로

JPA를 쓰던 손에서 떠올려 보자. `@Entity`를 박은 클래스 하나, `extends JpaRepository<Book, Long>` 한 줄짜리 인터페이스, 그리고 `findByTitleContaining`처럼 메서드 이름만 적으면 알아서 쿼리가 만들어지는 그 마법. 우리는 거의 코드를 안 쓰고도 CRUD를 짰다. EntityManager가 1차 캐시를 잡아주고, `@Transactional` 안에서 dirty checking이 자동으로 UPDATE를 쏘아 줬다. Hibernate가 떠받쳐 주던 자동화의 두께가 이렇게 두꺼웠다.

이제 그 자동화 위에 서 있던 발을 SQLAlchemy로 옮긴다. 처음 SQLAlchemy 2.0 코드를 보면 한 가지 감각이 먼저 든다. *명시적이다*. `select(...).where(...)`라는 빌더, `session.add()`라는 직접 호출, `session.commit()`이라는 마침표. JPA가 어노테이션 뒤에 숨겨 두던 동작이 코드 위로 다 올라온다. 이게 처음엔 번거롭게 느껴진다. 그러다 어느 순간, *우연한 commit 타이밍 버그*가 0에 가까워지는 걸 깨닫는다. 명시적이라는 건 손은 더 가지만, 머릿속이 더 깨끗하다는 뜻이다.

SQLAlchemy 진영의 공식 설명도 이 차이를 한 줄로 짚는다 — Hibernate가 Session을 SessionFactory로 만드는 데 비해, SQLAlchemy는 *unit-of-work* 개념에 더 집중하는 쪽이라고. 처음엔 어렵게 느껴지지만, 점점 *우연한 commit-타이밍 버그*가 0에 가까워진다.

그렇다면 어디서부터 손을 대야 할까. 도서 카탈로그를 예제로 잡고, 모델 정의 → 쿼리 → 세션 다루기 → 레포지토리 직접 짜기 → Alembic 마이그레이션 → 폴더 구조 약속까지 한 호흡으로 짚어보자. JPA 사고가 그대로 가는 부분, 살짝 비틀어야 하는 부분, 완전히 다시 짜야 하는 부분을 하나씩 분리해 보자.

> **이 장을 읽기 전 알아둘 것**
> - 4장의 `Depends()`와 `yield` 의존성, `app.dependency_overrides`는 본 장의 모든 라우트가 *전제*한다. 4장의 §`yield` 의존성·§테스트 오버라이드 두 절은 반드시 보고 오자.
> - 본 장은 동기 SQLAlchemy로 가르친다. async 모드는 8장에서 다시 본다.

## SQLAlchemy 2.0의 정체성 — Hibernate와 닮은 점, 다른 점

SQLAlchemy는 두 층으로 짜여 있다. **Core**(SQL Expression Language)와 **ORM**이다. Core는 "안전한 쿼리 빌더"고, ORM은 그 위에 클래스 ↔ 테이블 매핑을 얹은 층이다. Hibernate는 둘이 한 덩어리지만, SQLAlchemy는 둘이 분리돼 있다. ORM이 답답하면 언제든 Core로 내려갈 수 있다 — JPA에서 native query로 떨어지는 그 자리에 SQLAlchemy Core가 있다.

2.0 버전(2023년 1월 정식 출시)이 짜놓은 새 스타일은 한 줄로 요약된다. **모든 쿼리가 `select(...)`로 시작한다**. 1.x의 `session.query(User).filter(...).all()`은 더 이상 권장되지 않는다. 새 코드에선 이렇게 쓴다.

```python
result = session.execute(
    select(User).where(User.email == "tobi@example.com")
)
user = result.scalar_one_or_none()
```

처음엔 `session.execute().scalar_one_or_none()`이 장황해 보인다. JPQL의 `entityManager.createQuery("from User where email = :email", User.class)`와 같은 결과를 두 줄로 받는 데 어색함이 있다. 그러나 이게 정확히 *세션의 SQL 실행*과 *결과 형태*를 분리해 둔 모양이다. 같은 select가 ORM 객체로 떨어질 수도, Core row로 떨어질 수도, 단일 컬럼 스칼라로 떨어질 수도 있는 미래를 위해 한 단계를 둔 셈이다.

표 하나로 정신적 모양을 정렬해 두자.

| 측면 | Hibernate / JPA | SQLAlchemy 2.0 |
|---|---|---|
| 모델 정의 | `@Entity`, JPA 어노테이션 | `class User(DeclarativeBase)` + `Mapped[...]` |
| 쿼리 언어 | JPQL/HQL 또는 Criteria API | Core expression — `select(User).where(...)` |
| 영속성 컨텍스트 | EntityManager (1차 캐시) | Session (Identity Map + Unit of Work) |
| Flush 타이밍 | commit/쿼리 직전 자동 flush | autoflush=True 기본이나, 명시적 통제 권장 |
| Lazy loading | 프록시, 트랜잭션 종료 후 `LazyInitializationException` | 세션 분리 후 접근 → **`DetachedInstanceError`**. async는 더 까다로움 |
| 마이그레이션 | Flyway / Liquibase (외부 도구) | Alembic (SQLAlchemy 메타데이터를 직접 읽음) |
| 자동 레포지토리 | `extends JpaRepository<T, ID>` | **없다.** `class UserRepository:`를 손으로 작성 |
| 트랜잭션 | `@Transactional` (선언적) | `session.begin()` (명시적) — 6장 |

마지막 두 행이 가장 큰 충격이다. *자동 레포지토리가 없다*는 것 — 이게 본 장 후반의 큰 그림이다. *선언적 트랜잭션이 없다*는 것 — 이게 다음 장의 hinge다.

## 모델 정의 — `@Entity` 자리에 `DeclarativeBase`

도서 카탈로그를 짜보자. 도메인은 셋이다. `Book`, `Author`, `Category`. 다대다(Book ↔ Category)와 다대일(Book → Author) 관계가 한 번씩 등장한다. JPA로 짰다면 익숙한 어노테이션 더미가 등장하는 자리다. Kotlin/JPA로 짠 그림이 가장 짧으니 옮겨 적었다 — Java로 같은 일을 하면 getter/setter가 줄을 더한다.

```kotlin
// Spring (Kotlin) — JPA
@Entity
@Table(name = "books")
class Book(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false, length = 200)
    val title: String,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    val author: Author,

    @ManyToMany
    @JoinTable(
        name = "book_categories",
        joinColumns = [JoinColumn(name = "book_id")],
        inverseJoinColumns = [JoinColumn(name = "category_id")],
    )
    val categories: MutableSet<Category> = mutableSetOf(),
)
```

같은 그림을 SQLAlchemy 2.0으로 옮기자.

```python
# SQLAlchemy 2.0
from __future__ import annotations

from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped[Author] = relationship(back_populates="books")
    categories: Mapped[set[Category]] = relationship(
        secondary=book_categories, back_populates="books"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    books: Mapped[list[Book]] = relationship(back_populates="author")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    books: Mapped[list[Book]] = relationship(
        secondary=book_categories, back_populates="categories"
    )
```

매핑이 그대로 보인다. 하나하나 짚어두자.

- **`DeclarativeBase`** = JPA의 `@MappedSuperclass` + `@Entity`의 토대. 우리 도메인 클래스들이 다 이걸 상속한다.
- **`Mapped[int]` + `mapped_column(primary_key=True)`** = `@Id @GeneratedValue` + `@Column`. 타입 힌트가 nullable 정보까지 같이 전달한다 — `Mapped[int]`면 NOT NULL, `Mapped[int | None]`이면 NULL 가능.
- **`relationship(back_populates=...)`** = `@OneToMany(mappedBy=...)` + `@ManyToOne`의 양방향 표시. JPA처럼 *한쪽이 owning side*다 — `ForeignKey`를 가진 쪽이 그 자리.
- **`Table(..., secondary=...)`** = `@ManyToMany` + `@JoinTable`. 별도 클래스가 아니라 `Table` 객체로 정의하는 게 SQLAlchemy 식이다. 조인 테이블에 추가 컬럼(예: `added_at`)이 필요하면 그때는 별도 클래스로 승격한다.

JPA보다 코드 라인이 살짝 짧다는 느낌이 들 것이다. 어노테이션이 데코레이터로 빠지지 않고, 컬럼 타입이 타입 힌트와 합쳐졌기 때문이다. *타입 힌트가 곧 메타데이터*인 SQLAlchemy 2.0의 설계는 우리가 3장에서 본 Pydantic의 그것과 같은 정신적 모양이다 — 한 번 익히면 머리에 좋다.

### 엔진과 세션 — `SessionFactory` 자리에 `sessionmaker`

JPA에서는 보통 `EntityManagerFactory`(Spring이 만들어 줌)와 `EntityManager`(트랜잭션마다 새로)로 나뉜다. SQLAlchemy는 거의 같은 그림이다.

```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(
    "postgresql+psycopg://app:secret@localhost:5432/library",
    echo=False,           # True로 두면 SQL이 stdout에 찍힘 — 개발 시 유용
    pool_pre_ping=True,   # 죽은 커넥션 자동 재연결
)

SessionLocal = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)
```

- **`engine`** = `DataSource`. 커넥션 풀을 안에 품고 있다. 앱 한 개당 하나만 만든다.
- **`sessionmaker(...)`** = `EntityManagerFactory`. 호출하면 새 `Session`이 나온다.
- **`expire_on_commit=False`** = 이걸 잊지 말자. 기본값 `True`면 commit 직후 *모든 객체의 속성이 expire*되어서, 직후에 `book.title`을 읽으면 다시 SELECT가 일어난다. FastAPI에서는 응답 직렬화 시점에 commit 이후 객체를 다시 읽는 일이 흔해서, 잘못 두면 `DetachedInstanceError`가 폭발한다. 끔찍한 일이다.

엔진과 세션은 어디에 둘까. 답은 4장에서 잡아둔 `Depends()` 자리다. `yield` 의존성으로 한 요청 동안 살아 있다가 `finally`에서 닫히는 그 패턴 그대로다.

```python
# app/db/deps.py
from typing import Annotated, Iterator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 타입 별칭 — 4장에서 익힌 패턴
DbSession = Annotated[Session, Depends(get_db)]
```

이제 라우트는 이렇게 쓴다.

```python
@router.get("/books/{book_id}")
def get_book(book_id: int, db: DbSession):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
```

JPA에서 `EntityManager`를 `@PersistenceContext`로 주입받는 그 코드와 정신적 모양이 같다. 마법이 한 겹 벗겨졌을 뿐이다.

여기서 한 번 주의해 두자. **`finally` 절에서 `commit`을 하지 말자.** 무슨 말인가? FastAPI 튜토리얼 중에는 `try: yield db; db.commit(); except: db.rollback(); finally: db.close()` 같은 코드가 돌아다닌다. 이게 함정이다. `yield db` 다음 줄은 *경로 함수가 끝나고 응답이 클라이언트로 나간 뒤에* 실행된다. 그때 발생한 예외는 응답에 영향을 주지 않지만, 트랜잭션은 실패한 상태로 끝난다. 디버깅 호흡이 진짜 번거롭다.

FastAPI GitHub의 요청-스코프 트랜잭션 토론도 같은 함정을 한 줄로 짚는다 — *의존성의 finally 절에서 commit을 할 수 없다*고. 그 코드는 경로 함수가 끝나고 결과가 클라이언트에 반환된 뒤에 실행되기 때문이다.

권장 패턴은 단순하다. `get_db`는 세션을 열고 닫기만 하고, *트랜잭션 경계는 라우트 또는 서비스 레이어에서 명시*한다. 자세한 모양은 6장에서 본격적으로 다룬다. 이 장에선 우선 `with db.begin():` 한 줄을 손에 익혀두자.

```python
@router.post("/books", status_code=201)
def create_book(payload: BookCreate, db: DbSession):
    with db.begin():       # 트랜잭션 명시
        book = Book(**payload.model_dump())
        db.add(book)
    db.refresh(book)       # commit 뒤 ID 등을 다시 채우려면 필요
    return BookRead.model_validate(book)
```

## 쿼리 — JPQL 출신 손에 익혀둘 핵심 세 개

망라 대신 *손에 익을 핵심 셋*만 짚자. 도서 카탈로그에서 자주 쓰게 될 모양이다.

### 1) 단순 조회 — `where` + `order_by` + 페이징

```python
from sqlalchemy import select

def list_books(db: Session, q: str | None, limit: int, offset: int) -> list[Book]:
    stmt = select(Book)
    if q:
        stmt = stmt.where(Book.title.ilike(f"%{q}%"))
    stmt = stmt.order_by(Book.title.asc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())
```

JPQL의 `select b from Book b where ...`과 비교해 보면 *문자열이 아니라 객체로 쿼리*를 만든다는 점이 결정적 차이다. 컬럼 이름 오타를 IDE가 잡아준다. `Book.titel`이라 잘못 적으면 빨간 줄이 뜬다 — JPQL에선 런타임에야 알게 되던 그 자리다.

### 2) 조인과 `selectinload` — Lazy 함정 회피의 핵심

이게 SQLAlchemy의 가장 중요한 한 패턴이다. 손에 익히자.

```python
from sqlalchemy.orm import selectinload

def list_books_with_author(db: Session) -> list[Book]:
    stmt = (
        select(Book)
        .options(selectinload(Book.author), selectinload(Book.categories))
        .order_by(Book.id)
    )
    return list(db.execute(stmt).scalars().all())
```

`.options(selectinload(...))`는 JPA의 `@EntityGraph` 또는 `fetch join`에 해당한다. 차이가 있다면, SQLAlchemy의 `selectinload`는 *별도의 IN 쿼리*로 관계를 끌어오므로 카타시안 곱 폭발이 없다. 두 번째 쿼리가 한 번 더 나가지만, 결과 행 수가 폭발하지 않는다.

`joinedload`는 *같은 쿼리에 JOIN으로* 끌어온다. *-to-one 관계엔 적합하지만, *-to-many 관계에 쓰면 결과가 행 단위로 부풀어 페이지네이션과 충돌한다. JPA에서 `fetch join`을 `setMaxResults`와 함께 쓰면 경고가 뜨는 그 자리다. 같은 함정이 SQLAlchemy에도 있다 — 이름만 다르다.

손에 익혀 두자. **`-to-many`는 `selectinload`, `-to-one`은 `joinedload`**. 헷갈리면 `selectinload`를 기본으로.

### 3) 집계 — `func.count()` + `group_by`

```python
from sqlalchemy import func

def book_count_by_category(db: Session) -> list[tuple[str, int]]:
    stmt = (
        select(Category.name, func.count(Book.id).label("cnt"))
        .join(Category.books)
        .group_by(Category.name)
        .order_by(func.count(Book.id).desc())
    )
    return list(db.execute(stmt).all())
```

`db.execute(stmt).all()`은 ORM 객체가 아닌 *Row 튜플*을 반환한다. ORM 매핑이 필요 없는 집계엔 이게 자연스럽다. JPA의 `getResultList()`로 `Object[]`가 떨어지는 그 자리다.

이 세 패턴만 손에 익혀도 도서 카탈로그 90%는 짠다. *나머지 10%는 그때 SQLAlchemy 공식 문서를 찾자* — 망라하려고 욕심내는 대신 핵심 회로를 단단히 굳히는 편이 낫다.

## Session = Identity Map + Unit of Work — 미묘하지만 결정적인 차이

JPA의 EntityManager가 1차 캐시(Identity Map)와 dirty checking을 자동으로 해 주듯, SQLAlchemy의 Session도 같은 그림을 갖는다. 한 세션 안에서 같은 PK로 조회한 객체는 *항상 같은 인스턴스*다. 같은 객체에 속성을 바꾸면 commit 시점에 UPDATE가 자동으로 나간다 — 이것도 그대로다.

다만 작은 결이 다르다. 다음 세 가지를 머리에 박아 두자.

**첫째, flush 타이밍.** JPA는 트랜잭션 commit·쿼리 실행 직전에 자동 flush한다. SQLAlchemy도 기본은 같지만(`autoflush=True`), Session의 철학은 *flush를 명시적으로 통제할 수 있어야 한다*는 쪽으로 더 기울어 있다. 그래서 어떤 코드베이스는 `autoflush=False`로 두고 명시적으로 `db.flush()`를 부른다. 처음 접하면 어느 쪽이 맞는지 헷갈리는데, *프로젝트 한 군데로 정해두고 그 안에선 일관되게 가자*. 우리 책 예제는 `autoflush=True`(기본) + 명시적 `with db.begin():` 트랜잭션의 조합이다.

**둘째, dirty checking은 같지만 `expire_on_commit`이 다르다.** JPA에서 commit 후 영속 객체에 접근하면 그냥 값을 반환한다(detach될 때까지). SQLAlchemy는 *기본값이 commit 후 모든 속성 expire*다. 그래서 `session.commit()` 직후 `book.title`을 읽으면 SELECT가 한 번 더 나간다. 응답 직렬화 직전에 commit이 일어나는 FastAPI 패턴과 잘 안 맞는다. 그래서 우리 `SessionLocal`에 `expire_on_commit=False`를 두는 게 표준이다.

**셋째, Lazy loading의 실패 신호가 다르다.** JPA는 `LazyInitializationException`, SQLAlchemy는 `DetachedInstanceError`. 의미는 같다 — *세션이 닫힌 뒤 lazy 관계에 접근했다*. 단, SQLAlchemy의 async 모드에선 이 함정이 더 까다롭다(8장에서 다시). 동기 모드에선 `selectinload`/`joinedload`로 미리 끌어오는 습관 하나로 거의 다 해결된다.

이 세 항목만 머리에 두면 *JPA 사고로 SQLAlchemy를 쓰는* 대부분의 함정은 피한다. 손이 처음엔 불편하지만, 점점 익는다.

## 레포지토리를 직접 짜자 — Spring Data의 마법이 없는 세상

이게 본 장의 가장 큰 *멘탈 적응*이다. JPA를 쓰면서 우리는 거의 코드를 안 썼다.

```kotlin
interface BookRepository : JpaRepository<Book, Long> {
    fun findByTitleContaining(q: String): List<Book>
    fun findByAuthorId(authorId: Long, pageable: Pageable): Page<Book>
}
```

메서드 이름이 곧 쿼리였다. Spring Data가 런타임에 구현을 만들어 줬다. 편했다.

SQLAlchemy 진영엔 이게 없다. 정확히 말하면, *그 마법이 안티패턴*으로 여겨진다. 메서드 이름으로 쿼리를 만드는 자동화는 단순 케이스엔 빛나지만, 조금만 복잡해지면 메서드 이름이 *암호*가 된다. `findByAuthorIdAndCategoriesNameContainingOrderByPublishedAtDesc` 같은 이름을 본 적 있는가? 그게 그 자동화의 끝이다.

대신 우리는 손으로 짠다. 이게 처음엔 끔찍하게 느껴진다 — *내가 또 이걸 적어야 해?* 그러다 깨닫는다. 손으로 적는 쿼리가 *코드 리뷰에 명시적으로 올라오고*, 인덱스가 맞는지 *읽으면서 검증*되고, 페이지네이션·정렬·조인 옵션이 *데이터 모양과 함께 보인다*. 자동화가 가렸던 비용이 코드 표면에 올라오는 셈이다.

표준 모양을 잡자.

```python
# app/books/repository.py
from typing import Iterable
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.books.models import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def list(self, q: str | None, limit: int, offset: int) -> list[Book]:
        stmt = (
            select(Book)
            .options(selectinload(Book.author), selectinload(Book.categories))
            .order_by(Book.title.asc())
            .limit(limit)
            .offset(offset)
        )
        if q:
            stmt = stmt.where(Book.title.ilike(f"%{q}%"))
        return list(self.db.execute(stmt).scalars().all())

    def add(self, book: Book) -> None:
        self.db.add(book)

    def delete(self, book: Book) -> None:
        self.db.delete(book)
```

크지 않다. 4~5개 메서드면 한 도메인의 90%가 끝난다. *원할 때만 메서드를 추가*한다 — 미리 짜두지 말자. JPA처럼 100가지 `findBy...`를 미리 정의해 둘 필요가 없다. 쓸 때 한 줄 추가하는 호흡으로 가자.

서비스 레이어에서 이걸 어떻게 묶는지 보자.

```python
# app/books/service.py
from app.books.repository import BookRepository
from app.books.schemas import BookCreate, BookRead


class BookService:
    def __init__(self, db: Session, books: BookRepository):
        self.db = db
        self.books = books

    def create(self, payload: BookCreate) -> BookRead:
        with self.db.begin():
            book = Book(title=payload.title, author_id=payload.author_id)
            self.books.add(book)
        self.db.refresh(book)
        return BookRead.model_validate(book)
```

서비스가 트랜잭션 경계를 그린다. 레포지토리는 *SELECT/INSERT/DELETE*만 책임진다. 책임이 깔끔하게 나뉜다.

DI는 4장에서 익힌 그대로다.

```python
# app/books/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.books.repository import BookRepository
from app.books.service import BookService


def get_book_repo(db: Annotated[Session, Depends(get_db)]) -> BookRepository:
    return BookRepository(db)


def get_book_service(
    db: Annotated[Session, Depends(get_db)],
    books: Annotated[BookRepository, Depends(get_book_repo)],
) -> BookService:
    return BookService(db, books)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]
```

라우트는 이렇게 짧아진다.

```python
# app/books/router.py
from fastapi import APIRouter

from app.books.deps import BookServiceDep
from app.books.schemas import BookCreate, BookRead

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookRead, status_code=201)
def create_book(payload: BookCreate, service: BookServiceDep):
    return service.create(payload)
```

JPA + Spring Service 코드와 정신적 모양이 거의 같다. 차이는 한 줄 — *컨테이너가 만들어주지 않고 내가 함수로 그래프를 묶는다*. 그게 명시적이다는 말의 실체다.

### Unit of Work — DB 세션을 라우트 끝까지 끌고 다닐 것인가

여기서 한 가지 더 짚어두자. FastAPI 진영엔 *DB 세션을 의존성으로 라우트 끝까지 끌고 다니는 게 안티패턴*이라는 비판이 한 갈래로 자리잡고 있다. 라우트가 길어지면 *요청 내 longtail 트랜잭션*이 생기고, 어디서 commit이 일어났는지 추적이 힘들어진다는 주장이다.

대안은 **Unit of Work 객체**다. 도메인별 레포지토리를 한 묶음으로 들고 있는 컨텍스트 매니저를 만든다.

```python
# app/db/uow.py
from contextlib import contextmanager
from sqlalchemy.orm import Session

from app.books.repository import BookRepository
from app.db.session import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    @contextmanager
    def __call__(self):
        db = self._session_factory()
        try:
            self.books = BookRepository(db)
            # self.authors = AuthorRepository(db) ...
            yield self
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()


def get_uow() -> UnitOfWork:
    return UnitOfWork()
```

라우트는 이렇게 쓴다.

```python
@router.post("/books")
def create_book(
    payload: BookCreate,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow() as u:
        book = Book(**payload.model_dump())
        u.books.add(book)
    return BookRead.model_validate(book)
```

이 패턴은 *트랜잭션 경계가 한 곳에 모이고*, *commit/rollback이 with 블록 끝에 정확히 박힌다*는 장점이 있다. 작은 서비스엔 살짝 과해 보이지만, 도메인이 셋 넘어가면 가치가 빛난다.

이 장의 예제는 *서비스 레이어에서 명시 트랜잭션* 패턴으로 가르친다. UoW는 6장 트랜잭션 챕터의 본격 주제로 다시 만난다. 일단은 *이런 대안이 있다*는 사실만 머리에 넣어두자.

## Alembic — Flyway 자리에 무엇이 들어서는가

Spring Boot에서 마이그레이션은 보통 한 줄로 끝난다. `db/migration/V1__init.sql`을 두면 Flyway가 시작 시 자동으로 돌린다. *프로퍼티 한 줄도 필요 없다*. 우리가 그동안 누리던 자동화의 두께가 여기서도 두꺼웠다.

FastAPI/SQLAlchemy에선 그 동작을 Alembic이 떠맡는다. 차이가 둘 있다. *Flyway는 SQL이 일급*이고, *Alembic은 Python이 일급*이다. 그리고 *Alembic은 자동 시작이 없다* — `alembic upgrade head`를 컨테이너 startup script에 박아야 한다.

설치와 초기화부터 보자.

```bash
$ uv add alembic
$ uv run alembic init alembic
```

생긴 폴더 구조다.

```text
alembic/
├── env.py            # 마이그레이션 실행 환경 설정
├── script.py.mako    # 새 마이그레이션 파일 템플릿
├── versions/         # 실제 마이그레이션 파일들
└── README
alembic.ini           # 설정 파일
```

`alembic.ini`의 `sqlalchemy.url`을 우리 DB URL로 바꾸고, 더 깔끔한 방법으로는 `env.py`에서 환경변수로 읽도록 손본다. 그리고 `env.py`에 우리 모델의 메타데이터를 알려준다.

```python
# alembic/env.py (핵심 부분만)
from app.db.session import Base
from app.books import models  # noqa: F401 — 모든 모델 import 필요

target_metadata = Base.metadata
```

이제 첫 마이그레이션을 자동 생성하자.

```bash
$ uv run alembic revision --autogenerate -m "initial schema"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.autogenerate.compare] Detected added table 'authors'
INFO  [alembic.autogenerate.compare] Detected added table 'books'
INFO  [alembic.autogenerate.compare] Detected added table 'categories'
INFO  [alembic.autogenerate.compare] Detected added table 'book_categories'
  Generating alembic/versions/8f3e2a1b9c4d_initial_schema.py ... done
```

생긴 파일을 열어 보자.

```python
# alembic/versions/8f3e2a1b9c4d_initial_schema.py
"""initial schema

Revision ID: 8f3e2a1b9c4d
Revises:
Create Date: 2026-05-16 10:00:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "8f3e2a1b9c4d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("authors.id"), nullable=False),
    )
    # ... categories, book_categories 생략


def downgrade() -> None:
    op.drop_table("book_categories")
    op.drop_table("books")
    op.drop_table("categories")
    op.drop_table("authors")
```

적용은 한 줄.

```bash
$ uv run alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade  -> 8f3e2a1b9c4d, initial schema
```

여기까지는 Flyway와 정신적 모양이 거의 같다. 한 가지 *주의*가 있다. **`--autogenerate`를 맹신하지 말자.** Alembic의 autogenerate는 우리가 적은 모델 메타데이터와 *현재 DB 스키마*를 비교해 차이를 추론한다. 그런데 다음 변경은 자동으로 잡지 못하거나 잘못 잡는다.

- 컬럼 이름 변경 → autogenerate는 "기존 컬럼 drop + 새 컬럼 add"로 인식한다. 데이터 손실.
- 컬럼 타입의 미묘한 변경(예: `VARCHAR(50)` → `VARCHAR(100)`) → DB 방언별 결과가 다르다.
- 인덱스·제약조건의 이름 — 자동 생성된 이름과 실제 DB의 이름이 다르면 *불필요한 drop/recreate*가 나온다.

그래서 *생성된 파일은 반드시 사람이 한 번 읽고 보정한다*. 이건 Flyway에서 SQL을 직접 쓰던 그 자리와 같다 — 다만 첫 90%를 도구가 만들어주는 차이가 있다.

> Alembic은 SQLAlchemy 메타데이터를 직접 읽기 때문에 Java 진영의 Flyway와는 한 단계 더 단단히 묶여 있다. Flyway가 SQL을 *별도 언어*로 다루는 데 비해, Alembic은 *Python 함수*로 다룬다. 마이그레이션 안에서 일반 Python 코드를 돌려 데이터 마이그레이션을 끼우기도 쉽다.

## by-feature 폴더 구조 — 이 책 전체를 관통할 약속

한 그림을 마지막으로 박아두자. **모든 작은 예제**가 따라가는 폴더 구조의 표준이다. 새 도메인이 등장하는 4·6·7·9·10장 어디에서나 우리는 이 모양을 반복한다. 12장의 통합 프로젝트는 이걸 *이미 안다고 가정*한다.

```text
app/
├── main.py              # FastAPI 진입점, 라우터 등록
├── core/
│   ├── config.py        # pydantic-settings 기반 설정 (7장에서 본격 도입)
│   └── security.py      # 비밀번호 해싱, JWT 도구 (7장)
├── db/
│   ├── session.py       # engine + SessionLocal
│   ├── base.py          # DeclarativeBase
│   ├── deps.py          # get_db
│   └── uow.py           # 선택: Unit of Work
├── books/               # ← 한 도메인 = 한 폴더
│   ├── __init__.py
│   ├── models.py        # SQLAlchemy entity
│   ├── schemas.py       # Pydantic DTO
│   ├── repository.py    # 데이터 접근
│   ├── service.py       # 비즈니스 로직 + 트랜잭션 경계
│   ├── router.py        # FastAPI 라우트
│   └── deps.py          # 이 도메인 전용 Depends 헬퍼
├── authors/
│   └── (같은 구조)
└── tests/
    ├── books/
    └── authors/
```

이게 우리가 *Spring 출신*에게 가장 자연스럽다고 본 모양이다. Java 패키지 구조와 한 줄로 매핑된다.

| Spring 패키지 | FastAPI 모듈 |
|---|---|
| `com.foo.books.controller` | `app.books.router` |
| `com.foo.books.dto` | `app.books.schemas` |
| `com.foo.books.domain` | `app.books.models` |
| `com.foo.books.repository` | `app.books.repository` |
| `com.foo.books.service` | `app.books.service` |

매핑이 1:1로 떨어진다. Spring 프로젝트의 `com.foo.{도메인}.{layer}` 패키지 구조를 *언어를 갈아 끼우고 그대로 가져온* 모양이다.

> "FastAPI에서는 'feature/domain 별 그룹핑'이 잘 동작한다. 'by feature'는 웹 API에 잘 맞는다."

다른 후보로 *layer-first*(`controllers/`, `services/`, `repositories/` 폴더로 묶기) 구조도 있다. Spring 진영에서도 두 갈래가 있다. 그런데 도메인이 셋 넘어가면 *feature-first*가 훨씬 단단하다 — 한 도메인을 통째로 옮기거나, 한 도메인을 마이크로서비스로 떼어내거나, 한 도메인만 신규 입사자에게 맡기기가 쉽다. 우리 책은 feature-first를 표준으로 박는다.

손에 익혀 두자. 새 도메인을 추가할 때마다 이 6개 파일(`models.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`, `deps.py`)을 *복사해 채우는* 호흡이다. 이 호흡이 머리에 박히면, 책이 끝난 뒤 본인 프로젝트에 그대로 옮겨갈 수 있다.

## 한 호흡으로 정리

정리해야 할 패턴이 많은 자리다. 한 번에 정리해 두자.

- **모델 정의**는 `DeclarativeBase` + `Mapped[...]` + `relationship`의 삼총사. JPA `@Entity` + `@Column` + `@ManyToOne`의 평행 구도.
- **세션**은 `SessionLocal` → `get_db` → `yield` 패턴. `expire_on_commit=False`는 잊지 말자.
- **쿼리**는 `select(...).where(...).order_by(...)`로 시작한다. 손에 익힐 핵심은 셋 — `where`+페이징, `selectinload` 옵션, `func.count()` 집계.
- **Lazy 함정**: `DetachedInstanceError`는 `selectinload`/`joinedload`로 사전 차단하자. `-to-many`는 `selectinload`, `-to-one`은 `joinedload`.
- **레포지토리**는 손으로 짠다. Spring Data의 자동화는 없다. 그게 결국 *코드 표면에 비용이 올라오는* 깔끔함을 준다.
- **Unit of Work**는 도메인이 셋 넘어갈 때부터 검토하자. 5장은 서비스 레이어 명시 트랜잭션으로 충분.
- **Alembic**은 Flyway의 자리. autogenerate를 맹신하지 말고 *생성된 파일을 사람이 한 번 읽는다*.
- **폴더 구조**는 `app/{도메인}/{models|schemas|repository|service|router|deps}.py`의 by-feature 6종 세트. 책 끝까지 이 약속을 반복한다.

여기까지 오면 한 가지 감각이 든다. *JPA가 어노테이션 뒤에 숨겨두던 일을 SQLAlchemy는 코드 위로 다 올려둔다*. 그 차이가 답답하다가, 어느 순간 안심으로 바뀐다. *내가 무슨 쿼리를 짜는지 내가 본다*는 안심이다.

다음 장이 책 전체의 hinge다. `@Transactional` 한 줄이 없는 자리에서, 우리는 트랜잭션 경계를 어디에 어떻게 그릴지 본격적으로 결정해야 한다. 본 장에서 `with db.begin():` 한 줄을 손에 익혔으면, 다음 장에서 우리는 그 한 줄을 *어디에 둘 것인가*라는 더 큰 질문 앞에 선다.
