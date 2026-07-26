# 커뮤니티 리서치: 맥 컨테이너 실무자의 고통 (tech-book)
**검색 시점:** 2026-07-25 / **genre:** tech-book / **슬러그:** mac-docker-container

---

## 📋 수집 방법과 신뢰도 규칙 (저술가·fact-checker 필독)

**수집 방법**
- **GitHub 이슈:** `gh issue view` (GitHub REST API)로 직접 조회. 본문·댓글·상태(`OPEN`/`CLOSED`)·ISO 타임스탬프를 API가 반환한 값 그대로 기록. → **인용문은 원문 그대로다.**
- **Hacker News:** Algolia HN API(`hn.algolia.com/api/v1/items/{id}`)로 댓글 트리 전체를 받아 조회. → **인용문은 원문 그대로다.** (HTML 엔티티 `&#x27;` 등은 `'`로 복원)
- **한국 커뮤니티(velog·OKKY·GeekNews):** WebFetch로 조회. **WebFetch는 소형 모델이 페이지를 요약해 돌려주는 도구**라 반환된 한국어 문장이 페이지 원문인지 요약문인지 구분이 어렵다. → **이 문서의 한국어 출처 인용은 전부 `(원문 대조 필요)` 라벨을 달았다. 책에 그대로 따옴표로 옮기기 전에 URL을 다시 열어 원문을 확인하라.**

**신뢰도 등급 표기**
| 표기 | 의미 |
|------|------|
| 🟢 메인테이너 | 프로젝트 메인테이너/커미터 발언 (`wilkinsona`·`philwebb`·`snicoll` = Spring Boot, `dmikusa` = Paketo, `kiview` = Testcontainers, `abiosoft` = Colima, `jandubois` = Rancher Desktop, `dgageot`·`thaJeztah`·`ctalledo` = Docker). 상대적으로 권위 있으나 여전히 1차 문서 대조 필요 |
| 🟡 다수 재현 | 서로 다른 사용자 3명 이상이 같은 증상을 독립적으로 보고 |
| 🔴 단일 익명 | 한 사람의 개인 환경 보고. 일반화 금지 |

**절대 규칙**
- 커뮤니티에 나온 **버전 번호·라이선스 조건·성능 수치는 그 자체로 근거가 아니다.** 전부 "그 사용자의 환경에서 그 시점에 그렇게 보였다"일 뿐이다. 책에서 단정하려면 릴리스 노트·공식 문서로 대조하라. `(1차 소스 확인 필요)` 라벨을 참고할 것.
- **시점이 전부다.** 2022년 M1 전환기 고통담과 2026년 현재는 다르다. 모든 항목에 게시 시점을 붙였다. 오래된 글을 인용할 때는 반드시 "당시 기준"임을 본문에 쓸 것.

---

## ⭐ 챕터 오프닝 후보 일화 (최우선 산출물)

> ⚠️ **"연결되는 사용자 요구" 번호에 대한 고지:** 브리프는 "1/2/3/4 중 어디"를 적으라고 했으나 **번호의 정의는 주지 않았다.** 아래 뜻으로 임의 부여했다 — **1**(컨테이너 원리 이해), **2**(실무 판단 기준), **3**(맥 Apple Silicon 환경에서의 실전), **4**(운영/배포 감각). **오케스트레이터는 정전(canonical) 요구 목록으로 재매핑하라.** 정의가 다르면 11개 일화 전부 다시 붙여야 한다.

### 일화 1: "busybox조차 안 돌아간다" — M4 맥에서 amd64 에뮬레이션 자체가 죽은 사건 ⭐⭐⭐
- **상황:** 사용자 `RitikaKumari`가 Apple Silicon M4 맥의 dev container 환경에서 amd64로 빌드된 서비스 이미지를 실행. Docker Desktop 4.59.0 / client 29.2.0 / `Context: desktop-linux` / `OS/Arch: darwin/arm64`. (2026-02-05 등록)
- **증상 (본문 원문):**
  > "We are encountering the following error while running our service in Docker: `exec /entrypoint.sh: exec format error`
  > This occurs on a machine using Apple Silicon (M4). The Docker image is built for the amd64 architecture, and it appears that emulation via platform=linux/amd64 is not working as expected."
- **진단 과정이 이 일화의 핵심이다.** Docker 모더레이터 `thaJeztah`가 최소 재현을 요구했다 (2026-02-06):
  > "Does this reproduce with all images? e.g. does running a amd64 busybox image work?"

  그리고 사용자가 돌려준 결과 (2026-02-06):
  > ```
  > docker run -it --rm --platform=linux/amd64 busybox
  > Unable to find image 'busybox:latest' locally
  > latest: Pulling from library/busybox
  > 61dfb50712f5: Pull complete
  > Digest: sha256:b3255e7dfbcd10cb367af0d409747d511aeb66dfac98cf30e97e87e4207dd76f
  > Status: Downloaded newer image for busybox:latest
  > exec /bin/sh: exec format error
  > ```

  **세상에서 가장 단순한 이미지인 busybox의 `/bin/sh`조차 실행되지 않았다.** 여기서 문제의 범위가 "내 이미지"에서 "이 맥의 에뮬레이션 계층"으로 확 좁혀진다. 챕터 오프닝으로서, "이슈를 좁히는 방법" 자체를 가르치는 최고의 소재다.
- **메인테이너의 진단 명령** (`ctalledo`, 2026-04-29) 🟢:
  > "the `exec format error` on even a minimal image like `busybox` suggests the x86_64 emulation layer isn't set up in the VM, rather than an issue with your specific image.
  > Could you check which binfmt_misc entries are registered? Run this on your machine:
  > ```bash
  > docker run --rm --privileged --pid=host alpine \
  >     nsenter -t 1 -m -u -i -n sh -c 'ls /proc/sys/fs/binfmt_misc/'
  > ```
  > You should see `x86_64` in the output (and `rosetta`/`rosetta-wrapper` if you have Rosetta enabled). If those entries are missing, the emulation handlers didn't register at VM boot, which would explain the error.
  > ...Rosetta emulation requires Apple Virtualization, but amd64 emulation via QEMU should work regardless."
- **결말:** ⚠️ **해결되지 않았다.** 이슈는 2026-04-30에 `ctalledo`가 "Unable to repro, closing"으로 닫았다. **binfmt_misc 미등록은 메인테이너의 가설이지 확정된 원인이 아니다.** `(확인 필요 — "Docker Desktop의 binfmt 버그"로 단정하지 말 것)`
- **곁가지 일화 (그 자체로 강력):** 다른 사용자 `IJMacD`가 2026-02-25에 남긴 우회 후기 —
  > "I was experiencing this issue on v4.62.0 for MacOS. I tried to change the Virtual Machine Manager to HyperKit to see if that fixed the issue. Unfortunately switching caused Docker to be unable to start. My only option was to do "Reset to Factory defaults". After factory reset I was able to run the binary I wanted to without any exec format errors.
  > (note: I did loose all my containers, images, and volumes)"

  → 원인을 모른 채 VM 매니저를 바꿔봤다가 Docker가 아예 안 뜨게 되고, 공장 초기화로 컨테이너·이미지·볼륨을 전부 날린 이야기. **"블랙박스를 이해하지 못하면 결국 초기화 버튼을 누르게 된다"**는 이 책의 존재 이유 자체다.
- **연결되는 사용자 요구:** 1(원리 이해), 2(실무 판단 기준)
- **신뢰도:** 🔴 단일 익명(원 보고자) + 🔴 단일 익명(IJMacD) / 메인테이너 진단은 🟢이나 **미해결**
- **출처:** https://github.com/docker/for-mac/issues/7849 — 2026-02-05 등록, 2026-04-30 CLOSED(재현 불가)

---

### 일화 2: "로컬에선 잘 돌던 이미지가 클라우드에서 즉시 죽었다" — bootBuildImage의 조용한 배신 ⭐⭐⭐
- **상황:** 사용자 `maradanasai`가 M1 맥에서 Spring Boot 3.3 + CDS 테스트용 이미지를 `bootBuildImage`(Paketo buildpack)로 생성. (2024-06-21 등록)
- **증상 (본문 원문):**
  > "In mac M1, generated an image for testing SB 3.3 + CDS support using packeto buildpack which is part of bootBuildImage stage. This generated image is given following warning in mac M1 but able to run the app. But if I run the same image on cloud VM which is of type ARM64, it is giving following error and immediately existed with error `exec /cnb/process/web: exec format error`."

  로컬에서 뜬 경고 (원문):
  > `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested`
- **여기가 압권이다.** arm64 맥에서 Paketo가 만들어낸 이미지가 **amd64**였다. 즉 "arm64 맥이니까 arm64 이미지가 나오겠지"라는 직관이 틀렸다. 게다가 로컬에서는 **경고만 뜨고 앱이 돌아갔다** — Rosetta/QEMU가 조용히 받아줬기 때문이다. 정작 죽은 곳은 **arm64 클라우드 VM**이었다. 로컬 성공이 배포 성공을 보장하지 않는다는 걸 이보다 잘 보여주는 사례가 없다.
- **결말 1 — 메인테이너 답변** (`dmikusa`, Paketo, 2024-06-21) 🟢:
  > "We do have ARM64 support. It is new and not totally complete across all buildpacks at this point in time. You're using Java buildpacks and those are all updated, so you should be OK.
  > The trick at this point is that you need to use a specific builder. Not all of the Paketo builders support ARM64.
  > The builder you want to use is `paketobuildpacks/builder-jammy-buildpackless-tiny`."
  `(1차 소스 확인 필요 — 2024-06 시점 발언이다. 2026-07 현재 빌더 라인업·arm64 지원 범위는 Paketo 공식 문서로 재확인할 것)`
- **결말 2 — 고친 줄 알았는데 캐시가 발목을 잡았다.** 빌더를 바꾼 뒤 사용자가 받은 새 에러:
  > `ERROR: failed to launch: exec.d: failed to execute exec.d file at path '/layers/paketo-buildpacks_ca-certificates/helper/exec.d/ca-certificates-helper': fork/exec /layers/paketo-buildpacks_ca-certificates/helper/exec.d/ca-certificates-helper: exec format error`

  `dmikusa`의 진단 🟢:
  > "First thing, you've got some layers that were cached. Usually, caching is good and makes things faster. But in this case, it's not updating those cached layers with ARM64 binaries. I'll open a bug for that, cause it should consider the architecture in that caching decision, but for now, just delete your existing app images and the build cache."

  → **아키텍처를 고려하지 않는 빌드 캐시.** amd64 바이너리가 든 레이어가 arm64 빌드에 그대로 섞여 들어간다. 이건 "설정을 바꿨는데도 안 고쳐지는" 최악의 디버깅 함정이다.
- **연결되는 사용자 요구:** 1, 2, 3(맥에서의 실전)
- **신뢰도:** 🔴 단일 익명 보고 + 🟢 메인테이너 진단·처방
- **출처:** https://github.com/paketo-buildpacks/spring-boot/issues/491 — 2024-06-21 등록, CLOSED

---

### 일화 3: "밤새 돌렸는데 아직도 빌드 중" — Rosetta 켜고 33,656초 ⭐⭐⭐
- **상황:** M2 Max 맥북 프로 사용자 `a6z6`가 Ubuntu 서버용 Next.js 앱 이미지를 amd64로 빌드. Docker Desktop 설정에서 "Use Rosetta for x86/amd64 emulation on Apple Silicon"을 **켠** 상태. (2023-11-12 등록)
- **증상 (본문 원문):**
  > "If check `✅ Use Rosetta for x86/amd64 emulation on Apple Silicon`, then run `docker buildx build --platform linux/amd64 -t my_docker_repo/test_image:latest .`
  > After a whole night, the build was still running after 30k seconds:
  > ```
  > [+] Building 33656.6s (15/22)                    docker:desktop-linux
  >  => [deps 5/5] RUN yarn install                                463.3s
  > ...
  >  => [builder 5/5] RUN yarn build                            33186.8s
  > ```"

  **33,656초 = 약 9시간 21분.** 그중 `yarn build` 한 스텝이 33,186초를 먹었다. 밤새 돌려놓고 아침에 와서 봤더니 아직도 안 끝나 있었다는 이야기.
- **다른 사용자들의 같은 증상 (🟡 다수 재현):**
  - `alnaranjo` (2023-11-19): "I had to revert to 4.24.2 to be able to work. Using 4.25.x would cause docker build to hang indefinitely even when disabling 'use rosetta'. My app is a simple node/next app. **Building arm images is a breeze, though.**"
  - `iaurg` (2023-11-20, M1 Air): "Sometimes, the computer just crashes because resources are completely used by Docker, forcing me to reset the OS."
  - `AlexandreRoba` (2023-12-01): "Same here downgraded to 4.24.2 and unchecked `Use Roseta..` in order to build a very simple next app on an apple M3 Max with 64GB in more than 5 minutes."
  - `oming` (2024-06-24, M3 Pro): "I have same issue with docker 4.31.0 (153195) ... now building with uncheck `❌ Use Rosetta for x86/amd64 emulation on Apple Silicon`"
- **결말:** 메인테이너 `dgageot`가 2023-12-06에 4.26.0을 제안하고 한 사용자가 해결됐다고 하자 이슈를 닫았다. 그러나 그 뒤로도 4.30.0·4.31.0에서 같은 보고가 이어졌고, `jinmel`이 2024-06-29에 남긴 한마디:
  > "why is this closed? I think the issue persists for latest macbook users"

  **2026-07-25 조회 시점 이슈 상태는 `OPEN`이다.**
- **교훈:** Rosetta 토글은 "켜면 빨라진다"는 단순한 스위치가 아니다. 워크로드에 따라 켜면 느려지고, Docker Desktop 버전에 따라 결과가 뒤집힌다. **"Rosetta 켜니 빨라졌다"고 책에 쓰면 안 된다.**
- **연결되는 사용자 요구:** 1, 2, 3
- **신뢰도:** 🟡 다수 재현 (M1/M2 Max/M3 Max/M3 Pro, 2023-11 ~ 2024-06)
- **출처:** https://github.com/docker/for-mac/issues/7075 — 2023-11-12 등록, 조회 시점 OPEN

---

### 일화 4: "JVM이 세그폴트로 죽는다 — Docker Desktop을 업데이트했더니" ⭐⭐⭐ (자바 독자 정조준)
- **상황:** 사용자 `ThomasHurek`. M1 맥. Docker Desktop을 4.26.1 → 4.27.1로 업데이트한 직후. (2024-02-05 등록)
- **증상 (본문 원문):**
  > "Various docker containers built on arm64 and work fine with docker desktop 4.26.1 and earlier now fail with 4.27.1 with the following error when the Java JVM tries to start:
  > `qemu: uncaught target signal 11 (Segmentation fault) - core dumped`
  > Rolling back to 4.26.1 solves the problem."

  실행 명령에 `--platform=linux/amd64`가 붙어 있다. 즉 **amd64 이미지를 QEMU 에뮬레이션으로 돌리다 JVM 기동 중 세그폴트가 났다.**
