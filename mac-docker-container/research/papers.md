# 논문 리서치: 컨테이너 격리·성능·보안 (tech-book)

**검색 시점:** 2026-07-25 / **genre:** tech-book / **슬러그:** mac-docker-container
**역할:** 실무서의 "원리" 챕터 뒷받침. 주력 아님. 확보 논문 9편.

> **작성 규율:** 아래 모든 저자·연도·발표처·페이지·수치는 **이 세션에서 직접 내려받아 연 PDF, 학회 공식 페이지, 또는 DBLP/arXiv API 조회 결과**에서 읽은 것이다. 기억에서 재구성한 항목은 없다. 서지 항목마다 어느 경로로 확정했는지 밝혔다(PDF 본문 ↔ DBLP 조회를 구분해 표기). 확보하지 못한 영역은 「미확인 목록」에 명시했다.

---

## ⚠️ 이 리서치를 쓰기 전에 반드시 읽을 프레이밍 노트

**아래 논문 8편 중 7편은 x86_64 리눅스 베어메탈(또는 x86 클라우드 VM) 환경에서 측정됐다.** 대상 독자의 환경(Apple Silicon 맥 + Docker Desktop)과 실행 스택이 다르다.

Apple Silicon 맥에서 컨테이너는 **리눅스 VM 안에서** 돈다(Docker Desktop의 LinuxKit VM, Apple Hypervisor.framework 위). 즉 독자가 체감하는 비용은:

```
독자가 보는 비용 = [컨테이너 오버헤드] + [VM 오버헤드] + [호스트↔게스트 파일/네트워크 경계]
                    ↑ 논문들이 측정한 것    ↑ 논문들이 측정하지 않은 것(대부분)
```

따라서 **Felter(2015)의 "컨테이너 ≈ 네이티브"나 van Rijn(2021)의 오버헤드 수치는 맥 사용자에게 "바닥값(floor)"이지 "관측값"이 아니다.** 본문에서 이 수치들을 쓸 때는 반드시 "리눅스 네이티브 기준"이라는 단서를 붙여야 한다.

**⚠️ 반대 방향 함정도 똑같이 위험하다.** "맥이니까 항상 더 느리다"로 일반화하면 안 된다. 논문 3의 Table 4를 문자 그대로 읽으면 맥의 OverlayFS 쓰기가 리눅스보다 200배 빨라 보이는데, 이는 가상화가 아니라 **M1 Pro 로컬 NVMe vs Azure 2 vCPU 네트워크 스토리지**라는 하드웨어 차이 탓이다. **서로 다른 측정 티어의 절대값을 나란히 놓는 문장은 방향과 무관하게 전부 무효다.** 유효한 것은 각 환경 **내부**의 비율 비교뿐이다(예: "리눅스에서는 볼륨이 OverlayFS보다 100배 이상 빠른데, 맥에서는 그 차이가 통계적으로 유의하지 않다").

이 간극을 직접 측정한 유일한 자료가 아래 **논문 4 (Khan 2026, arXiv 프리프린트)** 이며, 프리프린트라서 별도의 취급 주의가 필요하다(해당 항목 참조).

역설적이지만 이 책에 가장 유용한 인용은 **Felter et al.(2015)의 마지막 단락**이다 — 그들은 2015년에 이미 "컨테이너를 VM 안에서 돌리는 관행"에 의문을 제기했는데, 그게 정확히 Docker Desktop on Mac의 구조다. (논문 1 참조)

---

## 1. 컨테이너 vs VM 성능 오버헤드

### 논문 1 (고전) — An Updated Performance Comparison of Virtual Machines and Linux Containers

- **저자/연도/발표처:** Wes Felter, Alexandre Ferreira, Ram Rajamony, Juan Rubio (IBM Research, Austin, TX) / 2015 / **ISPASS 2015, pp. 171–172**
- **DOI:** 10.1109/ISPASS.2015.7095802
- **서지 출처 명시:** 저자·본문·수치·페이지 번호(171–172)·IEEE ISBN 라인(`978-1-4799-1957-4/15/$31.00 ©2015 IEEE`)은 아래 PDF에서 직접 확인. **학회명(ISPASS)·연도·페이지·DOI는 DBLP API 조회(2026-07-25)로 확정**했다 — PDF 본문에는 학회 풀네임 문자열이 없다. (선행 IBM Research Report RC25482는 별건이며 이번 세션에서 열지 못했다.)
- **URL:** https://people.computing.clemson.edu/~jmarty/projects/lowLatencyNetworking/papers/NFVandContainers/AnupdatedPerfAnalysisofContainersandVMs.pdf (2026-07-25 접속, PDF 직접 확인)
- **재현 자료:** 실험 스크립트 공개 — https://github.com/thewmf/kvm-docker-comparison (논문 SOURCE CODE 절)
- **핵심 발견:**
  - CPU·메모리에는 컨테이너·VM 모두 사실상 오버헤드가 없다. 비용은 **I/O와 OS 상호작용**에서만 발생한다.
  - MySQL(SysBench oltp) 실측: Docker는 네이티브 대비 고동시성 구간에서 **약 2% 차이로 수렴**, KVM은 **측정된 모든 구간에서 40% 이상 손실**.
  - AUFS(컨테이너 파일시스템에 DB 저장)는 상당한 오버헤드를 유발 — 볼륨을 쓰면 사라진다.
  - Docker의 NAT 네트워킹도 패킷률 높은 워크로드에 오버헤드를 준다.
- **측정 조건 (⚠️ 필수 병기):** IBM System x3650 M4, Intel Sandy Bridge-EP Xeon E5-2665 ×2 (총 16코어 + HT), 256GB RAM, NUMA. **Ubuntu 13.10, Linux 커널 3.11.0, Docker 1.0, QEMU 1.5.0, libvirt 1.1.1, MySQL 5.5.37.** cpufreq performance 거버너, 컨테이너는 cgroup 제한 없음, VM은 32 vCPU. **측정 연도 2014(발표 2015).**
- **인용할 만한 문장 (원문 그대로):**
  > "When both are tuned for performance, Docker equals or exceeds KVM performance in every case we tested." (p.172, §III Conclusions)

  > "Thus Docker using default settings may be no faster than KVM." (p.172, §II.B Discussion)

  > "Docker has similar performance to native, with the difference asymptotically approaching 2% at higher concurrency. KVM has much higher overhead, higher than 40% in all measured cases." (p.171, §II.A)

  > "We also question the practice of deploying containers inside VMs, since this imposes the performance overheads of VMs while giving no benefit compared to deploying containers directly on non-virtualized Linux." (p.172, §III)
- **이 책에서의 쓸모:**
  - "원리" 챕터에서 **"컨테이너는 왜 가벼운가"의 실증적 근거**로 — 프로세스일 뿐이라 CPU/메모리에 세금이 없다는 서술의 뒷받침.
  - 더 중요한 쓸모: **네 번째 인용문이 Apple Silicon 맥 상황의 정확한 묘사다.** "2015년 IBM 연구자들이 '컨테이너를 VM 안에 넣는 건 왜 하는지 모르겠다'고 썼는데, 여러분의 맥이 정확히 그 구조다" — 챕터 오프닝 훅으로 강력하다.
  - "볼륨 vs 이미지 레이어에 쓰기" 판단 기준의 학술적 근거(AUFS 오버헤드). 맥에서는 이 격차가 더 커진다(논문 4 참조).
- **🕒 신선도 주의:** **2014년 측정, Linux 3.11 / Docker 1.0 기준.** 이후 12년간 커널 I/O 스택(io_uring, virtio 개선), Docker 스토리지 드라이버(AUFS → overlay2), KVM 모두 크게 바뀌었다. **AUFS 관련 구체 수치는 오늘날 그대로 쓰면 안 된다**(overlay2가 기본). "CPU/메모리는 공짜, I/O는 아니다"라는 **구조적 결론만** 인용하고, 수치는 반드시 "2014년 측정" 병기.

---

### 논문 2 (최근 재측정) — A Fresh Look at the Architecture and Performance of Contemporary Isolation Platforms

- **저자/연도/발표처:** Vincent van Rijn, Jan S. Rellermeyer (TU Delft, Netherlands) / 2021 / **Middleware '21 — Proceedings of the 22nd International Middleware Conference, December 6–10, 2021 (Virtual Event, Canada)**
- **URL/arXiv:** arXiv:2110.11462 (2021-10-21 제출) — https://arxiv.org/abs/2110.11462
- **재현 자료:** 벤치마크 셋업 공개 — https://github.com/rellermeyer/container_benchmarks.git (논문 §3 각주 2)
- **핵심 발견 (Finding 번호는 논문 원문 번호):**
  - **Finding 2:** "All containers, including secure containers, perform on-par with native for CPU-bound tasks."
  - **Finding 6:** "The I/O performance of most systems is close to native except for the secure containers gVisor and Kata containers, and for the hypervisor Cloud Hypervisor."
  - **Finding 8:** "gVisor performance, in its current form, is severely hampered by the use of both the 9P protocol and separate Gofer architectural component."
  - **Finding 7:** Kata의 경우 **virtio-fs가 구형 9P를 크게 앞지르며, QEMU 플랫폼 수준까지 따라붙는다**(저자들이 추가 실험으로 확인).
  - **Finding 12:** gVisor는 네트워크 90퍼센타일 응답시간이 **경쟁 플랫폼의 3~4배**.
  - **기동 시간(§3.5, 플랫폼당 300회 반복):** **Docker ≈ 100 ms, gVisor ≈ 190 ms, Kata containers ≈ 600 ms, LXC ≈ 800 ms.** 그리고 **"creation of containers through the Docker daemon causes a slowdown of around 250 milliseconds in startup time"** (OCI 런타임 직접 호출 대비).
  - I/O 처리량: "The secure containers gVisor and Kata containers suffer severely from the extra layers of indirection, in the best case reaching **only half of the speeds** achieved using other isolation platforms."
  - 보안은 HAP(horizontal attack profile, 게스트가 호출하는 호스트 커널 함수 수) 지표로 근사 측정. **Finding 26:** "The secure containers, gVisor and Kata container, have relatively high numbers, especially compared to the regular containers." **Finding 28:** "The HAP metric fails to capture the defense-in-depth isolation platforms provide."
