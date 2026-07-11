<!-- fact-checker 로그 · tech-book · 단일 append 파일 (샤딩 금지) · 챕터별 `## {NN}장` 섹션 -->

# Fact-check log — Learning in the harness

각 챕터 섹션에 라운드별로 append한다. 판정 라벨: ✅확인 / ❌정정(필수) / ⚠️출처없음·귀속(약화·보강) / 🕒신선도.

---

## 7장 — 익숙한 스택을 떠날 때

### 라운드 1 (2026-07-11) · 요청: writer-3 (style 합의 후)

- 대상: `chapters/07_draft.md`
- `(사실 확인 필요)` 마커: 0건 (원고에서 확인) — 해소할 미결 없음
- 신규 식별자(arXiv/DOI/URL): 없음 → 날조·의심 식별자 위험 없음
- 웹 2차 에스컬레이션: 불필요 (모든 Critical 주장 레퍼런스 1차 대조로 확정)

#### ⚠️ 귀속 정밀화 (1건 — 값은 정확, 출처 표현만 수정 권고)
- [원문] "컴파일 에러의 94%가 타입 체크 실패에서 나온다는 관찰이 있다(**GitHub 2025 데이터 기준**)" (L113)
  - 값 **94%** = ✅ 정확. 그러나 이 수치는 GitHub 자체 텔레메트리가 아니라 **Octoverse 2025 리포트가 인용한 2025년 한 학술 연구**의 결과다. "GitHub 2025 데이터 기준"은 GitHub이 직접 산출한 데이터로 오독될 소지.
  - 권고: "GitHub Octoverse 2025 기준(리포트가 인용한 2025년 연구)" 또는 최소 "Octoverse 2025 기준"으로 귀속을 좁혀라.
  - 근거: `research/web.md` §0 검증3 — Octoverse 원문 "A 2025 academic study found 94% of LLM-generated compilation errors were type-check failures." / `01_reference.md` §6-2·신선도 원장.

#### 🕒 신선도
- Octoverse 2025 순위·94%는 신선도 높음(2025-08 기여자 수 스냅샷). 본문에 "Octoverse 2025 기준" 라벨 이미 있음 → 유지. 94% 문장도 위 귀속 수정과 함께 동일 라벨을 명확히.

#### ✅ 확인됨
- "FastAPI is to Python what Spring Boot is to Java" — `01_reference.md` §4-2 / `web.md` 자료 11 verbatim 일치. "안내들이 반복해서 건네는 문장"으로 일반 귀속 — 적절.
- Uvicorn(ASGI)↔Tomcat/Undertow, Pydantic↔Bean Validation·DTO, @GetMapping↔@app.get — §4-2 대응표 일치. API 명칭 모두 유효.
- 철학 차이(스프링=추상화 위 추상화 / FastAPI=HTTP에 가깝고 타입이 무거운 일) — §4-2 / web.md 자료 11 "lets Python's type system do the heavy lifting" 일치.
- "FastAPI does not dictate a strict project structure like Spring Boot does" — §4-2 표현과 일치 (FYI: 원문은 뒤에 "or provide built-in tools"가 더 붙는다 — 아래 참고).
- "FastAPI is all based on these type hints" / "based on Pydantic" — §4-2 / web.md 자료 10 FastAPI 공식 문서 verbatim 일치.
- 먼 전이(far transfer): "심층 원리를 익혔을 때만 새 영역으로 전이" — §3-5 Barnett & Ceci(2002) 일치.
- 초보=표면/전문가=심층 원리 표상, 전문성=지식 조직화 — §3-5 Chi, Feltovich & Glaser(1981) 일치.
- TypeScript GitHub 최다 언어(Octoverse 2025 기준) — §6-2 / web.md §0 검증3 일치(2025-08 기여자 수). 스냅샷 라벨 적절.
- METR 콜백(느낌 vs 실측 부호 반대, 암묵적 저장소 맥락) — §3-2. 수치 재제시 없이 방향만 재진술 → 2장 분업과 정합, 재인용 아님. "historical" 라벨은 수치 미재제시라 여기선 불요.
- 코드 예시 2종(Pydantic BaseModel 기본형 / TS `as any`) — 버전 비민감 기본 문법. Pydantic 예시에 버전 휘발성 경고 부착 확인(🕒 적절 처리).
- 프론트 자동화(Swagger→TS 타입·API 훅·테스트·PR, Cursor Rules) — §6-2 / web.md 자료 12 일치.

#### FYI (선택 · 비차단)
- 인용 "FastAPI does not dictate a strict project structure like Spring Boot does": 원문(`research/community.md`)은 "...structure **or provide built-in tools** like Spring Boot does." 뜻 왜곡 없는 정당한 부분 인용이고 `01_reference.md` §4-2도 동일 절단을 쓰므로 **필수 수정 아님**. 완전 충실을 원하면 "…" 또는 절 복원 가능.

**판정 요약:** ❌ 0 / ⚠️ 1(귀속 정밀화) / 🕒 1(라벨 유지·확장) / ✅ 다수. 미해소·BLOCKING 없음. 94% 귀속 문구만 좁히면 통과.

### 라운드 2 (2026-07-11, 재확인) · writer-3 반영 보고
- `chapters/07_final.md` L113 grep 확인: "…(GitHub 2025 데이터 기준)" → "…(**GitHub Octoverse 2025 리포트가 인용한 2025년 연구**)". 값 94% 유지, 귀속 정정 반영 완료. ✅ **7장 통과.** 나머지 ✅·FYI 변동 없음.

---

## 1장 — 두 개의 피드백 루프

### 라운드 1 (2026-07-11) · 요청: writer-1 (style 합의 후)

- 대상: `chapters/01_draft.md` (프레이밍 장)
- `(사실 확인 필요)` 마커: 0건 (원고 확인)
- 신규 식별자(arXiv/DOI/URL): 없음 → 날조·의심 식별자 위험 없음
- 하드체크(§5-5) 대응: Codex **95.7% 수치 의도적 미사용** 확인 — 준수 ✅
- 웹 2차: 불필요 (전 주장 레퍼런스 1차 대조로 확정)

#### ⚠️ 귀속·시점 정밀화 (2건 — 값·사실은 옳음, 출처/시점 표현만)
- [원문] "LLM이 만든 코드에서 발생하는 컴파일 에러의 94%가 타입 검사에서 걸린다는 집계도 있다(**같은 2025 스냅샷 기준**)" (L74)
  - 값 **94%** ✅ 정확. 그러나 이 수치는 Octoverse의 기여자 수 스냅샷 텔레메트리가 아니라 **Octoverse 2025 리포트가 인용한 2025년 한 학술 연구** 결과. "같은 2025 스냅샷 기준"은 스냅샷 집계로 오독될 소지.
  - 권고: "**GitHub Octoverse 2025 리포트 기준**(리포트가 인용한 2025년 연구)"로. **← 7장 동일 수치와 문구 통일 필요(editor 용어 일관성).**
  - 근거: `research/web.md` §0 검증3 / `01_reference.md` §6-2·신선도 원장.
