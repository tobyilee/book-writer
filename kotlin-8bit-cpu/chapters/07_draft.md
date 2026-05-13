# 7장. 어셈블러와 디스어셈블러 — 사람의 글이 기계어가 되는 곳

처음 어셈블리어를 만났을 때를 떠올려보자. 학부 2학년 컴퓨터구조 시간, 강사가 칠판에 적은 한 줄.

```
LDA 9
ADD 10
OUT
HLT
```

옆 사람이 작은 목소리로 묻는다. "이거 이렇게 적으면 컴퓨터가 알아듣나?" 강사는 칠판 옆에 또 한 줄을 적는다. `0001 1001 / 0010 1010 / 1110 0000 / 1111 0000`. "이게 위 코드를 기계어로 옮긴 거다."

그 순간 우리 머릿속을 스친 질문이 있었다. **누가, 어떻게, 위 네 줄을 아래 네 줄로 바꾸는가?** 컴파일러는 알겠다 — Kotlin이 바이트코드가 되고 그 바이트코드가 어떤 기계 명령어가 된다는 흐름 정도는 안다. 그런데 어셈블리어와 기계어 사이는 너무 가깝다. 너무 가까워서 오히려 그 사이에 무엇이 일하는지가 보이지 않는다. `LDA`와 `0001`이 같은 것이라고? 누가 어디서 그 약속을 했나? 그 약속을 코드로 어떻게 적는가?

이 질문을 4년 동안 가슴 속에 묵혀두고 졸업한 사람도 적지 않을 것이다. 누군가는 OS 강의에서 어셈블리어 한 페이지를 더 만났고, 누군가는 GDB로 디버깅하다가 어셈블리 덤프를 본 적이 있을 것이다. 그러나 **"어셈블리어를 어떻게 기계어로 옮기는가"**는 학부 4년 동안 거의 다뤄지지 않는다. 답을 모르는 채로 우리는 그저 그 둘이 어쩌면 같은 것이라는 막연한 인상만 가지고 산다. 정말 찜찜한 일이다.

이 장에서 그 묵은 찜찜함을 풀어내 보자. 우리는 SAP-1을 6장에서 다 지었다. 이제 그 SAP-1 위에서 돌아갈 어셈블러를 손으로 짠다. 한 줄로 요약하면 이렇다. **사람이 적은 어셈블리어를 받아서 기계어 바이트 배열을 내놓는 함수 하나.** 그게 어셈블러의 정체다. 그 함수를 우리가 직접 짠다. 그러고 나서 그 어셈블러가 만든 바이트 배열을 우리가 6장에서 짠 SAP-1의 메모리에 올리고, 우리가 6장에서 짠 컨트롤러로 실행한다. **자기 손으로 짠 어셈블러로 자기 손으로 짠 CPU 위에서 자기 프로그램이 돌아간다.** 이 장의 마지막 줄에서 우리는 그 광경을 본다. 2부의 정서적 절정이다.

자, 시작해보자.

## 7.1 5바이트의 비밀 — 우리가 짤 첫 어셈블러의 입력과 출력

본격적으로 코드를 짜기 전에 우리가 만들 함수의 모양을 잡자. **입력은 무엇인가? 출력은 무엇인가?**

입력은 어셈블리 소스 코드 한 덩어리다. 멀티라인 문자열이다.

```
LDA 9
ADD 10
OUT
HLT
```

출력은 SAP-1 메모리에 그대로 올릴 수 있는 바이트 배열이다. 위 4줄짜리 프로그램의 출력은 4바이트다. (어 — 5바이트 아닌가? 잠시 후에 이 5바이트 이야기로 돌아간다. 우선은 4줄짜리 단순한 프로그램으로 시작한다.)

우리 어셈블러의 시그니처를 미리 적어두자.

```kotlin
class Assembler {
    fun assemble(source: String): ByteArray = TODO()
}
```

이 정도로 두고 시작하자. TDD 정신에 따라 함수 본문보다 테스트를 먼저 떠올리는 편이 낫다. 가장 단순한 테스트는 이렇다.

```kotlin
class AssemblerTest : FunSpec({
    val asm = Assembler()

    test("4줄짜리 프로그램이 4바이트로 어셈블된다") {
        val source = """
            LDA 9
            ADD 10
            OUT
            HLT
        """.trimIndent()

        val bytes = asm.assemble(source)
        bytes.size shouldBe 4
    }
})
```

이 한 줄이 우리의 첫 안전 그물이다. 빨간 줄이 뜨고, 우리는 그 빨간 줄을 초록 줄로 바꾸려고 어셈블러를 짠다.

그렇다면 위 4줄을 어떻게 4바이트로 바꿀까? SAP-1의 명령어 인코딩 약속을 한 번 다시 펴 보자.

