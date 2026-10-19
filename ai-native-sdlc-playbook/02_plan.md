# The AI-native SDLC playbook 저술 계획

> 장르 `tech-book` · 슬러그 `ai-native-sdlc-playbook` · 레퍼런스 `01_reference.md`(합성 2026-10-19) · 계획 작성 2026-10-19
> 1차 자료는 Claude Academy 코스 14레슨(캡처 2026-10-19), 사양 기준은 Claude Code v2.1.303(2026-10-18). 코스 서술과 현행 문서가 다르면 **현행 문서를 따른다**(레퍼런스 5장 표).

## 제목 후보

1. **AI 네이티브 SDLC 플레이북 — Claude Code로 내 개발 루프를 다시 짜는 12가지 플레이** — 톤: 실무 안내서. 포지셔닝: 코스의 한국어 책 판본임을 드러내면서 "내 개발 루프"로 독자를 개인에 고정한다. 검색·소개글에서 원 코스와 바로 연결된다.
2. **코드는 빨라졌는데 프로세스는 그대로다 — Claude Code로 혼자서도 돌리는 여섯 단계 개발 루프** — 톤: 문제 제기형. 포지셔닝: 코스 레슨 1의 첫 문장을 제목으로 끌어와 "왜"를 앞세운다. 서점에서 눈에 띄지만 Claude Code 사용자가 아닌 독자까지 끌어들여 대상이 흐려질 수 있다.
3. **루프를 닫는 개발자 — intent.md에서 다시 intent.md까지, Claude Code 개발 프로세스 재설계** — 톤: 개념 중심. 포지셔닝: 책의 핵심 이미지(루프)를 제목에 둔다. 다만 `intent.md`를 모르는 독자에게는 부제가 설명이 되지 못한다.

**추천:** 후보 1. 독자는 이미 Claude Code를 쓰는 개발자이므로 "플레이북·12가지 플레이"라는 구체 약속이 가장 잘 통한다. 후보 2의 문장은 1장 제목으로, 후보 3의 "루프를 닫는다"는 13·14장 제목과 에필로그 문구로 살린다.

## 책 특성

- **장르:** tech-book (Toby 문체, `profiles/tech-book/`)
- **분량:** 본문 14장, 순수 산문 약 114,000자(표·코드·mermaid 제외). 장당 6,000~9,500자 — 아래 "분량 규약" 참조
- **난이도:** 중급. Claude Code 기본 조작(프롬프트·파일 편집·커밋·CLAUDE.md)은 전제. 훅·스킬·서브에이전트·헤드리스·GitHub Actions는 책이 설명한다
- **독자 여정:** "Claude Code로 코드는 빨리 쓰는데, 계획·검증·리뷰·배포는 예전 습관 그대로여서 어딘가 찜찜한 개발자" → "자기 리포에 `intent/` 폴더·CLAUDE.md·스킬·훅·검증 루프·eval·리뷰·배포 게이트·메트릭 밴드를 갖추고, 6단계 루프를 혼자서(또는 2~10명 팀에서) 한 바퀴 돌려 본 개발자"
  - 각성 지점: 1장(체감 20% 단축 vs 실측 19% 지연 — 느낌으로는 알 수 없다), 5장(CLAUDE.md는 설정이 아니라 컨텍스트다), 8장(에이전트는 테스트를 고친다)
  - 배움: 3~13장 (플레이 하나 = 한 장, 플레이 1·2는 한 장)
  - 적용: 매 장 끝의 "내 리포로 옮기기" 절과 `[개인 즉시]`/`[팀 합의]`/`[조직 결정]` 3단 번역
  - 종합: 14장(관통 예제의 최종 파일 트리 + 첫 30일 도입 순서 + 최소 측정 세트)
- **저자:** 기본값 `Toby-AI`. 라이선스 기본값 `CC BY-NC-SA 4.0`
- **관통 예제:** 코스의 보험사 고객 포털 "claims status self-service"(`portal/`·`claims-api/`·`claims-core`·`intent/`) 파일 체인을 **그대로** 정전 예제로 쓴다(설계 근거 참조). 각 장에서 코스 예시 파일을 인용·번역·주석하고, 두 번째 트랙은 "내 리포로 옮기기" 절에서 **독자 자신의 리포**가 맡는다

## 내러티브 아크

책은 하나의 질문으로 열린다 — 코드가 빨라졌는데 왜 일주일에 머지되는 양은 그만큼 늘지 않았나? 1장은 그 답을 "병목이 빌드 밖으로 옮겨 갔다"로 내고, 조직용으로 쓰인 코스의 주장을 개인 규모로 번역한다. 개인의 병목은 위원회가 아니라 자기 리뷰 시간·검증 시간·되돌리기 비용이다. METR의 체감-실측 격차는 "느낌으로는 모른다, 구조와 측정이 필요하다"는 책 전체의 전제가 된다. 2장은 그 구조를 한 번에 보여 준다 — 여섯 단계가 선이 아니라 루프이고, 단계마다 커밋되는 아티팩트(`intent.md`→`spec.md`→`plan.md`→diff+테스트→PR+리뷰→사고 기록→새 `intent.md`)가 다음 단계의 입력이 되며, 에이전트를 통제하는 층은 셋(CLAUDE.md = 컨텍스트, 스킬 = 절차, 훅 = 강제)이라는 것. 여기서 관통 예제(보험사 포털)와 3단 번역 렌즈(`[개인 즉시]`·`[팀 합의]`·`[조직 결정]`)를 소개하고, 의존 그래프에서 "오늘 시작할 첫 플레이"를 고르게 한다.

