# @Transactional이 없는 세상

> Spring 사고를 끌고 와서 FastAPI를 짓는 법 — `@Transactional`이 사라진 자리에 무엇을 놓을지를 13개 장 한 호흡으로.

- **저자:** Toby-AI
- **부제:** Spring 사고로 FastAPI를 짓는 법
- **버전:** v1.0.0
- **발행일:** 2026-05-16
- **언어:** 한국어 (ko)
- **분량:** 13개 장 + 머리말·에필로그·부록 2종 / 본문 약 22만 자 (공백 제외)
- **라이선스:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko)

## 이 책은 무엇인가

Spring Boot·Spring Data JPA·Spring Security가 손에 박힌 한국 백엔드 개발자가 FastAPI를 *두 번째 도구함*으로 익히는 책이다. 단순 튜토리얼이 아니라, "Spring 사고와의 충돌·전환"을 통주저음으로 깔고 가는 에세이형 기술서에 가깝다. `@RestController`·`@Autowired`·`@Transactional`·`@PreAuthorize`·Actuator·MockMvc가 사라진 자리에 *무엇이 들어서는지*를 한눈 매핑표 한 장에서 시작해, 사내 태스크 관리 API + Slack 알림 봇이라는 통합 프로젝트 한 개로 닫는다.

세 막의 구조다. **1막 — 친숙함의 다리(1~3장)** 는 Spring과 1:1로 그려지는 영역만 골라 손을 잡아 끈다. **2막 — 충돌과 전환(4~8장)** 은 의존성 주입에서 워밍업한 뒤 SQLAlchemy에서 첫 충격, 트랜잭션에서 절정, 인증과 비동기에서 두 번째·세 번째 충돌로 사고 모델을 재구성한다. **3막 — 운영과 통합(9~13장)** 은 Actuator·MockMvc·Tomcat의 빈자리를 무엇으로 메우는지 보여주고, 12장에서 통합 프로젝트로 모든 조각을 한 코드베이스에 묶은 뒤, 13장에서 *언제 Spring으로 돌아가야 하는가*를 정직하게 짚는다.

핵심 약속을 한 문장으로 — *Spring을 버리는 책이 아니라 더하는 책*. *옮긴다*가 아니라 *짓는다*.

## 누구를 위한 책인가

이 책은 *Spring 출신 백엔드 개발자*를 향한다. 더 구체적으로는 — Java 또는 Kotlin으로 Spring Boot·Spring MVC·Spring Data JPA·Spring Security를 *프로덕션에서* 써본 사람. 빈 컨테이너 라이프사이클, `@Transactional` 전파 옵션, JPA의 1차 캐시, MockMvc로 컨트롤러 테스트하는 손버릇이 머리에 박혀 있다고 가정하고 글이 짜인다.

Python은 기초만 가정한다 — `if/for/list/dict`와 함수 정의 수준이면 따라올 수 있다. FastAPI는 처음, SQLAlchemy·Pydantic도 처음으로 가정한다. 반대로 — Python 자체 입문서는 아니고, FastAPI 모든 기능의 망라식 매뉴얼도 아니다. 공식 문서가 이미 친절하다. 이 책은 *Spring 사고와 부딪히는 지점*에 본문 무게를 둔다.

진입 상태와 출구 상태를 짧게 적자면 —

- **진입 상태:** "Python 백엔드를 한번 써봐야 한다는데 막막하다. `@Autowired`·`@Transactional`·`@RestController`가 머리에 박혀 있고, FastAPI 튜토리얼을 봐도 '그래서 트랜잭션은 어떻게 걸지?'에서 막힌다."
- **출구 상태:** FastAPI로 프로덕션급 API를 한 권의 책 호흡 안에서 만들 수 있다. Spring과 다르게 동작하는 지점(트랜잭션·DI 스코프·async·보안)을 알고, 어떤 경우에 FastAPI를 고르고 어떤 경우에 Spring으로 돌아갈지 판단할 수 있다.

## 무엇을 얻게 되는가

- Spring ↔ FastAPI를 가로지르는 한눈 매핑 지도 — 책 전체를 관통하는 1장의 표가 본문 어디에서나 다시 펴진다.
- `@Transactional`이 자동으로 해주던 일을 *내 손으로 명시*하는 감각 — SQLAlchemy 2.0 Session·UoW·`session.begin()`까지.
- `@Autowired`에서 `Depends()`로 — DI 스코프 차이(요청 단위 캐시, `lifespan`, `@lru_cache`)를 머릿속에 다시 그리는 법.
- Spring Security 없이 OAuth2/JWT를 손으로 짓고, 보호 라우트마다 `Depends(get_current_user)`를 *명시*하는 흐름.
- WebFlux 사고를 코루틴으로 옮기되, *async가 항상 빠르지 않다*는 사실을 함께 익히기.
- Actuator·MockMvc·Tomcat의 빈자리를 OpenTelemetry·TestClient + pytest·Uvicorn + Gunicorn + 컨테이너로 메우는 운영 감각.
- 마지막으로 — *언제 Spring으로 돌아가야 하는가*에 대한 정직한 판단 기준. 한국 시장 현실까지 포함해서.

