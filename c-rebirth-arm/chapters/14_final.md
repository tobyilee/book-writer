# 14장. 진짜 ARM — Raspberry Pi 4에서 부팅하기

QEMU 창에 `hello, aarch64`가 떠오르는 순간을 처음 봤을 때의 흥분을 기억하는가. 그건 분명 우리 코드가 가상의 ARM CPU 위에서 돌고 있다는 증거였다. 그런데 며칠 지나면 묘한 갈증이 따라온다. **이게 진짜 ARM에서도 동작할까. SD카드에 구워 넣고 보드에 꽂으면 정말 우리 코드가 실리콘 위에서 깨어날까.** 책상 위에 작은 라즈베리 파이 4 보드 한 장이 있고, USB-시리얼 어댑터 한 가닥, microSD 카드 하나가 손에 잡힌다고 상상해보자. 이 작은 부품 세 개와 13장까지 익힌 부팅 코드가 만나면, 우리는 두 번째 정점에 도달한다 — **자기 손으로 만든 코드가, 자기 손에 들린 칩 위에서, OS 없이 직접 돌아간다.**

그렇다면 무엇이 바뀌어야 할까. QEMU에서 잘 동작하던 코드를 실제 보드로 옮길 때, 우리는 정확히 어떤 차이를 마주하게 되는가. 결론부터 짚자면 차이는 셋이다. **첫째는 메모리 시작 주소가 바뀐다.** 0x40000000에서 0x80000으로 내려온다. **둘째는 UART의 종류와 주소가 바뀐다.** QEMU virt의 PL011 UART에서 BCM2711의 PL011 또는 mini UART로 옮겨야 하고, GPIO 핀을 직접 시리얼 기능으로 설정해야 한다. **셋째는 펌웨어가 ELF가 아니라 flat binary(`kernel8.img`)를 요구한다.** 우리가 만든 ELF를 한 번 더 변환하는 빌드 단계가 필요하다. 이 세 가지 차이만 정확히 흡수하면, 13장의 일곱 줄 약속이 보드에서도 그대로 통한다.

자, 손에 든 보드를 천천히 살펴보자. 그리고 그 보드가 부팅할 때 정확히 어떤 흐름이 일어나는지 한 단계씩 따라가보자.

## 라즈베리 파이 4와 BCM2711 — 손에 잡히는 칩 한 장

라즈베리 파이 4 모델 B의 심장은 **Broadcom BCM2711**이라는 시스템 온 칩(SoC)이다. 보드 한가운데에 자리 잡은 검은 정사각형 칩이 그것이다. BCM2711 안에는 **ARM Cortex-A72 코어 네 개**가 들어 있고, 클럭은 1.5GHz, AArch64(64비트 ARMv8-A)를 기본으로 지원한다. 우리가 12·13장에서 QEMU `-cpu cortex-a72`로 골랐던 바로 그 코어다 — QEMU의 `virt` 머신을 Cortex-A72로 설정했던 이유가 여기서 드러난다. **QEMU에서 익힌 부팅 코드가 실제 칩에서 거의 그대로 통하도록 미리 다리를 놓아둔 셈이다.**

| 항목 | 사양 |
|------|------|
| SoC | Broadcom BCM2711 |
| CPU | ARM Cortex-A72 (ARMv8-A) × 4코어 |
| 클럭 | 1.5GHz |
| L1 캐시 | 코어당 32KB I + 32KB D |
| L2 캐시 | 1MB 공유 |
| RAM | 2GB / 4GB / 8GB LPDDR4 (모델별) |
| GPU | VideoCore VI |
| 부트 로더 | GPU 펌웨어 (closed-source) |

여기서 한 가지 흥미로운 사실을 짚어두자. **라즈베리 파이의 부트 로더는 ARM CPU가 아니라 GPU가 실행한다.** 정확히 말하면, 보드에 전원이 들어오면 가장 먼저 깨어나는 것이 GPU(VideoCore VI)이고, GPU가 SD카드에서 펌웨어 파일들을 읽어와 ARM CPU에 점프할 코드를 메모리에 올려놓고 나서야 ARM 코어 네 개가 깨어난다. 이 디자인은 라즈베리 파이 시리즈만의 독특한 약속이라 다른 SoC를 만질 때는 그대로 통하지 않는다. 그래도 한 번 손에 익혀두면 임베디드 부팅의 다양성을 이해하는 좋은 출발점이 된다.

라즈베리 파이 4의 부팅 절차를 한 번 풀어보자.

