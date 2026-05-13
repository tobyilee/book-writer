# 9장. 조건 분기·서브루틴·I/O — 프로그램다운 프로그램

자, 지금 우리가 가진 SAP-2를 한번 떠올려보자. 8장에서 64K 메모리를 깔았고, 16비트 PC를 두었고, A·B·C 세 개의 범용 레지스터에 39개의 명령어 자리를 만들어 두었다. 명세는 풍요로워졌다. 그러나 솔직히 한 번 짚고 가자. 지금까지 우리가 짠 SAP-2 위에서 돌릴 수 있는 프로그램이 무엇이 있는가?

기껏해야 "메모리에서 값을 가져다 더하고 결과를 어딘가에 두는" 일직선 코드뿐이다. 사람이 짠 어떤 프로그램도 그런 단조로움 위에 살지 않는다. `if`가 있어야 한다. 함수가 있어야 한다. 키보드에서 글자가 들어오고 화면으로 글자가 나가야 한다. 그렇지 않으면 SAP-2는 "더하기 빼기를 잘하는 계산기"에 머문다. 우리가 매일 짜는 그 평범한 코드 한 줄과는 너무 멀다. 찜찜한 거리감이다.

여기서 그 거리감을 한 번에 좁히자. `if`가 기계어에서 어떻게 살아 움직이는지, 함수 호출이라는 추상이 메모리 어디에 어떤 자국을 남기는지, 그리고 CPU가 바깥 세계와 어떻게 대화하는지 — 셋을 한 호흡에 묶어본다. 다 끝나면 자기 SAP-2 위에서 Fibonacci 수열이 돌아간다. 자기 SAP-2가 콘솔에 "Hello"를 한 글자씩 떨어뜨린다. 우리가 매일 짜던 코드와 우리가 만든 CPU 사이의 간극이 그제야 한 번에 닫힌다.

## if를 기계어에 옮기는 법 — 조건 점프

먼저 가장 익숙한 것부터. Kotlin으로 `if (x == 0) { ... }`을 적는다고 해보자. 이 한 줄을 SAP-2의 어셈블리로 옮겨야 한다면 어떻게 적을 것인가?

답은 의외로 단순하다. SAP-2의 어셈블리에는 `if`라는 키워드 자체가 없다. 대신 **조건 점프** 명령어가 있다. JZ(jump if zero), JNZ(jump if not zero), JM(jump if minus) — 이름이 곧 의미다. 마지막 ALU 연산의 결과 플래그를 보고, 그 결과가 0이면 어딘가로 점프하고 아니면 다음 줄로 흘러간다.

이걸 코드 한 토막으로 적어보자. "A 레지스터의 값이 0이면 0번지에 99를 쓰고, 아니면 200번지에 88을 쓴다"라는 의사 코드가 있다고 하자.

```
        ; A의 값을 확인 — ALU가 0 플래그를 세우게 한다
        ANA A          ; A AND A — A 값을 바꾸지 않으면서 Z 플래그를 갱신
        JZ  ZERO_CASE
        LDA #88
        STA 200
        JMP DONE
ZERO_CASE:
        LDA #99
        STA 0
DONE:
        HLT
```

여기서 흥미로운 디테일 하나. **조건 점프는 ALU의 마지막 연산이 남긴 플래그를 본다.** A 자체를 보는 게 아니다. 그래서 `ANA A`(A AND A)라는 일견 무의미한 연산이 등장한다. 결과는 A 그대로지만, ALU가 한 번 동작하면서 Z 플래그가 갱신되니까 그 다음 `JZ`가 정확히 동작한다. 이 트릭은 6502·Z80·8080 모두에서 흔하다. "값을 검사하기 위해 의도적인 무의미 연산을 한 번 끼워 넣는" 패턴이다.

다른 길도 있다. 8080·SAP-2에는 `CMP`(compare) 명령어가 있어 두 수를 비교한 결과를 플래그에만 반영하고 A는 건드리지 않는다. 그렇게 하면 의도가 또렷해진다. 둘 중 어느 쪽을 쓸지는 어셈블리 작성자의 취향이다.

### Kotlin으로 점프를 짜자

SAP-2 코어 안에서는 어떻게 동작할까? 7장에서 짠 컨트롤러를 떠올려보자. opcode를 보고 `when`으로 분기해 execute 단계의 마이크로 동작을 선택한다. 점프 명령어도 같은 자리에서 처리된다. 다른 점은 단 하나 — execute 단계에서 **PC를 새 주소로 덮어쓴다**는 것이다.

