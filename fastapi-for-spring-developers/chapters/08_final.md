# 8장. 비동기와 GIL — WebFlux 사고를 코루틴으로

Spring WebFlux를 한 번이라도 진지하게 써본 손이라면 이런 장면이 익숙할 것이다. `Mono<User> user = userRepository.findById(id)`를 받아 `.flatMap`으로 묶고, `.subscribeOn(Schedulers.boundedElastic())`로 스레드 풀을 지정하고, 백프레셔가 어느 단계에서 깨졌는지 추적하느라 머리를 굴리던 그 시간. 반응형 사고가 손에 익기까지 걸린 비용을 기억할 것이다.

FastAPI를 처음 마주하면 `async def` 한 줄이 너무 가벼워 보인다. WebFlux의 그 무게가 다 어디로 갔지? 한 줄로 `async def read_user(...)`라고 쓰고, 안에서 `await db.execute(...)`만 해주면 끝이라고? 정말로?

정답부터 적자면, *손 모양은 가벼워졌고 함정의 모양도 가벼워졌다*. 그러나 함정 자체는 여전히 있고, *어떤 함정은 WebFlux 때보다 더 조용히 다친다*. 가장 흔한 사고가 이렇다 — async로 짰는데 sync DB 클라이언트를 한 줄 섞었다. 라이브러리 임포트가 잘못된 게 아니다, 코드는 정상 돌아간다. 그런데 부하 측정해보면 *sync로 짠 같은 코드보다 느리다*. 한 사례 보고는 sync 600 req/s, async + sync DB 550 req/s를 적어 둔다. 비동기의 오버헤드만 있고 이점은 없다.

두 가지를 손에 익히고 가자. 첫째, *`async def`를 어디에 쓰고 어디에 쓰지 말지*의 판단 회로. 둘째, `@Async`·`@Scheduled`가 떠받쳐 주던 *비동기 보조 자리* — 백그라운드 작업, 스케줄러 — 에 무엇을 놓을지의 의사결정 트리. Kotlin 코루틴 출신 독자에겐 한 절을 더 박아둔다, `suspend fun`과 `async def`의 닮음·다름을. GIL과 free-threaded Python의 2026년 현재 상태도 한 번 짚는다 — 한국 시장에 흘러다니는 "Python은 GIL 때문에 안 된다"는 단정을 정확한 자리에 놓아두는 게 본인 판단에 좋다.

> **이 장을 읽기 전 알아둘 것**
> - 5장의 SQLAlchemy 동기 모드와 `get_db` `yield` 의존성, 그리고 6장의 명시적 트랜잭션 경계는 본 장이 *async로 다시 쓰는 같은 그림*의 출발점이다.
> - 4장의 `Depends()` 그래프와 `Annotated[..., Depends(...)]` 타입 별칭 패턴이 본 장의 모든 라우트에 그대로 들어간다.

## §8.1 모델 비교 — WSGI vs ASGI, MVC vs WebFlux

Java 진영에 두 패러다임이 있다. *Spring MVC*는 서블릿 위의 동기·블로킹 모델이다. 한 요청에 한 스레드가 잡혀, DB·외부 API가 응답할 때까지 그 스레드가 점유된다. Tomcat 같은 컨테이너가 *스레드 풀*에 수십~수백 개를 미리 띄워두고 들어오는 요청에 하나씩 배정한다. *Spring WebFlux*는 Project Reactor·Netty 위의 비동기·논블로킹 모델이다. 한 스레드가 여러 요청을 *짧게짧게* 갈아 끼우며 처리한다. I/O 대기는 콜백으로 풀고, 스레드는 다른 요청을 본다.

Python 진영의 평행 분리가 *WSGI*와 *ASGI*다. WSGI(Web Server Gateway Interface)는 동기 인터페이스다 — Django·Flask가 오래 살아온 자리. ASGI(Asynchronous Server Gateway Interface)는 비동기 인터페이스다. FastAPI는 처음부터 ASGI 위에 있다.

| Java 진영 | Python 진영 | 본질 |
|---|---|---|
| Spring MVC + Servlet + Tomcat | WSGI + Gunicorn + Django/Flask | 한 요청 = 한 스레드, 블로킹 I/O |
| Spring WebFlux + Reactor + Netty | ASGI + Uvicorn + FastAPI | 한 스레드 = 여러 요청, 논블로킹 I/O |

매핑이 거의 1:1이다. 그래서 *FastAPI는 WebFlux가 기본값인 Spring*이라고 비유하는 게 가장 빠른 손짐작이다. 다만 두 가지 결이 다르다.

첫째, FastAPI는 *`async def`와 `def`를 한 앱 안에 섞어 쓸 수 있다*. WebFlux로 가면 *전 흐름이 반응형*이 되어야 일관성이 산다. `Mono`/`Flux` 중간에 블로킹 호출 하나가 끼면 그 자리부터 풀이 깨진다. FastAPI는 좀 더 너그럽다 — `def`로 두면 자동으로 스레드 풀에서 돌려준다. 이게 좋은 안전망이자 동시에 함정이다(§8.4에서 본격적으로).