- [원문] "OpenAI는 … Codex CLI를 **통째로 Rust로 다시 썼다**(**InfoQ 2025년 6월 보도 기준**), 그 이전 버전은 TypeScript" (L76)
  - 사실 자체 ✅ (Rust 재작성 실재, 이전 스택 TS 맞음 — `01_reference.md` 최초 오픈소스 2025-04 TS). 그러나 **InfoQ 2025-06은 '재작성 결정·네이티브 전환 발표'를 다룰 뿐 완성된 "통째로 다시 썼다"를 보도하지 않았다**(완성 근접 상태 95.7%는 저장소 2026 초 기준). "통째로 다시 썼다(InfoQ 2025-06 기준)"는 결정 보도를 완성 사실로 당김.
  - 권고(택1): (a) "Rust로 다시 쓰기로 하고 네이티브 재작성에 들어갔다(InfoQ 2025-06)"로 시제 완화, 또는 (b) 완성 상태를 굳이 말하려면 그 부분만 "openai/codex 저장소 2026 초 기준"으로 시점 분리.
  - 근거: `research/web.md` §0 검증4 / `01_reference.md` §5-5·신선도 원장.

#### 🕒 신선도
- Octoverse 순위·94%: 본문에 "2025년 10월 발표, 데이터는 2025년 8월 스냅샷 기준" 라벨 명시 — 우수. 94% 문장은 위 귀속 수정과 함께 유지.

#### ✅ 확인됨
- HN "AI is making me dumb" 556pt + `Quarrelsome` 인용: `01_reference.md` §4-1 / `community.md` 일치. **556은 스레드 점수**(개별 댓글 추천수 아님) — 올바른 사용. 한글 번역 자구 충실(원문 "I get paid more … Is it dumb or just clever delegation?" 대조 — 의역 아닌 충실역), 핵심 영문구 병기.
- 배민 이재홍 하네스 정의 "AI가 길을 잃지 않고 안정적으로 일할 수 있도록 외부 통제 환경을 구축하는 것" (2026-04): §1 / web.md 자료 6 verbatim 일치. 저자·날짜 정확.
- 배민 "프롬프트 → 환경·맥락 설계" 무게중심 이동: web.md 자료 6 충실 요약.
- Anthropic 공식 "통과냐 실패냐를 내놓는 무언가를 쥐여주면 루프는 알아서 닫힌다": §1 / web.md 자료 4 "produces a pass or fail, and the loop closes on its own" 충실역.
- TypeScript Octoverse 2025 최다 언어(JS·Python 제침): §6-2 / web.md §0 검증3 일치.
- Codex 이전 스택 TypeScript: §0·신선도 원장 일치.
- Rust borrow checker 컴파일 시점 메모리 안전 강제: 일반 정확.

**판정 요약:** ❌ 0 / ⚠️ 2(94% 귀속·Codex 시제) / 🕒 라벨 우수 / ✅ 다수. 미해소·BLOCKING 없음. 두 문구만 다듬으면 통과. **94% 귀속은 7장과 문구 통일 권고.**

### 라운드 2 (2026-07-12, 재확인) · writer-1 반영 보고
- `01_final.md` grep 확인:
  - L74: "…걸린다는 연구 결과도 있다(**GitHub Octoverse 2025 리포트가 인용한 2025년 연구 기준**)" — 94% 귀속 정정 반영 ✅ (7장과 문구 통일).
  - L76: "Codex CLI를 **Rust로 다시 쓰기로 하고 네이티브 재작성에 들어갔다**(InfoQ 2025년 6월 보도 기준, 그 이전 버전은 TypeScript)" — 시제 완화 반영 ✅.
- **1장 통과.** ⚠️ 2건 모두 해소, 미해소 없음.

---

## 8장 — 주니어를 위한 다른 지도

### 라운드 1 (2026-07-11) · 요청: writer-3 (style 합의 후)

- 대상: `chapters/08_draft.md`
- `(사실 확인 필요)` 마커: **1건 (Voss 노동 수치) — 웹 2차로 해소(아래).**
- 신규 식별자(arXiv/DOI/URL): 없음 → 날조 위험 없음
- 하드체크(§5-5): Voss 개별 수치 → 웹 2차 에스컬레이션 실행(Critical+마커)

