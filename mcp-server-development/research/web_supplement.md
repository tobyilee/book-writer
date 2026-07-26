<!-- 검색 시점: 2026-07-26 기준 -->
<!-- 보강 리서치: 2026-07-26 — book-planner가 02_plan.md에서 에스컬레이션한 레퍼런스 공백 5건 (1차 소스 우선) -->

# 웹 리서치 보강: MCP 서버 개발 — 공백 5건

**전 항목 공통: 검색 2026-07-26 기준.**

## 등급 정의 (이번 보강 전용)

| 등급 | 의미 |
|---|---|
| **[검증]** | 1차 소스 원문을 `curl`/WebFetch로 **직접 열어** 인용했다. 인용문은 원문 그대로다 |
| **[2차]** | 블로그·요약·검색 스니펫 수준. 원문 미확인 |
| **[미확인]** | 조사했으나 확보 실패. 지어내지 않는다 |

> ⚠️ **48시간 절벽 경고.** §7-D가 지적한 대로 `2026-07-28` 스펙이 **이틀 뒤** 릴리스 예정이고, Python `mcp` 2.0.0 정식도 "alongside" 나온다고 SDK README가 명시한다. 아래 **항목 4의 모든 버전 표기는 `2.0.0b2`/2026-07-26 기준이며 2026-07-28에 바뀔 수 있다.** 팩트체크 시점에 재확인하라.

---

## 조사 요약

| # | 항목 | 확보 | 최고 등급 |
|---|---|---|---|
| 1 | `uvx`/`uv run` 공식 실행 커맨드 + `[project.scripts]` | ✅ | [검증] |
| 2 | MCP 서버용 Dockerfile 권장 패턴 + Docker MCP 카탈로그 | ✅ | [검증] |
| 3 | `mcp-publisher` 서브커맨드 시퀀스 + `server.json` 스키마 | ✅ | [검증] |
| 4 | Python SDK 2.0 `MCPServer` 공식 사용 예제 | ✅ | [검증] |
| 5 | Claude Desktop 로컬 MCP 서버 등록 절차 (+ `.mcpb`) | ✅ | [검증] |
| **보너스** | **스코프 우선순위 `local > project > user` (§7-B-1)** | ✅ | **[검증]** |

**2차 조사에서 추가 확보:** ① Claude Code 워크스루 페이지까지 확인해 `uvx` 부정 발견을 2페이지로 확증 ② Node Dockerfile 4개 전수 확인으로 **`ENTRYPOINT`/`CMD` 초기 판단을 정정**(2-C) ③ support.claude.com·claude.com/docs·`anthropics/mcpb`로 **`.mcpb` 전체 절차 확보**(5-H) ④ 두 공식 소스의 경로 분기 발견(5-I).

**5건 전부 1차 소스로 확보했다.** 계획서가 "명령어를 지어내지 말고 개념 수준으로만 서술하라"고 묶어둔 제약은 **해제 가능하다.**

---

## 자료 1: `uvx` / `uv run`으로 MCP 서버 실행하기

### 1-A. 공식 Python 퀵스타트는 `uvx`가 아니라 `uv run`을 쓴다 **[검증]**

- 출처: `modelcontextprotocol/modelcontextprotocol` 리포 `docs/docs/develop/build-server.mdx` (modelcontextprotocol.io "Build an MCP server" 문서의 소스)
- URL: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/build-server.mdx
- 확인 방법: `raw.githubusercontent.com`에서 원문 직접 취득 (2026-07-26)

프로젝트 셋업 원문 그대로:

```bash
# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create our server file
touch weather.py
```

Windows 탭은 `.venv\Scripts\activate`와 `uv add mcp[cli] httpx`(따옴표 없음), `new-item weather.py`로 다르다.

실행 커맨드 원문:

> "Your server is complete! Run `uv run weather.py` to start the MCP server, which will listen for messages from MCP hosts."

### 1-B. 클라이언트 등록 시엔 `uv --directory ... run` 형태 **[검증]**

같은 문서의 Claude Desktop 설정 블록 원문:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

문서가 직접 해설한다:

> "2. To launch it by running `uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/weather run weather.py`"

두 가지 공식 주의사항이 원문에 달려 있다 (책에 그대로 옮길 가치가 있다):

> "You may need to put the full path to the `uv` executable in the `command` field. You can get this by running `which uv` on macOS/Linux or `where uv` on Windows."

> "Make sure you pass in the absolute path to your server. ... On Windows, remember to use double backslashes (`\\`) or forward slashes (`/`) in the JSON path."

**→ 핵심 구분 (책에서 반드시 갈라야 할 지점):**
- **아직 배포 안 한 로컬 개발 중 서버** → `uv --directory <경로> run <파일>.py`
- **PyPI에 배포된 서버** → `uvx <패키지명>` (아래 1-C)

이 둘을 섞으면 독자가 바로 막힌다. 계획서 9장에서 이 분기를 명시하라.

### 1-C. 배포된 서버는 `uvx <패키지명>` **[검증]**

- 출처: `modelcontextprotocol/servers` 리포 README.md
- URL: https://github.com/modelcontextprotocol/servers/blob/main/README.md

원문:

> "Python-based servers in this repository can be used directly with [`uvx`](https://docs.astral.sh/uv/concepts/tools/) or [`pip`](https://pypi.org/project/pip/). `uvx` is recommended for ease of use and setup."

```sh
# With uvx
uvx mcp-server-git

# With pip
pip install mcp-server-git
python -m mcp_server_git
```

클라이언트 설정 예시(같은 README):

```json
"git": {
  "command": "uvx",
  "args": ["mcp-server-git", "--repository", "path/to/git/repo"]
}
```

Windows 관련 원문 주의 — **`uvx`는 래핑하지 않는다**는 게 명시돼 있다:

> "On Windows, apply the same wrapper to each `npx`-based entry above by changing `"command"` to `"cmd"` and prepending `"/c", "npx"` to the existing `args`. **Leave `uvx` entries unchanged.**"

### 1-D. `uvx`의 정체와 엔트리포인트 결정 규칙 **[검증]**

- 출처: uv 공식 문서 "Using tools"
- URL: https://docs.astral.sh/uv/guides/tools/

원문 인용:

> "`uvx` is provided as an alias for convenience." — `uvx ruff`는 "exactly equivalent to: `uv tool run ruff`"

패키지명과 커맨드명이 다를 때:

> "When `uvx ruff` is invoked, uv installs the `ruff` package which provides the `ruff` command. However, sometimes the package and command names differ."

이 경우 `--from`을 쓴다 (예: `httpie`가 제공하는 `http` 커맨드 → `uvx --from httpie http`).

⚠️ **[부분 미확인]** uv 문서는 `[project.scripts]` **엔트리포인트 해석 메커니즘을 명시적으로 설명하지는 않는다.** "패키지명 == 커맨드명이면 그대로 쓰고, 다르면 `--from`으로 지정한다"는 동작만 보여준다. 아래 1-E가 그 빈틈을 실물로 메운다.

### 1-E. `[project.scripts]` 규약 — 공식 서버 pyproject.toml 실물 **[검증]**

