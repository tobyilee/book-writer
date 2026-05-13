# 책 동반 예제 코드 — Gradle Kotlin DSL 멀티모듈 프로젝트 설계

- **상태:** 승인 대기 (사용자 리뷰)
- **저술일:** 2026-05-13
- **연결되는 책:** *코드로 짓는 CPU — Kotlin으로 SAP-1에서 8비트 RISC까지* v1.0.0 (Toby-AI)
- **저장 경로:** 프로젝트 루트의 `example/`

## 1. 목적

책 *코드로 짓는 CPU*에 나오는 모든 Kotlin 예제 코드를 실제로 컴파일하고 실행할 수 있는 형태로 영구화한다. 독자는 책을 읽으며 해당 챕터의 `example/chapter-XX/`를 클론·실행해 그 시점의 CPU를 손에 잡을 수 있다.

차별점은 **누적 스냅샷**이라는 점이다. 챕터 N의 폴더는 챕터 1~N까지의 모든 코드를 담는다. 챕터마다 책의 산행이 끝난 직후 GitHub 저장소가 어떤 상태인지 그대로 재현한다.

## 2. 사용자가 얻는 경험

1. `git clone … && cd example/`
2. `./gradlew :chapter-06:test` — 챕터 6에서 만든 SAP-1 통합 테스트가 통과
3. `./gradlew :chapter-06:run` — `LDA 9 → ADD A → OUT → HLT` 5바이트 프로그램이 SAP-1 위에서 돌고 결과가 콘솔에 출력
4. `./gradlew :chapter-14:run` — 본 책 합성 8비트 RISC가 Fibonacci를 계산하면서 cycle counter를 함께 출력
5. `./gradlew test` — 전 챕터 테스트 전체 통과

## 3. 디렉토리 구조

```
example/
├── settings.gradle.kts          # rootProject + 15개 include
├── build.gradle.kts             # 모든 subproject에 공통 적용되는 Kotlin/JVM/test 설정
├── gradle.properties            # org.gradle.parallel=true 등
├── gradle/libs.versions.toml    # 의존성 버전 catalog
├── gradle/wrapper/              # Gradle 8.7 wrapper
├── gradlew, gradlew.bat
├── README.md                    # 전체 가이드 + 챕터 매트릭스
├── chapter-01/README.md         # 코드 없음 — 챕터 핵심 요약만
├── chapter-02/
│   ├── build.gradle.kts         # application 플러그인, main = "sap.ch02.MiniCpuKt"
│   ├── README.md                # 챕터 학습 포인트, 실행 커맨드
│   └── src/
│       ├── main/kotlin/sap/ch02/MiniCpu.kt
│       └── test/kotlin/sap/ch02/MiniCpuTest.kt
├── chapter-03/ … chapter-10/    # SAP-1 → SAP-2 점진 (누적)
├── chapter-11/
│   ├── README.md                # 비교 챕터 해설
│   └── comparison/
│       ├── fib_8080.asm
│       ├── fib_6502.asm
│       ├── fib_z80.asm
│       └── fib_8086.asm
├── chapter-12/README.md         # RISC vs CISC 역사 챕터, 코드 없음
├── chapter-13/                  # 새 출발 — RISC-8 ISA
├── chapter-14/                  # RISC-8 cycle-accurate
└── chapter-15/README.md         # 마무리 챕터, 코드 없음
```

## 4. 핵심 기술 선택

