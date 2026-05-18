/* linker.ld — AArch64 virt 보드용 최소 링커 스크립트.
 *
 * QEMU `-M virt -kernel <ELF>`는 ELF의 program header가 지정한 주소에
 * 섹션들을 적재하고, ENTRY가 가리키는 심볼로 점프한다.
 *
 * 로드 주소 0x40080000은 virt 보드의 RAM 시작(0x40000000)에서 0x80000만큼
 * 떨어진 자리 — 라즈베리파이 관행과 같은 위치라 학습용으로 익숙하다.
 */

ENTRY(_start)

SECTIONS
{
    . = 0x40080000;

    /* (1) 부팅 코드는 반드시 맨 앞에.
     *     KEEP는 링커가 "참조 없다"고 잘라내지 않도록 막는다. */
    .text : ALIGN(8) {
        KEEP(*(.text.boot))
        *(.text*)
    }

    .rodata : ALIGN(8) { *(.rodata*) }
    .data   : ALIGN(8) { *(.data*) }

    /* (2) .bss는 ELF에 자리만 잡고 데이터는 들고 가지 않는다.
     *     boot.S가 시작 직후 0으로 클리어한다. */
    .bss (NOLOAD) : ALIGN(16) {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(16);
        __bss_end = .;
    }

    /* (3) 스택은 .bss 뒤에 64KB 잡아둔다. */
    . = ALIGN(16);
    . = . + 0x10000;
    stack_top = .;

    /DISCARD/ : { *(.note.* .comment .eh_frame*) }
}
