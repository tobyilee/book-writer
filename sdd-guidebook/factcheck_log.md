# 사실 확인 로그 — sdd-guidebook

## 01장 (라운드 1)

### ❌ 정정
- "같은 글에서 전체 하네스는 6시간에 200달러를 썼고, 그중 플래너 단계는 4.7분에 0.46달러였다" → "DAW(디지털 오디오 워크스테이션) 앱을 만든 실행은 3시간 50분에 124.70달러를 썼고, 그중 플래너 단계는 4.7분에 0.46달러였다" — 플래너 단계 수치는 6시간/$200 레트로 게임 실행이 아니라 DAW 실행(V2 하네스)의 단계별 표에 속한다. 근거: research/sdd-report.md 862-869행 표, 1차 출처 anthropic.com/engineering/harness-design-long-running-apps (2026-03-24) 직접 확인
- "실행 전체에서 가장 싼 축에 드는 단계다" → "그 실행의 모든 단계 가운데 가장 싼 단계다" — 1차 출처 표(플래너 $0.46, QA 최소 $3.09, 빌드 최소 $5.88)로 확인, 표현을 정확화
- 계보 표 "형식 명세 (VDM, Z, B) | 1960년대~1990년대" → "1970년대~1990년대" — VDM은 IBM 빈 연구소의 1970년대 작업에서 나왔다(1960년대는 전신인 VDL). 01_reference.md §1.7의 "VDM 1960년대"는 전신과 혼동. 근거: Wikipedia "Vienna Development Method", Jones의 VDL→VDM 이행사(jucs.org)
### ⚠️ 약화·삭제
- "그 단계 하나를 빼자 결과가 눈에 띄게 나빠졌다" → "결과가 나빠졌다" — 원문은 "범위를 좁게 잡아 기능이 적은 앱"까지만 말함, 정도 부사 근거 없음
### 🕒 신선도
- (없음) — Claude Code 플랜 저장 위치는 이미 "2026년 11월 공식 문서 기준" 명기
### ✅ 확인 (요약)
- McGuinness 사례(2025-12-29, 40°F/52°F, 40마일, gpt-4o-mini, 열 줄 메모, 질문 약 50개·선택지 2~3개, 인터뷰 1시간+구현 1시간, 자기 보고 단서 유지) — research/community.md A2, 01_reference.md §3.5
- UnderSpecBench 2,208 변형·55.8~67.8% (측정) — 01_reference.md §5.3
- Anthropic 2026-03-24 글: 플래너·생성자·평가자, Opus 4.6에서 스프린트 구조 제거·플래너 유지, 원칙 문장, "앱 하나씩 직접 돌린 결과" 단서 유지 — §2.2, 1차 출처
- 정의 표 4행(Böckeler 2025-10-15, Delimarsky 2025-09-02, spec-driven.md, Brooker 2026-04-09), Ostroff·Makalsky·Paige 2004와 specdriven.com 연표 귀속, "semantically diffused" — §1.1
- 스펙/메모리 뱅크/계획 표, `~/.claude/plans`·`plansDirectory`, ExecPlan 필수 절 — §1.2, §9 충돌 #7(web.md 우선 반영됨)
- 동인 5가지(ExecPlan 7시간 (주장), Sean Grove 2025 AI Engineer World's Fair (주장), 비결정성, Specification Paradox (주장)) — §1.6
- Böckeler 2026-04 피드포워드/센서 구분 — §1.4
- 계보 표 나머지(DbC 1986, TDD 약 2000, Cucumber 2008, Thrift 약 2007, MDA 2001, EARS 2009 Rolls-Royce), Piskala 2026-01 개념 논문, Brooker TLA+·Lean, Knuth 유비, "맞춰 두는 비용 > 이득"의 (추론) 단서 유지 — §1.7
- 1장은 예제 프로젝트(bookshop-orders) 값을 쓰지 않음 (결제 웹훅 예는 장 내부 예시) — 정전 대조 대상 없음
### 미해소
- (없음)


## 04장 (라운드 1)

### ❌ 정정
- "2026년 비교 글들도 기능당 7~10개 이상을 적었다" → "기능당 7개 이상, 많게는 약 10개를 적었다" — 근거: 01_reference.md §2.6 (ypyl 2026-06-03 "7개 이상", Serverworks 2026-08-25 "약 10개"). "10개 이상"이라고 적은 출처 없음
- shuk `design.md` "요구 번호마다 검증할 속성을 연결한다" → "속성마다 그 속성이 검증하는 요구 번호를 단다" — 근거: research/web.md 자료 10 (속성 형식 "Property N" → "**Validates: Requirements 1.2, 1.5**", 연결 방향이 속성→요구)
### ⚠️ 약화·삭제
- Kiro "CLI와 Web에서도 같은 스펙 기능을 쓴다" → "같은 스펙 흐름(기능·버그픽스·퀵 스펙)을 쓴다" — 01_reference.md §4.3: Analyze Requirements는 Web 미지원, 속성 기반 테스트는 IDE 전용이라 "같은 기능"은 과장
### 🕒 신선도
- (없음) — 장 머리 기준 박스에 도구별 "{버전}/{날짜} 기준"이 이미 있고 Kiro는 "문서 접근 2026-11-10 기준"으로 명시됨
### ✅ 확인 (요약)
- 연표 13건(Harper Reed 2025-02-16 ~ GSD 2025-12-14, "열한 개"·"약 열 달" 계수 포함) — 01_reference.md §1.6과 일치
- 버전·날짜 9건(Spec Kit v1.3.3, OpenSpec v1.17.0, cc-sdd v3.1.0, BMAD v6.12.4, Spec Kit 발표 2025-09-02, Kiro 2025-07-14/2025-11-17, Spec Kit 1.0 2026-08-21, Design-First·버그픽스 2026-02, v0.10.0 브랜치 훅) — §0·§2.2·§4.1·§4.3
- 명령·경로·템플릿 헤딩 약 40건(Spec Kit 9개 명령·산출 파일·spec 템플릿 헤딩·`[NEEDS CLARIFICATION]`, OpenSpec core 6개·디렉터리 트리·델타 원문·아카이브 경로·`openspec config set delivery skills && openspec update`·#2022·v1.16.0/1.16.1 validate 규칙, Kiro 3문서·bugfix 세 문형·`/spec new`·`Ctrl+X`·스티어링 3파일·Plan 모드 15~60분, cc-sdd 설치·6개 명령·EARS 5패턴 영어 고정 규칙·spec.json·`_Boundary:_`, BMAD 5개 에이전트·SPEC.md 다섯 필드·`_bmad/`·v7 설치 명령) — research/web.md 자료 1~4·6~8·10·13~20
- 인용 6건("independent entry points, not mandatory phases", "Source of truth", "Code remains the source of truth.", "Installing 17 skills does not verify…", "`bmad-spec` is the only writer…", "Expect breaking changes between updates.", "You don't need BMad for an obvious, low-risk edit.") — web.md 원문과 일치
- 수치 8건(통합 키 43개, clarify 최대 5문항, Böckeler 파일 8개, 사용자 스토리 4개·수용 기준 16개, cc-sdd 명령 7개→스킬 17개, BMAD 입력 상한 약 40쪽·약 20세션, Serverworks 약 10·약 4·40~50개) — §2.2·§2.6·§4.x
- Radar Vol 35(OpenSpec Trial, 문서 난립 Caution에서 Spec Kit·BMAD 지목) — 01_reference.md §1.8 링 이력표, sdd-report.md 1747행
- 2025 비판 표(Spec Kit 7개 중 해결 4) — §6.3과 일치
- "다른 하네스에서는" 박스 표기 — §2.8·§4.1·§4.2·§4.4
- 예시 산출물 라벨: Spec Kit spec.md, Kiro bugfix.md, cc-sdd 수용 기준·명령 인자, "같은 요구, 다섯 가지 모양" 모두 "이 책 예제로 채운 예시"로 명시. OpenSpec 델타는 공식 문서 예(MIT)로 출처 명시. 도구 실행 출력으로 제시한 블록 없음
### 미해소
- (없음)

## 05장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "둘 다 설치하면 스킬이 두 번 보이니" → "mattpocock/skills를 두 경로로 함께 설치하면 스킬이 두 번 보이니" — 01_reference.md §4.6: 중복 경고는 mattpocock/skills 설치 안내에만 있음. 원문은 Superpowers와 mattpocock을 함께 설치하는 경우로 읽힐 수 있어 범위를 좁힘
### 🕒 신선도
- (없음) — 장 머리에 Superpowers v7.0.2/2026-11-03, mattpocock/skills v1.3.2/2026-10-29, Claude Code 2.1.319, 채택 지표 2026-11-09 판독값 명시됨
### ✅ 확인 (요약)
- 인용 3건("try to help by owning the process", "Mandatory workflows, not suggestions.", Agent OS v3 "the industry-standard approach…") — web.md 자료 21·23, 01_reference.md §2.2
- Superpowers 9건(발표 2025-10-09, `commands/` 없음, 설치 명령, 7단계 흐름·2~5분 태스크, 두 단계 리뷰, 설계·계획 저장 경로, 계획 머리말·태스크 골격 헤딩, README "complete code" 대 SKILL.md 불일치, 질문 41→23 제조사 측정·Builder check v7.0.0, 텔레메트리 환경 변수) — web.md 자료 21·22, §4.5
- mattpocock/skills 8건(저장소 2026-02-03, 사용자/모델 호출 구분, `/grill-me` 한 줄 본문, `/to-spec` "no interview, just synthesis"·이음매 확인·`ready-for-agent`, 템플릿 헤딩, `GLOSSARY.md`, `/setup-matt-pocock-skills`, 별 318,438·skills.sh 32.2M·인터뷰 0명) — web.md 자료 23·24, §2.7
- 플랜 모드 표 6행과 Claude Code 진입·승인 선택지·`Ctrl+G`·`showClearContextOnPlanAccept`·`plansDirectory` — §2.9·§4.7
- 비교 매트릭스 8행×6열 — §2.4와 전 칸 일치
- Uvik 표 5지표×5열과 조건(n=50, claude-sonnet-5, 시니어 5명, ±10%p, 대조군 29분, 플랜 모드 사용 여부 불명) — §2.5
- Ran the Builder(2026-04, 13개 범주, OpenSpec v1.2.0 4.00, Spec Kit v0.1.6 2.77, 인가 누락 관찰) — §2.6
- 채택 지표(별 318,438/314,546, npm 3,920,829, 인터뷰 OpenSpec 7·Spec Kit 3·Superpowers 3, 제작자 8명) — §2.7
- 하네스 교체 연표 3건(Roo Code 5월, Windsurf→Devin Desktop 6월, Amazon Q 2026-04 발표·2027-04 종료) — §2.10
- 보안 수치(31,132개·26.1%·2.12배, Snyk 3,984개·76개·91%)와 Claude Code 플러그인 문서 서술, 점검표 7항(`uvx mcp-scan@latest --skills`, `snyk aibom`, `pluginTrustMessage`, GPL-3.0, MIT + Commons Clause) — §6.2
- 컬리 2025-12 30쪽, intent-driven.dev 절충안, GSD 200k·파일명, Ralph 원형, ExecPlan 리빙 절·자기완결성 — §4.7·§2.2, sdd-report.md §3.8
- 예시 산출물 라벨: Superpowers 계획("이 책 예제로 채운 예시"), `/to-spec` 템플릿("이 책 예제로 채우면") 모두 구성 예시로 표시. 플랜 모드 블록은 문서의 선택지 이름이지 캡처 출력이 아님
### 미해소
- (없음)

## B장 (부록 B, 라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- `(사실 확인 필요)` OpenSpec 스킬 호출 표기(Cursor·Copilot) → "설치 위치 `.cursor/skills/openspec-*/` / `.github/skills/openspec-*/`, 호출 표기는 문서에 없음" — 웹 2차: OpenSpec `docs/supported-tools.md`(2026-11-10 조회)는 두 하네스의 스킬 경로만 적고 스킬 호출 표기는 적지 않음. 명령 형태 `/opsx-propose`만 문서화. 본문에 "이 두 하네스에서는 `/opsx-propose` 명령을 쓰자" 한 문장 추가
- `(사실 확인 필요)` Superpowers Codex 직접 호출 표기 → "직접 부르는 표기는 문서에 없음" — 웹 2차: Superpowers v7.0.1 릴리스 노트는 "by name or with `/brainstorming`" 요청 시 동작만 언급하고 Codex 표기(`$…` 등)는 없음. 리서치 원장에도 없음
- "스킬 이름으로 직접 부르는 방법은 v7.0.1 릴리스 노트에 있지만" → "v7.0.1 릴리스 노트는 이름이나 `/brainstorming`으로 브레인스토밍을 요청하는 경우를 언급하지만, 하네스별 호출 표기는 적지 않는다" — 같은 릴리스 노트: 호출 방법을 설명하지 않고 요청했을 때의 동작만 적음
- OpenSpec 프로젝트 원칙 "전용 장치 없음" → "헌법 같은 전용 장치는 약하다 (추론, `config.yaml`은 프로젝트 설정)" — 01_reference.md §2.2는 "사전 거버넌스 장치가 약함 (추론)"까지만 말함. "없음" 단정의 근거 없음
### 🕒 신선도
- (없음) — 부록 제목과 버전 기준표에 "2026-11-10 기준"과 판별 날짜가 모두 있음
### ✅ 확인 (요약)
- 버전 기준표 8행(판·날짜·라이선스·비고) — 01_reference.md §0, web.md §0
- Spec Kit 하네스별 표기·설치 위치·통합 키(`claude`·`cursor-agent`·`copilot`·`codex`·`none`) — web.md 자료 2, §4.1
- OpenSpec 명령 표기 4하네스, Copilot CLI 제한 — web.md 자료 14
- Superpowers 설치 4하네스 — web.md 자료 21
- 개념 대응표 10행(명령·산출물 이름, `/opsx:verify` 확장 프로필, Spec Refine 확장, `verification-before-completion` 스킬 실재) — §4.1·§4.2·§4.5
- 비실습 도구 4행(Kiro `/spec new`→`/spec run`, cc-sdd 흐름·`$kiro-*`·`--lang ko`, BMAD v6.12 흐름·`bmad-help`, mattpocock 흐름 "추론" 표시) — §4.3·§4.4·§4.6·§4.8
- 변경 가능 항목 9행(OpenSpec 2.0·#2022, BMAD v7 설치·`_bmad-output`, Claude Code 설정 키 5개, Spec Kit 버전 고정 명령, #4065·#4164 미채택, RENAMED 불일치, #821, `spec-driven.md` 브랜치 서술, Superpowers README/SKILL.md 불일치) — §4.x·§9
- 공식 문서 URL 11건 — web.md 출처 줄과 01_reference.md §10.1에 같은 주소가 있음
### 미해소
- (없음)
## 02장 (라운드 1)

### ❌ 정정
- 네이티브 플랜 모드 설명 "따로 저장하지 않으면 세션과 함께 사라지기 때문이다" → "그 작업에만 쓰이기 때문이다. 계획이 파일로 남는 하네스도 있지만(Claude Code는 기본으로 저장소 밖 `~/.claude/plans`에 저장), 다음 작업의 기준으로 다시 열리는 일은 드물다" — 보고서 서술이 1차 출처와 어긋남. 근거: 01_reference.md §9 충돌 #7, §1.2(web-26). 1장 서술과도 일치시킴
### ⚠️ 약화·삭제
- "Kent Beck은 … 가정 자체가 이상하다고 봤다" → "Martin Fowler가 2026년 1월 글에서 전한 Kent Beck의 반론은 …" — Beck 원문(LinkedIn)은 미확인, Fowler 글(2026-01-08) 경유로만 확인됨. 근거: research/sdd-report.md 1694·1762·3009행
- 자기 판정 오케스트레이터(247회·11번·4번)에 "논문 저자들이 직접 운영한 기능 아홉 개의 기록이다" 단서 추가 — (측정, 저자 실행 9개 기능) 단서가 본문에서 빠져 있었음. 근거: 01_reference.md §6.2
### 🕒 신선도
- (없음) — Uvik(2026-10-15 실행, 11-02 갱신), Radar Vol 35(2026-11), "2026년 11월 현재" 명기 확인
### ✅ 확인 (요약)
- Böckeler 3수준 표·판별 흐름, 요즘IT 번역(안영회, 2025-12-01) 용어, "대부분 도구는 실제로 스펙 우선형" — §1.3
- Monperrus 926단어·시연 1회·IEEE Software 게재 예정, Tessl 2025-09 베타 → 2026-01-29 전환(약 넉 달, 추론) — §1.3
- 세 갈래·F1~F8 표(보고서 추론 단서 유지), 계열≠수준, OpenSpec 아카이브로 고정형에 가까움 — §1.5
- Uvik 설계(n=50, 브라운필드 Python, 5유형×10, 크기 20/20/10, 45분 제한, 블라인드 5명, 재실행 10개, claude-sonnet-5, Kiro만 자체 IDE), 병합률 72/80/82/82/84%, 결함 0.86 대 평균 0.46(0.57·0.39·0.49·0.40 평균 0.4625), 파일 수별 표, 유형별 결과, 시간 29분·12~28분, 잡음 대역 ±10%p 판정, Kiro 비용 $2.35 대 $2.43 경고, 대조군 플랜 모드 미기록, 서비스 회사 이해관계 — §2.5 읽는 규칙 6개 모두 본문에 반영됨
- 채굴 연구 스펙 82.0% feat, OpenSpec FAQ 오타 — §6.1, §2.2
- F4·F6 측정 공백 — §2.6
- 스펙 적합성 6조건·Uvik "셋 이상" 규칙 — §3.6
- 여섯 국면, Radar 링 표(Vol 33/34 번호는 거꾸로 센 값 단서 유지), Vol 35 조합 해석(보고서 추론으로 귀속) — §1.8
- Marmelab 2025-11-12 다섯 비판·80% 추정(저자 추정 단서 유지), Atomic Object 2026-05-22 네 차이, Brooker, 2026-11 판정, Spec Kit 2025 비판 7개 중 해결 4·부분 1·유효 2 — §7 논쟁 4, §6.3
- 결론 판단과 판단 1·2·3(SWE-Bench Verified 94.3%, 247/11/4, 26%) — §1.9
### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- EARS 2009 사례의 저자 단서 "평가도 제작자 본인이 했다" → "막연함을 분류하는 일이 주관적이었다. 누락이 '사라졌다'는 결과도 조심해서 읽으라고 적었다(원치 않는 동작 일부를 찾았을 뿐 다른 누락을 잡았다는 증거는 없음)" — 저자가 밝힌 한계는 표본 36개·안전 관련 상위 요구 한정·막연함 분류의 주관성·누락 제거 주장 주의 네 가지다. "제작자 본인 평가"는 저자 단서에 없음. 근거: research/papers.md 논문 1 "저자가 밝힌 한계", 01_reference.md §5.2 경고
### ⚠️ 약화·삭제
- QUS "집합 단위 기준은 도구가 거의 잡지 못한다"(단정) → "그 다섯에 집합 단위 기준은 없었고, 이런 기준은 도구로 잡기 어렵다고 보는 편이 맞다" — 레퍼런스에서 이 판단은 (추론)으로 표시됨(AQUSA v1은 5개 기준만 점검). 근거: 01_reference.md §5.4
- Midolo "수정의 57%는 알고리즘 세부, 44%는 입출력 형식" → "고친 프롬프트의 57%에는 알고리즘 세부가, 44%에는 입출력 형식이 보태져 있었다" — 원 수치는 최적화된 프롬프트 627개 중 각 지침의 적용 비율(중복 적용). 근거: 01_reference.md §5.5 표
- EARS 표 "원전 예문"의 출처 명시 추가: "Mavin이 운영하는 EARS 소개 페이지의 문장이다(2009년 논문의 예시는 항공기 엔진 제어 요구다)" — 표의 휴대전화·ATM·노트북·선루프·신용카드 예문은 alistairmavin.com/ears 페이지의 것이고, RE'09 논문 예시는 엔진 제어 요구(research/papers.md 논문 1 표). "Mavin 2009 원전 예문"으로 오독되지 않게 함
### 🕒 신선도
- (없음) — "2026년 11월 현재" EARS 통제 실험 부재, IFScale "2025년 7월 모델 기준", Ambig-SWE "ICLR 2026 채택 표기" 명기 확인
### ✅ 확인 (요약)
- EARS: Mavin 등 2009, Rolls-Royce 제트 엔진 제어 감항 규정, RE'09; 일반형·시간 순서; 여섯 문형 이름·키워드·원전 예문 6개 원문 일치; 원치 않는 동작 별도 문형의 이유; 36→47개, 36.9→25.6단어, 8개 중 5개 유형 0건; LLM 통제 실험 부재 경고 유지 — §5.2, papers.md 논문 1
- 작성 규칙 4가지, cc-sdd `ears-format.md` 한국어 규칙, Salari 외 2025, 도구별 변형 표(Kiro `SHALL CONTINUE TO`, cc-sdd 다섯 패턴, OpenSpec·Spec Kit 비EARS) — §5.2
- Yang 외(Findings of ACL 2026) 41.1%·회귀 2배·LLM 앱 대상 단서, IFScale 500개·68%·앞쪽 편향, EPIC 114개·should→must(상관 단서 유지), 상세도 규칙 (추론) 단서 — §5.5
- HumanEvalComm(TOSEM 2025) 164→762, 14.21%, 65.58→31.34%, 31.68/5.84/5.84%, GPT-4급 미평가 단서; Ambig-SWE 74%·약 89%·인용문 — §5.3, papers.md 논문 5·6
- SWE-Milestone 98/25/80.6%/48.4%, TDFlow(EACL 2026) SWE-Bench Verified 94.3%·주 장애물, Spec Kit `[NEEDS CLARIFICATION: ...]`, QUS(Lucassen 2016) Atomic·Problem-oriented·Conflict-free 정의, 1,023개 중 평균 56% — §5.3, §5.4
- Vikram 외 API 메서드 40개·21%(프리프린트), Newcombe(AWS 2011~ TLA+, 서비스 10개), ShardStore 16건, 계약·속성 단 판단 (추론) 단서 — §5.6
- Ran the Builder(2026-04-13) 인가 누락 관찰, 실무자 1명·기능 1개 단서 유지 — §2.6
- 커뮤니티 최소 키트의 비목표·결정 기록 반복 — §3.2
- 예제 정전 대조(02_plan.md): 기존 기능·상태 4개·전체 취소 경로, `SHOP_ADMIN`·자기 서점 인가·403, `delivered_at`부터 168시간·`422 REFUND_WINDOW_EXPIRED`, `refunded_quantity`·`409 REFUND_QUANTITY_EXCEEDED`, PG 실패 `FAILED`·`502 PAYMENT_GATEWAY_ERROR`·상태 불변, `Idempotency-Key` 24시간·`422 IDEMPOTENCY_KEY_REUSED`, `PARTIALLY_REFUNDED`/`REFUNDED`, 비목표 5개, 기준 숫자(42,000·4,200·3,000·40,800, 책 B 1권 1,200→10,800, 합계 16,200+10,800+10,800=37,800, 정액 3,000원 1,285/857/857=2,999→1원 보정, 39,000=42,000−3,000) 직접 계산으로 모두 일치. 결정 기록에서 "168시간"을 뺀 것은 6장 복선으로 의도됨(orchestrator_notes.md)
### 미해소
- (없음)


## 09장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "Copilot 사용자들은 Ask 모드를 처방으로 들었다" → "댓글에서는 Copilot의 Ask 모드가 처방으로 나왔다" — 근거: 01_reference.md §4.1 이슈 #737 "처방: Copilot Ask 모드(댓글)", research/community.md 173행. 복수 사용자라는 근거 없음
### 🕒 신선도
- (없음) — 장 머리에 "Spec Kit v1.3.3/2026-11-09 기준" 상자, #4065·#4164 "2026-11 기준 미채택", Radar Vol 35(2026-11) 명기 확인. "며칠 간격으로 새 판"은 v1.3.2(2026-11-06)→v1.3.3(2026-11-09)와 맞음
### ✅ 확인 (요약)
- Scott Logic(2025-11, 1.0 이전, Copilot + Sonnet 4.5, 증분 2개·1인): 33분 30초, 689줄, 2,577줄, 검토 3.5시간, plan 2,067줄·약 2시간, 기준선 8분·1,000줄·15분·9분, 약 10배, "3.5시간 대 23분" 경고와 23분 30초 귀속 — §4.1
- 설치·통합: Python 3.11+, uv, `specify-cli`, `@v1.3.3` 고정 명령, `specify integration install claude`, `--integration-options="--no-model-invocation"`→`disable-model-invocation: true`, 하네스별 키·위치·호출(`claude`/`codex` `$speckit-specify`/`cursor-agent`/`copilot`), `--integration none`, 기존 프로젝트 가이드(커밋·stash, 작은 첫 변경, 기존 규칙에서 헌법), 진입점 넷과 "independent entry points, not mandatory phases" — §4.1, web.md 자료 1~3
- 헌법: `.specify/memory/constitution.md`, 템플릿 원칙 칸 5 + 추가 절 2 + Governance, "아홉 조항"은 `spec-driven.md` 설명틀·IV~VI 프로젝트 정의, Version/Ratified/Last Amended 줄 — §4.1 경고(§9 #11·#12). 예시 헌법은 "이 책 예제로 채운 예시, 도구가 생성한 출력이 아님" 명시
- 명령 9개 이름·설명·산출 파일, clarify "up to five targeted questions"·"Maximum of 5"·`/quizme`·`## Clarifications`/`### Session`, analyze "read-only", converge "append-only"·`tasks.md`에만 덧붙임·"Repeat implement and converge until … Converged", checklist `checklists/`, 기능 폴더 번호(NNN/`YYYYMMDD-HHMMSS`)·`feature.json` `"feature_directory"`, v0.10.0 `before_specify` 훅, `spec-driven.md` 구버전 브랜치 서술 — §4.1
- 템플릿 헤딩: spec(User Scenarios & Testing *(mandatory)*, Priority, Why this priority, Independent Test, Acceptance Scenarios, Edge Cases, FR-### MUST, Key Entities, SC-###, Assumptions, `[NEEDS CLARIFICATION: …]`, "technology-agnostic and measurable"), plan(Summary, Technical Context 9항목, "or NEEDS CLARIFICATION", Constitution Check GATE 원문), tasks(`[ID] [P?] [Story] Description`, Phase 3 MVP, Tests OPTIONAL 헤딩·정책 원문, Checkpoint 원문), plan 산출 파일 5종 — §4.1, web.md 자료 4
- 현장: 이슈 #4164(2026-08-17)·#4065(2026-08-12)·#737(2025-10-04), velog 2026-04-26(금지 규칙·TDD·clarify 반복), Ran the Builder 2026-04 인가 누락(실무자 1명 단서 유지), OrangeLoops 2026-05(195개, 약 1시간 6분, 4일, 인증 헤더, 타이밍 파일, 자기 보고) — §4.1, §2.6
- 무게: 파일 8개 + 헌법·`feature.json`, Serverworks 약 10·약 4([문서+실무] 단서 유지), Uvik(조건 병기) 132/93줄·18/12분·12.5%/2.4%·80% 대 72%(+8%p, 대역 안), 2025 비판 현황(브랜치 v0.10.0, 버그 확장, `uv tool install specify-cli`, 여전히 유효 둘, converge 부분 해결·판정은 에이전트), Radar Vol 35 문서 난립 Caution·Spec Kit 평(브라운필드, 경험 많은 엔지니어) — §2.5, §2.6, §6.3, §1.8
- 버그 확장(`specify extension add bug`, assess→fix→test, verified/partial/failed), 평가 확장(go/needs-clarification/kill) — §4.1
- 개념 표 대응물: Kiro Analyze Requirements, `openspec validate --strict`(v1.16.0 형식 점검), `/opsx:verify` 확장 프로필, Superpowers 스킬명 — §4.2·§4.3·§4.5
- 예제 정전 대조(02_plan.md): 책 A 18,000×1, 책 B 12,000×2, 10% 쿠폰 4,200, 배송비 3,000 → 40,800원; 책 B 1권 12,000−1,200=10,800원; 전 항목 37,800원=40,800−3,000; 정액 3,000원 1원 보정; 오류 코드 5종·403/404, 상태 `PARTIALLY_REFUNDED`/`REFUNDED`·`REQUESTED`/`COMPLETED`/`FAILED`, 키 24시간, 엔드포인트 2개·테이블 2개, 비목표 5개 — 직접 계산으로 일치. clarify 세션의 "새 키로 재요청"·"조회도 403"은 정전 규칙 5·6에서 끌어낸 장 내부 결정(orchestrator_notes.md에 기록됨)
- 예시 산출물 라벨: 헌법·spec.md·Clarifications·contracts·converge 절 모두 "이 책 예제로 채운 예시", spec.md·plan.md·tasks.md는 "헤딩은 템플릿 원문, 내용은 예제"로 명시. 캡처 출력으로 제시한 블록 없음
- 참고(편집 이관): 그림 2 캡션은 공식 설명대로 analyze를 "만들기 전" 관문에 두고, 12장 오프닝의 GPTers 회고는 analyze를 "만든 뒤 전용"으로 분류한다. 각자 출처대로 맞지만 독자가 충돌로 읽을 수 있음
### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- 두 단계 리뷰의 귀속: "태스크 사이에는 `requesting-code-review`가 끼어든다 … 그리고 리뷰는 두 단계로 나뉜다" → 두 단계 리뷰는 `subagent-driven-development` 경로에 붙는다고 고치고, README 원문 "two-stage review (spec compliance, then code quality)"와 v7.0.2 SKILL.md 구조(태스크마다 리뷰어 하나가 Part 1 Spec Compliance → Part 2 Code Quality 두 판정)를 적음. `requesting-code-review`는 "계획과 대조, 심각도별 보고, Critical은 진행을 막음"으로 한정 — 근거: 웹 2차, github.com/obra/superpowers README Skills Library("**subagent-driven-development** - Fast iteration with two-stage review (spec compliance, then code quality)", "**requesting-code-review** - Pre-review checklist"), `skills/subagent-driven-development/SKILL.md`·`task-reviewer-prompt.md` @v7.0.2(마지막 변경 커밋이 v7.0.2 릴리스 2026-11-03), 2026-11-10 조회. 레퍼런스 §2.2는 두 단계 리뷰를 어느 스킬에도 귀속하지 않았음
- 그림 2 캡션: "두 단계 리뷰의 순서. 스펙 준수가 통과해야 코드 품질을 본다" → "`subagent-driven-development`의 태스크 리뷰가 보는 두 단계의 순서. 스펙 준수를 먼저, 코드 품질을 그다음에 본다" — 같은 근거. v7.0.2는 리뷰어 하나가 diff를 한 번 읽고 두 판정을 내므로 "통과해야 본다"는 게이트 서술은 과장
- 개념 표: `requesting-code-review` 행의 "분리된 리뷰, 스펙 준수 먼저"를 "태스크 사이 리뷰, 심각도별 보고"로, 두 단계 리뷰는 `subagent-driven-development` 행으로 옮김 — 같은 근거
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음) — 장 머리 "Superpowers v7.0.2/2026-11-03 기준", v7.0.0(2026-10-10) brainstorming 재작성, `commands/` 없음 "2026-11-10 확인", SKILL.md(2026-09-25) 명기 확인
### ✅ 확인 (요약)
- 오프닝: Jesse Vincent 2025-10-05 글("How I'm using coding agents in September, 2025"), 3세션, 200~300단어 절, 긴 글 관찰, 설계자 세션 불일치 표시, 구현자 태스크 3~4개·`/compact` 대신 `/clear`, 발표 2025-10-09(나흘 뒤), "질문 하나씩, 가능하면 객관식" — 01_reference.md §3.3·§2.2, community.md C7
- Boris Tane `don't implement yet` — §3.5 A4
- 설치 6개 하네스 명령 원문, 자동 트리거·"Mandatory workflows, not suggestions"·"checks for relevant skills before any task", `/brainstorming` 직접 호출(v7.0.1), 텔레메트리 `SUPERPOWERS_DISABLE_TELEMETRY` — web.md 자료 21, §4.5
- 인프런 "클로드 코드의 정석"(SessionStart 훅·`using-superpowers`, Spike/Bounded/Architecture), "Claude Code 실전 업무 자동화" 초보자 권장(강사 의견 단서 유지) — §4.5 한국 맥락
- 플러그인 훅·샌드박스 서술, 점검표 셋째 항목 `hooks/hooks.json` — §6.2. "SDD 플러그인 하나만"은 보고서 (추론) 규칙과 일치
- brainstorming v7.0.2 세 변화, 41→23(제조사 측정 단서 유지), 설계 문서 위치·다룰 것 6항목, Builder check(v7.0.0, spec-document reviewer 대체) — web.md 자료 22
- 기본 흐름 7단계, worktree 기준선, 계획 위치·2~5분 태스크·머리말(Goal/Architecture/Tech Stack/Spec, Global Constraints, Review Focus)·Task 구조(Files/Interfaces/Step 1~5), SKILL.md 원문 "the exact signature … The implementer writes the body", README "complete code" 불일치(§9 #6), executing-plans "가장 저렴"·마지막 1회 리뷰, TDD가 테스트 전 코드 삭제, `verification-before-completion`·`finishing-a-development-branch`(merge/PR/keep/discard) — §4.5
- 근거와 한계: F4 독립 측정 없음, Uvik 문서 계열 넷만, 매트릭스 D11 Superpowers 1-[주장], D10 기본값 3 이상은 Superpowers·agent-skills, HN 토큰 주장 — §2.4, §2.6, §4.5
- TestSuiteBench 변이 점수 60% 미만, Netguru 규칙, 부팅 실패 사례 — §5.4, §6.2
- 예제 정전 대조: 설계 문서 Constraints 전 항목(168시간, 409/422/502/403/404, 24시간, 상태 이름, 기준 숫자 40,800·10,800·37,800), 스키마 열 목록, 비목표 5개, Task 1 금액(4,200×12,000/42,000=1,200 → 10,800; 16,200+10,800+10,800=37,800; 정액 3,000원 → 1,285.7→1,285, 857.1→857, 합 2,999 → 1원 보정) 직접 계산 일치. "정확히 168시간은 안"은 6장 D4와 같은 결정
- 예시 산출물 라벨: 설계 문서·계획 "이 책 예제로 채운 예시", 리뷰 점검 틀 "도구가 내는 보고 형식이 아님" 명시
- 참고(편집 이관): Task 2 시그니처 `isWithinWindow(Instant deliveredAt)`(Clock 주입)는 5장 발췌의 `isWithinWindow(Instant, Instant)`와 다름(orchestrator_notes.md 기존 항목)
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- 네 벌 비교 ①②: 정전에서 재구성한 문장(① "the Refund Service shall …", ② `Requirement: Refund Window`·169시간 시나리오)이 실제 6장·8장 원고와 다름 → 6장 `SPEC.md` R2·D4 원문과 8장 델타 스펙 `### Requirement: 환불 기간` + "경계 시각"·"기간 경과" 시나리오 원문으로 교체 — 근거: chapters/06_draft.md 189~190·250행, chapters/08_draft.md 136~148행(6·8장 final 미산출 시점이라 draft 기준. 편집 주석을 그 취지로 바꿔 남김)
- "④만이 '정확히 168시간은 안인가'라는 경계를 실행할 값으로 못 박았다" → ①은 D4, ②는 "경계 시각" 시나리오, ④는 Task 2가 경계를 못 박았고 ③만 "지난"이라는 말에 맡겼다고 고침 — 근거: 같은 6장 D4("168시간이 되는 시각까지 받는다")·AC4, 8장 경계 시각 시나리오, 9장 FR-002
- 비교표 "스펙 분량" 행: ① "전문 한 장" → "132줄", ② "델타 스펙" → "116줄", ③ "`spec.md`만 80줄 남짓" → "76줄", ④ "설계 문서 60줄 남짓" → "50줄 남짓" — 근거: 06_draft.md 코드 블록 120~251행(본문도 "132줄"이라 적음), 08_draft.md 115~230행, 09_draft.md 111~186행, 10_draft.md 52~102행 직접 셈
- "Scott Logic 기록에서 에이전트 시간은 33분" → "33분 30초" — 근거: 01_reference.md §4.1, 9장 오프닝과 일치시킴
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음) — 문턱값 "시작값, 추론" 단서와 Uvik 조건이 본문에 있음
### ✅ 확인 (요약)
- 비교표 나머지: 파일 수(1 / 4 / 8+헌법 / 2), OpenSpec 하네스(Claude Code·Cursor·Copilot IDE·Codex·Gemini·Kiro), Spec Kit 통합 키 43개, Superpowers 하네스 5종, `validate --strict` 형식 점검, `/opsx:verify` 확장 프로필, 스펙 수명 분류 — §2.8, §4.1, §4.2, §1.3. "이 책 예제 한 건의 관찰, 측정 아님" 단서 있음
- Ran the Builder(2026-04, 실무자 1명) 인가 누락, cc-sdd README "Installing 17 skills does not verify…" 취지, 2026 하네스 종료·개명 — §2.6, §2.8, §2.10
- Uvik: 대역 밖 OpenSpec +12%p 하나, 드리프트 2.4%/12.5%, 파일 수별 85/85·50/80, Superpowers·SPEC.md 경로 미측정 — §2.5
- 스펙 적합성 6조건, Uvik "셋 이상", 0~1·핫픽스·오타 → R0, 2점 → R1(추론·시험 출처 없음), 부분 환불 4점 — §3.6
- 사다리 표 7행(바닥 150줄 포함), 다섯 규칙, 그림 1 진입·하향 신호, 결정 트리(보고서 §9 트리를 계열 기호만 이름으로 바꿔 옮김), 곁가지 S·G·H 트랙 — §3.6
- C0~C4 점수·단 배치 — 02_plan.md 변경 시리즈 표와 일치. C2 4점 = 조건 1~4
- OpenSpec FAQ 오타 문장 — §2.2(rpt r136), sdd-report.md 641행. `/plan` 접두, `plansDirectory` `"./plans"` — §2.9·§4.7
- 경로 확실성: Loglass(2025-10-08), y-hirakaw(2026-03-15, 약 2개월), Kiro 상충, 보고서 조정안(추론) — §3.6, §7 논쟁 5
- .NET Razor Pages OpenSpec 약 2시간(단일 실험의 주장), Talk Think Do(2026-06, 작업 항목 이동·계획 규율 유지) — §4.2 1015~1016행
- 하향 신호 표 7행 — §6.5와 일치. 빼지 말 것 — §6.5
- 제조사 가벼운 경로, BMAD 인용문, Spec Kit "Stopping with a documented reason is also a useful outcome." — §6.1, §3.6
- 시험 계획 P0 1주(10개 이상)·P1 1주·R1 대 R2 2주, CSV 머리글 원문, 지표 셋, `.git/info/exclude`·user/local 범위 — §3.6. METR RCT 16명·246개·19%↑·20%↓ 믿음 — §6.4
- CSV 값 3줄은 "이 책 예제로 채운 예시"로 명시
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- Tessl "2025년 9월 프레임워크와 스펙 레지스트리를 공개했다가" → "프레임워크를 비공개 베타로, 스펙 레지스트리를 공개로 내놓았다가" — 근거: 01_reference.md §1.3 102행("Framework(비공개 베타)·Spec Registry 공개"), 2장 final 서술과 일치시킴
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음) — Radar Vol 35(2026-11), Asana(2026-09), 연표 날짜 모두 명기
### ✅ 확인 (요약)
- 오프닝: GPTers 황금호랑이(2026-08-05, 반년 가까이 SpecKit), 만들기 전(`clarify`·`checklist`)/만든 뒤(`analyze`·`converge`) 분류와 앞의 둘을 거의 안 씀, "검수할 수 있는 건 파일뿐"·Git 공유 요지 — 01_reference.md §3.2 498행·§4.1, community.md C26
- 스펙 수명 표 4선택과 근거(Brody PR `<details>`, TOKIUM 삭제, Spec Kit #620 하나로 합친 최신 스펙, cc-sdd "Code remains the source of truth.", Talk Think Do), 논쟁 2 양쪽(GitHub 살아 있는 산출물, Brooker, LayerX, GeekNews googol, irr123 "Rotten specs"), Brody의 연구/계획 분리 — §7 논쟁 2, §3.5
- 드리프트: 완료 시점에만 점검하는 실태(rpt r234), 같은 PR 규칙, converge, 아카이브, OpenSpec #821 제안, redism(2026-04-16) `parent`/`children`·결정 045 드리프트 실물, Radar 시맨틱 리뷰 Assess — §6.2 1600행, §1.8
- 팀: 98.3% 단독 저자·팀 검토는 조직 환경에서만, Asana(약 절반, 30~50명, 66개·약 150건·91%, 한 달 이상, 인프라 병목, 중복 필드, 한 쪽 설계 문서, PR 38%·약 2.66배는 위험 신호 단서, 소유자·보관 계획), "요구사항은 꼼꼼히·설계는 훑기" — §6.1, §6.5
- 주니어 이해 점검 세 질문 0~3점, Anthropic RCT 52명 50% 대 67%, 디버깅 격차, "일반 AI 코딩" 단서 — §3.6
- 바닥층: Radar 지시문 비대 Caution·처방, Gloaguen 20%+·개요 무익, Lulla 10개·124개·28.64%·16.58%, 함께 지키는 법(추론), 752→약 40줄·약 35%(자기 보고), 150줄, 74.0% 이유 없음, Claude Code 모범 사례 CLAUDE.md 네 항목·훅 — §3.7, §3.1
- 연표 7건 날짜·사건 — §2.10과 일치. `/opsx:propose`→`/openspec-propose` 2.0 예고 — 02_plan.md 용어 표기, §0
- Anthropic 2026-03-24 글(Opus 4.6, 스프린트 제거·플래너와 평가자 유지, 플래너 없으면 기능 적은 앱, 하네스 재점검), 변경 5~10개 재실행 — §2.2 280행, §6.5
- McGuinness(한 문단 스펙, 40마일, 52°F→40°F, 챗봇이 예보 가림, 구형 모델, 열 줄 메모, 질문 약 50개, 인터뷰·구현 각 약 1시간, 자기 보고) — §3.5 A2
- `CLAUDE.md` 예(22줄, "스무 줄 남짓"과 맞음)·PR 템플릿은 "이 책 예제로 채운 예시"로 명시. 정전 값(168시간, 10,800원, 전체 취소 경로, 1원 차액은 마지막 환불 항목) 일치
### 미해소
- (없음)

## A장 (부록 A, 라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- A.6 "기준 집합 전체를 봐야 하는 질문은 도구가 거의 잡지 못한다"(단정) → "도구로 잡기 어렵다고 보는 편이 맞다" — 01_reference.md §5.4에서 이 판단은 (추론)(AQUSA v1은 5개 기준만 점검). 3장 라운드 1의 같은 약화와 일치시킴
### 🕒 신선도
- (없음)
### ✅ 확인 (요약)
- A.5 EARS 여섯 문형 이름·키워드·틀(복합형 `While …, when …` 포함), 영어 키워드·한국어 변수 규칙, 작성 규칙 네 가지(papers.md 추론 규칙과 같은 내용), 근거 한계(2009 사례 1건·요구 36개, LLM 통제 실험 없음) — §5.2. `Where` 예문은 3장 표의 예문·단서("문형 선택이 늘 자명하지는 않다")와 같은 것이라 그대로 둠
- A.6 QUS Atomic·Problem-oriented·Unambiguous·Conflict-free·Complete, 스펙-오라클 격차, 7장 기준선 — §5.4
- A.7 6조건·Uvik "셋 이상"·0~1/2/3+ 분기·부분 환불 4점 — §3.6
- A.8 사다리 8행(S 트랙 포함)·하향 신호 8행 — §3.6, §6.5와 일치
- A.9 설치 전 점검표 7항(`hooks/hooks.json`·`.mcp.json`, "Will install"·`claude --plugin-dir <dir> plugin details <name>`, `uvx mcp-scan@latest --skills`, `snyk aibom`, `pluginTrustMessage`), 플러그인 훅·샌드박스·자동 업데이트 서술, SDD 플러그인 하나만(추론 규칙) — §6.2
- A.10 CSV 머리글 원문, P0/P1/R1 대 R2 기간, 지표 셋 — §3.6
- A.3 "skip style" 이유(리뷰어는 늘 무언가를 찾는다, 불필요한 추상화) — §3.1
- 참고(편집 이관): A.1~A.3 프롬프트는 6장·7장 draft의 프롬프트와 문구가 다름(A.1 선택지 "2~3개" 대 6장 "2~4개"·추천 이유·코드 먼저 읽기·범주 지정, A.2 검사 질문 범위, A.3 "실행한 명령과 출력" 줄 추가). 사실 오류는 아니고 orchestrator_notes.md 기존 항목대로 editor가 6·7장 final에 맞출 것. EARS 주어 "the Refund Service"도 기존 통일 항목
### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- "줄 번호는 검사 전 초안 기준인데, 위 전문과 줄 수가 같아" → "초안에는 결정 기록 끝의 두 줄(131~132행)이 없을 뿐 나머지 줄 위치는 위 전문과 같아" — 근거: 장 내부 대조. 확정판 SPEC.md는 132줄이고, diff상 D4·D5 두 줄이 131행에 추가됐으므로 초안은 130줄. 검사 보고서 줄 번호(4·30·70·100·105–106·131)는 확정판 전문의 해당 줄(상태·배송비 비목표·R2·AC2 THEN·AC4 두 줄·D4)과 일치함을 직접 셈
- "131줄을 매번 처음부터 다시 읽는 일" → "132줄을" — 같은 장 254행 "132줄이다", 7장 "132줄짜리 스펙"과 맞춤
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음) — 장 머리에 "Claude Code 2.1.319(로컬 설치본, 공식 문서 접근 2026-11-10) 기준", mattpocock/skills "v1.3.2/2026-10-29 기준" 명기됨
### ✅ 확인 (요약)
- 예제 정전 대조(02_plan.md): 기준 주문 O-1(18,000×1 + 12,000×2 = 42,000, 정률 10% 4,200, 배송비 3,000, 결제 40,800), API·헤더·스키마·상태·오류 코드 6종·비목표 5종·키 보관 24시간·바뀌지 않을 동작 — 모두 일치
- 산수: AC1 12,000 − 4,200×12,000/42,000(=1,200) = 10,800 / AC2 16,200+10,800+10,800 = 37,800 = 40,800−3,000 / AC3 3,000×18,000/42,000 = 1,285.71→1,285, 3,000×12,000/42,000 = 857.14→857, 1,285+857+857 = 2,999 → 마지막 858, 합 3,000 / 정액 3,000 쿠폰 시 결제 42,000, 환불 합계 39,000 = 42,000−3,000 / AC4 2026-11-02T10:00+09:00 + 168h = 2026-11-09T10:00:00+09:00(접수), 10:00:01(거절) — 모두 맞음
- 스펙 적합성 점수 4점·R2 한 파일 스펙(L6), Uvik 규칙 3점·n=50 브라운필드 Python·모델 1개, 스펙 길이 중앙값 93~188줄 — 01_reference.md §2.5·§3.6
- Claude Code 모범 사례(인터뷰→SPEC.md→새 세션, "Once `SPEC.md` exists, start a fresh session to build from it", 속도 제한 예·객관식 질문, 리뷰어는 늘 무언가 찾는다는 경고) — §3.1
- 커뮤니티 수치·사실 약 15건(VelvetShark 32문항·약 1/3·20~30/40~60·157줄·비목표·`~/.claude/commands/interview.md`·과하다는 한계, McGuinness 약 50·25~100·한 번에 하나, Vincent 200~300단어, Ray 2026-09-21 8일차 가계부·세 검사·Decision Log·1년 어긋난 예시 데이터, Tane·Brody 주석→요약, GPTers 황금호랑이 반년 Spec Kit·"검수할 수 있는 건 파일뿐", Ran the Builder 인가 누락, Spec Kit #737 2025-10-04) — §3.2~3.5, §2.6, research/community.md
- 연구 수치(HumanEvalComm 14.21%·31.68%·모순 5.84%, Ambig-SWE "거의 묻지 않았다", SWE-Milestone 80.6%) — §5.3·§5.4, 3장 final과도 일치
- 하네스 상자(Cursor Plan Mode 명확화 질문, Copilot `/plan`에 결과·제약·검증, Codex `/plan` 작업 중 불가, grill-me 설치 경로 4종+Cursor 범용) — §2.9·§4.6·§4.7. `/grill-me` 본문 한 줄·`grilling` 스킬 — §4.6
- 예시 라벨: 인터뷰 대화("만든 예시"), 검사 보고서("이 책 예제로 채워 보면") 명시. SPEC.md 전문에 "이 책 예제로 쓴" 라벨을 보강함(사실 정정 아님)
### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "검토 부담은 SDD를 향한 불만 가운데 가장 오래 살아남은 것이다" → "2025년의 불만 가운데 2026년 11월까지 살아남은 몇 안 되는 것이다" — 근거: 01_reference.md §6.3·845행. Spec Kit 2025 비판 7개 중 여전히 유효한 것은 "기능마다 파일이 많다"와 "긴 마크다운 검토 부담" 둘이라 "가장 오래"라는 최상급은 근거 없음
### 🕒 신선도
- (없음) — 장 머리에 "Claude Code 2.1.319(로컬 설치본, 공식 문서 접근 2026-11-10) 기준"과 설정 키 변동 경고가 이미 있음
### ✅ 확인 (요약)
- 플랜 모드 사실 9건: 진입 3종(`Shift+Tab`, `claude --permission-mode plan`, `/plan` 접두), `⏸ plan mode on`, 읽기·탐색 명령·계획 작성은 하되 소스는 고치지 않음, 승인 선택지 3개 원문(auto 불가 시 auto-accept edits), `Ctrl+G`, `plansDirectory` 프로젝트 루트 기준·루트 밖/백슬래시 경로 무시 시 `~/.claude/plans`, `showClearContextOnPlanAccept` → "Yes, clear context and …", 둘 다 settings-reference 키(`.claude/settings.json`) — 01_reference.md §4.7, research/web.md 922~931행
- 자기 판정 관문 감사(블록 점검 247회·미선언 변경 11회·중단 4회·저자 운영 기능 9개·직접 비교 없음 단서), Verus-SpecGym 26%, Nolan Lawson SQL·`EXPLAIN`, Netguru "동작이 없으면 실패해야 한다", 판정자 표 4행 — §6.2, research/sdd-report.md 156·1519행
- TDFlow(Lite 88.8%·+27.8점·Verified 94.3%·800회 중 7회), TestSuiteBench(앱 165개·변이 점수 60% 미만), Vikram 외 21% — §5.4·§5.6
- 커뮤니티 사실(엔라인 부팅 실패 목록·날짜 미표기·1인 보고·부팅 스모크·리뷰어 쓰기 권한 제거, McLeod "The checklist is the state of the work."·40~50K/160K/250~300K, Vincent 태스크 3~4개·`/clear`, Tane `don't implement yet`·버리고 다시·15분, Brody `<details>`, GeekNews 댓글, Loglass 1~2시간) — §3.2~3.5, §6.1
- Claude Code 모범 사례 리뷰 프롬프트 "skip style"·리뷰어 경고·`/code-review`·완료 주장의 증거 — §3.1
- 하네스 상자(Cursor 홈 디렉터리·Save to workspace, Copilot `/memories/session/plan.md`·Open in Editor, Codex 저장 위치 미기재) — §2.9·§4.7
- 예제 정전·산수: AC1 10,800, AC2 37,800, AC3 1,285/857/858, 쿠폰 안분 제거 시 12,000원, 168시간 경계, 스모크 시드 delivered_at 하루 전(창 안), 고정 시드 2026-11-02는 2026-11-09T10:00 이후 422 — 6장 SPEC.md·02_plan.md와 일치. "132줄짜리 스펙" 일치
- 예시 라벨: 계획 파일("이 책 예제로 채운 발췌"), JUnit("이 책 예제로 쓴 코드"), 검증 스크립트(예제 저장소 스크립트 주석) 명시. 도구 실행 출력으로 제시한 블록 없음
### 미해소
- (없음)

## 08장 (라운드 1)

### ❌ 정정
- 메인 스펙 제목 줄 `# Refunds Specification` → `# refunds Specification`, 마커 "(sync가 제목 줄을 어떻게 만드는지 확인하지 못했다)" → "sync 스킬과 `openspec archive`가 모두 능력 폴더 이름을 그대로 넣어 `# refunds Specification`으로 만든다(v1.17.0 소스 기준)" — 근거: 웹 2차, Fission-AI/OpenSpec v1.17.0 태그 `src/core/specs-apply.ts` `buildSpecSkeleton()`(`# ${specFolderName} Specification`), `skills/openspec-sync-specs/SKILL.md` Main Spec Format Reference(`# <capability> Specification`, 델타 Purpose는 그대로 복사)
- 그림 2 NG 가지 "병합 뒤 336시간, 시나리오 0개, 경계 시각 시나리오가 사라진다" → "validate 오류, archive 거부", 캡션도 맞춤. 마커 "(시나리오가 없는 요구를 validate가 잡는지 확인하지 못했다)" → v1.17.0 `validate`가 시나리오 없는 ADDED·MODIFIED 요구를 ERROR로, 메인 스펙 시나리오를 빠뜨린 MODIFIED도 오류로 잡고 `openspec archive`가 병합을 거부한다는 서술 + `/opsx:sync` 스킬은 언급 안 된 시나리오를 보존하라고 지시하므로 validate 없이 sync하면 낡은 경계 시나리오가 남을 수 있다는 (추론) — 근거: v1.17.0 `src/core/validation/validator.ts`("must include at least one scenario", scenario-loss 검사 #1477 "archive refuses to drop them"), `specs-apply.ts`("Refresh the change spec before archiving to avoid dropping scenarios"), sync SKILL.md("Preserve scenarios/content not mentioned in the delta"). "MODIFIED는 통째로 교체, 전문을 다시 적는다"는 concepts.md 규칙은 그대로 유지(병합 규칙 문단에 "concepts 문서 기준" 명기)
- 마커 "(`/opsx:verify`가 무엇을 대조하는지 확인하지 못했다)" → 문서 서술로 대체: 완전성(태스크·요구·시나리오)·정확성(스펙 의도·경계 사례)·일관성(설계 결정 반영) 세 차원, CRITICAL/WARNING/SUGGESTION 보고, 아카이브를 막지 않음. 판정자가 에이전트라는 (추론)은 유지 — 근거: docs/commands.md(웹 2차, 2026-11-10 접근)
- 마커 "(`/opsx:update`가 #821을 얼마나 메우는지 확인하지 못했다)" → "#821은 2026년 8월 'not planned'로 닫히고 토론 게시판으로 옮겨졌다. `/opsx:update`는 문서상 코드는 고치지 않으므로 #821의 요청 가운데 계획 산출물 쪽만 맡는다" — 근거: github.com/Fission-AI/OpenSpec/issues/821(2026-08-06 closed as not planned, Discussions #1567로 이동), docs/commands.md("never edits code", planning artifacts only)
- 마커 "(OPENSPEC_VERSION 형태 확인 필요)" → 확인: 설치 문서는 "`OPENSPEC_VERSION=v1.15.0` to pin a release"까지만 적고 명령 줄 전체는 없음, v1.17.0 `scripts/binary/install.sh`가 환경 변수 `OPENSPEC_VERSION`을 읽음(`version="${OPENSPEC_VERSION:-latest}"`) → 원고의 `| OPENSPEC_VERSION=v1.17.0 sh` 형태는 유효, 문장을 그 사실로 교체 — 근거: docs/installation.md, install.sh(웹 2차)
- "2026년 10월 이전 글에서 `npm install -g`로 시작하는 안내를 봤다면 그 내용은 낡았다" → "2026년 10월 24일 이전 글 ... 기본 설치 방법으로는 낡았다" — v1.15.0 릴리스일은 2026-10-24이고 npm은 여전히 대안 경로(Node.js 22.12.0+). 근거: 01_reference.md §4.2, research/web.md 자료 13, GitHub releases API(v1.15.0 2026-10-24T00:50Z)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음) — 장 머리 "OpenSpec v1.17.0/2026-11-09 기준" + 2.0 예고·릴리스 노트 확인 권고 있음. 새로 넣은 소스 근거에는 "v1.17.0 소스 기준"을 붙임
### ✅ 확인 (요약)
- 설치·구조·명령 약 20건: 독립 실행 파일 기본(v1.15.0), `~/.local/bin`, npm Node.js 22.12.0+(v1.16.0), init 후 `specs/`·`changes/`·`config.yaml`, Claude Code 스킬·명령 설치 경로, core 6개·확장 프로필(`openspec config profile` → `openspec update`)·onboard 첫 변경 권고, propose 출력 형태(예시 라벨), 스킬 표기 `/openspec-propose`·`/openspec-apply-change`, 하네스별 표기 4종·Copilot CLI 제한, 레거시 명령 — 01_reference.md §4.2, research/web.md 자료 13·14
- 문서 형식·규칙: proposal/design/tasks 헤딩, tasks 모범 사례 4개, writing-specs 인용 3개("One statement, one `SHALL`/`MUST`.", tester 질문, "A good change has one intent…") 원문 일치, 체크리스트 6항, 병합 규칙 4행·`retire_capabilities: true`, RENAMED 문서 불일치, archive 원문 "Archive won't block on incomplete tasks, but will warn", archive 경로 `changes/archive/YYYY-MM-DD-<name>/`, v1.16.0/1.16.1 validate 변화 — §4.2, web.md 자료 15
- 2.0 공지 원문 "command files (`/opsx:*`) go away in OpenSpec 2.0.", `openspec config set delivery skills && openspec update`, #2022 — §4.2
- 근거와 한계: Uvik(실행 2026-10-15, 42/50=84%, 대조군 72%, +12%p, 잡음 대역 ±10%p 밖 유일, 드리프트 2.4%, 스펙 단계 12분, 길이 93줄, 병합까지 36분 vs 29분, claude-sonnet-5, 버전 번호 없음), Radar Vol 35(2026-11-04) Trial·브라운필드·예측 가능·마크다운 다량·리빙 스펙 유지 규율(sdd-report.md 2570행), Razor Pages 단일 실험, Talk Think Do 2026-06-01, 사전 거버넌스 약함(추론), Spec Kit #620(2025-09-27), 제조사 "바꿀 부분만"·PRD 일괄 변환 경고 — §2.2·§2.5·§1.8, research/community.md
- 예제 정전·산수: C2 요구 11개·시나리오 15개(직접 셈 2+3+1+1+1+1+2+1+1+1+1), 열 번째 요구 "환불 사유", 정률 안분 1,200/10,800, 1,285/857/858, 37,800, 168시간 경계 2026-11-09T10:00:00/10:00:01, C3 336시간 경계 2026-11-02T10:00 + 336h = 2026-11-16T10:00:00(접수)/10:00:01(거절), 사유 코드 4종·`(Previously: 168시간)`·REMOVED+OTHER 메모, 두 변경 뒤 요구 11−1+2 = 12, 발췌 "요구 아홉 개가 이어진다"(11−2) — 02_plan.md 정전·6장 SPEC.md와 일치
- 명령 대응표(Spec Kit `/speckit-analyze` 읽기 전용, `/speckit-converge`, Superpowers `brainstorming`·`executing-plans`) — §4.1·§4.5
- 예시 라벨: propose 출력("실제로 실행해서 받은 출력이 아니라 형태를 보여 주는 예시"), proposal·델타(C2) 명시. design.md 발췌, tasks.md, 메인 스펙 발췌, C3 델타, 최종 폴더 트리에 "이 책 예제" 라벨 보강(사실 정정 아님)
### 미해소
- (없음)
- 참고: v1.17.0 실제 스킬 폴더 이름이 `openspec-sync-specs`, `openspec-verify-change`임을 저장소에서 봤다. 원고 상자는 "문서에서 확인한 스킬 이름은 둘뿐, 나머지는 설치 폴더로 확인"이라 사실상 틀리지 않아 손대지 않음. 부록 B 명령 대응표를 쓰는 쪽에서 참고 가능

## 03장 (라운드 2 — 수락 게이트 지적 반영)
- ❌→정정: "다만 그 다섯에 집합 단위 기준은 없었고" → AQUSA v1의 5개 기준(Atomic, Minimal, Well-formed, Uniform, Unique) 중 Unique·Uniform은 QUS 분류상 집합 기준이다 (research/papers.md 222–228). 문장을 "그 다섯 가운데 집합 단위 기준은 Unique·Uniform처럼 겉모양을 보는 둘뿐이었다. 모순 없음이나 완결성처럼 뜻을 따져야 하는 집합 기준은 도구로 잡기 어렵다고 보는 편이 맞다."로 교체. 사용자 승인(2026-11-10). 03_final.md·04_manuscript.md 동시 반영.
### 미해소
(없음)
