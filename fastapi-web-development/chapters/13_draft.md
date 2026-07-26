# 13장. 컨테이너와 클라우드 — 어디에, 몇 개의 프로세스로 올릴 것인가

파이프라인이 초록불이라고 해보자. 12장의 워크플로가 린트와 타입과 테스트를 지나 이미지를 굽는 데까지 갔고, 그 이미지를 어딘가에 올렸다. 그런데 트래픽이 조금 늘자 응답이 밀리기 시작한다.

스프링에서 왔다면 손이 어디로 갈지 안다. 요청 처리 스레드 수를 확인하고 모자라면 올린다. Node였다면 프로세스를 몇 개 띄웠는지부터 봤을 것이다.

여기서는 그 두 질문이 겹쳐 있고, 답이 설정 파일 하나가 아니라 이미지와 매니페스트와 플랫폼 계약에 흩어져 있다. 5장의 두 층은 7장에서 알림이 절반만 도착하는 모습으로, 8장에서 리포트가 네 번 생성되는 모습으로 돌아왔다. 그때마다 "그 숫자는 13장의 몫"이라며 미뤄뒀다. 갚을 차례다.

## 이미지 안에 무엇이 들어가는가

FastAPI 공식 문서는 컨테이너 예시를 pip로 보여주지만, Uvicorn 공식 문서에는 uv 기반 Dockerfile이 통째로 실려 있다. 전략이 한 문장으로 적혀 있다.[^13-1]

> "The key strategy is to install dependencies first, then copy the project files."

의존성을 먼저, 소스는 나중에. 매니페스트만 넣어 의존성을 받아둔 뒤 소스를 얹던 Maven·npm의 그 순서다. 자주 바뀌는 쪽을 뒤에 둬야 캐시가 산다.

그런데 **이 공식 예시를 그대로 베끼면 두 곳에서 물린다.**

하나는 사용자다. 같은 문서가 *"For production, create a non-root user!"*라고 경고해두고도 예시 Dockerfile에는 `USER` 지시어가 없다.[^13-1] 코드만 복사하면 경고는 흘러간다. 비루트 처방의 실제 출처는 uv 문서가 모범 사례로 링크하는 예제 저장소에 있다.[^13-2]

둘은 베이스 이미지다. 예시는 `python:3.12-slim`으로 태그를 박아뒀는데, 공식 `python` 이미지의 기본 배포판은 그사이 Debian trixie 세대로 옮겨갔다. `3.13-slim-trixie`와 `3.13-slim`이 2026-07-16 같은 시각에 갱신됐고 구 `-bookworm` 태그도 나란히 살아 있다.[^13-2] 그러니 **접미사 없는 태그를 믿지 말자.** 배포판까지 적어두면 베이스가 바뀌는 날이 와도 우리가 고른 날에 온다.

이제 12장이 남겨둔 파일을 채우자.

> **📐 저자 설계 —** 아래 Dockerfile은 공식 예시 그대로가 아니라, 위 두 함정을 메우고 빌드 단계를 나눈 이 책의 구성이다.

