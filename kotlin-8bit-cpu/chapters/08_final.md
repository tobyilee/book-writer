# 8장. 16바이트의 한계 — SAP-2는 왜 다시 설계되었는가

자, 7장까지 따라온 독자에게는 작지만 단단한 무언가가 손에 쥐어져 있을 것이다. 자기가 짠 SAP-1, 자기가 짠 어셈블러. 다섯 개 명령어, 16바이트 메모리, 한 줄짜리 어셈블리 프로그램이 자기 CPU 위에서 돌아간다. 2부 끝의 그 감정은 한동안 잊히지 않는다.

그런데 어느 날 — 아마 자기 SAP-1 위에서 조금 더 큰 프로그램을 짜보겠다고 마음먹은 날 — 한 가지 사실 앞에 멈춰 서게 된다. **이 SAP-1으로는 Fibonacci 수열을 출력하는 프로그램조차 짤 수 없다.** 

말이 안 되는 것 같다. 5 + 3 = 8을 출력하는 CPU가 Fibonacci를 못 한다고? 한번 직접 시도해보자. 손이 부딪히는 곳이 어디인지를 봐야 그다음 이야기가 와닿는다.

## SAP-1으로 Fibonacci를 짜보자 — 그리고 부딪혀보자

Fibonacci는 이렇게 시작한다. 0, 1, 1, 2, 3, 5, 8, 13, 21... 점화식은 `F(n) = F(n-1) + F(n-2)`다. SAP-1 어셈블리로 옮겨보자. 우선 5번째 항(=5)까지 출력하는 단순 버전부터.

```
; 주소 0~3에 코드, 4~7에 변수
        LDA  6       ; A ← M[6] = 0 (F(0))
        OUT          ; print 0
        LDA  7       ; A ← M[7] = 1 (F(1))
        OUT          ; print 1
        ; ... 그다음은?
```

여기서 막힌다. **반복**이 필요하다. "이 코드를 다섯 번 돌려라"를 어떻게 표현하지? 답은 분명하다. 위쪽으로 점프해 같은 코드를 다시 실행한다. 그런데 SAP-1에는 점프 명령이 없다. **`JMP`가 없다.** `LDA`, `ADD`, `SUB`, `OUT`, `HLT`. 다섯 개가 전부다.

그렇다면 코드를 일자로 늘어놓아 매 항을 명시적으로 계산하면? `F(n) = F(n-1) + F(n-2)`니까, 어쨌든 A 레지스터에 직전 값을 들고 있다가 그 앞 값을 더하면 된다. 시도해보자.

```
0: LDA  E      ; A ← M[E] = 0 (F0)
1: OUT
2: LDA  F      ; A ← M[F] = 1 (F1)
3: OUT
4: ADD  E      ; A ← 1 + 0 = 1 (F2)
5: OUT
6: ADD  F      ; A ← 1 + 1 = 2? 잠깐, M[F]는 여전히 1이지만
   ; F3 = F2 + F1 = 1 + 1 = 2. 그러려면 F1과 F2를 따로 보관해야 한다
   ; 그런데 A 외의 저장소가 거의 없다 ...
```

조금만 가도 머리가 복잡해진다. **저장소가 없다.** 누산기 A 하나뿐이다. B 레지스터는 ALU의 다른 입력 전용이라 사용자가 직접 못 쓴다. 그러니 직전 값과 직전직전 값을 메모리에 다시 저장해야 한다. 그러려면 `STA`(Store A)가 필요하다. **SAP-1에는 STA도 없다.** LDA만 있고 STA가 없는 것이다.

그러면 메모리에 값을 다시 쓸 수 없다. 결국 SAP-1의 메모리는 **읽기 전용 입력**처럼만 쓰인다. 우리가 짤 수 있는 건 "메모리에 미리 채워둔 상수들을 더하고 빼서 한 번 출력하고 끝나는 프로그램"뿐이다. 16바이트라는 작은 우주 안에서도, 정말로 짤 수 있는 프로그램은 작은 산수 하나다.

