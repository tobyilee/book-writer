# 5장. 기억의 모양 — 대화 history는 어디서 잘리고, 어디로 흘러가는가

메모리 관련 논문을 한 번이라도 들춰본 사람이라면, 첫 페이지에 등장하는 네 개의 단어를 본 적이 있을 것이다. *short-term, long-term, episodic, semantic.* 단기 기억, 장기 기억, 일화 기억, 의미 기억. 인지과학 교과서에서 그대로 빌려 왔다 해도 어색하지 않은 분류다. 2026년 3월에 나온 메모리 survey도 첫 절을 이 네 단어로 시작한다. 도식에는 동그라미 네 개가 사이좋게 배치돼 있고, 사이로 화살표가 오간다. 마치 인간 뇌의 회로도 같다.

그런데 그 도식 옆에 있는 코드를 들여다보면, 일순간 허탈하다. 도식이 약속한 화려함은 어디에도 없다. 모든 게 결국 한 가지 질문으로 환원된다. "이 리스트를 어디서 잘라야 하지?" 컨텍스트 윈도우가 가득 차기 전에 messages 배열에서 무엇을 떼어내고, 무엇을 살리고, 떨어진 조각은 어디에 보관할 것인가. 멋진 이름에 비해 코드로 내려와서 만나는 풍경은 좀 소박하다.

이 소박함이 사실 좋은 소식이다. 메모리라는 단어가 만든 거창한 인상에 짓눌릴 필요가 없다는 뜻이니까. 우리 손에 든 `mini_agent.py` v1은 매 iteration마다 `messages.append(...)`를 두 번씩 한다. 다섯 번 루프를 돌면 메시지가 열 개 늘어나고, 작업이 길어지면 백 개가 쌓이는 일도 어렵지 않다. 그렇게 컨텍스트가 부풀면 어느 순간 SDK가 "토큰 한도 초과"를 던진다. 그 순간 우리에게 필요한 건 *어떻게 자를 것인가*의 답이지, 인지과학적 통찰이 아니다. 차분히 한 번 살펴보자.

## 네 개의 동그라미를 코드로 옮기면

학술적 분류를 우리 코드 위에 한 번 포개 보자. 그러면 각 동그라미가 어디에 해당하는지가 또렷해진다.

**Short-term memory**는 현재 진행 중인 대화의 컨텍스트다. 우리 코드로 치면 `messages` 리스트 그 자체다. 모델이 매 호출마다 그대로 보는 그것. 한 세션이 끝나면 함께 사라지고, 컨텍스트 윈도우라는 물리적 한계에 묶여 있다. 가장 직관적인 메모리이자, 가장 자주 터지는 메모리다. 우리가 5장에서 본격적으로 손을 댈 자리도 거의 이 영역이다.

**Long-term memory**는 세션을 가로질러 살아남는 정보다. 사용자의 선호, 과거 대화의 요약, 자주 쓰이는 사실. 디스크에 저장되든 데이터베이스에 들어가든, 한 세션이 끝나도 다음 세션에서 다시 꺼내 쓸 수 있는 모든 것이 여기에 속한다. 우리 v1에는 아직 이 자리가 비어 있다. 5장에서 가장 단순한 모양으로 한 번 채워 본다.

**Episodic memory**는 과거 trial의 자기 메모다. 4장에서 Reflexion을 다룰 때 잠깐 등장했다. 어제 시험에서 무엇을 틀렸는지를 적어 두고, 오늘 시험 시작 전에 한 번 훑는 그 오답 노트. trial 단위로 누적되며, 보통 자연어 한 문단의 모양을 띤다. 4장의 `run_reflexion` 함수가 `memo` 변수에 누적하던 텍스트가 바로 이것이다. 메모리 분류학으로 보면 episodic이라는 자리에 들어간다.