둘째, *동시성 모델*이 다르다. WebFlux의 한 스레드는 진짜 OS 스레드고, 풀에 여럿이 있다. Python의 한 이벤트 루프는 *단일 스레드 안의 코루틴 스케줄러*다. GIL 때문에 사실상 한 시점엔 한 코루틴만 진행한다(§8.5). 이게 어떤 워크로드엔 자산이고 어떤 워크로드엔 부담이다.

## §8.2 이벤트 루프 — Java 스레드풀과의 본질적 차이

WebFlux의 `boundedElastic` 풀을 떠올려 보자. 풀에 스레드가 N개 있고, 작업이 들어오면 비어 있는 스레드에 배정한다. 스레드 자체는 OS 차원의 단위라 컨텍스트 스위치 비용이 있다. WebFlux가 자랑하는 효율은 *I/O 대기 동안 스레드를 점유하지 않는다*는 한 줄에서 나온다.

Python의 `asyncio` 이벤트 루프는 결이 다르다. 스레드가 *하나*다. 그 스레드가 코루틴들의 *순서*를 관리한다. 한 코루틴이 `await some_io()`를 만나면, 그 자리에 *돌아올 표시*를 남기고 다른 코루틴으로 넘어간다. I/O가 끝나면 표시한 자리로 돌아와 이어 실행한다. 마치 한 주방장이 여러 냄비를 동시에 끓이는 그림이다 — 한 냄비가 끓는 동안 다음 냄비를 본다.

```python
# 이벤트 루프의 정신적 모양
import asyncio

async def task_a():
    print("A 시작")
    await asyncio.sleep(2)   # 여기서 제어권을 루프에 반납
    print("A 끝")

async def task_b():
    print("B 시작")
    await asyncio.sleep(1)
    print("B 끝")

async def main():
    await asyncio.gather(task_a(), task_b())

asyncio.run(main())
# 출력:
# A 시작
# B 시작
# (1초 후)
# B 끝
# (1초 후)
# A 끝
```

이 정신적 모양 한 줄이 본 장의 모든 함정을 푸는 열쇠다. **`await` 한 곳이 *제어권 반납 지점*이다**. `await`이 없는 코드는 *반납을 하지 않는다*. 그 동안 다른 코루틴이 진행될 수 없다 — 이벤트 루프가 점유된다.

다시 강조한다. WebFlux는 *스레드가 풀에 여러 개*라 한 스레드가 막혀도 다른 스레드가 진행한다. FastAPI의 async 라우트는 *한 이벤트 루프*가 모든 코루틴을 굴리는 모양이다. 한 코루틴이 막히면 *그 워커의 모든 요청이 동시에 멈춘다*. 이게 다음 절의 함정으로 직결된다.

## §8.3 함정 — "Async가 항상 빠르지 않다"

본 장의 핵심 함정이다. 정신적으로 깊게 박아두자.

흔한 시나리오를 그려보자. 신입이 도서 카탈로그 API를 짠다. 5장에서 짠 동기 SQLAlchemy 코드를 가지고 와서, 라우트만 `async def`로 갈아 끼우고, "이제 비동기야"라고 안심한다.

```python
# 함정 — async 라우트 + sync SQLAlchemy
@router.get("/books/{book_id}")
async def get_book(book_id: int, db: DbSession):
    book = db.get(Book, book_id)        # 동기 SQLAlchemy — 블로킹
    return BookRead.model_validate(book)
```

이 코드는 정상 돌아간다. 테스트도 통과한다. 그런데 부하가 들어오면 *동기 버전보다 더 느리다*. 한 사례 보고는 이렇게 적는다 — sync FastAPI + sync SQLAlchemy가 ~600 req/s, async FastAPI + sync SQLAlchemy가 ~550 req/s. 일관되게 *async 쪽이 더 느리다*.

왜 이런가? 본 장 §8.2의 한 줄로 풀린다. `db.get(Book, book_id)`는 sync 함수다. `await`이 없다. 이벤트 루프가 *제어권을 반납받지 못한다*. 그 동안 다른 요청은 그저 줄을 선다. 한 워커가 한 요청씩 처리하는 *동기처럼* 동작하는데, 비동기 오버헤드(이벤트 루프 디스패치, 코루틴 프레임 생성)는 그대로 든다. 결과는 *느려지기*다.

한 사례 보고가 같은 함정을 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *어떤 개발자가 async로 '최적화' 한 뒤 FastAPI 성능이 곤두박질친 이유를 일주일 디버깅했다. async 함수 안에서 무거운 데이터 변환을 돌렸고 그게 이벤트 루프를 막고 있었다.* — Medium: lessons learned debugging (reference §4.1).

이 한 사례 보고가 본 장의 모든 가르침을 한 줄로 요약한다. *async 안에 sync를 섞지 말자*. 섞어야 한다면 §8.4의 안전 패턴을 쓰자.

세 가지 함정 유형을 분리해 두자.

**유형 1 — sync DB 클라이언트.** 위 예제. 해결책: async DB 드라이버(`asyncpg`, `aiomysql`)와 `AsyncSession`으로 통일. 또는 라우트를 `def`로 두자(§8.4의 자동 스레드풀로 떨어진다).

