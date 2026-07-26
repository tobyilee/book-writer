# 3장. Docker Desktop이 맥에서 실제로 하는 일

문서가 스스로 "가장 최신이고 가장 성능이 좋다"고 말하는 옵션을 골랐는데, 바로 그 선택 때문에 amd64 빌드가 훨씬 느려질 수 있다면 — 우리는 그 설정 화면을 제대로 읽고 있는 걸까?

설정 화면은 목록처럼 생겼다. 드롭다운 하나, 체크박스 하나, 슬라이더 몇 개. 목록처럼 생긴 것은 대개 서로 독립적이라고 읽힌다. 하나를 바꾸면 그 하나만 바뀔 것 같다. 그런데 맥의 Docker Desktop에서는 그렇지 않다. 위에서 고른 것이 아래 있던 항목을 화면에서 지워버리고, 왜 지워졌는지는 어디에도 적혀 있지 않다. 그 관계를 하나씩 풀어보자.

### VMM을 고르면 Rosetta가 따라온다

Docker Desktop 설정 화면에는 이런 이름의 항목이 있다 — "Choose Virtual Machine Manager (VMM)". 2장에서 그려둔 그 리눅스 VM을 무엇으로 돌릴지 고르는 자리다. 고를 수 있는 것은 셋이다(Docker Desktop 공식 문서, 2026-07-25 열람 기준).

| 설정에 표기된 이름 | 문서의 서술 (축자) | Rosetta |
|---|---|---|
| **Docker VMM** | "the latest and most performant Hypervisor/Virtual Machine Manager. This option is available only on Apple Silicon Macs and is in Beta." | **미지원** |
| **Apple Virtualization framework** | "A stable and well-established option for managing virtual machines on Mac" | Rosetta 옵션의 전제 조건 |
| **QEMU** | 세 번째 선택지. VMM 문서는 QEMU와 HyperKit을 legacy·deprecated로 표기한다 | — |

여기까지는 그냥 옵션 목록이다. 그런데 같은 설정 화면 아래쪽에 "Use Rosetta for x86_64/amd64 emulation on Apple Silicon"이라는 항목이 따로 있고(기본값 Disabled), 그 설명에 이런 문장이 붙어 있다.

> "This option is only available if you have selected **Apple Virtualization framework** as the Virtual Machine Manager."

그리고 Docker VMM을 설명하는 별도 문서에는 이 문장이 있다.

> "Docker VMM does not currently support Rosetta, so emulation of amd64 architectures is slow."

두 문장을 나란히 놓아보자. 무엇이 보이는가? **가장 최신이고 가장 성능이 좋다는 VMM을 고르는 순간, Rosetta 스위치는 화면에서 사라진다.** 각각 좋은 걸 고르면 되는 관계가 아니라, 하나가 다른 하나의 존재 여부를 결정하는 관계다. amd64 에뮬레이션이 필요한 사람에게는 VMM 선택 자체가 트레이드오프인 셈이다. 이걸 모른 채 "성능 좋다는 걸로 바꿨는데 왜 더 느려졌지" 하고 며칠을 태우기 딱 좋다.

한 가지 더. Docker VMM에는 "requires a minimum of 4GB of memory to be allocated to the Docker Linux VM"이라는 조건이 붙는다. 맥에 램이 4GB 있어야 한다는 말이 아니라, **그 리눅스 VM에 할당된 메모리**가 4GB 이상이어야 한다는 말이다. 2장에서 계층을 그려두지 않았다면 이 문장부터 헷갈렸을 것이다.

그렇다면 아무것도 안 만졌을 때 기본으로 잡히는 VMM은 무엇일까? **모른다.** 공식 문서에서 "기본은 이것이다"라는 문장을 확인하지 못했다. 그래서 이 책은 그 자리를 비워둔다 — 1장에서 약속한 대로, 확인하지 못한 것은 확인하지 못했다고 쓴다. 대신 지금 이 맥에서 직접 열어 확인하는 편이 낫다. 위 문장의 **"not currently"**라는 단어도 눈여겨볼 만하다 — 지금 시점의 상태라는 뜻이고, 이 관계는 바뀔 수 있다. 설정을 만지기 전에 공식 문서를 한 번 같이 열어보자.

