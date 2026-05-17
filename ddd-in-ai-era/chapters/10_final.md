# 10장. 가상 프로젝트 (전반) — 글로벌 결제 게이트웨이의 디스커버리와 전략

지금까지 9개 장에 걸쳐 ULang의 격상, BC와 에이전트의 매핑, Aggregate와 invariant의 사람 영역, Context Map과 ACL의 새 의미, Domain Event와 멀티 에이전트 통신까지 살펴봤다. 머릿속에는 그림이 그려졌을지 모른다. 그런데 막상 월요일 아침에 새 프로젝트를 받아 들고 노트북을 열면 어떨까. "그래서 첫 줄을 어디서부터 쓰지?" 하는 막막함이 밀려온다. 개념과 실무 사이에는 늘 메울 수 없을 것 같은 협곡이 있다.

이번에는 그 협곡 위로 다리 하나를 놓아보자. 가상의 도메인을 하나 잡고, 처음부터 끝까지 직접 디스커버리와 전략 단계를 밟아보는 것이다. 추상 개념이 손에 잡히는 워크플로로 응축되는 모습을 한 번 경험하고 나면, 자기 도메인으로 옮기는 일은 한결 수월해진다.

## 왜 글로벌 결제 게이트웨이인가

가상 프로젝트의 도메인을 무엇으로 잡을지 잠시 고민했다. 결국 글로벌 결제 게이트웨이로 정한 데에는 몇 가지 이유가 있다.

첫째, 한국 시니어 개발자에게 충분히 친숙하다. Toss, KCP, 이니시스, PayPal, Stripe — 직접 연동해본 적이 없더라도 한두 번쯤 결제 모듈 디버깅 화면을 들여다본 경험이 있을 것이다. 둘째, 도메인이 충분히 복잡하다. 다국가, 다통화, 환불, 분쟁(chargeback), 정산(settlement), 규제 준수(KYC/AML/PCI-DSS)까지 — 단순한 CRUD 한 장으로 끝나는 도메인이 아니다. 셋째, 공개 도메인 지식이 풍부하다. Stripe의 엔지니어링 블로그, Toss와 당근의 기술 블로그, 한국은행과 금융위의 전자금융업 자료까지 — 우리가 인용할 수 있는 1차 자료가 곳곳에 있다.

다만 한 가지 약속하고 가자. 이 가상 프로젝트는 책 한 권에 담는 응축본이다. 실제 글로벌 PG를 만들려면 이 책 분량의 50배가 필요할 것이다. 우리가 할 일은 모든 디테일을 채우는 것이 아니라, **디스커버리에서 전략까지의 워크플로 자체를 손으로 그려보는** 것이다. 자기 도메인에 적용할 때의 패턴 인식을 얻는 것 — 그것이 이 두 장의 목표다.

자, 그럼 첫 단계부터 시작해보자.

## 1단계 — 이해관계자 식별과 어휘 차이 매핑

DDD의 첫 미덕은 "코드를 쓰기 전에 사람을 먼저 본다"는 것이다. AI 시대에도 이건 변하지 않는다. 오히려 더 중요해졌다. 왜냐하면 에이전트는 이해관계자가 쓰는 어휘를 그대로 흡수해서 코드와 스키마에 박아 넣을 것이고, 한 번 박힌 어휘를 나중에 바꾸는 일은 끔찍하기 때문이다.

글로벌 결제 게이트웨이 프로젝트에서 만나야 할 사람들을 일단 적어보자.

- **PO (Product Owner)** — "결제 성공률을 어떻게 올리지", "신규 국가 진출이 우선이다"
- **운영(Operations)** — "환불 처리에 평균 며칠 걸리지", "분쟁 건수가 늘고 있다"
- **세일즈** — "엔터프라이즈 고객은 정산 주기 단축을 원한다"
- **법무·컴플라이언스** — "EU PSD2, 한국 전금법, 미국 OFAC 제재 목록"
- **정산 담당** — "T+2 정산", "월말 마감", "환차손 처리"
- **CS** — "고객은 '결제 취소'와 '환불'을 구분 못한다"
- **외부 PG 파트너 엔지니어** — "Visa 인터체인지 수수료", "BIN 라우팅"

