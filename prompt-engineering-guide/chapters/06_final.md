# 6장. 구조화 출력과 도구 사용 — 말고 받는 법

```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

금요일 오후 6시, 프로덕션 로그에 이 한 줄이 찍히는 순간을 상상해보자. 한참을 되짚어 보니 원인은 단순했다. LLM이 `Sure! Here's the JSON you requested:`라고 친절하게 한 문장 덧붙인 뒤에 JSON을 내놓은 것이다. 파서는 첫 글자에서부터 무너졌고, 티켓은 쌓였다. 난감하다. 이런 사고는 한 번 겪어 보면 꽤 오래 찜찜하게 남는다.

그런데 사실 이 문제는 2024년 들어 세 공급사가 이미 함께 풀어 둔 영역이다. OpenAI는 Structured Outputs(strict JSON schema)로, Anthropic은 tool_use로, Google은 responseSchema로 같은 고민에 답을 냈다. 라이브러리 쪽에도 Instructor, BAML, Outlines 같은 도구가 자리 잡았다. 즉, 2026년의 우리는 더 이상 `"Sure! Here's the JSON:"` 같은 접두어와 씨름할 필요가 없다. 그런데도 아직 많은 팀이 구식 프롬프트와 정규식 파서를 붙들고 있다. 이 장에서는 그 월요일 아침을 없애는 데 필요한 도구와 프롬프트 습관을 하나씩 정리해보자.

5장에서 우리는 RAG로 모델이 아는 것을 정확히 말하게 하는 법을 살폈다. 이제는 모델이 말한 것을 **기계가 소비할 수 있는 모양으로 받아내는** 법이 남았다. 컨텍스트를 집어넣는 쪽과 꺼내는 쪽, 두 방향이 모두 구조화되어야 시스템이 비로소 완성된다.

## 자유 텍스트는 왜 위험한가

LLM이 내놓는 자연어는 사람이 읽기엔 좋지만 기계가 소비하기엔 까다롭다. "응답을 JSON으로 주세요"라고 정중히 부탁하는 것만으로는 부족하다. 모델은 친절한 성격이라 서두에 해설을 붙이기도 하고, 코드 블록으로 감싸기도 하고, 한 번씩 trailing comma를 흘리기도 한다. 때로는 필드명을 살짝 바꿔 적는다. 스키마에 없는 필드를 창작해서 넣기도 한다. 이걸 파싱 단에서 일일이 구제하려 들면 정규식과 예외 처리로 코드가 두툼해지고, 그 자체가 버그의 온상이 된다. 번거롭다.

조금 더 구체적으로 자유 텍스트 시대의 실패 모드를 꼽아보자.

- **Preface 오염:** `"Sure! Here's the JSON:"` 같은 접두어 혹은 `"Let me know if you need anything else!"` 같은 후미사.
- **코드 펜스 포장:** 응답 전체가 ` ```json ... ``` `로 감싸져 오는 케이스. 파싱 전 fence 제거가 또 하나의 루틴이 된다.
- **Schema violation:** 필수 필드 누락, 필드명 변형(`user_name` → `username`), 타입 어긋남(`int`를 문자열로 내려주기).
- **Hallucinated field:** 스키마에 없는 `confidence` 같은 필드를 멋대로 붙이는 일. 무해해 보이지만 downstream 코드를 깨뜨린다.
- **Truncation:** 토큰 한도에 걸려 JSON이 중간에서 잘림. `}` 하나가 사라져 전체가 부서진다.

이런 실패는 한두 번이면 패치로 때우지만, 하루 수만 건을 돌리는 서비스에선 노이즈로 누적된다. **자유 텍스트의 유연함은 프로덕션에선 비용**이다. 그렇다면 어떻게 해야 할까? 두 가지 길이 있다. 하나는 **프롬프트 레벨의 구조화**이고, 다른 하나는 **디코더 레벨의 구조화**다. 좋은 시스템은 둘을 겹쳐 쓴다.

## 프롬프트로 구조를 미리 심어두기

디코더를 건드리기 전에, 프롬프트만으로도 꽤 많은 것을 잡을 수 있다. 원리는 단순하다. 모델에게 **형태**를 미리 보여 주면 모델은 그 형태를 흉내 낸다. 이걸 세 가지 장치로 나눠 정리해보자.

### XML 태그로 입력·출력을 구획한다

Claude 계열에서 특히 효과가 좋은 습관이다. `<document>...</document>`, `<task>...</task>`, `<output_format>...</output_format>` 같은 태그로 프롬프트를 구획하면 모델이 어느 부분이 참고 데이터이고 어느 부분이 지시인지 명확히 구분한다. Anthropic 공식 문서가 강하게 권장하는 패턴이기도 하다.