**유형 2 — CPU 무거운 연산.** 이미지 리사이즈, JSON 수만 줄 파싱, 정규식 폭주. 이런 건 async로 둘러도 *이벤트 루프 점유*가 본질이다. 해결책: `asyncio.to_thread`로 다른 스레드에 떼어 보내거나, 무거우면 *프로세스 풀*(또는 별도 워커)로 빼자.

**유형 3 — 블로킹 라이브러리 호출.** `requests.get(...)`, `time.sleep(5)`, 동기 Redis 클라이언트. async 라우트에 한 줄만 있어도 그 시간 동안 이벤트 루프가 멈춘다. 해결책: async 대응 라이브러리(`httpx`의 `AsyncClient`, `aioredis`)로 교체.

원칙 한 줄: **`async def` 라우트면, 그 안의 모든 I/O가 `await` 가능해야 한다**. 안 그러면 안전망이 깨진다.

### 한 번 측정해보자 — ML 추론 프록시 예제

추상적으로 듣지 말고 본인 손으로 한 번 측정해보자. 외부 ML 모델 API를 프록시하는 라우트를 셋으로 짜본다. 같은 일을 *동기로*, *async + sync 클라이언트로*, *async + async 클라이언트로*. 같은 부하를 흘려서 처리량을 비교한다.

```python
# app/ml/router.py — 세 가지 버전
import time
import requests
import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/ml")


# (a) 동기 def 라우트
@router.get("/sync")
def predict_sync(prompt: str):
    response = requests.post("http://ml-backend/infer", json={"prompt": prompt}, timeout=5)
    return response.json()


# (b) async 라우트 + 동기 클라이언트 (함정)
@router.get("/async-blocking")
async def predict_async_blocking(prompt: str):
    response = requests.post("http://ml-backend/infer", json={"prompt": prompt}, timeout=5)
    return response.json()


# (c) async 라우트 + async 클라이언트 (정석)
@router.get("/async-proper")
async def predict_async_proper(prompt: str, http_client: HttpClientDep):
    response = await http_client.post("http://ml-backend/infer", json={"prompt": prompt})
    return response.json()
```

`hey`나 `wrk` 같은 부하 도구로 동시 50 연결, 1만 요청을 흘려 보자.

```bash
$ hey -n 10000 -c 50 http://localhost:8000/ml/sync
$ hey -n 10000 -c 50 http://localhost:8000/ml/async-blocking
$ hey -n 10000 -c 50 http://localhost:8000/ml/async-proper
```

한 사례 보고를 기준으로 대략적인 결과 모양을 적어두자(환경에 따라 절댓값은 다르지만 *순서*는 일관된다).

| 버전 | 처리량 | P95 지연 | 비고 |
|---|---|---|---|
| (a) sync `def` | ~600 req/s | ~85ms | FastAPI 자동 스레드풀이 받침 |
| (b) async + 동기 클라이언트 | ~550 req/s | ~120ms | 이벤트 루프 점유로 *더 느림* |
| (c) async + async 클라이언트 | ~2,400 req/s | ~25ms | I/O 대기 동안 다른 요청 진행 |

(c)와 (a)의 차이가 약 *4배*다. 그게 async가 빛나는 자리다. 그러나 (b)는 *async를 흉내만 낸* 자리라 손해다 — 정확히 이 함정이 본 장이 가장 자주 지목하는 곳이다.

손에 익혀두자. **부하 측정 없이 async를 끼지 말자.** 측정해보고 (c)에 도달했을 때만 async의 이점이 손에 잡힌다. 그 전까지는 (a)가 안전하다.

## §8.4 안전 패턴 — sync를 async에 안전하게 묶기

원칙은 명료한데 현실은 그렇지 못하다. 우리가 쓰고 싶은 라이브러리 중에 async 버전이 없는 게 있다. 또는 *지금 코드를 다 갈아엎기 어려운* 상황이 있다. 이때 쓰는 안전망 두 개를 손에 익히자.

### `asyncio.to_thread` — 한 호출을 별도 스레드로

표준 라이브러리에 들어 있는 한 줄짜리 안전망이다. 동기 함수를 *별도 스레드에서 실행*하고, 그 결과를 `await` 가능한 코루틴으로 감싸 준다.

```python
import asyncio

@router.get("/books/{book_id}")
async def get_book(book_id: int, db: DbSession):
    # sync SQLAlchemy를 그대로 쓰되, 스레드로 떼어 보낸다
    book = await asyncio.to_thread(db.get, Book, book_id)
    return BookRead.model_validate(book)
```

`asyncio.to_thread(fn, *args)`는 내부적으로 *기본 스레드풀*에 작업을 던지고, 그 동안 이벤트 루프는 자유롭다. 다른 코루틴이 계속 진행한다. 결과가 준비되면 await이 풀리면서 이 코루틴이 이어진다.

