# 3장. 도구를 여러 번, 스스로 결정해서 — ReAct 루프 짓기

처음 ReAct 논문을 폈을 때를 떠올려보자. 한가운데 *"interleave reasoning traces and actions"*라는 한 줄이 박혀 있다. 우리말로 옮기면 "추론과 행동을 교차시킨다" 정도 되겠다. 보고 있자면 뭔가 거창한 알고리즘이 숨어 있을 것 같다. 도식이 그려진 페이지를 넘기면 Thought, Action, Observation이라는 단어들이 도형 안에서 화살표로 이어지고, 다시 처음으로 돌아가는 그림이 나온다. 이쯤 보면 머리가 살짝 지끈거리기 시작한다. 도대체 이걸 어떻게 코드로 옮기란 말인가.

그런데 막상 한 번 짜보고 나면 허탈해진다. 코드로 옮긴 ReAct는 **while 루프 하나**다. 그 안에서 SDK 호출 한 번 하고, 도구가 호출됐으면 실행해서 결과를 다시 메시지에 넣고, 또 호출하고, 또 넣고. 도구를 더 부르지 않겠다고 모델이 결정하면 루프를 빠져나온다. 끝이다. 2장에서 한 바퀴짜리 round-trip을 짰는데, 이제 그걸 **while로 감싸기만 하면 된다**. 이렇게 말해도 될까? 사실 그렇다. 그게 ReAct 본체다.

## Thought, Action, Observation은 어디로 갔는가

논문의 도식에는 분명히 세 단어가 등장하는데, 코드를 짜보면 그 세 단어가 어디에도 명시적으로 나타나지 않는다. 처음 짜는 사람은 여기서 한 번 멈칫한다. "Thought을 출력하라"고 모델에게 시키는 코드는 어디 있지? Action은 또 어떻게 표현하지? 이 질문이 생긴다면 자연스러운 일이다. 한 번 답을 정리하고 가자.

SDK 기반으로 짤 때 세 단어는 다음과 같이 매핑된다.

- **Thought** — 모델이 응답으로 돌려주는 자연어 텍스트. 모델이 도구를 부를지 말지 머릿속에서 굴리는 흔적이 여기에 묻혀 있다. 우리가 따로 "생각해라"라고 시키지 않아도 알아서 일부 응답을 텍스트로 남긴다.
- **Action** — 응답에 들어 있는 `tool_calls`. "나 이 도구를 이 인자로 부르고 싶다"는 모델의 선언이다.
- **Observation** — 우리가 도구를 실제로 실행한 뒤, 그 결과를 `tool` 역할 메시지로 모델에게 돌려주는 부분이다. "네 행동의 결과가 이거다"라고 보여주는 셈이다.

그러니까 우리가 손으로 만들어야 하는 건 사실 **Observation 한 종류뿐**이다. Thought와 Action은 모델이 응답에 함께 담아서 돌려준다. 우리는 그 응답에서 `tool_calls`를 뽑아 실행하고, 결과를 다시 모델에 돌려주기만 하면 된다. 한 바퀴를 그렇게 굴리는 게 2장에서 한 일이었다. 이제 그 한 바퀴를 *반복*시키자.

## 가장 단순한 ReAct 루프

이 정도면 코드가 보이기 시작한다. 한 번 가장 단순한 골격을 짜보자.

```python
messages = [{"role": "user", "content": user_message}]

while True:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tool_specs,
        messages=messages,
    )

    # 모델 응답을 history에 추가
    messages.append({"role": "assistant", "content": response.content})

    # 도구 호출이 더 없으면 종료
    if response.stop_reason != "tool_use":
        break

    # tool_calls를 하나씩 실행해서 tool_result로 넣기
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = dispatch(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

    messages.append({"role": "user", "content": tool_results})
```

이게 ReAct의 본체다. 코드를 가만히 들여다보고 있으면 좀 허탈할 정도다. 정말 이게 다인가? 그렇다. 이게 다다. 종료 조건이 `stop_reason != "tool_use"` 한 줄이고, 그 외에는 한 바퀴 round-trip을 무한히 반복하는 구조다. 2장의 한 바퀴를 `while True`로 감싸기만 한 셈이다.