```xml
<document>
From: customer@example.com
Subject: 반품이 안 되는데요

주문번호 #48211로 어제 받은 후드 티셔츠가
사이즈가 안 맞아서 반품 신청을 하려는데
앱에서 버튼이 비활성화돼 있어요. 도와주세요.
</document>

<task>
위 이메일을 읽고 지원 티켓으로 변환하라.
</task>

<output_format>
<ticket>
  <priority>low|medium|high</priority>
  <category>billing|shipping|product|account|other</category>
  <summary>한 문장 요약</summary>
  <customer_email>이메일 주소</customer_email>
</ticket>
</output_format>
```

모델이 `<ticket>` 시작 태그만 찾아 열면 나머지 파싱은 상당히 안정적으로 흘러간다. Claude뿐 아니라 GPT, Gemini도 이 형식을 그럭저럭 잘 따른다. 멀티-모델을 지원하는 제품이라면 XML+Markdown 하이브리드 템플릿으로 두는 편이 낫다.

### JSON 예시를 1~2개 박아 둔다

Few-shot이 포맷 학습에 특히 강하다는 건 오래된 경험칙이다. 지시문만으로 설명하는 것보다, 기대 형태를 한두 번 보여 주는 쪽이 훨씬 잘 먹힌다.

```
다음 이메일을 지원 티켓 JSON으로 변환하라.

예시:
입력: "카드 결제가 두 번 됐어요"
출력:
{
  "priority": "high",
  "category": "billing",
  "summary": "중복 결제 환불 요청",
  "customer_email": "<추출된 이메일>"
}

이제 다음 이메일을 같은 형식으로 변환하라:
<이메일>
```

한 가지 잊지 말아야 할 것이 있다. **예시에 나오지 않은 값은 모델이 흉내 내지 못한다는 사실**이다. `priority`에 `high`, `medium`만 보여 주면 `low`는 거의 안 쓴다. 예시의 분포가 실제 분포를 대표해야 한다. 이건 5장에서 RAG 예시를 고를 때 했던 고민과 정확히 같은 문제다.

### Pydantic/Zod로 프롬프트와 코드를 하나로 묶는다

여기서부터가 재밌어진다. Python이라면 `pydantic`, TypeScript라면 `zod`로 스키마를 정의해 두고, 이 스키마를 프롬프트에 자동으로 투영하는 것이다. 스키마 정의가 그대로 **타입 안전한 데이터 클래스**가 되면서, 동시에 **프롬프트의 일부**가 된다. Instructor, BAML, LangChain structured output이 모두 이 아이디어의 변형이다.

```python
from pydantic import BaseModel, Field
from typing import Literal

class SupportTicket(BaseModel):
    priority: Literal["low", "medium", "high"] = Field(
        description="긴급도. 결제·보안 이슈는 high, 단순 문의는 low."
    )
    category: Literal["billing", "shipping", "product", "account", "other"] = Field(
        description="티켓 분류."
    )
    summary: str = Field(
        description="한 문장 요약. 20자 이상 80자 이하."
    )
    customer_email: str = Field(description="고객의 이메일 주소.")
```

여기서 `description`이 단순한 주석이 아니라는 점을 기억해두자. 대부분의 라이브러리가 이 `description`을 그대로 프롬프트에 실어 모델에게 전달한다. **스키마가 문서가 되고 문서가 프롬프트가 되는 구조**다. 필드명을 `p`, `c` 같이 줄이지 말고 의미 있는 이름으로 두라는 권고도 같은 맥락이다. 모델은 필드명을 **읽어서** 의미를 유추한다.

## 디코더 레벨 구조화 — 세 공급사의 접근

프롬프트만으로도 꽤 가지만, 100% 보장은 디코더 쪽에서 온다. 세 공급사가 각자의 방식으로 이걸 푼다.

### OpenAI Structured Outputs — strict 모드

2024년 8월 OpenAI가 `response_format={"type": "json_schema", "strict": true}`를 공개했다. 이 모드는 JSON 스키마를 100% 준수한다고 공식 블로그가 단언한다. 내부적으로는 constrained decoding이라는 기법을 쓴다. 매 토큰 샘플링 시점에 스키마가 허용하지 않는 토큰의 확률을 0으로 마스킹해 버리는 방식이다. 모델이 아무리 유혹을 받아도 `"Sure! Here's the JSON:"`을 입에 올릴 수 없다.

