# 13장. Pattern Matching — ADT를 풀어내는 도구

PR 리뷰에서 한 컨트롤러를 받았다고 해보자. 새벽 두 시에 동료가 보낸 메시지에 "이상하게 동작합니다, 봐주세요"라고만 적혀 있다. 코드를 펼치니 이런 모양이다.

```java
public ResponseEntity<?> handle(Object response) {
    if (response instanceof SuccessResponse) {
        SuccessResponse s = (SuccessResponse) response;
        if (s.getPayload() instanceof OrderCreated) {
            OrderCreated created = (OrderCreated) s.getPayload();
            if (created.getCustomer() instanceof RegisteredCustomer) {
                RegisteredCustomer rc = (RegisteredCustomer) created.getCustomer();
                if (rc.getTier() instanceof PremiumTier) {
                    PremiumTier pt = (PremiumTier) rc.getTier();
                    return premiumHandler(pt, created);
                } else if (rc.getTier() instanceof StandardTier) {
                    // ...
                }
            } else if (created.getCustomer() instanceof GuestCustomer) {
                // ...
            }
        } else if (s.getPayload() instanceof PaymentApproved) {
            // ...
        }
    } else if (response instanceof ErrorResponse) {
        // ...
    }
    return ResponseEntity.badRequest().build();
}
```

캐스트 사다리가 9단까지 늘어났다. 같은 변수의 같은 타입을 *확인*하고 *캐스팅*하는 두 줄이 9번 반복된다. 한 줄 한 줄이 *끔찍한 일*은 아니지만, 한 화면에 모인 모습을 보면 그 누적이 *끔찍하다*. 사다리의 어느 한 칸이라도 잘못 적혀 있으면 `ClassCastException`이 production에서 새벽에 깨운다. 들여쓰기가 깊어지면서 가독성도 같이 떨어진다.

이쯤 되면 한 번쯤 묻게 된다. **캐스트 사다리, 이게 정말 최선이었을까?** 자바 이외의 거의 모든 현대 언어가 이 자리를 *pattern matching*으로 풀고 있다. Scala의 `match`, Kotlin의 `when`, Rust의 `match`, F#의 `match`, Swift의 `switch`. 같은 도구가 자바에 마침내 왔다 — Java 16의 `instanceof` 패턴(JEP 394)에서 시작해, Java 21의 switch 패턴(JEP 441)과 record 패턴(JEP 440)으로 완성되고, Java 22의 unnamed pattern(JEP 456)으로 다듬어진 그 도구.

이 장이 *Modern Java Bible의 미학적 클라이맥스*다. 앞 두 장에서 모은 records와 sealed가 이 장의 pattern matching과 만나면, Brian Goetz가 *Data-Oriented Programming in Java*라고 부른 한 묶음이 완성된다. *Records + Sealed + Pattern = 삼위일체*. 표현식 평가기, HTTP Result, Workflow 상태기계 — 세 본격 예제로 그 삼위일체가 현실 도메인에서 어떻게 풀려 들어오는지를 함께 살펴보자. 그리고 마지막에는 다음 장(14장 Virtual Threads)으로 가는 다리를 놓자. *도메인을 ADT로 모델링했으니, 그 도메인 위에서 동시성을 다시 생각해보자*는 다리다.

## preview의 8년 — 연표로 한 번에

자바의 pattern matching은 *6년에 걸쳐 7단계의 preview*를 거쳐 완성됐다. 그 흐름을 본문에서 한 단계씩 따라가는 일은 *지긋지긋*하다. 한 박스로 압축하자.

> **연표 박스 — Pattern Matching의 8년**
>
> - **JEP 305 (Java 14, 2020)** — pattern matching for `instanceof` 1차 preview. 자바 사상 처음으로 패턴이라는 어휘가 들어왔다.
> - **JEP 394 (Java 16, 2021)** — `instanceof` 패턴 표준. `if (x instanceof Point p)`의 그 형태.
> - **JEP 406 (Java 17, 2021)** — switch에 패턴이 1차 preview로 등장.
> - **JEP 420 (Java 18, 2022)** — switch 패턴 2차 preview. guard가 `&&`에서 `when`으로 바뀌는 굵직한 디자인 결정이 이 단계에서 내려진다.
> - **JEP 427 (Java 19, 2022)** — 3차. `case null` 처리, dominance 검사가 정착.
> - **JEP 432, 440 (Java 20, 2023)** — record pattern preview. `case Point(int x, int y)`라는 분해 문법이 등장.
> - **JEP 441 (Java 21, 2023)** — *switch 패턴 표준*. record pattern도 함께 표준화(JEP 440).
> - **JEP 456 (Java 22, 2024)** — *unnamed pattern* `_` 표준. 쓰지 않는 컴포넌트를 명시적으로 무시.

8년이다. 자바답다. records와 sealed가 2~3년에 표준에 도달한 데 비해, pattern matching은 *언어의 분기 의미론을 새로 짜는 일*이라 신중함이 곱절로 들어갔다. `case`의 의미가 fall-through 기반에서 arrow 기반으로, 그리고 *데이터 분해*까지 받아들이는 자리로 *바뀐 것*이다. 자바의 신중함이 가장 보수적으로 작동한 자리다.

본문에서는 *21 표준과 22 unnamed*에 집중하자. 그 둘이 우리가 매일 적을 코드의 99%다.

## 가장 작은 패턴 — `instanceof` 분해

도입부 캐스트 사다리의 한 칸을 떼어내자.

