# Kotlin으로 만드는 8비트 CPU 시뮬레이터 — 종합 레퍼런스

> **책 주제:** Kotlin 언어로 8비트 CPU 시뮬레이터(SAP-1 → SAP-2 → 8비트 RISC)를 직접 구현하며 컴퓨터 아키텍처를 학습.
> **대상 독자:** Kotlin/Java 중급 개발자, 학부 1학년 컴퓨터 아키텍처 수준의 지식을 다시 쌓고 싶은 사람.
> **수집 일시:** 2026-05-13.
> **소스:** 웹 리서치 28건 (`research/web.md`), 학술 논문 15편 + 표준 교과서 6종 (`research/papers.md`), 커뮤니티 토론 30+ 건 (`research/community.md`).
> **출처 표기 규칙:** `[웹-자료N]`, `[논문-N]`, `[교과서-TN]`, `[커뮤니티-패턴N]` / `[커뮤니티-휴리스틱N]` / `[커뮤니티-논쟁X]`.

---

## 1. 개념과 정의

### 1.1 von Neumann 아키텍처와 stored program

본 책의 첫 번째 핵심 개념. 1945년 John von Neumann이 *First Draft of a Report on the EDVAC*에서 처음 공식화 [논문-1]. 명령어와 데이터를 단일 메모리에 저장하는 모델 — 본 책이 만들 SAP-1, 6502, 그리고 오늘의 모든 일반 컴퓨터의 직계 조상.

핵심 구성:
- **CPU** (연산 + 제어), **메모리** (명령어 + 데이터 통합), **I/O**
- 단일 메모리 안에 명령어와 데이터가 함께 머문다 — Tanenbaum의 "computer as hierarchy of levels" [교과서-T3]의 ISA 계층.

> "A uniform memory containing both numbers (data) and orders (instructions)." (von Neumann 1945 [논문-1])

상충 관점: nand2tetris의 Hack CPU는 **Harvard 아키텍처**(명령어/데이터 메모리 분리)를 채택 [웹-자료6]. 본 책은 von Neumann을 따르되, Harvard와의 비교를 명시한다.

### 1.2 fetch-decode-execute 사이클

CPU 동작의 기본 루프. PC → MAR → 메모리 read → MDR → CIR → decode → execute → PC 증가 [웹-자료15]. 표준 교과서가 일관되게 정의.

> "The Fetch-Execute cycle... was first introduced by John von Neumann. This cycle starts when the computer is turned on and keeps repeating until the computer is shut down." (Baeldung CS [웹-자료15])

이 사이클이 본 책 챕터 2의 핵심 — Kotlin 코드에서 `while(true)` 루프 안에 fetch/decode/execute 메서드 호출이 직접 매핑된다.

### 1.3 SAP-1 (Simple-As-Possible 1)

Malvino & Brown, *Digital Computer Electronics* (1993)의 가장 단순한 교육용 CPU [웹-자료1, 교과서-T4].

| 항목 | 값 |
|------|---|
| 데이터 폭 | 8비트 |
| 어드레스 폭 | 4비트 |
| 메모리 | 16바이트 RAM |
| 명령어 | 5개 (LDA, ADD, SUB, OUT, HLT) — 일부 변형에서 8개 |
| 누산기 | 1개 (A) |
| ALU | 8비트 2's complement 가산/감산 + Z·C 플래그 |
| 컨트롤 | 조합 논리 + EEPROM lookup table (마이크로코드) |
| T-state | 명령어당 6개 (또는 변형 5개) |

핵심 모듈 [웹-자료3]: 클록, PC(4비트), MAR, RAM, IR(opcode 4비트 + operand 4비트), 컨트롤러/시퀀서, A·B 레지스터, ALU, 출력 레지스터, W-bus.

> "Capable of adding and subtracting 8-bit 2's complement integers" with flags for zero (Z) and carry (C). [웹-자료1]
> "ISA is patterned after and upward compatible with the ISA of the Intel 8080/8085 microprocessor family." [웹-자료1]

### 1.4 SAP-2

SAP-1의 진화형. **단순 명령어 추가가 아니라 마이크로아키텍처의 근본 재설계** [웹-자료2].

SAP-1 → SAP-2 변화:
- 메모리 16바이트 → 64K
- 어드레스 폭 4비트 → 16비트
- 명령어 5~8개 → 39개 (Intel 8080 subset)
- 누산기 1개 → 범용 레지스터 3개 (A/B/C)
- 컨트롤러: 조합 논리 → ROM 기반 마이크로코드 (35 control signals × 10 T-states)
- 새 명령어 클래스: 조건 점프(JZ/JNZ/JM), CALL/RET, 논리 연산(AND/OR/XOR), I/O 포트

상충/한계: Austin Morlan의 FPGA 구현 후기는 SAP-2 명세가 "highly awkward and strange"하다고 평한다 [웹-자료2]. 함수가 다른 함수를 호출하면 return address가 덮어쓰여 깨진다는 명세 결함. SAP-3에서 해결.

> "Where SAP-1 had one accumulator, SAP-2 introduces three general-purpose registers (A, B, C)." [웹-자료2]
> "If you find the architecture of this version to be highly awkward and strange, we are in agreement." (Austin Morlan [웹-자료2])

### 1.5 RISC (Reduced Instruction Set Computer)

핵심 정의:
- **load/store 아키텍처:** 메모리 접근은 LD/ST 명령어만, 산술 연산은 레지스터끼리만 [웹-자료16, 논문-2]
- **고정 길이 명령어:** 디코딩 단순화, 파이프라이닝 친화
- **단일 사이클 실행 목표:** IPC ≈ 1
- **큰 레지스터 파일:** 16~32개 범용 레지스터
- **단순화된 어드레싱 모드**
- **컴파일러 의존:** 하드웨어가 해결할 일을 컴파일러가 한다 (예: Stanford MIPS의 delay slot)

