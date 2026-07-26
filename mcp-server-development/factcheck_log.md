# 팩트체크 로그 — MCP 서버 개발 (tech-book)

> **검증 시점: 2026-07-26.** 라운드 1 = 1~12장 초안 전수 검증.
> **대조 기준:** `01_reference.md`(§1~§8) + `research/{web,papers,community,web_supplement}.md`
> **웹/1차 에스컬레이션:** 레퍼런스로 판정 불가한 Critical 주장 + 자기탐지 의심 항목에 한해 패키지 tarball·wheel 직접 해제, GitHub Contents API(태그 고정), arXiv abs 원문, 레지스트리/npm/PyPI API를 **직접 실행**해 판정했다.

**판정 등급**

| 등급 | 의미 | 처리 |
|---|---|---|
| ✅ | 근거 일치 | 통과 |
| ❌ | 오류 — 1차 소스와 불일치 | **Phase 4 BLOCKING.** 정정문대로 고쳐야 Phase 4 종료 |
| ⚠️ | 부분 오류·주의 | 정정 권고 (저술가 판단 여지 있음) |
| 🕒 | 신선도 경고 | **Phase 5 이월 게이트.** EPUB 빌드 직전 재조회 |

> **게이트 분리.** **Phase 4 종료 기준은 ❌ 8건뿐이다.** 🕒 1건은 스펙 정식화(2026-07-28)가 저술 이후에 일어나므로 Phase 4에서 해소할 수 없다 — **EPUB 빌드 직전(Phase 5)에 오케스트레이터/epub-builder가 처리하는 이월 게이트**로 둔다(§12장 🕒 참조).

---

## 총괄 판정 (라운드 1)

| 장 | ❌ | ⚠️ | 🕒 | 비고 |
|---|---|---|---|---|
| 1장 | 0 | 0 | 0 | 전 주장 재검증 통과 |
| 2장 | **1** | 1 | 0 | 협상 fallback 서술 오류(3곳) |
| 3장 | 0 | 0 | 0 | API 주장 4건 1차 실측 전부 통과 |
| 4장 | 0 | 0 | 0 | — |
| 5장 | **3** | 1 | 0 | `(사실 확인 필요)` 해소 + 봉투/fallback 오류 |
| 6장 | **2** | 1 | 0 | `(사실 확인 필요)` 해소 + 전제 오류 |
| 7장 | **1** | 1 | 0 | 논문 수치 방향 오류 |
| 8장 | 0 | 0 | 0 | 버전·수치 전건 일치 |
| 9장 | 0 | 1 | 0 | Dockerfile 예제 축약 |
| 10장 | **1** | 0 | 0 | 1.x 보안 헬퍼 부존재 단정 오류 |
| 11장 | 0 | 0 | 0 | — |
| 12장 | 0 | 1 | **1** | 미확인 서술 해소 + 정식화 재확인 |
| **합계** | **8** | **7** | **1** | ❌=Phase 4 게이트 · 🕒=Phase 5 이월 |

**`(사실 확인 필요)` 마커 2건 — 전부 해소됨** (5장 → §5-F1, 6장 → §6-F1). 미해소 마커 0건.

**버전 4축 혼동 전수 점검 (요청 항목 2).** 12개 초안 전문에서 **한 문장·한 표 칸에 서로 다른 축의 버전 사실이 묶인 곳**을 훑었다. 결과는 대체로 양호하다 — 1장의 4축 표와 71행("Java·Spring AI는 GA다 / TS·Python은 프리릴리스였다 / 같은 2.0이라도 구현 스펙이 다르다"를 각각 따로 세운 대목), 6장 5~7행(`2.0.0`과 `2025-11-25`를 한 문장에서 만나게 해놓고 곧바로 축을 갈라 설명), 9장 151행(`server.json` `2025-12-11`을 네 번째 축으로 재확인), 12장 71·77행이 모두 축을 정확히 분리한다. 5장 160행도 TS·Python을 한 문장으로 묶지 말라는 레퍼런스 지침을 그대로 이행한다.
**적발된 축 혼동은 1건**이다 — 10장 31행이 "이 API는 SDK **2.0 계열**에서 확인됐다"는 **SDK semver 축**의 관측을, "그러니 1.x에는 없다"는 **기능 존부 판정**으로 넘겨짚었다(→ **C-8**). 축을 섞은 결과가 곧 사실 오류가 된 사례라 별도 항목으로 세우지 않고 C-8에 통합했다.

---

## Critical 정정 목록 (BLOCKING — 8건)

| # | 장 | 한 줄 요약 | 근거 |
|---|---|---|---|
| C-1 | 2장 | "협상 실패 시 `2025-03-26`으로 낙착"은 **틀렸다.** initialize 실패 시 서버는 **LATEST(`2025-11-25`)**로 응답한다 | TS `server/index.js:274`, PY `server/session.py:186` |
| C-2 | 5장 | 위와 같은 서술의 5장 재기술(11행) | 동일 |
| C-3 | 5장 | `(사실 확인 필요)` 해소 — 예외를 던지면 SDK가 `isError` 봉투로 감싼다 | `lowlevel/server.py:589`, `tools/base.py:117` |
| C-4 | 5장 | "클라이언트에게는 **배열 그대로**가 간다" → SDK가 `{"result": [...]}`로 감싼다 | `func_metadata.py:126`(1.28.1)·`:138`(2.0.0b2) |
| C-5 | 6장 | `(사실 확인 필요)` 해소 — `@McpTool` 메서드의 예외는 `CallToolResult(isError=true)`로 변환된다 | spring-ai `v2.0.0` `SyncMcpToolMethodCallback.java:92` |
| C-6 | 6장 | "없다는 상황을 표현할 자리가 시그니처 어디에도 없다" → 반환 타입을 `CallToolResult`로 두면 그대로 통과한다 | 동 태그 `AbstractMcpToolMethodCallback.java:168` |
| C-7 | 7장 | "도구 개수 중앙값이 **3분의 1로** 줄었다" → 초록은 "**by one-third**"(3분의 1**만큼** 감소) | arXiv 2507.16044 초록 원문 |
| C-8 | 10장 | "1.x에 동등한 Host/Origin 헬퍼가 있는지 확인하지 못했다" → **1.29.0에 실재한다** | `dist/esm/server/middleware/hostHeaderValidation.d.ts` 외 |

---

## 1장

### 라운드 1 — ❌0 / ⚠️0 / 🕒0

**✅ 확인됨**

- `schema/` 디렉토리 = `2024-11-05`·`2025-03-26`·`2025-06-18`·`2025-11-25`·`draft` 5개 — **팩트체크 시점 재조회로 동일 확인**. `2026-07-28/` 여전히 부재.
  근거: `gh api repos/modelcontextprotocol/modelcontextprotocol/contents/schema`(2026-07-26 실행)
- `2026-07-28-RC`가 여전히 `prerelease: true` (게시 2026-05-29). 릴리스 태그 전수에 `2.0` 없음.
  근거: Releases API 실행 결과 `2026-07-28-RC prerelease=true`
- `JSONRPC_VERSION = "2.0"`은 JSON-RPC 버전 — 01_reference.md 최상단 §, §1-2와 일치
- 네 축 관측값 표 — **전 항목 팩트체크 시점 재조회 통과**: npm dist-tags `{latest: '1.29.0'}` / PyPI `mcp` `1.28.1` / `claude --version` = `2.1.220` / `codex --version` = `codex-cli 0.145.0` / Agent SDK TS `0.3.220`·PyPI `0.2.128` / 레지스트리 `GET /v0/servers` HTTP 200
- SDK 2.0 성숙도 표(Java 2.0.0 GA 06-11 / Spring AI 2.0.0 GA 06-12 / TS `2.0.0-beta.5` 07-21 / Python `2.0.0b2` 07-14) — §"MCP 2.0" 표와 일치
- "TS beta.5의 `SUPPORTED_PROTOCOL_VERSIONS`에 `2026-07-28` 부재, 문자열 210회는 전부 JSDoc" — 01_reference.md 결정적 증거 블록과 일치
- Python `MODERN_PROTOCOL_VERSIONS = ("2026-07-28",)` — §1-4 및 `mcp-types` 실측과 일치
- HN 스레드 수치 460/375(04-10), 447/284(03-01), 400/410(05-29) 및 "2~5월 넉 달 연속" — §4-1 표와 일치
- 영문·국문 인용 4건(0x696C6961 / bb88 / ejholmes / kaydash) — **원문 대조 결과 문자열 일치**(기계 대조, 아래 §부록)

**판정:** 이 장에 정정 사항 없음. 1장이 세운 "관측으로 쓴다" 규율 자체가 팩트체크를 가장 쉽게 통과한 장이다.

---

## 2장

### 라운드 1 — ❌1 / ⚠️1 / 🕒0

**❌ 정정 필요 (C-1, BLOCKING)**

> **수정 범위 주의 — 이 장의 오프닝(3~5행)이 정정 대상의 일부다.** 아래 네 곳만 고치면 **1장 도입부가 여전히 틀린 장면을 제시한 채로 남고**, 73행이 그것과 다른 이야기를 설명하게 된다. 오프닝부터 함께 고쳐야 한다.

- **[원문 3~5행 오프닝]** "최신 스펙을 지원한다는 SDK를 받아서 서버를 띄웠다. 그런데 로그를 열어보니 협상된 프로토콜 버전이 `2025-03-26`이라고 찍혀 있다. … 버그가 아니다. 그렇게 동작하도록 만들어진 것이고, 심지어 SDK 코드에 상수로 박혀 있다."
  → **두 겹으로 틀렸다.** (1) 그 상수는 협상 결과를 정하지 않는다(아래 근거). (2) 이 현상은 **Streamable HTTP 전용**인데, 이 시점 러닝 예제는 **stdio**다. **stdio 서버로는 오프닝의 장면 자체가 관측되지 않는다.**
  **[정정 방향]** 둘 중 하나를 고른다 — ⓐ 장면을 "원격(Streamable HTTP)으로 띄운 서버의 요청 로그"로 명시하거나, ⓑ 질문을 "협상이 왜 어긋났나"에서 **"이 `2025-03-26`이라는 값은 대체 어디서 오는가"**로 바꾼다. ⓑ가 73행의 정정문과 자연스럽게 이어진다.
