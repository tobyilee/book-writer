# 팩트체크 로그 — AI Agentic Coding의 4대 엔지니어링

> 장르: tech-book. 대조 기준: `01_reference.md` + `research/*.md` (검색 시점 2026-06-10).
> 판정 라벨: ✅ 확인됨 / ❌ 정정 필요 / ⚠️ 출처 없음·과장 / 🕒 신선도 경고.
> 단일 파일 정책 — 챕터별로 `## {NN}장` 섹션에 라운드 append. 샤딩 금지.

---

## 06장

### 라운드 1 (2026-06-10) — style-guardian 인계분 (L54 단건)

**검증 대상:** L54 "실제로 `AGENTS.md`는 특정 회사 도구를 넘어 업계 표준처럼 자리잡아, 여러 도구가 같은 파일을 읽도록 채택하고 있다."

#### 🕒 신선도 경고 (시점·예시 보강 권고) — 주장 자체는 ✅ 확인됨
- [원문] "실제로 `AGENTS.md`는 특정 회사 도구를 넘어 업계 표준처럼 자리잡아, 여러 도구가 같은 파일을 읽도록 채택하고 있다."
- **판정:** 주장의 사실성은 ✅ 확인됨. 단 (a) 시점 미명기, (b) "여러 도구"가 추상적 — 구체 예시 보강 시 신뢰도↑.
- **근거 (1차):** `01_reference.md` §3-2 L103 "`AGENTS.md`는 사실상 업계 표준(agents.md)으로 다른 도구도 채택" + `research/web.md` 자료 11 (OpenAI Developers, 2026 기준 지속 갱신, 표준 사이트 agents.md).
- **근거 (웹 2차, 2026-06-10 검색):** 공식 https://agents.md/ — "used by over 60k open-source projects", 채택 도구 20+ 명시: OpenAI Codex · Cursor · Aider · Gemini CLI(Google) · VS Code · GitHub Copilot coding agent · Devin(Cognition) · Windsurf · Jules(Google) · Amp · Zed · Warp · JetBrains Junie · goose · opencode · Factory · RooCode · Kilo Code · Augment Code 등. Linux Foundation 산하 Agentic AI Foundation이 표준 관리.
- **권고 정정안 (택1):**
  - (강) "2026년 중반 기준 `AGENTS.md`는 OpenAI Codex가 시작했지만 Cursor·Aider·Gemini CLI·VS Code 등 여러 도구가 같은 파일을 읽도록 채택해, 6만 개 이상 오픈소스 프로젝트가 쓰는 사실상의 업계 표준으로 자리잡았다(공식 표준 사이트 agents.md)."
  - (중) "2026년 중반 기준 `AGENTS.md`는 특정 회사 도구를 넘어 여러 코딩 에이전트가 함께 읽는 사실상의 업계 표준으로 자리잡았다."
  - 최소 요건: **"{2026년 중반/2026 기준}" 시점 1개는 반드시 본문에 박을 것.** 신선도 규율(시점 명기)상 시점 없는 "업계 표준" 단정은 통과 불가.
- **완충 불필요:** 근거가 1차+웹 2차로 강하므로 "~로 보인다"식 톤다운은 불필요. 시점만 박으면 단정해도 좋다.

#### 참고 (이번 인계 대상 아님 — 점검 의견만)
- L62 오픈웨이트 SWE-Bench Pro 점수: writer-3가 `(사실 확인 필요)` 주석으로 본문에 수치를 박지 않고 유보 — **이 판단이 옳다.** 점수표를 본문에 박지 말 것(🕒 변동성 매우 높음, Kimi K2.6 58.6 등은 단일 출처). L62의 해당 주석은 본문에 수치를 넣지 않는 한 final에서 제거해도 무방하나, "박지 않는다"는 서술 자체가 신선도 규율을 잘 지키고 있어 권장 형태다. (단, final 원고에 `(사실 확인 필요)` 문구가 괄호로 남으면 안 됨 — 서술로 흡수하거나 삭제.)

**총평:** L54는 사실 근거 확실(1차+공식 표준 사이트 60k+ 채택 확인). 시점 1개 명기만 추가하면 ✅. 점수표 유보(L62)는 올바른 판단.

### 라운드 2 (2026-06-10) — writer-3 정식 fact-check 요청 (장 전체 전수)

writer-3가 6장 style 합의 완료 후 장 전체 검증 요청. 구체 사실 주장 전수 대조. 라운드 1 정정(L54 시점)은 반영 확인됨.

#### ✅ 확인됨 — 도구 기능 귀속 (요청 항목 2, 전부 §3 일치)
- L28·L30·L32 Claude Code: CLAUDE.md=늘 켜진 컨텍스트·Skills=온디맨드 / Hooks(PreToolUse·PostToolUse)·MCP·Subagents=하네스 / `--dangerously-skip-permissions`(YOLO)·단일 스레드 마스터 루프=루프 → 01_reference.md §3-1 (L95–98) 일치.
- L42 Codex CLI: AGENTS.md=빌드·테스트·컨벤션 에이전트 전용·README는 사람용 / instruction chain 글로벌→루트→cwd → §3-2 (L101–102) 일치.
- L44 Gemini CLI: GEMINI.md 계층적(글로벌+워크스페이스·상위), 연결해 매 프롬프트와 전송 → §3-3 (L106) 일치.
- L56 Aider: repository map·자동 git 커밋·Claude/GPT/DeepSeek 등 거의 모든 LLM·모델 무관 하네스 → §3-4 (L109) 일치.

#### ✅ 확인됨 — 오픈웨이트 단일 교훈 (요청 항목 3)
- L66 "어떤 오픈웨이트 모델이든, 구조화된 하네스 안에서 raw chat보다 훨씬 잘한다" → §3-6 L120 / §5 L180 [커뮤: MindStudio 2026] 일치. (단일 교훈으로 약화·일반화 적절 — 점수 미인용으로 과장 위험 없음.)

#### ✅ 확인됨 — L54 라운드 1 정정 반영
- 현재 본문: "2026년 중반 기준 `AGENTS.md`는 OpenAI Codex가 시작했지만 Cursor·Aider·Gemini CLI·VS Code 등 여러 도구가 같은 파일을 읽도록 채택해, 6만 개가 넘는 오픈소스 프로젝트가 쓰는 사실상의 업계 표준으로 자리잡았다."
- 시점("2026년 중반 기준") 명기 ✅ + 도구 예시·"6만 개" 수치 모두 웹 2차(공식 agents.md 2026-06-10)와 일치 ✅. 라운드 1의 강안을 정확히 반영. 통과.

#### 🕒 신선도 — 본문 시점 라벨 점검 (요청 항목 4 일부)
- L26 "2026년 6월 시점의 기능 구성" + 공식 문서 확인 권고 → ✅ 적절.
- L62 "2026년 4~5월 기준" / L70 "2026년 중반 기준" → ✅ 적절. 신선도 규율 잘 지켜짐.

#### ❌→해소 대상 1건 (BLOCKING) — 잔존 마커 (요청 항목 4 핵심)
- L62 끝 "(개별 모델의 SWE-Bench Pro 점수 같은 구체 수치는 변동성이 매우 높아, 본문에 박지 않는다. — 사실 확인 필요)"
- **점수표를 본문에 박지 않은 판단은 ✅ 옳다** (Kimi K2.6 58.6 등은 단일 출처·고변동, 본문 배제 정확).
- **그러나 "— 사실 확인 필요" 마커는 final에 남으면 안 된다 (HARD BLOCK).** 해소 방법: 마커 문구만 제거. 앞 서술("변동성이 매우 높아 본문에 박지 않는다")은 신선도 규율 모범 문장이니 유지.
- 정정안: "(개별 모델의 SWE-Bench Pro 점수 같은 구체 수치는 변동성이 매우 높아 본문에 박지 않는다.)"

**총평:** 6장 사실 트랙은 L62 마커 제거 단 1건만 남았다. 도구 귀속·오픈웨이트 교훈·시점 라벨·L54 모두 ✅. 마커 제거하면 6장 사실 트랙 전체 통과.

### 라운드 3 (2026-06-10) — 클로징 (원본 직접 재검증)

writer-3가 라운드 2 정정 2건 반영 보고. writer 자기보고에 의존하지 않고 06_draft.md 원본을 직접 읽어 재검증.

