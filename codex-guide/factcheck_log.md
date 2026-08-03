# factcheck_log — `codex-guide`

> Phase 4 사실 검증 원장. **단일 append-only 파일.** 장마다 `## {NN}장 — 라운드 {N}` 섹션으로 누적한다.
> 판정: ✅ 확인 / ❌ 오류(수정안 필수) / ⚠️ 불확실(귀속·약화 필요) / 🕒 시점 민감(신선도 앵커 필요)
>
> **❌·🕒 판정과 에스컬레이션은 BLOCKING이다.** 스타일 이견과 달리 사실 오류·미해소 마커는 **저술가 재량으로 덮을 수 없다.** 정정·출처 확보·삭제 셋 중 하나로만 닫는다.
>
> **1차 대조 원장:** `research/codex-docs-raw/`(공식 문서 원문 캐시 69파일 — 최종 판정 기준) → `research/web-*.md`·`community*.md`·`papers.md` → `01_reference.md`
> **판정 우선순위:** `fact_rules_active.md`(FR-1~) > `02_plan.md` 저술 규율 > `01_reference.md`

---

## 01장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/01_draft.md`(스타일 반영본) · 구체 주장 40건 추출

**집계: ✅ 35 / ❌ 2 / ⚠️ 3 / 🕒 0**

### ❌ 정정 필요 (BLOCKING)

#### ❌-1. "changelog 항목만 95개다" (L99)

- **원문:** "색인해보면 changelog 항목만 95개다."
- **판정:** ❌ — 1차 원장에서 재현되지 않는 수치. 리서치 색인 기준 서술로도 성립하지 않는다.
- **근거:**
  - `research/codex-docs-raw/codex__changelog.md` — 날짜 카드(`^ YYYY-MM-DD $` 헤더) **81개**, 고유 날짜 **74개**. 월 내비게이션이 열거하는 14개월(2025-05 ~ 2026-07)이 캐시에 **전량 존재**하므로 캐시 누락으로 인한 과소 집계가 아니다.
  - `research/web-1.md` L967 — "총 **95개 항목**"이라 적었으나, **같은 파일의 전수 색인 자체가 87행**이다(2026년 7월 9 + 6월 12 + 5월 11 + 4월 8 + 3월 12 + 2월 12 + 1월 4 = 68행, 2025년 섹션은 "27건"이라 표기했으나 **실제 열거는 19행**). 즉 리서처의 라벨(95)과 리서처 자신의 색인(87)과 원문 캐시(81)가 **삼중으로 어긋난다.**
  - 월별 대조에서도 캐시와 리서치 색인이 양방향으로 불일치한다(2026-02: 캐시 14 vs 색인 12 / 2026-07: 캐시 8 vs 색인 9). 어느 한쪽을 정전으로 삼아도 95는 나오지 않는다.
- **저술가 질의에 대한 답:** "리서치 색인 기준 서술"은 **타당하지 않다.** 그 색인 자체가 자기 라벨과 8건 어긋나므로, 색인을 근거로 삼으면 근거가 근거를 반박한다. 원문 날짜 헤더 69개라는 저술가 측 관측과도 다시 어긋나므로(캐시 실측 81), **어떤 정확 수치도 이 원장으로는 확정할 수 없다.**
- **수정안 (택1):**
  - **A안(권장 — 수치를 하한으로 낮춘다):** "색인해보면 2025년 5월부터 2026년 7월까지 여든 건이 넘는 항목이 쌓여 있다."
    (근거: 캐시 날짜 카드 81개, 14개월 전량 포함 — 하한 주장이므로 세 집계 어느 쪽으로도 반박되지 않는다)
  - **B안(수치 제거):** "색인해보면 2025년 5월부터의 릴리스가 한 페이지에 전부 쌓여 있다."
- **주의:** 이 문단의 논지("굵은 마디만 뽑아 세워보자")는 수치에 의존하지 않는다. 정확도가 불확실한 숫자를 논지 없는 자리에 두면 손실만 남는다.

#### ❌-2. 표 2 Codex SDK 위치 표기 (L78)

- **원문:** `| Codex SDK | 오픈소스 | `openai/codex/sdk` |`
- **판정:** ❌ — 표 캡션이 "`/codex/open-source`의 컴포넌트별 공개 경계"라 **원문 표기여야 하는데** 원문과 다르다.
- **근거:** `research/codex-docs-raw/codex__open-source.md` L15 — "Where to find" 셀의 표시 문자열은 **`openai/codex/codex-sdk`**다(링크 URL만 `.../tree/main/sdk`).
- **수정안:** `openai/codex/codex-sdk`로 교체.
- 참고: 같은 표의 나머지 6행(`openai/codex` / `openai/codex/codex-rs/app-server` / `openai/skills` / IDE 확장 Not open source / Codex cloud Not open source / `openai/codex-universal`)은 **전부 원문 일치 ✅**.

### ⚠️ 출처·귀속 주의

#### ⚠️-1. "Claude Code는 CLI 층이 비공개다" (L89) — FR-3 화이트리스트 밖 (통과, 기록)

- **판정:** ⚠️ → **수정 불요, 예외로 기록.**
- **근거:** `01_reference.md` §2-7 L147이 이 주장을 직접 담고 있고, `02_plan.md` 1장 소절 3이 "Claude Code는 CLI 층이 비공개이므로 CLI 층에서 정확히 뒤집힌 구도"를 **명시적으로 지시**한다.
- **화이트리스트 판단:** FR-3의 금지 열거(버전·플래그명·기본값·이벤트 개수·요금·모델 라인업)에 해당하지 않고, 계획이 승인한 서술이다. 또한 대상 독자가 **직접 확인 가능한** 성질의 사실이므로 규율 12의 안전 문형("독자가 이미 아는 것으로 취급") 취지에 부합한다.
- 규율 10("Codex는 오픈소스다"라고 쓰지 않는다) 준수 ✅ — 본문 L71이 오히려 그 문장을 **사실 오류로 명시**한다.

#### ⚠️-2. "같은 기간 Claude Code는 CLI/SDK 중심을 지켰다" (L125)

- **판정:** ⚠️ 1차 출처 없음 — 이 장에서는 통과, **12장 승격 시 고지 의무.**
- **근거:** `01_reference.md` §4-5가 같은 문장을 담으나, 이 책의 리서치는 **Claude Code 문서를 1차 수집하지 않았다**(규율 12의 전제). 즉 이 대비의 한쪽은 1차 소스가 없다.
- **이 장 판정:** 본문에서는 부수적 대비 한 문장이고 독자 자신의 경험으로 검증 가능하므로 통과.
- **구속력 있는 후속:** 12장은 이 연표를 **"진화 방향이 갈렸다"는 논지의 증거로 승격**한다(계획 내러티브 아크). 증거로 승격하는 순간 1차 소스 부재가 논지 결함이 되므로, **12장에는 "이 책이 1차로 수집한 것은 Codex 쪽 연표뿐"이라는 한 줄 고지가 필수다.** → `fact_rules_active.md` FR-9로 승격.

#### ⚠️-3. 그림 1과 본문 L63의 어긋남

- **원문:** 그림 1이 `CX(Codex) --> WEB["웹 (chatgpt.com)"]`으로 웹을 Codex 하위 표면으로 그린다. 그런데 본문 L63은 "웹(chatgpt.com)은 Chat과 ChatGPT Work를 제공하고, **Codex 전용 개발자 뷰는 데스크톱 앱·CLI·IDE 쪽에 있다**"고 적는다.
- **근거:** `01_reference.md` §2-4와 일치하는 쪽은 **본문**이다. 그림이 본문을 반박한다.
- **수정안(택1):** ⓐ `WEB` 노드를 `GPT` 직속으로 옮긴다 ⓑ 노드 라벨을 `웹 (chatgpt.com)<br/>Chat · Work 중심`으로 바꿔 본문과 일치시킨다.

### ✅ 확인됨 (35건 — 근거 요약)

**원문 verbatim 대조 (표·인용 전량 일치)**
- 표 1 `/codex/use-chatgpt` 3분법 3행 — `codex__use-chatgpt.md` L32-36 **완전 일치**
- 표 3 `/codex/feature-maturity` 4등급 정의 — `codex__feature-maturity.md` L7-12 **완전 일치**
- "The updated desktop app is available globally on every ChatGPT plan, including Free." — `codex__whats-new.md` L128-130
- "ChatGPT can read and modify files in the folder you choose" — `codex__app.md` L23 / `01_reference.md` §2-1
- "The CLI inherits most defaults from `~/.codex/config.toml`. Any `-c key=value` overrides you pass at the command line take precedence for that invocation." — `codex__developer-commands.md` L34
- IDE Note "The IDE extension automatically includes your open files as context…" — `codex__prompting.md` L332
- "Currently, you can't change the default model for Codex cloud chats." — `codex__models.md` L508
- "Filter by term, definition, or surface" — `codex__glossary.md` L9
- "Added Import to Codex flows for importing supported setup from Claude Code and Claude Cowork, including during onboarding." — `codex__changelog.md` L321-322 (2026-06-09 · Codex app 26.608)

**수치**
- 전역 플래그 **20** / 서브커맨드 **28** / 내장 슬래시 명령 **약 60** (L59) — 3건 모두 실측 일치. 근거: `web-2.md` L3349 "Global flags (20행)"·L3376 "Command overview (28행)"(HTML `astro-island` 복원표), `codex__developer-commands.md` Command details 섹션 27개 중 `codex archive`·`unarchive` 합본 1개 → **28**, 슬래시 명령 고유 토큰 **60개**. 교차 검증: `01_reference.md` §2-2의 "experimental 7 + stable 21 = 28"과 정합.
  - 나이트: "Global flags" 20행 중 1행은 위치 인자 `PROMPT`다. 다만 원문 표 제목이 그러하므로 **원문 충실 서술로 통과.**

**연표 (전 마디 대조 — `codex__whats-new.md` + `codex__changelog.md`)**
- 2월: 앱 macOS 출시(병렬 프로젝트 chat·내장 Git 리뷰·worktree·스킬·예약 작업) + 같은 주 턴 중간 steering·이미지 외 파일 첨부 / **다음 주** chat 포크·always-on-top — L518-541 및 L505-517 ✅
- 3월: Windows 네이티브(PowerShell·샌드박스, WSL 잔존) + **"GPT-5.4 also arrived in Codex that week"** ✅ / 후속 3종(터미널 출력 검사 L459·컴포저 도구 선택 L431·플러그인 패키징 L418)
  - 나이트: 본문의 3종 나열 순서가 실제 시간순의 역순이다(터미널 검사 3/9-13 → 컴포저 3/16-20 → 플러그인 3/23-27). "이어서 ~ 붙는다"가 순서를 주장하지는 않으므로 통과하되, 순서를 맞추면 더 정확하다.
- 4월: PR 검토·머지(4/6-10) → 브라우저 조작·승인 자동 리뷰(4/20-24) ✅ 시간순 정확
- 5월: Chrome 확장(5/4-8) · Appshots·goal(5/18-22) · 모바일 이어받기(5/11-15) · 원격 제어(5/25-29) ✅
- 6월: 임포트(6/9) · Sites(6/2) · Record & Replay(6/18) ✅
- 7월 9일 병합 ✅ ("On July 9, the Codex app merged into the ChatGPT desktop app for macOS and Windows.")
- **7월 9일 ChatGPT Work 출시 ✅** — 원문 직접 인용 확보: "ChatGPT Work launched July 9, 2026." (`/codex/enterprise/work-admin-faq`, `web-5.md` L136·L1164). 같은 날 서술 정확.
- **7월 15일 Codex Micro ✅** — 원문 "On July 15, OpenAI and Work Louder launched Codex Micro, a limited-run physical control surface…" (`codex__whats-new.md` L58-64). "최대 여섯 개 chat 상태"·"아날로그 스틱과 다이얼로 추론 강도 조절"까지 원문 일치.
- 7월 20~24 다중 폴더·ChatGPT Voice ✅ — `codex__whats-new.md` L9-30. **primary/secondary 서술이 원문과 정확히 일치**("Choose a primary folder for new chats, Git operations, and automatic discovery of `AGENTS.md`, skills, and `config.toml`. Secondary folders remain available for file search, reading, and editing.")
- 2026-07-28 Codex Security ✅ — **커뮤니티 관측 귀속이 정확하다.** 근거 `community.md` §3-9(HN 49089755, 2026-07-28, 596pts). 규율 9 준수.

**그 외**
- whats-new / changelog 성격 구분 — 원문 "This weekly digest highlights … features that can change how you work" vs "For every versioned update, bug fix, and minor improvement" (`codex__whats-new.md` L5-7)와 정확히 대응
- Visualizations CLI·IDE 미렌더 — `codex__visualizations.md` L48 "Visualization rendering isn't supported"
- 성숙도: 정의표만 있고 기능별 명단 없음 / 실제 라벨("research preview"·"public beta")과 등급명 불일치 / "4단계 체계를 쓴다"는 과잉 일반화 — `01_reference.md` L100과 일치. **규율 8 준수 ✅**
- 라벨 실례 4종 — 권한 프로필 Beta(FR-8) / Chronicle "opt-in research preview"(`codex__customization__chronicle.md` L5) / Python SDK beta(`01_reference.md` §2-6, `web-3.md` L1919) / 일부 서브커맨드 experimental(§2-2의 7개) ✅
- Codex for OSS 혜택 3종 — "API credits, ChatGPT Pro with Codex, and selective access to Codex Security" 원문 일치
- 이슈 접수 창구 단일화 — `codex__open-source.md` L23-27 원문 일치
- **Gorinova et al., arXiv:2606.17799 ✅** — `papers.md` §1-8에 저자 6인·arXiv 등재일(2026-06-16)·개정일(2026-07-18) 전량 기재. 식별자 형식 유효, YYMM(2606)이 빌드 시점(2026-08-02) **과거** → 자동 ❌ 규칙 비해당. 본문이 "아직 동료 심사를 거치지 않은 프리프린트"로 **등급을 명시 ✅**
- **Yang et al., SWE-agent, NeurIPS 2024, arXiv:2405.15793 ✅** — `papers.md` §2-1. peer-reviewed 등급 표기 정확. ⏳ 낡음 수치(SWE-bench 12.5%)를 **인용하지 않은 것도 정확한 판단**(레퍼런스 §7 낡음 표시 필수 항목)

### 규율 준수 메모 (판정 아님)

- **규율 6(인용 금지 9건):** 위반 없음 ✅. `/codex/overview` UI 삽화 문자열("5.6 Sol Extra High" 등) 미사용 ✅
- **규율 7(WSL 경로 성능 권고):** 미등장 ✅
- **규율 11(경험담 금지):** 위반 없음 ✅ — 1인칭 일화 0건
- **FR-2 배치:** `(2026-08-02 문서 기준)`이 표 1·2·3 캡션 **3회**, 본문 0회. FR-2 문언은 "장당 첫 등장 1회 + **수치 표** 캡션"인데 이 셋은 정의·분류 표다. 앵커 자체는 확보됐으므로 사실 결함은 아니다. 권고: 표 1 캡션만 남기고 표 2·3에서 제거하거나, 본문 첫 등장 1회로 옮긴다. (비블로킹)

---

## 02장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/02_draft.md`(스타일 반영본) · 구체 주장 39건 추출

**집계: ✅ 38 / ❌ 0 / ⚠️ 1 / 🕒 0**

> 이 장은 **인용 밀도가 가장 높은데 오류가 0건**이다. 원문 대조 항목 20건이 전부 verbatim 일치했다. 특히 `/codex/app-server`는 원문 캐시에 파일이 없어 `web-3.md` §8-2의 전사본으로 대조했는데, 인용 6건이 전사본과 문자 단위로 일치했다.

### ⚠️ 정밀도 보정 (비블로킹, 수정안 제시)

#### ⚠️-1. `CODEX_HOME`과 인증 캐시의 동반 이동 (L123)

- **원문:** "`CODEX_HOME`의 기본값은 `~/.codex`이니, **이 경로를 옮기면 인증 캐시도 함께 따라간다.**"
- **판정:** ⚠️ 조건 누락 — **파일 저장(`file`) 모드에서만 참이다.**
- **근거:** `web-5.md` L263-266 (`/codex/auth` 원문) — "`file` — stores credentials in `auth.json` **under `CODEX_HOME`** (defaults to `~/.codex`). / `keyring` — stores credentials in your **operating system credential store**. / `auto` — uses the OS credential store when available, otherwise falls back to `auth.json`." 즉 `keyring` 모드에서는 자격증명이 `CODEX_HOME` 밖(OS 키체인)에 있으므로 따라가지 않는다. 헤드리스 폴백 주의 문구도 같은 취지다 — "If your OS stores credentials in a credential store instead of `~/.codex/auth.json`, this method may not apply."
- **수정안:** "`CODEX_HOME`의 기본값은 `~/.codex`다. **파일 저장을 쓴다면** 이 경로를 옮길 때 인증 캐시도 함께 따라간다."
  (바로 다음 문장이 이미 "파일 저장을 쓴다면"으로 시작하므로, 조건절을 앞 문장으로 당기면 문단 흐름도 자연스러워진다.)

### 저술가 명시 요청 판정

#### 판정 ②. `"Importing doesn't change or delete your existing agent setup."`의 보증 주어 — **✅ 확인됨. 소절 4 마지막 문단의 소극적 표현은 타당하다.**

- **검증 대상 서술(L108):** "문서가 보증한 것은 'your existing agent setup', 그러니까 **떠나온 쪽** 설정을 건드리지 않는다는 것이다. 도착한 쪽 설정, 즉 이미 손봐둔 `~/.codex/config.toml`까지 그대로 둔다는 약속은 저 문장에 들어 있지 않다."
- **판정 근거 3중:**
  1. **문맥이 주어를 확정한다.** `codex__import.md` L6-9 — 문서 도입부가 "bring your instructions, settings, skills, plugins, projects, and recent work **from other agents** into the ChatGPT desktop app"이라 범위를 세운 **직후** L10에 문제의 문장이 온다. 이 문맥에서 "your existing agent setup"은 임포트의 출처인 외부 에이전트 쪽 설정을 가리킨다.
  2. **문서 자신의 절차 목록이 같은 표현을 같은 자리에 둔다.** L40-45 "When you import, ChatGPT: 1. Detects supported setup and recent work. 2. Imports the items you select. **3. Leaves your existing agent setup unchanged.** 4. Checks whether imported plugins or connections still need setup." — 감지·임포트 대상(= 외부 에이전트 산출물)을 다루는 단계 목록 안에 놓여 있다.
  3. **도착지 보호는 별도로, 훨씬 좁게 열거돼 있다.** `web-3.md` L1813(`/codex/app-server` 원문) — "Detection returns only items that still have work to do. For example, Codex skips AGENTS migration when `AGENTS.md` already exists and is non-empty, and skill imports don't overwrite existing skill directories." 도착지 비파괴가 **`AGENTS.md`와 스킬 디렉터리 두 항목으로 한정 열거**된다는 사실이, 그 보호가 `config.toml`까지 미치지 않음을 방증한다. 초안이 이 열거를 바로 앞 문단(L100-104)에 배치해 근거로 삼은 구성은 정확하다.