비용을 한 번 짚어두자. 스레드를 빌리는 데 드는 *컨텍스트 스위치 비용*은 0이 아니다. 짧고 가벼운 작업엔 이게 오버헤드로 작용한다. 그래서 *원칙은 async 네이티브 라이브러리로 교체*가 맞고, *불가피한 경우의 임시 다리*가 `asyncio.to_thread`다. 영구 해결책으로 두면 안 된다.

FastAPI 진영엔 거의 같은 일을 하는 헬퍼가 또 있다.

```python
from fastapi.concurrency import run_in_threadpool

book = await run_in_threadpool(db.get, Book, book_id)
```

내부 구현은 거의 동등하다. 취향대로 골라 쓰자.

### sync def 라우트 — 자동 스레드풀의 안전망

여기 한 가지 더 손에 익혀두자. **FastAPI는 `def`로 선언한 라우트를 자동으로 스레드풀에서 실행한다.** 한 줄을 `async def`로 안 바꿔도, 이벤트 루프를 막지 않는다. *async 안전망*이 한 단계 더 있는 셈이다.

```python
# def 라우트 — FastAPI가 자동으로 threadpool에 던진다
@router.get("/books/{book_id}")
def get_book(book_id: int, db: DbSession):
    book = db.get(Book, book_id)
    return BookRead.model_validate(book)
```

이게 좋은 안전망이다. 5장에서 우리가 짠 sync 라우트들은 사실 이 안전망 위에서 정상 동작하고 있었다. *판단이 의심스러우면 `def`로 두는 게 낫다* — 이게 본 장이 줄 수 있는 가장 실용적인 한 줄이다.

그렇다면 언제 `async def`로 가는가? 답은 두 조건이 모두 맞을 때다.

1. 라우트 안의 모든 I/O가 *async 대응 라이브러리*로 구현돼 있다 (httpx AsyncClient, AsyncSession, aioredis 등).
2. 동시에 처리할 *I/O-bound 요청 수가 많다* — ML 모델 프록시, 외부 API 팬아웃, SSE/WebSocket 스트리밍처럼.

위 둘이 다 맞으면 async가 손에 잡히는 이득을 준다. 한쪽이라도 빠지면 sync `def`로 두고 자동 스레드풀에 맡기는 편이 낫다. *최적화는 측정 뒤에 한다*는 오래된 원칙이 본 장에서도 그대로다.

손에 익혀두자.

| 상황 | 권장 |
|---|---|
| 모든 I/O가 async | `async def` 라우트 |
| sync 라이브러리 1~2곳 | `async def` + `asyncio.to_thread`로 그 호출만 격리 |
| sync 라이브러리가 다수 | `def` 라우트 (자동 스레드풀) |
| CPU 무거운 작업 | `def` 라우트, 더 무거우면 별도 워커(§8.7) |
| 판단 애매 | `def` 라우트로 출발 — 안전망 위에서 출발 |

## §8.5 GIL — CPU-bound vs I/O-bound의 갈림과 PEP 703의 2026 현재

여기서 Java 출신이 가장 자주 갸우뚱하는 한 줄에 정확한 자리를 주자. *Python에는 GIL이 있어서 멀티스레드가 안 된다*는 단정이다. 반은 맞고 반은 틀린다.

GIL(Global Interpreter Lock)은 CPython 인터프리터에 박혀 있는 *전역 락*이다. 한 시점에 *Python 바이트코드를 실행하는 스레드는 하나*만 진행한다. 그래서 *순수 Python으로 CPU 무거운 일*을 멀티스레드로 돌려도 코어 하나만 쓴다. JVM의 정통 멀티스레드 효율을 기대하면 끔찍하다.

다만 한 줄을 더 보자. **I/O 대기 중에는 GIL이 풀린다.** 그래서 *I/O-bound* 워크로드(DB 쿼리, HTTP 호출, 파일 읽기)는 스레드를 늘려도 효과가 있다. asyncio가 단일 스레드에서 동작해도 *I/O 대기 중엔* 다른 코루틴이 진행할 수 있는 이유다. CPU가 진짜로 도는 시간은 *짧다*는 가정이 깔린 모델이다.

Spring 출신이 손에 익은 매핑으로 정리하자.

| 워크로드 | Java/Spring | Python/FastAPI |
|---|---|---|
| I/O-bound (대다수 API) | 멀티스레드 OK | asyncio 또는 멀티스레드 — 둘 다 효과 있음 |
| CPU-bound (이미지, 인코딩, ML 추론) | 멀티스레드/멀티프로세스 둘 다 | **멀티프로세스 권장.** asyncio·스레드는 효과 약함 |
| 혼합 | 한 스레드 풀로 | I/O는 async, CPU는 별도 워커로 분리 |

본 책의 1~7장이 다 *I/O-bound* 영역이다. 그래서 우리는 한 번도 GIL이 발목을 잡은 적이 없다. ML 모델 서빙처럼 CPU가 진짜로 도는 영역에 들어가면 그때 *별도 워커 또는 멀티프로세스*가 답이 된다. 11장이 그 자리를 본격적으로 다룬다.

### PEP 703과 free-threaded Python — 2026 현재