- **L54 (✅ 확정):** 원본 확인 — "실제로 2026년 중반 기준 `AGENTS.md`는 OpenAI Codex가 시작했지만 Cursor·Aider·Gemini CLI·VS Code 등 여러 도구가 같은 파일을 읽도록 채택해, 6만 개가 넘는 오픈소스 프로젝트가 쓰는 사실상의 업계 표준으로 자리잡았다." 권장(강) 정정안 그대로 반영. 시점·도구 예시·6만 수치 모두 웹 2차 일치. 통과.
- **L62 (✅ 확정):** 원본 확인 — "…점수표는 책의 수명을 갉아먹는다. 개별 모델의 SWE-Bench Pro 점수 같은 구체 수치는 변동성이 매우 높아, 일부러 본문에 박지 않는다." "— 사실 확인 필요" 마커 제거됨, 앞 서술 유지됨. 통과.
- **잔존 마커 0건 (✅ 독립 grep 검증):** `사실 확인 필요|미완성|리서치 공백|TODO|TK|placeholder` 패턴 grep 결과 미해소 마커 0건. (매치된 "채워보는"·"채워줄 수 없는"은 정상 산문 동사.)

**최종 판정: 6장 사실 트랙 전체 통과 (CLEARED).** 미해소 ❌/🕒 0건. 도구 기능 귀속(§3 일치)·오픈웨이트 교훈(§3-6/§5 일치)·신선도 라벨·L54·L62 모두 해소. 06_final.md 확정 가능.

> **참고(L62 마커 시점):** writer-3에 따르면 L62 "— 사실 확인 필요" 마커는 라운드 1 반영 시 이미 제거됐고, 라운드 2의 ❌ 지적은 내 라운드 2 읽기와 writer 편집이 시점상 엇갈린 것. 결과는 동일(현재 마커 0건). 라운드 2 ❌ 항목은 "지적 시점에 보이던 상태"로 로그에 남기되, 실제 해소는 라운드 1에 완료된 것으로 정정 기록.

### final 확정 검증 (2026-06-10) — 06_final.md 직접 점검

writer-3가 06_final.md로 확정. draft→final 회귀(마커 재유입·내용 변질) 점검 위해 final 파일 직접 grep.
- 마커 스캔(`사실 확인 필요|미완성|리서치 공백|TODO|TK|placeholder|작성 예정`): **0건.**
- L54 핵심 주장(AGENTS.md 2026년 중반 기준 업계 표준·6만 프로젝트): draft와 동일, 변질 없음.
- L62(SWE-Bench Pro 점수 본문 미수록 서술): draft와 동일, 마커 없음.
- L70 오픈웨이트 모델군(Qwen·DeepSeek·GLM·Kimi) "2026년 중반 기준" 라벨: 유지.

---

## 00장

### 라운드 1 (2026-06-10) — writer-1 요청

개념·비유(줌 레벨/동심원) 위주 장. 하드 수치·버전·인용·식별자 없음 — 검증 표면 거의 없음.

#### ✅ 확인됨 — 프레이밍 정합성
- 네 용어를 "줌 레벨이 다른 동심원"으로 설명 (L21·L30) → 01_reference.md §1-5 L59 "단 칼로 자르는 위계가 아니라 관점의 줌 레벨" 정전 입장과 일치.
- "context가 prompt를 대체했다"가 부정확하다는 입장 (L30·L32) → §4 논쟁 A 레퍼런스 판단(포함 관계, "죽음은 클릭베이트")과 일치.
- 잔존 마커 0건 (grep 확인).

**총평: 0장 통과 (CLEARED).** 검증 가능한 구체 사실 주장 0건. 사실 오류 없음.

---

## 01장

### 라운드 1 (2026-06-10) — writer-1 요청 (한 줄 기억 장치·포함 관계·표 전수 대조)

#### ✅ 확인됨 — 네 개의 한 줄 기억 장치 (글자 단위 대조, style-guardian 1차 교차 확인)
- L11 Prompt "한 번의 대화를 최적화한다." = §1-1 L17 글자 일치.
- L14 Context "전체 정보 환경을 최적화한다. 프롬프트는 그중 일부일 뿐." = §1-2 L23 글자 일치.
- L17 Harness "Agent = Model + Harness. 모델이 아니면 다 하네스다." = §1-3 L33 글자 일치.
- L20 Loop "한 번의 지시가 아니라, 반복하는 시스템을 설계한다." = §1-4 L45 글자 일치.

#### ✅ 확인됨 — 포함 관계
- L29 "Loop ⊃ Harness ⊃ Context ⊃ Prompt" = §1-5 L59 동일. "칼로 자르는 위계 아님·느슨함"(L45·L47) = §1-5 정전 단서와 일치.

#### ✅ 확인됨 — 추상화 계층·최적화 대상 표
- L55–60 표 4행(Prompt 단일 발화/한 번의 지시 · Context 추론 1회 전체 입력/윈도 전체 · Harness 에이전트 실행 1스텝/모델↔세계 실행층 · Loop 다스텝 자율 반복/반복 사이클 전체) = §1-5 L52–57 표와 행별 일치.
- (책 표는 레퍼런스 표의 "학술 뿌리" 열을 생략 — 1장 의도적 단순화, 사실 오류 아님. 학술 뿌리는 2~5장에서 다룸.)

- 잔존 마커 0건 (grep 확인).

**총평: 1장 통과 (CLEARED).** 기억 장치 4개·포함 관계·표 전부 레퍼런스와 일치. 미해소 ❌/🕒 0건.

---

## 02장

### 라운드 1 (2026-06-10) — writer-1 요청 (학술 귀속·연도·정의·Gwern 완충 검증)

#### ✅ 확인됨 — 학술 귀속·연도
- L29 "GPT-3(2020), 파인튜닝 없이 프롬프트 문구로 출력 품질 극적 변화 (Brown et al., 2020)" → §2-1 L67 / 참고문헌 16 (Brown 2020 NeurIPS, arXiv:2005.14165) 일치.
- L33 "CoT (Wei et al., 2022)" → §2-1 L68 / 참고문헌 17 (Wei 2022, arXiv:2201.11903) 일치.
- 본문에 arXiv ID 직접 노출 없음(저자·연도만) — 미래 YYMM 위조 위험 없음. 정상.

#### ✅ 확인됨 — Anthropic 정의 + 시점
- L39 "최적의 결과를 위해 LLM에게 줄 지시를 쓰고 조직하는 방법" + "컨텍스트 엔지니어링의 부분집합" + "2025-09-29 기준" → §1-1 L19 [웹: Anthropic 2025-09-29] 일치. 시점 명기 ✅.

#### ✅ 확인됨 (완충 처리 적절) — Gwern Branwen 귀속 [사전 등록 의심 항목]
- L27 "용어 자체는 흔히 Gwern Branwen이 GPT-3 입력을 작성하던 맥락에서 처음 쓴 것으로 널리 귀속된다. (다만 이 귀속은 2차 소스에 기댄 것이라, 누가 최초였는지를 단정하기는 조심스럽다.)"
- §2-1 L66 / §7 L230이 "**검증 필요**(1차 미확보)"로 표시한 항목. **책이 단정하지 않고 "널리 귀속된다" + "단정 조심" 이중 완충**으로 처리 → 정확한 처리. 사전 등록 의심 항목이었으나 본문이 이미 적절히 약화함. 추가 조치 불필요.
- (참고: 자기탐지 의심 인용·순환 인용 아님 — 외부 귀속을 명시적으로 약화한 정직한 처리.)

- 잔존 마커 0건 (grep 확인).

**총평: 2장 통과 (CLEARED).** 학술 귀속·연도·Anthropic 정의·시점 모두 일치, Gwern 귀속 완충 적절. 미해소 ❌/🕒 0건.

**06_final.md 검증 완료 — 회귀 없음. 6장 사실 트랙 최종 클로징.**

---

## 07장

### 라운드 1 (2026-06-10) — writer-3 요청 (책 fact-check 1순위, 휘발성 수치 집중)

7장은 사전 등록 의심 항목(설문·일화 비용·loop 귀속·Chroma)이 집중되는 장. 본문에 `(사실 확인 필요)` 의도적 유보 주석 6개 — 전부 판정 라벨로 해소(마커 제거 + 완충 유지/강화). 1개는 ⚠️ 정정(Chroma "단조" 과장).

