# 맥(Apple Silicon)에서의 Docker·컨테이너 심화 레퍼런스

**작성:** Phase 1 research-lead / **genre:** `tech-book` / **슬러그:** `mac-docker-container`
**검색 시점(모든 소스 공통):** 2026-07-25
**대상 독자:** 자바/스프링 중심 백엔드 개발자. Apple Silicon 맥 사용. 컨테이너를 어깨너머로 써봤지만 원리와 실무 판단 기준은 흐릿한 상태. 입문~중급.

---

## 0. 이 문서를 읽는 법 (Phase 2 book-planner·Phase 4 fact-checker 필독)

### 0-1. 소스 4종과 각각의 증거 능력

| 소스 | 파일 | 증거 능력 |
|------|------|-----------|
| **실측(probe)** | `research/env_probe.md` | 이 책을 쓴 맥 1대에서 직접 실행한 명령의 원본 출력. **표본 1. 일반화 금지.** "이 환경에서 관측됨"으로만 인용 |
| **웹(1차 소스)** | `research/web.md` + `research/web_gapfill.md` | 공식 문서·릴리스 노트·레지스트리 직접 조회. **버전·플래그·기본값의 유일한 근거** |
| **논문** | `research/papers.md` | 원리 챕터 뒷받침. 9편. **전부 조건부 수치** — 측정 연도·하드웨어 병기 없이 쓰면 안 됨 |
| **커뮤니티** | `research/community.md` | 실무자 고통·일화·논쟁. **버전·수치의 근거가 아님.** 인용은 "누가 언제 이렇게 말했다" 형태로만 |

> **다섯 파일 모두 보존 산출물이다** (`env_probe.md` · `web.md` · `web_gapfill.md` · `papers.md` · `community.md`). `01_reference.md` 합성 후에도 삭제·병합하지 않는다. Phase 4 fact-checker의 1차 대조 근거다.
>
> ⚠️ **`web.md`와 `web_gapfill.md`가 겹치는 주제에서는 `web_gapfill.md`가 최신·우선이다.** 특히 Jib(§8-2)·베이스 이미지(§8-3)·Docker Desktop 내장 K8s(§8-5)·`--load` 제약(§8-6)은 gapfill이 1차 리서치의 미확인·부분 서술을 교체했다.

### 0-2. 이 책의 fact-check 게이트는 BLOCKING이다

본문에 다음이 있으면 Phase 4에서 걸린다:

- 시점 없는 버전 주장 → 🕒. **모든 버전은 `"{버전}/{연도} 기준"` 형태로 못 박는다.**
- 레퍼런스에 근거 없는 수치·플래그·API → ❌
- probe 값을 일반화한 문장("Docker 최신 버전은 29.6.2다") → ❌
- 벤치마크 수치를 측정 연도·환경 없이 단독 사용 → 🕒
- 논문 3(arXiv 프리프린트)의 수치를 "프리프린트" 단서 없이 사용 → ⚠️

§신선도 원장(맨 아래)이 대조표다.

### 0-3. 커뮤니티 리서처의 "사용자 요구 번호"는 재매핑이 필요하다

`research/community.md`의 각 일화에 붙은 "연결되는 사용자 요구 1/2/3/4"는 커뮤니티 리서처가 **임의로 정의한 번호**다(1=원리 이해, 2=실무 판단 기준, 3=맥 실전, 4=운영 감각). **정전(canonical) 요구 번호와 다르다.** 이 문서 §3의 일화 표에 정전 번호로 재매핑해 두었다 — **그 표를 쓰고 원본 파일의 번호는 무시하라.**

정전 요구:
1. 맥 환경에서 Docker로 시스템을 개발할 때 알아야 할 것들
2. Spring Boot 앱을 컨테이너 이미지로 빌드해 배포하는 방법
3. 나만의 컨테이너 이미지를 만들고 **업데이트**하는 방법
4. Kubernetes는 언제 쓰는 기술인가 + 맥에서 써보려면 무엇을 해야 하는가

---

## 1. 개념과 정의

### 1-1. 컨테이너는 무엇인가 — 리눅스 커널 기능이다

컨테이너는 제품이 아니라 **리눅스 커널의 두 기능(네임스페이스 + cgroups)에 union filesystem을 얹은 조합**이다. 이 정의가 이 책 전체의 첫 단추다. 왜냐하면 **맥에는 리눅스 커널이 없기 때문이다.**

**네임스페이스** [웹 · man7 1차]
> "A namespace wraps a global system resource in an abstraction that makes it appear to the processes within the namespace that they have their own isolated instance of the global resource."
> — namespaces(7), Linux man-pages 6.18, 페이지 날짜 2026-02-08

8종 (man-pages 6.18 / 2026-02 기준):

| Namespace | Flag | 격리 대상 |
|---|---|---|
| Cgroup | `CLONE_NEWCGROUP` | Cgroup root directory |
| IPC | `CLONE_NEWIPC` | System V IPC, POSIX message queues |
| Network | `CLONE_NEWNET` | Network devices, stacks, ports |
| Mount | `CLONE_NEWNS` | Mount points |
| PID | `CLONE_NEWPID` | Process IDs |
| Time | `CLONE_NEWTIME` | Boot and monotonic clocks |
| User | `CLONE_NEWUSER` | User and group IDs |
| UTS | `CLONE_NEWUTS` | Hostname and NIS domain name |

**cgroups** [웹 · man7 1차]
> "Control groups, usually referred to as cgroups, are a Linux kernel feature which allow processes to be organized into hierarchical groups whose usage of various types of resources can then be limited and monitored."
> — cgroups(7), Linux man-pages 6.18, 2026-02-08

cgroups v2 컨트롤러: `cpu`, `cpuset`, `freezer`, `hugetlb`, `io`, `memory`, `perf_event`, `pids`, `rdma`. v1은 호환성 때문에 남아 있고, **v2는 아직 v1 컨트롤러의 부분집합만 구현**한다(man-pages 6.18 / 2026-02 기준).

> **자바 개발자에게 직결되는 연결고리:** JVM의 `UseContainerSupport`가 "읽는 것"이 바로 이 cgroup의 memory·cpu 제한이다(§5-4). 원리 → 실무가 한 줄로 이어진다.

**네임스페이스 생성 비용은 얼마인가** [논문 · ⚠️ arXiv 프리프린트]
> 7.94 ms (SSD, σ=2.05) / 8.45 ms (HDD, σ=2.57) — **전체 컨테이너 기동 시간의 1.5% 미만.** "Near-identical results confirm this is CPU-bound, not I/O-bound—a platform-invariant primitive."
> — Khan, arXiv:2602.15214 §4.2.1 (2026 측정, **동료심사 미확인 프리프린트**)

→ **"컨테이너 기동이 느린 건 리눅스 격리 원시요소 탓이 아니다."** 독자가 최적화 타깃을 잘못 잡는 것을 막는 데 최적인 수치.

### 1-2. OCI 이미지 — 태그 → 인덱스 → 매니페스트 → 레이어

[웹 · opencontainers/image-spec 1차]

- 매니페스트 미디어 타입: `application/vnd.oci.image.manifest.v1+json`. `schemaVersion`은 "MUST be `2` to ensure backward compatibility with older versions of Docker."
- config 미디어 타입: `application/vnd.oci.image.config.v1+json`
- layers: descriptor 배열. **인덱스 0이 base layer**, 이후 stack order
- 지원 레이어 타입: `...layer.v1.tar`, `...tar+gzip`, `nondistributable` 변형. `...tar+zstd`는 "SHOULD also support"
- digest는 SHA256

**이미지 인덱스(멀티아키 매니페스트 리스트):** `application/vnd.oci.image.index.v1+json`. 태그 하나가 아키텍처별 매니페스트 여러 개를 가리키는 구조다. 이 책에서는 **실물 응답으로 보여줄 수 있다** — §5-2의 Paketo 빌더 조회 결과가 정확히 이 형태다.

> **책 구성 제안:** "태그 → 인덱스 → 매니페스트 → 레이어 digest" 사슬은 mermaid 다이어그램 1순위 후보다. arm64 함정 챕터의 개념적 토대이기도 하다.

### 1-3. 왜 맥에서는 리눅스 VM이 끼는가

컨테이너 = 리눅스 커널 기능(§1-1) → macOS 커널(XNU)은 리눅스 커널이 아니다 → **리눅스 커널을 어디선가 가져와야 한다** → 경량 리눅스 VM.

그래서 맥 사용자가 실제로 치르는 비용은 [논문 프레이밍]:

```
독자가 보는 비용 = [컨테이너 오버헤드] + [VM 오버헤드] + [호스트↔게스트 파일/네트워크 경계]
                    ↑ 논문들이 측정한 것    ↑ 논문들이 대부분 측정하지 않은 것
```

**⭐ 이 책 전체에서 가장 강력한 인용 (챕터 오프닝 훅 최강):** [논문 1차]
> "We also question the practice of deploying containers inside VMs, since this imposes the performance overheads of VMs while giving no benefit compared to deploying containers directly on non-virtualized Linux."
> — Felter et al., ISPASS 2015, p.172 (**2014년 측정** 병기 필수)

2015년 IBM 연구자들이 "컨테이너를 VM 안에 넣는 관행"에 의문을 제기했는데, **그게 정확히 Docker Desktop on Mac의 구조다.** 11년 뒤 독자의 맥북이 그 구조로 돌고 있다.

### 1-4. Docker Desktop이 맥에서 도는 방식 — VMM·파일공유·Rosetta 3자 트레이드오프

[웹 · Docker 공식 문서 1차, 2026-07-25 검색]

**VM 매니저(VMM) 선택지 3종** (설정 이름 그대로):

| VMM | 공식 서술 | Rosetta |
|---|---|---|
| **Docker VMM** | "the latest and most performant Hypervisor/Virtual Machine Manager. This option is available only on Apple Silicon Macs and is in **Beta**." 최소 4GB 메모리 필요 | **미지원** — "Docker VMM does not currently support Rosetta, so emulation of amd64 architectures is slow." |
| **Apple Virtualization framework** | "A stable and well-established option for managing virtual machines on Mac" | 지원 (Rosetta 옵션의 전제 조건) |
| QEMU / HyperKit | Legacy / deprecated 표기 | — |

> ⚠️ **기본 VMM이 무엇인지는 공식 문서에서 확인하지 못했다(미확인).** 책에 "기본은 X다"라고 쓰지 말 것.

**⭐ 이 절의 핵심 판단 기준:** Rosetta 옵션은 **"Apple Virtualization framework를 VMM으로 선택했을 때만" 나타난다**(기본값 Disabled). 즉 **최신·최고 성능이라는 Docker VMM을 고르면 Rosetta를 못 쓴다.** amd64 에뮬레이션 성능을 원하면 VMM 선택 자체가 트레이드오프다. 이건 설정 화면만 봐서는 절대 안 보이는 관계다.

**파일 공유:**
- VirtioFS(기본) / gRPC FUSE
- > "VirtioFS has reduced the time taken to complete filesystem operations by up to 98%."
- > "It is the only file sharing implementation supported by Docker VMM."
- ⚠️ Docker VMM 경고: "Certain databases, like MongoDB and Cassandra, may fail when using virtiofs with Docker VMM."

**리소스 기본값:** 메모리 한도 = "Defaults to 50% of your host's memory." / Swap "1 GB default" / "Include VM in Time Machine backups" 기본 Disabled

**라이선스 임계값** [웹 · docker.com 공식 라이선스 페이지 1차]
> 무료: "Small businesses (**fewer than 250 employees AND less than $10 million in annual revenue**)". 그 외 "Professional use in larger organizations", "Government entities"는 유료 구독 필요.

→ **AND 조건이다.** 한쪽만 넘어도 유료. 한국 중견기업 독자에게 실질적으로 중요한 지점이다. (2026-07 검색 기준)

### 1-5. 격리(isolation) ≠ 보안(security)

이 구분이 이 책의 원리 챕터가 세워야 할 두 번째 기둥이다.

**학술 근거** [논문 1차]
> "We find the kernel security mechanisms such as Capability, Seccomp, and MAC play a more important role in preventing privilege escalation than the container isolation mechanisms (i.e., Namespace and Cgroup)."
> — Lin et al., ACSAC '18 (2018년 측정, Docker 17.09.1-ce 기준)

같은 논문: 실제 동작하는 익스플로잇 223건을 수집해 대표 88건으로 측정, **88건 중 50건(56.82%)이 Docker 기본 설정 컨테이너 안에서 공격에 성공**했고 **11건은 격리를 뚫고 권한 상승**에 성공했다(전부 공통된 4단계 공격 모델). 저자들은 기제 간 상호의존 때문에 **"short board effect"**(최약 링크가 방어력을 결정)에 빠질 수 있다고 지적한다.

> 🕒 **수치는 2018년 취약 커널 조합 기준이다.** 오늘날 패치 커널의 성공률이 아니다. **구조적 결론(어느 기제가 방어에 기여하는가)을 인용하고 수치는 조건 병기.**

**업계의 답변 — AWS는 컨테이너로 고객을 격리하지 않는다** [논문 1차]
> "The traditional view is that there is a choice between virtualization with strong security and high overhead, and container technologies with weaker security and minimal overhead. This tradeoff is unacceptable to public infrastructure providers, who need both strong security and minimal overhead."
> — Agache et al., NSDI '20 Abstract (Firecracker)

Firecracker 설계 목표치(**2020년 발표 시점 기준**): 컨테이너당 메모리 오버헤드 5MB 미만, 애플리케이션 코드까지 부팅 125ms 미만, 호스트당 초당 최대 150개 MicroVM 생성.

### 1-6. OCI / CRI / containerd / runc — "도커가 쿠버네티스에서 빠졌다"의 진실

[웹 · Kubernetes 공식 블로그 1차, 2022-02-17 발행]

> "The CRI standard was created to enable interoperability between orchestrators (like Kubernetes) and many different container runtimes. Docker Engine doesn't implement that interface (CRI), so the Kubernetes project created special code to help with the transition, and made that _dockershim_ code part of Kubernetes itself."
> "The dockershim code was always intended to be a temporary solution (hence the name: shim)."
> "The dockershim removal occurred in **Kubernetes 1.24**."

**⭐ 자바 개발자의 가장 흔한 오해를 한 문장으로 끝내는 인용:**
> "Yes, the images produced from `docker build` will work with all CRI implementations. **All your existing images will still work exactly the same.**"

→ "도커가 빠졌다"는 **이미지가 못 쓰이게 됐다는 뜻이 아니다.** 이미지 포맷은 OCI 표준이고, 빠진 것은 쿠버네티스가 Docker Engine과 대화하던 어댑터다.

> ⚠️ 이 글은 2022년 글이다. 다만 "제거됐다"는 확정 사실이라 신선도 리스크가 낮다. 그래도 "2022년 발표, Kubernetes 1.24에서 제거" 형태로 시점을 붙일 것.

---

## 2. 핵심 관점들

### 2-1. ⭐ 아키텍처 — 이 책의 중심축

**핵심 명제:** Apple Silicon 맥에서 아무 설정 없이 이미지를 만들면 **arm64 이미지**가 나온다. 운영 서버가 amd64면 그 이미지는 거기서 돌지 않는다. 그런데 **맥에서는 경고만 뜨고 돌아가기 때문에** 개발자가 배포 시점까지 모른다.

**멀티 플랫폼 빌드 3전략** [웹 · Docker 공식 1차]
1. "Using emulation, via QEMU"
2. "Use a builder with multiple native nodes"
3. "Use cross-compilation with multi-stage builds"

명령 형태(문서 그대로):
```
docker buildx build --platform linux/amd64,linux/arm64 .
docker build --platform linux/amd64,linux/arm64 -t multi-platform .
```

**함정 1 — 만들었는데 `docker images`에 안 보인다** [웹 · Docker 공식 1차]
> "Builds with the `docker-container` driver aren't automatically loaded to your Docker Engine image store."

→ `--load` 또는 `--push`를 안 붙이면 결과물이 로컬에 없다.

**함정 2 — 클래식 이미지 스토어는 멀티아키를 담지 못한다** [웹 · Docker 공식 1차]
> "It doesn't support image indices or manifest lists, so you can't load multi-platform images locally or build images with attestations."

**containerd image store 기본 활성 조건:** "The containerd image store is enabled by default in **Docker Desktop version 4.34 and later**."

> ⚠️ **버전 앵커가 두 개인 이유 (fact-checker 주의).** 이 문서에는 containerd 스토어 기본 활성에 대한 **서로 다른 두 버전 표기**가 나온다 — **Docker Desktop 4.34+**(위, Desktop 제품 라인)와 **Docker Engine 29.0+**(§8-6, Engine 제품 라인). **둘 다 원문 그대로이며 모순이 아니다. 제품 라인이 다르다.** Desktop은 Engine을 번들하는 별개 제품이다(4.83.0이 Engine 29.6.2를 번들 — §2-4). 책에서 인용할 때 **어느 제품의 버전인지 반드시 명시**할 것. 뭉뚱그리면 fact-checker가 충돌로 판정한다.

> ⛔⛔ **여기서 멈추면 틀린 책이 된다.** "멀티플랫폼은 `--load` 못 한다"를 **절대 규칙으로 쓰면 이 책 독자 다수에게 틀린 지시가 된다.** Docker 문서 두 곳이 충돌하는 것처럼 보이는 지점이고, **§8-6에서 세 번째 1차 소스로 해소했다** — 조건은 **classic 그래프 드라이버(overlay2) vs containerd 스토어**이며, **Docker Desktop과 Docker Engine 29.0+ 신규 설치는 기본이 containerd라 멀티플랫폼을 로컬에 담을 수 있다.** 반드시 §8-6의 조건부 서술을 따를 것.

→ 이 문장들이 "왜 `--platform a,b` 뒤에 `--push`를 요구하는 경우가 있는가"를 설명한다. **그리고 이 토글이 실제로 빌드 결과를 바꾼다** — §4-6·§5-1 H4 참조.

**증상은 하나가 아니다** [커뮤니티 · 🟡 반복 패턴]

아키텍처 불일치의 근본은 "이 바이너리는 이 CPU의 것이 아니다" 하나인데, **얼굴이 다섯 개다.** 이게 진단이 어려운 이유다.

| # | 실제 메시지 | 성격 | 출처 / 시점 |
|---|------------|------|------------|
| ① | `exec /entrypoint.sh: exec format error` | 커널이 바이너리 헤더 거부 | docker/for-mac#7849 / 2026-02 |
| ② | `exec /bin/sh: exec format error` (busybox조차) | 동일 — **문제 범위가 "내 이미지"가 아님을 증명** | 위 이슈 댓글 / 2026-02 |
| ③ | `exec /cnb/process/web: exec format error` | buildpack 런치 프로세스 | paketo/spring-boot#491 / 2024-06 |
| ④ | `fork/exec .../ca-certificates-helper: exec format error` | **헬퍼 스크립트만** 실패 (캐시 오염, 나머지 레이어는 정상) | paketo/spring-boot#491 / 2024-06 |
| ⑤ | `qemu: uncaught target signal 11 (Segmentation fault) - core dumped` | **에뮬레이션은 시작됐는데 도중에 죽음** | docker/for-mac#7172 / 2024-02 |

> ⛔ **정확성 주의:** ⑤는 `exec format error`가 **아니다.** ①~④는 "실행 자체가 거부됨", ⑤는 "QEMU가 amd64 바이너리를 돌리다 중간에 죽음"이다. 원인도 진단 경로도 다르다. 책에 **"exec format error가 세그폴트로 나타나기도 한다"고 쓰면 틀린다.** "에뮬레이션 실패는 `exec format error`가 아닌 형태로도 나타난다"로 쓸 것.
> **⑤가 특히 잔인한 이유:** 아키텍처 문제인데 에러 메시지에 아키텍처라는 단어가 한 번도 안 나온다.

**⭐ 같은 경고 템플릿, 정반대 두 방향** [커뮤니티]

Docker의 경고는 하나의 템플릿이다:
```
WARNING: The requested image's platform ({이미지}) does not match the detected host platform ({호스트})
```

그런데 확보한 두 사례는 **방향이 반대다. 이 구분이 이 책이 가르쳐야 할 핵심이다.**

| 방향 | 어디서 터졌나 | 원인 주체 | 출처 |
|------|--------------|----------|------|
| **amd64 이미지 → arm64 맥** | 맥에서는 **경고만 뜨고 돌아감**. 죽은 곳은 arm64 클라우드 VM | **빌드 도구가 결정**(Paketo가 amd64를 만듦) | paketo/spring-boot#491, 2024-06-21 |
| **arm64 이미지 → amd64 서버** | M1 맥에서 빌드 → EC2 배포 시점에 처음 발견 | **호스트가 결정**(맥이 arm64니까) | velog @msung99, 2023-01-05 `(원문 대조 필요)` |

**공통 패턴:** 맥에서는 경고만 뜨고 돌아간다 → 개발자가 무시한다 → 배포 대상에서 처음 죽는다. **"로컬에서 잘 됐는데요"의 컨테이너판.**
**차이:** 원인이 다르므로 처방도 다르다.

**⚠️ `exec format error`를 정면으로 설명하는 Docker 공식 문서 페이지는 확보하지 못했다(미확인).** 책에서는 증상 문자열을 공식 문서 인용인 것처럼 쓰지 말고, 원인을 1차 소스 조합으로 재구성하거나(§1-2 OCI 인덱스 + §2-1 이미지 스토어 한계 + §5-2 플랫폼 기본값) 저술 시점에 직접 재현해 캡처할 것.

### 2-2. Rosetta는 "켜면 빨라지는 스위치"가 아니다

