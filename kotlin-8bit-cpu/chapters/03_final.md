# 3장. SAP-1의 청사진과 첫 모듈

2장에서 30줄짜리 미니 CPU를 돌려봤다고 해보자. 첫 화면에 숫자가 찍히는 순간의 짜릿함은 며칠 가지만, 코드를 다시 들여다보면 곧 찜찜한 구석이 보인다. 메모리는 그냥 `IntArray` 한 덩어리였고, 명령어는 `when` 한 블록에 욱여넣었으며, "클록"이라 부를 만한 것도 없었다. 결국 우리가 만든 것은 "한 번에 다 일어나는" 무엇이었다. 진짜 CPU는 그렇게 한 번에 일어나지 않는다.

그렇다면 이제 무엇을 해야 할까? 우리가 짜야 할 다음 단계의 CPU는 어떤 모습이어야 하는가? 트랜지스터 5만 개짜리 8086을 흉내 낼 수는 없다. Z80도 너무 무겁다. 6502도 어드레싱 모드만 열세 가지다. 입문자가 발을 디딜 자리는 어디인가?

여기서 한 권의 교과서가 1980년대부터 변함없이 같은 답을 주고 있다. Malvino와 Brown의 *Digital Computer Electronics*다. 이 책은 "SAP"라는 이름의 CPU를 소개한다. **Simple-As-Possible.** 이름 그대로다. "가능한 한 단순한". 그리고 정말로 단순하다. 8비트 데이터, 4비트 주소, 메모리 16바이트, 명령어 다섯 개. 그게 전부다.

"고작 16바이트?"라며 한숨 쉬는 독자가 분명 있을 것이다. 메모리에 트윗 한 줄도 못 담는다. 그러나 SAP-1의 작음은 빈약함이 아니라 **선의 빈약함이다**. 데이터패스의 모든 선이 한눈에 들어온다. 클록 한 번에 무엇이 어디로 이동하는지를 종이 한 장에 그릴 수 있다. 이 작음을 손에 쥐어보지 않은 채로 ARM이나 RISC-V를 들여다보면, 신호선이 천 개쯤 되는 다이어그램 앞에서 그저 멍해질 뿐이다. 우리는 16바이트짜리 우주에서 살 줄을 먼저 익혀야 한다.

다섯 챕터에 걸쳐 짤 SAP-1의 청사진을 함께 펼쳐보자. 전체 지도를 보고, 한국 학습자의 약점이라 회자되는 **datasheet 읽기**도 같이 연습한다. 그러고 나서 첫 두 모듈을 Kotlin으로 짜본다. 가벼운 워밍업으로 시작하자.

## SAP-1 명세 한눈에 — 다섯 줄짜리 ISA

SAP-1의 명세는 표 하나로 끝난다. 표를 먼저 보자.

| 항목 | 값 |
|------|---|
| 데이터 폭 | 8비트 |
| 어드레스 폭 | 4비트 |
| 메모리 | 16바이트 RAM |
| 명령어 | 5개 (LDA, ADD, SUB, OUT, HLT) |
| 누산기 | 1개 (A 레지스터) |
| ALU | 8비트 2의 보수 가산/감산 + Z·C 플래그 |
| 컨트롤 | 조합 논리(또는 EEPROM 룩업 테이블) |
| T-state | 명령어당 6 클록 |

명령어 5개를 한 줄씩 풀어보자.

- `LDA addr` — 주소 `addr`의 값을 A 레지스터에 로드한다(LoaD A)
- `ADD addr` — 주소 `addr`의 값을 A에 더한다
- `SUB addr` — 주소 `addr`의 값을 A에서 뺀다
- `OUT` — A의 값을 출력 레지스터로 옮긴다
- `HLT` — 클록을 멈춘다 (HaLT)

이걸로 뭘 할 수 있나? "5와 3을 더해 8을 출력하는" 프로그램이 우리가 만들 수 있는 첫 산물이다. 너무 작아 실망스러운가? 그렇다면 잠깐 생각해보자. 이 다섯 줄짜리 ISA에 `JMP`만 추가하면 무한 루프가 가능하다. 거기에 조건 분기 하나만 더해주면 튜링 완전성에 도달한다. SAP-2 단계에서 우리가 그 길을 걷는다. 그러나 그 전에, 다섯 줄짜리 우주에서 fetch-decode-execute가 어떻게 돌아가는지를 손에 쥐어야 한다.

> **SAP-1의 ISA는 Intel 8080/8085와 상위 호환이다.** Malvino의 의도는 명확하다. 학습자가 SAP에서 익힌 어셈블리가 곧장 8080으로 이어지도록. SAP-2에 가면 이 호환성이 더 분명해진다. 우리가 보고 있는 것이 골동품이 아니라, 1970년대 실제 마이크로프로세서로 가는 좁은 다리라는 점을 기억해두자.

