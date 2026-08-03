# 10장. 두 개의 "검토" — 코드 리뷰와 Codex Security

국내 커뮤니티에 이런 조언이 돌아다닌다. GeekNews의 한 댓글(bungker, 2026-04-15)이 그 통념을 짧게 요약한다.

> "클로드로 짜고 코덱스로 리뷰하는 것 추천. 시간 걸리지만 회의 전에 걸어두면 완료율 높음"

영어권도 다르지 않다. Hacker News의 한 사용자(superfrank, 2026-05-15)는 두 도구를 나눠 쓰는 이유를 이렇게 정리했다.

> "Claude is far better at front end design. I think it's still better at big picture planning. Codex is far better at code review and catching bugs that actually matter."

이 통념은 이 책이 수집한 자료 중 가장 널리 공유되는 실무 합의다. 그런데 같은 자료 더미 안에 이 합의를 절반쯤 무너뜨리는 증언도 함께 들어 있다. 그것을 남긴 사람은 통념대로 쓰다가 자기 결과를 의심해본 쪽이었다.

이 장은 그 증언에서 시작해 "검토"라는 단어가 Codex에서 두 개의 서로 다른 물건을 가리킨다는 데까지 간다. 하나는 방금 말한 코드 리뷰이고, 다른 하나는 Codex Security라는 별개 제품이다. 이름이 비슷해 섞어 부르기 쉬운데, 문서는 두 곳에서 직접 선을 긋는다.

## 리뷰를 시작하는 세 개의 입구

먼저 지형부터 보자. 코드 리뷰라는 말로 묶여 있지만, Codex에서 리뷰를 시작하는 입구는 어디이고 각각 무엇이 다를까? 경로는 세 개다.

첫째, TUI와 앱의 `/review`. ChatGPT Work나 Codex 안에서 `/review`를 치면 리뷰가 시작되고, 결과는 리뷰 페인에 인라인 코멘트로 표시된다. 범위는 네 가지 중에서 고른다 — base 브랜치 대비, 커밋되지 않은 변경, 특정 커밋, 그리고 커스텀 리뷰 지시.

둘째, CLI의 `codex review`. 비대화형으로 도는 경로이며, 대상 지정 플래그는 `--uncommitted`·`--base`·`--commit` 셋 중 **하나만** 쓸 수 있다. 셋은 서로 충돌하므로 스크립트에 두 개를 같이 넣으면 그 자리에서 막힌다.

셋째, GitHub PR의 `@codex review`. PR 코멘트로 리뷰를 요청하는 방식이고, 저장소에 Codex 코드 리뷰가 미리 활성화돼 있어야 한다. 범위를 좁힌 요청도 가능하다 — `@codex review for security regressions` 같은 형태다. 리뷰가 끝난 뒤 `@codex fix the P1 issue`로 수정까지 이어붙일 수 있다. 여기서 P0·P1이라는 우선순위 라벨이 등장하는데, 이 라벨은 다음 절에서 다시 만난다.

한 가지 구조적 사실을 알아두면 문서를 읽을 때 헷갈리지 않는다. 코드 리뷰 페이지는 **웹·앱·CLI·IDE 네 표면별로 본문이 갈린다.** 같은 `/review`라도 표면마다 스코프 선택지와 설정 키가 다르다는 뜻이다. 어느 표면 이야기인지 확인하지 않고 읽으면 자기 환경에 없는 옵션을 찾게 된다.

설정 쪽에는 토글이 둘 있다. **Code review**로 기능 자체를 켜고, **Automatic reviews**로 사람이 부르지 않아도 리뷰가 돌게 만든다. 자동 리뷰를 켤 때는 권한이 맞아야 하고, PR 리뷰를 쓰려면 GitHub CLI 인증이 미리 되어 있어야 한다. 리뷰 대화를 본 작업에서 떼어내는 분리형 리뷰 chat 모드도 설정에서 고를 수 있는데, 7장에서 세운 원칙을 떠올리면 이 선택지의 의미가 분명해진다. 리뷰는 그 자체로 하나의 결과 단위이므로 본 작업 chat에 섞지 않는 편이 낫다.

리뷰 페인 자체는 Git 상태를 그대로 보여준다. unstaged, staged, 커밋, 브랜치, 그리고 마지막 턴의 변경까지. 여기서 인상적인 것은 조작 입도다. 전체 diff 단위, 파일 단위, hunk 단위 세 층위로 stage하거나 되돌릴 수 있다. 리뷰 결과를 통째로 받거나 버리는 대신 조각으로 다룰 수 있다는 뜻이다.