- 출처: `modelcontextprotocol/servers` `src/fetch/pyproject.toml`, `src/git/pyproject.toml`
- URL: https://github.com/modelcontextprotocol/servers/blob/main/src/fetch/pyproject.toml

`src/fetch/pyproject.toml` 원문 발췌:

```toml
[project]
name = "mcp-server-fetch"
version = "0.6.3"
requires-python = ">=3.10"

[project.scripts]
mcp-server-fetch = "mcp_server_fetch:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

`src/git/pyproject.toml`도 동일 패턴:

```toml
[project]
name = "mcp-server-git"
version = "0.6.2"

[project.scripts]
mcp-server-git = "mcp_server_git:main"
```

**여기서 읽히는 규약 (실물 2건 일치):**
1. **배포명(`name`)과 스크립트 키를 같게 둔다** — `mcp-server-fetch` = `mcp-server-fetch`. 그래야 `uvx mcp-server-fetch`가 `--from` 없이 동작한다 (1-D의 조건).
2. 스크립트 값은 `모듈명:함수` 형식이며, 모듈명은 **하이픈이 아니라 언더스코어** (`mcp_server_fetch:main`).
3. 빌드 백엔드는 두 서버 모두 `hatchling`.
4. `requires-python = ">=3.10"` — Python SDK의 최소 버전과 일치.

> 📌 **책에 쓸 규칙 한 줄:** "`uvx <이름>`으로 실행되게 하려면 `[project.scripts]`의 키를 배포 패키지명과 **똑같이** 두어라. 다르면 사용자가 매번 `--from`을 쳐야 한다."

### 1-F. `claude mcp add ... -- uvx ...` 리터럴 예시 — **[미확인 / 부정 발견]**

- 출처: Claude Code 공식 MCP 문서
- URL: https://code.claude.com/docs/en/mcp (구 `docs.claude.com/en/docs/claude-code/mcp`에서 **301 리다이렉트**)
- 확인 방법: WebFetch로 전문 취득 후 기계 검색

**측정 결과: 문서 전문에서 `uvx` 출현 0건.** (`grep -c -i "uvx"` → `0`)

**추가 확인 — 워크스루 페이지도 열었다.** 위 레퍼런스 페이지가 스스로 "This page is the full reference"라며 별도 워크스루를 가리키므로, 그쪽도 확인했다:

- URL: https://code.claude.com/docs/en/mcp-quickstart ("Connect to MCP servers")
- 결과: **`uvx`·`uv` 모두 출현 0건.** 로컬 stdio 서버 예시는 `npx`를 쓴다:

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

문서의 해설 원문:

> - "There's no `--transport` flag, because local servers use the default `stdio` transport."
> - "Everything after the `--` separator is the command Claude Code runs to start the server."
> - "`-y` tells `npx` to install the package without prompting."

**→ 부정 발견이 두 페이지(레퍼런스 + 워크스루)에서 확증됐다: Claude Code 공식 문서에 `uvx` 리터럴 예시는 없다.** Python 로컬 서버 예시 자체가 없고 전부 `npx` 기반이다. 지어내지 마라. 문서가 보증하는 것은 **일반 문법**이고, `uvx`는 거기에 대입하면 된다:

원문 그대로:

```bash
# Basic syntax
claude mcp add [options] <name> -- <command> [args...]