### 명령어 인코딩 — 4비트 + 4비트

SAP-1의 명령어는 8비트로 인코딩된다. 상위 4비트가 opcode, 하위 4비트가 operand(주소)다.

```
┌─────────────┬─────────────┐
│  opcode(4)  │  operand(4) │
└─────────────┴─────────────┘
   상위 nibble    하위 nibble
```

`LDA 5`는 어떻게 인코딩될까? LDA의 opcode를 `0x0`이라 정해두면 `0x05`다. `ADD 6`이라면 ADD opcode가 `0x1`일 때 `0x16`이 된다. opcode 표는 다음처럼 합의해두자.

| 명령어 | opcode | 인코딩 예시 |
|--------|--------|-------------|
| LDA    | 0x0    | `LDA 5` → `0x05` |
| ADD    | 0x1    | `ADD 6` → `0x16` |
| SUB    | 0x2    | `SUB 7` → `0x27` |
| OUT    | 0xE    | `OUT`   → `0xE0` |
| HLT    | 0xF    | `HLT`   → `0xF0` |

OUT과 HLT는 operand가 없는데 왜 4비트씩이나 차지하나? 자리가 남기 때문이다. opcode 4비트는 명령어 16개까지 표현 가능하고, 우리는 다섯 개만 쓴다. 나머지 열한 자리는 비어 있다. 이 빈자리가 후에 SAP-2로 진화할 여지가 된다.

## 데이터패스 한눈에 보기 — 누가 누구와 이야기하는가

SAP-1의 핵심 모듈을 나열해보자. 익숙해질 때까지 종이에 그려보는 편이 낫다.

| 모듈 | 역할 |
|------|------|
| 클록(Clock) | 모든 모듈을 동기화하는 박자 |
| 프로그램 카운터(PC) | 다음에 실행할 주소를 가리키는 4비트 카운터 |
| MAR(Memory Address Register) | RAM에 보낼 주소를 잠시 잡아두는 4비트 레지스터 |
| RAM | 16바이트 메모리. 주소 0~15. 한 칸에 8비트 저장 |
| IR(Instruction Register) | 방금 읽어온 명령어 한 바이트를 잡아두는 곳 |
| 컨트롤러/시퀀서 | "지금은 fetch", "지금은 execute" 같은 신호를 모듈들에게 뿌리는 두뇌 |
| A 레지스터 | 누산기. 산술 결과의 한쪽 피연산자이자 결과 |
| B 레지스터 | ALU의 다른 피연산자 |
| ALU | 8비트 가산기/감산기 |
| 출력 레지스터(O) | `OUT` 명령으로 A의 값을 옮겨두는 곳. 외부에서 LED나 콘솔로 보이는 창 |
| W-bus | 모든 모듈을 잇는 공용 8비트 버스 |

말이 길다. 한 문장으로 줄이면 이렇다. **모든 모듈은 W-bus에 매달려 있고, 컨트롤러가 매 클록마다 "지금은 누가 버스에 쓰고, 누가 버스에서 읽는다"를 결정한다.**

다이어그램으로 그리면 다음과 비슷한 모양이 된다.

```
        ┌──────────────────── W-bus(8) ────────────────────┐
        │                                                  │
   ┌────┴─────┐  ┌──────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌────┴────┐
   │   PC(4)  │  │ MAR  │  │ RAM │  │ IR  │  │  A  │  │ Output  │
   │          │  │      │  │16B  │  │     │  │     │  │         │
   └────┬─────┘  └──────┘  └─────┘  └─────┘  └──┬──┘  └─────────┘
        │                                       │
        │                                    ┌──┴──┐  ┌─────┐
        │      ┌──────────────────────┐      │ ALU │←─┤  B  │
        │      │ 컨트롤러 / 시퀀서    │      └─────┘  └─────┘
        │      │ (마이크로코드)       │
        └─────→│                      │←─── 클록
               └──────────┬───────────┘
                          │
                control signals(12개) → 모든 모듈
```

각 모듈에는 두 종류의 핀이 매달려 있다고 보면 된다. 하나는 **로드(load) 신호**다. "지금 이 모듈은 버스에 있는 값을 자기 안으로 가져간다"는 뜻이다. 다른 하나는 **인에이블(enable) 신호**다. "지금 이 모듈은 자기 안의 값을 버스에 띄운다"는 뜻이다. PC에는 `Cp`(증가), `Ep`(버스에 띄움), `Lp`(외부에서 로드) 같은 신호가 있다. A 레지스터에는 `La`(로드), `Ea`(버스에 띄움)가 있다. 컨트롤러는 매 클록마다 이 핀들을 적절히 켜고 끄는 일을 한다.

