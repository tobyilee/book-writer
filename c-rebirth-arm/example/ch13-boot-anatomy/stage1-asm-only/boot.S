/*
 * Stage 1 — 어셈블리만으로 짜인 가장 단순한 진입점.
 *
 * 이 단계는 (1) primary core(0번)만 통과시키고 (2) 나머지 코어와
 * primary 자신도 결국 `wfe`/`b halt`로 영원히 잠재운다. C 함수 호출도,
 * 스택도, BSS 클리어도 없다.
 *
 * 빌드 후 `aarch64-elf-objdump -d kernel.elf`로 진입점을 확인하고,
 * `aarch64-elf-readelf -h kernel.elf`로 Entry point address가
 * 0x40000000인지 본다.
 */
.section ".text.boot"
.globl _start
_start:
    mrs   x0, mpidr_el1     // 현재 CPU ID 읽기
    and   x0, x0, #3        // 하위 2비트만 남기기 (4코어 기준)
    cbnz  x0, halt          // 0번이 아니면 멈춰라
    // primary core는 곧장 halt로 진입한다 — Stage 1은 여기까지가 끝
halt:
    wfe                     // Wait For Event
    b     halt