그런데 가만 보면 위 코드에는 *위험한 구석*이 있다. `while True`다. 모델이 도구를 영원히 부르겠다고 결심하면, 이 루프는 영원히 돈다. 단순히 무한 루프로 끝나는 게 아니라, **한 바퀴마다 SDK 비용이 발생한다**. 4시간 뒤에 검출하면 누적 청구액이 수천 달러 단위로 찍힌다는 보고가 이미 여러 곳에 있다. 한 번의 호출에 토큰 500개씩 쓰던 작업이, 갇혀 15번 도는 동안 누적 4M 토큰으로 부풀어 버린 사례도 있다. 그러니 가장 단순한 루프조차 무조건 안전장치를 같이 갖고 가야 한다. 이 얘기는 잠시 뒤에 다시 한다.

한 가지 더 짚어두자. 위 골격 코드를 처음 보면, "모델이 한 번에 도구를 *여러 개* 부르면 어떡하지?"라는 의문이 들 수 있다. 결론부터 말하면, 모델은 한 응답에 `tool_use` 블록을 *여럿* 담아 돌려줄 수 있다. 우리 코드는 그 블록들을 차례로 모두 실행해서 `tool_results`에 *전부 담아* 한 번에 돌려주면 된다. 이걸 *병렬 도구 호출*이라고 부른다. 모델 입장에서는 "이번 바퀴에 셋을 동시에 부르겠다"는 선언이고, 우리 입장에서는 순서대로 실행해 결과를 한 번에 모아주는 셈이다. 한 바퀴 루프 안에서 자연스럽게 처리된다.

## 도구 세 개로 확장하기

루프가 한 바퀴만 도는 동안에는 도구가 하나만 있어도 충분했다. 2장에서는 `get_weather` 하나로 끝났다. 그런데 루프를 돌게 한 이상, 도구가 하나뿐이면 모델이 *결정할 게 없다*. 부르거나, 안 부르거나. 이 단조로움으로는 ReAct의 묘미가 안 살아난다. 도구를 *세 개로* 늘려보자. 그래야 모델이 "어떤 도구를 부를지" 고민하는 모습을 직접 관찰할 수 있다.

세 개로 늘리되 의도는 명확히 갈라놓자. 계산기, 가짜 웹 검색, 메모. 세 도구의 역할은 서로 겹치지 않는다.

- **calc** — 산술식을 받아 결과를 돌려준다. `2 * (15 + 7)` 같은 입력에 `44`를 돌려주는 식이다. 모델이 자기 머리로 계산을 시도하다 틀리는 경우가 흔하므로, 계산은 도구로 빼는 편이 낫다.
- **web_search** — 키워드를 받아 검색 결과를 돌려주는 척한다. 사실은 미리 준비한 가짜 결과를 반환한다. 외부 API를 붙이면 책의 코드가 환경에 의존하기 시작하므로, 입문 단계에서는 가짜로 충분하다. 진짜 검색 API로 갈아 끼우는 일은 함수 본체만 바꾸면 된다.
- **memo** — 어떤 메모를 받아 어딘가에 적어둔다. 결과는 `"ok"` 정도다. 부수 효과만 있고 돌려줄 정보가 별로 없는 도구의 전형적인 모양이다.

세 개로 늘리면 모델은 비로소 *고를* 일이 생긴다. "이 질문에는 어떤 도구를 먼저 부를까", "둘 다 부를까", "셋 다 부를까", "아예 안 부를까". 이게 ReAct가 "스스로 결정한다"고 부를 만한 부분이다. 우리는 그 결정의 결과만 받아서 도구를 실행하면 된다.

도구가 셋 정도일 때는 모델이 비교적 잘 고른다. 그런데 그 수가 늘어나면 어떻게 될까? OpenAI의 함수 호출 한도는 128개라고 알려져 있지만, 실용적으로 도구가 20~30개를 넘어가기 시작하면 모델의 선택 정확도가 떨어지는 경향이 보고된다. 도구 묶음을 잘 *큐레이션*하는 일은 그래서 중요하다. 이 책에서는 *작게 시작해서 필요할 때만 늘리는* 방향을 권한다. 우선 셋으로 시작해, 손에 익을 때까지 굴려보자.