**Semantic memory**는 사실과 지식의 저장소다. 위키피디아의 한 페이지, 사내 문서의 한 절, 제품 매뉴얼의 한 챕터. 도메인 지식 전반이 여기 들어간다. 이걸 모델이 필요할 때 꺼내 쓰는 방식이 흔히 말하는 RAG(Retrieval-Augmented Generation)다. 그런데 솔직히 말하면, semantic memory는 한 챕터로는 부족하다. retrieval 전략, 임베딩 모델 선택, 청크 단위 설계, 평가 메트릭이 줄줄이 따라붙는다. 그래서 이 책에서는 13장과 부록 B에 두 번 걸쳐 별도로 다루기로 한다. 5장에서는 *위치만 잡고* 넘어간다. 그 선언만 분명히 해두자.

네 동그라미를 정리해 보면, 5장에서 본격적으로 손대는 건 short-term 하나뿐이다. long-term은 가장 단순한 외부 저장소로 한 번 흘려보내고, episodic은 4장에서 만난 모양을 재인용하고, semantic은 위치만 표시하고 미룬다. 욕심을 부리지 않는 편이 낫다. 한 챕터에 모든 메모리를 다 넣으려고 하면 결국 어느 하나도 손에 안 잡힌다.

## 가장 단순한 전략 — sliding window

자, 이제 short-term으로 손을 옮겨 보자. messages 리스트가 길어진다. 어디서 자를까?

가장 단순한 답이 sliding window다. "마지막 N턴만 살리고 앞은 버린다." 다섯 글자로 끝나는 전략이다. 코드로 옮기면 더 짧다.

```python
def trim_window(messages, max_turns=10):
    return messages[-max_turns:]
```

이게 다다. 매 호출 직전에 messages를 이 함수에 통과시키면 된다. 한 줄짜리 슬라이스. 이 전략이 단순하다고 무시할 게 아니다. 작업이 *단발성*이거나 *최근 컨텍스트만으로 충분히 풀리는* 경우에는 이게 거의 최선이다. 챗봇이라기보다 "한 가지 작업을 도구로 처리하는 에이전트"라면, 멀리 떨어진 메시지를 굳이 들고 갈 이유가 없다.

물론 단점은 명확하다. *오래된 정보는 통째로 사라진다.* 사용자가 첫 메시지에서 "내 이름은 토비고, 오후 3시까지 끝내야 해"라고 말했는데, 윈도우가 그 메시지를 떨궈 버리면 모델은 사용자 이름도 마감 시간도 잊는다. 다섯 번째 도구 호출에서 문맥이 통째로 빠진 채로 결과를 내놓는다. 난감한 상황이다.

그래서 sliding window는 *작업의 컨텍스트가 좁은 범위 안에서 닫히는* 경우에 잘 맞는다. 대부분의 ReAct 루프가 여기 해당한다. 한 작업이 5~10 iteration 안에 끝나고, 작업의 결정적 정보가 그 안에 다 들어 있다면, 윈도우 한 줄로 충분하다. 한 가지 팁을 짚어두자. 시스템 프롬프트와 *맨 처음 사용자 메시지*는 윈도우에서 빼지 말자. 그 둘은 작업의 정체성 같은 것이라, 윈도우가 떨궈 버리면 모델이 자기가 뭘 하고 있었는지 헷갈리기 시작한다.

```python
def trim_window(messages, max_turns=10):
    if len(messages) <= max_turns + 1:
        return messages
    # 첫 user 메시지는 보존, 나머지에서 마지막 max_turns만
    return [messages[0]] + messages[-max_turns:]
```

이렇게 두 줄로 늘어나는 정도가 적당하다. 시스템 프롬프트는 별도의 인자로 빠지는 경우가 많으니, 여기서는 첫 사용자 메시지를 anchor로 본다. 만약 시스템 프롬프트가 messages 리스트 안에 들어가는 SDK라면 인덱스 0과 1을 모두 보존하면 된다.

## 요약으로 갈음하기 — summary buffer

작업이 길어지면 sliding window의 한계가 점점 거슬리기 시작한다. 떨어져 나간 메시지에는 *분명히* 쓸 만한 정보가 있었는데, 그게 통째로 사라진 채로 다음 iteration에 진입하는 게 찜찜하다. 모델이 같은 도구를 다시 부르거나, 사용자가 이미 답했던 질문을 또 던지는 상황이 종종 벌어진다.

