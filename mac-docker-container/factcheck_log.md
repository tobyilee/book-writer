# 팩트체크 로그 — 맥(Apple Silicon)에서의 Docker·컨테이너 심화서

**슬러그:** `mac-docker-container` / **genre:** `tech-book` / **게이트:** **BLOCKING**
**단일 append-only 파일.** 챕터별 샤딩 금지. 재검증은 같은 챕터 섹션에 새 라운드로 append한다.

## 판정 기호와 조치 규약

| 기호 | 의미 | 조치 |
|---|---|---|
| ✅ | 근거 파일과 일치 | 통과 |
| ⚠️ | 조건·시점·출처 표기 미흡 | 보강 (비블로킹) |
| ❌ | 근거와 충돌하거나 근거 없음 | **반드시 정정 (BLOCKING)** |
| 🕒 | 근거로 검증 불가 | 삭제·약화하거나 에스컬레이션 **(BLOCKING)** |

**❌/🕒 분기 규칙 (전 챕터 공통 적용):**
- 따옴표 안 축자 인용 문자열이 코퍼스에 **없으면 → ❌** (v1.8.0 하드블록: 근거 파일에 없는 인용은 지어낸 것으로 간주)
- 따옴표 없는 사실 주장이 코퍼스에 **없으면 → 🕒** (팩트체커의 기억으로 판정하지 않는다)
- 코퍼스에 **있으나 본문이 근거보다 넓게 주장하면 → ❌** (근거와 충돌)

**근거 별칭:** `W3`=`research/web_gapfill3.md` / `W2`=`web_gapfill2.md` / `W1`=`web_gapfill.md` / `W0`=`web.md` / `C2`=`community_gapfill.md` / `COMM`=`community.md` / `PAPER`=`papers.md` / `PROBE`=`env_probe.md` / `REF`=`01_reference.md`

---

## 1장. 나만 안 되는 이유가 있다

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/01_draft.md`
**집계:** ✅ 8 · ⚠️ 0 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 1-1 | "Docker로 여러 컨테이너를 띄워놨는데, Redis 컨테이너가 자주 꺼짐 / 다른 팀원들은 잘 동작하지만, 나만 꺼지는 상황" + "2025년 8월" | ✅ | `C2 §L-1` 축자 일치. velog @js03210, 게시 **2025-08-13** | — |
| 1-2 | "docker inspect 결과: `OOMKilled=true (exit=137)` → 메모리 부족(OOM Kill) 이 원인." | ✅ | `C2 §L-1` 축자 일치 | — |
| 1-3 | 2022년 1월 velog 인용 3건 — `chmod +x entrypoint.sh` 오진 / "차이점이라고는 코어의 차이(M1 or Intel)였는데, 설마 그게 문제일까하는 생각이 들기는 했다" / "문제 해결해 주신 리드님께 무한 감사,,,,😭" | ✅ | `COMM` 일화 4, `REF §3 A9`·`A10` 축자 일치. velog @___pepper, **2022-01-11** (축자 확보 등급) | — |
| 1-4 | "두 사람은 3년 반 차이가 나고" | ✅ | 2022-01-11 → 2025-08-13 = 3년 7개월. 근거 일치 | — |
| 1-5 | 국내 커뮤니티에 "도커 데스크톱 유료화·도커 허브 정책·도커 엔진을 한 덩어리로 묶어 질문한 글"이 있다 | ✅ | `REF §4-10` OKKY 1085503 — "글쓴이가 Docker Desktop 유료화 / Docker Hub 정책 / Docker Engine을 구분하지 못하고 있다". 코퍼스가 **날짜 미확인**으로 표시한 자료인데 본문이 날짜·축자를 쓰지 않고 현상만 서술 — 안전한 처리 | — |
| 1-6 | "Docker defaults to Docker Hub (docker.io)" (2026년 7월 조회 기준) | ✅ | `W3 §T4` 축자 — "**HOST** — Specifies the registry location where the image resides. **If omitted, Docker defaults to Docker Hub (docker.io).**" 본문의 "호스트를 생략하면"이 원문 "If omitted"와 정확히 대응 | — |
| 1-7 | "Docker Desktop 4.83.0의 릴리스 노트는 그 안에 Docker Engine v29.6.2가 들어 있다고 적고 있다(2026년 7월 조회 기준)" | ✅ | `W0 §A-3` / `REF §2-4` — 릴리스 노트 페이지 최상단 4.83.0(2026-07-20), Updates 목록에 "Docker Engine v29.6.2" 문서 표기 그대로. **1차 소스 귀속이 정확하다** — `PROBE`의 실측 데몬 버전(29.6.2)을 릴리스 노트 진술로 위장한 것이 아니라, 공개 릴리스 노트가 독립적으로 인쇄한 값을 인용했다 | — |
| 1-8 | "4.83.0과 29.6.2는 서로 다른 제품의 번호이지, 어느 쪽이 최신이라는 뜻이 아니다" | ✅ | **계획 §0-4 정정 13 정확 적용.** `REF §2-1` 경고("Desktop 제품 라인과 Engine 제품 라인은 모순이 아니라 다른 제품이다. 인용 시 어느 제품인지 반드시 명시")를 본문이 명시적 규율로 승격했다 | — |

**총평:** 1장에 사실 결함 없음. `PROBE` 값의 일반화(§0-2 금지)는 발생하지 않았고, 제품 라인 혼동(정정 13)도 없다. 오히려 정정 13을 독자용 규율로 명문화해 이후 장의 오보 위험을 낮췄다. §0-3 금지 항목(국내 사례 부재를 포지셔닝으로 쓰기)도 되살아나지 않았다.

---

## 2장. 컨테이너는 제품이 아니라 커널 기능이다

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/02_draft.md`
**집계:** ✅ 15 · ⚠️ 1 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 2-1 | "A namespace wraps a global system resource in an abstraction that makes it appear to the processes within the namespace that they have their own isolated instance of the global resource." — namespaces(7), Linux man-pages 6.18 (페이지 날짜 2026-02-08) | ✅ | `W0 §G-1` 축자 일치. 판본·페이지 날짜 표기까지 근거와 동일 | — |
| 2-2 | 네임스페이스 8종 표 (Cgroup/IPC/Network/Mount/PID/Time/User/UTS + `CLONE_*` 플래그 + 격리 대상) | ⚠️ | `W0 §G-1` 표와 8행 전부 일치. **단 Network 행의 원문은 "Network devices, stacks, ports, **etc.**"인데 본문이 "etc."를 떨어뜨려 목록이 닫힌 것처럼 읽힌다** | 보강: Network 행 격리 대상을 "Network devices, stacks, ports 등"으로 (한 단어) |
| 2-3 | "Control groups, usually referred to as cgroups, are a Linux kernel feature which allow processes to be organized into hierarchical groups whose usage of various types of resources can then be limited and monitored." — cgroups(7), 6.18 (2026-02-08) | ✅ | `W0 §G-2` 축자 일치 | — |
| 2-4 | cgroups v2 컨트롤러 9종 — `cpu`, `cpuset`, `freezer`, `hugetlb`, `io`, `memory`, `perf_event`, `pids`, `rdma` | ✅ | `W0 §G-2` 나열과 순서·항목 전부 일치 | — |
| 2-5 | "v1도 호환성 때문에 아직 남아 있는데, v2는 v1 컨트롤러의 부분집합만 구현한 상태"(man-pages 6.18 / 2026-02 기준) | ✅ | `W0 §G-2` 원문 2건 — "for compatibility reasons is unlikely to be removed" / "Currently, cgroups v2 implements only a subset of the controllers available in cgroups v1." 시점 병기 있음 | — |
| 2-6 | 네임스페이스 생성 비용 7.94ms(SSD, σ=2.05), 전체 기동의 1.5% 미만 — Khan, arXiv:2602.15214, **동료심사 미확인 프리프린트**, "2026년에 측정된" | ✅ | `PAPER` 논문 3 §4.2.1 축자 — "Namespace creation requires 7.94 ms (SSD, σ = 2.05) … contributing < 1.5% of total startup." 측정 연도 2026 · 프리프린트 단서 **둘 다 병기됨**(§0-2 요구 충족). arXiv ID `2602` = 2026-02로 빌드 시점(2026-07) 기준 **과거**이므로 미래 YYMM 자동 ❌ 규칙 비해당 | — |
| 2-7 | OCI — 매니페스트 미디어 타입 `application/vnd.oci.image.manifest.v1+json`, `schemaVersion`은 "MUST be `2` to ensure backward compatibility with older versions of Docker." | ✅ | `W0 §G-3` 축자 일치 | — |
| 2-8 | config `...image.config.v1+json` / layers는 descriptor 배열이며 **인덱스 0이 base layer** / digest는 SHA256 | ✅ | `W0 §G-3` — "layers: descriptor 배열, 인덱스 0이 base layer, 이후 stack order. digest는 SHA256" | — |
| 2-9 | 이미지 인덱스 `application/vnd.oci.image.index.v1+json`가 태그와 매니페스트 사이에 낀다 (그림 1 포함) | ✅ | `W0 §G-3`·`§E-2` — 실제 `imagetools inspect --raw` 응답에서 확인된 미디어 타입 | — |
| 2-10 | overlayfs 축자 2건 — "An overlay-filesystem tries to present…" / copy_up 문장 전문. 출처 표기 "(커널 버전 마커 미확인, 2026-07-25 열람)" | ✅ | `W2 §C-5` 축자 일치. 근거 파일이 "발행일/커널 버전 마커 미확인, 검색 2026-07-25"라 적은 것을 **본문이 그대로 승계** — 모범 처리 | — |
| 2-11 | "Docker의 스토리지 드라이버가 정확히 이 overlayfs로 구현된다는 연결은 커널 문서가 하지 않는다. 여기서는 개념적 대응까지만이다." | ✅ | `W2 §C-5` 라이더 및 **계획 2장 ⚠️ 라이더 준수**. 구현 동일시 회피 | — |
| 2-12 | Felter 축자 + "Felter et al., ISPASS 2015, p.172 (**2014년 측정**)" + "IBM 연구자 네 사람이 2014년에 측정하고 2015년에 발표" + "11년 전 논문" | ✅ | `PAPER` 논문 1 — 저자 4인(Wes Felter, Alexandre Ferreira, Ram Rajamony, Juan Rubio, **IBM Research, Austin TX**), ISPASS 2015 pp.171–172, 인용문 출처 p.172 §III, **측정 연도 2014(발표 2015)**. 2015→2026 = 11년 | — |
| 2-13 | "저자들이 문제 삼은 것은 리눅스 서버에서 굳이 VM을 끼우는 관행이고, 맥에서 VM은 선택이 아니라 전제다" | ✅ | 원문 "compared to deploying containers directly on non-virtualized Linux"의 정확한 독해. 논문 결론을 "맥에서 컨테이너를 쓰지 말라"로 확대하지 않음 | — |
| 2-14 | 비용 분해식 (`컨테이너 오버헤드 + VM 오버헤드 + 호스트↔게스트 경계`, 아래 화살표 주석 포함) | ✅ | `REF §1-3` 코드블록과 **축자 일치** | — |
| 2-15 | Lin 축자 + "Lin et al., ACSAC '18 (2018년 측정, Docker 17.09.1-ce 기준)" + 익스플로잇 223건/대표 88건/50건(56.82%)/11건 + "short board effect" + "패치된 커널의 값이 아니다" | ✅ | `PAPER` 논문 5 전부 일치. **측정 연도·런타임 버전·취약 커널 조건이 모두 병기**됐고 "오늘의 성공률로 읽으면 곤란하다"는 신선도 경고까지 본문에 있다(§0-2 요구 초과 충족) | — |
| 2-16 | Firecracker 축자 + "Agache et al., NSDI '20 Abstract" + "2020년 발표 시점 기준으로 내건 설계 목표치" 5MB/125ms/150개 + "전원 AWS" + "Rust로 최소 VMM" | ✅ | `PAPER` 논문 4 — 축자 일치, 저자 8인 전원 AWS, §1 p.419 "less than 5MB per container … less than 125ms … up to 150 MicroVMs per second per host". 근거 파일의 "이 역시 2020년 값" 경고를 본문이 **설계 목표치**로 정확히 한정 | — |
| 2-17 | dockershim — "Yes, the images produced from `docker build` will work with all CRI implementations. **All your existing images will still work exactly the same.**" + "쿠버네티스 공식 블로그가 2022년 2월에" + "제거는 Kubernetes 1.24에서 일어났다(2022년 발표 기준)" | ✅ | `W0 §F-2` — 두 문장이 **원문에서 연속**이다(스플라이스 아님). 블로그 발행일 2022-02-17 ✅. "The dockershim removal occurred in Kubernetes 1.24." 축자 ✅. 시점 병기 있음 | — |

**총평:** 2장은 이 배치에서 가장 근거 밀도가 높고 결함이 가장 적다. man-pages·OCI·커널 문서 축자 6건이 전부 근거 파일과 문자 단위로 일치했고, 논문 4편(Felter/Lin/Firecracker/Khan) 모두 **측정 연도 + 측정 환경 + 프리프린트 여부**가 병기됐다. dockershim 인용의 스플라이스 의심도 해소됐다(원문 연속). 유일한 지적은 표 한 칸의 "etc." 누락이며 비블로킹이다.

---

## 3장. Docker Desktop이 맥에서 실제로 하는 일

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/03_draft.md`
**집계:** ✅ 23 · ⚠️ 2 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 3-1 | 오프닝 — "바로 그 선택 때문에 amd64 빌드가 **몇 배로** 느려질 수 있다면" | ⚠️ | Docker 공식은 **정성 서술만** 한다("emulation of amd64 architectures is slow"). `REF §2-2`가 명시: "Rosetta 활성화 시 amd64 성능 수치는 공식 문서에 없다(미확인)". "몇 배"라는 배수 표현의 1차 근거가 없다 | 보강: "몇 배로" → "훨씬" 또는 "몇 시간씩" 류의 비배수 표현. (본문 뒤 소절이 커뮤니티 자기 보고임을 이미 명시하므로 오프닝만 조정하면 됨) |
| 3-2 | 설정 항목명 "Choose Virtual Machine Manager (VMM)" + 선택지 3종 (2026-07-25 열람 기준) | ✅ | `W0 §A-1` 축자 일치 | — |
| 3-3 | Docker VMM — "the latest and most performant Hypervisor/Virtual Machine Manager. This option is available only on Apple Silicon Macs and is in **Beta**." | ✅ | `W0 §A-1` / `REF §1-4` 축자 일치 (원문 "Select Docker VMM for the latest…"의 부분 인용, 의미 왜곡 없음) | — |
| 3-4 | Apple Virtualization framework — "A stable and well-established option for managing virtual machines on Mac" | ✅ | `W0 §A-1` 축자 일치 | — |
| 3-5 | "VMM 문서는 QEMU와 HyperKit을 legacy·deprecated로 표기한다" | ✅ | `W0 §A-1` / `REF §1-4` — "QEMU·HyperKit은 Legacy/deprecated로 표기" | — |
| 3-6 | "Use Rosetta for x86_64/amd64 emulation on Apple Silicon" 항목 + **기본값 Disabled** + "This option is only available if you have selected **Apple Virtualization framework** as the Virtual Machine Manager." | ✅ | `W0 §A-1` 축자 일치. 항목명·기본값·조건문 3요소 전부 | — |
| 3-7 | "Docker VMM does **not currently** support Rosetta, so emulation of amd64 architectures is slow." | ✅ | `W0 §A-1` 보강(docs.docker.com/desktop/features/vmm/) 축자 일치 | — |
| 3-8 | "'not currently'라는 단어도 기억해두자. 지금 시점의 상태라는 뜻이고, 이 관계는 바뀔 수 있다." | ✅ | 원문 단어에 근거한 신선도 경고. §0-2의 시점 규율에 부합 | — |
| 3-9 | Docker VMM "requires a minimum of 4GB of memory to be allocated to the Docker Linux VM" + "맥에 램이 4GB 있어야 한다는 말이 아니라, 그 리눅스 VM에 할당된 메모리" | ✅ | `W0 §A-1` 축자 일치. 해석도 원문 "allocated to the Docker Linux VM"의 정확한 독해 | — |
| 3-10 | **"기본으로 잡히는 VMM은 무엇일까? 모른다. 공식 문서에서 확인하지 못했다."** | ✅ | `W0 §A-1` — "**기본 선택이 무엇인지는 이 페이지에서 확인 못 함(미확인).**" **계획 3장 ⚠️("기본 VMM은 X다라고 쓰지 말 것") 정확히 준수.** 모범 처리 | — |
| 3-11 | "Choose file sharing implementation for your containers" + VirtioFS(기본)/gRPC FUSE | ✅ | `W0 §A-1` 축자 일치 | — |
| 3-12 | "VirtioFS has reduced the time taken to complete filesystem operations by up to 98%." + **"무엇 대비 98%인지가 안 적혀 있다 … 우리가 아는 것은 Docker 공식 문서가 그렇게 적어두었다는 사실까지다"** | ✅ | `W0 §A-1` 축자 일치. 벤더 주장을 저자 목소리로 승격하지 않고 **주장의 출처성 자체를 논지로 삼은** 모범 처리 | — |
| 3-13 | "It is the only file sharing implementation supported by Docker VMM." | ✅ | `W0 §A-1` 축자 일치 | — |
| 3-14 | "Certain databases, like MongoDB and Cassandra, may fail when using virtiofs with Docker VMM." | ✅ | `W0 §A-1` 축자 일치 | — |
| 3-15 | `docker/for-mac#7075` — 2023-11 등록, **2026-07-25 조회 시점 OPEN**, M2 Max 맥북 프로, Rosetta **켠** 상태 amd64 빌드 | ✅ | `COMM` 일화 3 / `REF §2-2` — 2023-11-12 등록, 조회 시점 OPEN, "M2 Max 맥북 프로 사용자 `a6z6`", "Use Rosetta … 켠 상태" 전부 일치 | — |
| 3-16 | 빌드 로그 `[+] Building 33656.6s (15/22)` / `=> [builder 5/5] RUN yarn build 33186.8s` + "약 9시간 21분" | ✅ | `REF §2-2` 코드블록과 축자 일치(원문 로그의 발췌형이며 `REF`가 이미 이 형태로 승인). 33,656.6s ÷ 3600 = 9시간 20.9분 | — |
| 3-17 | "이 숫자 자체는 벤치마크가 아니다 — 한 사람의 한 환경, 한 워크로드에서 나온 자기 보고다. 'Rosetta를 켜면 9시간이 걸린다'고 읽으면 안 된다." | ✅ | **§0-2 커뮤니티 자기 보고 규율 준수.** `REF §2-2`의 "커뮤니티 수치(33,656초)는 한 사람의 한 환경이며 벤치마크가 아니다"를 본문이 명시 | — |
| 3-18 | "같은 증상은 M1·M2 Max·M3 Max·M3 Pro에 걸쳐 2023년 11월부터 2024년 6월까지 반복 보고됐고" | ✅ | `COMM` 일화 3 신뢰도란 — "🟡 다수 재현 (M1/M2 Max/M3 Max/M3 Pro, 2023-11 ~ 2024-06)" 축자 일치 | — |
| 3-19 | "`AlexandreRoba`(M3 Max 64GB)는 **껐더니 5분** 만에 빌드가 끝났다고 적었다" | ⚠️ | `COMM` 일화 3 원문: "Same here **downgraded to 4.24.2** and unchecked `Use Roseta..` in order to build a very simple next app on an apple M3 Max with 64GB in more than 5 minutes." 그가 취한 조치는 **버전 다운그레이드 + Rosetta 끄기 두 가지**인데 본문은 Rosetta 끄기 단독 효과로 읽힌다. (`REF §2-2`도 같은 축약을 하나, 본문은 이 값을 "껐더니"의 대조 증거로 쓰므로 조건 하나가 더 필요하다) | 보강: "(4.24.2로 내리고 함께 껐다)" 한 구절 추가 |
| 3-20 | `alnaranjo` 축자 — "Using 4.25.x would cause docker build to hang indefinitely even when disabling 'use rosetta'. **Building arm images is a breeze, though.**" | ✅ | `COMM` 일화 3 / `REF §2-2` 축자 일치 | — |
| 3-21 | "이 이슈는 한 번 닫힌 적이 있다. Docker 쪽에서 특정 버전을 제안했고 실제로 해결된 사용자가 있었다." | ✅ | `COMM` 일화 3 결말 — 메인테이너 `dgageot`가 2023-12-06 4.26.0 제안, 해결된 사용자(`djcristi`) 있음. 버전 숫자를 본문에서 단정하지 않은 것도 안전 | — |
| 3-22 | "why is this closed? I think the issue persists for latest macbook users" — `jinmel`, 2024-06-29 | ✅ | `REF §2-2` 축자·발화자·날짜 일치 | — |
| 3-23 | "4.30·4.31에서도 같은 증상 보고가 올라왔으며, 2026-07-25에 조회한 시점에 이슈는 **다시 열려 있다**" | ✅ | `COMM` — `oming`(2024-06-24, M3 Pro) "docker 4.31.0", `COMM §요약표` "4.30/4.31에서도 끄고 씀(`oming`)", "2026-07-25 조회 시점 이슈 상태는 `OPEN`이다" | — |
| 3-24 | "**'Rosetta를 켜면 빨라진다'도, '그 문제는 이제 해결됐다'도** [쓰지 않는다]" | ✅ | **계획 3장 ⛔ 둘 다 금지 준수.** `REF §2-2` ⛔ 결론과 일치 | — |
| 3-25 | `p0w3n3d` — Podman + Rosetta + `eclipse-temurin:25-jdk-ubi10-minimal` + 스프링 부트, `podman run 0.02s user 0.01s system 0% cpu 24.960 total`, "2026년 2월", "같은 사람이 바로 앞에서 '내 머신에서 podman과 docker 사이에 차이가 없다'고 스스로 번복한 뒤" | ✅ | `C2 §C-4-a` 축자 일치(2026-02-26 후속 댓글). 이미지 태그 문자열·시간값·자기 번복 맥락 전부 근거에 있음. **"런타임 비교로 읽으면 안 된다 / 한 사용자의 자기 보고"** 명시 — 계획 3장 요구 충족 | — |
| 3-26 | 라이선스 축자 — "Small businesses (**fewer than 250 employees AND less than $10 million in annual revenue**)" | ✅ | `W0 §A-2` / `REF §4-6` 축자 **문자 단위 일치**. 출처 `docs.docker.com/subscription/desktop-license/`, 2026-07-25 열람, **발행일 미확인**까지 근거 파일과 동일하게 표기 | — |
| 3-27 | "Professional use in larger organizations"·"Government entities"에는 유료 구독이 필요하다 | ✅ | `W0 §A-2` — "그 외 'Professional use in larger organizations', 'Government entities'는 유료 구독 필요" 축자 일치 | — |
| 3-28 | **AND 조건 / 250명 "미만" / 1,000만 달러 "미만" / 둘 중 하나만 넘어도 무료 범위 밖 / 개인이 아니라 조직 / 대상은 Docker Desktop 제품** | ✅ | "fewer than"·"less than" → **미만**이 정확한 번역(이하 아님). (A AND B)의 부정 = "둘 중 하나만 넘어도 밖" — **논리 정확**. `W0 §A-2` 표기 권장문("AND 조건임에 주의 — 한쪽만 넘어도 유료다")과 일치. 임계값 주어가 employees/annual revenue이므로 조직 단위 ✅. 라이선스 페이지가 `subscription/desktop-license/`이므로 대상 제품도 정확 | — |
| 3-29 | "이 책이 옮긴 것은 2026년 7월 25일에 그 페이지가 그렇게 적혀 있었다는 사실 하나다. … 공식 라이선스 페이지를 직접 열어 그날의 문구로 확인하는 편이 낫다." | ✅ | 돈이 걸린 사실에 **조회 일자를 못 박고 독자에게 재확인을 요구**했다. §0-2 시점 규율 초과 충족 | — |
| 3-30 | `ifwinterco`(2026-07-02) "Docker CLI is free for commercial use, it's only docker desktop you have to pay for" / `pjmlp`(2026-07-02) "…**no docker of any kind being installed from https://www.docker.com.**" + "앞의 말은 공식 문서의 서술이 아니라 한 사용자의 발언이라는 점을 분명히 해두자" | ✅ | `C2 §C-1` 축자 일치. 스레드 HN 48762098, **제출 2026-07-02** ✅. `pjmlp` 인용은 원문의 문장 경계에서 끊겼다(무단 절단 아님). **커뮤니티 발언을 저자 목소리의 단정으로 승격하지 않고 명시적으로 격하** — §0-2 준수 모범. 참고: `C2` 결산표(802행)가 같은 자료를 "2026-02"로 적었으나 `§C-1` 본문 기록(2026-07-02)이 1차이며 본문은 옳은 쪽을 채택 | — |
| 3-31 | `yuppie_scum`(비용 승인 성공) / `pseudoramble` 축자 "Ah man, that must be a magical place. **I spent months (on-and-off) trying to convince my company to do this and failed.** ... it genuinely worries me that while **IT considers it unapproved software** that it won't stop its usage." + "4년 앞선 2022년 1월의 스레드" | ✅ | `COMM §3-1` / `REF §4-10` 축자 일치. HN 29815122, **2022-01-05** ✅. 2022-01 → 2026-07 = 4년 6개월, "4년 앞선" 성립 | — |
| 3-32 | 리소스 기본값 — 메모리 "Defaults to 50% of your host's memory.", 스왑 "1 GB default", "Include VM in Time Machine backups" 기본 Disabled | ✅ | `W0 §A-1` 축자 일치 | — |

**총평:** 3장의 최대 위험 지점이었던 **라이선스 조건은 결함이 없다.** 축자·AND 관계·"미만" 번역·조직 단위·제품 단위·조회 시점이 전부 정확하고, 커뮤니티 발언을 1차 소스와 명시적으로 분리했다. **"기본 VMM은 모른다"**는 계획이 지정한 미확인 자리를 그대로 비워둔 모범 사례다. Rosetta 소절도 계획 ⛔("켜면 빨라진다"·"해결됐다" 둘 다 금지)를 지켰다. ⚠️ 2건은 모두 배수 표현·조건 1개 누락이며 비블로킹이다.

---

