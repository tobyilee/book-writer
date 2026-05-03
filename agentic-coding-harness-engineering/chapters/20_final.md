# 20장. 격리 운영 레시피 — 30분 PoC 세 가지

> *"30분 안에 격리를 짤 수 있다. 진짜로? 그렇다, 진짜로."*
> — 저자 정리 (Anthropic Claude Code 팀의 *"Sandbox first, debug second."* [^claude-code]에서 도출)

19장에서 3축 — Tooling·Host·Network — 의 이론을 받아들였다. 자기 환경의 빈 축도 한 줄로 짚어 봤다. 이제 그 빈 축에 *진짜로 한 줄을 끼울 차례*다.

번거롭게 들리는가? 번거롭다. 인정하자. 그런데 이 번거로움이 *우리를 살린다*. 18장 끝에서 같은 문장을 박았다. 한 번 더 박는다. 번거로움이 우리를 살린다. 이 한 줄이 4부의 결을 닫는다.

이 챕터는 *30분 PoC 세 가지*를 손에 쥐어 준다. 세 PoC는 다음과 같다.

- **레시피 1 — Docker + egress proxy + ephemeral secrets** (10분 PoC). 격리 깊이 *중간*. 어떤 환경에서든 깔린다.
- **레시피 2 — devcontainer + 최소 권한 파일시스템** (10분 PoC). 격리 깊이 *얕음*. VS Code 사용자에게 가장 편하다.
- **레시피 3 — macOS sandbox-exec 프로파일** (10분 PoC). 격리 깊이 *얕음*. macOS 머신의 일상 작업에 가장 가볍다.

세 PoC를 *모두* 짤 필요는 없다. 19장에서 진단한 *빈 축*에 가장 잘 맞는 하나부터 짠다. 그러나 셋의 모양을 다 보고 나면 어느 게 *우리* 환경에 어울릴지가 명확해진다.

마지막에 Claude Code와 Codex CLI의 격리 옵션을 비교한다. 두 도구가 *기본으로* 켜고 있는 것과 *비어 있는 자리*를 짚는다. 그 위에 부록 G(운영 런북)으로 다리를 놓고 닫는다.

## 30분 PoC를 *왜* 30분으로 자르는가

30분이라는 숫자에는 이유가 있다.

격리를 *완벽하게* 짜려고 하는 팀이 있다. Firecracker 위에 자체 오케스트레이터를 얹고, 사내 PKI를 박고, 모든 도구를 형식 검증으로 통과시킨다. 6개월 걸리는 일이다. 그 6개월 동안 *오늘 막을 수 있던 사고*가 막히지 않는다.

반대로 *손도 안 대는* 팀이 있다. "지금까지 사고 없었으니 괜찮다"는 입장이다. 17장 Shai-Hulud의 72시간을 본 우리는 안다 — 사고는 *우리가 일어나기 전에* 끝난다.

그 사이에 30분 PoC가 있다. 깊지 않다. 한 줄짜리 시연이다. 그러나 *오늘 작동한다*. 그게 핵심이다. 30분짜리 PoC가 *0분짜리 비어 있음*을 이긴다.

> *"Sandbox first, debug second."*
> "샌드박스를 먼저 깔자. 디버깅은 그 다음이다."
> — Anthropic Claude Code 팀 [^claude-code]

이 한 줄을 받아들이고 들어간다.

## 레시피 1 — Docker + egress proxy + ephemeral secrets

이 PoC는 3축을 *한 번에* 살짝씩 닫는다. 격리 깊이는 중간이고, 어느 환경에서든 깔린다.

**핵심 아이디어.** 에이전트를 Docker 컨테이너 안에서 띄운다(Host 축). 컨테이너의 네트워크는 *egress 프록시*만 통과한다(Network 축). 외부 API 키는 *세션 단위로 발급되는 단기 토큰*으로 굴린다(시크릿 노출 시간 축소). 도구는 *작업 디렉토리 마운트*만 노출한다(Tooling 축).

**구성 요소.**