- **측정 조건 (⚠️ 필수 병기):** dual-socket **AMD EPYC2 7542** (각 64 스레드), **256 GiB RAM**, 전용 고속 NVMe SSD, **Ubuntu Linux Server 20.04 LTS**. 별도 명시 없으면 최소 10회 반복(기동 시간은 300회). 벤치마크: ffmpeg H.264→H.265 재인코딩(1080p 30MB, 16코어/16스레드), Sysbench CPU, tinymem, fio(128kB libaio 처리량 / 4kB randread 레이턴시), Netperf, MySQL Sysbench oltp_read_write, Memcached. **측정 연도 2021.**
- **인용할 만한 문장:**
  > "We find that container platforms have the best, near-native, performance while the newly emerging secure containers suffer from various overheads. The highest degree of isolation is achieved by unikernels, closely followed by traditional containers." (Abstract)

  > "Docker is very fast to boot, taking around 100 ms, followed by gVisor at around 190 ms. Much later, at 600 ms and 800 ms, we see the Kata container and LXC platforms, respectively." (§3.5)
- **이 책에서의 쓸모:**
  - **"격리를 더 세게 하면 뭘 잃는가"의 정량적 답.** gVisor/Kata를 "그냥 더 안전한 Docker"로 오해하는 독자에게 트레이드오프의 실제 크기를 보여준다.
  - **"Docker 데몬이 250ms 붙는다"는 실무 감각 수치** — `docker run`이 느껴지는 이유의 일부를 설명. (단, 이건 리눅스 네이티브 기준. 맥은 논문 4 참조.)
  - 9P vs virtio-fs 대목은 **맥의 파일 공유 성능 논의로 곧장 연결된다** — Docker Desktop의 bind mount 역시 호스트↔게스트 파일 공유 프로토콜 문제이고, 이 논문이 "공유 파일시스템 프로토콜이 격리 플랫폼 I/O 성능의 주범"임을 일반화해 보여준다.
- **🕒 신선도 주의:** **2021년 측정, gVisor·Kata·Cloud Hypervisor 당시 버전 기준.** gVisor는 이후 9P를 대체하는 방향(LISAFS 등)으로, Kata는 virtio-fs 기본화 방향으로 개선됐다는 게 커뮤니티 상식이므로, **"gVisor는 느리다"를 현재형 단정으로 쓰지 말고 "2021년 측정 시점에는"으로 한정**할 것. 논문 스스로도 Finding 7·9에서 개선 방향을 지목한다.

---

### 논문 3 (⭐ 맥 환경 직접 측정 / 프리프린트) — Decomposing Docker Container Startup Performance: A Three-Tier Measurement Study on Heterogeneous Infrastructure

- **저자/연도/발표처:** Shamsher Khan (단독 저자) / **2026-02-16** / **arXiv 프리프린트 (동료심사 미확인)**
- **arXiv:** arXiv:2602.15214 — https://arxiv.org/abs/2602.15214
- **재현 자료:** "All measurement scripts, raw data, and analysis tools are publicly available." (Abstract; 논문 참조 [25])
- **⚠️ 취급 주의 (이 항목만 규칙이 다르다):**
  1. **프리프린트다.** 동료심사 통과 여부 미확인, 단독 저자, 학회/저널 게재 정보 없음. → 본문에서 인용한다면 **"arXiv 프리프린트"임을 명시**하고 단정 근거로 삼지 말 것.
  2. **저자 본인의 한계 고지:** "We emphasize that the macOS results are intended to characterize developer environments rather than provide an architectural comparison with cloud CPUs." (§3.1) → **"Docker Desktop 가상화 세금 2.69배"는 하드웨어 차이(M1 Pro 랩톱 vs Azure 2 vCPU Xeon VM)가 섞인 수치다.** 순수 가상화 오버헤드로 읽으면 안 된다.
  3. 또 다른 한계: "On macOS, cache clearing cannot reach Docker Desktop's internal VM caches, documented as a limitation." (§3.3)
  4. **🚫 티어 간 절대값 비교 금지 (이 파일에서 가장 위험한 함정).** 세 플랫폼은 하드웨어가 완전히 다르다 — **M1 Pro 랩톱 + 로컬 NVMe/APFS** vs **Azure Standard_D2s_v3 (2 vCPU) + 네트워크 연결 스토리지**. 특히 Table 4를 문자 그대로 읽으면 "맥의 OverlayFS 쓰기(238.1 MB/s)가 리눅스(1.1 MB/s)보다 200배 빠르다"는 **완전히 잘못된 문장**이 나온다. 이건 가상화 얘기가 아니라 로컬 NVMe vs 네트워크 스토리지 얘기다.
     → **유효한 주장은 "티어 내부(within-tier) 비율"뿐이다:** OverlayFS 대 볼륨 비율이 SSD 0.006× / HDD 0.010× / **macOS 1.06×(유의하지 않음)** 라는 것. 즉 "리눅스에서는 볼륨이 압도적으로 유리한데, 맥에서는 그 차이가 사라진다"는 **비율의 대비**만 쓴다. 티어 간 절대 MB/s 수치를 나란히 놓지 말 것.
- **핵심 발견 (Finding 번호는 논문 원문):**
  - **Finding 1:** 이미지 크기는 기동 시간에 거의 영향이 없다. Premium SSD에서 **5MB(alpine) ~ 155MB(python:3.11-slim)** 이미지 간 warm-start 편차가 **554–568 ms, 즉 2.5%**. "Runtime overhead (namespace creation, cgroup setup, OverlayFS mount preparation) dominates."
  - **Finding 3:** "Docker Desktop virtualization tax is 2.69×. macOS (1528 ms) vs. SSD (568 ms) for alpine. For nginx, the penalty reaches 3.28×. This originates from the LinuxKit VM, virtio block device, and hypervisor scheduling."
  - **네임스페이스 생성 비용 (§4.2.1):** **7.94 ms (SSD, σ=2.05), 8.45 ms (HDD, σ=2.57)** — **전체 기동 시간의 1.5% 미만.** "Near-identical results confirm this is CPU-bound, not I/O-bound—a platform-invariant primitive."
  - **분산(§4.1.2):** 변동계수 CV — Premium SSD **3.4%**, Standard HDD **8.3%**, **macOS 32.8%**.
  - **CPU 제한 정확도(§4.2.2):** `--cpus=0.5`(목표 50%)일 때 실측 — SSD μ=**60.52%** (σ=3.79), HDD μ=**48.21%** (σ=16.24), **macOS μ=71.63% (σ=36.14), 이상치 최대 247%.** "The 9.5× variance increase from SSD to macOS demonstrates that two-level scheduling (macOS → LinuxKit → CFS) produces compounding inaccuracy."
  - **네트워크(§4.2.3):** bridge vs host 네트워크 차이는 SSD에서 0.04 ms, HDD에서 0.06 ms로 무시 가능. **"On macOS, both modes show ∼34 ms RTT (17× slower) because all traffic traverses the hypervisor's virtual network."**
  - **OverlayFS vs 볼륨 쓰기 처리량(§4.3.1, 256MB 순차 쓰기, 중앙값 MB/s):** Prem. SSD **1.1 vs 194.0 (0.006×)**, Std HDD **1.3 vs 136.6 (0.010×)**, **macOS DD 238.1 vs 224.5 (1.06×, p=0.21 — 유의하지 않음)**. macOS에서 차이가 없는 이유는 "Docker Desktop's virtio layer already serializes I/O."
  - **페이지 캐시 공유(§4.3.3):** "Page cache sharing efficiency is approximately 0% across all platforms: three identical nginx containers consume 3× the memory of one."
  - **warm-start 표 (Table 3, ms, mean ± 95% CI, n=50):**

    | 플랫폼 | alpine | nginx | python |
    |---|---|---|---|
    | Prem. SSD | 568 ± 5 (σ=19) | 564 ± 12 (σ=42) | 554 ± 6 (σ=22) |
    | Std HDD | 1157 ± 27 (σ=96) | 1287 ± 36 (σ=131) | 1334 ± 35 (σ=126) |
    | **macOS DD** | **1528 ± 139 (σ=502)** | **1850 ± 155 (σ=560)** | **1859 ± 139 (σ=502)** |

