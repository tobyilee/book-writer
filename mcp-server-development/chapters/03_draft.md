# 3장. 첫 서버 — TypeScript로 `team-wiki` 만들기

사내 위키를 클로드가 직접 읽게 해달라는 요청이 왔다고 해보자. 지금은 누군가 문서를 찾아 복사해서 대화창에 붙여넣고 있다. 문서가 열 개면 견딜 만하지만 수백 개가 되면 이야기가 달라진다.

요구사항을 정리하면 두 줄이다. **문서를 검색할 수 있을 것.** **찾은 문서의 본문을 가져올 수 있을 것.** 이걸 MCP 서버로 만들어보자. 이름은 `team-wiki`로 하고, 이 서버는 앞으로 여러 장에 걸쳐 우리를 따라다닌다. 5장에서는 Python으로, 6장에서는 Spring AI로 같은 걸 다시 만들고, 9장에서 배포하고, 10장에서 원격으로 연다.

## 무엇으로 시작할 것인가

TypeScript로 MCP 서버를 만들려면 공식 SDK를 쓴다. 그런데 여기서 첫 번째 결정을 해야 한다. 1장에서 봤듯이 SDK에는 2.0 세대가 있기 때문이다.

이 결정은 "무엇이 옳다"가 아니라 **"내가 조회한 시점에 무엇이 관측됐는가"**로 접근하는 편이 낫다. 2026-07-26 시점의 관측값은 이랬다.

- `npm view @modelcontextprotocol/sdk dist-tags`의 결과는 **`latest: 1.29.0` 하나뿐**이었다. `next`도 `beta`도 없었다.
- 같은 시점 저장소 README는 v2가 베타이며 **"v1.x remains the supported release for production"**이라고 명시했고, v2가 나온 뒤에도 **최소 6개월간** v1.x에 버그 수정과 보안 패치를 계속한다고 약속했다.

그래서 이 장은 `1.29.0`(2026-03-30 게시) 기준으로 쓴다. 다만 이 값은 이 책을 읽는 시점에 이미 바뀌어 있을 수 있다. **시작하기 전에 한 번 직접 조회해보자.**

```bash
npm view @modelcontextprotocol/sdk dist-tags
```

정식 2.0이 올라와 있다면 이 장의 코드가 틀린 게 아니라 선택지가 하나 늘어난 것이다. 무엇이 달라지는지는 이 장 후반부에 따로 정리해두었다.

## 뼈대 세우기

프로젝트를 만들고 `package.json`을 이렇게 잡는다.

```json
{
  "name": "mcp-server-team-wiki",
  "version": "0.1.0",
  "type": "module",
  "bin": { "mcp-server-team-wiki": "./build/index.js" },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.29.0",
    "zod": "^3.25"
  }
}
```

두 가지만 짚자.

**`"type": "module"`** — SDK가 ESM 전제로 만들어졌다. 이 줄이 없으면 import 문에서부터 막힌다.

**`bin` 키를 패키지 이름과 똑같이 맞췄다.** 지금은 그냥 실행 파일 등록으로 보이겠지만, 이 사소한 결정이 9장에서 회수된다. 이름 하나가 세 갈래 배포 경로를 동시에 결정하기 때문이다. 지금은 "맞춰둔다"만 기억하고 넘어가자.

`tsconfig.json`에서는 `outDir`을 `build`로 잡아둔다. `bin`이 가리키는 경로와 컴파일 결과가 어긋나면 실행이 안 되니 이 둘은 늘 같이 확인하자.

의존성은 SDK와 zod 둘이다. zod는 도구의 입력 스키마를 선언하는 데 쓴다. SDK `1.29.0`은 zod 3과 4를 모두 받아준다.

이제 서버 객체를 만든다.

```ts
// src/index.ts
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "team-wiki", version: "0.1.0" });
```

`McpServer`는 고수준 API다. 저수준 `Server`를 직접 쓰면 `tools/list` 같은 요청 핸들러를 손수 등록해야 하는데, `McpServer`는 도구를 등록하면 목록 응답까지 알아서 만들어준다. 2장에서 본 capability 선언도 등록 내용에 맞춰 자동으로 채워진다. 첫 서버라면 고민할 것 없이 이쪽이다.

## 도구 두 개 붙이기

첫 번째 도구는 검색이다.

```ts
server.registerTool(
  "wiki_search",
  {
    title: "위키 검색",
    description: "제목과 본문에서 문서를 검색해 경로 목록을 돌려준다.",
    inputSchema: {
      query: z.string().describe("검색어"),
      limit: z.number().int().min(1).max(50).default(10)
    },
    outputSchema: {
      results: z.array(z.object({ path: z.string(), title: z.string() }))
    }
  },
  async ({ query, limit }) => {
    const results = await wiki.search(query, limit);   // 위키 백엔드 호출
    return {
      content: [{
        type: "text",
        text: results.map(r => `${r.path} — ${r.title}`).join("\n")
      }],
      structuredContent: { results }
    };
  }
);
```