#### 🕒 신선도 — L3 $47,000 사고
- 본문: "$47,000(2025년 11월, 4개 에이전트 11일, 예산 캡 없음), 단일 일화, 매체 재인용".
- §4 논쟁 B L136 + 신선도 원장 L266과 수치·정황 일치. "단일 일화" 라벨 정확. [커뮤] 단일 출처지만 책이 일화로 한정 → 적절.
- **마커 처리:** 본문 끝 "— 사실 확인 필요" 제거. 앞 완충("단일 일화·매체 재인용") 유지. (정정: "(2025년 11월에 보도된 이 사례는 단일 일화이며, 액수·정황은 매체 재인용이다.)")

#### ⚠️ 출처 약화 적절 — L11 설문 82%/95% [사전 등록 의심 항목]
- §4 논쟁 A L130 + §7 L233 "1차 미확인, 검증 필요". 책이 "2차 매체 재인용·1차 미확인" 완충 + L13에서 "수치가 사실이라 해도 죽음이 아니라 확장" 조건부 재약화 → 이중 완충. 적절.
- Critical 아님: 이 수치는 책 핵심 논지(포함 관계)를 떠받치지 않고 "헤드라인이 부풀린다"는 반론 소재. 약화로 충분, 웹 2차 불요.
- **마커 처리:** "— 사실 확인 필요" 제거, 완충 유지. (정정: "…했다는 인용도 돈다. 다만 이 설문 수치는 2차 매체 재인용으로 1차 보고서가 확인되지 않았다.")

#### ⚠️ 출처 약화 적절 — L21 $297 (Huntley 자체 주장)
- §4 논쟁 B L135 / web.md 자료 5 L53 "$50k → $297 (저자 자체 주장·단일 사례)". 본문 "$50,000짜리 계약을 $297에" = web.md 원문("$50k USD contract … $297 USD")과 일치. "저자 본인 단일 사례·일반화 불가" 완충 적절.
- **마커 처리:** "— 사실 확인 필요" 제거, 완충 유지.

#### 🕒 신선도 — L25 비용 배수 50x/100x/3.2x~100x+
- §4 논쟁 C L141("~50x, 자율 디버깅 100x+") + 논쟁 B L136("3.2x(5스텝)→100x+(200스텝)")과 일치. "2026년 커뮤니티 분석·작업 유형/도구마다 편차" 완충 적절.
- **마커 처리:** "— 사실 확인 필요" 제거, 완충 유지.

#### ❌→⚠️ 정정 필요 (BLOCKING) — L37 Chroma "18개 모델 전부 단조 감소" [Critical, 웹 2차 수행]
- 본문: "18개 프런티어 모델 전부에서 입력이 길어질수록 성능이 **단조롭게** 떨어졌다."
- **웹 2차(1차 출처 직접, trychroma.com/research/context-rot, 2026-06-10):** 18개 모델(GPT-4.1·Claude 4·Gemini 2.5·Qwen3 포함)은 ✅ 확인. **그러나 "non-uniform performance with increasing input length" — 일부는 급락(cliff), 일부는 점진 하락으로 패턴이 모델마다 다름. "단조(monotonic)·전부 동일"이 아니다.**
- 레퍼런스 §4 L149도 "F1 단조 감소"로 적었으나 이는 레퍼런스 자체의 과장. **1차 출처 우선 원칙상 책 표현이 1차보다 강함 → ⚠️ 정정.**
- [정정안] "18개 프런티어 모델 모두에서, 입력이 길어질수록 성능(F1)이 **전반적으로 떨어졌다**(하락 정도와 양상은 모델마다 달랐다)." — "단조롭게" 삭제, "전반적으로" + "양상은 모델마다 다름" 추가.
- **셔플>일관 반전(L39·L41)은 ✅ 1차 확인:** "Shuffling the haystack and removing local coherence consistently improves performance" — 책 주장과 정확 일치. 통과.
- **마커 처리:** "(모델 수·구체 수치는 2025년 기준 Chroma 발표 — 사실 확인 필요)"에서 "— 사실 확인 필요" 제거, "2025년 Chroma 연구 기준" 시점 표기로 전환.

#### ⚠️/🕒 약화 적절 — L47 loop engineering 용어 귀속 [사전 등록 의심 항목]
- §2-4 L85 + §7 L231 "Addy Osmani/Steinberger/Boris Cherny, 2026-06, 1차 미확보·검증 필요". **책이 인물 귀속을 본문에서 빼고 "2026년 6월 무렵 대중화 + 최초 귀속 1차 미확인·단정 불가"로 처리 → 가장 안전한 완충.** 인물명 미기재가 정확한 선택(자기탐지 의심 인용 회피).
- **마커 처리:** "— 사실 확인 필요" 제거, 완충 유지. (정정: "…갓 나온 단어다. 이 용어의 최초 귀속은 1차 출처가 확인되지 않아 단정하기 어렵다.")

#### ✅ 확인됨 — 학술 뿌리·논쟁 입장
- L51 ReAct(2022)·SWE-agent 인터페이스 학술 뿌리 → §1-3/§1-4/논문 트랙 일치.
- 논쟁 A 포함 관계(context ⊃ prompt)·논쟁 B/C 설계·샌드박스·논쟁 D 신조어 판별 → §4 레퍼런스 판단과 일치.

**총평: 7장 BLOCKING 1건(L37 Chroma "단조"→약화) + 마커 6개 제거 필요.** 나머지 휘발성 수치(설문·$297·$47k·배수·loop 귀속)는 완충이 이미 적절 — 마커만 제거하면 통과. **마커는 final에 절대 못 남긴다(하드블록).** Chroma "단조" 정정 + 마커 6개 제거하면 7장 통과.

### 라운드 2 (2026-06-10) — 클로징 (원본 직접 재검증)

writer-3가 라운드 1 정정 전부 반영 보고. self-report 의존 안 하고 07_draft.md 원본 직접 읽어 재검증.

- **L37 Chroma "단조" 정정 (✅ 확정):** 원본 확인 — "18개 모델 모두에서 입력이 길어질수록 성능이 **전반적으로 떨어졌다.** (2025년 Chroma 연구 기준이며, 하락 정도와 양상은 모델마다 달랐다 — 어떤 모델은 특정 길이에서 급락했고, 어떤 모델은 완만히 내려갔다.)" → "단조롭게" 삭제 + 1차 출처(non-uniform: cliff/완만)를 정확히 반영. 시점("2025년 Chroma 연구 기준") 표기. grep "단조" 0건 독립 확인. 통과.
- **마커 6개 제거 (✅ 확정):** L3 $47k / L11 설문 / L21 $297 / L25 배수 / L37 Chroma / L47 loop 귀속 — 6개 모두 "— 사실 확인 필요" 제거, 완충 서술 유지. grep(`사실 확인 필요|미완성|리서치 공백|TODO|placeholder`) 0건 독립 확인.
- **셔플>일관 반전(L39·L41):** 1차 확인분 그대로 유지. 정상.

**최종 판정: 7장 사실 트랙 전체 통과 (CLEARED).** 미해소 ❌/🕒 0건. Chroma 1차 정정·마커 6개·휘발성 수치 완충·학술 뿌리 모두 해소. 07_final.md 확정 가능.

---

## 08장

### 라운드 1 (2026-06-10) — writer-3 요청 (종합·회고 장, 개념 회고)

휘발성 수치 없음. 기억 장치 문구 + Anthropic 귀속 점검.

#### ✅ 확인됨 — 네 기억 장치 (1장과 동일, §1 일치)
- L7·L9·L11·L13 = §1-1~1-4 글자 일치(1장 라운드 1에서 글자 단위 확인 완료). mermaid 그림(L17–26)의 각 겹 문구도 동일.

#### ✅ 확인됨 — Anthropic 단순함 원칙 + Workflow vs Agent
- L35 "가장 단순한 해법부터, 필요할 때만 복잡도를 올려라" → web.md 자료 4 L42 (Anthropic "Building Effective Agents" 2024-12-19) "가장 단순한 해법을 먼저 찾고, 필요할 때만 복잡도를 올려라"와 일치.
- L33·L37 Workflow(미리 정의된 코드 경로) vs Agent(동적 판단) 구분 → web.md 자료 4 L42–43과 일치.
- **출처 정정(메모):** writer-3는 "§2-4 인접"으로 귀속했으나 정확한 1차는 **"Building Effective Agents"(2024-12-19, web.md 자료 4 / 참고문헌 4)**. 본문에 출처·시점을 박지 않고 개념만 서술 → 문제 없음(2024-12 안정·저휘발성, 종합 장에서 시점 생략 허용 범위). 로그 귀속만 정정.

