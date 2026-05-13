# 웹 리서치: Kotlin으로 8비트 CPU 시뮬레이터(SAP-1/SAP-2/RISC) 구현 학습서

수집 일시: 2026-05-13. 슬러그: `kotlin-8bit-cpu`. 대상 독자: Kotlin/Java 중급 개발자.

대상 독자가 한국 개발자라 한국어 자료를 일부 포함했으나, 8비트 CPU 자료의 절대 다수가 영어권에 있어 영어 70%, 한국어 30% 비율로 수집.

---

## 자료 1: Simple-As-Possible Computer (Wikipedia)

- 출처: https://en.wikipedia.org/wiki/Simple-As-Possible_computer
- 저자·날짜: Wikipedia contributors, 지속 갱신
- 신뢰성: 중 (1차 출처는 Malvino & Brown 1993 textbook)
- 핵심 주장: SAP는 Malvino & Brown의 *Digital Computer Electronics* (1993)에서 교육용으로 설계된 von Neumann 컴퓨터. SAP-1은 8비트 데이터, 4비트 어드레스, 16바이트 RAM, 5개 명령어(LDA, ADD, SUB, OUT, HLT)로 가장 단순한 구성. SAP-3에 이르면 Intel 8080/8085 ISA와 상위 호환된다.
- 인용 가능한 구절:
  > "The ISA is patterned after and upward compatible with the ISA of the Intel 8080/8085 microprocessor family."
  > "Capable of adding and subtracting 8-bit 2's complement integers" with flags for zero (Z) and carry (C).
- 관련 섹션: §1 개념·정의 (SAP 정의), §3 대표 사례 (역사적 위치)

## 자료 2: Building an FPGA Computer: SAP-2 (Austin Morlan 블로그)

- 출처: https://austinmorlan.com/posts/fpga_computer_sap2/
- 저자·날짜: Austin Morlan, 블로그
- 신뢰성: 최상 (실제 FPGA 구현 기록, 작성자가 결정 근거를 명시)
- 핵심 주장: SAP-1 → SAP-2 전환은 단순한 명령어 추가가 아니라 마이크로아키텍처의 근본 재설계. 메모리 16바이트 → 64K, 명령어 8개 → 39개, 누산기 1개 → 범용 레지스터 3개(A/B/C), 컨트롤러가 조합 논리 → ROM 기반 마이크로코드로 진화. SAP-2 ISA는 Intel 8080 subset.
- 인용 가능한 구절:
  > "Where SAP-1 had one accumulator, SAP-2 introduces three general-purpose registers (A, B, C)."
  > "With 35 control signals and 10 T-states maximum, hand-coding became impractical."
  > "If you find the architecture of this version to be highly awkward and strange, we are in agreement." — SAP-2의 설계 비일관성에 대한 솔직한 평
  > "A function cannot call another function or else the return address will be overwritten" — SAP-2 한계, SAP-3에서 해결
- 관련 섹션: §1 (SAP-2 구조), §2 (CISC적 진화 관점), §4 (교육용 ISA의 타협)

## 자료 3: SAP-1 Processor Architecture documentation (dangrie158)

- 출처: https://dangrie158.github.io/SAP-1/
- 저자·날짜: dangrie158, GitHub Pages 문서
- 신뢰성: 최상 (실제 모듈별 구현 코드/회로 동봉)
- 핵심 주장: SAP-1은 ~400 Hz 클록, 8비트 데이터 버스, 5개 마이크로스텝, 16비트 control word로 동작. 핵심 모듈: 클록, A·B 레지스터, ALU(가산/감산 + Z·C 플래그), 4비트 PC, 16바이트 RAM, MAR, 명령어 레지스터(opcode/operand 분리), 명령어 디코더. 마이크로코드 시퀀스가 EEPROM lookup table로 구현된다.
- 인용 가능한 구절:
  > "5 microsteps, managing 16 bytes of RAM via a 16-bit control word"
  > "Instruction register splitting opcodes and parameters" — 8비트 명령어를 4비트 opcode + 4비트 operand로 분할
