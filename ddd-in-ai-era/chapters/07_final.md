# 7장. Aggregate와 invariant — 사람의 마지막 영역

월요일 아침이라고 상상해보자. 새로 합류한 에이전트 팀이 주말 동안 결제 도메인의 초기 모델을 잡아 놓았다. `docs/glossary.md`도 산뜻하게 정돈되어 있고, Entity와 Value Object는 클래스 다이어그램까지 가지런하다. Repository 인터페이스도 시그니처가 일관되고, 팩토리 메서드도 잘 분리되어 있다. 글로사리에서 시작해 메타모델까지 한 호흡에 떨어진 그 결과물은, 사람 개발자 한 명이 일주일을 들였어도 비슷한 수준이었을지 가늠하기 어려울 만큼 깔끔하다.

기분 좋게 코드를 펼친다. 그런데 `Order` 클래스의 한 메서드에서 눈이 멈춘다.

```python
class Order:
    def apply_refund(self, refund: Refund) -> None:
        # AI가 생성한 invariant
        if refund.amount > self.total_amount * 2:
            raise InvalidRefundError("환불 금액 초과")
        self.refunds.append(refund)
```

환불 금액이 주문 총액의 **두 배**를 넘으면 예외를 던진다. 두 배까지는 허용한다는 뜻이다. 어떻게 두 배까지 허용된다는 말인가. 글로사리에는 그런 규칙이 적혀 있지 않다. 회계 담당자에게 물어보면 분명히 "환불은 결제 금액을 초과할 수 없다"고 잘라 말할 것이다. 그런데 AI는 그럴듯한 톤으로 두 배라는 숫자를 코드 한복판에 박아 두었다. 코드는 컴파일도 되고 단위 테스트도 통과한다. 다만 비즈니스 규칙이 조용히 망가져 있을 뿐이다.

이 장면이 우리에게 던지는 질문은 단순하다. AI가 거의 다 해주는 영역과, 아직도 사람이 끝까지 들고 있어야 하는 영역의 경계는 어디인가? 그 경계 위에 우리의 일과 책임은 어떻게 새로 정의되는가?

## AI가 잘하는 영역 — 메타모델과 정형 산출물

먼저 좋은 소식부터 살펴보자. Wiegand 등이 2026년 보고한 연구에 따르면, 도메인 메타모델 JSON을 생성하는 작업은 큰 모델 없이도 잘 된다. Code Llama를 4비트로 양자화하고 LoRA로 파인튜닝한, 그야말로 컨슈머 GPU에서 돌아가는 작은 모델이 단순한 프롬프트만으로 구문상 정확한 JSON 객체를 일관되게 뽑아냈다. 후처리도 거의 필요 없었다. 자원이 빈약한 환경에서도 DDD 워크플로에 AI를 끼워 넣을 수 있다는 실증이다.

이 결과를 우리 일에 어떻게 옮길 수 있을까. Entity와 Value Object 정의, Repository 인터페이스, Factory 시그니처, 메타모델 스키마 — 이런 산출물은 본질적으로 **정형**이다. 형식이 정해져 있고, 들어가야 할 필드와 메서드의 이름이 글로사리에서 거의 강제된다. LLM은 이런 정형 산출물을 정말 잘 만든다. 한국어로 번역된 AI-DLC 백서가 Aggregate, VO, Entity, Domain Event, Repository, Factory를 모두 에이전트가 자율 생성하는 흐름을 그려둔 것도 같은 맥락이다. 한국 자동화 방법론에서도 DDD의 전술적 패턴은 1급 자동화 대상으로 들어와 있다.

여기까지만 보면 도메인 모델링이 거의 다 자동화되는 것처럼 보인다. 그렇다면 사람의 역할은 점점 줄어드는 것 아닌가? 결론을 내리기 전에 같은 시기의 또 다른 연구를 한 번 살펴보자.

## AI가 실패하는 지점 — Eisenreich의 FTAPI 실험

