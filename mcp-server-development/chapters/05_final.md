# 5장. Python 서버 — FastMCP, 그리고 `MCPServer`로 가는 길

`mcp` 2.0.0b2 휠을 통째로 내려받아 파일 전체에서 `fastmcp`라는 문자열을 찾아보면, 결과가 한 건도 나오지 않는다. 대소문자를 무시하고 뒤져도 0건이다.

Python으로 MCP 서버를 만들어본 사람이라면 이 문장이 얼마나 이상하게 들리는지 알 것이다. `from mcp.server.fastmcp import FastMCP` — Python MCP 서버는 사실상 이 한 줄에서 시작했다. 튜토리얼도, 블로그도, 사내 위키에 붙여둔 스니펫도 전부 저 줄로 시작한다. 다음 세대 패키지 안에 그 이름은 없다.

당황할 필요는 없다. 다만 이 장은 두 개의 시간대를 오간다는 것만 미리 알아두자. **지금 만들어 쓸 수 있는 라인**과 **곧 올 라인**이다. 두 시간대를 한 문단에 섞는 순간 코드가 동작하지 않는다.

## 지금 만들 수 있는 것 — 1.28.1의 FastMCP

먼저 좌표부터 찍자. 2026-07-26 시점에 PyPI가 `mcp` 패키지의 `info.version`으로 돌려주는 값은 **`1.28.1`**(2026-06-26 릴리스) 하나다. 2.x는 정식 릴리스가 아니라 프리릴리스 다섯 개(a1 → a2 → a3 → b1 → b2)로만 존재한다. `requires-python`은 `>=3.10`이고, 이 라인이 지원하는 스펙 리비전은 `2025-11-25`다. 그리고 `MCP-Protocol-Version` 헤더 없이 들어온 Streamable HTTP 요청은 `2025-03-26`으로 간주한다(2장 참고).

설치는 `uv`로 한다.

```bash
uv init team-wiki && cd team-wiki
uv venv
uv add "mcp[cli]"
```

`[cli]` extra가 `mcp` 커맨드까지 함께 깔아준다.

여기서 한 가지 짚고 넘어가자. 검색하다 보면 `uvx`로 서버를 띄우는 예제를 자주 만나게 되는데, **로컬에서 개발 중인 서버를 실행할 때 쓰는 건 `uvx`가 아니라 `uv run`이다.** 공식 Python 퀵스타트가 안내하는 경로도 `uv init` → `uv venv` → `uv add` → `uv run server.py`다. `uvx`는 이미 PyPI에 올라간 패키지를 받아서 실행하는 도구이니, 아직 아무 데도 올리지 않은 내 코드에는 맞지 않는다. 배포 후의 이야기는 9장에서 이어가자.

그래서 클라이언트 등록도 이렇게 된다.

```json
{
  "command": "uv",
  "args": ["--directory", "/absolute/path/to/team-wiki", "run", "server.py"]
}
```

`--directory`에 **절대경로**를 준다는 점이 중요하다. 상대경로로 적어두고 "어제는 됐는데" 하며 헤매는 경우가 의외로 많다.

## 같은 `team-wiki`를 Python으로

3장에서 TypeScript로 만든 것과 똑같은 서버를 만들어보자. 도구 두 개(`wiki_search`, `wiki_get`), 리소스 템플릿 하나(`wiki://{path}`), 프롬프트 하나(`summarize_page`)다.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("team-wiki")


@mcp.tool()
def wiki_search(query: str, limit: int = 10) -> list[dict]:
    """문서 제목과 본문에서 query를 검색해 상위 결과를 돌려준다."""
    hits = store.search(query)[:limit]
    return [{"path": h.path, "title": h.title} for h in hits]


@mcp.tool()
def wiki_get(path: str) -> str:
    """주어진 경로의 문서 본문을 돌려준다."""
    return store.read(path)


@mcp.resource("wiki://{path}")
def wiki_resource(path: str) -> str:
    return store.read(path)


@mcp.prompt()
def summarize_page(path: str) -> str:
    return f"다음 문서를 세 문장으로 요약해줘.\n\n{store.read(path)}"


if __name__ == "__main__":
    mcp.run()
