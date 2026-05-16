# 7장. 같은 에이전트, 두 번째로 짓기 — LangChain과 LCEL

OpenAI API 한 줄을 부르려고 클래스 셋을 거친 날이 있다. 농담처럼 도는 말이지만, LangChain을 처음 만진 사람이라면 거의 한 번씩은 같은 풍경을 본다. `from openai import OpenAI` 한 줄, `client.chat.completions.create(...)` 한 줄. 그게 두 줄이면 끝날 일을, LangChain은 `ChatOpenAI`·`ChatPromptTemplate`·`StrOutputParser`까지 객체 셋을 늘어세운다. 처음 보면 난감하다. "이게 정말 필요할까?" 싶다.

그런데 한 번 멈추고 따져 보자. 클래스 셋이 거기 있는 데에는 이유가 있다. LCEL — LangChain Expression Language — 의 설계는 그 *이유*에 대한 한 줄 답이다. Part 1에서 손으로 짠 `mini_agent.py` v3은 198줄짜리 캐논이었다. ReAct 루프, 메모리, 도구 디스패치, 안전장치, 비용 계측까지 직접 박았다. 같은 동작을 LangChain으로 다시 지으면 코드는 줄어들고, *추상의 깊이*는 늘어난다. 이 두 변화를 같이 들여다보자. 그래야 8장에서 진짜 강점을 가려낼 수 있고, 9장에서 그 비용을 정직하게 셀 수 있다.

## LangChain이 대신해 주는 네 가지

LangChain은 거대한 라이브러리다. 모듈 수가 수백 개, 통합(integration) 수는 천 단위에 이른다. 이걸 한 번에 머리에 담으려고 하면 길을 잃는다. 그러니 먼저 네 가지 큰 묶음으로 나누어 보자. 공식 문서가 직접 그렇게 정리하고 있기도 하다.

첫째, **공통 인터페이스**다. OpenAI, Anthropic, Google Gemini, Mistral, 로컬 Ollama — 모두 표면 API가 다르다. 메시지 포맷도 다르고, 도구 호출 응답 모양도 다르고, 스트리밍 방식도 다르다. LangChain은 이들을 모두 `Runnable`이라는 한 추상으로 묶는다. 모델만이 아니다. 임베딩, 벡터스토어, 도구, 파서, 심지어 직접 짠 함수까지 같은 인터페이스를 공유한다.

둘째, **합성**이다. `prompt | llm | parser` 같은 LCEL 파이프 표현으로 여러 단계를 한 줄에 묶을 수 있다. 그리고 한 번 묶어 두면, 스트리밍·배치·async·병렬을 LangChain이 알아서 처리한다.

셋째, **통합 모듈**이다. PGVector·Pinecone·Weaviate·Chroma·Qdrant 같은 벡터 DB들, 수십 종의 로더(PDF, HTML, Notion, S3, …), retriever 변종들, 콜백 후크들 — 이걸 직접 짤 일이 없어진다는 점이 LangChain을 쓰는 가장 현실적인 이유다.

넷째, **관찰성**이다. LangSmith를 붙이면 "그래서 이번에 모델이 정확히 뭘 받고 뭘 뱉었지?"라는 6장의 골치 아픈 질문에 거의 한 클릭으로 답이 나온다.

이번 장은 첫째와 둘째 — 공통 인터페이스와 합성 — 에 집중한다. 셋째와 넷째는 8장의 주제다.

## Runnable이라는 한 추상

LCEL의 시작점은 `Runnable`이다. 이름은 추상적이지만 실체는 단순하다. "입력을 받아 출력을 내는 한 단위 연산"이다. 함수처럼 호출할 수 있고, 입력 타입과 출력 타입이 명시적이고, 네 가지 메서드를 똑같이 제공한다.

```python
result = chain.invoke(input)         # 동기, 한 번
results = chain.batch([i1, i2, i3])  # 동기, 여러 입력 병렬
for tok in chain.stream(input):       # 동기, 토큰 스트림
    print(tok, end="")
result = await chain.ainvoke(input)  # 비동기
```