그게 다다. SAP-1의 작동 전체가 "클록 → 컨트롤러가 12개 신호를 결정 → 모듈들이 그 신호대로 버스에 읽고 쓴다"의 무한 반복이다. 이 그림 한 장을 머릿속에 박아두면, 앞으로 다섯 챕터의 코드가 자기 자리에 차곡차곡 들어맞는다.

### T-state — 명령어 하나가 여섯 클록인 까닭

SAP-1은 **한 명령어를 여섯 클록 사이클**(T1~T6)에 걸쳐 처리한다. 이 여섯 클록이 무엇을 하는지가 SAP-1의 정수다.

| T-state | 단계 | 하는 일 |
|---------|------|---------|
| T1 | fetch 1 | PC의 값을 MAR로 옮긴다 |
| T2 | fetch 2 | PC를 1 증가시킨다 |
| T3 | fetch 3 | MAR가 가리키는 RAM의 값을 IR로 가져온다 |
| T4 | execute 1 | (명령어별로 다름) |
| T5 | execute 2 | (명령어별로 다름) |
| T6 | execute 3 | (명령어별로 다름) |

T1~T3는 모든 명령어가 공유한다. 이것이 **fetch 사이클**이다. T4~T6는 명령어마다 내용이 다르다. **execute 사이클**이다. 예컨대 `LDA 5`라면 execute는 이렇게 흐른다.

| T-state | 하는 일 |
|---------|---------|
| T4 | IR의 하위 4비트(주소 5)를 MAR로 옮긴다 |
| T5 | RAM이 그 주소의 값을 버스에 띄우고, A 레지스터가 로드한다 |
| T6 | 아무 일도 안 한다(NOP). 다음 사이클을 위한 여유. |

`HLT`라면 어떨까? T4에서 클록을 멈춘다. 그게 전부다. T5, T6는 영원히 오지 않는다.

여섯 클록을 두는 이유가 뭘까? 답은 이렇다. **명령어 중에 가장 긴 것을 기준으로 맞추기 위해서다.** SAP-1에서 가장 단계가 많은 명령어가 ADD/SUB이고, 이들은 정확히 6 T-state를 필요로 한다. LDA처럼 짧은 명령어는 T6를 그냥 비워둔다. 이 "가장 긴 명령어에 맞춘 고정 길이" 발상은 후에 RISC 설계의 핵심 사상이 된다. 단순성을 위해 약간의 비효율을 감수한다. 1980년대 Patterson이 RISC를 주장하면서 들고 나온 논거의 8비트 버전을 우리는 이미 손에 쥐고 있는 것이다.

### 마이크로코드 — 컨트롤러가 명령어를 "번역"하는 방식

컨트롤러는 매 T-state마다 12개 컨트롤 신호를 켜고 끈다고 했다. 그 결정을 어떻게 내릴까? 답은 의외로 단순하다. **명령어(4비트 opcode) × T-state(6단계) → 12비트 컨트롤 워드.** 거대한 룩업 테이블이다. 16개 opcode × 6 T-state = 96개 행짜리 표를 만들어, 매 클록마다 "지금 IR에 무엇이 있고, 지금 몇 번째 T-state인지"로 그 표를 한 번 조회하면 된다. 이 표가 곧 **마이크로코드**다.

Ben Eater의 실물 SAP-1은 이 표를 EEPROM 두 개에 구워 넣는다. Kotlin에서는? 그냥 2차원 배열 한 줄이다. 이 단순한 변환이 컴파일러도 인터프리터도 아닌 "하드웨어 그 자체"를 흉내 내는 우리의 가장 큰 무기다. 마이크로코드 구현은 6장에서 자세히 다루기로 하고, 지금은 머릿속에 "표 하나면 컨트롤러 완성"이라고만 새겨두자.

## 우리만의 SAP-1 datasheet 한 페이지

여기서 잠깐 멈춰서 한 가지 약속을 하자. 한국 학습자가 약한 영역으로 자주 회자되는 것이 **datasheet 읽는 기술**이다. 영어 PDF 50쪽을 들춰서 핵심 표 두세 개를 뽑아낼 줄 알아야 하는데, 입문자에게는 그 자체가 벽이다. 그래서 모든 챕터의 첫머리에 **"이 챕터의 datasheet 한 장"**을 두기로 하자. 공식 명세를 그대로 베끼는 게 아니라, 우리가 짤 코드의 입력·출력·타이밍을 한 페이지로 정리한 것이다.

3장의 datasheet 페이지를 펴 보자.

