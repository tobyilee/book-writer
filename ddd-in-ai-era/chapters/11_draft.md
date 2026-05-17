# 11장. 가상 프로젝트 (후반) — 결제 게이트웨이의 전술과 실행

10장에서 우리는 화이트보드 앞에 모여 있었다. 글로사리를 정리하고, 6개의 Bounded Context를 그렸고, Context Map의 화살표 방향을 두고 입씨름을 했다. 종이 위에서는 그림이 제법 그럴듯해 보였다. 그렇다면 이제 무엇을 할까?

종이는 종이일 뿐이다. 코드로 살아나지 않는 글로사리는 한 달이면 잊히고, 실행되지 않는 Context Map은 두 달이면 거짓말이 된다. 디스커버리·전략이 끝났다는 것은 끝의 시작일 뿐이다. 이제 그 종이를 코드로, 운영 워크플로로, 측정 가능한 지표로 옮겨야 한다.

이 장에서는 그 옮김의 과정을 따라가 보자. Aggregate 안의 invariant가 어떻게 짜이고, Domain Event 카탈로그가 어떻게 자라며, 외부 카드사의 거친 응답을 어떻게 우리 ULang으로 길들이는지 — 그리고 6개의 에이전트가 어떻게 한 팀을 이루고, 사람은 그 팀의 어느 지점에 발을 디뎌야 하는지를. 마지막으로, 이 모든 것이 한 달, 6개월을 굴러가게 만들 측정 지표 몇 가지를 살펴보자. 그 지표가 다음 12장의 거버넌스로 자연스럽게 이어지는 다리가 된다.

## 6단계 — Aggregate 설계: 사람이 양보해서는 안 되는 영역

먼저 가장 까다로운 곳부터 시작해보자. Aggregate다.

10장에서 우리는 6개 Bounded Context를 식별했다. 결제 처리, 정산, 분쟁·환불, 규제 준수, 라우팅·라이센싱, 부정거래 감지. 각 컨텍스트 안에는 자기만의 핵심 모델이 있다. 결제 처리 안에는 Payment와 PaymentAttempt가 있고, 정산 안에는 Settlement가 있고, 분쟁·환불 안에는 Dispute와 Refund가 있다. 이 모델들 하나하나가 Aggregate다.

Aggregate가 뭐였나? 일관성을 함께 책임지는 객체들의 묶음이다. 묶음 안에서는 항상 참이어야 하는 규칙들이 있다. 그 규칙을 invariant라고 부른다.

예를 들어보자. Refund Aggregate 안에는 이런 규칙이 있다. **"Refund 금액의 합은 원 Payment 금액을 절대 넘을 수 없다."** 너무 당연해 보이는가? 그렇지 않다. 부분 환불이 두세 번 일어나고, 통화 변환이 끼고, 수수료가 빠지고 더해지다 보면 어느새 환불액이 원금을 0.7원 초과해 있는 경험을 해본 사람이 있을 것이다. 그 0.7원이 정산 시스템 전체를 멈춰 세운다.

또 하나. Dispute Aggregate에는 이런 규칙이 있다. **"Dispute가 OPEN 상태인 동안에는 그 Payment의 Settle 처리가 진행될 수 없다."** 분쟁이 진행 중인 거래의 돈이 가맹점으로 빠져나가면 어떻게 될까? 카드사가 chargeback을 걸어왔을 때 회수할 돈이 이미 손을 떠나 있는 끔찍한 일이 벌어진다.

PaymentAttempt에도 invariant가 있다. **"PaymentAttempt는 생성 후 24시간 안에 PaymentAuthorized 또는 PaymentFailed 중 하나로 전이되어야 한다."** 24시간을 넘어 INITIATED 상태로 떠도는 시도가 있다면, 그건 우리 시스템이 외부 PG의 응답을 어딘가에서 흘려버렸다는 신호다. 그대로 두면 다음에 같은 카드로 결제 시도가 들어왔을 때 중복 청구가 발생할 수 있다.

