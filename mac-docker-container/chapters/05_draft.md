# 5장. 무엇이 실행되고, 어디에 붙는가

이 책을 쓴 맥에서 2026년 7월 25일에 연달아 친 명령 두 줄이다.

```
$ docker --version
Docker version 27.5.0-rd, build 7a37716

$ docker info --format '{{.ServerVersion}} / {{.OperatingSystem}} / {{.Architecture}}'
29.6.2 / Docker Desktop / aarch64
```

같은 터미널에서 이어 친 두 줄인데 버전이 다르다. 27.5.0과 29.6.2. 그리고 위쪽 버전에 붙은 `-rd`는 Rancher Desktop이 만든 빌드라는 표시이고, 아래쪽은 자기가 Docker Desktop이라고 답한다.

그러니까 명령을 받아든 CLI는 Rancher Desktop의 것이고, 그 명령을 실제로 처리한 데몬은 Docker Desktop의 것이다. 한 줄을 치면 두 회사의 제품을 차례로 거쳐 간다. 더 찜찜한 건 이 상태에서도 대부분의 명령이 그냥 잘 돈다는 점이다. 그래서 몇 달이고 모른 채 지낼 수 있다.

앞 장 마지막에 남겨둔 질문이 이것이었다. 한도를 강제하고 숫자를 보고하는 그 데몬이, 정말 우리가 생각하는 그 제품이 맞을까? 적어도 이 맥에서는 아니었다. (표본은 하나다. 다른 맥의 기본 상태가 이렇다는 뜻이 아니라, 런타임을 둘 깔면 이런 조합이 만들어질 수 있다는 증거로만 읽자.)

### 첫 명령 세 줄

이런 상태를 알아채려면 무엇을 물어야 했을까? 질문을 둘로 쪼개는 게 먼저다. **무엇이 실행되는가**와 **어디에 붙는가**는 서로 다른 질문이고, 답이 있는 자리도 다르다.

첫째, 어느 바이너리가 실행되는가.

```
$ command -v docker
/Users/tobylee/.rd/bin/docker
```

`~/.rd/bin`은 Rancher Desktop이 PATH에 심어 둔 디렉터리이고, 같은 자리에 `docker-buildx`·`docker-compose`·`nerdctl`·`rdctl`·`kubectl`·`helm`이 함께 들어 있다. 런타임 하나를 설치하는 순간, 앞으로 칠 `docker`가 어느 회사 것인지가 PATH 순서로 조용히 결정된 것이다.

둘째, 그 CLI가 어느 데몬에 붙는가.

```
$ docker context ls
NAME              DESCRIPTION                               DOCKER ENDPOINT
default           Current DOCKER_HOST based configuration   unix:///var/run/docker.sock
desktop-linux *   Docker Desktop                            unix:///Users/tobylee/.docker/run/docker.sock
```

별표가 붙은 쪽이 활성 context이고, 그 엔드포인트가 Docker Desktop의 소켓이다. 여기서 이미 오프닝의 모순이 풀린다. 바이너리와 데몬이 각각 따로 결정된 것이다.

셋째, 그 선택을 누가 덮어쓰고 있지는 않은가. `echo $DOCKER_HOST`를 쳐보니 이 맥에서는 아무것도 나오지 않았다. 접속 대상을 정한 것이 환경변수가 아니라 context라는 뜻이다. 이 관계는 공식 문서가 축자로 정리해준다.

> "all `docker` commands run against this context, unless overridden with environment variables such as `DOCKER_HOST` and `DOCKER_CONTEXT`, or on the command-line with the `--context` and `--host` flags."

우선순위를 뽑아내면 이렇다. **CLI 플래그 > 환경변수 > 활성 context.** 뭔가 이상할 때 이 순서를 거꾸로 훑으면 대개 범인이 나온다.

세 줄로 세 가지를 갈라 물었으니, 이제 답을 맞춰볼 차례다. 네 번째 명령이 `docker info`다. 여기서 한 가지는 확실히 기억해두자. **`docker --version`은 클라이언트 버전이다.** 데몬 버전을 보려면 `docker info`나 `docker version`의 Server 섹션을 봐야 한다. 오프닝의 두 숫자가 갈렸던 이유가 정확히 그것이다.

