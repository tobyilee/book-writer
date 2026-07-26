<!-- 검색 시점: 2026-07-26 기준 -->

# 웹 리서치: MCP 서버 개발 (최신 스펙 + SDK + 배포)

**슬러그:** `mcp-server-development` · **장르:** tech-book
**대상 독자:** MCP 서버를 직접 만들어 쓰려는 개발자 (TypeScript / Python / Java 실무자)
**검색 시점: 2026-07-26 기준** — 아래 모든 버전·리비전 주장은 이 날짜에 실제로 fetch한 1차 소스에 근거한다.

> **재검증 스탬프:** 핵심 주장(스펙 `schema/` 디렉토리 목록·릴리스 태그·`LATEST_PROTOCOL_VERSION`·npm/PyPI dist-tags)을 리서치 **종료 직전 2026-07-26T03:03:09Z에 재조회**해 전부 동일함을 확인했다. `2026-07-28-RC`는 이 시각에도 여전히 `PRERELEASE`이고 `schema/2026-07-28/`는 여전히 없다.

---

## ⚠️ 이 리서치의 헤드라인 — 책 1페이지에서 바로잡아야 할 사실

> **오늘(2026-07-26)은 MCP 역사상 가장 나쁜 타이밍의 이틀 전이다.**
> `2026-07-28` 리비전이 **모레 정식 릴리스 예정**이고, 이 리비전은 `initialize` 핸드셰이크를 없애는 **파괴적 재설계**다.

| 축 | 2026-07-26 기준 확정 사실 | 근거 |
|---|---|---|
| **스펙 최신 "정식"** | `2025-11-25` | `schema/` 디렉토리 열거 + `LATEST_PROTOCOL_VERSION` 상수 |
| **스펙 최신 "RC"** | `2026-07-28` (prerelease, 2026-05-29 태깅, **정식 예정일 2026-07-28**) | GitHub Releases API `prerelease: true` |
| **"MCP 2.0" 스펙** | **존재하지 않음.** 스펙은 날짜 리비전만 사용 | 아래 §2-3 |
| **"2.0"의 정체** | **SDK 메이저 버전.** Java SDK 2.0.0 = **GA**, Spring AI 2.0.0 = **GA**, TS/Python 2.0 = **beta** | 아래 §2-4 |

---

# 토픽 2 — 최신 스펙 리비전 확정 (최우선 검증 과제)

## 2-1. `schema/` 디렉토리 열거 (주장이 아니라 열거)

**출처:** `https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/contents/schema`
**신뢰성: 최상 (1차 — GitHub Contents API 실제 디렉토리 리스팅)**
**검색: 2026-07-26 기준**

`main` 브랜치 `schema/` 하위 디렉토리 **전부**:

```
2024-11-05/
2025-03-26/
2025-06-18/
2025-11-25/
draft/
```

**핵심:** `schema/2026-07-28/` 디렉토리는 **아직 존재하지 않는다**. 이것은 확인된 부정적 발견이다 (열거로 확인). 2026-07-28 리비전은 아직 `draft/`에 산다.

## 2-2. `LATEST_PROTOCOL_VERSION` 상수 — `initialize`가 협상하는 바로 그 문자열

**출처:** `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/{revision}/schema.ts`
**신뢰성: 최상 (1차 — 소스 상수)** · **검색: 2026-07-26 기준**

| 파일 | 상수 값 |
|---|---|
| `schema/2025-06-18/schema.ts:12` | `export const LATEST_PROTOCOL_VERSION = "2025-06-18";` |
| `schema/2025-11-25/schema.ts:12` | `export const LATEST_PROTOCOL_VERSION = "2025-11-25";` |
| `schema/draft/schema.ts:30` | `export const LATEST_PROTOCOL_VERSION = "2026-07-28";` |
| (모든 리비전 공통) | `export const JSONRPC_VERSION = "2.0";` |

> ⚠️ **혼동 지점:** `JSONRPC_VERSION = "2.0"`. 이 `"2.0"`은 **JSON-RPC 2.0** 스펙 버전이지 MCP 버전이 아니다. "MCP 2.0"이라는 표현이 생기는 경로 중 하나로 의심된다.

## 2-3. GitHub Releases — "2.0"이라는 태그는 역사상 존재한 적 없다

**출처:** `https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/releases`
**신뢰성: 최상 (1차)** · **검색: 2026-07-26 기준**

| tag_name | published_at | 상태 |
|---|---|---|
| `2026-07-28-RC` | 2026-05-29 | **prerelease: true** |
| `2025-11-25` | 2025-11-25 | stable ← **현재 최신 정식** |
| `2025-11-25-RC` | 2025-11-15 | prerelease |
| `2025-06-18` | 2025-06-18 | stable |
| `2025-03-26` | 2025-03-26 | stable |
| `2024-11-05-final` | 2025-03-26 | stable |
| `2024-11-05` | 2025-01-17 | stable |
| `2024-10-07` | 2024-11-06 | stable |

**전 릴리스 태그가 날짜 형식이다. `v2.0`·`2.0`·`MCP 2.0`은 하나도 없다.**

`2026-07-28-RC` 릴리스 노트 원문 인용:

> "This release marks the **release candidate (RC)** `2026-07-28` revision of the Model Context Protocol."
>
> "**To users and implementers:** this specification is not final. Changes may be introduced between the RC and the final release. SDKs will adopt this version at their own pace, and the prior version of the spec may remain in use for an undetermined amount of time."

**관련 섹션:** 1장 도입부 — "당신이 들은 'MCP 2.0'은 무엇이었나" 바로잡기.

## 2-4. "MCP 2.0" 판정 — 세 갈래로 나눠 기록 (합치면 오독된다)

**세 개의 독립된 판정이다. 하나로 합치지 말 것.**

**(a) 스펙 축 — "MCP 2.0"은 공식 명칭으로 존재하지 않는다. (확정)**
스펙은 2024-10-07부터 지금까지 **날짜 리비전만** 써왔다. `schema/` 디렉토리 열거·릴리스 태그 전수·`LATEST_PROTOCOL_VERSION` 상수 세 경로로 교차 확인했고, 어디에도 "2.0"이 없다.

**(b) SDK 축 — "2.0"은 실재한다. 그것도 아주 크게. (확정)**

| SDK | 2.0 상태 | 날짜 |
|---|---|---|
| **Java SDK** | **`v2.0.0` GA (정식)** | 2026-06-11 |
| **Spring AI** | **`2.0.0` GA (정식)** | 2026-06-12 |
| **TypeScript SDK** | `2.0.0-beta.5` (beta) | 2026-07-21 |
| **Python SDK** | `2.0.0b2` (beta) | 2026-07-14 |

**(c) 판정 — 사용자가 말한 "2.0 스펙"은 SDK 세대를 가리켰을 가능성이 가장 높다.**
2026년 상반기에 MCP 생태계 전체가 SDK 메이저 2.0으로 넘어갔다. Java/Spring AI는 이미 GA, TS/Python은 beta. 이 물결이 "MCP가 2.0으로 업그레이드됐다"로 통칭되는 것이 자연스럽다.
**다만 잔여 모호성을 명시한다:** 사용자가 `2026-07-28` RC(진짜 파괴적 스펙 개정)를 가리켰을 가능성도 배제할 수 없다. 두 사건이 같은 분기에 겹쳤기 때문이다. 책은 **"둘 다"** 를 다루는 게 안전하다.

## 2-5. 리비전별 변경 이력 (2024-11-05 → 2026-07-28 RC)

| 리비전 | 날짜 | 주요 변경 (스펙 문서 확인분만) |
|---|---|---|
| `2024-10-07` | 2024-11-06 | 최초 공개 태그 |
| `2024-11-05` | 2025-01-17 | 최초 정식 리비전 |
| `2025-03-26` | 2025-03-26 | Streamable HTTP 도입, **HTTP+SSE 트랜스포트 deprecated 시작** |
| `2025-06-18` | 2025-06-18 | (아래 2025-11-25 changelog가 이 리비전을 직전 비교 대상으로 삼음) |
| `2025-11-25` | 2025-11-25 | **현 정식** — 아래 §2-6 |
| `2026-07-28` | RC (2026-05-29) | **파괴적 재설계** — 아래 §2-7 |

## 2-6. `2025-11-25` 주요 변경점 (현재 정식 리비전)

**출처:** `https://modelcontextprotocol.io/specification/2025-11-25/changelog`
**신뢰성: 최상 (1차 — 공식 스펙 changelog)** · **검색: 2026-07-26 기준**
(2025-06-18 대비 변경)

**Major changes (원문 인용):**