이런 규칙은 누가 짜야 할까? 코드 생성 에이전트가 짜도 되는 것일까?

답은 단호하다. 사람이 짜야 한다. FTAPI 사례(Eisenreich et al., 2026)가 정직하게 인정한 결론이 이것이었다. 1단계 ULang, 2단계 Event Storming, 3단계 Bounded Context 식별까지는 LLM이 신뢰성 있게 도왔지만, 4단계 Aggregate 설계와 5단계 기술 아키텍처 매핑에서는 앞 단계 오류가 누적되어 실용성이 무너졌다. invariant는 도메인의 가장 깊은 약속이다. AI가 만들어낸 그럴듯한 후보를 그대로 받아들이는 순간 — 그 0.7원이 어디에선가 우리를 기다린다.

코드로 옮기면 이렇게 생긴다. 파이썬과 Pydantic으로 가볍게 스케치해보자.

```python
class Refund(Aggregate):
    payment_id: PaymentId
    amount: Money
    reason: RefundReason
    status: RefundStatus

    def apply(self, original_payment: Payment) -> None:
        # invariant 1: 통화가 같아야 한다
        if self.amount.currency != original_payment.amount.currency:
            raise InvariantViolation(
                f"Refund currency {self.amount.currency} "
                f"!= Payment currency {original_payment.amount.currency}"
            )
        # invariant 2: 환불 합계가 원 결제액을 넘을 수 없다
        total_refunded = original_payment.total_refunded() + self.amount
        if total_refunded > original_payment.amount:
            raise InvariantViolation(
                f"Total refund {total_refunded} exceeds payment {original_payment.amount}"
            )
        # invariant 3: Dispute가 진행 중이면 Refund 불가
        if original_payment.has_open_dispute():
            raise InvariantViolation("Cannot refund while dispute is open")
        self.status = RefundStatus.APPLIED
```

여기서 핵심은 `InvariantViolation` 예외가 던져지는 그 지점이다. 그 지점이 우리 도메인의 약속이 발화되는 곳이다. 코드 한 줄 한 줄이 비즈니스 운영진과 우리가 회의실에서 합의한 문장들의 번역이다. "Dispute 중에는 환불이 안 됩니다"가 `has_open_dispute()`로, "환불 총액은 결제액을 넘으면 안 됩니다"가 부등식으로.

> **사이드바: 의료 청구의 invariant**
> 의료 보험 청구 도메인이라면 어떨까. "한 환자의 동일 진료일에 같은 수가 코드는 두 번 청구될 수 없다", "응급실 청구는 입원 청구와 동일 청구 건으로 묶일 수 없다" — 이런 규칙이 invariant다. 결제와 본질은 같다. 도메인 전문가가 한 문장으로 말할 수 있는 약속을, 그러나 위반되면 며칠치 정산을 거꾸로 되돌려야 하는 약속을 코드에 박는 일이다.

## 7단계 — Domain Event 카탈로그: 시스템의 말이 흐르는 강

Aggregate가 사실의 단위라면, Domain Event는 사건의 단위다. 무언가가 일어났음을 시스템이 발화하는 형식이다.

결제 도메인의 이벤트 카탈로그를 짜보자. 이름 짓기부터 시작이다.

- `PaymentInitiated` — 결제가 시도됨
- `PaymentAuthorized` — 카드사가 승인을 내림
- `PaymentSettled` — 정산이 완료됨
- `PaymentFailed` — 시도가 실패함
- `RefundRequested` — 환불이 요청됨
- `RefundApplied` — 환불이 적용됨
- `DisputeOpened` — 분쟁이 열림
- `DisputeResolved` — 분쟁이 해결됨
- `ComplianceFlagRaised` — 규제 준수 플래그가 올려짐

