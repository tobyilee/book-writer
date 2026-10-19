# 10장. PR 리뷰 — 사람의 눈을 줄에서 의도로 올린다

자동 리뷰를 붙였더니 PR이 닫히는 데 5시간 52분에서 8시간 20분이 걸렸다.

Cihan 외, "Automated Code Review In Practice"(ICSE-SEIP 2025)가 한 회사의 PR 4,335개를 추적한 결과다. 그중 1,568개가 LLM 기반 자동 리뷰를 거쳤고, 자동 코멘트의 73.8%가 해결됐다. 코멘트가 대부분 받아들여졌다는 것은 좋은 소식이다. 그런데 PR이 닫히는 데 걸린 평균 시간은 늘었다. 읽을 것이 늘고 고칠 것이 늘고 그 대화가 PR 위에서 오간 만큼 시간이 붙었다고 보는 것이 자연스럽다. 이 숫자를 첫머리에 두는 이유는 하나다 — AI 리뷰는 공짜가 아니다. 리뷰 하나가 늘어나면 PR 위에서 사람의 시간이 어디선가 빠져나간다. 그래서 "리뷰를 AI에게 맡기자"는 말만으로는 끝나지 않는다. 누가, 무엇을 기준으로, 얼마나 깊이 봐야 하나. 이 질문에 답하지 않으면 리뷰는 느려지기만 한다.

앞 장에서 설정 변경 PR이 eval 게이트를 통과해야 머지되게 했다. 그 PR을, 그리고 에이전트가 쓴 모든 PR을 누군가는 읽어야 한다. 이 장은 그 읽기를 다시 설계한다.

### 코스가 말하는 것: 주의를 한 층 올린다

코스 레슨 10의 변화 표는 이렇다. 전통 쪽은 "리뷰 역량은 사람의 산출량을 기준으로 계획된다. PR은 리뷰어가 전부 읽어 줄 때까지 기다리고, 리뷰 품질은 리뷰어의 부하에 따라 흔들리고, 작성자는 재촉하는 동안 백로그가 쌓인다." AI 네이티브 쪽은 "모든 PR이 동일한 리뷰 패스 세트를 받고, 발견은 심각도로 순위가 매겨진다. 사람의 주의는 한 층 위로 올라간다 — 변경이 플랜이 의도한 것을 하는지, 그리고 위험이 수락 가능한지로." 레슨 첫 문단은 방향을 둘로 적는다. "Claude는 리뷰를 주기도 받기도 한다." 들어오는 PR을 조직 정책에 대조해 리뷰하고, 자기 PR에 달린 리뷰 코멘트를 스스로 처리한다.

여섯 단계는 이렇다. 관리형 Code Review 서비스가 "가장 빠른 출발"이고, 파이프라인 통제가 필요하면 자기 CI에서 claude-code-action을 돌린다. 테크 리드가 리뷰 정책을 리포 루트의 `REVIEW.md`로 쓴다 — 패스는 "버그와 논리 오류, 보안과 취약점, 그리고 스펙(`spec.md`)·구현 플랜(`plan.md`)·설계 원칙에 대한 컴플라이언스". 사람 임계값을 정한다 — "발견은 스스로 PR을 승인하거나 차단하지 않으며, 브랜치 보호는 여전히 코드 오너의 승인을 요구한다." 코멘트에 `@claude`를 태그하면 Claude가 고쳐서 푸시하고, Claude가 연 PR은 "머지까지 베이비시팅"하게 둘 수 있다. 두 번째로 같은 실수가 지적되면 교정이 `CLAUDE.md`로 들어가고, "리뷰가 `CLAUDE.md`를 읽으므로 다음 PR부터 잡힌다." 월 1회 발견을 평가하고 Nit 양을 제한한다.

#### REVIEW.md

```markdown
# Review instructions
## Passes
Run three passes and tag each finding with its pass:
- Bugs: logic errors, broken edge cases, subtle regressions
- Security: injection risks, authentication gaps, PII in logs
- Compliance: the change matches spec.md, plan.md and our design principles
## What Important means here
Reserve Important for findings that would break behavior, leak data
or breach a policy. Style and naming are nits.
## Cap the nits
Report at most five nits per review; summarize the rest as a count.
## Do not report
Generated files under src/gen/ and anything CI already enforces.
```