- 관련 섹션: §1 (SAP-1 마이크로아키텍처), §5 (실무 구현 팁)

## 자료 4: Build an 8-bit computer | Ben Eater

- 출처: https://eater.net/8bit
- 저자·날짜: Ben Eater, 진행 중 시리즈
- 신뢰성: 최상 (가장 영향력 있는 8비트 CPU 교육 콘텐츠)
- 핵심 주장: 브레드보드와 74LS 시리즈 IC만으로 SAP-1 변형을 만드는 YouTube + 웹 시리즈. 모듈 순서: 클록 → 레지스터 → ALU → RAM → PC → 출력 → 버스 → 컨트롤 로직. "fully programmable 8-bit computer from simple logic gates"라는 슬로건이 핵심.
- 인용 가능한 구절:
  > "Build a fully programmable 8-bit computer from simple logic gates on breadboards"
- 관련 섹션: §3 (대표 사례 — Ben Eater 효과), §5 (학습 경로 추천)

## 자료 5: 8-bit SAP-1 Breadboard Computer (Raghav Marwah)

- 출처: https://raghavmarwah.com/blog/8-bit-computer/
- 저자·날짜: Raghav Marwah, 블로그
- 신뢰성: 중
- 핵심 주장: Ben Eater 디자인을 직접 따라 만든 후기. 사람들이 실제로 부딪히는 빌드 함정과 학습 효과 정리. "이론을 이해하는 것과 직접 손으로 만드는 것 사이에 거대한 격차가 있다"는 일관된 회고가 등장 (커뮤니티 자료에서도 반복됨).
- 관련 섹션: §3 (사례), §5 (시뮬레이션 vs 실물 빌드의 학습 가치)

## 자료 6: nand2tetris Hack CPU (공식 사이트 + Coursera)

- 출처: https://www.nand2tetris.org/project05 ; https://www.coursera.org/learn/build-a-computer
- 저자·날짜: Noam Nisan, Shimon Schocken, 공식 코스
- 신뢰성: 최상
- 핵심 주장: nand2tetris의 Hack 컴퓨터는 16비트 Harvard 아키텍처 (명령어/데이터 메모리 분리). 16K RAM, 메모리 매핑된 스크린/키보드. NAND 게이트만으로 시작해 CPU → 어셈블러 → 가상머신 → 컴파일러 → OS → Tetris까지 쌓아 올리는 12 프로젝트 코스. "build it yourself, no shortcuts"가 교수법의 핵심.
- 인용 가능한 구절:
  > "Build a Modern Computer from First Principles: From Nand to Tetris"
  > "Harvard architecture - separate instruction and data memories"
- 관련 섹션: §3 (유사 교육 시스템), §5 (CPU 이후 OS까지 학습 경로)

## 자료 7: ksim65 — Kotlin 6502 simulator (irmen)

- 출처: https://github.com/irmen/ksim65
- 저자·날짜: Irmen de Jong, MIT 라이선스
- 신뢰성: 최상 (Kotlin/JVM으로 6502를 본격 구현한 가장 성숙한 사례)
- 핵심 주장: Kotlin으로 6502/65C02 전체 명령어(불법 명령어, BCD 포함)를 구현. 모듈식 — 버스, CPU, 메모리, I/O 컨트롤러를 분리. 명령어 주기 시간만 시뮬레이션하고 cycle-exact는 일부러 포기 ("for simplicity reasons"). 실제 C-64 ROM을 돌리는 데모 포함.
- 인용 가능한 구절:
  > "Kotlin/JVM library that simulates the 8-bit 6502 and 65C02 microprocessors... includes a fairly functional C64 emulator running actual roms"
  > 의도적으로 사이클 정확도를 포기 — "simplicity reasons"