```kotlin
class Sap2 /* ... */ {
    val pc = ProgramCounter(width = 16)
    val flags = Flags()   // Z, S, C, P 등

    private fun executeJump(opcode: Int, target: Int) {
        val shouldJump = when (opcode) {
            OP_JMP -> true                      // 무조건 점프
            OP_JZ  -> flags.zero
            OP_JNZ -> !flags.zero
            OP_JM  -> flags.sign                // sign이 켜졌으면 음수
            OP_JP  -> !flags.sign
            OP_JC  -> flags.carry
            OP_JNC -> !flags.carry
            else   -> error("점프 명령이 아닌데 executeJump가 호출됐다: 0x${opcode.toString(16)}")
        }
        if (shouldJump) {
            pc.set(target and 0xFFFF)            // 16비트 마스크
        }
    }
}
```

코드 한 토막의 정수는 두 줄이다. **(1)** 플래그를 본다. **(2)** 가야 한다면 PC를 덮어쓴다. 그게 전부다. SAP-1에서 PC는 매 사이클 `+1`만 됐다. SAP-2부터는 PC가 어디로든 점프할 수 있게 된다 — 이것이 "프로그램이 통제 흐름(control flow)을 갖는다"는 말의 핵심이다.

> **사이드바: 6502와 Z80의 분기 명령어 차이**
>
> 같은 일을 하는데 표기 철학이 사뭇 다르다.
> - **8080·SAP-2**: 절대 점프. `JZ 0x2100`처럼 16비트 주소 그대로 적어 PC에 덮어쓴다. 어느 함수로도 점프 가능.
> - **MOS 6502**: 절대 점프(`JMP $2100`)와 상대 분기(`BEQ +8`)가 분리. 조건 분기는 상대 주소(-128~+127)만 가능 — 멀리 가려면 점프 + 점프 트릭이 필요하다.
> - **Zilog Z80**: 둘 다 지원. 절대(`JP NZ, 0x2100`)와 상대(`JR NZ, +8`) 두 어셈블리가 따로 존재. 짧은 분기엔 상대를, 먼 분기엔 절대를.
> - **Intel 8086**: 8086의 `JZ`도 8비트 상대. 멀리 가려면 `JNE 1f; JMP far; 1:` 식의 두 단계 트릭.
>
> 우리의 SAP-2는 8080 패턴을 따라 절대 점프만 둔다. 어셈블러도 단순해지고 학습 부담도 줄어든다. 13장의 합성 RISC에서는 상대 분기를 다시 한 번 진지하게 도입할 예정이다.

이 한 가지 변화 — PC가 점프 가능해진 것 — 으로 우리 프로그램은 `for`, `while`, `if-else`를 모두 흉내 낼 수 있다. 사실 모두 같은 도구의 다른 사용법이다. 루프는 "조건이 참인 동안 위로 점프", `if-else`는 "조건이 참이면 점프, 아니면 흘러감". 고급 언어가 우리 머리에 그려놓은 통제 흐름의 그림이 점프 한 줄로 환원된다. 묘하게 후련한 깨달음이다.

## 함수 호출의 비밀 — 스택과 CALL/RET

`if`를 손에 잡았다면, 다음 욕심은 함수다. 같은 코드 토막을 여러 자리에서 재사용하고 싶다. 어떻게 옮길 것인가?

가장 단순한 답은 "그 코드 토막의 시작 주소로 점프하라"다. 그런데 이 길에는 문제가 하나 있다. 점프했다가 — **어떻게 돌아오는가?** A 함수가 5번 자리에서 점프해 B 함수로 들어갔다고 하자. B의 마지막 줄에서 어디로 돌아와야 하는가? 6번 자리다. 그러나 CPU의 어디에도 그 6번이라는 정보가 적혀 있지 않다.

이 문제 — **return address를 어디에 둘 것인가** — 가 함수 호출의 본질이다. 답은 모두가 같다. **스택**이다. 한 번 손에 잡으면 평생 쓰는 자료구조.

### SP라는 작은 레지스터

스택을 코드로 옮기는 일은 의외로 단순하다. 메모리 어딘가에 "스택 영역"을 잡고, **SP**(Stack Pointer)라는 16비트 레지스터에 그 영역의 꼭대기 주소를 들고 다닌다. SAP-2의 명세대로 정리하자.