```python
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

client = OpenAI()

class SupportTicket(BaseModel):
    priority: Literal["low", "medium", "high"]
    category: Literal["billing", "shipping", "product", "account", "other"]
    summary: str
    customer_email: str

email_text = """
From: customer@example.com
Subject: 반품이 안 되는데요

주문번호 #48211로 어제 받은 후드 티셔츠가
사이즈가 안 맞아서 반품 신청을 하려는데
앱에서 버튼이 비활성화돼 있어요. 도와주세요.
"""

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "너는 고객 지원 티켓 분류기다."},
        {"role": "user", "content": email_text},
    ],
    response_format=SupportTicket,
)

ticket: SupportTicket = completion.choices[0].message.parsed
print(ticket.priority, ticket.category, ticket.summary)
```

`parse` 헬퍼가 Pydantic 모델을 받아 JSON schema로 변환하고, 응답을 다시 객체로 채워 준다. 파싱 실패는 원천 차단된다. 단 주의할 게 있다. strict 모드는 `oneOf`, 재귀 스키마, `anyOf` 같은 일부 구조를 거부한다. 공식 문서에 제약 목록이 있다. 스키마가 받아들여지지 않으면 에러가 바로 뜨니 개발 시점에 알 수 있다는 점은 오히려 편하다.

### Anthropic tool_use — 툴을 빌려 구조를 받는다

Anthropic 쪽은 살짝 다르게 접근한다. 전용 JSON 모드를 두는 대신 **tool use를 구조화 출력의 수단으로 쓰는** 우아한 방식을 택했다. 모델에게 "이런 시그니처의 가상의 함수가 있으니 호출하라"고 시키면, 모델은 함수 인자 자리에 정확한 JSON을 넣어 반환한다. 그 함수를 실제로 실행할 필요는 없다 — 인자만 받아 쓰면 끝이다.

```python
import anthropic

client = anthropic.Anthropic()

ticket_tool = {
    "name": "create_support_ticket",
    "description": "이메일을 지원 티켓으로 저장한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "긴급도.",
            },
            "category": {
                "type": "string",
                "enum": ["billing", "shipping", "product", "account", "other"],
            },
            "summary": {
                "type": "string",
                "description": "한 문장 요약. 20자 이상 80자 이하.",
            },
            "customer_email": {"type": "string"},
        },
        "required": ["priority", "category", "summary", "customer_email"],
    },
}

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[ticket_tool],
    tool_choice={"type": "tool", "name": "create_support_ticket"},
    messages=[{"role": "user", "content": email_text}],
)

# 툴 호출 블록을 찾아 인자를 꺼낸다
for block in response.content:
    if block.type == "tool_use" and block.name == "create_support_ticket":
        ticket = block.input  # dict
        print(ticket)
```

여기서 `tool_choice`를 `{"type": "tool", "name": "..."}`로 못 박은 게 핵심이다. 이렇게 두면 모델은 **반드시** 그 툴을 호출한다. 그 외 자연어 응답은 원천 차단된다. 이 패턴은 Anthropic Cookbook에서 "extracting structured data" 레시피로 꾸준히 등장한다.

그래도 옛 방식이 여전히 유효할 때가 있다. assistant 응답을 `"{"`로 prefill해 JSON을 강제 시작시키는 전통 기법이다. 툴 정의가 부담스러운 간단한 경우엔 여전히 쓸 만하다.

### Gemini responseSchema — controlled generation

Google 쪽도 비슷하게 간다. `generationConfig.responseMimeType = "application/json"`과 `responseSchema`를 세트로 넘기면 된다.

```python
import google.generativeai as genai

schema = {
    "type": "object",
    "properties": {
        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        "category": {
            "type": "string",
            "enum": ["billing", "shipping", "product", "account", "other"],
        },
        "summary": {"type": "string"},
        "customer_email": {"type": "string"},
    },
    "required": ["priority", "category", "summary", "customer_email"],
}

model = genai.GenerativeModel(
    "gemini-2.0-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": schema,
    },
)

result = model.generate_content(email_text)
ticket = json.loads(result.text)
```

대용량 컨텍스트와 멀티모달 입력을 한 번에 구조화해서 받는 일이 많은 만큼, Gemini에서 `responseSchema`는 "이미지 한 장과 PDF를 던져 넣고 structured 결과를 받는" 류의 파이프라인에 특히 잘 맞는다.

## 스키마 설계의 원칙

디코더가 강제한다 해도, 스키마 자체가 엉성하면 모델은 스키마 안에서 엉뚱한 값을 고른다. 강제는 **형식**이지 **의미**가 아니다. 그러니 스키마를 설계할 때 몇 가지 습관을 들여 두자.

