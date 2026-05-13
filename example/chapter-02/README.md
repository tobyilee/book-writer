# 2장 — fetch-decode-execute를 Kotlin 30줄로

## 핵심 질문

CPU가 "동작한다"는 말은 정확히 무엇을 뜻하는가? 박스와 화살표로 가득한 교과서 그림을 보고 고개를 끄덕였는데, 실제로 손에 잡히는 감각이 있었는가? 그 감각이 없었다면, 30줄짜리 Kotlin 코드가 답이다.

## 무엇을 짓는가

**MiniCpu** — fetch-decode-execute 사이클의 뼈대만 추린 미니 CPU.

| 항목 | 내용 |
|------|------|
| 메모리 | 가변 크기 `IntArray` (테스트마다 다름) |
| 레지스터 | 누산기(accumulator) + 프로그램 카운터(PC) |
| 명령어 | 2개 — `ADD addr`(0x01), `HLT`(0x10) |
| 인코딩 | 명령어 1바이트 + 주소 1바이트(ADD만) |

명령어가 두 개뿐이지만, 골격은 명령어가 200개인 CPU와 같다. `while` 루프 안에서 fetch → decode → execute가 한 박자씩 돈다. 그 박자를 손으로 직접 짜보는 것이 이 챕터의 목표다.

## 실행

```bash
./gradlew :chapter-02:run
```

출력:

```
Accumulator = 42
```

`17 + 25 = 42`. 우리가 짠 CPU가 메모리에서 두 명령어를 꺼내 누산기에 더한 결과다. 폰 노이만 사이클이 우리 코드 위에서 한 차례 뛴 것이다.

## 테스트

```bash
./gradlew :chapter-02:test
```

8개 테스트가 모두 통과한다:

- HLT 단일 명령으로 즉시 정지
- ADD + HLT 시 누산기에 합산
- 두 번의 ADD 누적
- PC가 메모리 끝을 넘으면 즉시 정지
- HLT 만나기 전까지 fetch-decode-execute 반복
- 초기 상태에서 PC=0, accumulator=0
- 실행 후 PC가 HLT 다음 위치로 이동
- ADD 후 PC는 2칸 전진, HLT 후 1칸 더

## 이번 챕터의 GitHub 산출물

```
chapter-02/
  build.gradle.kts
  src/main/kotlin/sap/ch02/MiniCpu.kt    (CPU 본체 + main, ~40줄)
  src/test/kotlin/sap/ch02/MiniCpuTest.kt (8개 테스트)

실행:   ./gradlew :chapter-02:run    → Accumulator = 42
테스트: ./gradlew :chapter-02:test   → 8/8 passed
```

## 다음 챕터로

이 30줄짜리 CPU는 SAP-1의 출발점이다. 3장에서는 메모리를 4바이트에서 16바이트로 넓히고, 명령어를 5개로 늘리고, 클록과 프로그램 카운터를 TDD로 짜본다. 같은 골격 위에 살이 한 겹씩 붙는다 — `while` 루프는 그대로이고, `when` 분기만 길어진다.