열세 줄, 네 절이다. 첫 절은 세 패스 — 세 번째 패스가 이 파일의 존재 이유다. `spec.md`와 `plan.md`는 3장과 4장에서 커밋한 파일이고, 리뷰어가 그것을 읽는다는 것이 아티팩트 체인의 다음 고리다. 둘째 절은 Important의 정의 — 동작을 깨뜨리거나, 데이터를 유출하거나, 정책을 위반하는 것. 셋째 절은 Nit 상한 다섯 개. 넷째 절은 보지 않을 것 — 생성 파일, 그리고 CI가 이미 강제하는 것. 6장의 `api-policy.sh`가 PR 필수 체크로 돌고 있으니 리뷰어가 같은 것을 또 지적할 이유가 없다.

#### check run에 찍힌 세 줄

코스는 이 파일로 리뷰한 PR 하나를 보여 준다. 관통 예제의 클레임 상태 패널 PR이다.

| Severity | File:Line | Issue |
|---|---|---|
| Important | `portal/src/claims/StatusPanel.tsx:22` | Compliance: the panel fetches on every render. `plan.md` says it must cache, because claims-core allows 50 requests a second |
| Important | `claims-api/routes/status.py:31` | Security: the error path logs the whole claims-core response, which includes `policy_holder_name` |
| Nit | `claims-api/tests/test_status.py:8` | Bugs: no test covers a `paid` claim with no expected date |

첫 발견을 보자. 패널이 렌더마다 fetch한다 — `plan.md`는 캐시해야 한다고 적었고, 그 이유는 claims-core가 초당 50요청만 받기 때문이다. 4장의 `plan.md` 위험 항목 "50 rps; the panel must cache (spec concern 3)" 그대로다. 코스의 문장은 이렇다. "첫 발견은 컴플라이언스 패스가 커밋된 `plan.md`를 읽기 때문에만 존재한다. diff만 보는 리뷰어는 그 파일을 열어 두고 있지 않았을 것이다." 이것이 4장에서 `plan.md`를 `intent/`에 커밋하라고 한 이유의 절반이다 — 사람이 다시 읽는 용도에 더해, 리뷰어가 대조하는 용도다.

둘째 발견은 익숙하다. 에러 경로가 claims-core 응답 전체를 로그하고, 그 안에 `policy_holder_name`이 있다. 6장의 스킬 규칙 4, 훅, 9장의 eval이 전부 지키려던 바로 그 필드다. 그런데 왜 여기까지 왔을까? 훅은 `Edit|Write`에만 걸리고, eval은 설정 변경 PR에서만 돈다. 리뷰는 모든 PR에 돈다. 같은 정책이 또 하나의 자리에서 한 번 더 걸린 것 — 같은 스크립트가 이 책에 네 번 나오는 이유다. 셋째는 Nit — `paid` 상태에 예정일이 없는 경우를 덮는 테스트가 없다. 고칠 가치는 있지만 머지를 막을 일은 아니다.

governance 절은 한 문장으로 요약된다. "코드를 쓴 에이전트가 그것을 승인할 길이 없으므로 직무 분리가 보존된다." 발견·수정·평가·승인이 전부 PR 히스토리에 남아 "PR이 감사 기록"이 되고, "승인은 발견을 참고한 사람이 브랜치 보호를 통해" 한다.

### 네 가지 길

리뷰를 에이전트에게 맡기는 경로는 Claude Code 2.1.303 / 2026-10 기준으로 넷이고, 플랜과 읽는 파일이 다르다.

| | 관리형 Code Review | `/code-review` 명령 | claude-code-action | 자작 리뷰 서브에이전트 |
|---|---|---|---|---|
| 어디서 돌나 | Anthropic 인프라, PR마다 자동 | 내 세션 안, 내가 호출 | 내 GitHub Actions 러너 | 내 세션 안의 `.claude/agents/` |
| 플랜 | Team · Enterprise | 모든 플랜 | 모든 플랜(API 키 또는 OAuth 토큰) | 모든 플랜 |
| 읽는 기준 파일 | `CLAUDE.md` + `REVIEW.md` | `CLAUDE.md`만 | 워크플로의 `prompt`와 플러그인이 정함 | 에이전트 정의 파일 |
| 머지 게이트 가능 | 발견만, 집계로 게이트 가능 | 불가(로컬) | 가능(워크플로 실패로) | 불가 |
| 비용 감각 | 공식 "리뷰당 평균 약 20분, 대개 $15–25" | 세션 사용량 | 러너 시간 + API 사용량 | 세션 사용량 |