Eisenreich, Jusic, Wagner가 2026년에 내놓은 논문은 LLM 프롬프팅으로 DDD를 자동화하는 프레임워크를 설계하고, FTAPI라는 실제 기업의 요구사항으로 검증했다. 이들은 DDD 활동을 다섯 단계로 분해했다.

1. Ubiquitous language 수립
2. Event storming 시뮬레이션
3. Bounded context 식별
4. Aggregate 설계
5. 기술 아키텍처 매핑

결과가 흥미롭다. 1단계부터 3단계까지는 신뢰성 있게 작동했다. 용어집과 컨텍스트 맵이 실용적 산출물로 떨어졌다. 그런데 4단계와 5단계에서 무너졌다. 앞 단계의 사소한 오류와 부정확성이 다음 단계로 전파되면서 누적·증폭되었고, aggregate 설계와 기술 매핑은 실용성을 잃을 정도로 흔들렸다. 저자들의 결론은 단호하다.

> "Later steps show how minor errors or inaccuracies can propagate and accumulate."
> "LLMs can enhance, but not replace, architectural expertise."

이 두 문장을 머릿속에 잘 새겨두자. AI는 아키텍처 전문성을 **보강한다**. 대체하지 못한다. 1, 2, 3단계의 작은 흔들림이 4, 5단계의 큰 흔들림으로 번지는 양상은, 우리가 LLM에게 어디까지 일을 맡길 수 있는가에 대한 가장 명확한 실증 자료다.

왜 4-5단계에서 실패할까. 단순히 모델이 작아서가 아니다. 이 두 단계는 본질적으로 다른 종류의 작업이다. Entity 정의는 한 줄의 결정 — "이 엔티티의 식별자는 무엇인가" — 으로 끝난다. 그러나 aggregate 설계는 다르다. "이 트랜잭션 경계 안에서 어떤 객체들이 함께 변경되어야 하는가", "어떤 invariant가 항상 참이어야 하는가", "어떤 외부 참조는 ID로만 두고 어떤 객체를 내부에 안고 있어야 하는가" — 이 모든 결정이 비즈니스 규칙의 응집을 요구한다. 단순 정형이 아니라 **규칙의 응집체**다. 그리고 그 규칙은 도메인 전문가의 머릿속과 비공식 문서에 분산되어 있다.

추론 체인이 다섯 층을 거치는 동안 각 층에서 5%의 오류가 끼면, 마지막에는 1 - 0.95⁵ ≈ 23%의 오류가 누적된다(사실 확인 필요 — 단순 계산 예시). aggregate 단계는 모델의 능력 한계가 아니라 **추론 누적의 한계**가 드러나는 자리다.

## Aggregate는 왜 사람의 영역인가

Aggregate를 다시 한 번 생각해보자. Aggregate는 단순한 객체 묶음이 아니다. 트랜잭션 일관성이 보장되어야 하는 경계이고, 그 경계 안에서는 invariant — 즉 "절대 깨져서는 안 되는 비즈니스 규칙" — 가 모든 시점에서 참이어야 한다.

쇼핑몰을 한 번 떠올려보자. `Order`라는 aggregate를 잡았다고 해보자. 이 안에는 `OrderLine`들이 있고, `Payment` 정보가 있고, `Refund` 이력이 있다. 이 aggregate가 지켜야 할 invariant는 무엇일까.

- 모든 `OrderLine`의 금액 합이 `Order.totalAmount`와 일치해야 한다.
- `Refund` 금액 총합은 `Payment` 금액을 넘지 못한다.
- `Order`가 `COMPLETED` 상태가 된 뒤에는 `OrderLine`을 추가할 수 없다.
- 취소 가능 기간이 지난 뒤에는 환불 가능 여부가 정책에 따라 달라진다.

이 규칙들이 모두 어디에 있는가? 일부는 글로사리에 적혀 있을 것이다. 일부는 회계팀의 운영 매뉴얼에 있다. 일부는 CS 담당자의 머릿속에만 있다. 일부는 작년 12월의 사장 결재 메일에만 있다. 일부는 누구도 명문화한 적 없는 **암묵지**다.