- **Docker 엔지니어의 즉답** (`dgageot`, 2024-02-05, 사고 40분 뒤) 🟢:
  > "Thank @ThomasHurek, sorry for breaking your workflow. I think I know where it comes from. I'll investigate some more tomorrow."
- **🟡 다수 재현:** `bradleygore`(postgis 이미지), `yilinjuang`(macOS Ventura 13.6.4), `jan-osch`(M1 Max, macOS 13.5.2, ubuntu:focal + Node 18), `zross`(M1, macOS Monterey 12.7), `jmlapre`(M1) — 모두 같은 `signal 11`.
- **⭐ 진짜 반전은 여기다.** 해결책이 Docker 버전이 아니라 **macOS 버전**이었다.
  - `bradleygore` (2024-02-06): "After upgrading OS to Sonoma this error went away 🥳"
  - `jan-osch` (2024-02-07): "Update: after updating to macOS `14.3` the issue does not occur anymore"
  - 그런데 원 보고자 `ThomasHurek` (2024-02-07): **"Unfortunately macOS 14.x is not rolled out in our company yet so stuck with 12.x or 13.x."**

  → **컨테이너의 격리는 호스트 OS까지 격리해주지 않는다.** "컨테이너 쓰면 환경이 똑같아진다"는 믿음이 깨지는 지점이고, 회사 IT 정책 때문에 macOS를 못 올려서 발이 묶이는 현실적 제약까지 붙는다. 챕터 오프닝으로 정말 강력하다.
- **연결되는 사용자 요구:** 1(격리의 경계가 어디까지인가), 2
- **신뢰도:** 🟡 다수 재현 + 🟢 Docker 엔지니어 확인. **2026-07-25 조회 시점 이슈 상태 `OPEN`**
- **출처:** https://github.com/docker/for-mac/issues/7172 — 2024-02-05 등록, OPEN

---

### 일화 5: "로컬 Colima 클러스터인 줄 알고 운영 배포를 지웠다" ⭐⭐⭐ (env_probe §5와 정확히 짝)
- **상황:** HN 사용자 `millerm`. Kubesafe(잘못된 클러스터에 명령 날리는 걸 막아주는 도구) 소개 스레드의 댓글. (2024-09-21)
- **증상·원문 인용:**
  > "Hah! I accidentally deleted a production deployment the other day, because I thought it was mucking with my local Colima Kubernetes's cluster. I forgot that I had my context set to one of my AWS clusters. I had been meaning to write a command to wrap helm and kubectrl to prompt me with info before committing, so I will have to take a peek at this."
- **⭐ 실측과의 짝:** `env_probe.md` §5가 정확히 이 상황이다 — 이 책을 쓴 맥에는 `docker-desktop`·`minikube` 로컬 클러스터가 둘 다 있는데, **활성 컨텍스트(`*`)는 원격 EKS(`ap-northeast-2`)** 였다. "로컬 실습하려고 `kubectl apply` 쳤는데 운영 클러스터로 나간다"는 시나리오가 **가설이 아니라 실측 + 실제 사고담**으로 동시에 확보됐다. 이 조합이 이 책 전체에서 가장 강한 오프닝 재료 중 하나다.
- **같은 스레드의 다른 목소리들 (🟡 다수 재현 — "다들 한 번씩 당했다"):**
  - `ed_mercer` (2024-09-21): "I got burned by this recently and came to the conclusion that **the concept of a current context is evil**. Now I always specify —-context when running kubectl commands."
  - `lukaslalinsky` (2024-09-21): "I also got burned by this, pretty badly, and ever since it happened, I don't even have a default kubeconfig, have to specify it for every single kubectl run."
  - `evnix` (2024-09-21): "Have been burnt by this, I have to deal with close to 8 clusters and it is very easy to make a mistake."
  - `Telemaco019`(도구 저자) (2024-09-21): "Got burned too, we've all been there I guess :)"
  - `cduzz` (2024-09-21), 뼈아픈 한마디: "In the early 1990s I ran a math department's 4 servers and 50 workstations and (with a few exceptions) only ever did administrative actions through scripts. ... Have we regressed to the point where we've turned big clusters of systems back into 'oops I ran a command as superuser in the wrong directory'?"
- **연결되는 사용자 요구:** 2(실무 판단 기준), 4(운영 감각)
- **신뢰도:** 🟡 다수 재현 (익명 개인 경험이지만 최소 5명이 독립적으로 "당했다"고 진술)
- **출처:** https://news.ycombinator.com/item?id=41578274 — 2024-09-18 게시(스레드), 댓글 2024-09-21

---

### 일화 6: "빌드가 몇 시간째 그 자리에 멈춰 있다" — M1 Max + GraalVM 네이티브 이미지 ⭐⭐
- **상황:** `JakobStadlhuber`. M1 Max. IntelliJ로 갓 만든 **완전히 새 프로젝트**(Spring Boot 3.0.0-RC2, Java 17, Kotlin)에서 `gradle bootBuildImage` 실행. (2022-11-13 등록)
- **증상 (본문 원문):**
  > ```
  > [creator]     GraalVM Native Image: Generating '/layers/paketo-buildpacks_native-image/native-image/...' (static executable)...
  > [creator]     [1/7] Initializing...                     (39.4s @ 0.19GB)
  > [creator]      Version info: 'GraalVM 22.3.0 Java 17 CE'
  > [creator]      C compiler: gcc (linux, x86_64, 7.5.0)
  > ```
  > "It is there for hours."

  로그 안의 `C compiler: gcc (linux, **x86_64**, 7.5.0)` — 이 한 줄이 범인이다. arm64 맥인데 컴파일러가 x86_64다.
- **정답에 도달하기까지 두 단계를 거친다 (진단의 교육적 가치):**
  - **① 재현 조건 좁히기 요청** — `snicoll`(Spring Boot 팀) 🟢 (2022-11-14):
    > "@JakobStadlhuber thanks for the report but I am not sure what you expect us to do with a screenshot and a build script. Can you please try outside of IntelliJ IDEA for a start? If you can reproduce, getting the threads dump of the process could help us figure out where that's coming from."

    → 진단이 아니라 **IDE 변수를 제거하라는 절차 요구**다. (오진 아님)
  - **② 실제 오진** — `wilkinsona`(Spring Boot 팀) 🟢 (2022-11-14):
    > "My guess would be that Docker doesn't have enough memory and the native compilation is suffering from GC thrash. How much memory have you allocated to Docker, @JakobStadlhuber?"

    → **메모리 부족으로 짚었으나 실제 원인은 에뮬레이션이었다.** 메인테이너도 처음엔 맥의 메모리 설정을 의심했다는 사실 자체가, 이 증상이 얼마나 헷갈리는지를 보여준다.
- **정답** (`dr-eme`, 2022-11-14):
  > "The issue is with the paketo builder, which uses an AMD64 image which runs with QEMU on ARM systems like Apple Silicon, and **performance is very poor**.
  > While there is no official support for ARM64 just yet, there is a preliminary workaround by using the following experimental builder:
  > ```
  > bootBuildImage {
  >   if (org.gradle.nativeplatform.platform.internal.DefaultNativePlatform.getCurrentArchitecture().isArm()) {
  >     builder = 'dashaun/java-native-builder-arm64'
  >   }
  > }
  > ```"
- **⭐ 감정이 실린 한 줄 — 챕터 오프닝용 최고 인용문:**
  > "Thank you @dr-eme thats it. I am just wondering why this is not mentioned anywhere, especially because how many devs using systems from Apple where ARM is de facto the standard for 2 years." — `JakobStadlhuber`, 2022-11-14

  "왜 이게 어디에도 안 적혀 있는 거죠?" — **이 책이 왜 필요한지를 독자가 대신 말해준 문장이다.**
- **결말:** `wilkinsona` 🟢 — "Given that this is a limitation that Spring Boot cannot control, we should probably mention it on the wiki" → 2022-11-17 "The wiki has been updated." (Known-GraalVM-Native-Image-Limitations 위키)
- **시점 주의:** **2022-11 기준이다.** 그 뒤 Paketo arm64 지원이 진행됐다(→ 아래 §2 타임라인). 이 일화는 반드시 "당시 기준"으로 써야 한다.
- **연결되는 사용자 요구:** 1, 2
- **신뢰도:** 🔴 단일 익명 보고 + 🟢 메인테이너 위키 반영으로 사실 확정
- **출처:** https://github.com/spring-projects/spring-boot/issues/33119 — 2022-11-13 등록, CLOSED

---

### 일화 7: "다른 분 노트북으로 빌드했더니 그냥 됐다" — 한국어 삽질기 ⭐⭐⭐
> ✅ **이 일화는 축자 인용(verbatim)을 재수집해 확보했다.** WebFetch에 "번역·요약하지 말고 한국어 본문을 한 글자도 바꾸지 말고 그대로 출력하라"고 요청해 받은 결과이며, 저자의 오탈자(`문게였다`, `다르게 때문에`)와 이모지 소제목이 그대로 남아 있는 것이 원문 보존의 방증이다. **이 문서에서 유일하게 그대로 따옴표에 넣을 수 있는 한국어 인용이다.**

- **상황:** velog 사용자 `___pepper`. `build.sh`로 도커 이미지를 만들어 레지스트리에 올린 뒤 배포. **이미지 생성도 성공, push도 성공. 그런데 배포만 계속 실패.** (2022-01-11 게시)
- **증상 (원문):**
  > "배포할 파일은 작성된 build.sh를 이용해서 도커 이미지를 생성하고 registry에 올린 뒤 배포를 진행하려고 했는데, 이미지 생성과 push는 성공하나 배포에서 계속 문제가 발생했다.
  > k9s에서 배포할 이미지로 값을 수정하면 pod가 만들어져야하는데, **registry에 이미지가 존재함에도 실행이 불가하다는 에러가 계속 발생했다.**"

  → 에러가 "아키텍처가 안 맞습니다"라고 친절히 말해주지 않았다. **"이미지는 분명히 있는데 실행이 안 된다"**는 형태로 나타났다.
- **⭐ 오진 구간이 이 글의 백미다 (원문):**
  > "찾아보니 **entrypoint.sh 파일의 실행 권한이 없을 경우에 발생할 수 있는 문제**라고 해서 일단 `chmod +x entrypoint.sh` 를 통해 권한을 바꿔주고 다시 이미지를 생성해봤다.
  > **사실 실행 권한을 확인해보니 이미 권한이 있기는 했다.**
  > 다시 이미지를 빌드해서 시도했으나, 또다시 실패. 에러 내용은 이전과 동일했다."

  → **검색해서 나온 첫 번째 답을 이미 아닌 걸 알면서도 해봤다.** 원리를 모를 때 우리가 실제로 하는 행동이 이거다. 토비 문체 챕터 오프닝으로 이보다 좋은 재료가 드물다.
- **⭐ 결정적 단서 (원문):**
  > "이상하다 싶어서 **다른 분의 노트북으로 이미지를 빌드해서 배포를 시도했더니 별 문제 없이 배포가 마무리되는 현상**을 확인할 수 있었다.
  > 차이점이라고는 **코어의 차이(M1 or Intel)** 였는데, **설마 그게 문제일까하는 생각이 들기는 했다.**"

  → "설마 그게 문제일까" — **범인을 눈앞에 두고도 못 믿는 순간.** 컨테이너가 "어디서나 똑같이 돈다"고 믿고 있으면 CPU 아키텍처를 용의선상에 올릴 수가 없다.
- **원인 (원문, 오탈자 포함):**
  > "결론적으로 코어가 다르게 때문에 발생한 문게였다.
  > M1 mac에서는 docker 이미지 빌드를 할 때 **"arm"** 으로 빌드를 하는 반면 intel은 **"amd"** 로 빌드를 한다.
  > 이렇게 빌드된 **"arm"** 이미지를 aws에서 돌리려고 한 것인데, **aws에서는 arm으로 빌드된 이미지를 실행할 수 없어서** 계속해서 에러가 발생하게 된 것이었다."
  `(주의 — "aws에서는 arm으로 빌드된 이미지를 실행할 수 없어서"는 2022-01 당시 그 팀의 클러스터 기준이다. AWS 전반에 대한 사실이 아니다(Graviton 등 arm64 인스턴스 존재). 책에 그대로 옮기면 오보가 된다. 인용은 하되 반드시 주석을 달 것.)`
- **해결:** 빌드 스크립트에 아키텍처 분기 추가.
  > ```bash
  > if [[ $(arch) == 'arm64' ]]; then
  >   DOCKER_BUILD_OPTS="--platform=linux/amd64"
  > fi
  > ```
  *(코드 블록은 첫 수집분에서 확보. 축자 재수집분에서는 코드 블록이 누락된 채 "를 추가해서"로만 나왔다 — 코드 인용 시 원 페이지 재확인 권장)*
- **⭐ 마무리 문장 (원문) — 감정이 그대로 살아 있다:**
  > "정말 뭐가 문제인지 싶었는데,,,,,
  > 문제 해결해 주신 리드님께 무한 감사,,,,😭"

  → 결국 **혼자 못 풀고 리드가 알려줬다.** "아는 사람은 3초, 모르는 사람은 며칠"인 지식의 전형이고, 이 책이 메우려는 격차가 바로 이것이다.
- **연결되는 사용자 요구:** 1(원리), 2(판단 기준), 4(배포 감각). **한국 독자 정조준.**
- **신뢰도:** 🔴 단일 익명 개인 경험 / **인용문 자체는 축자 확보 ✅**
- **출처:** https://velog.io/@___pepper/Docker-M1-mac-이미지-배포-오류 — 2022-01-11

---

### 일화 8: "Testcontainers가 죽은 소켓을 쳐다보고 있다" — Docker Desktop 탈출의 청구서 ⭐⭐ (자바 독자 정조준)
- **상황:** `codingdiscer`. **조직 차원의 결정으로** Docker Desktop을 버리고 Colima로 이주. (2022-02-08 등록)
- **본문 첫 문장이 시대를 압축한다:**
  > "In the move away from paid Docker Desktop and towards alternatives, my organization has selected Colima as our official Docker engine for desktop development. After installing Colima via Homebrew on my mac, I'm able to run all my favorite docker commands as-is."

  → `docker` 명령은 다 잘 됐다. **그래서 이주가 끝난 줄 알았다.**