1. *Docker 컨테이너.* 베이스 이미지는 자기 팀이 신뢰하는 이미지(예: `node:lts-slim`, `python:3.12-slim`). 사내 미러를 쓰면 17장에서 본 supply-chain 보호도 따라온다.
2. *Egress 프록시.* 컨테이너 안에서 모든 외부 호출이 거치는 한 곳. 화이트리스트된 도메인만 통과. 가장 단순한 구현은 `tinyproxy` 또는 `mitmproxy` 한 컨테이너를 띄우고 환경변수 `HTTP_PROXY` `HTTPS_PROXY`로 가리키는 것.
3. *작업 디렉토리 마운트.* 호스트의 *해당 프로젝트 디렉토리만* 컨테이너에 read-write로 마운트. 다른 디렉토리는 안 보인다.
4. *Ephemeral secrets.* API 키는 *짧게 살아 있는* 토큰으로 발급한다. Anthropic·OpenAI 콘솔에서 *expiration*이 짧은 키를 만들거나, 사내 시크릿 매니저(Vault·AWS Secrets Manager)에서 단기 토큰을 받아 환경변수로 주입.

**시연 흐름 (의사 명령).**

다음 흐름을 자기 환경의 셸 스크립트나 Docker compose로 옮긴다.

1. egress proxy 컨테이너를 먼저 띄운다. 화이트리스트 파일을 read-only로 마운트. 외부 포트 하나(예: 8888)에 listen.
2. 사내 시크릿 매니저에서 단기 토큰을 받아 환경변수로 보관. TTL 1시간 정도가 적당하다.
3. 격리된 코딩 에이전트 컨테이너를 띄운다.
   - 네트워크는 egress proxy 컨테이너에 결합 (`--network=container:egress-proxy`).
   - 환경변수에 단기 토큰 + `HTTP_PROXY`, `HTTPS_PROXY` 주입.
   - 호스트의 작업 디렉토리만 `/workspace`로 마운트.
   - 컨테이너 자체를 read-only로 띄우고 `/tmp`만 tmpfs로 둔다.

이 흐름을 한 벌의 docker compose 파일로 박아 두면 다음에 바로 띄울 수 있다.

**이 PoC가 닫는 축.**

- Tooling (얇음) — 작업 디렉토리만 마운트. 다른 호스트 파일 보이지 않음.
- Host (보통) — 컨테이너 격리. read-only + tmpfs로 컨테이너 내부도 일부 읽기 전용.
- Network (얇음) — egress proxy만 통과. 화이트리스트 밖은 거절.

**10분 안에 짜는 순서.**

1. (3분) `proxy-allowlist.txt` 한 줄씩 적기 — `api.anthropic.com`, `api.openai.com`, `github.com`, 자기 팀이 신뢰하는 도메인 5~10개.
2. (4분) Docker compose 또는 위 흐름의 셸 스크립트 한 벌. 첫 시도에서 컨테이너가 떴는지만 확인.
3. (3분) 평소 작업 한 가지를 컨테이너 안에서 시켜 보고, 잘 도는지 확인.

첫 시도에서 *몇 가지가 안 될* 가능성이 높다. 그게 정상이다. 안 되는 도구가 *어느 축*에 걸려 있는지를 보면, 그 자리에 1차 방어가 *지금 없다*는 신호다. 그 신호 자체가 진단이다.

## 레시피 2 — devcontainer + 최소 권한 파일시스템

이 PoC는 *얕은 격리*다. VS Code 사용자에게 가장 편하다.

**핵심 아이디어.** VS Code의 devcontainer 표준 [^devcontainer]을 활용해 *프로젝트별로 격리된 개발 환경*을 띄운다. 그 환경 안에서 코딩 에이전트가 돈다. 호스트의 다른 디렉토리는 보이지 않는다.

**구성 요소.**

1. `.devcontainer/devcontainer.json` — VS Code 표준 설정.
2. `Dockerfile` — devcontainer의 베이스 이미지.
3. `mounts` 설정 — 작업 디렉토리만 마운트.
4. `runArgs` — 추가 격리 플래그(`--read-only`, `--cap-drop=ALL` 등).

**예시 `devcontainer.json` 골격.**

