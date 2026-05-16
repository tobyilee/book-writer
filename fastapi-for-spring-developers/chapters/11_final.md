<!-- 개정: 2026-05-16 라운드 1 가디언 피드백 반영 (Should 1: 세 인용 형식을 5·6·8·9장 라운드 2 패턴(평어체 도입 + *번역 명시* + reference 출처)으로 통일; Should 2: §35 워커 공식 출처 정밀화) -->

# 11장. 배포·운영 — Tomcat에서 Uvicorn + Gunicorn + 컨테이너로

`java -jar app.jar`. 이 한 줄로 Spring Boot 서비스가 띄워진다. 안에 Tomcat이 들어 있고, 스레드풀이 알아서 잡히고, 클래스패스도 jar 안에 다 들어 있다. CI에서 빌드한 jar 하나를 EC2든 K8s든 어디든 *던지면 그만*이다. 이 단순함이 Spring Boot가 한 시대를 가져간 진짜 이유 중 하나다.

이제 같은 일을 FastAPI로 한다고 해보자. 손에 잡히는 그림이 한 번에 안 떠오른다. ASGI 서버는 *Uvicorn*인데, 그게 단독으로 운영 환경에 충분한가? *Gunicorn*은 어디서 어떻게 끼우는가? Tomcat의 스레드풀과 가장 닮은 자리는 어디인가? 컨테이너로 묶을 때 워커 수는 몇 개로 잡는가? Docker 이미지 안에 `uv`는 들어가야 하나, 빠져야 하나? 질문이 줄줄이 늘어선다. 살짝 난감하다.

핵심 질문은 둘이다. **`java -jar` 한 줄의 단순함이 사라진 자리에 무엇을 놓는가?** 그리고 **워커 수, 메모리, 컨테이너 전략은 어떻게 잡는가?** 답을 한 줄에 미리 흘려두자면 — *컨테이너 한 개 = Uvicorn 한 프로세스*가 K8s 시대의 기본형이다. 그 위에 Dockerfile·시크릿·헬스·메모리 모니터링이 한 층씩 쌓인다. 9장에서 깔아둔 관측성·헬스 엔드포인트가 11장에서 *진짜 운영 도구*로 받아진다. 한 발 한 발 함께 가보자.

## Uvicorn 단독 vs Gunicorn + Uvicorn worker

먼저 Tomcat의 자리를 떠올려보자. 한 JVM 프로세스 안에 스레드풀이 있고, 요청이 들어오면 스레드 하나가 잡혀서 *블로킹 IO*를 처리한다. 스레드 수는 보통 200~400개, JVM 프로세스는 *하나*다. 한 프로세스 안에서 멀티스레드로 수평 확장이 일어난다.

Python은 그 그림이 *조금* 다르다. **GIL** 때문이다. 한 프로세스 안에서 *동시에 실행되는 Python 바이트코드는 한 개*다(8장에서 깐 약속). 스레드를 200개 띄워도 *동시 실행되는 Python 코드는 하나*뿐이다. 그래서 Python 진영의 수평 확장은 *프로세스 단위*다. 워커 *프로세스*를 여러 개 띄우고, OS가 그 프로세스들에 요청을 분산시킨다.

여기서 두 도구가 같이 등장한다. **Uvicorn**은 *ASGI 서버* — Tomcat의 자리에 가장 가깝다. uvloop과 httptools 위에서 *한 프로세스의 이벤트 루프*로 비동기 요청을 처리한다. **Gunicorn**은 *프로세스 매니저* — 여러 워커 프로세스를 띄우고 죽은 워커를 살리는 역할이다. Spring 진영에는 Gunicorn의 정확한 평행 자리가 없다(Tomcat 자체가 둘 다 한다). 그래서 둘을 합쳐 쓰는 패턴이 흔히 다음과 같이 등장한다.

```bash
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 4 \
  -b 0.0.0.0:8000
```

