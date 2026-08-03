# 3장. 손이 먼저 기억한다 — 첫 주에 나는 사고들

> "I don't get it. So is there 'rewind' feature in Codex CLI or not? E.g. i am used to Claude code. I can REWIND changes OR conversation OR both. I don't care about the damn conversation rewind :) It's important that i can revert / rewind the changes agent made if things go sideways!"
>
> — archneon, GitHub 이슈 [#11626](https://github.com/openai/codex/issues/11626) 댓글 (2026-02-17)

> "No - the `rewind` or `undo` does NOT exist in Codex CLI. Hence this issue. We really need it."
>
> — Alek2077, 같은 스레드 (2026-02-17, 그 스레드에서 반응이 가장 많이 붙은 답변)

이 두 댓글 사이의 간격이 전환 첫 주에 벌어지는 일의 거의 전부다.

앞사람은 Claude Code를 쓰던 손으로 <kbd>Esc</kbd>를 두 번 눌렀다. 화면의 대화는 깔끔하게 되감겼다. 그래서 코드도 함께 돌아왔으리라 믿었다. 그리고 파일을 열어봤다. 수정은 그대로 남아 있었다. "대화 되감기는 아무래도 상관없다"는 그 투덜거림에는, 되돌렸다고 믿은 채로 다음 작업을 얹었을지 모른다는 서늘함이 깔려 있다.

앞 장에서 우리는 임포트로 설정을 옮겼다. `CLAUDE.md`는 `AGENTS.md`가 됐고, `settings.json`은 `config.toml`이 됐고, 슬래시 명령은 스킬로 접혔다. 파일은 전부 제자리를 찾았다. 그런데 왜 사고가 나는가?

옮겨지지 않은 것이 하나 있기 때문이다. **손이다.** 이주는 파일을 옮기는 일이지만 전환은 손을 옮기는 일이고, 손은 설정 파일처럼 한 번에 복사되지 않는다. 게다가 손버릇은 이름을 보고 움직인다. 이름이 같으면 같은 결과를 기대하게 되는데, 그 기대가 틀렸다는 사실은 대개 되돌릴 수 없게 된 워킹 트리가 알려준다.

그래서 이 장은 사고 기록에 가깝다. 첫 주에 실제로 사람들이 어디서 넘어졌는지를 이슈 번호와 함께 따라가보자. 넘어진 자리를 알면 같은 자리는 피할 수 있다.

## 위험한 순서대로 — 첫 주의 사고 세 가지

새 도구를 배울 때 우리는 보통 문서를 위에서부터 읽는다. 전환자는 그렇게 배우면 손해다. 이미 아는 것이 90%이고 나머지 10%가 사고를 내는데, 문서는 그 10%를 눈에 띄게 표시해주지 않기 때문이다. 위험도가 높은 순서로 셋만 먼저 보자 (2026-08-02 문서 기준).

**ⓐ `/clear`는 새 chat을 연다.** Codex CLI 문서는 `/clear`의 동작을 이렇게 적는다.

> "Codex clears the terminal, resets the visible transcript, and starts a fresh chat in the same CLI session."

터미널을 지우고, 보이던 트랜스크립트를 초기화하고, 같은 CLI 세션 안에서 새 chat을 시작한다. Claude Code에서 `/clear`는 컨텍스트 초기화다. 이름이 같으니 손이 먼저 나간다. 문제는 여기서 시작된다. Codex에서 그 한 번의 타이핑은 화면 스크롤백까지 함께 날려버린다. 방금 에이전트가 어떤 파일을 왜 고쳤는지 눈으로 되짚으려던 근거가, 컨텍스트를 비우겠다는 의도만으로 사라지는 것이다.

억울한 건, 문서가 대안까지 친절하게 적어뒀다는 점이다.

> "Unlike <kbd>Ctrl</kbd>+<kbd>L</kbd>, `/clear` starts a new chat."
> "<kbd>Ctrl</kbd>+<kbd>L</kbd> only clears the terminal view and keeps the current chat."

읽고 나면 단순하다. 한 덩어리였던 손버릇을 셋으로 쪼개면 된다. 화면만 정리하고 싶다면 <kbd>Ctrl</kbd>+<kbd>L</kbd>이다. 화면은 남긴 채 새 chat만 열고 싶다면 `/new`가 있다 — 문서는 여기서도 대비를 명시한다. "Unlike `/clear`, `/new` doesn't clear the current terminal view first." 그리고 긴 대화가 무거워져서 정리하려던 것이라면, 애초에 필요한 건 `/compact`다. 요약으로 앞부분을 접어 토큰을 되찾는 쪽이 목적에 맞다.

작은 안전장치도 하나 있다. `/clear`와 <kbd>Ctrl</kbd>+<kbd>L</kbd>은 작업이 진행 중일 때는 둘 다 비활성화된다. 달리는 에이전트 위에 손이 미끄러지는 사고까지는 막아준다는 뜻이다.

**ⓑ <kbd>Esc</kbd> 두 번은 분기다.** 가장 위험한 항목이 여기다. 문서의 대화형 단축키 목록에 이렇게 적혀 있다.

> "Press <kbd>Esc</kbd> twice with an empty composer to edit the previous user message and fork the chat from that point."

빈 컴포저에서 <kbd>Esc</kbd>를 두 번 누르면 이전 사용자 메시지를 편집해 그 지점에서 chat을 fork한다. 문장 어디에도 파일 이야기가 없다. 분기는 대화에만 일어난다. 작업은 그대로다. 이슈 #11626의 재현 절차가 그 결과를 그대로 보여준다. ⓐ Codex CLI에 파일 수정을 요청한다 ⓑ <kbd>Esc</kbd>를 두 번 눌러 이전 메시지로 되감고 fork한다 ⓒ 대화는 되감기지만 **이전 파일 수정은 워킹 트리에 그대로 남는다.**

이 사고가 최고 위험인 이유는 파괴력이 커서가 아니라 **조용해서**다. 에러가 나지 않는다. 경고도 없다. 화면상으로는 분명히 그 시점으로 돌아왔고, 그래서 우리는 되돌아간 세계를 전제로 다음 지시를 내린다. 두 번, 세 번 그렇게 쌓이고 나면 워킹 트리에는 되돌린 줄 알았던 수정과 새 수정이 뒤엉켜 있다. 이쯤 되면 뒷맛이 찜찜한 정도를 넘어 아찔하다.

그렇다면 어떻게 해야 할까? 도구가 안 해주는 일은 습관이 대신해야 한다. 같은 이슈 스레드에서 suparious가 내놓은 대응이 커뮤니티에서 가장 널리 받아들여진 형태다.

> "When you open codex in a repo, you must start from a clean git tree. ... I also always engineer in 'COMMIT but do not PUSH' in the context too. That way I am always the gatekeeper for changes to go into the repository."
>
> — suparious, #11626 댓글 (2026-05-01)

두 줄로 요약된다. 깨끗한 git 트리에서 시작하고, "커밋은 하되 푸시는 하지 마"를 지침에 박아둔다. 앞의 것은 되돌릴 기준점을 만드는 일이고, 뒤의 것은 되돌릴 수 있는 상태를 유지하는 일이다. `/rewind`가 없는 자리를 git이 메우는 셈인데, 이 대응에는 값이 붙는다 — 그 대가는 이 장 끝에서 다시 이야기하자.

**ⓒ 중첩 `AGENTS.md`는 자동으로 읽히지 않는다.** 세 번째는 워낙 큰 사안이라 다음 절 전체를 여기에 쓴다. 한 줄만 먼저 박아두자. Claude Code는 작업 디렉터리에서 위로 올라가며 지침 파일을 모두 로드해 연결하지만, **Codex는 중첩 `AGENTS.md`를 자동으로 로드하지 않는다.** 모노레포에서 패키지마다 규칙을 나눠 둔 사람이라면, 이주 직후의 Codex는 그 규칙들을 대부분 못 본 채로 일하고 있다.

지금까지 본 것과 앞으로 볼 것을 한 장에 모으면 이렇게 된다.

| 손버릇 | Claude Code에서의 결과 | Codex에서의 결과 | 위험도 | 대응 |
|---|---|---|---|---|
| `/clear` | 컨텍스트 초기화 | 터미널을 지우고 **새 chat 시작** | 높음 | 화면만 → <kbd>Ctrl</kbd>+<kbd>L</kbd> / 새 chat만 → `/new` / 컨텍스트 절약 → `/compact` |
| 되돌리기(<kbd>Esc</kbd> 두 번) | 대화·코드 양쪽 되돌리기 | **대화만 되감고 파일 수정은 워킹 트리에 남음** | 최고 | 깨끗한 git 트리에서 시작 + "커밋은 하되 푸시는 하지 마" |
| 중첩 지침 파일 | 상위로 올라가며 모두 로드·연결 | **중첩 `AGENTS.md`를 자동 로드하지 않음** | 최고 | 규칙을 루트로 합치거나 폴더마다 작성 (설정 손잡이는 4장) |
| 스킬 호출 접두사 | `/` | **`$`** (ChatGPT 표면은 `@`) | 중간 | 슬래시 목록에도 스킬이 뜨지만, 명시 호출은 `$` |
| 위험 플래그 이름 | `--dangerously-skip-permissions` | `--dangerously-bypass-approvals-and-sandbox` (별칭 `--yolo`) | 중간 | 평소엔 `--sandbox workspace-write`, 디렉터리는 `--add-dir`로 |
| 훅 커버리지 | 29+ 이벤트 (이슈 [#21753](https://github.com/openai/codex/issues/21753)이 대조군으로 제시한 수치) | **부분 지원** — `PreToolUse`/`PostToolUse`가 Partial | 높음 | 훅에 의존하는 검사는 이식 전 재확인 (6장) |

표 1. 손버릇 교정표 (2026-08-02 문서 기준)

여섯 줄 중 셋은 이번 장에서 이미 봤고, 넷째와 다섯째는 잠시 뒤에, 여섯째는 6장에서 다시 만난다. 이 표를 책상 옆에 두고 첫 주를 보내면 사고 대부분은 피할 수 있다.

## 폴더마다 다시 쓰게 만드는 것 — 중첩 `AGENTS.md`

모노레포를 쓰는 사람은 지침을 한 파일에 몰아넣지 않는다. 루트에는 공통 규칙을 두고, `packages/api`에는 API 규약을, `packages/web`에는 프런트 컨벤션을 따로 둔다. 도구가 작업 디렉터리에서 위로 올라가며 지침 파일을 전부 읽어 연결해준다는 전제 위에서 만들어진 구조다. 그 전제가 사라지면 어떻게 될까? 파일은 그대로 있는데 아무도 읽지 않는 상태가 된다. **지침이 없는 것보다 나쁘다.** 없으면 없는 줄이라도 알지만, 이쪽은 잘 관리하고 있다고 믿게 만들기 때문이다.

이슈 [#12115](https://github.com/openai/codex/issues/12115) "Dynamically loading nested AGENTS.md"가 이 문제를 다룬다. 2026-02-18 개설, 👍 102, open이다. 이 이슈를 특별하게 만드는 건 반응 수보다 이슈에 붙은 메타데이터다. 고객 요청으로 Wix가 제출자로 기록돼 있고(Andrew Ginns, 2026-05-05), 영향 계정으로 Stripe LLC가 우선순위 `Must have`로 올라 있다(최근 근거 2026-07-13). 대형 조직의 도입 블로커로 추적되고 있다는 뜻이다.

기술적 근거도 이슈 안에서 정리돼 있다. miraclebakelaser는 `AGENTS.md` 표준 문서 자체를 인용해 반박한다.

> "It's also part of the AGENTS.md standard: '4. Large monorepo? Use nested AGENTS.md files for subprojects... Agents automatically read the nearest file in the directory tree, so the closest one takes precedence.' For example, at time of writing the main OpenAI repo has 88 AGENTS.md files."
>
> — miraclebakelaser, #12115 댓글 (2026-02-18)

표준이 중첩을 권하고, OpenAI 자신의 저장소에도 `AGENTS.md`가 88개 있는데, 정작 Codex는 가장 가까운 파일을 알아서 읽어주지 않는다. 문서가 말하는 규칙과 도구가 실제로 하는 일이 어긋나는 지점이다.

이 어긋남의 비용은 정확히 무엇일까? 스레드에 답이 있다. 전환을 포기한 이유로 이 항목을 직접 지목한 댓글이 둘이다.

> "This is keeping me from switching from Claude Code, it's really tough to have pretty well-configured AGENTS.md files everywhere only to have Codex ignore them entirely."
>
> — anrooo, #12115 댓글 (2026-05-15)

> "Will be staying on Claude Code until this is fixed."
>
> — leonardo-panseri, #12115 댓글 (2026-06-04)

기능 요청 스레드에서 "이래서 안 옮긴다"는 말이 나오는 건 흔치 않다. 대개는 불편하다는 선에서 멈춘다. 여기서 사람들이 전환 자체를 접는 이유는, 이 문제가 **관리 방식 전체를 바꾸라고 요구**하기 때문이다. 한 번 고치고 끝나는 설정 항목과는 무게가 다르다.

한국어로 남은 1차 증언도 같은 지점을 짚는다. dcinside 특이점갤의 코유키1357이 2026-04-28에 올린 글이다(조회 7,507).

> "코덱스의 경우 hook은 있는데 rules가 없어 각 폴더 루트마다 AGENTS.md를 작성해야하고 이로 인해 프롬프트 관리가 까다로워지는 문제가 있음"

"각 폴더 루트마다 작성해야 하고"라는 표현이 정확하다. 자동 로드가 없으니 남는 선택지는 둘뿐이다. 규칙을 루트 한 파일로 모으거나, 필요한 폴더마다 사람이 직접 챙기거나. 전자는 파일이 비대해지고 관련 없는 규칙까지 매번 컨텍스트에 실린다. 후자는 관리 지점이 폴더 수만큼 늘어난다. 어느 쪽이든 이전보다 손이 더 간다.

여기서 한 가지 덧붙일 게 있다. 이 문제에는 설정 손잡이가 몇 개 있고, 파일명 자체를 바꾸는 방법도 있다. 다만 그 손잡이들은 지침·설정을 통째로 다시 세우는 다음 장의 소재다. 지금 이 장에서 가져갈 결론은 하나로 충분하다. 임포트가 끝난 직후, 내 저장소의 `AGENTS.md`가 몇 개이고 **그중 몇 개가 실제로 읽히고 있는지** 확인하자. 이 확인을 건너뛴 채 "지침을 옮겼다"고 넘어가는 것이, 첫 주에 가장 조용히 손해를 보는 길이다.

한국어 후기가 이 한 건뿐이라는 사실도 그대로 적어둘 만하다. 이 책을 준비하며 국내 커뮤니티를 훑었지만, 전환 경험을 구체적으로 남긴 한국어 1차 자료는 놀랄 만큼 적었다. 남의 후기로 검증할 수 없다면 스스로 확인하는 수밖에 없다는 뜻이기도 하다.

## 여덟 줄짜리 원장 — 마찰은 어디에 모여 있는가

국내에 실명과 소속을 밝힌 심층 비교가 하나 있다 — Kyutae Park(AWS AI 스페셜리스트 SA), AWS 한국 기술블로그, 2026-06-11. 두 도구의 실행 스타일 차이를 다룬 자료이고, 그 논의는 프롬프팅을 본격적으로 다루는 7장에서 꺼낸다. 여기서는 존재만 알아두자.

지금 필요한 건 다른 종류의 자료다. **번호가 붙은 마찰** 말이다.

도구 비교 글은 대체로 믿기 어렵다. 어느 쪽이 더 낫더라는 후기는 쓴 사람의 코드베이스와 그날의 모델 버전에 크게 좌우되고, 무엇보다 반박할 방법이 없다. 반면 GitHub 이슈는 성격이 다르다. 개설일이 있고, 반응 수가 있고, 상태가 있고, 재현 절차가 붙어 있으며, 무엇보다 지금 열어서 확인할 수 있다. 그래서 이 책은 전환 마찰을 이슈 번호로 다룬다.

한 가지 더 좋은 점이 있다. 이슈는 **누가 아쉬워하는지**까지 보여준다. 앞 절에서 본 것처럼 이슈 메타데이터에 기업 이름이 붙기도 하고, 댓글에는 "그래서 안 옮긴다"는 판단이 그대로 남는다. 마케팅 문구로는 절대 얻을 수 없는 종류의 정보다. 이 책이 다룰 마찰을 한 표에 모으면 이렇게 된다.

| 마찰 | 이슈 | 개설일 | 👍 | 상태 | 주 서술 장 |
|---|---|---|---|---|---|
| `/rewind` 부재 — 코드가 안 돌아간다 | [#11626](https://github.com/openai/codex/issues/11626) | 2026-02-12 | 192 | open | **3장** |
| 질문이 60초 뒤 자동 응답된다 | [#28969](https://github.com/openai/codex/issues/28969) | 2026-06-18 | 186 | open | **3장** |
| 중첩 `AGENTS.md` 미로드 (Wix·Stripe 신호) | [#12115](https://github.com/openai/codex/issues/12115) | 2026-02-18 | 102 | open | **3장** |
| macOS가 번들 `rg`를 차단한다 | [#28190](https://github.com/openai/codex/issues/28190) | 2026-06-14 | 79 | open | 9장 |
| Plan mode로 시작하는 기본 옵션이 없다 | [#13942](https://github.com/openai/codex/issues/13942) | 2026-03-08 | 34 | open | 7장 |
| 스킬 메타데이터 컨텍스트 예산 2% 하드코딩 | [#19679](https://github.com/openai/codex/issues/19679) | 2026-04-26 | 31 | open | 6장 |
| 훅 커버리지 부분 지원 | [#21753](https://github.com/openai/codex/issues/21753) | 2026-05-08 | 22 | open | 6장 |
| Claude 설정 마이그레이션이 사용자 config를 덮어쓴다 | [#24515](https://github.com/openai/codex/issues/24515) | 2026-05-26 | 0 | open | 2장 |

표 2. 전환 마찰 원장 (2026-08-02 문서 기준)

이 표는 이 장의 요약이자 남은 장들의 목차다. 위 세 줄은 이번 장이 맡고, 나머지는 각자 제 자리에서 다시 나온다. 마찰이 여덟 개나 되는데 왜 흩어 놓았을까? 마찰만 모아 한 장에 몰면 그 장은 불평 목록이 되고, 정작 필요한 대응은 어디에도 붙지 못하기 때문이다. 훅 커버리지는 확장 모델을 이야기하는 자리에서, Plan mode는 프롬프팅을 이야기하는 자리에서 다뤄야 대응까지 함께 손에 잡힌다. 원장은 지도 역할만 하면 된다.

한 가지 덧붙이면, 이 여덟 줄은 "Codex의 결함 목록"이 아니라 **"Claude Code를 쓰던 손이 걸려 넘어지는 지점"**의 목록이다. 둘은 다르다. Codex를 처음 배우는 사람에게는 대부분 문제가 되지 않는 항목들이고, 반대로 우리에게는 문서 어디에도 경고로 적혀 있지 않은 항목들이다. 기대가 있어야 배신도 있는 법이니까.

읽을 때 조심할 게 하나 있다. **반응 수는 위험도가 아니다.** 맨 아래 #24515를 보자. 👍가 0인데도 2장이 임포트 전 백업 절차를 따로 세운 이유가 이것이다 — 프로젝트 설정이 없을 때 사용자 레벨 `~/.codex/config.toml`을 덮어써 승인 폭탄을 만드는 사고다. 반응이 안 붙은 건 아마 사고를 당한 사람이 원인을 그 이슈와 연결짓지 못했기 때문일 것이다. 반대로 👍가 세 자리인 항목은 대개 매일 부딪히는 마찰이다. 두 축은 다르다.

또 하나. 여덟 줄이 **지금 전부 open**이다. 이걸 어떻게 읽어야 할까? 두 가지로 읽을 수 있다. 하나는 나쁜 소식이다 — 첫 주에 겪을 불편이 곧 사라지지는 않는다. 다른 하나는 좋은 소식에 가깝다. 이 여덟 줄은 공개적으로 추적되는 목록이고, 그래서 우리는 각 항목의 현재 상태를 언제든 직접 확인할 수 있다. 이 책을 읽는 시점에는 몇 줄이 닫혀 있을 것이다. 표를 외우는 대신 번호를 열어보는 습관을 들이는 편이 낫다.

## 글자 한 개 차이 — `$`, `@`, 그리고 `--yolo`

앞의 셋이 조용히 손해를 입히는 사고였다면, 이번 절의 것들은 시끄럽게 실패한다. 명령이 안 먹거나, 엉뚱한 팝업이 뜨거나, 아예 못 알아듣는다. 그래서 덜 위험하지만 더 자주 짜증난다.

먼저 스킬 호출 접두사다. Codex 문서는 이렇게 못 박는다.

> "ChatGPT supports `@` mentions, while Codex supports `$` mentions for skills."

Claude Code에서 스킬은 `/`로 부른다. Codex 개발자 표면에서는 `$`이고, ChatGPT 표면에서는 `@`다. 같은 제품 안에서도 표면에 따라 갈리는 셈이라, 데스크톱 앱과 CLI를 오가며 쓰는 사람은 하루에도 몇 번씩 헷갈린다.

여기에 함정이 하나 더 겹친다. CLI에서 `@`는 **파일 검색**이다. 문서의 대화형 단축키 항목에 그렇게 적혀 있다. "Type `@` to search for a file in the workspace and add its path to the prompt." 스킬을 부르려고 `@`를 쳤는데 파일 목록이 뜨는 이유가 이것이다. `/`도 여전히 쓸모가 있다. 슬래시 팝업에는 활성화된 스킬이 함께 나타나기 때문이다. 다만 **명시적으로 호출할 때의 문법은 `$`**라는 것만 손에 익히면 된다.

정리하면 이렇다. **`$`는 스킬, `@`는 (CLI에서) 파일, `/`는 명령.** 세 글자를 각각 다른 서랍에 넣어두자.

접두사 하나가 뭐 그리 대수인가 싶을 수 있다. 다만 이 차이는 두 제품이 확장 기능을 어떻게 바라보는지를 압축해 보여준다. 앞 장에서 임포트 매핑을 볼 때 이미 한 번 마주쳤다 — 슬래시 명령이 스킬로 접혔다. 명령과 스킬을 한 서랍에 넣는 쪽과, 명령은 명령대로 두고 스킬에 별도의 문법을 주는 쪽. 손끝의 글자 한 개는 그 설계 차이가 표면으로 튀어나온 자리다.

다음은 위험 플래그다. 이름이 길어서 오히려 다행인 경우다.

| | 플래그 |
|---|---|
| Claude Code | `--dangerously-skip-permissions` |
| Codex | `--dangerously-bypass-approvals-and-sandbox` (별칭 `--yolo`) |

표 3. 위험 플래그 이름 대조

익숙한 쪽을 그대로 치면 당연히 안 먹는다. 이건 사고라기보다 재학습 비용이다. 진짜 주의할 점은 **범위**다. Codex 쪽 플래그 이름을 천천히 읽어보자 — 승인(approvals)과 샌드박스(sandbox)를 **둘 다** 우회한다고 적혀 있다. 승인과 샌드박스가 별개의 축이라는 사실이 플래그 이름에 박혀 있는 것이다. 이 구분이 왜 결정적인지는 5장에서 세 개의 축으로 제대로 풀어보자.

문서 자신의 권고도 분명하다.

> "Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM."
> "When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`."

자리를 비운 채 돌릴 거면 `--sandbox workspace-write`를 쓰고, 디렉터리가 더 필요하면 권한 등급을 올리지 말고 `--add-dir`로 필요한 만큼만 열어라. 전권을 주고 싶은 유혹이 들 때마다 이 두 줄을 떠올리면 좋겠다.

마지막으로 자주 검색해서 만나게 되는 함정 하나. **`--full-auto`는 이미 deprecated다.** 문서의 플래그 표에 "Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used."라고 적혀 있다. 인터넷의 조금 오래된 글들이 여전히 이 플래그를 추천하고 있으므로, 경고 문구를 보고도 "원래 이런가 보다" 하고 넘기지 않도록 기억해두자. 경고는 대개 미래의 제거 예고다.

## 달리는 중에 말 걸기 — Steering과 Queuing, 그리고 60초

에이전트가 일하는 중에 뭔가를 덧붙이고 싶어지는 순간이 있다. "아, 그 파일은 건드리지 마"라거나 "끝나면 테스트도 돌려줘" 같은 것들이다. 이 둘은 성격이 완전히 다르다. 앞의 것은 **지금 이 실행을 바꾸는** 말이고, 뒤의 것은 **끝난 다음에 할 일**이다. Codex는 이 둘에 각각 이름을 붙여 나눠뒀다.

> "Steer adds the message to the current run. Use it to change direction, add a missing detail, or share new information."
> "Queue saves the message for the next run. Use it for a follow-up that should wait until the current work finishes."

CLI에서는 키가 다르다. 작업 중에 <kbd>Enter</kbd>를 누르면 현재 턴에 지시가 주입되고(steer), <kbd>Tab</kbd>을 누르면 다음 턴을 위해 저장된다(queue). 슬래시 명령이나 셸 명령도 같은 방식으로 큐에 넣을 수 있는데, 큐에 들어간 슬래시 명령은 실행될 때 파싱되므로 메뉴나 오류가 현재 턴이 끝난 뒤에야 나타난다. 미리 알아두지 않으면 "명령을 쳤는데 아무 반응이 없다"고 오해하기 쉽다.

데스크톱 앱에서는 기본 동작을 **Settings > General > Follow-up behavior**에서 고른다. 큐에 든 메시지는 컴포저 위에 쌓여서 편집·재정렬·전송·삭제가 가능하고, 기본값을 바꾸지 않은 채 이번 한 번만 반대로 동작시키는 단축키도 그 설정 화면에 표시된다. IDE 확장 쪽에는 `chatgpt.followUpQueueMode` 설정 키가 따로 있고 기본값은 `queue`다.

두 모드를 이렇게 이름·단축키·설정 키로 갈라 노출한 것은 Codex 쪽 특징이다 (사실 확인 필요). 익숙한 감각으로 <kbd>Enter</kbd>를 눌러 "그 파일은 건드리지 마"를 보냈는데 그게 다음 턴으로 미뤄진다면, 하지 말라고 한 일이 이미 끝난 뒤에 지시가 도착한다. 반대로 다음 턴에 시키려던 일이 지금 실행에 끼어들면 방향이 어긋난다. 첫날에 이 키 두 개부터 확인해두자. 손버릇 교정 중 가장 값싸고 효과가 큰 항목이다.

다만 이 steering 감각을 정면으로 배신하는 동작이 하나 보고돼 있다. 이슈 [#28969](https://github.com/openai/codex/issues/28969) "Add setting to disable the auto-resolve in 60 seconds for questions"다. 2026-06-18 개설, 👍 186, open — 전환 마찰 원장에서 두 번째로 큰 항목이다. 재현 절차는 이렇다. ⓐ plan mode로 들어간다 ⓑ 모델이 질문을 하게 만드는 프롬프트를 쓴다 ⓒ 질문에 답할 시간이 **60초**뿐임을 확인한다. 그 안에 답하지 않으면 Codex가 권장 답을 스스로 수락하고 진행한다.

스레드의 반응은 격했다.

> "Who thought this was a good idea to auto enable for everyone?"
>
> — ScyDev, #28969 댓글 (2026-06-28)

> "This is a blocker for everyone using Codex for proper planning and production level development and renders the `request_user_input` tool completely useless."
>
> — gergo-hortobagyi, #28969 댓글 (2026-06-24)

불평에서 끝나지 않는다. 계획 도구로서의 신뢰를 문제 삼고, 나아가 실패하는 편이 낫다는 말까지 나온다.

> "If your project has high complexity, 60 seconds is simply too little. ... I'd honestly prefer an option for the tool to fail rather than the bot merrily implementing changes I did not request."
>
> — irm-codebase, #28969 댓글 (2026-06-28)

마지막 문장이 이 마찰의 핵심을 짚는다. 사람에게 물어놓고 사람이 답하기 전에 스스로 답해버리는 것은, 계획 단계에서 사람을 관문에 세우겠다는 약속 자체를 무르는 일이다. 커피를 타러 다녀온 사이 결정이 끝나 있는 셈이다. 잠깐 자리를 뜰 생각이라면 질문이 나올 만한 프롬프트는 던져놓고 나가지 않는 편이 낫다. 그리고 이 항목이야말로 표를 외우지 말고 번호를 열어보라고 한 이유에 해당한다 — 설정 옵션이 추가됐는지 여부가 곧바로 작업 방식을 바꾸기 때문이다.

## 없던 서랍들 — 이름과 문법만 먼저

지금까지는 이름이 같은데 다르게 움직이는 것들을 봤다. 이제 반대쪽이다. 손이 아예 기억하지 못하는 것들, 즉 Codex에만 있는 조작이다. 여기서는 **무엇이 있고 어떻게 부르는지까지만** 익히자. 언제 쓰는 게 좋은지는 chat을 작업 단위로 쪼개는 원칙과 함께 7장에서 다루는 편이 자연스럽다. 도구를 먼저 알고 용도를 나중에 배우는 순서가 이 경우엔 맞다.

chat을 쪼개는 세 가지부터 보자. `/fork`는 현재 chat을 새 ID의 새 chat으로 복제한다. 원본 트랜스크립트는 손대지 않으므로 다른 접근을 나란히 시험해볼 수 있다. 저장된 세션을 복제하려면 터미널에서 `codex fork`를 실행해 세션 선택기를 연다. `/side`(별칭 `/btw`)는 조금 다르다. 본 chat에서 빠져나가지 않은 채 일회성 곁가지를 여는 것이고, 곁가지의 트랜스크립트는 부모와 분리된다. 곁가지에 있는 동안에도 TUI는 부모 chat의 상태를 계속 보여주므로 본 작업이 아직 돌고 있는지 확인할 수 있다. 다만 곁가지 안에서 또 `/side`를 열 수는 없고, 리뷰 모드에서도 쓸 수 없다.

지속 목표를 거는 `/goal`도 있다. `/goal <objective>`로 목표를 걸어두면 작업이 이어지는 동안 chat에 붙어 있는다. `/goal`만 치면 현재 목표를 보고, `/goal edit`으로 고치고, `/goal pause`·`/goal resume`·`/goal clear`로 멈추거나 지운다. 길이 제한이 있다는 점은 기억해두자 — 목표는 비어 있으면 안 되고 **최대 4,000자**다. 더 긴 지시가 필요하면 내용을 파일에 넣고 목표가 그 파일을 가리키게 하라고 문서는 권한다. 목표를 먼저 다듬고 싶다면 `/plan`으로 형태를 잡은 뒤 `/goal`로 확정하는 순서가 있다.

화면과 출력을 손보는 것들도 있다. `/raw`는 raw 스크롤백을 켜고 꺼서 터미널에서 선택·복사를 쉽게 만든다(<kbd>Alt</kbd>+<kbd>R</kbd> 기본 바인딩, `tui.raw_output_mode`로 고정 가능). `/statusline`은 푸터에 무엇을 어떤 순서로 띄울지 골라 `tui.status_line`에 남기고, `/title`은 터미널 창·탭 제목 항목을 정한다. `/theme`은 문법 강조 테마를 고른다.

입력과 응답 쪽은 이렇다. `/personality`는 응답 스타일을 고른다 — `friendly`, `pragmatic`, `none` 세 가지이고, 활성 모델이 지원하지 않으면 이 명령 자체가 보이지 않는다. `/keymap`은 TUI 단축키를 다시 매핑해 `config.toml`에 저장한다. `/vim`은 컴포저를 Vim 모드로 전환하며, 새 세션의 기본값으로 삼으려면 `tui.vim_mode_default = true`를 설정한다.

목록이 길다고 느껴진다면 정상이다. CLI 레퍼런스 한 페이지가 **전역 플래그 20개 + 서브커맨드 28개 + 내장 슬래시 명령 약 60개**를 한꺼번에 담고 있다. 처음부터 다 외울 필요는 없고, 그럴 수도 없다. 대신 문서를 뒤질 때 알아두면 좋은 함정이 하나 있다. 표면별 명령 페이지가 서로 별칭으로 중복돼 있다. 예를 들어 `/codex/cli/reference`와 `/codex/cli/slash-commands`는 바이트 단위로 같은 문서다. 이런 쌍이 여섯 개라, URL은 148개인데 고유 문서는 약 140개다. 두 URL을 다른 문서로 착각해 "여기엔 있는데 저기엔 없다"를 찾아 헤매지 않도록 하자.

## 편의에는 청구서가 붙는다

이 장이 준 것은 두 장의 종이다. 손버릇 교정표와 전환 마찰 원장. 이 둘만 있으면 첫 주에 나는 사고의 대부분은 넘길 수 있다. 그런데 그 편의가 무엇을 대가로 요구하는지도 정직하게 적어두자.

첫째, **되돌리기를 도구에서 습관으로 옮겨야 한다.** `/rewind`가 없는 자리를 깨끗한 git 트리와 "커밋은 하되 푸시는 하지 마"가 메운다고 했다. 이건 매 작업 앞에 붙는 세금이다. 작업을 시작하기 전에 트리를 정리하고, 지침에 관문 규칙을 박아두고, 에이전트가 끝날 때마다 diff를 눈으로 확인해야 한다. 도구가 대신 기억해주던 일을 사람이 떠맡는 것이므로, 잊으면 그날 그대로 사고가 난다.

둘째, **원장에는 유효기간이 있다.** 여덟 줄이 지금 전부 열려 있다는 사실은 곧 여덟 줄이 언젠가 닫힌다는 뜻이기도 하다. 이 표를 지식으로 외워두면, 고쳐진 뒤에도 고쳐지지 않은 세계에 맞춰 우회하고 있는 자신을 발견하게 된다. 표를 믿지 말고 번호를 열어보자.

셋째, **명령이 많다는 것 자체가 비용이다.** `/fork`와 `/side`와 `/goal`은 분명 없던 자유를 준다. 그러나 자유는 판단을 요구한다. 언제 갈라야 하고 언제 한 chat으로 밀어붙여야 하는지를 모르면, 늘어난 명령은 늘어난 혼란일 뿐이다.

세 장의 청구서를 다 받아들일 각오가 됐다면, 첫 주는 넘긴 셈이다.