같은 "결제"라는 단어를 두고도 이들은 서로 다른 것을 본다. PO에게 "결제"는 전환율 지표 한 줄이고, 운영에게는 환불 가능 여부가 걸린 상태 머신이며, 법무에게는 보관 의무 7년짜리 거래 기록이고, 정산 담당에게는 T+2 후 통장에 찍힐 숫자다. 이 어휘 차이를 처음에 매핑하지 않으면 에이전트가 짜는 코드는 곧 누구의 언어도 아닌 잡종이 된다.

여기서 잠깐, 벤치마크 리딩을 같이 해두면 좋다. Stripe 엔지니어링 블로그의 *"How we built it: Stripe's revenue recognition system"* 같은 글을 읽어보면, 그들이 도메인 어휘를 어떻게 코드 모듈명까지 끌고 들어갔는지 보인다. PayPal과 Adyen의 공개 도큐먼트도 마찬가지다. 외부 회사의 어휘 그대로 베끼라는 뜻이 아니다. **"같은 도메인을 먼저 푼 사람들이 어떤 단어들을 1급 시민으로 격상시켰는지"**를 흡수하는 것이 목적이다. 우리 도메인의 ULang 초안에 좋은 출발점이 된다.

> **사이드바: 의료 도메인에서는 이 단계가 어떻게 다른가**
> 의료 청구(medical claims) 시스템을 시작한다고 해보자. 이해관계자는 의사, 간호사, 청구 담당자(coder), 보험사 심사역, 환자, 그리고 HIPAA 규제 담당자다. 결제와 비슷하게 "claim"이라는 한 단어가 사람마다 다른 의미다 — 의사에게는 진료 행위 한 건, coder에게는 ICD-10/CPT 코드의 묶음, 보험사 심사역에게는 승인/거부 대상이다. 다른 점은 **의료에서는 "환자 안전"이라는 비기능 요구가 일찍부터 ULang에 등장한다**는 것이다. 결제의 "분쟁"이 사후 처리 흐름이라면, 의료의 "오진 위험"은 사전 차단 흐름이다. 도메인이 다르면 이해관계자 매핑 결과의 무게중심이 다르게 잡힌다는 점을 기억하자.

## 2단계 — Vibe Modeling 워크숍

이해관계자와 그들의 어휘를 한 차례 모았다면, 이제 그것들을 **시각적인 흐름**으로 펼쳐야 한다. 여기서 Vibe Modeling을 쓴다.

Vibe Modeling은 vibemodeling.app이 제안한 워크숍 형식이다. Event Storming의 디지털·AI 보조 버전이라고 보면 된다. 화이트보드 대신 무한 캔버스, 오프라인 포스트잇 대신 디지털 스티커, 그리고 한쪽에 LLM 어시스턴트가 앉아서 "지금 이 도메인 이벤트 다음에 자연스럽게 따라올 이벤트가 뭐죠?"를 묻는 식이다.

가상 프로젝트의 워크숍을 한 번 머릿속에서 돌려보자. 도메인 전문가(PO·운영·법무 대표), 시니어 개발자 두세 명, 그리고 AI 어시스턴트가 한자리에 모였다. 시작은 늘 가장 큰 사건부터다.

```
[PaymentInitiated] → [PaymentAuthorized] → [PaymentCaptured] → [PaymentSettled]
                  ↘ [PaymentFailed]
                  
[RefundRequested] → [RefundApproved] → [RefundExecuted]
                  ↘ [RefundDenied]

[DisputeOpened] → [EvidenceSubmitted] → [DisputeWon | DisputeLost]

[ComplianceFlagRaised] → [HumanReviewRequested] → [TransactionBlocked | TransactionReleased]
```