역사적 발전 [웹-자료16, 논문-2,3,4]:
1. **IBM 801** (1975~1980, John Cocke) — "first RISC system"
2. **Berkeley RISC-I** (1981~1982, Patterson) — 44,420 트랜지스터, 32 명령어
3. **Stanford MIPS** (1981~1984, Hennessy) — "Microprocessor without Interlocked Pipeline Stages"
4. **SPARC** (Sun 1987), **ARM** (Acorn 1986), **MIPS R2000** (1985, 상용화)
5. **RISC-V** (Berkeley 2010s) — 오픈 ISA

> "Most programs made no use of the large variety of complex instructions" (Patterson, Berkeley RISC 결론 [웹-자료16])
> "In some sense the 801 appears to be rushing in the opposite direction to the conventional wisdom of this field. Namely, everyone else is busy moving software into hardware and we are clearly moving hardware into software." (Radin 1983 [논문-3])

본 책의 "8비트 RISC" 챕터는 이 정신을 8비트로 축소 — 단순화된 MIPS/DLX [웹-자료] 또는 RISC-V 32I subset의 8비트 버전.

### 1.6 CISC (Complex Instruction Set Computer)

대비점:
- 가변 길이 명령어
- 메모리 직접 연산(memory-memory 명령)
- 마이크로코드 기반 컨트롤 (마이크로프로그래밍)
- 코드 밀도 우선

8비트 시대의 CISC: Intel 8080, 8085, Z80 (Z80은 더 강한 CISC), 8086.
8비트 시대의 (준)RISC: 6502 (단순 명령어 + 적은 레지스터지만, 페이지 0 지향 어드레싱이 강력해 RISC와 CISC 중간).

### 1.7 datapath와 control unit

CPU 내부 구조의 2분류:
- **datapath:** 데이터가 흐르는 회로 (레지스터, ALU, 버스) [웹-자료]
- **control unit:** datapath의 control signal을 생성

control unit 두 종류 [웹-자료]:
- **hardwired:** 조합 논리로 직접 signal 생성. 빠르지만 변경 불가. SAP-1에 적합.
- **microprogrammed:** ROM에서 마이크로 명령어를 읽어 signal 생성. 유연하지만 한 단계 느림. SAP-2 이상에 적합.

> "The data section is the same for both the micro-coded and hardwired approaches. The main difference between Hardwired and Microprogrammed Control Unit is that a Hardwired Control Unit is a sequential circuit that generates control signals while a Microprogrammed Control Unit is a unit with microinstructions in the control memory to generate control signals." [웹-자료]

### 1.8 instruction-accurate vs cycle-accurate emulation

[웹-자료20, 논문-12, 커뮤니티-논쟁B]

- **instruction-accurate:** 명령어 완료 시점만 정확. 내부 사이클은 추상화.
- **cycle-accurate:** 매 클록 사이클마다 하드웨어와 동일한 상태.
- **gate-level / transistor-level:** 더 깊은 정확도 (게이트/트랜지스터 단위 — 대부분 실용 가치 없음)

Game Boy의 경우 1 M-cycle = 4 T-cycle. M-cycle 단위 추상화가 정확도-성능 좋은 절충 [웹-자료20].

> "Cycle accuracy means that every single aspect of the emulated system occurs at the correct time relative to everything else." [웹-자료20]

본 책 위치: instruction-accurate로 시작 → 마지막에 cycle-accurate으로 리팩토링 (8비트 CPU의 메모리/IO 동기 학습).

### 1.9 어셈블러/디스어셈블러

[웹-자료22]

**2-pass 어셈블러:**
1. 1차 pass: 명령어 길이/주소 결정, 심볼 테이블 구축
2. 2차 pass: forward reference 해결, 기계어 생성

가변 길이 명령어가 있으면 3-pass도 필요. 본 책의 Kotlin 어셈블러 구현 챕터의 골격 알고리즘.

---

## 2. 핵심 관점들

### 2.1 페다고지 관점 — 만들어야 안다

세 갈래 자료 모두 일관되게 강조:

- 학술 (논문-7,8,9,13,14): "simulators enhance learning"이 SIGCSE/CACM 합의. 시뮬레이터 사용 그룹이 대조군 대비 어셈블리 이해 시험에서 유의미 우위 [논문-13].
- 웹 (자료6,19): nand2tetris와 Crafting Interpreters가 페다고지 모델. "first principles, hands-on, project per chapter."
- 커뮤니티 (패턴1,5): "Ben Eater 영상 한 편이 학부 강의 2년보다 낫다"는 후렴 반복.

> "ChampSim simulator's design does not necessarily attempt to precisely replicate all hardware functions, but to emulate it in a readable way, allowing a student to rapidly grasp its functionality." [논문-12]
> "Students should first learn about systems in terms of how they affect the behavior and performance of their programs—a 'programmer's perspective.'" (CSAPP [웹-자료24])

### 2.2 단순함 우선 관점

세 자료 모두 합의: **첫 emulator는 단순한 시스템에서 시작.**

- 웹 자료 (emudev.org [웹-자료21]): "Most people start with a CHIP-8 emulator."
- 학술 (논문-8): "복잡한 실제 CPU보다 단순한 교육용 시뮬레이터가 학습 효과 우월."
- 커뮤니티 (패턴2): r/EmuDev 17K 회원 사실상 만장일치로 "Chip-8 먼저."