- 잔존 마커 0건 (grep 확인). 본문 arXiv ID 노출 없음.

**총평: 8장 통과 (CLEARED).** 기억 장치·Anthropic 귀속 모두 일치. 미해소 ❌/🕒 0건. 08 final 확정 가능.

---

## 03장

### 라운드 1 (2026-06-10) — writer-2 요청 (영문 인용 글자 단위 + 타임라인 + 4대 전략)

#### ✅ 확인됨 — 영문 인용 4종 (글자 단위 대조)
- L3 Karpathy: "the delicate art and science of filling the context window with just the right information for the next step." = §1-2 L25 / web.md L13 **글자 일치.**
- L26 Lütke: "the art of providing all the context for the task to be plausibly solvable by the LLM." = §1-2 L26 / web.md L21 **글자 일치.**
- L28 Chase: "building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task." = §1-2 L27 / web.md L73 **글자 일치.**
- L20 Anthropic(한글역): "LLM 추론 중에 최적의 토큰(정보) 집합을 큐레이션하고 유지하는 전략의 집합" = §1-2 L28 영문("the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference")의 충실한 한글역. 의미 일치.

#### ✅ 확인됨 — 날짜·타임라인·"6일"
- Karpathy 2025-06-25(L4) / Lütke 2025-06-19(L40) / Chase 2025-06-23(L41) / Anthropic 2025-09-29(L20·43·67) → §2-2 / 신선도 원장 전부 일치. mermaid 타임라인 4개 날짜 일치.
- "6일 사이"(L33·47): 06-19(Lütke)~06-25(Karpathy) = 6일, Chase(06-23) 그 사이. 정확.

#### ✅ 확인됨 — 4대 전략 명칭
- Compaction / Structured Note-Taking / Sub-Agents / Just-in-Time (L69·73·77·81) = §5 L162 / web.md 자료 3 일치.

#### ✅ 확인됨 — Chroma 누설 점검 (7장 복선 분업)
- L61은 "7장에서 숫자로 회수" 예고만, 18개 모델·F1·셔플 정량 수치 일절 없음. 복선 분업 정확히 지켜짐.

- 잔존 마커 0건, arXiv 노출 없음.

**총평: 3장 통과 (CLEARED).** 영문 인용 4종 글자 일치·타임라인·전략 명칭 모두 정확. 미해소 ❌/🕒 0건.

---

## 04장

### 라운드 1 (2026-06-10) — writer-2 요청 (수치·정의·학술 귀속)

#### ✅ 확인됨 — SWE-bench pass@1 12.5% + 시점
- L5 "pass@1 12.5% (2024 기준)" → §1-5 각주 L56 / 신선도 원장 L263 / papers.md L49 일치. 시점 명기.

#### ✅ 확인됨 — HF 하네스 정의 + MindStudio 비유
- L19 "에이전트 내부의 실행층 — 모델을 호출하고, 모델의 툴 콜을 처리하고, 언제 멈출지 결정한다 (2026-05-25 기준)" → §1-3 L35 영문("The execution layer inside the agent: it calls the model, handles its tool calls, decides when to stop") 충실한 한글역, 날짜 일치.
- L19 "언어 모델과 실제 세계 사이의 모든 것…" → §1-3 L36 / web.md 자료 9("everything between the language model and the real world. The harness decides what that text can touch") 한글역 일치.
- L13 "Agent = Model + Harness" → §1-3 L33 [HF 글로서리] 일치.

#### ✅ 확인됨 — 학술 귀속·명칭
- L40 SWE-agent (Yang et al., 2024 NeurIPS) → §1-5 / 참고문헌 20 / papers.md 일치.
- L42 Toolformer (Schick et al., 2023 NeurIPS) → 참고문헌 19 / papers.md 일치.
- L40 ACI = Agent-Computer Interface → §1-3 L41 일치. L54 MCP = Model Context Protocol → 정확.

- 잔존 마커 0건, arXiv 노출 없음.

**총평: 4장 통과 (CLEARED).** 수치(12.5%/2024)·HF 정의·학술 귀속 모두 일치. 미해소 ❌/🕒 0건.

---

## 05장

### 라운드 1 (2026-06-10) — writer-2 요청 (정의 출처·5패턴·Ralph·완충)

#### ❌ 정정 필요 (BLOCKING) — L15 Anthropic 에이전트 정의 **시점 오류**
- 본문: Anthropic은 에이전트를 "LLM이 툴을 루프 안에서 자율적으로 사용하는 것"이라 했고 **(2024-12 기준)**.
- 영문 원문 "LLMs autonomously using tools in a loop"는 **web.md 자료 3 = Anthropic "Effective context engineering" (2025-09-29)** 의 문장이다. **2024-12가 아니다.**
- 2024-12("Building Effective Agents")는 Workflow vs Agent를 다룬 다른 글. 이 인용구는 그 글이 아니다.
- **writer-2 요청서의 귀속("…+ 2024-12 (Building Effective Agents)")부터 틀림** — 출처 혼동. 인용구 자체의 출처는 2025-09-29 글.
- [정정] "…자율적으로 사용하는 것"이라 했고 **(2025-09-29 기준)**. — 시점만 2024-12 → 2025-09(또는 2025-09-29)로 교체. 인용구·내용은 정확하니 그대로.

#### ✅ 확인됨 — Willison 루프 정의 + 시점
- L15 "목표를 달성하기 위해 툴을 루프 안에서 돌리는 것 (2025-09 기준)" → §1-4 L46 "Runs tools in a loop to achieve a goal." [Willison 2025-09-30] 일치. 시점 정확.

#### ✅ 확인됨 — Workflow vs Agent + Building Effective Agents 2024-12
- L23 "Building Effective Agents에서 워크플로 vs 에이전트 (2024-12 기준)" → web.md 자료 4 / 참고문헌 4 (2024-12-19) 일치. (L23은 출처·시점 정확 — L15만 오류.)
- L43 "가장 단순한 해법부터, 필요할 때만 복잡도를 올려라" → web.md 자료 4 L42 일치.

#### ✅ 확인됨 — 5패턴 명칭
- L49–55 표: prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer → web.md 자료 4 L42 일치. (루프 패턴 매핑은 레퍼런스 §5 패턴의 저자 해석 — 사실 주장 아님, 논지.)

#### ✅ 확인됨 — Ralph loop + ReAct
- L89·92 Ralph: 명령어 `while :; do cat PROMPT.md | claude-code; done` + Huntley 2025-07-14 → §3-7 L123 / 신선도 원장 / web.md 자료 5 명령어·날짜 일치.
- L17 ReAct (Yao 2022) → §1-4 L48 / 참고문헌 18 일치.

#### ✅ 확인됨 (완충 적절) — loop engineering 용어 [사전 등록 의심 항목]
- L17 "2026년에야 막 퍼지기 시작, 1차 출처 또렷하지 않음 → 작명자 따지기보다 벤더(Anthropic)+영향력자(Willison) 정의 병치." 인물명(Addy Osmani 등) 미기재. §2-4/§7 "검증 필요"를 가장 안전하게 처리. 정확.

- 잔존 마커 0건, arXiv 노출 없음.

**총평: 5장 BLOCKING 1건 — L15 Anthropic 정의 시점 2024-12 → 2025-09-29 정정.** 나머지(Willison·Workflow/Agent·5패턴·Ralph·ReAct·loop 완충) 전부 ✅. 시점 1개만 고치면 5장 통과.

### 라운드 2 (2026-06-10) — 클로징 (원본 직접 재검증)

writer-2가 L15 시점 정정 보고. self-report 의존 안 하고 05_draft.md 원본 직접 읽어 재검증.

- **L15 시점 정정 (✅ 확정):** 원본 확인 — "Anthropic은 에이전트를 \"LLM이 툴을 루프 안에서 자율적으로 사용하는 것\"이라 했고 **(2025-09-29 기준)**." 2024-12 → 2025-09-29 교체 완료. 인용구·내용 그대로. 출처 시점이 web.md 자료 3("Effective context engineering", 2025-09-29)과 일치.
- **L23 분리 유지 (✅ 확정):** "Building Effective Agents에서 … **(2024-12 기준)**" 그대로 유지. 두 Anthropic 소스가 각자 정확한 날짜로 분리됨(L15=2025-09-29 정의 인용, L23=2024-12 Workflow/Agent). 충돌 없음.
- **회귀 점검 (✅):** grep으로 L15에 "2024-12" 잔존 0건 확인. 마커 0건.

