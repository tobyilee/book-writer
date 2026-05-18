/* Stage 1 — 가장 단순한 링커 스크립트.
 * .text.boot이 맨 앞에 와야 한다는 약속만 박아둔다.
 */
ENTRY(_start)

SECTIONS
{
    . = 0x40000000;                /* QEMU virt 머신의 RAM 시작 주소 */
    .text : { KEEP(*(.text.boot)) *(.text*) }
    .rodata : { *(.rodata*) }
    .data   : { *(.data*) }
    .bss    : { *(.bss*) *(COMMON) }
}
