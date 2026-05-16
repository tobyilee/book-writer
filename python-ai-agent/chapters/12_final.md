# 12장. 상태를 저장하고, 사람을 끼우고, 다시 깨우기 — Checkpointer와 HITL

한 시간 전 대화의 다음 턴을 자연스럽게 이어 받는 챗봇을 떠올려 보자. 어제 작성하다 만 보고서의 다음 문단을 오늘 아침 출근해서 같은 자리에서 이어가는 에이전트도 좋다. 비결이 뭘까. 모델이 어젯밤 잠든 사이 더 똑똑해졌을 리는 없다. 진짜 비결은 시시하다 — 그래프가 자기 상태를 어딘가에 적어 뒀기 때문이다. 적어 뒀기 때문에 다시 읽을 수 있고, 다시 읽을 수 있기 때문에 이어갈 수 있다.

그런데 이 *적어 두기*는 우리가 지금까지 짠 모든 에이전트에 빠져 있다. 10장의 mini_agent_lg는 invoke가 끝나는 순간 모든 메시지가 메모리에서 증발했다. 11장의 supervisor 멀티 에이전트도 마찬가지다. 사용자가 페이지를 새로고침하는 순간, 토큰 수백만 개로 합의한 워크플로의 진행 상황이 *깨끗하게* 사라진다. 운영 관점에서 보면 끔찍한 일이다. 응답이 길어질수록, 워크플로가 복잡해질수록 — 즉 *비싸질수록* — 사라질 때의 손실이 커진다. 그렇다면 어떻게 해야 할까. LangGraph의 Checkpointer가 그 답이다.

## 그래프에게 기억을 주는 한 줄

Checkpointer는 추상이 아주 깔끔하다. *그래프 실행의 매 step마다 현재 상태를 외부 저장소에 적는 어댑터.* 그게 전부다. 그래프가 노드를 하나 통과할 때마다 checkpointer가 그 시점의 state를 통째로 직렬화해 저장소에 push한다. 다음 invoke에서 같은 `thread_id`로 들어오면, 저장소에서 가장 최근의 state를 꺼내 그 위에 새 입력을 붙여 이어 간다. 그래프 입장에서는 자기가 어디서 어떻게 깨어났는지 모른다. *그냥 다음 step을 실행한다.* 이게 핵심이다 — 상태 복원이 그래프 내부 로직에 전혀 침투하지 않는다.

말로는 추상적이니 코드로 살펴보자. 10장에서 짠 mini_agent_lg에 SQLite checkpointer를 붙이는 데에 정말 한 줄이면 된다.

```python
# mini_agent_lg_persist.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict, Annotated
from operator import add
from anthropic import Anthropic
import sqlite3

class AgentState(TypedDict):
    messages: Annotated[list, add]

def call_model(state: AgentState) -> AgentState:
    client = Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-7",
        max_tokens=1024,
        messages=state["messages"],
    )
    return {"messages": [{"role": "assistant", "content": resp.content[0].text}]}

# 그래프 정의 (10장과 동일)
graph = StateGraph(AgentState)
graph.add_node("model", call_model)
graph.add_edge("__start__", "model")
graph.add_edge("model", END)

# 여기가 새로 추가된 단 한 줄
conn = sqlite3.connect("agent_state.db", check_same_thread=False)
memory = SqliteSaver(conn)
app = graph.compile(checkpointer=memory)

# 사용
config = {"configurable": {"thread_id": "user-42"}}
app.invoke({"messages": [{"role": "user", "content": "안녕"}]}, config=config)
app.invoke({"messages": [{"role": "user", "content": "내 이름 기억나?"}]}, config=config)
```

두 번째 invoke가 첫 번째의 메시지를 *기억한다.* 사용자가 "내 이름 기억나?"라고 묻기 전에 이미 다른 메시지가 있었고, checkpointer가 그걸 SQLite에 적어 뒀기 때문이다. `thread_id="user-42"`라는 키 한 줄이 두 호출을 같은 대화로 묶어 준다.

물론 첫 invoke에서 사용자가 자기 이름을 말하지 않았다면 모델이 이름을 알 도리는 없다. 그러나 *이전 메시지가 살아 있다*는 사실 자체가 큰 변화다. 메모리에 떠 있던 대화 히스토리를 외부 저장소가 들고 있게 됐다. 프로세스가 죽었다가 살아나도, 서버를 재시작해도, 사용자가 새로고침을 해도 — 상태가 살아남는다. 이걸 운영 시스템에서 처음 체험할 때 느끼는 감정은 안도감에 가깝다. 더 이상 메모리에 모든 걸 들고 다니지 않아도 된다.

