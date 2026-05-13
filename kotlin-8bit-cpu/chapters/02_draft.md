# 2장. fetch-decode-execute를 Kotlin 30줄로

처음 CPU를 공부할 때를 떠올려보자. 교과서를 펴면 어김없이 등장하는 그림이 있다. 박스 하나에는 "CU", 다른 박스에는 "ALU", 그 옆으로 "Registers", "Memory", 그리고 그 사이를 잇는 굵은 화살표 몇 개. 화살표에는 "data bus", "address bus", "control bus"라는 라벨이 점잖게 붙어 있다. 우리는 그 그림을 보고 고개를 끄덕인다. "아, CPU는 이렇게 생겼구나." 그러고는 다음 페이지로 넘어간다.

그런데 솔직히 말해서, 그 그림을 보고 "CPU가 어떻게 동작하는가"가 손에 잡혔는가? 박스와 화살표만 봐서는 어딘가 찜찜하다. 화살표 위에 무엇이 흐르는지, 박스 안에서 무슨 일이 벌어지는지, 그 흐름이 시간 축 위에서 어떤 순서로 일어나는지 — 그림 한 장으로는 도저히 보이지 않는다. 무언가를 안 것 같은데 실은 아무것도 안 것이 없다. 가장 흔한 함정이다.

그렇다면 어떻게 해야 할까? 가장 빠른 길은 그 동작을 코드로 직접 짜보는 것이다. 그것도 아주 짧게. 30줄짜리 Kotlin 코드 안에 "CPU가 한 명령어를 처리하는 한 박자"를 통째로 담아본다. 박스와 화살표로 흐릿하던 것이 갑자기 함수 호출 세 줄로 또렷해진다. 이번 장 끝에 우리는 처음으로 "돌아가는 무엇"을 손에 쥐게 될 것이다.

## CPU의 가장 작은 심장 박동

먼저 한 가지 질문에서 시작하자. CPU가 "동작한다"라는 말은 정확히 무엇을 뜻하는가?

답은 의외로 간단하다. CPU는 켜진 뒤부터 꺼질 때까지 같은 일을 끝없이 반복한다. 메모리에서 명령어 한 줄을 가져온다(fetch). 그것이 무슨 뜻인지 해석한다(decode). 그리고 그 뜻대로 실행한다(execute). 그게 전부다. 이 세 박자가 CPU의 심장 박동이다. 1945년 폰 노이만이 *EDVAC* 보고서에서 이 골격을 적어 둔 뒤 [논문-1], 지금 우리가 쓰는 모든 일반 컴퓨터가 이 박동 위에서 돌고 있다.

말로만 들으면 추상적이다. 그래서 좀 더 구체적으로 풀어보자. 책상 위에 일감이 종이 한 묶음으로 쌓여 있다고 상상해보자. 우리는 한 손으로 종이를 하나씩 집어 든다. 다른 손으로 그 종이의 명령을 읽는다. "1번 항목과 2번 항목을 더하라." 그러면 우리는 그대로 한다. 그러고 나서 다음 종이를 집어 든다. 이걸 종이가 다 떨어질 때까지, 혹은 "끝(HLT)"이라고 적힌 종이를 만날 때까지 계속한다. CPU도 정확히 이렇게 일한다. 종이 묶음이 메모리이고, "지금 몇 번째 종이를 집을 차례인가"를 기억하는 작은 변수가 프로그램 카운터(PC)다.

이 비유에서 한 가지 더 짚어두자. "종이를 집어 든다"와 "종이를 읽고 해석한다"는 사실 별개의 동작이다. 종이를 집는 단계에서는 그것이 더하기 명령인지 빼기 명령인지 따지지 않는다. 그저 손에 가져올 뿐이다. 손에 들고 난 뒤에야 비로소 글자를 읽고 의미를 따진다. 이 두 단계를 분리해서 보는 시야가 중요하다. 분리해야 코드가 단순해지고, 분리해야 나중에 우리가 짤 SAP-1 시뮬레이터의 데이터패스 그림이 머릿속에 또렷이 들어온다.

### fetch, decode, execute — 세 박자의 정체

좀 더 정확히 적어보자. 표준 교과서가 정의하는 사이클은 다음과 같이 흐른다 [웹-자료15].

