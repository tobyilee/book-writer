# 12장. 첫 AArch64 커널 — QEMU에서 "Hello, ARM!"

11장의 마지막 줄을 지나며 우리는 이런 결심을 했다 — **호스트 OS 없는 세계로 한 걸음 들어가 보자.** 그 한 걸음의 결과를 이번 장에서 손에 쥔다. 코드 한 줄이 ARM CPU 위에서 직접 도는 첫 경험. 이 책의 정점이다.

여기서 한 가지 정직한 안내부터 해 둔다. **이 장과 다음 장은 같은 코드를 두 번 본다.** 12장은 "네 파일이 어떻게 협력해서 첫 글자에 도달하는가" — 큰 그림. 13장은 "왜 그 한 줄이 거기에 있는가" — 줄별 해부. 그러니 이 장에서 모든 줄을 다 설명하지 않는 건 의도된 일이다. 우선 동작하는 그림을 손에 잡고, 한 명령씩 들어가는 깊이는 다음 장에 약속한다. 작동하는 무언가를 먼저 만들고, 그 다음에 안을 들여다보는 순서는 학습에서 자주 도움이 되는 길이다.

## 목표 — 한 줄로

QEMU의 `-M virt -cpu cortex-a72` 보드에 우리가 만든 `kernel.elf`를 올려, 시리얼 라인으로 `hello, aarch64` 한 줄을 흘려보낸다.

```
$ make run
QEMU 시작 — 종료는 Ctrl+A 누른 뒤 x
hello, aarch64
```

이 한 줄이 화면에 닿는 순간이 이 책에서 가장 진하게 남는 장면이다. 자바 시절을 떠올려 보자. `System.out.println("Hello")`가 한 줄. 그 한 줄이 JVM을 거쳐 OS를 거쳐 터미널까지 가는 동안 우리는 그 사슬을 의식할 일이 없었다. 지금 우리가 만들고 있는 건 그 사슬 자체다 — **OS도 JVM도 끼지 않은, 우리 코드와 ARM CPU와 UART 하드웨어만 있는 세계.**

자, 그럼 그 세계로 들어가는 네 파일을 본다.

## 네 파일의 큰 그림

```
example/ch12-aarch64-hello/
├── boot.S       — 진입 어셈블리. _start에서 시작해 kernel_main을 부른다
├── kernel.c     — kernel_main(). UART에 "hello, aarch64\n"을 한 글자씩 송신
├── linker.ld    — 메모리 배치. .text.boot이 맨 앞, 로드 주소 0x40080000
└── Makefile     — 툴체인을 찾아 빌드. make run이 QEMU 실행
```

각 파일이 하는 일을 한 문장으로 잡아 두자.

- **`boot.S`** — "전기가 들어왔다. CPU 0번만 살리고, 스택을 잡고, `.bss`를 0으로 밀고, C 함수로 점프한다."
- **`kernel.c`** — "C 세계에 도착했다. UART 데이터 레지스터에 한 바이트씩 써서 글자를 흘려보낸다."
- **`linker.ld`** — "ELF의 각 섹션을 메모리 어디에 둘지 정한다. 부팅 진입점은 맨 앞에, 스택 영역은 `.bss` 뒤에."
- **`Makefile`** — "툴체인을 찾아 두 오브젝트 파일을 만들고 링커 스크립트에 따라 묶어 `kernel.elf`로 내놓는다."

이 네 파일이 어떻게 협력하는가를 데이터 흐름으로 그려 보자.

```
        electricity / qemu -kernel kernel.elf
                       │
                       ▼
       ┌───────────────────────────────┐
       │  CPU 4개 코어 동시 진입         │ ← _start (boot.S)
       │  EL2, MMU off, sp는 쓰레기      │
       └───────────────┬───────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
    primary (코어 0)      나머지 코어
              │                 │
              │            halt (wfe)
              ▼
   sp ← stack_top    (linker.ld가 정한 자리)
   .bss를 0으로 클리어 (__bss_start ~ __bss_end)
              │
              ▼
        kernel_main()    (kernel.c — C 세계 진입)
              │
              ▼
   uart_puts("hello, aarch64\n")
              │
              ▼
   UART0 DR (0x09000000)에 바이트 쓰기
              │
              ▼
   QEMU PL011 모델 → -nographic 터미널 → 화면
```