여기서 한 박자 쉬자. 이 네 메서드는 별일 아닌 듯 보이지만 *별일이 맞다*. Part 1에서 우리가 직접 짤 때, 스트리밍은 어떻게 했었는지 기억해 보자. `client.chat.completions.create(..., stream=True)`로 바꾸고, 응답을 `for chunk in response` 루프로 받고, `chunk.choices[0].delta.content` 같은 점 표기를 풀어내야 했다. 배치는 또 어떤가. 입력 N개를 N번 동기로 부르거나, `asyncio.gather`로 직접 fan-out을 짜야 했다. 비동기 호출은 또 별도 메서드. 네 가지 호출 모양이 각자 다른 API였다.

`Runnable`은 이 네 가지 호출 모양을 *한 객체의 메서드*로 통일한다. 같은 chain을 만들어 두면 한 번은 `invoke`로, 다른 곳에선 `batch`로, 또 다른 곳에선 `stream`으로 부르면 된다. 모델을 OpenAI에서 Anthropic으로 바꿔도 호출 코드는 그대로다. 이걸 *공통 인터페이스의 가치*라고 부른다. 한 번 익혀 두면, 그 뒤에 만지는 모든 LangChain 구성 요소가 같은 모양으로 동작한다.

물론 공짜는 아니다. `Runnable`은 추상 베이스 클래스 위에 여러 추상 계층이 올라간 구조라, MRO(메서드 결정 순서)가 길다. 나중에 디버거로 `bind_tools` 한 줄을 step into 하면 호출 스택이 깊어지는 걸 보게 된다. 그 깊이의 비용은 이 장의 후반에서 다시 세어 보자.

## LCEL 파이프 — `__or__`의 가독성과 함정

LCEL의 시그니처 문법은 파이프 문자다. `prompt | llm | parser`. 셸의 파이프와 똑같이 보인다. 실제로 의미도 비슷하다. 왼쪽의 출력이 오른쪽의 입력으로 흘러간다.

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant."),
    ("user", "{question}"),
])
llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
chain = prompt | llm | StrOutputParser()

answer = chain.invoke({"question": "What is LCEL in one sentence?"})
print(answer)
```

세 단계가 한 줄에 깔끔하게 묶인다. 가독성은 정말 좋다. 셸을 한 번이라도 써 본 개발자라면 이 문법은 거의 즉시 읽힌다.

그렇다면 이 파이프는 어떻게 동작할까? 파이썬에는 `|` 연산자가 있지만, 본래 비트 OR이다. LangChain은 `Runnable` 클래스에서 `__or__`를 오버로딩해 이 동작을 새로 정의했다. `a | b`는 `a.__or__(b)`를 부르고, 결과는 새로운 `RunnableSequence` 객체다. 즉 파이프는 *실행*이 아니다. 객체를 *조합*해 새 chain을 만들 뿐이다. 실제 모델 호출은 `chain.invoke(...)` 시점에 일어난다.

이 사실을 기억해 두자. `|`는 정의(declarative)다. 실행이 아니다. 익숙해지면 자연스럽지만, 처음 보면 한 번 헷갈린다. "왜 이 줄에서 LLM이 안 도는 거지?" 싶다. 디버거로 잡아 보면 그제야 알게 된다. 파이프는 그저 객체 결합. 실제 일은 `invoke` 시점에 벌어진다.

함정도 있다. 파이프는 가독성이 좋은 만큼 *순서가 보이지 않게 숨는다.* 다섯 단계, 여섯 단계로 파이프가 길어지면 어디서 무엇이 변형되는지 추적이 힘들어진다. 한 단계가 실패하면 traceback이 LangChain 내부로 깊게 들어가, 막상 내 잘못이 어디였는지 한 번 더 살펴야 한다. 그래서 "파이프는 짧게, 의미 단위로 끊자"가 실무 권고다. 다섯 줄짜리 한 chain보다, 두 줄짜리 두 chain을 명시적으로 부르는 편이 디버깅에는 낫다.

## 분기와 병렬 — 코드가 아니라 *조합*으로

ReAct 루프 하나만 짤 때는 보이지 않지만, 실제 워크플로엔 *분기*가 자주 등장한다. "사용자 의도가 질문이면 RAG로, 명령이면 도구 실행으로." "두 가지 retriever 결과를 동시에 가져와 합치자." 이런 패턴을 손으로 짜면, 결국 if/else 또는 `asyncio.gather`다.

LCEL은 이걸 *조합* 차원에서 표현한다.

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 두 chain을 병렬로 돌려 결과를 dict로 묶는다
fan_out = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
)
combined = fan_out | merger_chain

# RunnablePassthrough는 "입력을 그대로 흘려보내는" 한 단위
# context와 question을 같이 가지고 다닐 때 자주 쓴다
rag = (
    RunnableParallel(
        context=retriever,
        question=RunnablePassthrough(),
    )
    | prompt
    | llm
    | StrOutputParser()
)
```

