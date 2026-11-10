# 논문 리서치: 좋은 스펙을 어떻게 쓰는가

- 대상 책: 『SDD 가이드북』(tech-book, 슬러그 `sdd-guidebook`)
- 검색·확인 시점: 2026-11-10
- 확인 경로: arXiv API(메타·초록), Crossref API(DOI·발표처·피인용수), Semantic Scholar API(일부 초록·피인용수), 원문 PDF·arXiv HTML(본문 수치)
- 범위: 기준 보고서 `research/sdd-report.md` 6절(2026-11-09 검증)이 이미 다룬 SDD 연구 지형(SLUMP, 스펙 격차, SpecPath, TDFlow, TestSuiteBench, ClarifyGPT·SpecFix·ClarifyCodeBench·Orchid, 형식 명세 9편, 컨텍스트 파일 11편)은 **다시 조사하지 않았다**. 이 파일은 그 위에 "개발자가 스펙을 **어떻게 쓰면** 결과가 좋아지는가"라는 작성법 근거만 더한다. 기준 보고서 문헌은 `[기준 r번호]`로 가리킨다.

## 읽는 법

- **발표 상태**: `동료심사`(학회·저널 게재 또는 게재 확정 표기 확인) / `프리프린트`(arXiv만 확인) / `잡지`(편집 심사 매체).
- **확인 수준**: `본문`(원문에서 수치를 직접 읽음) / `HTML`(arXiv HTML 본문을 요약 도구로 읽음, 수치는 표 값) / `초록`(초록만 읽음) / `메타만`(서지 정보만 확인, 내용은 미열람).
- 피인용수는 조회한 API 이름과 함께 적는다. API마다 값이 다르다.
- 각 항목의 **작성 규칙**은 논문 결과에서 이 리서치가 끌어낸 실천 문장이다(추론). 논문 저자의 권고와 구분하려고 따로 적는다.

---

## 한눈에 보기: 다섯 영역의 작성 규칙

| 영역 | 작성 규칙(추론) | 대표 수치 | 근거 | 주의점 |
|---|---|---|---|---|
| (1) EARS | 요구 하나를 `[While 상태] [When 트리거] 시스템은 [응답]을 해야 한다` 틀에 넣고, 실패·이상 상황은 `If…then`으로 따로 쓴다 | 요구 36개 → 47개로 쪼개짐, 요구당 단어 36.9 → 25.6. 8개 결함 유형 중 5개가 사례에서 사라짐 | Mavin 2009 (동료심사, 본문) | 요구 36개 한 건의 사례 연구. 제작자 본인 평가. LLM·에이전트 대상 통제 실험은 찾지 못함 |
| (2) 모호성·명확화 | 에이전트에게 "모호하면 먼저 물어라"를 명시하고, 스펙 안의 서로 모순되는 문장을 사람이 먼저 지운다. 답할 정보는 기대 동작과 실패 양상 위주로 준다 | 명시 지시 없이는 모델이 "거의 묻지 않음". 상호작용 시 비상호작용 대비 최대 74% 향상(Ambig-SWE). ChatGPT는 결함 있는 문제의 14.21%에서만 질문(HumanEvalComm) | Ambig-SWE (ICLR 2026), HumanEvalComm (TOSEM 2025) | 대부분 벤치마크 과제. 모순(inconsistency)이 가장 덜 잡힘 |
| (3) 수용 기준·BDD | 사용자 스토리 한 줄이 아니라 상세 요구 설명에서 Given-When-Then을 뽑는다. 스토리는 한 기능만, 해결책 말고 문제를 쓴다 | 상세 요구만 준 입력이 고품질 시나리오, 스토리만 준 입력은 저품질(Rathnayake). QUS 13개 기준 중 자동 점검 5개로 1,023개 스토리의 56%에서 결함 1개 이상 | Lucassen 2016 (동료심사, 본문), Rathnayake 2026 (프리프린트) | GWT가 에이전트 구현 품질을 올린다는 직접 통제 실험은 찾지 못함 |
| (4) 상세도 | 입출력 형식·사전/사후조건·알고리즘 세부·예시를 적되, 규칙 수를 무작정 늘리지 않는다. "should" 대신 "must" | 테스트 통과로 이끈 프롬프트 수정의 57%가 알고리즘 세부, 44%가 입출력 형식(Midolo). 덜 정한 프롬프트는 모델·프롬프트 변경 시 회귀 확률 2배(Yang). 지시 500개에서 최고 모델 정확도 68%(IFScale) | Yang (Findings of ACL 2026), Midolo·IFScale (프리프린트) | 함수 수준 과제와 비코딩 지시 과제. 저장소 수준 재현은 없음 |
| (5) 계약·경량 형식 명세 | 핵심 모듈만 사전조건·사후조건·불변식으로 쓰고, 그 계약을 속성 기반 테스트나 실행 가능한 참조 모델로 검사한다 | AWS: TLA+를 대형 시스템 10개에 적용, 엔지니어가 2~3주에 학습, 35단계 오류 추적 발견. S3 ShardStore: 경량 형식 기법으로 16건이 운영 진입 전 차단 | Newcombe 2015 (잡지), Bornholt 2021 (동료심사) | 분산 시스템 핵심부 사례. LLM 에이전트와 결합한 일반 업무 코드 비용은 미측정 |

---

## (1) EARS: 다섯 문형과 모호성 감소 근거

### 논문 1: EARS (Easy Approach to Requirements Syntax)

