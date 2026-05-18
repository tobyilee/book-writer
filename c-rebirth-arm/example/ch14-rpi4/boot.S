/*
 * Raspberry Pi 4 모델 B (BCM2711, Cortex-A72 x4) AArch64 베어메탈 진입점.
 *
 * GPU 펌웨어가 kernel8.img를 0x80000에 적재 후 ARM 코어 4개 모두를
 * 깨워서 그 주소로 점프시킨다. primary core(0번)만 통과시키고 나머지
 * 셋은 잠재운다.
 */
.section ".text.boot"
.globl _start
_start:
    mrs   x0, mpidr_el1     // CPU ID 읽기
    and   x0, x0, #3        // 4코어 → 하위 2비트
    cbnz  x0, halt          // primary가 아니면 정지

    // 스택 포인터 셋업 (16KB 스택, 링커 스크립트가 stack_top을 정의)
    ldr   x1, =stack_top
    mov   sp, x1

    // .bss 0으로 클리어
    ldr   x1, =__bss_start
    ldr   x2, =__bss_end
clear_bss:
    cmp   x1, x2
    b.ge  bss_done
    str   xzr, [x1], #8
    b     clear_bss
bss_done:

    bl    kernel_main       // C로 진입

halt:
    wfe
    b     halt