1. **fetch**: PC가 가리키는 메모리 주소에서 명령어를 읽어와 명령어 레지스터(IR)에 싣는다. 동시에 PC는 다음 명령어를 가리키도록 1 증가한다.
2. **decode**: IR 안에 들어 있는 비트열을 해석해 "어떤 종류의 명령어인지", "피연산자는 어디에 있는지"를 알아낸다.
3. **execute**: 해석된 의미대로 ALU를 가동시키거나 레지스터 값을 옮기거나 메모리에 쓴다.

> "The Fetch-Execute cycle... was first introduced by John von Neumann. This cycle starts when the computer is turned on and keeps repeating until the computer is shut down." (Baeldung CS [웹-자료15])

이 세 박자가 머릿속에서 분리되어 또렷해졌다면, 다음 단계는 가볍게 흘러간다. 30줄짜리 Kotlin 코드 안에 이 세 박자가 각자의 함수로 자리 잡게 만들면 그만이다.

## 30줄짜리 CPU를 짜보자

이제 손을 움직일 차례다. 우리가 만들 미니 CPU의 명세는 다음과 같다. 일부러 끔찍하게 작게 잡았다.

- **메모리**: 4바이트. 그 이상도 그 이하도 아니다.
- **레지스터**: 누산기(A) 단 하나. PC 하나.
- **명령어**: 두 개만 둔다.
  - `ADD addr` — 메모리 `addr` 번지의 값을 A에 더한다.
  - `HLT` — 정지한다.

명령어가 두 개뿐이라니 너무 시시한 것 아닌가 싶을 수 있다. 하지만 잠시만 참아보자. 이 시시함이 우리가 챙겨야 할 진짜 알맹이를 가려준다. CPU의 골격은 명령어가 2개든 200개든 똑같다. 명령어를 100개 추가해봐야 `when` 분기가 길어질 뿐이다. 골격을 먼저 잡고, 그 위에 살을 붙이는 편이 낫다.

명령어 인코딩도 단순하게 가자. 한 바이트(8비트) 안에 다 욱여넣는다.

- 상위 4비트: opcode. `0x1` = `ADD`, `0xF` = `HLT`.
- 하위 4비트: 피연산자 주소(0~3). HLT는 이 자리를 무시한다.

이 정도면 종이 한 장에 그릴 수 있을 만큼 작다. 그렇다면 이걸 Kotlin으로 옮겨보자.

### 첫 번째 시도 — 한 덩어리로

먼저 가장 직접적인 형태로 적어보자. 클래스 하나, 메서드 세 개, `while` 루프 하나. 군더더기 없이.

```kotlin
class MiniCpu(private val memory: IntArray) {
    private var pc: Int = 0
    private var a: Int = 0
    private var halted: Boolean = false

    fun run() {
        while (!halted) {
            val instruction = fetch()
            val (opcode, operand) = decode(instruction)
            execute(opcode, operand)
        }
    }

    private fun fetch(): Int {
        val byte = memory[pc] and 0xFF
        pc = (pc + 1) and 0x03   // 4바이트 메모리 → wrap-around
        return byte
    }

    private fun decode(instruction: Int): Pair<Int, Int> {
        val opcode = (instruction shr 4) and 0x0F
        val operand = instruction and 0x0F
        return opcode to operand
    }

    private fun execute(opcode: Int, operand: Int) {
        when (opcode) {
            0x1 -> a = (a + (memory[operand] and 0xFF)) and 0xFF   // ADD
            0xF -> halted = true                                    // HLT
            else -> error("알 수 없는 opcode: 0x${opcode.toString(16)}")
        }
    }

    fun accumulator(): Int = a
}
```

다 합쳐서 본문 30줄 남짓. CPU 한 대가 손바닥 위에 올라온다. 우리가 처음에 본 박스와 화살표 그림 — `while` 루프가 한가운데에 있고, `fetch`·`decode`·`execute`가 화살표를 따라 차례로 호출되는 그 그림이 코드 그대로다.

이 코드에는 몇 가지 약속이 숨어 있다. 살펴보자.

- **`Int`로 들고 다니고, 매번 `and 0xFF`로 마스크한다.** JVM에서 `Byte`는 부호 있는 -128~127이라서 자연어와 어긋난다. 그러다 보면 `byte == 0xFF`가 `false`를 내뱉고는 한다. 끔찍한 일이다. 그래서 본 책 전반부는 일단 `Int + 마스킹` 정책으로 간다. 가독성과 호환성이 좋다는 이유가 크다. UByte 카드는 4장에서 본격적으로 다시 꺼낼 예정이다 [§5.1].
- **PC 증가는 `(pc + 1) and 0x03`.** 메모리가 4바이트뿐이라 주소가 4 이상으로 튀어 오르면 곤란하다. wrap-around로 둘러서 가두자. SAP-1으로 가면 4비트 주소 폭이 자연스럽게 같은 효과를 낸다.
- **HLT의 피연산자 자리는 무시.** `execute`에서 opcode만 보고 종료시키니 operand가 무엇이든 상관없다. 다만 인코딩 자체는 8비트를 채워 둔다 — 어차피 메모리 슬롯 하나니까.

