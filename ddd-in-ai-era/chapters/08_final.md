# 8장. Context Map과 ACL의 새로운 의미 — Schema-as-Contract와 Semantic Firewall

6개월쯤 굴린 멀티 에이전트 시스템의 프롬프트를 처음 열어 보는 순간을 상상해보자. 한 에이전트의 입력 프롬프트가 3,000 토큰이다. 거기서 도메인 로직을 추려 봤더니 고작 15% 남짓. 나머지 85%는 다른 에이전트가 토해낸 응답을 다시 파싱하고, 키 이름이 어쩌다 `function_name`이 됐는지 짐작하고, 두 번째 에이전트가 "이건 함수가 아니라 메서드인데요" 하고 따지면 다시 변환해주는 — 그런 통합 로직이다. 그걸 본 시니어가 한마디 한다. "내가 짜고 있던 게 도메인 시스템이었는지, 아니면 거대한 어댑터 한 덩어리였는지 모르겠다."

이 풍경, 어딘가 익숙하지 않은가? 마이크로서비스 초기에 우리가 겪었던 분산 spaghetti와 본질적으로 같은 모양이다. 그때 우리는 답을 알고 있었다. 컨텍스트 사이에 명시적 계약을 놓고, 컨텍스트 안에서는 자기 어휘로 자유롭게 말하게 하고, 컨텍스트 밖으로 나갈 때만 부패 방지 계층(ACL)을 통과시킨다. 그런데 어쩐 일인지 에이전트의 시대가 오자 우리는 이 답을 잊어버렸다. 더 정확히 말하면, "자연어로 시키면 되니까" 라는 환상에 잠시 흘려보냈다.

이 장에서는 두 가지를 함께 살펴보자. 첫째, 다이어그램으로만 그려지던 Context Map이 어떻게 **실행 가능한 코드**로 격상되는가. 둘째, 데이터 변환 계층에 머물러 있던 ACL이 어떻게 **의미적 방화벽(Semantic Firewall)** 으로 변신하는가. 그리고 그 변신의 끝에서, 우리가 알던 고전 Context Map 패턴들 — Customer-Supplier, Conformist, Shared Kernel, Published Language — 이 멀티 에이전트 아키텍처의 1급 시민으로 어떻게 다시 등장하는지 함께 보자.

## Context Map은 더 이상 그림이 아니다

Eric Evans가 Context Map을 그릴 때 우리에게 권한 도구는 화이트보드와 마커였다. 박스 몇 개, 화살표 몇 개, "U/D"라고 적힌 라벨 한두 개. 그 그림이 가진 가치는 분명했다 — 팀 사이의 정치적 관계를 한 눈에 보여준다. 누가 누구에게 휘둘리는지, 어느 경계가 위험한지, 누가 누구에게 무엇을 약속했는지.

그런데 그 그림에는 치명적인 약점이 있었다. **코드가 그림을 배신해도 아무도 모른다는 점이다.** 화이트보드의 "Customer-Supplier" 화살표가 코드에서는 사실 양방향 결합이어도, 그 사실을 알려면 누군가 한참 코드를 들여다본 뒤에야 깨닫는다. 그동안 그림은 거짓말을 하고 있다.

에이전트 시대에는 이 거짓말이 훨씬 빨리, 훨씬 비싸게 들통난다. 왜일까? 에이전트는 우리가 의도하지 않은 호출 시퀀스로 시스템을 두드린다. "Agents don't break systems — they expose them"이라는 Natasha Wijesekare의 표현이 정확하다. 잘못된 Context Map, 누락된 계약, 암묵적 가정 — 이런 것들을 에이전트는 자기도 모르는 사이에 매번 폭로한다. 시스템이 caller의 점잖음에 기대고 있었다면 에이전트는 그 점잖음을 가차 없이 깨뜨린다.

그래서 Siemens의 Nikita Golovko가 제안한 길은 이렇다. **Context Map을 다이어그램이 아니라 실행 가능한 코드로 적자.** upstream/downstream 관계, 계약 버전, 어댑터 구현체를 코드로 명시하고, CI 파이프라인에서 검증한다. 그림이 거짓말을 하면 빌드가 깨지게 한다.

구체적으로 어떤 모양일까? 가장 단순하게는 이렇게 시작할 수 있다.