여기서 잠시 멈춰 한숨을 쉬어도 된다. **답답하다**. 그러나 이 답답함이 우리를 SAP-2로 데려간다.

## SAP-1이 못 하는 것들 — 한 번에 정리

SAP-1의 한계를 표로 정리해보자.

| 못 하는 것 | 부족한 것 | 일상 프로그램에서 의미 |
|------------|-----------|------------------------|
| 반복문 | JMP 명령어 | for/while 자체가 불가능 |
| 조건 분기 | JZ/JNZ 같은 조건 점프 | if 자체가 불가능 |
| 메모리에 결과 저장 | STA 명령어 | 계산 결과를 다음 단계로 못 넘김 |
| 함수 호출 | CALL/RET + 스택 | 코드 재사용 불가 |
| 변수 두 개 이상 | 사용자 가용 레지스터 1개(A뿐) | 임시 변수 두 개도 못 굴림 |
| 키보드 입력 | I/O 포트 | 외부와 대화 불가 |
| 곱하기/나누기 | MUL/DIV (혹은 시프트) | 손으로 반복 더하기로도 불가, 위 JMP 부재가 결정타 |
| 큰 프로그램 | 16바이트 메모리 | 16바이트는 너무 좁다 |

이 표를 보면 한 가지가 드러난다. **SAP-1이 못 하는 것은 단지 "수가 적다"의 문제가 아니다.** 명령어 다섯 개가 열 개로 늘어나는 식의 단순 확장으로는 메울 수 없다. 점프가 있어야 반복이 된다. 점프와 함께 조건 플래그를 보는 어떤 명령어가 있어야 if가 된다. STA가 있어야 변수가 산다. 그리고 64KB로 늘리지 않으면 함수도 의미 없다. **여러 결정이 한꺼번에 같이 변해야 의미 있는 프로그래밍 환경이 생긴다.**

이 점이 Malvino가 SAP-2를 "단순 확장"이 아니라 **근본 재설계**라고 부른 이유다. 5개 명령어를 39개로 늘리고 메모리를 4096배로 늘리는 게 단지 큰 칩이 아니라 다른 종류의 칩을 만든다.

## SAP-2의 변화 일람 — 한눈에 보기

SAP-2가 SAP-1에서 무엇을 바꾸는지를 표로 정리해보자.

| 항목 | SAP-1 | SAP-2 |
|------|-------|-------|
| 데이터 폭 | 8비트 | 8비트 (같음) |
| 어드레스 폭 | 4비트 | **16비트** |
| 메모리 | 16바이트 | **64KB** (4096배) |
| 명령어 수 | 5개 | **39개** |
| 사용자 가용 레지스터 | A 1개 | **A, B, C 3개** + SP, PC |
| 컨트롤러 | 조합 논리(hardwired) | **마이크로코드 ROM** (35 control signals × 10 T-states) |
| 산술 | ADD, SUB | ADD, SUB, INR, DCR, RAL, RAR (회전 포함) |
| 논리 | 없음 | **AND, OR, XOR, CMA** (NOT) |
| 분기 | 없음 | **JMP, JZ, JNZ, JM**(jump-if-minus) |
| 함수 | 없음 | **CALL, RET** + 스택 |
| I/O | OUT만 (출력 레지스터) | **IN, OUT** + 256개 포트 |
| 메모리 쓰기 | 불가 | **STA** + 메모리 직접 산술 일부 |
| ISA 호환성 | 독자 | **Intel 8080 subset** |

이 표를 한 번 들여다보면 8장의 본 내용은 거의 다 들어와 있다. 그러나 표가 말하는 것보다 더 중요한 게 한 가지 있다. **SAP-2의 ISA는 Intel 8080의 부분집합이다.** Malvino가 그렇게 설계했다. 이게 단순한 우연이 아니라는 점을 다음 절에서 짚자.