이 흐름이 한 장면으로 들어오면 12장의 큰 그림은 거의 잡힌 거다. 이제 각 조각을 따로따로 본다.

## `boot.S` — 진입과 무대 준비

부팅 직후의 ARM CPU는 어떤 상태일까? 11장에서 한번 짚었지만 다시 정리하자.

- Exception Level은 EL2 (또는 일부 설정에선 EL1)
- MMU와 데이터 캐시 비활성
- 일반 레지스터(X0~X30)는 미정의 — 쓰레기 값
- 스택 포인터(`sp`)도 미정의
- **4개 코어가 동시에 진입한다** — QEMU virt 보드는 기본 4 코어 cortex-a72

이 상태에서 우리가 첫 번째로 할 일은 코어 하나만 골라내는 것이다. 4개가 한꺼번에 `kernel_main`을 부르면 같은 UART에 네 명이 동시에 글자를 쓰는 끔찍한 일이 벌어진다.

```asm
    .section .text.boot, "ax"
    .globl _start
_start:
    /* (1) primary core(코어 0) 골라내기.
     *     mpidr_el1의 하위 두 비트가 코어 번호. 0이 아니면 정지. */
    mrs     x0, mpidr_el1
    and     x0, x0, #3
    cbnz    x0, halt
```

`mpidr_el1`은 "Multiprocessor Affinity Register"라는 시스템 레지스터다. 한 줄로 코어 번호를 알려준다. 하위 두 비트가 0이면 우리가 통과하고, 나머지 세 코어는 `halt`로 보내져 영원히 잠든다. (`wfe`/`b halt` 두 줄이 그 잠.)

다음은 스택. 11장에서 정리했듯, `sp`에 유효한 메모리 주소를 박지 않으면 첫 함수 호출 한 줄에서 우주가 끝난다.

```asm
    /* (2) 스택 포인터 설정.
     *     linker.ld가 .bss 끝에 stack_top 심볼을 둔다. */
    ldr     x0, =stack_top
    mov     sp, x0
```

`stack_top`이라는 심볼은 우리 어셈블리 어디에도 정의돼 있지 않다. **그건 링커 스크립트가 약속해 주는 이름이다.** `linker.ld`를 보면 `.bss` 뒤에 64KB 공간을 잡고 그 끝에 `stack_top`을 박는 코드가 들어 있다. 어셈블리는 그 약속만 믿고 `ldr`로 끌어다 쓴다.

세 번째는 `.bss` 클리어. C 표준이 "초깃값 없는 전역 변수는 0"이라고 약속했으니, 그 약속을 베어메탈에서 우리가 지킨다.

```asm
    /* (3) .bss를 0으로 클리어. */
    ldr     x0, =__bss_start
    ldr     x1, =__bss_end
1:  cmp     x0, x1
    b.ge    2f
    str     xzr, [x0], #8        // 8바이트씩 0 쓰기, 포인터 자동 증가
    b       1b
2:
```

`__bss_start`와 `__bss_end`도 링커 스크립트가 약속해 주는 심볼이다. `xzr`는 AArch64의 "zero register" — 항상 0을 들고 있는 가짜 레지스터다. `str xzr, [x0], #8`은 "0을 x0가 가리키는 주소에 8바이트로 쓰고, x0를 8만큼 증가시킨다"는 한 줄이다. 짧은 루프 하나로 .bss 전체를 0으로 민다.

마지막은 C 코드로 점프.

```asm
    /* (4) C 코드로 점프 — 돌아오지 않는다고 가정 */
    bl      kernel_main

halt:
    wfe
    b       halt
```

`bl kernel_main`이 우리가 어셈블리에서 C로 건너가는 단 한 줄이다. `bl`은 "branch with link" — 리턴 주소를 `x30`에 저장하고 점프한다. `kernel_main`이 끝나면 그 주소로 돌아오는데, 우리 `kernel_main`은 무한 루프라 돌아오지 않는다. 만에 하나 돌아오더라도 `halt`로 떨어져 안전하게 멈춘다.