- **증상:** 그런데 Testcontainers(Spring Boot 통합 테스트의 사실상 표준)가 깨졌다. 사용자가 붙인 진단:
  > ```
  > docker context list
  > NAME        TYPE      DESCRIPTION                               DOCKER ENDPOINT
  > colima *    moby      colima                                    unix:///Users/ddowma/.colima/docker.sock
  > default     moby      Current DOCKER_HOST based configuration   unix:///var/run/docker.sock
  > ```
  > "As shown in the output above, there is still a `default` entry, and it points to `unix:///var/run/docker.sock`. However, I can see that no such file exists at that location"

  Ryuk(Testcontainers의 컨테이너 청소 사이드카)이 남긴 로그:
  > `panic: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

  → **`docker` CLI는 context를 읽고 Colima로 잘 갔는데, Testcontainers가 띄운 Ryuk 컨테이너는 컨테이너 안에서 `/var/run/docker.sock`을 찾고 있었다.** "누가 어느 소켓을 어느 관점에서 보느냐"가 전부 다른 문제다. `env_probe.md` §4(클라이언트≠데몬)와 같은 뿌리다.
- **결말:** `DOCKER_HOST`만 바꿔선 안 됐다. 정답을 찾은 사람 `benhexagon` (2022-02-11):
  > "The problem is most likely that **Ryuk needs the docker socket endpoint from inside the Colima VM**. Setting the environment variable `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` to `/var/run/docker.sock` and the `DOCKER_HOST` variable to `unix:///${HOME}/.colima/docker.sock` allowed me to run testcontainers with Colima."

  → 두 변수가 **서로 다른 값**을 가리켜야 한다. `DOCKER_HOST`는 호스트에서 본 경로, `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE`는 컨테이너 안에서 본 경로.
- **⛔ 반면교사 — 커뮤니티에서 도는 위험한 처방:** `rottenha`(2022-02-11)가 `TESTCONTAINERS_RYUK_DISABLED=true`를 추천했고, 이 설정은 지금도 여러 한국어 블로그에 복붙되어 돌아다닌다. 그러나 메인테이너 `kiview` 🟢가 곧바로 반박했다:
  > "This will mask the error, rather than fixing the root cause, since it will simply disable Ryuk, thereby leaving you without reliable resource cleanup."

  **"에러가 사라진 것"과 "고친 것"의 차이** — 이 책이 가르쳐야 할 핵심 태도이고, 커뮤니티 복붙 처방의 위험을 보여주는 실제 사례다.
- **연결되는 사용자 요구:** 2, 3
- **신뢰도:** 🟡 다수 재현(`codingdiscer`·`sanimalp`·`rottenha` 등) + 🟢 메인테이너 반박
- **출처:** https://github.com/testcontainers/testcontainers-java/issues/5034 — 2022-02-08 등록, CLOSED

---

### 일화 9: "소켓 지우고 심링크 걸기, 2전 2패" ⭐⭐
- **상황:** `james-s-w-clark`. 회사 맥에서 Colima를 시도 → Testcontainers 때문에 Docker Desktop 소켓을 지우고 Colima 소켓을 심링크해야 했다. 개인 맥에서 `act`(GitHub Actions 로컬 실행)를 시도 → 또 같은 문제. (2022-07-12 등록)
- **원문 인용:**
  > "So I'm 2 for 2 on needing to delete the old socket and symlink Colima's. It seems very common for tools to point to that socket file."
- **메인테이너의 반론** (`abiosoft`, Colima 저자, 2022-07-14) 🟢 — **양쪽 논거가 다 있는 좋은 논쟁 소재:**
  > "I can understand your frustration. While it may be your experience, **many tools are indeed catching up and utilising docker context instead.**
  > Another advantage of this approach is the ability to try out Colima without breaking your current workflow."

  → "심링크 안 거는 게 오히려 기존 워크플로를 안 깨뜨리는 설계"라는 반론. 소켓 하이재킹 vs. context 존중, 어느 쪽이 옳은지 자체가 논쟁이다.
- **1년 뒤에도 같은 요청** (`henrik242`, 2023-03-30):
  > "Would it be possible to get Colima to automatically symlink `/var/run/docker.sock` to `$HOME/.colima/default/docker.sock`? **Or at least warn if it points somewhere else? That would help some hard-to-debug scenarios I've helped colleagues resolve lately.**"
- **결말:** `abiosoft` 🟢 "it's on the roadmap. Something similar to `colima nerdctl install`, maybe `colima docker link-socket`." — **2026-07-25 조회 시점에도 이슈는 `OPEN`이다** (2022-07 등록 이후 4년째).
- **연결되는 사용자 요구:** 2, 3
- **신뢰도:** 🔴 단일 익명 + 🟢 메인테이너 응답
- **출처:** https://github.com/abiosoft/colima/issues/365 — 2022-07-12 등록, OPEN

---

### 일화 10: "런타임 두 개 깔았더니 명령이 통째로 실패한다" (env_probe §4와 짝) ⭐⭐
- **상황:** `giggio`. **Rancher Desktop과 Docker Desktop을 동시에 설치**해 쓰는 환경. (2024-11-01 등록)
- **원문 인용:**
  > "I'm running Rancher Desktop as well as Docker Desktop for Windows and when the latter starts it changes the docker context to `docker-linux` or `docker-windows`. When I close it, it stays set. Rancher Desktop seems to work with the default context. When I start Rancher Desktop it **does not** set the context, so **any command issued in a terminal will fail until the context is reset to `default` with `docker context use default`**."
- **⚠️ 중요한 단서 — 이 보고는 Windows다, 맥이 아니다.** `env_probe.md`의 맥 관측(클라이언트=Rancher Desktop `27.5.0-rd`, context=`desktop-linux`, 데몬=Docker Desktop `29.6.2`)과 **정확히 같은 사례는 이번 검색에서 찾지 못했다.** 다만 실패의 구조는 같다: **런타임 두 개가 `docker context`라는 하나의 전역 상태를 놓고 다투고, 아무도 그걸 사용자에게 알려주지 않는다.**
  → 책에서 쓸 때는 "커뮤니티에는 Windows 사례가 보고돼 있고, 이 책을 쓴 맥에서는 실측으로 클라이언트/데몬이 갈린 상태가 관측됐다"로 **두 근거를 분리해서** 쓸 것. 맥 사례로 둔갑시키지 말 것.
- **관련 이슈들(제목·상태·날짜만 확인, 본문 미열람):**
  - `rancher-desktop#3080` "Create docker context earlier" — 2022-10-03, OPEN
  - `rancher-desktop#3350` "Current context "rancher-desktop" is not found on the file system" — 2022-11-07, OPEN. (본문 열람함: macOS Monterey 12.1 / RD 1.6.1에서 `docker images` 실행 시 `Current context "rancher-desktop" is not found on the file system, please check your config file at /Users/.../.docker/config.json`) 🔴
  - `rancher-desktop#10443` "Linux binary directories in Windows `%PATH%` break Docker CLI in other WSL distros (credential helper conflict)" — 2026-06-11, OPEN. Windows/WSL 사례지만 **PATH 주입으로 인한 조용한 오염**이라는 실패 형태가 `~/.rd/bin` 관측과 같은 계열. `rfay`의 코멘트(2026-07-16): "this is a general mysterious problem that can create silent problems for any user."
- **연결되는 사용자 요구:** 1, 2
- **신뢰도:** 🔴 단일 익명. **플랫폼 불일치 있음(Windows)** — 반드시 명시할 것
- **출처:** https://github.com/rancher-sandbox/rancher-desktop/issues/7712 — 2024-11-01 등록, OPEN

---

### 일화 11: "디스크 120GB 남았는데 No space left on device" ⭐
- **상황:** `Stargator`. macOS 12에서 Rancher Desktop 사용 중 Kubernetes 기동 에러. (2023-04-14 등록)
- **원문 인용:**
  > "My HD has 120 GB free, so I don't understand the "No space left on device" nor the references to `nerdctl`."
- **진단 (메인테이너 `jandubois`) 🟢:**
  > "You may be out of space inside the VM. **The data volume has a default maximum size of 100GiB**, so if you created/pulled a lot of images, it may be full."
  > ```
  > $ rdctl shell df -h /mnt/data
  > ```
  `(1차 소스 확인 필요 — 100GiB 기본값은 2023-04 시점 메인테이너 발언. 현재 Rancher Desktop 1.17.x의 기본값은 공식 문서 확인)`
- **사용자가 실행한 결과:**
  > ```
  > Filesystem                Size      Used Available Use% Mounted on
  > /dev/disk/by-label/data-volume
  >                          97.9G     93.1G         0 100% /mnt/data
  > ```
- **핵심:** **맥 호스트 디스크와 VM 안 디스크는 다른 디스크다.** Finder가 "120GB 남음"이라고 말해도 컨테이너는 꽉 차서 죽는다. 맥의 컨테이너가 리눅스 VM 위에서 돈다는 사실이 이 순간에 처음으로 아프게 체감된다.
- **결말:** `rdctl factory-reset`. `jandubois` 🟢: "Yes, it will delete the VM and all data." → 일화 1의 IJMacD와 **같은 결말: 원인을 못 찾으면 초기화.**
- **연결되는 사용자 요구:** 1(VM 경계), 3
- **신뢰도:** 🔴 단일 익명 + 🟢 메인테이너 진단
- **출처:** https://github.com/rancher-sandbox/rancher-desktop/issues/4457 — 2023-04-14 등록, CLOSED

---

## 1. Apple Silicon 아키텍처 고통

### 1-1. 아키텍처 불일치가 드러나는 다섯 가지 얼굴 (🟡 반복 패턴)
근본은 "이 바이너리는 이 CPU의 것이 아니다"인데 **증상은 전혀 다르게 보인다.** 이게 진단이 어려운 이유다.

**(A) `exec format error` 계열 — 커널이 바이너리 헤더를 읽고 거부하는 경우**

| 얼굴 | 실제 메시지 | 출처 | 시점 |
|------|------------|------|------|
| ① 컨테이너가 즉시 죽음 | `exec /entrypoint.sh: exec format error` | docker/for-mac#7849 | 2026-02 |
| ② busybox `/bin/sh`조차 실패 | `exec /bin/sh: exec format error` | docker/for-mac#7849 댓글 | 2026-02 |
| ③ buildpack 런치 프로세스 실패 | `exec /cnb/process/web: exec format error` | paketo/spring-boot#491 | 2024-06 |
| ④ buildpack **헬퍼 스크립트만** 실패 (캐시 오염 — 나머지 레이어는 정상) | `fork/exec /layers/paketo-buildpacks_ca-certificates/helper/exec.d/ca-certificates-helper: exec format error` | paketo/spring-boot#491 | 2024-06 |

**(B) `exec format error`가 아닌 얼굴 — 에뮬레이션은 시작됐는데 도중에 죽는 경우**

| 얼굴 | 실제 메시지 | 출처 | 시점 |
|------|------------|------|------|
| ⑤ 에뮬레이터 위에서 JVM 기동 중 세그폴트 | `qemu: uncaught target signal 11 (Segmentation fault) - core dumped` | docker/for-mac#7172 | 2024-02 |

> ⚠️ **⑤는 `exec format error`가 아니다.** ①~④는 "실행 자체가 거부됨"이고, ⑤는 "QEMU가 amd64 바이너리를 받아서 돌리다가 중간에 죽음"이다. **원인도 진단 경로도 다르다.** 다만 실무자 입장에서는 둘 다 "amd64 이미지를 arm64 맥에서 돌리려다 터진 일"로 묶여 보인다. → 책에서는 **"exec format error가 세그폴트로 나타나기도 한다"고 쓰면 틀린다.** "에뮬레이션 실패는 `exec format error`가 아닌 형태로도 나타난다"로 쓸 것.
> **⑤가 특히 잔인한 이유:** 아키텍처 문제인데 에러 메시지에 아키텍처라는 단어가 한 번도 안 나온다.

### 1-2. 같은 경고 템플릿, 정반대 방향 — 그래서 배포 때 터진다 (🟡 반복 패턴)
Docker가 내는 경고는 하나의 템플릿이다:
> `WARNING: The requested image's platform ({이미지 플랫폼}) does not match the detected host platform ({호스트 플랫폼})`

그런데 확보한 두 사례는 **방향이 정반대다.** 이 구분이 이 책이 가르쳐야 할 핵심이다.

| 방향 | 이미지 | 호스트 | 어디서 터졌나 | 출처 |
|------|--------|--------|--------------|------|
| **amd64 이미지 → arm64 맥** | `linux/amd64` | `linux/arm64/v8` | 맥에서는 **경고만 뜨고 돌아감**(Rosetta/QEMU가 받아줌). 죽은 곳은 arm64 클라우드 VM | paketo-buildpacks/spring-boot#491, 2024-06-21 |
| **arm64 이미지 → amd64 서버** | `linux/arm64/v8` | `linux/amd64` | M1 맥에서 빌드 → EC2 배포 시점에 처음 발견 | velog @msung99, 2023-01-05 `(원문 대조 필요)` |

**공통 패턴:** 맥에서는 경고만 뜨고 돌아간다 → 개발자가 무시한다 → 배포 대상에서 처음으로 죽는다. **"로컬에서 잘 됐는데요"의 컨테이너판.**
**차이:** 첫 번째는 "arm64 맥인데 왜 amd64 이미지가 나왔지?"(빌드 도구가 결정), 두 번째는 "arm64 맥이니 arm64 이미지가 나왔다"(호스트가 결정). **원인이 다르므로 처방도 다르다.**

### 1-3. Rosetta 토글에 대한 실사용 의견은 갈린다 (→ §논쟁 표 참고)
- 켜면 느려졌다는 보고: docker/for-mac#7075 (33,656초 사례, 2023-11)
- 껐더니 5분 만에 빌드됐다: `AlexandreRoba`, M3 Max 64GB, 2023-12-01
- **arm64 네이티브 빌드는 아무 문제 없었다:** `alnaranjo`, 2023-11-19 — "Building arm images is a breeze, though."
  → **가장 확실한 처방은 "에뮬레이션을 안 하는 것"** 이라는 실무 결론.

### 1-4. 전환기(2022) vs 지금(2026) — 시점별 온도차
| 시점 | 커뮤니티 온도 | 근거 |
|------|-------------|------|
| 2022-01 | "M1은 arm, intel은 amd"라는 사실 자체가 발견 대상 | velog @___pepper, 2022-01-11 |
| 2022-11 | Paketo 빌더가 amd64뿐 → QEMU → "performance is very poor". 비공식 커뮤니티 빌더(`dashaun/*`)로 우회 | spring-boot#33119 |
| 2023-11 | Rosetta 토글이 도입됐으나 **켜면 더 느려지는** 회귀 다수 | docker/for-mac#7075 |
| 2024-02 | Docker Desktop 4.27.1 회귀로 QEMU 위 JVM 세그폴트. 해법이 macOS 14.3 업그레이드 | docker/for-mac#7172 |
| 2024-06 | Paketo arm64 지원 존재하되 "not totally complete across all buildpacks" (🟢 dmikusa) | paketo/spring-boot#491 |
| 2024-11 | Spring Boot 3.4.0에 `imagePlatform` 도입. 단 **한 번에 한 플랫폼만** | spring-boot#491 댓글 |
| 2025-08~11 | `imagePlatform` + containerd 이미지 스토어 조합 버그 → PR #47292로 수정, 3.5.8-SNAPSHOT에서 검증 | spring-boot#46665 |
| 2026-02 | 여전히 M4에서 amd64 에뮬레이션이 통째로 죽는 보고 (재현 불가로 종결) | docker/for-mac#7849 |