## "Intel 8080 subset"이라는 한 줄의 무게

Malvino의 원전(*Digital Computer Electronics*)이 SAP-2를 소개하는 한 문장에 이런 표현이 있다.

> "ISA is patterned after and upward compatible with the ISA of the Intel 8080/8085 microprocessor family."

이 한 줄을 가볍게 읽지 말자. **상위 호환**이다. SAP-2 어셈블리로 짠 프로그램은 실제 인텔 8080에서도 (메모리 배치만 맞으면) 그대로 돌아간다. 즉 우리가 SAP-2로 익히는 어셈블리는 **1974년에 알테어 8800을 움직이고, CP/M을 실어 나르고, 빌 게이츠와 폴 앨런이 BASIC을 짠 그 칩**의 어셈블리다. 8080은 단순한 교실 장난감이 아니다. 마이크로컴퓨터의 시작점이다.

이 점이 SAP-2의 학습적 가치를 결정짓는다. 우리가 SAP-2로 익히는 것은:

- 64KB 메모리를 다루는 16비트 주소 공간의 감각
- 범용 레지스터 3개(A·B·C)로 더 큰 프로그램을 짜는 방식
- 함수 호출과 스택의 의미
- 마이크로코드 ROM이라는 컨트롤러의 두 번째 진화

이 모든 것이 SAP-2의 단기 결과지만, 동시에 **8080이라는 실제 칩의 80%를 이미 손에 쥔 상태**라는 장기 결과를 가진다. 9장에서 SAP-2의 조건 분기·서브루틴·I/O를 직접 구현한 뒤, 11장에서 같은 Fibonacci를 8080·6502·Z80·8086 어셈블리로 비교한다. 그때 우리 어셈블리가 가장 닮은 것이 8080일 것이다. 우연이 아니라 처음부터 의도된 결과다.

> **사이드바: Malvino가 8080을 고른 까닭**
>
> Malvino의 *Digital Computer Electronics*는 1980년대 초판이고, SAP-2가 8080을 모방한 것도 그 시기다. 그때 8080은 어떤 위상이었나? 1974년 출시 → 알테어 8800(1975) → CP/M(1976) → 마이크로컴퓨터 산업의 표준. 모토로라 6800도 같은 해 나왔지만 가격(360달러 vs 360달러)과 보급률에서 8080이 한 발 앞섰다. Zilog Z80(1976)은 8080 상위 호환으로 발매됐다(즉 Z80도 8080 어셈블리를 받아준다는 뜻). MOS 6502(1975)는 25달러라는 충격적 가격으로 다른 길을 갔다 — Apple II, C64, NES로.
>
> 교과서 저자 입장에서 보면 8080 호환은 "학생이 익힌 어셈블리가 알테어, CP/M, Z80, 그리고 후의 8086까지 자연스럽게 이어진다"는 큰 그림을 그릴 수 있다. 그 선택의 그림자가 오늘날까지 이어진다. SAP를 익힌 사람은 8080을 30분 만에 읽는다.

## 마이크로코드 컨트롤러 — 컨트롤 방식의 진화

SAP-1과 SAP-2의 가장 깊은 차이는 명령어 수가 아니다. **컨트롤러가 어떻게 결정을 내리는가**의 차이다.

| 컨트롤러 방식 | 신호 결정 | 강점 | 약점 |
|---------------|----------|------|------|
| Hardwired (조합 논리) | opcode + T-state를 입력으로 받는 조합 회로 | 빠르다 (한 클록에 신호 결정) | 명령어가 늘어나면 회로가 폭발적으로 커진다. 변경 불가. |
| Microprogrammed (마이크로코드 ROM) | ROM에 옙코드별 마이크로명령어 시퀀스를 굽고 매 클록마다 인덱스 한 칸 진행 | 명령어 추가/변경이 ROM 굽기로 끝남. 39개도 거뜬 | 한 클록 더 걸린다(ROM 액세스). 메모리를 쓴다. |