```java
if (response instanceof SuccessResponse) {
    SuccessResponse s = (SuccessResponse) response;
    // s 사용
}
```

`instanceof`로 확인하고, 같은 줄을 한 번 더 적어 캐스팅한다. 같은 의도를 두 번 적는다. *번거롭다*. 어디서 본 듯한 *지루함*이다.

Java 16의 JEP 394로 이 두 줄이 한 줄이 됐다.

```java
if (response instanceof SuccessResponse s) {
    // s 사용 — 이미 SuccessResponse 타입
}
```

`SuccessResponse s`. 이것이 *type pattern*의 가장 작은 형태다. 매칭이 성공하면 `s`라는 *binding 변수*가 자동으로 생기고, 그 변수의 타입은 `SuccessResponse`다. 캐스팅이 필요 없다. `if` 블록 안에서 `s`를 *그대로 쓰면 된다*.

흥미로운 자리가 한 군데 있다. `s`의 스코프는 *매칭이 성공하는 분기*에 자동으로 묶인다.

```java
if (!(response instanceof SuccessResponse s)) {
    return ResponseEntity.badRequest().build();
}
// 여기에서 s가 살아 있다 — 실패 분기에서 일찍 return했기 때문에
return ResponseEntity.ok(s.getPayload());
```

*flow scoping*이라 부르는 이 동작이다. early return으로 실패 분기를 끊어내면, 나머지 본문에서 `s`가 *살아남는다*. guard clause 스타일의 코드에 자연스럽다. 컴파일러가 *변수의 정의 가능 위치*를 흐름 분석으로 추적하기 때문에 가능한 일이다. 자바 14의 effectively final 추적과 같은 결의 일이 패턴에서 한 번 더 일어난 셈이다.

## switch가 패턴을 만나면 — Java 21의 본격

`instanceof` 패턴이 길어지면 결국 *분기의 나열*이 된다. 도입부 사다리가 정확히 그것이다. 그래서 분기의 나열은 switch가 가장 잘 다룬다. Java 21에 들어서면서 switch가 *type을 case 라벨로* 받는다.

같은 컨트롤러를 sealed `Response`와 switch 패턴으로 다시 적자.

```java
public sealed interface Response {
    record SuccessResponse(Payload payload) implements Response {}
    record ErrorResponse(String code, String message) implements Response {}
}

public ResponseEntity<?> handle(Response response) {
    return switch (response) {
        case SuccessResponse s -> ResponseEntity.ok(s.payload());
        case ErrorResponse e   -> ResponseEntity.status(400).body(e);
    };
}
```

9단 사다리가 4줄로 무너졌다. 그리고 *더 중요한 일이 일어났다* — 컴파일러가 이 switch의 *완전성을 검증*한다. `Response`가 sealed로 `SuccessResponse`와 `ErrorResponse` 둘만 허용하므로, 두 case가 모든 가능성을 덮는다. *default가 필요 없다*. 새 sub-type — 예를 들어 `PartialResponse` — 가 sealed에 추가되는 순간 이 switch는 컴파일 에러로 갱신을 요구한다.

화살표 `->`의 의미를 짚자. 전통적인 `case ... :` + `break;`의 fall-through 모델이 아니다. 화살표 case는 *해당 분기만 실행*한다. switch가 expression일 때(위처럼 값을 반환할 때) `yield`나 명시적 return으로 값을 내보낸다. fall-through의 그 묵은 *찜찜함*이 화살표 한 번으로 정리됐다.

## guard — `when`으로 조건을 잇는다

타입 매칭에 더해, 한 가지 추가 조건이 필요한 자리가 자주 있다. 예를 들어 "성공 응답이되 payload가 5MB를 넘으면 다른 처리"라는 식. 이걸 case 안에서 `if`로 다시 풀면 *흐름이 한 번 꺾인다*. switch 패턴은 그 자리를 `when`이라는 키워드로 받는다.

```java
return switch (response) {
    case SuccessResponse s when s.payload().sizeBytes() > 5_000_000
        -> ResponseEntity.status(413).body("Payload too large");
    case SuccessResponse s -> ResponseEntity.ok(s.payload());
    case ErrorResponse e   -> ResponseEntity.status(400).body(e);
};
```

`when` 절에는 *binding 변수를 자유롭게 활용한 boolean 표현식*이 들어간다. guard라 부른다. guard가 있는 case는 같은 타입의 *guard 없는 case*보다 *위에* 와야 한다 — 위에서부터 첫 매칭으로 분기하므로. 컴파일러가 이 순서까지 챙겨준다. *dominance check*라 부른다. 만약 guard 없는 case가 먼저 오면 그 아래의 guard case가 *영원히 도달 불가능*해진다는 에러를 컴파일러가 일으킨다.

설계 결정에 한 가지 흥미로운 점이 있다. 자바의 guard는 `when`이지 `&&`가 아니다. 첫 preview(JEP 406)에서는 `&&`였다. 그러나 산업 피드백을 받으며 `when`으로 바뀌었다(JEP 420). `&&`이면 일반 boolean과 *시각적으로 구별되지 않는다*는 비판이 있었다. `when`이라는 *영어 단어*가 들어가면서 "여기서부터는 guard"라는 의미가 *읽는 사람에게 명시적*이 된다. 작은 단어 하나의 결정이지만, 8년 preview의 신중함이 만든 결정이다.