```dockerfile
# Dockerfile
FROM python:3.13-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM python:3.13-slim-trixie

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
CMD ["uvicorn", "tracker.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

빌더 단계부터 보자. `COPY --from=ghcr.io/astral-sh/uv:latest`가 uv 실행 파일만 남의 이미지에서 꺼내 오고, 세 환경 변수는 uv 문서가 컨테이너용으로 안내하는 것들이다 — 바이트코드를 미리 컴파일하고, 마운트된 캐시라 복사를 쓰고, 개발 의존성은 통째로 뺀다.[^13-2]

`RUN`에 붙은 마운트가 이 파일의 핵심이다. 캐시 마운트는 uv의 다운로드 캐시를 빌드 사이에 살려두고, 바인드 마운트는 두 파일을 복사하지 않은 채 잠깐 빌려 쓴다. 그래서 이 레이어는 락파일이 바뀔 때만 다시 돈다. `--no-install-project`가 의존성만 설치하고, 프로젝트 자신은 소스를 복사한 뒤 두 번째 `uv sync`가 맡는다. `--locked`는 12장의 결정을 그대로 이었다 — 공식 Uvicorn Dockerfile은 `--frozen`을 쓰지만 uv 자신의 예제와 가이드는 `--locked`다.[^13-2]

두 번째 `FROM`이 런타임 이미지를 새로 연다. 빌더의 `/app`을 가져오고 가상 환경의 실행 파일 경로를 `PATH` 앞에 놓는다. uv 자신은 넘어오지 않는다 — 실행에 필요 없는 것을 남기지 않으려고 단계를 나눴다. 다만 빌더의 `COPY . /app`이 저장소 전체를 복사하니 더 줄이려면 `.dockerignore`가 필요하다. 마지막 `CMD`에는 워커 수를 정하는 플래그가 없다.

## Alpine과 slim, 절반만 맞는 이야기

베이스를 고를 때 반드시 나오는 말이 있다. "Alpine은 musl을 쓰니까 wheel을 못 받아서 소스 빌드가 돌고, 그래서 느리다." **출처를 따라가면 이 설명은 반쯤 어긋나 있다.** 공식 `python` 이미지 README의 alpine 문단은 wheel을 말하지 않는다. 런타임 이야기다.[^13-3]

> "it does use musl libc instead of glibc and friends, so software will often run into issues"

"소스 빌드가 실패한다"는 문장은 slim 문단에 있고, 원인은 musl이 아니라 컴파일러 부재다.[^13-3] 서로 다른 두 경고가 뭉쳐진 것이다.

게다가 musl용 wheel의 표준은 이미 있다. PEP 656이 musllinux 태그를 정의했고 2021년 Final이 됐다. 얼마나 배포되는지는 PyPI의 파일 목록에서 태그를 집계하면 알 수 있다. 2026-07-25 조회 기준 pydantic-core 21개, uvloop 16개, httptools 14개, orjson 20개이고, uvloop과 httptools는 manylinux와 개수가 같다.[^13-3]

그러니 정확한 권고는 "Alpine을 쓰지 마라"가 아니다. 기본은 `-slim`으로 가되, Alpine을 쓸 거면 의존성 전체의 musllinux wheel 보유를 확인하자. 남는 위험은 wheel이 아니라 musl과 glibc의 런타임 차이, 그리고 wheel이 없을 때 빌드할 툴체인이 alpine에 없다는 사정이다.

## 컨테이너 하나에 프로세스를 몇 개 띄울 것인가

미뤄둔 숫자다. 그런데 답을 찾으러 공식 문서를 열면 **두 곳이 다른 말을 한다.**

FastAPI 배포 문서는 워커를 늘리는 방법으로 `fastapi run --workers 4 main.py`와 `uv run uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4`를 보여준 뒤, 컨테이너로 넘어가면 방향을 바꾼다.[^13-4]

> "when running on Kubernetes you will probably not want to use workers and instead run a single Uvicorn process per container"

이 문서에는 gunicorn이라는 단어가 **아예 나오지 않는다.** 한편 Uvicorn 자신의 배포 문서는 일반 규칙을 이렇게 연다.[^13-4]

> "As a general rule, you probably want to: ... Run `gunicorn -k uvicorn.workers.UvicornWorker` for production."

같은 페이지 아래쪽에는 `uvicorn.workers`가 폐기 예정이니 별도 패키지 `uvicorn-worker`를 쓰라는 경고가 있다. 실제로 `uvicorn/workers.py`는 임포트하는 순간 `DeprecationWarning`을 던진다.[^13-4]

어느 쪽이 옳은지 여기서 판정하지는 않겠다. **판정보다 중요한 것은 이 불일치가 존재한다는 사실 자체다.** 인터넷에 남은 `gunicorn -k UvicornWorker` 예제들이 전부 낡은 것도 아니라는 뜻이다 — 그 형태는 지금도 서버 쪽 공식 문서 첫 문단에 있다.

대신 선택에 쓸 사실이 하나 더 있다. Uvicorn 문서가 gunicorn 경유 시의 기능 손실을 밝혀뒀다.[^13-4]

> "some options such as `--limit-concurrency` are not yet supported when running with Gunicorn"

5장에서 문 앞의 손잡이라고 불렀던 그 플래그다. **gunicorn을 앞에 세우면 그 손잡이가 사라진다.**

— 여기서부터는 **저자 기준**이다. 이 책은 컨테이너 안에 프로세스를 하나만 둔다. 배포 문서가 K8s에 대해 그렇게 권하고, Uvicorn 공식 Dockerfile도 워커 하나짜리이며 개수는 *"let your orchestration system manage the number of deployed containers"*라고 오케스트레이터에 맡긴다.[^13-1] 무엇보다 gunicorn 경로를 택하면 5장에서 세운 backpressure를 잃는다. 앞 절의 `CMD`에 `--workers`가 없던 이유다. 컨테이너 밖이라면 다르다 — 가상 머신 한 대라면 프로세스를 늘릴 주체가 우리뿐이니 `fastapi run --workers 4 main.py` 쪽이 맞다. **워커 수를 정하는 것은 CPU 개수가 아니라 그 프로세스를 누가 세는가**다. 참고로 `--workers`는 `$WEB_CONCURRENCY`를 기본값으로 읽는다.[^13-4] 2장에서 워커 수를 `Settings`에 넣지 않은 이유가 이것이다 — 이 이름에는 `TRACKER_` 접두사가 붙지 않으니, 설정 클래스로 끌고 들어오면 진실이 두 군데 생긴다.

그러면 레플리카는 몇 개일까. 5장의 두 층이 그대로 산수가 된다. 프로세스 하나에 동기 작업용 스레드 40개, 6장에서 커넥션 풀을 5+10으로 잡았으니 프로세스당 최대 15개. 레플리카가 12개면 데이터베이스가 보는 커넥션은 180개다. **레플리카 수를 정하는 일은 곱셈**이고, 곱해지는 쪽이 우리 것이 아닐 때가 많다.

7장이 남긴 문제도 여기서 답이 난다. WebSocket 연결은 그것을 받은 프로세스에만 붙어 있어서, 레플리카가 여럿이면 알림이 절반만 도착한다. 길은 둘이다. 앞단이 같은 클라이언트를 늘 같은 파드로 보내게 하거나 — 쿠버네티스 서비스에는 `.spec.sessionAffinity`를 `ClientIP`로 두는 설정이 있고 기본값은 `None`이다[^13-6] — 아니면 7장에서 이미 만든 팬아웃을 쓰거나. **어피니티는 연결을 고정하고, 팬아웃은 고정할 필요를 없앤다.** 파드는 언제든 교체되니 이 책은 후자에 남는다.

## 프록시 뒤에서 잃어버리는 주소

컨테이너는 앞단 뒤에 선다. 그러면 클라이언트 주소는 프록시의 것이 되고, HTTPS 요청도 앱에게는 HTTP로 보인다. 해법은 익숙하다 — 프록시가 심어준 헤더를 믿는 것이다. 다만 범위가 좁다. uvicorn이 다루는 헤더는 `X-Forwarded-For`와 `X-Forwarded-Proto` 둘뿐이고, `--proxy-headers`는 기본으로 켜져 있지만 신뢰 목록이 따로 있어 `--forwarded-allow-ips`의 기본값이 `127.0.0.1`이다.[^13-5]

기본값 그대로면 다른 노드의 인그레스가 심은 헤더는 무시된다. 그래서 손쉬운 값을 넣게 된다. **FastAPI 프록시 문서의 예시부터가 `--forwarded-allow-ips="*"`를 쓴다.**[^13-5] 복사해 붙이기 딱 좋은 모양인데, 그 옆에 경고가 붙어 있다.

> "Only trust clients you can actually trust! Incorrectly trusting other clients can lead to malicious actors spoofing their apparent client address"

`*`는 아무나 헤더를 지어내도 믿겠다는 선언이다. 클라이언트 주소로 접근을 제한하거나 감사 로그를 남기고 있다면, 그 값이 요청자가 적어 보낸 값이 된다. 아찔한 조합이다. 프록시가 기존 헤더를 지우고 자기 것만 심는다는 걸 확인했을 때만 쓰자. 1장에서 본 `root_path`가 앞단 경로와 어긋나지 않는지도 함께 확인하자.

## 살아 있는 것과 받을 준비가 된 것

쿠버네티스는 컨테이너에 두 가지를 따로 묻는다. 아직 살아 있는가, 지금 트래픽을 받을 수 있는가. 공식 문서의 처방은 이 둘을 나누라는 것이다.[^13-6]

> "The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available."

liveness가 실패하면 컨테이너가 재시작되고, readiness가 실패하면 그 파드의 주소가 서비스 엔드포인트에서 빠진다. 결과가 이렇게 다르니 같은 판정을 쓰면 곤란하다. 데이터베이스가 흔들릴 때 readiness가 빠지는 건 옳지만, 같은 이유로 앱을 재시작하면 상황만 나빠진다.

**스프링의 헬스 엔드포인트에 익숙하다면 여기서 손이 허공을 짚는다.** 대응하는 기성품이 없어서 상태를 모으는 것도, 둘로 나누는 것도 우리가 만든다. 1장에서 `/healthz`를 미리 정해둔 이유가 이것이다.

> **📐 저자 설계 —** 아래 두 엔드포인트의 판정 내용과 파일 배치는 이 책이 정한 것이다. 프레임워크가 주는 규약이 아니다.

```python
# src/tracker/api/health.py
from fastapi import APIRouter
from sqlalchemy import text