- 관련 섹션: §3 (Kotlin emulator 레퍼런스 구현), §4 (정확도 vs 단순성 트레이드오프), §5 (구현 패턴)

## 자료 8: Scuffed-6502Kt (barrettotte)

- 출처: https://github.com/barrettotte/Scuffed-6502Kt
- 저자·날짜: Brett Otte, 학습 프로젝트
- 신뢰성: 중 (자체적으로 "scuffed"라고 표시)
- 핵심 주장: "Kotlin과 6502 아키텍처를 함께 배우려는" 자기학습 프로젝트. 본 책의 대상 독자(중급 Kotlin 개발자)와 거의 동일한 출발선의 사례. 코드 양이 작고 깔끔해 입문 레퍼런스로 적합.
- 관련 섹션: §3 (학습용 Kotlin 구현 레퍼런스)

## 자료 9: kNES — Kotlin NES emulator (ArturSkowronski)

- 출처: https://github.com/ArturSkowronski/kNES
- 저자·날짜: Artur Skowronski (Kotlin 커뮤니티 인플루언서)
- 신뢰성: 최상 (Java vNES emulator를 Kotlin으로 포팅한 교육용 프로젝트)
- 핵심 주장: 56개 official opcode + cycle-accurate 구현. Kotlin 코드 스타일이 Kotlinic — `when` 디스패치, 데이터 클래스, sealed class 활용. 본 책의 "Kotlin 답게 짜기" 챕터의 직접 레퍼런스.
- 관련 섹션: §3 (대표 사례), §5 (Kotlin 관용 패턴)

## 자료 10: Kotlin Unsigned Integer Types (공식 문서)

- 출처: https://kotlinlang.org/docs/unsigned-integer-types.html ; https://github.com/Kotlin/KEEP/blob/master/proposals/unsigned-types.md
- 저자·날짜: JetBrains, Kotlin 1.5+ stable
- 신뢰성: 최상 (공식 문서)
- 핵심 주장: Kotlin 1.5부터 `UByte` (0..255), `UShort` (0..65535), `UInt`, `ULong` 정식 stable. inline class로 구현되어 JVM에서 primitive로 컴파일 — overhead 거의 없음. 단, UByte/UShort의 비트 시프트는 미구현 상태("under consideration").
- 인용 가능한 구절:
  > "There is no significant overhead when using unsigned integer types on the JVM"
  > "Under the covers, all of the unsigned types in Kotlin are implemented as inline classes"
  > "Bit shifts are provided only for UInt and ULong; for the narrower types, both for signed and unsigned, they are under consideration"
- 관련 섹션: §5 (실무 적용 팁 — Kotlin 비트 처리 결정), §4 (UByte vs Int 어느 쪽으로 8비트 값을 표현할 것인가)

## 자료 11: Z80 instruction set & history (Wikipedia)

- 출처: https://en.wikipedia.org/wiki/Zilog_Z80 ; https://en.wikipedia.org/wiki/Z80_instruction_set
- 저자·날짜: Wikipedia contributors
- 신뢰성: 최상
- 핵심 주장: Z80은 1976년 Zilog 출시. 8080 명령어와 binary 호환. 추가: IX/IY 인덱스 레지스터 + 대체 레지스터 셋(AF', BC', DE', HL'), DD/FD prefix로 어드레싱 모드 확장, 비트 조작 명령어, 블록 전송(LDIR/LDDR). 적용처: TRS-80, ZX Spectrum, Amstrad CPC, MSX, ColecoVision, Sega Master System/Game Gear, Pac-Man 아케이드, 그리고 **Game Boy(Sharp LR35902, Z80 변형)**.
- 인용 가능한 구절:
  > "The Z80 was designed to be upward binary compatible with the Intel 8080"
  > "Nintendo's Game Boy and Game Boy Color handheld game systems used a Z80 clone manufactured by Sharp Corporation, which had a slightly different instruction set"