- **왜 소극적 표현이 옳은가:** 초안은 "문서가 도착지 설정을 덮어쓴다고 인정했다"고 주장하지 **않는다.** "저 문장에 들어 있지 않다"는 **부재의 진술**이며, 실제 사고는 [#24515]를 "커뮤니티 보고, open"으로 별도 귀속했다(L21). 규율 4·9가 요구하는 출처 등급 분리를 정확히 지킨 형태다. 더 강한 표현("문서가 도착지를 보호하지 않는다"·"임포트는 도착지를 덮어쓴다")은 원장으로 뒷받침되지 않으므로 **강화하지 마라.**
- **추가 권고:** 없음. 현행 유지.

#### 판정 ③. "커스텀 슬래시 명령 자리는 있으나 deprecated, 스킬로 수렴 중" — **✅ 확인됨**

- **검증 대상:** 본문 L50("Codex에도 커스텀 프롬프트라는 자리가 있기는 하지만, 그쪽은 이미 폐기 예정으로 표기돼 있다. 재사용할 지시 묶음은 스킬이라는 한 가지 그릇으로 모으겠다는 방향이 정해져 있는 것이다") + 표 2 행("Custom prompts (`~/.codex/prompts/`) | 커스텀 슬래시 명령 | 대응하나 **Codex 쪽은 deprecated**")
- **근거 4중:**
  1. **원문 첫 문장 verbatim:** "**Custom prompts are deprecated.** Use skills for reusable instructions that Codex can invoke explicitly or implicitly." (`web-6.md` L1270 = `/codex/custom-prompts`). 대체재로 skills를 **문서가 직접 지정**하므로 "스킬로 수렴 중"은 해석이 아니라 원문 진술이다.
  2. **경로 표기 정확:** `~/.codex/prompts/` — `web-6.md` L1282("최상위 `.md` 파일만 스캔")
  3. **임포트 표가 같은 방향으로 착지한다:** `codex__import.md` L58 "Slash commands → **Skills**" — 폐기 예정 기능이 아니라 스킬로 보낸다.
  4. **연표 근거:** changelog **2026-01-22 "Custom prompts deprecated"** (`web-1.md` 자료 19 색인) — 수렴이 진행 중인 상태임을 날짜로 확인.
- **화이트리스트 점검:** 표 2의 Claude Code 측 셀은 "커스텀 슬래시 명령"뿐이며 이는 `01_reference.md` §1-5 L76과 **문자 단위로 동일**하다. FR-3 준수 ✅. (`web-6.md` L1327이 Claude Code 측 경로 `~/.claude/commands/*.md`까지 대응시키지만, **초안이 이를 쓰지 않은 것은 옳은 판단**이다 — 화이트리스트 밖이다.)
- **주의(6장 인계):** 6장 소절 3이 이 기능의 주 서술이다. 이 장에서 이미 "폐기 예정"을 못 박았으므로, 6장은 **중복이 아니라 심화**로 가야 한다.

#### 판정 ④. CLI `/import` 명령 서술 — **✅ 확인됨 (인용 출처는 L404 표, L535-544가 아님)**

- **검증 대상(L56):** "원문 설명은 'Import Claude Code setup, project files, and recent chats'이고… 제약도 명시돼 있다. **로컬 TUI 세션에서만** 쓸 수 있고, 작업이 실행 중이거나 원격 세션이거나 로컬 app-server 데몬에 연결된 상태에서는 사용할 수 없다."
- **인용문 근거:** `codex__developer-commands.md` **L404**(내장 슬래시 명령 표) — "| `/import` | **Import Claude Code setup, project files, and recent chats.** | Migrate supported external-agent artifacts into Codex configuration and local files. |" → **verbatim 일치 ✅**
  - ⚠️ 저술가가 지목한 **L535-544 절에는 이 문장이 없다.** 그 절의 문안은 "Import Claude Code configuration with `/import`" (제목) / "Choose the Claude Code setup, project files, or recent chats you want to migrate."(2단계)다. 인용 자체는 정확하나 **행 근거는 L404**이다. 각주·출처 메모를 남길 계획이라면 L404로 적어라.
- **제약 근거:** 같은 파일 **L543-544** — "Run `/import` from a local TUI session. It's unavailable while a task is running, in remote sessions, and while connected to the local app-server daemon." → 초안의 3제약 서술이 **원문과 1:1 대응 ✅**
- **부수 확인:** `research/web-2_v1_webfetch.md` L2511에 다른 설명문("Import Claude Code setup and configuration")이 남아 있으나 이는 **1차 수집 v1의 폐기본**이다. 확정본 `web-2.md` L3298과 원문 캐시가 일치하므로 현행 인용이 옳다. 이후 장에서 v1 파일을 근거로 쓰지 마라.

### ✅ 확인됨 (38건 — 근거 요약)

**`/codex/app-server` 인용 6건 — 전량 verbatim (`web-3.md` §8-2 전사본 대조)**
- 오프닝 인용 "Import /Users/me/project/CLAUDE.md to /Users/me/project/AGENTS.md." — detect **응답** 예시 내 `AGENTS_MD` 항목의 `description`. 초안의 "JSON-RPC 응답 예시다"라는 위치 서술까지 정확 ✅
- `"source": "claude-code"`가 **요청** 예시에 있다는 서술 ✅ (import 요청 params)
- `~/.claude/skills` → `~/.agents/skills` 스킬 폴더 복사 — 같은 응답 예시의 `SKILLS` 항목 ✅
- "Use `externalAgentConfig/detect` to discover external-agent artifacts that can be migrated, then pass the selected entries to `externalAgentConfig/import`." ✅
- `source` 파라미터 역할 — 원문 "labels the product that produced the selected migration items"의 정확한 번역 ✅
- itemType 9종 verbatim — `AGENTS_MD`·`CONFIG`·`SKILLS`·`PLUGINS`·`MCP_SERVER_CONFIG`·`SUBAGENTS`·`HOOKS`·`COMMANDS`·`SESSIONS` ✅ (그림 1의 9종 나열도 일치)
- `importId` / `import/progress` / `import/completed` / 타입별 `successes`·`failures`를 담은 `itemTypeResults` / `readHistories` ✅
- `detect`가 `includeHome`·`cwds`(배열)를 받는다 ✅
- `codex app-server`는 experimental + "may change without notice" ✅ (`01_reference.md` §2-2)

**`/codex/import` 대조 — 전량 일치 (`codex__import.md`)**
- 표 1 임포트 대응표 **10행 전부 verbatim** (L48-59) ✅
- "Importing doesn't change or delete your existing agent setup." (L10) ✅
- Settings > Import / 없으면 General > "Import other agent setup" / 5단계 (L21-27) ✅
- "임포트 후 검토" 5항목 — 스킬·에이전트 권한 / MCP 커스텀 인증·헤더·환경 변수·트랜스포트(재로그인 가능성) / 훅 / 플러그인·마켓플레이스 / 인자·셸 보간·경로 플레이스홀더 의존 프롬프트 템플릿 (L74-83) ✅ **5항목 순서까지 일치**
- 중복 방지 규칙 verbatim ✅ / 마켓플레이스 추론(`extraKnownMarketplaces` → `anthropics/claude-plugins-official`) verbatim ✅ / Standard Claude Chat 임포트 불가 ✅ (`web-1.md` L181)
- "Chats from the last 30 days" 30일 제한 ✅

**[#24515] 메타데이터 — 6항목 전량 일치 (`community.md` L100-105)**
- 2026-05-26 개설 ✅ / CLI **0.133.0** ✅ / macOS arm64 ✅ / 👍 **0** ✅ / open ✅ / 인용 "Every subsequent Codex command prompts for user approval" ✅
- `approvals_reviewer`가 `guardian_subagent` → `user`로 리셋됐다는 서술 ✅
- **귀속 등급 정확:** "단일 보고자의 커뮤니티 관측이고, 공식 문서가 인정한 동작이 아니다"(L21) — 원장 등급 `[출처 명확 — 재현 절차·환경 명시, 다만 단일 보고자]`와 정확히 대응. **규율 4 준수 ✅**

**소절 1 안전 절차 5종**
- 깨끗한 git 트리 — suparious, #11626 댓글 ✅ (`community.md` L25·L382)
- `--sandbox` 3값 `read-only`·`workspace-write`·`danger-full-access` ✅ (`01_reference.md` §2-2 전역 플래그 표)
- "avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM." ✅ verbatim
- `/debug-config` — 레이어를 **낮은 우선순위부터** 출력 / on-off 상태·정책 출처 / `allowed_approval_policies`·`allowed_sandbox_modes`·`mcp_servers`·`rules` 항목 / "Use this output to debug why an effective setting differs from `config.toml`." — `codex__developer-commands.md` L675-685 **전량 일치 ✅**

**인증 (소절 5) — 11항목 전량 일치 (`web-5.md` §7-11 = `/codex/auth`)**
- 로그인 계열 6종(`codex login` / `--with-api-key` / `--with-access-token` / `--device-auth`(beta) / `login status` / `logout`) ✅
- `~/.codex/auth.json` 평문 캐시 또는 OS 자격증명 저장소 ✅ / "비밀번호처럼 다뤄라 — 커밋·티켓·채팅 공유 금지" 원문 취지 일치 ✅
- `cli_auth_credentials_store` = `file`·`keyring`·`auto` ✅
- **"CLI와 IDE 확장은 같은 캐시를 공유한다. 한쪽에서 로그아웃하면 다른 쪽도 재로그인" ✅** — 원문 "The CLI and extension share the same cached login details…"와 정확히 대응
- device code 로그인이 **1순위 권장**이며 계정 보안 설정·워크스페이스 권한에서 먼저 켜야 함 ✅
- 폴백 2종(auth.json 복사 / 콜백 포트 터널링) ✅ / 포트 **1455** ✅ / `ssh -L 1455:localhost:1455 user@remote` ✅
- 환경 변수 3종 + `CODEX_CA_CERTIFICATE` 미설정 시 `SSL_CERT_FILE` 폴백 ✅
- API 키 로그인 제약 "Some features might not be available." ✅ (`web-1.md` L71)

**용어 정전 표 (표 2, 10행) — `01_reference.md` §1-5 대조**
- 10행 전부 §1-5와 대응 ✅. §1-5의 마지막 2행(Codex cloud / Chronicle·Computer Use·Appshots)을 1행으로 합쳐 계획이 요구한 **10행**을 맞춘 것은 정합 처리 ✅
- **Subagents 행에서 Claude Code 측 경로(`.claude/agents/*.md`)를 뺀 것은 옳은 판단이다.** §1-5 원문에는 그 경로가 있으나 FR-3 화이트리스트 취지상 **경로까지 주장하지 않는 쪽이 안전**하다. 이 처리를 이후 장에도 유지하라.
- `$skill` ↔ `/skill` 접두사 차이 ✅ / Hooks 부분 대응 ✅ / execpolicy `.rules` ↔ `permissions.allow/deny/ask` + Codex만 테스트 하네스 ✅ / `codex exec` ↔ `claude -p` ✅ — **전부 §1-5 안**

**클로징 체크리스트 5줄** — 소절 1의 5항목과 1:1 대응, 새 사실 추가 없음 ✅

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` 본문 L33 **1회**. 문언 그대로 준수 ✅ — 3개 장 중 유일하게 정확하다.
- **규율 6·7·11:** 위반 없음 ✅
- **규율 12:** Claude Code 주장이 표 2(§1-5 범위) 안으로만 한정됨 ✅

---

## 03장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/03_draft.md`(스타일 반영본) · 구체 주장 39건 추출

**집계: ✅ 35 / ❌ 0 / ⚠️ 4 / 🕒 0** (⚠️-1은 `(사실 확인 필요)` 마커 해소 항목 — **BLOCKING**)

> 이 장은 인용 15건·이슈 메타데이터 8행·명령 스펙 12건을 다루면서 **사실 오류 0건**이다. 특히 커뮤니티 인용의 진영·게시일 병기(규율 9)와 [#21753] "29+" 귀속(FR-3)이 전건 정확하다.

### ⚠️ 정정·약화 필요

#### ⚠️-1. `(사실 확인 필요)` 마커 해소 — "2모드 구분은 Codex 쪽 특징" (L187) — **BLOCKING**

- **원문:** "두 모드를 이렇게 이름·단축키·설정 키로 갈라 노출한 것은 Codex 쪽 특징이다 **(사실 확인 필요)**."
- **판정:** ⚠️ **출처 없음 — Claude Code 화이트리스트 안에서 판정 불가.** 마커를 지우고 그대로 두는 것은 허용되지 않는다.
- **화이트리스트 대조 결과:**
  - **§1-5(용어 대응 지도)** — Steering/Queuing 항목 **없음**
  - **§4-2(같은 이름 다른 동작 6행)** — `/clear`·되돌리기·중첩 지침·스킬 접두사·위험 플래그·훅 커버리지. **없음**
  - **§4-4(Claude Code에만 있는 것 6항목)** — `/rewind`·중첩 지침 자동 로드·Plan Mode 기본값·상태 표시줄·서브에이전트별 모델 지정·훅 완전 커버리지. **없음** (그리고 §4-4는 *Codex 결손* 목록이므로 애초에 "Claude Code에 X가 없다"의 근거가 될 수 없다)
  - 참고로 **§4-3(Codex에만 있는 것)에도 Steering/Queuing이 없다.** 즉 어느 쪽 목록에서도 이 주장을 끌어올 수 없다.
- **레퍼런스 §3-6의 취급:** `01_reference.md` L301에 "→ Claude Code에는 이 2모드 구분이 없다(실행 중 입력이 단일 동작으로 큐잉된다)"가 있다. 그러나 ⓐ 화이트리스트 밖이고 ⓑ 괄호 안은 Claude Code의 **구체 동작 주장**인데 이 책은 Claude Code 문서를 1차 수집하지 않았다. **이것이 정확히 규율 12·FR-3이 막으려는 종류의 문장이다.** 레퍼런스에 있다는 이유로 통과시키지 않는다.
- **웹 2차 에스컬레이션 판단:** 하지 않는다. 이 항목은 "의심 식별자"가 아니라 **경쟁 제품 동작 주장**이며, 웹으로 확인하더라도 이 책의 1차 소스 범위 밖에서 Claude Code 사실을 조달하는 선례가 되어 12개 장 전체에 같은 문을 연다. 규율 12가 봉인한 구조적 위험이 그것이다. **주장을 Codex 쪽 진술로 좁히는 것이 정답이다.**
- **수정안 (택1 — 필수 반영):**
  - **A안(권장 — Codex 진술로만 서술, 독자 감각은 그대로 살린다):**
    > 두 모드를 이름(Steer / Queue)과 단축키(<kbd>Enter</kbd> / <kbd>Tab</kbd>), 그리고 설정 키(`chatgpt.followUpQueueMode`)로 각각 갈라 노출한 것이 Codex의 방식이다. 익숙한 감각으로 <kbd>Enter</kbd>를 눌러 "그 파일은 건드리지 마"를 보냈는데 그게 다음 턴으로 미뤄진다면, …
  - **B안(규율 12의 안전 문형 적용):**
    > Codex는 실행 중에 보낸 메시지를 Steer와 Queue 두 갈래로 나누고, 갈래마다 이름·단축키·설정 키를 따로 준다. **실행 중에 그냥 <kbd>Enter</kbd>를 눌러오던 손이라면 여기서 갈린다.** 익숙한 감각으로 …
- **주의:** 이어지는 문장들("익숙한 감각으로 <kbd>Enter</kbd>를 눌러…", "첫날에 이 키 두 개부터 확인해두자")은 **수정 불필요**하다. 이미 Codex 쪽 동작만 말하고 있다.

#### ⚠️-2. "한국어 후기가 이 한 건뿐" (L107) — 인접 소절과 내부 모순으로 읽힌다

- **원문:** "한국어 후기가 이 한 건뿐이라는 사실도 그대로 적어둘 만하다."
- **문제:** 바로 다음 소절 도입부(L111)가 "국내에 실명과 소속을 밝힌 심층 비교가 **하나 있다** — Kyutae Park, AWS 한국 기술블로그, 2026-06-11"로 시작한다. 두 문장을 이어 읽으면 **한 건 → 또 하나 있음**으로 어긋난다.
- **원장 실황:** `community-2.md` L552 — "§8-3 — 한국어 전환 마찰 1차 후기 없음 | **1건 확보, 나머지 확정 부재** | §2-1(dcinside 코유키1357)이 유일. OKKY·회사 기술블로그·커리어리·요즘IT는 확인 결과 없음." 즉 "유일"인 것은 **전환 마찰을 다룬 한국어 1차 증언**이며, AWS 블로그는 **실행 스타일 심층 비교**라는 다른 범주다(`community.md` L393). 별개로 brunch(kk2daddy, 2026-03-14) 같은 한국어 글도 존재한다.
- **수정안:** "**전환 마찰**을 구체적으로 남긴 한국어 1차 증언이 이 한 건뿐이라는 사실도 그대로 적어둘 만하다."
  (뒤 문장 "전환 경험을 구체적으로 남긴 한국어 1차 자료는 놀랄 만큼 적었다"는 이미 정확하므로 유지)

#### ⚠️-3. "URL은 148개인데 고유 문서는 약 140개다" (L221) — 귀속 주체 불명

- **문제:** 앞뒤 문맥이 전부 공식 문서 서술이라, 독자가 이 수치를 **공식 문서가 밝힌 사실**로 읽을 수 있다. 실제로는 `01_reference.md` L779-780의 **이 책 리서치 집계**다("148 URL 배정 / 148 수집 성공 / 접근 실패 0건. 단, 148개 URL은 별칭 중복을 포함한다 — `/codex/cli/reference` ≡ `/codex/cli/slash-commands`처럼 바이트 단위로 같은 문서가 6쌍 있어, 고유 문서 수는 약 140개다").
- **수치 자체는 ✅** — 148 / 6쌍 / 약 140 / 바이트 단위 동일 문서 예시까지 전부 원장 일치.
- **수정안:** "이런 쌍이 여섯 개다. **이 책이 훑은 148개 URL 기준으로 고유 문서는 약 140개**다."

#### ⚠️-4. 오프닝 인용자의 행동 재구성 (L13)

- **원문:** "앞사람은 Claude Code를 쓰던 손으로 <kbd>Esc</kbd>를 두 번 눌렀다. 화면의 대화는 깔끔하게 되감겼다. 그래서 코드도 함께 돌아왔으리라 믿었다. **그리고 파일을 열어봤다. 수정은 그대로 남아 있었다.**"
- **판정:** ⚠️ 경미 — archneon의 댓글은 "i am used to Claude code"와 되돌리기 요구까지만 말한다. 파일을 열어봤다는 **행위 자체는 원문에 없다.** 규율 11(경험담 생성 금지)의 직접 위반은 아니다(실존 인물·출처·게시일이 있고 메커니즘은 이슈 본문의 재현 절차로 뒷받침된다). 다만 실명 인용자의 행동을 추가 서술하는 것은 같은 종류의 위험이다.
- **수정안(경미, 택1):** ⓐ "그리고 파일을 열어봤다" → "**그런데 이슈 본문의 재현 절차는 다른 결말을 적는다 — 파일 수정은 워킹 트리에 그대로 남는다.**" ⓑ 현행 유지하되 문단 끝에 근거를 명시. 저술가 재량 허용.

### ✅ 확인됨 (35건 — 근거 요약)

**오프닝 인용 2건 (`community.md` L20-23)**
- archneon, #11626, **2026-02-17** ✅ verbatim (문장 경계에서 절단, 의미 왜곡 없음)
- Alek2077, 같은 날 ✅ verbatim. **"그 스레드에서 반응이 가장 많이 붙은 답변"이라는 서술 정확** — 원장 "반응 77 — 스레드 최다"

**소절 1 — 사고 3종**
- `/clear` 원문 "Codex clears the terminal, resets the visible transcript, and starts a fresh chat in the same CLI session." — `codex__developer-commands.md` L554-555 ✅
- "Unlike <kbd>Ctrl</kbd>+<kbd>L</kbd>, `/clear` starts a new chat." / "<kbd>Ctrl</kbd>+<kbd>L</kbd> only clears the terminal view and keeps the current chat." — L559·L561-562 ✅
- "Unlike `/clear`, `/new` doesn't clear the current terminal view first." — L789 ✅
- `/compact` "Summarize the visible chat to free tokens." ✅
- **"작업이 진행 중일 때는 둘 다 비활성화된다" ✅** — "Codex disables both actions while a task is in progress."(L562)
- <kbd>Esc</kbd> 두 번 원문 "Press <kbd>Esc</kbd> twice with an empty composer to edit the previous user message and fork the chat from that point." — L349 ✅
- #11626 재현 절차 3단계 ✅ (`community.md` L19)
- suparious 인용 **2026-05-01** ✅ verbatim(생략 부호 정확), "커밋은 하되 푸시는 하지 마" 대응 ✅

**표 1 손버릇 교정표 6행 — 전행이 `01_reference.md` §4-2와 대응 ✅ (FR-3 완전 준수)**
- `/clear` / 되돌리기 / 중첩 지침 / 스킬 접두사(`/` vs `$`, ChatGPT 표면 `@`) / 위험 플래그 이름 / 훅 커버리지 — 6행 모두 §4-2 원문 범위 안
- **훅 "29+ 이벤트" 귀속이 정확하다 ✅** — "(이슈 [#21753]이 대조군으로 제시한 수치)"로 표기. FR-3의 명시 요구를 그대로 이행했다. 이 처리를 6장에도 유지하라.

**소절 2 — 중첩 `AGENTS.md` (`community.md` L33-40)**
- #12115 2026-02-18 개설 / 👍 **102** / open ✅
- **Wix(제출자 Andrew Ginns, 2026-05-05) · Stripe LLC(우선순위 `Must have`, 최근 근거 2026-07-13) ✅** — 이슈 메타데이터 4항목 전량 일치
- miraclebakelaser 인용(2026-02-18) ✅ verbatim, **"OpenAI 저장소에 `AGENTS.md`가 88개"** ✅
- anrooo(2026-05-15) ✅ verbatim / leonardo-panseri(2026-06-04) ✅ verbatim
- 코유키1357 dcinside 특이점갤 **2026-04-28 · 조회 7,507** ✅ (`community-2.md` L296) — 인용문 **글자 단위 일치**. 진영·게시일 병기로 **규율 9 준수 ✅**
- **V3 준수 확인 ✅** — AWS 한국 기술블로그를 이 소절에 인용하지 않았다. 계획이 가장 강하게 경계한 오귀속을 정확히 회피했다.
- 메커니즘(`project_doc_max_bytes` 등)을 4장으로 넘긴 M9 분담 준수 ✅

**표 2 전환 마찰 원장 8행 — 이슈 번호·개설일·👍·상태 **32개 셀 전량 일치** (`community.md` L444-464)**
| 이슈 | 개설일 | 👍 | 상태 | 판정 |
|---|---|---|---|---|
| #11626 | 2026-02-12 | 192 | open | ✅ |
| #28969 | 2026-06-18 | 186 | open | ✅ |
| #12115 | 2026-02-18 | 102 | open | ✅ |
| #28190 | 2026-06-14 | 79 | open | ✅ |
| #13942 | 2026-03-08 | 34 | open | ✅ |
| #19679 | 2026-04-26 | 31 | open | ✅ |
| #21753 | 2026-05-08 | 22 | open | ✅ |
| #24515 | 2026-05-26 | 0 | open | ✅ |
- "여덟 줄이 지금 전부 open" ✅ / 주 서술 장 배정이 계획 소절 3의 담당 배정과 완전 일치 ✅
- **🕒 신선도 처리 우수:** "표를 외우는 대신 번호를 열어보는 습관을 들이는 편이 낫다"(L138)·"원장에는 유효기간이 있다"(L229)로 휘발성을 **두 번 고지**했다. 별도 신선도 앵커 요구 없음.
- AWS 한국 기술블로그 도입 서술(L111) ✅ — 저자·소속·매체·날짜 4항목 정확, 7장 이관 명시로 V3 재배치 지시 이행

**소절 4 — 접두사·플래그**
- "ChatGPT supports `@` mentions, while Codex supports `$` mentions for skills." — `codex__skills-and-plugins.md` L39-40 ✅ verbatim
- "Type `@` to search for a file in the workspace and add its path to the prompt." — `codex__developer-commands.md` L342 ✅
- **"슬래시 팝업에는 활성화된 스킬이 함께 나타난다" ✅** — 원문 근거 확보: "Enabled skills also appear in the slash command list."(`codex__reference__slash-commands.md` L16)
- 위험 플래그 대조 표 3 ✅ §4-2 / `--yolo` 별칭 ✅
- 안전 권고 2인용 ✅ verbatim (`codex__developer-commands.md` 안전 권고절)
- **`--full-auto` deprecated ✅** — "Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used." 원문 일치

**소절 5 — Steering / Queuing (⚠️-1 제외 전량 ✅, `codex__prompting.md` L146-165)**
- Steer / Queue 정의 2인용 ✅ verbatim
- CLI <kbd>Enter</kbd>=steer / <kbd>Tab</kbd>=queue ✅
- **큐잉된 슬래시 명령의 지연 파싱 ✅** — "Codex parses queued slash commands when they run, so command menus and errors appear after the current turn finishes."(`codex__developer-commands.md` L376-378)
- 데스크톱 Settings > General > Follow-up behavior ✅ / 컴포저 위 스택·편집·재정렬·전송·삭제 ✅ / 1회 반전 단축키 표시 ✅
- **IDE `chatgpt.followUpQueueMode` 기본값 `queue` ✅** (`web-6.md` L2073)
- #28969: 2026-06-18 / 👍 **186** / open ✅, 재현 3단계 ✅, **60초** ✅
- ScyDev(2026-06-28) ✅ / gergo-hortobagyi(2026-06-24) ✅ / irm-codebase(2026-06-28) ✅ — 3건 전부 verbatim, 날짜 정확

**소절 6 — Codex 고유 조작 (`codex__developer-commands.md`)**
- `/fork` 새 ID 복제·원본 트랜스크립트 무손상 ✅(L818-820) / **`codex fork` 세션 선택기 ✅**(L822-823)
- `/side`(별칭 `/btw`) 임시 곁가지·부모와 분리된 트랜스크립트·부모 상태 계속 표시 ✅(L837-845) / **곁가지 안 중첩 불가 + 리뷰 모드 불가 ✅**(L847)
- `/goal` 문법 5종(`edit`·`pause`·`resume`·`clear`) ✅ / **최대 4,000자 + 초과 시 파일로 빼고 가리키라 ✅**(L499-500)
- **`/plan` → `/goal` 순서 ✅** — 원문 확보: "If the outcome is still unclear, start with `/plan`. … Then start the refined goal with `/goal`."(`codex__long-running-work.md` L69-71)
- `/raw` + <kbd>Alt</kbd>+<kbd>R</kbd> + `tui.raw_output_mode` ✅ / `/statusline` → `tui.status_line` ✅ / `/title` ✅ / `/theme` ✅
- `/personality` `friendly`·`pragmatic`·`none` + **미지원 모델에서는 명령 자체가 숨겨진다 ✅**("Codex hides this command", L477)
- `/keymap` → `config.toml` 저장 ✅ / `/vim` + `tui.vim_mode_default = true` ✅
- 전역 플래그 20 + 서브커맨드 28 + 슬래시 약 60 ✅ (1장과 동일 근거, 표기 일관 ✅)
- 별칭 6쌍·`/codex/cli/reference` ≡ `/codex/cli/slash-commands` 바이트 동일 ✅ (귀속은 ⚠️-3)

### 규율 준수 메모 (판정 아님)

- **규율 11(경험담 금지) — 오프닝 ✅.** "지어낸 새벽 3시"가 아니라 **인용된 실패**(#11626 댓글 2건)로 열었다. 계획의 가장 강한 요구를 정확히 이행했다.
- **규율 6:** 인용 금지 9건 미등장 ✅
- **규율 9:** 커뮤니티 인용 전건에 출처·게시일 병기 ✅ (dcinside는 갤러리명까지)
- **FR-2:** `(2026-08-02 문서 기준)`이 본문 L23 1회 + 표 1·표 2 캡션 2회 = **3회**. 표 2는 수치 표라 문언 부합, 표 1은 대조표다. 권고: 표 1 캡션에서 제거해 2회로. (비블로킹)
- **m3·m4 분담 준수 ✅:** 접두사는 이 장이 주 서술(6장은 콜백만), 고유 명령은 "있다는 사실과 문법"까지만 — "언제 쓰는가는 7장"을 명시(L211)

---

## 파(wave) 1 종합 — 오케스트레이터·저술가 통보

### BLOCKING 3건 (원고 확정 전 필수 해소)

| # | 장 | 항목 | 해소 방법 |
|---|---|---|---|
| 1 | 1장 | ❌-1 "changelog 항목 95개" | A안(여든 건 초과) 또는 B안(수치 제거) |
| 2 | 1장 | ❌-2 표 2 SDK 위치 `openai/codex/sdk` | `openai/codex/codex-sdk`로 교체 |
| 3 | 3장 | ⚠️-1 `(사실 확인 필요)` 마커 | A안/B안으로 문장 교체 — **마커만 지우는 것 불가** |

### 비블로킹 권고 5건

1장 ⚠️-3(그림 1 ↔ 본문 L63) · 2장 ⚠️-1(`CODEX_HOME` 조건절) · 3장 ⚠️-2(한국어 후기 한정) · 3장 ⚠️-3(148/140 귀속) · 3장 ⚠️-4(오프닝 재구성)

### 파 1 총계

| 장 | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|
| 1장 | 35 | 2 | 3 | 0 |
| 2장 | 38 | 0 | 1 | 0 |
| 3장 | 35 | 0 | 4 | 0 |
| **합계** | **108** | **2** | **8** | **0** |

**정확도 소견.** 원문 verbatim 대조 대상 47건 중 **불일치 1건**(1장 SDK 경로)뿐이다. 이 팀의 인용 규율은 매우 높다. 오류가 난 두 자리는 공통점이 있다 — **둘 다 "원문을 옮긴다"가 아니라 "집계·요약한다"에서 났다.** 인용은 정확한데 집계가 흔들린다. FR-9~FR-11이 이 패턴을 겨눈다.

---

# 파(wave) 2 — 4·5·6장

> 판정 기준: 파 1과 동일 + 누적 규율 **FR-1 ~ FR-14**.

## 04장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/04_draft.md`(스타일 반영본) · 구체 주장 38건 추출

**집계: ✅ 35 / ❌ 1 / ⚠️ 2 / 🕒 0**

### 저술가 명시 요청 판정

#### 판정 ①. `AGENTS.md` 정의 3구절 + "Many quality issues…" 인용의 근거 등급 — **✅ 확인됨 (tier 2 — 전사본 단독 근거, 사용 승인)**

- **저술가 관측이 정확하다.** `research/codex-docs-raw/guides__best-practices.md`는 **본문이 없는 404 페이지 캡처**다. 파일 안에 `<title>Page not found</title>`, `canonical href="https://developers.openai.com/404"`가 들어 있고 "Page not found" 문자열이 4회 등장한다. 이 파일로는 어떤 인용도 대조할 수 없다.
- **유일한 근거:** `research/web-6.md` **자료 5** (L1340-1382). 수집 비고가 명시돼 있다 — "URL: `https://learn.chatgpt.com/codex/learn/best-practices` (캐노니컬 `/guides/best-practices`) / 신뢰성 **최상**(공식 1차) / **`.md`가 404 → HTML을 pandoc 변환해 복원**".
- **왜 ✅로 통과시키는가 (3가지 근거):**
  1. **전사본의 실패 사유가 캐시 상태로 교차 검증된다.** 리서처가 "`.md` 404"라고 적었고, 실제 캐시 파일이 정확히 404 페이지다. 전사본의 자기 보고와 독립 증거가 일치한다 — 이건 신뢰를 **낮추는** 게 아니라 **높이는** 사실이다.
  2. **이 실패는 이 문서 집합에서 재현되는 알려진 패턴이다.** `/codex/changelog`도 `.md` 404였다(파 1에서 확인). 이례적 사건이 아니다.
  3. **부분 교차 확인이 있다.** 3구절 중 2개가 `01_reference.md` §1-4 L61·L63에 독립적으로 실려 있다.
- **의심 식별자 규칙 비해당.** URL 형식 정상, 미래 날짜 없음, 검증 불가 식별자 아님. 웹 2차 에스컬레이션 대상이 아니다.
- **인용 4건 문자 단위 대조 — 전량 일치 ✅**
  - "Think of `AGENTS.md` as an open-format README for agents." (web-6 L1372)
  - "Keep it practical. A short, accurate `AGENTS.md` is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes." (L1374)
  - "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`." (L1376)
  - "Many quality issues are really setup issues, like the wrong working directory, missing write access, wrong model defaults, or missing tools and connectors." (L1380)
- **후속 규율:** 원문 캐시가 404인 페이지는 이 책에 최소 2개다. 이후 장이 같은 판정을 반복하지 않도록 **FR-15**로 목록화한다.

#### 판정 ②. "설정 키가 270개가 넘는다" 하한 서술 — **✅ 확인됨. FR-9의 모범 적용이다.**

- **직접 카운트 결과:** `research/codex-docs-raw/_config-reference-tables.md`에서 표 행을 직접 셌다.
  - `config.toml` 설정 키: **274행** (L2 헤더 라벨 "274개"와 **일치**)
  - `requirements.toml` 설정 키: **116행** (L281 헤더 라벨 "116개"와 **일치**)
- 파 1의 changelog 사례와 달리 **라벨과 실측이 어긋나지 않는다.** `web-2.md` L1789가 복원 검증까지 기록했다("자리표시자 2개 = 복원 표 2개, 인라인 항목 390개 = 표 행 390개, 1:1 검증 완료").
- 그럼에도 초안이 **"270개가 넘고"라는 하한**을 택한 것은 FR-9가 요구한 그대로다. 274가 확정 가능한 상황이므로 "274개"라 써도 통과했겠지만, **하한 서술은 스냅샷이 바뀌어도 계속 참이라는 추가 이점**이 있다. 유지 권장.
- `requirements.toml` **116개**는 정확 수치로 썼는데 이 역시 실측 일치 ✅.

#### 판정 ③. 6단계 우선순위 표 + 미신뢰 프로젝트 `.codex/` 스킵 — **✅ 확인됨 (전 셀 일치)**

- **표 1의 6행이 원문과 1:1 일치한다.** 근거 `research/codex-docs-raw/codex__config-file__config-basic.md` L21-28 "Codex resolves values in this order (highest precedence first)". 순위·층·위치가 전부 대응하고, 2번 행 괄호의 **"closest wins; trusted projects only"**까지 옮겨져 있다.
- **미신뢰 스킵 서술이 원문 문장과 정확히 대응한다.** L32 verbatim: "If you mark a project as untrusted, Codex skips project-scoped `.codex/` layers, **including project-local config, hooks, and rules.** User and system config still load, including user/global hooks and rules."
  - 초안 L113의 세 문장("층이 통째로 건너뛰어진다" / "설정과 함께 훅과 규칙까지 빠진다" / "사용자·시스템 층은 그대로 로드되므로 Codex 자체는 멀쩡히 돌아가고")이 원문의 세 요소를 빠짐없이 옮겼다 ✅
- 보너스: 11장 예고(L154)의 `requirements.toml` 금지 예시 두 개(`approval_policy = "never"`·`sandbox_mode = "danger-full-access"`)도 같은 페이지 L36-40 원문과 일치 ✅

### ❌ 정정 필요 (BLOCKING)

#### ❌-1. "문서는 갱신 시점을 **네 가지**로 구체화한다" (L27)

- **판정:** ❌ — 원문의 항목 수는 **다섯**이다. 개수를 문서에 귀속했으므로 수치 오류다.
- **근거:** `research/codex-docs-raw/codex__customization__overview.md` L36-41, `### When to update AGENTS.md` 아래 불릿 **5개**:
  `Repeated mistakes` / `Too much reading` / `Recurring PR feedback` / **`In GitHub`**(PR 코멘트에서 `@codex`에 갱신을 위임) / `Automate drift checks`
- 초안이 옮긴 네 항목의 **내용은 전부 정확하다.** 빠진 것은 `In GitHub` 하나뿐이다.
- **수정안 (택1):**
  - **A안(권장 — 개수 귀속을 뺀다):** "문서는 갱신 시점을 **여러 갈래로** 구체화한다."
  - **B안(다섯째를 넣는다):** "…그리고 예약 작업으로 지침 공백을 주기적으로 점검하고 싶을 때. 여기에 하나가 더 붙는다 — **GitHub 풀 리퀘스트 코멘트에서 `@codex`에게 갱신 자체를 맡기는 경로**다."
- 이 오류는 파 1의 ❌-1(changelog 95개)과 **같은 계열**이다. 인용은 정확한데 **세는 순간 틀린다.** FR-9를 저술가 자신의 카운트에도 적용하도록 FR-16으로 확장한다.

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. 32 KiB 인용의 중간 생략에 생략 부호가 없다 (L41)

- **초안:** "Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default). Raise the limit or split instructions across nested directories when you hit the cap."
- **원문**(`codex__agent-configuration__agents-md.md` L15)에는 두 문장 **사이에** 한 문장이 더 있다 — "For details on these knobs, see [Project instructions discovery](…)."
- 생략된 것은 내비게이션 문장이라 **의미 왜곡은 없다.** 다만 파 1에서 통과시킨 것은 *끝을 자르는* 절단이었고, 이건 *가운데를 빼는* 생략이라 기준이 다르다.
- **수정안:** 두 문장 사이에 `…`를 넣는다. (또는 두 문장을 각각 별도 인용으로 분리)

#### ⚠️-2. 표 3의 `[desktop]` 표기가 실제 범위보다 넓게 읽힌다 (L180)

- **초안 셀:** 데스크톱 앱 설정 위치 = "앱 Settings UI + `~/.codex/config.toml`의 `[desktop]`"
- **실측:** `[desktop]` 테이블은 실재하지만 **키가 7개뿐이고 전부 `desktop.custom_file_handlers.*`**(`_config-reference-tables.md` L207-213), 용도는 **Open in 메뉴에 외부 편집기를 추가하는 것** 하나다. "user-level only"라고 원문에 명시돼 있다.
- 셀이 "앱 Settings UI **+**"로 시작하므로 배타 주장은 아니지만, 독자가 데스크톱 설정을 `config.toml`에서 찾으러 갈 여지가 있다.
- **수정안:** "앱 Settings UI (+ `[desktop]`은 **Open in 커스텀 파일 핸들러 전용**)"

### ✅ 확인됨 (35건 — 근거 요약)

**`AGENTS.md` 탐색·병합 — `codex__agent-configuration__agents-md.md` 전건 일치**
- 3단계 발견 순서(전역 / 프로젝트 / 병합) — L11-13과 **문장 단위로 대응** ✅. "이 층에서는 비어 있지 않은 첫 파일 하나만"·"디렉터리당 최대 한 파일"·"빈 줄로 잇는다"·"가까운 파일이 뒤에 놓이므로 앞의 지침을 덮는다" 전부 원문 ✅
- **"Codex stops searching once it reaches your current directory." ✅ verbatim** (L83) — 3장 현상의 메커니즘 규명으로 정확
- `AGENTS.override.md` 동작 ✅ — 같은 디렉터리의 `AGENTS.md`가 무시된다는 서술은 원문 FileTree 주석 "Ignored because an override exists"(L105)가 근거. `services/payments/` 예시 ✅ L64-73
- 전역 층 용법(기본 파일 안 지우고 임시 교체, 지우면 복귀) ✅ L47
- 트러블슈팅 순서 ✅ L210-214 — "상위 디렉터리와 Codex 홈의 override를 먼저 찾고 이름을 바꾸거나 지운다"(L211) / `codex status` 워크스페이스 루트 확인 + 빈 파일 무시(L210) / `echo $CODEX_HOME`(L214) **3항목 전부 원문**
- 검증 명령 2종 ✅ — `codex --cd services/payments --ask-for-approval never "List the instruction sources you loaded."`(L78)와 **기대 결과**(전역 → 저장소 루트 → 해당 디렉터리 override, L81) / `codex -c log_dir=./.codex-log`(L205)
- 클로징 과제 명령 `codex --ask-for-approval never "Summarize the current instructions."` ✅ L42·L203
- 캐시 없음 — "Codex rebuilds the instruction chain on every run (and at the start of each TUI session), so there is no cache to clear manually." ✅ L206
- 32 KiB 예산: 빈 파일 skip / **결합 크기** 기준 / 한도 도달 시 중단 ✅ L15 (인용 형식은 ⚠️-1)
- `project_doc_fallback_filenames` ✅ — 예시 값 `["TEAM_GUIDE.md", ".agents.md"]`이 원문 예시와 동일(L153), 탐색 순서 `AGENTS.override.md` → `AGENTS.md` → `TEAM_GUIDE.md` → `.agents.md` ✅ L159, **"Filenames not on this list are ignored for instruction discovery." ✅ verbatim**
- `project_doc_max_bytes = 65536` 예시 ✅ L154 (원문 예시와 동일 값)
- `## Code Review Rules` 섹션 ✅ L124-143 — "루트 vs 코드에 가장 가까운 파일" 배치, "짧게 / 지적 대상과 안전한 우회로 / 포매팅·린트는 CI" 3권고 전부 원문
- `/init` 스캐폴드 ✅ (`codex__developer-commands.md` L849-855). **초안이 Claude Code를 이름으로 부르지 않고 "이름도 역할도 손에 익은 그대로다"로 처리한 것은 FR-12의 안전 문형 그대로다 — 모범 사례로 기록**

**커스터마이즈 층 — `codex__customization__overview.md`**
- 5층(지침·메모리·스킬·MCP·서브에이전트) ✅ L7-13 / **"These are complementary, not competing." ✅ verbatim** L15 / 층별 역할 4구 ✅ L15-17
- 저장소 파일 항목 예시 4개 ✅ L26-29 — "Build and test commands / Review expectations / repo-specific conventions / **Directory-specific instructions**" → 초안의 "빌드·테스트 명령, 리뷰 기대치, 저장소 고유 관례, 디렉터리별 지시사항"과 **4개 전부 대응**
- 전역/저장소 역할 분리(전역=소통 방식·리뷰 스타일·상세함·개인 기본값) ✅ L45 verbatim
- "피드백 루프의 저장소" ✅ — "Treat it as a feedback loop."(L30)

**설정 — `config-basic` / `config-advanced` / `config-reference`**
- 공식 JSON 스키마 URL `https://learn.chatgpt.com/docs/config-schema.json` ✅ `codex__config-file__config-reference.md` L1609
- 3계층 운용 권고(개인 `~/.codex/config.toml` / 저장소 `.codex/config.toml` / 일회성 명령줄) ✅ web-6 L1417-1419 원문 목록
- `--profile` = `~/.codex/profile-name.config.toml` 적층 ✅ `config-advanced` L32-35. 예시 `codex --profile deep-review`는 **원문 예시와 동일** ✅
- `-c`/`--config`는 TOML 파싱 → 문자열에 따옴표 한 겹 더 ✅ L64-66 + 원문 예시 `codex --config model='"gpt-5.6-terra"'`와 동형. `model_reasoning_effort='"high"'`의 `high`도 정전 값 목록 안 ✅ (`minimal|low|medium|high|xhigh`, `_config-reference-tables.md` L171 — **FR-6 정전 페이지 준수**)
- `--strict-config` ✅ `codex__developer-settings.md` L89-90 — "기본은 무시, 플래그를 주면 오류로 처리"가 원문 그대로
- 표 2 `[features]` 5행 ✅ 전부 원문 표(web-2 L372-386)와 일치. 캡션의 **"원문 표의 일부"** 표기가 정직하다(원문 14행) ✅
- `codex --enable feature_name` ✅

**진단 — `/status` vs `/debug-config`**
- `/status`: 활성 모델·승인 정책·쓰기 가능 루트·토큰 사용량 ✅ `codex__developer-settings.md` L85-86
- `/debug-config`: 낮은 우선순위부터 나열 / on-off / 정책 출처 / `allowed_approval_policies`·`allowed_sandbox_modes`·`mcp_servers`·`rules` + 설정 시 `enforce_residency`·`experimental_network` ✅ `codex__developer-commands.md` L675-685 전건
- 용도 한 줄 ✅ "Use this output to debug why an effective setting differs from `config.toml`."

**개인화 3층**
- 성격 Friendly·Pragmatic·None ✅ `codex__personalize.md` L11
- ⭐ **"개인 지침은 전역 `AGENTS.md`에 저장된다" ✅ verbatim** — "In Codex, these personal instructions are stored in your global `AGENTS.md` file."(L17-19). 이 장의 가장 값어치 있는 발견이고 근거가 정확하다
- 메모리 저장소 분리 ✅ — "ChatGPT web uses ChatGPT memory, while local Codex clients use a separate local…"(`codex__customization__memories.md` L7) / `/memories`가 "쓸지 · 재료가 될지"를 각각 제어 ✅ L20-21
- Chronicle 조건·경고 ✅ — opt-in research preview / ChatGPT Pro macOS 한정 / Screen Recording·Accessibility 권한 / **위험 3종(사용량 한도 빨리 소모 · 프롬프트 인젝션 위험 증가 · 기기에 암호화하지 않고 저장)** — `codex__customization__chronicle.md` L5-17과 **3개 전부 일치**
- **"Keep required team guidance in `AGENTS.md` or checked-in documentation. Treat memories as a helpful recall layer, not as the only source for rules that must always apply." ✅ verbatim** (`memories.md` L12-14)

**표 3 표면별 지형도**
- ⭐ **"CLI와 IDE 확장은 같은 설정 층을 공유한다" ✅** — 원문 근거 확보: "Codex settings control agent behavior **shared with Codex CLI**, including the model, reasoning effort, permissions, sandbox, MCP servers, and personalization. **Codex reads these settings from `config.toml`.**"(web-6 L2060)
- IDE 진입 경로(기어 아이콘 > Codex Settings > Open config.toml) ✅ web-6 L2084
- Windows `[windows] sandbox = "elevated"` / `"unelevated"` ✅ `codex__windows__windows-sandbox.md` L54-55, 권장·폴백 관계 ✅ L69-71 ("If both modes are available, use `elevated`."), 초안 L191의 "관리자 권한이 없거나 elevated 설정이 실패할 때"도 원문 취지 일치
- WSL은 리눅스 환경 선호자를 위한 선택지로 잔존 ✅ (1장과 동일 근거, 표기 일관)
- **규율 7 준수 ✅ — WSL 경로 성능 권고가 등장하지 않는다.** 확정 불가 항목을 정확히 회피했다

**커뮤니티·이슈**
- [#13386] 2026-03-03 / 👍 11 / open ✅ (`community.md` L41). **등급 처리가 정확하다** — "익명 보고자의 커뮤니티 관측이고, 공식 문서가 '경고 없이 자른다'고 인정한 것은 아니다"(L47)는 원장 등급 `[익명 주장·확인 필요]`와 정확히 대응. 문서가 인정하는 범위(잘림 + 대처법)를 따로 그은 것도 정확 ✅ (트러블슈팅 L213)
- [#28903] 2026-06-18 / open ✅ (`community.md` L42) — 제목·방향(저장소 루트 **위쪽** 조상 미로드) 정확
- steve-atx-7600 HN **2026-07-09** ✅ (`community.md` L369-370) 인용 verbatim, 문장 경계에서 시작. **등급 병기 ✅**("익명 사용자의 개인 운용법이고 공식 문서가 보증하는 구성은 아니다") — 규율 9 준수

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` 본문 L47 1회 + 표 1·2 캡션 2회. 표 1·2 모두 수치·목록 표라 문언 부합 ✅
- **FR-3 / 규율 12:** Claude Code 고유명 언급 **0회**. `/init`·`CLAUDE.md`가 등장하는 자리 전부 인용문 안이거나 §1-5 범위. **파 1·2 통틀어 가장 깨끗하다** ✅
- **규율 6·7·11:** 위반 없음 ✅ (경험담 0건, WSL 성능 권고 0건, 인용 금지 9건 0건)

---

## 05장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/05_draft.md`(스타일 반영본) · 구체 주장 44건 추출

**집계: ✅ 43 / ❌ 0 / ⚠️ 1 / 🕒 0**

> **이 책에서 지금까지 가장 정확한 장이다.** 원문 인용 26건이 전량 verbatim 일치했고, 저술가가 미리 지목한 위험 지점 7곳이 **전부 정확하게 처리돼 있었다.** 아래 명시 요청 판정은 그 확인 기록이다.

### 저술가 명시 요청 판정 (7건 — 전건 ✅)

#### ① destructive action avoidance 수치 + 벤더 자체 보고 명시 — **✅**
- 네 값 `0.66`(gpt-5-codex) / `0.70`(gpt-5.1-codex) / `0.75`(gpt-5.1-codex-max) / `0.76`(gpt-5.2-codex) — `research/papers.md` §4-5 Table 4 (L273-278)와 **모델명·값 전부 일치** ✅
- 출처 표기 "GPT-5.2-Codex 시스템 카드 애드덤(2025-12-18)" ✅ (papers.md L259)
- **"이 수치는 벤더 자체 보고이므로 그 점을 감안해 읽어야 한다"(L285) ✅** — papers.md L261의 요구("peer-review 대상 아님 — **벤더 자체 보고**임을 명시할 것")를 명시적으로 이행
- 인용문 verbatim ✅ ("Simple instructions like 'clean the folder' or 'reset the branch' can mask dangerous operations (rm -rf, git clean -xfd, git reset –hard, push –force)…")
- ⭐ **"이 애드덤에는 프롬프트 인젝션 정량 평가표가 없다. …출처를 의심하자"(L285) ✅** — papers.md L282의 ⚠️ 경고("책에서 'OpenAI가 인젝션 방어율 N%를 보고했다'고 쓰면 **거짓이 된다**")를 회피하는 데 그치지 않고 **독자에게 그 함정을 넘겨준** 처리다. 계획 5장 소절 7의 요구를 초과 이행

#### ② IssueTrojanBench 66.5% 조건 병기 — **✅ (단정 표현 1건만 ⚠️-1로 분리)**
- Singh, Yang, Chen / arXiv:2607.20759 / 2026-07-22 / 66.5% ✅ (papers.md §4-4 L246-256)
- **식별자 점검:** `2607.20759`의 YYMM=2607(2026년 7월)은 빌드 시점 2026-08-02 기준 **과거**다. 자동 ❌ 규칙(미래 YYMM) 비해당, 형식 정상 ✅
- 인용 "rejection is almost entirely from LLMs rather than the agent frameworks" ✅ verbatim (abstract)
- **조건 병기 3중 이행 ✅** — ⓐ "이 벤치마크가 설계한 공격 시나리오 집합 기준이며 실사용 환경의 침해율이 아니다" ⓑ "아직 동료 심사를 거치지 않은 preprint" ⓒ 인용 가치의 근거 명시. papers.md L256이 요구한 것("**'이 벤치마크가 설계한 공격 시나리오 기준'임을 반드시 함께 적어라**")을 그대로 이행

#### ③ miki123211 HN 인용 — 게시일·등급 병기 — **✅**
- 2026-07-14 ✅ / HN ✅ (`community.md` L197-198) / 인용 verbatim + 생략 부호 ✅
- **등급 병기 ✅** — "개인 후기이므로 공식 권고와 같은 무게로 읽을 것은 아니지만, 방향은 문서와 정확히 같다"(L297). 원장 등급 `[익명·확인 필요]`와 대응하면서, 뒤이어 **공식 문서 인용 2건**(`--add-dir` 우선 / 규칙 사용)으로 같은 방향을 뒷받침한 구성이 정확하다. 규율 9 준수 ✅

#### ④ 서킷 브레이커 문안 — **✅ (가장 자주 틀리는 자리를 정확히 지켰다)**
- 원문 verbatim ✅ — "Auto-review interrupts the turn after `3` consecutive denials or `10` denials within a rolling window of the last `50` reviews in the same turn."(web-4.md L443)
- ⭐ **"뒤 조건을 '턴당 10회'로만 옮기면 틀린 서술이 된다. 창 크기 50이 함께 있어야 조건이 성립한다"(L226)** — 오독 지점을 **독자에게 명시적으로 경고**했다. 계획 5장 소절 5의 요구("50건 창을 빼먹으면 틀린 서술")를 이행
- 부속 사실도 전건 일치 ✅ — 비-거부 시 연속 카운터 초기화 / 경고 후 턴 중단(web-4 L445) / `/approve` 피커·**작업당 최대 10건 기록**·좁은 승인·**재시도도 Auto-review 재통과**(L450)

#### ⑤ `--yolo` → `web_search` live 함정 — **✅ (원문 캐시로 직접 확인)**
- 인용 verbatim ✅ 그리고 **원문 캐시에 독립 근거가 있다** — `_config-reference-tables.md` L247의 `web_search` 항목: "(default: `"cached"`; …; **if you use `--yolo` or another full access sandbox setting, it defaults to `"live"`**)"
- `web_search` 4값 `cached`(기본)·`live`·`disabled`·`indexed` ✅ 같은 행
- 초안이 이를 "문서에 적히지 않은 부작용"이라 부른 것(L149)은 **표 2에 안 적힌**이라는 뜻으로 읽히고 뒤에 원문을 인용하므로 오도 없음 ✅

#### ⑥ WSL `0.114`/`0.115` 버전 앵커 — **✅ (원문 캐시 직접 확인)**
- `codex__agent-approvals-security.md` **L320** verbatim: "WSL1 was supported through Codex `0.114`; starting in `0.115`, the Linux sandbox moved to `bwrap`, so WSL1 is no longer supported." ✅
- 권한 프로필의 `0.138.0` 앵커도 별도 확인 ✅ (web-4 L177 원문)

#### ⑦ 표 1 마지막 열 — 빈칸을 "판정하지 않음"으로 처리 — **✅ 이 책의 모범 처리로 기록한다**
- 3축 중 `sandbox_mode`·`approval_policy` 두 행만 대응을 적었고, 그 둘은 각각 **§4-2(위험 플래그 이름)**·**§1-5(execpolicy `.rules` ↔ `permissions.allow/deny/ask`)** 안에 정확히 들어간다 ✅ FR-3 준수
- `approvals_reviewer`와 granular 5토글은 "대응 항목이 레퍼런스에 없다 — 이 책은 판정하지 않는다"로 비워뒀다 ✅
- ⭐ **L98의 해명 문단이 이 처리의 핵심이다** — "빈칸이 말하는 것은 '이 책이 근거를 갖고 말할 수 없다'는 사실 하나뿐이다. **대응물이 실제로 있는지 없는지는 별개의 문제**이고, 그 자리는 당신이 직접 쓰는 도구를 열어 채우는 편이 정확하다."
  이것은 **FR-12가 요구한 것보다 한 걸음 더 나간 처리**다. FR-12는 "목록의 부재는 사실의 부재가 아니다"를 fact-checker의 판정 규칙으로 세웠는데, 이 문단은 그 구분을 **독자에게 직접 설명**한다. 이후 장에서 화이트리스트 공백을 만나면 이 문단의 방식을 재사용하라 → **FR-17로 승격**

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. "…최신 벤치마크가 이것뿐이기 때문이다" (L291) — 단정의 범위가 넓다

- **문제:** 같은 원장에 다른 벤치마크가 있다. `papers.md` §1-7 **Terminal-Bench 2.0**(ICLR 2026, ✅ peer-reviewed, arXiv:2601.11868)은 "**Claude Code, Codex CLI**, OpenHands, Mini-SWE-Agent를 공식 지원"하며, 원장은 그쪽에 "Codex CLI가 실제로 평가 대상인 **유일한** 주요 학술 벤치마크"라는 라벨을 따로 붙여뒀다. 두 "유일" 라벨이 원장 안에 공존한다.
- **엄밀히는 초안이 옳다** — IssueTrojanBench는 *Codex **Desktop***을 *악의적 이슈 방어* 관점에서 평가했고, Terminal-Bench는 *Codex **CLI***를 *역량* 관점에서 평가했다. 겹치지 않는다.
- 그러나 초안 문장에는 그 구분어가 없어서, Terminal-Bench를 아는 독자에게는 반박 가능한 단정으로 읽힌다.
- **수정안(한 단어):** "…이름으로 직접 평가한 **보안** 벤치마크가 이것뿐이기 때문이다."
- 8장이 Terminal-Bench를 꺼낼 예정이라면 이 구분어가 **더 필요해진다**(같은 책 안에서 두 "유일"이 충돌하는 것처럼 읽힌다).

### ✅ 확인됨 (43건 — 근거 요약)

**분리 명제 — 세 문서의 반복 (전량 verbatim)**
- `codex__permission-modes.md` L38-45: "The **sandbox** defines which files and network resources ChatGPT can access." / "**Approvals** determine when ChatGPT pauses before an action or sends the request to automatic review." / "Changing who reviews a request doesn't expand the sandbox. For example, **Approve for me** keeps the same workspace boundary as **Ask for approval**; it sends requests to cross that boundary to automatic review." ✅ 3건
- web-4 L320·L322·L325·L327: "Sandboxing and approvals are different controls that work together…" / "The sandbox applies to spawned commands, not just to built-in file operations…" / "The sandbox reduces approval fatigue…" / "**You aren't just trusting the agent's intentions; you are trusting that the agent is operating inside enforced limits.**" ✅ 4건
- `codex__agent-approvals-security.md` 2정의(Sandbox mode / Approval policy) ✅
- 초안 L47의 관찰("세 개의 문서가 같은 분리를 세 번 되풀이한다")은 실제 대조 결과와 정확히 일치 ✅

**3축 + granular**
- 세 축의 값 정의 9건 전부 원문(web-4 L329-341) ✅. `approvals_reviewer`에 붙은 조건절("When approvals are interactive…")까지 옮겼다 ✅
- granular 인용 verbatim ✅ — 원문 캐시에도 독립 확인(`codex__agent-approvals-security.md` L195). 5범주 ↔ 5토글 대응 ✅
- 프리셋 인용 verbatim ✅ (web-4 L347) / "Full access 라벨 하나가 두 축을 동시에 끝까지 민 상태"라는 해석도 인용문에서 직접 따라온다 ✅
- 기본값 ✅ — 버전 관리 폴더 `Auto`(workspace write + on-request) / 비버전 폴더 `read-only` / 명시적 신뢰 전까지 `read-only` 시작 가능 / 워크스페이스 = 현재 디렉터리 + `/tmp` 같은 임시 디렉터리 / `/status`로 확인 — `codex__agent-approvals-security.md` L166-170 **5항목 전건**

**세 층 · 표면별 노출**
- 3종 소개 + Ask for approval은 항상 사용 가능 + Approve for me(설정에서 **Auto-review**로 표기)·Full access는 켜야 노출 ✅ `permission-modes.md` L23-28
- **"Enabling a mode makes it available in the menu; it doesn't select the mode or change an existing chat." ✅ verbatim**
- 데스크톱·IDE 메뉴 확장 인용 ✅ (web-4 L352) / CLI `/permissions` ✅ / **"ChatGPT web doesn't expose the local Codex sandbox or approval-mode selector." ✅ verbatim**
- "권한 모드는 N가지다라고 외우면 어느 쪽이든 틀린다"(L122) ✅ — FR-6의 "표면별 병기" 지시 이행
- 표 2 의도별 조합 **6행 전부 원문 표와 일치** ✅ (web-4 L598-604). 캡션의 "플래그·설정 열은 원문 표기, 결과 열은 우리말로 풀었다"가 정직 ✅
- `untrusted` 상세 인용 verbatim ✅ (L143)
- `codex exec --sandbox workspace-write` 권장 + `codex exec --full-auto`는 deprecated 호환 경로 + 경고 출력 ✅ (web-4 L606)

**권한 프로필 (FR-8 준수)**
- 정의 인용 ✅ / 경로별 `read`·`write`·`deny` + 도메인별 `allow`·`deny` ✅ / 우선순위(구체 > 광범위, 같은 경로면 deny > write > read) ✅
- **"Beta. Permission profiles are under active development and may change." ✅ verbatim**
- ⭐ **폴백 규칙 인용 verbatim ✅** — "…**If `sandbox_mode` appears in any loaded config file, you pass `--sandbox`, or the selected config profile sets `sandbox_mode`**, Codex uses those older sandbox settings instead of `default_permissions`." 초안이 세 조건을 하나씩 풀어 쓴 것(L173)까지 정확
- 예외 `allowed_permission_profiles` + **Codex `0.138.0` 이상** ✅ verbatim
- 내장 3종 `:read-only`·`:workspace`·`:danger-full-access` 정의 ✅ verbatim / `extends` 제약("It cannot extend `:danger-full-access`; Codex also rejects unknown parents and inheritance cycles.") ✅ verbatim / `:workspace` 확장 시 워크스페이스 루트의 `.codex`가 읽기 전용으로 남는 보호 승계 ✅
- **FR-8 완전 준수** — "기본 경로는 여전히 구 체계이고, 권한 프로필은 그 옆에서 Beta로 병행한다"(L167)가 FR-8이 요구한 논지 문안 그대로 ✅. 그림 2의 폴백 결정 흐름도 원문 조건과 1:1 ✅

**Auto-review**
- 정의 인용 ✅ / **"Auto-review is a reviewer swap, not a permission grant. It does not expand `writable_roots`, enable network access, or weaken protected paths." ✅ verbatim**
- 5단계 작동 순서 ✅ / 리뷰어 입력 범위(압축된 대화 기록·정확한 승인 요청·사용자 메시지·표면화된 어시스턴트 업데이트·관련 도구 호출과 출력) ✅
- **"Hidden assistant reasoning is not included. Auto-review sees retained chat items and tool evidence, not private chain-of-thought." ✅ verbatim**
- "Auto-review works best when the sandbox already covers your common safe workflows…" ✅ verbatim / 좁은 접두사 권고(`["cargo","test"]` vs `["python"]`) ✅
- **"…but it is not a deterministic security guarantee." ✅ verbatim** — 제품 문서의 자기 한계 고지를 그대로 옮겼고, 마지막 소절 논지로 이어진 구성이 정확 ✅

**OS 강제 층**
- macOS Seatbelt + `sandbox-exec` + 모드 대응 프로파일(`-p`) ✅ / Linux `bwrap` + `seccomp` 기본 ✅ / Windows 네이티브 or WSL2 ✅ — `codex__agent-approvals-security.md` L316-320 전건
- `bubblewrap` 준비물 ✅ — `PATH`에서 처음 찾은 `bwrap` 사용, 없으면 번들 헬퍼 폴백(비특권 사용자 네임스페이스 필요) ✅ (web-4 L369) / `sudo apt install bubblewrap`·`sudo dnf install bubblewrap` ✅ / **Ubuntu 25.04는 추가 설정 불필요, 24.04는 경고 지속 가능** ✅ (web-4 L372-374) — 버전을 뭉개지 않은 처리
- 컨테이너에서 네임스페이스·`seccomp` 차단 시 미동작 ✅
- ⭐ `codex sandbox macos|linux|windows` 3종 + `--permissions-profile`·`--log-denials`(macOS)·`[COMMAND]...` ✅ **원문 코드 블록과 문자 단위 일치**(`codex__agent-approvals-security.md` L301-308) / `codex debug` 별칭 + `codex sandbox seatbelt`·`landlock` ✅ L312
- 보호 경로 4항목 ✅ **verbatim**(L179-184) + `gitdir:` 포인터 파일의 실제 Git 디렉터리까지 보호 ✅
- 네트워크 2단 게이트 진리표 3행 ✅ (web-4 L524-526) / 로컬 기본 차단 + `sandbox_workspace_write.network_access` + `features.network_proxy` 도메인 단위 ✅ / 클라우드는 9장 이관 ✅

**잔여 위험 소절**
- **"Destructive app/MCP tool calls always require approval when the tool advertises a destructive annotation, even if it also advertises other hints (for example, read-only hints)." ✅ verbatim** — 원문 캐시에도 독립 확인
- 초안 L311의 뒤집기("표시하지 않는 도구는 이 그물에 걸리지 않는다")는 인용문의 논리적 대우이며 원문을 넘어서지 않는다 ✅
- "When a workflow needs a specific exception, use rules…" ✅ verbatim / "…choose the narrowest scope that lets the task continue. Keep the project boundary as the default; use separate projects or worktrees…" ✅ verbatim
- `--add-dir` 우선 권고 ✅ (3장·`developer-commands` 안전 권고와 동일 근거, 표기 일관)

**클로징 스키마 블록**
- 5개 키의 값·기본값이 전부 위 근거와 일치 ✅ — `sandbox_mode`/`network_access = false`/`approval_policy`/granular 5토글/`approvals_reviewer = "user"`/`web_search = "cached"` + `--yolo` 주석

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` L167 **1회**. 문언 그대로 준수 ✅ (2장과 함께 가장 정확)
- **FR-3 / 규율 12:** Claude Code 주장이 표 1의 두 행(§4-2·§1-5 범위)뿐 ✅
- **규율 2·3:** 권한 프로필 Beta 처리 ✅ / **승인 축 3개 기준으로 대응표 작성 ✅** — 계획 규율 3이 "2축으로 뭉개면 5장 전체가 틀린다"고 경고한 지점을 정확히 통과
- **규율 6·7·11:** 위반 없음 ✅

---

## 06장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/06_draft.md`(스타일 반영본) · 구체 주장 41건 추출

**집계: ✅ 37 / ❌ 2 / ⚠️ 2 / 🕒 0**

### 저술가 명시 요청 판정 (5건)

#### ① 접미사 없는 `gpt-5.6` 원문 표기 인용 (FR-7) — **✅ 완전 준수**
- 인용 3구 전부 원문 캐시와 **문자 단위 일치** ✅ — `codex__agent-configuration__subagents.md` **L167-169**:
  "**`gpt-5.6`**: Start here for demanding agents." / "**`gpt-5.6-terra`**: Use for agents that favor speed and efficiency over depth…" / "**`gpt-5.6-luna`**: Use for fast, narrowly scoped agents handling clear, repeatable, or high-volume work."
- FR-7의 세 요구를 모두 이행 ✅ — ⓐ **"이건 원문 표기 그대로"**라고 병기 ⓑ **"이 페이지는 `gpt-5.6`을 계열 또는 기본 구성의 이름으로 쓴다"**로 성격 규정(FR-7의 판정과 동일) ⓒ **"여기서 임의로 특정 모델 ID로 바꿔 읽지 않는 편이 낫다"**로 해석 금지
- L154의 마무리("문서 안에서 표기가 갈리는 자리를 만나면, 우리가 할 일은 해석이 아니라 병기다")는 **FR-7을 독자용 규율로 승격한 문장**이다. 8장·12장의 모델 서술에서 재사용하라
- FR-7 지시대로 **원문 재확인을 반복하지 않았다** — 위 대조는 이번 파의 인용 대조 과정에서 부수적으로 얻은 것이므로 추가 비용 없음

#### ② 훅 이벤트 11개 직접 카운트 — **✅ 확인됨 (FR-9 모범 적용)**
- **직접 카운트:** `codex__hooks.md` `## Hooks` 섹션(L477-929)의 `###` 이벤트 하위 절 = **11개** — SessionStart / SessionEnd / SubagentStart / PreToolUse / PermissionRequest / PostToolUse / PreCompact / PostCompact / UserPromptSubmit / SubagentStop / Stop
- 초안의 분해(턴 중 8 + 시작 2 + 종료 1 = **11**)와 **이벤트 이름 11개가 전부 일치** ✅
- 교차 확인: `matcher` 표(L328-340)의 이벤트 행도 **11행**으로 같은 집합 ✅
- **"`SessionEnd`는 서브에이전트에는 걸리지 않는다" ✅ verbatim** — "It won't run for subagents."(L518)
- 다만 귀속 문구에 문제가 있다 → **⚠️-1**

#### ③ 이슈 3건 상태 — **✅ 확인됨 (전 셀 일치)**
| 이슈 | 초안 | 원장(`community.md`) | 판정 |
|---|---|---|---|
| #14039 | 기능 요구 · 2026-03-09 · 17 · open | L462 동일 | ✅ |
| #31814 | 버그 · 2026-07-09 · 167 · closed | L451·L74 동일 | ✅ |
| #15250 | 문서 불일치 · 2026-03-20 · 16 · open | L463 동일 | ✅ |
- 성격 3분류가 원장 서술과 정확히 대응 ✅ — #31814는 제목부터 "GPT-5.6 Sol cannot specify subagent models, forcing all subagents to also be Sol instances"(특정 버그), #14039는 "Allow per-subagent model/provider/profile selection"(근본 요구), #15250은 `spawn_agent`가 일반 `agent_type`만 받는 문서-동작 불일치
- **"That is not the behavior the docs imply." ✅ verbatim** + CLI **0.144.1** 재현(2026-07-12) ✅ (`community.md` L425)
- ⭐ **"#31814에는 후속 이슈가 하나 더 달려 있어서, closed 하나로 이 축이 정리됐다고 보기는 이르다"(L166) ✅** — 원장 L85에 실재한다: **#34301 "GPT Sol and Terra threads cannot spawn Luna subagents"(2026-07-20, 👍 23, open)**
  - **개선 권고(비블로킹):** 이 장이 스스로 "번호를 열어보라"고 가르치므로, 후속 이슈도 번호를 다는 편이 일관된다 → "후속 이슈([#34301](https://github.com/openai/codex/issues/34301), 2026-07-20, 👍 23, open)가 하나 더 달려 있어서"

#### ④ "Plugins aren't available in the IDE extension." verbatim — **✅**
- `codex__plugins.md` **L47** 원문 그대로 ✅
- 이어지는 서술 "데스크톱 앱·웹·CLI에서 브라우저를 열어 설치해야 한다"도 **세 표면 전부 확인됨** ✅ — 데스크톱(L19-21 "open **Plugins** to browse, install, and use plugins") / 웹(L26-28 "In ChatGPT web, turn on Work in the switcher and open **Plugins**…") / CLI(L34-37 "enter `/plugins` to open the plugin browser")
  - 원문 L47-48은 IDE 절 안이라 "use the ChatGPT desktop app or Codex CLI" 둘만 들지만, **웹도 실제 지원 표면**이므로 초안의 3표면 서술이 더 정확하다 ✅
- 표 3 플러그인 행의 "새 세션에서 확인" ✅ — "start a new session before using its bundled skills or tools"(L37-38)

#### ⑤ 스킬 탐색 위치 5행 표 — **❌ 한 행이 빠졌고, 본문과 어긋난다 (❌-1)**

### ❌ 정정 필요 (BLOCKING)

#### ❌-1. 표 1에 `SYSTEM` 행이 없다 — 같은 절 본문과 모순 (L30-40)

- **본문 L30:** "Codex는 저장소·사용자·관리자·**시스템** 위치에서 스킬을 읽는데…" → 원문 verbatim이다 ✅ ("Codex reads skills from repository, user, admin, and **system** locations", `codex__build-skills.md` L135)
- **그런데 바로 아래 표 1에는 REPO 3 · USER 1 · ADMIN 1 = 5행뿐이고 SYSTEM 행이 없다.** 본문이 네 범위를 말하고 표가 세 범위를 보여준다 — **장 내부 모순**이다.
- **원문 표는 6행이다**(`codex__build-skills.md` L137-145). 빠진 행:
  > `SYSTEM` | Bundled with Codex by OpenAI. | Useful skills relevant to a broad audience such as **the skill-creator and plan skills**. Available to everyone when they start Codex.
- **이 누락이 특히 아까운 이유:** 바로 앞 절 L24가 **`$skill-creator`**를 소개한다. SYSTEM 행이 그 스킬이 어디서 오는지("설치만 하면 누구에게나 있다")를 정확히 설명해준다. 행 하나를 넣으면 앞 절과 이 절이 연결된다.
- **수정안:** 표 1에 행 추가.
  > `| SYSTEM | Codex에 번들 | \`$skill-creator\`·plan 같은 기본 제공 스킬 — 설치하면 누구에게나 있다 |`
- 나머지 5행은 경로·쓰임 모두 원문과 일치한다 ✅

#### ❌-2. "지침 파일은 가장 가까운 하나만 보고" (L44) — 4장과 원문 양쪽에 어긋난다

- **초안:** "둘째, 저장소 스킬은 위로 올라가며 전부 모인다. **3장에서 본 중첩 `AGENTS.md`의 동작과 정반대다.** 같은 제품 안에서 **지침 파일은 가장 가까운 하나만 보고**, 스킬은 경로를 타고 올라가며 다 모은다."
- **두 가지가 틀렸다.**
  1. **`AGENTS.md`도 여러 개를 모은다.** 원문(`codex__agent-configuration__agents-md.md` L12-13): "In each directory along the path, it checks for… Codex includes **at most one file per directory**." / "Codex **concatenates files from the root down**, joining them with blank lines." → **디렉터리당 한 파일씩, 경로 전체에서 여러 개를 이어 붙인다.** "가장 가까운 하나만"이 아니다.
     - **4장 L70-74가 이걸 정확히 서술했다.** 6장이 4장을 반박하는 상태다.
     - 오염원 추정: 3장에 인용된 **`AGENTS.md` 표준** 문구("Agents automatically read the nearest file in the directory tree, so the closest one takes precedence" — miraclebakelaser, #12115). 그건 **표준의 규정**이고 **Codex의 동작이 아니다.** 3장은 그 구분을 지켰는데 6장에서 흡수됐다.
  2. **"정반대"가 성립하지 않는다.** 지침은 루트→cwd로 내려오고 스킬은 cwd→루트로 올라가지만, **훑는 디렉터리 집합은 같다.** 방향만 반대고 커버리지는 동일하다. 따라서 이어지는 "왜 규칙은 안 읽히는데 스킬은 다 뜨지"라는 상황은 **이 비대칭으로는 발생하지 않는다.**
- **수정안 (실재하는 차이로 교체):**
  > 둘째, 저장소 스킬은 **현재 디렉터리에서 저장소 루트까지 올라가며 모인다.** 4장에서 볼 지침 파일과 방향이 반대인데(지침은 루트에서 현재 디렉터리로 내려온다), 훑는 디렉터리 집합 자체는 같다. 진짜 차이는 **모으는 방식**에 있다. 지침은 디렉터리당 한 파일만 쓰고 결합 크기가 32 KiB에 닿으면 뒤가 잘리지만, 스킬은 **범위가 네 개**(저장소·사용자·관리자·시스템)로 늘어나고 심볼릭 링크까지 따라가며, **이름이 같아도 병합 없이 둘 다 목록에 오른다.**
- 근거: 범위 4종 ✅ L135, 심볼릭 링크 추적 ✅ L147("Codex supports symlinked skill folders and follows the symlink target"), 동명 스킬 미병합 ✅ L135
- **⚠️ 4장과의 정합성은 editor 통권 검수에서도 확인 대상이다.** 두 장이 같은 메커니즘을 다르게 서술하는 상태로 합본되면 Phase 4.5에서 걸린다.

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. "문서가 표로 정리한 실행 시점은 이렇다" (L86) — 그런 표는 없다
- 이벤트 **개수와 이름은 정확하다**(위 판정 ②). 문제는 귀속이다. `codex__hooks.md`에는 "실행 시점"으로 묶은 표가 없다. 이벤트는 `## Hooks` 아래 `###` 절로 나열되고, 표로 된 것은 **`matcher` 표**(L328-340, 무엇을 필터링하는지)다.
- 턴 중 8 / 시작 2 / 종료 1이라는 **3분류는 저술가의 정리**이며 원문의 구성이 아니다.
- **수정안:** "문서가 정의한 훅 이벤트를 실행 시점으로 묶으면 이렇다." (귀속을 저자 정리로 되돌린다)

#### ⚠️-2. `SessionEnd` 서술이 원문보다 좁다 (L86)
- 초안: "**메인 스레드가 끝날 때** 하나(`SessionEnd`)"
- 원문(L514-518)은 발화 조건을 셋으로 명시한다 — 열려 있는 대화를 **아카이브하거나 삭제할 때**, Codex가 **정상 종료할 때**, 그리고 대화가 유휴 상태로 **어느 클라이언트에도 열려 있지 않은 채 30분이 지난 뒤**.
- "끝날 때"로 뭉개면 **30분 유휴 발화**를 예상하지 못한다. 세션 종료 훅으로 정리 작업을 거는 사람에게는 실무 차이가 있다.
- **수정안:** "메인 스레드가 끝날 때 하나(`SessionEnd` — 아카이브·삭제·정상 종료, 그리고 **어디에도 열려 있지 않은 채 30분이 지났을 때** 발화한다)"

### ✅ 확인됨 (37건 — 근거 요약)

**정의·경계 (`codex__skills-and-plugins.md`)**
- "A skill packages instructions and supporting resources for a specific task or workflow." ✅ verbatim (L9-10)
- "A plugin is an installable bundle that can include skills, connectors, or both. Connectors are backed by Model Context Protocol (MCP) servers and can optionally include custom ChatGPT UI." ✅ verbatim (L11-13)
- 스킬 3 구성요소 ⓐ 이름·설명 ⓑ 워크플로 지시 ⓒ 보조 자원(템플릿·예시·스키마·연결된 도구) ✅ L23-27 **3항목 전부 대응**
- 선택 기준 ✅ L90-92 ("Use a skill when you need reusable instructions for a focused task. Use a plugin when you want an installable package that can combine instructions with connected services or other tools.") — 초안의 재진술("혼자 쓸 절차면 스킬, 남에게 건넬 물건이면 플러그인")은 저자 정리로 표기돼 있고, `customization/overview` L79-80("plugins are the installable distribution unit")이 방향을 뒷받침 ✅
- `$skill-creator`(ChatGPT 표면 `@skill-creator`) ✅ / 호출 문법 3장 이관 ✅ (m3 분담 준수)

**스킬 예산**
- ⭐ **2% 인용 verbatim ✅** (`codex__build-skills.md` L37-41) — "In Codex, the initial list also includes each skill's file path. To avoid crowding out the rest of the prompt, this list uses at most 2% of the model's context window, or 8,000 characters when the context window is unknown. If many skills are installed, Codex shortens skill descriptions first. For large skill sets, Codex may omit some skills from the initial list and show a warning."
- 초안의 요약("설명이 먼저 줄고, 그다음엔 스킬이 목록에서 빠진다")이 원문 두 문장의 순서를 정확히 옮겼다 ✅
- 점진적 공개(처음엔 이름·설명, 선택 후 `SKILL.md` 전문) ✅ / "초기 목록에만 적용되는 예산" ✅
- 필수 필드 `name`·`description` 둘뿐 ✅
- [#19679] 2026-04-26 · 👍 31 · open ✅ / 코드 위치 특정 ✅ / 경고 문자열 존재 ✅ (`community.md` L89-92)
- **aldegad 실측 ✅ 전건** — 2026-04-28 / **15,822자 → 13,992자** / codex-cli **0.125.0-alpha.3** / macOS / 경고 소멸. **"단일 환경 측정이라 그대로 우리 숫자가 되지는 않는다"는 단서 병기 ✅** — 규율 9·4 준수
- 컨텍스트 예산 3연작 예고(8장 #32806 · 11장 MCP) ✅ 계획과 일치

**커스텀 프롬프트 (파 1 2장과 동일 근거, 표기 일관)**
- "Custom prompts are deprecated. Use skills for reusable instructions that Codex can invoke explicitly or implicitly." ✅ verbatim (web-6 L1270)
- `~/.codex/prompts/` ✅ / 슬래시 목록에 **`/prompts:<이름>`** 형태로 노출 ✅ (web-6 L2281 "Custom prompts appear as `/prompts:<name>` commands.")
- "explicitly or implicitly"를 호출 경로 2개의 근거로 쓴 해석 ✅ 원문 범위 내

**훅**
- ⭐ **"Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility with existing plugin hooks." ✅ verbatim** (`codex__hooks.md` L313-314). 초안의 위치 서술("`PLUGIN_ROOT`·`PLUGIN_DATA`를 설명한 바로 다음 줄에")도 정확 ✅ (L309-312)
- exit code `2` + `stderr`에 이유 ✅ L622·L764 / `permissionDecision: "deny"` + 이유 JSON ✅ L607-608
- 해시 기반 신뢰 검토 ✅ L61-70 전건 — 비관리형 명령 훅은 검토·신뢰 필요 / **현재 해시에 대고 기록** / 새로 생기거나 바뀌면 재검토 대상이며 그때까지 건너뜀 / `/hooks`에서 검토·신뢰·비활성화 / 시작 시 경고 / `--dangerously-bypass-hook-trust`로 그 실행에 한해 우회
- 플러그인 번들 훅도 신뢰 전까지 건너뜀 ✅ L316-318 (표 3 함정 열과 일치)
- [#21753] 2026-05-08 · 👍 22 · open · **엄브렐라 트래커** ✅ (`community.md` L64)
- 이벤트 매트릭스 ✅ L65 — `SessionStart` Shipped / `UserPromptSubmit` Shipped / `PreToolUse` **Partial** / `PostToolUse` **Partial** / 일부 Missing. 초안 L90의 서술과 정확히 대응
- **"Coverage must be consistent across every tool handler, not only selected paths." ✅ verbatim** L66
- ⭐ **"29+" 귀속 ✅** — "제목에 붙은 '29+'라는 수치는 이 이슈가 대조군으로 제시한 숫자다". FR-3의 명시 요구를 3장에 이어 두 번째로 정확히 이행

**execpolicy (`codex__agent-configuration__rules.md`)**
- **"Rules are experimental and may change." ✅ verbatim** (L7) — 강점을 길게 쓰기 전에 고지부터 단 순서가 정확
- `.rules` 위치 `~/.codex/rules/default.rules` ✅ / 활성 config 레이어마다 `rules/` 스캔 ✅ / **프로젝트 로컬은 `.codex/` 레이어가 신뢰됐을 때만 로드** ✅ L42 (4장 표 1의 미신뢰 스킵과 정합)
- `prefix_rule` 예시 ✅ **코드 블록이 원문과 동일**(L13-37) — `pattern`·`decision`·`justification`·`match` 3항·`not_match` 1항 전부
- `justification` ✅ L64 — 승인 프롬프트·거부 메시지에 노출 가능 / `forbidden`이면 대안 병기 권고 + **`rg` vs `grep` 예시가 원문 예시 그대로** ✅
- **"inline unit tests" ✅** L26-27·L65 / `not_match` 항목이 걸리지 않는 이유("the `pattern` must be an exact prefix") ✅ L34
- `codex execpolicy check --pretty --rules … --` ✅ **명령이 원문과 문자 단위 일치**(L125-129) / 출력 = 가장 엄격한 판정 + 걸린 규칙 + `justification` ✅ L131 / `--rules` 다중 지정 ✅
- 셸 래퍼 처리 ✅ L77-93 — `bash -lc`·`bash -c`·`zsh`/`sh` 등가물 특별 취급 / **평범한 단어가 `&&`·`||`·`;`·`|`로만 이어진 선형 사슬**이면 파싱해 분리 / 예시가 `["git","add","."]`과 `["rm","-rf","/"]` 둘로 갈라짐 / **가장 엄격한 판정이 이긴다** / `git add` 허용해도 전체가 자동 허용되지 않음(L94)
- 분리 불가 조건 5종 ✅ L99-105 — 리다이렉션(`>`,`>>`,`<`) / 치환(`$(...)`) / 환경 변수 대입(`FOO=bar`) / 와일드카드(`*`,`?`) / 제어 흐름 — **초안의 5항목과 1:1**, 그리고 전체를 단일 invocation으로 취급 ✅ L110-116
- `Starlark` ✅ L135 verbatim (파이썬 닮은 문법, 부작용 없이 안전, 파일 시스템 미접촉)
- 2장 정전 표의 `.rules` 행("대응 + Codex가 테스트 하네스 보유")과 정합 ✅

**서브에이전트 · Record & Replay**
- 내장 3종 `default`·`worker`·`explorer` + 각 역할 ✅ L325-327
- 경로 `~/.codex/agents/`(개인) · `.codex/agents/`(프로젝트) · 파일 하나당 에이전트 하나 TOML ✅ L330-333
- 필수 필드 3종 ✅ L338-342 + 스키마 표 L374-378 / **"진실의 출처는 `name` 필드" ✅ verbatim** ("the `name` field is the source of truth", L387-389)
- 추가 가능 키 `model`·`model_reasoning_effort`·`sandbox_mode`·`mcp_servers` + 생략 시 부모 상속 ✅ L344-350·L381
- 수치·선택 기준을 8장으로 넘긴 처리 ✅ (m6 분담 준수)
- Record & Replay ✅ — macOS / **초기 가용 지역에서 EEA·영국·스위스 제외** / **Computer Use가 가능하고 켜져 있어야 함** — `codex__extend__record-and-replay.md` L5-7 **3조건 전부 일치**. 예시("경비 처리", "정기 보고서 내려받기")도 원문 예시 그대로("file an expense", "download a recurring report") ✅

**표 3 이식 판단표 (6행)**
- 6행의 난이도·해야 할 일·함정이 위 근거들과 전건 정합 ✅. 함정 열의 이슈 번호·상태 3건(#19679 open / #21753 open / #14039·#31814·#15250)도 원장 일치 ✅
- 클로징 7단계 절차도 본문에서 확인된 사실만 사용 ✅

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` 본문 L9 1회 + 표 2·3 캡션 2회 ✅ (표 2는 수치 표, 표 3은 원장형)
- **FR-3 / 규율 12:** Claude Code 관련 서술이 `CLAUDE_PLUGIN_ROOT`·`CLAUDE_PLUGIN_DATA` **인용문**과 "29+" **귀속 표기**뿐 ✅. 훅 커버리지 비교에서 Claude Code 쪽 이벤트를 새로 정의하지 않았다
- **FR-7:** 완전 준수 (위 판정 ①)
- **규율 6·7·11:** 위반 없음 ✅
- **🕒 처리:** 훅 매트릭스(L96)·서브에이전트 이슈 표(L168) 두 곳에 "번호를 열어 현재 상태를 확인하라"는 고지를 붙였다 ✅ — 3장에서 세운 문형의 재사용이며, 이 때문에 🕒 판정이 0건이다

---

## 파(wave) 2 종합 — 오케스트레이터·저술가 통보

### BLOCKING 3건 (원고 확정 전 필수 해소)

| # | 장 | 항목 | 해소 방법 |
|---|---|---|---|
| 1 | 4장 | ❌-1 "문서는 갱신 시점을 **네 가지**로 구체화한다"(L27) — 원문은 5항목 | A안 "여러 갈래로" / B안 5번째(GitHub PR 코멘트 `@codex` 위임) 추가 |
| 2 | 6장 | ❌-1 표 1에 `SYSTEM` 행 누락 — 같은 절 본문("저장소·사용자·관리자·**시스템**")과 모순 | 행 1개 추가 (문안 제시함) |
| 3 | 6장 | ❌-2 "지침 파일은 가장 가까운 하나만 보고"(L44) — 원문·**4장 L70-74와 정면 충돌** | 대체 문단 제시함 (실재하는 차이로 교체) |

> ❌-3은 **장 간 모순**이라 6장만 고쳐서는 안 되고, 4장 서술이 정전임을 확인한 뒤 6장을 맞춰야 한다. 4장이 원문 그대로이므로 **6장을 고친다.**

### 비블로킹 권고 5건

4장 ⚠️-1(32 KiB 인용 중간 생략에 `…` 추가) · 4장 ⚠️-2(`[desktop]`은 커스텀 파일 핸들러 전용) · 5장 ⚠️-1("보안 벤치마크"로 범위 한정) · 6장 ⚠️-1(훅 이벤트 3분류는 저자 정리) · 6장 ⚠️-2(`SessionEnd` 30분 유휴 발화 병기)

### 파 2 총계

| 장 | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|
| 4장 | 35 | 1 | 2 | 0 |
| 5장 | 43 | 0 | 1 | 0 |
| 6장 | 37 | 2 | 2 | 0 |
| **합계** | **115** | **3** | **5** | **0** |

### 누적 (파 1+2, 6개 장)

| | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|
| 파 1 (1·2·3장) | 108 | 2 | 8 | 0 |
| 파 2 (4·5·6장) | 115 | 3 | 5 | 0 |
| **누적** | **223** | **5** | **13** | **0** |

**정확도 소견 — 파 1의 진단이 재확인됐다.** 이번 파에서 원문 verbatim 대조 대상은 **62건, 불일치 0건**이다. 반면 ❌ 3건 중 2건(4장 "네 가지", 6장 SYSTEM 행 누락)은 **또다시 "세기·옮겨 담기"에서 났다.** 파 1의 두 오류와 합치면 **❌ 5건 중 4건이 같은 계열**이다.

새로 관측된 것은 세 번째 계열이다 — **장 간 전파 오염**(6장 ❌-2). 3장이 인용한 *외부 표준*의 문구("nearest file… closest one takes precedence")가 6장에서 *Codex의 동작*으로 흡수됐고, 그 결과 4장을 반박했다. 인용은 정확했는데 **인용의 주어가 장을 건너면서 바뀌었다.** FR-18이 이 패턴을 겨눈다.

---

# 파(wave) 3 — 7·8·9장

> 판정 기준: 파 1·2와 동일 + 누적 규율 **FR-1 ~ FR-18**.

## 07장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/07_draft.md`(스타일 반영본) · 구체 주장 41건 추출

**집계: ✅ 38 / ❌ 1 / ⚠️ 2 / 🕒 0**

### 저술가 명시 요청 판정

#### ① 두 프레임 원문 대조 + `best-practices` FR-15 판정 — **✅ 확인됨**

- **프레임 1 (`/codex/prompting`) — 원문 캐시 직접 대조, 4항목 문자 단위 일치 ✅**
  `codex__prompting.md` L17-21: "**Goal:** What should ChatGPT do? / **Context:** What information or sources will help? / **Output:** What format, length, or level of detail do you need? / **Boundaries:** What must stay unchanged? What should ChatGPT avoid or check with you before it acts?" — 초안 L15-18과 완전 일치
- **프레임 2 (`best-practices`) — FR-15 tier 2 적용, 통과 ✅**
  근거 `research/web-6.md` L1360-1363. 4항목 확인 — **Goal / Context / Constraints / Done when** ✅. 원문 캐시(`guides__best-practices.md`)가 404 페이지라 대조 불가한 것은 파 2에서 이미 확정했고(FR-15), **판정을 반복하지 않는다.**
  - 초안이 프레임 2를 **인용 블록이 아니라 산문으로 요약**한 것은 오히려 옳은 처리다. FR-15는 이 출처의 인용을 "문자 단위로 옮기고 재구성하지 마라"고 했는데, 초안은 인용하지 않고 항목명만 옮겼으므로 위반이 아니다 ✅
- **두 프레임을 병기하고 어느 쪽도 지우지 않은 처리 ✅** — FR-6(문서 내부 불일치는 정전 페이지 하나만)의 예외가 정당한 자리다. 여기서는 **둘 다 원문이고 용도가 갈리므로** 병기가 맞다. 초안 L22의 해설(앞쪽은 일반 작업용, 뒤쪽은 코드 작업용 어휘)도 두 프레임의 항목 성격과 부합
- **"Use only the parts that help. You don't need to fill in every item or follow a required format." ✅ verbatim** (L23-24)

#### ② 여덟 가지 실수 8불릿 직접 카운트 — **✅ 확인됨 (FR-16 모범)**

- **직접 카운트: `web-6.md`의 "흔한 실수" 목록 = 정확히 8불릿** ✅
- 초안 L56-63의 8불릿이 **원문과 문자 단위로 일치** ✅ (Overloading / Not letting the agent see its work / Skipping planning / Giving Codex full permission / Running live tasks without Git worktrees / Scheduling a recurring task before it's reliable manually / Treating Codex like something you have to watch step by step / Using one chat for an entire project)
- 초안 L65의 재집계 "여덟 개 중 **다섯 개**가 프롬프트 바깥의 문제" — 직접 확인: 지침 파일(1) · 권한(4) · 워크트리(5) · 예약 실행(6) · chat 관리(8) = **5개** ✅ 카운트 정확
- 표 1의 8행도 원문 8불릿과 1:1 ✅. 캡션이 "…의 흔한 실수 여덟 가지와 **대응**"이라 원문 표라고 주장하지 않는다 ✅ (대응·관련 장 열은 저자 정리)

#### ③ METR 수치와 조건 4종 — **✅ 확인됨 (조건 병기 완전 이행)**

- Becker, Rush, Barnes, Rein (METR), **arXiv:2507.09089**, 2025, 📄 preprint ✅ (`papers.md` §3-3 L176-178). 저자 순서까지 원장과 동일
- **식별자 점검:** YYMM=2507(2025-07)은 빌드 시점 2026-08-02 기준 과거 ✅. 형식 정상, 자동 ❌ 규칙 비해당
- 인용 verbatim ✅ — "Before starting tasks, developers forecast that allowing AI will reduce completion time by 24%. After completing the study, developers estimate that allowing AI reduced completion time by 20%. Surprisingly, we find that allowing AI actually increases completion time by 19%—AI tooling slowed developers down."
- 세 숫자 24% / 20% / 19% **증가** ✅
- **조건 4종 전부 일치 ✅** (`papers.md` L179·L187) — 숙련 개발자 **16명** / 과제 **246개** / **평균 5년간 다뤄온 자기 저장소** / 도구 기준 **2025년 2~6월**
- ⭐ 원장이 "**반드시 함께 적을 것**"이라 요구한 한계 서술을 초안이 초과 이행했다 — "이 실험은 **AI에게 가장 불리한 조건에서의 상한선 측정**에 가깝고, 낯선 코드베이스나 새 언어로 일반화할 수 없다"(L186). 원장 L187의 "AI에게 가장 불리한 조건" 표현과 정확히 대응
- 결론 처리도 정확 ✅ — "속도에 대한 결론은 이 조건에서 일반화되지 않는다. 남는 것은 **자기 체감이 방향까지 틀릴 수 있다**는 사실 하나다"

#### ④ 관점 A·B·C 귀속·게시일 — **✅ 확인됨 (3건 전건)**

| 관점 | 초안 표기 | 원장 | 판정 |
|---|---|---|---|
| A | Kyutae Park(AWS AI 스페셜리스트 SA), AWS 한국 기술블로그, **2026-06-11** | `community.md` L142 — Kyutae Park, Ph.D (AWS AI 스페셜리스트 SA), 2026-06-11, `[출처 명확 — 실명·소속 있음]` | ✅ |
| B | Hacker News, chandureddyvari, **2026-02-03** | `community.md` L163, `[익명 주장·확인 필요]` | ✅ |
| C | r/codex, imperfectlyAware, **2026-04-24**, macOS/Swift + 레거시 ObjC | `community-2.md` L45, 환경 명시 | ✅ |

- 관점 A 내용 ✅ 전건 — "단일 패스 작성자"·"700~800줄"·"장인적 접근"·`pwd`/`ls`·`apply_patch`·자가 검증 (`community.md` L144)
- 관점 B·C 인용 verbatim ✅ (B는 첫 절만, 문장 경계 절단)
- **3장의 V3 지시 이행 확인 ✅** — 3장에서 존재만 알리고 7장으로 넘긴 AWS 자료를 여기서 펼쳤고, 귀속 범위(실행 스타일 비교)를 벗어나지 않았다
- ⭐ **"셋 다 인용된 관측이고, 셋 다 서로를 반박한다"(L132)** + 성격 규정 거부 ✅ — FR-12·FR-17이 요구한 "판정 불가를 판정으로 위장하지 않기"를 산문으로 구현
- 코드베이스 성격 가설을 **"이건 가설이고, 이 책의 리서치는 이를 확인할 근거를 갖고 있지 않다"**(L134)로 닫은 처리 ✅ — 원장 `community-2.md` L543의 "코드베이스 성격이 변수"와 등급이 일치

#### ⑤ PinEnvironmental6395 인용 verbatim — **❌ 두 군데가 원문과 다르다 (❌-1)**

### ❌ 정정 필요 (BLOCKING)

#### ❌-1. PinEnvironmental6395 인용문이 변조됐다 (L44)

- **원장** (`community-2.md` L251, `[익명 주장·확인 필요 — 다만 이 문서에서 가장 많이 재확인된 관찰]`):
  > "**GPT-5** is very good at doing what you say. But if you don't tell it what you want it won't do it. It's the opposite tradeoff Claude makes — **it's good** at figuring out what you want but at the cost of doing things you didn't want it to do. You have to prompt gpt to be proactive and Claude to be non-destructive."
- **초안 L44:**
  > "**GPT** is very good at doing what you say. … It's the opposite tradeoff Claude makes — **good** at figuring out what you want …"
- **차이 2건:**
  1. **`GPT-5` → `GPT`** — 모델 세대 표기가 지워졌다. **이것이 의미 있는 변조다.** 원 진술은 GPT-5 세대에 대한 관측인데, `GPT`로 일반화하면 세대 무관 성격 규정으로 읽힌다.
  2. `it's good` → `good` — 두 단어 누락(경미)
- **왜 BLOCKING인가:** 이 장 자신이 L146에서 독자에게 규율을 넘긴다 — **"'이 모델은 지시를 잘 따른다/안 따른다'는 문장을 볼 때는 반드시 버전과 시점을 확인하자. 그 두 가지가 없는 서술은 다음 릴리스에서 뒤집혀도 반박할 방법이 없다."** 그런데 이 장의 대표 인용에서 **버전 표기를 지웠다.** 자기가 세운 규율을 자기 인용에서 어긴 형태라, 남겨두면 장 전체의 논지가 자기모순이 된다.
- **수정안:** 원문 그대로 복원.
  > "GPT-5 is very good at doing what you say. But if you don't tell it what you want it won't do it. It's the opposite tradeoff Claude makes — it's good at figuring out what you want but at the cost of doing things you didn't want it to do. You have to prompt gpt to be proactive and Claude to be non-destructive."
- 인용 뒤의 귀속 서술(L42·L48 — r/codex 진영 명시, 게시일 2026-05-12, "공식 문서가 보증하는 성격 규정도 아니다")은 **정확하므로 그대로 둔다** ✅

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. `/codex/guides/best-practices` — 존재하지 않는 경로 (L20·L54·L80, 3회)

- **실제 경로:** `https://learn.chatgpt.com/**codex/learn**/best-practices` (캐노니컬 `https://learn.chatgpt.com/**guides**/best-practices`) — `web-6.md` L1342
- 초안의 `/codex/guides/best-practices`는 **둘을 섞은 하이브리드**라 어느 쪽으로도 열리지 않는다. 독자가 URL로 찾아갈 자리라 실무 손해가 있다.
- **수정안:** 3곳 모두 `/codex/learn/best-practices`로 통일. (다른 장들이 `/codex/...` 형식을 쓰므로 이쪽이 표기 일관성에도 맞다)

#### ⚠️-2. xoStardustt 인용이 문장 중간에서 끊긴다 (L138)

- **초안:** "Sol tends to go apeshit and refactor half my code ... even with an agents.md that explicitly forbids"
- **원문**(`community-2.md` L206): "…(and even with an agents.md that explicitly forbids **cleanup/refactor if it's out of scope**)."
- 목적어가 잘린 채 끝나 인용문 자체로는 무엇을 금지했는지 알 수 없다. 바로 다음 문장이 "정리·리팩터링을 명시적으로 금지한"으로 풀어주므로 **의미 왜곡은 없다.**
- **수정안:** 끝에 `…`를 붙이거나 `forbids cleanup/refactor`까지 넣는다.

### ✅ 확인됨 (38건 — 근거 요약)

**프롬프팅 원문 (`codex__prompting.md`)**
- 4요소 ✅ / "Use only the parts that help…" ✅ / **Boundaries 정의** ✅ L104-107 / **"Focus on the one or two boundaries that matter most. You don't need to control every step ChatGPT takes." ✅** L113-114 — 초안 L28의 "가장 중요한 한두 개에 집중하라고 못 박는다"가 원문 수치와 정확히 일치
- Codex 프롬프트 정의 4요소 ✅ L311-313 — "names the behavior you want, points to the relevant code or reproduction steps, preserves important constraints, and **says how to verify the change**"
- **"Your first prompt doesn't need to be perfect. Review the result, then ask for the specific change you want." ✅ verbatim** L135-136
- 초안 L38의 모순 해소("완벽하지 않아도 되는 것은 지시의 상세함이고, 미리 정해야 하는 것은 끝났다는 판정 기준")는 두 원문의 대상 차이를 정확히 읽은 해석 ✅

**chat 단위 · `/goal`**
- **"Keep one chat per coherent unit of work. If the work is still part of the same problem, staying in the same chat is often better because it preserves the reasoning trail. Fork only when the work truly branches." ✅ verbatim** (`web-6.md`)
- 초안 L92의 강조점("가운데 문장" — 같은 문제면 한 chat에 머물러라)이 정확 ✅. "자주 새로 시작하라"로 오독하지 말라는 경고도 원문 취지와 일치
- `/goal` 3요소 표 ✅ — `codex__long-running-work.md` L82-85 **Outcome / Constraints / Verification** 원문 표와 1:1
- 예시 verbatim ✅ L91-92 "Migrate this codebase from JavaScript to TypeScript. Preserve existing behavior, compile in strict mode without explicit `any` types, and make the full test suite pass."
- `/plan` → `/goal` 순서 ✅ (파 2와 동일 근거 `long-running-work.md` L69-71, 표기 일관)
- `/fork`·`/side`(별칭 `/btw`) 용법 ✅ (3장에서 확인한 문법과 정합 — 부모 상태 계속 표시까지)
- [#13942] 2026-03-08 · 👍 34 · open ✅ (`community.md` L459) + **"이슈 상태는 바뀔 수 있으니 표에 적힌 상태를 외우기보다 번호를 열어 확인하자" 🕒 고지 ✅**

**예약 실행 (`codex__automations.md`)**
- **"Scheduled tasks run unattended with your default sandbox settings." ✅ verbatim** L114·L229 — 초안 L156의 "무인으로 실행되며 기본 샌드박스 설정을 그대로 쓴다"가 정확
- 예약 전 3확인 ✅ L204-209 **3항목 원문과 1:1** (프롬프트 명확·범위 / 모델·추론 강도·도구 동작 / 결과가 검토 가능한 형태)
- "처음 몇 번의 실행 결과는 직접 보고 프롬프트나 주기를 조정" ✅ L211-212
- 워크트리 누적 + 보관 처리 + 고정 회피 ✅ L221-227

**입출력**
- 웹 검색 4모드 `cached`(기본)·`indexed`·`live`·`disabled` ✅ + `--search`가 그 호출에 한해 live ✅ + **전체 접근 시 기본이 live** ✅ (5장과 동일 근거 `_config-reference-tables.md` L247, 표기 일관)
- "프롬프트 인젝션 위험을 낮추지만 없애지는 않는다" ✅ — 원문의 강도("reduces exposure … but you should still treat web results as untrusted")를 과장 없이 옮겼다
- Visualizations CLI·IDE 미렌더 ✅ (1장과 동일 근거)
- **"Work with files" 명칭 ✅ — 규율 8 준수** ("Artifacts viewer"를 쓰지 않았다)
- IDE 자동 컨텍스트 vs CLI 명시 Note ✅ (1장과 동일 근거) + 초안 L108의 해석("프롬프트가 나쁜 게 아니라 파일이 안 들어간 것이다") ✅
- steering/queuing ✅ (3장과 동일 근거, 표기 일관)

**논쟁 절**
- NootropicDiary **2026-07-10** / xoStardustt **2026-07-11** ✅ + "같은 모델, 같은 주, 정반대의 경험" ✅ (`community-2.md` L203-206 — 하루 차이 정확)
- ⭐ **초안이 원장의 `Fable` 비교 부분을 옮기지 않은 것은 옳다** — 화이트리스트 밖 모델 비교를 스스로 잘라냈다. FR-3 준수 ✅
- 판정 유보 + 실무 함의 도출("어느 쪽 성향을 가정하고 프롬프트를 짜도 절반은 틀린다 → 성향에 기대지 않는 프롬프트가 안전하다") ✅ — 원장이 "판정 유보"로 남긴 것을 유보한 채로 쓸모를 뽑아낸 처리
- **"이 책에 적힌 관측들도 예외가 아니어서, 전부 게시일과 함께 적었다"(L146)** — 실제로 이 장의 커뮤니티 인용 6건 전부에 게시일이 붙어 있다 ✅ 규율 9 완전 준수 (❌-1의 버전 표기 누락만 예외)

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` L84 **1회**. 문언 그대로 준수 ✅
- **FR-3 / 규율 12:** Claude Code 고유 주장 0건. 인용문 안의 `Claude` 언급뿐이며 초안이 새로 정의하지 않았다 ✅
- **규율 6:** 인용 금지 9건 전건 미사용 ✅ (스캔으로 확인)
- **규율 11:** 경험담 0건 ✅
- ⚠️ **인접 위험 고지:** `codex__automations.md` **L110**의 Illustration `ariaLabel`에 **"5.6 Sol Extended"**가 들어 있다 — FR-4가 인용을 금지한 UI 삽화 문자열이다. 7장은 인용하지 않았다 ✅. **12장(표면 소개)이 이 페이지를 열 때 걸릴 자리이므로 FR-19로 경고를 승격한다.**

---

## 08장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/08_draft.md`(스타일 반영본) · 구체 주장 49건 추출

**집계: ✅ 47 / ❌ 0 / ⚠️ 2 / 🕒 0**

> **최고 위험 장으로 지목됐으나 ❌가 0건이다.** 요금·한도·크레딧 수치 **31개 셀을 `codex__pricing.md` 원문과 전수 대조했고 불일치가 없었다.** 규율 4(범위값 보존)·FR-1(은퇴 미래 시제)·규율 6(인용 금지)이 전건 준수됐다. 아래는 그 확인 기록이다.

### 저술가 명시 요청 판정 (7건)

#### ① 플랜 가격 원문 대조 — **✅ 6개 값 일치 / ⚠️ 배수 매핑 1건 (⚠️-1)**

`codex__pricing.md`의 `PricingCard` 속성을 직접 읽어 대조했다.

| 초안 | 원문 | 행 | 판정 |
|---|---|---|---|
| Free `$0` | `name="Free"` `price="$0"` | L29·L31 | ✅ |
| Go `$8` | `name="Go"` `price="$8"` | L37·L39 | ✅ |
| Plus `$20` | `name="Plus"` `price="$20"` | L45·L47 | ✅ |
| Pro `$100` | `name="Pro"` `priceEyebrow="From"` `price="$100"` | L63·L66 | ✅ |
| Pro `$200` | "Unlimited ChatGPT Voice on the **$200/month tier**" | L77 | ✅ |
| Business 사용자당 `$20` | `name="Business"` `price="$20"` `interval="/ user / month*"` | L108·L110 | ✅ |
| **Business 각주** — 2명 이상 · 연간 결제 · 월 결제 시 사용자당 월 `$25` | `footnoteLabel="*2+ users, billed annually. $25 per user per month when billed monthly."` | **L114** | ✅ **문자 단위 일치** |

- 각주 3요소(2+ users / billed annually / $25 monthly)를 하나도 빠뜨리지 않았다 ✅ — 규율 4가 가장 경계한 "조건을 떼고 숫자만 옮기기"를 정확히 피했다
- 배수 매핑만 ⚠️-1로 분리

#### ② 크레딧 표 — 캐시된 입력 열 원문 직접 대조 — **✅ 9개 셀 전건 일치**

- `codex__pricing.md` **L811-828** 원문 표와 대조:

| 모델 | 입력 | **캐시된 입력** | 출력 | 판정 |
|---|---|---|---|---|
| GPT-5.6 Sol | 125 | **12.5** | 750 | ✅ |
| GPT-5.6 Terra | 50 | **5** | 300 | ✅ |
| GPT-5.6 Luna | 5 | **0.5** | 30 | ✅ |

- **저술가 관측이 정확하다** — `01_reference.md`에 캐시된 입력 열이 없어 원문에서 직접 발췌한 것이고, **그 발췌가 원문과 정확히 일치한다** ✅
- ⭐ **행 수 카운트도 정확하다.** 캡션이 "원문에는 이전 세대와 이미지 모델을 포함해 **아홉 행**이 있다"고 적었는데, 원문 `<tbody>` 직접 카운트 결과 **9행**(Sol·Terra·Luna·GPT-5.5·GPT-5.4·GPT-5.4 mini·Codex-Spark·GPT-Image-2 image·GPT-Image-2 text) ✅ — **FR-16 4항("일부만 옮길 거면 캡션에 명시")을 정확히 이행**
- 초안 L151의 해석("캐시된 입력은 일반 입력의 10분의 1이다. 세 모델 모두 같은 비율") — 125/12.5, 50/5, 5/0.5 = 전부 10배 ✅ 산술 정확
- 오프닝 "스물다섯 배" ✅ — 입력 125÷5=25, 출력 750÷30=25, "출력 쪽도 같은 배율" ✅
- 각주 2건 ✅ verbatim — "GPT-5.6 usage averages **5-40** credits per message."(L879) / Fast mode가 더 빨리 소모(L883-885)

#### ③ 프리셋·`--model`·`-m` — **✅**

- **프리셋 4종 원문 verbatim ✅** (`codex__models.md` L296-299): "Start with the default **Power** setting, which uses `gpt-5.6-sol` with medium reasoning. Move toward **Smarter** for deeper reasoning or **Faster** for faster, lower-cost work. Open **Advanced** when you want `gpt-5.6-luna` or a specific model, reasoning effort, or speed."
  - 초안 L69가 4개 프리셋·기본값·Sol medium·Advanced의 `gpt-5.6-luna` 예시까지 전부 옮겼다 ✅
  - 초안의 해석("프리셋 이름만 보면 성능 다이얼 같지만, 실제로는 세 축을 묶어둔 단축키")은 원문의 "a specific model, reasoning effort, or speed"와 정확히 대응 ✅
- `--model` / `-m` 별칭 ✅, `codex exec -m …`로 비대화형에도 적용 ✅ — 전역 플래그 표 `--model, -m`(`web-2.md` L3355)과 일치

#### ④ FR-1 은퇴 문안 적용 — **✅ 완전 준수 (문자 단위 일치)**

- 초안 L95가 **FR-1의 채택 문안과 문자 단위로 동일하다** ✅:
  > `gpt-5.4`·`gpt-5.4-mini`는 **2026-08-31 은퇴 예정**이다(ChatGPT 로그인 사용자 한정 — API 키 인증은 영향 없음). 대체는 각각 Terra·Luna. **2026-08-02 문서 기준으로는 아직 은퇴 전이다.** 이 책을 읽는 시점에는 이미 지난 날짜일 가능성이 높으므로, 은퇴 여부가 아니라 **대체 경로**를 기준으로 읽어라.
- **과거형 서술 0건** ✅ (전 장 스캔 — "은퇴했다"·"이미 은퇴한"·"지난 8월" 미검출)
- 절 제목 "8월 31일에 **사라지는** 두 모델" ✅ 미래형 프레이밍
- 원문 인용 2건 verbatim ✅ (`codex__models.md` L355-362) — "GPT-5.4 and GPT-5.4 mini retire from Codex on August 31, 2026." / "If you sign in with ChatGPT, replace `gpt-5.4` with `gpt-5.6-terra` and `gpt-5.4-mini` with `gpt-5.6-luna` in saved configurations, custom agents, and scheduled tasks. The OpenAI API and Codex authenticated with your own API key aren't affected."
- **"셋으로 짚어줬다" 카운트 정확 ✅** — saved configurations / custom agents / scheduled tasks = 3 (FR-16 준수)
- ⭐ **레퍼런스 §3-1·§7-4 #1의 오류를 되돌리지 않았다** ✅ — FR-1이 가장 경계한 실패가 발생하지 않았다
- 보너스: "모델 이름이 사라지면 에러로 멈추거나 조용히 대체되거나 둘 중 하나인데 **어느 쪽인지는 문서가 말해주지 않는다**"(L106) — 없는 것을 없다고 적은 처리 ✅

#### ⑤ 규율 4 범위값 보존 + #28879 귀속 — **✅ 완전 준수**

- **표 2 (Plus 5시간 한도) — 6행 18셀 전건 일치 ✅** (`codex__pricing.md` L272-307)
  Sol `10-100` / Terra `25-200` / Luna `250-2,000` / GPT-5.5 `15-80` / GPT-5.4 `20-100` / GPT-5.4 mini `60-350`, Cloud chats·Code Reviews 전부 `Not available`
  - 캡션 "**원문 표 전체**" ✅ 정확 (원문도 6행)
  - ⭐ **범위를 단일 수치로 뭉개지 않았고, 뭉개면 안 되는 이유까지 적었다**(L129) — "이걸 단일 수치로 뭉개서 'Plus는 5시간에 Sol 100번'이라고 옮기면 그 순간 틀린 문장이 된다. **범위가 넓다는 사실 자체가 정보다**". 규율 4의 요구를 독자에게 넘긴 처리
  - 메시지당 평균 `5-40`도 "여덟 배 폭의 범위이므로 단일 값으로 읽지 말자"로 동일 처리 ✅
- **각주 verbatim ✅** — "The usage limits for local messages and cloud chats share a five-hour window. Additional weekly limits may apply."(L312-314). 초안이 "지갑은 하나"라는 함의와 "주간 한도" 둘 다 짚었다 ✅
- **[#28879] 귀속 ✅ 전건**
  - 메타데이터: 2026-06-18 / 👍 **362** / 💬 **210** / open ✅ (`community.md` L233)
  - 표 4의 3행 9셀 전부 원장 값과 일치 ✅ (57,112 / 3,645 / 9%→11% · 20,480 / 0 / 45% · 23,839 / 0 / 77%)
  - **대안 가설 배제 4종 ✅** (리즈닝 강도 · 컨텍스트 팽창 · 설정 변경 · 주간 캡) — 원장 L244와 1:1
  - ⭐ **귀속 문안이 원장 요구와 정확히 일치** — `web-6.md` L1248이 "반드시 '커뮤니티 관측·주장'으로 귀속하고 공식 확인 불가를 병기할 것. 판정 등급 ⚠️"라고 요구했는데, 초안 L183이 **"커뮤니티 관측이며, 1차 소스로 확인 불가"**로 못 박고 "요율이 실제로 바뀌었다고 단정하지도, 착각이라고 일축하지도 않는다"로 양방향을 닫았다
  - 표 4 캡션에도 "커뮤니티 관측, 공식 문서로 확인 불가" ✅
- **확인 불가의 구조적 근거를 먼저 세운 구성 ✅** — `/codex/pricing` 단일 소스 + 변경 이력 없음 / `/codex/enterprise/usage-limits`에 수치 0개. 후자는 원장(`web-6.md` L1220)이 "전문이 **37줄**"이라 적었고 초안은 "**마흔 줄이 안 되고**"로 **하한 서술** ✅ FR-9 모범
  - 인용 verbatim ✅ "These controls aren't a universal Codex limit system and don't govern OpenAI API Platform billing."
- [#34035] 2026-07-18 / 👍 131 / open ✅ + "요구가 존재한다는 사실 자체가 그런 기간이 있었음을 **시사**하지만, 그 역시 문서로는 확인되지 않는다" ✅ — 원장 L251("시사한다")의 강도를 그대로 유지
- "5x or 20x higher rate limits" vs "materially inconsistent" ✅ (원장 L426)

#### ⑥ 인용 금지 9건 미사용 — **✅ 전건 확인**

- 7·8·9장 전체 스캔 결과 **검출 0건** — dev.to 65% 설문 / "2.2배" 벤치마크 / 세션 6,852건 / SWE-Lancer / Terminal-Bench 구체 순위 / Threads(qjc.ai) / SEO성 정리 콘텐츠 / velog 토큰 비교 / `/codex/overview` UI 삽화 문자열
- ⭐ **Terminal-Bench 처리가 특히 정확하다**(L201) — "다만 이 책은 **구체 순위나 점수를 옮기지 않는다.** 리더보드는 상시 갱신되고, 종이에 박힌 순위는 인쇄되는 순간 낡기 시작한다." 금지를 지키면서 **금지의 이유까지** 적었다. 원장 `papers.md` L94가 권한 처리("구체 순위 대신 링크와 …정도로만")를 초과 이행
- Terminal-Bench 메타데이터 ✅ — **Merrill** 등(제1저자 Mike A. Merrill), **ICLR 2026**(✅ peer-reviewed), **arXiv:2601.11868** ✅. 과제 구성 서술(고유 컨테이너 환경 + 사람이 작성한 정답 풀이 + 검증 테스트)도 원장 L92와 1:1 ✅. Codex CLI 공식 지원 ✅

#### ⑦ Fast 모드 배율 — **✅ 3개 수치 전건 일치**

`codex__agent-configuration__speed.md` L14-26 원문 대조:
- **속도 1.5배** ✅ ("increases supported model speed by **1.5x**")
- **GPT-5.6·GPT-5.5 = 2.5배** ✅ / **GPT-5.4 = 2배** ✅ ("GPT-5.6 and GPT-5.5 consume credits at 2.5x the Standard rate; GPT-5.4 consumes credits at 2x the Standard rate.")
- `/fast on`·`/fast off`·`/fast status` ✅ / `service_tier = "fast"` + `[features].fast_mode = true` ✅ / 데스크톱·CLI·IDE + ChatGPT 로그인 ✅ / API 키면 API 토큰 가격, 크레딧 배율 미적용 ✅
- 초안 L89의 요약("급할 때 1.5배 빨라지는 대신 2.5배를 낸다")이 GPT-5.6 기준으로 정확 ✅

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. Pro의 `$100`↔5x / `$200`↔20x 매핑은 문서에 없다 (L116)

- **원문이 말하는 것:** `subtitle="Choose 5x or 20x higher rate limits than Plus."` / `priceEyebrow="From"` `price="$100"` / "Unlimited ChatGPT Voice on the **$200/month tier**" / 한도 표의 탭 이름 **`Pro 5x`**·**`Pro 20x`**
- **원문이 말하지 않는 것:** 어느 금액이 어느 배수인지. 네 조각을 합치면 `$100`=5x, `$200`=20x가 거의 확실하지만 **문서가 그렇게 적지는 않았다.**
- **판정 근거:** 원장이 이 대응을 **반박하지 않고 침묵한다.** 모순이 아니라 부재이므로 ❌가 아니라 ⚠️(출처 없음)다. 다만 **규율 4가 이 책에서 가장 엄한 규율**이고, 이 장 자체가 "확인 가능한 것과 불가능한 것의 경계를 긋는 데 후반부를 쓴다"(L9)고 선언했으므로 추론을 사실처럼 두는 것은 자기 기준에 못 미친다.
- **수정안 (택1):**
  - **A안(권장 — 추론을 지운다):** "Pro는 `From $100`이고 `$200`/월 단계가 따로 있다. 문서는 Pro를 'Plus 대비 5배 또는 20배 한도'라고만 적고, **어느 금액이 어느 배수인지는 밝히지 않는다.**"
  - **B안(추론을 보이게 한다):** "…`$100`과 `$200` 두 단계이고, 한도 표는 `Pro 5x`·`Pro 20x` 두 탭으로 갈린다. **금액과 배수의 대응은 문서에 명시돼 있지 않다.**"
- A안을 쓰면 뒤의 "확인 불가" 절과 논지가 오히려 강해진다.

#### ⚠️-2. 표 4가 원장 4행 중 3행 발췌인데 "일부" 표기가 없다 (L173-179)

- 원장(`community.md` L237-242)의 로그 표는 **4행**이고, 초안은 `06-12 06:54`(79,961 / 5,125 / 15%→16%) 행을 뺐다.
- **값 왜곡은 없다** — 오히려 남긴 `06-12 06:51`(57,112)이 두 06-12 행 중 **작은 쪽**이라 대비를 보수적으로 만든다. 초안 L181의 "입력 토큰이 3분의 1로 줄고"도 57,112 → 20,480/23,839 기준으로 정확 ✅
- 다만 표 3 캡션이 "원문 표의 일부"라고 밝힌 것과 대비되어, 표 4만 발췌 표기가 없다. **FR-16 4항**에 걸린다.
- **수정안:** 캡션을 "…보고자가 제시한 세션 로그 비교(**4행 중 3행 발췌**) — 커뮤니티 관측, 공식 문서로 확인 불가"로.

### ✅ 확인됨 (47건 — 추가 근거 요약)

**모델 선택 (`codex__models.md`)**
- **"Codex offers three GPT-5.6 models: Sol for detail and polish, Terra as the everyday workhorse, and Luna for clear, repeatable work. If you are unsure, start with Sol." ✅ verbatim** L303-305
- 3모델 설명 ✅ L309-319 — Sol의 "For narrower tasks, define what done looks like"(초안 "범위가 좁은 작업에 Sol을 쓸 때는 무엇이 완료인지 정의해두라") ✅ / **"It is a natural starting point for work you previously gave GPT-5.5." ✅ verbatim** / Luna의 4작업(추출·분류·변환·구조화된 요약) ✅
- ⭐ **역량·속도 눈금 방향 ✅ 실측 확인** — 아이콘 개수를 직접 셌다: 역량 Sol **5** > Terra **4** > Luna **3**, 속도 Sol **2** < Terra **3** < Luna **4**. 초안 L29의 "Sol에서 Luna로 갈수록 역량은 내려가고 속도는 올라간다" ✅
- Codex-Spark ✅ — "Text-only research preview model optimized for near-instant, real-time coding iteration. Available to ChatGPT Pro users."(L262) + **별도 사용 한도 + 출시 시점 API 미제공** ✅ (`web-1.md` L592: "isn't available in the API **at launch**" / "governed by a **separate usage limit** that may adjust based on demand"). 초안의 "출시 시점에는"이 `at launch`의 정확한 번역 ✅
- Fast 모드와 Spark를 구별한 서술 ✅ (설정 vs 별개 모델 선택지)

**표 1 표면별 가용성 — 4행 28셀 전건 일치 ✅**
- `codex__models.md`의 `ModelDetails` `features` 배열을 모델별로 직접 읽어 대조. **Sol만 `Codex cloud: true`**, Terra·Luna·Spark는 `false` ✅. Spark는 web·credits·API도 전부 `false` ✅
- 이전 세대(GPT-5.5 등)도 cloud만 false ✅ — 초안 L48 "클라우드만 막혀 있고 나머지는 열려 있다"
- **"Currently, you can't change the default model for Codex cloud chats." ✅ verbatim** (1장과 동일 근거, 표기 일관)
- 초안의 결론("표면 선택이 곧 모델 선택인 셈이다", "무엇을 시킬 것인가보다 어디서 시킬 것인가가 먼저다") — 표에서 직접 따라오는 추론 ✅

**추론 강도**
- **"Use the lowest reasoning effort that produces the result you need. Increase it for tasks that need more planning, analysis, or checking." ✅ verbatim** L322-323
- 값 이름 ✅ — Light(앱·웹·IDE) / **Low(CLI)** / Medium / High / Extra High, 각각의 용도까지 원문과 1:1 (L325-330)
- **"There is no exact mapping from GPT-5.5 reasoning efforts to GPT-5.6. Try a familiar task at a lower setting and adjust based on the result." ✅ verbatim** L331-332
- Max / Ultra ✅ L336-342 + **"Most tasks do not need Max or Ultra." ✅ verbatim**. Ultra가 서브에이전트로 병렬 처리한다는 것도 원문 ✅
- ⭐ **FR-6·FR-7 준수 ✅** — "설정 레퍼런스 페이지를 정전으로 삼고, 서브에이전트 페이지에만 등장하는 `ultra`·`max` 표기는 그 페이지의 표기로 따로 취급하자"(L81). FR-6의 정전 지정과 FR-7의 "해석하지 말고 병기"를 둘 다 이행

**한도 초과 대응 (`codex__pricing.md` L729-741) — 3항목 전건 ✅**
- 진행 중 턴은 fair use 안에서 계속 ✅ / Plus·Pro는 플랜 업그레이드 없이 크레딧 추가 구매 ✅ / **"If you are approaching usage limits, you can also switch to a smaller model to make your usage limits last longer." ✅** — 초안 L139의 "공급자가 직접 '작은 모델을 쓰라'고 적어둔 셈"이 정확
- 이미지 생성 ✅ **"3-5x faster on average"**(L750-752) — 초안 "평균적으로 같은 한도를 3~5배 빠르게" ✅ 범위 보존

**벤치마크 절**
- SWE-Bench+ ✅ — Aleithan 등, **arXiv:2410.06992**, 2024, 📄 preprint ✅ / **32.67%** ✅ / **12.47% → 3.97%** ✅ / SWE-bench Verified에도 남아 있다 ✅ (`papers.md` §1-2). "3분의 1 토막" 산술 ✅
- SWE-Bench Pro ✅ — Deng 등, **arXiv:2509.16941**, 2025, 📄 preprint ✅ / GPT-5 공개 **23.3%** · 상업 **14.9%** ✅ / "프런티어 모델도 Pass@1이 25%에 못 미친다" ✅ (`papers.md` §1-6)
- **식별자 점검:** 2410.06992(2024-10) · 2509.16941(2025-09) · 2601.11868(2026-01) — 3건 모두 형식 정상, YYMM이 빌드 시점 과거 ✅
- [#32806] ✅ — 1.05M 광고 / 353K → 258K / **closed** ✅ + **"닫혔다는 사실이 곧 회복을 뜻하지는 않으므로, 이 책은 여기까지만 적는다"** — 원장 L427("closed — 회복 여부 확인 필요")의 유보를 그대로 유지 ✅
- 컨텍스트 예산 3연작 완결(6장 2% → 8장 분모 → 11장 MCP) ✅ 계획과 일치

**표 5 (작업 유형별 가이드)**
- ⭐ **"이 표는 앞 절들의 기준을 종합한 판단 가이드이며, 공식 문서에는 이런 표가 없다"(L207) ✅** — 저자 종합임을 명시했다. FR-16 4항의 정신을 표 전체에 적용한 처리
- 6행의 크레딧 값이 표 3과 정합 ✅ / 클라우드 행의 "Sol (선택 불가)" ✅ / Spark 행의 "Pro 한정 · 로컬 3개 표면" ✅

**미해결 고지 (클로징)**
- 4항목 전부 실제로 원장에 없는 것들이다 ✅ — 5시간 범위의 근거 / 주간 한도 값 / 2026-06 요율 변화 / 광고 대비 실측 컨텍스트
- **"이것들은 이 책이 게을러서 비워둔 자리가 아니라 1차 소스가 존재하지 않아서 비워둔 자리다"** — 계획의 클로징 기법('미해결 고지형')과 정확히 일치하며, ⚠️ 판정 항목을 본문에서 스스로 고지한 형태 ✅

### 규율 준수 메모 (판정 아님)

- **FR-1:** 완전 준수 (위 판정 ④). 이 책에서 가장 위험한 시제 함정을 통과했다
- **FR-2:** `(2026-08-02 문서 기준)` 4회 — 전부 **수치 표 캡션**(표 1·2·3)과 본문 1회. 문언 부합 ✅
- **FR-3 / 규율 12:** Claude Code 언급 **0건** ✅
- **규율 4:** 완전 준수 — 범위값 6쌍을 모두 범위로 유지, 커뮤니티 한도 주장을 확인 불가로 귀속 ✅
- **규율 6·11:** 위반 없음 ✅
- **🕒 0건인 이유:** 이 장은 가장 빨리 낡는 영역인데, 본문이 **"요금과 한도는 이 책에서 가장 빨리 낡는 영역이므로, 표를 외우는 대신 자기 계정의 사용량 화면과 이슈 번호를 직접 열어보는 쪽을 권한다"**(L187)로 스스로 신선도 경고를 달았다. 3장에서 세운 문형의 가장 강한 적용 사례다

---

## 09장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/09_draft.md`(스타일 반영본) · 구체 주장 44건 추출

**집계: ✅ 42 / ❌ 0 / ⚠️ 2 / 🕒 0**

### 저술가 명시 요청 판정 (5건)

#### ① Local·Worktree·Cloud 3모드 — 계획의 3분법을 원문 기준으로 교정한 서술 — **✅ 교정이 옳다**

- **원문 근거:** `research/web-3.md` L168-176 (`/codex/environments/modes`, 추출 충실도 `[원문]` — 짧은 페이지라 사실상 전문 회수)
  - Local — "work directly in your current project directory." ✅ verbatim
  - Worktree — "isolate changes in a Git worktree." ✅ (원문 뒤의 "Learn more."는 UI 문구라 뺀 것이 옳다)
  - Cloud — "run remotely in a configured cloud environment." ✅ verbatim
- ⭐ **핵심 교정이 원문에 직접 근거한다.** 초안 L17의 "**Local과 Worktree는 둘 다 내 컴퓨터에서 돈다. 원격으로 나가는 것은 Cloud뿐이다**"는 원장 L176의 "**Local과 Worktree 챗은 둘 다 사용자 컴퓨터에서 실행된다. Cloud만 원격 실행이다**"와 정확히 일치 ✅
- 초안이 여기서 한 걸음 더 나간 해석("이 3지선다는 '어디서 실행하나'와 '파일을 어떻게 격리하나'라는 서로 다른 두 축이 한 줄에 접힌 형태")도 세 정의문에서 직접 따라온다 ✅
- **비대화형을 "축이 다른 네 번째 경로"로 분리한 처리 ✅** — `codex exec`는 `/environments/modes`의 3지선다에 없으므로, 같은 층에 넣지 않고 축을 달리한 것이 정확하다
- 원장 주의사항도 지켰다 ✅ — "**비교표는 이 페이지에 없다**"(L177)이므로 초안이 3모드 비교표를 만들지 않고 산문 + 결정 흐름도로 처리한 것이 맞다

#### ② `experimental` 명령 7개 직접 카운트 — **✅ 확인됨 (FR-16 모범)**

- **직접 카운트:** `research/web-2.md` L3379-3394의 Command overview 복원 표에서 `experimental` 라벨 행을 직접 셌다 → **7개**
  `codex app-server` · `codex remote-control` · `codex debug app-server send-message-v2` · `codex debug models` · `codex debug prompt-input` · `codex cloud` · `codex execpolicy`
- 초안 L170-177의 목록과 **7개 전부 일치** ✅ (순서까지 동일)
- 초안 L178 "나머지 서브커맨드는 `stable`이다" ✅ — 28 − 7 = 21, `01_reference.md` §2-2의 "나머지 21개는 `stable`"과 정합
- 등급 정의 인용 ✅ — "Unstable and OpenAI may remove or change it." / **"Use at your own risk."** (1장 표 3과 동일 근거, 표기 일관)
- `codex app-server`의 "may change without notice" ✅ (2장과 동일 근거)
- ⭐ **1장의 미수금 회수가 정확하다** — 1장은 "정의표는 있는데 명단이 없다"로 개념만 짚고 목록을 9장에 넘겼는데(m5 분담), 여기서 그 목록이 나오고 **"라벨은 기능 소개 페이지에서는 각주처럼 보이지만, 자동화 설계도 위에서는 의존성의 수명 예고로 읽힌다"**(L182)로 회수 이유까지 댔다. 규율 8("4단계 체계를 쓴다"는 과잉 일반화 금지)도 준수 — "성숙도 라벨은 변경 가능성에 대한 예고이지 품질 등급이 아니다"(L184)

#### ③ 붙는 자리 표 8행 — **✅ 8행 직접 카운트, 셀 전건 대조 통과**

| 진입점 | 대조 결과 | 근거 |
|---|---|---|
| `codex exec` | Git 저장소 요구 + `--skip-git-repo-check` 우회 ✅ | `web-3.md` L1079·플래그 표 |
| GitHub Action | `openai-api-key` 시크릿 / Linux·macOS 러너 / **Windows는 `safety-strategy: unsafe`** ✅ | L982·L1049 |
| `@codex` PR 코멘트 | GitHub 연결 / 클라우드 ✅ | L1418 계열 |
| Slack | Slack 앱 + GitHub 연결 / **Plus·Pro·Business·Enterprise·Edu + 환경 1개 이상** ✅ | **L1379 원문과 1:1** |
| Linear | Linear 커넥터 / **트리아지 규칙 시 이슈 작성자 계정** ✅ | **L1426 verbatim** |
| Remote(모바일·SSH) | 연결된 호스트에서 실행 / **설정은 모바일 앱에서만** ✅ | L1457 |
| 통합 터미널 | 데스크톱 앱 전용 / 로컬 ✅ | 앱 문서 |
| Amazon Bedrock | `model_provider = "amazon-bedrock"` / **데스크톱·IDE는 `~/.codex/.env` 필요** ✅ | **L1542 원문 함정 그대로** |

- **8행 = 직접 카운트 8개** ✅
- **Linear 규정 verbatim ✅** — "Linear assigns new issues that enter triage to Codex automatically. When you use triage rules, **Codex runs chats using the account of the issue creator**."(L1426). 초안 L154의 "이슈 작성자의 계정으로 실행된다" + "감사 추적 관점에서 무게가 있는 규정" ✅
- **환경 자동 선택 함정 ✅ 2건 모두 원문** — Slack(L1387)·Linear(L1418) 공통: "selects the one that **best matches** your request. If the request is ambiguous, it **falls back to the environment you used most recently**." 초안 L150이 "가장 최근에 쓴 환경"까지 옮겼고, 문서 자신이 트러블슈팅으로 인정한다는 점과 `@Codex fix the above in openai/codex` 형태의 대응까지 ✅
- **Remote 인용 verbatim ✅** — "Remote access uses the connected host's projects, chats, files, credentials, permissions, plugins, Computer Use, browser setup, and local tools."(L1457). 초안의 결론("실행 위치가 하나 늘어나는 게 아니라 기존 실행 위치에 붙는 원격 조작 창구다") ✅
- **GitHub Action 보안 ✅ 전건** — 잡 2분할(`contents: read` + API 키 없는 별도 잡, L996·L1071) / `safety-strategy` 기본값 **`drop-sudo`** + 잡당 되돌릴 수 없음(L1049·L1058) / **"Run Codex as the last step in a job so later steps don't inherit state changes." ✅ verbatim**(L1068) / `codex-version` 입력(L1047)
- **비대화형 인증 경고 verbatim ✅**(L1171) + `CODEX_API_KEY=<키> codex exec …` ✅ + **"`CODEX_API_KEY` is only supported in `codex exec`." ✅**(L1176)

#### ④ 클라우드 네트워크·시크릿 — **✅ 확인됨 (단계별 권한 분리 정확)**

- **"Tasks delegated to the cloud run in isolated environments. Internet access is off during the agent phase unless you enable it for the environment." ✅ verbatim** (5장 §2-5와 동일 근거, 표기 일관)
- 단계별 구분 ✅ (`web-3.md` L257-259) — 셋업 단계 인터넷 있음 / **에이전트 단계 기본 OFF** / **모든 아웃바운드는 HTTP/HTTPS 프록시 경유**
- **표 2 (변수 vs 시크릿) ✅** — Environment variables는 chat 전 기간, **Secrets는 셋업 스크립트에서만이고 에이전트 단계 전에 제거 + 추가 암호화** ✅
- ⭐ 초안 L105의 원리 서술("인터넷을 끊는 것과 같은 발상이다 — 에이전트가 실행되는 순간의 권한 표면을 최소로 줄인다")이 원장 L261의 분석("**에이전트가 실행되는 순간의 권한 표면을 최소화**")과 정확히 대응 ✅
- 5장에서 미뤄둔 진리표의 나머지 절반을 여기서 회수한 구성 ✅ (계획의 분담대로)
- 클라우드 실행 순서 6단계 ✅ / 자동 셋업 대상(npm·yarn·pnpm·pip·pipenv·poetry) ✅ / **컨테이너 캐시 최대 12시간**("up to 12 hours", L252) ✅ / 셋업 스크립트·변수 변경 시 무효화 ✅ / Business·Enterprise는 캐시 공유 ✅ / `openai/codex-universal` ✅ (1장 표 2와 정합)
- `codex cloud` 계열 ✅ — `codex cloud` 선택기 / `codex cloud exec --env {ENV_ID} --attempts 1-4` / `codex cloud list --limit 1-20` / `codex apply {TASK_ID}` (`01_reference.md` §2-5와 일치, **범위값 `1-4`·`1-20` 보존** — 규율 4 준수 ✅)

#### ⑤ 이슈 번호·상태 — **✅ 확인됨**

- **[#28190]** 2026-06-14 / 👍 **79** / open ✅ (`community.md` L202·L455)
  - 원인 규명 ✅ — 번들 바이너리의 `com.apple.quarantine` xattr, 매 호출마다 macOS 검증 경고(L203)
  - 해결책 `xattr -d com.apple.quarantine …` ✅ (L204)
  - ⭐ **반박 인용 ✅ verbatim** — "the issue still occurs in ghostty. it is not a fix"(L205). 초안 L82의 "**터미널을 바꿔봐야 소용이 없다**"가 원장의 판정("터미널 교체는 해결책이 아니다")과 일치. 스레드 노이즈를 걸러낸 처리가 정확
  - 🕒 고지 ✅ "이 항목은 커뮤니티 보고이므로 상태가 바뀔 수 있다. 번호를 열어 현재 상태부터 확인하자"
- ⚠️ 반박 인용자 이름·날짜 누락은 ⚠️-2로 분리
- **[#34301]은 이 장에 등장하지 않는다** — 6장 서브에이전트 후속 이슈였고, 9장 범위 밖이다. 누락이 아님 ✅

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. "앞의 넷 중" — 표 3과 대응하지 않는다 (L148)

- **초안:** "표를 세로로 훑으면 축이 두 개 보인다. … **앞의 넷 중** `codex exec`와 통합 터미널·Bedrock은 내 컴퓨터에서 돌고, Slack·Linear·PR 멘션은 클라우드로 나간다."
- **문제:** `codex exec`는 표 3의 **1행**, 통합 터미널은 **7행**, Bedrock은 **8행**이다. "앞의 넷"에 들어가지 않는다. 앞의 넷(`codex exec`·GitHub Action·PR 코멘트·Slack)이라면 오히려 뒤 절의 분류와 어긋난다.
- 문장 앞부분(축 두 개)과 뒷부분(로컬/클라우드 분류)은 **둘 다 표와 맞는다.** "앞의 넷 중"만 잔여물로 남은 형태다.
- **수정안:** "여덟 줄 가운데 `codex exec`와 통합 터미널·Bedrock은 내 컴퓨터에서 돌고, Slack·Linear·PR 멘션은 클라우드로 나간다."
  (GitHub Action은 Action 러너, Remote는 연결된 호스트라 어느 쪽도 아니므로 두 목록에서 빠진 것은 정확하다)

#### ⚠️-2. ghostty 반박 인용에 화자·게시일이 없다 (L82)

- 이 장의 다른 커뮤니티 인용 3건(ModernMech 2026-07-26 / tunesmith 2026-06-13 / knuckleheads 2026-06-09)은 **전부 계정명 + 게시일**을 달았다. 이 인용만 "그 제안에 대해 …라는 반박이 붙어 있다"로 익명 처리됐다.
- 원장에 화자가 있다 — **backnotprop** (`community.md` L205).
- 규율 9(커뮤니티 인용은 진영·게시일 병기) 일관성 문제다.
- **수정안:** "그 제안에 대해 backnotprop이 남긴 반박이 붙어 있다 — \"the issue still occurs in ghostty. it is not a fix\"." (원장에 게시일이 없으면 계정명만이라도)

### ✅ 확인됨 (42건 — 추가 근거 요약)

**비대화형 (`codex exec`)**
- **"Non-interactive mode lets you run Codex from scripts (for example, continuous integration (CI) jobs) without opening the interactive TUI. You invoke it with `codex exec`." ✅ verbatim** (L1079)
- **쓸 자리 4가지 ✅ 원문 4불릿과 1:1** (L1081-1085) — 파이프라인 한 단계 / 다른 도구로 넘길 출력 생산 / 명령 출력을 물리고 다시 넘기는 CLI 워크플로 / 샌드박스·승인을 미리 못 박은 실행. **FR-16 카운트 정확**
- 기본값 read-only ✅ / `--sandbox workspace-write` ✅ / **"Use `danger-full-access` only in a controlled environment (for example, an isolated CI runner or container)." ✅ verbatim**(L1120) — 초안 L27의 "격리된 CI 러너나 컨테이너 같은 통제된 환경에서만"이 정확한 번역
- **"While `codex exec` runs, Codex streams progress to `stderr` and prints only the final agent message to `stdout`." ✅ verbatim**(L1091) + `| tee release-notes.md` 예시가 **원문 예시와 동일** ✅
- stdin 규약 ✅(L1099) — "Codex treats the prompt as the instruction and the piped content as additional context"
- `--json` JSON Lines + 이벤트명 ✅ — `thread.started`·`turn.started`·`item.*`·`turn.completed` 전부 원문 이벤트 목록 안(L1126). 초안이 "같은 이벤트가"라 적어 완전 열거를 주장하지 않았다 ✅
- `--output-schema` ✅ / `--ephemeral`·`--ignore-user-config`·`--ignore-rules` 3종 의미 ✅ 플래그 표와 1:1 / `codex exec resume --last` ✅
- ⭐ 초안 L37의 경고("뒤의 둘은 CI에서 내 로컬 설정이 섞여 들어오는 문제를 끊을 때 쓰지만, **6장에서 CI에 걸자고 한 규칙까지 함께 꺼진다**")는 `--ignore-rules`의 정의에서 직접 따라오는 실무 함의 ✅ 장 간 연결이 정확
- Git 저장소 요구 + `--skip-git-repo-check` ✅ + 3장 습관과의 연결 ✅

**워크트리 (`/codex/environments/git-worktrees`)**
- 용어 3종 verbatim ✅(L270-272) — Local checkout / Worktree / **Handoff: "The flow that moves a chat between Local and Worktree. Codex handles the Git operations required to move your work safely between them."** 초안 L58의 인용이 **용어 정의 절 원문과 문자 단위 일치** ✅
- 왜 쓰는가 3가지 ✅(L273-276) / 시작 절차 + **detached HEAD 기본** ✅(L280)
- 셋업 스크립트 이유 인용 ✅ — "your project might not be fully set up and might be missing dependencies or files that aren't checked into your repository."
- **표 1의 5행 전건 일치 ✅**(L288-295) — `$CODEX_HOME/worktrees` / Settings > Worktrees > Worktree root / `.worktreeinclude`(`.env`·`.env.local`·`config/secrets.json`) / **`AGENTS.override.md` 자동 복사** / **`.git` 공유**
- **"Codex keeps your most recent 15 Codex-managed worktrees." ✅** → "최근 15개까지" ✅(L297)
- **"Git only allows a branch to be checked out in one place at a time." ✅ verbatim**(L299) + 실무 함의 ✅
- 7장 "흔한 실수" 5번과의 연결 ✅ / "둘 다 옳은 일을 하면서 결과는 망가진다"는 격리 필요성의 정확한 서술 ✅

**재현성 절**
- **ModernMech HN 2026-07-26 인용 verbatim ✅**(`community-2.md` L386) — 초안 L117이 원문 전문을 문자 단위로 옮겼다
- **등급 병기 ✅** — "익명 계정의 단일 보고이며, 공식 문서가 인정한 동작은 아니다. 그럼에도 인용할 값이 있는 이유는 **대조 조건을 스스로 명시했기 때문**이다"(L119). 원장 등급 `[익명 주장·확인 필요 — 대조 조건 명시]`와 정확히 대응
- 도출 원리 ✅ — "클라우드는 실행 환경이 공급자 소유라, 내 쪽 변경이 하나도 없어도 어제와 다른 도구가 될 수 있다"가 원장 L387의 분석과 일치
- tunesmith HN **2026-06-13** ✅ 루틴 4단계 ✅ (`community.md` L387)
- knuckleheads HN **2026-06-09** ✅ + 등급·시점 의존성 병기 ✅ (`community-2.md` L392)
- ⭐ **공백을 공백으로 보고한 처리 ✅** — "이 주제를 리서치하면서 확보한 클라우드 위임 성공 사례는 전부 커밋에서 MR 한 개 사이 크기였다. 몇 시간짜리 대형 위임을 끝까지 밀어붙인 1차 후기는 찾지 못했다. **그런 후기가 세상에 없다고 단정할 수는 없고, 이 리서치의 범위 안에서 공백이라는 뜻이다.**"(L127) — 원장 `community-2.md` L551("다만 '몇 시간짜리 위임'은 여전히 공백. 확보된 성공 사례는 전부 **커밋~MR 한 개 크기**")과 정확히 대응하며, **부재 주장의 범위를 스스로 한정**했다. FR-12가 요구한 태도의 모범

**그림 1 (위임 결정 흐름)**
- 5개 분기와 종착점이 본문에서 확인된 사실만 사용 ✅ — 비대화형이면 샌드박스·승인 사전 확정 / Cloud면 에이전트 단계 인터넷 기본 차단. 새 사실 도입 없음 ✅

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` L7 본문 1회 + 표 3 캡션 1회 = 2회 ✅ 문언 부합
- **FR-3 / 규율 12:** Claude Code 언급은 표 3의 `codex exec` 행 "(↔ `claude -p`)" **1건뿐이고 §1-5 범위 안** ✅. 2장 정전 표의 표기를 그대로 재사용 ✅
- **규율 6·11:** 위반 없음 ✅
- **규율 9:** 커뮤니티 인용 4건 중 3건에 계정명+게시일 ✅ (1건은 ⚠️-2)
- **🕒 0건인 이유:** #28190·`experimental` 라벨 두 곳 모두 "번호를 열어라"·"자동화에 넣기 전에 지금 라벨이 무엇인지 열어보자"로 휘발성을 고지했다 ✅

---

## 파(wave) 3 종합 — 오케스트레이터·저술가 통보

### BLOCKING 1건 (원고 확정 전 필수 해소)

| # | 장 | 항목 | 해소 방법 |
|---|---|---|---|
| 1 | 7장 | ❌-1 PinEnvironmental6395 인용 변조 — **`GPT-5` → `GPT`**(버전 표기 삭제) + `it's good` → `good` | 원문 그대로 복원 (문안 제시함) |

> 이 한 건이 BLOCKING인 이유는 단순 오타가 아니기 때문이다. **같은 장 L146이 독자에게 "버전과 시점 없는 서술을 믿지 말라"는 규율을 넘기는데, 그 장의 대표 인용에서 버전 표기가 지워졌다.** 고치지 않으면 장의 논지가 자기모순이 된다.

### 비블로킹 권고 6건

7장 ⚠️-1(`/codex/guides/best-practices` → `/codex/learn/best-practices`, 3곳) · 7장 ⚠️-2(xoStardustt 인용 끝 `…`) · 8장 ⚠️-1(Pro `$100`↔5x 매핑은 문서에 없음 — A안 권장) · 8장 ⚠️-2(표 4 캡션에 "4행 중 3행 발췌") · 9장 ⚠️-1("앞의 넷 중" → "여덟 줄 가운데") · 9장 ⚠️-2(ghostty 반박 인용자 backnotprop 병기)

### 파 3 총계

| 장 | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|
| 7장 | 38 | 1 | 2 | 0 |
| 8장 | 47 | 0 | 2 | 0 |
| 9장 | 42 | 0 | 2 | 0 |
| **합계** | **127** | **1** | **6** | **0** |

### 누적 (파 1+2+3, 9개 장)

| | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|
| 파 1 (1·2·3장) | 108 | 2 | 8 | 0 |
| 파 2 (4·5·6장) | 115 | 3 | 5 | 0 |
| 파 3 (7·8·9장) | 127 | 1 | 6 | 0 |
| **누적** | **350** | **6** | **19** | **0** |

**정확도 소견 — 최고 위험 장이 최저 오류율을 냈다.**

8장은 요금·한도·모델·은퇴가 한 장에 몰린 최고 위험 구간이었는데 **❌ 0건**이다. 수치 셀 31개를 원문과 전수 대조해 불일치가 없었고, 규율 4(범위값 보존)와 FR-1(은퇴 미래 시제)이 문자 단위로 지켜졌다. 파 2에서 관측한 "세기·옮겨 담기에서 틀린다"는 패턴이 **이번 파에서는 재발하지 않았다** — 오히려 8장 표 3 캡션의 "아홉 행"(실측 9), 9장의 `experimental` 7개(실측 7), 7장의 8불릿(실측 8), 9장 표 3의 8행 등 **직접 카운트가 요구된 자리 4곳이 전부 정확**했다. FR-9·FR-16이 작동했다고 본다.

대신 새 계열이 하나 드러났다 — **인용문 자체의 미세 변조**(7장 ❌-1). 파 1·2에서 verbatim 대조 109건 무결이었던 팀이, 처음으로 인용문 안의 단어를 바꿨다. 그리고 바뀐 단어가 하필 **모델 버전 표기**였다. 원문에 없는 것을 넣은 게 아니라 **있는 것을 지운** 형태라 눈에 덜 띈다. FR-19가 이 패턴을 겨눈다.

---

# 파(wave) 4 — 10·11·12장 (최종 파)

> 판정 기준: 파 1~3과 동일 + 누적 규율 **FR-1 ~ FR-22**.
> **앞 장 참조는 `{NN}_final.md` 기준(FR-18).** 파 1~3의 BLOCKING 6건이 final에 전건 반영된 것을 먼저 확인했다(아래 "선행 파 해소 확인").

## 선행 파 BLOCKING 해소 확인 (Phase 4 종료 기준 판정용)

| 파 | 장 | 항목 | final 확인 결과 |
|---|---|---|---|
| 1 | 1장 | "changelog 항목 95개" | ✅ **해소** — `01_final.md` L99 "2025년 5월부터 2026년 7월까지 **여든 건이 넘는** 항목" (A안 채택) |
| 1 | 1장 | 표 2 SDK 경로 | ✅ **해소** — L78 `openai/codex/codex-sdk` |
| 1 | 3장 | `(사실 확인 필요)` 마커 | ✅ **해소** — `03_final.md` L187 "…갈라 노출한 것이 **Codex의 방식이다**"(A안 채택), 마커 0건 |
| 2 | 4장 | "갱신 시점을 네 가지로" | ✅ **해소** — `04_final.md` L27 "**여러 갈래로** 구체화한다" + 5번째(GitHub PR 코멘트 `@codex`) 추가 (A·B 병합 채택) |
| 2 | 6장 | 표 1 `SYSTEM` 행 누락 | ✅ **해소** — `06_final.md` L39에 `SYSTEM` 행 추가 |
| 2 | 6장 | "가장 가까운 하나만" | ✅ **해소** — 해당 표현 0건, 대체 문단 반영 |
| 3 | 7장 | PinEnvironmental6395 인용 변조 | ✅ **해소** — `07_final.md` L44 "**GPT-5** is very good… — **it's good** at figuring out…" 원문 복원 |

비블로킹 권고도 확인되는 대로 반영돼 있다 — 7장 `/codex/learn/best-practices` 경로 정정(`guides/best-practices` 0건), 8장 Pro 배수 매핑 A안 채택(L116 "**어느 금액이 어느 배수인지는 밝히지 않는다**"), 9장 backnotprop 병기·"여덟 줄 가운데" 교정.

---

## 10장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/10_draft.md`(스타일 반영본) · 구체 주장 47건 추출

**집계: ✅ 45 / ❌ 0 / ⚠️ 2 / 🕒 0**

### 저술가 명시 요청 판정 (7건)

#### ① `gpt-5.6-sol` + `xhigh` 유일 권장 (FR-7) — **✅ 완전 준수**

- **원문 verbatim ✅** — "For the best scan quality, use `gpt-5.6-sol` with `xhigh` reasoning effort."(`web-4.md` L869). 원장이 "문서 6곳에서 동일 문장 반복"이라 적었고 초안은 "관련 문서 여러 곳에서 같은 형태로 반복된다"로 **수치를 쓰지 않았다** ✅ (FR-16의 정신 — 개수가 논지에 기여하지 않으면 쓰지 않는다)
- ⭐ **FR-7의 함정을 정확히 회피하고 독자에게 넘겼다** — FR-7은 "CLI 예시의 `gpt-5.6-terra`를 권장 모델로 서술하면 **오류**"라고 경고했는데, 초안 L192가 선제적으로 못 박는다: "**예시 명령줄에 다른 모델 이름이 보이더라도 그건 플래그 사용법을 보여주는 문자열로 읽어야 한다.** 8장에서 봤듯 모델 이름은 계열이 여럿이라 섞이기 쉬운 자리다."
- `--model`·`--effort` 플래그가 열려 있다는 사실과 "권하는 조합은 이것 하나뿐"을 분리해 서술 ✅ — 가능한 것과 권장되는 것을 섞지 않았다

#### ② 3버전 계열 (0.1.15 / 0.1.11 / 0.1.3) — **✅ 전건 일치**

- 호스티드 데스크톱 카탈로그 **`0.1.15`** ✅ / 공개 CLI 마켓플레이스 **`0.1.11`** ✅ (`web-4.md` L1199-1200 원문 인용 2건)
- CLI·SDK 패키지 **`0.1.3`**과 **별개 계열** ✅ (L1204·L1693) — 초안 L196의 "나란히 놓고 비교할 대상이 아니다. 계열이 다르기 때문이다"가 원장의 "모순이 아니다" 판정과 정확히 대응. **FR-6(문서 내부 불일치)의 응용** — 불일치처럼 보이는 것이 실은 별개 계열임을 밝힌 처리
- "어느 쪽에서 설치했느냐에 따라 쓸 수 있는 기능이 다르다" ✅ + "긴 스캔을 시작하기 전에 체인지로그를 확인하라" ✅
- 🕒 처리 ✅ — "여기가 이 장에서 가장 빨리 낡을 부분이다" + "자기 환경에서 직접 확인해야 할 항목의 목록으로 읽자"

#### ③ MCP `info` 읽기 전용 한정 — **✅ verbatim**

- "**MCP exposes only the read-only `info` metadata command. Scans, exports, authentication, validation, and patching remain CLI-only.**"(`web-4.md` L1383) ✅
- ⭐ **초안이 이 인용으로 자기 앞 문단을 반박하는 구성이 정확하다** — L204에서 `codex-security mcp`·`skills`·`--llms`를 들어 "부품으로 편입되도록 설계된 것처럼 읽힌다"고 세운 뒤, L208의 원문으로 범위를 좁힌다. 그리고 **"'MCP를 통해 다른 에이전트가 스캔을 돌릴 수 있다'고 쓰면 사실과 어긋난다"**(L210)로 오독을 명시적으로 차단했다
- 부품화의 실제 경로를 스킬 동기화로 정정 ✅ — `$codex-security:security-scan` 등 스킬 이름도 원장과 일치

#### ④ Ok_Economist3865 자기 반증 귀속 — **✅ (FR-19 준수 확인)**

- **r/codex, 2026-03-17** ✅ 진영·게시일 ✅ (`community-2.md` L28)
- **인용 verbatim ✅** — 90% → 25~40%, 역방향 무검출까지 원문 그대로
- ⭐ **FR-19 준수 ✅** — 인용문 안의 모델 세대 표기(`gpt 5.2 xhigh`, `opus 4.5/4.6`)가 **보존**됐고, 초안 L53이 **"인용문에 적힌 그대로"**라고 한 번 더 못 박았다. 파 3 7장 ❌-1(버전 표기 삭제)의 재발이 없다
- 3조건 병기 ✅ — 익명 커뮤니티 진술 / 특정 모델 세대 / 표본 1인
- 해석의 균형 ✅ — "통념의 절반을 깎는다"(L49)와 "통념이 통째로 무너지지는 않는다 … **역방향 비대칭은 그대로 남았다**"(L51)를 둘 다 적었다. 원장 L30의 판정("절반은 프롬프트 문제였다 + 남은 비대칭도 함께 기록")과 정확히 일치

#### ⑤ FAQ "세 번의 No" — **✅**

- SAST 대체 **No** ✅ verbatim("**No. Codex Security complements SAST.** It adds semantic, LLM-based reasoning and automated validation, while existing SAST tools still provide broad deterministic coverage.", `web-4.md` L1267)
- 수동 보안 리뷰 대체 **No** ✅ / 패치 자동 적용 **No** ✅ (L1275)
- 원장 L1290이 "**세 번의 No**"로 정리한 것과 초안 L85의 프레이밍이 동일 ✅
- ⚠️ 원장 L1289의 경고("데이터 보존 정책은 이 FAQ에 없다 — **추측 금지**")도 준수 ✅ — 초안에 보존 서술 0건

#### ⑥ 표 1 수명주기 7단계 · 표준↔딥 Scope 동일 — **✅**

- **7행 직접 카운트 ✅** (위협 모델 / 표준 스캔 / 딥 스캔 / 변경 리뷰 / 트리아지 / 수정·검증 / 내보내기·리포트)
- 캡션이 "**실무 수명주기**"라 원문 표라고 주장하지 않는다 ✅ — 실제로 문서에는 이런 표가 없고 초안의 재구성이다. L89가 그 사실을 밝힌다("페이지를 하나씩 따라가면 길을 잃으므로, **실무에서 밟게 되는 순서로 다시 세워보자**") ✅ FR-16 4항 준수
- ⭐ **표준 vs 딥 Scope 동일 ✅** — 원문 표(`web-4.md` L943-949)의 `Scope` 행이 양쪽 다 "Repository or explicit folder". 초안 L131의 "**딥 스캔은 더 넓게 보는 게 아니라 같은 범위를 더 파는 것**"이 정확한 독해다
- "can reduce variability between runs" ✅ / 위임 워커 필요 + 미충족 시 표준으로 폴백 ✅ / **"A deep scan never substitutes for the diff-focused workflow." ✅ verbatim**

#### ⑦ superfrank·bottlepalm·gregwebs 인용 verbatim·게시일 — **✅ 3건 전건**

| 인용자 | 초안 | 원장 | 판정 |
|---|---|---|---|
| superfrank | HN, **2026-05-15** | `community.md` L132-133 | ✅ 게시일·매체 일치, 인용 3문장 verbatim(앞뒤 문장 경계 절단) |
| bottlepalm | HN, **2026-07-08** | L134-135 | ✅ 인용 verbatim |
| gregwebs | HN 스레드, **2026-07-28** | L292-293 | ✅ 서술로 처리(거의 한 시간·Pro 주간 절반·HEAD 오류) 전건 일치 |

- 벤더 답변(dangelosaurus) verbatim ✅ L294 / arpinum **2026-07-29** ✅ L296 / 데이터 반출 벤더 확인 **2026-07-29** verbatim ✅ L299
- HN 스레드 메타 ✅ — 2026-07-28 / 596 포인트 / 댓글 227개 / 벤더 상주
- ⭐ **"출시 나흘째의 기록"이라는 전제 고지 ✅** — 원장(`01_reference.md` L876 "리서치 시점 기준 4일 차")과 일치하며, "초기 버그일 가능성이 높고, 지금은 달라졌을 수 있다"로 🕒을 본문에서 해소

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. 릴리스 간격 "2~5일" — 실측은 2~3일 (L198)

- **초안:** "2026년 7월 하순의 릴리스는 23일·25일·28일·30일에 나왔다. **2~5일 간격이다.**"
- **날짜 4개는 정확하다 ✅** — `web-4.md` L1208-1211: `0.1.12` July 23 / `0.1.13` July 25 / `0.1.14` July 28 / `0.1.15` July 30
- **간격 실측:** 23→25 = **2일**, 25→28 = **3일**, 28→30 = **2일**. 최대가 3일이다. 상한 `5`가 어느 쌍에서도 나오지 않는다.
  (직전 릴리스 `0.1.11`은 July 10이라 그 간격은 13일 — `5`와도 맞지 않는다)
- **수정안:** "**2~3일 간격이다.**"
- 이 문단의 논지("릴리스가 매우 잦다")는 2~3일 쪽이 오히려 더 강해진다.

#### ⚠️-2. 표 2 캡션 "(원문 그대로)"인데 의미 열이 번역문이다 (L145) — FR-10

- 판정명 3개(`confirmed`·`not_actionable`·`needs_review`)는 원문 표기 ✅. 그러나 "의미" 열은 원문 영문을 우리말로 옮긴 것이다.
- **FR-10:** "표 캡션이 '원문 표'라고 말하면 셀은 원문 문자열이어야 한다. 다듬고 싶으면 캡션에서 '원문 그대로'를 빼라."
- 번역 자체는 정확하다 ✅ (`web-4.md` L1064-1068과 의미 단위로 1:1)
- **수정안:** 캡션을 "표 2. 트리아지 판정 3종 (**판정명은 원문 표기**)"으로.

### ✅ 확인됨 (45건 — 추가 근거 요약)

**리뷰 세 입구**
- `/review` 스코프 4종(base 대비·커밋되지 않은 변경·특정 커밋·커스텀 지시) ✅ / `codex review`의 `--uncommitted`·`--base`·`--commit` **상호 배타** ✅ / `@codex review` + 범위 좁힌 요청 + `@codex fix the P1 issue` ✅
- **코드 리뷰 페이지가 웹·앱·CLI·IDE 네 표면별로 본문이 갈린다 ✅** — 초안 L25의 경고("어느 표면 이야기인지 확인하지 않고 읽으면 자기 환경에 없는 옵션을 찾게 된다")가 정확
- 설정 토글 2종(Code review / Automatic reviews) ✅ / GitHub CLI 인증 전제 ✅ / 분리형 리뷰 챗 모드 ✅
- 리뷰 페인 조작 입도 3층(전체 diff·파일·hunk) ✅
- `## Code Review Rules` 규칙 작성 지침 4구 ✅ **영문 원문 병기** — "Focus on consequential, repository-specific behavior" / "State the safe path or exception" / "Keep rules scoped and durable" / "Leave mechanical checks in CI" (4장과 동일 근거, 표기 일관)
- ⭐ **"필수 승인을 대체하지 않고, 테스트나 브랜치 보호를 대체하지도 않는다" ✅** — 리뷰 자동화 도입 시 기존 게이트를 걷어내지 말라는 경계 명시

**통념 검증**
- bungker GeekNews **2026-04-15** ✅ (`community.md` L136) — 한국어 1차 인용, 진영·게시일 병기 ✅
- **P0/P1 인용 verbatim ✅** — "models must be trained specifically to identify P0 and P1-level bugs, and tuned to provide concise, high-signal feedback; overly verbose responses are ignored just as easily as noisy lint warnings."(`web-6.md` L1566)
- 초안의 해석("리뷰 도구의 성능 지표가 '얼마나 많이 잡는가'가 아님을 벤더 문서가 스스로 적어둔 셈" / "등급을 나누는 목적은 **읽힐 양으로 줄이는 데** 있다") ✅ 원문 범위 내
- **"At OpenAI, Codex reviews 100% of PRs." ✅ + 단서 병기 ✅** — "출처 표기가 없는 벤더 자체 주장이고, 어떤 기준으로 셌는지도 밝혀져 있지 않다"(L63). 원장 `web-6.md` L1398이 수치만 싣고 근거를 안 붙인 것을 초안이 스스로 등급화했다 ✅

**두 제품 경계**
- 실행 보안 페이지의 분리 인용 verbatim ✅ (5장 §3-10과 동일 근거)
- Codex Security 정의 verbatim ✅ + 경로 4종(Codex 안·터미널·TypeScript SDK·연결된 GitHub) ✅ + npm `@openai/codex-security` ✅
- 클라우드 스캔 "currently in research preview" ✅ + 라벨 처리 규율 적용 ✅
- 접점 2개 ✅ — `--sandbox workspace-write` 필요 + "프롬프트가 여전히 체크아웃을 건드리지 말 것을 요구해야" ✅ / **"For best results, use an account verified for Trusted Access for Cyber."** 문서 4곳 반복 ✅ (뒤의 거절 사례와 연결한 구성이 정확)

**수명주기·판정 어휘**
- 위협 모델 정의·자동 생성·"결과가 어긋나면 가장 먼저 고칠 것" ✅ / 4항목(진입점·신뢰 경계·민감 데이터 경로·우선 검토 영역) ✅ / 예시 verbatim ✅
- `SECURITY.md` ✅ — 내용 5종 / **중첩 파일 + 코드에 가장 가까운 파일이 이긴다** ✅ (4장 지침 체인과의 대응이 정확) / `AGENTS.md`와의 역할 분담 ✅
- **"Codex Security treats these files as policy context, not executable instructions." ✅ verbatim** + 초안의 해석("남이 보낸 PR이 `SECURITY.md`를 고쳐 스캐너를 조종하는 경로를 막는다") ✅
- 표준 스캔 국면 7종 + "완결된 결과를 기다리라"는 경고 ✅
- **"AI-assisted scans can vary, even with the same scan configuration." ✅ verbatim** — 이 인용을 절 전체의 전제로 세운 구성이 정확
- finding 상태 **5종**(`new`·`persisting`·`reopened`·`resolved`·`unknown`) ✅ / 커버리지 **3등급**(`complete`·`partial`·`unknown`) ✅ (`web-4.md` L1485·L1592) — ⭐ **"두 목록 모두 마지막 칸이 `unknown`" + "'모른다'가 일급 값으로 들어 있다"**(L135)는 정확한 관찰
- 랭크 규약 ✅ verbatim 대응 — `1`부터 / **각 판정 큐 안에서 독립적으로** / 스캐너 심각도 점수 아님 / `not_actionable`은 순위 없음
- 트리아지 태도 ✅ — 입증되지 않은 주장 취급 / 반증 증거 함께 탐색 / 증명 공백 기록 / 중복도 병합 없이 입력 순서대로
- 입력 범위 ✅ + **"GitHub Issues는 기본 소스에 들어가지 않는다"** ✅
- **"If a regression test is unsafe or infeasible, Codex records the proof gap and provides the strongest repeatable validation artifact instead." ✅ verbatim** + "검증 성공이 finding을 자동으로 닫지 않는다" ✅
- 내보내기 승인 5단계 + **"정확히 같은 페이로드"** + 첫 불확실 지점에서 중단 + 다시 읽어 확인 ✅
- **"The result is a design portfolio, not a patch, and doesn't prove that it fixes a vulnerability." ✅ verbatim** + 작성 기준 "관측된 사실·추론·제안된 설계 속성 분리" ✅
- 클라우드 스캔 소요 시간 FAQ ✅ (몇 시간~며칠, 이후 증분으로 빨라짐)

**자동화 표 3 (4행)**
- CLI 단건 / 벌크 / CI / TypeScript SDK **4행 직접 카운트** ✅
- Node.js 22+ · Python 3.10+ ✅ / `--auth {auto,chatgpt,api-key}` ✅ / `--format toon|json|yaml|jsonl` ✅ / `CODEX_API_KEY` ✅ / 산출물 경로 ✅ / **CI에 마켓플레이스 플러그인이 없으므로 먼저 설치** ✅ / SDK 베타 접근 ✅
- `scan` 대상 플래그 상호 배타(`--path`·`--diff`·`--working-tree`) + `--head`↔`--diff` / `--base`↔`--working-tree` 짝 ✅ / diff·워킹트리는 Git 워크트리 루트 요구 ✅
- `--max-cost`·`--fail-on-severity` ✅ + "안전망으로 충분한지는 다음 절에서" 예고 → 실제로 회수 ✅

**클로징**
- FAQ 인용 verbatim ✅ — "Codex Security accelerates review and helps rank findings, but it does not replace code-level validation, exploitability checks, or human threat assessment." 계획의 클로징 기법('원문 인용으로 닫기' — 해설 없이 1차 소스 문장 하나로 끝낸다)을 정확히 이행 ✅

### 규율 준수 메모 (판정 아님)

- **FR-2:** `(2026-08-02 문서 기준)` 4회 — 본문 1(L77) + 표 1·3 캡션 2 + L196 버전 문단 1. 수치·원장형 표라 문언 부합 ✅
- **FR-3 / 규율 12:** Claude Code 고유 주장 **0건** ✅. 인용문 안의 `Claude`/`Opus`/`Fable`은 전부 커뮤니티 화자의 말이고 초안이 새로 정의하지 않았다
- **규율 6·11:** 위반 없음 ✅ / **규율 9:** 커뮤니티 인용 6건 전부 매체+게시일 병기 ✅

---

## 11장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/11_draft.md`(스타일 반영본) · 구체 주장 43건 추출

**집계: ✅ 42 / ❌ 0 / ⚠️ 1 / 🕒 0**

### 저술가 명시 요청 판정 (6건)

#### ① `experimentalApi` 게이팅 + 스레드/턴/아이템 3층 — **✅**

- **게이팅 인용 verbatim ✅** — "Some app-server methods and fields are intentionally gated behind `experimentalApi` capability."(`web-3.md` L791). 원문 뒤의 "Omit `capabilities` (or set `experimentalApi` to `false`) to stay on the stable API surface, and the server rejects experimental methods/fields."를 초안이 "켜지 않으면 서버가 실험 메서드를 거절한다"로 정확히 옮겼다 ✅
- ⭐ 초안의 실무 결론이 원문에서 직접 따라온다 — "자동화를 오래 굴릴 생각이라면 이 스위치를 **끈 채로** 설계하는 쪽이 안전하다. 켜야만 되는 기능이 있다면, 그 기능이 예고 없이 바뀔 수 있다는 뜻이기도 하다"(L45). 원문의 "stay on the stable API surface"를 뒤집어 읽은 것
- **3층 모델 ✅** — `web-3.md` L434의 app-server 섹션 구조가 실제로 **Threads / Turns / Items**로 갈린다(Start or resume a thread … / Start a turn … / Items / Item deltas). 초안 L43의 "스레드를 시작하거나 재개하고, 그 안에서 턴을 돌리고, 턴이 아이템을 만든다" ✅
- SDK의 `startThread`·`run`·`resumeThread`가 이 층에 대응한다는 서술 ✅ — SDK 예제 코드와 정합

#### ② MCP 옵션 기본값 — **✅ 원문 캐시 직접 대조, 전건 일치**

`research/codex-docs-raw/_config-reference-tables.md` L91-97에서 직접 확인:

| 초안 | 원문 | 판정 |
|---|---|---|
| `startup_timeout_sec` 기본 **10초** | "Override the **default 10s** startup timeout for an MCP server."(L91) | ✅ |
| `tool_timeout_sec` 기본 **60초** | "Override the **default 60s** per-tool timeout for an MCP server."(L93) | ✅ |
| `enabled_tools` 허용 목록 | "Allow list of tool names exposed by the MCP server."(L94) | ✅ |
| `disabled_tools` 거부 목록, **거부가 나중에 적용** | "Deny list **applied after `enabled_tools`** for the MCP server."(L95) | ✅ |
| `default_tools_approval_mode` = `auto`·`prompt`·`writes`·`approve` **4값** | `mcp_servers.<id>.default_tools_approval_mode`(L96) 동일 4값 | ✅ |

- ⭐ **키의 스코프를 정확히 골랐다** — 같은 이름의 키가 `apps.<id>.*`(L53·L58)와 `plugins.<plugin>.mcp_servers.<server>.*`(L230)에도 있는데, 초안은 MCP 문맥이므로 `mcp_servers.<id>.*`를 썼다. 원문 캐시 L96이 정확히 그 키다 ✅
- `writes`의 의미("읽기 전용으로 표시되지 않은 도구에만 승인을 묻는다") ✅ / 초안 L99의 결론("승인 축이 MCP 층에도 따로 하나 더 있는 셈") ✅ — 5장 3축과의 관계를 정확히 위치시켰다
- STDIO는 `command`+`args`, HTTP는 `url` ✅ / 인증 4종(`bearer_token_env_var`·`http_headers`·`env_http_headers`·OAuth) ✅

#### ③ access token "최단 하루" · 7/30/60/90일 (FR-6 정전 페이지 기준) — **✅**

- **"The shortest custom expiration is one day." ✅** (`web-5.md` L375, `/codex/enterprise/access-tokens`)
- 권장 유한 만료 **7·30·60·90일** ✅ 같은 행 / 만료 없음 선택 시 정기 교체 권고 ✅
- ⭐ **FR-6 정전 페이지 준수 ✅** — FR-6 표가 "access token 지원 플랜 → `access-tokens`(전용 페이지)"를 정전으로 지정했고, 초안 L152가 **그 페이지 원문을 인용**했다: "Codex access tokens are currently supported for ChatGPT Business and Enterprise workspaces." ✅ verbatim
- 관리자 **Access token expiration limit** ✅ + "새로 만드는 토큰에만 적용되며 기존 토큰은 자기 만료를 유지한다" ✅ verbatim 대응(L364)
- 초안 L154의 진단 시나리오("야간 파이프라인이 인증 오류로 멈췄다면, 조직이 상한을 조인 뒤 내가 토큰을 재발급한 시점을 의심") — 두 사실의 조합이며 원문 범위 내 ✅

#### ④ 네 지점 표의 최소 버전 열 — **✅**

| 지점 | 최소 버전 열 | 원장 | 판정 |
|---|---|---|---|
| 관리형 설정 | — | 버전 조건 없음 | ✅ |
| 권한 프로필 허용 목록 | Codex **`0.138.0` 이상**(이하 버전은 무시) | **"Permission-profile allowlists require Codex 0.138.0 or later. Codex 0.137.0 and earlier ignore `allowed_permission_profiles` and managed `default_permissions`."**(`web-5.md` L491) | ✅ verbatim |
| 워크스페이스 모델 가용성 | — | 버전 조건 없음 | ✅ |
| access token 정책 | **Business·Enterprise 워크스페이스** | `access-tokens` 원문 | ✅ |
- ⭐ **빈 칸을 `—`로 두고 억지로 채우지 않았다** ✅ — FR-17(빈칸은 "말할 수 없다"의 표시)의 응용
- 초안 L144의 해석("`0.137.0` 이하는 이 설정을 무시한다 … **양쪽이 서로 다른 규칙으로 도는 상황**")과 임시 호환 장치(`allowed_sandbox_modes`) 언급 ✅ — 5장 FR-8 근거와 정합
- 허용 목록의 화이트리스트 성격(존재하면 완전 목록 / `true`만 허용 / 생략·`false`는 거부 / 앞으로 추가될 내장 프로필까지 거부) ✅

#### ⑤ METR "2025년 8월 기준" · "주당 2~5시간 출처 미표기" 귀속 — **✅ 원장의 fact-checker 지시 4개 전건 이행**

`research/web-6.md` L1544-1551이 이 페이지에 대해 fact-checker 지시 4개를 남겼는데, 초안이 **넷 다 이행**했다.

| 원장 지시 | 초안 이행 | 판정 |
|---|---|---|
| ① "2시간 17분/50% 신뢰도"는 **METR 연구**이지 OpenAI 측정이 아니다. **"2025년 8월 기준"** 병기 필수 | L227 "이건 **OpenAI의 측정이 아니라 METR의 연구 결과**이고, 원문이 스스로 **2025년 8월 기준**이라고 못 박는다. 지금 시점에서는 한 해가 지난 값이다." | ✅ |
| ② "7개월마다 배증"으로 **현재 시점 외삽 금지** | L227 "그 배증률로 오늘 값을 계산해내는 것은 **문서에 없는 산수다. 그런 외삽은 하지 말자.**" | ✅ **독자에게 규율을 넘김** |
| ③ "주당 2~5시간"은 **출처 미표기** → "가이드의 주장"으로 귀속 | L229 "**출처가 표기돼 있지 않다.** 그러니 이 책은 이 값을 사실로 쓰지 않고, **이 가이드의 주장으로만** 옮긴다." | ✅ |
| ④ 페이지 전체가 마케팅 성격 — 기술적 사실의 근거로 쓰지 말 것 | L231 벤더 자체 주장 처리 + L233 **"관점을 빌리기에는 좋고 수치를 빌리기에는 나쁘다"** | ✅ |

- 수치 자체도 정확 ✅ — "2 hours and 17 minutes … roughly 50% confidence"(L1538) → "2시간 17분 … 약 50% 신뢰도"
- ⭐ **L233의 일반 기준이 이 책의 자산이다** — "문서가 자기 수치의 출처와 시점을 함께 적었는가. 적었다면 그대로 옮기고, 안 적었다면 '이 문서의 주장'으로 옮기자." **FR-20(침묵 vs 모순)의 독자용 판본**이다

#### ⑥ Pro 매핑 — 8장 final과의 정합 — **✅ 해당 서술 없음(정합 위반 없음)**

- 11장에는 Pro 요금·배수 서술이 등장하지 않는다. 8장 표 1의 모델 가용성 설계를 "조직 정책 아래에서 한 겹 더 걸린다"로 참조할 뿐이다(L148) ✅
- 8장 final이 A안을 채택해 배수 매핑을 제거했으므로, 11장이 그 매핑을 재도입하지 않은 것은 **장 간 정합 유지** ✅

### ⚠️ 정밀도 보정 (비블로킹)

#### ⚠️-1. MCP 커뮤니티 보고 3건에 진영(서브레딧) 표기가 없다 (L103·L105·L107) — 규율 9

- 세 보고 모두 **r/codex** 출신이다(`community-2.md` L454·L466·L484).
- 초안은 계정명과 게시일은 정확히 달았다 ✅ — buildxjordan **2026-02-11** / ChoasMaster777 **2026-03-19** / tokovar **2026-07-13** (원장과 전건 일치). 수치도 전건 일치 ✅ — 컨텍스트 **90~91%** 시작 → `search_tool = true`로 **99%** 회복 / 메모리 **100GB** / Sol **3시간** 지연
- 그러나 **규율 9**는 "커뮤니티 인용은 **출신 서브레딧을 명시**하고 게시일을 붙인다"를 요구한다. 이 책의 다른 장들은 지켰다 — 7장 "r/codex의 한 사용자(PinEnvironmental6395, 2026-05-12)", 9장 "Hacker News에 ModernMech이라는 계정", 10장 "r/codex의 한 사용자(Ok_Economist3865, 2026-03-17)". **11장만 매체를 뺐다.**
- 등급 병기는 되어 있다 ✅ (L109 "세 보고 전부 커뮤니티 관측이고 공식 문서가 인정한 동작은 아니다")
- **수정안:** 첫 등장에 매체를 한 번만 넣으면 된다 — "buildxjordan은 **r/codex에** 2026-02-11에 …", 이후 둘은 "같은 서브레딧의 ChoasMaster777이…" 형태로.

### ✅ 확인됨 (42건 — 추가 근거 요약)

**SDK · app-server**
- 설치·요구 버전 ✅ — `npm install @openai/codex-sdk` / `pip install openai-codex` / **Node.js 18 이상, Python 3.10 이상**
- 예제 코드 ✅ — `startThread()` / `thread.run(...)` / `result.finalResponse` / `resumeThread(threadId)`
- ⭐ **"The Python SDK controls the local Codex app-server over JSON-RPC." ✅ verbatim** (`01_reference.md` §2-6). 초안의 두 함의(SDK 미지원 기능은 app-server 직접 / app-server의 불안정성이 SDK로 전달)가 이 한 문장에서 직접 따라온다 ✅
- **Python SDK beta ✅** + 설치 규칙 인용 verbatim ✅ (`web-3.md` L1919) + "지금 `--pre`를 붙일 이유는 없다"는 정확한 독해 ✅
- `codex app-server` experimental + "may change without notice" ✅ (2·9장과 동일 근거, 표기 일관)
- 그림 1의 3경로 도식 ✅ — 새 사실 도입 없이 본문 내용만 배치

**경로 선택 · `mcp-server`**
- **선택 규칙 인용 verbatim ✅** — "Use the Codex SDK for coding-focused Codex threads. If Codex is one specialist inside a broader orchestrated workflow, run Codex CLI as an MCP server and orchestrate it with the Agents SDK."(`01_reference.md` §2-6). 초안의 요약("Codex가 주인공이면 SDK, 조연이면 MCP") ✅
- SDK 활용처 4종 ✅ / `Sandbox.read_only`·`workspace_write`·`full_access` 3값 + 생략 시 app-server 설정 기본값 ✅ (5장 축과 정합)
- **`codex mcp-server` ✅** — "Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex." ✅ verbatim / 노출 도구 **정확히 둘**(`codex`·`codex-reply`) ✅ / `tools/list` ✅ / 인스펙터 명령 ✅
- `codex` 도구 파라미터 ✅ — `prompt`(필수) + `approval-policy`·`model`·`cwd`·`config`·`base-instructions`·`developer-instructions`. 초안의 해석("**부르는 쪽이** 승인 정책과 모델과 작업 디렉터리를 지정한다") ✅
- ⭐ 12장 논지로 넘기는 연결("이 책의 마지막 장이 '둘 중 하나를 고르라'로 끝나지 않는 **기술적 근거**") ✅ — 실제로 12장 L122가 이를 회수한다

**MCP 클라이언트 방향**
- 임포트 `MCP_SERVER_CONFIG` 항목 ✅ (2장과 정합) / [#13762] 👍 **55** open ✅ (`community.md` L457) + "MCP etc. not being configured correctly" ✅
- ⭐ **컨텍스트 예산 3연작 완결 ✅** — 6장(스킬 2%) → 8장(분모의 광고-실측 괴리) → 11장(MCP 90%대 시작). 세 장의 서술이 서로 정합하고, 결론("컨텍스트는 내가 쓰기 전에 이미 상당 부분 예약돼 있고, 그 예약을 하는 것은 내가 붙여둔 것들이다")이 세 근거에서 따라온다 ✅

**조직 네 지점**
- **"A request must pass every boundary that applies to it. …" ✅ verbatim** (`web-5.md` L460). 초안의 비대칭 독해("내 설정은 나를 더 좁힐 수만 있고, 조직이 닫아둔 것을 열지는 못한다") ✅ 원문의 "can't grant a workspace feature or model"에서 직접 따라옴
- 관리형 설정 2종 인용 verbatim ✅ (L480) — Requirements(덮을 수 없음) / Managed defaults(다음 실행에 재적용)
- 강제 가능 항목 9종 ✅ — 승인 정책·승인 리뷰어·자동 리뷰 정책·샌드박스 모드·권한 프로필·웹 검색 모드·관리형 훅·MCP 서버 허용·플러그인 마켓플레이스 소스. 초안 L130의 "4·5·6장에서 우리가 손으로 세운 것들이 거의 그대로 목록에 있다" ✅
- **충돌 시 폴백 인용 verbatim ✅** (L487) — "falls back to a compatible value and **notifies the user**". 초안이 "조용히 무시되지는 않는다"로 정확히 읽었다
- 요구사항 실림 위치 4종 ✅ — 시스템 `requirements.toml`(Unix `/etc/codex/`, Windows `%ProgramData%\OpenAI\Codex\`) / 클라우드 번들 / 레거시 필드 재해석 / macOS MDM `com.openai.codex:requirements_toml_base64`. 클라우드 번들 실패 시 "조용히 시작하지 않고 오류" ✅
- 4장 3계층 → 4계층 예고 회수 ✅ (4장 L154가 예고했고 여기서 회수)

**관리 문서 지도 (표 2, 15행)**
- ⭐ **"위임" 열의 정직성 ✅** — L171의 사전 고지("게으른 정리로 읽으면 곤란하다. **문서의 실제 상태다.** … 그 사실을 감추고 그럴듯한 값을 채워 넣는 쪽이 훨씬 나쁘다")가 FR-17·FR-20의 정신과 일치
- **Owner·Admin·Member 3역할까지만 확정 ✅** — 원문 "Built-in Owner, Admin, and Member roles…"(`web-5.md` L141) + 위임 인용 verbatim ✅ "Because available seats, roles, and permissions change with product and plan updates, use the Help Center for the current permission list and setup procedure."(L470). 초안 L195 "그러니 이 책도 셋까지만 적는다" ✅ 원장 L1201의 판정과 정확히 일치
- **Analytics API·Compliance API 엔드포인트 미공개 ✅** — "그런 API가 존재한다는 사실까지가 공개 정보다"(L197)
- L201의 관찰("위임되지 않은 항목은 전부 **내 클라이언트의 런타임 동작을 실제로 바꾸는 것들**") — 표에서 직접 따라오는 정확한 패턴 읽기 ✅
- 관리자에게 물을 네 가지가 앞 절 네 지점과 1:1 ✅

**`build-ai-native-engineering-team`**
- Delegate / Review / Own 프레임 ✅
- 인용 2건 verbatim ✅ — "In practice, this shifts much of the mechanical 'build work' from engineers to agents. The agent becomes the first-pass implementer; the engineer becomes the reviewer, editor, and source of direction."(`web-6.md` L1555) / "True ownership of code—especially for new or ambiguous problems—still rests with engineers, and certain challenges exceed the capabilities of current models."
- 테스트 인용 verbatim ✅ + 초안의 연결("프롬프트에 '무엇이 완료인지' 적으라고 했던 조언의 코드판") ✅ 7장 Done when과 정합

**클로징**
- 세 갈래 정리가 본문 근거만 사용 ✅ / 계획의 클로징 기법('선택지 제시형' — 갈림길 2~3개를 제시하고 선택을 독자에게) 이행 ✅

### 규율 준수 메모 (판정 아님)

- **FR-2:** 3회 — 표 1·2 캡션 2 + L37 본문 1. 원장형 표라 문언 부합 ✅
- **FR-3 / 규율 12:** Claude Code 언급 **0건** ✅
- **규율 6·11:** 위반 없음 ✅
- **🕒 0건인 이유:** 위임 항목·역할 목록·API 계약 세 곳 모두 "문서가 위임한다"는 사실 자체를 적어 휘발성을 구조적으로 고지했다 ✅

---

## 12장 — 라운드 1

검증일 2026-08-02 · 대상 `chapters/12_draft.md`(스타일 반영본) · 구체 주장 38건 추출

**집계: ✅ 38 / ❌ 0 / ⚠️ 0 / 🕒 0**

> **이 책에서 유일하게 ❌·⚠️가 모두 0인 장이다.** 마지막 장은 앞 열한 장의 사실을 회수하는 구조라 전파 오염(FR-18) 위험이 가장 컸는데, 앞 장 **final** 기준으로 정합했고 fact-checker가 남긴 구속 규율 두 건(FR-13·FR-22)을 모두 이행했다.

### 저술가 명시 요청 판정 (6건)

#### ① FR-13 이행 — 연표를 증거로 승격할 때의 1차 소스 부재 고지 — **✅ 초과 이행**

- **FR-13 요구:** *"12장은 이 연표를 '진화 방향이 갈렸다'는 논지의 증거로 승격한다. 승격하는 순간 1차 소스 부재가 논지 결함이 되므로, **'이 책이 1차로 수집한 것은 Codex 쪽 연표뿐'이라는 한 줄 고지가 필수다.** 이 고지 없이 12장이 제출되면 fact-checker가 ❌로 판정한다."*
- **초안 L13-17이 한 줄이 아니라 문단 단위로 이행했다 ✅**
  - L13 승격 시점을 스스로 명시 — "이제 **논지의 증거로 쓸 차례**인데, 증거로 승격하는 순간 먼저 밝혀둘 것이 있다."
  - L15 **독립 굵은 문단** — "**이 대비에서 이 책이 1차로 수집한 것은 Codex 쪽 연표뿐이다.**"
  - L17 범위 한정 + 검증을 독자에게 이양 — "같은 기간 다른 도구가 어디로 갔는지는 **이 책의 리서치 범위 밖이다.** 그러니 '갈라졌다'는 판단의 나머지 절반은 **독자 자신의 사용 경험에 맡긴다.** … 이 책이 근거를 갖고 말할 수 있는 것은 Codex 쪽 궤적 하나이며, 그것만으로도 충분히 뚜렷하다."
- ⭐ **1장 ⚠️-2의 인계가 완결됐다.** 파 1에서 "12장 승격 시 고지 의무"로 남긴 항목이 여기서 닫힌다. 그리고 처리 방식이 FR-12(부재 주장 금지)·FR-17(빈칸 + 해명)과 같은 계열이다 — **"말할 수 없다"를 숨기지 않고 논지의 일부로 만든다.**

#### ② FR-22 이행 — `automations` 삽화 문자열 미인용 — **✅**

- 전 장 스캔 결과 **"5.6 Sol Extended"·"5.6 Sol Extra High"·"5.6 Sol" 검출 0건** ✅
- FR-4가 인용을 금지한 UI 삽화 문자열(`codex__automations.md` L110의 `ariaLabel`)이 12장의 표면 서술에 유입되지 않았다 ✅
- 표 1이 표면별 조건을 다루면서도 UI 삽화가 아니라 **본문 서술**만 근거로 삼았다 ✅

#### ③ 은퇴 문안 — 8장 final과 문자 단위 동일 — **✅ diff 무결**

- `chapters/08_final.md`와 `chapters/12_draft.md`의 해당 문장을 기계 대조한 결과 **IDENTICAL** ✅
  > `gpt-5.4`·`gpt-5.4-mini`는 **2026-08-31 은퇴 예정**이다(ChatGPT 로그인 사용자 한정 — API 키 인증은 영향 없음). 대체는 각각 Terra·Luna다. **2026-08-02 문서 기준으로는 아직 은퇴 전이다.** 이 책을 읽는 시점에는 이미 지난 날짜일 가능성이 높으므로, 은퇴 여부가 아니라 **대체 경로**를 기준으로 읽어라.
- **FR-1 완전 준수 ✅** — 계획 규율 5가 요구한 "8장과 12장 양쪽에 위 문안을 그대로 적용"이 문자 단위로 지켜졌다. 과거형 서술 0건 ✅
- 파 3 FR-19의 권고("12장이 같은 문안을 다시 쓸 때 8장 L95를 그대로 복사하라")를 그대로 이행 ✅

#### ④ 고유 표면 9종 9행 표 — **✅ 직접 카운트 일치**

- **표 1 데이터 행 직접 카운트 = 9** ✅ (내장 브라우저 · Computer Use · Chrome 확장 · Appshots · Sites · ChatGPT Voice · Codex Micro · Chronicle · `/pets`)
- 본문 L31·L47이 "아홉 가지"·세 덩어리(화면 3 / 웹 3 / 입력 3)로 재집계하는데 **3+3+3 = 9** ✅ 내부 정합
- 각 행의 시점·조건이 앞 장 근거와 정합 ✅ — 내장 브라우저·Computer Use 2026-04 주간 / Chrome 확장·Appshots 2026-05 주간 / Sites 2026-06 주간 / Voice 2026-07 주간(Plus·Pro·Business·Edu·Enterprise) / **Micro 2026-07-15**(원문에 "On July 15"가 있는 유일한 일자 — **FR-11 준수** ✅) / Chronicle opt-in 리서치 프리뷰·ChatGPT Pro·macOS
- 조건 열의 제약도 전건 근거 있음 ✅ — 내장 브라우저는 CLI·IDE 확장 불가 / Appshots·Chronicle은 macOS 한정 / Computer Use는 지원 지역 + 플러그인 + 화면 기록·손쉬운 사용 권한
- ⭐ **"이 목록이 기능의 가치 순서를 뜻하지 않는다"(L57)** — 표의 해석 범위를 스스로 한정한 처리 ✅

#### ⑤ BloondAndDoom 게시일 (style m3 이관분) — **✅ 이관 완료**

- **3장에 BloondAndDoom 검출 0건 / 12장 L126에만 등장** ✅ — style m3의 이관 지시가 정확히 반영됐다
- **HN, 2026-03-16** ✅ (`community.md` L395·L493 — 두 곳 모두 동일 날짜)
- 인용 취지 정확 ✅ — 원장 "many people don't understand that you can just say 'check again' to the model you use and it will just find bugs, repeat it until there are no bugs. … It's intuitive to assume another will help more and better review but yeah I don't know."를 초안이 "같은 모델에 'check again'을 반복해도 결국 버그를 찾아낸다며, 다른 모델을 부르는 것이 더 낫다는 직관을 의심한다"로 옮겼다 — **교차 리뷰 무용론**이라는 원장 라벨과 일치
- 등급 처리 ✅ — 원장은 `[익명 주장·확인 필요]`인데, 초안은 계정명·매체·게시일을 달고 **바로 뒤 문장에서 양쪽 다 미확정으로 닫는다**: "**교차 리뷰는 시도할 값이 있는 가설이지, 검증된 우위가 아니다.**" 관점 A(AWS 실명 소스)와 반론을 같은 무게로 두지 않으면서도 판정을 유보한 처리가 정확 ✅
- 10장과의 구조 대응 서술("10장에서 '코드 리뷰는 Codex'라는 통념에 자기 반증이 붙어 있던 것과 같은 구도") ✅ — 10장 Ok_Economist3865 절과 실제로 정합

#### ⑥ 1장 final 연표와의 정합 — **✅ 6줄 전건 대응 (FR-18 준수)**

`chapters/01_final.md` 그림 2(mermaid timeline)와 12장 L9의 산문 요약을 항목 단위로 대조:

| 월 | 1장 final | 12장 요약 | 판정 |
|---|---|---|---|
| 2026-02 | Codex 앱 macOS 출시 · 턴 중간 steering | macOS 데스크톱 앱이 나오고 | ✅ |
| 2026-03 | Windows 네이티브 실행 | Windows 네이티브 실행이 붙고 | ✅ |
| 2026-04 | 브라우저 조작과 승인 자동 리뷰 | 브라우저 조작과 승인 자동 리뷰가 들어오고 | ✅ |
| 2026-05 | Appshots · Chrome 확장 · 원격 제어 | Chrome 확장·Appshots·원격 제어가 이어지고 | ✅ (순서만 다름) |
| 2026-06 | Sites · Claude Code 설정 임포트 · Record & Replay | Sites와 Record & Replay가 나오고 | ✅ (임포트는 2장 주제라 생략 — 표면 확장 궤적만 요약하는 이 문단의 범위에 맞다) |
| 2026-07 | 데스크톱 앱 병합 · ChatGPT Work · Codex Micro · 다중 폴더 · 음성 · Codex Security | 병합·Micro·다중 폴더·음성·Security가 몰렸다 | ✅ |

- 한 줄 압축("터미널 도구 → 데스크톱 앱 → GUI·브라우저·컴퓨터 조작·음성·전용 하드웨어")도 1장 final L125와 **동일 문구** ✅
- ⭐ **FR-18 준수 ✅** — draft가 아니라 final과 정합한다. 파 2에서 관측한 장 간 전파 오염(6장 ❌-2)이 재발하지 않았다

### ✅ 확인됨 (38건 — 추가 근거 요약)

**내장 브라우저 · Computer Use (논지의 결정적 증거)**
- **"The built-in browser in the ChatGPT desktop app gives you and ChatGPT a shared view of websites and local web apps inside a chat." ✅ verbatim**
- **"Treat page content as untrusted context." ✅ verbatim** — 원문 캐시 `codex__browser.md` **L18** 직접 확인. 5장 프롬프트 인젝션 감각과 연결한 서술 ✅
- 별도 브라우저 프로파일 / 기존 탭·세션 미승계 ✅ / 세 갈래 선택 기준(전용 통합→플러그인, 로그인 맥락→Chrome, localhost→내장 브라우저) ✅ + **"내장 브라우저는 격리된 프로파일이지만, Chrome 확장은 내 실제 세션을 내준다"**는 신뢰 경계 대비 ✅
- **"With Computer Use, ChatGPT can see and operate graphical user interfaces on macOS or Windows." ✅ verbatim**
- 쓸 자리 4종(데스크톱 앱 상태 확인·앱 설정 변경·플러그인 없는 데이터 소스·GUI에서만 재현되는 버그) ✅
- **"Because Computer Use can affect app and system state outside your project workspace, use it for scoped tasks and review permission prompts before continuing." ✅ verbatim**
- 앱 단위 승인 + "항상 허용" 목록 + Windows는 대상 앱을 활성 데스크톱에 ✅
- ⭐ **논지 완성이 근거에서 직접 따라온다**(L89) — "앞서 세워온 통제 모델은 전부 파일과 명령을 대상으로 한 것 … **마우스 클릭에는 워크스페이스 개념이 없기 때문이다.** 새 표면은 새 통제 축을 요구한다." 5장 `protected paths`가 파일 시스템 경계였다는 사실과 원문 "outside your project workspace"를 겹쳐 읽은 정확한 추론 ✅

**§4-4 반대쪽 목록 (6항목)**
- 6줄이 `01_reference.md` §4-4와 **문자 단위로 대응** ✅ — `/rewind`(코드까지 되돌리기) · 중첩 지침 파일 자동 로드 · Plan Mode 기본값 시작 · 상태 표시줄 · 서브에이전트별 모델 지정 · 훅 완전 커버리지
- 각 항목의 실무 요구 서술이 앞 장과 정합 ✅ — `/rewind` 부재↔3장 습관 / 중첩 미로드↔3·4장 / 상태 표시줄↔`/statusline` / 서브에이전트 모델↔6장 이슈 3건 / 훅 커버리지↔6장 Partial
- ⭐ **규율 12·FR-3의 자기 선언 ✅**(L110) — "**여섯 항목을 벗어난 비교는 이 책에 없다.** 이 책의 리서치는 Codex 공식 문서를 1차로 수집했고 다른 도구의 문서는 수집하지 않았다. … 그 밖의 자리는 빈칸으로 두거나 Codex 쪽 진술로 돌렸다. **5장 표 1의 빈칸들, 그리고 그 아래 붙인 해명 문단이 그 결과다.**"
  - 실제로 검증됐다 — 5장 표 1의 빈칸 처리(파 2 판정 ⑦)와 7장·12장의 Codex 진술 전환이 그 결과다. **FR-17이 책의 결론부에서 회수됐다** ✅
- L112의 마무리("빈칸이 불편했다면, 그 불편이 정확한 감각이다. **이 책이 근거를 갖고 말할 수 있는 범위가 거기까지라는 뜻이지, 대응물이 없다는 뜻이 아니다.**") — **FR-12의 정의를 독자에게 그대로 전달** ✅

**두 하네스 네 가지 방법**
- ① `codex mcp-server` ✅ (11장과 동일 근거, "다른 에이전트가 Codex를 소비할 때" 인용 일관) / SDK↔MCP 선택 기준 재사용 ✅
- ② 지침 이중 관리 회피 — **steve-atx-7600, Hacker News 2026-07-09** ✅ (4장과 동일 근거·동일 날짜 표기) / `.agents/skills` 벤더 중립 경로 ✅ (2·6장과 정합)
- ③ 교차 리뷰 — AWS 한국 기술블로그(Kyutae Park, **2026-06-11**) ✅ + BloondAndDoom 반론 ✅ (위 판정 ⑤)
- ④ 작업 성격 분기 — 네 자리(`.rules`+`codex execpolicy check` / 클라우드 위임 / `codex exec` / Computer Use)가 각각 6·9·9·12장 근거와 정합 ✅

**연구 인용 (클로징)**
- **Liu et al. arXiv:2603.28592, 2026, 📄 preprint ✅** — 5개 수치 전건 일치(`papers.md` §3-4): 저장소 **6,299개** / AI 작성 커밋 **302.6천 건** / 총 **484,366건** 이슈 / **코드 스멜 89.3%** / **22.7%가 최신 버전에도 생존**. 식별자 YYMM=2603(2026-03) 과거 ✅
- **Sawada et al., EASE 2026, ✅ peer-reviewed** ✅ (`papers.md` §3-5, arXiv:2605.06464) — 초안이 "동료 심사를 거친 논문"으로 등급을 명시 ✅
- **생산성 RCT 3편 ✅ 전건** — +**55.8%**(2023 Copilot, 그린필드 단일 과제, **저자에 해당 기업 소속 포함** ✅) / +**21%**(**96명**, **저자 스스로 신뢰구간이 넓다고 밝힘** ✅) / −**19%**(METR, 숙련 16명·246과제·평균 5년 자기 저장소·2025-02~06 ✅). 세 편의 조건이 전부 원장과 일치
- ⭐ **"평균을 내려 하지 말자"(L142) ✅** — 원장 `papers.md` L153의 판정("세 개의 RCT가 +55.8%, +21%, −19%로 갈린다. **이 불일치 자체가 책에서 다뤄야 할 사실이다**")을 정확히 이행. 7장 METR 절과도 정합
- ⏳ 낡음 표시 항목 미사용 ✅ — SWE-bench 1.96%·SWE-agent 12.5%·Copilot 40% 취약 등을 현재 성능 근거로 쓰지 않았다

**유효기간 목록 (5항목)**
- 다섯 항목이 전부 이 책이 실제로 판정 유보하거나 🕒 처리한 자리와 일치 ✅ — 모델 은퇴(FR-1) / 요금·한도(8장 ⚠️ 구간, #28879·#34035) / 권한 프로필 Beta(FR-8) / 전환 마찰 3건(#11626·#12115·#28969, 3장) / Codex Security 출시 직후(10장)
- 이슈 번호 4건의 링크·주제가 앞 장과 정합 ✅
- ⭐ **책 전체의 🕒 처리를 마지막 장치로 회수한 구성** — "기술서가 독자에게 줄 수 있는 가장 정직한 것은 **확인하는 습관**" + "이슈 번호를 열고, 문서의 첫 문장을 읽고, 성숙도 라벨을 확인하고, **인용된 관측에 게시일이 붙어 있는지 보라고.**" 이 책이 3장부터 실제로 지켜온 네 가지 규율의 요약이며, fact-checker 판정 기준과 동일 계열 ✅

**여정 회수 (L116)**
- 1~11장의 요약 11개가 각 장 final의 실제 내용과 정합 ✅ (계획의 클로징 기법 '여정 회수형' 이행)

### 규율 준수 메모 (판정 아님)

- **FR-1:** 완전 준수 — 8장 final과 문자 단위 동일 ✅
- **FR-2:** 2회(표 1 캡션 + L146 본문) ✅
- **FR-3 / 규율 12:** §4-4 6항목 안에서만 비교, 그리고 **그 사실을 본문에서 선언** ✅
- **FR-4 / FR-22:** UI 삽화 문자열 0건 ✅
- **FR-11:** Micro만 일자(원문에 "On July 15" 존재), 나머지는 주간 표기 ✅
- **FR-13:** 초과 이행 ✅ / **FR-18:** 1장 final 기준 정합 ✅
- **규율 6·9·11:** 위반 없음 ✅

---

## 파(wave) 4 종합 — 오케스트레이터 통보

### BLOCKING 0건

**파 4에서 ❌ 판정이 나오지 않았다.** 12개 장 가운데 처음으로 한 파 전체가 무결이다.

### 비블로킹 권고 3건

| # | 장 | 항목 | 수정안 |
|---|---|---|---|
| 1 | 10장 | ⚠️-1 릴리스 간격 "2~5일"(L198) — 실측 2~3일 | "**2~3일 간격이다.**" |
| 2 | 10장 | ⚠️-2 표 2 캡션 "(원문 그대로)"인데 의미 열이 번역문 (FR-10) | 캡션을 "(**판정명은 원문 표기**)"로 |
| 3 | 11장 | ⚠️-1 MCP 보고 3건에 서브레딧(r/codex) 미표기 (규율 9) | 첫 등장에 "r/codex에" 한 번 삽입 |

### 파 4 총계

| 장 | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|
| 10장 | 45 | 0 | 2 | 0 |
| 11장 | 42 | 0 | 1 | 0 |
| 12장 | 38 | 0 | 0 | 0 |
| **합계** | **125** | **0** | **3** | **0** |

---

# Phase 4 사실 검증 종료 판정 — 12개 장 누적

## 누적 집계

| 파 | 장 | ✅ | ❌ | ⚠️ | 🕒 |
|---|---|---|---|---|---|
| 1 | 1·2·3 | 108 | 2 | 8 | 0 |
| 2 | 4·5·6 | 115 | 3 | 5 | 0 |
| 3 | 7·8·9 | 127 | 1 | 6 | 0 |
| 4 | 10·11·12 | 125 | 0 | 3 | 0 |
| **누적** | **12개 장** | **475** | **6** | **22** | **0** |

- 검증 대상 구체 주장 **503건**
- 원문 verbatim 대조 대상 **약 240건**, 불일치 **2건**(1장 SDK 경로, 7장 인용 변조) — **정확도 99.2%**

## 에스컬레이션 잔여 — **0건**

### BLOCKING 6건 전건 해소 확인

| 파 | 장 | 항목 | 상태 |
|---|---|---|---|
| 1 | 1장 | changelog "95개" | ✅ 해소 (`01_final.md` "여든 건이 넘는") |
| 1 | 1장 | 표 2 SDK 경로 | ✅ 해소 (`openai/codex/codex-sdk`) |
| 1 | 3장 | `(사실 확인 필요)` 마커 | ✅ 해소 (`03_final.md` A안, 마커 0건) |
| 2 | 4장 | "갱신 시점을 네 가지로" | ✅ 해소 (`04_final.md` "여러 갈래로" + 5번째 추가) |
| 2 | 6장 | 표 1 `SYSTEM` 행 누락 | ✅ 해소 (`06_final.md` L39) |
| 2 | 6장 | "가장 가까운 하나만"(4장과 충돌) | ✅ 해소 (표현 0건, 대체 문단) |
| 3 | 7장 | PinEnvironmental6395 인용 변조 | ✅ 해소 (`07_final.md` L44 원문 복원) |

> 표기상 7행이지만 6장이 2건이므로 **BLOCKING 총 6건 → 전건 해소**.

### ⚠️ 22건 처리 상태

- **본문 반영 확인분:** 7장 경로 정정 · 8장 Pro 배수 매핑 A안 · 9장 backnotprop 병기 · 9장 "여덟 줄 가운데" 등 파 1~3 권고가 final에 반영돼 있다
- **미반영 잔여 3건:** 파 4의 비블로킹 권고(위 표) — **전부 비블로킹**이며 editor 단계에서 처리 가능
- **판정 유보로 본문에 명시된 항목:** 8장 요금·한도 확인 불가 구간, 7장 실행 스타일 논쟁, 10장 Codex Security 초기 관측 — **이것들은 미해결이 아니라 "미해결로 확정된" 항목**이다. 본문이 스스로 유보를 선언했고, 12장 "유효기간" 목록이 다섯 항목으로 회수했다

### 🕒 0건 — 신선도 경고가 한 건도 필요하지 않았던 이유

이 책은 가장 빨리 낡는 주제(요금·한도·모델 은퇴·이슈 상태·Beta 딱지)를 다루면서 🕒 판정이 **0건**이다. 저술 측이 휘발 항목마다 본문에서 먼저 고지했기 때문이다 — 3장에서 세운 문형("표를 외우지 말고 번호를 열어보라")이 4~12장에 일관되게 이어졌고, 12장이 그 목록을 마지막 장치로 회수했다.

## 관측된 실패 패턴 4계열 (하네스 회고용)

| 계열 | 건수 | 사례 | 대응 규율 |
|---|---|---|---|
| **세기·집계** | ❌4 | 1장 "95개", 4장 "네 가지", 6장 표 1행 누락, 8장 등 | FR-9 → FR-16 |
| **옮겨 담기** | ❌1 | 1장 표 2 SDK 경로(링크 target vs 셀 문자열) | FR-10 |
| **장 간 전파 오염** | ❌1 | 6장이 3장의 *외부 표준* 인용을 *Codex 동작*으로 흡수 → 4장 반박 | FR-18 |
| **인용 미세 변조** | ❌1 | 7장 `GPT-5` → `GPT`(버전 표기 삭제) | FR-19 |

**핵심 소견:** ❌ 6건 중 **5건이 "옮기기"가 아니라 "세기·요약하기·회수하기"에서 났다.** 원문 인용은 240건 중 2건만 어긋났다. 이 팀의 취약점은 인용 정확도가 아니라 **2차 가공**이었고, FR-9·16·18·19가 그 지점을 겨눈 뒤 파 4에서 ❌ 0건이 됐다.

**파별 ❌ 추이: 2 → 3 → 1 → 0.** 규율 누적이 작동했다고 본다.

## Phase 4 사실 검증 종료 판정 — **통과 (에스컬레이션 잔여 없음)**

1. **BLOCKING 6건 전건 해소** — final 파일에서 기계 확인 완료
2. **미해소 `(사실 확인 필요)` 마커 0건** — `03_final.md` 포함 12개 final 전체 스캔 결과 0건
   - ⚠️ 참고: `03_draft.md`에는 마커 1건이 남아 있으나 **`03_final.md`가 정전**이며 거기서는 해소됐다. editor는 final을 소비하므로 무해하나, draft 파일이 갱신되지 않은 상태임을 기록해둔다
3. **규율 위반 0건** — 규율 4(요금 범위값)·6(인용 금지 9건)·9(진영·게시일)·11(경험담)·12(Claude Code 화이트리스트) 및 FR-1~FR-22 전 장 스캔 통과
4. **잔여 ⚠️ 3건은 전부 비블로킹**

**→ 원고는 사실 정확성 기준으로 Phase 4.5(통권 수락 게이트)에 넘길 수 있다.**

### editor·manuscript-reviewer에게 인계하는 사항

1. **뒷부속(서문·에필로그·참고문헌)은 아직 검증되지 않았다.** 이 로그는 `chapters/*`만 다뤘다. editor 산출 후 **fact-checker의 front/back matter 한정 검증 패스가 별도로 필요**하다 — 특히 **참고문헌의 확인 등급 라벨**(✅ peer-reviewed / 📄 preprint / ⏳ 낡음 / ❌ 벤더 자체 보고)이 `research/papers.md`·`community*.md` 원장과 일치하는지. 이 책은 본문에서 등급을 일관되게 병기해왔으므로 참고문헌에서 어긋나면 눈에 띈다
2. **용어 정전은 2장 표 2(10행)다.** 12장 L110이 이를 명시적으로 재확인했다
3. **은퇴 문안은 8장·12장 두 곳에 문자 단위로 동일하게 존재한다.** 통합 시 한쪽만 수정하지 마라
4. **비블로킹 권고 3건**(위 표)은 editor 단계에서 반영 가능

---

# 뒷부속 검증 패스 (front/back matter) — 라운드 1

검증일 2026-08-02 · 대상 `04_manuscript.md`의 **판권·서문·목차·에필로그·참고문헌**만
(챕터 본문은 파 1~4에서 판정 종료 — 재검증하지 않았다)

**집계: ✅ 39 / ❌ 0 / ⚠️ 3 / 🕒 0 → BLOCKING 0건**

> FR-23이 명세한 검사 항목 5개를 전부 수행했다. **참고문헌의 확인 등급 라벨은 원장과 전건 일치**하고, URL은 구성되지 않았으며(Reddit thread ID 6개 전수 실재 확인), 148 URL 전수·표 A 18건·표 B 13건이 **직접 카운트로 캡션과 일치**한다.

## FR-23 검사 항목별 결과

### 검사 ①. 참고문헌 확인 등급 라벨 — **✅ 전건 일치**

**범례 7등급 직접 카운트 = 7 ✅** (🟢 원문(.md) / 🟢 원문(HTML) / 🟡 목록 추출 / ✅ / 📄 / ❌ / ⏳) + 커뮤니티 성격 2종(출처 명확 / 익명 관측) 별도 서술.

**표 B 13건의 등급을 `research/papers.md` 원장과 1:1 대조 — 불일치 0건:**

| 문헌 | 매뉴스크립트 등급 | 원장 | 판정 |
|---|---|---|---|
| Yang, SWE-agent | ✅ NeurIPS 2024 | §2-1 "✅ peer-reviewed" | ✅ |
| Merrill, Terminal-Bench | ✅ ICLR 2026 | §1-7 "✅ peer-reviewed" | ✅ |
| Sawada | ✅ EASE 2026 | L369 "EASE 2026 \| ✅" | ✅ |
| Kwa (METR 시간 지평) | ✅ ⏳ NeurIPS 2025 | L341 "NeurIPS 2025 … ✅ peer-reviewed" | ✅ (⏳ 부여 근거는 ⚠️-3) |
| Gorinova | 📄 | §1-8 "📄 preprint" | ✅ |
| Singh, IssueTrojanBench | 📄 | §4-4 "📄 preprint" | ✅ |
| Becker (METR RCT) | 📄 | §3-3 "📄 preprint" | ✅ |
| Aleithan, SWE-Bench+ | 📄 | §1-2 "📄 preprint" | ✅ |
| Deng, SWE-Bench Pro | 📄 | §1-6 "📄 preprint" | ✅ |
| Liu | 📄 | §3-4 "📄 preprint" | ✅ |
| Peng (Copilot 2023) | 📄 | L157 "📄 preprint (**이해관계 있음**)" | ✅ |
| Paradis (Google 2024) | 📄 | L167 "📄 preprint" | ✅ |
| OpenAI Addendum | ❌ | §4-5 "**벤더 자체 보고**임을 명시할 것" | ✅ |

- **재집계도 정확하다 ✅** — 본문 서술 "열세 건 가운데 **여덟 건**이 아직 동료 심사를 거치지 않았다"를 직접 카운트: 📄 **8** + ✅ **4** + ❌ **1** = 13 ✅ (FR-16 준수)
- **두 METR 연구를 정확히 구분했다 ✅** — 시간 지평(Kwa, NeurIPS 2025, 11장)과 생산성 RCT(Becker, preprint, 7·12장)를 별개 행으로 두고 인용 장을 다르게 매핑했다. 혼동하기 쉬운 자리인데 갈랐다
- 커뮤니티 성격 라벨도 원장과 일치 ✅ — Ok_Economist3865 "익명이나 **자기 반증 포함**"(원장 `community-2.md` L576 "익명이나 자기 반증 포함 — 인용 가치 높음") / buildxjordan·ChoasMaster777·tokovar "출처 명확"(원장 L454·L466·L484 동일) / gregwebs "출처 명확 (로그 첨부)"(원장 L292 "`[출처 명확 — 로그 붙임]`")

### 검사 ②. URL이 원장에서 그대로 옮겨졌는가 (구성 URL 금지) — **✅ 전건 실재**

- **Reddit thread ID 6개 전수 대조 — 6/6 원장 실재 ✅**
  `1tao42q` · `1rwjmqp` · `1usogxo` · `1r22uk1` · `1rxu4ur` · `1uvigpf` — 모두 `research/community-2.md`에 있다. **구성된 ID 0건**
  - ⭐ **댓글 인용자와 스레드의 매핑도 정확하다.** Ok_Economist3865(2026-03-17)와 imperfectlyAware(2026-04-24)가 **같은 스레드 `1rwjmqp`**를 가리키는데, 원장 L575-578이 그 스레드("Those of you who switched from Claude Code to Codex", 2026-03-17 개설)의 하위 댓글로 둘을 함께 싣는다. 날짜 차이는 댓글 시점 차이이며 오류가 아니다 ✅
  - NootropicDiary·xoStardustt → `1usogxo` ✅ (원장 L587, 2026-07-10 스레드)
  - PinEnvironmental6395 → `1tao42q` ✅ (원장 L569, 2026-05-12)
- **HN item ID 8개** 전부 원장 실재 ✅ (49089755 · 49057553 · 48904705 · 48851396 · 48828605 · 48519556 · 48464767 · 48150929 · 47405533 · 46866331)
- **국내 3건** ✅ — AWS 블로그 URL / dcinside `no=1149110` / GeekNews `topic?id=28538`(원장 `community.md` L170) 전부 실재
- **arXiv ID 12개** 전부 `papers.md` 실재 ✅ / **식별자 형식 점검 통과** — YYMM이 빌드 시점(2026-08-02) 미래인 항목 **0건**(최신이 2607 = 2026-07). 자동 ❌ 규칙 비해당

### 검사 ③. 148 URL 전수·섹션 헤더·범례 구성 — **✅ 직접 카운트 일치**

- **공식 문서 표 행 직접 카운트 = 148 ✅** (A 33 + B 34 + C 21 + D 28 + E 17 + F 15). 서문 L48과 참고문헌 도입부의 "148개 URL" 주장과 일치
- 섹션 헤더 A~F가 리서치 파일 분담(web-1~6)과 대응 ✅
- "별칭 중복 **여섯 쌍** → 고유 문서 약 140개" ✅ (`01_reference.md` L780과 일치). 표 F에 실제로 별칭 쌍이 표시돼 있다 — #134↔#135, #140↔#41, #141↔#42, #142↔#59, #143↔#145 ✅
- 개별 비고도 원장과 일치 ✅ — #5 `/codex/import` "`.md`가 HTML보다 짧다" / #19 changelog `.md` 404 / #39 "실제 제목은 **Work with files**"(규율 8) / #50 274키+116키 / #63 ConfigTable 29개 174행 / #137 "수치 전무(37줄)" / #138 best-practices HTML 복원(**FR-15와 일치**) / #147·#148 HTML 복원
- **🟡 목록 추출 4건(#85~#88)에 "개수 단정 금지" 표기 ✅** — 11장 L241의 서술("개수를 세어 외우는 것은 의미가 없다")과 정합

### 검사 ④. 은퇴 문안 세 번째 사본 부재 — **✅ 확인**

- **에필로그에 `gpt-5.4`·은퇴 관련 서술 0건** ✅ (기계 스캔)
- 은퇴 문안은 8장·12장 **두 곳에만** 존재하며 두 사본은 문자 단위로 동일하다(파 4에서 diff 확인) ✅ FR-1 준수
- 에필로그가 12장과 역할이 갈린다 ✅ — 12장은 여정 회수 + 유효기간 5항목, 에필로그는 **메타 층**(비운 자리 / 끝내 답하지 못한 질문 / 독자에게 넘기는 기록 습관). 중복 서술 없음

### 검사 ⑤. 뒷부속에 새 사실 주장이 없는가 — **✅ (⚠️-3 1건 제외)**

- **서문의 수치 주장은 "148개 URL"·"고유 문서 약 140개" 둘뿐** ✅ (기계 스캔 — 나머지는 전부 장 번호 참조). 두 값 모두 3장·참고문헌·원장과 정합
- 서문의 규약 4종이 이 책의 실제 규율과 일치 ✅ — 용어 정전 2장 표 2(12장 L110이 재확인) / 시점 앵커 `(2026-08-02 문서 기준)` 고정(**FR-2 문안 그대로**) / 인용에 게시일·출신 커뮤니티 / 확인 등급 병기
- 서문 "이 책이 약속하지 않는 것" 3항목이 실제 판정과 일치 ✅ — 우열 판정 안 함 / **상대 도구에 대한 새 사실 주장 안 함**(FR-3·규율 12의 독자용 선언) / 오래 유효한 수치 약속 안 함
- 에필로그의 미해결 목록 6항목이 **실제 유보 구간과 전건 일치** ✅ — 5시간 범위·주간 한도·2026-06 요율(8장 ⚠️ 구간) / 컨텍스트 광고-실측 간격(8장 #32806) / 실행 스타일 코드베이스 가설(7장) / 한국어 1차 증언 부족(3장). **새로 만든 항목 0건**
- 유일한 예외가 표 B의 Kwa 행 → **⚠️-3**

## 판권·목차 검증

### 판권 — **✅ 6건 전건 일치**

| 항목 | 매뉴스크립트 | 대조 | 판정 |
|---|---|---|---|
| 판본 | v1.0.0 | `book_manifest.json` `"version": "1.0.0"` | ✅ |
| 발행일 | 2026-08-02 | `"pub_date": "2026-08-02"` | ✅ |
| 저자 | Toby-AI | `"author": "Toby-AI"` | ✅ |
| 식별자 | `urn:uuid:882cf2c0-4843-41b5-8799-f979fe9cc244` | 매니페스트 `identifier` 동일 | ✅ |
| 라이선스 | CC BY-NC-SA 4.0 + 3조항 + 공식 링크 | `"license": "CC BY-NC-SA 4.0"` / 링크 `creativecommons.org/licenses/by-nc-sa/4.0/` 정확 | ✅ |
| 하네스 | book-writer **v1.10.0** + `github.com/tobyilee/book-writer` | 프로젝트 루트 `VERSION` = `1.10.0`, README L7 URL 동일 | ✅ |

- 매니페스트 부가 필드도 정합 ✅ — `genre: tech-book` / `harness_version: 1.10.0` / `rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0`
- 저작권 고지 문안 ✅ — "인용은 출처와 게시일을 병기하는 방식으로만 이뤄졌으며"가 실제 규율(규율 9)과 일치

### 목차 — **✅ 2건 일치**

- **12개 장 제목이 본문 `# N장.` 헤더와 diff 무결(IDENTICAL)** ✅
- 목차 15항목 = 서문 + 12장 + 에필로그 + 참고문헌 ✅ 실제 구조와 일치, 순서도 일치

### 서문 style 수정 3건 — 사실 측면 확인 (문체는 style-guardian 소관)

- style-guardian이 지적한 **C2(참고문헌 구간에서 시점 표기 규약 3회 위반)**는 **FR-2가 관할하는 항목**이므로 확인했다 → **수정 완료 ✅**
  - 뒷부속 전체 스캔 결과 시점 표기 3건이 전부 `2026-08-02 문서 기준` 형식이고 **변형 표기 0건**("2026년 8월 기준"·"2026-08 기준" 미검출)
- 나머지 2건(bold 밀도·수사 대구)은 문체 지적이라 사실 판정 대상이 아니다. 수정 과정에서 **사실 드리프트가 발생하지 않았음**은 위 검사 ⑤로 확인했다

## ⚠️ 정밀도 보정 (비블로킹)

### ⚠️-1. HTML 주석이 원고에 남아 있다 (L2999)

- **`<!-- 추출 행 수: 148 -->`** — editor의 작업 흔적이다. 참고문헌 공식 문서 표 바로 뒤에 있다.
- 사실 오류는 아니다(행 수 148은 실측과 일치 ✅). 다만 **산출물에 남아서는 안 되는 잔여 마커**이고, Phase 4.5 통권 수락 게이트의 "금지 잔여 마커" 스캔 대상이다.
- **수정안:** 삭제. (원고 전체에서 HTML 주석은 이 1건뿐이다 — 기계 스캔 확인)

### ⚠️-2. 표 A `#32806` 행의 개설일·👍를 비웠는데 원장에 값이 있다

- 매뉴스크립트: `| #32806 | 광고된 컨텍스트 창과 실측의 간격 | — | — | closed | 8장 |`
- **원장에는 값이 세 곳에 명시돼 있다** — `research/community.md` L271("2026-07-13, 👍 54, **closed**") · L427 · L458(`2026-07-13 | 54 | 27 | closed`)
- 표 아래 각주가 "`—`는 본문이 확인해 싣지 않은 항목이다. **값이 없다는 뜻이 아니라 이 책이 검증하지 않았다는 뜻**"이라고 설명하는데, **이 책은 검증했다.** 8장 본문이 날짜·👍를 인쇄하지 않았을 뿐이다.
- 비교: 같은 표의 `#28903` 👍 `—`는 **정확하다** ✅ — 원장(`community.md` L42)에 👍가 실제로 없다.
- **수정안 (택1):**
  - **A안(권장):** `#32806` 행을 `2026-07-13 | 54 | closed`로 채운다. 그러면 `—`가 남는 칸은 `#28903`의 👍 하나뿐이 되고, 각주도 그 한 칸에 정확히 들어맞는다.
  - **B안:** 각주 문안을 "원장에 값이 없거나 본문이 싣지 않은 항목"으로 넓힌다.
- A안이 낫다 — 이 책의 다른 이슈 17행은 전부 값이 채워져 있어 한 칸만 비면 오히려 눈에 띈다.

### ⚠️-3. 표 B의 Kwa et al. 행 — 본문이 하지 않은 서지 특정 (FR-23 항목 5)

- **11장은 Kwa et al.을 인용하지 않았다.** 11장 L227이 인용한 것은 `/codex/guides/build-ai-native-engineering-team`이고, 그 가이드가 **METR을 인용한 것**을 "이건 OpenAI의 측정이 아니라 METR의 연구 결과"라고 되짚었을 뿐이다. 논문명·저자·arXiv ID를 대지 않았다.
- 참고문헌이 이를 **arXiv:2503.14499(Kwa et al., NeurIPS 2025)로 특정**했다. 서지 자체는 원장에 실재하고 등급도 정확하다 ✅. "7개월마다 배증"도 그 논문의 핵심 수치와 일치한다(`papers.md` L135) ✅
- 다만 두 지점이 본문을 넘어선다:
  1. **11장이 인용한 헤드라인 값 "2시간 17분 / 50% 신뢰도"는 이 논문 항목에 기록돼 있지 않다.** 원장 §2-3이 적은 값은 "Claude 3.7 Sonnet의 50% 시간 지평 ≈ **50분**(2025-03 논문 v1 기준)"이다. 2시간 17분은 가이드가 "as of August 2025"로 인용한 **후속 METR 수치**다.
  2. 표 아래 해설이 **"원문이 스스로 2025년 8월 기준이라고 밝힌 값"**이라 적는데, 11장에서 "원문"은 **OpenAI 가이드**를 가리켰다. 참고문헌에서는 "원문"이 Kwa 논문을 가리키는 것으로 읽힌다 — **지시 대상이 이동했다.**
- ❌가 아닌 이유: 서지·등급·배증률은 원장과 일치하고, METR 시간 지평 연구 계열을 특정한 것 자체는 독자에게 유용하다. **모순이 아니라 본문 범위 초과**이므로 FR-20 기준 ⚠️다.
- **수정안 (택1):**
  - **A안(권장 — 간접 인용임을 표기):** 표 B의 인용 장을 `11장(간접 — OpenAI 가이드가 인용)`으로 바꾸고, 해설을 "**11장이 인용한 수치는 OpenAI 가이드가 METR을 인용하며 '2025년 8월 기준'이라 밝힌 값**이다. 시간 지평 연구의 서지는 위 항목이다"로.
  - **B안:** 표 B에서 이 행을 빼고, 11장 해당 문단에 각주로 서지만 남긴다.
- 이 항목은 **FR-23 항목 5("뒷부속에 새 사실을 도입하지 마라")의 유일한 해당 사례**다. 나머지 부속 전체에서 새 사실 주장은 검출되지 않았다.

## ✅ 확인됨 — 추가 기록

**참고문헌의 자기 한계 고지 3건 — 전부 원장 근거 있음 ✅**
- **"Reddit 인용에는 업보트 수가 빠져 있다"** ✅ — 크롤러 차단으로 Atom RSS 경로를 썼고 그 경로가 업보트를 제공하지 않는다는 사실을 밝혔다. 원장 `community-2.md`의 Reddit 표에 실제로 👍 열이 없다 ✅. **GitHub·HN에는 지표가 있다는 대비까지 적은 것이 정확**하다
- **"진영 편향 고지"** ✅ — r/codex 편중과 "자기 진영에 불리한 진술에 더 큰 무게를 뒀다"는 서술이 실제 처리와 일치한다(Ok_Economist3865 자기 반증을 10장에서 가장 길게 인용) ✅ 규율 9의 정신
- **"한국어 전환 마찰 1차 증언은 한 건이 사실상 전부"** ✅ — 원장 `community-2.md` L552와 일치하며, **3장 final의 한정 표현("전환 마찰을 구체적으로 남긴 한국어 1차 증언")과 정합** ✅ (파 1 ⚠️-2 수정이 부속에도 반영됐다)

**국내 1차 소스 3건 서지 ✅** — AWS(Kyutae Park, Ph.D, AWS AI 스페셜리스트 SA, 2026-06-11) / dcinside 코유키1357(2026-04-28, 조회 7,507) / GeekNews bungker(2026-04-15). 저자·날짜·성격 라벨 전건 원장 일치

**GitHub 이슈 댓글 표 11행 ✅** — 인용자·이슈·게시일이 파 1~4에서 검증한 값과 전건 일치(archneon/Alek2077 2026-02-17 · suparious 2026-05-01 · miraclebakelaser 2026-02-18 · anrooo 2026-05-15 · leonardo-panseri 2026-06-04 · ScyDev 2026-06-28 · gergo-hortobagyi 2026-06-24 · irm-codebase 2026-06-28 · aldegad 2026-04-28). **backnotprop이 추가돼 있다** — 파 3 9장 ⚠️-2에서 요청한 화자 병기가 부속에도 반영됐다 ✅

**⏳ 등급 설명 ✅** — "⏳가 붙은 항목은 본문이 시점 낡음을 명시한 것"이라는 정의가 범례와 일치하고, 실제로 ⏳가 붙은 유일한 행(Kwa)에 대해 11장이 "한 해가 지난 값"이라 적었다 ✅

**참고문헌 마감 문장 ✅** — "위 URL과 상태는 그 시점에 확인한 것이다. 지금 값이 궁금하면 이 목록에서 번호를 골라 열어보자." 3장부터 이어온 🕒 문형의 마지막 적용 ✅

## 뒷부속 검증 패스 판정 — **통과 (BLOCKING 0건)**

1. **❌ 0건** — 확인 등급 라벨·URL·수치·서지 전건 원장 일치
2. **구성 URL 0건** — Reddit thread ID 6개, HN item ID 10개, arXiv ID 12개 전수 실재 확인
3. **직접 카운트 3건 전부 캡션과 일치** — 148 URL / 이슈 18건 / 문헌 13건(📄 8 + ✅ 4 + ❌ 1)
4. **FR-1·FR-2·FR-15·FR-16 준수** — 은퇴 문안 세 번째 사본 없음, 시점 변형 표기 0건(style C2 수정 확인), best-practices HTML 복원 표기 정확, 재집계 정확
5. **⚠️ 3건은 전부 비블로킹** — HTML 주석 잔여 / `#32806` 빈 칸 / Kwa 서지 귀속

**→ 원고 전체(본문 12장 + 부속)가 사실 정확성 기준으로 Phase 4.5에 넘어갈 수 있다.**

### manuscript-reviewer에게 넘기는 사항

- **⚠️-1(HTML 주석 `<!-- 추출 행 수: 148 -->`, L2999)은 Phase 4.5의 "금지 잔여 마커" 검사와 겹친다.** 사실 오류가 아니므로 fact 쪽에서는 비블로킹이지만, 수락 게이트 기준으로는 별도 판정 대상일 수 있다
- ⚠️-2·⚠️-3은 editor가 반영 가능한 국소 수정이다
- 본문 12장에 대해서는 **에스컬레이션 잔여 0건**(파 4 종료 판정 참조)