이 `boot.S`의 줄별 의미 — `mrs`가 정확히 무엇이고, `cbnz`가 어떤 비교를 하고, `b.ge`가 signed인지 unsigned인지 — 는 13장의 몫이다. 12장에서는 "네 단계의 흐름"만 손에 잡으면 된다. 코어 하나 고르기, 스택 잡기, `.bss` 청소, C로 점프. 그 넷이다.

## `kernel.c` — UART와 만나는 자리

C 세계에 도착했다. 손에 있는 건 무엇인가? **스택, UART 주소, 우리 코드.** 그게 전부다. `printf`도 없고, `malloc`도 없고, `errno`도 없다 — 11장에서 정리한 그대로의 freestanding 세계.

이 세계의 출력은 UART 데이터 레지스터에 한 바이트 쓰기로 시작된다.

```c
#include <stdint.h>

#define UART0_BASE   0x09000000UL
#define UART0_DR     (UART0_BASE + 0x000)   /* Data Register */
#define UART0_FR     (UART0_BASE + 0x018)   /* Flag Register */
#define UART_FR_TXFF (1u << 5)              /* Transmit FIFO Full */

static volatile uint32_t *const uart_dr = (volatile uint32_t *)UART0_DR;
static volatile uint32_t *const uart_fr = (volatile uint32_t *)UART0_FR;
```

여기서 멈추고 한 가지를 짚자. **`volatile` 키워드가 빠지면 일이 끔찍해진다.** 우리가 `*uart_dr = 'h'; *uart_dr = 'i';`를 연속으로 쓰면, 컴파일러는 "같은 주소에 같은 값을 두 번 쓸 이유가 없네 — 첫 줄은 어차피 덮어쓰일 테니 생략하자"고 판단할 수 있다. 그 판단이 일반 메모리에선 맞지만, MMIO 레지스터에선 **틀린다.** UART 데이터 레지스터에 쓰기는 "값을 저장한다"가 아니라 "한 글자를 송신한다"는 부수 효과다. 한 줄을 생략하면 한 글자가 사라진다.

`volatile`은 컴파일러에게 "이 주소에 대한 접근은 부수 효과가 있으니, 코드에 적힌 그대로 모든 접근을 수행하라"는 명령이다. 베어메탈 코드의 흔한 함정이 바로 이 키워드를 빼먹는 일이다 — 11장 7.7절에서 미리 경고했던 함정이 여기서 실제로 일한다.

이제 한 글자 송신 함수.

```c
static void uart_putc(char c)
{
    /* TX FIFO가 가득 차 있으면 빌 때까지 대기 */
    while (*uart_fr & UART_FR_TXFF) { /* spin */ }
    *uart_dr = (uint32_t)(unsigned char)c;
}
```

PL011 UART는 작은 송신 FIFO를 들고 있어, 한 번에 여러 글자를 받아 두고 시리얼 라인으로 천천히 흘려보낸다. 그 FIFO가 가득 차 있으면 우리는 빈자리가 생길 때까지 기다린다 — Flag Register의 5번 비트(`TXFF`, Transmit FIFO Full)가 떨어질 때까지 spin한다. 그게 이 짧은 함수의 전부다.

여기서 7장의 "비트 조작 절"이 일을 하기 시작한다. `(1u << 5)`로 5번 비트의 마스크를 만들었고, `& UART_FR_TXFF`로 그 한 비트만 뽑아냈다. 베어메탈 코드는 이런 비트 마스크 한 줄이 매 줄마다 나온다. 7장의 손풀기가 여기서 그대로 쓰인다.

문자열 송신은 한 줄짜리 루프.

```c
static void uart_puts(const char *s)
{
    while (*s) {
        if (*s == '\n') uart_putc('\r');
        uart_putc(*s++);
    }
}
```

흥미로운 한 줄이 있다 — `if (*s == '\n') uart_putc('\r');`. 시리얼 터미널은 "줄바꿈"을 두 글자로 해석한다 — Carriage Return(`\r`, 0x0D)으로 커서를 줄 시작으로 보내고, Line Feed(`\n`, 0x0A)으로 한 줄 내린다. 우리 C 문자열은 `\n`만 들고 있으니, `\n` 앞에 `\r`을 자동으로 끼워 넣는다. 빼먹으면 글자가 사선으로 쏟아진다 — `hello, aarch64`의 다음 줄이 `aarch64` 뒤에서 시작되지 않고 그 자리에 이어 붙는다.