이름을 보면 한 가지 공통점이 있다. 전부 과거형이다. `Initiate`, `Authorize`가 아니라 `Initiated`, `Authorized`. 이미 일어난 일을 부른다. 이 작은 문법적 약속이 시스템 전체의 사고방식을 바꾼다. 누구도 이벤트를 "취소"할 수 없다. 일어난 일은 일어난 것이다. 그 위에 다른 이벤트(예: `PaymentReversed`)를 쌓아 올릴 뿐이다.

스키마는 어떻게 짤까. Pydantic으로 한 예를 보자.

```python
class PaymentAuthorized(DomainEvent):
    event_id: EventId
    occurred_at: datetime
    aggregate_id: PaymentId
    schema_version: int = 1

    amount: Money
    authorization_code: str
    issuer_country: CountryCode
    pg_reference: str  # 외부 PG가 돌려준 식별자
```

`schema_version` 필드를 빠뜨리지 말자. 이 한 줄이 6개월 뒤 우리를 살린다. 비즈니스가 자라면 같은 이벤트의 형태가 바뀐다. 새 필드가 추가되고, 기존 필드의 의미가 미세하게 변한다. 버전 번호 없이 시작했다가는, 어느 시점에 어떤 모양의 이벤트가 흘렀는지 추적할 수 없는 난감한 상황에 빠진다.

발행과 구독은 어떻게 설계할까. 결제 처리 컨텍스트가 `PaymentAuthorized`를 발행하면, 정산 컨텍스트와 부정거래 감지 컨텍스트가 구독한다. 정산은 그 이벤트로 자기 워크플로의 시작 신호를 받고, 부정거래 감지는 그 패턴이 위험한지 점수를 매긴다. 한 이벤트가 여러 컨텍스트의 행동을 촉발한다.

여기서 중요한 운영적 가치 하나가 따라온다. **audit trail**이다. 이벤트 로그를 시간 순으로 다 보관해두면, "이 결제 건이 왜 이 상태가 되었나"를 언제든지 재구성할 수 있다. 에이전트가 뭔가를 잘못했을 때도 마찬가지다. 어떤 이벤트를 받고, 어떤 결정을 내려, 어떤 이벤트를 발행했는지가 전부 남아 있다. AI 시대에 이 audit trail은 단순한 로그가 아니다. 에이전트의 행동을 검증하고, 회귀하고, 책임을 추적하는 단일 진실이 된다.

> **사이드바: 게임 도메인의 domain event**
> MMORPG라면 `PlayerLeveledUp`, `ItemDropped`, `PartyFormed`, `BossDefeated`가 이벤트다. 게임 서버에서 일어난 일이 분석·랭킹·로그 시스템으로 흘러간다. 결제와 다른 점은 빈도다. 초당 수만 건. 하지만 본질은 같다. 과거형 이름, 스키마 버전, 발행/구독 관계, 그리고 audit trail.

## 8단계 — Anti-Corruption Layer: 의미의 국경 검문소

이제 외부와 만날 차례다. 우리 게이트웨이는 결국 카드사 PG를 호출해야 한다. Stripe, KCP, Toss, NICE — 각자 자기 어휘로 응답을 돌려준다.

Stripe의 PaymentIntent 응답을 한번 보자.

```json
{
  "id": "pi_3O8...",
  "amount": 5000,
  "currency": "krw",
  "status": "requires_capture",
  "charges": {
    "data": [{
      "id": "ch_3O8...",
      "outcome": {
        "network_status": "approved_by_network",
        "reason": null,
        "risk_level": "normal"
      }
    }]
  }
}
```

KCP는 또 다른 모양이다. `res_cd`, `tno`, `amount`, `card_cd` 같은 짧은 한글/영어 약어 필드들. Toss는 또 다르다. 같은 "승인됨"이라는 사실을 세 회사가 서로 다른 단어로 부른다.