- **[원문 73행]** "세 번째 상수, 협상이 어긋났을 때 떨어지는 기본값은 최신이 아니라 **`2025-03-26`**이다. Python SDK `1.28.1`도 같은 값을 쓴다."
  **[원문 85행 그림 2]** `A -.->|"버전 제안이 없거나 해석할 수 없는 경우"| I["기본값 2025-03-26으로 낙착"]`
  **[원문 90행]** "양쪽 중 한쪽이 버전을 제대로 싣지 못하면 조용히 두 세대 전으로 떨어진다."
  **[원문 147행 핵심]** "협상 실패 시 기본값은 최신이 아니라 `2025-03-26`이다."

  **근거 (1차 실측, 레퍼런스 §1-4·§5-3-2를 반증):**
  - TS `@modelcontextprotocol/sdk@1.29.0` `dist/esm/server/index.js:274`
    ```js
    const protocolVersion = SUPPORTED_PROTOCOL_VERSIONS.includes(requestedVersion)
        ? requestedVersion : LATEST_PROTOCOL_VERSION;
    ```
    → **클라이언트가 미지원 버전을 제안하면 서버는 `LATEST`(`2025-11-25`)로 응답한다.** `2025-03-26`이 아니다.
  - `DEFAULT_NEGOTIATED_PROTOCOL_VERSION`의 **전(全) 사용처는 단 한 곳**이다(`dist/esm` 전수 grep):
    `server/webStandardStreamableHttp.js:473` — `req.headers.get('mcp-protocol-version') ?? DEFAULT_NEGOTIATED_PROTOCOL_VERSION`.
    같은 파일 622행 `validateProtocolVersion()` 주석 원문: *"For HTTP requests without the MCP-Protocol-Version header: Accept and default to the version negotiated at initialization."*
    → 이 상수는 **Streamable HTTP에서 `MCP-Protocol-Version` 헤더가 없는 후속 요청에 적용되는 하위호환 가정값**이다. `initialize` 협상 경로에 전혀 관여하지 않는다.
  - Python `mcp==1.28.1`도 구조가 같다. `mcp/server/session.py:186`
    ```python
    requested_version if requested_version in SUPPORTED_PROTOCOL_VERSIONS else types.LATEST_PROTOCOL_VERSION
    ```
    그리고 상수 이름은 `DEFAULT_NEGOTIATED_PROTOCOL_VERSION`이 아니라 **`DEFAULT_NEGOTIATED_VERSION`**(`mcp/types.py:35`)이며, 사용처는 **`mcp/server/streamable_http.py` 뿐**(553·555·871·906행)이다.

  **[정정문]** (73행 대체)
  > 세 번째 상수는 성격이 다르다. `DEFAULT_NEGOTIATED_PROTOCOL_VERSION`은 **`initialize` 협상의 실패값이 아니라, Streamable HTTP에서 `MCP-Protocol-Version` 헤더 없이 들어온 요청을 어느 리비전으로 간주할지 정하는 하위호환 가정값**이다. 이 헤더는 `2025-06-18`에서 도입됐으니, 헤더를 안 보내는 클라이언트는 그 이전 세대라고 보고 `2025-03-26`으로 취급하는 것이다. Python SDK `1.28.1`도 같은 값을 같은 자리에 둔다(이름은 `DEFAULT_NEGOTIATED_VERSION`).
  >
  > 그러면 `initialize`에서 버전이 어긋나면 어떻게 될까? 서버는 자기가 아는 **최신**을 제시한다 — `SUPPORTED_PROTOCOL_VERSIONS`에 없으면 `LATEST_PROTOCOL_VERSION`으로 응답하고, 클라이언트가 그걸 못 받으면 연결이 끊긴다. 즉 **조용히 구버전으로 떨어지는 경로는 stdio 핸드셰이크가 아니라 HTTP 헤더 쪽에 있다.**

  **[정정문]** (그림 2) 점선 분기 라벨을 `"initialize 없이 온 HTTP 요청에<br/>MCP-Protocol-Version 헤더가 없으면"` → `"2025-03-26으로 간주 (하위호환)"`로 바꾸고, `B -->|"아니오"|` 경로의 서버 제시값을 **"서버가 자기 LATEST를 제시"**로 명시.

  **[정정문]** (147행 핵심) → "`MCP-Protocol-Version` 헤더가 없는 HTTP 요청은 `2025-03-26`으로 간주된다. '왜 구버전으로 붙지?'는 핸드셰이크가 아니라 이 헤더를 의심할 자리다."

  > ⚠️ **레퍼런스 자체의 오류다.** `01_reference.md` §1-4의 "협상 실패 시 fallback이 최신이 아니라 `2025-03-26`이다"와 §5-3-2가 근거였다. `[웹]` 등급 2차 서술이 `[검증]` 상수 열거와 섞여 들어간 것으로 보인다. research-lead·editor에 에스컬레이션한다.

**⚠️ 출처 없음/미표기**

- **[원문 11행]** > "MCP provides a JSON-RPC client-server interface for secure tool invocation and typed data exchange."
  인용문 자체는 §1-1과 **문자열 일치**한다(✅). 다만 본문은 "학계 쪽 정의"라고만 하고 출처를 밝히지 않는다. 영문 직접 인용에는 귀속이 필요하다.
  **[정정 권고]** "에이전트 프로토콜 서베이 한 편(arXiv 2505.02279)의 한 줄 규정이 훨씬 정확하다" 정도로 논문 식별자를 본문 또는 참고문헌에 노출.

**✅ 확인됨**

- TS 1.29.0 상수 3종 및 `SUPPORTED_PROTOCOL_VERSIONS` 5개 열거 — `dist/esm/types.js` 실측 일치 (Python은 4개로 `2024-10-07`이 없다 — 본문이 TS만 인용하므로 문제 없음)
- 버전 문자열 부등호 비교 금지 인용문(`"zzz" > "2025-11-25"`) — §1-4 원문과 **문자열 일치**
- 프리미티브 3종·메서드 이름 7종, 서버→클라이언트 4종 — §1-2와 일치
- 트랜스포트 3종 지위표 — §1-3과 일치
- `2025-11-25` 주요/부수 변경 목록(5건) — §2-2와 일치. SEP-1303 해석("모델의 자기교정") ✅
- stdio 약점 4종 — §1-3과 일치

---

## 3장

### 라운드 1 — ❌0 / ⚠️0 / 🕒0 · **3장↔5장 봉투 쟁점의 승자**

**✅ 확인됨 (전부 `@modelcontextprotocol/sdk@1.29.0` tarball 직접 해제로 실측)**

- **[49행]** "SDK `1.29.0`은 zod 3과 4를 모두 받아준다"
  → `package.json` `peerDependencies.zod = "^3.25 || ^4.0"`, `dependencies.zod = "^3.25 || ^4.0"` ✅ **VERIFIED**. 예제의 `"zod": "^3.25"`도 정합.
- **[95행]** `registerTool` 설정 객체 필드 = `title`·`description`·`inputSchema`·`outputSchema`·`annotations`·`_meta`, 전부 선택
  → `dist/esm/server/mcp.d.ts:150-157`에 **정확히 이 6개, 전부 `?`** ✅ **VERIFIED** (누락·초과 없음)
- **[101행]** "`outputSchema`를 선언하면 `structuredContent`를 반드시 함께 돌려줘야 한다"
  → `mcp.js` `validateToolOutput()`: `if (!result.structuredContent) throw new McpError(... "has an output schema but no structured content was provided")` ✅ **VERIFIED**
- **[101행]** "와이어 위의 `structuredContent`는 객체이지 배열이 아니다"
  → `dist/esm/types.js:1302` `structuredContent: z.record(z.string(), z.unknown()).optional()` / `:1472` `z.object({}).loose().optional()` ✅ **VERIFIED**. **5장 131행의 반대 서술이 틀린 쪽이다(C-4).**
- **[138행]** `ResourceTemplate`의 `{ list: undefined }`를 "SDK가 명시적으로 요구한다"
  → `mcp.d.ts:225-229`, 타입은 `list: ListResourcesCallback | undefined`(옵셔널 아님) + JSDoc 원문 *"This is required to specified, even if `undefined`, to avoid accidentally forgetting resource listing."* ✅ **VERIFIED** — 본문의 "친절한 강제" 해석까지 원문이 뒷받침한다
- **[196행]** "SDK는 `isError`가 붙은 결과에 대해 `outputSchema` 검증을 건너뛴다"
  → `validateToolOutput()` 본문 `if (result.isError) { return; }`가 `structuredContent` 검사보다 **앞에** 있다 ✅ **VERIFIED**
- **[176행]** 입력 검증 오류를 Tool Execution Error로 (SEP-1303) — SDK 구현도 정합: `CallToolRequestSchema` 핸들러가 `McpError`를 잡아 `createToolError()`(=`isError: true`)로 변환한다(`UrlElicitationRequired`만 예외적으로 재던짐)
- **[13·202~210행]** dist-tags `latest: 1.29.0` 단일, README의 v1 프로덕션 라인·6개월 약속, v2 패키지 분해·Standard Schema·`serveStdio`·`WebStandardStreamableHTTPServerTransport`·beta.5의 `2026-07-28` 미협상 — §3-1 및 팩트체크 시점 npm 재조회와 일치
- **[218행]** `claude mcp add team-wiki -- node /절대/경로/build/index.js` — §3-6 공식 help 문법과 일치