리뷰 규칙은 4장에서 세운 지침 파일에 얹는다. `AGENTS.md`에 `## Code Review Rules` 섹션을 두면 그 규칙이 리뷰에 적용된다. 문서가 규칙 작성 지침을 네 줄로 정리해뒀는데, 그대로 옮길 값어치가 있다. 결과에 영향을 주는 저장소 고유 동작에 집중할 것("Focus on consequential, repository-specific behavior"), 안전한 우회로나 예외를 함께 적을 것("State the safe path or exception"), 범위를 좁게 잡고 오래 갈 규칙만 남길 것("Keep rules scoped and durable"), 그리고 기계적 검사는 CI에 맡길 것("Leave mechanical checks in CI").

마지막 항목이 이 절의 핵심 경계선이다. 문서는 코드 리뷰의 지위도 함께 못 박는다 — **필수 승인을 대체하지 않고, 테스트나 브랜치 보호를 대체하지도 않는다.** 리뷰 자동화를 도입하면서 기존 게이트를 걷어내는 것은 문서가 지지하지 않는 구성이다.

## 통념은 어디까지 사실인가

이제 서두의 증언으로 돌아가자. "리뷰는 Codex"라는 통념을 뒷받침하는 관측은 여럿이다. 앞서 본 superfrank 외에도, 다른 사용자(bottlepalm, HN 2026-07-08)는 이유를 한 단어로 짚었다.

> "Currently I use Opus mostly, Codex for code reviews because it is pedantic, and Fable for tough problems and high level design."

깐깐하다는 것이다. 리뷰에서는 그 성질이 미덕이 된다.

그런데 r/codex의 한 사용자(Ok_Economist3865, 2026-03-17)가 남긴 기록은 결이 다르다. 이 책이 수집한 커뮤니티 자료 중 유일한 정량적 자기 반증이라 길게 인용한다.

> "Heavy CC user here, around 2 months ago, i started using codex as well. Just out of curiosity I started using gpt 5.2 xhigh to review opus 4.5/4.6 code against a small task. Almost 90 percent of the time, I found critical issues. After a month I got tired and realized that there has to be something wrong with my prompts. Visited anthropic official prompt engineering guideline for opus 4.5/4.6, improved my prompts. Now 5.2xhigh review results into 25-40 percent issues, down from 90. Then one day I tried the reverse, how about gpt 5.2xhigh codes and opus reviews but nope, opus says no critical and high issues."

읽는 순서가 중요하다. 처음에는 통념대로였다. 한쪽 도구로 짠 코드를 다른 쪽으로 리뷰하니 90%에서 심각한 문제가 나왔다. 그런데 이 사용자는 그 숫자를 성과로 받아들이지 않고 자기 프롬프트를 의심했다. 공식 프롬프트 가이드대로 프롬프트를 고치자 지적률이 25~40%로 떨어졌다.

여기서 나오는 결론은 통념의 절반을 깎는다. **"리뷰가 문제를 많이 잡는다"의 상당 부분이 실은 리뷰 대상 코드를 만든 프롬프트의 품질 문제였다.** 도구가 예리했던 게 아니라 원본이 허술했던 것이다.

다만 통념이 통째로 무너지지는 않는다. 같은 기록의 마지막 문장이 남는다. 방향을 뒤집어 반대쪽으로 리뷰하게 했더니 심각·높음 등급이 하나도 나오지 않았다는 것이다. **지적률은 90%에서 25~40%로 내려왔지만, 역방향 비대칭은 그대로 남았다.** 이건 프롬프트로 설명되지 않는 부분이다.

세 가지를 함께 기억해두자. 이 관측은 익명 커뮤니티 진술이고, 특정 모델 세대(인용문에 적힌 그대로 `gpt 5.2 xhigh`와 `opus 4.5/4.6`)에서의 경험이며, 표본은 한 사람이다. 그럼에도 인용하는 이유는 이 자료가 자기에게 불리한 방향으로 검증을 진행한 유일한 사례이기 때문이다.

문서 자신도 리뷰 도구의 실패 모드를 인정한다.

> "models must be trained specifically to identify P0 and P1-level bugs, and tuned to provide concise, high-signal feedback; overly verbose responses are ignored just as easily as noisy lint warnings."

장황한 응답은 시끄러운 린트 경고만큼이나 쉽게 무시된다는 것이다. 리뷰 도구의 성능 지표가 "얼마나 많이 잡는가"가 아님을 벤더 문서가 스스로 적어둔 셈이다. P0·P1 라벨이 여기서 의미를 얻는다. 등급을 나누는 목적은 **읽힐 양으로 줄이는 데** 있다.