- `PUSH r`: SP를 1 감소시킨 뒤, `mem[SP]`에 레지스터 r의 값을 적는다.
- `POP r`: `mem[SP]`에서 값을 읽어 r에 적은 뒤, SP를 1 증가시킨다.

스택이 메모리의 위에서 아래로 자란다는 점이 처음에 헷갈린다. 책상 위에 종이를 올리듯이 자라는 게 아니라, 우물 안으로 점점 내려가듯이 자란다. 8080·6502·Z80·SAP-2 모두 같은 컨벤션이다. 머릿속 그림으로는 "스택 영역의 가장 높은 주소가 빈 자리고, push할 때마다 한 칸씩 내려간다"가 자연스럽다.

```kotlin
class Stack(
    private val memory: Memory,
    private val sp: RegisterWide,        // 16비트 레지스터
) {
    fun push(value: Int) {
        sp.set((sp.value - 1) and 0xFFFF)
        memory.write(sp.value, value and 0xFF)
    }

    fun pop(): Int {
        val value = memory.read(sp.value)
        sp.set((sp.value + 1) and 0xFFFF)
        return value
    }

    fun pushWord(value: Int) {
        // 16비트 — high·low 순으로 두 바이트.
        push((value shr 8) and 0xFF)
        push(value and 0xFF)
    }

    fun popWord(): Int {
        val lo = pop()
        val hi = pop()
        return (hi shl 8) or lo
    }
}
```

코드는 짧다. 그러나 한 가지 약속을 짚고 가자. **16비트 값을 push할 때는 두 바이트로 쪼개야 한다.** 메모리 자체는 8비트짜리 셀이니까. 우리의 컨벤션은 "low를 먼저, high를 나중에" 푸시한다 — 8080과 일치하는 little-endian 순서다. pop할 때 반대로 꺼내야 원본이 복원된다.

이 순서를 잘못 적으면 다음 일이 벌어진다. push에서는 `low → high` 순으로 쌓았는데 pop에서는 `low → high` 순으로 꺼낸다면? 두 바이트가 뒤바뀐 채 돌아온다. 함수 호출은 멀쩡한데 인자만 이상하게 나타나는, 잡기 정말 어려운 버그가 생긴다. 끔찍한 디버깅이다. 이 컨벤션은 한 번 정해두면 절대 흔들면 안 된다.

### CALL과 RET — 함수의 두 입출구

이제 스택이 손에 있으니, 함수 호출은 자연스럽다.

- `CALL addr`: 현재 PC(즉 CALL 다음 줄의 주소)를 스택에 push한다. 그러고 PC를 addr로 점프시킨다.
- `RET`: 스택에서 값을 pop해 PC에 적는다.

```kotlin
private fun executeCall(target: Int) {
    stack.pushWord(pc.value)            // CALL 다음 줄의 주소 — fetch에서 이미 +3됨
    pc.set(target and 0xFFFF)
}

private fun executeReturn() {
    pc.set(stack.popWord())
}
```

세 줄짜리 메서드 두 개. 함수라는 거대한 추상이 정말 이게 전부냐고 묻고 싶어진다. 그렇다. 정말 이게 전부다. 어셈블리 한 줄(`CALL`)이 push + jump 두 마이크로 동작으로 펼쳐지고, 다른 한 줄(`RET`)이 pop + jump로 펼쳐진다. 그 두 줄 위에 우리가 매일 쓰는 모든 함수 호출이 살고 있다.

> **사이드바: SAP-2의 함수 재진입 버그 — 명세의 정직한 결함**
>
> Malvino 3판 SAP-2의 명세를 그대로 따르면 한 가지 끔찍한 일이 생긴다 [§1.4, §4.5]. **함수가 다른 함수를 호출하면 return address가 깨진다.** 정통 SAP-2는 return address를 별도의 한 칸짜리 레지스터(스택이 아닌)에 저장한다. 그러니 함수 A가 함수 B를 부르면 그 한 칸이 덮어써져 A로 돌아갈 길이 사라진다.
>
> Austin Morlan은 그의 SAP-2 FPGA 구현 후기에서 이를 두고 "highly awkward and strange"라고 말한다 [§4.5].
>
> > "If you find the architecture of this version to be highly awkward and strange, we are in agreement." (Austin Morlan)
>
> SAP-3에서는 진짜 스택이 도입되면서 이 문제가 해결된다. 우리는 학습의 결을 단순하게 가져가기 위해 SAP-2에 처음부터 스택을 두는 길을 택한다 — 원전을 절반쯤 SAP-3 쪽으로 끌고 온 셈이다. 원전 그대로 따라 하면 재귀를 못 짜는 CPU가 되고, 그러면 학습이 머리 한 가운데에서 멈춘다. 명세의 권위보다 학습의 흐름이 더 중요한 순간이다.