> **우리 SAP-1 datasheet (요약판)**
>
> **데이터 폭:** 8비트 (`Int and 0xFF`)
> **주소 폭:** 4비트 (`Int and 0xF`)
> **메모리:** 16바이트 RAM
> **레지스터:** PC(4비트), MAR(4비트), IR(8비트), A(8비트), B(8비트), O(8비트)
> **ALU:** 가산/감산, Z·C 플래그
> **버스:** 8비트 W-bus, 한 클록에 한 모듈만 쓴다
> **클록:** 단상(single-phase). 모든 모듈은 상승 에지에 동작
> **명령어:** LDA(0x0), ADD(0x1), SUB(0x2), OUT(0xE), HLT(0xF)
> **T-state:** 명령어당 6 사이클 (T1~T3 fetch 공통, T4~T6 execute)
> **컨트롤 신호 12개:** Cp, Ep, Lm, ER, Li, Ei, La, Ea, Su, Eu, Lb, Lo (자세한 의미는 6장)
>
> **우리 책의 단순화 결정:**
> - Ben Eater의 실물 SAP-1과 달리, 우리는 클록의 양 에지를 굳이 구분하지 않는다(소프트웨어에서는 의미 없음)
> - W-bus 충돌은 컴파일 타임에 막지 않고, 테스트로 잡는다
> - 마이크로코드 EEPROM 대신 Kotlin `Map`을 쓴다

이 한 페이지를 거듭 들춰보게 될 것이다. 코드를 짜다가 "어, 이 모듈 폭이 몇 비트였더라?" 싶을 때 위로 올라와 표를 본다. 자기 책의 자기 합성 datasheet다. 익숙해지면 다른 칩의 datasheet도 같은 눈으로 보게 될 것이다.

> **사이드바: Ben Eater의 브레드보드 SAP-1과 우리 Kotlin SAP-1의 차이**
>
> Ben Eater의 YouTube 시리즈는 SAP-1을 74LS 시리즈 IC와 브레드보드로 짓는다. 학습 효과 면에서는 가장 영향력 큰 콘텐츠일 것이다. 그런데 부품 값이 약 300달러, 디버깅 시간의 90%가 회로 문제, 결국 16바이트짜리 컴퓨터에 시간을 무한히 쏟게 된다는 후기가 적지 않다. HN 토론을 옮겨보면 한 쪽은 "전선을 자르고 손으로 꽂아본 감각이 임베디드 직관을 만든다"고 말하고, 다른 쪽은 "학습 효율로는 nand2tetris 같은 시뮬레이터가 비교 불가"라고 응수한다. 합의 지점은 대체로 "이론 → 시뮬레이터 → 실물"의 3단계가 이상적이라는 것이다. 이 책은 가운데 단계, 시뮬레이터에 집중한다. 끝에서 Ben Eater를 추천하면서 3단계로 가는 다리를 놓는다.
>
> Kotlin 시뮬레이터의 비교 우위는 분명하다. **편집-실행 루프가 초 단위**다. 회로의 floating input이나 전압 강하 같은 물리적 변수에 시간을 뺏기지 않는다. 대신 잃는 것도 있다. "이 명령어가 실제로 몇 나노초 걸리는지"의 감각이다. 우리는 14장에서 cycle-accurate 리팩토링을 하면서 그 감각의 일부를 되찾을 것이다.

## Kotlin 패턴의 선택 — 무엇을 무엇으로 모델링할 것인가

이제 코드를 쓸 차례다. 그런데 그 전에 한 번 멈춰 정해야 할 것이 있다. **SAP-1의 부품들을 Kotlin의 어떤 구성요소로 표현할 것인가?**

이 결정이 책 전체를 가른다. 한 번 정하면 14장까지 끌고 가야 하니 가볍지 않다. 그러니 함께 고민해보자.

### 레지스터 — 클래스로 본다

레지스터는 "값을 잡아두는 작은 상자"다. 매 클록마다 값이 들어왔다 나간다. 가장 자연스러운 모델은 **클래스다**.

```kotlin
class Register(val name: String, width: Int) {
    private val mask = (1 shl width) - 1
    var value: Int = 0
        private set

    fun load(v: Int) {
        value = v and mask
    }

    override fun toString() = "$name=0x${value.toString(16).padStart(width / 4, '0')}"
}
```

왜 클래스인가? 함수형 데이터 클래스로 표현할 수도 있겠지만, 레지스터는 정의상 **가변 상태**다. 클록 한 번에 값이 바뀐다. 이걸 매번 새 인스턴스로 만드는 함수형 접근은 표현력 면에서 손해를 본다. 우리는 하드웨어를 흉내 내는 중이고, 하드웨어는 그 자리에 "남아 있는" 물건이다. 가변 클래스로 표현하는 편이 낫다.

`width`로 비트 폭을 받아 마스킹을 자동 적용한 점도 봐두자. 4비트짜리 PC에 16을 넣어도 0이 들어간다. 이 작은 안전장치 하나가 디버깅 한나절을 살린다.

### 버스 — 함수 인자로 본다

