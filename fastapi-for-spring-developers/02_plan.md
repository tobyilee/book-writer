# FastAPI for Spring Developers 저술 계획

## 제목 후보

1. **Spring 개발자를 위한 FastAPI** — 부제: *@Autowired에서 Depends까지, JVM 사고로 Python 백엔드를 짓는 법*
   - 톤: 정공법, 입문서. 안전한 선택.
   - 포지셔닝: 서점 매대에서 Spring 개발자가 보자마자 "내 책이다"라고 알아챈다. 검색 SEO도 좋다.
   - 약점: 다소 평범하다. 호기심을 자극하지 않는다.

2. **@Transactional이 없는 세상** — 부제 후보 3종:
   - (a) *Spring 사고로 FastAPI를 짓는 법* — 정공법, "버리지 않고 짓는다"의 뉘앙스 (추천)
   - (b) *@Autowired 출신이 Depends()와 만나는 시간* — 인물 중심, 여정의 호흡
   - (c) *Spring 출신 백엔드가 FastAPI로 옮길 때 배우는 것들* — 마이그레이션 톤 (원안, 약점: "옮긴다"가 마이그레이션 책처럼 읽힘)
   - 톤: 도발적, 에세이형 기술서.
   - 포지셔닝: Spring 개발자가 가장 공감하는 통증("자동 트랜잭션이 없다고?")을 제목으로 박는다. 책을 펴게 만드는 힘이 강하다. 본문도 같은 호흡으로 갈 수 있다.
   - 약점: 트랜잭션만 다루는 책처럼 오해될 수 있어 부제로 균형을 잡아야 한다.

3. **두 번째 백엔드 언어, FastAPI** — 부제: *Spring에서 출발해 Python으로 영역을 넓히는 개발자를 위한 안내서*
   - 톤: 차분한 가이드, 멘토 같은 어조.
   - 포지셔닝: "Spring을 버리는 책이 아니다, 둘 다 쓰는 사람을 위한 책이다"라는 메시지가 강하다. 한국 시장에서 "Spring은 메인이고 FastAPI는 보조"인 현실에 정직하게 맞춘다.
   - 약점: 다소 신중한 톤이라 임팩트가 약하다.

**추천: 2번 — "@Transactional이 없는 세상" × 부제 (a) "Spring 사고로 FastAPI를 짓는 법"**

이유: 본 책의 핵심 가치 명제가 "Spring 사고방식의 어느 부분이 무너지고, 무엇으로 대체되는가"이기 때문이다. 리서치에서 가장 강한 시그널이 "트랜잭션·DI·보안 자동화의 부재"였고, 한국 velog 후기들도 같은 톤이다. 제목이 곧 책의 약속이다. 부제 (a)는 "옮긴다"가 아니라 "짓는다"를 택해, 본 책의 진짜 포지셔닝 — "Spring을 버리는 책이 아니라 Spring 사고를 끌고 와서 FastAPI를 짓는 책"(3번 후보의 메시지) — 을 도발적 제목 아래 정확히 박는다. Toby 문체의 평어체·청유형과도 잘 어울린다 — "없는 세상에서 살아보자"라는 청유형 호흡이 본문 전반에 흐를 수 있다.

---

## 책 특성

- **장르**: 에세이형 기술서 (실용 비교서). 단순 튜토리얼이 아니라 "Spring 사고와의 충돌·전환"이 통주저음으로 흐른다.
- **분량**: 약 380~430페이지 (한글 본문 기준, 약 18~22만 자). 챕터당 평균 17,000~21,000자.
- **난이도**: Spring 경력자 기준 입문~중급. Python 자체는 기초만 가정(if/for/list/dict 수준). FastAPI는 처음으로 가정. SQLAlchemy·Pydantic도 처음으로 가정.
- **독자 여정**:
  - **진입 상태**: "Python 백엔드를 한번 써봐야 한다는데 막막하다. @Autowired·@Transactional·@RestController가 머리에 박혀 있고, FastAPI 튜토리얼을 봐도 '그래서 트랜잭션은 어떻게 걸지?'에서 막힌다. Spring 사고를 그대로 끌고 와도 되나?"
  - **출구 상태**: "FastAPI로 프로덕션급 API를 한 권의 책 호흡 안에서 만들 수 있다. Spring과 다르게 동작하는 지점(트랜잭션·DI 스코프·async·보안)을 알고, 어떤 경우에 FastAPI를 고르고 어떤 경우에 Spring으로 돌아갈지 판단할 수 있다. Python의 동적 본성과 어떻게 공존할지 안다."

---

## 내러티브 아크

이 책은 Spring 출신 독자의 인지 부담을 의도적으로 분산시킨다. 한꺼번에 "Python·FastAPI·SQLAlchemy·async"를 들이부으면 누구나 익사한다. 그래서 아크는 세 막으로 짠다.

**1막: 친숙함의 다리 (1~3장)** — 먼저 "여기, 너의 사고와 비슷한 것들이 있다"를 보여준다. 정체성 지도(1장), 환경 셋업(2장), 첫 라우트(3장). Spring과 1:1로 그려지는 부분만 골라 손을 잡아 끈다. 이 막의 목적은 *불안 해소*다. 독자가 "어, 이거 익숙하네"라고 느끼게 만든다.

**2막: 충돌과 전환 (4~8장)** — 이제 Spring 사고가 더는 통하지 않는 영역으로 한 발씩 데려간다. 의존성 주입의 스코프 차이(4장)로 워밍업한 뒤, SQLAlchemy의 Session·UoW(5장)에서 첫 충격을 준다. 그 충격이 6장의 트랜잭션 — `@Transactional`이 없는 세상 — 에서 절정에 이른다. 7장의 보안과 8장의 비동기·GIL은 두 번째·세 번째 충돌이다. 이 막에서 독자의 사고 모델이 재구성된다. *깨달음*의 막이다.

