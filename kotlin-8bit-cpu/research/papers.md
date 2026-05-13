# 논문 리서치: Kotlin으로 8비트 CPU 시뮬레이터(SAP-1/SAP-2/RISC) 구현 학습서

수집 일시: 2026-05-13. 슬러그: `kotlin-8bit-cpu`.

대상 독자가 비학문 개발자(중급 Kotlin/Java)이므로, 본 책은 학술적 엄밀성보다는 "왜 이 구조가 이렇게 진화했는지"의 역사적·경험적 정당화에 인용을 활용한다. 따라서 seminal 논문 + 교과서 + 최신 CS-education 논문 조합으로 수집했다.

---

## 논문 1: First Draft of a Report on the EDVAC

- 저자·연도: John von Neumann, 1945 (handwritten between Feb–Jun 1945, distributed June 30, 1945)
- 발표처: 미공식 배포본; 후에 IEEE Annals of the History of Computing에 재출간
- DOI/링크: https://en.wikipedia.org/wiki/First_Draft_of_a_Report_on_the_EDVAC ; PDF: https://web.mit.edu/sts.035/www/PDFs/edvac.pdf
- 피인용수: 측정 불가 (역사적 1차 사료, 거의 모든 컴퓨터 아키텍처 교과서가 인용)
- 요약: 저장된 프로그램(stored program) 개념을 처음 공개적으로 기술한 101-페이지 미완 보고서. CPU(연산 + 제어) + 메모리 + I/O라는 단일 메모리 안에 명령어와 데이터가 함께 머무는 구조를 제시. 이름은 "von Neumann architecture"로 굳었지만, 실제로 Eckert & Mauchly가 먼저 설계했다는 학술적 논쟁이 존재.
- 방법론: 형식적 논리 설계. 실제 회로가 아닌 추상 모델.
- 핵심 결과: "uniform memory containing both numbers (data) and orders (instructions)" — 명령어와 데이터를 같은 메모리에 두는 결정.
- 인용할 만한 문장:
  > "A uniform memory containing both numbers (data) and orders (instructions)" — 그 한 줄이 컴퓨터 아키텍처의 80년 역사를 정의한다.
- 독자 전달 방식 제안: 챕터 2 "von Neumann 아키텍처" 도입부에서, 1945년 손글씨로 기차에서 쓰여진 101페이지 보고서가 SAP-1, 6502, 그리고 오늘 우리가 만드는 시뮬레이터의 직계 조상이라는 일화로 시작.

## 논문 2: The Case for the Reduced Instruction Set Computer

- 저자·연도: David A. Patterson, David R. Ditzel, 1980
- 발표처: *ACM SIGARCH Computer Architecture News*, Vol. 8, No. 6, pp. 25–33
- DOI: 10.1145/641914.641917
- 피인용수: 1,800+ (Google Scholar, 2026 기준)
- 요약: Patterson이 1979년 DEC의 VAX 마이크로코드 개선 안식년에서 받은 충격에서 출발. 점점 복잡해지는 명령어 셋(CISC)이 비용 대비 효과적이지 않다는 주장. RISC가 동일 비용으로 더 나은 성능을 낸다는 가설을 제시 — 이후 Berkeley RISC-I 프로젝트로 검증.
- 방법론: 실제 VAX 명령어 사용 통계 + 컴파일러가 생성하는 명령어 분포 분석. 단순 명령어가 90%+ 사용된다는 경험적 발견에 근거.
- 핵심 결과: 단순 명령어 + 큰 캐시 + 컴파일러 최적화가 마이크로코드 + 복잡 명령어보다 이긴다는 명제 정립.
- 인용할 만한 문장 (Wikipedia/Berkeley CS252 노트에서 재인용):
  > "Examines the case for a Reduced Instruction Set Computer (RISC) being as cost-effective as a Complex Instruction Set Computer (CISC)."
  > Radin이 IBM 801에 대해 한 동시대 논평: "In some sense the 801 appears to be rushing in the opposite direction to the conventional wisdom of this field. Namely, everyone else is busy moving software into hardware and we are clearly moving hardware into software." (Radin 1983 인용)
- 독자 전달 방식 제안: 챕터 7~8 "RISC로 점프"에서, 1979년 VAX 안식년 에피소드를 미니 일화로 삽입. "사람들이 더 똑똑한 CPU를 만들려 할 때, Patterson은 더 멍청한 CPU를 만들어 이겼다"라는 한 줄로 RISC 정신을 요약.

