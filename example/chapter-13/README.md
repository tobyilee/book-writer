# 13장 — 우리의 8비트 RISC를 설계하다

> **핵심 한 줄:** 12장에서 손에 쥔 RISC 철학을 8비트로 축소해 직접 만져본다 — 16비트 고정 길이 명령어, 레지스터-레지스터 산술, load/store, R0=zero. SAP-2 계보를 끊고 백지에서 새로 그린다.

---

## 이 장이 던지는 질문

11장에서 8080·Z80·6502·8086을 나란히 놓아봤다. 모두 CISC였다. 명령어가 많고 어드레싱 모드가 다양하고 사이클 수가 들쭉날쭉했다.

12장에서는 RISC 진영의 외침을 따라갔다. "명령어를 줄여라. 고정 길이로. load/store만 메모리를 만지게. 컴파일러를 똑똑하게."

그렇다면 그 철학을 우리 손으로 8비트에 축소해보자. **RISC-8** — 이 책만의 합성 ISA. 16비트 고정 길이 명령어, 8개 8비트 레지스터, R0은 하드와이어 zero. 그러면 무엇이 보일까?

---

## RISC-8 ISA 한눈에

| 항목 | 본 책 RISC-8 | 비교: 본 책 SAP-2 |
|------|--------------|-------------------|
| 명령어 길이 | **16비트 고정** | 1~3바이트 가변 (8080 subset) |
| 메모리 모델 | Harvard-ish (instr/data 분리) | von Neumann |
| 레지스터 | R0..R7 (R0=zero) | A, B, C |
| 명령어 종류 | 20개 (NOP/HALT 포함) | 39개 |
| 어드레싱 모드 | 즉치·레지스터·base+disp 셋 | 즉치·직접·간접 등 다양 |
| 사이클 모델 | 1 instr = 1 step (instruction-accurate) | 가변 (14장에서 cycle-accurate화) |
| 분기 | PC-relative (3-bit / 6-bit signed) | 절대 주소 |
| 인터럽트 | ECALL/EBREAK 트랩 (단순 종료) | (없음) |

11장 표에 한 줄 더 끼워보면 RISC-8의 자리가 보인다.

| CPU | 출시 | 명령어 길이 | 명령어 수 | 분기 모델 | 레지스터 |
|-----|------|-------------|-----------|-----------|----------|
| Intel 8080 | 1974 | 1~3 바이트 가변 | ~244 | 절대 주소 | 7 (8-bit) |
| MOS 6502 | 1975 | 1~3 바이트 가변 | 56 | 절대 + relative | 3 (8-bit) |
| Zilog Z80 | 1976 | 1~4 바이트 가변 | ~252 + prefix | 절대 + relative | 7+alt |
| Intel 8086 | 1978 | 1~6 바이트 가변 | ~117 base | 절대 + segment | 8 (16-bit) |
| **RISC-8 (본 책)** | **2026 합성** | **2 바이트 고정** | **20** | **PC-relative** | **8 (8-bit, R0=zero)** |

길이가 고정되고 종류가 줄어든 자리에 무엇이 들어차는가 — 디코더의 단순함, 컴파일러의 부담, 그리고 fetch-decode-execute 한 사이클의 청결함이다.

---

## 명령어 포맷

비트 배치는 다음 네 가지다.

```
  bit 15........9 8....6 5....3 2....0
R-type: [opcode:7][rd:3 ][rs1:3][rs2:3]
I-type: [opcode:7][rd:3 ][rs1:3][imm:3]    (imm은 3-bit signed; 메모리·JR는 unsigned로 해석)
J-type: [opcode:7][rd:3 ][   imm6:6      ] (분기 오프셋 6-bit signed)
L-type: [opcode:7][rd:3 ][   imm6:6      ] (LI는 6-bit zero-extended)
```

opcode 7비트 = 최대 128종이지만 우리는 20개만 정의한다. 남은 자리는 후속 챕터에서의 확장(인터럽트 핸들러, mul/div, etc.) 여지로 비워둔다.

---

## opcode 표