`registerTool`은 인자를 셋 받는다. **이름**, **설정 객체**, **핸들러**다. 설정 객체에 넣을 수 있는 필드는 `title`·`description`·`inputSchema`·`outputSchema`·`annotations`·`_meta`이고, 전부 선택이다.

`inputSchema`에 zod 스키마를 넣으면 SDK가 JSON Schema로 변환해 모델에게 내보낸다. `limit`에 `.default(10)`을 붙였으니 이 필드는 필수 목록에서 빠진다. 모델이 생략하면 10이 들어온다.

여기서 눈여겨볼 건 **반환값이 둘로 갈린다**는 점이다. `content`는 모델이 읽을 텍스트고, `structuredContent`는 클라이언트 프로그램이 파싱할 데이터다. 같은 결과를 두 벌 만드는 게 낭비처럼 보이는가? 그렇지 않다. 모델에게는 읽기 좋은 요약을, 프로그램에게는 다루기 좋은 구조를 주는 것이다. 5장에서 Python SDK가 이 분리를 어떻게 표현하는지 보면 설계 의도가 더 선명해진다.

한 가지 주의할 점이 있다. `outputSchema`를 선언하면 **`structuredContent`를 반드시 함께 돌려줘야 한다.** 빠뜨리면 SDK가 검증 단계에서 오류를 던진다. 그리고 와이어 위의 `structuredContent`는 객체이지 배열이 아니다. 그래서 `{path, title}` 배열을 `results` 키로 한 번 감쌌다.

두 번째 도구는 훨씬 단순하다.

```ts
server.registerTool(
  "wiki_get",
  {
    title: "위키 문서 가져오기",
    description: "경로로 문서 본문을 가져온다.",
    inputSchema: { path: z.string().describe("문서 경로") }
  },
  async ({ path }) => {
    const doc = await wiki.get(path);
    return { content: [{ type: "text", text: doc.body }] };
  }
);
```

도구 이름에 `wiki_` 접두사를 붙인 것도, 도구를 딱 둘만 만든 것도 우연이 아니다. 왜 이렇게 하는 게 나은지는 7장에서 근거와 함께 다룬다.

## 리소스와 프롬프트

도구 말고 나머지 두 프리미티브도 하나씩 붙여보자.

```ts
server.registerResource(
  "wiki-page",
  new ResourceTemplate("wiki://{path}", { list: undefined }),
  { description: "위키 문서 한 건", mimeType: "text/markdown" },
  async (uri, { path }) => {
    const doc = await wiki.get(String(path));
    return { contents: [{ uri: uri.href, text: doc.body }] };
  }
);
```

`ResourceTemplate`의 두 번째 인자에 `{ list: undefined }`를 넘긴 게 어색해 보일 것이다. 실수가 아니다. SDK가 이 필드를 **명시적으로 요구**한다. 목록 콜백을 안 주더라도 `undefined`라고 적게 만들어서, 리소스 목록 제공을 깜빡 잊는 일을 막으려는 설계다. 친절한 강제라고 할까.

프롬프트도 붙이자.