**왜 6→7→8인가 (7장이 6장 직후인 이유)**: 한 가지 통주저음이 6·7장을 잇는다 — **명시성**이다. 6장이 가르치는 건 "`@Transactional`이 자동으로 해주던 일을 너의 손으로 명시한다"이고, 7장이 가르치는 건 "Spring Security가 자동으로 막아주던 일을 너의 손으로 명시한다"이다. 같은 인지 운동이 연속으로 흐른다 — 자동에서 명시로의 전환. 6장에서 트랜잭션 경계를 직접 그리는 손에 익은 감각이, 7장에서 보호 라우트마다 `Depends(get_current_user)`를 명시하는 손에 그대로 이어진다. 반대로 6장 직후에 8장(async)을 끼우면 인지의 축이 한 번 꺾인다(명시성 → 동시성 모델). 8장은 7장(인증 토큰 검증, 외부 IDP 호출의 async 시나리오)까지 다 본 뒤 마지막 충돌로 두는 게 호흡상 자연스럽다. 또한 7장은 reference §2.8 기준 "리소스 서버 패턴"이라 DB·트랜잭션 의존이 약해, 6장에서 막 트랜잭션을 익힌 독자의 두뇌에 무리한 짐을 지우지 않는다.

**3막: 운영과 통합 (9~11장)** — 사고 모델이 정리됐으면 이제 실전이다. 예외/관측성(9장), 테스트(10장), 배포(11장). Spring Actuator·MockMvc·Tomcat의 빈자리를 무엇으로 메우는지 보여준다. 작은 실행 코드들이 12장의 미니 통합 프로젝트에 모인다.

**에필로그 격 마지막 장**: 13장은 "언제 Spring으로 돌아가야 하는가" — 한국 케이스 포함. 정직한 한계 인정이 책의 신뢰를 마무리한다.

이 순서의 장점:
- 충격을 1막 끝까지 유예 → 독자가 책을 덮지 않는다.
- 트랜잭션을 책 한가운데(6장) 두어 hinge 역할을 시키되, 그 전에 5장(SQLAlchemy)에서 충분히 깔아둔다.
- async를 후반(8장)에 둔 이유: 1~7장에서 sync 모드로 충분히 책을 끌고 갈 수 있고, async는 "선택적 가속"으로 가르치는 게 안전하다. (리서치 § 4.1: async가 항상 빠른 게 아니라는 사실 자체가 한 챕터의 주제다.)
- 12장의 미니 프로젝트는 1~11장 지식을 한 번에 통합한다. 챕터별 작은 예제는 각 챕터에서 끝내고, 12장은 별도 도메인으로 다시 짓는다 (중복 학습 회피, 통합 사고 검증).

---

## 통합 미니 프로젝트의 형태 (다양한 예제 요구 처리 방식)

**선택안: "사내 태스크 관리 API + Slack 알림 봇"**

이유:
- Spring 출신이 가장 자주 만드는 도메인(태스크·티켓·이슈)이라 비즈니스 로직 학습 부담이 0이다. 책의 학습 곡선이 FastAPI 자체에 집중된다.
- 인증(JWT)·DB(태스크/사용자/댓글)·async(Slack webhook 호출)·백그라운드(알림 큐)·SSE(실시간 업데이트)를 *자연스럽게* 다 끌어들일 수 있다. 억지 통합이 안 생긴다.
- 12장의 통합 프로젝트로 빌드하지만, 챕터별 작은 예제는 다른 도메인을 쓴다 — 3장: 간단한 환율 변환 API, 4장: 사용자 조회 API, 5장: 도서 카탈로그 CRUD, 6장: 송금 트랜잭션 시나리오, 7장: 로그인 토큰 발급, 8장: 외부 ML API 비동기 프록시, 9장: 에러 핸들러 데모, 10장: 위 모든 것을 테스트하는 픽스처, 11장: Docker로 띄우기. **다양성 + 12장의 통합**의 두 축이다.

대안 비교 (선택 안 한 이유):
- "ML 모델 서빙 API" — FastAPI의 sweet spot이지만 Spring 출신에게 "비즈니스 백엔드도 FastAPI로 되는가"라는 질문이 더 중요하다. ML 서빙은 13장 한 절로만 다룬다.
- "게시판 API" — 너무 평범하고 인증·비동기 통합 동기가 약하다.
- "결제 시스템" — 트랜잭션·보안 시연에는 좋지만, 외부 결제 게이트웨이 의존성이 책 학습을 산만하게 한다.

---

## 챕터 목록

### 1장. 왜 FastAPI, 왜 Spring 출신에게 친숙한가

- **핵심 질문**:
  1. Spring을 쓰던 내가 왜 FastAPI를 배워야 하는가?
  2. FastAPI는 Spring의 무엇과 닮았고, 무엇이 결정적으로 다른가?
  3. Spring을 떠나면서 무엇을 잃는가 (정직한 약점 인식)?
- **주요 내용**:
  - FastAPI의 정체성 — Starlette + Pydantic + uvicorn의 얇은 조합 (Spring MVC + Jackson + Tomcat의 평행 구도)
  - 한눈 매핑표: 24개 항목 (`@RestController` ↔ `@app.get` 등). 책의 지도 역할.
  - "타입 힌트가 곧 검증·직렬화·문서의 단일 소스"라는 한 줄의 의미
  - **정직한 약점 인식 절**: 트랜잭션·보안 자동화 부재(이 책 6·7장의 동기), 메모리 누수의 조용한 성장("180MB → 며칠 사이 600MB" Medium 6개월 비교 사례 직접 인용 — 11장 본문에서 도구 제시), 운영 비용 차이(480시간 vs 160시간의 한 사례 인용). reference §3.2의 약점을 책의 약속과 정렬해 깐다.
  - 한국 시장의 현실: Spring이 메인, FastAPI는 보조라는 진실. 그래도 왜 배워야 하는가
  - 책의 약속: 이 책이 다루는 것과 다루지 않는 것