이렇게 도메인 이벤트를 시간 순으로 쭉 펼쳐놓으면 자연스럽게 보이는 것이 있다. **이벤트들이 묶음으로 뭉친다**. 결제 처리 묶음, 환불·분쟁 묶음, 정산 묶음, 규제 묶음. 이게 곧 Bounded Context 후보다.

워크숍 중에 AI 어시스턴트의 역할은 두 가지다. 첫째, **"빠뜨린 이벤트"를 묻는다**. "PaymentInitiated와 PaymentAuthorized 사이에 사기 점수 평가가 들어가는데, 그건 어디 이벤트로 잡을까요?" 둘째, **용어 일관성을 체크한다**. 누군가는 "결제 실패", 누군가는 "결제 거절"이라고 했다면 "둘이 같은 건가요, 다른 건가요?"라고 묻는다. 답은 사람이 한다. 결정권은 도메인 전문가가 가진다. AI는 빠진 곳을 찾아주는 보조다.

이 단계에서 절대 하지 말아야 할 것이 있다. **AI에게 "결제 게이트웨이의 도메인 이벤트를 다 뽑아줘"라고 시키고 그 결과를 받아쓰기 하는 것**이다. 그건 ULang을 외부 일반 지식으로 덮어쓰는 행위다. 6장에서 다뤘듯 ULang은 그 조직만의 정밀한 단어 합의이고, 워크숍 자체가 그 합의를 만드는 의식이다. AI가 합의 결과를 대체할 수는 없다.

> **사이드바: 게임 도메인에서의 Event Storming**
> MMORPG 백엔드 팀이 같은 워크숍을 한다고 해보자. 도메인 이벤트는 [PlayerSpawned] → [QuestAccepted] → [MonsterDefeated] → [ItemDropped] → [InventoryUpdated] → [LevelUp] 같은 흐름이 펼쳐진다. 결제와 가장 다른 점은 **시간 스케일**이다. 결제는 초·분·일 단위의 이벤트가 섞이지만, 게임은 밀리초 단위의 이벤트가 폭주한다. 그래서 게임에서는 Event Storming 단계에서 이미 "어떤 이벤트가 실시간으로 처리되고, 어떤 이벤트가 배치로 처리될지"의 경계가 같이 그려진다. 도메인의 시간 특성이 BC 분할에 미리 영향을 준다는 점에서 결제와 다르다.

## 3단계 — `docs/glossary.md` 작성, ULang 정렬

5장에서 ULang이 LLM 시대의 1급 자산이라고 했다. 그 말이 실무에서 어떻게 구현되는지가 이 단계다. Paul Iusztin의 6-Agent 팀이 가장 먼저 만든 것도 `docs/glossary.md`였다.

워크숍에서 모인 단어들을 정밀하게 다듬어보자. 결제 도메인에서 가장 혼동되는 트리플 — **PaymentAttempt vs Payment vs RefundedPayment** — 부터 잡아보자.

```markdown
# docs/glossary.md

## 핵심 거래 용어

### PaymentAttempt (결제 시도)
사용자가 결제 버튼을 눌러 PG에 인증을 요청한 단일 시도.
- 상태: PENDING → AUTHORIZED | FAILED
- 24시간 안에 종결 상태로 전이되어야 한다 (invariant)
- 한국어 표준 표기: "결제 시도"
- 외부 PG 매핑: Stripe `PaymentIntent`, Toss `paymentKey` (raw)

### Payment (결제)
PaymentAttempt가 AUTHORIZED 된 후 CAPTURED까지 완료된 상태.
즉, 가맹점이 실제로 돈을 "받기로 확정한" 거래.
- "결제 완료"와 동의어 (CS 화면에서는 후자 사용)
- 한 PaymentAttempt에서 최대 1개의 Payment가 파생된다
- 정산(Settlement)의 단위

### Refund (환불)
이미 CAPTURED 된 Payment의 전체 또는 일부를 사용자에게 돌려주는 행위.
- Refund.amount ≤ Payment.amount (invariant, 부분 환불 합도 포함)
- "취소(Cancellation)"와 다르다 — 취소는 CAPTURE 전 단계의 철회

### Cancellation (취소)
PaymentAttempt가 AUTHORIZED 됐지만 CAPTURE 되기 전 단계에서의 철회.
- 사용자 입장에서는 "결제 취소"로 보이지만, 회계 흐름은 Refund와 완전히 다르다
- 정산 대상이 되지 않으므로 Settlement 모듈에 노출되지 않는다

### Dispute (분쟁)
사용자(또는 발급사)가 이미 완료된 Payment에 이의를 제기한 상태.
- Chargeback과 동의어로 쓰지만, 내부 ULang은 Dispute로 통일
- Dispute가 OPEN인 Payment는 Settle될 수 없다 (invariant)
- 증거 제출(EvidenceSubmission)·심사 기한(deadline)·승패(Won/Lost)의 라이프사이클
```