첫째, **관리형 Code Review** — 관리자가 켜고 리포를 고르면 PR마다 자동으로 돈다. 가장 손이 안 가고, Pro/Max 개인에게는 열려 있지 않다. 둘째, **`/code-review` 명령** — 세션 안에서 현재 diff나 PR 번호를 리뷰하고 `--fix`로 바로 적용할 수 있지만, 로컬이라 머지 게이트가 될 수 없고 호출을 잊으면 돌지 않는다. 셋째, **claude-code-action** — 자기 CI에서 돌고 워크플로를 실패시켜 게이트로 쓸 수 있으며 Pro/Max의 OAuth 토큰으로 인증할 수 있다. 세팅과 비용 관리는 자기 몫이다. 넷째, **자작 리뷰 서브에이전트** — 7장의 `verifier` 옆에 `reviewer`를 두는 식이다. 가장 유연하고 가장 보장이 없다.

어느 쪽이 나을까? 혼자 쓰는 리포라면 `/code-review`가 출발점이고, 2~10명 팀이고 PR이 머지 전에 한 번은 리뷰되어야 한다면 action이다. 관리형 서비스는 Team 플랜으로 올라간 뒤의 선택이다.

흔한 오해를 하나 바로잡자. 관리형 Code Review와 `/code-review` 명령은 이름이 비슷해서 같은 도구의 두 입구처럼 보인다. 공식 문서는 분명하게 말한다. "Code Review 서비스와 로컬 `/code-review` 명령은 두 개의 별개 도구이며, 다른 파일을 읽는다. 서비스는 `CLAUDE.md`와 `REVIEW.md`를 둘 다 읽는다. `/code-review` 명령은 `CLAUDE.md` 파일들을 읽고 `REVIEW.md`는 읽지 않는다." 개인이 리뷰 기준을 두고 싶으면 `CLAUDE.md`의 한 절에 쓰거나 리뷰 스킬·서브에이전트에 넣는 편이 낫다. 그리고 `REVIEW.md`는 "베이스 브랜치 또는 기본 브랜치의 것을 읽고, PR 자신의 변경에서는 절대 읽지 않는다" — PR에서 리뷰 규칙을 고쳐 자기 PR의 리뷰를 느슨하게 만드는 일을 막기 위해서다. 9장의 `evals/` 삭제와 같은 원리다. 평가자가 평가 대상 안에 있으면 안 된다.

### 현행 사양

> **구버전 주의** — 코스(2026-08)는 관리형 Code Review를 "(research preview)"라고 표기하고, 코스 예시가 요구하는 최소 버전(2.1.193)에서는 `/review`가 별도 명령이었다. 현행(2.1.303) 문서에는 "research preview" 라벨이 없고 플랜 조건은 Team·Enterprise다. `/review`는 v2.1.223부터 `/code-review`의 별칭이다. 이 책은 현행을 따른다. 플랜 조건은 바뀔 수 있는 부분이니 공식 문서를 함께 확인하자.

관리형 서비스는 네 단계로 돈다. "**Find**: 여러 에이전트가 diff와 주변 코드를 병렬로 검사한다. **Verify**: 검증 단계가 후보 발견을 코드에 대조해 오탐을 걸러 낸다. **Rank**: 남은 발견을 중복 제거하고 심각도로 순위 매긴다. **Post**." 기본 초점은 "정확성 — 운영을 깨뜨릴 버그이고, 포매팅 선호나 빠진 테스트 커버리지가 아니다." 심각도는 셋이다. Important — "머지 전에 고쳐야 할 버그". Nit — "고칠 가치는 있지만 막지는 않는 사소한 문제". Pre-existing — "코드베이스에 있지만 이 PR이 들여온 것은 아닌 버그". 그리고 코스가 거듭 말한 것. "리뷰는 PR을 승인하거나 차단하지 않는다. 머지 결정은 팀에 남는다." check run은 neutral로 끝나고 "절대 failure로 끝나지 않는다."