- **예제 소재**: Hello World 수준의 `@app.get("/")` 한 줄과 `@RestController` 한 클래스의 시각적 대비
- **독자가 얻는 것**: 책 전체를 관통하는 매핑 지도 + 학습 부담의 윤곽 + 정직한 약점 지도
- **예상 분량**: 약 15,000자 (~30페이지)

### 2장. 개발 환경 — Maven/Gradle 마인드에서 uv·Poetry로

- **핵심 질문**:
  1. Python 프로젝트 셋업이 왜 Java보다 더 혼란스러운가? 무엇을 표준으로 골라야 하는가?
  2. IDE·린트·타입 체커는 어떻게 IntelliJ급 안전망을 만드는가?
- **주요 내용**:
  - Python 가상환경 개념 — JVM 클래스패스와의 비교
  - uv를 기본으로 선택하는 이유 (Poetry 100배, requirements.txt는 deprecated)
  - `pyproject.toml`의 구조와 Maven `pom.xml` 매핑
  - PyCharm / VSCode 설정, mypy/pyright/ruff/black 세팅
  - 첫 FastAPI 프로젝트 스캐폴드 — `uv init`, `uv add fastapi uvicorn`, 첫 실행
- **예제 소재**: 새 프로젝트 폴더 만들기. `uv run uvicorn app.main:app --reload`로 첫 실행 + `/docs` 자동 생성 확인.
- **독자가 얻는 것**: 손에 익은 Spring Boot Initializr 같은 빠른 셋업 루틴
- **예상 분량**: 약 13,000자 (~26페이지)

### 3장. 첫 라우트와 Pydantic — `@RestController` × DTO를 한 줄에 녹이기

- **핵심 질문**:
  1. `@RestController` + `@RequestBody UserDto` + `@Valid`의 삼중주가 FastAPI에선 어떻게 한 함수로 합쳐지는가?
  2. Pydantic 모델은 Jackson과 어떻게 다르고, 무엇을 더 해주는가?
- **주요 내용**:
  - FastAPI의 데코레이터 라우팅 — 함수 단위 라우트의 의미. "한 함수로 합치기"의 *체감*에 본문 무게를 둔다.
  - Pydantic v2 모델 정의 — `BaseModel`, `Field`, 핵심 `field_validator` 한 개. (디테일은 부록 또는 책 끝 레퍼런스 표로)
  - 요청·응답을 같은 모델로 쓰는 위험과 분리 패턴 (`UserCreate` / `UserRead` / `UserInDB`)
  - 자동 OpenAPI/Swagger UI — Spring `springdoc-openapi`와의 차이
  - **이동된 항목**: Query/Path/Body/Header 파라미터의 세부 표는 부록 A로 이동(본문에선 환율 API 예제에 자연스럽게 나타나는 것만 짧게 짚는다). APIRouter 본격 사용은 4장 끝 짧은 절 + 12장 통합 프로젝트로 이동.
- **예제 소재**: 환율 변환 API (`/convert?from=USD&to=KRW&amount=100`). 입력 검증, 응답 모델, OpenAPI 자동 문서까지 한 챕터 안에서 완성.
- **독자가 얻는 것**: 첫 "이건 진짜 Spring보다 짧다"의 체감
- **예상 분량**: 약 16,000자 (~32페이지) — 원안 19k에서 3k 다이어트. 이유: Spring 사고가 채 정착되기 전에 Pydantic 디테일·라우팅 세부·APIRouter까지 다 들이부으면 1막의 *불안 해소*가 깨진다. 본 챕터는 "한 함수의 체감"에 집중.

### 4장. 의존성 주입 — `@Autowired`에서 `Depends()`로

- **핵심 질문**:
  1. Spring의 싱글톤 빈 세계와 FastAPI의 함수-파라미터-DI 세계는 무엇이 같고 무엇이 다른가?
  2. 요청-스코프가 기본값이라는 사실이 코드를 어떻게 바꾸는가?
- **주요 내용**:
  - `Depends()` 기본 — 함수 파라미터의 마커가 어떻게 빈 그래프 역할을 하는가
  - 중첩 의존성 — Spring의 `@Component` 그래프와의 평행 구조
  - 요청-스코프 캐시 (한 요청에서 같은 의존성은 한 번만 실행)
  - 싱글톤이 필요할 때 — `lifespan` 컨텍스트, 모듈 상수, `@lru_cache`
  - `yield` 의존성 — 트랜잭션·세션 같은 라이프사이클 자원을 finally까지 끌고 가는 패턴
  - `Annotated[X, Depends(get_x)]` 타입 별칭 패턴 — 코드 길어짐 회피
  - 테스트 오버라이드 — `app.dependency_overrides[get_db] = lambda: fake_db` 한 줄의 위력
  - **APIRouter로 라우트 그룹화 (짧은 절)** — Spring의 `@RequestMapping` 클래스 prefix와 1:1 매핑. 본격 사용은 12장. 여기서는 "한 도메인의 라우트를 한 파일에 묶는 방법"만 시연.
  - **미들웨어와 횡단관심자** — Spring `Filter`/`Interceptor`/`@Aspect` 3중주가 FastAPI에선 ASGI 미들웨어 + 의존성으로 어떻게 나뉘는가 (reference §2.5). AOP는 없다 — 이 사실 자체가 가르침. 요청 ID 미들웨어를 한 절에서 소개하고, 본격 활용은 9장(관측성)에서.