> **JLS 인용 박스 — §14.30 Patterns**
>
> *원문* — "A pattern describes a structure that a value may match. Pattern matching is the process of testing whether a value matches a pattern, and if so, deconstructing it."
>
> *번역* — "패턴은 어떤 값이 매칭될 수 있는 *구조*를 기술한다. 패턴 매칭이란 *값이 그 패턴에 매칭되는지를 검사하고, 매칭되면 그 값을 분해하는* 과정이다."
>
> *해설* — 핵심 단어가 두 개다. *structure*, 그리고 *deconstructing*. 패턴은 단순한 타입 검사가 아니라 *값의 구조를 기술하는 어휘*다. 그 구조를 *분해*해서 컴포넌트에 이름을 붙이는 일이 패턴 매칭의 본질이다. 이 정의 한 줄이 자바를 *Java 8 시절의 캐스트 사다리 언어*에서 *함수형 분해를 아는 언어*로 옮긴 분기점이다.
>
> *본문 연결* — 다음 절에서 다룰 record 패턴이 이 *deconstructing*의 정확한 사례다. record header에 적힌 컴포넌트가 곧 *분해 가능한 구조*이고, 패턴 매칭은 그 구조를 *역방향으로 푸는* 어휘다.

## record pattern — 컴포넌트를 한 줄에 풀어내다

지금까지의 `case SuccessResponse s`는 *타입만 매칭*하고 컴포넌트는 분해하지 않았다. record pattern은 그 마지막 한 발을 더 간다.

```java
return switch (response) {
    case SuccessResponse(Payload p) -> ResponseEntity.ok(p);
    case ErrorResponse(String code, String message) -> ResponseEntity.status(400).body(code + ": " + message);
};
```

`SuccessResponse(Payload p)`. record header를 *그대로 패턴*으로 적었다. 매칭이 성공하면 `p`라는 binding이 컴포넌트의 값으로 채워진다. `ErrorResponse(String code, String message)`는 *두 컴포넌트를 한 번에* 분해했다. 분해된 변수가 case 본문에서 바로 쓰인다.

`var`로 받는 줄임도 있다.

```java
case ErrorResponse(var code, var message) -> ...
```

코드의 의도에 따라 타입을 명시할지, `var`로 줄일지 선택하면 된다. 컴포넌트가 한두 개일 때는 `var`가 자연스럽고, 컴포넌트가 많거나 의미가 모호할 때는 명시적 타입을 권한다.

## 중첩 분해 — 도메인이 깊어질 때

도메인 모델이 자라면 record가 다른 record를 컴포넌트로 가진다. 그 깊이까지 패턴이 *재귀적으로* 따라간다.

```java
public record Point(int x, int y) {}
public record Line(Point start, Point end) {}

double slope(Line line) {
    return switch (line) {
        case Line(Point(int x1, int y1), Point(int x2, int y2))
            when x1 != x2 -> (y2 - y1) / (double)(x2 - x1);
        case Line(Point p1, Point p2) -> Double.POSITIVE_INFINITY;  // 수직선
    };
}
```

`Line(Point(int x1, int y1), Point(int x2, int y2))`. record 안의 record를 한 번에 분해했다. 컴포넌트 네 개가 한 줄에 펼쳐진다. 도입부의 캐스트 사다리 9단이 *분해 한 줄*이 됐다.

이 자리에서 자바가 *Scala·Rust·Haskell과 같은 어휘*를 받아들였다는 사실을 다시 확인하자. 함수형 언어들은 30년 동안 데이터 구조를 *역방향으로 분해*하는 도구로 패턴을 다듬어왔다. 자바가 그 도구를 자기 어휘로 받았다. records가 product type을 *만드는* 어휘라면, record pattern은 그 product를 *분해하는* 어휘다. 둘은 *짝패*다.

## unnamed pattern `_` — 무시할 권리 (Java 22)

깊은 분해를 적다 보면 한 가지 *작은 불편*에 부딪힌다. 신경 쓰지 않는 컴포넌트까지 *이름을 지어야* 한다는 점이다. 위 `slope` 함수의 *수직선 분기*에서 `Line(Point p1, Point p2)`라고 적었는데, `p1`과 `p2`를 본문에서 쓰지 않는다. 안 쓰는 이름 두 개가 *어색하게* 남아 있다.

Java 22의 JEP 456이 이 자리를 풀어준다. *unnamed pattern* `_`이다.

```java
double slope(Line line) {
    return switch (line) {
        case Line(Point(int x1, int y1), Point(int x2, int y2))
            when x1 != x2 -> (y2 - y1) / (double)(x2 - x1);
        case Line(Point _, Point _) -> Double.POSITIVE_INFINITY;
    };
}
```

`Point _`. "Point 타입이긴 한데, 그 내부 값에는 *관심이 없다*"는 명시적 선언이다. 이름이 사라지지 않는다 — 그 자리에 *익명*이라는 *명시적 표시*가 들어간다. *읽는 사람에게 의도가 더 분명해진다*. 안 쓸 변수에 어색한 이름을 지어 *찜찜하게* 남기던 일이 끝났다.

`_`는 *binding이 일어나지 않는다*. 같은 case 안에 `_`가 여러 개 나와도 충돌하지 않는다. 그 점이 *변수 이름*과 달라 정신적 부담이 적다.

## sealed + pattern = 완전성 (exhaustiveness)

여기까지 도구를 모았으니, sealed의 짝패 효과를 다시 짚자. switch가 *모든 가능성을 덮는지*를 컴파일러가 검사하는 그 기능 — **exhaustiveness**.