# Real example: Add Airtable server
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
```

`--` 구분자에 대한 공식 설명 원문:

> "**Important: Separate server arguments with `--`**
>
> For stdio servers, the `--` (double dash) separates Claude's own options, such as `--transport`, `--env`, and `--scope`, from the command and arguments that run the server. Everything after `--` is passed to the server untouched."

> - "`claude mcp add --transport stdio myserver -- npx server` → runs `npx server`"
> - "`claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080` → runs `python server.py --port 8080` with `KEY=value` in environment"

> "Without `--`, Claude Code would try to parse the server's flags, like `--port` above, as its own options."

`--env` 관련 함정도 원문에 있다 (실무 팁으로 쓸 만하다):

> "`--env` accepts multiple `KEY=value` pairs. If the server name comes directly after `--env`, the CLI reads the name as another pair and rejects it, so place at least one other option between `--env` and the server name."

**→ 저술 지침:** `claude mcp add --transport stdio weather -- uvx mcp-server-weather` 같은 문장을 쓸 수는 있으나, **"공식 문서의 예시"라고 귀속하지 마라.** "공식 문법에 `uvx`를 대입한 형태"로 정직하게 쓰거나, 문서에 실재하는 `npx`/`python` 예시를 그대로 인용하라.

### 1-G. stdio 서버에 주입되는 환경 변수 **[검증]**

같은 Claude Code 문서에서 부수 수확 — 9장에 유용하다:

> "Claude Code sets `CLAUDE_PROJECT_DIR` in the spawned server's environment to the project root, so your server can resolve project-relative paths without depending on the working directory. ... for example `process.env.CLAUDE_PROJECT_DIR` in Node or `os.environ["CLAUDE_PROJECT_DIR"]` in Python."

> "A server that limits its own filesystem access to a set of allowed directories should implement the MCP `roots/list` request instead. ... **Before v2.1.203**, `roots/list` returned only the launch directory and Claude Code didn't send `notifications/roots/list_changed`."

---

## 자료 2: MCP 서버용 Dockerfile 권장 패턴

### 2-A. 어떤 공식 서버가 Dockerfile을 갖고 있나 — 전수 열거 **[검증]**

- 방법: GitHub Trees API로 `modelcontextprotocol/servers` `main` 전체 트리를 열거 (경로 추측 아님)
- 명령: `curl -s "https://api.github.com/repos/modelcontextprotocol/servers/git/trees/main?recursive=1"`

**Dockerfile 보유 서버 전체 7개 (2026-07-26 기준):**

| 경로 | 언어 |
|---|---|
| `src/everything/Dockerfile` | Node |
| `src/fetch/Dockerfile` | Python |
| `src/filesystem/Dockerfile` | Node |
| `src/git/Dockerfile` | Python |
| `src/memory/Dockerfile` | Node |
| `src/sequentialthinking/Dockerfile` | Node |
| `src/time/Dockerfile` | Python |

**→ 부정 발견으로서 의미 있음:** 공식 리포에 남은 레퍼런스 서버는 **7개뿐**이고, Python 3 / Node 4로 갈린다. "공식 서버가 수십 개"라는 인상은 2026-07-26 기준 사실이 아니다.

### 2-B. Python 서버 Dockerfile — 3개가 완전히 동일한 템플릿 **[검증]**

`src/fetch/Dockerfile` 원문 전문:

```dockerfile
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev --no-editable

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=uv /root/.local /root/.local
COPY --from=uv --chown=app:app /app/.venv /app/.venv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# when running the container, add --db-path and a bind mount to the host's db file
ENTRYPOINT ["mcp-server-fetch"]
```

`src/git`, `src/time`도 **바이트 수준으로 사실상 동일**하고 차이는 딱 셋:
- `git`: 런타임 스테이지에 `RUN apt-get update && apt-get install -y git git-lfs && rm -rf /var/lib/apt/lists/* && git lfs install --system` 추가
- `time`: `ENV LOCAL_TIMEZONE=${LOCAL_TIMEZONE:-"UTC"}` 추가, `ENTRYPOINT ["mcp-server-time", "--local-timezone", "${LOCAL_TIMEZONE}"]`
- 각자의 `ENTRYPOINT` 실행 파일명

**→ 읽어낼 권장 패턴 6가지 (실물 3건 일치):**
1. **멀티스테이지** — 빌드는 `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`, 런타임은 순정 `python:3.12-slim-bookworm`. **uv는 최종 이미지에 남지 않는다.**
2. **`UV_COMPILE_BYTECODE=1`** — 콜드 스타트 단축. stdio 서버는 요청마다 프로세스를 띄우므로 실질 이득이 있다.
3. **`UV_LINK_MODE=copy`** — 캐시가 마운트 볼륨이라 하드링크가 안 먹히는 문제 회피.
4. **의존성과 프로젝트 소스를 나눠 설치** — 원문 주석이 이유를 직접 말한다: "Installing separately from its dependencies allows optimal layer caching".
5. **`--locked`** — 락파일 불일치 시 조용히 갱신하지 않고 실패. 재현성 보장.
6. **`ENTRYPOINT`는 `[project.scripts]`가 만든 실행 파일** — 1-E와 정확히 연결된다. `ENTRYPOINT ["mcp-server-fetch"]`가 동작하는 이유가 `[project.scripts]`의 `mcp-server-fetch = "mcp_server_fetch:main"`이다.

> 📌 **9장 서술 연결 고리:** 항목 1(`[project.scripts]`)과 항목 2(Dockerfile `ENTRYPOINT`)는 **같은 한 줄에 의존한다.** 따로 설명하지 말고 "엔트리포인트를 한 번 정의하면 `uvx`·`docker`·`pip` 세 배포 경로가 전부 그 이름을 쓴다"로 묶어라. 이게 이 장의 가장 좋은 구조적 통찰이다.

### 2-C. Node 서버 Dockerfile **[검증]**

`src/everything/Dockerfile` 원문 전문:

```dockerfile
FROM node:22.12-alpine AS builder

COPY src/everything /app
COPY tsconfig.json /tsconfig.json

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm npm install

FROM node:22-alpine AS release

WORKDIR /app

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/package-lock.json /app/package-lock.json

ENV NODE_ENV=production

RUN npm ci --ignore-scripts --omit-dev

CMD ["node", "dist/index.js"]
```

**Node 4개 전수 확인 결과** (filesystem·memory·sequentialthinking도 원문 취득):

공통 패턴 — 멀티스테이지 + `node:22.12-alpine`(빌드) / `node:22-alpine`(런타임) + `ENV NODE_ENV=production` + `npm ci --ignore-scripts --omit-dev`(공급망 관점에서 `--ignore-scripts`가 핵심) + `dist/`만 런타임 스테이지로 복사.

⚠️ **초기 판단 정정.** `src/everything` 하나만 보고 "Node는 `CMD`"라고 일반화했으나 **틀렸다.** 4개를 전수 확인한 실측:

| 서버 | 종료 지시자 | 빌더 스테이지의 `npm ci` |
|---|---|---|
| `src/everything` | **`CMD ["node", "dist/index.js"]`** | 없음 |
| `src/filesystem` | `ENTRYPOINT ["node", "/app/dist/index.js"]` | 있음 |
| `src/memory` | `ENTRYPOINT ["node", "dist/index.js"]` | 있음 |
| `src/sequentialthinking` | `ENTRYPOINT ["node", "dist/index.js"]` | 있음 |

**→ 정정된 결론: 7개 중 6개가 `ENTRYPOINT`를 쓴다** (Python 3 + Node 3). `CMD`는 `src/everything` **단 하나뿐인 예외**다. `everything`은 이름대로 모든 기능을 시연하는 데모 서버라 다른 6개보다 대표성이 낮다.

**→ 따라서 "공식 레퍼런스 서버의 지배적 패턴은 `ENTRYPOINT`"라고 쓸 수 있다** (6/7, 두 언어 모두). 다만 "공식 문서가 ENTRYPOINT를 **권장한다**"는 서술은 여전히 금지 — **명문 권장 규정은 어디에도 없고**, 이건 실물 관찰에서 나온 빈도 사실이다. 책에는 "공식 서버 7개 중 6개가 ENTRYPOINT를 쓴다"처럼 **측정치로** 써라.

`ENTRYPOINT`가 stdio 서버에 더 맞는 실질 이유: `docker run ... mcp/foo` 뒤에 붙는 인자가 `CMD`를 통째로 덮어쓰는 것과 달리 `ENTRYPOINT`는 인자로 **추가**되므로, `--repository` 같은 서버 옵션 전달이 자연스럽다(2-B의 `mcp-server-time` 예시가 정확히 이 형태). ※ 이 해설은 저술가 서술이며 1차 문서 명문이 아니다.

### 2-D. stdio 컨테이너 실행: `docker run -i --rm` **[검증]**

- 출처: `modelcontextprotocol/servers` `src/fetch/README.md`
- URL: https://github.com/modelcontextprotocol/servers/blob/main/src/fetch/README.md

원문 그대로 (Claude Desktop 설정):

```json
{
  "mcpServers": {
    "fetch": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/fetch"]
    }
  }
}
```

VS Code용도 같은 리포에 있고 `args`가 동일하다.

**`-i`가 필수인 이유** (책에서 반드시 설명할 것): stdio 트랜스포트는 컨테이너의 **stdin을 계속 열어둬야** 한다. `-i`(`--interactive`)가 없으면 stdin이 즉시 닫혀 서버가 첫 요청도 못 받고 죽는다. `-t`(TTY)는 **쓰지 않는다** — TTY를 붙이면 라인 버퍼링·에코가 JSON-RPC 프레이밍을 깨뜨린다. `--rm`은 클라이언트가 서버를 껐다 켤 때마다 죽은 컨테이너가 쌓이는 걸 막는다.

> ⚠️ 위 "`-i`/`-t` 동작 원리" 문단은 **1차 문서에 명문화된 설명이 아니라** 관찰된 커맨드(`-i --rm`, `-t` 부재)에 대한 기술적 해설이다. 책에 쓸 때 "공식 문서가 말하길"로 귀속하지 마라. 커맨드 자체는 [검증], 해설은 저술가 서술이다.

### 2-E. Docker MCP 카탈로그 (`mcp/` 네임스페이스) **[검증]**

**존재 여부 — Docker Hub API로 실측:**

```
curl -s "https://hub.docker.com/v2/repositories/mcp/?page_size=1"
→ {"count":245, ...}
```

**`mcp/` 네임스페이스는 실재하며 2026-07-26 기준 공개 리포지토리 245개.** 상위 항목 실측치:

| 이미지 | pull_count | 설명(API 원문) | last_updated |
|---|---|---|---|
| `mcp/fetch` | **1,718,376** | "Fetches a URL from the internet and extracts its contents as markdown" | 2026-07-07 |
| `mcp/time` | 839,028 | "Time and timezone conversion capabilities" | 2025-06-17 |
| `mcp/git` | 134,772 | "Git repository interaction and automation." | 2025-06-16 |

`date_registered`는 셋 다 **2024-12-19** — MCP 발표(2024-11-25) 약 한 달 뒤 Docker가 네임스페이스를 열었다는 뜻이다.

**카탈로그 공식 설명 [검증]** (https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/):

승인된 서버는 24시간 내에 "The [Docker Hub](https://hub.docker.com/u/mcp) `mcp` namespace (for MCP servers built by Docker)"에 올라간다.

> "Docker builds and signs all local servers in the catalog"

검증된 서버는 "full provenance and SBOM metadata"를 포함한다.

**사용법 [부분]:** 카탈로그 문서는 주로 **Docker Desktop GUI** 흐름을 안내한다 — "In Docker Desktop, select **MCP Toolkit**. Select the **Catalog** tab to browse available servers." CLI로 확인된 건 커스텀 카탈로그 가져오기 하나뿐:

```console
$ docker mcp catalog pull <oci-reference>
```

⚠️ **[미확인]** `docker mcp` CLI의 **전체 서브커맨드 목록**은 이 페이지에서 확인하지 못했다. 카탈로그 이미지를 굴리는 실질 경로는 2-D의 `docker run -i --rm mcp/<name>`이며 이건 [검증]됐다. `docker mcp run` 같은 커맨드를 **지어내지 마라.**

---

## 자료 3: `mcp-publisher` CLI + `server.json` 스키마

### 3-A. 소스 **[검증]**

- 리포: `modelcontextprotocol/registry` (GitHub Trees API로 `docs/` 전체 열거)
- 게시 가이드: `docs/modelcontextprotocol-io/quickstart.mdx`
- CLI 레퍼런스: `docs/reference/cli/commands.md`
- 스키마 원본: `docs/reference/server-json/draft/server.schema.json`
- URL: https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/cli/commands.md

> ⚠️ 계획서가 "publish-server.md"를 지목했으나 **그런 파일은 존재하지 않는다.** 실제 경로는 위 두 개다. (트리 전수 열거로 확인)

### 3-B. 레지스트리 상태 — 여전히 preview **[검증]**

퀵스타트 상단 Note 원문:

> "The MCP Registry is currently in preview. Breaking changes or data resets may occur before general availability."

→ §7-A-5("가동 중이나 GA 아님")를 **1차 문서로 재확인**했다.

### 3-C. 설치 **[검증]**

```bash
brew install mcp-publisher
```

바이너리 직접 설치(퀵스타트 원문):

```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/
```

`mcp-publisher --help` 출력 원문:

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

### 3-D. 전체 서브커맨드 — `--help`보다 많다 **[검증]**

`docs/reference/cli/commands.md`에는 `--help`에 안 나오는 **`validate`와 `status`가 문서화돼 있다.**

| 커맨드 | 용도 | `--help`에 노출 |
|---|---|---|
| `init` | `server.json` 템플릿 생성(패키지 매니저 자동 감지) | ✅ |
| `login <method>` | 인증 (`github`/`github-oidc`/`dns`/`http`/`none`) | ✅ |
| `validate [file]` | 게시 없이 검증 | ❌ |
| `publish [PATH]` | 레지스트리에 게시 | ✅ |
| `status --status <...>` | 게시된 서버 lifecycle 변경 | ❌ |
| `logout` | 저장된 인증정보 삭제 | ✅ |

전역 옵션: `--help`/`-h`, `--registry` (기본값 `https://registry.modelcontextprotocol.io`).

### 3-E. 실제 게시 시퀀스 6단계 **[검증]**

퀵스타트가 규정한 순서 (npm 기준, 원문 단계 제목 그대로):

1. **Step 1: Add verification information to the package** — npm이면 `package.json`에 `"mcpName": "io.github.my-username/weather"` 추가
2. **Step 2: Publish the package** — `npm publish --access public`. 원문: "The MCP Registry only hosts metadata, not artifacts, so we must publish the package to npm before publishing the server to the MCP Registry."
3. **Step 3: Install `mcp-publisher`**
4. **Step 4: Create `server.json`** — `mcp-publisher init`
5. **Step 5: Authenticate** — `mcp-publisher login github`
6. **Step 6: Publish** — `mcp-publisher publish`

> 📌 **책에서 강조할 반직관 포인트:** **패키지를 먼저 npm/PyPI에 올리고, 그 다음에 레지스트리에 등록한다.** 레지스트리는 **메타데이터만** 호스팅한다. 순서를 뒤집으면 소유권 검증에서 막힌다. 이게 초보가 가장 많이 틀리는 지점이다.

`login github` 출력 원문 (device flow):

```text
Logging in with github...

To authenticate, please:
1. Go to: https://github.com/login/device
2. Enter code: ABCD-1234
3. Authorize this application
Waiting for authorization...
```

`publish` 출력 원문:

```text
Publishing to https://registry.modelcontextprotocol.io...
✓ Successfully published
✓ Server io.github.my-username/weather version 1.0.1
```

검증 (원문):

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.my-username/weather"
```

### 3-F. `server.json` 실물 + 필수 필드 **[검증]**

`mcp-publisher init`이 생성하는 파일 원문:

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

**✅ 스키마 버전 교차 확인:** `$schema`가 **`2025-12-11`** — 기존 레퍼런스 "신선도 원장"이 레지스트리 API 응답에서 `[검증]`으로 기록한 값과 **정확히 일치한다.** 서로 독립된 두 경로(API 응답 / 게시 문서)가 같은 값을 준다. 모순 없음.

**필드 정리:**

| 필드 | 위치 | 비고 |
|---|---|---|
| `$schema` | 루트 | `2025-12-11` |
| `name` | 루트 | `dns-namespace/name` 형식 강제 |
| `description` | 루트 | |
| `version` | 루트 | 패키지 버전과 별개로 존재 |
| `repository.url` / `.source` | 루트 | `source: "github"` |
| `packages[].registryType` | 배열 | `npm` / PyPI / NuGet / OCI / MCPB |
| `packages[].identifier` | 배열 | 레지스트리상의 패키지명 |
| `packages[].version` | 배열 | |
| `packages[].transport.type` | 배열 | 예: `stdio` |
| `packages[].environmentVariables[]` | 배열 | `name`·`description`·`isRequired`·`format`·`isSecret` |

`init` 템플릿의 최소형(commands.md 예시)은 `registryType`·`identifier`·`version` 3개만 갖는다 → **`transport`·`environmentVariables`는 선택.**

**이름 일치 규칙 (원문):**

> "The `name` property in `server.json` **must** match the `mcpName` property in `package.json`."

> "Because we will be using GitHub-based authentication, `mcpName` **must** start with `io.github.my-username/`."

### 3-G. 패키지 타입별 소유권 검증 마커 **[검증]**

퀵스타트 트러블슈팅 표 원문:

> "Ensure your package includes the required ownership-verification marker for its package type. For npm this is `mcpName` in `package.json`; for PyPI and NuGet it is an `mcp-name: <server-name>` line (or HTML comment) in the package README; for other types see Package Types."

**PyPI는 README에 `mcp-name:` 줄을 넣는 방식이다** — npm의 `mcpName`과 다르다. 계획서 9장이 PyPI 경로를 다루므로 중요하다.

**실물 확인 [검증]:** `src/fetch/README.md` 3번째 줄에 실제로 있다:

```markdown
<!-- mcp-name: io.github.modelcontextprotocol/server-fetch -->
```

→ 공식 서버가 이 규약을 실제로 쓰고 있음을 문서와 실물 양쪽에서 확인했다.

### 3-H. 인증 방식 4종 **[검증]**

| 방식 | 커맨드 | 부여 네임스페이스 |
|---|---|---|
| GitHub 대화형 | `mcp-publisher login github` | `io.github.{username}/*`, `io.github.{org}/*` |
| GitHub OIDC (CI) | `mcp-publisher login github-oidc` | 동일. 워크플로에 `id-token: write` 필요 |
| DNS | `mcp-publisher login dns --domain=example.com --private-key=HEX_KEY` | `com.example.*` |
| HTTP | `mcp-publisher login http --domain=example.com --private-key=HEX_KEY` | `com.example.*` |
| 익명 (테스트) | `mcp-publisher login none` | 로컬 레지스트리 전용 |

DNS/HTTP는 Ed25519(64자 hex) 또는 ECDSA P-384(96자 hex) 키를 쓴다. Google KMS·Azure Key Vault 서명도 지원한다.

DNS TXT 레코드 형식 (원문): `example.com. IN TXT "v=MCPv1; k=ed25519; p=PUBLIC_KEY"`
HTTP 검증 위치 (원문): `https://example.com/.well-known/mcp-registry-auth`

토큰 저장 위치 (원문): `~/.config/mcp-publisher/token.json`

> "**Note:** Tokens were previously stored in `~/.mcp_publisher_token`. If you are upgrading, run `mcp-publisher logout` followed by `mcp-publisher login` to migrate to the new location."

---

## 자료 4: Python SDK 2.0 `MCPServer` 공식 사용 예제

> 🕒 **전 항목 `mcp` 2.0.0b2 / 2026-07-26 기준. 2026-07-27~28 정식 릴리스로 바뀔 수 있다.**

### 4-A. 판정: 공식 예제는 **존재한다** — §7-B-6 해소 **[검증]**

기존 레퍼런스 §7-B-6은 "클래스·모듈 구조는 실측했으나 **예제 코드 미확보**"였다. 이는 wheel만 뒤진 결과로 보인다. **예제는 wheel이 아니라 리포에 있다.**

**열거 방법 (추측 아님):** `v2.0.0b2` **태그** 트리 전수 열거

```
curl -s "https://api.github.com/repos/modelcontextprotocol/python-sdk/git/trees/v2.0.0b2?recursive=1"
```

확인된 태그 목록: `v2.0.0b2`, `v2.0.0b1`, `v2.0.0a3`, `v2.0.0a2`, `v2.0.0a1`, `v1.28.1`…
PyPI 실측: `latest: 1.28.1`, 2.x 계열은 `['2.0.0a1','2.0.0a2','2.0.0a3','2.0.0b1','2.0.0b2']` — **정식 2.x 없음**(§7-A-4 재확인).

**태그에 존재하는 문서 트리 (발췌):** `docs/index.md`, `docs/migration.md`, `docs/protocol-versions.md`, `docs/deprecated.md`, `docs/get-started/{index,installation,first-steps,real-host,testing}.md`, `docs/servers/{index,tools,resources,prompts,structured-output,completions,media,uri-templates,handling-errors}.md`, `docs/handlers/*`, `docs/client/*`, `docs/run/{index,asgi,authorization,deploy,legacy-clients,opentelemetry}.md`, `docs/advanced/*`

→ **"공식 예제 부재"는 틀린 결론이었다. 문서 사이트 전체가 태그 안에 들어 있다.**

### 4-B. 15줄 서버 — 실행 가능한 원문 소스 **[검증]**

README가 참조하는 실제 파일 `docs_src/index/tutorial001.py` 전문 (스니펫 인용이 아니라 **소스 파일 원문**):

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

README 해설 원문:

> "That's a complete MCP server: one tool, one templated resource."

> "Notice what you did **not** write: no JSON Schema (`a: int, b: int` _is_ the schema), no request parsing, no validation code, no protocol handling. Two type-hinted Python functions and a docstring."

실행:

```bash
uv run mcp dev server.py
```

설치 (README 원문):

```bash
uv add "mcp[cli]==2.0.0b1"          # or: pip install "mcp[cli]==2.0.0b1"
```

> "The pin matters while v2 is in pre-release: an unpinned install resolves to the latest stable v1.x, which this README does not describe."

### 4-C. 세 프리미티브 전부 — `docs_src/first_steps/tutorial001.py` 원문 **[검증]**

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


@mcp.prompt()
def summarize(text: str) -> str:
    """Summarize a piece of text in one sentence."""
    return f"Summarize the following text in one sentence:\n\n{text}"
```

`docs/get-started/first-steps.md`의 프리미티브 구분 표 (원문 그대로 — 책에 인용 가치 높음):

| Primitive | Controlled by | What it is | Example |
|---|---|---|---|
| **Tools** | The model | A function the model calls to take an action | An API call, a database write |
| **Resources** | The application | Data the host loads into the model's context | A file's contents, an API response |
| **Prompts** | The user | A reusable message template the user invokes by name | A slash command, a menu entry |

> "'Controlled by' is the whole point of the split. A tool runs because the **model** decided to call it. A resource is attached because the **application** decided the model needed it. A prompt runs because the **user** picked it."

웹 API 비유 (원문):

> "If you've built a web API you already have most of the intuition: a **resource** is a `GET` (it loads data and changes nothing) and a **tool** is a `POST` (it does work and may have side effects). A **prompt** has no HTTP analogue; it's closer to a saved query the user runs by name."

### 4-D. ⚠️ import 경로가 문서 간 불일치 — 저술 시 주의 **[검증]**

**두 공식 문서가 서로 다른 경로를 쓴다:**

`docs/get-started/first-steps.md` 원문:

> "The two halves of the SDK have two import paths: `from mcp import Client` and `from mcp.server import MCPServer`. **There is no `from mcp import MCPServer`.**"

반면 `docs/migration.md`의 마이그레이션 예시 원문:

```python
from mcp.server.mcpserver import MCPServer, Context

mcp = MCPServer("Demo")
```

→ `mcp.server`(재노출)와 `mcp.server.mcpserver`(실제 위치) **둘 다 유효**한 것으로 보이나, **1차 문서가 명시적으로 정리해주지 않았다.** 책에서는 **`from mcp.server import MCPServer`를 쓰라** — 이쪽이 튜토리얼·README·실제 `docs_src/*.py` 소스 전부가 쓰는 형태다. `Context`가 필요할 때만 `mcp.server.mcpserver`를 언급하라. **"둘은 같다"고 단정하지는 마라** (⚠️ 미확인).

### 4-E. 툴 등록의 스키마 자동 생성 — `docs/servers/tools.md` **[검증]**

원문: "You declare one by putting `@mcp.tool()` on a plain Python function. **That's the whole API.**"

실제 소스 `docs_src/tools/tutorial001.py` 원문:

```python
from mcp.server import MCPServer

mcp = MCPServer("Bookshop")


@mcp.tool()
def search_books(query: str, limit: int) -> str:
    """Search the catalog by title or author."""
    return f"Found 3 books matching {query!r} (showing up to {limit})."
```

SDK가 함수에서 읽는 세 가지 (원문):

> - "The **name** of the tool is the name of the function: `search_books`."
> - "The **description** the model sees is the docstring: `Search the catalog by title or author.`"
> - "The **arguments** the model is allowed to pass come from the type hints: `query: str` and `limit: int`."

생성되는 JSON Schema 원문:

```json
{
  "type": "object",
  "properties": {
    "query": {"title": "Query", "type": "string"},
    "limit": {"title": "Limit", "type": "integer"}
  },
  "required": ["query", "limit"],
  "title": "search_booksArguments"
}
```

> "Type hints aren't documentation here. They are **the contract**. If a client sends `"limit": "ten"`, the SDK rejects it before your function ever runs."

기본값을 주면 `required`에서 빠진다 (원문): "Give a parameter a default value and it stops being required. That's it. It's just Python." → 스키마에 `"default": 10`이 붙고 `required`는 `["query"]`만 남는다.

반환값 두 갈래 (원문):

```python
result.content             # [TextContent(text="Found 3 books matching 'dune' (showing up to 5).")]
result.structured_content  # {'result': "Found 3 books matching 'dune' (showing up to 5)."}
```

> "`content` is the text the **model** reads. `structured_content` is typed data for the **client application**."

### 4-F. capabilities 자동 선언 **[검증]**

`docs/get-started/first-steps.md` 원문 출력:

```text
{'prompts': {'list_changed': True}, 'resources': {'subscribe': True, 'list_changed': True}, 'tools': {'list_changed': True}}
```

> "`MCPServer` serves all three primitives, so all three are always declared."

> "Notice what isn't there. `completions` ... needs a handler you write, this server doesn't have one, so the capability is absent and a well-behaved client won't ask. That's the rule for everything optional: register the thing and the capability appears."

### 4-G. v1→v2 breaking change 표 — 9장/마이그레이션 절에 직결 **[검증]**

`docs/migration.md`의 "Changes almost every project hits" 원문 표:

| Change | First symptom |
|---|---|
| `FastMCP` renamed to `MCPServer` | `ModuleNotFoundError: No module named 'mcp.server.fastmcp'` |
| Fields renamed from camelCase to snake_case | `AttributeError: 'Tool' object has no attribute 'inputSchema'` |
| `mcp.types` moved to the `mcp-types` package | `ModuleNotFoundError: No module named 'mcp.types'` |
| `McpError` renamed to `MCPError` | `ImportError: cannot import name 'McpError' from 'mcp'` |
| Resource URIs are `str`, not `AnyUrl` | `AttributeError: 'str' object has no attribute 'host'` |
| `streamablehttp_client` removed | `ImportError: cannot import name 'streamablehttp_client'` |
| `Client` defaults to `mode='auto'` | servers log an unexpected `server/discover` request |
| Transport parameters moved off the `MCPServer` constructor | `TypeError: MCPServer.__init__() got an unexpected keyword argument 'port'` |
| Sync handlers run on a worker thread | `asyncio.get_running_loop()` in a `def` handler raises `RuntimeError` |
| Lowlevel decorators replaced with `on_*` constructor params | `AttributeError: 'Server' object has no attribute 'list_tools'` |
| Roots, Sampling, and Logging deprecated (SEP-2577) | `MCPDeprecationWarning` at call sites |

**✅ §7-A-6 재확인:** "`FastMCP`는 Python `mcp` 2.0에 존재하지 않는다"는 기존 부정 발견이 **마이그레이션 가이드 원문으로 확증됐다** — `FastMCP` → `MCPServer` 개명. 기존 레퍼런스는 wheel 문자열 검색(0건)으로 도달했고, 이번엔 공식 문서가 이유를 설명한다:

> "The `FastMCP` class has been renamed to `MCPServer` to better reflect its role as the main server class in the SDK. This is a simple rename with no functional changes to the class itself."

> 📌 두 독립 경로가 같은 결론 → 이 주장은 책에서 **강하게 단정해도 된다.**

의존성 하한 상승 (원문 표 발췌): `anyio >=4.9`, `pydantic >=2.12`, `sse-starlette >=3.0.0`, `typing-extensions >=4.13.0`, `opentelemetry-api >=1.28.0`(신규 필수), `mcp-types`(신규, 정확 핀), **`httpx` 제거 → `httpx2`로 교체**.

### 4-H. 프로덕션 경고 — 반드시 인용할 것 **[검증]**

README 최상단 CAUTION 블록 원문:

> "**This README documents v2 of the MCP Python SDK — a pre-release (alpha/beta) line under active development. Do not use v2 in production.** Pre-releases are published to PyPI as `2.0.0aN` / `2.0.0bN`, and **each pre-release may contain breaking changes from the previous one**."

> "**v1.x is the only stable release line and remains recommended for production.**"

> "**If your package depends on `mcp`, add a `<2` upper bound to your version constraint (for example `mcp>=1.27,<2`) before the stable release lands.**"

> "Stable v2 is targeted for **2026-07-27**, alongside the spec release."

⚠️ **저술·팩트체크 주의:** README는 정식 v2를 **2026-07-27** 목표라고 쓰고, 스펙 릴리스는 **2026-07-28**이다. 하루 차이가 실제인지 문서 오차인지는 **미확인**. 둘을 뭉뚱그려 "같은 날"이라고 쓰지 마라.

---

## 자료 5: Claude Desktop 로컬 MCP 서버 등록

### 5-A. 공식 절차 전문 **[검증]**

- 출처: `modelcontextprotocol/modelcontextprotocol` `docs/docs/develop/connect-local-servers.mdx`
- URL: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/connect-local-servers.mdx
- 제목 원문: "Connect to local MCP servers"

**→ §7-B에 없던 항목이 통째로 해소됐다. 계획서가 예고한 "4장 제목에서 Desktop 빼기" 대응은 불필요하다.**

### 5-B. GUI 경로 — 4단계 **[검증]**

원문 Steps 제목 그대로:

1. **"Open Claude Desktop Settings"** — 원문: "Click on the Claude menu in your system's menu bar (**not the settings within the Claude window itself**) and select 'Settings...'"
2. **"Access Developer Settings"** — 원문: "navigate to the '**Developer**' tab in the left sidebar" → "Click the '**Edit Config**' button"
3. **"Configure the Filesystem Server"** — JSON 편집
4. **"Restart Claude Desktop"** — 원문: "completely quit Claude Desktop and restart it"

> 📌 1단계의 "메뉴 바의 Claude 메뉴이지, 창 안의 설정이 아니다"는 **실제로 사람들이 가장 많이 헤매는 지점**이고 공식 문서가 굵게 경고한다. 책에 그대로 살려라.

### 5-C. 설정 파일 경로 **[검증]**

`Edit Config` 버튼이 만들거나 여는 파일 (원문):

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

원문: "This action creates a new configuration file if one doesn't exist, or opens your existing configuration."

`build-server.mdx`의 동일 경로 + 여는 방법 (교차 확인, 원문):

```bash
# macOS/Linux
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Windows
code $env:AppData\Claude\claude_desktop_config.json
```

⚠️ **Linux 경로는 [미확인]** — 그리고 `build-server.mdx`가 이유를 밝힌다 (원문): "**Claude for Desktop is not yet available on Linux.**" 리눅스 경로를 지어내지 마라.

### 5-D. `mcpServers` 스키마 **[검증]**

macOS 예시 원문:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Downloads"
      ]
    }
  }
}
```

Windows는 `"C:\\Users\\username\\Desktop"`처럼 **이중 백슬래시**를 쓴다.

필드 해설 원문:

> - "`"filesystem"`: A friendly name for the server that appears in Claude Desktop"
> - "`"command": "npx"`: Uses Node.js's npx tool to run the server"
> - "`"-y"`: Automatically confirms the installation of the server package"
> - "The remaining arguments: Directories the server is allowed to access"

보안 경고 원문 (인용 가치 높음):

> "Only grant access to directories you're comfortable with Claude reading and modifying. **The server runs with your user account permissions, so it can perform any file operations you can perform manually.**"

`env` 키도 유효 (트러블슈팅 절 원문 예시):

```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "APPDATA": "C:\\Users\\user\\AppData\\Roaming\\",
      "BRAVE_API_KEY": "..."
    }
  }
}
```

→ 확인된 필드: **`command`, `args`, `env`.**

### 5-E. 등록 후 UI 확인 경로 **[검증]**

원문: 대화 입력창 좌하단 "Add files, connectors, and more /" 인디케이터 클릭 → "move the mouse over '**Connectors**' and click '**Manage connectors**'" → 목록에서 서버 선택하면 도구 목록이 보인다.

⚠️ **"망치 아이콘(hammer icon)"은 낡은 표현이다.** 트러블슈팅 제목에 "hammer icon missing"이 남아 있지만 본문 절차는 **Connectors** UI로 갱신됐다. 책에서는 **Connectors** 쪽을 써라.

### 5-F. 로그 위치 — 디버깅 장에 직결 **[검증]**

원문:

- macOS: `~/Library/Logs/Claude`
- Windows: `%APPDATA%\Claude\logs`

> "`mcp.log` will contain general logging about MCP connections and connection failures."
> "Files named `mcp-server-SERVERNAME.log` will contain error (stderr) logging from the named server."

```bash
# macOS/Linux
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
# Windows
type "%APPDATA%\Claude\logs\mcp*.log"
```

### 5-G. 트러블슈팅 체크리스트 **[검증]**

"Server not showing up in Claude" 원문 5단계:

> 1. "Restart Claude Desktop completely"
> 2. "Check your `claude_desktop_config.json` file syntax"
> 3. "Make sure the file paths included in `claude_desktop_config.json` are valid and that they are **absolute and not relative**"
> 4. "Look at logs to see why the server is not connecting"
> 5. "In your command line, try manually running the server ... to see if you get any errors"

Windows `${APPDATA}` ENOENT 이슈 + "npm should be installed globally" 경고도 원문에 있다 (`npm install -g npm`).

### 5-H. `.mcpb` / Desktop Extensions **[검증]**

`connect-local-servers.mdx`·`build-server.mdx`에는 `.mcpb` 서술이 **없다**(그 자체가 사실이다). 그러나 Anthropic 쪽 1차 소스에는 **충분히 있다.** 확인한 소스 3종:

- https://claude.com/docs/connectors/building/mcpb ("Build a desktop extension with MCPB") — 정전 가이드
- https://github.com/anthropics/mcpb README.md (원문 직접 취득)
- https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop

**정의 원문:**

> "An `.mcpb` file is a zip archive containing a local MCP server and a `manifest.json`. It enables single-click installation in Claude Desktop, similar to a browser extension."

특성 원문: "Runs locally on the user's machine / Communicates via **stdio** transport / Bundles all dependencies / Works offline / **No OAuth required**"

리포 README의 비유 원문:

> "The format is spiritually similar to Chrome extensions (`.crx`) or VS Code extensions (`.vsix`), enabling end users to install local MCP servers with a single click."

**⚠️ DXT → MCPB 개명 (중요 — 낡은 자료 판별 기준):**

> "**IMPORTANT NOTICE: This project is being renamed from DXT (Desktop Extensions) to MCPB (MCP Bundles)**"
> - "`dxt` CLI is now `mcpb`"
> - "`.dxt` files are now `.mcpb` files"
> - "`@anthropic-ai/dxt` package will be moved to `@anthropic-ai/mcpb`"

→ **`.dxt`/`dxt`를 쓰는 자료는 구버전이다.** 책에서 `.dxt`를 쓰지 마라. 이건 독자가 블로그를 볼 때 신선도를 판별하는 좋은 기준이기도 하다.

**빌드 시퀀스 원문 (4단계):**

```bash
npm install -g @anthropic-ai/mcpb   # 1. CLI 설치
# 2. stdio MCP 서버 작성
mcpb init                            # 3. manifest.json 생성
mcpb pack                            # 4. .mcpb 번들 생성
```

리포 README 원문: "At the core, MCPB are simple zip files containing your entire MCP server and a `manifest.json`. Consequently, turning a local MCP server into a bundle is straightforward: You just have to put all your required files in a folder, create a `manifest.json`, and then create an archive."

**설치 경로 — 3가지 (원문):**

> 1. "**Double-click** the `.mcpb` file"
> 2. "**Drag and drop** the `.mcpb` file into the Claude Desktop window"
> 3. "**Settings**: Settings → Extensions → Advanced settings → Install Extension… → select the `.mcpb` file"

> "Installation is per-user; each user installs separately on their own system."

**번들 구조 (Node 예시, README 원문):**

```
bundle.mcpb (ZIP file)
├── manifest.json         # Required: Bundle metadata and configuration
├── server/               # Server files
│   └── index.js          # Main entry point
├── node_modules/         # Bundled dependencies
├── package.json          # Optional: NPM package definition
├── icon.png              # Optional: Bundle icon
└── assets/               # Optional: Additional assets
```

> "A `manifest.json` is the only required file."

**언어 권장 — Node.js (원문):**

> "**We recommend implementing MCP servers in Node.js** rather than Python to reduce installation friction. Node.js ships with Claude for macOS and Windows, which means your bundle will work out-of-the-box for users without requiring them to install additional Python runtimes."

**🔗 item 1과의 연결 고리 — `server.type = "uv"` (README 원문):**

> **UV Runtime (v0.4+):**
> - "Use `server.type = "uv"` in manifest"
> - "Include `pyproject.toml` with dependencies (no bundled packages needed)"
> - "Host application manages Python and dependencies automatically"
> - "Works cross-platform without user Python installation"
> - "See `examples/hello-world-uv`"

→ **MCPB v0.4+는 Python 번들에 uv를 1급으로 지원한다.** 자료 1(uv)과 자료 5(Desktop)가 여기서 만난다 — 9장에서 배포 경로를 묶어 서술할 때 좋은 마무리가 된다.

**플랫폼:** "Claude Desktop runs on macOS (`darwin`) and Windows (`win32`)" — 5-C의 Linux 부재와 일치.

⚠️ **MCPB는 2차 배포 경로다 (원문 Note):**

> "MCPB is the **secondary** distribution path. Remote MCP servers are recommended for directory listing."

책에서 MCPB를 "권장 배포 방식"으로 소개하지 마라. Anthropic의 공식 입장은 **디렉토리 등재 목적이면 원격 서버가 우선**이고, MCPB는 방화벽 내부·로컬 리소스·프라이버시 요구가 있을 때의 경로다.

⚠️ **리포 위치 표기 주의:** 정전 가이드는 `github.com/modelcontextprotocol/mcpb`를 가리키고, README 원문은 `github.com/anthropics/mcpb`에서 취득했다. 이관 중으로 보이나 **관계를 확인하지 못했다 [미확인]** — 책에 리포 URL을 박을 때 저술 시점에 재확인하라.

### 5-I. ⚠️ 두 공식 소스가 서로 다른 1차 경로를 안내한다 **[검증]**

이번 보강에서 가장 주목할 발견이다.

| 소스 | 제시하는 주 경로 |
|---|---|
| modelcontextprotocol.io (`connect-local-servers.mdx`) | Settings → **Developer** → Edit Config → `claude_desktop_config.json` 직접 편집 |
| support.claude.com (`10949351`) | Settings → **Extensions** (데스크톱 확장 설치) |

support.claude.com 문서를 열어 확인한 결과 (원문): "Navigate to Settings > Extensions on Claude Desktop". **이 문서에는 `claude_desktop_config.json` 경로도, `mcpServers` JSON 예시도 등장하지 않는다.** Developer settings는 "checking MCP server connection status and viewing logs" 용도로만 언급된다.

**→ 해석:** Anthropic 지원 문서는 일반 사용자에게 **Extensions(.mcpb)를 1차 경로로** 밀고 있고, JSON 수동 편집은 MCP 프로토콜 문서 쪽에 남아 있다. **둘 다 유효하며 폐기된 것은 없다** — 5-A의 Developer → Edit Config 절차는 modelcontextprotocol.io 현행 문서에 그대로 살아 있다.

**저술 지침:** 4장에서 두 경로를 **모두** 제시하되 대상을 갈라라 — 직접 만든 서버를 개발 중 붙일 때는 `claude_desktop_config.json`(반복 수정이 빠르다), 남에게 배포할 때는 `.mcpb`(사용자가 JSON을 만질 필요가 없다). "공식 방법은 하나"라고 쓰면 둘 중 하나가 틀린 말이 된다.

---

## 보너스: 스코프 우선순위 §7-B-1 해소 **[검증]**

계획서 154행이 "**1차 문서로 확인되지 않았다 — 단정 금지**"로 묶어둔 항목이다. **이번에 1차 문서를 확보했다.**

- 출처: Claude Code 공식 문서, "Scope hierarchy and precedence" 절
- URL: https://code.claude.com/docs/en/mcp

원문 그대로:

> "When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source. **The entire server entry from that source is used; fields are not merged across scopes.**"
>
> 1. Local scope
> 2. Project scope
> 3. User scope
> 4. Plugin-provided servers
> 5. claude.ai connectors

> "The three scopes match duplicates by name. **Plugins and connectors match by endpoint**, so one that points at the same URL or command as a server above is treated as a duplicate."

**→ 세 가지 수정 사항:**
1. `local > project > user`는 이제 **[검증]이며 단정 가능하다.** 계획서의 "다수 자료가 이렇게 설명한다" 완화 표현은 **불필요하다.**
2. 다만 목록은 **3단계가 아니라 5단계**다 — 플러그인 서버와 claude.ai 커넥터가 아래에 붙는다. 2차 블로그들이 놓친 부분이다.
3. **"필드는 스코프 간에 병합되지 않는다"**는 실무적으로 가장 중요한데 2차 자료에 거의 없다. 책에 꼭 넣어라.

---

## 수집 한계 (이번 보강)

### 확정된 부정적 발견 (조사 완료 — 미조사가 아니다)

| 발견 | 근거 |
|---|---|
| **Claude Code 공식 문서에 `uvx` 리터럴 예시가 없다** | 레퍼런스(`/docs/en/mcp`) + 워크스루(`/docs/en/mcp-quickstart`) **두 페이지 전문 기계 검색 0건**. 로컬 서버 예시는 전부 `npx` |
| **공식 레퍼런스 서버는 7개뿐이다** | `servers` 리포 트리 전수 열거 (Python 3 / Node 4) |
| **공식 서버 7개 중 6개가 `ENTRYPOINT`를 쓴다** | 7개 Dockerfile 전수 원문 확인. `CMD`는 `src/everything` 하나뿐 |
| **Claude Desktop에 Linux 경로는 존재하지 않는다** | 원문 "Claude for Desktop is not yet available on Linux" + MCPB 문서 "macOS (`darwin`) and Windows (`win32`)" |
| **Python SDK 2.0 공식 예제는 존재한다** (§7-B-6 반증) | `v2.0.0b2` 태그 트리 전수 열거 → `docs/**` + `docs_src/**/*.py` 실재 |
| **`.dxt`/`dxt` 표기는 구버전이다** | 리포 README의 DXT→MCPB 개명 공지 |

### 남은 미확인 (지어내지 말 것)

| 미확인 항목 | 상태 | 저술 지침 |
|---|---|---|
| `docker mcp` CLI 전체 서브커맨드 | 카탈로그 문서는 GUI 위주. `docker mcp catalog pull`만 확인 | `docker mcp run` 등을 지어내지 마라. `docker run -i --rm mcp/<name>`은 [검증] |
| uv의 `[project.scripts]` 해석 메커니즘 명문 | uv 문서가 명시 설명 안 함 | 공식 서버 pyproject.toml 실물 2건(1-E)을 근거로 삼아라 |
| `mcp.server` vs `mcp.server.mcpserver` 동치 여부 | 두 공식 문서가 다른 경로 사용, 관계 명문화 없음 | `from mcp.server import MCPServer` 사용. "같다"고 단정하지 마라 |
| v2 정식일 2026-07-27 vs 스펙 2026-07-28 | 하루 차이 근거 불명 | 뭉뚱그리지 마라 |
| MCPB 리포 정본 위치 (`anthropics/mcpb` vs `modelcontextprotocol/mcpb`) | 이관 중으로 보이나 관계 미확인 | 리포 URL은 저술 시점에 재확인 |
| MCPB `manifest.json` 전체 필드 스펙 | `MANIFEST.md` 원문 미취득 (존재는 확인) | 필드를 열거하지 마라. 필요하면 `MANIFEST.md`를 열어라 |
| `ENTRYPOINT` 권장의 명문 규정 | 어디에도 없음 — 빈도 사실일 뿐 | "6/7이 쓴다"는 측정치로 쓰고 "권장한다"로 쓰지 마라 |

**등급 분포:** 조사 5건 + 보너스 1건 = **6건 전부 [검증] 확보.** 위 부정적 발견 6건은 **조사 완료된 결론**이고, 남은 미확인은 7개 하위 항목이며 전부 "지어내지 말 것" 지침과 함께 격리했다.