- 관련 섹션: §3 (Z80 영향력), §6 비교 표 데이터

## 자료 12: MOS Technology 6502 (Wikipedia + IEEE Spectrum + Commodore.ca)

- 출처: https://en.wikipedia.org/wiki/MOS_Technology_6502 ; https://spectrum.ieee.org/chip-hall-of-fame-mos-technology-6502-microprocessor ; https://harlepengren.com/6502-chip-that-powered-a-revolution/
- 저자·날짜: 다수
- 신뢰성: 최상
- 핵심 주장: 6502는 1975년 Chuck Peddle & Bill Mensch 설계, $25 (8080은 $179~$360). 트랜지스터 약 3,510개로 동시대 CPU의 절반. 레지스터 3개(A/X/Y) + SP/PC/P. 13개 어드레싱 모드, 56개 official opcode. 적용처: Apple II, Commodore PET/VIC-20/C64, Atari 2600(6507), Atari 8-bit, BBC Micro, Acorn Atom, Apple Lisa의 일부, NES(Ricoh 2A03/2A07 — BCD 제거, APU 통합).
- 인용 가능한 구절:
  > "The 8-bit 6502 was a smash hit from the get-go when it was released in 1975, due to its low price. The 6502 was sold for just $25"
  > "The Apple II put computing in schools. The Commodore 64 put it in living rooms. The NES made it entertainment for an entire generation."
  > "The 65C02, a low-power CMOS variant, is still in production and used in embedded systems today"
- 관련 섹션: §3 (6502 영향력 — 산업 혁명), §6 비교 표

## 자료 13: Intel 8080 (Wikipedia)

- 출처: https://en.wikipedia.org/wiki/Intel_8080
- 저자·날짜: Wikipedia contributors
- 신뢰성: 최상
- 핵심 주장: 1974년 4월 출시, 4,500~6,000 트랜지스터, 2~3.125 MHz, 8비트 데이터/16비트 어드레스(64KB). 레지스터: A, B, C, D, E, H, L (7개 8비트, BC/DE/HL 쌍으로 16비트 사용), SP, PC. 약 244개 명령어. Altair 8800, CP/M의 타깃 CPU. x86 계보의 시조.
- 인용 가능한 구절:
  > "Introduced in April 1974... 4,500-6,000 transistors, 2-3.125 MHz, 6 μm NMOS"
  > "Seven 8-bit registers (A, B, C, D, E, H, L) usable individually or as three 16-bit pairs (BC, DE, HL), plus a 16-bit stack pointer and program counter"
  > "Approximately 244 instructions"
- 관련 섹션: §3 (8080의 계보적 중요성), §6 비교 표

## 자료 14: Intel 8086 (Wikipedia)

- 출처: https://en.wikipedia.org/wiki/Intel_8086
- 저자·날짜: Wikipedia contributors
- 신뢰성: 최상
- 핵심 주장: 1978년 출시. 8080의 16비트 확장. 세그먼트 레지스터(CS/DS/SS/ES) + 16비트 오프셋으로 20비트 물리 주소 = 1MB. "8비트의 16비트 후계"라는 책의 비교 대상으로 정확히 맞는 위치. 어셈블리는 8080과 유사하지만 binary 비호환.
- 인용 가능한 구절:
  > "Fully 16-bit extension of Intel's 8-bit 8080 microprocessor, with memory segmentation as a solution for addressing more memory than can be covered by a plain 16-bit address"
  > "The complete physical address which is 20 bits long is generated using segment and offset registers, each 16 bit long"
- 관련 섹션: §3 (8080 → 8086 계보), §6 비교 표

## 자료 15: Fetch-Execute Cycle (Baeldung CS)

