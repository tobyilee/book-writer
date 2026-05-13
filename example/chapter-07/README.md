# 7장 — 어셈블러와 디스어셈블러

> "`0x1A`가 ADD 10인지 외우는 건 두 명령이면 한계다."
> 자작 CPU를 처음 깐 사람이 보통 사흘 안에 만나는 벽이다.

## 핵심 질문

사람이 적은

```
LDA $9
ADD $A
OUT
HLT
```

이 어떻게 `0x09 0x1A 0xE0 0xF0` — 4바이트의 0과 1 — 이 되는가?
거꾸로, 메모리에 박힌 `0x2A`를 보고 우리는 "이건 데이터이지 명령이 아니다"라고 어떻게 판단하는가?

이 장은 그 사이를 잇는 작은 컴파일러 — **어셈블러**와 그 반대 방향 — **디스어셈블러**를 만든다.
그 순간 우리의 SAP-1은 **자기 언어를 가진 컴퓨터**의 첫 모서리를 갖는다.

## 이 장에서 만드는 것

| 파일 | 역할 |
|------|------|
| `asm/Lexer.kt` | 텍스트를 토큰 스트림으로 자르는 어휘 분석기 |
| `asm/Assembler.kt` | 토큰을 두 번 훑어 바이트열로 바꾸는 2-pass 어셈블러 |
| `asm/Disassembler.kt` | 바이트열을 사람이 읽을 수 있는 텍스트로 되돌리는 역과정 |
| `Asm07Demo.kt` | 소스 → 토큰 → 심볼 → 바이트 → 실행을 한 번에 보여주는 main |
| `programs/add.sap1` | 우리가 어셈블할 첫 어셈블리 소스 |

5장·6장에서 만든 `AluFlags`, `Register`, `ProgramCounter`, `Instruction`, `Ram`, `Sap1`은
이번 장에서도 그대로 쓴다 — 어셈블러는 이들이 먹는 바이트를 생산할 뿐이다.

## 첫 어셈블리 소스

```
; SAP-1 program: 42 + 5 = 47
start:  LDA  $9
        ADD  $A
        OUT
        HLT
9:      $2A
A:      $05
```

이 소스에 들어 있는 문법 요소를 하나씩 보자.

- `; ...` — 줄 끝까지 무시되는 주석.
- `start:` — 심볼 라벨. 현재 주소를 가리킨다 (여기서는 0).
- `LDA $9` — 니모닉 + 16진수 피연산자. `$`는 hex 마커.
- `9:` / `A:` — **숫자 라벨**. "다음 데이터는 이 주소에 놓아라"는 뜻의 주소 디렉티브.
- `$2A`, `$05` — 데이터 바이트.

라벨이 십진수가 아니라 **16진수**로 해석되는 게 살짝 미묘하다.
이유는 SAP-1의 주소 공간이 4비트이기 때문이다 — 0..F가 자연스럽다.

## 왜 2-pass인가

한 번에 못 끝낼까? 못 끝낸다.

```
        LDA  data    ; data는 어디 있지?
        HLT
data:   $2A          ; 여기 — 주소 2
```

`LDA data`를 만나는 순간, 어셈블러는 아직 `data`의 주소를 모른다.
이걸 **forward reference**라고 부른다.
두 가지 길이 있다.

1. **One-pass + back-patching** — 일단 빈자리(`0x0?`)를 박아두고, `data:`를 만나면 돌아가서 채운다.
2. **Two-pass** — 첫 번째 패스에서 라벨의 주소만 모으고, 두 번째 패스에서 실제 바이트를 찍는다.

우리는 2-pass로 간다. 코드가 두 단계로 깔끔히 갈리고, 디버깅이 쉽다.
지금 단계에선 명령이 5개뿐이라 성능 차는 무의미하다.

```
[Source text]
     │
     ▼
   Lexer ──→  List<Token>
                 │
                 ▼
        Pass 1: 라벨 주소 수집
                 │
                 ▼
         symbols: { "start" → 0, ... }
                 │
                 ▼
        Pass 2: 토큰 → 바이트
                 │
                 ▼
            IntArray(16)
```

## Lexer — 한 줄씩 자르기

`Lexer.tokenize(source)`는 텍스트를 받아 `List<Token>`을 돌려준다.
토큰은 다섯 종류다.

```kotlin
sealed class Token {
    data class Label(val name: String) : Token()       // "start:"
    data class Mnemonic(val name: String) : Token()    // "LDA"
    data class Number(val value: Int) : Token()        // 9, $2A
    data class Identifier(val name: String) : Token()  // 심볼 참조
    data object Newline : Token()
}
```