AI 에이전트는 이 분산된 지식을 알 수 없다. 알려준 적이 없기 때문이다. 그래서 LLM은 가장 자주 만나는 패턴 — 학습 데이터에 흔히 등장하는 도메인 모델 — 으로 빈칸을 채운다. 그 결과가 "환불은 결제 금액의 두 배까지 가능"이라는 그럴듯한 거짓말이다. 모델은 거짓말을 하려고 한 것이 아니라, 채울 정보가 없어서 가장 그럴듯한 숫자를 채웠을 뿐이다.

기억해두자. **Aggregate 경계와 invariant는 비즈니스 규칙의 응집이고, 비즈니스 규칙은 데이터셋에 없다.** 데이터셋에 없는 것을 모델이 추론으로 메우는 순간, 그것이 곧 환각이다.

## AI 환각의 도메인 모델링적 결과

조금 더 구체적으로 살펴보자. AI 에이전트가 도메인 모델링에서 환각을 일으킬 때, 그 환각은 어떤 모습으로 나타나는가? 모르고 지나치면 정말 난감해질 수 있는 세 가지 유형을 짚어보자.

**첫째, 잘못된 invariant 제안.** 앞서 본 환불 두 배 사례가 전형이다. AI는 "이 정도면 합리적이겠지" 싶은 임의의 임계값을 코드에 박아 넣는다. 컴파일도 되고 테스트도 통과한다. 그런데 회계 규칙과 어긋난다. 운영에 올라가서 환불이 두 배로 나간 뒤에야 발견되면, 그때 복구 비용은 끔찍한 수준이 된다.

**둘째, 가짜 ULang 후보.** 글로사리에 등재되지 않은 용어를 AI가 만들어내서 코드에 흘리는 경우다. 회사에서 한 번도 쓴 적 없는 단어가 메서드 이름이나 도메인 이벤트 이름으로 등장한다. 예를 들어 결제 도메인에서 갑자기 `PaymentReconciliationToken` 같은 용어가 등장한다면, 그게 회사의 표준 어휘인지 AI가 지어낸 단어인지 어떻게 구별할까. 다른 에이전트도 같은 컨텍스트에서 이 단어를 마주치면 "기존 용어"로 받아들이고 강화한다. 한 번의 환각이 어휘 표준을 오염시킨다.

**셋째, 허구의 외부 API 가정.** AI가 "Stripe API에 이런 엔드포인트가 있을 것이다", "결제 게이트웨이가 이런 응답을 줄 것이다"라고 가정하고 어댑터를 짜는 경우다. 실제 API 문서를 펼쳐보면 그런 엔드포인트는 존재하지 않는다. 통합 테스트 단계에서 발견되면 그나마 다행이지만, 모킹된 단위 테스트만으로 PR이 통과해 버리면 운영에서 NullPointerException으로 터진다.

이 세 가지는 모두 같은 뿌리에서 나온다. **모델이 모르는 것을 모른다고 말하지 못한다.** 가장 그럴듯한 답을 채우는 것이 학습 목적이었으니, 그 본성이 도메인 모델링에서도 그대로 발현된다. 우리는 이 본성을 바꿀 수 없다. 다만 그 본성이 위험한 자리 — aggregate와 invariant — 에 사람이 서 있으면 된다.

환각 문제는 그 자체로 더 깊은 논의가 필요하다. 거버넌스 차원에서 어떻게 막을지, 어떤 신호로 조기에 잡을지는 뒤에서 한 번 더 본격적으로 다룰 자리가 있다. 여기서는 일단, **aggregate 설계에서 환각이 가장 비싸게 먹힌다**는 사실을 기억하고 다음으로 넘어가자.

## Mimul의 12원칙이 다시 빛나는 자리

Mimul의 "언어 독립적 도메인 중심 코딩 12원칙" 중에 이런 문장이 있다.

> "비즈니스 규칙은 반드시 도메인 모델 내부에 명시적으로 표현되어야 한다."

그리고 같은 글에 이런 문장도 있다.

> "AI가 코드를 생성하고 수정하는 빈도가 높아질수록 코드가 얼마나 명확하고 의도적으로 작성되었는지가 AI의 추론 품질과 직결된다."

