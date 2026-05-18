/*
 * Raspberry Pi 4 PL011 UART(UART0)에 "hello, raspi4!" 출력.
 *
 * config.txt의 `dtoverlay=disable-bt`가 PL011을 외부 GPIO 14/15번 핀으로
 * 라우팅해준 상태를 가정한다. 우리 코드는 GPIO 핀을 Alt0(PL011 TX/RX)으로
 * 설정하고, PL011 자체를 115200 8N1로 초기화한 뒤 한 글자씩 송신한다.
 *
 * 시리얼 콘솔 연결: USB-시리얼 어댑터의 GND를 보드 6번 핀(GND),
 *                  어댑터 RX를 보드 8번 핀(GPIO14, TX),
 *                  어댑터 TX를 보드 10번 핀(GPIO15, RX)에 연결.
 *                  PC에서 115200 8N1로 시리얼 콘솔을 연다.
 */
#include <stdint.h>

/* BCM2711 MMIO 베이스 (low peripheral mode 기본값) */
#define MMIO_BASE   0xFE000000UL

/* GPIO 레지스터들 */
#define GPFSEL1     (*(volatile uint32_t*)(MMIO_BASE + 0x200004))
#define GPPUD       (*(volatile uint32_t*)(MMIO_BASE + 0x200094))
#define GPPUDCLK0   (*(volatile uint32_t*)(MMIO_BASE + 0x200098))

/* PL011 UART (UART0) 레지스터들 */
#define UART0_DR    (*(volatile uint32_t*)(MMIO_BASE + 0x201000))
#define UART0_FR    (*(volatile uint32_t*)(MMIO_BASE + 0x201018))
#define UART0_IBRD  (*(volatile uint32_t*)(MMIO_BASE + 0x201024))
#define UART0_FBRD  (*(volatile uint32_t*)(MMIO_BASE + 0x201028))
#define UART0_LCRH  (*(volatile uint32_t*)(MMIO_BASE + 0x20102C))
#define UART0_CR    (*(volatile uint32_t*)(MMIO_BASE + 0x201030))
#define UART0_ICR   (*(volatile uint32_t*)(MMIO_BASE + 0x201044))

#define UART_FR_TXFF (1u << 5)   /* TX FIFO full */

static void delay(int count) {
    while (count--) __asm__ volatile ("nop");
}

static void uart_init(void) {
    /* 1) UART 일단 끄기 */
    UART0_CR = 0;

    /* 2) GPIO 14, 15번 핀을 Alt0(PL011 TX/RX)으로 설정.
     *    GPFSEL1은 GPIO 10~19를 담당, 각 핀 3비트.
     *    14번 핀: 비트 12~14, 15번 핀: 비트 15~17.
     *    Alt0 = 0b100. */
    uint32_t sel = GPFSEL1;
    sel &= ~((7u << 12) | (7u << 15));
    sel |=  ((4u << 12) | (4u << 15));
    GPFSEL1 = sel;

    /* 3) 풀업/풀다운 비활성화 (시리얼 핀에는 내장 풀업 불필요) */
    GPPUD = 0;
    delay(150);
    GPPUDCLK0 = (1u << 14) | (1u << 15);
    delay(150);
    GPPUDCLK0 = 0;

    /* 4) 이전 인터럽트 클리어 */
    UART0_ICR = 0x7FF;

    /* 5) 보레이트 — config.txt의 enable_uart=1이 UART 클럭을 48MHz로 고정.
     *    48,000,000 / (16 * 115200) = 26.04
     *    IBRD = 26, FBRD = 0.04 * 64 ≈ 3 */
    UART0_IBRD = 26;
    UART0_FBRD = 3;

    /* 6) 라인 제어: 8비트 데이터, FIFO 활성화 */
    UART0_LCRH = (3u << 5) | (1u << 4);

    /* 7) UART 본체 + TX + RX 활성화 */
    UART0_CR = (1u << 0) | (1u << 8) | (1u << 9);
}

static void uart_putc(char c) {
    while (UART0_FR & UART_FR_TXFF) { }
    UART0_DR = (uint32_t)c;
}

static void uart_puts(const char *s) {
    while (*s) {
        if (*s == '\n') uart_putc('\r');
        uart_putc(*s++);
    }
}

void kernel_main(void) {
    uart_init();
    uart_puts("hello, raspi4!\n");
    uart_puts("two parts down — boot.S and kernel.c both alive.\n");
    for (;;) {
        /* 영원히 산다 — 다음 장에서 인터럽트와 함께 깨운다. */
    }
}