- 출처: https://www.baeldung.com/cs/fetch-execute-cycle
- 저자·날짜: Baeldung, 갱신 중
- 신뢰성: 중상
- 핵심 주장: fetch-decode-execute 사이클의 표준 설명. PC → MAR → memory read → MDR → CIR → decode → execute. "John von Neumann이 처음 도입"이라는 역사적 맥락 제공. 챕터 2 (von Neumann 아키텍처) 도입부에 그대로 활용 가능.
- 인용 가능한 구절:
  > "The Fetch-Execute cycle... was first introduced by John von Neumann. This cycle starts when the computer is turned on and keeps repeating until the computer is shut down."
- 관련 섹션: §1 (von Neumann 사이클)

## 자료 16: RISC vs CISC (Stanford SOCO + Wikipedia)

- 출처: https://cs.stanford.edu/people/eroberts/courses/soco/projects/risc/risccisc/ ; https://en.wikipedia.org/wiki/Reduced_instruction_set_computer
- 저자·날짜: Stanford CS151 SOCO project ; Wikipedia
- 신뢰성: 최상
- 핵심 주장: RISC 핵심 — load/store 아키텍처(메모리 접근은 LD/ST만), 고정 길이 명령어, 단일 사이클 실행 목표, 큰 레지스터 파일, 파이프라이닝 친화적. CISC — 가변 길이, 메모리 직접 연산, 마이크로코드. RISC의 핵심 통찰: "compiler가 영리하다면 단순한 명령어로도 짧은 코드를 만들 수 있다."
- 인용 가능한 구절:
  > "RISC simplifies processor design by using a small, uniform set of instructions where each instruction performs a basic operation (e.g., load, compute, store) and is designed to execute in a single clock cycle"
  > "Only load and store instructions interact with memory, while all other operations occur between registers"
  > "RISC reduces the cycles per instruction at the cost of the number of instructions per program, while CISC attempts to minimize the number of instructions per program but at the cost of an increase in the number of cycles per instruction"
- 관련 섹션: §1 (RISC 정의), §4 (RISC vs CISC 논쟁), §5 (8비트 RISC 챕터의 핵심 가이드)

## 자료 17: LC-3 (Wikipedia)

- 출처: https://en.wikipedia.org/wiki/Little_Computer_3
- 저자·날짜: Wikipedia
- 신뢰성: 최상
- 핵심 주장: Yale Patt & Sanjay Patel이 *Introduction to Computing Systems* (McGraw-Hill, 2003) 교재용으로 설계. 16비트, R0~R7 (8개 레지스터), 4비트 opcode (15개 명령어 사용), trap instruction으로 시스템 콜 모사. C 컴파일러 타깃 가능. SAP보다 약간 더 풍부한 교육용 ISA.
- 인용 가능한 구절:
  > "Simplified 16-bit educational computer architecture and assembly language designed to teach the fundamentals of computer organization, digital logic, and low-level programming"
  > "Eight registers, referred to by number as R0 through R7"
  > "Instructions are 16 bits wide and have 4-bit opcodes"
- 관련 섹션: §3 (다른 교육용 ISA), §1 (SAP 외 비교 대상)

## 자료 18: Chip-8 Emulator in Kotlin (Cedric Beust)

- 출처: https://github.com/cbeust/chip-8 ; https://www.beust.com/weblog/a-chip-8-emulator-written-in-kotlin/
- 저자·날짜: Cédric Beust (TestNG 창시자)
- 신뢰성: 최상 (저자 인지도 높음, 블로그에 학습 과정 기록)
- 핵심 주장: Chip-8은 "emulator dev 입문의 hello world." Kotlin으로 짜는 데 며칠 정도. 명령어 35개, 4KB 메모리, 64x32 단색 디스플레이. 본격 8비트 CPU(6502/Z80) 시뮬레이터 짓기 전 워밍업으로 권장. *"emudev 커뮤니티가 모두 Chip-8부터 시작하라고 외친다"* (자료 21 emudev.org와 일치).
- 관련 섹션: §3 (Kotlin 학습 곡선 사례), §5 (단계별 학습 권장 경로)