> 1. "Enhance authorization server discovery with support for **OpenID Connect Discovery 1.0**." (PR #797)
> 2. "Allow servers to expose **icons** as additional metadata for tools, resources, resource templates, and prompts (SEP-973)."
> 3. "Enhance authorization flows with **incremental scope consent** via `WWW-Authenticate` (SEP-835)"
> 4. "Provide guidance on **tool names** (SEP-986)"
> 5. "Update `ElicitResult` and `EnumSchema` to use a more standards-based approach and support titled, untitled, single-select, and multi-select enums (SEP-1330)."
> 6. "Added support for **URL mode elicitation** (SEP-1036)"
> 7. "Add **tool calling support to sampling** via `tools` and `toolChoice` parameters (SEP-1577)"
> 8. "Add support for **OAuth Client ID Metadata Documents** as a recommended client registration mechanism (SEP-991)"
> 9. "Add **experimental support for tasks** to enable tracking durable requests with polling and deferred result retrieval (SEP-1686)."

**Minor changes 중 저술에 쓸 만한 것:**

> 1. "Clarify that servers using **stdio transport may use stderr for all types of logging**, not just error messages" (PR #670)
> 5. "Clarify that **input validation errors should be returned as Tool Execution Errors rather than Protocol Errors** to enable model self-correction (SEP-1303)."
> 10. "Establish **JSON Schema 2020-12 as the default dialect** for MCP schema definitions (SEP-1613)."
> 3. "Clarify that servers must respond with **HTTP 403 Forbidden for invalid Origin headers** in Streamable HTTP transport." (PR #1439)

**거버넌스:**
> 4. "Establish **SDK tiering system** with clear requirements for feature support and maintenance commitments (SEP-1730)."

**관련 섹션:** 2장(프로토콜 기초), 4장(elicitation/tasks), 7장(인증).

## 2-7. `2026-07-28` RC 주요 변경점 — **MCP를 stateless로 만드는 재설계**

**출처:** `https://modelcontextprotocol.io/specification/draft/changelog`
**신뢰성: 최상 (1차 — 공식 draft changelog)** · **검색: 2026-07-26 기준**
**⚠️ RC 상태 — 정식 확정 전. 정식 예정일 2026-07-28.**

**Major changes (원문 인용 — 이 책의 뼈대가 될 내용):**

> 1. "**Remove protocol-level sessions and the `Mcp-Session-Id` header** from the Streamable HTTP transport. List endpoints (`tools/list`, `resources/list`, `prompts/list`) no longer vary per-connection. Servers that need cross-call state use explicit, server-minted handles passed as ordinary tool arguments (SEP-2567)."
>
> 2. "**Make MCP stateless: remove the `initialize`/`notifications/initialized` handshake.** Every request now carries its protocol version and client capabilities in `_meta` (`io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientCapabilities`). Clients SHOULD identify themselves on each request (`io.modelcontextprotocol/clientInfo`), and servers SHOULD identify themselves in each result's `_meta` (`io.modelcontextprotocol/serverInfo`). Version mismatches return `UnsupportedProtocolVersionError` (SEP-2575)."
>
> 3. "**Add `server/discover`**: servers MUST implement this RPC to advertise their supported protocol versions, capabilities, and identity. Clients MAY call it before any other request for up-front version selection, or use it as a backward-compatibility probe on STDIO (SEP-2575)."
>
> 4. "Replace the HTTP GET endpoint and `resources/subscribe`/`resources/unsubscribe` with **`subscriptions/listen`**: a single long-lived POST-response stream for opted-in server-to-client change notifications. ... (SEP-2575)"
>
> 5. "**Remove `ping`, `logging/setLevel`, and `notifications/roots/list_changed`.** Log level is now set per-request via `io.modelcontextprotocol/logLevel` in `_meta` ... (SEP-2575)"
>
> 6. "**Move experimental tasks out of the core protocol and into an official extension** (`io.modelcontextprotocol/tasks`). The redesigned extension replaces the blocking `tasks/result` method with polling via `tasks/get` and a new `tasks/update` for client-to-server input, removes `tasks/list` ... (SEP-2663)"
>
> 7. "**Multi Round-Trip Requests (MRTR)** pattern introduced which replaces the previous approach of sending server-initiated requests, such as `roots/list`, `sampling/createMessage`, or `elicitation/create`. Servers return an `InputRequiredResult` (`resultType: "input_required"`) whose `inputRequests` field carries the requests for the additional information needed to process the request. Clients respond with `inputResponses` on a retry of the original request ... (SEP-2322)"
>
> 8. "All results now carry a required **`resultType`** field: `"complete"` for ordinary results and `"input_required"` for multi round-trip request interim results. Clients **MUST** treat results from earlier-protocol servers that omit the field as `"complete"` (SEP-2322)."
>
> 9. "**Remove SSE stream resumability and message redelivery** (the `Last-Event-ID` header and SSE event IDs) from the Streamable HTTP transport. A broken response stream loses the in-flight request; clients **MUST** re-issue it as a new request with a new request ID (SEP-2575)."

**Deprecated (원문 인용) — 책의 "무엇을 배우지 말아야 하는가" 섹션 재료:**

> 1. "**Deprecate the Roots, Sampling, and Logging features** (SEP-2577). These features remain fully functional during the deprecation window but new implementations should not add support for them. Suggested migrations: pass directories or files via tool parameters, resource URIs, or server configuration instead of **Roots**; integrate directly with LLM provider APIs instead of **Sampling**; log to `stderr` (stdio) or use OpenTelemetry instead of **Logging**."
>
> 2. "Reclassify the **HTTP+SSE transport (deprecated since protocol version `2025-03-26`)** as Deprecated under the feature lifecycle policy (SEP-2596). Migrate to Streamable HTTP."
>
> 4. "**Deprecate the OAuth 2.0 Dynamic Client Registration Protocol (RFC7591)** as a client registration mechanism in favor of **Client ID Metadata Documents** (PR #2858)."

**Minor changes 중 중요:**

> 1. "Add **`extensions` field** to `ClientCapabilities` and `ServerCapabilities` to support optional extensions beyond the core protocol."
> 4. "Require standard MCP request headers (**`Mcp-Method`, `Mcp-Name`**) on Streamable HTTP POST requests, and add support for custom headers from tool parameters via `x-mcp-header` (SEP-2243)."
> 5. "Require **`ttlMs` and `cacheScope`** fields on results returned by `tools/list`, `prompts/list`, `resources/list`, `resources/read`, and `resources/templates/list` via a new **`CacheableResult`** interface. ... `cacheScope` (`"public"` or `"private"`) controls whether shared intermediaries may cache the response (SEP-2549)."
> 6. "Change **resource not found error code from `-32002` to `-32602`** (Invalid Params) to align with JSON-RPC specification."
> 10. "Loosen `inputSchema` and `outputSchema` to allow any **JSON Schema 2020-12** keywords, and `structuredContent` to allow any JSON value (SEP-2106)."
> 12. "Define an **error code allocation policy** ... `-32000` to `-32019` remains implementation-defined (existing SDK usage is grandfathered), `-32020` to `-32099` is reserved for the MCP specification. Renumber ... `HeaderMismatch` `-32001` → `-32020`, `MissingRequiredClientCapability` `-32003` → `-32021`, `UnsupportedProtocolVersion` `-32004` → `-32022`."

**거버넌스 — 책에서 "왜 이렇게 자주 바뀌나"에 답할 재료:**
> "Adopt a specification **feature lifecycle and deprecation policy** defining the Active, Deprecated, and Removed feature states, a **minimum twelve-month deprecation window**, and a registry of deprecated features (SEP-2596)."

**관련 섹션:** 별도 장 하나 통째로 — "2026-07-28: MCP가 stateless가 되다".

## 2-8. 교차 검증 — Python SDK 2.0 소스가 리비전 세대를 코드로 구분한다

**출처:** `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.0.0b2/src/mcp-types/mcp_types/version.py`
**신뢰성: 최상 (1차 — SDK 소스)** · **검색: 2026-07-26 기준**

이 파일 하나가 §2-7의 구조 변화를 코드로 증명한다:

```python
KNOWN_PROTOCOL_VERSIONS: Final[tuple[str, ...]] = (
    "2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25", "2026-07-28",
)
"""Every released protocol revision, oldest to newest."""

HANDSHAKE_PROTOCOL_VERSIONS: Final[tuple[str, ...]] = (
    "2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25",
)
"""Protocol revisions reachable via the initialize handshake."""

MODERN_PROTOCOL_VERSIONS: Final[tuple[str, ...]] = ("2026-07-28",)
"""Protocol revisions that use the stateless per-request envelope."""
```

`LATEST_HANDSHAKE_VERSION` docstring: *"Newest revision reachable via the `initialize` handshake; the client's offer and server's counter-offer default."*
`LATEST_MODERN_VERSION` docstring: *"Newest per-request-envelope revision; the `server/discover` probe default."*

**책에 그대로 쓸 만한 설계 논평 (파일 상단 docstring 원문):**

> "Date-string protocol revisions happen to sort lexicographically, but versions are an **enumerated set, not an ordered scalar**: future identifiers are not guaranteed to be date-shaped, and unrecognized peer strings must compare conservatively instead of accidentally (e.g. `"zzz" > "2025-11-25"`)."

→ **"버전 문자열을 부등호로 비교하지 마라"** 는 실무 교훈의 1차 출처.

**관련 섹션:** 버전 협상 장.

---

# 토픽 1 — MCP 핵심 기술

## 1-1. MCP란 무엇인가 (공식 정의)

**출처:** `https://modelcontextprotocol.io/docs/getting-started/intro`
**신뢰성: 최상 (1차 — 공식 문서)** · **검색: 2026-07-26 기준**

> "MCP (Model Context Protocol) is an **open-source standard for connecting AI applications to external systems**."
>
> "Think of MCP like a **USB-C port for AI applications**. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems."

생태계 지원 (원문):
> "AI assistants like Claude and ChatGPT, development tools like Visual Studio Code, Cursor, MCPJam, and many others all support MCP — making it easy to **build once and integrate everywhere**."

**관련 섹션:** 1장 도입.

## 1-2. 아키텍처·primitives·트랜스포트 (확인된 사실 정리)

**신뢰성: 최상 (1차 — 스펙 changelog·SDK 소스에서 교차 확인)**

- **JSON-RPC 2.0 기반** — 전 리비전 공통 `JSONRPC_VERSION = "2.0"` (§2-2)
- **서버 primitives:** tools / resources / prompts — 전 SDK README·스펙에서 일관 확인
  - 관련 메서드: `tools/list`, `resources/list`, `prompts/list`, `resources/read`, `resources/templates/list` (§2-7 minor change 5에 전부 열거됨)
- **서버→클라이언트 방향 primitives:** roots, sampling, elicitation, logging
  - `2025-11-25`까지: 서버가 클라이언트에 요청을 보내는 방식 (`roots/list`, `sampling/createMessage`, `elicitation/create`)
  - `2026-07-28` RC: **MRTR 패턴으로 전면 대체**, 그리고 **Roots·Sampling·Logging은 deprecated** (§2-7)
- **lifecycle:** `initialize` / `notifications/initialized` 핸드셰이크 + capability negotiation
  - **`2026-07-28` RC에서 제거됨** → `server/discover` + per-request `_meta` 봉투 (§2-7)
- **트랜스포트:**
  - **stdio** — 전 리비전 지원. stdio에서 stderr는 모든 로깅에 사용 가능 (2025-11-25 minor 1)
  - **Streamable HTTP** — `2025-03-26` 도입, 현재 권장
  - **HTTP+SSE** — `2025-03-26`부터 deprecated, `2026-07-28`에서 feature lifecycle상 Deprecated로 재분류 (§2-7)
- **에러 규약:** JSON-RPC 에러 코드. `2026-07-28`에서 할당 정책 신설 — `-32000~-32019` 구현 정의(기존 SDK grandfathered), `-32020~-32099` 스펙 예약 (§2-7 minor 12)

**관련 섹션:** 2~3장.

## 1-3. tasks — `2025-11-25` experimental의 흔적이 SDK 코드에 남아 있다

**출처:** `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.29.0/src/types.ts`
**신뢰성: 최상 (1차 — SDK 소스)** · **검색: 2026-07-26 기준**

```typescript
export const LATEST_PROTOCOL_VERSION = '2025-11-25';
export const DEFAULT_NEGOTIATED_PROTOCOL_VERSION = '2025-03-26';
export const SUPPORTED_PROTOCOL_VERSIONS = [LATEST_PROTOCOL_VERSION, '2025-06-18', '2025-03-26', '2024-11-05', '2024-10-07'];

export const RELATED_TASK_META_KEY = 'io.modelcontextprotocol/related-task';

/* JSON-RPC types */
export const JSONRPC_VERSION = '2.0';
```

**주목:** `DEFAULT_NEGOTIATED_PROTOCOL_VERSION = '2025-03-26'` — 협상 실패 시 fallback이 최신이 아니라 `2025-03-26`이다. Python SDK v1.28.1도 동일 (`DEFAULT_NEGOTIATED_VERSION = "2025-03-26"`). 실무에서 "왜 내 서버가 구버전으로 붙지?"의 답.

**관련 섹션:** 버전 협상 장 / 트러블슈팅.

---

# 토픽 3 — 언어별 서버 SDK

> **세 축을 절대 섞지 말 것: (1) SDK 버전 · (2) 릴리스 날짜 · (3) 그 SDK가 지원하는 스펙 리비전.**

## 3-1. TypeScript — 1.x와 2.x가 완전히 다른 패키지다

**출처:** npm registry API + `https://github.com/modelcontextprotocol/typescript-sdk` README (main)
**신뢰성: 최상 (1차 — 레지스트리 메타데이터 + 공식 README)** · **검색: 2026-07-26 기준**

### v1 (프로덕션 권장)

| 항목 | 값 |
|---|---|
| 패키지 | `@modelcontextprotocol/sdk` |
| **현재 버전** | **`1.29.0`** (npm `dist-tags.latest`) |
| **릴리스 날짜** | **2026-03-30** |
| **지원 스펙 리비전** | `LATEST = 2025-11-25`, `SUPPORTED = [2025-11-25, 2025-06-18, 2025-03-26, 2024-11-05, 2024-10-07]` |
| 총 배포 버전 수 | 78 |

### v2 (beta — 2026-07-28 스펙 구현)

**모노레포가 패키지를 쪼갰다.** 전부 `2.0.0-beta.5` (2026-07-21):

| 패키지 | 역할 | dist-tags |
|---|---|---|
| `@modelcontextprotocol/server` | MCP 서버 구축 | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/client` | "Model Context Protocol implementation for TypeScript - Client package" | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/core` | "public Zod schemas (spec + OAuth/OpenID)" | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/node` | Node.js Streamable HTTP 트랜스포트 래퍼 | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/express` | Express 어댑터 | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/hono` | Hono 어댑터 | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/fastify` | Fastify 어댑터 | beta=`2.0.0-beta.5`, **latest=`2.0.0-beta.4`** |
| `@modelcontextprotocol/server-legacy` | "Frozen v1 SSE transport and OAuth Authorization Server helpers... **Deprecated**" | latest=beta=`2.0.0-beta.5` |
| `@modelcontextprotocol/codemod` | "**Codemod to migrate MCP TypeScript SDK code from v1 to v2**" | latest=beta=`2.0.0-beta.5` |

**공식 README 원문 인용 (책에 그대로 쓸 가치가 있음):**

> "**This is the `main` branch — v2 of the SDK, now in beta** (`@modelcontextprotocol/server`, `@modelcontextprotocol/client`), implementing the 2026-07-28 MCP spec."
>
> "We expect a **stable release alongside the full release of the 2026-07-28 spec on July 28, 2026**. Until then, **v1.x remains the supported release for production**; it keeps receiving bug fixes and security updates for **at least 6 months after v2 ships**."

> "This repository contains the TypeScript SDK implementation of the MCP specification. It runs on **Node.js, Bun, and Deno**"

**Zod 사용 여부 — v1과 v2가 다르다 (중요):**

> "Tool and prompt schemas use **[Standard Schema](https://standardschema.dev/)** — bring **Zod v4, Valibot, ArkType, or any compatible library**."

→ v2는 Zod 고정이 아니라 Standard Schema 인터페이스. `@modelcontextprotocol/core`는 여전히 "public Zod schemas"를 노출.

**미들웨어 패키지 설계 철학 (원문):**
> "They are intentionally **thin adapters**: they should not introduce new MCP functionality or business logic."

**문서 URL:** v1 = `https://ts.sdk.modelcontextprotocol.io/` · v2 = `https://ts.sdk.modelcontextprotocol.io/v2/`

**관련 섹션:** TS 서버 구현 장 + "v1으로 배울 것인가 v2로 배울 것인가" 결정 섹션.

## 3-2. Python — `mcp` (FastMCP 통합)

**출처:** PyPI JSON API + python-sdk GitHub releases/README
**신뢰성: 최상 (1차)** · **검색: 2026-07-26 기준**

| 항목 | 값 |
|---|---|
| 패키지 | `mcp` |
| **현재 안정 버전** | **`1.28.1`** (PyPI `info.version`) |
| **릴리스 날짜** | **2026-06-26** |
| **지원 스펙 리비전** | `LATEST_PROTOCOL_VERSION = "2025-11-25"`, `DEFAULT_NEGOTIATED_VERSION = "2025-03-26"` (`src/mcp/types.py:27,35`) |
| requires_python | `>=3.10` |
| **2.0 프리릴리스** | `2.0.0b2` (2026-07-14). a1(06-11) → a2(06-16) → a3(06-26) → b1(06-30) → b2(07-14) |
| **2.0.0b2가 지원하는 스펙 리비전** | **`LATEST_PROTOCOL_VERSION = "2026-07-28"`** — `KNOWN`=(2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, **2026-07-28**), `HANDSHAKE`=…2025-11-25, `MODERN`=(2026-07-28) (`mcp_types/version.py`) |

> ⚠️ **세 축 혼동 주의 (fact-checker 필독).** Python SDK는 **같은 패키지의 v1과 v2가 서로 다른 스펙 세대를 구현한다**:
> - `mcp` **1.28.1** → 스펙 **`2025-11-25`** (핸드셰이크 방식)
> - `mcp` **2.0.0b2** → 스펙 **`2026-07-28`** 까지 (stateless per-request 봉투 포함, §2-8)
>
> §3-2 표만 읽고 "Python 2.0도 2025-11-25를 따른다"고 결론 내리면 **틀린다.** 반대로 **Java SDK 2.0.0 / Spring AI 2.0.0은 `2025-11-25`** 다 — "SDK 2.0"이라는 숫자가 같아도 구현 스펙은 언어마다 다르다.

**2.0의 구조 변경:** 타입이 별도 패키지 `mcp-types`로 분리됐다 (PyPI `mcp-types` `2.0.0b2`, 2026-07-14). `src/mcp/__init__.py`가 `from mcp_types import (...)`로 재수출. `mcp_types` 내부에 `v2025_11_25/`·`v2026_07_28/` 버전별 wire 타입 서브패키지 존재.

**공식 README v1 원문 — 실무자가 반드시 읽어야 할 경고:**

> "v2 pre-releases are published to PyPI as `2.0.0aN`. Installers never select a pre-release unless you opt in (for example `pip install mcp==2.0.0a1`), so v1.x users are unaffected. **If your package depends on `mcp`, add a `<2` upper bound to your version constraint (for example `mcp>=1.27,<2`) before the stable v2 release lands.**"

**FastMCP API 형태 (v1.28.1 README 발췌 — 라인 96~137):**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", json_response=True)

@mcp.tool()
def ...

@mcp.resource("greeting://{name}")
def ...

@mcp.prompt()
def ...

# Run with streamable HTTP transport
    mcp.run(transport="streamable-http")
```

**설치:**
```bash
uv add "mcp[cli]"     # 권장
pip install "mcp[cli]"
```
→ `[cli]` extra가 `mcp` CLI를 설치한다.

README가 명시한 트랜스포트: *"Use standard transports like **stdio, SSE, and Streamable HTTP**"*

**마이그레이션 문서:** `https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/migration.md`, `README.v2.md`

**관련 섹션:** Python 서버 구현 장.

## 3-3. Java — 공식 Java SDK 2.0.0 (GA)

**출처:** `https://api.github.com/repos/modelcontextprotocol/java-sdk/releases/tags/v2.0.0`
**신뢰성: 최상 (1차 — 공식 릴리스 노트)** · **검색: 2026-07-26 기준**

| 항목 | 값 |
|---|---|
| **현재 버전** | **`v2.0.0` (GA/stable)** |
| **릴리스 날짜** | **2026-06-11** |
| **지원 스펙 리비전** | **`2025-11-25`** (릴리스 노트 명시) |
| 이전 계열 | `v1.1.3`(2026-05-21), `v0.18.3`(2026-06-09) 병행 유지 |
| 마일스톤 경로 | M1 → M2(2026-05-13) → M3(2026-05-21) → RC1(2026-06-04) → **2.0.0(2026-06-11)** |

**릴리스 노트 원문 인용:**

> "We're thrilled to announce the **General Availability of the MCP Java SDK 2.0.0** — the first major release since 1.x and the culmination of three milestones (M1, M2, M3) and a release candidate (RC1). It **tracks the latest 2025-11-25 MCP specification** and lays the groundwork for everything that comes next."

**Highlights (원문):**
> - "A new **JSON compatibility foundation** for consistent forward/backward wire compatibility as the protocol evolves."
> - "**Spec-accurate schema** with enforced required fields and lenient wire deserialization."
> - "**End-to-end validation** of tool inputs and embedded JSON Schema documents (2020-12)."
> - "**Richer elicitation**: client-side schema defaults, URL elicitation, and form-based elicitation schemas."
> - "**Icons & metadata** support (SEP-973) across the API."
> - "**Streamable HTTP first**: SSE transports are now deprecated in favor of Streamable HTTP."
> - "Cleaner, quieter logging with unified configuration and saner default levels."

**Breaking Changes (원문 발췌):**
> - "feat!: consistent JSON forward/backward compatibility — the 2.0 foundation (PR #927)"
> - "feat!: enforce required MCP spec fields in `McpSchema`; lenient wire deserialization (PR #928)"
> - "feat!: add tool input arguments validation (#697) (PR #873)"
> - "fix: Remove `JsonSchema` and use a `Map` for `inputSchema` to support JSON Schema dialects (PR #749)"

**마이그레이션 가이드:** `https://github.com/modelcontextprotocol/java-sdk/blob/v2.0.0/MIGRATION-2.0.md`

**관련 섹션:** Java 서버 구현 장.

## 3-4. Spring AI — MCP 서버 스타터 2.0.0 (GA)

**출처:** Maven Central `maven-metadata.xml` (권위 소스 — solrsearch 인덱스는 2025-05-19에서 멈춰 있어 신뢰 불가)
`https://repo1.maven.org/maven2/org/springframework/ai/{artifact}/maven-metadata.xml`
**신뢰성: 최상 (1차 — Maven Central 저장소 메타데이터)** · **검색: 2026-07-26 기준**

| groupId | artifactId | **release** | lastUpdated |
|---|---|---|---|
| `org.springframework.ai` | `spring-ai-bom` | **`2.0.0`** | 20260612110418 (2026-06-12) |
| `org.springframework.ai` | `spring-ai-starter-mcp-server` | **`2.0.0`** | 2026-06-12 |
| `org.springframework.ai` | `spring-ai-starter-mcp-server-webmvc` | **`2.0.0`** | 2026-06-12 |
| `org.springframework.ai` | `spring-ai-starter-mcp-server-webflux` | **`2.0.0`** | 2026-06-12 |
| `org.springframework.ai` | `spring-ai-starter-mcp-client` | **`2.0.0`** | 2026-06-12 |
| `org.springframework.ai` | `spring-ai-starter-mcp-client-webflux` | (동일 계열) | — |

버전 히스토리 (마지막 8개, 전 아티팩트 동일):
`2.0.0-M4 → M5 → M6 → M7 → M8 → RC1 → RC2 → 2.0.0`

**세 가지 서버 변형 (아티팩트명이 곧 답이다):**
- `spring-ai-starter-mcp-server` — **stdio** (플레인)
- `spring-ai-starter-mcp-server-webmvc` — **WebMVC** (동기, Streamable HTTP)
- `spring-ai-starter-mcp-server-webflux` — **WebFlux** (리액티브)

**타이밍 주목:** Spring AI 2.0.0(2026-06-12)이 Java SDK 2.0.0(2026-06-11) **바로 다음 날** 나왔다. Spring AI 2.0이 Java SDK 2.0을 물고 올라간 것으로 보이며, 따라서 **스펙 `2025-11-25` 계열**로 추정된다.

### Spring AI 2.0.0 서버 API — `@Tool`이 아니라 **`@McpTool`** 이다 (중요 정정)

**출처(1차·원문):** `https://raw.githubusercontent.com/spring-projects/spring-ai/main/spring-ai-docs/src/main/antora/modules/ROOT/pages/api/mcp/mcp-server-boot-starter-docs.adoc`
**출처(1차·원문):** 같은 디렉토리 `mcp-annotations-server.adoc`
**신뢰성: 최상 (1차 — Spring AI 레퍼런스 문서 asciidoc 원문. 렌더링 페이지가 아니라 소스 파일에서 직접 인용)** · **검색: 2026-07-26 기준**
**렌더링 문서상 현재 버전: Spring AI `2.0.0` (Stable). 병행: `1.1.8` (Stable), `2.0.1-SNAPSHOT`, `1.1.9-SNAPSHOT`**

**아티팩트 × 프로토콜 매트릭스 (adoc 원문 표에서 그대로 발췌 — 29·36~38·44~46행):**

| 서버 유형 | artifactId | 활성화 프로퍼티 |
|---|---|---|
| STDIO | `spring-ai-starter-mcp-server` | `spring.ai.mcp.server.stdio=true` |
| SSE WebMVC *(deprecated since 2.0.0, use STREAMABLE instead)* | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=SSE` |
| Streamable-HTTP WebMVC | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| Stateless WebMVC | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STATELESS` |
| SSE WebFlux *(deprecated since 2.0.0, use STREAMABLE instead)* | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=SSE` |
| Streamable-HTTP WebFlux | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| Stateless WebFlux | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STATELESS` |

> **중요:** 아티팩트는 3개인데 **프로토콜은 프로퍼티로 고른다.** WebMVC/WebFlux 아티팩트 하나가 SSE·STREAMABLE·STATELESS 셋을 다 커버한다. "WebMVC용 Streamable 스타터"를 따로 찾으면 안 된다.
> `_(deprecated since 2.0.0, use STREAMABLE instead)_` 는 **adoc 원문 그대로**다 — §3-3 java-sdk 2.0.0 릴리스 노트의 "SSE transports are now deprecated in favor of Streamable HTTP"와 독립 교차 확인됐다.

**adoc 원문 인용 — STREAMABLE / STATELESS 설명:**

> "**Streamable-HTTP** - The Streamable HTTP transport allows MCP servers to operate as independent processes that can handle multiple client connections using HTTP POST and GET requests, with optional Server-Sent Events (SSE) streaming for multiple server messages. **It replaces the SSE transport.** To enable the `STREAMABLE` protocol, set `spring.ai.mcp.server.protocol=STREAMABLE`."
>
> (STATELESS에 대해) "They are ideal for **microservices architectures and cloud-native deployments**. To enable the `STATELESS` protocol, set `spring.ai.mcp.server.protocol=STATELESS`."

**툴 등록 — `@McpTool` (adoc `mcp-annotations-server.adoc` 원문 그대로):**

> "The `@McpTool` annotation marks a method as an MCP tool implementation with **automatic JSON schema generation**."

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

**`@McpTool` 애노테이션 속성 (adoc 표 원문):**

| Attribute | Default | Description |
|---|---|---|
| `name` | method name | "The tool identifier. Defaults to the method name if not provided." |
| `description` | method name | "Human-readable description of the tool." |
| `title` | `""` | "Intended for UI and end-user contexts — optimized to be human-readable. If not provided, `name` is used for display. (Precedence: `annotations.title` > `title` > `name`)" |
| `generateOutputSchema` | `false` | "If `true`, automatically generates a JSON output schema for non-primitive return types." |
| `annotations` | `@McpAnnotations` | "Additional hints for clients (see tool annotations below)." |
| `metaProvider` | `DefaultMetaProvider.class` | "Class implementing `MetaProvider` that supplies data for the `_meta` field in the tool declaration." |

**주요 애노테이션 (adoc 98행 등):** `@McpTool` · `@McpToolParam` · `@McpResource`(URI 템플릿) · `@McpPrompt` · `@McpComplete`

**책에 쓸 만한 세 가지 관찰:**

1. **`@Tool`/`ToolCallbackProvider`가 아니다 — `@McpTool`이다.** Spring AI의 일반 툴 콜링 API(`@Tool`, `MethodToolCallbackProvider`)와 **MCP 서버 전용 애노테이션(`@McpTool` 등)은 별개 체계**다. 구버전 자료를 보고 `@Tool`로 MCP 서버를 만들려다 막히는 것이 예상되는 지점 — 책이 명시적으로 갈라줘야 한다.
2. **`protocol=STATELESS`가 이미 있다.** §2-7의 `2026-07-28` stateless 방향과 정확히 맞물린다. Spring AI 2.0이 stateless 운용을 선반영했다는 뜻이며, 전용 문서 `mcp-stateless-server-boot-starter-docs.adoc`까지 따로 있다.
3. **문서가 트랜스포트별로 쪼개져 있다** — `mcp-stdio-sse-server-boot-starter-docs.adoc` / `mcp-streamable-http-server-boot-starter-docs.adoc` / `mcp-stateless-server-boot-starter-docs.adoc` / `mcp-annotations-server.adoc` / `mcp-security.adoc`. 챕터 구성 시 이 분할을 참고할 만하다.

> ⚠️ **여전히 미확인:** (a) `@McpTool` 애노테이션이 **Spring AI 소속인지 MCP Java SDK 소속인지** — Java SDK 2.0이 annotations 모듈을 제공할 가능성이 있고, 이는 책의 의존성 안내(어느 아티팩트를 추가해야 하는가)를 바꾼다. (b) Spring AI 2.0.0이 pin하는 java-sdk 정확한 버전 (BOM 의존성 트리 미확인).

**관련 섹션:** Spring 개발자용 장.

## 3-5. 기타 언어 (한 줄씩)

**신뢰성: 중 — 저장소 존재는 확인, 버전은 미확인.** `modelcontextprotocol` org 하위에 Kotlin/C#/Go/Rust SDK가 존재하나 이번 세션에서 버전을 열거하지 못했다. §확인하지 못한 것 참조.
참고: `2025-11-25`에서 **"Establish SDK tiering system with clear requirements for feature support and maintenance commitments (SEP-1730)"** 가 도입됐다 — SDK별 지원 등급이 공식화됐다는 뜻. 언어 선택 시 티어를 확인하라는 조언의 근거.

---

# 토픽 7 — 배포

## 7-1. npm 배포 → `npx` 실행 (가장 중요한 경로)

**출처:** `https://raw.githubusercontent.com/modelcontextprotocol/registry/main/docs/modelcontextprotocol-io/quickstart.mdx`
**신뢰성: 최상 (1차 — 공식 레지스트리 문서)** · **검색: 2026-07-26 기준**

공식 퀵스타트가 제시하는 절차 (원문 인용):

**package.json 준비:**
```diff
 {
-  "name": "mcp-quickstart-ts",
-  "version": "1.0.0",
+  "name": "@my-username/mcp-weather-server",
+  "version": "1.0.1",
+  "mcpName": "io.github.my-username/weather",
   "main": "index.js",
```
```diff
+  "repository": {
+    "type": "git",
+    "url": "https://github.com/my-username/mcp-weather-server.git"
+  },
+  "description": "An MCP server for weather information.",
```

**빌드 → 배포:**
```bash
npm install
npm run build
npm adduser          # 필요 시 인증
npm publish --access public
```

> "Then follow npm's publishing guide. In particular, you will probably need to run the following commands"

**스코프 패키지 + `--access public`** — 공식 문서가 스코프 패키지(`@my-username/...`)를 기본으로 삼고 `--access public`을 명시한다. 스코프 패키지는 기본이 private이므로 이 플래그가 없으면 배포가 실패한다.

**참고 예제 저장소:** `https://github.com/modelcontextprotocol/quickstart-resources` (`weather-server-typescript`)

### `package.json` 실물 — 공식 quickstart 예제 서버 (bin·files·ESM)

**출처:** `https://raw.githubusercontent.com/modelcontextprotocol/quickstart-resources/main/weather-server-typescript/package.json`
**신뢰성: 최상 (1차 — 공식 예제 저장소 실물 파일)** · **검색: 2026-07-26 기준**

```json
{
  "name": "mcp-quickstart-ts",
  "version": "1.0.0",
  "main": "index.js",
  "type": "module",
  "bin": {
    "weather": "./build/index.js"
  },
  "scripts": {
    "build": "tsc && node -e \"require('fs').chmodSync('build/index.js', '755')\""
  },
  "files": [
    "build"
  ],
  "keywords": [],
  "author": "",
  "license": "ISC",
  "description": "",
  "devDependencies": {
    "@types/node": "^22.19.2",
    "typescript": "^5.9.3"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.24.3"
  }
}
```

**책에서 짚어야 할 4가지 (전부 이 파일에서 직접 관찰됨):**

1. **`"type": "module"`** — ESM. TS SDK v1은 ESM 전제로 쓴다.
2. **`"bin": { "weather": "./build/index.js" }`** — `npx`가 실행할 수 있게 만드는 핵심 필드. 키(`weather`)가 곧 커맨드 이름이 된다.
3. **`"files": ["build"]`** — 배포 tarball에 `build/`만 포함. 소스·설정 제외.
4. **`prepublishOnly`가 없다.** 대신 **build 스크립트가 직접 `chmod 755`** 를 한다: `tsc && node -e "require('fs').chmodSync('build/index.js', '755')"`. 컴파일 산출물에 실행 권한이 없으면 `npx`가 실패하기 때문이다 — Windows에서도 동작하도록 `chmod` 대신 Node 인라인 스크립트를 쓴 점이 실무 팁.

> 🔍 **shebang — 확정된 부정적 발견 (예상과 반대).** 실제 경로는 `weather-server-typescript/src/index.ts`(루트가 아니라 `src/`)였고, **그 파일 첫 줄에 shebang이 없다.** 확인된 첫 3줄:
> ```typescript
> import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
> import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
> import { z } from "zod";
> ```
> 즉 **공식 quickstart 예제는 `bin` 타깃에 shebang을 넣지 않고 `chmod 755`만 한다.** 유닉스에서 `bin` 스크립트는 통상 `#!/usr/bin/env node`가 필요하므로, 이 예제를 그대로 `npm publish` → `npx`로 실행했을 때 동작하는지는 **경험적 검증이 필요하다**. 책에서 이 예제를 베끼기 전에 반드시 실제로 돌려보고, 필요하면 shebang 추가를 권고해야 한다. **"공식 예제가 이렇게 돼 있다"와 "이렇게 하면 된다"는 다르다.**
>
> 또한 이 예제는 `@modelcontextprotocol/sdk: ^1.24.3`(v1 계열)에 고정돼 있고 `McpServer`·`StdioServerTransport`·`zod`를 쓴다 — **v2 패키지 기준 예제가 아니다.**
> 참고로 v1의 import 경로 형태가 여기서 확인된다: `@modelcontextprotocol/sdk/server/mcp.js`, `@modelcontextprotocol/sdk/server/stdio.js` (ESM `.js` 확장자 포함).

**관련 섹션:** 배포 장 (가장 상세히).

## 7-2. MCP Registry — **preview, GA 아님**

**출처(1):** `https://raw.githubusercontent.com/modelcontextprotocol/registry/main/README.md`
**출처(2):** `https://api.github.com/repos/modelcontextprotocol/registry/releases`
**신뢰성: 최상 (1차)** · **검색: 2026-07-26 기준**

| 항목 | 값 |
|---|---|
| **소프트웨어 릴리스** | `v1.8.0` (2026-07-13) — 직전 `v1.7.9` (2026-05-12) |
| **API 상태** | **preview / API freeze v0.1 — GA 아님** |
| 저장소 활동 | stars 7,068 · pushed 2026-07-25 |
| Live API docs | `https://registry.modelcontextprotocol.io/docs` |

**공식 문서 원문 인용 (quickstart.mdx 상단 Note):**

> "**The MCP Registry is currently in preview.** Breaking changes or data resets may occur before general availability."

**README "Development Status" 원문:**

> "**2025-10-24 update**: The Registry API has entered an **API freeze (v0.1)** 🎉. For the next month or more, the API will remain stable with no breaking changes, allowing integrators to confidently implement support. This freeze applies to v0.1 while development continues on v0. We'll use this period to validate the API in real-world integrations and gather feedback to shape **v1 for general availability**."
>
> "**2025-09-08 update**: The registry has launched in **preview** 🎉. While the system is now more stable, this is still a preview release and breaking changes or data resets may occur. **A general availability (GA) release will follow later.**"

> ⚠️ **주의:** README의 Development Status 최신 항목이 **2025-10-24**에 멈춰 있다(저장소 릴리스는 2026-07-13까지 진행). README가 stale일 가능성이 있으나, **quickstart.mdx의 "currently in preview" Note는 main 브랜치 현행 문서**이므로 preview 판정의 근거로 삼는다.

**레지스트리 성격 (원문):**
> "The MCP registry provides MCP clients with a list of MCP servers, **like an app store for MCP servers**."
>
> "**The MCP Registry only hosts metadata, not artifacts**, so we must publish the package to npm before publishing the server to the MCP Registry."

**Registry Working Group:** Tadas Antanavicius (PulseMCP), Radoslav Dimitrov (Stacklok), Bob Dickinson (TeamSpark), Preeti Dewani (Ravenmail)

## 7-3. `mcp-publisher` CLI + 소유권 검증

**출처:** 위 quickstart.mdx · **신뢰성: 최상 (1차)** · **검색: 2026-07-26 기준**

**Step 1 — 패키지에 소유권 검증 정보 추가 (npm의 경우 `mcpName`):**

> "The MCP Registry verifies that a server's underlying package matches its metadata. For npm packages, this requires adding an `mcpName` property to `package.json`"
>
> "The value of `mcpName` will be your server's name in the MCP Registry. Because we will be using GitHub-based authentication, `mcpName` **must** start with `io.github.my-username/`."

**지원 패키지 타입 (원문):** "npm, **PyPI, NuGet, OCI, MCPB**" — 각 타입마다 소유권 검증 방식이 다르며 `./package-types` 문서 참조.

**Step 3 — `mcp-publisher` 설치:**

```bash
# macOS/Linux
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/

# Homebrew
brew install mcp-publisher
```
Windows는 `mcp-publisher_windows_{amd64|arm64}.tar.gz`를 `Invoke-WebRequest`로 받아 PATH에 배치.

**인증:** "The MCP Registry supports **multiple authentication methods**" — 튜토리얼은 GitHub 기반 인증 사용.

**`mcp-publisher --help` 출력 원문:**

```text
MCP Registry Publisher Tool

Usage:
  mcp-publisher <command> [arguments]

Commands:
  init          Create a server.json file template
  login         Authenticate with the registry
  logout        Clear saved authentication
  publish       Publish server.json to the registry
```

**Step 4 — `server.json` 생성 (`mcp-publisher init`). 생성물 원문:**

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.my-username/weather",
  "description": "An MCP server for weather information.",
  "repository": {
    "url": "https://github.com/my-username/mcp-weather-server",
    "source": "github"
  },
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "npm",
      "identifier": "@my-username/mcp-weather-server",
      "version": "1.0.0",
      "transport": {
        "type": "stdio"
      },
      "environmentVariables": [
        {
          "description": "Your API key for the service",
          "isRequired": true,
          "format": "string",
          "isSecret": true,
          "name": "YOUR_API_KEY"
        }
      ]
    }
  ]
}
```

> **`server.json` 스키마 버전: `2025-12-11`** (`$schema` URL에 박혀 있다). 스펙 리비전과 **다른 날짜 체계**임에 주의 — 레지스트리 스키마는 독자 버저닝을 한다.

**핵심 제약 (원문 인용):**
> "The `name` property in `server.json` **must** match the `mcpName` property in `package.json`."

**Step 5 — 인증:**
```bash
mcp-publisher login github
```
GitHub Device Flow. 출력 원문: *"To authenticate, please: 1. Go to: https://github.com/login/device 2. Enter code: ABCD-1234 3. Authorize this application"*

**Step 6 — 배포 및 확인:**
```bash
mcp-publisher publish
# → ✓ Successfully published
# → ✓ Server io.github.my-username/weather version 1.0.1

curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.my-username/weather"
```

> **API 엔드포인트가 `/v0.1/`이다** — §7-2의 "API freeze (v0.1)" 상태와 정확히 일치한다. GA(v1)가 아니라는 독립적 증거.

**트러블슈팅 표 (원문 인용) — 패키지 타입별 소유권 검증 마커:**

| Error Message | Action |
|---|---|
| "Registry validation failed for package" | "Ensure your package includes the required ownership-verification marker for its package type. **For npm this is `mcpName` in `package.json`; for PyPI and NuGet it is an `mcp-name: <server-name>` line (or HTML comment) in the package README**; for other types see Package Types." |
| "Invalid or expired Registry JWT token" | "Re-authenticate by running `mcp-publisher login github`." |
| "You do not have permission to publish this server" | "Your authentication method doesn't match your server's namespace format. With GitHub auth, your server name **must start with `io.github.your-username/`**." |

→ **PyPI/NuGet은 `package.json`이 없으므로 README에 `mcp-name: <server-name>` 줄을 넣는다.** 이건 1차 소스에서만 알 수 있는 실무 디테일.

**관련 섹션:** 배포 장 — 레지스트리 등록.

## 7-4. PyPI + `uvx` / `uv run`, Docker

**신뢰성: 중~최상 혼재 · 검색: 2026-07-26 기준**

- **PyPI:** Registry가 PyPI 패키지 타입을 지원함은 quickstart가 명시 (§7-3). Python SDK 설치 권장 경로는 `uv add "mcp[cli]"` (§3-2, 1차 확인).
- **Docker/OCI:** Registry가 **OCI** 패키지 타입을 지원 (§7-3, 1차 확인). Registry 자체도 컨테이너로 배포되며 README가 `ko`(Go 컨테이너 이미지 빌더)와 GitHub Container Registry 사용을 명시 — 단 이건 레지스트리 서버 운영 얘기지 MCP 서버 배포 일반론은 아니다.
> ⚠️ **미확인:** `uvx`로 MCP 서버를 실행하는 공식 문서상 정확한 커맨드, MCP 서버용 Dockerfile 공식 권장 패턴. §확인하지 못한 것 참조.

## 7-5. 원격 서버(Streamable HTTP) 배포 — 인증·세션

**신뢰성: 최상 (1차 — 스펙 changelog에서 도출)** · **검색: 2026-07-26 기준**

- **세션 관리:** `2025-11-25`까지는 `Mcp-Session-Id` 헤더 기반 프로토콜 레벨 세션. **`2026-07-28` RC에서 완전 제거** — "Servers that need cross-call state use **explicit, server-minted handles passed as ordinary tool arguments**" (§2-7)
- **보안:** "servers must respond with **HTTP 403 Forbidden for invalid Origin headers** in Streamable HTTP transport" (2025-11-25 minor 3)
- **OAuth 진화:**
  - `2025-11-25`: OpenID Connect Discovery 1.0 지원, `WWW-Authenticate` 기반 incremental scope consent, **OAuth Client ID Metadata Documents를 권장 등록 메커니즘으로 추가**
  - `2026-07-28` RC: **RFC7591 Dynamic Client Registration을 deprecated**, Client ID Metadata Documents로 이행. `iss` 파라미터 검증(RFC 9207) 요구, DCR 시 `application_type` 지정 요구, 클라이언트 자격증명을 발급 authorization server별로 키잉 요구 (§2-7)
- **캐싱/중계:** `2026-07-28` RC의 `CacheableResult`(`ttlMs`, `cacheScope`) — `cacheScope: "public"|"private"`가 **공유 중계자의 캐싱 가능 여부**를 제어 (§2-7 minor 5)

**관련 섹션:** 원격 배포·인증 장.

---

# 부록 — 클라이언트 연결 (Claude Code)

**출처:** `https://code.claude.com/docs/en/mcp` (`docs.claude.com/en/docs/claude-code/mcp`에서 301 리다이렉트)
**신뢰성: 최상 (1차 — Anthropic 공식 문서)** · **검색: 2026-07-26 기준**