## 4장. 6GB를 주랬더니 11.5GB를 쓴다

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/04_draft.md`
**집계:** ✅ 24 · ⚠️ 2 · **❌ 1** · **🕒 1**

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 4-1 | "Same here, set Docker Desktop to use 6 GB of RAM, instead it uses 11,5 GB. Using Docker VMM." — `bastibense`, Docker Desktop 4.44.3 / Docker VMM. 이슈 `docker/for-mac#7749`("com.docker.krun using insane amount of memory", 2025년 8월 21일 등록, **2026년 7월 25일 조회 시점 OPEN**) | ✅ | `C2 §D-1` — 축자·발화자·환경(4.44.3 / Docker VMM)·이슈 제목·등록일(2025-08-21)·조회 시점 OPEN **6요소 전부 일치** | — |
| 4-2 | "today I had 122 GB RAM usage for a container that usually took up like 200 MB." + "한 사용자가 자기 화면에서 본 것을 적은 것이지 측정된 벤치마크가 아니다" | ✅ | `C2 §D-1` 축자 일치. **§0-2 커뮤니티 자기 보고 규율 준수** | — |
| 4-3 | 메모리 "Defaults to 50% of your host's memory.", 스왑 "1 GB default", CPU·디스크 이미지 위치 조정 가능, Time Machine 기본 Disabled (2026년 7월 검색 기준) | ✅ | `W0 §A-1` 축자 일치, 시점 병기 있음 | — |
| 4-4 | "Docker VMM requires a minimum of 4GB of memory to be allocated to the Docker Linux VM." → "메모리는 'Docker 리눅스 VM에 할당'된다" | ✅ | `W0 §A-1` 축자 일치. 슬라이더가 컨테이너가 아니라 VM에 걸린다는 해석의 근거로 정확 | — |
| 4-5 | `YoannD42`(Docker Desktop 4.45.0 / Docker VMM) — 40GB, 컨테이너 **하나**만 몇 시간, 재시작해야만 메모리 반환 | ✅ | `C2 §D-1` 축자 — "it went up to 40GB on our macs with colleagues … just need to let even A container run, for a few hours … Only releases memory, when restarting docker desktop." 환경 표기도 일치 | — |
| 4-6 | `VikiAnn` — 밤새 재부팅 후 도커 미실행인데 `com.docker.krun`이 "almost 140 GB memory and like 668% CPU" | ✅ | `C2 §D-1` 축자 일치. 도커 미실행 정황도 원문에 있음 | — |
| 4-7 | `Fail-Safe` — "I notice my MacBook M3 machine getting noticeably warm, which is rare. CPU usage stays constant at ~200%" | ✅ | `C2 §D-1` 축자 일치 | — |
| 4-8 | **"이 증언들은 전부 Docker Desktop 자체에 대한 것이다."** | ✅ | **§0-3 금지("로컬 K8s의 배터리·발열 비교") 경계를 본문이 스스로 명시했다.** `C2 §D-1` 주의문("로컬 K8s가 아니라 Docker Desktop 자체에 대한 것이다. 혼동해서 쓰지 말 것") 준수 — 모범 | — |
| 4-9 | `djs55` 축자 — "The current theory is that the memory is being miscounted by the 'footprint' metric … the VM is signalling free memory to the host and macOS is informed with `madvise` … that it can drop the contents, but the footprint metric doesn't currently reflect that reliably." | ✅ | `C2 §D-1` 축자. **스플라이스 검사 통과** — 첫 `…`는 "(the one labelled 'Memory' in Activity Monitor), leading to the process appear to leak over time. In practice"를 정당하게 생략했고(본문이 그 내용을 한국어 삽입구로 복원), 둘째 `…`는 **원문 자체에 이미 있는 말줄임**이다. 없는 문장을 이어 붙인 곳 없음 | — |
| 4-10 | `YoannD42` 반박 — 풋프린트 45GB / 실제 메모리 7.2GB / 컨테이너 5.3GB + "Nonetheless, the mac displays memory pressure in red, things get in swap" + 컨트리뷰터 재답변 "This is a definite possibility." | ✅ | `C2 §D-1` 축자·수치 3개 전부 일치 | — |
| 4-11 | "이 이슈는 조회 시점에 여전히 열려 있고 원인은 규명 중이다. … 결론이 나지 않았다." | ✅ | **`C2 §D-1` 📌 fact-checker 주의("'이건 버그다'로 단정하지 말 것. 컨트리뷰터 가설과 사용자 반박을 양쪽 다 적을 것") 정확히 준수.** 계획 4장 ⛔ 충족 | — |
| 4-12 | velog @js03210, 2025-08-13 + "다른 팀원들은 잘 동작하지만 나만 꺼지는" + `OOMKilled=true (exit=137)` 축자 | ✅ | `C2 §L-1` 축자·날짜 일치 | — |
| 4-13 | "글쓴이는 원인을 **'Docker VM에서 사용 가능한 메모리가 적어서'**라고 적었다" | ✅ | `C2 §L-1` 원문 — "**Docker VM에서 사용 가능한 메모리가 적어서 Redis가 죽음**" 축자 일치 | — |
| 4-14 | **2GB vs 50% 충돌 처리** — "글쓴이는 자기 Docker Desktop 메모리 설정이 '기본값(2GB)'이었고 … 그런데 앞에서 본 공식 문서의 기본값은 호스트 메모리의 50%다(2026년 7월 검색 기준). 두 값이 왜 다른지는 이 책이 확인하지 못했다." | ✅ | `C2 §L-1` 원문("나: 기본값(2GB)으로 설정")을 **글쓴이 진술로만 귀속**하고, 1차 소스 값(50%, `W0 §A-1`)을 나란히 제시한 뒤 **불일치를 미해소로 선언**했다. 커뮤니티 값을 기본값으로 단정하지 않음 — **§0-2 증거 능력 규칙의 모범 적용** | — |
| 4-15 | Redis 사례이며 스프링 부트로 옮기지 않음 | ✅ | **§0-3 금지("스프링 부트 컨테이너 OOMKilled 일화") 준수.** `C2 §L-1` 한계 주석과 일치 | — |
| 4-16 | `cdrage`(Podman Desktop 팀, 2026년 2월 25일 HN) — Docker Desktop 기본 램 50% + CPU 최대치 / Podman Desktop 기본 램 4GB + CPU 50% | ✅ | `C2 §C-4-b` 축자 일치. 스레드 HN 47151163, 2026-02-25 ✅ | — |
| 4-17 | `p0w3n3d` 반증 — "Podman에 8GB를 줘도 속도가 안 오르고, Docker는 4GB로도 여전히 9초" + "⚠️ 이 초 단위 수치는 한 사용자가 자기 맥에서 재본 자기 보고다 … 벤치마크로 읽으면 안 된다" | ✅ | `C2 §C-4-b` 축자 일치. **§0-2 자기 보고 규율 준수** | — |
| 4-18 | `Stargator` 축자 — "My HD has 120 GB free, so I don't understand the 'No space left on device'" | ⚠️ | `COMM` 일화 11 원문은 **"…the 'No space left on device' nor the references to `nerdctl`."** 문장 중간에서 말줄임 표기 없이 끊고 닫는 따옴표를 붙였다. 의미 왜곡은 없으나 축자 인용의 완결성 표기가 빠졌다 | 보강: 인용 끝에 `…` 추가하거나 후반절 복원 |
| 4-19 | `jandubois` 축자 — "You may be out of space inside the VM. The data volume has a default maximum size of 100GiB." | ⚠️ | `COMM` 일화 11 원문은 "…default maximum size of 100GiB**, so if you created/pulled a lot of images, it may be full.**" 본문이 **쉼표를 마침표로 바꾸고** 후반절을 잘랐다. 발화자·진단 내용은 정확 | 보강: "…of 100GiB…"로 말줄임 표기하거나 후반절 복원 |
| 4-20 | `rdctl shell df -h /mnt/data` 출력 — `97.9G / 93.1G / 0 / 100% /mnt/data` | ✅ | `COMM` 일화 11 / `REF §3 A15` 코드블록 축자 일치 | — |
| 4-21 | 이슈 `rancher-sandbox/rancher-desktop#4457`, 2023년 4월 14일, **CLOSED**, 결말은 `rdctl factory-reset` | ✅ | `COMM` 일화 11 / `REF §신선도 원장` — 2023-04-14 / CLOSED, 결말 factory-reset 일치 | — |
| 4-22 | **"(100GiB라는 기본값은 2023년 4월 시점 메인테이너의 발언이다. 지금 쓰는 버전의 기본값은 공식 문서로 다시 확인하는 편이 낫다. (사실 확인 필요))"** | **🕒** | `REF §신선도 원장` 1731행이 이 값을 **`(1차 소스 확인 필요)`**로 표시했고, `COMM` 일화 11도 "100GiB 기본값은 2023-04 시점 메인테이너 발언. 현재 Rancher Desktop 1.17.x의 기본값은 공식 문서 확인"이라 적었다. **코퍼스에 1차 소스가 없어 값 자체는 검증 불가.** 다만 본문은 이미 **시점·발화자·재확인 권고를 병기해 약화**를 완료한 상태다 | **마커 처리: 본문의 헤지 문장은 그대로 유지하고 `(사실 확인 필요)` 문자열만 삭제.** 판정 근거는 이 로그 행이 보존한다. 최종본에 마커 잔존 금지 |
| 4-23 | `docker/for-mac#7517` "Simple Way to Shrink Docker.raw Disk"(2025-01-02 등록, CLOSED) + `bsousaa` 축자 "closing as duplicate of https://github.com/docker/roadmap/issues/771" + **"그 로드맵 이슈의 내용까지는 이 책이 확인하지 않았으므로 해석은 여기서 멈추자"** | ✅ | `C2 §D-2` — 이슈 번호·제목·날짜·상태·유일한 댓글 축자 전부 일치. **근거 파일이 "그 로드맵 이슈는 열지 않았다"고 적은 한계를 본문이 그대로 승계** — 계획 4장 "해석 붙이지 말 것" 준수 모범 | — |
| 4-24 | `--cpus=0.5` 실측 — 평균 **71.63%**, 표준편차 **36.14**, 이상치 최대 **247%** (macOS Docker Desktop) | ✅ | `PAPER` 논문 3 §4.2.2 — "macOS μ=71.63% (σ=36.14), 이상치 최대 247%" 축자 일치 | — |
| 4-25 | "two-level scheduling (macOS → LinuxKit → CFS) produces compounding inaccuracy." | ✅ | `PAPER` 논문 3 §4.2.2 축자(원문 문장의 후반부 발췌, 계획 4장이 지정한 인용 형태와 동일) | — |
| 4-26 | 기동 시간 변동계수 macOS **32.8%**, 같은 실험 SSD **3.4%** | ✅ | `PAPER` 논문 3 §4.1.2 — SSD 3.4% / HDD 8.3% / macOS 32.8%. **계획 4장이 명시적으로 지정한 조합**이며, 무차원 분산 지표라 §35의 "티어 간 절대값 비교 금지"에 저촉되지 않음 | — |
| 4-27 | 페이지 캐시 공유 효율 약 0% + "three identical nginx containers consume 3× the memory of one" 축자 | ✅ | `PAPER` 논문 3 §4.3.3 축자 일치 | — |
| 4-28 | **"리눅스에서라면 공유돼 아껴졌을 메모리가 여기서는 그냥 세 배로 붙는다."** | **❌** | **근거와 정면 충돌.** `PAPER` §4.3.3 원문은 **"Page cache sharing efficiency is approximately 0% <ins>across all platforms</ins>: three identical nginx containers consume 3× the memory of one."** — 페이지 캐시 미공유는 **모든 플랫폼(SSD·HDD·macOS) 공통 관측**이지 맥 고유 현상이 **아니다.** 본문은 이 문장을 "맥에서는 CPU 제한이 잘 안 먹는다" 소절 안에 놓고 리눅스 대비 열위로 재서술해, 논문이 하지 않은 대조를 만들었다. 계획 4장 ⛔ **"티어 간 절대값 비교 금지"** 및 저자 본인 고지("macOS 결과는 개발자 환경을 특징짓기 위한 것이지 아키텍처 비교가 아니다") 위반 | **정정문(택1) — ① 권장:**<br>**① 삭제** — 앞 문장(축자 인용)까지만 두고 마지막 한 문장을 뺀다. 이 소절은 세 줄 뒤에 "티어 간 비교 금지"를 스스로 고지하므로, 비(非)맥 플랫폼 이야기를 아예 들이지 않는 쪽이 가장 안전하다.<br>**② 교체(대안)** — "리눅스에서라면 공유돼 아껴졌을 메모리가 여기서는 그냥 세 배로 붙는다." → **"흥미롭게도 이건 맥만의 일이 아니다. 논문은 이 0%가 측정한 모든 플랫폼에서 똑같이 나타났다고 적는다 — 컨테이너를 여러 개 띄우면 메모리는 그 수만큼 곱해서 든다고 보는 편이 안전하다."** ⛔ 대체 문장에서 플랫폼 **개수를 세지 말 것**("세 환경" 등) — 논문 축자는 "across all platforms"까지이고 그 열거는 코퍼스에 없다 |
| 4-29 | "**arXiv:2602.15214(Khan, 2026)이며 단독 저자의 프리프린트다.** 동료 심사 여부는 확인되지 않았다." + 저자 고지("macOS 결과는 개발자 환경을 특징짓기 위한 것이지 클라우드 CPU와의 아키텍처 비교가 아니다") + "'맥이 클라우드보다 부정확하다'로 옮겨 적으면 저자가 하지 않은 말을 하는 셈" | ✅ | `REF §참고문헌 3` — "arXiv:2602.15214 (2026-02-16, **단독 저자**, 동료심사 미확인)". **§0-2 프리프린트 단서 요구 충족.** arXiv ID `2602`(2026-02)는 빌드 시점(2026-07) 기준 과거이므로 미래 YYMM 자동 ❌ 규칙 비해당 | — |
| 4-30 | "JVM은 … `-XX:ActiveProcessorCount` 옵션이 왜 필요한지가 여기서 반쯤 설명된다" (8장 예고) | ✅ | `W0 §E` / `REF §5-4`에 `-XX:ActiveProcessorCount` 공식 문서 근거 있음. 예고 수준의 서술로 과잉 주장 없음 | — |

**총평:** 4장의 커뮤니티 자기 보고 수치(6GB→11.5GB, 122GB, 40GB, 140GB·668%, ~200%, 4GB·8GB·9초)는 **전부 "누가 언제 어떤 환경에서 보고했다" 형태로 귀속됐고 벤치마크가 아님이 명시**됐다 — §0-2 요구 충족. 2GB vs 50% 충돌 처리와 로드맵 이슈 절제도 모범이다. **단 하나, 페이지 캐시 0%를 맥 고유 현상으로 재서술한 4-28이 근거와 충돌하며 BLOCKING이다.** 100GiB 마커(4-22)는 이미 약화가 완료돼 마커 문자열 삭제만 남았다.

---

## 배치 종합 (1~4장, 라운드 1)

| 챕터 | ✅ | ⚠️ | ❌ | 🕒 |
|---|---|---|---|---|
| 1장 | 8 | 0 | 0 | 0 |
| 2장 | 15 | 1 | 0 | 0 |
| 3장 | 23 | 2 | 0 | 0 |
| 4장 | 24 | 2 | **1** | **1** |
| **합계** | **70** | **5** | **1** | **1** |

**BLOCKING 항목 2건:** 4-28(❌ 페이지 캐시 0%의 플랫폼 한정 오류) · 4-22(🕒 `(사실 확인 필요)` 마커 제거).
이 2건이 해소되기 전에는 Phase 5(EPUB 빌드)로 넘어갈 수 없다.

**웹 2차 에스컬레이션:** 0건. 모든 Critical 주장이 레퍼런스 코퍼스 1차 대조로 판정됐다. 의심 식별자(형식 이례 arXiv ID·미해결 DOI/URL·검증 불가 인용)는 발견되지 않았다.

**계획 §0-4 사실 정정 13건 대조:** 1~4장에 배정된 것은 **정정 13(Desktop 4.x / Engine 29.x 제품 라인 구분)** 뿐이며, 1장이 이를 준수했을 뿐 아니라 독자용 규율로 명문화했다. 나머지 12건은 5·7·8·11·12장 배정분으로 이 배치의 검증 범위 밖이다. **위반 0건.**

**계획 §0-3 금지 목록 대조:** 로컬 K8s 배터리·발열(4장이 경계를 명시), 스프링 부트 OOMKilled(4장이 Redis로 유지), 이미지 스캔 알림 피로, 베이스 갱신 주기, rootless, 볼륨 마운트 성능 수치, macOS `.docker/config.json` 경로, Colima "k3s 기반" 호칭 — **전부 되살아나지 않음.**

**`PROBE` 일반화 검사:** "Docker 최신 버전은 29.6.2다" 류 0건. 1장의 4.83.0/29.6.2 언급은 공개 릴리스 노트 인용이며 실측 위장이 아니다.

**사실 판정 아님 — 인계 메모 (저술가·editor용, 비블로킹):** `04_draft.md` 55행·94행이 **독자에게 보이는 본문에 리터럴 `⚠️` 글리프**를 달고 있다. 내용은 정확한 조건 고지이므로 사실 결함이 아니지만, Phase 4.5의 잔존 마커 스캔이 편집 마커로 오탐할 수 있다. 처리 여부는 style-guardian·editor 소관이며 팩트체커의 판정 대상이 아니다.


## 라운드 2 추가 규약 (5~8장부터 적용)

**명령·코드 블록 판정 규칙 (신설 — 7장의 축자 명령 약 20줄을 일관되게 판정하기 위해):**
- 코퍼스에 **축자로 존재** → ✅
- 축자는 없으나 **문서의 Usage·문법 축자를 그대로 인스턴스화**한 것(플레이스홀더 치환 포함) → ✅
- 문법 근거 없이 옵션·값·출력이 등장 → 🕒
- 문법·옵션명이 **한 글자라도 어긋남** → ❌

**파일 우선순위 대조 축 (신설 — 오케스트레이터 지시, 2장 "digest는 SHA256" 오류 유형):**
축자 대조와 **별개로**, 근거가 1차 라운드 파일(`W0`·`COMM`)이면 같은 주제가 보강 파일(`W1`·`W2`·`W3`·`C2`)에 재등장하는지 확인한다. 재등장하면 **보강 쪽이 유효 판정**이다(계획 §0-1). 뒤에 온 파일이 앞을 교체했는데 본문이 앞을 옮겼으면 → **❌**, 로그에 `근거: {새 파일}이 {옛 파일}을 교체` 형태로 명시한다.

---

## 5장. 무엇이 실행되고, 어디에 붙는가