**최종 판정: 5장 사실 트랙 전체 통과 (CLEARED).** 미해소 ❌/🕒 0건. 05_final.md 확정 가능.

### 라운드 3 (2026-06-10) — L15 시점 1차 출처 직접 확정 (style-guardian 역방향 단서 검증)

style-guardian이 "L15 인용구가 agent 정의이므로 시점이 2025-09-29가 아니라 **2024-12(Building Effective Agents)** 일 가능성 — 정정 방향이 반대일 수 있다"는 단서 전달. 레퍼런스만으로는 두 Anthropic 문서가 모두 에이전트를 정의해 모호 → Critical(시점 정확성)이므로 **1차 출처 두 문서 직접 웹 확인.**

- **"Effective context engineering" (anthropic.com, 발행일 2025-09-29) — 직접 확인:** 정확히 이 문장 존재 → "we've gravitated towards a simple definition for agents: **LLMs autonomously using tools in a loop.**" (그 정의를 Simon Willison 2025-09-18에서 가져왔다고 명시.)
- **"Building Effective Agents" (anthropic.com, 발행일 2024-12-19) — 직접 확인:** 이 정확한 문구 **없음.** 다른 정의 사용("LLMs dynamically direct their own processes and tool usage" / "LLMs using tools based on environmental feedback in a loop").

**결론: 인용구 "LLMs autonomously using tools in a loop"의 출처는 2025-09-29 글이 맞다. 현재 본문 L15 "(2025-09-29 기준)" 표기가 정확하다.** style-guardian의 역방향 가설은 합리적 의심이었으나 1차 확인으로 기각. 라운드 1·2 판정 유지. (web.md 자료 3 기록과도 일치.)

---

## 05장 (v1.1.0 재저술)

### 준비 (2026-06-10) — 신규 대조 기준 숙지 + 검증 체크리스트 사전 등록

5장이 빈약하다는 독자 피드백으로 재저술 착수. 신규 1차 출처(`research/loop-engineering-deep.md`, addyosmani.com/blog/loop-engineering 2026-06-07 정밀 수집)와 갱신된 `01_reference.md §8` 숙지 완료. writer-5 재저술본 도착 전 사전 등록 — 도착 즉시 아래 체크리스트로 전수 검증한다.

**v1.0.0 → v1.1.0 변화 (대조 기준 이동):**
- 기존 v1.0.0(05_final.md 현재본)은 loop engineering 귀속을 **인물명 미기재**로 완충 처리했다(라운드 1 ✅ "가장 안전한 처리"). 1차 출처 미확보가 이유였다.
- v1.1.0은 1차 출처(Osmani 2026-06-07) 확보로 **실명 귀속 가능**해졌다. 단 "완충 해제 = 정확도 부담 증가" — 귀속 역할 구분이 새 핵심 검증 포인트.

**사전 등록 검증 체크리스트 (writer-5 도착 시 전수):**

1. **Osmani 정의·발행일·영문 인용 일치 (Critical)**
   - 정의 "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead." (deep.md §1-1 / §8-1) — 한글역 시 의미 보존.
   - 발행일 **2026-06-07** 정확. 시점 라벨 필수.
   - 영문 인용 시 철자 원문(paralell·dont) 처리는 에디터 몫이나, 인용 충실성 점검.

2. **계보 귀속 역할 구분 (Critical — v1.1.0 핵심)**
   - **Steinberger = 촉발** ("designing loops that prompt your agents", X @steipete / "Just Talk To It" 2025-10).
   - **Cherny = 증폭** ("My job is to write loops"). **반드시 "Osmani가 인용한" 형식 강제** — Cherny 1차 단독 출처 미확보(deep.md §7 / §2-2). Cherny를 직접 인용처럼 단정하면 ⚠️.
   - **Osmani = 명명** (명사구 "loop engineering" 분과화). Steinberger/Cherny를 "명명자"로 귀속하면 ❌.

3. **별개 계보 혼재 금지 (⚠️ 트리거)**
   - Huntley Ralph(2025-07) = 구현 패턴 / Willison agentic loops(2025-09) = 기술 정의 / Schmid inner·outer(2026-02) = 구조 분류. **Osmani 글은 이 셋을 명시 인용하지 않음**(deep.md §1-6 음성 확인). "Osmani가 Ralph/Willison/Schmid를 인용·계승했다"는 식으로 합쳐 서술하면 ⚠️. "수렴 진화(별개 계보)"로만 병치 가능. Ralph는 "Loop Engineering의 가장 단순한 구현체"로는 연결 가능.

4. **도구 기능 현황 시점 라벨 (🕒 필수)**
   - Claude Code ralph-wiggum/ralph-loop 플러그인, Codex `/goal`(CLI 0.128.0~), Cursor Background Agents, GitHub Continuous AI, Gemini CLI — **전부 "2026-06 기준" 라벨 필수**(deep.md §4 / §8-7, 변동성 높음). 벤더 1차(§6 자료 10~14)로 대조, Critical 항목은 웹 2차.
   - Opus 4.5 "4h49m"·"14시간 device driver"·"$297"·"$47k"는 보도·일화 — 일반화 금지.

5. **비용 수치 영역 분리 (지적 대상)**
   - **$297·$47,000은 7장 영역**(7장 라운드 1에서 완충 처리·CLEARED). 5장에서 중복 상술하면 지적 — 5장은 "위험은 7장에서 사고와 함께" 예고(현 v1.0.0 L97 방식)가 정합적. 5장에서 액수를 다시 박으면 ⚠️/분업 위반.

6. **마커·식별자 회귀 (HARD BLOCK)**
   - `사실 확인 필요|미완성|리서치 공백|TODO|TK|placeholder|작성 예정` 0건.
   - 본문 arXiv ID 노출 시 미래 YYMM 위조 점검(현재 v1.0.0은 ID 노출 0). Osmani/Steinberger URL·날짜 의심 식별자는 웹 2차 에스컬레이션.

7. **기존 ✅ 항목 보존 회귀**
   - L15 Anthropic 정의 "(2025-09-29 기준)"(라운드 1~3 1차 확정) / Willison "(2025-09 기준)" / BEA "(2024-12 기준)" / 5패턴 명칭 / Ralph 명령어·Huntley 2025-07-14 / ReAct(Yao 2022) — 재저술본에서 회귀 없는지 점검.

**대기 상태:** writer-5 검증 요청 수신 대기. 도착 즉시 라운드 1 전수 검증 append.

### 사전 판정 (2026-06-10) — Steinberger 인용 "(2026 기준)" 라벨 단건 [writer-5 ACK 중 직접 질의, Critical → 웹 2차 수행]

writer-5가 6개 제약 사전 반영 ACK와 함께 단건 질의: Steinberger 인용 도입에 붙인 "(2026 기준)" 라벨이 적절한가. 인용 시점 정확성 = Critical → 1차 출처(Osmani 글) + X 원문 타임스탬프 웹 2차로 직접 확인.

#### 🕒→✅ 적절 (라벨 유지 권고) — Steinberger 인용 "(2026 기준)"
- **인용 문구 (✅ 1차 일치):** "you shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." — X @steipete status/2063697162748260627에서 verbatim 확인. Osmani 글(addyosmani.com/blog/loop-engineering, 2026-06-07)이 정확히 이 트윗을 링크. 단, 트윗 원문은 "Here's your **monthly reminder** that…"로 시작 — 즉 **매달 재게시되는 상시 입장**(evergreen repost)이다(deep.md §7 "재게시"·"monthly reminder" 일치).
- **날짜 앵커 (✅ 웹 2차 확인):** digg.com/ai/7ifyvmb9가 해당 X 게시물 타임스탬프를 **2026-06-07 11:58 AM**으로 보도. Osmani 글 발행일(2026-06-07)과 같은 날 — Osmani가 당일 트윗을 인용한 구조로 정합. 따라서 이 발언은 **2026년 발화가 맞다.**
- **판정:** "(2026 기준)" 라벨은 **적절. 유지 권고.** 근거 두 가지:
  1. "monthly reminder"라 정밀 일자(2026-06-07)로 못 박으면 오히려 *상시 입장을 일회성 일자로 과대 특정*하는 셈. **연(年) 수준 "(2026 기준)" 라벨이 정확한 altitude.**
  2. 책의 계보 프레임(촉발 2026 Steinberger → 증폭 Cherny → 명명 Osmani 2026-06-07)과 "2026" 앵커가 일관. Steinberger의 **다른** 글 "Just Talk To It"(2025-10, "I ship code I don't read")와 혼동만 피하면 됨 — writer-5는 이를 분리하고 있음(✅).