## 모델은 어떻게 결정하고, 어떻게 실패하는가

이제 다소 신경 쓰이는 얘기를 하자. 모델이 "결정한다"고 했는데, 그 결정이 *항상 잘 되리라는 보장은 없다*. 직접 짠 루프를 돌려보면 즉시 알게 된다. 모델은 가끔 헛소리를 한다. 그게 도구 호출에 어떻게 나타나는지 세 가지 패턴으로 정리해두자. 직접 짠 사람만 보는 풍경이다. 프레임워크 뒤에 가려 있을 땐 잘 안 보인다.

첫째, **존재하지 않는 도구 이름**을 부른다. 우리가 등록한 건 `calc`, `web_search`, `memo` 셋인데, 응답에는 `calculator`나 `search_web` 같은 이름이 들어 있다. 비슷한 이름을 지어내는 셈이다. 디스패치 테이블에서 키 조회가 실패하므로, 우리 쪽에서 `KeyError`로 떨어진다. 여기서 그대로 크래시 내면 루프는 멈춰버린다. 그렇다고 무시하고 다음 바퀴로 넘기면 모델은 왜 호출이 안 됐는지 모른다. 그래서 답이 명확하다. **`tool_result`에 에러 메시지를 담아 모델에게 돌려보낸다**. "그런 이름의 도구는 없다. 등록된 이름은 이 셋이다"라고 알려주면, 다음 바퀴에서 모델이 알아서 고친다. 놀라울 정도로 잘 고친다.

둘째, **JSON이 깨진 채로** 도구를 부른다. SDK가 인자를 파싱해서 구조화된 dict로 돌려주는 편이 대부분이라 직접적인 충돌은 드물지만, 인자 *내용물*이 깨지는 경우는 흔하다. `calc`의 `expression` 필드에 `"2 * (3 + "` 같은 미완성 표현식이 들어 있다든지, 숫자가 들어와야 할 자리에 한국어 문장이 들어 있다든지. 이때도 답은 같다. 도구 실행 중에 잡힌 예외를 문자열로 직렬화해서 `tool_result`에 담아 돌려보낸다. 그러면 모델이 다음 바퀴에서 인자를 고친다.

셋째, 도구가 멀쩡하게 실행됐는데 **모델이 결과를 이상하게 해석**한다. 이건 코드로는 손쓰기 어려운 영역이다. 도구 결과 자체가 빈약하거나, 형식이 모호하거나, 두 도구의 결과를 모델이 헷갈리는 식이다. 이걸 줄이는 길은 결국 *도구 설계* 쪽에 있다. 2장에서 다룬 "Intern Test"가 다시 떠오르는 대목이다. 인턴이 봐도 알아볼 만한 도구 결과인가? 그렇지 않다면 결과 포맷부터 손보는 편이 낫다.

세 패턴을 정리해보면 결국 공통점이 보인다. **에러를 던지지 말고 모델에게 돌려준다.** 도구 호출은 일종의 대화다. 도구 쪽에서 일방적으로 끊지 말고, "이렇게 잘못됐다"고 알려주면 모델이 알아서 다시 시도한다. 직접 짠 루프의 가장 큰 권한 중 하나가 이 부분이다. 프레임워크 안에서는 보통 묻혀 있다. 어떤 라이브러리는 잘못된 호출에서 조용히 크래시를 내고, 어떤 라이브러리는 알 수 없는 형태로 묻어버린다. 직접 짜면 이 셋이 *눈에 들어온다*. 모델의 결정이 어디서 어떻게 빗나가는지를 보고 나면, 도구 설명문을 다듬을 점도, 시스템 프롬프트로 가드레일을 칠 지점도 자연스럽게 보인다.

한 가지 짚어두자. 우리는 지금 모델을 "결정자"로 두고, 도구는 "행동의 결과"로만 두고 있다. 둘의 역할 분리가 흐릿해지면 코드도 흐릿해진다. 예를 들어 도구가 결과 안에 *모델이 따라야 할 지시문*을 넣고 있으면 — "다음 단계는 X를 해라" 같은 — 모델은 그걸 명령으로 받아들일 수 있다. 의도와 다른 동작이 나오기 쉽다. 도구 결과는 *데이터*에 머무는 편이 바람직하다. 명령은 시스템 프롬프트와 사용자 메시지 쪽에 둔다.