[커뮤니티 · 🟡 다수 재현 / docker/for-mac#7075, 2023-11 등록, **2026-07-25 조회 시점 OPEN**]

M2 Max 맥북 프로 사용자가 Rosetta를 **켠** 상태로 amd64 빌드:
```
[+] Building 33656.6s (15/22)
 => [builder 5/5] RUN yarn build      33186.8s
```
**33,656초 = 약 9시간 21분.** 밤새 돌려놓고 아침에 왔는데 아직 안 끝나 있었다.

같은 증상 다수(M1 / M2 Max / M3 Max / M3 Pro, 2023-11 ~ 2024-06):
- `alnaranjo`: "Using 4.25.x would cause docker build to hang indefinitely even when disabling 'use rosetta'. **Building arm images is a breeze, though.**"
- `iaurg` (M1 Air): "Sometimes, the computer just crashes because resources are completely used by Docker, forcing me to reset the OS."
- `AlexandreRoba` (M3 Max 64GB): 껐더니 **5분 만에** 빌드
- `jinmel` (2024-06-29, 이슈가 닫힌 뒤): "why is this closed? I think the issue persists for latest macbook users"

**⛔ 결론: 책에 "Rosetta를 켜면 빨라진다"고 쓰면 안 된다.** 워크로드에 따라 켜면 느려지고, Docker Desktop 버전에 따라 결과가 뒤집힌다. **가장 확실한 처방은 "에뮬레이션을 안 하는 것"이다.**

**⚠️ Rosetta 활성화 시 amd64 성능 수치는 공식 문서에 없다(미확인).** Docker 공식은 정성 서술("emulation ... is slow")만 한다. 커뮤니티 수치(33,656초)는 **한 사람의 한 환경**이며 벤치마크가 아니다.

### 2-3. 클라이언트와 데몬은 다른 물건이다 — 이 책 고유의 실측 자산

[**실측(probe) · 이 책을 쓴 맥, 2026-07-25**]

```
$ command -v docker
/Users/tobylee/.rd/bin/docker        # 실행되는 CLI = Rancher Desktop의 것

$ docker --version
Docker version 27.5.0-rd            # 클라이언트: 27.5.0-rd

$ docker context ls
default           unix:///var/run/docker.sock
desktop-linux *   unix:///Users/tobylee/.docker/run/docker.sock   # 활성 context = Docker Desktop

$ echo "${DOCKER_HOST:-(unset)}"
(unset)

$ docker info --format '{{.ServerVersion}} / {{.OperatingSystem}} / {{.Architecture}}'
29.6.2 / Docker Desktop / aarch64   # 데몬: Docker Desktop 29.6.2
```

**관측된 사실:** PATH가 잡은 CLI는 Rancher Desktop 것인데, context가 가리키는 데몬은 Docker Desktop 것이다. `DOCKER_HOST`는 unset이므로 **접속 대상을 결정한 것은 환경변수가 아니라 `docker context`**다.

**공식 문서가 이 관측을 설명한다** [웹 · Docker 공식 1차]
> "all `docker` commands run against this context, unless overridden with environment variables such as `DOCKER_HOST` and `DOCKER_CONTEXT`, or on the command-line with the `--context` and `--host` flags."

→ 우선순위: **CLI 플래그 > 환경변수(`DOCKER_CONTEXT`/`DOCKER_HOST`) > 활성 context**

**⚠️ 다만 "PATH가 잡은 CLI와 context가 가리키는 데몬이 서로 다른 제품"이라는 교차 상황 자체는 공식 문서가 다루지 않는다(미확인).** 그래서 이 실측이 이 책의 고유 가치다.

**커뮤니티에서 짝을 이루는 사례는 확보했으나 플랫폼이 다르다** [커뮤니티 · 🔴 단일 · **Windows 사례**]
> "when [Docker Desktop] starts it changes the docker context ... **any command issued in a terminal will fail until the context is reset to `default` with `docker context use default`**"
> — rancher-desktop#7712, 2024-11-01, OPEN

> ⛔ **이 보고는 Windows다. 맥 사례로 둔갑시키지 말 것.** 책에서는 "커뮤니티에는 Windows 사례가 보고돼 있고, 이 책을 쓴 맥에서는 실측으로 클라이언트/데몬이 갈린 상태가 관측됐다"로 **두 근거를 분리해서** 쓴다. 실패의 *구조*는 같다: 런타임 두 개가 `docker context`라는 하나의 전역 상태를 놓고 다투고, 아무도 사용자에게 알려주지 않는다.

**왜 사람들이 런타임을 두 개 깔아두는가** [커뮤니티] — `styfle`의 한마디가 심리를 정확히 짚는다:
> "I have a machine with Colima and don't want to bork it if I try Orbstack. ... Is "brew install orbstack" a drop in replacement for colima or does it install other things that might conflict?"

→ 지우기는 무서우니까 일단 같이 깔아둔다. `env_probe.md`가 보여주는 상태가 정확히 그 결과다.

### 2-4. 대안 런타임 — 공개 릴리스 라인 (2026-07-25 조회)

| 도구 | 최신 릴리스 | 날짜 | 근거 강도 |
|---|---|---|---|
| Docker Desktop | **4.83.0** | **2026-07-20** | 강 (릴리스 노트 본문 인쇄값) |
| Rancher Desktop | v1.23.1 | 2026-06-29 | 약 (GitHub Releases 날짜 추출 신뢰성 문제 — §4-8) |
| Podman Desktop | v1.28.3 | 2026-07-20 | 약 (동일) |
| Colima | v0.10.3 | 2025-06-04 | 약 (동일) |
| **OrbStack** | **미확인** | — | 조회하지 않음 |

Docker Desktop 4.83.0 번들 구성(릴리스 노트 표기 그대로): Docker Engine **v29.6.2** / Docker Compose **v5.3.1** / Docker Desktop Build v0.36.0 / Docker Desktop CLI v0.4.2 / Docker Model Runner v1.2.6 / Docker Offload v0.6.9 / Docker Agent v1.103.0

인접 릴리스: 4.82.0(2026-07-13), 4.81.0(2026-07-06), 4.80.0(2026-06-29, Engine v29.6.1), 4.79.0(2026-06-22)
→ 주 단위 리듬으로 **보이지만** 문서가 "주 1회"라고 명시하진 않았다. **날짜 나열만 근거로 제시하고 주기를 단정하지 말 것.**

> ⚠️ **Colima의 최신 릴리스가 2025-06-04라는 것은 2026-07 기준 1년 이상 새 릴리스가 없다는 뜻이다.** 책에 "활발히 개발 중"이라고 쓰지 말 것 — 관측된 사실만 쓰고 판단은 독자에게 넘긴다.

> ⚠️ **Rancher Desktop의 containerd vs dockerd(moby) 선택과 `nerdctl` 사용법은 공식 문서를 확보하지 못했다(미확인).** 확보된 것은 실측으로 `~/.rd/bin`에 `nerdctl`·`rdctl`·`helm`·`kuberlr`가 함께 설치된다는 관측뿐이다.

### 2-5. 이미지를 만들고 **업데이트**한다는 것 (요구 3번의 뼈대)

**캐시 재사용 규칙** [웹 · Docker 공식 1차]
> "a layer is reused from the build cache if **the instruction and the files it depends on hasn't changed** since it was previously built." 그리고 "a change causes a rebuild for steps that follow."

`.dockerignore`: "Ignore-rules specified in the `.dockerignore` file apply to the **entire build context, including subdirectories**."

**⭐ 태그는 고정된 이미지를 가리키지 않는다** [웹 · Docker 공식 1차]
> "If you specify `FROM alpine:3.21` in your Dockerfile, `3.21` resolves to the **latest patch version** for `3.21`."

→ **같은 Dockerfile이 어제와 오늘 다른 이미지를 만든다.** 이 한 문장이 요구 3번("업데이트") 챕터의 출발점이다.

**digest 고정** [웹 · Docker 공식 1차]
> "By pinning your images to a digest, you're guaranteed to always use the same image version, even if a publisher replaces the tag with a new image."
```dockerfile
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

**⭐ 업데이트 워크플로의 실제 명령 — 두 플래그의 차이가 이 절의 뼈대다** [웹 · Docker 공식 1차]
> `--pull`: "forces Docker to check for and download a **newer version of the base image**, even if you have a version cached locally."
> `--no-cache`: "**disables the build cache**, forcing Docker to rebuild all layers from scratch."

```
docker build --pull -t my-image:my-tag .
docker build --no-cache -t my-image:my-tag .
docker build --pull --no-cache -t my-image:my-tag .
```

→ **digest로 고정했으면 `--pull`은 아무것도 안 바꾼다**(같은 digest니까). **태그로 뒀으면 `--pull`이 베이스 패치를 끌어온다.** 캐시 무효화는 또 다른 문제다. 이 세 갈래를 구분해 가르치는 것이 요구 3번의 핵심이다.

**BuildKit 캐시 마운트** [웹 · Docker 공식 1차, 문서 예시 그대로]
```dockerfile
RUN --mount=type=cache,target=/root/.npm npm install
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked apt update && apt-get install -y gcc
```
> ⚠️ **Gradle(`/root/.gradle`) 예시는 문서에 없다.** 책에 쓰려면 "문서의 원리를 Gradle에 적용하면"이라고 밝히고 직접 검증할 것.
> ⚠️ `--mount=type=secret` 예시는 이 페이지에서 확인하지 못했다(미확인).

**외부 캐시 백엔드** [웹 · Docker 공식 1차]
```
docker buildx build --cache-from type=registry,ref=user/app:buildcache .
cache-to: type=registry,ref=user/app:buildcache,mode=max
```

**레이어 정리 원칙** [웹 · Docker 공식 1차]
- "Always combine `RUN apt-get update` with `apt-get install` in the same `RUN` statement." (캐시 때문에 update가 낡은 채 굳는 고전 함정)
- "Whenever possible, sort multi-line arguments alphanumerically"
- 멀티스테이지: "let you reduce the size of your final image, by creating a cleaner separation between the building of your image and the final output"

**취약점 스캔 — Docker Scout** [웹 · Docker 공식 1차]
> "Docker Scout is a solution for proactively enhancing your software supply chain security."
> SBOM: 이미지를 분석해 "compiles an inventory of components, also known as a Software Bill of Materials (SBOM)" 하고 "matched against a continuously updated vulnerability database".

> ✅ **G4 해소 (§8-4).** 하위 명령 **19개** 전체 목록 확보. 요구 3번에 직결되는 것은 `quickview` / `cves` / **`recommendations`("베이스 이미지 업데이트 권고")** / `sbom`. **`compare`·`policy`·`environment`·`stream`은 문서에 `(experimental)` 표시가 있으니 병기 필수.**
> ✅ **번들 여부도 확정:** "The Docker Scout CLI plugin **comes pre-installed with Docker Desktop.**" → 맥 독자는 추가 설치 없이 실습 가능.

**⭐ "이미지는 만들어 놓고 끝이 아니다"의 결정타** [논문 1차]
> "Vulnerability patching of software in Docker images is significantly delayed by **422 days on average**."
> — Liu et al., ESORICS 2020 §1 (**2019년경 수집** 병기 필수)

같은 논문(약 220만 개 이미지 조사, 2019년경):
- 커뮤니티 이미지 **64% 초과**가 고위험/치명 취약점 보유. 공식 이미지는 최신본의 약 30%
- 악성 이미지 42개 발견(원격 코드 실행, 크립토마이닝). **공식 저장소 147개 최신 이미지에서는 악성 실행 프로그램 0건**
- 저장소 설명의 권장 `docker run` 명령당 **민감 파라미터 평균 1개**(예: `--privileged`), 그리고 "users are not aware of the threats ... they will directly execute run-commands specified by developers without checking"

> 🕒 **그 이후 Docker Hub는 Docker Scout·자동 스캔·Verified Publisher 등을 도입했다. 42건·422일·64%를 현재형으로 쓰면 안 된다.** 재측정값은 확보하지 못했다.

**⭐ 이미지 다이어트는 언제 효과가 있고 언제 없는가 — 이번 논문 리서치의 최대 산출**

두 논문을 짝지어야 뉘앙스가 정확해진다:

| 상황 | 이미지 크기의 영향 | 근거 |
|------|------------------|------|
| **cold path (pull 포함)** | **기동 시간의 76%가 pull. 그중 실제 읽히는 데이터는 6.4%** | Harter et al., FAST '16 (2016 측정) |
| **warm start (이미 pull됨)** | 5MB(alpine) ~ 155MB(python:3.11-slim) 사이 편차가 **554–568ms, 즉 2.5%** | Khan, arXiv:2602.15214 Finding 1 (2026, **프리프린트**) |

> "pulling packages accounts for 76% of container start time, but only 6.4% of that data is read." — Harter et al., FAST '16 Abstract

→ **"이미지를 줄이면 빨라진다"는 조건부 참이다.** 배포 파이프라인(cold)에서는 크게 효과가 있고, 로컬 재기동(warm)에서는 거의 없다. 이 구분 없이 "슬림 베이스를 쓰자"고 하면 독자가 잘못된 곳에 시간을 쓴다.

**같은 계보의 세 번째 점** [논문 1차]
> "Task startup latency ... median typically about 25 s. **Package installation takes about 80% of the total**"
> — Verma et al., EuroSys '15 §3.4 (Google Borg, 2015 기준. **Borg는 Kubernetes가 아니다** — 수치를 K8s 수치처럼 쓰지 말 것)

→ **Borg(2015) → Slacker(2016) → 오늘날 레이지 풀링(eStargz/SOCI/Nydus)** 이라는 서사 한 줄이 만들어진다.

### 2-6. Kubernetes — 언제 쓰고 언제 쓰지 않는가 (요구 4번)

**⭐ 공식 문서가 직접 기대를 반박한다** [웹 · kubernetes.io 공식 1차]

"What Kubernetes is not" 원문:
> "Kubernetes is not a traditional, all-inclusive PaaS (Platform as a Service) system."
> "**Does not deploy source code and does not build your application.** Continuous Integration, Delivery, and Deployment (CI/CD) workflows are determined by organization cultures and preferences..."
> "**Does not provide application-level services**, such as middleware (for example, message buses), data-processing frameworks (for example, Spark), databases (for example, MySQL), caches, nor cluster storage systems (for example, Ceph) as built-in services."
> "**Does not dictate logging, monitoring, or alerting solutions.**"
> "Does not provide nor mandate a configuration language/system (for example, Jsonnet)."
> "Does not provide nor adopt any comprehensive machine configuration, maintenance, management, or self-healing systems."
> "Additionally, Kubernetes is not a mere orchestration system. In fact, **it eliminates the need for orchestration.** ... Kubernetes comprises a set of independent, composable control processes that continuously drive the current state towards the provided desired state."

→ **"K8s를 도입하면 배포가 해결된다"는 기대를 공식 문서가 정면으로 반박한다.** 빌드도 CI/CD도 DB도 로깅도 안 준다. **이 목록을 그대로 "K8s가 당신에게 안 해주는 것" 절로 쓰면 챕터 하나가 선다.**

반대편 목록(공식 "Why you need Kubernetes and what it can do"): Service discovery and load balancing / Storage orchestration / Automated rollouts and rollbacks / Automatic bin packing / Self-healing / Secret and configuration management / Batch execution / Horizontal scaling / IPv4-IPv6 dual-stack / Designed for extensibility

**현재 지원 버전대와 릴리스 주기** [웹 · kubernetes.io 공식 1차, 2026-07-25 검색]

| Minor | Latest Patch | Release Date | End of Life |
|---|---|---|---|
| 1.36 | 1.36.2 | 2026-06-09 | 2027-06-28 |
| 1.35 | 1.35.6 | 2026-06-09 | 2027-02-28 |
| 1.34 | 1.34.9 | 2026-06-09 | 2026-10-27 |

> "The Kubernetes project maintains release branches for the most recent **three** minor releases (1.36, 1.35, 1.34)."
> "Kubernetes 1.19 and newer receive **approximately 1 year of patch support**."
> "**Kubernetes releases currently happen approximately three times per year.**"

> ⚠️ **"연 4회/분기별"이 아니다.** 공식 문장은 "approximately three times per year"다. 이 값은 도구 요약이 "quarterly"라고 잘못 추정했던 항목이라 특히 주의(§4-8).
> ⚠️ 릴리스 사이클 구조(Normal Dev 1~11주 → Code Freeze 12~14주 → Post-Release)에서 "약 14~16주 사이클"을 **유도할 수는 있으나 문서의 문장이 아니다.** 쓰려면 유도임을 밝힐 것.

**실측이 주는 버전 skew 소재:** 이 맥의 `kubectl` client는 **v1.32.1**로, 위 지원 범위(1.34~1.36)보다 낮다. **지원 종료된 마이너 라인의 클라이언트다.** "정상 상태"가 아니라 버전 skew를 설명할 실물 소재로 쓸 것.

**맥에서 로컬 K8s에 내 이미지 올리기** [웹 · 각 도구 공식 1차]

**kind:**
```
kind create cluster
kind create cluster --name kind-2
kind load docker-image my-app:latest
kind load docker-image my-app:latest my-db:latest my-cache:latest
kind load image-archive /my-image-archive.tar
```
- ⭐ **pull policy 함정(공식 문장):** "The Kubernetes default pull policy is `IfNotPresent` **unless the image tag is `:latest`**...in which case the default policy is `Always`." → 해결: `:latest`를 쓰지 않거나 `imagePullPolicy: IfNotPresent`/`Never` 명시
- 런타임 자동 감지: "can auto-detect the docker, podman, or nerdctl installed and choose the available one." → **Rancher Desktop만 깐 맥에서도 nerdctl 경유로 동작 여지가 있다**
- 최신 릴리스 v0.32.0, 기본 노드 이미지 `kindest/node:v1.36.1` (**날짜는 폐기 — §4-8**)

**minikube:**
```
eval $(minikube docker-env) && docker build -t my_image .
minikube image load my_image
minikube image build -t my_image .
minikube cache add alpine:latest / cache reload / cache list
minikube addons enable registry
  docker build --tag $(minikube ip):5000/test-img . && docker push $(minikube ip):5000/test-img
```
- 공통 함정(공식): "Remember to turn off the `imagePullPolicy:Always` (use `imagePullPolicy:IfNotPresent` or `imagePullPolicy:Never`)"
- 실측: 이 맥의 minikube는 v1.35.0

**⭐ Docker Desktop 내장 Kubernetes — "체크박스 하나" 모델이 아니다** [웹 · Docker 공식 1차, G5 해소 / 상세 §8-5]

> "Select **Create cluster**. Choose your cluster type: **Kubeadm** creates a single-node cluster and the version is set by Docker Desktop. **kind** creates a multi-node cluster and you can set the version and number of nodes."

공식 비교표에서 **실무적으로 가장 아픈 항목:**

| | kubeadm | kind |
|---|---|---|
| 멀티 노드 / 버전 선택 | No / No | Yes / Yes |
| 프로비저닝 속도 | ~1 min | ~30 seconds |
| **Docker image store 호환** | Yes | **No** |
| containerd image store 호환 | Yes | Yes |

→ ⭐⭐ **kind는 Docker image store와 호환되지 않는다.** 로컬에서 `docker build`한 이미지를 kind 클러스터가 바로 못 본다는 뜻이고, **자바 개발자가 "로컬 빌드 → 로컬 클러스터 배포" 흐름에서 정확히 부딪히는 벽**이다. 요구 4번 챕터의 핵심 실습 함정.

> ⛔ **번들 Kubernetes 버전은 "미확인"이 아니라 "문서에 명시 없음"으로 확정됐다.** 문서가 안내하는 것은 직접 확인뿐이다 — "check which version of Kubernetes you're on with: `kubectl version`". **책에 특정 버전 숫자를 쓰지 말고 `kubectl version`으로 확인하라고 안내할 것.**
> ⛔ **Ingress 예제, k3s(Colima) 경로, 로컬 K8s 리소스 소모 비교는 1차 소스가 전혀 없다. Phase 2는 이 세 소절을 계획에 넣지 말거나, 넣는다면 저술 시점에 직접 확보해야 한다.**

**⭐ `kubectl` 컨텍스트 사고 — 실측과 사고담이 정확히 짝을 이루는 지점**

실측 [probe §5]:
```
$ kubectl config get-contexts
CURRENT   NAME
          docker-desktop
          minikube
*         tobyilee@web-quickstart.ap-northeast-2.eksctl.io   ← 원격 EKS
```
로컬 클러스터가 둘이나 있는데 **활성 컨텍스트는 원격 EKS다.**

사고담 [커뮤니티 · HN 41578274, 댓글 2024-09-21]:
> "Hah! I accidentally deleted a production deployment the other day, because I thought it was mucking with my local Colima Kubernetes's cluster. **I forgot that I had my context set to one of my AWS clusters.**" — `millerm`

→ **가설이 아니라 실측 + 실제 사고담이 동시에 확보됐다.** 이 책 전체에서 가장 강한 오프닝 재료 중 하나다.

---

## 3. 대표 사례 (챕터 오프닝 후보)

> **Phase 2 book-planner에게:** 아래 일화들은 `research/community.md`에 본문·댓글 전문이 확보된 것들이다. 원문 인용문이 필요하면 그 파일의 해당 절을 열어라. 여기 실린 인용문은 전부 축자(verbatim)다.
> `tech-book` 프로필의 **오프닝 메뉴**(상황 가정 / 수사적 질문 / 충격적 수치 / 인용·일화 / 실패 장면 / 앞 장 콜백 / 정의 뒤집기)에 매핑해 두었다. **인접 챕터가 같은 기법을 반복하지 않도록**, 그리고 '상황 가정'이 전체의 1/3을 넘지 않도록 분산할 것.
>
> ⛔ **요구 3번(이미지 만들기·업데이트)에는 일화가 사실상 없다.** 아래 표에서 요구 3번에 매핑되는 것은 A4 하나뿐이고 그마저 요구 2번과 공유한다. 커뮤니티 리서치가 해당 주제 3종에서 모두 0건을 반환했다. **일화를 찾지 말고 §7-2의 "충격적 수치" 오프닝 대안 표를 쓸 것.**
> ⚠️ **분포 주의:** 아래 후보는 '실패 장면'과 '인용·일화'에 크게 쏠려 있다. 그대로 배분하면 책 전체가 한 리듬에 갇힌다. 수사적 질문·정의 뒤집기·충격적 수치를 의도적으로 끼워 넣을 것.

| # | 일화 | 정전 요구 | 오프닝 기법 후보 | 신뢰도 | 출처 / 시점 |
|---|------|----------|-----------------|--------|------------|
| A1 | **busybox조차 안 돌아간다** — M4 맥에서 amd64 에뮬레이션 자체가 죽음. Docker 모더레이터가 `--platform=linux/amd64 busybox`로 범위를 좁히자 `exec /bin/sh: exec format error`. **미해결로 종결** | 1 | 실패 장면 / 수사적 질문 | 🔴 단일 + 🟢 메인테이너 가설 | docker/for-mac#7849, 2026-02-05 등록 / 2026-04-30 재현불가 CLOSED |
| A2 | **곁가지:** 원인을 못 찾고 VM 매니저를 바꿔봤다가 Docker가 아예 안 뜸 → 공장 초기화. "(note: I did loose all my containers, images, and volumes)" | 1 | 실패 장면 | 🔴 단일 | 위 이슈 댓글, 2026-02-25 |
| A3 | **로컬에선 잘 돌던 이미지가 클라우드에서 즉시 죽었다** — M1 맥의 `bootBuildImage` 산출물이 **amd64**였다. 맥에선 경고만 뜨고 돌았고, arm64 클라우드 VM에서 `exec /cnb/process/web: exec format error` | **2** | 정의 뒤집기 / 실패 장면 | 🔴 단일 + 🟢 Paketo 메인테이너 처방 | paketo-buildpacks/spring-boot#491, 2024-06-21 CLOSED |
| A4 | **고친 줄 알았는데 캐시가 발목** — 빌더를 바꿨는데도 `ca-certificates-helper: exec format error`. 🟢 dmikusa: "you've got some layers that were cached... **it's not updating those cached layers with ARM64 binaries**" | 2, 3 | 앞 장 콜백 | 🟢 메인테이너 | 위 이슈 |
| A5 | **밤새 돌렸는데 아직 빌드 중** — Rosetta 켜고 33,656초(약 9시간 21분). 껐더니 5분 | 1 | 충격적 수치 | 🟡 다수 재현 | docker/for-mac#7075, 2023-11-12, **OPEN** |
| A6 | **JVM이 세그폴트로 죽는다** — Docker Desktop 4.26.1→4.27.1 업데이트 후 `qemu: uncaught target signal 11`. **⭐ 해결책이 Docker 버전이 아니라 macOS 14.3 업그레이드였다.** 그런데 원 보고자는 "macOS 14.x is not rolled out in our company yet" | 1 | 실패 장면 / 정의 뒤집기 | 🟡 다수 재현 + 🟢 Docker 엔지니어 | docker/for-mac#7172, 2024-02-05, **OPEN** |
| A7 | **빌드가 몇 시간째 멈춰 있다** — M1 Max + GraalVM 네이티브. 로그 한 줄 `C compiler: gcc (linux, **x86_64**, 7.5.0)`이 범인. **메인테이너도 처음엔 메모리 부족으로 오진했다** | 2 | 실패 장면 | 🔴 단일 + 🟢 위키 반영으로 확정 | spring-boot#33119, 2022-11-13 CLOSED |
| A8 | **⭐ "왜 이게 어디에도 안 적혀 있죠?"** — "I am just wondering why this is not mentioned anywhere, especially because how many devs using systems from Apple where ARM is de facto the standard for 2 years." | 2 | 인용·일화 | 🔴 단일 | 위 이슈 댓글, 2022-11-14 |
| A9 | **⭐⭐ 다른 분 노트북으로 빌드했더니 그냥 됐다** (한국어, **축자 인용 확보**) — 이미지 생성·push는 성공, 배포만 계속 실패. entrypoint 권한으로 오진(이미 권한 있는 걸 알면서도 `chmod +x`) → 동료 Intel 맥에선 성공 → "차이점이라고는 **코어의 차이(M1 or Intel)**였는데, **설마 그게 문제일까하는 생각이 들기는 했다**" | 1, 2 | 실패 장면 / 인용·일화 | 🔴 단일 / **인용문 축자 ✅** | velog @___pepper, 2022-01-11 |
| A10 | **A9의 마무리** — "정말 뭐가 문제인지 싶었는데,,,,, 문제 해결해 주신 리드님께 무한 감사,,,,😭" → 혼자 못 풀고 리드가 알려줬다. **"아는 사람은 3초, 모르는 사람은 며칠"** | 1 | 인용·일화 | 🔴 단일 / 축자 ✅ | 위 |
| A11 | **⭐⭐ 로컬 Colima인 줄 알고 운영 배포를 지웠다** — env_probe §5와 정확히 짝. 같은 스레드에 "나도 당했다" 5인 | **4** | 실패 장면 / 인용·일화 | 🟡 다수 재현 | HN 41578274, 댓글 2024-09-21 |
| A12 | **"current context라는 개념 자체가 악(evil)"** — `ed_mercer`. 그리고 `cduzz`: "Have we regressed to the point where we've turned big clusters of systems back into 'oops I ran a command as superuser in the wrong directory'?" | 4 | 인용·일화 / 정의 뒤집기 | 🟡 | 위 스레드 |
| A13 | **Testcontainers가 죽은 소켓을 쳐다보고 있다** — 조직 차원 결정으로 Colima 이주. `docker` 명령은 다 잘 됐다. **그래서 이주가 끝난 줄 알았다.** 그런데 Ryuk이 컨테이너 안에서 `/var/run/docker.sock`을 찾고 있었다 | 1, 2 | 정의 뒤집기 | 🟡 다수 재현 + 🟢 메인테이너 | testcontainers-java#5034, 2022-02-08 CLOSED |
| A14 | **소켓 지우고 심링크, 2전 2패** — "So I'm **2 for 2** on needing to delete the old socket and symlink Colima's. It seems very common for tools to point to that socket file." **2022-07 등록, 4년째 OPEN** | 1 | 인용·일화 | 🔴 단일 + 🟢 메인테이너 반론 | colima#365, 2022-07-12, OPEN |
| A15 | **디스크 120GB 남았는데 `No space left on device`** — 맥 호스트 디스크와 VM 안 디스크는 **다른 디스크**다. `rdctl shell df -h /mnt/data` → `97.9G / 93.1G used / 0 available / 100%`. 결말은 또 factory-reset | 1 | 수사적 질문 / 실패 장면 | 🔴 단일 + 🟢 메인테이너 | rancher-desktop#4457, 2023-04-14 CLOSED |
| A16 | **1000 users, 초당 거의 0 요청에 월 1만 유로** — "Because Docker and 'scalability' it offered looked much better on the investor slides... we ended up with thing like **running two application in a same container, having database on containers that disappear**... I don't work there anymore..." | **4** | 충격적 수치 / 인용·일화 | 🔴 단일 `(확인 필요)` | HN 22491170, 2020-03 |
| A17 | **"You don't need K8s until you start to build a half-assed K8s."** — `zeveb` | 4 | 인용·일화 / 정의 뒤집기 | 🔴 단일 | 위 스레드 |
| A18 | **7년째 열려 있는 이슈** — docker/for-mac#3677 "Bind mounts are really slow" 2019-05-20 등록, 2026-07-25 조회 시점 **여전히 OPEN**. #77 "File access in mounted volumes extremely slow"는 2016-08-02 등록, **10년째 OPEN** | 1 | 충격적 수치 | 제목·상태·날짜만 확인 | GitHub API 조회 |

> ⛔ **A18 사용 제한:** 확인된 것은 **이슈 번호·제목·등록일·조회 시점 상태** 네 가지뿐이다. **본문·댓글을 열지 않았다.** "왜 안 닫혔는지", "구조적 한계라서 못 고쳤다" 같은 해석을 붙이면 창작이다. 분포·존속기간 근거로만 쓸 것. `research/community.md` §5에 같은 성격의 이슈 약 27건이 목록으로 있으며, **전부 동일한 제한이 걸린다.**

---

## 4. 논쟁점·상충 관점

> 이 섹션은 `tech-book` 프로필의 **비교 대조형 챕터**(선택지 A / 선택지 B / 기준 / 의사결정 가이드 / 흔한 오해)에 그대로 매핑된다. 어느 쪽도 통합하지 말고 **양쪽 근거를 나란히** 제시할 것.

### 4-1. ⭐ 논쟁 TOP 1 — 소규모 팀에 Kubernetes가 필요한가

주 출처: HN 22491170 "「Let's use Kubernetes.」 Now you have eight problems" (2020-03-05, 719 points, 469 comments)
> ⚠️ **2020년 스레드다. 6년 전 논쟁이므로 "당시 기준"임을 반드시 명시할 것.** 2026-06-02의 후속 스레드(HN 48366913)는 실질 댓글이 1개뿐이라 재료가 없다.

**관점 A — 필요 없었다**
- `sho`: "startups for whom I believe drinking the k8s/golang/microservices kool-aid has cost them **6-12 months of launch delay and hundreds of thousands of dollars**... **k8s on day one at a startup is like a mom and pop grocery store buying SAP.**" `(확인 필요 — 3자 전언)`
- `zeveb`: "**You don't need K8s until you start to build a half-assed K8s.**"
- `mirko22`: 1000 users, 초당 거의 0 요청에 GKE 3개 대륙 월 1만 유로 (→ A16)
- `onion2k`: "**Choosing to build microservices is what adds complexity and makes tools like k8s necessary, not the business.**" ← 인과의 방향을 뒤집는 논거
- `Kaze404`: K8s·마이크로서비스 오버헤드로 인한 번아웃·퇴사

**관점 B — 필요했다 / 반박**
- `WnZ39p0Dgydaz1`: "**I'm getting tired of these 'you don't need k8' posts.**... I've been using it in production for close to 2 years now - not a single service downtime, great fault-tolerance, and absolutely zero management effort."
- `honkycat`: "**if you go with Docker-Compose, or Amazon ECS, or something lower level, you are just going to end up rebuilding a shittier version of Kubernetes.**"
- `envoked`: "**a lot of these anti-k8s articles are written by software developers who haven't really been exposed to the world of SRE** and mostly think in terms of web servers." + 구체적 문제 목록(배포 시 시스템 의존성, 시크릿 저장, cronjob 관리, 내부 서비스 통신)
- `avereveard`: 스케일이 아니라 **재현성**이 목적 — "we can spin any branch at any time on any provider and be sure it's exactly as we have it in production down to networking and routing"
- `bertil`: **조직 내 가독성** — "fitting in that system gives you **legibility to your peers** that a nginx might not"
- `TallGuyShort`: **고객 압력** — "customers asking us 'what's your Kubernetes story?'"

**⭐ 진짜 논쟁은 "필요한가"가 아니라 "무엇을 기준으로 판단하는가"다 — 실무 판단 기준으로 그대로 쓸 것**

| 기준 | 주장 | 출처 |
|------|------|------|
| 규모·트래픽 | 원글 및 다수 | HN 22491170 |
| **팀에 이미 아는 사람이 있는가** (규모가 아니라 역량) | "I was also very familiar with k8s ahead of time. **I would not recommend someone in my shoes to learn k8s from scratch at the stage I rolled it out**, but if you know it already, it's a solid choice" | `theptip` |
| **직접 운영하는가 vs 매니지드를 쓰는가** | "k8s is raw technology like linux kernel. You shouldn't use it directly" / "all of these pain points go away with a managed kubernetes" | `adieu`, `supermatt` |
| **먼저 데이터베이스를 봐라** | "Most customers I've dealt with who have scaling issue need take a look at their database before Kubernetes." | `mrweasel` |
| 마이크로서비스 선택이 원인 | (위) | `onion2k` |
| 조직 내 가독성 / 고객 요구 / 채용 경쟁력 | (위) | `bertil`, `TallGuyShort`, `marcinzm` |

> ⭐ **`adieu`·`supermatt`의 구분이 이 논쟁의 열쇠다: "K8s를 쓴다"와 "K8s를 운영한다"는 완전히 다른 결정이다.** 논쟁 대부분이 이걸 안 나눠서 평행선을 달린다. 책에서 이 구분을 세워주면 독자가 남의 싸움을 자기 판단으로 번역할 수 있다.

**⭐ 그리고 이 질문이 이 책 독자가 서 있는 자리 그 자체다** — `skrebbel`:
> "It seems to me that there's something of a **gap between 'for single machine setups' (eg docker-compose) and 'for 500-engineer teams' (eg kubernetes)**."

**중간 지대(가장 실용적)**
- `mrweasel`: "I would recommend **two machines and a loadbalancer.**... **when stuff breaks, you'll prefer that it's not the Kubernetes stuff.**"
- `supermatt`: "There are less moving parts in docker compose, and its easier to run on a single VM - but it doesnt offer any of the dynamic features of kubernetes that you would want at scale. **The same containers can run on both.**"
- `mosselman` — 원글의 "compose→k8s 마이그레이션이 사소하다"는 주장에 대한 반박: "The migration path of docker-compose to **swarm** is basically `docker deploy --compose-file`. **I have looked into k8s and it wasn't as easy as this.**"

### 4-2. ⭐ 논쟁 TOP 2 — buildpack vs Dockerfile (arm64 맥에서)

**자바 독자에게 가장 직결되는 논쟁이다. 요구 2번의 핵심.**

**관점 A — buildpack (`bootBuildImage` / `spring-boot:build-image`)**
- Dockerfile을 쓰지 않아도 된다. Spring Boot 공식 경로다
- 기본 빌더(Spring Boot 플러그인 문서 표기 4.1.0 기준): `paketobuildpacks/builder-noble-java-tiny:latest` — "contains a reduced set of system libraries and does not include a shell"
- **arm64는 실제로 지원된다** — 레지스트리 직접 조회로 확정(§5-2)

**관점 B — Dockerfile + `buildx`**
- `heruan` (2024-11-21): buildx는 `docker buildx build --platform linux/amd64,linux/arm64 --push .` **한 방**인데, buildpack은 "it seems like it **works for one platform at a time.** I can build images for both platforms with different tags... then create and tag a single multi platform manifest — but then I have **three different tags** in the registry while with `buildx` a single tag is pushed."
- 🟢 `dmikusa` (Paketo 메인테이너) 확답 (2024-11-21):
  > "**Neither `pack build` nor `spring-boot:build-image` will build images for multiple architectures in one run.** That may be something that comes in the future... For now, what you can do is build the two images independently and then use a command like `docker manifest` to make an index image from the two."
- 한국어 실전 후기도 같은 결론 (velog @cmsong111, 2025-03-09) `(원문 대조 필요)`: "Dockerfile을 사용하지 않기 때문에 **멀티플랫폼 지원을 위해 Docker Manifest를 수동으로 생성해야 하는 불편함**"

> ✅ **G1 해소 (§8-1).** dmikusa의 2024-11 진술은 **2026-07-25 공식 문서 기준으로도 유효하다.** 독립 1차 증거 5건이 확인했다 — 그중 결정적인 것은 (a) `pack build --platform`의 타입이 **`string`(단수)**이라는 기계 생성 표기, (b) **CNB RFC 0128이 스스로 범위를 "빌더·패키지"로 한정**한다는 원문. **책에 "여전히 1회 1아키텍처"라고 쓸 수 있다.**
>
> ⚠️ **단, "CNB 멀티아키 지원"의 두 얼굴을 반드시 구분하라** — 빌더·빌드팩 **패키징**은 멀티아키를 지원하지만, **앱 이미지 1회 빌드**는 아니다. 구분하지 않으면 이 결론이 CNB 자기 문서와 모순되는 것처럼 읽힌다. (§8-1 표)

**⭐ 그리고 논쟁은 2파전이 아니라 3파전이다 — Jib이 판을 바꾼다 (§8-2)**

| | 1회 빌드 멀티아키 출력 |
|---|---|
| Dockerfile + buildx | ✅ `--platform linux/amd64,linux/arm64` |
| **Paketo** | ❌ **불가** |
| **Jib** | ✅ **가능** — `platforms` 복수 지정 시 매니페스트 리스트 push (**incubating**, 레지스트리 push 경로 전용) |

> "When multiple platforms are specified, **Jib creates and pushes a manifest list (also known as a fat manifest)**" — Jib 공식 FAQ
>
> → **"buildpack이냐 Dockerfile이냐"라는 이분법 자체가 불완전하다.** 멀티아키가 문제라면 Jib이 Dockerfile을 쓰지 않으면서도 그 문제를 푼다. 이 반전이 요구 2번 챕터의 좋은 구조가 된다.

**⭐ 이 논쟁이 드러내는 더 큰 원리:** buildpack의 판매 포인트는 "설정 없이 이미지가 나온다"인데, **arm64에서 그 약속이 깨진다.** 2024-06 시점 🟢 `dmikusa`의 처방은 "특정 빌더를 골라야 한다"(`builder-jammy-buildpackless-tiny`)였고, 그건 "buildpackless" 빌더라 **쓸 빌드팩 목록을 직접 지정해야** 했다. **"그냥 되던 것"이 "설정을 알아야 되는 것"으로 바뀐 지점이다.**

### 4-3. 논쟁 TOP 3 — Ryuk을 끄는 우회는 허용되는가

**관점 A(실용):** `rottenha` (2022-02-11)가 `TESTCONTAINERS_RYUK_DISABLED=true`를 추천했고, **이 설정은 지금도 여러 한국어 블로그에 복붙되어 돌아다닌다.**

**관점 B(메인테이너, 🟢 `kiview`):**
> "**This will mask the error, rather than fixing the root cause**, since it will simply disable Ryuk, thereby leaving you without reliable resource cleanup."

**정답 처방** (`benhexagon`, 2022-02-11) — **두 변수가 서로 다른 값을 가리켜야 한다:**
- `DOCKER_HOST` = **호스트에서 본** 소켓 (`unix:///${HOME}/.colima/docker.sock`)
- `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` = **컨테이너(Ryuk) 안에서 본** 소켓 (`/var/run/docker.sock`)

> ⭐ **"에러가 사라진 것"과 "고친 것"의 차이** — 이 책이 가르쳐야 할 태도이고, 커뮤니티 복붙 처방의 위험을 보여주는 실물 사례다. 자바 독자 정조준.

### 4-4. Colima는 `/var/run/docker.sock`을 차지해야 하는가

| 관점 A — 차지해야 한다 | 관점 B — 차지하면 안 된다 (🟢 `abiosoft`, Colima 저자) |
|---|---|
| 너무 많은 도구가 그 경로를 하드코딩한다. "2 for 2"(`james-s-w-clark`) / 최소한 경고라도 달라(`henrik242`, 2023-03) | "**many tools are indeed catching up and utilising docker context instead.** Another advantage of this approach is the ability to **try out Colima without breaking your current workflow.**" |

**결말:** 저자가 "it's on the roadmap. Something similar to `colima nerdctl install`, maybe `colima docker link-socket`"이라고 답했으나 **2026-07-25 조회 시점에도 이슈는 OPEN이다(2022-07 등록 이후 4년째).**

### 4-5. Alpine을 써야 하는가

주 출처: HN 35056594 (2023-03-07, 34 points). ⚠️ **3년 전 논쟁이다.**

| 관점 A — 쓰지 마라 | 관점 B — 써도 된다 |
|---|---|
| `brimstedt`: "we go for **Debian slim**. Works perfectly and is **worth the extra bytes**." ⭐ 이미지 크기 최적화의 손익분기점을 한 문장으로 | `Gordonjcp`: "they're going to stop using a particular distro that **nearly everything in Docker is based on**? Oooh-kaaaay" |
| **자바 정조준** `huksley`: "Using some PDF / Graphics related stack with Alpine can be difficult and might fail in some not obvious ways... those java/jdk-*-alpine images... **actually support only subset of a (gigantic) APIs available in Java.**" | `mattpallissard`: "shipping statically compiled binaries that call getaddrinfo with musl '**Just works**'. That is not the case with glibc which expects to be dynamically linked." |
| `kenmacd`: musl DNS의 구체적 실패 경로(K8s `ndots:5` + Cloudflare DNSSEC NSEC → musl이 `EAI_NODATA` 반환, **다른 libc는 계속 탐색함**) | `justin_oaks`(가장 실용적): "**I often reach for Alpine first. If that doesn't work for some reason I think 'Oh well' and switch to Debian or Ubuntu.**" |

> ⛔ **시점 함정 — 이 논쟁의 핵심 논거는 이미 수정 중이었다.** `_ikke_` (2023-03-07): "**dns-over-tcp has been added to musl and will be part of the next release.**"
> → **"Alpine은 DNS over TCP를 지원하지 않는다"고 2026년 책에 쓰면 틀릴 가능성이 크다.** `(1차 소스 확인 필요 — musl 릴리스 노트 + Alpine 반영 버전)`
> ⛔⛔ **판정 완료 — "JDK Alpine 이미지가 Java API의 부분집합만 지원한다"는 주장은 책에 쓰지 마라.** G3 보강 조사(§8-3)에서 **뒷받침하는 공식 서술을 찾지 못했고 반증이 우세하다:** (a) Eclipse Temurin이 `eclipse-temurin:25-jdk-alpine-3.23`을 **JDK로** 배포한다 — 부분집합 런타임이면 `jdk` 태그를 달 수 없다, (b) 공식 caveat은 Java API가 아니라 **musl libc 호환성**이다.
> ✅ **대신 이렇게 쓸 것:** "Alpine 자바 이미지의 진짜 주의점은 API가 아니라 **musl libc**다. 네이티브 라이브러리를 쓰는 의존성에서 문제가 날 수 있다." — Temurin 공식 caveat으로 근거가 있다. **베이스 이미지 선택 기준 전체는 §8-3.**

### 4-6. Rosetta는 켜는 게 나은가

| 관점 A — 끄는 게 낫다 | 관점 B — 특정 버전에서 해결됐다 |
|---|---|
| 33,656초 → 껐더니 5분(`AlexandreRoba`, M3 Max 64GB) / 4.30·4.31에서도 끄고 씀(`oming`) / "Building arm images is a breeze"(`alnaranjo`) | Docker 팀(`dgageot`)이 4.26.0을 제안했고 실제로 해결된 사용자가 있어 이슈를 닫았다 |

**⛔ 그러나 이슈는 2026-07-25 조회 시점 다시 OPEN이고**, 닫힌 뒤로도 4.30.0·4.31.0에서 같은 보고가 이어졌다. **"해결됐다"고 쓰면 안 된다.**

### 4-7. OrbStack 유료가 합당한가 / 대안 런타임 이주의 청구서

| 관점 A — 합당 | 관점 B — 주의 |
|---|---|
| `jchw`: Envoy 빌드가 Docker Desktop **3~4시간** → OrbStack **1시간 미만**. "absolutely justify the cost" `(⚠️ 벤치마크 아님, 한 사람의 체감, 환경 미상 — 일반 수치로 쓰지 말 것)` | **라이선스 서버 의존** `weikju`: 인터넷 없는 한 달 동안 "OrbStack couldn't contact the license server and soon stop functioning." ⭐ **Docker Desktop 라이선스를 피해서 왔는데 또 다른 라이선스 의존이 생겼다** |
| `marvin-hansen`: "All integration tests run so much faster. Especially parallel container starts a noticable faster." | **회사가 안 사준다** `commandersaki` — §4-9의 조직 정치와 같은 벽 |
| | **백업 소프트웨어 충돌** `KingMob`: 8TB sparse disk image가 Backblaze·tarsnap·Time Machine 등을 깬다 `(1차 소스 확인 필요 — orbstack#29 미열람)` |
| | ⭐ **로컬-운영 등가성이 깨진다** `nkmnz`: "the networking with domains **does not translate 1:1** between orbstack locally and docker compose + nginx in production." → **"로컬과 운영을 똑같이 만들려고 컨테이너를 쓰는데, 런타임을 바꾸면 그 등가성이 깨진다"** |

**Colima 진영의 반론** `nrvn` (2년 사용자): OrbStack 웹사이트의 비교표가 "**not very accurate**". "Low power/CPU usage is advertised as non-existent in colima. **This is simply not true.**... **Unlike docker desktop, especially with kubernetes on. Does not drain my battery, does not bog my CPU down**" `(확인 필요 — 측정 아님, 체감)`
Colima 단점 `princevegeta89`: "**file mounting and sharing caused reliability and permission issues** for me"

**⭐ 이주하면 실제로 깨지는 것들 체크리스트** [커뮤니티 종합 — 실무 적용 팁으로 그대로 쓸 것]

| 깨지는 것 | 출처 | 시점 |
|-----------|------|------|
| Testcontainers / Ryuk 소켓 | testcontainers-java#5034 | 2022-02 |
| `/var/run/docker.sock`을 하드코딩한 도구들(`act` 등) | colima#365 | 2022-07 |
| docker-compose 호환성 (Podman) | HN 29815122 | 2022-01 |
| 볼륨 마운트 권한·안정성 (Colima) | HN 41421846 | 2024-09 |
| 로컬↔운영 네트워킹/도메인 등가성 (OrbStack) | HN 41421846 | 2024-09 |
| 백업 소프트웨어 (OrbStack sparse image) | HN 41421846 | 2024-09 `(1차 소스 확인 필요)` |
| 오프라인에서 라이선스 서버 접속 실패 (OrbStack) | HN 41421846 | 2024-09 |
| `docker context` 전역 상태 다툼 (런타임 2개 공존) | rancher-desktop#7712 | 2024-11 (**Windows**) |

### 4-8. ⛔ 소스 신뢰성 상충 — fact-checker 필독

이 리서치에서 **도구가 만들어낸 오류를 직접 잡아낸 기록**이다. 책의 정확성에 직결된다.

1. **[미해소 · 중요] GitHub Releases의 날짜 추출이 체계적으로 어긋났다.**
   조회 도구가 `spring-boot` v4.1.0을 "2024-06-10", `kind` v0.32.0을 "2025-06-02"로 보고했다. 그런데 **kind v0.32.0이 담은 노드 이미지가 `kindest/node:v1.36.1`이고, Kubernetes 1.36은 2026-06-09 릴리스다**(kubernetes.io 1차 확인). **담긴 것이 담은 것보다 나중일 수 없다.**
   → **조치: 두 릴리스 페이지에서 버전만 채택하고 날짜는 전부 폐기했다.** 같은 경로로 얻은 Rancher Desktop·Podman Desktop·Colima 날짜도 **약한 근거**로 취급한다. 반면 `docs.docker.com/desktop/release-notes/`의 날짜(4.83.0 = 2026-07-20)는 **페이지 본문에 인쇄된 값**이라 신뢰도가 높다.

2. **[해소] Kubernetes 릴리스 주기** — 도구 요약은 "quarterly cadence(연 4회)"라고 **추정 서술**했으나, 공식 문장은 "approximately **three** times per year"다. **연 3회 채택.**

3. **[해소] Paketo jammy vs noble** — 커뮤니티 논의(#1387)와 검색 요약은 **jammy** 빌더의 arm64 지원을 말하는데, Spring Boot 4.1.0 문서의 기본 빌더는 **noble**이다. **jammy의 arm64 지원은 noble의 arm64 지원을 증명하지 않는다.** → 추론하지 않고 레지스트리를 직접 조회해 해소(§5-2). **책에서 이 추론 단계를 생략하지 말 것 — "비슷하니까 되겠지"가 왜 위험한가를 가르치는 좋은 소재다.**

4. **[주의] `-Djarmode=layertools` vs `-Djarmode=tools`** — 널리 퍼진 2차 자료(블로그·강의)는 `layertools`를 쓰지만, **2026-07-25에 렌더된 Spring Boot 공식 문서(표기 4.1.0) 두 페이지에는 `layertools`가 등장하지 않고 `tools`만 나온다.** 공식 문서 채택. **전환 시점은 미확인이므로 "언제부터"는 쓰지 말 것.**

5. **[주의] 무버전 문서 URL의 함정** — `docs.spring.io/spring-boot/...`는 그날의 current를 서빙한다. 문서가 "4.1.0"을 표기했다는 것은 **문서가 4.1.0 기준으로 렌더됐다**는 뜻이지 그날의 GA라는 증명이 아니다. → 표기는 "**2026-07-25에 렌더된 문서 기준**"으로.

### 4-9. probe(실측) vs 공개 릴리스 라인 — 일치·불일치 병기

| 항목 | 이 맥의 실측 | 공개 릴리스 라인 | 판정 |
|---|---|---|---|
| Docker Desktop | 4.83.0 | 4.83.0 (2026-07-20) | ✅ **일치** — 이 맥은 조회 시점 최신 |
| Docker Engine (데몬) | 29.6.2 | 4.83.0 번들 = v29.6.2 | ✅ **일치** |
| Docker Compose | **v5.3.1** | 4.83.0 번들 = **v5.3.1** | ✅ **일치.** ⛔ Compose가 v5 라인이라는 것은 릴리스 노트로 1차 확인됐다. **"v2일 것"이라고 고치면 오류다** |
| buildx | v0.35.0-desktop.2 | 릴리스 노트 "Docker Desktop Build v0.36.0" | ⚠️ **미해소** — 같은 컴포넌트인지 미확인. probe의 buildx가 `~/.rd/bin/docker-buildx`일 가능성도 배제 못 함. **버전 숫자를 단정하지 말 것** |
| Rancher Desktop | 1.17.1 | v1.23.1 (2026-06-29, 약한 근거) | ⚠️ **불일치** — 여러 마이너 뒤처짐. "1.17.1이 최신"이라 쓰면 오류. 병기할 것 |
| kubectl client | v1.32.1 | 지원 범위 1.34–1.36 | ⚠️ **불일치** — **지원 종료 라인.** 버전 skew 소재이지 정상 상태가 아님 |
| Docker 클라이언트 | 27.5.0-rd (Rancher 빌드) | — | 데몬 29.6.2와 **다른 제품·다른 버전** (§2-3) |

### 4-10. 조직 정치 — 기술 논쟁이 아닌 논쟁

[커뮤니티 · Docker Desktop 유료화 전후]

- 돈으로 해결한 쪽 `yuppie_scum`: "I got my management to agree that it's worth the $5 a month for everyone's productivity."
- 실패한 쪽 `pseudoramble`: "Ah man, that must be a magical place. **I spent months (on-and-off) trying to convince my company to do this and failed.**... it genuinely worries me that while **IT considers it unapproved software** that it won't stop its usage."
  → ⭐ **"승인 안 된 소프트웨어인 걸 알면서 다들 그냥 쓰고 있다"** — 한국 SI/대기업 독자에게 특히 공감될 회색지대.
- 대안 이주 실패담 `xtracto`: "**The podman compatibility is unusable, and migrating to K8s manifest files is cumbersome.** Also Rancher Desktop is not a complete replacement solution... All this kind of has made me think more about **the vendor lock-in that we were having with Docker.**"
- 맥이 유독 어려운 이유를 한 줄로: "For Linux and Windows (with WSL) I just use the docker engine cli, **but for Mac, I'm not sure.**"

**⭐ 한국 커뮤니티에서 발견한 값진 혼동** [OKKY 1085503 `(원문 대조 필요, 날짜 미확인, 댓글 로그인 벽)`]
글쓴이가 **Docker Desktop 유료화 / Docker Hub 정책 / Docker Engine을 구분하지 못하고 있다.**
→ ⭐ **이 혼동 자체가 발견이다.** 입문~중급 독자의 실제 상태가 이것이며, **책에서 이 셋의 경계를 명확히 그어줄 이유**가 된다.

---

## 5. 실무 적용 팁

### 5-1. ⭐ 트러블슈팅 휴리스틱 (커뮤니티에서 반복 검증된 것)

**H1. 첫 명령은 "무엇이 실행되고, 어디에 붙는가"를 분리해서 묻는 것**
- `docker --version`은 **클라이언트** 버전이다. 데몬은 `docker info` 또는 `docker version`의 Server 섹션
- 순서: `command -v docker`(어느 바이너리?) → `docker context ls`(어느 데몬?) → `echo $DOCKER_HOST` → `docker info`
- 근거: 실측 §4(클라이언트 27.5.0-rd ↔ 서버 29.6.2) + testcontainers#5034 + colima#365

**H2. `exec format error`가 보이면 가장 단순한 이미지로 범위를 좁혀라**
- 🟢 Docker 모더레이터 `thaJeztah`의 실제 진단 절차: `docker run -it --rm --platform=linux/amd64 busybox`
- **busybox조차 실패하면 → 내 이미지 문제가 아니라 에뮬레이션 계층 문제다**
- 다음 단계 (🟢 `ctalledo`): `binfmt_misc` 등록 확인
  ```bash
  docker run --rm --privileged --pid=host alpine \
      nsenter -t 1 -m -u -i -n sh -c 'ls /proc/sys/fs/binfmt_misc/'
  ```
  > "You should see `x86_64` in the output (and `rosetta`/`rosetta-wrapper` if you have Rosetta enabled)."
  ⛔ **이건 메인테이너의 가설이고 해당 이슈는 재현 불가로 종결됐다. "Docker Desktop의 binfmt 버그"로 단정하지 말 것.**

**H3. 아키텍처를 바꿨는데 안 고쳐지면 캐시를 의심하라**
- 🟢 `dmikusa` (2024-06): "just delete your existing app images and the build cache" / "or you can change the image name, that will trigger a fresh build too"
- `jdnurmi` (2025-09): "Anything less any the builds seemed '**contaminated**'" → `docker rmi -f` 빌더·런 이미지 전부 + `./gradlew --stop`
- ⭐ **1년 이상 간격을 둔 두 사람이 같은 진단에 도달했다** (🟡)

**H4. ⭐ Docker Desktop의 "Use containerd for pulling and storing images" 토글은 빌드 결과를 바꾼다**
- `hojooo` (2025-10-23, M1): "If that option is turned **on**, I have confirmed the similar issue is reproduced... **turning off that option won't reproduce the problem.**"
- 🟢 Spring Boot 커미터 `philwebb`도 2025-11-13 분석에서 on/off를 나눠 검증했다
- → **"내 맥에서만 안 되는데요"의 유력한 용의자.** 동료와 결과가 다르면 이 체크박스부터 비교하라
- `(1차 소스 확인 필요 — Docker Desktop 4.83.x에서 이 옵션의 기본값은 미확인. §2-1의 "4.34+ 기본 활성"은 containerd image store 자체에 대한 서술이며 이 토글 문구와 동일한지 대조 필요)`

**H5. Rosetta 토글은 켠다/끈다 둘 다 시도해야 하는 변수다** — 다만 §4-6대로 **"끄는 게 맞다"고 단정하지 말 것.** 가장 확실한 처방은 **에뮬레이션을 안 하는 것.**

**H6. Testcontainers + 대안 런타임은 두 개의 서로 다른 소켓 경로를 요구한다** (§4-3)

**H7. `kubectl` current-context 처방 스펙트럼 — 합의된 답이 없다 (강도 순)**
1. 프롬프트에 컨텍스트·네임스페이스 표시(kubectx + kube-ps1)
   - ⚠️ `Telemaco019`: "I also have it in my zsh config, but **that didn't stop me from screwing up** in the past."
   - ⚠️ `terinjokes`의 반박: 프롬프트는 한 번 그려지므로 **다른 셸에서 컨텍스트를 바꾸면 낡은 정보를 보여준다**
2. 위험 명령에 확인 프롬프트(kubesafe 류)
3. 매번 `--context` 명시
4. 기본 kubeconfig를 아예 두지 않고 `KUBECONFIG`로만
5. 셸 시작 시 current-context를 unset — 본인 왈 "now I mess up the wrong namespace instead :)"
6. 디렉터리 기반 자동 전환(direnv)
7. **운영 kubeconfig를 로컬에 아예 두지 않고 필요할 때만 받아온다**

→ **실측 §5(활성 컨텍스트가 원격 EKS)를 이 스펙트럼 위에 올려놓고 독자에게 고르게 하면 좋은 챕터가 된다.**

**H8. Alpine은 "먼저 시도해보고 안 되면 갈아탄다"** — 반대 진영의 최종 착지점도 대개 **Debian slim**

### 5-2. ⭐⭐ Spring Boot 이미지 빌드 — 요구 2번의 심장

**세 가지 경로**

| 경로 | 무엇 | 특징 | 확보 상태 |
|------|------|------|----------|
| ① 손수 쓴 Dockerfile | `docker build` / `buildx` | 멀티아키가 한 방(`--platform a,b`). 통제권 최대. **`FROM` 고민이 생기는 유일한 경로** | ✅ 1차 소스 충분 |
| ② Buildpacks | `bootBuildImage`(Gradle) / `spring-boot:build-image`(Maven) → Paketo | Dockerfile 불필요. **arm64에서 함정 다수. 1회 1아키텍처**(§8-1) | ✅ 1차 소스 충분 |
| ③ Jib | `jib`/`jib:build` (레지스트리) · `jibDockerBuild`/`jib:dockerBuild` (데몬) | 레지스트리 직행 경로가 별도로 있음. **복수 `platforms` 지정 시 매니페스트 리스트 생성**(incubating) | ✅ **G2 해소 (§8-2)** |

> ⭐ **완성된 3경로 비교표는 §8-2에 있다.** 요구 2번 챕터의 뼈대로 그대로 쓸 것.

**Jib의 정의와 차별점** [웹 · 프로젝트 공식 리포 1차]
> "**Jib builds optimized Docker and OCI images for your Java applications without a Docker daemon** - and without deep mastery of Docker best-practices."
> **Fast** — "Jib separates your application into multiple layers, splitting dependencies from classes."
> **Reproducible** — "Rebuilding your container image with the same contents always generates the same image."
> **Daemonless** — "Build your Docker image from within Maven or Gradle and push to any registry of your choice."

→ ⭐ **daemonless가 맥 독자에게 갖는 의미:** Docker Desktop 라이선스(§1-4)·VM 성능(§1-3)·런타임 충돌(§2-3) 문제를 **전부 우회한다.** 3경로 비교표에서 Jib의 차별점은 여기다.
> ✅ **G2 해소.** Jib의 명령 문법·플러그인 버전·멀티플랫폼 지원은 **§8-2에 전부 있다.** Jib 관련 서술은 §8-2에서만 가져올 것 — 특히 **릴리스 날짜는 폐기됐고(추출 오류 확정), "Docker 데몬이 전혀 필요 없다"는 단정은 금지**다(적극적 문장 미확보).

**⭐⭐ `bootBuildImage`의 결과 이미지는 왜 arm64가 되는가 — 2단계 논증**

이 책이 블로그 대신 1차 소스로 답할 수 있는 대표 항목이다. **두 단계를 그대로 보여주는 것이 오히려 좋은 교육 소재다.**

**(a) 플랫폼 기본값** [웹 · Spring Boot 공식 플러그인 레퍼런스 1차, 문서 표기 4.1.0, 2026-07-25 렌더]
`imagePlatform` 옵션 설명:
> "The platform (operating system and architecture) of any builder, run, and buildpack images that are pulled. Must be in the form of `OS[/architecture[/variant]]`, such as `linux/amd64`, `linux/arm64`, or `linux/arm/v5`."

그리고 기본값:
> "**No default value, indicating that the platform of the host machine should be used.**"

→ Apple Silicon 맥에서 아무 설정 없이 돌리면 호스트 플랫폼(= linux/arm64)이 쓰인다.
**도입 버전: Since `3.4.0`** (Maven 플러그인 파라미터 상세에 명시). **3.4 미만 독자에게는 이 옵션 자체가 없다 — 버전 분기 안내가 챕터에 필요하다.**

**(b) 빌더·run 이미지가 실제로 arm64 매니페스트를 퍼블리시하는가** [웹 · **레지스트리 직접 조회**, 최상급 1차]

```
$ docker buildx imagetools inspect paketobuildpacks/builder-noble-java-tiny:latest --raw
{"schemaVersion":2,"mediaType":"application/vnd.oci.image.index.v1+json","manifests":[
 {..., "platform":{"architecture":"amd64","os":"linux"}},
 {..., "platform":{"architecture":"arm64","os":"linux"}}]}
```

| 이미지 | 퍼블리시된 플랫폼 (2026-07-25 조회) |
|---|---|
| `paketobuildpacks/builder-noble-java-tiny:latest` (**Spring Boot 기본 빌더**) | linux/amd64, linux/arm64 |
| `paketobuildpacks/run-noble-tiny:latest` (해당 run 이미지) | linux/amd64, linux/arm64 |
| `paketobuildpacks/builder-jammy-java-tiny:latest` (이전 세대) | linux/amd64, linux/arm64 |

> ⛔ **인용 규율:** (a)가 직접 말하는 것은 **"pull되는 builder·run·buildpack 이미지의 플랫폼"**이다. "따라서 **결과 이미지**가 arm64가 된다"는 (a)+(b) 2단계 추론이다. 두 근거가 다 있으므로 결론은 견고하지만, **"공식 문서에 결과 이미지가 arm64라고 적혀 있다"고 쓰면 안 된다.**
> ⛔ **digest를 책에 못 박지 말 것.** `:latest` 태그의 2026-07-25 상태다. "당시 조회 결과 amd64/arm64 두 매니페스트가 있었다"로 쓴다.

**Paketo arm64 지원 경위** [웹 · 프로젝트 공식 Discussion 1차, 2024-04-04 게시]
- 2024-04-04 beta 공지 → 🟢 메인테이너 코멘트 "**UPDATED MAY 22: no need for beta tag anymore, it's in latest**"
- 2024-06-11 기준 arm64가 **없는** Java 빌드팩은 둘뿐: `aternity`, `google-stackdriver` — "those agents do not have arm64 versions"
- ⚠️ **이 논의는 jammy 계열에 대한 것이다** (§4-8 상충 3)

**`bootBuildImage` 크로스 플랫폼 빌드가 깨졌던 실화** [웹 · GitHub 이슈 1차]
- spring-boot#46665, 2025-08-04 등록, **CLOSED**
- 증상: arm64 MacBook에서 `imagePlatform`으로 **amd64** 이미지를 만들려 하면 `Invalid buildpack reference '<buildpack>'` / `Image platform mismatch detected. The configured platform 'linux/amd64' is not supported by the image...`
- 원인(보고자 진단): 플러그인이 `docker pull --platform <imagePlatform>`은 올바르게 쓰지만, 이어지는 **`docker save`에는 platform 플래그를 주지 않아** Docker가 호스트(arm64)를 가정 → 불일치
- 보고 환경: Spring Boot 3.5.4 / Gradle plugin 3.5.4 / Docker Desktop 4.42.1 / M4 Pro
- ⭐ **제목에 속지 말 것.** 🟢 `wilkinsona`가 명시적으로 정정했다: "it sounds like the problem **only occurs when trying to build an `amd64` image on an arm64 host.**"
  → **책에 "arm64 맥에서 bootBuildImage가 실패한다"고 쓰면 오보다.** 정확히는 "arm64 호스트에서 amd64 이미지를 만들려 할 때"다.
- ⚠️ **수정 버전(milestone)은 미확인이다.** 커뮤니티에는 PR #47292 / 3.5.8-SNAPSHOT 검증까지만 나온다. **"X.Y.Z에서 고쳐졌다"고 쓰지 말 것.**

**⭐ Paketo/bootBuildImage arm64 — 4년 타임라인** [커뮤니티, 이슈 4건 본문·댓글 전문 확보]

> ⚠️ **이 타임라인은 흩어놓지 말고 하나의 이야기로 써야 한다.** 4개 이슈가 2022→2026 시간 축 위에 정확히 놓인다.

| 시점 | 상태 | 근거 |
|------|------|------|
| **2022-11** | 빌더 자체가 amd64뿐 → QEMU 위에서 돎, "performance is very poor". 우회는 커뮤니티 개인 빌더(`dashaun/*`). Spring Boot 팀은 **고치는 대신 위키에 한계를 문서화** — "this is a limitation that Spring Boot cannot control". **이 시절의 정답은 "Dockerfile을 직접 쓴다"였다** | spring-boot#33119 |
| **2024-06** | arm64 지원은 생겼는데 **"빌더를 골라야" 한다.** 🟢 dmikusa: "It is new and **not totally complete across all buildpacks**". 게다가 "buildpackless" 빌더라 빌드팩 목록을 직접 지정해야 함. + **아키텍처를 고려하지 않는 빌드 캐시** | paketo/spring-boot#491 |
| **2024-11** | Spring Boot 3.4.0의 `imagePlatform` 도입. 단 **한 번에 한 플랫폼만.** 멀티아키 태그를 원하면 `docker manifest`를 손으로 | 위 이슈 댓글 |
| **2025-08~11** | `imagePlatform` + **containerd 이미지 스토어 토글**의 조합 버그. 같은 맥·같은 코드인데 체크박스 하나로 결과가 갈림 | spring-boot#46665 |
| **2026-02** | **여전히** M4에서 amd64 에뮬레이션이 통째로 죽는 보고(재현 불가로 종결) | docker/for-mac#7849 |

**⛔ 결론: 2022년보다 훨씬 나아졌지만 "끝났다"고 쓰면 안 된다. 2026년에도 살아 있는 보고가 있다.**

### 5-3. Spring Boot layered jar — `-Djarmode=tools`

[웹 · Spring Boot 공식 문서 1차, 표기 4.1.0, 2026-07-25 렌더]

```
Usage:
  java -Djarmode=tools -jar my-app.jar

Available commands:
  extract      Extract the contents from the jar
  list-layers  List layers from the jar that can be extracted
  help         Help about any command
```
추출: `java -Djarmode=tools -jar application.jar extract --layers --destination extracted`

**공식 멀티스테이지 Dockerfile 예제(문서 그대로):**
```dockerfile
# Perform the extraction in a separate builder container
FROM bellsoft/liberica-openjre-debian:25-cds AS builder
WORKDIR /builder
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} application.jar
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted

FROM bellsoft/liberica-openjre-debian:25-cds
WORKDIR /application
COPY --from=builder /builder/extracted/dependencies/ ./
COPY --from=builder /builder/extracted/spring-boot-loader/ ./
COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
COPY --from=builder /builder/extracted/application/ ./
ENTRYPOINT ["java", "-jar", "application.jar"]
```
- **레이어 순서:** `dependencies/` → `spring-boot-loader/` → `snapshot-dependencies/` → `application/` (**자주 안 바뀌는 것부터**)
- 문서 주석: "Every copy step creates a new docker layer / This allows docker to **only pull the changes it really needs**", "This layout is efficient to start up and AOT cache (and CDS) friendly"
- ⭐ **오해를 끊는 문장:** "After startup, you should not expect any differences in execution time between running an executable jar and running an extracted jar." → **차이는 "시작"에 있지 "실행"에 있지 않다.**
- ⚠️ **`layertools` deprecate 시점은 미확인.** "3.x부터 tools로 바뀌었다" 식 단정 금지 (§4-8 상충 4)

### 5-4. ⭐ JVM과 컨테이너 — 자바 독자에게 가장 실용적인 절

**공식 문서에서 확인한 것** [웹 · Oracle JDK 21 `java` man page 1차]
- `-XX:-UseContainerSupport`:
  > "**Linux only:** The VM now provides automatic container detection support, which allows the VM to determine the amount of memory and number of processors that are available to a Java process running in docker containers... **The default for this flag is `true`**, and container support is enabled by default."
  > "Use `-Xlog:os+container=trace` for maximum logging of container information."
- `-XX:ActiveProcessorCount=x`:
  > "Overrides the number of CPUs that the VM will use to calculate the size of thread pools... **This flag is honored even if `UseContainerSupport` is not enabled.**"

**로컬 실측** [실측 · 이 책을 쓴 맥, JDK 21.0.10, 2026-07-25]
```
$ java -XX:+PrintFlagsFinal -version | grep -Ei "RAMPercentage|ActiveProcessorCount|MaxRAM "
   int  ActiveProcessorCount   = -1            {product} {default}
double  InitialRAMPercentage   = 1.562500      {product} {default}
uint64_t MaxRAM               = 137438953472   {pd product} {default}
double  MaxRAMPercentage       = 25.000000     {product} {default}
double  MinRAMPercentage       = 50.000000     {product} {default}
```
→ **JDK 21.0.10에서 `MaxRAMPercentage` 기본값 25.0으로 관측.** 즉 "컨테이너에 2GB를 줘도 힙은 기본 500MB 근처"라는 흔한 함정의 실측 근거다.
> ⛔ **일반화 금지.** 이건 **이 JDK 빌드에서의 관측**이다. `MaxRAMPercentage`의 공식 문서 기재는 확보하지 못했다(미확인). **"모든 JVM의 기본값"으로 쓰지 말고, 독자에게 `-XX:+PrintFlagsFinal`로 직접 확인하는 법을 알려주는 편이 낫다.** (이게 오히려 더 좋은 교육이다.)

**Paketo Java 빌드팩의 Memory Calculator** [웹 · paketo.io 공식 1차] — Spring 사용자에게 직접적
- 공식: `Heap = Total Container Memory - Non-Heap - Headroom`
- 문서가 언급한 기본값: `-XX:MaxDirectMemorySize` 10MB / `-XX:ReservedCodeCacheSize` 240MB / `-XX:MaxMetaspaceSize` 자동 계산 / `-Xss` 1M × 250(스레드 수 × 스택 크기) / `-Xmx`는 나머지. 모두 런타임에 `JAVA_TOOL_OPTIONS`로 붙는다
- Spring Boot 전용 컴포넌트가 "can apply domain-specific knowledge to optimize the performance of Spring Boot applications"(예: 리액티브 웹 앱의 스레드 수를 50으로 축소)
- ⚠️ `BPL_JVM_THREAD_COUNT` / `BPL_JVM_HEAD_ROOM` 환경변수, CDS/AOT 언급은 이 페이지에서 확인 못 함(미확인)

**⭐ 맥에서 `--cpus` 제한이 잘 안 먹는다** [논문 · ⚠️ arXiv 프리프린트]
`--cpus=0.5`(목표 50%) 실측:

| 플랫폼 | 평균 | σ | 비고 |
|---|---|---|---|
| Azure Premium SSD | 60.52% | 3.79 | |
| Azure Standard HDD | 48.21% | 16.24 | |
| **macOS Docker Desktop** | **71.63%** | **36.14** | **이상치 최대 247%** |

> "The 9.5× variance increase from SSD to macOS demonstrates that **two-level scheduling (macOS → LinuxKit → CFS) produces compounding inaccuracy.**"
> — Khan, arXiv:2602.15214 §4.2.2 (2026, **프리프린트**)

→ 자바 개발자가 컨테이너 CPU 인식으로 겪는 혼란과 직결된다. **`ActiveProcessorCount`를 명시하는 이유가 여기 있다.**

**기동 시간 변동계수(CV):** SSD 3.4% / HDD 8.3% / **macOS 32.8%** → 맥에서는 **결과가 재현되지 않는다**는 것 자체가 특징이다.

### 5-5. Spring Boot Docker Compose 지원과 `@ServiceConnection`

[웹 · Spring Boot 공식 문서 1차, 표기 4.1.0]

- Maven: `org.springframework.boot:spring-boot-docker-compose` (`<optional>true</optional>`)
- Gradle: `developmentOnly("org.springframework.boot:spring-boot-docker-compose")`
- 동작: `compose.yml` 등을 찾아 **`docker compose up`** 호출 → 지원 컨테이너마다 service connection 빈 생성 → 종료 시 **`docker compose stop`**
- `spring.docker.compose.lifecycle-management`: `none` / `start-only` / `start-and-stop`
- 그 외 프로퍼티(문서 그대로): `spring.docker.compose.start.command=up`, `stop.command=down`, `start.arguments[0]=--build`, `stop.arguments[0]=--volumes`, `stop.timeout=1m`, `file=../my-compose.yml`, `profiles.active=myprofile`
- `@ServiceConnection` 지원 서비스: ActiveMQ, Artemis, Cassandra, Elasticsearch, MongoDB, Neo4j, MySQL, PostgreSQL, MariaDB, MSSQL, Oracle, ClickHouse, RabbitMQ, Redis, Hazelcast, Pulsar, LDAP, OTLP(logging/metrics/tracing), Zipkin, JDBC/R2DBC
- 커스텀 이미지용 라벨: `org.springframework.boot.service-connection: redis` / 무시: `org.springframework.boot.ignore: true`
- Testcontainers 쪽: `testAndDevelopmentOnly("org.springframework.boot:spring-boot-testcontainers")`, `@ImportTestcontainers`, `@RestartScope`, `DynamicPropertyRegistrar`. 실행은 `spring-boot:test-run`(Maven) / `bootTestRun`(Gradle). 시작 순서 `spring.testcontainers.beans.startup=sequential|parallel`

> **책 구성 제안:** 컨테이너를 "배포용"이 아니라 **"개발용"**으로 쓰는 챕터의 핵심. 자바 독자가 가장 빨리 체감할 수 있는 실용 가치다.

### 5-6. Testcontainers — 런타임별 설정 (공식 문서가 직접 준다)

[웹 · Testcontainers for Java 공식 1차]

- **Docker Desktop:** "automatically detected and used by Testcontainers without any additional configuration"
- **Colima:**
  ```
  export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
  export TESTCONTAINERS_HOST_OVERRIDE=$(colima ls -j | jq -r '.address')
  export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
  ```
- **Podman (macOS):**
  ```
  export DOCKER_HOST=unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')
  export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
  ```
- **Rancher Desktop:** M1 머신용으로 QEMU 구성과 VZ(비관리자) 구성 **두 가지가 문서화되어 있다**
  - QEMU: `export TESTCONTAINERS_HOST_OVERRIDE=$(rdctl shell ip a show rd0 | awk '/inet / {sub("/.*",""); print $2}')`
- ⚠️ **OrbStack은 이 페이지에 언급 없음(미확인)**

→ **§4-3의 논쟁(Ryuk 소켓)이 여기서 해소된다.** 공식 문서에 답이 있는데도 커뮤니티가 `TESTCONTAINERS_RYUK_DISABLED=true`를 복붙하고 있다는 대비가 좋은 서사다.

### 5-7. 성능에 대해 독자에게 정직하게 말해야 하는 것

**리눅스 네이티브 기준 (⚠️ 맥 값이 아니다)** [논문]

| 항목 | 값 | 출처 / 측정 연도 |
|------|-----|------------------|
| Docker vs 네이티브 (MySQL 고동시성) | 약 2%로 점근 | Felter et al., ISPASS '15 / **2014** |
| KVM vs 네이티브 (동일) | 측정 전 구간 40% 초과 | 동일 / 2014 |
| 컨테이너 기동 | Docker ~100ms, gVisor ~190ms, Kata ~600ms, LXC ~800ms | van Rijn & Rellermeyer, Middleware '21 / **2021** |
| Docker 데몬 경유 추가 지연 | 약 250ms (OCI 런타임 직접 호출 대비) | 동일 / 2021 |
| secure container(gVisor/Kata) I/O | 최선의 경우에도 타 플랫폼의 **절반** | 동일 / 2021 |

> ⛔ **fact-checker 하드 규칙:** 위 값들은 **전부 x86_64 리눅스** 기준이다. **맥 환경 값처럼 서술되면 ❌.** 맥 사용자에게 이 수치들은 "관측값"이 아니라 **"바닥값(floor)"**이다.
> ⛔ **gVisor·Kata 단독 논문은 확보하지 못했다.** 그 수치들은 전부 van Rijn 2021의 3자 측정이다. **"gVisor는 느리다"를 현재형 단정으로 쓰지 말고 "2021년 측정 시점에는"으로 한정할 것** — 논문 스스로 개선 방향(9P → 대체 프로토콜)을 지목한다.

**맥 환경 직접 측정 — 유일한 자료이며 프리프린트다** [논문 · ⚠️ arXiv:2602.15214]

warm-start 지연 (ms, mean ± 95% CI, n=50):

| 플랫폼 | alpine | nginx | python |
|---|---|---|---|
| Azure Prem. SSD | 568 ± 5 | 564 ± 12 | 554 ± 6 |
| Azure Std HDD | 1157 ± 27 | 1287 ± 36 | 1334 ± 35 |
| **macOS Docker Desktop** | **1528 ± 139** | **1850 ± 155** | **1859 ± 139** |

- "Docker Desktop virtualization tax is **2.69×**... For nginx, the penalty reaches **3.28×**. This originates from the LinuxKit VM, virtio block device, and hypervisor scheduling."
- macOS 컨테이너 네트워크 RTT: bridge·host **양 모드 모두 약 34 ms** — "because all traffic traverses the hypervisor's virtual network" (리눅스에서는 두 모드 차이가 0.04~0.06ms로 무시 가능)
- 페이지 캐시 공유 효율 **약 0%**: "three identical nginx containers consume 3× the memory of one"

> ⛔⛔ **fact-checker 하드 규칙 (이 리서치에서 가장 위험한 함정):**
> 1. **프리프린트·단독 저자·동료심사 미확인** 단서 없이 쓰면 ⚠️
> 2. **티어 간 절대값 비교 금지.** M1 Pro 랩톱(로컬 NVMe) vs Azure 2 vCPU VM(네트워크 스토리지)은 하드웨어가 다르다. 저자 본인이 고지했다: "the macOS results are intended to characterize developer environments **rather than provide an architectural comparison with cloud CPUs**."
> 3. **특히 OverlayFS 쓰기 처리량:** 티어 내부 비율만 유효하다 — SSD **0.006×** / HDD **0.010×** / **macOS 1.06×(p=0.21, 유의하지 않음)**. 즉 **"리눅스에서는 볼륨이 OverlayFS보다 100배 이상 빠른데, 맥에서는 그 차이가 사라진다"**(둘 다 virtio에 막혀서)는 유효한 문장이다. 반면 **"맥의 OverlayFS 쓰기가 리눅스보다 빠르다"류의 문장은 즉시 ❌**
> 4. **"17× slower" 배수를 다른 수치로 재계산하지 말 것.** 논문이 분모를 밝히지 않았다. 34ms RTT는 인용 가능하되 배수는 논문 표현을 그대로 쓰거나 생략
> 5. 2.69×·3.28×도 하드웨어 교란을 포함하므로 **"가상화만의 비용"으로 서술되면 ⚠️**

> ⭐ **이 제약 자체가 책의 논거다.** "리눅스에서 통하는 조언이 맥에서 안 통한다"(볼륨 vs OverlayFS)는 대비는 실무적으로 매우 유용하고, 근거도 견고하다.

**⭐ 학계가 당신의 환경을 측정해주지 않았다 — 검증된 부재** [논문]
arXiv 전수 검색(2026-07-25 실행):
- `abs:"Docker Desktop"` → **전체 아카이브에 단 2편**(그중 컨테이너 성능 연구는 1편)
- `abs:"Apple Silicon" AND abs:container` → **3편, 전부 컨테이너 성능 연구가 아님**

→ **이 공백 자체가 이 책의 논거다:** "여러분의 환경은 학계가 측정해 주지 않았다. 그러니 **직접 재보는 법**을 배워야 한다." 챕터 하나의 동기로 충분하다.

---

## 6. 참고문헌

### 6-1. 1차 소스 — 공식 문서·릴리스 노트 (전부 2026-07-25 열람)

**Docker**
- Docker Desktop 릴리스 노트 — https://docs.docker.com/desktop/release-notes/ (4.83.0 = 2026-07-20, 페이지 인쇄 날짜)
- Docker Desktop 설정 — https://docs.docker.com/desktop/settings-and-maintenance/settings/
- Docker VMM — https://docs.docker.com/desktop/features/vmm/
- containerd image store — https://docs.docker.com/desktop/features/containerd/
- Multi-platform builds — https://docs.docker.com/build/building/multi-platform/
- Optimize cache usage in builds — https://docs.docker.com/build/cache/optimize/
- Building best practices — https://docs.docker.com/build/building/best-practices/
- Contexts — https://docs.docker.com/engine/manage-resources/contexts/
- Docker Scout — https://docs.docker.com/scout/
- Docker Desktop license agreement — https://docs.docker.com/subscription/desktop-license/

**Spring / Java**
- Packaging OCI Images (Gradle Plugin) — https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html (문서 표기 4.1.0)
- Packaging OCI Images (Maven Plugin) — https://docs.spring.io/spring-boot/maven-plugin/build-image.html (문서 표기 4.1.0)
- Efficient Deployments — https://docs.spring.io/spring-boot/reference/packaging/efficient.html
- Dockerfiles — https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html
- Development-time Services — https://docs.spring.io/spring-boot/reference/features/dev-services.html
- Releases · spring-projects/spring-boot — https://github.com/spring-projects/spring-boot/releases (**버전만 채택, 날짜 폐기**)
- java — JDK 21 Tools Reference — https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html
- Java Reference — Paketo Buildpacks — https://paketo.io/docs/reference/java-reference/
- GoogleContainerTools/jib — https://github.com/GoogleContainerTools/jib
- Supported Docker environments — Testcontainers for Java — https://java.testcontainers.org/supported_docker_environment/

**Kubernetes / 컨테이너 표준**
- Kubernetes Releases — https://kubernetes.io/releases/
- Kubernetes Release Cycle — https://kubernetes.io/releases/release/
- What is Kubernetes? (Overview) — https://kubernetes.io/docs/concepts/overview/
- Dockershim Removal FAQ — https://kubernetes.io/blog/2022/02/17/dockershim-faq/ (발행 2022-02-17)
- kind Quick Start — https://kind.sigs.k8s.io/docs/user/quick-start/
- kind Releases — https://github.com/kubernetes-sigs/kind/releases (**버전만 채택, 날짜 폐기**)
- minikube — Pushing images — https://minikube.sigs.k8s.io/docs/handbook/pushing/
- OCI Image Format Specification (Manifest) — https://github.com/opencontainers/image-spec/blob/main/manifest.md
- namespaces(7) — https://man7.org/linux/man-pages/man7/namespaces.7.html (man-pages 6.18, 2026-02-08)
- cgroups(7) — https://man7.org/linux/man-pages/man7/cgroups.7.html (man-pages 6.18, 2026-02-08)

**런타임 릴리스 (⚠️ 날짜는 약한 근거 — §4-8)**
- Rancher Desktop — https://github.com/rancher-sandbox/rancher-desktop/releases
- Podman Desktop — https://github.com/podman-desktop/podman-desktop/releases
- Colima — https://github.com/abiosoft/colima/releases

**보강 조사분 (G1~G7) 1차 소스** — buildpacks.io(`pack build` CLI, Build for ARM), CNB RFC 0128, Jib README×2 + FAQ, GoogleContainerTools/distroless, alpinelinux.org/about, docker-library/docs(debian·eclipse-temurin), docs.docker.com(scout CLI·scout/install·desktop/features/kubernetes·reference/cli/docker/buildx/build·.../imagetools/inspect·engine/storage/containerd)
→ **전체 URL·인용문은 §L-7 및 `research/web_gapfill.md`**

**레지스트리 직접 조회 (최상급 1차, 2026-07-25 시점 상태)**
- `docker buildx imagetools inspect paketobuildpacks/builder-noble-java-tiny:latest --raw`
- `docker buildx imagetools inspect paketobuildpacks/run-noble-tiny:latest --raw`
- `docker buildx imagetools inspect paketobuildpacks/builder-jammy-java-tiny:latest --raw`

### 6-2. 논문 (전부 PDF·학회 공식 페이지·DBLP/arXiv API로 서지 확정)

1. Felter, W., Ferreira, A., Rajamony, R., Rubio, J. (IBM Research). "An Updated Performance Comparison of Virtual Machines and Linux Containers." **ISPASS 2015, pp. 171–172.** DOI: 10.1109/ISPASS.2015.7095802 — 측정 2014 (Ubuntu 13.10, 커널 3.11.0, Docker 1.0, KVM/QEMU 1.5.0, MySQL 5.5.37, Xeon E5-2665×2)
2. van Rijn, V., Rellermeyer, J. S. (TU Delft). "A Fresh Look at the Architecture and Performance of Contemporary Isolation Platforms." **Middleware '21.** arXiv:2110.11462 — 측정 2021 (AMD EPYC2 7542 dual-socket, Ubuntu Server 20.04 LTS)
3. ⚠️ **프리프린트** — Khan, S. "Decomposing Docker Container Startup Performance: A Three-Tier Measurement Study on Heterogeneous Infrastructure." **arXiv:2602.15214 (2026-02-16, 단독 저자, 동료심사 미확인)** — macOS: Apple M1 Pro, 16GB, APFS/VM, Docker 28.4.0, Hypervisor.framework / Azure: Standard_D2s_v3 2 vCPU, Docker 28.x, overlay2
4. Agache, A., Brooker, M., **Florescu, A.**, Iordache, A., Liguori, A., Neugebauer, R., Piwonka, P., Popa, D.-M. (AWS). "Firecracker: Lightweight Virtualization for Serverless Applications." **NSDI '20, pp. 419–434.** — 측정 2019~2020 (EC2 m5d.metal)
   > 📌 **USENIX 공식 페이지의 `citation_author` 메타태그에는 저자가 7명만 있고 Andreea Florescu가 빠져 있다. PDF 표지 기준 8명이다. 자동 인용 생성기를 쓰면 저자가 누락된다.**
5. Lin, X., Lei, L., Wang, Y., Jing, J., Sun, K., Zhou, Q. "A Measurement Study on Linux Container Security: Attacks and Countermeasures." **ACSAC '18, pp. 418–429.** DOI: 10.1145/3274694.3274720 — 측정 2018 (Docker 17.09.1-ce)
6. He, Y., Guo, R., Che, X., Xing, Y., Sun, K., Liu, Z., Xu, K., Li, Q. "Cross Container Attacks: The Bewildered eBPF on Clouds." **USENIX Security '23, pp. 5971–5988.** ⚠️ **Abstract만 확보** — 본문 실험 조건 미확인, 수치성 주장 인용 금지
7. Verma, A., Pedrosa, L., Korupolu, M., Oppenheimer, D., Tune, E., Wilkes, J. (Google). "Large-scale cluster management at Google with Borg." **EuroSys '15, Article 18, pp. 18:1–18:17.** DOI: 10.1145/2741948.2741964 — 관측 ~2014~2015. ⚠️ **Borg는 Kubernetes가 아니다**
8. Harter, T., Salmon, B., Liu, R., Arpaci-Dusseau, A. C., Arpaci-Dusseau, R. H. "Slacker: Fast Distribution with Lazy Docker Containers." **FAST '16.** — 측정 2015~2016
9. Liu, P., Ji, S., Fu, L., Zhang, X., Lu, T., Chen, W., Lu, K., Lee, W.-H., Beyah, R. "Understanding the Security Risks of Docker Hub." **ESORICS 2020, LNCS 12308, pp. 257–276.** DOI: 10.1007/978-3-030-58951-6_13 — 수집 2019년경(정확 일자 미확인)

### 6-3. 커뮤니티 (본문·댓글 전문 확보 — 인용 가능)

| 출처 | URL | 시점 / 상태 |
|---|---|---|
| docker/for-mac#7849 (M4 amd64 에뮬레이션 사망) | https://github.com/docker/for-mac/issues/7849 | 2026-02-05 / CLOSED(재현불가) |
| docker/for-mac#7172 (QEMU 위 JVM signal 11) | https://github.com/docker/for-mac/issues/7172 | 2024-02-05 / **OPEN** |
| docker/for-mac#7075 (Rosetta 33,656초) | https://github.com/docker/for-mac/issues/7075 | 2023-11-12 / **OPEN** |
| spring-boot#33119 (M1 Max GraalVM 정체) | https://github.com/spring-projects/spring-boot/issues/33119 | 2022-11-13 / CLOSED |
| spring-boot#46665 (imagePlatform amd64 크로스빌드) | https://github.com/spring-projects/spring-boot/issues/46665 | 2025-08-04 / CLOSED |
| paketo-buildpacks/spring-boot#491 (멀티아치·캐시 오염) | https://github.com/paketo-buildpacks/spring-boot/issues/491 | 2024-06-21 / CLOSED |
| paketo-buildpacks/java Discussion #1387 (arm64 beta) | https://github.com/paketo-buildpacks/java/discussions/1387 | 2024-04-04~2024-07-27 |
| testcontainers-java#5034 (Colima Ryuk 소켓) | https://github.com/testcontainers/testcontainers-java/issues/5034 | 2022-02-08 / CLOSED |
| colima#365 (소켓 심링크 논쟁) | https://github.com/abiosoft/colima/issues/365 | 2022-07-12 / **OPEN (4년째)** |
| rancher-desktop#7712 (런타임 2개 context 다툼, **Windows**) | https://github.com/rancher-sandbox/rancher-desktop/issues/7712 | 2024-11-01 / OPEN |
| rancher-desktop#4457 (VM 디스크 만땅) | https://github.com/rancher-sandbox/rancher-desktop/issues/4457 | 2023-04-14 / CLOSED |
| HN 22491170 (K8s 논쟁 본체) | https://news.ycombinator.com/item?id=22491170 | 2020-03-05, 719pt, 469 comments |
| HN 41578274 (kubectl 컨텍스트 사고) | https://news.ycombinator.com/item?id=41578274 | 2024-09-18 / 댓글 2024-09-21 |
| HN 41421846 (OrbStack 후기) | https://news.ycombinator.com/item?id=41421846 | 2024-09-02, 307pt |
| HN 35056594 (Alpine 논쟁) | https://news.ycombinator.com/item?id=35056594 | 2023-03-07, 34pt |
| HN 29815122 (Docker Desktop 대안 탐색) | https://news.ycombinator.com/item?id=29815122 | 2022-01-05 |
| HN 28371788 (Podman 회의론) | https://news.ycombinator.com/item?id=28371788 | 2021-08-31 |

**한국어**

| 출처 | URL | 시점 | 인용 가능 여부 |
|---|---|---|---|
| velog @___pepper (M1 이미지 배포 오류) | https://velog.io/@___pepper/Docker-M1-mac-이미지-배포-오류 | 2022-01-11 | ✅ **축자 인용 확보 — 유일** |
| velog @msung99 (플랫폼 호환성 에러) | (research/community.md §신선도 원장 37행) | 2023-01-05 | ⚠️ 요약 경유 `(원문 대조 필요)` |
| velog @cmsong111 (buildpack 멀티아치) | (동 39행) | 2025-03-09 | ⚠️ 요약 경유 |
| OKKY 1085503 (도커 유료화 문의) | https://okky.kr/articles/1085503 | **날짜 미확인** | ⚠️ 요약 경유 / 댓글 로그인 벽 |
| GeekNews 16867 (Docker Desktop 대안) | https://news.hada.io/topic?id=16867 | 2024-09-21 | ⚠️ 요약 경유 |
| 우아한형제들 기술블로그 (K8s 테스트 환경) | https://techblog.woowahan.com/2562/ | **2018-03-13** | ⚠️ **8년 전 글. 명령·버전 인용 금지.** 서사·동기 용도만 |

> ⭐ **한국어 축자 회수 방법(실증됨):** WebFetch에 "**번역하거나 요약하지 마라. 한국어 본문을 한 글자도 바꾸지 말고 그대로 출력하라**"고 명시하면 원문을 받을 수 있다. `research/community.md` 일화 7이 이 방법으로 확보됐다(저자 오탈자까지 보존). **⚠️ 요약 경유 4건은 따옴표로 옮기기 전 이 방법으로 재수집해야 한다.**

---

## 7. 리서치 한계

### 7-1. 커버리지 자기평가 A~G (엄격 루브릭)

> **판정 기준:** **충분** = 해당 영역의 모든 버전 민감 항목에 1차 소스 + 시점이 있고 챕터 한 절을 쓸 재료가 있다 / **보통** = 재료는 있으나 일부 항목이 1차 소스 미확보 / **부족** = 체크리스트 항목 중 아예 소스가 없는 게 있다.

| 영역 | 등급 | 빠진 것 |
|------|------|--------|
| **A. 맥에서의 Docker 실행 구조** | **충분** | VMM 3종·Rosetta 전제조건·VirtioFS·리소스 기본값(메모리 50%, swap 1GB)·라이선스 임계값(250인 AND $10M)·릴리스 라인 모두 1차 확보. **기본 VMM이 무엇인지만 미확인**(경미). "왜 VM이 끼는가"의 커널 논거는 G-1로 충족 |
| **B. 아키텍처 (arm64/amd64)** | **충분** ⬆️ | 멀티플랫폼 3전략·`--load`/`--push`/`--platform` CLI 레퍼런스·**`--load` 제약의 진짜 조건(§8-6, 문서 충돌 해소)**·containerd image store·**Paketo 빌더의 실제 arm64 매니페스트(레지스트리 실물)**·**`imagetools inspect` 정석 확인 명령**·에뮬레이션 성능 공식 서술·5가지 증상 얼굴·양방향 경고 사례 확보. 잔여 결손(경미): `exec format error` 문자열의 공식 서술 미발견(원인 서술은 확보), Rosetta 정량 수치 없음, buildx 드라이버 4종 전체 비교 미열람 |
| **C. 대안 런타임** | **보통** | 4개 도구 공개 최신 버전 + `docker context` 우선순위 공식 문장 + 이주 시 깨지는 것 체크리스트 8항목 + 실사용 후기 다수 확보. **결손: OrbStack 버전 전무, Rancher의 containerd/moby 선택·`nerdctl` 공식 문서 없음, 각 런타임의 VM/하이퍼바이저 아키텍처 비교 1차 소스 없음** |
| **D. 이미지 만들기·업데이트** | **보통** ⬆️(부족→보통) | 캐시 규칙·`.dockerignore`·캐시 마운트·외부 캐시·digest 고정·`--pull`/`--no-cache`·멀티스테이지·태그 해석 방식 1차 확보. 논문 3편(76%/6.4%, 2.5%, 422일)으로 "왜"까지 뒷받침. **G3·G4로 두 빈칸이 닫혔다** — 베이스 이미지 선택 기준(distroless/Alpine/Debian slim/Temurin/Liberica 전부 1차) + `docker scout` 하위 명령 19개·번들 여부·`recommendations`·`sbom`. ⛔ **충분이 아닌 이유(루브릭 적용): `semver 태깅·태그 승격 워크플로`와 `dive`·`docker history`는 소스가 0건이다** — 둘 다 체크리스트 D의 명시 항목. `--mount=type=secret` 예시도 없음 |
| **E. Spring 컨테이너화** | **충분** ⬆️ | **핵심 축 전부 1차 확보** — 기본 빌더(noble)·`imagePlatform` 기본값 및 도입 버전(3.4.0)·레지스트리 실물 arm64 확인·layered Dockerfile 전문·compose 지원·`@ServiceConnection` 목록·Testcontainers 런타임별 설정·`UseContainerSupport`. **G1·G2로 가장 중요한 두 빈칸이 닫혔다** — 멀티아키 단일 태그 현황(증거 5건) + Jib 전모(명령·버전·`platforms`·매니페스트 리스트·제약) → **3경로 비교표 완성**. 부수로 CDS/AOT 캐시 플래그 확보. 잔여 결손: `MaxRAMPercentage` 공식 문서 근거 없음(로컬 관측만), `layertools` 전환 시점 미확인, #46665 수정 릴리스 미확인 |
| **F. Kubernetes** | **보통** ⬆️ | 지원 버전표·EOL·**연 3회** 주기·1년 패치 지원·dockershim 제거(1.24)·"What Kubernetes is not" 전문·kind/minikube 이미지 로딩 명령·pull policy 함정·도입 논쟁 양쪽 확보. **G5가 큰 결손을 닫았다** — Docker Desktop 내장 K8s가 **kubeadm/kind 선택제**임을 확인하고 **공식 비교표**(특히 **kind ↔ Docker image store 비호환**) 확보. **번들 버전은 "문서에 명시 없음"으로 확정**(미확인이 아니라 부재 확정). ⛔ **충분이 아닌 이유(루브릭 적용): `Ingress 예제`·`k3s(Colima) 경로`·`로컬 K8s 리소스 소모 비교` 세 항목은 소스가 0건이다** — 전부 체크리스트 F의 명시 항목 |
| **G. 원리** | **보통** | namespaces(7)·cgroups(7)·OCI manifest는 최상급 1차(man-pages 6.18, 2026-02-08). 네임스페이스 생성 8ms·격리 vs 보안 학술 근거·Firecracker·Docker Hub 실태 조사 확보. **결손: overlayfs 전용 문서 미열람, 컨테이너 vs VM 보안 경계 1차 논거 없음, rootless·cosign 서명·SBOM 생성 공식 문서 전무** |

### 7-2. ⭐ 사용자 4대 요구별 — 챕터를 쓸 재료가 있는가

| 요구 | 판정 | 근거 |
|------|------|------|
| **1. 맥 환경에서 Docker 개발 시 알아야 할 것들** | ✅ **충분 — 챕터 2~3개 분량** | A(충분) + B + C + 실측 §4 고유 자산 + 일화 A1·A2·A5·A6·A13·A14·A15·A18. VMM/Rosetta/파일공유 3자 트레이드오프, 클라이언트≠데몬, VM 디스크 경계까지 전부 실물 근거 있음 |
| **2. Spring Boot 이미지 빌드·배포** | ✅✅ **충분 — 이 책의 중심축, 챕터 2~3개. 가장 강한 영역** | E(충분) + 4년 타임라인 + 일화 A3·A4·A7·A8·A9. **G1·G2로 3경로 비교표가 완성됐다**(§8-2) — Paketo는 1회 1아키텍처, Jib은 매니페스트 리스트 가능(incubating)이라는 **반전**까지 1차 소스로 확보. 부수로 CDS/AOT 캐시 절 재료 |
| **3. 이미지 만들고 업데이트하기** | ⚠️ **본문 재료는 충분, 그러나 오프닝 일화가 없다** | D(보통). 뼈대(캐시·digest·`--pull`/`--no-cache`·멀티스테이지)는 견고하고 논문 근거도 강하다. **G3·G4가 두 빈칸을 닫았다** — 베이스 이미지 선택 요약표(공식 근거 5종) + `docker scout recommendations`로 **"업데이트" 루프가 도구 수준까지 연결됐다.** ⛔ **두 가지 결손을 Phase 2가 반드시 알아야 한다: (a) `semver 태깅·태그 승격`·`dive`/`docker history` 소스 0건 — 소절로 계획하지 말 것. (b) 오프닝 일화 0건 — 아래 대안 참조** |
| **4. K8s 언제 쓰나 + 맥에서 써보기** | ✅ **챕터 2개 분량 — 단 소절 3개는 재료가 없다** | F(보통). "왜 쓰나"는 공식 "What Kubernetes is not" + HN 논쟁 양쪽으로 **매우 강함**. "맥에서 써보기"는 kind·minikube 명령·pull policy 함정·**Docker Desktop kubeadm/kind 선택제 공식 비교표**·실측 EKS 컨텍스트 사고 + 사고담으로 충분. ⭐ **kind ↔ Docker image store 비호환**이 실습 함정으로 강력. ⛔ **`Ingress 예제`·`k3s(Colima) 경로`·`로컬 K8s 리소스 소모 비교`는 소스 0건 — 계획에서 빼거나 저술 시점에 직접 확보할 것** |

**⛔ Phase 2가 계획에 넣으면 안 되는 소절 (소스 0건 — 통합 목록)**

| 소절 후보 | 영역 | 상태 |
|---|---|---|
| semver 태깅 전략 / 태그 승격 워크플로 | D | 공식 가이드 0건 |
| `dive` / `docker history`로 레이어 뜯어보기 | D | 소스 0건 |
| `--mount=type=secret` 실습 | D | 예시 0건 |
| Ingress로 외부 노출하기 | F | 예제 0건 |
| k3s(Colima)로 로컬 K8s 돌리기 | F | 경로 0건 |
| 로컬 K8s 리소스 소모 비교(kind vs minikube vs Desktop) | F | 수치 0건 |
| rootless / cosign 이미지 서명 / SBOM **생성** 실습 | G | 공식 문서 0건 (`docker scout sbom` 명령 존재는 확인 — §8-4) |
| `latest` 태그 사고담 · 베이스 갱신 운영 실태 · 스캔 알림 피로 | 요구 3 | 커뮤니티 자료 0건 |

**⭐ 요구 3번 챕터의 오프닝 대안 — 일화 대신 "충격적 수치"로 열어라**

`research/community.md`가 요구 3번의 세 일화 주제(`latest` 사고담·베이스 갱신 실태·스캔 피로)에서 **모두 0건**을 반환했다. §3 일화 표에서도 요구 3번에 매핑되는 것은 A4 하나뿐이고 그마저 요구 2번과 공유한다. **일화를 찾아 헤매지 말고, 이미 확보된 수치로 열면 된다** — `tech-book` 프로필 오프닝 메뉴의 "충격적 수치·사실" 기법이다.

| 오프닝 수치 후보 | 값 | 출처 (§ 병기 필수) |
|---|---|---|
| 이미지 취약점 패치 지연 | **평균 422일** | Liu et al., ESORICS 2020 (2019년경 수집) |
| 커뮤니티 이미지 고위험 취약점 비율 | **64% 초과** | 동일 |
| pull이 기동 시간에서 차지하는 비중 vs 실제 읽히는 데이터 | **76% vs 6.4%** | Harter et al., FAST '16 (2016 측정) |
| 태그는 고정이 아니다 | `FROM alpine:3.21` → "resolves to the **latest patch version**" | Docker 공식 best-practices |

→ **부수 효과:** 현재 §3 오프닝 기법 분포가 '실패 장면'에 쏠려 있다. 요구 3번을 '충격적 수치'로 열면 프로필의 "인접 챕터는 같은 기법을 반복하지 않는다" 규칙을 만족시키기도 쉬워진다.

### 7-3. 리서치 공백 — 확보하지 못한 것 (정직한 목록)

**🔴 자료가 0건인 영역 (책에서 다루려면 저술 시점에 직접 확보하거나 범위에서 뺄 것)**
1. **`latest` 태그 때문에 터진 구체적 사고담** — HN 전수 검색에도 일화라 부를 스레드가 없었다. 대신 **kind 문서의 pull policy 규칙**(`:latest`면 기본이 `Always`)을 근거로 삼는 편이 정확하다
2. **베이스 이미지 업데이트를 실제로 어떻게 굴리는가** (자동화 vs 수동, 주기) — 커뮤니티 자료 없음
3. **취약점 스캔 도입 후의 알림 피로** — 자료 없음
4. **로컬 K8s(kind/minikube/k3s/Docker Desktop 내장)의 맥북 배터리·메모리 소모 비교** — 수치 자료 없음. 체감 증언 1건뿐
5. **맥 메모리 할당 튜닝 실패담** — 이슈 제목 + 체감 2건뿐
6. **"맥에서 Testcontainers가 느려 Spring Boot 테스트가 느려진다"는 성능 증언** — 소켓 문제는 충분하나 성능 증언은 0건
7. **Gradle/Maven 빌드나 node_modules 워크로드의 볼륨 마운트 성능 수치** — 없음

**🟡 부분 확보 / 시점이 낡은 영역**
8. **K8s 도입 논쟁이 2020년 스레드 중심이다** (6년 전). 2024~2026 최신 스레드는 빈약했다 → 본문에 반드시 "2020년 당시" 명시
9. **Alpine 논쟁이 2023년 자료다** (3년 전). 게다가 **핵심 논거(musl DNS-over-TCP 부재)가 그 시점에 이미 수정 중이었다** → 1차 소스 재확인 없이 쓰면 오보 위험
10. **Docker Desktop 라이선스 원 공지(2021-08-31)의 대형 HN 댓글 스레드 미열람**, OKKY 댓글은 로그인 벽
11. **Podman 후기가 2021~22년 것뿐**
12. **한국어 소스 5건 중 축자 인용 가능한 건 1건**(velog @___pepper). 나머지 4건은 WebFetch 요약 경유 → §6-3의 회수 방법으로 재수집 필요
13. **국내 회사 엔지니어링 블로그의 최신 컨테이너/멀티아키 사례 없음** — 1차 검색 2회 + G7 도메인 한정 검색 3회, 총 5회 시도에서 **멀티아키·Apple Silicon 직결 한국어 글 0건.** ⛔ **다만 이걸 "국내에 없다"로 격상하지 말 것**(§8-7) — 검색 5회는 부재의 증명이 아니다. **서문 포지셔닝 문구로 인용 금지**
14. **gVisor·Kata 단독 논문 미확보** — 3자 측정(van Rijn 2021)에만 의존
15. **Apple Silicon 컨테이너 성능의 동료심사 논문이 사실상 없다** — 이건 리서치 실패가 아니라 **검증된 부재**이며, 그 자체가 책의 논거다(§5-7)

**🟠 실측과 어긋나 반드시 병기해야 하는 것**
16. Rancher Desktop 1.17.1(실측) vs v1.23.1(공개 최신, 약한 근거)
17. kubectl v1.32.1(실측) vs 지원 범위 1.34~1.36 → **지원 종료 라인**
18. buildx v0.35.0-desktop.2(실측) vs "Docker Desktop Build v0.36.0"(릴리스 노트) → **같은 컴포넌트인지 미확인. 버전 숫자 단정 금지**

**✅ 보강 조사 완료 (G1~G7) — 6/7 해소. 상세는 §8**

| 갭 | 상태 | 결과 |
|---|---|---|
| G1 Paketo 멀티아키 | ✅ **해소** | **여전히 1회 1아키텍처** (1차 증거 5건) |
| G2 Jib | ✅ **해소** | 명령·버전·`platforms`·**매니페스트 리스트 생성 확인**. 날짜는 전부 폐기 |
| G3 베이스 이미지 | ✅ **해소** | distroless·Alpine·Debian slim·Temurin·Liberica 전부 1차. **"Alpine JDK 부분집합설" 반증 우세 판정** |
| G4 `docker scout` | ✅ **해소** | 하위 명령 19개 + Docker Desktop 사전 설치 확인 |
| G5 Desktop 내장 K8s | ✅ **해소** | **kubeadm/kind 선택제** 발견 + 공식 비교표. 번들 버전은 **"문서에 명시 없음"으로 확정** |
| G6 `exec format error` | ⚠️ **부분** | 오류 문자열 자체는 미발견. **원인 서술·에뮬레이션 성능·`imagetools inspect`는 확보. `--load` 문서 충돌을 해소한 것이 최대 수확** |
| G7 한국어 최신 사례 | ✅ **해소(부정)** | 검색 3회, 직결 자료 0건 — **부재 단정 금지** |

**⛔ 보강 조사가 뒤집은 것 — 이걸 모르면 틀린 책이 된다**
1. **"멀티플랫폼은 `--load` 못 한다"는 절대 규칙이 아니다** (§8-6). classic 드라이버 vs containerd 스토어 조건이며, **맥의 Docker Desktop 독자는 대체로 담을 수 있다**
2. **Jib은 한 번의 빌드로 매니페스트 리스트를 만든다** (§8-2). "buildpack이냐 Dockerfile이냐" 이분법이 불완전하다
3. **"Alpine JDK는 Java API 부분집합" 주장은 반증 우세** (§8-3). 커뮤니티 인용을 그대로 옮기면 오보
4. **Docker Desktop 내장 K8s는 kubeadm/kind 선택제** (§8-5). "체크박스 하나" 모델로 쓰면 틀림

### 7-4. 실패한 리서처 / 도구 실패 기록

- **리서처 실패는 없다.** web·paper·community 3명 + 보강 web-researcher 1명, 총 4명 전원 산출물 생성 완료
- 도구 실패: `bugs.openjdk.org` **HTTP 403**(→ 로컬 `PrintFlagsFinal` 관측으로 대체, 1차 문서 근거 없음) / Semantic Scholar API **429 2회**(→ DBLP 대체) / ACM DL 봇 차단(→ 기관 오픈 PDF + DBLP 우회) / USENIX WebFetch **403**(→ curl 우회 성공) / OKKY 댓글 로그인 벽
- **의도적으로 제외한 소스:** 개인 블로그·Medium·Stack Overflow는 **버전·플래그·기본값의 근거로 채택하지 않았다.** 검색 결과에 노출됐던 글들은 열지 않았고 인용하지 않는다
- **WebSearch 요약문 자체를 소스로 쓰지 않았다.** 첫 검색 요약이 "Spring Boot 3.4.0의 멀티아키 지원" 등을 단언했으나 인용문이 아닌 생성 문장이므로 전부 1차 소스로 재확인했다
- **미접근 플랫폼:** 커리어리, 개발자 Discord/Slack 공개 로그, Lobsters, Dev.to, Stack Overflow, X/Mastodon, 네이버 카페

---

## 8. 보강 조사 결과 (G1~G7)

> 원본: `research/web_gapfill.md` (2026-07-25). 6/7 해소. **이 섹션은 §4-2·§5-2·§7의 판정을 바꾼다.**

### 8-1. ⭐⭐ G1 해소 — Paketo/`bootBuildImage`는 **여전히 1회 1아키텍처**다

**결론: dmikusa의 2024-11-21 진술은 2026-07-25 공식 문서 기준으로도 유효하다.** 서로 독립적인 1차 증거 5건이 같은 결론을 가리킨다.

| # | 증거 | 원문 |
|---|------|------|
| 1 | Spring Boot **Gradle** 플러그인 레퍼런스 | `imagePlatform` 형식이 `OS[/architecture[/variant]]` **단일 값**. 콤마 목록 허용 서술 없음 |
| 2 | Spring Boot **Maven** 플러그인 레퍼런스 | 글자 단위로 같은 문구 → 두 플러그인이 같은 단일 플랫폼 모델 공유 |
| 3 | ⭐ **`pack build` CLI 레퍼런스** | `--platform **string**` (단수). 같은 표의 `-t, --tag **strings**` / `-b, --buildpack **strings**` / `--pre-buildpack **stringArray**`와 대비 |
| 4 | CNB "Build for ARM architecture" | "**We do not currently support building an app image for one architecture on a different architecture.** However, if your host machine supports emulation (for example, with QEMU) you may be able to perform cross platform builds, **albeit with a performance penalty**." |
| 5 | ⭐ **CNB RFC 0128 (Approved)** | RFC가 스스로 범위를 한정: "**The purpose of this RFC is to solve the statement 2**, adding the capability to the commands: `pack buildpack package`, `pack builder create`..." |

> **증거 3이 왜 단단한가:** `string` vs `strings`/`stringArray` 구분은 CLI 플래그 정의에서 **기계 생성**된 표기다. 산문 설명과 달리 저자의 표현 실수일 여지가 거의 없다.

**⚠️⚠️ 반드시 구분해서 쓸 것 — "CNB 멀티아키 지원"의 두 얼굴**

CNB 생태계에 "멀티아키 지원"이라는 말이 돌아다니는데 **서로 다른 두 가지다.** 구분하지 않으면 위 결론이 CNB 자기 문서와 모순되는 것처럼 읽힌다.

| 대상 | 멀티아키 | 근거 |
|------|---------|------|
| **빌더·빌드팩 패키징** (`pack builder create`, `pack buildpack package`) | ✅ **지원** — 이미지 인덱스 생성 | CNB RFC 0128 (statement 2) |
| **앱 이미지 1회 빌드** (`pack build`, `bootBuildImage`, `spring-boot:build-image`) | ❌ **미지원** — 1회 1아키텍처 | 증거 1~4 |

RFC는 문제를 셋으로 쪼갠 뒤 자신이 푸는 것은 2번이라고 명시했다. **3번(애플리케이션 개발자가 멀티아키 앱 이미지를 만드는 것)은 이 RFC의 대상이 아니다.** 즉 CNB 자신이 두 문제를 별개로 번호 매겨 분리했다.

**실무 결론 (책에 쓸 형태):** 맥(arm64)에서 `bootBuildImage`를 그냥 돌리면 arm64 이미지가 나온다. amd64 서버에 배포하려면 둘 중 하나다.
1. `imagePlatform=linux/amd64` 지정 — **호스트 에뮬레이션 필요, 성능 페널티**(CNB 문서가 QEMU 경로를 명시적으로 인정)
2. 두 아키텍처를 **각각 독립적으로 빌드**한 뒤 `docker manifest`로 인덱스 이미지 합성

**앵커:** pack CLI 최신 **v0.40.8 (2026-07-13)**. 최근 릴리스 중 아키텍처 관련 유일 언급은 v0.40.2의 "fix: treat amd64 as equivalent to x86-64 for lifecycle binary selection" — **앱 이미지 멀티아키 출력과 무관하다.**

> ⛔ `buildpacks/pack#1570` "Multi arch image build support"(2022-12-06 생성, **Closed**)는 **종료 사유를 읽어내지 못했다.** "멀티아키가 구현되어 닫혔다"는 근거로 쓰지 말 것.

### 8-2. ⭐⭐ G2 해소 — **Jib은 한 번의 빌드로 매니페스트 리스트를 만든다** (3경로 비교표의 반전)

**이것이 Paketo와의 결정적 차이이며, 이 책 3경로 비교의 핵심 대비축이다.**

**목표·태스크 이름** [Jib 공식 README]

| | Maven | Gradle |
|---|---|---|
| 레지스트리 push | `jib:build` | `gradle jib` — "Builds and pushes a container image to a registry" |
| Docker 데몬으로 빌드 | `jib:dockerBuild` | `gradle jibDockerBuild` — "Builds directly to a local Docker daemon" |
| 타르볼 | `jib:buildTar` | `gradle jibBuildTar` |

**버전 (⚠️ 날짜는 전부 폐기)**

| 플러그인 | 버전 |
|---|---|
| `jib-maven-plugin` | **3.5.2** |
| `jib-gradle-plugin` | **3.5.4** |
| `jib-core` | 0.28.2 |

> ⛔ **Jib 릴리스 날짜를 책에 쓰지 마라.** GitHub Releases 추출이 최신 3건을 "2024-07-14"로 보고했는데, 같은 릴리스의 변경 내용에 **"Java 25 지원"**이 있다. 명백히 틀렸다. **버전만 채택.**
> ⚠️ Maven(3.5.2)과 Gradle(3.5.4)이 **독립 버저닝**된다. "Jib 3.5.x"로 뭉뚱그리지 말고 플러그인별로 표기할 것.

**기본 베이스 이미지:** `eclipse-temurin:{8,11,17,21,25}-jre` (JAR 프로젝트) / WAR은 `jetty`
> ⚠️ `{8,11,17,21,25}`는 **문서 표기법**이다 — 프로젝트 자바 버전에 따라 결정된다는 뜻이지 리터럴 태그가 아니다. Dockerfile에 그대로 복사하면 안 된다.

**멀티플랫폼 설정 (Gradle README 예제 그대로):**
```groovy
from {
  platforms {
    platform { architecture = 'amd64'; os = 'linux' }
    platform { architecture = 'arm64'; os = 'linux' }
  }
}
```

**⭐ 출력이 매니페스트 리스트인가 — FAQ가 직접 답한다 (YES)**
> "When multiple platforms are specified, **Jib creates and pushes a manifest list (also known as a fat manifest)** after building and pushing all the images for the specified platforms."
> — Jib 공식 FAQ

> ⚠️ Maven README의 property 설명("select from a manifest list")만 보면 **입력 선택**으로만 읽힌다. **반드시 FAQ의 위 문장을 근거로 쓸 것.**

**Jib 멀티플랫폼의 제약 — 책에 반드시 병기** (**incubating feature**로 표시됨)
- "**OCI image indices are not supported** (as opposed to Docker manifest lists)."
- "**Does not support pushing to a Docker daemon** (`jib:dockerBuild` / `jibDockerBuild`) **or building a local tarball**" → **멀티플랫폼은 레지스트리 push 경로 전용**
- architecture·os만 지원 (variant 미지원)
- 로컬 Docker 데몬 이미지·타르볼을 베이스로 쓸 수 없음
- **크로스 컴파일 미지원** — "platform-specific binaries needed"

> ⚠️ **"매니페스트 리스트를 만든다"와 "크로스 컴파일 미지원"은 모순이 아니다.** 앞은 **출력 이미지 형태**, 뒤는 **플랫폼별 네이티브 바이너리가 필요한 경우** Jib이 그걸 대신 만들어주지 않는다는 제약이다. 나란히 읽는 독자가 충돌로 오해하기 쉬우니 **책에서 이 구분을 반드시 붙일 것.**
> ⚠️ "순수 JVM 바이트코드 앱이면 이 제약이 실질 문제가 아니다"는 **1차 소스로 확인되지 않은 해석이다.** 쓰려면 `(사실 확인 필요)` 표시.
> ⚠️ **"Docker 데몬이 전혀 필요 없다"는 단정을 피하라.** README에 "does not require a Docker daemon"류 **적극적 문장은 확보하지 못했다.** 확인된 것은 `jib`(레지스트리 직행)과 `jibDockerBuild`(데몬 사용) **태스크가 분리되어 있다는 관찰된 사실**뿐이다. 그 구조 자체를 근거로 서술할 것.

**⭐⭐ 3경로 비교표 (이제 완성됐다 — 요구 2번 챕터의 뼈대)**

| | **Dockerfile + buildx** | **Paketo** (`bootBuildImage`) | **Jib** |
|---|---|---|---|
| **1회 빌드 멀티아키 출력** | ✅ **가능** — `--platform linux/amd64,linux/arm64` (`docker-container` 드라이버) | ❌ **불가** — `imagePlatform` 단일 값 | ✅ **가능** — `platforms` 복수 지정 시 매니페스트 리스트 push (**incubating**) |
| **멀티아키 제약** | 스토어 종류에 따라 `--load` 가부가 갈림(§8-6) | 아키텍처별 독립 빌드 후 `docker manifest`로 합성 | **레지스트리 push 전용.** `jibDockerBuild`·`jibBuildTar` 불가. **OCI index 미지원** |
| **베이스 이미지** | 직접 `FROM` 지정 | 빌더가 결정 (`paketobuildpacks/builder-noble-java-tiny:latest`) | 기본 `eclipse-temurin:{ver}-jre` |
| **Docker 데몬** | 필요 | 필요 | `jib`은 레지스트리 직행 (위 ⚠️) |
| **`FROM` 고민** | 있음 | 없음 | 없음(기본값 자동) |

> ⭐ **이 표가 요구 2번 챕터의 구조를 정한다.** "Dockerfile을 직접 쓸 때만 `FROM` 고민이 생긴다"는 구조가 여기서 자연스럽게 도출되고, §8-3(베이스 이미지 선택)이 그 자리에 붙는다.

### 8-3. G3 해소 — 베이스 이미지 선택 기준 (요구 3번의 빈칸이 채워졌다)

**Google distroless** [프로젝트 공식 README]
> "Distroless" images contain **only your application and its runtime dependencies**.
> they do not include "**package managers, shells or any other programs** you would expect to find in a standard Linux distribution."

- 자바 이미지: `gcr.io/distroless/java-base-debian13`, `java17-debian13`, `java21-debian13`, `java25-debian13`
- 아키텍처: amd64, **arm64**, s390x, ppc64le, riscv64 → **맥에서 그대로 쓸 수 있다**
- 태그 변형: `latest`, `nonroot`, `debug`, `debug-nonroot`. 디버그 이미지는 "a busybox shell to enter" 제공
- 자바 이미지 deprecated 표시 **없음**

> ⭐ **자바 독자에게 distroless를 설명하는 가장 빠른 3단 논리:** 셸이 없다 → `docker exec ... sh`가 안 된다 → 그래서 `:debug` 태그가 따로 있다.

**Alpine** [alpinelinux.org 공식]
> "Alpine Linux is built around **musl libc and busybox**. This makes it small and very resource efficient."
> "A container requires **no more than 8 MB**" / "a minimal installation to disk requires around 130 MB"
> 보안: "All userland binaries are compiled as **Position Independent Executables (PIE)** with stack smashing protection."

**Debian slim** [Docker Official Images 문서]
> `-slim`: "an experiment in providing a slimmer base (**removing some extra files that are normally not necessary within containers, such as man pages and documentation**)"

- 스위트: `bookworm`(12), `bullseye`(11), `trixie`(13, latest)
- 아키텍처: amd64, arm32v5, arm32v7, **arm64v8**, i386, mips64le, ppc64le, riscv64, s390x

> ⭐ **핵심 대비:** slim은 **man page·문서를 뺀 것**이지 런타임을 바꾼 게 아니다(여전히 glibc/Debian). Alpine은 **libc 자체가 다르다**(musl). **이 차이가 자바에서 갈리는 지점이다.**

**Eclipse Temurin** [Docker Official Images 문서]
- 태그: `eclipse-temurin:25-jdk-alpine-3.23`, `:25-jre-jammy`, `:25-jdk-noble` (jammy/noble/resolute는 Ubuntu 릴리스 코드네임)
- 아키텍처: amd64, arm32v7, **arm64v8**, ppc64le, riscv64, s390x, windows-amd64
- **Alpine 변형 공식 caveat (원문):** "Alpine Linux is much smaller than most distribution base images (**~5MB**)... but the main caveat to note is that it does use **musl libc instead of glibc** and friends, so software will often run into issues depending on the depth of their **libc requirements/assumptions**."
- ⭐ **공식 권고:** "JRE images are available for all versions of Eclipse Temurin but it is recommended that you **produce a custom JRE-like runtime using `jlink`**." → `jlink` 절의 공식 근거

**⛔⛔ G3 핵심 판정 — "Alpine JDK는 Java API의 부분집합만 지원한다"는 주장은 책에 쓰지 마라**

§4-5에 실린 커뮤니티 주장(`huksley`, 2023-03, 본인도 불확실 표시)에 대한 판정: **뒷받침하는 공식 서술을 찾지 못했고, 반증이 우세하다.**
1. **Eclipse Temurin이 `eclipse-temurin:25-jdk-alpine-3.23`을 JDK로 배포한다.** 부분집합 런타임이면 `jdk` 태그를 달 수 없다
2. **공식 caveat은 Java API가 아니라 libc 문제다** — 네이티브 라이브러리(JNI)·libc 의존 소프트웨어의 호환성 문제이지, Java 표준 API가 잘려 있다는 말이 아니다

> **책에 쓸 형태:** "Alpine 자바 이미지의 진짜 주의점은 API가 아니라 **musl libc**다. 네이티브 라이브러리를 쓰는 의존성(일부 이미지 처리, 암호화, DB 드라이버)에서 문제가 날 수 있다." — 이건 Temurin 공식 caveat으로 근거가 있다.
> ⛔ 민담의 기원을 확인하려 `openjdk.org/jeps/386`을 시도했으나 **HTTP 403**. JEP 번호·제목·상태 전부 미확인 → **인용 금지.**

**⭐ 베이스 이미지 선택 요약표 (책 초안용)**

| 후보 | 특징 | 공식 근거 |
|------|------|-----------|
| `eclipse-temurin:{ver}-jre-{noble\|jammy}` | Ubuntu 기반, glibc, 무난한 기본값 | Temurin README |
| `eclipse-temurin:{ver}-jdk-alpine-{ver}` | ~5MB 베이스, **musl libc 주의** | 위 README caveat |
| `debian:{suite}-slim` | man page·문서 제거, 런타임은 그대로 | debian README |
| `gcr.io/distroless/java{17\|21\|25}-debian13` | 셸·패키지 매니저 없음, `nonroot`/`debug` 변형 | distroless README |
| `bellsoft/liberica-openjre-debian:25-cds` | **Spring Boot 공식 문서 예제가 쓰는 이미지**, CDS/AOT 친화 | Spring Boot 문서(표기 4.1.0) |

> ⚠️ BellSoft Liberica 자체의 태그 라인업(musl/alpine 변형 존재 여부)은 **미확인** — bell-sw.com 공식 문서 미열람.

**⭐ 부수 수확 — CDS/AOT 캐시 (별도 절 하나를 만들 만하다)** [Spring Boot 공식 문서, 표기 4.1.0]

Spring 공식 Dockerfile 예제의 주석: "This layout is efficient to start up and **AOT cache (and CDS) friendly**"

| 기법 | 훈련 실행 | 실행 |
|------|----------|------|
| **AOT 캐시 (Java 25+)** | `RUN java -XX:AOTCacheOutput=app.aot -Dspring.context.exit=onRefresh -jar application.jar` | `ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "application.jar"]` |
| **CDS (Java 24+)** | `RUN java -XX:ArchiveClassesAtExit=application.jsa -Dspring.context.exit=onRefresh -jar application.jar` | `ENTRYPOINT ["java", "-XX:SharedArchiveFile=application.jsa", "-jar", "application.jar"]` |

**문서의 권고: Java 25+에서는 CDS보다 AOT 캐시를 권장.**
> ⚠️ 실측 맥의 Java는 **21.0.10**이다(L-1). 두 기법 모두 그보다 높은 버전을 요구하므로, 책에서 실습으로 넣으려면 **독자의 JDK 버전 전제를 명시**해야 한다.

### 8-4. G4 해소 — `docker scout` CLI

[Docker 공식 CLI 레퍼런스] 하위 명령 19개. 책에서 쓸 핵심:

| 명령 | 문서 원문 |
|------|-----------|
| `quickview` | "Quick overview of an image" |
| `cves` | "Display CVEs identified in a software artifact" |
| ⭐ `recommendations` | "**Display available base image updates and remediation recommendations**" |
| `sbom` | "**Generate or display SBOM of an image**" |
| `compare` | "Compare two images and display differences **(experimental)**" |
| `attestation` / `vex` / `policy`* / `environment`* / `stream`* | attestation·VEX 관리, Rego 정책 평가 등 (*표시는 experimental) |

> ⭐ **`recommendations`가 요구 3번("업데이트")과 정확히 맞물린다** — "베이스 이미지를 언제 올릴까"에 대해 도구가 직접 권고를 준다.
> ⚠️ `compare`·`policy`·`environment`·`stream`은 문서에 **`(experimental)` 표시가 있다.** 책에 쓸 때 반드시 병기.

**번들 여부 — 해소** [docs.docker.com/scout/install/]
> "**The Docker Scout CLI plugin comes pre-installed with Docker Desktop.**"
> "If you run Docker Engine without Docker Desktop, Docker Scout doesn't come pre-installed, but you can install it as a standalone binary."

→ **맥 독자(Docker Desktop 사용)는 추가 설치 없이 바로 `docker scout`을 쓸 수 있다.** 실습 진입 장벽이 낮다.

### 8-5. ⭐ G5 해소 — Docker Desktop 내장 Kubernetes는 **kubeadm/kind 선택제**다

[docs.docker.com/desktop/features/kubernetes/]

> "Open the Docker Desktop Dashboard and select the **Kubernetes** view. Select **Create cluster**. Choose your cluster type: **Kubeadm** creates a single-node cluster and the version is set by Docker Desktop. **kind** creates a multi-node cluster and you can set the version and number of nodes."

⭐ **1차 리서치에 없던 발견.** "설정에서 체크박스 하나 켜면 클러스터가 뜬다"는 옛 모델로 서술하면 **틀린다.**

**공식 비교표 (문서에 실린 표 그대로):**

| 항목 | kubeadm | kind |
|------|---------|------|
| 멀티 노드 지원 | No | Yes |
| 버전 선택 | No | Yes |
| 프로비저닝 속도 | ~1 min | ~30 seconds |
| ECI 지원 | No | Yes |
| **Docker image store 호환** | Yes | **No** |
| containerd image store 호환 | Yes | Yes |

> ⭐⭐ **`kind`가 Docker image store와 호환되지 않는다**는 항목이 실무적으로 가장 아프다. 로컬에서 `docker build`한 이미지를 kind 클러스터가 바로 못 본다는 뜻이고, **자바 개발자가 "로컬에서 빌드해서 로컬 클러스터에 올린다" 흐름에서 정확히 부딪히는 벽**이다. §8-6의 이미지 스토어 논의와 이어진다. 요구 4번 챕터의 핵심 실습 함정.

**번들 Kubernetes 버전 — 문서에 명시 없음 (확정)**
- kubeadm 경로: "the version is **set by Docker Desktop**" (사용자가 못 고름)
- kind 경로: "**you can set the version**"
- 문서가 안내하는 것은 직접 확인뿐: "check which version of Kubernetes you're on with: `kubectl version`"

> ✅ **이건 미확인이 아니라 "문서에 없음"으로 확정됐다.** 1차 리서치가 4.83.0 릴리스 노트에서 못 찾은 것과 일관된다 — **Docker가 이 숫자를 문서에 고정하지 않는다.** 책에는 **특정 버전 숫자를 쓰지 말고 `kubectl version`으로 확인하라고 안내할 것.**
> ⚠️ minikube·독립 kind와의 공식 비교는 이 페이지에 없다(미확인). 다만 위 kubeadm vs kind 표는 **공식 표라 인용이 안전하다.**

### 8-6. ⚠️⚠️ G6 부분 해소 — `--load` "절대 규칙"은 틀린다 (이 리서치에서 가장 중요한 교정)

**`exec format error` 문자열:** 확인한 페이지(멀티플랫폼 문서 2판 + docs.docker.com 도메인 검색)에서 **찾지 못했다.**
> ⚠️ **"공식 문서에 없다"고 단정하지 말고 "확인한 페이지에서 못 찾았다"로 표기할 것.**

**대신 원인은 공식이 명확히 서술한다:**
> "Multi-platform images contain a **manifest list**, pointing to multiple manifests, each of which points to a different configuration and set of layers."

컨테이너는 호스트 커널을 공유하므로 안에서 도는 코드가 호스트 아키텍처와 호환돼야 한다 → 에뮬레이션 없이는 arm64 호스트에서 linux/amd64 컨테이너를 못 돌린다. 플랫폼 미지정 상태에서 로컬 캐시 이미지의 OS/아키텍처가 안 맞으면 **가용 이미지로 컨테이너를 만들되 플랫폼 불일치 경고를 붙인다**(§2-1의 경고 템플릿이 여기서 나온다).

**에뮬레이션 성능 (공식):**
> "**Emulation with QEMU can be much slower than native builds, especially for compute-heavy tasks like compilation** and compression or decompression."

→ ⭐ **자바 빌드는 정확히 "compute-heavy compilation" 범주다.** §8-1의 `imagePlatform=linux/amd64` 경로가 왜 아픈지, §2-2의 33,656초가 왜 나왔는지를 이 한 문장이 설명한다.

**`--load` / `--push` / `--platform`** [buildx CLI 레퍼런스]

| 옵션 | 문서 원문 |
|------|-----------|
| `--load` | "Shorthand for `--output=type=docker`" |
| `--push` | "Shorthand for `--output=type=registry`" |
| `--platform` | "Set the target platform for the build. All `FROM` commands inside the Dockerfile without their own `--platform` flag will pull base images for this platform." |

**`--platform`의 복수 값:** **`docker-container` 드라이버**를 쓸 때 콤마 구분 복수 지정이 가능하고, 그 결과 **모든 플랫폼에 대한 매니페스트 리스트**가 만들어진다.
→ ⭐ **이게 §8-1과의 결정적 대비다.** buildx의 `--platform`은 콤마 목록을 받는다. `pack`의 `--platform string`은 안 받는다. Spring의 `imagePlatform`도 안 받는다.

**⛔⛔ 문서 간 충돌 1건을 발견하고 해소했다 — 책의 정확성에 직결된다**

Docker 문서 두 곳이 정면 충돌하는 것처럼 보였다:
> (A) "**The default image store in Docker Engine doesn't support loading multi-platform images.**" — buildx build CLI 레퍼런스
> (B) "**Docker Desktop and Docker Engine 29.0+ use the containerd image store by default, which supports multi-platform images out of the box.**" — multi-platform 문서

**세 번째 1차 소스(containerd 스토어 문서)가 조건을 확정한다:**
> "Building and storing multi-platform images locally. **With classic storage drivers, you need external builders for multi-platform images.**"
> "The containerd image store is the default storage backend for **Docker Engine 29.0 and later on fresh installations**."
> "**If you upgraded from an earlier version, your daemon continues using the legacy graph drivers (overlay2)** until you enable the containerd image store."

→ **모순이 아니라 스토어 세대가 다르다.** (A)의 "default image store"는 **classic/legacy 그래프 드라이버(overlay2)**를 가리키는, containerd 전환 이전 시점의 서술이다.

**⭐ 책에 쓸 실무 규칙 (반드시 조건부로):**
- **containerd 이미지 스토어**면 멀티플랫폼 이미지를 **로컬에 빌드·저장할 수 있다.** Docker Desktop과 **Docker Engine 29.0+ 신규 설치**는 기본이 containerd → **맥에서 Docker Desktop을 쓰는 이 책의 독자는 대체로 여기에 해당한다**
- **classic 스토리지 드라이버**(구버전에서 업그레이드해 overlay2를 계속 쓰는 경우)면 로컬에 못 넣는다 → 외부 빌더 + **`--push`로 레지스트리 경유** 필요
- 콤마로 여러 플랫폼을 쓰려면 **`docker-container` 드라이버 빌더**가 필요하다
- 단일 플랫폼이면 어느 쪽이든 `--load`로 로컬 확인 가능

> ⛔ **"멀티플랫폼은 `--load` 못 한다"를 무조건 규칙으로 쓰면 독자 다수에게 틀린 지시가 된다.** 반드시 "내 스토어가 무엇인지 확인하는 법"을 먼저 안내한 뒤 조건부로 서술할 것.
> ⚠️ **스토어 확인 명령 자체는 공식 문서로 확인하지 않았다 — `(사실 확인 필요)`.**
> ⛔ (A)·(B) 두 문장은 **의역 금지.** 같은 문서를 두 번 페치했을 때 렌더링 범위가 미묘하게 달랐다. 특히 **"Docker Engine 29.0+"라는 버전 경계는 원문 그대로만** 쓸 것.

**⭐ 책에서 가르칠 정석 확인 명령** [buildx imagetools inspect 공식 레퍼런스]
> 설명: "**Show details of an image in the registry**" / 사용법: `docker buildx imagetools inspect [OPTIONS] NAME`
> `--format` (기본값 `{{.Manifest}}`) / `--raw` — "Show original, unformatted JSON manifest"

문서 예제 그대로:
```console
$ docker buildx imagetools inspect moby/buildkit:master --format "{{.Manifest}}"
$ docker buildx imagetools inspect --raw moby/buildkit:master | jq
```

> ⛔ **"내 이미지가 무슨 아키텍처인가"를 확인하는 방법으로는 이 명령만 가르칠 것.** `docker image inspect --format '{{.Os}}/{{.Architecture}}'` 같은 다른 명령은 이번 리서치에서 공식 문서로 확인하지 않았다.

### 8-7. G7 — 한국어 최신 사례: 확인 범위 내 0건

도메인 한정 검색 3회(d2.naver.com, toss.tech, techblog.woowahan.com, tech.kakao.com, engineering.linecorp.com, techblog.lycorp.co.jp):

| 검색어 | 결과 |
|--------|------|
| `Apple Silicon 컨테이너 멀티아키텍처 arm64 amd64 도커 빌드 배포` | 멀티아키 직결 한국어 글 **0건** |
| `도커 컨테이너 이미지 빌드 스프링 부트 배포 쿠버네티스 2024 2025` | 쿠버네티스·배포 글 다수, **멀티아키·Apple Silicon 직결 0건** |
| `M1 맥북 Apple Silicon 도커 arm64 로컬 개발 환경` | **0건** |

> ⛔⛔ **이걸 "국내에 이런 글이 사실상 없다"로 격상하지 말 것.** 근거는 검색 3회뿐이고 그 정도로는 부재를 증명할 수 없다. **서문 포지셔닝 문구로 인용 금지** — 서문은 검증 불가능한 단정이 그대로 굳는 자리다. 쓰려면 "확인한 범위에서는 찾지 못했다"로만.

**근접 자료(한국어 아님):** "Docker Bake 食譜公開：一次烤出多種 Image" — techblog.lycorp.co.jp (**번체 중국어**, 발행일 미확인). `--platform linux/amd64,linux/arm64`와 Docker Bake를 다룬다. **버전·플래그 근거로 쓰지 말 것**(2차 소스). "LY Corp에서도 Bake로 멀티아키를 묶어 관리한다" 정도의 맥락 예시로만.

**배경용 국내 사례 (제목·URL만 확인, 본문 미열람 — 인용하려면 별도 확인):**
- 우아한형제들 "쿠버네티스를 이용해 테스팅 환경 구현해보기" / "안정적인 AI 서빙 시스템 + 자동화"
- 카카오 "쿠버네티스 프로비저닝 툴과의 만남부터 헤어짐까지" (URL에 2023-02-10 표기)
- LINE "Private Docker Registry를 구축하기 위한 오픈소스 Harbor 도입기"

### 8-8. 보강 조사가 남긴 미확인

| 항목 | 상태 |
|------|------|
| `buildpacks/pack#1570`의 종료 사유 | 페이지 추출이 메인테이너 코멘트를 반환하지 않음. 번호·제목·Closed·생성일만 확인 |
| Jib 릴리스 날짜 전부 | **폐기** (날짜 추출 오류 확정) |
| Jib "Docker 데몬 불필요"의 적극적 문장 | 미확보 — 구조적 추론으로만, 단정 금지 |
| OpenJDK Alpine/musl 포트 JEP | **HTTP 403** — 번호·제목·상태 전부 미확인, 인용 금지 |
| `exec format error` Docker 공식 서술 | 확인한 페이지에서 미발견 (부재 단정 금지) |
| 내 Docker가 어느 이미지 스토어를 쓰는지 **확인하는 명령** | 공식 문서 미확인 — **(사실 확인 필요)** |
| BellSoft Liberica 태그 라인업 | bell-sw.com 미열람 |
| Docker Desktop vs minikube·독립 kind 공식 비교 | 없음 |
| Jib 멀티플랫폼이 순수 JVM 앱에서 실질 제약이 없는지 | 저자 해석, 1차 소스 미확인 |

---

## 신선도 원장

> **Phase 4 fact-checker 대조표.** 소스별 발행일·버전 시점·검색 시점을 보존한다. 개별 `research/*.md`가 정리되더라도 이 표만으로 그라운딩이 가능하도록 설계했다.
>
> **"발행일 미확인"을 읽는 법:** 미확인이 많은 것은 리서치 태만이 아니라 **소스 유형의 구조적 특성**이다. `docs.docker.com` / `docs.spring.io` / `kubernetes.io/docs` / 프로젝트 문서 사이트는 **본문에 발행일을 노출하지 않는다.** 이 경우 "검색 시점"이 사실상의 유효 기준이다. 반대로 **날짜가 있는 행은 실제로 페이지에 인쇄된 값**이다. **GitHub Releases에서 온 날짜는 적극적으로 폐기했다**(§4-8 상충 1) — 해당 행의 "미확인"은 판단이지 누락이 아니다.

### L-1. 실측 (probe) — 표본 1, 일반화 금지

| 주장 | 값 | 소스 | 측정 시점 |
|------|-----|------|-----------|
| 호스트 | macOS 26.5.2 (25F84) / arm64 | `sw_vers`, `uname -m` | 2026-07-25 |
| Docker Desktop 설치 버전 | 4.83.0 | 앱 번들 `CFBundleShortVersionString` | 2026-07-25 |
| Rancher Desktop 설치 버전 | 1.17.1 | 동일 | 2026-07-25 |
| `docker` CLI 실체 | `~/.rd/bin/docker`, `27.5.0-rd` (Rancher 빌드) | `command -v docker`, `docker --version` | 2026-07-25 |
| 활성 context / 데몬 | `desktop-linux` → **Docker Desktop 29.6.2 / aarch64** | `docker context ls`, `docker info` | 2026-07-25 |
| `DOCKER_HOST` | unset (접속 대상은 context가 결정) | shell | 2026-07-25 |
| Docker Compose | v5.3.1 | `docker compose version` | 2026-07-25 |
| buildx | v0.35.0-desktop.2 | `docker buildx version` | 2026-07-25 |
| kubectl client | v1.32.1 (Kustomize v5.5.0) | `kubectl version --client` | 2026-07-25 |
| minikube | v1.35.0 | `minikube version` | 2026-07-25 |
| Java | OpenJDK 21.0.10 LTS (2026-01-20) | `java -version` | 2026-07-25 |
| **활성 kubectl 컨텍스트** | **원격 EKS** (`ap-northeast-2`), 로컬 `docker-desktop`·`minikube`는 비활성 | `kubectl config get-contexts` | 2026-07-25 |
| `MaxRAMPercentage` 기본값 | **25.0** (JDK 21.0.10 관측) | `java -XX:+PrintFlagsFinal -version` | 2026-07-25 |
| `MinRAMPercentage` / `InitialRAMPercentage` | 50.0 / 1.5625 | 동일 | 2026-07-25 |
| `ActiveProcessorCount` 기본값 | -1 | 동일 | 2026-07-25 |
| Rancher Desktop이 PATH에 심는 바이너리 | `docker`, `docker-buildx`, `docker-compose`, `nerdctl`, `rdctl`, `helm`, `kubectl`, `kuberlr`, `spin`, credential helper 3종 | `ls ~/.rd/bin` | 2026-07-25 |

### L-2. 웹 1차 소스 — 버전 민감 주장

| 주장 | 값 | 1차 소스 | 발행일 | 검색 시점 |
|------|-----|----------|--------|-----------|
| Docker Desktop 최신 릴리스 | **4.83.0** | docs.docker.com/desktop/release-notes/ | **2026-07-20** (본문 인쇄값) | 2026-07-25 |
| ↳ 번들 Docker Engine | v29.6.2 | 동일 | 2026-07-20 | 2026-07-25 |
| ↳ 번들 Docker Compose | **v5.3.1** | 동일 | 2026-07-20 | 2026-07-25 |
| ↳ 번들 "Docker Desktop Build" | v0.36.0 (실측 buildx v0.35.0-desktop.2와 불일치 — §4-9) | 동일 | 2026-07-20 | 2026-07-25 |
| Docker Desktop 무료 임계값 | 직원 **250명 미만 AND** 연매출 **$10M 미만** | docs.docker.com/subscription/desktop-license/ | 미확인 | 2026-07-25 |
| VMM 선택지 | Docker VMM(Beta, Apple Silicon 전용) / Apple Virtualization framework / QEMU(legacy) | docs.docker.com/desktop/settings-and-maintenance/settings/ | 미확인 | 2026-07-25 |
| Rosetta 옵션 전제 조건 | **Apple Virtualization framework 선택 시에만** 사용 가능. 기본 Disabled | 동일 | 미확인 | 2026-07-25 |
| Docker VMM의 Rosetta 지원 | **미지원** — "emulation of amd64 architectures is slow" | docs.docker.com/desktop/features/vmm/ | 미확인 | 2026-07-25 |
| Docker VMM 최소 메모리 | 4GB | 동일 | 미확인 | 2026-07-25 |
| 기본 파일공유 구현 | VirtioFS (대안 gRPC FUSE). "up to 98%" 개선 | settings 문서 | 미확인 | 2026-07-25 |
| Docker Desktop 기본 메모리 한도 | 호스트 메모리의 **50%** (swap 기본 1GB) | 동일 | 미확인 | 2026-07-25 |
| **기본 VMM이 무엇인가** | **미확인** | — | — | 2026-07-25 |
| containerd image store 기본 활성 | Docker Desktop **4.34 이상** | docs.docker.com/desktop/features/containerd/ | 미확인 | 2026-07-25 |
| 클래식 이미지 스토어 한계 | 매니페스트 리스트 미지원 → 멀티플랫폼 로컬 로드 불가 | 동일 | 미확인 | 2026-07-25 |
| `docker-container` 드라이버 주의 | 결과가 Engine 이미지 스토어에 자동 로드되지 않음 | docs.docker.com/build/building/multi-platform/ | 미확인 | 2026-07-25 |
| docker context 우선순위 | CLI 플래그 > 환경변수 > 활성 context | docs.docker.com/engine/manage-resources/contexts/ | 미확인 | 2026-07-25 |
| 태그의 해석 방식 | `FROM alpine:3.21` → 3.21의 **최신 패치**로 해석(고정 아님) | docs.docker.com/build/building/best-practices/ | 미확인 | 2026-07-25 |
| digest 고정의 보장 | 퍼블리셔가 태그를 갈아끼워도 같은 이미지 보장 | 동일 | 미확인 | 2026-07-25 |
| 베이스 이미지 갱신 명령 | `docker build --pull` (캐시 무시는 `--no-cache`) | 동일 | 미확인 | 2026-07-25 |
| 캐시 재사용 규칙 | "instruction and the files it depends on hasn't changed" | docs.docker.com/build/cache/optimize/ | 미확인 | 2026-07-25 |
| `.dockerignore` 적용 범위 | 하위 디렉터리 포함 **전체 빌드 컨텍스트** | 동일 | 미확인 | 2026-07-25 |
| **Spring Boot 현재 GA (Latest 배지)** | **v4.1.0** (v4.0.7·v3.5.16 병행) | github.com/spring-projects/spring-boot/releases | **미확인 — 날짜 폐기 (§4-8)** | 2026-07-25 |
| Spring Boot 플러그인 기본 빌더 | `paketobuildpacks/builder-noble-java-tiny:latest` | docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| `imagePlatform` 도입 버전 | **Since 3.4.0** | docs.spring.io/spring-boot/maven-plugin/build-image.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| **`imagePlatform` 기본값** | **없음 = 호스트 머신 플랫폼 사용** | 동일 | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| `bootBuildImage` 옵션 전체 | builder, trustBuilder, imagePlatform, runImage, imageName, pullPolicy, environment, buildpacks, bindings, network, cleanCache, verboseLogging, publish, tags, buildWorkspace, buildCache, launchCache, createdDate, applicationDirectory, securityOptions | Gradle 플러그인 문서 | 미확인 (표기 4.1.0) | 2026-07-25 |
| **noble 빌더의 퍼블리시 플랫폼** | **linux/amd64 + linux/arm64** (OCI image index) | `docker buildx imagetools inspect ... --raw` (레지스트리 직접 조회) | 해당 없음 (조회 시점 상태) | 2026-07-25 |
| `run-noble-tiny:latest` 플랫폼 | linux/amd64 + linux/arm64 | 동일 | 해당 없음 | 2026-07-25 |
| `builder-jammy-java-tiny:latest` 플랫폼 | linux/amd64 + linux/arm64 | 동일 | 해당 없음 | 2026-07-25 |
| Paketo arm64 beta 태그 해제 | "no need for beta tag anymore, it's in latest" | github.com/paketo-buildpacks/java/discussions/1387 | 2024-04-04 (코멘트 2024-05-22) | 2026-07-25 |
| arm64 미지원 Java 빌드팩 | `aternity`, `google-stackdriver` 2종 | 동일 | 2024-06-11 (코멘트) | 2026-07-25 |
| bootBuildImage 크로스빌드 버그 보고 환경 | Spring Boot 3.5.4 / Gradle plugin 3.5.4 / Docker Desktop 4.42.1 / M4 Pro | github.com/spring-projects/spring-boot/issues/46665 | 2025-08-04 (오픈) | 2026-07-25 |
| ↳ **수정 릴리스** | **미확인** (CLOSED만 확인) | 동일 | 미확인 | 2026-07-25 |
| Spring Boot jar 추출 명령 | `java -Djarmode=tools -jar app.jar extract --layers --destination extracted` | docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html | 미확인 (표기 4.1.0) | 2026-07-25 |
| ↳ `-Djarmode=layertools` | **4.1.0 문서에 등장하지 않음.** 전환 시점 미확인 | 동일 | 미확인 | 2026-07-25 |
| Spring 공식 Dockerfile 예제 베이스 | `bellsoft/liberica-openjre-debian:25-cds` | 동일 | 미확인 (표기 4.1.0) | 2026-07-25 |
| layered jar 레이어 순서 | dependencies → spring-boot-loader → snapshot-dependencies → application | 동일 | 미확인 | 2026-07-25 |
| `spring-boot-docker-compose` 라이프사이클 | `none` / `start-only` / `start-and-stop` | docs.spring.io/spring-boot/reference/features/dev-services.html | 미확인 (표기 4.1.0) | 2026-07-25 |
| Testcontainers Colima 설정 3종 | `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE`, `TESTCONTAINERS_HOST_OVERRIDE`, `DOCKER_HOST` | java.testcontainers.org/supported_docker_environment/ | 미확인 | 2026-07-25 |
| ↳ OrbStack 지원 서술 | **없음(미확인)** | 동일 | — | 2026-07-25 |
| `UseContainerSupport` 기본값·플랫폼 | 기본 **true**, **Linux only** | docs.oracle.com/en/java/javase/21/docs/specs/man/java.html | 미확인 | 2026-07-25 |
| `ActiveProcessorCount` 동작 | UseContainerSupport 비활성이어도 존중됨 | 동일 | 미확인 | 2026-07-25 |
| ↳ `MaxRAMPercentage` 공식 문서 기재 | **미확인** (로컬 관측 25.0만 보유 — L-1) | — | — | 2026-07-25 |
| Paketo Memory Calculator 공식 | `Heap = Total Container Memory - Non-Heap - Headroom` | paketo.io/docs/reference/java-reference/ | 미확인 | 2026-07-25 |
| Paketo 기본 `ReservedCodeCacheSize` | 240MB | 동일 | 미확인 | 2026-07-25 |
| Jib의 정의 | "builds optimized Docker and OCI images ... **without a Docker daemon**" | github.com/GoogleContainerTools/jib | 미확인 | 2026-07-25 |
| ↳ Jib 버전·명령 문법·멀티플랫폼 | ✅ **해소 — L-7 참조** | — | — | 2026-07-25 |
| Kubernetes 지원 마이너 | **1.36 / 1.35 / 1.34** (최근 3개) | kubernetes.io/releases/ | 미확인 | 2026-07-25 |
| Kubernetes 최신 패치·EOL | 1.36.2 (2026-06-09), EOL 2027-06-28 / 1.35.6 EOL 2027-02-28 / 1.34.9 EOL 2026-10-27 | 동일 | 2026-06-09 | 2026-07-25 |
| **Kubernetes 릴리스 주기** | **"approximately three times per year" (연 3회)** | kubernetes.io/releases/release/ | 미확인 | 2026-07-25 |
| Kubernetes 패치 지원 기간 | 1.19 이상 약 1년 | kubernetes.io/releases/ | 미확인 | 2026-07-25 |
| dockershim 제거 버전 | **Kubernetes 1.24** | kubernetes.io/blog/2022/02/17/dockershim-faq/ | **2022-02-17** | 2026-07-25 |
| `docker build` 이미지의 K8s 호환성 | "will work with all CRI implementations" | 동일 | 2022-02-17 | 2026-07-25 |
| K8s 기본 imagePullPolicy 규칙 | `IfNotPresent`, **단 태그가 `:latest`면 `Always`** | kind.sigs.k8s.io/docs/user/quick-start/ | 미확인 | 2026-07-25 |
| kind 로컬 이미지 적재 | `kind load docker-image my-app:latest` | 동일 | 미확인 | 2026-07-25 |
| kind 최신 릴리스 | v0.32.0, 기본 노드 이미지 `kindest/node:v1.36.1` | github.com/kubernetes-sigs/kind/releases | **미확인 — 날짜 폐기 (§4-8)** | 2026-07-25 |
| minikube 로컬 이미지 적재 | `minikube image load my_image` | minikube.sigs.k8s.io/docs/handbook/pushing/ | 미확인 | 2026-07-25 |
| **Docker Desktop 내장 K8s 버전** | ⛔ **문서에 명시 없음 (부재 확정)** — `kubectl version`으로 확인하라고만 안내 | docs.docker.com/desktop/features/kubernetes/ | 미확인 | 2026-07-25 |
| Rancher Desktop 최신 릴리스 | v1.23.1 / 2026-06-29 | github.com/rancher-sandbox/rancher-desktop/releases | 2026-06-29 (**약한 근거**) | 2026-07-25 |
| Podman Desktop 최신 릴리스 | v1.28.3 (podman 5.8.5 번들) | github.com/podman-desktop/podman-desktop/releases | 2026-07-20 (**약한 근거**) | 2026-07-25 |
| Colima 최신 릴리스 | v0.10.3 — **1년 이상 신규 릴리스 없음** | github.com/abiosoft/colima/releases | 2025-06-04 (**약한 근거**) | 2026-07-25 |
| **OrbStack 버전** | **미확인** | — | — | 2026-07-25 |
| Linux 네임스페이스 종류 | **8종** (Cgroup/IPC/Network/Mount/PID/Time/User/UTS) | man7.org/linux/man-pages/man7/namespaces.7.html | **2026-02-08** (man-pages 6.18) | 2026-07-25 |
| cgroups v2 컨트롤러 | cpu, cpuset, freezer, hugetlb, io, memory, perf_event, pids, rdma | man7.org/linux/man-pages/man7/cgroups.7.html | **2026-02-08** (man-pages 6.18) | 2026-07-25 |
| cgroups v1/v2 관계 | v2가 v1 컨트롤러의 **부분집합만** 구현. v1은 호환성 때문에 존속 | 동일 | 2026-02-08 | 2026-07-25 |
| OCI 이미지 매니페스트 미디어 타입 | `application/vnd.oci.image.manifest.v1+json` | github.com/opencontainers/image-spec/blob/main/manifest.md | 미확인 (main 브랜치) | 2026-07-25 |
| OCI 이미지 인덱스 미디어 타입 | `application/vnd.oci.image.index.v1+json` (레지스트리 응답 실물 확인) | 동일 + 레지스트리 조회 | 해당 없음 | 2026-07-25 |
| **`docker scout` CLI 명령** | ✅ **해소 — L-7 참조** (하위 명령 19개) | — | — | 2026-07-25 |
| **`exec format error` 공식 서술** | ⚠️ **확인한 페이지에서 미발견** (부재 단정 금지 — §8-6) | — | — | 2026-07-25 |
| **rootless / cosign / SBOM 생성 공식 문서** | **미확인** | — | — | 2026-07-25 |
| 우아한형제들 K8s 테스트 환경 글 | ⚠️ **8년 전 글 — 명령·버전 인용 금지** | techblog.woowahan.com/2562/ | **2018-03-13** | 2026-07-25 |

### L-3. 논문 — 전부 조건부 수치 (측정 연도·환경 병기 필수)

| 주장 | 값 | 소스 | 측정/발행 연도 | 검색 시점 |
|------|-----|------|--------------|-----------|
| Docker vs 네이티브 (MySQL 고동시성) | 약 2%로 점근 | DOI 10.1109/ISPASS.2015.7095802 p.171 | 2015 (**측정 2014**) | 2026-07-25 |
| KVM vs 네이티브 (동일) | 전 구간 40% 초과 | 동일 | 2015 (측정 2014) | 2026-07-25 |
| Felter 실험 환경 | Xeon E5-2665×2 16코어, 256GB, Ubuntu 13.10, 커널 3.11.0, **Docker 1.0**, QEMU 1.5.0, MySQL 5.5.37 | 동일 p.171 §II | 2015 | 2026-07-25 |
| 컨테이너 기동 시간 (**리눅스 네이티브**) | Docker ~100ms / gVisor ~190ms / Kata ~600ms / LXC ~800ms | arXiv:2110.11462 §3.5 | 2021 | 2026-07-25 |
| Docker 데몬 경유 추가 지연 | 약 250ms | 동일 | 2021 | 2026-07-25 |
| secure container I/O 처리량 | 최선의 경우에도 타 플랫폼의 절반 | 동일 §3.3 | 2021 | 2026-07-25 |
| gVisor 네트워크 p90 응답시간 | 경쟁 플랫폼의 3~4배 | 동일 Finding 12 | 2021 | 2026-07-25 |
| van Rijn 실험 환경 | AMD EPYC2 7542 dual-socket, 256GiB, NVMe, Ubuntu Server 20.04 LTS | 동일 §3 | 2021 | 2026-07-25 |
| Firecracker 컨테이너당 메모리 오버헤드 | 5MB 미만 | NSDI '20 p.419 §1 | 2020 | 2026-07-25 |
| Firecracker 부팅 시간 | 125ms 미만 (애플리케이션 코드까지) | 동일 | 2020 | 2026-07-25 |
| Firecracker MicroVM 생성률 | 호스트당 초당 최대 150개 | 동일 | 2020 | 2026-07-25 |
| Firecracker 게스트 IOPS 제한 | 하드웨어 340,000+ IOPS → 게스트 약 13,000 IOPS | 동일 §5.3 p.429 | 2020 | 2026-07-25 |
| Firecracker 네트워크 처리량 | loopback 44.14 Gb/s vs Firecracker 15.61 Gb/s (1 스트림) | 동일 Table 1 | 2020 | 2026-07-25 |
| Firecracker 실험 환경 | EC2 m5d.metal, Xeon Platinum 8175M×2 48코어(HT off), 384GB, 커널 4.15.0-1044-aws | 동일 §5 | 2020 | 2026-07-25 |
| 기본 설정 컨테이너에서 성공한 익스플로잇 | **88건 중 50건 (56.82%)** | DOI 10.1145/3274694.3274720 Abstract | 2018 | 2026-07-25 |
| 격리를 뚫고 권한 상승 성공 | 11건 (공통 4단계 공격 모델) | 동일 | 2018 | 2026-07-25 |
| 수집된 유효 익스플로잇 데이터셋 | 223건 | 동일 | 2018 | 2026-07-25 |
| Lin et al. 실험 환경 | **Docker 17.09.1-ce**, 취약 커널별 배포판 교체(Ubuntu 14.04/15.10 등) | 동일 §4.1 | 2018 | 2026-07-25 |
| Borg 작업 기동 지연 | 중앙값 약 25초, 그중 **패키지 설치 약 80%** | DOI 10.1145/2741948.2741964 §3.4 | 2015 (**Borg ≠ K8s**) | 2026-07-25 |
| Borg 셀 규모 중앙값 | 약 10,000대 | 동일 §2.2 | 2015 | 2026-07-25 |
| 컨테이너 기동 중 pull 비중 | **76%** | FAST '16 Abstract | 2016 | 2026-07-25 |
| pull한 데이터 중 실제 읽히는 비율 | **6.4%** | 동일 | 2016 | 2026-07-25 |
| Slacker 개선폭 | 개발 사이클 중앙값 20배, 배포 사이클 5배 | 동일 | 2016 | 2026-07-25 |
| HelloBench 규모·대표성 | 57개 앱 / Docker Hub 라이브러리 pull의 86% 커버 | 동일 §3 | 2016 (집계 2015-01-15) | 2026-07-25 |
| ⚠️ 네임스페이스 생성 비용 | **7.94ms (SSD, σ=2.05) / 8.45ms (HDD, σ=2.57), 전체 기동의 1.5% 미만** | **arXiv:2602.15214 §4.2.1 (프리프린트)** | 2026 | 2026-07-25 |
| ⚠️ warm-start (alpine) | Azure SSD 568±5ms / **macOS 1528±139ms (σ=502)**, n=50 | 동일 Table 3 (프리프린트) | 2026 | 2026-07-25 |
| ⚠️ Docker Desktop "가상화 세금" | alpine **2.69×** / nginx **3.28×** (**하드웨어 교란 포함 — 저자 본인 고지**) | 동일 Finding 3, §3.1 | 2026 | 2026-07-25 |
| ⚠️ 이미지 크기가 warm-start에 미치는 영향 | 5MB~155MB 편차 **2.5%** (554–568ms, SSD) | 동일 Finding 1 | 2026 | 2026-07-25 |
| ⚠️ 기동 시간 변동계수 (CV) | SSD 3.4% / HDD 8.3% / **macOS 32.8%** | 동일 §4.1.2 | 2026 | 2026-07-25 |
| ⚠️ `--cpus=0.5` 실측 사용률 | SSD 60.52%(σ=3.79) / HDD 48.21%(σ=16.24) / **macOS 71.63%(σ=36.14), 이상치 최대 247%** | 동일 §4.2.2 | 2026 | 2026-07-25 |
| ⚠️ macOS 컨테이너 네트워크 RTT | bridge·host 양 모드 약 **34ms**. ⛔ **"17× slower" 배수 재계산 금지 — 논문이 분모 미명시** | 동일 §4.2.3 | 2026 | 2026-07-25 |
| ⚠️ OverlayFS vs 볼륨 쓰기 (**티어 내부 비율만 유효**) | SSD **0.006×** / HDD **0.010×** / **macOS 1.06× (p=0.21, 유의하지 않음)**. ⛔ **티어 간 절대 MB/s 비교는 ❌** | 동일 Table 4 | 2026 | 2026-07-25 |
| ⚠️ 컨테이너 간 페이지 캐시 공유 효율 | 약 **0%** (동일 nginx 3개가 1개의 3배 메모리) | 동일 §4.3.3 | 2026 | 2026-07-25 |
| ⚠️ Khan 실험 환경 | macOS: **M1 Pro, 16GB, APFS/VM, Docker 28.4.0, Hypervisor.framework** / Azure: Standard_D2s_v3 2 vCPU, Docker 28.x, overlay2 | 동일 Table 2 | 2026 | 2026-07-25 |
| Docker Hub 조사 규모 | 저장소 975,858 / 이미지 2,227,244 / 개발자 349,861 | DOI 10.1007/978-3-030-58951-6_13 Table 1 | 2020 (**수집 2019경**) | 2026-07-25 |
| Docker Hub 악성 이미지 | 42개 (20,000+ 스캔 중) | 동일 Abstract·§5.2 | 2020 (수집 2019경) | 2026-07-25 |
| 공식 저장소(147개) 악성 실행 프로그램 | **0건** | 동일 §5.2 | 2020 | 2026-07-25 |
| 이미지 취약점 패치 지연 | **평균 422일** | 동일 §1 | 2020 (수집 2019경) | 2026-07-25 |
| 고위험/치명 취약점 보유 비율 | 공식 최신본 약 30% / **커뮤니티 64% 초과** | 동일 §5 | 2020 | 2026-07-25 |
| 권장 run-command당 민감 파라미터 | 평균 1개 (예: `--privileged`) | 동일 §1·§2 | 2020 | 2026-07-25 |
| eBPF 컨테이너 탈출 실증 | Jupyter/셸 서비스 5곳 + GCP Cloud Shell 침해; 주요 클라우드 3사 K8s에서 노드 간 공격 가능 | USENIX Sec '23 Abstract | 2023 (⚠️ **본문 미확보**) | 2026-07-25 |
| ⭐ arXiv 전수 검색 `abs:"Docker Desktop"` | **전체 아카이브 2편** | arXiv API | — | 2026-07-25 |
| ⭐ arXiv 전수 검색 `abs:"Apple Silicon" AND abs:container` | **3편, 전부 컨테이너 성능 연구 아님** | arXiv API | — | 2026-07-25 |

### L-4. 커뮤니티 — 게시 시점·조회 시점 상태

> ⛔ **이 표의 값은 "그 사용자의 환경에서 그 시점에 그렇게 보였다"일 뿐이다. 버전·수치의 근거가 아니다.**
> 🟢 메인테이너 / 🟡 다수 재현 / 🔴 단일 익명

| 주장·일화 | 출처 | 게시 시점 | 상태(2026-07-25) | 신뢰도 |
|-----------|------|-----------|------------------|--------|
| M4 맥에서 amd64 busybox조차 `exec format error`; binfmt_misc 가설 | docker/for-mac#7849 | 2026-02-05 | CLOSED(재현불가 2026-04-30) | 🔴 + 🟢 가설, **미해결** |
| VM 매니저 변경 실패 → 공장 초기화, 전부 소실 | 위 이슈 댓글 | 2026-02-25 | — | 🔴 |
| Docker Desktop 4.27.1에서 QEMU 위 JVM `signal 11`; **해결은 macOS 14.3** | docker/for-mac#7172 | 2024-02-05 | **OPEN** | 🟡 + 🟢 |
| Rosetta 켜고 amd64 빌드 **33,656초**; 끄고 5분 | docker/for-mac#7075 | 2023-11-12 | **OPEN** | 🟡 (M1/M2 Max/M3 Max/M3 Pro) |
| M1 Max GraalVM 빌드 수시간 정체; Paketo 빌더가 amd64/QEMU | spring-boot#33119 | 2022-11-13 | CLOSED | 🔴 + 🟢 위키 반영 |
| "왜 이게 어디에도 안 적혀 있죠?" | 위 이슈 댓글 | 2022-11-14 | — | 🔴 |
| M1 bootBuildImage 산출물이 **amd64** → arm64 클라우드에서 즉사 | paketo/spring-boot#491 | 2024-06-21 | CLOSED | 🔴 + 🟢 처방 |
| 아키텍처 무시하는 빌드 캐시 → 헬퍼만 `exec format error` | 위 이슈 댓글 | 2024-06-21 | — | 🟢 dmikusa |
| **"pack도 spring-boot:build-image도 한 번에 멀티아키 못 만든다"** | 위 이슈 댓글 | **2024-11-21** | — | 🟢 dmikusa `(G1 재확인 중)` |
| `Image platform mismatch detected`; containerd 스토어 토글이 변수 | spring-boot#46665 | 2025-08-04 | CLOSED | 🟡 + 🟢 philwebb 재현 |
| "제목이 오해를 부른다 — arm64 호스트에서 amd64를 만들 때만" | 위 이슈 댓글 | 2025-08-04 | — | 🟢 wilkinsona |
| containerd 이미지 스토어 on/off로 재현 여부 갈림 | 위 이슈 댓글 (hojooo) | 2025-10-23 | — | 🔴 + 🟢 교차검증 |
| "the builds seemed **contaminated**" | 위 이슈 댓글 (jdnurmi) | 2025-09-04 | — | 🔴 |
| Colima 이주 후 Testcontainers/Ryuk 소켓 실패 | testcontainers-java#5034 | 2022-02-08 | CLOSED | 🟡 |
| `TESTCONTAINERS_RYUK_DISABLED=true`는 **은폐다** | 위 이슈 댓글 (kiview) | 2022-02-11 | — | 🟢 메인테이너 |
| "2 for 2 on needing to delete the old socket and symlink Colima's" | colima#365 | 2022-07-12 | **OPEN (4년째)** | 🔴 + 🟢 반론 |
| "many tools are ... utilising docker context instead" | 위 이슈 댓글 (abiosoft) | 2022-07-14 | — | 🟢 Colima 저자 |
| RD+DD 공존 시 context 미설정으로 모든 명령 실패 (**Windows**) | rancher-desktop#7712 | 2024-11-01 | OPEN | 🔴 **플랫폼 불일치** |
| 호스트 120GB 여유인데 VM 데이터 볼륨 100% → factory-reset | rancher-desktop#4457 | 2023-04-14 | CLOSED | 🔴 + 🟢 jandubois |
| Rancher Desktop 데이터 볼륨 기본 최대 100GiB | 위 이슈 (jandubois) | 2023-04 | — | 🟢 `(1차 소스 확인 필요)` |
| "Bind mounts are really slow" — **7년째 OPEN** | docker/for-mac#3677 | 2019-05-20 | **OPEN** | 제목·상태만 |
| "File access in mounted volumes extremely slow" — **10년째 OPEN** | docker/for-mac#77 | 2016-08-02 | **OPEN** | 제목·상태만 |
| Docker.qcow2가 줄어들지 않음; "+1" 댓글에 👍349 | docker/for-mac#371 | 2016-08-19 | CLOSED | 🟡 (반응 수), **10년 전** |
| K8s 도입 논쟁 (양쪽 전부) | HN 22491170 | **2020-03-05** (719pt, 469c) | — | 🔴 익명 다수, **6년 전** |
| 로컬 Colima인 줄 알고 **운영 deployment 삭제** | HN 41578274 | 2024-09-18 / 댓글 2024-09-21 | — | 🟡 ("나도 당했다" 5인) |
| OrbStack: Envoy 빌드 3~4시간 → 1시간 미만 | HN 41421846 | 2024-09-02 (307pt) | — | 🔴 **체감, 벤치마크 아님** |
| OrbStack 라이선스 서버 접속 불가로 정지 예고 | 위 스레드 | 2024-09-02 | — | 🔴 |
| OrbStack 8TB sparse image가 백업 소프트웨어를 깬다 | 위 스레드 | 2024-09-02 | — | 🔴 `(1차 소스 확인 필요)` |
| Colima는 배터리·CPU를 안 먹는다 (DD는 "especially with kubernetes on") | 위 스레드 | 2024-09-02 | — | 🔴 체감 |
| Alpine/musl 논쟁 (양쪽) | HN 35056594 | **2023-03-07** (34pt) | — | 🔴, **3년 전** |
| **musl에 DNS-over-TCP 추가됨** | 위 스레드 (_ikke_) | 2023-03-07 | — | 🔴 `(1차 소스 확인 필요 — 논쟁의 핵심 논거가 이미 무효일 수 있음)` |
| "JDK Alpine 이미지가 Java API 부분집합만 지원" | 위 스레드 (huksley) | 2023-03-07 | — | 🔴 **본인도 불확실 표시. 틀릴 가능성 높음** `(G3 확인 중)` |
| Docker Desktop 유료화 직후 Podman 회의론 | HN 28371788 | 2021-08-31 (47pt) | — | 🔴 |
| 유예 종료 직전 맥 대안 탐색; 조직 승인 성공/실패 양쪽 | HN 29815122 | 2022-01-05 | — | 🔴 |
| M1 빌드 이미지가 EC2에서 플랫폼 불일치 | velog @msung99 | 2023-01-05 | — | 🔴 `(원문 대조 필요)` |
| 레지스트리엔 있는데 파드 실행 불가 → 동료 Intel 맥에선 성공 | velog @___pepper | 2022-01-11 | — | 🔴 / **축자 확보 ✅** |
| ↳ "aws에서는 arm으로 빌드된 이미지를 실행할 수 없어서" | 동일 | 2022-01-11 | — | ⛔ **사실 아님** (Graviton 등 arm64 인스턴스 존재). 인용 시 주석 필수 |
| GitHub Actions x86 러너에서 ARM64 buildpack 빌드 실패 → 러너를 ARM으로 | velog @cmsong111 | 2025-03-09 | — | 🔴 `(원문 대조 필요)` |
| "내년부터 도커 유료화하나요?" — Desktop/Hub/Engine 혼동 | OKKY 1085503 | **날짜 미확인** | 댓글 로그인 벽 | 🔴 `(원문 대조 필요)` |
| GeekNews "Docker Desktop 대안"; 댓글에서 Podman 상태 문의 | news.hada.io/topic?id=16867 | 2024-09-21 / 댓글 2024-09-27 | — | 🔴 `(원문 대조 필요)` |

### L-5. 📒 원장 블록 — 제목·상태·날짜만 확인한 이슈군

- **출처:** `gh issue list --repo docker/for-mac | rancher-sandbox/rancher-desktop | testcontainers/*` (GitHub REST)
- **검색 시점:** 2026-07-25
- **검증된 범위:** 이슈 번호 / 제목 문자열 / `createdAt` / `state`(OPEN·CLOSED) — **이 네 가지만**
- **해당 이슈:** docker/for-mac `#77` `#371` `#1592` `#2501` `#3677` `#5164` `#5486` `#6120` `#6243` `#6678` `#6698` `#6865` `#6921` `#7093` `#7145` `#7187` `#7440` `#7464` `#7475` `#7494` `#7499` / rancher-desktop `#3080` `#3350` `#8606` `#10049` `#10443` / testcontainers-java `#8537` `#10528` / testcontainers-go `#2952` `#3460`
- ⛔ **사용 규칙: 분포·존속기간 근거로만. 인용·증상·원인·해결 서술 전면 금지.** 제목에서 이야기를 상상해 채우면 창작이다.

### L-6. ⛔ 절대 인용 금지 — 제목만 노출, 페이지 미열람

`paketo-buildpacks/base-builder#652` / `paketo-buildpacks/stacks#51` / `buildpacks/pack#1003` / `orbstack/orbstack#29` / HN 22182226 (Alpine Python, 2020-01-29, 306pt — 댓글 미열람) / HN 28368997 (Docker 라이선스 공지 제출, 2021-08-31, 135pt — 댓글 미열람)
**추가:** `buildpacks/pack#1570` (2022-12-06 생성, Closed — **종료 사유 미확인**) / `openjdk.org/jeps/386` (HTTP 403 — 번호·제목·상태 전부 미확인)

### L-7. 보강 조사분 (G1~G7) — 원본 `research/web_gapfill.md`

| 주장 | 값 | 1차 소스 URL | 발행일 | 검색 시점 |
|------|-----|--------------|--------|-----------|
| **`pack build --platform` 타입** | **`string` (단수)** — 1회 1플랫폼 | https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/pack/cli/pack_build/ | 미확인 | 2026-07-25 |
| **CNB 교차 아키텍처 앱 이미지 빌드** | **미지원** (QEMU 에뮬레이션 시 가능, 성능 페널티) | https://buildpacks.io/docs/for-app-developers/how-to/special-cases/build-for-arm/ | 미확인 | 2026-07-25 |
| CNB 멀티아키 빌더 예시 | `heroku/builder:24` (amd64 + arm64) | 동일 | 미확인 | 2026-07-25 |
| **CNB RFC 0128 범위** | 빌더·빌드팩 **패키지 한정** ("solve the statement 2"). **앱 이미지 멀티아키(statement 3)는 대상 아님.** 상태 Approved | https://github.com/buildpacks/rfcs/blob/main/text/0128-multiarch-builders-and-package.md | 미확인 | 2026-07-25 |
| pack CLI 최신 버전 | **v0.40.8** | https://github.com/buildpacks/pack/releases | **2026-07-13** | 2026-07-25 |
| `jib-maven-plugin` 버전 | **3.5.2** | jib-maven-plugin README + Releases | **미확인 (날짜 추출 오류로 폐기)** | 2026-07-25 |
| `jib-gradle-plugin` 버전 | **3.5.4** (Maven과 **독립 버저닝**) | jib-gradle-plugin README + Releases | **미확인 (동일)** | 2026-07-25 |
| `jib-core` 버전 | 0.28.2 | https://github.com/GoogleContainerTools/jib/releases | 미확인 | 2026-07-25 |
| Jib Maven 목표 | `jib:build` / `jib:dockerBuild` / `jib:buildTar` | jib-maven-plugin README | 미확인 | 2026-07-25 |
| Jib Gradle 태스크 | `jib` / `jibDockerBuild` / `jibBuildTar` | jib-gradle-plugin README | 미확인 | 2026-07-25 |
| Jib 기본 베이스 이미지 | `eclipse-temurin:{8,11,17,21,25}-jre` (WAR은 `jetty`). **`{...}`는 문서 표기법** | 위 README | 미확인 | 2026-07-25 |
| **Jib 멀티플랫폼 출력** | 복수 `platforms` 지정 시 **매니페스트 리스트 생성·push** (incubating) | https://github.com/GoogleContainerTools/jib/blob/master/docs/faq.md | 미확인 | 2026-07-25 |
| Jib 멀티플랫폼 제약 | **OCI index 미지원**, `jibDockerBuild`·`jibBuildTar` 불가, variant 미지원, 크로스 컴파일 미지원 | 동일 FAQ | 미확인 | 2026-07-25 |
| distroless 자바 이미지 태그 | `gcr.io/distroless/java{17,21,25}-debian13`, `java-base-debian13` | https://github.com/GoogleContainerTools/distroless | 미확인 | 2026-07-25 |
| distroless 태그 변형 | `latest`, `nonroot`, `debug`, `debug-nonroot` (debug는 busybox 셸 제공) | 동일 | 미확인 | 2026-07-25 |
| distroless 아키텍처 | amd64, **arm64**, s390x, ppc64le, riscv64 | 동일 | 미확인 | 2026-07-25 |
| Alpine 컨테이너 크기 | "no more than **8 MB**" (디스크 설치는 약 130 MB) | https://www.alpinelinux.org/about/ | 미확인 | 2026-07-25 |
| Alpine 구성 | **musl libc + busybox**. 전 userland 바이너리 PIE + stack smashing protection | 동일 | 미확인 | 2026-07-25 |
| Debian `-slim` 정의 | man page·문서 등 "extra files" 제거. **런타임은 그대로(glibc)** | https://github.com/docker-library/docs/blob/master/debian/README.md | 미확인 | 2026-07-25 |
| Debian 스위트 코드네임 | bookworm(12), bullseye(11), trixie(13, latest) | 동일 | 미확인 | 2026-07-25 |
| Temurin Alpine 태그 예시 | **`eclipse-temurin:25-jdk-alpine-3.23`** (JDK로 배포됨) | https://github.com/docker-library/docs/blob/master/eclipse-temurin/README.md | 미확인 | 2026-07-25 |
| Temurin 지원 아키텍처 | amd64, arm32v7, **arm64v8**, ppc64le, riscv64, s390x, windows-amd64 | 동일 | 미확인 | 2026-07-25 |
| **Alpine 자바 이미지의 공식 caveat** | Java API가 아니라 **musl libc 호환성** — "software will often run into issues depending on the depth of their libc requirements/assumptions" | 동일 | 미확인 | 2026-07-25 |
| Temurin의 `jlink` 권고 | "recommended that you produce a custom JRE-like runtime using `jlink`" | 동일 | 미확인 | 2026-07-25 |
| AOT 캐시 플래그 (Java 25+) | `-XX:AOTCacheOutput=app.aot` / `-XX:AOTCache=app.aot` | docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html | 미확인 (표기 4.1.0) | 2026-07-25 |
| CDS 플래그 (Java 24+) | `-XX:ArchiveClassesAtExit=application.jsa` / `-XX:SharedArchiveFile=application.jsa` | 동일 | 미확인 (표기 4.1.0) | 2026-07-25 |
| Spring 권고: CDS vs AOT | **Java 25+에서는 AOT 캐시 권장** | 동일 | 미확인 (표기 4.1.0) | 2026-07-25 |
| `docker scout` 하위 명령 | **19개.** `compare`/`environment`/`policy`/`stream`은 **experimental** | https://docs.docker.com/reference/cli/docker/scout/ | 미확인 | 2026-07-25 |
| `docker scout recommendations` | "Display available **base image updates** and remediation recommendations" | 동일 | 미확인 | 2026-07-25 |
| `docker scout sbom` | "Generate or display SBOM of an image" | 동일 | 미확인 | 2026-07-25 |
| **Docker Scout 번들 여부** | "**comes pre-installed with Docker Desktop**" / Docker Engine 단독은 별도 설치 | https://docs.docker.com/scout/install/ | 미확인 | 2026-07-25 |
| **Docker Desktop K8s 프로비저너** | **kubeadm(단일 노드) / kind(멀티 노드) 선택제** | https://docs.docker.com/desktop/features/kubernetes/ | 미확인 | 2026-07-25 |
| ↳ 프로비저닝 속도 | kubeadm ~1 min / kind ~30 seconds | 동일 | 미확인 | 2026-07-25 |
| ↳ **kind의 Docker image store 호환** | **No** (containerd image store는 Yes) | 동일 | 미확인 | 2026-07-25 |
| ↳ 버전 선택 | kubeadm 불가(Docker Desktop이 정함) / kind 가능 | 동일 | 미확인 | 2026-07-25 |
| containerd 스토어 기본 적용 (A) | "Docker Desktop and **Docker Engine 29.0+** use the containerd image store by default, which supports multi-platform images out of the box" ⛔ **의역 금지** | https://docs.docker.com/build/building/multi-platform/ | 미확인 | 2026-07-25 |
| containerd 스토어 기본 적용 조건 (B) | "default storage backend for Docker Engine 29.0 and later on **fresh installations**" | https://docs.docker.com/engine/storage/containerd/ | 미확인 | 2026-07-25 |
| 업그레이드 설치의 스토어 | "your daemon continues using the **legacy graph drivers (overlay2)** until you enable the containerd image store" | 동일 | 미확인 | 2026-07-25 |
| classic 드라이버의 멀티플랫폼 제약 | "With **classic storage drivers**, you need external builders for multi-platform images" | 동일 | 미확인 | 2026-07-25 |
| ⛔ `--load` 멀티플랫폼 제약의 **진짜 조건** | (A)(B) 충돌은 **모순이 아니라 스토어 세대 차이.** "멀티플랫폼은 `--load` 못 한다"를 **절대 규칙으로 쓰면 ❌** | 위 3개 소스 교차 | — | 2026-07-25 |
| `--load` / `--push` 정의 | "Shorthand for `--output=type=docker`" / "`...=type=registry`" | https://docs.docker.com/reference/cli/docker/buildx/build/ | 미확인 | 2026-07-25 |
| `--platform` 복수 값 조건 | **`docker-container` 드라이버**에서 콤마 구분 복수 지정 → 매니페스트 리스트 생성 | 동일 | 미확인 | 2026-07-25 |
| **QEMU 에뮬레이션 성능 (공식)** | "can be **much slower** than native builds, especially for **compute-heavy tasks like compilation**" | https://docs.docker.com/build/building/multi-platform/ | 미확인 | 2026-07-25 |
| `docker buildx imagetools inspect` | "Show details of an image in the registry". `--format`(기본 `{{.Manifest}}`) / `--raw` | https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/ | 미확인 | 2026-07-25 |
| 국내 5대 기술블로그 멀티아키/Apple Silicon 글 | **0건 (확인 범위 내)** ⛔ 부재 단정 금지 | 도메인 한정 검색 3회 (§8-7) | 해당 없음 | 2026-07-25 |
| ↳ 근접 자료 | "Docker Bake 食譜公開" — techblog.lycorp.co.jp (**번체 중국어**, 2차 소스) | https://techblog.lycorp.co.jp/zh-hant/docker-bake | **미확인** | 2026-07-25 |
| 내 Docker의 이미지 스토어 **확인 명령** | **미확인 — (사실 확인 필요)** | — | — | 2026-07-25 |
| BellSoft Liberica 태그 라인업 | **미확인** (bell-sw.com 미열람) | — | — | 2026-07-25 |