그리고 진입점.

```c
void kernel_main(void)
{
    uart_puts("hello, aarch64\n");

    /* 정점에 도달했으니, 영원히 여기에 머무른다. */
    for (;;) {
        __asm__ volatile ("wfe");
    }
}
```

`kernel_main`의 이름이 `main`이 아니라는 점이 11장에서 미리 다뤄둔 의미를 가진다. **호스트 환경에서 `main`이라는 이름이 가졌던 특별함은 베어메탈에서는 없다.** 이름은 우리 마음이고, `boot.S`의 `bl kernel_main`이 가리키는 심볼이면 그만이다.

마지막 `for (;;)` 루프 안의 `wfe`(Wait For Event)는 CPU에게 "할 일 없으니 잠시 자라"는 명령이다. 폴링 루프로 CPU를 100% 태우는 대신, 인터럽트나 이벤트가 들어올 때까지 저전력 상태로 기다린다. 우리는 인터럽트를 안 켜 뒀으니 영원히 잠든다.

이 `kernel.c`의 모든 줄을 다시 보면 한 가지 흥미로운 사실이 보인다. **표준 함수 호출이 단 한 줄도 없다.** `printf`도, `puts`도, `write`도, 심지어 `memset`도 안 부른다. `#include <stdint.h>`는 타입 정의만 끌어오고, 함수는 가져오지 않는다. 이 코드는 진짜로 외부에 어떤 의존도 없다 — 11장에서 `nm`으로 확인했던 그 모양 그대로다.

## `linker.ld` — 메모리 배치의 약속

`boot.S`가 `stack_top`과 `__bss_start`/`__bss_end`라는 심볼을 끌어다 썼다. 그 심볼들이 어디서 왔는지가 링커 스크립트의 일이다.

```ld
ENTRY(_start)

SECTIONS
{
    . = 0x40080000;

    .text : ALIGN(8) {
        KEEP(*(.text.boot))
        *(.text*)
    }

    .rodata : ALIGN(8) { *(.rodata*) }
    .data   : ALIGN(8) { *(.data*) }

    .bss (NOLOAD) : ALIGN(16) {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(16);
        __bss_end = .;
    }

    . = ALIGN(16);
    . = . + 0x10000;
    stack_top = .;

    /DISCARD/ : { *(.note.* .comment .eh_frame*) }
}
```

링커 스크립트는 처음 보면 외계어처럼 보이지만, 의미는 단순하다 — **"어떤 섹션을 메모리 어디에 둘지"** 정하는 글이다.

한 줄씩 큰 그림만 짚자.

- **`ENTRY(_start)`** — ELF의 진입점 심볼. `qemu-system-aarch64 -kernel`이 ELF를 적재한 뒤 이 주소로 점프한다.
- **`. = 0x40080000;`** — 현재 위치 카운터를 0x40080000으로 설정. 이 자리부터 섹션을 쌓는다. virt 보드의 RAM은 0x40000000부터 시작하니, 0x80000(512KB) 떨어진 자리에 우리 커널을 둔다.
- **`.text : ... { KEEP(*(.text.boot)) *(.text*) }`** — 코드 섹션. **`.text.boot`을 맨 앞에** 두는 게 핵심. `boot.S`가 `.section .text.boot`으로 선언했던 그 섹션이다. `KEEP`은 링커가 "참조 없다"고 잘라내지 않게 막는다.
- **`.bss (NOLOAD) : ...`** — `.bss` 섹션. `NOLOAD` 표시는 "ELF 파일에 자리만 잡고 데이터는 들고 가지 않는다"는 뜻. 데이터는 어차피 0이니까. `__bss_start`와 `__bss_end` 심볼이 여기서 정의된다.
- **`. = . + 0x10000; stack_top = .;`** — 64KB 더 가서 그 끝을 `stack_top`으로 잡는다. 이게 `boot.S`가 `sp`에 박는 그 주소다.
- **`/DISCARD/`** — 우리가 안 쓰는 섹션(주석, 디버그 노트, exception unwind 정보)을 버린다.