- **예제 소재**: 사용자 조회 API. `UserRepository`, `UserService`를 명시적으로 짜서 Spring의 자동 주입과 무엇이 다른지 시연. APIRouter로 `/users/*` 묶기. 요청 ID 미들웨어 한 개. 마지막에 같은 코드의 테스트에서 의존성 한 줄 갈아 끼우기.
- **독자가 얻는 것**: Spring DI에 익숙한 사고를 FastAPI 패턴으로 1:1 번역하는 회로 + 횡단관심사를 어디에 둘지의 감각
- **예상 분량**: 약 21,000자 (~42페이지) — 원안 20k에서 1k 증가. APIRouter + 미들웨어 절 흡수.

### 5장. 데이터 접근 — JPA에서 SQLAlchemy 2.0으로

- **핵심 질문**:
  1. Hibernate의 Session·1차 캐시·Lazy loading이 SQLAlchemy에선 어떻게 대응되는가?
  2. Spring Data JPA의 메서드 이름 magic 없이 어떻게 깔끔한 레포지토리를 짜는가?
  3. 도메인이 둘 셋 늘어나면 폴더는 어떻게 짜야 하는가?
- **주요 내용**:
  - SQLAlchemy 2.0 모델 정의 — `DeclarativeBase`, `Mapped[...]`, JPA `@Entity`와의 매핑
  - Core expression 쿼리 — JPQL/Criteria API 출신에게 친숙한 점과 다른 점 (핵심 2~3개 패턴만, 망라 X)
  - Session = Identity Map + Unit of Work — JPA EntityManager와의 미묘한 차이
  - Lazy loading의 함정 — `DetachedInstanceError`, JPA `LazyInitializationException`과의 비교
  - 레포지토리 패턴을 직접 짜기 — Spring Data 자동 구현이 없는 세상
  - Alembic 마이그레이션 — Flyway와의 비교, autogenerate의 한계
  - **레이어드 아키텍처 — 폴더 구조의 약속 (한 절, 약 1,500자)**: reference §4.3의 by-feature 폴더 구조(`users/router.py, schemas.py, models.py, repository.py, service.py, deps.py`)를 Spring 패키지 구조(`com.foo.users.{controller,dto,domain,repository,service}`)와 매핑. 이 구조를 4·6·7·9·10장의 모든 작은 예제가 따른다고 약속한다. 12장이 이걸 *이미 안다고 가정*할 수 있게.
  - **이동된 항목**: "SQLModel을 왜 권하지 않는가" 비교는 13장의 미래·생태계 절로 이동 (5장의 학습 부담 경감).
- **예제 소재**: 도서 카탈로그 CRUD. `Book`, `Author`, `Category` 엔티티와 관계, `BookRepository` 직접 작성, Alembic으로 첫 마이그레이션. 도메인 폴더 구조로 정리해서 본문에 배치.
- **독자가 얻는 것**: JPA 사고로 SQLAlchemy를 잘못 쓰는 흔한 함정 회피 + 깔끔한 도메인-레포 분리 + 이후 챕터를 관통할 폴더 약속
- **예상 분량**: 약 20,000자 (~40페이지) — 원안 22k에서 2k 다이어트. SQLModel 비교를 13장으로 이동한 결과 + Core 쿼리를 핵심만 추리는 결과. 레이어드 절(+1.5k)을 흡수해도 순감.

### 6장. 트랜잭션 — `@Transactional`이 없는 세상에서 살아남기

- **핵심 질문**:
  1. `@Transactional` 한 줄이 사라진 자리에 무엇을 놓아야 같은 안전성을 얻는가?
  2. 한 요청 안의 트랜잭션 경계를 어디에 그어야 하는가?
- **주요 내용**:
  - 왜 FastAPI/SQLAlchemy는 `@Transactional`을 흉내 내지 않았는가 — 명시성의 철학
  - 흔한 안티패턴: `get_db()` finally에서 commit (응답 나간 뒤 실행되는 함정)
  - 권장 패턴: 라우트/서비스 레이어에서 `async with session.begin():` 명시
  - Unit of Work 패턴 — Matthew Brown 블로그의 비판과 대안
  - 격리 수준, 롤백, savepoint — Spring `@Transactional(isolation=...)`과의 대응
  - 트랜잭션과 예외의 관계 — Spring의 unchecked 자동 롤백 vs SQLAlchemy의 명시적 처리
  - 테스트에서의 트랜잭션 (Spring은 자동 롤백, FastAPI는 직접)
- **예제 소재**: 송금 시나리오. 두 계좌 간 amount 이동, 잔액 부족 예외, 부분 실패 시 롤백 보장. Spring `@Transactional`로 짠 의사 코드와 FastAPI 명시 트랜잭션을 양면 페이지로 대조.
- **독자가 얻는 것**: 책 전체에서 가장 큰 인지 전환. 트랜잭션을 어디서 시작하고 닫을지 본능적으로 판단할 수 있게 됨.
- **예상 분량**: 약 21,000자 (~42페이지)

### 7장. 인증·인가 — Spring Security 없이 OAuth2/JWT

- **핵심 질문**:
  1. `@PreAuthorize("hasRole('ADMIN')")` 한 줄의 무게를 무엇으로 대체하는가?
  2. 보안 자동화가 없는 세상에서 누락을 어떻게 막는가?