다만 정직하게 밝혀둘 것이 있다. 공식 문서는 context의 우선순위까지는 설명하지만, **PATH가 고른 CLI와 context가 가리키는 데몬이 서로 다른 제품인 교차 상태 자체는 다루지 않는다.** 짝이 되는 커뮤니티 보고가 하나 있긴 하다 — Docker Desktop이 시작하면서 context를 바꿔놓는 바람에 `docker context use default`로 되돌리기 전까지 명령이 전부 실패했다는 `rancher-desktop#7712`(2024-11-01 등록, 2026-07-25 조회 시점 OPEN). 그런데 이건 **Windows 사례다.** 맥 이야기로 옮겨 적을 수는 없으니 두 근거는 나란히 두자. 실패의 구조만은 같다 — 런타임 두 개가 `docker context`라는 하나의 전역 상태를 놓고 다투는데, 아무도 사용자에게 알려주지 않는다.

### 개발 환경을 컨테이너로 꾸리기

새 팀원이 들어와 저장소를 받았다고 해보자. 앱을 켜기 전에 준비할 것이 있다. Postgres가 있어야 하고, Redis도 있어야 하고, 프로젝트에 따라서는 메시지 브로커까지 있어야 한다. 예전에는 이걸 각자 맥에 직접 깔았다. 그러면 사람마다 버전이 갈리고, 프로젝트를 옮겨 다니는 사이 한 맥에 Postgres 세 벌이 쌓인다.

그래서 이제는 컨테이너로 띄운다. 사실 자바 백엔드 개발자가 맥에서 도커를 쓰는 **가장 흔한 이유**가 이쪽이다. 내 앱을 이미지로 만들어 배포하려고가 아니라, **내 앱이 기대는 것들을 띄워놓고 그 위에서 개발하려고** 쓴다. 4장에서 본 그 velog 글쓴이도 배포하다 사고를 만난 게 아니었다. 여러 컨테이너를 띄워놓고 개발하다가 Redis가 자꾸 꺼진 것이었다.

그런데 이 방식에는 잔손이 붙는다. 앱을 켜기 전에 컨테이너를 올리고, 끝나면 내린다. 접속 정보를 애플리케이션 설정에 또 한 번 적고, 포트를 하나 바꾸면 두 군데를 같이 고친다. 사소하지만 매일 반복되니 번거롭다.

스프링 부트에는 이 잔손을 걷어가는 모듈이 있다. `spring-boot-docker-compose`다. 메이븐은 이 좌표에 `<optional>true</optional>`을, 그레이들은 `developmentOnly(...)`를 붙인다. 둘 다 "개발 중에만"이라는 표시로, 배포되는 산출물에는 딸려 나가지 않는다.

붙이고 나면 무엇이 자동으로 일어날까? 공식 문서(표기 4.1.0, 2026년 7월 25일 검색 기준)가 밝히는 계약은 세 단계다. `compose.yml` 같은 통상적인 이름의 compose 파일을 찾아 **`docker compose up`을 호출**하고, 지원되는 컨테이너마다 **service connection 빈을 만들고**, 애플리케이션이 종료될 때 **`docker compose stop`을 호출**한다.

두 번째 단계가 잔손의 핵심을 걷어낸다. 컨테이너가 어느 포트에 떴는지를 스프링이 직접 읽어 연결 정보를 만들어주므로, 같은 값을 설정 파일에 두 번 적을 일이 없다. 이 자동 연결이 붙는 서비스는 문서 기준 스무 종에 이른다 — PostgreSQL·MySQL·MariaDB·Oracle·Redis·MongoDB·Cassandra·Elasticsearch·RabbitMQ·Pulsar·Zipkin 등에 JDBC/R2DBC까지. 직접 만든 이미지에 붙이려면 `org.springframework.boot.service-connection: redis` 같은 라벨을, 반대로 건드리지 않게 하려면 `org.springframework.boot.ignore: true`를 단다.