`-k uvicorn.workers.UvicornWorker`가 Gunicorn에게 *워커를 Uvicorn 방식으로 만들라*고 지시한다. `-w 4`가 워커 *수*다. Gunicorn이 4개의 Uvicorn 프로세스를 띄우고, 각 프로세스가 *자기 이벤트 루프*를 돌린다. 요청은 OS 소켓에 들어와 4개 워커 중 *준비된* 워커가 받는다(소위 *pre-fork 모델*).

Medium iklobato의 글이 두 도구의 자리를 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *Gunicorn이 프로세스 관리(병렬성)를, Uvicorn이 async 요청 처리(동시성)를 담당한다. `-k uvicorn.workers.UvicornWorker` 플래그로 Gunicorn(WSGI 서버)이 Uvicorn(ASGI) 워커를 관리한다.* — Medium, "Mastering Gunicorn and Uvicorn" (reference §4.5).

Tomcat 한 프로세스 안의 *스레드풀 200개*가, FastAPI에서는 *프로세스 4개 × 이벤트 루프*로 옮겨졌다. 표현이 다르지만 결국 같은 일이다 — *동시 요청을 흘려보낼 통로*를 늘리는 것. 다만 *통로의 단위*가 스레드에서 프로세스로 바뀌었다.

## 워커 수 공식 — 어디서부터 시작하고 어디서 멈출지

워커 수를 몇 개로 잡을지가 다음 질문이다. 인터넷에는 두 공식이 떠다닌다.

- **Sync 워커:** `(2 × CPU) + 1` — 전통적인 Gunicorn 공식. 워커가 *블로킹 IO*에 자주 묶이므로 CPU 수보다 약간 더 많이 띄운다.
- **Async Uvicorn 워커:** *CPU 수와 같게.* 단일 스레드에서 *동시 요청을 효율적으로 처리하므로* 컨텍스트 스위치를 최소화하기 위해 워커 수를 CPU 수와 같게 둔다 — Medium iklobato의 같은 글에서 짚은 워커 공식이다 (reference §4.5, *async uvicorn 워커: CPU 수와 같게*).

8장에서 익힌 호흡을 들고 와보자. 라우트가 *대부분 async + 비동기 IO*라면 두 번째 공식을 따른다. 라우트에 *sync def + 블로킹 호출*이 섞여 있다면 — FastAPI가 자동으로 스레드풀에서 실행하지만 — 첫 번째 공식이 안전하다. 모르겠으면 *CPU 수와 같게* 두고 부하 테스트로 조정하는 게 보통이다.

여기서 한 가지를 짚자. *공식이 절대값이 아니다.* 한 워커의 메모리가 *200MB*라면 8 워커는 *1.6GB*다. 컨테이너의 메모리 limit이 1GB라면 OOM-Killer가 워커를 *번갈아 죽이는 사이클*이 시작된다. 끔찍한 일이다. 워커 수는 *CPU만 보고* 정하면 안 된다 — *메모리 한도 / 워커당 메모리*도 함께 봐야 한다. 부하 테스트에서 워커 수를 1씩 줄여보며 안정점을 찾는 편이 낫다.

## Kubernetes에선 컨테이너당 단일 프로세스

여기까지 따라온 다음 한 가지 *전환점*이 등장한다. Gunicorn으로 한 컨테이너에 4 워커를 띄우는 패턴은 *VM 시대*의 호흡이다. K8s 시대로 오면 그림이 살짝 바뀐다.

FastAPI 공식 deployment 문서가 이 자리를 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *Kubernetes에서는 워커를 쓰지 말고 컨테이너당 단일 Uvicorn 프로세스를 권장한다*. 이유는 *K8s replica가 곧 워커 역할*이기 때문이다 (reference §4.5).

K8s의 Deployment는 *replicas 4*를 박으면 컨테이너 *4개*가 뜬다. 각 컨테이너 안에 Uvicorn *1개*. OS 소켓 분산 대신 *Kubernetes Service*가 들어와 부하 분산을 한다. 컨테이너가 죽으면 *kubelet이 살린다.* Gunicorn이 하던 일을 K8s가 *컨테이너 단위*로 다시 하는 셈이다.

