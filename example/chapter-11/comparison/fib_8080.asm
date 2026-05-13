; CPU:      Intel 8080 (Intel syntax)
; What:     Compute first 10 Fibonacci numbers, output to port 1
; Assembler: as80 fib_8080.asm -o fib.bin
; Reference: Intel MCS-80 Assembly Language Programming Manual (1975)
; Note:     Our SAP-2 ISA is a subset of 8080 — most mnemonics match directly.

        ORG     0100h           ; CP/M convention: start at 0x100

        ; Initialise prev = 0, curr = 1
        MVI     B, 0            ; B ← 0 (prev)
        MVI     C, 1            ; C ← 1 (curr)

        ; Output F(0) and F(1)
        MOV     A, B
        OUT     1               ; port 1 ← F(0) = 0
        MOV     A, C
        OUT     1               ; port 1 ← F(1) = 1

        ; Compute and output F(2)..F(9)  — 8 more terms
        MVI     D, 8            ; D ← loop counter

LOOP:
        MOV     A, B
        ADD     C               ; A ← prev + curr  (= next)
        OUT     1               ; port 1 ← next
        MOV     B, C            ; prev ← curr
        MOV     C, A            ; curr ← next
        DCR     D               ; D ← D - 1        (dedicated decrement)
        JNZ     LOOP            ; if D != 0, repeat

        HLT                     ; stop

; ------------------------------------------------------------
; Register map:
;   B  = prev Fibonacci value
;   C  = current Fibonacci value
;   A  = scratch / next value
;   D  = loop counter (8 iterations → total 10 outputs)
;
; Key differences vs our SAP-2:
;   - DCR is a dedicated 1-byte decrement instruction (SAP-2 uses SUB)
;   - OUT n uses a port number directly in the opcode
;   - 7 general-purpose 8-bit registers (vs SAP-2's 3: A, B, C)
;   - All core mnemonics (MVI, MOV, ADD, OUT, JNZ, HLT) are identical
; ------------------------------------------------------------
