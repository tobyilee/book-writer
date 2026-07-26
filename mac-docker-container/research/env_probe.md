# 로컬 환경 실측 (Primary Evidence)

**측정 시점:** 2026-07-25
**측정 방법:** 이 책을 저술한 맥에서 직접 실행한 명령의 원본 출력. 추정·기억이 아니라 관측값이다.
**용도:** fact-checker의 1차 대조 근거. 이 파일에 있는 값은 "이 환경에서 관측됨"으로 인용할 수 있다. 단, **일반화는 금지** — 다른 맥의 기본값이라고 단정하지 말 것.

---

## 1. 호스트

```
$ sw_vers
ProductName:    macOS
ProductVersion: 26.5.2
BuildVersion:   25F84

$ uname -m
arm64
```

→ Apple Silicon(arm64), macOS 26.5.2.

---

## 2. 설치된 컨테이너 런타임 (두 개가 공존)

```
$ ls /Applications | grep -iE "docker|rancher"
Docker.app
Rancher Desktop.app
```

| 앱 | 버전 (CFBundleShortVersionString) |
|----|------|
| Docker Desktop | `4.83.0` |
| Rancher Desktop | `1.17.1` |

---

## 3. CLI 버전

```
$ docker --version
Docker version 27.5.0-rd, build 7a37716

$ docker compose version
Docker Compose version v5.3.1

$ docker buildx version
github.com/docker/buildx v0.35.0-desktop.2 b554ce1decd8b509893b1e7c6227eabfb923d094

$ kubectl version --client
Client Version: v1.32.1
Kustomize Version: v5.5.0

$ minikube version
minikube version: v1.35.0
commit: dd5d320e41b5451cdf3c01891bc4e13d189586ed

$ java -version
openjdk version "21.0.10" 2026-01-20 LTS
OpenJDK Runtime Environment (build 21.0.10+10-LTS)
OpenJDK 64-Bit Server VM (build 21.0.10+10-LTS, mixed mode, sharing)
```

---

## 4. ⭐ 핵심 관측: 클라이언트와 데몬이 서로 다른 제품

이 항목은 이 책에서 **가장 값진 실측 사례**다. 맥에서 컨테이너 도구를 여러 개 깔았을 때 실제로 벌어지는 일을 보여준다.

```
$ echo $PATH | tr ':' '\n' | grep -n "\.rd/bin"
9:/Users/tobylee/.rd/bin        # Rancher Desktop이 PATH 9번째에 자기 bin을 심음

$ command -v docker
/Users/tobylee/.rd/bin/docker   # → 실행되는 CLI는 Rancher Desktop의 것

$ docker --version
Docker version 27.5.0-rd          # 클라이언트: 27.5.0-rd ("-rd" = Rancher Desktop 빌드)

$ docker context ls
NAME              DESCRIPTION                               DOCKER ENDPOINT
default           Current DOCKER_HOST based configuration   unix:///var/run/docker.sock
desktop-linux *   Docker Desktop                            unix:///Users/tobylee/.docker/run/docker.sock

$ echo "${DOCKER_HOST:-(unset)}"
(unset)

$ docker info --format '{{.ServerVersion}} / {{.OperatingSystem}} / {{.Architecture}}'
29.6.2 / Docker Desktop / aarch64   # 데몬: Docker Desktop, 29.6.2
```

**관측된 사실:**
- 실행되는 `docker` **바이너리는 Rancher Desktop의 것**(`~/.rd/bin/docker`, `27.5.0-rd`)인데,
- 활성 **context는 `desktop-linux`(Docker Desktop)** 이고,
- 따라서 실제 명령을 처리하는 **데몬은 Docker Desktop의 `29.6.2`** 이다.
- `DOCKER_HOST`는 unset — 즉 접속 대상을 결정한 것은 환경변수가 아니라 **docker context**다.
- 데몬 아키텍처는 `aarch64`(= arm64).

**이 사례가 가르치는 것:**
1. `docker --version`은 **클라이언트** 버전이다. 데몬 버전을 보려면 `docker info` 또는 `docker version`(서버 섹션)을 봐야 한다. 클라이언트 27.5.0과 서버 29.6.2처럼 **버전이 갈릴 수 있다**.
2. 맥에 런타임을 두 개 깔면 "어느 CLI가 실행되는가"(PATH)와 "어느 데몬에 붙는가"(context/`DOCKER_HOST`)가 **따로 논다**. 둘을 같이 확인해야 한다.
3. 트러블슈팅의 첫 명령은 `docker context ls` + `docker info`다.

---

## 5. Kubernetes 컨텍스트

```
$ kubectl config get-contexts
CURRENT   NAME                                               CLUSTER
          docker-desktop                                     docker-desktop
          minikube                                           minikube
*         tobyilee@web-quickstart.ap-northeast-2.eksctl.io   web-quickstart.ap-northeast-2.eksctl.io
```

**관측된 사실:**
- 로컬 클러스터 선택지가 두 개 존재: `docker-desktop`(Docker Desktop 내장 K8s), `minikube`.
- 그런데 **현재 활성 컨텍스트(`*`)는 로컬이 아니라 원격 EKS 클러스터**(`ap-northeast-2`, eksctl로 생성)다.
- → `kubectl apply`가 의도치 않게 **운영/클라우드 클러스터로 나갈 수 있다**는 실물 증거. 로컬 실습 전 `kubectl config current-context` 확인이 왜 필수인지 보여주는 사례.

---

## 6. Rancher Desktop이 PATH에 제공하는 바이너리

```
$ ls ~/.rd/bin
docker                          helm
docker-buildx                   kubectl
docker-compose                  kuberlr
docker-credential-ecr-login     nerdctl
docker-credential-none          rdctl
docker-credential-osxkeychain   spin
```

→ `nerdctl`(containerd CLI), `rdctl`(Rancher Desktop 제어), `helm`, `kuberlr`(kubectl 버전 shim)까지 함께 깔린다.

---

## 7. 빌드 툴체인 (이 책 자체를 만드는 데 쓰임)

```
pandoc      /opt/homebrew/bin/pandoc
epubcheck   /opt/homebrew/bin/epubcheck
magick      /opt/homebrew/bin/magick
```

---

## 사용 규칙 (저술가·fact-checker용)

- ✅ **가능:** "이 책을 쓴 맥(macOS 26.5.2 / arm64, 2026-07 기준)에서는 클라이언트 27.5.0-rd가 서버 29.6.2에 붙어 있었다"처럼 **관측 맥락과 함께** 인용.
- ❌ **금지:** "Docker의 최신 버전은 29.6.2다", "맥의 기본 context는 desktop-linux다"처럼 **일반화·최신성 단정**. 그런 주장은 별도 1차 소스(릴리스 노트·공식 문서)가 있어야 하며 `01_reference.md`에서 근거를 찾아야 한다.
- ⚠️ 이 파일은 **한 대의 맥**에서 나온 값이다. 표본 1이다.