이게 더 좋은가? 두 가지 이유로 그렇다. **첫째**, 한 워커가 메모리 누수로 부풀어 올라도 *그 컨테이너*만 OOM된다. 옆 워커들은 영향을 안 받는다. K8s가 알아서 죽이고 살린다. **둘째**, 메트릭이 *컨테이너 단위*로 깔끔하게 잡힌다. 한 컨테이너의 CPU·메모리·요청 수가 그대로 한 워커의 시그널이다. 디버깅이 한 단계 더 깨끗해진다.

VM이나 EC2에 직접 띄우는 환경이라면 Gunicorn + 4 워커. K8s라면 *Uvicorn 단독 + replicas로 수평 확장*. 두 패턴 모두 답이고, *환경이 무엇이냐*가 답을 정한다. 책에서는 K8s 패턴을 기본으로 가져간다 — 2026 현재 한국에서도 대부분의 새 프로젝트가 그쪽이다.

```dockerfile
# K8s 패턴: Uvicorn 단독, 워커 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

이 한 줄이 11장의 출발점이다. 그 위에 Dockerfile의 *몸통*을 쌓아 올린다.

## Dockerfile — multi-stage, `uv sync --frozen`, non-root

이제 Dockerfile을 짜보자. 2장에서 깔아둔 `uv`와 `pyproject.toml`을 그대로 활용한다. 가장 많이 쓰는 패턴은 *multi-stage 빌드*다 — 빌드 단계의 도구를 *실행 이미지에 안 가져가는* 방식이다.

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder

# uv를 빌드 단계에만 설치
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# 의존성 해상도와 설치를 lock 파일 기반으로
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 애플리케이션 소스 복사
COPY app/ ./app/
RUN uv sync --frozen --no-dev

# ============================================================
FROM python:3.13-slim AS runtime

RUN useradd -m -u 1000 -s /bin/bash appuser
WORKDIR /app

# 빌더에서 .venv만 가져옴
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/app /app/app
ENV PATH="/app/.venv/bin:${PATH}"

USER appuser
EXPOSE 8000

# 그레이스풀 셧다운을 위해 init을 PID 1로
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
```

조각조각 짚어보자.

**`--frozen`은 *lock 파일 그대로* 설치한다는 약속이다.** 빌드 시점에 `uv.lock`이 최신이 아니면 *실패한다*. Maven의 `--strict-locks`나 Gradle 잠금과 같은 자리다. *프로덕션 빌드에서 의존성이 조용히 바뀌는 사고*를 막는다. 2장에서 깐 `uv.lock`이 여기서 본 모습을 드러낸다.

**`--no-dev`로 dev 의존성은 들이지 않는다.** pytest·ruff·mypy는 컨테이너에 들어갈 이유가 없다. 이미지 크기와 공격 면을 함께 줄인다.

**`UV_COMPILE_BYTECODE=1`은 `.pyc` 파일을 미리 만들어둔다.** 컨테이너 콜드 스타트가 한 박자 빨라진다. K8s 환경에서 *처음 뜨는 Pod*에서 의미가 있다.

**Non-root 유저(`appuser`).** Spring Boot의 jar 한 줄 띄우기와 다르게, 컨테이너는 *기본이 root*다. 그대로 두면 *컨테이너 탈출 시* 호스트 root 권한이 새어 나간다. K8s `PodSecurityPolicy`/`PodSecurity` 표준이 *non-root를 요구한다*. 컨테이너에 사용자 한 명을 만들고 `USER`로 전환하는 두 줄이 그 표준을 채운다.

**`--proxy-headers --forwarded-allow-ips=*`.** 다음 절에서 자세히 본다.

## 그레이스풀 셧다운 — `lifespan` 컨텍스트와 signal

Spring Boot에는 `@PreDestroy` 어노테이션과 그레이스풀 셧다운 옵션이 박혀 있다. K8s가 Pod에 `SIGTERM`을 보내면 *진행 중인 요청을 마치고* 깔끔하게 종료된다. FastAPI에도 같은 자리가 있다 — `lifespan` 컨텍스트다.

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시: 자원 초기화
    await db_pool.connect()
    await redis_pool.connect()
    yield
    # 종료 시: 자원 정리
    await db_pool.close()
    await redis_pool.close()