| opcode | 니모닉 | 타입 | 연산 |
|--------|--------|------|------|
| 0x00 | `NOP` | — | 아무것도 안 한다 |
| 0x01 | `ADD rd, rs1, rs2` | R | rd ← rs1 + rs2 |
| 0x02 | `SUB rd, rs1, rs2` | R | rd ← rs1 − rs2 |
| 0x03 | `AND rd, rs1, rs2` | R | rd ← rs1 & rs2 |
| 0x04 | `OR  rd, rs1, rs2` | R | rd ← rs1 \| rs2 |
| 0x05 | `XOR rd, rs1, rs2` | R | rd ← rs1 ^ rs2 |
| 0x06 | `SHL rd, rs1, rs2` | R | rd ← rs1 << (rs2 & 7) |
| 0x07 | `SHR rd, rs1, rs2` | R | rd ← rs1 >> (rs2 & 7) (logical) |
| 0x10 | `ADDI rd, rs1, imm` | I | rd ← rs1 + signExt(imm3) |
| 0x11 | `ANDI rd, rs1, imm` | I | rd ← rs1 & signExt(imm3) |
| 0x20 | `LB rd, rs1, imm` | I | rd ← mem[rs1 + imm] |
| 0x21 | `SB rd, rs1, imm` | I | mem[rs1 + imm] ← rd |
| 0x30 | `BEQ rd, rs1, off` | I | if rd == rs1 then PC ← PC + signExt(imm3) |
| 0x31 | `BNE rd, rs1, off` | I | if rd != rs1 then PC ← PC + signExt(imm3) |
| 0x40 | `JAL rd, imm6` | J | rd ← PC; PC ← PC + signExt(imm6) |
| 0x41 | `JR rd, rs1, imm` | I | PC ← rs1 + signExt(imm3) |
| 0x50 | `LI rd, imm6` | L | rd ← imm6 (zero-extended to 8) |
| 0x60 | `ECALL` | — | 환경 호출 (본 책에서는 단순 종료로 처리) |
| 0x61 | `EBREAK` | — | 브레이크포인트 트랩 (단순 종료) |
| 0x7F | `HALT` | — | 실행 종료 |

> **PC는 명령어당 +1로 증가한다.** 명령어가 `IntArray`에 워드 단위로 저장되기 때문이다 — 진짜 하드웨어처럼 바이트 어레이에 명령어를 풀어두면 +2가 맞지만, 시뮬레이터 단순성을 위해 워드 인덱스를 PC로 본다.

---

## 설계 결정

### 왜 16비트 고정 길이인가

8비트 시대의 CISC는 1바이트 opcode 다음에 0~2바이트 피연산자가 따라붙는 가변 길이 방식을 썼다. 디코더가 첫 바이트를 보고 "아, 이건 2바이트짜리, 저건 3바이트짜리" 식으로 명령어 길이를 정해야 한다. 파이프라이닝의 적이다.

RISC-8은 모든 명령어가 정확히 2바이트(16비트)다. 어떤 명령어든 다음 명령어는 +1 떨어진 자리에 있다. fetch가 끝나는 순간 다음 fetch 주소가 결정된다. 14장에서 cycle-accurate 시뮬레이터를 짤 때 이 단순함의 보상을 받는다.

### 왜 8개 레지스터인가 (R0..R7)

처음 계획은 16개였다. 그러나 16개를 가리키려면 4비트 필드가 필요하다. R-type 명령어에는 rd·rs1·rs2 세 자리가 있으니까 16비트 명령어에서 4·4·4 = 12비트가 레지스터 자리로 빠지고, opcode에 4비트만 남는다. opcode 16개 — RISC라기엔 너무 빈약하다.

3비트 레지스터 필드로 줄이면 레지스터는 8개로 줄어드는 대신 opcode가 7비트(128종)까지 늘어난다. RISC의 정신은 명령어 수를 줄이는 쪽이지만, ISA 확장 여지를 7비트 opcode가 더 시원하게 준다. 본 책은 그 트레이드오프를 받아들였다.

### 왜 R0 = 0 (zero register)

RISC-V·MIPS·SPARC 모두 R0을 하드와이어 0으로 둔다. 그 자리에 비교 값을 두면 `BNE rd, R0, off`가 "rd != 0 이면 분기"가 된다 — 별도 `BNEZ` 명령어를 안 만들어도 된다. 본 책 Fibonacci에서 `ADD R1, R0, R2`로 "R1 ← R2" 이동을 했다. zero 레지스터 하나로 `MOV` 명령어 자리를 비웠다.

### 왜 load/store 아키텍처

RISC의 다섯 줄 선언문 두 번째 조항 — "메모리 접근은 LB/SB 두 명령어로만. 산술은 레지스터끼리만." 그 결과 6502의 `ADC $81`처럼 산술이 메모리를 직접 만지는 명령어가 RISC-8에는 없다. `LB → ADD → SB`로 세 명령어가 된다.