그러니 도입 기대치는 이렇게 조정하는 편이 낫다. 리뷰 자동화는 놓친 결함을 잡아주는 장치이면서, 동시에 **내 프롬프트 품질을 드러내는 거울**이다. 지적이 쏟아진다면 두 가설을 나란히 세워보자. 리뷰가 예리한 것인가, 아니면 생성 단계가 부실한 것인가.

한 가지 더. 문서에는 이런 문장도 있다 — "At OpenAI, Codex reviews 100% of PRs." 인상적인 수치지만 출처 표기가 없는 벤더 자체 주장이고, 어떤 기준으로 셌는지도 밝혀져 있지 않다. 그대로 인용하려면 이 단서를 함께 붙이는 편이 정직하다.

## 같은 단어, 다른 제품

지금까지 다룬 코드 리뷰와, 지금부터 다룰 Codex Security는 이름이 겹칠 뿐 다른 제품이다. 헷갈리는 사람이 많다는 것을 문서도 아는 듯, 실행 보안 페이지가 첫머리에서 직접 선을 긋는다.

> "This page covers how to operate Codex safely, including sandboxing, approvals, and network access. If you are looking for Codex Security, the product for scanning connected GitHub repositories, see [Codex Security]."

5장에서 다룬 샌드박스·승인·네트워크 통제는 에이전트를 안전하게 굴리는 이야기였다. 승인 요청을 모델이 심사하는 자동 리뷰어도 그쪽 소관이었다. 반면 Codex Security는 **코드에서 취약점을 찾는 별개의 애플리케이션 보안 제품**이다. 문서의 정의는 이렇다.

> "Codex Security is an application security agent that helps security and engineering teams find, confirm, and fix vulnerabilities. Use it in Codex, from your terminal, through the TypeScript SDK, or with connected GitHub repositories."

찾고, 확인하고, 고친다. 이 세 동사가 제품 구조를 그대로 요약한다. 그리고 쓰는 경로가 넷이라는 점도 함께 적혀 있다 — Codex 안에서, 터미널에서, TypeScript SDK로, 그리고 연결된 GitHub 저장소로. CLI와 SDK는 공개 npm 패키지 `@openai/codex-security`로 배포된다.

경계는 제품 내부에서 한 번 더 갈린다. 데스크톱의 Security 워크벤치와 Codex CLI는 플러그인을 쓰고, 클라우드 스캔은 Codex cloud를 통해 연결된 GitHub 저장소를 훑는다. 그리고 클라우드 쪽에는 라벨이 하나 붙어 있다 — 원문 표현으로 "currently in research preview"다(2026-08-02 문서 기준). 4장에서 세운 규칙대로, 라벨이 붙은 기능은 바뀔 수 있다는 전제로 다룬다.

두 주제가 만나는 접점도 정확히 둘이다.

하나는 실행 권한이다. CI에서 스캔이나 수정을 돌리려면 `codex exec`를 `--sandbox workspace-write`로 띄워야 한다. 9장에서 확인한 대로 기본값이 읽기 전용이기 때문이다. 스캔은 임시 산출물을 쓰기 위해 그 권한이 필요한데, 문서는 곧바로 조건을 붙인다 — 프롬프트가 여전히 체크아웃을 건드리지 말 것을 요구해야 한다는 것이다. 권한은 열되 지시로 좁히는 구성이다.

다른 하나는 계정 자격이다. "For best results, use an account verified for Trusted Access for Cyber." 이 문장은 관련 문서 네 곳에서 반복된다. 스캔 품질이 모델 능력 통제 정책과 직접 묶여 있다는 뜻이다. 뒤에서 볼 커뮤니티 관측 하나가 이 조건과 정면으로 연결된다.

제품의 자기 규정도 짚어두자. FAQ에 세 번의 "No"가 있다. 기존 정적 분석 도구(SAST)를 대체하는가 — 아니다, 보완한다("Codex Security complements SAST. It adds semantic, LLM-based reasoning and automated validation, while existing SAST tools still provide broad deterministic coverage"). 수동 보안 리뷰를 대체하는가 — 아니다. 패치를 자동으로 적용하는가 — 아니다. LLM 추론과 결정적 커버리지의 역할을 나눠 적은 이 자기 규정은, 보안 도구를 도입할 때 기대치를 세우는 출발점으로 쓸 만하다.

## 스캔 한 번의 수명주기

Codex Security 문서는 스무 페이지가 넘는다. 페이지를 하나씩 따라가면 길을 잃으므로, 실무에서 밟게 되는 순서로 다시 세워보자.