## 종료 조건의 세 가지 얼굴

자, 다시 위험한 구석으로 돌아오자. `while True`. 종료는 누가 시키지?

ReAct 루프의 종료는 세 가지 모양으로 들어온다. 셋을 헷갈리지 말자.

첫째, **자연 종료**. 모델이 더 이상 도구를 부르지 않겠다고 결정한 경우다. `stop_reason`이 `"end_turn"`이거나, 응답 안에 `tool_use` 블록이 하나도 없다. 모델이 사용자에게 줄 최종 답을 정리했다는 뜻이다. 이게 가장 흔한 정상 종료다.

둘째, **강제 종료**. 우리가 정해둔 `max_iterations` 한도를 채운 경우다. ReAct 루프는 모델의 결정에 종료를 맡기는 구조라서, 모델이 도구를 계속 부르겠다고 결심하면 우리 쪽에서 끊는 길밖에 없다. 이 한도가 없으면 운영 중에 한 번이라도 모델이 *루프에 갇히는 순간* 청구서가 폭주한다. 입문 단계에서는 10번이나 15번 정도로 잡아두고, 한도에 도달했을 때 "안전을 위해 루프를 강제로 끊었다"는 표시를 사용자에게 남기는 편이 바람직하다.

셋째, **비정상 종료**. 우리가 안 잡은 예외가 위로 올라온 경우다. 네트워크 끊김, SDK 라이브러리 자체의 버그, 디스패치 함수 안의 예측 못한 에러. 이건 본질적으로 *코드의 결함*이거나 *외부 환경의 사고*다. 사용자에게 보낼 답이 없다. 입문 단계에서는 try/except로 잡아 로그를 남기고 깔끔하게 끊으면 충분하다.

세 종료를 *코드에서 다르게 다뤄야 한다*는 점은 기억해두자. 자연 종료는 결과를 그대로 돌려주면 되지만, 강제 종료는 "왜 끊었는지" 알려주는 편이 친절하고, 비정상 종료는 흔적을 남겨야 한다. 잘 짠 루프는 셋의 차이를 호출자에게 명확히 노출한다. 함께 묶어서 던지면 운영 중에 무슨 일이 났는지 거꾸로 추적하기가 번거롭다.

여기에 한 가지 더 얹어두자. iteration 한도만이 안전장치는 아니다. **토큰 한도, 시간 한도, 비용 한도**를 함께 두는 편이 안전하다. 누군가 이걸 "하드 캡 4종 세트"라고 부르더라. 책의 v1에서는 우선 iteration 캡만 박아두고 가지만, 운영 단계에 가까워질수록 나머지 셋도 차례로 채워가는 편이 좋다. 일단 머릿속에 자리만 잡아두자.

## mini_agent.py v1 — 책의 첫 정본

이쯤 되면 손에 잡힌 조각들을 하나로 모을 차례다. 도구 N개를 받고, ReAct 루프를 돌고, 세 종료를 다르게 다루는 함수를 짜보자. 이름은 `mini_agent.py`로 한다. **이 파일은 책 전체의 캐논 코드의 시작점이다**. Part 1에서 v3까지 다듬어가고, Part 2에서 LangChain으로, Part 3에서 LangGraph로 다시 짓는다. 다 같은 골격을 가져간다. 그러니 v1부터 깔끔하게 박아두자.

