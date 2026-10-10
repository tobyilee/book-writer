# AI 코딩 에이전트 신뢰 곡선 — 저술 계획

- 슬러그: `agentic-dev-trust-curve` · 장르: tech-book · delegation_mode: production
- 레퍼런스: `agentic-dev-trust-curve/01_reference.md` (2026-10-10 검색 시점)
- 프로필: `profiles/tech-book/` (voice · scaffolds · style-checklist)

## 제목 후보

1. **에이전트를 믿어도 될까** — 신뢰 곡선으로 배우는 Claude Code·Codex 실전 개발 (Java/Spring·React/Next.js) — 톤: 독자의 질문을 그대로 표지에. 포지셔닝: "써봤지만 맡기기엔 불안한" 개발자의 첫 의심에서 출발하는 책
2. **신뢰 곡선을 오르는 개발자** — 지켜보기에서 자동 머지까지, AI 코딩 에이전트에게 일을 맡기는 법 — 톤: 여정·성장. 포지셔닝: Lauren Tan 워크숍 프레임을 전면에, 독자가 자기 위치를 찍고 한 칸씩 올라가는 안내서
3. **검증하는 에이전트, 설계하는 개발자** — Claude Code와 Codex로 Spring·Next.js 저장소를 에이전트 친화적으로 만드는 법 — 톤: 역할 전환(헤드 셰프). 포지셔닝: 도구 사용법이 아니라 "저장소를 바꾸는" 책

**추천:** 후보 1 (독자가 막혀 있는 지점이 제목이고, 부제가 프레임·도구·스택을 다 싣는다. 후보 2는 Lauren의 프레임을 모르는 독자에게는 "신뢰 곡선"이 낯설고, 후보 3은 대상 독자보다 한 단계 위 독자에게 말을 건다.)

## 책 특성

- 장르: tech-book (Toby 문체, 신선도 규율 강)
- 분량: 본문 12장 약 **60,000자**(장당 4,500~5,500자, 순수 산문 기준) + 부록 A·B 약 3,000자. 소절은 장당 4~6개, 소절당 3,000자 상한.
- 난이도: 중급 (Spring Boot·Next.js로 실제 서비스를 만들어 본 사람. Claude Code 또는 Codex를 한 번이라도 써 본 사람)
- 독자 여정: "AI 도구를 써봤고 빨라진 것 같은데, 리뷰·교정에 시간을 더 쓰고 있다. 에이전트에게 맡기자니 어디까지 맡겨도 되는지 모르겠다" → "내가 신뢰 곡선의 어느 단계에 있는지 안다. 내 저장소에 격리·검증 스킬·하드 집행·교차 리뷰를 순서대로 달 수 있고, 다음 단계로 올라갈 조건과 올라가지 말아야 할 신호를 안다"
- 각성 지점: 1장(빨라진 게 아니라 검증이 느린 것) · 4장(내가 검증자면 병목) · 9장(리뷰 코멘트는 집행 실패의 증상)
- 핵심 요약 박스(`### 이 장의 핵심`): 개념 밀도가 높은 **1·4·7·9장**에만 둔다. 다른 장은 쓰지 않는다.
- 그림: mermaid 규약(`그림 N.` 캡션, 장마다 1부터). 1장(곡선+기둥), 4장(게이트 4단), 9장(집행 피라미드), 10장(워크트리·클라우드 흐름), 11장(교차 리뷰 흐름)에 각 1개 이상.

## 내러티브 아크

이 책의 척추는 **신뢰 곡선의 단계**다. 독자의 질문이 "어디까지 맡겨도 되나"이기 때문에, 독자가 고르는 축(0단계 격리 → 1단계 지켜보기 → 2단계 자가 검증 → 3단계 클라우드 → 4단계 자동 머지)을 책의 순서로 삼는다. Lauren의 **세 기둥**은 독립된 부로 떼지 않고, 각 기둥이 "다음 단계로 올라가기 위해 필요해지는 지점"에 접어 넣는다 — 기둥 1(검증)은 1→2단계 사이에, 기둥 2(스킬+eval)는 2단계를 유지하는 수단으로, 기둥 3(아키텍처+집행)은 2→3·4단계로 병렬화하기 **전에** 반드시 깔아야 하는 바닥으로.

1부(1~3장)는 지도와 바닥이다. 1장이 METR의 "숙련자는 19% 느려졌다"와 Lauren 자신의 "리뷰하느라 시간을 더 쓴다"를 맞붙여, 문제가 코드 생성이 아니라 **검증 비용**이라는 것을 보인 뒤 신뢰 곡선과 세 기둥을 지도로 편다. 여기서 "토큰 무제한" 반론을 Lauren 본인의 답으로 **첫 장에서** 받는다 — 제약이 강한 코드베이스일수록 싼 모델도 잘한다는 ROI 논리. 2장은 커뮤니티의 "YOLO가 너무 이르다" 반론을 흡수하는 0단계: 믿기 전에 가둔다(권한 모드·deny·sandbox·VM·자격증명 분리). 3장은 1단계를 "못 믿는 상태"가 아니라 **학습 단계**(백시트 드라이버, 툴 콜 읽기, 작은 커밋, 실패하는 테스트 먼저, CLAUDE.md/AGENTS.md에 뭘 넣고 뭘 빼나)로 재해석한다.

2부(4~6장)는 기둥 1이다. 4장이 검증을 정의한다 — "다시 확인해봐"는 검증이 아니고(Huang), 실행 피드백이 있을 때만 자기 수정이 작동하며(Self-Debug·Reflexion), 설명은 과신을 만드니(Bansal) **단언이 아니라 증거**를 받아야 한다. 그다음 두 장이 스택 번역이다. 5장 Java/Spring: 에이전트가 `./gradlew test`를 기다리다 멈추는 문제 → 슬라이스 테스트·Testcontainers 재사용·Modulith `verify()`로 **검증 단위 시간을 1분 안으로**. 6장 React/Next.js: 스크린샷만 보고 성공을 선언하는 문제 → 기능 지도(Feature Map) + Playwright/DevTools MCP로 Act→Observe→Compare→Report, 그리고 `next build`가 린트를 안 돌리는 함정.

3부(7~8장)는 기둥 2다. 7장은 스킬을 "5초 전 입사한 엔지니어 온보딩"으로 소개하고 CLAUDE.md(권고)·스킬(절차)·훅(결정론)을 가르는 기준을 세운다. 8장은 eval — 순서만 바꿔 66/80이 뒤집히는 judge 편향에서 출발해, 숨긴 디렉터리·다른 모델 judge·hill-climb(`/goal`·`/loop`)·`claude plugin eval` ablation으로 "검증자를 검증"한다.

4부(9장)는 기둥 3 — 집행 피라미드. 리뷰 코멘트는 code smell이고, 같은 규칙도 어디서 집행하느냐가 70% vs 0에 가까운 차이를 만든다(Distefano, ⚠️ 2차). Java는 Modulith/ArchUnit/NullAway, React는 boundaries/dependency-cruiser/ESLint로 "가장 짧은 길이 가장 좋은 길"을 만든다. Dune은 베끼는 대상이 아니라 원리로만 쓴다.

5부(10~12장)는 올라가기다. 10장은 "하나를 못 믿으면서 백을 띄우지 말라"를 정량 근거(Brown·Kim)로 못 박고 워크트리 병렬 → 클라우드(Routines·Codex Cloud·Benny 패턴)의 순서를 잡는다. 11장은 두 도구 병용을 **우열이 아니라 교차 리뷰 구조**로 — 같은 모델이 자기 코드를 승인하는 약점(Panickssery)을 Claude 구현 ↔ Codex 비차단 리뷰로 메운다. 12장은 4단계 자동 머지와 토큰·조직 현실을 종합하며 독자가 1장에서 찍은 자기 위치를 다시 찍게 한다.