이걸 우리 도메인 코드 안에 그대로 끌어들이면 어떻게 될까? `if response.status == "requires_capture" or response.res_cd == "0000": ...` 같은 코드가 결제 처리 컨텍스트 안에서 자라기 시작한다. 그 if문이 두 줄, 세 줄, 일곱 줄로 늘어나는 데는 한 분기면 충분하다. 우리 ULang은 어디로 갔는가? 어디에도 없다. 외부의 단어들이 우리 도메인을 점령해버렸다.

그래서 필요한 것이 Anti-Corruption Layer, 줄여서 ACL이다. Golovko의 표현을 빌리면 "semantic firewall"이다. 외부의 거친 단어가 우리 도메인 안으로 들어오기 전에 우리 ULang으로 번역되는 지점.

```python
class StripeAdapter:
    def authorize(self, command: AuthorizeCommand) -> PaymentAuthorized | PaymentFailed:
        raw = self.stripe_client.create_payment_intent(
            amount=command.amount.minor_units,
            currency=command.amount.currency.code.lower(),
        )
        return self._translate(raw, command)

    def _translate(self, raw: dict, cmd: AuthorizeCommand) -> DomainEvent:
        # Stripe의 어휘 → 우리 ULang
        status = raw["status"]
        if status in ("requires_capture", "succeeded"):
            return PaymentAuthorized(
                aggregate_id=cmd.payment_id,
                amount=cmd.amount,
                authorization_code=raw["id"],
                issuer_country=self._infer_country(raw),
                pg_reference=raw["id"],
                occurred_at=datetime.utcnow(),
            )
        if status in ("requires_payment_method", "canceled"):
            return PaymentFailed(
                aggregate_id=cmd.payment_id,
                reason=self._translate_reason(raw),
                occurred_at=datetime.utcnow(),
            )
        # 우리가 모르는 상태가 들어오면? 절대 통과시키지 말자.
        raise UnknownExternalStatus(f"Stripe status not mapped: {status}")
```

여기서 마지막 줄을 주의해서 보자. 우리가 모르는 외부 상태가 들어오면 예외를 던진다. 그냥 무시하거나, 디폴트 처리로 넘기면 어떻게 될까? Stripe가 새로운 상태값을 어느 날 추가했을 때, 우리 시스템은 그것을 조용히 삼키고 잘못된 가정 위에서 돌아가게 된다. ACL은 모르는 단어를 "모른다"고 명시적으로 외쳐주는 검문소여야 한다.

KCP, Toss용 adapter도 같은 형태로 만든다. 외부에서 보면 셋이 다 다른 PG지만, 우리 도메인 코드 입장에서는 셋 다 똑같이 `PaymentAuthorized` 또는 `PaymentFailed`만 돌려준다. 도메인은 PG가 누군지 신경 쓰지 않아도 된다.

이게 Hexagonal 원칙 — "도메인 계층은 표준 라이브러리 외 외부 의존성 0" — 의 실제 모습이다. Stripe SDK는 adapter 안에서만 import된다. 도메인 안에서는 import 한 번 일어나지 않는다.

## 9단계 — 6-Agent 팀: 누가 무엇을 책임지는가

도메인 모델과 ACL이 자리를 잡았으니, 이제 에이전트를 붙여보자.

Iusztin의 6-agent 패턴을 기반으로 결제 게이트웨이에 맞춰 다시 짠다. 우리 경우엔 SWE 에이전트가 6개의 Bounded Context를 각각 맡으므로 좀 더 커진다.

- **PM 에이전트** — 작업 분해, ADR 작성, `docs/glossary.md` 유지
- **SWE-Payment 에이전트** — 결제 처리 BC 전담
- **SWE-Settlement 에이전트** — 정산 BC 전담
- **SWE-Dispute 에이전트** — 분쟁·환불 BC 전담
- **SWE-Compliance 에이전트** — 규제 준수 BC 전담
- **SWE-Routing 에이전트** — 라우팅·라이센싱 BC 전담
- **SWE-Fraud 에이전트** — 부정거래 감지 BC 전담
- **Tester 에이전트** — 적대적 E2E, 도메인 이벤트 시나리오 생성
- **PR Reviewer 에이전트** — diff-only 리뷰, 글로사리 위반·중복·죽은 코드 점검
- **On-Call 에이전트** — CI 통과까지 루프, 실패 원인 분류
- **Self-Improve 에이전트** — 회고, 코딩 layer·glossary 갱신 제안