### 한번 돌려보자

말로만 CPU를 짜는 것은 의미가 없다. 직접 돌려보자. `main` 함수 한 줄을 곁들이면 된다.

```kotlin
fun main() {
    // 메모리 레이아웃:
    //   [0] 0x12  → ADD memory[2]  (A += 7)
    //   [1] 0x13  → ADD memory[3]  (A += 35)
    //   [2] 0x07  → 데이터: 7
    //   [3] 0x23  → 데이터: 35

    val program = intArrayOf(0x12, 0x13, 0x07, 0x23)
    val cpu = MiniCpu(program)
    cpu.run()
    println("A = ${cpu.accumulator()}")   // 출력: A = 42
}
```

`./gradlew :chapter-02:run`을 두드리면 `A = 42`가 콘솔에 떨어진다. 별 것 아니지만, 별 것 아닌 것이 아니다. 우리가 손수 짠 30줄짜리 CPU가 자기 메모리 위에서 두 명령어를 차례로 가져와, 해석하고, 누산기에 더한 결과를 내놓은 것이다. 폰 노이만 사이클의 모든 박자가 우리 코드 위에서 한 차례 뛰었다.

이 작은 성공의 무게를 잠시 음미하자. 이 책의 정체성은 "코드로 짓는다"는 한 줄로 요약된다. 그 첫 커밋이 방금 떨어졌다. 앞으로 13개 챕터에 걸쳐 이 작은 심장이 점점 커진다. SAP-1으로 옮겨가면 16바이트 메모리에 5개 명령어가 붙고, SAP-2로 가면 64K 메모리에 39개 명령어가 붙고, 마지막엔 우리의 8비트 RISC가 등장한다. 모두가 이 30줄 위에 한 단계씩 쌓이는 이야기다.

## while 루프와 데이터패스의 매핑

코드를 다시 한번 들여다보자. `run()`의 본체가 어떻게 생겼는지.

```kotlin
fun run() {
    while (!halted) {
        val instruction = fetch()
        val (opcode, operand) = decode(instruction)
        execute(opcode, operand)
    }
}
```

세 줄이다. 그런데 이 세 줄이 1장에서 본 폰 노이만 데이터패스의 흐름을 그대로 따라간다. fetch는 PC → MAR → 메모리 read → MDR로 이어지는 경로다. decode는 MDR이 IR로 가서 컨트롤러가 비트 패턴을 보고 어떤 신호를 켤지 결정하는 단계다. execute는 ALU나 레지스터 사이의 데이터 이동, 또는 컨트롤 플래그(HLT 같은)를 건드리는 단계다.

데이터패스 그림에서 박스와 화살표로 그려졌던 모든 것이 이 세 줄 안에 압축되어 있다. 박스는 메서드의 지역 변수나 클래스 필드가 되고, 화살표는 메서드 호출이 된다. 그렇다면 데이터패스의 "버스"는 어디에 있는가? 우리 코드에서 버스는 메서드 인자다. `execute(opcode, operand)`의 두 인자가 W-bus가 운반하는 데이터에 해당한다. 단순한 매핑이지만 한 번 머릿속에 자리 잡으면 SAP-1으로 넘어갈 때 흐름이 한결 매끄러워진다 [§5.4].

### 박자 사이를 비울까, 채울까

물론, 어떤 사람은 이 코드를 보고 "이건 너무 추상적이다"라고 할지 모른다. 실제 CPU는 한 명령어를 6개의 T-state로 쪼개 처리하는데, 우리는 한 함수 호출로 명령어를 끝내고 있다. 그 사이의 마이크로 동작 — `Eo Lm`(PC out, MAR load), `Er`(RAM out), `La Eu`(ALU out, A load) 같은 컨트롤 신호의 순서 — 이 통째로 사라졌다. 이게 과연 CPU인가?