| 단계 | 무엇을 하는가 | 언제 쓰는가 | 산출물 | 주의 |
|---|---|---|---|---|
| 위협 모델 세우기 | 저장소 동작을 짧은 보안 요약으로 정리 | 스캔 전 1회, 그리고 결과가 어긋날 때마다 | 프로젝트 개요(편집 가능) | "결과가 이상하면 가장 먼저 고칠 것"이라고 문서가 지목한다 |
| 표준 스캔 | 저장소 또는 폴더를 넓게 훑는다 | 첫 실행과 정기 점검 | `report.md` + 구조화 데이터 | 모노레포는 소유자·보안 경계가 뚜렷한 폴더 하나로 좁힌다 |
| 딥 스캔 | 같은 범위를 더 깊게, 실행 간 편차를 줄여 | 표준 스캔을 한 번 돌린 뒤 | 위와 같음 + 상세 리포트 | 위임 워커가 필요하고 시간·자원이 더 든다. PR·diff에는 쓸 수 없다 |
| 변경 리뷰 | 바뀐 파일과 직접 관련된 코드만 본다 | PR·커밋 단위 회귀 점검 | 변경 범위 리포트 | 전체 감사로 확장하지 않는다. 브랜치를 대신 체크아웃해주지도 않는다 |
| 트리아지 | 외부에서 들어온 finding을 저장소 증거로 판정 | 스캐너 티켓·CVE·버그바운티 보고가 쌓였을 때 | 판정 + 순위 큐 | 각 finding을 **입증되지 않은 주장**으로 취급한다 |
| 수정·검증 | 패치와 회귀 테스트를 만들고 재현을 다시 시도 | 사람이 finding을 수락한 뒤 | 패치 초안 + 검증 증거 | 한 번에 하나씩. 여러 finding을 한 chat에서 고치지 않는다 |
| 내보내기·리포트 | 결과를 JSON·CSV·SARIF로 빼거나 티켓으로 만든다 | 기존 보안 워크플로에 넘길 때 | 내보내기 파일 / 이슈 초안 | 봉인된 스캔 번들 자체는 바뀌지 않는다 |

표 1. Codex Security 스캔의 실무 수명주기 (2026-08-02 문서 기준)

일곱 줄을 다 밟아야 하는 것은 아니다. 처음 도입한다면 위 두 줄까지만 하고 멈춰도 좋다. 위협 모델과 표준 스캔 한 번이 나머지 다섯 단계의 정확도를 좌우하기 때문이다. 아래 다섯 줄은 finding이 쌓이기 시작한 뒤에 하나씩 붙이면 된다.

이 표에서 가장 먼저 손대야 할 줄은 맨 위다. 위협 모델은 문서의 표현으로 "저장소가 어떻게 동작하는지에 대한 짧은 보안 요약"이며, 시스템은 이것을 이후 스캔·우선순위·검토의 컨텍스트로 쓴다. 첫 초안은 코드에서 자동 생성되는데, 문서가 붙인 조언이 명료하다 — 결과가 어긋난다고 느껴지면 **가장 먼저 고칠 것이 이 문서**라는 것이다.

무엇을 적는가도 네 항목으로 정해져 있다. 진입점과 신뢰할 수 없는 입력, 신뢰 경계와 인증 가정, 민감 데이터 경로나 특권 동작, 그리고 팀이 먼저 검토받고 싶은 영역. 문서의 예시 마지막 문장이 이 넷을 실전에서 어떻게 쓰는지 보여준다.

> "Focus review on auth checks, upload parsing, and service-to-service trust boundaries."

우선순위를 문장으로 지목하는 것이다. 4장에서 지침 파일을 다룰 때 봤던 원리가 여기서 반복된다. 에이전트에게 시스템의 경계를 글로 설명해주면 판정 품질이 올라가고, 결과가 이상하면 코드보다 컨텍스트 문서를 먼저 고치는 쪽이 빠르다.

저장소에 두는 파일도 하나 더 늘어난다. `SECURITY.md`다. 문서는 여기에 위협 모델, 보안 불변식, 보고 대상 finding의 기준, 제외 대상, 심각도 맥락을 적으라고 안내한다. 그리고 로딩 규약이 눈에 익다 — **디렉터리별 중첩 파일을 둘 수 있고, 정책이 충돌하면 코드에 가장 가까운 파일이 이긴다.** 4장에서 본 지침 체인과 같은 원리다. 역할 분담도 명시돼 있다. `SECURITY.md`는 보안 정책 컨텍스트를 담고, 빌드·검증 명령은 `AGENTS.md`에 남긴다.

여기에 조용하지만 중요한 단서가 붙는다.

> "Codex Security treats these files as policy context, not executable instructions."

정책 컨텍스트로만 다룬다는 것이다. 저장소 파일을 통한 프롬프트 인젝션을 의식한 설계이며, 남이 보낸 PR이 `SECURITY.md`를 고쳐 스캐너를 조종하는 경로를 막는다.