| Mnemonic | Opcode (4비트) | Operand (4비트) | 의미 |
|----------|----------------|------------------|------|
| `LDA addr` | `0001` | 4비트 주소 | 메모리에서 A로 적재 |
| `ADD addr` | `0010` | 4비트 주소 | 메모리 값을 A에 더함 |
| `OUT` | `1110` | (무시) `0000` | A를 출력 레지스터로 |
| `HLT` | `1111` | (무시) `0000` | 정지 |

이 표 위에서 `LDA 9`를 한 바이트로 옮기는 길이 또렷이 보인다. opcode 4비트(`0001`) + operand 4비트(`1001`, 즉 9) = `0001 1001` = `0x19`. 같은 방식으로 4줄을 4바이트로 옮기면 이렇다.

```
LDA 9   →  0x19   (0001 1001)
ADD 10  →  0x2A   (0010 1010)
OUT     →  0xE0   (1110 0000)
HLT     →  0xF0   (1111 0000)
```

이 4바이트가 우리 어셈블러가 내놓아야 하는 출력이다. 손으로 한 번 직접 적어보자. 종이 위에 옮겨 적는 그 한 번이 머릿속에 회로 하나를 그려준다.

자, 그러면 5바이트 이야기는 어디서 오나? SAP-1의 가장 유명한 예제 프로그램은 다음과 같다.

```
LDA 9      ; 메모리 주소 9의 값을 A에 적재
ADD 10     ; 메모리 주소 10의 값을 A에 더함
OUT        ; A의 값을 출력 레지스터로
HLT        ; 정지
```

여기까지가 4바이트(주소 0~3). 그러면 주소 4~8은? 비워둔다. 그리고 주소 9에는 데이터 `0x03`(=3)을, 주소 10에는 데이터 `0x05`(=5)를 둔다. **명령어와 데이터가 같은 메모리에 산다**는 1장의 그 한 줄이 여기서 다시 살아 난다. 어셈블러가 만든 4바이트 명령어와, 우리가 손으로 적어둔 2바이트 데이터가 같은 16바이트 RAM에 함께 들어간다.

그래서 본격적인 SAP-1 프로그램의 어셈블러 출력은 보통 16바이트 전체를 채운다 — 명령어 + 0으로 채운 공백 + 데이터. 이 챕터의 마지막에서 우리는 그 16바이트 버전을 만들고, 6장에서 짠 SAP-1 위에 올리고, 결과로 `0x08`(=8 = 3 + 5)이 출력 레지스터에 적히는 광경을 본다. 약속하자. 거기까지 함께 가 보자.

## 7.2 사람의 글이 기계어가 되는 세 단계

어셈블러가 일하는 길은 사실 컴파일러가 일하는 길과 같다. 다만 단계가 훨씬 적을 뿐이다. 한 줄로 정리하면 이렇다.

```
소스 코드 (문자열)
      │
      │  ① Lexer — 토큰으로 자르기
      ▼
   토큰 배열
      │
      │  ② Parser — 의미 단위로 묶기 (이번 어셈블러에서는 매우 단순)
      ▼
   구문 트리 (우리는 List<Instruction>으로 간단히 대체)
      │
      │  ③ Code generation — 바이트로 옮기기
      ▼
   바이트 배열 (기계어)
```

학부에서 컴파일러 강의를 들은 사람이라면 위 그림이 익숙할 것이다. 들은 적이 없는 사람이라도 걱정하지 말자. 어셈블러는 이 그림 중 가장 단순한 형태다. **Parser와 Code generation의 사이가 거의 없다.** 한 줄의 어셈블리어가 한 바이트(또는 두세 바이트)의 기계어로 거의 1대1 대응되기 때문이다. 어셈블리어는 사실상 "사람이 읽기 좋게 적은 기계어"다. 이게 어셈블리어의 정체다.

그러나 1대1 대응에도 한 가지 함정이 있다 — **forward reference**. 점프 명령어가 자기보다 뒤에 있는 라벨을 가리킬 때 발생한다. 예를 들어 이런 코드.

```
        LDA counter
loop:
        ADD counter
        JMP done       ; ← done 라벨은 아직 정의되지 않았다
        HLT
done:
        OUT
        HLT
```

1번 줄을 어셈블할 때 `loop`이라는 라벨이 어디 있는지 아직 모른다. 4번 줄을 어셈블할 때 `done`이 어디 있는지 아직 모른다. **모르는 상태로 어셈블할 수는 없다.** 점프 명령어는 정확한 주소를 바이트로 적어야 한다.

이 문제를 푸는 표준 길이 **2-pass 어셈블러**다. 한 번 훑으면서 모든 라벨의 위치를 먼저 표로 만든다(1차 pass). 그러고 나서 다시 훑으면서 라벨을 주소로 치환해 바이트로 적는다(2차 pass). 두 번 훑으니까 2-pass다. 정직한 이름이다.