```

3장의 TypeScript 코드와 나란히 놓으면 차이가 선명하다. TypeScript에서는 `registerTool`에 이름·설명·입력 스키마를 **명시적으로 건네준다.** Python에서는 그걸 하나도 적지 않았다. 이름은 함수명에서, 설명은 docstring에서, 입력 스키마는 타입 힌트에서 SDK가 알아서 읽어간다. `limit: int = 10`처럼 기본값을 주면 그 인자는 필수 목록에서 빠진다.

편하다. 그런데 편한 만큼 **타입 힌트를 대충 적으면 그게 그대로 모델에게 전달되는 계약이 된다.** 주석이 아니라 계약이다.

## 없는 문서를 물어보면 무슨 일이 일어나야 하나

러닝 예제에는 오류 케이스가 하나 박혀 있다. 존재하지 않는 `path`로 `wiki_get`을 부르는 경우다. 여기서 어떻게 응답하느냐가 이 서버의 품질을 가른다.

3장에서 이야기했듯, 이건 **Protocol Error가 아니라 Tool Execution Error로 돌려주는 게 맞다.** `2025-11-25` 리비전의 SEP-1303이 정한 원칙이 그것이다 — 입력 검증 오류는 프로토콜 레벨에서 실패시키지 말고 도구 실행 결과로 돌려줘서, 모델이 스스로 고칠 수 있게 하라는 것이다. 엄밀히 말하면 지금 우리 상황은 조금 다르다. "형식은 맞지만 실재하지 않는 경로"이니 스키마 검증 실패가 아니라 조회 실패다. 그래도 같은 논리가 그대로 통한다.

왜 그럴까? Protocol Error로 던지면 모델은 "이 도구는 고장 났다"까지만 알게 된다. 반면 결과로 돌려주면 "`docs/onbording.md`는 없다. 비슷한 경로로 `docs/onboarding.md`가 있다"까지 읽고 모델이 알아서 오타를 고쳐 다시 부른다. 같은 실패인데 하나는 막다른 길이고 하나는 우회로다.

3장의 TypeScript 코드에서는 이 결정이 눈에 잘 보였다. 반환 객체를 직접 조립하니 `isError` 플래그와 안내 텍스트를 손으로 넣게 된다. Python은 그 지점이 한 겹 감춰져 있다. 앞서 봤듯 이 SDK는 함수 시그니처와 docstring에서 계약을 읽어낸다. 그래서 성공 경로에서 우리가 만든 건 `list[dict]`와 `str`뿐이었다. **반환 봉투는 한 번도 만진 적이 없다.**

다행히 SDK가 이 자리를 이미 마련해두었다. `mcp` 1.28.1에서 **도구 함수가 예외를 던지면 SDK가 그것을 `isError: true` 결과로 감싸서 내보낸다.** FastMCP가 예외를 `ToolError("Error executing tool wiki_get: …")`로 감싸고, 그 아래 저수준 서버가 그것을 잡아 `CallToolResult(isError=True)`로 바꾼다. 즉 프로토콜 에러로 새지 않는다.

```python
@mcp.tool()
def wiki_get(path: str) -> str:
    """주어진 경로의 문서 본문을 돌려준다."""
    doc = store.read(path)
    if doc is None:
        raise ValueError(f"'{path}' 문서를 찾을 수 없다. wiki_search로 경로를 먼저 확인하라.")
    return doc
