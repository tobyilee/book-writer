# 통합 레퍼런스 — 꺼내 쓰는 뇌

본 문서는 Phase 1 리서치의 마스터 인덱스다. 세 명의 전문 리서처가 각자 산출한 원본 파일을 함께 읽어야 한다.

## 원본 자료 위치

| 파일 | 분량 | 담당 영역 |
|------|------|----------|
| `research/papers.md` | 8,882단어, 60편 논문 | 학술 근거 — 인용·수치·실험 설계 |
| `research/web.md` | 6,303단어, 7권 도서 + 강의 | 권위 자료 — 학습법 베스트셀러·코치·도구 |
| `research/community.md` | 4,141단어, 28개 일화 | 실제 학습자 고통·성공·안티패턴 |

## 챕터 저자가 반드시 인지해야 할 프레이밍 가이드

### 1) 핵심 차별 메시지 — 인코딩 우선론
대중 학습법 시장의 표준 처방은 "Anki + Spaced Repetition"이다. 본 책은 **"애초에 인코딩의 질을 높여 망각 곡선의 경사를 완만하게 만든다"** 는 입장을 차별점으로 가져간다 (Justin Sung의 "encoding-first" 주장과 동일 맥락). 단순 SRS 비판 → 인코딩 강화 → 인출 훈련 → 시스템 구축의 순서로 흐른다.

### 2) 용어 사용 주의

- **"PACER 정보 분류법"** — 학술 용어가 아니라 Justin Sung(iCanStudy)의 학습 코칭 프레임워크다. Procedural / Analogous / Conceptual / Evidence / Reference. 본문 첫 등장 시 **"학습 코치 Justin Sung이 제안한 분류법"** 로 출처를 명시한다.
- **"Opportunistic Retrieval"** — Sung 강의에서 직접 이 라벨로 명명된 출처를 찾지 못했다. 의미상 같은 자리에 SIR(Spaced Interleaved Retrieval), Free vs Cued Recall이 있다. 본서가 이 용어를 핵심 키워드로 채택할 경우 **"Toby의 명명, Sung의 학습 철학에서 영감"** 으로 표기한다.
- **"Retrieval Practice"의 한국어** — "인출 연습"으로 통일하되, 첫 등장 시 영문 병기. "회상 연습"은 cued recall 뉘앙스라 피한다.
- **수치 표기** — Roediger & Karpicke 2006a의 idea unit 비율(SS≈0.42, ST≈0.56)은 그래프 추정값이다. 본문에서 "약 0.42 vs 약 0.56" 또는 "약 14%p 차이"로 보수적으로 적는다.

### 3) 한국 독자 친화도

- chapter opener는 가능한 한 한국 일화로 시작 (community.md 한국 일화 섹션 활용)
- 영문 일화도 한국 독자가 즉시 공감 가능한 상황(시험·이직·발표·인터뷰)으로 골라 옮김
- 한국:영문 일화 비율 6:4 유지

### 4) 학술 정직성 체크리스트

- 10,000시간 신화는 Macnamara 메타분석이 반박했다 — 단정적으로 쓰지 않는다 (papers.md 논쟁 섹션 참조)
- Sparrow 2011 Google Effect는 재현 실패 사례 있음 — "초기 가설 + 후속 재현 논쟁"으로 둔다
- Dunning-Kruger는 통계적 비판 있음 — 보조 도구로만 사용
- MIT Cognitive Debt 연구(Kosmyna 2024)는 arXiv preprint — "사전 인쇄"로 명시

## 챕터 매핑 요약 (각 파일의 챕터 매핑 섹션이 더 상세)

### 1장 — 망각의 원리
- 핵심 근거: Ebbinghaus(1885), Bahrick(1984) permastore, Dunlosky(2013) 10기법 등급, Karpicke·Butler·Roediger(2009) 학생들이 retrieval 안 쓰는 현실
- 대표 일화: 최윤석(Brunch) "책을 덮는 순간 수증기처럼 증발한다", 책 100권 챌린지 후기
- 대중 자료: Make It Stick의 "rereading is the most-preferred but least-effective", Coursera Learning How to Learn의 illusion of competence

### 2장 — 인코딩 전략
- 핵심 근거: Sweller Cognitive Load, Craik & Lockhart Levels of Processing, Bartlett schema, Bloom's Taxonomy 개정판, Gentner structure mapping, Slamecka & Graf Generation Effect
- 대표 도구: PACER 분류 (Sung, dev.to/Suraj Vatsya 정리), 마인드맵, 유추 만들기
- 대표 일화: yoon_life0315(Threads) "읽기는 입력이고 시험은 꺼내는 것", 노트만 예쁘게 정리하다 망한 사례

### 3장 — 인출의 기술
- 핵심 근거: Roediger & Karpicke(2006a, 2006b), Karpicke & Roediger(2008) Science, Karpicke & Blunt(2011), Bjork desirable difficulties, Cepeda(2006) 메타분석, Adesope(2017) 메타분석, Self-Explanation(Chi)
- 대표 도구: 백지 인출(blank page recall), 파인만 기법 4단계, free vs cued recall
- 대표 일화: giraffesunrise(Anki Forums) "Yesterday I reviewed 1671 cards", Brunch 학생 "내가 확실히 뭘 모르는지 눈에 보인다"

### 4장 — 기회주의적 인출
- 핵심 근거: Tolman(1948) latent learning, Pyc & Rawson(2010) mediator effectiveness, Larsen(2009) 의대 RCT(+13%p), Carpenter & DeLosh transfer
- 대표 도구: 다음 날 팀 브리핑에서 가르치기, 의사결정에 즉시 적용, 즉시 피드백 받기
- 대표 일화: 직장인의 "공부할 시간 없다" 호소, 의대생 OSCE 인출 훈련, 우아한형제들 기술 공유 문화

### 5장 — 메타인지·시스템
- 핵심 근거: Flavell(1979) metacognition, Nelson & Narens metamemory, Risko & Gilbert cognitive offloading, Sparrow(2011) Google Effect(재현 논쟁 주의), MIT Kosmyna(2024) preprint
- 대표 도구: 메타인지 레이더(active vs passive 자기 점검), Luhmann Zettelkasten, BASB(Tiago Forte) 비판적 검토
- 대표 일화: 클리앙 날아라국장 "AI가 다 짜준 코드를 후배는 본인이 모른다", 옵시디언 무덤(collector's fallacy)

## 5개 정서적 앵커 인용 (책 전반 활용)

community.md의 부록 B에 정리된 핵심 인용:

1. **1장 첫 문장 후보** — 최윤석 (Brunch, 2016): "책을 덮는 순간 수증기처럼 증발한다."
2. **2장 epigraph** — yoon_life0315 (Threads, 2026): "읽기는 입력이고 시험은 꺼내는 것이다. 두 가지는 완전히 다른 능력이다."
3. **3장 사례 박스** — giraffesunrise (Anki Forums, 2021): "Yesterday I reviewed 1671 cards. … I'm about to throw in the towel."
4. **3장 처방 도입** — Brunch 인터뷰 학생 (2024): "내가 확실히 뭘 모르는지 눈에 보인다."
5. **5장 도입** — 날아라국장 (클리앙, 2024): "AI가 다 짜준 코드를 후배는 본인이 모른다."

## 사용법

book-planner와 chapter-writer 모두 이 인덱스를 먼저 읽고, 필요한 챕터의 원본 파일을 추가로 읽어 인용을 뽑는다. 인용 시 papers.md / web.md / community.md 어느 파일의 어느 섹션을 참조했는지 메모를 남긴다.
