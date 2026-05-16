# 8장. LangChain이 진짜로 빛나는 자리 — 통합, 도구 생태계, LangSmith

Hamel Husain이라는 사람이 있다. 평가(eval) 분야에서 가장 자주 인용되는 실무가 중 한 명이고, 여러 회사의 AI 팀을 컨설팅하면서 LangChain을 줄곧 비판해 온 것으로도 유명하다. 그런 그가 어느 날 트위터에 이런 문장을 올렸다.

> "처음엔 LangChain에 짜증이 났다. 그런데 업계 사람들과 일해 보니 다들 LangChain을 쓰고 있더라. 시간이 지나 이유를 알게 됐다 — 그들은 사용자에게 광적으로 귀를 기울인다."

이 한 문장이 묘하게 마음에 걸린다. 비판자가 마지못해 인정한 강점, 그러니까 "기술적으로 우아하지는 않을지 몰라도, 실무자가 *진짜로 부딪히는* 문제에 라이브러리가 응답하고 있다"는 평가. 이게 무엇을 뜻하는지 한 번 진지하게 살펴보자.

7장에서 우리는 mini_agent를 LangChain으로 다시 짰다. `prompt | llm | parser`라는 파이프 한 줄로 round-trip이 우아하게 묶이는 경험. 그게 LangChain의 *합성 측면*이었다. 그런데 솔직히 말하면, mini_agent 수준이면 SDK 버전도 충분히 우아했다. 줄 수도 비슷하고, 가독성도 한 쪽이 다른 쪽을 압도하지 않는다. 그렇다면 LangChain의 진짜 매력은 어디에 있는가? 7장의 작은 예제만 봐서는 답이 잘 안 보인다.

이번엔 시각을 좀 더 넓혀 보자. mini_agent를 넘어 실제 제품을 만든다고 가정하면 — 그러니까 PDF를 읽고, Postgres에서 임베딩을 꺼내고, Slack에 알림을 보내고, 누가 호출했을 때 무엇이 잘못됐는지 사후에 추적하려고 한다면 — 그때 LangChain은 갑자기 결이 달라진다.

## 다시 짤 가치가 없는 코드

LangChain의 첫 번째 강점은 *통합(integration)의 양*이다. 멋있는 표현은 아니다. 그저 "남이 이미 짜 놓은 어댑터가 수백 개 있다"는 뜻이다. 그런데 이 평범한 사실이 실무에서 무엇을 의미하는지 한 번 따져 보자.

벡터 데이터베이스를 예로 들어보자. Pinecone, Weaviate, Qdrant, Milvus, Chroma, PGVector, OpenSearch, Redis, Elasticsearch, Vespa... 이름만 늘어놔도 숨이 찬다. 각각이 SDK가 다르고, 인증 방식이 다르고, 메타데이터 쿼리 문법이 다르다. PoC에서 Chroma로 시작했다가 본 서비스에서 Pinecone으로 갈아탄다고 해보자. 직접 짠 코드라면 `add`, `query`, `delete`, `update`, `filter` 함수를 전부 다시 쓰게 된다. 끔찍한 일이다.

그런데 LangChain의 `VectorStore` 추상 위에 올려놨다면? `Chroma(...)`를 `Pinecone(...)`으로 바꾸는 한 줄로 끝난다. 나머지 코드는 모른다. `as_retriever()` 한 번 호출하면 그다음부터는 동일한 retriever 인터페이스로 흐른다. 이건 추상화 과잉이 아니라 *진짜 추상화*다. 인터페이스를 모두 같이 보고 한 번에 잘 짠 사람이 있고, 그 위에 100여 개 백엔드 어댑터가 붙어 있다.

이걸 우리가 직접 짜야 한다고 상상해 보자. 각 백엔드의 SDK 버전이 올라갈 때마다 어댑터를 다시 손봐야 한다. Pinecone v2와 v3 사이의 시그니처 변경, Weaviate gRPC로의 마이그레이션, Qdrant collection API의 리네이밍... 어느 순간 우리 회사의 핵심 기능과는 무관한 *어댑터 유지보수*가 사이드 잡으로 늘어붙기 시작한다. 끔찍한 일이다. 그 일을 100명이 분담해 처리해 주는 라이브러리가 곁에 있다면, 일단 그 자리는 양보하는 편이 낫다.