### 파일이 VM 경계를 넘는 방식

`docker run -v "$(pwd)":/app ...` 같은 명령을 별생각 없이 써왔다면, 그게 실제로 무슨 일인지 다시 보자. 왼쪽 경로는 맥 파일시스템에 있고, 오른쪽 경로는 **VM 안 리눅스**에 있다. 한 머신 안에서 디렉터리 두 개를 이어붙이는 게 아니라, 서로 다른 운영체제 두 개를 이어붙이는 일이다. 2장의 그 VM이 여기서 처음으로 얼굴을 내민다 — 그 경계가 있기 때문에 맥 쪽 디렉터리를 컨테이너 안에서 보이게 하려면 두 운영체제 사이에서 파일 접근을 중계해줄 무언가가 필요하고, 그 중계 방식이 설정 화면의 한 항목으로 올라와 있다.

그 항목의 이름 역시 축자로 이렇다 — "Choose file sharing implementation for your containers". 선택지는 VirtioFS(기본)와 gRPC FUSE 둘이다. 이름이 낯설어도 지금은 "맥과 VM 사이에서 파일을 중계하는 방식 두 가지"라고만 알아두면 충분하다. 여기서 먼저 눈여겨볼 것은 이름이 아니라 **선택지가 있다는 사실 자체**다. 리눅스에서 도커를 쓰는 사람의 설정 화면에는 이런 항목이 없다. 고를 것이 생겼다는 건 그 자리에 무언가 값이 든다는 뜻이고, 그 값은 2장에서 본 경계의 청구서다.

문서는 두 선택지 가운데 VirtioFS에 이런 문장을 달아두었다.

> "VirtioFS has reduced the time taken to complete filesystem operations by up to 98%."

숫자가 크다. 그런데 잠시 멈추고 이 문장을 다시 읽어보자. **무엇 대비 98%인지가 안 적혀 있다.** 어떤 워크로드에서 잰 것인지도 없다. 그러니 이 책은 "VirtioFS로 바꾸면 98% 빨라진다"라고 우리 문장으로 옮기지 않는다. 우리가 아는 것은 Docker 공식 문서가 그렇게 적어두었다는 사실까지다.

이 구분을 그냥 깐깐함으로 넘기지 말자. 실무에서 이 차이는 꽤 크게 벌어진다. 문서가 준 것은 방향이다 — 두 구현 중 하나가 파일 작업에서 유리하다는 벤더의 주장. 문서가 주지 않은 것은 크기다. 당신의 프로젝트에서, 당신의 소스 트리 크기로, 당신이 실제로 돌리는 빌드와 테스트에서 그 차이가 몇 초인지는 그 문장이 답해주지 않는다. 그러니 이 항목을 만질 때 기대할 수 있는 것은 "이 방향으로 가면 나아질 여지가 있다"까지이고, 실제 크기는 자기 프로젝트에서 같은 작업을 두 번 돌려보는 수밖에 없다. 벤더의 숫자를 자기 환경의 예측치로 옮겨 적는 순간, 우리는 확인하지 않은 것을 확인한 것처럼 다루게 된다.

그리고 이 항목은 앞 소절과도 이어져 있다.

> "It is the only file sharing implementation supported by Docker VMM."

VMM 하나를 골랐을 뿐인데 파일 공유 구현까지 따라 정해진다. 사슬이 한 칸 더 길어진 것이다. 게다가 그 조합에는 이런 경고까지 붙어 있다.

> "Certain databases, like MongoDB and Cassandra, may fail when using virtiofs with Docker VMM."

성능이 좀 떨어진다가 아니라 **fail**이다. 이 문장이 왜 중요한지는 자기 개발 환경을 떠올려보면 바로 안다. 로컬에서 DB를 컨테이너로 띄워두고 작업해본 적이 있다면, 공식 문서가 이름을 대며 실패 가능성을 경고하는 대상이 바로 그 자리다. 다시 말해 이 드롭다운은 "조금 빠른 쪽을 고르는 취향의 문제"가 아니라, 어떤 조합에서는 뜨느냐 마느냐의 문제로 넘어간다. 성능 항목처럼 생긴 자리에 동작 여부가 걸려 있는 셈이다.