> **사이드바: 왜 3-pass가 필요한가?**
>
> 가변 길이 명령어를 가진 ISA에서는 2-pass로 부족할 때가 있다. 예를 들어 x86의 `JMP`는 짧은 점프(1바이트 오프셋, 총 2바이트)와 긴 점프(4바이트 오프셋, 총 5바이트)가 있다. 1차 pass에서 모든 점프를 짧은 점프로 가정하고 라벨 위치를 계산한다. 그런데 2차 pass에서 어떤 점프가 짧은 점프 범위를 넘는다는 사실이 발견되면, 그 점프를 긴 점프로 바꿔야 한다 — 그러면 명령어 길이가 늘어나고, 그 뒤에 따라오는 모든 라벨 위치가 한 칸씩 밀린다. 그래서 한 번 더 훑어야 한다. 3-pass다. GCC의 어셈블러 `as`가 실제로 이 알고리즘을 쓴다. SAP-1의 모든 명령어는 1바이트 고정이라 우리는 2-pass로 충분하다. 행운이다.

SAP-1의 어셈블러는 2-pass로 짜자. 그러면 1차 pass와 2차 pass가 무엇을 하는지 한 번 더 정리해두자.

- **1차 pass:** 토큰화 + 명령어 길이 계산 + **심볼 테이블 구축** (`Map<String, Int>`로 라벨 → 주소).
- **2차 pass:** 심볼 테이블을 보면서 forward reference 해결 + 바이트 생성.

이 골격을 따라가 보자.

## 7.3 Lexer — 사람의 글을 토큰으로 자른다

가장 먼저 짤 것은 토큰화다. 한 줄짜리 문자열을 의미 있는 조각들로 나누는 일. 예를 들어 `LDA 9`라는 문자열은 두 개의 토큰으로 나뉜다 — `LDA`(mnemonic)와 `9`(숫자). `loop: ADD counter`는 세 개의 토큰으로 — `loop:`(라벨), `ADD`(mnemonic), `counter`(심볼).

토큰을 Kotlin sealed class로 모델링하자.

```kotlin
sealed class Token {
    data class Mnemonic(val name: String) : Token()
    data class Number(val value: Int) : Token()
    data class Symbol(val name: String) : Token()
    data class Label(val name: String) : Token()
    object Newline : Token()
    object Eof : Token()
}
```

각 토큰이 어떤 모양인지가 타입으로 강제된다는 점이 핵심이다. `Mnemonic("LDA")`는 `Mnemonic`이고, `Number(9)`는 `Number`다. 이걸 `String` 하나로 다 다루려고 들면 코드가 곧 끔찍해진다. 한 번 데여 보면 안다.

Lexer 자체는 정규식과 `when` 표현식의 조합으로 짠다.

```kotlin
class Lexer(private val source: String) {
    private val lines = source.lines()

    fun tokenize(): List<Token> {
        val tokens = mutableListOf<Token>()

        for (rawLine in lines) {
            // 주석 제거 (; 이후의 문자 버리기)
            val line = rawLine.substringBefore(';').trim()
            if (line.isEmpty()) continue

            // 라벨 처리: "loop:" 같은 형태
            val (labelPart, rest) = if (':' in line) {
                val parts = line.split(':', limit = 2)
                parts[0].trim() to parts[1].trim()
            } else {
                null to line
            }
            if (labelPart != null) {
                tokens += Token.Label(labelPart)
            }

            // 나머지를 공백 기준으로 자른다
            val parts = rest.split(Regex("\\s+")).filter { it.isNotEmpty() }
            for (part in parts) {
                tokens += classify(part)
            }
            tokens += Token.Newline
        }
        tokens += Token.Eof
        return tokens
    }

    private fun classify(word: String): Token = when {
        word.uppercase() in MNEMONICS -> Token.Mnemonic(word.uppercase())
        word.matches(Regex("[0-9]+")) -> Token.Number(word.toInt())
        word.matches(Regex("0x[0-9a-fA-F]+")) -> Token.Number(word.substring(2).toInt(16))
        word.matches(Regex("[a-zA-Z_][a-zA-Z0-9_]*")) -> Token.Symbol(word)
        else -> error("알 수 없는 토큰: $word")
    }

    companion object {
        private val MNEMONICS = setOf("LDA", "ADD", "SUB", "OUT", "HLT", "JMP", "JZ", "JNZ")
    }
}
```

코드가 좀 길어 보이지만 핵심은 단순하다. **한 줄씩 읽으면서, 주석을 떼고, 라벨이 있으면 따로 빼고, 남은 단어들을 mnemonic/숫자/심볼로 분류한다.** 그게 전부다.

테스트도 함께 짜자.