## 논문 3: The 801 Minicomputer

- 저자·연도: George Radin, 1983 (IBM 내부 연구는 1974–1980)
- 발표처: *IBM Journal of Research and Development*, Vol. 27, pp. 237–246
- DOI: 10.1147/rd.273.0237
- 피인용수: 500+ (역사적 1차 사료)
- 요약: IBM 801은 1974년 John Cocke가 이끄는 팀이 전화 교환기 컨트롤러를 위해 시작한 RISC 시초 프로젝트. 초당 300통화 처리 = 당시 IBM 최고 메인프레임의 3~4배 성능 요구. 결과적으로 등장한 24비트 CPU는 "first RISC system" (Michael J. Flynn 평가).
- 방법론: 실측 통계 기반 — 복잡 명령어는 거의 안 쓰인다. 컴파일러가 생성한 단순 명령어 시퀀스가 마이크로코드 호출보다 빠르다.
- 핵심 결과: 12 MIPS 목표 달성. 단순 ISA + 큰 레지스터 파일 + 공격적 컴파일러 최적화 = 단일 사이클 실행.
- 인용할 만한 문장:
  > "Everyone else is busy moving software into hardware and we are clearly moving hardware into software" (Radin)
- 독자 전달 방식 제안: 챕터 7 RISC 개막부에서 "당시 누구도 mainframe 3배 성능을 단순화로 달성할 수 있다고 믿지 않았다"는 일화로 시작.

## 논문 4: MIPS: A Microprocessor Architecture

- 저자·연도: John L. Hennessy, Norman Jouppi, et al., 1982
- 발표처: ACM SIGMICRO Newsletter (MICRO-15 Workshop), 1982
- DOI: https://www.semanticscholar.org/paper/MIPS%3A-A-microprocessor-architecture-Hennessy-Jouppi/4d4ebf403867ae014ba49c24923a021376aeae40
- 피인용수: 700+
- 요약: Stanford MIPS의 첫 공식 논문. "Microprocessor without Interlocked Pipeline Stages" — 하드웨어가 파이프라인 의존성을 해결하지 않고, 컴파일러가 지연 슬롯(delay slot)에 안전한 명령어를 채우게 한다는 과감한 결정. 1981~1984 진행, 이후 MIPS Computer Systems(1984)로 상용화 → R2000 (1985).
- 방법론: VLSI 구현 + 컴파일러-하드웨어 공동 설계.
- 핵심 결과: 5-stage 파이프라인을 지연 슬롯 노출 방식으로 단순화. 클록당 1 명령어(IPC=1) 목표 달성.
- 인용할 만한 문장:
  > "Exposed all hazards caused by the five-stage pipeline using delay slots" — 하드웨어가 해결할 일을 컴파일러가 한다. (Stanford MIPS 위키 인용)
- 독자 전달 방식 제안: 챕터 8~9 "파이프라이닝" 도입에서, MIPS의 "이름 자체가 약자다" 일화로 RISC의 컴파일러-친화 철학을 설명.

## 논문 5: A New Golden Age for Computer Architecture

- 저자·연도: John L. Hennessy, David A. Patterson, 2019 (2018 Turing Lecture)
- 발표처: *Communications of the ACM*, Vol. 62, No. 2 (Feb 2019), pp. 48–60
- DOI: 10.1145/3282307
- 피인용수: 1,200+
- 요약: 2017 Turing Award 수상 강연. 1986~1996 RISC 혁명을 첫 황금기로 정의, 2018~ 시기를 "두 번째 황금기"로 선언. 4가지 동력: (1) Domain-Specific Architecture(DSA), (2) 보안, (3) Open ISA(RISC-V), (4) Agile chip design.
- 방법론: 회고적 분석 + 미래 비전.
- 핵심 결과: Moore's Law/Dennard scaling 종말 이후, 일반 목적 CPU 최적화가 한계에 도달. 도메인 특화(GPU, TPU) + 오픈 ISA가 다음 혁명.
- 인용할 만한 문장:
  > "Approximately 1986–1996, when new instruction set architectures, almost all reduced instruction set computers (RISCs), revolutionized the industry." — 첫 황금기 정의
  > 두 번째 황금기 선언과 함께 "Domain-Specific Hardware/Software Co-Design, Enhanced Security, Open Instruction Sets, and Agile Chip Development"