1. **전원이 들어오면** GPU가 깨어나서 보드 내부의 작은 ROM에서 1단계 부트로더를 실행한다. 이게 SD카드에서 `bootcode.bin`을 찾아 읽는다(라즈베리 파이 4부터는 이 부분이 EEPROM에 들어 있어 `bootcode.bin`이 필요 없다 — 모델 3와의 차이다).
2. **GPU 펌웨어** `start4.elf`와 `fixup4.dat`을 SD카드에서 읽어 GPU 자체를 초기화한다.
3. **`config.txt`** 라는 텍스트 설정 파일을 읽어 부팅 옵션을 결정한다 — 어느 커널 이미지를 쓸지, ARM CPU를 64비트로 띄울지 32비트로 띄울지 등.
4. **`kernel8.img`** 라는 flat binary 파일을 SD카드에서 읽어 메모리에 적재한다. 64비트 모드(AArch64)의 경우 적재 주소는 **0x80000**이다. 파일 이름의 `8`이 ARMv8(64비트)을 의미한다.
5. **ARM 코어 네 개를 모두 깨워서** 적재 주소 0x80000으로 점프시킨다. 13장에서 익힌 primary core 골라내기 약속이 여기서 그대로 발동한다 — 네 코어 중 0번만 통과시키고 나머지 셋은 잠재워야 한다.

이 다섯 단계가 라즈베리 파이 4 AArch64 베어메탈 부팅의 기본 시퀀스다. 우리가 손댈 부분은 4단계와 5단계 — **`kernel8.img`를 만들어 SD카드에 올리고, 부팅 직후 우리 코드가 동작하도록 boot.S와 kernel.c를 보드에 맞게 조정하는 일.**

## QEMU `raspi4b` 머신 — 보드 없이 미리 검증하기

보드를 손에 들기 전에 한 가지 무기를 챙기자. **QEMU의 `raspi4b` 머신**이다. QEMU 9.0(2024년 출시) 이후로 라즈베리 파이 4 모델 B 보드를 거의 그대로 흉내내는 가상 머신이 들어왔다. CPU·메모리·일부 주변 장치까지 BCM2711에 가깝게 모사하므로, **`kernel8.img`를 만들어 QEMU에서 먼저 시험한 다음 SD카드로 옮기는 흐름**이 베어메탈 디버깅의 시간을 크게 단축한다.

다만 QEMU `raspi4b`는 완벽한 모사가 아니다. 알려진 한계가 몇 가지 있다.

- **GPU(VideoCore VI)는 시뮬레이션되지 않는다.** HDMI 출력은 동작하지 않으므로, 화면 출력을 보려면 시리얼 UART에 의존해야 한다(어차피 우리도 시리얼만 쓴다).
- **일부 주변 장치**(예: 카메라 인터페이스, 일부 GPIO 변형 동작)는 단순화되거나 누락된다.
- **부트 펌웨어 흐름**이 약간 다르다 — QEMU는 보통 `start4.elf` 같은 GPU 펌웨어를 거치지 않고 곧장 `kernel8.img`를 0x80000에 올려준다.

이 차이들 때문에 "QEMU에서 동작하는데 보드에서 멈춘다"는 사고가 가끔 일어난다. 그래도 80%~90%의 베어메탈 코드는 QEMU `raspi4b`에서 그대로 검증된다. 가상 환경에서 한 번 거른 다음 실기로 넘어가는 편이 시간 절약에 절대적으로 유리하다.

QEMU `raspi4b`로 우리 `kernel8.img`를 띄우는 명령은 한 줄이다.

```sh
qemu-system-aarch64 -M raspi4b -kernel kernel8.img -serial stdio -display none
```

옵션을 풀어보자. `-M raspi4b`는 머신을 라즈베리 파이 4 모델 B로 지정한다. `-kernel kernel8.img`는 이 파일을 0x80000에 적재하고 진입점을 그곳으로 잡으라는 약속이다. `-serial stdio`는 보드의 PL011 UART 출력을 호스트 터미널의 표준 입출력으로 연결한다 — 우리 코드가 UART에 보낸 문자가 곧 호스트 터미널에 찍힌다는 의미다. `-display none`은 어차피 GPU 출력이 없으니 화면 창을 띄우지 말라는 부탁이다.

12장의 QEMU `virt` 머신과 비교해보면 명령이 거의 같은 모양이고, 머신 이름과 kernel 파일 형식만 바뀌었다. 14장의 첫 번째 큰 성취는 이 한 줄로 `hello, raspi4!`를 찍는 것이다.

## UART의 분화 — PL011과 mini-UART는 다르다

이제 가장 까다로운 차이를 정면으로 보자. **라즈베리 파이 4에는 UART가 두 개 있다.** 정확히 말하면 더 많지만, 우리가 만날 두 가지는 **PL011**(ARM PrimeCell의 표준 UART)과 **mini-UART**(BCM2711이 자체 구현한 단순 UART)다.