Iusztin의 가장 중요한 원칙을 기억하자. **"No agent both writes code and decides whether the code is correct."** 코드를 짠 에이전트가 자기 코드를 검증하지 않는다. SWE가 짠 코드는 Tester가 두드리고, PR Reviewer가 본다. 자기 글을 자기가 교정하면 오타가 안 보이는 것과 똑같다.

각 에이전트의 시스템 프롬프트에는 무엇이 들어가야 할까? 글로사리다. 절대 빠뜨려서는 안 된다.

```text
[SWE-Settlement 에이전트 시스템 프롬프트 일부]

너는 결제 게이트웨이의 Settlement Bounded Context를 담당한다.
이 컨텍스트의 ULang은 다음과 같다.

- Payment: 카드사 승인이 완료된 결제. PaymentAttempt와 구분된다.
- Settlement: 가맹점 계좌로의 정산 단위. 일자별·통화별로 묶인다.
- SettlementBatch: 같은 정산 주기·같은 가맹점에 속한 Settlement의 묶음.
- SettlementCycle: 정산 주기 (T+1, T+3 등). 가맹점 계약에 따라 다르다.

invariants:
- 한 Settlement는 한 가맹점·한 통화에만 속한다.
- Settlement 금액의 합은 그에 속한 Payment 금액의 합과 ±0.01 미만 차이여야 한다.
- Dispute가 OPEN인 Payment는 Settlement에 포함될 수 없다.

너는 Payment Aggregate를 직접 수정하지 않는다. 결제 처리 BC의 schema와
event를 통해서만 상호작용한다.
```

이 프롬프트가 매 세션마다 SWE-Settlement에게 주입된다. 에이전트는 자기가 어느 컨텍스트 안에 있는지, 자기 컨텍스트의 단어가 무엇인지, 다른 컨텍스트와 어떻게 이야기해야 하는지를 매번 다시 듣는다. 그래야 한 달 뒤에 다른 모델로 갈아끼웠을 때도 같은 약속을 지킬 수 있다.

물론 Iusztin이 솔직하게 인정한 한계가 있다. "에이전트가 글로사리를 일관되게 활용하지 못하는 경우도 있다." 그래서 PR Reviewer가 있다. PR Reviewer의 체크리스트 첫 줄에 "이 PR에 등장한 도메인 어휘가 glossary.md에 있는가, 같은 의미로 쓰였는가"를 박아두자.

> **사이드바: 물류 운영의 에이전트 팀**
> 화물 운송 도메인이라면 어떨까. Order Booking 에이전트, Route Optimization 에이전트, Customs Clearance 에이전트, Last-Mile Delivery 에이전트, Tracking 에이전트가 각자 BC를 책임진다. 핵심은 같다. BC 1개 = 에이전트 1개. 한 에이전트가 두 BC를 겸하기 시작하면, 둘 사이의 ULang 경계가 흐려진다. 그 흐려진 곳에서 버그가 자란다.

## 10단계 — 휴먼 체크포인트: 사람이 발을 디뎌야 하는 자리

자동화는 좋다. 하지만 자동화가 사람을 영원히 빼내는 것은 아니다. 어떤 자리에서는 반드시 사람이 발을 디뎌야 한다.

체크포인트를 명시적으로 설계하자. 결제 게이트웨이 운영에서 사람이 반드시 보아야 하는 4개 지점을 짚어본다.

**첫째, invariant 위반 검사.** 모든 `InvariantViolation` 예외는 운영 대시보드에 알람을 띄운다. 에이전트가 이 예외를 catch해서 조용히 retry하게 두면 안 된다. invariant 위반은 우리 도메인의 가장 깊은 약속이 깨졌다는 신호다. 사람이 보고, 이 위반이 진짜 데이터 이상인지 아니면 우리 invariant 자체를 수정해야 하는지를 판단해야 한다.