**검증:** 2026-07-26 / 라운드 1(5~8장 배치의 첫 라운드) / 대상 `chapters/05_draft.md`
**집계:** ✅ 31 · ⚠️ 1 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 5-1 | 오프닝 실측 2블록 — `Docker version 27.5.0-rd, build 7a37716` / `29.6.2 / Docker Desktop / aarch64` + "이 책을 쓴 맥에서 2026년 7월 25일에" | ✅ | `PROBE §3`·`§4` 출력 블록과 **문자 단위 일치**. 측정 시점 2026-07-25도 파일 헤더와 동일 | — |
| 5-2 | "(표본은 하나다. 다른 맥의 기본 상태가 이렇다는 뜻이 아니라, 런타임을 둘 깔면 이런 조합이 만들어질 수 있다는 증거로만 읽자.)" | ✅ | **`PROBE` 사용 규칙("표본 1, 일반화 금지") 준수.** §0-2의 `PROBE` 규율 충족 | — |
| 5-3 | `command -v docker` → `/Users/tobylee/.rd/bin/docker` | ✅ | `PROBE §4` 축자 일치 | — |
| 5-4 | "`~/.rd/bin` … 같은 자리에 `docker-buildx`·`docker-compose`·`nerdctl`·`rdctl`·`kubectl`·`helm`이 함께 들어 있다" | ✅ | `PROBE §6` `ls ~/.rd/bin` 출력에 6개 전부 존재(`kuberlr`·`spin`·`docker-credential-*`는 생략 — 누락일 뿐 오기 아님) | — |
| 5-5 | `docker context ls` 출력 2행 전문(`default` / `desktop-linux *`) | ✅ | `PROBE §4` 축자 일치 | — |
| 5-6 | "`echo $DOCKER_HOST`를 쳐보니 이 맥에서는 아무것도 나오지 않았다" | ✅ | `PROBE §4` — `echo "${DOCKER_HOST:-(unset)}"` → `(unset)`. unset의 정확한 서술 | — |
| 5-7 | "all `docker` commands run against this context, unless overridden with environment variables such as `DOCKER_HOST` and `DOCKER_CONTEXT`, or on the command-line with the `--context` and `--host` flags." | ✅ | `W0 §C-2` / `REF §2-3` 축자 **문자 단위 일치** | — |
| 5-8 | "**CLI 플래그 > 환경변수 > 활성 context**" | ✅ | `W0 §C-2` 도출 문장과 동일 | — |
| 5-9 | "**`docker --version`은 클라이언트 버전이다.** 데몬 버전을 보려면 `docker info`나 `docker version`의 Server 섹션" | ✅ | `PROBE §4` "이 사례가 가르치는 것" 1번과 일치 | — |
| 5-10 | "PATH가 고른 CLI와 context가 가리키는 데몬이 서로 다른 제품인 교차 상태 자체는 다루지 않는다" + `rancher-desktop#7712`(2024-11-01 등록, 조회 시점 OPEN) + "**이건 Windows 사례다**" | ✅ | `REF §2-3` ⛔("이 보고는 Windows다. 맥 사례로 둔갑시키지 말 것. 두 근거를 분리해서 쓴다") **정확히 준수.** 계획 5장 ⚠️ 충족 | — |
| 5-11 | Maven `<optional>true</optional>` / Gradle `developmentOnly(...)` | ✅ | `W0 §E-6` 축자 일치 | — |
| 5-12 | 라이프사이클 3단계 — `compose.yml` 탐색 → **`docker compose up`** → service connection 빈 → 종료 시 **`docker compose stop`** (표기 4.1.0, 2026-07-25 검색 기준) | ✅ | `W0 §E-6` 동작 서술과 **어순까지 일치.** 문서 표기 버전·검색 시점 병기 → §0-2 충족 | — |
| 5-13 | "이 자동 연결이 붙는 서비스는 **문서 기준 스무 종**에 이른다 — PostgreSQL·MySQL·MariaDB·Oracle·Redis·MongoDB·Cassandra·Elasticsearch·RabbitMQ·Pulsar·Zipkin 등에 JDBC/R2DBC까지" | ✅ | `W0 §E-6` 나열을 세면 **정확히 20개**(ActiveMQ·Artemis·Cassandra·Elasticsearch·MongoDB·Neo4j·MySQL·PostgreSQL·MariaDB·MSSQL·Oracle·ClickHouse·RabbitMQ·Redis·Hazelcast·Pulsar·LDAP·OTLP·Zipkin·JDBC/R2DBC). 본문이 든 이름 12개도 전부 그 목록 안 | — |
| 5-14 | 라벨 2종 — `org.springframework.boot.service-connection: redis` / `org.springframework.boot.ignore: true` | ✅ | `W0 §E-6` 축자 일치 | — |
| 5-15 | `spring.docker.compose.lifecycle-management` 3값(`none`/`start-only`/`start-and-stop`) + `file`·`profiles.active`·`start.command`·`stop.command`·`start.arguments[0]=--build`·`stop.timeout` | ✅ | `W0 §E-6` 프로퍼티 나열과 일치. (`stop.arguments[0]=--volumes` 1건 미채택 — 누락이지 오기 아님) | — |
| 5-16 | ⛔ **`compose.yml` 예제·파일 문법·`docker compose up` 실행 예제가 본문에 없다** + "(compose 파일 자체의 문법은 이 책의 범위가 아니다. 그건 Compose 공식 문서의 몫이다.)" | ✅ | **계획 5장 ⛔⛔ BLOCKING 재료 한계 준수.** 코퍼스 일반 Compose 재료 0건인데 창작이 발생하지 않았다 — 이 배치에서 가장 중요한 회피 | — |
| 5-17 | `styfle` — "I have a machine with Colima and don't want to bork it if I try Orbstack." | ✅ | `REF §2-3` 축자 일치. 원문은 뒤에 문장이 더 있으나 본문은 **문장 경계에서 종료**(스플라이스 아님) | — |
| 5-18 | `abiosoft` — "many tools are indeed catching up and utilising `docker context` instead. Another advantage of this approach is the ability to **try out Colima without breaking your current workflow.**" + "2022년 7월에 등록된 이 이슈는 2026년 7월 25일 조회 시점에도 열려 있다. 4년째다." | ✅ | `COMM` 일화 9 축자 — 두 문장이 **원문에서 연속**(스플라이스 아님). colima#365, 2022-07-12 등록, 조회 시점 OPEN(4년째) 전부 일치 | — |
| 5-19 | `spockz`(2026-07-02, Podman v6.0.0 스레드) — "lately it has been very error prone" / "Podman on macOS feels miles less refined. Orbstack is a way better choice." / 리눅스는 "blazing fast" | ✅ | `C2 §C-1` 축자·발화자·날짜 일치. HN 48762098 제출 2026-07-02. 마운트 실패·네트워킹 규칙·VM 재시작 서술도 원문에 있음 | — |
| 5-20 | `bmurphy1976`(2026-02-25) — Rancher Desktop으로 옮겨 "지금까지는 그냥 잘 된다" | ✅ | `C2 §C-4-c` — "So I've been lately using rancher by SuSE… **So far it just works.**" 번역 일치 | — |
| 5-21 | `Shebanator` — "products like this need security updates at the very least." + "이 책은 OrbStack의 릴리스 라인을 조회하지 않았으니 그 물음에 답을 보태지 않겠다" | ✅ | `C2 §C-4-d` 축자 일치(2026-02-25, 같은 HN 47151163 스레드). **계획 5장 "OrbStack 쏠림에는 반대 축 반드시 병기" 준수** + `W0` 미확인 #9(OrbStack 최신 버전 미조회)를 본문이 그대로 승계 | — |
| 5-22 | "2026년 7월 25일 조회 시점에 확인된 최신 릴리스는 2025년 6월 4일자였다" + "활발히 개발 중" 미사용 | ✅ | `W0 §C-1`·`REF §2-4` — v0.10.3 / 2025-06-04. 근거 파일이 이 날짜를 **약한 근거**로 표시했는데 본문이 "조회 시점에 확인된"으로 관측 귀속했고, ⛔ 금지어("활발히 개발 중")도 회피 | — |
| 5-23 | `xinit`(Davit 저자) VM 축자 + `watermelon0`의 "바로 다음 날" 반론(리눅스 커널 오버헤드로 메모리 사용량 증가) | ✅ | `C2 §C-2` 축자 일치. xinit 2026-07-07 / watermelon0 2026-07-08 → "바로 다음 날" 성립 | — |
| 5-24 | 이주 체크리스트 — Ryuk 소켓(2022-02) / 하드코딩 소켓(colima#365, 2022-07) / Colima 볼륨 권한·안정성(2024-09) / OrbStack 백업 소프트웨어·오프라인 라이선스(2024-09) / `docker context` 전역 상태 | ✅ | `REF §4-7` 체크리스트 표와 **항목·시점 전부 일치** | — |
| 5-25 | `nkmnz` — OrbStack 로컬 네트워킹과 운영의 compose + nginx가 "does not translate 1:1" | ✅ | `REF §4-7` 축자 일치. 계획이 ⭐로 지정한 요구 1 자산이 정확히 회수됨 | — |
| 5-26 | Testcontainers — Docker Desktop "automatically detected and used by Testcontainers without any additional configuration" / `DOCKER_HOST`(호스트에서 본) vs `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE`(컨테이너 안에서 본, `/var/run/docker.sock`) | ✅ | `W0 §E-7` 축자 + `REF §4-3` 두 변수 구분과 일치 | — |
| 5-27 | `kiview` — "**This will mask the error, rather than fixing the root cause**, since it will simply disable Ryuk, thereby leaving you without reliable resource cleanup." | ✅ | `REF §4-3`·`COMM` 일화 8 축자 **문자 단위 일치**(강조 위치까지 동일). 2022-02-11 | — |
| 5-28 | ⭐ **정정 6** — "2월 3일 메인테이너가 빌드 도구 설정으로 같은 목적을 이룰 수 있다며 **병합하지 않고 닫았다**(병합 기록이 비어 있음을 2026년 7월 25일에 확인했다). 그러니 '이제 `ryuk.disabled` 프로퍼티를 지원한다'는 말을 들었다면 사실이 아니다." | ✅ | **`C2 §I-2` 정확 적용.** `gh pr view 11414` → `state: CLOSED`, **`mergedAt: null`**(2026-07-25 조회), 반려 시각 2026-02-03, 반려 사유(빌드 도구 설정) 전부 일치. 이슈 11413·PR 11414 등록일 2026-01-05도 일치. **`CLOSED`를 "머지됨"으로 읽지 않았고, 오히려 "병합 기록이 비어 있다"는 검증 방법까지 본문에 노출했다.** 커뮤니티 리서처가 자기 판정을 뒤집은 항목이 본문에 올바른 쪽으로 안착 | — |
| 5-29 | testcontainers-java 이슈(2025-12-01 등록, 조회 시점 OPEN) — `2.0.1`은 감지, `2.0.2`·`2.0.3`은 미감지 / "체인지로그에서 파괴적 변경을 하나도 못 찾겠다" / `I would like to know when we broke this.` / "(원인은 아직 확정되지 않았고 표본도 그의 환경 하나다. '2.0.2에서 회귀가 있었다'고 옮겨 적으면 안 된다.)" | ✅ | `C2 §I-1` 축자 일치(#11254, 등록 2025-12-01, OPEN). **계획 ⚠️("회귀가 있었다로 단정 금지") 준수** + 표본 한계까지 본문이 명시 — 모범 | — |
| 5-30 | "the testcontainers' GitHub actions file does not test either Rancher Desktop or Docker Desktop." + `Could not find a valid Docker environment` | ✅ | `C2 §I-1` 축자 일치. 두 문자열 모두 같은 컨트리뷰터 보고 안에 있음 | — |
| 5-31 | Rancher Desktop 버전 3종(실측 1.17.1 / 릴리스 라인 / 컨트리뷰터의 1.20.1)이 **서로 연결되지 않았다** | ✅ | 본문은 세 값 중 **어느 것도 인쇄하지 않고** "자기 환경의 Rancher Desktop"으로만 서술. 계획이 경계한 오연결이 발생하지 않았다 | — |
| 5-32 | "사실 자바 백엔드 개발자가 맥에서 도커를 쓰는 **가장 흔한 이유**가 이쪽이다" | ⚠️ | 최상급 단정인데 코퍼스에 사용 빈도 근거(설문·통계)가 **없다.** 계획 5장이 지시한 문구를 그대로 옮긴 것이라 저술가 과실은 아니나, 검증 가능한 근거가 없는 단정이다 | 보강: "가장 흔한 이유" → "**가장 흔한 이유일 것이다**" 또는 "**흔한 이유 중 하나가**" (한 어절) |

**총평:** 5장의 최대 위험 지점 셋이 모두 통과했다. ① **`compose.yml` 창작이 일어나지 않았다** — 코퍼스 재료 0건인 영역에서 소절 하나를 쓰고도 파일 문법·실행 예제를 한 줄도 지어내지 않았고, 범위 밖임을 독자에게 고지했다(계획의 BLOCKING 조항 준수). ② **Ryuk PR을 "반려"로 정확히 읽었다** — `CLOSED`를 병합으로 오독하지 않았을 뿐 아니라 "병합 기록이 비어 있다"는 확인 방법까지 본문에 노출해 정정 6을 독자용 규율로 승격했다. ③ **`PROBE` 실측 4블록이 전부 "이 책을 쓴 맥" 맥락과 함께 인용됐고 일반화가 0건**이며, Rancher Desktop 버전 3종의 오연결도 없다. `rancher-desktop#7712`의 Windows 단서, Colima 릴리스 정체의 관측 귀속, OrbStack 릴리스 라인 미조회 고지까지 계획의 ⛔ 조항이 전부 지켜졌다. ⚠️ 1건은 최상급 표현이며 비블로킹이다.

---

## 6장. 같은 명령, 다른 결과 — arm64와 amd64

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/06_draft.md`
**집계:** ✅ 27 · ⚠️ 1 · **❌ 1** · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 6-1 | "이 책을 쓴 맥에서 데몬의 아키텍처를 물어보면 `aarch64`가 돌아온다 — arm64의 다른 이름이다" | ✅ | `PROBE §4` "데몬 아키텍처는 `aarch64`(= arm64)" 일치. 관측 귀속됨 | — |
| 6-2 | **"맥에서는 그 이미지가 경고만 뜨고 잘 돌아간다."** — 앞 문장이 "아무 설정 없이 이미지를 만들면 그 이미지는 **arm64**가 된다"이므로 "그 이미지"는 맥이 만든 arm64 이미지로 확정돼 있고, 뒷문장("배포 대상이 amd64라면 거기서는 즉시 죽는데도")이 방향을 **arm64 이미지 → amd64 서버**로 못 박는다 | **❌** | **근거와 충돌 — 본문이 근거보다 넓게 주장.** 본문이 옮긴 것은 `REF §3`의 **공통 패턴 압축 문장**("맥에서는 경고만 뜨고 돌아간다 → 개발자가 무시한다 → 배포 대상에서 처음 죽는다")인데, 이 문장은 **두 방향을 하나로 압축하면서 방향 1의 증상을 빌려 쓴 것**이다. 같은 코퍼스가 방향별로는 정반대를 적는다: ① `REF §3` 방향 표 2행 — arm64 이미지 → amd64 서버는 "M1 맥에서 빌드 → **EC2 배포 시점에 처음 발견**"(맥에서는 아무것도 안 보였다), ② `COMM`(375행) 방향 표 — 방향 2의 경고는 이미지 `linux/arm64/v8` / **detected host `linux/amd64`**, 즉 경고를 낸 쪽이 **서버**다, ③ `C2 §L-3` velog 기록 — 그 경고 문자열은 **서버 콘솔에서** 처음 나타났고 글쓴이의 결론도 "서버에서 실행이 되지 않았다"다. **코퍼스 전수 검색 결과, 맥이 자기가 만든 arm64 이미지에 대해 플랫폼 경고를 냈다는 근거는 한 건도 없다**(경고 템플릿은 불일치가 있어야 뜬다). 방향 1의 맥 쪽 경고(`COMM` 77행, 이미지 `linux/amd64` / host `linux/arm64/v8`)는 **amd64 이미지** 경우다. 게다가 이 장 자신의 방향 표(소절 2)가 세 문단 뒤에서 두 방향을 정확히 갈라놓아 **본문 내부에서도 충돌한다.** `REF §3`이 "**이 구분이 이 책이 가르쳐야 할 핵심이다**"라고 못 박은 바로 그 구분이며, 본문은 이 문장을 "이 책에서 가장 값비싼 문장"으로 제시한다 — 라운드 1의 4-28(근거가 말한 범위를 본문이 재범위화)과 **동일한 모양** | **정정문(필수):**<br>"맥에서는 그 이미지가 경고만 뜨고 잘 돌아간다." → **"맥에서는 그 이미지가 아무 경고 없이 그냥 잘 돌아간다."**<br>방향 2에 정확하고("맥에서는 아무 신호도 없다"), 장의 논지("신호가 만든 자리에서 오지 않고 배포 시점까지 미뤄진다")는 **오히려 강해진다.** "경고" 모티프는 소절 2의 방향 표에서 제자리를 찾는다.<br>⛔ **대체 문장에서 "맥이 경고를 낸다"는 서술을 새로 만들지 말 것.** ⛔ 소절 2의 공통 패턴 요약(본문 66행 "맥에서는 경고만 뜨고 돌아간다 → 무시한다 → 배포 대상에서 처음 죽는다")은 **방향 표 바로 아래**에 있어 두 방향이 이미 구분된 뒤이므로 `REF §3` 축자 그대로 **유지해도 된다** — 고칠 곳은 오프닝(9행) 한 문장이다 |
| 6-3 | 다섯 얼굴 표 — ①`exec /entrypoint.sh:` ②`exec /bin/sh:` ③`exec /cnb/process/web:` ④`fork/exec .../ca-certificates-helper:` ⑤`qemu: uncaught target signal 11 (Segmentation fault) - core dumped` + 출처·시점 5행 | ✅ | `REF §3` 증상 표와 **5행 전부 문자 단위 일치**(문자열·설명·출처·시점) | — |
| 6-4 | "**⑤는 `exec format error`가 아니다.** … 정확한 문장은 이쪽이다 — **에뮬레이션 실패는 `exec format error`가 아닌 형태로도 나타난다.**" | ✅ | **`REF §3` ⛔ 정확성 주의를 축자 수준으로 준수.** 계획 6장이 명시한 금지 표현("exec format error가 세그폴트로 나타나기도 한다")을 쓰지 않았다 | — |
| 6-5 | "⑤가 특히 잔인한 이유 … 에러 메시지에 아키텍처라는 단어가 한 번도 안 나온다" | ✅ | `REF §3` 주석 축자 일치 | — |
| 6-6 | `thaJeztah`의 진단 절차 — `docker run -it --rm --platform=linux/amd64 busybox` | ✅ | `REF §3 A1` / `COMM` — "Docker 모더레이터가 `--platform=linux/amd64 busybox`로 범위를 좁히자" 일치 | — |
| 6-7 | "`binfmt_misc` 등록 상태를 확인해보라는 다음 단계 제안 … 그건 메인테이너의 가설이고 해당 이슈는 재현 불가로 종결됐다. 가설까지로만 받아두자." | ✅ | `REF §3`(752–755행) ⛔("이건 메인테이너의 가설이고 해당 이슈는 재현 불가로 종결됐다. 'Docker Desktop의 binfmt 버그'로 단정하지 말 것") **정확히 준수**. docker/for-mac#7849, 2026-04-30 재현불가 CLOSED | — |
| 6-8 | **항목 10** — "이 책은 `exec format error`라는 문자열을 정면으로 설명하는 Docker 공식 페이지를 **확인한 페이지들에서는 찾지 못했다.** 없다고 단정하는 게 아니라 찾지 못했다는 뜻이다." | ✅ | `REF §3` ⚠️ + `W0` 미확인 #6과 일치. **공식 문서가 이 문자열을 정의한 것처럼 쓰지 않았고**, 부재 판정을 "확인한 페이지 한정"으로 정확히 약화했다 — 모범 | — |
| 6-9 | 경고 템플릿 — `WARNING: The requested image's platform ({이미지}) does not match the detected host platform ({호스트})` | ✅ | `REF §3` 템플릿 축자 일치 | — |
| 6-10 | 방향 표 2행 — amd64 이미지 → arm64 호스트(빌드 도구가 결정) / arm64 이미지 → amd64 서버(호스트가 결정) | ✅ | `REF §3` 방향 표와 **원인 주체 귀속까지 일치** | — |
| 6-11 | **항목 11 관련** — "**맥도 arm64였고 배포 대상인 클라우드 VM도 arm64였는데, 맥에서는 경고만 뜬 채 돌았고 그 VM에서는 죽었다.**" | ✅ | `REF §3 A3` 축자 — "M1 맥의 `bootBuildImage` 산출물이 **amd64**였다. 맥에선 경고만 뜨고 돌았고, **arm64 클라우드 VM**에서 `exec /cnb/process/web: exec format error`". **배포 대상이 arm64였다는 것이 코퍼스에 명시돼 있다** — 본문이 넓힌 것이 아니다 | — |
| 6-12 | **항목 11의 절제** — "같은 불일치를 한쪽은 넘어가 주고 다른 쪽은 넘어가 주지 않은 것이다"까지만 쓰고 **이유(에뮬레이션 유무)를 쓰지 않았다** | ✅ | **절제가 옳다.** 코퍼스 전수 확인 결과 그 VM의 binfmt/에뮬레이션 상태를 말하는 근거는 **어디에도 없다**(`REF §3 A3`·`COMM`·`C2` 모두 부재). 맥 쪽 에뮬레이션 존재는 3장 근거(Rosetta 토글, 기본 Disabled)로 알 수 있으나 **클라우드 VM 쪽은 미확인**이므로, 이유를 썼다면 근거 없는 단정이 됐다 | — |
| 6-13 | velog `@atoye1` 2022년 11월 + 인용 2건 + "**Node.js 앱이고 2022년의 이야기**라는 점은 먼저 밝혀두자. 자바가 아니다." | ✅ | `C2 §L-3` — 게시 **2022-11-17**, 인용 2건 축자 일치(둘 다 문장 경계에서 종료, 스플라이스 아님). 계획 ⚠️("Node.js이고 2022년임을 명시") 준수 | — |
| 6-14 | 멀티플랫폼 3전략 축자 — "Using emulation, via QEMU" / "Use a builder with multiple native nodes" / "Use cross-compilation with multi-stage builds" | ✅ | `W0 §B-1` 축자 3건 일치 | — |
| 6-15 | "Emulation with QEMU can be much slower than native builds, especially for compute-heavy tasks like compilation and compression or decompression." | ✅ | `W1` 축자 일치 | — |
| 6-16 | `docker buildx build --platform linux/amd64,linux/arm64 .` + "복수 플랫폼 지정은 `docker-container` 드라이버 빌더를 쓸 때 가능하고, 그 결과로 나오는 것이 … **매니페스트 리스트**" | ✅ | `W0 §B-1` 명령 축자 + `W1`("`docker-container` 드라이버를 쓸 때는 콤마로 구분한 여러 값을 지정할 수 있고, 그 결과 모든 플랫폼에 대한 매니페스트 리스트가 만들어진다") 일치 | — |
| 6-17 | "Builds with the `docker-container` driver aren't automatically loaded to your Docker Engine image store." + `--load`="Shorthand for `--output=type=docker`" / `--push`="Shorthand for `--output=type=registry`" | ✅ | `W1` 축자 3건 일치 | — |
| 6-18 | **항목 7·정정 11** — (A)/(B) 두 축자를 출처와 함께 병치하고 "**모순이 아니라 이미지 스토어의 세대가 다르다**" + classic 규정 축자 + "정확한 문장은 … **classic 스토어면 못 담고, containerd 스토어면 담을 수 있다**" | ✅ | `W1 §--load 제약의 진짜 조건` 3단 구조를 **그대로 재현**. (A)의 출처 "buildx build CLI 레퍼런스", (B)의 출처 "멀티플랫폼 문서"까지 근거 파일 표기와 일치. **절대 규칙으로 서술하지 않았다** | — |
| 6-19 | "**맥에서 Docker Desktop을 쓰는 이 책의 독자는 대체로 담을 수 있는 쪽이다**" + Desktop 축자 2건("Docker Desktop uses containerd as its image store by default." / "…enabled by default in Docker Desktop version 4.34 and later.") (2026년 7월 26일 조회 기준) | ✅ | `W3 §T5-2` 축자 일치. 조회 시점(2026-07-26)이 `W3` 검색 시점과 동일. "대체로"라는 한정어가 유지됨 | — |
| 6-20 | **정정 13** — "**둘 다 원문 그대로이고 모순도 아니다. 제품 라인이 다르다.** … '도커는 4.34부터 containerd가 기본'이라고 뭉뚱그리면 틀린 문장이 된다." | ✅ | **`W3 §T5-2` ⛔("'도커는 4.34부터 containerd가 기본'이라고 뭉뚱그리면 ❌")를 본문이 그대로 승격.** 계획 정정 13이 **독자용 규율**로 명문화됐다 — 1장 1-8과 같은 모범 처리 | — |
| 6-21 | **항목 7의 Engine 조건** — Engine 축자 전문 인용 + "**신규 설치일 때만 기본값이라는 것.** 예전 버전에서 올려 쓴 데몬은 직접 켜기 전까지 overlay2를 계속 쓴다." + "어제 산 맥에서는 틀린 규칙이지만, 3년째 굴리는 빌드 서버에서는 맞는 규칙이다." | ✅ | `W3 §T5-2` Engine 축자 전문과 일치. **"fresh installations"·"upgraded from an earlier version … overlay2" 두 조건이 모두 살아 있다** — 항목 7이 요구한 조건 누락 없음 | — |
| 6-22 | **항목 8** — `docker info -f '{{ .DriverStatus }}'` → `[[driver-type io.containerd.snapshotter.v1]]` + "**보이면 containerd 스토어다.** 딱 이 방향으로만 읽는다. 반대로 '안 보이면 classic이다'라고 단정하지는 말자" + "이 명령은 문서의 리눅스 데몬 설정 절차 안에 실려 있어서, macOS에서 똑같은 출력이 나온다고 문서가 말해주지도 않는다" | ✅ | `W3 §T5-1` 축자 + **⛔ 3항목(역방향 단정 금지 / 클래식 출력 미확인 / macOS 미보장) 전부 준수.** 계획 §0-3 새 금지 #2·#4 충족. 독자에게 직접 쳐 보게 안내하는 교육 패턴까지 지시대로 | — |
| 6-23 | Desktop 토글 경로(**Settings → General → "Use containerd for pulling and storing images" → Apply**) + "전환하면 반대편 스토어의 이미지와 컨테이너는 디스크에 남아 있되 **보이지 않게 된다**" + "압축본과 비압축본을 둘 다 보관하기 때문이다" | ✅ | `W3 §T5-2` 축자 3건 일치("hidden until you switch back" / "stores images in both compressed and uncompressed formats") | — |
| 6-24 | `hojooo`(2025년 10월, M1) 토글 on/off 재현 여부 + `philwebb`(2025년 11월) on/off 나눠 검증 | ✅ | `REF`(763–764행) — `hojooo` **2025-10-23**, M1, 축자 "If that option is turned **on**, I have confirmed the similar issue is reproduced… **turning off that option won't reproduce the problem.**" / `philwebb` **2025-11-13** 분석에서 on/off를 나눠 검증. `COMM §H4`도 동일. **두 날짜·두 행위 모두 근거 있음** | — |
| 6-25 | 계획 M8 금지어 — 이 장에서 "멀티플랫폼 인덱스"·"API v1.41"·"inspect의 플랫폼 선택"을 **쓰지 않았다** | ✅ | 6장 본문 전수 확인 — 세 표현 모두 미등장. 메커니즘은 7장으로 온전히 이월됐다(계획 6장 ⛔ M8 준수) | — |
| 6-26 | `docker buildx imagetools inspect moby/buildkit:master --format "{{.Manifest}}"` / `--raw … | jq` + "Show details of an image in the registry" / `--format` 기본값 `{{.Manifest}}` / "Show original, unformatted JSON manifest" | ✅ | `W1` 예제 블록·옵션 설명과 **문자 단위 일치** | — |
| 6-27 | "'유일한 방법'이라는 말은 … **이 책이 이 하나만 가르친다**는 뜻이다. 이미지의 OS와 아키텍처를 뽑아준다는 다른 명령들이 … 이번 리서치에서 공식 문서로 확인하지 못했다." | ✅ | `W1` ⚠️("이 명령만 가르칠 것. `docker image inspect --format '{{.Os}}/{{.Architecture}}'` 같은 다른 명령은 … 쓰지 말 것") 준수. **금지된 대체 명령을 인쇄하지 않으면서** 이유를 밝혔다 | — |
| 6-28 | `dmikusa`(2024년 6월) — "just delete your existing app images and the build cache" / "or you can change the image name, that will trigger a fresh build too" + 2025년 9월 다른 사람의 "contaminated" | ✅ | `REF §5-1 H3`·`COMM §H3` 축자 일치. `jdnurmi` 2025-09-04 → "1년 넘게 지난" 성립(2024-06 → 2025-09) | — |
| 6-29 | 그림 1(mermaid) 노드 텍스트 — 드라이버 조건·출력 경로 2갈래·스토어 2종·판정 명령 주석 | ⚠️ | 노드 텍스트는 전부 6-16~6-22의 근거 안에 있다. 다만 `C2` 노드가 "**멀티플랫폼 이미지를 로컬에 담을 수 있다**"로 단정형인데, 근거(`W3 §T5-2`)의 대응 축자는 "The containerd image store lets you build multi-platform images and load them to your local image store"로 동일하다 — 본문 서술과 그림이 어긋나지 않는다. 유일한 미세 지점은 **판정 주석이 그림 안에서는 macOS 단서를 달지 못한다**는 것(본문 6-22가 세 줄 뒤에 보완) | 보강(선택): 그림 1 `V` 노드 끝에 "(문서의 리눅스 절차 기준)" 한 구절. 본문이 이미 보완하므로 비블로킹 |

**총평:** 6장의 세 고위험 지점이 전부 통과했다. ① **`--load` 조건부 규칙**(정정 11)이 (A)/(B) 축자 병치 → 제3 문서로 조건 확정 → "classic이면 못 담고 containerd면 담는다"로 정확히 재현됐고, **Engine의 "신규 설치"·"업그레이드 데몬은 overlay2 유지" 두 조건이 살아 있다.** ② **판정 명령이 한 방향으로만** 서술됐고 역방향 단정·macOS 단정이 둘 다 없다(§0-3 새 금지 #2·#4 충족). ③ **제품 라인 혼동**(정정 13)은 회피를 넘어 독자용 규율로 승격됐다. `exec format error`의 공식 문서 부재도 "확인한 페이지에서 못 찾음"으로 정확히 약화됐고, 계획 M8 금지어 3종도 지켜졌다. **항목 11(저술가 질문)에 대한 답: 절제가 옳고, 코퍼스에 그 이유의 근거는 없다.** 다만 배포 대상이 arm64였다는 사실은 코퍼스에 명시돼 있어 본문이 넓힌 것이 아니다.

**그러나 오프닝 한 문장이 BLOCKING이다(6-2).** 이 장이 소절 2에서 정확히 갈라놓는 두 방향을, 9행의 "가장 값비싼 문장"이 하나로 뭉쳐 **방향 1의 증상(맥 쪽 경고)을 방향 2의 이미지(맥이 만든 arm64)에 붙였다.** 코퍼스는 방향 2에서 경고를 낸 쪽을 일관되게 **서버**로 적는다. 역설적이지만 정정하면 논지가 강해진다 — 맥이 경고조차 안 낸다는 쪽이 "신호가 만든 자리에서 오지 않는다"는 이 장의 주제에 더 정확하다. ⚠️ 1건(그림 주석)은 비블로킹이다.

---

## 7장. Spring Boot 앱을 이미지로 만드는 세 갈래

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/07_draft.md`
**집계:** ✅ 40 · ⚠️ 2 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 7-1 | **정정 7** — 비교표 1행: Dockerfile+buildx ✅ / **Paketo ❌ 불가**(`imagePlatform` 단일 값) / **Jib ✅ 가능**(`platforms` 복수 지정 시 매니페스트 리스트 push, **incubating**) | ✅ | `W1` 3경로 비교표와 **칸 단위 일치.** `REF §8-2`도 동일. incubating 표시 유지 | — |
| 7-2 | Jib 제약 칸 — "**레지스트리 push 전용** — `jibDockerBuild`·`jib:dockerBuild`·`jibBuildTar` 경로에서는 안 된다. **OCI image index 미지원**, **크로스 컴파일 미지원**, architecture·os만 지원(variant 미지원)" | ✅ | `W1` FAQ 제약 나열과 일치 — "OCI image indices are not supported", "Does not support pushing to a Docker daemon (`jib:dockerBuild`/`jibDockerBuild`) or building a local tarball (`jib:buildTar`/`jibBuildTar`)", "architecture와 os만 지원 (variant 미지원)", "크로스 컴파일 미지원". **4개 제약 전부 근거 있음** | — |
| 7-3 | Jib 베이스 기본값 `eclipse-temurin:{ver}-jre` / Paketo 빌더 `paketobuildpacks/builder-noble-java-tiny:latest` | ✅ | `W1` — "기본 `eclipse-temurin:{8,11,17,21,25}-jre`". 근거 파일이 ⚠️로 "`{8,11,17,21,25}`는 문서 표기법이지 리터럴 태그가 아니다"라 경고한 것을, 본문이 `{ver}`로 바꿔 **리터럴 오해 위험을 오히려 낮췄다** | — |
| 7-4 | Docker 데몬 칸 — "`jib`·`jib:build`는 레지스트리로 직행, `jibDockerBuild`·`jib:dockerBuild`는 데몬 사용" | ✅ | `W1` ⚠️("'데몬이 전혀 필요 없다'는 단정은 피하고, 두 태스크가 별개라는 **관찰된 구조**로 쓸 것") **정확히 준수.** 계획 7장 ⚠️ 충족 | — |
| 7-5 | Paketo ❌ 증거 5건 — ①`--platform string`(단수) vs `--tag strings`·`--buildpack strings`·`--pre-buildpack stringArray` ②CNB 축자 ③`imagePlatform`이 `OS[/architecture[/variant]]` 단일 값 ④RFC 0128 범위 한정 ⑤"CNB 멀티아키 지원"의 두 얼굴 | ✅ | `W1 §G1`·`REF §8-1` — 플래그 타입 4종 표기, "We do not currently support building an app image for one architecture on a different architecture." 축자, RFC 0128 범위(빌더·빌드팩 패키지 한정, Approved) 전부 일치. **⑤의 패키징/앱 이미지 구분이 본문에 있어 CNB 자기 문서와의 외견상 모순이 해소됨** | — |
| 7-6 | Jib FAQ 축자 — "When multiple platforms are specified, **Jib creates and pushes a manifest list (also known as a fat manifest)** after building and pushing all the images for the specified platforms." | ✅ | `W1` 축자 **문자 단위 일치** | — |
| 7-7 | "매니페스트 리스트를 만든다면서 크로스 컴파일은 안 된다니 모순처럼 들리지 않는가? 모순이 아니다. 앞은 **출력 이미지의 형태**이고, 뒤는 플랫폼별 네이티브 바이너리가 필요할 때 Jib이 그것까지 만들어주지는 않는다는 이야기다." | ✅ | `W1` ⚠️ 해설과 **논리·표현 모두 일치.** 계획이 "이 구분을 반드시 붙일 것"이라 지시한 항목 충족 | — |
| 7-8 | "`jib-maven-plugin` 3.5.2와 `jib-gradle-plugin` 3.5.4처럼 플러그인별로 따로 매겨진다(2026년 7월 조회 기준)" | ✅ | `W1` 표 — maven **3.5.2** / gradle **3.5.4**, 독립 버저닝 서술 일치. **⛔ 릴리스 날짜(폐기 판정)를 쓰지 않았다** — 계획 ⛔ 준수 | — |
| 7-9 | `imagePlatform` 축자 2건 — "The platform (operating system and architecture) of any builder, run, and buildpack images that are pulled." / "**No default value, indicating that the platform of the host machine should be used.**" (문서 표기 4.1.0, 2026년 7월 렌더 기준) | ✅ | `W0 §E-1`·`W1` 축자 일치. 문서 표기 버전·렌더 시점 병기 | — |
| 7-10 | "이 문장이 직접 말하는 것은 **pull해 오는 빌더·run·빌드팩 이미지의 플랫폼**이지 결과 이미지가 아니다. '공식 문서에 결과 이미지가 arm64라고 적혀 있다'고 옮기면 문서가 하지 않은 말을 하는 셈" | ✅ | **`W0 §E-1` ⚠️("추론과 인용의 경계")를 축자 수준으로 준수.** 2단계 추론임을 본문이 스스로 드러냄 — 계획 ⛔ 충족, 모범 | — |
| 7-11 | 레지스트리 조회 블록 + "2026년 7월 25일 조회 시점에 … `builder-noble-java-tiny:latest`와 그 짝인 `run-noble-tiny:latest` 모두 linux/amd64와 linux/arm64 두 매니페스트를 담고 있었다" | ✅ | `W0 §E-2` — 조회 결과 표 2행 일치, `mediaType: application/vnd.oci.image.index.v1+json` 일치, 조회 시점 2026-07-25 일치. **⛔ digest를 못 박지 않았다**(`{...}`로 생략) — 계획 ⛔ 준수 | — |
| 7-12 | "`imagePlatform` 도입은 **3.4.0부터**다(Maven 플러그인 파라미터 상세에 명시)" | ✅ | `W0 §E-1` — "도입 버전: `imagePlatform`은 **Since `3.4.0`** (Maven 플러그인 파라미터 상세에 명시)" 축자 일치 | — |
| 7-13 | spring-boot#46674 — 제목 축자, 2025년 8월 5일 등록, **CLOSED** — PR #47292로 대체됨, 컨트리뷰터 `hojooo` | ✅ | `C2 §J-1` — 제목·등록일·상태·대체 PR·association(contributor) 전부 일치 | — |
| 7-14 | `hojooo` 블록 인용(containerd 인덱스 / API v1.41 / `GET /images/{name}/json` 플랫폼 미선택 / 호스트 기본 플랫폼 → `linux/arm64`) | ⚠️ | `C2 §J-1` 축자와 **단어 단위 일치**하며 생략된 구간 없음. 다만 **원문은 `*` 불릿 2개**인데 본문이 하나의 연속 산문으로 이어 붙였다(순서 보존, 사이 생략 없음). 의미 왜곡 없음 | 보강(선택): 인용 안에서 두 불릿을 줄바꿈으로 분리하거나 각각 별도 인용줄로. 비블로킹 |
| 7-15 | "보고자가 제시한 임시 우회는 둘이다. `DOCKER_DEFAULT_PLATFORM=linux/amd64`를 지정하거나, containerd 이미지 스토어를 **잠시 끄는** 것." | ✅ | `C2 §J-1` "Workarounds for affected users (temporary)" 2항목 축자 일치 | — |
| 7-16 | "이 스토어는 Docker Desktop 4.34 이상에서 **기본으로 켜져 있으므로**(2026년 7월 검색 기준), 여기서 하는 일은 내가 켠 걸 되돌리는 게 아니라 **기본값을 임시로 내리는** 쪽에 가깝다." | ✅ | `W3 §T5-2` 축자에 근거. **⛔ "보고자도 기본값이었다"고 쓰지 않았다**(문장 주어가 독자다) — `W3 §T5-3` ⛔ 준수. `hojooo`의 환경은 오히려 토글 ON으로 코퍼스에 명시돼 있어 충돌도 없다 | — |
| 7-17 | **항목 17** — "이슈에 등장하는 API 버전 숫자(v1.41·v1.51·v1.52)는 **보고자와 참여자들이 자기 환경에서 본 값**" | ✅ | `C2 §J-1` — v1.51(`hojooo` Environment), 1.52(`hiro345g`), v1.41(`hojooo`의 `DockerApi` 서술). 근거 파일의 지시("이 숫자들은 이슈 보고자의 서술이다. fact-checker가 1차 소스로 대조할 것")에 대해 **본문이 1차 소스 승격을 하지 않고 보고자 귀속으로 낮춘 것이 정확한 처리**다 | — |
| 7-18 | **항목 16** — "이슈가 PR #47292로 대체되며 닫히긴 했지만 그 PR의 머지·릴리스 여부는 이 책이 확인하지 못했다 — **'고쳐졌다'고 읽지 말자.**" | ✅ | `C2 §J-1` 📌("PR #47292가 머지됐는지, 어느 릴리스에 들어갔는지는 확인하지 않았다. '고쳐졌다'고 쓰지 말 것") + `REF §5-2` ⚠️ 준수. **`CLOSED`를 병합으로 읽지 않았다** | — |
| 7-19 | spring-boot#46665 — `docker pull`에는 플랫폼 플래그, 이어지는 `docker save`에는 미부여 → Docker가 호스트 가정 | ✅ | `REF §5-2`(848행)·`COMM`(461행 `ofirm93` 축자) 일치 | — |
| 7-20 | `wilkinsona` 축자 — "it sounds like the problem **only occurs when trying to build an `amd64` image on an arm64 host.**" + "'arm64 맥에서 `bootBuildImage`가 실패한다'는 요약은 틀렸다" | ✅ | `REF §5-2`(850–851행)·`COMM §2-4` 축자 일치. **계획이 지정한 정정을 본문이 독자용 규율로 승격** | — |
| 7-21 | 4년 타임라인 — 2022-11 / 2024-06 / 2024-11(3.4.0) / 2025-08~11 / 2026-02 M4 재현 불가 종결 + "끝났다고 말하기에는 이르다" | ✅ | `REF §5-2` 타임라인 표 5행과 **시점·내용 전부 일치.** ⛔("'끝났다'고 쓰지 말 것") 준수 | — |
| 7-22 | `java -Djarmode=tools -jar my-app.jar` + `extract`/`list-layers`/`help` 3줄 | ✅ | `W0 §E-5` 도움말 블록과 일치(본문은 `Usage:` 헤더를 프롬프트 `$`로 대체 — 표현 차이, 내용 동일) | — |
| 7-23 | "검색하면 `-Djarmode=layertools`가 많이 나오는데, 지금 문서가 안내하는 것은 `-Djarmode=tools`다(문서 표기 4.1.0, 2026년 7월 렌더 기준). **어느 버전에서 바뀌었는지는 이 책이 확인하지 못했으니**" | ✅ | `W0 §E-5` 미확인 표시 + 미확인 목록 #3("`layertools` 제거·deprecate 시점")을 본문이 그대로 승계. 계획 ⛔("'언제부터'는 쓰지 말 것") 준수 | — |
| 7-24 | 공식 멀티스테이지 Dockerfile 전문(`bellsoft/liberica-openjre-debian:25-cds` 2회, `COPY` 4줄, `ENTRYPOINT`) | ✅ | `W0 §E-5`·`W1` 코드블록과 **줄 단위 일치**(런타임 스테이지 주석 1줄만 생략) | — |
| 7-25 | "복사 단계마다 새 도커 레이어가 생기고 … 'only pull the changes it really needs'" + 순서는 자주 안 바뀌는 것부터 | ✅ | `W0 §E-5` 문서 주석 축자 + 레이어 순서 일치 | — |
| 7-26 | "After startup, you should not expect any differences in execution time between running an executable jar and running an extracted jar." + "차이는 **시작**에 있지 **실행**에 있지 않다" | ✅ | `W0 §E-5` ⭐ 축자 일치. 계획이 ⭐로 지정한 오해 차단 문장 회수 | — |
| 7-27 | `docker login [OPTIONS] [SERVER]` / "**서버를 생략하면 Docker Hub다**" | ⚠️ | 문법은 `W3 §T4-1` 축자 일치. 그러나 "서버를 생략하면 Docker Hub"라는 **일반 규칙 문장은 코퍼스에 축자로 없다** — 있는 것은 ① 서버 없는 `$ docker login` 예제가 Docker Hub 디바이스 코드 흐름으로 가는 출력 전문, ② "For Docker Hub, the docker login command uses a device code flow by default"다. 한편 `docker logout`의 대응 문장은 "If no server is specified, **the default is defined by the daemon.**"이다(§T4-5). 예제로 뒷받침되지만 규칙문으로 승격된 상태 | 보강: "서버를 생략하면 Docker Hub다" → "**서버를 생략하고 그냥 `docker login`을 치면 문서 예제는 Docker Hub 흐름으로 간다**" (관측 귀속) |
| 7-28 | `--password-stdin` 권장 근거 축자 — "Using STDIN prevents the password from ending up in the shell's history, or log-files." + 디바이스 코드 흐름 기본, `--username` 주면 자격증명 경로 | ✅ | `W3 §T4-1` 축자 2건 일치 | — |
| 7-29 | 자체 호스팅 함정 — "`docker login registry.example.com/foo/`는 틀리고 `docker login registry.example.com`이 맞다. 호스트명과, 필요하면 포트까지다." | ✅ | `W3 §T4-1` ⛔ 축자 일치 | — |
| 7-30 | 자격증명 저장 축자 2건 — 키체인 문장 / base64 문장 + `Apple macOS keychain` 헬퍼 목록 + `osxkeychain` + "With Docker Desktop, the credential store is already installed and configured for you." | ✅ | `W3 §T4-2` 축자 **4건 전부 문자 단위 일치** | — |
| 7-31 | **항목 15** — "다만 파일 경로를 단정하지는 말자 — 공식 문서가 경로를 명시하는 대상은 Linux와 Windows뿐이다." | ✅ | **§0-3 새 금지 #3 준수.** macOS `.docker/config.json` 경로가 본문 어디에도 없다(전수 grep 확인). `config.json`이라는 문자열은 **공식 축자 인용 안에만** 등장 | — |
| 7-32 | GHCR 블록 4줄 — `export CR_PAT=YOUR_TOKEN` / `echo $CR_PAT \| docker login ghcr.io -u USERNAME --password-stdin` / `> Login Succeeded` / `docker push ghcr.io/NAMESPACE/IMAGE_NAME:2.5` | ✅ | `W3 §T4-6` 축자 **4줄 전부 일치**(플레이스홀더 `YOUR_TOKEN`·`USERNAME`·`NAMESPACE`·`IMAGE_NAME` 유지) | — |
| 7-33 | "GitHub Packages only supports authentication using a personal access token (classic)." + `write:packages` 선택 시 `repo` 동반 선택 + 좁히는 URL `https://github.com/settings/tokens/new?scopes=write:packages` + Actions는 `GITHUB_TOKEN` 권고 | ✅ | `W3 §T4-6` 축자 4건 일치(URL 문자열 포함) | — |
| 7-34 | ECR — `aws ecr get-login-password --region region \| docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com` + 사용자명 문자 그대로 `AWS` + **12시간 유효** + 레지스트리마다 반복 | ✅ | `W3 §T4-7` 축자 **명령 한 글자까지 일치.** "is valid for 12 hours" / "use the value AWS for the username" / "If authenticating to multiple registries, you must repeat the command for each registry." 3건 일치. **플레이스홀더를 실제 값으로 지어내지 않았다** — ⛔ 준수 | — |
| 7-35 | 참조 문법 `[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]` + 3중 기본값 + 분해 표 2행(`example.com:5000/team/my-app:2.0` / `alpine`) | ✅ | `W3 §T4-3` 축자 — 문법·3기본값·분해 예시 2건 **전부 문자 단위 일치** | — |
| 7-36 | `docker tag my-app:1.0 ghcr.io/NAMESPACE/my-app:1.0` | ✅ | 축자 예제는 아니다. 그러나 `W3 §T4-3`의 Usage 축자 `docker image tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]`와 참조 문법 축자를 **그대로 인스턴스화**한 것이며 어긋난 토큰이 없다 → 라운드 2 명령 규칙의 2항 적용 | — |
| 7-37 | `docker image push [OPTIONS] NAME[:TAG]` / 별칭 `docker push` / "Registry credentials are managed by docker login." / 진행 표시줄은 **비압축 크기** / `docker logout [SERVER]` | ✅ | `W3 §T4-4`·`§T4-5` 축자 5건 일치. **⛔ `docker container commit` 경로를 옮기지 않았다** — ⛔ 준수 | — |
| 7-38 | **항목 14** — "프라이빗 레지스트리에서 이미지를 내려받아야 한다면 **쿠버네티스 쪽에도 별도의 자격증명 설정이 필요하다.** 이 책의 범위 밖이니…" | ✅ | **§0-3 새 금지 #1 준수 — 그 이상이다.** 본문에 `imagePullSecrets`라는 **필드명 자체가 등장하지 않고**, 매니페스트·YAML·설정 예제도 없다. 한 줄 고지 + 공식 문서 안내로 종료 | — |
| 7-39 | `docker pull` / `docker run --rm -p 8080:8080` + `docker buildx imagetools inspect … --raw` 재사용 | ✅ | pull/run은 문서 문법의 인스턴스화(라운드 2 명령 규칙 2항), `imagetools inspect --raw`는 `W1` 축자. 6장 명령의 재사용이라 새 주장 없음 | — |
| 7-40 | `docker push --platform`(**API 1.46 이상**) 축자 — "Push a platform-specific manifest as a single-platform image to the registry. **Image index won't be pushed, meaning that other manifests, including attestations won't be preserved.**" | ✅ | `W3 §T4-4` 옵션 표 축자 일치. **⚠️ 조건 `API 1.46+`이 병기됐다** — `W3`가 "반드시 병기하라"고 지시한 항목 충족 | — |
| 7-41 | "Paketo 경로를 쓰면서 멀티아키 태그가 필요하다면 … **두 아키텍처를 각각 독립적으로 빌드한 뒤 `docker manifest`로 인덱스 이미지를 합성**한다" | ✅ | `REF §8-1` 실무 결론 2 / `REF §5-2` 타임라인(2024-11 "멀티아키 태그를 원하면 `docker manifest`를 손으로")와 일치 | — |
| 7-42 | 12장 예고 — "클러스터가 이미지를 언제 다시 당겨오는지, 그 판단이 태그를 어떻게 읽는지에 달려 있기 때문이다" | ✅ | **정책 이름(`imagePullPolicy`)을 단정하지 않았다** — 계획 M6 규율 준수 | — |

**총평:** 7장은 이 배치에서 축자 밀도가 가장 높다. **`W3 §T4`의 축자 약 20건을 전수 대조한 결과 명령·옵션·URL·플레이스홀더가 한 글자도 어긋나지 않았다** — GHCR PAT 4줄, ECR 파이프 1줄, 태그 문법과 분해 표, `push --platform`의 API 1.46+ 조건까지 전부 원문과 일치한다. 계획의 두 BLOCKING 금지도 회피를 넘어섰다: **`imagePullSecrets`는 필드명조차 등장하지 않고**, **macOS `.docker/config.json` 경로는 어디에도 없다**(`config.json` 문자열은 공식 축자 인용 안에만). PR #47292·#46674·#46665의 `CLOSED` 규율도 지켜져 "고쳐졌다"는 오독이 없고, API 버전 숫자는 보고자 귀속으로 낮춰졌다. 정정 7(3파전)의 Jib·Paketo 제약도 근거와 칸 단위로 일치한다. ⚠️ 2건은 인용 서식(불릿 병합)과 규칙문 승격이며 둘 다 비블로킹이다.

---

## 8장. `FROM` 뒤의 선택, 그리고 그 안의 자바

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/08_draft.md`
**집계:** ✅ 28 · ⚠️ 0 · ❌ 0 · **🕒 1**

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 8-1 | "Our analysis shows that pulling packages accounts for 76% of container start time, but only 6.4% of that data is read." — Harter et al., FAST '16 Abstract (**2016년 측정**) | ✅ | `PAPER` 대표 인용 5 축자 일치. **측정 연도 병기** → §0-2 충족 | — |
| 8-2 | warm start — Premium SSD, alpine 5MB ↔ `python:3.11-slim` 155MB, **554~568밀리초, 2.5%** (Khan, arXiv:2602.15214 Finding 1, **2026년, 프리프린트**) | ✅ | `PAPER` 논문 3 Finding 1 축자 일치. **측정 연도 + 프리프린트 단서 둘 다 병기** → §0-2 요구 충족. arXiv ID `2602`(2026-02)는 빌드 시점(2026-07) 기준 **과거**이므로 미래 YYMM 자동 ❌ 규칙 비해당 | — |
| 8-3 | "이 편차를 지배하는 것은 이미지 크기가 아니라 런타임 오버헤드 — 네임스페이스 생성, cgroup 설정, 파일시스템 마운트 준비 — 라는 것이 저자의 설명이다" | ✅ | `PAPER` — "Runtime overhead (namespace creation, cgroup setup, OverlayFS mount preparation) dominates." 일치(OverlayFS → "파일시스템"은 상위 개념으로의 완화이며 과잉 주장 아님). **저자 귀속 명시** | — |
| 8-4 | "**재는 구간이 다를 뿐이다** … '이미지를 줄이면 빨라진다'는 명제는 조건부로만 참이다" + cold/warm 구분 | ✅ | `PAPER` 논문 3 "이 책에서의 쓸모" — "단, cold start / pull 시간은 별개임을 반드시 구분할 것" 준수. **티어 간 절대값 비교 없음**(§0-2·계획 4장 ⛔ 저촉 없음) | — |
| 8-5 | Borg — "작업 기동 지연의 중앙값이 대략 25초였고 그중 **패키지 설치가 약 80%**"(Verma et al., EuroSys '15 §3.4, 2015년 기준) + "**Borg는 Kubernetes가 아니다**" | ✅ | `PAPER` 논문 7 §3.4 축자 + 🕒 신선도 주의("Borg는 Kubernetes가 아니다 … 25초/80%는 2015년 Google Borg 기준임을 반드시 병기") **완전 준수.** 저자·연도·구글 소속까지 본문에 있음 | — |
| 8-6 | 후보 5종 표 — `eclipse-temurin:{ver}-jre-{noble\|jammy}` / `eclipse-temurin:{ver}-jdk-alpine-{ver}` / `debian:{suite}-slim` / `gcr.io/distroless/java{17\|21\|25}-debian13` / `bellsoft/liberica-openjre-debian:25-cds` (전부 2026년 7월 25일 조회 기준) | ✅ | `W1 §G3`·`REF §8-3` — 태그 라인업(`25-jre-jammy`·`25-jdk-noble`·`25-jdk-alpine-3.23`), distroless 자바 이미지 3종, Liberica 예제 이미지 전부 일치. 근거 열도 근거 파일의 출처와 일치 | — |
| 8-7 | `-slim` 축자 — "an experiment in providing a slimmer base (removing some extra files that are normally not necessary within containers, such as man pages and documentation)" + "**`-slim`과 Alpine은 같은 종류의 절약이 아니다**" | ✅ | `W1 §G3` 축자 일치 + "slim은 짐을 덜어낸 같은 집이고, Alpine은 다른 집이다"는 근거 파일의 ⭐ 핵심 대비와 동일한 논지 | — |
| 8-8 | "Alpine은 애초에 **musl libc와 busybox 위에 지어진** 배포판이라고 공식 소개가 밝힌다" | ✅ | `W1 §G3` — "Alpine Linux is built around musl libc and busybox." 일치 | — |
| 8-9 | distroless — "애플리케이션과 그 런타임 의존성만" + "package managers, shells or any other programs you would expect to find in a standard Linux distribution" + 3단 논리 + `debug` 태그의 busybox 셸 + 자바 이미지 arm64 지원 | ✅ | `W1 §G3`·`REF §8-3` 축자 4건 일치. arm64 지원(amd64/**arm64**/s390x/ppc64le/riscv64)도 근거 있음 | — |
| 8-10 | Temurin 권고 — "JRE images are available for all versions of Eclipse Temurin but it is recommended that you produce a custom JRE-like runtime using `jlink`." | ✅ | `W1 §G3` 축자 일치 | — |
| 8-11 | **항목 21** — "다만 태그 라인업은 이 책이 확인하지 못했으니, 쓰기로 했다면 벤더 문서를 열어보고 고르자"(BellSoft Liberica) | ✅ | `W1 §G3` — "Liberica 자체의 태그 라인업(musl/alpine 변형 존재 여부)은 **미확인**" 을 본문이 그대로 승계 | — |
| 8-12 | **정정 8(a)** — 통설을 `huksley`(2023년 3월 HN)에게 귀속 + 축자 "those java/jdk-\*-alpine images... actually support only subset of a (gigantic) APIs available in Java." | ✅ | `COMM §6-1`·`REF §8-3` 축자 일치. 원문 "Even those java/jdk-\*-alpine images, **claiming being able to run JDK** actually support only subset…"에서 중간 삽입절을 **말줄임(`...`)으로 표시하고 생략** — 스플라이스 아님. **통설을 저자 목소리로 승격하지 않고 2023년 커뮤니티 발언으로 격하** | — |
| 8-13 | **정정 8(b) 반증 2건** — ① "Eclipse Temurin이 `eclipse-temurin:25-jdk-alpine-3.23`을 JDK로 배포하고 있다. 표준 API가 잘려 있는 런타임이라면 `jdk` 태그를 달 수 없다." ② "Alpine 변형에 대한 공식 caveat이 가리키는 곳은 Java API가 아니라 libc다." + caveat 축자 전문 | ✅ | `REF §8-3` ⛔⛔ 판정 문장과 **논리·태그명 모두 일치**(태그 `25-jdk-alpine-3.23` 정확). caveat 축자("Alpine Linux is much smaller than most distribution base images (~5MB)… it does use musl libc instead of glibc and friends, so software will often run into issues depending on the depth of their libc requirements/assumptions.")도 `W1 §G3`과 문자 단위 일치 | — |
| 8-14 | "위험한 것은 자바 표준 API가 아니라, 네이티브 라이브러리를 끼고 도는 의존성이다" + "덧붙이면 원 발언자 본인도 자기 말에 불확실 표시를 달아두었다" | ✅ | `REF §8-3` ✅("대신 이렇게 쓸 것: 진짜 주의점은 API가 아니라 musl libc다. 네이티브 라이브러리를 쓰는 의존성에서 문제가 날 수 있다") 지시와 일치. 불확실 표시는 `COMM §6-1` `(확인 필요 — "Last time I checked"…)` 근거 | — |
| 8-15 | **정정 9** — "몇 년 전 대표 근거는 musl의 DNS 처리였는데, 논쟁이 오가던 당시 이미 수정이 진행 중이라는 지적이 **같은 스레드에 달렸다**" | ✅ | `REF §8-3` ⛔ 시점 함정 — `_ikke_`(2023-03-07, **같은 HN 35056594 스레드**): "dns-over-tcp has been added to musl and will be part of the next release." **⛔ "Alpine은 DNS over TCP를 지원하지 않는다"를 현재형으로 쓰지 않았다** | — |
| 8-16 | 2025년 9월 논거 교체 + `jauntywundrkind` 인용 2줄(나방/굿하트) — 단일 귀속 "— `jauntywundrkind`, 2025-09-08" | ✅ | `C2 §B-1` — **두 문장 모두 같은 발화자의 같은 댓글**(2025-09-08, HN 45164869)에서 나온다. 단일 귀속이 정확하다. 굿하트 법칙 설명도 원문에 있음 | — |
| 8-17 | `flohofwoe` 반론 / `masklinn` 재반박 (둘 다 같은 날) | ✅ | `C2 §B-1` — flohofwoe 2025-09-08(45166368), masklinn 2025-09-08(45166312) 축자·번역 일치 | — |
| 8-18 | **항목 19 / 정정 9의 ⚠️** — "**저 스레드는 JVM 이야기가 아니다.** 맥락은 Rust와 C 쪽이고, 대화 어디에도 자바나 JVM 언급이 없다. '그래서 Alpine 위의 스프링 부트가 느리다'로 이어 붙이면, 근거가 하지 않은 말을 우리가 대신 해주는 셈이다." | ✅ | **`C2 §B-1` ⚠️("이 스레드는 Rust/C 맥락이다. 스레드 안에 JVM 언급은 없다 … 자바로 확장 서술 금지")를 별도 문단으로 명시.** 계획 정정 9의 ⚠️⚠️ 조항이 회피를 넘어 **독자용 규율로 승격**됐다 — 모범 | — |
| 8-19 | **항목 A / 8장 마커** — "한편 2025~2026년 사이에는 'CVE 0건'을 내세운 베이스 이미지가 하나의 상품 범주로 등장했다는 관측도 있다. 이 책은 그 제품군의 1차 자료를 열어보지 못했으니 존재를 언급하는 선에서 멈춘다 **(사실 확인 필요)** — 각 벤더 공식 문서로 대조할 것." | **🕒** | `C2 §E-2`(465–473행)가 **존재 관측만** 보유한다 — "**'제로 CVE 베이스 이미지'가 2025~2026년의 상품 카테고리로 등장했다는 사실 자체는 확인된다**(Chainguard·Wiz 양쪽)". **단 같은 절이 ⛔ "HN 검색 결과 목록에서 제목·URL·점수만 확인했고 스레드를 열지 않았다. 인용 금지, 존재 근거로만"** 그리고 **"본문에 쓰려면 1차 소스(각 벤더 문서)로 다시 확인해야 한다"**고 못 박았다. 즉 **존재는 근거 있고 내용은 검증 불가.** 본문은 벤더명·제목·점수를 **하나도 쓰지 않고** 범주 존재까지만 서술 → 인용 금지 준수. 계획 8장이 지시한 `(1차 소스 확인 필요)` 표시를 저술가가 정확히 이행한 것이므로 **저술가 과실이 아니다.** 그러나 **마커가 최종본에 남으면 Phase 5가 차단된다** | **마커 처리(4-22 판례 적용):** 헤지 문장은 **그대로 유지**하고 편집 지시 문자열만 삭제한다. 정정문 — "…존재를 언급하는 선에서 멈춘다 **(사실 확인 필요) — 각 벤더 공식 문서로 대조할 것.**" → "…**존재를 언급하는 선에서 멈춘다. 이 축을 실제로 검토하게 되면 각 벤더의 공식 문서를 직접 열어 확인하자.**" ⛔ **해소한다고 벤더명(Chainguard·Wiz 등)·제품명·수치를 새로 넣지 말 것** — `C2 §E-2`가 인용을 금지한 자료다. 판정 근거는 이 로그 행이 보존한다 |
| 8-20 | JDK 21 축자 — "**Linux only:** The VM now provides automatic container detection support… **The default for this flag is `true`**, and container support is enabled by default." | ✅ | `W0 §E-8` 축자 일치. 중간 생략 구간("It uses this information to allocate system resources.")이 **`...`로 표시**됨 — 스플라이스 아님 | — |
| 8-21 | "기능 이름은 `UseContainerSupport`이고 기본값은 `true`" + `-XX:±UseContainerSupport` + 진단 "Use `-Xlog:os+container=trace` for maximum logging of container information." | ✅ | `W0 §E-8` 축자 일치 | — |
| 8-22 | **항목 20** — `PrintFlagsFinal` 출력 5줄(`ActiveProcessorCount = -1` / `InitialRAMPercentage = 1.562500` / `MaxRAM = 137438953472` / `MaxRAMPercentage = 25.000000` / `MinRAMPercentage = 50.000000`) + 명령 한 줄 + "(2026년 7월 25일, 호스트에서 실행)" | ✅ | `W0 §E-8` "로컬 실측 (2026-07-25, 이 책을 쓴 맥의 JDK 21.0.10)" 블록과 **명령·5줄·공백까지 문자 단위 일치.** JDK 21.0.10은 `PROBE §3`에서도 교차 확인(`openjdk version "21.0.10" 2026-01-20 LTS`). **실측 위조 없음** | — |
| 8-23 | **항목 20의 핵심** — "**위 값은 이 책을 쓴 맥의 그 JDK 빌드에서 관측된 것이지, 모든 JVM의 기본값이라는 근거가 아니다.** `MaxRAMPercentage`에 대한 공식 문서 기재는 이 책이 확보하지 못했다. 그러니 숫자를 외우는 대신 재는 법을 익히자." + "위 출력은 컨테이너 밖 호스트에서 잰 것이니" | ✅ | `W0 §E-8` ⚠️("공식 문서 인용은 `UseContainerSupport`·`ActiveProcessorCount`까지만 … 실측값을 별도 근거로") + `W0` 미확인 #4("`-XX:MaxRAMPercentage` 공식 문서 기재 … 로컬 관측값으로만 보유")를 **본문이 명시적으로 승계.** **⛔ 대체 퍼센트 값을 권하지 않았다**(전수 확인 — "30%로 잡아라" 류 0건). 계획 8장 ⛔ 완전 충족 | — |
| 8-24 | `-XX:ActiveProcessorCount` 축자 — "Overrides the number of CPUs that the VM will use to calculate the size of thread pools" + "**This flag is honored even if `UseContainerSupport` is not enabled.**" + 4장 콜백 | ✅ | `W0 §E-8` 축자 일치. **⛔ 4장의 수치(71.63%·σ 36.14·2단 스케줄링)를 반복하지 않았다** — 계획 라운드 1 M1 준수 | — |
| 8-25 | Memory Calculator — `Heap = Total Container Memory - Non-Heap - Headroom` + `MaxDirectMemorySize` 10MB / `ReservedCodeCacheSize` 240MB / `MaxMetaspaceSize` 자동 계산 / `-Xss` 1MB × 250 / 나머지가 `-Xmx` / 런타임에 `JAVA_TOOL_OPTIONS`로 부착 | ✅ | `W0 §E-8` Paketo 항목과 **값·단위 전부 일치.** ⚠️ `BPL_JVM_THREAD_COUNT`(미확인)를 쓰지 않았다 — 계획 ⚠️ 준수 | — |
| 8-26 | "can apply domain-specific knowledge to optimize the performance of Spring Boot applications" + 리액티브 웹 앱 스레드 수 50 | ✅ | `W0 §E-8` 축자 일치 | — |
| 8-27 | CDS/AOT 표 — AOT `Java 25+`(`-XX:AOTCacheOutput=app.aot` / `-XX:AOTCache=app.aot`), CDS `Java 24+`(`-XX:ArchiveClassesAtExit=application.jsa` / `-XX:SharedArchiveFile=application.jsa`), `-Dspring.context.exit=onRefresh` + "Java 25 이상에서는 CDS보다 AOT 캐시를 권한다"(표기 4.1.0 기준) | ✅ | `W1 §BellSoft Liberica` 축자 — 4개 플래그·2개 버전 전제·권고 전부 일치 | — |
| 8-28 | **항목 21** — "이 책이 실측에 쓴 맥의 자바는 **21.0.10**이라 둘 다 그대로는 쓸 수 없다. 여러분의 JDK부터 확인하고" | ✅ | `PROBE §3` 21.0.10 + 24/25 요구 대비 정확한 산술. 계획 ⚠️("독자의 JDK 버전 전제를 반드시 명시") 충족 | — |
| 8-29 | **항목 22** — 스프링 부트 OOMKilled 일화가 **없다** | ✅ | 8장 전수 grep — `OOMKilled`·`exit=137`·메모리 사고 일화 0건. `C2 §K`("자바 직결 0건. 없는 일화를 만들지 말 것") 준수 | — |

**총평:** 8장의 최고 위험 지점이었던 **`PrintFlagsFinal` 실측 5줄이 `W0 §E-8`의 로컬 실측 블록과 문자 단위로 일치한다** — 값이 그럴듯해서가 아니라 근거 파일에 실제로 있어서 통과했고, JDK 21.0.10도 `PROBE`에서 교차 확인된다. `MaxRAMPercentage`의 공식 문서 부재도 본문에 명시됐고 **대체 퍼센트 값을 권하지 않았다.** 정정 8·9 둘 다 정확히 적용됐다: Alpine 통설은 2023년 커뮤니티 발언으로 격하되고 반증 2건(태그명 `25-jdk-alpine-3.23` 정확, caveat이 musl libc를 가리킴)이 붙었으며, **musl 할당자 논거의 JVM 확장 금지는 별도 문단으로 명문화**됐다. 논문 3편(Harter·Khan·Verma)은 측정 연도·환경·프리프린트 단서를 전부 병기했고 Borg를 쿠버네티스로 옮기지 않았다. **유일한 BLOCKING은 마커 1건(8-19)이며, 판정은 🕒 — 코퍼스가 존재 근거만 보유하고 인용을 금지한 자료다. 헤지는 이미 완성돼 있으므로 마커 문자열 삭제만 남았다.**

---

## 배치 종합 (5~8장, 라운드 1)

| 챕터 | ✅ | ⚠️ | ❌ | 🕒 | 행 합계 |
|---|---|---|---|---|---|
| 5장 | 31 | 1 | 0 | 0 | 32 |
| 6장 | 27 | 1 | **1** | 0 | 29 |
| 7장 | 40 | 2 | 0 | 0 | 42 |
| 8장 | 28 | 0 | 0 | **1** | 29 |
| **합계** | **126** | **4** | **1** | **1** | **132** |

**BLOCKING 항목 2건:**
1. **6-2 (❌)** — 오프닝의 방향 오류. "맥에서는 그 이미지가 경고만 뜨고 잘 돌아간다" → **"맥에서는 그 이미지가 아무 경고 없이 그냥 잘 돌아간다."** 맥이 자기가 만든 arm64 이미지에 경고를 낸다는 근거는 코퍼스에 0건이며, `REF §3` 방향 표·`COMM` 375행·`C2 §L-3`이 모두 그 경고를 **서버 쪽**에 배치한다. 고칠 곳은 6장 9행 한 문장이며, 소절 2의 공통 패턴 요약(66행)은 방향 표 뒤에 있으므로 그대로 둔다.
2. **8-19 (🕒)** — `(사실 확인 필요)` 마커 제거. 헤지 문장은 유지하고 편집 지시 문자열만 삭제한다. ⛔ 벤더명·제품명 주입 금지.

이 2건이 해소되기 전에는 Phase 5(EPUB 빌드)로 넘어갈 수 없다.

**웹 2차 에스컬레이션:** 0건. 모든 Critical 주장이 레퍼런스 코퍼스 1차 대조로 판정됐다. **의심 식별자 검사:** 형식 이례 arXiv ID·미래 YYMM·미해결 DOI/URL·검증 불가 인용 **0건**. 8장의 `arXiv:2602.15214`는 2026-02로 빌드 시점(2026-07) 기준 과거이며 `PAPER`에 저자·날짜·URL·프리프린트 단서가 모두 기록돼 있다.

**축자 실재성 전수 스캔:** 4개 챕터의 인용문·명령·식별자·사용자명·날짜에서 추출한 **판별 문자열 약 215건**을 코퍼스 8개 파일 + `01_reference.md`에 일괄 대조했다. **미스 1건**(Borg "25 seconds")뿐이며, 그것도 근거 파일에 한국어 서술 "median typically about 25 s"로 존재해 실질 미스는 **0건**이다. 지어낸 인용·URL·사용자명·날짜는 발견되지 않았다.

**인용 스플라이스 검사(라운드 1에서 2건을 잡은 검사):** 이번 배치 **적발 0건.** 검사한 위험 지점 — 5-17(styfle, 문장 경계 종료) · 5-18(abiosoft, 원문 연속) · 6-13(velog 2건, 문장 경계) · 8-12(huksley, 생략을 `...`로 표시) · 8-20(JDK, 생략을 `...`로 표시). 서식 지적 1건(7-14, 원문 불릿 2개를 연속 산문으로 이어 붙임 — 순서 보존·생략 없음)만 ⚠️.

**커뮤니티 발언의 저자 목소리 승격 검사:** 0건. spockz·bmurphy1976·Shebanator·styfle·huksley·jauntywundrkind·flohofwoe·masklinn·hojooo·jdnurmi 전원이 발화자·시점과 함께 귀속됐고, 5장 지형 소절은 "**추천이 아니라 사람들이 무엇을 쓰고 무엇을 말하는지의 요약**"이라고 본문이 스스로 성격을 규정했다.

**⭐ 파일 우선순위 대조 축 (오케스트레이터 추가 지시) — 이 배치 결과: 위반 0건.**
2장의 "digest는 SHA256" 유형(1차 파일과는 일치하나 보강 파일이 교체한 판정)을 6개 표적 주제에 대해 재확인했다.

| 표적 주제 | 유효 판정 파일 | 본문이 인용한 근거 | 결과 |
|---|---|---|---|
| **Jib 멀티아키** | `W1`(FAQ 축자 확보) — `W0 §E-9`는 "버전·명령·플랫폼 서술 **미확인**"으로 자기 신고 | 7장이 `W1`의 매니페스트 리스트 축자·제약 4종·플러그인 버전을 인용 | ✅ **최신 판정 채택** |
| **베이스 이미지 / "Alpine JDK 부분집합" 반증** | `W1 §G3` + `REF §8-3`(반증 판정) — `COMM §6-1`은 통설의 **존재 근거**일 뿐 | 8장이 통설을 `huksley` 발언으로 격하하고 `W1`의 반증 2건을 인용 | ✅ **최신 판정 채택.** `W2`·`W3`는 이 주제를 다시 다루지 않아 `W1`이 여전히 최신 |
| **`--load` 제약(조건부)** | `W3 §T5` > `W1 §--load 제약의 진짜 조건` — `W0 §B-1`은 조건을 덜 갖춘 서술 | 6장이 `W1`의 3단 해소 + `W3 §T5-1·T5-2`의 판정 명령·기본값 축자를 인용 | ✅ **최신 판정 채택** |
| **Ryuk PR(병합 아님 반려)** | `C2 §I-2` > `COMM`/`REF §4-3`(2022년 논쟁까지만) | 5장이 `C2 §I-2`의 `mergedAt: null`·2026-02-03 반려를 인용하고 "지원한다는 말은 사실이 아니다"까지 명시 | ✅ **최신 판정 채택.** 리서처가 스스로 뒤집은 판정이 본문에 올바른 쪽으로 안착 |
| **Alpine 논거 교체(DNS → musl 할당자)** | `C2 §B-1` > `COMM §6-1`(2023년 DNS 논거) | 8장이 DNS를 **과거형**으로 쓰고("몇 년 전 대표 근거는") 2025-09 할당자 논거를 현재 논거로 배치 | ✅ **최신 판정 채택.** DNS를 현재형으로 쓰는 오류 없음 |
| **containerd 스토어 기본값(제품 라인)** | `W3 §T5-2` > `W1` | 6장이 Desktop 4.34+ / Engine 29.0+를 **제품 라인 구분과 함께** 인용 | ✅ **최신 판정 채택** |

**"일반형·조건부 → 특정형·절대" 좁힘 검사(이번 오류의 모양):** **적발 1건 — 6-2가 정확히 이 모양이다.** 다만 교체 관계가 파일 간(`W2`가 `W0`를 교체)이 아니라 **같은 파일 안**이다: `REF §3`의 두 방향 표·`COMM` 375행의 방향별 호스트 값이 조건을 나누는데, 같은 절의 **공통 패턴 압축 문장** 하나가 방향 1의 증상으로 두 방향을 대표한다. 본문은 그 압축 문장을 축자로 옮겼고 — 그래서 **축자 대조로는 통과했다** — 문맥이 방향을 arm64 이미지로 확정하는 바람에 근거보다 넓은 주장이 됐다. digest-SHA256 유형과 같은 실패 모드이며, 축자 검사만으로는 잡히지 않고 **조건을 나눈 표와 대조해야** 잡힌다. 나머지 지점에서는 **오히려 반대 방향이 관측된다.** 6-22(판정 명령을 한 방향으로만), 6-8·7-23·8-11·8-23(부재를 "확인한 페이지에서 못 찾음"으로 약화), 7-10(2단계 추론임을 노출), 7-4("데몬 불필요" 단정 회피) — 근거 파일의 조건·한계가 본문에서 **살아남거나 오히려 강화**됐다. 좁힘으로 볼 여지가 있는 것은 7-27(`docker login` 서버 생략 시 Docker Hub — 예제로만 뒷받침되는데 규칙문으로) 하나이며 ⚠️ 비블로킹으로 처리했다.

**계획 §0-4 사실 정정 13건 대조 — 이 배치 배정분 위반 0건:**

| # | 정정 | 배정 | 이행 |
|---|---|---|---|
| 6 | Ryuk `ryuk.disabled` 미지원(PR 반려) | 5장 | ✅ 5-28 — "병합 기록이 비어 있음"까지 본문에 노출 |
| 7 | Paketo 1회 1아키 / Jib 매니페스트 리스트 / **3파전** | 7장 | ✅ 7-1·7-2·7-5 — 증거 5건이 표 아래 증거 박스로 |
| 8 | "Alpine JDK = Java API 부분집합"은 반증 우세, 진짜 주의점은 musl libc | 8장 | ✅ 8-12·8-13·8-14 |
| 9 | Alpine 논거 교체(DNS → musl 할당자), **JVM 확장 금지** | 8장 | ✅ 8-15·8-16·8-18 — 확장 금지를 별도 문단으로 명문화 |
| 11 | "멀티플랫폼은 `--load` 못 한다"는 절대 규칙이 아니다 | 6장 | ✅ 6-18·6-19·6-21 |
| 13 | Desktop 4.34+ ≠ Engine 29.0+ (제품 라인) | 6장 | ✅ 6-20 — 독자용 규율로 승격 |

나머지 7건(1·2·3·4·5·10·12)은 11·12장 배정분으로 이 배치의 검증 범위 밖이다.

**계획 §0-3 금지 목록 대조 — 되살아난 항목 0건.** 전수 grep으로 확인: 로컬 K8s 배터리·발열 / 이미지 스캔 알림 피로 / 베이스 갱신 주기 실태 / rootless / 볼륨 마운트 성능 수치(`spockz`의 "3~4배" 미등장) / Colima "k3s 기반"(Colima의 Kubernetes 자체가 미등장) / 국내 사례 부재 포지셔닝 / 스프링 부트 OOMKilled / macOS `.docker/config.json` 경로 / `imagePullSecrets` 매니페스트(필드명조차 미등장) / 클래식 스토어 `DriverStatus` 역방향 단정 / `compose.yml` 예제 창작 — **전부 부재.**

**`PROBE` 일반화 검사:** 0건. 5장의 실측 4블록은 전부 "이 책을 쓴 맥에서 2026년 7월 25일에" 맥락과 함께 인용됐고 "표본은 하나다"라는 명시적 고지가 붙었다. Rancher Desktop 버전 3종(실측 1.17.1 / 릴리스 라인 / 컨트리뷰터 1.20.1)의 오연결도 없다 — 본문은 셋 중 어느 값도 인쇄하지 않았다.

**사실 판정 아님 — 인계 메모 (저술가·editor용, 비블로킹):**
1. 계획 6장이 지정한 클래식 스토어 에러 문자열(`ERROR: Multi-platform build is not supported for the docker driver…`)과 5장의 `stop.arguments[0]=--volumes`가 초안에 없다. **완결성 문제이지 정확성 문제가 아니므로** 팩트체커의 판정 대상이 아니다. 넣을 경우 근거는 `W3 §T5-2`·`W0 §E-6`에 축자로 있다.
2. 7장 그림 1(mermaid)의 `jib:build`·`jib:dockerBuild` 화살표 라벨은 `W1`의 태스크 구분과 일치한다 — 별도 조치 불필요.

---

## 라운드 3 추가 규약 (9~12장부터 적용)

**⭐ "낡은 근거 파일 통과" 축 — 라운드 3 확장.** 라운드 1의 2장 "digest = SHA256" 오류(1차 파일 `W0 §G-3`과는 일치하나 `W2 §A-1`이 명시적으로 금지한 단정)를 계기로, 이 배치는 **"본문이 어떤 근거와 일치하는가"에 더해 "그 근거가 이 주제에서 최신 판정인가"를 함께** 물었다. 이 배치에서 보강이 1차를 교체한 표적 주제 4건: Docker Desktop 내장 K8s의 kubeadm/kind 선택제(12장) · `ingress-nginx` 은퇴(12장) · K8s 도입 논쟁의 시점 이동(11장) · NodePort 범위 되살림(12장).

**축자 절단·무표시 생략 검사 기준(라운드 1에서 2건 적발):** 따옴표 안 문자열이 원문 문장 중간에서 끝나거나 원문의 삽입구를 말줄임 없이 들어냈으면 ⚠️. 문장 경계에서 끝나는 것은 통과.

---

## 9장. 코드를 고쳤는데 왜 그대로일까 — 태그·캐시·재현성

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/09_draft.md`
**집계:** ✅ 25 · ⚠️ 1 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 9-1 | velog 증상 축자 "spring 처음에 띄운 것 대로 nickname이 null로 들어가고 … 계속해서 nickname이 null로 들어가는 문제 발생" | ✅ | `C2 §G-1` 축자 완전 일치 | — |
| 9-2 | "velog, 「[springboot&docker] push한 도커 이미지가 적용이 안된다면?」 (2022-11-20 게시, 2026-07-25 검색)" | ✅ | `C2 §G-1` — 제목·게시일·검색일 전부 일치 | — |
| 9-3 | ⭐ **원인/증상 분리** — "가져올 수 있는 건 **증상**이다 … 반면 **원인**은 그렇지 않다. 글쓴이 본인이 그 대목을 '문제 예상 원인'이라고 적었고, 'Ec2에서 docker가 어떤 생태 흐름으로 흘러가는지는 모르나'라고 스스로 단서를 달았다. 그러니 그가 추정한 메커니즘은 이 책이 사실로 옮기지 않는다." | ✅ | `C2 §G-1` "⚠️ 정직한 한계" 4항을 **전부** 이행. ⛔ "저자가 추정한 메커니즘(가장 앞의 오래된 이미지를 run)을 사실로 옮기지 말 것"이 정확히 지켜졌다 — 본문에 그 메커니즘이 **등장조차 하지 않는다** | — |
| 9-4 | "**2022년 11월 글**이고, 운영 장애가 아니라 개발 성격의 배포다. '프로덕션이 죽었다'는 이야기로 부풀리지 말자." | ✅ | `C2 §G-1` 한계 1·2항 축자 대응 | — |
| 9-5 | ⭐ "**'그래서 그 서버가 왜 옛날 것을 돌렸는가'까지는 이 책이 말하지 않는다.**" | ✅ | 근거가 허용하는 경계에서 정확히 멈췄다. 계획 §7 9장 M5 지시 이행 | — |
| 9-6 | "이름이 같은 이미지가 그 EC2에 세 개 있었다고 적혀 있다" | ✅ | `C2 §G-1` 축자 "문제가 발생한 ec2에서 docker 이미지를 확인해보면 **같은 이름으로 3개가 있다.**" | — |
| 9-7 | "이제까지 무지성으로 사용했던 `-t`가 이름과 태그를 붙이는 옵션이었다. 태그명은 생략 가능한데, 생략하면 기본적으로 `latest`가 붙는다." | ✅ | `C2 §G-1` "무지의 자백" 축자 일치 | — |
| 9-8 | "If you specify `FROM alpine:3.21` in your Dockerfile, `3.21` resolves to the **latest patch version** for `3.21`." (2026년 7월 검색 기준) | ✅ | `W0 §D-3`(best-practices) 축자 + `REF` 재확인. 시점 병기 ✅ | — |
| 9-9 | "**같은 Dockerfile이 어제와 오늘 다른 이미지를 만든다.**" | ✅ | `W0 §D-3` 해설과 동일 결론. **⛔ "태그는 가변이다"를 OCI 스펙 인용으로 달지 말라**(`W2 §A-1`)는 금지를 지켰다 — 본문의 근거는 Docker best-practices 문장 + 레지스트리가 불변성을 옵션으로 판다는 사실(10장) 둘뿐 | — |
| 9-10 | OCI 축자 "The digest property of a Descriptor acts as a **content identifier**, enabling content addressability. It **uniquely identifies content by taking a collision-resistant hash of the bytes.**" | ✅ | `W2 §A-1` 축자 완전 일치 | — |
| 9-11 | `FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c` | ✅ | **의심 식별자 검사 통과.** `W0 §D-3` 373행에 Docker 공식 문서 예제로 축자 존재. 64자 hex 전수 대조 일치 — 날조 아님 | — |
| 9-12 | "By pinning your images to a digest, you're **guaranteed to always use the same image version**, even if a publisher replaces the tag with a new image." | ✅ | `W0 §D-3` 축자 일치 | — |
| 9-13 | ⭐ "위 예시가 `sha256:`으로 시작한다고 해서 digest가 곧 SHA-256인 것은 아니다. 스펙의 문법은 `algorithm \":\" encoded`라는 일반형이고, `sha256`은 실무에서 흔히 보게 되는 형태일 뿐이다." | ✅ | **라운드 1이 2장에서 놓쳤던 바로 그 오류의 정정판.** `W2 §A-1` "digest 알고리즘은 스펙상 `sha256` 고정이 아니다 … 'digest = sha256'으로 단정하지 마라"를 본문이 **독자용 규율로 승격**했다 | — |
| 9-14 | "실제로 태그 덮어쓰기를 막는 기능은 레지스트리가 **옵션으로 켜고 끄는 상품**이다 … 그 이야기는 운영 쪽 재료라 10장에서 다룬다." | ✅ | `W2 §A-2` 근거. 10장으로 정확히 이월 | — |
| 9-15 | 12장 예고 — "**쿠버네티스에서는 태그로 두느냐 digest로 박느냐가 이미지를 내려받는 동작까지 바꾼다.** 그건 12장의 몫이다." | ✅ | 계획 M6 준수. **정책 이름(`IfNotPresent`)을 여기서 말하지 않았다** — 4갈래는 12장 독점 | — |
| 9-16 | `--pull` 정의 "forces Docker to check for and download a **newer version of the base image**, even if you have a version cached locally." | ✅ | `W0 §D-3` 축자 일치 | — |
| 9-17 | `--no-cache` 정의 "**disables the build cache**, forcing Docker to rebuild all layers from scratch." | ✅ | `W0 §D-3` 축자 일치 | — |
| 9-18 | 세 갈래 구분 — "digest로 고정했다면 `--pull`은 아무것도 바꾸지 못한다 / 태그로 뒀다면 `--pull`이 베이스의 패치를 끌어온다 / 내 코드가 반영되지 않는 문제는 이 둘 어느 쪽도 아니다" | ✅ | 두 축자(9-16·9-17) + 9-8의 태그 해석 규칙에서 직접 따라 나오는 구분. 근거를 넘지 않는다 | — |
| 9-19 | 캐시 규칙 2축자 "a layer is reused … if **the instruction and the files it depends on hasn't changed**" / "a change causes a **rebuild for steps that follow**" | ✅ | `W0 §D-1` 축자 일치 | — |
| 9-20 | `.dockerignore` "apply to the **entire build context, including subdirectories**" | ✅ | `W0 §D-1` 축자 일치 | — |
| 9-21 | "Always combine `RUN apt-get update` with `apt-get install` in the same `RUN` statement" | ✅ | `W0 §D-1` 축자 일치 | — |
| 9-22 | 캐시 마운트 3줄(`/root/.npm`·`/root/.cache/pip`·`/var/cache/apt,sharing=locked`) + "문서에 실린 예시 그대로다" | ✅ | `W0` 345~347행 축자 3줄 완전 일치 | — |
| 9-23 | ⚠️ **저술가 확인 요청 지점** — "레이어 캐시가 **단계를 통째로 건너뛰는** 장치라면, 캐시 마운트는 **그 단계가 다시 돌아야 할 때 빈손으로 시작하지 않게** 해주는 쪽에 가깝다. … `npm install`은 다시 돌아간다. 다만 이미 받아둔 것을 또 받지는 않는다." | ⚠️ | **판정: 해석이 인용처럼 읽히지 않는다.** ① 따옴표 밖이고 ② 인용 귀속문("문서에 실린 예시 그대로다")이 **예시에만** 걸려 있으며 ③ "~쪽에 가깝다"로 완충됐다. 코퍼스에는 캐시 마운트의 **기능 정의 문장이 없고**(문법·예시뿐, `W0` 343~349행), 두 축자(9-19 레이어 캐시 규칙 + 캐시 대상 디렉터리)에서 끌어낸 저자 해석이 맞다. **다만 마지막 문장 "다만 이미 받아둔 것을 또 받지는 않는다"만 단정형**이라 앞 문장의 완충이 여기까지 미치지 않는다 | **비블로킹.** 권고: "다만 이미 받아둔 것을 또 받지는 **않는 것이 이 마운트의 취지다**" 정도로 한 어절 완충. 또는 앞에 "문서가 이 차이를 문장으로 설명하지는 않는다"를 한 줄 추가 |
| 9-24 | Gradle/Maven 캐시 — "**그 예시는 문서에 없다.** 원리상 같은 방식이 적용될 것 같지만, 이 책은 확인하지 못한 것을 확인한 척 쓰지 않기로 했다." | ✅ | `W0` 349행 "그 구체 예시는 문서에 없다. 직접 검증 후 쓸 것" + 계획 §10-3 폴백을 정확히 이행 | — |
| 9-25 | `docker buildx build --cache-from type=registry,ref=user/app:buildcache .` | ✅ | `W0` 352행 축자 일치 | — |
| 9-26 | "Build arguments and environment variables are **inappropriate for passing secrets to your build, because they persist in the final image.**" | ✅ | `W2 §C-1` 축자 일치 | — |
| 9-27 | ⛔ **`docker history`로 `ARG` 값이 보인다는 미확보 주장** | ✅ **부재 확인** | `W2 §C-1` 주의("그 축자 문장은 확보하지 않았다 — 'persist in the final image'까지만"). 본문 전수 검색 결과 **그런 문장이 없다.** `CREATED BY`에 대한 서술은 "그 레이어를 만든 명령"까지로, `ARG` 값 노출과 무관 | — |
| 9-28 | `RUN --mount=type=secret,id=aws \ AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \ aws s3 cp ...` + `--secret` 3형태(`src=`·`env=`·이름만) | ✅ | `W2 §C-1` 축자 4블록 완전 일치 | — |
| 9-29 | "The default file path of the secret, inside the build container, is `/run/secrets/<id>`." + "`id=aws`로 넘겼으면 빌드 중에는 `/run/secrets/aws`에서 읽는다" | ✅ | `W2 §C-1` 축자 일치. 파생 예시도 규칙에서 직접 따라 나온다 | — |
| 9-30 | `docker image history` "Show the history of an image" + 옵션 5행 표 + 컬럼 `IMAGE CREATED CREATED BY SIZE COMMENT` (2026년 7월 검색 기준) | ✅ | `W2 §A-7` 옵션 표·컬럼 축자 **행 단위 일치**(`--format`·`-H/--human` 기본값 `true`·`--no-trunc`·`--platform`·`-q/--quiet`) | — |
| 9-31 | "값은 여기 옮기지 않는다 — 문서의 예제 출력이 오래된 형식이라, 여러분이 직접 친 결과가 훨씬 정확하다" | ✅ | `W2 §A-7` 주의("예제 출력은 오래된 형식이다 … 컬럼 이름만 인용하고 값은 독자 실행 결과로") 정확 이행 | — |
| 9-32 | `--platform` — "다만 문서는 이 옵션이 있다는 것까지만 말한다. 그 이상의 활용법은 확인된 바 없으니 직접 쳐 보고 판단하자." | ✅ | `W2 §A-7` "확대 해석 금지" 준수 | — |
| 9-33 | `dive` 자기 규정 축자 + `brew install dive` + `CI=true` 통과/실패 + "물론 이건 이 도구가 자기 자신에 대해 하는 말이고, 이 책이 다른 도구와 견줘본 것은 아니다" | ✅ | `W2 §A-7` 축자 일치. **버전 숫자 미기재 ✅**, **"표준 도구"류 규범 표현 없음 ✅** | — |
| 9-34 | 10·12장 소관 침범 여부 | ✅ **없음** | 전수 grep: `scout`·`semver`·`crane`·`metadata-action`·`imagePullPolicy`·`IfNotPresent` **전부 0건** | — |

**총평:** 9장에 사실 결함 없음(❌ 0 / 🕒 0). 이 장은 이 배치에서 **근거 경계 준수의 시범 사례**다 — velog 글에서 증상만 취하고 글쓴이 추정 메커니즘을 본문에 아예 등장시키지 않았고, 라운드 1이 2장에서 놓쳤던 "digest = SHA256" 오류를 **같은 소절에서 정면으로 반박**한다(9-13). 저술가가 확인을 요청한 캐시 마운트 문단(9-23)은 **해석임이 충분히 신호돼 있어 통과**이며, 한 문장의 완충만 권고한다.

---

## 10장. 만든 뒤가 진짜다 — 갱신·스캔·승격

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/10_draft.md`
**집계:** ✅ 27 · ⚠️ 2 · ❌ 0 · 🕒 0

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 10-1 | "Vulnerability patching of software in Docker images is significantly delayed by **422 days on average**." — Liu et al., ESORICS 2020 §1 (**2019년경 수집**, 약 220만 개 이미지 조사) | ✅ | `PAPER` 논문 9 §1 축자 일치. 데이터셋 2,227,244개 ≈ "약 220만 개" ✅. 수집 시점 "2019년경"(추정임을 코퍼스가 명시) 병기 ✅ | — |
| 10-2 | "같은 조사에서 커뮤니티 이미지의 **64% 초과**가 고위험 또는 치명 등급 취약점을 갖고 있었다." | ⚠️ | `PAPER` 축자 "more than 64% of community images are affected by highly/critically severe vulnerabilities"와 **문면은 일치**(논문 자신의 문장). 다만 `PAPER` 인용 목록 #9가 **"인기 상위 10,000개 커뮤니티 저장소 기준 병기 필수"**로 못 박은 표본 조건이 본문에 없다 | **비블로킹 보강.** 권고: "커뮤니티 이미지의" → "조사 대상이 된 **인기 상위 1만 개 커뮤니티 저장소** 이미지의". 측정 연도·표본 규모는 이미 병기돼 있으므로 조건 한 개만 추가하면 §0-2를 완전히 만족한다 |
| 10-3 | 🕒 신선도 처리 — "이 숫자를 지금 이 순간의 사실로 읽으면 곤란하다. 수집 시점이 **2019년경**이고, 그 뒤 Docker Hub는 Docker Scout, 자동 스캔, Verified Publisher 같은 장치를 차례로 들였다 … 재측정값 역시 확보하지 못했다." | ✅ | `PAPER` 논문 9 "🕒 신선도 주의" 문단을 **거의 그대로** 이행. 계획 §7 10장 오프닝 지시 준수 | — |
| 10-4 | "논문이 지목한 원인 … 이미지 안의 프로그램들은 본류에서 떨어져 나와 있어서, 개발자가 그것을 갱신할 동기가 약하다" | ✅ | `PAPER` 축자 "the programs are decoupled from the mainstream ones, and developers are less incentivized to update programs in Docker images" | — |
| 10-5 | "The Docker Scout CLI plugin comes pre-installed with Docker Desktop." + Engine 단독은 별도 설치 | ✅ | `W1 §G3`(scout/install) 축자 2문장 일치 | — |
| 10-6 | "`docker scout`의 하위 명령은 **19개**다(2026년 7월 25일 조회 기준)" | ✅ | `W1` 하위 명령 전체 목록 표를 **기계 대조로 행 수 계수 = 19** 확인. 조회일 일치 | — |
| 10-7 | `quickview`/`cves`/`recommendations`/`sbom` 한 줄 규정 4개 | ✅ | `W1` 표 축자 4행 완전 일치 | — |
| 10-8 | "`compare`·`policy`·`environment`·`stream`에는 **`(experimental)`** 표시가 붙어 있다" | ✅ | `W1` 표 — 네 명령 전부 설명 끝에 `(experimental)` 확인 | — |
| 10-9 | Dependabot 최소 설정 YAML 4줄 + 주석 축자 2개 + 생태계 값 `"docker"`/`"docker-compose"` | ✅ | `W2 §A-6` 축자 완전 일치 | — |
| 10-10 | Renovate "Renovate supports updating Dockerfile dependencies." + 정규식 2줄 | ✅ | `W2 §A-6` 축자 일치(정규식 문자 단위 대조 통과) | — |
| 10-11 | ⛔ **"두 문서 모두, 서술 범위는 'PR을 여는 것'까지다. 'Dependabot이 재빌드를 트리거한다'고 읽으면 틀린다 … 그 연결을 명시한 1차 문장은 확보하지 못했다."** | ✅ | `W2 §A-6` 금지 지시를 **독자용 규율로 승격**. 계획 §7 10장 ⛔ 준수 | — |
| 10-12 | ⛔ **베이스 갱신 주기·빈도 실태**(§0-3 금지) | ✅ **부재 확인** | 전수 검색 — 실태·빈도 주장 0건. 등장하는 유일한 주기 값은 Dependabot 공식 예제의 `interval: "weekly"`이며 이는 **문서의 설정 예시**이지 실태 주장이 아니다. `pinDigests` 언급도 0건(`W2 §A-6` 금지 준수) | — |
| 10-13 | HN "Turn Dependabot off" 2026-02-20, 647점 + "원문 블로그는 이 책이 열어보지 않았으므로 글쓴이의 주장은 옮기지 않는다" | ✅ | `C2 §E-1` — 제출일·점수 일치. 인용 등급("블로그 원문 미열람 → 글쓴이 주장 인용 금지") 정확 이행 | — |
| 10-14 | `esafak` (2026-02-20) 축자 2문장 | ✅ | `C2 §E-1` 축자 일치. **문장 경계에서 종료** — 스플라이스 아님 | — |
| 10-15 | `seg_lol` (2026-02-20) "Time is a good **firwall**." + "원문의 `firwall` 오타 그대로" | ✅ | `C2 §E-1` 축자 일치. 오타 보존 + 명시 ✅ | — |
| 10-16 | `robszumski`의 자동 머지 질문 / `dotancohen`의 답 "No" | ✅ | `C2 §E-1` 자동 머지 반대파 항목 축자 일치 | — |
| 10-17 | "또 다른 참여자는 '몇 단계를 건너뛰고 내가 당신 인프라에 설치할 멀웨어 zip을 직접 보내줄 수도 있다'고 비꼬았다." | ⚠️ | 발언 자체는 `C2 §E-1` `UqWBcuFx6NV4r`로 실재("We could just skip some steps and I could send you a zip file of malware **for you to install on your infra** directly if you'd like."). 다만 한국어 렌더링에서 **설치 주체가 뒤집혔다** — 원문은 "당신이 설치하도록", 본문은 "내가 당신 인프라에 설치할" | **비블로킹 정정.** 권고: "몇 단계를 건너뛰고, **당신이 당신 인프라에 직접 설치할** 멀웨어 zip 파일을 내가 보내줄 수도 있다". 풍자의 요지(중간 단계를 생략하자)는 이렇게 해야 살아난다 |
| 10-18 | "정리하자면, **자동 머지에 대해 커뮤니티는 합의하지 않았다.**" | ✅ | `C2 §E-1`의 3파 구도(자동 머지+쿨다운 / 반대 / 도구 고백)가 **같은 스레드에 공존**한다는 관측 결과와 일치. 저자가 한쪽 편을 들지 않았다 | — |
| 10-19 | Renovate 메인테이너 `jamietanna`(2026-02-20)의 `govulncheck` 고백 | ✅ | `C2 §E-1` 🟢 항목 축자 일치. 메인테이너 신분 표기 정확 | — |
| 10-20 | ⛔⭐ **알림 피로 인용의 귀속 용접** — "같은 스레드의 `indiekitai`(2026-02-21)가 남긴 문장은 **의존성 스캐너를 두고 나온 말이지만**, 그 답을 가장 날카롭게 담고 있다." | ✅ | 계획 §7 10장 ⛔⛔("**Alert fatigue is a real attack surface.**를 홀로 세우지 마라 … 반드시 '의존성 스캐너를 두고 나온 말이지만' 식으로 귀속을 붙인다") **문자 그대로 이행** | — |
| 10-21 | `indiekitai` 축자 전문(코드 경로 미인지 → 12개 경고 → "Alert fatigue is a real attack surface.") | ✅ | `C2 §E-1` 축자 일치. 첫 문장("The core problem is that Dependabot treats dependency graphs as flat lists.")을 뺐으나 **문장 경계에서 시작**하고 내부 생략은 `…`로 표시 — 스플라이스 아님 | — |
| 10-22 | ⛔⛔ **알림 피로 금지선** — 소절 끝 "**여기 인용한 증언은 전부 의존성 스캐너 이야기다.** `docker scout`이나 그에 준하는 도구로 **컨테이너 이미지를 스캔한 뒤**의 알림 피로에 대해서는, 2026년 7월 25일 재검색에서도 인용할 만한 증언을 찾지 못했다. 위 문장들을 이미지 스캔 쪽으로 옮겨 읽지 말자." | ✅ **핵심 통과** | §0-3 최고 위험 항목. **전수 검색으로 이미지 스캔 알림 피로를 잇는 문장 0건 확인.** 소절 제목도 "쿨다운과 자동 머지 논쟁"으로 '스캐너'를 뺐고(계획 M3), 소절 위치도 Dependabot/Renovate 직후여서 **문맥이 이미 의존성 도구**다. `C2 §E-1` 📌 판정("컨테이너 이미지 스캔의 알림 피로는 여전히 0건")과 정확히 일치 | — |
| 10-23 | `wpollock`(2026-02-21) OWASP dependency-check + "이건 한 스레드의 표본 하나다. '자바 생태계엔 도달 가능성을 아는 도구가 없다'로 단정할 근거는 되지 못한다." | ✅ | `C2 §E-1` ⚠️ 지시("표본 하나이므로 단정 금지") 이행 | — |
| 10-24 | `docker/metadata-action`(**v6**, 2026년 기준) 파생 규칙 표 7행 | ✅ | `W2 §A-3` 축자 표와 **행 단위 대조 전부 일치**: `{{raw}}`→`v1.2.3` / `{{version}}`→`1.2.3` / `{{major}}.{{minor}}`→`1.2` / `v{{major}}`→`v1` / 프리릴리스 3행 전부 `2.0.8-beta.67` | — |
| 10-25 | ⭐ **프리릴리스 예외** — "`{{major}}` 패턴을 걸어도 `2`가 나오지 않는다 … **이동 태그가 베타를 가리키게 되는 일이 없다**" | ✅ | `W2 §A-3` ⭐ 해설과 동일 결론 | — |
| 10-26 | ⛔ **"semver 표준"이라 부르지 않았는가** | ✅ **통과** | 본문: "⚠️ 이 표의 출처는 **그 액션 자신의 README**다. 널리 쓰이는 구현이 채택한 규칙이라고는 말할 수 있어도, '**semver 태깅의 업계 표준**'이라고 부를 근거는 아니다." — `W2 §A-3` ⛔ 주의를 **부정형으로 명문화**했다. 계획이 허용한 표현("GitHub Actions 공식 액션이 채택한 규칙")도 본문 96행에 그대로 사용 | — |
| 10-27 | `type=sha` "Output Git short commit (or long if specified) as Docker tag like `sha-860c190`." + `latest`는 `flavor` 입력의 기본 `auto` 모드 | ✅ | `W2 §A-3` 축자 일치. `sha-860c190`도 코퍼스 실재(의심 식별자 아님) | — |
| 10-28 | `crane tag` "**Tag remote image without downloading it.**" + `crane tag ubuntu v1` + "매니페스트가 이미 존재한다는 것을 알기 때문에 레이어 존재 확인을 건너뛸 수 있고, 그래서 `tag`가 `copy`보다 조금 더 빠르다" | ✅ | `W2 §A-4` 축자 3건 일치. crane 버전 숫자 미기재 ✅ | — |
| 10-29 | `docker buildx imagetools create` — 자기 규정 "Create a new manifest list based on source manifests."를 **먼저** 제시하고 "'태그만 붙이는 명령'이 아니다"라고 명시 | ✅ | `W2 §A-4` ⚠️("자기 규정은 여전히 매니페스트 리스트 생성이므로 '태그만 붙이는 명령'으로 소개하지 말 것") 정확 이행 | — |
| 10-30 | "must already exist in the registry" + "carbon copy" 2축자 + `--prefer-index=false` 함정 | ✅ | `W2 §A-4` 축자 일치. ⛔ 함정 병기 의무 이행 | — |
| 10-31 | ECR 태그 불변성 축자 + `ImageTagAlreadyExistsException` | ✅ | `W2 §A-2` 축자 완전 일치 | — |
| 10-32 | "예외 필터를 두는 옵션(`IMMUTABLE_WITH_EXCLUSION`)도 함께 실려 있다. 다만 같은 페이지에 '모든 태그에 적용되며 일부만 불변으로 만들 수는 없다'는 옛 문장도 남아 있어서 **페이지 안이 서로 어긋난다**(2026년 7월 25일 조회). 그러니 'ECR은 전부 아니면 전무'라고 외우지 말고" | ✅ | `W2 §A-2` ⛔ 주의("페이지 내부가 자기모순이다. '전체 태그에만 적용된다'고 단정하지 마라") **완전 이행 + 조회일 병기** | — |
| 10-33 | ⭐ **GHCR "좁힘" 검사 대표 사례** — "**이 책이 확인한 컨테이너 레지스트리 문서 페이지에는 태그 불변성·덮어쓰기 방지에 대한 언급이 없었다.** 이것은 'GHCR에 그런 기능이 없다'는 뜻이 아니라, 확인한 문서에 나오지 않았다는 뜻이다." + Docker Hub "이번 리서치에서 조회하지 않았다" | ✅ **모범** | `W2 §A-2`("표기는 '확인한 페이지에 없음'으로만. 'GHCR에는 그 기능이 없다'로 격상 금지" / Docker Hub 🕒 미확인)를 **부재 판정의 성격까지 본문에서 해설**했다. **좁힘(부재→없음) 0건** | — |
| 10-34 | SBOM 설명 + `docker scout sbom`(조회) vs `--sbom=true`(생성)의 층위 구분 + `--provenance=mode=max` + "`mode=min` … 빌더와 출력 종류에 따라 조건이 붙는지는 확인하지 못했으니 무조건적인 기본값으로 여기지는 말자" | ✅ | `W2 §C-2` 축자·⚠️ 주의 일치. 층위 구분 명시 ✅ | — |
| 10-35 | `cosign sign $IMAGE` + "검증 쪽 명령은 이 책이 1차 소스로 확인하지 못했으니 sigstore 문서를 직접 확인하자" | ✅ | 계획 ⛔("`cosign verify` 명령·플래그는 미확보이므로 검증 명령을 쓰면 ❌") 준수 — **`cosign verify` 0건** | — |

**총평:** 10장에 사실 결함 없음(❌ 0 / 🕒 0). 이 배치 최대 위험 항목이었던 **알림 피로 금지선(10-22)이 인용 귀속 용접 + 소절 끝 명시적 부재 고지 + 소절 재배치 3중으로 방어**되어 이미지 스캔으로 번지는 문장이 한 줄도 없다. GHCR 부재 처리(10-33)는 이 배치에서 **"좁힘" 검사의 모범 답안**이다. ⚠️ 2건은 표본 조건 한 개 추가(10-2)와 번역 주체 정정(10-17)으로 각각 한 문장이면 닫힌다.

---

## 11장. 쿠버네티스는 언제 쓰는 기술인가

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/11_draft.md`
**집계:** ✅ 34 · ⚠️ 2 · ❌ 0 · 🕒 0
**인용 실재성:** 축자·핸들·스레드 ID·점수·날짜 **70건 전수 대조 — 미스 0건**

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 11-1 | "2020년 3월 … 「'쿠버네티스를 씁시다.' 이제 당신에겐 여덟 개의 문제가 생겼다」 … 719점에 댓글 469개(2026년 7월 25일 조회 기준)" | ✅ | `REF §4-1` / `COMM` — HN 22491170, 2020-03-05, 719 points, 469 comments. 조회 시점 병기 ✅ | — |
| 11-2 | `zeveb` 축자 3문장 — "If Kubernetes had only cost us a year and two hundred thousand dollars … **You don't need K8s until you start to build a half-assed K8s.**" (2020-03-05) | ✅ | `COMM` 557행 축자 완전 일치 | — |
| 11-3 | "그리고 마지막 문장이 **유명해졌다**." | ⚠️ | 인용 자체는 ✅. 다만 "유명해졌다"는 **그 발언의 수용·전파에 대한 주장**이며 코퍼스에 근거가 없다. `REF`·`COMM`은 이 문장을 "⭐" 표시로 강조하지만 그것은 리서처의 활용 가치 평가이지 대중적 유명세의 증거가 아니다 | **비블로킹.** 권고: "그리고 마지막 문장이 이 논쟁을 요약한다" 또는 "그리고 마지막 문장이 이 스레드에서 가장 자주 되풀이됐다"(후자를 쓰려면 근거 필요하므로 전자 권장) |
| 11-4 | `dangus` 축자 "'Avoid k8s' shouldn't mean 'avoid containers' because they have major velocity and reliability benefits for small teams with no ops engineers." — HN 44985447 (2025년 8월) | ✅ | `C2 §A-4` 표 축자 완전 일치. 스레드 ID·시점 일치 | — |
| 11-5 | "What Kubernetes is not" 5축자(PaaS 아님 / 소스 배포·빌드 안 함 + CI/CD는 조직 문화가 결정 / 애플리케이션 수준 서비스 미제공 / 로깅·모니터링·알림 미지시 / 설정 언어 미제공) | ✅ | `W0 §F-4` 축자 **5건 전부 문자 단위 일치**(Jsonnet 예시 포함) | — |
| 11-6 | "kubernetes.io, 2026년 7월 25일 조회" 시점 병기 | ✅ | `W0 §F-4` 검색일 일치 | — |
| 11-7 | 반대편 목록 10항(서비스 디스커버리·로드 밸런싱 / 스토리지 오케스트레이션 / 자동 롤아웃·롤백 / 자동 빈 패킹 / 자가 치유 / 시크릿·설정 관리 / 배치 실행 / 수평 확장 / IPv4-IPv6 듀얼 스택 / 확장성 설계) | ✅ | `W0 §F-4` "Why you need Kubernetes" 나열과 **항목·순서 일치** | — |
| 11-8 | dockershim — 공식 블로그(2022-02-17), Docker Engine이 CRI 미구현 → 전환용 코드 dockershim, "임시 해법으로 의도된 것이라 이름도 shim", 제거는 1.24, "All your existing images will still work exactly the same." | ✅ | `W0 §F-2` 축자 4건 일치. 발행일 정확 | — |
| 11-9 | ⚠️ **시점 고정** — "다만 시점을 붙들어야 한다. 아래는 전부 2020년 3월 스레드의 발언이다." | ✅ | 계획 §7 11장 ⚠️("반드시 '2020년 당시'로 명시") 이행. 소절 제목도 「**2020년의 논쟁** — 그때 오간 말들」 | — |
| 11-10 | `sho` — "출시가 6~12개월 밀리고 수십만 달러의 엔지니어링·데브옵스 시간을 낭비" + "k8s on day one at a startup is like a mom and pop grocery store buying SAP." + `(확인 필요 — 3자 전언, 검증 불가)` | ✅ | `COMM` 553~555행 축자 일치("6-12 months of launch delay and hundreds of thousands of dollars **in wasted engineering/devops time**"). **등급 마커도 `COMM` 555행 축자 그대로** | — |
| 11-11 | "다만 본인이 겪은 일이 아니라 아는 회사들 이야기라는 점은 기억해두자." | ✅ | 원문 "I personally know startups"의 정확한 성격 규정 | — |
| 11-12 | `mirko22` — "사용자 1000명에 초당 요청이 거의 0인 서비스를 GKE로 3개 대륙에 배포하느라 월 1만 유로" + 투자자 슬라이드 이유 + `(확인 필요 — 익명 개인 경험)` | ✅ | `COMM` 559~563행 축자 일치. 등급 마커 `COMM` 563행 축자 그대로 | — |
| 11-13 | `onion2k` 축자 "Choosing to build microservices is what adds complexity and makes tools like k8s necessary, not the business." | ✅ | `REF §4-1`·`COMM` 축자 일치 | — |
| 11-14 | `WnZ39p0Dgydaz1` — "이런 '너희에겐 k8s가 필요 없다' 글들에 지친다" + 2년 가까이 프로덕션 + "not a single service downtime, great fault-tolerance, and absolutely zero management effort" | ✅ | `COMM` 572행 축자 일치. **무작위형 핸들 실재 확인**(가장 날조 위험이 높았던 식별자) | — |
| 11-15 | `honkycat` — "Docker Compose든 ECS든 더 낮은 층위로 가면 결국 더 구린 버전의 쿠버네티스를 다시 만들게 될 뿐" | ✅ | `COMM` 578행 축자 대응. 발화자 귀속 ✅ | — |
| 11-16 | `avereveard` — "스케일이 아니라 환경 재현성 … 아무 브랜치나 네트워킹과 라우팅까지 프로덕션과 똑같이 띄울 수 있다" | ✅ | `REF §4-1` 축자 "we can spin any branch at any time on any provider and be sure it's exactly as we have it in production down to networking and routing" | — |
| 11-17 | "한쪽은 회사를 죽인다 하고 다른 쪽은 관리 노력이 0이라 한다. 어느 쪽이 거짓말을 하고 있을까? 아마 아무도 아닐 것이다." | ✅ | "회사를 죽인다"는 `sho`의 "can be a death sentence"(`COMM` 554행) 대응. 저자가 판정하지 않고 어긋남 자체를 재료로 남김 — 계획 지시 준수 | — |
| 11-18 | `herval` 축자 "However, hosted K8s options have improved significantly in recent years … it's become extremely easy to read & write deployment configs." — HN 44976292 (2025-08-21), 27점·댓글 50개 | ✅ | `C2 §A-1` 축자·메타데이터 완전 일치 | — |
| 11-19 | ⭐ **정정 12 적용** — "같은 스레드, 같은 날에 두 증언이 정면으로 부딪힌다. **그리고 둘 다 자체 운영이 아니라 매니지드 EKS 이야기다.**" | ✅ | `C2 §A-3` 맥락 축자가 **리서처 자신의 판정으로 동일 문장을 싣는다**: "A-2와 정면으로 충돌한다. 같은 스레드, 같은 날. … **둘 다 managed(EKS) 이야기다.**" 저자 추론이 아니라 근거 파일의 판정 승계 | — |
| 11-20 | `tnjm` 축자 + HN 44976744 (2025-08-21) | ✅ | `C2 §A-2` 축자 일치. 원문이 "managed k8s using EKS"로 **명시** | — |
| 11-21 | `therealfiona` 축자 2문장 + HN 44978566 (2025-08-21) | ✅ | `C2 §A-3` 축자 일치 | — |
| 11-22 | ⛔ **"매니지드를 쓰면 해결된다"로 결론내지 않았는가** | ✅ **통과** | 본문: "그러니 '매니지드를 쓰면 해결된다'는 정리는 하지 않겠다. 그건 합의가 아니다. 한쪽을 골라 결론으로 삼는 순간 근거의 절반을 버리게 된다." — 계획 §0-4 정정 12 정확 이행 | — |
| 11-23 | `elthor89` — "That's when I realized: we'd built a dependency on one person's specialized knowledge. And that knowledge had nothing to do with our actual product." + "**`elthor89`가 기사에서 인용**, HN 46577325 (2026-01-11)" | ✅ | `C2 §A-5` 축자 일치. **재인용 구조를 귀속에 명시**("기사에서 인용") — Medium 원문 미열람 제약 준수 | — |
| 11-24 | "2026년 1월, 쿠버네티스가 과했다며 Docker Compose로 내려왔다는 글이 올라왔고(22점, 댓글 17개)" | ✅ | `C2 §A-5` — HN 46576224, 2026-01-11, 22 points, 17 comments 일치 | — |
| 11-25 | "2020년의 질문은 '이 기술이 복잡한가'였고, 2026년의 질문은 '우리 조직이 그 지식을 감당할 수 있는가'에 가깝다." | ✅ | `C2 §A-5` "쓸 곳" 판정("무게중심이 '기술이 복잡하다'에서 '조직이 그 지식을 감당할 수 있는가'로 옮겨간 증거")과 동일. "~에 가깝다"로 완충 ✅ | — |
| 11-26 | `adieu` 축자 "k8s is raw technology like linux kernel. You shouldn't use it directly which will be hard to maintain. There are bunch of packaged solutions around k8s like Google GKE or AWS EKS." | ✅ | `COMM` 595행 축자 완전 일치 | — |
| 11-27 | ⭐ **저술가 확인 요청 지점** — `supermatt`의 "all of these pain points go away with a managed kubernetes" 뒤에 "**2020년 당시의 판단이며, `therealfiona`가 2025년에 매니지드 EKS를 두고 정반대 이야기를 했다는 사실과 나란히 놓고 읽는 편이 낫다.**" | ✅ **확인 완료** | `COMM` 596행 축자 일치. 시점 명시 + 2025년 반대 증언과의 병치가 **같은 문장 안에서** 이루어졌다. 2020년 판단이 현재형 처방으로 읽힐 여지가 닫혔다 | — |
| 11-28 | "**쿠버네티스를 쓴다와 쿠버네티스를 운영한다는 다른 결정이다.**" | ✅ | `REF §4-1` ⭐ 판정("`adieu`·`supermatt`의 구분이 이 논쟁의 열쇠다: 'K8s를 쓴다'와 'K8s를 운영한다'는 완전히 다른 결정이다")의 승계. 본문이 "**두 사람이 그은 선**"이라고 귀속 ✅ | — |
| 11-29 | 릴리스 주기 — "최근 세 개의 마이너 릴리스에 대해서만 릴리스 브랜치를 유지 / 1.19 이후 대략 1년의 패치 지원 / 'approximately three times per year' — 대략 연 3회(kubernetes.io, 2026년 7월 25일 조회 기준) / 유지되던 라인은 1.36·1.35·1.34 / 1.34의 수명 종료일 2026년 10월 27일" | ✅ | `W0 §F-1` 축자·표와 **전부 일치**(1.34 EOL = 2026-10-27). ⚠️ 코퍼스 상충 기록 2("도구 요약의 quarterly/연 4회는 오추정, 연 3회 채택")의 올바른 쪽을 인용했다. 시점 병기 ✅ | — |
| 11-30 | "이 책을 쓴 맥에 깔린 `kubectl` 클라이언트는 v1.32.1이다. 유지되는 세 라인이 1.34부터였으니 이미 범위 밖이고" | ✅ | `PROBE` §(kubectl) + `W0` 상충 기록 6. **"이 책을 쓴 맥에서" 맥락 병기 ✅** — §0-2 `PROBE` 일반화 금지 준수 | — |
| 11-31 | `skrebbel` 축자 "It seems to me that there's something of a gap between 'for single machine setups' (eg docker-compose) and 'for 500-engineer teams' (eg kubernetes)." | ✅ | `REF` 584행 축자 일치(따옴표 종류만 `REF` 렌더링을 따름 — 내용 동일) | — |
| 11-32 | `mrweasel` — 머신 두 대와 로드밸런서 + "when stuff breaks, you'll prefer that it's not the Kubernetes stuff." + "직접 굴린다면 디버깅이 극도로 복잡하다는 이유도 함께 들었다" | ✅ | `COMM` 593~594행 축자 3요소 전부 일치("because debugging it is extremely complex") | — |
| 11-33 | `supermatt` Compose 평가 + "**The same containers can run on both.**" | ✅ | `COMM` 596행 축자 일치 | — |
| 11-34 | `mosselman` — swarm 경로는 명령 한두 줄 + "I have looked into k8s and it wasn't as easy as this" | ✅ | `COMM` 598행 축자 일치 | — |
| 11-35 | ⚠️ **60시간 수치 처리** — "이 수치는 조심해서 다루자. 이 책은 원 기사를 열어보지 않았고, 확인한 것은 **그런 주장을 담은 글이 Hacker News에 올라왔고 댓글이 그 대목을 옮겨 적었다는 사실까지**다." | ✅ **적절 판정** | `C2 §A-5` ⚠️ 주의("'어떤 팀이 그렇게 말했다'가 아니라 '그런 주장을 담은 기사가 2026년 1월 HN에 올라왔고 댓글이 이 대목을 인용했다'로만 쓸 것. 수치를 사실로 단정 금지")를 **거의 축자로** 이행. 3중 재인용 구조(기사→HN 댓글→이 책)를 독자에게 전부 공개했다 | — |
| 11-36 | `halfmatthalfcat`(2026-01-11) — "throw the baby out with the bath water" | ✅ | `C2 §A-5` 축자 일치 | — |
| 11-37 | `theptip` — 2년 차부터 k8s, 엔지니어 15명까지 전담 운영 인력 불요 + 축자 "I was also very familiar with k8s ahead of time. I would not recommend someone in my shoes to learn k8s from scratch at the stage I rolled it out." | ✅ | `COMM` 574~575행 축자 일치("Year 2 onwards, k8s" / "we only needed to make our first dedicated ops hire after 15 engineers") | — |
| 11-38 | `mrweasel` 데이터베이스 논거 / `onion2k` 인과 논거 / `bertil` 가독성 / `TallGuyShort` 고객 요구 / `marcinzm` 채용 | ✅ | `REF §4-1` 기준표 + `COMM` 791행 대조 — 5건 전부 발화자 일치 | — |
| 11-39 | `more_corn` 축자 "If you can't immediately rattle off those three things, you don't need it." / `tdsanchez` 재설계 논거 | ✅ | `C2 §A-4` 표 축자 일치 | — |
| 11-40 | ⭐ **체크리스트 6문항 출처** — "새로 만든 기준은 없다 — 인용한 사람들의 문장을 당신 쪽으로 돌려놓은 것뿐이다." | ✅ **전수 추적 완료** | ①=`more_corn`(`C2 §A-4`) ②=`adieu`/`supermatt`(`REF §4-1`) ③=`elthor89`(`C2 §A-5`) ④=`mrweasel`(`REF §4-1`) ⑤=`tdsanchez`(`C2 §A-4`) ⑥=`onion2k`(`REF §4-1`). **6문항 전부 본문에 이미 인용된 발언에서 나오며 저자 창작 0건.** 계획 §7 11장 M4 지시("저자 의견이 한 줄도 추가되지 않는다") 이행 | — |
| 11-41 | ⭐ **등급 마커 2건**(`(확인 필요 — 3자 전언, 검증 불가)` · `(확인 필요 — 익명 개인 경험)`)의 최종 원고 잔존 가부 | ⚠️ | **판정: 사실 문제 아님, 잔존 허용.** 두 마커 모두 `COMM` 555행·563행의 **출처 신뢰도 등급을 축자로 옮긴 것**이며, 하네스가 금지한 저술 미완 마커 `(사실 확인 필요)`와는 성격이 다르다(전자는 독자에게 증거 등급을 알리는 서지 표기, 후자는 팩트체크 미해소 표시). **다만 Phase 4.5의 마커 스캔이 부분 문자열 `확인 필요`로 걸릴 경우 오탐한다** | **비블로킹, 표기 변경 권고.** 인식론적 등급을 유지하면서 충돌 토큰을 없애는 산문형 권장: `(확인 필요 — 3자 전언, 검증 불가)` → "**(본인이 겪은 일이 아니라 전해 들은 이야기라 검증할 수 없다)**" / `(확인 필요 — 익명 개인 경험)` → "**(익명의 개인 경험이다)**". 오케스트레이터·`manuscript-reviewer`에 **오탐 예상 2건**으로 인계 |
| 11-42 | ⛔ **저자 목소리 승격 검사(전수)** | ✅ **0건** | 18+16개 발언 전부가 발화자·시점과 함께 귀속됐다. 저자 단정으로 보이는 세 문장(11-25 축 이동 / 11-28 쓴다 vs 운영한다 / 11-19 둘 다 매니지드)은 **셋 다 근거 파일이 같은 판정을 명시한 것**의 승계이며, 나머지는 "~라는 것이다"·"~고 적었다" 형태로 발화자에 매여 있다 | — |
| 11-43 | ⛔ **2020년 논쟁을 현재형으로 쓴 곳** | ✅ **0건** | 소절 제목("2020년의 논쟁 — 그때 오간 말들")·도입("아래는 전부 2020년 3월 스레드의 발언이다")·개별 귀속(`(2020-03)` 9회)·`supermatt` 처리(11-27)까지 4중. 2025~2026 발언은 개별 날짜(2025-08-21 3회 / 2026-01-11 2회 / 2025년 8월 1회)로 구분 | — |
| 11-44 | ⛔ **인용 스플라이스 검사** | ✅ **0건** | 검사 지점 — 11-2(문장 경계 종료) · 11-10(원문 2문단을 한국어 요약 + 축자 인용으로 분리) · 11-14(도입부 한국어 요약 후 축자만 따옴표) · 11-20/11-21(원문 `…` 보존) · 11-37(문장 경계). **말줄임 없이 문장 중간을 자른 곳 없음** | — |
| 11-45 | `kubectl` v1.32.1에 붙은 서술 — "유지되는 세 라인이 1.34부터였으니 **이미 범위 밖**이고, **특별히 방치한 것도 아닌데 그렇게 됐다**" | ✅ | `W0` 상충 기록 6이 이 값에 **명시적 주의**를 붙인 유일한 11장 항목이다: "이 맥의 kubectl은 **지원 종료된 라인**의 클라이언트다. **버전 skew 서술의 실물 소재이지 '정상 상태'가 아니다.**" 본문은 ① "이미 범위 밖"으로 **비정상임을 먼저 못 박고** ② "특별히 방치한 것도 아닌데"를 **정상화가 아니라 그 반대 논거**로 쓴다 — 방치하지 않아도 지원 창 밖으로 밀려난다는 뜻이고, 이어지는 "그래서 업데이트는 끝나지 않는 업무가 된다"(`therealfiona` 증언에 귀속)로 곧장 연결된다. 코퍼스가 지정한 용도(버전 skew 소재)와 정확히 일치하며, "방치하지 않았다"는 **저자 자신의 맥에 대한 자기 보고**라 근거를 넘지 않는다 | — |

**총평:** 11장에 사실 결함 없음(❌ 0 / 🕒 0). 이 배치에서 커뮤니티 인용 밀도가 가장 높은 장인데도 **인용 실재성 70건 전수 대조 미스 0건**, 스플라이스 0건, 저자 목소리 승격 0건이다. 특히 위험했던 세 지점 — `supermatt`의 2020년 매니지드 낙관(11-27), 60시간 3중 재인용(11-35), 체크리스트의 저자 창작 혼입(11-40) — 이 **전부 계획이 지정한 처리를 그대로 따랐다.** ⚠️ 2건은 수사적 표현 완화(11-3)와 마커 표기 변경 권고(11-41)이며 둘 다 비블로킹이다.

---

## 12장. 맥에서 쿠버네티스를 켜보기 — 그리고 마지막 벽

**검증:** 2026-07-26 / 라운드 1 / 대상 `chapters/12_draft.md`
**집계:** ✅ 40 · ⚠️ 4 · ❌ 0 · 🕒 0
**YAML·명령 축자:** `diff` 바이트 대조 — **불일치 0건**

| # | 주장(원문 인용) | 판정 | 근거 | 조치 |
|---|---|---|---|---|
| 12-1 | ⛔ **정정 10** — Docker Desktop 내장 K8s 축자 "Choose your cluster type: **Kubeadm** creates a single-node cluster and the version is set by Docker Desktop. **kind** creates a multi-node cluster and you can set the version and number of nodes." + "스위치 하나를 켜면 클러스터가 뜨는 게 아니라, **어떤 종류의 클러스터를 만들 것인지 먼저 고르게 한다**" | ✅ | `REF §8-5` / `W1` 431행 축자 완전 일치. **"체크박스 하나" 옛 모델을 본문이 명시적으로 반박** — 낡은 근거 잔재 0건 | — |
| 12-2 | kubeadm vs kind 비교표 5행 | ⚠️ | `REF §8-5` / `W1` 표와 대조: 멀티 노드 No/Yes ✅ · 버전 선택 No/Yes ✅ · 프로비저닝 속도 ~1 min/~30 seconds ✅ · **Docker image store 호환 Yes/No** ✅ · containerd image store 호환 Yes/Yes ✅. **값은 전부 정확하나 문서 표의 `ECI 지원`(No/Yes) 한 행이 빠졌다.** 본문이 "문서가 함께 싣는 비교표"라고 소개해 전재로 읽힌다 | **비블로킹(서식).** 권고: 표 캡션에 "(발췌)"를 붙이거나 `ECI 지원` 행 복원. 라운드 2의 7-14와 같은 성격 |
| 12-3 | ⛔ **번들 K8s 버전** — "번들된 쿠버네티스 버전은 여기서 말하지 않겠다. 문서가 그 숫자를 적어 두지 않고, 안내하는 것은 `kubectl version`으로 직접 확인하는 방법뿐이기 때문이다." | ✅ | `REF §8-5` "문서에 명시 없음(확정)". **버전 숫자 0건** | — |
| 12-4 | kind 독립 도구 v0.32.0 / 2026 기준 + `kind create cluster` | ✅ | `W2 §B-5` 축자 일치 | — |
| 12-5 | ⛔ **Colima 명명** — "Colima를 쓴다면 `--kubernetes` 플래그로 쿠버네티스를 켤 수 있다(**어떤 배포판을 쓰는지는 Colima 문서가 밝히지 않는다**)" | ✅ | §0-3 금지("k3s 기반이라 부르지 말 것") 준수. 전수 검색 — "k3s 기반" 0건. **부재를 괄호로 명시**해 오히려 강화 | — |
| 12-6 | ⛔ **로컬 K8s 리소스** — minikube *최소 요구사항* 2 CPU/2GB/20GB, Colima *기본 할당값* 2 CPU/2GiB/100GiB, k3s 2코어·2GB는 *리눅스 노드 하드웨어 요구사항*(macOS 미언급) + "성질이 다른 세 수치를 한 줄에 세워 '최소 사양'이라 부르면 곤란하다" + kind "quick-start 페이지에 수치 자체가 없는데 그걸 '가볍다'로 읽지는 말자" + "**맥에서 실제로 얼마를 먹는지 잰 자료는 찾지 못했다**" | ✅ **모범** | `W2 §B-4` 표·축자·⛔ 주의 **4항 전부 이행**. §0-3 금지(배터리·발열·실측 소모)를 전수 검색 — **0건** | — |
| 12-7 | AMD64 튜토리얼 축자 "This tutorial uses a container that requires the AMD64 architecture. If you are using minikube on a computer with a different CPU architecture …" (2026-07-26 검색) | ✅ | `W3 §T1-6` 축자 완전 일치. 검색일 = `W3` 회차 일치 | — |
| 12-8 | Pod 정의 "Pods are the smallest deployable units of computing that you can create and manage in Kubernetes." | ✅ | `W3 §T1-5` 축자 일치 | — |
| 12-9 | ⭐ **2장 회수 축자** "The shared context of a Pod is **a set of Linux namespaces, cgroups**, and potentially other facets of isolation - the same things that isolate a container." + "**내가 이어 붙인 연결이 아니라 공식 문서의 문장이다**" | ✅ | `W3 §T1-5` 축자 일치. 저자 해석이 아님을 본문이 스스로 규정 | — |
| 12-10 | "Pods are generally not created directly and are created using workload resources." / "Usually you don't need to create Pods directly, even singleton Pods. Instead, create them using workload resources such as Deployment or Job." | ✅ | `W3 §T1-5` 축자 2건 일치 | — |
| 12-11 | "A Deployment provides declarative updates for Pods and ReplicaSets." | ✅ | `W3 §T1-1` 축자 일치 | — |
| 12-12 | ReplicaSet 권고 2축자 "we recommend using Deployments instead of directly using ReplicaSets, unless you require custom update orchestration or don't require updates at all." / "Do not manage ReplicaSets owned by a Deployment." | ✅ | `W3 §T1-1` 축자 일치. 출처를 "ReplicaSet" / "Deployments" 두 페이지로 정확히 분리 표기 | — |
| 12-13 | ⭐⭐ **Deployment 최소 YAML 21줄** | ✅ **바이트 일치** | `W3 §T1-2` **A안**(Deployment 페이지, `controllers/nginx-deployment.yaml`)을 임시 파일로 추출해 `diff` — **차이 0(코드 펜스 제외).** `labels` 존재 ✅ · `replicas: 3` ✅ · `replicas`가 `selector`보다 앞 ✅ · `nginx:1.14.2` ✅ · `containerPort: 80` ✅. ⛔ **B안(run-stateless, `replicas: 2`·`labels` 없음·필드 순서 다름)과의 혼입 0건** — 계획 §7 12장 (c) 최우선 제약 통과 | — |
| 12-14 | "`.spec.selector` 필드는 생성된 ReplicaSet이 어떤 Pod를 관리할지 찾는 방법을 정한다…" 축자 + "다른 컨트롤러와 라벨이 겹치지 않게 하라고 못 박는다" | ✅ | `W3 §T1-2` 필드별 해설 축자 + 라벨 충돌 경고 축자 대응 | — |
| 12-15 | `kubectl apply -f ./my-manifest.yaml` + "This is the recommended way of managing Kubernetes applications on production." | ✅ | `W3 §T3-1` 축자 일치. ⛔ **`kubectl create deployment`(명령형) 경로 0건** — 계획 지시 준수 | — |
| 12-16 | `get deployments` 출력 2줄(`nginx-deployment 0/3 0 0 1s`) + "'ready/desired' 형식이라 방금 만든 직후에는 정상인 값이다" | ✅ **바이트 일치** | `W3 §T1-3` 출력 블록 축자 일치. 컬럼 해설 축자("It follows the pattern ready/desired") 대응 | — |
| 12-17 | `kubectl rollout status deployment/nginx-deployment` | ✅ | `W3 §T1-3` 축자 일치 | — |
| 12-18 | `kubectl get rs` 출력 2줄(`nginx-deployment-75675f5897 3 3 3 18s`) + 이름 형식 `[DEPLOYMENT-NAME]-[HASH]` | ✅ **바이트 일치** | `W3 §T1-3` 축자 일치. **해시 `75675f5897`·나이 `18s`·`1s` 전부 코퍼스 실재** — 의심 식별자 아님(문서 예제 출력) | — |
| 12-19 | `kubectl get pods --show-labels` + "그 해시가 Pod 이름과 라벨에 그대로 붙어 있다" | ✅ | `W3 §T1-3` 축자(`pod-template-hash=75675f5897`) 대응. **낡은 `describe` 출력의 날짜·해시는 옮기지 않았다**(`W3 §T1-3` ⛔ 주의 준수) | — |
| 12-20 | Service 동기 축자 3연(동적 생성·소멸 / "This leads to a problem: …" / "**Enter Services.**") | ✅ | `W3 §T2-1` 축자 일치. 생략은 `…`로 표시, 인용 단위는 `/`로 분리 — 스플라이스 아님 | — |
| 12-21 | ⭐ **Service 최소 YAML 12줄** | ✅ **바이트 일치** | `W3 §T2-2` 축자와 `diff` 결과 차이 0. `app.kubernetes.io/name: MyApp` ✅ · `port: 80` ✅ · `targetPort: 9376` ✅ | — |
| 12-22 | "`port`는 Service가 받는 포트, `targetPort`는 Pod가 듣는 포트이며 안 적으면 같은 값이 된다" + 컨트롤러가 "selector에 맞는 Pod를 계속 훑는다" | ✅ | `W3 §T2-2` 축자 2건("By default and for convenience, the targetPort is set to the same value as the port field." / "continuously scans for Pods that match its selector") | — |
| 12-23 | Service 타입 4종 표(공식 설명 발췌) | ✅ | `W3 §T2-3` 축자 4행과 대조 일치. `ClusterIP`·`ExternalName` 행의 생략은 `...`로 표시 ✅, 표 머리글이 "(발췌)"를 명시 ✅ | — |
| 12-24 | "designed as nested functionality - each level adds to the previous" + "아무것도 안 적으면 `ClusterIP`다" | ✅ | `W3 §T2-3` 축자 일치. `ClusterIP` 기본값은 같은 페이지 3중 근거 | — |
| 12-25 | ⛔⛔ **NodePort 조건 2개 병기** — "30000–32767은 **`--service-node-port-range` 플래그의 기본값**이라 운영자가 바꿀 수 있고, 같은 문서가 그 범위를 다시 **정적 밴드 30000–30085**와 **동적 밴드 30086–32767**로 쪼갠다." | ✅ **핵심 통과** | `W3 §T2-4` 축자 #1·#3과 **수치 단위 일치.** §0-3·§10-2의 최우선 반복 확인 항목 — **조건 2개 모두 병기됐고 단독 인용 0건.** 본문이 "직접 박을 이유는 별로 없다"로 마무리해 밴드 언급의 위험도 낮췄다 | — |
| 12-26 | "The first step in debugging a Pod is taking a look at it." + `kubectl describe pods <이름>` | ✅ | `W3 §T3-4(a)` 축자 일치 | — |
| 12-27 | ⛔⛔ **4상태의 층위 구분** — 표에 "어디에 찍히는 값인가" 열을 두고 `Pending`=Pod **phase** / `Waiting`=**container state** / `ImagePullBackOff`·`CrashLoopBackOff`=kubectl이 보여주는 **Status** | ✅ **핵심 통과** | `W3 §T3-4` ⛔ 주의("네 개를 한 표에 'Pod 상태'로 나란히 놓으면 부정확하다. 층위 열을 두거나 산문으로 구분하라") 정확 이행. 본문이 "넷을 뭉뚱그려 'Pod 상태'라 부르지 않은 이유가 있다"고 **스스로 해설** | — |
| 12-28 | "Make sure not to confuse Status, a kubectl display field for user intuition, with the pod's phase." | ✅ | `W3 §T3-4(e)` 축자 일치 | — |
| 12-29 | ⭐ **저자 해석 2건 명시** — "`Pending`의 원인으로 문서가 첫손에 꼽는 것은 자원 부족이니, 맥에서 이 값을 만나면 앞 소절의 요구사항 표를 다시 보자 … `CrashLoopBackOff`의 원인 목록에도 눈에 익은 항목이 있다 … 4장의 한도와 8장의 힙 계산이 한 화면에 모이는 지점인데, **두 연결 모두 문서의 문장이 아니라 내가 놓은 다리다.**" | ✅ **명시 충분** | `W3 §T3-4(b)`·`(e)` ⚠️ 2건("그 인과는 저자 해석임을 밝혀라" / "공식 문서는 자바·JVM을 언급하지 않는다 — 확장 서술 금지")을 **한 문장으로 두 건 동시 해소.** 인용 축자("Resource constraints, where the container might not have enough memory or CPU to start properly")는 정확하고, **JVM·자바로 확장하는 서술이 없다**(4·8장 "연결" 언급까지만) | — |
| 12-30 | 롤아웃 — "태그를 바꿔 다시 `apply`하면 새 ReplicaSet이 생기고 옛 것은 0으로 내려간다" + "'`RollingUpdate` is the default value'다" | ✅ | `W3 §T1-4` 축자 2건 대응("creating a new ReplicaSet … scaling down the old ReplicaSet to 0 replicas" / `\"RollingUpdate\" is the default value`) | — |
| 12-31 | ⛔ **유추 표시** — "문서는 롤아웃이 '**if and only if the Deployment's Pod template is changed**' 트리거된다고만 적는다. '태그를 그대로 두고 apply하면 롤아웃이 안 일어나겠구나'는 거기서 읽어낸 **유추이지 문서의 문장이 아니다.**" | ⚠️ | **유추 표시 자체는 ✅**(`W3 §T1-4` ⛔ 제약 이행). 다만 인용 문자열이 원문의 삽입구를 **말줄임 없이** 들어냈다 — 원문 "if and only if the Deployment's Pod template **(that is, .spec.template)** is changed" | **비블로킹(축자).** 권고: "…Pod template **…** is changed"로 생략 표시하거나 삽입구 복원 |
| 12-32 | kind 적재 3명령(`kind load docker-image my-app:latest` / 복수 / `--name test-cluster`) | ✅ **바이트 일치** | `W2 §B-5` 축자 3줄 완전 일치 | — |
| 12-33 | minikube 4경로(`minikube image load` / `eval $(minikube docker-env)` / `minikube image build` / `minikube addons enable registry`) | ✅ | `W2 §B-5`·`W0 §F-3` 대응. 계획 §7 12장 소절 3 지시 항목과 일치 | — |
| 12-34 | `Waiting` 축자 "**The most common cause of Waiting pods is a failure to pull the image.** There are three things to check: …" + 3항목 체크리스트 | ✅ | `W3 §T3-4(c)` 축자 일치. "맥의 로컬 클러스터에서는 두 번째 항목의 답이 대개 '안 했다'이다"는 앞 문단의 kind 비호환 사실에서 직접 따라 나옴 | — |
| 12-35 | `ImagePullBackOff` "재시도 간격이 늘어나 **최대 300초(5분)**까지 벌어진다" | ✅ | `W3 §T3-4(d)` 축자("a compiled-in limit, which is 300 seconds (5 minutes)"). **설정 가능한 값처럼 쓰지 않았다** ✅ | — |
| 12-36 | ⛔ **`imagePullSecrets` 한 줄 고지** — "이 상태의 원인 목록에는 프라이빗 레지스트리에서 자격증명 없이 받으려는 경우도 있다. 쿠버네티스 쪽에도 별도 자격증명이 필요하다는 뜻인데, **그 설정은 이 책의 범위 밖이다.**" | ✅ **핵심 통과** | §0-3 `W3` 확인 실패 #1. **필드명 `imagePullSecrets`가 본문에 등장조차 하지 않고**, 매니페스트도 없다. 한 줄 고지 형태까지 계획 지시와 동일 | — |
| 12-37 | ⛔ **정정 5 — `imagePullPolicy` 4갈래** 표(digest→`IfNotPresent` / `:latest`→`Always` / **태그 생략→`Always`** / `:latest` 아닌 태그→`IfNotPresent`) + "**`imagePullPolicy` 필드를 생략했을 때만** 적용된다" | ✅ | `W2 §A-5` 축자 4갈래·⛔ 주의("생략했을 때만") **완전 이행.** 흔한 2갈래 통설을 "절반만 맞다"로 먼저 격하한 것도 근거 파일의 교정 취지와 일치 | — |
| 12-38 | 7장 태그 규칙과의 짝 — "도커에서 태그를 생략하면 `latest`가 붙고, 쿠버네티스에서 태그를 생략하면 pull 정책이 `Always`가 된다. **두 생략이 같은 방향으로 위험하다.**" | ✅ | `W3 §T4-3`(도커 태그 생략 규칙) + `W2 §A-5`(K8s 생략 규칙) 두 1차 축자의 병치. 계획 §7 12장 소절 3 ⭐ 지시 그대로 | — |
| 12-39 | `PROBE` 실측 컨텍스트 목록 + "로컬 클러스터가 둘이나 있는데 별표는 원격 EKS에 찍혀 있다 … **표본 하나짜리 관측이지만, 하필 이 책을 쓴 맥이 그랬다.**" | ✅ | `PROBE §5` 출력 일치(CLUSTER 열만 지면상 `…`로 축약). **"이 책을 쓴 맥에서" + "표본 하나" 2중 고지** — §0-2 `PROBE` 일반화 금지 준수 | — |
| 12-40 | `millerm` 축자 "Hah! I accidentally deleted a production deployment the other day … **I forgot that I had my context set to one of my AWS clusters.**" — HN 41578274, 2024-09-21 댓글 | ✅ | `COMM` 일화 5 축자 일치. 스레드 ID·댓글 날짜 정확(스레드 게시 2024-09-18 / 댓글 2024-09-21) | — |
| 12-41 | "같은 스레드에 '나도 당했다'는 사람이 **다섯 명 더** 붙었다." | ⚠️ | `COMM` 일화 5 신뢰도란은 "**최소 5명**이 독립적으로 '당했다'고 진술"이라고 적었고, 이는 `millerm`을 **포함한** 수로 읽힌다. 명시적으로 "burned/got burned"를 말한 추가 발화자는 `ed_mercer`·`lukaslalinsky`·`evnix`·`Telemaco019` **4명**이다(`cduzz`는 일반론) | **비블로킹.** 권고: "**네 명이 더**" 또는 "**여러 명이 더**" |
| 12-42 | 처방 스펙트럼 7단계 + `Telemaco019` "나도 zsh 설정에 넣어 뒀지만 그게 내가 망치는 걸 막아주지는 않았다" + `terinjokes`의 구조적 한계 지적 | ✅ | `REF §5-1 H7` / `COMM` H7 **7항목 순서까지 일치**(프롬프트 표시 → 확인 프롬프트 → `--context` 명시 → `KUBECONFIG`만 → current-context unset → 디렉터리 자동 전환 → 운영 kubeconfig 미보관). 두 반박 축자 대응 ✅. "이 질문에는 합의된 답이 없다" ✅ | — |
| 12-43 | ⛔ **규범 문장 금지** — "'실습 전에 컨텍스트를 확인하라'는 문장은 **공식 문서에 없다.** 공식 문서에서 가져온 것은 명령의 존재와 용법뿐이고, 확인하라는 당부는 위의 실측과 사고담에서 나왔다. 그러니 이건 규칙이 아니라 권유다." | ✅ **모범** | `W3 §T3-3` ⛔ 주의(NOT_PRESENT) 정확 이행 | — |
| 12-44 | `kubectl config get-contexts` / `current-context` / `use-context` 3명령 + 원문 주석 | ✅ **바이트 일치** | `W3 §T3-3` 축자와 주석·정렬까지 일치 | — |
| 12-45 | ⛔ **정정 3 — Ingress frozen** 2축자 병기 + "**동결(frozen)은 폐기(deprecated)가 아니다** … '**Ingress는 없어진다**'고 옮기면 공식 문서와 정반대의 말이 된다" | ✅ | `W2 §B-2` 축자 2건 일치. "곧 없어진다"류 서술 **0건** | — |
| 12-46 | ⛔ **정정 1 — `ingress-nginx` 은퇴** "**2026년 3월에 은퇴했고**, 이후로는 릴리스도 버그픽스도 보안 패치도 없다" + 성명 축자 2건 + "— Kubernetes 블로그, Steering·Security Response Committee 성명 (발행 2026-01-29)" | ✅ **핵심 통과** | `W2 §B-1` 축자 일치, 발행일 정확. ⛔ **일 단위 은퇴 날짜 0건**(전수 grep "3월 [0-9]" 미검출), ⛔ **"약 50%" 사용률 0건**(전수 grep "50%" 미검출) — 폐기된 값이 되살아나지 않았다 | — |
| 12-47 | ⛔ **정정 2 — minikube addon** "그래서 이 책은 `minikube addons enable ingress`를 실습으로 싣지 않는다. minikube 문서가 스스로 '**The ingress addon uses the ingress nginx controller**'라고 적고 있어(2026-07-26 재확인), 그 한 줄을 아무 말 없이 실으면 패치가 끊긴 컨트롤러를 깔라고 시키는 셈이기 때문이다." | ⚠️ | **사실·처리는 ✅** — 축자는 `W2 §B-6` 일치이고, 계획 §10-3이 지정한 폴백(애드온 제외, 노출은 `port-forward` → `cloud-provider-kind` 둘만)을 **정확히 적용**했다. 다만 **"(2026-07-26 재확인)"의 시점 표기가 코퍼스와 어긋난다** — 이 축자의 근거는 `W2`(검색 2026-07-25)이고, `W3`(2026-07-26)는 minikube 애드온을 다시 조회하지 않았다 | **비블로킹(시점 표기).** 권고: "(2026-07-25 확인)"으로 정정. 저술가가 실제로 저술 시점에 재조회했다면 그 사실을 별도 명기 |
| 12-48 | `kubectl port-forward svc/` · `deploy/` 2명령 + 주석 | ✅ **바이트 일치** | `W3 §T3-2` 축자 2줄 일치 | — |
| 12-49 | "`LOCAL_PORT:REMOTE_PORT`라고 적혀 있지만 오른쪽의 의미가 대상에 따라 다르다. `svc/`면 Service의 target port 이름, `deploy/`면 그 Deployment가 만든 Pod의 포트다. '**Service의 `port`로 간다**'고 뭉뚱그리면 틀린다." + "문서의 권고가 아니라 여기까지 따라온 **내 결론**이고" | ✅ | `W3 §T3-2` ⛔ 주의 2건("대상에 따라 다르다" / "'맥에서 권장 경로다'라는 공식 문장은 없다 — 저자의 결론임을 밝혀라") **둘 다 이행** | — |
| 12-50 | 실습 함정 축자 "The forwarding session ends when the selected pod terminates, and a rerun of the command is needed." | ⚠️ | 원문(`W2 §B-8`)은 "…and a rerun of the command is needed **to resume forwarding**." **문장 중간에서 잘린 뒤 마침표가 붙어 완결 문장처럼 보인다** | **비블로킹(축자).** 권고: 전문 복원 또는 "…is needed…"로 생략 표시 |
| 12-51 | ⛔⛔ **LoadBalancer 2층 인용** — ① **왜 그런가** = Service 공식 문서 축자("Kubernetes does not directly offer a load balancing component; you must provide one…") ② **화면에 무엇이 보이는가** = minikube 문서 축자("Note that without `minikube tunnel`, Kubernetes will show the external IP as **'pending'**") | ✅ **핵심 통과** | §10-2 반복 확인 #4. 본문이 **"두 겹으로 읽어야 정확한 현상이다"**라고 구조를 먼저 선언하고, 두 인용에 **각각 다른 출처·검색일**을 달았다(2026-07-26 Service / 2026-07-25 minikube). ⛔ **Service 문서를 "pending"의 출처로 단 곳 0건** — `W3 §T2-5`가 가장 경계한 오보가 발생하지 않았다 | — |
| 12-52 | kind 확인 흐름 `INGRESS_IP=$(kubectl get ingress example-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}')` + `curl ${INGRESS_IP}/foo` | ✅ **바이트 일치** | `W2 §B-3` 축자 일치(jsonpath 문자 단위 대조 통과). ⛔ **옛 `extraPortMappings` 레시피 0건** | — |
| 12-53 | ⭐⭐ **정정 4 — 마지막 벽** "Mac and Windows run the containers inside a VM and, on the contrary to Linux, the KIND nodes are not reachable from the host, so the LoadBalancer assigned IP is not working for users." — cloud-provider-kind README (2026-07-25 검색) | ✅ | `W2 §B-3b` 축자 완전 일치. 2장 모티프 회수 서술("맥의 컨테이너는 VM 안에 있다")도 근거 범위 안 | — |
| 12-54 | 우회 경로 — `brew install cloud-provider-kind` + "**맥에서는 `sudo`로 실행해야 한다**('On macOS and WSL2 you must run cloud-provider-kind using `sudo`')" + `--enable-lb-port-mapping` → `curl localhost:[port]` | ✅ | `W2 §B-3b` 축자 4건 전부 일치. 버전 숫자 미기재 ✅ | — |
| 12-55 | 최소 Ingress — "공식 문서의 최소 예제(`networking.k8s.io/v1`의 `minimal-ingress`)가 안전하다" + "Only creating an Ingress resource has no effect. You must have an Ingress controller to satisfy an Ingress." | ✅ | `W2 §B-2` 축자 일치. kind `usage.yaml`(내용 미확보)을 쓰지 않고 공식 최소 예제를 지목 — 계획 從 지시 준수. YAML 전재 대신 이름만 지목해 위험도 더 낮췄다 | — |
| 12-56 | 그림 1(K8s 오브젝트 관계) 노드·화살표 | ✅ | `W3 §Z-1` 근거 목록과 대조 — Deployment→ReplicaSet ✅ · ReplicaSet→Pod ✅ · Service selector 훑기 ✅ · 타입 계단("뒤 단계가 앞 단계에 얹힌다") ✅ · "Ingress — Service 타입이 아니다 / 클러스터의 입구 역할"은 축자 "Ingress is not a Service type, but it acts as the entry point for your cluster" ✅ | — |
| 12-57 | 그림 2(맥에서 끊기는 지점) | ✅ | `W2 §B-3b` 축자(호스트→KIND 노드 도달 불가 / 포트 매핑 우회)의 도해. 새 사실 추가 없음 | — |
| 12-58 | arXiv 전수 검색 — "초록에 `\"Docker Desktop\"`이 들어간 논문은 두 편뿐이었고, `\"Apple Silicon\"`과 컨테이너를 함께 다룬 논문 세 편 중 컨테이너 성능을 잰 것은 없었다(2026-07-25 전수 검색)" | ✅ | `PAPER` 인용 목록 #47·#48 / `REF §5-7` 일치. 실행일 병기 ✅ | — |
| 12-59 | 12장 매듭 — "클러스터 종류를 골라야 했고, 이미지를 손으로 밀어 넣어야 했고, 마지막에는 IP 하나에 닿지 못해 별도 프로세스를 `sudo`로 띄웠다" | ✅ | 계획 §10-4 중복 방지 준수 — **책 전체 회고(파일 공유·메모리 회계·소켓·아키텍처·CPU 제한 나열)가 없고** 12장 3단계 매듭까지만. editor 후기와 충돌하지 않는다 | — |

**총평:** 12장에 사실 결함 없음(❌ 0 / 🕒 0). **독자가 그대로 따라 칠 YAML 2종·명령 12블록·출력 3블록을 `diff` 바이트 대조로 검증한 결과 불일치 0건**이며, 특히 계획이 최우선 제약으로 못 박은 **두 Deployment 예제 혼입(12-13)이 발생하지 않았다.** §10-2가 반복 확인을 지시한 5개 항목(NodePort 조건 2개 · 4상태 층위 · `imagePullSecrets` 한 줄 · LoadBalancer 2층 · `ingress-nginx` 은퇴일) **전부 통과**했고, 폐기된 값(일 단위 은퇴일·50% 사용률·번들 K8s 버전·"k3s 기반"·실측 리소스 소모)은 **한 건도 되살아나지 않았다.** ⚠️ 4건은 표 한 행 복원(12-2)·축자 생략 표시 2건(12-31·12-50)·시점 표기 정정(12-47)·인원수(12-41)이며 전부 비블로킹이다.

---

## 배치 종합 (9~12장, 라운드 1)

**집계 합계: ✅ 126 · ⚠️ 9 · ❌ 0 · 🕒 0**

| 장 | ✅ | ⚠️ | ❌ | 🕒 | BLOCKING |
|---|---|---|---|---|---|
| 9장 | 25 | 1 | 0 | 0 | 없음 |
| 10장 | 27 | 2 | 0 | 0 | 없음 |
| 11장 | 34 | 2 | 0 | 0 | 없음 |
| 12장 | 40 | 4 | 0 | 0 | 없음 |

**⛔ BLOCKING 항목 0건. Phase 5 진행을 막는 사유가 없다.**

**⚠️ 전달 상태 (오케스트레이터 확인 요망):** 이 라운드의 판정 메시지를 `chapter-writer`에게 `SendMessage`로 보내려 했으나 **해당 에이전트에 도달할 수 없었다**(standalone 실행). 따라서 위 ⚠️ 9건은 **로그에만 존재하며 저술가에게 전달되지 않았다.** 다만 **게이트 판정은 이 전달에 의존하지 않는다** — ❌·🕒가 0건이므로 저술가 왕복이 불필요하고, 초안을 그대로 채택해도 사실 오류는 없다. ⚠️ 9건을 반영하려면 오케스트레이터가 이 로그의 각 장 표를 저술가에게 중계해야 한다.

**웹 2차 에스컬레이션: 0회.** 코퍼스 1차 대조만으로 전 항목이 판정됐다 — 판정 불가한 Critical 주장이 없었고, 의심 식별자도 0건이라 구속력 있는 웹 검증 대상이 발생하지 않았다.

**축자 실재성 전수 스캔(v1.8.0 하드블록):** 4개 챕터에서 추출한 판별 문자열 **약 200건**을 코퍼스 8개 파일 + `01_reference.md`에 공백 정규화 후 일괄 대조했다. 기계 미스는 7건이었고 **전부 서식 기인 위양성**으로 확인됐다 — 볼드 마커 삽입(`**Kubeadm**`·`**'Avoid k8s'…**`), 백틱 추가(`` `minikube tunnel` ``), 이스케이프된 따옴표(`\"RollingUpdate\"`), 인용부호 종류 차이(`"` vs `'`, `REF` 렌더링을 따름), 한국어 날짜 표기(`2026년 10월 27일` ↔ `2026-10-27`). **실질 미스 0건. 지어낸 인용·URL·핸들·날짜는 발견되지 않았다.**

**의심 식별자 검사(자동 ❌ 규칙 포함):** 4개 챕터의 식별자를 정규식으로 전수 추출했다 — arXiv ID **0건**, DOI **0건**, URL **0건**, sha256 digest **1건**, HN 스토리/댓글 ID **11건**. 전부 코퍼스에 실재한다. 특히 9장의 `sha256:a8560b36…3ef88c`(64자 hex)는 `W0 §D-3` 373행의 Docker 공식 문서 예제와 **문자 단위 일치**하며, 12장의 ReplicaSet 해시 `75675f5897`·나이 `1s`/`18s`는 `W3 §T1-3`의 문서 예제 출력이다. **미래 날짜 YYMM을 가진 식별자 0건. 검증 불가·형식 이례 식별자 0건.**

**인용 스플라이스 검사(라운드 1에서 2건 적발한 검사):** **적발 2건 — 둘 다 12장, 둘 다 ⚠️ 비블로킹.** 12-50(port-forward 함정 축자가 "…is needed."로 절단되어 완결 문장처럼 보임) · 12-31(롤아웃 트리거 축자에서 삽입구 "(that is, .spec.template)"를 말줄임 없이 제거). 나머지 검사 지점은 전부 통과 — 9-3·9-13(따옴표 밖 해설) · 10-21(`indiekitai`, 내부 생략 `…` 표시) · 10-14(`esafak`, 문장 경계) · 11-2/11-14/11-37(문장 경계) · 12-20(인용 단위를 `/`로 분리, 생략은 `…`) · 12-23(표 머리글에 "발췌" 명시).

**커뮤니티 발언의 저자 목소리 승격 검사:** **0건.** 11장 34개 발언·12장 6개 발언 전원이 발화자·시점과 함께 귀속됐다. 저자 단정처럼 보이는 세 문장(11-19 "둘 다 매니지드 EKS 이야기다" / 11-25 "축이 옮겨갔다" / 11-28 "쓴다와 운영한다는 다른 결정이다")은 검증 결과 **셋 다 근거 파일이 동일한 판정을 명문으로 싣고 있는 것의 승계**였다.

**⭐ 파일 우선순위 대조 축 — 이 배치 결과: 위반 0건.**
2장 "digest = SHA256" 유형(1차 파일과는 일치하나 보강 파일이 교체한 판정)을 이 배치의 표적 5주제에 대해 재확인했다.

| 표적 주제 | 유효 판정 파일 | 본문이 인용한 근거 | 결과 |
|---|---|---|---|
| **digest ≠ SHA256** | `W2 §A-1` > `W0 §G-3` | 9장 9-13이 "`sha256`은 실무에서 흔히 보게 되는 형태일 뿐"이라고 **명시적으로 반박** | ✅ **최신 판정 채택 — 라운드 1 오류의 정정판** |
| **NodePort 30000–32767** | `W3 §T2-4`(되살림, 조건 2개 병기 의무) > `W2 §B-8`·`§F-1`("쓰지 마라") | 12장 12-25가 **플래그 기본값 + 밴드 분할** 둘 다 병기 | ✅ **최신 판정 채택** |
| **Docker Desktop 내장 K8s** | `REF §8-5`(kubeadm/kind 선택제) > 옛 "체크박스 하나" 모델 | 12장 12-1이 옛 모델을 **본문에서 명시적으로 반박** | ✅ **최신 판정 채택** |
| **`ingress-nginx` 은퇴** | `W2 §B-1`·`§B-0`(2026-03 은퇴, 일 단위·50% 폐기) > 옛 튜토리얼 | 12장 12-46이 "2026년 3월"까지만, 12-47이 minikube 애드온 폴백 적용 | ✅ **최신 판정 채택. 폐기값 0건** |
| **K8s 도입 논쟁의 시점** | `C2 §A-1`~`§A-5`(2025~2026, 정정 12) > `REF §4-1`·`COMM`(2020) | 11장이 2020년 자료를 **소절 제목·도입·개별 귀속 3중으로 과거형 고정**하고, 2025~2026 자료를 별도 소절로 분리 | ✅ **최신 판정 채택. 2020년을 현재형으로 쓴 곳 0건** |

**"일반형·조건부·부재 → 특정형·절대·없음" 좁힘 검사(이번 오류의 모양): 적발 0건. 오히려 반대 방향이 지배적이다.** 이 배치에서 근거 파일의 조건·한계가 본문에서 **살아남거나 강화된** 지점 — 10-33(GHCR: "확인한 문서에 나오지 않았다는 뜻"이라고 부재의 성격까지 해설) · 12-5(Colima: 배포판 미기재를 괄호로 명시) · 12-6(kind: 수치 부재를 "가볍다"로 읽지 말라고 독자에게 직접 경고) · 12-3(번들 K8s 버전: 미기재이므로 말하지 않겠다고 선언) · 12-43(규범 문장이 공식 문서에 없음을 밝히고 "규칙이 아니라 권유"로 격하) · 9-24(Gradle 캐시 예시 부재 명시) · 9-32(`--platform` 확대 해석 자제) · 10-11(Dependabot의 서술 범위가 PR까지임을 규율로 승격) · 11-35(60시간을 3중 재인용 구조로 공개) · 10-23(자바 도구 표본 1건을 단정으로 만들지 않음). **좁힘의 반대인 "근거보다 좁게·약하게 쓰기"가 이 배치의 지배적 패턴이다.**

**계획 §0-4 사실 정정 13건 대조 — 11·12장 배정분 위반 0건:**

| # | 정정 | 배정 | 이행 |
|---|------|------|------|
| 1 | `ingress-nginx` 2026년 3월 은퇴, 성명 축자, **일 단위 날짜·50% 인용 금지** | 12장 | ✅ 12-46 — 축자 2건 + 발행일. 폐기값 전수 grep 0건 |
| 2 | `minikube addons enable ingress`는 은퇴한 컨트롤러를 설치, 경고 없이 싣지 말 것 | 12장 | ✅ 12-47 — 계획 지정 폴백(애드온 제외) 적용. ⚠️ 재확인 시점 표기만 보강 |
| 3 | Ingress는 frozen이나 **제거 계획 없음** — "곧 없어진다"도 틀림 | 12장 | ✅ 12-45 — 양쪽 축자 병기 + "동결은 폐기가 아니다" |
| 4 | kind 가이드의 `curl ${INGRESS_IP}/foo`가 맥에서 작동하지 않음(모티프 최종 회수) | 12장 | ✅ 12-52·12-53·12-54 — 확인 흐름 축자 → README 축자 → `sudo` 우회 3단 |
| 5 | `imagePullPolicy` 4갈래 + **생략했을 때만** 적용 | 12장 | ✅ 12-37 — 표 4행 + "생략했을 때만" 볼드 |
| 10 | Docker Desktop 내장 K8s는 kubeadm/kind 선택제, kind는 Docker image store 비호환 | 12장 | ✅ 12-1·12-2 — 옛 모델 명시 반박 + 비호환 항목을 소절 2개 뒤 실습 벽으로 회수 |
| 12 | K8s 논쟁에서 "managed 쓰면 해결"로 결론내지 말 것, 축은 "한 사람의 지식에 조직이 인질" | 11장 | ✅ 11-19·11-22·11-23·11-25 — 충돌 병치 + 결론 유보 명시 + 축 이동 서술 |

나머지 6건(6·7·8·9·11·13)은 5·6·7·8장 배정분으로 라운드 1·2에서 이미 이행 확인됐다.

**계획 §0-3 금지 목록 대조 — 되살아난 항목 0건.** 전수 grep으로 확인: 로컬 K8s 배터리·발열·실측 리소스 소모 / 스프링 부트 OOMKilled / **컨테이너 이미지 스캔 알림 피로**(최고 위험) / 베이스 갱신 주기·빈도 실태 / rootless / 볼륨 마운트 성능 수치 / 국내 사례 부재 포지셔닝 / **`imagePullSecrets` 설정법·매니페스트**(필드명조차 미등장) / 클래식 스토어 `DriverStatus` 역방향 단정 / macOS `.docker/config.json` 경로 / **Colima "k3s 기반"** / Renovate `pinDigests` / `cosign verify` — **전부 부재.**

**`PROBE` 일반화 검사:** 0건. 12장의 컨텍스트 실측은 "이 책을 쓴 맥에서"(223행) + "표본 하나짜리 관측이지만, 하필 이 책을 쓴 맥이 그랬다"(233행) 2중 고지, 11장의 `kubectl` v1.32.1도 "이 책을 쓴 맥에 깔린" 맥락과 함께 인용됐다.

**논문 수치 조건 병기 검사:** 422일 ✅(연도·표본 규모·재측정 부재 3중) / 64% 초과 ⚠️(표본 조건 1개 누락 → 10-2) / arXiv 전수 검색 결과 ✅(실행일 병기). `PAPER` 하드 규칙 #5("리눅스 네이티브 측정값이 맥 환경 값처럼 서술되면 ❌") 위반 0건 — 이 배치에는 성능 측정값 자체가 없다.

**사실 판정 아님 — 인계 메모 (비블로킹):**
1. **`manuscript-reviewer`(Phase 4.5) 오탐 예상 2건.** 11장 48행·52행의 등급 마커가 부분 문자열 `확인 필요`를 포함한다. **금지 마커 `(사실 확인 필요)`가 아니라 `COMM`에서 축자로 옮겨온 출처 신뢰도 표기**이며 팩트체크는 통과 판정이다. 11-41의 산문형 대체를 채택하면 충돌 자체가 사라진다.
2. **개인 식별 정보(editor·오케스트레이터 소관).** 12장 230행이 `PROBE` 출력을 그대로 실으면서 실제 개인 EKS 컨텍스트 문자열(`tobyilee@web-quickstart.ap-northeast-2.eksctl.io`)을 인쇄한다. 사실 정확성에는 문제가 없으나(실측 그대로) 발행물에 개인 계정·리전 정보가 노출된다. 익명화 여부는 팩트체커 소관이 아니므로 판정하지 않고 인계한다.
3. **완결성(정확성 아님).** 12장 12-2의 `ECI 지원` 행 누락은 표를 "문서가 함께 싣는 비교표"로 소개한 것과 어긋나지만, 실린 5행의 값은 전부 정확하다. 캡션에 "(발췌)"를 붙이는 것만으로 해소된다.
