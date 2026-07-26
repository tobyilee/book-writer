# 6장. Java와 Spring AI — `@McpTool`, 그리고 GA인 2.0의 진짜 의미

공식 Java SDK 2.0.0 릴리스 노트에 이런 문장이 있다.

> "**General Availability of the MCP Java SDK 2.0.0** — the first major release since 1.x… It **tracks the latest 2025-11-25 MCP specification**."

한 문장 안에 `2.0.0`과 `2025-11-25`가 나란히 붙어 있다. 잠시 멈추고 이 문장을 들여다보자. 버전이 2.0인데, 따르는 스펙은 이 책이 주로 다루는 그 리비전, 그러니까 **현행 정식**이다. 1장에서 네 개의 버전 축을 따로 세워둔 이유가 바로 이 문장이다. SDK의 메이저 번호가 올라간 것과 스펙 리비전이 바뀌는 것은 애초에 다른 축에서 벌어지는 일이다.

숫자만 보고 "2.0이니까 최신 스펙이겠지"라고 넘겨짚는 순간, JVM 진영의 지형이 통째로 어긋나 보이기 시작한다. 그러니 순서를 지켜 하나씩 보자.

## GA가 된 2.0이 실제로 가져온 것

먼저 좌표다. 2026-07-26 시점의 관측값이다.

| 항목 | 값 |
|---|---|
| 버전 | `2.0.0` GA (2026-06-11) |
| 좌표 | `io.modelcontextprotocol.sdk:mcp` |
| 구현 스펙 | `2025-11-25` |
| 경로 | M1 → M2(05-13) → M3(05-21) → RC1(06-04) → 2.0.0(06-11) |
| 병행 유지 | `1.1.3`(2026-05-21), `0.18.3`(2026-06-09) |

마일스톤 넷을 지나 GA에 도달했고, 이전 라인 둘도 계속 살아 있다. 급하게 밀어붙인 릴리스가 아니라는 뜻이다.

내용 쪽에서 눈여겨볼 것은 **검증이 엄격해졌다**는 점이다. 스펙에 충실한 스키마를 쓰되 들어오는 메시지는 관대하게 역직렬화하고, 도구 입력은 JSON Schema 2020-12로 종단에서 검증한다. elicitation이 URL·폼까지 받을 수 있게 넓어졌고 아이콘 지원(SEP-973)도 들어왔다.

그리고 릴리스 하이라이트에 이런 한 줄이 있다.

> "Streamable HTTP first: SSE transports are now deprecated"

2장에서 트랜스포트 3종의 지위를 정리하며 짚었던 그 방향이, JVM SDK에서도 릴리스 노트 문구로 확정됐다.