버스는 어떻게 표현할까? "여러 모듈이 동시에 접근하는 8비트 공용 전선"이다. 클래스로 만들 수도 있다. 그러나 더 단순한 방법이 있다. **버스는 함수 인자 또는 메서드 호출의 흐름이다.**

```kotlin
fun tick() {
    val busValue = pc.value          // PC가 버스에 띄운다
    mar.load(busValue)               // MAR가 버스에서 읽는다
}
```

이 단순함이 우리의 결정이다. 굳이 `Bus` 클래스를 만들어 들고 다니지 않는다. 한 함수 안에서 잠깐 살고 사라지는 로컬 변수 `busValue`로 충분하다. ksim65와 kNES 같은 성숙한 Kotlin 에뮬레이터도 본질적으로 같은 패턴을 쓴다.

물론 이 결정에 반론이 있을 수 있다. "그러면 두 모듈이 동시에 버스에 쓰는 버스 충돌은 어떻게 잡나?" 좋은 질문이다. 실물 회로에서 버스 충돌은 짧은 회로를 만들어 IC를 태운다. Kotlin에서는? 명시적 `Bus` 클래스를 만들어 "이번 클록에 이미 쓰는 모듈이 있다"는 어설션을 걸 수도 있다. 그러나 우리의 결정은 **테스트로 잡는다**다. 컨트롤러의 마이크로코드 표가 잘못되면 두 모듈에 동시에 인에이블 신호가 떨어진다. 그 잘못은 단위 테스트로 충분히 잡힌다. 런타임 어설션을 매 클록마다 도는 비용은 굳이 부담하지 말자.

### 명령어 — sealed class로 본다

명령어는 어떨까? `Int` opcode로 다닐 수도 있고, enum으로 만들 수도 있다. 우리의 선택은 **sealed class**다.

```kotlin
sealed class Instruction {
    data class Lda(val addr: Int) : Instruction()
    data class Add(val addr: Int) : Instruction()
    data class Sub(val addr: Int) : Instruction()
    data object Out : Instruction()
    data object Hlt : Instruction()
}
```

왜 sealed class인가? 첫째, **operand 유무가 명령어마다 다르다**. LDA에는 주소가 있지만 OUT은 없다. enum으로는 표현이 어색하다. data class로 operand를 그대로 묶을 수 있는 sealed class가 자연스럽다.

둘째, `when` 분기가 컴파일러의 완전성 검사 대상이 된다.

```kotlin
fun execute(inst: Instruction) {
    when (inst) {
        is Instruction.Lda -> loadA(inst.addr)
        is Instruction.Add -> addA(inst.addr)
        is Instruction.Sub -> subA(inst.addr)
        Instruction.Out    -> outA()
        Instruction.Hlt    -> halt()
    }
}
```

빠진 분기가 있으면 컴파일러가 경고한다. SAP-2에서 명령어가 39개로 늘어날 때, 이 안전망은 큰 위안이 된다.

셋째, 디스어셈블러를 짤 때 한 번 더 빛을 본다. `0x05` → `Instruction.Lda(5)`로 파싱한 뒤 그대로 `toString()` 찍으면 사람이 읽는 어셈블리가 나온다. data class의 자동 `toString`을 그대로 활용할 수 있다.

### 메모리 — `IntArray`로 본다 (당분간)

8비트 값을 어떻게 표현할 것인가? Kotlin은 `Byte`(signed -128~127), `UByte`(unsigned 0~255), `Int`+마스킹의 세 가지 선택지를 준다. 이 결정은 4장에서 정면으로 다룬다. 지금은 **`Int` + 마스킹**이라는 잠정안만 받아들이자. 이유는 두 가지다.

첫째, JVM에서 가장 빠르고 호환성이 좋다. ksim65도 이 길을 택했다. 둘째, `UByte`는 시프트 연산자 `>>`, `shl`이 직접 지원되지 않는다(Kotlin 1.x.x 시점). 매번 `.toInt().shr(n).toUByte()`처럼 변환을 해줘야 하는데, 입문자에게는 번거롭다.

> *Kotlin 공식 문서: "There is no significant overhead when using unsigned integer types on the JVM... Bit shifts are provided only for UInt and ULong; for the narrower types, both for signed and unsigned, they are under consideration."*

그래서 메모리는 이렇게 표현한다.

```kotlin
class Ram(val size: Int) {
    private val cells = IntArray(size)

    fun read(addr: Int): Int = cells[addr and 0xF] and 0xFF
    fun write(addr: Int, value: Int) {
        cells[addr and 0xF] = value and 0xFF
    }
}
```

`and 0xF`로 주소를, `and 0xFF`로 데이터를 강제 마스킹한다. SAP-1의 4비트 주소·8비트 데이터를 위반하지 않게 만들어두는 작은 안전판이다. 이 안전판이 없으면 디버깅 한나절이 통째로 날아간다. 정말 아찔한 일이다.

