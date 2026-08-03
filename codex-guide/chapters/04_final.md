# 4장. 지침과 설정 — `AGENTS.md`와 `config.toml`을 다시 세우기

32,768.

이 숫자가 자기 지침 파일과 무슨 상관인지 아는 사람은 많지 않다. Codex 설정 키 하나의 기본값이고, 이름은 `project_doc_max_bytes`, 하는 일은 지침을 어디까지 읽어들일지 정하는 것이다. 32 KiB. 결합된 지침이 그 선에 닿으면 Codex는 거기서 파일 추가를 멈춘다.

손버릇을 다 고쳐도 남는 문제가 있다. 내가 써둔 규칙이 애초에 모델에게 도착하지 않는 경우다. 이때 에이전트는 규칙을 어기는 것이 아니다. **모른 채로 일한다.** 그리고 이쪽이 훨씬 잡기 어렵다. 어긴 것은 결과에 흔적을 남기지만, 모르는 것은 아무 흔적도 남기지 않기 때문이다.

지침이 도착하지 않는 경로는 생각보다 여러 개다. 파일이 탐색 경로 밖에 있을 수도 있고, 예산에 걸려 뒷부분이 잘렸을 수도 있고, 이름이 인식 목록에 없을 수도 있다. 설정 쪽도 사정이 비슷하다. 같은 키를 여섯 개의 층이 각자 들고 있고, 그중 하나만 이긴다.

그래서 이 장은 두 개의 질문을 붙들고 간다. 내 지침은 정말 다 읽히고 있는가? 그리고 설정은 어느 층에서 이기는가?

## 에이전트를 위한 README — `AGENTS.md`의 자리

Codex 문서가 `AGENTS.md`를 정의하는 방식은 담백하다.

> "Think of `AGENTS.md` as an open-format README for agents."

README에 빗댄 것이 핵심이다. 사람이 읽는 README가 그렇듯 이 파일도 정확할 때 쓸모가 생긴다. 길이는 그다음 문제다. 문서는 그 점을 곧바로 못 박는다.

> "Keep it practical. A short, accurate `AGENTS.md` is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes."

처음부터 완벽한 규칙 세트를 쓰려 하지 말고, 기본만 적은 뒤 반복되는 실수를 관찰한 다음에 규칙을 늘리라는 얘기다. 이 운영 방식을 한 문장으로 요약한 대목도 있다.

> "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`."

같은 실수가 두 번 나오면 회고를 시키고 그 결과를 파일에 반영한다. 지침 파일을 **피드백 루프의 저장소**로 다루라는 뜻이다. 문서는 갱신 시점을 여러 갈래로 구체화한다. 같은 실수가 반복될 때, 맞는 파일을 찾긴 하는데 너무 많이 읽을 때(이때는 어느 디렉터리를 우선 볼지 라우팅 안내를 넣는다), 같은 리뷰 피드백을 두 번 이상 남기게 될 때, 그리고 예약 작업으로 지침 공백을 주기적으로 점검하고 싶을 때. 여기에 하나가 더 붙는다 — GitHub 풀 리퀘스트 코멘트에서 `@codex`를 태그해 **갱신 자체를 맡기는 경로**다.

시작이 막막하면 `/init`이 스캐폴드를 만들어준다. 이름도 역할도 손에 익은 그대로다.

배치 원칙도 문서가 정해준다. 전역 파일과 저장소 파일의 역할을 이렇게 나눈다 — 전역 파일에는 Codex가 나와 어떻게 소통할지(리뷰 스타일, 상세함의 정도, 개인 기본값)를 담고, 저장소 파일은 팀과 코드베이스의 규칙에 집중시킨다. 저장소 쪽에 들어갈 항목의 예시도 구체적이다. 빌드·테스트 명령, 리뷰 기대치, 저장소 고유 관례, 그리고 디렉터리별 지시사항.

한 가지 덜 알려진 용법도 있다. `AGENTS.md`에 `## Code Review Rules` 섹션을 두면 GitHub에서 도는 Codex 코드 리뷰가 그 규칙을 읽는다. 저장소 전체에 걸리는 검사는 루트에, 특정 서비스에만 걸리는 검사는 그 코드에 가장 가까운 파일에 둔다. 문서의 조언은 여기서도 같다. 규칙은 짧게 쓰고, 무엇을 지적할지와 안전한 우회로를 함께 적고, 포매팅과 린트 검사는 CI에 맡기라는 것이다. 리뷰 이야기는 10장에서 본격적으로 다룬다.