이 정도까지 정밀하게 써두면 무엇이 좋은가? 모든 에이전트의 시스템 프롬프트에 이 glossary가 주입되는 순간, **PaymentAttempt를 Payment라고 부르는 코드가 더는 PR에 들어오지 않는다**. 5장에서 봤듯 에이전트는 ULang을 자동으로 알 수 없고, 명시적으로 가르치지 않으면 GPT가 학습한 일반 영문 결제 용어 — 흔히는 Stripe의 어휘 — 로 덮어써버린다. 그러면 같은 코드베이스 안에서 PaymentIntent와 PaymentAttempt가 뒤섞이는 끔찍한 사태가 벌어진다.

한국 결제사 용어와의 매핑을 별도 섹션으로 두는 것도 권장한다. Toss는 `paymentKey`, KCP는 `tno`, 이니시스는 `tid` — 외부 어휘를 내부 ULang으로 번역하는 사전이 곧 ACL의 출발점이 된다(이건 11장의 ACL 설계로 연결된다).

Toss의 기술 블로그를 보면 "결제 시스템 도메인 분리기" 같은 글에서 자기네 ULang의 일부가 노출된다. 당근도 마찬가지로 비즈니스 도메인을 코드 모듈명에 박은 사례를 공유해왔다. 그런 공개 자료는 우리의 glossary 초안을 검증하는 데 좋은 거울이 된다.

> **사이드바: 물류 도메인에서의 ULang 사례**
> 글로벌 물류 시스템에서 가장 정밀하게 정의되는 단어 중 하나는 "Shipment"다. 화주(shipper)에게는 "보낸 한 건의 짐", 운송사에게는 "Bill of Lading 번호 하나가 붙는 묶음", 세관에게는 "HS 코드별 신고 단위", 창고에게는 "랙 위치 점유 단위"다. 한 도메인 안에서 같은 단어가 5개의 다른 단위로 작동한다. 물류 회사의 ULang은 그래서 Shipment, Consignment, Container, Package, SKU를 각각 별개의 1급 시민으로 등재하고, 어떤 관계로 묶이는지를 도식으로 명시한다. 결제의 PaymentAttempt vs Payment 구분과 똑같은 정밀도가 요구된다. 도메인은 달라도 ULang을 정밀하게 다듬는 작업의 결은 같다는 것을 보여주는 사례다.

## 4단계 — Bounded Context 식별

이제 ULang이 정리됐고 도메인 이벤트의 묶음이 보인다. 그 묶음들을 정식 Bounded Context로 격상시킬 차례다. 6장에서 "BC = Agent 1개"라는 산업 표준 매핑을 봤으니, 우리는 처음부터 **각 BC가 곧 에이전트 책임 단위**라는 전제로 그린다.

가상 프로젝트의 6개 BC를 잡아보자.

1. **결제 처리(Payment Processing)** — PaymentAttempt 생성·인증·캡처. 외부 카드사 통신, 3DS 인증, 결제 라우팅 호출. 가장 트래픽이 많고 가장 지연 민감한 코어 컨텍스트.

2. **정산(Settlement)** — Payment를 가맹점별·일자별로 모아 송금. T+N 정산 사이클, 환차 처리, 수수료 차감. 결제 처리의 **downstream**이고, 한 번 정산되면 되돌리기 어려운 사후 회계 컨텍스트.