**결론:** 2022년보다 훨씬 나아졌지만 **"끝났다"고 쓰면 안 된다.** 2026년에도 살아 있는 보고가 있다.

---

## 2. Paketo buildpacks / bootBuildImage arm64 — 4년 타임라인

> ⚠️ **이 섹션은 개별 일화가 아니라 하나의 이야기로 써야 한다.** 4개 이슈가 2022→2026 시간 축 위에 정확히 놓인다. 흩어놓으면 가치가 절반으로 떨어진다.

### 확인된 이슈 원장 (번호·제목·상태·날짜 전부 이번 세션 조회값)

| # | 저장소 | 제목 | 등록일 | 상태(2026-07-25 조회) |
|---|--------|------|--------|------|
| 33119 | spring-projects/spring-boot | Document limitations of using buildpacks to build a native image on ARM64 devices | 2022-11-13 | CLOSED |
| 491 | paketo-buildpacks/spring-boot | Add support for building multi-arch docker images with paketo | 2024-06-21 | CLOSED |
| 46665 | spring-projects/spring-boot | New arm64 macbooks fail to bootBuildImage due to incorrect platform image | 2025-08-04 | CLOSED |
| 652 | paketo-buildpacks/base-builder | Apple Silicon (M1) support for all paketo-buildpacks Builder | 미확인 | 미확인 |
| 51 | paketo-buildpacks/stacks | Add support for arm64 | 미확인 | 미확인 |
| 1387 | paketo-buildpacks/java (Discussion) | Arm64 (beta) Support for Paketo Buildpacks | 미확인 | 미확인 |
| 1003 | buildpacks/pack | Apple Silicon Support | 미확인 | 미확인 |

> ⛔ **아래 4개(652 / 51 / 1387 / 1003)는 웹 검색 결과에 제목만 노출됐을 뿐 이번 세션에서 페이지를 열지 않았다.** 제목·번호 이상은 아무것도 쓰지 말 것. 인용·상태·날짜 금지.

### 2-1. 단계 ① 2022-11 — 빌더 자체가 amd64뿐이었다
- 증상: M1 Max에서 `bootBuildImage` + GraalVM 네이티브 이미지가 **몇 시간째 멈춤**. (일화 6)
- 원인: Paketo 빌더 이미지가 AMD64 → ARM에서 QEMU 위에서 돎 → "performance is very poor"
- 우회: 커뮤니티 개인이 만든 비공식 빌더 `dashaun/java-native-builder-arm64` / `dashaun/builder-arm:tiny`
- 공식 대응: Spring Boot 팀이 **고치는 대신 위키에 한계를 문서화**했다 (`wilkinsona` 🟢, 2022-11-17) — "this is a limitation that Spring Boot cannot control"
- **교훈:** 이 시절의 정답은 "Dockerfile을 직접 쓴다"였다.

### 2-2. 단계 ② 2024-06 — arm64 지원은 생겼는데 "빌더를 골라야" 한다
- `dmikusa` 🟢: "We do have ARM64 support. It is new and not totally complete across all buildpacks at this point in time."
- 처방: `paketobuildpacks/builder-jammy-buildpackless-tiny` + `buildpacks` 목록 직접 지정
  > "The other point to note is that this is a "buildpackless" builder, so there are no buildpacks installed on the builder by default. This is intentional, but it means you need to supply a list of buildpacks you want to use when you perform your build."
  → **"그냥 되던 것"이 "설정을 알아야 되는 것"으로 바뀌었다.** buildpack의 판매 포인트(설정 없이 이미지가 나온다)가 arm64에서 깨진 지점.
- 숨은 함정: **아키텍처를 고려하지 않는 빌드 캐시** → 빌더를 바꿔도 낫지 않음. 처방은 `docker rmi` + 캐시 볼륨 삭제 또는 이미지 이름 변경.

### 2-3. 단계 ③ 2024-11 — 멀티아키 태그를 원하면 손으로 manifest를 만들어야 한다
`heruan`(Spring Boot로 K8s Operator를 만드는 사용자)와 `dmikusa` 🟢의 대화:
- `heruan` (2024-11-21): buildx는 한 번에 되는데 buildpack은 안 된다며 —
  > "I'd like to switch from `docker buildx build --platform linux/amd64,linux/arm64 --push .` to `mvn spring-boot:build-image` but I cannot find a way to build images (ultimate goal native images) for multiple platform and push them as a single tagged manifest to the registry (as `buildx` does)."
- Spring Boot 3.4.0의 `imagePlatform` 도입 후에도 (`heruan`, 2024-11-21):
  > "there is a new `imagePlatform` attribute but **it seems like it works for one platform at a time.** I can build images for both platforms with different tags running `spring-boot:build-image` multiple times (once for each platform), push them individually, then create and tag a single multi platform manifest — but then I have three different tags in the registry while with `buildx` a single tag is pushed."
- `dmikusa` 🟢 확답 (2024-11-21):
  > "**Neither `pack build` nor `spring-boot:build-image` will build images for multiple architectures in one run.** That may be something that comes in the future, but it's not clear how that should work, especially when there is native code involved (emulation would be required).
  > For now, what you can do is build the two images independently and then use a command like `docker manifest` to make an index image from the two."

  `(1차 소스 확인 필요 — 2024-11 시점 발언. 2026-07 현재 Spring Boot 4.x / Paketo에서 바뀌었는지 릴리스 노트로 확인 필수. 이 책의 독자에게 가장 중요한 항목 중 하나다)`
- **한국어 실전 확인** (velog @cmsong111, 2025-03-09, 저자 김남주) `(원문 대조 필요)`:
  > "GitHub Actions에서 x86 환경에서 ARM64 이미지를 빌드하려고 하면 오류가 발생했습니다. 따라서 GitHub Actions의 Runner 자체를 ARM 환경으로 변경하여 이 문제를 해결하였습니다."

  그리고 저자의 총평:
  > "Dockerfile을 사용하지 않기 때문에 멀티플랫폼 지원을 위해 Docker Manifest를 수동으로 생성해야 하는 불편함"

  → **"Dockerfile 직접 쓰기로 갈아탄 사람들의 이유"가 이 한 문장에 다 있다.** buildpack이 Dockerfile을 없애준 대가로 멀티아키 제어권을 가져갔다.

### 2-4. 단계 ④ 2025-08~11 — `imagePlatform` + containerd 이미지 스토어의 함정
- **제목에 속지 말 것.** 이슈 제목은 "New arm64 macbooks fail to bootBuildImage"지만 메인테이너 `wilkinsona`가 명시적으로 정정했다 🟢 (2025-08-04):
  > "The title describes what sounds like a broad problem with `bootBuildImage` on Apple Silicon. However, reading the description, **it sounds like the problem only occurs when trying to build an `amd64` image on an arm64 host.** Can you please clarify?"

  → 책에 쓸 때 **"arm64 맥에서 bootBuildImage가 실패한다"고 쓰면 오보다.** 정확히는 "arm64 호스트에서 amd64 이미지를 만들려 할 때"다.
- 실제 에러 (메인테이너가 직접 재현한 원문):
  > `Image platform mismatch detected. The configured platform 'linux/amd64' is not supported by the image 'docker.io/paketobuildpacks/builder-noble-java-tiny:latest'. Requested platform 'linux/amd64' but got 'linux/arm64'`
- 원 보고자 `ofirm93`의 기술적 진단 (2025-08-04, M4 Pro / Spring Boot 3.5.4 / Gradle plugin 3.5.4):
  > "the plugin implements the docker calls (in DockerApi class) which are the equivalent of the following docker cli commands: `docker pull --platform <imagePlatform> <buildpack>` / `docker save <buildpack>`. **The problem is in the second command implementation, as it doesn't provide the requested platform.** In such case `dockerd` decides the platform is the host platform, which in my case is `arm64` which doesn't match the pulled image platform."
- **⭐ 비자명한 레버 — Docker Desktop의 "Use containerd for pulling and storing images" 토글** (`hojooo`, 2025-10-23, M1):
  > "If that option is turned on, I have confirmed the similar issue is reproduced on the m1 processor. **However, turning off that option won't reproduce the problem.**"

  → 같은 코드, 같은 맥, 같은 Spring Boot인데 **Docker Desktop 설정 체크박스 하나로 결과가 갈린다.** 이건 일화가 아니라 **휴리스틱**이다. 아래 §휴리스틱에 다시 넣었다.
- 다른 사용자 `jdnurmi`가 스스로 찾아낸 탈출 절차 (2025-09-04):
  > "So chasing this down myself, the effective steps I needed to run to change architectures:
  > ```
  > docker rmi -f docker.io/paketobuildpacks/builder-jammy-java-tiny:latest paketobuildpacks/java paketobuildpacks/run-jammy-tiny paketobuildpacks/java paketobuildpacks/builder-jammy-buildpackless-tiny
  > ./gradlew --stop
  > ```
  > **Anything less any the builds seemed "contaminated"** - I also had to use distinct build images (appended $arch myself), and then do manifest create/push to get it to upload.
  > Hopefully this helps someone else who gets here by search"

  → "contaminated"라는 단어가 §2-2의 캐시 오염과 정확히 같은 진단이다. **1년 넘게 같은 함정이 재생산됐다.** (🟡 반복 패턴)
- **결말:** `philwebb` 🟢가 2025-11-13에 `pack` CLI로 직접 대조 검증 후 수정 PR을 언급, `hojooo`가 3.5.8-SNAPSHOT에서 재검증.
  `(1차 소스 확인 필요 — PR #47292가 실제로 어느 릴리스에 들어갔는지, 그 릴리스가 GA인지 Spring Boot 릴리스 노트로 확인할 것. 이슈 댓글은 SNAPSHOT 검증까지만 담고 있다)`

---

## 3. Docker Desktop 라이선스와 대안 런타임 이주

### 3-1. 2021-08~2022-01, 발표 직후의 온도
- **원 공지 HN 제출:** "Docker is updating and extending our product subscriptions" (docker.com/blog/updating-product-subscriptions/) — HN 28368997, **2021-08-31**, 135 points. *(댓글 스레드는 이번 세션에서 열지 않았다 — 미확인)*
- **같은 날 올라온 Ask HN:** "Ask HN: Any Good Alternative for Docker?" (2021-08-31, 47 points)
  - Podman 회의론 (`c7DJTLrn`) — **대안 이주가 순탄하지 않다는 첫 신호:**
    > "I'm a Podman skeptic. Whenever I've tried these "OCI compatible" alternatives in the past it's been a painful experience because something doesn't work as expected. **Podman's homepage proclaims it's as simple as "alias docker=podman" but it has never worked out for me this way.** Docker is ubiquitous and significantly more battle-tested, and even has a rootless mode now."
- **유예 종료 직전 (2022-01-05) "Ask HN: What are you going to use instead of Docker Desktop for macOS?"** (HN 29815122)
  - 질문자 본인의 상황 정리 (원문): "For Linux and Windows (with WSL) I just use the docker engine cli, **but for Mac, I'm not sure.**" → **맥이 유독 어려운 이유가 이 한 줄에 있다.**
  - 대안별 실패담 (`xtracto`):
    > "I've tried both of those and minikube by itself. For me the main disadvantage has been **compatibility with docker-compose.** I've got several projects that I run using docker-compose.yml as a "turnkey" solution. **The podman compatibility is unusable, and migrating to K8s manifest files is cumbersome.** Also Rancher Desktop is not a complete replacement solution, once you install it you have to add some other stuff to make it work.
    > All this kind of has made me think more about **the vendor lock-in that we were having with Docker.**"
  - **조직 정치가 등장하는 지점** (양쪽 다 있다):
    - 돈으로 해결한 쪽 (`yuppie_scum`): "I got my management to agree that it's worth the $5 a month for everyone's productivity."
    - 실패한 쪽 (`pseudoramble`): "Ah man, that must be a magical place. **I spent months (on-and-off) trying to convince my company to do this and failed.** ... it genuinely worries me that while **IT considers it unapproved software** that it won't stop its usage."
      → **"승인 안 된 소프트웨어인 걸 알면서 다들 그냥 쓰고 있다"** — 조직의 회색지대. 한국 SI/대기업 독자에게 특히 공감될 지점.

### 3-2. 한국 커뮤니티 반응
- **OKKY "내년부터 도커 유료화하나요?"** (작성자: 날리지베이스, 카테고리 "사는 얘기")
  - 접근 결과: 본문은 읽혔으나 **댓글은 "댓글을 남기려면 로그인이 필요합니다"로 막혀 미열람.** 게시 날짜도 페이지에 노출되지 않았다 → **날짜 미확인.**
  - 내용 요지 `(원문 대조 필요 — WebFetch 요약)`: 도커를 배우려다 라이선스 변경을 발견. "내년 2월부터 무료사용자에 대한 도커 데스크탑 접근을 제한"한다는 언급. **Docker Desktop과 Docker Hub의 차이를 혼동**하고 있으며, 오픈소스로 알았던 도구의 상업화에 실망을 표함.
  - ⭐ **이 혼동 자체가 값진 발견이다.** "Docker Desktop 유료화"와 "Docker Hub 유료화"와 "Docker Engine"을 구분 못 하는 게 입문~중급 독자의 실제 상태다. **책에서 이 셋의 경계를 명확히 그어줄 이유.**
  - 출처: https://okky.kr/articles/1085503
- **GeekNews "Docker Desktop 대안, Container Desktop"** (news.hada.io/topic?id=16867, 2024-09-21, 댓글 2개)
  - 댓글 `ndrgrd` (2024-09-27) 요지 `(원문 대조 필요)`: Podman이 예전에는 버그가 많다고 들었는데 최근에 나아졌는지 궁금하다.
  - → 2024년 말에도 **"Podman 괜찮아졌나요?"가 여전히 열린 질문**이라는 신호.
- **미열람 한국어 소스 (제목·URL만 확인, 본문 미확인):**
  - 주길재(Giljae Joo), "유료로 전환되는 도커 데스크탑 대체하기 (Mac M1)" — giljae.com URL의 경로에 `2022/01/21` 포함
  - devkuma, "Apple M1 칩셋의 macOS 환경에서 Colima 활용하여 Testcontainers 실행하는 방법"
  - DEVOCEAN(SK), "Docker Desktop 유료화와 대응방법" / "M1 Mac에서 Docker사용 (feat. Rancher desktop)"

### 3-3. OrbStack 실사용 후기 — 성능은 압도적, 그런데 (HN 41421846, 2024-09-02, 307 points)
**긍정 (성능):**
- `jchw` — 이 책에서 인용할 만한 가장 구체적인 성능 증언:
  > "Using Docker Desktop to compile Envoy using the standard Docker build process took somewhere in the ball park of **3 to 4 hours** depending on my luck. OrbStack, on the other hand, brought it down to **a bit under an hour**, much closer to inline with a fresh compilation natively. Needless to say, the kinds of performance benefits I was seeing with OrbStack were game changers, and absolutely justify the cost."
  `(확인 필요 — 벤치마크가 아니라 한 사람의 체감·환경 미상. "3~4시간 → 1시간 미만"을 일반 수치로 쓰지 말 것)`
