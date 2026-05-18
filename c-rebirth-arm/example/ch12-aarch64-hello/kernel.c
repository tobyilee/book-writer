/* kernel.c — QEMU virt 보드의 PL011 UART에 글자를 보낸다.
 *
 * "OS 위에서 도는 프로그램"이 아니라 "CPU 위에서 직접 도는 프로그램"이라는
 * 사실이 이 작은 함수 몇 개에 모두 들어 있다. printf 한 줄이 없다 —
 * 한 글자를 보내려면 UART 데이터 레지스터에 직접 쓴다.
 */
#include <stdint.h>

/* QEMU `-M virt`의 PL011 UART0 베이스 주소.
 * OSDev wiki "QEMU AArch64 Virt Bare Bones" 페이지에서 확인 가능. */
#define UART0_BASE   0x09000000UL
#define UART0_DR     (UART0_BASE + 0x000)   /* Data Register */
#define UART0_FR     (UART0_BASE + 0x018)   /* Flag Register */
#define UART_FR_TXFF (1u << 5)              /* Transmit FIFO Full */

/* volatile이 빠지면 컴파일러가 "같은 주소에 같은 값을 두 번 쓸 이유가
 * 없다"고 판단해 일부 출력을 제거할 수 있다. 베어메탈의 흔한 함정. */
static volatile uint32_t *const uart_dr =
    (volatile uint32_t *)UART0_DR;
static volatile uint32_t *const uart_fr =
    (volatile uint32_t *)UART0_FR;

static void uart_putc(char c)
{
    /* TX FIFO가 가득 차 있으면 빌 때까지 대기 */
    while (*uart_fr & UART_FR_TXFF) { /* spin */ }
    *uart_dr = (uint32_t)(unsigned char)c;
}

static void uart_puts(const char *s)
{
    while (*s) {
        if (*s == '\n') uart_putc('\r');
        uart_putc(*s++);
    }
}

/* boot.S가 .bss를 클리어한 뒤 sp를 잡고 여기로 점프한다.
 * 이 시점에 우리가 가진 건 (a) 스택, (b) UART 주소, (c) 우리 코드. 그뿐이다. */
void kernel_main(void)
{
    uart_puts("hello, aarch64\n");

    /* 정점에 도달했으니, 영원히 여기에 머무른다.
     * 종료는 사용자가 Ctrl+A x 로 QEMU를 직접 죽인다. */
    for (;;) {
        __asm__ volatile ("wfe");
    }
}