`RunnableParallel`은 dict 모양의 fan-out이고, `RunnablePassthrough`는 "이 자리에 입력을 그대로 끼워 넣어라"는 의미다. 두 추상이 만나면, RAG의 가장 흔한 패턴 — retriever와 user question을 같이 prompt에 박는 모양 — 이 다섯 줄에 깔끔하게 잡힌다.

여기서 LCEL의 진짜 가치 한 가지가 드러난다. **병렬 실행은 우리가 짠 게 아니라 LangChain이 자동으로 해 준다.** `RunnableParallel`이 fan-out 부분을 알아서 `asyncio.gather`로 묶는다. 직접 async를 짤 때 자주 빠뜨리는 예외 전파, 부분 실패 처리 같은 자잘한 일도 LangChain 안쪽에서 처리된다. 이 부분은 정말 편하다.

## 5종 워크플로를 LCEL로 옮겨 보자

1장에서 Anthropic의 분류를 한 번 살펴봤다. 다섯 가지 워크플로 패턴 — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. 이걸 LCEL로 옮기면 어떻게 될까. 한 번 표로 묶어 보자.

| 워크플로 | LCEL 표현 | 짧은 코드 모양 | 매끄러움 |
|---|---|---|---|
| **Prompt chaining** | `\|` 파이프 | `step1 \| step2 \| step3` | 완벽히 자연스럽다 |
| **Routing** | `RunnableBranch` | `RunnableBranch((cond1, chain1), (cond2, chain2), default)` | 자연스럽다 |
| **Parallelization** | `RunnableParallel` | `RunnableParallel(a=ca, b=cb)` | 자연스럽다 |
| **Orchestrator-workers** | (강제로 끼우면 가능) | dynamic dispatch + custom logic | **매끄럽지 않다** |
| **Evaluator-optimizer** | (사이클 필요) | LCEL은 DAG라 표현이 안 된다 | **표현 자체가 어렵다** |

위 셋은 LCEL이 잘 받는다. 한 줄짜리 합성으로 깨끗하게 잡힌다. 아래 둘은 사정이 다르다.

Orchestrator-workers는 *중앙 supervisor가 동적으로 worker를 고르는* 패턴이다. LCEL로도 강제로 짤 수는 있지만, `RunnableLambda` 안에 디스패치 로직을 박고, 결과를 다시 모으는 코드를 손으로 작성해야 한다. 그리고 가장 큰 문제는 evaluator-optimizer — "결과를 평가해 만족할 때까지 반복" — 다. **LCEL은 본질적으로 DAG**다. 사이클이 없다. 그러니 "한 번 더 시도"의 자연스러운 표현이 불가능하다. 억지로 끼우면 코드가 더러워지고, 가독성은 떨어진다.

이 둘이 본격적으로 다뤄지는 자리는 10장의 LangGraph다. 사이클을 받는 그래프 추상이 등장하면, 위 두 패턴이 다시 매끄러워진다. LCEL과 LangGraph가 같이 존재하는 이유가 여기 있다. 합성에는 LCEL이, 사이클에는 LangGraph가.

## 도구 정의 — JSON schema를 손으로 안 써도 된다

Part 1에서 도구를 정의할 때, 우리는 JSON schema를 손으로 짰다. `"name": "calc"`, `"description": "..."`, `"input_schema": {"type": "object", "properties": {...}}` — 한 도구당 열 줄 가까이 되었다. 도구가 셋이면 서른 줄. 보일러플레이트의 본보기다.

LangChain은 이걸 `@tool` 데코레이터 한 줄로 줄인다.

```python
from langchain_core.tools import tool

@tool
def calc(expression: str) -> str:
    """Evaluate a simple arithmetic expression like '2 + 3 * 4'."""
    return str(eval(expression, {"__builtins__": {}}))
```