자동으로 일어나는 일이 있으면 **끄는 법**도 같이 알아두자. 이미 손으로 띄워 둔 컨테이너를 앱이 마음대로 내려버리면 그것대로 난감하기 때문이다. 스위치는 `spring.docker.compose.lifecycle-management`이고 값은 셋이다 — `none`(아무것도 하지 않음), `start-only`(띄우기만 하고 내리지 않음), `start-and-stop`. 그 밖에 파일 위치(`file`)와 프로파일(`profiles.active`), 호출할 명령(`start.command`·`stop.command`)과 인자(`start.arguments[0]=--build`), 종료 대기 시간(`stop.timeout`)까지 문서가 프로퍼티로 열어두었다.

한 가지만 더 짚자. 이 모듈이 결국 하는 일은 **`docker compose up`을 대신 쳐주는 것**이다. 그 명령이 어느 데몬으로 나갈지는 이 모듈이 정하지 않는다. 앞 소절의 context가 정한다. 개발 환경을 컨테이너로 꾸린다는 건, 매일 아침 이 장의 첫 질문 위에서 일을 시작한다는 뜻이기도 하다. (compose 파일 자체의 문법은 이 책의 범위가 아니다. 그건 Compose 공식 문서의 몫이다.)

### 2026년의 대안 런타임 지형

그런데 왜 한 맥에 런타임이 두 개나 깔려 있었을까? `styfle`이라는 사용자의 한마디가 그 심리를 정확히 짚는다.

> "I have a machine with Colima and don't want to bork it if I try Orbstack."

새 걸 써보고는 싶은데, 쓰던 걸 지웠다가 지금 굴러가는 환경이 망가지는 게 무섭다. 그래서 일단 같이 깔아둔다. 이 책을 쓴 맥의 상태가 정확히 그 결과물이다.

같이 깔면 뭔가를 놓고 다툰다. 대표 선수가 `/var/run/docker.sock`이다. Colima가 그 소켓을 차지하게 해달라는 요청은 "너무 많은 도구가 그 경로를 하드코딩한다"는 이유로 반복해 올라오는데, Colima 저자 `abiosoft`의 답은 이랬다.

> "many tools are indeed catching up and utilising `docker context` instead. Another advantage of this approach is the ability to **try out Colima without breaking your current workflow.**"

앞 소절에서 본 그 context를 쓰라는 이야기다. 2022년 7월에 등록된 이 이슈는 2026년 7월 25일 조회 시점에도 열려 있다. 4년째다.

그럼 2026년의 판세는 어떨까. 아래는 **추천이 아니라 사람들이 무엇을 쓰고 무엇을 말하는지의 요약**이고, 전부 커뮤니티 발언이라 "누가 언제 이렇게 말했다"까지만 유효하다.

2026년 7월 2일 Podman v6.0.0 발표 스레드에서 `spockz`가 남긴 댓글이 밀도가 높다. 그는 맥에서 Docker Desktop이 더 직관적이었다고 하면서도 "lately it has been very error prone"이라고 적는다. 파일 마운트가 무작위로 실패하고, 네트워킹 규칙 정리가 안 되고, 갑자기 느려져 VM을 재시작해야 한다는 것이다. 그러고는 이렇게 잇는다 — "Podman on macOS feels miles less refined. Orbstack is a way better choice." 흥미로운 건 같은 사람이 리눅스의 Podman은 "blazing fast"라고 적었다는 점이다. 제품의 우열이 아니라 **맥이라는 조건이 판단을 뒤집는다.** 2026년 2월 25일 스레드의 `bmurphy1976`은 Rancher Desktop으로 옮겨 "지금까지는 그냥 잘 된다"고 적었다. OrbStack 쪽엔 칭찬이 몰려 있는데, 같은 스레드의 `Shebanator`는 다른 축을 짚었다 — "products like this need security updates at the very least." 이 책은 OrbStack의 릴리스 라인을 조회하지 않았으니 그 물음에 답을 보태지 않겠다. Colima도 관측만 적어둔다. 2026년 7월 25일 조회 시점에 확인된 최신 릴리스는 2025년 6월 4일자였다.