본 책의 SAP-1(5 명령어, 16바이트)은 Chip-8과 동등한 진입 수준. **본 책의 차별점은 거기서 SAP-2 → 8비트 RISC로 단계적으로 올라간다는 점.**

### 2.3 점진적 진화 관점 (incremental construction)

- 학술 (논문-7, 교과서-T5,T6): nand2tetris(12 프로젝트), Crafting Interpreters(Lox를 두 번 — Java tree-walker → C bytecode VM). 본 책의 SAP-1 → SAP-2 → RISC도 같은 패턴.
- 웹 (자료19): "This dual implementation strategy isn't just a structural gimmick. It serves a deep pedagogical purpose, allowing readers to first grasp the conceptual architecture in a high-level language before rebuilding everything from raw memory."
- 커뮤니티 (패턴5): "make it work → make it right → make it fast"가 emudev 합의.

### 2.4 역사적 맥락 관점

학술과 웹이 일치: 8비트 시대(1970~1980년대)는 컴퓨터 아키텍처의 기초 어휘가 정립된 시대. 8086(1978)이 16비트로 확장되며 x86 계보 시작 [웹-자료14]. RISC 혁명은 1980년대 [논문-2,3,4]. Apple Silicon, RISC-V의 부상까지 이어진다.

> "Approximately 1986–1996, when new instruction set architectures, almost all reduced instruction set computers (RISCs), revolutionized the industry." (Hennessy & Patterson 2019 [논문-5])

본 책 함의: 8비트 CPU를 만드는 것은 박물관 견학이 아니라 **컴퓨터 아키텍처의 어휘를 손으로 익히는 일.**

### 2.5 가독성 우선 관점

본 책의 코딩 결정에 직접 적용:
- ksim65 [웹-자료7]는 의도적으로 cycle-exact를 포기 — "simplicity reasons."
- ChampSim [논문-12]: "한 학기에 학생이 이해 가능한 가독성"이 정확도보다 우선.

대조 관점: BeesNES (sub-cycle-accurate NES emulator) 같은 프로젝트는 정확도가 본질이라고 본다. 본 책은 학습용이므로 가독성 우선 노선을 선택.

---

## 3. 대표 사례

### 3.1 SAP-1을 실제로 만든 사례들

- **Ben Eater 8-bit breadboard computer** [웹-자료4]: SAP-1을 74LS IC + 브레드보드로 구현. YouTube 시리즈가 표준. 학습 효과 측면에서 가장 영향력 큰 콘텐츠 [커뮤니티-후기].
- **dangrie158 SAP-1 documentation** [웹-자료3]: SAP-1을 모듈별로 상세 문서화. EEPROM lookup table 코드 공개.
- **Austin Morlan FPGA SAP-2** [웹-자료2]: SAP-2를 FPGA로 구현. SAP-1 → SAP-2 진화의 학술적 비판도 포함.

### 3.2 Kotlin/JVM CPU 시뮬레이터 사례

| 프로젝트 | 대상 CPU | 특징 | 인용 |
|---|---|---|---|
| **ksim65** | 6502/65C02 | 가장 성숙. C-64 ROM 실행. instruction-accurate. MIT. | [웹-자료7] |
| **kNES** | 6502 + NES | Java vNES Kotlin 포팅. cycle-accurate. | [웹-자료9] |
| **6502Android** | 6502 | Easy 6502를 Android Kotlin으로 | [웹-자료] |
| **Scuffed-6502Kt** | 6502 | 학습 프로젝트. 본 책 대상 독자와 동일 출발선. | [웹-자료8] |
| **cbeust/chip-8** | Chip-8 | Cédric Beust (TestNG 창시자)의 Kotlin Chip-8 | [웹-자료18] |
| **p1ng07/chip8-emulator-kotlin** | Chip-8 | 입문자용 Kotlin Chip-8 | [웹-자료] |

본 책은 위 사례들을 부록의 "더 읽을거리"로 추천하고, 본문에서 ksim65와 kNES의 패턴(`when` 디스패치, sealed class, data class 활용)을 인용한다.

### 3.3 실제 8비트 CPU 비교 (정량 데이터)

[웹-자료11,12,13,14,자료26,27, 논문 보강]

| CPU | 출시 | 트랜지스터 | 데이터/주소 | 레지스터 | 명령어 수 | 어드레싱 모드 | 가격(출시 당시) | 대표 적용처 |
|---|---|---|---|---|---|---|---|---|
| Intel 8080 | 1974 | 4,500~6,000 | 8/16비트 (64KB) | A,B,C,D,E,H,L + SP + PC | ~244 | 다양 | $360 | Altair 8800, CP/M |
| MOS 6502 | 1975 | ~3,510 | 8/16비트 (64KB) | A,X,Y + SP + PC + P | 56 (official) | 13 | **$25** | Apple II, C64, NES, Atari 2600 |
| Zilog Z80 | 1976 | ~8,500 | 8/16비트 (64KB) | A,B,C,D,E,H,L,F,I,R + IX,IY + SP + PC + alt set | ~252 + prefix 확장 | 다양 | ~$50 | TRS-80, ZX Spectrum, MSX, Sega Master System, Game Boy(클론) |
| Motorola 6800 | 1974 | 4,000+ | 8/16비트 (64KB) | A,B + IX + SP + PC | ~72 | 7 | $360 | (6502가 후속) |
| Intel 8085 | 1976 | 6,500 | 8/16비트 (64KB) | 8080과 호환 + 2개 신규 | ~246 (8080 + 2) | 8080과 동일 | $20~30 | 임베디드 |
| Intel 8086 | 1978 | 29,000 | 16/20비트 (1MB, 세그먼트) | AX,BX,CX,DX,SI,DI,BP,SP + 4 segment + PC + Flags | ~117 base | 다양 | $86.65 (1979) | IBM PC (8088 변형) |