```kotlin
class LexerTest : FunSpec({
    test("단순 LDA 9 토큰화") {
        val tokens = Lexer("LDA 9").tokenize()
        tokens shouldBe listOf(
            Token.Mnemonic("LDA"),
            Token.Number(9),
            Token.Newline,
            Token.Eof
        )
    }

    test("주석을 떼낸다") {
        val tokens = Lexer("LDA 9 ; load counter").tokenize()
        // 주석 이후는 무시
        tokens.filterIsInstance<Token.Symbol>() shouldBe emptyList()
    }

    test("라벨과 명령어가 한 줄에 있을 수 있다") {
        val tokens = Lexer("loop: ADD counter").tokenize()
        tokens shouldBe listOf(
            Token.Label("loop"),
            Token.Mnemonic("ADD"),
            Token.Symbol("counter"),
            Token.Newline,
            Token.Eof
        )
    }

    test("16진수 리터럴") {
        val tokens = Lexer("LDA 0x0A").tokenize()
        tokens.filterIsInstance<Token.Number>().single().value shouldBe 10
    }

    test("빈 줄은 무시한다") {
        val tokens = Lexer("\n\nHLT\n\n").tokenize()
        tokens.filterIsInstance<Token.Mnemonic>().single() shouldBe Token.Mnemonic("HLT")
    }
})
```

다섯 개의 테스트가 Lexer의 핵심 동작을 모두 잡는다. 다음으로 가자.

## 7.4 1차 pass — 심볼 테이블을 짓는다

토큰 배열을 손에 쥐었으니, 이제 라벨 → 주소의 표를 만들 차례다. 1차 pass의 일은 단 두 가지다.

1. **각 명령어가 메모리에서 차지하는 길이를 안다** (SAP-1은 모든 명령어가 1바이트, 그래서 단순).
2. **라벨이 등장하면 현재 주소를 표에 적는다.**

SAP-1은 모든 명령어가 1바이트 고정이라 매우 단순하다. 토큰 배열을 한 번 훑으면서 mnemonic을 만날 때마다 주소를 1 증가시킨다. 라벨을 만나면 그 시점의 주소를 표에 적는다.

```kotlin
class Assembler {
    private val mnemonicSize: Map<String, Int> = mapOf(
        "LDA" to 1, "ADD" to 1, "SUB" to 1,
        "OUT" to 1, "HLT" to 1,
        "JMP" to 1, "JZ" to 1, "JNZ" to 1
    )

    private fun buildSymbolTable(tokens: List<Token>): Map<String, Int> {
        val table = mutableMapOf<String, Int>()
        var addr = 0
        for (token in tokens) {
            when (token) {
                is Token.Label -> {
                    if (token.name in table) error("중복 라벨: ${token.name}")
                    table[token.name] = addr
                }
                is Token.Mnemonic -> {
                    addr += mnemonicSize[token.name]
                        ?: error("알 수 없는 mnemonic: ${token.name}")
                }
                else -> { /* 숫자, 심볼, 개행은 1차 pass에서 무시 */ }
            }
        }
        return table
    }
}
```

`when` 표현식의 패턴 매칭이 빛을 발하는 자리다. Kotlin sealed class를 토큰으로 쓰면 1차 pass의 본문이 정확히 "토큰 종류별로 무엇을 할지"만 적는 짧은 코드가 된다.

자, 1차 pass를 테스트해보자.

```kotlin
class SymbolTableTest : FunSpec({
    val asm = Assembler()

    test("라벨 없는 코드는 빈 표를 만든다") {
        val tokens = Lexer("LDA 9\nHLT").tokenize()
        asm.buildSymbolTable(tokens) shouldBe emptyMap()
    }

    test("라벨이 주소에 매핑된다") {
        val source = """
            LDA 9
            loop:
            ADD 10
            HLT
        """.trimIndent()
        val tokens = Lexer(source).tokenize()
        asm.buildSymbolTable(tokens) shouldBe mapOf("loop" to 1)
        // LDA가 0번지, loop은 1번지(ADD 자리), HLT는 2번지
    }

    test("여러 라벨이 정확한 주소에 매핑된다") {
        val source = """
            start:
            LDA 14
            loop:
            ADD 15
            JMP loop
            done:
            OUT
            HLT
        """.trimIndent()
        val tokens = Lexer(source).tokenize()
        asm.buildSymbolTable(tokens) shouldBe mapOf(
            "start" to 0,
            "loop" to 1,
            "done" to 3
        )
    }

    test("중복 라벨은 에러를 던진다") {
        val source = """
            loop:
            HLT
            loop:
            HLT
        """.trimIndent()
        val tokens = Lexer(source).tokenize()
        shouldThrow<IllegalStateException> {
            asm.buildSymbolTable(tokens)
        }
    }
})
```

이 네 개의 테스트가 1차 pass의 핵심을 잡는다. 특히 세 번째 테스트가 흥미롭다 — 라벨이 여러 줄에 걸쳐 있을 때 각 라벨의 주소가 정확히 어디인지 사람이 손으로 계산해서 표로 옮기는 일이 1차 pass가 하는 정확한 일이다. 손으로 한 번 그 표를 그려보면 코드가 무엇을 하는지 머릿속에 또렷이 새겨진다.

## 7.5 2차 pass — 바이트를 생성한다

심볼 테이블이 준비됐다. 이제 토큰을 다시 한 번 훑으면서, 각 명령어를 1바이트로 옮기자. 라벨이 등장하면 심볼 테이블에서 주소를 가져온다.