## 차례

1. **왜 FastAPI, 왜 Spring 출신에게 친숙한가** — 한눈 매핑표 한 장으로 책 전체의 지도를 깔고, 정직한 약점(트랜잭션·보안 자동화 부재, 메모리 누수, 운영 비용)을 함께 인정한다.
2. **개발 환경 — Maven/Gradle 마인드에서 uv·Poetry로** — `pyproject.toml`을 `pom.xml` 옆에 놓고, IntelliJ급 안전망(mypy/pyright/ruff/black)을 어떻게 다시 짤지.
3. **첫 라우트와 Pydantic — `@RestController` × DTO를 한 줄에 녹이기** — 타입 힌트 한 줄이 곧 검증·직렬화·`/docs`의 단일 소스가 된다는 사실의 의미.
4. **의존성 주입 — `@Autowired`에서 `Depends()`로** — 함수 파라미터의 마커가 어떻게 빈 컨테이너의 역할을 대신하는가. 스코프·캐시·`lifespan`까지.
5. **데이터 접근 — JPA에서 SQLAlchemy 2.0으로** — Session·Unit of Work·Identity Map. JPA의 1차 캐시와 어디까지 같고 어디서 갈라지는가.
6. **트랜잭션 — `@Transactional`이 없는 세상에서 살아남기** — 책의 척추. 트랜잭션 경계를 *손으로* 그리는 감각, 전파·롤백·중첩까지.
7. **인증·인가 — Spring Security 없이 OAuth2/JWT** — 6장의 명시성이 보안에 그대로 이어진다. 토큰 발급·검증·보호 라우트를 직접 짓는다.
8. **비동기와 GIL — WebFlux 사고를 코루틴으로** — async가 *선택적 가속*인 이유. 함수 색깔(color) 문제와 sync/async 혼용 가이드.
9. **예외·로깅·관측성 — Actuator 없이** — 예외 핸들러를 어디에 두는지, OpenTelemetry로 트레이스를 어떻게 깔지.
10. **테스트 — MockMvc에서 TestClient + pytest로** — 픽스처 사고의 전환, DB 격리, 의존성 오버라이드.
11. **배포·운영 — Tomcat에서 Uvicorn + Gunicorn + 컨테이너로** — 워커 모델·시그널 처리·메모리 누수 감지까지.
12. **통합 프로젝트 — 사내 태스크 관리 API + Slack 알림 봇** — 1~11장이 한 코드베이스로 합쳐지는 한 호흡의 마무리.
13. **언제 Spring으로 돌아가야 하는가** — 정직한 한계 인정. 한국 시장의 현실, 팀·도메인·운영 비용 기준의 판단 표.

부록으로 *Spring ↔ FastAPI 매핑 한눈에* 표와 *더 읽을 거리* 큐레이션 가이드가 따라붙는다.

## 저자 소개

Toby-AI는 한국 개발자 커뮤니티의 글쓰기·아키텍처·교육 어휘를 학습한 AI 저자 페르소나다. 평어체와 청유형, 수사적 질문과 상황 가정, "정직한 한계 인정" 같은 호흡을 의도적으로 살려 쓴다. 이 책은 Spring을 *프로덕션에서 길게* 굴려본 독자를 1번 좌석에 앉힌 채, 같은 작업대 옆에 FastAPI를 가져다 놓는 손길로 짜여 있다.

## 책 정보

- **파일:** `@Transactional이-없는-세상-v1.0.0.epub` (EPUB 3, 약 376 KB)
- **하네스:** [book-writer](https://github.com/) v1.2.0
- **형식 검증:** EPUB 3 구조 정상 (mimetype·OPF·NCX·nav 모두 포함, 14개 본문 챕터로 split). `epubcheck` 실행 결과 차례의 내부 fragment 링크 16건이 RSC-012 경고를 일으키지만 (장(chapter) 단위 split에서 발생하는 알려진 패턴) 모든 주요 리더에서 정상 동작한다.
- **라이선스:** CC BY-NC-SA 4.0 — 저작자 표시·비상업적 이용·동일조건 변경허락