3. **분쟁·환불(Dispute & Refund)** — Refund 요청 처리, Dispute 라이프사이클 관리, 증거 수집·제출. 결제 처리와는 다른 시간 스케일(일·주 단위)에서 움직인다.

4. **규제 준수(Compliance)** — KYC, AML 스크리닝, OFAC 제재 매칭, PCI-DSS 감사 로그. 모든 거래 흐름에 가로지르는 **횡단 관심사**지만, 한 BC로 묶어 정책 결정과 플래그 발행을 책임지게 한다.

5. **라우팅·라이센싱(Routing & Licensing)** — 어느 카드 BIN을 어느 PG 파트너로 보낼지, 어느 국가의 어느 라이선스로 처리할지 결정. 결제 처리의 **upstream**으로 작동하지만, 라우팅 규칙 자체는 별도의 도메인 로직이다.

6. **부정거래 감지(Fraud Detection)** — 실시간 사기 점수 평가, 룰 엔진·머신러닝 모델 운영. Compliance와 다른 점은 "법적 의무" vs "비즈니스 손실 방어"의 무게중심 차이.

이렇게 6개로 자르고 나면 자연스럽게 떠오르는 질문이 있다. **"왜 6개인가, 4개나 8개면 안 되나?"** 답은 단호하다. **정답은 없고, 조직 구조와 운영 책임 라인을 따른다**. 만약 어떤 회사에서 분쟁과 환불을 두 개의 별도 팀이 운영한다면 그건 2개의 BC로 쪼개야 한다. Conway's Law를 거스르면 BC 분할은 한 달 안에 무너진다.

여기서 한 가지 중요한 결정 기준을 짚어두자. James Croft가 "에이전트 = 비즈니스 capability와 매핑 — 기술 편의로 임의로 쪼개지 않는다"고 못박은 그 원칙이다(5.4절 인용). 만약 "DB Access 에이전트"나 "Cache 에이전트" 같은 게 BC 목록에 들어와 있다면 그건 잘못 자른 것이다. 그건 기술 레이어지 도메인이 아니다. 우리 6개는 모두 비즈니스 capability — "이 일을 누가 책임지는가"의 질문에 답이 되는 단위 — 로 잡혀 있다.

> **사이드바: 의료 보험 청구의 BC 분할**
> 의료 보험 청구 시스템을 같은 방식으로 자르면 어떻게 될까. (1) 청구 접수(Claim Intake) — 의료기관에서 들어온 청구를 표준 양식으로 정규화, (2) 코딩 검증(Coding Validation) — ICD/CPT 코드 정합성 검사, (3) 자격 확인(Eligibility) — 환자가 보장 대상인지 보험 가입 정보와 대조, (4) 심사·결정(Adjudication) — 보장 범위 안인지 판단, (5) 지급(Payment) — 의료기관에 송금, (6) 항소·이의(Appeals) — 거부된 청구의 재심사. 결제 게이트웨이의 6개와 놀랍게 닮았다. 코어 처리·하류 정산·이의 처리·규제 준수의 4축이 똑같이 나타난다. 도메인이 달라도 **"돈을 받고 → 정합성을 보고 → 처리하고 → 분쟁을 해소하는"** 흐름은 비슷한 BC 풍경을 만든다.

## 5단계 — Context Map을 코드로 설계

BC가 6개로 잡혔다. 마지막 단계는 이 6개 사이의 관계 — 누가 누구의 upstream인지, 어디에 ACL을 둘지, 무슨 스키마로 소통할지 — 를 그리는 것이다. 8장에서 Context Map과 ACL을 "Schema-as-Contract"와 "Semantic Firewall"로 새로 정의했다. 그 정의를 실행 가능한 코드로 옮겨보자.

먼저 관계도다.