이게 끝이다. 함수 시그니처와 docstring과 타입 힌트만 있으면, LangChain이 알아서 JSON schema를 생성한다. 인자 이름·타입·docstring의 자연어 설명까지 자동으로 schema에 매핑된다. 보일러플레이트가 한 줄로 줄어드는 마법.

그런데 *마법*이라는 말을 한 번 의심해 보자. 어떻게 함수 시그니처에서 schema가 나올까? LangChain은 `inspect` 모듈로 함수의 시그니처를 읽고, 타입 힌트를 pydantic 모델로 변환하고, docstring을 파싱해 설명을 채운다. 이 과정에 *부작용*이 몇 가지 있다.

첫째, 데코레이터를 다는 순간 함수는 더 이상 평범한 함수가 아니다. `BaseTool`을 상속한 객체 인스턴스다. `calc(2)` 같은 직접 호출도 가능하긴 한데, 그건 도구로서 호출이지 원래 함수 호출이 아니다. `calc.invoke({"expression": "2 + 3"})` 같은 `Runnable` 인터페이스로 부르는 게 정상이다. 이게 헷갈리면 한 번 멈춰서 정리할 필요가 있다.

둘째, 타입 힌트를 *반드시* 정확하게 써야 한다. `def calc(expression)`처럼 힌트 없이 쓰면, schema 생성 시점에 "타입을 모르겠다"는 에러가 난다. Part 1에서 우리가 손으로 schema를 짤 때는 어떤 타입이든 자유롭게 적었지만, `@tool`은 inspect 결과에 강하게 의존한다. 함수 시그니처가 곧 계약이다.

셋째, docstring의 첫 줄이 도구의 *설명*으로 들어간다. 다음 줄들은 인자 설명으로 파싱된다(formats: Google·Sphinx·NumPy 스타일을 인식). docstring을 평소 습관처럼 대충 쓰면, 모델이 보는 도구 설명이 망가진다. 이 사실을 한 번 본 다음부터는, 도구 함수 docstring을 *진지하게* 쓰게 된다.

마지막으로, `@tool`은 호출 경로에 한 겹을 더 끼운다. 모델이 `calc` 도구를 부르면, 실제로는 `calc.invoke(...)`가 돌고, 그 안에서 원본 함수가 호출된다. traceback에 LangChain 내부 프레임이 한두 개 더 끼는 정도지만, "내가 짠 함수가 직접 도는 게 아니다"라는 사실은 기억해 두자.

이 정도면 도구 정의 측면에서 LangChain이 우리에게서 가져간 것과 우리에게 준 것이 그려진다. 보일러플레이트 30줄을 가져가고, 대신 *시그니처와 docstring을 진지하게 다루어야 한다*는 규율을 두고 갔다. 좋은 거래다.

한 가지 한국어 환경의 작은 주의도 짚어 두자. `@tool`이 파싱하는 docstring과 인자 설명은 결국 모델 프롬프트의 일부로 들어간다. 도구 설명을 한국어로 쓰면, 영어 모델일 때 미세한 성능 편차가 생기는 경우가 있다. Anthropic·OpenAI 최신 모델은 한국어 instruction을 잘 받아내는 편이지만, 도구의 *식별자*(함수 이름, 인자 이름)는 영어로 두고, *설명*만 한국어로 쓰는 절충이 안전하다. 이 부분은 부록의 한국어 노트에서 다시 짚는다.

## mini_agent의 LangChain 버전

이제 본론이다. Part 1에서 손으로 짠 `mini_agent.py` v3을 LangChain으로 다시 짓는다. 같은 동작, 다른 추상.

