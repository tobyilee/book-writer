/* Raspberry Pi 4 (AArch64) 베어메탈용 링커 스크립트.
 *
 * 핵심은 시작 주소 0x80000 — GPU 펌웨어가 kernel8.img를 이 주소에 적재 후
 * 점프한다. (32비트 모드는 0x8000이지만 64비트는 0x80000.)
 */
ENTRY(_start)

SECTIONS
{
    . = 0x80000;

    .text : { KEEP(*(.text.boot)) *(.text*) }
    .rodata : { *(.rodata*) }
    .data   : { *(.data*) }

    . = ALIGN(8);
    __bss_start = .;
    .bss : { *(.bss*) *(COMMON) }
    . = ALIGN(8);
    __bss_end = .;

    /* 16KB 스택 */
    . = ALIGN(16);
    . += 0x4000;
    stack_top = .;
}