SAP-1은 5개 명령어니까 조합 논리로 충분했다. 그러나 39개로 가면 조합 회로의 진리표가 사람이 손으로 관리할 크기를 넘는다. 그래서 마이크로코드로 넘어간다. **35개 control signal × 10 T-state짜리 큰 표 한 장으로 모든 명령어를 표현**한다.

Kotlin 입장에서 보면 이게 어떻게 보이나? 이미 6장에서 우리는 SAP-1의 마이크로코드를 작은 `Map`으로 구현했다. SAP-2에서는 그 표가 더 커진다. 명령어가 39개니까. 그러나 자료 구조 자체는 같은 결이다.

```kotlin
// SAP-2 마이크로코드 표 한 줄 예시 (개념적)
// 10장에서 본격 다룬다
typealias MicroStep = Set<ControlSignal>
typealias MicroProgram = List<MicroStep>

val sap2Microcode: Map<Opcode, MicroProgram> = mapOf(
    Opcode.LDA to listOf(/* T1~T10 단계별 신호 */),
    Opcode.STA to listOf(/* ... */),
    Opcode.JMP to listOf(/* ... */),
    // ... 36개 더
)
```

표가 커진다는 점이 코드의 본질을 바꾸지는 않는다. **이게 마이크로코드가 가진 우아함이다.** 명령어를 늘려도 코드 구조는 거의 그대로다. SAP-1을 마이크로코드로 짜둔 6장의 결정이 8장에서 보답한다.

## SAP-2의 명세 — Austin Morlan의 한숨

이제 솔직한 이야기를 하나 해야 한다. **SAP-2의 명세는 완벽하지 않다.** 

Austin Morlan은 SAP-2를 FPGA로 직접 구현한 뒤 자기 블로그에 후기를 올렸다. 그 후기에 이런 한 줄이 있다.

> "If you find the architecture of this version to be highly awkward and strange, we are in agreement."

번역해보면 "이 버전의 아키텍처가 매우 어색하고 이상하게 느껴진다면, 그 점에 우리가 동의한다는 뜻이다"쯤 된다. SAP-1을 만든 사람이 SAP-2도 똑같이 깔끔할 거라 기대하고 들어왔다가 한 번씩 한숨을 내쉬게 된다.

구체적으로 무엇이 어색한가? 가장 자주 지적되는 한 가지가 **CALL/RET의 명세 모호함**이다. SAP-2 명세대로 따라가면, **함수가 다른 함수를 호출하면 return address가 덮어쓰여 깨진다**. 즉 재귀나 중첩 호출이 깨지는 명세 결함이 있다. 이 문제는 SAP-3에서 비로소 해결된다.

다른 모호함도 있다.

- 일부 명령어의 인코딩이 8080과 정확히 일치하지 않는데, 어디서 다른지가 본문에 명시되지 않은 곳이 있다
- 일부 T-state 시퀀스의 길이가 명령어별로 다른데, 컨트롤러 ROM의 정확한 구조가 모호하다
- I/O 포트의 정확한 어드레싱 방식이 8080의 그것과 살짝 어긋난다

그러면 우리는 어떻게 해야 하나? 답은 한 가지다. **이 책의 SAP-2 구현은 명세의 모호한 부분을 일관성 있게 해석한 한 버전이다.** 다른 책이나 강좌가 다른 해석을 쓸 수 있다. 그게 자연스럽다. Malvino의 원전이 모호한 부분을 우리가 어떻게 해석했는지를 메타 코멘트로 남겨두면 학습자가 자기 코드와 다른 자료를 비교할 때 방향을 잡기 쉽다.