from tracker.deps import SessionDep

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(session: SessionDep) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ready"}
```

1장에서 `main.py`에 달았던 `/healthz`가 여기로 옮겨왔다. 경로는 그대로다 — 이름을 바꾸면 매니페스트와 문서가 어긋난다. 이 엔드포인트는 의존성을 하나도 받지 않아서 이 프로세스가 요청을 받아 응답을 만들 수 있다는 것 외에는 아무것도 주장하지 않는다. 반대로 `/ready`는 6장의 `SessionDep`으로 질의를 한 번 던지고,[^13-6] 실패하면 예외가 3장의 핸들러를 타고 5xx로 나가 준비되지 않았다는 신호가 된다.

매니페스트로 넘어가자. 기본값은 `periodSeconds` 10초, `timeoutSeconds` 1초, `failureThreshold` 3이고 `httpGet`은 200 이상 400 미만이면 성공이다.[^13-6]

> **📐 저자 설계 —** 아래 매니페스트의 골격은 쿠버네티스 공식 예제를 따르고, 숫자와 배치는 이 장의 논의로 이 책이 정한 것이다.

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tracker
  labels:
    app: tracker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tracker
  template:
    metadata:
      labels:
        app: tracker
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: tracker
        image: tracker:latest
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          periodSeconds: 10
          failureThreshold: 6
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 10
          failureThreshold: 3
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]
```

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: tracker
spec:
  selector:
    app: tracker
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