핵심 비교 포인트:
- **6502의 가격 혁명** [웹-자료12, 자료26]: $25 vs $179~$360. Apple II, NES, C64를 가능하게 만든 결정적 요인.
  > "The Apple II put computing in schools. The Commodore 64 put it in living rooms. The NES made it entertainment for an entire generation." (Harlepengren [웹-자료12])
- **Z80의 8080 호환 + 확장** [웹-자료11]: binary 상위 호환. IX/IY 인덱스 레지스터, 대체 레지스터 셋, 블록 전송, 더 풍부한 비트 조작.
- **8086의 16비트 확장** [웹-자료14]: 8080의 16비트 확장. 세그먼트 레지스터로 20비트 = 1MB. binary 비호환이지만 어셈블리 유사.
- **6502 vs Z80 레지스터 철학 차이**: 6502는 적은 레지스터(3개) + 강력한 zero page (페이지 0의 256바이트가 사실상 레지스터 파일). Z80은 많은 레지스터(7개+alt) + 풍부한 명령어.

### 3.4 교육용 CPU 비교

[웹-자료6,17 + 논문-7,10,11,14]

| 시스템 | 비트 | 명령어 수 | 레지스터 | 메모리 | 페다고지 모델 |
|---|---|---|---|---|---|
| SAP-1 (Malvino) | 8 | 5 | A (1) | 16바이트 | "Simplest possible" |
| SAP-2 (Malvino) | 8 | 39 | A,B,C (3) | 64KB | 8080 subset |
| Hack (nand2tetris) | 16 | ~28 | D,A (2) | 32KB | Harvard, gate-up |
| LC-3 (Patt & Patel) | 16 | 15 | R0-R7 (8) | 64K words | trap instruction으로 OS 모사 |
| MIPS (Patterson) | 32 | ~50 (subset) | 32 GPR | full | RISC pedagogy 표준 |
| DLX (H&P) | 32 | RISC pedagogy 클린업 | 32 GPR | full | *Quantitative Approach* 5판까지 |
| RISC-V (RV32I) | 32 | 47 base | 32 GPR | full | 현재 표준 |
| Chip-8 | 4 (opcode 12-bit) | 35 | V0-VF (16) | 4KB | emudev hello world |

본 책 위치: **SAP-1 → SAP-2 → 8비트 RISC 라인의 점진적 진화**가 위 어느 교과서에도 정확히 없다 — 본 책의 시장 공백.

### 3.5 후속 학습 경로 사례

[웹-자료6, 자료24, 자료28, 커뮤니티-휴리스틱6]

- nand2tetris: NAND → CPU → 어셈블러 → VM → 컴파일러 → OS → Tetris (12 프로젝트) [웹-자료6, 논문-7]
- *Computer Systems: A Programmer's Perspective* [웹-자료24]: layered abstraction (HW → asm → C → 응용)
- *Operating Systems: Three Easy Pieces* (OSTEP), *Crafting Interpreters*, *Operating Systems from 0 to 1* — CPU 시뮬레이터 다음 자연스러운 학습 경로

본 책 마지막 챕터: "여기서 어디로 갈 것인가" — Kotlin emulator 다음 단계로 메모리 시스템 → I/O 디바이스 → 인터럽트 → 커널 → OS의 청사진 제시.

---

## 4. 논쟁점·상충 관점

### 4.1 RISC vs CISC — 1980년대의 격렬한 논쟁

[논문-2,5,15, 커뮤니티-논쟁C]

**관점 A (RISC 옹호, Patterson 진영):**
- Patterson & Ditzel 1980: "단순 명령어가 90% 사용된다. 마이크로코드로 복잡 명령어를 만드는 비용은 그 명령어의 사용 빈도를 정당화하지 못한다." [논문-2]
- 결과적으로 ARM 모바일 지배, Apple Silicon, RISC-V 부상. "역사가 RISC 손을 들어줬다."

**관점 B (CISC 옹호, Clark & Strecker 진영):**
- Clark & Strecker 1980: "복잡 명령어는 마이크로코드로 저렴하다. 메모리/캐시 비용을 줄인다." [논문-15]
- "Most of the proposed RISC's advantage will be lost when faced with the realities of the marketplace." (요약)

**관점 C (현대적 통합 관점):**
- 현대 x86은 internal하게 RISC-like micro-op으로 변환. RISC vs CISC 구분은 사실상 사라졌다. [논문-5, 커뮤니티-논쟁C]
- "Modern RISC sets often rival CISC in size." [웹-자료16]

본 책 위치: **1980년대의 격렬한 논쟁을 역사로 다루되, "RISC 정신이 ISA 설계의 표준 어휘가 됐다"고 정리**. 8비트 RISC 챕터에서 그 정신을 손으로 체화.

### 4.2 cycle-accurate vs instruction-accurate

[웹-자료20, 논문-12, 커뮤니티-논쟁B]

**관점 A (사이클 정확도 필수):**
- 8비트 시스템(NES, Game Boy)은 PPU/CPU 동기에 의존. instruction-accurate면 게임이 깨진다 [웹-자료20].
- 결과적 사례: BeesNES(sub-cycle-accurate), bsnes/higan (Byuu의 cycle-accurate 철학).

**관점 B (학습용은 instruction-accurate):**
- ksim65 [웹-자료7] 의도적 포기 — "for simplicity reasons."
- ChampSim 페다고지 [논문-12]: "한 학기 가독성"이 우선.