```python
# mini_agent_lc.py
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

# --- 도구 정의: 세 개 모두 @tool 한 줄 ---

@tool
def calc(expression: str) -> str:
    """Evaluate a simple arithmetic expression like '2 + 3 * 4'."""
    return str(eval(expression, {"__builtins__": {}}))

@tool
def web_search(query: str) -> str:
    """Search the web and return a short snippet. (Demo stub.)"""
    return f"[stub] Top result for '{query}': example.com/2026"

# 단순 메모: 모듈 변수 한 줄
_MEMO: dict[str, str] = {}

@tool
def memo(action: str, key: str, value: str = "") -> str:
    """Store or retrieve a note. action='set' or 'get'."""
    if action == "set":
        _MEMO[key] = value
        return f"Saved '{key}'."
    if action == "get":
        return _MEMO.get(key, f"No memo for '{key}'.")
    return f"Unknown action: {action}"

TOOLS = [calc, web_search, memo]
TOOL_MAP = {t.name: t for t in TOOLS}

# --- 모델: 도구를 바인딩한다 ---

llm = ChatAnthropic(
    model="claude-sonnet-4-5",
    temperature=0,
    max_tokens=1024,
).bind_tools(TOOLS)

# --- ReAct 루프: 6장 v3와 동일 모양, 호출만 LangChain ---

def run_agent(user_input: str, max_iter: int = 10) -> str:
    messages = [HumanMessage(content=user_input)]
    for i in range(max_iter):
        ai_msg: AIMessage = llm.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            return ai_msg.content  # 자연 종료

        for call in ai_msg.tool_calls:
            tool_fn = TOOL_MAP[call["name"]]
            try:
                result = tool_fn.invoke(call["args"])
            except Exception as e:
                result = f"Tool error: {e}"
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return "[iteration cap reached]"

# --- 회복력: 한 줄로 끼울 수 있다 (비용은 따로 본다) ---

resilient_llm = llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
).with_fallbacks([ChatAnthropic(model="claude-haiku-4-5", temperature=0)])

if __name__ == "__main__":
    print(run_agent("125 * 17은 얼마야? 그리고 그 결과를 'q1' 메모로 저장해."))
```

코드 블록을 그대로 세면 71줄(공백·주석 포함), 실 코드 라인만 추리면 50줄 남짓이다. 6장에서 완성한 v3는 같은 기준으로 198줄·실 코드 약 140줄이었다. 어느 기준으로 재든 LangChain 버전은 *절반 이하*로 줄어든다. 무엇이 줄었는지 한 번 헤아려 보자.

- **도구 정의:** v3에선 도구 하나당 JSON schema 10줄 + 핸들러 함수 5줄 = 15줄. 셋이면 45줄. `@tool` 버전에선 도구 하나당 5~7줄 정도, 셋이면 약 20줄. **25줄 정도 감소.**
- **클라이언트 호출:** v3에선 `client.messages.create(...)` 한 번에 모델·max_tokens·tools·tool_choice·system을 매번 명시. LangChain에선 `ChatAnthropic(...)` 한 번 초기화하고, `.bind_tools(...)`로 도구를 묶어 두면 그 뒤로는 `.invoke(messages)`만 부르면 된다. **15줄 감소.** 더 중요한 건 `bind_tools`가 하는 일이다. 이 한 메서드 안에서 `BaseTool` 인스턴스들을 모델 SDK가 요구하는 JSON schema로 직렬화하고, 그 schema를 모든 후속 `.invoke` 호출에 자동으로 끼워 준다. 우리가 매 호출마다 `tools=[...]`를 손에 들고 다닐 필요가 없다. 작은 편의 같지만, 도구 목록이 다섯 개를 넘어가기 시작하면 이 자동화의 가치가 빠르게 누적된다.
- **tool 결과 메시지 포맷:** v3에선 `{"role": "user", "content": [{"type": "tool_result", "tool_use_id": ..., "content": ...}]}` 같은 dict를 손으로 조립해야 했다. LangChain에선 `ToolMessage(content=..., tool_call_id=...)` 한 줄. **줄 수 절감과 *가독성* 양쪽으로 이득.** 게다가 OpenAI 모델로 갈아끼우면 같은 `ToolMessage` 객체가 그 SDK에 맞는 dict로 자동 변환된다. 메시지 포맷 차이를 우리가 외워 둘 필요가 없어진다는 점은 두 모델을 같이 다루는 자리에서 진짜 가치가 있다.
- **안전장치 일부:** v3에서 손으로 짰던 retry·fallback·exponential backoff는 `with_retry()`, `with_fallbacks()` 한 줄에 들어간다. **30줄 가까이 절감.**

이 정도 절감이라면 LangChain의 추상화 *과잉* 비판이 좀 누그러진다. 보일러플레이트가 실제로 큰 폭으로 줄어드는 자리가 있다. 그런데 그게 다는 아니다. **줄 수는 줄었지만 *추상의 깊이*는 늘었다.** 다음 절에서 그 깊이를 정확히 재 보자.