명령어를 sealed class로 모델링해서 본문이 패턴 매칭으로 깔끔하게 떨어지게 하자.

```kotlin
sealed class Instruction(val opcode: Int) {
    data class Lda(val addr: Int) : Instruction(0x10)
    data class Add(val addr: Int) : Instruction(0x20)
    data class Sub(val addr: Int) : Instruction(0x30)
    object Out : Instruction(0xE0)
    object Hlt : Instruction(0xF0)
    data class Jmp(val addr: Int) : Instruction(0x40)
    data class Jz(val addr: Int) : Instruction(0x50)
    data class Jnz(val addr: Int) : Instruction(0x60)

    fun encode(): Byte = when (this) {
        is Lda -> (opcode or (addr and 0x0F)).toByte()
        is Add -> (opcode or (addr and 0x0F)).toByte()
        is Sub -> (opcode or (addr and 0x0F)).toByte()
        is Jmp -> (opcode or (addr and 0x0F)).toByte()
        is Jz  -> (opcode or (addr and 0x0F)).toByte()
        is Jnz -> (opcode or (addr and 0x0F)).toByte()
        is Out -> opcode.toByte()
        is Hlt -> opcode.toByte()
    }
}
```

각 명령어가 자기 opcode를 알고 있고, `encode()`로 자기 자신을 한 바이트로 옮긴다. opcode와 operand를 `or`로 한 바이트에 합치는 한 줄 — 비트 연산이 이렇게 쓰인다는 사실이 손에 잡힌다.

이제 2차 pass의 본체.

```kotlin
class Assembler {
    // 1차 pass는 위에서 짰다

    fun assemble(source: String): ByteArray {
        val tokens = Lexer(source).tokenize()
        val symbolTable = buildSymbolTable(tokens)
        return generateBytes(tokens, symbolTable)
    }

    private fun generateBytes(
        tokens: List<Token>,
        symbolTable: Map<String, Int>
    ): ByteArray {
        val bytes = mutableListOf<Byte>()
        var i = 0
        while (i < tokens.size) {
            val token = tokens[i]
            when (token) {
                is Token.Label -> i++  // 라벨은 1차 pass에서 처리했으니 건너뛴다
                is Token.Mnemonic -> {
                    val (instr, consumed) = parseInstruction(tokens, i, symbolTable)
                    bytes += instr.encode()
                    i += consumed
                }
                is Token.Newline, Token.Eof -> i++
                else -> error("예상하지 못한 토큰: $token (위치 $i)")
            }
        }
        return bytes.toByteArray()
    }

    private fun parseInstruction(
        tokens: List<Token>,
        start: Int,
        symbolTable: Map<String, Int>
    ): Pair<Instruction, Int> {
        val mnemonic = (tokens[start] as Token.Mnemonic).name
        return when (mnemonic) {
            "LDA" -> Instruction.Lda(resolveOperand(tokens[start + 1], symbolTable)) to 2
            "ADD" -> Instruction.Add(resolveOperand(tokens[start + 1], symbolTable)) to 2
            "SUB" -> Instruction.Sub(resolveOperand(tokens[start + 1], symbolTable)) to 2
            "JMP" -> Instruction.Jmp(resolveOperand(tokens[start + 1], symbolTable)) to 2
            "JZ"  -> Instruction.Jz (resolveOperand(tokens[start + 1], symbolTable)) to 2
            "JNZ" -> Instruction.Jnz(resolveOperand(tokens[start + 1], symbolTable)) to 2
            "OUT" -> Instruction.Out to 1
            "HLT" -> Instruction.Hlt to 1
            else -> error("알 수 없는 mnemonic: $mnemonic")
        }
    }

    private fun resolveOperand(
        token: Token,
        symbolTable: Map<String, Int>
    ): Int = when (token) {
        is Token.Number -> token.value
        is Token.Symbol -> symbolTable[token.name]
            ?: error("정의되지 않은 심볼: ${token.name}")
        else -> error("operand로 올 수 없는 토큰: $token")
    }
}
```

`resolveOperand` 함수가 핵심이다 — operand가 숫자면 그대로 쓰고, 심볼이면 심볼 테이블에서 주소를 가져온다. **forward reference가 여기서 자연스럽게 해결된다.** 1차 pass에서 모든 라벨의 주소를 미리 알아두었으니, 2차 pass에서는 그저 표를 보고 치환만 하면 된다. 두 pass로 나눈 이유가 이 한 줄에 있다.

e2e 테스트 한 줄을 짜자.

