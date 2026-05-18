/* Stage 2 — BSS 경계 심볼과 스택 영역을 명시적으로 정의한다.
 *
 * __bss_start, __bss_end : boot.S의 BSS 클리어 루프가 참조하는 심볼.
 * stack_top              : SP 레지스터에 박을 스택 꼭대기 주소.
 */
ENTRY(_start)

SECTIONS
{
    . = 0x40000000;

    .text : { KEEP(*(.text.boot)) *(.text*) }
    .rodata : { *(.rodata*) }
    .data   : { *(.data*) }

    . = ALIGN(8);
    __bss_start = .;
    .bss : { *(.bss*) *(COMMON) }
    . = ALIGN(8);
    __bss_end = .;

    /* 스택 영역 — 16KB */
    . = ALIGN(16);
    . += 0x4000;
    stack_top = .;
}