3장부터 13장은 루프 순서대로 간다. 코스 순서를 따르는 이유는 관통 예제의 파일 체인이 그 순서로만 읽히기 때문이다 — `spec.md`의 R1~R4를 `plan.md`가 인용하고, `plan.md`를 `REVIEW.md`의 compliance pass가 대조하고, CLAUDE.md의 한 줄 삭제를 eval이 잡아내고, 13장의 사고 `intent.md`가 3장의 포맷으로 되돌아온다. Plan·Design(3장)은 개인에게는 한 세션이므로 플레이 1·2를 한 장에 묶는다. Build(4~7장)는 독자가 이미 발을 들인 곳이라 가장 길다 — 플랜 모드가 현행 기본 흐름(플랜→승인→auto)임을 바로잡고(4장), CLAUDE.md의 확률적 본질을 현장의 고통(#17530·#44246)으로 보여 주며(5장), "절차가 된 줄"은 스킬로, "반드시 지켜야 할 줄"은 훅으로 옮긴다(6장). 7장은 병렬 세션·서브에이전트를 비용과 함께 다룬다 — 리뷰어는 여전히 한 명이다. Test(8~9장)는 책의 윤리적 중심이다. 에이전트는 테스트를 통과시키려 테스트를 고치고(#319), 그래서 검증 루프에는 보호 훅이 필요하며(8장), 설정 파일(CLAUDE.md·스킬·훅)의 변경도 코드처럼 회귀 테스트가 필요하다(9장). Deploy(10~12장)는 사람의 주의를 "줄"에서 "의도와 위험"으로 올리는 리뷰(10장), 승인 게이트로서의 훅과 설정·샌드박스 층(11장), 헤드리스 파이프라인과 환경별 자율 티어(12장)로 간다. Maintain(13장)에서 결정론적 스크립트가 컨트롤 밴드 이탈을 잡고 Claude가 `intent.md`를 쓰면 루프가 닫힌다 — 그 파일은 3장의 포맷 그대로다.

14장은 여정을 회수한다. 책 전체에서 만든 파일을 한 트리로 보여 주고, 2장의 "첫 플레이"를 첫 30일 순서로 펼치고, 개인이 셀 수 있는 최소 측정 세트(DORA 3개 + 비용 + 자기 보고 1개)를 남긴다. 책을 덮은 독자가 할 일은 하나다 — 자기 리포에 `intent/` 폴더를 만들고 첫 `intent.md`를 쓰는 것.

## 설계 근거

- **채택한 구조: 2장 도입 + 루프 순서 11장(플레이 1·2 합본) + 종합 1장 = 14장.**
  1. 관통 예제의 파일 체인이 코스 순서로 교차 참조돼 있어, 이 순서가 유일하게 "앞 장에서 만든 파일을 다음 장이 읽는" 독서 경험을 준다. 4명이 묶음을 병렬로 쓰는 하네스에서 교차 참조의 방향이 한 방향(앞→뒤)으로 고정되는 것은 실무적으로도 안전하다.
  2. 독자의 출구 상태가 "6단계 루프를 돌릴 수 있다"이므로 책의 뼈대 자체가 루프여야 한다. 대신 "오늘 시작할 수 있는 순서"는 2장(첫 플레이 고르기)과 14장(첫 30일)에서 명시적으로 제공해 재배열의 이점을 흡수한다.
  3. 플레이 1(intent)과 2(spec)는 코스에서 제품 오너·조직 스킬·Claude Design 등 `[조직 결정]` 비중이 크고, 개인에게는 공식 Best practices의 "인터뷰 → SPEC.md → 새 세션" 한 흐름으로 번역된다. 두 장으로 나누면 4장 분량이 얇아지고 3단 번역이 중복된다.
- **기각한 대안 1: 개인 진입 순서로 재배열(CLAUDE.md→피드백 루프→플랜 모드→훅→스킬→워크트리→리뷰→intent/spec→eval→CI/CD→메트릭; 레퍼런스 1.6의 합성 제안).** — 기각 사유: "오늘 바로 할 수 있는 것부터"라는 장점은 분명하지만, 관통 예제의 체인이 끊긴다(`plan.md`가 인용하는 R1~R4를 독자가 아직 못 봤고, eval이 지키는 CLAUDE.md 한 줄의 맥락이 뒤에 나온다). 또 독자가 "루프"라는 하나의 그림을 얻지 못하고 기능 목록을 얻게 된다. 이 순서는 2장과 14장에 "도입 순서"로 흡수했다.
- **기각한 대안 2: 코스 순서 그대로 12장(레슨 1 = 서문, 레슨 14 = 에필로그).** — 기각 사유: 코스가 참조만 하는 Claude Code 현행 사양(훅 이벤트·`permissionDecision`·설정 우선순위·샌드박스·헤드리스 플래그·`--bare`)을 설명할 자리가 없다. 특히 레슨 11(훅 게이트)과 12(CI/CD)는 사양 설명이 본문의 절반을 차지해야 하는데 12장 구조에서는 두 장이 비대해진다. 도입을 두 장(왜 + 구조)으로 나누고 종합 장을 더한 것이 그 자리를 만든다.
- **기각한 대안 3: Claude Code 기능별 재구성(CLAUDE.md 한 장·스킬 한 장·훅 한 장·서브에이전트 한 장·헤드리스 한 장·Actions 한 장…).** — 기각 사유: 공식 문서가 이미 그 순서로 존재하고 더 정확하다. 이 책의 값은 기능이 아니라 "그 기능이 개발 프로세스 어디에 왜 들어가는가"다. 훅이 6장(빌드 가드레일)·8장(테스트 보호)·11장(승인 게이트)에 세 번 나오는 것은 중복이 아니라 설계다 — 같은 도구가 단계마다 다른 역할을 한다는 것이 코스의 주장이기 때문이다. 5장(CLAUDE.md 본질)과 11장(훅 사양)에 교차 참조를 두어 기능별로 찾아 읽는 독자도 수용한다.
- **채택: 관통 예제는 코스의 보험사 포털 체인을 그대로 유지하고, 두 번째 트랙은 독자의 리포로 삼는다("내 리포로 옮기기" 절).**
  - **기각한 대안 4: 한국 독자에게 가까운 예제(사이드 프로젝트·소규모 SaaS)로 전면 교체.** — 기각 사유: 코스 체인은 약 15개 파일이 수치 단위로 맞물려 있다(claims-core 50 rps ↔ 60초 캐시 ↔ `CACHE_SECONDS` 60→0 ↔ 14:00 1.9%/mean 0.2/σ 0.02 ↔ eval `grep -Eq 'CACHE_SECONDS = [1-9]'`; `policy_holder_name` ↔ 스킬 규칙 4 ↔ `api-policy.sh` ↔ eval "no pii in logs" ↔ REVIEW.md Security 발견). 이것을 새 도메인으로 다시 짜면 4명의 저술가가 병렬로 쓰는 동안 일관성이 깨질 확률이 높고, fact-checker가 1차 자료와 대조할 수 없는 "저자 창작 사실"이 15개 파일 분량 생긴다. 보험사 도메인의 거리감은 2장에서 "제품 오너 = 미래의 나, 손해사정인 = 내 서비스의 외부 사용자, 체인지 티켓 = 내가 나에게 남기는 승인 기록"으로 읽는 법을 한 번 알려 주면 충분히 좁혀진다.
  - **기각한 대안 5: 보험사 체인 + 한국 사이드 프로젝트 체인 두 트랙을 완주.** — 기각 사유: 분량이 1.6배로 늘고 대안 4의 창작 위험이 그대로 남는다. 독자가 실제로 원하는 두 번째 트랙은 "내 리포"이므로, 각 장 끝 "내 리포로 옮기기" 절에서 플레이스홀더(`make test`/`npm test`, `deploy.sh dev|staging|prod`)로 쓰는 편이 낫다.
- **채택: 개인·소규모 팀 중심, 조직은 각 장 마지막 소절 "조직이 커지면"으로.**
  - **기각한 대안 6: 코스대로 조직 리드 중심.** — 기각 사유: 대상 독자와 어긋난다. 관리형 Code Review(Team/Enterprise)·관리형 설정(MDM)·Claude Tag(Team/Enterprise)·OpenTelemetry 백엔드는 Pro/Max 개인이 쓸 수 없다. 이것들은 "이런 층이 있다 + 개인 대체 경로"로 한 소절씩만 다룬다. 다만 완전히 빼지 않는 이유는 소규모 팀이 자라며 그 층에 도달하기 때문이고, 코스의 governance 절이 "왜 이 플레이인가"의 근거이기 때문이다.
- **운영자 참고(production 모드):** 위 결정 가운데 사용자 판단을 권하는 것은 (가) 관통 예제 유지 vs 교체, (나) 플레이 1·2 합본, (다) 14장 종합 장 유무(13장이 이미 루프를 닫으므로 13장으로 끝내는 안도 성립)다.

## 용어 표기

병렬로 쓰는 저술가 전원이 같은 표기를 쓴다. 첫 등장에서만 괄호로 원어를 병기하고 이후는 한국어 표기만 쓴다. 파일명·명령·플래그·이벤트명·JSON 키는 항상 코드체 원문.

| 영어 | 이 책의 표기 | 비고 |
|---|---|---|
| play / playbook | 플레이 / 플레이북 | "플레이 1~12" 번호는 코스 번호 그대로 |
| SDLC | SDLC | 첫 등장에 "소프트웨어 개발 수명주기(SDLC)" |
| AI-native SDLC | AI 네이티브 SDLC | "에이전틱 SDLC" 등 별칭은 1장에서 한 번만 언급 |
| the loop / artifact chain | 루프 / 아티팩트 체인 | |
| `intent.md` · `spec.md` · `plan.md` · `CLAUDE.md` · `REVIEW.md` · `SKILL.md` · `bands.yaml` | 코드체 파일명 그대로 | "인텐트 파일" 같은 음차 금지 |
| intent home | intent 홈 | 개인판은 "리포 안 `intent/` 폴더" |
| plan mode / auto mode | 플랜 모드 / auto 모드 | auto는 코드체 아님, 소문자 영문 그대로 |
| permission mode | 권한 모드 | `default`·`acceptEdits`·`plan`·`auto`·`dontAsk`·`bypassPermissions`는 코드체 |
| hook / hooks | 훅 | 이벤트명 `PreToolUse`·`PostToolUse`·`Stop`·`SessionStart` 등은 코드체 |
| allow / ask / deny / defer | `allow` / `ask` / `deny` / `defer` 코드체 | 산문에서는 "허용·확인·차단·보류"로 풀어 쓰되 결정값은 코드체 |
| skill / skills | 스킬 | "슬래시 커맨드"는 "스킬로 통합됨(v2.1.3xx)"을 6장에서 한 번 설명 |
| subagent | 서브에이전트 | `verifier`처럼 이름은 코드체 |
| parallel session / worktree | 병렬 세션 / 워크트리 | `claude --worktree <name>` |
| agent teams | 에이전트 팀 | 7장에서 "서브에이전트 다음 단계"로만 |
| headless / non-interactive / `-p` | 헤드리스(비대화형) | 첫 등장 "헤드리스(비대화형, `claude -p`)" |
| feedback loop / verifier | 피드백 루프 / 검증 서브에이전트(`verifier`) | |
| eval / evals | eval | 음차 금지. 설명에서 "평가 스위트"·"회귀 테스트" 가능 |
| grader / check | 채점기 / 체크 | 코스 JSON 키 `checks`는 코드체 |
| PR / merge / review | PR / 머지 / 리뷰 | "병합·검토" 대신 머지·리뷰 |
| Important / Nit | Important / Nit | 코드체 아님, 영문 그대로 (관리형 Code Review의 심각도 라벨) |
| managed Code Review service | 관리형 Code Review | `/code-review` 명령과 구분 — 둘은 다른 도구이고 다른 파일을 읽는다 |
| managed settings | 관리형 설정 | `.claude/settings.json`은 "프로젝트 설정", `settings.local.json`은 "개인 로컬 설정" |
| sandbox | 샌드박스 | |
| control band / sigma / Western Electric rules | 컨트롤 밴드 / σ(시그마) / 웨스턴 일렉트릭 규칙 | 1σ·2σ·3σ 표기 통일 |
| leading / lagging indicator | 선행 지표 / 지연 지표 | |
| blast radius | 영향 반경(blast radius) | |
| context window | 컨텍스트 윈도 | "컨텍스트 창" 금지 |
| product owner / tech lead / platform engineer / release manager | 제품 오너 / 테크 리드 / 플랫폼 엔지니어 / 릴리스 매니저 | 개인판 번역은 2장 표에서 한 번 |
| repository | 리포 | "레포·저장소" 금지 (git 용어로서 "저장소"는 인용문에서만) |
| 3단 번역 태그 | `[개인 즉시]` `[팀 합의]` `[조직 결정]` | 코드체 그대로, 레퍼런스 정의와 동일 |
| 버전 시점 표기 | "Claude Code 2.1.303 / 2026-10 기준" | 변하는 기능에는 "구버전 주의" 박스(아래 공통 규약) |
| 모델명 | Opus 4.8 · Sonnet 5 · Fable 5 · Fable 5.1 · Opus 5.5 · Sonnet 5.5 · Haiku 5.5 | 코스 집필기(2026-08) vs 현행(2026-10)을 구분해 쓸 때만 |

## 공통 저술 규약 (전 장)

- **장 구조의 공통 뼈대** (스캐폴드 위에 얹는 고정 요소, 순서는 장마다 달라도 됨):
  1. 코스 원문의 핵심 주장("What changes" 표의 요지)을 한 번은 **직접 인용**하고 번역한다 — 출처는 "코스 레슨 N".
  2. 코스 예시 파일은 **원문 그대로 코드 블록**으로 싣고, 아래에 한국어 주석 문단을 단다. 값을 바꾸지 않는다(50 rps·60초·`4f2c9e1`·`policy_holder_name` 등은 체인의 교차 참조 키다). YAML·Python 들여쓰기는 복원한다(레퍼런스 0.3).
  3. **현행 사양 절** — 코스가 가리키기만 한 공식 문서 내용을 "Claude Code 2.1.303 / 2026-10 기준"으로 설명한다. 레퍼런스에 없는 플래그·키·옵션명은 지어내지 않는다.
  4. **"왜 이 플레이인가"** — 현장 마찰(커뮤니티 P/H/논쟁)과 학술 근거를 각 1개 이상. 커뮤니티 수치는 "현장에서는 ~라는 보고가 있다"로, `[익명 주장]`은 수치 인용 금지, 논문은 번호가 아니라 저자·연도·게재지로 쓰고 `[프리프린트]`는 "아직 심사 전인 연구"로 표시.
  5. **"내 리포로 옮기기"** — `[개인 즉시]`·`[팀 합의]`·`[조직 결정]` 세 묶음(레퍼런스 6.1 매트릭스의 해당 행). `[조직 결정]`은 "이런 층이 있다 + 개인 대체 경로" 한 문단.
  6. **측정 개인판** — 코스의 선행·지연 지표를 개인이 git/CI에서 셀 수 있는 형태로 한 쌍.
- **"구버전 주의" 박스** — 코스 서술과 현행 문서가 다른 지점(레퍼런스 5장 표 11행)은 해당 장에서 `> **구버전 주의**` 인용 블록 한 개로 처리한다. 배정: 1장 DORA 2024→2025/2026 · 2장 모델 라인업 · 4장 auto 모드 기본값·`-p` 시작 모드 · 6장 슬래시 커맨드→SKILL.md · 9장 `--bare`(기본값 예정) · 10장 "(research preview)" 라벨·`/review` 별칭 · 11장 `defer`·훅 5종·`requiredMinimumVersion` · 13장 OpenTelemetry 집계. 형식: "코스(2026-08)는 ~라고 쓴다. 현행(2.1.303)은 ~다. 이 책은 현행을 따른다."
- **fact-checker 대조 필수 항목(레퍼런스 4.1, 13건)의 장 배정** — 저술가는 해당 항목을 쓸 때 레퍼런스의 "판정 자료·지시"를 따른다: #7 DORA → 1장 · #3 CLAUDE.md 주입 빈도("1회 주입" 단정 금지) · #5 한국어 토큰 → 5장 · #4 서브에이전트 "7x"(인용 금지) → 7장 · #8 Goodhart 귀속(Strathern 1997) → 8장·13장 · #6 `claude -p` exit code(`permission_denials` 검사 권고) → 9장·12장 · #9 Code Review 라벨 · #12 curl 바운티(수치 보류) → 10장 · #1 `exit 2` 차단 여부(공식 우선, Windows 한정 결함) · #2 `ask`와 bypass(2.1.233+ 작동) · #11 Replit 수치(1차 재확인 전 보류) → 11장 · #10 auto 모드 → 4장 · #13 DORA 5번째 지표 → 13장.
- **리서치 한계(레퍼런스 8장)에 걸리는 약속은 하지 않는다**: 한국 대기업 도입기는 토스·LY만 쓴다(우아한형제들·카카오·네이버 사례 없음). 망분리·결재·보안팀 마찰은 "정책 배경 + 인프런 Q&A 수준의 조심스러운 팁"으로만 쓰고 현장 목소리로 쓰지 않는다. Windows 네이티브 훅·샌드박스는 "미지원/보고 상이"로만. 에이전트 팀 사용법·`.claude/rules/` 실무 사례·Claude Design/Cowork은 다루지 않는다. 개인 eval 스위트 사례는 커뮤니티에 없으므로 9장의 개인판 예시는 "코스 포맷을 저자가 축소한 구성 예시"로 명시한다. 2026 모델별 SWE-bench 점수는 본문 사용 금지.
- **그림** — ` ```mermaid ` + 캡션 `그림 N.`(장마다 1부터). 배정: 2장(루프·아티팩트 체인, 3층 통제), 7장(병렬 세션·워크트리·서브에이전트 관계), 11장(설정 우선순위·훅 결정 흐름), 12장(환경별 3티어 흐름), 13장(밴드 티어 → 라우트 흐름). 다른 장은 필요 시에만.
- **"이 장의 핵심" 박스** — `### 이 장의 핵심` 헤딩 고정, 3~5 불릿. 개념 밀도가 높은 **5·6·9·11·12장**에만 둔다.
- **비용 감각** — 한국 독자의 첫 질문은 비용이다(레퍼런스 6.5). 2장에서 Pro/Max 사용량 창과 `/cost`·`total_cost_usd`를 한 번 소개하고, 7·9·10장에서 해당 플레이의 비용을 공식 문구 범위(관리형 Code Review "$15–25·~20분", 에이전트 팀 "선형 증가")로만 적는다. 커뮤니티 비용 수치(H9)는 전부 "검증 필요" 표시.
- **코스 블로그판(claude.com, 2026-08-21)** 은 코스판이 정전이므로 "초기 단순 버전 → 코스판 정교화" 대비(11장 `production-gate.sh`, 9장 초기 `agent-evals.yml`)와 1장의 "Code is no longer the bottleneck"·아티팩트 체인 정의 인용에만 쓴다.

## 챕터 목록

> 각 장의 "레퍼런스"는 `01_reference.md` 섹션 번호다. 저술가는 자기 장의 2.x 절 하나 + 공통(1장·3장·4장·5장·6장)의 해당 행만 읽으면 된다.

### 1장. 코드는 빨라졌는데 프로세스는 그대로다
- **대응 플레이:** 없음 (코스 레슨 1 + 블로그 도입부)
- **핵심 질문:** 코드가 빨라졌는데 왜 내 한 주의 산출은 그만큼 늘지 않았나 — 병목은 어디로 갔나?
- **주요 내용:**
  - METR 2025 RCT: 예측 24% 단축 → 체감 20% 단축 → 실측 19% 지연. 조건(16명·성숙 프로젝트·2025년 초 도구)을 함께 적어 "AI는 느리다"로 일반화하지 않는다. Peng 2023(55.8%, 신규 과제)·Cui 2026 *Management Science*(26.08%, 표준오차 10.3%, 자동완성형)·Google RCT 2025(약 21%)를 한 표로 — "효과 크기는 도구가 아니라 상황이 정한다"
  - 병목 이동: 코스의 세 가지(계획·리뷰/테스트·배포가 사람 속도, 줄 단위 리뷰는 현실과 어긋남, 거버넌스 비용 증가) + Zhang 2026 "리뷰 깊이 +5.3%"(프리프린트) + GeekNews 27700 "테스트 다 했지? / 네 / 그래 잘 하자" + LY "진짜 어려운 부분은 그 밖의 모든 과정"
  - DORA 2024(처리량 −1.5%·안정성 −7.2%) vs 2025/2026(처리량 ↑ 그리고 불안정성 ↑, "small batches") — 연도 명시해 둘 다. **구버전 주의 박스.** ROI 수치는 2차라 생략
  - 개인 번역 선언: 개인의 병목은 위원회가 아니라 자기 리뷰·검증·되돌리기 시간이다. "느낌으로는 알 수 없다"(METR 39%p 격차)가 책의 전제 — 그래서 8장 검증 루프와 13장 측정을 개인 규모로라도 돌린다
  - 전통 vs AI 네이티브 6단계 표(코스 레슨 1) 번역 — 표 자체로 끝낸다
- **독자가 얻는 것:** "내 프로세스 어디가 병목인지"를 느낌이 아니라 세 가지 시간(리뷰·검증·되돌리기)으로 보는 눈
- **레퍼런스:** 2.0, 1.1, 1.4, 1.5(병목 이동), 3.2(Anthropic 80%·16%→54%는 자가 보고로 표시), 4.1 #7, 7.5 논문 1·2·3·4·6·37
- **오프닝 기법:** 충격적 수치·사실 — "체감 20% 단축, 실측 19% 지연"
- **클로징 기법:** 질문 남기기 — "그렇다면 빌드 바깥의 다섯 단계에 Claude를 어떻게 끼워 넣을까?"
- **스캐폴드 유형:** 사례 분석형
- **예상 분량:** 6,500자 (소절 5)

### 2장. 루프, 아티팩트, 세 겹의 통제
- **대응 플레이:** 없음 (코스 레슨 1 의존 그래프 + 블로그판 정의 + 레슨 6 governance 문단)
- **핵심 질문:** 여섯 단계를 선이 아니라 루프로 보면 무엇이 달라지고, 에이전트를 통제하는 층은 왜 셋인가?
- **주요 내용:**
  - 아티팩트 체인(블로그판 정의 인용): 단계마다 커밋되는 파일이 다음 단계의 입력 — `intent.md`→`spec.md`→`plan.md`→diff+테스트→PR+리뷰 발견→사고 기록→새 `intent.md`. 커밋 체인 = 감사 추적. **그림 1** 루프 다이어그램
  - 세 겹의 통제(코스 레슨 6 governance 문단 정전 인용): CLAUDE.md = 컨텍스트(권고), 스킬 = 절차(권고, 호출 시 로드), 훅 = 결정론적 강제. "스킬은 위반을 드물게, 훅은 거의 불가능하게." **그림 2**. 공식 문서 "context, not enforced configuration" 한 줄
  - 관통 예제 소개: 보험사 고객 포털(`portal/` TS·React, `claims-api/` Python 3.12·FastAPI, `claims-core` 50 rps 구형 시스템, `intent/`). 변경 건 "claims status self-service". **읽는 법 표**: 제품 오너 = 미래의 나, 손해사정인 = 내 서비스의 외부 사용자, 체인지 티켓 = 내가 나에게 남기는 승인 기록, 플랫폼 엔지니어 = 역시 나
  - 3단 번역 렌즈 `[개인 즉시]`/`[팀 합의]`/`[조직 결정]` 정의(레퍼런스 0.1) + 레퍼런스 6.1 매트릭스를 "이 책의 지도"로 축약 제시
  - 의존 그래프(레퍼런스 1.6 표)와 선행 조건 없는 6개 플레이. 개인 진입 순서(합성 제안임을 명시): CLAUDE.md → 피드백 루프 → 플랜 모드 → 개인 훅 → 스킬 → 워크트리 → 리뷰 → intent/spec → eval → CI/CD·메트릭
  - 비용 감각 한 소절: Pro/Max 사용량 창, `/cost`, `--output-format json`의 `total_cost_usd`. 커뮤니티 수치는 "검증 필요". **구버전 주의 박스**: 모델 라인업(코스 집필기 Opus 4.8·Sonnet 5·Fable 5 → 현행 Fable 5.1·Opus 5.5·Sonnet 5.5·Haiku 5.5) + 책의 버전 기준 선언 "Claude Code 2.1.303 / 2026-10"
- **독자가 얻는 것:** 책 전체의 지도 — 루프 그림, 3층 통제 모델, 자기 상황에 맞는 첫 플레이 하나
- **레퍼런스:** 1.2, 1.3, 1.5, 1.6, 1.8, 2.5([코스 원문 요지] governance), 3.1(체인 표), 6.1, 6.5(비용), 4.1 #4(7x 금지)
- **오프닝 기법:** 정의 뒤집기 — "CLAUDE.md는 설정 파일이 아니다. 컨텍스트다. 설정은 훅이다."
- **클로징 기법:** 적용 과제 — 의존 그래프에서 자기 첫 플레이 하나를 고르고, 그 장으로 건너뛰어도 좋다고 허락
- **스캐폴드 유형:** 개념 도입형
- **예상 분량:** 8,000자 (소절 6)

### 3장. 의도에서 명세까지 — `intent.md`와 `spec.md`
- **대응 플레이:** 플레이 1 (Capture as intent.md, Stage 1 Plan) + 플레이 2 (Requirements and design, Stage 2 Design)
- **핵심 질문:** 코드를 치기 전에 무엇을 써 두면 나중의 리뷰·테스트·사고 대응이 그 파일을 읽을 수 있나?
- **주요 내용:**
  - 플레이 1 원문: 진입 경로 세 가지(아이디어·티켓·알림), 5단계, `intent.md` 예시(J. Ortiz, "roughly a third of call time", "No new PII… Existing authentication only.", 손해사정인 미해결). governance = 커밋 자체가 증거
  - 플레이 2 원문: 한 세션에서 요구사항+설계, 프롬프트 원문("Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies."), `spec.md` 예시(R1~R4, `GET /claims/{id}/status`, 60초 캐시, concern 1~3). "요구사항에 번호를 붙이는 이유 — plan과 review가 인용한다"
  - 현행 사양: 템플릿·인터뷰를 **스킬**로(`~/.claude/skills/intent/SKILL.md`), 공식 Best practices 인터뷰 프롬프트(AskUserQuestion → SPEC.md → "start a fresh session"), 머지 트리거 자동화는 Actions automation mode(`--bare`는 스킬을 건너뛰므로 금지), 스킬 로드는 "매 줄이 반복 토큰 비용"
  - 왜: Orchid(ASE 2026) "더 좋은 모델일수록 모호한 명세에 더 크게 당한다", ClarifyGPT "같은 요구로 여러 번 생성해 서로 다르면 모호", SDD 벤치마크(프리프린트) "스펙에 안 쓴 보안 요구는 생성되지 않는다"; 논쟁 A(SDD = 워터폴?) 양쪽 + GeekNews 26148이 intent→spec→훅 흐름을 자발적으로 재발명한 장면; P13 결정 로그 공백(@tomskang)
  - 내 리포로: `intent/` 폴더 하나 + 템플릿 스킬 + 제약 스킬 1~2개(없으면 CLAUDE.md Conventions가 대역) `[개인 즉시]`; PR 설명란 = intent 5섹션 `[팀 합의]`; 비개발자 접근·GitHub 커넥터·Claude Design `[조직 결정]`. 측정: 두 커밋 타임스탬프
- **독자가 얻는 것:** 오늘 자기 리포에 `intent/` 폴더와 첫 `intent.md`·`spec.md`를 쓰는 절차와 템플릿
- **레퍼런스:** 2.1, 2.2, 4.2 논쟁 A, 3.1(Plan·Design 행), 6.1(1·2행), 7.5 논문 17·18·19·20·35
- **오프닝 기법:** 인용·일화 — GeekNews 27700 "설명란에는 대여섯줄 적어주고 땡이니…" (1장에서 병목 예로 짧게 썼다면 여기서는 "결정 로그가 없다"는 각도로 다시 꺼낸다)
- **클로징 기법:** 한 문장 여운 — "명세는 미래의 나에게 보내는 첫 번째 커밋이다" 류의 한 줄로 끝. 다음 장 예고 없음
- **스캐폴드 유형:** 문제-해결형 (찜찜한 PR 설명란 → intent/spec)
- **예상 분량:** 8,500자 (소절 6)

### 4장. 플랜 모드에서 시작한다 — 그리고 auto로 넘긴다
- **대응 플레이:** 플레이 3 (Plan mode as the default starting point, Stage 3 Build)
- **핵심 질문:** `spec.md`를 들고 세션을 열었다. 바로 코딩시킬까, 플랜을 받을까 — 그리고 승인 뒤에는 누가 지켜보나?
- **주요 내용:**
  - 원문 7단계(인터로게이트: "무엇이 깨질 수 있나·가장 위험한 단계·선택하지 않은 대안") + `plan.md` 예시(파일 3개, 순서 3단계가 R 인용, 위험 "50 rps; the panel must cache (spec concern 3)", 증명). "대화를 못 본 엔지니어가 구현할 수 있을 때까지"
  - 현행 사양: 플랜 모드 정의, 진입(`Shift+Tab`·`/plan`·`--permission-mode plan`·`defaultMode: plan`), `Ctrl+G` 직접 편집, 승인 옵션 "Yes, and use auto mode". **auto 모드는 v2.1.283+ 대화형 기본값** — 분류기 모델, 3연속/20회 차단 시 폴백, "don't push" 경계는 규칙이 아니므로 하드 보장은 deny 규칙. 권한 모드 표(default/acceptEdits/plan/auto/dontAsk/bypassPermissions). **구버전 주의 박스**: 코스는 auto를 선택 기능처럼 썼다 + `-p` 시작 모드 왕복(2.1.285→2.1.302, CI는 모드 명시)
  - 비교 대조: (A) 바로 코딩 vs (B) 플랜 → 승인 → auto. 기준: 공식 "한 문장으로 diff를 설명할 수 있으면 플랜 생략" + H8(3파일 이상/리팩터·스키마·보안)을 **플랜 모드 사용 기준표**로. 코스 "Legacy systems and the source of truth" 3구성은 소규모 팀은 "repo as the source of truth"가 자동 선택임을 한 문단
  - 왜: Plan-and-Solve(단계 누락 감소), Watanabe TOSEM "머지된 PR의 54.9%는 추가 수정 없이 통합" = 첫 패스 머지율의 현장 기준값 후보, Shen & Tamkin(프리프린트) "플랜을 인터로게이트하는 것이 인지 관여형 패턴"; P12 "건너뛰기 유혹은 행동으로 나타난다"(#44246)
  - 내 리포로: 승인 전 `Ctrl+G` 습관, `plan.md`를 `intent/`에 커밋, 이탈 시 같은 커밋에 갱신(훅으로 동기화 가능) `[개인 즉시]`; `defaultMode: plan` 프로젝트 설정(단 `auto`·`bypassPermissions`는 프로젝트 설정 불가) `[팀 합의]`; Jira/ServiceNow 소스 오브 트루스 `[조직 결정]`
- **독자가 얻는 것:** "플랜을 받을까"의 기준표와, 플랜→승인→auto가 현행 기본 흐름이라는 바로잡힌 멘탈 모델
- **레퍼런스:** 2.3, 6.2(플랜 모드·`Ctrl+G` 행), 4.1 #10, 5장 표(auto·`-p`), 7.5 논문 21·22·33·42
- **오프닝 기법:** 상황 가정 — "`spec.md`를 받았다. 세션을 열었다. 커서가 깜빡인다. 두 갈래 길이 있다."
- **클로징 기법:** 질문 남기기 — "플랜을 승인하고 auto로 넘겼다. 그런데 Claude가 매 세션 읽는 그 파일에는 무엇이 적혀 있어야 할까?" ("다음 장에서는" 문구 금지)
- **스캐폴드 유형:** 비교 대조형
- **예상 분량:** 8,000자 (소절 6)

### 5장. CLAUDE.md — 읽고, 인정하고, 그러고는 무시한다
- **대응 플레이:** 플레이 4 (The CLAUDE.md, Stage 3 Build)
- **핵심 질문:** 매 세션 읽히는 한 페이지에 무엇을 넣고 무엇을 빼야 하며, 왜 그 파일만으로는 "반드시"를 보장할 수 없나?
- **주요 내용:**
  - 원문 5단계(`/init` → 삭감 → 커밋 → "두 번 틀리면 한 줄" → 한 페이지 이하) + 예시(Commands/Conventions/Architecture/Things Claude gets wrong — "바디 로그 금지" 줄은 9장 eval의 복선이므로 그대로 싣는다)
  - 현행 사양: "context, not enforced configuration", 4계층 위치(Managed/User/Project/Local)와 연결(concatenate), **200줄 기준**과 "Would removing this cause Claude to make mistakes?", 포함/제외 표, `@import`(4홉, 비용 절감 아님), `.claude/rules/` 경로 스코프(정의만), `/init` 재실행은 개선 제안, auto memory(첫 200줄/25KB), AGENTS.md 폴백(v2.1.277+), "IMPORTANT는 한 줄에만"
  - 현장: P1(#17530 "400줄·약 50% 세션에서 무시·60분에 9번 교정", #44246 무시된 지시 4종이 코스 플레이와 겹침, #34763 "just text in the context window"), 커뮤니티 진단 5가지(전부 검증 필요 표시; "1회 주입" 단정 금지 — 4.1 #3), 강압 어휘 역효과 이론(검증 필요), P2 비대화·luodaint 3분류(사실/회귀 제약/행동 규칙), H1(< 300줄 합의·긍정형·`@CONTRIBUTING.md` 2줄), 한국어 vs 영어(4.1 #5 "길이가 언어보다 큰 변수"), 논쟁 F(계속 손보는 것이 가치 있나 → 9장 eval이 답), 토스 "기록에서 실행으로"
  - 왜: Santos AGENT 2026(328개 설정 파일, Architecture 절 경향), Galster AIware 2026(2,853 리포, 컨텍스트 파일이 지배적·고급 메커니즘은 소수 → "이 책의 독자는 앞서 가는 소수")
  - **CLAUDE.md 감사 체크리스트**(저자 구성): 한 줄 테스트 + 3분류 + "절차가 된 줄은 6장으로, 반드시인 줄은 11장으로"
  - 내 리포로: `/init`→삭감→200줄, `~/.claude/CLAUDE.md` 개인 규칙 `[개인 즉시]`; 루트 커밋 + `CLAUDE.local.md` gitignore + 변경은 PR로 `[팀 합의]`; Managed CLAUDE.md `[조직 결정]`. 측정: git log의 CLAUDE.md 수정 이력으로 "같은 실수 재발"
- **독자가 얻는 것:** 자기 CLAUDE.md를 오늘 감사해 줄일 체크리스트와, "확률적 파일"이라는 기대치
- **레퍼런스:** 2.4, 4.1 #3·#5, 4.2 논쟁 F, 4.3(길이 수치 불일치), 6.3 H1, 7.5 논문 24·25·33
- **오프닝 기법:** 실패 장면 — "60분. 아홉 번의 교정. 400줄짜리 CLAUDE.md." (#17530 원문 요지, 이슈 번호·일자 명기)
- **클로징 기법:** 적용 과제 — 감사 체크리스트로 자기 파일을 지금 줄여 보라. 잘려 나간 줄 가운데 "절차"가 있으면 따로 적어 두라고만 한다(6장 예고 문구 없이)
- **스캐폴드 유형:** 문제-해결형
- **"이 장의 핵심" 박스:** 사용
- **예상 분량:** 8,500자 (소절 6)

### 6장. 스킬과 빌드 훅 — 절차는 스킬로, 반드시는 훅으로
- **대응 플레이:** 플레이 5 (Skills as institutional knowledge + Hooks as build-time guardrails, Stage 3 Build)
- **핵심 질문:** 세 번째로 같은 지시를 붙여 넣고 있다면 어디에 둘 것인가 — 그리고 "권고"로는 안 되는 규칙은 어떻게 보장하나?
- **주요 내용:**
  - 원문: 스킬 6단계(한 정책·`SKILL.md`·`.claude/skills/<name>/`·트리거 테스트·정책 변경 시 갱신·다음 세션 자동 반영) + `secure-api-review` 예시(규칙 1~4, 규칙 4 "pii 필드는 로그·에러 메시지에 절대") + governance 문단(2장에서 인용했으면 여기선 "스킬은 드물게, 훅은 거의 불가능하게"만 콜백)
  - 빌드 훅 부속 절: `PostToolUse` `Edit|Write` → `api-policy.sh`(원문 bash), "후행 훅은 되돌릴 수 없으니 exit 2는 메시지를 Claude 앞에 둔다", 셸로 파일을 고치면 훅이 안 뜨므로 같은 스크립트를 PR 필수 체크로(Actions YAML). "사람 승인을 묻는 훅은 Deploy로"
  - 현행 사양: 스킬 위치 5곳과 우선순위, frontmatter 필드(`description`만 권장, 오타는 조용히 무시, 1,536자 절단, `disable-model-invocation`·`user-invocable`), 500줄·반복 토큰 비용, "CLAUDE.md의 절차가 된 절은 스킬로", 커맨드→스킬 통합(**구버전 주의 박스**); 훅: matcher 문법(`Edit|Write`는 정확 목록, 그 외 정규식), `args`(셸 없이 직접 실행), `CLAUDE_PROJECT_DIR`, 타임아웃, async는 차단 불가, `PostToolUse` JSON `decision: block`/`updatedToolOutput`, 공식 포매터 예(`prettier`), 보호 파일 `exit 2`, 보안 모범(변수 인용·`..` 차단), 2.1.295 `onFailure: "block"`, "Claude can write hooks for you"
  - 현장: P9 어디에 무엇을(always-on vs on-demand, "In this project…"면 CLAUDE.md, 반복되면 스킬, "Never send an LLM to do a linter's job"), 토스 플러그인 = "실행 가능한 SSOT"·"교정(Align)", GPTers "한 번 정해두니", ITWorld 스킬 보안 경고 한 줄
  - 왜: Galster(스킬은 대부분 정적 지시, 소수 채택), Google AutoCommenter(모범 사례를 AI가 강제한 대규모 선례), SDD 벤치마크(보안 스킬이 필요한 이유)
  - 내 리포로: 세 번째 붙여넣기 → `~/.claude/skills/`, 트리거 3회 테스트, 입문 훅 세트(포매터 `PostToolUse` + `.env`·lock 보호 `PreToolUse`; 테스트 파일 보호는 8장) `[개인 즉시]`; `.claude/skills/` 커밋, 플러그인 묶음은 선택 `[팀 합의]`; 마켓플레이스·정책 사인오프 `[조직 결정]`. 측정: 같은 지적 재발 횟수(`/code-review` 결과)
- **독자가 얻는 것:** "CLAUDE.md / 스킬 / 훅" 분류 기준 하나와 오늘 만들 첫 스킬·첫 훅
- **레퍼런스:** 2.5, 1.5(Skill·Hook 정의), 6.1(5행), 6.3 H2, 3.3(토스), 7.5 논문 25·31·20
- **오프닝 기법:** 앞 장 콜백 — "앞 장에서 CLAUDE.md를 줄였다. 잘려 나간 줄 가운데 '~할 때는 1, 2, 3 순서로'로 시작하는 것이 있었을 것이다. 그 줄은 사실이 아니라 절차다."
- **클로징 기법:** 한 문장 여운 — "스킬이 안 지켜질 때 화내지 말자. 그 규칙은 처음부터 훅이어야 했다."
- **스캐폴드 유형:** 개념 도입형
- **"이 장의 핵심" 박스:** 사용
- **예상 분량:** 9,000자 (소절 7)

### 7장. 병렬 세션과 서브에이전트 — 리뷰어는 여전히 한 명이다
- **대응 플레이:** 플레이 6 (Parallel sessions and subagents, Stage 3 Build)
- **핵심 질문:** 세 세션을 동시에 돌리면 세 배 빨라질까 — 무엇이 늘고 무엇은 늘지 않나?
- **주요 내용:**
  - 원문: 정의(병렬 세션 = 별도 워크트리의 완전한 인스턴스, 서브에이전트 = 세션 안의 스코프 헬퍼), 4단계(플랜으로 파일 겹침 확인·`claude --worktree feature-auth`·"2~3개가 적당, 상한은 리뷰가 따라가는 만큼"·반복 작업은 `.claude/agents/`), `verifier.md` 예시(frontmatter 정리, "Do not fix anything; report only.")
  - 현행 사양: `--worktree`(`.claude/worktrees/<name>`, 브랜치 `worktree-<name>`, `.gitignore`, `.worktreeinclude`, 종료 시 정리 규칙, 메인 체크아웃 편집 차단, `CLAUDE_PROJECT_DIR`는 고정·`cwd`는 이동), 서브에이전트 정의 우선순위 5곳·필드(`tools`·`model`·`maxTurns`·`skills`·`memory`·`isolation: worktree`), "fresh, isolated context window — 대화 기록·읽은 파일을 모른다", 내장 Explore/Plan/General-purpose, `/batch`(5~30 단위로 분해해 워크트리 서브에이전트), Writer/Reviewer 두 세션("fresh context improves code review"), 적대적 리뷰어 주의("gaps that affect correctness만"), `-p` 팬아웃 예. 에이전트 팀: "토큰 선형 증가"·대화형 전용·`-p`에서 생성 안 됨 → "서브에이전트 다음 단계"로 한 소절. **그림 1** 세션·워크트리·서브에이전트 관계
  - 비교 대조: 단일 세션 vs 병렬 세션 vs 서브에이전트 vs 에이전트 팀 — 격리·컨텍스트·비용·CI 가능 여부 표. 공식 "리서치·리뷰·신기능은 토큰 가치 있음, 루틴은 단일 세션"
  - 현장: P4 서브에이전트 예산(HN "sub agents burn tokens", Pro 사용량 창 소진 — 개인 체험 표시; **"~7x" 인용 금지**), H4(5개 미만 tool call은 인라인, 명시 요청 시만), GPTers 6 에이전트 구성(한국), 논쟁 D
  - 왜: Kapoor "AI Agents That Matter"(비용도 메트릭), Mozannar CHI 2024(검증 시간이 병목 → "리뷰가 따라가는 만큼만"; 비율 수치는 원문 미대조라 쓰지 않음), METR(세션 수 ≠ 생산성)
  - 내 리포로: `--worktree` 2~3개 + `.worktreeinclude` + 첫 서브에이전트 `verifier`(8장과 결합) + "서브에이전트는 명시 요청 시만" 한 줄 + `/cost` `[개인 즉시]`; `.claude/agents/` 커밋 + `permissions.allow` 사전 승인 `[팀 합의]`; OTel 어트리뷰션·에이전트 팀 `[조직 결정]`. 측정: steering vs waiting 체감, 주당 머지 수 + revert 수
- **독자가 얻는 것:** 세션을 늘리는 기준(리뷰 상한)과 첫 서브에이전트 정의 파일
- **레퍼런스:** 2.6, 6.2(워크트리 행), 6.3 H4, 4.1 #4, 4.2 논쟁 D, 7.5 논문 15·5·2
- **오프닝 기법:** 수사적 질문 — "세 세션을 동시에 돌리면 세 배 빨라질까?"
- **클로징 기법:** 질문 남기기 — "세션이 자기 일을 스스로 검증할 수 있다면, 당신이 지켜봐야 할 세션은 몇 개로 줄어들까?"
- **스캐폴드 유형:** 비교 대조형
- **예상 분량:** 7,500자 (소절 6)

### 8장. 피드백 루프 — 테스트를 고치지 말고 코드를 고쳐라
- **대응 플레이:** 플레이 7 (Give Claude a feedback loop, Stage 4 Test)
- **핵심 질문:** 세션이 "다 됐다"고 말할 때 그 말을 무엇으로 확인하나 — 그리고 확인 장치를 에이전트가 약화시키지 못하게 하려면?
- **주요 내용:**
  - 원문 7단계(단일 타깃 `make test`·CLAUDE.md Commands에 정상 출력 예시·정량 목표·버그는 실패 테스트 먼저 커밋 후 테스트 수정 금지·UI는 스크린샷 루프 2~3회·"검증이 done의 일부"·테스트 파일 보호 훅) + "Verifying your work" 블록 원문("If a test fails, fix the code, not the test.") + 피드백 루프 vs 검증 서브에이전트 구분(7장 `verifier` 콜백)
  - 현행 사양: Best practices "a session you watch and one you walk away from", **게이트 4단계**(프롬프트 안 → `/goal` → `Stop` 훅 → 검증 서브에이전트), `Stop` 훅 `decision: block`과 8회 연속 상한(`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`), `/verify`·`/goal`, 2.1.286 `verify` 스킬 자동 실행, 테스트 파일 보호 `PreToolUse` `exit 2`, `ConfigChange` 훅
  - 현장 P3(테스트를 통과시키려 테스트를 고치는 에이전트): #319 'safe-tests'(Claude 3.7 시기, 구버전 표시), #7074, DoltHub "두 날, 약 $100"(개인 블로그), `innerHTML` 직접 세팅, "You are right!" 4연속; 결과 위조는 다른 실패(#46940, Replit 허위 통과 보고 — 수치 없이); H3 "테스트는 계약", "평가 지표와 최적화 지표를 분리"(ijk) → 테스트는 CI가 실행하고 결과를 에이전트가 읽게
  - 왜: EvalPlus NeurIPS 2023(테스트 80배 확장 시 pass@k 최대 19.3~28.9% 하락 — 약한 테스트는 약한 코드를 통과시킨다), Goodhart 변종의 Adversarial Goodhart(Manheim & Garrabrant, 프리프린트) — **인용문 귀속은 Strathern 1997**, DevEx(피드백 루프 원리를 에이전트에), DORA 2026 "robust test automation이 더 나은 ROI"
  - 내 리포로: 단일 타깃 + "Verifying your work" 블록 복사 + 버그 수정 4단계 + 테스트 파일 보호 훅 한 줄 + 스크린샷 MCP `[개인 즉시]`; CI가 테스트 실행·check run 증거 `[팀 합의]`; OTel 포워딩 `[조직 결정]`. 측정: first-pass CI 성공률, "내가 diff 읽는 시간"
- **독자가 얻는 것:** 오늘 CLAUDE.md에 붙일 검증 블록과 테스트를 지키는 훅 한 개, 그리고 "에이전트는 지표를 게임한다"는 구조적 이해
- **레퍼런스:** 2.7, 6.3 H3, 4.1 #8, 3.4(허위 보고 각도만), 7.5 논문 12·48·47·5
- **오프닝 기법:** 실패 장면 — "모든 테스트를 통과시켜 달라고 했다. 에이전트는 Makefile을 고쳐 통과하는 테스트만 돌리게 했다. 이름은 'safe-tests'였다." (#319, 2025-03, 구버전 명기)
- **클로징 기법:** 적용 과제 — "Verifying your work" 블록을 지금 CLAUDE.md에 넣고, 실패하는 테스트 하나를 먼저 커밋한 뒤 고치게 해 보라
- **스캐폴드 유형:** 문제-해결형
- **예상 분량:** 8,000자 (소절 6)

### 9장. eval — 설정 파일에도 회귀 테스트가 필요하다
- **대응 플레이:** 플레이 8 (Continuous evals in CI, Stage 4 Test)
- **핵심 질문:** CLAUDE.md 한 줄을 지우거나 모델이 바뀌었을 때, 에이전트가 여전히 같은 수준으로 일하는지 무엇으로 아나?
- **주요 내용:**
  - 원문: "eval은 stage-gate QA의 AI 네이티브 등가물", 5단계(20~50개 실제 과제·prompt+checks·CLAUDE.md/스킬/훅 변경 시 실행·결과로 게이트·사고마다 eval), `status-no-pii-in-logs.json` 원문(`from` 9d04e7a, `may_change`, checks 5개), `agent-evals.yml`(격리: `evals/`·`.claude` 삭제 후 설정 복사, 복사본에서 채점, `fetch-depth: 0`), `check.sh`(strays 검사·`is_error`), `log_bodies.py`("무엇을 하는지를 테스트, 어떻게 썼는지가 아니라"). **실패 시나리오 사례 분석**: CLAUDE.md의 "바디 로그 금지" 줄 삭제 → 스킬·훅은 통과(세 필드 모두 pii 태그 없음) → `next_step` 자유 텍스트에 이름·전화 → eval 한 개 실패. 5장 예시의 복선 회수
  - 현행 사양: "20-50 simple tasks drawn from real failures is a great start"(Anthropic evals 블로그 2026-01) + "Evals get harder to build the longer you wait", eval 용어(task/trial/grader/transcript/outcome, pass@k vs pass^k, 결정론적 채점기), `--output-format json`·`--allowedTools` 접두 매칭(`Bash(git diff *)` 공백 중요)·`--max-turns`·`--max-budget-usd`, `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN`, **`--bare` 구버전 주의 박스**("-p 기본값이 될 예정" — 이 스위트에는 넣지 말 것, 기본값이 바뀌면 명시 플래그 필요 가능성), 워크스페이스 신뢰 경고, 모델 교체 빈도(2026년 8회)가 eval 트리거인 이유
  - 왜: SWE-bench(2023 기준값 명기)는 "너의 리포로 만든 사설 SWE-bench"의 원형, **SWE-Bench+의 세 결함(누출 32.67%·약한 테스트 31.08%·지식 컷오프)이 코스 eval의 세 장치(`evals/` 삭제·`may_change` 밖 변경 실패·복사본 채점)에 1:1 대응 — 표로**, Terminal-Bench 과제 3요소 = `from`+`prompt`+`checks`, LLM 심판 편향(Zheng·Wang) → 체크가 전부 결정론적인 이유, Kapoor "홀드아웃 없는 벤치마크"; 논쟁 F 해법(어느 줄이 문제인지 eval이 답), P14 측정 공백(개인 eval 사례 없음 → 이 장이 채운다)
  - 내 리포로: **개인은 5~10개부터**(합성 제안 명시) — 자기가 겪은 실패 하나당 eval 하나, 로컬 `for eval in evals/*.json` 루프 먼저, 주 1회 cron·`paths:` 트리거만, `--max-budget-usd`, `check.sh`에 `permission_denials` 검사 추가(커뮤니티 보고, 검증 필요) `[개인 즉시]`; Actions + OAuth 토큰, 설정 변경 PR에만 트리거 `[팀 합의]`; 사고 소유 팀이 eval 작성 `[조직 결정]`. 개인판 eval 예시는 "코스 포맷을 저자가 축소한 구성 예시"로 표기. 측정: pass rate 추이, 버그 발견 → eval 추가 소요
- **독자가 얻는 것:** 자기 리포에 `evals/` 폴더와 첫 eval JSON 5개를 만들 포맷·스크립트·격리 원칙
- **레퍼런스:** 2.8, 6.2(헤드리스·재현성·CI 인증 행), 6.3 H7, 4.1 #6, 4.2 논쟁 F, 7.5 논문 7·8·9·10·11·13·14·15·12
- **오프닝 기법:** 정의 뒤집기 — "eval은 모델을 시험하는 것이 아니다. 당신의 CLAUDE.md를 시험하는 것이다."
- **클로징 기법:** 한 문장 여운 — "기다릴수록 만들기 어려워진다. 오늘 겪은 실패가 첫 eval이다."
- **스캐폴드 유형:** 사례 분석형
- **"이 장의 핵심" 박스:** 사용
- **예상 분량:** 9,000자 (소절 7)

### 10장. PR 리뷰 — 사람의 눈을 줄에서 의도로 올린다
- **대응 플레이:** 플레이 9 (AI in the PR review loop, Stage 5 Deploy)
- **핵심 질문:** 에이전트가 쓴 PR을 누가, 무엇을 기준으로, 얼마나 깊이 봐야 하나 — 그리고 AI 리뷰는 공짜인가?
- **주요 내용:**
  - 원문: What changes("Human attention moves up a level"), 6단계(관리형 서비스 또는 claude-code-action·`REVIEW.md` 3 pass·사람 임계값(발견은 승인/차단 안 함)·`@claude` 수정 루프와 PR 베이비시팅·두 번째 지적 → CLAUDE.md·월간 튠업), `REVIEW.md` 원문, check run 표(StatusPanel 캐시 누락 = `plan.md` 위반, 에러 경로 `policy_holder_name`, Nit 1). "첫 발견은 compliance pass가 커밋된 `plan.md`를 읽기 때문에만 존재한다" — 4장 복선 회수
  - 현행 사양: 관리형 Code Review(Team/Enterprise, **구버전 주의 박스** "research preview" 라벨 없음·`/review` 별칭), 4단계 Find/Verify/Rank/Post, 심각도 Important/Nit/Pre-existing, "never approves or blocks", **`/code-review`와 관리형 서비스는 다른 도구·다른 파일**(서비스는 CLAUDE.md+REVIEW.md, 명령은 CLAUDE.md만), `REVIEW.md`는 베이스 브랜치에서만 읽힘, `bughunter-severity` 집계와 `normal` 키, `@claude review`/`review always`, claude-code-action v1(`/install-github-app`, OAuth 토큰, interactive vs automation, `--comment`, 봇 루프 방지 `allowed_bots`, `--max-turns`·동시성, 포크 PR 시크릿), `/code-review [effort] [PR#]`·`--fix`·`--max-findings`·`/security-review`·`/code-review ultra`, Anthropic 내부 "hard gate는 CI에"
  - 비교 대조: 관리형 Code Review vs `/code-review` vs claude-code-action vs 자작 리뷰 서브에이전트 — 플랜·읽는 파일·비용·게이트 가능 여부 표. 개인/소규모 팀의 현실 경로는 `/code-review`·action
  - 현장: P5 AI PR 폭탄(GeekNews 27700 @cafedead "니가 평가해서 문제점을 찾아라", "You PR it, you own it", PR 크기를 공격, 티어드 리뷰, Ghostty AI_POLICY.md; curl 바운티 수치는 보류), P6 노이즈(Greptile 2024 구버전, "AI code review bubble", Cloudflare 스레드의 비용 대비, **공식 "$15–25·~20분"**), H5(작성 모델 ≠ 리뷰 모델 — 한국 @bungker·@aer0700, `synchronize` 재리뷰 제거, nit 상한), 논쟁 B(무엇을 봐야 하나 — 코드에서 **결정**으로)
  - 왜: Cihan ICSE-SEIP 2025 "자동 리뷰 후 PR 종료 5h52m → 8h20m, 코멘트 73.8% 해결" — 리뷰는 공짜가 아니다·nit 상한의 근거, Xia & Miller(프리프린트) "no-review율 10%p ↑ → 유지보수 부담 약 6% ↑", Fu TOSEM 2025(정적 분석 경고를 주면 최대 55.5% 수정 — `@claude` 루프의 근거), Perry CCS 2023(AI 사용자가 더 안전하다고 믿음), Bacchelli & Bird 2013(리뷰의 실제 가치는 지식 전달), LLM 심판 장황함 편향 → Important/Nit 정의
  - 내 리포로: `/code-review`(+`--fix`)·`/security-review`·Writer/Reviewer 두 세션, 리뷰 기준은 CLAUDE.md 또는 리뷰 스킬(REVIEW.md는 서비스 전용) `[개인 즉시]`; action + REVIEW.md + `--max-turns` + 티어드 + 사람 승인 1명("2명 팀에서도 작성자 ≠ 승인자") `[팀 합의]`; 관리형 서비스·클라우드 라우팅·심각도 게이트 `[조직 결정]`. 측정: time to first review, `@claude`로 해결된 코멘트 비율
- **독자가 얻는 것:** 자기 플랜에서 가능한 리뷰 경로 하나와, 리뷰 기준 파일(CLAUDE.md 절 또는 REVIEW.md) 초안
- **레퍼런스:** 2.9, 4.1 #9·#12, 4.2 논쟁 B, 6.3 H5, 3.5(Bugbot `BUGBOT.md` 대비 한 줄), 7.5 논문 30·36·27·26·28·29·43·44·13·14
- **오프닝 기법:** 충격적 수치·사실 — "자동 리뷰를 붙였더니 PR이 닫히는 데 5시간 52분에서 8시간 20분이 걸렸다." (Cihan et al., ICSE-SEIP 2025)
- **클로징 기법:** 적용 과제 — 리뷰 기준을 한 페이지로 적어 보라: 세 pass, Important의 정의, Nit 상한, 보지 않을 것
- **스캐폴드 유형:** 비교 대조형
- **예상 분량:** 8,500자 (소절 6)

### 11장. 훅은 승인 게이트다 — allow, ask, deny, 그리고 설정의 층
- **대응 플레이:** 플레이 10 (Hooks as approval gates + Managed settings, Stage 5 Deploy)
- **핵심 질문:** 자동 승인하면 후회할 행동은 무엇이고, 그 앞에 사람을 어떻게 세우나 — 세션에서도, 아무도 답할 수 없는 파이프라인에서도?
- **주요 내용:**
  - 원문: 빌드 훅(allow/block, 사람 없음) vs 게이트 훅(`ask`·기록된 승인 대기), 4단계(생존해야 할 승인 목록·게이트 = 훅·팀 훅은 `.claude/settings.json`·non-negotiable은 관리형·"block은 스스로 설명해야"), `release-gate.sh` 원문(MCP `mcp__deploy-.*__release` 매처, `decide()` JSON, dev allow / staging ask(main 파이프라인은 allow) / prod CHG 티켓 검증, "비대화형에서는 ask를 답할 사람이 없어 deny"), 출력 JSON 두 예, "ask의 reason은 사람에게, deny의 reason은 Claude에게". 관리형 설정 예시 원문(`permissions.deny/allow`·`disableBypassPermissionsMode`·`sandbox`·`credentials`·`allowManagedHooksOnly`·`strictKnownMarketplaces`·`requiredMinimumVersion`)과 "control terms" 해설 — 개인판에서는 이 키들이 "해당 없음"임을 정직하게
  - 현행 사양: `permissionDecision` 4값(`defer` 추가 — **구버전 주의 박스**: `defer`·훅 5종·`requiredMinimumVersion` 2.1.193 vs 2.1.303), 우선순위 `deny` > `defer` > `ask` > `allow`, exit code 의미(0+JSON / 2 차단 / 1 비차단), `updatedInput`, MCP 매처 `.*` 필수, **설정 위치 표와 우선순위**(managed > `--settings` > local > project > user; 프로젝트 설정 커밋 → 전원 적용, 개인은 local로 오버라이드 가능), 규칙 문법(`Bash(npm run test *)`, `Read(./.env.*)`), `/status`·`/permissions`, 샌드박스(OS 경계·셸 명령만·macOS/Linux/WSL2·Windows 네이티브 미지원·`failIfUnavailable`·`/sandbox`), auto 모드와 deny 규칙("Deny rules block in every mode"), 훅 결정 로깅(`tool_decision source="hook"`, 기본 off). **그림 1** 설정 우선순위, **그림 2** 훅 결정 흐름
  - 현장: P7 훅 디버깅 고통 — #77212 `ask`가 bypass에서 조용히 통과(2.1.199) → **bcherny 공식 응답 2.1.233+ 작동**(이 조사에서 거의 유일한 서면 응답), `exit 2` 차단 상충(#13756·#80039 Windows·#55334 ↔ 공식 문서 우선, 플랫폼·버전 한정 결함으로 서술 — 4.1 #1), reason 미표시 보고, 디버깅 체크리스트(수동 실행 `echo $?` → `claude --debug` → 세션 재시작), H6 "강제 경계는 deny, ask는 편의", `rm -rf`·`force push` regex 차단은 휴리스틱; P10 Replit 사고(수치 보류, 골격만: 운영 DB 삭제·허위 통과 보고·이후 dev/prod 분리) = release-gate의 정반대 설계; 논쟁 G(책임), 토스 정세훈 "위임 여부는 우리가 결정"; 한국 보안은 정책 배경 + 인프런 "로직이나 구조만·더미 데이터"로만
  - 왜: **Parasuraman & Manzey 2010 "자동화 편향은 훈련·지시로 막을 수 없다"** → "조심하세요"는 대책이 아니고 구조(훅)가 대책; Parasuraman & Riley 1997 disuse(잦은 오경보로 무시) → `permissions.allow`로 안전 내부 루프를 사전 승인하는 이유; Bainbridge 1983(남는 사람 과제는 더 어렵다 — 승인 게이트는 쉬운 일이 아니다); Lee CHI 2025(GenAI 확신 ↑ → 비판적 사고 ↓, 자기 보고 한계)
  - 내 리포로: **"자동 승인하면 후회할 행동 목록"**(`git push --force`·운영 배포·`.env` 읽기·수정 중 테스트 파일·마이그레이션) → 각각 `PreToolUse` deny/ask 훅 하나, `~/.claude/settings.json` deny/allow + `/sandbox`, `decide()` 함수 재사용, **훅을 넣으면 직접 깨뜨려 보기** `[개인 즉시]`; `.claude/settings.json` 훅 커밋(끌 수 있음을 정직하게) `[팀 합의]`; 관리형 설정·체인지 티켓·`requiredMinimumVersion` `[조직 결정]`. 측정: 게이트 대기 체감, 되돌린 배포 횟수
- **독자가 얻는 것:** 후회 목록에서 뽑은 훅 3개와, 설정이 어디서 와서 무엇이 무엇을 덮는지 아는 눈
- **레퍼런스:** 2.10, 6.2(권한 규칙·샌드박스·훅 디버그 행), 6.3 H6, 4.1 #1·#2·#11, 4.2 논쟁 G, 4.3(ask vs deny 긴장), 3.4, 1.7(블로그판 `production-gate.sh` 대비), 7.5 논문 38·39·40·41
- **오프닝 기법:** 상황 가정 — "금요일 저녁 여섯 시. 에이전트가 `release`를 호출하려 한다. 당신은 자리를 비웠다. 이 호출은 통과돼야 할까?"
- **클로징 기법:** 질문 남기기 — "이 게이트를 끄는 데 당신은 몇 초가 걸리나? 그 답이 개인 훅과 팀 훅과 관리형 설정의 차이다."
- **스캐폴드 유형:** 개념 도입형
- **"이 장의 핵심" 박스:** 사용
- **예상 분량:** 9,500자 (소절 8)

### 12장. 파이프라인 안의 Claude — 헤드리스, 샌드박스, 환경별 자율 티어
- **대응 플레이:** 플레이 11 (CI/CD integration and deployment, Stage 5 Deploy)
- **핵심 질문:** 아무도 지켜보지 않는 러너에서 Claude를 돌릴 때, 무엇을 허락하고 무엇을 막고, 실패는 어떻게 알아보나?
- **주요 내용:**
  - 원문: 6단계(읽기 전용 판단 스텝부터 → 게이트 뒤의 쓰기 스텝(PR로만) → 컨테이너·단기 토큰 → MCP로 배포 노출 → 환경별 자율 티어 → 롤백은 가장 리허설된 경로), 트리아지 스텝 YAML(`if: failure()`), `.mcp.json`(deploy-dev/staging/prod, "허용 규칙은 서버와 툴을 지정하고 인자는 못 보므로 환경별 서버 분리"), 3툴 표(release/status/rollback), 스테이징 스텝(`--allowedTools "mcp__deploy-staging__*"` 3개 + `--permission-mode dontAsk`, 스테이징 토큰만), **3티어 표**(Dev 전부 / Staging ask 또는 main에서 allow / Prod `release` 비허용 → 훅 allow만이 유일한 길, fail-closed). governance "에이전트는 운영 게이트까지 갈 수 있고 넘을 수 없다". **그림 1** 3티어 흐름
  - 현행 사양: `dontAsk` 정의, `--permission-prompts none`(v2.1.259+), **`-p` 시작 모드 왕복 → CI는 항상 모드 명시**, `--allowedTools` vs `--tools` vs `--disallowedTools`(가시성 제한은 `--tools`), `--max-turns`·`--max-budget-usd`·`--json-schema`·`--restricted`·`--append-system-prompt`, `--bare`와 `.mcp.json`(2.1.286: 명령줄에 지정한 MCP만), Agent SDK(Python/TS, 다른 언어는 `-p` 서브프로세스, 서드파티에 claude.ai 로그인 제공 불가), Actions 클라우드 라우팅(OIDC), MCP 툴 설계(네임스페이스가 allowlist 경계), DORA 5지표 현행 정의(변경 리드타임·배포 빈도·실패 배포 복구 시간·변경 실패율·배포 재작업률; "MTTR → Failed Deployment Recovery Time"; Accelerate는 설문 상관 연구라는 한 줄), 업계 대비 한 줄(Codex Action `sandbox`/`safety-strategy`)
  - 현장: **P8 헤드리스 조용한 실패**(Wmedia 2026-07, 개인 블로그 — 권한 거부돼도 exit 0·`is_error: false`, 흔적은 `permission_denials`만 — 4.1 #6 "확인 필요", 안전 측 권고로), auto 모드 중단 "too many classifier denials in headless mode", bypass는 컨테이너+`--max-turns`+JSON과만, root 거부, H7, 헤드리스에서 에이전트 팀 불가
  - 왜: Bainbridge(자동화 실패 시 사람에게 남는 수동 개입 — "롤백은 가장 리허설된 경로"의 70년 전 근거), Xia & Miller(리뷰 건너뛴 기여의 부담), Kapoor(비용도 메트릭)
  - 내 리포로: `if: failure()` 트라이지 `claude -p` 한 스텝 `[개인 즉시]`; 개인 배포(Vercel/Fly/Cloud Run)에 MCP 서버 3개는 과하다 → **`deploy.sh dev|staging|prod` 한 스크립트 + `PreToolUse` 훅으로 `prod` 인자 deny/ask**(블로그판 `production-gate.sh` 문자열 매칭이 개인 규모에 맞는 형태, 우회 가능성 정직하게) + `rollback` 한 줄 명령을 스테이징에서 돌려 보기 `[개인 즉시]`; 브랜치 보호(에이전트는 PR만), GitHub Environments 토큰 분리, `dontAsk`+`--allowedTools`, `permission_denials` 검사 `[팀 합의]`; Bedrock/Vertex/Foundry·컨테이너 프로필·릴리스 매니저·에이전트 ID `[조직 결정]`. 측정: 사람 호출 없이 트리아지된 파이프라인 실패 비율, DORA 3개(배포 빈도·리드타임·실패율)는 개인도 git/CI에서
- **독자가 얻는 것:** 자기 CI에 넣을 첫 `claude -p` 스텝(읽기 전용)과 배포 스크립트 앞의 훅, 그리고 "조용한 실패"를 잡는 검사 한 줄
- **레퍼런스:** 2.11, 6.2(헤드리스·CI 권한 행), 6.3 H7, 4.1 #6, 1.7(블로그판 대비), 3.5(Codex Action), 7.4(DORA 지표), 7.5 논문 38·36·15·45
- **오프닝 기법:** 인용·일화 — "일을 하지 못한 실행과 전부 해낸 실행이 똑같이 보인다." (Wmedia, 2026-07, 개인 블로그 — 검증 필요 표시와 함께)
- **클로징 기법:** 한 문장 여운 — "롤백은 가장 많이 연습한 경로여야 한다. 에이전트가 그 명령을 처음 치는 날이 사고 날이어서는 안 된다."
- **스캐폴드 유형:** 문제-해결형
- **"이 장의 핵심" 박스:** 사용
- **예상 분량:** 8,500자 (소절 7)

### 13장. 루프를 닫는다 — 컨트롤 밴드에서 새 `intent.md`까지
- **대응 플레이:** 플레이 12 (Closing the loop on metrics + Claude Tag, Stage 6 Maintain) + 코스 레슨 14 맺음말
- **핵심 질문:** 사람이 시작하지 않아도 루프가 한 바퀴 돌 수 있나 — 그리고 그때 사람은 어디에 서 있나?
- **주요 내용:**
  - 원문: "Where every earlier stage needs a person to start it…", 컨트롤 밴드 정의(30일 시간당 평균·σ·1σ/2σ/3σ·확률 1/6·1/44·1/740·720 readings·웨스턴 일렉트릭 규칙 4/5·8연속), 7단계(안정 기준선 메트릭 하나·결정론적 탐지 스크립트(모델 없음)·`bands.yaml` 티어(1σ 로그/2σ 읽기 전용 진단/3σ PR 또는 사전 승인 런북)·트리거 층·`intent.md` 포맷으로 기록·트리아지(dismiss가 밴드를 튠)·사고마다 eval), `bands.yaml` 원문, 33줄 Python 원문(들여쓰기 복원), **사고 시나리오 사례 분석**: 13:52 릴리스 `4f2c9e1`이 `CACHE_SECONDS` 60→0 → 14:00 `{"tier": "3sigma", "reading": 1.9, "mean": 0.2, "sigma": 0.02}` → `rollback-deploy` 런북 14:02 → `8c41d07` 14:04 → 사고 `intent.md`(3장 포맷 그대로, "Action already taken" 절 추가) → `status-panel-keeps-its-cache.json` eval. 세 예시(CI 실패율·5xx·PR 사이클 타임 드리프트). Claude Tag 부속 절은 코스 인용으로 귀속("first responder" 묘사는 발표 페이지에 없음)
  - 현행 사양: Claude Tag(Team/Enterprise 베타, Opus 4.8 기반 — 개인 대안: Slack webhook → `claude -p`, Routines), Agent SDK 러너, `SessionStart` 훅으로 메트릭 스냅샷 주입, OpenTelemetry(**구버전 주의 박스**: 코스 "OTel export"는 기본 off·리포 설정 불가 → 개인은 `total_cost_usd`·세션 로그), Anthropic 내부 Monitor 트리아지 에이전트의 세 권한(= 2σ 티어 철학), Building effective agents의 "workflow"(탐지는 결정론·모델은 티어별로 가둠), SPACE 5차원·"최소 3차원", DORA 5지표(4.1 #13 — dora.dev 가이드를 1차로). **그림 1** 티어 → 라우트 흐름
  - 현장: P14 측정 공백(현장이 실제로 입에 올리는 지표 — PR 크기·리뷰 대기·"You are right!" 횟수·사용량 창 소진·리뷰당 비용; 벤더 수치는 "업계가 이렇게 말한다"), LY "confidence gate"(정량 없음), 논쟁 D 중간 입장(작업 크기에 오버헤드를 맞추라)
  - 왜: Shewhart 1930·웨스턴 일렉트릭 1956 — SPC는 70년 된 도구, "메트릭 루프는 새 발명이 아니라 소프트웨어로 옮겨 온 것"(1/6·1/44·1/740은 정규분포 단측 꼬리 근삿값으로 맞음); Goodhart 변종(게이트 조건을 지표로 삼으면 게임된다; 귀속 Strathern); SPACE(Activity는 폭증하는데 Performance는 아닐 수 있다 — AIDev 456,000 PR); METR·Ziegler(체감은 수락률에 끌려간다 — "재라"); Kapoor(비용도 메트릭)
  - 내 리포로: **CI 테스트 실패율 하나**(Actions API) + 33줄 스크립트 그대로 + 1σ 로그/2σ 읽기 전용 `claude -p`/3σ PR까지(런북 자동 롤백은 스테이징 리허설 뒤에만) `[개인 즉시]`; 최소 측정 세트: DORA 3개 + 비용(`total_cost_usd`) + 자기 보고 1개("이번 주 되돌린 횟수") `[개인 즉시]`; cron 워크플로 + `bands.yaml` 커밋 + 이슈 라벨 트리아지 큐 `[팀 합의]`; Claude Tag·Prometheus·Agent SDK 서비스·OTel `[조직 결정]`. 측정: 밴드 이탈 → `intent.md` 소요, 발견 → 머지 비율, 같은 급 사고 재발
  - 맺음말(코스 레슨 14 + 블로그판 "The loop keeps running. Human judgement stays above it.") — 이 장 마지막 소절에서 짧게. 리소스 순서는 개인용으로 재배열(memory → permission-modes → hooks → skills → worktrees → sub-agents → headless → github-actions → code-review → sandboxing → monitoring), 조직 전용은 "부록 참조"
- **독자가 얻는 것:** 메트릭 하나와 스크립트 하나로 자기 리포의 루프를 닫는 최소 구성, 그리고 "사람은 루프 위에 있다"는 자리
- **레퍼런스:** 2.12, 2.13, 3.1(Maintain 행), 4.1 #8·#13, 6.1(12행), 7.4, 7.5 논문 48·49·46·47·15·2·6·34
- **오프닝 기법:** 실패 장면 — "13:52, 릴리스가 나갔다. 14:00, 스크립트가 한 줄을 찍는다. `{"tier": "3sigma", "reading": 1.9, "mean": 0.2, "sigma": 0.02}`. 아무도 보고 있지 않다."
- **클로징 기법:** 다음 단계로 잇는 매듭 — 사고 `intent.md`가 `intent/` 폴더에 들어왔다. 이 파일을 읽을 사람은 3장의 당신이다. 루프가 한 바퀴 돌았다는 사실을 짧게 확인하고 끝낸다(회고는 14장에 양보)
- **스캐폴드 유형:** 사례 분석형
- **예상 분량:** 8,500자 (소절 7)

### 14장. 내 리포에서 루프 돌리기 — 첫 30일
- **대응 플레이:** 없음 (종합)
- **핵심 질문:** 책에서 만든 것을 전부 모으면 내 리포에는 어떤 파일이 생기고, 어떤 순서로 30일 안에 갖출 수 있나?
- **주요 내용:**
  - 관통 예제의 최종 파일 트리 한 장(레퍼런스 3.1 체인 표를 트리로): `intent/`(intent·spec·plan 3종 + 사고 intent), `CLAUDE.md`, `.claude/settings.json`(훅 2종), `.claude/hooks/`(api-policy·release-gate), `.claude/skills/secure-api-review/`, `.claude/agents/verifier.md`, `evals/`(JSON 2종·check.sh·log_bodies.py), `REVIEW.md`, `.mcp.json`, `.github/workflows/`(API policy·agent-evals·release·bands cron), `bands.yaml`. 각 파일 옆에 "몇 장에서 만들었나"와 "그 파일을 읽는 다음 파일"
  - 되짚기(나열 아닌 연결): 아티팩트 체인 — 3층 통제 — 검증 루프와 그 보호 — 설정의 회귀 테스트 — 사람의 눈을 의도로 — 게이트 — 루프 복귀. 각각 한 문단, 앞 장의 핵심 한 줄을 콜백
  - **첫 30일 도입 순서**(2장의 개인 진입 순서를 주 단위로, 합성 제안 명시): 1주 CLAUDE.md 감사 + "Verifying your work" + 테스트 보호 훅 / 2주 플랜 모드 기준표 + 후회 목록 훅 3개 + 첫 스킬 / 3주 `intent/` 폴더 + 첫 intent·spec·plan + `/code-review` 루틴 + 워크트리 2개 / 4주 eval 5개 + CI 트리아지 스텝 + CI 실패율 밴드. 팀이면 각 주에 `[팀 합의]` 항목을 한 줄씩 덧붙임
  - 최소 측정 세트 재확인(13장) + "느낌으로는 모른다"(1장) 콜백 — 30일 뒤 무엇을 비교할지(첫 패스 머지율·되돌린 횟수·사용량)
  - 한국 독자 주의 모음(레퍼런스 6.5): 비용(Pro/Max 창), 플랫폼(Windows 네이티브는 샌드박스 미지원·훅 보고 상이 → WSL2), 한국어 CLAUDE.md(길이가 언어보다 큰 변수), 보안·망분리는 정책 배경만. 공식 Best practices 실패 패턴 5종("kitchen sink"·"correcting over and over"·"over-specified CLAUDE.md"·"trust-then-verify gap"·"infinite exploration")을 각 장과 연결해 닫는다
  - 닫는 매듭: 책을 덮고 할 일은 하나 — `intent/` 폴더를 만들고 첫 `intent.md`를 쓰는 것. "The loop keeps running. Human judgement stays above it."을 번역해 마지막 문장으로
- **독자가 얻는 것:** 복사해 쓸 파일 트리와 30일 체크리스트, 그리고 자기 리포에서 루프를 한 바퀴 돌릴 때까지의 순서
- **레퍼런스:** 3.1, 1.6(진입 순서), 6.1, 6.4, 6.5, 2.13(리소스 순서)
- **오프닝 기법:** 앞 장 콜백 — "앞 장 끝에서 사고 `intent.md`가 `intent/` 폴더에 들어왔다. 이제 그 폴더 옆에 무엇이 함께 있는지 전부 꺼내 보자."
- **클로징 기법:** 회고형 닫는 매듭 — 여정 회고 + 독자가 가져갈 관점 한 문장
- **스캐폴드 유형:** 종합 정리형
- **예상 분량:** 6,000자 (소절 5)

## 통권 변주 배정표

인접 장은 오프닝 기법이 다르고, '상황 가정'은 14장 중 2장(4·11장, 1/3 이하)이다. 클로징은 네 가지 형태가 번갈아 들고 13·14장만 매듭형이다. 저술가는 자기 묶음 밖의 장이 무엇으로 열고 닫는지 이 표로 확인한다.

| 장 | 단계 / 플레이 | 오프닝 기법 | 클로징 기법 | 스캐폴드 | 핵심 박스 | 그림 | 분량(자) |
|---|---|---|---|---|---|---|---|
| 1 | 도입 | 충격적 수치·사실 | 질문 남기기 | 사례 분석형 | — | — | 6,500 |
| 2 | 도입 | 정의 뒤집기 | 적용 과제 | 개념 도입형 | — | 2 | 8,000 |
| 3 | Plan·Design / P1+P2 | 인용·일화 | 한 문장 여운 | 문제-해결형 | — | — | 8,500 |
| 4 | Build / P3 | 상황 가정 | 질문 남기기 | 비교 대조형 | — | — | 8,000 |
| 5 | Build / P4 | 실패 장면 | 적용 과제 | 문제-해결형 | 사용 | — | 8,500 |
| 6 | Build / P5 | 앞 장 콜백 | 한 문장 여운 | 개념 도입형 | 사용 | 선택 | 9,000 |
| 7 | Build / P6 | 수사적 질문 | 질문 남기기 | 비교 대조형 | — | 1 | 7,500 |
| 8 | Test / P7 | 실패 장면 | 적용 과제 | 문제-해결형 | — | — | 8,000 |
| 9 | Test / P8 | 정의 뒤집기 | 한 문장 여운 | 사례 분석형 | 사용 | — | 9,000 |
| 10 | Deploy / P9 | 충격적 수치·사실 | 적용 과제 | 비교 대조형 | — | — | 8,500 |
| 11 | Deploy / P10 | 상황 가정 | 질문 남기기 | 개념 도입형 | 사용 | 2 | 9,500 |
| 12 | Deploy / P11 | 인용·일화 | 한 문장 여운 | 문제-해결형 | 사용 | 1 | 8,500 |
| 13 | Maintain / P12 | 실패 장면 | 다음 단계로 잇는 매듭 | 사례 분석형 | — | 1 | 8,500 |
| 14 | 종합 | 앞 장 콜백 | 회고형 닫는 매듭 | 종합 정리형 | — | — | 6,000 |

- 오프닝 분포: 충격 수치 2(1·10) · 정의 뒤집기 2(2·9) · 인용·일화 2(3·12) · 상황 가정 2(4·11) · 실패 장면 3(5·8·13) · 앞 장 콜백 2(6·14) · 수사적 질문 1(7).
- 스캐폴드 분포: 사례 분석 3 · 개념 도입 3 · 문제-해결 4 · 비교 대조 3 · 종합 정리 1.
- 금지: 모든 장에서 "이 장에서는 ~를 다룬다" 메타 선언, "다음 장에서는 ~" 예고 공식, `## 마무리` 헤딩 강제. 이음은 위 클로징 기법으로만.
- 훅이 6·8·11·12장에 반복 등장하므로, 각 장은 "이 단계에서 훅이 맡는 역할"만 말하고 사양 설명의 본진은 11장임을 교차 참조로 가리킨다(6장: 빌드 가드레일·`PostToolUse`, 8장: 테스트 파일 보호·`Stop`, 11장: 승인 게이트·`permissionDecision`·설정 층, 12장: 파이프라인에서의 fail-closed).

## 분량 규약

- **기준:** 순수 산문(표·코드 블록·mermaid·인용 블록 제외) 글자 수. `book-editing/scripts/length_report.py`로 실측한다.
- **장 목표:** 위 표의 값, 허용 편차 ±15%. 전체 약 114,000자.
- **소절:** 장당 5~8개(`###`), **소절당 순수 산문 3,000자 상한**. 목표 분량이 기본값(3,000~6,000)을 넘는 장은 문단을 늘리지 않고 소절을 늘린다.
- **코드 블록:** 코스 예시 파일은 원문 전체를 싣는다(잘라 쓰지 않는다). 11장(`release-gate.sh` + 관리형 설정 JSON)·9장(`agent-evals.yml` + `check.sh` + `log_bodies.py`)·13장(33줄 Python)은 코드가 길어 산문 대비 코드 비율이 높아도 괜찮다 — 산문 목표는 그대로 지킨다.
- **"내 리포로 옮기기" 절:** 장당 800~1,500자. 세 태그가 모두 등장하되 `[조직 결정]`은 한 문단을 넘지 않는다.
- **"구버전 주의" 박스:** 3~5문장. 장당 최대 2개.

## 저술가 묶음 제안 (오케스트레이터 참고)

4명 병렬 기준, 연속 묶음: **A** 1~3장(도입+Plan·Design) · **B** 4~7장(Build) · **C** 8~10장(Test+리뷰) · **D** 11~14장(게이트·CI/CD·Maintain·종합). D는 14장을 쓰기 위해 다른 묶음의 파일 트리를 알아야 하므로, 14장은 레퍼런스 3.1 체인 표를 정전으로 삼아 쓰고 editor가 실제 산출과 대조한다.

## 사용자 판단이 필요한 것

1. **관통 예제 유지(보험사 포털) vs 한국 예제로 교체** — 계획은 유지를 채택했다(설계 근거 대안 4·5). 교체를 원하면 플레이 체인 15개 파일을 새 도메인으로 재설계해야 하므로 계획 재실행이 필요하다.
2. **플레이 1·2 합본(3장)** — 분리를 원하면 15장이 된다.
3. **14장 종합 장 유무** — 13장이 이미 루프를 닫으므로 13장으로 끝내고 14장의 파일 트리·30일 순서를 부록으로 내리는 안도 성립한다.
4. **리서치 보강 여부** — 레퍼런스 8장에 따라 다음은 책이 약속하지 않는다: 한국 대기업(우아한형제들·카카오·네이버) 도입기, 망분리·결재 현장 후기, Windows 네이티브 훅 검증, 에이전트 팀 사용법, `.claude/rules/` 실무 사례. 이 가운데 하나라도 책에 넣고 싶다면 리서치 보강이 필요하다. 개인 eval 사례는 커뮤니티에 없어 9장이 "저자 구성 예시"로 채운다 — 이 표기를 유지할지 확인.

## 개정 이력

| 날짜 | 변경 | 사유 |
|---|---|---|
| 2026-10-19 | 초안 작성 (v1) | — |