- **주요 내용**:
  - 리소스 서버 패턴 — FastAPI가 토큰 발급보다 검증에 집중하는 이유
  - `OAuth2PasswordBearer`, `python-jose`/`PyJWT`로 JWT 검증
  - `Depends(get_current_user)` 패턴 — 메서드 어노테이션 대신 함수 파라미터
  - 스코프 기반 RBAC — `Security(..., scopes=["admin"])`가 OpenAPI까지 반영되는 이점
  - 비밀번호 해싱 — `passlib`, `bcrypt`, `argon2` 선택
  - CSRF, 세션 고정 같은 Spring Security가 무료로 막아주던 항목 — 직접 책임지기
  - **환경별 시크릿 — `pydantic-settings`의 도입 (이 책에서 처음 등장)**: Spring `@Value("${...}")` 매핑, `.env`, 검증 가능한 `BaseSettings`. 11장은 이걸 *전제*로 Kubernetes Secret 연동만 다룬다.
- **예제 소재**: 로그인 → JWT 발급 → 보호된 라우트 호출 → 스코프 검증의 전 흐름. `/auth/login`, `/me`, `/admin/users` 세 엔드포인트. JWT 비밀 키를 `pydantic-settings`로 주입.
- **독자가 얻는 것**: Spring Security가 떠받쳐 주던 안전망을 본인이 의식적으로 짜는 감각
- **예상 분량**: 약 19,000자 (~38페이지)

### 8장. 비동기와 GIL — WebFlux 사고를 코루틴으로

- **핵심 질문**:
  1. Spring WebFlux/Reactor를 알던 사람에게 `async/await`는 어떻게 다른가?
  2. 언제 `async def`를 쓰고 언제 `def`로 두는 게 안전한가?
  3. Spring의 `@Async`·`@Scheduled` 자리에는 무엇을 놓는가?
- **주요 내용** (절 단위 구조):
  - **§8.1 모델 비교**: WSGI vs ASGI — Spring MVC vs WebFlux 평행 구도
  - **§8.2 이벤트 루프**: asyncio 이벤트 루프 — Java 스레드풀과의 본질적 차이
  - **§8.3 함정**: "Async가 항상 빠르지 않다" — async + sync DB의 함정 (sync 600 req/s, async + sync 550 req/s)
  - **§8.4 안전 패턴**: 블로킹 함수를 async에서 안전하게 호출하는 법 — `asyncio.to_thread`, `run_in_threadpool` / sync def 라우트의 안전성 — FastAPI가 자동으로 스레드풀에서 실행
  - **§8.5 GIL**: CPU-bound vs I/O-bound 워크로드의 갈림 + free-threaded Python(PEP 703)의 2026 현재 상태
  - **§8.6 Kotlin 코루틴 ↔ Python async (독립 절, 약 2,000자)** — Kotlin 경력자 대상 보강. `suspend fun` ↔ `async def`의 닮음과 다름, structured concurrency 비교, `runBlocking` ↔ `asyncio.run`. reference §9.10이 명시한 한계 영역이라 직접 합성.
  - **§8.7 백그라운드 작업 — `@Async`/`@Scheduled`의 대체 (독립 절, 약 2,500자)** — reference §2.10 본문 흡수. `BackgroundTasks`(fire-and-forget) / APScheduler(in-process 스케줄러) / ARQ(asyncio 친화 분산 큐) / Celery(성숙도) 비교 표 + 어느 시점에 BackgroundTasks를 벗어나야 하는지의 판단 기준. 12장의 Slack webhook 사례가 *이걸 전제로* 가벼운 케이스를 다룬다.
- **예제 소재**: ① 외부 ML 추론 API 비동기 프록시 (동기 vs async 부하 측정, sync DB 섞은 함정 시연) ② 백그라운드 작업 — 이메일 발송 fire-and-forget을 BackgroundTasks로 짠 뒤 부하가 늘면 ARQ로 옮기는 1단계 마이그레이션.
- **독자가 얻는 것**: "async 쓰면 빨라진다"는 단순 신화를 깨고, 언제·왜 async를 쓰는지 판단 기준 + Kotlin 출신 독자의 손에 익은 비교점 + Spring `@Async`/`@Scheduled` 자리에 무엇을 놓을지의 의사결정
- **예상 분량**: 약 23,000자 (~46페이지) — 원안 20k에서 3k 증가. Kotlin 절(+2k) + 백그라운드 절(+2.5k) 흡수, 일부 중복 정리로 -1.5k.

### 9장. 예외·로깅·관측성 — Actuator 없이

- **핵심 질문**:
  1. `@ControllerAdvice`의 전역 핸들러를 FastAPI에선 어떻게 구성하는가?
  2. `spring-boot-starter-actuator` 한 줄의 마법을 무엇으로 대체하는가?
- **주요 내용**:
  - `@app.exception_handler` — Spring `@ControllerAdvice`와 거의 1:1
  - 도메인 예외 계층 — `DomainNotFound`, `BusinessRuleViolation` 같은 의미적 예외
  - 전역 캐치올 핸들러 + Sentry 연동 — try/except 도배 회피
  - 구조화 로깅 — `structlog` + ContextVar로 Spring MDC 흉내내기
  - 요청 ID 미들웨어 — 분산 추적의 첫걸음
  - Prometheus 메트릭 — `prometheus-fastapi-instrumentator` 한 줄
  - OpenTelemetry 트레이싱 — `FastAPIInstrumentor.instrument_app(app)`
  - health/readiness 엔드포인트 — Spring Actuator `/actuator/health`의 수제 버전
  - Pyctuator로 Spring Boot Admin과 연동 (사내 환경 통합 옵션)