liveness의 `failureThreshold`를 readiness보다 크게 뒀다. 같은 엔드포인트를 쓰되 liveness 쪽 임계를 높이라는 것이 공식 문서가 권하는 형태다.[^13-6] 재시작은 되돌릴 수 없으니 더 확실할 때 하자는 것이다. `image`의 `latest`는 임시 이름이고, 12장의 잡이 커밋 해시로 붙인 태그가 여기 들어온다 — 그 잡의 `push: false`가 뒤집히고 로그인 스텝이 붙는 것이 12장에 되돌려주는 변경이다. 설정은 6장이 정한 `TRACKER_` 환경 변수로 들어온다.

## 끝내는 데도 순서가 있다

배포는 새 파드를 띄우는 일이면서 옛 파드를 죽이는 일이고, 후자가 훨씬 자주 사고를 낸다.

종료 절차는 이렇다. kubelet이 주 프로세스에 `SIGTERM`을 보내고, 유예 시간이 끝나면 `KILL`을 보낸다. `preStop` 훅이 있으면 그 전에 실행하고, `terminationGracePeriodSeconds`의 기본값은 30초다.[^13-7] 여기서 흔히 도는 설명 하나를 고쳐두자. "SIGTERM이 먼저 오고 엔드포인트 제거는 나중이라 순서가 보장되지 않는다"는 말이 있는데, **현재 문서의 서술은 그렇지 않다.** 두 과정은 병렬이다.[^13-7]

> "At the same time as the kubelet is starting graceful shutdown of the Pod, the control plane evaluates whether to remove that shutting-down Pod from EndpointSlice objects"

종료 중인 엔드포인트도 즉시 사라지지 않고 `ready`가 `false`로 남는다.[^13-7] 그럼 `preStop`에 `sleep`을 넣는 관행은 근거가 없을까? 그렇지는 않고, 이유를 정확히 말하면 된다. 동시에 진행되기 때문에, 갱신을 아직 전달받지 못한 로드밸런서나 클라이언트가 있을 수 있다. 몇 초를 쉬는 건 그 전파를 기다리는 시간이지, 순서가 뒤집힐까 봐 드는 보험이 아니다.