## 추상의 깊이 — 세 가지 측정 좌표

"LangChain은 추상이 너무 깊다"는 비판이 자주 나온다. 하지만 "깊다"는 어휘는 모호하다. 한 번 정량적으로 들여다보자. 세 가지 측정 좌표를 제안한다. (a) import 그래프, (b) 호출 트레이스, (c) 추상이 늘어난 *구체적인 자리*.

### 좌표 1: import 그래프 깊이

v3의 import 그래프는 단순했다. `anthropic`, `json`, `time`, `tiktoken` 정도. 직접 의존성 5개 이내. 각 라이브러리의 내부 의존성도 얕다. `pip show anthropic`을 해 보면 직접 의존성이 한 자릿수다.

`mini_agent_lc.py`의 직접 import는 셋뿐이지만 — `langchain_anthropic`, `langchain_core.tools`, `langchain_core.messages` — 그 아래가 깊다. `langchain_core` 한 패키지 안에 60개 이상의 하위 모듈이 있고, `langchain_anthropic`은 `langchain_core`와 `anthropic` SDK 양쪽에 의존한다. 한 번 호출하면 import되는 모듈 수가 v3의 3~4배는 된다. import 시간도 그만큼 늘어난다. 작은 CLI 도구를 짤 때는 이 지연이 체감된다.

### 좌표 2: tool 등록 한 동작의 호출 트레이스

v3에서 도구 하나를 등록하는 과정은 *명시적이고 짧다*. JSON schema를 dict로 짜서 `tools=[...]`에 넣는다. SDK 내부에서 schema가 모델 요청에 직렬화되는 것까지 한두 단계. 디버거로 step into 하면 anthropic SDK 안에서 두세 프레임 정도다.

`@tool` 데코레이터 한 줄 뒤에선 무슨 일이 벌어질까. 한 번 따라가 보자.

1. `@tool`이 데코레이터 함수를 부른다.
2. 데코레이터가 함수 시그니처를 `inspect.signature(...)`로 읽는다.
3. 타입 힌트를 모아 pydantic `BaseModel`을 동적으로 만든다.
4. docstring을 파싱해 description과 인자 설명을 추출한다.
5. 위 결과를 가지고 `StructuredTool` 인스턴스를 생성한다.
6. 그 인스턴스는 `BaseTool`을 상속하고, `BaseTool`은 또 `Runnable`을 상속한다.

그 다음 `bind_tools(TOOLS)`가 부르는 길은 또 한 겹이다. `BaseTool` 인스턴스들을 JSON schema로 변환해, 모델 요청에 함께 보낼 수 있는 모양으로 만든다. 모델 응답이 돌아오면, `AIMessage.tool_calls`에 파싱돼 들어간다. 우리가 `tool_fn.invoke(call["args"])`를 부르면, `BaseTool.invoke`가 돌고, 그 안에서 args를 pydantic 모델로 검증하고, 마지막으로 원본 함수가 호출된다.

이 모든 단계가 한 줄 데코레이터 뒤에 숨어 있다. 좋은 점은 보일러플레이트가 사라진다는 것이고, 나쁜 점은 *내가 짠 함수가 호출되기까지 거치는 LangChain 프레임의 수*가 늘어난다는 것이다. 평소엔 보이지 않다가, traceback에서 한 번 만나는 순간 "이게 다 뭐지?" 싶어진다. 찜찜하다. 그래서 한 번쯤은 LangChain 내부를 따라 들어가 보는 편이 낫다. 적어도 한 번은.

### 좌표 3: 추상이 늘어난 자리 — 구체 사례 네 개

추상의 깊이가 *어디서* 늘어났는지 구체적으로 꼽아 보자. 추상이라는 단어를 손에 잡히게 만들어 두면 비판도 옹호도 정직해진다.

**(1) `@tool`의 inspect 마법.** 위에서 본 그것. 함수 시그니처가 곧 도구의 계약이 된다. 좋은 점도 나쁜 점도 있다. 좋은 점은 보일러플레이트 절감, 나쁜 점은 *런타임까지 가야* 시그니처 문제가 드러난다는 점.