## 설계 근거

- **채택한 구조: 신뢰 곡선 단계를 척추로, 세 기둥을 단계 사이에 접어 넣고, 스택 번역 장을 기둥 1 뒤에 배치.** 이유 (1) 독자의 결정 축이 "어디까지 맡기나"이므로 단계가 곧 목차가 되어야 자기 위치를 찾기 쉽다. (2) Lauren의 핵심 경고 "단계를 건너뛰지 말라"(L9)와 커뮤니티의 "0단계 격리" 반론은 단계 구조에서만 자연스럽게 자리가 생긴다. (3) 두 도구·두 스택을 한 구조 안에서 다루므로 원리를 한 번만 쓰고 레시피만 갈라진다.
- **기각한 대안 1: 세 기둥 3부 구성** (1부 Verification / 2부 Skills+Evals / 3부 Architecture, 신뢰 곡선은 서문) — 기각 사유: 워크숍 구성과 같아 1차 소스 충실도는 높지만, 독자가 "지금 나는 뭘 해야 하나"를 고를 축이 사라진다. 0단계 격리와 "건너뛰지 말라" 경고가 서문으로 밀려 비중을 잃는다.
- **기각한 대안 2: 도구별 2부 구성** (Claude Code 편 / Codex 편 + 병용 장) — 기각 사유: 커뮤니티의 "왕좌" 담론("최강자가 자꾸 바뀐다")에 책이 종속되어 유통기한이 모델 은퇴 주기(1~2개월)에 묶인다. 기능 대응표로 끝날 위험. 구조는 도구 독립적이어야 하고 도구 사실은 레시피·부록에 가둬야 한다.
- **기각한 대안 3: 스택별 2부 구성** (Java/Spring 편 / React/Next.js 편) — 기각 사유: 검증·스킬·집행의 원리가 두 번 서술되고, 풀스택 독자(대상 독자의 다수)가 같은 내용을 두 번 읽는다. 번역은 기둥 1 아래 두 장(5·6장)과 9장의 스택별 소절로 충분하다.
- **기각한 대안 4: 워크숍 순서 그대로** (기둥 1→2→3→Q&A에서 토큰 반론) — 기각 사유: 워크숍은 이미 올라간 사람의 회고 순서다. "토큰 무제한인 사람 얘기 아닌가"는 독자의 첫 의심이므로 1장에서 받고 12장에서 운영 수준으로 닫아야지, 끝의 Q&A로 두면 책 전체를 의심 속에서 읽게 된다.
- **장 수 12에 대해:** 기본 범위(5~10)를 넘는다. 4단계+0단계, 3기둥, 2스택, 2도구의 곱을 한 구조에 담으려면 스택 번역 2장과 병용 1장이 추가로 필요했다. 7·8장(스킬·eval)을 합치면 9,000자를 넘어 호흡이 무너지므로 분리했다.

## 레퍼런스 한계와 계획의 대응

§7·§9의 미확인 항목에 계획이 기대지 않도록 아래를 저술 제약으로 둔다.

- **숫자 한정:** 월 PR 수는 "2026-07 기준 본인 보고(약 1,000)", 후속은 "이후 본인 발표 기준 2,000~2,500", 항상 "외부 감사 없음" 병기. "20개 PR"은 "그날 아침". 4단계 번호는 "호스트 요약, 본인 동의". 교훈은 "워크숍에서 추린".
- **비공개 산출물:** control-glass·Dune·Benny는 "Lauren의 사례"로만. 따라 할 수 있는 것은 공개 대응물 — `control-ui`/`control-cli`(cursor-team-kit), `verification-skill-example`의 기능 지도 형태, pstack(2026-05-23 공개). "pstack의 control-glass"라고 쓰지 않는다.
- **도구 사실:** 본문은 "2.1.x/2026-10 기준", "0.16x/2026-10 기준" 꼬리표. 모델명은 본문 금지, 부록 A 표로만. Codex의 `/goal`·`/loop` 대응물은 "공식 대응 미확인"으로 쓴다.
- **검증 전 사용 금지:** `no-restricted-syntax`의 `useEffect` 셀렉터는 저술가가 실제로 돌려보고 쓰거나 `(사실 확인 필요)` 표시. ArchUnit의 결함 예방 효과를 정량 주장하지 않는다. Lombok 실패담·PIT는 쓰지 않는다. Sandbagging은 코딩 eval로 일반화하지 않는다.
- **학술 수치:** 생산성 범위(−19%~+55.8%)는 하나를 대표로 세우지 않는다. Distefano "70% vs near-zero"는 ⚠️ 2차로 표기. Wickens 70% 임계값은 2차 인용 한정. arXiv 2607.27250·2602.23905·2601.00753은 인용하지 않는다.
- 리서치 보강이 필요할 수 있는 지점: 한국 대기업 도입 회고(§9), Codex 측 조건 반복 기능. 계획은 둘 다 없이 성립하도록 짰다.

## 용어 표기

| 용어 | 이 책의 표기 | 비고 |
|------|-------------|------|
| Claude Code / Codex | 영문 그대로. 클라우드 제품은 "Codex Cloud", CLI를 구분할 때만 "Codex CLI" | "클로드 코드" 같은 음차 금지 |
| 에이전트 | "에이전트" (첫 등장 시 "AI 코딩 에이전트"). 하위는 "서브에이전트" | "agent" 영문 단독 사용 금지 |
| 신뢰 곡선 | "신뢰 곡선"(첫 등장 시 "신뢰 곡선(Trust Curve)") | |
| 단계 | "0단계 격리 · 1단계 지켜보기 · 2단계 자가 검증 · 3단계 클라우드 · 4단계 자동 머지" | 숫자+이름 세트로 고정. "Stage 0" 등 영문 금지 |
| 세 기둥 | "검증(Verification)", "스킬과 eval", "아키텍처와 집행" | 첫 등장 시 영문 병기, 이후 한국어 |
| 맞는 코드 / 좋은 코드 | 이 두 어구로 고정 | correct ≠ good의 번역 |
| 스킬 | "스킬" (파일은 `SKILL.md`). 검증용은 "검증 스킬" | |
| 훅 | "훅" (이벤트명은 `PreToolUse`처럼 코드 표기) | |
| 워크트리 | "워크트리" (플래그는 `--worktree`) | |
| 기능 지도 | "기능 지도(Feature Map)" 첫 등장 후 "기능 지도" | |
| eval / judge | "eval"·"judge 모델" 영문 소문자 그대로 | "평가"로 번역하지 않음(일반 명사와 혼동) |
| 집행 레이어 | "집행 피라미드", "하드 레이어"(컴파일러·린트·CI·훅), "소프트 레이어"(CLAUDE.md·스킬·리뷰 봇) | |
| 교차 리뷰 | "교차 리뷰" | cross review |
| 자동 머지 | "자동 머지" (GitHub 기능은 "auto-merge" 코드 표기) | |
| 권한 모드 | `default`·`acceptEdits`·`plan`·`auto`·`dontAsk`·`bypassPermissions` 코드 표기 | Codex는 `--sandbox read-only` 등 플래그 그대로 |
| 슬라이스 테스트 | "슬라이스 테스트"(`@WebMvcTest`·`@DataJpaTest`) | |
| 인물 | "Lauren Tan(Cursor, React Compiler 코어팀)" 첫 등장, 이후 "Lauren". 직함 금지 | §2-1 정전 |
| 제품 | pstack(소문자) · Grok Bot(두 단어) · control-glass · Dune · Benny · gstack · Bugbot | §2-2·§2-3 매핑표 |
| 버전 꼬리표 | "2.1.x/2026-10 기준", "0.16x/2026-10 기준", "Spring Boot 4.1/2026-10 기준", "Next.js 16/2026-10 기준" | 정확한 패치 버전은 부록 A에만 |
| 모델명 | 본문 금지. 부록 A 표에만 | 은퇴 주기 1~2개월 |
| 문서 링크 | Claude Code `code.claude.com/docs`, Codex `learn.chatgpt.com/docs`(구 developers.openai.com/codex 병기) | |

