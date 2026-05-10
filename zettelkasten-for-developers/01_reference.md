# Zettelkasten for Developers — 리서치 종합

> **대상 독자:** 소프트웨어 개발자
> **주제:** Zettelkasten을 Obsidian으로 일상에 적용하는 방법
> **합본 일자:** 2026-05-10
> **소스:** web.md (20건), papers.md (8편), community.md (5+5+5건)

---

## 1. 개념·정의

### 1.1 Zettelkasten이란
독일어로 "슬립박스(slip box)". 1950년대부터 1997년까지 독일 사회학자 **Niklas Luhmann**이 약 90,000장의 색인 카드를 운영하며 70권의 책과 400편의 논문을 산출한 개인 지식 시스템. 단순한 색인이 아니라 "사고 파트너(communication partner)"로 기능했다는 것이 핵심 — 사용자가 **카드의 내용을 완벽히 예측하지 못하기 때문에** 카드와의 만남이 새 정보를 만들어낸다 (Schmidt, 2016).

Luhmann은 통념과 달리 **두 개의 슬립박스**를 별도로 운영했다 — (1) 서지 정보용 카탈로그(자기 의견 없음), (2) 사고 도구(자기 사유). 번호 체계는 위계가 아니라 **사고 흐름의 분기**를 표현한다 (1, 1a, 1a1, 1b, 2…).

### 1.2 핵심 용어 (Sönke Ahrens, 2017 표준화)

| 용어 | 정의 | 수명 | 위치 |
|------|------|------|------|
| **Fleeting Note** | 떠오른 생각의 즉시 캡처. 정리되지 않아도 됨. 24시간 내 가공 또는 폐기. | 일회성 | Inbox |
| **Literature Note** | 한 자료(책·논문·영상)의 핵심을 자기 언어로 요약 + 출처 명시. | 영구 보관 | Reference |
| **Permanent Note** | 한 개의 atomic 아이디어를 자기 문장으로 작성. 출처 맥락 없이도 일주일 후의 자신이 이해 가능해야 함. | 영구 + 갱신 | Zettelkasten |
| **MOC (Map of Content)** | 특정 주제로 들어가는 진입점. 하위 노트들의 인덱스. | 영구 + 재구성 | 진입점 |
| **Atomic Note** | "한 노트 = 한 주장(claim)" (Bob Doto) 또는 "한 노트 = 한 아이디어" (Ahrens). | — | — |

### 1.3 관점 차이 — Permanent Note vs Evergreen Note
같은 의미로 쓰이는 경우가 많지만, **Bob Doto는 둘을 구분한다** —
- **Permanent**: "더 이상 손대지 않는 완성형 카드" (Luhmann 원형)
- **Evergreen** (Andy Matuschak): "지속적으로 갱신·재작성되는 살아있는 노트, API처럼 제목이 안정적인 인터페이스"

이 책에서는 두 용어를 혼용하되, **"갱신을 전제하는가"** 가 둘의 본질적 차이임을 명시할 것.

### 1.4 Obsidian이란
2020년 출시된 마크다운 기반 PKM 도구. 캐나다 워털루대 졸업생 Erica Xu·Shida Li가 개발. 2025년 기준 활성 사용자 150만+, 커뮤니티 플러그인 2,000+. **로컬 파일 우선(local-first)**·**플레인 마크다운**·**[[bidirectional links]]**가 세 기둥. 핵심 기능은 코어로 모두 가능하고 플러그인은 옵션.

---

## 2. 주요 관점

### 2.1 학술적 근거 — 왜 Zettelkasten은 작동하는가
인지과학 4개 효과가 동시에 활용되기 때문이다.

| 효과 | 출처 | Zettelkasten에서의 발현 |
|------|------|------------------------|
| **Testing Effect** | Roediger & Karpicke (2006) — 인용 4,500+ | Permanent note를 다시 쓰는 행위 자체가 인출 연습 |
| **Spacing Effect** | Cepeda et al. (2006) — 인용 2,500+ | 주간 리뷰·spaced repetition 플러그인의 이론적 근거 |
| **Elaborative Interrogation / Self-Explanation** | Dunlosky et al. (2013) "moderate utility" 등급 | "왜 이 개념이 다른 노트와 충돌하는가" 같은 메타 질문 |
| **Writing-to-Learn** | Bangert-Drowns et al. (2004) 메타분석 — d≈0.17, 메타인지 프롬프트 추가 시 4배 | Permanent note 작성 = 메타인지 프롬프트 + 자기 언어 |