```java
sealed interface Shape permits Circle, Square, Triangle {}
record Circle(double radius) implements Shape {}
record Square(double side) implements Shape {}
record Triangle(double base, double height) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle(double r)      -> Math.PI * r * r;
        case Square(double s)      -> s * s;
        case Triangle(double b, double h) -> 0.5 * b * h;
    };
}
```

`default`가 없다. 그런데 컴파일러가 에러를 내지 않는다. `Shape`가 sealed로 세 sub-type을 *permits*하고, 위 switch가 셋을 모두 *case*로 받았으므로 *완전*하다. 컴파일러가 *그 사실을 안다*.

이제 누군가가 `Shape`에 `Hexagon`을 추가한다고 해보자. `permits` 목록에 `Hexagon`이 들어가는 순간, 위 `area` 함수의 switch가 *컴파일 에러*가 된다. "Hexagon이 빠졌다"고. 도메인이 자라는 자리를 *컴파일러가 우리 손에 쥐어준다*. enum + if 분기로는 결코 받을 수 없었던 *언어 차원의 안전망*이다.

JLS는 이 자리를 한 번 더 분명히 한다.

> **JLS 인용 박스 — §14.30.3 switch exhaustiveness**
>
> *원문* — "A `switch` block is exhaustive if it has no `default` clause and the set of patterns in its case labels covers all possible values of the selector expression."
>
> *번역* — "어떤 `switch` 블록이 `default` 절 없이도, case 라벨들의 패턴 집합이 *selector 표현식의 가능한 모든 값을 덮는다*면 그 switch는 *exhaustive*하다."
>
> *해설* — 단순한 syntactic 검사가 아니다. *type system 차원의 검사*다. sealed 계층의 `permits` 목록을 컴파일러가 들고, switch의 case 패턴 집합이 그 목록을 *모두 덮는지*를 검사한다. 덮으면 *default 없이도 통과*. 덮지 못하면 컴파일 에러. JLS의 이 한 문장이 *records + sealed + pattern*이라는 삼위일체의 *마지막 못*을 박는다.
>
> **synthetic default의 작은 비밀** — 한 가지 *내부 사정*이 있다. 컴파일러는 위와 같은 exhaustive switch를 바이트코드로 내릴 때, *synthetic default*를 자동으로 끼워 넣는다. 이유는 *separate compilation*. 클래스 A가 컴파일된 후, 라이브러리 B의 sealed 계층에 새 sub-type이 추가되고 *B만 재컴파일*되면, A의 switch가 그 새 sub-type을 받을 때 *런타임에 매칭에 실패*할 수 있다. 그 경우를 위해 `MatchException`을 던지는 default가 살짝 들어간다. 우리는 코드에서 보이지 않지만, 클래스 파일을 열어보면 거기 있다.

## 예제 1 — 표현식 평가기 (교과서적)

자, 도구를 모두 모았다. 이제 본격 예제 셋으로 들어가자. 첫 번째는 함수형 언어 교과서에 반드시 등장하는 그 예제 — *표현식 평가기*다.

`Num(3) + Mul(Add(Num(2), Num(4)), Num(5))` 같은 수식 트리를 만들어 평가하는 일이다. 자바 8 시절이면 `interface Expr` + 추상 클래스 + Visitor 패턴으로 60줄을 적었을 것이다. records + sealed + pattern으로는 이렇게 된다.

```java
public sealed interface Expr {
    record Num(int value) implements Expr {}
    record Add(Expr left, Expr right) implements Expr {}
    record Mul(Expr left, Expr right) implements Expr {}
}

public class Evaluator {
    public static int eval(Expr expr) {
        return switch (expr) {
            case Expr.Num(int v) -> v;
            case Expr.Add(Expr l, Expr r) -> eval(l) + eval(r);
            case Expr.Mul(Expr l, Expr r) -> eval(l) * eval(r);
        };
    }

    public static void main(String[] args) {
        Expr e = new Expr.Mul(
            new Expr.Add(new Expr.Num(2), new Expr.Num(4)),
            new Expr.Num(5)
        );
        System.out.println(eval(e));  // 30
    }
}
```

20줄 안쪽. 그러면서 컴파일러가 *세 가지 case가 Expr의 sub-type을 모두 덮는다*는 사실을 안다. `default`가 없다. 새 연산 — 예를 들어 `Sub` — 을 sealed에 추가하면 `eval`이 컴파일 에러로 갱신을 요구한다.

이 예제가 교과서적인 이유가 있다. *재귀적 데이터 구조*와 *재귀적 분기*가 같은 형태로 짝지어진다. `Add(Expr l, Expr r)`라는 record 패턴이 *데이터 구조를 그대로 그려내고*, `eval(l) + eval(r)`이 *그 구조 위의 연산을 그대로 그려낸다*. 데이터의 모양과 코드의 모양이 *일치*한다. 함수형 프로그래밍이 30년 동안 자랑해온 그 *대응*이 자바에 들어왔다.

여기에 *덧셈에서 0 더하기 같은 사소한 경우를 미리 제거*하는 *상수 폴딩(constant folding)*을 한 줄 더 붙여보자. guard가 빛나는 자리다.