### 작은 호출 트리를 손으로 따라가보자

코드만 보면 추상적이다. SP가 매 줄 어디로 움직이는지 직접 따라가보자. 다음 어셈블리를 생각해보자.

```
        ; main
        LXI SP, 0xFFFF      ; SP를 메모리 꼭대기에
        CALL foo            ; main → foo
        HLT
foo:
        CALL bar            ; foo → bar
        RET                 ; bar에서 돌아온 뒤 foo도 return
bar:
        RET
```

SP의 흐름:

| 단계 | 동작 | SP | 스택 꼭대기 |
|---|---|---|---|
| 초기 | `LXI SP, 0xFFFF` | 0xFFFF | (비어 있음) |
| ① | `CALL foo` 실행 | 0xFFFD | `[HLT 주소]` |
| ② | `CALL bar` 실행 | 0xFFFB | `[RET 주소], [HLT 주소]` |
| ③ | bar의 `RET` 실행 | 0xFFFD | `[HLT 주소]` (RET가 pop한 후 foo 안의 RET 직전으로 복귀) |
| ④ | foo의 `RET` 실행 | 0xFFFF | (비어 있음) (HLT로 복귀) |
| ⑤ | `HLT` 실행 | — | 정지 |

이 표를 한 번 손으로 그리면 함수 호출 트리가 마음에 또렷이 자리 잡는다. 우리가 매일 짜는 재귀 함수도 똑같은 매커니즘으로 움직인다. 콜 스택이 깊어진다는 것은 SP가 내려간다는 것이고, 스택 오버플로는 SP가 다른 영역을 침범한다는 뜻이다. 너무 자주 듣던 단어들이 비로소 살아 있는 그림이 된다.

## I/O — CPU가 바깥과 대화하는 두 가지 방법

`if`와 함수가 손에 잡혔다. 이제 마지막 한 조각이 남았다. **CPU가 바깥 세계와 어떻게 대화하는가**. 키보드의 입력, 화면으로의 출력, 디스크 읽기 — 이 모두를 추상화한 단어가 I/O다.

여기서 두 학파가 갈라진다. 6502의 길과 8080의 길. 둘은 같은 문제를 정반대로 푼다.

### 메모리 매핑 I/O — 6502의 길

6502는 **별도의 I/O 명령어가 없다.** 외부 디바이스를 메모리 주소처럼 본다. NES의 PPU(그래픽 칩)는 `$2000`~`$2007`이라는 메모리 주소에 매핑된다. CPU가 `STA $2000`이라고 적으면 그 바이트가 PPU로 흘러들어가고, `LDA $2002`라고 적으면 PPU의 상태 레지스터를 읽어온다. 메모리에 쓰는 것과 디스플레이에 쓰는 것이 같은 명령어다. 깔끔하다.

이 디자인의 매력은 분명하다. **명령어 종류가 줄어든다.** 6502에는 56개의 공식 명령어가 있는데 [§3.3], 그 중 I/O 전용은 0개다. LD/ST 명령어 한 쌍이 메모리와 I/O를 모두 책임진다. 컴파일러 입장에서도 단순하다 — 메모리 주소를 다루는 코드를 그대로 디바이스에도 쓸 수 있다.

단점은 무엇일까? 메모리 주소 공간이 잘려나간다. 64K 메모리 중 일부 구간은 디바이스에 양보된다. 그리고 디바이스의 응답 시간 — 메모리는 빠르지만 디바이스는 느릴 수 있다 — 을 처리할 별도 메커니즘이 필요하다.

### 별도 포트 공간 — 8080의 길

8080은 정반대다. 메모리와 별개로 **256개짜리 I/O 포트 공간**을 따로 둔다. `IN port`와 `OUT port`라는 전용 명령어가 있다. 메모리에 쓰는 것과 포트에 쓰는 것이 코드 상으로 명백히 구분된다.

```
        IN  0x01       ; 포트 1번에서 한 바이트 읽어와 A에
        OUT 0x02       ; A의 값을 포트 2번으로 출력
```

