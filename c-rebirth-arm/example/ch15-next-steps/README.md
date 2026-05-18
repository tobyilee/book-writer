# ch15-next-steps — 다음 걸음 네 갈래

이 디렉토리에는 **빌드 타깃이 없다.** 15장은 작별의 짧은 인사이며, 다음 학습의 출발점을 손에 잡히도록 안내하는 자리다. 코드 대신 **권장 학습 경로**와 **참고 코드베이스**를 정리해두었다.

```sh
make            # 안내 메시지만 출력
```

## 다음 네 갈래 길

### 1. 인터럽트 — GIC + 예외 벡터 테이블

**왜 필요한가:** 우리 커널은 지금 `for (;;)`에 갇혀 있다. 외부에서 일이 벌어졌다는 사실, 시간이 흐른다는 사실을 CPU에게 가르치려면 인터럽트가 필요하다. 멀티태스킹의 출발점이다.

**어디서 시작하는가:**

- [s-matyukevich/raspberry-pi-os — Lesson 3](https://s-matyukevich.github.io/raspberry-pi-os/docs/lesson03/rpi-os.html): 인터럽트 처리의 모범 답안. 라즈베리 파이 4용 GIC 초기화와 타이머 인터럽트가 단계별로 풀려 있다.
- [bztsrc/raspi3-tutorial](https://github.com/bztsrc/raspi3-tutorial): 인터럽트 관련 짧은 단위(예: `09_framebuffer`, `10_virtualmemory`)가 함께 있어 칩챔 학습에 좋다.
- [ARM GIC v2 Architecture Specification](https://developer.arm.com/documentation/ihi0048/latest/): 공식 문서. 한 번은 훑어볼 가치가 있다.
- [Memfault Interrupt blog](https://interrupt.memfault.com/blog/): 실무 디버깅 관점에서 풍부한 인터럽트 시리즈.

### 2. MMU — 페이지 테이블과 메모리 보호

**왜 필요한가:** 우리 커널은 지금 모든 메모리에 자유롭게 접근한다. 사용자 프로세스 격리와 메모리 보호를 위해서는 **MMU의 페이지 테이블**이 필요하다. 가상 메모리의 출발점이다.

**어디서 시작하는가:**

- [s-matyukevich/raspberry-pi-os — Lesson 6](https://s-matyukevich.github.io/raspberry-pi-os/docs/lesson06/rpi-os.html): 가상 메모리 도입의 단계별 안내. 항등 매핑부터 시작해 점진적으로 분리하는 정석.
- [OSDev wiki — Setting Up Paging](https://wiki.osdev.org/Setting_Up_Paging): 일반적 페이지 테이블 개념 설명.
- [ARMv8-A Address Translation white paper](https://developer.arm.com/documentation/100940/0101): 4단계 페이지 테이블 변환의 자세한 그림.

### 3. 컨텍스트 스위치 — 여러 작업의 환상

**왜 필요한가:** 한 작업이 쓰던 모든 레지스터를 저장하고 다른 작업의 상태를 복원하는 일. 동시 실행의 환상을 만드는 핵심 메커니즘이다.

**어디서 시작하는가:**

- [s-matyukevich/raspberry-pi-os — Lesson 4 (프로세스)](https://s-matyukevich.github.io/raspberry-pi-os/docs/lesson04/rpi-os.html), [Lesson 5 (사용자 프로세스)](https://s-matyukevich.github.io/raspberry-pi-os/docs/lesson05/rpi-os.html): 컨텍스트 스위치 어셈블리의 모범.
- [Linux kernel `arch/arm64/kernel/entry.S`](https://github.com/torvalds/linux/blob/master/arch/arm64/kernel/entry.S): 가독성이 의외로 좋다.
- *Operating Systems: Three Easy Pieces* — [ostep.org](https://pages.cs.wisc.edu/~remzi/OSTEP/): 무료 PDF로 공개된 OS 교과서. 컨텍스트 스위치 챕터가 큰 그림을 잡아준다.

### 4. 시스템 콜 — EL0/EL1 경계

**왜 필요한가:** 사용자 공간(EL0)과 커널(EL1)을 분리하고, 사용자가 안전하게 커널 서비스를 요청할 수 있는 다리. 보안과 안정성의 출발점이다.

**어디서 시작하는가:**

- [s-matyukevich/raspberry-pi-os — Lesson 5](https://s-matyukevich.github.io/raspberry-pi-os/docs/lesson05/rpi-os.html): SVC 명령과 시스템 콜 디스패치 테이블의 친절한 구현.
- [xv6-riscv](https://github.com/mit-pdos/xv6-riscv): MIT의 교육용 OS. 시스템 콜 구현이 짧고 우아하다. AArch64로 옮겨 적기 좋은 참고.
- ARMv8-A 매뉴얼의 Exception Handling 챕터.

## 권장 코드베이스 — 종합

| 저장소 | 특징 |
|--------|------|
| **s-matyukevich/raspberry-pi-os** | 단계별 lesson 1~7. AArch64 라즈베리 파이 3/4 기준. 본 책 다음 단계의 정석. |
| **bztsrc/raspi3-tutorial**       | 작은 단위 튜토리얼들(blink, uart, framebuffer 등). 칩챔 학습용. |
| **OSDev wiki**                   | 백과사전. 막힐 때마다 검색하면 유용. |
| **Linux ARM64 부트 코드**        | `arch/arm64/kernel/head.S`와 `entry.S`. 실전급 참고. |
| **xv6-riscv (또는 xv6-x86)**    | 교육용 OS 전체 구현. 시스템 콜·파일시스템·스케줄러까지 한눈에. |

## 책에서 못 다룬 영역

위 네 갈래 길 너머에는 또 한 켜의 영역이 있다.

- **동시성·메모리 모델**: C11 `<stdatomic.h>`, AArch64 `LDXR`/`STXR`, 메모리 배리어(`DMB`/`DSB`/`ISB`).
- **SIMD/NEON**: 32개 128비트 벡터 레지스터로 병렬 연산.
- **디바이스 드라이버**: SD카드·USB·이더넷·디스플레이 — 각자 100~500쪽 데이터시트.
- **보안과 TrustZone**: EL3 보안 모니터, OP-TEE 같은 trusted OS.

이 영역들은 각각 책 한 권 분량의 깊이를 갖는다. 본 책이 입구까지 데려다주었으니, 깊이는 다음 여정에 맡긴다.

## Rust로의 다리

같은 베어메탈 영역을 Rust로 해보고 싶다면:

- [The Embedded Rust Book](https://docs.rust-embedded.org/book/): `#![no_std]` 베어메탈 Rust의 출발점.
- [Rust raspberrypi-OS tutorials](https://github.com/rust-embedded/rust-raspberrypi-OS-tutorials): s-matyukevich의 라즈베리 파이 OS 시리즈와 결이 비슷한 Rust 버전.
- [Tock OS](https://www.tockos.org/): 라즈베리 파이를 포함한 다양한 보드에서 도는 Rust 기반 마이크로 OS.

C로 한 번 익혀둔 손은 Rust에서 더 빨리 깊이 들어간다. 언어가 바뀌어도 부팅의 의식은 그대로 통한다.

## 작가의 작은 권유

여기서 멈춰도 충분히 멀리 왔다. 책을 덮고 자기 본업으로 돌아가도, 시스템에 대한 직관과 메모리에 대한 손 감각이 일상의 코드에 보이지 않게 스며든다. 계속 가도 좋다 — 위 네 단계를 차례로 손에 넣고 나면 자기 이름이 붙은 작은 운영체제 한 개가 생긴다. 그때 1장을 다시 펼쳐보자. "왜 지금, 다시 C인가"에 대한 그때의 답이 어떻게 달라져 있을지.

좋은 여정 되시길.