### Rosetta는 켜면 빨라지는 스위치가 아니다

앞에서 우리는 "Rosetta를 쓰려면 VMM을 이걸로 골라야 한다"까지 왔다. 그러면 그렇게 골라 켜기만 하면 amd64가 쾌적해질까?

`docker/for-mac#7075`(2023-11 등록, 2026-07-25 조회 시점 OPEN)에 올라온 빌드 로그를 보자. M2 Max 맥북 프로 사용자가 Rosetta를 **켠** 상태로 amd64 이미지를 빌드한 결과다.

```
[+] Building 33656.6s (15/22)
 => [builder 5/5] RUN yarn build      33186.8s
```

33,656초. 약 **9시간 21분**이다. 밤새 돌려놓고 아침에 출근했는데 아직 안 끝나 있었다는 이야기다. 물론 이 숫자 자체는 벤치마크가 아니다 — 한 사람의 한 환경, 한 워크로드에서 나온 자기 보고다. "Rosetta를 켜면 9시간이 걸린다"고 읽으면 안 된다. 다만 같은 증상은 M1·M2 Max·M3 Max·M3 Pro에 걸쳐 2023년 11월부터 2024년 6월까지 반복 보고됐고, 같은 이슈에 모인 다른 목소리들을 겹쳐 보면 그림이 좀 더 선명해진다. `AlexandreRoba`(M3 Max 64GB)는 Docker Desktop을 4.24.2로 내리고 Rosetta도 함께 끈 뒤 5분 만에 빌드가 끝났다고 적었고 — 두 가지를 같이 바꿨으니 어느 쪽 덕인지는 그 보고만으로 가릴 수 없다 — `alnaranjo`는 이렇게 말했다.

> "Using 4.25.x would cause docker build to hang indefinitely even when disabling 'use rosetta'. **Building arm images is a breeze, though.**"

이 이슈는 한 번 닫힌 적이 있다. Docker 쪽에서 특정 버전을 제안했고 실제로 해결된 사용자가 있었다. 그런데 닫힌 뒤에도 같은 보고가 이어졌다.

> "why is this closed? I think the issue persists for latest macbook users" — `jinmel`, 2024-06-29

그리고 4.30·4.31에서도 같은 증상 보고가 올라왔으며, 2026-07-25에 조회한 시점에 이슈는 **다시 열려 있다.** 그래서 이 책은 두 문장을 다 쓰지 않는다. **"Rosetta를 켜면 빨라진다"도, "그 문제는 이제 해결됐다"도.** 켜서 좋아진 사람과 꺼서 살아난 사람이 같은 이슈 안에 나란히 있고, Docker Desktop 버전에 따라 결과가 뒤집힌다.

자바 쪽 판본도 하나 있다. 2026년 2월 한 커뮤니티 스레드에서 `p0w3n3d`라는 사용자가, **Podman에서** Rosetta를 켠 amd64 환경으로 `eclipse-temurin:25-jdk-ubi10-minimal` 이미지 위의 Spring Boot 앱을 띄운 결과를 이렇게 올렸다.

```
podman run   0.02s user 0.01s system 0% cpu 24.960 total
```

20초대다. 이건 런타임 비교로 읽으면 안 된다 — 같은 사람이 바로 앞에서 "내 머신에서 podman과 docker 사이에 차이가 없다"고 스스로 번복한 뒤에 올린 관측이고, 어느 쪽이든 한 사용자의 자기 보고다. 여기서 남는 건 딱 하나다. 에뮬레이션 위에 올라간 자바는 느리다. 그렇다면 가장 확실한 처방은 무엇일까? 에뮬레이션을 잘 켜는 게 아니라 **에뮬레이션을 안 하는 것**이다. 그러려면 내가 만드는 이미지가 어느 아키텍처인지부터 알아야 하는데, 그 이야기는 6장의 몫이다.

### 무료로 쓸 수 있는가 — 250인 AND $10M

설정 화면 바깥에도 결정이 하나 있다. **이걸 회사에서 써도 되는가.**