여기서 떠오르는 보완책이 summary buffer다. 발상은 단순하다. "오래된 메시지를 *버리지 말고* 한 줄로 요약해서 한 자리에 박아두자." 마치 회의 끝에 "오늘 결정된 사항은 셋이다"라고 적어 두는 식. 다음 iteration에 들어갈 때 모델은 그 요약과 최근 N턴을 함께 본다.

코드 모양을 한 번 잡아보자.

```python
def trim_summary(messages, max_recent=6, summarizer=None):
    if len(messages) <= max_recent + 1:
        return messages
    old, recent = messages[1:-max_recent], messages[-max_recent:]
    summary = summarizer(old)  # 오래된 부분을 한 단락 요약
    return [
        messages[0],  # 첫 user 메시지 보존
        {"role": "user", "content": f"[지난 대화 요약]\n{summary}"},
        *recent,
    ]
```

`summarizer`는 LLM 호출 한 번을 감싼 함수다. 오래된 messages를 통째로 넘기면 "이 대화에서 무슨 일이 있었는지 한 단락으로 적어라" 같은 프롬프트로 한 줄 요약을 받아 온다. 그 요약 한 줄이 윈도우 안에 자리를 잡는다. 모델은 윈도우에서 떨어진 메시지를 *못 보지만*, 요약 한 줄은 본다. 사용자 이름도, 마감 시간도, 거기 들어 있을 가능성이 높다.

물론 trade-off가 있다. 첫째, 요약을 만드는 데 LLM 호출이 한 번 더 든다. 매 iteration마다 요약을 다시 만들면 비용이 두 배가 된다. 그래서 보통은 *임계점에 도달했을 때만* 요약을 갱신한다. 둘째, 요약은 *손실이 있는 압축*이다. 모델이 한 단락으로 압축하면서 미세한 디테일이 사라진다. 사용자가 던진 구체적 숫자 하나가 요약에서 빠질 수 있고, 그 숫자가 나중에 결정적인 정보였을 수도 있다. 셋째, 요약이 점점 누적된다. 요약을 한 번 만들고 또 만들면 *요약의 요약*이 생긴다. 시처럼 추상화돼서, 실효는 떨어진다.

그래서 summary buffer는 *작업이 명백히 길고, 컨텍스트의 핵심이 자연어 디테일에 있는* 경우에 잘 맞는다. 대화형 어시스턴트, 긴 호흡의 코드 리뷰 작업, 사용자의 선호가 누적되는 챗봇이 여기에 들어간다. 반대로 도구 결과의 정확한 숫자가 중요한 작업, 다섯 단계의 절차가 또렷한 작업에는 sliding window 쪽이 안전하다. 요약이 숫자를 뭉개거나 절차를 흩뜨리면 다음 iteration이 통째로 꼬인다.

한 가지 더 짚어두자. 요약을 누구에게 시킬 것인가. 보통은 본 작업과 같은 모델을 쓰는데, 작은 모델을 따로 쓰는 변형도 가능하다. 요약은 reasoning이 깊지 않아서 Haiku나 GPT-4o-mini 같은 가벼운 모델로도 충분하다. 비용 절감의 여지가 보이는 자리다.

## 컨텍스트 밖으로 흘려보내기 — 외부 저장소 spillover

sliding window도 summary buffer도 결국 *컨텍스트 안에서* 무엇을 살리고 무엇을 버릴지를 정하는 전략이다. 그런데 어떤 정보는 컨텍스트에 항상 들고 다닐 필요 없이, "필요할 때만 꺼내" 쓰면 충분하다. 사용자가 한 달 전에 입력했던 주소, 어제 작업의 결과 요약, 시스템이 처음 만났을 때 받은 환경 설정. 이런 정보는 messages 리스트 안에 들고 다니지 말고 *외부에 저장*했다가, 도구로 꺼내는 편이 깔끔하다.