```python
# mini_agent.py — v1: ReAct loop
# 책 "맨손으로 짓는 AI 에이전트" 정본 코드
# Part 1에서 v3까지 발전하고, Part 2에서 LangChain, Part 3에서 LangGraph로 다시 짓는다.

from anthropic import Anthropic
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    func: Callable[..., Any]


def _to_specs(tools: list[Tool]) -> list[dict]:
    return [
        {"name": t.name, "description": t.description, "input_schema": t.input_schema}
        for t in tools
    ]


def run_agent(
    user_message: str,
    tools: list[Tool],
    model: str = "claude-sonnet-4-6",
    max_iterations: int = 10,
) -> dict:
    client = Anthropic()
    dispatch = {t.name: t.func for t in tools}
    tool_specs = _to_specs(tools)
    messages = [{"role": "user", "content": user_message}]

    for step in range(max_iterations):
        try:
            response = client.messages.create(
                model=model, max_tokens=1024,
                tools=tool_specs, messages=messages,
            )
        except Exception as exc:
            return {"status": "error", "step": step, "reason": str(exc)}

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            text = "".join(b.text for b in response.content if b.type == "text")
            return {"status": "ok", "step": step, "answer": text}

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            func = dispatch.get(block.name)
            if func is None:
                payload = f"error: unknown tool '{block.name}'. available: {list(dispatch)}"
            else:
                try:
                    payload = str(func(**block.input))
                except Exception as exc:
                    payload = f"error: {type(exc).__name__}: {exc}"
            results.append({
                "type": "tool_result", "tool_use_id": block.id, "content": payload,
            })

        messages.append({"role": "user", "content": results})

    return {"status": "capped", "step": max_iterations,
            "reason": f"max_iterations={max_iterations} reached"}


# ─── 데모 ───────────────────────────────────────────
if __name__ == "__main__":
    notes: list[str] = []

    def calc(expression: str) -> str:
        return str(eval(expression, {"__builtins__": {}}, {}))

    def web_search(query: str) -> str:
        return f"(fake) top result for '{query}': 서울 인구는 약 940만명."

    def memo(text: str) -> str:
        notes.append(text)
        return "ok"

    tools = [
        Tool("calc", "산술식을 계산한다.",
             {"type": "object", "properties": {"expression": {"type": "string"}},
              "required": ["expression"]}, calc),
        Tool("web_search", "웹을 검색해 짧은 요약을 돌려준다.",
             {"type": "object", "properties": {"query": {"type": "string"}},
              "required": ["query"]}, web_search),
        Tool("memo", "한 줄짜리 메모를 적어둔다.",
             {"type": "object", "properties": {"text": {"type": "string"}},
              "required": ["text"]}, memo),
    ]

    result = run_agent(
        "서울 인구를 찾아서 2026에 곱한 값을 알려주고, 그 숫자를 메모에 적어둬.",
        tools=tools,
    )
    print(result)
    print("notes:", notes)
```

한 번 천천히 따라가 보자. 함수 시그니처가 받는 건 사용자 메시지, 도구 리스트, 모델 이름, 그리고 최대 반복 횟수다. `dispatch`는 이름 → 함수 매핑이고, `tool_specs`는 SDK에 넘길 도구 명세 리스트다. 루프 안에서 SDK 호출은 try로 감싸 비정상 종료를 분리한다. `stop_reason`이 `"tool_use"`가 아니면 자연 종료 — `status: ok`로 답을 돌려준다. 도구 호출이 있으면 디스패치하고, 미등록 이름이면 친절한 에러 문자열을, 도구 안에서 예외가 나면 `type(exc).__name__: 메시지` 형태로 잡아 모델에 돌려준다. 루프가 한도까지 채워지면 `status: capped`로 끝낸다.

세 종료가 함수의 반환값에 *명시적으로* 드러난다는 점을 봐두자. 호출자는 `status` 필드 하나만 보고 다음 행동을 결정할 수 있다. 로그를 어떻게 남길지, 사용자에게 어떻게 보여줄지가 갈린다. 이게 *루프를 직접 짠 사람만 누리는 권한*이다. 프레임워크 안에서 한 줄로 호출하면 이 세 가지가 한 묶음으로 추상화되어, 운영 중에 무슨 종료가 일어났는지 거꾸로 추적하기가 번거로워진다.

데모에서는 도구 셋을 등록하고 한 가지 질문을 던진다. "서울 인구를 찾아서 2026에 곱한 값을 알려주고, 그 숫자를 메모에 적어둬." 잘 돌아가면 모델은 `web_search`로 인구를 가져오고, `calc`로 곱셈을 하고, `memo`로 결과를 적어둔다. 한 바퀴에 한 도구씩, 적어도 세 바퀴는 돈다. 운이 나쁘면 도구 이름을 잘못 부르거나 인자를 깨뜨릴 수도 있는데, 우리 코드는 그걸 모델에게 다시 돌려보내고 한 번 더 시도하도록 둔다. 어떻게 도는지 직접 손에 받아보길 권한다. 한 번 굴려보면 ReAct가 "여러 번, 스스로 결정해서" 도구를 부른다는 말이 비로소 손에 잡힌다.