**CLI 커맨드 (원문 그대로):**

```bash
# stdio (로컬 프로세스)
claude mcp add [options] <name> -- <command> [args...]
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable -- <command>

# HTTP (Streamable HTTP)
claude mcp add --transport http <name> <url>
claude mcp add --transport http notion https://mcp.notion.com/mcp

# SSE (레거시)
claude mcp add --transport sse <name> <url>
claude mcp add --transport sse asana https://mcp.asana.com/sse

# JSON 직접 (WebSocket 등)
claude mcp add-json events-server '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{"Authorization":"Bearer YOUR_TOKEN"}}'

# 관리
claude mcp list
claude mcp get github
claude mcp remove github
/mcp                      # 세션 내 패널
```

**`--` 의 의미 (원문 인용) — 초보자가 가장 많이 틀리는 지점:**

> "For stdio servers, the `--` (double dash) separates Claude's own options, such as `--transport`, `--env`, and `--scope`, from the command and arguments that run the server. **Everything after `--` is passed to the server untouched.**"
>
> 예: `claude mcp add --transport stdio myserver -- npx server` → runs `npx server`

**스코프 (원문):**
> "Use the `-s` or `--scope` flag to specify where the configuration is stored: ... `project`: shared with everyone in the project via the `.mcp.json` file"
> (local / project / user 3종)

