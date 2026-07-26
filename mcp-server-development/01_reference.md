# MCP 서버 개발 레퍼런스

> **검색·검증 시점: 2026-07-26 기준.** 이 문서의 모든 버전·리비전 주장은 이 날짜에 실제로 조회한 1차 소스(스펙 저장소 파일, 패키지 레지스트리 API, 로컬 CLI 실행, GitHub 이슈, arXiv abs 페이지)에 근거한다.
> **장르:** tech-book · **슬러그:** `mcp-server-development`
> **대상 독자:** MCP 서버를 직접 만들어 쓰려는 개발자 (TypeScript / Python / Java 실무자)
>
> **출처 표기 범례:** `[웹]` web-researcher · `[커뮤]` community-researcher · `[논문]` paper-researcher · **`[검증]`** research-lead가 레지스트리·저장소·로컬 CLI를 직접 조회해 확인한 사실(산문 요약이 아니라 열거·상수·HTTP 응답).

---

## ⚠️ 최우선 정정 — "MCP 2.0 스펙"은 존재하지 않는다

기획 단계의 "최근 업그레이드된 2.0 스펙"이라는 표현은 **사실과 다르다.** 책 1페이지에서 바로잡아야 한다. **네 개의 독립된 버전 축**을 분리해야 혼동이 풀린다.

| 축 | 2026-07-26 기준 사실 | 근거 |
|---|---|---|
| **스펙 리비전** | 날짜 문자열만 사용. 최신 **정식 = `2025-11-25`** | `[검증]` `schema/` 디렉토리 열거 + `LATEST_PROTOCOL_VERSION` 상수 |
| **차기 스펙** | **`2026-07-28`** — **RC(prerelease), 정식 예정일이 이틀 뒤** | `[검증]` GitHub Releases `prerelease: true` |
| **"2.0"의 정체** | **SDK 메이저 버전.** 스펙과 무관한 독립 축 | `[검증]` 아래 표 |
| **레지스트리 스키마** | `server.json` = **`2025-12-11`** | `[검증]` 레지스트리 API 응답 `$schema` |

**"MCP 2.0" 스펙은 없다.** 스펙은 `2024-10-07`부터 지금까지 날짜 리비전만 써왔고, 릴리스 태그 전수에 `2.0`이 하나도 없다 `[검증][웹]`.

**그러나 "2.0"은 실재한다 — SDK 세대로서.** 2026년 상반기에 생태계 전체가 SDK 메이저 2.0으로 넘어갔다 `[검증][웹]`:

| SDK | 2.0 상태 | 날짜 | **구현 스펙 리비전** |
|---|---|---|---|
| **Java SDK** (`io.modelcontextprotocol.sdk:mcp`) | **2.0.0 GA** | 2026-06-11 | **`2025-11-25`** (릴리스 노트 명시) |
| **Spring AI** (`spring-ai-starter-mcp-*`) | **2.0.0 GA** | 2026-06-12 | `2025-11-25` 계열 |
| **TypeScript** (신규 스코프 패키지) | `2.0.0-beta.5` | 2026-07-21 | **런타임은 아직 `2025-11-25`까지만 협상** (README는 `2026-07-28` 표방) |
| **Python** (`mcp`) | `2.0.0b2` | 2026-07-14 | **`2025-11-25` + `2026-07-28` 실제 병행** |

> **⚠️ 결정적 증거 `[검증]` — TS와 Python의 "2026-07-28 지원"은 성숙도가 다르다. 같은 수준으로 쓰면 안 된다.**
>
> **TypeScript** `@modelcontextprotocol/core@2.0.0-beta.5` tarball을 풀어 런타임 번들(`dist/auth-*.mjs`/`.cjs`)의 상수를 직접 읽은 결과:
> ```js
> LATEST_PROTOCOL_VERSION = "2025-11-25"
> DEFAULT_NEGOTIATED_PROTOCOL_VERSION = "2025-03-26"
> SUPPORTED_PROTOCOL_VERSIONS = ["2024-10-07","2024-11-05","2025-03-26","2025-06-18", LATEST_PROTOCOL_VERSION]
> ```
> → **`2026-07-28`은 협상 가능 목록에 없다.** 패키지 안에 `2026-07-28` 문자열이 210회 나오지만 **전부 JSDoc 주석**이다(예: `@deprecated Deprecated as of protocol version 2026-07-28 (SEP-2577)`). 신형 타입(`DiscoverRequest` 등)은 export되고 세대 분기 유틸(`ProtocolEra`)도 있지만, **와이어 버전 협상은 아직 신 리비전을 제안하지 않는다.**
> → 즉 README의 *"implementing the 2026-07-28 MCP spec"*은 **beta.5 시점에선 지향 선언에 가깝다.**
>
> **Python**은 다르다. `mcp-types 2.0.0b2` wheel의 `mcp_types/version.py`에 **구조적·런타임 상수**로 명시돼 있다:
> ```python
> KNOWN_PROTOCOL_VERSIONS    = ("2024-11-05","2025-03-26","2025-06-18","2025-11-25","2026-07-28")
> HANDSHAKE_PROTOCOL_VERSIONS = ("2024-11-05","2025-03-26","2025-06-18","2025-11-25")
> MODERN_PROTOCOL_VERSIONS    = ("2026-07-28",)   # stateless per-request envelope
> ```
> → **Python 2.0의 이원 세대 지원은 확립된 사실이고, TS 2.0 beta.5의 그것은 아직 아니다.**
>
> **"2.0"이라는 숫자가 같아도 구현 스펙은 언어마다 다르다.** 이 표의 마지막 열을 절대 생략하지 마라.

**혼동의 또 다른 경로 `[웹]`:** 모든 리비전 스키마에 `JSONRPC_VERSION = "2.0"`이 있다. 이 `"2.0"`은 **JSON-RPC 2.0** 스펙 버전이지 MCP 버전이 아니다.

**책의 서술 원칙 (이 리서치의 가장 중요한 제약):**
주 서술 대상은 **`2025-11-25`(정식)**. `2026-07-28`은 "RC 기준, 확정 시 변동 가능"으로만 다룬다. 예제 코드가 `server/discover`를 전제하면 출간일에 틀린 책이 된다. RC 릴리스 노트의 공식 경고를 그대로 인용할 가치가 있다 `[검증][웹]`:

> "this specification is not final. Changes may be introduced between the RC and the final release. **SDKs will adopt this version at their own pace, and the prior version of the spec may remain in use for an undetermined amount of time.**"

---

## 1. 개념과 정의

### 1-1. MCP란 무엇인가

공식 정의 `[웹]` (modelcontextprotocol.io/docs/getting-started/intro):

> "MCP is an **open-source standard for connecting AI applications to external systems**."
> "Think of MCP like a **USB-C port for AI applications**."

학술 정의 `[논문]` — B-2(arXiv 2505.02279)의 한 줄 규정이 더 정확하다:
> "MCP provides a **JSON-RPC client-server interface for secure tool invocation and typed data exchange**."

> ⚠️ 공식 문서의 "build once and integrate everywhere"는 **마케팅 문구**다. 클라이언트마다 설정 파일·지원 기능이 갈린다는 반론이 강하다 → §4-4.

### 1-2. 아키텍처와 메시지 계층

- **JSON-RPC 2.0 기반.** 전 리비전 공통 `JSONRPC_VERSION = "2.0"` `[검증][웹]`
- **Host / Client / Server** 3자 구조
- **서버 primitives:** `tools` / `resources` / `prompts`
  메서드: `tools/list`, `tools/call`, `resources/list`, `resources/read`, `resources/templates/list`, `prompts/list`, `prompts/get` `[검증]`
- **서버→클라이언트 방향:** `roots`, `sampling`, `elicitation`, `logging`
  - `2025-11-25`까지: 서버가 클라이언트에 요청 (`roots/list`, `sampling/createMessage`, `elicitation/create`)
  - **`2026-07-28` RC: MRTR 패턴으로 전면 대체 + Roots·Sampling·Logging deprecated** → §2-3
- **lifecycle:** `initialize` / `notifications/initialized` + capability negotiation
  - **`2026-07-28` RC에서 제거** → `server/discover` + per-request `_meta` 봉투

> **보안 관점의 재분해 `[논문]` (A-9, SoK):** 서버가 노출하는 공격면은 Tools만이 아니다. **Resources·Prompts·Tools 세 primitive 각각**이 구조적 취약성을 갖는다. 세 개를 따로 위협 검토해야 한다.

### 1-3. 트랜스포트

| 트랜스포트 | 상태 (2026-07-26 기준) |
|---|---|
| **stdio** | 전 리비전 지원. 로컬 프로세스의 기본 |
| **Streamable HTTP** | `2025-03-26` 도입, 현재 권장 |
| **HTTP+SSE** (구) | `2025-03-26`부터 deprecated → `2026-07-28`에서 feature lifecycle상 **Deprecated 재분류** `[웹]` |

**stdio의 핵심 규율 `[웹]`:** `2025-11-25` minor change — "servers using **stdio transport may use stderr for all types of logging**". 즉 **stdout은 프로토콜 전용**이다 → §5-1의 최대 함정.