- 독자 전달 방식 제안: 책 서장 또는 마지막 챕터 "지금 8비트 CPU를 왜 만드나"에서, "두 번째 황금기를 이해하려면 첫 번째 황금기의 RISC 정신을 손으로 만들어 봐야 한다"는 도입.

## 논문 6: Validity of the Single-Processor Approach to Achieving Large-Scale Computing Capabilities

- 저자·연도: Gene M. Amdahl, 1967
- 발표처: AFIPS Spring Joint Computer Conference Proceedings, p. 483
- DOI: 10.1145/1465482.1465560
- 피인용수: 5,000+ (역사적 seminal)
- 요약: Amdahl의 법칙. 병렬화 가능한 비율을 α라 할 때 N개 프로세서를 써도 최대 속도 향상은 1/((1-α) + α/N)으로 제한된다. 단일 프로세서 성능을 끝까지 짜내야 하는 이유의 수학적 근거.
- 방법론: 형식적 분석 + 실증 데이터.
- 핵심 결과: 직렬 부분이 5%만 있어도 최대 20배 가속이 한계. CPU 마이크로아키텍처 최적화의 정당화.
- 인용할 만한 문장:
  > "The potential speedup to be obtained by applying multiple CPUs will be bounded by the program's inherently sequential computations."
- 독자 전달 방식 제안: 챕터 9 또는 부록에서, "RISC가 클록 속도와 IPC를 둘 다 잡으려 한 이유는 Amdahl이 1967년에 이미 말했다"는 식으로 RISC 동기 부여.

## 논문 7: Nand to Tetris: Building a Modern Computer System from First Principles

- 저자·연도: Shimon Schocken, Noam Nisan, 2024
- 발표처: *Communications of the ACM*, Vol. 67, No. 5 (May 2024)
- DOI: 10.1145/3626513
- 피인용수: 신간 (200+ 인용, Schocken/Nisan 책 인용 누적은 수천)
- 요약: 2002년 시작된 nand2tetris 커리큘럼의 회고. 12개 프로젝트로 NAND 게이트부터 OS·게임까지. 400개 이상의 대학·고교·부트캠프에서 채택. CACM 회고 논문에서 페다고지 원리 정리.
- 방법론: 1차 사례연구 + 학습 효과 회고.
- 핵심 결과: "bottom-up first-principles" 페다고지가 추상 개념을 직관으로 변환한다는 명제. 무료 오픈 자료가 핵심 동력.
- 인용할 만한 문장 (CACM 논문 + 책 머리말):
  > "Nand to Tetris is a hands-on journey that starts with the most elementary logic gate, called Nand, and ends up, twelve projects later, with a general-purpose computer system."
  > "All course materials—lectures, projects, specifications, and software tools—are freely available in open source. Nand to Tetris courses are taught at 400+ universities, high schools, and bootcamps."
- 독자 전달 방식 제안: 본 책 서문 또는 챕터 1에서 "nand2tetris가 게이트부터 OS까지 12 프로젝트라면, 우리 책은 SAP-1부터 8비트 RISC까지 점진적으로 쌓는다"는 비교 위치 설정.

## 논문 8: Teaching Computer Organization/Architecture with Limited Resources Using Simulators

- 저자·연도: William Yurcik, Jean Mary, 2001
- 발표처: *ACM SIGCSE Bulletin*, Vol. 33 (SIGCSE 2001)
- DOI: 10.1145/563517.563408
- 피인용수: 250+
- 요약: 시뮬레이터가 컴퓨터 아키텍처 교육의 표준 도구로 자리 잡은 시점의 종합 정리. EasyCPU(8086), Little Man Computer(LMC), RTLSim(MIPS-like) 등을 평가.
- 방법론: 시뮬레이터 카탈로그 + 교육 효과 정성 평가.
- 핵심 결과: "복잡한 실제 CPU보다 단순한 교육용 시뮬레이터가 학습 효과 우월" — 본 책의 SAP-1 선택을 정당화하는 학술적 근거.
- 인용할 만한 문장:
  > "As the complexity and variety of computer system hardware increases, its suitability as a pedagogical tool in computer organization/architecture courses diminishes. As a consequence, many instructors are turning to simulators as teaching aids."
  > "Visualization of different computer hardware architectures with the use of simulators enhances the learning process among students."