## 챕터 목록

### 1장. 빨라졌는데 왜 더 피곤할까 — 신뢰 곡선이라는 지도
- **핵심 질문:** AI로 코드를 빨리 쓰는데 왜 전체 시간은 안 줄어들까? 그 병목을 치우는 길은 어떤 순서인가?
- **주요 내용:**
  - METR 2025(숙련 OSS 개발자 16명, AI 허용 시 19% 더 오래 걸림, 사전 예측은 −24%)와 Lauren의 오프닝 발언("리뷰하고 고치는 데 시간을 더 쓴다")을 맞붙임. 생산성 범위(−19%~+55.8%)는 하나를 대표로 세우지 않고 "가르는 변수 = 검증 부담"으로
  - 신뢰는 감정이 아니라 보정(calibration) 문제 — Lee & See 2004의 overtrust→misuse / distrust→disuse, 관찰로 갱신되는 learned trust(Hoff & Bashir)
  - 신뢰 곡선 4단계(Lauren이 그린 곡선을 호스트가 4단계로 요약, 본인 동의) + 커뮤니티의 0단계 격리 반론을 미리 예고. "단계를 건너뛰지 말라"(26:41, 28:01)
  - 세 기둥과 "맞는 코드 ≠ 좋은 코드"(06:29) — 기둥 1은 correctness, 기둥 3은 quality
  - "토큰 무제한인 사람 얘기 아닌가" 반론을 정면으로: Lauren 본인의 답(47:57 "모두가 똑같이 할 수는 없다", 48:09 "breaking the bank 없이 가능", 50:02 ROI, 50:17 제약 강한 코드베이스는 싼 모델도 잘함). 12장에서 운영 수준으로 닫는다고 예고
  - 호스트의 "대부분 로컬 2~3개"(47:12)로 독자 위치 가늠
- **독자가 얻는 것:** 문제의 이름(검증 비용), 지도(단계·기둥), 자기 위치
- **저장소 행동:** 지난 2주의 에이전트 세션을 돌아보고 "내가 손으로 검증한 것 / 에이전트가 증거를 낸 것"을 나눠 자기 단계를 한 줄로 적는다
- **레퍼런스:** §1-1~1-4, §1-7(47:43 토큰 Q&A), §5-1(METR·Lee & See·Hoff·Peng·Cui·Paradis), §5-2 생산성 범위, §6-8 Hashimoto·토스
- **오프닝 기법:** 충격적 수치 — "사전 예측 −24%, 실측 +19%"
- **클로징 기법:** 독자 자기 진단 — "당신은 어디에 서 있나"를 적게 하는 질문
- **스캐폴드 유형:** 개념 도입형 (핵심 요약 박스 사용)
- **예상 분량:** 5,000자