**본 책 결정:** instruction-accurate로 시작, **마지막에 cycle-accurate로 리팩토링**해 정확도의 의미를 직접 체험. M-cycle(machine cycle) 단위 추상화도 옵션으로 다룬다.

### 4.3 실물 빌드 vs 시뮬레이터

[커뮤니티-논쟁A]

**관점 A (실물 필수):**
- HN: "Tactile experience of cutting wires and physically putting it together creates lasting intuition about hardware behavior—something simulations cannot replicate for embedded systems work."
- 회로의 floating input, 전압 강하, 타이밍을 겪어야 "왜 컴퓨터가 동작하는 것이 기적인가"를 안다.

**관점 B (시뮬레이터가 효율 우월):**
- HN: "$300+ in parts for a computer with only 16 bytes of memory... For learning efficiency, alternatives like nand2tetris offer similar conceptual understanding without physical assembly."
- 디버깅 시간 90%가 회로 문제. 페다고지 효율 낮다.

**합의:** "이론 → 시뮬레이터 → 실물"의 3단계가 이상적. **본 책은 2단계에 집중**, 마지막에 Ben Eater 추천으로 3단계 안내.

### 4.4 첫 emulator 언어 선택

[커뮤니티-논쟁D]

**관점 A (C/C++ 표준):**
- 비트 처리·메모리 레이아웃이 emulator와 직결. 대부분 튜토리얼이 C/C++.

**관점 B (친숙한 언어 우선):**
- tobiasvl Chip-8 가이드 [웹-자료]: "Pick a programming language you're familiar with such as C/C++ or Java."
- emulator 학습이 본업이지 언어 학습이 아니다.

**본 책 위치:** Kotlin 선택의 정당화. 대상 독자(중급 Kotlin/Java)에게 친숙한 언어가 본질에 집중하게 한다. 다만 Kotlin의 signed byte 함정 [커뮤니티-패턴4]은 명시.

### 4.5 SAP-2 명세의 일관성 문제

[웹-자료2 (Austin Morlan)]

Malvino *Digital Computer Electronics* 3판 SAP-2 명세는 "highly awkward and strange" — 명세가 부분적으로 모호하다. 본 책은 모호한 부분을 일관성 있게 정리하는 게 가치 추가 지점. 책 본문에서 "원전이 모호한 곳은 이렇게 해석한다"고 메타 코멘트.

### 4.6 von Neumann이 진짜 발명자인가

[논문-1]

Eckert & Mauchly가 stored program 아이디어를 먼저 설계했고, von Neumann이 정리만 했다는 학술적 논쟁. 본 책은 "von Neumann architecture"라는 표준 용어를 쓰되, 한 단락 분량으로 역사적 논쟁을 명시.

---

## 5. 실무 적용 팁

### 5.1 Kotlin/JVM에서 8비트 값 표현 결정

[웹-자료10, 커뮤니티-패턴4]

선택지:
1. **`Int` + 마스킹 (`value and 0xFF`)**: JVM primitive로 가장 빠르고 호환성 좋음. 단점: 매번 마스킹 잊으면 부호 확장 버그. ksim65가 채택.
2. **`UByte` (Kotlin 1.5+)**: 0~255 자연 표현. JVM bytecode는 결국 Byte로 컴파일되지만 inline class라 overhead 무. 단점: Byte/Short의 비트 시프트가 미지원 (Kotlin 1.x.x 시점). `>>`을 쓰려면 `.toInt().shr().toUByte()` 변환 필요.
3. **`Byte` (signed -128~127)**: 자연어와 어긋남. 디버깅 지옥.

> "There is no significant overhead when using unsigned integer types on the JVM... Under the covers, all of the unsigned types in Kotlin are implemented as inline classes." [웹-자료10]

> "Bit shifts are provided only for UInt and ULong; for the narrower types, both for signed and unsigned, they are under consideration." [웹-자료10]

**책 권장:** 본문은 `Int` + 마스킹으로 시작(가독성, 호환성), 후반 챕터에서 `UByte`로 마이그레이션해 타입 안전성과 표현력의 차이를 직접 보여준다.

### 5.2 6502 ADC/SBC 플래그 구현

[웹-자료, 커뮤니티-패턴3]

90%의 입문자가 막히는 지점. 본 책 ALU 챕터에서:
1. 2의 보수 도식을 시각화
2. 각 비트별 carry-in/carry-out 흐름 다이어그램
3. ADC와 SBC의 overflow 플래그 공식을 단계 분해
4. 256개 × 2 carry 상태 = 512가지 케이스를 커버하는 테이블 기반 테스트

> "There's a program from 6502.org that verifies 6502 Overflow (V) Flag behavior, which tests both ADC and SBC instructions with all 256 possible values for both operands and different carry flag states." [웹-자료22, 커뮤니티-휴리스틱3]

본 책에 직접 적용: Kotlin의 parameterized test (`@ParameterizedTest`, kotest의 `forAll`)로 표 기반 검증을 작성하는 코드 패턴 제공.

### 5.3 어셈블러 2-pass 구현

[웹-자료22]

Kotlin으로 SAP 어셈블러를 짤 때:
1. **1차 pass:** 토큰화 + 명령어 길이 계산 + 심볼 테이블 구축. `Map<String, Int>`로 라벨 → 주소.
2. **2차 pass:** forward reference 해결, opcode 생성, 바이트 배열 출력.
3. 디스어셈블러는 역과정 — 바이트 → opcode → mnemonic. Kotlin `when` + sealed class로 분기.

### 5.4 데이터패스 모델링 (Kotlin 패턴)