**해석상 주의:** Mueller & Oppenheimer(2014)의 "손글씨 > 키보드" 연구는 후속 재현(Morehead et al., 2019)에서 효과 크기가 작아졌다. 그러나 "verbatim transcription을 피하고 자기 언어로 재구성하라"는 메커니즘은 반복적으로 검증됨 — 이게 Zettelkasten의 permanent note 원칙과 정확히 일치한다.

### 2.2 철학적 토대 — Extended Mind
Clark & Chalmers(1998) "The Extended Mind" — 인지는 두개골 안에 갇혀 있지 않다. 다이어리·노트가 "능동적 외재주의(active externalism)" 조건을 만족하면 그 자체가 마음의 일부. **Otto의 다이어리** 사고 실험: 알츠하이머 환자 Otto가 다이어리로 약속을 기억한다면, 그 다이어리는 일반인의 기억과 인지적으로 동등한 지위를 갖는다.

> 책에서의 활용: "당신의 README와 ADR은 이미 팀의 외장된 마음이다 — Zettelkasten은 그것을 개인 차원으로 끌어내린 것."

### 2.3 전문가 관점 비교

| 인물 | 강조점 | 차별점 |
|------|--------|--------|
| **Niklas Luhmann** (원형) | 두 박스 분리, 분기 번호, communication partner | "사고 파트너"는 사용자를 놀라게 해야 함 |
| **Sönke Ahrens** (How to Take Smart Notes, 2017) | 3종 노트 분류 표준화 | "베끼지 말고 새로운 것을 만들어라" |
| **Andy Matuschak** (evergreen notes) | 5원칙: 원자적·개념 중심·밀집 링크·연관 우선·자신을 위해 | 제목을 API처럼, spaced repetition 통합 |
| **Bob Doto** (A System for Writing, 2024) | 한 노트 = 한 주장(claim) | Evergreen ≠ Permanent 구분, 학습보다 글쓰기 결과 강조 |
| **Tiago Forte** (BASB / PARA, 2022) | 자료 관리 시스템 | "Zettelkasten은 사고, PARA는 자료" — 다른 층위 |
| **Nick Milo** (Linking Your Thinking, LYT) | MOC 중심 | 80/20 — 순수 Zettelkasten 없이도 80% 효과 |

---

## 3. 실제 사례

### 3.1 개발자 워크플로우 패턴

**(a) 코드 리뷰 노트 (Architecture Decision Records, ADR)**
- Matteo Paoli (Medium) — Obsidian + Git에 MADR 템플릿 + Templater 자동화. 결정 카드는 백링크로 관련 결정과 연결되어 "결정의 진화"를 추적 가능.
- 폴더 구조: `01_decisions/` 안에 `ADR-001-postgres-vs-mongo.md` 같이 번호 부여, 각 ADR은 백링크로 영향받는 시스템 노트와 연결.

**(b) 학습 일지 (TIL — Today I Learned)**
- 한국 개발자 다수: Daily Notes + 학습한 개념을 즉시 atomic note로 분리.
- 패턴: `2026-05-10.md` (데일리) → `[[Postgres VACUUM 동작 원리]]` (atomic) → `[[MVCC]]` (개념)
- GitHub Private 저장소 + Obsidian Git 플러그인이 한국 표준 셋업 (Sync 유료 회피).

**(c) AI 컨텍스트 저장소 (2025~2026 부상한 새 사용 사례)**
- 한국 디지털투데이 보도(2024) + 청년개발자신문(2026): 옵시디언이 "AI 코딩 시대의 지식 저장소"로 재발견됨.
- 폴더 패턴: `01_requirements/`, `02_architecture/`, `03_prompts/`, `04_results/`. MCP로 Claude/Claude Code가 vault 직접 참조.

**(d) 회의록·일감 관리**
- 송요창(Medium): 일감 트래킹 + 학습 노트 + 회고를 한 vault에 통합. 이모지 메타데이터(📅 due, 🏃 in-progress)와 백링크.

### 3.2 도구 사용 패턴 — 코어 vs 플러그인

**최소 셋업 (시작 권장):**
1. Obsidian 코어 + 한국어 설정
2. 핵심 단축키만 익히기 (`[[`, `Ctrl+O`, `Ctrl+Shift+F`)
3. 폴더는 `Inbox/`, `Permanent/`, `Reference/` 세 개만