- **예제 소재**: **주문 API의 도메인 예외 계층** (`OrderNotFound`, `InsufficientStock`, `PaymentDeclined`, `IdempotencyConflict`, `RateLimitExceeded` — 5가지 실패 모드). 도메인 예외 → `@app.exception_handler` 매핑 → 캐치올 → 요청 ID 미들웨어(4장에서 도입한 것 재사용) → Prometheus 메트릭(주문 상태별 카운터) → `/healthz`까지 한 도메인 안에서 점진적으로 쌓아 올리기. 다른 챕터(환율/도서/송금/JWT)와 톤 일치.
- **독자가 얻는 것**: Spring Actuator가 자동으로 해주던 것을 직접 조립할 수 있는 능력
- **예상 분량**: 약 18,000자 (~36페이지)

### 10장. 테스트 — MockMvc에서 TestClient + pytest로

- **핵심 질문**:
  1. `@SpringBootTest` + `@MockBean` 조합을 무엇으로 옮기는가?
  2. Testcontainers를 Python에서도 그대로 쓸 수 있는가?
- **주요 내용**:
  - pytest 기초 — JUnit 5와의 평행 비교 (`@fixture` ↔ `@BeforeEach`, parametrize ↔ `@ParameterizedTest`)
  - TestClient(app) — Starlette 기반의 HTTP 테스트 (Spring MockMvc와의 비교)
  - 의존성 오버라이드 — `app.dependency_overrides`로 mock 주입
  - 비동기 테스트 — `pytest-asyncio` + `httpx.AsyncClient`
  - Testcontainers Python — Spring 진영과 거의 똑같이 PostgreSQL/Redis 컨테이너 띄우기
  - 트랜잭션 자동 롤백이 없는 세상의 fixture 전략 — savepoint, truncate, schema-per-test
  - 픽스처 스코프 — Spring `@DirtiesContext`와의 매핑
  - 계약 테스트(consumer-driven) 한 절 — Spring Cloud Contract 출신 독자 위로
- **예제 소재**: 1~9장에서 만든 작은 API들을 통합 테스트로 묶기. 환율 API + 사용자 API + 도서 CRUD + 송금 + JWT 인증 + 비동기 프록시를 pytest로 검증. Testcontainers로 실제 PostgreSQL 띄우기.
- **독자가 얻는 것**: Spring 테스트 자산(MockMvc, Testcontainers, `@MockBean`)을 잃지 않고 옮기는 자신감
- **예상 분량**: 약 19,000자 (~38페이지)

### 11장. 배포·운영 — Tomcat에서 Uvicorn + Gunicorn + 컨테이너로

- **핵심 질문**:
  1. JAR 한 개 띄우는 단순함이 사라진 자리에 무엇을 놓는가?
  2. 워커 수, 메모리, 컨테이너 전략은 어떻게 잡는가?
- **주요 내용**:
  - Uvicorn 단독 vs Gunicorn + Uvicorn worker — Tomcat의 스레드풀 vs 멀티 프로세스
  - 워커 수 공식 — sync `(2 × CPU) + 1`, async uvicorn은 CPU 수
  - Kubernetes에선 컨테이너당 단일 프로세스 권장 (replica가 워커 역할)
  - Dockerfile 패턴 — multi-stage, `uv sync --frozen`, non-root 유저
  - 그레이스풀 셧다운 — `lifespan` 컨텍스트, signal handling
  - **시크릿 관리 — Kubernetes Secret 연동만**: pydantic-settings 자체는 7장에서 도입했다고 가정. 여기서는 K8s Secret/ConfigMap → 환경 변수 → BaseSettings 파이프라인만 다룬다.
  - **메모리 누수 모니터링 (사례 직접 인용)**: 1장에서 예고한 "180MB → 며칠 사이 600MB" Medium 6개월 비교 사례를 본문에서 풀어 *왜* 이 도구들이 필요한지 정렬한 뒤 — JVM 힙덤프의 빈자리에 `tracemalloc`·`memray`·`py-spy`를 어떻게 배치하는지 시연. 사례는 "한 회사의 경험"으로만 인용(일반화 금지).
  - 로드 밸런서 뒤의 X-Forwarded-* 처리 — `--proxy-headers`
  - 헬스 체크, readiness probe 패턴
- **예제 소재**: 1~9장 코드를 Docker로 패키징 → docker-compose로 PostgreSQL과 같이 띄우기 → Kubernetes manifest 예시. CI/CD 파이프라인 스켈레톤(GitHub Actions).
- **독자가 얻는 것**: Spring Boot의 `java -jar` 한 줄에 가까운 표준 배포 루틴
- **예상 분량**: 약 17,000자 (~34페이지)

### 12장. 통합 프로젝트 — 사내 태스크 관리 API + Slack 알림 봇

- **핵심 질문**:
  1. 지금까지 배운 모든 조각이 한 프로덕션 서비스 안에서 어떻게 합쳐지는가?
  2. 도메인 분리, 트랜잭션, 비동기, 보안, 테스트가 한 코드베이스에서 어떻게 공존하는가?
- **주요 내용**:
  - 요구사항 정의 — 사용자, 태스크, 댓글, 알림. Spring 개발자가 가장 친숙한 도메인.
  - 도메인-별 폴더 구조 (`tasks/`, `users/`, `notifications/`)
  - 인증(JWT) + RBAC(`admin`/`member` 스코프)
  - 태스크 상태 변경 트랜잭션 + 도메인 이벤트
  - 댓글 작성 시 Slack webhook 알림 — `BackgroundTasks` + httpx async
  - 알림 큐가 무거워지면 — ARQ로 외부 워커 이전 시점 토론
  - SSE로 실시간 태스크 업데이트 — Spring WebFlux SSE와 비교
  - 통합 테스트 + Docker 배포 + 관측성 — 11장까지 배운 것 전부 활용
  - 코드 리뷰 — Spring 출신이 빠지기 쉬운 함정 체크리스트