---

## 4장

### 라운드 1 — ❌0 / ⚠️0 / 🕒0

**✅ 확인됨**

- `claude mcp add [options] <name> -- <command> [args...]`, `--` = "passed to the server untouched" — §3-6·§8-B와 일치
- 옵션표(`-s/--scope` 기본 `local`, `-t/--transport` `stdio|sse|http`, `-e`, `-H`, OAuth 3종 + `MCP_CLIENT_SECRET`) — §3-6 실측과 일치
- `type` 필드의 `streamable-http` → `http` 별칭 — §3-6과 일치
- **스코프 5단계**(local→project→user→플러그인→claude.ai 커넥터), 3스코프는 이름 매칭·플러그인/커넥터는 엔드포인트 매칭 — §8-G와 일치
- 인용 > "The entire server entry from that source is used; **fields are not merged across scopes.**" — §8-G 원문과 **문자열 일치**
- 저장 위치 표 + 읽지 않는 경로 3종 + `%USERPROFILE%` — §8-B 부수 수확과 일치
- `local` 기본값이 "저장소 루트, git이 아니면 그 디렉터리"에 묶임 — §3-6 quickstart 원문과 일치
- v2.1.154(Pending approval)·v2.1.196(자기승인 차단)을 **별개 릴리스로 분리 서술** — 신선도 원장 버전 매핑과 일치 (drift 없음)
- `"timeout": 600000`, HTTP/SSE 첫 바이트 60초, 지수 백오프 최대 5회·1초 2배, stdio 자동 재연결 없음 — §3-6과 일치
- Desktop: 메뉴 바 경고 인용, Developer→Edit Config, 완전 재시작, macOS/Windows 경로, **Linux 경로 없음**, `command`·`args`·`env` 3필드, 보안 경고 인용, Connectors(망치 아이콘은 구표현) — §8-F와 일치. 인용 2건 문자열 일치
- `.mcpb` 설치 3경로, DXT→MCPB 개명, **2차 배포 경로**임을 명시 — §8-F와 일치 (권장 배포로 오독될 여지 없음)
- Agent SDK 4형태(외부 3 + 인프로세스 1), `createSdkMcpServer`/`create_sdk_mcp_server`, 0.x 릴리스 주기 주의 — §3-6과 일치
- Codex CLI 서브커맨드 6종·`~/.codex/config.toml` — §3-6과 일치
- 파편화 사례 3건(#66262 PATH 상속 / #74768 DCR `client_name` 403 / #77388 양쪽 "연결됨") — §4-4와 일치. 날짜 표기 정확

---

## 5장

### 라운드 1 — ❌3 / ⚠️1 / 🕒0

### §5-F1. `(사실 확인 필요)` 마커 해소 (C-3, BLOCKING)

**[원문 89행 마커]** "1.28.1의 FastMCP에서 도구 함수의 예외를 SDK가 감싸주는지, 결과 객체를 직접 구성해야 하는지 — 은 레퍼런스에서 확인되지 않았다."

**판정: 해소.** `mcp==1.28.1` wheel을 직접 해제해 확인했다. **두 경로 모두 성립하며, 권장 경로는 "예외를 던지는 것"이다.**

1. **예외를 던지면 SDK가 감싼다.**
   - `mcp/server/fastmcp/tools/base.py:116-117` — 도구 함수에서 나온 예외를 `ToolError(f"Error executing tool {self.name}: {e}")`로 감싼다.
   - `mcp/server/lowlevel/server.py:589-590` — `except Exception as e: return self._make_error_result(str(e))`
   - `:473-479` `_make_error_result()` = `CallToolResult(content=[TextContent(type="text", text=error_message)], isError=True)`
   → **`raise ValueError("...")` 한 줄이면 Tool Execution Error 봉투가 된다.** 프로토콜 에러로 새지 않는다. 입력/출력 스키마 검증 실패도 같은 경로로 `isError` 결과가 된다(`:538`, `:568-575`).
2. **결과 객체를 직접 구성해도 된다.**
   - `mcp/server/fastmcp/utilities/func_metadata.py:114-117` — 도구가 `CallToolResult`를 반환하면 변환 없이 그대로 통과시킨다. `lowlevel/server.py:546` 도 `isinstance(results, types.CallToolResult)`면 그대로 `ServerResult`로 싣는다.
   → 안내 문구를 완전히 통제하고 싶으면 `types.CallToolResult(isError=True, content=[TextContent(...)])`를 반환하면 된다.

**[정정문]** (89행 마커 블록을 삭제하고 아래로 대체)

> 다행히 SDK가 이 자리를 이미 마련해두었다. `mcp` 1.28.1에서 **도구 함수가 예외를 던지면 SDK가 그것을 `isError: true` 결과로 감싸서 내보낸다.** FastMCP가 예외를 `ToolError("Error executing tool wiki_get: …")`로 감싸고, 그 아래 저수준 서버가 그것을 잡아 `CallToolResult(isError=True)`로 바꾼다. 즉 프로토콜 에러로 새지 않는다.
>
> ```python
> @mcp.tool()
> def wiki_get(path: str) -> str:
>     """주어진 경로의 문서 본문을 돌려준다."""
>     doc = store.read(path)
>     if doc is None:
>         raise ValueError(f"'{path}' 문서를 찾을 수 없다. wiki_search로 경로를 먼저 확인하라.")
>     return doc
> ```
>
> 단, 모델에게 도달하는 텍스트는 **예외 메시지 그 자체**다. 그러니 메시지에 다음 행동을 적어 넣어야 3장에서 손으로 조립하던 그 안내와 같은 값을 한다. 문구를 완전히 통제하고 싶다면 `types.CallToolResult(isError=True, content=[...])`를 직접 반환해도 된다 — SDK가 이 경우 변환 없이 그대로 실어 보낸다.

### ❌ 정정 필요 (C-4, BLOCKING) — structuredContent 봉투

**[원문 131행]** "모델에게는 … 요약 텍스트가 가고, 클라이언트에게는 **배열 그대로**가 간다."

**근거 (3장↔5장 쟁점의 최종 판정, 1차 실측):**
- 와이어 스펙: `structuredContent`는 **객체**다 — TS `types.js:1302` `z.record(z.string(), z.unknown())`. 배열은 실을 수 없다.
- Python SDK가 **자동으로 감싼다**: `func_metadata.py` — `wrap_output`가 참이면 `result = {"result": result}`.
  - 1.28.1: `:125-126`, 2.0.0b2: `:137-138` (동일 동작)
  - `:213` 주석 원문 — *"Generic types (list, dict, Union, etc.) - wrapped in a model with a 'result' field"*
  → `wiki_search(...) -> list[dict]`의 구조화 출력은 **`{"result": [{...}, …]}`**로 나간다.
- 3장의 `{ results }` 수동 래핑은 **같은 제약에 대한 수동 대응**이며 3장 101행 서술이 옳다.

**[정정문]** (131행 후반부 대체)
> …모델에게는 "세 건을 찾았고 제목은 이렇다"는 요약 텍스트가 가고, 클라이언트에게는 타입이 살아 있는 구조화 데이터가 간다. 한 가지 알아둘 게 있다. **구조화 출력은 와이어 위에서 반드시 객체다.** 그래서 `list[dict]`를 돌려주면 SDK가 말없이 `{"result": [...]}`로 한 겹 감싸서 내보낸다. 3장에서 우리가 `{path, title}` 배열을 `results` 키로 직접 감쌌던 것과 정확히 같은 제약이고, 다만 TypeScript에서는 손으로, Python에서는 SDK가 대신 한다는 차이다. 키 이름이 `results`가 아니라 `result`가 된다는 것도 함께 기억해두자 — 클라이언트를 짜는 사람에게는 이 한 글자가 계약이다.

### ❌ 정정 필요 (C-2, BLOCKING) — 협상 fallback

**[원문 11행]** "이 라인이 지원하는 스펙 리비전은 `2025-11-25`, **협상 실패 시 기본값은 `2025-03-26`**이다."
근거·정정 방향은 **2장 C-1과 동일**. Python 1.28.1은 `DEFAULT_NEGOTIATED_VERSION`(이름 다름)을 `server/streamable_http.py`에서만 쓰고, `session.py:186`의 initialize 경로는 미지원 요청에 `LATEST_PROTOCOL_VERSION`을 응답한다.
**[정정문]** "…지원하는 스펙 리비전은 `2025-11-25`이고, `MCP-Protocol-Version` 헤더 없이 들어온 Streamable HTTP 요청은 `2025-03-26`으로 간주한다(2장 참고)."
(전 장 grep 결과 이 서술의 재기술은 **2장 4곳 + 5장 11행이 전부**다. 다른 장에는 없다.)

**⚠️ 인용 범위 주의 — SEP-1303을 넓게 적용했다**

**[원문 81행]** "`2025-11-25` 리비전이 **SEP-1303에서 정리한 내용이 정확히 이것이다** — 입력 검증 오류는 …"
SEP-1303은 레퍼런스 §2-2 기준 **"입력 검증 오류(input validation error)"**에 대한 규정이다. 그런데 러닝 예제의 상황은 "형식은 맞지만 실재하지 않는 경로"이므로 **스키마 검증 실패가 아니라 조회 실패**다. 처방(`isError`로 돌려주기)과 근거(모델의 자기교정)는 그대로 전이되지만, **"정확히 이것이다"는 인용 범위를 넘는다.** 6장 116행도 같은 취지를 반복한다(3장 176행은 오류 유형을 특정하지 않아 상대적으로 안전하다).
**[정정 권고]** "SEP-1303이 입력 검증 오류에 대해 정한 원칙인데, 조회 실패에도 같은 논리가 그대로 통한다" 정도로 **확장 적용임을 밝히고 단정을 완화**한다. 코드·수치 변경은 없다.

**✅ 확인됨**

- `mcp` `info.version` = **1.28.1** (팩트체크 시점 PyPI 재조회 일치), 2.x는 프리릴리스 5개(a1→a2→a3→b1→b2), `requires-python >=3.10`
- `uv init`/`uv venv`/`uv add "mcp[cli]"`, **로컬 개발은 `uvx`가 아니라 `uv run`**, 클라이언트 등록의 `--directory <절대경로>` — §8-B와 일치 (가장 정확하게 옮긴 대목)
- FastMCP 1.x 데코레이터 4종 + 시그니처·docstring·타입 힌트에서 계약을 읽는다는 서술 — §3-2 및 wheel 실측과 일치
- `FastMCP` → `MCPServer` 개명: **wheel 문자열 0건 재확인**(`grep -ril fastmcp mcp-2.0.0b2` → 결과 없음) + `docs/migration.md` 원문 인용 문자열 일치. `from mcp.server import MCPServer`가 실제 export임도 확인(`mcp/server/__init__.py:4`) ✅
- 2.0.0b2 튜토리얼 예제 원문, "That's the whole API." / "Type hints … the contract." 인용 — §8-E와 문자열 일치
- 2.0 파괴적 변경 표 8행, `httpx`→`httpx2`, `opentelemetry-api` 하드 의존성 승격 — §8-E와 일치
- `mcp-types` 세대 상수 3종 — §1-4와 일치
- "Do not use v2 in production. … v1.x is the only stable release line" 인용 + `mcp>=1.27,<2` 상한 + v2 목표일 2026-07-27 — §8-E와 일치 (하루 차이의 이유를 지어내지 않은 점 ✅)
- 별개 패키지 `fastmcp` 3.4.4, `Optional[X]` 스키마 소실(#56263) — §3-2·§5-1과 일치

---

## 6장

### 라운드 1 — ❌2 / ⚠️1 / 🕒0

### §6-F1. `(사실 확인 필요)` 마커 해소 (C-5, BLOCKING)

**[원문 122행 마커]** "Spring AI의 `@McpTool` 메서드에서 예외를 던졌을 때 프레임워크가 Tool Execution Error로 감싸주는지, 별도 반환 타입을 써야 하는지 — 은 레퍼런스에서 확인되지 않았다."

**판정: 해소.** 공식 문서(`docs.spring.io/.../mcp-annotations-server.html`)는 예외 처리를 **다루지 않는다**(전문 조회로 확인된 부정 발견). 그래서 구현체를 **`spring-projects/spring-ai` 태그 `v2.0.0`에 고정해** 직접 읽었다.

`mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/method/tool/SyncMcpToolMethodCallback.java` (ref=`v2.0.0`)
```java
@Override
public CallToolResult apply(McpSyncServerExchange exchange, CallToolRequest request) {
    validateSyncRequest(request);
    try {
        Object[] args = this.buildMethodArguments(exchange, request.arguments(), request);
        Object result = this.callMethod(args);
        return this.processResult(result);
    }
    catch (Exception e) {
        if (this.toolCallExceptionClass.isInstance(e)) {
            return this.createSyncErrorResult(e);      // ← Tool Execution Error
        }
        throw e;
    }
}
```
- 기본 생성자가 `toolCallExceptionClass`를 **`Exception.class`**로 넘긴다(`:42-44`) → **모든 예외가 대상**이다.
- `AbstractSyncMcpToolMethodCallback.createSyncErrorResult()` (ref=`v2.0.0`, `:62-67`)
  ```java
  Throwable rootCause = findCauseUsingPlainJava(e);
  return CallToolResult.builder().isError(true)
      .addTextContent(e.getMessage() + System.lineSeparator() + rootCause.getMessage()).build();
  ```
  → 모델이 받는 텍스트는 **`예외 메시지 + 줄바꿈 + 루트 원인 메시지`**다.

**[정정문]** (122행 마커 블록 삭제 후 대체)
> 다행히 프레임워크가 이 자리를 이미 메워준다. Spring AI 2.0.0의 `@McpTool` 처리기는 메서드에서 나온 **예외를 잡아 `CallToolResult`의 `isError`를 켜서 돌려준다.** 대상 예외 타입의 기본값이 `Exception`이니 사실상 전부다. 모델이 읽게 되는 텍스트는 `예외 메시지 + 루트 원인 메시지`이므로, 메시지 자체에 다음 행동을 적어두면 세 언어가 똑같은 결과에 도달한다.
>
> ```java
> @McpTool(name = "wiki_get", description = "주어진 경로의 문서 본문을 돌려준다")
> public String wikiGet(@McpToolParam(description = "문서 경로", required = true) String path) {
>     String body = store.read(path);
>     if (body == null) {
>         throw new IllegalArgumentException(
>             "'" + path + "' 문서를 찾을 수 없다. wiki_search로 경로를 먼저 확인하라.");
>     }
>     return body;
> }
> ```

### ❌ 정정 필요 (C-6, BLOCKING) — "표현할 자리가 없다"는 전제

**[원문 118행]** "`@McpTool`이 붙은 메서드의 **반환 타입이 곧 도구의 성공 결과**다. 위의 `wikiGet`은 `String`을 돌려주게 돼 있고, '문서가 없다'는 상황을 **표현할 자리가 시그니처 어디에도 없다.** 그러니 자바 개발자의 손은 자연스럽게 예외로 간다 … 여기서는 **기존 습관이 반대 방향으로 잡아당긴다.**"

**근거:** `AbstractMcpToolMethodCallback.convertValueToCallToolResult()` (ref=`v2.0.0`, `:168-170`)
```java
if (result instanceof CallToolResult) {
    return (CallToolResult) result;
}
```
→ **메서드 반환 타입을 `CallToolResult`로 두면 그대로 통과한다.** 즉 (a) 예외 던지기, (b) `CallToolResult` 직접 반환 — **두 자리가 다 있다.** 게다가 (a)는 프레임워크가 공식적으로 지원하는 경로이므로, "습관이 반대 방향으로 잡아당긴다"는 진단은 **사실 관계가 뒤집혀 있다.** 자바 개발자의 예외 습관은 여기서 **정답 쪽**이다.

**[정정문]** (118행 문단 재구성 방향 — 문장 다듬기는 저술가 재량)
> 그런데 JVM에서는 이 결정이 눈에 잘 안 띈다. `@McpTool`이 붙은 메서드의 반환 타입이 곧 도구의 성공 결과라서, `String`을 돌려주는 `wikiGet`의 시그니처만 봐서는 실패를 어디에 실을지 보이지 않는다. 3장의 TypeScript에서는 반환 객체를 손으로 조립하느라 이 선택이 코드에 드러났고, 5장의 Python에서는 한 겹 감춰져 있었다면, 여기서는 **애너테이션 뒤로 완전히 들어가 있다.** 실은 자리가 둘이나 있는데도 그렇다 — 예외를 던지거나(프레임워크가 `isError`로 감싼다), 반환 타입을 `CallToolResult`로 두고 직접 조립하거나. 반가운 소식은 자바 개발자가 십 년 넘게 길들여진 그 습관, 그러니까 **예외를 던지는 쪽이 여기서는 정답**이라는 것이다.

### ⚠️ 출처 갱신 필요

**[원문 79행]** "`@McpTool`이 어느 아티팩트에 들어 있는지, Spring AI 2.0.0이 어떤 java-sdk 버전을 고정하는지는 **확인하지 못했다.**"
→ **둘 다 확인됐다** (§7-B-7 해소):
- 아티팩트: **`org.springframework.ai:spring-ai-mcp-annotations`** (`mcp/mcp-annotations/pom.xml`). `spring-ai-starter-mcp-server`의 `pom.xml`이 이것을 의존으로 선언하므로 **스타터를 넣으면 따라 들어온다**(별도 의존성 추가 불필요).
- 패키지: **`org.springframework.ai.mcp.annotation.McpTool`** (ref=`v2.0.0`에 파일 존재 확인). ※ 커뮤니티 인큐베이터 리포(`spring-ai-community/mcp-annotations`)는 `org.springaicommunity.mcp.annotation`을 쓰므로 **옛 블로그의 import를 그대로 베끼면 안 된다**는 주의가 오히려 유용하다.
- 고정 버전: 루트 `pom.xml`(ref=`v2.0.0`) `<mcp.sdk.version>2.0.0</mcp.sdk.version>` → `io.modelcontextprotocol.sdk:mcp-bom:2.0.0`.
**[정정 권고]** 79행을 위 세 사실로 교체하고, "IDE 자동 완성으로 확인하라"는 조언은 커뮤니티 패키지와의 혼동 주의로 바꾼다.

**✅ 확인됨**

- Java SDK 2.0.0 릴리스 노트 인용 2건("General Availability …", "Streamable HTTP first: SSE transports are now deprecated") — §3-3과 **문자열 일치**
- 좌표·경로(M1→M2 05-13→M3 05-21→RC1 06-04→2.0.0 06-11)·병행 유지 라인(1.1.3, 0.18.3) — §3-3과 일치
- 파괴적 변경 3종(#928 필수 필드, #873 입력 검증, #749 `JsonSchema` 제거→`Map`) + `MIGRATION-2.0.md` — §3-3과 일치
- Spring AI 2.0.0 = Java SDK **바로 다음 날**(06-12), `spring-ai-bom` 2.0.0 — §3-4와 일치
- **스타터 5개**(서버 3 + 클라이언트 2)와 **7행 프로토콜 매트릭스**, "WebMVC용 Streamable 스타터는 없다", STATELESS 인용 — §3-4와 일치 (레퍼런스가 가장 강조한 정정을 정확히 반영)
- `@McpTool`/`@McpToolParam` 계산기 예제 및 속성(`name` 기본=메서드명, `title` 우선순위, `generateOutputSchema` 기본 `false`), `@McpResource` — §3-4와 일치
- 124행 "JVM 진영은 논문도 커뮤니티 논의도 없다" — §7-A-11과 일치 (정직한 한계 표시)

---

## 7장

### 라운드 1 — ❌1 / ⚠️1 / 🕒0

**❌ 정정 필요 (C-7, BLOCKING)**

**[원문 59행]** "같은 연구에서 필터링과 재그룹화만으로 **API당 도구 개수 중앙값이 3분의 1로 줄었다.**"

**근거:** arXiv 2507.16044 초록 원문(abs 페이지 직접 조회, 2026-07-26):
> "…automated repair raises this to 94.2%, while filtering and regrouping **reduce the median tool count per API by one-third**."

**"by one-third" = 3분의 1만큼(약 33%) 감소**다. "3분의 1로 줄었다"는 67% 감소를 뜻하므로 감소폭을 두 배로 부풀린 서술이 된다. (레퍼런스 §5-7과 `research/papers.md:280`의 "1/3 감소"라는 축약 표기가 오독을 유발한 것으로 보인다.)

**[정정문]** "같은 연구에서 필터링과 재그룹화만으로 API당 도구 개수 중앙값이 **3분의 1 줄었다**."
(또는 오독 여지를 아예 없애려면 "…중앙값을 **3분의 1만큼 감소**시켰다.")

**⚠️ 정정 권고 — 최상급의 주어가 바뀌었다**

**[원문 105행, 「이 장의 핵심」]** "거부율은 **최고 성능 모델**조차 3% 미만이었다."

**근거:** MCPTox 초록 원문 — *"agents rarely refuse these attacks, with the **highest refused rate** (Claude-3.7-Sonnet) less than 3%"*. 3% 미만이 붙는 주어는 **"거부율이 가장 높았던 모델"**이지 "성능이 가장 좋은 모델"이 아니다. `research/papers.md` N-8도 이 논문에 **순위 주장을 붙이지 말라**고 명시적으로 경고한다.
본문 87행("거부율은 가장 높은 모델조차 3% 미만이었다")은 옳다 — **핵심 요약에서만 드리프트가 났다.**

**[정정문]** "거부율은 **가장 잘 거부한 모델조차** 3% 미만이었다."

**✅ 확인됨 (논문 수치 전건을 arXiv 초록 원문으로 재대조)**

- 2507.16044: 공식 서버 **116개**, **88.6%** REST 기반, **92%** bare API wrapper, **중앙값 19%** 노출, "명세로부터 예측 가능한 체계적 패턴" — 초록 원문과 일치 ✅
- 2605.24660: BFCL **370개** 도구에서 평균 **7개** 제시 vs 50개 제시 → **90.3% vs 90.8%** ✅ / ToolBench **3,251개**에서 고정 5개가 총 커버리지 **64.7% vs 61.9%**이지만 *"finds nothing on hard queries"* ✅ / 하류 검증 **93.1% vs 87.1%**, 중난도 **76.8% vs 60.9%** ✅ — 전부 초록 원문과 일치. **"tool 100개면 정확도 13%" 류 금지 수치는 원고에 없다** ✅
- 2508.14925 (MCPTox): 실서버 **45개**·실도구 **353개**·에이전트 **20종**, **o1-mini 72.8%**로 정확히 귀속(순위 주장 없음) ✅, 인용문 *"more capable models are often more susceptible…"* **문자열 일치** ✅, AAAI-26 게재 표기 ✅
- 2510.16558: **67,057개** 서버 / 6개 레지스트리 / 취약 **833개** / 의심 설명 **18건**, *"Code-level vulnerabilities … are not required but can amplify"* ✅, DSN 2026 표기 ✅
- 2506.13538: 오픈소스 **1,899개**, **7.2%** 일반 취약점, **5.5%** tool poisoning, **8종 중 3종만** 전통적 취약점과 겹침 ✅ — **A-2/A-3 혼동 없음**(N-8 규정 준수)
- 2506.01333 (ETDI) 인용 맥락(승인을 도구 정의 해시에 묶기) ✅ / 생애주기 4단계(A-1) ✅
- **arXiv 식별자 5건 전수 실측**: 2507.16044·2605.24660·2510.16558·2506.13538·2506.01333 → abs 페이지 `citation_title`이 참고문헌 제목과 **전부 일치**. 미래 YYMM·해석 불가 식별자 **0건** ✅
- 컨텍스트 비용 절: 0xbadcafebee 인용("150 * 50, or 7500 tokens…") 문자열 일치, 79k/36k/20k·59.4k·"2025년 9월 이슈", newdps 인용, "deferred loading 이전 데이터" 반박 — §4-2와 일치. **도입 시점과 85% 수치를 단정하지 않았다** ✅ (§7-B-8 차단선 준수)

---

## 8장

### 라운드 1 — ❌0 / ⚠️0 / 🕒0

**✅ 확인됨 (버전·수치 밀도가 가장 높은 장인데 drift 0건)**

- #81268: **10,780→2,048자(81% 손실)**, 절단 **502건**, Anthropic 자체 커넥터 포함, 2026-07-26 작성·v2.1.220·open, `/mcp`가 원문을 보여줌 — §5-1과 일치. 인용문 *"the server is never told it happened…"* **문자열 일치**
- v2.1.144 페이지네이션 도구 드롭 / #56263 `Optional[X]`(2026-05-05, open) / #77296 16KB(2026-07-13) / #43968 헤드리스 무신호(2026-04-05) / v2.1.219 공백 경고 — 전부 §5-1·§5-3·신선도 원장과 일치
- v2.1.181 `! Connected · tools fetch failed` 및 "✓ Connected는 핸드셰이크 성공일 뿐" — §5-1과 일치
- #80996 인용(*"functionally deaf while looking alive from the outside"*)과 *"~15 min penalty per event"* — §3-7-6과 **문자열 일치**
- stdout 함정: 에러 3종 문자열, `[2m` ANSI 힌트, 래퍼 스크립트·`.zshrc` 원인, 제안 문구 인용 — §5-2와 **문자열 일치**. v2.1.208 stderr 64MB 누수 ✅
- Inspector **1.0.0 (2026-07-18)**, 직전 0.22.0(2026-06-04) — §5-4와 일치. **팩트체크 시점 npm 재조회 `1.0.0` 확인** ✅
- 로그 경로 2종(Claude Code JSONL / Desktop `mcp.log`·`mcp-server-*.log`), `tail -n 20 -f`, Desktop 트러블슈팅 5단계 — §5-4·§8-F와 일치
- `--debug` 출력 3줄, `-32000: Connection closed` — §5-4와 **문자열 일치**
- `--safe-mode`(v2.1.169), `--strict-mcp-config`, #68375(서버 11개 → 68초 초과 행 → 1개 시 약 5초) — §5-4·§3-7-7과 일치
- 타임아웃 표 5행(v2.1.206·212·187·162 + `MCP_SERVER_CONNECTION_BATCH_SIZE`, 틀린 이름 반증 언급) — §5-5와 **버전 전건 일치**
- 관찰성: span 계층 `session → task → turn → tool.call`, stdio 헤더 부재, `OTEL_LOG_TOOL_DETAILS=1`(v2.1.157), `/usage`(v2.1.149), 최대 7배(v2.1.208), Python 2.0 `opentelemetry-api` 하드 의존성 — §5-6과 일치
- "관찰성은 공격의 사후 탐지 수단"(E-1) — §5-6 논지와 일치

---

## 9장

### 라운드 1 — ❌0 / ⚠️1 / 🕒0

**⚠️ 주의 — Dockerfile 예제가 축약형임이 표시되지 않았다**

**[원문 98~112행]** 코드 블록에 `WORKDIR`·`ADD . /app`·의존성 캐시 마운트가 빠져 있어 **그대로 복사하면 빌드되지 않는다.** 공식 원문(`servers/src/fetch/Dockerfile`, 직접 조회)은 다음을 포함한다.
```dockerfile
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev --no-editable
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev --no-editable
```
**[정정 권고]** 블록 첫 줄에 "핵심만 남긴 축약형이다 — 전문은 공식 리포의 `src/fetch/Dockerfile`" 한 줄을 달거나, `WORKDIR /app` + `ADD . /app` 두 줄을 넣어 최소 실행 가능 형태로 만든다. (사실 오류는 아니지만 독자가 복사하는 코드다.)

**✅ 확인됨 (공식 리포 원문 직접 조회로 재검증)**

- quickstart `package.json` 실물 4포인트 — `modelcontextprotocol/quickstart-resources`에서 직접 조회: `"type": "module"` ✅ / `"bin": {"weather": "./build/index.js"}` ✅ / `"files": ["build"]` ✅ / `"build": "tsc && node -e \"require('fs').chmodSync('build/index.js', '755')\""` ✅ / deps `^1.24.3` ✅ (원고가 버전만 관측값으로 바꿨다고 명시한 점 ✅)
- **"공식 예제의 `bin` 타깃에 셔뱅이 없다"** — `src/index.ts` 1행이 `import { McpServer } …` ✅ **VERIFIED**. "베끼기 전에 `npx`로 확인하라"는 권고까지 정확
- `npm publish` 흐름과 **스코프 패키지 `--access public`** 분리 서술 ✅ (§3-8과 일치, 비스코프 예제에 불필요한 플래그를 넣지 않음)
- `uvx` = `uv tool run` 별칭, 패키지명≠커맨드명이면 `--from` 필요, `[project.scripts]` 키=배포명, 공식 서버 2건(`src/fetch`·`src/git`)·`hatchling`·`>=3.10` — §8-B와 일치
- **"Claude Code 공식 문서에 `uvx` 리터럴 예시가 없다"**는 부정 발견과 "그 한 줄은 문법에 대입한 것이지 문서의 예시가 아니다"라는 귀속 — §8-B 지침을 정확히 이행 ✅
- Dockerfile 패턴 요소 전건 일치(빌드 `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` / 런타임 `python:3.12-slim-bookworm` / `UV_COMPILE_BYTECODE=1` / `UV_LINK_MODE=copy` / `uv sync --locked --no-dev --no-editable` / `ENTRYPOINT ["mcp-server-fetch"]` / 레이어 캐싱 주석 원문) ✅ — 원문 대조 완료
- **종료 지시자 "7개 중 6개가 `ENTRYPOINT`, `CMD`는 데모 서버 하나"를 측정치로 서술** — §8-C의 "권장 규정 없음" 지침을 정확히 이행 ✅
- Node 4건 패턴(`node:22.12-alpine`→`node:22-alpine`, `NODE_ENV=production`, `npm ci --ignore-scripts --omit-dev`, `dist/`만 복사) ✅
- `docker run -i --rm mcp/fetch`, `-t` 미사용, **해설이 필자 서술임을 괄호로 표시** ✅ (§8-C 지침 이행). `docker mcp` 창작 커맨드 **0건** ✅
- Docker Hub `mcp/` 공개 리포 **245개**(2026-07-26 실측) ✅
- 레지스트리: 메타데이터만 호스팅 → 패키지 먼저, 게시 6단계, 소유권 마커 타입별 차이(npm `mcpName` / PyPI·NuGet README `mcp-name:`), `server.json` 필수 필드, 인증 4종, `validate`·`status`는 문서에만, **`$schema` = `2025-12-11`** — §8-D와 일치 ✅
- 레지스트리 preview 경고 ✅ / `.mcpb` 4단계·`manifest.json` 유일 필수·`server.type = "uv"`·**2차 배포 경로 명시** ✅ (MCPB `MANIFEST.md` 필드를 열거하지 않은 점도 §8-H 준수)

---

## 10장

### 라운드 1 — ❌1 / ⚠️0 / 🕒0

**❌ 정정 필요 (C-8, BLOCKING)**

**[원문 31행]** "`validateHostHeader`·`validateOriginHeader` 같은 헬퍼는 **SDK 2.0 계열에서 확인된 API**다 … **1.x로 만들었다면 Host·Origin 검증은 트랜스포트 앞단에서 직접 해야 한다.** … 1.x에 동등한 헬퍼가 있는지 없는지는 **이 책이 확인하지 못했으므로 단정하지 않는다.**"

**근거 (`@modelcontextprotocol/sdk@1.29.0` tarball 직접 해제):** 1.x에 **동등 이상의 수단이 이미 있다.**
1. **트랜스포트 옵션 3종** — `dist/esm/server/webStandardStreamableHttp.d.ts:84-96`
   ```ts
   allowedHosts?: string[];
   allowedOrigins?: string[];
   enableDnsRebindingProtection?: boolean;  // "requires allowedHosts and/or allowedOrigins"
   ```
   그리고 `dist/esm/server/streamableHttp.d.ts:20` — `export type StreamableHTTPServerTransportOptions = WebStandardStreamableHTTPServerTransportOptions;`
   → **Node용 `StreamableHTTPServerTransport`에서도 그대로 쓸 수 있다.** `SSEServerTransportOptions`(`sse.d.ts:15-29`)도 동일 3종을 갖는다.
2. **Express 미들웨어** — `dist/esm/server/middleware/hostHeaderValidation.d.ts`: `hostHeaderValidation(allowedHostnames: string[])`, `localhostHostValidation()`. JSDoc 원문: *"Express middleware for DNS rebinding protection. … This is particularly important for servers without authorization or HTTPS, such as localhost servers or development servers."*
3. **앱 팩토리** — `dist/esm/server/express.d.ts`: `createMcpExpressApp({ host, allowedHosts })`. JSDoc 원문: *"When the host is '127.0.0.1', 'localhost', or '::1' (the default is '127.0.0.1'), DNS rebinding protection middleware is automatically applied."*

**[정정문]** (31행 문단 대체)
> 여기서 버전 계열을 못 박고 가자. 이름은 계열마다 다르지만 **v1 라인에도 방어 수단이 이미 들어 있다.** `1.29.0` 기준으로 Streamable HTTP·SSE 트랜스포트가 `allowedHosts`·`allowedOrigins`·`enableDnsRebindingProtection` 세 옵션을 받는다.
>
> ```ts
> const transport = new StreamableHTTPServerTransport({
>   sessionIdGenerator: () => randomUUID(),
>   enableDnsRebindingProtection: true,
>   allowedHosts: ['localhost', '127.0.0.1', '[::1]'],
>   allowedOrigins: ['https://wiki.example.com']
> });
> ```
>
> Express를 쓴다면 `hostHeaderValidation(['localhost', '127.0.0.1', '[::1]'])` 미들웨어를 얹거나, 아예 `createMcpExpressApp()`으로 앱을 만들면 된다 — 후자는 localhost에 바인딩할 때 DNS rebinding 방어를 **자동으로** 켠다. SDK 2.0 계열의 `validateHostHeader`·`validateOriginHeader`는 같은 방어를 함수 단위로 노출한 것이다. **미들웨어를 손으로 짜기 전에 쓰는 SDK의 트랜스포트 옵션부터 확인하자.**

**✅ 확인됨**

- `Mcp-Session-Id` 기반 세션(`2025-11-25`까지) → RC에서 제거, 서버 발급 핸들을 일반 도구 인자로 — §2-3·§3-8과 일치
- `mcp.run(transport="streamable-http")` — §3-2 FastMCP API와 일치
- Spring AI `protocol=STREAMABLE` / `STATELESS`와 *"microservices architectures and cloud-native deployments"* 인용 — §3-4와 일치
- 잘못된 Origin에 HTTP 403 — §2-2·§3-8과 일치
- `2025-11-25` OAuth 3종(OIDC Discovery·incremental scope consent·Client ID Metadata Documents) — §2-2와 일치
- v2.1.196 `scopes_supported` 전량 요청 → GitLab self-hosted `invalid_scope` — §4-7과 **인용 맥락 일치**
- OAuth 실패 표 4건(#67291 2026-06-11 / #47390 2026-04-13 빈 User-Agent / #44652 / #67999) — §4-7과 일치. **날짜 미상 항목을 "—"로 비워둔 처리 정확** ✅
- RC의 DCR deprecated → Client ID Metadata Documents — §2-3과 일치
- **CVE-2025-49596**: CVSS **9.4**, 2025-07 공개, Inspector **0.14.1 미만**, 인증 부재 + "0.0.0.0 Day" + CSRF 체이닝 → 워크스테이션 RCE — §4-3과 일치. 이후 `1.0.0`(2026-07-18)까지 왔다는 서술도 ✅
- v2.1.161(시크릿 출력)·v2.1.196(자기승인)·v2.1.207(`headersHelper` 셸 인젝션) — 신선도 원장 버전 매핑과 일치

---

## 11장

### 라운드 1 — ❌0 / ⚠️0 / 🕒0

**✅ 확인됨 — 이 장은 "불확실성을 그대로 서술하는" 처리가 특히 정확하다**

- `agent-intern` README 경고 인용(*"This runs unsandboxed code with your privileges." … "no usable approval gate"*) — §3-7과 일치. **생략 표시(…)로 두 조각을 이었음이 드러난다** ✅
- 패턴 A/B 분리와 표면 4종(`claude mcp add`/`codex mcp add`, `claude mcp serve`/`codex mcp-server`, `claude -p`/`codex exec`) — §3-7 실측표와 일치
- 구현체 3개와 상태: `steipete/claude-code-mcp` **1,313⭐ 아카이브**(마지막 푸시 2026-05-15) / `grahama1970/claude-code-mcp-enhanced` **125⭐** 14개월 방치(2025-05-20) / `SinanTufekci/agent-intern` **16⭐** 활발(2026-07-24) — §3-7과 일치
- **"정착된 실무 관행이 아니다"**로 프레이밍 — §7-A-8 지침 이행 ✅
- 함정 #1(샌드박스 비상속, `--dangerously-skip-permissions`, `codex exec`의 `sandbox` 기본 `read-only`만 실제 경계, `workspace`는 시작 컨텍스트) — §3-7과 일치
- 함정 #2: **"일부 래퍼 구현의 기본 타임아웃이 3,600초"로 귀속을 좁히고 "업계 규범으로 읽지 말라"는 단서를 붙임** — 원 근거(`CLAUDE_CLI_TIMEOUT_SECONDS`)보다 보수적 ✅
- 함정 #3 출력 규약 4종, #4 `HOME` 경합, #5 무신호(*"zero signal"* 취지 + `tools: 70` → `tools: 22, mcp_servers: []`), #7 서버 11개 행/약 5초 — §3-7과 일치
- **번호를 리서치 문서 번호에 맞춰 유지(#6 결번)하고 그 사실을 45행에서 밝힘** — 추적성 확보 ✅
- "비용 폭발·무한 재귀 보고 0건, 동기는 오히려 쿼터 차익거래" — §7-A-9와 일치 (반직관 발견을 뒤집지 않았다)

---

## 12장

### 라운드 1 — ❌0 / ⚠️1 / 🕒1

**⚠️ 정정 권고 — 이제 확인된 사항**

**[원문 71행]** "다만 Spring AI가 어느 java-sdk 버전을 고정하는지는 **이 책이 1차 소스로 확인하지 못했으니**, 여기서 근거로 삼는 것은 Java SDK 쪽 명시다."
→ 확인됨: `spring-projects/spring-ai` 태그 `v2.0.0`의 루트 `pom.xml`에 **`<mcp.sdk.version>2.0.0</mcp.sdk.version>`**, 이 값으로 `io.modelcontextprotocol.sdk:mcp-bom`을 임포트한다.
**[정정문]** "…그리고 Spring AI 2.0.0의 빌드 파일은 `mcp-bom`을 **2.0.0**으로 고정한다. 즉 Spring AI 2.0.0 → Java SDK 2.0.0 → 스펙 `2025-11-25`로 사슬이 끝까지 이어진다. 숫자가 크다고 최신 스펙이 아니라는 말의 가장 깔끔한 증거다."
(6장 79행과 동일 근거이므로 **두 장을 같이 고친다.**)

**🕒 신선도 경고 (Phase 5 이월 게이트 — Phase 4 블로커 아님)**

**팩트체크 시점(2026-07-26) 재조회 결과 RC 상태는 그대로다:**
- `schema/` = `2024-11-05`·`2025-03-26`·`2025-06-18`·`2025-11-25`·`draft` → **`2026-07-28/` 여전히 없음**
- Releases API → `2026-07-28-RC`, `prerelease: true` (published 2026-05-29)
- npm `@modelcontextprotocol/sdk` dist-tags → `{ latest: '1.29.0' }` (2.x 정식 없음)
- PyPI `mcp` → `1.28.1` (2.x 정식 없음)

**그러나 정식 예정일이 이틀 뒤(2026-07-28)다.** 원고는 이미 관측 시점을 명기해 서술하고 있어(7행·71행·75행) **문장이 즉시 거짓이 되지는 않는다.** 다만 EPUB 빌드 직전에 아래 4개를 한 번 더 조회하고, 상태가 바뀌었다면 해당 문장을 관측형으로 갱신할 것을 권고한다.

| 재확인 대상 | 커맨드 | 영향 장 |
|---|---|---|
| `schema/2026-07-28/` 생성 여부 | `gh api repos/modelcontextprotocol/modelcontextprotocol/contents/schema` | 1·12 |
| RC의 `prerelease` 플래그 | `gh api repos/modelcontextprotocol/modelcontextprotocol/releases` | 1·10·12 |
| TS SDK 2.0 정식 여부 | `npm view @modelcontextprotocol/sdk dist-tags` | 1·3·12 |
| Python `mcp` 2.0 정식 여부 | `curl -s https://pypi.org/pypi/mcp/json` | 1·5·12 |

**✅ 확인됨**

- RC 3대 변경(세션 제거·`initialize` 제거 + `_meta` 봉투·`server/discover` 서버 MUST/클라이언트 MAY) — §2-3과 일치
- 곁가지 정리(`ping`·`logging/setLevel` 제거, 로그 레벨 `_meta`, `subscriptions/listen` 통합, tasks 코어 밖 확장·폴링, MRTR, `resultType` 필수·생략 시 `"complete"`, SSE 재개 제거) — §2-3과 일치
- **"changelog 수준까지만 확인했으므로 `server/discover` 예제를 지어내지 않는다"** — §7-B-5 지침 이행 ✅
- Roots·Sampling·Logging deprecated + 공식 대체안 3종(도구 파라미터·리소스 URI·서버 설정 / LLM 공급자 API 직접 / stderr·OpenTelemetry) — §2-3과 일치
- sampling 강화(SEP-1577) → 한 리비전 뒤 폐기라는 진동과 양 관점 — §4-6과 일치
- RC 조각 4종(`traceparent`·`tracestate`·`baggage` / `ttlMs`·`cacheScope` / `tools/list` 결정적 순서 SHOULD / 에러코드 `-32000~-32019` 구현 정의·`-32020~-32099` 예약) — §2-3 minor와 일치
- RC 릴리스 노트 인용 *"SDKs will adopt this version at their own pace…"* — §최상단 경고 원문과 **문자열 일치**
- 최소 **12개월** deprecation 창(SEP-2596), Active/Deprecated/Removed 3상태 — §2-3과 일치
- Java SDK 2.0.0 GA가 `2025-11-25`를 명시한다는 증거 재사용 ✅ / SDK 티어링(SEP-1730) ✅
- MCP = "context-oriented × general-purpose" 사분면, 스택의 첫 단계, "MCP냐 A2A냐는 잘못된 질문" — §2-5와 일치

---

## 에스컬레이션

### E-1. 레퍼런스 자체의 오류 (research-lead·editor 대상)

`01_reference.md` **§1-4의 "협상 실패 시 fallback이 최신이 아니라 `2025-03-26`이다 (Python SDK 1.28.1도 동일)"** 와 **§5-3-2 "왜 구버전으로 붙지? — 협상 실패 fallback이 `2025-03-26`"** 는 1차 소스와 어긋난다.
- 실제: `DEFAULT_NEGOTIATED_PROTOCOL_VERSION`(TS) / `DEFAULT_NEGOTIATED_VERSION`(PY)은 **Streamable HTTP에서 `MCP-Protocol-Version` 헤더가 없을 때의 가정값**이고, `initialize` 협상 실패 시에는 양 SDK 모두 **`LATEST_PROTOCOL_VERSION`을 응답**한다.
- 원인 추정: 상수 열거(`[검증]`)에 2차 해석(`[웹]`)이 붙으면서 상수의 **용도**가 바뀌어 기록됐다.
- 조치: 레퍼런스 §1-4·§5-3-2에 정정 주석을 달아야 후속 재저술·재검수에서 같은 오류가 재발하지 않는다.

### E-2. 해소된 §7-B 항목 (레퍼런스 갱신 권고)

| §7-B 항목 | 상태 | 근거 |
|---|---|---|
| B-6 Python SDK 2.0 `MCPServer` 예제 | 이미 §8-E에서 해소 + **본 라운드에서 `from mcp.server import MCPServer` export 실측 재확인** | `mcp/server/__init__.py:4` |
| **B-7 `@McpTool` 소속 아티팩트 / Spring AI가 pin하는 java-sdk 버전** | **본 라운드에서 해소** | `spring-ai-mcp-annotations`, `<mcp.sdk.version>2.0.0</mcp.sdk.version>` (ref=`v2.0.0`) |

### E-3. 저술가 재량이 적용되지 않는 항목

C-1~C-8은 **사실 판정**이다. 스타일 왕복 3회 후 저술가 최종본 채택 규칙이 적용되지 않는다(하네스 v1.9.1 규정). **이 8건이 Phase 4의 종료 기준**이며, 🕒 1건은 Phase 5(EPUB 빌드 직전)로 이월된다. ⚠️ 7건은 정정 권고로, 저술가가 다른 표현을 택하더라도 사실이 유지되면 통과다.

---

## 부록 — 본 라운드에서 실행한 1차 검증 (재현 가능)

**패키지 직접 해제**
```bash
npm pack @modelcontextprotocol/sdk@1.29.0        # dist/esm 전수 grep
pip download mcp==1.28.1 --no-deps                # wheel 해제
pip download mcp==2.0.0b2 --pre --no-deps         # wheel 해제
```
- TS: `server/index.js:274`(협상), `server/webStandardStreamableHttp.js:473,622`(헤더 기본값), `server/mcp.js`(isError·outputSchema), `server/mcp.d.ts:150-157,222-236`(registerTool·ResourceTemplate), `types.js:1302,1472`(structuredContent), `package.json`(zod 범위), `server/middleware/hostHeaderValidation.d.ts`·`server/express.d.ts`·`server/sse.d.ts`(DNS rebinding)
- PY 1.28.1: `server/lowlevel/server.py:473,538,563,568,589`, `server/fastmcp/tools/base.py:116`, `server/fastmcp/utilities/func_metadata.py:114,125`, `server/session.py:186`, `types.py:35`, `shared/version.py`
- PY 2.0.0b2: `server/mcpserver/utilities/func_metadata.py:137`, `server/mcpserver/server.py:412`, `server/mcpserver/tools/base.py:172-181`, `server/__init__.py:4`, `grep -ril fastmcp` → 0건

**저장소 태그 고정 조회 (`gh api … ?ref=v2.0.0`)**
- `spring-projects/spring-ai`: `SyncMcpToolMethodCallback.java`, `AbstractSyncMcpToolMethodCallback.java`, `AbstractMcpToolMethodCallback.java`, `mcp/mcp-annotations/pom.xml`, `starters/spring-ai-starter-mcp-server/pom.xml`, 루트 `pom.xml`
- `modelcontextprotocol/servers`: `src/fetch/Dockerfile`
- `modelcontextprotocol/quickstart-resources`: `weather-server-typescript/package.json`, `src/index.ts`
- `modelcontextprotocol/modelcontextprotocol`: `contents/schema`, `releases`

**논문 원문 대조** — arXiv abs 페이지 5건의 `citation_title` + 초록 전문 직접 취득 (2507.16044 / 2605.24660 / 2508.14925 / 2510.16558 / 2506.13538)

**인용문 기계 대조** — 12개 초안의 25자 이상 영문 인용 전수를 추출해 `01_reference.md` + `research/*.md`와 정규화 비교. **패러프레이즈 드리프트 0건.** 검출된 차이는 문장 부호 2건(5장 99행·4장 109행에서 인용 부호 안에 마침표 추가)뿐으로, 의미 변화가 없어 지적 대상에서 제외했다.

**라이브 상태 재조회 (2026-07-26)** — `claude --version`(2.1.220) / `codex --version`(0.145.0) / `npm view @modelcontextprotocol/inspector version`(1.0.0) / `npm view @anthropic-ai/claude-agent-sdk version`(0.3.220) / PyPI `claude-agent-sdk`(0.2.128) / PyPI `mcp`(1.28.1) / npm `@modelcontextprotocol/sdk` dist-tags(`latest: 1.29.0`) / 레지스트리 `GET /v0/servers` → HTTP 200

---

# 라운드 2 검증 (2026-07-26) — `{NN}_final.md` 12개

**대상:** `chapters/01_final.md` ~ `12_final.md` (라운드 1 대상은 `*_draft.md`)
**방법:** ① C-1~C-8 정정 반영 여부를 초안 대비 diff로 확인 ② ⚠️ 6건 처리 확인 ③ 금지 마커 grep ④ **정정 과정에서 새로 생긴 사실 오류**를 SDK 실측·인용 기계 대조로 재검증

## 총괄 — 잔여 ❌ 0건

| 항목 | 결과 |
|---|---|
| **C-1 ~ C-8 (BLOCKING 8건)** | **전건 해소** |
| ⚠️ 6건 | **전건 처리** |
| 금지 마커 (`(사실 확인 필요)` / `[리서치 공백]` / `[미완성]` / `TODO`) | **12개 파일 0건** (grep 결과 무출력) |
| 정정 과정에서 새로 생긴 사실 오류 | **0건** (신규 주장 3건 추가 실측 후 통과) |
| 영문 인용 재대조 | 드리프트 **0건** (검출 20건 전부 한국어 산문·mermaid 라벨·코드 식별자 오탐) |
| **잔여 ❌** | **0** |
| **잔여 🕒** | **1** (12장 — Phase 5 이월, 변동 없음) |

> **라운드 1 총괄표 산술 정정:** ⚠️ 합계를 **7**로 적었으나 장별 합(2·5·6·7·9·12 각 1건)은 **6**이다. 실제 ⚠️는 6건이며 라운드 2에서 6건 전부 처리됐다. 판정 내용에는 영향이 없다.

## C-1 ~ C-8 해소 확인

| # | 장 | 해소 위치 | 확인 |
|---|---|---|---|
| C-1 | 2장 | 3~5행·73~77행·그림 2·93행·핵심 bullet | ✅ **오프닝까지 재작성됨.** 훅이 "협상이 어긋났다"에서 **"이 값이 어디서 와서 어디에 쓰이는가"**로 바뀌어(정정 방향 ⓑ) stdio/HTTP 불일치가 해소됐다. 75행이 헤더 부재 가정값임을 정확히 기술하고, 77행이 "미지원 제안 → 서버가 `LATEST` 제시"를 명시. 그림 2는 `B -->|아니오| F["서버가 자기 LATEST를 제시(2025-11-25)"]`와 **독립 노드** `J -.-> I["2025-03-26으로 간주(하위호환)"]`로 분리됨 |
| C-2 | 5장 11행 | ✅ "`MCP-Protocol-Version` 헤더 없이 들어온 Streamable HTTP 요청은 `2025-03-26`으로 간주한다(2장 참고)" — 정정문 그대로. 전 장 grep 결과 fallback 오기 **잔존 0곳** |
| C-3 | 5장 | 마커 삭제 + 검증된 메커니즘·코드 예제 삽입 | ✅ "예외를 던지면 SDK가 `isError: true`로 감싼다" + `ToolError("Error executing tool wiki_get: …")` 경유 설명 + `raise ValueError(...)` 예제 + `types.CallToolResult` 직접 반환 대안까지 반영 |
| C-4 | 5장 143행 | ✅ "구조화 출력은 와이어 위에서 반드시 객체다 … SDK가 말없이 `{"result": [...]}`로 한 겹 감싸서 내보낸다" + 3장의 `results` 수동 래핑과 **키 이름 한 글자 차이**까지 명시. **3장 101행은 원래 옳았고 그대로 유지됨** — 두 장의 서술이 이제 정합 |
| C-5 | 6장 | ✅ "Spring AI 2.0.0의 `@McpTool` 처리기는 예외를 잡아 `CallToolResult`의 `isError`를 켜서 돌려준다. 대상 예외 타입의 기본값이 `Exception`" + 텍스트 조합(`예외 메시지 + 루트 원인 메시지`) + `throw new IllegalArgumentException(...)` 예제 |
| C-6 | 6장 | ✅ "실은 자리가 둘이나 있는데도 그렇다 — 예외를 던지거나, 반환 타입을 `CallToolResult`로 두고 직접 조립하거나. … **예외를 던지는 쪽이 여기서는 정답**이다." 전제가 뒤집힌 서술("습관이 반대 방향으로 잡아당긴다")이 제거됐고, "애너테이션 뒤로 들어가 있다"는 **가시성** 논점만 남아 사실과 정합 |
| C-7 | 7장 59행 | ✅ "API당 도구 개수 중앙값이 **3분의 1만큼 감소**했다" — 초록의 "by one-third"와 일치 |
| C-8 | 10장 31~42행 | ✅ 전면 교체. `allowedHosts`·`allowedOrigins`·`enableDnsRebindingProtection` 코드 예제 + `hostHeaderValidation()`·`createMcpExpressApp()` + "2.0의 `validateHostHeader`는 같은 방어의 함수 단위 노출". **장 말미 체크리스트의 "v1이라면 직접 건 미들웨어" 문구도 함께 제거**돼 잔존 모순 없음 |

## ⚠️ 6건 처리 확인

| 장 | 항목 | 확인 |
|---|---|---|
| 2 | 학술 인용 무출처 | ✅ "에이전트 프로토콜을 다룬 서베이 한 편(**arXiv 2505.02279**)의 한 줄 규정" |
| 5 | SEP-1303 범위 과확대 | ✅ "엄밀히 말하면 지금 우리 상황은 조금 다르다. … 스키마 검증 실패가 아니라 조회 실패다. 그래도 같은 논리가 그대로 통한다" — 확장 적용임을 명시. 6장의 반복 인용은 SEP 번호를 빼고 원칙만 서술해 문제 소멸(finals grep: SEP-1303은 3·5장에만 등장) |
| 6 | 아티팩트·pin 미확인 | ✅ "`org.springframework.ai:spring-ai-mcp-annotations`", 패키지 `org.springframework.ai.mcp.annotation`, "서버 스타터가 의존으로 선언", "`io.modelcontextprotocol.sdk:mcp-bom:2.0.0`" + **커뮤니티 패키지(`org.springaicommunity.mcp.annotation`) 혼동 주의**까지 추가 |
| 7 | "최고 성능 모델조차 3% 미만" | ✅ 본문·핵심 bullet 모두 "**가장 잘 거부한 모델**(Claude-3.7-Sonnet)조차 3% 미만" |
| 9 | Dockerfile 축약 미표시 | ✅ "아래는 **구조가 보이도록 핵심만 남긴 축약형**이다 — 전문은 공식 리포의 `src/fetch/Dockerfile`" + `WORKDIR /app`·`ADD . /app`·2단계 `uv sync`(`--no-install-project` 포함) 추가로 **공식 원문 구조와 일치** |
| 12 | Spring AI pin 미확인 | ✅ "Spring AI 2.0.0의 빌드 파일은 `mcp-bom`을 **2.0.0**으로 고정한다. 즉 Spring AI 2.0.0 → Java SDK 2.0.0 → 스펙 `2025-11-25`로 사슬이 끝까지 이어진다" |

## 정정 과정에서 새로 생긴 주장 — 추가 실측 결과

정정부에서 **초안에 없던 사실 주장 3건**이 새로 들어왔다. 전부 1차 확인했다.

1. **[2장 93행]** "핸드셰이크가 어긋나면 **연결이 끊어지므로 어쨌든 눈에 보인다.** 반면 헤더가 빠진 HTTP 요청은 조용히 두 세대 전으로 처리된다."
   → ✅ **VERIFIED.** `@modelcontextprotocol/sdk@1.29.0` `dist/esm/client/index.js:304-305`
   ```js
   if (!SUPPORTED_PROTOCOL_VERSIONS.includes(result.protocolVersion)) {
       throw new Error(`Server's protocol version is not supported: ${result.protocolVersion}`);
   ```
   서버가 제시한 버전을 클라이언트가 못 받으면 **예외를 던진다** — 침묵하지 않는다. 대비 구도가 성립한다.
2. **[6장]** "서버 스타터가 이 아티팩트를 의존으로 선언하고 있어서 스타터를 넣으면 따라 들어온다."
   → ✅ **VERIFIED.** `starters/spring-ai-starter-mcp-server/pom.xml`에 `spring-ai-mcp-annotations` 의존 선언 확인.
3. **[9장]** 축약 Dockerfile에 추가된 `WORKDIR /app` / `RUN uv sync --locked --no-install-project --no-dev --no-editable` / `ADD . /app` 순서
   → ✅ **VERIFIED.** `modelcontextprotocol/servers` `src/fetch/Dockerfile` 원문과 **순서·플래그 일치**(원문은 캐시·바인드 마운트가 추가로 붙으며, 그 생략은 축약 고지로 커버됨).

**부가 관찰 (지적 아님):** 5장 87행 "모델에게 도달하는 텍스트는 **예외 메시지 그 자체**다"는 엄밀히는 `Error executing tool wiki_get: {메시지}` 형태로 접두사가 붙는다. **바로 앞 문장이 그 래핑 형식을 이미 보여주므로** 독자가 오해할 여지가 없어 정정 대상으로 세우지 않는다.

## 장별 잔여 카운트 (라운드 2 종료 시점)

| 장 | ❌ | ⚠️ | 🕒 |
|---|---|---|---|
| 1~11장 | 0 | 0 | 0 |
| 12장 | 0 | 0 | **1** (Phase 5 이월) |
| **합계** | **0** | **0** | **1** |

**판정: Phase 4 팩트체크 게이트 통과.** ❌ 잔여 0건, 미해소 마커 0건.
**Phase 5로 넘기는 것 1건** — EPUB 빌드 직전 §12장 🕒의 4개 조회(`schema/` 트리 · Releases `prerelease` 플래그 · npm dist-tags · PyPI `mcp`)를 실행하고, 상태가 바뀌었다면 1·3·5·10·12장의 관측 문장을 갱신한다. 원고가 전부 관측 시점을 명기해 서술하므로 **미갱신 시에도 문장이 거짓이 되지는 않는다.**