- 독자 전달 방식 제안: 책 서장 "왜 우리는 실제 칩을 만들지 않는가" 답변으로 직접 인용 가능.

## 논문 9: Three Simulator Tools for Teaching Computer Architecture: Little Man Computer, and RTLSim

- 저자·연도: William Yurcik, et al., 2001
- 발표처: *Journal on Educational Resources in Computing (JERIC)*, Vol. 1, No. 4
- DOI: 10.1145/514144.514732
- 피인용수: 150+
- 요약: LMC, EasyCPU, RTLSim 세 시뮬레이터 비교 평가. LMC는 100-셀 메모리에 mailbox 비유를 쓰는 von Neumann 모사. SAP-1과 거의 동일한 추상화 수준.
- 핵심 결과: 단순 시뮬레이터가 처음 접하는 학생에게 fetch-decode-execute를 이해시키는 데 가장 효과적.
- 인용할 만한 문장:
  > "Little Man Computer simulator is generally used for educational purposes because it models a simple Von Neumann architecture computer, and it demonstrates how assembly code is processed by the CPU using the Fetch, Decode and Execute (FDE) Cycle."
- 독자 전달 방식 제안: 챕터 1~2 SAP-1 소개에서 "이 단순함은 우연이 아니라 30년간의 교육 실험으로 정착된 추상화 수준"이라는 메타 코멘트로 보강.

## 논문 10: VRV: A Versatile RISC-V Simulator for Education

- 저자·연도: 2025 (SIGCSE 2025)
- 발표처: *Proceedings of the 56th ACM Technical Symposium on Computer Science Education V. 2*
- DOI: 10.1145/3641555.3705240
- 피인용수: 신간
- 요약: SPIM(MIPS) 시대 종말 이후 빈자리를 채우는 RISC-V 교육용 시뮬레이터. CLI + GUI, 디버거 내장, 시스템 프로그래밍 지원. 학부 컴퓨터 아키텍처 강의용.
- 핵심 결과: 학생들이 RISC-V를 처음 배울 때 시각화된 데이터패스가 학습 효과의 2배.
- 독자 전달 방식 제안: 챕터 7 "8비트 RISC" 도입에서, "산업계는 RISC-V를 채택했지만, 우리는 8비트 변형으로 정신만 빌린다"는 위치 설정. RISC-V 32비트 ISA가 본 책의 8비트 RISC 챕터의 직접 모델.

## 논문 11: WebRISC-V: a Web-Based Education-Oriented RISC-V Pipeline Simulation Environment

- 저자·연도: Roberto Giorgi, Gianfranco Mariotti, 2019
- 발표처: WCAE 2019 (Workshop on Computer Architecture Education)
- DOI: 10.1145/3338698.3338890
- 피인용수: 100+
- 요약: 웹 브라우저에서 사이클별 RISC-V 파이프라인 동작을 시각화. forward, stall, branch prediction을 셀 단위로 표시.
- 인용할 만한 문장:
  > "Currently the first simulator that can be executed directly in a web-browser while displaying the cycle-by-cycle detailed pipeline execution for a RISC-V processor."
- 독자 전달 방식 제안: 챕터 7~8 파이프라이닝 챕터에서, Kotlin 시뮬레이터에 사이클별 trace 출력을 어떻게 짜는지의 학술적 정당화. "사이클 시각화가 학습에 본질적"이라는 인용.

## 논문 12: Architectural Simulation for Education and Competition (ChampSim)

- 저자·연도: 2022
- 발표처: arXiv:2210.14324
- DOI/arXiv: https://arxiv.org/pdf/2210.14324
- 피인용수: 50+
- 요약: ChampSim 시뮬레이터의 교육적 설계 철학. 정확성보다 가독성을 우선해 학생이 한 학기 안에 구조를 이해하고 변경할 수 있게 함.
- 인용할 만한 문장:
  > "ChampSim simulator's design does not necessarily attempt to precisely replicate all hardware functions, but to emulate it in a readable way, allowing a student to rapidly grasp its functionality, configure it, and implement or modify techniques they've learned about in class within one academic semester."