**3~4주 후 추가 (Sébastien Dubois 2026 가이드):**
- **Templater**: 노트 템플릿 자동 삽입
- **Dataview**: SQL처럼 노트 쿼리, MOC 자동 생성
- **Periodic Notes**: 주간/월간 노트
- **Excalidraw**: 다이어그램·스케치
- **Smart Connections**: AI 임베딩으로 의미적 유사 노트 추천

**개발자 특화:**
- **Obsidian Git**: GitHub Private 저장소 동기화 (한국에서 표준)
- **Code Block Customizer**: 코드 하이라이팅
- **Advanced Slides**: Marp 호환 발표 자료

### 3.3 모바일 워크플로우
- **iOS**: 즉시 캡처는 Drafts → Shortcuts로 vault `Inbox.md`에 append. Working Copy로 GitHub 동기화.
- **Android**: Fleeting Notes 또는 Zettel Notes 별도 앱 → Obsidian Sync/Git 동기화.
- **공통 패턴**: Obsidian 모바일 앱 cold start 시간(4~6초) 때문에 **별도 캡처 앱 + 저녁에 Obsidian으로 정리** 워크플로우가 보편적.

### 3.4 공개된 Vault 사례 (영감용)
- **Andy Matuschak's notes** (notes.andymatuschak.org) — evergreen notes 원형
- **Bryan Jenks** (50만+ 영상) — Obsidian + Zotero + Raindrop.io 종합 워크플로우
- **MolecularNotes** (GitHub: robertmartin8) — 정량 분석가의 Obsidian Second Brain
- **Obsidian-Zettelkasten-Starter-Kit** (GitHub: groepl) — 그대로 가져다 쓸 수 있는 vault 템플릿

---

## 4. 논쟁점·Pain Point

### 4.1 가장 흔한 실패 패턴 5가지 (커뮤니티에서 반복 확인)

1. **Collector's Fallacy** — "노트 쌓기 = 학습"이라는 착각
   - Nori Parelius: *"My Zettelkasten felt like a black hole that I was feeding, but getting nothing back from it."*
   - 해결책: 캡처 시간을 하루 30분으로 제한, 가공 1시간 확보. "한 시간 읽었으면 두 시간 가공" 휴리스틱.
2. **Tinkering Trap** — 플러그인 셋업에 더 많은 시간을 쓰기
   - HN Bccdee: *"It feels like the type of infrastructure envy that leads engineers to spin up a k8s cluster to serve a static website."*
   - 해결책: Daily Notes 3~4주 습관화 후 플러그인 추가.
3. **파편화 불안** — atomic note를 어디까지 쪼개야 하는가
   - Nori Parelius: *"My ideas more and more fragmented and difficult to express."*
   - 해결책: Bob Doto의 "한 노트 = 한 주장" 정의 채택.
4. **임계점 전 절망** — 200~500 노트 전에는 그래프 뷰가 무의미
   - 한국 클리앙 사용자: *"활용 효과를 느끼기까지 시간이 오래 걸리고, 노트가 상당히 축적되어야 효과가 나타난다."*
   - 해결책: 첫 3개월은 ROI 기대 금지. "글쓰기 마감"이 있는 사람만 진짜 가치를 안다.
5. **모바일 캡처 마찰** — Obsidian 모바일 cold start로 아이디어 휘발
   - 해결책: 외부 캡처 앱(Drafts, Fleeting Notes) + Obsidian 동기화 분업.

### 4.2 핵심 논쟁 4건 (관점 보존)

#### 논쟁 A — MOC(Map of Content) vs 순수 Zettelkasten
- **관점 1 (LYT, Nick Milo):** 순수 Zettelkasten은 학자용. MOC로 80% 효과를 20% 노력에 얻는다.
- **관점 2 (Bob Doto):** MOC는 보조 도구. 핵심은 노트 사이 의미 연결. MOC에 의존하면 thinking이 organizing으로 변질.
- **책에서의 입장 제안:** 임계점(200+ 노트) 이전에는 MOC 불필요. 그 이후 점진적 도입.

#### 논쟁 B — AI가 Zettelkasten의 본질을 해치는가
- **관점 1 (회의론):** *"Using AI for thinking activities is like using a motorcycle during training for a marathon."* 노트 쓰기 자체가 사고이므로 AI에 맡기면 사고가 사라진다.
- **관점 2 (활용론):** AI는 캡처·요약·검색에 쓰고, 사고와 연결은 사람이 한다 (NotebookLM 패턴).
- **관점 3 (반-Zettelkasten, HN bad_username):** *"Raw, unstructured notes work excellently with LLM agents using search."* AI 시대엔 정교한 조직화가 오히려 불필요할 수 있다.
- **책에서의 입장 제안:** 의도적 분업 — AI는 캡처·요약·연결 추천, 사람은 atomic claim 결정과 영구 노트 작성.