여기서 가장 흔히 떠오르는 단어가 long-term memory다. 디스크 위에 살아남는 메모리. 처음부터 화려하게 갈 필요는 없다. SQLite 한 파일이면 충분하다. JSON 파일 하나라도 시작점으로는 부족하지 않다.

```python
import json
from pathlib import Path

class JSONMemory:
    def __init__(self, path="memory.json"):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def save(self, key, value):
        self.data[key] = value
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def load(self, key, default=None):
        return self.data.get(key, default)
```

그리고 이걸 도구로 노출한다. `save_fact`, `recall_fact` 같은 도구 두 개. 모델이 "이건 다음에도 쓸 정보 같다"고 판단하면 `save_fact`를 부른다. 다음 세션에서 같은 키로 `recall_fact`를 부르면 값이 돌아온다. 디스크 위에 살아남는 메모리가 그렇게 완성된다.

이게 너무 단순해 보인다면 좋은 직감이다. 운영 단계에서는 SQLite로 옮기고, 동시 접근을 락으로 보호하고, 키 충돌을 막는 namespace 설계도 끼어든다. 그런데 입문 단계에서 그런 손질을 미리 다 하려고 들면, 정작 메모리의 본질이 안 잡힌다. JSON 파일 하나로 시작하자. 손에 익으면 SQLite로 옮기는 일은 한나절이면 끝난다.

한 가지 짚어둘 점이 있다. 외부 저장소는 메모리이긴 한데, *모델이 자발적으로 사용하는* 메모리다. 모델이 "이 정보를 저장해 두자"고 결정해야 도구 호출이 들어간다. 그 결정이 늘 정확한 건 아니다. 사용자가 "내 이름은 토비야"라고 말했어도, 모델이 그 정보의 *중요성*을 알아채지 못하면 `save_fact`를 부르지 않는다. 그래서 외부 메모리는 시스템 프롬프트에 *명시적 지침*을 곁들이는 편이 낫다. "사용자가 다음에도 쓸 만한 정보를 주면 save_fact로 저장하라" 같은 한 줄이 있어야 모델이 자발적으로 손을 뻗는다.

## Semantic memory와 RAG는 13장에서

지금쯤 한 가지 의심이 들 수도 있다. "그러면 이 메모리들에 *내용 기반 검색*이 필요한 경우는 어떻게 하지? 키로 꺼내는 게 아니라, 의미로 비슷한 걸 찾아야 하는 경우는?"

거기서 등장하는 단어가 RAG, 더 정확히는 벡터 데이터베이스다. 외부 문서를 임베딩 벡터로 변환해 저장해 두고, 사용자 질문도 임베딩 벡터로 바꾼 다음, 코사인 유사도가 높은 청크를 끌어와 컨텍스트에 끼우는 그것. 우리 분류에서는 semantic memory의 가장 흔한 구현이다. 사실과 지식을 통째로 보관하고, 필요할 때 의미적으로 가까운 조각을 꺼낸다.

그런데 이 책에서는 RAG를 5장에서 다루지 않는다. 13장에서 한 챕터, 부록 B에서 또 한 챕터를 따로 할애한다. 미루는 이유는 단순하다. RAG는 임베딩 모델 선택, 청크 단위 설계, retrieval 전략, reranking, 평가 메트릭, 운영 모니터링까지 줄줄이 따라붙는다. 5장의 한 절에 욱여넣으려고 하면 *어느 것도 손에 안 잡히는* 모양이 된다. 그리고 RAG는 메모리의 한 변종이긴 하지만, *데이터 파이프라인*의 색깔이 훨씬 강하다. 평가와 retrieval을 본격적으로 다루는 13장에서 다른 도구들과 함께 보는 편이 자연스럽다.

지금은 *RAG가 있다는 사실*과 *그 자리가 semantic memory다*라는 것만 박아두자. 컨텍스트 윈도우의 한계를 만났을 때 떠오르는 첫 번째 답이 "벡터 DB!"가 아닐 수 있다는 점도 함께 기억해두자.