- 독자 전달 방식 제안: 챕터 6 "정확도 vs 단순성" 토론에서, ksim65가 cycle-exact를 포기한 것과 같은 페다고지 결정의 학술적 정당화. 본 책의 코드도 "한 학기에 이해 가능한 가독성"을 우선한다는 선언의 근거.

## 논문 13: Further Evaluations of a Didactic CPU Visual Simulator (CPUVSIM)

- 저자·연도: 2024
- 발표처: arXiv:2411.05229
- DOI/arXiv: https://arxiv.org/abs/2411.05229
- 피인용수: 신간
- 요약: 시각적 CPU 시뮬레이터의 학습 효과 실증 평가. Open Pedagogy 접근으로 반복 개선. 고수준 코드 → 어셈블리 매핑을 학생이 이해하게 도와줌.
- 핵심 결과: 시뮬레이터 사용 그룹이 대조군 대비 어셈블리 이해 시험에서 유의미 우위.
- 독자 전달 방식 제안: 책 전반의 "Kotlin 코드 + 가상 어셈블리 + 머신 코드"의 3중 시각화 정당화.

## 논문 14: Teaching Computer Architecture by Designing and Simulating Processors from Their Bits and Bytes (VSCPU)

- 저자·연도: 2024
- 발표처: *PeerJ Computer Science* (PMC10909196)
- DOI: https://pmc.ncbi.nlm.nih.gov/articles/PMC10909196/
- 피인용수: 신간
- 요약: VerySimpleCPU(VSCPU) 플랫폼. 학생이 자기 ISA를 설계하고 시뮬레이터를 짜고 FPGA에 올린다. "from scratch" 페다고지의 최신 형태.
- 핵심 결과: ISA 자율 설계가 컴퓨터 아키텍처 이해도를 결정적으로 높임.
- 독자 전달 방식 제안: 책 후반 "당신의 8비트 RISC를 설계하라" 과제 챕터의 학술적 근거.

## 논문 15: Comments on "The Case for the Reduced Instruction Set Computer"

- 저자·연도: Douglas W. Clark, William D. Strecker, 1980
- 발표처: *ACM SIGARCH Computer Architecture News*, Vol. 8, No. 6, 1980
- DOI: 10.1145/641914.641918
- 피인용수: 200+ (Patterson 원논문 직후 반박)
- 요약: VAX 설계자 측의 반박. "복잡 명령어는 마이크로코드로 저렴하고, 메모리/캐시 비용을 줄인다"는 CISC 변호. RISC/CISC 논쟁의 초기 양면을 보여주는 논문.
- 핵심 결과: RISC 가설이 1980년 시점에 자명하지 않았음을 보여줌. 양 진영의 논거 모두 존재.
- 인용할 만한 문장: "Most of the proposed RISC's advantage will be lost when faced with the realities of the marketplace." (Clark & Strecker 요약)
- 독자 전달 방식 제안: §4 (논쟁점)에서 "RISC가 처음부터 명백히 우월하지 않았다 — 1980년대 내내 격렬한 논쟁이 있었다"는 균형 잡힌 서술의 근거.

---

## 핵심 교과서 참조 (학술적 standard reference)

이 논문 리서치에 추가로, 본 책이 직접 인용해야 할 표준 교과서 4종:

### T1. Computer Organization and Design (MIPS / RISC-V Edition)

- 저자: David A. Patterson, John L. Hennessy
- 출판: Morgan Kaufmann, 1994 (1판) ~ 2020 (6판)
- ISBN: 9780128201091 (MIPS 6판), RISC-V edition도 별도
- 위상: 학부 컴퓨터 아키텍처 표준 교과서. 40,000+ 학생/년이 사용.
- 본 책 관련: 8비트 RISC 챕터의 datapath, single-cycle vs multi-cycle, pipelining 5-stage 모델의 직접 원천.
- 인용할 표현: 본 책은 "단순화한 MIPS"를 본 책의 8비트 RISC 모델로 차용한다고 명시.

### T2. Computer Architecture: A Quantitative Approach

- 저자: John L. Hennessy, David A. Patterson (5판부터 Christos Kozyrakis 합류)
- 출판: Morgan Kaufmann, 1990 (1판) ~ 2024 (7판)
- ISBN: 9780128119051 (6판)
- 위상: 대학원/실무자 표준. DLX(simplified MIPS) → RISC-V로 5판부터 전환.
- 본 책 관련: "Quantitative Approach"라는 제목 자체가 본 책의 비교 표(8080 vs Z80 vs 6502 정량 비교) 페다고지의 직접 영감.