- `marvin-hansen` (2024-09-02): "I am so close to delete Docker permanently. There is no comparison, not even close. All integration tests run so much faster. Especially parallel container starts a noticable faster."
- `rudi_mk`: "Pretty performant on my older M1 MBP too."

**부정·주의 (여기가 더 값지다):**
- **라이선스 서버 의존** (`weikju`, 2024-09-02):
  > "I was moving and during nearly a month there was no home internet. My server was happily chugging along on wifi though, but one day I connected to it and saw a message that **OrbStack couldn't contact the license server and soon stop functioning.** This put me off a bit and made me consider whether I want to run anything I depend on using this."
  → **Docker Desktop 라이선스를 피해서 왔는데 또 다른 라이선스 의존이 생겼다.** 아이러니 그 자체.
- **회사가 안 사준다** (`commandersaki`): "unfortunately I have difficulty convincing my employer to pay for a commercial license, and with my sparse Docker usage, I'm confined to using it only for personal/hobby usage." → §3-1의 `pseudoramble`과 정확히 같은 벽.
- **백업 소프트웨어와 충돌** (`KingMob`):
  > "Under the hood, OrbStack uses an **8TB sparse disk image**, which doesn't play nice with most backup software. ... It caused me problems with Backblaze, but the Github issues for this show that it also breaks all sorts of backup software, including tarsnap, Druva inSync, Carbon Cloner, iDrive, Carbonite, and even Time Machine itself when formatted with HFS+, apparently. **The official position for a year was "won't fix"**, because it's an Apple technology, and backup software should support that."
  `(1차 소스 확인 필요 — 8TB sparse image / "won't fix" 정책은 orbstack/orbstack#29 이슈를 직접 열어 확인할 것. 이번 세션에서 열지 않았다)`
- **로컬-운영 네트워킹 불일치** (`nkmnz`):
  > "One reason I'm still using docker desktop in my (small) company is that our production systems are using docker compose and **the networking with domains does not translate 1:1 between orbstack locally and docker compose + nginx in production.**"
  → **"로컬과 운영을 똑같이 만들려고 컨테이너를 쓰는데, 런타임을 바꾸면 그 등가성이 깨진다"** — 이 책의 핵심 논점 중 하나.
- **바꿔보기가 무섭다** (`styfle`): "I have a machine with Colima and don't want to bork it if I try Orbstack. ... Is "brew install orbstack" a drop in replacement for colima or does it install other things that might conflict?"
  → ⭐ **`env_probe.md`가 보여주는 "런타임 두 개 공존" 상태를 만드는 심리가 바로 이거다.** 지우기는 무서우니까 일단 같이 깔아둔다.

### 3-4. Colima 진영의 반론 (같은 스레드)
`nrvn` (2024-09-02), colima 2년 사용자:
> "I have been using colima as a lightweight alternative to docker desktop and the likes of it for almost two years. Looking at the comparison provided on the orbstack website it seems to be **not very accurate** or at least requires some explanations/clarifications.
> For instance: Low power/CPU usage is advertised as non-existent in colima. **This is simply not true.** Based on my perception I can't tell whether colima VM is running or not. **Unlike docker desktop, especially with kubernetes on. Does not drain my battery, does not bog my CPU down** unless I intentionally spin up something resource hungry."

→ ⭐ **"Docker Desktop은 Kubernetes를 켜면 배터리를 먹는다"**는 체감 보고. 2순위 요구사항의 "맥북 배터리·메모리 불평"에 해당. `(확인 필요 — 측정 아님, 체감)`

Colima의 단점 보고 (`princevegeta89`, 2024-09-02):
> "I've been using Colima which has been great, and much better than Docker Desktop which sucked ass for me. With Colima, **file mounting and sharing caused reliability and permission issues for me** though I've applied some workarounds with success."

---

## 4. K8s 도입 논쟁 (양쪽 다)

> 주 출처: HN "「Let's use Kubernetes.」 Now you have eight problems" — https://news.ycombinator.com/item?id=22491170, **2020-03-05, 719 points, 469 comments** (원글: pythonspeed.com/articles/dont-need-kubernetes/)
> ⚠️ **2020년 스레드다.** 6년 전 논쟁이므로 "당시 기준"임을 반드시 명시할 것. 2026-06-02의 후속 스레드(HN 48366913, "You Don't Need Kubernetes", 6 points)는 실질 댓글이 1개뿐이라 논쟁 재료로는 빈약했다.

### 관점 A: "필요 없었다"
- **비용을 수치로 말한 증언** (`sho`):
  > "I personally know startups for whom I believe drinking the k8s/golang/microservices kool-aid **has cost them 6-12 months of launch delay and hundreds of thousands of dollars** in wasted engineering/devops time. For request loads one hundredth of what I was handling effortlessly with a monolithic Rails server in 2013.
  > It is the job of the CTO to steer excitable juniors away from the new hotness... **k8s on day one at a startup is like a mom and pop grocery store buying SAP.** It wouldn't be acceptable in any other industry, and can be a death sentence."
  `(확인 필요 — 3자 전언, 검증 불가)`
- **더 세게 받은 사람** (`zeveb`):
  > "If Kubernetes had only cost us a year and two hundred thousand dollars then we'd have been luckier than we actually are. It definitely has a place, but it is *so* not a good idea for a small team. **You don't need K8s until you start to build a half-assed K8s.**"
- **구체적 청구서** (`mirko22`) — 챕터 오프닝으로도 쓸 만하다:
  > "**1000 users, almost 0 request per second / 10000 euro a month** to deploy a very simple software on GKE in 3 continents and have some development instances.
  > Why? Because Docker and "scalability" it offered looked much better on the investor slides...
  > How? Instead of actually hiring someone that at least has experience with docker he decided it was very easy thing to learn so he did it him self and we ended up with thing like **running two application in a same container, having database on containers that disappear** (container restarts when ram is full is the *best* way to run a database) etc...
  > And after all that started talking about mirco-services... I don't work there anymore..."
  `(확인 필요 — 익명 개인 경험)`
- **아키텍처 선택이 원인이지 사업이 원인이 아니다** (`onion2k`):
  > "**Choosing to build microservices is what adds complexity and makes tools like k8s necessary, not the business.** ... In most small startups that are just proving their model they'd be much better off hacking something together that they'll throw away later in order to validate the business idea."
- **인사·번아웃 피해** (`Kaze404`):
  > "I worked at a startup where the CTO *was* the impressionable junior and it caused all of those issues you described and more. I ended up leaving when I decided I shouldn't be having panic attacks in the middle of the night due to ridiculously tight deadlines that I couldn't meet because of the overhead introduced by k8s and microservices."
- **과잉 사례** (`_xnmw`): "I've seen k8s deployed for internal back office apps that have literally 5 users - a raspberry pi could've hosted it. **Keeping things simple and reliable is often a harder skill to learn than $BIGCO_TECH**, and often confounded by political incentives."

### 관점 B: "필요했다 / 반박"
- **정면 반박** (`WnZ39p0Dgydaz1`):
  > "**I'm getting tired of these "you don't need k8 posts".** Sure, if you have a simple web application with a REST API, don't use k8, unless it's for learning purposes. But nobody does that anyway. If you have something more complex with many moving parts that are separate services, k8 is a great option. I've been using it in production for close to 2 years now - **not a single service downtime, great fault-tolerance, and absolutely zero management effort.**"
- **성공 사례 + 조건 명시** (`theptip`) — 논쟁에서 가장 균형 잡힌 발언:
  > "Anecdata: series B startup. First year was a single VM with two docker containers for api and nginx. Deploy was a one shot "pull new container, stop old, start new" shell command. Year 2 onwards, k8s. No regrets, **we only needed to make our first dedicated ops hire after 15 engineers**, due in large part to the infra being so easy to program.
  > I used GKE and **I was also very familiar with k8s ahead of time. I would not recommend someone in my shoes to learn k8s from scratch at the stage I rolled it out**, but if you know it already, it's a solid choice for the first point that you want a second instance."
  → ⭐ **손익분기점이 "규모"가 아니라 "팀에 이미 아는 사람이 있는가"라는 주장.** 실무 판단 기준으로 그대로 쓸 수 있다.
- **"대안도 결국 K8s가 된다"** (`honkycat`):
  > "I've been saying for years that **if you go with Docker-Compose, or Amazon ECS, or something lower level, you are just going to end up rebuilding a shittier version of Kubernetes.**
  > I think the real alternative is Heroku or running on VMs, but then you do not get service discovery, or a cloud agnostic API for querying running services, or automatic restarts, or rolling updates, or encrypted secrets, or automatic log aggregation, or plug-and-play monitoring, or VM scaling... **But nobody needs those things right?**"
- **저자층에 대한 반론** (`envoked`):
  > "**I think a lot of these anti-k8s articles are written by software developers who haven't really been exposed to the world of SRE** and mostly think in terms of web servers.
  > A few years ago I joined a startup where everything (including the db) was running on one, not-backed-up, non-reproducible, VM. In the process of "productionizing" I ran into a lot of open questions: How do we handle deploys with potentially updated system dependencies? Where should we store secrets (not the repo)? How do we manage/deploy cronjobs? How do internal services communicate? **All things a dedicated SRE team managed in my previous role.** GKE offered a solution to each of those problems."
- **스케일이 아니라 재현성이 목적** (`avereveard`):
  > "same we use kubernet not for scale but for **the environment repeatability**. we can spin any branch at any time on any provider and be sure it's exactly as we have it in production down to networking and routing"
- **조직 내 가독성** (`bertil`) — 잘 안 나오는 논거:
  > "I think **the main oversight of those "you don't need k8s" is that most projects are part of a system and fitting in that system gives you legibility to your peers** that a nginx might not."
- **외부 압력** (`TallGuyShort`):
  > "I've seen the pressure come from customers too, in the case of b2b between tech companies. My company embraced Kubernetes after years of customers asking us **"what's your Kubernetes story?"** and not liking the answer, "that doesn't solve any problems we have"."
- **채용 압력** (`marcinzm`): 신기술을 안 쓰면 엔지니어가 다른 데로 간다는 반론.

### 중간 지대 (실무 판단 기준으로 가장 유용)
- `mrweasel`:
  > "I would recommend **two machines and a loadbalancer.** Most often the thing that doesn't scale isn't the applications you're able to run in Kubernetes, at least not at first. **Most customers I've dealt with who have scaling issue need take a look at their database before Kubernetes.** ...
  > The thing is: **when stuff breaks, you'll prefer that it's not the Kubernetes stuff.** If you run the infrastructure your self, you should be VERY sure that you know how it works, because debugging it is extremely complex."
- `adieu`: "k8s is raw technology like linux kernel. You shouldn't use it directly which will be hard to maintain. There are bunch of packaged solutions around k8s like Google GKE or AWS EKS." → **"K8s를 쓴다"와 "K8s를 운영한다"는 완전히 다른 결정**이라는 구분. 논쟁 대부분이 이걸 안 나눠서 평행선을 달린다.
- `supermatt`: "If you are managing kubernetes yourself, on your own hardware, the moving parts can indeed be a burden for a small team - **but all of these pain points go away with a managed kubernetes**... There are less moving parts in docker compose, and its easier to run on a single VM - **but it doesnt offer any of the dynamic features of kubernetes that you would want at scale. The same containers can run on both.**"
- `mosselman` — compose → K8s 마이그레이션 경로가 쉽다는 원글 주장에 대한 반박:
  > "「there is a trivial migration path from docker-compose to kubernetes」 The migration path of docker-compose to **swarm** is basically: `eval $(docker-machine env my_cluster)` / `docker deploy --compose-file docker-compose.yml PROJECT_NAME`. **I have looked into k8s and it wasn't as easy as this.**"
- `skrebbel`가 던진 질문이 이 책이 답해야 할 질문 그 자체다:
  > "It seems to me that there's something of a gap between "for single machine setups" (eg docker-compose) and "for 500-engineer teams" (eg kubernetes)."
  > → **바로 이 갭이 이 책의 독자가 서 있는 자리다.**

### 로컬 K8s / 맥 리소스 관련
- `supermatt` (2020): "I could use minikube in almost exactly the same way. i.e. **there is effectively no difference from a development perspective.**"
- `nrvn` (2024, §3-4): Docker Desktop은 "especially with kubernetes on" 배터리·CPU를 먹는다.
- ⚠️ **kind/k3s/minikube 각각의 맥북 배터리·메모리 소모를 수치로 비교한 커뮤니티 자료는 이번 검색에서 확보하지 못했다.** (커버리지 부족 항목)

---

## 5. 맥 개발 환경 일반의 고통

> # ⛔ 이 섹션을 읽는 챕터 저술가에게 — 먼저 읽어라
>
> 이 섹션의 대부분(`[제목만]` 표시 항목)은 **`gh issue list`로 제목·상태·등록일만 확인했고 본문·댓글은 열지 않았다.**
>
> - ✅ **사실로 쓸 수 있는 것:** 그 번호의 이슈가 존재한다는 것, 그 제목, 등록일, 2026-07-25 조회 시점의 OPEN/CLOSED 상태. **딱 여기까지다.**
> - ⛔ **쓸 수 없는 것:** 인용문, 사고 경위, 증상 상세, 원인, 해결 과정, 등장인물. **오프닝 일화로 쓰지 마라.** 제목에서 이야기를 상상해 채우는 순간 그건 창작이다.
> - 오프닝 소재가 필요하면 위 ⭐ 섹션(본문·댓글 전문 확보)에서 가져와라.
>
> 이 섹션의 용도는 **"이 주제에 이슈가 이만큼 쌓여 있고 이만큼 오래 열려 있다"는 분포 근거**를 제공하는 것이다.
>
> 신선도 원장에는 `[제목만]` 항목을 개별 행으로 넣지 않았다. **§5의 `[제목만]` 항목 전체는 아래 "미확인 / 확인 필요 목록"에 한 블록으로 원장 처리한다** (신뢰도 = "제목·상태·날짜만 확인, 본문 미열람").

### 5-1. 볼륨 마운트 I/O 성능
- `docker/for-mac#3677` "**Bind mounts are really slow**" — 2019-05-20 등록, **2026-07-25 조회 시점 여전히 `OPEN`** `[제목만]`
  → **확인된 사실:** 2019-05-20 등록, 제목이 저것, 조회 시점 OPEN. 즉 **7년 넘게 열려 있다.** 이 세 가지는 쓸 수 있다. 이슈 안에서 무슨 논의가 오갔는지, 왜 안 닫혔는지는 **모른다** — "구조적 한계라서 못 고쳤다" 같은 해석을 붙이지 마라.