| 항목 | PL011 (UART0) | mini-UART (UART1) |
|------|---------------|-------------------|
| 출처 | ARM PrimeCell 표준 IP | BCM2711 자체 구현 |
| MMIO 베이스 | 0xFE201000 (Pi 4) | 0xFE215040 (Pi 4) |
| FIFO | 16바이트 깊이 | 8바이트 깊이 |
| 인터럽트 | 풍부 | 제한적 |
| 클럭 안정성 | 안정 | VPU 클럭에 의존 (변동 가능) |
| 기본 사용처 | 블루투스 또는 시리얼 콘솔 | 시리얼 콘솔 또는 블루투스 |

핵심 차이를 한 문장으로 정리하면, **PL011은 ARM 표준의 정직한 UART이고, mini-UART는 BCM2711이 한 단계 단순하게 만든 UART다.** 12장에서 QEMU virt 보드의 PL011(베이스 주소 0x09000000)을 다뤘으니, 라즈베리 파이 4의 PL011은 거의 같은 레지스터 맵을 따르고 베이스 주소만 다르다는 사실이 반갑게 들릴 것이다. **우리는 PL011 쪽으로 가자.** 12장의 코드를 거의 그대로 재활용할 수 있고, mini-UART의 클럭 변동 문제 같은 변수도 피할 수 있다.

그런데 한 가지 함정이 있다. **라즈베리 파이 4의 기본 설정에서 PL011은 블루투스 모듈에 연결되어 있고, 외부 GPIO 핀에는 mini-UART가 나와 있다.** 이걸 바꿔야 한다. `config.txt`에 한 줄을 추가하면 PL011과 mini-UART의 역할이 뒤바뀐다.

```
# config.txt
arm_64bit=1
kernel=kernel8.img
enable_uart=1
dtoverlay=disable-bt
```

각 줄을 풀어보자.

- `arm_64bit=1`: ARM CPU를 64비트(AArch64) 모드로 깨운다. 32비트 모드(AArch32)로는 우리의 64비트 코드가 동작하지 않는다.
- `kernel=kernel8.img`: 64비트 모드용 커널 이미지 파일명을 명시한다. 사실 기본값이 이 이름이라 생략해도 되지만, 명시해두면 헷갈리지 않는다.
- `enable_uart=1`: UART를 활성화하고, 시리얼 콘솔로 쓸 수 있도록 클럭을 고정시킨다. 이 옵션이 없으면 mini-UART의 클럭이 VPU 부하에 따라 흔들려서 시리얼 출력이 깨진다.
- `dtoverlay=disable-bt`: 블루투스를 비활성화해서 **PL011을 외부 GPIO 핀(14·15번)으로 라우팅한다.** 우리에게 결정적인 한 줄이다.

`dtoverlay=disable-bt`가 들어가면 PL011 UART의 송신선(TX)이 **GPIO 14번 핀**으로, 수신선(RX)이 **GPIO 15번 핀**으로 나온다. 이 두 핀이 보드의 40핀 헤더에서 우리가 USB-시리얼 어댑터를 물릴 곳이다.

### GPIO 14·15번 핀을 시리얼 기능으로 — Alt0 설정

핀 라우팅이 끝나도 한 단계가 더 남았다. 라즈베리 파이의 GPIO 핀들은 각각 여러 가지 **대체 기능(alternate function)** 을 가지고 있다. 같은 14번 핀이 일반 입출력으로 쓰일 수도 있고, UART의 TX로 쓰일 수도 있다. 부팅 직후 어느 기능이 활성화될지는 GPFSEL(GPIO Function Select) 레지스터의 비트로 결정된다. **PL011 UART를 쓰려면 GPIO 14·15번 핀의 기능을 Alt0(대체 기능 0)으로 세팅해야 한다.**

GPFSEL 레지스터의 비트 구조를 한 번 보자. GPFSEL1 레지스터(베이스 0xFE200004)가 GPIO 10번부터 19번까지를 담당하고, 각 핀당 3비트씩 할당된다. 14번 핀은 그 안의 12~14비트, 15번 핀은 15~17비트다. 각 3비트 필드의 값에 따라 핀의 기능이 정해진다.

| 3비트 값 | 의미 |
|---------|------|
| `0b000` | 입력 |
| `0b001` | 출력 |
| `0b100` | Alt0 |
| `0b101` | Alt1 |
| `0b110` | Alt2 |
| `0b111` | Alt3 |
| `0b011` | Alt4 |
| `0b010` | Alt5 |

PL011 TX/RX는 14·15번 핀의 **Alt0**에 매핑되어 있다. 그래서 두 핀의 3비트 필드를 모두 `0b100`으로 세팅하면 된다. C 코드로 풀어보면 다음과 같다.