- **측정 조건 (⚠️ 필수 병기):** 3개 티어 비교 (Table 2).
  - Azure Premium SSD: 2 vCPU (Xeon), 8GB, SSD(LRS), Docker 28.x, overlay2, 가상화 없음
  - Azure Standard HDD: 2 vCPU (Xeon), 8GB, HDD(LRS), Docker 28.x, overlay2, 가상화 없음 (둘 다 Standard_D2s_v3)
  - **macOS Docker Desktop: Apple M1 Pro, 16GB, APFS/VM, Docker 28.4.0, overlayfs, Hypervisor.framework (HV.f)**
  - 이미지: `alpine:latest`(5MB, 1 레이어), `nginx:latest`(67MB, 7 레이어), `python:3.11-slim`(155MB, 5 레이어)
  - 반복: 측정당 50회(pull 테스트 n=10, cold start n=20). Mann-Whitney U 검정(α=0.05), Cliff's delta 효과크기. **측정 연도 2026.**
- **이 책에서의 쓸모:** **이 책의 핵심 논거 여러 개를 직접 뒷받침한다.**
  - "원리" 챕터: **네임스페이스 생성은 8ms, 전체 기동의 1.5% 미만** — "컨테이너가 느린 건 리눅스 격리 원시요소 탓이 아니다"를 수치로 못 박는다. 최적화 타깃을 잘못 잡는 독자를 바로잡는 데 최적.
  - 맥 챕터: **CPU 제한(`--cpus`)이 맥에서 잘 안 먹는다**는 실무 관측(σ=36, 이상치 247%)의 근거. 자바 개발자가 `-XX:MaxRAMPercentage`나 CPU 코어 인식으로 겪는 혼란과 직결.
  - 볼륨 챕터: **리눅스에서는 볼륨이 OverlayFS보다 100배 이상 빠른데, 맥에서는 그 차이가 사라진다**(둘 다 virtio에 막혀서). "리눅스에서 통하는 조언이 맥에서 안 통하는" 대표 사례.
  - 이미지 최적화 챕터의 **찬물 끼얹기 근거**: 이미지 크기를 5MB로 줄여도 warm-start는 2.5%밖에 안 줄어든다. (단, **cold start / pull 시간은 별개**임을 반드시 구분할 것.)
- **🕒 신선도 주의:** 2026년 2월 측정으로 매우 신선. 다만 **프리프린트 + 단독 저자 + 하드웨어 교란**이라는 3중 단서를 항상 병기. Phase 4 fact-checker는 이 항목의 모든 수치를 arXiv 원문과 대조할 것.

---

## 2. 격리 강화 (Firecracker / gVisor / Kata)

### 논문 4 — Firecracker: Lightweight Virtualization for Serverless Applications