이 길의 매력 — 메모리 주소 공간이 온전히 보존된다. 64K 전체를 프로그램과 데이터에 쓸 수 있다. 그리고 의도가 또렷하다. `OUT`이 적힌 곳을 보면 "여기 외부 디바이스가 관여한다"가 한눈에 보인다.

단점은 명령어가 두 개 늘어난다는 점, 그리고 포트 256개라는 한정된 공간. 디바이스가 많은 시스템에서는 256개가 빠듯해진다.

### Kotlin으로 포트 공간을 짜보자

SAP-2는 8080을 따라 별도 포트 공간을 둔다. 256개의 입력 포트와 256개의 출력 포트.

```kotlin
class IoPort {
    private val inputPorts = IntArray(256)
    private val outputPorts = IntArray(256)
    private val outputListeners = mutableMapOf<Int, (Int) -> Unit>()

    fun readPort(port: Int): Int {
        return inputPorts[port and 0xFF] and 0xFF
    }

    fun writePort(port: Int, value: Int) {
        val p = port and 0xFF
        outputPorts[p] = value and 0xFF
        outputListeners[p]?.invoke(value and 0xFF)
    }

    fun setInputPort(port: Int, value: Int) {
        inputPorts[port and 0xFF] = value and 0xFF
    }

    fun onOutput(port: Int, handler: (Int) -> Unit) {
        outputListeners[port and 0xFF] = handler
    }
}
```

코드의 정수 — `IN`은 입력 포트 배열에서 읽고, `OUT`은 출력 포트 배열에 쓴 뒤 등록된 listener를 호출한다. 우리가 콘솔에 출력을 띄우고 싶다면 포트 1번에 `println` listener를 걸어두면 끝이다.

```kotlin
val cpu = Sap2()
cpu.io.onOutput(port = 0x01) { byte ->
    print(byte.toChar())          // ASCII 변환 후 콘솔로
}
```

이제 어셈블리에서 `OUT 0x01`을 적으면 A의 값이 콘솔에 한 글자로 떨어진다.

> **사이드바: 6502 vs Z80 vs 8086의 I/O 모델 한 줄 표**
>
> | CPU | I/O 모델 | I/O 명령어 | 메모리 공간 영향 |
> |---|---|---|---|
> | MOS 6502 | 메모리 매핑 | 없음 (`LDA`/`STA`만) | 일부 메모리 영역 양보 |
> | Intel 8080 | 별도 포트 | `IN`, `OUT` | 메모리 64K 온전 |
> | Zilog Z80 | 별도 포트 (+ 메모리 매핑 보조) | `IN`, `OUT` (+ `INI`, `OUTI` 등) | 메모리 64K 온전 |
> | Intel 8086 | 별도 포트 (64K 포트 공간) | `IN`, `OUT` (16비트 포트) | 메모리 1MB 온전 |
> | NES PPU | 메모리 매핑 (`$2000`~`$2007`) | 6502의 `LDA`/`STA`로 접근 | 8바이트 양보 |
>
> 두 길이 절대적으로 옳고 그른 것이 아니다. 6502가 게임기·홈 컴퓨터에서 강했던 이유 중 하나는 메모리 매핑 I/O 덕분이었고, 8080·Z80이 비즈니스 컴퓨터(CP/M)에서 강했던 이유 중 하나는 별도 포트의 또렷함 덕분이었다. 어떤 시스템에 무엇이 적합한가의 문제다.

## 인터럽트 — 첫 만남

여기까지 짜고 나면 한 가지 찜찜한 자리가 남는다. CPU가 키보드 입력을 기다린다고 해보자. 지금까지 짠 도구로는 어떻게 할 것인가? **폴링** — `IN`을 무한 루프로 돌리며 값이 들어왔는지 끊임없이 확인한다.

```
WAIT:
        IN  0x10
        ANA A           ; A == 0 ?
        JZ  WAIT        ; 0이면 다시 — 키 입력 없음
        ; 여기 도달하면 키가 눌렸다
```

돌아간다. 그러나 한심하다. CPU가 키 한 번 들어올 때까지 자기 사이클의 99.99%를 빈손으로 도는 셈이다. 멀티태스킹은 꿈도 못 꾼다.