**풍부한 description을 쓰자.** 필드명만 보고 모델이 의미를 유추하게 두지 말자. `description`에 "긴급도. 결제·보안 이슈는 high, 단순 문의는 low"처럼 **판단 기준**을 짧게 써 주는 것만으로 일관성이 크게 올라간다. 스키마는 "데이터 모델"이자 동시에 "판단 지침"이라는 점을 기억해두자.

**필드명을 의미 있게 쓰자.** `f1`, `f2`, `p` 같은 약어는 모델의 추론을 방해한다. `priority`, `customer_email` 같이 풀어 쓴 이름이 훨씬 잘 먹는다. Instructor GitHub 이슈 트래커에 가 보면 필드명 하나 바꾸고 정확도가 10%p 올라갔다는 식의 보고가 심심찮게 올라온다.

**Optional 필드는 최소화하자.** 모델에게 "이건 필요하면 넣어도 되고 안 넣어도 된다"는 여지를 주면 거의 언제나 넣어 버린다. 그게 맞을 때도 있지만 대체로는 스키마 용량을 갉아먹는 잡음이 된다. 옵션이 많아질수록 출력 필드 수는 **10~15개 이하**로 관리하는 편이 낫다. 그 이상은 모델이 한 번에 끌고 가기 힘들다.

**`oneOf`와 재귀 스키마는 피하자.** Instructor의 FAQ에도 이 얘기가 있다. `oneOf`는 모델이 가장 자주 틀리는 구조 중 하나다. 재귀 스키마도 마찬가지다. 정말 필요하면 두 번의 호출로 쪼개는 편이 안정적이다. 한 번에 분류하고, 다른 한 번에 그 분류에 맞는 상세 스키마를 채우게 하는 식이다.

**출력 필드명과 의미를 일치시키자.** `status`라는 필드에 `"completed"`가 들어갈지 `"success"`가 들어갈지 프롬프트 작성자가 혼동하면, 모델도 혼동한다. `Literal[...]` 혹은 `enum`으로 가능한 값을 박아 두자. 이것만으로도 schema violation의 큰 축이 잡힌다.

## Tool Use — 모델에게 손과 발을 주기 위한 프롬프트

구조화 출력을 조금만 더 밀고 가면 그게 바로 tool use다. "JSON으로 답해 줘"와 "이 함수를 호출해 줘"는 표면은 비슷하지만 의미는 크게 다르다. 전자는 모양만 잡는 것이고 후자는 **모델이 세계에 개입하는** 일이다. 9장에서 본격적으로 다룰 에이전트 프롬프팅의 출발점이기도 하다.

### 툴 매니페스트를 문서처럼 쓰자

모델은 툴 정의를 **문서로 읽는다**. name, description, parameter의 이름·타입·description이 모두 프롬프트의 일부로 들어간다. 그러니 대충 쓰면 안 된다. 간단한 예로 날씨 조회 툴을 생각해보자.

```python
weather_tool = {
    "name": "get_weather",
    "description": (
        "주어진 도시의 현재 날씨를 조회한다. "
        "결과는 섭씨 온도와 한국어 날씨 상태(맑음/흐림/비/눈)를 포함한다. "
        "한국 도시만 지원한다. 미지원 도시는 'unsupported'를 반환한다."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "도시 이름(한글). 예: '서울', '부산'.",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "온도 단위. 기본 celsius.",
            },
        },
        "required": ["city"],
    },
}
```

description에 **지원 범위**, **반환 형식**, **미지원 시 동작**까지 적었다는 점을 눈여겨보자. 이걸 적어 두지 않으면 모델은 "서울"과 "Seoul"을 번갈아 쓰기도 하고, 지원하지 않는 도시에 대해 창작 응답을 반환하기도 한다. 툴 정의는 **API 문서 수준의 꼼꼼함**이 필요하다는 얘기다. 번거롭다고 생략하면 런타임에 훨씬 더 번거로운 일이 벌어진다.

### 파라미터 이름은 ambiguity를 없애는 레버다

`date`라는 파라미터가 있으면 모델은 `"2026-04-18"`로 줄지, `"April 18, 2026"`으로 줄지, `"오늘"`로 줄지 고민한다. `date_iso_8601`이라고 이름을 바꾸면 고민이 사라진다. 이름 하나로 포맷 준수율이 바뀌는 경험은 Tool use를 운용해 본 사람이라면 공감할 것이다. 약어 대신 풀어 쓰기, 단위 명시하기(`price_usd`, `duration_seconds`), enum 쓰기 — 이 세 가지만 지켜도 실패율이 크게 떨어진다.

### 툴이 많아지면 라우팅이 필요하다