> **우리 책의 SAP-2 해석 정책 (요약)**
>
> - **CALL/RET 명세 결함:** 우리 책은 처음부터 스택을 SP 기반으로 명시 구현한다(즉 SP를 사용한 push/pop으로 return address 저장). 이 방식이 SAP-3와 8080의 공식 동작과 일치한다. SAP-2 원본의 모호함을 한 번에 정리한다.
> - **I/O 포트:** 8080의 IN/OUT 명세(`IN port` / `OUT port`, port는 8비트)를 따른다. SAP-2 원본은 포트 개수가 모호하지만 우리는 256개로 고정한다.
> - **명령어 인코딩:** 가능한 한 8080과 일치시킨다. 다른 곳은 명시적 표로 책에 노출한다(부록 D).
> - **T-state 시퀀스:** 우리 책의 마이크로코드 표는 모든 명령어가 최대 10 T-state를 점유한다. 짧은 명령어는 NOP T-state로 채운다 (SAP-1의 6 T-state 패턴의 확장).
>
> 이 정책은 일관성을 위한 결정이지 "원본이 틀렸다"는 주장이 아니다.

이런 메타 코멘트가 어떤 느낌인지 처음 접하면 살짝 찜찜할 수도 있다. "교과서가 모호한 부분을 자기 마음대로 해석한다고?" 한 번 잠깐 생각해보자. 사실 모든 교과서가 그렇다. **컴퓨터 구조 같은 분야는 진짜로 완벽히 표준화된 단일 명세가 드물다.** 자기가 짠 해석을 명시적으로 적어두는 편이 학습자에게 훨씬 친절하다. 다른 자료와 비교할 때 "왜 다른지"를 알 수 있다.

## SAP-2 핵심 모듈 — Kotlin scaffold

이제 8장의 결과물을 짤 차례다. 8장에서는 **SAP-2의 뼈대만** 잡는다. 본격 구현은 9장(분기·서브루틴·I/O)과 10장(마이크로코드·디버거)에서 나눠진다. 8장의 산물은 두 가지다.

1. **`Sap2Core.kt`** — SAP-2 CPU의 최상위 클래스. 모듈들을 들고 있는 컨테이너. 메서드는 거의 비어 있다(scaffold).
2. **`RegisterFile.kt`** — A·B·C 세 레지스터를 묶어 들고 다닐 클래스.

먼저 RegisterFile부터. 3장에서 짠 `Register` 클래스를 그대로 재활용한다.

```kotlin
// chapter-08/sap2/RegisterFile.kt
class RegisterFile {
    val a = Register(name = "A", width = 8)
    val b = Register(name = "B", width = 8)
    val c = Register(name = "C", width = 8)

    fun reset() {
        a.load(0)
        b.load(0)
        c.load(0)
    }

    override fun toString(): String = "$a $b $c"
}
```

작다. 이 자체로는 별 일을 안 한다. 그러나 코드가 작은 게 핵심이다. **8비트 범용 레지스터 셋은 결국 그저 레지스터 세 개의 묶음**이다. SAP-2의 거대해 보이는 39개 명령어들도 결국 이 세 레지스터를 이러저러하게 굴리는 일이다. 마음의 짐을 좀 덜자.

테스트도 짧다.

```kotlin
// chapter-08/sap2/RegisterFileTest.kt
class RegisterFileTest : FunSpec({

    test("초기화 후 모든 레지스터는 0이다") {
        val rf = RegisterFile()
        rf.a.value shouldBe 0
        rf.b.value shouldBe 0
        rf.c.value shouldBe 0
    }

    test("각 레지스터는 독립적으로 동작한다") {
        val rf = RegisterFile()
        rf.a.load(0x42)
        rf.b.load(0x99)
        rf.a.value shouldBe 0x42
        rf.b.value shouldBe 0x99
        rf.c.value shouldBe 0
    }

    test("reset()은 모든 레지스터를 0으로 되돌린다") {
        val rf = RegisterFile()
        rf.a.load(0x42)
        rf.b.load(0x99)
        rf.c.load(0xFF)
        rf.reset()
        rf.a.value shouldBe 0
        rf.b.value shouldBe 0
        rf.c.value shouldBe 0
    }
})
```