파괴적 변경은 세 가지가 대표적이다. `McpSchema`의 필수 필드가 강제되고(#928), 도구 입력 검증이 들어갔으며(#873), `JsonSchema` 타입이 사라지고 `inputSchema`가 `Map`으로 바뀌었다(#749). 1.x에서 올라온다면 `MIGRATION-2.0.md`를 먼저 펴는 편이 낫다. 특히 필수 필드 강제가 고약하다. "예전엔 비워둬도 돌아가던 것"을 깨뜨리는데, **컴파일은 멀쩡히 통과하고 런타임에 가서야 걸린다.** 배포 파이프라인에서 만나면 꽤 아찔하다.

## 스타터는 다섯 개가 전부다

Spring AI 2.0.0은 Java SDK 2.0.0이 나온 **바로 다음 날**(2026-06-12) 릴리스됐다. `spring-ai-bom`도 같은 2.0.0이다.

여기서 가장 많이 헤매는 지점을 먼저 정리하고 가자. `org.springframework.ai` 아래에 있는 MCP 관련 스타터는 **다섯 개가 전부다.** 서버 셋(`spring-ai-starter-mcp-server`, `-server-webmvc`, `-server-webflux`)과 클라이언트 둘(`-client`, `-client-webflux`)이다.

그런데 실제로 고를 수 있는 서버 조합은 일곱 가지다. 아티팩트가 일곱 개여서가 아니라, **프로토콜을 아티팩트가 아니라 프로퍼티로 고르기 때문**이다.

| 서버 유형 | artifactId | 활성화 프로퍼티 |
|---|---|---|
| STDIO | `spring-ai-starter-mcp-server` | `spring.ai.mcp.server.stdio=true` |
| SSE WebMVC *(2.0.0에서 deprecated)* | `-server-webmvc` | `spring.ai.mcp.server.protocol=SSE` |
| Streamable HTTP WebMVC | `-server-webmvc` | `protocol=STREAMABLE` |
| Stateless WebMVC | `-server-webmvc` | `protocol=STATELESS` |
| SSE WebFlux *(2.0.0에서 deprecated)* | `-server-webflux` | `protocol=SSE` |
| Streamable HTTP WebFlux | `-server-webflux` | `protocol=STREAMABLE` |
| Stateless WebFlux | `-server-webflux` | `protocol=STATELESS` |

그래서 Maven Central에서 "WebMVC용 Streamable 스타터"를 찾고 있다면 지금 멈추자. **그런 아티팩트는 없다.** 있을 필요도 없다. `-server-webmvc` 하나가 SSE·STREAMABLE·STATELESS 셋을 다 덮는다. Maven Central을 뒤지며 이름을 짐작해 넣어보는 시간이 통째로 절약된다.

`STATELESS`가 무엇에 좋은지도 문서가 직접 말해준다 — *"ideal for microservices architectures and cloud-native deployments"*. 세션 상태를 서버가 들고 있지 않아도 되는 배치라면 이쪽이 자연스럽다.

## `@Tool`이 아니라 `@McpTool`이다

Spring AI를 써봤다면 `@Tool`과 `ToolCallbackProvider`가 손에 익었을 것이다. 그래서 MCP 서버도 그 조합으로 만들려다 한참을 돌아가는 경우가 있다. 애플리케이션은 뜨는데 도구 목록이 비어 있고, 로그에는 아무것도 안 남는다. 익숙한 것을 썼다가 헤매는 상황만큼 뒷맛이 찜찜한 것도 없다.

그렇다면 무엇을 써야 할까? MCP 도구는 **별도 애너테이션 체계**를 쓴다. 이름이 비슷하다고 같은 등록 경로일 거라 넘겨짚지 말자 — 공식 레퍼런스가 안내하는 것은 `@McpTool`이다.

공식 레퍼런스 문서에 실린 계산기 예제를 그대로 옮겨 보자.

```java
@Component
public class CalculatorTools {
    @McpTool(name = "add", description = "Add two numbers together")
    public int add(
        @McpToolParam(description = "First number", required = true) int a,
        @McpToolParam(description = "Second number", required = true) int b) {
        return a + b;
    }
}
```

문서의 설명은 이렇다 — *"The `@McpTool` annotation marks a method as an MCP tool implementation with **automatic JSON schema generation**."* 메서드 하나에 애너테이션을 붙이면 JSON 스키마가 자동으로 만들어진다. 5장의 Python이 타입 힌트에서 스키마를 읽어냈다면, 여기서는 메서드 시그니처와 `@McpToolParam`이 그 자리를 대신한다.

속성도 몇 개 알아두면 편하다. `name`은 생략하면 메서드명이 되고, `title`은 `annotations.title` > `title` > `name` 순으로 결정된다. 출력 스키마 생성(`generateOutputSchema`)은 기본값이 `false`다. 리소스 쪽에는 `@McpResource`가 짝으로 있다.

의존성을 어디서 끌어와야 하는지도 짚고 가자. `@McpTool` 계열 애너테이션은 `org.springframework.ai:spring-ai-mcp-annotations`에 들어 있고, 패키지는 `org.springframework.ai.mcp.annotation`이다. 다행히 따로 추가할 필요는 없다 — 서버 스타터가 이 아티팩트를 의존으로 선언하고 있어서 스타터를 넣으면 따라 들어온다. Spring AI 2.0.0이 고정하는 Java SDK는 `io.modelcontextprotocol.sdk:mcp-bom:2.0.0`이다.

여기서 한 가지 주의할 게 있다. 커뮤니티 인큐베이터 저장소에서 출발한 같은 이름의 애너테이션들이 `org.springaicommunity.mcp.annotation` 패키지를 쓴다. **옛 블로그의 import 문을 그대로 베끼면 컴파일이 안 되거나, 되더라도 다른 물건을 쓰게 된다.** import는 IDE 자동 완성으로 채우고, 헷갈리면 의존성 트리를 한 번 열어보자.

## `team-wiki`를 JVM에서 완성하기

계산기는 문법을 보여주는 예제일 뿐이다. 우리가 만들 서버는 3장·5장과 같은 `team-wiki`다.

```java
@Component
public class WikiTools {

    private final WikiStore store;

    public WikiTools(WikiStore store) {
        this.store = store;
    }

    @McpTool(name = "wiki_search", description = "문서 제목과 본문에서 검색어를 찾는다")
    public List<WikiHit> wikiSearch(
        @McpToolParam(description = "검색어", required = true) String query,
        @McpToolParam(description = "최대 결과 수", required = false) Integer limit) {
        return store.search(query, limit == null ? 10 : limit);
    }

    @McpTool(name = "wiki_get", description = "주어진 경로의 문서 본문을 돌려준다")
    public String wikiGet(
        @McpToolParam(description = "문서 경로", required = true) String path) {
        return store.read(path);
    }
}

public record WikiHit(String path, String title) {}
```

메서드 이름은 자바 관례대로 `wikiSearch`로 두되, 도구 이름은 `name` 속성으로 `wiki_search`를 명시했다. 세 언어에서 만든 서버가 클라이언트 쪽에서 **똑같은 도구 이름**으로 보여야 하기 때문이다. 이름이 언어마다 달라지면 4장에서 만든 설정을 그대로 못 쓰고, 7장에서 이야기할 네임스페이스 규칙도 무너진다.

이제 남은 건 그 오류 케이스다. `wiki_get`에 없는 경로가 들어오면 어떻게 될까?

원칙은 세 언어가 같다. **프로토콜 레벨에서 실패시키지 말고, 도구 실행 결과로 "그 문서는 없다"를 돌려주자.** 그래야 모델이 오타를 고쳐 다시 부른다. 스택 트레이스가 프로토콜 오류로 올라가 버리면 모델 입장에서는 도구가 통째로 고장 난 것과 구분되지 않는다.

그런데 JVM에서는 이 결정이 눈에 잘 안 띈다. `@McpTool`이 붙은 메서드의 반환 타입이 곧 도구의 성공 결과라서, `String`을 돌려주는 `wikiGet`의 시그니처만 봐서는 실패를 어디에 실을지 보이지 않는다. 3장의 TypeScript에서는 반환 객체를 손으로 조립하느라 이 선택이 코드에 드러났고, 5장의 Python에서는 한 겹 감춰져 있었다면, 여기서는 **애너테이션 뒤로 완전히 들어가 있다.**

실은 자리가 둘이나 있는데도 그렇다 — 예외를 던지거나, 반환 타입을 `CallToolResult`로 두고 직접 조립하거나. 그리고 반가운 소식이 있다. 자바 개발자가 십 년 넘게 길들여진 그 습관, 그러니까 **예외를 던지는 쪽이 여기서는 정답**이다.

Spring AI 2.0.0의 `@McpTool` 처리기는 메서드에서 나온 **예외를 잡아 `CallToolResult`의 `isError`를 켜서 돌려준다.** 대상 예외 타입의 기본값이 `Exception`이니 사실상 전부다. 모델이 읽게 되는 텍스트는 `예외 메시지 + 루트 원인 메시지`이므로, 메시지 자체에 다음 행동을 적어두면 세 언어가 똑같은 결과에 도달한다.

```java
@McpTool(name = "wiki_get", description = "주어진 경로의 문서 본문을 돌려준다")
public String wikiGet(@McpToolParam(description = "문서 경로", required = true) String path) {
    String body = store.read(path);
    if (body == null) {
        throw new IllegalArgumentException(
            "'" + path + "' 문서를 찾을 수 없다. wiki_search로 경로를 먼저 확인하라.");
    }
    return body;
}
```

`@McpToolParam`의 `required`가 잡아주는 범위와 헷갈리지 말자. 필수 여부는 스키마 단계에서 걸러지지만, "형식은 맞는데 실재하지 않는 값"은 스키마가 잡아줄 수 없다. 그 판단은 결국 메서드 본문 안에 있다.

한 가지 덧붙이자면, JVM 진영의 MCP는 아직 이야깃거리가 적은 동네다. 논문도 없고, 커뮤니티에 쌓인 삽질 회고도 거의 없다. 그래서 이 장은 처음부터 끝까지 SDK와 Spring AI의 공식 문서 위에만 서 있다. "실무에서는 보통 이렇게 한다"는 말을 이 장에서 한 번도 하지 않은 이유다.

세 언어로 같은 서버를 만들어봤다. 이제 "어떻게 만드는가"보다 훨씬 어려운 질문이 남았다 — **무엇을 만들 것인가.**