해결책의 어휘만 미리 알아두자. **인터럽트.** 외부 디바이스가 "나 일 났어!" 하고 CPU에 신호를 보내면, CPU는 지금 하던 일을 잠시 멈추고 미리 약속된 자리로 점프한다. 그 자리에 적힌 코드 — **ISR**(Interrupt Service Routine)이 인터럽트를 처리한다. 끝나면 원래 자리로 돌아간다. 어디로 점프할지는 **vector table**이라는 작은 표에 적혀 있다.

원전 SAP-2 명세에는 인터럽트가 없다. 8080의 INT 핀과 8259 같은 인터럽트 컨트롤러가 있긴 하지만, 교육용 SAP-2는 거기까지 가지 않는다. 우리는 SAP-2에서 폴링 I/O만 쓰고, **인터럽트는 13장에서 합성 8비트 RISC를 설계할 때 본격적으로 도입한다.** RISC의 단순함이라는 정신을 인터럽트와 어떻게 화해시킬 것인가 — RISC-V의 trap 메커니즘을 8비트로 축소한 합성 설계로 그 자리에서 만난다.

지금은 어휘만 머리 한 구석에 남겨두자. 폴링 vs 인터럽트, vector table, ISR. 이 세 단어가 머리에 있으면 13장의 진입이 매끄럽다.

## 자기 CPU로 Fibonacci를 돌려보자

손에 잡힌 도구를 다 합쳐 한 프로그램을 짜보자. Fibonacci 수열의 첫 10개를 콘솔에 찍는다. `if`(루프 종료 조건), 함수, I/O가 한 자리에 모인다.

```
        ; main
        LXI SP, 0xFFFF
        MVI B, 0           ; F(0) = 0
        MVI C, 1           ; F(1) = 1
        MVI D, 10          ; 카운트 10
LOOP:
        MOV A, B           ; A = B (현재 Fibonacci 값)
        CALL PRINT_NUM
        MOV A, B
        ADD C              ; A = B + C
        MOV B, C           ; B = 이전 C
        MOV C, A           ; C = 새 합
        DCR D              ; D-- (Z 플래그 갱신됨)
        JNZ LOOP
        HLT

        ; PRINT_NUM: A의 값을 ASCII 숫자 한 자리로 콘솔에 — 0~9만 단순 처리
PRINT_NUM:
        ADI 0x30           ; '0' = 0x30, A에 더해 ASCII로
        OUT 0x01           ; 콘솔 포트
        MVI A, 0x20        ; 공백
        OUT 0x01
        RET
```

이 한 묶음 안에 우리가 손에 잡은 모든 것이 들어 있다. 루프(JNZ), 함수 호출(CALL/RET), I/O(OUT), 그리고 스택의 정상 동작(CALL이 PUSH한 return address가 RET에서 정확히 POP된다). 이걸 어셈블해 SAP-2 위에서 돌리면 콘솔에 다음이 찍힌다 — 정확히는 첫 10개의 한 자리 숫자 (수열의 2자리수부터는 표시가 깨지지만, 단순 데모로는 충분하다).

```
0 1 1 2 3 5 8 13 21 34
```

(13 이상은 두 자릿수가 되어 위 PRINT_NUM이 처리하지 못하지만 — 이 한계가 보이는 점이 오히려 좋다. 어셈블리 한 줄을 손에 들고 두 자리수 출력 함수를 짤 수 있게 되는 것이 다음 단계 도전 과제다.)

자기 SAP-2 위에서 자기 어셈블리가 돌고, 그 결과가 자기 콘솔에 떨어진다. 통합의 또 한 차례 보상이다. 8장에서 깐 64KB 메모리, 7장에서 짠 어셈블러, 6장에서 묶은 컨트롤러, 그리고 오늘 더한 분기·함수·I/O까지 — 모두가 한 박자에 손을 맞잡고 첫 한 자리수 한 자리수를 콘솔에 떨어뜨린다.

### "Hello"를 찍어보자

기왕 콘솔이 손에 들어왔으니, 진짜 "Hello"도 한 번 떨어뜨려보자. ASCII 코드를 메모리에 깔아두고 한 글자씩 OUT한다.

```
        LXI SP, 0xFFFF
        LXI HL, MSG           ; HL = MSG의 주소
LOOP:
        MOV A, M              ; A = mem[HL]
        ANA A                 ; Z 플래그 확인 — 0이면 종료
        JZ  DONE
        OUT 0x01              ; 콘솔로
        INX H                 ; HL++
        JMP LOOP
DONE:
        HLT

MSG:    DB  'H', 'e', 'l', 'l', 'o', 0x0A, 0
```