`eval`을 도구 안에 박아둔 게 마음에 걸린다면 좋은 직감이다. 운영 단계에서는 *반드시 안전한 표현식 평가기*로 갈아 끼워야 한다. 입문 데모용으로는 빌트인을 차단한 `eval`도 한 줄 짜리로 의도가 잘 드러나서 가져왔지만, 사용자 입력을 그대로 `eval`에 넣는 코드는 운영에 두면 끔찍한 일이다. 잊지 말자.

## 한계와, 4장 예고

v1이 손에 잡혔다. 그런데 ReAct만 알면 모든 문제가 풀리는가? 그렇지 않다. ReAct는 "한 단계씩 추론하고 도구를 부르면 잘 풀리는 문제"에 강하다. 사실 그 범위가 꽤 넓어서, 입문 단계에 만나는 대부분의 작업은 ReAct만으로 충분하다. 하지만 어떤 문제는 다르게 생겼다. 예를 들어 단순 CoT로 4%밖에 못 푸는 Game of 24 같은 탐색 문제는, 같은 모델로도 트리 탐색을 도입하면 74%까지 올라간다. ReAct의 *한 줄짜리* 추론 흐름으로는 닿기 어려운 영역이다. 또 어떤 작업은 *실패를 기억해 다음 시도를 고치는* 패턴이 더 효율적이다. 코드 작성 같은 영역이 그렇다.

이런 영역의 *학술 변종* — Plan-and-Solve, Reflexion, Tree of Thoughts — 은 다음 장에서 본격적으로 다룬다. 흥미로운 점은, 셋 다 우리 `mini_agent` v1의 *루프 모양만 살짝 비틀어* 만들 수 있다는 사실이다. plan 단계를 앞에 끼우면 Plan-and-Solve가 되고, 시도 실패의 메모를 다음 호출의 시스템 프롬프트에 끼우면 Reflexion이 되고, 응답을 여러 갈래로 분기시키면 Tree of Thoughts가 된다. v1을 잘 박아두면 변종 셋이 차례로 자연스럽게 따라온다.

## 마무리

손에 쥔 것들을 잠깐 정리하고 가자. 2장의 한 바퀴 round-trip을 while로 감싸 ReAct 루프를 만들었다. 도구를 셋으로 늘려 모델이 "고를" 일을 줬다. 실패 모드 세 가지 — 환각 이름, 깨진 인자, 모호한 결과 — 를 모델에 돌려보내는 방식으로 다뤘다. 종료 조건 세 가지 — 자연·강제·비정상 — 를 함수 반환값에 명시적으로 노출했다. 그리고 `mini_agent.py` v1을 손에 쥐었다.

이 v1은 책 전체의 *정본*이다. 다음 장에서 학술 변종 셋을 v1의 변형으로 짠다. 그 뒤로 v2에서는 메모리와 컨텍스트 관리를, v3에서는 비용·시간·토큰 캡까지 얹어 운영에 가까워지는 모양으로 키운다. Part 2에서는 같은 골격을 LangChain으로 다시 짓고, Part 3에서는 LangGraph로 또 한 번 짓는다. 그때마다 우리는 *바닥에 무엇이 있는지를 알고* 추상화 위로 올라선다. v1이 손에 있다는 것의 가치가 거기 있다.

기억해두자. 우리가 짠 80줄짜리 함수는 단순히 데모가 아니라, 책의 끝까지 들고 갈 *축*이다. 다음 장으로 넘어가기 전에, 한 번 실제로 데모를 돌려보고, 도구 이름을 일부러 틀려보고, `max_iterations`를 2로 줄여보고, 사용자 메시지를 도구가 필요 없는 인사말로 바꿔보길 권한다. 자연 종료, 강제 종료, 모델의 자기 교정이 어떤 식으로 일어나는지 손으로 느껴두면, 4장의 변종들이 훨씬 가볍게 다가올 것이다.