링커 스크립트의 진짜 깊은 의미 — VMA vs LMA, `ALIGN`이 왜 8과 16이고 4가 아닌지, `KEEP`이 없으면 정확히 어떤 일이 벌어지는지 — 는 13장에서 한 줄씩 다시 본다. 12장에서는 "이 한 장이 메모리 지도를 정한다"는 큰 그림만 손에 잡아 두자.

## `Makefile` — 툴체인을 찾아 연결한다

마지막 조각은 빌드 파이프라인이다. 코드를 적었으니 그것을 ELF로 묶어 QEMU에 넣어야 한다.

여기서 손에 익은 호스트 빌드와 다른 점이 하나 있다. **베어메탈 빌드는 크로스 컴파일러가 필요하다.** Apple Clang으로는 macOS용 Mach-O 바이너리가 나오는데, QEMU virt 보드가 원하는 건 ELF다. 두 길 중 하나를 고른다.

| 길 | 도구 | 설치 |
|----|------|------|
| A | `aarch64-elf-gcc` + `aarch64-elf-ld` | `brew install aarch64-elf-gcc` |
| B | `clang --target=aarch64-none-elf` + `ld.lld` | `brew install lld` (Apple Clang은 이미 있음) |

길 A는 정통 베어메탈 GCC. 인터넷의 베어메탈 튜토리얼 99%가 이 길이라 다른 자료를 따라 읽기 쉽다. 길 B는 Apple Clang에 lld 하나만 더 깔면 되는 가벼운 경로. 둘 다 잘 동작한다.

책의 예제 Makefile은 둘을 자동으로 감지한다.

```make
AARCH64_GCC := $(shell command -v aarch64-elf-gcc 2>/dev/null)
LLD         := $(shell command -v ld.lld 2>/dev/null)

ifneq ($(AARCH64_GCC),)
  CC      = aarch64-elf-gcc
  LD      = aarch64-elf-ld
  CFLAGS  = -ffreestanding -nostdlib -nostartfiles \
            -mgeneral-regs-only -mcpu=cortex-a72 -O2 -g -Wall -Wextra
  LDFLAGS = -T linker.ld -nostdlib
else ifneq ($(LLD),)
  CC      = clang
  LD      = ld.lld
  CFLAGS  = --target=aarch64-none-elf -ffreestanding -nostdlib \
            -mgeneral-regs-only -mcpu=cortex-a72 -O2 -g -Wall -Wextra
  LDFLAGS = -T linker.ld
else
  $(error 툴체인이 없다. brew install aarch64-elf-gcc 또는 brew install lld 중 하나가 필요하다.)
endif
```

이 분기 덕에 `make` 한 줄이면 환경에 맞춰 알아서 돈다. 여기서 컴파일 플래그가 11장에서 정리한 그대로라는 점을 보자 — `-ffreestanding -nostdlib -mgeneral-regs-only -mcpu=cortex-a72`. 11장의 표가 여기서 한 줄씩 일한다.

빌드 규칙은 익숙한 모양.

```make
OBJ = boot.o kernel.o
ELF = kernel.elf

$(ELF): $(OBJ) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJ)

boot.o: boot.S
	$(CC) $(CFLAGS) -c $< -o $@

kernel.o: kernel.c
	$(CC) $(CFLAGS) -c $< -o $@
```

세 단계 — (1) `boot.S` → `boot.o`, (2) `kernel.c` → `kernel.o`, (3) 두 오브젝트 + 링커 스크립트 → `kernel.elf`. 8장에서 정리한 그 컴파일 사이클이 그대로 적용된다.

실행 타깃은 QEMU 호출 한 줄.

```make
run: $(ELF)
	$(QEMU) -M virt -cpu cortex-a72 -nographic -kernel $(ELF)
```

각 옵션의 의미.

- **`-M virt`** — virt 보드 모델. 가상의 ARM 머신으로, 실제 SoC의 복잡함이 없어 학습에 가장 편하다.
- **`-cpu cortex-a72`** — 라즈베리파이 4가 쓰는 CPU. 다음 장(13)과 그 다음 장(14)에서 같은 CPU로 일관성을 가져간다.
- **`-nographic`** — 그래픽 창 없이 호스트 터미널을 그대로 시리얼로 쓴다. 우리가 `printf` 대신 UART에 쓰는 글자가 이 터미널에 직접 나타난다.
- **`-kernel kernel.elf`** — ELF를 적재할 자리에 적재하고 진입점으로 점프하라는 지시.

