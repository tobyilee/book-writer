# 부록 B. JLS 인용 인덱스

본문에서 우리는 JLS(Java Language Specification)와 JVM 스펙을 곳곳에서 인용했다. 어떤 자리는 한 페이지짜리 박스를 통째로 할애했고, 어떤 자리는 본문 한 줄에 §번호만 슬쩍 끼워두었다. 이 부록은 그 인용을 *양방향으로* 찾을 수 있게 한 인덱스다.

두 표가 있다. 첫 번째 표는 *챕터에서 JLS로* — "내가 11장에서 본 records 정의는 JLS의 어디인가?". 두 번째 표는 *JLS에서 챕터로* — "JLS §14.30을 봤는데, 이 책에서 어디에 나오는가?". 두 방향 모두 자주 쓰인다.

인용은 가급적 *원문 + 한국어 번역*을 짝지어 본문에 실었다. JLS는 영문이 정본이지만, 한국 독자를 위해 의미를 풀어 번역하고 그 옆에 원문을 박스로 같이 두었다. 박스를 *2~4단 구성*(원문 / 번역 / 의미 해설 / 본문과의 연결)으로 정리한 것도 이 때문이다.

기준 JLS 버전은 *JLS 21(JSR 396)*이고, 25 표준화 항목은 *JLS 25*(2025-09-16 GA 시점)를 참조했다. Memory Model 부분은 JSR-133 원문도 함께 인용했다.

---

## B.1 표 1 — 챕터 → JLS

본문 챕터 순서로 정리했다. 각 행의 *주제* 열은 해당 인용이 답하려는 질문을, *인용 위치* 열은 본문 안에서 그 박스가 어디 들어갔는지를 알려준다.

| 챕터 | JLS § | 정식 명칭 | 주제 | 인용 위치 |
|---|---|---|---|---|
| 3장 | §15.27 | Lambda Expressions | "effectively final"의 정확한 정의 | 본문 박스 1쪽 |
| 3장 | §15.27.2 | Lambda Body | 람다 본체와 enclosing 컨텍스트의 관계 | 본문 박스 0.5쪽 |
| 5장 | (패키지 문서) | `java.util.stream` | Stream의 *non-interference* 조건 | 본문 박스 1쪽 |
| 6장 | (패키지 문서) | `java.util.stream.Gatherer` | Gatherer의 contract — `integrator`·`finisher`·`combiner` | 본문 박스 1쪽 |
| 7장 | (Javadoc) | `java.util.Optional` | "value-based class" — `==` 비교 금지 근거 | 본문 박스 0.5쪽 |
| 8A장 | §17.4 | Memory Model | happens-before 관계의 정의 | 본문 박스 2쪽 (JSR-133 원문 포함) |
| 8A장 | §17.5 | final Field Semantics | `final` 필드의 publication 보장 | 본문 박스 1쪽 |
| 8A장 | (JSR-133 원문) | JSR-133 Java Memory Model | happens-before·sequential consistency·OOTA 차단 | 본문 박스 2쪽 |
| 9장 | §7.7 | Module Declarations | `module-info.java`의 5개 키워드 정의 | 본문 박스 1쪽 |
| 9장 | §7.7.1 | Dependences | `requires` / `requires transitive` / `requires static` | 본문 박스 0.5쪽 |
| 10장 | §14.4 | Local Variable Declaration Statements (LVTI) | `var`의 추론 규칙 | 본문 박스 1쪽 |
| 10장 | §14.11 | The `switch` Statement | switch statement (fall-through 형식) | 본문 박스 1쪽 |
| 10장 | §15.28 | Switch Expressions | `case L ->`·`yield`의 정의 | 본문 박스 1쪽 |
| 10장 | §3.10.6 | Text Blocks | incidental whitespace 알고리즘 — *왜 들여쓰기가 자동 제거되는가* | 본문 박스 1쪽 (예제 포함) |
| 11장 | §8.10 | Record Classes | record의 정의·자동 생성 멤버 | 본문 박스 1쪽 |
| 11장 | §8.10.4 | Record Constructors | canonical constructor·compact constructor의 정의 | 본문 박스 0.5쪽 |
| 12장 | §8.1.1.2 | `sealed` Classes | `sealed`·`permits`·`non-sealed`·`final`의 정의 | 본문 박스 1쪽 |
| 13장 | §14.30 | Patterns | pattern의 정의 — type pattern·record pattern | 본문 박스 1쪽 |
| 13장 | §14.30.3 | Exhaustiveness of switch | exhaustiveness check의 정의 — sealed와의 관계 | 본문 박스 1쪽 |
| 14장 | §17.1 | Threads | Thread의 정의 (virtual / platform) | 본문 박스 0.5쪽 |
| 14장 | (JEP 444 원문) | Virtual Threads | virtual thread의 의도·M:N 스케줄링 | 본문 박스 1쪽 |
| 16장 | (JEP 506 원문) | Scoped Values | ScopedValue의 contract — bounded·immutable | 본문 박스 1쪽 |
| 16장 | (JEP 505 원문) | Structured Concurrency | `StructuredTaskScope`의 success/failure semantics | 본문 박스 0.5쪽 |
| 17장 | §12.6 | Finalization of Class Instances | finalize의 deprecation — Cleaner 권장 | 본문 박스 0.5쪽 |
| 18장 | (Javadoc) | `java.lang.foreign.MemorySegment` | MemorySegment의 lifetime 규칙 | 본문 박스 0.5쪽 |
| 22장 | (Project Valhalla draft) | Value Classes | value class의 의도·미래 | 본문 박스 0.5쪽 (disclaimer 포함) |