```python
# context_map/inventory_to_order.py
from pydantic import BaseModel
from typing import Literal

class InventoryContextMap(BaseModel):
    """Inventory BC와 Order BC 사이의 관계를 코드로 기술"""

    upstream: Literal["inventory"] = "inventory"
    downstream: Literal["order"] = "order"

    relationship: Literal["customer-supplier"] = "customer-supplier"
    # downstream(order)이 upstream(inventory)에 영향을 줄 수 있는 관계.
    # Conformist였다면 downstream이 upstream에 일방적으로 맞춘다.

    contract_version: str = "2.3.0"
    contract_schema: str = "schemas/inventory_v2_3_0.json"
    adapter_module: str = "adapters.inventory_v2_3_0"

    # 이 관계의 SLA — 응답 지연, 가용성 목표
    sla_p95_ms: int = 300
    sla_availability: float = 0.995
```

이 작은 파일 한 장이 무엇을 가능하게 하는가? CI에서 "현재 사용 중인 어댑터가 정말 `inventory_v2_3_0`인가", "스키마 파일이 존재하는가", "downstream이 upstream의 새 버전을 따라가지 못하고 있는가" 같은 질문을 **사람이 아니라 빌드 파이프라인이** 물어보게 된다. 그림이 거짓말을 하는 시간이 0에 수렴한다.

물론 모든 컨텍스트 관계를 처음부터 이렇게 정밀하게 기술할 필요는 없다. 시작은 단순하게 — 가장 자주 깨지는 한두 개의 경계부터, BC 사이의 "이 관계가 무엇인가"를 코드 한 줄로 적는 데서 출발하는 편이 낫다. 그림이 부족했던 게 아니라, 그림이 코드와 분리돼 살았던 게 문제였다는 점을 기억해두자.

## Schema-as-Contract — 자연어 API를 폐기하자

Context Map이 관계의 지도라면, 그 위에 흐르는 실제 메시지는 무엇으로 적을 것인가? Golovko가 한 줄로 답한다. "자연어가 아니라 스키마로."

자연어 API의 문제를 잠시 짚어보자. 한 에이전트가 다른 에이전트에게 이렇게 말한다고 해보자.

> "주문 ABC-123의 상태를 알려줘. 가능하면 결제 정보도 같이."

받은 에이전트는 무엇을 돌려줘야 할까? JSON? 자연어 문장? "결제 정보"의 범위는 어디까지인가 — 결제 수단인가, 금액인가, 트랜잭션 ID인가? 두 에이전트가 같은 회사 사람이라도 이 모호함은 회의 한 번으로 해결된다. 그런데 두 에이전트가 LLM이라면? 매번 다르게 해석한다. 어떤 날은 결제 수단만 주고, 어떤 날은 트랜잭션 로그까지 주고, 어떤 날은 "결제 정보는 별도 API를 사용하세요"라고 거절한다. 받은 쪽은 그걸 또 다 파싱해야 한다. 토큰의 85%가 파싱 로직이 되는 길은 여기서 시작된다.

그래서 Pydantic이든 JSON Schema든 — 도구는 무엇이든 상관없다 — **에이전트 사이에 흐르는 메시지를 정형 스키마로 못박는 편이 낫다.**

```python
# schemas/inventory_v2_3_0.py
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class ReservationRequest(BaseModel):
    """Order BC가 Inventory BC에 보내는 재고 예약 요청"""
    schema_version: Literal["2.3.0"] = "2.3.0"
    order_id: str = Field(..., pattern=r"^ORD-\d{8}$")
    sku: str
    quantity: int = Field(..., gt=0)
    reserve_until: datetime

class ReservationResult(BaseModel):
    """Inventory BC가 Order BC에 돌려주는 결과"""
    schema_version: Literal["2.3.0"] = "2.3.0"
    status: Literal["reserved", "out_of_stock", "partial"]
    reservation_id: str | None = None
    reserved_quantity: int = 0
    expires_at: datetime | None = None
```

이 짧은 코드가 가져오는 것들을 하나씩 짚어보자.

**첫째, 검증이 무료다.** Pydantic이 들어오는 메시지를 자동으로 검증한다. `quantity=-1`이 들어오면 그 메시지는 도메인 로직에 닿기도 전에 차단된다. LLM이 가끔 토해내는 헛소리를 도메인 안쪽에서 다시 한번 의심할 필요가 없다.

