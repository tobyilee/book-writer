# 1장 — 컴퓨터는 왜 이런 모습인가

> **핵심 한 줄:** von Neumann 골격의 정당화 — 명령어와 데이터가 같은 메모리에 산다는 한 줄이 오늘날 모든 컴퓨터의 출발점이다.

---

## 이 장이 던지는 질문

`./gradlew build`를 입력하는 순간, JVM이 뜨고, CPU가 명령어를 하나씩 꺼내 실행한다. 그런데 — 그 CPU는 왜 그런 식으로 동작할까? 왜 코드와 데이터가 같은 메모리에 섞여 있을까? 왜 8비트, 16비트, 32비트, 64비트라는 단위로 자라 왔을까?

이 질문들에 대한 답이 von Neumann 아키텍처다. 1945년 한 편의 보고서가 이후 80년 동안 만들어진 거의 모든 컴퓨터의 골격을 정했다. 그 골격을 이해하는 것이 이 책 전체의 출발선이다.

---

## 코드 없음

이 장은 코드가 없다. von Neumann 모델이 어디서 왔는지, 왜 Harvard 모델 대신 von Neumann을 택했는지, fetch-decode-execute 사이클이 무엇인지, 왜 8비트부터 시작하는지 — 이 네 가지 개념의 토대를 먼저 쌓는다. 손이 아직 키보드에 닿지 않는 유일한 챕터다.

---

## 학습 지도 — 5부 15장 한눈에

| 부 | 장 | 제목 | 핵심 |
|---|---|---|---|
| **1부** | 1 | 컴퓨터는 왜 이런 모습인가 | 골격 이해 (이 장) |
| | 2 | 30줄짜리 미니 CPU | Kotlin 첫 코드 |
| | 3 | SAP-1 — 16바이트의 우주 | 5개 명령어 CPU |
| | 4 | 비트와 바이트, 그리고 Kotlin의 선택 | 정수 표현 |
| | 5 | ALU — 덧셈기 하나로 시작한다 | 산술 연산 회로 |
| **2부** | 6 | 어셈블러 — 사람 글이 기계어가 되는 과정 | 2-pass 어셈블러 |
| | 7 | SAP-2 — 64K로 폭증 | 39개 명령어 |
| | 8 | 조건 분기와 반복 | BEQ·BNE·DJNZ |
| | 9 | 스택, 함수 호출, I/O | CALL·RET·IN·OUT |
| **3부** | 10 | 마이크로코드와 제어 유닛 | 컨트롤러를 데이터로 |
| | 11 | 8080·6502·Z80·8086 — 박물관 한 바퀴 | 4개 ISA 비교 |
| **4부** | 12 | RISC의 약속 — 1980년대의 격렬한 논쟁 | RISC vs CISC |
| | 13 | 합성 8비트 RISC ISA 설계 | 우리만의 ISA |
| | 14 | cycle-accurate 리팩토링 | T-state까지 |
| **5부** | 15 | 여기서 어디로 — 컴퓨터 전체로 가는 다리 | 다음 12개월 |

---

## 핵심 개념 요약

**von Neumann 아키텍처의 본질은 딱 한 줄이다.**

> "A uniform memory containing both numbers (data) and orders (instructions)."  
> — von Neumann, *First Draft of a Report on the EDVAC*, 1945

명령어를 숫자로 적고, 그 숫자를 데이터와 같은 메모리 칸에 둔다. 이것이 80년치 컴퓨터 산업의 출발선이다. ENIAC은 새 프로그램을 돌리려면 며칠 동안 케이블을 다시 꽂아야 했다. von Neumann의 한 줄 이후, 메모리의 비트만 바꾸면 된다.

**왜 Harvard 아키텍처를 택하지 않았나?** nand2tetris의 Hack CPU가 Harvard를 택한 것은 단순화를 위해서다. 우리는 반대다. 명령어와 데이터가 같은 비트로 표현된다는 사실 — 그래서 어셈블러가 다른 프로그램을 만들어낼 수 있다는 사실이 컴파일러와 인터프리터로 가는 가장 자연스러운 다리이기 때문이다.

**fetch-decode-execute의 세 박자.** 컴퓨터의 전원이 켜져 있는 동안 이 사이클은 멈추지 않는다. PC → MAR → 메모리 → MDR → IR → PC++. 이 화살표들이 이 책에서 짤 모든 SAP CPU의 뼈대다.

**왜 8비트인가?** 단순함이 가르치는 힘 때문이다. SAP-1은 명령어 5개, 메모리 16바이트. 그 좁은 우주에서 CPU의 모든 화살표가 손 안에 들어온다. 그리고 8비트는 컴퓨터 아키텍처 어휘의 정립기 — 1974년 8080부터 1978년 8086까지, 오늘날 우리가 쓰는 거의 모든 개념이 그 시대에 손으로 굳어졌다.

---

## 다음 챕터 미리 보기 — 2장: 30줄짜리 미니 CPU

이 장을 다 읽으면, 2장에서 만날 Kotlin 미니 CPU의 골격이 머릿속에 미리 그려진다. fetch-decode-execute의 세 박자를 Kotlin으로 직접 옮기면 이런 모습이다.

```kotlin
class MiniCpu(val memory: IntArray) {
    var pc: Int = 0
    var a: Int = 0           // 누산기
    var halted: Boolean = false

    fun step() {
        val opcode = fetch()      // 1. 꺼낸다
        decode(opcode)            // 2. 풀고 → 수행한다
    }

    private fun fetch(): Int {
        val byte = memory[pc] and 0xFF
        pc = (pc + 1) and 0xFF   // PC를 한 칸 올린다
        return byte
    }

    private fun decode(opcode: Int) {
        when (opcode and 0xF0) {
            0x10 -> a = (a + (opcode and 0x0F)) and 0xFF   // ADD
            0xF0 -> halted = true                           // HLT
            else -> error("unknown opcode: $opcode")
        }
    }
}
```

낯선 코드가 한 줄도 없다. `IntArray`로 메모리를 흉내내고, `var`로 레지스터를 만들고, `when`으로 명령어를 분기한다. 2장에서 이 30줄을 처음부터 끝까지 손으로 짜고 테스트로 검증한다. 첫 번째 작은 성공이 거기 있다.