- **무라벨/다른 시점은 부적절:** 무라벨이면 신선도 규율(시점 명기) 위반. "2025-10"은 다른 출처("Just Talk To It")의 날짜라 이 인용엔 오귀속(❌이 될 것). 현행 "(2026 기준)"이 정답.

#### ⚠️ 추가 발견 (Cherny 귀속 — 사슬 1단 더 깊음, "Osmani가 인용한" 형식 재확인)
- 웹 2차로 Osmani 글 확인 중 발견: Osmani가 인용한 **Cherny 발언("My job is to write loops")의 출처는 Cherny 본인 1차 게시물이 아니라 Rohan Paul이 중계한 X 게시물**(status/2063289804708835412)이다. 즉 사슬이 Cherny → (Rohan Paul 중계) → Osmani 인용 → 책으로, 1차에서 **두 단계** 떨어져 있다.
- **함의:** "Osmani가 인용한 형태로 옮기면" 도입(writer-5가 이미 채택)이 **필수일 뿐 아니라 정확.** Cherny를 직접 1차 인용처럼 단정하면 ⚠️가 아니라 사실상 오귀속에 가까움. writer-5의 현 처리가 정답 — 그대로 유지.
- "head of Claude Code at Anthropic" 소개(deep.md §1-2)도 Osmani 글과 일치 (✅).

**총평: Steinberger "(2026 기준)" 유지 권고(🕒→✅). Cherny는 "Osmani가 인용한" 형식 필수 재확인(웹 2차로 사슬 1단 더 깊음 발견).** 재저술본 도착 시 라운드 1 전수 검증에서 본문 실제 반영 확인.

**대기 상태(갱신):** writer-5 style 합의 후 재저술본 수신 대기. 도착 즉시 라운드 1 전수 검증 append.

### 라운드 1 (2026-06-10) — writer-5 재저술본 전수 검증 (style 합의 후 05_draft.md, 9,457자)

style-guardian 합의 종결분 도착. 사전 등록 7개 체크리스트 + writer-5 제시 9개 사실 주장 전수 대조. **영문 verbatim 인용 4종은 deep.md와 글자 단위 대조**, 한글역 인용은 deep.md 원문과 의미 충실성 대조, 귀속·날짜·계보 정밀 점검.

#### ✅ 확인됨 — 영문 verbatim 인용 4종 (글자 단위 대조, deep.md 일치)
- **L17 Osmani 정의:** "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead." = deep.md L18 **글자 일치.**
- **L35 Schmid:** "The loop is hardcoded. What the model does inside the loop is not." = deep.md L117 **글자 일치.** 한글역(L36) 충실.
- **L110 Osmani 검증:** "Verification is still on you. A loop running unattended is also a loop making mistakes unattended." = deep.md L134의 두 문장 정확 결합. **글자 일치.**
- **L178 Osmani 클로징:** "Cherny's point isn't that the work got easier. It's that the leverage point moved. Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go." = deep.md L76 **글자 일치.**

#### ✅ 확인됨 — 계보 귀속 역할 구분 (v1.1.0 핵심, Critical)
- **L23 Steinberger(촉발):** 산문 패러프레이즈 "이제 코딩 에이전트에게 프롬프트하지 말고, 에이전트에게 프롬프트를 넣어줄 루프를 설계하라" = deep.md L37("You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents") 충실 한글역. 역할 "불을 댕겼다"(촉발) 정확. **"(2026 기준)" 라벨 = 사전 판정에서 웹 2차로 적절 확정**(X @steipete 2026-06-07 타임스탬프, "monthly reminder" 상시 입장 → 연 수준 라벨이 정확).
- **L23 Cherny(증폭):** **"Osmani가 인용한 그의 말은" 형식 정확 채택** — 사전 판정에서 발견한 사슬(Cherny→Rohan Paul 중계→Osmani 인용)에 비춰 필수+정확. 한글역 "나는 더 이상 Claude에게 직접 프롬프트하지 않는다, 내 일은 루프를 쓰는 것이다" = deep.md L41 충실. "Anthropic에서 Claude Code를 책임지는" = "head of Claude Code at Anthropic" 일치.
- **L25 명명(Osmani) + 3단 패턴:** "촉발(Steinberger) → 증폭(Cherny) → 명명(Osmani)" = deep.md L44 명령 그대로. context engineering 동형(Lütke 촉발→Karpathy 대중화→Anthropic 공식화)도 deep.md L44와 일치. **명명자를 Steinberger/Cherny로 돌리는 오류 없음.**

#### ✅ 확인됨 — 별개 계보 혼재 금지 (⚠️ 트리거 회피)
- **L153 Ralph 화자 한정 헤지:** "적어도 내가 확인한 범위에서 Osmani의 글은 Huntley의 Ralph를 직접 인용하지는 않는다 … 수렴 진화" = deep.md L80(음성 확인) 정확 반영. Ralph는 "loop engineering의 가장 단순한 구현체"로만 연결(deep.md L102 허용). **합쳐 서술 없음.**
- **L101 Willison:** 종료-조건 절에서 "automated tests" 인용("이 모든 것에 공통으로 흐르는 주제는 자동화된 테스트" = deep.md L128 "A common theme in all of these is automated tests") + "(2025-09 기준)"으로만 등장. **Osmani 계보로 묶지 않음.**
- **L31–33 Schmid:** inner/outer를 "Philipp Schmid는 이를 …로 갈랐다 (2026-02-20 기준)"로 **독립 분류**로 제시. 정의 한글역 = deep.md L115–116 충실. **Osmani 인용으로 오귀속 없음.**

#### ✅ 확인됨 — 도구 현황 "2026-06 기준" 라벨 (🕒 해소)
- L159 소절 도입에 "2026-06 기준" + "이 영역은 빠르게 바뀌니 공식 문서를 함께 확인하자" 안전 문구 ✅.
- L99 completion promise(Ralph 플러그인 기본, deep.md L126/163) "(2026-06 기준)" / L161 ralph-wiggum Stop hook(deep.md L163–166) / Codex `/goal` "계획-실행-관찰-재계획-다시 실행"(deep.md L173) / Cursor 평가 인용 "토큰 예산을 걸고 수십 분간 무인으로 돌리도록 설계된 것은 아니다"(deep.md L183) / GitHub Continuous AI human-on-the-loop(deep.md L186–188) — 전부 1차 대조 일치. **휘발성 일화(Opus 4.5 4h49m·14시간 device driver) 미노출 = 적절(deep.md §7 주의 준수).**

#### ✅ 확인됨 — 기타 사실 주장
- **L19 Osmani 루프 정의:** "목적(purpose)을 정해두면 AI가 완료될 때까지 반복하는 재귀적 목표" = deep.md L22("recursive goal where you define a purpose and the AI iterates until complete") 충실. "(2026-06 기준)".
- **L100 max-iterations "1차 안전장치":** "공식 권고" = Anthropic ralph-wiggum 플러그인 문서 가이드("Always rely on `--max-iterations` as your primary safety mechanism", deep.md L127/166). 벤더 1차 문서 근거라 "공식 권고" 표현 정확.
- **L113 verifier 서브에이전트:** boolean 판정→실패 시 replanning + Osmani "하나가 아이디어를 내면 다른 하나가 검사" = deep.md L136 충실.
- **L123 이해 부채:** "루프가 네가 쓰지 않은 코드를 빨리 출하할수록…간극은 커진다" = deep.md L69 충실 한글역.
- **L125 인지적 항복:** "의견을 갖기를 멈추고 그냥 주는 대로 받아 삼키고" + "판단을 갖고 할 때는 치료약…생각하기를 피하려고 할 때는 가속 페달" = deep.md L72 충실. (이름 출처 표기 L119 "뒤 둘은 Osmani 원어, 첫째는 책이 붙인 이름" = 정직한 처리 ✅.)
- **L27 ReAct:** "추론과 행동을 교차하는 루프"(reason → act → observe → repeat) = 레퍼런스 §1-4 L48(ReAct=reason+act 교차, Yao 2022) 일치. 학술 사이클이라 reason 선두 순서 정확(루프 엔지니어링 기억 장치 act→observe→reason→repeat과 의도적 구분, 오류 아님).
- **L57 BEA(2024-12) + 5패턴:** "Building Effective Agents … (2024-12 기준)" 정확. 5패턴 매핑표(L83–89)는 prompt chaining/routing/parallelization/orchestrator-workers/evaluator-optimizer = web.md 자료 4 일치(루프 매핑은 저자 해석, 사실 주장 아님).