## SQLite로 시작하고, Postgres로 이주하자

처음에는 SQLite로 시작하는 편이 낫다. 파일 하나로 끝나니까 의존성이 없고, 로컬 개발에서 디버깅하기 좋다. `agent_state.db`를 SQLite 클라이언트로 열어 보면 그래프가 무엇을 어떻게 적었는지 다 보인다. 실패한 워크플로의 마지막 state를 뜯어 보고 싶을 때 SQLite의 직관성은 큰 도움이 된다. *어떤 노드가 어떤 state를 통과시켰고, 그다음에 무엇이 일어났는가* — 이 모든 게 테이블 몇 개로 정리돼 있다.

그러나 운영으로 넘어가는 순간 SQLite는 한계가 분명하다. 멀티 프로세스에서 동시 쓰기를 잘 못한다. 워커 N대가 같은 SQLite 파일을 두고 경쟁하면 락이 쌓이고, lock contention이 응답 시간을 야금야금 갉아먹는다. 운영 초입에서 이 증상을 처음 만나면 *난감하다.* 그래프 코드는 멀쩡한데 응답이 갑자기 느려지니까, 어디부터 봐야 할지 감이 안 온다. 이 시점에서 Postgres로 이주하자. LangGraph는 `langgraph-checkpoint-postgres` 패키지를 제공하고, API는 거의 동일하다.

```python
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://user:pass@host:5432/agentdb"
with PostgresSaver.from_conn_string(DB_URI) as memory:
    memory.setup()  # 최초 1회 — 필요한 테이블 생성
    app = graph.compile(checkpointer=memory)
```

이주의 비용이 거의 0이라는 점에 주목하자. 그래프 정의는 한 줄도 안 바꾼다. compile 인자만 갈아 끼우면 된다. 이게 Checkpointer 추상의 진짜 가치다 — *저장소를 갈아 끼울 때 비즈니스 로직을 안 바꿔도 된다.* 처음부터 Postgres 띄우고 시작할 필요가 없고, 처음부터 추상화에 짓눌릴 필요도 없다. 작게 시작하고, 필요할 때 옮긴다. 이 두 단계 사이에 코드 변경이 거의 없다는 사실이 우리를 가볍게 한다.

## 한 줄로 얻는 세 가지

`compile(checkpointer=memory)` 한 줄은 단순히 "상태가 저장된다"는 효과 이상을 가져온다. 세 가지가 한 번에 따라온다.

첫째는 **시간 여행 디버깅**이다. checkpointer는 매 step의 state를 다 적어 두므로, 사후에 *임의의 시점*으로 그래프를 되감을 수 있다. `app.get_state_history(config)`로 과거 state 리스트를 가져오고, 그중 하나를 골라 거기서부터 다시 시작할 수 있다. 이게 왜 좋은가? 운영에서 이상한 응답이 나왔을 때, "그 응답 직전의 state는 뭐였지?"를 추측이 아니라 *조회*로 답할 수 있다. 버그를 재현하려고 같은 입력을 다시 흘려 보는 일이 줄어든다. 그 상태를 그대로 가져와서 거기서부터 노드를 다시 실행해 보면 된다. 디버깅이 *추론*에서 *조사*로 옮겨간다.

둘째는 **실패 후 재개**다. 그래프 실행 중 어떤 노드가 예외를 던졌다고 해 보자. invoke는 실패 상태로 끝난다. 그런데 checkpointer는 *예외 직전까지 성공한 노드들의 state는 이미 적어 뒀다.* 그러므로 같은 thread_id로 다시 invoke를 부르면, 그래프는 마지막 성공 지점부터 이어서 실행한다. 사용자 입장에서는 *재시도 한 번에 워크플로가 멈춘 자리에서 일어선다.* 11장의 멀티 에이전트처럼 토큰 100만 개짜리 워크플로가 마지막 단계에서 실패할 때, 이 능력이 비용을 살린다. 처음부터 다시 돌리지 않아도 된다는 사실 하나가 운영 비용 곡선을 결정적으로 바꾼다.