> **사이드바: 다른 8비트 CPU는 이 결정을 어떻게 했나**
>
> | 프로젝트 | 8비트 표현 | 비고 |
> |---------|-----------|------|
> | ksim65 (6502 Kotlin) | `Int` + 마스킹 | 가장 성숙한 Kotlin 에뮬레이터. C-64 ROM도 돈다. |
> | kNES (6502+NES Kotlin) | `Int` 위주 | cycle-accurate. Java vNES Kotlin 포팅 |
> | Scuffed-6502Kt | `UByte` | 학습 프로젝트. 시프트 변환의 번거로움이 코드에 보인다 |
> | cbeust/chip-8 (Cédric Beust) | `Int` | TestNG 창시자의 Kotlin Chip-8. |
>
> 패턴이 보이는가? **성숙한 에뮬레이터일수록 `Int`+마스킹을 쓴다.** UByte의 타입 안전성은 매력적이지만, 8비트 CPU의 본질은 `Int`로도 충분히 표현된다. 이 책은 그 선택을 따른다. 단, 후반 챕터에서 `UByte` 마이그레이션을 한 번 보여줘서 두 세계의 차이를 직접 체감하도록 한다.

## 첫 모듈: 클록

지도를 다 펼쳤으니, 이제 **첫 모듈을 짜자.** 가장 단순한 것부터다. 클록.

CPU의 클록이란 무엇인가? 박자다. 모든 모듈이 그 박자에 맞춰 한 단계씩 움직인다. 실물 회로에서 클록은 4MHz, 1GHz 같은 주파수를 가지지만, 우리는 시뮬레이터다. **클록은 그저 "다음 단계로 가자"는 신호이고, `tick()`이라는 함수 호출 한 번이다.**

테스트부터 써보자. SAP-1의 6 T-state를 클록이 순환한다는 것을 검증한다.

```kotlin
// chapter-03/sap1/ClockTest.kt
import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class ClockTest {

    @Test
    fun `클록은 0부터 시작해 T1을 가리킨다`() {
        val clock = Clock()
        clock.tState shouldBe 1
    }

    @Test
    fun `클록은 한 번 tick하면 T2로 간다`() {
        val clock = Clock()
        clock.tick()
        clock.tState shouldBe 2
    }

    @Test
    fun `클록은 T6 다음에 T1으로 돌아온다`() {
        val clock = Clock()
        repeat(6) { clock.tick() }
        clock.tState shouldBe 1
    }

    @Test
    fun `HLT 후에는 tick해도 멈춰 있다`() {
        val clock = Clock()
        clock.halt()
        clock.tick()
        clock.tick()
        clock.tState shouldBe 1
        clock.halted shouldBe true
    }
}
```

테스트가 빨갛다. 좋다. 이제 초록으로 만들자.

```kotlin
// chapter-03/sap1/Clock.kt
class Clock {
    var tState: Int = 1
        private set

    var halted: Boolean = false
        private set

    fun tick() {
        if (halted) return
        tState = if (tState == 6) 1 else tState + 1
    }

    fun halt() {
        halted = true
    }

    fun reset() {
        tState = 1
        halted = false
    }
}
```

코드는 거짓말처럼 작다. 다섯 줄이 채 안 된다. 그런데 이 다섯 줄이 SAP-1의 박자 전체를 만든다. `halted` 체크 하나로 HLT 명령어의 의미도 자연스럽게 표현된다. 그렇다면 의문이 들 것이다. **이게 정말 클록인가?** 회로의 클록은 수정 진동자에서 나오고, 위상이 있고, 듀티 사이클이 있고, 지터가 있다. 우리의 클록은 단지 1부터 6까지 도는 변수다.

답은 이렇다. **시뮬레이터에서의 클록은 "이산 사건의 진행자"다.** 실물 회로의 클록이 가진 물리적 속성은 우리에게 무의미하다. 우리에게 의미 있는 것은 "지금 T-state가 몇이냐"뿐이다. 14장의 cycle-accurate 챕터에 가면 이 인식이 한 번 더 흔들리는데, 거기서는 한 명령어 안의 모든 모듈이 동일한 클록의 동일한 에지를 본다는 사실이 결정적으로 중요해진다. 지금은 그 단순한 형태로 충분하다.

작은 디테일 하나 짚어두자. `tState`를 0이 아니라 **1부터 시작**하게 한 점이다. Malvino 교과서가 T-state를 T1, T2, ...로 부르기 때문이다. 코드 안에서도 그 명칭을 그대로 유지하면 datasheet와 코드의 거리를 줄일 수 있다. 0-based가 익숙한 프로그래머에게는 살짝 어색해도, datasheet와 같은 말을 쓰는 편이 낫다.

## 두 번째 모듈: 프로그램 카운터

