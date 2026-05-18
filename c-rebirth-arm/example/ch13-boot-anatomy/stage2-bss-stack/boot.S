/*
 * Stage 2 — BSS 클리어와 스택 포인터 셋업까지.
 *
 * Stage 1과의 차이는 두 가지다.
 *   (1) .bss 영역을 0으로 채운다 (호스트 OS의 ELF 로더가 없으므로 직접).
 *   (2) SP 레지스터에 stack_top 주소를 박는다 — C 함수 호출의 발판.
 *
 * 그러나 아직 kernel.c가 없으므로 결국 halt로 잠든다.
 * 다음 Stage 3에서 `bl kernel_main`이 추가된다.
 */
.section ".text.boot"
.globl _start
_start:
    mrs   x0, mpidr_el1     // 1) 현재 CPU ID 읽기
    and   x0, x0, #3        // 2) 하위 2비트만 (4코어 기준)
    cbnz  x0, halt          // 3) primary core(0)가 아니면 정지

    // 4) 스택 포인터 셋업 — 링커 스크립트의 stack_top 심볼 사용
    ldr   x1, =stack_top
    mov   sp, x1

    // 5) .bss 영역 0으로 클리어
    ldr   x1, =__bss_start
    ldr   x2, =__bss_end
clear_bss:
    cmp   x1, x2
    b.ge  bss_done
    str   xzr, [x1], #8     // *x1 = 0; x1 += 8;
    b     clear_bss
bss_done:
    // 6) C 함수 호출 준비가 끝났지만 아직 호출할 함수가 없음
    //    Stage 3에서 여기에 `bl kernel_main`이 들어간다.

halt:
    wfe
    b     halt