#### ✅ 회귀·경계 점검
- **마커 0건** (`사실 확인 필요|미완성|리서치 공백|TODO|TK|placeholder|작성 예정|FIXME` grep) — final-차단 통과.
- **arXiv ID 본문 노출 0건** — 미래 YYMM 위조 위험 없음.
- **비용 수치($297/$47k/burger/배수) 0건** — 7장 분업 경계 정확 준수. L155 "그 비용과 위험은 7장에서 한 사고와 함께 정면으로 다룬다" 포인터만(중복 상술 없음). human-in vs on the loop 논쟁도 L91에서 "7장에서 정면으로" 예고만.
- **v1.0.0 ✅ 보존:** 구 L15 Anthropic agent 정의 "(2025-09-29)" 인용구는 재저술에서 제거되고 Osmani 정의로 대체 — 고아 날짜·잘못된 시점 없음. BEA "(2024-12 기준)"만 정확히 남음. (두 Anthropic 소스 혼동 위험 자체가 사라짐.)

**최종 판정: 5장(v1.1.0) 사실 트랙 전체 통과 (CLEARED). 미해소 ❌/🕒 0건.** 영문 인용 4종 글자 일치, 계보 역할 구분 정확(Cherny "Osmani가 인용한" 형식 준수), 별개 계보(Ralph·Willison·Schmid) 혼재 없음, 도구 현황 "2026-06 기준" 라벨, 비용 7장 경계 준수, 마커·식별자 회귀 0. 1차 출처 확보로 v1.0.0의 인물명 미기재 완충을 정확한 실명 귀속으로 승급 — 정확도 손실 없이 강화됨. 05_final.md 확정 가능.

> **웹 2차 수행분(사전 판정에서):** Steinberger X 타임스탬프(2026-06-07, digg 교차확인) + Osmani 글 직접 fetch로 Cherny 인용 사슬(Rohan Paul 중계) 확인.

### final 확정 검증 (2026-06-10) — 05_final.md 직접 점검 (draft→final 회귀)

writer-5가 05_final.md로 확정(draft 본문 + 상단 개정 주석 1줄, 라인 +1 시프트). self-report 의존 안 하고 final 파일 직접 읽어 회귀 점검.

- **본문 동일성 (✅ diff 독립 확인):** `diff <(draft) <(final 본문 L2~)` 결과 **byte 단위 동일.** 유일한 델타는 L1 개정 주석(`<!-- 개정: 2026-06-10 5장 전면 재저술 (v1.1.0) — … Osmani 1차 출처(2026-06-07) … style-guardian·fact-checker 합의 반영. -->`)뿐. 이 주석은 메타데이터(사실 주장 아님)이며 내용도 정확(Osmani 1차 2026-06-07·v1.1.0). draft→final 내용 변질 0.
- **마커 스캔 (✅):** `사실 확인 필요|미완성|리서치 공백|TODO|TK|placeholder|작성 예정|FIXME` → **0건.**
- **arXiv ID 노출 (✅):** 0건 (미래 YYMM 위조 위험 없음).
- **비용 수치 (✅):** `297|47,?000|47k|$50|burger|버거` → **0건. 7장 분업 경계 유지.**
- **날짜 라벨 (✅ 7개 보존):** L16 (2026-06-07)·L20 (2026-06)·L24 (2026)·L32 (2026-02-20)·L58 (2024-12)·L100 (2026-06)·L102 (2025-09) — 라운드 1 검증분 그대로. 시프트만 +1, 값·귀속 무변.
- **두 Critical 보존 (✅):** L24 Steinberger "(2026 기준)" + Cherny "Osmani가 인용한" 형식 — 내 판정대로 무수정 유지 확인.

**최종 판정: 5장(v1.1.0) final 확정 — 회귀 없음 (CLEARED). 미해소 ❌/🕒 0건.** 05_final.md = 검증된 draft 본문 + 개정 주석. EPUB 빌드 사실 측면 클리어. **5장 v1.1.0 사실 트랙 종결.**

---

**9개 챕터 전부 통과 (CLEARED). 미해소 ❌/🕒 0건.**

| 장 | 판정 | 라운드 | 핵심 |
|----|------|--------|------|
| 00 | ✅ CLEARED | 1 | 개념·비유, 검증 가능 주장 0건 |
| 01 | ✅ CLEARED | 1 | 기억 장치 4개·포함 관계·표 §1 글자 일치 |
| 02 | ✅ CLEARED | 1 | GPT-3/CoT/Anthropic 정의·Gwern 완충 적절 |
| 03 | ✅ CLEARED | 1 | 영문 인용 4종 글자 일치·타임라인·전략 명칭 |
| 04 | ✅ CLEARED | 1 | SWE-bench 12.5%(2024)·HF 정의·SWE-agent/Toolformer |
| 05 | ✅ CLEARED | v1.0.0:2 / v1.1.0:1 | v1.1.0 재저술 — Osmani 1차 귀속 승급(영문 4종 글자 일치·계보 역할·Cherny "Osmani 인용" 형식·별개 계보 비혼재·7장 경계) |
| 06 | ✅ CLEARED | 3 | AGENTS.md 표준 시점·도구 보강(웹 2차)·점수표 유보 |
| 07 | ✅ CLEARED | 2 | Chroma "단조"→비단조 정정(1차 우선)·마커 6개·휘발성 완충 |
| 08 | ✅ CLEARED | 1 | 기억 장치·Anthropic 단순함 원칙 귀속 |

**웹 2차 검증 수행:** 6장 AGENTS.md(공식 agents.md), 7장 Chroma Context Rot(trychroma.com 1차).
**1차 우선 원칙으로 레퍼런스 과장 정정:** 7장 Chroma "단조 감소" — 레퍼런스 §4 표현이 1차보다 강해 책을 1차에 맞춰 약화.
**사전 등록 의심 항목 처리:** Gwern 귀속(2장)·loop engineering 귀속(5·7장)·설문 82/95%(7장) — 전부 완충/인물명 미기재로 적절 처리, 자기탐지 의심 인용 없음.
**마커 final-차단:** 전 챕터 draft·final 마커 0건(style-guardian과 2중 게이트). arXiv 미래 YYMM 위조 0건(본문 ID 노출 없음).

---

## 통합본 (04_manuscript.md, 881줄) — 사실 회귀 패스 (2026-06-10)

team-lead 요청. editor 통합 원고 대상. 신규 삽입부(머리말·판권·에필로그·참고문헌) + 연결부 새 사실 주장 + 고위험 watchlist + 참고문헌 식별자 정합 + 마커 회귀 전수 점검.

### ❌→해소 회귀 1건 (BLOCKING) — 참고문헌 L877 Chroma "단조" 재유입
- editor가 참고문헌 요약을 작성하며 레퍼런스 §4의 과장 표현("F1 단조 감소")을 그대로 가져옴 → 본문 7장(L721, "전반적으로 떨어졌다 + 양상 모델마다 다름")과 모순되는 회귀. style-guardian이 예고한 고위험 지점 적중.
- **정정 완료:** L877 "18개 프런티어 모델 F1 단조 감소" → "18개 프런티어 모델에서 F1이 전반적으로 감소 — 단, 하락 양상은 모델마다 비균일, 셔플 건초더미 역설". 본문·1차 출처(trychroma.com non-uniform)와 일치.
- 재확인: grep "단조" 0건(전 원고).

### ✅ 신규 삽입부 — 새 사실 주장 회귀 없음
- 머리말(L32–57): 개념 서술만, 새 수치/날짜/인용 0. ✅
- 판권(L10–28): 식별자 urn:uuid·하네스 v1.8.0·판본 v1.0.0/2026-06-10 — 메타, 사실 주장 아님. ✅
- 에필로그(L831–845): SWE-bench·토큰비용·오픈웨이트 순위를 "낡는다"로만 언급, 구체 수치 0. loop "신조어" 서술 본문과 일관. ✅