Docker의 공식 라이선스 페이지(`docs.docker.com/subscription/desktop-license/`, 2026-07-25 열람. 발행일은 페이지에서 확인하지 못했다)가 무료 사용 범위로 든 문구 가운데 하나는 축자로 이렇다.

> "Small businesses (**fewer than 250 employees AND less than $10 million in annual revenue**)"

그리고 같은 페이지는 "Professional use in larger organizations"와 "Government entities"에는 유료 구독이 필요하다고 적는다.

여기서 놓치면 안 되는 것이 두 가지다. 첫째, 직원 250명 미만 그리고 연매출 1,000만 달러 미만 — **AND 조건**이다. 둘 중 하나만 넘어도 무료 범위 밖이다. 사람 수만 보고 "우리는 100명이니까 괜찮다"고 넘어가기 쉬운데, 매출 쪽이 먼저 임계값을 넘는 회사가 적지 않다. 둘째, 이 임계값은 개인이 아니라 조직에 걸리고, 돈이 걸린 대상은 Docker Desktop이라는 제품이다. 1장에서 Docker Desktop·Docker Engine·Docker Hub의 경계를 먼저 그어둔 이유가 여기 있다 — 뭉뚱그려 놓으면 이 문장이 무엇에 대한 조건인지부터 흐려진다.

그런데 현장의 대화는 조건표보다 훨씬 어지럽다. 2026년 7월 한 커뮤니티 스레드에서 오간 두 마디다.

> `ifwinterco` (2026-07-02): "Docker CLI is free for commercial use, it's only docker desktop you have to pay for"
>
> `pjmlp` (2026-07-02): "I know, but companies legal or IT department make it easier, **no docker of any kind being installed from https://www.docker.com.**"

앞의 말은 공식 문서의 서술이 아니라 한 사용자의 발언이라는 점을 분명히 해두자. 확인된 1차 소스는 위에 옮긴 라이선스 페이지 문구뿐이다. 그럼에도 이 두 마디에는 값이 있다. **논쟁이 실제로 벌어지는 자리가 기술이 아니라 구매 정책이라는 것**을 보여주기 때문이다. 조건을 아무리 정확히 읽어도, 법무나 IT가 "docker.com에서 받는 건 무엇이든 설치 금지"로 잘라버리면 개발자에게 남는 선택지는 다른 종류의 것이 된다.

이 풍경이 새롭지도 않다는 게 더 난감하다. 4년 앞선 2022년 1월의 스레드에는 회사를 설득해 비용을 승인받았다는 사람(`yuppie_scum`)과, 이런 사람이 나란히 있었다.

> `pseudoramble`: "Ah man, that must be a magical place. **I spent months (on-and-off) trying to convince my company to do this and failed.** ... it genuinely worries me that while **IT considers it unapproved software** that it won't stop its usage."

뒤의 말이 특히 마음에 걸린다. **승인되지 않은 소프트웨어라는 걸 조직이 알면서도, 아무도 쓰는 걸 멈추지는 않는 상태.** 한국의 SI·대기업에서 일해본 독자라면 이 회색지대가 남 이야기 같지 않을 것이다.

그러니 이 소절의 결론은 이렇게 두자. **라이선스 조건은 돈이 걸린 사실이고, 돈이 걸린 사실은 바뀐다.** 여기 옮긴 것은 2026년 7월 25일에 그 페이지가 그렇게 적혀 있었다는 사실 하나다. 회사에서 쓸지 말지를 실제로 판단해야 하는 자리라면, 기준으로 삼을 것은 이 책의 문장이 아니라 그날의 공식 라이선스 페이지다.

설정 화면을 한 번 더 내려보자. VMM·파일 공유·Rosetta 아래에는 메모리와 CPU, 디스크를 정하는 슬라이더들이 있고, 문서는 각각에 정해진 기본값을 적어두었다. 아무것도 만지지 않아도 이미 어떤 값이 잡혀 있다는 뜻이다.

설정 화면은 옵션 목록이 아니라 관계도다. 하나를 고르면 다른 하나가 화면에서 사라지고, 사라진 줄도 모른 채 시간이 지나간다. 그런데 이 관계도에는 아직 한 번도 손대지 않은 칸이 남아 있다. 아래쪽, 숫자가 적힌 그 슬라이더들이다.