3장의 §15.27 박스는 책 전체에서 가장 자주 *되돌아보게 되는* 인용이다. "effectively final"이 람다·local class·익명 inner class 모두에 적용되는 *하나의 정의*임을 거기서 못박는다.

8A장의 §17.4 박스는 책에서 가장 길게 인용한 부분이다. JSR-133 원문까지 함께 실은 이유는 — JLS 본문은 happens-before의 *정의*만 다루는데, *왜 그렇게 정의했는가*는 JSR-133 원문이 답하기 때문이다.

---

## B.2 표 2 — JLS § → 챕터

JLS 섹션 번호 순으로 정렬했다. JLS를 보다가 *이 부분이 책의 어디서 다뤄졌나*를 찾을 때 쓰자.

| JLS § | 정식 명칭 | 챕터 | 비고 |
|---|---|---|---|
| §3.10.6 | Text Blocks (incidental whitespace) | 10장 | 알고리즘 박스 |
| §7.7 | Module Declarations | 9장 | 5개 키워드 |
| §7.7.1 | Dependences | 9장 | `requires` 변형 |
| §8.1.1.2 | `sealed` Classes | 12장 | permits·non-sealed·final |
| §8.10 | Record Classes | 11장 | record 정의 |
| §8.10.4 | Record Constructors | 11장 | canonical·compact |
| §12.6 | Finalization of Class Instances | 17장 | finalize deprecation |
| §14.4 | Local Variable Declaration (LVTI) | 10장 | `var` 추론 |
| §14.11 | The `switch` Statement | 10장 | statement form |
| §14.30 | Patterns | 13장 | pattern 정의 |
| §14.30.3 | Exhaustiveness of switch | 13장 | sealed exhaustive |
| §15.27 | Lambda Expressions | 3장 | effectively final |
| §15.27.2 | Lambda Body | 3장 | enclosing context |
| §15.28 | Switch Expressions | 10장 | `case L ->`·`yield` |
| §17.1 | Threads | 14장 | virtual / platform |
| §17.4 | Memory Model | 8A장 | happens-before |
| §17.5 | `final` Field Semantics | 8A장 | publication 보장 |
| (JSR-133) | Java Memory Model | 8A장 | happens-before 정의문 |
| (JEP 444) | Virtual Threads | 14장 | M:N 스케줄링 |
| (JEP 506) | Scoped Values | 16장 | bounded·immutable |
| (JEP 505) | Structured Concurrency | 16장 | StructuredTaskScope |
| (`java.util.stream`) | Stream non-interference | 5장 | 패키지 문서 |
| (`Gatherer`) | Gatherer contract | 6장 | integrator·finisher |
| (`Optional`) | value-based class | 7장 | `==` 금지 |
| (`MemorySegment`) | lifetime 규칙 | 18장 | FFM |
| (Valhalla draft) | Value Classes | 22장 | disclaimer 박스 |