표준 스캔 한 번이 내부적으로 거치는 국면도 문서에 나열돼 있다. 위협 모델링, finding 발견, 검증, 영향·경로 분석, 리포팅, 구조적 하드닝, 그리고 마무리. 마지막 국면에서 구조화된 스캔 계약을 검증하고 `report.md`를 만든다. 이 순서를 알아둘 실익은 하나다. 문서가 덧붙인 경고가 그것을 말해준다 — 초기 후보만 보고 판단하거나 한 국면이 오래 걸린다고 중단하지 말고 완결된 결과를 기다리라는 것이다.

## 같은 설정으로 돌려도 결과가 달라진다

보안 스캐너에 기대하는 성질이 하나 있다. 같은 코드에 같은 설정이면 같은 결과가 나와야 하지 않을까? 규칙 기반 도구라면 당연한 요구다. 그런데 Codex Security는 그 기대를 문서에서 직접 꺾는다.

> "AI-assisted scans can vary, even with the same scan configuration."

제품이 자기 비결정성을 스스로 명문화한 문장이다. 이 한 줄이 이 절 전체의 전제가 된다. 편차가 있다는 사실을 받아들이고 나면, 문서가 마련해둔 장치들이 왜 그런 모양인지 읽히기 시작한다.

첫째 장치는 딥 스캔이다. 딥 스캔의 정의부터가 편차 이야기다 — 저장소를 더 넓게 훑고 "실행 간 편차를 줄일 수 있다"고 적혀 있다. 표준과 딥의 차이를 문서가 표로 정리해뒀는데, 흥미로운 것은 범위(Scope) 행이 양쪽 다 같다는 점이다. 저장소 또는 명시한 폴더. 딥 스캔은 더 넓게 보는 게 아니라 **같은 범위를 더 파는** 것이고, 대가는 실행 시간과 자원이다. 그리고 위임 워커가 필요해서, 런타임이 요구 사항을 못 맞추면 표준 스캔으로 돌아가거나 여유가 생길 때 다시 시도해야 한다.

한 가지 제약도 못 박혀 있다. **딥 스캔은 PR과 diff에 쓸 수 없다.** 변경 리뷰 워크플로를 쓰라는 것이고, 문서는 한 번 더 강조한다 — "A deep scan never substitutes for the diff-focused workflow." 더 무거운 도구가 더 좋은 도구는 아니라는 얘기다.

둘째 장치는 등급 어휘다. 결과가 흔들릴 수 있으면 결과를 읽는 사람에게 확신의 등급이 필요하다. 그래서 이 제품에는 판정 어휘가 여러 겹으로 깔려 있다. 스캔 사이의 finding 상태 비교는 다섯 가지로 갈린다 — `new`, `persisting`, `reopened`, `resolved`, `unknown`. 커버리지는 세 등급이다 — `complete`, `partial`, `unknown`. 두 목록 모두 마지막 칸이 `unknown`이라는 점을 눈여겨보자. **"모른다"가 일급 값으로 들어 있다.**

트리아지 판정에서 이 설계가 가장 선명하게 드러난다. 외부에서 들어온 finding을 저장소 증거로 판정하는 워크플로인데, 결과는 세 가지다.

| 판정 | 의미 |
|---|---|
| `confirmed` | 저장소 증거가 취약 경로의 도달 가능성과 보안 경계 침범을 뒷받침한다 |
| `not_actionable` | 저장소 증거가 주장을 배제한다 — 영향 없는 버전, 도달 불가 경로, 유효한 가드, 배포되지 않는 표면 등 |
| `needs_review` | 증거가 판단에 부족하다 — 정보 누락, 모호함, 런타임·환경·정책 의존 |

표 2. 트리아지 판정 3종 (판정명은 원문 표기)

`needs_review`가 별도 판정으로 있다는 것이 핵심이다. 판단할 수 없는 상태를 "일단 아님"으로 밀어넣지 않는다. 순위 규약도 이 분리를 지킨다 — 정수 순위를 `1`부터 매기되 **각 판정 큐 안에서 독립적으로** 부여한다. 그래서 "고쳐야 할 것"의 1순위와 "더 알아봐야 할 것"의 1순위가 섞이지 않는다. 문서는 오해도 미리 막는다. 이 순위는 스캐너 심각도 점수가 아니며, `not_actionable`에는 순위를 매기지 않는다.

트리아지가 각 finding을 다루는 태도도 적혀 있다. 입증되지 않은 주장으로 취급하고, 주장을 뒷받침하는 증거와 반박하는 증거를 함께 찾고, 부족한 부분을 증명 공백으로 기록한다. 중복으로 보이는 항목도 병합하거나 버리지 않고 입력 순서대로 하나씩 결과를 남긴다. 출처 추적성을 유지하기 위해서다.