물론 맞는 지적이다. 하지만 너무 일찍 그 디테일을 끌어오면 학습이 무겁게 가라앉는다. 우리는 instruction-accurate 시뮬레이션 [웹-자료20, §1.8]에서 시작한다. 명령어가 "완료된 시점"에서만 상태가 정확하면 충분하다. 한 명령어 안에서 사이클별로 어떤 신호가 켜지는지는 마지막 13장에서 cycle-accurate으로 리팩토링할 때 본격적으로 들춰볼 예정이다.

순서를 거꾸로 잡으면 어떻게 될까? 처음부터 컨트롤 신호와 T-state를 욱여넣는다고 해보자. 30줄짜리 코드는 단숨에 200줄로 부풀고, 독자는 "지금 내가 ADD 한 줄을 돌리려는데 왜 microstep 변수가 6개나 필요한가" 같은 의문 속에서 길을 잃는다. 가장 흔한 학습 사고다. 그래서 본 책은 큰 박자부터 잡고, 박자 사이를 채워 넣는 순서로 간다.

> 사이드바: nand2tetris·Ben Eater와의 위치 차이
>
> nand2tetris는 NAND 게이트 한 종류에서 출발해 트랜지스터급 디테일을 한 번에 다 노출한다. Ben Eater의 브레드보드 SAP-1은 와이어 한 가닥부터 직접 꽂는다 [§3.1, §4.3]. 둘 다 훌륭한 길이다. 다만 한국 학습자에게는 진입 비용이 높다. 본 책은 그 중간 — Kotlin 코드 30줄로 큰 박자부터 만져보고, 디테일은 챕터를 거듭하며 점진적으로 내려간다. 자기 손에 익은 언어로 시작한다는 점이 핵심이다.

## 자료형 한 줄 — 8비트를 어떻게 표현할까

위 코드에서 `Int`와 `0xFF` 마스크가 곳곳에 등장했다. 잠시 짚어두자. 이 선택은 의외로 책 전체에 영향을 미친다.

JVM 위에서 8비트 값을 다루는 방법은 크게 셋이다 [§5.1, 커뮤니티-패턴4].

1. **`Int` + 마스킹(`and 0xFF`)**: 가장 직관적이고 빠르다. JVM primitive 그대로 흐른다. 단점은 마스킹을 한 번 잊으면 부호 확장 사고가 난다. 흔히 ksim65 같은 6502 시뮬레이터가 채택하는 방식이다.
2. **`UByte`(Kotlin 1.5+)**: 0~255 범위를 자연스럽게 표현한다. inline class라 런타임 overhead는 사실상 없다. 다만 비트 시프트 연산자(`shr`, `shl`)가 좁은 타입에는 아직 들어 있지 않다. 그래서 `value.toInt().shr(4).toUByte()` 같은 변환을 거쳐야 한다. 답답하다.
3. **`Byte`(signed -128~127)**: 자연어와 어긋나서 디버깅이 끔찍해진다. 추천하지 않는다.

> "There is no significant overhead when using unsigned integer types on the JVM... Under the covers, all of the unsigned types in Kotlin are implemented as inline classes." [웹-자료10]

본 책의 정책은 이렇다. **앞 절반(2~6장)은 `Int + 마스킹`으로 간다.** 가독성도 좋고 코드를 따라가는 부담이 적다. 그러다 **4장 후반에서 같은 코드를 `UByte`로 다시 짜본다.** 같은 일을 두 번 한다는 점이 부담스럽게 들릴 수 있지만, 두 접근의 장단점을 자기 손으로 비교해보는 경험이 훨씬 값지다. UByte의 표현력과 타입 안전성, 그리고 부호 시프트의 함정 — 이 모두가 한 번에 손에 잡힌다.

지금 이 챕터에서는 깊이 들어가지 않는다. 잊지 말자. 이 정책 선언만 머리에 담아두자.

## 테스트로 잡아두자

손으로 한 번 돌려 본 코드라고 끝이 아니다. 한 줄짜리 `main`은 즉흥적인 실험으로 충분하지만, 우리가 정말 "이 CPU가 옳게 동작한다"라고 말하려면 테스트가 곁에 있어야 한다. 다음 챕터부터 SAP-1을 짤 텐데, 그때부터는 테스트 없이 가는 게 매우 위험하다. ALU 한 비트의 carry-out이 잘못 흐르면 30개 명령어가 동시에 깨진다. 그 디버깅이 얼마나 끔찍한지 한 번 경험해본 사람은 두 번 겪고 싶어 하지 않는다.

JUnit 5 기반으로 8개의 테스트를 적어보자. 작은 CPU지만 작은 CPU에도 잡아야 할 것이 의외로 많다.