§17.4와 §17.5가 같은 8A장에 모이는 게 자연스럽다. 메모리 모델 한 단원에서 *happens-before*와 *`final` field publication*은 같은 동전의 양면이기 때문이다.

§14.30·§14.30.3 둘이 13장에 함께 묶이는 것도 마찬가지 — 패턴 매칭의 *정의*(§14.30)와 *그 정당성 보장*(§14.30.3, exhaustiveness)이 한 호흡에 들어간다.

---

## B.3 인용 박스의 구조 — *원문 / 번역 / 의미 / 연결*

본문에 들어간 모든 JLS 인용 박스는 동일한 4단 구성을 따랐다. 다시 읽거나 인용을 직접 참조할 때 도움이 되도록 그 구조를 적어둔다.

```
┌─────────────────────────────────────┐
│ JLS §X.Y (정식 명칭)                  │
├─────────────────────────────────────┤
│ [원문 — 영문]                         │
│ A record class is a special kind... │
├─────────────────────────────────────┤
│ [한국어 번역]                          │
│ record 클래스는 ... 의 특별한 종류다.    │
├─────────────────────────────────────┤
│ [의미 해설]                            │
│ "shallowly immutable"이 왜 중요한가...  │
├─────────────────────────────────────┤
│ [본 챕터 본문과의 연결]                  │
│ 우리가 위 예제에서 본 Point는 ...        │
└─────────────────────────────────────┘
```

- *원문*은 가급적 한 문장 또는 한 문단으로 끊는다. 너무 길면 문맥이 흐트러진다.
- *번역*은 직역보다 *의미가 통하는 번역*을 선호한다. 자바 용어는 그대로 두되, 일반어는 한국어로.
- *의미 해설*은 spec의 표현이 *왜 그렇게* 됐는지를 한 문단으로 푼다.
- *연결*은 본문의 그 자리에서 이 박스를 *왜 펼쳤는가*를 한 줄로 적는다.

이 4단 구성이 책 전체에서 일관되니, 박스의 모양만 봐도 "지금 spec을 읽고 있구나"가 바로 보일 것이다.

---

## B.4 spec 원문을 직접 읽고 싶다면

OpenJDK 공식 사이트에서 JLS 25 정본을 PDF/HTML로 받을 수 있다. URL은 시점에 따라 바뀌니 *jls 25 pdf*로 검색하는 편이 빠르다. 책에서 쓴 §번호는 JLS 21·25 모두 거의 같지만, 25에서 새로 추가된 항목(예: `void main()`, sealed 관련 보강)은 25 정본을 참조해야 정확하다.

JSR-133(Java Memory Model)은 별도 문서다. *Java Memory Model and Thread Specification*이라는 제목의 PDF가 정본이고, Doug Lea의 [JSR-133 cookbook](https://gee.cs.oswego.edu/dl/jmm/cookbook.html)이 더 읽기 좋은 해설이다. 8A장의 후반부는 이 둘을 함께 읽기를 권한다.

JEP 원문은 `openjdk.org/jeps/{번호}` 한 줄로 충분하다. 부록 A의 JEP 일람과 함께 보면 좋다.

---

## B.5 인용 누락에 대한 양해

이 책은 JLS의 *모든* 인용을 다루지 않는다. 자바의 핵심 변화 — 11년의 굵직한 변화에 한정해 인용을 골랐다. 예를 들어 generics(§8.4), exceptions(§11), annotations(§9.6) 같은 *이미 알고 있다고 전제한 영역*은 인용을 생략했다.

또 한 가지 — 책에서 spec을 *부분적으로 단순화한* 자리도 있다. 정확한 spec 문장은 종종 너무 정밀해서 한 권의 책에서 다 풀기 어렵다. 본문 박스에서 "단순화"라는 말이 등장한다면, 원문은 더 정밀하고 더 까다롭다는 뜻이다. 정확한 동작이 의심스러우면 늘 *원문 정본*으로 돌아가자.

마지막으로 — *spec은 진화한다*. 25 시점의 spec이 26·27에서 어떻게 바뀔지는 아무도 정확히 모른다. Project Valhalla·Amber·Babylon·Leyden이 spec에 닿을 때, 이 인덱스도 함께 갱신될 것이다. 22장의 disclaimer 박스를 한 번 더 짚어두자.
