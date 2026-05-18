/*
 * Stage 3 — Ch12와 동등한 완성형 부트 코드.
 *
 * Stage 2와의 차이는 단 한 줄: `bl kernel_main`.
 * 어셈블리에서 C로 처음 넘어가는 그 한 줄이 곧 부팅의 정점이다.
 */
.section ".text.boot"
.globl _start
_start:
    mrs   x0, mpidr_el1
    and   x0, x0, #3
    cbnz  x0, halt

    ldr   x1, =stack_top
    mov   sp, x1

    ldr   x1, =__bss_start
    ldr   x2, =__bss_end
clear_bss:
    cmp   x1, x2
    b.ge  bss_done
    str   xzr, [x1], #8
    b     clear_bss
bss_done:
    bl    kernel_main       // ★ Stage 3의 결정적 한 줄

halt:
    wfe
    b     halt