**둘째, 신규 도메인 이벤트 추가.** 새로운 `Event` 클래스를 만드는 PR이 들어오면 반드시 사람이 승인한다. Domain Event는 한번 시스템에 등록되면 모든 컨텍스트에 영향을 미친다. 에이전트가 자동으로 늘려가게 두면 6개월 뒤 이벤트 카탈로그가 30개에서 200개로 부풀고, 무엇이 무엇과 어떻게 다른지 아무도 모르는 상태가 된다.

**셋째, schema 버저닝 결정.** 기존 이벤트의 스키마를 바꿀 때 — 새 필드 추가, 기존 필드 의미 변경, 필드 제거 — 사람이 버전을 올린다. 에이전트가 "그냥 이렇게 하면 되겠지" 하고 schema_version 그대로 둔 채 필드를 바꿔버리면, 그 이벤트를 구독하던 다른 컨텍스트의 파싱이 조용히 깨진다.

**넷째, Compliance 플래그 검토.** `ComplianceFlagRaised` 이벤트는 늘 사람의 눈을 거친다. AML(자금세탁 방지), KYC(고객 확인) 관련 플래그는 법적 책임이 따르는 영역이다. 에이전트가 자동으로 "false positive로 분류하고 종료" 처리하게 두면, 어느 날 금융감독원 감사에서 끔찍한 일이 벌어진다.

Iusztin이 제안한 "휴먼 체크포인트 2개 + 재시도 상한 5회"는 출발점이다. 도메인이 무거울수록 체크포인트는 더 늘어난다. 결제는 위 4개를 권장한다. 너무 많은가? 자동화의 본질은 사람이 손을 떼는 것이 아니다. 사람이 손을 **더 중요한 곳에** 디딜 수 있도록 다른 자리에서 손을 떼는 것이다.

## 11단계 — 측정 지표: 운영을 굴리는 다섯 가지 숫자

이 모든 것이 한 달, 6개월을 굴러가게 만들려면 무엇을 봐야 할까. 다섯 가지 지표를 권하자.

**(1) 에이전트당 평균 토큰, 그 중 도메인 로직 비중.** Siemens의 Golovko가 제시한 KPI다. 6개월간 prompt spaghetti가 자라기 전 상태가 에이전트당 3,000+ 토큰, 그 중 85%가 파싱·통합 로직이었다. DDD 4패턴(BC 분리, schema-as-contract, ACL, context map)을 적용한 뒤 ~500 토큰, 90%가 도메인 로직으로 바뀌었다. 우리 시스템에서도 같은 측정을 하자. 도메인 로직 비중이 50%를 밑돌기 시작하면 prompt spaghetti의 전조다.

**(2) 글로사리-코드 일관도.** `docs/glossary.md`에 등재된 용어가 코드·OpenAPI 스키마·DB 컬럼명·UI 카피에 얼마나 일관되게 등장하는가. CI에 검증 스크립트를 박아둘 수 있다. 예: "glossary에 `PaymentAttempt`가 등재되어 있는데 코드에 `payment_try`라는 변수명이 등장하면 경고." 100%를 목표로 할 필요는 없지만, 90% 밑으로 내려가면 ULang이 침식되고 있다는 신호다.

**(3) AI 공저 코드의 보안 취약점 비율.** 박정현이 제시한 2.74×의 차이, arXiv 2602.12430이 보고한 에이전트 스킬 취약점 26.1%를 기억하자. SAST 도구에서 검출된 취약점 수를, 인간 단독 작성 코드와 AI 공저 코드로 나누어 비교한다. 격차가 좁혀지지 않는다면 PR Reviewer 에이전트의 보안 가드레일을 강화해야 한다.