**둘째, 버저닝이 명시적이다.** `schema_version: Literal["2.3.0"]` 한 줄이 있어서, 누가 어떤 버전을 쓰는지 코드가 안다. Inventory가 2.4.0으로 올라갔는데 Order가 아직 2.3.0이면, 그 어긋남이 빌드 시점에 드러난다.

**셋째, 셀프 도큐먼테이션이다.** `ReservationResult.model_json_schema()` 한 줄이면 JSON Schema가 떨어진다. 그걸 OpenAPI로, Markdown으로, 또는 다른 에이전트의 시스템 프롬프트로 그대로 흘려보낼 수 있다. "이 에이전트에게 뭘 보내면 되나요?"라는 질문에 답할 살아있는 사양이 코드로 존재한다.

**넷째, 에이전트의 프롬프트가 얇아진다.** Golovko가 측정한 수치를 다시 보자. 3,000+ 토큰의 85%가 파싱 spaghetti였던 에이전트가, 4개 패턴을 적용한 뒤 500 토큰에 90%가 도메인 로직이 됐다. 6배 가까운 다이어트다. 이 다이어트가 비용·지연·정확도에 직접 효과를 낸다는 점은 굳이 별도 그래프를 그리지 않아도 짐작할 만하다.

물론 단점도 있다. 스키마를 너무 엄격하게 못박으면 에이전트가 자기 추론으로 보태려는 좋은 정보가 잘려나간다. 너무 느슨하게 두면 다시 spaghetti로 회귀한다. 균형점은 도메인마다 다르지만, 한 가지 휴리스틱은 분명하다 — **에이전트 사이의 "약속"에 해당하는 메시지는 엄격하게, 에이전트 안에서의 자기 추론은 자유롭게 두자.** 약속은 계약이고, 추론은 작업장이다.

## ACL은 데이터 변환을 넘어 의미 변환으로

자, 이제 또 하나의 고전 패턴을 꺼내보자. Anti-Corruption Layer. 한국어로는 "부패 방지 계층"으로 옮긴다. Evans가 이 패턴을 처음 소개했을 때 떠올린 그림은 단순했다 — 우리 도메인의 깨끗한 모델이 외부 레거시 시스템의 어휘에 오염되지 않도록, 사이에 변환 계층을 두자. 데이터 모델의 충돌을 흡수하는 완충재였다.

에이전트 시대에 이 패턴의 의미가 한 단계 진화한다. **이제 ACL은 데이터를 변환하는 게 아니라 의미를 변환한다.** Golovko가 든 예시 하나가 절묘하다. "function"이라는 단어가 코드 생성 에이전트에게는 무엇을 뜻할까? 시그니처와 구현이다. 그러면 테스팅 에이전트에게는? behavior contract다. 두 에이전트는 같은 단어를 쓰지만 머릿속에 떠올리는 게 전혀 다르다.

이런 어휘 충돌을 그대로 두면 어떻게 되는가? 코드 생성 에이전트가 "function done"이라고 알리면, 테스팅 에이전트는 "아, 행위 계약이 정해졌으니 그 계약을 검증할 케이스를 만들어야지"라고 해석한다. 그런데 코드 생성 에이전트는 "구현까지 다 됐다는 뜻이었는데?"라고 어리둥절해 한다. 미묘하지만, 운영에 들어가면 매번 사고를 부르는 종류의 어긋남이다. 찜찜한 일이다.

그래서 등장하는 게 의미적 방화벽으로서의 ACL이다. 두 에이전트 사이에 한 겹의 어댑터를 두고, 한쪽의 어휘를 다른 쪽의 어휘로 **번역**한다.

```python
# acl/code_to_test.py
from schemas.codegen_v1 import FunctionImplementation
from schemas.testing_v1 import BehaviorContract, BehaviorClause

class CodeToTestACL:
    """코드 생성 BC의 'function' → 테스팅 BC의 'behavior contract' 변환"""

    def translate(self, impl: FunctionImplementation) -> BehaviorContract:
        # 코드 생성 쪽에서 'function'은 signature + implementation
        # 테스팅 쪽에서 'function'은 검증해야 할 behavior clause 집합

        clauses = [
            BehaviorClause(
                given=case.precondition,
                when=f"{impl.signature.name}({case.input_repr})",
                then=case.expected_output_repr,
            )
            for case in impl.documented_examples
        ]

        # 시그니처의 타입 힌트를 invariant clause로 추가
        for param in impl.signature.parameters:
            if param.constraints:
                clauses.append(
                    BehaviorClause(
                        given=f"{param.name} 입력",
                        when=f"호출 시점",
                        then=f"{param.name} 제약 {param.constraints} 충족"
                    )
                )

        return BehaviorContract(
            function_id=impl.signature.qualified_name,
            clauses=clauses,
            source_version=impl.version,
        )
```