그런데 코스는 "심각도 수를 기계 판독 가능한 집계로 읽어 게이트할 수 있다"고 했다. 그 실체가 문서에 있다. check run 출력의 HTML 주석에 `bughunter-severity:` 뒤로 JSON이 숨어 있고, `gh api`로 꺼낼 수 있다 — 결과는 `{"nit": 1, "normal": 2, "pre_existing": 0}` 모양이며, "`normal` 키가 Important 발견의 수"다. 위의 check run 표가 정확히 이 값이다. `normal`이 0보다 크면 잡을 실패시키는 식으로 게이트를 만든다. 리뷰 요청은 PR 코멘트로 한다. `@claude review`는 한 번, `@claude review always`는 푸시마다. 둘 다 "리포에 write·maintain·admin 권한"이 필요하다.

claude-code-action v1은 자기 CI 경로다. 설치는 `/install-github-app`(github.com 리포 전용, 리포 admin 필요). 시크릿은 `ANTHROPIC_API_KEY` 또는 `CLAUDE_CODE_OAUTH_TOKEN`("Pro, Max, Team, Enterprise 플랜에서 사용 가능. 로컬에서 `claude setup-token`을 돌려 생성"). 워크플로에 `prompt` 입력이 없으면 대화형(`@claude`를 기다림), 있으면 자동화 모드다. 리뷰 워크플로의 핵심은 플러그인 `code-review@claude-code-plugins`를 로드하고 `prompt`로 `/code-review:code-review --comment` 뒤에 PR 경로를 넘기는 것이다. `--comment`가 중요하다 — "이 플래그가 없으면 아무것도 게시하지 않는다." 안전장치도 문서에 있다. 트리거는 "write 권한"과 "사람 행위자"를 확인하고, 봇 행위자는 `allowed_bots`에 올리지 않으면 거부해 봇이 Claude를 루프로 트리거하는 것을 막는다. 공개 리포에서는 "포크 PR이 트리거한 실행에 GitHub이 시크릿을 주지 않는다."

로컬 명령은 Pro/Max 개인의 주 도구다. `/code-review`는 "현재 diff의 정확성 버그를 확인하고 `--fix`로 발견을 적용할 수 있다. `/code-review high 1234`처럼 PR 번호를 넘기면 PR을 리뷰한다. `/review`는 별칭. `/code-review ultra`는 클라우드에서 멀티 에이전트 리뷰를 돌린다. `/security-review`는 diff의 보안 취약점을 확인한다." 2.1.288부터 `--max-findings <n>|all`이 있다. 스크립트로 가고 싶다면 공식 헤드리스 예가 있다 — `gh pr diff "$1" | claude -p --append-system-prompt "You are a security engineer. Review for vulnerabilities." --output-format json`.

Anthropic 자신은 어떻게 하는지도 적혀 있다. 보안 SDLC 글(2026-07)은 에이전트가 PR 전에 `/security-review`를 돌리고, "일부 고객은 `PreToolUse` 훅을 더 강한 게이트로 쓰지만 Anthropic은 하드 코드 리뷰 게이트를 CI에 둔다"고 썼다. 세션 안의 훅과 CI의 게이트, 둘의 자리가 다르다는 뜻이다.

### 왜 이 플레이인가

#### PR 폭탄과 노이즈

현장의 고통은 두 방향이다. 하나는 받는 쪽인데, 난감한 쪽이다. GeekNews 27700(2026-03)의 한 댓글은 이렇다. "과거 PR은 내가 만든 결과물을 내가 책임진다는 느낌이 있었지만, Vibe coder의 PR은 '내가 뭘 만들었는지도 모르겠고 어쨌든 결과물은 있으니 니가 평가해서 문제점을 찾아라' 같습니다." r/ExperiencedDevs의 최다 득표 답은 비난처럼 들리지 않게 PR 크기를 공격하라는 것이었고, 다른 댓글은 "You PR it, you own it" 한 줄이었다. 티어드 리뷰 — 저위험 PR은 가볍게, 핵심 경로는 깊게 — 제안도 반복된다. Ghostty 프로젝트의 AI_POLICY.md는 "모든 형태의 AI 사용은 공개되어야 한다"와 "사람이 모든 코드를 완전히 이해해야 한다"를 명문화했다. curl 프로젝트는 2026년 1월, AI 생성 보고의 폭증을 이유로 버그 바운티 종료를 공지했다 — 부실한 보고를 보낼 유인을 없애려는 조치였다. 보고 건수는 보도마다 달라 숫자는 적지 않는다.

