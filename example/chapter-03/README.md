# 3장 — SAP-1의 청사진과 첫 모듈

## 핵심 질문

SAP-1이란 얼마나 단순한가?

8비트 데이터, 4비트 주소, 메모리 16바이트, 명령어 다섯 개. 이게 전부다. 이 작음이 빈약함이 아니라 선의 단순함임을 손으로 짜면서 확인한다.

## SAP-1 전체 명세

| 항목 | 값 |
|------|----|
| 데이터 폭 | 8비트 |
| 어드레스 폭 | 4비트 |
| 메모리 | 16바이트 RAM |
| 명령어 | LDA, ADD, SUB, OUT, HLT (5개) |
| 누산기 | A 레지스터 (8비트) |
| ALU | 8비트 가산/감산, Z·C 플래그 |
| T-state | 명령어당 6 클록 (T1~T3 fetch 공통, T4~T6 execute) |

### 명령어 인코딩 (4비트 opcode + 4비트 주소)

| 명령어 | opcode | 예시 |
|--------|--------|------|
| LDA    | 0x0    | `LDA 5` → `0x05` |
| ADD    | 0x1    | `ADD 6` → `0x16` |
| SUB    | 0x2    | `SUB 7` → `0x27` |
| OUT    | 0xE    | `OUT`   → `0xE0` |
| HLT    | 0xF    | `HLT`   → `0xF0` |

## 이번 챕터에서 짓는 것

### Clock — T1~T6 박자 모듈

모든 모듈을 동기화하는 클록. `tick()` 한 번이 T-state 하나를 전진시키고, T6 다음은 T1으로 순환한다. 실물 회로의 수정 진동자를 Kotlin 변수 하나로 표현한다.

### ProgramCounter — 4비트 PC

다음에 실행할 명령어 주소를 가리키는 4비트 카운터. `increment()`로 1씩 올라가고 0xF 다음은 0으로 순환한다. `load()`로 임의 주소를 적재할 수 있어 SAP-2의 JMP 명령어를 대비한다.

### Instruction — sealed class 명령어 계층

SAP-1의 다섯 명령어를 sealed class로 모델링한다. operand 유무가 명령어마다 다르기 때문에 enum보다 sealed class가 자연스럽다. `when` 분기의 컴파일타임 완전성 검사로 SAP-2 확장 시 누락 분기를 잡는다.

## Kotlin 패턴 결정

| 하드웨어 개념 | Kotlin 표현 | 이유 |
|---------------|-------------|------|
| 레지스터 | 가변 클래스 | 가변 상태, 매 클록마다 제자리에서 변한다 |
| 버스 | 함수 인자 | 로컬 변수로 충분, 별도 클래스 불필요 |
| 명령어 | sealed class | operand 구조 차이 + 컴파일타임 완전성 |
| 메모리 | `IntArray` + 마스킹 | JVM 최적, UByte 시프트 제한 회피 |

## 실행

```bash
./gradlew :chapter-03:test
```

테스트 총 16개 — ClockTest 4개, ProgramCounterTest 5개, InstructionTest 7개. 모두 초록불이 떨어지면 4장으로 넘어가도 좋다.

## GitHub 산출물

```
example/chapter-03/
├── build.gradle.kts
├── README.md
└── src/
    ├── main/kotlin/sap/ch03/
    │   ├── Clock.kt
    │   ├── ProgramCounter.kt
    │   └── Instruction.kt
    └── test/kotlin/sap/ch03/
        ├── ClockTest.kt
        ├── ProgramCounterTest.kt
        └── InstructionTest.kt
```

## 다음 챕터로

4장에서는 **A·B 레지스터와 ALU**를 짠다. 그 과정에서 이 책 전체의 비트 표현 정책을 결정한다 — `Byte`, `UByte`, `Int` + 마스킹 세 선택지 중 무엇으로 갈 것인가. 동시에 두 8비트 수를 더한다는 것이 회로 차원에서 무슨 의미인지, 2의 보수가 왜 우아한지를 직접 손으로 짚는다.
