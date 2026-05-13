; CPU:      Intel 8086 / 8088 (Intel / NASM syntax)
; What:     Compute first 10 Fibonacci numbers, output to port 1
; Assembler: nasm -f bin fib_8086.asm -o fib.com
; Reference: Intel iAPX 86/88 User's Manual (1981)
; Note:     8086 extends 8080 to 16-bit. AX = AH:AL; we use 8-bit sub-registers.
;           LOOP auto-decrements CX — equivalent to Z80's DJNZ but for CX.

        ORG     0100h           ; DOS .COM convention (same origin as 8080 / Z80)

        ; Initialise prev = 0, curr = 1  (8-bit, stored in BL and CL)
        MOV     BL, 0           ; BL ← 0 (prev)    [8080: MVI B, 0]
        MOV     CL, 1           ; CL ← 1 (curr)    [8080: MVI C, 1]

        ; Output F(0) and F(1)
        MOV     AL, BL
        OUT     1, AL           ; port 1 ← F(0)    [8080: OUT 1]
        MOV     AL, CL
        OUT     1, AL           ; port 1 ← F(1)

        ; Compute and output F(2)..F(9)  — 8 more terms
        MOV     CX, 8           ; CX ← 8  (LOOP uses CX as its implicit counter)

LOOP_FIB:
        MOV     AL, BL
        ADD     AL, CL          ; AL ← prev + curr  (8-bit arithmetic)
        OUT     1, AL           ; port 1 ← next
        MOV     BL, CL          ; prev ← curr
        MOV     CL, AL          ; curr ← next
        LOOP    LOOP_FIB        ; CX-- ; if CX != 0, jump  *** 8086 unique ***

        INT     20h             ; DOS: terminate program (replaces HLT in .COM files)

; ------------------------------------------------------------
; Register map:
;   BL = prev Fibonacci value (lower byte of BX)
;   CL = current Fibonacci value (lower byte of CX used for data AND as LOOP counter)
;   AL = scratch / next value (lower byte of AX)
;   CX = LOOP's implicit 16-bit counter (upper byte CH = 0 here)
;
; 8086 register naming reminder:
;   AX (16-bit)  =  AH (bits 15-8) : AL (bits 7-0)
;   BX, CX, DX follow the same H/L split pattern
;   SI, DI, BP, SP have no H/L split
;
; Key differences vs 8080:
;   - MOV replaces MVI for immediates (unified mnemonic)
;   - ADD AL, CL has explicit register operands (Intel two-operand syntax)
;   - OUT 1, AL — destination port then source register (reversed field order vs 8080)
;   - LOOP = "CX-- ; branch if CX != 0"  (one instruction like Z80's DJNZ, but uses CX)
;   - Termination via DOS interrupt (INT 20h) rather than HLT in .COM context
;   - Segment registers (CS, DS, ES, SS) not visible in this 64 KB program
;
; 8086 extras not used here:
;   - 16-bit arithmetic: ADD AX, BX computes 16-bit Fibonacci in one instruction
;   - Segment:offset addressing for >64 KB data
;   - String ops: MOVSB, LODSB, STOSB (block memory operations)
; ------------------------------------------------------------