코드는 길어진다. 그러나 ALU는 단순해지고, 파이프라이닝이 깨끗해진다. 12장에서 봤듯 1980년대 컴파일러가 이 단점을 흡수하기 시작했고, 1990년대가 되면서 RISC가 우세해진 결정적인 이유다.

### 왜 PC-relative 분기

8080·6502·8086은 분기 타깃을 절대 주소로 적었다. 그 결과 코드를 메모리 다른 위치로 옮기면 분기를 다시 어셈블해야 한다 — 위치 독립적이지 않다.

RISC-8 분기는 모두 PC-relative다. `BEQ R1, R2, +3`은 "지금 PC에서 3 떨어진 자리로 점프"다. 코드 전체를 옮겨도 분기는 그대로다. 이걸 **position-independent code(PIC)**라 부른다 — 공유 라이브러리·ASLR·다이내믹 링킹이 다 이 위에 서 있다.

### 인터럽트 — ECALL/EBREAK 트랩

RISC-V를 따랐다. `ECALL`은 환경 호출(시스템 콜), `EBREAK`은 브레이크포인트. 본 책 시뮬레이터에서는 둘 다 단순히 CPU를 종료시킨다 — 진짜 트랩 벡터·핸들러 도입은 14장 이후의 숙제로 남겨둔다. 명령어 자리만 미리 잡아두는 셈이다.

---

## 어셈블러

본 책 어셈블러는 7장의 SAP-2 어셈블러와 같은 두-패스 구조다.

```
Pass 1: 라벨 주소 수집
Pass 2: 명령어 인코딩 (라벨 → 오프셋 계산 포함)
```

분기/점프 타깃에 라벨이 오면 PC-relative 오프셋을 자동 계산한다.

```asm
        BEQ R0, R0, end       ; "end" 라벨 → +1 forward
        LI  R1, 99
end:    HALT
```

이런 식이다. 한 줄에 여러 라벨도 가능하고, 라벨만 있는 줄도 허용한다. `;` 이후는 주석.

---

## Fibonacci 실행

```bash
./gradlew :chapter-13:run
```

기대 출력:

```
--- RISC-8 Fibonacci ---
프로그램 워드 수: 14
실행 사이클 수: ~83
메모리 [0x10..0x19] = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

소스는 `src/main/resources/programs/fib.risc8`에 있다.

`BEQ`의 3-bit signed 오프셋이 ±4 범위라 5칸 이상 떨어진 라벨로는 못 간다. 그래서 본 책 Fibonacci 루프는 `BEQ`로 짧은 forward 종료 점프 + `JAL`(6-bit signed, ±32)로 긴 backward 점프를 조합한다. 이 패턴이 RISC 시대 컴파일러가 즐겨 쓴 분기 확장(branch displacement extension)의 작은 예시다.

---

## 테스트

```bash
./gradlew :chapter-13:test
```

- `IsaTest` — 모든 명령어의 encode/decode 라운드트립, 비트 레이아웃 검증
- `AssemblerTest` — 라벨 forward/backward 참조, 16진수·음수 즉치, 주석·빈 줄 처리
- `CpuFibTest` — LI/ADD/SB/LB/루프 기본 동작 + Fibonacci end-to-end

---

## 산출물

```
src/main/kotlin/risc8/ch13/
├── Isa.kt          — sealed class Instruction (R/I/J/L type) + encode/decode
├── Assembler.kt    — two-pass assembler with PC-relative label resolution
├── Cpu.kt          — instruction-accurate simulator
└── Risc8Demo.kt    — fib.risc8 실행하는 main()

src/main/resources/programs/
└── fib.risc8       — Fibonacci F(0)..F(9)

src/test/kotlin/risc8/ch13/
├── IsaTest.kt
├── AssemblerTest.kt
└── CpuFibTest.kt
```

---

## 관련 챕터

- **11장** — 8080/Z80/6502/8086 CISC 비교 — RISC-8 한 줄을 이 표에 추가한다
- **12장** — RISC의 약속 — Patterson·Hennessy의 RISC 다섯 줄 선언
- **14장** — instruction-accurate에서 cycle-accurate로 — 본 챕터의 RISC-8을 사이클 단위로 다시 짠다
- **15장** — 여기서 어디로 — RISC-V로 가는 다리