**(4) 환각 발생 빈도.** 에이전트가 존재하지 않는 함수를 호출하거나, 가짜 ULang 용어를 만들어내거나, 외부 API를 허구로 가정하는 빈도를 센다. 어떻게 세나? CI 실패 로그, 글로사리 검증 실패, PR Reviewer가 잡아낸 케이스 — 이 셋을 합산한다. 절대 0이 될 수는 없다. 하지만 추세가 위로 향하면 무언가가 무너지고 있는 것이다.

**(5) 비용·토큰 사용량 추이.** 일·주·월 단위로 모델별, 에이전트별 토큰 사용량을 그래프로 본다. 어느 에이전트가 갑자기 토큰을 두 배 쓰기 시작했다면 — Self-Improve 에이전트가 그것을 회고 주제로 잡게 한다. 한국 환경에서는 환율 변동까지 따로 추적해야 한다는 점도 잊지 말자.

이 다섯 지표를 매주 한 페이지짜리 대시보드에 띄워두자. 회의실 모니터에 늘 떠 있게. 숫자 하나가 이상해지면 누구든 알아챌 수 있다.

## 의도적으로 다루지 않은 것

한 권의 책에 담은 가상 프로젝트는 완전체일 수 없다. 우리는 결제 게이트웨이의 골격을 봤지만, 실제로 production에 올리려면 다뤄야 할 영역이 산처럼 남아 있다. 멀티 리전 배포 전략, 데이터 마이그레이션, 외부 PG의 webhook 재시도 보장, 통화 환산의 정밀한 처리, 정산 주기와 휴일 캘린더의 결합 — 이 모든 것이 각자 한 챕터씩을 차지해야 마땅한 주제다.

이 책의 가상 프로젝트가 보여준 것은 한 가지다. **AI 시대에 DDD의 패턴이 어떻게 손에 잡히는 코드와 운영으로 옮겨지는가**의 한 경로. 결제가 아닌 도메인 — 의료, 게임, 물류, 교육 — 으로 옮길 때 사이드바들을 참고하자. 본질은 같다. 글로사리, Bounded Context, Aggregate와 invariant, Domain Event, ACL, 에이전트와 휴먼 체크포인트, 측정 지표. 단어가 바뀔 뿐이다.

## 마무리 — 12장으로 가는 다리

여기까지 따라온 우리에겐 한 가지 풍경이 손에 잡혀 있을 것이다. 10장의 화이트보드가 11장에서 코드와 운영으로 살아났다. PM 에이전트가 작업을 나누고, 6개의 SWE 에이전트가 각자의 BC를 짜고, Tester가 두드리고, PR Reviewer가 보고, On-Call이 굴리고, Self-Improve가 회고한다. 사람은 네 군데 체크포인트에 발을 디딘다. 다섯 개의 숫자가 매주 대시보드에 뜬다.

그렇다면 이 6-Agent 팀이 한 달, 6개월, 1년을 안정적으로 돌아가려면 무엇이 더 필요할까?

답이 쉽지 않다. 한 달은 어떻게든 굴러간다. 6개월 차에 prompt spaghetti가 자라고, AI 공저 코드의 보안 취약점이 인간 코드보다 2.74배 더 쌓이기 시작하고, 환각이 어느 날 잘못된 invariant를 슬쩍 끼워넣고, 비용이 어느 분기엔가 두 배로 뛰고, 누가 무엇을 했는지 추적할 수 없는 사건이 한 번 터진다. 그리고 외부 라이브러리를 쓴 코드가 라이선스 위반이라는 메일이 법무팀에서 날아온다.

이 다섯 가지 — 보안, 환각, 비용, 관측성, IP·라이선스 — 가 시니어와 아키텍트의 일상이 된다. 11장에서 우리가 세운 측정 지표들은 사실 이 다섯 기둥의 입구다. 다음 12장에서 그 다섯 기둥을 하나씩 세워보자. 거기서 우리의 6-Agent 팀이 비로소 6개월을, 1년을 살아남는다.