**`type` 필드 별칭 (원문) — 스펙 명칭과 CLI 명칭의 간극:**
> "When configuring MCP servers via JSON in `.mcp.json`, `~/.claude.json`, or `claude mcp add-json`, the `type` field accepts **`streamable-http` as an alias for `http`**. The MCP specification uses the name `streamable-http` for this transport, so configurations copied from server documentation work without modification."

**OAuth:**
> "Use `/mcp` to authenticate with remote servers that require **OAuth 2.0** authentication"

**WebSocket vs HTTP 선택 기준 (원문):**
> "Use HTTP instead when your server only responds to requests, since **HTTP supports OAuth and the `claude mcp add --transport` flag, while WebSocket supports neither**."

**타임아웃:**
> "Set a per-server tool execution timeout by adding a `timeout` field in milliseconds to that server's `.mcp.json` entry, for example `"timeout": 600000` for ten minutes. This overrides the `MCP_TOOL_TIMEOUT` environment variable for that server only."
> HTTP/SSE는 별도로 **첫 응답 바이트까지 60초** per-request 타이머가 존재. stdio·WebSocket은 per-request 타이머 없음.

**재연결:**
> "If an HTTP or SSE server disconnects mid-session, Claude Code automatically reconnects with exponential backoff: **up to five attempts, starting at a one-second delay and doubling each time**. ... **Stdio servers are local processes and are not reconnected automatically.**"