## 그 한 순간 — `make run`

이제 모든 조각이 모였다. `example/ch12-aarch64-hello/` 디렉토리에서 다음을 친다.

```
$ make
clang --target=aarch64-none-elf -ffreestanding -nostdlib -mgeneral-regs-only -mcpu=cortex-a72 -O2 -g -Wall -Wextra -c boot.S -o boot.o
clang --target=aarch64-none-elf -ffreestanding -nostdlib -mgeneral-regs-only -mcpu=cortex-a72 -O2 -g -Wall -Wextra -c kernel.c -o kernel.o
ld.lld -T linker.ld -o kernel.elf boot.o kernel.o
툴체인: clang (clang + ld.lld)

$ make run
QEMU 시작 — 종료는 Ctrl+A 누른 뒤 x
hello, aarch64
```

**여기서 한 번 멈추자.** 화면에 글자가 떴는가? 다음 줄은 빠르게 넘어가지 말고 그 순간을 좀 곱씹는 게 좋다.

자바 시절을 떠올려 보자. `public static void main(String[] args)` 안의 `System.out.println("Hello")`. 그 한 줄을 처음 돌렸을 때의 작은 기쁨이 있었다. 그게 입문의 풍경이었다. 같은 인사말이 이번엔 다르게 도착했다. JVM이 없다. OS가 없다. 표준 라이브러리가 없다. 우리가 짠 어셈블리 50줄과 C 30줄과 링커 스크립트 한 장이, 호스트 OS 위가 아니라 **ARM CPU 위에서 직접** 돌면서 글자를 만들었다.

이 한 줄이 통과하면, 정직하게 말해 이 책의 7할이 완성된다. 남은 3할은 한 줄씩 해부(13장), 진짜 보드 옮기기(14장), 다음 걸음 가리키기(15장)다. 정점은 여기에 있다.

## 무엇이 동작하지 않을 때

축하 한 줄을 적었으니, 솔직하게 짚어야 할 것도 적자. **이 빌드는 의외의 자리에서 깨질 수 있다.** 흔한 함정을 미리 봐 두면 안심이 된다.

### 빌드는 통과했는데 글자가 안 나온다

가장 빈번한 함정. 다음 셋 중 하나일 가능성이 높다.

1. **`volatile`을 빼먹었다.** 컴파일러가 UART 쓰기를 최적화로 날려 버렸다. `kernel.c`의 `uart_dr` 선언에 `volatile`이 있는지 다시 본다.
2. **로드 주소가 어긋났다.** `linker.ld`의 `. = 0x40080000;`이 빠지거나 잘못된 주소라 ELF가 QEMU의 기대 위치에 떨어지지 않는다. virt 보드의 RAM은 0x40000000부터고, `-kernel` 옵션의 기본 로드 주소가 0x40080000이다.
3. **`-nographic`을 안 줬다.** QEMU가 그래픽 창을 띄우려고 하는데 그쪽엔 시리얼이 안 나간다. 다른 콘솔 옵션이 필요하다.

### `make run`이 멈춰 있고 종료가 안 된다

이건 함정이 아니라 의도된 동작이다. `kernel_main`이 무한 루프(`wfe`)에 들어 있으니, QEMU는 그대로 동작 중이다. 종료는 **Ctrl+A 한 번, x 한 번.** `Ctrl+C`로 끄려고 하면 안 된다 — `-nographic`에서 Ctrl+C는 게스트(우리 커널)에게 인터럽트로 전달되니까. 외워 두자 — **종료는 Ctrl+A x.**

QEMU 단축키 도움말은 `Ctrl+A h`로 볼 수 있다. 한 번쯤 봐 두면 다른 단축키도 손에 익는다.

### 글자가 깨져 보인다

`uart_puts` 안의 `if (*s == '\n') uart_putc('\r');`이 빠지면 줄바꿈이 어긋난다. `hello, aarch64` 뒤에 새 줄이 시작되지 않고 사선으로 흘러내린다. 이 한 줄은 시리얼 터미널의 관행과 우리 C 문자열 사이의 다리다.

### `aarch64-elf-gcc not found`