```c
#define GPFSEL1   ((volatile uint32_t*)0xFE200004)

void uart_init(void) {
    uint32_t sel = *GPFSEL1;
    sel &= ~((7u << 12) | (7u << 15));   // 14·15번 비트 필드 클리어
    sel |=  ((4u << 12) | (4u << 15));   // 둘 다 Alt0(=0b100)
    *GPFSEL1 = sel;

    // 이제 PL011 레지스터를 초기화한다 (다음 절)
    ...
}
```

7장에서 익힌 비트 마스크와 시프트가 여기서 또 한 번 일터로 나간다. `(7u << 12)`로 12·13·14비트 자리에 `0b111`을 만들고, `&= ~(...)`로 그 자리를 한 번 0으로 비운 뒤, `|= (4u << 12)`로 `0b100`을 박는다. **클리어 후 세팅**이라는 이 두 단계 관용구는 임베디드 레지스터 조작의 핵심 리듬이다. 만약 클리어 없이 곧장 `|=`를 하면 이전 값과 새 값이 OR로 섞여서 의도와 다른 비트가 켜질 수 있다.

`volatile` 키워드를 잊지 말자. 7장에서 다뤘던 그 약속이다 — MMIO 주소에 대한 접근은 컴파일러가 최적화로 날려버려서는 안 되므로 반드시 `volatile`을 붙인다. 베어메탈 사고의 절반이 `volatile`을 빼먹어서 일어난다. 끔찍한 일이다.

### PL011 레지스터 초기화 — 보레이트와 프레임

GPIO 라우팅이 끝나면 PL011 UART 자체를 초기화해야 한다. 우리가 쓸 레지스터는 네 개다.

| 레지스터 | 베이스 + 오프셋 | 역할 |
|---------|----------------|------|
| `UART_DR`     | 0xFE201000 + 0x00 | 데이터 (read = 수신, write = 송신) |
| `UART_FR`     | 0xFE201000 + 0x18 | 플래그 (busy·FIFO 상태) |
| `UART_IBRD`   | 0xFE201000 + 0x24 | 정수 보레이트 분주 |
| `UART_FBRD`   | 0xFE201000 + 0x28 | 소수 보레이트 분주 |
| `UART_LCRH`   | 0xFE201000 + 0x2C | 라인 제어 (프레임 형식) |
| `UART_CR`     | 0xFE201000 + 0x30 | 제어 (UART·송수신 활성화) |

보레이트를 어떻게 계산하는가. PL011은 클럭 주파수를 보레이트로 나눈 값을 분주기에 넣는다. **`enable_uart=1`을 `config.txt`에 적은 덕분에 PL011의 입력 클럭이 48MHz로 고정**된다. 우리가 흔히 쓰는 115200 보레이트를 목표로 하면, 분주값은 `48000000 / (16 × 115200) = 26.0417`. 정수부 26은 `UART_IBRD`에, 소수부 0.0417은 64를 곱해서 `UART_FBRD`(보통 3)에 넣는다.

```c
#define UART_BASE 0xFE201000UL
#define UART_DR   ((volatile uint32_t*)(UART_BASE + 0x00))
#define UART_FR   ((volatile uint32_t*)(UART_BASE + 0x18))
#define UART_IBRD ((volatile uint32_t*)(UART_BASE + 0x24))
#define UART_FBRD ((volatile uint32_t*)(UART_BASE + 0x28))
#define UART_LCRH ((volatile uint32_t*)(UART_BASE + 0x2C))
#define UART_CR   ((volatile uint32_t*)(UART_BASE + 0x30))

void uart_init(void) {
    // (1) GPIO 14·15를 Alt0으로 — 앞 절 코드
    // ...

    *UART_CR   = 0;            // UART 일단 끈다
    *UART_IBRD = 26;           // 정수 분주
    *UART_FBRD = 3;            // 소수 분주
    *UART_LCRH = (3 << 5);     // 8N1, FIFO 비활성
    *UART_CR   = (1 << 0)      // UART enable
               | (1 << 8)      // TX enable
               | (1 << 9);     // RX enable
}

void uart_putc(char c) {
    while (*UART_FR & (1 << 5)) { }   // TX FIFO full이면 대기
    *UART_DR = (uint32_t)c;
}

void uart_puts(const char *s) {
    while (*s) uart_putc(*s++);
}
```

`UART_LCRH`의 비트 5·6번이 워드 길이 — `0b11`이면 8비트 데이터다. 패리티(parity)와 정지비트(stop bit)는 기본값이 그대로 8N1(8 데이터·패리티 없음·1 정지비트)이라 별도 설정 없이 충분하다. `UART_CR`의 0·8·9번 비트를 각각 켜면 UART 본체·송신부·수신부가 모두 활성화된다.