**예약어 (원문):** `workspace`, `claude-in-chrome`, `computer-use`, `Claude Preview`, `Claude Browser` — "`claude mcp add` rejects a reserved name with an error."

**서버 스캐폴딩 도구:**
> "You can also have Claude scaffold a server for you with the official [`mcp-server-dev` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev)."
> 슬래시 커맨드: `/mcp-server-dev:build-mcp-server`

**관련 섹션:** "만든 서버를 붙여 쓰기" 장.

---

## 신선도 원장

| # | 소스 | URL | 발행일/버전 시점 | 신뢰성 | 검색 시점 |
|---|---|---|---|---|---|
| 1 | MCP 스펙 `schema/` 디렉토리 열거 | api.github.com/.../modelcontextprotocol/contents/schema | main HEAD | 최상 (1차·열거) | 2026-07-26 |
| 2 | `schema/{rev}/schema.ts` 상수 | raw.githubusercontent.com/.../schema.ts | main HEAD | 최상 (1차·소스) | 2026-07-26 |
| 3 | MCP 스펙 GitHub Releases | api.github.com/.../releases | 최신 `2026-07-28-RC` (2026-05-29) | 최상 (1차) | 2026-07-26 |
| 4 | `2026-07-28` draft changelog | modelcontextprotocol.io/specification/draft/changelog | **RC — 정식 예정 2026-07-28** | 최상 (1차) | 2026-07-26 |
| 5 | `2025-11-25` changelog | modelcontextprotocol.io/specification/2025-11-25/changelog | 2025-11-25 | 최상 (1차) | 2026-07-26 |
| 6 | MCP 공식 소개 문서 | modelcontextprotocol.io/docs/getting-started/intro | 상시 갱신 | 최상 (1차) | 2026-07-26 |
| 7 | npm `@modelcontextprotocol/sdk` | registry.npmjs.org | **1.29.0 / 2026-03-30** | 최상 (1차) | 2026-07-26 |
| 8 | npm `@modelcontextprotocol/{server,core,node,express,hono,fastify,server-legacy,codemod}` | registry.npmjs.org | **2.0.0-beta.5 / 2026-07-21** | 최상 (1차) | 2026-07-26 |
| 9 | TS SDK README (main = v2) | github.com/modelcontextprotocol/typescript-sdk | v2 beta, 안정판 예정 **2026-07-28** | 최상 (1차) | 2026-07-26 |
| 10 | TS SDK v1.29.0 `src/types.ts` | raw.githubusercontent.com/.../v1.29.0/src/types.ts | 1.29.0 → 스펙 2025-11-25 | 최상 (1차·소스) | 2026-07-26 |
| 11 | PyPI `mcp` | pypi.org/pypi/mcp/json | **1.28.1 / 2026-06-26**, 2.0.0b2 / 2026-07-14 | 최상 (1차) | 2026-07-26 |
| 12 | PyPI `mcp-types` | pypi.org/pypi/mcp-types/json | 2.0.0b2 / 2026-07-14 | 최상 (1차) | 2026-07-26 |
| 13 | python-sdk `mcp_types/version.py` (v2.0.0b2) | raw.githubusercontent.com/.../v2.0.0b2/... | 2.0.0b2 | 최상 (1차·소스) | 2026-07-26 |
| 14 | python-sdk `src/mcp/types.py` (v1.28.1) | raw.githubusercontent.com/.../v1.28.1/... | 1.28.1 → 스펙 2025-11-25 | 최상 (1차·소스) | 2026-07-26 |
| 15 | python-sdk README (v1.28.1) | raw.githubusercontent.com/.../v1.28.1/README.md | 1.28.1 | 최상 (1차) | 2026-07-26 |
| 16 | java-sdk `v2.0.0` 릴리스 노트 | api.github.com/.../java-sdk/releases/tags/v2.0.0 | **2.0.0 GA / 2026-06-11 → 스펙 2025-11-25** | 최상 (1차) | 2026-07-26 |
| 17 | Maven Central `spring-ai-*` metadata | repo1.maven.org/maven2/org/springframework/ai/... | **2.0.0 / lastUpdated 2026-06-12** | 최상 (1차) | 2026-07-26 |
| 18 | MCP Registry README | raw.githubusercontent.com/.../registry/main/README.md | **Status 항목은 2025-10-24에 멈춤 (stale 의심)** | 최상 (1차, 단 stale) | 2026-07-26 |
| 19 | MCP Registry publish quickstart | .../registry/main/docs/modelcontextprotocol-io/quickstart.mdx | main HEAD — "currently in preview" | 최상 (1차) | 2026-07-26 |
| 20 | MCP Registry GitHub Releases | api.github.com/.../registry/releases | **v1.8.0 / 2026-07-13** | 최상 (1차) | 2026-07-26 |
| 21 | Claude Code MCP 문서 | code.claude.com/docs/en/mcp | 상시 갱신 (v2.1.196/2.1.208 언급) | 최상 (1차) | 2026-07-26 |
| 22 | quickstart-resources `weather-server-typescript/package.json` | raw.githubusercontent.com/.../quickstart-resources/main/... | main HEAD · sdk `^1.24.3` 의존 | 최상 (1차·실물 파일) | 2026-07-26 |
| 23 | Spring AI `mcp-server-boot-starter-docs.adoc` (원문) | raw.githubusercontent.com/spring-projects/spring-ai/main/spring-ai-docs/.../api/mcp/ | main HEAD · 렌더 문서상 **2.0.0 Stable** | 최상 (1차·원문) | 2026-07-26 |
| 24 | Spring AI `mcp-annotations-server.adoc` (원문) | 〃 같은 디렉토리 | main HEAD | 최상 (1차·원문) | 2026-07-26 |
| 25 | `server.json` 스키마 | static.modelcontextprotocol.io/schemas/**2025-12-11**/server.schema.json | 스키마 버전 2025-12-11 | 최상 (1차) | 2026-07-26 |
| 26 | npm `@modelcontextprotocol/client` | registry.npmjs.org | **2.0.0-beta.5** | 최상 (1차) | 2026-07-26 |
| 27 | quickstart-resources `weather-server-typescript/src/index.ts` | raw.githubusercontent.com/.../src/index.ts | main HEAD — **shebang 없음(확인)** | 최상 (1차·실물) | 2026-07-26 |