```java
public static Expr simplify(Expr expr) {
    return switch (expr) {
        case Expr.Add(Expr.Num(int v1), Expr.Num(int v2)) -> new Expr.Num(v1 + v2);
        case Expr.Mul(Expr.Num(int v1), Expr.Num(int v2)) -> new Expr.Num(v1 * v2);
        case Expr.Add(Expr l, Expr.Num(int v)) when v == 0 -> simplify(l);
        case Expr.Add(Expr.Num(int v), Expr r) when v == 0 -> simplify(r);
        case Expr.Mul(Expr l, Expr.Num(int v)) when v == 1 -> simplify(l);
        case Expr.Add(Expr l, Expr r) -> new Expr.Add(simplify(l), simplify(r));
        case Expr.Mul(Expr l, Expr r) -> new Expr.Mul(simplify(l), simplify(r));
        case Expr.Num n -> n;
    };
}
```

여덟 줄에 *컴파일 타임 폴딩 + 항등원 제거 + 일반 재귀*가 모두 들어갔다. Visitor 패턴으로 이걸 적었더라면 100줄을 넘었을 것이다. 그리고 컴파일러는 여전히 *모든 sub-type이 덮였는지*를 검사한다.

## 예제 2 — HTTP `Result<T, E>` (현실 도메인)

교과서를 떠나 *현실 도메인*으로 옮기자. HTTP API 호출은 두 가지 결과 중 하나다 — *성공*이거나 *실패*. 자바 8 시절에는 이를 *checked exception*이나 *nullable 반환*으로 풀었다. 둘 다 *찜찜한 코드*를 만들었다.

함수형 진영의 답은 명확하다. `Result<T, E>`. 성공이거나 실패. 두 경우 각각이 *서로 다른 데이터*를 가진다. sealed가 정확히 받아낼 모양이다.

```java
public sealed interface Result<T, E> {
    record Ok<T, E>(T value) implements Result<T, E> {}
    record Err<T, E>(E error) implements Result<T, E> {}
}

public record HttpError(int status, String code, String message) {}

public Result<OrderResponse, HttpError> getOrder(String orderId) {
    try {
        var response = httpClient.send(buildRequest(orderId), JsonHandler.of(OrderResponse.class));
        return switch (response.statusCode()) {
            case 200 -> new Result.Ok<>(response.body());
            case 404 -> new Result.Err<>(new HttpError(404, "NOT_FOUND", "Order not found"));
            case int s when s >= 500 -> new Result.Err<>(new HttpError(s, "SERVER_ERROR", "Upstream failure"));
            default -> new Result.Err<>(new HttpError(response.statusCode(), "UNKNOWN", ""));
        };
    } catch (IOException | InterruptedException e) {
        return new Result.Err<>(new HttpError(0, "IO_ERROR", e.getMessage()));
    }
}
```

응답을 받아 *예외를 던지지 않고* `Result`로 감싼다. 호출 측은 어떻게 받는가?

```java
Result<OrderResponse, HttpError> result = client.getOrder("ord-42");

String userMessage = switch (result) {
    case Result.Ok<OrderResponse, HttpError>(OrderResponse order)
        -> "주문 " + order.orderId() + " 상태: " + order.status();
    case Result.Err<OrderResponse, HttpError>(HttpError(int status, String code, String _))
        when status == 404 -> "주문을 찾을 수 없습니다";
    case Result.Err<OrderResponse, HttpError>(HttpError(int status, var code, var msg))
        when status >= 500 -> "서버에 문제가 있습니다, 잠시 후 다시 시도해주세요";
    case Result.Err<OrderResponse, HttpError>(HttpError(var status, var code, var msg))
        -> "오류: " + code;
};
```

`HttpError` record를 *중첩 분해*하면서, *상태 코드별로 다른 메시지*를 만든다. guard가 *상태 코드 범위*를 받아내고, unnamed pattern이 *쓰지 않는 메시지*를 무시한다. 캐스트가 한 번도 등장하지 않고, `null`이 한 번도 등장하지 않고, 분기를 빠뜨릴 가능성이 0이다. *컴파일러가 그 모든 보증을 들고 있다*.

이 패턴이 Rust의 `Result<T, E>`와 거의 같은 모양이라는 점을 잠시 짚자. Rust 사용자라면 위 코드가 *문법만 다를 뿐 동일한 어휘*로 읽힌다. 자바가 함수형 진영의 *오랜 어휘*를 자기 것으로 받았다는 사실을 코드 한 덩이가 증명한다.

Spring의 `RestClient`나 `WebClient`를 사용하는 자리에서 이 `Result`가 자주 등장한다. 예외 기반 에러 처리와 결과 기반 에러 처리를 *섞지 않고*, 도메인 경계에서 한 번 변환한 뒤 *내부에서는 일관되게 Result*로 흐르게 하는 패턴이다.

## 예제 3 — Workflow 상태기계

세 번째 예제로 *주문 워크플로우의 상태기계*를 보자. 12장에서 잠시 짚은 결제 상태가 *단순한 결과*였다면, 워크플로우는 *상태 간의 *전이*를 모델링하는 일*이다. enum + flag 필드로 적던 그 자리다.

```java
public sealed interface OrderState {
    record Pending(Instant createdAt) implements OrderState {}
    record Paid(Instant createdAt, Instant paidAt, String paymentId) implements OrderState {}
    record Shipped(Instant createdAt, Instant paidAt, String paymentId,
                   Instant shippedAt, String trackingNumber) implements OrderState {}
    record Delivered(Instant createdAt, Instant paidAt, String paymentId,
                     Instant shippedAt, String trackingNumber, Instant deliveredAt) implements OrderState {}
    record Cancelled(Instant createdAt, Instant cancelledAt, String reason) implements OrderState {}
}
```