- **예제 소재**: 본문 전체가 한 프로젝트. 깃허브 리포 형태로도 산출 가능한 분량.
- **독자가 얻는 것**: 본인의 첫 FastAPI 프로덕션 서비스 템플릿
- **예상 분량**: 약 24,000자 (~48페이지)

### 13장. 언제 Spring으로 돌아가야 하는가

- **핵심 질문**:
  1. FastAPI가 진짜로 안 맞는 경우는 언제인가?
  2. 한국 시장에서 FastAPI의 위치는 어디인가? 커리어상 어떻게 양 다리를 걸치는가?
  3. 책이 끝난 뒤 한국 독자가 흔히 빠지는 인식 함정은 무엇이고, 어떻게 보정하는가?
- **주요 내용** (절 단위):
  - **§13.1 FastAPI가 빛나는 도메인** — ML 서빙, 데이터 플랫폼 내부 API, 빠른 MVP, 사내 어드민
  - **§13.2 FastAPI가 다치는 도메인** — 복잡한 대규모 트랜잭션, 대형 팀의 거대 모놀리스, 엔터프라이즈 인테그레이션(배치/메시징/규제). velog "FastAPI에서 Spring으로 마이그레이션" 사례 한 건을 *한 사례의 경험치*로만 정독.
  - **§13.3 한국 독자에게 줘야 할 인식 보정 4항목 (본문화)** — reference §6.4의 4항목을 본문 톤으로 풀기: ① "FastAPI = Spring 대체"가 아니라 상보적이다, ② 타입 힌트가 있다고 Java처럼 안전하지 않다, ③ "async라서 빠르다"가 아니라 "async를 잘 써야 빠르다", ④ Spring 출신의 가장 큰 충격은 트랜잭션·보안 자동화의 부재(이 책의 6·7장이 답했다)다.
  - **§13.4 한국 도입 사례의 정직한 한계** — reference §9.2 명시: 카카오·네이버·토스의 *공개* FastAPI 사례를 책 집필 시점에 확인 가능한 범위까지만 명기. 확인 못 한 부분은 "확인된 영역(ML/데이터 플랫폼)에 한정"이라 정직하게 적는다. 독자 신뢰가 깨지지 않도록.
  - **§13.5 한국 채용·생태계 현실** — Spring 채용 압도, FastAPI는 보조·실험. 양 다리 전략. "둘 다 쓰는 사람"이 되는 길.
  - **§13.6 SQLModel을 권할 것인가** — 5장에서 미뤘던 비교를 미래·생태계 절로 흡수. reference §5.5 두 관점(편의 vs 학습 깊이). Spring 출신의 결론: SQLAlchemy 2.0 직접 학습이 결국 이득.
  - **§13.7 미래 변수** — Pydantic v2 안정화, free-threaded Python(PEP 703) 추이, ARQ vs Celery의 성숙도 곡선.
  - **§13.8 두 프레임워크를 도구함에 두는 사고** — "어떤 망치를 들 것인가" 의사결정 트리.
  - **§13.9 더 읽을 거리 — 큐레이션 + 짧은 해설**: 단순 링크 나열이 아니라 각 자료가 *왜* 다음 단계인지 한두 줄 해설.
- **예제 소재**: 의사 결정 트리 다이어그램 + 한국 사례 표 (확인 가능한 범위 내) + SQLModel 짧은 코드 비교(5장 도서 카탈로그 예제와 1:1).
- **독자가 얻는 것**: 책을 덮은 뒤의 판단력. "FastAPI 광신도"가 아니라 "도구를 고르는 사람"으로의 정체성 전환 + 한국 시장에서 양 다리 걸치는 실용 감각.
- **예상 분량**: 약 16,000자 (~32페이지) — 원안 12k에서 4k 증가. 인식 보정 4항목 본문화(+1.5k) + SQLModel 흡수(+1k) + 한국 사례 한계 명시(+0.5k) + 더 읽을 거리 해설화(+1k).

---

## 분량 합계 (v2 — 리뷰 라운드 1 반영 후)

| 챕터 | 분량(자) | v1 대비 |
|---|---|---|
| 1. 왜 FastAPI (약점 인식 보강) | 15,000 | +1,000 |
| 2. 환경 셋업 | 13,000 | — |
| 3. 첫 라우트 + Pydantic (슬림화) | 16,000 | -3,000 |
| 4. 의존성 주입 (+APIRouter·미들웨어 절) | 21,000 | +1,000 |
| 5. SQLAlchemy 2.0 (+레이어드, SQLModel 이동) | 20,000 | -2,000 |
| 6. 트랜잭션 | 21,000 | — |
| 7. 인증·인가 (시크릿 도입 명확화) | 19,000 | — |
| 8. 비동기와 GIL (+Kotlin·백그라운드 절) | 23,000 | +3,000 |
| 9. 예외·관측성 (주문 API 도메인) | 18,000 | — |
| 10. 테스트 | 19,000 | — |
| 11. 배포 (메모리 누수 사례화, 시크릿 정리) | 17,000 | — |
| 12. 통합 프로젝트 | 24,000 | — |
| 13. 언제 Spring으로 (인식 보정·SQLModel 흡수) | 16,000 | +4,000 |
| **합계** | **약 242,000자** | +4,000 |

페이지 환산(1페이지 ≈ 500자) → 약 484페이지. 목표 380~430페이지로 압축 시 챕터별 10~15% 다이어트 가능. 최종은 저술·편집 과정에서 조정. 챕터 간 편차는 v1(12~24k, 2배)에서 v2(13~24k, 1.85배)로 약간 완화 — 13장 보강이 효과.

---

## 챕터 의존도 그래프