- **레지스터 = 클래스 또는 mutable property**
- **버스 = 함수 인자 또는 메서드 호출**
- **명령어 = sealed class + data class**: `sealed class Instruction { data class Lda(val addr: Int): Instruction(); ... }`
- **명령어 디스패치 = `when` 표현식**: `when (opcode) { 0x00 -> nop(); 0x01 -> lda(operand); ... }`
- **마이크로코드 = 비트 플래그 enum + EnumSet 또는 Int 비트마스크**
- **메모리 = `IntArray` 또는 `UByteArray`**

ksim65, kNES 사례에서 검증된 패턴 [웹-자료7,9].

### 5.5 테스트 전략 (test ROM)

[커뮤니티-휴리스틱3]

8비트 emulator 검증의 사실상 표준:
- 6502: `klaus2m5/6502_65C02_functional_tests` (완전한 명령어 정상성 검증)
- NES: `nestest.nes`
- Chip-8: Timendus' test suite
- SAP-1: 본 책에서 직접 작성. 각 명령어 × 각 플래그 조합 = ~50개 단위 테스트.

본 책에 직접 적용: 처음부터 TDD로 SAP-1을 구현 — 빨간 줄(테스트) → 초록 줄(구현) → 리팩터의 사이클이 emulator 개발의 가장 안전한 방법.

### 5.6 datasheet 읽기 능력 빌드

[커뮤니티-휴리스틱4]

한국 학습자 약점 영역. 본 책은:
- Intel 8080 datasheet의 핵심 페이지(레지스터 맵, 명령어 인코딩, 타이밍 다이어그램)를 발췌해 보여준다
- "이 페이지의 이 표를 보고 Kotlin 코드의 이 부분을 짠다"를 명시
- SAP-1의 합성 datasheet를 책에서 직접 제공 — 학습자가 "공식 명세 → 코드"의 흐름을 체화

> "Reading a microcontroller datasheet is a skill that improves with practice. Over time, you will develop the ability to pick up any new microcontroller and get it running quickly because all datasheets follow the same patterns." [웹-자료]

### 5.7 단계적 학습 곡선 설계

[커뮤니티-패턴2, 휴리스틱1,2]

본 책의 14 챕터 안배 권장:
1. **챕터 1~2:** von Neumann + fetch-decode-execute + Kotlin 미니 Chip-8 (워밍업, 며칠 안에 끝나는 첫 성취)
2. **챕터 3~5:** SAP-1 단계적 구현 (클록 → 레지스터 → ALU → RAM → 버스 → IR → 컨트롤러)
3. **챕터 6:** SAP-1 어셈블러/디스어셈블러
4. **챕터 7~8:** SAP-2 진화 (메모리 확장, JMP/CALL/RET, I/O, 마이크로코드 ROM)
5. **챕터 9~11:** 8비트 RISC (load/store ISA, 고정 길이 명령어, 5-stage pipeline 모사)
6. **챕터 12:** 실제 8비트 CPU 비교 (8080/Z80/6502/8086 어드레싱 모드, 어셈블리 차이 표)
7. **챕터 13:** instruction-accurate → cycle-accurate 리팩토링
8. **챕터 14:** 향후 청사진 (CPU → 메모리 시스템 → I/O 디바이스 → 인터럽트 → 커널 → OS)

추가 옵션: 부록 — 한국어 컴퓨터구조 학습 자료 큐레이션 (한국어 공백 채우기 [커뮤니티-패턴7]).

### 5.8 페다고지 메타 코멘트 활용

[커뮤니티 후기·인생 변화 발언 모음]

본 책은 챕터 오프닝/메타 코멘트에서 다음 류 발언을 활용 가능:
- "It's pretty amazing to see it all come together and work in the end."
- "This is what really made it click."
- "How does the COMPUTER know what to do?"

이런 감정 표현이 본 책의 "토비 문체" (평어체 + 청유형 + 수사적 질문)와 자연스럽게 어울린다.

---

## 6. 참고문헌

### 6.1 표준 교과서 (인용 핵심)

- **Malvino, A. P., & Brown, J. A. (1993).** *Digital Computer Electronics* (3rd ed.). McGraw-Hill. ISBN 9780028005942.
  → SAP-1/SAP-2/SAP-3 원전. 본 책의 단계적 확장 골격의 직접 출처.
- **Patterson, D. A., & Hennessy, J. L. (2020).** *Computer Organization and Design (MIPS Edition)* (6th ed.). Morgan Kaufmann. ISBN 9780128201091.
  → 학부 컴퓨터 아키텍처 표준 교과서. 40,000+ 학생/년. 8비트 RISC 챕터의 datapath/pipelining 모델 원천.
- **Hennessy, J. L., & Patterson, D. A. (2017).** *Computer Architecture: A Quantitative Approach* (6th ed.). Morgan Kaufmann. ISBN 9780128119051.
  → DLX → RISC-V로 5판부터 전환. 정량 비교 페다고지의 원전.
- **Tanenbaum, A. S., & Austin, T. (2024).** *Structured Computer Organization* (6th ed.). Pearson. ISBN 9780137618446.
  → "computer as hierarchy of levels" 페다고지. 본 책 학습 청사진의 직계 후예.
- **Nisan, N., & Schocken, S. (2021).** *The Elements of Computing Systems* (2nd ed.). MIT Press. ISBN 9780262539807.
  → nand2tetris 정전. 본 책 페다고지 모델.
- **Nystrom, R. (2021).** *Crafting Interpreters*. genever benning. https://craftinginterpreters.com/
  → 두 번 구현 페다고지의 직접 영감원.