이 어댑터가 하는 일은 데이터 키 이름을 바꾸는 게 아니다. **개념을 번역한다.** 코드 생성 BC 안에서는 "function = 시그니처 + 구현"이라는 어휘로 자유롭게 산다. 테스팅 BC 안에서는 "function = 검증할 행위 절들의 모음"이라는 어휘로 산다. 두 컨텍스트 모두 자기 어휘를 포기하지 않는다. 둘 사이의 어댑터만이 양쪽 어휘를 모두 안다.

이렇게 두면 무엇이 좋은가? 한쪽 BC가 어휘를 바꿔도 다른 쪽이 흔들리지 않는다. 코드 생성 BC가 내일 "function" 대신 "callable unit"이라고 부르기 시작해도, 테스팅 BC는 그 사실을 알 필요가 없다. ACL이 그 사이에서 흡수한다. Bounded Context의 본래 약속 — "내 컨텍스트 안에서는 내 어휘로 산다" — 이 에이전트 시대에 다시 1급 시민이 된다.

여기서 한 가지 휴리스틱을 짚고 가자. **ACL이 필요한 경계를 어떻게 알아채는가?** 두 BC 사이에서 같은 단어를 다르게 쓰는 게 발견되는 순간, 그 자리가 ACL의 자리다. 회의 중에 누군가 "잠깐, 그쪽이 말하는 X는 우리 쪽의 Y랑 같은 건가요?"라고 묻는 순간 — 그 순간이 단서다. 그 순간을 놓치면 그 모호함이 코드에 침투하고, 에이전트가 그 모호함을 매번 다르게 해석하면서 시스템 곳곳에서 잔잔히 폭발한다.

## 고전 Context Map 패턴이 다시 살아난다

여기까지 오면 자연스러운 질문이 떠오른다. **Evans가 정리한 고전 Context Map 패턴들 — Customer-Supplier, Conformist, Shared Kernel, Published Language, Partnership, Separate Ways — 이게 에이전트 간 관계에 그대로 매핑되는가?** 답은 "놀랍도록 자연스럽게 매핑된다"이다. 함께 짚어보자.

**Customer-Supplier.** Downstream(Customer)이 Upstream(Supplier)에게 "이런 데이터가 필요하다"라고 요구하고, Upstream이 그 요구를 받아들여 자기 출력에 반영한다. 에이전트 세계로 옮기면 — Order 에이전트가 Inventory 에이전트에게 "예약 결과에 expires_at 필드가 필요하다"라고 요청하고, Inventory 에이전트의 스키마가 거기 맞춰 진화한다. 두 에이전트 팀(또는 두 사람)이 같은 회사 안에 있고 협력 의지가 있을 때 자연스러운 모델이다.

**Conformist.** Downstream이 Upstream에 일방적으로 맞춘다. Upstream이 외부 회사거나, 협상력이 없을 때다. 에이전트 세계로 옮기면 — 외부 LLM API(OpenAI, Anthropic)나 외부 검색 API에 우리 에이전트가 일방적으로 맞추는 관계다. 이때는 ACL을 두는 게 거의 필수다. 외부의 어휘를 그대로 우리 도메인으로 끌고 들어오면 외부의 변화가 우리 도메인을 뒤흔든다.

**Shared Kernel.** 두 BC가 공유하는 작은 핵심 모델을 함께 소유하고, 변경에는 양쪽 합의가 필요하다. 에이전트 세계에서는 — 공통 도메인 글로사리(`docs/glossary.md`), 공유 스키마 모듈, 또는 양쪽 에이전트가 함께 의존하는 공통 unit 정의가 여기 해당한다. Iusztin이 PM 에이전트에게 글로사리 유지 권한을 준 것은 정확히 이 Shared Kernel을 한 곳에서 관리하기 위한 셋업이다.