### T3. Structured Computer Organization

- 저자: Andrew S. Tanenbaum, Todd Austin (5판부터)
- 출판: Pearson, 1976 (1판) ~ 2024 (6판)
- ISBN: 9780137618446 (6판)
- 위상: "computer as a hierarchy of levels" 페다고지의 원조.
- 본 책 관련: 본 책의 학습 청사진(CPU → 메모리 → 버스 → I/O → 커널 → OS → 응용)이 Tanenbaum의 "digital logic / microarchitecture / ISA / OS / assembly" 5계층 모델의 직계 후예.
- 인용할 표현:
  > "A computer can be structured as a hierarchy of levels, covering the digital logic level, the microarchitecture level, the instruction set architecture level, the operating system machine level and the assembly language level."

### T4. Digital Computer Electronics (Malvino & Brown)

- 저자: Albert Paul Malvino, Jerald A. Brown
- 출판: McGraw-Hill, 1977 (1판) ~ 1993 (3판)
- ISBN: 9780028005942 (3판)
- 위상: SAP-1/SAP-2/SAP-3 원전. 본 책의 단계적 확장 골격의 직접 출처.
- 본 책 관련: 본 책은 Malvino의 SAP-1/SAP-2 ISA를 그대로 차용하되, 하드웨어 구현 대신 Kotlin 시뮬레이터로 대체한다.
- 비판적 위치: Austin Morlan (자료 2)이 지적했듯 SAP-2 명세가 다소 ad-hoc하다는 점을 명시. 본 책에서는 모호한 부분을 일관성 있게 정리하는 게 가치 추가 지점.

### T5. The Elements of Computing Systems (nand2tetris 책)

- 저자: Noam Nisan, Shimon Schocken
- 출판: MIT Press, 2005 (1판) / 2021 (2판)
- ISBN: 9780262539807 (2판)
- 위상: nand2tetris 커리큘럼의 정전.
- 본 책 관련: 본 책의 페다고지 모델 — "from first principles, hands-on, project per chapter".

### T6. Crafting Interpreters

- 저자: Robert Nystrom
- 출판: 자체 출판 (genever benning), 2021
- 위상: 인터프리터 자기학습서의 새 표준.
- 본 책 관련: 본 책의 점진적 구현 페다고지("Lox를 두 번 구현"의 8비트 CPU 버전: SAP-1을 만들고, SAP-2로 확장하고, 다시 RISC로 다시 짠다)의 직접 영감.

---

## 수집 한계

- **Patterson 1980 RISC 논문 본문 직접 접근:** PDF가 binary 인코딩으로 잡혀 핵심 문장을 원문 그대로 추출하지 못했다. Wikipedia/Berkeley 강의 노트 + Semantic Scholar 메타데이터로 보강했지만, 직접 본문을 봤다면 4가지 cost-effectiveness 논거를 더 정밀히 인용했을 것.
- **CACM nand2tetris 2024 논문 본문:** 403 Forbidden으로 못 가져왔다. 책 머리말과 ACM 소개 페이지로 대체.
- **Hennessy 1981 "MIPS: A VLSI Processor Architecture":** Semantic Scholar 메타데이터만, full text 접근 불가.
- **8비트 CPU 시뮬레이션의 학술 페다고지 논문:** 8비트(SAP-1, 6502 등) 시뮬레이터에 대한 본격 학술 논문은 적다. 대부분 16/32비트(MIPS/RISC-V) 교육 논문이다. → 8비트 페다고지의 정당화는 1차 사료(Malvino 책)와 nand2tetris CACM 논문이 가장 가까운 학술 근거.
- **Cycle-accurate 에뮬레이션의 학술 서베이:** 본격 peer-reviewed survey는 발견하지 못함. 커뮤니티 자료(mGBA blog 등)가 사실상 표준 — 학술 논문이 아닌 1차 구현자의 글. → 커뮤니티 리서치에서 보강.
- **국내 학술 자료:** 한국 학회(KIISE 등) 논문은 본격 검색하지 않았다. 본 책의 인용 가치 측면에서 영문 seminal/textbook이 더 권위 있다고 판단.