```
[Routing & Licensing]  ─── upstream/Customer-Supplier ──→  [Payment Processing]
                                                                    │
                                                                    │ publishes events
                                                                    ▼
                                              ┌─────────────────────┴─────────────────────┐
                                              │                                           │
                                              ▼                                           ▼
                                       [Settlement]                              [Dispute & Refund]
                                                                                          │
[Compliance] ←── conformist ──── (모든 BC가 ComplianceFlag을 발행한다)                    │
                                                                                          │
[Fraud Detection] ←── partnership ──── [Payment Processing]                              │
                                                                                          │
                              외부 PG (Stripe/Toss/KCP) ── ACL ── [Payment Processing]   │
```

이 관계도가 머릿속 다이어그램으로만 남으면 6개월 후 prompt spaghetti가 된다(5장의 Siemens 사례를 기억하자). 그래서 우리는 이걸 **Pydantic 스키마로 직접 코드화**한다. Schema-as-Contract의 정신이다.

```python
# contexts/payment_processing/contracts.py
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

# === Payment Processing이 발행하는 이벤트 ===

class PaymentInitiated(BaseModel):
    """결제 처리 → (정산, 분쟁·환불, 부정거래 감지) 로 발행"""
    event_type: Literal["PaymentInitiated"] = "PaymentInitiated"
    payment_attempt_id: UUID
    merchant_id: str
    amount: Decimal = Field(..., gt=0, description="결제 시도 금액")
    currency: str = Field(..., pattern=r"^[A-Z]{3}$")
    initiated_at: datetime
    routing_decision_id: UUID  # Routing & Licensing이 내려준 결정 참조

class PaymentAuthorized(BaseModel):
    event_type: Literal["PaymentAuthorized"] = "PaymentAuthorized"
    payment_attempt_id: UUID
    authorization_code: str
    authorized_at: datetime
    fraud_score: float = Field(..., ge=0.0, le=1.0)  # Fraud Detection의 반환값

class PaymentSettled(BaseModel):
    """정산 BC가 구독, 회계 보고용"""
    event_type: Literal["PaymentSettled"] = "PaymentSettled"
    payment_id: UUID
    settlement_batch_id: UUID
    net_amount: Decimal
    settled_at: datetime
```

```python
# contexts/dispute_refund/contracts.py

class RefundRequested(BaseModel):
    event_type: Literal["RefundRequested"] = "RefundRequested"
    payment_id: UUID
    requested_amount: Decimal = Field(..., gt=0)
    reason_code: str  # ULang에 등재된 사유 코드 enum
    requested_at: datetime

class DisputeOpened(BaseModel):
    """이 이벤트가 발행되면 Payment Processing은
    해당 Payment의 Settle을 막아야 한다 (cross-BC invariant)"""
    event_type: Literal["DisputeOpened"] = "DisputeOpened"
    payment_id: UUID
    dispute_id: UUID
    opened_at: datetime
    response_deadline: datetime
```

```python
# contexts/payment_processing/acl/stripe_adapter.py
"""외부 Stripe 응답을 우리 ULang으로 번역하는 ACL.
   이 파일이 곧 Semantic Firewall이다."""

from contexts.payment_processing.contracts import PaymentAuthorized
from .stripe_raw import StripePaymentIntentResponse  # 외부 SDK 타입

def translate_stripe_to_ulang(raw: StripePaymentIntentResponse) -> PaymentAuthorized:
    # 외부 어휘 PaymentIntent.status == "succeeded" 
    # → 우리 ULang PaymentAuthorized 로 변환
    if raw.status != "succeeded":
        raise ValueError(f"Cannot translate non-success status: {raw.status}")
    
    return PaymentAuthorized(
        payment_attempt_id=UUID(raw.metadata["our_attempt_id"]),
        authorization_code=raw.charges.data[0].authorization_code,
        authorized_at=datetime.fromtimestamp(raw.created),
        fraud_score=float(raw.metadata.get("our_fraud_score", "0.0"))
    )
```

이 스키마들이 단순한 타입 정의로만 남으면 또 무너진다. 핵심은 **CI에서 자동 검증**하는 것이다.