다른 방향은 AI 리뷰어 자체의 노이즈다. 2024년 12월 HN의 Greptile 스레드(구버전 도구 시기다)에서는 "PR에 노이즈가 너무 많고 실제로 유용한 코멘트는 아주 적은 비율"이라는 불만과, 벤더 스스로 심각도 분류를 시도했더니 "치명적 문제를 nitpick으로 분류하는 일도 잦았다"고 인정한 대목이 있다. 2026년 1월 "AI 코드 리뷰 버블" 스레드에서도 "신호 대 잡음비가 나쁘다"가 반복되고, 같은 벤더는 "LLM은 문제의 심각도를 낮게 보는 위험을 꺼린다"고 썼다 — 반대편에는 "경험 많은 팀원들이 놓친 것을 일관되게 찾아낸다"는 보고도 있다. 비용은 2026년 5월 Cloudflare 스레드가 솔직하다 — 한쪽은 ROI가 높아 가장 강한 모델을 써도 아깝지 않다 하고, 다른 쪽은 10줄짜리 PR에 든 돈을 따진다. 커뮤니티 비용 수치는 전부 검증이 필요하고, 공식 문구는 하나다 — Anthropic이 Code Review 출시 때 적은 "리뷰는 평균 약 20분, 대개 $15–25".

한국 현장에서 눈에 띄는 것은 교차 모델 리뷰다. GeekNews 20800(2025-05)의 한 댓글: "커서(클로드)로 작성한 코드를 pr하면 chatgpt로 리뷰하고 있습니다. 이제부터 서로 싸워라 하고요." 작성 모델과 리뷰 모델을 분리하는 것은 7장의 Writer/Reviewer 두 세션("fresh context")과 같은 직관이다. 운영 휴리스틱도 쌓여 있다 — 커밋마다 재리뷰가 쌓여 `synchronize` 트리거를 뺐다는 블로그, Nit 상한, 스타일 코멘트는 opt-in.

#### 무엇을 봐야 하나

이 장 제목의 "줄에서 의도로"는 코스의 문장이지만, 그 근거는 오래됐다. Bacchelli와 Bird(ICSE 2013)는 리뷰의 실제 결과가 기대와 다르다는 것을 보였다 — 결함 발견은 기대보다 적고, 실제 가치는 지식 전달·팀 인식·대안 논의에 있었다. 사람 리뷰를 "의도와 위험"으로 재배치하는 것은 사람이 원래 잘하던 것을 남기고 못하던 것(줄 단위 결함 발견)을 넘기는 일이다. 한국 커뮤니티의 한 댓글이 같은 것을 다른 말로 했다 — 리뷰 단위를 코드에서 결정으로.

반론도 있다. 리뷰에는 교육 기능이 있고, 그것을 AI로 대체하면 "PR 리뷰 중에 일어나는 모든 학습이 위험해진다"는 것이다. 맞는 말이고, 이 책은 사람 리뷰를 없애자고 하지 않는다. 사람이 읽는 것을 바꾸자고 한다. 그리고 리뷰를 건너뛰는 쪽의 비용도 측정되어 있다. Xia와 Miller(arXiv:2607.09902, 아직 심사 전인 연구다)는 182개 리포를 종단 추적해 "프로젝트의 리뷰 없는 머지 비율이 10%p 오를 때마다 에이전트 유지보수 부담이 평균 약 6% 늘어난다"고 보고했다. 리뷰를 건너뛰면 나중에 갚는다.

`@claude` 수정 루프의 근거도 있다. Fu 외(TOSEM 2025)는 GitHub 프로젝트에 올라간 Copilot 등 AI 어시스턴트 생성 스니펫 733개에서 보안 약점을 찾은 뒤, 정적 분석 경고를 모델에게 주면 "최대 55.5%의 보안 문제를 고칠 수 있었다"고 썼다. 발견을 작성자에게 돌려주면 상당 부분이 고쳐진다 — 그 작성자가 에이전트일 때도. 다만 Perry 외(CCS 2023)의 경고를 옆에 두자. "AI 어시스턴트에 접근한 참가자들은 그렇지 않은 참가자들보다 자기가 안전한 코드를 썼다고 믿을 가능성이 높았다." 리뷰를 AI에게 맡기면 그 확신은 더 커진다. 그래서 Important의 정의가 필요하다 — 9장에서 본 LLM 심판의 장황함 편향은 리뷰어에게도 있고, "모든 것이 Important"인 리뷰는 Important가 없는 리뷰와 같다.