2023년 10월에 PEP 703이 받아들여졌다. 한 줄로 요약하면 *GIL을 제거한 빌드를 옵션으로 제공*한다. Python 3.13(2024년 10월)부터 *experimental* free-threaded 빌드(`python3.13t`)가 함께 배포된다. 2026년 현재, free-threaded 빌드는 *베타*에 가까운 단계다 — 표준 라이브러리는 거의 호환되지만, *C 확장 모듈*(NumPy, Pillow, psycopg, lxml 등)은 호환이 진행 중이다. 프로덕션 권장은 아직 아니다.

그러면 *언제 우리가 신경 쓰게 될까?* 한 시점이 있다. C 확장 호환이 70~80% 수준에 도달하고, 주요 ASGI 서버(uvicorn, hypercorn)가 free-threaded 모드를 검증할 때 — 빠르면 2027년, 보수적으론 2028년이다. 그때까지 *프로덕션 가이드는 여전히 프로세스 다중화*(uvicorn workers, k8s replicas)다.

손에 익혀두자. **2026년 현재 FastAPI 프로덕션 배포의 표준은 *프로세스 다중화*다.** GIL이 무서워서가 아니다. *프로세스 단위 격리*가 운영적으로 단단하기 때문이다(11장에서 본격).

### CPU-bound를 만났을 때 — 한 줄짜리 우회

CPU가 진짜로 도는 작업이 한두 군데 끼는 경우의 표준 손짐작 한 줄을 짚어두자. `concurrent.futures.ProcessPoolExecutor`를 통과시키는 패턴이다.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

# 앱 생명주기에 맞춰 한 번 만든다 (lifespan에서)
process_pool = ProcessPoolExecutor(max_workers=4)


def heavy_image_resize(image_bytes: bytes) -> bytes:
    # Pillow로 리사이즈하는 CPU 무거운 작업
    ...


@router.post("/thumbnails")
async def make_thumbnail(file: UploadFile):
    image_bytes = await file.read()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(process_pool, heavy_image_resize, image_bytes)
    return Response(result, media_type="image/jpeg")
```

`run_in_executor`에 `ProcessPoolExecutor`를 넘기면 GIL을 우회한 *진짜 멀티프로세스* 실행이 된다. 이벤트 루프는 자유롭게 다른 코루틴을 진행하고, 무거운 일은 *별도 프로세스가* 받는다. Spring에서 `@Async`로 ExecutorService에 던지는 모양과 정신적 짝이다.

다만 한 가지를 짚어두자 — *프로세스 간 인자·결과가 직렬화*된다(pickle). 큰 바이너리를 매번 복사하면 비용이 크다. 그래서 *진짜 무거운 CPU 작업*은 본격적으로 §8.7의 ARQ/Celery 워커로 빼는 편이 낫다. `ProcessPoolExecutor`는 *한두 군데 작은 우회용*이다.

### 한국 시장의 흔한 단정 — "Python은 GIL 때문에 안 된다"

한국 백엔드 커뮤니티에 흘러 다니는 단정 한 줄에 정확한 자리를 주자. *"Python은 GIL이 있어서 동시성이 안 된다"*는 말. 이게 정확한 자리는 *CPU-bound 워크로드*다. *I/O-bound* 영역에선 거의 모든 백엔드 워크로드가 그 안에 들어가고, asyncio가 풀어준다.

한국에서 FastAPI를 진지하게 쓰는 자리들이 어디인지 보면 답이 보인다 — *ML 서빙*, *내부 데이터 플랫폼 API*, *외부 API 통합*. 이들이 다 I/O-bound다. 그래서 GIL이 발목을 잡지 않는다. *Java처럼 코어 다 쓰는 멀티스레드*가 안 되는 건 맞지만, *코어 다 쓰려고 멀티스레드를 쓰지 않는다* — 멀티프로세스(uvicorn workers, k8s replicas)로 *프로세스 단위*로 다 쓴다. 결과적으로 코어가 놀지 않는다. 단정의 절반은 맞고 절반은 잘못된 비유다.

손에 익혀두자. **본인이 짜는 API가 I/O-bound라면 GIL 논쟁에 휘말리지 말자.** 측정해서 (c) 패턴(§8.3)으로 도달하면 그게 답이다.

## §8.6 Kotlin 코루틴 ↔ Python async — 닮음과 다름

Kotlin 백엔드 경력이 있는 독자에게는 한 절을 따로 박아둔다. `suspend fun`과 `async def`는 *같은 정신*에서 출발한 두 언어다 — 정지 가능한 함수를 통해 협력적 동시성을 구현한다는 점. 그러나 결이 다른 자리가 셋 있다.

먼저 가장 닮은 자리부터 보자.

```kotlin
// Kotlin
suspend fun getUser(id: Long): User {
    val user = userRepository.findById(id)  // suspend 함수 — 정지점
    return user
}
```

```python
# Python
async def get_user(id: int) -> User:
    user = await user_repository.find_by_id(id)   # await — 정지점
    return user