| 항목 | 값 | 근거 |
|---|---|---|
| Kotlin | 2.0.x | 책 시점 안정 LTS, K2 컴파일러 |
| JVM target | 17 | 모던 LTS, 광범위 호환 |
| Gradle | 8.7 (wrapper 동봉) | Kotlin 2.0 친화, Kotlin DSL 안정 |
| 테스트 프레임워크 | **kotest 5.x** (JUnit5 platform 위에서) | 책 5장이 kotest 도입을 명시. property-based·table-driven·DescribeSpec 모두 사용. assertion은 `shouldBe` 등 kotest 표준 |
| 패키지 네임스페이스 | `sap.chXX.*`, `risc8.chXX.*` | 챕터 격리, 클래스 이름 충돌 없음 |
| Gradle 플러그인 | `application` (`run` 태스크 가능) + `org.jetbrains.kotlin.jvm` | 각 챕터에 데모 실행이 있음 |
| 누적 정책 | 챕터 N은 챕터 N-1의 모든 코드를 포함, 그 위에 새 코드 추가 | 사용자 선택, 클론 직진성 |
| 14장 벤치마크 | JMH 1.37 (`me.champeau.jmh` 플러그인) | 책 14장의 JVM 시뮬레이터 성능 측정 소절 |

## 5. 챕터별 코드 산출물

책의 각 챕터 카드 "GitHub 산출물" 박스를 그대로 따른다.

| Ch | 새로 추가되는 핵심 클래스 | 테스트 개수 (목표) | 실행 가능 데모 |
|----|------------------|---|----|
| 1 | (없음 — README만) | — | — |
| 2 | `MiniCpu.kt` | 8 | `:chapter-02:run` → ADD/HLT 실행 |
| 3 | `Clock.kt`, `ProgramCounter.kt`, `sealed class Instruction` | 6~8 | — |
| 4 | `Register.kt`, `Alu.kt` | ~30 (ALU 테이블 테스트) | — |
| 5 | `AluFlags.kt` (Z/C/S/V), kotest 도입 | ~50 (256x2 overflow 테이블) | — |
| 6 | `Ram.kt`, `Bus.kt`, `Controller.kt`, `Sap1.kt` | ~15 (통합) | `:chapter-06:run` → SAP-1이 5바이트 프로그램 실행 |
| 7 | `asm/Lexer.kt`, `asm/Assembler.kt`, `asm/Disassembler.kt` | e2e 어셈블→실행 (≥10) | `:chapter-07:run` → `programs/add.sap1` 어셈블 후 SAP-1 실행 |
| 8 | `Sap2Core.kt(scaffold)`, `RegisterFile.kt` | 64KB·16-bit PC 동작 검증 | — |
| 9 | `Jump.kt`, `Stack.kt`, `IoPort.kt` | Fibonacci e2e + "Hello" 출력 | `:chapter-09:run` → SAP-2가 "Hello" 출력 |
| 10 | `MicroRom.kt`, `Debugger.kt` | SAP-2 test ROM 묶음 | `:chapter-10:run` → debugger CLI |
| 11 | (Kotlin 없음 — .asm 4개 + README) | — | — |
| 12 | (없음 — README만) | — | — |
| 13 | `risc8/Isa.kt`, `risc8/Assembler.kt`, `risc8/Cpu.kt` | RISC-8 ISA 디코딩·실행 | `:chapter-13:run` → RISC-8 Fibonacci |
| 14 | `risc8/CycleAccurate.kt` + JMH | cycle counter 검증 | `:chapter-14:run` → cycle count 출력, `:chapter-14:jmh` → 벤치 |
| 15 | (없음 — README만) | — | — |

## 6. 누적 정책 세부

- 챕터 N의 `src/`는 챕터 1~N의 모든 코드를 포함
- 클래스가 챕터를 거치며 *수정*되는 경우(예: 4장 ALU에 5장에서 Flag 추가): 챕터 5에서는 *완전판* ALU를 그대로 사용. 챕터 4 폴더는 4장 시점의 ALU(플래그 없음)를 별도로 보존.
- 패키지 네임스페이스가 챕터별로 격리되므로 클래스 이름 충돌 없음. 챕터 3의 `Alu`는 `sap.ch03.Alu`, 챕터 4의 `Alu`는 `sap.ch04.Alu`. 챕터 N 내부의 import는 챕터 N 자신의 패키지를 가리킴.
- 책 본문과 코드가 일치하지 않으면(책이 의도적으로 생략한 helper, import 등) **책 본문을 권위로 삼되 코드는 컴파일·실행 가능하도록 채운다.** 책에 직접 나오지 않은 의미상 추가(helper 함수, util, 데모용 main, 누락 import)는 *허용*. 책의 의미와 다른 변경은 *금지* — 그런 충돌이 있으면 챕터 README에 한 줄로 명시.