- `docker/for-mac#77` "File access in mounted volumes extremely slow" — 2016-08-02 등록, **OPEN** `[제목만]` (10년 열려 있음)
- `docker/for-mac#1592` "File system performance improvements" — 2017-05-05, OPEN `[제목만]`
- `docker/for-mac#7494` "file corruption virtioFS and gRPC bind mount 4.36.0" — 2024-11-27, OPEN `[제목만]` ← **성능이 아니라 파일 손상 보고. 제목만으로도 무겁다**
- `docker/for-mac#6243` "VirtioFS is not handling permissions as expected. All mount permissions are owned by root regardless of chown." — 2022-03-19, OPEN `[제목만]`
- `docker/for-mac#7464` "What makes Docker VMM better than Apple Virtualization Framework?" — 2024-10-24, OPEN `[제목만]` ← VM 백엔드 선택지가 여러 개라는 것 자체가 혼란의 원천
- ⚠️ **Gradle/Maven 빌드나 node_modules 워크로드의 구체적 수치 비교는 확보하지 못했다.**

### 5-2. 디스크 이미지가 계속 커지는 문제
- `docker/for-mac#371` "**Docker.qcow2 never shrinks - disk space usage leak in docker for mac**" — 2016-08-19 등록, CLOSED.
  - 확인된 흥미로운 사실: 이 이슈의 `+1` 한 줄짜리 댓글(`lxhunter`, 2016-08-20)에 **THUMBS_UP 349개, THUMBS_DOWN 45개**가 달려 있다. → 얼마나 많은 사람이 같은 문제로 이 페이지에 도달했는지를 보여주는 지표. (2016년 이슈, 당시 기준)
- `docker/for-mac#7187` "High Disk Usage after updating to 4.27.1 on Mac M2" — 2024-02-14, OPEN `[제목만]`
- `docker/for-mac#6865` "Docker Desktop reports incorrect VM Disk usage, possibly causing Engine to be unable to start" — 2023-06-02, OPEN `[제목만]`
- `docker/for-mac#5486` "**Shrinking Docker Disk Image Size DELETES All Other Files In The Same Directory As The Disk Image**" — 2021-03-21, CLOSED `[제목만]`
  → ⛔ **확인된 사실은 "2021-03-21에 이런 제목의 이슈가 등록됐고 CLOSED다"까지가 전부다.** 실제로 파일이 삭제됐는지, 재현됐는지, 어떻게 종결됐는지는 **본문을 열지 않아 모른다.** "정리하려다 파일을 날린 사건이 있었다"고 쓰면 안 된다. 쓰려면 이슈를 먼저 열어라.
- `docker/for-mac#2501` "Operations hang after starting system prune" — 2018-01-24, OPEN `[제목만]`
- **VM 안 디스크가 따로라는 사실:** 일화 11 (Rancher Desktop, 호스트 120GB 여유인데 VM 데이터 볼륨 100% 사용) 참고.