```kotlin
class MiniCpuTest {

    @Test
    fun `HLT 한 명령어로 즉시 정지한다`() {
        // [0] HLT  → 누산기는 손도 안 댄다.
        val cpu = MiniCpu(intArrayOf(0xF0, 0x00, 0x00, 0x00))
        cpu.run()
        assertEquals(0, cpu.accumulator())
    }

    @Test
    fun `ADD 한 번으로 누산기에 값이 더해진다`() {
        // [0] ADD m[2]=7   [1] HLT   [2] 데이터 7
        val cpu = MiniCpu(intArrayOf(0x12, 0xF0, 0x07, 0x00))
        cpu.run()
        assertEquals(7, cpu.accumulator())
    }

    @Test
    fun `결과는 8비트로 마스크된다`() {
        // [0] ADD m[2]=0xFF   [1] HLT   [2] 0xFF
        // A는 0 + 0xFF = 0xFF로 남는다. 한 번의 덧셈으로 상한을 찍는다.
        val cpu = MiniCpu(intArrayOf(0x12, 0xF0, 0xFF, 0x00))
        cpu.run()
        assertEquals(0xFF, cpu.accumulator())
    }

    @Test
    fun `누산기는 자기 자신을 더해도 마스크된다`() {
        // 같은 주소를 두 번 짚으면 두 번 누적된다.
        // [0] ADD m[3]=0x80   [1] ADD m[3]=0x80   [2] HLT
        // A = 0x80 + 0x80 = 0x100 → 마스크 → 0x00
        val cpu = MiniCpu(intArrayOf(0x13, 0x13, 0xF0, 0x80))
        cpu.run()
        assertEquals(0x00, cpu.accumulator())
    }

    @Test
    fun `알 수 없는 opcode는 예외를 던진다`() {
        // opcode 5는 정의된 적이 없다.
        val cpu = MiniCpu(intArrayOf(0x50, 0xF0, 0x00, 0x00))
        assertFailsWith<IllegalStateException> {
            cpu.run()
        }
    }

    @Test
    fun `HLT 이후로는 한 줄도 더 실행되지 않는다`() {
        // [0] HLT  [1] ADD m[2]=0xFF — 절대 실행돼선 안 된다.
        val cpu = MiniCpu(intArrayOf(0xF0, 0x12, 0xFF, 0x00))
        cpu.run()
        assertEquals(0, cpu.accumulator())
    }

    @Test
    fun `다른 주소를 짚어도 정확히 그 값이 더해진다`() {
        // [0] ADD m[3]=0xF0   [1] HLT   [2] 미사용   [3] 0xF0
        val cpu = MiniCpu(intArrayOf(0x13, 0xF0, 0x00, 0xF0))
        cpu.run()
        assertEquals(0xF0, cpu.accumulator())
    }

    @Test
    fun `PC와 누산기는 종료 직전 상태로 멈춘다`() {
        // [0] ADD m[2]=0x07   [1] HLT   [2] 0x07
        // 실행이 끝났을 때 PC는 HLT 다음 자리(2)를 가리킨다 — fetch가 PC를 미리 증가시키니까.
        // 별도 게터를 외부에 공개하지 않으면 직접 확인할 수는 없지만,
        // 적어도 누산기는 7로 굳어 있어야 한다. run을 두 번 불러도 같은 값이어야 한다.
        val cpu = MiniCpu(intArrayOf(0x12, 0xF0, 0x07, 0x00))
        cpu.run()
        cpu.run()   // 이미 halted=true니까 루프에 진입조차 안 한다.
        assertEquals(7, cpu.accumulator())
    }
}
```

테스트 한 건당 평균 5~6줄이다. 그 자체로 우리가 막 짠 코드에 대한 명세 문서이기도 하다. "이 CPU는 이 입력을 받으면 이 결과를 낸다"를 검증 가능한 형태로 묶어둔 셈이다.

세 번째와 네 번째 테스트가 흥미롭다. "오버플로가 8비트로 마스크되는지"를 정직하게 확인하려면 ADD 두 번이 필요한데, 4바이트 메모리로는 ADD 둘 + HLT + 데이터 둘을 한꺼번에 담을 수 없다. 5바이트가 필요하다. 그래서 우회로를 썼다 — 같은 주소를 두 번 짚어 누산을 한 번에 두 번 일으키고, 데이터 칸을 절약한 셈이다. 짧은 코드에서 4바이트의 한계가 정직하게 드러난 순간이다. 다음 챕터부터 SAP-1의 16바이트 메모리가 왜 의미 있는지 — 그 정서적 동기를 바로 이 자리에서 얻는다.