트리아지에 넣을 수 있는 입력도 넓다. 붙여넣은 SARIF 결과나 CVE·GHSA 식별자, 권고문, 스캐너 티켓, 버그바운티 보고서, 심지어 평문으로 쓴 취약점 주장까지 받는다. Jira와 Linear는 커넥터로, GitHub은 인증된 REST 접근으로 연결한다. 다만 한 가지 예외가 명시돼 있다 — **GitHub Issues는 기본 소스에 들어가지 않는다.** 이슈를 판정하고 싶으면 특정 이슈를 지정하거나 명시적으로 요청해야 한다.

증명 공백이라는 개념은 수정 단계까지 따라간다. finding을 고칠 때 문서가 요구하는 계약은 회귀 테스트다. 고치기 전에는 실패하고 고친 뒤에는 통과하는 테스트를 붙이라는 것이다. 그런데 조건절이 함께 붙어 있다.

> "If a regression test is unsafe or infeasible, Codex records the proof gap and provides the strongest repeatable validation artifact instead."

테스트가 안전하지 않거나 현실적으로 불가능하면 어떻게 하는가? 그냥 넘어가지 않는다. **증명 공백을 기록하고** 가능한 가장 강한 검증 산출물을 대신 남긴다. "못 했으면 못 했다고 적어라"를 계약으로 만든 셈이다. 검증 이후의 처리도 같은 태도다 — 검증에 성공했다고 finding이 자동으로 닫히지 않는다. 명령과 결과와 남은 증명 공백을 사람이 읽고, 정확한 사유와 함께 닫거나 열어둔 채로 둔다.

쓰기 동작에도 같은 원리가 걸려 있다. finding을 외부 이슈 트래커로 내보낼 때 문서는 승인 절차를 다섯 단계로 나누고, 마지막에 이렇게 못 박는다 — 승인한 것과 **정확히 같은 페이로드**만 나가며, 대상이나 공개 범위나 내용이 바뀌면 미리보기를 새로 받아야 한다. 그리고 배치 처리는 하나씩 진행하다 **첫 불확실 지점에서 멈추고**, 생성이나 갱신은 Codex가 결과를 **다시 읽어 확인한 뒤에야** 완료로 친다.

셋째 장치는 하드닝 보고서의 자기 한정이다. 구조적 하드닝 워크플로는 증거 묶음을 설계 대안으로 바꿔주는데, 문서가 결과물의 지위를 먼저 못 박는다.

> "The result is a design portfolio, not a patch, and doesn't prove that it fixes a vulnerability."

설계 포트폴리오이며, 취약점을 고친다는 증명까지는 아니라는 것이다. 작성 기준 여섯 개 중 마지막도 같은 방향이다 — **관측된 사실, 추론, 제안된 설계 속성을 분리해서 적을 것.** 심지어 이 워크플로는 "구조 변경보다 국소 수정이 더 적절하다"는 결론을 낼 수도 있다고 적혀 있다. 도구가 자기 산출물의 필요성을 부정할 여지를 남겨둔 셈이다.

마지막으로 시간 감각을 하나 조정해두자. 클라우드 스캔의 소요 시간에 대해 FAQ는 이렇게 답한다 — 저장소 크기와 빌드 시간, 검증까지 가는 finding 수에 따라 몇 시간이 걸릴 수 있고, 큰 저장소에서는 며칠이 걸릴 수도 있다. 이후 스캔은 새 커밋과 증분 변경에 집중하므로 대개 빨라진다. 처음 돌려보고 결과가 안 보인다고 티켓부터 열 일이 아니라는 뜻이다.

## 자동화로 붙이는 네 갈래

지금까지는 사람이 화면 앞에 있는 경우였다. 이제 자동으로 도는 경로를 보자. 네 갈래가 있고 각각 전제와 제약이 다르다.

| 경로 | 명령·설치 | 인증 | 출력 | 제약 |
|---|---|---|---|---|
| CLI 단건 | `npm install @openai/codex-security` → `codex-security scan` | `--auth {auto,chatgpt,api-key}` | `--format toon\|json\|yaml\|jsonl` | Node.js 22+ 필요. 스캔·내보내기에는 Python 3.10+ 추가 |
| 벌크 스캔 | `codex-security bulk-scan` | 위와 같음 | 위와 같음 | 저장소를 탐색해 이어서 재개 가능한 방식으로 돈다 |
| CI 통합 | `codex plugin add codex-security@openai-curated` → `codex exec` | `CODEX_API_KEY` 환경 변수 | `$TMPDIR/codex-security-scans/<저장소>/<스캔-id>/` | **`--sandbox workspace-write` 필수.** 새 러너에는 마켓플레이스 플러그인이 없으므로 먼저 설치해야 한다 |
| TypeScript SDK | `@openai/codex-security` 패키지 | 위와 같음 | 구조화 finding·커버리지 | 베타 접근 권한이 필요하다 |