```
1 (지도)
 └─→ 2 (환경)
      └─→ 3 (첫 라우트 + Pydantic)
            ├─→ 4 (DI) ─────────────────────────────┐
            │                                        │
            └─→ 5 (SQLAlchemy) ───┐                  │
                                  │                  │
                                  └─→ 6 (트랜잭션)   │
                                  │      │           │
                                  │      │           ↓
                                  │      │      ┌─→ 7 (인증)
                                  │      │      │
                                  │      │      ↓
                                  │      └─→ 8 (async)
                                  │             │
                                  └─→ 9 (예외/관측성) ←┘
                                        │
                                        └─→ 10 (테스트)
                                              │
                                              └─→ 11 (배포)
                                                    │
                                                    └─→ 12 (통합 프로젝트)
                                                          │
                                                          └─→ 13 (전환 판단)
```

**해설**:
- **1·2장**은 모든 챕터의 전제. 한 번 읽으면 끝.
- **3장(Pydantic)**은 이후 모든 챕터의 데이터 모델 기반. 가장 강한 전제.
- **4장(DI) → 5장(DB)는 강한 의존**: 5장의 모든 라우트가 `Depends(get_db)`와 `yield` 의존성을 *전제*로 짜여 있다. 4장 없이 5장을 읽으면 코드가 마법처럼 보인다. 발췌 독자도 5장 이전에 4장의 §`yield` 의존성과 §테스트 오버라이드 절은 반드시 보라고 챕터 도입부에 박는다. (이전 v1에서 "병렬"이라 표현했던 부분 정정.)
- **6장(트랜잭션)**은 4·5장 모두를 전제로 한다. 이 책의 가장 강한 hinge.
- **7장(인증)**은 3·4장만으로 읽을 수 있게 설계 (5·6장 의존 최소화). 인증을 빨리 보고 싶은 독자가 6장을 건너뛰고 와도 무리 없게 한다.
- **8장(async)**은 4·5·6장의 sync 모드를 다 본 다음에야 의미가 있다 — 그래서 후반에 배치. 5장의 SQLAlchemy를 async로 다시 보는 과정이 자연스럽다.
- **9장**은 1~8장 코드를 운영 모드로 끌어올리는 챕터. 독립성 약함.
- **10장(테스트)**은 4장(dep override)과 6장(트랜잭션 롤백)을 강하게 전제.
- **11장(배포)**은 8장(워커 수와 GIL)과 9장(헬스/관측)을 전제.
- **12장(통합)**은 1~11장 전체를 활용. 이 책의 캡스톤.
- **13장**은 메타 챕터. 어느 장을 읽다가도 마지막에 들러도 좋다.

**선형 읽기 권장 vs 발췌 읽기**: 책은 선형 읽기를 전제로 쓰되, 각 챕터 시작에 "이 챕터를 읽으려면 알아야 할 것" 박스를 둬서 발췌 독자도 길을 찾게 한다.

---

## 검증 체크리스트 (v2)

- [x] 모든 챕터가 핵심 질문에 답하고 있는가? — 각 챕터에 1~3개 명시.
- [x] 챕터 순서에 맥이 흐르는가? — 3막 구조(친숙함 → 충돌 → 운영) + 6→7→8의 명시성 통주저음을 아크 본문에 명시.
- [x] 대상 독자(Spring 경력자, Python 입문) 수준에 맞는가? — Python 기초만 가정, FastAPI/SQLAlchemy/Pydantic은 처음으로 가정. Spring 비교가 모든 챕터의 통주저음. 3장 슬림화로 진입 부담 경감.
- [x] 레퍼런스의 주요 자료가 빠짐없이 배치되는가? — § 1~6 항목들이 1~11장에 분산 매핑. **§2.5(미들웨어/AOP) → 4장**, **§2.10(백그라운드 작업) → 8장 §8.7**, **§4.3(레이어드 아키텍처) → 5장 한 절**, **§3.2-2(메모리 누수) → 1장 예고 + 11장 사례화**, **§5.7(타입 힌트 한계) → 1장 약점 인식 절**, **§6.4(인식 보정 4항목) → 13장 §13.3**.
- [x] 챕터 간 중복이 없는가? — Pydantic은 3장에만, DI는 4장에만, 트랜잭션은 6장에만, async는 8장이 유일. **시크릿 관리는 7장 도입 + 11장 K8s 연동으로 분리(중복 정리됨)**.
- [x] 예상 분량 합계가 목표 분량에 부합하는가? — 약 242,000자 → 약 484페이지. 목표 380~430페이지 대비 10~15% 다이어트 여지.
- [x] 챕터별 작은 예제 + 12장 통합 프로젝트의 이중 구조가 "다양한 예제" 요구를 만족하는가? — 12개의 서로 다른 도메인 작은 예제(환율/사용자/도서/송금/JWT/ML프록시·배경잡/주문/픽스처/배포/태스크) + 1개의 통합 프로젝트. **9장이 v1의 "데모"에서 "주문 API"로 도메인화됨**.
- [x] 챕터 분량 편차가 합리적인가? — v1 12~24k(2.0배) → v2 13~24k(1.85배). 13장 보강과 3·5장 슬림화로 양 끝을 좁힘.

---

## 리서치 한계 반영

리서치 § 9에서 명시된 한계 중 책 집필 시 보강 필요 항목:
- **13장의 한국 도입 사례 표** — Codenary 재시도 또는 카카오·네이버·토스 기술 블로그 직접 검색 필요. 못 찾으면 "확인된 영역(ML/데이터)만" 정직하게 명시.
- **8장의 Kotlin 코루틴 ↔ Python async 비교** — 직접 합성 필요. Kotlin 출신 독자 비중을 고려할 때 한 절은 필수.
- **6개월 비교 글의 인용 톤** — 일반화하지 않고 "한 사례의 경험치"로만 인용. 6장·11장에서 등장 시 동일 톤 유지.