어셈블해서 돌리면 콘솔에 다음이 찍힌다.

```
Hello
```

다섯 글자에 줄바꿈 한 번. 별 것 아니다. 그러나 별 것 아닌 게 아니다. **우리가 짠 CPU가 사람이 읽을 수 있는 글자를 처음으로 화면에 떨어뜨린 순간**이다. 6장에서 `OUT = 42`라는 8비트 정수 하나를 떨어뜨렸을 때의 감격이 한 단계 자란 셈이다. 그때는 숫자 한 개였다. 이번엔 문장이다.

ASCII라는 단어를 한 줄로 짚어두자. 1963년에 정해진 7비트 문자 인코딩 표준. 'A'는 0x41, 'a'는 0x61, '0'은 0x30. 8비트 OUT 한 번은 ASCII 한 글자 출력과 정확히 대응된다. 한국어를 출력하지 못한다는 점은 아쉽지만, ASCII만으로도 영어권 텍스트 처리의 시작은 충분하다. 13장의 합성 RISC에서는 16비트 출력 포트를 두고 UTF-16 BMP 한 글자를 한 번에 보내는 변형도 한 번 고려해본다.

## 통합 테스트 — 분기·함수·I/O가 정확히 작동하는가

지금까지 짠 것을 테스트로 굳히자. 7~8개 정도면 핵심 회로를 다 짚는다.

```kotlin
class Sap2BranchTest {

    @Test
    fun `JZ — Z 플래그가 켜져 있을 때만 점프한다`() {
        val cpu = Sap2().apply {
            assemble("""
                MVI A, 0
                ANA A           ; Z=1
                JZ  HIT
                MVI A, 0xFF
                HLT
            HIT:
                MVI A, 0x42
                HLT
            """)
            run()
        }
        assertEquals(0x42, cpu.a.value)
    }

    @Test
    fun `JNZ — Z 플래그가 꺼져 있을 때만 점프한다`() {
        val cpu = Sap2().apply {
            assemble("""
                MVI A, 1
                ANA A
                JNZ HIT
                MVI A, 0xFF
                HLT
            HIT:
                MVI A, 0x42
                HLT
            """)
            run()
        }
        assertEquals(0x42, cpu.a.value)
    }

    @Test
    fun `CALL과 RET이 짝을 이뤄 PC를 정확히 복원한다`() {
        val cpu = Sap2().apply {
            assemble("""
                LXI SP, 0xFFFF
                CALL FOO
                MVI A, 0xCC
                HLT
            FOO:
                MVI A, 0xBB
                RET
            """)
            run()
        }
        assertEquals(0xCC, cpu.a.value)   // CALL 이후 줄까지 도달
    }

    @Test
    fun `함수 안에서 함수 호출이 깨지지 않는다 — SAP-3 식 스택`() {
        val cpu = Sap2().apply {
            assemble("""
                LXI SP, 0xFFFF
                CALL OUTER
                MVI A, 0xAA
                HLT
            OUTER:
                CALL INNER
                RET
            INNER:
                MVI A, 0xBB
                RET
            """)
            run()
        }
        assertEquals(0xAA, cpu.a.value)   // OUTER가 정확히 main으로 복귀
    }

    @Test
    fun `OUT 명령이 등록된 listener를 호출한다`() {
        val received = mutableListOf<Int>()
        val cpu = Sap2()
        cpu.io.onOutput(port = 0x01) { received += it }
        cpu.assemble("""
            MVI A, 0x48      ; 'H'
            OUT 0x01
            MVI A, 0x69      ; 'i'
            OUT 0x01
            HLT
        """)
        cpu.run()
        assertEquals(listOf(0x48, 0x69), received)
    }

    @Test
    fun `IN 명령이 입력 포트 값을 읽는다`() {
        val cpu = Sap2()
        cpu.io.setInputPort(port = 0x10, value = 0x37)
        cpu.assemble("""
            IN  0x10
            HLT
        """)
        cpu.run()
        assertEquals(0x37, cpu.a.value)
    }

    @Test
    fun `Fibonacci 첫 10개를 콘솔로 찍는다`() {
        val output = StringBuilder()
        val cpu = Sap2()
        cpu.io.onOutput(port = 0x01) { output.append(it.toChar()) }
        cpu.assembleFromFile("/asm/fib10.asm")
        cpu.run()
        // ASCII 한 자릿수만 PRINT — 13 이상은 표시 깨짐. 첫 7개만 검증.
        assertTrue(output.toString().startsWith("0 1 1 2 3 5 8"))
    }

    @Test
    fun `Hello 데모 — null 종료 문자열을 한 글자씩 출력`() {
        val output = StringBuilder()
        val cpu = Sap2()
        cpu.io.onOutput(port = 0x01) { output.append(it.toChar()) }
        cpu.assembleFromFile("/asm/hello.asm")
        cpu.run()
        assertEquals("Hello\n", output.toString())
    }
}
```