**2차 소스 사용 내역: 없음.** 이번 리서치는 전량 1차 소스(공식 스펙·SDK 소스·패키지 레지스트리·공식 문서)로 구성했다. 버전·수치 주장 중 2차 소스에 근거한 것은 하나도 없다.

---

## 확인하지 못한 것 / 부정적 발견

### A. 확정된 부정적 발견 (= 조사 완료된 결론. 미조사가 아님)

1. **"MCP 2.0"은 스펙의 공식 명칭으로 존재하지 않는다.** 세 경로로 확인:
   (a) `schema/` 디렉토리 열거 — 날짜 디렉토리 4개 + `draft` 뿐
   (b) GitHub Releases 태그 전수 — `2024-10-07`~`2026-07-28-RC`, 전부 날짜
   (c) `LATEST_PROTOCOL_VERSION` 상수 — 전부 날짜 문자열
   유일한 `"2.0"`은 `JSONRPC_VERSION = "2.0"`(JSON-RPC 스펙 버전)이다.

2. **`schema/2026-07-28/` 디렉토리는 2026-07-26 시점에 존재하지 않는다.** `main`과 `2026-07-28-RC` 태그 **양쪽 모두** 디렉토리 리스팅으로 확인했고, 두 곳 다 `2024-11-05 / 2025-03-26 / 2025-06-18 / 2025-11-25 / draft` 5개뿐이다. 2026-07-28 리비전은 아직 `draft/`에 있다.