```

`suspend fun` ↔ `async def`, *호출 가능한 정지점*이 양쪽 다 있다. 호출자도 정지 함수 또는 async 컨텍스트여야 한다는 *전파 규칙*도 같다 — Kotlin은 `suspend`가 위로 전파되고, Python은 *함수가 async면 호출자도 async에서 await해야* 한다.

이제 다른 자리 셋이다.

**첫째, structured concurrency가 다르다.** Kotlin은 `coroutineScope { ... }` 또는 `supervisorScope { ... }`로 *부모-자식 코루틴의 생명주기*가 자동으로 묶인다. 부모 블록이 끝나면 자식도 다 끝나거나 취소된다. *코루틴이 새어나가지 않는다*. Python의 `asyncio`는 오래도록 이 자리가 약했다. 다행히 3.11부터 `asyncio.TaskGroup`이 들어와서 비슷한 그림이 가능해졌다.

```python
import asyncio

async def fetch_user_details(user_id: int):
    async with asyncio.TaskGroup() as tg:
        profile_task = tg.create_task(fetch_profile(user_id))
        orders_task = tg.create_task(fetch_orders(user_id))
        reviews_task = tg.create_task(fetch_reviews(user_id))
    # 블록을 빠져나오는 시점에 모든 자식 태스크가 완료. 하나라도 실패하면 형제 취소.
    return {
        "profile": profile_task.result(),
        "orders": orders_task.result(),
        "reviews": reviews_task.result(),
    }
```

Kotlin의 `coroutineScope` 정신을 *비슷한 손짐작*으로 받는 자리다. 다만 *3.11 이전 버전을 쓰는 코드*가 인터넷에 여전히 많고, `asyncio.gather`로 비슷한 일을 하지만 *실패 전파*가 미묘하게 다르다 — `TaskGroup` 쪽이 더 강하다.

**둘째, 디스패처 명시성이 다르다.** Kotlin에선 `withContext(Dispatchers.IO) { ... }`나 `withContext(Dispatchers.Default) { ... }`로 *어느 풀에서 돌릴지*를 코드에 박는다. Python에선 이게 묵시적이다. 같은 이벤트 루프에서 다 돌린다. *별도 스레드로 빼야 할 때*만 `asyncio.to_thread`나 `loop.run_in_executor`로 *명시적*으로 떼어 보낸다. 손짐작이 더 단조롭다 — 좋은 자리이자 동시에 *실수가 묻히기 쉬운* 자리.

**셋째, `runBlocking` ↔ `asyncio.run`.** Kotlin의 `runBlocking { ... }`은 *현재 스레드를 점유*해서 코루틴 결과를 받는다 — 메인 함수나 테스트에서 쓰는 다리다. Python의 `asyncio.run(main())`도 같은 자리다 — *이벤트 루프를 만들고, main 코루틴이 끝날 때까지 블로킹하고, 루프를 정리한다*. 한 가지 주의점이 있다 — `asyncio.run()`은 *프로세스 당 한 번*만 깔끔하게 동작한다. 라이브러리 안에서 함부로 호출하면 안 된다. 호출자에게 *이미 돌고 있는 루프가 있는지*를 위임하는 호흡이 안전하다.

손에 익혀두자. Kotlin의 명시적·구조적 동시성에 익숙한 손이라면, Python에선 *덜 명시적이지만 더 단조로운* 호흡을 만나게 된다. 좋은 점은 손이 가볍다는 것, 다친 자리는 *명시성이 없어서 누군가 sync 한 줄을 슬쩍 끼웠을 때 폭발의 원인이 모호하다는 것*. §8.4의 안전 패턴이 그 모호함을 다소 메운다.

## §8.7 백그라운드 작업 — `@Async`·`@Scheduled`의 대체

이 절이 본 장의 마지막 큰 자리다. Spring 진영에선 *짧고 가벼운* 백그라운드 작업은 `@Async`, *반복 스케줄*은 `@Scheduled(cron=...)`, *분산·신뢰성 있는 큐*는 RabbitMQ/Kafka + 별도 워커로 풀어왔다. 같은 그림을 FastAPI 진영에선 어떻게 받는가?

답은 *한 도구가 아니라 도구함*이다. 네 후보를 짚어두자.

| 용도 | Spring | FastAPI 진영 |
|---|---|---|
| 짧은 fire-and-forget | `@Async` | `BackgroundTasks` |
| 같은 프로세스 내 스케줄 | `@Scheduled(cron)` | APScheduler |
| asyncio 친화 분산 큐 | (Java 외부 큐) | ARQ |
| 성숙한 분산 큐 | Quartz/Spring Batch | Celery |

하나씩 본다.

### `BackgroundTasks` — fire-and-forget의 표준

FastAPI에 내장된 가장 가벼운 백그라운드 도구다. 라우트가 응답을 *먼저 보내고*, 그 뒤에 *같은 프로세스에서* 추가 작업을 실행한다.

```python
from fastapi import BackgroundTasks


@router.post("/users", status_code=201)
def create_user(
    payload: UserCreate,
    background: BackgroundTasks,
    service: UserServiceDep,
):
    user = service.create(payload)
    background.add_task(send_welcome_email, user.email)
    return UserRead.model_validate(user)


def send_welcome_email(email: str) -> None:
    # SMTP 호출 또는 외부 메일 API
    ...