이 두 문장을 묶어서 읽어보자. 어떤 그림이 그려지는가. 비즈니스 규칙이 도메인 모델 **내부에** 있어야 한다는 말은 단순한 OOP 모범 사례가 아니다. AI 시대에 이 원칙은 한 단계 더 무거워진다. 규칙이 서비스 클래스에 흩어져 있거나 컨트롤러에 박혀 있거나 데이터베이스의 트리거에 숨어 있으면, AI 에이전트는 그 규칙을 발견하지 못한다. 발견하지 못한 규칙은 무시되고, 무시된 규칙은 환각의 빈자리가 된다.

반대로 규칙이 도메인 모델 내부에 명시적으로 있으면 — 즉 `Order.apply_refund()` 메서드 안에 invariant가 명문으로 검사되고 있으면 — AI는 그 메서드의 시그니처와 본문을 읽고 규칙을 학습한다. 다음 번에 비슷한 로직을 만들 때 그 패턴을 따라간다. 명시성은 AI에게 가장 친절한 형태의 문서다.

그렇다면 도메인 모델을 어디에 두어야 그 명시성이 보호되는가? 여기서 Hexagonal 아키텍처가 다시 등장한다.

## Hexagonal — 도메인 계층의 외부 의존성 0

Bardia Khosravi가 2025년에 정리한 "AI 코딩 에이전트를 위한 백엔드 코딩 규칙"에 한 줄로 표현된 원칙이 있다.

> "도메인 계층은 표준 라이브러리 외 외부 의존성을 0으로 유지하라."

이 원칙은 AI 시대에 특별히 더 중요해진다. 왜 그럴까. AI 에이전트는 자기에게 주어진 컨텍스트 안에서 추론한다. 도메인 모델 파일을 읽을 때, 그 파일이 ORM 어노테이션 범벅이고, 프레임워크 시그니처가 메서드마다 붙어 있고, 외부 SDK 호출이 비즈니스 로직 한복판에 끼어 있으면, AI는 **무엇이 도메인 규칙이고 무엇이 인프라 글루 코드인지 구별하지 못한다.** 도메인 추론과 인프라 추론이 같은 추론 체인에 섞이면 환각 표면이 그만큼 넓어진다.

반대로 도메인 계층이 표준 라이브러리 외에 아무 의존성도 없다면, AI가 도메인 파일을 열었을 때 보이는 것은 순수한 비즈니스 규칙뿐이다. 추론할 범위가 좁아지고, 잘못 채울 빈칸도 줄어든다. 같은 이유로, 사람이 코드 리뷰를 할 때도 도메인 규칙만 떼어내서 검토할 수 있다. Hexagonal 원칙은 사람과 AI 모두에게 친절한 경계다.

실무에서 어떻게 강제할 수 있을까? 정적 분석으로 도메인 패키지의 import 문을 검사하는 것이 간단한 출발점이다.

```python
# tests/architecture/test_domain_purity.py
import ast
from pathlib import Path

ALLOWED_STDLIB = {"datetime", "decimal", "enum", "typing", "uuid", "dataclasses"}
DOMAIN_ROOT = Path("src/domain")

def test_domain_layer_has_no_external_dependencies():
    violations = []
    for py_file in DOMAIN_ROOT.rglob("*.py"):
        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                top = (node.module or "").split(".")[0]
                if top and top not in ALLOWED_STDLIB and not top.startswith("domain"):
                    violations.append(f"{py_file}: {node.module}")
    assert not violations, f"도메인 계층 외부 의존성 발견:\n" + "\n".join(violations)
```

이런 테스트 하나가 CI에 들어가 있으면, AI 에이전트가 무심코 `import sqlalchemy`를 도메인 파일에 추가했을 때 자동으로 막힌다. 사람이 일일이 PR을 검토하지 않아도 된다. 이런 가드레일이야말로 AI 시대 도메인 계층을 지키는 방법이다.

## 테스트 전략 위계 — 누가 무엇을 책임지는가