```kotlin
class AssemblerE2ETest : FunSpec({
    val asm = Assembler()

    test("4줄짜리 LDA/ADD/OUT/HLT 프로그램이 정확한 바이트로 어셈블된다") {
        val source = """
            LDA 9
            ADD 10
            OUT
            HLT
        """.trimIndent()

        val bytes = asm.assemble(source)
        bytes.toList().map { it.toInt() and 0xFF } shouldBe listOf(
            0x19, 0x2A, 0xE0, 0xF0
        )
    }

    test("라벨이 포함된 점프 프로그램") {
        val source = """
            LDA 14
            loop:
            ADD 15
            JMP loop
            HLT
        """.trimIndent()

        val bytes = asm.assemble(source)
        bytes.toList().map { it.toInt() and 0xFF } shouldBe listOf(
            0x1E,   // LDA 14
            0x2F,   // ADD 15
            0x41,   // JMP loop (loop은 1번지)
            0xF0    // HLT
        )
    }
})
```

두 테스트가 통과하는 순간, 우리 어셈블러가 **사람의 글을 기계어로 옮기는 일**을 정확히 해낸다는 사실이 우리 손에 잡힌다. 한 줄로 정리하면 그게 어셈블러의 정체다.

## 7.6 디스어셈블러 — 역방향으로 가 보자

어셈블러를 다 짰으니 그 반대 방향도 짜 보자. **바이트 → mnemonic.** 메모리 덤프를 사람이 읽을 수 있게 옮기는 일. 디버거의 핵심 부품이고, 다른 사람의 SAP-1 프로그램을 읽어볼 때 결정적인 도구다.

다행히 디스어셈블러는 어셈블러보다 훨씬 단순하다. 1-pass면 충분하고, 라벨 추정 같은 까다로운 일도 없다(라벨을 다시 만드는 디스어셈블러도 있지만 우리는 일단 mnemonic만 복원한다).

```kotlin
class Disassembler {
    fun disassemble(bytes: ByteArray): String {
        val lines = mutableListOf<String>()
        for ((i, b) in bytes.withIndex()) {
            val byte = b.toInt() and 0xFF
            val opcode = byte and 0xF0
            val operand = byte and 0x0F
            val mnemonic = when (opcode) {
                0x10 -> "LDA $operand"
                0x20 -> "ADD $operand"
                0x30 -> "SUB $operand"
                0x40 -> "JMP $operand"
                0x50 -> "JZ $operand"
                0x60 -> "JNZ $operand"
                0xE0 -> "OUT"
                0xF0 -> "HLT"
                else -> ".db 0x${byte.toString(16).padStart(2, '0').uppercase()}"
            }
            lines += "0x${i.toString(16).padStart(2, '0')}:  $mnemonic"
        }
        return lines.joinToString("\n")
    }
}
```

상위 4비트로 opcode를 추출하고, 하위 4비트로 operand를 추출한다. `byte and 0xF0`, `byte and 0x0F` 두 줄이 그 모든 일을 한다. 알 수 없는 opcode는 `.db 0xNN` 형태로 적어둔다 — 명령어가 아닌 데이터일 수도 있으니까.

테스트.

```kotlin
class DisassemblerTest : FunSpec({
    val disasm = Disassembler()

    test("어셈블러의 출력을 그대로 다시 사람의 글로 옮긴다") {
        val bytes = byteArrayOf(0x19, 0x2A.toByte(), 0xE0.toByte(), 0xF0.toByte())
        disasm.disassemble(bytes) shouldBe """
            0x00:  LDA 9
            0x01:  ADD 10
            0x02:  OUT
            0x03:  HLT
        """.trimIndent()
    }

    test("데이터 바이트는 .db로 적힌다") {
        val bytes = byteArrayOf(0x19, 0x03)
        disasm.disassemble(bytes) shouldBe """
            0x00:  LDA 9
            0x01:  .db 0x03
        """.trimIndent()
    }
})
```

흥미로운 점 하나. **디스어셈블러는 명령어와 데이터를 구별할 수 없다.** 16번지에 `0x19`라는 바이트가 적혀 있으면, 그게 `LDA 9`라는 명령어인지 그저 25라는 정수 데이터인지 디스어셈블러는 모른다. 그저 옵코드로 해석해서 보여 줄 뿐이다. **명령어와 데이터가 같은 메모리에 산다**는 von Neumann 아키텍처의 그 한 줄이 디스어셈블러에서 정확히 이런 형태로 다시 등장한다. 1장에서 우리가 짚었던 그 한 줄이 7장에서 다시 손에 잡힌다. 기분 좋은 일이다.

> **사이드바: 8086 시대의 어셈블러는 어떻게 가변 길이를 다루나?**
>
> 8086의 명령어는 1바이트부터 6바이트까지 가변이다. `MOV AX, 0x1234`는 3바이트, `JMP 0x1000`은 5바이트, `NOP`은 1바이트. 이 가변 길이가 어셈블러를 까다롭게 만든다. 1차 pass에서 모든 점프를 짧은 점프(2바이트)로 가정하고 라벨 위치를 계산하고, 2차 pass에서 짧은 점프 범위를 벗어난 점프를 긴 점프(5바이트)로 바꾼다. 그러면 그 점프 뒤의 라벨 주소가 모두 3바이트씩 밀린다. 그래서 3차 pass가 필요해진다. 더 심한 경우 GCC의 `as`처럼 "수렴할 때까지 반복"하는 알고리즘을 쓰기도 한다. SAP-1의 1바이트 고정 길이가 우리에게 얼마나 친절한지가 이 사이드바에서 또렷이 보인다. 11장에서 8086 어셈블리를 직접 만날 때, 이 사이드바를 다시 떠올려보자.