툴이 15~20개를 넘어가면 모델의 선택 정확도가 떨어진다. 이건 커뮤니티와 Anthropic 블로그가 공통으로 말하는 관찰이다. 대응은 두 가지다. 하나는 **Routing agent**로 먼저 분류한 뒤, 해당 카테고리의 툴 부분집합만 다음 호출에 로드하는 것. 다른 하나는 **동적 tool subset** — 쿼리에 따라 관련 툴만 선택해 프롬프트에 싣는 것. 9장에서 더 본격적으로 다루겠지만, 구조화 출력 관점에서도 "툴 목록 자체가 프롬프트의 일부"라는 사실을 잊지 말자. 목록이 길면 프롬프트가 길어지고, 프롬프트가 길어지면 신호 대 잡음비가 떨어진다.

### Few-shot tool call

tool use에도 few-shot이 통한다. 특히 멀티 스텝 호출 패턴을 가르칠 때 유용하다. 시스템 프롬프트에 "이전에 이런 상황에서는 이렇게 호출했다"는 짧은 trajectory를 한두 개 박아 두면 모델이 그 경로를 흉내 낸다.

```
예시:
User: "서울 날씨 알려 줘"
Assistant: get_weather(city="서울")
Tool result: {"temp_c": 18, "condition": "맑음"}
Assistant: "서울은 현재 18도, 맑습니다."

User: "그럼 부산은?"
Assistant: get_weather(city="부산")
```

이 예시 하나만으로도 "이전 대화의 맥락을 이어 새 툴 호출을 만드는" 패턴이 훨씬 안정적으로 잡힌다.

## 실전 예제 1 — 이메일 → 구조화 티켓

앞서 나온 조각들을 모아, 실제로 고객센터 이메일을 티켓으로 변환하는 파이프라인을 구성해보자. Anthropic SDK 기준이다.

```python
import anthropic
from pydantic import BaseModel, ValidationError
from typing import Literal

client = anthropic.Anthropic()

class SupportTicket(BaseModel):
    priority: Literal["low", "medium", "high"]
    category: Literal["billing", "shipping", "product", "account", "other"]
    summary: str
    customer_email: str
    needs_human_review: bool

ticket_tool = {
    "name": "create_support_ticket",
    "description": (
        "고객 이메일을 내부 지원 티켓으로 변환한다. "
        "결제·보안·법적 이슈는 priority=high로, "
        "모호하거나 민감한 건은 needs_human_review=true로 표시한다."
    ),
    "input_schema": SupportTicket.model_json_schema(),
}

SYSTEM_PROMPT = """너는 고객 지원 티켓 분류기다.
<rules>
- 결제 중복, 개인정보 노출, 법적 언급은 항상 priority=high.
- 단순 사용법 문의는 priority=low.
- summary는 20~80자 한국어 한 문장.
- 고객 이메일 주소가 본문에 없으면 From 헤더에서 추출한다.
- 모호하면 needs_human_review=true로 두고 best-effort 분류를 한다.
</rules>"""

def classify_email(email_text: str) -> SupportTicket:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=[ticket_tool],
        tool_choice={"type": "tool", "name": "create_support_ticket"},
        messages=[{"role": "user", "content": f"<email>\n{email_text}\n</email>"}],
    )
    for block in response.content:
        if block.type == "tool_use":
            try:
                return SupportTicket(**block.input)
            except ValidationError as e:
                # 디코더가 스키마를 지켰어도 비즈니스 룰 위반은 여기서 잡힌다
                raise RuntimeError(f"스키마는 통과했지만 검증 실패: {e}")
    raise RuntimeError("모델이 툴을 호출하지 않았다")
```

몇 가지 포인트를 짚어 두자. 첫째, 시스템 프롬프트에 `<rules>` 태그로 **비즈니스 룰**을 박아 둔다. 스키마만으로는 "결제 중복은 high"를 가르칠 수 없다. 둘째, `model_json_schema()`로 Pydantic 모델을 그대로 스키마로 쓴다. 코드-프롬프트-타입이 하나로 묶인다. 셋째, tool_use가 성공적으로 파싱된 뒤에도 **Pydantic 검증을 한 번 더 돌린다**. 디코더 레벨 강제와 애플리케이션 레벨 검증은 서로 다른 층위다. 둘 다 필요하다.

## 실전 예제 2 — 긴 문서에서 엔티티 추출

두 번째 예제는 20페이지짜리 계약서에서 당사자, 금액, 기간을 뽑는 일이다. OpenAI Structured Outputs로 풀어보자.