### ✅ 참고문헌 식별자·날짜 정합 (editor 신규 작성부)
- 학술 5건 arXiv 전수: 2005.14165/2201.11903/2210.03629/2302.04761/2405.15793 — 전부 신선도 원장 일치, 미래 YYMM 0건. SWE-bench 12.5% 병기 정확.
- 벤더: BEA(2024-12)·ECE(2025-09-29) 두 Anthropic 문서 정확히 분리. HF Glossary 2026-05-25.
- 실무자: Lütke 06-19·Chase 06-23·Karpathy 06-25·Willison(Runs tools…/2025-09·11)·Huntley Ralph 07-14 — 날짜·영문 인용 일치.
- 커뮤니티(1차 미확인 묶음): Gwern/loop 귀속 완충 명시, 설문 82/95% 1차 미확인 명시, 비용 배수·$297/$47k 단일 사례·일반화 불가 명시, AGENTS.md 6만+/2026 중반 — 전부 적절(L877 제외).

### ✅ 고위험 watchlist 전수 — 회귀 없음
- Anthropic 2024-12 vs 2025-09-29: 본문 L256·299·346·490(ECE/에이전트 정의)·498(BEA) + 참고문헌 L863/864 전부 정합. 5장 L15 정정(2025-09-29) 통합본에 보존. 혼동 0.
- SWE-bench 12.5%/2024: 본문 L390·참고문헌 L859 일치.
- AGENTS.md 2026 중반/6만: 본문 L653·참고문헌 L881 일치.
- 마커: grep 0건.

**최종 판정: 통합본 사실 회귀 패스 — PASS (회귀 1건 발견·정정 완료).** 미해소 ❌/🕒 0건. Chroma 참고문헌 회귀 해소 후 전 원고 "단조" 0건. EPUB 빌드 사실 측면 클리어.

---

## 통합본 v1.1.0 재통합 (04_manuscript.md, 951줄) — 사실 회귀 패스 (2026-06-10)

editor 요청. 5장 v1.1.0 재저술 통합 후 장 간 사실 일관성(회귀) 검증. editor가 5장 계보(Osmani 1차)에 맞춰 7장 논쟁 D를 동기화함 — 그게 내가 watchlist에 올린 최우선 점검 지점. 5개 검증 포인트 전수 + 전역 회귀 스캔.

### ✅ 검증 포인트 1 — loop 귀속 5장↔7장 동기화 (핵심, 회귀 위험 1순위)
- **5장(L503·505):** "촉발(Steinberger) → 증폭(Cherny) → 명명(Osmani)" 계보 + context engineering 동형.
- **7장 논쟁 D(L797·799):** "loop engineering 명사구는 2026년 6월 Osmani가 못 박아 대중화" + "Steinberger가 촉발하고 Cherny가 증폭한 현상에 Osmani가 뒤늦게 이름을 붙인 것 … 촉발 → 증폭 → 명명".
- **판정:** 두 장 귀속 서술 **완전 일관.** 같은 사실을 같은 역할 구분으로 말함. **내가 watchlist에 경고한 "7장 v1.0.0 인물명 미기재·단정 불가 완충이 남아 5장 실명 귀속과 모순" 위험 = 해소됨.** editor가 7장을 1차 실명 귀속으로 정확히 동기화. 잔존 v1.0.0 loop 완충 0건(grep — L249 매치는 Gwern/prompt engineering 건으로 별개, 그건 1차 미확보라 완충 유지가 정확).

### ✅ 검증 포인트 2 — Cherny 귀속 3곳 완충 일관
- **5장(L503):** "Osmani가 인용한 그의 말은…" — 직접 1차 단정 아님.
- **참고문헌(L942):** "Osmani 글이 인용한 형태로 확보. 원 발언 1차 링크는 미확보로, 본문에서 'Osmani가 인용한 Cherny'로 표기."
- **7장(L799):** Cherny를 "증폭한" 역할로만 언급(직접 인용 없음) → 완충 불필요·일관.
- **판정:** 세 곳 모두 일관. 내가 사전 판정에서 확인한 사슬(Cherny→Rohan Paul 중계→Osmani)에 정확히 부합. ✅

### ✅ 검증 포인트 3 — 5장 7장 예고 ↔ 7장 수치 충돌 없음
- **5장(L635):** "그 비용과 위험은 7장에서 한 사고와 함께 정면으로 다룬다" — 정성적, **수치 0.**
- **7장(L753·771·773):** $47,000(11일·4 에이전트·예산 캡 없음·2025-11 보도·단일 일화 완충) / $297(저자 단일 사례 완충) 정량 회수. L773 "5장에서 배운 그대로(가드레일·검증·샌드박스)" 교차참조.
- **판정:** 충돌 없음. 5장은 예고만, 7장이 회수. **5장 본문(L481–660)에 비용 수치 0건 grep 확인 — 7장 분업 경계 유지.** 7장 수치는 직전 7장 라운드 1(CLEARED)에서 완충 검증 완료분 그대로.

### ✅ 검증 포인트 4 — 참고문헌 신규 항목 발행일·검색시점 (deep.md 대조)
- **Osmani(L940):** addyosmani.com/blog/loop-engineering, 2026-06-07 (검색 2026-06-10) = deep.md L219 일치. "1차 정전" 표기 적절.
- **Steinberger(L941):** "designing loops"(촉발)·"I ship code I don't read"("Just Talk To It") / 2025-10 / 2026 = deep.md L223·224 일치. 두 출처(트윗 2026·Just Talk To It 2025-10) 정확 분리. ("I ship code…"는 참고문헌에만, 7장 본문 직접 인용 아님 — 날짜 충돌 없음.)
- **Cherny(L942):** Osmani 경유·1차 미확보 명시, 2026 = deep.md L225/§7 일치.
- **Schmid(L943):** philschmid.de/inner-loop-vs-outer-loop, 2026-02-20 = deep.md L229 일치. "The loop is hardcoded…" 귀속 정확.
- **판정:** 신규 4항목 발행일·검색시점·URL 전부 deep.md 일치. L948 주석이 Gwern(1차 미확보 유지) vs loop(Osmani 1차 확정) 정확히 구분. ✅

### ✅ 검증 포인트 5 — inner/outer loop Schmid 귀속
- **5장(L511):** "Philipp Schmid는 이를 inner loop와 outer loop로 갈랐다 (2026-02-20 기준)" + 정의 한글역 + "The loop is hardcoded…"(L658 인근/L36 원문) = deep.md L114–117 일치. 날짜·출처 정확. ✅

### ✅ 전역 회귀 스캔
- **마커 0건** (`사실 확인 필요|미완성|리서치 공백|TODO|TK|placeholder|작성 예정|FIXME`).
- **arXiv ID 5건 전수(L921–925):** 2005.14165/2201.11903/2210.03629/2302.04761/2405.15793 — 전부 과거 YYMM, **미래 위조 0건.**
- **사이클 순서 일관:** loop 기억 장치는 전 원고 `act → observe → reason → repeat`(L149·493·647·827). ReAct 학술 원형만 `reason → act → observe → repeat`(L507) — 의도적 구분, 모순 아님. v1.0.0과 동일 순서(회귀 없음).
- **8장 회고(L903):** "loop engineering은 막 자리 잡는 중인 신조어" — 5·7장 "신조어이되 실재 분과" 입장과 일관. 충돌 없음.
- **1장(L148·195):** 기억 장치 "한 번의 지시가 아니라, 반복하는 시스템을 설계한다" 글자 일치 + "언제까지·어떤 조건에서 반복할까"(§1-5 일치). 5장과 정합.

**최종 판정: 통합본 v1.1.0 사실 회귀 패스 — GREEN (회귀 0건).** 미해소 ❌/🕒 0건. 5개 검증 포인트 전부 ✅, 전역 회귀 스캔 클린. **핵심:** editor의 7장 논쟁 D 동기화로 내가 경고한 5장↔7장 귀속 모순 위험이 정확히 해소됨 — 두 장이 같은 1차 계보를 같은 역할 구분으로 서술. 참고문헌 신규 4항목 deep.md 일치. EPUB 빌드 사실 측면 클리어.
