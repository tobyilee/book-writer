/*
 * Stage 3 — QEMU virt 보드의 PL011 UART에 "hello, aarch64\n"을 찍는다.
 *
 * Ch12의 kernel.c와 완전히 동일하다. 13장의 목적은 boot.S의 한 줄씩
 * 해부였으므로 kernel.c는 일부러 손대지 않았다.
 */
#include <stdint.h>

#define UART0_BASE 0x09000000UL          /* QEMU virt PL011 UART */
static volatile uint32_t *uart_dr = (uint32_t*)UART0_BASE;

static void uart_putc(char c) {
    *uart_dr = (uint32_t)c;
}

static void uart_puts(const char *s) {
    while (*s) uart_putc(*s++);
}

void kernel_main(void) {
    uart_puts("hello, aarch64\n");
    uart_puts("stage 3 — bl kernel_main passed\n");
    for (;;) { /* 무한 루프 */ }
}