세 가지만 기억하면 된다.

- `; ` 이후는 자른다 (주석 제거).
- 공백·콤마로 자른다.
- 각 조각을 위 5종에 매핑한다.

## Assembler — 두 번 훑기

Pass 1은 라벨을 모은다.

```kotlin
var addr = 0
for (line in lines) {
    while (line.firstIsLabel) {
        val name = line.popLabel()
        val numericAddr = name.toIntOrNull(16)
        if (numericAddr != null && line.isDataOnly) {
            addr = numericAddr               // 주소 디렉티브
        } else {
            symbols[name] = addr             // 심볼 라벨
        }
    }
    addr += sizeOf(line)
}
```

Pass 2는 토큰을 바이트로 바꾼다.
SAP-1은 명령이 한 바이트이므로 인코딩이 단순하다.

```kotlin
return (opcode shl 4) or (operandAddr and 0xF)
```

피연산자가 라벨이면 `symbols[name]`을 찾는다.
이미 Pass 1에서 다 모았으니 forward reference도 그냥 해결된다.

## Disassembler — 거꾸로

`Disassembler.bytesToText(bytes)`는 단순하다.
16바이트를 한 줄씩 돌면서, 각 바이트를 `Instruction.decode()`에 던지고
그 결과를 텍스트로 포맷한다.

```
$00: 0x09  LDA $9
$01: 0x1A  ADD $A
$02: 0xE0  OUT
$03: 0xF0  HLT
$04: 0x00  LDA $0
...
$09: 0x2A  SUB $A
$0A: 0x05  LDA $5
```

여기서 한 가지 짚을 게 있다.
`$09`에 있는 `0x2A`는 우리 의도로는 **데이터**(=42)지만,
디스어셈블러는 그것이 데이터인지 명령인지 모른다.
그래서 그대로 `SUB $A`로 해석한다.

이건 버그가 아니라 **자작 CPU의 본질**이다.
바이트는 그 자체로는 의미가 없다 — 어디서 PC가 그것을 fetch하느냐가 의미를 만든다.
디스어셈블러를 더 똑똑하게 만들려면 PC가 닿는 영역을 추적하는 **흐름 분석**이 필요하다.
이 책의 범위를 벗어나므로 지금은 "raw view"만 보여주고 넘어간다.

## 실행

```bash
./gradlew :chapter-07:run
```

기대 출력 (요약):

```
--- Bytes (16 hex) ---
0x09 0x1A 0xE0 0xF0 0x00 0x00 0x00 0x00 0x00 0x2A 0x05 0x00 ...
--- Execution ---
OUT = 47 (0x2F)
Cycles: 4
```

테스트:

```bash
./gradlew :chapter-07:test
```

## GitHub 산출물

```
chapter-07/
├── build.gradle.kts
├── README.md
└── src/
    ├── main/
    │   ├── kotlin/sap/ch07/
    │   │   ├── AluFlags.kt          (6장 그대로)
    │   │   ├── Bus.kt
    │   │   ├── Clock.kt
    │   │   ├── Controller.kt
    │   │   ├── Instruction.kt
    │   │   ├── ProgramCounter.kt
    │   │   ├── Ram.kt
    │   │   ├── Register.kt
    │   │   ├── Sap1.kt
    │   │   ├── Asm07Demo.kt         ← 신규
    │   │   └── asm/
    │   │       ├── Lexer.kt         ← 신규
    │   │       ├── Assembler.kt     ← 신규
    │   │       └── Disassembler.kt  ← 신규
    │   └── resources/programs/
    │       └── add.sap1             ← 신규
    └── test/kotlin/sap/ch07/
        ├── (6장 테스트 그대로)
        ├── LexerTest.kt             ← 신규
        ├── AssemblerTest.kt         ← 신규
        └── AsmEndToEndTest.kt       ← 신규
```

## 다음 장으로

명령 5개로는 곧 답답해진다.
"이 조건일 때 저쪽으로 점프해라"가 안 되면 같은 일을 반복할 수 없다.
변수가 16바이트밖에 안 되면 한 번에 다룰 수 있는 데이터도 너무 적다.

다음 장은 **SAP-2** — 256바이트 메모리, JMP/JNZ 분기 명령, 그리고 8개로 늘어난 ISA다.
그 순간 우리의 CPU는 **루프**를 돌릴 수 있게 된다.
어셈블러도 함께 진화한다 — 같은 2-pass 골격이 어디까지 버티는지 본다.

---

> 참고: Albert Paul Malvino & Jerald A. Brown, *Digital Computer Electronics* 3rd ed., 1992 — SAP-1 ISA 원전.