`uart_putc` 함수에서 `UART_FR`(플래그 레지스터)의 5번 비트를 검사하는 부분이 핵심이다. 이 비트가 1이면 송신 FIFO가 가득 차 있다는 뜻이므로, 빈자리가 생길 때까지 빙빙 돈다. 사실상 폴링이다. 인터럽트 기반 드라이버를 짠다면 이 폴링을 인터럽트 핸들러로 대체하지만, 14장에서는 가장 단순한 폴링 방식으로 충분하다.

자, 코드는 길지만 결국 이 모두가 한 가지를 한다 — **GPIO 핀을 시리얼 기능으로 돌리고, 클럭을 보레이트에 맞게 나누고, UART 송수신부를 켠다.** 한 번 손으로 짜두면 라즈베리 파이 4 베어메탈의 절반 이상은 손에 들어온 셈이다.

## kernel8.img 만들기 — ELF에서 flat binary로

13장까지 우리가 만든 산출물은 `kernel.elf`였다. ELF는 메타데이터(섹션 헤더·심볼 테이블·재배치 정보 등)가 풍부하게 들어 있는 포맷이라 디버거와 잘 어울린다. 그런데 라즈베리 파이 4의 GPU 펌웨어는 ELF를 모른다. **펌웨어가 원하는 것은 메모리에 한 덩어리로 떨어뜨리면 곧장 실행 가능한, 순수한 바이트열**이다. 이걸 **flat binary**라고 부른다.

ELF를 flat binary로 변환하는 도구가 `objcopy`다. 이름이 "object copy"인데 사실은 "한 포맷에서 다른 포맷으로 변환"하는 만능 변환기에 가깝다. AArch64 크로스 도구 모음에서 가져온 `aarch64-elf-objcopy`로 한 줄에 변환한다.

```sh
aarch64-elf-objcopy -O binary kernel.elf kernel8.img
```

`-O binary` 옵션이 "출력 형식을 raw binary로"라는 약속이다. 이 한 줄이 ELF의 메타데이터를 모두 잘라내고, `.text`·`.rodata`·`.data` 섹션의 실제 바이트만 차곡차곡 이어붙인 순수 바이너리를 만들어낸다. 결과 파일이 우리가 SD카드에 올릴 `kernel8.img`다.

여기서 한 가지 약속을 다시 짚자. **링커 스크립트의 시작 주소가 라즈베리 파이 4의 로드 주소와 일치해야 한다.** 13장의 QEMU virt 보드용 링커 스크립트는 `. = 0x40000000;`이었지만, 라즈베리 파이 4용은 다음과 같이 바뀐다.

```ld
ENTRY(_start)
SECTIONS
{
    . = 0x80000;                /* GPU 펌웨어가 kernel8.img를 이 주소에 적재 */
    .text : { KEEP(*(.text.boot)) *(.text*) }
    .rodata : { *(.rodata*) }
    .data : { *(.data*) }
    . = ALIGN(8);
    __bss_start = .;
    .bss : { *(.bss*) *(COMMON) }
    . = ALIGN(8);
    __bss_end = .;
    . = ALIGN(16);
    . += 0x4000;
    stack_top = .;
}
```

13장 스크립트와 비교하면 단 한 줄, `. = 0x40000000;`이 `. = 0x80000;`으로 바뀌었다. 이 한 줄이 보드를 바꾼다. **`objcopy`로 만든 `kernel8.img`는 0x80000부터 시작하는 메모리 이미지로 해석되므로, 우리 코드 안의 모든 절대 주소 참조도 0x80000을 기준으로 해석되어야 한다.** 링커 스크립트의 시작 주소가 그 일치를 보장한다.

자, 이제 `Makefile`로 한 번에 묶어보자.

```make
CC      = aarch64-elf-gcc
LD      = aarch64-elf-ld
OBJCOPY = aarch64-elf-objcopy

CFLAGS  = -ffreestanding -nostdlib -nostartfiles -mgeneral-regs-only \
          -mcpu=cortex-a72 -O2 -Wall -Wextra
LDFLAGS = -T linker.ld -nostdlib

OBJS = boot.o kernel.o

kernel8.img: kernel.elf
	$(OBJCOPY) -O binary $< $@

kernel.elf: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

%.o: %.S
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

qemu: kernel8.img
	qemu-system-aarch64 -M raspi4b -kernel kernel8.img \
	                    -serial stdio -display none

clean:
	rm -f *.o *.elf *.img
```

`make` 한 줄이면 `kernel8.img`가 만들어지고, `make qemu`로 QEMU `raspi4b`에서 검증할 수 있다. `-mcpu=cortex-a72` 옵션은 컴파일러가 Cortex-A72에 최적화된 명령을 쓰도록 알려주는 약속인데, 베어메탈 코드는 호환성보다 정확한 칩 지정이 안전하다.