3. **TypeScript SDK에 2.x 정식 릴리스는 없다.** `@modelcontextprotocol/sdk`의 `dist-tags`는 `{latest: 1.29.0}` 단 하나 — `next`·`beta` 태그조차 없다. 2.0은 **별도 패키지 이름**(`@modelcontextprotocol/server` 등)으로만 존재하며 전부 beta다.

4. **Python `mcp`에 2.x 정식 릴리스는 없다.** PyPI `info.version` = `1.28.1`. 2.0은 a1~b2 프리릴리스만 존재.

5. **MCP Registry는 GA가 아니다.** 공식 quickstart가 "currently in preview"라고 명시. GA 선언 문구를 어디서도 찾지 못했다. API 엔드포인트가 `/v0.1/servers`인 것이 독립 증거.

6. **공식 quickstart 예제의 `bin` 타깃에 shebang이 없다.** `weather-server-typescript/src/index.ts` 첫 줄은 `import`다 (§7-1). 예상과 반대되는 결과이므로 "공식 예제에 shebang이 있다"고 쓰면 안 된다.

7. **Spring AI MCP 서버는 `@Tool`/`ToolCallbackProvider`를 쓰지 않는다.** `@McpTool`·`@McpToolParam`·`@McpResource`·`@McpPrompt`·`@McpComplete` 별도 체계다 (§3-4, adoc 원문 확인). 과제 지시서가 가정했던 `@Tool` 형태는 **틀린 전제**였다.

### B. 확인하지 못한 것 (후속 리서치 필요 — 챕터 저술 전 반드시 보강)

1. ~~`package.json`의 `bin`·`files`·ESM 설정~~ → **해소 (§7-1).** ~~shebang 미확인~~ → **해소, 단 결과가 예상과 반대** (§7-1의 부정적 발견): 공식 예제에 **shebang이 없다**. 잔여 과제는 조사가 아니라 **경험적 검증** — 실제로 publish 후 `npx` 실행이 되는지 돌려볼 것.
2. ~~`server.json` 스키마 및 `mcp-publisher` 서브커맨드~~ → **해소 (§7-3).** 잔여: `server.schema.json`(2025-12-11) **전체 필드 목록**은 미확인 — quickstart 예제에 등장하는 필드만 확보. `transport.type`이 `stdio` 외에 어떤 값을 받는지, remote(Streamable HTTP) 서버 등록 시 `packages` 대신 무엇을 쓰는지 미확인.
3. ~~Spring AI 서버 API 형태~~ → **해소, adoc 원문으로 재검증 완료 (§3-4).** 예상과 달리 **`@Tool`이 아니라 `@McpTool`**이며, 아티팩트 3개 × 프로토콜 프로퍼티 매트릭스 구조. 잔여: **`@McpTool`의 소속 아티팩트(Spring AI vs MCP Java SDK annotations 모듈)** 와 Spring AI 2.0.0이 pin하는 java-sdk 버전.
4. **`uvx` / `uv run`으로 MCP 서버를 실행하는 공식 커맨드**, MCP 서버 Dockerfile 공식 권장 패턴. (미해소 — 토픽 7에서 가장 약한 부분)
5. **Kotlin/C#/Go/Rust SDK 버전** — 저장소 존재는 알려져 있으나 이번 세션에서 버전을 열거하지 않았다. SEP-1730 SDK 티어링 등급표도 미확인.
6. **`2026-07-28` RC의 `server/discover` RPC 상세 시그니처**와 `_meta` 봉투 필드 전체 목록 — changelog 수준까지만 확인. 스펙 본문(`/specification/draft/basic/...`) 미열람.
7. **Claude Agent SDK에서 MCP 서버를 연결하는 방법** — Claude Code CLI 쪽은 1차 확인했으나 Agent SDK(TS/Python) 쪽 `mcpServers` 설정 API는 확인하지 못했다.
8. **회사 엔지니어링 블로그·한국어 자료(우아한형제들·카카오·토스·네이버 D2·LINE)** — 이번 리서치는 1차 소스 검증(토픽 2)에 예산을 집중했다. 한국어 색채·맥락 자료는 0건. 대상 독자가 한국 개발자이므로 **후속 리서치에서 반드시 보강**해야 한다.

### C. 하류(fact-checker)를 위한 경고

- **이 문서의 모든 버전 주장은 2026-07-26에 고정된 스냅샷이다.** 특히 `2026-07-28` 리비전은 **2일 뒤 정식 릴리스 예정**이므로, 챕터 저술·팩트체크 시점에 `schema/` 디렉토리와 GitHub Releases를 **반드시 재확인**하라. `schema/2026-07-28/`가 생겼고 `2026-07-28` 릴리스가 `prerelease: false`가 됐다면 이 문서의 §2-1~2-3은 그 즉시 낡는다.
- 같은 이유로 **TS SDK 2.0.0 정식**과 **Python SDK 2.0.0 정식**도 며칠 내 나올 수 있다 (TS README: "stable release alongside the full release of the 2026-07-28 spec on July 28, 2026").
- **Java SDK 2.0.0과 Spring AI 2.0.0은 스펙 `2025-11-25`를 따른다.** "2.0"이라는 숫자가 같다고 `2026-07-28` 스펙을 구현한다고 착각하지 마라. **SDK 메이저 버전과 스펙 리비전은 완전히 독립된 축이다.**

## 수집 한계

- **접근 실패:** `https://registry.modelcontextprotocol.io/docs` — WebFetch가 제목만 반환(SPA 렌더링). GitHub 저장소의 마크다운 원문으로 우회했다.
- **신뢰 불가로 폐기한 소스:** `search.maven.org/solrsearch` — 인덱스가 2025-05-19에서 멈춰 Spring AI를 `1.0.0`으로 잘못 보고했다. `repo1.maven.org`의 `maven-metadata.xml`(권위 소스)로 교체해 `2.0.0`을 확인했다. **다른 리서치에서도 Maven 버전을 solrsearch로 확인하지 말 것.**
- **의도적으로 제외한 소스 유형:** 커뮤니티(Reddit/HN/velog 등)와 논문 — 별도 에이전트 담당. 개인 블로그의 "MCP 2.0" 서술 — 1차 소스와 충돌 시 무의미하므로 애초에 수집하지 않았다.
- **접근 실패(2) → 해소:** `quickstart-resources/weather-server-typescript/index.ts` 404 → 실제 경로가 `src/index.ts`였다. 재조회 성공.
- **소스 등급 상향:** Spring AI 섹션(§3-4)은 처음에 렌더링 HTML을 요약 경유해 얻었으나, **asciidoc 원문(`.adoc`)을 직접 fetch해 전량 재검증**했다. 표·인용문은 전부 원문 발췌다.
- **자료 건수:** 27건 (전량 1차 소스). 목표 8~15건 초과 — 토픽 2의 검증 요구가 다각 교차 확인을 요구했기 때문.
- **언어 비율:** 영어 100%. 대상 독자가 한국 개발자임을 감안하면 한국어 자료 보강이 필요하다 (§B-8).