```

응답이 클라이언트로 *먼저* 나가고, `send_welcome_email`이 그 뒤에 돈다. 사용자가 가입 폼에서 기다리는 시간이 짧아진다. Spring `@Async` 어노테이션의 *체감*과 거의 같다.

장점은 셋이다. 추가 인프라가 없다. 의존성이 가볍다. 학습 비용이 0에 가깝다.

단점도 셋이다. *같은 프로세스*에서 돈다 — 워커가 죽으면 작업이 사라진다. *재시도·결과 추적이 없다*. *워커의 메모리·CPU를 점유*해서 처리량을 깎는다.

FastAPI 공식 문서와 ARQ/Celery 비교 글이 한 줄로 정리한다 (저자의 영문 표현을 옮긴 한 줄) — *BackgroundTasks는 같은 이벤트 루프에서 응답이 흐른 뒤 실행된다. 짧고 작은 작업엔 효율적이지만 무거운 백그라운드 연산엔 Celery를 써야 한다.* — Background Tasks 공식 + Medium ARQ 비교 (reference §4.3).

판단 기준 한 줄: **작업이 짧고(<1초), 실패해도 큰 손실이 없고, 트래픽이 가볍다면 `BackgroundTasks`로 충분.** 어느 한 조건이 깨지면 다음 도구로 넘어가자.

### APScheduler — 같은 프로세스 내 스케줄

Spring `@Scheduled(cron="0 0 * * * *")`의 직접 대체다. *같은 FastAPI 프로세스* 안에서 cron 표현으로 작업을 반복 실행한다.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


async def cleanup_expired_sessions():
    # 만료된 세션 삭제 로직
    ...


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(cleanup_expired_sessions, "cron", hour=2)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
```

장점은 *외부 인프라 없이 cron이 돈다*는 것. 단점은 *프로세스가 여럿이면 작업이 중복 실행*된다는 것 — uvicorn 워커가 4개면 같은 작업이 4번 돈다. 이걸 막으려면 *분산 락*(Redis 기반)을 별도로 깔거나, 스케줄러를 *전용 워커 한 개*로 분리해야 한다. 운영 복잡도가 한 단계 올라간다.

판단 기준: **단일 프로세스 배포(또는 단일 leader 워커)에선 깔끔. K8s 다중 replica에선 별도 분리 권장.**

### ARQ — asyncio 친화 분산 큐

ARQ는 Redis 기반의 *asyncio 네이티브* 분산 큐다. FastAPI와 정신적 모양이 잘 맞는다 — 같은 async 호흡 위에서 워커가 동작한다.

```python
# tasks/worker.py
from arq.connections import RedisSettings
import httpx


async def send_slack_notification(ctx, channel: str, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://hooks.slack.com/services/...",
            json={"channel": channel, "text": text},
        )


class WorkerSettings:
    functions = [send_slack_notification]
    redis_settings = RedisSettings(host="redis", port=6379)
```

FastAPI 라우트에선 이렇게 큐에 푸시한다.

```python
# app/notifications/router.py
from typing import Annotated
from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from fastapi import Depends


async def get_arq_pool() -> ArqRedis:
    return await create_pool(RedisSettings(host="redis", port=6379))


# 4·5·6장 패턴대로 타입 별칭으로 묶어두자
ArqDep = Annotated[ArqRedis, Depends(get_arq_pool)]


@router.post("/notify")
async def notify(payload: NotifyRequest, arq: ArqDep):
    job = await arq.enqueue_job("send_slack_notification", payload.channel, payload.text)
    return {"job_id": job.job_id}
```

워커는 별도 프로세스로 띄운다.

```bash
$ uv run arq tasks.worker.WorkerSettings
```

장점은 셋이다. 워커 프로세스 분리로 *FastAPI 워커의 메모리·CPU 자유*. Redis로 *잡 영속화* — 워커가 죽어도 잡은 살아 있다. *재시도·결과·진행 상황 추적*이 내장.

단점은 둘. Redis 의존성이 추가된다. 라이브러리 성숙도가 Celery만큼은 아니다 — 큰 커뮤니티의 시간은 Celery가 더 길다.

### Celery — 성숙한 분산 큐

Python 진영의 *전통 강자*. RabbitMQ/Redis 위에서 동작하고, Spring + RabbitMQ 조합이 줄 만한 모든 기능 — 우선순위, 라우팅, 결과 백엔드, 분산 락, 비트(Celery beat로 cron) — 을 다 갖춘다.

```python
# tasks/celery_app.py
from celery import Celery

app = Celery("myapp", broker="redis://redis:6379/0")

@app.task
def send_welcome_email(email: str):
    ...
```

FastAPI 라우트에선:

```python
@router.post("/users")
def create_user(payload: UserCreate, service: UserServiceDep):
    user = service.create(payload)
    send_welcome_email.delay(user.email)   # 큐에 푸시
    return UserRead.model_validate(user)
```

장점: 가장 검증된 분산 큐. 운영 지식이 인터넷에 풍부. 큰 트래픽·복잡한 워크플로우에 강함.