```
{
  "name": "Isolated Coding Agent",
  "build": { "dockerfile": "Dockerfile" },
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
  ],
  "runArgs": [
    "--read-only",
    "--tmpfs=/tmp",
    "--cap-drop=ALL",
    "--security-opt=no-new-privileges"
  ],
  "remoteEnv": {
    "ANTHROPIC_API_KEY": "${localEnv:SHORT_LIVED_ANTHROPIC_KEY}"
  },
  "customizations": {
    "vscode": {
      "extensions": ["anthropic.claude-code"]
    }
  }
}
```

**이 PoC가 닫는 축.**

- Tooling (보통) — 작업 디렉토리만 마운트. capability 모두 제거.
- Host (얇음) — Docker 컨테이너 격리(devcontainer 표준).
- Network (없음) — 추가로 짜야 한다. egress proxy를 함께 쓰면 닫힌다.

**10분 안에 짜는 순서.**

1. (3분) `.devcontainer/devcontainer.json` 한 벌과 `Dockerfile` 최소 한 벌.
2. (4분) VS Code에서 *Reopen in Container*. 첫 빌드는 좀 걸린다 — 그 시간은 PoC 시간 안에 안 친다.
3. (3분) 컨테이너 안에서 평소 작업 한 가지. 호스트 파일이 안 보이는지 확인.

이 PoC의 강점은 *개발 워크플로 통합*이다. 격리를 *별도의 도구*로 익힐 필요가 없다 — 평소 쓰는 VS Code 안에서 한 줄 설정으로 닫힌다. 약점은 Network 축이 비어 있다는 것 — 1번 레시피와 결합하면 보완된다.

## 레시피 3 — macOS sandbox-exec 프로파일

이 PoC는 *macOS 한정*이다. 한국 회사의 다수 개발자가 macOS를 쓴다는 점을 감안하면, 손에 쥐어 둘 가치가 충분하다. 가장 가볍게 시작하는 길이다.

**핵심 아이디어.** Apple의 sandbox-exec(SBPL — Sandbox Policy Language) [^aisi-sandbox]를 써서 프로세스 단위로 작업 디렉토리·네트워크를 잠근다. 별도 컨테이너가 없으므로 *시작 시간이 즉시*다.

**구성 요소.**

1. `agent.sb` — SBPL 정책 파일.
2. 정책에 *작업 디렉토리 화이트리스트* + *네트워크 화이트리스트*를 적는다.
3. `sandbox-exec -f agent.sb <명령>` 한 줄로 띄운다.

**예시 `agent.sb` 골격** (단순화된 형태).

```
(version 1)
(deny default)

;; 작업 디렉토리만 read-write
(allow file-read* file-write*
  (subpath "/Users/me/projects/my-app"))

;; 시스템 라이브러리는 read-only
(allow file-read*
  (subpath "/usr/lib")
  (subpath "/System/Library"))

;; 네트워크는 화이트리스트된 호스트만
(allow network-outbound
  (remote ip "api.anthropic.com:443")
  (remote ip "api.openai.com:443"))

;; 그 외 시스템 호출 일부 허용 (실행에 필요한 최소)
(allow process-exec)
(allow signal (target self))
```

**시연 명령 형태.**

```
sandbox-exec -f agent.sb claude --workspace /Users/me/projects/my-app
```

**이 PoC가 닫는 축.**

- Tooling (얇음) — 작업 디렉토리 화이트리스트.
- Host (얇음) — 프로세스 격리. 컨테이너 수준은 아님.
- Network (보통) — 도메인 화이트리스트 가능.

**10분 안에 짜는 순서.**

1. (3분) `agent.sb` 한 벌 — 위 예시를 자기 환경에 맞게 수정.
2. (4분) `sandbox-exec`로 띄우기. 첫 시도에서 *허용되지 않은 syscall* 때문에 무언가 안 될 수 있다 — 콘솔 메시지를 보면서 정책을 살짝씩 넓힌다.
3. (3분) 평소 작업 한 가지. 호스트의 다른 디렉토리가 보이지 않는지 확인.