```ts
server.registerPrompt(
  "summarize_page",
  {
    title: "문서 요약",
    description: "위키 문서 한 건을 요약한다.",
    argsSchema: { path: z.string() }
  },
  ({ path }) => ({
    messages: [{
      role: "user",
      content: { type: "text", text: `wiki://${path} 문서를 세 문단으로 요약해줘.` }
    }]
  })
);
```

프롬프트는 모델이 고르는 게 아니라 **사용자가 고르는** 것이다. 슬래시 명령처럼 노출된다고 생각하면 이해하기 쉽다.

마지막으로 트랜스포트를 연결한다.

```ts
const transport = new StdioServerTransport();
await server.connect(transport);
```

두 줄이 전부다. 이제 클라이언트가 이 프로세스를 띄우면 표준 입출력으로 JSON-RPC가 오간다.

## 없는 문서를 물어보면 어떻게 되나

여기서 잠시 멈추자. `wiki_get("없는/경로")`가 들어오면 어떻게 해야 할까?

가장 먼저 떠오르는 건 예외를 던지는 것이다. 그런데 그렇게 하면 프로토콜 레벨 오류가 되고, 모델 입장에서는 대화가 그냥 끊긴 것처럼 보인다. 무엇이 잘못됐는지도, 어떻게 고쳐야 하는지도 모른 채로 말이다. 뒷맛이 개운하지 않다.

`2025-11-25`가 이 부분을 정리했다. **입력 검증 오류는 Protocol Error가 아니라 Tool Execution Error로 돌려주라**는 것이다(SEP-1303). 이유는 명확하다. 모델이 스스로 고칠 기회를 주기 위해서다.

```ts
async ({ path }) => {
  const doc = await wiki.get(path);
  if (!doc) {
    return {
      isError: true,
      content: [{
        type: "text",
        text: `'${path}' 문서를 찾을 수 없다. wiki_search로 경로를 먼저 확인해보라.`
      }]
    };
  }
  return { content: [{ type: "text", text: doc.body }] };
}
```

`isError: true`를 실어 정상 응답으로 돌려준다. 그러면 모델은 이 텍스트를 읽고 `wiki_search`를 먼저 부른 다음 다시 시도한다. 사람이 개입하지 않아도 복구되는 것이다.

부수적인 이점도 있다. SDK는 `isError`가 붙은 결과에 대해서는 **`outputSchema` 검증을 건너뛴다.** 출력 스키마를 선언한 도구라도 오류 경로에서 구조화 데이터를 억지로 만들어 붙일 필요가 없다는 뜻이다.

**이 오류 케이스를 기억해두자.** 5장과 6장에서 Python과 Spring AI로 똑같은 상황을 재현한다. 세 언어가 같은 규정을 각자의 방식으로 어떻게 표현하는지 비교하는 게 이 책의 한 축이다.

## 별도 절 — SDK 2.0 계열은 무엇이 다른가

v1으로 시작하기로 했지만, 2.0 세대가 어떻게 생겼는지는 알아둘 필요가 있다. 아래는 `2.0.0-beta.5`(2026-07-21 기준) 관측 내용이다.

**패키지가 쪼개졌다.** 단일 `@modelcontextprotocol/sdk` 하나였던 것이 모노레포로 갈렸다 — `server`, `client`, `core`(공개 스키마), `node`(HTTP 트랜스포트 래퍼), 그리고 `express`·`hono`·`fastify` 프레임워크 어댑터, 마이그레이션용 `codemod`까지. 어댑터는 의도적으로 얇게 설계됐다. 새 기능이나 비즈니스 로직을 넣지 않는다는 게 명시된 방침이다.

**스키마 라이브러리 정책이 바뀌었다.** v1은 zod 3에 묶여 있었지만 v2는 **Standard Schema**를 채택해 zod 4·Valibot·ArkType 등을 골라 쓸 수 있다. zod를 계속 쓴다면 3에서 4로 넘어가는 메이저 점프가 따라온다.

**새 진입점과 트랜스포트가 생겼다.** stdio 서버를 한 줄로 띄우는 `serveStdio`, Cloudflare Workers 같은 환경을 겨냥한 `WebStandardStreamableHTTPServerTransport` 등이 추가됐다. 반면 `McpServer`·`registerTool`·`registerResource`·`registerPrompt`·`ResourceTemplate`은 그대로 남아 있다. 이 장에서 익힌 형태가 통째로 버려지지는 않는다는 뜻이다.

**그리고 관측된 사실 하나.** beta.5 패키지는 새 리비전용 타입(`DiscoverRequest` 등)과 세대 분기 유틸을 export하지만, 런타임의 `SUPPORTED_PROTOCOL_VERSIONS` 목록에는 `2026-07-28`이 들어 있지 **않았다.** 즉 그 시점에는 새 리비전을 실제로 협상하지 않았다. README가 새 스펙 구현을 표방한 것과 런타임 동작 사이에 아직 거리가 있었던 셈이다. 이 부분은 빠르게 바뀔 수 있으니 공식 저장소를 함께 확인하자.

## 붙여서 확인하기

빌드하고 한 줄로 붙여보자.

```bash
npx tsc
claude mcp add team-wiki -- node /절대/경로/build/index.js
```

`claude mcp list`로 목록에 뜨는지 확인한다. 붙었다면 클로드에게 "위키에서 배포 절차 문서 찾아줘"라고 시켜보자. `wiki_search`가 호출되고 결과가 돌아오면 성공이다.

물론 한 번에 되지 않을 가능성이 꽤 높다. 등록은 됐는데 도구가 안 보이거나, 붙었다는 표시는 뜨는데 아무 반응이 없거나. 그럴 때 어디를 봐야 하는지는 4장과 8장에서 차근차근 다룬다. 지금은 붙는 것 자체를 확인하는 데까지만 가면 충분하다.

---

여기까지 왔으면 도구 둘, 리소스 하나, 프롬프트 하나를 가진 서버가 손에 있다. 넘어가기 전에 하나만 해보자.

**`wiki_list_spaces`라는 도구를 하나 더 붙여보자.** 위키의 공간(스페이스) 목록을 돌려주는 도구다. 인자는 없어도 되고, 반환은 이름 목록이면 된다. `registerTool`의 설정 객체에서 `inputSchema`를 아예 빼면 인자 없는 도구가 된다.

붙여봤다면 하나 더 생각해보자. 이렇게 계속 도구를 늘려도 괜찮을까? 이 질문은 7장에서 다시 만나게 된다.