셋째는 **멀티 세션**이다. 같은 그래프를 두고 thread_id만 다르게 invoke하면, 두 세션은 완전히 분리된 대화 히스토리를 갖는다. 한 사용자에게 100명의 사용자가 동시에 접속해도, 각자의 thread_id가 자기 state를 분리해 준다. 이걸 우리가 직접 짤 수도 있다 — 사용자별로 메시지 리스트 dict를 만들고, lock을 걸고, 만료 정책을 적고... 끔찍한 일이다. checkpointer는 이 모든 걸 한 줄에 처리한다.

세 가지가 다 한 줄에서 떨어진다. *어떤 추상이 좋은 추상인가*라는 질문을 받을 때마다 나는 이 한 줄을 떠올린다. 추가 코드 없이 능력 셋을 동시에 얻는 추상. Checkpointer는 그 모범 사례에 가깝다.

## short-term과 long-term 사이의 분담 — Store

그런데 한 가지 자연스러운 의문이 생긴다. 사용자가 어제 한 대화를 오늘 이어가는 건 좋다. 그런데 *사용자에 대해 학습한 사실*은 어디에 둬야 할까? 예컨대 "이 사용자는 답변을 짧게 받는 걸 선호한다", "이 사용자의 회사 이름은 X다" 같은 *세션을 가로지르는 지식*이다. 이런 걸 매번 messages에 끼워 넣는 건 토큰 낭비다. 새 대화를 시작할 때마다 "참고로 이 사용자는 답변을 짧게 받는 걸 좋아한다"는 시스템 프롬프트를 갱신해서 끼워 넣어야 한다면 — 그 데이터는 어디에 저장돼야 할까?

LangGraph는 여기에 별도 추상을 둔다. **Store**다. checkpointer가 *short-term memory*(한 thread 안의 메시지·중간 state)를 다룬다면, Store는 *long-term memory*(사용자별 프로필, 학습된 선호, 누적된 사실)를 다룬다. 둘의 분담을 한 줄로 정리하면 이렇다.

- **Checkpointer:** thread_id 단위로 묶인 *대화의 진행 상태*. 한 invoke 안의 모든 step.
- **Store:** user_id(혹은 namespace) 단위로 묶인 *영속적 사실*. thread를 가로지르는 데이터.

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
app = graph.compile(checkpointer=memory, store=store)

# 노드 안에서 사용
def call_model(state, config, store):
    user_id = config["configurable"]["user_id"]
    profile = store.get(("users", user_id), "profile")
    # profile.value를 system prompt에 합치는 식으로 활용
    ...
    store.put(("users", user_id), "profile", {"prefers_short": True})
    return {...}
```

namespace를 튜플로 잡는 게 살짝 어색해 보이지만, 익숙해지면 편하다. `("users", user_id)`처럼 계층을 표현할 수 있고, prefix로 검색할 수도 있다. Store는 처음에는 InMemoryStore로 시작하다가, Postgres·Redis 백엔드로 옮기는 식으로 진화시키면 된다. checkpointer와 같은 패턴이다 — 저장소를 갈아 끼우는 비용이 거의 0이다.

short-term과 long-term의 분담이 처음에는 과해 보일 수 있다. "왜 하나로 안 합쳐?" 묻고 싶어진다. 하지만 *생명 주기*가 다르다는 사실이 결국 둘을 가른다. 대화 한 건은 일주일이면 만료해도 좋지만, 사용자 프로필은 1년이 가도 살아 있어야 한다. 만료 정책이 다르면 저장소도 다른 편이 낫다. checkpointer는 빠르게 쌓이고 빠르게 사라지는 데이터, Store는 천천히 쌓이고 천천히 사라지는 데이터. 처음에는 둘 다 SQLite에 두더라도, 개념적으로 분리해 두면 나중에 옮길 때 편하다. 기억해두자.

## 사람을 끼우는 자리 — `interrupt()`

여기까지가 *상태 저장*의 이야기다. 이제 한 발 더 나가자. 에이전트가 자율적으로 도구를 호출하다가, *어떤 도구는 정말 위험해서* 사람이 한 번 봐 줘야 할 때가 있다. 예를 들어 사용자의 결제 카드로 1,000만 원을 결제하는 도구, 프로덕션 DB의 레코드를 삭제하는 도구, 외부에 이메일을 발송하는 도구. 이런 destructive action을 사람의 확인 없이 자동으로 흘려보내는 건 *찜찜한 일* 정도가 아니라 *사고의 입구*다.

LangGraph는 이 자리에 `interrupt()`라는 깔끔한 도구를 두고 있다. 노드 안에서 `interrupt(...)`를 부르면 그래프가 그 자리에서 *일시정지*한다. 그래프는 죽는 게 아니라 *멈춘다.* 그리고 checkpointer에 현재 state를 저장한 채 invoke가 returns를 반환한다. 호출자(우리 애플리케이션)는 그 returns를 받아 사람에게 prompt를 띄우고, 사람의 응답을 받아서 `Command(resume=...)`를 그래프에 넘기면, 그래프는 멈춘 자리에서 *재개*한다. 핵심은 이거다 — interrupt와 resume 사이에 *어떤 시간이 흘러도 된다.* 1초가 흐르든, 1시간이 흐르든, 다음 날이 되든. checkpointer가 state를 들고 있으니까.

코드로 확인하자. mini_agent_lg에 "도구 호출 전 사람의 승인을 받는" 노드를 추가한다.

```python
# mini_agent_lg_hitl.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command
from typing import TypedDict, Annotated
from operator import add
from anthropic import Anthropic
import sqlite3, json