- **저자/연도/발표처:** Alexandru Agache, Marc Brooker, **Andreea Florescu**, Alexandra Iordache, Anthony Liguori, Rolf Neugebauer, Phil Piwonka, Diana-Maria Popa (전원 Amazon Web Services) / 2020 / **17th USENIX Symposium on Networked Systems Design and Implementation (NSDI '20), February 25–27, 2020, Santa Clara, CA, pp. 419–434.** ISBN 978-1-939133-13-7
- **URL:** https://www.usenix.org/conference/nsdi20/presentation/agache (PDF: https://www.usenix.org/system/files/nsdi20-paper-agache.pdf)
- **재현 자료:** https://github.com/firecracker-microvm/nsdi2020-data (논문 §5 각주 7 — 설정·스크립트·원자료 공개)
- **📌 인용 시 주의 (직접 확인한 불일치):** USENIX 공식 페이지의 `citation_author` 메타태그에는 **저자가 7명만** 들어 있고 **Andreea Florescu가 빠져 있다.** PDF 표지의 실제 저자는 **8명**이다. 위 목록은 PDF 표지 기준이다. 자동 인용 생성기를 쓰면 저자가 하나 누락된다.
- **핵심 발견:**
  - Firecracker는 QEMU를 통째로 대체한, Rust로 쓴 최소 VMM. 게스트 커널 최소 구성에서 **컨테이너당 메모리 오버헤드 5MB 미만, 애플리케이션 코드까지 부팅 125ms 미만, 호스트당 초당 최대 150개 MicroVM 생성.** (§1)
  - 2018년 12월 Apache 2 오픈소스 공개. AWS Lambda에서 2018년부터 프로덕션 사용.
  - **I/O가 여전히 대가를 치른다(§5.3):** "4kB reads are only 49µs slower than native reads. Large blocks have significantly more overhead, with Firecracker more than doubling the IO latency." 그리고 "The hardware is capable of over **340,000 read IOPS (1GB/s at 4kB)**, but the Firecracker (and Cloud Hypervisor) guest is limited to around **13,000 IOPS (52MB/s at 4kB)**."
  - **네트워크 처리량(Table 1, Gb/s, iperf3, 1500 MTU, tap 인터페이스):** loopback(호스트) 44.14 (1 RX) / 46.92 (10 RX), **Firecracker 15.61 (1 RX) / 15.13 (10 RX)**, Cloud Hypervisor 23.12, QEMU 23.76.
  - 부팅 시간 측정 정의: "the time between when VMM process is forked and the guest kernel forks its init process."
- **측정 조건 (⚠️ 필수 병기):** **EC2 m5d.metal**, Intel Xeon Platinum 8175M ×2 (총 48코어, **하이퍼스레딩 비활성**), **384GB RAM**, 로컬 NVMe SSD 840GB ×4. 호스트 OS **Ubuntu 18.04.2, 커널 4.15.0-1044-aws**. 게스트 커널 **Linux 4.14.94** 직접 로드, 최소 드라이버·모듈 없음. 부팅 실험은 vCPU 1개 / 메모리 256MB, 500회 직렬 측정. I/O 실험은 vCPU 2개 / 메모리 512MB, fio + libaio + direct IO, 큐 깊이 32(처리량) / 1(레이턴시). **측정 연도 2019~2020.**
- **인용할 만한 문장:**
  > "The traditional view is that there is a choice between virtualization with strong security and high overhead, and container technologies with weaker security and minimal overhead. This tradeoff is unacceptable to public infrastructure providers, who need both strong security and minimal overhead." (Abstract)

  > "With the provided minimal Linux guest kernel configuration, it offers memory overhead of less than 5MB per container, boots to application code in less than 125ms, and allows creation of up to 150 MicroVMs per second per host." (§1, p.419)
- **이 책에서의 쓸모:**
  - "컨테이너 격리는 어디까지인가" 논의의 **업계 최고 권위 답변**. "AWS Lambda는 고객 간 격리를 컨테이너가 아니라 microVM으로 한다"는 사실 자체가 컨테이너 격리의 한계를 웅변한다.
  - Abstract의 첫 인용문은 **격리 강도 vs 오버헤드 트레이드오프 챕터의 정의 문장**으로 그대로 쓸 수 있다.
  - **맥 사용자에게 직접 유용:** VMM을 통과하는 I/O·네트워크가 얼마나 비싼지 보여주는 1차 근거 — 340,000 IOPS 하드웨어가 게스트에서 13,000 IOPS로, 44Gb/s 루프백이 15Gb/s로. Docker Desktop의 bind mount와 포트 포워딩이 왜 답답한지에 대한 **구조적 설명**(같은 원인, 다른 VMM).
  - "Lambda는 왜 콜드 스타트가 있나"에 대한 근거(125ms 부팅 + 풀 관리, §4.2 Little's law 서술).
- **🕒 신선도 주의:** **2019~2020년 측정, Firecracker 초기 버전 기준.** 논문 스스로 "We expect to fix both of these limitations in time"라고 적었으므로 **13,000 IOPS·15Gb/s는 현재 성능이 아니다.** "2020년 논문 발표 시점 기준" 반드시 병기. 5MB/125ms/150개는 설계 목표치로 널리 인용되지만 이 역시 2020년 값.

> **gVisor / Kata 성능은 논문 2(van Rijn & Rellermeyer 2021)에 정량 데이터가 있다.** gVisor·Kata 단독 논문은 이번 세션에서 1차 소스로 확보하지 못했다(「미확인 목록」 참조).

---

## 3. 보안 취약점 분류·실증

### 논문 5 — A Measurement Study on Linux Container Security: Attacks and Countermeasures

- **저자/연도/발표처:** Xin Lin, Lingguang Lei, Yuewu Wang, Jiwu Jing (Institute of Information Engineering, CAS / University of Chinese Academy of Sciences), Kun Sun (George Mason University), Quan Zhou / 2018 / **ACSAC '18 — 2018 Annual Computer Security Applications Conference, December 3–7, 2018, San Juan, PR, USA, pp. 418–429**
- **DOI:** 10.1145/3274694.3274720 (DBLP 조회로 저자·페이지·DOI 교차 확인, 2026-07-25)
- **오픈 PDF:** https://csis.gmu.edu/ksun/publications/container-acsac18.pdf (직접 내려받아 확인)
- **핵심 발견:**
  - 컨테이너 플랫폼에서 실제 동작하는 **익스플로잇 223건** 데이터셋을 수집해 2차원 분류 체계로 정리, 그중 **대표 88건**으로 격리 강도 측정.
  - **88건 중 50건(56.82%)이 Docker 기본 설정 컨테이너 안에서 공격에 성공.**
  - **11건은 컨테이너 격리를 실제로 뚫고 권한 상승(privilege escalation)에 성공**했고, 이 11건 모두 **공통된 4단계 공격 모델**을 따랐다.
  - **가장 중요한 구조적 결론:** 권한 상승을 막는 데는 **Capability·Seccomp·MAC(AppArmor/SELinux)** 같은 커널 보안 기제가 **Namespace·Cgroup 같은 컨테이너 격리 기제보다 더 큰 역할**을 한다. 또한 이 기제들 사이의 상호의존·상호영향 때문에 **"short board effect"**(최약 링크가 전체 방어력을 결정)에 빠질 수 있다.
- **측정 조건 (⚠️ 필수 병기):** **Docker 17.09.1-ce** (Seccomp 등 커널 보안 기제 지원 버전). 익스플로잇마다 취약 커널이 필요해 배포판을 바꿔가며 실험(예: Ubuntu 14.04 / 15.10). 일부 실험은 VMware VM에 **Ubuntu 16.04 LTS AMD64, Linux 커널 4.8.0#1**, 쿼드코어 2.80GHz, 8GB. **측정 연도 2018.**
- **인용할 만한 문장:**
  > "We find 50 (56.82%) exploits can successfully launch attacks from inside the container with the default configuration." (Abstract)

  > "We find the kernel security mechanisms such as Capability, Seccomp, and MAC play a more important role in preventing privilege escalation than the container isolation mechanisms (i.e., Namespace and Cgroup)." (Abstract)
- **이 책에서의 쓸모:**
  - **"네임스페이스와 cgroups는 보안 경계가 아니다"라는 이 책의 핵심 주장에 학술 근거를 준다.** 두 번째 인용문이 그 결정적 문장이다.
  - `--cap-drop`, seccomp 프로파일, non-root 사용자, `--privileged` 금지 같은 실무 권고가 왜 "선택 사항"이 아닌지 설명하는 데 쓴다.
  - 컨테이너 탈출이 이론적 우려가 아니라 **측정된 사실**임을 보여주는 근거(88건 중 11건).
- **🕒 신선도 주의:** **2018년 측정, Docker 17.09 / 커널 4.8~4.x 기준.** 구체 익스플로잇 목록과 성공률(56.82%)은 **2018년 시점의 취약 커널 조합에 대한 값**이며 오늘날 최신 패치 커널 성공률이 아니다. **개별 수치보다 구조적 결론(어느 기제가 방어에 기여하는가)을 인용할 것.** 수치를 쓸 땐 "2018년 측정, 당시 알려진 익스플로잇 88건 대상" 필수 병기.

---

### 논문 6 (최신 공격면) — Cross Container Attacks: The Bewildered eBPF on Clouds

- **저자/연도/발표처:** Yi He, Roland Guo, Xijia Che (Tsinghua University and BNRist), Yunlong Xing, Kun Sun (George Mason University), Zhuotao Liu, Ke Xu, Qi Li (Tsinghua University and Zhongguancun Laboratory) / 2023 / **32nd USENIX Security Symposium (USENIX Security '23), pp. 5971–5988.** ISBN 978-1-939133-37-3
- **URL:** https://www.usenix.org/conference/usenixsecurity23/presentation/he (USENIX 공식 페이지 메타데이터 직접 확인)
- **핵심 발견 (Abstract 기준 — 본문 PDF는 미확보, abstract 한정):**
  - eBPF는 컨테이너 보안·네트워크 관리·관측성 강화에 널리 쓰이지만, **공격용 eBPF는 컨테이너에 새로운 공격면을 만든다.** eBPF 트레이싱 기능으로 컨테이너 격리를 깨고 호스트를 공격(민감 데이터 탈취, DoS, 컨테이너 탈출)할 수 있다.
  - 실제 서비스 침해 실증: **온라인 Jupyter/인터랙티브 셸 서비스 5곳과 Google Cloud Platform의 Cloud Shell을 실제로 침해.**
  - **주요 클라우드 벤더 3사의 Kubernetes 서비스**에서 eBPF로 컨테이너 탈출 후 **노드 간(cross-node) 공격**이 가능함을 확인. 알리바바 Kubernetes 서비스에서는 과다 권한 메트릭/관리 Pod를 악용해 **클러스터 전체 장악**이 가능.
  - "the existing eBPF permission model cannot confine the eBPF and ensure secure usage in shared-kernel container environments."
- **측정 조건:** ⚠️ **미확인** — 본문 PDF를 이번 세션에서 열지 못해 커널 버전·컨테이너 런타임 버전·실험 일자를 확보하지 못했다. Abstract 수준 정보만 기록. **수치성 주장은 인용하지 말 것.**
- **인용할 만한 문장:**
  > "With eBPF tracing features, attackers can break the container's isolation and attack the host, e.g., steal sensitive data, DoS, and even escape the container." (Abstract)
- **이 책에서의 쓸모:**
  - "컨테이너는 커널을 공유한다 → 커널에 새 기능이 생기면 공격면도 함께 늘어난다"라는 **구조적 교훈**의 최근 사례. eBPF는 2020년대 관측성의 총아인데 그게 그대로 공격 벡터가 됐다는 서사가 강하다.
  - 논문 5(2018)와 짝지어 "이건 옛날 얘기가 아니다"를 보이는 데 유용.
  - 다만 **이 책 독자(맥 로컬 개발)의 직접 위협 모델은 아니다.** 프로덕션 배포를 다루는 절에서만 짧게.
- **🕒 신선도 주의:** 2023년 발표. eBPF 권한 모델은 이후 커널에서 계속 변경 중(`CAP_BPF` 분리 등). "2023년 시점" 병기.

---

### 논문 9 (이미지 생태계 실태 조사) — Understanding the Security Risks of Docker Hub

- **저자/연도/발표처:** Peiyu Liu, Shouling Ji, Lirong Fu, Xuhong Zhang, Tao Lu, Wenzhi Chen (Zhejiang University), Kangjie Lu (University of Minnesota Twin Cities), Wei-Han Lee (IBM Research), Raheem Beyah (Georgia Institute of Technology) / 2020 / **ESORICS 2020 — 25th European Symposium on Research in Computer Security, LNCS 12308, pp. 257–276, Springer**
- **DOI:** 10.1007/978-3-030-58951-6_13 (DBLP 교차 확인 + PDF 본문 저작권 라인에서 재확인)
- **오픈 PDF:** https://nesa.zju.edu.cn/download/Understanding%20the%20Security%20Risks%20of%20Docker%20Hub.pdf (직접 내려받아 확인)
- **공개 데이터셋:** 저자들이 재현성을 위해 데이터셋을 공개했다고 논문에 명시 (§1 기여 목록, 참조 [13])
- **핵심 발견:**
  - **데이터셋 규모 (Table 1):** 공식 저장소 147개(이미지 1,384개, 개발자 1) + 커뮤니티 저장소 975,711개(이미지 2,225,860개, 개발자 349,860명) = **총 975,858개 저장소 / 2,227,244개 이미지 / 349,861명 개발자.** Docker Hub API 기반 자체 크롤러로 수집.
  - **런 커맨드의 민감 파라미터:** "we observe that each recommended run-command in the repository description contains **one sensitive parameter on average**." 예시로 든 민감 파라미터가 `--privileged`이며, "when users run an image with the parameter of `--privileged`, the container will get the root access to the host."
  - **사용자 인식 조사:** "our user study reveals that users are not aware of the threats from sensitive parameters—they will directly execute run-commands specified by developers without checking and understanding them."
  - **악성 이미지:** 20,000개 이상 이미지 스캔에서 **악성 이미지 42개** 발견(원격 코드 실행, 악성 크립토마이닝). 세부: 693,757개 실행 프로그램 → 중복 제거 36,584개 고유 프로그램 → **악성 프로그램 13개가 이미지 17개에 존재.** **공식 저장소 147개의 최신 이미지에서는 악성 실행 프로그램이 발견되지 않았다.**
  - **취약점 심각도 (CVSSv3 기준):** 공식 이미지는 "only 6% of vulnerabilities are highly/critically severe, they exist in **almost 30% of the latest official images**." 인기 상위 10,000개 커뮤니티 저장소에서는 medium 비율 **37% 초과**, high 비율 **8% 초과**로 상승하고, **"more than 64% of community images are affected by highly/critically severe vulnerabilities."**
  - **패치 지연:** "Vulnerability patching of software in Docker images is significantly delayed by **422 days on average**." 원인으로 "the programs are decoupled from the mainstream ones, and developers are less incentivized to update programs in Docker images."
- **측정 조건 (⚠️ 필수 병기):** Docker Hub 공개 정보 전수 크롤링. 취약점 스캔에 **Anchore**, 악성 판정 보조에 **VirusTotal intelligence API** 사용. 악성 프로그램 분석 대상은 공식 147 저장소 최신 이미지 + 인기 상위 10,000 커뮤니티 저장소 최신 이미지 + 나머지를 인기순 100그룹으로 나눠 그룹당 100개 랜덤 추출(총 커뮤니티 10,000개). **수집 정확 일자는 논문에서 확인하지 못했다** — 참고문헌 접속일이 "August 2019"로 표기된 것으로 보아 2019년경으로 보이나 이는 추정이다. 발표 2020.
- **인용할 만한 문장:**
  > "We uncover 42 malicious images that can cause attacks such as remote code execution and malicious cryptomining." (Abstract)

  > "Vulnerability patching of software in Docker images is significantly delayed by 422 days on average." (§1)

  > "it is quite alarming that more than 64% of community images are affected by highly/critically severe vulnerabilities such as the denial of service and memory overflow." (§5)
- **이 책에서의 쓸모:**
  - **이미지 챕터의 "왜 베이스 이미지를 함부로 고르면 안 되는가"에 대한 유일한 대규모 실증 근거.** 자바 개발자가 `FROM openjdk:...` 한 줄을 아무 생각 없이 쓰는 관행을 흔드는 데 쓴다.
  - **422일 패치 지연**은 "이미지를 정기적으로 재빌드해야 하는 이유"의 결정적 수치. "빌드해 놓고 6개월 방치한 이미지"에 대한 실무 경고와 직결.
  - **README의 `docker run` 명령을 복붙하지 말라**는 권고에 근거를 준다 — 권장 런 커맨드당 민감 파라미터가 평균 1개, 그리고 사용자들은 확인하지 않는다는 사용자 조사까지 있다. `--privileged` 챕터의 오프닝 소재로 강력하다.
  - 공식 이미지 vs 커뮤니티 이미지 선택 기준의 정량적 근거(공식에서는 악성 0건, 커뮤니티 64%가 고위험 취약점 보유).
- **🕒 신선도 주의:** **2019년경 수집, 2020년 발표.** 그 이후 Docker Hub는 Docker Scout·자동 취약점 스캔·Docker Official Images 정책·Verified Publisher 프로그램 등을 도입했고 이미지 총량도 크게 늘었다. **42건·422일·64% 같은 수치를 현재형으로 쓰면 안 된다.** "2020년 ESORICS 발표 당시 약 220만 개 이미지 조사 기준"을 반드시 병기하고, 오늘날 재측정값은 확보하지 못했음을 밝힐 것.

---

## 4. 커널 격리 기본기 (네임스페이스·cgroups·seccomp·capabilities)

> **정직한 상태 보고:** "리눅스 네임스페이스·cgroups 그 자체"를 정면으로 다루는 **독립 학술 논문은 이번 세션에서 1차 소스로 확보하지 못했다.** 이 영역의 정전(canonical) 문헌은 커널 문서(`Documentation/admin-guide/cgroup-v2.rst`, `man 7 namespaces`)와 LWN 기사 등 **비학술 1차 소스**다 — 이는 web-researcher의 영역이다. 대신 아래 두 개의 **논문 내 정량·구조 서술**이 이 영역을 충분히 뒷받침한다.

- **정량 근거 (논문 3, Khan 2026, §4.2.1):** **네임스페이스 생성 비용은 7.94 ms(SSD) / 8.45 ms(HDD)로 전체 컨테이너 기동 시간의 1.5% 미만이며, I/O 바운드가 아니라 CPU 바운드인 "플랫폼 불변 원시요소(platform-invariant primitive)"다.**
  → "컨테이너 기동이 느린 건 네임스페이스 탓이 아니다"를 못 박는 데 최적. 기동 시간 분해 모델도 논문에 명시: `T_startup = T_kernel + T_runtime + T_storage(tier)`, `T_kernel ≈ 8 ms (invariant, σ < 3 ms)`.

- **보안 근거 (논문 5, Lin et al. 2018):** **권한 상승 방어에서 Namespace·Cgroup보다 Capability·Seccomp·MAC의 기여가 크다**, 그리고 이 기제들은 상호의존 때문에 **"short board effect"**에 빠질 수 있다.
  → 격리(isolation) ≠ 보안(security)이라는 구분을 세우는 데 최적.

- **아키텍처 서술 (논문 2, van Rijn & Rellermeyer 2021, §2):** 컨테이너(namespace + cgroups) / secure container(gVisor: Sentry가 시스템콜 재구현 + seccomp로 I/O 시스템콜 차단 후 Gofer에 9P로 위임, Kata: namespace 설정 + 하이퍼바이저 기동) / 하이퍼바이저 / 유니커널을 한 축 위에 놓고 비교하는 **구조도와 서술**을 제공한다. 그림 1~4가 챕터 삽화의 개념적 원본으로 쓸 만하다(직접 재작도 필요).

---

## 5. 오케스트레이션·스케줄링

> **커버리지 자기평가: 부족.** 이 책의 초점(맥 로컬 개발)에서 멀어 의도적으로 1편만 확보했다.

### 논문 7 — Large-scale cluster management at Google with Borg

- **저자/연도/발표처:** Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune, John Wilkes (Google Inc.) / 2015 / **EuroSys '15 — Proceedings of the Tenth European Conference on Computer Systems, April 21–24, 2015, Bordeaux, France, Article 18, pp. 18:1–18:17.** ACM 978-1-4503-3238-5/15/04
- **DOI:** 10.1145/2741948.2741964 (DBLP 조회로 저자·페이지·DOI 교차 확인, 2026-07-25)
- **PDF:** https://research.google.com/pubs/archive/43438.pdf (직접 내려받아 확인)
- **핵심 발견:**
  - Borg는 수십만 개 잡을, 각각 최대 수만 대 머신인 여러 클러스터에서 돌리는 클러스터 매니저. "It achieves high utilization by combining admission control, efficient task-packing, over-commitment, and machine sharing with process-level performance isolation." (Abstract)
  - **셀 규모:** "Our median cell size is about 10 k machines after excluding test cells; some are much larger." (§2.2)
  - **작업 기동 지연 (§3.4) — 이 책에 직접 쓸 대목:** "Task startup latency (the time from job submission to a task running) is an area that has received and continues to receive significant attention. It is highly variable, with the **median typically about 25 s. Package installation takes about 80% of the total**: one of the known bottlenecks is contention for the local disk where packages are written to."
  - 확장성: 단일 Borgmaster가 수천 대 머신 관리, 여러 셀이 **분당 10,000 태스크 이상**의 도착률, 바쁜 Borgmaster는 **10~14 CPU 코어, 최대 50 GiB RAM** 사용.
- **측정 조건:** Google 프로덕션 Borg 셀 운영 데이터 기반(합성 벤치마크 아님). **관측 연도 ~2014~2015.**
- **이 책에서의 쓸모:**
  - Kubernetes의 지적 계보를 한 문장으로 설명할 때의 1차 근거(Borg → Omega → Kubernetes).
  - **"이미지/패키지 배포가 기동 시간의 80%"라는 수치가 이 책의 이미지 최적화 챕터와 곧장 연결된다.** 그리고 이 문장은 논문 8(Slacker)이 자기 연구의 출발점으로 직접 인용한 문장이다 — **Borg(2015) → Slacker(2016) → 오늘날 레이지 풀링**이라는 서사 한 줄이 만들어진다.
- **🕒 신선도 주의:** **2015년 논문, ~2014년 Google 내부 운영 데이터.** Borg는 Kubernetes가 아니다 — 이 책에서 Borg 수치를 Kubernetes 수치처럼 쓰면 안 된다. 25초/80%는 **2015년 Google Borg 기준**임을 반드시 병기.

---

## 6. 이미지·레지스트리 실측

> **이미지 생태계의 보안 실태(취약점·악성 이미지·패치 지연)는 논문 9(Liu et al., ESORICS 2020)에 있다.** 편의상 §3(보안)에 배치했으나 이미지 챕터에서 함께 쓸 것.

### 논문 8 — Slacker: Fast Distribution with Lazy Docker Containers

- **저자/연도/발표처:** Tyler Harter (University of Wisconsin—Madison), Brandon Salmon, Rose Liu (Tintri), Andrea C. Arpaci-Dusseau, Remzi H. Arpaci-Dusseau (University of Wisconsin—Madison) / 2016 / **14th USENIX Conference on File and Storage Technologies (FAST '16), February 22–25, 2016, Santa Clara, CA.** ISBN 978-1-931971-28-7
- **URL:** https://www.usenix.org/conference/fast16/technical-sessions/presentation/harter (PDF: https://www.usenix.org/system/files/conference/fast16/fast16-papers-harter.pdf)
- **핵심 발견:**
  - **HelloBench**라는 벤치마크를 만들어 **57개 컨테이너화된 애플리케이션**의 기동 시간을 측정.
  - **"pulling packages accounts for 76% of container start time, but only 6.4% of that data is read."** ← 이 책에서 가장 인용 가치 높은 수치.
  - 이 관찰에서 출발해 레이지 페칭 기반 Docker 스토리지 드라이버 Slacker를 설계, **컨테이너 개발 사이클 중앙값 20배, 배포 사이클 5배 단축.**
  - Docker Hub 라이브러리 이미지 pull 수를 2015-01-15에 집계했을 때, HelloBench가 다루는 이미지들이 **전체 pull의 86%**를 차지 — 벤치마크의 대표성 근거.
- **측정 조건 (⚠️ 필수 병기):** HelloBench 57개 이미지(Docker Hub 라이브러리 이미지 기반). 이미지별로 압축 크기·비압축 크기·실행 시 실제 읽힌 바이트를 측정하며, 읽기는 **blktrace로 추적한 블록 디바이스** 위에서 워크로드를 돌려 계측. Docker Hub pull 수 집계 시점 **2015-01-15**(HelloBench 이미지 최초 수집 7개월 후, 라이브러리는 72→94개로 증가). **측정 연도 2015~2016.**
- **인용할 만한 문장:**
  > "Our analysis shows that pulling packages accounts for 76% of container start time, but only 6.4% of that data is read." (Abstract)

  > "Slacker speeds up the median container development cycle by 20× and deployment cycle by 5×." (Abstract / §1)
- **이 책에서의 쓸모:**
  - **이미지 최적화 챕터의 개념적 심장.** "여러분이 내려받은 이미지의 대부분은 한 번도 읽히지 않는다(6.4%만 읽힘)" — 멀티스테이지 빌드, 슬림 베이스 이미지, 레이어 캐시 전략이 왜 효과가 있는지를 설명하는 근본 근거.
  - 오늘날의 **레이지 풀링(eStargz, SOCI, Nydus)** 계보의 출발점 논문으로 소개 가능.
  - 논문 3(Khan 2026)과 **짝지으면 뉘앙스가 정확해진다:** warm-start(이미 pull된 상태)에서는 이미지 크기가 2.5%밖에 영향을 안 주지만, **pull이 포함된 cold path에서는 이미지가 기동 시간의 76%**다. → "이미지 다이어트가 언제 효과 있고 언제 없는가"를 정확히 구분해 쓸 수 있다. **이 대비가 이 책에서 논문 리서치가 만들어내는 가장 큰 가치다.**
- **🕒 신선도 주의:** **2015~2016년 측정.** 당시 Docker 스토리지 드라이버는 AUFS/devicemapper 시대이고, 레지스트리 프로토콜·압축(gzip → zstd), 병렬 pull, 레이어 캐시 모두 이후 개선됐다. **76%/6.4%는 "2016년 FAST 논문 측정 기준"으로만 인용.** 오늘날 정확한 재측정값은 확보하지 못했다(「미확인 목록」).

---

## 인용 가능한 문장 후보 (본문에 그대로 쓸 만한 것)

1. > "When both are tuned for performance, Docker equals or exceeds KVM performance in every case we tested."
   — Felter et al., ISPASS 2015, p.172. **(2014년 측정 병기 필수)**

2. > "We also question the practice of deploying containers inside VMs, since this imposes the performance overheads of VMs while giving no benefit compared to deploying containers directly on non-virtualized Linux."
   — Felter et al., ISPASS 2015, p.172. **← Apple Silicon 맥 = 정확히 이 구조. 챕터 오프닝 훅으로 최강.**

3. > "The traditional view is that there is a choice between virtualization with strong security and high overhead, and container technologies with weaker security and minimal overhead. This tradeoff is unacceptable to public infrastructure providers, who need both strong security and minimal overhead."
   — Agache et al., NSDI '20, Abstract. **← 격리 트레이드오프 챕터의 정의 문장.**

4. > "We find the kernel security mechanisms such as Capability, Seccomp, and MAC play a more important role in preventing privilege escalation than the container isolation mechanisms (i.e., Namespace and Cgroup)."
   — Lin et al., ACSAC '18, Abstract. **← "네임스페이스는 보안 경계가 아니다"의 학술 근거.**

5. > "Our analysis shows that pulling packages accounts for 76% of container start time, but only 6.4% of that data is read."
   — Harter et al., FAST '16, Abstract. **(2016년 측정 병기 필수)**

6. > "Task startup latency ... is highly variable, with the median typically about 25 s. Package installation takes about 80% of the total."
   — Verma et al., EuroSys '15, §3.4. **(2015년 Google Borg 기준 병기 필수)**

7. > "Docker is very fast to boot, taking around 100 ms, followed by gVisor at around 190 ms. Much later, at 600 ms and 800 ms, we see the Kata container and LXC platforms, respectively."
   — van Rijn & Rellermeyer, Middleware '21, §3.5. **(2021년 측정, 리눅스 네이티브 기준 병기 필수)**

8. > "Vulnerability patching of software in Docker images is significantly delayed by 422 days on average."
   — Liu et al., ESORICS 2020, §1. **(2019년경 수집 병기 필수) ← "이미지는 만들어 놓고 끝이 아니다"의 결정타.**

9. > "it is quite alarming that more than 64% of community images are affected by highly/critically severe vulnerabilities such as the denial of service and memory overflow."
   — Liu et al., ESORICS 2020, §5. **(2019년경 수집, 인기 상위 10,000개 커뮤니티 저장소 기준 병기 필수)**

10. > "Namespace creation requires 7.94 ms (SSD, σ = 2.05) and 8.45 ms (HDD, σ = 2.57), contributing < 1.5% of total startup."
    — Khan, arXiv:2602.15214, §4.2.1. **(⚠️ arXiv 프리프린트 명시 필수) ← "컨테이너 기동이 느린 건 네임스페이스 탓이 아니다"의 근거.**

---

## 미확인 목록 (찾으려 했으나 확보하지 못한 영역)

| 영역 | 상태 | 비고 |
|---|---|---|
| **Apple Silicon 컨테이너 성능 학술 연구** | ⚠️ 거의 없음 — **검증된 부재** | arXiv API 전수 검색(2026-07-25 실행): `abs:"Docker Desktop"` → **전체 아카이브에 단 2편**(그중 컨테이너 성능은 논문 3 하나). `abs:"Apple Silicon" AND abs:container` → **3편**이며 전부 컨테이너 성능 연구가 아님(블록체인 PoW 실증, ARM64 엣지 AI 텐서 가상화, 멀웨어 샌드박스). 확보한 유일한 직접 측정이 **논문 3(Khan 2026)이며 arXiv 프리프린트·단독 저자**다. → **이 공백 자체가 책의 논거다:** "여러분의 환경은 학계가 측정해 주지 않았다. 그러니 직접 재보는 법을 배워야 한다." |
| (참고) Apple Silicon 아키텍처 불일치 문제를 언급한 인접 논문 | ✅ 서지 확인 | Alejandro Avina, Yashas Hariprasad, Naveen Kumar Chaudhary, "pokiSEC: A Multi-Architecture, Containerized Ephemeral Malware Detonation Sandbox", **arXiv:2512.20860 (2025-12-24 제출, 12쪽)**. Abstract에서 "the adoption of ARM64 developer hardware (e.g., Apple Silicon), where common open-source sandbox recipes and pre-built environments frequently assume x86_64 hosts and do not translate cleanly across architectures"라고 문제를 진술한다. **성능 수치는 없다** — "x86 가정이 깨진다"는 문제 인식의 인용 근거로만 사용 가능. |
| **Rosetta 2 / x86 이미지 에뮬레이션 오버헤드** | ❌ 미확인 | Apple Rosetta를 통한 amd64 컨테이너 실행 오버헤드에 대한 학술 측정을 확보하지 못했다. 엔지니어링 문헌(web/community researcher) 영역. |
| **virtiofs / gRPC-FUSE bind mount 성능 정량 비교 (맥 한정)** | ❌ 미확인 | 논문 2가 9P vs virtio-fs 일반론을 제공하지만 **Docker Desktop for Mac 구체 측정은 확보 실패.** |
| **gVisor 단독 논문** | ❌ 미확보 | gVisor 성능은 논문 2의 3자 측정으로 대체. 구글 자체 발표 논문의 1차 소스는 이번 세션에서 열지 못했다. |
| **Kata Containers 단독 논문** | ❌ 미확보 | 동일. 논문 2의 측정으로 대체. |
| **Docker Hub 이미지 취약점 대규모 스캔 — 최신 재측정** | ⚠️ 부분 | 2020년 조사(논문 9)는 확보. **2021년 이후 대규모 재측정은 확보하지 못했다.** Docker Scout·자동 스캔 도입 이후의 수치는 없음. |
| **논문 9의 데이터 수집 정확 일자** | ⚠️ 미확인 | PDF 본문에서 수집 시작·종료 일자를 찾지 못했다. 참고문헌 접속일 "August 2019"로 미루어 2019년경으로 보이나 **추정이며 단정하지 말 것.** |
| **Cross Container Attacks 본문 수치** | ⚠️ Abstract만 | 논문 6은 USENIX 공식 페이지의 메타데이터·Abstract만 확보. 본문 실험 조건(커널 버전 등) 미확인. |
| **JVM 컨테이너 자원 인식 (`UseContainerSupport` 등)** | ❌ 미확인 (예상대로) | 태스크에서 예고한 대로 학술보다 엔지니어링 문헌 영역. 학술 논문 탐색을 조기 중단했다. web-researcher가 OpenJDK JEP·이슈로 커버할 영역. |
| **컨테이너 이미지 레이어 중복률 최신 재측정** | ❌ 미확인 | Slacker(2016) 이후의 대규모 재측정 연구를 확보하지 못했다. |
| **컨테이너 vs VM 오버헤드 2020년대 x86 재측정** | ✅ 부분 확보 | 논문 2(2021)가 그 역할. 2023년 이후 재측정은 미확인. |

### 도구 실패 기록
- **Semantic Scholar Graph API**: HTTP 429 (Too Many Requests) 2회 연속 발생 → **DBLP API로 대체**하여 서지 교차 검증 수행(논문 5, 7, Liu et al.).
- **ACM Digital Library (dl.acm.org)**: 봇 차단으로 메타데이터 추출 실패 → 저자 기관 오픈 PDF(GMU) 및 DBLP로 우회.
- **USENIX 페이지 WebFetch**: HTTP 403 → curl(User-Agent 지정)로 우회 성공.

---

## 커버리지 자기평가

| 영역 | 평가 | 빠진 것 |
|---|---|---|
| 1. 컨테이너 vs VM 성능 오버헤드 | **충분** | 2023년 이후 x86 재측정 없음. 고전(2015)·최근(2021)·맥(2026 프리프린트) 3점 확보로 충분. |
| 2. 격리 강화 (gVisor/Kata/Firecracker) | **보통** | Firecracker는 1차 소스 확보. gVisor·Kata는 **3자 측정(논문 2)에만 의존** — 단독 논문 미확보. 실무서 수준에는 충분하나 "gVisor가 느리다"를 단정하려면 부족. |
| 3. 보안 취약점 분류·실증 | **충분** | 3층 확보 — 커널 격리 실증(논문 5, 2018), 이미지 생태계 실태(논문 9, 2020), 최신 공격면(논문 6, 2023). 모두 2018~2023년이라 **오늘날 수치로는 못 쓰지만 구조적 결론은 견고.** |
| 4. 커널 격리 기본기 | **보통** | 독립 학술 논문 없음. **논문 3의 8ms 네임스페이스 수치 + 논문 5의 방어 기여도 결론**으로 충분히 뒷받침되나, 원리 서술 자체는 커널 문서(web-researcher 영역)에 의존해야 함. |
| 5. 오케스트레이션·스케줄링 | **부족 (의도적)** | Borg 1편만. Omega·Kubernetes 논문 미확보. **이 책의 초점에서 멀어 확대하지 않기로 판단.** 필요하면 web-researcher가 커버. |
| 6. 이미지·레지스트리 실측 | **충분** | Slacker(2016, 성능) + Liu et al.(2020, 보안·규모 220만 이미지) 두 축 확보. **최신 레이지 풀링(eStargz/SOCI/Nydus) 학술 재측정과 2021년 이후 Docker Hub 재조사는 미확보.** |
| 7. JVM 컨테이너 자원 인식 | **미확인 (예상대로)** | 학술 영역 아님. 조기 중단. |
| **⭐ Apple Silicon 맥 환경** | **부족 — 그러나 그 자체가 발견** | 동료심사 논문 없음. 프리프린트 1편(논문 3)이 전부. **본문에서 이 공백을 정직하게 말하는 것이 억지 인용보다 낫다.** |

---

## 신선도 원장

> Phase 4 fact-checker 대조용. 이 표의 모든 행은 2026-07-25에 해당 1차 소스를 직접 열어 읽은 값이다.

| # | 주장 | 값 | 1차 소스 URL/DOI | 발행(측정) 연도 | 검색 시점 |
|---|------|-----|------------------|--------------|-----------|
| 1 | MySQL 고동시성에서 Docker의 네이티브 대비 손실 | 약 2%로 점근 | DOI 10.1109/ISPASS.2015.7095802, p.171 §II.A | 2015 (측정 2014) | 2026-07-25 |
| 2 | 동일 조건 KVM의 네이티브 대비 손실 | 측정 전 구간 40% 초과 | DOI 10.1109/ISPASS.2015.7095802, p.171 §II.A | 2015 (측정 2014) | 2026-07-25 |
| 3 | Felter 실험 환경 | Xeon E5-2665 ×2, 16코어, 256GB, Ubuntu 13.10, 커널 3.11.0, Docker 1.0, QEMU 1.5.0, MySQL 5.5.37 | DOI 10.1109/ISPASS.2015.7095802, p.171 §II | 2015 (측정 2014) | 2026-07-25 |
| 4 | 컨테이너 런타임 기동 시간 (리눅스 네이티브) | Docker ~100ms / gVisor ~190ms / Kata ~600ms / LXC ~800ms | arXiv:2110.11462 §3.5 | 2021 | 2026-07-25 |
| 5 | Docker 데몬 경유로 인한 추가 기동 지연 | 약 250 ms (OCI 런타임 직접 호출 대비) | arXiv:2110.11462 §3.5 | 2021 | 2026-07-25 |
| 6 | secure container(gVisor/Kata)의 I/O 처리량 | 최선의 경우에도 타 플랫폼의 절반 수준 | arXiv:2110.11462 §3.3 | 2021 | 2026-07-25 |
| 7 | gVisor 네트워크 90퍼센타일 응답시간 | 경쟁 플랫폼의 3~4배 | arXiv:2110.11462 Finding 12 | 2021 | 2026-07-25 |
| 8 | van Rijn 실험 환경 | AMD EPYC2 7542 dual-socket, 256GiB, NVMe, Ubuntu Server 20.04 LTS | arXiv:2110.11462 §3 | 2021 | 2026-07-25 |
| 9 | Firecracker 컨테이너당 메모리 오버헤드 | 5MB 미만 | NSDI '20 p.419 §1 | 2020 | 2026-07-25 |
| 10 | Firecracker 애플리케이션 코드까지 부팅 시간 | 125 ms 미만 | NSDI '20 p.419 §1 | 2020 | 2026-07-25 |
| 11 | Firecracker 호스트당 MicroVM 생성률 | 초당 최대 150개 | NSDI '20 p.419 §1 | 2020 | 2026-07-25 |
| 12 | Firecracker 4kB 읽기 레이턴시 페널티 | 네이티브 대비 +49 µs | NSDI '20 §5.3 p.429 | 2020 | 2026-07-25 |
| 13 | Firecracker 게스트 4kB 랜덤 읽기 IOPS 제한 | 하드웨어 340,000+ IOPS(1GB/s) → 게스트 약 13,000 IOPS(52MB/s) | NSDI '20 §5.3 p.429 | 2020 | 2026-07-25 |
| 14 | Firecracker 네트워크 처리량 (iperf3, tap, MTU 1500) | 호스트 loopback 44.14 Gb/s vs Firecracker 15.61 Gb/s (1 스트림) | NSDI '20 Table 1 p.429 | 2020 | 2026-07-25 |
| 15 | Firecracker 실험 환경 | EC2 m5d.metal, Xeon Platinum 8175M ×2, 48코어(HT off), 384GB, Ubuntu 18.04.2 커널 4.15.0-1044-aws, 게스트 커널 4.14.94 | NSDI '20 §5 | 2020 | 2026-07-25 |
| 16 | 기본 설정 컨테이너에서 성공한 익스플로잇 비율 | 88건 중 50건 = 56.82% | DOI 10.1145/3274694.3274720, Abstract | 2018 | 2026-07-25 |
| 17 | 컨테이너 격리를 뚫고 권한 상승에 성공한 익스플로잇 | 11건 (공통 4단계 공격 모델) | DOI 10.1145/3274694.3274720, Abstract | 2018 | 2026-07-25 |
| 18 | 수집된 컨테이너 유효 익스플로잇 데이터셋 규모 | 223건 (그중 대표 88건 실험) | DOI 10.1145/3274694.3274720, Abstract | 2018 | 2026-07-25 |
| 19 | Lin et al. 실험 환경 | Docker 17.09.1-ce, 취약 커널별 배포판 교체(Ubuntu 14.04/15.10 등), 일부 Ubuntu 16.04 커널 4.8.0#1 | ACSAC '18 §4.1 | 2018 | 2026-07-25 |
| 20 | Borg 작업 기동 지연 중앙값 | 약 25초, 그중 패키지 설치가 약 80% | DOI 10.1145/2741948.2741964 §3.4 | 2015 | 2026-07-25 |
| 21 | Borg 셀 규모 중앙값 | 약 10,000대 (테스트 셀 제외) | DOI 10.1145/2741948.2741964 §2.2 | 2015 | 2026-07-25 |
| 22 | Borgmaster 자원 사용 / 처리율 | 10–14 CPU 코어, 최대 50 GiB RAM / 일부 셀 분당 10,000 태스크 초과 | DOI 10.1145/2741948.2741964 §3.4 | 2015 | 2026-07-25 |
| 23 | 컨테이너 기동 시간 중 패키지 pull 비중 | 76% | FAST '16 Abstract | 2016 | 2026-07-25 |
| 24 | pull한 데이터 중 실제로 읽히는 비율 | 6.4% | FAST '16 Abstract | 2016 | 2026-07-25 |
| 25 | Slacker의 개선폭 | 개발 사이클 중앙값 20배, 배포 사이클 5배 | FAST '16 Abstract | 2016 | 2026-07-25 |
| 26 | HelloBench 규모·대표성 | 57개 애플리케이션 / Docker Hub 라이브러리 pull의 86% 커버(2015-01-15 집계) | FAST '16 Abstract, §3 | 2016 | 2026-07-25 |
| 27 | ⭐ 네임스페이스 생성 비용 | 7.94 ms (SSD, σ=2.05) / 8.45 ms (HDD, σ=2.57), 전체 기동의 1.5% 미만 | arXiv:2602.15214 §4.2.1 | 2026 (프리프린트) | 2026-07-25 |
| 28 | ⭐ warm-start 지연: Azure Premium SSD (alpine) | 568 ± 5 ms (σ=19), n=50 | arXiv:2602.15214 Table 3 | 2026 (프리프린트) | 2026-07-25 |
| 29 | ⭐ warm-start 지연: macOS Docker Desktop (alpine) | 1528 ± 139 ms (σ=502), n=50 | arXiv:2602.15214 Table 3 | 2026 (프리프린트) | 2026-07-25 |
| 30 | ⭐ Docker Desktop "가상화 세금" 배수 | alpine 2.69× / nginx 3.28× (⚠️ 하드웨어 차이 교란 포함 — 저자 본인 고지) | arXiv:2602.15214 Finding 3, §3.1 | 2026 (프리프린트) | 2026-07-25 |
| 31 | ⭐ 이미지 크기가 warm-start에 미치는 영향 (SSD) | 5MB~155MB 사이 편차 2.5% (554–568 ms) | arXiv:2602.15214 Finding 1 | 2026 (프리프린트) | 2026-07-25 |
| 32 | ⭐ 기동 시간 변동계수 (CV) | SSD 3.4% / HDD 8.3% / macOS 32.8% | arXiv:2602.15214 §4.1.2 | 2026 (프리프린트) | 2026-07-25 |
| 33 | ⭐ `--cpus=0.5` 실측 CPU 사용률 | SSD 60.52%(σ=3.79) / HDD 48.21%(σ=16.24) / macOS 71.63%(σ=36.14), macOS 이상치 최대 247% | arXiv:2602.15214 §4.2.2 | 2026 (프리프린트) | 2026-07-25 |
| 34 | ⭐ macOS 컨테이너 네트워크 RTT | bridge·host 양 모드 모두 약 34 ms. **⚠️ 논문은 "(17× slower)"라고만 쓰고 분모를 명시하지 않았다.** 같은 절의 "리눅스 bridge-host 차이 0.04–0.06 ms"는 **RTT가 아니라 두 모드 간 차이값**이므로 34 ms와 나눠서 배수를 재계산하지 말 것(34/0.04 = 850이지 17이 아니다). 두 수치는 종류가 다르다. | arXiv:2602.15214 §4.2.3 | 2026 (프리프린트) | 2026-07-25 |
| 35 | ⭐ OverlayFS vs 볼륨 순차 쓰기 (256MB, 중앙값 MB/s) | SSD 1.1 vs 194.0 (**0.006×**) / HDD 1.3 vs 136.6 (**0.010×**) / macOS 238.1 vs 224.5 (**1.06×**, p=0.21 유의하지 않음). **🚫 인용 가능한 것은 각 티어 내부의 비율뿐이다.** 티어 간 절대 MB/s 비교(예: "맥 238 vs 리눅스 1.1")는 하드웨어 교란(M1 Pro 로컬 NVMe vs Azure 2 vCPU 네트워크 스토리지) 때문에 **무효 — 본문에 등장하면 ❌**. | arXiv:2602.15214 Table 4 | 2026 (프리프린트) | 2026-07-25 |
| 36 | ⭐ 컨테이너 간 페이지 캐시 공유 효율 | 약 0% (동일 nginx 3개가 1개의 3배 메모리 소비) | arXiv:2602.15214 §4.3.3 | 2026 (프리프린트) | 2026-07-25 |
| 37 | ⭐ Khan 2026 실험 환경 | macOS: **Apple M1 Pro, 16GB, APFS/VM, Docker 28.4.0, overlayfs, Hypervisor.framework** / Azure: Standard_D2s_v3 2 vCPU Xeon, 8GB, Docker 28.x, overlay2 | arXiv:2602.15214 Table 2 | 2026 (프리프린트) | 2026-07-25 |
| 38 | eBPF로 실제 침해한 서비스 | 온라인 Jupyter/인터랙티브 셸 5곳 + GCP Cloud Shell; 주요 클라우드 3사 K8s에서 노드 간 공격 가능 | USENIX Sec '23 pp.5971–5988, Abstract | 2023 | 2026-07-25 |
| 39 | Docker Hub 조사 데이터셋 규모 | 저장소 975,858개 / 이미지 2,227,244개 / 개발자 349,861명 (공식 147저장소·1,384이미지 포함) | DOI 10.1007/978-3-030-58951-6_13, Table 1 | 2020 (수집 2019경) | 2026-07-25 |
| 40 | Docker Hub에서 발견된 악성 이미지 수 | 42개 (20,000+ 이미지 스캔 대상 중); 세부로 고유 실행 프로그램 36,584개 중 악성 13개가 이미지 17개에 존재 | DOI 10.1007/978-3-030-58951-6_13, Abstract·§5.2 | 2020 (수집 2019경) | 2026-07-25 |
| 41 | 공식 저장소(147개) 최신 이미지의 악성 실행 프로그램 | 0건 | DOI 10.1007/978-3-030-58951-6_13, §5.2 | 2020 (수집 2019경) | 2026-07-25 |
| 42 | Docker 이미지 소프트웨어 취약점 패치 지연 | 평균 422일 | DOI 10.1007/978-3-030-58951-6_13, §1 | 2020 (수집 2019경) | 2026-07-25 |
| 43 | 고위험/치명 취약점 보유 이미지 비율 | 공식 이미지 최신본의 약 30% (전체 취약점 중 고위험 비중은 6%) / 커뮤니티 이미지는 **64% 초과** | DOI 10.1007/978-3-030-58951-6_13, §5 | 2020 (수집 2019경) | 2026-07-25 |
| 44 | 커뮤니티 이미지 취약점 심각도 분포 (상위 10,000 저장소) | medium 37% 초과, high 8% 초과 (공식 이미지보다 높음) | DOI 10.1007/978-3-030-58951-6_13, §5 | 2020 (수집 2019경) | 2026-07-25 |
| 45 | 저장소 설명의 권장 run-command당 민감 파라미터 개수 | 평균 1개 (예: `--privileged` → 호스트 root 권한 획득) | DOI 10.1007/978-3-030-58951-6_13, §1·§2 | 2020 (수집 2019경) | 2026-07-25 |
| 46 | Liu et al. 분석 도구 | Anchore(취약점 스캔) + VirusTotal intelligence API(악성 판정) + 자체 크롤러/파서 | DOI 10.1007/978-3-030-58951-6_13, §3 | 2020 | 2026-07-25 |
| 47 | ⭐ arXiv 전수 검색: `abs:"Docker Desktop"` 매칭 논문 수 | 전체 아카이브에 2편 (컨테이너 성능 연구는 1편 = 논문 3) | arXiv API `export.arxiv.org/api/query` | — | 2026-07-25 |
| 48 | ⭐ arXiv 전수 검색: `abs:"Apple Silicon" AND abs:container` 매칭 논문 수 | 3편, 모두 컨테이너 성능 연구 아님 | arXiv API `export.arxiv.org/api/query` | — | 2026-07-25 |

---

## Phase 4 fact-checker를 위한 하드 규칙

1. **논문 3(arXiv:2602.15214)의 모든 수치는 "arXiv 프리프린트" 단서 없이 본문에 등장하면 ⚠️ 판정.**
2. **표의 "발행(측정) 연도"가 본문에 병기되지 않은 수치는 🕒 판정.** 특히 Felter(2014 측정)·Slacker(2016)·Lin(2018)·Borg(2015).
3. **Firecracker 저자 인용 시 8명(Andreea Florescu 포함) 확인.** USENIX 메타태그 기반 자동 생성 인용은 7명으로 나온다.
4. **gVisor·Kata 단독 논문에서 나온 것처럼 보이는 수치가 본문에 있으면 ❌** — 이번 리서치에서 본문을 확보하지 않았다. gVisor·Kata 관련 수치는 논문 2(van Rijn & Rellermeyer 2021)의 3자 측정으로만 뒷받침된다.
5. **리눅스 네이티브 측정값이 맥 환경 값처럼 서술되면 ❌.** 논문 1·2·4·5·7·8은 전부 x86_64 리눅스 기준이다.
6. **논문 3(Khan 2026)의 티어 간 절대값 비교는 ❌.** M1 Pro 랩톱(로컬 NVMe)과 Azure 2 vCPU VM(네트워크 스토리지)은 하드웨어가 달라 절대 수치를 나란히 놓을 수 없다. 특히 **"맥의 OverlayFS 쓰기가 리눅스보다 빠르다"류의 문장은 즉시 ❌** — 유효한 것은 각 티어 **내부**의 OverlayFS:볼륨 비율(0.006× / 0.010× / 1.06×) 대비뿐이다. 기동 시간의 2.69×·3.28×도 같은 교란을 포함하므로 "가상화만의 비용"으로 서술되면 ⚠️.
7. **논문 3의 "17× slower" 네트워크 배수를 다른 수치로 재계산해 쓰면 ❌.** 논문이 분모를 밝히지 않았다. 34 ms RTT는 그대로 인용 가능하되, 배수는 논문 표현을 인용하거나 생략할 것.
8. **본문 어디든 "리눅스 네이티브 기준" / "{연도} 측정 기준" 단서 없이 벤치마크 수치가 단독으로 등장하면 🕒.** 이 리서치의 모든 성능 수치는 예외 없이 조건부다.