**Published Language.** 잘 정의되고 문서화된 공용 언어를 통해 통신한다. 에이전트 세계로 옮기면 — JSON Schema, OpenAPI 사양, MCP(Model Context Protocol)가 이 자리다. 모두가 약속한 형식이고, 누구든 그 형식을 따르면 끼어들 수 있다. Schema-as-Contract 패턴이 사실 이 Published Language의 현대적 구현이다.

**Partnership.** 두 BC가 운명을 함께 한다. 한쪽이 실패하면 다른 쪽도 의미가 없는 관계. 에이전트 세계에서는 PM 에이전트와 SWE 에이전트의 관계가 비슷하다 — PM이 작업을 잘 쪼개지 못하면 SWE의 산출물이 쓸모없고, SWE가 산출을 못하면 PM의 계획이 종이쪼가리가 된다.

**Separate Ways.** 통합하지 않는다. 그냥 따로 산다. 에이전트 세계에서도 의외로 자주 등장한다 — "이 에이전트와 저 에이전트는 통합할 가치가 없다, 사람이 중간에서 옮긴다." 통합 비용보다 분리 비용이 낮은 영역이 분명히 있다는 사실을 잊지 말자.

이 매핑을 좀 더 넓혀보자. arXiv 2601.12560(Agentic AI 아키텍처 분류)이 정리한 멀티 에이전트 토폴로지 — chain, star, mesh, workflow graph — 도 Context Map의 다른 얼굴이다. 표 하나로 옮겨보자.

| 에이전트 토폴로지 | 대응하는 Context Map 패턴 |
|---|---|
| **Chain** (선형 파이프라인) | Customer-Supplier 연쇄. 앞단이 뒷단의 Supplier. |
| **Star** (허브 1개 + spoke n개) | 허브가 Published Language를 발행, 스포크는 Conformist. |
| **Mesh** (전체 연결) | Partnership 또는 Shared Kernel이 다수 BC 사이에 펼쳐진 형태. |
| **Workflow Graph** (조건부 분기) | Customer-Supplier + 일부 Separate Ways의 혼합. |

이 표가 말해주는 건 분명하다. **에이전트 토폴로지를 처음 설계할 때, 우리는 사실 Context Map을 그리고 있다.** 토폴로지가 곧 정치 구조다. 그러니 "이 에이전트들을 어떻게 엮을까"를 결정할 때, 25년간 쌓인 Context Map의 휴리스틱을 그냥 가져다 쓰지 않을 이유가 없다.

## 카카오 헤어샵을 다시 본다

여기서 한 한국 사례를 짚고 가자. 2018년 카카오 헤어샵 팀이 남긴 도메인 모델링 기록이다. 그 팀은 예약 상태 enum을 비즈니스 운영진의 어휘 그대로 코드에 흡수했다 — READY, OK, CANCELED, WAIT_CANCEL, COMPLETED, NO_SHOW. 회의실에서 운영진이 쓰던 말이 그대로 자바 코드에 들어갔다. Ubiquitous Language의 한국형 표본이라 할 만하다.

다만 한 가지 한계가 기록에 정직하게 남아 있다. **Bounded Context를 완전히 못 나누고 패키지 기반 분할에 머물렀다는 점이다.** 같은 DAO를 여러 컨텍스트가 공유했다. 즉, 코드 안에서는 어휘가 통일됐지만, 컨텍스트의 정치적 경계는 흐릿했다.

이 사례를 ACL의 관점에서 다시 보면 흥미로운 그림이 나온다. ACL이 없었다는 건 두 얼굴을 가진다.

**좋은 면.** 같은 단어가 코드 곳곳에서 같은 뜻으로 통했다. 운영진의 "노쇼"가 그대로 `NO_SHOW`가 되고, 그 enum이 시스템 어디에서나 같은 의미였다. 작은 도메인에서 ACL을 두지 않은 선택은 비용 대비 효율이 좋다 — 작은 회사가 매번 어휘 번역 계층을 두는 건 ceremony 과잉이다.