class AgentState(TypedDict):
    messages: Annotated[list, add]
    pending_tool: dict | None  # 승인 대기 중인 도구 호출

def call_model(state: AgentState) -> AgentState:
    client = Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-7",
        max_tokens=1024,
        tools=[{
            "name": "delete_record",
            "description": "프로덕션 DB의 레코드를 삭제",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string"}}},
        }],
        messages=state["messages"],
    )
    # 도구 호출이 있으면 pending_tool에 적어 두고 다음 노드로
    for block in resp.content:
        if block.type == "tool_use":
            return {
                "messages": [{"role": "assistant", "content": resp.content}],
                "pending_tool": {"name": block.name, "input": block.input, "id": block.id},
            }
    return {"messages": [{"role": "assistant", "content": resp.content[0].text}]}

def human_approval(state: AgentState) -> AgentState:
    tool = state.get("pending_tool")
    if not tool:
        return state
    # 사람에게 묻고 멈춘다
    decision = interrupt({
        "question": f"도구 '{tool['name']}'을 input={tool['input']}으로 실행할까요? (y/n)",
        "tool": tool,
    })
    if decision == "y":
        # 실제 도구 실행 (생략 — 실 운영에서는 여기서 DB 호출)
        result = f"deleted {tool['input'].get('id')}"
        return {
            "messages": [{"role": "tool", "tool_use_id": tool["id"], "content": result}],
            "pending_tool": None,
        }
    return {
        "messages": [{"role": "tool", "tool_use_id": tool["id"], "content": "사용자가 거부함"}],
        "pending_tool": None,
    }

def needs_approval(state: AgentState) -> str:
    return "human" if state.get("pending_tool") else END

graph = StateGraph(AgentState)
graph.add_node("model", call_model)
graph.add_node("human", human_approval)
graph.add_edge("__start__", "model")
graph.add_conditional_edges("model", needs_approval, {"human": "human", END: END})
graph.add_edge("human", "model")  # 승인 후 모델로 다시

conn = sqlite3.connect("agent_state.db", check_same_thread=False)
app = graph.compile(checkpointer=SqliteSaver(conn))

# CLI 데모
config = {"configurable": {"thread_id": "demo-1"}}
result = app.invoke({"messages": [{"role": "user", "content": "id=42 레코드 삭제해"}]}, config=config)

# interrupt가 발생하면 result에 __interrupt__ 키가 들어 있다
if "__interrupt__" in result:
    payload = result["__interrupt__"][0].value
    print(payload["question"])
    answer = input("> ").strip().lower()  # 사람에게 물어본다
    app.invoke(Command(resume=answer), config=config)  # 멈춘 자리에서 재개