## "Claude Code는 vector DB가 아니라 grep을 쓴다"

여기서 1장에서 흘려 두었던 한 가지 사실을 다시 꺼낼 차례다. 2026년 시점의 가장 성공적인 코딩 에이전트 — Claude Code, Cursor, Devin — 이 코드베이스를 다루는 방식을 살펴보면, 의외로 벡터 DB가 보이지 않는다. 대신 보이는 건 grep과 ripgrep, 파일 시스템 순회, 그리고 *명시적 컨텍스트 엔지니어링*이다.

이게 무슨 뜻일까. 사용자가 "이 함수 어디서 호출되는지 찾아봐"라고 했을 때, 벡터 DB 기반 RAG라면 함수명을 임베딩으로 바꿔 코사인 유사도가 높은 청크를 가져온다. 그런데 정확히 그 함수의 호출처를 찾는 데에는 grep 한 줄이 *더 정확하고, 더 빠르고, 더 싸다*. `grep -r "function_name" .` 한 줄이면 끝난다. 임베딩이 끼어들 자리가 없다.

이게 무엇을 보여주는가. 모든 메모리 문제가 RAG로 풀리는 건 아니라는 점이다. 어떤 정보는 *정확한 토큰 매칭*으로 풀리고, 어떤 정보는 *명시적인 파일 위치*로 풀린다. 벡터 DB는 "정확히 무엇을 찾는지 모를 때, 의미적으로 가까운 것을 끌어오는" 데에 강하다. 반대로 "정확히 이 키워드를 가진 곳을 다 찾는" 작업에는 grep이 훨씬 낫다. 둘은 다른 문제를 푼다.

이 사실이 메모리 챕터에 끼어드는 이유는 분명하다. semantic memory = vector DB라는 등식이 머릿속에 박혀 있으면, *적절하지 않은 자리에 RAG를 끼우는* 함정에 빠지기 쉽다. Claude Code가 grep을 쓴다는 사실은 이 함정을 떠올리게 하는 좋은 자석이다. "벡터는 한 선택지일 뿐, 명시적 컨텍스트가 더 잘 통하는 영역도 있다"는 균형 감각이 메모리 설계의 출발점이다. 13장에서 RAG를 본격적으로 다룰 때 다시 이 자석을 꺼낼 것이다.

## mini_agent.py v2 — Memory 클래스 부착

이제 손에 든 조각들을 코드로 합쳐 보자. 3장의 `mini_agent.py` v1을 갱신해 *메모리를 끼울 수 있는* v2로 만든다. v1의 `Tool` 클래스와 `run_agent` 함수의 골격은 그대로 유지하고, `Memory` 클래스 하나와 `run_agent`에 인자 하나를 추가하는 정도의 변경이다.