app = FastAPI(lifespan=lifespan)
```

`yield` 위가 *시작*, 아래가 *종료*다. Spring의 `@PostConstruct`/`@PreDestroy` 한 쌍과 같은 자리지만 — *생성자/소멸자가 아니라 컨텍스트 매니저*로 표현된다. 6장의 트랜잭션 패턴과 같은 결이다 — *들여쓰기로 시작과 끝이 한눈에 보인다.*

K8s가 Pod를 죽일 때의 흐름을 따라가보자. 첫째, `SIGTERM`을 보낸다. 둘째, *terminationGracePeriodSeconds*(기본 30초) 동안 기다린다. 셋째, 그래도 살아 있으면 `SIGKILL`. Uvicorn은 `SIGTERM`을 받으면 *새 요청 받기를 멈추고, 진행 중 요청이 끝나기를 기다리고, lifespan의 종료 부분을 실행하고, 종료된다*. 정확히 우리가 원하는 그림이다.

여기서 한 가지 함정. 컨테이너 안에서 *PID 1 프로세스*에 신호 처리 이슈가 있다. Python 프로세스가 PID 1이면 일부 신호(`SIGINT` 등)가 *기본 핸들러로 무시*될 수 있다. 운영 환경에서는 `tini` 같은 *최소 init*를 PID 1으로 두는 게 안전하다.

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends tini && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
```

`tini`가 PID 1로 들어가 신호를 *uvicorn에 정확히 전달*한다. K8s 1.20+ 환경이라면 컨테이너의 `restartPolicy`와 `terminationGracePeriodSeconds`를 함께 봐두자. 한 번 머리에 새겨두는 게 좋다.

## 시크릿 관리 — K8s Secret을 BaseSettings로 받는 파이프라인

7장에서 `pydantic-settings`를 도입했다. JWT 비밀 키를 `.env` 또는 환경 변수에서 받아 `BaseSettings`로 검증하는 그 자리다. 11장에서는 그 입력이 *K8s Secret*에서 오는 운영 환경의 파이프라인만 다룬다.

```python
# app/core/settings.py (7장에서 이미 도입)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    jwt_secret: str
    db_url: str
    redis_url: str
    sentry_dsn: str | None = None

settings = Settings()
```

K8s에서 Secret을 만들고 컨테이너에 *환경 변수*로 주입한다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-api-secrets
type: Opaque
stringData:
  APP_JWT_SECRET: "real-secret-here"
  APP_DB_URL: "postgresql+asyncpg://user:pass@db:5432/orders"
  APP_REDIS_URL: "redis://redis:6379/0"
  APP_SENTRY_DSN: "https://abc@sentry.io/123"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-api
spec:
  replicas: 4
  template:
    spec:
      containers:
        - name: order-api
          image: registry.example.com/order-api:v1.2.3
          envFrom:
            - secretRef:
                name: order-api-secrets
          # ... 헬스 체크는 다음 절에서
```

`envFrom: secretRef`로 Secret의 모든 키가 *환경 변수로* 주입된다. 컨테이너 안의 `pydantic-settings`가 `APP_` prefix로 그 변수들을 *자동으로* 읽어 `Settings` 인스턴스로 검증한다. K8s Secret → 환경 변수 → BaseSettings 세 단계가 *깔끔한 파이프라인*으로 이어진다.

여기서 Spring 출신이 의식해야 할 한 가지. Spring의 `@Value("${...}")`는 *런타임 lookup*이라 키가 없거나 잘못된 타입이면 *부팅이 늦은 자리에서* 터진다. `pydantic-settings`는 *부팅 시 검증*이다. K8s Secret에서 한 키가 빠지거나 타입이 잘못되면 *Pod가 즉시 죽는다*. 처음에는 *이런 거 갑자기 죽나?* 싶지만 — 실은 *늦게 발견되는 것보다 빨리 발견되는 게 안전*하다. 6장 명시성 통주저음이 11장 시크릿에서도 같은 결로 흐른다.

## 메모리 누수 — 180MB가 600MB로 기어 올라가는 자리

11장의 가장 *어두운* 절을 짚자. 메모리 누수다. 1장의 약점 지도에서 예고한 자리다.

Medium "FastAPI vs Spring Boot: I tested both for 6 months in production"의 한 줄을 옮겨보자 (저자의 영문 표현을 옮긴 한 줄) — *한 회사 사례에서 FastAPI 서비스의 메모리가 180MB에서 시작해 며칠 사이 600MB까지 기어 올라갔다* (reference §3.2-2).

먼저 한 가지 못 박고 가자. 이건 *한 회사의 경험치*다. 모든 FastAPI 서비스가 메모리 누수에 시달린다는 일반화가 아니다. 하지만 *왜 그런 일이 일어나는가*는 일반적이다 — Python에는 JVM 같은 *성숙한 메모리 프로파일링 도구 체인*이 부족하다. JVM이라면 `jmap`·`jstat`·VisualVM·MAT가 즉시 손에 잡힌다. Python 진영에는 그 자리에 *작은 도구 세 개*가 있다. 각자 다른 자리에서 빛난다.

**`tracemalloc` — 표준 라이브러리로 시작하는 자리.**

```python
import tracemalloc