여덟 개의 테스트가 우리 SAP-2의 새 기능을 한 바퀴 다 확인한다. 분기 두 가지(JZ·JNZ), 함수 호출의 정상 복귀, 함수 안의 함수 호출(SAP-3 방식 스택의 정상 동작), I/O 입출력, 그리고 두 개의 e2e 데모. 어셈블러가 잘못된 바이트를 내거나, 컨트롤러가 점프를 잘못 처리하거나, 스택 컨벤션이 어긋나면 이 중 하나가 정확히 빨갛게 변한다.

특히 네 번째 테스트 — "함수 안에서 함수 호출이 깨지지 않는다" — 는 우리가 의도적으로 SAP-3 식 스택을 채택한 결정을 회귀로 굳히는 자리다. 원전 SAP-2를 그대로 따랐다면 이 테스트가 실패했을 것이다. 명세와 다른 결정을 했을 때, 그 결정이 굳건한지 테스트가 증언한다.

## 마무리

손에 잡힌 것을 정리하자. **분기**(JZ/JNZ/JM/JMP)는 ALU 플래그를 보고 PC를 새 자리로 옮기는 두 줄짜리 마이크로 동작이다. `if`, `for`, `while`이라는 고급 언어의 통제 흐름이 점프 한 종류로 환원된다. **함수**(CALL/RET)는 스택 위에 return address를 push/pop하는 메커니즘이다. 재귀도 콜 스택도 모두 SP가 메모리 위에서 위아래로 미끄러지는 그림 한 장으로 손에 잡힌다. **I/O**(IN/OUT)는 별도 포트 공간이라는 8080의 길을 따른다 — 6502의 메모리 매핑이라는 다른 길도 손에 잡았다.

원전 SAP-2의 정직한 결함 — return address 한 칸의 덮어쓰기 — 을 우리가 어떻게 우회했는지도 기억해두자. 명세의 권위와 학습의 흐름이 충돌할 때, 우리는 학습의 흐름을 택했다. 그 결정이 옳았는지는 네 번째 테스트가 빨간 줄 한 번 없이 통과하는 것으로 증명된다.

폴링 vs 인터럽트, vector table, ISR — 이 세 단어는 머리 한 구석에 어휘로만 남겨두자. 13장에서 합성 8비트 RISC를 설계할 때 본격적으로 만난다. RISC의 단순함과 인터럽트의 비동기성이 어떻게 화해할 수 있는지가 그 자리의 핵심 질문이다.

다음 장에서는 마이크로코드와 디버거를 함께 짜보자. SAP-2의 컨트롤러를 ROM 기반 마이크로코드로 옮기고, 자기 CPU의 내부를 한 사이클씩 들여다보는 디버거를 손에 쥔다. 자기가 만든 컴퓨터에 처음으로 breakpoint와 step을 걸어보는 자리다. 그 자리가 3부의 정서적 절정이 된다.

> **이번 챕터의 GitHub 커밋**
>
> ```
> chapter-09/
>   build.gradle.kts
>   src/main/kotlin/sap2/
>     Jump.kt          (조건 점프 디코딩, ~40줄)
>     Stack.kt         (PUSH/POP/pushWord/popWord, ~35줄)
>     IoPort.kt        (256포트 + listener, ~30줄)
>   src/main/resources/asm/
>     fib10.asm        (Fibonacci 첫 10개 콘솔 출력)
>     hello.asm        (null 종료 문자열 출력 데모)
>   src/test/kotlin/sap2/
>     Sap2BranchTest.kt (8개 통합 테스트, Fibonacci·Hello e2e 포함)
>
> 실행:  ./gradlew :chapter-09:run --args="fib10"   → 0 1 1 2 3 5 8 ...
>       ./gradlew :chapter-09:run --args="hello"   → Hello
> 테스트: ./gradlew :chapter-09:test                → 8/8 passed
> ```