**중요한 한 줄.** Apple은 sandbox-exec를 *deprecated*로 표기한 상태다. 그러나 macOS에서 *현재* 동작하고, Claude Code와 Codex CLI 모두 내부적으로 활용한다 [^claude-code] [^openai-harness]. 미래의 Apple OS 업데이트에서 어떻게 될지는 *지켜봐야* 하지만, 오늘 손에 쥘 수 있는 가장 가벼운 격리는 이것이다. 가벼움의 가치를 인정하자.

## Claude Code와 Codex CLI의 격리 옵션 — 비교

두 도구가 격리를 어떻게 통합하는지 한 줄씩 정리한다 [^claude-code] [^openai-harness].

| 항목 | Claude Code | Codex CLI |
|------|-------------|-----------|
| 기본 호스트 격리 | macOS sandbox-exec / Linux user namespaces | macOS sandbox-exec / Linux user namespaces |
| 작업 디렉토리 격리 | 기본 활성화 (`workspace` 단위) | 기본 활성화 |
| 네트워크 격리 | 옵션 (도메인 화이트리스트 가능) | 옵션 (egress 차단 모드 있음) |
| 위험 명령 게이트 | Hooks로 사용자 정의 가능 | 사용자 승인 필요 명령 정의 가능 |
| 도구 권한 표면 | MCP 서버 단위 그룹화 | AGENTS.md + 사용자 정의 |
| 격리 설정 위치 | 프로젝트별 `.claude/` | 프로젝트별 `.codex/` 또는 AGENTS.md |

이 표에서 짚을 두 가지.

첫째, *기본으로 켜진 격리*가 이미 있다. 둘 다 작업 디렉토리 격리는 기본이다. 별도 설정 없이도 *최소한의 Tooling 축*은 닫혀 있다. 그래도 19장에서 본 3축 매트릭스로 점검하면 *Network 축*이 빠져 있는 경우가 많다 — 그래서 레시피 1의 egress proxy가 가치가 있다.

둘째, *Hooks*가 큰 차이를 만든다. Claude Code의 Hooks 시스템은 *위험 명령 직전*에 사용자 정의 검증을 끼울 수 있다. 16장의 *사용자 승인 게이트*를 한 줄짜리 후크로 구현 가능하다. Codex CLI도 사용자 승인 정의가 있다. 두 도구의 이 기능이 *이미 손에 쥐어진* 1차 방어선이다 — 안 쓰면 손해다.

## 운영 트러블슈팅 — 자주 만나는 세 가지

PoC를 짜다 보면 자주 막히는 자리가 있다. 미리 알면 시간을 아낀다.

**(1) Egress proxy가 깨질 때.** 자주 있는 일이다. 화이트리스트에 빠진 도메인이 호출돼 막힌다. 첫 반응은 화이트리스트를 *넓히고 싶은* 충동이다. 잠깐 멈추자. *왜* 그 도메인이 호출됐는가? 정상적인 호출인가, 아니면 인젝션의 1차 신호인가? 정상이라면 화이트리스트에 추가하되, *추가 이력을 로그로 남긴다*. 한 달 뒤에 그 추가가 정당했는지 audit한다.

**(2) Sandbox-exec 권한 거부.** macOS sandbox-exec은 정책 외 호출을 *조용히* 막는 경우가 있다. 콘솔 로그에는 보이는데 에이전트 출력에는 안 보인다. 디버깅이 어렵다. *먼저* 콘솔(`Console.app`)을 띄워 두고 sandbox 위반을 실시간으로 보면서 정책을 수정한다.

**(3) Ephemeral secrets 만료.** 단기 토큰이 *작업 중간에* 만료되는 경우가 있다. 길고 복잡한 작업 한 번이 1시간을 넘기면 1시간짜리 토큰은 만료된다. *재발급 후크*를 정의해 자동으로 갱신하거나, *작업 단위로 토큰을 새로 발급*받게 한다. 만료가 *기능*이지 *버그*가 아니라는 점을 받아들이자.

## 부록 G — 운영 런북으로의 다리

PoC가 굴러가기 시작하면, *운영 런북*이 다음 단계다. 부록 G에 다음을 모아 둔다.

- 비용 알람 템플릿 (15장과 짝)
- 모델 회귀 탐지 회로 (15장 + 22장과 짝)
- on-call 플레이북: 에이전트 폭주, MCP 서버 응답 정지, 시크릿 유출 의심
- 트레이스 도구 대시보드 예시: LangSmith·Helicone·Langfuse