**stdio의 구조적 약점 `[커뮤]`** (전부 1차 근거로 뒷받침됨):
- stdout 오염에 취약
- **OTel trace context 전파 불가** — 헤더가 없어 파라미터·환경변수로 수동 전달해야 함
- 프로세스 생명주기 관리가 클라이언트 몫 → 누수·좀비 (claude-code #74329)
- 자동 재연결 동작이 **문서와 실제가 불일치** (같은 이슈)

### 1-4. 버전 협상 — 실무에서 가장 많이 헷갈리는 지점

`[검증]` TS SDK 1.29.0 `dist/esm/types.js` 실측:
```js
LATEST_PROTOCOL_VERSION = '2025-11-25'
DEFAULT_NEGOTIATED_PROTOCOL_VERSION = '2025-03-26'
SUPPORTED_PROTOCOL_VERSIONS = ['2025-11-25','2025-06-18','2025-03-26','2024-11-05','2024-10-07']
```

> **주목 `[웹]`:** 협상 실패 시 fallback이 최신이 아니라 `2025-03-26`이다 (Python SDK 1.28.1도 동일). **"왜 내 서버가 구버전으로 붙지?"**의 답.

Python SDK 2.0의 `mcp_types/version.py`가 세대 구분을 코드로 못 박았다 `[웹]`:
```python
KNOWN_PROTOCOL_VERSIONS = ("2024-11-05","2025-03-26","2025-06-18","2025-11-25","2026-07-28")
HANDSHAKE_PROTOCOL_VERSIONS = ("2024-11-05","2025-03-26","2025-06-18","2025-11-25")  # initialize로 도달 가능
MODERN_PROTOCOL_VERSIONS = ("2026-07-28",)  # stateless per-request envelope
```

**책에 그대로 쓸 설계 논평 (docstring 원문) `[웹]`:**
> "Date-string protocol revisions happen to sort lexicographically, but versions are an **enumerated set, not an ordered scalar**: future identifiers are not guaranteed to be date-shaped, and unrecognized peer strings must compare conservatively instead of accidentally (e.g. `"zzz" > "2025-11-25"`)."

→ **"버전 문자열을 부등호로 비교하지 마라"**의 1차 출처.

---

## 2. 핵심 관점들

### 2-1. 리비전 계보 (2024-10-07 → 2026-07-28 RC)

`[검증]` GitHub Releases 태그 전수 + `schema/` 디렉토리 열거:

| 리비전 | 게시일 | 상태 | 핵심 |
|---|---|---|---|
| `2024-10-07` | 2024-11-06 | stable | 최초 공개 태그 |
| `2024-11-05` | 2025-01-17 | stable | 최초 정식 리비전 |
| `2025-03-26` | 2025-03-26 | stable | **Streamable HTTP 도입**, HTTP+SSE deprecated 시작 |
| `2025-06-18` | 2025-06-18 | stable | elicitation 등 |
| **`2025-11-25`** | 2025-11-25 | **stable ← 현 정식** | tasks(실험), URL elicitation, icons, sampling 도구호출 |
| `2026-07-28` | RC 2026-05-29 | **prerelease** | **stateless 재설계** |

`schema/`에는 `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25`, `draft` 5개만 존재 — **`schema/2026-07-28/`는 아직 없다** `[검증][웹]`. 확인된 부정적 발견이다.

### 2-2. `2025-11-25`가 가져온 것 (현 정식 — 책의 주 서술 대상)

공식 changelog 원문 `[웹]`:
> 1. OpenID Connect Discovery 1.0 지원으로 authorization server discovery 강화 (PR #797)
> 2. tools/resources/templates/prompts에 **icons** 메타데이터 (SEP-973)
> 3. `WWW-Authenticate` 기반 **incremental scope consent** (SEP-835)
> 5. `ElicitResult`·`EnumSchema` 표준 기반 개편 — titled/untitled, single/multi-select (SEP-1330)
> 6. **URL mode elicitation** (SEP-1036)
> 7. **sampling에 도구 호출 지원** — `tools`·`toolChoice` (SEP-1577)
> 8. **OAuth Client ID Metadata Documents**를 권장 등록 메커니즘으로 (SEP-991)
> 9. **tasks 실험적 지원** — 폴링·지연 결과 회수 (SEP-1686)

저술에 쓸 minor changes `[웹]`:
> - stdio 서버는 **stderr를 모든 로깅에** 사용 가능 (PR #670)
> - **입력 검증 오류는 Protocol Error가 아니라 Tool Execution Error로** — 모델의 자기교정 가능하게 (SEP-1303)
> - **JSON Schema 2020-12를 기본 dialect로** (SEP-1613)
> - 잘못된 Origin 헤더에 **HTTP 403** (PR #1439)
> - **SDK 티어링 시스템** 확립 (SEP-1730)

`[검증]` 스키마 diff 교차 확인 신규 export: `Task`/`TaskStatus`/`CreateTaskResult`/`GetTaskRequest`/`ListTasksRequest`/`CancelTaskRequest`/`TaskStatusNotification`, `ElicitRequestURLParams`/`FormParams`, `Icon`/`Icons`, `ToolChoice`/`ToolUseContent`/`ToolResultContent`, `EnumSchema` 계열.

### 2-3. `2026-07-28` RC — MCP를 stateless로 만드는 재설계

**책의 별도 장을 통째로 쓸 만한 사건이다.** 공식 draft changelog 원문 `[검증][웹]`:

**Major changes:**
1. **프로토콜 레벨 세션 제거** — `Mcp-Session-Id` 헤더 삭제. list 엔드포인트가 연결별로 달라지지 않는다. 교차 호출 상태는 서버가 발급한 핸들을 **일반 도구 인자**로 전달 (SEP-2567)
2. **MCP를 무상태로** — **`initialize`/`notifications/initialized` 제거.** 모든 요청이 `_meta`에 프로토콜 버전·capability를 싣는다 (`io.modelcontextprotocol/protocolVersion`, `/clientCapabilities`, `/clientInfo`, 결과엔 `/serverInfo`). 불일치 시 `UnsupportedProtocolVersionError` (SEP-2575)
3. **`server/discover` 추가** — 서버는 **MUST** 구현, 클라이언트는 MAY 호출 (SEP-2575)
4. **`subscriptions/listen`** — HTTP GET + `resources/subscribe`/`unsubscribe`를 대체하는 단일 장수명 POST-응답 스트림. 옵트인 4종, `io.modelcontextprotocol/subscriptionId` 태깅. **`notifications/progress`·`message`는 여전히 해당 요청의 응답 스트림으로** (SEP-2575)
5. **`ping`, `logging/setLevel`, `notifications/roots/list_changed` 제거.** 로그 레벨은 요청별 `_meta`의 `io.modelcontextprotocol/logLevel` (SEP-2575)
6. **tasks를 코어 밖 공식 확장으로 이관** (`io.modelcontextprotocol/tasks`). 블로킹 `tasks/result` → **`tasks/get` 폴링**, **`tasks/update`** 신설, **`tasks/list` 제거** (SEP-2663)
7. **MRTR(Multi Round-Trip Requests)** — 서버 개시 요청을 대체. 서버가 `InputRequiredResult`(`resultType:"input_required"`)로 요구하면 클라이언트가 **원 요청을 재시도하며** `inputResponses`로 답한다 (SEP-2322)
8. **모든 결과에 `resultType` 필수.** 구버전 서버가 생략하면 **MUST** `"complete"`로 취급 (SEP-2322)
9. **SSE 재개·재전달 제거** — `Last-Event-ID`·이벤트 ID 삭제. 끊기면 **새 request ID로 재발행 MUST** (SEP-2575)

**⚠️ Deprecated — "무엇을 배우지 말아야 하는가" 재료 `[검증][웹]`:**
> **Roots·Sampling·Logging 기능 자체가 deprecated** (SEP-2577). 공식 권장 대체: Roots → 도구 파라미터/리소스 URI/서버 설정; **Sampling → LLM 공급자 API 직접 연동**; **Logging → stderr(stdio) 또는 OpenTelemetry**.

또한 HTTP+SSE Deprecated 재분류(SEP-2596), `includeContext`의 `"thisServer"`·`"allServers"` Deprecated, **OAuth 2.0 DCR(RFC7591) deprecated → Client ID Metadata Documents** (PR #2858).

**minor 중 중요 `[검증][웹]`:**
- `ClientCapabilities`/`ServerCapabilities`에 **`extensions` 필드**
- **OpenTelemetry 트레이스 컨텍스트 규약 문서화** — `_meta`의 `traceparent`·`tracestate`·`baggage` (SEP-414)
- `tools/list` **결정적 순서** SHOULD (클라이언트 캐싱·프롬프트 캐시 적중률)
- Streamable HTTP POST에 **`Mcp-Method`·`Mcp-Name` 헤더 필수**, `x-mcp-header` (SEP-2243)
- **`CacheableResult`** — list/read 계열에 **`ttlMs`·`cacheScope`(`"public"`|`"private"`) 필수** (SEP-2549)
- resource not found **`-32002` → `-32602`**
- `inputSchema`/`outputSchema`에 **JSON Schema 2020-12 전면 허용** (SEP-2106)
- **에러코드 할당 정책**: `-32000~-32019` 구현 정의(grandfathered), **`-32020~-32099` 스펙 예약**. HeaderMismatch `-32020`, MissingRequiredClientCapability `-32021`, UnsupportedProtocolVersion `-32022`

**거버넌스 — "왜 이렇게 자주 바뀌나"에 답할 재료 `[웹]`:**
> feature lifecycle 정책 — Active/Deprecated/Removed 3상태, **최소 12개월 deprecation 창**, deprecated 기능 레지스트리 (SEP-2596)

### 2-4. SDK 2.0의 설계 관점 — "다리(bridge)로서의 SDK"

`[검증]` TS SDK 2.0 베타 export를 직접 뜯어보면 의도가 드러난다. **구·신 타입을 동시에 export**한다: `InitializeRequest` **와** `DiscoverRequest`, `SubscribeRequest` **와** `SubscriptionsListenRequest`, `Task` 계열 **와** `InputRequest`/`InputRequiredResult`. 여기에 명시적 세대 분기 유틸이 붙는다 — `ProtocolEra`, `isLegacyRequest`, `classifyInboundRequest`, `legacyStatelessFallback`, `InboundLegacyRoute`/`InboundModernRoute`.

→ **SDK 2.0은 두 세대를 한 코드베이스로 잇는 다리로 설계됐다.** Python SDK 2.0도 같은 방향 — `mcp_types`에 `v2025_11_25/`·`v2026_07_28/` 버전별 wire 타입 서브패키지가 있다 `[검증][웹]`.

> ⚠️ **단, "설계됐다"와 "지금 동작한다"는 다르다 `[검증]`.** Python은 `MODERN_PROTOCOL_VERSIONS = ("2026-07-28",)`로 신 세대를 **실제로 협상**한다. TS beta.5는 신형 타입과 세대 분기 유틸을 **export하지만 `SUPPORTED_PROTOCOL_VERSIONS`에 `2026-07-28`이 없어 아직 협상하지 않는다**(→ 최상단 표). 다리의 **설계도는 양쪽 다 있지만, 차가 건너고 있는 건 Python 쪽뿐**이다. 책에서 이 둘을 같은 문장으로 묶지 마라.

### 2-5. 학계의 관점 — "MCP는 스택의 첫 단계다"

`[논문]` B-1(arXiv 2504.16736)의 **2차원 분류**: (1) context-oriented vs inter-agent, (2) general-purpose vs domain-specific. **MCP는 "context-oriented × general-purpose" 사분면**에 놓인다 — A2A 같은 inter-agent 프로토콜과 **경쟁이 아니라 다른 축**이다.

`[논문]` B-2가 제안한 **단계적 도입 로드맵**: **MCP(도구 접근) → ACP(구조화·멀티모달 메시징) → A2A(협업적 작업 실행) → ANP(탈중앙 마켓플레이스)**. MCP가 이 스택의 **첫 단계**로 자리매김된다.

→ **"MCP냐 A2A냐"는 잘못된 질문이다** `[논문]`. 대개 둘 다 필요하다.

---

## 3. 대표 사례

### 3-1. TypeScript — 1.x와 2.x가 **완전히 다른 패키지**다

**v1 (프로덕션 권장) `[검증]`**

| 항목 | 값 |
|---|---|
| 패키지 | `@modelcontextprotocol/sdk` |
| 현재 버전 | **`1.29.0`** (dist-tags에 2.x 없음) |
| 릴리스 | **2026-03-30** (npm publish 타임스탬프) |
| 지원 스펙 | `LATEST = 2025-11-25` |

**v2 (beta) — 모노레포가 패키지를 쪼갰다 `[검증][웹]`.** 전부 `2.0.0-beta.5` (2026-07-21):

| 패키지 | 역할 |
|---|---|
| `@modelcontextprotocol/server` / `client` | 서버 / 클라이언트 구축 |
| `@modelcontextprotocol/core` | public Zod schemas (spec + OAuth/OpenID) |
| `@modelcontextprotocol/node` | Node.js Streamable HTTP 트랜스포트 래퍼 |
| `@modelcontextprotocol/express` / `hono` / `fastify` | 프레임워크 어댑터 |
| `@modelcontextprotocol/server-legacy` | Frozen v1 SSE + OAuth AS 헬퍼 — **Deprecated** |
| `@modelcontextprotocol/codemod` | **v1 → v2 마이그레이션 codemod** |

**공식 README 원문 `[웹]`:**
> "**This is the `main` branch — v2 of the SDK, now in beta**, implementing the 2026-07-28 MCP spec."
> "We expect a **stable release alongside the full release of the 2026-07-28 spec on July 28, 2026**. Until then, **v1.x remains the supported release for production**; it keeps receiving bug fixes and security updates for **at least 6 months after v2 ships**."

**v2 패키지 실측 `[검증]`:**
- `type: "module"`, dual ESM/CJS, `engines.node: ">=20"`
- deps: **`zod: ^4.2.0`** (v1의 Zod 3 → **Zod 4 메이저 점프**), `@modelcontextprotocol/core`
- 서브패스 exports: `.`, `./stdio`, `./validators/ajv`, `./validators/cf-worker`
- `./stdio`: `StdioServerTransport`, **`serveStdio`**(신규 간편 진입점)
- 신규 트랜스포트: **`WebStandardStreamableHTTPServerTransport`**(Cloudflare Workers 등), `PerRequestHTTPServerTransport`, `createMcpHandler`
- **OAuth 리소스 서버**: `requireBearerAuth`, `verifyBearerToken`, `buildOAuthProtectedResourceMetadata`
- **보안(DNS rebinding 방어)**: `validateHostHeader`, `validateOriginHeader`, `localhostAllowedHostnames/Origins`
- **관찰성**: `TRACEPARENT_META_KEY`, `TRACESTATE_META_KEY`, `BAGGAGE_META_KEY`
- 서버 API 존치: `McpServer`, `Server`, `registerTool`/`registerPrompt`/`registerResource`, `ResourceTemplate`, `completable`

**스키마 라이브러리 정책 변화 `[웹]`:**
> "Tool and prompt schemas use **Standard Schema** — bring **Zod v4, Valibot, ArkType, or any compatible library**."

(`StandardSchemaV1` export로 교차 확인 `[검증]`.)

**어댑터 설계 철학 `[웹]`:** "They are intentionally **thin adapters**: they should not introduce new MCP functionality or business logic."

### 3-2. Python — `mcp`, 그리고 2.0의 **FastMCP 소멸**

| 항목 | 값 |
|---|---|
| 현재 안정 | **`1.28.1`** (2026-06-26) `[검증]` |
| 지원 스펙 | `LATEST = 2025-11-25`, `DEFAULT_NEGOTIATED = 2025-03-26` |
| requires_python | `>=3.10` |
| 2.0 프리릴리스 | a1(06-11) → a2(06-16) → a3(06-26) → b1(06-30) → **b2(2026-07-14)** `[검증]` |

**v1.28.1의 FastMCP API `[웹]`:**
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Demo", json_response=True)

@mcp.tool()
def ...
@mcp.resource("greeting://{name}")
def ...
@mcp.prompt()
def ...

mcp.run(transport="streamable-http")
```
설치: `uv add "mcp[cli]"` 또는 `pip install "mcp[cli]"` — `[cli]` extra가 `mcp` CLI를 설치.

> **⚠️ 최대 파괴적 변경 `[검증]` — `FastMCP`가 2.0에서 완전히 사라졌다.**
> `mcp 2.0.0b2` wheel 전체에 "fastmcp" 문자열이 **0건**(`grep -ril fastmcp` → 결과 없음). 대체는 `mcp/server/mcpserver/server.py`의 **`MCPServer`**.
> 같은 디렉토리 정의 클래스: `MCPServer`, `Context`, `Settings`, `Elicit`, `Sample`, `ListRoots`, `Resolve`, `MCPServerError`, `ToolError`, `ResourceError`, `InvalidSignature` — `Elicit`/`Sample`/`ListRoots`/`Resolve`는 핸들러 시그니처 주입(DI)형으로 보인다.
> → **Python 1.x의 `@mcp.tool()` 코드는 2.0에서 그대로 동작하지 않는다.** 1.28.1과 2.0.0b2를 반드시 분리 서술.

**2.0 구조 변경 `[검증][웹]`:** 타입이 별도 패키지 **`mcp-types`**로 분리(`from mcp_types import ...`), 내부에 `v2025_11_25/`·`v2026_07_28/` 서브패키지. 신규 모듈 `_otel.py`, `caching.py`, `_streamable_http_modern.py`, `request_state.py`, `extension.py`. **`opentelemetry-api>=1.28.0`이 하드 의존성으로 승격** — 관찰성이 기본이 됐다. 그 외 `httpx2>=2.5.0`, `pydantic>=2.12.0`.

**공식 README 경고 — 실무자 필독 `[웹]`:**
> "**If your package depends on `mcp`, add a `<2` upper bound to your version constraint (for example `mcp>=1.27,<2`) before the stable v2 release lands.**"

> **혼동 주의 `[검증]`:** PyPI의 별도 패키지 **`fastmcp`(jlowin)는 현재 3.4.4**로 독자 노선이다. 공식 `mcp`에 통합됐던 FastMCP와 이름만 같다.

### 3-3. Java — 공식 Java SDK 2.0.0 (GA)

| 항목 | 값 `[검증][웹]` |
|---|---|
| 현재 버전 | **`2.0.0` GA** (2026-06-11) |
| 좌표 | `io.modelcontextprotocol.sdk:mcp` |
| 지원 스펙 | **`2025-11-25`** (릴리스 노트 명시) |
| 경로 | M1 → M2(05-13) → M3(05-21) → RC1(06-04) → **2.0.0(06-11)** |
| 병행 유지 | `1.1.3`(2026-05-21), `0.18.3`(2026-06-09) |

**릴리스 노트 원문 `[웹]`:**
> "**General Availability of the MCP Java SDK 2.0.0** — the first major release since 1.x... It **tracks the latest 2025-11-25 MCP specification**."

Highlights: JSON 호환성 기반, spec-accurate schema + lenient wire deserialization, 도구 입력·JSON Schema 2020-12 종단 검증, richer elicitation(URL·form), Icons(SEP-973), **"Streamable HTTP first: SSE transports are now deprecated"**.
Breaking: `McpSchema` 필수 필드 강제(#928), 도구 입력 검증(#873), `JsonSchema` 제거 후 `inputSchema`를 `Map`으로(#749). 마이그레이션: `MIGRATION-2.0.md`.

### 3-4. Spring AI — MCP 스타터 2.0.0 (GA)

`[검증]` Maven Central `maven-metadata.xml` + 2.0.0 경로 HTTP 200 전수 확인. **아티팩트 이름은 2.0.0에서도 그대로다**:

`org.springframework.ai` 하위 MCP 관련 starter는 **5개가 전부** `[검증]` — **서버 3개**(`spring-ai-starter-mcp-server`, `-server-webmvc`, `-server-webflux`) **+ 클라이언트 2개**(`-client`, `-client-webflux`). `spring-ai-bom`도 `2.0.0`.
(아래 매트릭스는 이 중 **서버 3개**만 다룬다 — 행이 7개인 건 아티팩트가 7개라서가 아니라 **프로토콜을 프로퍼티로 고르기 때문**이다.)

> **⚠️ 중요 정정 `[웹]` — 서버 아티팩트는 3개인데 프로토콜은 프로퍼티로 고른다.**
> Spring AI 레퍼런스 asciidoc 원문에서 직접 확인한 매트릭스:

| 서버 유형 | artifactId | 활성화 프로퍼티 |
|---|---|---|
| STDIO | `spring-ai-starter-mcp-server` | `spring.ai.mcp.server.stdio=true` |
| SSE WebMVC *(deprecated since 2.0.0)* | `-server-webmvc` | `spring.ai.mcp.server.protocol=SSE` |
| **Streamable-HTTP WebMVC** | `-server-webmvc` | `protocol=STREAMABLE` |
| **Stateless WebMVC** | `-server-webmvc` | `protocol=STATELESS` |
| SSE WebFlux *(deprecated since 2.0.0)* | `-server-webflux` | `protocol=SSE` |
| **Streamable-HTTP WebFlux** | `-server-webflux` | `protocol=STREAMABLE` |
| **Stateless WebFlux** | `-server-webflux` | `protocol=STATELESS` |

> **"WebMVC용 Streamable 스타터"를 따로 찾으면 안 된다** — 아티팩트 하나가 SSE·STREAMABLE·STATELESS 셋을 다 커버한다 `[웹]`.
> `(deprecated since 2.0.0, use STREAMABLE instead)`는 **adoc 원문 그대로**이며, java-sdk 2.0.0 릴리스 노트의 "SSE deprecated"와 독립 교차 확인됐다.
> STATELESS는 adoc 원문상 *"ideal for **microservices architectures and cloud-native deployments**"*.

> **⚠️ 두 번째 중요 정정 `[웹]` — `@Tool`/`ToolCallbackProvider`가 아니라 `@McpTool` 체계다.**

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
adoc 원문: "The `@McpTool` annotation marks a method as an MCP tool implementation with **automatic JSON schema generation**."
속성: `name`(기본=메서드명), `description`, `title`(우선순위 `annotations.title` > `title` > `name`), `generateOutputSchema`(기본 `false`), `annotations`, `metaProvider`. 그 외 `@McpResource` 등이 있다 `[웹]`.

**타이밍 `[웹]`:** Spring AI 2.0.0(06-12)이 Java SDK 2.0.0(06-11) **바로 다음 날** 나왔다.

### 3-5. 기타 언어

`modelcontextprotocol` org 하위에 Kotlin/C#/Go/Rust SDK가 존재하나 이번 리서치에서 버전을 열거하지 못했다 `[웹]` → §7.
`2025-11-25`의 **SDK 티어링(SEP-1730)** — 언어 선택 시 공식 지원 등급을 확인하라는 조언의 근거 `[웹]`.

`[논문]` C-2(arXiv 2607.10123, 검증된 MCP 프로젝트 2,297개): **Python과 TypeScript가 MCP 개발을 지배**하며 하이브리드 아키텍처가 가장 흔한 설계 패턴.
> ⚠️ **이 데이터셋은 Java의 위상에 대해 아무 근거도 제공하지 않는다** `[논문]`. Java 관련 주장을 이 논문으로 뒷받침하지 마라.

### 3-6. 클라이언트 연결

#### Claude Code `[검증]` (로컬 `claude --version` = **2.1.220**)

서브커맨드 전수: `add`, `add-from-claude-desktop`, `add-json`, `get`, `list`, `login`, `logout`, `remove`, `reset-project-choices`, **`serve`**.

`claude mcp add` 옵션 실측 `[검증]`:
- **`-s, --scope <scope>`** — `local` | `user` | `project` (**기본값 `local`**)
- **`-t, --transport <transport>`** — `stdio` | `sse` | `http` (미지정 시 stdio)
- `-e, --env <env...>`, `-H, --header <header...>`
- OAuth: `--client-id`, `--client-secret`(또는 `MCP_CLIENT_SECRET`), `--callback-port`

공식 help 예시 원문 `[검증]`:
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp add --transport http corridor https://app.corridor.dev/api/mcp --header "Authorization: Bearer ..."
claude mcp add my-server -e API_KEY=xxx -- npx my-mcp-server
claude mcp add my-server -- my-command --some-flag arg1
```

공식 문서 추가 사실 `[웹]`:
- **`--`의 의미:** "Everything after `--` is passed to the server untouched."
- **`type` 별칭:** "`type` field accepts **`streamable-http` as an alias for `http`**"
- **타임아웃:** `.mcp.json`에 `"timeout": 600000`(ms). HTTP/SSE는 **첫 응답 바이트까지 60초** 별도 타이머
- **재연결:** HTTP/SSE는 지수 백오프 **최대 5회, 1초에서 2배씩**. **stdio는 자동 재연결 안 함**
- **예약어:** `workspace`, `claude-in-chrome`, `computer-use`, `Claude Preview`, `Claude Browser`
- **WebSocket vs HTTP:** "HTTP supports OAuth and the `claude mcp add --transport` flag, while WebSocket supports neither"
- 스캐폴딩: 공식 `mcp-server-dev` 플러그인, `/mcp-server-dev:build-mcp-server`

**스코프의 실제 의미 `[커뮤]`** (공식 quickstart 원문):
> "Local-scoped servers are tied to the project where you added them: the repository root, or the exact directory if you weren't in a git repository."

> ⚠️ **스코프 우선순위(`local > project > user`)는 다수 2차 블로그가 일치하나 1차 문서로 확인되지 않았다 `[커뮤]`. 책에서 단정하지 마라** → §7.

#### Claude Agent SDK `[검증]` (TS **0.3.220**, PyPI **0.2.128**)

`sdk.d.ts` 실측:
- `mcpServers?: Record<string, McpServerConfig>`
- `McpServerConfig = McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfigWithInstance` — **외부 프로세스 3종 + 인프로세스 1종**
- **`createSdkMcpServer(options)`** — 별도 프로세스 없이 **같은 프로세스 안에서** MCP 서버 정의
- **`tool<Schema extends AnyZodRawShape>(name, description, inputSchema, handler, extras?)`**

Python 대응 `[커뮤]`: `create_sdk_mcp_server(...)` + `@tool` 데코레이터. Go·Rust·Elixir·Perl 서드파티 포팅 존재.

> Agent SDK는 0.x이고 릴리스가 며칠 간격이다(PyPI 0.2.125→0.2.128이 07-21~07-25). 시그니처를 단정할 땐 **"0.3.x / 2026-07 기준"** 명기 필수 `[검증]`.

#### 기타 클라이언트 — Codex CLI `[검증]` (`codex-cli` **0.145.0**)
- **`codex mcp`** — `list`/`get`/`add`/`remove`/`login`/`logout`
- 설정: **`~/.codex/config.toml`** (TOML — Claude Code의 JSON과 대조)

### 3-7. 서버가 역으로 코딩 에이전트를 호출하는 패턴 (토픽 6)

**먼저 두 패턴을 분리해야 한다 `[커뮤]`:**
- **패턴 A — 에이전트를 MCP 서버로 *노출*** (Claude Code 자체를 서버로 띄움)
- **패턴 B — MCP 서버가 에이전트를 *호출*(오케스트레이션)** ← 본 토픽의 주제

`[검증]` 두 CLI의 표면이 **양방향**임을 직접 확인했다:

| 방향 | Claude Code | Codex CLI |
|---|---|---|
| 에이전트가 MCP 서버를 **소비** | `claude mcp add` | `codex mcp add` |
| 에이전트가 **MCP 서버가 됨** (패턴 A) | **`claude mcp serve`** | **`codex mcp-server`** |
| **헤드리스 호출** (패턴 B) | `claude -p` | **`codex exec`** |

> **🚨 가장 중요한 발견 — 이 패턴은 정착된 실무 관행이 아니다 `[커뮤]`.**
> `gh repo view`로 확인한 실제 구현체는 **3개뿐**이고:
> - `steipete/claude-code-mcp` (**1,313⭐**) — **🔴 아카이브됨** (2026-05-15 마지막 푸시)
> - `grahama1970/claude-code-mcp-enhanced` (125⭐) — **14개월 방치** (2025-05-20)
> - `SinanTufekci/agent-intern` (16⭐) — ✅ 활발 (2026-07-24)
>
> 대표 리포가 아카이브되고 2위가 방치된 반면 활발한 건 16⭐ 신생 프로젝트다. **여러 검색 쿼리가 모두 빈 결과를 냈다** `[커뮤]`.
> → **책의 태도:** "떠오르는 베스트 프랙티스"로 소개하면 안 된다. **"실험적이고, 대표 구현이 유지보수를 멈춘 영역"**으로 정직하게 프레이밍해야 한다.

**문서화된 함정 `[커뮤]`** (README·이슈 1차 인용):

1. **샌드박스가 상속되지 않는다.** `steipete/claude-code-mcp` README: *"This wrapper is **not an OS-level sandbox**"* / *"cannot approve prompts that belong to a parent MCP client... or make another Claude Code session inherit its settings."* 진입 조건 자체가 `--dangerously-skip-permissions`를 요구한다.
   `agent-intern` README `[!WARNING]`: *"**This runs unsandboxed code with your privileges.** `agy -p` auto-executes its tools... with **no usable approval gate**"* / *"`codex exec` also runs autonomously, but its `sandbox` flag (default `read-only`) **is** a real, enforced boundary."* / *"in all four cases the `workspace` argument is a *starting context*, **not a security boundary**."*
2. **시간 스케일이 다르다.** `CLAUDE_CLI_TIMEOUT_SECONDS` 기본 **3600초(1시간)** — 일반 MCP 도구 타임아웃(60초~5분)과 **두 자릿수 배 차이**.
3. **에이전트마다 답을 돌려주는 방식이 다르다** — 서버가 **에이전트의 출력 규약에 인질로 잡힌다**:

| CLI | 답을 읽는 방법 |
|---|---|
| `agy -p` (Antigravity) | 1.0.15+(Windows)는 stdout; 아니면 `transcript.jsonl` **스크래핑** |
| `codex exec` | `-o/--output-last-message`로 **파일에 씀** |
| `copilot -p` | stdout (`-s`) |
| `cursor-agent -p` | stdout (`--output-format text`) |
4. **병렬 실행 시 `HOME` 상태 경합** — agy는 *"Runs with an isolated `HOME` to avoid state races"*.
5. **헤드리스에서 MCP 실패가 무신호** (claude-code #43968, 2026-04-05): *"There is **zero signal** in stderr or the `stream-json` output... Orchestrators have no way to detect the failure except by counting tools."* 실제 로그 대비 — 1차 요청 `tools: 70`, `--resume` 후 `tools: 22, mcp_servers: []`.
6. **살아 있는 척하는 실패** (#80996, 2026-07-24): *"our agents' **only inbound-message path is an MCP server**, so a session that resumes with the MCP down is **functionally deaf while looking alive from the outside**."* `/mcp`가 **대화형 전용**이라 자동 복구 경로가 없다. 우회책의 대가는 *"~15 min penalty per event"*.
7. **함대가 커지면 헤드리스 호출이 행** (#68375, 2026-06-14, 2.1.177 리그레션): 전체 11개 서버 → 행(>68초); `--strict-mcp-config`로 1개만 → **~5초**. *"A nightly headless job... ran fine through 2026-06-12; the first run after the 2.1.177 auto-update hung."*

> **반직관적 발견 `[커뮤]`:** **비용 폭발·무한 재귀 사고 보고는 하나도 없다.** 오히려 이 패턴의 명시적 동기가 **비용 절감(쿼터 차익거래)**이다 — *"Burn Antigravity / Codex quota on grunt work instead of Claude tokens."* 먼저 보고되는 문제는 비용이 아니라 **권한과 상태**다.

### 3-8. 배포

#### npm → `npx` (가장 중요한 경로)

공식 quickstart 예제의 **실물 `package.json`** `[웹]`:
```json
{
  "name": "mcp-quickstart-ts",
  "version": "1.0.0",
  "type": "module",
  "bin": { "weather": "./build/index.js" },
  "scripts": {
    "build": "tsc && node -e \"require('fs').chmodSync('build/index.js', '755')\""
  },
  "files": ["build"],
  "dependencies": { "@modelcontextprotocol/sdk": "^1.24.3" }
}
```

책에서 짚을 4가지 `[웹]`:
1. **`"type": "module"`** — ESM 전제
2. **`"bin"`** — `npx`가 실행하게 만드는 핵심 필드. **키가 곧 커맨드 이름**
3. **`"files": ["build"]`** — tarball에 빌드 산출물만
4. **`prepublishOnly`가 없고, build 스크립트가 직접 `chmod 755`** — 실행 권한이 없으면 `npx`가 실패한다. **Windows에서도 되도록 `chmod` 대신 Node 인라인 스크립트**를 쓴 게 실무 팁

> **⚠️ 정정 `[웹]`: 이 공식 예제의 `bin` 타깃에는 shebang이 없다.** `src/index.ts` 첫 줄이 `import`다. 통념(`#!/usr/bin/env node` 필수)과 어긋나므로 **베끼기 전에 실제로 `npx` 실행을 검증해야 한다.**

배포 절차 `[웹]`:
```bash
npm install && npm run build
npm adduser
npm publish --access public
```
스코프 패키지(`@user/...`)는 기본이 private이므로 **`--access public`이 없으면 배포가 실패한다** `[웹]`.

#### MCP Registry

`[검증]` 실제 API 호출 (2026-07-26): `GET https://registry.modelcontextprotocol.io/v0/servers?limit=2` → **HTTP 200, 정상 가동**.
- 엔트리 구조: `server{ $schema, name(역DNS형 예 `ac.inference.sh/mcp`), description, title, version, remotes[{type:"streamable-http", url}] }` + `_meta["io.modelcontextprotocol.registry/official"]{ status, publishedAt, updatedAt, isLatest }`
- 커서 페이지네이션: `metadata{ nextCursor, count }`
- **`server.json` 스키마 = `2025-12-11`** ← 네 번째 독립 날짜 축
- 레지스트리 소프트웨어: **v1.8.0 (2026-07-13)** `[검증][웹]`

**상태 판정 `[웹]`:** 공식 quickstart — "**The MCP Registry is currently in preview.** Breaking changes or data resets may occur before general availability." → **가동 중이지만 GA는 아니다.**

**성격 `[웹]`:** "like an app store for MCP servers" / "**The MCP Registry only hosts metadata, not artifacts**, so we must publish the package to npm before publishing the server to the MCP Registry."

**등록 절차 `[웹]`:** `package.json`에 **`mcpName`** 추가(GitHub 인증 시 `io.github.my-username/`로 시작 **必**) → `mcp-publisher` CLI(`brew install mcp-publisher`) → 게시. 지원 타입: **npm, PyPI, NuGet, OCI, MCPB**.

#### 원격(Streamable HTTP) 배포
- **세션:** `2025-11-25`까지 `Mcp-Session-Id` 기반. **`2026-07-28` RC에서 제거** → "server-minted handles passed as ordinary tool arguments" `[웹]`
- **보안:** 잘못된 Origin에 **HTTP 403** `[웹]`. SDK 2.0은 `validateHostHeader`/`validateOriginHeader` 제공 `[검증]`
- **OAuth 진화:** `2025-11-25` OIDC Discovery + incremental scope consent + Client ID Metadata Documents → `2026-07-28` RC에서 **DCR deprecated**, `iss` 검증(RFC 9207) 요구 `[웹]`
- **캐싱/중계:** `cacheScope: "public"|"private"`가 공유 중계자 캐싱 여부를 제어 `[웹]`

---

## 4. 논쟁점·상충 관점

### 4-1. MCP가 필요한가, CLI면 충분한가 (가장 큰 논쟁)

**논쟁의 규모 `[커뮤]`** (HN Algolia API로 점수·댓글수 직접 확인):

| 스레드 | 점수/댓글 | 날짜 |
|---|---|---|
| "I still prefer MCP over skills" | **460/375** | 2026-04-10 |
| "When does MCP make sense vs CLI?" (원제 "MCP is dead, long live the CLI") | **447/284** | 2026-03-01 |
| "MCP is dead?" | **400/410** | 2026-05-29 |
| "Making MCP cheaper via CLI" | 324/119 | 2026-02-25 |
| "MCP is dead; long live MCP" | 295/205 | 2026-03-14 |

> **패턴 `[커뮤]`:** 2026년 2~5월에 **4개월 연속** "MCP는 죽었다"류 대형 스레드가 올라왔다. 단발성 백래시가 아니라 **지속적 논쟁**이고, **매번 방어 측이 400+ 댓글로 반론**했다.

**🅰️ 관점 A — "그냥 CLI를 써라" `[커뮤]`**
- **edgyquant**: *"We had curl, HTTP and OpenAPI specs, but we created MCP. Now we're wrapping MCP into CLIs..."* (순환 논리 조롱)
- **lukol**: *"Simple REST APIs often do the job as well. **MCP felt like a vibe-coded fever dream from the start.**"*
- **jauntywundrkind**: *"**With CLI tools, it all composes**"* — MCP는 모든 조합이 LLM을 거쳐야 한다
- **bb88**: *"I was writing MCP servers, now I just write tools for agents to consume. **It's often easier.**"* (전향 사례)
- **eddythompson80**: *"every MCP that could have been a CLI call is **a new opportunity for sandbox escape**"*
- 🇰🇷 **jamsya** (GeekNews): *"**AWS MCP 안 깔아도 클로드 코드가 알아서 AWS CLI로 필요한 거 가져다 쓰더라구요**"* — 한국 실무자의 가장 구체적인 반증
- 🇰🇷 **sonnet**: *"MCP가 이점이 없는 게 아니라 **무차별적으로 사용하던 환상에서 깨어난 거죠**"*
- 🇰🇷 **kaydash**: *"개발할때는 쓸만하고 **서비스할때에는 비용문제 때문에 skill정도만** 쓰고있어요"* — 개발/운영 단계별 분기

**🅱️ 관점 B — "MCP는 CLI가 못 하는 걸 한다" `[커뮤]`**
- **p_ing**: *"**Tell my business users to use CLI when they create their agents. It's just not happening.** MCP is point-and-click for them."*
- **0x696C6961**: *"I have a couple MCP servers connected to my **Claude web & mobile** clients. **How would your clis work there?**"* — CLI가 존재할 수 없는 환경
- **CharlieDigital**: *"How do I guard those keys from both developer and agent? **Put it behind MCP; neither dev nor agent ever sees the key**"*
- **bb88** (관점 A와 같은 인물의 다른 각도): *"**MCP exists to take capability away from agents** ... tightly allowlist what the agent is capable of executing"* — **MCP를 "능력 제한 장치"로 재해석. 논쟁 프레임을 바꾸는 인용.**
- **didibus**: *"MCP is a JSON-RPC + a fixed auth/discovery handshake ... **Having a standard for that is really nice**"* (단, *"**MCPs are impossible to combine [like shell]**"*도 인정). Asana·Square·Linear·Dropbox·Canva·Slack은 **MCP는 제공하지만 동등한 CLI가 없다**
- **eikenberry**: *"if you have **300 employees** ... you want to push an update to the skill, mcp provides you with a standard way"*
- 🇰🇷 **develosopher**: *"[SaaS 개발자라면] MCP를 먼저 선택할 것 같아요. **CLI 지원은 관리 포인트가 늘어나니까요**"* — **제공자(서버 저자) 관점의 반전**

**⚖️ 중재 `[커뮤]`**
- **ejholmes(원저자 본인)**: *"The article title and content is **intentionally provocative**"* — **"MCP는 죽었다" 글의 저자조차 제목이 낚시였다고 인정했다.** 책에 반드시 넣을 것
- **leonidasv**: *"I still prefer hammer over screwdriver"* — 거짓 이분법이라는 일침
- **goodmythical**: 학습 데이터에 없는 새 도구라면 **MCP든 CLI든 토큰 낭비는 똑같다** — 차이는 형식이 아니라 **친숙도**
- **kristopolous**: 벡터 검색으로 관련 MCP만 동적 발견하는 게이트웨이 자작 → 문제를 프로토콜이 아니라 **아키텍처로** 푸는 제3의 길

### 4-2. 컨텍스트 비용은 여전히 문제인가 — 그리고 신선도 함정

**관점 A(문제다) `[커뮤]`:** 0xbadcafebee의 계산 — 도구 50개 = *"150 * 50, or **7500 tokens**, dumped into the beginning of every session"*. claude-code #8288(2025-09-28)의 실측: **79k(40%) → 36k(18%) → 20k(10%)** 토큰 변동, 도구 정의만 약 **59.4k 토큰**.

**관점 B(이미 해결됐다) `[커뮤]`:** deferred tool loading이 도입돼 대부분 해소됐다는 반박(JoshGlazebrook의 "85%+" 주장). 🇰🇷 **newdps**: *"claude 같은 경우 deferred tool로 분류해서 이름만 넣도록 최적화하긴 합니다"*.

**⏱️ 결정적 메타 논점 `[커뮤]`:** **red_hare** — *"**Deferred tool loading was added in Nov 2025** ... so these numbers are at least 7 months out of date."*
→ **"MCP는 컨텍스트를 낭비한다"는 비판의 상당수가 deferred loading 이전 데이터에 기반한다.**
→ **책의 태도:** 컨텍스트 비판을 소개하되 **"어느 시점의, 어느 클라이언트 동작을 전제한 비판인가"를 반드시 함께 표시**해야 한다. **이게 이 책이 다른 MCP 글과 차별화될 지점이다.**
> ⚠️ 단, deferred loading 도입 시점(2025-11?)과 85% 수치는 **1차 검증되지 않았다** `[커뮤]` → §7.

**관점 C(문제는 다른 데 있다) `[커뮤]`:** 🇰🇷 **newdps**는 컨텍스트보다 **디버깅과 상태 관리의 어려움**이 더 크다고 지적. **이 책의 토픽 5가 존재하는 이유를 한국 실무자가 직접 말해준 셈.**

**학술적 중재 `[논문]`:** D-4(arXiv 2605.24660)가 이 논쟁에 숫자로 답한다. 단 **"tool 100개면 정확도 13%" 류의 비보정 수치는 이 논문의 주장이 아니며 학술 출처가 확인되지 않았다 — 책에 쓰지 마라.** 논문의 실제 결과:
- **BFCL(370개 tool)**: 학습 정책이 **평균 7개만 제시하면서 50개 제시 대비 커버리지 90.3% vs 90.8%** (1/7로 줄여도 손실 0.5%p)
- **Claude Sonnet 4.6 downstream**: 짧은 적응형 목록이 **선택 정확도 자체를 개선** — **93.1% vs 87.1%** (항상 5개 제시 대비). 중난도 질의에선 **76.8% vs 60.9%**로 격차 확대
- 단, ToolBench(3,251개)에선 고정 5개가 총 커버리지는 높지만(64.7% vs 61.9%) **어려운 질의에서 아무것도 못 찾는다**

### 4-3. 보안: MCP는 방벽인가 공격면인가

**방벽론 `[커뮤]`:** CharlieDigital(키 격리), bb88(능력 제한), SyneRyder(엔드포인트 노출 차단·파라미터 검증), DieErde(인가 계층).
**공격면론 `[커뮤]`:** eddythompson80 — *"a new opportunity for sandbox escape"*.

**⚖️ 제3의 사실 — 툴체인에서 실제로 터졌다 `[커뮤]`:**
- **CVE-2025-49596** (CVSS **9.4**, 2025-07 공개): MCP Inspector **0.14.1 미만**에서 클라이언트-프록시 간 **인증 부재**. 브라우저 "0.0.0.0 Day" + CSRF 체이닝 시 **악성 웹사이트 방문만으로 개발자 워크스테이션에서 RCE**. → **"로컬 개발 도구니까 안전하다"는 가정이 깨진 사례.**
- `claude mcp list`가 **시크릿을 터미널에 출력** (v2.1.161에서 수정) — 이전 버전에선 출력을 이슈·슬랙에 붙여넣으면 토큰이 샜다
- 커밋된 `.mcp.json` **자기승인 차단** (v2.1.196)
- `headersHelper` **셸 인젝션 수정** (v2.1.207)

**학술적 실측 `[논문]` — "얼마나 위험한가"에 숫자를 붙일 때:**
- **A-2** (arXiv 2506.13538, 오픈소스 서버 **1,899개**): **7.2%**가 일반 취약점, **5.5%**가 **MCP 고유 tool poisoning**. 식별된 취약점 **8종 중 3종만** 전통적 소프트웨어 취약점과 겹친다 → *"기존 SAST를 돌렸다고 MCP 서버가 안전한 게 아니다"*. 유지보수성은 **66%**가 code smell.
- **A-3** (arXiv 2510.16558, ✅ **DSN 2026 게재 확정**, 6개 레지스트리 **67,057개 서버**): **833개 취약 서버** + **18개 의심 description** 식별. 핵심 주장 — *"Code-level vulnerabilities (e.g., code injection) **are not required** but can amplify"* → **소스가 깨끗해도 tool description만으로 공격이 성립한다.**
- **A-4 MCPTox** (arXiv 2508.14925, ✅ **AAAI-26 게재**, DOI 10.1609/aaai.v40i42.40895; 실서버 45개·실tool 353개·악성 케이스 1,312개·에이전트 20종): **o1-mini ASR 72.8%**. 그리고 가장 반직관적인 발견 — > *"We find that **more capable models are often more susceptible**, as the attack exploits their superior instruction-following abilities."* 거부율은 **최고치(Claude-3.7-Sonnet)조차 3% 미만**.
  ⚠️ 72.8%를 "모델 중 최고치"라고 단정하지 마라(초록에 순위 주장 없음). "약한 모델이 뚫린다"로 뒤집으면 **논문을 정반대로 인용**하는 것이다 `[논문]`.
- **A-6 MCPSecBench** (arXiv 2508.13220, 코드 공개): 4개 공격면 × 17종 공격, 3개 주요 플랫폼 **전 공격면에서 침해 성공**. > *"current protection mechanisms proved largely ineffective, achieving an **average success rate of less than 30%**."*
- **A-5** (arXiv 2509.24272): > *"malicious MCP servers are **easy to implement, difficult to detect** with current tools"* — **"스캐너 통과"를 신뢰 근거로 삼지 마라.**

→ **실무 결론 `[논문]`:** 모델의 alignment를 방어선으로 계산에 넣지 마라(거부율 3% 미만). 방어는 모델 **밖**(서버 측 권한 최소화, description 검증, 실행 승인 게이트)에 세워야 한다.

> **미수집 `[커뮤]`:** 프롬프트 인젝션·도구 포이즈닝에 대한 **커뮤니티 1차 토론**은 확보하지 못했다 — 학술(위)과 벤더 블로그만 있다 → §7.

### 4-4. `.mcp.json` 파편화 — "build once, integrate everywhere"의 실제

공식 문서는 "build once and integrate everywhere"를 내세운다 `[웹]`. 그러나 `[검증]` 확인만 봐도 Claude Code는 `.mcp.json`/`~/.claude.json`(JSON)에 3스코프, Codex는 `~/.codex/config.toml`(TOML)을 쓴다. Claude Code가 스펙 명칭 `streamable-http`를 `http`의 별칭으로 받는 것 자체가 **명칭 파편화 흡수 조치**다 `[웹]`.

**파편화의 진짜 비용 `[커뮤]`:** 서드파티 MCP 서버 리포지토리들이 **"Claude Desktop 설정 자동 작성" 기능을 별도 이슈로 관리**하는 패턴이 반복 관측된다(Filmroom#40, apple-mail-fast-mcp#399, mcp-studio#4, mcp-manager#10).
→ **"내 서버를 어떻게 설치시키지"가 서버 개발자의 실제 업무가 됐다.**

**같은 서버, 다른 클라이언트, 다른 결과 `[커뮤]`:**
- claude-code #66262 (2026-06-08): Windows에서 **VS Code 확장은 stdio 서버 스폰 실패, CLI는 정상** (PATH 상속 차이)
- #74768 (2026-07-06): Desktop의 DCR이 `client_name`을 `"Claude Desktop (…)"`로 보내 **Figma MCP 등록이 403 거부** — CLI는 `"Claude Code"`를 보내서 성공
- #77388 (2026-07-14): `.mcpb` 확장의 도구가 Chat엔 안 보이고 Cowork엔 보임 — **양쪽 다 "연결됨" 표시**

### 4-5. 지금 배우면 곧 낡는가 — 학습 타이밍 딜레마

**관점 A (v1으로 배워라):** TS SDK README가 "**v1.x remains the supported release for production**"이라 명시하고, v2 안정판 이후에도 **최소 6개월** 수정을 약속한다 `[웹]`. Java SDK 2.0·Spring AI 2.0은 GA면서 `2025-11-25`를 따른다 `[검증]`.

**관점 B (v2/2026-07-28로 배워라):** TS v2 안정판이 **2026-07-28 스펙 정식과 동시** 예정이고 `[웹]`, 그 스펙은 `initialize`를 없앤다. v1으로 배운 라이프사이클 지식은 수명이 짧다.

**중재 `[검증]`:** RC 릴리스 노트가 직접 답한다 — "**SDKs will adopt this version at their own pace, and the prior version of the spec may remain in use for an undetermined amount of time.**" 그리고 스펙은 **최소 12개월 deprecation 창**을 정책화했다(SEP-2596) `[웹]`.

### 4-6. 스펙이 스스로를 부정하다 — Sampling의 운명

`2025-11-25`는 **sampling에 도구 호출을 추가**했다(SEP-1577) `[웹]`. 불과 한 리비전 뒤 `2026-07-28` RC는 **Sampling 자체를 deprecated**하고 "integrate directly with LLM provider APIs instead"라고 권한다 `[검증][웹]`.

**관점 A:** 서버가 클라이언트의 LLM을 빌려 쓰는 설계는 우아하지만 구현한 클라이언트가 적고 보안·비용 귀속이 모호했다 → 정리하는 게 맞다.
**관점 B:** 한 리비전 만에 강화했다가 폐기하는 것은 거버넌스의 불안정성을 보여준다. 이런 진동이 채택을 늦춘다.

### 4-7. stdio vs HTTP / 로컬 vs 원격

**원격 옹호 `[커뮤]`:** 0x696C6961(웹·모바일엔 CLI가 없다), dvcrn(폰·웹·iPad 이식성), didibus(대기업 SaaS는 MCP만 제공).
**stdio의 약점:** §1-3 참조.
**HTTP/원격의 약점 — OAuth 지옥 `[커뮤]`** (전부 1차 이슈): #67291 *"HTTP MCP server that requires OAuth **freezes entire CLI**"*(2026-06-11), #47390 *"MCP OAuth SDK sends **empty User-Agent**, causing 403 from WAF/Cloudflare-protected servers"*(2026-04-13), #44652 403 step-up 재인가 미작동, #67999 Google Desktop OAuth 시크릿 거부.
- **v2.1.196**: *"Fixed MCP OAuth requesting the authorization server's full `scopes_supported` catalog when no scope is specified, causing `invalid_scope` failures on **GitLab self-hosted** and other enterprise IdPs"* → **자체 호스팅 IdP를 쓰는 한국 기업 환경에 특히 관련.**

---

## 5. 실무 적용 팁

### 5-1. 지배적 패턴: **고통은 "에러"가 아니라 "침묵"이다** `[커뮤]`

> **이것이 이 책의 가장 강력한 챕터 오프닝 소재다.** 초보자는 에러 고치는 법을 배우지만, MCP 서버 개발자는 **아무 일도 안 일어난 것처럼 보이는 상황을 의심하는 법**을 배워야 한다.

| 조용한 손실 | 출처 | 상세 |
|---|---|---|
| **도구 `description`·`instructions`가 2048자에서 말없이 잘림** | claude-code **#81268**, **2026-07-26 작성(당일!)**, v2.1.220, **open** | 실측 **502건 절단**, 최악 **10780→2048자(81% 손실)**. 영향 상위에 **Anthropic 자체 커넥터** 포함. *"the server is **never told it happened**: no error, no field in the response, no warning."* 게다가 `/mcp`는 **안 잘린 원문**을 보여줘 눈으로 확인조차 불가 |
| `tools/list` 페이지네이션 2페이지 이후 도구 조용히 드롭 | CHANGELOG v2.1.144 | 도구 많은 서버를 만들면 반드시 밟는다 |
| **`Optional[X]` / `anyOf [X, null]` 스키마가 모델 도달 전 제거** | #56263 (2026-05-05, **open**) | **Python으로 서버 짜며 `Optional[str]`을 쓰면 스키마가 뭉개진다** |
| 16KB 초과 `inputSchema` 도구 조용히 드롭 | #77296 (2026-07-13) | claude.ai 커넥터 인제스천 |
| 헤드리스 MCP 연결 실패가 **"zero signal in stderr or stream-json"** | #43968 (2026-04-05) | §3-7 참조 |

**그리고 "✓ Connected"는 거짓말을 한다 `[커뮤]`.** 핸드셰이크 성공 ≠ 도구 사용 가능. v2.1.181이 표시를 `! Connected · tools fetch failed`로 바꾼 이유다. "왜 내 서버가 안 붙나" 카탈로그의 상당수가 실은 **"붙었는데 도구가 없다"**이다.

### 5-2. stdout 함정 — "한 번은 다 당하는" 실수 1위

**증상 → 원인 → 해결 `[커뮤]`** (claude-code #48866, 2026-04-16):
- **증상:** `Parse error: Unexpected token ... '[2m2026-0' ... is not valid JSON` / `Protocol error: Method not found: notifications/initialized` / 시작하자마자 `Connection closed`
- **원인:** stdout이 프로토콜 채널인데 배너·타임스탬프·**ANSI 컬러 코드**·`print()`·의존 라이브러리 로그가 섞였다. **래퍼 셸 스크립트나 셸 시작 파일(`.zshrc`)의 출력도 포함** — 이게 특히 안 보이는 원인
- **해결:** stdout엔 JSON-RPC만. 로깅은 전부 stderr

이슈가 제안한 문서 문구(그대로 인용 가능):
> "**Important:** For stdio MCP servers, stdout is reserved for MCP protocol messages. Do not print banners, logs, or other non-JSON text to stdout. Send diagnostics to stderr instead."

한때는 **stdout에 이물질 한 줄만 나와도 즉시 연결이 끊겼다** (2.1.105 리그레션) `[커뮤]`.

> **부가 주의:** stderr도 공짜가 아니다 — v2.1.208이 *"MCP stdio server stderr accumulating up to **64 MB per server**"* 누수를 수정했다 `[커뮤]`.
> **그리고 공식 문서가 이걸 설명하지 않는다는 이슈가 따로 있다**(#48866, closed as not planned) — 책이 채울 수 있는 공백.

### 5-3. 그 밖의 필수 함정

1. **버전 문자열을 부등호로 비교하지 마라** — 공식 SDK 주석이 직접 경고 `[웹]` (§1-4)
2. **"왜 구버전으로 붙지?"** — 협상 실패 fallback이 `2025-03-26` `[검증][웹]`
3. **`npx` 실행 실패** — `bin` 대상에 실행 권한(755) 필요. 단 **공식 예제에 shebang은 없다** `[웹]` (§3-8)
4. **스코프 패키지 배포 실패** — `--access public` 누락 `[웹]`
5. **Python 의존성 사고 예방** — 안정 v2 전에 **`mcp>=1.27,<2` 상한** `[웹]`
6. **`--` 위치** — `claude mcp add`에서 `--` 뒤는 전부 서버 실행 커맨드 `[웹]`
7. **어제는 됐는데 오늘은 안 보인다** `[커뮤]` — `--scope` 없이 추가 → 기본값 `local` → **추가한 디렉터리에 묶임**. 해결: `--scope user`(전역) 또는 `--scope project`(`.mcp.json` 커밋)
8. **`.mcp.json`을 커밋했는데 팀원 환경에서 `⏸ Pending approval`** `[커뮤]` — v2.1.196의 의도적 보안 강화(리포지토리 자기승인 차단). → **"설정 파일을 커밋한다"는 게 곧 "임의 프로세스 실행을 커밋한다"는 뜻**임을 자각시킬 지점
9. **토큰이 맞는데 401** `[커뮤]` — 설정값 앞뒤 **보이지 않는 공백**(v2.1.219가 경고를 추가한 이유)
10. **Claude Desktop이 심링크된 설정 파일을 일반 파일로 갈아치운다** (#80276) `[커뮤]` — dotfiles 사용자가 정확히 당한다

### 5-4. 디버깅 도구

- **MCP Inspector**: `npx @modelcontextprotocol/inspector` — **1.0.0 (2026-07-18 릴리스)** `[검증]`. 직전이 0.22.0(2026-06-04)이니 **최근에야 1.0에 도달**했다.
  > **구조적 한계 `[커뮤]`:** Inspector는 **당신의 서버와 직접** 말한다. 그래서 **"Inspector에선 되는데 Claude Code에선 안 된다"**가 발생한다 — 스코프·환경변수·PATH·승인 상태는 Inspector가 재현하지 않는 층이다.
- **로그 경로 `[커뮤]`** (1차 확인, macOS/2.1.220): `~/Library/Caches/claude-cli-nodejs/*/mcp-logs-*/*.jsonl` — **JSONL이라 `jq`로 바로 분석 가능**
- **`--debug` 실제 출력 `[커뮤]`:**
  ```
  [DEBUG] MCP server "X": Successfully connected (transport: stdio) in 3727ms
  [DEBUG] MCP server "X": Tool 'my_tool' still running (30s elapsed)
  [DEBUG] MCP server "X": Tool 'my_tool' failed after 68s: MCP error -32000: Connection closed
  ```
  → **`MCP error -32000: Connection closed`가 실무에서 가장 자주 보게 될 에러 문자열**이다
- **`--safe-mode`** (v2.1.169) `[커뮤]`: CLAUDE.md·플러그인·스킬·훅·MCP를 전부 끄고 기동 → **이분 탐색 디버깅의 출발점**
- **`--strict-mcp-config`** `[커뮤]`: 특정 서버만 로드해 격리. #68375에서 실제 진단에 사용됨(전체 함대 행 → 1개 제한 시 5초)

### 5-5. 타임아웃 — 구체적 노브 `[커뮤]` (전부 CHANGELOG 1차)

| 항목 | 버전 | 내용 |
|---|---|---|
| 기본 **60초** 타임아웃 & `request_timeout_ms` 무시 버그 | v2.1.206 | 긴 도구 호출이 신규 세션에서 60초에 죽었다 |
| **2분 초과 시 자동 백그라운드** | v2.1.212 | `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`로 조절/비활성 |
| 원격 MCP **5분 무응답 행** | v2.1.187 | `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`로 오버라이드 |
| 1000ms 미만 timeout이 **모든 호출을 죽인** 버그 | v2.1.162 | 이제 sub-1000ms 값은 무시됨 |
| 연결 배치 크기 | — | `MCP_SERVER_CONNECTION_BATCH_SIZE` — **바이너리 grep으로 실존 확인**. 같은 댓글이 커뮤니티에 돌던 **틀린 이름 `MCP_MAX_CONCURRENT_INIT`를 명시적으로 반증**했다 `[커뮤]` |

### 5-6. 관찰성 (프로덕션)

- **분산 추적이 프로토콜에 들어왔다 `[검증][웹]`:** `2026-07-28` RC가 `_meta`의 `traceparent`·`tracestate`·`baggage`(W3C Trace Context) 전파를 문서화(SEP-414). TS SDK 2.0이 `TRACEPARENT_META_KEY` 등으로 구현 중이고, **Python SDK 2.0은 `opentelemetry-api`를 하드 의존성으로** 넣었다.
- **로깅의 미래 `[검증][웹]`:** `2026-07-28` RC가 Logging을 deprecated하며 "log to `stderr` (stdio) or use **OpenTelemetry**"를 권한다 → **관찰성 장은 OTel 중심으로 쓰는 게 맞다.**
- **stdio의 구조적 제약 `[커뮤]`:** HTTP 계열은 헤더로 trace context가 자연스럽게 전파되지만 **stdio는 헤더가 없어** 파라미터·환경변수로 명시적으로 실어야 한다. 권장 span 계층: `session → task → turn → tool.call`.
- **클라이언트 측 텔레메트리 `[커뮤]`** (v2.1.157): `tool_decision` 이벤트에 `tool_parameters` 포함 — 환경변수 **`OTEL_LOG_TOOL_DETAILS=1`**
- **비용 가시성 `[커뮤]`** (v2.1.149): `/usage`가 **MCP 서버별 비용**을 분해해 보여준다
- **성능 `[커뮤]`** (v2.1.208): 도구 많을 때 tool-pool 조립 캐싱으로 **최대 7배** 빨라짐 → **도구가 많으면 CPU 비용도 든다**는 걸 Anthropic이 최적화로 인정한 셈
- **학술적 근거 `[논문]`** (E-1, arXiv 2606.04990): *"최종 답 정확도만으로는 tool 호출이 정당했는지 설명할 수 없다."* → 로그에 "무엇을 실행했나"만으론 부족하고 **어떤 컨텍스트·증거가 그 호출을 유발했는지**까지 남겨야 사후에 tool poisoning을 판별할 수 있다. **관찰성은 운영 편의가 아니라 공격의 사후 탐지 수단이다.**

### 5-7. 설계 규칙 — tool을 몇 개나 만들 것인가

**생태계 실측과 성능 실험이 같은 답을 가리킨다.**

`[논문]` C-1 (arXiv 2507.16044, 공식 서버 116개 + OpenAPI 계약 80개):
> "We find that **88.6% of servers are fully or partially REST-backed, with 92% implementing tools as bare API wrappers**. MCP servers expose a **median of 19% of available operations**…"
- 그 선택은 무작위가 아니라 **명세로부터 예측 가능한 체계적 패턴**을 따른다
- 자동 생성 성공률 **baseline 76% → 자동 복구 시 94.2%**
- **필터링·재그룹화로 API당 tool 개수 중앙값을 1/3 감소**

`[논문]` D-4: 짧은 적응형 목록이 **LLM의 tool 선택 능력 자체를 개선**(93.1% vs 87.1%).

→ **핵심 설계 규칙:** **REST API 전체를 tool로 1:1 노출하지 마라.** 잘 만들어진 서버들은 중앙값 **19%**만 노출한다. tool을 줄이는 건 손해가 아니라 **선택 정확도를 올리는 일**이다. 잘게 쪼개기보다 의미 단위로 묶고 개수를 의도적으로 억제하라.

**보조 규칙 `[논문]`:**
- **tool 이름에 네임스페이스를 붙여라** — B-3(arXiv 2602.11327)이 다중 서버 환경에서 resolver 정책에 따른 **"wrong-provider tool execution"**(다른 서버의 tool이 실행되는) 위험을 정량화했다
- **tool 정의에 버전과 서명을 붙이고, 정의가 바뀌면 재승인을 요구하게 만들어라** — A-8 ETDI(arXiv 2506.01333). rug pull의 본질은 "승인된 tool 정의가 나중에 바뀐다"이므로 승인은 **tool 정의 해시에 묶여야** 한다
- **description은 짧고 정확하게** — 길게 쓰면 2048자에서 말없이 잘린다 `[커뮤]` (§5-1)
- **보안 게이트를 생성·배포·운영·유지보수 4개 시점으로 쪼개라** — A-1(arXiv 2503.23278)의 생애주기 4단계×16활동. **특히 유지보수(업데이트) 단계가 rug pull의 진입점**

### 5-8. 버전 명기 규율 (이 책 특유의 요구)

**네 개의 독립 축을 절대 하나로 합치지 마라 `[검증]`:**
1. **스펙 리비전** — `2025-11-25`(정식) / `2026-07-28`(RC)
2. **SDK semver** — TS 1.29.0·2.0.0-beta.5 / Python 1.28.1·2.0.0b2 / Java 2.0.0 / Spring AI 2.0.0
3. **클라이언트 CLI 버전** — Claude Code 2.1.220 / Codex 0.145.0 / Agent SDK 0.3.220·0.2.128
4. **`server.json` 레지스트리 스키마** — `2025-12-11`

---

## 6. 참고문헌

### 1차 소스 — 스펙
1. MCP Specification, `schema/` 디렉토리 열거. https://github.com/modelcontextprotocol/modelcontextprotocol/tree/main/schema (검색 2026-07-26)
2. `schema/2025-11-25/schema.ts` — `LATEST_PROTOCOL_VERSION = "2025-11-25"` (L12)
3. `schema/draft/schema.ts` — `LATEST_PROTOCOL_VERSION = "2026-07-28"` (L30)
4. MCP Specification Changelog (2025-11-25). https://modelcontextprotocol.io/specification/2025-11-25/changelog
5. MCP Specification Draft Changelog (2026-07-28). https://modelcontextprotocol.io/specification/draft/changelog
6. MCP GitHub Releases — 태그 전수 및 `2026-07-28-RC` 릴리스 노트 (2026-05-29, `prerelease: true`). https://github.com/modelcontextprotocol/modelcontextprotocol/releases
7. MCP 공식 소개. https://modelcontextprotocol.io/docs/getting-started/intro

### 1차 소스 — SDK
8. `@modelcontextprotocol/sdk` npm (1.29.0, publish 2026-03-30)
9. `@modelcontextprotocol/{server,client,core,node,express,hono,fastify,server-legacy,codemod}` npm (2.0.0-beta.5, 2026-07-21)
10. TypeScript SDK README (main = v2 beta). https://github.com/modelcontextprotocol/typescript-sdk
11. PyPI `mcp` (1.28.1 / 2026-06-26; 2.0.0b2 / 2026-07-14). https://pypi.org/project/mcp/
12. PyPI `mcp-types` (2.0.0b2); PyPI `fastmcp` (3.4.4, jlowin — 별개 패키지)
13. python-sdk `mcp_types/version.py` (v2.0.0b2) — `KNOWN`/`HANDSHAKE`/`MODERN_PROTOCOL_VERSIONS`
14. MCP Java SDK v2.0.0 릴리스 노트 (2026-06-11). https://github.com/modelcontextprotocol/java-sdk/releases/tag/v2.0.0
15. MCP Java SDK `MIGRATION-2.0.md`
16. Spring AI Maven Central `maven-metadata.xml` (2.0.0 / 2026-06-12). https://repo1.maven.org/maven2/org/springframework/ai/
17. Spring AI 레퍼런스 asciidoc 원문 — `mcp-server-boot-starter-docs.adoc`, `mcp-annotations-server.adoc` (`@McpTool`·프로토콜 매트릭스). https://github.com/spring-projects/spring-ai

### 1차 소스 — 배포·도구·클라이언트
18. MCP Registry README + publish quickstart (`mcpName`, `mcp-publisher`, "currently in preview"). https://github.com/modelcontextprotocol/registry
19. MCP Registry Live API — `GET /v0/servers` HTTP 200, `server.json` 스키마 `2025-12-11`. https://registry.modelcontextprotocol.io/v0/servers
20. MCP Registry GitHub Releases (v1.8.0 / 2026-07-13)
21. `@modelcontextprotocol/inspector` npm 1.0.0 + GitHub 릴리스 1.0.0 (2026-07-18)
22. Claude Code MCP 공식 문서. https://code.claude.com/docs/en/mcp · quickstart: https://code.claude.com/docs/en/mcp-quickstart
23. Claude Code CLI 실측 — `claude --version` = 2.1.220, `claude mcp --help`, `claude mcp add --help` (로컬 2026-07-26)
24. `@anthropic-ai/claude-agent-sdk` 0.3.220 `sdk.d.ts` 실측; PyPI `claude-agent-sdk` 0.2.128 (2026-07-25)
25. Claude Agent SDK 커스텀 도구 문서. https://platform.claude.com/docs/en/agent-sdk/custom-tools
26. Codex CLI 0.145.0 실측 — `codex --help`, `codex mcp --help` (로컬 2026-07-26)
27. MCP quickstart-resources `weather-server-typescript/package.json`. https://github.com/modelcontextprotocol/quickstart-resources
28. `anthropics/claude-code` CHANGELOG.md (2026-07-26 스냅샷, 최신 2.1.220). https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

### 논문 (전부 arXiv abs 페이지 직접 검증, 2026-07-26)
**보안 (A)**
29. Hou, X., Zhao, Y., Wang, S., Wang, H. (2025). *Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions.* arXiv:2503.23278 (v3 2025-10-07). https://arxiv.org/abs/2503.23278
30. Hasan, M. M., Li, H., Fallahzadeh, E., Rajbahadur, G. K., Adams, B., Hassan, A. E. (2025). *MCP at First Glance: Studying the Security and Maintainability of MCP Servers.* arXiv:2506.13538 (v5 2026-04-13). https://arxiv.org/abs/2506.13538
31. Li, X., Gao, X. (2025). *A First Look at the Security Issues in the Model Context Protocol Ecosystem.* arXiv:2510.16558 (v2 2026-04-27). **✅ DSN 2026 게재 확정.** https://arxiv.org/abs/2510.16558
32. Wang, Z., Gao, Y., Wang, Y., et al. (2025). *MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers.* arXiv:2508.14925. **✅ AAAI-26**, Vol.40 Iss.42, pp.35811–35819. **DOI: 10.1609/aaai.v40i42.40895** ⚠️ arXiv판 제목엔 "Attack"이 있고 게재판엔 없다
33. Zhao, W., Liu, J., Ruan, B., Li, S., Liang, Z. (2025). *When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation.* arXiv:2509.24272
34. Yang, Y., Gao, C., Wu, D., Chen, Y., Li, Y., Wang, S. (2025). *MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols.* arXiv:2508.13220 (v3 2026-02-12). 코드: github.com/AIS2Lab/MCPSecBench
35. Huang, C., Huang, X., Tran, N. P., Milani Fard, A. (2026). *MCP Threat Modeling and Analyzing Vulnerabilities to Prompt Injection with Tool Poisoning.* arXiv:2603.22489. ⚠️ MDPI 저널판과 동일 연구 가능성 — 두 편으로 세지 말 것
36. Bhatt, M., Narajala, V. S., Habler, I. (2025). *ETDI: Mitigating Tool Squatting and Rug Pull Attacks in MCP by using OAuth-Enhanced Tool Definitions and Policy-Based Access Control.* arXiv:2506.01333
37. Gaire, S., Gyawali, S., Mishra, S., Niroula, S., Thakur, D., Yadav, U. (2025). *SoK: Security and Safety in the Model Context Protocol Ecosystem.* arXiv:2512.08290 (v2 2025-12-13)

**프로토콜 비교 (B)**
38. Yang, Y., Chai, H., Song, Y., et al. (2025). *A Survey of AI Agent Protocols.* arXiv:2504.16736 (v3 2025-06-21)
39. Ehtesham, A., Singh, A., Gupta, G. K., Kumar, S. (2025). *A survey of agent interoperability protocols: MCP, ACP, A2A, and ANP.* arXiv:2505.02279 (v2 2025-05-23)
40. Anbiaee, Z., Rabbani, M., Mirani, M., et al. (2026). *Security Threat Modeling for Emerging AI-Agent Protocols: MCP, A2A, Agora, and ANP.* arXiv:2602.11327 (v2 2026-04-17)

**생태계 실증 (C)**
41. Mastouri, M., Ksontini, E., Barrak, A., Kessentini, W. (2025). *From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents.* arXiv:2507.16044 (v4 2026-04-06)
42. Toeppe, B., Barrak, A., Ksontini, E. (2026). *A Large-Scale Dataset of MCP Implementations on GitHub.* arXiv:2607.10123 (v1 2026-07-11) 🕒 검색 시점 기준 15일 전

**도구 사용의 계보 (D)**
43. Yao, S., Zhao, J., Yu, D., et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629 (v3 2023-03-10). **✅ ICLR camera ready.** https://react-lm.github.io
44. Schick, T., Dwivedi-Yu, J., Dessì, R., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* arXiv:2302.04761 ⚠️ 게재처 단정 금지
45. Qin, Y., Liang, S., Ye, Y., et al. (2023). *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs.* arXiv:2307.16789 (v2 2023-10-03)
46. Repantis, V., Gawde, A., Singh, H., Blackwell II, J. (2026). *How Many Tools Should an LLM Agent See? A Chance-Corrected Answer.* arXiv:2605.24660 (v2 2026-06-07)

**관찰성 (E)**
47. Wang, Y., Zhang, J., Cai, T., et al. (2026). *From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents.* arXiv:2606.04990 (v4 2026-06-28)

### 커뮤니티 (전부 작성일·버전 확인)
**GitHub 이슈 (`gh issue view` 1차)**
48. claude-code #81268 — MCP 2048자 조용한 절단 (2026-07-26, open, v2.1.220)
49. claude-code #48866 — stdio stdout/stderr 문서 누락 (2026-04-16, closed as not planned; 2.1.105 리그레션 인용)
50. claude-code #43968 — 헤드리스 MCP 실패 무신호 (2026-04-05, v2.1.92)
51. claude-code #68375 — `claude -p` 도구 호출 행 (2026-06-14, open, 2.1.177 리그레션)
52. claude-code #80996 — `--resume` 후 MCP 복구 경로 없음 (2026-07-24, open)
53. claude-code #74329 — stdio 서버 프로세스 누수 (2026-07-05, open, 2.1.201)
54. claude-code #56263 — `Optional[X]` 스키마 제거 (2026-05-05, open)
55. claude-code #8288 — 스코프 가시성 + 79k/36k/20k 토큰 실측 (2025-09-28, closed) ⚠️구식
56. claude-code #66262 / #74768 / #77388 / #80016 / #80276 — 클라이언트별 동작 차이·Desktop 함정 (2026-06~07)
57. claude-code #67291 / #47390 / #44652 / #67999 — OAuth 실패 계열 (2026-04~06)
58. claude-code #7279 — in-process SDK MCP 무음 실패 (2025-09-07) ⚠️구식

**HN 스레드 (Algolia API로 점수·댓글수 확인)**
59. "I still prefer MCP over skills" (47712718) — 460/375, 2026-04-10
60. "When does MCP make sense vs CLI?" (47208398) — 447/284, 2026-03-01
61. "MCP is dead?" (48330436) — 400/410, 2026-05-29
62. "MCP server that reduces Claude Code context consumption by 98%" (47193064) — 570/107, 2026-02-28
63. "MCP is dead; long live MCP" (47380270) — 295/205, 2026-03-14
64. "Zero-Touch OAuth for MCP" (48592163) — 278/103, 2026-06-18

**국내 커뮤니티**
65. GeekNews "MCP는 죽었나?" (topic 30028, ~2026-05). https://news.hada.io/topic?id=30028
66. GeekNews "MCP는 죽었다. CLI 만세" (topic 27129, ~2026-03)
67. GeekNews Context Mode (topic 27108 / 29106, 2026-02·04 추정)

**리포지토리 (`gh repo view`)**
68. steipete/claude-code-mcp — 1,313⭐, **아카이브됨** (푸시 2026-05-15)
69. grahama1970/claude-code-mcp-enhanced — 125⭐, 마지막 푸시 2025-05-20
70. SinanTufekci/agent-intern — 16⭐, 활발 (2026-07-24). 검증 버전 명시: agy 1.1.6 / codex-cli 0.144.1 / copilot-cli 1.0.69 / cursor-agent 2026.07.08

**보안 공시**
71. CVE-2025-49596 — MCP Inspector RCE, CVSS 9.4, `<0.14.1`, 공개 2025-07. GHSA-7f8r-222p-6f5g

---

## 7. 리서치 한계 (커버하지 못한 영역)

### A. 확정된 부정적 발견 (조사 완료된 결론 — 미조사가 아니다)
1. **"MCP 2.0"은 스펙의 공식 명칭으로 존재하지 않는다.** 세 경로 교차 확인(디렉토리 열거·릴리스 태그 전수·상수). 유일한 `"2.0"`은 `JSONRPC_VERSION` `[검증][웹]`
2. **`schema/2026-07-28/`는 2026-07-26 시점에 존재하지 않는다.** `main`과 RC 태그 양쪽 확인 `[웹]`
3. **TS SDK에 2.x 정식 릴리스 없음** — dist-tags는 `{latest: 1.29.0}` 하나뿐 `[검증]`
4. **Python `mcp`에 2.x 정식 릴리스 없음** — `info.version` = 1.28.1 `[검증]`
5. **MCP Registry는 가동 중이나 GA가 아니다** `[웹]`
6. **`FastMCP`는 Python `mcp` 2.0에 존재하지 않는다** — wheel 전체 문자열 검색 0건 `[검증]`
7. **"MCP 서버 개발 방법"에는 학술 문헌이 없다** `[논문]` — SDK 사용법·구현 패턴·배포 실무를 다룬 논문은 **존재하지 않는다.** 학계는 "위험한가(A)·다른 프로토콜과 어떻게 다른가(B)·생태계가 어떻게 생겼나(C)"로 접근한다. 유일한 예외가 C-1. → **논문은 "왜 그렇게 설계해야 하는가"의 근거로만 쓰는 게 맞다**
8. **토픽 6은 정착된 실무 관행이 아니다** `[커뮤]` — 여러 검색 쿼리가 모두 빈 결과. 구현체 3개 중 최대 리포는 아카이브, 2위는 14개월 방치. **이건 실패가 아니라 결과다**
9. **토픽 6의 비용 폭발·재귀 사고 보고가 하나도 없다** `[커뮤]` — 보고되는 건 권한·상태 문제이고, 이 패턴의 명시적 동기는 오히려 **비용 절감(쿼터 차익거래)**이다
10. **OAuth confused deputy / 토큰 패스스루 전용 학술 논문 없음** `[논문]` → 이 주제는 **MCP 명세 + RFC 9700**을 1차 근거로 삼고 ETDI로 보조해야 한다
11. **Java/JVM MCP를 다룬 논문 없음** `[논문]`, **Java/Kotlin 커뮤니티 논의도 없음** `[커뮤]` — 담론은 TS·Python에 압도적 편중

### B. 확인하지 못한 것 (챕터 저술 전 보강 필요)
1. **MCP 스코프 우선순위(`local > project > user`)** — 2차 블로그는 일치하나 **1차 문서 미확인. 단정 금지** `[커뮤]`
2. **`server.json` 스키마 전문**과 `mcp-publisher` 서브커맨드(`init`/`login`/`publish`) 시퀀스 `[웹]`
3. **`uvx`/`uv run` 실행 공식 커맨드**, MCP 서버용 Dockerfile 공식 권장 패턴 `[웹]`
4. **Kotlin/C#/Go/Rust SDK 버전**과 SEP-1730 SDK 티어 등급표 `[웹]`
5. **`server/discover` RPC 상세 시그니처**와 `_meta` 봉투 필드 전체 목록 — changelog 수준까지만 `[웹]`
6. **Python SDK 2.0 `MCPServer`의 공식 사용 예제** — 클래스·모듈 구조는 실측했으나 예제 코드 미확보 `[검증]`
7. **Spring AI 2.0.0이 pin하는 java-sdk 버전**, `@McpTool`의 소속 아티팩트 `[웹]`
8. **deferred tool loading 도입 시점(2025-11?)과 "85% 절감" 수치** — 1차 미검증 `[커뮤]`
9. **한국어 CORS/OAuth discovery 함정 사례** — 원문 URL·작성일 특정 실패 `[커뮤]`
10. **stdio vs Streamable HTTP 성능 비교 논문** — 확보 실패 `[논문]`

### C. 접근 차단·수집 실패
- **Reddit 전면 차단** `[커뮤]` — r/mcp·r/ClaudeAI·r/LocalLLaMA의 1차 토론을 **전혀 수집하지 못했다.** 브리프 지정 소스 중 가장 큰 공백
- **Lobsters·Dev.to·Mastodon·X·Discord/Slack** — 체계적으로 탐색하지 못함 `[커뮤]`
- **arXiv API 전수 열거 실패** `[논문]` — `Rate exceeded`(12회 재시도) + Semantic Scholar 429. 논문 목록은 "WebSearch로 발견 가능한 범위"이며 **전수 조사가 아니다**. 미검증 후보 19편이 papers.md N-7에 격리돼 있다
- **웹 리서치의 한국어 자료 0건** `[웹]` — 예산을 토픽 2의 1차 검증에 집중한 결과
- **국내 커뮤니티는 논쟁에만 활발** `[커뮤]` — **토픽 5(디버깅)·토픽 6(오케스트레이션)에 대한 한국어 1차 토론은 발견하지 못했다.** velog는 대부분 "사용법 소개"이고 삽질 회고는 드물다
  > **→ 이것이 이 책의 포지셔닝 기회다: 토픽 5·6의 한국어 자료가 사실상 없다.**

### D. 하류(fact-checker)를 위한 경고
- **이 문서는 2026-07-26에 고정된 스냅샷이다.** 특히 `2026-07-28` 리비전은 **이틀 뒤 정식 릴리스 예정**이다. 저술·팩트체크 시점에 `schema/` 디렉토리와 GitHub Releases를 **반드시 재확인**하라. `schema/2026-07-28/`가 생겼고 릴리스가 `prerelease: false`가 됐다면 §2-1·§2-3의 "RC" 서술은 즉시 낡는다
- 같은 이유로 **TS SDK 2.0.0 정식**·**Python `mcp` 2.0.0 정식**도 며칠 내 나올 수 있다 (TS README: "stable release alongside the full release of the 2026-07-28 spec on July 28, 2026")
- **Java SDK 2.0.0과 Spring AI 2.0.0은 스펙 `2025-11-25`를 따른다.** 숫자가 2.0이라고 `2026-07-28`을 구현한다고 착각하지 마라
- **Maven 버전을 `search.maven.org/solrsearch`로 확인하지 마라** — 인덱스가 낡아 Spring AI를 `1.0.0`으로 잘못 보고한다. `repo1.maven.org`의 `maven-metadata.xml`이 권위 소스 `[웹][검증]`
- **`research/community.md`와 `research/papers.md`의 `(확인 필요)` 표시는 챕터의 `(사실 확인 필요)` 마커가 아니다** — 리서처 수준의 출처 확보 실패 기록이며 이미 상당한 검색 후에도 실패한 항목들이다(특히 Perplexity·21k토큰 수치). **Critical 웹 예산을 여기에 재소모하지 말 것.** 이 라벨들은 저술가가 해당 주장을 본문에 쓰지 못하게 막는 **차단선**으로 기능해야 한다
- **인용 시 논문 혼동 금지** `[논문]`: "1,899개 서버 / 7.2% / 5.5% / 66%"는 **A-2(2506.13538)**, "67,057개 / 833개 취약"은 **A-3(2510.16558)**. 19편 중 **동료 심사 통과가 문서로 확인된 것은 A-3·A-4·D-1 3편뿐**이며 나머지는 프리프린트다. "연구에 따르면"으로 단정 인용할 땐 이 3편을 우선 배치하라

### E. 리서처 산출 상태
- `research/web.md` — **완료** (27개 소스, 전량 1차)
- `research/papers.md` — **완료** (19편 전원 arXiv abs 직접 검증 + 미검증 후보 19편 격리)
- `research/community.md` — **완료** (GitHub 이슈·CHANGELOG 버전 매핑·HN Algolia API·GeekNews 1차)

---

## 신선도 원장 (소스별 발행일·버전 시점)

> **네 개의 독립 축을 분리 유지한다.** 합치면 fact-checker가 오비교한다.

### 축 1 — 스펙 리비전
| 리비전 | 지위 | 날짜 | 확인 방법 |
|---|---|---|---|
| `2025-11-25` | **정식 최신** | 2025-11-25 게시 | `[검증]` schema.ts L12 상수 + 릴리스 태그 |
| `2026-07-28` | **RC(prerelease)**, 정식 예정 2026-07-28 | RC 2026-05-29 게시 | `[검증]` Releases API `prerelease: true`, `schema/draft/schema.ts` L30 |
| `2025-06-18` / `2025-03-26` / `2024-11-05` / `2024-10-07` | 구 정식 | 각 태그일 | `[검증]` 태그 전수 |

### 축 2 — SDK 버전 ("{버전}/{연도} 기준")
| SDK | 정식 | 프리릴리스 | **구현 스펙** |
|---|---|---|---|
| TS `@modelcontextprotocol/sdk` | **1.29.0 / 2026-03-30 기준** | — | 2025-11-25 |
| TS `@modelcontextprotocol/{server,client,core,node,express,hono,fastify,server-legacy,codemod}` | — | **2.0.0-beta.5 / 2026-07-21 기준** | **런타임 `SUPPORTED`는 2025-11-25까지** (2026-07-28은 JSDoc에만 등장). README는 2026-07-28 표방 `[검증]` |
| Python `mcp` | **1.28.1 / 2026-06-26 기준** | **2.0.0b2 / 2026-07-14 기준** | 1.x=2025-11-25; 2.0은 **2026-07-28 실제 병행** |
| Python `mcp-types` | — | 2.0.0b2 / 2026-07-14 | `MODERN_PROTOCOL_VERSIONS = ("2026-07-28",)` `[검증]` |
| Python `fastmcp` (jlowin, **별개 패키지**) | **3.4.4 / 2026 기준** | — | 미확인 |
| Java `io.modelcontextprotocol.sdk:mcp` | **2.0.0 / 2026-06-11 기준** | — | **2025-11-25** (릴리스 노트 명시) |
| Spring AI `spring-ai-starter-mcp-*` (5개) | **2.0.0 / 2026-06-12 기준** | — | 2025-11-25 계열(추정) |

### 축 3 — 클라이언트·도구 버전
| 대상 | 버전 | 시점 | 확인 |
|---|---|---|---|
| Claude Code CLI | **2.1.220** | 2026-07-26 로컬 | `[검증]` `claude --version` |
| `@anthropic-ai/claude-agent-sdk` (TS) | **0.3.220** | 2026-07-26 | `[검증]` npm |
| `claude-agent-sdk` (PyPI) | **0.2.128** | **2026-07-25 게시** | `[검증]` PyPI |
| Codex CLI | **0.145.0** | 2026-07-26 | `[검증]` `codex --version` |
| MCP Inspector | **1.0.0** | **2026-07-18 게시** | `[검증]` npm + GitHub 릴리스 |
| MCP Registry 소프트웨어 | **v1.8.0** | 2026-07-13 게시 | `[검증]` GitHub 릴리스 |

### 축 4 — 레지스트리 스키마
| 대상 | 버전 | 확인 |
|---|---|---|
| `server.json` 스키마 | **`2025-12-11`** | `[검증]` 레지스트리 API 응답 `$schema` |

### 커뮤니티 소스 신선도 (버전 매핑 확인)
`anthropics/claude-code` CHANGELOG 스냅샷 **2026-07-26, 최신 릴리스 2.1.220**. 인용 항목의 버전 `[커뮤]`: 2.1.219(`mcp_server_errors`·공백 경고·HTTP 상태 표시), 2.1.212(2분 자동 백그라운드), 2.1.208(stderr 64MB 누수·7배 CPU 최적화), 2.1.207(셸 인젝션 수정), 2.1.206(60초 기본 타임아웃 버그), 2.1.202(`type` 누락 에러 개선), 2.1.196(`.mcp.json` 자기승인 차단·OAuth scope), 2.1.191(404 URL 표시), 2.1.187(5분 원격 행), 2.1.181(`tools fetch failed`), 2.1.169(`--safe-mode`), 2.1.162(sub-1000ms timeout), **2.1.161(시크릿 유출 수정)**, 2.1.157(`OTEL_LOG_TOOL_DETAILS`), 2.1.154(pending approval), 2.1.153(strict-mcp-config/subagent), 2.1.149(`/usage` MCP별 비용), 2.1.144(페이지네이션 도구 드롭), 2.1.105(stdout 리그레션).

⚠️ **구식 표시 소스** `[커뮤]`: #8288(2025-09-28, 토큰 79k/36k/20k 실측 — **deferred loading 이전 데이터일 가능성**), #7279(2025-09-07), HN 원조 MCP 발표 스레드(2024-11-25).

### 논문 신선도 (arXiv 최신 개정일)
2025~2026년 논문 **16편** : 2022~2023 seminal **3편**(ReAct·Toolformer·ToolLLM) ≈ 8:2 `[논문]`.
가장 최신: **C-2 (2607.10123, v1 2026-07-11 — 검색 시점 기준 15일 전)** 🕒 / **B-3 (2602.11327, v2 2026-04-17)** / **A-3 (2510.16558, v2 2026-04-27)**.
동료 심사 확인: **A-3(DSN 2026)**, **A-4(AAAI-26, DOI)**, **D-1(ICLR camera ready)** — 나머지 16편은 프리프린트.

### 소스별 검색 시점
**전 소스 공통: 검색 2026-07-26 기준.**
- web-researcher는 종료 직전 **2026-07-26T03:03:09Z**에 핵심 주장(schema 디렉토리·릴리스 태그·`LATEST_PROTOCOL_VERSION`·npm/PyPI dist-tags)을 재조회해 동일함을 확인했다 `[웹]`
- paper-researcher는 19편 전원의 **arXiv abs 페이지를 직접 열어** 제목·저자·전 버전 제출일·Comments·초록 원문을 대조했다 `[논문]`
- community-researcher는 **CHANGELOG 인용문을 "줄 번호 → 직전 `##` 헤더" 매핑으로 기계 검증**했다(초기 버전 귀속 9건이 1~12 릴리스만큼 틀렸고 전부 측정으로 교정) `[커뮤]`
- research-lead는 npm/PyPI/Maven Central/GitHub API·레지스트리 API·로컬 CLI(`claude`/`codex`)·패키지 tarball 해제를 **2026-07-26 당일 직접 실행**했다 `[검증]`

---

## §8. 보강 리서치 (2026-07-26)

<!-- 검색 시점: 2026-07-26 기준 -->

**배경.** book-planner가 `02_plan.md`에서 레퍼런스 공백 5건을 에스컬레이션했다(9장 3건 + 4장 1건 + 스코프 1건). 1차 소스 우선으로 재조사한 결과다. 전체 원문·인용은 **`research/web_supplement.md`**에 있고, 아래는 §7 갱신에 필요한 결론만 담는다.

> **§7은 수정하지 않았다(append-only).** 아래 8-A가 §7-B의 어느 항목이 해소됐는지 명시하므로, §7-B를 읽을 때 반드시 이 절을 함께 보라.

**등급:** `[검증]`=1차 소스 원문을 직접 열어 인용 / `[2차]`=블로그·요약 / `[미확인]`=확보 실패.

### 8-A. 판정 요약 — §7-B 항목 해소 현황

| 요청 | 대상 | 결과 | 등급 |
|---|---|---|---|
| 1 | `uvx`/`uv run` 공식 커맨드 + `[project.scripts]` (§7-B-3 전반) | ✅ 해소 | `[검증]` |
| 2 | MCP 서버용 Dockerfile 패턴 + Docker 카탈로그 (§7-B-3 후반) | ✅ 해소 | `[검증]` |
| 3 | `mcp-publisher` 시퀀스 + `server.json` (§7-B-2) | ✅ 해소 | `[검증]` |
| 4 | Python SDK 2.0 `MCPServer` 공식 예제 (§7-B-6) | ✅ 해소 | `[검증]` |
| 5 | Claude Desktop 등록 절차 (§7-C 공백) | ✅ 해소 | `[검증]` |
| 보너스 | 스코프 우선순위 `local > project > user` (§7-B-1) | ✅ 해소 | `[검증]` |

**→ `02_plan.md`가 9장·4장에 걸어둔 "명령어를 지어내지 말고 개념 수준으로만 서술하라" 제약은 해제된다.** 4장 제목에서 "Desktop"을 빼는 대응도 불필요하다.

### 8-B. `uvx` / `uv run` — 두 경로를 갈라야 한다 `[검증]`

출처: `modelcontextprotocol/modelcontextprotocol` `docs/docs/develop/build-server.mdx`, `modelcontextprotocol/servers` README.md, docs.astral.sh/uv (전부 원문 직접 취득).

**공식 Python 퀵스타트는 `uvx`가 아니라 `uv run`을 쓴다.** 이 구분이 9장의 핵심이다.

- **로컬 개발 중(미배포)**: `uv init` → `uv venv` → `uv add "mcp[cli]" httpx` → 실행은 `uv run weather.py`. 클라이언트 등록은 `command: "uv"`, `args: ["--directory", "<절대경로>", "run", "weather.py"]`
- **PyPI 배포 후**: `uvx mcp-server-git` — servers README 원문 "`uvx` is recommended for ease of use and setup"

`uvx`는 `uv tool run`의 별칭이다(uv 문서 원문: "exactly equivalent to: `uv tool run ruff`"). 패키지명과 커맨드명이 다르면 `--from`이 필요하다.

**`[project.scripts]` 규약** — 공식 서버 실물 2건(`src/fetch`, `src/git`)이 일치:

```toml
[project.scripts]
mcp-server-fetch = "mcp_server_fetch:main"   # 키 == 배포 패키지명, 값은 모듈명(언더스코어):함수
```

→ **스크립트 키를 배포명과 똑같이 두어야 `uvx <이름>`이 `--from` 없이 동작한다.** 빌드 백엔드는 둘 다 `hatchling`, `requires-python = ">=3.10"`.

⚠️ **Claude Code 공식 문서에는 `uvx` 리터럴 예시가 없다** `[검증된 부정 발견]` — **두 페이지 전문 기계 검색 결과 출현 0건**: 레퍼런스 `code.claude.com/docs/en/mcp`와 워크스루 `code.claude.com/docs/en/mcp-quickstart`. 로컬 stdio 예시는 전부 `npx` 기반이며 Python 서버 예시 자체가 없다. 보증된 것은 일반 문법뿐이다:

```bash
claude mcp add [options] <name> -- <command> [args...]
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
claude mcp add playwright -- npx -y @playwright/mcp@latest   # 워크스루 페이지
```

`--` 뒤는 "passed to the server untouched". 워크스루 원문: "There's no `--transport` flag, because local servers use the default `stdio` transport." **`uvx`를 대입한 문장을 쓰되 "공식 문서의 예시"로 귀속하지 마라.**

**부수 수확 `[검증]`** — 워크스루의 스코프별 저장 위치 표(4장에 유용):

| Scope | File | Available to |
|---|---|---|
| `local` | `~/.claude.json`, under the entry for this project | "Only you, only this project. **The default**" |
| `project` | `.mcp.json` in your project root | "Everyone who clones the project" |
| `user` | `~/.claude.json`, under the top-level `mcpServers` key | "Only you, all projects" |

Windows에서 `~/.claude.json`은 `%USERPROFILE%\.claude.json`. 원문 경고: Claude Code는 `~/.claude/.mcp.json`·`~/.claude/mcp.json`·`%APPDATA%\Claude\mcp.json` 같은 경로를 **읽지 않는다**(흔한 오설정).

### 8-C. Dockerfile 패턴 `[검증]`

`modelcontextprotocol/servers` 트리 전수 열거 결과 **Dockerfile 보유 서버는 7개**(Python 3: fetch·git·time / Node 4: everything·filesystem·memory·sequentialthinking).

**Python 3건은 사실상 동일한 템플릿이다.** 추출되는 권장 패턴:

1. 멀티스테이지 — 빌드 `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`, 런타임 순정 `python:3.12-slim-bookworm`(**uv는 최종 이미지에 없다**)
2. `ENV UV_COMPILE_BYTECODE=1` (콜드 스타트), `ENV UV_LINK_MODE=copy` (캐시 마운트 하드링크 회피)
3. 의존성/소스 분리 설치 — 원문 주석: "Installing separately from its dependencies allows optimal layer caching"
4. `uv sync --locked --no-dev --no-editable` — `--locked`로 재현성 강제
5. `ENTRYPOINT ["mcp-server-fetch"]` — **`[project.scripts]`가 만든 실행 파일**

> 📌 **8-B와 8-C는 같은 한 줄에 의존한다.** `[project.scripts]` 하나가 `uvx`·`docker` `ENTRYPOINT`·`pip` 세 배포 경로의 이름을 동시에 결정한다. 9장은 이 연결로 묶어 서술하는 게 좋다.

Node 4개도 전수 확인: alpine 멀티스테이지(`node:22.12-alpine`→`node:22-alpine`) + `ENV NODE_ENV=production` + `npm ci --ignore-scripts --omit-dev`(공급망 관점에서 `--ignore-scripts`가 핵심) + `dist/`만 런타임으로 복사.

**종료 지시자 — 7개 전수 실측 결과 `[검증]`: `ENTRYPOINT` 6 / `CMD` 1.** `CMD`는 `src/everything`(전 기능 시연용 데모 서버) **단 하나뿐인 예외**이고, `filesystem`·`memory`·`sequentialthinking`은 Python 3건과 마찬가지로 `ENTRYPOINT`를 쓴다.
⚠️ 그러나 **`ENTRYPOINT`를 권장하는 명문 규정은 어디에도 없다.** "공식이 권장한다"가 아니라 **"공식 서버 7개 중 6개가 쓴다"는 측정치로** 서술하라.

**stdio 컨테이너 실행** (`src/fetch/README.md` 원문): `"command": "docker", "args": ["run", "-i", "--rm", "mcp/fetch"]`. `-i`는 stdin 유지에 필수, `-t`는 쓰지 않는다(TTY가 JSON-RPC 프레이밍을 깨뜨림). ※ `-i`/`-t` 동작 **해설**은 1차 문서 명문이 아니라 저술가 서술이다 — 커맨드만 `[검증]`.

**Docker MCP 카탈로그** — Docker Hub API 실측 `[검증]`: `mcp/` 네임스페이스 **공개 리포 245개**(2026-07-26). `mcp/fetch` pull 1,718,376 / `mcp/time` 839,028 / `mcp/git` 134,772, `date_registered` 전부 2024-12-19. 공식 문서 원문: "Docker builds and signs all local servers in the catalog", verified 서버는 provenance·SBOM 포함.
⚠️ `docker mcp` CLI 전체 서브커맨드는 `[미확인]`(확인된 건 `docker mcp catalog pull <oci-reference>` 하나) — **`docker mcp run` 같은 커맨드를 지어내지 마라.**

### 8-D. `mcp-publisher` + `server.json` `[검증]`

출처: `modelcontextprotocol/registry` `docs/reference/cli/commands.md`, `docs/modelcontextprotocol-io/quickstart.mdx`.
⚠️ 계획서가 지목한 `publish-server.md`는 **존재하지 않는다**(트리 전수 열거로 확인).

**게시 시퀀스 6단계** — 반직관 포인트가 핵심이다: **패키지를 먼저 npm/PyPI에 올리고 그 다음 레지스트리에 등록한다.** 원문: "The MCP Registry only hosts metadata, not artifacts."

1. 소유권 마커 추가 → 2. 패키지 게시(`npm publish --access public`) → 3. `mcp-publisher` 설치(`brew install mcp-publisher`) → 4. `mcp-publisher init` → 5. `mcp-publisher login github` → 6. `mcp-publisher publish`

**서브커맨드는 `--help`가 보여주는 것보다 많다:** `init`·`login`·`publish`·`logout`(--help 노출) + **`validate`·`status`**(문서에만). 전역 옵션 `--registry`(기본 `https://registry.modelcontextprotocol.io`).

**`server.json` 필수 필드:** `$schema`·`name`(`dns-namespace/name` 강제)·`description`·`version`·`repository{url,source}`·`packages[]{registryType, identifier, version}`. `packages[].transport{type}`·`environmentVariables[]`는 선택.

**✅ `$schema`가 `2025-12-11`로 축 4 신선도 원장과 정확히 일치한다** — 레지스트리 API 응답과 게시 문서라는 독립된 두 경로가 같은 값을 준다. **모순 없음.**

**소유권 검증 마커는 패키지 타입마다 다르다** (원문): npm은 `package.json`의 `mcpName`, **PyPI·NuGet은 README에 `mcp-name: <server-name>` 줄**. 실물 확인 — `src/fetch/README.md` 3행: `<!-- mcp-name: io.github.modelcontextprotocol/server-fetch -->`.

인증 4종: `github`(device flow) / `github-oidc`(CI, `id-token: write`) / `dns`·`http`(Ed25519 또는 ECDSA P-384, `v=MCPv1; k=ed25519; p=...`) / `none`(로컬 테스트). 토큰은 `~/.config/mcp-publisher/token.json`.

**레지스트리는 여전히 preview** — 원문 "currently in preview. Breaking changes or data resets may occur" → §7-A-5를 1차 문서로 재확인.

### 8-E. Python SDK 2.0 `MCPServer` 공식 예제 — **존재한다** `[검증]`

**§7-B-6의 "예제 코드 미확보"는 갱신되어야 한다.** 예제는 wheel이 아니라 **리포**에 있다. `v2.0.0b2` **태그** 트리를 전수 열거하니 문서 사이트 전체(`docs/get-started/*`, `docs/servers/*`, `docs/handlers/*`, `docs/client/*`, `docs/run/*`, `docs/migration.md`)와 실행 가능한 예제 소스(`docs_src/**/*.py`)가 들어 있다.

`docs_src/index/tutorial001.py` 원문 전문:

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

`docs_src/first_steps/tutorial001.py`는 여기에 `@mcp.prompt()`까지 더해 세 프리미티브를 모두 보여준다. 실행은 `uv run mcp dev server.py`, 설치는 `uv add "mcp[cli]==2.0.0b1"`.

**툴 등록** (`docs/servers/tools.md` 원문): "You declare one by putting `@mcp.tool()` on a plain Python function. **That's the whole API.**" SDK가 함수에서 읽는 것 — 이름=함수명, 설명=docstring, 인자=타입 힌트. "Type hints aren't documentation here. They are **the contract**." 기본값을 주면 `required`에서 빠지고 스키마에 `default`가 붙는다. 반환은 `result.content`(모델이 읽는 텍스트)와 `result.structured_content`(클라이언트용 타입 데이터)로 갈린다.

**capabilities는 자동 선언된다**: `{'prompts': {...}, 'resources': {...}, 'tools': {...}}`. 핸들러를 등록해야 생기는 것(`completions`)은 없으면 선언되지 않는다.

**✅ §7-A-6 확증:** `docs/migration.md` 원문 — "The `FastMCP` class has been renamed to `MCPServer`". 기존 결론(wheel 문자열 검색 0건)과 **독립 경로로 일치** → 책에서 강하게 단정해도 된다.

주요 breaking change: `FastMCP`→`MCPServer`, camelCase→snake_case, `mcp.types`→`mcp-types` 패키지 분리, `McpError`→`MCPError`, 리소스 URI `AnyUrl`→`str`, `streamablehttp_client` 제거, 트랜스포트 파라미터가 생성자에서 `run/app`으로 이동, 동기 핸들러가 워커 스레드에서 실행, lowlevel 데코레이터→`on_*` 생성자 파라미터, Roots·Sampling·Logging deprecated(SEP-2577). 의존성: `httpx` 제거→`httpx2`, `opentelemetry-api`·`mcp-types` 신규 필수.

⚠️ **import 경로 불일치 `[미확인]`**: first-steps는 "There is no `from mcp import MCPServer`"라며 `from mcp.server import MCPServer`를, migration은 `from mcp.server.mcpserver import MCPServer, Context`를 쓴다. **책에서는 `from mcp.server import MCPServer`를 써라**(README·튜토리얼·실제 소스가 모두 이 형태). **"둘은 같다"고 단정하지 마라.**

🕒 **프로덕션 경고 — 반드시 인용할 것.** README 원문: "**Do not use v2 in production.** ... **v1.x is the only stable release line**", 그리고 "add a `<2` upper bound ... (for example `mcp>=1.27,<2`)". PyPI 실측 `latest: 1.28.1`, 2.x는 프리릴리스 5개뿐 → §7-A-4 재확인.
⚠️ README는 정식 v2를 **2026-07-27** 목표라 쓰고 스펙은 **2026-07-28**이다. 하루 차이의 근거는 `[미확인]` — **뭉뚱그리지 마라.** §7-D 경고대로 이 절 전체가 이틀 뒤 낡을 수 있다.

### 8-F. Claude Desktop 등록 절차 `[검증]`

출처: `modelcontextprotocol/modelcontextprotocol` `docs/docs/develop/connect-local-servers.mdx` ("Connect to local MCP servers") + `build-server.mdx` 교차 확인. **§7-C가 "레퍼런스에 없다"고 한 공백이 통째로 해소됐다.**

**GUI 4단계:** ① 시스템 **메뉴 바의 Claude 메뉴** → "Settings..." (원문이 굵게 경고: "**not the settings within the Claude window itself**" — 가장 많이 헤매는 지점) → ② 좌측 사이드바 **"Developer"** 탭 → **"Edit Config"** 버튼 → ③ JSON 편집 → ④ **완전 종료 후 재시작**.

**설정 파일 경로:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- ⚠️ **Linux 없음** — 원문 "Claude for Desktop is not yet available on Linux." **경로를 지어내지 마라.**

**`mcpServers` 스키마** — 확인된 필드는 `command`·`args`·`env` 3개:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Desktop"]
    }
  }
}
```

Windows는 이중 백슬래시(`C:\\Users\\...`). 보안 경고 원문(인용 가치 높음): "**The server runs with your user account permissions, so it can perform any file operations you can perform manually.**"

**등록 확인 UI:** 입력창 좌하단 "Add files, connectors, and more /" → **Connectors** → **Manage connectors**.
⚠️ **"망치 아이콘"은 낡은 표현이다** — 트러블슈팅 제목에만 잔존하고 본문 절차는 Connectors로 갱신됐다. **책에서는 Connectors를 써라.**

**로그(디버깅 장 직결):** macOS `~/Library/Logs/Claude`, Windows `%APPDATA%\Claude\logs`. `mcp.log`=연결 일반, `mcp-server-SERVERNAME.log`=해당 서버 stderr. `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log`.

**트러블슈팅 5단계**(원문): 완전 재시작 → JSON 문법 확인 → **경로가 절대경로인지** 확인 → 로그 확인 → 커맨드를 직접 실행해보기.

**`.mcpb` / Desktop Extensions `[검증]`** — modelcontextprotocol.io 문서엔 없으나 Anthropic 1차 소스 3종(claude.com/docs/connectors/building/mcpb, `anthropics/mcpb` README, support.claude.com 10949351)에서 확보했다.

정의 원문: "An `.mcpb` file is a zip archive containing a local MCP server and a `manifest.json`. It enables single-click installation in Claude Desktop, similar to a browser extension." 특성: 로컬 실행·**stdio**·의존성 번들·오프라인 동작·**OAuth 불필요**. `.crx`/`.vsix`에 비유된다.

빌드 4단계: `npm install -g @anthropic-ai/mcpb` → stdio 서버 작성 → `mcpb init`(manifest 생성) → `mcpb pack`(번들 생성). `manifest.json`이 **유일한 필수 파일**이다.

설치 3경로(원문): ① `.mcpb` **더블클릭** ② 창에 **드래그 앤 드롭** ③ **Settings → Extensions → Advanced settings → Install Extension…**. "Installation is per-user."

⚠️ **DXT → MCPB 개명** — 리포 README 공지: "`dxt` CLI is now `mcpb`", "`.dxt` files are now `.mcpb` files". **`.dxt`를 쓰는 자료는 구버전이다**(독자의 신선도 판별 기준으로도 유용).

⚠️ **MCPB는 2차 배포 경로다** — 원문: "MCPB is the **secondary** distribution path. Remote MCP servers are recommended for directory listing." "권장 배포 방식"으로 소개하지 마라.

🔗 **item 1과 연결:** MCPB v0.4+는 manifest에 `server.type = "uv"`를 지원하고 `pyproject.toml`만 넣으면 "Host application manages Python and dependencies automatically" (`examples/hello-world-uv`). 8-B의 uv 논의가 여기서 닫힌다. 다만 언어 권장은 Node.js다 — "Node.js ships with Claude for macOS and Windows".

⚠️ `[미확인]`: `MANIFEST.md` 전체 필드 스펙 미취득(존재만 확인) — **필드를 열거하지 마라.** 리포 정본 위치도 `anthropics/mcpb`와 `modelcontextprotocol/mcpb`가 병존해 관계 미확인.

### 8-F-2. ⚠️ 두 공식 소스가 서로 다른 1차 경로를 안내한다 `[검증]`

| 소스 | 제시하는 주 경로 |
|---|---|
| modelcontextprotocol.io (`connect-local-servers.mdx`) | Settings → **Developer** → Edit Config → `claude_desktop_config.json` 직접 편집 |
| support.claude.com (`10949351`) | Settings → **Extensions** (`.mcpb` 설치) |

support.claude.com 문서 원문은 "Navigate to Settings > Extensions on Claude Desktop"이고, **`claude_desktop_config.json` 경로도 `mcpServers` 예시도 등장하지 않는다**(Developer settings는 연결 상태·로그 확인 용도로만 언급).

**→ 둘 다 유효하며 폐기된 것은 없다.** 지원 문서는 일반 사용자에게 Extensions를, 프로토콜 문서는 개발자에게 JSON 편집을 안내한다. **저술 지침:** 4장에서 두 경로를 모두 제시하되 대상을 갈라라 — **개발 중 자기 서버를 붙일 때는 `claude_desktop_config.json`**(반복 수정이 빠르다), **남에게 배포할 때는 `.mcpb`**(사용자가 JSON을 만질 필요가 없다). "공식 방법은 하나"라고 쓰면 둘 중 하나가 틀린 말이 된다.

### 8-G. 보너스 — 스코프 우선순위 §7-B-1 해소 `[검증]`

출처: Claude Code 공식 문서 "Scope hierarchy and precedence" (https://code.claude.com/docs/en/mcp).

원문: "When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source. **The entire server entry from that source is used; fields are not merged across scopes.**"

우선순위는 **3단계가 아니라 5단계**다: ① Local scope ② Project scope ③ User scope ④ Plugin-provided servers ⑤ claude.ai connectors. "The three scopes match duplicates by name. **Plugins and connectors match by endpoint.**"

**→ 세 가지 수정:**
1. `local > project > user`는 이제 **`[검증]`이며 단정 가능하다.** `02_plan.md` 154행의 "단정 금지"·"다수 자료가 이렇게 설명한다" 완화 표현은 **불필요하다.**
2. 목록은 **5단계**다 — 2차 블로그가 놓친 플러그인·커넥터 계층을 추가하라.
3. **"필드는 스코프 간 병합되지 않는다"**가 실무적으로 가장 중요한데 2차 자료에 거의 없다. 책의 차별점이 된다.

**부수 수확 `[검증]`**: Claude Code는 stdio 서버 환경에 `CLAUDE_PROJECT_DIR`(프로젝트 루트)를 주입한다. 파일시스템 접근을 제한하려는 서버는 대신 MCP `roots/list`를 구현해야 하며, **v2.1.203 이전**에는 `roots/list`가 실행 디렉토리만 반환하고 `notifications/roots/list_changed`를 보내지 않았다.

### 8-H. 이번 보강의 한계 (하류 경고)

**확정된 부정적 발견 (조사 완료 — 미조사가 아니다):**

| 발견 | 근거 |
|---|---|
| Claude Code 공식 문서에 `uvx` 리터럴 예시 없음 | 레퍼런스+워크스루 **2페이지** 전문 검색 0건 |
| 공식 레퍼런스 서버는 **7개뿐** | `servers` 리포 트리 전수 열거 |
| 7개 중 **6개가 `ENTRYPOINT`** (`CMD`는 `everything` 하나) | Dockerfile 7개 전수 원문 확인 |
| Claude Desktop **Linux 경로는 존재하지 않음** | "not yet available on Linux" + MCPB "darwin/win32" |
| **Python SDK 2.0 공식 예제는 존재함** (§7-B-6 반증) | `v2.0.0b2` 태그 트리 전수 열거 |
| **`.dxt`/`dxt` 표기는 구버전** | 리포 README의 DXT→MCPB 개명 공지 |

**남은 미확인 (지어내지 말 것):**

| 미확인 | 저술 지침 |
|---|---|
| `docker mcp` CLI 전체 서브커맨드 | `docker run -i --rm mcp/<name>`만 `[검증]`. 다른 커맨드 창작 금지 |
| uv의 `[project.scripts]` 해석 메커니즘 명문 | 공식 서버 `pyproject.toml` 실물 2건을 근거로 |
| `mcp.server` vs `mcp.server.mcpserver` 동치 | `from mcp.server import MCPServer` 사용, 동치 단정 금지 |
| v2 정식 2026-07-27 vs 스펙 2026-07-28 | 하루 차이 근거 불명, 뭉뚱그리지 말 것 |
| MCPB `MANIFEST.md` 전체 필드 스펙 | 존재만 확인. **필드를 열거하지 마라** |
| MCPB 리포 정본(`anthropics/` vs `modelcontextprotocol/`) | URL은 저술 시점에 재확인 |
| `ENTRYPOINT` 권장의 명문 규정 | 없음. "6/7이 쓴다"는 측정치로만 서술 |

**🕒 §7-D 재강조:** 8-E의 모든 버전 표기는 **`2.0.0b2` / 2026-07-26 기준**이다. 스펙 `2026-07-28`과 Python `mcp` 2.0 정식이 **이틀 안에** 나올 수 있다. fact-checker는 이 절의 버전 주장을 **저술 시점에 재확인**하라.

**전체 원문·인용·URL·확인 방법:** `research/web_supplement.md`

---

## §9. 정정 주석 (2026-07-26 Phase 4 팩트체크 발견 — append-only)

> **⚠️ §1-4·§5-3-2의 fallback 서술은 틀렸다.** `DEFAULT_NEGOTIATED_PROTOCOL_VERSION`(=`2025-03-26`)은 "협상 실패 시 낙착값"이 아니다. TS `server/index.js:274`·Python `session.py:186`의 initialize 경로는 미지원 버전 요청에 **LATEST(`2025-11-25`)로 응답**한다. 이 상수의 유일한 실사용처는 Streamable HTTP에서 `MCP-Protocol-Version` **헤더가 없는 요청**을 어느 리비전으로 간주할지(TS `webStandardStreamableHttp.js:473`)다. 상세 근거·정정문은 `factcheck_log.md` C-1·C-2. 이 문서를 재사용하는 후속 실행은 §1-4·§5-3-2 대신 이 주석을 따르라.
>
> **§7-B-7은 해소됐다** — `@McpTool`은 `org.springframework.ai:spring-ai-mcp-annotations`(서버 스타터 전이 의존) 소속이고, Spring AI 2.0.0은 `<mcp.sdk.version>2.0.0</mcp.sdk.version>`으로 Java SDK를 고정한다 (spring-ai `v2.0.0` 태그 빌드 파일 실측).