문서 로더도 마찬가지다. PDF, DOCX, HTML, Notion, Confluence, Google Drive, S3, Slack 메시지, GitHub 이슈... `langchain_community.document_loaders` 한 모듈에 100개 넘는 로더가 산다. 모두 같은 `load() -> list[Document]` 시그니처다. 어떤 회사에 가도 "우리는 데이터가 Notion에 있어요"는 만나는 말이다. 그때마다 Notion API 문서 뒤지고 페이지네이션 디버깅하고 권한 처리 짜고 있을 시간이 있는가? 없다. 한 줄이면 된다.

```python
from langchain_community.document_loaders import NotionDirectoryLoader
docs = NotionDirectoryLoader("./notion_export").load()
```

이게 *내가 다시 짤 가치가 없는 코드*다. 누군가가 이미 잘 짜 놨고, 100명의 사용자가 이미 한 번씩 버그를 발견해 PR을 보냈고, 메인테이너가 그걸 다 머지했다. 내가 처음부터 짜면 그 100번의 디버깅을 혼자 다 겪어야 한다. 그럴 시간에 내 도메인 로직에 집중하는 편이 낫다.

retriever, embedding, chat model, output parser, callback handler... LangChain이 제공하는 *통합 어댑터*는 영역마다 비슷한 양이 쌓여 있다. 한 번 표로 정리해 봐도 좋다. 어떤 영역에서 LangChain이 직접 짜기를 면제해 주는지가 한눈에 들어온다.

| 영역 | 어댑터 모듈 | 대략적 갯수 | 우리가 안 짜도 되는 것 |
|---|---|---|---|
| 채팅 모델 | `langchain_*` provider 패키지 | 30+ | provider별 함수 시그니처, 메시지 직렬화, 스트리밍 토큰 핸들링 |
| 임베딩 | `langchain_*.embeddings` | 30+ | 배치 크기 조절, retry, rate limit 회피 |
| 벡터스토어 | `langchain_community.vectorstores` | 80+ | upsert/query/delete의 백엔드별 차이 |
| 문서 로더 | `langchain_community.document_loaders` | 100+ | 외부 SaaS API의 페이지네이션·인증 |
| 도구 | `langchain_community.tools` | 100+ | 외부 서비스 호출 보일러플레이트 |
| 콜백 | `langchain_core.callbacks` | 15+ | trace, 로깅, 토큰 카운팅 훅 |

숫자는 시점에 따라 들쭉날쭉하고 정확하지 않을 수 있다(사실 확인 필요). 핵심은 *어디에 시간이 안 들 것이냐*를 한 번 보자는 데 있다. 위 표의 항목 중에 우리가 직접 짜야 의미 있는 게 몇 개나 되는지 한 번 따져 보면 답이 분명해진다. 거의 없다.

여기서 한 가지 더 짚어 두자. 통합 어댑터를 가져다 쓴다고 해서 LangChain 본체의 모든 추상에 묶일 필요는 없다. 직접 짠 mini_agent에 `langchain_community.vectorstores.Chroma`만 끼워 쓰는 방식도 충분히 가능하다. retriever 인터페이스를 직접 호출해 결과를 받은 다음, 우리가 만든 ReAct 루프에 그대로 흘려 넣으면 된다. 이게 핵심이다. LangChain은 통째로 삼키는 종교가 아니다. 통합 부분만 떼다 쓰는 어댑터 창고로 봐도 된다.

## 도구 생태계 한 번 둘러보기

도구(tool) 쪽도 사정이 비슷하다. mini_agent에서 우리는 `add`, `multiply` 같은 장난감 도구를 손으로 짰다. 진짜 에이전트는 그것보단 무거운 일을 한다 — 웹 검색, SQL 실행, 셸 명령, 코드 인터프리터, 이미지 처리, 캘린더 조회.

`langchain_community.tools` 카탈로그를 한 번 훑어보자. 이름만 쓱 봐도 어떤 일이 가능한지 감이 잡힌다.

- 검색: `DuckDuckGoSearchRun`, `TavilySearchResults`, `GoogleSearchAPIWrapper`, `BingSearchAPIWrapper`, `BraveSearch`
- 코드 실행: `PythonREPLTool`, `ShellTool`, `E2BDataAnalysisTool`
- SQL: `QuerySQLDataBaseTool`, `InfoSQLDatabaseTool`, `ListSQLDatabaseTool`
- 파일: `ReadFileTool`, `WriteFileTool`, `CopyFileTool`, `DeleteFileTool`
- 외부 SaaS: `SlackGetMessage`, `GmailSearch`, `JiraAction`, `GitHubAction`

