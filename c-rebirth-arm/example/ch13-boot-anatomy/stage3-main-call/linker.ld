/* Stage 3 — Stage 2와 동일. 변경 없음. */
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

    . = ALIGN(16);
    . += 0x4000;
    stack_top = .;
}