## 자료 19: Crafting Interpreters (Robert Nystrom)

- 출처: https://craftinginterpreters.com/
- 저자·날짜: Robert Nystrom (Google 컴파일러 엔지니어), 2021
- 신뢰성: 최상 (해당 분야 최고 평가 입문서)
- 핵심 주장: 동일 언어 Lox를 두 번 구현한다 — 먼저 Java로 tree-walking interpreter, 다음 C로 bytecode VM. 챕터마다 모든 라인을 보여주며 점진적으로 쌓아 올리는 방식이 본 책의 "SAP-1 → SAP-2 → RISC" 점진 전개의 직접 영감원. 본 책의 페다고지 모델로 인용 가능.
- 인용 가능한 구절:
  > "This dual implementation strategy isn't just a structural gimmick. It serves a deep pedagogical purpose, allowing readers to first grasp the conceptual architecture of language processing in a high-level language before rebuilding everything from raw memory and pointer arithmetic"
  > "One of the best programming books published in recent years. It takes a subject that most programmers consider forbiddingly complex and renders it not just comprehensible but engaging."
- 관련 섹션: §5 (페다고지 모델), §3 (영향력 있는 자기학습형 시스템 책)

## 자료 20: Cycle-accurate vs Instruction-accurate (mGBA + Emulation Wiki)

- 출처: https://mgba.io/2017/04/30/emulation-accuracy/ ; https://emulation.gametechwiki.com/index.php/Emulation_Accuracy
- 저자·날짜: endrift (mGBA 저자) ; 위키 contributors
- 신뢰성: 최상 (실제 cycle-accurate 에뮬레이터 저자의 글)
- 핵심 주장: Cycle-accurate = 매 클록 사이클마다 하드웨어와 동일한 상태. Instruction-accurate = 명령어 종료 시점만 정확. 8비트 CPU(NES, Game Boy)는 PPU/APU와 타이밍 의존성이 강해 cycle-accurate가 필수에 가깝지만 성능 비용이 크다. Game Boy는 M-cycle(4 T-cycle) 단위로 추상화하면 정확도와 성능의 좋은 절충.
- 인용 가능한 구절:
  > "Cycle accuracy means that every single aspect of the emulated system occurs at the correct time relative to everything else"
  > "1 M-cycle = 4 T-cycles. CPU instructions are usually measured in M-cycles, and emulators that simulate only M-cycles group all four T-cycles into a single unit of work, which simplifies execution but may obscure timing-sensitive behavior"
- 관련 섹션: §4 (정확도 트레이드오프), §5 (8비트 시뮬레이터 실무 선택)

## 자료 21: EmuDev 입문 로드맵 (emudev.org)