모두 `BaseTool`을 상속한다. 즉 mini_agent_lc의 agent executor에 그대로 들어간다. 새 도구를 더하는 건 import 한 줄과 리스트에 추가 한 줄이 전부다.

```python
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

db = SQLDatabase.from_uri("sqlite:///app.db")

tools = [
    DuckDuckGoSearchRun(),
    QuerySQLDataBaseTool(db=db),
]
```

이걸 직접 짠다고 상상해보자. DuckDuckGo HTML 스크래핑하다가 rate limit 맞고, SQL 결과 직렬화하면서 datetime 처리 빼먹어서 JSON 인코더가 터지고, 권한 없는 테이블 조회하다가 의도치 않게 트랜잭션을 열어 둔 채로 죽는 사고를 한 번씩 겪게 된다. 익숙한 풍경이다. 통합 어댑터의 가치는 *내가 안 겪을 사고들을 다른 사람들이 미리 겪어 줬다*는 데에 있다. 이 부분만큼은 의심할 여지 없이 LangChain이 우위다.

도구를 *직접 만들고 싶을 때*도 LangChain의 결을 따르는 편이 낫다. `@tool` 데코레이터 한 줄이면 평범한 파이썬 함수가 LangChain agent에 그대로 들어가는 도구로 변신한다. 함수의 docstring이 도구 설명으로, 타입 어노테이션이 입력 스키마로 자동 변환된다.

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str, unit: str = "celsius") -> str:
    """주어진 도시의 현재 날씨를 가져온다. unit은 celsius 또는 fahrenheit."""
    # ... 실제 API 호출 ...
    return f"{city}: 18도, 흐림"
```

이 함수를 tools 리스트에 그대로 넣으면, 모델이 호출할 때의 JSON 스키마는 LangChain이 알아서 생성한다. 6장에서 우리가 직접 작성하던 `{"type": "function", "function": {...}}` 보일러플레이트가 사라진다. 번거로운 일을 라이브러리가 대신 해 주는 자리, 이런 자리에선 LangChain의 도움이 정말로 깔끔하다.

물론, 도구가 많아질수록 모델이 어떤 도구를 골라야 할지 혼란스러워한다는 다른 문제가 생긴다. 도구 설명을 명확하게 쓰는 일, few-shot 예시를 적절히 끼우는 일은 여전히 우리 몫이다. 어댑터가 있다고 다 끝난 게 아니라는 점은 기억해 두자.

## "그래서 모델이 뭘 봤지?"라는 질문에 답하기

6장에서 우리는 한 가지 골치 아픈 질문에 매달렸다. "방금 모델이 어떤 메시지 배열을 받았지?" 도구 호출이 두세 번 오갔는데 무엇이 잘못됐는지 추적하려면, 매 round-trip의 입력과 출력을 일일이 찍어 봐야 했다. print를 박고, 로그 파일을 열고, JSON을 손으로 펼쳐 가며 detective work를 했다. 작은 예제에선 해 볼 만했지만, 도구가 다섯 개로 늘고 루프가 열 번 도는 순간 사람이 따라가기를 포기하게 된다. 찜찜하다.

물론 그동안 우리에게 도구가 아예 없었던 것은 아니다. 표준 라이브러리의 `logging` 모듈로 매 호출을 찍을 수도 있고, OpenAI SDK의 `httpx` 클라이언트에 이벤트 훅을 꽂아 raw HTTP 페이로드를 출력할 수도 있다. 그런데 정작 그렇게 찍어 놓고 보면, 한 호출의 입력과 출력이 *시간 순서로 흘러가는 텍스트*로만 남는다. 트리도 없고, 사이클 횟수도 없고, "이 LLM 호출 다음에 어느 tool 호출이 왔다"는 인과 관계도 직접 머릿속에서 짜 맞춰야 한다. 텍스트 로그는 한 번 흘러간 강물이고, 거슬러 올라가기 번거롭다.

LangSmith는 이 질문에 처음으로 *제대로* 답한다. 키 두 개를 환경 변수에 꽂는 것으로 시작이다.

```bash
export LANGSMITH_API_KEY="lsv2_..."
export LANGSMITH_TRACING="true"
export LANGSMITH_PROJECT="mini-agent-lc"
```

이 세 줄이 다다. 7장에서 짠 mini_agent_lc 코드는 한 글자도 안 고치고, 그대로 다시 돌리기만 하면 LangSmith 대시보드에 모든 실행이 자동으로 쌓이기 시작한다. LangChain은 내부 callback handler를 통해 LCEL 파이프의 *모든* 단계 — prompt 생성, LLM 호출, tool 실행, parser 적용 — 를 자동으로 trace 트리로 묶어 보낸다.

자동 추적이 불편하거나 LangChain 바깥 코드를 추적하고 싶을 때는 `@traceable` 데코레이터로 명시적으로 묶을 수도 있다. 예를 들어 mini_agent의 정본(SDK 버전)에 trace만 붙이고 싶다면 이렇게 짠다.

```python
# trace_mini_agent.py
from langsmith import traceable
from mini_agent import call_llm, run_step