- 저자·연도: Alistair Mavin, Philip Wilkinson, Adrian Harwood, Mark Novak (Rolls-Royce), 2009
- 발표처: 2009 17th IEEE International Requirements Engineering Conference (RE'09), pp. 317–322
- DOI: 10.1109/RE.2009.9
- 피인용수: 265 (Crossref, 2026-11-10)
- 발표 상태: 동료심사 / 확인 수준: 본문(6쪽 전체)
- 요약: 비전문가가 자유 서술로 쓴 이해관계자 요구는 모호함, 막연함, 복잡함, 누락, 중복, 장황함, 구현 서술, 검증 불가의 8가지 문제를 갖는다. 저자들은 작은 구조 규칙 집합으로 모든 자연어 요구를 다섯 틀 중 하나로 쓰게 했다. 항공기 엔진 제어 감항 규정(CS-E 50)에서 요구를 추출해 원문과 EARS 재작성본의 문제 수를 비교했다.
- 방법론 요약: 일반 문형은 `<선택적 사전조건> <선택적 트리거> the <system name> shall <system response>`이다. 절의 순서는 시간 논리를 따른다. 사전조건이 먼저 성립하고, 그다음 트리거가 참이어야 응답이 요구된다. 다섯 유형은 다음과 같다.

  | 유형 | 키워드 | 틀 | 논문 예시(요약) |
  |---|---|---|---|
  | 상시(Ubiquitous) | 없음 | The <시스템> shall <응답> | 제어 시스템은 엔진 과속을 막아야 한다 |
  | 이벤트(Event-driven) | When | WHEN <트리거> the <시스템> shall <응답> | 연속 점화가 명령되면 연속 점화를 켠다 |
  | 원치 않는 동작(Unwanted behaviour) | If … Then | IF <트리거>, THEN the <시스템> shall <응답> | 대기속도 결함 플래그가 서면 모델 추정 속도를 쓴다 |
  | 상태(State-driven) | While (During) | WHILE <상태> the <시스템> shall <응답> | 비행 중에는 연료 유량을 하한 위로 유지한다 |
  | 선택 기능(Optional feature) | Where | WHERE <기능 포함> the <시스템> shall <응답> | 과속 보호 기능이 있으면 출항 전 가용성을 시험한다 |
  | 복합(Complex) | 위 키워드 조합 | While …, when …, the <시스템> shall … | 지상에 있을 때 역추력 명령이 오면 전개를 허용한다 |

  저자들은 "원치 않는 동작"에 별도 문형을 준 이유를 이렇게 설명한다. 초기 요구에서 누락의 주된 출처가 장애·교란·오사용 처리이고, 별도 문형이 있으면 수명주기 내내 그 요구를 찾기 쉽다.
- 핵심 수치·결과:
  - 원문 요구 36개가 EARS 재작성 후 47개가 되었다(복합 요구를 원자 요구로 분리, 약 +31%). 요구당 평균 단어는 36.9 → 25.6(약 −31%) (Table 2).
  - 8개 기준 가운데 5개(복잡함, 누락, 중복, 구현 서술, 검증 불가)는 재작성본에서 문제가 0건이었다. 모호함, 막연함, 장황함은 크게 줄었지만 남았다 (Graph 1, 로그 척도. 원 수치는 공개하지 않음).
  - 남은 모호함의 원인으로 저자들은 추론으로만 이해된 사전조건이 명시되지 않은 어휘적 모호함, 상위 요구에 본래 있는 막연함, 조건절이 많은 긴 요구의 어색한 문장을 든다.
- 저자가 밝힌 한계: 원 요구 36개의 작은 표본, 안전 관련 상위 요구에 한정, 막연함 분류의 주관성. 누락이 "제거되었다"는 주장은 조심해야 한다고 저자 스스로 적었다. 원치 않는 동작 일부를 찾았을 뿐 다른 누락 요구를 잡았다는 증거는 없다는 것이다. 또 이 방법은 상위 이해관계자 요구에 가장 적합하다고 범위를 한정한다.
- 인용할 만한 문장:
  > "Against five of the criteria, the interpretations contain none of the problems" (p.321, §5)
- 작성 규칙(추론):
  1. 요구 한 문장에 트리거 하나만 둔다. 트리거가 둘이면 요구를 둘로 나눈다. 요구 수가 늘고 문장은 짧아지는 것이 정상이다.
  2. 정상 흐름마다 "이게 실패하면?"을 묻고 `If…then` 요구를 따로 쓴다. 이 문형이 누락을 드러내려고 만든 장치다.
  3. 머릿속에만 있는 전제(예: "로그인한 상태에서")를 `While` 절로 꺼낸다. 남은 모호함의 첫째 원인이 이것이었다.
  4. "어떻게 만들지"는 쓰지 않는다. 구현 서술은 EARS 재작성에서 사라진 결함 유형이다.
- 독자 전달 방식 제안: 같은 요구를 자유 서술 → EARS로 바꾸는 전후 비교 1건(예: 결제 실패 처리)과 "요구는 늘고 문장은 짧아진다"는 36→47, 36.9→25.6 수치를 함께 보여 준다. Kiro `requirements.md`와 cc-sdd가 이 문형을 쓴다는 연결은 기준 보고서 2.2절 [기준 r100]을 참조.

### 논문 2: Big Ears (The Return of "Easy Approach to Requirements Engineering")

- 저자·연도: Alistair Mavin, Philip Wilkinson, 2010
- 발표처: 2010 18th IEEE International Requirements Engineering Conference (RE'10)
- DOI: 10.1109/RE.2010.39
- 피인용수: 45 (Crossref), 72 (Semantic Scholar), 2026-11-10
- 발표 상태: 동료심사 / 확인 수준: **메타만** (IEEE 유료, 초록이 API에서 비공개 처리됨)
- 요약: 2009 논문의 후속으로 EARS를 더 넓은 요구 집합에 적용한 보고로 알려져 있다. 이번 조사에서는 본문을 열지 못했다. 검색 결과 요약에는 "EARS를 경직되게 적용하면 문제가 생긴다"는 취지가 보였지만 원문으로 확인하지 못했으므로 본문 인용에 쓰지 않는다.
- 작성 규칙: 없음(미확인).

### 논문 3: Listens Learned (8 Lessons Learned Applying EARS)

- 저자·연도: Alistair Mavin, Philip Wilkinson, Sarah Gregory, Eero Uusitalo, 2016
- 발표처: 2016 IEEE 24th International Requirements Engineering Conference (RE'16)
- DOI: 10.1109/RE.2016.38
- 피인용수: 29 (Crossref, Semantic Scholar 동일), 2026-11-10
- 발표 상태: 동료심사 / 확인 수준: **메타만**
- 요약: 여러 조직에 EARS를 적용하며 얻은 교훈 8가지를 정리한 실무 보고로 알려져 있다. 8개 교훈의 목록은 이번 조사에서 확인하지 못했다. Crossref는 저자명을 "Wilksinson"으로 오기했다.
- 작성 규칙: 없음(미확인). 책에서 "EARS 적용 교훈"을 인용하려면 원문 확인이 필요하다.

### 논문 4: An Empirical Investigation of Requirements Engineering and Testing Utilizing EARS Notation in PLC Programs

- 저자·연도: Mikael Ebrahimi Salari, Eduard Paul Enoiu, Wasif Afzal, Cristina Seceleanu, 2025
- 발표처: SN Computer Science, vol. 6 (2025-03-24 게재)
- DOI: 10.1007/s42979-025-03843-3
- 피인용수: 미조회
- 발표 상태: 동료심사(저널) / 확인 수준: 초록
- 요약: 참가자가 자연어 요구를 EARS로 옮기고, 그 EARS 요구로 IEC 61131-3 PLC 소프트웨어를 시험하는 실험이다. 참가자가 고른 EARS 문형 유형과 명세 단계의 어려움을 관찰하고, 산업 현장에서 EARS 기반 시험 결과를 보고한다.
- 핵심 수치·결과: 초록에 수치 없음. 참가자 수와 문형 분포는 본문을 열지 못해 미확인.
- 작성 규칙(추론): 사람이 EARS로 옮길 때 어떤 문형을 주로 고르는지가 연구 주제가 될 만큼 문형 선택은 자명하지 않다. 책에서는 "문형 고르기 결정표"를 제공하는 근거로만 가볍게 쓴다.

### EARS 영역 종합

- EARS의 효과 근거는 2009년 단일 사례(요구 36개)가 거의 전부다. 동료심사를 거쳤지만 제작자 본인의 평가이고 통제군이 없다.
- 2018년에 EARS 전용 국제 워크숍(1st International Workshop on EARS, IEEE)이 열렸다. 여기서 형식화 시도(Lucio & Iqbal, "Formalizing EARS – First Impressions", DOI 10.1109/EARS.2018.00009)와 확장 문법 CLEAR(Hall, DOI 10.1109/EARS.2018.00010)가 발표되었다. 두 논문은 메타만 확인했다.
- **EARS 문형이 LLM 코딩 에이전트의 출력 품질을 자유 서술보다 높인다는 통제 실험은 이번 조사에서 찾지 못했다.** EARS를 에이전트 스펙에 쓰는 근거는 (a) 2009 사례의 결함 감소, (b) 아래 (2)·(4) 영역에서 "결함(냄새)이 적고 조건이 명시된 요구가 정답률을 높인다"는 간접 근거의 결합이다. 책은 이 점을 숨기지 않아야 한다.

---

## (2) 요구의 모호성·불완전성과 명확화 질문

기준 보고서 6절이 ClarifyGPT, SpecFix, ClarifyCodeBench, Orchid를 다뤘다 [기준 r228, r250, r248, r249]. 여기서는 "어떤 결함을 모델이 놓치는가", "어떤 질문이 효과가 있는가", "스펙 결함을 얼마나 넣으면 정답률이 떨어지는가"를 더한다.

### 논문 5: HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent

- 저자·연도: Jie JW Wu, Fatemeh H. Fard, 2025
- 발표처: ACM Transactions on Software Engineering and Methodology (TOSEM), 2025
- DOI: 10.1145/3715109 / arXiv:2406.00215
- 피인용수: 미조회
- 발표 상태: 동료심사 / 확인 수준: HTML(앞쪽 100,000자, Table 3·4)
- 요약: HumanEval 164문제의 설명을 모순(inconsistency), 모호(ambiguity), 불완전(incompleteness) 세 유형으로 고쳐 762개 변형을 만들었다. 모델이 코드를 쓰기 전에 명확화 질문을 하는지(Communication Rate), 그 질문이 빠진 정보를 되찾는지(Good Question Rate)를 쟀다. 질문을 하도록 설계한 에이전트 Okanagan도 비교했다.
- 핵심 수치·결과:
  - 결함을 넣은 문제에서 ChatGPT(GPT-3.5)는 14.21%의 경우에만 질문했고, Pass@1은 원본 65.58% → 변형 31.34%로 떨어졌다.
  - 질문 에이전트 Okanagan(ChatGPT 기반)은 질문 비율 72.73%, Pass@1 31.34% → 39.62%(약 +8점).
  - 유형별로는 대부분의 모델이 **불완전**은 가장 잘 알아채고 **모순**은 가장 덜 알아챘다(예: ChatGPT 질문 비율 불완전 31.68%, 모호 5.84%, 모순 5.84%).
  - 원본(결함 없는) 문제에서는 Okanagan이 불필요한 질문을 해 성능이 오히려 낮았다.
- 주의점: GPT-4급 이후 모델은 평가하지 않았다. 논문 서론과 본문의 Okanagan 향상 수치가 서로 다르게 적혀 있다(본문 표 기준 +58%p, +38%p).
- 작성 규칙(추론):
  1. 모델은 스펙의 **자기모순**을 가장 못 잡는다. 사람이 스펙을 넘기기 전에 "두 문장이 같은 상황에 다른 결과를 요구하는가"만 따로 점검한다.
  2. 질문 단계는 결함이 있을 때 효과가 있고, 없을 때는 비용이다. 큰 변경에만 명확화 단계를 넣는 선택적 운용이 맞다.
- 독자 전달 방식 제안: "에이전트는 빈칸은 눈치채지만 모순은 못 본다"를 세 유형 표 하나로 보여 준다.

### 논문 6: Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering

- 저자·연도: Sanidhya Vijayvargiya, Xuhui Zhou, Akhila Yerukola, Maarten Sap, Graham Neubig, 2025(arXiv) / 2026(학회)
- 발표처: ICLR 2026 (arXiv 코멘트의 채택 표기 기준)
- arXiv ID: 2502.13069
- 피인용수: 미조회
- 발표 상태: 동료심사(채택 표기 확인) / 확인 수준: HTML
- 요약: SWE-Bench Verified 이슈에서 정보를 일부 숨긴 변형(Ambig-SWE)을 만들어, 에이전트가 (a) 정보 부족을 알아채는지, (b) 표적 질문을 하는지, (c) 답을 받아 성능을 올리는지를 단계별로 쟀다. 모의 사용자가 숨긴 정보를 쥐고 답한다.
- 핵심 수치·결과:
  - 명시적 지시가 없으면 모델은 심하게 덜 정해진 입력에서도 "거의 묻지 않았다".
  - 정보 부족 감지 정확도는 Claude Sonnet 4가 0.74~0.89로 가장 높았고, 다른 모델은 0.47~0.84 범위였다. Llama 3.1 70B는 너무 자주 물어 거짓 양성률이 최대 0.95였다.
  - 상호작용을 허용하면 비상호작용 대비 최대 74% 향상. Claude Sonnet 4는 완전한 이슈를 받았을 때 성능의 약 89%를 상호작용으로 회복했다.
  - 저자 표현으로 가장 효과적인 질문은 구체적이고 실행 가능하며 과제 수준인 질문이었다. 코드에서 스스로 찾을 수 있는 구현 세부를 묻는 질문은 가치가 적었다.
  - 사용자가 준 정보 중 "정보형"(기대 동작, 오류의 성격)은 거의 모든 상호작용에 들어 있었다. "위치형"(파일 경로)은 약한 모델에 도움이 되고(예: Claude Sonnet 3.5 해결률 37.94% → 59.52%), 강한 모델에는 이득이 작거나 오히려 떨어졌다(Qwen 3 Coder 55.43% → 52.38%).
  - 상호작용은 효과를 올렸지만 효율은 올리지 않았다(Claude Sonnet 4 평균 단계 65 → 75).
- 인용할 만한 문장:
  > "The most effective questions are specific, actionable, and task-level." (§RQ2 분석)
- 작성 규칙(추론):
  1. 스펙이나 에이전트 지시에 "불분명하면 구현 전에 질문하라"를 명시한다. 기본값으로는 묻지 않는다.
  2. 스펙에는 기대 동작과 실패 양상(무엇이 틀리면 안 되는가)을 먼저 쓴다. 파일 위치는 에이전트가 스스로 찾을 수 있으면 생략해도 된다.
  3. 에이전트가 던진 질문이 구현 세부(변수명, 내부 함수)라면 스펙 질문이 아니다. 과제 수준 질문에만 답을 보강한다.
- 독자 전달 방식 제안: "에이전트는 추측하는 쪽을 기본값으로 갖는다"를 기준 보고서의 UnderSpecBench(행동 경계 위반 55.8~67.8%) [기준 r245]와 함께 묶어 설명한다.

### 논문 7: Rapid quality assurance with Requirements Smells

- 저자·연도: Henning Femmer, Daniel Méndez Fernández, Stefan Wagner, Sebastian Eder, 2017(권호)
- 발표처: Journal of Systems and Software, vol. 123, pp. 190–213
- DOI: 10.1016/j.jss.2016.02.047 / arXiv:1611.08847
- 피인용수: 141 (Crossref), 208 (Semantic Scholar), 2026-11-10
- 발표 상태: 동료심사 / 확인 수준: 초록 + 목차(본문 텍스트 추출 실패)
- 요약: 코드 냄새 개념을 요구공학으로 옮겨 "요구 냄새"를 정의하고 탐지 도구 Smella를 만들었다. 냄새는 ISO/IEC/IEEE 29148의 언어 기준에 근거한다(§3.2 제목 기준). 산업 3곳과 대학 1곳 사례에 적용했다.
- 핵심 수치·결과: 자동 탐지 평균 정밀도 59%, 평균 재현율 82%(사례별 편차 큼). 실무 환경에서 품질 결함 인식이 높아지는 효과가 관찰되었고, 일부 냄새는 서로 구별이 잘 되지 않았다.
- 작성 규칙(추론): 요구 냄새 점검은 리뷰를 대체하지 않고 보충한다. 정밀도 59%라면 경고 10개 중 4개는 오탐이다. 린트처럼 빠르게 돌리고 사람이 거른다.
- 독자 전달 방식 제안: "코드에 린트가 있듯 스펙에도 린트가 있다"는 비유. 냄새 목록 자체는 원문 확인 뒤 싣는다.

### 논문 8: On the Impact of Requirement Smells in LLM-Based Code Generation

- 저자·연도: Hugo Villamizar, Jannik Fischbach, Mert Şahin, Julian Frattini, Alessio Ferrari, Alexander Korn 외, 2026
- 발표처: PROFES 2026(27th International Conference on Product-Focused Software Process Improvement) 발표 채택 표기
- arXiv ID: 2609.29208
- 피인용수: 미조회
- 발표 상태: 동료심사(채택 표기) / 확인 수준: HTML
- 요약: 명확한 요구에 의미(모호함), 구문(수동태, 부정), 어휘(약한 동사) 냄새를 단계적으로 주입하고 LLM이 만든 코드의 기능 정확도를 시스템 테스트로 쟀다. 앞선 연구는 같은 데이터로 요구-코드 추적성에 대한 냄새 영향을 봤다(Vogelsang 외, ICSE-NIER 2025, pp. 51–55, DOI 10.1109/ICSE-NIER66352.2025.00016, 메타만 확인).
- 방법론 요약: 게임 4개(Dice 25개, Arkanoid 19개, Snake 14개, Scopa 16개, 총 요구 74개), GPT-4o와 DeepSeek-V3, temperature 0, 설정당 5회. 냄새 밀도 5단계.
- 핵심 수치·결과:
  - 냄새 밀도가 높아지면 평균 정확도가 대체로 낮아졌다. 예: Snake에서 DeepSeek-V3 64.3% → 52.9%, Scopa에서 GPT-4o 72.5% → 57.5%. 그러나 Arkanoid는 모든 단계에서 88~90% 이상을 유지했고, Scopa의 DeepSeek-V3는 오히려 81.3% → 90.0%였다.
  - 음의 순위 상관이 일부 관찰되었지만(예: ρ = −0.97, p = 0.033) Bonferroni 보정 뒤 유의한 결과는 없었다.
  - 냄새 범주(의미·구문·어휘) 사이에 효과 차이가 없었다.
  - 냄새가 없는 요구도 결함 코드를 만들었다.
  - 추적성 과제에서는 냄새 영향이 작았지만 코드 생성은 더 민감해 보였다(저자들은 탐색적 비교라고 명시).
- 작성 규칙(추론): 특정 냄새 하나를 고치는 것보다 요구 문장 전체의 결함 밀도를 낮추는 것이 방향이다. 다만 깨끗한 요구가 정답을 보장하지 않으므로, 요구 정리와 실행 가능한 테스트를 함께 둔다.
- 주의점: 짧은 게임 4개, 모델 2개, 인공 주입 냄새, 통계적 검정력 낮음.

### 논문 9: LLM-based Agents for Automated Bug Fixing: How Far Are We?

- 저자·연도: Xiangxin Meng, Zexiong Ma, Pengfei Gao, Chao Peng, 2026(학회) / 2024(arXiv, 제목 "An Empirical Study on LLM-based Agents for Automated Bug Fixing")
- 발표처: Proceedings of the 2026 IEEE/ACM 48th International Conference on Software Engineering (ICSE 2026)
- DOI: 10.1145/3744916.3773269 / arXiv:2411.10213
- 피인용수: 미조회
- 발표 상태: 동료심사 / 확인 수준: HTML(arXiv v2)
- 요약: SWE-bench Verified에서 수리 시스템 6개를 비교하고, 모든 시스템이 푼 이슈 181개와 아무도 못 푼 이슈 96개의 이슈 설명 품질을 Xia 외(Agentless)의 품질 척도로 비교했다.
- 핵심 수치·결과(평균 품질 점수, 못 푼 이슈 → 모두 푼 이슈):
  - 해결 방법 서술 0.656 → 1.276(약 1.95배). 저자는 이것을 해결 여부의 가장 중요한 요인으로 본다.
  - 위치 정보는 파일 1.052 → 1.326, 심볼 0.906 → 1.177, 줄 0.813 → 0.994(1.22~1.30배).
  - 재현 예시는 2.01 → 2.022로 거의 차이가 없었다.
- 주의점: 상관 비교이고, 해결 방법이 이슈에 적혀 있으면 정답 유출에 가깝다(Agentless 저자들도 SWE-bench Lite에서 정답 패치가 설명에 든 문제를 걸러 Lite-S를 만들었다, arXiv:2407.01489).
- 작성 규칙(추론): 버그 수정 스펙에는 "무엇이 틀렸는지"만이 아니라 "어떤 방향으로 고치길 원하는지"와 관련 심볼을 적는다. 재현 절차만 길게 쓰는 것은 효과가 작다.

---

## (3) 수용 기준, Given-When-Then, BDD, 테스트를 스펙으로

기준 보고서 6절이 TiCoder, Fakhoury 외(TSE 2024), TDFlow, TENET, WebApp1K, TestSuiteBench, Google 스펙 주도 테스트 생성을 다뤘다 [기준 r251, r19, r20, r21, r253, r22, r55]. 핵심 결론은 "사람이 쓴 테스트가 가장 검증된 실행 가능한 스펙"이다. 여기서는 그 앞 단계, 즉 **수용 기준 문장을 어떻게 쓰는가**를 더한다.

### 논문 10: Improving agile requirements: the Quality User Story framework and tool

- 저자·연도: Garm Lucassen, Fabiano Dalpiaz, Jan Martijn E. M. van der Werf, Sjaak Brinkkemper, 2016
- 발표처: Requirements Engineering, vol. 21, no. 3, pp. 383–403
- DOI: 10.1007/s00766-016-0250-x
- 피인용수: 224 (Crossref), 265 (Semantic Scholar), 2026-11-10
- 발표 상태: 동료심사 / 확인 수준: 본문(저자 원고 PDF, Table 1·4·5)
- 요약: 사용자 스토리 품질 기준 13개(QUS)를 Lindland의 구문·의미·화용 범주로 정리하고, 그중 자동 판정이 가능한 기준을 NLP 도구 AQUSA로 점검했다. 18개 조직의 스토리 1,023개로 평가했다.
- QUS 13개 기준(Table 1, 요약):

  | 범주 | 기준 | 뜻 | 단위 |
  |---|---|---|---|
  | 구문 | Well-formed | 최소한 역할과 수단(means)을 가진다 | 개별 |
  | 구문 | Atomic | 정확히 한 기능만 요구한다 | 개별 |
  | 구문 | Minimal | 역할, 수단, 목적(ends) 외의 내용이 없다 | 개별 |
  | 의미 | Conceptually sound | 수단은 기능, 목적은 이유를 말한다 | 개별 |
  | 의미 | Problem-oriented | 문제만 쓰고 해결책은 쓰지 않는다 | 개별 |
  | 의미 | Unambiguous | 여러 해석을 낳는 용어·추상을 피한다 | 개별 |
  | 의미 | Conflict-free | 다른 스토리와 모순되지 않는다 | 집합 |
  | 화용 | Full sentence | 완결된 문장이다 | 개별 |
  | 화용 | Estimatable | 계획·우선순위를 매기기 어려운 큰 덩어리가 아니다 | 개별 |
  | 화용 | Unique | 중복이 없다 | 집합 |
  | 화용 | Uniform | 같은 틀을 쓴다 | 집합 |
  | 화용 | Independent | 다른 스토리에 본질적으로 의존하지 않는다 | 집합 |
  | 화용 | Complete | 스토리 집합을 구현하면 빠진 단계 없이 기능이 완성된다 | 집합 |

- 핵심 수치·결과:
  - AQUSA v1이 점검한 5개 기준(Atomic, Minimal, Well-formed, Uniform, Unique)만으로도 스토리의 평균 56%에서 결함이 1개 이상 나왔다.
  - 전체 재현율·정밀도는 매크로 평균 92.1%·77.4%, 마이크로 평균 93.8%·72.2%. 기준별 정밀도는 Well-formed 42.31%에서 Unique 100%까지 차이가 컸다(Table 5).
  - 저자들은 NLP 요구 도구가 쓸모 있으려면 재현율 100%여야 한다는 Berry의 조건을 목표로 삼았고 아직 도달하지 못했다고 밝힌다.
- 작성 규칙(추론):
  1. 스토리 하나에 기능 하나(Atomic). 에이전트 작업 단위를 나눌 때도 같은 기준을 쓴다.
  2. 스토리에는 해결책을 쓰지 않는다(Problem-oriented). 해결책은 설계 문서로 보낸다. EARS의 "구현 서술 금지"와 같은 방향이다.
  3. 스토리 집합 단위 기준(모순 없음, 독립, 완결)은 도구가 거의 못 잡는다. 사람이 집합 전체를 한 번 읽어야 한다.
- 독자 전달 방식 제안: 13개 기준을 "한 장짜리 스토리 점검표"로 옮겨 싣는다. 단, 원문 기준명은 영문 그대로 병기한다.

### 논문 11: Behaviour Driven Development Scenario Generation with Large Language Models

- 저자·연도: Amila Rathnayake, Mojtaba Shahin, Golnoush Abaei, 2026
- 발표처: arXiv 프리프린트
- arXiv ID: 2603.04729
- 피인용수: 미조회
- 발표 상태: 프리프린트 / 확인 수준: 초록
- 요약: 상용 제품 4개에서 모은 사용자 스토리·요구 설명·BDD 시나리오 500건으로 GPT-4, Claude 3, Gemini의 시나리오 생성 품질을 텍스트 유사도, LLM 평가자, 전문가 평가로 비교했다.
- 핵심 수치·결과(초록 기준):
  - 상세한 요구 설명만 준 입력은 고품질 시나리오를, 사용자 스토리만 준 입력은 저품질 시나리오를 만들었다.
  - 프롬프트 기법의 효과는 모델마다 달랐다(GPT-4는 제로샷, Claude 3는 사고 사슬, Gemini는 퓨샷이 최선).
  - LLM 평가자(특히 DeepSeek)가 텍스트 유사도 지표보다 사람 판단과 더 강하게 상관했다.
- 작성 규칙(추론): "As a user, I want…" 한 줄로는 좋은 Given-When-Then이 나오지 않는다. 스토리 아래에 조건·예외·경계값을 적은 요구 설명을 붙인 뒤 시나리오를 뽑는다.
- 주의점: 시나리오 품질을 쟀고, 그 시나리오로 에이전트가 만든 코드 품질은 재지 않았다.

### 논문 12: Epic-Organized vs. Requirement-Aligned Gherkin: An Empirical Evaluation of LLM-Based Acceptance Criteria Generation

- 저자·연도: Shahbaz Siddeeq, Mateen Abbasi, Jussi Rasku, Zheying Zhang, François Christophe, Tommi Mikkonen, 2026
- 발표처: SEET 2026(International Conference on Software Engineering of Emerging Technologies) 채택, Communications in Computer and Information Science vol. 3126, pp. 85–100, Springer(2027 권호 표기)
- arXiv ID: 2607.01980
- 피인용수: 미조회
- 발표 상태: 동료심사(채택 표기) / 확인 수준: 초록
- 요약: PURE 데이터셋 요구 문서 4개(요구 107개)로, 에픽 단위로 묶어 Gherkin을 생성하는 파이프라인과 요구 하나당 시나리오를 만드는 단순 LLM 기준선을 비교했다.
- 핵심 수치·결과: 의미 기반 요구 커버리지는 94.3% 대 92.9%로 비슷했다. 연구자 4명의 블라인드 평가에서 에픽 단위 생성이 정확성 4.61 대 4.14, 실행 가능성 4.61 대 4.07, 완결성 4.31 대 3.50으로 높았다. TF-IDF 커버리지는 에픽 단위 출력에서 낮게 나와, 어휘 지표가 상위 추상의 시나리오를 놓칠 수 있음을 보였다.
- 작성 규칙(추론): 수용 기준을 요구 문장마다 기계적으로 하나씩 만들기보다, 관련 요구를 기능(에픽) 단위로 묶어 시나리오를 쓰면 완결성이 높게 평가된다.
- 주의점: 평가자 4명이 연구자, 저자 자신의 파이프라인과 비교.

### 논문 13: From Law to Gherkin: A Human-Centred Quasi-Experiment on the Quality of LLM-Generated Behavioural Specifications from Food-Safety Regulations

- 저자·연도: Shabnam Hassani, Mehrdad Sabetzadeh, Daniel Amyot, 2025
- 발표처: Information and Software Technology 게재 채택(arXiv 코멘트 기준)
- arXiv ID: 2508.20744
- 피인용수: 미조회
- 발표 상태: 동료심사(채택 표기) / 확인 수준: 초록
- 요약: 식품 안전 규정에서 Claude와 Llama가 만든 Gherkin 명세 60개를 참가자 10명이 다섯 기준으로 평가했다(평가 120건).
- 핵심 수치·결과: 상위 두 등급 비율이 관련성 95%, 명확성 100%, 완결성 94.2%, 단일성 93.4%, 시간 절약 91.7%. 참가자 간·모델 간 통계적 차이는 없었다. 정성 의견에서는 가끔의 누락, 환각, 의도 혼합이 지적되었다.
- 작성 규칙(추론): LLM이 초안으로 뽑은 Given-When-Then은 읽기에는 좋아 보여도 누락과 환각이 섞인다. 시나리오마다 "의도 하나"인지(단일성)를 사람이 확인한다.

### 논문 14: Comprehensive Evaluation and Insights Into the Use of Large Language Models in the Automation of Behavior-Driven Development Acceptance Test Formulation

- 저자·연도: Shanthi Karpurapu, Sravanthy Myneni, Unnati Nettur, Likhit Sagar Gajja, Dave Burke, Tom Stiehm, 2024
- 발표처: IEEE Access, vol. 12, pp. 58715–58721
- DOI: 10.1109/ACCESS.2024.3391815 / arXiv:2403.14965
- 피인용수: 35 (Crossref, 2026-11-10)
- 발표 상태: 동료심사 / 확인 수준: 초록
- 요약: GPT-3.5, GPT-4, Llama-2-13B, PaLM-2로 BDD 수용 테스트를 제로샷·퓨샷 생성하고 구문 오류와 검증 정확도를 비교했다. GPT-3.5와 GPT-4가 오류 없는 테스트를 만들었고, 퓨샷이 더 정확했다.
- 작성 규칙(추론): 팀의 기존 Gherkin 예시 몇 개를 스펙 템플릿에 넣으면 형식 오류가 준다. 초록에 효과 크기 수치는 없다.

### 논문 15: Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development (AutoGlue)

- 저자·연도: Xinyu Shi, Zhou Yang, An Ran Chen, 2026
- 발표처: arXiv 프리프린트
- arXiv ID: 2607.19703
- 피인용수: 미조회
- 발표 상태: 프리프린트 / 확인 수준: 초록
- 요약: Gherkin 단계를 프로젝트 코드에 잇는 글루 코드를 다중 에이전트로 생성했다. 오픈소스 Java 프로젝트 8개의 단계 1,307개로 평가했다.
- 핵심 수치·결과: 퓨샷 대비 API F1 +58.7%, CodeBLEU +43.7%. 단계의 46.1%에서 바로 쓸 수 있는 글루 코드를 만들었다. 단계의 의도를 시나리오 맥락에서 먼저 해석하는 구성 요소와 프로젝트 맥락 검색이 모두 기여했다(절제 실험).
- 작성 규칙(추론): Gherkin 시나리오를 실행 가능한 스펙으로 쓰려면 단계 문장이 프로젝트 어휘(도메인 용어, API 이름)와 맞아야 에이전트가 연결하기 쉽다. 기준 보고서의 "스펙-오라클 격차"(스펙에 없는 이름에 기대는 테스트는 80.6% 실패) [기준 r244]와 같은 방향이다.

### 수용 기준 영역 종합

- **Given-When-Then 형식이 에이전트 구현 품질을 자유 서술 수용 기준보다 올린다는 직접 통제 실험은 이번 조사에서 찾지 못했다.** 측정된 것은 (a) LLM이 만든 시나리오의 품질, (b) 시나리오를 코드에 잇는 일, (c) 사람이 쓴 테스트를 스펙으로 줄 때의 큰 이득(기준 보고서)이다.
- 따라서 책의 규칙은 "GWT로 쓰면 좋아진다"가 아니라 "수용 기준을 **실행 가능한 테스트로 바꿀 수 있는 형태**로 쓰고, 그 테스트를 사람이 소유한다"가 근거에 맞다.
- BDD 체계적 매핑 연구(Binamungu & Maro, JSS vol. 203, 111749, 2023, DOI 10.1016/j.jss.2023.111749)와 BDD 명세 유지보수 과제 연구(Binamungu 외, SANER 2018, pp. 175–184, DOI 10.1109/SANER.2018.8330207)는 메타만 확인했다.

---

## (4) 스펙 상세도·입도와 에이전트 출력 품질

기준 보고서 6절의 스펙 격차 연구(상세도 L0→L3에서 단일 에이전트 89% → 56%) [기준 r17], SLUMP [기준 r16], 플래너-코더 격차 [기준 r229], Lost in the Middle [기준 r275], 문구별 준수율 연구 [기준 r267]가 이 영역의 기본 근거다. 여기서는 "무엇을 더 적으면 효과가 있는가"와 "얼마나 많이 적으면 역효과인가"를 더한다.

### 논문 16: Guidelines to Prompt Large Language Models for Code Generation: An Empirical Characterization

- 저자·연도: Alessandro Midolo, Alessandro Giagnorio, Fiorella Zampetti, Rosalia Tufano, Gabriele Bavota, Massimiliano Di Penta, 2026
- 발표처: arXiv 프리프린트(게재처 표기 없음)
- arXiv ID: 2601.13118
- 피인용수: 미조회
- 발표 상태: 프리프린트 / 확인 수준: HTML
- 요약: 테스트가 실패하는 코드 생성 프롬프트를 테스트 통과까지 자동으로 고치게 하고, 그 수정 내용을 분류해 프롬프트 개선 지침 10개를 뽑았다. 그다음 실무자 50명에게 사용 빈도와 유용성을 물었다.
- 방법론 요약: BigCodeBench(1,140), HumanEval+(163), MBPP+(375), 모델 4개(GPT-4o mini, Llama 3.3 70B, Qwen2.5 72B, DeepSeek Coder V2).
- 핵심 수치·결과(최적화된 프롬프트 627개 중 각 패턴이 쓰인 비율):

  | 지침 | 내용 | 적용 비율 |
  |---|---|---|
  | 알고리즘 세부 | 복잡한 로직의 정의·공식·세부 | 57% |
  | 입출력 형식 | 입출력 타입·구조·특수 경우 | 44% |
  | 예시 추가 | 구체 예시, doctest | 24% |
  | 사후조건 | 출력의 범위·순서 같은 보장 | 23% |
  | 의존 요구 | 필요한 라이브러리와 용도 | 19% |
  | 예외 | 어떤 예외를 언제, 어떤 메시지로 | 12% |
  | 단정형 언어 | "must"처럼 확정적인 표현 | 9% |
  | 사전조건 | 실행 전 성립해야 할 조건 | 7% |
  | 변수 명칭 일관 | 같은 대상에 같은 이름 | 3% |
  | 불명확한 조건 | "otherwise" 대신 양쪽 분기를 모두 명시 | 1% |

  - 실무자 약 88%가 입출력 형식 지침을 유용하다고 평가했다. 예시 추가는 실제 사용보다 유용성 평가가 높았다(저자는 인지 부족 가능성을 든다). 단정형 언어는 가장 적게 쓰였다.
- 주의점: 함수 수준 Python 벤치마크. 수정 프롬프트 수가 본문 안에서 627과 690(모델별 합)으로 엇갈린다. 동료심사 전.
- 작성 규칙(추론): 스펙의 "기능" 절에 최소한 입출력 형식, 사후조건, 예외 처리, 예시 1~2개를 넣는다. "그 외의 경우"라고 뭉개지 말고 분기마다 결과를 쓴다. 기준 보고서의 EPIC 사례("should" 대신 "must") [기준 r235]와 지침 10이 같은 방향이다.

### 논문 17: What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts

- 저자·연도: Chenyang Yang, Yike Shi, Qianou Ma, Michael Xieyang Liu, Christian Kästner, Tongshuang Wu, 2026(학회) / 2025(arXiv)
- 발표처: Findings of the Association for Computational Linguistics: ACL 2026, pp. 9072–9101
- DOI: 10.18653/v1/2026.findings-acl.441 / arXiv:2505.13360
- 피인용수: 미조회
- 발표 상태: 동료심사 / 확인 수준: 초록
- 요약: LLM 프롬프트에서 요구를 빠뜨리는 "덜 정함"을 분석했다. 모델은 빠진 요구를 기본값으로 추론하기도 하지만, 그 행동은 깨지기 쉽다.
- 핵심 수치·결과(초록 기준):
  - 명시하지 않은 요구를 모델이 기본으로 맞힌 비율 41.1%.
  - 덜 정한 프롬프트는 모델이나 프롬프트가 바뀔 때 회귀할 가능성이 2배였고, 정확도가 20% 넘게 떨어지는 경우도 있었다.
  - 모든 요구를 그냥 다 적는 것은 일관되게 도움이 되지 않았다. 모델의 지시 준수 능력에 한계가 있고 요구끼리 충돌하기 때문이다.
  - 요구를 의식한 프롬프트 최적화가 기준선 대비 평균 4.8% 향상.
- 작성 규칙(추론):
  1. 지금 모델이 알아서 맞혀 주는 요구라도, 모델을 바꿀 때 깨지면 안 되는 것은 스펙에 적는다. 암묵 요구는 모델 교체 때 회귀의 2배 위험이다.
  2. 반대로 요구를 무한히 늘리지 않는다. 적을 요구를 고르고, 서로 충돌하지 않는지 확인한다.
- 주의점: 코딩 에이전트가 아니라 LLM 애플리케이션 프롬프트 대상.

### 논문 18: How Many Instructions Can LLMs Follow at Once? (IFScale)

- 저자·연도: Daniel Jaroslawicz, Brendan Whiting, Parth Shah, Karime Maamari, 2025
- 발표처: arXiv 프리프린트
- arXiv ID: 2507.11538
- 피인용수: 미조회
- 발표 상태: 프리프린트 / 확인 수준: 초록
- 요약: 보고서 작성 과제에 "키워드 포함" 지시를 최대 500개까지 넣어 지시 밀도에 따른 준수율 저하를 20개 모델로 쟀다.
- 핵심 수치·결과: 최고 수준 모델도 지시 500개에서 정확도 68%. 모델 크기와 추론 능력에 따라 세 가지 저하 패턴이 나타났고, 앞쪽 지시를 더 잘 지키는 편향이 있었다.
- 작성 규칙(추론): 스펙과 컨텍스트 파일에 지시를 쌓을수록 일부는 조용히 무시된다. 꼭 지켜야 할 제약은 수를 줄이고 앞쪽에 둔다. 기준 보고서의 Lost in the Middle [기준 r275], 컨텍스트 파일 비용 연구 [기준 r231]와 함께 읽는다.
- 주의점: 단순 키워드 포함 지시라 코드 제약과 성격이 다르다. 2025년 7월 모델 기준.

### 상세도 영역 종합

- 근거는 두 방향을 함께 가리킨다. 적어야 할 것을 빼면 결과가 나쁘고 불안정하다(스펙 격차, Yang, Midolo). 너무 많이 적으면 준수율이 떨어지고 요구끼리 충돌한다(Yang, IFScale, 기준 보고서의 컨텍스트 파일 연구).
- 책의 실천 규칙(추론): **"입출력·조건·예외·예시는 빠짐없이, 배경 설명과 저장소 개요는 최소로, 꼭 지킬 제약은 짧게 앞에."** 저장소 수준 과제에서 이 균형점을 잰 연구는 이번 조사에서 찾지 못했다.

---

## (5) 계약에 의한 설계와 경량 형식 명세: 스펙 사다리의 꼭대기

기준 보고서 6절이 nl2postcond, Lahiri, SpecGen, AutoSpec, Clover, Verus-SpecGym, Maji, AxDafny, RLVR 스펙 해킹을 다뤘다 [기준 r257~r264, r230]. 결론은 "진전이 크지만 증명 통과가 의도 포착은 아니다"였다. 여기서는 개발자가 실제로 오를 수 있는 **중간 단**(계약, 속성 기반 테스트, 실행 가능한 참조 모델)과 그 산업 근거를 더한다.

### 논문 19: Applying "Design by Contract"

- 저자·연도: Bertrand Meyer, 1992
- 발표처: IEEE Computer, vol. 25, no. 10, pp. 40–51
- DOI: 10.1109/2.161279
- 피인용수: 1,419 (Crossref, 2026-11-10)
- 발표 상태: 잡지(IEEE Computer, 편집 심사) / 확인 수준: **메타만**(본문 미열람)
- 요약(널리 알려진 개념, 원문 문장 대조 전): 루틴과 호출자의 관계를 계약으로 본다. 사전조건(precondition)은 호출자가 지킬 의무, 사후조건(postcondition)은 루틴이 보장할 결과, 클래스 불변식(invariant)은 객체가 늘 지키는 성질이다. Eiffel 언어가 이를 언어 차원에서 지원한다.
- 관련: Jean-Marc Jézéquel, Bertrand Meyer, "Design by Contract: The Lessons of Ariane", IEEE Computer 30(1), pp. 129–130, 1997, DOI 10.1109/2.562936 (메타만). Ariane 5 사고를 계약 관점에서 해석한 짧은 기고로 알려져 있다.
- 작성 규칙(추론): 자연어 스펙의 "기능" 하나마다 "호출 전에 참이어야 할 것 / 호출 뒤 참이 될 것 / 언제나 참인 것" 세 줄을 쓰는 것이 계약 단의 최소 형태다. Midolo 연구에서 사전·사후조건이 테스트 통과로 이끈 수정 패턴이었다는 점(7%, 23%)이 LLM 시대의 간접 근거다.
- fact-checker 주의: 이 항목의 개념 설명은 원문과 대조하지 않았다. 본문에 Meyer의 문장을 인용하려면 원문 확인이 필요하다.

### 논문 20: How Amazon Web Services Uses Formal Methods

- 저자·연도: Chris Newcombe, Tim Rath, Fan Zhang, Bogdan Munteanu, Marc Brooker, Michael Deardeuff, 2015
- 발표처: Communications of the ACM, vol. 58, no. 4, pp. 66–73
- DOI: 10.1145/2699417
- 피인용수: 312 (Crossref, 2026-11-10)
- 발표 상태: 잡지(CACM 편집 심사) / 확인 수준: 본문(2014-09-29 저자 원고 "Use of Formal Methods at Amazon Web Services", lamport.azurewebsites.net 게시본). **수치는 이 원고 기준이며 CACM 최종본과 다를 수 있다.**
- 요약: AWS는 2011년부터 TLA+(와 PlusCal)로 분산 시스템 설계를 명세하고 모델 체킹했다. 산문 설계 문서는 모호하고 부분 장애나 원자성 단위를 빠뜨리기 쉬운데, 정밀한 설계 명세는 작성자를 더 명확히 생각하게 하고 도구로 검사할 수 있다.
- 핵심 수치·결과(저자 원고 기준):
  - TLA+를 대형 실서비스 시스템 10개에 적용했고, 모든 경우에 미묘한 버그를 찾거나 공격적 성능 최적화를 할 확신을 주었다.
  - 신입부터 수석 엔지니어까지 TLA+를 처음부터 배워 2~3주 안에 쓸모 있는 결과를 냈다.
  - DynamoDB 복제·그룹 멤버십 명세(939줄)에서 버그 3개를 찾았고, 일부는 오류를 드러내는 가장 짧은 추적이 35단계였다.
  - 설계·코드 리뷰를 여러 번 통과하고 몇 달 시험 뒤에야 드러난 버그를, 2주 동안 쓴 명세로 모델 체커가 몇 초 만에 찾은 사례가 있다.
- 작성 규칙(추론): 형식 명세는 "모든 코드"가 아니라 동시성·장애 복구처럼 시험으로는 상태 공간을 다 못 덮는 설계 핵심부에 쓴다. 이 경우 학습 비용은 몇 주 수준이라는 산업 근거가 있다.
- 후속: Brooker & Desai, "Systems Correctness Practices at Amazon Web Services", CACM 2025, DOI 10.1145/3729175 (메타만).

### 논문 21: Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3

- 저자·연도: James Bornholt, Rajeev Joshi, Vytautas Astrauskas, Brendan Cully, Bernhard Kragl, Seth Markle 외, 2021
- 발표처: Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles (SOSP '21), pp. 836–850
- DOI: 10.1145/3477132.3483540
- 피인용수: 68 (Crossref, 2026-11-10)
- 발표 상태: 동료심사 / 확인 수준: 초록(Amazon Science 게시 페이지)
- 요약: 개발 중인 S3 저장 노드 ShardStore에 완전한 형식 검증 대신 "경량 형식 기법"을 적용했다. 정확성을 독립 속성으로 나누고 속성마다 맞는 도구로 검사하며, 실행 가능한 참조 모델을 구현의 스펙으로 썼다.
- 핵심 수치·결과: 크래시 일관성과 동시성 문제를 포함해 16건이 운영 진입 전에 차단되었다. 형식 기법 비전문가가 기능이 늘 때 검사를 직접 확장했다.
- 인용할 만한 문장:
  > "prevented 16 issues from reaching production" (초록)
- 작성 규칙(추론): 증명 대신 "실행 가능한 참조 모델 + 그 모델과 구현을 대조하는 자동 검사"가 현실적인 꼭대기 단이다. 에이전트에게는 참조 모델을 스펙으로, 대조 검사를 수용 관문으로 준다.

### 논문 22: Alloy: A Lightweight Object Modelling Notation

- 저자·연도: Daniel Jackson, 2002
- 발표처: ACM Transactions on Software Engineering and Methodology, vol. 11, no. 2, pp. 256–290
- DOI: 10.1145/505145.505149
- 피인용수: 814 (Crossref, 2026-11-10)
- 발표 상태: 동료심사 / 확인 수준: **메타만**
- 요약: "경량 형식 기법"이라는 말의 대표 출처 중 하나다. 자동 분석이 가능한 작은 관계형 모델링 언어를 제안했다. 이번 조사에서는 본문을 읽지 않았으므로 내용 주장은 하지 않는다. AWS 원고는 Pamela Zave가 Alloy로 Chord 멤버십 프로토콜의 버그를 찾은 사례가 AWS의 형식 기법 도입 근거가 되었다고 적는다(Newcombe 원고 "First Steps" 절).

### 논문 23: Towards AI-Assisted Synthesis of Verified Dafny Methods

- 저자·연도: Md Rakib Hossain Misu, Cristina V. Lopes, Iris Ma, James Noble, 2024
- 발표처: Proceedings of the ACM on Software Engineering, vol. 1, FSE (FSE 2024), pp. 812–835
- DOI: 10.1145/3643763 / arXiv:2402.00247
- 피인용수: 미조회
- 발표 상태: 동료심사 / 확인 수준: 초록
- 요약: MBPP 178문제로 GPT-4와 PaLM-2에게 검증 가능한 Dafny 메서드(코드와 스펙)를 합성하게 했다. 프롬프트는 맥락 없음, 시그니처+테스트, 사고 사슬+검색 예시의 세 종류였다.
- 핵심 수치·결과: GPT-4는 사고 사슬+검색 예시 프롬프트로 문제의 58%에서 검증되고 사람이 확인한 Dafny 메서드를 만들었다. 맥락 없음은 19%, 시그니처+테스트는 10%였다.
- 작성 규칙(추론): 형식 명세 단에서는 시그니처와 테스트만 주는 것으로 부족했다. 문제를 단계로 나눈 설명과 비슷한 문제의 검증된 예시가 필요했다. 형식 스펙을 에이전트에게 시킬 때도 "예시 + 단계 분해"가 핵심이다.
- 주의점: 2023~2024년 모델, 함수 수준 과제. 기준 보고서의 AxDafny(92.7%) [기준 r230]가 최신 수준이다.

### 논문 24: Can Large Language Models Write Good Property-Based Tests?

- 저자·연도: Vasudev Vikram, Caroline Lemieux, Joshua Sunshine, Rohan Padhye, 2023(arXiv v1) / v2 개정
- 발표처: arXiv 프리프린트(게재처 표기 없음)
- arXiv ID: 2307.04346
- 피인용수: 미조회
- 발표 상태: 프리프린트 / 확인 수준: 초록
- 요약: API 문서를 자연어 스펙으로 삼아 LLM이 속성 기반 테스트(PBT)를 합성하게 하고, 유효성·건전성·속성 커버리지(속성 변이체를 잡는 능력)로 평가했다. Python 라이브러리 API 메서드 40개, 모델 3개(GPT-4, Gemini-1.5-Pro, Claude-3-Opus).
- 핵심 수치·결과: 최선 조건에서 유효하고 건전한 PBT를 평균 2.4회 샘플링으로 얻었다. 그러나 API 문서에서 뽑을 수 있는 속성 중 GPT-4가 올바른 PBT로 만든 비율은 21%였다. 건전성 판정 지표는 사람 판단과 정밀도 100%, 재현율 97%로 일치했다.
- 작성 규칙(추론): 스펙 문서에 "항상 참인 성질"(예: 정렬 결과는 비내림차순, 직렬화 후 역직렬화하면 원래 값)을 명시해 두면, 에이전트가 PBT로 옮길 재료가 된다. 문서에서 속성을 스스로 찾게 두면 대부분을 놓친다(21%).

### 논문 25: Agentic Property-Based Testing: Finding Bugs Across the Python Ecosystem

- 저자·연도: Muhammad Maaz, Liam DeVoe, Zac Hatfield-Dodds, Nicholas Carlini, 2025
- 발표처: NeurIPS 2025, The 4th Deep Learning for Code Workshop
- arXiv ID: 2510.09907
- 피인용수: 미조회
- 발표 상태: 동료심사(워크숍) / 확인 수준: 초록
- 요약: 에이전트가 Python 모듈의 코드와 문서에서 속성을 추론하고 PBT를 합성·실행해 버그 보고서를 낸다. 인기 패키지 100개에 적용했다.
- 핵심 수치·결과: 에이전트 버그 보고의 56%가 수동 검토에서 실제 버그였고, 32%는 유지보수자에게 보고할 만했다. 상위 점수 21건은 86%가 실제 버그였다. 보고 5건 중 패치 3건이 병합되었다(NumPy 포함).
- 작성 규칙(추론): PBT는 저자들 표현대로 "경량 형식 기법"이다. 스펙의 불변식을 PBT로 바꾸는 일은 에이전트에게 맡길 수 있지만, 결과 보고의 절반 가까이는 거짓 경보이므로 사람 검토가 남는다.

### 논문 26: Effective LLM Code Refinement via Property-Oriented and Structurally Minimal Feedback (PGS)

- 저자·연도: Lehan He, Zeren Chen, Zhe Zhang, Xiang Gao, Lu Sheng, 2025
- 발표처: arXiv 프리프린트
- arXiv ID: 2506.18315
- 피인용수: 미조회
- 발표 상태: 프리프린트 / 확인 수준: 초록
- 요약: 테스트 개수보다 피드백 품질에 초점을 둔다. 고수준 속성(예: 정렬 함수 출력은 비내림차순)을 검사하고 가장 단순한 반례를 LLM에 돌려준다.
- 핵심 수치·결과: 다른 TDD 기반 방법 대비 pass@1 최대 +13.4%, 처음 실패한 문제의 64% 이상을 고쳤다. 버그 수정률이 가장 강한 디버깅 기반 방법의 1.4~1.6배.
- 작성 규칙(추론): 입출력 예시만 나열하는 것보다 "성질" 한 줄이 에이전트의 수정 루프에 더 좋은 신호를 준다. 테스트 사다리에서 예시 테스트 다음 단을 속성으로 두는 근거다.

### 계약·경량 형식 영역 종합

- 산업 근거(AWS 2건)는 "설계 핵심부에 정밀 명세를 쓰면 시험으로 못 찾는 버그를 찾는다"를 보인다. 학습 비용은 몇 주였다. 다만 두 건 모두 AWS 저자의 자기 보고이고, 대상은 분산 저장·복제 시스템이다.
- LLM 근거는 "속성을 명시하면 에이전트가 그것을 테스트와 피드백으로 잘 쓰지만, 속성을 스스로 찾는 능력은 약하다"(21%, 거짓 경보 약 절반)를 보인다.
- 책의 사다리 제안(추론): 자연어 요구 → EARS 문형 → 수용 기준(GWT) → 예시 테스트(사람 소유) → **계약(사전·사후·불변식)과 속성 기반 테스트** → 실행 가능한 참조 모델 → 형식 명세·증명. 대부분의 업무 코드는 계약·속성 단까지가 비용 대비 효율적이라는 판단은 측정이 아니라 추론이다.

---

## 기준 보고서와의 연결표

| 이 파일의 항목 | 기준 보고서 6절의 짝 | 관계 |
|---|---|---|
| EARS 2009 | Kiro·cc-sdd의 EARS 사용 [기준 r99, r100] | 도구가 쓰는 문형의 원 출처와 그 효과 근거 |
| HumanEvalComm, Ambig-SWE | ClarifyGPT, ClarifyCodeBench, Orchid, UnderSpecBench [기준 r228, r248, r249, r245] | "모델은 혼자 모호함을 잘 못 찾는다"를 저장소 수준(Ambig-SWE)과 결함 유형별(HumanEvalComm)로 보강 |
| 요구 냄새 2편 | SpecFix [기준 r250] | 스펙 결함 밀도가 정답률을 떨어뜨린다는 간접 근거 |
| QUS, BDD 4편 | TDFlow, TestSuiteBench, 스펙-오라클 격차 [기준 r20, r22, r244] | 수용 기준 작성 단계의 품질 기준 |
| Midolo, Yang, IFScale | 스펙 격차, EPIC, Lost in the Middle, 문구별 준수율 [기준 r17, r235, r275, r267] | 적을 것(입출력·조건·예시)과 줄일 것(지시 수)의 양쪽 근거 |
| AWS 2편, Meyer, PBT 3편, Misu | 형식 명세 9편 [기준 r256~r264, r230] | 증명 단 아래의 현실적 꼭대기 단(계약·속성·참조 모델) |

## 수집 한계

- EARS가 LLM 에이전트 출력 품질을 자유 서술보다 높인다는 통제 실험, Given-When-Then 수용 기준이 에이전트 구현을 개선한다는 통제 실험은 찾지 못했다. 두 주제의 근거는 사람 대상 요구공학 연구와 LLM 간접 근거의 결합이다.
- Big EARS(2010), Listens Learned(2016), Alloy(2002), Meyer(1992), BDD 매핑 연구(2023)는 유료 또는 추출 실패로 메타만 확인했다. 본문 인용 전에 원문 확인이 필요하다.
- Semantic Scholar API가 요청 제한(429)을 걸어 피인용수 다수를 Crossref로 대신했다. 2024년 이후 논문 대부분은 피인용수를 조회하지 않았다.
- Femmer 외(2017)의 냄새 목록과 Salari 외(2025)의 실험 세부는 PDF 텍스트 추출에 실패해 초록 수준으로만 적었다.
- AWS TLA+ 수치는 CACM 최종본이 아니라 2014년 저자 원고에서 읽었다.
- 2026년 프리프린트(Midolo, Rathnayake, AutoGlue, IFScale, PGS, Vikram)는 동료심사 전이다.