```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

client = OpenAI()

class Party(BaseModel):
    role: str = Field(description="계약상 역할. 예: '갑', '을', '수탁자'.")
    legal_name: str = Field(description="법인 전체 명칭 또는 개인 성명.")
    representative: str | None = Field(
        default=None, description="대표자 이름. 법인이 아니면 None."
    )

class ContractExtract(BaseModel):
    parties: List[Party] = Field(description="계약 당사자 목록.")
    total_amount_krw: int = Field(description="총 계약 금액(원). 부가세 포함.")
    start_date_iso: str = Field(description="계약 시작일(YYYY-MM-DD).")
    end_date_iso: str = Field(description="계약 종료일(YYYY-MM-DD).")
    governing_law: str = Field(description="준거법. 예: '대한민국 법'.")

SYSTEM = """너는 계약서에서 핵심 조항을 추출하는 어시스턴트다.
원문에 명시되지 않은 값은 추측하지 않는다. 필드가 반드시 필요한데
원문에 없다면 빈 문자열이나 0을 넣지 말고, 가장 근접한 표현을 그대로 옮겨 적는다."""

def extract_contract(contract_text: str) -> ContractExtract:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"# 계약서 원문\n\n{contract_text}"},
        ],
        response_format=ContractExtract,
    )
    return completion.choices[0].message.parsed
```

포인트 하나를 붙여 두자. **"모르면 빈값을 넣지 말라"**는 지시가 의외로 중요하다. 모델은 스키마가 `str`이면 빈 문자열을, `int`면 `0`을 기본값처럼 넣는 습관이 있다. 이건 5장에서 본 환각의 변형이다. 기권 경로 대신 추측 경로로 흐르는 것이다. 스키마가 강제하는 타입과 사람이 원하는 의미가 어긋나는 틈에서 이런 사고가 난다. 프롬프트에 "원문 표현을 그대로 옮기라"는 한 문장을 더해 두면 꽤 많은 거짓 0이 사라진다.

긴 문서를 다룰 때는 또 한 가지를 기억해두자. 2장에서 다룬 **Lost in the Middle** 편향이다. 20페이지 계약서를 한 번에 넣으면 중간 조항을 놓치기 쉽다. 중요한 부분은 앞/뒤에 재인용하거나, map-reduce로 섹션별 추출 후 통합하는 전략이 낫다.

## 실전 예제 3 — 멀티 스텝 tool call

마지막 예제는 날씨와 일정 API를 섞어 쓰는 가벼운 에이전트다. 모델이 한 번에 끝내지 않고, 툴 결과를 보고 다음 툴을 고르는 **다단계 루프**를 구성한다.

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "도시의 현재 날씨를 조회. 한국 도시만 지원.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
    {
        "name": "suggest_indoor_activity",
        "description": "비·눈 올 때 추천할 실내 활동을 반환.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
]

# 가짜 툴 실행기 — 실제로는 API 호출이 들어간다
def run_tool(name: str, args: dict) -> str:
    if name == "get_weather":
        return json.dumps({"temp_c": 12, "condition": "비"})
    if name == "suggest_indoor_activity":
        return json.dumps({"suggestion": "국립중앙박물관 방문"})
    return json.dumps({"error": "unknown tool"})

def agent_loop(user_message: str, max_turns: int = 5):
    messages = [{"role": "user", "content": user_message}]
    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason == "end_turn":
            # 모델이 최종 답을 냈다
            return response.content[-1].text
        # tool_use 블록을 찾아 실행하고 결과를 다음 turn에 넣는다
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tu in tool_uses:
            result = run_tool(tu.name, tu.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": result,
                }
            )
        messages.append({"role": "user", "content": tool_results})
    raise RuntimeError("max_turns 초과")