자, 이제 가장 실용적인 질문으로 들어가자. Aggregate와 invariant를 사람이 책임진다고 했는데, 구체적으로 어떻게 책임진다는 말인가? 매번 모든 코드를 사람이 직접 작성해야 한다는 뜻인가? 그렇지는 않다. 책임의 핵심은 작성이 아니라 **검증**에 있다. 그리고 검증은 세 층의 위계로 분담하는 편이 낫다.

### 1층 — 사람이 작성하는 invariant 단위 테스트

가장 안쪽 층이고 가장 무거운 책임이다. Aggregate가 지켜야 할 invariant를 **사람이 직접** 단위 테스트로 명문화한다. 이 테스트는 AI가 짜지 않는다. 왜냐하면 invariant 자체가 비즈니스 규칙의 정수이고, 그 규칙을 AI가 알 수 없기 때문이다. AI에게 invariant 테스트를 맡기면 환각이 또 다른 환각을 검증하는 자기 참조 구조가 된다.

이 층의 테스트가 어떻게 생겼는지 살펴보자.

```python
# tests/domain/test_order_invariants.py
import pytest
from decimal import Decimal
from domain.order import Order, OrderLine, OrderStatus
from domain.refund import Refund

class TestOrderInvariants:

    def test_refund_total_cannot_exceed_payment(self):
        """[INV-1] 환불 누적 금액은 결제 금액을 절대 초과할 수 없다.
        근거: 회계 운영 매뉴얼 §3.2 (2025-11 결재)
        """
        order = Order.create(total=Decimal("10000"))
        order.record_payment(Decimal("10000"))
        order.apply_refund(Refund(amount=Decimal("7000")))

        with pytest.raises(InvalidRefundError):
            order.apply_refund(Refund(amount=Decimal("4000")))

    def test_completed_order_rejects_new_line(self):
        """[INV-2] COMPLETED 상태의 주문에는 새 라인을 추가할 수 없다.
        근거: 글로사리 OrderStatus 정의
        """
        order = Order.create(total=Decimal("0"))
        order.add_line(OrderLine(name="A", price=Decimal("5000")))
        order.complete()

        with pytest.raises(OrderImmutableError):
            order.add_line(OrderLine(name="B", price=Decimal("3000")))

    def test_line_total_matches_order_total(self):
        """[INV-3] 모든 라인의 금액 합은 주문 총액과 일치한다."""
        order = Order.create(total=Decimal("0"))
        order.add_line(OrderLine(name="A", price=Decimal("3000")))
        order.add_line(OrderLine(name="B", price=Decimal("2000")))

        assert order.total == sum(line.price for line in order.lines)
```

각 테스트의 docstring에 invariant 번호와 **출처**를 적어둔 점에 주목하자. "회계 운영 매뉴얼 §3.2"처럼 비공식 문서로 분산된 규칙의 출처를 코드 안으로 끌어오면, 미래의 사람과 AI 모두에게 동일한 단일 진실이 생긴다. 이것이 사람이 작성하는 invariant 테스트의 본질이다 — 검증 자체보다 **규칙의 명문화**가 더 중요하다.

### 2층 — AI가 생성하는 적대적 케이스

사람이 invariant의 정상 케이스를 작성했다면, AI에게 **적대적 케이스**를 부탁할 차례다. "이 invariant를 깨뜨릴 만한 입력값들을 떠올려봐. 경계값, 음수, 0, 매우 큰 수, 부동소수점 오차, 동시성, 시간대 — 가능한 모든 적대적 케이스를 나열해줘."

AI가 잘하는 일 중 하나가 바로 이것이다. 학습 데이터에 수많은 엣지 케이스가 있었고, 그 패턴을 빠르게 조합해낸다. 사람이 놓치기 쉬운 케이스를 잘 떠올린다. 단, **사람이 작성한 정상 케이스가 먼저 있어야** AI의 적대적 케이스가 의미를 갖는다. 그렇지 않으면 AI는 자기가 짠 invariant를 자기가 적대 테스트하는 셈이 되어, 환각의 자기 합리화 구조가 된다.