**(2) LCEL `__or__`의 부작용.** `a | b`는 평범한 OR가 아니라 객체를 합성해 새 `RunnableSequence`를 만든다. 의미가 새로 정의된 연산자다. 가독성은 좋지만, 한 번 멈춰 "이건 정의지 실행이 아니다"를 머리에 박아야 한다.

**(3) `RunnableConfig` 전파.** 거의 모든 `Runnable.invoke`는 두 번째 인자로 `config`를 받는다. `config={"callbacks": [...], "tags": [...], "run_name": "..."}` 같은 것들이 그 안에 들어간다. 그리고 이 `config`는 chain을 따라 *자동으로 전파*된다. 명시적으로 넘기지 않아도 children Runnable이 같은 callbacks를 받는다. 편한 동작인데, 명시적으로 짠 코드보다는 *암묵적*이다. "왜 이 자식 chain이 부모의 callback을 받지?" 싶은 순간이 한 번은 온다.

**(4) callback 흐름.** LangSmith trace, 토큰 카운터, 비용 추적 — 이 모든 게 callback 시스템 위에 올라간다. callback handler들은 `RunnableConfig`를 타고 chain 전체를 흐른다. 강력하지만 *간접적*이다. trace를 따라가다 보면, 우리가 짠 코드를 LangChain의 콜백 큐가 둘러싸고 있는 모양이 보인다. 8장에서 이 흐름을 도식으로 잡는다.

이 네 자리에서 추상이 늘어났다. 줄 수가 절반으로 줄어든 *대가*가 여기 있다. 어느 한쪽이 일방적으로 좋은 거래는 아니다. 한 번 직접 짜 본 사람과 그렇지 않은 사람 사이에 LangChain의 *값*이 다르게 보이는 이유가 이것이다. 6장까지 손으로 짠 우리는, 이 거래의 양쪽을 모두 셀 수 있다.

## `with_retry()`와 `with_fallbacks()` — 내장된 토큰 비용

코드 마지막 줄에서 슬쩍 보였던 두 메서드를 한 번 더 들여다보자.

```python
resilient_llm = llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
).with_fallbacks([ChatAnthropic(model="claude-haiku-4-5", temperature=0)])
```

한 줄로 끼우는 회복력. v3에서 우리가 30줄 가까이 손으로 짠 retry 로직과 같은 효과를 낸다. 보일러플레이트 절감 측면에서 정말 큰 이득이다.

그런데 한 번 의심해 보자. "내장된 회복력"이라는 말은 한 줄에 들어가는 *비용*을 가린다. `stop_after_attempt=3`이 무엇을 의미할까. 한 번의 호출이 실패하면 *같은 입력으로 두 번 더 시도한다*는 뜻이다. 입력 토큰은 매 시도마다 다시 든다. 모델 응답 토큰도 마찬가지. 즉 **한 번 실패한 호출의 토큰 비용은 3배**가 될 수 있다. with_fallbacks도 같다. 1차 모델이 실패하면, 같은 입력을 2차 모델에 다시 보낸다. 토큰 비용이 또 든다.

이 사실을 알고 한 줄을 끼우는 것과 모르고 끼우는 것은 다르다. 알고 끼우면 "이 자리는 retry가 정말 가치 있다"는 판단이 들어간다. 모르고 끼우면 *암묵적으로 토큰 청구서가 부풀어 오른다*. 6장에서 우리가 셌던 무한 루프 청구서와 비슷한 구조다. 폭주는 아니지만, 누적이 보이지 않게 늘어난다.

9장에서 이 비판을 본격적으로 다룬다. 지금은 한 가지만 기억해 두자. **LangChain의 한 줄 편의는 한 줄 비용을 가린다.** 편의가 나쁘다는 게 아니라, *가린다는 사실*을 한 번 보는 게 중요하다.

## 다시 한 번, 줄 수 대 깊이의 표

지금까지 본 것을 한 표로 묶어 두자. 8장 이후에 또 인용할 표다.

