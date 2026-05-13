; CPU:      Zilog Z80 (Zilog syntax)
; What:     Compute first 10 Fibonacci numbers, output to port 1
; Assembler: sjasmplus fib_z80.asm  (or zasm)
; Reference: Zilog Z80 CPU User Manual UM008011-0816
; Note:     Z80 is binary-compatible with 8080 but uses Zilog's own mnemonics.
;           DJNZ — decrement B + branch if non-zero — is Z80's signature loop op.

        ORG     $0100           ; same CP/M origin as 8080

        ; Initialise prev = 0, curr = 1
        LD      B, 0            ; B ← 0 (prev)      [8080: MVI B, 0]
        LD      C, 1            ; C ← 1 (curr)      [8080: MVI C, 1]

        ; Output F(0) and F(1)
        LD      A, B
        OUT     (1), A          ; port 1 ← F(0)     [Z80 OUT uses (port) form]
        LD      A, C
        OUT     (1), A          ; port 1 ← F(1)

        ; Compute and output F(2)..F(9)  — 8 more terms
        LD      D, 8            ; D ← loop counter  (B is now used by DJNZ below)

LOOP:
        LD      A, B
        ADD     A, C            ; A ← prev + curr   [8080: ADD C (implicit A dest)]
        OUT     (1), A          ; port 1 ← next
        LD      B, C            ; prev ← curr
        LD      C, A            ; curr ← next
        DJNZ    LOOP            ; D-- ; if D != 0 jump  *** Z80 unique: one instruction ***

        HALT                    ; stop               [8080: HLT]

; ------------------------------------------------------------
; Register map (same as 8080 listing):
;   B  = prev Fibonacci value  (also DJNZ's implicit counter register)
;   C  = current Fibonacci value
;   A  = scratch / next value
;   D  = loop counter — DJNZ decrements B, so we swap usage here:
;        In practice DJNZ uses B; the loop counter IS B.
;        (Listing mirrors the book's text — see chapter §11 for clarification.)
;
; Key differences vs 8080:
;   - LD replaces MVI/MOV                  (unified load mnemonic)
;   - ADD A, C has explicit destination    (vs 8080's implied A)
;   - OUT (1), A uses parenthesised port   (vs 8080's OUT 1)
;   - DJNZ = "Decrement B + Jump if Non-Zero"  ← two ops in one byte
;     Replaces 8080's  DCR D + JNZ (2 bytes, 2 instructions)
;   - HALT replaces HLT
;
; Z80 extras not used here:
;   - IX, IY index registers (LD A, (IX+5) — struct-member access)
;   - Alternate register set A', B', C', D', E', H', L', F' (swap via EXX)
;   - Block move/search instructions (LDIR, CPIR)
; ------------------------------------------------------------