- **Bryant, R. E., & O'Hallaron, D. R. (2015).** *Computer Systems: A Programmer's Perspective* (3rd ed.). Pearson. ISBN 9780134092669. https://csapp.cs.cmu.edu/
  → "programmer's perspective" 철학.

### 6.2 핵심 학술 논문

- **von Neumann, J. (1945).** *First Draft of a Report on the EDVAC.* https://web.mit.edu/sts.035/www/PDFs/edvac.pdf
- **Patterson, D. A., & Ditzel, D. R. (1980).** The case for the reduced instruction set computer. *ACM SIGARCH Computer Architecture News*, 8(6), 25–33. DOI: 10.1145/641914.641917
- **Radin, G. (1983).** The 801 minicomputer. *IBM Journal of Research and Development*, 27, 237–246. DOI: 10.1147/rd.273.0237
- **Hennessy, J. L., Jouppi, N., et al. (1982).** MIPS: A microprocessor architecture. *ACM SIGMICRO Newsletter* (MICRO-15).
- **Clark, D. W., & Strecker, W. D. (1980).** Comments on "The Case for the Reduced Instruction Set Computer." *ACM SIGARCH Computer Architecture News*, 8(6). DOI: 10.1145/641914.641918
- **Amdahl, G. M. (1967).** Validity of the single-processor approach to achieving large-scale computing capabilities. *AFIPS Conference Proceedings*, 30, 483–485. DOI: 10.1145/1465482.1465560
- **Hennessy, J. L., & Patterson, D. A. (2019).** A new golden age for computer architecture. *Communications of the ACM*, 62(2), 48–60. DOI: 10.1145/3282307
- **Schocken, S., & Nisan, N. (2024).** Nand to Tetris: Building a modern computer system from first principles. *Communications of the ACM*, 67(5). DOI: 10.1145/3626513
- **Yurcik, W., & Mary, J. (2001).** Teaching computer organization/architecture with limited resources using simulators. *ACM SIGCSE Bulletin*, 33. DOI: 10.1145/563517.563408
- **(2024).** Teaching computer architecture by designing and simulating processors from their bits and bytes. *PeerJ Computer Science*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10909196/
- **(2024).** Further Evaluations of a Didactic CPU Visual Simulator (CPUVSIM). arXiv:2411.05229
- **Giorgi, R., & Mariotti, G. (2019).** WebRISC-V: a Web-Based Education-Oriented RISC-V Pipeline Simulation Environment. WCAE 2019. DOI: 10.1145/3338698.3338890

### 6.3 웹 자료 (1차 1차 참조)

#### CPU 아키텍처
- Simple-As-Possible computer — https://en.wikipedia.org/wiki/Simple-As-Possible_computer
- Austin Morlan, *Building an FPGA Computer: SAP-2* — https://austinmorlan.com/posts/fpga_computer_sap2/
- dangrie158, *SAP-1 Processor Architecture* — https://dangrie158.github.io/SAP-1/
- Ben Eater, *Build an 8-bit computer* — https://eater.net/8bit
- nand2tetris — https://www.nand2tetris.org/
- LC-3 — https://en.wikipedia.org/wiki/Little_Computer_3

#### 실제 8비트 CPU
- MOS Technology 6502 — https://en.wikipedia.org/wiki/MOS_Technology_6502
- Chip Hall of Fame: MOS Technology 6502 (IEEE Spectrum) — https://spectrum.ieee.org/chip-hall-of-fame-mos-technology-6502-microprocessor
- Intel 8080 — https://en.wikipedia.org/wiki/Intel_8080
- Intel 8086 — https://en.wikipedia.org/wiki/Intel_8086
- Zilog Z80 — https://en.wikipedia.org/wiki/Zilog_Z80

#### Kotlin/JVM emulators
- ksim65 (Kotlin 6502/65C02) — https://github.com/irmen/ksim65
- kNES (Kotlin NES) — https://github.com/ArturSkowronski/kNES
- Scuffed-6502Kt (Kotlin 학습용 6502) — https://github.com/barrettotte/Scuffed-6502Kt
- 6502Android (Kotlin) — https://github.com/felipecsl/6502Android
- chip-8 (Kotlin, Cédric Beust) — https://github.com/cbeust/chip-8

#### Kotlin 비트 처리
- Kotlin Unsigned Integer Types — https://kotlinlang.org/docs/unsigned-integer-types.html
- KEEP-unsigned-types — https://github.com/Kotlin/KEEP/blob/master/proposals/unsigned-types.md

#### 페다고지·튜토리얼
- Tobias Langhoff, *Guide to making a CHIP-8 emulator* — https://tobiasvl.github.io/blog/write-a-chip-8-emulator/
- emudev.org getting started — https://emudev.org/getting_started
- awesome-emu-resources — https://github.com/marethyu/awesome-emu-resources
- 6502.org tutorials — https://6502.org/tutorials/vflag.html
- Ken Shirriff, *The 6502 overflow flag explained mathematically* — http://www.righto.com/2012/12/the-6502-overflow-flag-explained.html
- mGBA, *Emulation Accuracy, Speed, and Optimization* — https://mgba.io/2017/04/30/emulation-accuracy/

#### 한국어 자료
- POCU 아카데미, 어셈블리 프로그래밍 — https://pocu.academy/ko/Courses/COMP2300
- 나무위키, 모스 테크놀로지 6502 — https://namu.wiki/w/모스%20테크놀로지%206502
- 위키백과, 자일로그 Z80 — https://ko.wikipedia.org/wiki/자일로그_Z80
- ned3y2k, 8086 프로세서 어셈블리 — https://ned3y2k.co.kr/entry/8086-프로세서-어셈블리-프로그래밍
- 한빛 출판사, 컴퓨터 구조와 운영체제를 알아야 하는 이유 — https://hongong.hanbit.co.kr/컴퓨터-구조와-운영체제를-알아야-하는-이유/