마지막으로 짚어둘 것은 `AGENTS.md`가 혼자 일하지 않는다는 점이다. 문서는 커스터마이즈를 다섯 층으로 나눈다. 지침(`AGENTS.md`), 메모리, 스킬, MCP, 서브에이전트. 그리고 이들의 관계를 이렇게 정리한다 — "These are complementary, not competing." `AGENTS.md`는 행동을 규정하고, 메모리는 이전 맥락을 실어 나르고, 스킬은 반복 절차를 포장하고, MCP는 바깥 시스템을 연결한다. 이 장은 첫 번째 층과 그 층을 떠받치는 설정을 다룬다. 스킬과 MCP는 확장 모델을 세우는 6장의 몫이다.

## 문서에 박혀 있는 32 KiB 예산

이제 서두의 숫자로 돌아가자. `AGENTS.md`를 찾는 규칙과 함께, 문서는 읽어들이는 양의 상한도 명시한다.

> "Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default). … Raise the limit or split instructions across nested directories when you hit the cap."

이 한 문장에 실무 정보가 세 개 들어 있다. 빈 파일은 건너뛴다는 것, **결합 크기**가 기준이라는 것, 그리고 한도에 닿으면 더 붙이지 않는다는 것. 전역 파일과 저장소 루트 파일과 하위 디렉터리 파일을 다 합친 크기가 32 KiB에 닿으면, 그 뒤에 붙었어야 할 내용은 이번 세션에 존재하지 않는다.

32 KiB가 작은 수치일까? 한글 기준으로 대략 만 자 남짓이다. 지침 파일 하나로는 넉넉하다. 그런데 이 예산은 파일 하나가 아니라 체인 전체를 대상으로 한다. 전역 파일에 개인 취향을 길게 적어두고, 저장소 루트에 팀 규약을 얹고, 작업 디렉터리에 세부 규칙을 더한 상태라면 셋의 합이 기준이 된다. 각 파일이 "이 정도면 짧지" 싶은 크기여도 합계는 다른 이야기가 된다.