#### 논쟁 C — PARA vs Zettelkasten (Forte vs Ahrens)
- **합의점:** *"BASB is a system for resource management while the Zettelkasten Method is a method for working with ideas themselves."* 둘은 다른 층위.
- **충돌점:** PARA는 카테고리·검색에 의존해 1만 노트에서 무너진다는 비판.
- **책에서의 입장 제안:** PARA는 프로젝트/자료, Zettelkasten은 학습/글쓰기. 한 vault에서 폴더로 분리.

#### 논쟁 D — Obsidian 플러그인 의존이 위험한가
- **관점 1:** 플러그인 abandonment, 보안 리스크가 누적된다.
- **관점 2:** 마크다운 파일이라 Logseq·Foam으로 언제든 이동 가능. *"recreating Obsidian's linking functionality would take a few hours for motivated developers."*
- **책에서의 입장 제안:** 핵심 워크플로우는 코어로만, 플러그인은 "없어도 되는 가속기" 위치.

### 4.3 폴더 vs 태그 vs 링크 (실용 가이드)
커뮤니티 표준 분업 (Obsidian Forum 다수 합의):
- **폴더**: 노트 종류 구분 (Inbox / Permanent / Reference)에만. 주제별 폴더는 안티패턴.
- **태그**: 유형 메타데이터 (#fleeting, #literature, #project-x).
- **링크**: 내용 관계. 대부분의 의미는 여기에.

---

## 5. AI 도구 연동

### 5.1 통합 패턴 5가지

| 패턴 | 도구 | 워크플로우 |
|------|------|-----------|
| **임베딩 검색** | Smart Connections | vault 전체에 임베딩 → 작성 중 노트와 의미적으로 가까운 노트 자동 표시 |
| **노트 채팅** | Smart Chat / Copilot for Obsidian | "이 vault에 OAuth 관련해서 뭐가 있더라" 같은 질문에 vault 검색 + LLM 답변 |
| **외부 분석** | NotebookLM | vault Markdown을 Google Drive로 동기화 → NotebookLM에서 출처 추적 가능한 답변·팟캐스트 생성 |
| **MCP 직접 접근** | Claude Desktop + Obsidian MCP Tools | Claude가 vault 파일을 직접 읽고 쓸 수 있음 — Permanent note 생성을 Claude에게 위임 가능 |
| **Claude Code 통합** | Claudian (YishenTu/claudian) | Claude Code가 vault 안에서 "에이전트 협업자"로 동작 |

### 5.2 권장 사용 시나리오 (관점 2 활용론 기준)
1. **캡처 단계**: 음성 → Whisper → fleeting note로 자동 변환 (모바일에서 효과적)
2. **Literature 단계**: 긴 논문/영상을 NotebookLM에 업로드 → 질문으로 핵심 추출 → 자기 언어로 atomic note 작성
3. **연결 단계**: Smart Connections로 "내가 잊고 있던 관련 노트" 발견
4. **글쓰기 단계**: Claude/MCP로 여러 atomic note를 인용해 초안 작성 → 사람이 흐름·논리 검수

### 5.3 위험 신호
- "AI가 만든 atomic note를 그대로 저장" → Collector's Fallacy의 AI판
- "노트 사이 연결을 AI에게 맡김" → Zettelkasten의 본질(사람이 만드는 의미 연결)이 사라짐
- "AI hallucination이 영구 노트로 진입" → 검증되지 않은 정보가 시스템을 오염

### 5.4 한국에서의 부상
2024~2026 한국 미디어(디지털투데이, 청년개발자신문)에서 옵시디언은 "AI 코딩 시대의 지식 저장소"로 재발견되는 중. MCP/Claude Code 연동이 한국 개발자 사이에서 빠르게 퍼지고 있다.

---

## 6. 한국 개발자 맥락

### 6.1 한국 커뮤니티 특성
- **유료 회피 강함**: Obsidian Sync($4/월) 대신 Obsidian Git + GitHub Private 저장소가 표준.
- **단행본 문화**: 영어권은 블로그·유튜브 중심이지만 한국은 단행본 출간이 활발 — 『세컨드 브레인을 구축하는 제텔카스텐 & 옵시디언』(생산적생산자, 2024), 『옵시디언 with 클로드 코드』(2026 출간 예정) 등.
- **AI 통합 빠른 채택**: MCP·Claude Code 연동 사례가 영어권보다 빠르게 한국 개발자 블로그에 등장.

### 6.2 한국어 자료 핵심
| 자료 | 출처 | 특징 |
|------|------|------|
| 골든래빗 — 옵시디언+챗GPT로 제텔카스텐 구축하기 | goldenrabbit.co.kr (2024) | 한국 독자용 Smart Connections 셋업 |
| 옵시디언 GitHub 동기화 가이드 | clarit7.github.io, velog 다수 | iOS Working Copy, Android Termux 결합 |
| 송요창 — Obsidian으로 일감 관리하기 | medium.com/@totuworld | 한국 개발자 실무 통합 사례 |
| 디지털투데이 — AI 코딩 지식 저장소 | digitaltoday.co.kr (2024) | AI 컨텍스트 저장소로의 재발견 |
| 제텔카스텐 연구소 | zklab.kr | 한국어 커뮤니티 허브 |
| 클리앙 — 옵시디언으로 제텔카스텐 활용하기 | clien.net | 템플릿 공유 + 실사용 후기 |

### 6.3 한국 개발자에게 특히 유효한 패턴
1. **GitHub Private 저장소 + Obsidian Git** — 회사 보안 정책 대응에 유리, 비용 0
2. **개발 블로그(velog/티스토리) 직전 단계로 Permanent Note 활용** — 한국 개발자는 블로그 글이 곧 포트폴리오. atomic note → 블로그 글의 흐름이 자연스럽다.
3. **TIL 폴더와 Permanent 폴더 분리** — TIL은 학습 기록, Permanent는 자기 주장. 두 층위가 한국 개발자 문화에 잘 맞음.
4. **개발자 컨퍼런스 발표 준비에 활용** — atomic note 5~7개를 묶어 발표 1편 구성 (한국 개발자 컨퍼런스 발표 문화와 호응).

---

## 7. 참고문헌

### 학술 (papers.md 기반)
- Schmidt, J. F. K. (2016). *Niklas Luhmann's Card Index: Thinking Tool, Communication Partner, Publication Machine*. In Forgetting Machines (pp. 289–311). Brill. DOI: 10.1163/9789004325258_014
- Mueller, P. A., & Oppenheimer, D. M. (2014). The Pen Is Mightier Than the Keyboard. *Psychological Science*, 25(6), 1159–1168. DOI: 10.1177/0956797614524581
- Roediger, H. L., & Karpicke, J. D. (2006). The Power of Testing Memory. *Perspectives on Psychological Science*, 1(3), 181–210.
- Dunlosky, J., et al. (2013). Improving Students' Learning With Effective Learning Techniques. *Psychological Science in the Public Interest*, 14(1), 4–58.
- Bangert-Drowns, R. L., Hurley, M. M., & Wilkinson, B. (2004). The Effects of School-Based Writing-to-Learn Interventions: A Meta-Analysis. *Review of Educational Research*, 74(1), 29–58.
- Clark, A., & Chalmers, D. (1998). The Extended Mind. *Analysis*, 58(1), 7–19.
- Cepeda, N. J., et al. (2006). Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis. *Psychological Bulletin*, 132(3), 354–380.
- Luhmann, N. (1981). Kommunikation mit Zettelkästen. Ein Erfahrungsbericht. (영문 번역: zettelkasten.de)

### 단행본
- Ahrens, S. (2017). *How to Take Smart Notes*. CreateSpace.
- Doto, B. (2024). *A System for Writing*. New Old Traditions.
- Forte, T. (2022). *Building a Second Brain*. Atria Books.
- 생산적생산자 (2024). *세컨드 브레인을 구축하는 제텔카스텐 & 옵시디언*. 길벗.

### 핵심 웹 자료
- Zettelkasten 공식 사이트 — https://zettelkasten.de/introduction/
- Andy Matuschak's notes — https://notes.andymatuschak.org/Evergreen_notes
- Bob Doto — https://writing.bobdoto.computer/
- Bryan Jenks 2021 종합 워크플로우 — https://www.bryanjenks.dev/blog/my-2021-comprehensive-obsidian-zettelkasten-workflow
- Nicole van der Hoeven + Bob Doto — https://nicolevanderhoeven.com/blog/20250625-a-real-zettelkasten-workflow-in-obsidian/
- Ernest Chiang — Luhmann's Original Zettelkasten — https://www.ernestchiang.com/en/posts/2025/niklas-luhmann-original-zettelkasten-method/
- Collector's Fallacy — https://zettelkasten.de/posts/collectors-fallacy/
- Goodbye, Zettelkasten (Nori Parelius) — https://www.noriparelius.com/post/goodbye-zettelkasten/
- MOC vs Zettelkasten 토론 — https://forum.obsidian.md/t/mocs-vs-zettelkasten-an-80-20-approach-for-those-of-us-who-arent-luhmann/106518

### Obsidian 도구·플러그인
- Smart Connections — https://github.com/brianpetro/obsidian-smart-connections
- Obsidian-Zettelkasten-Starter-Kit — https://github.com/groepl/Obsidian-Zettelkasten-Starter-Kit
- Templater, Dataview, Periodic Notes, Excalidraw — Obsidian 커뮤니티 플러그인
- Claudian (Claude Code 통합) — https://github.com/YishenTu/claudian
- Obsidian MCP Tools — Claude Desktop ↔ vault 연동

### 한국어 자료
- 골든래빗 — 옵시디언+챗GPT 제텔카스텐 — https://goldenrabbit.co.kr/2024/06/17/...
- 디지털투데이 — AI 코딩 지식 저장소 옵시디언 — https://www.digitaltoday.co.kr/news/articleView.html?idxno=656418
- 제텔카스텐 연구소 — https://www.zklab.kr/
- 옵시디언 GitHub 동기화 — https://clarit7.github.io/obsidian_sync_setting/
- 송요창 — Obsidian으로 일감 관리하기 — https://medium.com/@totuworld/...
- Jay's Blog — 옵시디언 사용기 — https://otzslayer.github.io/잡담/2023/02/01/using-obsidian-for-note-taking.html

### 커뮤니티 토론
- Hacker News "Zettelkasten method in Obsidian" — https://news.ycombinator.com/item?id=47700556
- Reddit r/ObsidianMD, r/Zettelkasten (스레드 다수, web search 결과 기반)
- Obsidian Forum — Folders vs Linking vs Tags — https://forum.obsidian.md/t/folders-vs-linking-vs-tags-the-definitive-guide/78468

---

## 리서치 한계 (커버하지 못한 영역)

1. **Reddit 본문 직접 fetch 미수행** — Reddit API 제한으로 검색 결과 스니펫과 외부 인용에 의존. 인용된 r/ObsidianMD·r/Zettelkasten 인사이트는 2차 소스 기반이므로 책 집필 시 필요하면 직접 재확인 권장.
2. **YouTube 영상 자막 미추출** — Bryan Jenks·Linking Your Thinking·Nick Milo 영상은 메타정보·블로그 요약본만 인용. 영상 내 구체 워크플로우 캡처는 챕터 집필 시 보강 필요.
3. **유료 강의 접근 안 함** — Nick Milo의 LYT, Bob Doto의 워크숍 등은 외부 리뷰·블로그만 참조.
4. **한국 디스코드/카톡 오픈채팅 비공개 채널 미접근** — 한국 사용자 raw voice는 공개 블로그·velog에 한정.
5. **Reddit·HN 외 영어 커뮤니티 (Lobste.rs, dev.to 일부)** 부분만 수집 — 추가 검색 가능.
6. **언어 비중 편향**: 영어 약 75% / 한국어 약 25%. 한국 독자 대상이지만 자료 자체는 영어가 우세 — 한국어 자료가 부족한 영역(예: AI 통합 사례)은 책에서 영어 자료를 한국 독자용으로 재해석 필요.
7. **PKM 자체의 학술 연구 미성숙** — Wikipedia에서도 인정하듯 "under-researched". Zettelkasten 효과를 RCT로 검증한 연구는 사실상 없음. 책에서는 인접 분야(testing effect, writing-to-learn 등)의 증거를 빌려와 간접 정당화하는 접근 필요.
8. **AI + PKM 학술 연구 emerging** — 2024~2026 출간된 학술 논문은 거의 없음. 블로그·실무 사례 위주.

> 이 한계를 알고 책을 쓸 때, **불확실한 지점은 "현재 합의 부족"으로 명시**하고 사용자가 자기 환경에서 실험하도록 유도하는 톤이 적절하다.