## 7. 테스트 정책

- 각 코드 챕터의 `:chapter-XX:test`가 통과해야 함
- 책에 명시된 테스트 개수를 *목표*로 함 (정확히 맞출 필요는 없지만 의도된 커버리지를 잃지 않음)
- 5장은 kotest `forAll` 표 기반 테스트로 256×2 = 512 케이스를 검증 (overflow 정면돌파)
- 6장의 SAP-1 통합 테스트: 메모리에 직접 hex 5바이트를 적고 실행→결과 비교
- 7장의 e2e: 어셈블리 텍스트 → 바이트열 → SAP-1 실행 → 결과
- 10장의 SAP-2 test ROM: 단순화된 6502 functional test의 SAP-2 축소판
- 14장의 RISC-8 cycle-accurate: 같은 프로그램의 instruction-count vs cycle-count 검증

## 8. 빌드 검증 절차

구현 완료 후 다음이 모두 통과해야 한다:

```
./gradlew clean
./gradlew build               # 전체 빌드 (모든 챕터)
./gradlew test                # 전체 테스트
./gradlew :chapter-02:run     # 미니 CPU
./gradlew :chapter-06:run     # SAP-1
./gradlew :chapter-09:run     # SAP-2 "Hello"
./gradlew :chapter-13:run     # RISC-8 Fibonacci
./gradlew :chapter-14:run     # RISC-8 cycle-accurate
```

## 9. 범위 제한 (Non-goals)

- IDE 설정 파일(`.idea/`, `.iml`)은 포함하지 않음 — 사용자가 IntelliJ로 import만 하면 됨
- Docker 이미지, CI 워크플로우 파일은 이번 범위 아님
- README 외 별도 튜토리얼/사이트 생성 없음
- 코드 스타일(detekt/ktlint)은 이번 범위 아님
- 챕터 1·12·15의 다이어그램·이미지는 README 텍스트로만 (이미지 추가는 별도 작업)

## 10. 위험 / 트레이드오프

| 위험 | 완화책 |
|---|---|
| 챕터 간 코드 중복으로 인한 저장소 비대화 | 단순한 텍스트라 git 압축이 잘 됨. 누적 정책의 학습 이점이 더 큼 |
| 챕터 N의 코드를 챕터 N-1과 비교해 보고 싶은 사용자 | README에 `git diff chapter-03 chapter-04 -- src/` 같은 비교 명령 안내 |
| 책 본문의 코드 스니펫과 실제 컴파일 가능 코드의 차이가 독자를 혼란시킬 가능성 | 챕터 README에 "책 vs 실제 코드" 차이를 한 줄씩 명시 |
| 챕터 13의 8비트 RISC ISA가 합성이라 인용할 표준 명세가 없음 | 챕터 13의 README에 ISA 명세 인라인 (책 13장 사용 레퍼런스 §7.1과 동일) |
| 챕터 14의 JMH 벤치 실행 시간 | 기본 옵션은 빠른 dry-run 수준. 정식 벤치는 README의 옵션 안내로만 |

## 11. 후속 작업 (별도 계획)

이 설계 승인 후 `writing-plans` 스킬로 다음을 작성:

1. 실행 계획 (Gradle 골격 → 챕터 1~15 순차 구현 → 검증)
2. 챕터별 구현 단위 (각 챕터의 코드를 만들기 위한 step-by-step)
3. 최종 검증 체크리스트