#### 🔴→✅ 하드체크 해소 — Voss 노동 수치 (웹 2차 완료, seldo.com 원문 대조)
- [원문] "신입 공고 약 −28% · CS 졸업생 실업률 6.1% (사실 확인 필요: Voss 2026-07 인용, BLS·ADP 원 출처 대조 필요)"
- 웹 검증(https://seldo.com/posts/ai-has-torched-the-market-for-junior-programmers):
  - **−28% 신입 공고 = ✅ 확인.** 원문 "Entry-level software postings are down 28% from their 2022 peaks." (2022 정점 대비 — 본문 프레이밍과 일치)
  - **6.1% CS 졸업생 실업률 = ✅ 확인.** 원문 "Computer science graduates now have a 6.1% unemployment rate, higher than liberal arts majors."
  - **1차 출처 정정 메모:** 6.1%의 원 출처는 **뉴욕 연준(Federal Reserve Bank of New York)** — 마커가 추정한 BLS·ADP 아님. 22–25세 −19%·41–49세 +14%는 ADP/Stanford, 컴퓨터 프로그래머 −16%·웹 개발자 −11%는 BLS OEWS(2024-05~2025-05). 본문은 Voss에게 귀속했고 두 수치 모두 Voss 원문에 실재하므로 **판정 ✅**.
- 판정: **✅ 확인됨 — 마커 반드시 제거(final에 잔존 불가).** 수치 유지, Voss 귀속·논쟁적 진단·비인과 프레이밍 유지. (선택) 6.1% 원 출처를 명기하려면 "뉴욕 연준"으로.

#### ✅ 확인됨 (요청 대조 지점 전부)
- evan-moon 3인용("10년…1년 반복"·"뇌는 편하면 기억 안 함"·"AI 없이 판단할 수 있는 개발자"): `community.md`/§4-1 국문 원문 verbatim 일치.
- teo("담론/현실 간극"·"스스로 생각하기 포기로 대체당함"): §4-1/§5-4 일치(간극은 충실 요약, "대체당함"은 verbatim).
- gchamonlive("AI는 의도를 증폭할 뿐"): §4-1 "LLM changed nothing … boosting people's intention" 충실역. 뒤의 '반대로…' 확장은 저자 해석(비인용) — 정당.
- kimjoin2("복붙 주니어는 스택오버플로우 시대에도"): §5-3 일치(원문 "단순 복붙…쓸모가 없었습니다"의 충실 재서술 — FYI 아래).
- Fastly(2025-08 자체 설문, 시니어가 더 많이 출하): 2.5배 수치 미사용·벤더 설문 캐비엇·시점 명기 — 안전 처리 ✅. (FYI: Fastly 원 지표는 'AI 생성 코드 과반 출하 비율' 32% vs 13%.)
- BLS "향후 10년 두 자릿수 성장": §5-3 "2024–2034 15% 성장"을 "두 자릿수"로 안전 뭉갬 — 적정 ✅.
- CIO "월 몇 달러 AI vs 연봉 수천만 원 주니어": §6 "$10 Copilot vs $90K junior"의 정성 로컬라이즈(비인용 특징화) — 허용. (FYI: 원 수치 $90K는 "수천만 원"보다 큼 — 특징화라 비차단.)
- 개념: 생성 효과=사전지식 요구(§6-3·§5-1, **필수 단서 병기 확인**), 전문성 역전(§3-3), CHI 구조화 루프 학습 저해 없음(§5-1), Koli "구조 없으면 먼저 위임"(§2-3 무수치), 역량의 착각/수행≠학습(§3-3), 자동화 안주 전문가도 예외 아님·항공/의료(§3-4), Osmani 주니어 최취약(§6-3) — 전부 일치.
- **2장 Stanford ~20% 재제시 없이 콜백만**: 확인(L21 위험 구조 재인용, 수치 미재제시) — 분업 정합.

#### FYI (선택 · 비차단)
- kimjoin2 인용: 원문은 "단순 복붙하는 주니어 개발자는 스택오버플로우 시대 때에도 쓸모가 없었습니다." 본문은 뜻 동일한 재서술. 따옴표 인용이라 엄밀 verbatim 원하면 원문 자구로.
- CIO $90K → "연봉 수천만 원"은 로컬라이즈. Fastly는 'AI 생성 코드 과반 비율' 지표. 둘 다 정성 특징화라 통과.

**판정 요약:** ❌ 0 / ✅ 다수(하드체크 Voss 웹 2차로 해소) / FYI 2. **BLOCKING: 마커 제거 필수**(수치는 확인됐으니 유지·마커만 삭제). 그 외 통과.

---

## 9장 — 인지 작업의 소유권

### 라운드 1 (2026-07-11) · 요청: writer-3 (style 합의 후)

- 대상: `chapters/09_draft.md` (종합·회고 장)
- `(사실 확인 필요)` 마커: 0건
- 신규 식별자·신규 수치·신규 인용: **없음** — 전부 앞 장 확정 사실의 콜백
- 지어낸 수치/인용 스캔: **없음** ✅

#### ✅ 확인됨
- evan-moon "1년짜리 경험 10번 반복 ≠ 10년" 콜백(§4-1) — verbatim.
- 생성 효과 "스스로 생성·인출한 것만 남는다" 개념 콜백(§3-3) — 무수치, 정확.
- METR "느려졌다" 방향만, 개별 수치 재제시 없음 — 2장 분업 정합 ✅.
- 70%/30%·최종 게이트(4장), 두 루프(1장), 다이얼 탄생(3장), 디버깅 격차(2장), 흐름 안·밖(5·6장) — 전부 확정 사실 콜백, 신규 주장 없음.
- Quarrelsome 질문 콜백(L69) — 원문 의미 충실.

#### FYI (선택 · 비차단 · editor 참고)
- Quarrelsome 인용 자구가 1장과 9장에서 미세하게 다르게 옮겨짐(1장 "내가 직접 코드를 치는 건 아니다…" / 9장 "나는 코드를 안 쓰지만…"). 둘 다 원문 충실. 통권 일관성 원하면 editor가 한 표현으로 통일 권고.

**판정 요약:** ❌ 0 / ✅ 전량 콜백 확인 / 날조 없음. 미해소·BLOCKING 없음. **9장 통과.**

---

## 2장 — 위임한 만큼 배우지 못한다 (핵심 실증 장 · 하드체크 밀도 최상)

### 라운드 1 (2026-07-12) · 요청: writer-1 (style 합의 후)

- 대상: `chapters/02_draft.md` · `(사실 확인 필요)` 마커: 0건
- 신규 식별자: arXiv:2507.09089 · DOI 10.1038/s43588-025-00845-2 — **둘 다 레퍼런스와 정확 일치, 날조 아님**(2507=2025-07 과거, DOI 정합).

#### ✅ 확인됨 — 하드체크 전부 정확 처리
- Anthropic 실험: 50% vs 67%(17퍼센트포인트·"거의 두 학점"), Cohen's d=0.738·p=0.01, n=52(대부분 주니어), 과제=Trio(파이썬 비동기) 기능 2개, AI 약 2분 빠름·비유의, **디버깅 격차 최대**, 완전위임 40% 미만, 고득점 3결(선생성-후이해/혼합/개념질문) — §3-1 전부 일치. **시드 "65% 이상" 상단값 미사용 확인**(하드체크 준수).
- METR: +19% 느림, 사전 −24%·사후 −20% vs 실측 +19%(부호 반대), 16명·246이슈, Cursor Pro+Claude 3.5/3.7 Sonnet, 느려짐 5원인, **"historical" 라벨 병기 확인** — §3-2 일치. arXiv:2507.09089 정확.
- Nature Comp Sci 2025(DOI 10.1038/s43588-025-00845-2): 미탐지 오류 수용·명령어 주입·미정의 변수 **3주+ 지속**, 관점/재현부족 유보 병기 — §3-6 일치.
- **[하드체크] Stanford "Canaries"**: SW개발자 22~25세 ~20%↓(2022말 정점 대비)·30세+ 6~12%↑·2025-11 발표·데이터 2025-09까지·ADP — §3-7 일치. **13%(직군 전반) vs 20%(SW개발자)를 "집계 단위가 다른 숫자"로 명시 구분 확인 — §5-5 하드체크 정확 준수.** 인과 회피·위험 구조로만 처리 확인.
- Bjork 수행≠학습, testing effect(다시읽기<인출·학습자 오판) — §3-3 개념 정확.
- 한계 전 항목 병기(52명 소표본·단일단기·상관 not 인과 / METR 16명·특정조건 / Nature 관점·재현부족 / 노동 인과 회피) — 지적 정직성 확보.

**판정 요약:** ❌ 0 / ⚠️ 0 / ✅ 전부. **모범적 하드체크 처리(13 vs 20 구분·METR historical·65% 미사용·식별자 정합). 2장 통과.**

---

## 4장 — 하네스의 마지막 게이트는 사람이다

### 라운드 1 (2026-07-12) · 요청: writer-2 (style 합의 후)

- 대상: `chapters/04_draft.md` · `(사실 확인 필요)` 마커: 0건
- 신규 식별자: 없음(AI & Society·Nature는 저널명만, DOI 미인용 — §3-6이 AI&Society DOI를 "계열 wildcard"로 표시했으므로 특정 DOI 미인용은 오히려 안전). 날조 위험 없음.

#### ✅ 확인됨
- Osmani "Beyond the 70%"(2025-03) 70/30·우발적 복잡성·30% 인간 전문성 / "If you're not actively engaging with why…you might actually learn less" — §2-2 verbatim 일치.
- Anthropic "Give Claude something that produces a pass or fail, and the loop closes on its own" / 게이트 4단계 / "the agent doing the work isn't the one grading it" — §1·§4-3 verbatim 일치. (Stop hook "8연속"을 "정해진 횟수만큼"으로 안전 일반화 — 적정.)
- Koli 2023 "760개 중 92% 먼저 위임" — §2-3 일치.
- AI & Society(2025) "deskilling 구조적 문제" + Nature(2025) 미탐지 오류 3주+ + 최신·재현부족 유보 — §3-6 일치.
- Willison vibe coding 구분(읽고·테스트하고·이해했으면 아님) — §1·§4-3 일치.
- 시드 인용 "시스템이 자신의 최종 품질 게이트를 마모시키는 기본값 위에 서 있다면 … 설계 결함이다" — §0 verbatim 일치.
- georgemcbay(사회 위험 프레임)·pton_xd(어셈블리 비유) — §5-3·§5-4 충실.

#### FYI (선택 · 비차단)
- 커뮤니티 비유 largbae·devolving-dev는 **비인용(따옴표 없는) 귀속 패러프레이즈**로, 화자의 문자 그대로보다 살짝 확장됨. 원문: largbae "My compiler writing skills atrophied with the advent of high-level languages, but in exchange I got more done." / devolving-dev "I'm sure people got worse at arithmetic after the invention of the calculator." 레퍼런스 §5-3이 이들을 "컴파일러 비유/계산기 비유"로 이미 분류했고 gist 일치하므로 **비차단**. 화자에게 말을 얹지 않도록 패러프레이즈를 원문 취지에 묶어두면 더 안전.

**판정 요약:** ❌ 0 / ⚠️ 0 / ✅ 전부 / FYI 1. **4장 통과.**

---

## 5장 — 흐름 안에서 배우기

### 라운드 1 (2026-07-12) · 요청: writer-2 (style 합의 후)

- 대상: `chapters/05_draft.md` · `(사실 확인 필요)` 마커: 0건 · 신규 arXiv/DOI/URL: 없음

#### ✅ 확인됨
- 생성 효과 Slamecka & Graf(1978)·testing effect Roediger & Karpicke(2006) — §3-3 이름·연도 정확.
- Anthropic 고득점 집단=설명 요구·개념 되묻기(2장 콜백, 수치 미재제시) — §3-1 정합.
- Kent Beck "you own the spec, the AI owns the implementation, so it can't validate its own bugs" / 테스트+구현 동시 생성 금지 / Red 인간 소유 — §4-3 verbatim·정합.
- CLAUDE.md advisory·훅 deterministic·게이트 4단계 — §4-3 일치. **훅 settings.json 예시는 2026 Claude Code 기준, 버전 휘발성 경고 부착 확인(🕒 적정).**
- TS Octoverse 1위·컴파일 에러 94% 타입체크 — **1장 콜백으로 처리, 출처 재인용 없음(시점 앵커 1장 소유) 확인.** 값 정확.
- Cursor Rules/Skills·Swagger→TS 타입·API 훅·테스트·PR — §6-2 일치.
- **book-writer 셀프 레퍼런스 — 저장소 실물 대조 완료:** `docs/learning-loop.md` 실재 ✅ / `02_plan.md` delegation_mode=production ✅ / "설계 근거" 3 기각 대안("아티클 확장판"·"독자별 분권"·"주제별 백과") 실재 ✅. 서술 정확.

**판정 요약:** ❌ 0 / ⚠️ 0 / ✅ 전부(셀프레퍼런스 실물 대조 포함). **5장 통과.**

---

## 6장 — 흐름 밖에서 벼리기

### 라운드 1 (2026-07-12) · 요청: writer-2 (style 합의 후)

- 대상: `chapters/06_draft.md` · `(사실 확인 필요)` 마커: 0건 · 신규 arXiv/DOI/URL: 없음

#### ✅ 확인됨
- Parasuraman & Manzey(2010) 자동화 안주 — 전문가도 예외 아님·단순 연습으로 예방 안 됨·항공/의료 확립·**SW 유추 한계 병기 확인** — §3-4 이름·연도 정확.
- Chi, Feltovich & Glaser(1981) 전문가 표상(초보=표면/전문가=심층·조직화) — §3-5 정확.
- Ericsson 의도적 연습 + **2019 재검토 "필요조건이지 충분조건 아님" 병기 확인** — §3-3 정확.
- expertise reversal(Kalyuga 2003, 3장 콜백)·METR(숙련자 자기 코드베이스 이득 역전, **수치 재제시 없이 질적 콜백만 확인**) — §5-1·§3-2 정합.
- Risko & Gilbert(2016) 인지 오프로딩 / Sparrow et al.(2011) 구글 효과 — **상식 기억 과제 한계·보수적 방향성 인용 병기 확인** — §3-4 이름·연도 정확.
- gchamonlive "LLM changed nothing … boosting people's intention … if your intention is to learn, you are in luck"(6장 owner, HN 핸들 귀속) — §4-1 verbatim 충실역.
- 기술 서술(@Transactional 프록시 자기호출 미적용·체크예외 롤백·ConcurrentHashMap.computeIfAbsent·useMemo/stale closure/useEffect cleanup) — 모두 정확한 프레임워크 사실, 버전 비민감.

**판정 요약:** ❌ 0 / ⚠️ 0 / ✅ 전부(학습과학 인용 이름·연도·필수 캐비엇 전량 정확). **6장 통과.**

---

## 진행 현황 (fact-checker 종합 · 2026-07-12)

| 장 | 판정 | 비고 |
|----|------|------|
| 1 | ✅ 통과(R2) | 94% 귀속·Codex 시제 정정 반영 |
| 2 | ✅ 통과 | 모범 하드체크(13 vs 20·METR historical·65% 미사용) |
| 3 | ⏳ 미요청 | 하드체크 밀도 높음(150%↑·버그83%↓ 배제·Codex 출처 분리·CHI 수치) — 대기 |
| 4 | ✅ 통과 | FYI 1(largbae/devolving-dev 패러프레이즈) |
| 5 | ✅ 통과 | 셀프레퍼런스 실물 대조 완료 |
| 6 | ✅ 통과 | 학습과학 인용 전량 정확 |
| 7 | ✅ 통과(R2) | 94% 귀속 정정 |
| 8 | ⚠️ 마커 삭제 대기 | Voss 웹 2차로 수치 확인, 마커만 제거하면 통과 |
| 9 | ✅ 통과 | 콜백만·날조 없음 |

**미해소·BLOCKING:** 없음. 8장 마커 제거만 남음(수치는 확인됨). 3장 검증 요청 대기 중.

---

## 2장 — 위임한 만큼 배우지 못한다 (불편한 실증)

### 라운드 1 (2026-07-12) · 요청: team-lead 대기열 (fact-checker-2 교체 검증) · 대상: `chapters/02_draft.md`

- `(사실 확인 필요)` 마커: **0건** (원고 전수 스캔 — grep 확인)
- 신규 식별자: arXiv:2507.09089(METR)·DOI 10.1038/s43588-025-00845-2(Nature Comp. Sci.) 2건 → 둘 다 `01_reference.md` §8·신선도 원장에 등재된 기존 식별자. **YYMM=2507(2025-07)은 빌드 시점(2026-07) 이전** → 미래 날짜 아님, 날조 신호 없음. 형식 정상. 의심 식별자 없음
- 웹 2차 에스컬레이션: **불필요** — 모든 Critical 주장이 레퍼런스 1차 대조(§3-1·§3-2·§3-6·§3-7)로 확정

#### ✅ 하드체크 대상 전부 통과 (team-lead 지정)
- **Stanford 13% vs 20% 집계 구분 (§5-5 하드체크 핵심):** 본문 L105가 "AI 노출 큰 직군 전반 젊은 층 = 13%"와 "SW 개발자 22~25세 = 약 20%"를 **명시적으로 다른 집계 단위로 구분**하고 "둘을 뒤섞으면 근거가 헐거워진다"까지 경고. → §3-7·§5-5 지침을 정확히 이행. **모범 처리.**
- **인과 주장 금지 (위험 구조로만):** L107·L109가 "인과로 단정하면 안 된다 / 이 책은 이 데이터를 '위험 구조'로만 취한다 / 이건 의심이지 증명이 아니다"로 반복 방어. 교란 변수(금리·팬데믹) 병기(L107). → §0·§3-7 "인과 아니라 위험 구조" 준수. ✅
- **Nature/deskilling 귀속 정확성:** 3주+ 미탐지 오류(명령어 주입·미정의 변수)를 **Nature Computational Science에만** 귀속(L91), 동반 AI & Society "deskilling 구조적" 논의는 무리하게 끌어오지 않음. → §3-6 귀속 경계 정확. 오귀속 없음. ✅
- **Anthropic "65% 이상" 상단 경계값 회피:** 본문은 고득점 패턴(3결)·저득점 "40% 미만"만 사용하고 **원문 미확인 "65% 이상"은 쓰지 않음**(L33·L35). → §3-1·§5-5 주의사항 준수. ✅

#### ✅ 확인됨 (수치·인용 전량 레퍼런스 일치)
- Anthropic 통제 실험: 52명(대부분 주니어)·Trio(Python 비동기)로 기능 2개·퀴즈 **50% vs 67%**·17퍼센트포인트·"거의 두 학점(letter grade)"·**Cohen's d=0.738·p=0.01**·AI 그룹 약 2분 빠르나 비유의 (L19·21·25) — §3-1 정본 verbatim 일치.
- 고득점 3결(먼저 생성 후 AI 설명=generation-then-comprehension / 코드·설명 오가며=hybrid / 개념 파고들기=conceptual inquiry) + 저득점 완전 위임 "40% 미만" (L33·35) — §3-1 패턴 3종·"40% 미만"과 일치. 방향(고관여>완전위임) 정확.
- "격차 최대 = 디버깅"(L43) — §3-1 일치. 상관≠인과 한계 명기(L53) — §3-1 연구진 자기 단서와 일치.
- 역량의 착각 / 로버트 비요크 수행(performance)≠학습(learning) (L57·61) — §1·§3-3 Bjork 일치. 인물 귀속(Robert Bjork = desirable difficulties·수행/학습 구분) 정확.
- "다시 읽기 vs 스스로 인출" 메타인지 착각(L63) — §3-3 testing effect(Roediger & Karpicke) "재학습이 낫다고 틀리게 확신"과 일치. (수치 없이 방향만 — 안전)
- METR RCT: arXiv:2507.09089·2025-07-10·**19% 느림**·예측 −24%/사후추정 −20%/실측 +19%(부호 반대)·16명·246이슈·Cursor Pro+Claude 3.5/3.7 Sonnet·느려짐 5원인·**"historical" 라벨**·한계(16명·숙련자·성숙 대형 저장소) (L73·75·77·79·81) — §3-2 전부 일치. historical 과장 금지 지침 이행.
- Nature Comp. Science DOI 10.1038/s43588-025-00845-2·3주+ 미탐지 버그·관점/리뷰 성격·재현 부족 한계(L91·97) — §3-6·§8 일치.
- Stanford "Canaries in the Coal Mine?"·2025-11·데이터 2025-09까지·ADP·22~25세 ~20%↓·30세+ 6~12%↑ (L103) — §3-7·신선도 원장 일치.

#### 🕒 신선도 — 적정 처리
- 시점 민감 값(Stanford 노동 데이터·METR·Octoverse 계열) 모두 발행 시점·조건 라벨 부착(2025-11/데이터 2025-09까지, 2025-07-10, historical). 별도 보강 불요.

**판정 요약:** ❌ 0 / ⚠️ 0 / 🕒 0(라벨 우수) / ✅ 전량. 하드체크 4종(13%vs20%·비인과·deskilling 귀속·65% 회피) **모두 모범 이행**. 미해소·BLOCKING 없음. **2장 통과** — 정정 요구 없음.

---

## 3장 — 같은 도구, 정반대 결론 (모순을 화해시키기)

### 라운드 1 (2026-07-12) · 요청: team-lead 대기열 (fact-checker-2) · 대상: `chapters/03_draft.md`

- `(사실 확인 필요)` 마커: **0건** (원고 전수 스캔)
- 신규 식별자: arXiv **2302.07427**(CHI)·**2309.14049**(Koli)·**2302.06590**(Copilot) 3건 → 전부 `01_reference.md` §8 등재 기존 식별자. **YYMM = 2302/2309(2023-02/09) 모두 빌드 시점(2026-07) 이전** → 미래 날짜 아님, 형식 정상, 날조·의심 신호 없음. DOI 신규 없음
- 웹 2차: **불필요** — Critical 주장 전부 레퍼런스 1차 대조(§5-1·§3-2·§4-3)로 확정

#### ✅ 하드체크 대상 전부 통과 (team-lead 지정)
- **"Claude Code 150%↑·버그 83%↓" (§5-5 핵심):** L78이 이 수치를 **"출처 불분명한 화려한 수치"의 경계 사례로 제시**하고 "마케팅성 2차 인용 / 신뢰할 만한 1차 출처를 찾기 어렵다 / 벤더의 주장 정도로만 받아 두는 게 안전"이라 명시. → §5-5 "배제 또는 '벤더 주장' 명시" 지침을 **벤더 주장 명시 + 경계 교훈으로 모범 처리.** ✅
- **METR "historical" 라벨:** L72가 19% 느림에 "'그 시점의 기록'이라는 단서를 달았다"로 historical 병기. 16명·246이슈는 2장에서 확정된 값이라 콜백 시 미재제시(분업 정합). ✅
- **Codex 95% Rust:** 3장에 **미등장** → 출처 어긋남 이슈 발생 안 함(§5-5 항목은 1장에서 별도 처리). ✅
- **시드 "65% 이상" 상단값:** 미사용. CHI/Anthropic/Koli 확정 수치만 사용. ✅
- **expertise reversal(Kalyuga 2003) 서술:** L40 "초보에게 학습을 돕던 안내가 사전지식이 쌓이면 학습·수행을 방해" — §1·§3-3·§5-1 정의와 정확히 일치. 자전거 보조바퀴·자동완성 비유는 저자 예시(비귀속) — 정당. ✅
- **배민 "5년→1달" 귀속:** L84 "배달의민족(우아한형제들) … 2026년 4월 공개된 사례 기준" — §4-3·§8(이재홍 2026-04-17) 정확 귀속. ✅

#### ✅ 확인됨 (수치·인용 전량 레퍼런스 일치)
- CHI 2023(Kazemitabaar 외, arXiv:2302.07427): 69명(10–17세)·45개 Python 과제·Codex·완성률 약 1.15배·점수 약 1.8배·**수동 수정 저하 없음**·1주 지연 사후검사 AI측 약간 우세(비유의) (L17) — §5-1 정본 일치. ("약" 완화는 안전.)
- CHI 하위발견: 사전지식(Scratch 경험) 높을수록 파지 이득 더 큼 → 사전지식×도구 상호작용 (L19) — §5-1 "reversal의 냄새"와 일치.
- CHI vs Anthropic 대조표(결론/대상/도구/맥락) (L29–34) — §5-1 표와 일치.
- **정직한 유보**: "순수 교과서적 reversal 아님 — 사전지식 축 + 도구 양식 축 겹침" (L50) — §5-1 "정직한 유보" 문구를 충실 반영. **과장 회피 우수.**
- Koli Calling 2023(arXiv:2309.14049): "같은 연구진"(Kazemitabaar et al. — §8 확인)·760개 과제·**92% 손코딩 전 곧바로 위임** (L60) — §2-3·§5-1 일치.
- Copilot RCT(Peng 외, arXiv:2302.06590): 처치군 HTTP 서버 **55.8% 빠름**·저경험일수록 이득↑·회사 자체 연구 캐비엇 (L72·74) — §3-2·§8 일치.
- 배민: 확률적 AI + 결정론적 checker(린팅)·**180+ 번역 누락** 방지·데이터 **96.5% 절감** (L86) — §4-3 일치.
- 2×2 좌표(전문성 × 구조)와 각 칸 배치(CHI/Koli/이상/Anthropic·METR) (L102–107) — §5-1 "전문성 수준 × 수용 방식의 구조화" 두 축의 저자 합성. 레퍼런스 논지와 정합, 신규 사실 주장 아님.
- 위임 다이얼 개념·"생산 모드 vs 학습 모드" 손잡이 (L111~) — §0·§1·§7-3 시드 개념과 일치.

**판정 요약:** ❌ 0 / ⚠️ 0 / 🕒 0(라벨 우수) / ✅ 전량. 하드체크 전 항목 이행(150%/83% 벤더 주장 명시·historical·reversal·배민 귀속). 미해소·BLOCKING 없음. **3장 통과** — 정정 요구 없음.

---

## 4장 — 하네스의 마지막 게이트는 사람이다

### 라운드 1 (2026-07-12) · 요청: team-lead 대기열 (fact-checker-2) · 대상: `chapters/04_draft.md`

- `(사실 확인 필요)` 마커: **0건** (원고 전수 스캔)
- 신규 식별자(arXiv/DOI/URL): **없음** — 《Nature Computational Science》·《AI & Society》는 저널명만 표기(DOI 미인쇄), 둘 다 §3-6·§8 등재. 날조·의심 식별자 위험 없음
- 웹 2차: **불필요** — Critical 주장 전부 레퍼런스 1차 대조(§0·§1·§2-2·§3-6·§4-3·§5-3·§5-4)로 확정
- 커뮤니티 인용 자구: `research/community.md` 원문 직접 대조 완료(아래)

#### ✅ 하드체크 대상 통과 (team-lead 지정)
- **Osmani "human 30%" 귀속:** L7 "애디 오스마니(Addy Osmani)가 2025년 3월에 쓴 글 「Beyond the 70%」" — §2-2·§8(2025-03-13 "Beyond the 70%: Maximizing the human 30%") 정확. 70%(우발적 복잡성·보일러플레이트)/30%(엣지케이스·유지보수성·아키텍처·무엇을 왜) 배분·Osmani 원문 "If you're not actively engaging with why the AI is generating certain code, you might actually learn less"(L97) — §2-2 verbatim.
- **maker/checker 논지의 시드 충실성:** 형식화 70%(기계)/형식화 안 되는 30%(인간 최종 게이트), 시드 인용 "시스템이 자신의 최종 품질 게이트를 마모시키는 기본값 위에 서 있다면, 그것은 개인 의지의 문제가 아니라 설계 결함이다"(L71) — §0 verbatim. "유사한 것을 만들어 보고 실패해 본 경험"(L29) 시드 귀속. 예상 반론 3답변(시점/구조 이동/개인 유인)(L117~147) — §0·§5-4 충실. **시드 논증 척추 정확 재현.**

#### ✅ 확인됨
- Anthropic best-practices "Give Claude something that produces a pass or fail, and the loop closes on its own"(L15) — §1 verbatim.
- Anthropic 검증 게이트 4단계(in-prompt→목표조건→Stop hook→검증 서브에이전트)·"the agent doing the work isn't the one grading it"(L19) — §4-3 verbatim. Stop hook "8연속"은 "정해진 횟수만큼 연속"으로 안전 일반화(특정 숫자 미주장).
- deskilling 귀속: "구조적 문제(deskilling)"→《AI & Society》, 3주+ 미탐지 버그(명령어 주입·미정의 변수)→《Nature Computational Science》(L77) — §3-6 **두 저널 귀속 분리 정확**(2장=Nature만, 4장=둘 다 — 각각 올바름). 재현 부족·논평 성격 한계 병기(L79).
- Simon Willison vibe coding 구분(모든 줄 LLM이 써도 읽고·테스트·이해했으면 vibe coding 아님)(L91) — §1·§7-1 일치, 귀속 정확.
- Koli 760개·92% 먼저 위임(L67) 콜백 — §2-3·§5-1 일치.

#### ✅ 커뮤니티 인용 대조 (community.md 원문 확인)
- **georgemcbay**(L145): 원문 "AI will remain at roughly current levels and we'll dull our skills … innovation will stall because we've offloaded too much of the thinking"(community.md L29) → 본문 "AI가 현재 수준에 머무는데 우리가 사고를 너무 많이 오프로딩해서, 혁신 자체가 정체되는 것" — **충실역.** §5-4 일치. 핸들 귀속 정확.
- **largbae·devolving-dev·pton_xd**(L113): 세 핸들 community.md L208–210 실재·귀속 정확. §5-3 "컴파일러/계산기/어셈블리 비유"와 일치.

#### FYI (선택 · 비차단 · editor 참고 — 의역 표시)
- 세 핸들은 **직접 인용이 아니라 "비유를 든다/단언한다"는 특징화**로 제시됨. 원문 자구 대조:
  - `largbae` 원문 "My compiler writing skills atrophied with the advent of high-level languages, but in exchange I got more done" → 본문은 "컴파일러 등장으로 어셈블리를 몰라도 소프트웨어를 만든다"로 **방향 재구성**(원문은 '컴파일러 작성 능력'이 고급언어로 위축). 핵심(추상화 상승→하위 스킬 불요) 보존. 특징화라 비차단.
  - `devolving-dev` 원문 "I'm sure people got worse at arithmetic after the invention of the calculator"(중립 관찰) → 본문 "문명이 퇴보했는가? 아니다, 더 높은 수학으로 올라갔다"는 **저자 부연**(devolving-dev 발언 아님). 비유 귀속은 타당, 확장은 저자 목소리.
  - `pton_xd` 원문 "thinking will be like efficiently coding in assembly, no longer necessary" → 본문 "코드를 직접 읽고 쓰는 능력이 … 필요 없어질 것"은 **의역**('thinking'→'코드 읽고 쓰기' 미세 이동). 방향 일치, §5-3 요약과 정합.
  - → 셋 다 anecdotal 특징화이고 레퍼런스 gloss와 정합 → **필수 수정 아님.** 완전 충실 원하면 editor가 "취지" 표현으로 완화 또는 원문 병기 가능.

**판정 요약:** ❌ 0 / ⚠️ 0 / 🕒 0 / ✅ 전량 / FYI 1(커뮤니티 의역 3건, 비차단). 하드체크(Osmani 30%·maker/checker 시드·deskilling 귀속) 모두 통과. 미해소·BLOCKING 없음. **4장 통과** — 정정 요구 없음.

---

## 5장 — 흐름 안에서 배우기 (상호작용 기본값을 하네스에 새기기)

### 라운드 1 (2026-07-12) · 요청: team-lead 대기열 (fact-checker-2) · 대상: `chapters/05_draft.md`

- `(사실 확인 필요)` 마커: **0건** (원고 전수 스캔)
- 신규 식별자(arXiv/DOI/URL): **없음** — 학습과학 원전은 저자·연도만 표기(§8 등재). 코드 블록(settings.json·markdown 커맨드·Python 테스트)은 illustration, 식별자 아님. 날조 위험 없음
- 웹 2차: **불필요** — 학습과학 귀속·Anthropic·Willison·Kent Beck 전부 레퍼런스 1차 대조로 확정. **셀프 레퍼런스는 로컬 정전 문서 2건 직접 대조**(아래)

#### ✅ 하드체크 대상 통과 (team-lead 지정) — 셀프 레퍼런스 정확성 (Critical)
book-writer '운영자 학습 루프' 셀프 레퍼런스(L156–174)를 `docs/learning-loop.md`(정전 스펙)·`learning-in-the-harness/02_plan.md`와 **직접 대조** → 전부 정확:
- L160 "문서 이름은 '운영자 학습 루프'" — learning-loop.md 제목과 일치. ✅
- L164 "02_plan.md '설계 근거' 섹션 의무 / 기각 대안 2개 이상 + 기각 사유" — learning-loop.md L38 "02_plan.md에 '설계 근거' 섹션 의무화 … 기각한 대안 구조 2개 이상 + 기각 사유"와 **정확 일치.** 그리고 "실제 세 개의 기각 구조 — '아티클 확장판'·'독자별 분권'·'주제별 백과' — 가 각각 기각 사유와 함께" — **02_plan.md L57·59·61·199에서 세 명칭·기각 사유 verbatim 확인.** ✅✅
- L166 선판단 초대 "이 주제·독자라면 어떤 챕터 흐름을 기대하시나요? 한두 줄이면 됩니다(건너뛰어도 됩니다)" — learning-loop.md L37 near-verbatim 일치, "선판단 후공개(Phase 3)". ✅
- L168 설명 가능성 자문 "이 책의 핵심 논지를 남에게 한 문단으로 설명할 수 있는가? 막히는 지점이 바로 직접 읽을 지점이다" — learning-loop.md L39 near-verbatim(원문 "막히는 지점이 직접 읽을 지점" — "바로"만 첨가, 무해). ✅
- L170 learning/production 모드("이 주제를 공부하려고" 신호→learning, 선판단 초대 기본 단계 승격·첫 챕터 직접 읽기 권유 / 신호 없으면 production) — learning-loop.md L59·60·63·64와 일치. 위임 다이얼 실물(6장 예고) 정합. ✅
- L172 비블로킹("응답 안 하거나 자율 실행 중이면 생략, 품질 게이트는 fact/continuity/acceptance로 별도") — learning-loop.md L70 불변 원칙 1과 일치. ✅
- **셀프 레퍼런스는 날조 위험이 가장 큰 지점인데 정전 문서와 near-verbatim으로 대조됨 — 모범.**

#### ✅ 기술적 정확성 (CLAUDE.md·훅·TDD 예시 — team-lead 지정)
- **훅 예시(L69–84):** `settings.json` → `hooks.PreToolUse[].matcher: "Bash"` + `hooks[].{type:"command", command}` — 2026 기준 Claude Code 훅 스키마와 **일치**(matcher=도구명, command 타입). L88 신선도 캐비엇("도구 버전에 따라 바뀔 수 있다 … illustration … 공식 문서 확인") 부착 — 🕒 적정.
- **커스텀 커맨드(L90–102):** `.claude/commands/design-first.md` + `$ARGUMENTS` — Claude Code 커스텀 슬래시 커맨드 형식 정확(마크다운 파일 + 인자 플레이스홀더). ✅
- **CLAUDE.md 규칙(L55–63):** advisory 성격·"테스트(Red)와 구현(Green)을 같은 응답에 함께 만들지 않는다" 등 — 책 처방과 정합, 기술적으로 타당. ✅

#### ✅ 확인됨 (학습과학·인용 귀속)
- 생성 효과 = **슬라메카와 그라프 1978**(L17) — §3-3·§8 일치. testing effect = **로디거와 카픽 2006**(L21) — §3-3·§8 일치. 둘 다 인물·연도 정확 귀속.
- Anthropic 실험 고성과 패턴(설명 요구·개념 되묻기) vs 완전 위임 바닥(L25) — §3-1 콜백 일치.
- Kent Beck TDD "당신이 스펙을 소유하고, AI가 구현을 소유 … 자기 버그를 스스로 검증 못 함"(L114) — §4-3 "you own the spec, the AI owns the implementation, so it can't validate its own bugs"(Kent Beck) 충실역. "테스트+구현 한 응답이면 TDD 무의미"(L116) — §4-3 경고 일치.
- Simon Willison vibe coding 게이트(L29) — §1·§7-1 콜백. Anthropic 게이트 4단계·Stop hook(L86) — §4-3 일치.
- 94% 타입체크 실패·TS 최다 언어(L137) — 1장 확정 사실 **콜백**(수치 재제시하되 새 출처 귀속 안 함 → 1장 final의 "Octoverse 2025 리포트가 인용한 2025년 연구" 귀속과 정합). §6-2 일치. Cursor Rules/Skills·Swagger→TS 타입·API 훅·PR(L141) — §6-2 일치.

**판정 요약:** ❌ 0 / ⚠️ 0 / 🕒 0(훅 캐비엇 우수) / ✅ 전량. 하드체크 2종(셀프 레퍼런스 정확성·기술 예시 정확성) **모두 정전 문서 대조로 통과** — 특히 셀프 레퍼런스가 near-verbatim. 미해소·BLOCKING 없음. **5장 통과** — 정정 요구 없음.

---

## 판정 정본 정리 (team-lead · 2026-07-12)

연결 순단으로 fact-checker(원본)와 fact-checker-2가 병행 가동되어 **2장·4장이 이중 기록**되었다 (5·6장은 원본 단독, 3장은 fc-2 단독). 정리:

- **실질 충돌 없음** — 중복 장 포함 전 장에서 양측 판정 일치: 전부 통과, ❌ 0.
- **중복 장(2·4)의 정본은 fact-checker-2 섹션**으로 한다 (더 늦은 검증, 원본도 동의).
- **8장 Voss 마커 제거 확인 완료** — team-lead가 9개 final 전체를 스캔, `(사실 확인 필요)`·`[리서치 공백]`·`[미완성]` 마커 0건 (2026-07-12).
- 최종 상태: **9개 장 전부 팩트체크 통과, 미해소·BLOCKING 0건.** Phase 4.5 검수자는 이 노트 기준으로 중복 섹션을 해석하면 된다.

---

## 6장 — 흐름 밖에서 벼리기 · fact-checker-2 독립 재확인 (2026-07-12)

team-lead 대기열의 내 배정 장(2·3·4·5·6) 중 마지막. 위 `## 6장`(원본 fact-checker) 판정과 **독립 검증 결과 완전 일치 — ❌ 0, 6장 통과.** 중복 방지를 위해 전체 재기록 대신 확인 사항만 남긴다.

- `(사실 확인 필요)` 마커 0건(grep 확인). 신규/미래 날짜 arXiv·DOI 없음 — 학습과학은 저자·연도만 표기(전부 §8 등재).
- **하드체크(team-lead 지정) 재확인:**
  - Ericsson **1993 + 2019 재검토("필요조건이지 충분조건 아님") 병기**(L61) — §3-3·§8 정확. ✅
  - **위임 다이얼 expertise reversal 콜백**(L80–87): 초보 스캐폴딩↔숙련자 독, 위임도 같은 곡선, METR 숙달 영역 이득 역전 콜백(수치 미재제시) — §5-1·§3-2 정합. ✅
  - Bjork 바람직한 어려움(L80 콜백)·Roediger·Karpicke는 5장에서 확정, 6장 무재인용 — 정합.
- 학습과학 귀속: Parasuraman & Manzey 2010(자동화 안주, SW 유추 한계 병기)·Chi 1981·Risko & Gilbert 2016·Sparrow 2011(구글 효과, 상식 기억 과제 한계 병기) — 이름·연도·캐비엇 전량 정확(§3-4·§3-5).
- **gchamonlive 인용 자구 대조**: `research/community.md` L148·L230 원문 "LLM changed nothing though. It's just boosting people's intention. If your intention is to learn, you are in luck!" → 본문 국역(L97) **충실역**. HN 핸들 귀속 정확.
- 기술 서술(@Transactional 프록시 자기호출 미적용·체크예외 롤백·N+1 지연로딩·ConcurrentHashMap.computeIfAbsent 락 경합·useMemo 의존성/stale closure/useEffect cleanup·key prop 리마운트) — 전부 정확한 프레임워크 사실, 버전 비민감.

**판정 요약:** ❌ 0 / ⚠️ 0 / 🕒 0 / ✅ 전량. 원본 판정과 일치. **6장 통과** — 정정 요구 없음. → **fact-checker-2 배정분(2·3·4·5·6) 전부 완료, 미해소·BLOCKING 0.**