단점: *asyncio와 결이 안 맞는다* — Celery 워커는 기본이 동기 코드 가정이다. FastAPI의 async 호흡과 코드 스타일이 갈린다. 학습 곡선이 가파르다 — broker/result backend/queue 설정이 만만치 않다.

### 어느 시점에 무엇으로 옮기나 — 단계적 마이그레이션

손에 익혀두자. 백그라운드 작업은 *처음부터 분산 큐를 짤 필요가 없다*. 시작은 가볍게, 부하가 늘면 단계적으로 옮긴다.

| 단계 | 도구 | 트래픽 가정 |
|---|---|---|
| 1 | `BackgroundTasks` | 분당 수~수십 건, 짧은 작업 |
| 2 | `BackgroundTasks` + APScheduler | + 정기 cron 작업 추가 |
| 3 | ARQ (또는 Celery) | 분당 수백 건 이상, 또는 작업이 무거워졌을 때 |
| 4 | ARQ + 전용 워커 노드 | 본격 분산, 여러 종류의 큐 |

예제 한 줄로 흐름을 박아두자. *이메일 발송*을 가벼운 단계 1로 시작해, 트래픽이 늘었을 때 단계 3으로 옮기는 그림이다.

```python
# 단계 1 — BackgroundTasks
@router.post("/users")
def create_user(payload, background: BackgroundTasks, ...):
    user = service.create(payload)
    background.add_task(send_welcome_email_sync, user.email)
    return ...


# 단계 3 — ARQ로 옮긴 뒤
@router.post("/users")
async def create_user(payload, arq: ArqDep, ...):
    user = await service.create(payload)
    await arq.enqueue_job("send_welcome_email", user.email)
    return ...
```

라우트 변경은 *한 줄*이다 — `background.add_task(...)` → `await arq.enqueue_job(...)`. 함수 본체는 거의 그대로 옮겨간다. *처음부터 ARQ로 짤 필요가 없는 이유*가 여기 있다 — 단계 옮김이 가볍다. 12장 통합 프로젝트의 Slack 알림이 *이걸 전제로* 가벼운 케이스를 다룬다.

판단 기준 한 줄을 박아두자. **트래픽·작업 크기·신뢰성 요구가 어느 한 축에서 어긋나면, 그때 다음 도구로 옮긴다.** 미리 가지 말자.

## 한 호흡으로 정리

8장에서 받아갈 것을 한 번에 묶어두자.

- **모델 비교:** WSGI/ASGI = Spring MVC/WebFlux. FastAPI는 *WebFlux가 기본값인 Spring*에 가깝다. 다만 `async def`/`def`를 섞어 쓸 수 있는 유연함이 더 있다.
- **이벤트 루프:** 한 스레드 안의 코루틴 스케줄러. `await` 한 곳이 *제어권 반납 지점*. `await`이 없으면 다른 코루틴이 진행하지 못한다.
- **함정:** *async 안에 sync를 섞으면 더 느리다*. 한 사례 보고는 sync 600 req/s vs async + sync DB 550 req/s를 적어 둔다. 세 가지 유형(sync DB, CPU 무거운 연산, 블로킹 라이브러리)을 분리해서 보자.
- **안전 패턴:** `asyncio.to_thread`/`run_in_threadpool`로 sync 호출을 격리하거나, *판단 의심스러우면 `def` 라우트로* 두자 — FastAPI가 자동으로 스레드풀에서 굴린다.
- **GIL과 PEP 703:** I/O-bound는 GIL이 잘 풀린다. CPU-bound는 별도 워커/멀티프로세스. PEP 703의 free-threaded Python은 2026년 현재 *experimental* — 프로덕션 표준은 여전히 *프로세스 다중화*다.
- **Kotlin 코루틴 비교:** `suspend fun` ↔ `async def`의 정신은 같다. 차이는 셋 — structured concurrency(`coroutineScope` ↔ `asyncio.TaskGroup`), 디스패처 명시성(Kotlin 명시, Python 묵시), 진입 다리(`runBlocking` ↔ `asyncio.run`).
- **백그라운드 작업:** `BackgroundTasks` → APScheduler → ARQ → Celery의 4단 계단. *미리 가지 말고 단계로 올라가자*. 라우트 한 줄 갈아 끼우는 비용으로 충분히 옮길 수 있다.

여기까지 오면 한 가지 감각이 든다. *async가 마법이 아니라, 도구함의 한 칸*이라는 감각이다. *언제 async를 쓰고 언제 sync로 두는지*가 본인 손에 잡힌다. WebFlux를 진지하게 써본 손이라면 이 감각은 그저 새로 쓰는 게 아니라 *옮겨 적는* 일이다.

다음 장은 *예외와 관측성*이다. `@ControllerAdvice`가 떠받쳐 주던 자리에 `@app.exception_handler`가 들어서고, Spring Boot Actuator가 한 줄로 깔아 주던 health/metrics/trace를 우리는 어떻게 손으로 조립하는지 보자. 본 장에서 만든 async 라우트들이 *관측성의 첫 시험대*다 — request_id가 코루틴을 넘나들 때 어떻게 따라다니는지가 9장의 한 자리다.