```python
# mini_agent.py — v2: ReAct loop + Memory
# 책 "맨손으로 짓는 AI 에이전트" 정본 코드
# v1(3장) → v2(5장: 메모리) → v3(6장: 안전장치)

from anthropic import Anthropic
from dataclasses import dataclass, field
from typing import Callable, Any, Optional, Literal


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    func: Callable[..., Any]


@dataclass
class Memory:
    """sliding window 또는 summary 두 모드."""
    mode: Literal["window", "summary"] = "window"
    max_turns: int = 10
    summarizer: Optional[Callable[[list[dict]], str]] = None
    _summary: str = ""
    _messages: list[dict] = field(default_factory=list)

    def add(self, message: dict) -> None:
        self._messages.append(message)

    def view(self) -> list[dict]:
        """모델 호출에 넘길 messages를 돌려준다."""
        if len(self._messages) <= self.max_turns + 1:
            return list(self._messages)
        anchor, recent = self._messages[0], self._messages[-self.max_turns:]
        if self.mode == "window":
            return [anchor, *recent]
        # summary 모드
        if self.summarizer is None:
            raise ValueError("summary mode requires a summarizer")
        old = self._messages[1:-self.max_turns]
        if not self._summary or len(old) % self.max_turns == 0:
            self._summary = self.summarizer(old)
        return [
            anchor,
            {"role": "user", "content": f"[지난 대화 요약]\n{self._summary}"},
            *recent,
        ]


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
    memory: Optional[Memory] = None,
) -> dict:
    client = Anthropic()
    dispatch = {t.name: t.func for t in tools}
    tool_specs = _to_specs(tools)

    mem = memory if memory is not None else Memory(mode="window", max_turns=max_iterations * 2)
    mem.add({"role": "user", "content": user_message})

    for step in range(max_iterations):
        try:
            response = client.messages.create(
                model=model, max_tokens=1024,
                tools=tool_specs, messages=mem.view(),
            )
        except Exception as exc:
            return {"status": "error", "step": step, "reason": str(exc)}

        mem.add({"role": "assistant", "content": response.content})

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

        mem.add({"role": "user", "content": results})

    return {"status": "capped", "step": max_iterations,
            "reason": f"max_iterations={max_iterations} reached"}


# ─── 데모 ───────────────────────────────────────────
if __name__ == "__main__":
    from anthropic import Anthropic as _A

    def summarize(old_messages: list[dict]) -> str:
        client = _A()
        text = "\n".join(str(m.get("content", ""))[:200] for m in old_messages)
        resp = client.messages.create(
            model="claude-haiku-4-5", max_tokens=300,
            messages=[{"role": "user",
                       "content": f"다음 대화를 한 단락으로 요약하라:\n{text}"}],
        )
        return "".join(b.text for b in resp.content if b.type == "text")

    # window 모드
    mem_window = Memory(mode="window", max_turns=8)
    # summary 모드
    mem_summary = Memory(mode="summary", max_turns=6, summarizer=summarize)

    # tools는 3장과 동일하다고 가정
    # result = run_agent("...", tools=tools, memory=mem_summary)
```

한 번 변경점을 정리하고 가자. 첫째, `Memory` 클래스가 등장했다. 두 모드 — `"window"`와 `"summary"` — 를 한 클래스에 담아 두고, `mode` 필드 하나로 분기한다. `add(message)`로 메시지를 누적하고, `view()`가 모델 호출에 실제로 넘길 messages 리스트를 돌려준다. 둘째, `run_agent`에 `memory: Optional[Memory] = None`이 추가됐다. 인자가 들어오지 않으면 기본 window 메모리가 자동으로 생성된다. v1과의 *호출 호환성*이 유지된다는 점이 중요하다. v1으로 작성된 코드는 v2에서 그대로 돈다. 셋째, messages를 직접 쌓던 코드가 `mem.add(...)` / `mem.view()`로 갈렸다. 외부 인터페이스만 보면 v1 그대로지만, 내부에서 메모리 관리가 분리된다.

`summarizer`를 `Callable`로 받는 부분도 짚어둘 가치가 있다. 어떤 함수든 *오래된 messages 리스트를 받아 한 단락 문자열을 돌려주는* 시그니처만 맞으면 끼울 수 있다. 위 데모에서는 Haiku를 쓰는 작은 함수를 끼웠지만, 외부 서비스로 빼도 되고, 더 정교한 압축 로직을 짜 넣어도 된다. 인터페이스만 고정되면 구현은 자유다. 이게 dataclass + Callable 조합의 작은 미덕이다.

외부 저장소 메모리는 어디로 갔는가? 위 코드에는 들어 있지 않다. 그건 *도구*로 노출하는 편이 자연스럽기 때문이다. 앞에서 만든 `JSONMemory`를 감싸 `save_fact`, `recall_fact` 두 함수를 만들고, 그걸 `Tool` 인스턴스로 등록해 `run_agent`에 넘기면 끝이다. `Memory` 클래스는 *컨텍스트 윈도우 안의* 메모리를 다루고, 외부 저장소는 *도구* 옵션으로 들어간다. 둘의 역할이 깔끔하게 갈린다.