### 2장. 0단계 격리 — 믿기 전에 가둬라
- **핵심 질문:** 신뢰를 쌓기 시작하기도 전에, 에이전트가 할 수 없어야 하는 일은 무엇인가?
- **주요 내용:**
  - 커뮤니티 반론 흡수: "YOLO 모드가 너무 이르게 온다"(HN 47923275), 멀리 숨긴 데이터 폴더를 레퍼런스 하나로 찾아간 사례(HN 48348578 — "VM을 써라"), mtlynch "모든 접근을 줘야만 쓸 만하다", GeekNews "샌드박스는 기본 꺼져 있다". Lauren 자신도 "인턴이 프로덕션 DB를 지우지 않게 자격증명을 제한"(31:28)이라고 말함 — 반론이 아니라 전제
  - Claude Code 권한 모드 6종(`default`→`acceptEdits`→`auto`→`dontAsk`→`bypassPermissions`)을 신뢰 단계에 대응. `auto`는 2.1.283+ 대화형 기본 — 분류기 모델이 행동을 사전 검토. "Deny rules는 `bypassPermissions`에서도 막는다". `claude -p --bare`(신뢰 안 한 폴더의 훅·MCP 실행 방지)
  - Codex `--sandbox read-only|workspace-write|danger-full-access`, `-a on-request|never`, `--yolo`는 "격리된 러너 안에서만". 자동화의 조용한 `workspace-write` 폴백(#15310), 민감 파일 제외(#2847), Windows 샌드박스(#51601)
  - 자격증명 분리·별도 머신·VM vs 컨테이너 논쟁(관점 병기). 워크트리의 `.worktreeinclude`로 `.env`를 복사할 때 무엇을 빼야 하나
  - 신뢰 단계 ↔ 권한 매핑표(§4-4)의 0·1단계 줄
- **독자가 얻는 것:** "끄고 자도 되는" 최소 격리 설정
- **저장소 행동:** deny rules(프로덕션 자격증명·`rm -rf`·`git push --force`류) + Codex `config.toml` 샌드박스 기본값을 저장소에 커밋하고, 에이전트 전용 자격증명을 분리한다
- **레퍼런스:** §3-2 권한 모드·`--bare`·Worktrees, §3-3 샌드박스·승인, §6-1 권한·샌드박스 우회, §6-7, §4-4
- **오프닝 기법:** 실패 장면(in medias res) — 레퍼런스 하나를 보고 숨긴 폴더를 찾아가는 에이전트
- **클로징 기법:** 체크리스트 과제 — "오늘 밤 이 다섯 줄이 켜져 있는가"
- **스캐폴드 유형:** 문제-해결형
- **예상 분량:** 4,500자

### 3장. 1단계 지켜보기 — 운전석에 앉되, 배우는 자리로
- **핵심 질문:** "모든 출력을 지켜보는" 단계는 낭비인가, 아니면 다음 단계의 재료를 모으는 시간인가?
- **주요 내용:**
  - 백시트 드라이버(20:08~20:46): 툴 콜·읽은 파일·thinking을 열어 본다 = learned trust의 입력. Lauren의 `how` 스킬이 여기서 나왔다("코드를 안 읽고 추측하더라")
  - 작게 자르기: 세션 = 이슈 1개, 커밋 단위로 묶기(HN phillipcarter·altern8), 원자적 PR과 "git history는 컨텍스트"(36:57). 실패하는 테스트 먼저(토비 라이브 gist: N+1 검증 테스트)
  - 1단계의 Java/React 함정: "스프링 이니셜라이저를 써"라고 안 하면 Gradle을 손으로 쓰다 버전 충돌(토비 라이브) / Next.js 15+ 비동기 request API·`"use client"` 경계 — 모델 지식 컷오프 vs 프레임워크 메이저. 해법은 버전 고정 규칙을 CLAUDE.md/AGENTS.md **와** 린트 양쪽에(9장 예고)
  - CLAUDE.md/AGENTS.md에 무엇을 넣나: "없애면 실수하는가? 아니면 지워라"(공식 best practices), 토스 "자주 수정하고 있다면 거기 있으면 안 되는 것", 비표준 관행만(Gloaguen: 저장소 개요 무용). 효과의 상충 — 성공률 불변+비용↑(Gloaguen) vs 시간·토큰↓(Lulla) = "똑똑하게"가 아니라 "헤매지 않게"
  - 지시 망각은 설정 버그가 아니라 모델 행동(#32650 "Reading ≠ binding", #19471 "✓ Rules loaded" 직후 위반) — 그래서 1단계가 길어지고, 그래서 다음 장이 필요
  - 주니어 성장 논쟁(§6-6 C)을 1단계=학습 단계로 재해석
- **독자가 얻는 것:** 1단계에서 "관찰 기록"을 남기는 습관, 1페이지짜리 지침 파일
- **저장소 행동:** CLAUDE.md 또는 AGENTS.md를 비표준 관행만 남긴 1페이지로 줄이고, 이번 주 관찰한 실패 3개를 `docs/agent-observations.md`에 적는다(7장의 스킬 재료)
- **레퍼런스:** §1-4 기둥 2 세부(how 스킬·백시트), §1-4 기둥 3 PR 크기, §3-2 Best practices·CLAUDE.md, §5-1 Hoff·Gloaguen·Lulla, §6-1 지시 무시, §6-2 작은 작업·실패 테스트·계획 먼저, §6-4 토비 gist, §4-3 ③ 룰, §6-6 C, §6-8 토스
- **오프닝 기법:** 인용·일화 — 토비 라이브 "최선의 스프링 개발자들이 세팅해놓은 최선의 걸 가지고 만들잖아요"
- **클로징 기법:** 한 문장 여운 — 관찰 기록이 곧 다음 단계의 설계도라는 한 줄
- **스캐폴드 유형:** 사례 분석형
- **예상 분량:** 5,000자

### 4장. 당신이 검증자면 병목이다 — 단언이 아니라 증거
- **핵심 질문:** 에이전트가 "다 했다"고 말할 때, 무엇을 받아야 믿을 수 있나?
- **주요 내용:**
  - 검증의 정의(06:10): 에이전트가 **앱을 실제로 실행·측정·확인**하는 능력. 사람이 검증자면 병렬화 불가(08:48, 09:13). 공식 문서 대응: "Without a check it can run, you become the verification loop"
  - Lauren 첫 주 플레임 그래프 장면(07:05): 스크린샷을 붙이면 자신 있게 엉뚱한 원인을 짚는다 → 에이전트가 스스로 트레이스를 뜰 수 있어야
  - 학술 삼각: "다시 확인해봐"는 검증이 아니다(Huang — 외부 피드백 없는 자기 교정은 악화) / 실행 피드백이 있으면 작동(Self-Debug 단위 테스트 +12%p, Reflexion 91%는 테스트 피드백 有) / 설명은 맞든 틀리든 수용을 올리고 성능은 그대로(Bansal) → 설명 대신 실행 증거. 검증 비용이 크면 사람은 stamp한다(Vasconcelos)
  - "통과"와 "증거"의 차이: 테스트 전부 초록인데 커버리지 68→61·`@Transactional` 소실(dev.to 200K), 목으로 도망간 VibeTDD, "find the exact edge of your success criteria and stop there"
  - 게이트 4단(공식 best practices): 프롬프트 안 조건 → `/goal`(완료 판정은 작업 모델이 아닌 fresh 모델, 단 명령 실행·파일 읽기는 안 함) → Stop 훅(결정론, exit 2, `onFailure: "block"`) → 검증 서브에이전트(fresh context). Codex 쪽은 `codex exec -s workspace-write -a never` + 셸 루프로 대응(공식 조건 반복 기능은 미확인)
  - 커밋 전 `verify` 스킬(2.1.286+) — "show evidence rather than asserting success"
- **독자가 얻는 것:** 검증의 조작적 정의와 게이트를 어디에 거는지
- **저장소 행동:** 에이전트가 **스스로 실행할 수 있는 체크 1개**(테스트·빌드·스크린샷 비교)를 고르고 `/goal` 조건 또는 Stop 훅으로 건다
- **레퍼런스:** §1-4 기둥 1 세부, §1-7(17:23), §3-2 `/goal`·Hooks·Best practices·Skills(verify), §3-3 `codex exec`, §5-1 Huang·Chen·Shinn·Bansal·Vasconcelos·Anthropic Building effective agents, §6-1 완료 주장 환각·테스트 고침, §6-4 200K 모놀리스, §6-8 Hashimoto "verify its work"
- **오프닝 기법:** 실패 장면 — 테스트 전부 초록, 커버리지 7포인트 하락, `@Transactional`이 조용히 사라진 아침
- **클로징 기법:** 오프닝 장면 재방문 — 같은 아침을 "증거 기준"으로 다시 보면 어디서 멈췄을지
- **스캐폴드 유형:** 개념 도입형 (핵심 요약 박스 사용, 그림: 게이트 4단)
- **예상 분량:** 5,500자

### 5장. Java/Spring 번역 — 검증 단위 시간을 1분 안으로
- **핵심 질문:** 에이전트가 `./gradlew test`를 기다리다 대화를 멈춘다면, 검증 스킬은 어디서부터 가능한가?
- **주요 내용:**
  - 문제: "Java+Spring Boot는 TS·Python보다 피드백 루프가 길다"(codenote, 단일 저자 측정 — 3~5분, JVM 기동·빈 초기화·컨테이너 부팅, 에이전트 셸 타임아웃). 검증 단위 시간이 길면 에이전트는 검증을 **건너뛰는 쪽으로 최적화**한다(목으로 도망간 VibeTDD와 연결)
  - 처방 1 — 슬라이스 테스트 레인: `@SpringBootTest`(5~15s) 대신 `@WebMvcTest`(0.3~0.8s)·`@DataJpaTest`(0.5~1.5s), Gradle 데몬·병렬·configuration cache. 에이전트가 1분 안에 돌릴 `quickCheck` 태스크와, 사람/CI가 돌릴 전체 레인을 분리(수치는 codenote 측정치로 한정)
  - 처방 2 — 앱을 실제로 띄우는 검증: Testcontainers `@ServiceConnection`(spring-boot-testcontainers, 4.1 기준) + 컨테이너 재사용. "plain HTTP for services" 경로 = Java의 control-ui
  - 처방 3 — 아키텍처를 테스트 한 줄로: Spring Modulith `ApplicationModules.of(App.class).verify()`(2.1 기준 — 모듈 순환 금지, API 패키지 외 접근 거부, `@ApplicationModule(allowedDependencies)`), ArchUnit `layeredArchitecture()`·네이밍 규칙(Adapter/Wrapper/Compat/Legacy 정당화 필수 — 200K 모놀리스 사례). ArchUnit 효과의 정량 주장은 하지 않음
  - 처방 4 — 컴파일러를 엄격하게: Error Prone + NullAway + JSpecify(`-Werror`, NullAway는 기본 경고라 ERROR로 올려야 CI가 빨개짐; 기존 코드베이스는 NullAway만 켜고 시작). Rust 비유(45:36)의 Java 판
  - 린트로 못 올리는 것의 예: 트랜잭션 경계 — "사람이 반드시 리뷰". Spring 함정 목록(`@Transactional` self-invocation·N+1·fetch join+Pageable·"Resume does not exist: ID=35" 행복 경로 편향)은 CLAUDE.md/AGENTS.md 룰 + 가능한 것은 테스트로
  - Spring Boot 4.0/4.1·Java 25 환경 꼬리표, 버전은 부록 A
- **독자가 얻는 것:** 에이전트용 빠른 검증 레인과 사람용 전체 레인의 2층 구조
- **저장소 행동:** 1분 안에 끝나는 `./gradlew quickCheck`(슬라이스 테스트 + Modulith/ArchUnit verify + NullAway)를 만들고 에이전트 지침에 "커밋 전 quickCheck"를 적는다
- **레퍼런스:** §4-1, §4-2 전체, §6-4, §6-1 테스트 고침, §1-4 기둥 3 언어 선택(45:36), §5-1 Pearce(SAST)
- **오프닝 기법:** 수사적 질문 — "왜 에이전트는 빌드를 기다리다 대화를 멈춰 버릴까?"
- **클로징 기법:** 측정 지표 제시 — "검증 단위 시간" 숫자 하나를 재고 다음 장의 전제로 넘김
- **스캐폴드 유형:** 문제-해결형
- **예상 분량:** 5,500자

### 6장. React/Next.js 번역 — 브라우저를 에이전트 손에
- **핵심 질문:** 스크린샷이 멀쩡하면 끝난 것인가? 에이전트가 사용자처럼 앱을 "만져 보게" 하려면 무엇이 필요한가?
- **주요 내용:**
  - 사례: "스크린샷 도구가 있어도 깨진 페이지에서 성공을 선언한다"(qaskills) — 스크린샷에만 보이는 실패(빈 영역·CSS 충돌·좁은 뷰포트·올바른 컴포넌트에 잘못된 데이터)와, 스크린샷으로 안 보이는 실패
  - 원리 추출: 도구보다 **기능 지도(Feature Map)**가 먼저(10:17~13:10 — 스킬이 있어도 "Agents Window가 뭔지 몰랐다"). 공개 형태는 `verification-skill-example`의 기능별 4개 H2(Sub-features / How to get to it (user POV) / Driving it / Gotchas). "???"+스크린샷 수준 리포트도 재현 가능해야. 루프: Act → Observe → Compare(명시된 기대) → Report
  - control-glass는 비공개·Lauren의 사례. 독자는 만들지 않고 MCP로 대체: Playwright MCP(접근성 트리 스냅샷, `browser_snapshot`·`click`·`fill_form`·`network_requests`) = 행동, Chrome DevTools MCP(트레이스·콘솔·성능) = 진단, Next.js 16 DevTools MCP(브라우저+서버 로그 통합) = 프레임워크 내장. 토큰 비용 주의(접근성 스냅샷이 스크린샷보다 비쌀 수 있다는 단일 저자 측정, HN "token burner")
  - 함정 1: `next build`는 린트를 안 돌린다(Next.js 16 — `next lint` 제거, Biome/ESLint 직접) → CI에 ESLint 단계를 명시적으로. `@next/eslint-plugin-next` Flat Config
  - 함정 2: Dune의 `useEffect` 금지를 ESLint로 — `react-hooks/exhaustive-deps: error` + `no-restricted-syntax`(셀렉터는 저술 시 실제 확인 후 기재). 왜 금지하나: "9 Patterns" 1위 useEffect+useState 페칭, React 19.2 공식 "대부분 린트를 끄는데 그러면 버그". 전면 금지 vs 예외 허용은 비교 대조로 짧게
  - 시각 회귀를 하드 게이트로: Storybook + Chromatic "UI Tests" required check
- **독자가 얻는 것:** 기능 지도 + MCP 2종 + 린트 함정 2개를 아는 프런트 검증 레인
- **저장소 행동:** `features/README.md`에 핵심 기능 1개의 기능 지도를 쓰고 Playwright MCP를 연결해 에이전트가 그 기능을 "사용자처럼" 한 번 통과하게 한다
- **레퍼런스:** §1-4 기둥 1 세부(Feature Map·control-glass), §2-2(verification-skill-example·control-ui), §4-1, §4-3 전체, §6-5, §7-1 C7, §7-2 19번
- **오프닝 기법:** 상황 가정 — "배포 직전, 에이전트가 보낸 스크린샷은 멀쩡하다. 그런데 버튼이 눌리지 않는다고 해보자"
- **클로징 기법:** 경고·반전 — "MCP만 붙이면 성공 선언만 늘어난다 — 지도가 먼저다"
- **스캐폴드 유형:** 사례 분석형
- **예상 분량:** 5,500자

### 7장. 스킬 — 5초 전 입사한 엔지니어를 가르치는 법
- **핵심 질문:** 관찰한 실패를 어디에 적어야 다음 세션에서 같은 실패가 안 나오나 — 지침 파일, 스킬, 훅 중 어디에?
- **주요 내용:**
  - 매니저 비유(15:33): 코딩은 잘하는데 맥락이 0인, 5초 전 입사한 엔지니어. 온보딩 문서 = 스킬. latent space 이야기(16:01)는 "좋은 토큰을 먼저 주면 더 나은 패턴에 매칭한다" 정도로만
  - 스킬은 마크다운이고 프레임워크가 필요 없다(16:01, 17:52). Agent Skills 오픈 표준 — 같은 `SKILL.md`를 `.claude/skills/`와 `.agents/skills/`에 두면 Claude Code·Codex 양쪽에서 동작. frontmatter(`description`·`disable-model-invocation`·`allowed-tools`·`context: fork`·`hooks`)
  - 세 서랍의 기준: CLAUDE.md/AGENTS.md = 항상 보이는 권고(advisory), 스킬 = 필요할 때만 로드되는 절차, 훅 = 결정론("hooks are deterministic and guarantee the action happens", "To block regardless of what Claude decides, use a PreToolUse hook"). 판단 규칙: 매번 어기면 훅으로, 가끔 필요하면 스킬로, 그래도 남으면 지침으로. Positive phrasing("Don't do X"는 X를 컨텍스트에 심는다)
  - 스킬이 떴다고 의도대로 한 것은 아니다("Seeing a skill trigger tells you Claude found it, not that it did what you intended"). Vercel 평가 "56%에서 스킬이 호출조차 안 됨"(2차). fresh session on/off 비교, `/skill-doctor`
  - 유지보수는 어렵다(20:08 "taste와 관찰"). pstack은 설계된 게 아니라 축적(14:11). `how`·`verify`·`create-verification-skill`의 유래. 토스의 하네스 비유(Skills=컴포넌트)
  - 남의 플러그인은 포크하라(28:30 "blindly trust me 하지 말라"). pstack(2026-05-23 공개, MIT)·gstack(`./setup --host codex`로 Codex 지원)을 출발점으로
- **독자가 얻는 것:** 관찰→스킬→훅 승격 사다리와 두 도구에 동시에 설치되는 스킬 구조
- **저장소 행동:** 3장의 관찰 기록에서 실패 1개를 골라 `SKILL.md` 하나로 쓰고 `.claude/skills/`·`.agents/skills/` 양쪽에 둔다
- **레퍼런스:** §1-4 기둥 2 세부, §1-5 비유, §1-6 L10, §3-2 Skills·Hooks·Best practices, §3-3 Skills, §3-5 스킬 행, §5-1 Mei, §6-1 지시 무시(Vercel), §6-2 린트/CI/훅 가드레일(Positive phrasing), §6-8 토스
- **오프닝 기법:** 인용·일화 — "5초 전에 입사한, 코딩은 정말 잘하는 엔지니어가 있다고 Lauren은 말한다"
- **클로징 기법:** 인용으로 닫기 — "fork it, make it your own"
- **스캐폴드 유형:** 개념 도입형 (핵심 요약 박스 사용)
- **예상 분량:** 5,000자

### 8장. eval — 스킬의 단위 테스트, 그리고 검증자를 검증하기
- **핵심 질문:** 스킬이 "좋아졌다"는 것을 어떻게 알까? 그 판정을 내리는 모델은 또 누가 검증하나?
- **주요 내용:**
  - 충격: 답 순서만 바꾸면 80문항 중 66문항이 뒤집힌다(Wang 2024). judge 편향 4종(위치·장황함·자기 강화·제한 추론, Zheng). 같은 모델이 자기 결과를 채점하면 자기 선호가 선형으로 는다(Panickssery)·원인은 익숙함(Wataoka). 벤치마크도 검증이 필요했다(SWE-bench Verified: 1,699→500)
  - 선택지 A — Lauren의 eval 파이프라인(18:46~19:52): 코디네이터가 루브릭 → 서브에이전트 N개를 격리 디렉터리에 → **평가 중임을 모르게 디렉터리명을 숨김**(모델은 평가 상황을 알아챈다, Needham AUC 0.83 — sandbagging은 위험 역량 평가 맥락의 결과이니 코딩 eval로 일반화하지 않음) → 다른 모델 judge → "스킬을 고칠 때마다 하나는 돌린다". hill-climb: Cursor `/loop … until 10/10`의 Claude Code 대응은 `/goal`(조건) + `/loop`(시간, 7일 만료). 검증 스킬 자체도 같은 절차로(21:15 verify the verifier)
  - 선택지 B — `claude plugin eval`(2.1.269+): 케이스 = 프롬프트 + 그레이더 6종(`regex`·`tool_used`·`tool_order`·`file_exists`·`llm`·`baseline`), **기본 3회 × with/without = 6런 ablation**, `--judge-model`로 다른 모델, 임계값 미달 시 non-zero로 CI 게이트. "`tool_used: Skill`이 통과했는데 Δ가 음수면 플러그인보다 judge를 의심하라". 빌드·테스트 통과는 결과를 파일에 쓰게 해 `file_exists`로
  - 기준: 둘 다 블라인드·다른 모델 judge. A는 자유도·스택 무관, B는 ablation이 기본이고 CI에 바로 붙는다. 스킬이 Claude·Codex 공용이면 A로 양쪽 돌리고, Claude 전용이면 B
  - 비용 반론: 여러 작은 모델 패널이 단일 큰 judge보다 일치율↑·비용 1/7(PoLL). promptfoo·Braintrust는 각주
  - "a skill that worked well last month might behave differently today"(skill-creator 블로그) — 모델이 바뀌면 eval을 다시
- **독자가 얻는 것:** 스킬 수정의 회귀 테스트와 judge를 못 믿을 때의 체크
- **저장소 행동:** 7장의 스킬에 eval 케이스 3개를 붙여 with/without 비교를 한 번 돌리고 Δ를 기록한다(`claude plugin eval` 또는 격리 디렉터리 + 다른 모델 judge)
- **레퍼런스:** §1-4 기둥 2 세부(eval·judge·hill-climb·verify the verifier), §1-7(17:13·17:23), §3-2 `claude plugin eval`·`/loop`·`/goal`·skill-creator, §3-5 반복/조건 행, §4-3 eval 도구, §5-1 Zheng·Wang·Panickssery·Wataoka·Verga·Gu·Needham·van der Weij·SWE-bench Verified, §5-2 Sandbagging
- **오프닝 기법:** 충격적 수치 — "답의 순서만 바꿨더니 80문항 중 66문항이 뒤집혔다"
- **클로징 기법:** 명시적 다음 장 이음(변주) — "eval이 10/10이어도 '맞는 코드'까지다. '좋은 코드'는 다른 기둥이 받친다"
- **스캐폴드 유형:** 비교 대조형
- **예상 분량:** 5,500자

### 9장. 리뷰 코멘트는 code smell이다 — 집행 피라미드
- **핵심 질문:** 같은 규칙인데 왜 어떤 저장소에서는 지켜지고 어떤 저장소에서는 썩어 가나?
- **주요 내용:**
  - 정의 뒤집기: 코드 리뷰를 "마지막 방어선"이라 부르지만, Lauren은 사람이 입으로 불변식을 집행하는 "코드 리뷰 랜드"를 최악의 자리라 한다(46:18). 리뷰 코멘트마다 물어라 — 린트로? CI 실패로? 아예 범주적으로 제거?(46:35). Willison "모든 줄을 눈으로 보는 건 한 번도 최선이 아니었다"
  - 집행 피라미드(42:13~45:22): ① 아키텍처·컨벤션("에이전트는 기존 패턴을 베끼길 좋아한다" — 가장 강함) ② 컴파일러·린트·CI(빨간불) ③④⑤ 룰·스킬·리뷰 봇(소프트, "잊을 수 있다"). "소프트만 있으면 코드베이스가 쓰레기가 되는 건 시간문제"(45:07). Claude Code 공식 Code Review도 "차단하지 않는다"고 명시 — 소프트 레이어
  - 산업 근거: 같은 규칙도 어디서 집행하느냐 — diff time 배포 수정률 70% 이상 vs 워크플로 밖 배치 리스트는 0에 가까움(Distefano, ⚠️ 2차 수치); FindBugs 3회 실패의 교훈(Sadowski 2018); 리뷰 코멘트 다수는 결함이 아니라 관행(Bacchelli) → 자동화 가능(AutoCommenter). Thoughtworks "결정론적 품질 게이트". GN#347 "반복 실패엔 문서를 늘리지 말고 코드베이스를 고쳐라"
  - 가장 짧은 길이 가장 좋은 길(43:34): 기능 = 디렉터리 하나(colocation), "가장 멍청한 에이전트"를 위한 설계. 금지 목록 + CI — 단, "Lauren said never do this"처럼 일회성 피드백을 영구 규칙으로 오해하는 문제(39:09). human slop before AI slop(31:01): 빅테크 가드레일은 "가장 못하는 엔지니어"를 위해 만든 것이라 에이전트에 그대로 맞음
  - 그린필드가 가장 위험(31:58): organic architecture — 정량 징후는 GitClear의 중복 블록 증가(2차, "감소"만 서술). 리라이트 논쟁은 "경우에 따라"로 병기
  - 스택 번역 소절: Java — Modulith `verify()`·ArchUnit(①), NullAway `-Werror`(②), Spring 함정 룰(③). React — 기능 디렉터리 + eslint-plugin-boundaries·dependency-cruiser(①, Ghost 사례), knip(죽은 코드), ESLint+CI 명시 단계(②), `useEffect` 금지(②). 5·6장을 피라미드 좌표로 재배치
  - Dune은 원리만: feature/entry point/transcript card라는 명사, 금지 목록, 임포트 경계 — 세부는 비공개이므로 추측하지 않는다
- **독자가 얻는 것:** 리뷰 코멘트를 피라미드 아래층으로 내리는 반복 절차
- **저장소 행동:** 최근 리뷰 코멘트 10개를 ①②③ 어디로 내릴 수 있는지 분류하고, 1개를 린트 룰 또는 아키텍처 테스트로 승격해 CI에 넣는다
- **레퍼런스:** §1-4 기둥 3 전체, §1-5 비유, §1-6 L6·L7·L8·L11, §1-7(37:41), §2-2 Dune, §3-2 Code Review(차단 안 함), §4-2·§4-3 ①② 행, §5-1 Distefano·Sadowski×2·Bacchelli·Bosu·Vijayvergiya·GitClear·아키텍처 침식, §6-2 린트/CI 가드레일, §6-8 Willison·Thoughtworks·GN#347, §7-1 C17·C19
- **오프닝 기법:** 정의 뒤집기 — "코드 리뷰는 마지막 방어선이라고들 한다. 사실은 집행 실패의 증상에 더 가깝다"
- **클로징 기법:** 비유 회수 — 헤드 셰프: 요리하지 않고 주방을 설계한다(22:48)
- **스캐폴드 유형:** 문제-해결형 (핵심 요약 박스 사용, 그림: 집행 피라미드)
- **예상 분량:** 5,500자

### 10장. 하나를 믿기 전에 백을 띄우지 말라 — 워크트리 병렬에서 클라우드로
- **핵심 질문:** 병렬화는 언제 이득이고 언제 오류를 증폭하나? 로컬과 클라우드 중 어디서 먼저 늘리나?
- **주요 내용:**
  - 앞 장 콜백: 손이 비면 백 개를 띄우고 싶어진다. Lauren: "하나의 출력도 못 믿으면서 백 개를 띄울 수 없다"(03:36), "토큰만 낭비"(26:41)
  - 정량 근거: 검증기가 있을 때만 반복이 이득(Brown — SWE-bench Lite 1회 15.9%→250회 56%, 검증기 없는 과제는 다수결이 못 따라감). 단일 에이전트 기준선이 약하면 독립 병렬이 오류를 17.2배 증폭, 중앙집중은 4.4배(Kim 2025). 병렬 실패 14종 중 한 범주가 "검증·종료"(Cemri MAST). → 2단계(자가 검증)가 3·4단계의 **전제**라는 것의 숫자
  - 선택지 A — 로컬 워크트리: `claude --worktree <name>`(`.claude/worktrees/`, 브랜치 `worktree-<name>`), 서브에이전트 `isolation: worktree`, `/batch`(5~30 서브에이전트, 각자 워크트리), 동시 20개 제한·깊이 3. Codex 서브에이전트는 기본 활성이나 워크트리 격리 언급 없음. "로컬에서 시작하라, 관찰할 수 있으니까"(23:52). 경고: "격리·범위·검증 없이 에이전트만 늘리면 머지·테스트·리뷰 문제가 더 커진다"
  - 선택지 B — 클라우드: Claude Code `--cloud`(노트북 닫아도 계속), Routines(스케줄·API·GitHub 이벤트 트리거, 최소 1시간, 권한 모드 선택 없음), `/autofix-pr`. Codex Cloud(태스크별 워크스페이스), `codex cloud exec --attempts 1–4`(best-of-N — Brown과 연결), 자동화 트리거. Benny 패턴(25:16, Slack 버그 리포트→재현→"이미 main에서 고쳐짐")을 Routines/자동화로 재현하는 설계
  - Agent teams는 선택(experimental, 토큰 "significantly more", 2차 "~7배"). 책의 기본은 서브에이전트+워크트리
  - 야간 실행(Hashimoto End-of-Day, pstack overnight)과 그 전제 — 아침에 무엇을 보나(12장 예고). dev.to 200K 팀이 야간 완전 자율을 **포기**하고 "이슈 1개→계획 승인→검증 스크립트→diff→머지"로 돌아온 사례 병기
  - 압축 후 망각(#19471·#18720)과 `ACTIVE_CONTRACT.md` 우회 — 긴 세션의 현실
- **독자가 얻는 것:** 병렬화 조건표(검증기 유무·기준선)와 로컬→클라우드 진입 순서
- **저장소 행동:** 독립된 이슈 2개를 워크트리 2개로 병렬 처리하고, 둘 다 5·6장의 검증 레인을 통과하는지 본 뒤 1개를 야간 클라우드 세션으로 보낸다
- **레퍼런스:** §1-3 핵심 경고, §1-4 기둥 1 세부(Benny·어디서 시작), §1-7(23:28), §3-2 Subagents·Worktrees·클라우드/Routines·Agent teams·`/batch`, §3-3 Subagents·Cloud·`codex cloud exec`, §3-5 서브에이전트·클라우드·압축 행, §5-1 Brown·Ehrlich·Kim·Cemri, §6-2 워크트리 병렬·계획 먼저·야간 실행, §6-8 Hashimoto
- **오프닝 기법:** 앞 장 콜백 — "앞 장에서 리뷰 코멘트를 린트로 내렸다. 손이 비었다. 그 손으로 백 개를 띄우고 싶어진다"
- **클로징 기법:** 선택 분기 — "이 두 조건이 참이면 클라우드로, 하나라도 거짓이면 로컬에 남는다"
- **스캐폴드 유형:** 비교 대조형 (그림: 워크트리·클라우드 흐름)
- **예상 분량:** 5,000자

### 11장. Claude Code와 Codex 병용 — 우열이 아니라 교차 리뷰
- **핵심 질문:** 두 도구를 왜 같이 쓰나? 같은 모델이 자기 코드를 승인하는 약점을 어떻게 메우나?
- **주요 내용:**
  - 실패 장면: `replace_all`이 `GROQ_URL = GROQ_URL`을 만들고 "다 했다"(HN) — "자기 검증은 절대 못 믿는다". 근거: 자기 선호 편향(Panickssery·Wataoka), Osmani "한 모델의 복사본 넷은 청구서만 커진 리뷰어 하나", 4개 도구 발견의 93.4%는 한 도구만 잡았다(벤더 보고, 방향만). Lauren 21:30 "다른 모델의 judge" — 두 벤더로 구현
  - 레시피 1 — GeekNews 29011 "Claude한테 짜게 시키고 Codex한테 까게 시키기"(한 달, 같은 레포): Claude = 메인 작성자, Codex = **차단하지 않는** 자문 리뷰어. slash command + pre-push 훅 양쪽 같은 래퍼. 왜 비차단인가: 모델 장애·오탐이 `--no-verify`를 유도(Parasuraman의 disuse — 오경보가 잦으면 꺼 버린다). `codex review --base main`(소규모) vs `codex exec` + diff(100파일+). 잡은 것: race condition, null 체크 누락
  - 레시피 2 — OpenAI 공식 `codex-plugin-cc`: `/codex:review`(read-only), `/codex:adversarial-review`(선택한 설계에 도전), `/codex:rescue`, `/codex:transfer`. 설치 3줄. 무인 리뷰 게이트(Stop 훅)는 Claude↔Codex 긴 루프로 사용량 급소모 — OpenAI 자신의 경고
  - 역할은 대칭: "Codex를 메인으로 쓰니 Claude가 결함을 찾더라"(GeekNews 29576), "Opus는 구현자보다 리뷰어로 낫다"(HN petcat), trilateral(Claude 서브에이전트 fresh + Codex + Gemini). 핵심은 **다른 계열**이지 어느 쪽이 위인가가 아님. 지시 준수는 관점 병기(C21)
  - 지침 파일 공유: Claude Code는 CLAUDE.md가 없을 때만 AGENTS.md를 읽음(2.1.277+, 기본 `claude-md-or-agents-md`), Codex는 CLAUDE.md를 읽지 않음(`project_doc_fallback_filenames`로 추가 가능). 전략 3개 — AGENTS.md만 / CLAUDE.md 첫 줄 `@AGENTS.md` / 심링크(Windows 주의). "만드는 법(CLAUDE.md)·리뷰할 것(AGENTS.md) 겹침 80% 넘으면 분업 실패". Codex `## Code Review Rules` — "포맷·린트는 CI에 맡겨라". 스킬은 두 경로에 같은 파일(7장)
  - "두 모델이 일치해도 정답 보장은 없다"(kavtsya #301) — 최종 대조는 코드와 사람. 한국 "왕좌" 담론·토큰 불만과의 거리 두기
  - 모델명·버전은 부록 A로
- **독자가 얻는 것:** 비차단 교차 리뷰 레인과 두 도구가 같은 저장소 지침을 읽게 하는 설정
- **저장소 행동:** pre-push 훅 또는 slash command로 Codex 리뷰 레인(비차단, 결과는 파일로)을 붙이고, AGENTS.md를 두 도구가 모두 읽는지 각 도구에서 확인한다
- **레퍼런스:** §1-4 기둥 2 세부(21:30), §3-2 CLAUDE.md/AGENTS.md, §3-3 `codex review`·AGENTS.md 규칙·codex-plugin-cc, §3-5 전체, §5-1 Panickssery·Wataoka·Verga·Parasuraman, §6-3 전체, §6-8 Osmani, §7-1 C14·C21
- **오프닝 기법:** 실패 장면 — `replace_all`이 만든 `GROQ_URL = GROQ_URL`, 그리고 "다 했습니다"
- **클로징 기법:** 열린 질문 — "두 모델이 같은 답을 냈다. 그러면 누가 최종 승인을 누르나?"(12장으로)
- **스캐폴드 유형:** 문제-해결형 (그림: 교차 리뷰 흐름)
- **예상 분량:** 5,500자

### 12장. 4단계 자동 머지, 그리고 보통 사람의 신뢰 곡선
- **핵심 질문:** 아침에 main을 열었을 때 무엇을 보면 되나? 토큰이 무제한이 아닌 팀에서 이 곡선은 어디까지 현실인가?
- **주요 내용:**
  - 두 아침: Lauren의 "20개 PR이 이미 main에 있었고 괜찮았다"(03:52, 그날 아침) vs 독자의 "45분 만에 증발한 세션 크레딧"(#16157 1,499 댓글·codex #14593 630 댓글). 같은 기술, 정반대 경험 — 차이는 게이트와 코드베이스
  - 되짚기(연결): 0단계 가둠 → 1단계 관찰 → 2단계 증거(기둥 1) → 스킬·eval로 유지(기둥 2) → 집행으로 바닥(기둥 3) → 병렬·클라우드 → 교차 리뷰. 단계마다 "올라갈 조건"을 한 줄로
  - 4단계 구현: GitHub required checks(Modulith/ArchUnit/NullAway/ESLint/boundaries/Playwright/Chromatic — 전부 하드 레이어) + auto-merge + merge queue(`merge_group`). pstack autopilot 원칙 — 소유 에이전트는 자기 판정으로 못 머지, 독립 검증자, 트렁크 리베이스 head에서 CI 그린, 매 push 재검증. 팀 권장 시작점은 **머지하지 않는** autopilot-stack. 아침엔 히스토리 샘플링, 이상하면 revert·린트 추가(4단계도 9장의 루프)
  - 반대 관점 병기: "작고 범위가 명확한 변경만 자동 머지", "수락률이 아니라 재작업을 측정"(dekita — 인용 수치는 벤더 보고), "whoever clicks merge owns it"(Osmani), 위험 도메인엔 Lauren도 "답이 없다". 리뷰 문화 붕괴 담론(The Register "AI PR 10개 중 1개만 적법", 레포 차단 사례)
  - 토큰·ROI 정면: 1장의 Lauren 답을 운영 수준으로 — 제약이 강한 코드베이스일수록 싼 모델이 잘한다(50:17) = 기둥 3의 비용 효과. 비용 계측: `claude -p --output-format json`의 `total_cost_usd`, PoLL(작은 judge 여럿이 1/7), Code Review $15–25/PR·20분(공식), Agent teams 토큰 경고. "사람을 뽑느냐 토큰을 쓰느냐"(50:02)
  - 조직: PM이 버그 고쳐 와서 stamp(54:13, "Dune이 버티고 있다")와 커뮤니티의 "do not touch" 목록(결제·권한·고객 데이터는 개발자). 주니어: 1단계를 학습 단계로 쓰는 팀 운영. 한국 사례는 토스·LY(소프트 레이어 플랫폼화)로 한정, 대기업 회고는 미확인 명시
  - 에이전트의 가치는 "불가능했던 일"(49:18) — gardening PR, 한 사람이 1시간 붙잡을 재현 자동화
  - 닫는 매듭: 1장에서 적은 자기 단계를 다시 적게 하고, "신뢰는 감정이 아니라 시스템"(28:59)으로 돌아옴. 다음 걸음은 "한 칸"
- **독자가 얻는 것:** 자동 머지의 조건표, 비용 통제 지점, 자기 팀의 현실적 목표 단계
- **저장소 행동:** required checks를 모두 하드 레이어로 채운 뒤, docs-only 또는 gardening PR **1종**에만 auto-merge를 켜고 2주간 재작업률을 기록한다
- **레퍼런스:** §1-2 숫자 표(20 PR·월 PR 한정), §1-3, §1-6 L1·L9·L12, §1-7(47:43·52:16), §3-2 `claude -p`·Code Review 비용·Agent teams, §4-3 auto-merge/merge queue, §4-4 4단계 행, §5-1 Verga·DORA·Bosu, §6-1 토큰 소각, §6-6 A·B·C·D, §6-8 Osmani·OpenAI harness(2차)·LY·토스, §7-1 C1
- **오프닝 기법:** 상황 가정 — "월요일 아침, 노트북을 열었다고 해보자. 두 사람의 화면이 있다"
- **클로징 기법:** 회고형 닫는 매듭 — 여정 회수 + 자기 단계 재표시
- **스캐폴드 유형:** 종합 정리형
- **예상 분량:** 5,500자

## 부록 (editor가 뒷부속으로 작성, 레퍼런스 표를 그대로)

- **부록 A. 도구·모델·환경 버전표 (2026-10-10 기준)** — §3-1 버전 기준표 + Codex 모델명·은퇴 이력 + §4-1 환경 기준(Java 25·Spring Boot 4.1.1·Modulith 2.1.1·Next.js 16.4·React 19.3·ESLint 10·npm 패키지). "출간 시 재확인" 머리말. 미확인 버전(Testcontainers·NullAway·Error Prone 등)은 "GitHub releases 확인" 표기. 약 1,500자
- **부록 B. 신뢰 단계 ↔ 권한·도구·하드 게이트 체크리스트** — §4-4 표를 Claude Code / Codex / 하드 게이트 3열로, 장별 "저장소 행동" 12개를 단계 순으로 모은 체크리스트. 약 1,500자
- 참고문헌은 §8 원장 그대로(등급 라벨 유지).

## 통권 변주 배정표

| 장 | 오프닝 | 클로징 | 스캐폴드 | 그림 | 핵심 박스 |
|---|---|---|---|---|---|
| 1 | 충격적 수치 | 독자 자기 진단 | 개념 도입형 | 곡선+기둥 | O |
| 2 | 실패 장면 | 체크리스트 과제 | 문제-해결형 | — | — |
| 3 | 인용·일화 | 한 문장 여운 | 사례 분석형 | — | — |
| 4 | 실패 장면 | 오프닝 장면 재방문 | 개념 도입형 | 게이트 4단 | O |
| 5 | 수사적 질문 | 측정 지표 제시 | 문제-해결형 | (선택) 2층 레인 | — |
| 6 | 상황 가정 | 경고·반전 | 사례 분석형 | (선택) Act→Observe→Compare→Report | — |
| 7 | 인용·일화 | 인용으로 닫기 | 개념 도입형 | — | O |
| 8 | 충격적 수치 | 명시적 다음 장 이음 | 비교 대조형 | (선택) eval 파이프라인 | — |
| 9 | 정의 뒤집기 | 비유 회수 | 문제-해결형 | 집행 피라미드 | O |
| 10 | 앞 장 콜백 | 선택 분기 | 비교 대조형 | 워크트리·클라우드 | — |
| 11 | 실패 장면 | 열린 질문 | 문제-해결형 | 교차 리뷰 흐름 | — |
| 12 | 상황 가정 | 회고형 닫는 매듭 | 종합 정리형 | — | — |

- 상황 가정 2/12 (≤1/3). 인접 장 오프닝 중복 없음(실패 장면 2·4·11, 인용 3·7, 충격 수치 1·8 — 모두 비인접).
- 클로징 12종 전부 다름. `## 마무리` 헤딩은 의무가 아니다.
- 스캐폴드: 개념 3 · 문제-해결 4 · 사례 2 · 비교 2 · 종합 1.
- 수사 대구("A가 아니라 B다") 장당 3회 이하. 근거 고지형 부정("벤더 보고이지 독립 측정이 아니다" 류)은 상한 없음, 문형 변주.
- 감정 공감 표현("찜찜하다"·"난감하다")은 장당 1~2회. 2·5·9장은 비워도 좋다.

## 저술가 묶음 제안 (오케스트레이터 참고)

연속 묶음 4개: [1·2·3] 지도와 바닥 / [4·5·6] 기둥 1과 스택 번역 / [7·8·9] 기둥 2·3 / [10·11·12] 올라가기. 묶음 간 인접 장(3→4, 6→7, 9→10)의 오프닝·클로징은 위 표가 이미 갈라 놓았다. 5·6장 저술가는 Gradle·ESLint 명령을 실제로 돌려 볼 수 있어야 한다(`no-restricted-syntax` 셀렉터 확인).

## 개정 이력

- 2026-10-10 v1 초안.