**나쁜 면.** 도메인이 커지면 같은 단어가 컨텍스트마다 미묘하게 다른 의미를 갖기 시작한다. "예약"이 고객 화면의 예약과 미용사 스케줄의 예약과 정산 시스템의 예약이 다 같은 단어를 쓰지만, 안에 담긴 책임과 invariant가 다르다. 이 시점에 ACL이 없으면 같은 DAO가 모든 컨텍스트의 짐을 다 짊어진다. 그 DAO가 무거워질수록 변경의 두려움이 커진다. 끔찍한 일이다.

오늘 같은 도메인을 다시 시작한다면, 어떻게 설계할 수 있을까? Iusztin 식의 6-에이전트 팀을 가정하면 — PM 에이전트가 글로사리에 `Reservation`, `Schedule`, `Settlement.ReservationRef` 같은 어휘를 등재하고, 각 BC를 하나의 에이전트에 매핑하고, BC 사이에는 Schema-as-Contract와 ACL을 둔다. 같은 "예약"이라는 한국어 단어를 쓰더라도 각 컨텍스트의 스키마 이름이 다르고, ACL이 그 사이의 번역을 담당한다.

이게 카카오 헤어샵의 한계를 부정하는 얘기가 아니다. 2018년의 그 선택은 그 시기 그 팀의 상황에서 합리적이었다. 우리가 배울 점은 — **ACL이 비싸 보일 때조차도, "지금은 같은 단어가 같은 뜻이지만, 6개월 뒤에도 그럴까?"를 한 번씩 묻는 습관**이다. 에이전트가 끼면 이 6개월이 6주로 줄어든다는 점만 더하면 된다.

## 계약 테스트 — 스키마가 변할 때 누가 검증하나

여기까지 와서 한 가지 질문이 따라붙는다. **스키마와 ACL이 코드로 살아있다는 건 알겠다. 그런데 그게 변할 때, 누가 어떻게 검증하나?** 이 질문은 7장에서 살펴본 테스트 위계의 BC 간 짝이라 할 수 있다.

7장에서 우리는 사람·AI·테스터 에이전트의 분업을 정리했다. 사람이 invariant 단위 테스트를 작성하고, AI가 적대적 케이스를 생성하고, 테스터 에이전트가 E2E를 돌린다. 그 위계는 한 BC 안에서의 테스트 책임 분담이었다. 그런데 BC 사이의 계약은 어떻게 검증하는가? 답은 **계약 테스트(contract test)** 다.

계약 테스트의 발상은 단순하다. **Provider(공급자)와 Consumer(소비자)가 각자 "내가 이런 계약을 지킨다/요구한다"라는 사양을 코드로 남기고, CI에서 둘이 일치하는지 자동으로 검증한다.** Pact 같은 도구가 잘 알려져 있지만, 도구를 굳이 쓰지 않더라도 핵심 발상은 그대로 적용할 수 있다.

```python
# tests/contract/test_inventory_reservation_contract.py
from schemas.inventory_v2_3_0 import ReservationRequest, ReservationResult

def test_consumer_order_can_construct_valid_request():
    """Order BC(소비자)가 Inventory에 보낼 메시지를 만들 수 있는가"""
    req = ReservationRequest(
        order_id="ORD-20260517",
        sku="HAIR-CUT-30",
        quantity=1,
        reserve_until="2026-05-17T15:00:00",
    )
    # 소비자 쪽 코드가 이 스키마로 메시지를 빚을 수 있어야 한다.
    assert req.schema_version == "2.3.0"

def test_provider_inventory_can_respond_with_all_branches():
    """Inventory BC(공급자)가 약속한 모든 상태로 응답할 수 있는가"""
    for status in ("reserved", "out_of_stock", "partial"):
        result = ReservationResult(status=status)
        # 공급자가 약속한 모든 분기를 만들 수 있어야 한다.
        assert result.status == status

def test_acl_translates_between_versions():
    """v2.3.0 응답을 v2.2.0 어휘로 변환하는 ACL이 작동하는가"""
    new = ReservationResult(status="partial", reserved_quantity=2)
    legacy = LegacyReservationAdapter().to_v2_2_0(new)
    # partial은 v2.2.0에 없으므로 reserved+경고로 매핑됐는지 검증
    assert legacy.status == "reserved"
    assert "partial_warning" in legacy.flags
```

여기서 누가 무엇을 책임지는가의 분업표를 다시 한번 그어보자.