이게 왜 성가신가. 지침이 잘려도 눈에 띄는 신호가 없기 때문이다. 커뮤니티에는 정확히 그 제목의 이슈가 있다 — [#13386](https://github.com/openai/codex/issues/13386) "AGENTS.md is silently truncated and instructions near the end ignored"(2026-03-03 개설, 👍 11, open). 긴 지침 파일의 뒷부분이 조용히 무시된다는 보고다. 다만 이건 익명 보고자의 커뮤니티 관측이고, 공식 문서가 "경고 없이 자른다"고 인정한 것은 아니다. 문서가 인정하는 것은 잘림 자체와 그 대처법까지다(2026-08-02 문서 기준). 그럼에도 이 이슈를 알아둘 값어치는 있다. 대응 비용이 설정 한 줄이기 때문이다.

```toml
# ~/.codex/config.toml
project_doc_max_bytes = 65536
```

문서가 제시하는 두 갈래는 한도를 올리거나, 지침을 하위 디렉터리로 쪼개는 것이다. 그런데 쪼개는 쪽을 고르려면 다음 절을 먼저 읽어야 한다. 쪼갠 파일이 실제로 읽히는지가 위치에 달려 있다.

같은 자리에 손잡이가 하나 더 있다. `project_doc_fallback_filenames`다.

```toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
```

이렇게 두면 Codex는 각 디렉터리에서 `AGENTS.override.md` → `AGENTS.md` → `TEAM_GUIDE.md` → `.agents.md` 순으로 찾는다. 문서의 경고도 함께 기억해두자 — "Filenames not on this list are ignored for instruction discovery." 목록에 없는 이름은 지침 파일로 취급되지 않는다.

이 키의 의미는 단순한 편의 이상이다. **지침 파일의 이름 자체가 설정 대상**이라는 뜻이기 때문이다. 이미 다른 이름으로 팀 규약 문서를 운영하는 저장소라면 파일을 옮기지 않고 목록에 이름만 얹으면 된다. 지침 파일 이름을 바꾼다는 발상 자체를 해본 적 없는 손이라면, 여기서 한 번 갈린다.

## 어디까지 올라가고 어디서 멈추는가

3장에서 확인한 현상 — 폴더마다 규칙을 나눠둔 저장소에서 Codex가 그 규칙 대부분을 못 본 채 일한다는 것 — 의 메커니즘이 여기 있다. 문서가 발견 순서를 세 단계로 명시한다.

첫째, 전역 범위. Codex 홈 디렉터리(기본 `~/.codex`, `CODEX_HOME`으로 변경 가능)에서 `AGENTS.override.md`가 있으면 그것을, 없으면 `AGENTS.md`를 읽는다. 이 층에서는 비어 있지 않은 첫 파일 하나만 쓴다.

둘째, 프로젝트 범위. 프로젝트 루트(보통 Git 루트)에서 시작해 현재 작업 디렉터리까지 내려오면서 경로상의 각 디렉터리를 확인한다. 디렉터리마다 `AGENTS.override.md` → `AGENTS.md` → fallback 이름 순으로 보고, 디렉터리당 최대 한 파일만 포함한다.

셋째, 병합. 루트부터 아래로 이어 붙이되 빈 줄로 잇는다. 가까운 파일이 뒤에 놓이므로 앞의 지침을 덮는다.

문제는 둘째 단계의 방향이다. 탐색은 루트에서 cwd로 내려오면서 이뤄지고, 원문은 여기에 한 문장을 덧붙인다 — "Codex stops searching once it reaches your current directory." 즉 **현재 디렉터리보다 아래는 보지 않는다.** 저장소 루트에서 Codex를 띄우면 `packages/api/AGENTS.md`도 `services/payments/AGENTS.md`도 경로 위에 없으니 로드 대상이 아니다. 모노레포에서 규칙을 패키지마다 나눠둔 사람이 겪는 일이 정확히 이것이고, 문서가 권하는 정공법은 작업할 디렉터리에서 Codex를 여는 것이다. 반대 방향으로도 보고가 있다 — [#28903](https://github.com/openai/codex/issues/28903) "AGENTS.md not loaded from ancestor directories above repo root"(2026-06-18, open)는 저장소 루트보다 위쪽 조상 디렉터리가 로드되지 않는다는 이슈다.

그 대신 앞 장에서 보지 못한 손잡이가 하나 나온다. `AGENTS.override.md`다. 같은 디렉터리에 `AGENTS.md`와 나란히 두면 override 쪽이 이기고 원래 파일은 무시된다. 문서의 예시도 이 용법을 보여준다 — `services/payments/`에 `AGENTS.override.md`를 두면 그 디렉터리에서 시작한 세션은 결제 서비스 규칙을 마지막에 얹는다. 전역 층에서는 쓰임이 더 좋다. 기본 파일을 지우지 않고 임시로 전역 지침만 갈아끼울 수 있고, override 파일을 지우면 원래 지침이 그대로 돌아온다.

이 편리함에는 대가도 있다. 어느 날 갑자기 엉뚱한 지침이 적용된다면 트리 위쪽이나 Codex 홈에 잊고 있던 `AGENTS.override.md`가 남아 있을 확률이 높다. 문서의 트러블슈팅 항목도 정확히 그 순서를 안내한다 — 잘못된 지침이 보이면 상위 디렉터리와 Codex 홈의 override 파일을 먼저 찾고, 그 파일 이름을 바꾸거나 지워 원래 파일로 되돌리라는 것이다. 아무것도 로드되지 않을 때의 점검 순서도 있다. `codex status`가 보고하는 워크스페이스 루트가 내가 생각한 그 저장소인지 확인하고, 지침 파일이 비어 있지는 않은지 본다(빈 파일은 무시된다). 그리고 `echo $CODEX_HOME`. 이 값이 기본이 아니면 내가 편집한 홈과 Codex가 읽는 홈이 서로 다른 디렉터리다.

그래서 실무 규칙은 이렇게 정리된다. **지침은 "작업을 시작하는 위치"를 기준으로 배치한다.** 루트에서 주로 일한다면 규칙을 루트로 모으고, 패키지 단위로 들어가 일한다면 그 패키지에 두고 거기서 Codex를 연다. 어느 쪽이든 확인 절차는 있다.

```bash
codex --cd services/payments --ask-for-approval never "List the instruction sources you loaded."
```

문서가 기대 결과까지 적어둔 명령이다. 전역 파일이 먼저, 저장소 루트 `AGENTS.md`가 다음, 해당 디렉터리 override가 마지막으로 보고되어야 한다. 더 확실히 보고 싶으면 평문 TUI 로그를 켜서 실제로 어떤 파일이 로드됐는지 들여다볼 수 있다.

```bash
codex -c log_dir=./.codex-log
```

지침이 낡아 보일 때 캐시를 지울 필요는 없다. Codex는 실행할 때마다(TUI라면 세션을 띄울 때마다) 지침 체인을 다시 만든다. 파일을 고쳤으면 다시 띄우면 그만이다.

## `config.toml`이라는 지형 — 그리고 여섯 층의 우선순위

지침이 무엇을 시킬지 정한다면, `config.toml`은 그 일을 어떤 조건에서 하게 할지 정한다. 규모부터 보자. 설정 키는 270개가 넘고, 관리자가 강제하는 `requirements.toml` 쪽에 116개가 더 있다. 다 외울 물건은 아니다. 외울 필요도 없다. 공식 JSON 스키마가 `https://learn.chatgpt.com/docs/config-schema.json`에 공개돼 있기 때문이다. 편집기에 TOML 확장을 깔고 파일 맨 위에 스키마 한 줄을 얹어두면 자동완성과 진단을 받을 수 있다.

정작 중요한 것은 **어느 값이 이기는가**다. 문서는 해석 순서를 여섯 단계로 못 박는다.

| 순위 | 층 | 위치 |
|---|---|---|
| 1 (최우선) | CLI 플래그와 `--config` 오버라이드 | 명령줄 |
| 2 | 프로젝트 설정 | `.codex/config.toml` (루트 → cwd 순, 가까운 것이 이김 · 신뢰한 프로젝트만) |
| 3 | 프로필 | `~/.codex/profile-name.config.toml` (`--profile`로 선택) |
| 4 | 사용자 설정 | `~/.codex/config.toml` |
| 5 | 시스템 설정 | `/etc/codex/config.toml` (Unix, 있을 때만) |
| 6 | 내장 기본값 | — |

표 1. `config.toml` 값 해석 순서 (2026-08-02 문서 기준)

이 표에서 실무적으로 가장 자주 물리는 곳은 2번 줄 끝의 괄호다. **신뢰하지 않은 프로젝트에서는 프로젝트 범위 `.codex/` 층이 통째로 건너뛰어진다.** 설정과 함께 훅과 규칙까지 빠진다. 사용자·시스템 층은 그대로 로드되므로 Codex 자체는 멀쩡히 돌아가고, 그래서 증상이 더 헷갈린다. "저장소에 설정을 넣어뒀는데 하나도 안 먹는다" 싶으면 문법보다 신뢰 여부를 먼저 확인하는 편이 낫다.

문서가 권하는 운용은 세 계층으로 단순하다. 개인 기본값은 `~/.codex/config.toml`에, 저장소마다 다른 값은 `.codex/config.toml`에, 그리고 일회성은 명령줄에 둔다.

```bash
codex --profile deep-review
codex --config model_reasoning_effort='"high"'
```

`--profile`은 `~/.codex/profile-name.config.toml`을 얹는 방식이라, 리뷰용·실험용처럼 묶음으로 달라지는 값을 통째로 갈아끼우기 좋다. `-c`/`--config`는 TOML로 파싱되므로 문자열 값에는 따옴표가 한 겹 더 필요하다는 점만 주의하자.

오타에 대한 방어책도 하나 있다. 기본 동작은 알 수 없는 키를 무시하는 것인데, `--strict-config`로 띄우면 그런 키를 오류로 처리한다. 설정을 크게 손본 직후에 한 번 돌려보자. 조용히 무시되고 있던 줄이 그때 드러난다.

마지막으로 `[features]` 테이블이 있다. 선택적·실험적 기능을 켜고 끄는 자리인데, 성숙도 라벨이 표 안에 함께 적혀 있다는 점이 이 테이블의 미덕이다.

| 키 | 기본값 | 성숙도 |
|---|---|---|
| `hooks` | true | Stable |
| `goals` | true | Stable |
| `multi_agent` | true | Stable |
| `memories` | **false** | **Experimental** |
| `web_search` | true | Deprecated (상위 `web_search` 설정을 쓸 것) |

표 2. `[features]` 테이블에서 자주 건드리는 항목 (2026-08-02 문서 기준 · 원문 표의 일부)

`codex --enable feature_name`으로 한 번만 켤 수도 있다. 다만 Experimental·Deprecated 라벨이 붙은 줄은 예고 없이 바뀔 수 있으니, 여기 적힌 기본값을 외우기보다 자기 버전에서 표를 직접 열어보자.

## `/debug-config` — 왜 내 설정이 안 먹히는가

층이 여섯 개나 되면 반드시 생기는 증상이 있다. 분명히 값을 넣었는데 다르게 동작하는 것이다. 이럴 때 어디부터 봐야 할까? 파일을 다시 들여다보며 오타를 찾는 건 대개 헛수고다. 값은 멀쩡한데 **다른 층이 이기고 있는** 경우가 훨씬 많기 때문이다.

문서도 같은 진단을 내놓는다.

> "Many quality issues are really setup issues, like the wrong working directory, missing write access, wrong model defaults, or missing tools and connectors."

품질 문제로 보이는 것의 상당수가 실은 설정 문제라는 얘기다. 잘못된 작업 디렉터리, 없는 쓰기 권한, 어긋난 모델 기본값, 빠진 도구와 커넥터. 앞 절에서 본 신뢰하지 않은 프로젝트 문제도 정확히 이 목록의 성격이다.

그래서 Codex는 진단 명령을 두 개 준비해뒀다. `/status`는 지금 이 세션의 결과를 보여준다. 활성 모델, 승인 정책, 쓰기 가능 루트, 토큰 사용량. 반면 `/debug-config`는 그 결과가 어떻게 만들어졌는지를 보여준다. 설정 층이 우선순위 순서(낮은 것부터)로 나열되고, 각 층의 on·off 상태와 정책의 출처가 함께 찍힌다. 출력에는 `allowed_approval_policies`·`allowed_sandbox_modes`·`mcp_servers`·`rules` 같은 항목이 포함되고, 설정돼 있다면 `enforce_residency`·`experimental_network`까지 나온다. 문서가 이 명령의 용도를 한 줄로 적어둔 것이 정확하다 — 실효 설정이 `config.toml`과 다른 이유를 디버깅하는 데 쓰라는 것이다.

이 명령을 언제 쓰면 좋을까. 2장에서 임포트 직후 절차의 마지막 단계로 `/debug-config`를 넣어둔 이유가 여기 있다. 남의 도구에서 옮겨온 설정은 어느 층에 떨어졌는지가 눈에 보이지 않고, 그 상태로 승인·샌드박스를 만지면 진단이 두 배로 어려워진다. 옮긴 직후에 한 번, 그리고 "왜 이러지" 싶을 때마다 한 번. 이 두 시점이면 충분하다.

한 가지 예고를 붙여둔다. 지금까지 본 여섯 층은 **내 컴퓨터 안에서 끝나는 층**이다. 조직이 관리하는 기기에서는 `requirements.toml`이라는 층이 하나 더 얹히고, 그 층은 사용자가 덮을 수 없다. 관리자가 `approval_policy = "never"`나 `sandbox_mode = "danger-full-access"`를 금지해뒀다면 내 `config.toml`에 뭘 적든 그 값은 서지 않는다. `/debug-config`의 출력에 정책 출처가 함께 나오는 것도 이 때문이다. 이 이야기는 11장에서 제대로 다룬다.

## 무엇이 남고 무엇이 안 남는가

지침과 설정을 세우고 나면 그다음 질문이 자연스럽게 온다. 매번 다시 설명하지 않아도 되는 것들은 어디에 쌓이는가?

Codex는 이 자리를 세 층으로 나눠뒀다.

첫째, 개인 지침. 성격(personality)을 Friendly·Pragmatic·None 중에서 고르고, 응답 스타일 같은 개인 취향은 커스텀 인스트럭션으로 둔다. 여기서 짚어둘 것이 하나 있다. 문서에 따르면 Codex에서 이 개인 지침은 **전역 `AGENTS.md` 파일에 저장된다.** 설정 UI에서 만졌든 파일을 직접 열어 적었든 도착지는 같은 곳이라는 뜻이다. 이 층은 별도의 저장소가 아니라 지침 체인의 맨 첫 칸이다. 전역 파일에는 "나와 어떻게 대화할지"를 두고 저장소 파일에는 "이 코드베이스의 규칙"을 두라던 권고가 여기서 그대로 이어진다.

둘째, 메모리. 이전 작업에서 얻은 맥락을 다음 작업으로 실어 나르는 층이다. ChatGPT 웹은 ChatGPT 메모리를 쓰고, 로컬 Codex 클라이언트는 별도의 로컬 메모리 저장소를 쓴다. 두 저장소가 다르다는 점은 기억해둘 값어치가 있다. 웹에서 나눈 대화가 로컬 세션의 메모리로 흘러들지 않는다는 뜻이기 때문이다. 대화 단위 제어는 `/memories`로 한다 — 이 대화가 기존 메모리를 쓸지, 그리고 앞으로의 메모리에 재료가 될지를 각각 정한다. `[features]` 표가 보여주듯 이 기능은 기본값이 `false`이고 라벨은 Experimental이다. 켜야 쓸 수 있고, 켜더라도 동작이 바뀔 수 있다.

셋째, Chronicle. 화면에서 최근 맥락을 끌어와 메모리를 보강하는 기능이다. 다만 여기에는 조건과 경고가 촘촘히 붙어 있다. opt-in 리서치 프리뷰이고, macOS의 ChatGPT Pro 구독자만 쓸 수 있으며, 화면 녹화와 손쉬운 사용 권한을 요구한다. 문서 자신이 켜기 전에 알아야 할 위험을 세 가지로 적어둔다 — 사용량 한도를 빨리 소모하고, 프롬프트 인젝션 위험을 높이며, 메모리를 기기에 **암호화하지 않은 채** 저장한다. 자기 기능의 위험을 이만큼 앞세워 적어둔 문서는 흔치 않으니, 켜기 전에 그 절을 직접 읽어보길 권한다. Chronicle이 어떤 성격의 표면인지는 12장에서 다시 만난다.

세 층을 관통하는 원칙은 문서가 한 문장으로 정리해준다.

> "Keep required team guidance in `AGENTS.md` or checked-in documentation. Treat memories as a helpful recall layer, not as the only source for rules that must always apply."

**반드시 적용돼야 하는 규칙은 메모리에 맡기지 않는다.** 메모리는 도움이 되는 회상 층으로만 다루고, 항상 적용돼야 하는 것은 `AGENTS.md`나 체크인된 문서에 둔다. 이유는 간단하다. 메모리는 내 기기에 쌓이지만 저장소 파일은 팀 전체에 쌓인다. 개인화 층이 아무리 편해도 이 선은 지키는 편이 낫다.

## 어느 문서를 열어야 하는가

1장에서 표면이 여럿이라고 했다. 설정 문서도 그만큼 갈라져 있다. 어느 페이지를 열어야 하는지 헷갈릴 때 쓸 지도를 한 장 만들어두자.

| 표면 | 담당 문서 | 설정 위치 | 개인화 가능 항목 | 주의 |
|---|---|---|---|---|
| ChatGPT 데스크톱 앱 | `/codex/reference/settings` | 앱 Settings UI (+ `[desktop]`은 **Open in 커스텀 파일 핸들러 전용**) | 성격·커스텀 인스트럭션·메모리·알림·외형·펫·브라우저·Computer Use | 개인화 항목 대부분이 **Settings > Personalization** 한 곳에 모여 있다 |
| IDE 확장 | `/codex/ide` · `/codex/config-file/config-basic` | CLI와 **같은 설정 층**을 공유 | 기어 아이콘 > Codex Settings > Open config.toml | 열린 파일이 자동으로 컨텍스트에 들어간다(1장) — 설정이 아니라 표면 특성이다 |
| CLI | `/codex/developer-settings` | `~/.codex/config.toml` · `.codex/config.toml` · `--profile` · `-c` | `/model`·`/permissions`·`/personality`·`/keymap`·`/statusline`·`/theme`·`/vim` | TUI 피커는 세션 한정인 것과 저장되는 것이 섞여 있다 |
| Windows · WSL | `/codex/windows/windows-app` · `/codex/windows/wsl` | 위와 같음 + `[windows]` 테이블 | `sandbox = "elevated"`(권장) / `"unelevated"`(폴백) | 관리자 권한이 없거나 elevated 설정이 실패할 때만 `unelevated`를 쓴다 |

표 3. 표면별 설정 지형도

표에서 가장 중요한 줄은 두 번째다. **CLI와 IDE 확장은 같은 설정 층을 공유한다.** 두 표면을 오가며 쓰는 사람에게 이건 좋은 소식이다. 한 번 세워둔 `config.toml`이 양쪽에 그대로 적용되니 이중 관리가 필요 없다. 반대로 데스크톱 앱은 자기 UI에서 바꾸는 항목이 많으므로, "CLI에서 고쳤는데 앱에서는 왜 그대로지" 같은 상황이 생기면 표의 첫 줄을 먼저 떠올리는 게 빠르다.

TUI 피커에 대해서도 한 줄 덧붙인다. `/model`이나 `/personality` 같은 명령은 어떤 것은 이번 세션에만 적용되고 어떤 것은 저장할지 물어본다. 다음 세션에도 유지하고 싶으면 대응하는 설정 키를 직접 적어두는 편이 확실하다. `/statusline`이나 `/theme`처럼 선택 즉시 `config.toml`의 `[tui]` 아래에 남는 것도 있다. 어느 쪽인지 헷갈릴 때는 피커에서 고른 뒤 파일을 열어보면 바로 확인된다.

윈도우 사용자를 위해 한 줄 더. 네이티브로 돌릴 때는 `[windows]` 테이블의 샌드박스 모드를 `elevated`로 두는 것이 문서의 권장이고, `unelevated`는 관리자 권한이 없거나 elevated 설정이 실패할 때 쓰는 폴백이다. WSL 쪽은 리눅스 환경을 선호하는 사람을 위해 계속 남아 있는 선택지다.

마지막으로 두 도구를 함께 쓰는 사람들이 자주 부딪히는 문제를 하나 짚자. 지침 파일을 양쪽에 하나씩 두면 곧바로 이중 관리가 시작된다. 한쪽만 고치고 다른 쪽을 잊는 일이 반복되면 어느 쪽이 진짜인지 알 수 없게 된다. Hacker News의 한 사용자(steve-atx-7600, 2026-07-09)가 자기 방식을 이렇게 적었다.

> "I was a claude only user and just have my user level `AGENTS.md` for codex and others simply point at my user `CLAUDE.md`. Have a script that syncs my skills (just directories) between all models."

사용자 레벨 `AGENTS.md`가 기존 파일을 가리키게 하고, 스킬은 디렉터리 동기화 스크립트로 맞춘다는 것이다. 익명 사용자의 개인 운용법이고 공식 문서가 보증하는 구성은 아니다. 그럼에도 소개할 값어치가 있는 이유는 방향이 앞에서 본 문서 권고와 같기 때문이다 — 전역 파일은 "나"를 담고, 저장소 파일은 "이 코드베이스"를 담는다. 전역 층에 한 번만 포인터를 두면 개인 취향은 한 곳에서만 관리된다.

여기까지 왔으면 오늘 자기 환경에서 해볼 일이 하나 정해진다. **평소 Codex를 띄우는 그 디렉터리에서, 아래 한 줄을 실행해보자.**

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

돌아온 요약에 당신이 기대한 규칙이 전부 들어 있는지 확인하면 된다. 빠진 게 있다면 원인은 셋 중 하나다. 파일이 탐색 경로 위에 없거나(위치를 옮기거나 그 디렉터리에서 연다), 32 KiB 예산에 걸렸거나(`project_doc_max_bytes`를 올리거나 쪼갠다), 이름이 목록에 없거나(`project_doc_fallback_filenames`에 얹는다). 세 원인 모두 이 장에서 손잡이를 봤다. 확인에 드는 시간은 1분이고, 이 1분이 "왜 시킨 대로 안 하지"라는 의문을 몇 주치 줄여준다.

### 이 장의 핵심

- `AGENTS.md`는 **피드백 루프의 저장소**로 다룬다. 같은 실수가 두 번 나오면 회고를 시키고 그 결과를 파일에 반영한다.
- 지침에는 **32 KiB(`project_doc_max_bytes`) 예산**이 있고, 결합 크기가 한도에 닿으면 뒤쪽이 붙지 않는다. 한도를 올리거나 지침을 나눈다.
- 지침 탐색은 **루트에서 현재 디렉터리까지 내려오며** 이뤄지고 거기서 멈춘다. cwd 아래의 파일은 읽히지 않으므로, 지침은 "작업을 시작하는 위치"를 기준으로 배치한다.
- 설정 값은 **여섯 층**에서 해석된다. 신뢰하지 않은 프로젝트에서는 `.codex/` 층이 통째로 빠지므로, 저장소 설정이 안 먹으면 문법보다 신뢰 여부를 먼저 본다.
- 실효 설정이 파일과 다를 때는 `/status`로 결과를, **`/debug-config`로 그 결과가 만들어진 층 순서**를 확인한다.