각 상태가 자기 정보를 *충분히 가진다*. `Pending`은 생성 시각만, `Paid`는 결제 시각과 ID, `Shipped`는 운송장 정보까지, `Delivered`는 도착 시각, `Cancelled`는 취소 사유. *상태에 따라 다른 데이터*라는 점이 자연스럽게 표현된다.

상태 전이도 switch 한 덩이에 담는다.

```java
public OrderState transition(OrderState current, OrderCommand command) {
    return switch (current) {
        case OrderState.Pending(var createdAt) -> switch (command) {
            case OrderCommand.Pay(var paymentId) ->
                new OrderState.Paid(createdAt, Instant.now(), paymentId);
            case OrderCommand.Cancel(var reason) ->
                new OrderState.Cancelled(createdAt, Instant.now(), reason);
            default -> throw new IllegalStateException("Pending에서 허용되지 않는 명령: " + command);
        };
        case OrderState.Paid(var createdAt, var paidAt, var paymentId) -> switch (command) {
            case OrderCommand.Ship(var trackingNumber) ->
                new OrderState.Shipped(createdAt, paidAt, paymentId, Instant.now(), trackingNumber);
            case OrderCommand.Cancel(var reason) ->
                new OrderState.Cancelled(createdAt, Instant.now(), reason);
            default -> throw new IllegalStateException("Paid에서 허용되지 않는 명령: " + command);
        };
        case OrderState.Shipped(var c, var p, var pid, var s, var t) -> switch (command) {
            case OrderCommand.Deliver _ ->
                new OrderState.Delivered(c, p, pid, s, t, Instant.now());
            default -> throw new IllegalStateException("Shipped에서 허용되지 않는 명령: " + command);
        };
        case OrderState.Delivered d ->
            throw new IllegalStateException("Delivered 상태에서는 전이 없음");
        case OrderState.Cancelled c ->
            throw new IllegalStateException("Cancelled 상태에서는 전이 없음");
    };
}
```

이중 switch — *외부는 상태, 내부는 명령*. 각 (상태, 명령) 조합에 대해 *허용되는 전이만* 코드에 적힌다. 허용되지 않는 조합은 명시적으로 거부한다. 상태와 데이터가 한 번 매칭되면, 그 데이터가 그대로 *다음 상태로 흘러 들어간다*. `Paid`의 `paymentId`가 `Shipped`로 그대로 옮겨가는 모습이 코드에 그려진다.

이런 모양을 *유한 상태기계(FSM)*라 부른다. 자바 8 시절에는 `Map<Pair<State, Command>, Transition>`이나 *Spring Statemachine* 같은 별도 라이브러리로 풀던 자리다. records + sealed + pattern으로 이 자리가 *언어 차원에서 표현 가능*해졌다. 별도 라이브러리 없이, 컴파일러의 보증을 받으면서.

여기에 한 가지 흥미로운 자리를 짚자. 위 코드에서 `default -> throw`가 등장하는데, 이 `default`가 *실제로는 도달하지 않을* 분기라면 어떨까? `OrderCommand`를 sealed로 만들어 *모든 명령을 명시적으로 분기*하면, `default` 자체가 사라진다. 그러면 새 명령이 추가될 때마다 *모든 상태의 switch*가 컴파일 에러로 갱신을 요구한다. 도메인이 자라는 자리를 *컴파일러가 우리 손에 쥐어준다*. 그 안전망이 production에서 *어느 새벽의 끔찍한 NPE*를 막아준다.

## Brian Goetz의 한 문단 — Data-Oriented Programming

이 자리에서 자바의 설계자 본인의 말을 한 번 인용하자. Brian Goetz가 2022년 InfoQ에 기고한 *Data-Oriented Programming in Java*의 핵심 문단이다.

> "Object-oriented programming says: combine code and data, and hide implementation details. Data-oriented programming says: separate code and data, make data immutable, and make illegal states unrepresentable.
>
> Records give us product types. Sealed classes give us sum types. Pattern matching gives us a way to take them apart. These three features together let us model data the way functional languages have for decades, but in idiomatic Java."

번역하자.

> "객체지향은 말한다 — *코드와 데이터를 묶고, 구현 세부를 감추라*. 데이터지향은 말한다 — *코드와 데이터를 분리하고, 데이터를 불변으로 만들고, 잘못된 상태가 표현되지 않도록 하라.*
>
> Records가 product type을 준다. Sealed가 sum type을 준다. Pattern matching이 그것들을 *분해할 도구*를 준다. 이 세 기능이 함께, 함수형 언어들이 *수십 년 동안* 해온 데이터 모델링을 *자바답게* 가능하게 해준다."

이 문단의 마지막 단어가 *idiomatic Java*다. 자바의 *문법답게*. 함수형 패러다임의 어휘를 자바로 *번역*해 들여온 것이 아니라, *자바답게 받아낸* 것이다. records의 `private final` 자동 부여, sealed의 `permits` 명시성, pattern의 `case`와 `when` — 모두 자바 사용자에게 *낯설지 않은 어휘*다. 자바답다.

*illegal states unrepresentable*이라는 표현도 음미하자. 잘못된 상태를 *표현할 수 없게* 만든다. enum + null이 표현했던 *"Pending인데 인증 URL이 null"* 같은 모양이 records + sealed에서는 *컴파일이 안 된다*. 잘못된 상태가 *코드로 적힐 수 없는* 자리에 못이 박힌다. 그것이 데이터지향 자바의 가장 큰 약속이다.

## Visitor 패턴의 사망 신고서