| 책임 | 누가 |
|---|---|
| **스키마 정의** | 사람 (BC 소유 팀이 합의) |
| **소비자 측 계약 테스트 작성** | 사람 + AI 보조 |
| **공급자 측 계약 테스트 작성** | 사람 + AI 보조 |
| **ACL의 변환 로직 테스트** | 사람 (이게 가장 미묘함) |
| **스키마 변경의 영향 분석** | AI가 1차 스캔, 사람이 결정 |
| **CI 통합·실행** | 자동화 (테스터 에이전트 또는 단순 CI) |

특히 **ACL의 변환 로직 테스트는 사람이 직접 작성하는 편이 낫다.** 왜냐하면 ACL이 다루는 건 의미의 번역이고, 의미는 도메인 전문가의 머릿속에 있기 때문이다. AI가 "v2.3.0의 `partial`을 v2.2.0에서 어떻게 표현해야 하나?"를 알리 없다. 그건 도메인 결정이다.

계약 테스트가 도입되면 한 가지 안심거리가 생긴다. **스키마 변경이 silent failure로 이어지지 않는다.** Inventory 팀이 v2.4.0으로 올리면서 `expires_at` 필드를 옵셔널로 바꿨다고 해보자. Order 팀의 계약 테스트가 즉시 깨진다. 깨지는 게 좋은 일이라는 점을 기억해두자 — 운영에서 깨지는 것보다 CI에서 깨지는 게 백 배 낫다.

## 실행 패턴 — 월요일에 무엇을 할 것인가

여기까지 개념을 함께 풀었다. 이제 손에 잡히는 실행 패턴으로 옮겨보자. "내 시스템의 에이전트들이 자연어로 대화하던 부분을 어디부터 schema로 바꿀 것인가"의 우선순위 — 이 질문에 답해보자.

**1단계. 가장 자주 깨지는 한 경계를 고르자.** 지금 운영 중인 멀티 에이전트 시스템에서, 디버깅 시간을 가장 많이 쓰게 하는 BC 간 메시지가 있을 것이다. "어제도 이 두 에이전트 사이에서 응답 파싱이 깨졌지"라는 그 자리. 거기서 시작하자. 전체를 한 번에 바꾸려 들면 다 못 끝낸다.

**2단계. 그 자리의 메시지를 Pydantic 모델로 적자.** 이미 양쪽 에이전트가 주고받던 메시지의 평균적 모양을 보면서, 가장 안정적인 필드만 먼저 적는다. 처음부터 완벽하게 만들려 하지 말자. v0.1.0으로 시작해도 좋다.

**3단계. 양쪽 에이전트의 프롬프트에서 그 메시지에 해당하는 자연어 지시를 제거하자.** "JSON으로 답해, 필드는 status, reservation_id, …" 같은 장황한 지시가 사라진다. 대신 `ReservationResult.model_json_schema()`를 시스템 프롬프트의 앞부분에 박는다. LLM은 JSON Schema를 의외로 잘 따른다.

**4단계. 계약 테스트 한 줄을 추가하자.** 소비자가 메시지를 만들 수 있는지, 공급자가 약속한 모든 분기로 응답할 수 있는지 — 이 두 가지만 먼저. 완벽한 테스트 스위트는 나중에.

**5단계. ACL이 필요한지 판단하자.** 두 BC 사이에서 같은 단어가 다른 의미로 쓰이는 게 발견되면 ACL을 둔다. 발견되지 않으면 두지 않는다. 모든 경계에 ACL을 두는 건 ceremony 과잉이다.

**6단계. 버저닝 전략을 정하자.** Semantic Versioning을 권한다. Breaking change는 major bump. 양쪽 BC가 다른 버전을 동시에 지원해야 하는 기간은 항상 발생하므로, 그 기간 동안의 ACL(또는 multi-version adapter)을 어떻게 둘지 미리 정해두자.

**7단계. 다음 경계로 이동하자.** 한 경계가 안정되면 다음으로. 점진적 마이그레이션이 정답이다.

이 7단계를 한 문장으로 요약하면 이렇다 — **가장 자주 깨지는 경계에서 시작해, 메시지를 스키마로 못박고, 계약 테스트로 보호하고, 필요한 곳에만 ACL을 두자.**

## 한계 — 너무 엄격해도, 너무 느슨해도