이제 SAP-2 코어. 64KB 메모리, 16비트 PC, 레지스터 파일, ALU, 마이크로코드 ROM(자리만 잡고), 출력 디바이스. 9장과 10장에서 본격 구현하기 위해 인터페이스만 잡아둔다.

```kotlin
// chapter-08/sap2/Sap2Core.kt
class Sap2Core(
    private val memorySize: Int = 65536    // 64KB
) {
    val clock = Clock()
    val pc = ProgramCounter(width = 16)
    val registers = RegisterFile()
    val ram = Ram(memorySize, addrWidth = 16, dataWidth = 8)
    val alu = Alu()
    val ir = Register(name = "IR", width = 8)
    val sp = Register(name = "SP", width = 16)     // 스택 포인터 (9장)
    val output = OutputDevice()                     // 출력 (9장에 IN/OUT으로 일반화)

    // 마이크로코드 컨트롤러는 10장에서 본격 구현
    private val microcode: Sap2Microcode = Sap2Microcode.placeholder()

    fun reset() {
        clock.reset()
        pc.reset()
        registers.reset()
        sp.load(0xFFFF)        // 스택은 메모리 최상단에서 아래로 자란다
        ir.load(0)
    }

    fun loadProgram(bytes: ByteArray, startAt: Int = 0) {
        for ((i, b) in bytes.withIndex()) {
            ram.write(startAt + i, b.toInt() and 0xFF)
        }
    }

    fun step() {
        // 한 명령어 실행. 9장에서 본격 구현.
        throw NotImplementedError("9장에서 구현한다")
    }

    fun run() {
        while (!clock.halted) {
            step()
        }
    }
}

// scaffold용 placeholder
class Sap2Microcode private constructor() {
    companion object {
        fun placeholder() = Sap2Microcode()
    }
}

class OutputDevice {
    private val log = mutableListOf<Int>()
    fun write(value: Int) { log.add(value and 0xFF) }
    fun history(): List<Int> = log.toList()
}
```

`step()`에 `NotImplementedError`를 던지는 게 거슬릴 수 있다. **일부러 그렇게 둔다.** 9장에서 실제로 채울 자리를 명시적으로 비워두는 것이다. 이렇게 해두면 8장 안에서 SAP-2 코어가 만들어지긴 했지만 "아직 살아 있지는 않은" 상태가 명확해진다. 학습자가 자기 코드 어디까지 짰는지를 손으로 짚을 수 있다. 보이지 않는 상태로 두면 나중에 9장에서 "어, 이건 어디서 채워야 하지?" 싶은 일이 생긴다. 그게 진짜로 찜찜하다.

핵심 모듈 다섯 가지가 비어 있더라도 한 자리씩 잡혀 있다는 게 보이는가? Clock, PC(16비트로 확장), RegisterFile, Ram(64KB로 확장), ALU(5장 결과 그대로 재활용). **SAP-1에서 쓴 모듈을 거의 그대로 가져왔다.** 클래스의 width 인자만 바꿔주면 4비트 PC가 16비트 PC가 되고, 16바이트 RAM이 64KB RAM이 된다. 3장에서 width를 인자로 받아둔 것이 8장에서 보답하는 순간이다. 3장의 작은 결정이 8장에서 큰 보답으로 돌아온 셈이다.

### Ram 클래스의 확장

3장의 Ram 클래스도 비트 폭을 인자로 받도록 재설계해두자. 4비트 주소를 16비트로 확장하는 데 한 줄 변경이면 충분하다.

```kotlin
// chapter-03에서 가져와 확장
class Ram(
    val size: Int,
    addrWidth: Int = 4,
    dataWidth: Int = 8
) {
    private val addrMask = (1 shl addrWidth) - 1
    private val dataMask = (1 shl dataWidth) - 1
    private val cells = IntArray(size)

    fun read(addr: Int): Int = cells[addr and addrMask] and dataMask
    fun write(addr: Int, value: Int) {
        cells[addr and addrMask] = value and dataMask
    }
}
```