12장에서 Visitor 패턴의 *지긋지긋함*을 짚었다. 이 장의 도구를 모두 모은 자리에서, Visitor를 *한 줄 한 줄 ADT로 옮겨 보내자*. 4페이지 분량으로 한꺼번에.

같은 한 가지 도메인 — *식 표현식의 평가, 출력, 미분* — 을 Visitor와 ADT 두 방식으로.

**Visitor:**

```java
public abstract class Expr {
    public abstract <R> R accept(Visitor<R> v);
    public interface Visitor<R> {
        R visitNum(Num n);
        R visitAdd(Add a);
        R visitMul(Mul m);
    }
    // 세 sub-class 각각 약 10줄 — 생략
}

class Evaluator implements Expr.Visitor<Integer> {
    public Integer visitNum(Num n) { return n.value(); }
    public Integer visitAdd(Add a) { return a.left().accept(this) + a.right().accept(this); }
    public Integer visitMul(Mul m) { return m.left().accept(this) * m.right().accept(this); }
}

class Printer implements Expr.Visitor<String> {
    public String visitNum(Num n) { return String.valueOf(n.value()); }
    public String visitAdd(Add a) { return "(" + a.left().accept(this) + " + " + a.right().accept(this) + ")"; }
    public String visitMul(Mul m) { return "(" + a.left().accept(this) + " * " + a.right().accept(this) + ")"; }
}

class Differentiator implements Expr.Visitor<Expr> {
    private final String var;
    Differentiator(String var) { this.var = var; }
    public Expr visitNum(Num n) { return new Num(0); }
    public Expr visitAdd(Add a) { return new Add(a.left().accept(this), a.right().accept(this)); }
    public Expr visitMul(Mul m) {
        // 곱의 미분: (fg)' = f'g + fg'
        return new Add(
            new Mul(m.left().accept(this), m.right()),
            new Mul(m.left(), m.right().accept(this))
        );
    }
}
```

세 연산을 *세 개의 클래스*로 풀었다. 클래스마다 *세 visit 메서드*. 9개의 작은 메서드가 9개의 분기를 *객체로 모사*한다. 그리고 사용 측은 `expr.accept(new Evaluator())` 같은 호출을 적는다.

**ADT + Pattern matching:**

```java
public sealed interface Expr {
    record Num(int value) implements Expr {}
    record Add(Expr left, Expr right) implements Expr {}
    record Mul(Expr left, Expr right) implements Expr {}
}

public class Algebra {
    public static int eval(Expr e) {
        return switch (e) {
            case Expr.Num(int v) -> v;
            case Expr.Add(var l, var r) -> eval(l) + eval(r);
            case Expr.Mul(var l, var r) -> eval(l) * eval(r);
        };
    }

    public static String print(Expr e) {
        return switch (e) {
            case Expr.Num(int v) -> String.valueOf(v);
            case Expr.Add(var l, var r) -> "(" + print(l) + " + " + print(r) + ")";
            case Expr.Mul(var l, var r) -> "(" + print(l) + " * " + print(r) + ")";
        };
    }

    public static Expr differentiate(Expr e) {
        return switch (e) {
            case Expr.Num n -> new Expr.Num(0);
            case Expr.Add(var l, var r) -> new Expr.Add(differentiate(l), differentiate(r));
            case Expr.Mul(var l, var r) -> new Expr.Add(
                new Expr.Mul(differentiate(l), r),
                new Expr.Mul(l, differentiate(r))
            );
        };
    }
}
```

세 *함수*가 *한 클래스 안*에 모였다. 클래스를 따로 만들 필요 없고, accept-visit 왕복도 없다. 사용 측은 `Algebra.eval(expr)`을 그냥 호출한다.

Visitor 코드가 60줄 가까이 되는 데 비해, ADT 코드는 30줄. 그리고 컴파일러의 *완전성 보증*은 양쪽 다 같다. ADT 쪽은 *default가 필요 없으면서* 그 보증을 받는다.

Visitor 패턴은 *언어가 분기를 모르던 시절의 우회로*였다. 자바의 분기가 *데이터 분해를 알게* 된 순간, 그 우회로의 사용 이유가 사라졌다. *기존 Visitor 코드를 다 갈아치우자*는 말은 아니다. 그건 *지긋지긋한 작업*이 될 것이다. 그러나 *새로 적는 코드에 Visitor 패턴을 끌어들이지 말자*는 권유는 분명히 할 수 있다. 자바가 더 좋은 도구를 손에 쥐여줬으므로.

## Java 8 vs Java 21 — 한 도메인의 변천사

이 장의 마지막 비교로, 같은 한 가지 일 — *API 응답을 받아 사용자 메시지로 변환* — 을 11년 사이의 두 버전으로 적어보자.

**Java 8, 캐스트 사다리:**

```java
public String formatResponse(Object response) {
    if (response == null) {
        return "응답 없음";
    }
    if (response instanceof SuccessResponse) {
        SuccessResponse s = (SuccessResponse) response;
        if (s.getPayload() == null) {
            return "성공이지만 빈 응답";
        }
        if (s.getPayload() instanceof OrderCreated) {
            OrderCreated created = (OrderCreated) s.getPayload();
            return "주문 생성: " + created.getOrderId();
        }
        if (s.getPayload() instanceof PaymentApproved) {
            PaymentApproved approved = (PaymentApproved) s.getPayload();
            return "결제 승인: " + approved.getTransactionId();
        }
        return "알 수 없는 성공 응답";
    }
    if (response instanceof ErrorResponse) {
        ErrorResponse e = (ErrorResponse) response;
        if (e.getStatusCode() >= 500) {
            return "서버 오류: " + e.getMessage();
        }
        return "오류: " + e.getCode();
    }
    return "알 수 없는 응답 타입";
}
```