## SD카드 셋업 — 부팅 파일 다섯 개

QEMU `raspi4b`에서 `hello, raspi4!`가 찍혔다면, 이제 실제 SD카드로 옮길 차례다. 라즈베리 파이 4 부팅에 필요한 파일은 다음 다섯 개다.

| 파일 | 출처 | 역할 |
|------|------|------|
| `bootcode.bin` | (Pi 4는 EEPROM이 대체, 보통 불필요) | 1단계 부트로더 |
| `start4.elf` | Raspberry Pi firmware 저장소 | GPU 펌웨어 |
| `fixup4.dat` | Raspberry Pi firmware 저장소 | GPU 초기화 데이터 |
| `config.txt` | 우리가 직접 작성 | 부팅 설정 |
| `kernel8.img` | 우리 빌드 산출물 | 64비트 커널 이미지 |

`start4.elf`와 `fixup4.dat`은 라즈베리 파이 재단의 공식 firmware 저장소(github.com/raspberrypi/firmware)의 `boot/` 디렉토리에서 가져오는 닫힌 소스 파일이다. 라즈베리 파이 4의 GPU 초기화에 필요한 펌웨어 자체라서 다른 파일로 대체할 수 없다.

SD카드는 **FAT32**로 포맷한다. macOS 사용자라면 `diskutil`로, Linux 사용자라면 `mkfs.vfat`으로, 또는 Raspberry Pi Imager 같은 도구로 빈 FAT32 파티션을 만들 수 있다. 그 안에 위 다섯 파일을 모두 복사해 넣으면 SD카드가 부팅 가능한 상태가 된다.

`config.txt`는 앞 절에서 본 그 네 줄이다. 다시 한번 정리해두자.

```
arm_64bit=1
kernel=kernel8.img
enable_uart=1
dtoverlay=disable-bt
```

이 네 줄이 빠지거나 잘못 적히면 보드가 깨어나지 않거나, UART에서 글자가 깨져 나오거나, 32비트 모드로 진입해서 우리 64비트 코드가 즉시 폭주한다. 한 줄도 빠뜨리지 말자.

macOS에서 SD카드에 굽는 한 흐름은 다음과 같다.

```sh
# 1) SD카드 디바이스 식별
diskutil list

# 2) 마운트 해제 (예: /dev/disk5)
diskutil unmountDisk /dev/disk5

# 3) FAT32로 포맷
diskutil eraseDisk FAT32 RPI4 MBRFormat /dev/disk5

# 4) 파일 복사
cp bootcode.bin start4.elf fixup4.dat /Volumes/RPI4/
cp config.txt kernel8.img /Volumes/RPI4/

# 5) 안전하게 추출
diskutil eject /dev/disk5
```

디바이스 이름(`/dev/disk5`)은 사람마다 다르니 반드시 `diskutil list`로 확인하자. 잘못된 디바이스를 지정하면 호스트 디스크를 날릴 수도 있는 끔찍한 사고가 일어난다. 늘 한 번 더 확인하는 습관을 들이자.

## USB-시리얼 어댑터 — 보드와 PC를 잇는 한 가닥

이제 마지막 다리다. **보드의 UART에서 나오는 시리얼 신호를 PC의 터미널로 끌어오는 USB-시리얼 어댑터.** Amazon이나 동네 부품점에서 5천 원에서 1만 5천 원 사이에 살 수 있는 작은 부품으로, FTDI FT232 칩이나 CP2102 칩을 쓴 어댑터가 흔하다. 보드에 USB 커넥터가 있고, 반대쪽에 보통 5개 또는 6개의 점프 와이어가 나온다.

연결할 핀은 세 개다. **GND(접지), 보드의 TX → 어댑터의 RX, 보드의 RX → 어댑터의 TX.** 라즈베리 파이 4의 40핀 헤더에서 각 핀의 위치는 다음과 같다.

| 보드 핀 번호 | 신호 | 어댑터 연결 |
|------------|------|-----------|
| 6번 | GND | 어댑터의 GND |
| 8번 (GPIO 14) | TX | 어댑터의 RX |
| 10번 (GPIO 15) | RX | 어댑터의 TX |

전원선(5V·3.3V)은 **연결하지 않는다.** 보드는 자체 USB-C 전원으로 켜고, 어댑터는 PC USB로 자체 전원을 받기 때문에 전원선을 연결하면 두 전원이 충돌할 수 있다. **그라운드만 공유하고, 데이터선 두 줄만 교차로 연결한다.** TX는 송신, RX는 수신이므로 양쪽이 서로 보내는 쪽을 받는 쪽에 물려야 하는 것은 직관적이다. 이 교차를 잊으면 신호가 전혀 안 흐르거나 양쪽이 동시에 송신해서 충돌한다. 잊지 말자.