20장의 PoC가 *오늘의 첫 줄*이라면, 부록 G는 *그 다음 한 달*의 작업대다. 본문이 닫힌 다음에도 곁에 두고 펴 보자.

---

> **시그니처 인용 박스**
>
> *"Sandbox first, debug second."*
> "샌드박스를 먼저 깔자. 디버깅은 그 다음이다."
> — Anthropic Claude Code 팀 [^claude-code]
>
> 30분짜리 PoC가 *0분짜리 비어 있음*을 이긴다. 깊은 격리를 6개월 걸려 짜는 동안, 얕은 격리로 *오늘 작동하는* 한 줄을 확보하자. 번거롭다. 그런데 이 번거로움이 *우리를 살린다*.

---

## 실습 — Docker와 sandbox-exec 두 가지 격리 비교

이번 실습은 *비교*다. 같은 작업을 두 가지 격리 환경에서 띄워 보고, 무엇이 다른지를 손으로 느낀다.

**준비 (5분).** 자기 평소 작업 한 가지를 정한다. *간단한 코딩 작업* 정도. 예: 작은 함수 하나 짜기.

**1단계 — Docker (15분).** 레시피 1의 Docker + egress proxy 환경을 띄운다. 위 시연 흐름을 자기 환경에 맞게 옮긴다. 첫 시도에서 컨테이너가 떴는지만 확인. 평소 작업을 시킨다. 시킨 작업이 정상적으로 끝나는지 본다.

**2단계 — sandbox-exec (10분).** 레시피 3의 sandbox-exec 환경을 띄운다. `agent.sb`를 작성하고 `sandbox-exec -f agent.sb`로 같은 작업을 시킨다. 콘솔 로그를 띄워 두고 sandbox 위반이 있는지 본다.

**3단계 — 비교 (10분).** 다음을 비교한다.

- *시작 시간.* sandbox-exec이 즉시. Docker는 첫 빌드 후 몇 초.
- *통합 깊이.* sandbox-exec은 호스트 위에서 그냥 돈다. Docker는 별도 환경.
- *깨질 때의 디버깅.* 어느 쪽이 더 *왜 깨졌는지* 보기 쉬운가?
- *다음 작업 재시작.* 어느 쪽이 더 가볍게 다시 띄워지는가?

**4단계 — 결정 (5분).** 자기 환경에 어느 쪽이 어울리는가? 결정하지 않아도 된다. *둘 다 손에 쥐어 본 것*이 이번 실습의 출구다. 다음 사고가 났을 때, 어느 쪽이든 *오늘 깔 수 있는* 도구가 손에 있다는 사실 — 그게 가치다.

---

## 기억해두자

- *30분 PoC 세 가지를 손에 쥐자.* Docker + egress proxy, devcontainer, macOS sandbox-exec.
- *세 PoC를 모두 짤 필요는 없다.* 19장에서 진단한 빈 축에 가장 잘 맞는 하나부터 짠다.
- *번거롭다. 그런데 이 번거로움이 우리를 살린다.* 30분짜리 PoC가 0분짜리 비어 있음을 이긴다.
- *Claude Code와 Codex CLI는 기본 격리를 가진다.* 그것을 출발점 삼고, Network 축은 추가로 짠다.
- *Hooks와 사용자 승인 게이트는 이미 손에 쥐어진 1차 방어선이다.* 안 쓰면 손해다.

격리됐어도 — 평가 환경을 *인지하는* 모델이 있다. 21장이 그 사각지대를 본다. 보안과 평가가 만나는 자리, Sandbagging의 시야다.

[^claude-code]: Anthropic Claude Code. https://code.claude.com/docs/ko/overview
[^openai-harness]: OpenAI, *Harness engineering: leveraging Codex in an agent-first world*, 2026-02. https://openai.com/index/harness-engineering/
[^aisi-sandbox]: GitHub UKGovernmentBEIS/aisi-sandboxing. https://github.com/UKGovernmentBEIS/aisi-sandboxing
[^devcontainer]: Microsoft, *Development Containers Specification*. https://containers.dev/