> **사이드바: Z80과 8080의 어셈블러 mnemonic 차이**
>
> Z80은 8080의 binary 상위 호환이지만 어셈블리 mnemonic은 다르다. 8080에서 `MOV A, B`라고 적는 명령어를 Z80에서는 `LD A, B`라고 적는다. opcode는 같은 `0x78`이지만 사람이 읽는 글자가 다르다. 둘 다 같은 비트 패턴을 메모리에 적는 그저 다른 이름들이다. 어셈블러는 결국 **약속의 표를 적용하는 함수**일 뿐이라는 사실이 여기서도 또렷하다. 누가 어떤 약속을 정해두었느냐가 어셈블리어의 모양을 결정한다. 같은 칩에 다른 두 어셈블러를 짤 수도 있다(실제로 1970년대 후반에 둘이 공존했다). 11장에서 같은 Fibonacci 코드를 8080·Z80 두 가지로 비교할 때 이 차이가 분명히 드러난다.

## 7.7 자기 어셈블러로 짠 프로그램이 자기 SAP-1 위에서 돌아간다

자, 이 장의 정서적 절정에 도착했다. 우리가 짠 어셈블러로 SAP-1 첫 프로그램을 어셈블하고, 그 바이트 배열을 6장에서 짠 SAP-1의 메모리에 올리고, 실행한다.

전체 흐름을 짧은 코드로 정리하면 이렇다.

```kotlin
fun main() {
    // ① 사람의 글 — 어셈블리 소스
    val source = """
        LDA 9      ; A에 메모리 9의 값 적재
        ADD 10     ; A에 메모리 10의 값 더함
        OUT        ; A를 출력 레지스터로
        HLT        ; 정지
    """.trimIndent()

    // ② 어셈블러가 사람의 글을 4바이트의 0과 1로 옮긴다
    val program = Assembler().assemble(source)
    println("Assembled bytes: ${program.joinToString(" ") {
        "0x${(it.toInt() and 0xFF).toString(16).uppercase().padStart(2, '0')}"
    }}")
    // → Assembled bytes: 0x19 0x2A 0xE0 0xF0

    // ③ SAP-1의 16바이트 RAM을 짓는다 — 명령어 4바이트 + 공백 5바이트 + 데이터 2바이트 + 공백
    val ram = IntArray(16)
    program.forEachIndexed { i, b -> ram[i] = b.toInt() and 0xFF }
    ram[9]  = 0x03   // 데이터: 3
    ram[10] = 0x05   // 데이터: 5

    // ④ SAP-1을 6장에서 짠 그대로 켠다
    val cpu = Sap1(ram)
    cpu.run()

    // ⑤ 결과를 출력 레지스터에서 꺼낸다
    println("Output: ${cpu.out.value}")
    // → Output: 8
}
```

이 17줄짜리 `main` 함수가 우리가 2부 내내 손으로 짠 모든 것을 한 번에 보여 준다. 사람의 글이 어셈블러를 거쳐 바이트가 되고, 그 바이트가 SAP-1 메모리에 올라가고, 컨트롤러가 한 박자씩 명령어를 꺼내 실행하고, ALU가 더하기를 하고, 결과가 출력 레지스터에 적힌다. **3 + 5 = 8.** 가장 작은 수의 가장 단순한 덧셈. 그러나 그 한 줄을 우리가 짠 CPU와 어셈블러가 함께 만들어냈다.

이 순간이 학부 시절의 그 묵은 찜찜함을 풀어내는 자리다. `LDA 9`라는 글자가 어떻게 `0x19`가 되는지를 더 이상 모를 수 없다. 우리가 그 변환 함수를 손으로 짰기 때문이다. 그 변환 함수를 돌리는 컴퓨터는 또 우리가 짠 SAP-1이다. **어셈블리어**라는 단어가 더 이상 신비한 외래어로 들리지 않을 것이다. 그저 우리가 적는 한 줄의 텍스트에 불과하다. 그게 어셈블리어의 정체였다.

e2e 테스트로 이 흐름을 검증해두자.