PC 쪽에서 시리얼 콘솔을 여는 방법은 OS에 따라 다르다.

**macOS:** 어댑터가 인식되면 `/dev/cu.usbserial-XXXX` 형태의 디바이스 노드가 나타난다.

```sh
# 1) 디바이스 확인
ls /dev/cu.usbserial-*

# 2) screen으로 콘솔 열기 (115200 8N1)
screen /dev/cu.usbserial-AB0LXTZH 115200

# 빠져나오기: Ctrl+A 다음 K, y로 종료 확인
```

**Linux:** `/dev/ttyUSB0` 같은 노드가 나타난다.

```sh
ls /dev/ttyUSB*
sudo screen /dev/ttyUSB0 115200
# 또는 minicom -D /dev/ttyUSB0 -b 115200
```

`screen` 대신 `minicom`이나 `picocom`을 쓰는 사람도 많다. 어느 도구를 쓰든 핵심은 **115200 보레이트, 8 데이터비트, 패리티 없음, 1 정지비트**(115200 8N1)다. 우리의 PL011 초기화가 정확히 이 설정을 가정하므로, 콘솔 도구도 같은 설정으로 맞춰야 한다.

자, 이제 모든 준비가 끝났다. SD카드를 보드에 꽂고, USB-시리얼을 PC에 꽂고, 시리얼 콘솔을 연 상태에서 보드에 USB-C 전원을 연결한다. 몇 초가 지나면 GPU 펌웨어가 깨어나고, `kernel8.img`가 0x80000에 적재되고, ARM Cortex-A72 네 코어 중 0번이 우리의 `_start`로 점프하고, 시리얼 콘솔에 `hello, raspi4!`가 떠오른다. **두 번째 정점이다.**

## 디버깅 — 보드는 멈췄는데 시리얼은 침묵한다

물론 한 번에 글자가 떠오르는 행운은 흔하지 않다. 보드에 전원을 줬는데 시리얼 콘솔이 침묵한다면 어디부터 봐야 할까. 손에 익혀둘 만한 체크리스트를 정리해두자.

**(1) 보드의 ACT LED가 깜빡이는가.** 라즈베리 파이 4의 보드에는 빨간 PWR LED와 녹색 ACT LED가 있다. 전원이 들어오면 PWR이 켜지고, GPU가 SD카드를 읽으면 ACT가 깜빡인다. PWR이 안 켜지면 전원 자체의 문제이고, ACT가 안 깜빡이면 SD카드 인식의 문제다. ACT가 잠깐 깜빡이다가 멈추면 펌웨어 파일(`start4.elf`·`fixup4.dat`)이 빠졌거나 손상됐을 가능성이 크다.

**(2) `config.txt`가 정확한가.** 자주 일어나는 실수가 `enable_uart=1` 누락이다. 이 한 줄이 빠지면 UART 클럭이 가변이라 글자가 깨져 나오거나 아예 출력되지 않는다. `dtoverlay=disable-bt`가 빠지면 PL011이 블루투스에 계속 묶여 있어서 GPIO 14·15번 핀에는 mini-UART가 나오므로 우리 PL011 코드가 동작하지 않는다. **이 두 줄을 직접 다시 한번 확인하자.**

**(3) USB-시리얼 배선이 교차되었는가.** TX-RX 교차를 잊고 일자로 연결하면 양쪽이 동시에 송신하느라 신호가 깨진다. 한 번 다시 보자.

**(4) 보레이트가 일치하는가.** `screen` 명령에서 115200을 입력했는지, 보드 코드에서 `UART_IBRD = 26`(48MHz / (16 × 115200) = 26.04)을 정확히 박았는지 한 번 더 확인하자. 보레이트가 어긋나면 신호는 흐르지만 글자가 깨져서 알아볼 수 없는 기호의 연속으로 나타난다.

**(5) `kernel8.img`가 SD카드 루트에 있는가.** 가끔 SD카드의 서브디렉토리에 들여놓고 펌웨어가 못 찾는 사고가 있다. 모든 파일은 SD카드의 **최상위 디렉토리**에 있어야 한다.

**(6) QEMU에서 동작했는가.** SD카드 굽기 전에 QEMU `raspi4b`로 같은 `kernel8.img`를 시험해보자. QEMU에서도 안 나오면 코드 자체의 문제고, QEMU에서는 나오는데 보드에서만 안 나오면 SD카드·배선·`config.txt` 쪽의 문제다. **이 양분이 디버깅 시간을 크게 줄인다.**