| 항목 | `mini_agent.py` v3 (Part 1) | `mini_agent_lc.py` (Part 2) |
|---|---|---|
| 본문 줄 수 | 약 198줄 (실 코드 ~140) | 약 71줄 (실 코드 ~50) |
| 직접 import 수 | 4~5개 | 3개 (전이는 60+) |
| 도구 정의(셋) | JSON schema 45줄 | `@tool` 20줄 |
| 모델 호출 코드 | 매 호출 dict 조립 | `.invoke(messages)` |
| 메모리 클래스 | 직접 작성 | (이 장에선 다루지 않음) |
| 재시도·폴백 | 손으로 30줄 | `.with_retry().with_fallbacks(...)` |
| ReAct 루프 | while + try/except | while + try/except (그대로) |
| 토큰·비용 계측 | 직접 카운터 | callback handler (8장에서) |
| traceback 깊이 | 얕다 | 깊다 |
| 호출 스택 추상 단 | 1~2단 | 3~5단 |

이 표를 보면 결론이 한 줄로 정리된다. **LangChain은 보일러플레이트를 줄이는 대신 추상의 깊이를 늘렸다.** 어느 쪽이 더 좋은지는 도구의 본질이 아니라 *맥락*이 결정한다. 작은 CLI 도구를 짠다면 v3 같은 직접 구현이 빠르고 가볍다. 도구·통합·관찰성·평가까지 묶인 큰 시스템을 짠다면 LangChain의 추상이 갚이 든 비용을 회수한다. 같은 도구가 맥락에 따라 다른 점수를 받는다.

## 그런데 이게 LangChain의 진짜 강점일까

마지막으로 한 발 물러서서, 우리가 이 장에서 본 것의 한계를 인정하자.

`mini_agent_lc.py` 한 파일만 두고 비교하면 LangChain의 가치는 *그저 보일러플레이트 절감* 정도다. 71줄 대 198줄. 그 차이를 위해 위에 본 추상의 깊이를 떠안아야 하느냐 — 솔직히 말하면 *그것만으론 손해*에 가깝다. import 시간이 늘고, traceback이 깊고, 디버깅이 한 박자씩 느려진다. 작은 에이전트 하나만 짤 거면, Part 1처럼 손으로 짜는 편이 더 빠르고 더 명료하다.

그렇다면 왜 업계 사람들은 다 LangChain을 쓸까. Hamel Husain의 한 줄을 빌리자면, "처음엔 짜증냈는데, 일해 보니 다들 쓰고 있더라. 알고 보니 그들은 사용자에게 광적으로 귀를 기울인다." 진짜 강점은 mini_agent 수준에서 보이지 않는다. *생태계*에서 드러난다. 수백 개의 통합 모듈, LangSmith의 관찰성, 평가 데이터셋의 운용, 도구 카탈로그 — 이걸 직접 짤 일이 없다는 *시간 가치*가 LangChain의 본전이다. 8장에서 그 자리를 본다.

또 하나, 이 장에서 LCEL을 다뤘지만, 두 가지 패턴 — orchestrator-workers와 evaluator-optimizer — 은 LCEL로 매끄럽지 않았다. LCEL은 DAG, 사이클이 없다. 사이클이 필요한 자리에는 *다른 추상*이 필요하다. 그게 LangGraph다. 10장에서 본격적으로 다룬다.

## 마무리

이 장에서 같은 에이전트를 두 번째로 지었다. 같은 동작, 다른 추상. 줄 수가 절반으로 줄었고, 추상의 깊이는 두세 배로 늘었다. 두 변화를 *동시에* 보아야 LangChain을 정직하게 평가할 수 있다.

기억해 두자. LangChain의 `Runnable` 한 추상이 LCEL의 시작이다. 파이프 `|`는 실행이 아니라 정의다. `@tool`은 보일러플레이트를 가져가는 대신 시그니처·docstring을 진지하게 다루라는 규율을 두고 갔다. `with_retry()` 한 줄은 한 줄짜리 토큰 청구서를 가린다. 다섯 워크플로 중 셋은 LCEL이 깔끔하게 받고, 둘은 LangGraph가 받는다.

이게 LangChain의 *합성* 측면이다. 다음 장에선 *생태계* 측면을 본다. mini_agent 한 파일 수준에선 보이지 않던 LangChain의 진짜 자산 — 통합·도구 카탈로그·LangSmith 관찰성 — 을 한 번 둘러보자. "내가 다시 짤 가치가 없는 것"이 어디까지인지 한 번 가늠해 보자.