이 v2가 책의 두 번째 정본이 된다. v1과 비교해 라인 수가 약간 늘었지만, 추가된 것은 결국 `Memory` 데이터클래스 하나와 그걸 끼울 자리뿐이다. 다음 장에서는 이 v2를 다시 한 번 손봐 *안전장치*를 얹는다. v2가 v3에 그대로 흡수되니, 지금 이 모양에 너무 집착할 필요는 없다. 다만 한 번은 손으로 짜고 굴려 보길 권한다. summary 모드를 켜고 긴 작업을 던지면, 컨텍스트가 어떻게 압축돼서 들어가는지 손으로 느낄 수 있다.

## 메모리 설계의 작은 체크리스트

여기까지 다룬 네 가지를 한 번 정리해 두자. 새 에이전트를 설계할 때 한 번씩 던져 볼 만한 질문들이다. 작업이 *단발성*인가, *세션 가로지르는 누적*이 있는가? 단발성이면 sliding window 한 줄로 충분하고, 누적이 있다면 외부 저장소 도구를 곁들이는 편이 낫다. 작업의 핵심이 *정확한 숫자나 키워드*인가, *자연어 디테일*인가? 숫자라면 window가 안전하고, 자연어라면 summary가 잘 맞는다. *trial 사이의 학습*이 의미가 있는가? 있다면 4장에서 본 Reflexion 스타일의 episodic memory가 별도로 필요하다. *정확한 키워드 매칭*이면 충분한가, *의미 기반 검색*이 필요한가? 키워드면 grep, 의미면 벡터 DB다. 후자에 손을 뻗기 전에 한 번은 "정말 의미 기반이 필요한가?"를 다시 묻자.

이 질문들의 답을 종합하면 *내 에이전트에 필요한 메모리 조합*이 자연스럽게 잡힌다. 입문 단계에서 풀세트를 한 번에 깔지는 말자. 부담만 키운다. 가장 단순한 sliding window 한 줄로 시작해서, 부족함을 느끼는 자리부터 한 가지씩 보태는 편이 바람직하다. 모양보다 *왜 이 모양을 끼우는가*의 답이 더 중요하다.

## 마무리, 그리고 다음 장 예고

손에 쥔 것들을 한 번 정리하자. 메모리 분류 네 동그라미를 코드 위에 포갰다. short-term이 messages 리스트, long-term이 외부 저장소, episodic이 4장의 trial 메모, semantic이 RAG라는 매핑을 박았다. sliding window와 summary buffer 두 모드를 손으로 짰고, JSON 파일 하나로 시작하는 외부 저장소 모양도 손에 받았다. RAG는 13장과 부록 B로 자리만 잡아두고 미뤘다. 그리고 `mini_agent.py` v2 — `Memory` 클래스가 부착된 두 번째 정본 — 가 우리 손에 들어왔다.

그런데 한 가지 골칫거리가 남는다. history만 잘 관리하면 에이전트가 안전해지는가? 그렇지 않다. 메모리가 깔끔하게 잘려도, 루프 자체가 폭주하면 청구서는 그대로 부풀어 오른다. *$0.08짜리 작업이 4시간 동안 무한 루프로 $2,847이 되었다*는 보고가 이미 여러 곳에 있다. 한 번의 호출에 토큰 500개씩 쓰던 작업이, 갇혀 15번 도는 동안 누적 4M 토큰으로 부풀어 버린 사례도 있다. 메모리 한 줄로는 막을 수 없는 모양이다.

다음 6장에서는 그래서 *에이전트가 망가지는 다섯 가지 모양*을 정면으로 다룬다. 무한 루프, 컨텍스트 overflow, hallucinated tool, malformed JSON, 재시도 폭주. 그리고 그걸 막는 하드 캡 4종 세트 — iteration cap, token cap, time cap, spend cap. v2에 안전장치를 얹어 v3로 키울 것이다. history만 잘 관리한다고 끝이 아니다. 루프가 폭주하기 시작하면, 그 모양을 *어디서 알아채고 어디서 끊을 것인가*가 진짜 문제다. 다음 장으로 넘어가자.