다음은 PC다. **다음에 실행할 명령어의 주소를 가리키는 4비트 카운터**.

SAP-1의 PC가 가져야 할 동작을 정리해보자.

1. 리셋 시 0을 가리킨다
2. `increment()`로 1 증가한다
3. 4비트이므로 15 다음은 0으로 순환한다
4. 외부에서 임의 주소를 로드할 수 있다(JMP 명령어를 위한 인터페이스. SAP-1에서는 안 쓰지만 SAP-2에서 쓴다)
5. 버스에 현재 값을 띄울 수 있다(`output()`)

테스트로 정리하면 이렇다.

```kotlin
// chapter-03/sap1/ProgramCounterTest.kt
import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class ProgramCounterTest {

    @Test
    fun `PC는 0에서 시작한다`() {
        val pc = ProgramCounter()
        pc.value shouldBe 0
    }

    @Test
    fun `increment하면 1 증가한다`() {
        val pc = ProgramCounter()
        pc.increment()
        pc.value shouldBe 1
    }

    @Test
    fun `15 다음은 0으로 순환한다`() {
        val pc = ProgramCounter()
        repeat(16) { pc.increment() }
        pc.value shouldBe 0
    }

    @Test
    fun `JMP 인터페이스로 임의 주소를 로드할 수 있다`() {
        val pc = ProgramCounter()
        pc.jumpTo(7)
        pc.value shouldBe 7
    }

    @Test
    fun `4비트를 초과하는 주소를 로드해도 4비트로 마스킹된다`() {
        val pc = ProgramCounter()
        pc.jumpTo(0xAB)
        pc.value shouldBe 0xB
    }

    @Test
    fun `output은 현재 값을 그대로 반환한다`() {
        val pc = ProgramCounter()
        pc.increment()
        pc.increment()
        pc.output() shouldBe 2
    }
}
```

여섯 개의 테스트. 다섯째 테스트가 흥미롭다. "0xAB를 넣어도 0xB만 남는다"는 동작이 4비트 카운터의 물리적 진실이다. 실물 회로에서 4비트 카운터에 8비트 값을 흘려보내면 상위 4비트는 사라진다. 우리 코드도 그 동작을 모사해야 한다. 그렇지 않으면 SAP-2로 갔을 때 "왜 PC가 64KB까지 늘어났냐"는 자기 코드의 거짓말에 시달리게 된다. 초난감한 일이다.

구현은 이렇다.

```kotlin
// chapter-03/sap1/ProgramCounter.kt
class ProgramCounter(private val width: Int = 4) {
    private val mask: Int = (1 shl width) - 1

    var value: Int = 0
        private set

    fun increment() {
        value = (value + 1) and mask
    }

    fun jumpTo(addr: Int) {
        value = addr and mask
    }

    fun reset() {
        value = 0
    }

    fun output(): Int = value
}
```

`width = 4`를 생성자 파라미터로 받아둔 점에 주목하자. SAP-2로 가면 PC가 16비트가 된다. 같은 클래스를 `ProgramCounter(width = 16)`으로 재사용할 수 있다. 작은 미래 대비다.

`mask = (1 shl width) - 1`은 4비트면 `0xF`, 16비트면 `0xFFFF`다. **비트 폭을 인자로 받으면 마스크가 자동으로 따라온다**는 점이 Kotlin의 정수 타입 인플레이션을 우회하는 우리의 작은 트릭이다. 익숙해지면 모든 레지스터를 이 패턴으로 짠다.

### 두 모듈을 잇는 첫 통합 테스트

각 모듈이 따로 통과한다고 끝이 아니다. 두 모듈을 같이 돌려보는 작은 시나리오 하나는 짜둬야 한다. 미래의 자기 자신을 위한 안전망이다.

```kotlin
@Test
fun `클록 T2에 PC가 증가하는 시나리오`() {
    val clock = Clock()
    val pc = ProgramCounter()

    // SAP-1의 fetch 사이클에서 T2가 PC 증가 단계라고 정의한다
    repeat(2) { 
        if (clock.tState == 2) pc.increment()
        clock.tick()
    }

    // T1 → T2 진입 시점에 PC가 1 증가했다
    pc.value shouldBe 1
}
```

지금은 컨트롤러가 없어서 클록의 `tState`를 직접 보는 좀 어색한 통합 테스트지만, 6장의 컨트롤러가 들어오면 이 자리가 정말로 깔끔해진다. **컨트롤러가 매 T-state마다 어느 모듈을 깨울지 결정하는 것**이 SAP-1의 핵심이라는 걸 다시 한 번 기억해두자.

## TDD를 권하는 이유

여기까지 코드 두 모듈, 테스트 열한 개를 짰다. 양으로만 보면 코드보다 테스트가 많다. 부담스러워 보일 수 있다. 그러나 에뮬레이터 개발에서 TDD가 가지는 의미는 일반 애플리케이션과는 결이 다르다.