> 사이드바: 8086·Z80·6502의 사이클은 어떻게 다른가
>
> 우리의 30줄짜리 미니 CPU는 instruction-accurate이라 명령어 하나당 한 박자다. 실제 8비트 CPU는 그렇지 않다.
> - **Intel 8080**: 명령어당 4~17 T-state. 가변 사이클.
> - **Zilog Z80**: 명령어당 4~23 T-state. M-cycle(memory cycle) 단위로 다시 묶임.
> - **MOS 6502**: 명령어당 2~7 사이클. 어드레싱 모드에 따라 변화.
> - **Intel 8086**: 명령어당 2~140 사이클 (DIV, MUL 같은 게 무겁다). prefetch queue가 따로 동작.
>
> 본 책의 SAP-1은 모든 명령어가 정확히 6 T-state로 고정된다. 그 단순함이 "Simple-As-Possible"의 정수다. 실제 CPU의 들쭉날쭉함은 11장에서 8080·Z80·6502·8086의 같은 Fibonacci 프로그램을 사이클까지 비교할 때 다시 본격적으로 다룬다.

## 첫 GitHub 커밋 — 작은 성공의 무게

이 챕터를 다 읽고 코드를 따라 친 사람은 자기 노트북에 다음 두 파일을 가진 셈이다.

- `chapter-02/src/main/kotlin/MiniCpu.kt` — 30줄 남짓의 CPU 본체와 `main` 함수.
- `chapter-02/src/test/kotlin/MiniCpuTest.kt` — 8개의 테스트.

손가락이 근질거리면 한 번 `./gradlew :chapter-02:run`을 두드려보자. `A = 42`가 떨어진다. 그리고 `./gradlew :chapter-02:test`로 8개 테스트를 한꺼번에 통과시켜보자. 작은 초록 줄이 8개 떨어지는 광경을 보면 알 수 없는 안도감이 든다. 그것이 우리가 챙긴 첫 번째 정서적 보상이다. 앞으로 13개 챕터에 걸쳐 이런 보상이 매번 따라붙을 것이다. 손으로 짠 코드가, 자기가 적은 테스트로, 자기 손바닥 위에서 돌아간다.

이 챕터의 진짜 산출물은 코드 30줄이 아니다. **"CPU가 동작한다"는 추상적 명제가 자기 코드의 어느 줄에 매핑되는지에 대한 손 감각** — 그것이 본문이고, 코드는 그 감각을 들고 갈 그릇이다. 그 감각이 손에 잡혔다면, 우리는 이미 SAP-1을 짤 자격을 갖춘 셈이다.

## 마무리

세 박자만 기억하자. fetch, decode, execute. CPU가 켜진 뒤로 꺼질 때까지 이 세 박자를 반복한다. 우리가 짠 `while` 루프 안의 세 줄이 정확히 그 박자다. 박스와 화살표로 그려졌던 데이터패스가 함수 호출과 메서드 인자로 옮겨왔다. 이 매핑을 잊지 말자. 다음 챕터에서 SAP-1의 16바이트 메모리, 5개 명령어, 6 T-state 컨트롤러가 등장할 때, 결국 같은 골격 위에 살이 붙는다는 것을 기억하면 헷갈리지 않는다.

8비트 표현 정책도 머리 한 구석에 남겨두자. 본문 절반은 `Int + 마스킹`으로 간다. 그러다 4장 후반에서 `UByte`로 옮겨갈 때 두 접근을 자기 손으로 비교해본다. 지금은 정책 선언만 받아둔다.

다음 장은 SAP-1의 청사진을 펼치는 자리다. 16바이트 우주 안에 다섯 명령어를 담는 작은 CPU의 모듈 지도를 그리고, 첫 두 모듈(클록과 PC)을 TDD로 짜본다. 우리의 30줄짜리 미니 CPU가 그 청사진의 어느 자리에 들어맞는지, 함께 살펴보자.

> **이번 챕터의 GitHub 커밋**
>
> ```
> chapter-02/
>   build.gradle.kts
>   src/main/kotlin/MiniCpu.kt    (CPU 본체 + main, ~40줄)
>   src/test/kotlin/MiniCpuTest.kt (8개 테스트)
>
> 실행:  ./gradlew :chapter-02:run        → A = 42
> 테스트: ./gradlew :chapter-02:test       → 8/8 passed
> ```
