# 4장 — 레지스터와 8비트 산술

## 핵심 질문

두 8비트 수를 더한다는 것은 무엇인가?

255 + 1은 256이 아니라 0이다. 0 - 1은 -1이 아니라 255다. 이 규칙이 낯설게 느껴진다면, 지금이 바로 2의 보수와 화해할 순간이다. 레지스터 두 개와 ALU 하나를 직접 짜면서, 8비트라는 작은 우주 안에서 산술이 어떻게 작동하는지를 손으로 확인해 보자.

## 이번 챕터에서 짓는 것

### Register — 8비트 값을 가두는 그릇

A 레지스터, B 레지스터 모두 같은 `Register` 클래스 하나로 표현한다. `load()` 호출 시 `and 0xFF` 마스킹으로 8비트 경계를 지킨다. 음수를 `load(-1)` 해도 `value`에는 `0xFF`가 담긴다. 하드웨어의 D 플립플롭이 하는 일을 변수 하나와 마스킹 한 줄로 표현한 셈이다.

### Alu — 플래그 없는 순수 산술

`add`, `sub`, `and`, `or`, `xor`, `not` 여섯 연산을 제공한다. 결과는 모두 `and 0xFF`로 마스킹해 8비트 범위 안에 가둔다. **이 챕터에서 플래그(Z·C·S·V)는 아직 없다** — carry, overflow, zero 감지는 5장에서 추가한다. 지금은 산술 자체에 집중한다.

## UByte vs Int 마스킹 정책

Kotlin에서 8비트 수를 다루는 방법은 세 가지다: `Byte`, `UByte`, `Int + and 0xFF`. 이 책은 **Int + `and 0xFF` 마스킹**을 채택한다.

이유는 세 가지다.

첫째, JVM은 피연산자 스택을 32비트 단위로 다룬다. `UByte`를 쓰면 컴파일러가 매 연산마다 변환 바이트코드를 삽입한다 — 성능이 아니라 노이즈다. `Int`는 JVM 네이티브다.

둘째, `UByte`는 부호 없는 타입이라 `shr`(논리 시프트)는 되지만 `ushr`(부호 없는 오른쪽 시프트)가 별도로 필요 없다. 반면 `Int`로 표현하면 `shr`와 `ushr`의 차이를 직접 손으로 짚을 수 있어, 5·6장의 플래그·시프트 연산 설명이 명료해진다.

셋째, SAP-1에서 음수는 2의 보수로 표현한다. `Int`로 음수를 받아 `and 0xFF`로 마스킹하면 2의 보수 변환이 자연스럽게 일어난다. 별도 변환 코드가 필요 없다.

## Kotlin 패턴 결정

| 하드웨어 개념 | Kotlin 표현 | 이유 |
|---------------|-------------|------|
| A·B 레지스터 | `Register` 클래스 | 같은 구조, 인스턴스만 두 개 |
| ALU 연산 | `object Alu` | 상태 없음, 순수 함수 집합 |
| 8비트 범위 강제 | `and 0xFF` | JVM 네이티브 Int, 2의 보수 자연 처리 |
| 플래그 | 없음 (5장에서 추가) | 관심사 분리, 단계적 구현 |

## 실행

```bash
./gradlew :chapter-04:test
```

테스트 총 25개 — ch03에서 상속한 ClockTest 4개, ProgramCounterTest 5개, InstructionTest 7개에 RegisterTest 5개, AluTest 9개가 새로 추가됐다. 모두 초록불이면 5장으로 넘어가도 좋다.

## GitHub 산출물

```
example/chapter-04/
├── build.gradle.kts
├── README.md
└── src/
    ├── main/kotlin/sap/ch04/
    │   ├── Clock.kt          ← ch03 상속
    │   ├── ProgramCounter.kt ← ch03 상속
    │   ├── Instruction.kt    ← ch03 상속
    │   ├── Register.kt       ← 신규
    │   └── Alu.kt            ← 신규
    └── test/kotlin/sap/ch04/
        ├── ClockTest.kt          ← ch03 상속
        ├── ProgramCounterTest.kt ← ch03 상속
        ├── InstructionTest.kt    ← ch03 상속
        ├── RegisterTest.kt       ← 신규
        └── AluTest.kt            ← 신규
```

## 다음 챕터로

5장에서는 overflow의 무덤을 정면으로 돌파한다. 255 + 1 = 0은 아무 문제가 없다 — CPU는 이미 알고 있다, carry 플래그로. 127 + 1 = -128은 어딘가 이상하다 — CPU는 그것도 안다, overflow 플래그로. Z·C·S·V 네 비트가 ALU에 붙으면 산술이 단순한 계산에서 판단의 도구로 바뀐다.