```python
# tests/domain/test_order_invariants_adversarial.py
# AI 에이전트 생성 → 사람 리뷰 통과 후 반영
class TestOrderInvariantsAdversarial:

    @pytest.mark.parametrize("amount", [
        Decimal("0.01"),               # 최소 금액
        Decimal("9999999999.99"),      # 최대 금액
        Decimal("-100"),               # 음수
        Decimal("0"),                  # 0
    ])
    def test_refund_with_boundary_amounts(self, amount):
        order = Order.create(total=Decimal("10000"))
        order.record_payment(Decimal("10000"))

        if amount <= 0 or amount > Decimal("10000"):
            with pytest.raises((InvalidRefundError, ValueError)):
                order.apply_refund(Refund(amount=amount))
        else:
            order.apply_refund(Refund(amount=amount))
```

### 3층 — Tester 에이전트의 E2E 검증

마지막 층은 별도의 Tester 에이전트가 책임진다. Iusztin의 6-에이전트 팀 구성을 떠올려보자. 그 팀의 원칙 중 하나가 이것이었다.

> "No agent both writes code and decides whether the code is correct."

코드를 짠 에이전트와 그 코드를 검증하는 에이전트는 반드시 분리한다. Tester 에이전트는 SWE 에이전트가 만든 aggregate 구현이 사람이 정의한 invariant 단위 테스트와 AI가 생성한 적대적 케이스를 모두 통과하는지 E2E로 돌려보고, 더 나아가 시나리오 기반으로 적대적 검증을 수행한다. "결제 후 부분 환불, 추가 환불, 동시 환불 요청 — 이 시퀀스가 invariant를 깨지 않는가."

세 층의 분업표를 한 번 정리해보자.

| 층 | 작성자 | 산출물 | 책임 |
|---|---|---|---|
| 1층 | **사람** | invariant 단위 테스트 | 비즈니스 규칙의 명문화 |
| 2층 | AI(생성) → 사람(리뷰) | 적대적 엣지 케이스 | 사람이 놓친 입력 공간 탐색 |
| 3층 | Tester 에이전트 | E2E 시나리오 검증 | 통합 흐름의 invariant 보존 |

이 위계의 핵심은 **위에서 아래로** 작성한다는 점이다. 1층이 비어 있는 상태에서 2층부터 시작하면 안 된다. 사람이 invariant를 모르는 채로 AI에게 적대적 케이스를 만들라고 시키면, AI는 자기가 상상한 invariant에 대한 적대적 케이스를 만들 뿐이다. 그게 우리 회사의 비즈니스 규칙과 일치할 가능성은 낮다.

테스트 거버넌스 전반은 뒤에서 다시 다룰 자리가 있다. 여기서는 일단 이 3층 분업의 골격을 잡고 가자.

## 실행 패턴 — 한 사이클을 어떻게 굴리는가

이제까지의 원칙을 한 사이클로 묶어보자. 새 도메인 모델을 만들 때, 사람과 AI는 어떤 순서로 일을 주고받아야 할까. 권장 흐름은 다음과 같다.

**1단계. 사람이 도메인을 스케치한다.** 글로사리에 핵심 용어를 등재한다. Aggregate 후보를 식별하고, 각 aggregate가 지켜야 할 invariant를 문장으로 적어둔다. 이때는 코드를 짜지 않는다. 자연어로도 충분하다. Evan Moon의 말을 빌리면, "AI 사용 전에 자신의 설계안을 먼저 작성"하는 단계다. 생성 효과(generation effect) 덕분에 도메인 직관이 살아 있는다.

**2단계. AI에게 Entity와 VO 초안을 맡긴다.** 글로사리와 사람이 적은 invariant 문서를 컨텍스트로 주고, Entity 클래스와 Value Object를 생성하라고 한다. Wiegand 등의 실험이 보여주듯, 이 단계는 작은 모델로도 잘 돌아간다. 산출물은 사람이 빠르게 훑고 명백한 오타나 불일치만 잡아준다.