`brew install aarch64-elf-gcc`를 안 깔았는데 Makefile이 GCC 경로를 골랐을 때. 두 길 중 하나 — (A) `brew install aarch64-elf-gcc`, (B) `brew install lld`. 책의 README가 두 길을 다 설명한다.

### `error: invalid linker name in argument '-fuse-ld=lld'`

Apple Clang 안에는 lld가 같이 들어 있지 않다. Homebrew의 lld를 따로 깔면(`brew install lld`) Makefile이 `ld.lld`를 PATH에서 찾아 자동으로 쓴다.

이 함정들의 공통점이 있다 — **하나같이 검증 가능하다.** "어쩌면 동작하지 않을 수도 있는" 모호한 영역이 아니라, 한 줄을 고치면 한 줄이 통과한다. 베어메탈의 매력 중 하나는 이런 직선성이다.

## 디버깅의 다리

마지막으로 한 가지 도구를 가리키고 가자. `make debug`를 돌리면 QEMU가 `-s -S` 옵션과 함께 떠서 **gdb 호환 디버그 포트(1234)에서 대기**한다.

```
$ make debug
QEMU를 -s -S로 띄운다. 다른 터미널에서 다음 중 하나로 붙는다.
  lldb -o 'gdb-remote localhost:1234' kernel.elf
  aarch64-elf-gdb kernel.elf -ex 'target remote :1234'
```

다른 터미널에서 lldb로 붙으면 — 우리 `kernel.elf`의 심볼 정보를 들고 — 베어메탈 코드에 breakpoint를 걸 수 있다.

```
(lldb) b kernel_main
Breakpoint 1: where = kernel.elf`kernel_main + 0 at kernel.c:34
(lldb) c
Process 1 stopped
* thread #1, stop reason = breakpoint 1.1
    frame #0: 0x000000004008003c kernel.elf`kernel_main at kernel.c:34
(lldb) s
(lldb) p *uart_dr = 'H'
```

`p` 한 줄로 UART 데이터 레지스터에 글자를 직접 쓸 수 있다. **우리 코드를 한 단계도 안 돌려 놓고도 글자가 화면에 찍힌다.** 그게 베어메탈 디버깅의 묘한 즐거움 중 하나다. 하드웨어가 거기 있고, 우리는 그 위에서 한 명령씩 움직인다.

13장에서는 이 디버거를 더 본격적으로 쓴다. `boot.S`의 한 줄에 breakpoint를 걸고, 그 줄 직후의 레지스터를 들여다보면서 "왜 이 줄이 거기에 있는지"를 손에 잡는다.

## 마무리

이 장의 끝에서 우리가 손에 든 것이 무엇인지 정리하자.

- **`kernel.elf` 한 파일.** 80여 줄의 어셈블리·C·링커 스크립트가 만든 ELF.
- **`make run` 한 줄.** QEMU에 그 ELF를 올리는 명령.
- **시리얼 라인의 첫 글자.** OS 없이 ARM CPU 위에서 직접 도는 코드가 만든 출력.

이 셋이 함께 있다는 사실이 책 절반의 무게를 갖는다.

기억해 두자.

- **네 파일은 분업이다.** `boot.S`는 무대 준비, `kernel.c`는 본 공연, `linker.ld`는 좌석 배치, `Makefile`은 입장권 발급. 네 파일이 하나의 ELF로 모인다.
- **`.text.boot`은 맨 앞에.** 링커 스크립트가 이 약속을 지키지 않으면 CPU가 점프할 자리에 우리 진입점이 없다.
- **`volatile`은 MMIO의 생명선이다.** 잊으면 글자가 사라진다.
- **`Ctrl+A x`가 종료다.** `Ctrl+C`는 게스트로 들어간다. 외워 두자.
- **첫 글자가 찍히는 순간, 책의 7할이 완성된다.** 나머지는 그 그림을 깊게 파고 진짜 보드로 옮기는 일이다.

다음 장에서는 같은 네 파일을 다시 본다. 이번엔 한 줄씩, 한 명령씩. `mrs x0, mpidr_el1`의 `mrs`가 정확히 무엇이고, 왜 `cbnz`가 `cmp + bne` 두 줄을 한 줄로 줄였는지, 링커 스크립트의 `KEEP`이 없으면 어떤 일이 벌어지는지. 12장이 동작이라면 13장은 이유다.