`Ram(16)` → `Ram(65536, addrWidth = 16)`. 변경 한 줄. **이게 width를 인자로 받아두는 패턴의 보상이다.** 같은 코드가 SAP-1과 SAP-2를 모두 책임진다.

테스트도 한 줄 시나리오로 충분하다.

```kotlin
test("64KB RAM은 0xFFFF 주소까지 동작한다") {
    val ram = Ram(65536, addrWidth = 16, dataWidth = 8)
    ram.write(0xFFFF, 0xAB)
    ram.read(0xFFFF) shouldBe 0xAB
    ram.read(0) shouldBe 0     // 다른 주소는 영향 없음
}

test("16비트 주소를 초과하는 값을 쓰면 마스킹된다") {
    val ram = Ram(65536, addrWidth = 16, dataWidth = 8)
    ram.write(0x1FFFF, 0x42)    // 17비트 주소
    ram.read(0xFFFF) shouldBe 0x42    // 하위 16비트로 마스킹
}
```

이 두 줄짜리 테스트가 SAP-1에서 SAP-2로 가는 RAM의 확장을 검증한다. 우리가 이전에 깐 안전망이 그대로 작동한다.

## "SAP-1 → SAP-2"가 가르치는 교훈

여기서 잠시 멈춰서 큰 그림을 한 번 보자. SAP-1에서 SAP-2로 가는 발걸음이 우리에게 무엇을 가르치고 있는가?

**첫째, ISA 설계는 한 결정의 묶음이다.** 명령어 하나를 추가할 때 그 뒤에 따라오는 결정의 사슬을 봐야 한다. JMP를 추가한다고? 그러면 주소 폭이 충분한가? PC가 거기까지 갈 수 있나? 분기 명령어를 처리하는 마이크로코드는? 어셈블러는 라벨을 어떻게 해결할까? 어셈블러는 forward reference를 어떻게? 한 명령어가 다른 모든 결정을 끌고 들어온다.

**둘째, "확장"과 "재설계"의 경계가 보인다.** SAP-1에서 명령어 5개를 8개로 늘리는 건 확장이다. 그러나 16바이트를 64KB로 늘리는 건 재설계다. 둘 사이의 경계가 한 번 흐릿한 곳을 지나는데, 그 흐릿한 자리에서 좋은 설계자와 평범한 설계자가 갈린다. Malvino는 SAP-2에서 그 경계를 의도적으로 큰 폭으로 넘어버렸다. "한 발만 떼는 척 두 발을 다 옮긴" 셈이다.

**셋째, ISA는 추상화의 한 켜를 짓는다.** SAP-2의 어셈블리로 짠 프로그램은 8080 위에서도, Z80 위에서도(Z80은 8080 상위 호환) 비슷하게 돈다. 즉 ISA는 **소프트웨어 자산이 살아남는 시간 단위**를 결정한다. 1974년에 짠 8080 BASIC이 1976년 Z80 위에서, 1985년 V20 위에서, 어쩌면 2026년 우리 SAP-2 Kotlin 시뮬레이터 위에서도 비슷하게 돈다. 이게 ISA라는 단어가 무겁게 들리는 까닭이다.

**넷째, 하드웨어와 소프트웨어의 경계가 ISA에서 만난다.** 마이크로코드를 ROM에 굽는 결정은 하드웨어 설계자의 일이다. 그러나 ISA가 무엇을 약속하느냐는 소프트웨어 작성자에게 직접적인 영향을 준다. 그 약속을 어디까지 두느냐, 어떤 모호함을 남기느냐가 1980년대의 격렬한 논쟁(RISC vs CISC)으로 번진다. 12장에서 그 논쟁을 본격적으로 들여다본다.