```

단, 모델에게 도달하는 텍스트는 **예외 메시지 그 자체**다. 그러니 메시지에 다음 행동을 적어 넣어야 3장에서 손으로 조립하던 그 안내와 같은 값을 한다. 문구를 완전히 통제하고 싶다면 `types.CallToolResult(isError=True, content=[...])`를 직접 반환해도 된다 — SDK가 이 경우 변환 없이 그대로 실어 보낸다.

**"없는 문서"는 서버의 버그가 아니라 대화의 한 장면이다.** 6장에서 Spring AI로 같은 케이스를 다시 만난다.

## 2.0이 오면 무엇이 달라지나

이제 다른 시간대로 넘어가자.

가장 큰 변화는 서두에서 말한 그것이다. **`FastMCP` 클래스가 `MCPServer`로 이름이 바뀌었다.** 이 사실은 두 갈래 독립 경로가 똑같이 가리킨다. 하나는 앞서 본 휠 문자열 검색 0건이고, 다른 하나는 마이그레이션 문서 원문이다.

> "The `FastMCP` class has been renamed to `MCPServer`."

같은 결론에 서로 다른 방법으로 도달했으니, 이건 추측이 아니라 사실로 받아들여도 된다.

그럼 코드는 어떻게 생겼을까? 2.0.0b2 태그의 문서 예제(`docs_src/index/tutorial001.py`) 원문이다.

```python
from mcp.server import MCPServer

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"
```

보고 나면 조금 허탈할지도 모르겠다. 클래스 이름 한 줄만 바뀌었을 뿐, `@mcp.tool()`도 `@mcp.resource()`도 그대로다. 공식 문서는 도구 등록 철학을 이렇게 못 박는다.

> "You declare one by putting `@mcp.tool()` on a plain Python function. **That's the whole API.**"

그리고 앞서 감각으로 잡아두라고 한 그 이야기를, 문서가 직접 말한다.

> "Type hints aren't documentation here. They are **the contract**."

한 가지 더, 우리 서버 설계에 직결되는 변화가 있다. **도구의 반환이 두 갈래로 갈린다** — 모델이 읽는 텍스트인 `result.content`와, 클라이언트가 타입을 유지한 채 받아가는 `result.structured_content`다. `wiki_search`가 `{path, title}` 객체 배열을 돌려주도록 명세를 잡은 이유가 여기에 있다. 모델에게는 "세 건을 찾았고 제목은 이렇다"는 요약 텍스트가 가고, 클라이언트에게는 타입이 살아 있는 구조화 데이터가 간다. 하나의 반환을 두 청중에게 나눠 보내는 셈이다.

한 가지 알아둘 게 있다. **구조화 출력은 와이어 위에서 반드시 객체다.** 그래서 `list[dict]`를 돌려주면 SDK가 말없이 `{"result": [...]}`로 한 겹 감싸서 내보낸다. 3장에서 우리가 `{path, title}` 배열을 `results` 키로 직접 감쌌던 것과 정확히 같은 제약이고, 다만 TypeScript에서는 손으로, Python에서는 SDK가 대신 한다는 차이다. 키 이름이 `results`가 아니라 `result`가 된다는 것도 함께 기억해두자 — 클라이언트를 짜는 사람에게는 이 한 글자가 계약이다.

`import` 경로에 대해서는 주의가 하나 필요하다. 문서마다 `from mcp.server import MCPServer`와 `from mcp.server.mcpserver import MCPServer` 두 형태가 섞여 등장한다. 이 책은 튜토리얼·README·실제 소스가 모두 쓰는 앞의 형태를 따르되, **둘이 완전히 같다고 단정하지는 않는다.**

## 잔가지들, 그리고 무엇을 잠글 것인가

2.0의 파괴적 변경은 클래스 이름 하나로 끝나지 않는다. 굵직한 것만 모아보자.

| 항목 | 1.x | 2.0 |
|---|---|---|
| 서버 클래스 | `FastMCP` | `MCPServer` |
| 타입 | `mcp.types` | 별도 패키지 `mcp-types` |
| 예외 | `McpError` | `MCPError` |
| 리소스 URI | `AnyUrl` | `str` |
| 필드 표기 | camelCase | snake_case |
| 트랜스포트 지정 | 생성자 | `run` / `app` |
| HTTP 클라이언트 | `streamablehttp_client` | 제거 |
| 동기 핸들러 | — | 워커 스레드에서 실행 |

의존성도 갈아엎었다. `httpx`가 빠지고 `httpx2`가 들어왔으며, **`opentelemetry-api`가 하드 의존성으로 승격**됐다. 관찰성이 선택 사항에서 기본값으로 옮겨간 것이다. 이 변화의 의미는 8장에서 다시 만나게 된다. Roots·Sampling·Logging은 deprecated 표시가 붙었다.

그리고 Python 진영에만 있는 특별한 사실이 하나 있다. `mcp-types` 2.0.0b2의 `version.py`가 리비전을 **세대로 쪼개 상수로 못 박아 뒀다.**

```python
KNOWN_PROTOCOL_VERSIONS = ("2024-11-05","2025-03-26","2025-06-18","2025-11-25","2026-07-28")
HANDSHAKE_PROTOCOL_VERSIONS = ("2024-11-05","2025-03-26","2025-06-18","2025-11-25")
MODERN_PROTOCOL_VERSIONS = ("2026-07-28",)
```

3장에서 TypeScript SDK 2.0.0-beta.5를 볼 때, 신형 타입은 export되지만 지원 리비전 목록에 새 리비전이 **없다**는 관측을 했다. Python은 다르다. 여기서는 새 세대가 실제 협상 대상 상수 안에 들어 있다. **설계도는 양쪽에 다 있지만, 차가 건너고 있는 건 Python 쪽이다.** 다만 이 둘을 한 문장으로 묶어 "생태계가 2.0으로 넘어갔다"고 요약하는 순간 틀린 말이 된다는 것도 기억해두자.

그렇다면 당장 무엇을 해야 할까? 공식 README가 답을 대신 말해준다.

> "**Do not use v2 in production.** … **v1.x is the only stable release line**"

그리고 이렇게 덧붙인다 — 패키지가 `mcp`에 의존한다면 안정 v2가 나오기 전에 `mcp>=1.27,<2`처럼 **상한을 걸어두라**고. 지루한 조언 같지만, 어느 날 CI가 2.0을 끌어와 `FastMCP`를 못 찾고 무너지는 것보다는 훨씬 낫다. 덧붙이면, 같은 README는 정식 v2의 목표일로 2026-07-27을 적어두고 있다. 이 장의 버전 표기가 며칠 만에 낡을 수 있다는 뜻이니, 코드를 옮겨 적기 전에 공식 문서를 한 번 열어보는 습관을 들이자.

마지막으로 함정 두 가지만 짚어두자. 첫째, PyPI에 `fastmcp`라는 **별개 패키지**(3.4.4)가 있다. 공식 `mcp`에 통합됐던 그 FastMCP와 이름만 같은 다른 노선이다. 검색하다 섞어 쓰면 난감해진다. 둘째, 인자에 `Optional[str]`을 쓰면 생성되는 `anyOf [X, null]` 스키마가 **모델에 도달하기 전에 사라질 수 있다.** 아무도 에러를 내지 않는데 도구가 이상하게 동작하는 유형이다 — 8장에서 정면으로 다룬다.

여기까지가 Python이다. 데코레이터 몇 개로 서버 하나가 완성됐고, 다음 세대가 어떤 모양일지도 눈으로 확인했다. 그런데 같은 서버를 JVM에서 만들면 어떨까? 애너테이션 몇 개로 끝날까, 아니면 스타터 고르는 데만 반나절이 걸릴까?