### 5-3. 메모리·발열
- `docker/for-mac#6120` "**Docker process doesn't free up memory - macOS, Apple Silicon, Virtualization.framework**" — 2022-01-03, OPEN `[제목만]`
- `docker/for-mac#7145` "**CPU Usage peaks to 800% on running amd64 docker images**" — 2024-01-27, OPEN `[제목만]` ← amd64 에뮬레이션과 CPU 폭주의 연결
- `docker/for-mac#5164` "com.docker.backend uses 100% with no containers running" — 2020-12-21, CLOSED `[제목만]`
- 실사용 증언 (`iaurg`, 2023-11-20, docker/for-mac#7075 댓글, 본문 확인함):
  > "Sometimes, the computer just crashes because resources are completely used by Docker, forcing me to reset the OS."
- 배터리 체감 (`nrvn`, 2024-09-02, HN): colima는 "Does not drain my battery, does not bog my CPU down" — Docker Desktop 대비, **especially with kubernetes on**. `(확인 필요 — 체감)`

### 5-4. Rosetta/QEMU 관련 이슈 밀집 (제목만)
`gh issue list --repo docker/for-mac --search "Rosetta emulation"` 결과 중 OPEN 상태인 것들:
- `#7093` "Docker Rosetta x64 emulation failing" — 2023-11-28
- `#7475` "Rosetta error: Unimplemented syscall number 282 - M1 Mbp inside docker container" — 2024-11-05
- `#7440` "Rosetta adds a cache folder owned by root in user directory" — 2024-10-01
- `#6921` "Unable to debug amd64 binaries on apple silicon" — 2023-07-16 ← **디버깅이 안 된다**는 건 자바 개발자에게 치명적
- `#7499` "Next.js next build churns CPU forever in linux/amd64 on arm64 silicon mac" — 2024-12-09
- `#6698` "rosetta error: unexpected valid thread with no suspend owner while resuming during php composer install" — 2023-01-21
- `#6678` "Docker Desktop 4.16.0 Run x86_64 dind image fails to pull images" — 2023-01-13
→ **2023~2024에 걸쳐 Rosetta 관련 OPEN 이슈가 계속 쌓여 있다**는 사실 자체가 "에뮬레이션은 여전히 새는 추상"이라는 논거. `[전부 제목만]`

### 5-5. Testcontainers
- 일화 8·9 참조.
- `testcontainers/testcontainers-java#8537` "[Enhancement]: Support TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE to be read from `~/.testcontainers.properties`" `[제목만, 상태·날짜 미확인]`
- `testcontainers/testcontainers-java#10528` "[Bug]: LocalStack fails on macOS/colima with socket creation error" `[제목만, 상태·날짜 미확인]`
- `testcontainers/testcontainers-go#3460` "[Bug]: panic when connecting to colima 0.9.1" `[제목만]`
- `testcontainers/testcontainers-go#2952` "[Bug]: `panic: rootless Docker not found` with Colima on macos" `[제목만]`
→ **Colima 이주 시 Testcontainers가 깨지는 건 Java에 국한되지 않는다**(Go 클라이언트에도 같은 계열 이슈). 다만 본문 미확인.
- ⚠️ **"맥에서 Testcontainers가 느려서 Spring Boot 테스트가 느려진다"는 구체적 수치·증언은 확보하지 못했다.** (커버리지 부족)

---

## 6. 이미지 빌드·업데이트 실무 습관

> ⚠️ **이 섹션이 이번 리서치에서 가장 부실하다.** 아래 §커버리지 자기평가 참조.

### 6-1. Alpine 논쟁 (양쪽 다) — HN 35056594, 2023-03-07, 34 points
원글: martinheinz.dev/blog/92 "I Will Never Use Alpine Linux Ever Again"

**Alpine 반대 진영:**
- `brimstedt`:
  > "Alpine has bitten me on several occasions as well. Nowadays, both on my previous and current job, **we go for Debian slim. Works perfectly and is worth the extra bytes.** I will also never use alpine again :-)"
  → ⭐ **"몇 바이트 더 쓰는 게 낫다"** — 이미지 크기 최적화의 실무 손익분기점을 한 문장으로.
- ⭐ **자바 독자 정조준** (`huksley`):
  > "Last time I checked, also - Java. **Using some PDF / Graphics related stack with Alpine can be difficult and might fail in some not obvious ways.** Maybe this situation improved a bit now. Even those java/jdk-*-alpine images, claiming being able to run JDK **actually support only subset of a (gigantic) APIs available in Java.**"
  `(확인 필요 — "Last time I checked", "Maybe this situation improved a bit now"라고 본인이 불확실성을 붙였다. 2023-03 시점 의견. JDK Alpine 이미지의 현재 상태는 반드시 1차 소스로 확인할 것)`
- `kenmacd` — musl DNS의 구체적 실패 경로 (K8s + Cloudflare DNSSEC):
  > "* K8s sets container to use `ndot:5`, causing the search list to be used / * Musl walks that search list looking for domain / * Cloudflare does not set the NXDOMAIN flag on a DNSSEC domain but does include an NSEC record... / * **Musl takes this 'NOERROR' reply and returns an EAI_NODATA.** ... The issue is that **every other libc I tested will continue searching**"

**Alpine 옹호 진영:**
- `Gordonjcp` — 냉소적 반박:
  > "So because they have a weirdass edge case because of their broken design (ridiculously outsize DNS replies), they're going to stop using a particular distro that **nearly everything in Docker is based on**? Oooh-kaaaay.... sure, I guess"
- `mattpallissard`:
  > "The only real gripe I see in here is 'Alpine uses muslc'. And the only problem they have with musl is DNS resolution over UDP. I've written a fair amount of C over my career. And let me tell you, **shipping statically compiled binaries that cal getaddrinfo with musl "Just works". That is not the case with glibc which expects to be dynamically linked.**"
- `justin_oaks` — 가장 실용적인 태도:
  > "The Docker containers I run are a mixed bag of base images. **I often reach for Alpine first. If that doesn't work for some reason I think "Oh well" and switch to Debian or Ubuntu.**"

**시점 주의 (중요):** `_ikke_` (2023-03-07):
> "You might not be aware, but **dns-over-tcp has been added to musl and will be part of the next release.**" (링크: musl 커밋 51d4669)

→ ⛔ **"Alpine은 DNS over TCP를 지원하지 않는다"고 2026년 책에 쓰면 틀릴 가능성이 크다.** 이 논쟁의 핵심 논거는 2023-03 시점에 이미 수정 중이었다. `(1차 소스 확인 필요 — musl 릴리스 노트에서 어느 버전부터 들어갔는지, Alpine이 어느 버전부터 그 musl을 쓰는지 확인 필수)`

### 6-2. 확보하지 못한 것 (정직한 공백)
- **`latest` 태그 때문에 터진 구체적 사고담:** HN Algolia에서 `latest tag docker production incident` 등으로 검색했으나 **일화라 부를 만한 스레드를 찾지 못했다.** 관련 언급이 있는 스토리 제목은 "Things to avoid in Docker containers"(2016-03-01), "Dockerfile Security Best Practices"(2020-10-14) 정도이며 본문 미확인.
- **베이스 이미지 업데이트를 실제로 어떻게 굴리는가 (자동화 vs 수동, 주기):** 관련 커뮤니티 토론 미확보.
- **취약점 스캔 도입 후의 알림 피로:** 미확보.
- **이미지 크기 줄이기 삽질담:** Alpine 논쟁 외 확보 못 함. 참고로 "Alpine makes Python Docker builds slower, and images larger"(HN 22182226, 2020-01-29, **306 points, 149 comments**)는 **제목·점수만 확인했고 댓글은 열지 않았다.** 후속 리서치 1순위 대상.

---

## 실무자 휴리스틱 (커뮤니티에서 반복 등장하는 판단 기준)

### H1. 트러블슈팅의 첫 명령은 "무엇이 실행되고 어디에 붙는가"를 분리해서 묻는 것
- `docker --version`은 **클라이언트** 버전일 뿐이다. 데몬은 `docker info` / `docker version`의 Server 섹션.
- 근거: `env_probe.md` §4 실측(클라이언트 `27.5.0-rd` ↔ 서버 `29.6.2`) + testcontainers#5034의 `docker context list` 진단 + colima#365.
- 커뮤니티 처방: `docker context ls`로 활성 컨텍스트 확인 → `DOCKER_HOST` 확인 → `command -v docker`로 실제 바이너리 확인.

### H2. `exec format error`가 보이면 **가장 단순한 이미지로 범위를 좁혀라**
- `thaJeztah`(Docker) 🟢의 실제 진단 절차: `docker run -it --rm --platform=linux/amd64 busybox`
- busybox조차 실패하면 → 내 이미지 문제가 아니라 **에뮬레이션 계층 문제**.
- 다음 단계 (`ctalledo` 🟢): `binfmt_misc` 등록 확인 (§일화 1에 명령 원문).
- 출처: docker/for-mac#7849, 2026-02

### H3. 아키텍처를 바꿨는데 안 고쳐지면 **캐시를 의심하라**
- 빌드 캐시·기존 이미지가 아키텍처를 고려하지 않고 재사용될 수 있다.
- `dmikusa` 🟢 (2024-06): "just delete your existing app images and the build cache" / "or you can change the image name, that will trigger a fresh build too"
- `jdnurmi` (2025-09): "Anything less any the builds seemed 'contaminated'" → `docker rmi -f` 빌더/런 이미지 전부 + `./gradlew --stop`
- **1년 이상 간격을 둔 두 사람이 같은 진단에 도달했다** (🟡)

### H4. ⭐ Docker Desktop의 "Use containerd for pulling and storing images" 토글은 빌드 결과를 바꾼다
- `hojooo` (2025-10-23, M1): 이 옵션을 켜면 `bootBuildImage`의 플랫폼 불일치 문제가 재현되고, 끄면 재현되지 않았다.
- `philwebb`(Spring Boot 커미터) 🟢도 2025-11-13 분석에서 이 옵션 on/off를 나눠서 검증했다.
- → **"내 맥에서만 안 되는데요"의 유력한 용의자.** 동료와 결과가 다르면 이 체크박스부터 비교하라.
- `(1차 소스 확인 필요 — 현재 Docker Desktop 4.83.x에서 이 옵션의 기본값이 무엇인지는 확인하지 않았다. env_probe에도 없다)`

### H5. Rosetta 토글은 켠다/끈다 둘 다 시도해봐야 하는 변수다
- 커뮤니티 다수가 **끄는 쪽**에서 해결을 봤다 (docker/for-mac#7075, 2023-11~2024-06, 🟡)
- 다만 이건 그 시기·그 Docker Desktop 버전들의 이야기다. **"끄는 게 맞다"고 단정하지 말 것.**
- 가장 확실한 처방은 여전히 **에뮬레이션을 안 하는 것**: "Building arm images is a breeze" (`alnaranjo`)

### H6. Testcontainers + 대안 런타임은 **두 개의 서로 다른 소켓 경로**를 요구한다
- `DOCKER_HOST` = 호스트에서 본 소켓 (`unix:///${HOME}/.colima/docker.sock`)
- `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` = **컨테이너(Ryuk) 안에서 본 소켓** (`/var/run/docker.sock`)
- 출처: `benhexagon`, testcontainers-java#5034, 2022-02-11
- ⛔ **`TESTCONTAINERS_RYUK_DISABLED=true`는 해결이 아니라 은폐다** (`kiview`, Testcontainers 메인테이너 🟢). 한국어 블로그에 널리 복붙돼 있으니 특히 경고할 것.

### H7. kubectl "current context"에 대한 커뮤니티 처방 스펙트럼 (HN 41578274, 2024-09)
합의된 답이 없다. 강도 순으로:
1. 프롬프트에 컨텍스트·네임스페이스 표시 (`decasia`, `Yasuraka` — kubectx + kube-ps1)
   - 단, `Telemaco019` 🔴: "I also have it in my zsh config, but that didn't stop me from screwing up in the past."
   - `terinjokes`의 반박: 프롬프트는 한 번 그려지므로 **다른 셸에서 컨텍스트를 바꾸면 낡은 정보를 보여준다.**
2. 위험 명령에 확인 프롬프트 (kubesafe)
3. 매번 `--context` 명시 (`ed_mercer`: "the concept of a current context is evil", `cryptonector`)
4. 기본 kubeconfig를 아예 두지 않고 `KUBECONFIG`로만 (`lukaslalinsky`, `adolph`)
5. 셸 시작 시 current-context를 unset (`thewisenerd`) — 본인 왈 "now I mess up the wrong namespace instead :)"
6. 디렉터리 기반 자동 전환 (direnv + kustomize, `physicles`)
7. **운영 kubeconfig를 로컬에 아예 두지 않고 필요할 때만 받아온다** (`acedTrex`)
→ `env_probe.md` §5(활성 컨텍스트가 원격 EKS)를 이 스펙트럼 위에 올려놓고 독자에게 선택하게 하면 좋은 챕터가 된다.

### H8. K8s 손익분기점에 대한 커뮤니티 기준들 (합의 없음, 근거만 정리)
- "팀에 이미 K8s를 아는 사람이 있는가" (`theptip`) — 규모가 아니라 **역량**
- "직접 운영하는가 vs 매니지드를 쓰는가" (`adieu`, `supermatt`) — 이 구분 없이 논쟁하면 평행선
- "먼저 데이터베이스를 봐라" (`mrweasel`) — 스케일 문제의 진짜 위치
- "마이크로서비스를 선택했기 때문에 K8s가 필요해진 것" (`onion2k`) — 인과의 방향
- "고장 났을 때 그게 K8s가 아니길 바라게 된다" (`mrweasel`)

### H9. Alpine은 "먼저 시도해보고 안 되면 갈아탄다" (`justin_oaks`)
- 반대 진영의 최종 착지점도 대개 **Debian slim** (`brimstedt`)
- 자바에서 특히 주의 (`huksley`) `(확인 필요)`

### H10. 대안 런타임으로 옮길 때 실제로 깨지는 것들 체크리스트 (커뮤니티 보고 종합)
| 깨지는 것 | 출처 | 시점 |
|-----------|------|------|
| Testcontainers / Ryuk 소켓 | testcontainers-java#5034 | 2022-02 |
| `/var/run/docker.sock`을 하드코딩한 도구들(`act` 등) | colima#365 | 2022-07 |
| docker-compose 호환성 (Podman) | HN 29815122 | 2022-01 |
| 볼륨 마운트 권한·안정성 (Colima) | HN 41421846 | 2024-09 |
| 로컬↔운영 네트워킹/도메인 등가성 (OrbStack) | HN 41421846 | 2024-09 |
| 백업 소프트웨어 (OrbStack sparse image) | HN 41421846 | 2024-09 `(1차 소스 확인 필요)` |
| 오프라인에서 라이선스 서버 접속 실패 (OrbStack) | HN 41421846 | 2024-09 |
| `docker context` 전역 상태 다툼 (런타임 2개 공존) | rancher-desktop#7712 | 2024-11 (Windows) |

---

## 의견이 갈리는 지점 (논쟁 정리)

| 쟁점 | 관점 A + 근거 | 관점 B + 근거 | 출처 / 시점 |
|------|--------------|--------------|------------|
| **소규모 팀에 K8s가 필요한가** | 불필요. 6~12개월 지연 + 수십만 달러 낭비 목격(`sho`); "결국 반쪽짜리 K8s를 만들게 되기 전까진 필요 없다"(`zeveb`); 1000 users에 월 1만 유로(`mirko22`) | 필요할 수 있다. 2년 무중단·관리 노력 제로(`WnZ39p0Dgydaz1`); 엔지니어 15명까지 전담 ops 없이 버팀(`theptip`); Compose/ECS로 가면 "더 구린 K8s"를 재발명(`honkycat`); 안티-K8s 글은 SRE 경험이 없는 사람이 쓴다(`envoked`) | HN 22491170 / 2020-03 |
| **판단 기준을 무엇으로 잡을 것인가** | 규모·트래픽 (원글 및 다수) | 규모가 아니라 **이미 아는 사람이 있는지**(`theptip`), **직접 운영 vs 매니지드**(`adieu`), **조직 내 가독성**(`bertil`), **고객 요구**(`TallGuyShort`), **채용 경쟁력**(`marcinzm`) | HN 22491170 / 2020-03 |
| **Rosetta 켜는 게 나은가** | 끄는 게 낫다. 33,656초 → 껐더니 5분(`AlexandreRoba`, M3 Max 64GB); 4.30/4.31에서도 끄고 씀(`oming`) | Docker 팀은 특정 버전(4.26.0)에서 해결됐다고 보고 이슈를 닫았고 실제로 해결된 사용자도 있음(`djcristi`) | docker/for-mac#7075 / 2023-11~2024-06 |
| **Colima는 `/var/run/docker.sock`을 차지해야 하는가** | 차지해야 한다. 너무 많은 도구가 그 경로를 하드코딩("2 for 2", `james-s-w-clark`); 최소한 경고라도(`henrik242`) | 차지하면 안 된다. 도구들이 `docker context`로 옮겨가는 중이고, 소켓을 안 건드려야 **기존 워크플로를 깨지 않고 시험해볼 수 있다**(`abiosoft` 🟢) | colima#365 / 2022-07~2023-03, **여전히 OPEN** |
| **Ryuk을 끄는 우회는 허용되는가** | 실용적. 그렇게 해서 돌아갔다(`rottenha`) + 다수 한국어 블로그가 복붙 | ⛔ 안 된다. 원인 은폐이며 **리소스 정리가 신뢰할 수 없게 된다**(`kiview` 🟢) | testcontainers-java#5034 / 2022-02 |
| **Alpine을 써야 하는가** | 쓰지 마라. musl DNS(UDP only)로 여러 번 당함; Debian slim이 몇 바이트 값어치를 함(`brimstedt`); 자바 stack에서 예측 못 할 실패(`huksley`) | 써도 된다. 문제는 DNS 엣지 케이스 하나뿐이며 Docker 생태계 대부분의 기반(`Gordonjcp`); musl 정적 링크는 오히려 "Just works"(`mattpallissard`); **그리고 DNS-over-TCP는 이미 musl에 들어갔다**(`_ikke_`) | HN 35056594 / 2023-03 |
| **OrbStack 유료가 합당한가** | 합당. 3~4시간 → 1시간 미만 빌드, "absolutely justify the cost"(`jchw`) | 회사가 안 사준다(`commandersaki`); 라이선스 서버 오프라인 시 정지(`weikju`); colima 비교표가 부정확(`nrvn`) | HN 41421846 / 2024-09 |
| **buildpack vs Dockerfile (arm64 맥에서)** | buildpack. Dockerfile 안 써도 됨 | Dockerfile. buildx는 `--platform linux/amd64,linux/arm64`로 한 방인데 buildpack은 플랫폼별로 따로 빌드 후 **manifest를 손으로 만들어야** 한다(`heruan`, `dmikusa` 🟢 확인); 한국어 실전 후기도 같은 결론(velog @cmsong111) | paketo/spring-boot#491 / 2024-11, velog / 2025-03 |
| **kubectl current context는 유용한가** | 유용. 없으면 느려진다. 대신 안전망을 씌우자(`Telemaco019`) | "current context라는 개념 자체가 악(evil)"(`ed_mercer`); 기본 kubeconfig를 아예 두지 마라(`lukaslalinsky`) | HN 41578274 / 2024-09 |

---

## 미확인 / 확인 필요 목록

**📒 원장 블록 처리 — §5의 `[제목만]` 항목 전체**
신선도 원장에 개별 행을 만들지 않고 여기서 한 블록으로 원장 처리한다.
- **출처:** `gh issue list --repo docker/for-mac|rancher-sandbox/rancher-desktop|testcontainers/* --json number,title,state,createdAt` (GitHub REST)
- **검색 시점:** 2026-07-25
- **검증된 범위:** 이슈 번호 / 제목 문자열 / `createdAt` 날짜 / `state`(OPEN·CLOSED) — **이 네 가지만.**
- **신뢰도:** 제목·상태·날짜만 확인, **본문·댓글 미열람**
- **해당 이슈:** docker/for-mac `#77` `#371`(본문 일부 확인) `#1592` `#2501` `#3677` `#5164` `#5486` `#6120` `#6243` `#6678` `#6698` `#6865` `#6921` `#7093` `#7145` `#7187` `#7440` `#7464` `#7475` `#7494` `#7499` / rancher-desktop `#3080` `#8606` `#10049` / testcontainers-java `#8537` `#10528` / testcontainers-go `#2952` `#3460`
- **사용 규칙:** 분포·존속기간 근거로만. 인용·증상·원인·해결 서술 전면 금지.

**⛔ 절대 인용 금지 (제목만 확인, 페이지 미열람)**
- `paketo-buildpacks/base-builder#652`, `paketo-buildpacks/stacks#51`, `paketo-buildpacks/java` Discussion #1387, `buildpacks/pack#1003` — 웹 검색 결과 스니펫에만 등장. **상태·날짜·본문 전부 미확인.**
- `orbstack/orbstack#29` (8TB sparse image 백업 문제) — HN 댓글이 링크만 언급.
- `docker/for-mac` 이슈 중 §5에서 `[제목만]`으로 표시한 전부.
- `testcontainers-java#8537`, `#10528`, `testcontainers-go#3460`, `#2952`.
- HN 22182226 "Alpine makes Python Docker builds slower, and images larger" (2020-01-29, 306pt, 149 comments) — 댓글 미열람.
- HN 28368997 Docker 라이선스 공지 제출(2021-08-31, 135pt) — 댓글 미열람.

**🔍 1차 소스로 반드시 검증할 기술적 주장**
| 주장 | 커뮤니티 출처 | 검증할 곳 |
|------|--------------|----------|
| "arm64용 Paketo 빌더는 `builder-jammy-buildpackless-tiny`" | dmikusa, 2024-06 | Paketo 공식 문서 (2026-07 현재 빌더 라인업) |
| "`pack build`도 `spring-boot:build-image`도 한 번에 멀티아키를 못 만든다" | dmikusa, 2024-11 | Spring Boot 4.x / buildpacks 릴리스 노트. **이 책 독자에게 가장 중요** |
| "PR #47292가 imagePlatform 문제를 고쳤다" | philwebb, 2025-11 (SNAPSHOT 검증까지만) | Spring Boot 릴리스 노트에서 실제 GA 버전 확인 |
| "Rancher Desktop 데이터 볼륨 기본 최대 100GiB" | jandubois, 2023-04 | Rancher Desktop 1.17.x 공식 문서 |
| "musl에 DNS-over-TCP가 추가됐다" | `_ikke_`, 2023-03 | musl 릴리스 노트 + Alpine 어느 버전부터 반영인지 |
| "JDK Alpine 이미지가 Java API의 부분집합만 지원" | huksley, 2023-03 (본인도 불확실 표시) | Eclipse Temurin/BellSoft 등 공식 문서. **틀릴 가능성 높음** |
| "OrbStack 상용 라이선스 $8/월" | 검색 요약(WebSearch)에만 등장, 원 페이지 미열람 | OrbStack 공식 가격 페이지 |
| "Docker Desktop 무료 조건 250인/$10M" | 검색 요약에만 등장 | Docker 공식 라이선스 페이지 |
| Docker Desktop "Use containerd image store" 옵션의 현재 기본값 | 미확인 | Docker Desktop 문서 / 직접 확인 |

**🔴 미해결·논쟁 중이라 단정 금지**
- docker/for-mac#7849의 원인(binfmt_misc 미등록)은 **메인테이너 가설**이며 이슈는 재현 불가로 종결됐다.
- docker/for-mac#7075, #7172는 **조회 시점 OPEN**이다. "해결됐다"고 쓰지 말 것.

**🌐 한국어 인용 상태**
- ✅ **velog @___pepper (일화 7) — 축자 인용 확보.** WebFetch에 "번역·요약 금지, 원문 그대로 출력"을 명시해 재수집했고 저자 오탈자까지 보존됐다. **그대로 따옴표에 넣어도 되는 유일한 한국어 출처.** 단 코드 블록은 재수집분에 누락 → 코드 인용 시 재확인.
- ⚠️ **velog @msung99, velog @cmsong111, OKKY 1085503, news.hada.io 16867 — 전부 WebFetch 요약 경유.** 따옴표로 옮기기 전 URL 재방문 필수. 같은 축자 요청 프롬프트(`번역하거나 요약하지 마라. 한국어 본문을 한 글자도 바꾸지 말고 그대로 출력하라`)를 쓰면 회수 가능하다 — 일화 7에서 실증됐다.
- ⛔ **내용 자체가 틀린 커뮤니티 주장 주의:** 일화 7의 "aws에서는 arm으로 빌드된 이미지를 실행할 수 없어서"는 2022-01 그 팀의 클러스터 사정이지 AWS 일반 사실이 아니다(Graviton arm64 인스턴스 존재). **인용은 하되 반드시 주석을 달 것.**

---

## 커버리지 자기평가

| 영역 | 등급 | 빠진 것 |
|------|------|--------|
| Apple Silicon `exec format error` 목격담 | **충분** | 2026년 사례가 "재현 불가"로 닫혀 현재 상태 판정이 애매 |
| arm64 빌드 → amd64 서버 사고담 | **충분** | 영문·한국어 양쪽 확보 |
| `--platform linux/amd64` 에뮬레이션 성능 (JVM·빌드) | **보통** | JVM 세그폴트·Next.js 빌드 사례는 확보. **Gradle/Maven 빌드 시간 비교 수치 없음** |
| Rosetta on/off 실사용 후기 | **충분** | 2023-11~2024-06 구간 집중. 2025~2026 최신 후기 없음 |
| 2021~22 전환기 vs 지금 | **충분** | 타임라인 표로 정리 |
| Paketo / bootBuildImage arm64 | **충분 (최강)** | 이슈 4건 본문·댓글 전문 확보, 4년 타임라인 완성. `pack`·`stacks` 쪽 이슈는 미열람 |
| Dockerfile로 갈아탄 이유 | **보통** | velog @cmsong111 1건 + `heruan` 대화. 더 많은 증언 필요 |
| Docker Desktop 라이선스 반응 | **보통** | Ask HN 2건 확보. **원 공지(2021-08-31) 대형 댓글 스레드 미열람**, OKKY 댓글은 로그인 벽 |
| 대안 런타임 이주 후기 (Colima/OrbStack/RD/Podman) | **충분** | OrbStack·Colima·Podman 실사용 증언 다수. Podman은 2021~22 것뿐 |
| 이주 후 깨진 것들 | **충분** | 체크리스트 H10으로 정리 |
| K8s "필요 없었다" 논쟁 (양쪽) | **충분** | 단 **2020년 스레드 중심**. 2024~2026 최신 논쟁 스레드는 빈약 |
| 손익분기점 구체 기준 | **보통** | 정성적 기준은 많으나 "서비스 N개/팀 M명" 같은 수치 기준은 못 찾음 |
| 로컬 K8s(kind/minikube/k3s) 선택 후기 | **부족** | 배터리·메모리 소모 비교 자료 없음. `nrvn`의 체감 1건뿐 |
| 볼륨 마운트 I/O 성능 | **보통** | 7~10년 열린 이슈 존재를 확인(강한 서사). **본문·수치 미확인** |
| 디스크 이미지 비대화 | **보통** | 이슈 목록 + Rancher Desktop VM 만땅 사례 1건. Docker Desktop 쪽 본문 미열람 |
| 메모리·발열·배터리 | **부족** | 이슈 제목 + 체감 증언 2건. 구체적 튜닝 실패담 없음 |
| Testcontainers 맥 문제 | **보통** | 소켓 문제는 충분. **"느려졌다"는 성능 증언 없음** |
| `latest` 태그 사고담 | **부족** | ⛔ **일화를 하나도 못 찾았다** |
| 베이스 이미지 업데이트 운영 실태 | **부족** | ⛔ **자료 없음** |
| 이미지 크기 줄이기 / Alpine | **보통** | Alpine 논쟁은 양쪽 확보. 크기 최적화 삽질담은 없음 |
| 취약점 스캔 알림 피로 | **부족** | ⛔ **자료 없음** |
| 한국 커뮤니티 | **보통** | velog 3 + OKKY 1(댓글 차단) + GeekNews 1. **그중 축자 인용 가능한 건 1건**(일화 7). 나머지 4건은 요약 경유. **커리어리 미접근, OKKY 댓글 미접근, 카카오/우아한형제들 기술블로그 댓글 미접근** |
| env_probe §4 짝 (런타임 2개 공존, PATH/context) | **보통** | 실패의 구조는 확보했으나 **맥 사례는 못 찾았고 확보된 건 Windows 사례다.** 반드시 명시할 것 |
| env_probe §5 짝 (잘못된 kubectl 컨텍스트) | **충분** | `millerm`의 Colima↔AWS 혼동 사고담이 정확히 일치 |

### 수집 한계 (정직한 기록)
- **미접근 플랫폼:** OKKY 댓글(로그인 필요), 커리어리, 개발자 Discord/Slack 공개 로그, Lobsters, Dev.to, Stack Overflow, X/Mastodon, 네이버 카페. 이번 세션에서 **시도하지 않았거나 접근하지 못했다.**
- **언어 편중:** 영어 출처가 압도적. 한국어는 5건이며 그중 원문 그대로 인용 가능한 건 사실상 0건(전부 WebFetch 요약 경유).
- **최신성 편중:** Paketo/bootBuildImage는 2022~2025로 잘 덮였으나, **K8s 도입 논쟁은 2020년, Alpine 논쟁은 2023년 자료다.** 6년·3년 된 논쟁을 2026년 책에 쓸 때는 반드시 시점을 명시하고, 가능하면 최신 재검색을 한 번 더 돌릴 것.
- **검색 도구 실패:** 없음. `gh`·HN Algolia API·WebFetch·WebSearch 모두 정상 동작했다. 다만 `gh issue list --json comments`가 1.2MB를 반환해 한 번 절단됐고, 해당 호출은 필드를 줄여 재실행했다.

---

## 신선도 원장

> **fact-checker 대조용 필수 표.** 이 문서에서 인용한 모든 페이지가 한 행씩 들어 있다. "게시 시점"은 API가 반환한 값 또는 페이지 표기값이며, 알 수 없으면 "미확인"으로 적었다.

| # | 주장/일화 | 출처 URL | 게시 시점 | 상태(조회 시점) | 검색 시점 | 신뢰도 |
|---|-----------|----------|-----------|------|-----------|--------|
| 1 | M4 맥에서 amd64 busybox조차 `exec format error`; binfmt_misc 가설 | https://github.com/docker/for-mac/issues/7849 | 2026-02-05 | CLOSED(재현불가, 2026-04-30) | 2026-07-25 | 🔴 단일 + 🟢 메인테이너 가설, **미해결** |
| 2 | 공장 초기화로 컨테이너·이미지·볼륨 전부 소실 (IJMacD) | 위 이슈 댓글 | 2026-02-25 | — | 2026-07-25 | 🔴 단일 익명 |
| 3 | Docker Desktop 4.27.1에서 QEMU 위 JVM `signal 11`; macOS 14.3으로 해결 | https://github.com/docker/for-mac/issues/7172 | 2024-02-05 | **OPEN** | 2026-07-25 | 🟡 다수 재현 + 🟢 Docker 엔지니어 확인 |
| 4 | Rosetta 켜고 amd64 빌드 33,656초; 끄고 5분 | https://github.com/docker/for-mac/issues/7075 | 2023-11-12 | **OPEN** | 2026-07-25 | 🟡 다수 재현 (M1/M2 Max/M3 Max/M3 Pro) |
| 5 | M1 Max GraalVM 네이티브 빌드 수시간 정체; Paketo 빌더가 amd64/QEMU | https://github.com/spring-projects/spring-boot/issues/33119 | 2022-11-13 | CLOSED | 2026-07-25 | 🔴 단일 + 🟢 위키 반영으로 확정 |
| 6 | "왜 이게 어디에도 안 적혀 있죠?" (JakobStadlhuber) | 위 이슈 댓글 | 2022-11-14 | — | 2026-07-25 | 🔴 단일 익명 |
| 7 | M1 bootBuildImage 산출물이 amd64 → arm64 클라우드 VM에서 `exec /cnb/process/web: exec format error` | https://github.com/paketo-buildpacks/spring-boot/issues/491 | 2024-06-21 | CLOSED | 2026-07-25 | 🔴 단일 + 🟢 메인테이너 처방 |
| 8 | 아키텍처 무시하는 빌드 캐시 → `ca-certificates-helper: exec format error` | 위 이슈 댓글 | 2024-06-21 | — | 2026-07-25 | 🟢 dmikusa (Paketo) |
| 9 | "pack도 spring-boot:build-image도 한 번에 멀티아키 못 만든다" | 위 이슈 댓글 | 2024-11-21 | — | 2026-07-25 | 🟢 dmikusa `(1차 소스 확인 필요)` |
| 10 | imagePlatform=amd64 시 "Image platform mismatch detected"; containerd 이미지 스토어 토글이 변수 | https://github.com/spring-projects/spring-boot/issues/46665 | 2025-08-04 | CLOSED | 2026-07-25 | 🟡 + 🟢 (philwebb 재현 검증) |
| 11 | "제목이 오해를 부른다 — arm64 호스트에서 amd64를 만들 때만" | 위 이슈 댓글 | 2025-08-04 | — | 2026-07-25 | 🟢 wilkinsona |
| 12 | containerd 이미지 스토어 on/off로 재현 여부 갈림 | 위 이슈 댓글 (hojooo) | 2025-10-23 | — | 2026-07-25 | 🔴 단일 + 🟢 philwebb 교차검증 |
| 13 | "Anything less any the builds seemed 'contaminated'" | 위 이슈 댓글 (jdnurmi) | 2025-09-04 | — | 2026-07-25 | 🔴 단일 익명 |
| 14 | Colima 이주 후 Testcontainers/Ryuk 소켓 실패; 두 변수 서로 다른 값 필요 | https://github.com/testcontainers/testcontainers-java/issues/5034 | 2022-02-08 | CLOSED | 2026-07-25 | 🟡 다수 재현 |
| 15 | `TESTCONTAINERS_RYUK_DISABLED=true`는 은폐다 | 위 이슈 댓글 (kiview) | 2022-02-11 | — | 2026-07-25 | 🟢 Testcontainers 메인테이너 |
| 16 | "2 for 2 on needing to delete the old socket and symlink Colima's" | https://github.com/abiosoft/colima/issues/365 | 2022-07-12 | **OPEN (4년째)** | 2026-07-25 | 🔴 단일 + 🟢 메인테이너 반론 |
| 17 | "many tools are indeed catching up and utilising docker context instead" | 위 이슈 댓글 (abiosoft) | 2022-07-14 | — | 2026-07-25 | 🟢 Colima 저자 |
| 18 | RD+DD 공존 시 context 미설정으로 모든 명령 실패 (**Windows 사례**) | https://github.com/rancher-sandbox/rancher-desktop/issues/7712 | 2024-11-01 | OPEN | 2026-07-25 | 🔴 단일, **플랫폼 불일치** |
| 19 | 호스트 120GB 여유인데 VM 데이터 볼륨 100% → factory-reset | https://github.com/rancher-sandbox/rancher-desktop/issues/4457 | 2023-04-14 | CLOSED | 2026-07-25 | 🔴 단일 + 🟢 jandubois |
| 20 | macOS Monterey에서 `Current context "rancher-desktop" is not found on the file system` | https://github.com/rancher-sandbox/rancher-desktop/issues/3350 | 2022-11-07 | OPEN | 2026-07-25 | 🔴 단일 익명 |
| 21 | PATH 주입이 "silent problems for any user"를 만든다 (**WSL 사례**) | https://github.com/rancher-sandbox/rancher-desktop/issues/10443 | 2026-06-11 | OPEN | 2026-07-25 | 🔴 단일, **플랫폼 불일치** |
| 22 | Docker.qcow2가 줄어들지 않음; "+1" 댓글에 👍349 | https://github.com/docker/for-mac/issues/371 | 2016-08-19 | CLOSED | 2026-07-25 | 🟡 (반응 수로 추정), **10년 전** |
| 23 | "Bind mounts are really slow" — 7년째 OPEN | https://github.com/docker/for-mac/issues/3677 | 2019-05-20 | **OPEN** | 2026-07-25 | 제목·상태만 확인 |
| 24 | K8s 도입 논쟁 (양쪽 전부) | https://news.ycombinator.com/item?id=22491170 | 2020-03-05 (719pt, 469 comments) | — | 2026-07-25 | 🔴 익명 다수, **6년 전** |
| 25 | "You Don't Need Kubernetes" 최신 스레드 (댓글 1개뿐) | https://news.ycombinator.com/item?id=48366913 | 2026-06-02 (6pt) | — | 2026-07-25 | 🔴 빈약 |
| 26 | 로컬 Colima인 줄 알고 운영 deployment 삭제 (millerm) | https://news.ycombinator.com/item?id=41578274 | 2024-09-18(스레드) / 댓글 2024-09-21 | — | 2026-07-25 | 🟡 다수 재현("나도 당했다" 5인) |
| 27 | OrbStack: Envoy 빌드 3~4시간 → 1시간 미만 (jchw) | https://news.ycombinator.com/item?id=41421846 | 2024-09-02 (307pt) | — | 2026-07-25 | 🔴 단일 체감 `(확인 필요)` |
| 28 | OrbStack 라이선스 서버 접속 불가로 정지 예고 (weikju) | 위 스레드 | 2024-09-02 | — | 2026-07-25 | 🔴 단일 익명 |
| 29 | OrbStack 8TB sparse image가 백업 소프트웨어를 깬다 (KingMob) | 위 스레드 | 2024-09-02 | — | 2026-07-25 | 🔴 단일 `(1차 소스 확인 필요)` |
| 30 | Colima는 배터리·CPU를 안 먹는다; OrbStack 비교표 부정확 (nrvn) | 위 스레드 | 2024-09-02 | — | 2026-07-25 | 🔴 단일 체감 |
| 31 | Docker Desktop 유료화 직후 "Podman 회의론" | https://news.ycombinator.com/item?id=28371788 | 2021-08-31 (47pt) | — | 2026-07-25 | 🔴 익명 |
| 32 | 유예 종료 직전 맥 대안 탐색; 조직 승인 성공/실패 양쪽 | https://news.ycombinator.com/item?id=29815122 | 2022-01-05 (22pt) | — | 2026-07-25 | 🔴 익명 |
| 33 | Docker 라이선스 공지 HN 제출 (**댓글 미열람**) | https://news.ycombinator.com/item?id=28368997 | 2021-08-31 (135pt) | — | 2026-07-25 | 제목·점수만 확인 |
| 34 | Alpine/musl 논쟁 (양쪽); JDK Alpine이 Java API 부분집합만 지원 주장 | https://news.ycombinator.com/item?id=35056594 | 2023-03-07 (34pt) | — | 2026-07-25 | 🔴 익명, **3년 전** `(확인 필요)` |
| 35 | musl에 DNS-over-TCP 추가됨 (_ikke_) | 위 스레드 | 2023-03-07 | — | 2026-07-25 | 🔴 익명 `(1차 소스 확인 필요)` |
| 36 | Kubesafe 도구 자체 | https://github.com/Telemaco019/kubesafe | 미확인(HN 제출 2024-09-18) | 미확인 | 2026-07-25 | 리포지토리 미열람 |
| 37 | M1 빌드 이미지가 EC2에서 플랫폼 불일치 경고 → `--platform linux/amd64`로 재빌드 | https://velog.io/@msung99/Docker-이미지-빌드-플랫폼-호환성-관련-에러-linuxamd64 | 2023-01-05 | — | 2026-07-25 | 🔴 단일 `(원문 대조 필요)` |
| 38 | 레지스트리엔 있는데 파드 실행 불가; entrypoint 권한으로 오진 → 동료 노트북(Intel)에선 성공 → `arch` 분기로 해결 | https://velog.io/@___pepper/Docker-M1-mac-이미지-배포-오류 | 2022-01-11 | — | 2026-07-25 | 🔴 단일 익명 / **인용문 축자 확보 ✅** (단 "aws는 arm 실행 불가" 주장은 사실 아님 — 주석 필수) |
| 39 | GitHub Actions x86 러너에서 ARM64 buildpack 빌드 실패 → 러너를 ARM으로; manifest 수동 생성 불편 | https://velog.io/@cmsong111/Spring-Boot-Native-Buildpack을-활용한-x86-ARM-네이티브-이미지-빌드-테스트-통합-태그-적용 | 2025-03-09 | — | 2026-07-25 | 🔴 단일 `(원문 대조 필요)` |
| 40 | "내년부터 도커 유료화하나요?" — Desktop/Hub 혼동, 상업화 실망 | https://okky.kr/articles/1085503 | **미확인**(페이지에 날짜 미노출) | 댓글 로그인 벽 | 2026-07-25 | 🔴 단일 `(원문 대조 필요)`, 댓글 미열람 |
| 41 | GeekNews "Docker Desktop 대안, Container Desktop"; 댓글에서 Podman 상태 문의 | https://news.hada.io/topic?id=16867 | 2024-09-21 / 댓글 2024-09-27 | — | 2026-07-25 | 🔴 단일 `(원문 대조 필요)` |
| 42 | Alpine이 Python Docker 빌드를 느리게·이미지를 크게 (**댓글 미열람**) | https://news.ycombinator.com/item?id=22182226 | 2020-01-29 (306pt, 149c) | — | 2026-07-25 | 제목·점수만 확인 |
