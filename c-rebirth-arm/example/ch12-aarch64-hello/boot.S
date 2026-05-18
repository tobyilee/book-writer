/* boot.S — AArch64 베어메탈 진입점
 *
 * QEMU virt 보드(-M virt -cpu cortex-a72)가 .text.boot 섹션을
 * 로드 주소(linker.ld의 0x40080000)에 적재하고 _start로 점프한다.
 *
 * 진입 직후 CPU 상태:
 *   - Exception Level은 보통 EL2 (이번 데모에서는 EL1으로 강등하지 않고 그대로 둔다)
 *   - MMU와 캐시는 비활성
 *   - 모든 일반 레지스터는 미정의
 *   - 4개 코어가 동시에 진입한다 — primary core 하나만 통과시킨다
 *
 * 이 파일은 큰 그림이 목적이라 명령 줄별 해부는 Ch13에 미룬다.
 */

    .section .text.boot, "ax"
    .globl _start
_start:
    /* (1) primary core(코어 0) 골라내기.
     *     mpidr_el1의 하위 두 비트가 코어 번호. 0이 아니면 정지. */
    mrs     x0, mpidr_el1
    and     x0, x0, #3
    cbnz    x0, halt

    /* (2) 스택 포인터 설정.
     *     linker.ld가 .bss 끝에 stack_top 심볼을 둔다. */
    ldr     x0, =stack_top
    mov     sp, x0

    /* (3) .bss를 0으로 클리어.
     *     C 표준은 정적/전역 변수의 초깃값을 0으로 약속한다.
     *     호스트 OS가 없으니 그 약속도 우리가 직접 지킨다. */
    ldr     x0, =__bss_start
    ldr     x1, =__bss_end
1:  cmp     x0, x1
    b.ge    2f
    str     xzr, [x0], #8
    b       1b
2:

    /* (4) C 코드로 점프 — 돌아오지 않는다고 가정 */
    bl      kernel_main

    /* (5) 만에 하나 kernel_main이 리턴해도 안전한 정지 */
halt:
    wfe
    b       halt