25줄. 들여쓰기 3단. instanceof + 캐스팅 6번. null 체크 2번. *알 수 없는*으로 끝나는 분기가 2개 — 이게 *진짜* 일어나야 하는 분기인지 *방어용*인지 코드를 읽어서는 알 수 없다. *찜찜한 코드*다.

**Java 21, sealed + pattern matching:**

```java
public sealed interface Response {
    record Success(Payload payload) implements Response {}
    record Error(int statusCode, String code, String message) implements Response {}
}

public sealed interface Payload {
    record OrderCreated(String orderId) implements Payload {}
    record PaymentApproved(String transactionId) implements Payload {}
}

public String formatResponse(Response response) {
    return switch (response) {
        case Response.Success(Payload.OrderCreated(var orderId))
            -> "주문 생성: " + orderId;
        case Response.Success(Payload.PaymentApproved(var txId))
            -> "결제 승인: " + txId;
        case Response.Error(int status, var code, var msg) when status >= 500
            -> "서버 오류: " + msg;
        case Response.Error(int status, var code, var _)
            -> "오류: " + code;
    };
}
```

15줄. 들여쓰기 1단. 캐스팅 0번. null 체크 0번. 그리고 *알 수 없는* 분기가 0개 — 모든 가능성이 sealed의 `permits`로 *명시적으로 닫혀 있기 때문*이다. 새 payload 타입이 추가되면 컴파일러가 그 사실을 *우리 손에 쥐어준다*.

11년이 두 코드 사이에 흘렀다. 그 11년 동안 자바는 *분기에 대한 자기 입장*을 *완전히 바꿔* 들었다. 이것이 modern Java의 미학이다.

## 14장으로 가는 다리 — 도메인을 ADT로 모델링했다면

여기까지가 데이터지향 자바의 *삼위일체*다. records로 *불변 데이터*를 정의하고, sealed로 *닫힌 대안*을 표명하고, pattern matching으로 *그것들을 분해*한다. 도메인이 코드에 *자연스럽게* 그려진다. 잘못된 상태는 *코드로 적힐 수 없다*.

자, 이 도메인 위에서 한 발 더 나가자. *동시성*이다.

생각해보자. 우리는 위 예제 2에서 HTTP API 호출을 `Result<OrderResponse, HttpError>`로 받았다. 만약 API 호출이 *세 개*라면? *외부 결제 게이트웨이 + 재고 시스템 + 회원 정보 시스템* — 세 API를 *병렬*로 호출하고, 세 결과가 모두 도착한 후에 결합해야 한다고 해보자.

Java 8 시절에는 `CompletableFuture.allOf`로 풀었다. 풀리긴 했다. 그러나 *Result로 감싼 결과 셋*을 합치는 코드는 *지긋지긋하게* 길었다. 그리고 `ForkJoinPool.commonPool()`에 blocking I/O를 태운 *끔찍한 사건*들도 동시에 일어났다.

Java 21의 *virtual threads*가 그 자리를 풀어준다. 다음과 같이 적힌다.

```java
public Result<OrderSummary, HttpError> compose(String orderId) {
    try (var scope = StructuredTaskScope.open()) {
        var paymentFuture = scope.fork(() -> paymentClient.get(orderId));
        var inventoryFuture = scope.fork(() -> inventoryClient.get(orderId));
        var memberFuture = scope.fork(() -> memberClient.get(orderId));

        scope.join();

        var payment = paymentFuture.get();
        var inventory = inventoryFuture.get();
        var member = memberFuture.get();

        return switch (payment) {
            case Result.Err<?, HttpError>(var err) -> new Result.Err<>(err);
            case Result.Ok<Payment, HttpError>(var p) -> switch (inventory) {
                case Result.Err<?, HttpError>(var err) -> new Result.Err<>(err);
                case Result.Ok<Inventory, HttpError>(var i) -> switch (member) {
                    case Result.Err<?, HttpError>(var err) -> new Result.Err<>(err);
                    case Result.Ok<Member, HttpError>(var m)
                        -> new Result.Ok<>(new OrderSummary(p, i, m));
                };
            };
        };
    }
}
```

`StructuredTaskScope`로 세 task를 *구조적으로* 묶고, 각 결과를 *pattern matching으로 분해*한다. virtual thread가 *세 호출의 blocking을 OS thread 없이* 견뎌낸다. 13장의 sealed `Result`가 14장의 virtual thread와 *그대로 만난다*.

다음 장에서는 *왜 이제야 thread-per-request가 가능해졌는지*를 시작점으로, virtual thread의 정체와 한계를 함께 살펴보자. 100 thread 풀로 버티던 *답답함*이 어떻게 풀려나는지, 그러나 켰는데 오히려 deadlock이 나는 *끔찍한 새벽*은 왜 일어나는지를. 도메인을 ADT로 모델링한 자리에서 *그 도메인 위의 동시성*을 다시 짜는 일이 시작된다.

기억해두자. records + sealed + pattern은 *언어가 데이터를 인정한 어휘*다. 그 어휘 위에 동시성과 메모리와 네이티브가 차곡차곡 쌓인다. 자바 11년의 변화가 *왜 이 자리에서 가장 아름다운지*를, 다음 장의 virtual thread에서 한 번 더 확인하자.