### 내 리포로 옮기기

`[개인 즉시]` 리뷰 경로는 `/code-review`다. PR을 열기 전에 세션에서 한 번, 필요하면 `--fix`로 바로 적용하고, 보안이 걸리는 변경에는 `/security-review`를 더한다. 리뷰 기준은 `CLAUDE.md`의 한 절에 쓴다 — `REVIEW.md`는 `/code-review`가 읽지 않으니, 위의 열세 줄을 `CLAUDE.md`로 옮기면 된다. 더 강한 분리를 원하면 7장 방식으로 Writer/Reviewer 두 세션을 쓴다. 그리고 같은 지적을 두 번 받으면 `CLAUDE.md`에 한 줄 — 5장의 "두 번 틀리면 한 줄"이 리뷰에서 들어오는 입력이다.

`[팀 합의]`에서 action이 들어온다. `/install-github-app`, Max 구독의 `claude setup-token`으로 `CLAUDE_CODE_OAUTH_TOKEN`, 그리고 `REVIEW.md`를 리포 루트에 — 단 베이스 브랜치에서만 읽히므로 `REVIEW.md` 변경은 머지 후에 효력이 난다. `claude_args`에 `--max-turns`, 동시성 제한, `synchronize` 재리뷰는 끈다. 티어드로 간다 — 저위험 PR은 작성자가 로컬 `/code-review`, 핵심 경로만 CI 리뷰. 마지막이 가장 중요하다. 브랜치 보호에 사람 승인 1명. 2명 팀에서도 작성자와 승인자는 다른 사람이어야 한다 — 에이전트가 쓴 PR을 그 세션을 돌린 사람이 승인하면 코스가 말한 직무 분리는 사라진다.

`[조직 결정]`은 관리형 Code Review(Team/Enterprise), Bedrock·Vertex·Foundry로의 API 라우팅, `bughunter-severity` 집계 기반 머지 게이트, 월간 튠업 담당자다. 개인에게는 해당 없고, 대체 경로는 위의 `/code-review`와 action이다 — 발견의 품질이 다르지 않고, 자동으로 돌지 않을 뿐이다.

측정은 둘이다. 선행 지표 "첫 리뷰까지의 시간"은 action 로그에서 바로 나오고, "사람이 브랜치를 건드리지 않고 해결된 리뷰 코멘트의 비율"은 `@claude` 루프를 쓰면 PR 스레드에서 셀 수 있다. 그리고 첫머리의 숫자를 자기 리포에서 한 번 재 보자 — 리뷰를 붙인 뒤 PR이 닫히는 데 걸리는 시간이 늘었나, 줄었나. 늘었다면 Nit 상한과 제외 목록이 답이다.

지금 할 일은 리뷰 기준을 한 페이지로 적는 것이다. 위의 `REVIEW.md`를 옆에 두고 네 가지만 쓴다. 첫째, 세 패스 — 자기 리포에서 버그·보안·컴플라이언스가 각각 무엇을 뜻하는지, 컴플라이언스 패스가 대조할 파일(`plan.md`든 `CLAUDE.md`의 Architecture 절이든)은 무엇인지. 둘째, Important의 정의 — 어떤 발견이면 머지를 미룰 것인지. 셋째, Nit 상한 — 숫자 하나. 넷째, 보지 않을 것 — 생성 파일, 그리고 CI가 이미 돌리는 것. 혼자라면 `CLAUDE.md`에, 팀이라면 `REVIEW.md`에 넣는다. 그리고 다음 PR에서 그 기준으로 리뷰를 한 번 돌려 보고, 발견 세 개를 읽는 데 걸린 시간을 적어 둔다.

리뷰는 승인하지 않는다. 발견을 읽고 머지 버튼을 누르는 것은 사람이다. 그런데 그 사람이 승인하는 것은 코드만이 아니다 — 머지 뒤에 파이프라인이 하는 일, 배포가 닿는 환경, 에이전트가 호출할 도구까지 어딘가에서 누군가 허락해야 한다. 리뷰가 끝나는 자리에서 그 허락의 자리가 시작된다.