그리고 2026년, 축이 하나 늘었다. Apple Containers다. 이걸 쓰는 도구(Davit)를 만든 `xinit`의 설명이 구조를 한 줄로 보여준다.

> "Docker Desktop/Obstack start a single VM that runs all your containers. This means that you'll have to scale it accordingly. Davit uses Apple Containers that runs a very thin VM for each container you spin up."

VM 하나에 컨테이너를 모두 태울 것인가, 컨테이너마다 얇은 VM을 하나씩 붙일 것인가. 2장에서 심어둔 문장의 변주다. 어느 쪽을 고르든 **맥에서는 VM이 있다.** 물론 공짜는 아니어서, 바로 다음 날 `watermelon0`이 반론을 달았다 — 컨테이너마다 별도 VM을 만들면 리눅스 커널 오버헤드 때문에 메모리 사용량이 오히려 커진다는 것이다. 이 지형은 빠르게 바뀐다. 고를 때가 되면 각 제품의 공식 문서를 그날 기준으로 다시 열어보자.

### 이주하면 실제로 깨지는 것들

옮기기로 마음먹었다면 청구서를 먼저 보자. 커뮤니티가 실제로 겪고 보고한 목록이 있다.

가장 앞줄이 **Testcontainers와 Ryuk의 소켓**이다(2022-02 보고). 다음 소절 전체를 쓸 만큼 중요하니 여기서는 이름만 걸어둔다. 그다음은 `/var/run/docker.sock` 경로를 **하드코딩한 도구들**(colima#365, 2022-07) — 방금 본 논쟁이 남의 도구에서 에러로 나타나는 순간이다. Colima 쪽에는 볼륨 마운트의 **권한·안정성** 증언이(2024-09), OrbStack 쪽에는 백업 소프트웨어와 충돌하거나 오프라인에서 라이선스 서버에 닿지 못해 동작이 멈췄다는 증언이 있다(2024-09). 마지막이 앞에서 본 `docker context` 전역 상태 다툼이다.

목록만 보면 성가신 잔고장 모음처럼 읽힌다. 그런데 `nkmnz`의 한 줄이 성격을 바꿔놓는다. OrbStack의 로컬 네트워킹과 운영의 compose + nginx 조합이 "does not translate 1:1"이라는 지적이었다.

우리가 애초에 컨테이너를 쓰는 이유가 무엇이었나. **로컬과 운영을 같게 만들려는 것**이었다. 그런데 로컬의 런타임을 바꾸면 바로 그 등가성이 조금씩 깎인다. 얻는 것(속도·자원·라이선스)과 잃는 것(로컬이 운영과 닮은 정도)이 서로 다른 통장에 찍히기 때문에, 옮긴 직후에는 이득만 보이고 손실은 몇 달 뒤에 청구된다. 뒷맛이 찜찜한 거래다. 그러니 이주를 검토한다면 "무엇이 빨라지는가"만 재지 말자. **무엇이 운영과 달라지는가**를 같이 적어두는 편이 낫다.

### 런타임을 바꾸면 자바 테스트가 먼저 안다

등가성이 깨지는 걸 가장 먼저 알아채는 건 사람이 아니다. 테스트다. 자바 개발자에게는 대개 Testcontainers가 그 역할을 한다.

공식 문서는 런타임별 설정을 아예 직접 준다. Docker Desktop은 "automatically detected and used by Testcontainers without any additional configuration" — 손댈 게 없다. 반면 Colima·Podman·Rancher Desktop에는 각각 환경변수 묶음이 문서화돼 있고, 거기 반복해 나오는 두 변수가 이 장의 핵심을 다시 건드린다.

- `DOCKER_HOST` — **호스트(맥)에서 본** 소켓 경로
- `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` — **컨테이너 안에서 본** 소켓 경로(`/var/run/docker.sock`)

같은 소켓을 가리키는데 값이 서로 다르다. 왜 그럴까? Testcontainers는 테스트가 끝난 뒤 남은 컨테이너를 치우려고 Ryuk이라는 정리용 컨테이너를 함께 띄우는데, **그 컨테이너도 데몬에 붙어야 하기 때문이다.** 맥에서 본 소켓의 주소와, VM 안에서 도는 컨테이너가 본 같은 소켓의 주소가 다르다. 그래서 둘을 따로 알려줘야 한다.

2장에서 심어둔 문장이 여기서 세 번째로 돌아온다. 소켓 하나가 **VM 경계를 넘고 있고**, 경계 이쪽과 저쪽에서 이름이 달라진다. 4장의 메모리가 층마다 다르게 세어지던 것과 같은 구조다.

이 사정을 모른 채 마주치는 에러는 꽤 사납다. 그래서 커뮤니티에는 훨씬 짧은 처방이 돌아다닌다. `TESTCONTAINERS_RYUK_DISABLED=true`. 붙여넣으면 에러는 사라진다. 하지만 메인테이너 `kiview`의 답은 단호했다.

> "**This will mask the error, rather than fixing the root cause**, since it will simply disable Ryuk, thereby leaving you without reliable resource cleanup."

에러를 가린 것이지 고친 게 아니고, 대신 정리를 책임지던 장치를 잃는다는 것이다. 이 입장은 2026년에도 유지된다. 같은 해 1월 5일 이 값을 `testcontainers.properties`로 설정하게 해달라는 요청과 PR이 올라왔지만, 2월 3일 메인테이너가 빌드 도구 설정으로 같은 목적을 이룰 수 있다며 **병합하지 않고 닫았다**(병합 기록이 비어 있음을 2026년 7월 25일에 확인했다). 그러니 "이제 `ryuk.disabled` 프로퍼티를 지원한다"는 말을 들었다면 사실이 아니다. 요청은 반복되고, 메인테이너는 매번 우회 방법을 알려주며 반려한다.

설정을 다 맞춰도 얻어맞을 때가 있다. 2025년 12월 1일 등록되어 2026년 7월 25일 조회 시점에도 열려 있는 이슈에서, 한 컨트리뷰터가 버전을 이등분해가며 보고했다. `2.0.1`은 자기 환경의 Rancher Desktop이 제공하는 도커 엔진을 감지했는데 `2.0.2`와 `2.0.3`은 감지하지 못했고, "체인지로그에서 파괴적 변경을 하나도 못 찾겠다"는 것이다. 메인테이너의 답도 솔직했다 — "I would like to know when we broke this." (원인은 아직 확정되지 않았고 표본도 그의 환경 하나다. "2.0.2에서 회귀가 있었다"고 옮겨 적으면 안 된다.)

같은 글에 구조를 설명하는 한 줄이 붙어 있다.

> "the testcontainers' GitHub actions file does not test either Rancher Desktop or Docker Desktop."

맥 개발자가 왜 자꾸 이런 자리에 서게 되는지가 여기 있다. 우리가 매일 쓰는 조합은 라이브러리의 CI가 지나가는 길 위에 없다. 그러니 자바 테스트가 갑자기 "Could not find a valid Docker environment"를 뱉는다면, 코드를 뒤지기 전에 **어느 데몬에 붙으려 했는지**부터 확인하자. 이 장의 첫 세 줄이 거기서 다시 쓸모를 얻는다.

---

이제 두 가지를 손에 넣었다. 무엇이 실행되고 어디에 붙는지를 분리해 묻는 세 줄, 그리고 그 데몬 위에 개발 환경을 통째로 올려 쓰는 동선이다. 앱을 켜면 DB가 따라 뜨고, 테스트를 돌리면 컨테이너가 붙었다 사라진다.

그런데 우리는 여태 그 데몬에게 시킨 적이 없다. **자기 이미지를 하나 만들어보라고.** 지금까지 다룬 건 전부 남이 만든 이미지를 받아 띄우는 일이었다. 데몬이 제 손으로 무언가를 만들기 시작하는 순간, 사람들의 며칠을 가장 자주 잡아먹는 문제가 등장한다.