```

코드가 길어 보이지만 핵심은 두 줄이다. `interrupt(payload)`에서 그래프가 멈추고, `app.invoke(Command(resume=answer))`로 다시 깨운다. 그 사이에 사람이 콘솔에서 y/n을 입력한다. 데모는 CLI지만 본질은 같다 — *interrupt에서 멈춘 state는 checkpointer에 저장돼 있고, 어떤 채널로든 사람의 응답을 받아 resume할 수 있다.*

웹 환경이라면 어떻게 짜야 할까. 그래프가 interrupt를 만나면 API 응답으로 `{"status": "pending_approval", "thread_id": "...", "question": "..."}`를 돌려준다. 프런트엔드는 그걸 UI로 띄운다. 사용자가 승인 버튼을 누르면 별도 엔드포인트(예: `POST /resume`)로 thread_id와 응답을 보내고, 서버는 같은 thread_id로 `app.invoke(Command(resume=...))`를 부른다. 그래프는 어디서 멈췄는지를 *자기가 안다.* 우리는 키만 넘기면 된다. 이 패턴이 *webhook 스타일 HITL*이다 — interrupt는 메시지 큐의 ack를 기다리는 작업 같은 모양이 된다.

이 자리에서 destructive action에 대한 회의주의를 한 번 더 강조하자. 도구 박스에 *부작용이 있는 도구*가 단 한 개라도 있다면, 그 도구의 호출 직전에 interrupt를 두는 게 *기본값*이다. "사용자가 너무 많이 클릭해야 해서 UX가 나빠진다"는 반론이 흔한데, 그래도 첫 1~2주는 모든 destructive call에 사람을 끼우는 편이 낫다. 그러면 *모델이 어떤 입력에서 destructive call을 부르는지*에 대한 실데이터가 쌓인다. 그 데이터를 봐야 *어떤 패턴은 자동화해도 안전한지*가 분명해진다. 처음부터 자동화하면 사고가 한 번 나서 자료가 쌓이는데, 그 자료의 비용이 너무 비싸다. 끔찍한 일이다.

## 멀티 사용자·멀티 세션 — thread_id의 역할

지금까지 thread_id를 가볍게 썼지만, 한 번 정색하고 짚고 가자. *thread_id는 단순한 키가 아니라 보안 경계다.* 100명의 사용자가 같은 서비스를 쓴다고 해 보자. 각 사용자의 대화 히스토리가 다른 사용자에게 노출되면 그건 그냥 데이터 유출이다. checkpointer는 thread_id를 키로 state를 분리하지만, *thread_id를 정확히 잡는 책임은 우리에게* 있다.

규칙은 단순하다. *사용자 식별자를 thread_id에 반드시 포함시키자.* 예컨대 `f"user-{user_id}-session-{session_id}"` 같은 형태가 안전하다. 사용자 식별자 없이 session_id만 쓰면, 어떤 버그로 session_id가 충돌할 때 다른 사용자의 대화가 섞일 수 있다. 식별자 합성으로 *물리적으로 분리*하는 편이 안전하다.

여기에 더해 long-term memory의 user_id는 또 다른 차원이다. 같은 사용자가 여러 thread를 가질 수 있고, 그 모든 thread는 같은 user_id의 long-term profile을 공유한다. 그러므로 코드는 보통 이렇게 짠다.

```python
config = {
    "configurable": {
        "thread_id": f"user-{user_id}-session-{session_id}",  # 대화별
        "user_id": user_id,  # 사용자별 long-term
    }
}
```

thread_id와 user_id가 다른 추상이라는 사실을 분명히 해 두자. thread_id는 *대화 한 건*, user_id는 *사람 한 명*. 한 사람이 여러 대화를 가질 수 있고, 각 대화는 자기 short-term state를 가지면서도 *같은 사람의 long-term state*를 공유한다. 이 모델이 처음에는 살짝 복잡해 보이지만, 실제 서비스의 데이터 흐름과 정확히 맞는다. 두 식별자를 잘못 합치면 *남의 대화*나 *남의 프로필*이 노출되는 사고가 난다. 주의해야 한다.

## 실패 후 재개의 정확한 모양

실패 후 재개는 앞에서 잠깐 짚었지만 한 번 더 자세히 알아보자. 그래프가 노드 A → 노드 B → 노드 C 순으로 흐르는데, 노드 B에서 외부 API가 timeout을 던졌다고 하자. checkpointer가 노드 A 직후의 state는 적어 뒀지만, 노드 B는 미완으로 끝났다. 이때 같은 thread_id로 다시 invoke를 부르면 어떻게 될까.

LangGraph는 *마지막 성공 지점에서 이어 간다.* 즉, 노드 A의 결과는 그대로 두고, 노드 B부터 *다시 실행한다.* 노드 A를 처음부터 돌리지 않는다는 점이 중요하다. 노드 A가 비싼 LLM 호출이었거나 외부 API 호출이었다면, 그 비용을 두 번 내지 않는다. 이게 운영 비용 그래프를 결정적으로 바꾼다.

다만 주의할 점이 있다. 노드 B가 *부작용이 있는 작업의 일부*였다면, 재실행이 부작용을 두 번 일으킬 수 있다. 외부 결제 API를 부르는 노드가 timeout을 던졌을 때, 결제가 *이미 일어났지만 응답을 못 받았을* 가능성이 있다. 이 경우 재실행하면 결제가 두 번 발생한다. 그러므로 *부작용이 있는 노드*는 idempotency key를 자기가 들고 다녀야 한다. checkpointer가 자동으로 해 주지 않는다. 노드 안에서 "이번 호출이 이미 처리됐는지 확인" 로직을 짜는 책임은 우리에게 있다. 이 분담을 헷갈리지 말자.

또 한 가지. 재개 시점에 모델의 응답이 *결정론적이지 않다*는 사실도 기억해 두자. 같은 입력을 같은 모델에 두 번 넣어도 출력이 살짝 다를 수 있다(temperature가 0이 아닐 때 특히). 그래서 노드 B의 재실행 결과가 첫 실행과 미묘하게 달라도 놀라지 말자. 이런 비결정성이 디버깅을 어렵게 한다는 점은 LangGraph 운영 후일담에서 자주 나온다. 가능하면 부작용 있는 노드와 LLM 호출 노드를 분리하고, 부작용 있는 노드는 결정론적으로 짜는 편이 낫다.

## 11장의 멀티 에이전트도 같은 도구로

여기까지의 도구들이 11장의 멀티 에이전트와 어떻게 만나는지 한 줄로 짚어 두자. 11장의 supervisor 그래프도 결국 `StateGraph`다. 그러니 같은 `compile(checkpointer=memory, store=store)`로 감싸면 *멀티 에이전트 전체*가 영속화된다. supervisor가 worker로 핸드오프하는 순간의 state, worker가 결과를 들고 돌아오는 순간의 state — 모두 checkpointer에 적힌다. 그래프 안에 `interrupt()` 노드를 하나 끼우면 *멀티 에이전트 워크플로 중간에서도 사람 승인*을 받을 수 있다. 추상이 동일하다는 사실이 여기서 빛난다. 단일 에이전트와 멀티 에이전트가 *같은 영속화 도구*를 쓰니까, 한쪽에서 익힌 패턴이 다른 쪽에서 그대로 통한다.

## 마무리 — 그리고 13장으로

상태 저장·HITL·재개는 LangGraph의 *후반부 가치*다. 그래프라는 추상의 진가가 여기서 드러난다. 한 줄로 추가되는 checkpointer, 노드 안에 끼우는 interrupt, namespace로 분리되는 Store — 이 셋이 운영 가능한 에이전트와 PoC 에이전트의 경계선이다. 데모에서는 이 모든 게 필요 없어 보이지만, 운영에서는 이 셋이 없으면 *모든 invoke가 도박*이 된다. 한 번 실패하면 처음부터, 사용자별 분리도 손으로, 사람 승인도 임시로. 그런 시스템은 운영할 수 없다.

그러니 데모를 갓 넘긴 자리에 있다면, 다음 한 줄을 우선 추가해 보자.

```python
app = graph.compile(checkpointer=SqliteSaver(conn))
```

그리고 사람의 승인이 필요한 자리에 `interrupt(...)`를 한 번 끼워 보자. 이 두 변경만으로 시스템이 *진짜로 운영 가능한 모양*에 한 발 다가선다. 회사 내부 데모에서 외부 출시로 가는 거리의 절반은 이 두 줄에 있다.

자, 짓는 법은 충분히 다뤘다. 단일 에이전트에서 멀티 에이전트로, 그리고 영속화·HITL까지. 그런데 한 가지 빠진 질문이 있다. *이 에이전트가 잘 도는지 어떻게 측정하지?* 평가가 없으면 개선의 방향을 모른다. *운영 중에 무슨 일이 일어나는지 어떻게 보지?* 관찰성이 없으면 사고가 나도 원인을 모른다. 다음 장에서는 이 두 가지를 다룬다 — 평가·관찰성. PoC를 넘어 운영으로 들어가는 마지막 한 발이다. 13장에서 이어 가자.