### 6.4 커뮤니티 토론

- Hacker News, Ben Eater 8-bit (2024) — https://news.ycombinator.com/item?id=43533715
- Hacker News, Ben Eater 시리즈 토론 — https://news.ycombinator.com/item?id=31098130
- Hacker News, nand2tetris (2024) — https://news.ycombinator.com/item?id=38735066
- Hacker News, Crafting Interpreters 리뷰 — https://news.ycombinator.com/item?id=31835818
- NESdev forum, "Emulation, where to start?" — https://forums.nesdev.org/viewtopic.php?t=4352
- NESdev forum, "Understanding overflow flag for ADC on the 6502" — https://forums.nesdev.org/viewtopic.php?t=6331
- 6502.org forum, Carry & Overflow Flags — http://forum.6502.org/viewtopic.php?t=62
- OKKY, 컴퓨터구조 학습 자료 요청 — https://okky.kr/articles/678731
- velog, 면접 컴퓨터구조 — https://velog.io/@co_mong/면접-컴퓨터구조
- Kotlin Slack archive, bitshifting bytes — https://slack-chats.kotlinlang.org/t/474212/

---

## 7. 리서치 한계

### 7.1 커버하지 못한 영역

- **Malvino *Digital Computer Electronics* 원서 본문**: SAP-1/SAP-2의 정확한 명령어 인코딩(LDA = `0000`, ADD = `0001` 같은 4비트 opcode 매핑), 마이크로코드 시퀀스 정확값은 원서를 직접 펴봐야 한다. 본 리서치에서는 Wikipedia + Austin Morlan FPGA 후기 + dangrie158 문서로 보강했다. 본 책 저술 시 원서 한 권은 반드시 옆에 둘 것.
- **Patterson & Ditzel 1980 RISC 논문 본문 직접 인용**: PDF가 WebFetch에서 binary로 잡혀 핵심 문장 직접 인용 실패. Wikipedia/Semantic Scholar로 메타데이터·요약을 보강했지만, 책에 직접 인용할 핵심 문장은 도서관 접근 또는 ACM Digital Library로 재확인 권고.
- **8086/Z80 어셈블리의 정량 코드 예제**: 본 리서치는 비교 표 수준에서 멈췄다. 본 책의 챕터 12에서 같은 "Fibonacci 계산"을 8080/6502/Z80/8086 어셈블리로 각각 짠 코드 예제는 별도 자료(Wikibooks Z80 Assembly, masswerk 6502, Steve Morse 8086) 또는 직접 작성.
- **cycle-accurate 8비트 emulator의 학술 서베이 부재**: peer-reviewed survey가 사실상 없다 — 커뮤니티 자료(mGBA blog, byuu/Near의 글)가 사실상 표준. 본 책의 cycle-accurate 챕터는 학술적 권위보다는 실무 구현자 합의로 정당화해야 한다.
- **8비트 RISC ISA의 구체 설계**: "8비트 RISC"는 본 책 고유의 합성 ISA가 될 것 — 직접 영감원이 될 만한 완전한 사례가 없다 (RV32E 같은 32비트 임베디드 RISC-V는 있지만 8비트는 아니다). 본 책 챕터 9~11에서 ISA를 직접 설계해야 하며, 이 설계가 본 책의 가장 창의적인 산물이 될 것.
- **한국어 1차 자료**: 한국 개발자가 "Kotlin으로 8비트 CPU를 만들었다"는 후기 자료는 거의 없다. 본 책 출간 자체가 한국어 시장 공백을 채우는 가치 — 동시에 본 책에서 인용 가능한 한국어 후기·일화 빈약을 의미한다. 본 책에서는 영어 커뮤니티 발언을 번역·인용하거나, 한국 컴퓨터구조 학습 일반 자료(OKKY, velog, 나무위키)에서 정황 인용으로 메운다.

### 7.2 검증 필요 항목

- Kotlin Slack 토론 본문 (`#getting-started` 채널의 "Bitshifting for bytes is not supported"): 검색 메타데이터로만 확인, 원문 본문은 429 에러로 미접근. 본 책에 직접 인용하기 전 원문 확인.
- "RISC가 단순 명령어 90% 사용에 근거한다"는 Patterson 1980 핵심 주장: Wikipedia/Berkeley 강의 노트로 보강했지만 원문 직접 인용 미확보.
- 한국 학부 컴퓨터구조 강의의 구체적 페다고지 실패 패턴: 추정 수준. 별도 검증 (한국 컴퓨터구조 교수 인터뷰, KIISE 논문) 권장.

### 7.3 리서치 활용 권고

- 본 레퍼런스 문서는 책의 14 챕터를 채울 1차 자료 큐레이션이다. 책 본문 저술 시:
  1. 각 챕터 도입부의 "공감 포인트"는 §2 (관점)와 §4 (논쟁), 커뮤니티 후기에서 가져온다.
  2. 정의·역사적 사실은 §1 (개념)과 §3 (사례)에서, 출처 표기 필수.
  3. 코드 패턴은 §5 (실무 적용 팁) + ksim65/kNES 소스 직접 확인.
  4. 정량 비교 표 (§3.3)는 본 책의 챕터 12 시각화 자료로 그대로 활용 가능.
- 본 책은 SAP-1 → SAP-2 → 8비트 RISC 라인을 점진적으로 다루는 **시장 공백을 채우는 위치**다. nand2tetris(추상 게이트)와 Ben Eater(실물 칩) 사이에 정확히 자리 잡는다.