> **GitHub 산출물**
>
> 이 챕터에서 추가될 GitHub 레포의 디렉터리는 다음과 같다.
>
> ```
> chapter-08/
>   build.gradle.kts
>   src/main/kotlin/sap2/
>     Sap2Core.kt          ← scaffold (step()은 9장에서 채움)
>     RegisterFile.kt
>     OutputDevice.kt
>     Sap2Microcode.kt     ← placeholder (10장에서 채움)
>   src/main/kotlin/common/
>     Ram.kt               ← 3장 Ram 확장 (addrWidth/dataWidth 인자)
>     Register.kt          ← 3장과 동일
>   src/test/kotlin/sap2/
>     RegisterFileTest.kt  (3개)
>     RamExtensionTest.kt  (2개)
>     Sap2CoreScaffoldTest.kt  (구조 점검 4개)
> ```
>
> 실행:
> ```
> ./gradlew :chapter-08:test
> ```
>
> 산물 개수가 적게 느껴질 수 있지만, 이 챕터의 의미는 **8장의 코드 양**이 아니라 **3장부터 5장까지 짜둔 모듈을 64KB 환경으로 확장하는 데 변경이 거의 필요하지 않다**는 검증이다. 작은 테스트가 큰 약속을 보장한다.

## 마무리 — 16바이트의 우주를 떠난다

다시 정리하자.

1. **SAP-1로는 Fibonacci 한 줄 못 짠다**는 답답함을 직접 부딪혔다 — JMP 없음, STA 없음, A 레지스터 하나뿐
2. **SAP-1의 한계 표 한 장**으로 못 하는 일들의 결을 봤다 — "수가 적은" 문제가 아니라 "여러 결정이 같이 변해야 하는" 문제
3. **SAP-2의 변화 일람**을 받아들였다 — 16바이트 → 64KB, 4비트 → 16비트 주소, 5개 → 39개 명령어, 1개 → 3개 레지스터
4. **"Intel 8080 subset"의 무게**를 짚었다 — 우리 어셈블리는 1974년 알테어 8800의 어셈블리와 거의 같다
5. **마이크로코드 컨트롤러로의 전환**을 이해했다 — hardwired는 5개까지, 39개부터는 ROM
6. **Austin Morlan이 한숨 쉰 SAP-2 명세의 모호함**을 인정하고, 우리 책의 해석 정책을 명시했다
7. **SAP-2 scaffold를 짰다** — RegisterFile, Sap2Core(step은 9장), Ram 확장. 핵심은 코드 양이 아니라 SAP-1 모듈을 거의 그대로 재활용한다는 점

여기까지 따라온 독자는 8장이 코드가 적다고 살짝 의아할지도 모르겠다. 코드 양보다 더 중요한 산물은 **"우리가 갈 길의 지도"**다. 다음 챕터에서 펼쳐낼 39개 명령어, 분기, 함수, I/O를 끌어안을 준비를 한 셈이다.

9장에서는 그 39개 중 가장 정서적으로 큰 의미를 가지는 한 묶음을 짠다. **조건 분기, 서브루틴, I/O.** 한마디로 "프로그램다운 프로그램"을 짤 수 있는 첫 순간이다. 자기 SAP-2 위에서 Fibonacci가 돌아가고, 함수 호출이 일어나고, 가상 키보드로 입력을 받고, 가상 콘솔로 출력하는 작은 우주가 열린다. 16바이트 우주를 떠나 64KB 우주에서 살아남는 첫걸음이다.

잠깐 쉬어가자. 차 한 잔 들고 자기 SAP-1 코드를 마지막으로 한 번 들여다보자. 작지만 또렷한 첫 산물이다. 다음 챕터에서, 그 코드의 어떤 결이 SAP-2로 자연스럽게 이어지고 어떤 결이 새로 짜야 하는지를 함께 손에 쥐어보자. 9장에서 만나자.