tracemalloc.start()
# ... 한참 운영 ...
snapshot1 = tracemalloc.take_snapshot()
# ... 더 운영 ...
snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, "lineno")
for stat in top_stats[:10]:
    print(stat)
```

표준 라이브러리에 들어 있어서 *추가 설치가 없다*. 두 스냅샷을 비교해 *어디서 메모리가 늘어났는지* 라인 단위로 본다. 처음 의심이 들 때 가볍게 켜보는 자리다. 단점은 *오버헤드*가 작지 않다는 것 — 운영 환경에서 *상시* 켜두기엔 부담스럽다.

**`memray` — Bloomberg가 만든 본격 프로파일러.**

```bash
uv run memray run -o output.bin -m uvicorn app.main:app
# 부하를 흘려넣은 뒤 종료
uv run memray flamegraph output.bin
```

flamegraph로 *메모리 할당의 호출 스택*을 그려준다. JVM의 MAT(Memory Analyzer Tool)와 가장 닮은 자리다. *어느 함수가 얼마나 할당했는지*가 한눈에 잡힌다. 단점은 *프로세스를 종료해야 리포트가 나온다*는 점이라 운영 컨테이너에 상시 켜두긴 어렵다. *로컬 재현*이나 *스테이징 환경*에서 빛난다.

**`py-spy` — 운영 환경의 살아 있는 프로세스를 들여다보는 자리.**

```bash
# 운영 컨테이너에 들어가서
py-spy dump --pid 1     # 스택 트레이스
py-spy top --pid 1      # top 같은 실시간 뷰
```

핵심은 *프로세스를 재시작하지 않고* 들여다본다는 것. JVM의 `jstack`과 같은 자리다. *지금 어느 함수에서 시간이 가고 있는지*가 실시간으로 보인다. CPU 누수에 더 강하고, 메모리 분석은 약하지만 — *진짜 이상한 일이 일어나는 컨테이너*에 들어가서 한 줄 찍을 때 가장 빛난다.

세 도구 모두 JVM의 *한 도구로 다 되는* 그림에 비해 작고 분산돼 있다. 찜찜한 자리다. 하지만 *세 도구의 자리를 각자 익혀두면* — `tracemalloc`으로 가벼운 의심, `memray`로 본격 분석, `py-spy`로 운영 환경 실시간 — 세 개를 합쳐 JVM 도구 체인의 *기능적 빈자리*를 메운다. 손이 한 번씩 더 가지만 손길이 곧 안전망이다.

권장하는 운영 패턴 한 가지. **컨테이너 메트릭의 `container_memory_working_set_bytes`를 Prometheus로 항상 보고** + **OOM kill 이벤트를 알람**으로 받자. 9장에서 깐 Prometheus 인프라가 *그대로* 메모리 모니터링에도 쓰인다. *부풀어 오르기 전*에 알람이 오면 `memray`나 `py-spy`를 들고 *천천히* 분석할 시간이 생긴다.

## `--proxy-headers` — 로드 밸런서 뒤의 진짜 IP

운영 환경에서는 Uvicorn 앞에 *로드 밸런서*가 거의 항상 있다. K8s Ingress, ALB, Nginx 같은 것들. 이 *프록시*가 사이에 끼면 — *클라이언트의 진짜 IP가 사라진다*. Uvicorn이 보는 IP는 *프록시의 IP*다. 로깅·rate limit·지오 IP 같은 자리에서 곤란해진다.

표준 해결책은 *프록시가 `X-Forwarded-For`·`X-Forwarded-Proto` 헤더에 진짜 정보를 박아 보내고*, *서버는 그 헤더를 읽어* 진짜 IP를 복원하는 거다. Uvicorn은 그 동작을 *명시적으로 켜야* 한다.

```bash
uvicorn app.main:app --proxy-headers --forwarded-allow-ips="*"
```

`--proxy-headers`가 헤더 *해석*을 켜고, `--forwarded-allow-ips`가 *어느 IP의 프록시를 신뢰할지*를 정한다. K8s 내부 클러스터처럼 *모든 트래픽이 신뢰된 프록시를 거친다*는 가정이라면 `*`로 충분하다. 외부에 노출된 환경이라면 *프록시의 정확한 IP 대역*을 박는 편이 낫다 — 안 그러면 *클라이언트가 직접 `X-Forwarded-For`를 위조*해 진짜 IP를 속일 수 있다. 보안 관점에서 끔찍한 일이다.

라우트 안에서는 평소처럼 `request.client.host`를 쓰면 *복원된 진짜 IP*가 잡힌다. Spring의 `request.getRemoteAddr()`이 `RemoteIpValve`로 자동 복원되던 자리와 같다. Uvicorn은 *그 valve를 명시적으로 켜는 두 옵션*으로 표현한다.

## 헬스 체크와 readiness probe — 9장 엔드포인트를 K8s manifest로 받음

9장에서 깐 `/healthz`와 `/readyz`가 이 자리에서 *진짜 운영 도구*로 받아진다. K8s Deployment manifest에 두 probe를 명시한다.

```yaml
spec:
  template:
    spec:
      containers:
        - name: order-api
          image: registry.example.com/order-api:v1.2.3
          envFrom:
            - secretRef:
                name: order-api-secrets
          ports:
            - containerPort: 8000
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 2
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
```

**`livenessProbe`는 `/healthz`** — 9장에서 *프로세스가 살아 있는가만* 보는 자리. 실패하면 K8s가 *컨테이너를 재시작*한다. DB 의존성을 *여기에 넣지 않는다*. 9장에서 강조한 함정이다 — DB가 잠시 끊겼는데 컨테이너가 재시작되면 *연쇄 재기동*이 시작된다.

**`readinessProbe`는 `/readyz`** — *지금 요청을 받을 준비가 됐는가*. 실패하면 K8s가 *서비스 라우팅에서 뺀다*. 컨테이너는 살아 있지만 요청이 안 들어온다. DB 핑·외부 의존성을 *여기서* 확인한다.

**`resources.requests/limits`.** Spring Boot의 JVM 힙 설정(`-Xmx`)과 비슷한 자리. requests는 *스케줄러가 보장하는 최소*고, limits는 *못 넘는 천장*이다. limits을 *워커당 메모리의 1.5~2배*로 잡는 게 보통이다 — 메모리 누수가 시작될 때 *알람이 울릴 여유*를 둔다. 그 여유 안에서 `py-spy`나 `memray`를 들고 분석한다.

여기까지 오면 Spring Boot의 `java -jar`가 한 줄로 하던 일이 *Dockerfile 30줄 + K8s manifest 40줄*로 풀려나왔다. 손이 더 많이 가지만 *어디가 어떻게 동작하는지*가 코드 위에 다 드러난다. 6장 명시성 통주저음이 11장 배포에서도 같은 결로 흐른다 — *자동의 자리에 명시가 들어선다.*

## CI/CD 스켈레톤 — GitHub Actions 한 자락

마지막으로 짧게 CI 파이프라인 한 자락. 2장의 lint·test·build 명령들을 GitHub Actions에 박는 자리다.

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv sync --frozen --all-extras
      - name: Lint
        run: |
          uv run ruff check .
          uv run ruff format --check .
      - name: Type check
        run: uv run mypy app
      - name: Test
        run: uv run pytest -v --cov=app --cov-report=xml

  build:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: registry.example.com/order-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

`uv sync --frozen`이 CI에서도 같은 결이다 — *lock 파일의 의존성 그대로*. `cache-from`/`cache-to`로 Docker 빌드 레이어 캐시를 GitHub Actions가 관리한다. 빌드 시간이 *재시도마다* 짧아진다. 사내 환경이라면 *컨테이너 이미지 스캐닝*과 *Helm 배포 스텝*을 더해야 하지만, 그 자리는 사내 사정마다 다르다. 이 책에서는 *공통의 뼈대*만 보여두고 사내 색깔은 운영팀과 함께 짠다.

## 한 호흡으로 정리

머리에 박혀야 할 건 셋이다.

**첫째, K8s 시대의 기본형은 *컨테이너 한 개 = Uvicorn 한 프로세스*다.** VM·EC2 시대에는 Gunicorn이 *4 워커*를 띄워 OS 분산을 받았다. K8s에서는 *replicas 4*가 그 자리를 가져간다. 컨테이너가 부풀거나 죽어도 *그 컨테이너만* 영향을 받고, 메트릭도 *컨테이너 단위*로 깔끔하게 잡힌다. 워커 수 공식은 *환경이 무엇이냐*가 답을 정한다. 모르겠으면 *CPU 수와 같게* 두고 부하 테스트로 조정하자.

**둘째, Dockerfile은 `uv sync --frozen` + multi-stage + non-root가 표준이다.** 2장에서 깐 `uv.lock`이 *프로덕션 빌드에서 의존성이 조용히 바뀌는 사고*를 막는다. multi-stage로 빌드 도구를 *실행 이미지에 안 가져가고*, non-root 유저로 *컨테이너 탈출 시 호스트 권한 노출*을 막는다. PID 1에는 `tini` — Python 프로세스의 신호 처리 이슈를 피하는 자리다. `lifespan` 컨텍스트가 Spring의 `@PostConstruct`/`@PreDestroy` 한 쌍을 *들여쓰기 한 블록*으로 표현한다.

**셋째, JVM 도구 체인의 빈자리는 *세 도구로 나눠* 메운다.** `tracemalloc`(표준 라이브러리, 가벼운 의심), `memray`(본격 분석, 스테이징), `py-spy`(운영 환경 실시간). 1장에서 예고한 *180MB → 600MB* 사례는 *한 회사의 경험치*다 — 일반화는 금물이지만, *Python 진영의 도구가 작게 분산돼 있다는 사실*은 짚어둘 만하다. Prometheus의 `container_memory_working_set_bytes`를 항상 보고 OOM kill 이벤트를 알람으로 받자 — 부풀어 오르기 전에 알람이 오면 *천천히* 분석할 시간이 생긴다. 9장의 `/healthz`·`/readyz` 분리는 K8s livenessProbe·readinessProbe로 *manifest에서* 받아진다 — 의존성 끊김에 *연쇄 재기동*하지 않도록 하는 안전망이다.

다음 장은 통합 프로젝트다. 1~11장에서 깐 모든 조각이 *사내 태스크 관리 API + Slack 알림 봇*이라는 한 도메인 안에서 *함께 동작*한다. 3장의 Pydantic 모델, 4장의 Depends + APIRouter, 5장의 SQLAlchemy 도메인 폴더, 6장의 트랜잭션, 7장의 JWT + scope, 8장의 BackgroundTasks·SSE, 9장의 도메인 예외·메트릭, 10장의 TestClient·Testcontainers, 그리고 11장의 Dockerfile·K8s manifest까지. 책을 덮을 때쯤 손에 *프로덕션급 FastAPI 템플릿 한 벌*이 잡힌다. 자동의 자리에 명시가 들어선 11권의 기둥이 12장에서 한 그림으로 모인다 — 손에 익은 회로를 들고 다음으로 가자.