print(agent_loop("오늘 서울 날씨 보고 뭐 할지 추천해 줘"))
```

이 짧은 루프 안에 구조화 출력과 tool use가 한 번에 녹아 있다. 모델은 첫 턴에서 `get_weather`를 호출하고, 결과가 "비"인 걸 본 뒤 두 번째 턴에서 `suggest_indoor_activity`를 호출한다. 그리고 세 번째 턴에서 최종 텍스트 응답을 낸다. **툴 정의가 곧 프롬프트**이고, **툴 결과가 곧 다음 턴의 컨텍스트**라는 관점을 여기서 잡아 두자. 9장에서 본격적으로 파고들 에이전트 프롬프팅의 기본 회로다.

한 가지만 덧붙이자. 이 루프에 `max_turns`를 반드시 두자. 모델이 무한히 툴 호출을 계속하다가 토큰 예산을 태우는 사고가 실제로 자주 난다. 예산이 터진 밤을 한 번 겪고 나면, `max_turns` 가드가 얼마나 고마운지 알게 된다. 끔찍한 일을 예방하는 장치다.

## 흔한 실패 모드와 대응

세 공급사의 강제 모드를 써도 완벽하진 않다. 실전에서 자주 마주치는 실패 모드를 짚어 두자.

**Schema violation이 남아 있는 드문 경우.** strict 모드가 아닌 파생 모드를 썼을 때, 혹은 라이브러리가 스키마의 일부만 강제할 때 생긴다. 대응은 단순하다. 애플리케이션 단에서 다시 한 번 Pydantic/Zod 검증을 돌리자. 재시도 루프를 하나 두되, 재시도 프롬프트에 **원인**을 돌려주면 한 번에 고쳐지는 경우가 많다. "앞선 응답에서 `customer_email`이 누락됐다. 다시 시도하되 해당 필드를 반드시 채워라"처럼.

**Hallucinated field.** 스키마에 없는 필드를 넣는 일은 strict 모드에선 거의 사라진다. 그래도 Anthropic tool_use에선 드물게 보인다. `additionalProperties: false`를 스키마에 박아 두자. JSON Schema 레벨에서 추가 필드를 거부한다.

**Truncation.** 출력이 토큰 한도에 걸려 중간에서 잘리는 문제. 이건 모양 강제의 문제가 아니라 **예산**의 문제다. `max_tokens`를 충분히 주고, 긴 필드(예: `summary`)에 "100자 이내"처럼 경계를 박아 두자. Pydantic `Field(max_length=100)`도 함께 쓰면 모델이 짧게 맞추는 경향이 생긴다.

**Enum 값 흘림.** 드물게 `priority`에 `"High"`처럼 대소문자가 달라지거나, `"긴급"`처럼 한국어가 섞여 나올 때가 있다. strict 모드에선 막히지만 그 외엔 검증 후 재시도로 처리하는 게 낫다. 혹은 description에 "값은 영소문자만"이라고 한 줄 더 박자.

**Optional 남용이 만드는 잡음.** 앞서도 말했지만 한 번 더 기억해두자. Optional 필드가 많으면 모델이 빈 객체나 빈 배열을 "있어 보이게" 채워 넣는다. 필요 없는 필드는 **빼는 편이 낫다**.

## 라이브러리 생태계 — Instructor, BAML, Outlines, Guidance

세 공급사의 네이티브 기능만으로도 많은 걸 할 수 있지만, 오픈소스 도구들이 그 위에 한 층의 편의를 쌓아 왔다. 하나씩 살펴보자.

**Instructor (jxnl/instructor).** 가장 널리 쓰이는 Python 라이브러리다. 아이디어는 단순하다. "OpenAI/Anthropic/Gemini 클라이언트를 한 줄로 패치해, `response_model=Pydantic클래스`만 넘기면 Pydantic 객체를 돌려주는" 인터페이스다. 내부적으로 공급사별 구조화 모드를 골라 쓰고, 실패 시 자동 재시도와 에러 메시지 피드백까지 제공한다. 프로덕션에 구조화 출력을 처음 도입할 때 시작점으로 좋다.

**BAML (BoundaryML).** 조금 더 과감한 선언을 한다. 프롬프트를 **함수 시그니처**로 쓰자는 것이다. `.baml` 파일에 함수와 타입을 선언하면 BAML 컴파일러가 각 공급사용 프롬프트·클라이언트 코드를 자동 생성한다. 8장에서 다룰 자동 최적화 관점과도 맞닿아 있다. "프롬프트를 코드처럼" 관리하는 실험이 가장 진전된 도구 중 하나다.

**Outlines (dottxt-ai/outlines).** 로컬 오픈소스 모델까지 포함해서 구조화 출력을 제공한다. 정규식, JSON schema, 문맥자유문법(CFG)을 직접 받는다. vLLM이나 llama.cpp 기반으로 자체 인프라를 돌리는 팀이라면 Outlines가 필수적이다. strict JSON을 공급사 API 없이도 얻을 수 있다.

**Guidance (guidance-ai/guidance).** 프롬프트 템플릿 안에 **생성 제약을 인라인으로 박는** 문법을 제공한다. "여기에는 `["yes", "no"]` 중 하나, 여기에는 최대 100자 문자열"처럼. 로컬 모델 기반에서 특히 강력하다.

어떤 걸 쓸까? 처음에는 **Instructor 하나로 시작**하는 편이 낫다. 세 공급사를 오가는 추상화가 필요해지면 **BAML**로 넘어가자. 로컬 모델을 직접 돌린다면 **Outlines/Guidance**가 답이다. 도구 고르기가 번거로워 보이지만, 일단 한 번 자리 잡으면 이후의 피로가 크게 줄어든다.

## RAG 결과를 툴 응답처럼 주입하기

5장에서 우리는 RAG로 외부 지식을 끌어다 쓰는 법을 다뤘다. 거기서 검색 결과를 프롬프트 본문에 그대로 붙여 넣었다. 그런데 6장의 관점에서 다시 보면, **RAG 결과도 일종의 툴 응답**으로 볼 수 있다. 모델이 `search_docs(query="...")` 같은 가상의 툴을 호출한 결과라고 가정하고, tool_result 블록으로 주입하는 패턴이다.

왜 이렇게 할까? 첫째, **출처가 구조화된다**. `{"source_id": "doc-42", "text": "..."}` 형태로 내려주면 모델이 `[doc-42]` 같은 인용을 자연스럽게 끌어낸다. 둘째, **에이전트와의 경계가 흐려진다**. 오늘은 static RAG이지만 내일은 모델이 스스로 검색을 호출할 수도 있다. 두 경우를 같은 인터페이스로 취급하면 시스템이 단순해진다. 9장에서 본격적으로 다룰 내용이지만, 구조화 출력 관점에서도 이 설계를 미리 심어 두는 편이 낫다.

## 처음이라면 이것만 (학생 독자용)

처음 구조화 출력을 도입한다면 이 순서로 가자. 첫째, Pydantic 모델(또는 Zod 스키마)을 먼저 정의한다. 둘째, 공급사가 OpenAI라면 `beta.chat.completions.parse`, Anthropic이면 `tool_choice`로 특정 툴 강제, Gemini면 `responseSchema`를 쓴다. 셋째, 파싱 성공 후에도 Pydantic으로 한 번 더 검증한다. 넷째, 실패 시 원인을 프롬프트에 돌려주는 재시도 루프를 하나 둔다. 다섯째, 필드 수 10개 이하, optional 최소화, description 꼼꼼히.

이게 전부다. 처음 만드는 구조화 파이프라인은 화려할 필요가 없다. 오히려 꾸준히 작동하는 단순한 루프가 팀의 월요일 아침을 지켜 준다.

## 원 출처 포인터 (연구자 독자용)

- OpenAI, *Introducing Structured Outputs in the API*, 2024-08 (platform.openai.com/docs/guides/structured-outputs)
- Anthropic, *Tool use (function calling)* 공식 문서 (docs.anthropic.com/en/docs/build-with-claude/tool-use)
- Google, *Controlled generation / responseSchema* (ai.google.dev/gemini-api/docs/structured-output)
- Instructor — github.com/jxnl/instructor
- BAML — github.com/BoundaryML/baml
- Outlines — github.com/dottxt-ai/outlines
- Guidance — github.com/guidance-ai/guidance
- Schulhoff et al., *The Prompt Report: A Systematic Survey of Prompting Techniques*, arXiv:2406.06608 (2024) — §3.12 관련 부분이 가장 간결한 요약.

구조화 출력과 tool use를 다룬 단일 권위 논문은 아직 없다. 이 영역은 2024년 이후 **공식 문서와 실무 블로그가 학술 논문을 앞서 나간** 드문 분야다. 연구자라면 세 공급사의 changelog를 주기적으로 추적하는 편이 최신 동향 파악에 유리하다.

## 마무리

자유 텍스트를 그대로 받아쓰던 시절은 지나갔다. 2024년 이후 우리는 스키마를 강제할 수 있고, 툴로 세계와 연결할 수 있다. 금요일 오후 6시의 `JSONDecodeError`는 더 이상 감수해야 할 현실이 아니라 **예방 가능한 사고**가 됐다.

기억해두자. 구조화 출력은 형식의 문제이고, 스키마 설계는 의미의 문제다. 디코더가 형식을 잡아 주는 동안 우리는 **스키마에 의미를 담는 일**에 집중해야 한다. 필드명은 풀어 쓰고, description은 문서처럼 꼼꼼히, optional은 최소화하고, enum으로 가능한 값을 박아 두자. 그 다음에야 strict 모드나 tool_use 같은 디코더 장치가 빛을 발한다. 둘 중 하나만으로는 부족하고, 둘이 겹쳐져야 튼튼한 파이프라인이 된다.

그리고 한 가지 더. 6장이 다룬 구조화는 단일 호출 안에서의 구조화였다. 7장에서는 **같은 프롬프트를 Claude, GPT, Gemini에 던졌을 때 왜 결과가 다른가**를 살필 것이다. XML이 잘 먹는 모델과 Markdown이 잘 먹는 모델, system 프롬프트에 예민한 모델과 덜 예민한 모델 — 이 차이를 모르고 멀티-모델 시스템을 짜면 한밤중에 롤백하는 일이 잦아진다. 6장의 스키마 설계를 그대로 들고, 7장에서 세 공급사 각각에 맞게 옷을 갈아입히는 연습을 해보자.