이제 8장이 넘긴 요구 조건을 갚자. 그 장은 **백그라운드 태스크의 최악 실행 시간보다 종료 유예 시간이 길어야 한다**고 적고 숫자를 미뤘다. 사슬은 이렇다. `preStop`이 몇 초 쉬고, uvicorn이 `SIGTERM`을 받아 남은 응답과 백그라운드 태스크를 마저 처리하고,[^13-7] lifespan의 `yield` 이후 코드가 자원을 닫는다. 이 전부가 `terminationGracePeriodSeconds` 안에 끝나야 `KILL`을 맞지 않는다. **`terminationGracePeriodSeconds` > `preStop` 대기 + uvicorn의 `--timeout-graceful-shutdown`**, 그래서 위 매니페스트가 30초 대신 60초를 썼다. 주간 리포트가 그 창에 못 들어온다면, 유예를 늘릴 문제가 아니라 8장 말대로 그 일을 요청 수명 밖으로 내보낼 문제다.

한 가지는 확인하지 못했다. **uvicorn `--timeout-graceful-shutdown`의 기본값이 문서에 표기돼 있지 않다.** (사실 확인 필요) 부등식의 오른쪽을 모르면 왼쪽을 정할 수 없으니, 이 값은 비워두지 말고 명시적으로 주자.

덧붙이면, 오토스케일러가 레플리카를 줄일 때 보수적으로 구는 것도 파드 하나가 사라질 때마다 이 사슬이 처음부터 돌기 때문이다.[^13-7]

## 서버리스는 한 단어가 아니다

마지막 질문은 어디에 올리느냐다. 그리고 여기서 **5장의 결론이 한 번 뒤집힌다.**

AWS Lambda 문서는 실행 모델을 이렇게 적어둔다.[^13-8]

> "For each concurrent request, Lambda provisions a separate instance of your execution environment."
> "this execution environment is busy and cannot process other requests."

동시 요청 하나에 실행 환경 하나다. 공식 동시성 식도 `Concurrency = (average requests per second) * (average request duration in seconds)`로 요청 수와 처리 시간만으로 계산된다. Cloud Run은 정반대 계약을 쓴다. 인스턴스 하나가 동시에 받는 요청 수의 기본값이 "80 times the number of vCPUs"이고 최대 1,000이다.[^13-8]

— 여기서부터는 **저자 추론**이다. 벤더가 이렇게 말한 게 아니라 위 사실에서 내가 끌어낸 결론이다. Lambda에서는 `async def`가 처리량을 늘려주지 않는다. 환경 하나가 한 요청만 붙들고 있으니 요청들을 겹칠 기회 자체가 없다. `async`의 이득이 남는 곳은 한 요청 안에서 여러 I/O를 동시에 기다릴 때뿐이다. Cloud Run은 반대다. 인스턴스 하나가 80개를 받으니, I/O를 겹칠 수 있으면 같은 인스턴스가 더 많이 처리하고 그것이 곧 인스턴스 수와 비용이다.

그러니 **"FastAPI를 서버리스에 올린다"를 한 문장으로 묶으면 안 된다.** 5장에서 `def`와 `async def`를 고를 때 깔려 있던 전제 — 한 프로세스가 여러 요청을 동시에 들고 있다 — 가 Lambda에서는 성립하지 않는다. 같은 코드가 플랫폼에 따라 다른 값을 낸다.

기동과 종료도 다르다. Cloud Run은 `PORT`를 주입하고 `0.0.0.0` 바인딩을 요구하며 기본 포트가 8080이라 앞의 Dockerfile이 그대로 붙는다. 대신 **`SIGTERM` 후 10초 뒤에 `SIGKILL`이다.**[^13-8] 쿠버네티스 기본 30초를 전제로 짠 정리 코드가 여기서는 잘린다. 앞 절의 부등식은 플랫폼마다 다시 풀어야 한다.

Lambda에 올리는 방법은 둘이다. Mangum은 앱을 감싸 핸들러로 만드는 파이썬 라이브러리이고, AWS 공식인 Lambda Web Adapter(v1.0.1 / 2026-05 기준)는 확장 바이너리라 코드를 고치지 않는다 — 위에서 구운 이미지를 그대로 올린다. Mangum은 아카이브되지 않았고 릴리스도 있지만 최근 커밋 대부분이 의존성 범프와 문서 수정이니, "죽었다"도 "활발하다"도 아닌 **유지보수 모드**가 정확한 표현이다.[^13-8] `aws-serverless-java-container`를 써봤다면 낯익은 두 갈래다.