에뮬레이터는 **참조 명세(reference specification)가 명확한 소프트웨어**다. SAP-1이라면 Malvino의 책, 6502라면 MOS의 datasheet, NES라면 nestest.nes 같은 검증 ROM이 있다. 명세가 명확하다는 건 무슨 뜻인가? **테스트로 정확하게 표현할 수 있다는 뜻이다**. "이 명령어를 이 상태에서 실행하면 이 결과가 나와야 한다"가 한 줄로 적힌다. 이건 보통 비즈니스 로직에서는 누리기 힘든 호사다.

게다가 에뮬레이터는 **회귀가 가장 무서운 분야**다. ADD를 고치다가 SUB이 깨지고, ALU를 손대다가 플래그가 어긋난다. 회귀를 늦게 발견하면 디버깅 비용이 폭발한다. 일주일 전 잘 돌던 코드가 어디서 깨졌는지 모른 채 git log를 뒤지는 일은 끔찍하다. 6502 커뮤니티가 klaus2m5의 `6502_65C02_functional_tests`를 거의 종교처럼 떠받드는 것도, NES 개발자가 nestest.nes를 첫 마일스톤으로 두는 것도 그래서다. 우리 SAP-1에는 그런 외부 테스트 ROM이 없다. **그래서 처음부터 직접 짠다.** 명령어 다섯 개 × 플래그 두 개 × 경계 케이스 몇 개 = 약 50개. 한 챕터에 한 줌씩 쌓아가면 마지막에는 단단한 안전망이 된다.

TDD가 부담스럽다면, 적어도 **테스트와 구현을 같은 커밋에 넣는 규율**은 지키는 편이 낫다. 테스트 없이 들어간 코드는 다음 챕터에서 거의 반드시 우리를 배신한다. 경험에서 우러나는 충고다.

> **GitHub 산출물**
>
> 이 챕터에서 코드를 짤 GitHub 레포의 디렉터리 구조는 다음과 같다.
>
> ```
> chapter-03/
>   build.gradle.kts
>   src/main/kotlin/sap1/
>     Clock.kt
>     ProgramCounter.kt
>   src/test/kotlin/sap1/
>     ClockTest.kt
>     ProgramCounterTest.kt
> ```
>
> 실행:
> ```
> ./gradlew :chapter-03:test
> ./gradlew :chapter-03:run
> ```
>
> 테스트는 총 11개(클록 4 + PC 6 + 통합 1)다. 모두 초록불이 떨어지면 다음 챕터로 넘어가도 좋다.

## 마무리 — 16바이트의 우주에 발을 디뎠다

지금까지 한 일을 다시 정리해보자.

1. SAP-1의 명세를 한 표로 머릿속에 넣었다 — 8비트, 4비트 주소, 16바이트, 명령어 5개
2. 데이터패스 지도와 T-state 6단계의 의미를 봤다
3. **우리만의 합성 datasheet**라는 약속을 받아들였다 — 한 페이지짜리 명세를 매 챕터의 닻으로 삼는다
4. Kotlin 모델링의 큰 그림을 정했다 — 레지스터=클래스, 버스=함수 인자, 명령어=sealed class, 메모리=`IntArray`(잠정)
5. 첫 두 모듈을 짰다 — 클록과 PC, 테스트 11개와 함께

작아 보이지만, **여기서부터 SAP-1의 모든 코드가 같은 결을 갖게 된다**. 다음 챕터에서 짤 레지스터와 ALU도, 6장에서 짤 컨트롤러도, 7장에서 짤 어셈블러도 이 결을 따른다. 패턴 결정 다섯 줄은 14장 끝까지 우리를 끌고 갈 척추다. 첫 모듈에 11개씩이나 테스트를 붙이는 것이 사치처럼 보일 수 있겠지만, 다음 챕터에서 ALU가 들어와 모듈이 다섯 개로 늘어날 때 그 테스트들이 정말로 우리를 살린다. **테스트는 안전망이자 명세 그 자체**라는 점을 기억해두자.

4장에서는 본격적으로 **레지스터 A·B와 ALU**를 짠다. 그리고 거기서 우리는 한 가지 결정을 정면으로 마주하게 된다. **Java의 signed byte와 Kotlin의 UByte, 그리고 `Int` + 마스킹 중 무엇으로 살아갈 것인가?** 이 책 전체의 비트 표현 정책이 4장에서 결정된다. 동시에 두 8비트 수를 더한다는 것이 회로 차원에서 무슨 일을 의미하는지, 2의 보수가 왜 그토록 우아한지를 직접 손으로 짚어본다. 16바이트의 우주에서 첫 산술이 일어나는 챕터다. 잠깐 쉬고, 함께 가보자.