@traceable(name="mini_agent_run", run_type="chain")
def traced_run(task: str) -> str:
    return run_step(task)

if __name__ == "__main__":
    traced_run("3 더하기 5는?")
```

LangChain을 안 써도 LangSmith는 따로 돈다. 이 점은 뒤에서 다시 강조하겠다.

이렇게 한 번 돌리고 LangSmith 웹 대시보드를 열면, 트리 형태로 펼쳐진 trace를 보게 된다. 클릭하면 각 노드의 입력 메시지 배열과 출력이 정돈된 JSON으로 펼쳐진다. 토큰 수, 응답 시간, 비용도 노드마다 따로 붙는다. 한 화면 안에 모든 것이 있다. 6장에서 print로 디버깅하던 시절과 비교하면, 같은 작업이 detective work에서 *읽기 작업*으로 격하된다.

trace JSON을 한 번 발췌해 보자. mini_agent_lc가 "3 더하기 5는?"을 풀 때 LangSmith가 받아 적는 한 노드의 모양은 대략 이렇다.

```json
{
  "name": "ChatOpenAI",
  "run_type": "llm",
  "start_time": "2026-05-16T09:23:01.142Z",
  "end_time":   "2026-05-16T09:23:01.987Z",
  "inputs": {
    "messages": [
      {"role": "system", "content": "You are a helpful agent..."},
      {"role": "user",   "content": "3 더하기 5는?"}
    ]
  },
  "outputs": {
    "generations": [{
      "message": {
        "role": "assistant",
        "content": "",
        "tool_calls": [{
          "name": "add",
          "args": {"a": 3, "b": 5},
          "id": "call_8f2k..."
        }]
      }
    }]
  },
  "usage_metadata": {
    "input_tokens": 142,
    "output_tokens": 18,
    "total_tokens": 160
  }
}
```

이 한 덩어리를 *읽으면* 무엇이 보이는가. 845밀리초 동안, 입력 142토큰을 받아 출력 18토큰을 뱉었다. assistant는 텍스트가 아니라 도구 호출을 골랐다. `add(a=3, b=5)`. id까지 찍혀 있어서 다음 round-trip의 tool_result와 짝지을 수 있다. 6장에서 우리가 손으로 짜 맞추던 일을 LangSmith가 그냥 *보여 준다*. 잊지 말자 — 디버깅이 가능한 시스템은, 디버깅이 가능하다는 사실 자체만으로 안정성이 한 단계 위로 올라간다.

trace를 본격적으로 읽는 법을 짧게 정리해 보자. 한 번의 에이전트 실행이 LangSmith에 떨어지면, 보통 다음 네 가지를 차례로 살피게 된다.

1. **트리 구조** — 루트는 `AgentExecutor` 또는 우리가 `@traceable`로 묶은 함수. 그 아래에 LLM 호출 노드와 tool 호출 노드가 번갈아 매달린다. 사이클이 몇 번 돌았는지가 시각적으로 보인다.
2. **각 노드의 input/output** — 클릭하면 메시지 배열이 펼쳐진다. 시스템 프롬프트가 의도한 대로 들어갔는지, tool_result가 모델에 어떤 모양으로 다시 흘러갔는지 그 자리에서 확인된다.
3. **토큰·시간·비용** — 각 LLM 노드 옆에 작은 숫자가 붙는다. "이 한 번의 round-trip이 0.4초 걸렸고 320 토큰을 썼고 0.0008달러를 태웠다." 비용 폭주의 원인을 사후에 짚는 일이 *어느 노드인지*를 찍는 일로 단순해진다.
4. **에러와 retry** — `with_retry()`로 묶인 호출이 실패한 뒤 재시도된 경우, 첫 시도와 재시도가 같은 노드 아래에 형제로 매달린다. 한 번 실패했다는 사실이 숨지 않고 보인다.

이 네 가지를 한 화면에서 보고 있으면, 6장 풍경이 떠오른다. 그때 우리는 print 한 줄 한 줄을 터미널에서 스크롤로 거슬러 올라가며, 어떤 출력이 어떤 입력의 응답인지 *머릿속으로* 짝지어야 했다. 그 작업을 LangSmith는 트리로 정돈해 보여 준다. 한 가지 일을 두 사람이 같이 짚을 수 있게 되는 효과도 크다 — "이 trace를 봐주세요" 한 줄로 동료에게 디버깅 책임을 넘길 수 있다. 혼자 끙끙대던 일이 협업할 수 있는 일로 격하된다.

## 한 페이지짜리 평가 미리보기

LangSmith의 두 번째 얼굴은 *평가 도구*다. 본격적인 이야기는 13장에서 한다. 여기서는 단어 세 개와 한 호흡만 미리 익혀 두자 — dataset, evaluator, run.

- **Dataset**: 입력-기대출력 쌍의 모음. "이 질문엔 이 답이 나와야 한다"를 모은 표.
- **Evaluator**: 모델 출력이 기대출력에 얼마나 가까운지를 점수화하는 함수. 정확도, 유사도, LLM-as-judge, 도메인 규칙 — 무엇이든 evaluator로 둘 수 있다.
- **Run**: dataset의 각 입력에 대해 시스템을 한 번 돌린 결과. evaluator가 run마다 점수를 매긴다.

대시보드에서 dataset을 만들고, 위의 trace 화면에서 "이 실행을 dataset에 추가" 버튼을 누르면 시작이다. evaluator를 붙이면 같은 dataset 위에서 prompt를 바꿔 가며 점수가 어떻게 움직이는지 본다. 모델 버전을 올리거나 도구 설명을 손볼 때, *감*이 아니라 *수치*로 판단할 근거가 생긴다. 너무 멀어서 손에 안 잡힐 것 같은가? 그래서 13장에서 천천히 다시 만지기로 했다. 지금은 "trace 화면에서 한 클릭으로 평가 데이터셋이 만들어진다"는 사실 하나만 머리 한 켠에 넣어 두자.

한 가지만 더 짚자. 평가 도구 시장에는 LangSmith 말고도 Braintrust, Ragas, DeepEval, Arize Phoenix 같은 선수들이 있다. 영역별로 강점이 다르다. RAG 메트릭에 특화된 Ragas, CI/CD 자동화에 강한 DeepEval, 엔터프라이즈 모니터링이 강한 Arize Phoenix, 그리고 dataset→scoring→production monitoring→CI gate를 한 시스템으로 묶는 Braintrust. LangSmith의 가장 큰 강점은 LangChain·LangGraph와의 매끄러운 통합이지만, 그게 *우리 스택의 가장 중요한 요구*가 아니라면 다른 도구가 더 잘 맞을 수도 있다. 13장에서 비교표를 펴고 한 번 더 신중하게 골라 보기로 하자. 지금 단계에서는 "한 도구가 모든 자리를 차지하는 시장이 아니다"라는 사실만 알아 두면 된다.

## LangSmith는 LangChain이 아니다

여기서 한 가지 중요한 nuance를 짚어야 한다. Hamel Husain의 그 트윗에는 후일담이 있다. 그는 "LangChain 본체에는 여전히 의문이 있지만, LangSmith는 단독으로 써도 좋다"는 입장을 여러 인터뷰에서 반복했다. 이게 무슨 뜻인가?

LangSmith는 LangChain 본체와 *기술적으로 분리 가능하다*. 위에서 본 `@traceable` 데코레이터는 LangChain 없이도 동작한다. OpenAI SDK 직호출, Anthropic SDK 직호출, 그냥 평범한 파이썬 함수에도 붙는다. 우리가 1부에서 짠 mini_agent의 정본을 그대로 두고 trace만 켜는 선택이 가능하다는 말이다. 한 번 정리해 보자.

```python
# mini_agent_traced.py — 1부 정본 + LangSmith trace만
import os
from langsmith import traceable
from openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "mini-agent"