PaaS는 짧게 짚자. Fly.io는 `fly.toml`의 `internal_port`가 기본 8080, Render는 `PORT`에 기본 10000이고, 나머지 계약은 확인하지 못했으니 단정하지 않는다. 다만 Railway 공식 FastAPI 가이드는 uvicorn이 아니라 Hypercorn을 쓴다 — **uvicorn이 HTTP/1.1만 지원한다**는 사실과 함께, 플랫폼 문서가 어떤 서버를 전제하는지부터 봐야 한다는 증거다.[^13-9]

밝혀둘 것이 둘 남았다. gunicorn은 26.0.0 / 2026-05 기준으로 메이저가 크게 뛰었는데 **그 변경 내역을 이 책은 확인하지 못했다.** 그 경로를 택한다면 CHANGELOG를 직접 펴보자. lifespan이 워커마다 도는지도 4장에서 밝혔듯 확인하지 못했다. 워커를 늘리는 순간, 기동 코드가 몇 번 도는지가 문제가 된다.

---

이 장에서 만든 건 파일 셋이다. Dockerfile 하나, 매니페스트 둘. 그런데 그 파일들이 실제로 정한 것은 **경계의 개수**다. 프로세스 하나에 스레드 40개, 파드 하나에 프로세스 하나, 서비스 하나에 파드 셋. 5장의 두 층이 곱셈이 되어 커넥션 수와 종료 유예 시간과 인스턴스 요금으로 나타났다.

그러니 새 플랫폼 문서를 열 때 당신이 던질 질문도 정해진다. **인스턴스 하나에 요청을 몇 개까지 넣는가, 그리고 죽일 때 몇 초를 주는가.** 앞의 숫자가 당신 앱의 동시성 모델이 쓸모 있는지를 정하고, 뒤의 숫자가 정리 코드가 끝까지 도는지를 정한다.

앱은 이제 어딘가에서 돌고 있다. 그리고 돌기 시작한 앱에 대해 우리가 아는 것은, 프로브가 200을 돌려준다는 사실 하나뿐이다.

[^13-1]: Uvicorn 공식 문서 Deployment: Dockerfile — uv 기반 예시 전문과 세 축자 — https://github.com/Kludex/uvicorn/blob/main/docs/deployment/docker.md (조회 2026-07-25)

[^13-2]: uv 공식 Docker 가이드 — 멀티스테이지·`slim-trixie` 베이스·`UV_*` 변수·`--locked`·`--no-install-project` · `astral-sh/uv-docker-example` Dockerfile — 비루트 사용자와 `PATH` · Docker Hub Tags API `library/python` (조회 2026-07-26)

[^13-3]: `python` 공식 이미지 README(docker-library/docs)의 alpine·slim 문단 · PEP 656 (Final, 2021-03-17) · wheel 개수는 PyPI JSON API의 파일 태그 집계 (조회 2026-07-25)

[^13-4]: K8s 축자와 `--workers` — https://fastapi.tiangolo.com/deployment/server-workers/ · gunicorn 규칙·`uvicorn-worker`·`--limit-concurrency`·`$WEB_CONCURRENCY` — https://uvicorn.dev/deployment/ 와 소스 `workers.py` (조회 2026-07-25)

[^13-5]: Uvicorn 공식 문서 Settings — 헤더 2종·`--forwarded-allow-ips` 기본값·경고 축자 · FastAPI 공식 문서 Behind a Proxy — `"*"` 예시 (조회 2026-07-25)

[^13-6]: Kubernetes 공식 문서 Probes — 분리 축자·기본값 · kubernetes/website 저장소의 `examples/` YAML 4종과 `virtual-ips.md` 원문 — 매니페스트 골격·`.spec.sessionAffinity` · `from sqlalchemy import text` — SQLAlchemy 2.0 공식 문서 (조회 2026-07-26)

[^13-7]: 종료 시퀀스·`preStop`·30초·병렬 축자 — kubernetes/website 저장소 `pod-lifecycle.md` 원문 · 축소 동작 — k8s HPA 문서 · 백그라운드 태스크 대기 — Uvicorn Server Behavior (조회 2026-07-25)

[^13-8]: 실행 환경 축자와 동시성 식 — https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html · `PORT`·10초·80×vCPU — https://docs.cloud.google.com/run/docs/container-contract · `aws/aws-lambda-web-adapter`·`Kludex/mangum` 저장소 (조회 2026-07-25)

[^13-9]: Fly.io·Render·Railway 공식 문서 — 포트 계약과 Hypercorn · Granian(2.7.9 / 2026-07 기준)·Hypercorn(0.18.0 / 2025-11 기준) README (조회 2026-07-25)