```yaml
# .github/workflows/context-map-check.yml
name: Context Map Integrity

on: [pull_request]

jobs:
  schema-contract-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: ULang 일관성 검사
        run: |
          python scripts/check_glossary_coverage.py \
            --glossary docs/glossary.md \
            --contexts contexts/ \
            --fail-on-undefined-term
      
      - name: BC 경계 위반 검사  
        run: |
          # 한 BC가 다른 BC의 내부 모듈을 직접 import하면 실패
          python scripts/check_bc_boundaries.py \
            --allow-only contracts/ events/
      
      - name: 이벤트 스키마 호환성
        run: |
          # 새 PR이 발행 이벤트의 필드를 깨면 실패
          python scripts/check_event_schema_compat.py \
            --base origin/main
```

이 CI가 돌고 있는 한, 어떤 에이전트가 무슨 코드를 짜오더라도 ULang을 깨는 코드는 PR 단계에서 차단된다. **사람이 매번 검사하지 않아도 ULang과 BC 경계가 지켜지는 것** — 이게 8장에서 말한 Semantic Firewall의 실체다.

> **사이드바: 게임에서의 Context Map**
> MMORPG의 Context Map은 결제와 다른 풍경이다. (1) 캐릭터·인벤토리, (2) 전투·스킬, (3) 퀘스트·진행도, (4) 길드·소셜, (5) 경제·거래소, (6) 매칭·서버 배치. 가장 흥미로운 차이는 **시간 일관성 요구의 비대칭**이다. 캐릭터·인벤토리와 경제·거래소 사이는 분 단위 일관성이면 충분하지만, 전투·스킬 안에서는 밀리초 일관성이 필요하다. 그래서 게임 Context Map에서는 BC마다 다른 일관성 클래스(strong vs eventual)가 명시적으로 표기된다. 결제도 비슷한데 — 결제 처리는 strong, 정산은 daily eventual — 게임만큼 극단적이지 않을 뿐이다. 도메인의 시간 특성이 Context Map의 어노테이션에 들어간다는 것을 기억해두자.

마지막으로 외부 PG 통합의 ACL 패턴에 관한 공개 자료를 권한다. martinfowler.com의 Kief Morris와 Rahul Garg가 쓴 "Patterns for Reducing Friction in AI-Assisted Development" 계열 글들, 그리고 Iusztin의 decodingai.com "From Vibe Coding to a Six-Agent Claude Code Team"이 ACL을 어떻게 코드 레벨로 끌어내리는지 좋은 레퍼런스가 된다. 외부 SDK의 raw 타입을 그대로 도메인 모델에 흘려보내지 않는 것 — 이 작은 규율 하나가 6개월 후의 코드베이스 운명을 가른다.

## 마무리 — 종이에서 코드로 가는 다리

여기까지가 디스커버리와 전략 단계다. 이해관계자 매핑, Vibe Modeling 워크숍, ULang 정렬, BC 식별, Context Map의 코드화 — 다섯 단계를 거쳐 우리는 글로벌 결제 게이트웨이의 **종이 위 청사진**을 그렸다.

여기까지만 해도 이미 작은 회사의 한 분기 분량 작업이다. 그런데 잊지 말자. **종이는 코드가 아니다**. glossary.md, BC 다이어그램, Pydantic 스키마, CI 워크플로 — 이 모든 것이 갖춰져 있어도, 정작 첫 번째 PaymentAttempt가 들어왔을 때 어떻게 처리되는지의 코드는 아직 한 줄도 없다. invariant는 어디에서 강제되고, 사람이 어디서 개입하며, 6개 에이전트는 실제로 어떤 시스템 프롬프트로 켜지는가 — 그게 다음 장의 몫이다.

11장에서는 같은 가상 프로젝트의 **후반전**, 즉 Aggregate와 invariant의 사람 영역, Domain Event 카탈로그의 완성, ACL과 6-Agent 팀의 시스템 프롬프트 설계, 휴먼 체크포인트, 그리고 측정 지표를 운영 자산으로 만드는 일까지 다룬다. 종이가 코드로 살아나는 모습을 같이 보자.