이 여섯 체크 항목으로 99%의 첫 부팅 실패가 잡힌다. 그래도 안 되면 두 가지 길이 더 있다 — 하나는 JTAG 디버거를 연결해서 ARM 코어의 상태를 직접 들여다보는 길(라즈베리 파이 4에 JTAG 핀이 있다), 다른 하나는 LED를 GPIO로 토글하면서 어디까지 코드가 진행되었는지 표시하는 가장 원시적인 디버깅(printf debugging의 베어메탈 버전이다). 본 책에서 깊이 다루지는 않지만, "어디서 막혔는지 모를 때는 LED 한 줄을 켜보는" 습관이 임베디드 디버깅의 시작이다.

## ch14-rpi4 예제 — 손으로 빌드하고 굽기

이번 장의 핵심 예제는 `example/ch14-rpi4/`다. 12장의 네 파일 구조를 그대로 가져와서 라즈베리 파이 4용으로 조정한 한 세트다.

```
ch14-rpi4/
├── boot.S              # primary core 골라내기 + 스택 + BSS 클리어
├── kernel.c            # PL011 초기화 + uart_puts("hello, raspi4!\n")
├── linker.ld           # 시작 주소 0x80000
├── Makefile            # kernel8.img 생성 + QEMU 실행 타깃
├── config.txt          # arm_64bit=1, enable_uart=1, dtoverlay=disable-bt
└── README.md           # SD카드 셋업, USB-시리얼 배선, QEMU 명령
```

`make`로 `kernel8.img`를 만들고, `make qemu`로 QEMU `raspi4b`에서 검증한다. `make sd-files`로 SD카드에 복사할 파일들을 `dist/` 디렉토리에 모아주는 보조 타깃도 들어 있다. `README.md`에 macOS·Linux 양쪽의 SD카드 굽기 흐름과 시리얼 콘솔 연결법이 친절하게 적혀 있다.

여기서 한 가지 짚어둘 점이 있다. `aarch64-elf-gcc`가 호스트에 설치되어 있지 않으면 빌드가 실패한다. macOS의 경우 Homebrew로 설치할 수 있다.

```sh
brew install --cask gcc-aarch64-embedded
# 또는
brew install aarch64-elf-gcc
```

Linux(Ubuntu/Debian 계열)는 `apt`로.

```sh
sudo apt install gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu
# 이 경우 Makefile의 CC를 aarch64-linux-gnu-gcc로 바꿔주자
```

크로스 도구의 이름이 배포판마다 미묘하게 다르다는 점이 베어메탈의 흔한 함정이다. `example/README.md`에 이 변형을 정리해두었으니 막히는 분은 그쪽을 참고하자. **QEMU만 있고 크로스 도구가 없는 경우**라면, 다음 절에서 본 QEMU 실행 흐름까지만 손에 익히고 실기 부팅은 다음 기회로 미뤄도 좋다. 책의 큰 그림은 여기서 충분히 손에 들어온다.

## 마무리 — 첫 번째와 두 번째 정점 사이

13장에서 익힌 일곱 줄의 약속이 14장에서 어떻게 살아 돌아왔는지 한 번 짚어보자. **primary core 골라내기**(`mpidr_el1` + `and` + `cbnz`)는 그대로다. **스택 포인터 셋업**(`ldr` + `mov sp`)도 그대로다. **BSS 클리어**도 그대로다. **`bl kernel_main`을 통한 어셈블리-C 경계 넘기**도 그대로다. 보드가 바뀌었지만 부팅의 골격은 한 줄도 바뀌지 않았다 — 13장의 학습이 보드와 무관하게 통한다는 사실이 14장에서 비로소 체감된다.

바뀐 것은 메모리 시작 주소, UART의 베이스 주소와 초기화 절차, ELF에서 flat binary로의 변환, SD카드 부팅 파일 다섯 개뿐이다. 이 차이는 **링커 스크립트 한 줄, `objcopy` 한 줄, `kernel.c`의 UART 초기화 함수 한 토막, 그리고 SD카드의 `config.txt` 네 줄**로 모두 흡수된다. 손에 들어오는 변경의 양이 생각보다 적다는 사실이 베어메탈의 매력 중 하나다.

기억해두자. **QEMU에서 한 번, 실기에서 한 번 — 두 번의 정점이 우리에게 있다.** 둘 모두 자기 손으로 만든 코드가 ARM CPU 위에서 OS 없이 직접 도는 경험이며, 한 번 손에 박히고 나면 평생 잊히지 않는다. 그리고 이 경험이 다음 장 — 인터럽트, MMU, 컨텍스트 스위치, 시스템 콜이라는 진짜 OS의 영역 — 으로 가는 모든 길의 출발점이 된다.

자, 다음 장에서는 작별의 인사를 짧게 나누고, 이 책이 다 다루지 못한 영역으로 가는 네 갈래 길을 함께 살펴보자.