표 3. Codex Security 자동화 경로 네 갈래 (2026-08-02 문서 기준)

표에서 가장 자주 걸리는 줄은 세 번째다. CI 러너는 매번 새로 만들어지므로 **마켓플레이스 플러그인이 기본으로 들어 있지 않다.** 문서가 이 함정을 직접 경고한다 — `codex exec`가 쓰는 `CODEX_HOME`에 Codex Security를 먼저 설치하라는 것이다. 그리고 앞에서 본 샌드박스 조건이 여기 붙는다. 기본이 읽기 전용이므로 스캔과 수정 모두 `--sandbox workspace-write`로 띄우되, 프롬프트에는 체크아웃을 건드리지 말라는 지시를 남긴다.

CLI 자체는 생각보다 넓다. 스캔 외에 저장된 스캔을 나열·비교·재실행하고, finding을 검토·갱신하고, CSV·JSON·SARIF로 내보내고, 후보를 검증하고, 패치까지 만드는 명령이 각각 따로 있다. Git 커밋 전에 도는 훅을 설치하는 명령도 포함된다.

`scan` 명령의 플래그 중 실무에서 먼저 알아야 할 것은 대상 선택이다. `--path`, `--diff`, `--working-tree` 세 가지가 상호 배타다. `--head`는 `--diff`와만, `--base`는 `--working-tree`와만 함께 쓴다. 그리고 diff·워킹트리 스캔은 저장소 인자가 Git 워크트리 루트여야 한다.

모델 설정에 대해서는 문서가 하나만 권한다.

> "For the best scan quality, use `gpt-5.6-sol` with `xhigh` reasoning effort."

이 문장은 관련 문서 여러 곳에서 같은 형태로 반복된다. `--model`과 `--effort` 플래그가 열려 있으니 다른 값을 넣을 수는 있지만, **스캔 품질에 대해 문서가 권하는 조합은 이것 하나뿐**이다. 예시 명령줄에 다른 모델 이름이 보이더라도 그건 플래그 사용법을 보여주는 문자열로 읽어야 한다. 8장에서 봤듯 모델 이름은 계열이 여럿이라 섞이기 쉬운 자리다.

비용 통제 플래그도 있다. `--max-cost`로 예상 지출 상한을, `--fail-on-severity`로 심각도 기준 실패를 걸 수 있다. 다만 `--max-cost`가 안전망으로 충분한지는 다음 절에서 다시 이야기한다.

버전 이야기로 이 절을 닫자. 여기가 이 장에서 가장 빨리 낡을 부분이다. 2026-08-02 문서 기준으로, 같은 Codex Security 플러그인인데도 **호스티드 데스크톱 카탈로그는 `0.1.15`, 공개 CLI 마켓플레이스는 `0.1.11`**이다. 어느 쪽에서 설치했느냐에 따라 쓸 수 있는 기능이 다르다는 뜻이고, 문서도 "긴 스캔을 시작하기 전에 체인지로그를 확인하라"고 권한다. 게다가 이 번호는 **Codex 앱·CLI·TypeScript SDK와 별개 계열**이라, CLI·SDK 패키지 쪽에서 본 `0.1.3` 같은 번호와 나란히 놓고 비교할 대상이 아니다. 계열이 다르기 때문이다.

릴리스 간격도 함께 보자. 2026년 7월 하순의 릴리스는 23일·25일·28일·30일에 나왔다. 2~3일 간격이다. 그러니 이 절의 버전 숫자는 자기 환경에서 직접 확인해야 할 항목의 목록으로 읽자.

## 부품으로 붙는가, 어디까지 붙는가

이 장을 여기까지 읽은 사람이라면 자연스럽게 드는 생각이 있을 것이다. 이건 경쟁 제품인가?

CLI에 흥미로운 통합 명령이 둘 있다. `codex-security mcp`는 CLI를 MCP 서버로 등록하고, `codex-security skills`는 Codex Security 스킬을 에이전트에 동기화한다. 에이전트 친화적인 진입점도 함께 열려 있다 — `--llms`로 에이전트가 읽을 수 있는 명령 매니페스트를 받고, `scan --schema --format json`으로 인자 스키마를 JSON으로 받는다. 표면만 보면 이 제품은 다른 에이전트의 부품으로 편입되도록 설계된 것처럼 읽힌다.

그런데 문서를 끝까지 읽으면 범위가 확 좁아진다.

> "MCP exposes only the read-only `info` metadata command. Scans, exports, authentication, validation, and patching remain CLI-only."