**3단계. 사람이 aggregate 경계를 정의한다.** 어떤 Entity가 어떤 aggregate에 속하는가, aggregate 루트는 누구인가, aggregate 간 참조는 ID로만 둘 것인가. 이 결정은 사람이 한다. 이유는 앞서 말한 그대로다. 트랜잭션 일관성과 invariant 응집은 비즈니스 규칙의 응집이고, 비즈니스 규칙은 AI의 학습 데이터에 없다.

**4단계. AI에게 Repository와 Factory를 위임한다.** Aggregate 경계가 정해지면, 그 경계를 따라 Repository 인터페이스와 Factory를 만드는 일은 다시 정형 작업이다. AI가 잘한다. 단, Hexagonal 경계 — 도메인 계층은 외부 의존성 0 — 가 지켜지는지 정적 분석 테스트로 강제한다.

**5단계. 사람이 invariant 단위 테스트를 작성한다.** 1단계에서 적어둔 invariant를 코드 테스트로 옮긴다. 각 테스트의 출처를 docstring에 남긴다. 이 단계는 짧지만, 책 전체에서 사람이 가장 결연하게 들고 있어야 할 자리다.

**6단계. Tester 에이전트에게 적대적 검증을 부탁한다.** 적대적 케이스 생성, E2E 시나리오 통과 여부 확인, 동시성·시간대·경계값 모두 훑게 한다. 실패가 나오면 다시 1단계 invariant 정의로 돌아간다 — 새로 발견된 규칙을 글로사리와 invariant 문서에 추가한다.

이 사이클의 정신은 단순하다. **AI에게는 정형 산출물을, 사람에게는 규칙의 응집을.** 둘의 경계가 분명할수록 환각의 표면적이 줄어든다.

## 그래서 우리의 일은 어떻게 변하는가

처음 던졌던 질문으로 돌아가보자. AI가 거의 다 해주는 영역과 사람이 끝까지 들고 있어야 하는 영역의 경계는 어디인가? 그 경계가 우리의 일과 책임에 무엇을 의미하는가?

경계는 분명해졌다. 글로사리 등재, Entity 정의, VO 추출, Repository 시그니처, Factory 메서드, 메타모델 JSON — 이런 정형 산출물은 AI에게 맡기는 편이 낫다. 사람이 직접 짤 때보다 빠르고 일관성도 좋다. 반대로 aggregate 경계 결정, invariant의 명문화, 트랜잭션 일관성 설계, cross-aggregate 정합성 정책 — 이런 규칙의 응집은 사람의 영역이다. 데이터셋에 없는 것은 추론으로 메울 수 없다.

이 경계가 우리 일에 의미하는 바는, 시니어 개발자의 가치가 **코딩 속도**가 아니라 **규칙 응집의 정확성**으로 옮겨간다는 사실이다. 더 빨리 타이핑하는 사람이 아니라, 도메인 전문가와 더 오래 앉아 invariant를 캐낼 수 있는 사람, 분산된 비즈니스 규칙의 출처를 추적해 코드 안으로 끌어오는 사람, 그리고 그렇게 모은 규칙을 사람이 작성한 단위 테스트로 명문화할 줄 아는 사람이 가장 비싼 사람이 된다. 박정현의 표현을 빌리면, "AI는 생산성을 높여주는 도구이지, 나를 대체하는 도구가 아니다." 단, 그 도구를 가장 잘 쓰려면 사람이 들고 있어야 할 영역을 명확히 알아야 한다.

기억해두자. 정형은 위임하고, **응집은 직접 들자**. Aggregate와 invariant는 사람의 마지막 영역이다. 그리고 그 마지막 영역을 정확히 지키는 것이 AI 시대 시니어의 차별화된 가치다.

다음 장에서는 시야를 한 단계 넓혀보자. 한 에이전트 안에서 aggregate를 잘 지킨다고 끝이 아니다. 에이전트가 여럿 있을 때, 같은 단어가 컨텍스트마다 다른 의미를 가질 때, 그 의미의 경계를 어떻게 그어야 하는가. Context Map과 ACL이 AI 시대에 어떤 새로운 의미를 갖게 되었는지 — Schema-as-Contract와 Semantic Firewall이라는 두 개의 키워드로 풀어가보자.