- 출처: https://emudev.org/getting_started ; https://github.com/marethyu/awesome-emu-resources
- 저자·날짜: emudev 디스코드 커뮤니티 (큐레이션)
- 신뢰성: 최상 (커뮤니티 큐레이션의 가장 권위 있는 리스트)
- 핵심 주장: 권장 학습 곡선 — Chip-8 → Game Boy or NES → 본격 시스템. "Chip-8부터 시작" 권유. 6502는 NES emulator 학습으로 자연스럽게 이어진다. tobiasvl의 Chip-8 가이드(https://tobiasvl.github.io/blog/write-a-chip-8-emulator/)가 사실상 표준 입문서.
- 인용 가능한 구절:
  > "Most people start with a CHIP-8 emulator"
  > "After that, you can pretty much move to whatever system you want to. You don't have to 'work your way up' to it as many seem to think"
- 관련 섹션: §5 (학습 경로), §3 (커뮤니티 합의 학습 순서)

## 자료 22: 6502 Assembler 설계 (6502.org forum + Wikibooks)

- 출처: https://6502.org/forum/viewtopic.php?f=2&t=5153 ; https://en.wikibooks.org/wiki/6502_Assembly ; https://www.masswerk.at/6502/assembler.html
- 저자·날짜: 6502 커뮤니티 누적
- 신뢰성: 중상
- 핵심 주장: 2-pass 어셈블러 구조 — 1차 pass에서 명령어 길이/주소 결정 + 심볼 테이블 구축, 2차 pass에서 forward reference 해결 + 기계어 생성. 가변 길이 명령어가 있으면 3-pass도 필요. 본 책의 "어셈블러/디스어셈블러 구현" 챕터의 알고리즘 골격.
- 인용 가능한 구절:
  > "In a two-pass assembler, all the references of subroutine calls are tackled during the second pass, and this resolving of forward references and getting corresponding addresses associated with all subroutine calls is referred to as a resolution table"
- 관련 섹션: §5 (어셈블러 구현 가이드)

## 자료 23: Computer Organization and Design — MIPS Edition (Patterson & Hennessy)

- 출처: https://shop.elsevier.com/books/computer-organization-and-design-mips-edition/patterson/978-0-12-820109-1
- 저자·날짜: David Patterson, John Hennessy. 6판 (Elsevier/Morgan Kaufmann, 2020)
- 신뢰성: 최상 (학부 컴퓨터 아키텍처 표준 교과서)
- 핵심 주장: 단순화된 MIPS ISA로 datapath, control, pipelining, hazards, memory hierarchy를 강의. 40,000+ 학생/년이 사용. "RISC-V Edition"도 별도 존재. 8비트 RISC 챕터의 ISA 설계 가이드.
- 인용 가능한 구절:
  > "Used by more than 40,000 students per year"
- 관련 섹션: §3 (학술 레퍼런스), §1 (MIPS 단순화 모델)

## 자료 24: Computer Systems: A Programmer's Perspective (CSAPP, Bryant & O'Hallaron)

- 출처: https://csapp.cs.cmu.edu/
- 저자·날짜: Randal Bryant & David O'Hallaron, CMU (1998 코스 시작, 3판 2015)
- 신뢰성: 최상
- 핵심 주장: "builder's perspective" 대신 "programmer's perspective" — 컴퓨터를 설계하지 않더라도 그 동작을 알면 더 나은 프로그래머가 된다. 본 책의 대상 독자(애플리케이션 개발자)에게 정확히 맞는 페다고지 철학. 책 서문/머리말 인용 가치 있음.
- 인용 가능한 구절:
  > "Students should first learn about systems in terms of how they affect the behavior and performance of their programs—a 'programmer's perspective.'"
- 관련 섹션: §5 (책의 페다고지 설정), §1 (왜 시뮬레이터인가?)

## 자료 25: POCU 어셈블리 프로그래밍 강좌 (한국어)

- 출처: https://pocu.academy/ko/Courses/COMP2300
- 저자·날짜: POCU 아카데미, 박포프
- 신뢰성: 중상 (한국어권 어셈블리 교육의 대표 강좌)
- 핵심 주장: x86-16 (8086) 어셈블리어를 통해 컴퓨터 구조와 OS의 기초를 학습. 한국어권 개발자가 컴퓨터 구조에 다시 접근할 때 자주 추천되는 코스. 본 책의 "8086 비교" 챕터의 한국어 독자 친화 레퍼런스.
- 인용 가능한 구절:
  > "x86 계열 CPU의 시초인 Intel 8086/8088 CPU에서 x86-16 어셈블리어 코드를 작성... 하드웨어의 본질을 깊이 이해하고, 기초 컴퓨터 구조 및 운영체제의 세계를 완벽하게 습득"
- 관련 섹션: §6 한국어 학습 자원

## 자료 26: 모스 테크놀로지 6502 (나무위키, 한국어)

- 출처: https://namu.wiki/w/%EB%AA%A8%EC%8A%A4%20%ED%85%8C%ED%81%AC%EB%86%80%EB%A1%9C%EC%A7%80%206502
- 저자·날짜: 나무위키 contributors
- 신뢰성: 중
- 핵심 주장: 한국어로 정리된 6502 역사. 8080/Z80과의 정량 비교 (트랜지스터 ~3,500 vs 6,000, 가격 $25 vs $179). 한국 독자가 친숙해할 만한 적용처(NES = 패미컴) 강조.
- 인용 가능한 구절:
  > "6502는 총 6개의 레지스터로 8비트 A, X, Y, P, S와 16비트 프로그램 카운터를 가지고 있으며, 8비트 레지스터만으로 구성되어 있지만 16비트의 메모리를 다룰 수 있었습니다."
  > "트랜지스터 개수가 약 3천개 중반으로 동시대 프로세서에 비하면 절반밖에 안 되는 칩 크기"
- 관련 섹션: §3 (한국어 독자용 6502 정리), §6 비교 표

## 자료 27: 자일로그 Z80 (위키백과 한국어)

- 출처: https://ko.wikipedia.org/wiki/%EC%9E%90%EC%9D%BC%EB%A1%9C%EA%B7%B8_Z80
- 저자·날짜: 위키백과 contributors
- 신뢰성: 중상
- 핵심 주장: 한국어로 정리된 Z80. "8080의 개량형, 5V 단일 전원, 더 높은 클럭, 1980년대 중순까지 PC CPU"라는 한국 독자에게 친근한 설명. MSX 적용 강조 (한국에서 1980년대 인기).
- 관련 섹션: §3 (Z80 — 한국 독자 친숙도), §6

## 자료 28: CSAPP free PDF mirror

- 출처: https://www.cs.sfu.ca/~ashriram/Courses/CS295/assets/books/CSAPP_2016.pdf
- 저자·날짜: Bryant & O'Hallaron, 3rd ed. (강의 자료용 mirror)
- 신뢰성: 최상 (원본 PDF)
- 핵심 주장: 컴퓨터 시스템을 layered abstraction으로 설명 — 하드웨어 → 어셈블리 → C → 응용. 본 책의 학습 청사진(CPU → 메모리 → 버스 → I/O → 커널 → OS → 응용)이 이 layered view를 따라간다.
- 관련 섹션: §5 (학습 청사진의 이론적 근거)

---

## 수집 한계

- **접근 불가/제약:** Wikipedia SAP 페이지는 Ben Eater 설계 기반의 간략 정보만 제공, Malvino 원서의 정확한 명령어 인코딩(LDA = `0000`, ADD = `0001` 같은 4비트 opcode 매핑)은 직접 textbook을 봐야 한다. → §6 참고문헌에 textbook 인용으로 보강.
- **8-bit CPU 정량 비교 표:** bigmessowires 글이 정확한 트랜지스터 수/가격 표를 제공하지 않아 다른 출처(Wikipedia 각 CPU 페이지)에서 항목별로 모았다. 한 곳에 깔끔하게 정리된 비교 표가 부족 → 본 책에서 직접 표를 그려야 한다.
- **Kotlin 8비트 CPU 시뮬레이터의 실무 후기:** ksim65를 제외하면 본격 production 사례가 적다. 학습 프로젝트(Scuffed-6502Kt) 위주. → 커뮤니티 리서치에서 보강.
- **의도적 제외:** 광고성 "RISC vs CISC explained in 3 minutes" 류 짧은 SEO 글, 출처 불명 나열형 아티클.
- **한국어 자료의 깊이 부족:** 한국어 자료는 위키류 정리와 어셈블리 강좌 위주. 한국 개발자가 "직접 CPU 시뮬레이터를 만들었다"는 본격 블로그는 거의 잡히지 않음 → 커뮤니티 리서치(velog/OKKY)에서 추가 발굴 권장.