MCP로 내주는 것은 읽기 전용 `info` 하나뿐이다. 스캔·내보내기·인증·검증·패치는 전부 CLI에만 남는다. 그러니 "MCP를 통해 다른 에이전트가 스캔을 돌릴 수 있다"고 쓰면 사실과 어긋난다. **메타데이터 조회 통로가 열려 있을 뿐이다.**

부품화의 실제 경로는 오히려 다른 쪽이다. 스킬 동기화다. `skills add`로 Codex Security 스킬을 에이전트에 붙이면, 6장에서 본 스킬 호출 문법으로 워크플로를 부를 수 있다. 실제로 이 제품의 대화형 실행은 전부 그 형태다 — `$codex-security:security-scan`, `$codex-security:security-diff-scan`, `$codex-security:triage-finding` 같은 이름들이다. 스킬 디렉터리가 벤더 중립 경로에 놓인다는 사실을 2장에서 확인했으니, 이 통로가 왜 열리는지도 짐작할 수 있다.

정리하면 이렇다. 이 제품은 조합 가능한 부품에 가깝게 설계돼 있지만, 지금 열려 있는 폭은 **스킬 동기화와 메타데이터 조회까지**다. 실행 자체는 여전히 CLI를 통한다.

한계는 통합 범위만이 아니다. 출시 직후 커뮤니티에 남은 기록을 함께 읽어야 이 제품을 도입할지 판단할 수 있다. Codex Security는 2026년 7월 28일 Hacker News에 올라왔고(596 포인트, 댓글 227개), 그 스레드에는 OpenAI에서 이 CLI를 만든 사람이 직접 답변으로 상주했다. 그래서 사용자 불만과 벤더 확인이 같은 자리에 남아 있다. 다만 **출시 나흘째의 기록**이라는 점을 전제로 읽어야 한다. 초기 버그일 가능성이 높고, 지금은 달라졌을 수 있다.

가장 먼저 눈에 띄는 것은 비용이다. 한 사용자(gregwebs, HN 스레드, 2026-07-28)는 작은 저장소에 돌렸는데 거의 한 시간을 돌다 중단됐고, Pro 플랜 주간 사용량의 절반이 사라졌다고 적었다. 마지막에 받은 것은 스캔 중 저장소 HEAD가 바뀌었다는 오류였다. 벤더 측 답변은 방어적이지 않았다.

> "Oof, that's a bad outcome. Half your weekly usage and a 50-minute scan just to get a HEAD error at the end is not acceptable. `--max-cost` can help limit estimated spend, but that doesn't fix the underlying problem."

앞 절에서 본 `--max-cost`가 여기서 다시 나오는데, 벤더 자신이 그것으로 근본 문제가 해결되지 않는다고 인정한다. 다른 사용자(arpinum, 2026-07-29)의 경험은 그 한계를 구체적으로 보여준다. 상한을 100으로 걸었더니 끝내지 못하고 중단됐는데, 105달러였다면 결과를 받았을지 500달러였어야 했을지는 알 수 없었다는 것이다.

거절 문제도 기록돼 있다. 방어 목적의 스캔이 모델 가드레일에 걸려 거절되면서 토큰만 소모한 사례가 있었고, 벤더는 원인을 이렇게 설명했다 — CLI는 저장소 소유권 검사를 하지 않으며, 거절은 과도하게 조심스러울 수 있는 모델 가드레일에서 온다는 것이다. 우회 경로로 언급된 것이 Trusted Access for Cyber 승인이다. 그 자격이 왜 문서 네 곳에서 반복되는지가 여기서 설명된다.

마지막 하나가 도입 판단에서 가장 무겁다. 벤더 확인(2026-07-29)이다.

> "this isn't an offline scanner. The CLI runs locally but the code and context needed for analysis are sent to the hosted model. ... If your company doesn't allow source code to leave its environment, you shouldn't run this against that codebase."

CLI는 로컬에서 돌지만 분석에 필요한 코드와 컨텍스트는 호스팅 모델로 전송된다. 소스가 조직 밖으로 나갈 수 없는 환경이라면 쓰지 말라고 벤더가 직접 적었다. 5장에서 세운 샌드박스는 **에이전트가 내 기계에서 무엇에 닿는지**를 통제하는 장치였지, 데이터가 어디로 가는지를 통제하는 장치가 아니었다. 두 경계는 별개다.

그래서 이 제품을 어떻게 다룰 것인가. 문서 자신이 FAQ에 적어둔 한 줄이 이 장의 두 "검토" 모두에 그대로 적용된다.

> "Codex Security accelerates review and helps rank findings, but it does not replace code-level validation, exploitability checks, or human threat assessment."