client = OpenAI()

@traceable(run_type="llm", name="call_llm")
def call_llm(messages, tools=None):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )

@traceable(run_type="chain", name="run_agent")
def run_agent(task: str) -> str:
    # ... 3장의 ReAct 루프를 그대로 ...
    pass
```

이 파일에 LangChain은 한 글자도 안 들어간다. 그런데 LangSmith 대시보드를 열면 LCEL 파이프와 *동일한 모양의 trace 트리*가 보인다. 이게 무슨 뜻인지 음미해 보자. *통합 어댑터*와 *합성 추상화*는 잠시 미뤄 두고 LangSmith의 trace 능력만 가져다 써도 좋다는 뜻이다. LangChain의 모든 결정에 동의할 필요가 없다. 디버깅 도구로서의 LangSmith는, 우리가 1부에서 짠 직접 만든 mini_agent에도 똑같이 붙는다.

이 분리 가능성이 책의 9장에서 다룰 "골라 쓰기" 입장의 기술적 뒷받침이다. "LangChain은 통째로 삼키는 종교가 아니다"라는 우리의 한 줄이, 단지 정서적 균형 잡기가 아니라 *실제로 가능한 운영 방식*이라는 점. 기억해 두자.

조금 더 일반화해 보자. LangChain 생태계는 사실상 세 겹으로 쌓여 있다. 가장 안쪽에 `langchain_core`(Runnable, LCEL, tool 추상), 그 위에 `langchain`(고수준 chain·agent, 빠르게 deprecate되는 옛 API 다수), 가장 바깥에 `langchain_community` 및 provider별 패키지(통합 어댑터). 그리고 옆에 별도로 LangSmith와 LangGraph가 떨어져 산다. 우리가 받아들일지 거절할지를 *겹별로* 결정할 수 있다는 사실, 이게 LangChain을 다루는 마음가짐에서 가장 중요한 한 가지다. "전부 다 vs. 아무것도" 양자택일이 아니다.

## "이건 쓰지 말자" 목록

LangChain을 옹호하다 보면 한 가지 위험이 따른다 — 라이브러리 내부에 *권장되지 않는 옛 API*가 섞여 있다는 사실을 잊고 안내해 버리는 일이다. 2024~2026년 사이에 LangChain은 두 번의 큰 정리(0.1 → 0.2 → 0.3)를 거쳤다. 그 과정에서 deprecate된 또는 deprecate를 향해 가는 API가 적지 않다. 한 번 분명하게 짚자.

먼저, **메모리(memory) 모듈의 옛 클래스들**. `ConversationBufferMemory`, `ConversationBufferWindowMemory`, `ConversationSummaryMemory` — 이름이 익숙한가? 인터넷에 떠도는 튜토리얼의 상당수가 이걸 보여 준다. 대화 이력을 자동으로 누적해 주는 편리한 객체로 자주 소개된다. 그런데 LangChain 공식 가이드는 이미 명확하게 이렇게 말한다 — *short-term memory와 long-term memory가 필요하면 LangGraph + checkpointer로 이동하라*. 옛 memory 클래스는 단순 누적 외엔 별달리 하는 일도 없고, LCEL 파이프와 자연스럽게 합성되지 않으며, 다중 세션이나 영속화를 다루는 순간 한계가 곧장 드러난다. 새 코드에 굳이 끌어 쓰지 말자.

다음으로, **LCEL 이전 시대의 chain 클래스들**. `LLMChain`, `ConversationChain`, `SimpleSequentialChain`, `StuffDocumentsChain`, `RetrievalQA`... 익숙하다면 이미 오래된 LangChain 자료를 봤다는 신호다. 이들은 모두 LCEL의 `Runnable`로 대체되었고, 신규 코드에는 추천되지 않는다. 같은 일이 `prompt | llm | parser`로 더 간단하고, 더 명시적이고, 더 testable하게 표현된다. 옛 chain은 "기존 코드가 의존하니까 호환을 위해 남겨 두는 박물관 전시품" 정도로 받아들이는 편이 낫다.

마지막으로, **`AgentExecutor`도 시한이 정해진 느낌**이다. 2026년 현 시점에 여전히 동작하긴 하지만, LangChain 팀의 공식 권고는 "복잡한 에이전트 흐름은 LangGraph로 짜라"는 쪽으로 무게 추가 옮겨 갔다. 4부에서 LangGraph를 만질 때 이 흐름을 다시 다룬다.

정리하면 이렇다 — *튜토리얼이 오래된 자료라면 일단 한 번 의심하자.* `LLMChain(...)`, `ConversationBufferMemory(...)`, `RetrievalQA.from_chain_type(...)` 같은 호출이 보이면, 같은 일을 LCEL과 LangGraph로 어떻게 푸는지 공식 문서에서 한 번 더 확인하는 편이 안전하다. LangChain은 사용자에게 광적으로 귀를 기울이는 만큼, 옛 API를 빠르게 버리고 새 API로 옮기는 속도도 빠르다. 양날의 칼이다.

실무적인 팁 하나를 덧붙이자. 패키지 import 경로가 `langchain.xxx`로 시작하면 보통 옛 API, `langchain_core.xxx` 또는 `langchain_<provider>.xxx`로 시작하면 새 API다. 이 규칙만 머리에 박아 둬도 코드 리뷰에서 "이건 deprecated 흐름인데요"라는 한 줄을 빠르게 적을 수 있다. 새 코드라면 `langchain_core`와 provider별 패키지(`langchain_openai`, `langchain_anthropic` 등)에서 import 하는 편이 안전하다. `langchain_community`는 여전히 활발하지만, 그 안의 모듈도 점진적으로 provider별 패키지로 분가되는 흐름이 보인다.

## 마무리

LangChain이 빛나는 자리는 mini_agent 크기의 예제가 아니라, *우리가 다시 짤 마음이 안 드는 곳*에 있다. 100여 개의 벡터 DB 어댑터, 도구 카탈로그, 그리고 LangSmith trace. 이 세 가지가 LangChain을 "기술적으로 우아한 라이브러리"는 아닐지 몰라도 "실무에서 사실상 표준으로 자리 잡은 라이브러리"로 만든 이유다.

한 번 더 정리해 두자. Hamel이 트윗에서 인정했던 LangChain의 미덕 — "사용자에게 광적으로 귀를 기울인다" — 의 구체적인 모습이 이것들이다. 새로운 벡터 DB가 시장에 등장하면 며칠 안에 어댑터가 들어오고, 새로운 모델 provider가 공개되면 그 주에 `langchain_<provider>` 패키지가 따라 나오고, 실무자가 "trace에서 X 정보가 필요해요" 한 줄을 issue에 남기면 다음 minor 버전에 들어 있다. 라이브러리가 시장의 *속도*에 발을 맞추고 있다. 이게 우아함과 별개로 인정해야 할 강점이다.

특히 LangSmith의 위치는 다시 강조해 둘 만하다. 6장에서 우리를 괴롭히던 "그래서 모델이 뭘 봤지?"라는 질문에 LangSmith는 거의 무료에 가까운 노력으로 답한다. 그리고 그 답은 LangChain 본체와 묶이지 않는다. mini_agent 정본에도, LangChain 버전에도, 둘 모두에 동일하게 붙는다.

그렇다면 LangChain의 모든 것이 좋기만 한가? 그럴 리가. Hamel의 옹호가 마지못한 톤이었던 데에는 이유가 있다. 추상화 과잉, breaking change의 잦은 빈도, 문서와 실제의 불일치, 그리고 친절해 보이는 기능 뒤에 숨은 토큰 비용. 7장의 끄트머리에서 슬쩍 언급했던 `with_retry()`, `with_fallbacks()`의 "내장된 회복력"이 실제로는 "내장된 토큰 비용"이라는 점도 같이 들여다봐야 한다. 다음 장에서는 LangChain을 *비판하는* 목소리들을 진지하게 한 줄씩 검증해 보자. 어느 정도까지 사실이고, 어디부터 과장인가. 옹호와 비판을 한 자리에 놓고 보면, 비로소 *얼마나 받아들이고 어디서 거절할지*에 대한 우리의 입장이 단단해진다.