```kotlin
class AssembleAndRunTest : FunSpec({
    test("어셈블해서 실행하면 3 + 5 = 8이 출력된다") {
        val source = """
            LDA 9
            ADD 10
            OUT
            HLT
        """.trimIndent()

        val program = Assembler().assemble(source)
        val ram = IntArray(16).apply {
            program.forEachIndexed { i, b -> this[i] = b.toInt() and 0xFF }
            this[9] = 3
            this[10] = 5
        }

        val cpu = Sap1(ram)
        cpu.run()

        cpu.out.value shouldBe 8
    }

    test("어셈블해서 디스어셈블하면 mnemonic이 거의 그대로 복원된다") {
        val source = """
            LDA 9
            ADD 10
            OUT
            HLT
        """.trimIndent()

        val program = Assembler().assemble(source)
        val recovered = Disassembler().disassemble(program)
        recovered shouldContain "LDA 9"
        recovered shouldContain "ADD 10"
        recovered shouldContain "OUT"
        recovered shouldContain "HLT"
    }
})
```

이 두 e2e 테스트가 통과하면 — 정확히 그 순간에 — 우리는 **자기가 짠 SAP-1 위에서 자기가 짠 어셈블러로 어셈블한 프로그램이 도는 광경**을 손에 쥔다. 학부 2학년의 그 멍한 표정이 풀어진다. 이 묵은 질문이 풀어진다. 정말 즐거운 순간이다.

## 7.8 한 챕터를 마치며 — 2부의 끝에서

이번 장에서 우리가 손에 쥔 것을 정리해보자.

첫째, **어셈블러란 단순한 함수다.** 입력이 문자열, 출력이 바이트 배열인 함수. 그 사이를 잇는 길은 Lexer → 1차 pass(심볼 테이블) → 2차 pass(바이트 생성)라는 세 단계다. **컴파일러의 가장 단순한 형태**가 어셈블러다.

둘째, **forward reference 때문에 2-pass가 필요하다.** 한 번 훑으면서 라벨 위치를 표로 만들고, 다시 훑으면서 라벨을 주소로 치환한다. 가변 길이 명령어가 있는 ISA에서는 3-pass가 필요한 이유도 함께 봤다.

셋째, **디스어셈블러는 거꾸로 가는 길이다.** 단순한 1-pass면 충분하다. 다만 명령어와 데이터를 구별할 수 없다는 von Neumann의 본질적 한계가 디스어셈블러의 출력에 그대로 드러난다는 점이 흥미롭다.

넷째 — 이게 이 장의 진짜 보상이다 — **자기 어셈블러로 짠 프로그램이 자기 SAP-1 위에서 돌아가는 광경**을 우리는 직접 봤다. 학부 시절의 그 묵은 찜찜함이 풀어졌다. 어셈블리어는 더 이상 외래어가 아니다. 우리가 적은 텍스트가 우리가 짠 함수로 바이트가 되고, 우리가 짠 CPU가 그 바이트를 한 박자씩 실행한다. 처음부터 끝까지 우리 손이다. 정말 환한 순간이다.

기억해두자. **여기서 우리가 짠 어셈블러는 그저 SAP-1 어셈블러일 뿐이지만, 이 골격은 모든 어셈블러에 그대로 적용된다.** 8086의 `MASM`도, ARM의 `as`도, 우리가 짠 골격을 가변 길이에 맞춰 확장한 것이다. RISC-V의 `gas`도 마찬가지다. 컴파일러로 가는 첫 발판이 우리 손에 들어왔다.

자, 2부의 끝이다. 한 발 멈춰서 우리가 어디까지 왔는지 돌아보자.

- 3장에서 SAP-1의 청사진을 그렸다.
- 4장에서 레지스터와 ALU를 짰다.
- 5장에서 overflow의 무덤을 통과했다.
- 6장에서 모든 모듈을 하나의 컨트롤러 아래 묶었다. SAP-1이 처음 돌아갔다.
- 7장에서 그 SAP-1 위에서 돌아갈 어셈블러까지 짰다.

**2부 끝에서 우리는 16바이트 메모리, 5~8개 명령어, 1개 누산기를 가진 한 대의 컴퓨터와 그 컴퓨터의 어셈블러를 손에 쥐었다.** 이 한 줄이 9주 동안의 산행을 정리한다. 3부로 넘어가면 이 16바이트 우주가 좁아진다. **5개에서 39개로** — SAP-2가 우리를 부른다. 16바이트가 64KB가 되고, 누산기 하나가 범용 레지스터 세 개로 늘어나며, 컨트롤러가 마이크로코드로 다시 짜인다. 새 산이다. 또 한 번 같이 올라가 보자.

> **GitHub 산출물**
>
> - 파일: `chapter-07/sap1/asm/Lexer.kt`, `chapter-07/sap1/asm/Assembler.kt`, `chapter-07/sap1/asm/Disassembler.kt`
> - 테스트: `LexerTest.kt`(5개), `SymbolTableTest.kt`(4개), `AssemblerE2ETest.kt`(2개), `DisassemblerTest.kt`(2개), `AssembleAndRunTest.kt`(2개) — 합계 ~15개
> - 실행 커맨드: `./gradlew :chapter-07:test`, `./gradlew :chapter-07:run` (3 + 5 = 8 데모 실행)
> - 2부의 절정. 3부 8장에서 SAP-2의 근본 재설계를 만난다.
