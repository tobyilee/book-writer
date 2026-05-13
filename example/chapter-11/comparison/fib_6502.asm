; CPU:      MOS Technology 6502 (MOS/ca65 syntax)
; What:     Compute first 10 Fibonacci numbers, write to memory-mapped output $D012
; Assembler: ca65 fib_6502.asm -o fib.o && ld65 -t none fib.o -o fib.bin
; Reference: MOS 6500 Microprocessor Family Programming Manual (1976)
; Note:     6502 has only A, X, Y registers — zero-page ($00-$FF) acts as fast RAM.
;           No IN/OUT instructions: I/O is memory-mapped (STA to a device address).

        .org    $0600

        ; Initialise prev = 0, curr = 1  (stored in zero page)
        LDA     #$00
        STA     $80             ; zero-page $80 = prev  (acts like an extra register)
        LDA     #$01
        STA     $81             ; zero-page $81 = curr

        ; Output F(0) and F(1) via memory-mapped I/O
        LDA     $80
        STA     $D012           ; writing to $D012 → output device (system-dependent)
        LDA     $81
        STA     $D012

        ; Compute and output F(2)..F(9)  — 8 more terms
        LDX     #$08            ; X ← loop counter

LOOP:
        LDA     $80             ; A ← prev
        CLC                     ; must clear carry before ADC (no bare ADD on 6502)
        ADC     $81             ; A ← prev + curr  (ADC = add with carry)
        STA     $82             ; zero-page $82 = next (temp)
        STA     $D012           ; output next

        LDA     $81             ; shift: prev ← curr
        STA     $80
        LDA     $82             ; shift: curr ← next
        STA     $81

        DEX                     ; X ← X - 1
        BNE     LOOP            ; if X != 0, repeat

        BRK                     ; software break / stop

; ------------------------------------------------------------
; Zero-page map (acts as extra registers):
;   $80 = prev Fibonacci value
;   $81 = current Fibonacci value
;   $82 = next Fibonacci value (temporary)
;
; Register map:
;   A  = scratch / computation
;   X  = loop counter
;   Y  = unused here
;
; Key differences vs 8080 / SAP-2:
;   - Only 3 registers (A, X, Y)  — zero page fills the gap
;   - No IN/OUT opcodes: all I/O is plain memory read/write
;   - ADC always adds carry; CLC must precede every simple addition
;   - DEX + BNE replaces DCR + JNZ (same concept, different register)
;   - 6502 code is slightly longer because variable shuffles hit memory each time
;   - Addressing: 13 modes, but zero-page accesses need only 1-byte address
; ------------------------------------------------------------