물론 이 모든 게 만능은 아니다. Schema-as-Contract와 ACL이 가져오는 두 가지 위험을 정직하게 짚자.

**첫째, 너무 엄격하면 에이전트의 자유도가 줄어든다.** LLM이 자기 추론으로 보태려는 좋은 정보가 잘려나간다. 예를 들어 Inventory 에이전트가 "재고가 부족하지만 비슷한 SKU가 있다"라는 정보를 알려주고 싶을 때, 스키마에 그 필드가 없으면 그 정보는 버려진다. 스키마는 약속이지만, 그 약속이 너무 빡빡하면 에이전트의 reasoning이 흘러나갈 통로가 막힌다.

**둘째, 너무 느슨하면 spaghetti로 회귀한다.** "그래도 LLM이 가끔 도움 되는 추가 정보를 주니까" 하면서 `additional_info: dict[str, Any]` 같은 필드를 두기 시작하면, 그 필드를 통해 모든 spaghetti가 다시 들어온다. 6개월 뒤에 그 필드 안에 뭐가 들어 있는지 아무도 모른다.

균형점은 어디인가? 한 가지 권할 만한 휴리스틱은 — **약속에 해당하는 핵심 필드는 엄격하게 못박되, 부가 정보 채널을 명시적으로 한두 개 열어두자.** 예를 들어 `reasoning_notes: list[str] | None`처럼, "이건 부가 정보이고, 비결정적이고, 로깅용이다"라는 의도가 분명한 필드를 둔다. 도메인 결정은 핵심 필드로만 내리고, reasoning_notes는 모니터링과 디버깅의 단서로만 쓴다. 이렇게 두면 엄격함과 유연함이 한 스키마 안에서 공존한다.

또 한 가지 한계 — **모든 경계에 정형 계약을 두는 게 항상 옳지는 않다.** 도메인이 아주 작고, 에이전트가 두세 개뿐이고, 어휘 충돌이 거의 없는 시스템에서는 카카오 헤어샵의 초기 선택처럼 ACL 없이 사는 게 합리적일 수 있다. 도구를 도구로 쓰자. 시스템이 작을 때는 ceremony보다 속도가, 시스템이 커지면 ceremony가 속도를 만든다.

## 마무리

다이어그램이던 Context Map은 이제 코드가 된다. 데이터 변환 계층이던 ACL은 이제 의미적 방화벽이 된다. 자연어로 흘리던 에이전트 간 메시지는 이제 스키마로 못박힌다. 이 세 가지 변신은 새로운 발명이 아니다. 우리가 25년간 쌓아 온 Context Map의 지혜를, 에이전트의 시대가 다시 1급 시민으로 끌어올린 것뿐이다.

월요일 출근해서 무엇부터 할 수 있을까? 가장 자주 깨지는 한 경계 — 그 자리의 메시지를 Pydantic 모델 하나로 적어보자. 양쪽 에이전트의 프롬프트에서 그 메시지에 해당하는 자연어 지시 한 줄을 지우고, 스키마로 대체해보자. 계약 테스트 한 줄을 적어보자. 이 작은 변화 하나가, 6개월 뒤의 prompt spaghetti를 미리 차단한다. Golovko가 인용한 문장이 정확하다 — "시작하기 가장 좋은 때는 6개월 전이었다. 두 번째로 좋은 때는 월요일이다."

그리고 한 가지 더 기억해두자. **에이전트가 자연어로 대화하던 자리에 스키마를 놓는 것은, 에이전트의 지능을 의심하는 게 아니라 그 지능을 더 좋은 일에 쓰게 하는 것이다.** 파싱과 통합에 85%의 토큰을 쓰던 에이전트가 도메인 로직에 90%를 쓰게 되는 그 순간, 우리가 처음 멀티 에이전트 시스템을 꿈꿨을 때의 그림이 비로소 시야에 들어온다.

다음 장에서는 한 발 더 나아가보자. 에이전트 간 메시지가 스키마로 정형화되면, 그 메시지의 흐름이 곧 **Domain Event**의 흐름이 된다. 한 번도 제대로 도입해보지 못했던 Event Storming을 AI 도구의 도움으로 다시 열어볼 시점이다. Vibe modeling이 vibe coding의 위험을 줄이는 사전 단계로 어떻게 부활했는지 — 그 이야기로 자연스럽게 넘어가자.
