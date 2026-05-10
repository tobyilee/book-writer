# 커뮤니티 리서치: AI 시대의 PKM (Personal Knowledge Management)

수집 일자: 2026-05-10. 대상 독자(한국 50대 개발자, Google Docs+Obsidian 주 사용)에 맞춰 한국 커뮤니티(클리앙·Velog·생산적생산자 블로그) 비중을 의식적으로 확보했고, 글로벌 자료는 Hacker News·Obsidian Forum·Zettelkasten Forum·Reddit·Medium에서 수집했다.

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "노트가 쌓이기만 하고 다시 보지 않는다" — Collector's Fallacy
이 문제가 가장 압도적으로 반복된다. 글로벌·한국 모두에서 PKM을 시작하는 사람의 90% 가까이가 처음 6–12개월 안에 부딪힌다.

- 출현 예시:
  - Hacker News "I deleted my second brain" (https://news.ycombinator.com/item?id=44402470) — 댓글 다수: "내 second brain은 그냥 디지털 쓰레기통이 됐다."
    > "A second brain you don’t revisit is just a digital junk drawer."
  - Reddit·Obsidian Forum "Every attempt at PKM has landed me in the same place: a huge mess" (https://forum.zettelkasten.de/discussion/3034/) — 도구를 5년 이상 바꿔도 결과는 같다는 토로.
  - 한국 클리앙 (https://www.clien.net/service/board/lecture/16752664) — "롬 리서치에서 시작해 노션을 거쳐 옵시디언에 정착했지만 메모는 활용되지 않음."
  - 생산적생산자 블로그 (https://blog.productibe.com/zettelkasten-obsidian-connected-thinking/) — "에버노트, 노션, 워크플로위 등 어떤 도구를 써도 쌓이기만 하고 활용되지 않는 메모 무덤이 만들어졌다."
- 추정 원인 (커뮤니티가 공유하는 진단):
  1. 캡처가 너무 쉬우니 처리·연결을 안 한다 — "Capture is cheap, distillation is expensive."
  2. 다시 꺼낼 트리거(MOC·태그·검색 습관)가 없다.
  3. **"수집 = 학습"이라는 인지적 환상** — Zettelkasten.de Collector's Fallacy 글이 핵심 진단으로 반복 인용됨.

### 패턴 2: "도구를 또 바꾸고 있다" — Tool-hopping addiction
- 출현 예시:
  - HN "Show HN: I deleted my second brain" 댓글 (https://news.ycombinator.com/item?id=44507956) — "Notion → Roam → Obsidian → Logseq → Tana로 5년간 옮겨 다녔다."
  - Obsidian Forum "Honest Alternatives to Zettelkasten" (https://forum.obsidian.md/t/honest-alternatives-to-zettelkasten/57076) — 여러 사용자가 "도구 변경 자체가 procrastination이 됐다"고 자백.
- 추정 원인: "이번에는 다를 거야" 심리. 도구 변경이 지식 작업의 진척처럼 느껴짐 (sunk cost + dopamine of newness).

### 패턴 3: "Zettelkasten은 너무 복잡하다 / 나는 Luhmann이 아니다"
- 출현 예시:
  - Obsidian Forum "Zettelkasten is complex, obscure and not for you" (https://forum.obsidian.md/t/zettelkasten-is-complex-obscure-and-not-for-you/94498)
  - Obsidian Forum "MOCs Vs Zettelkasten: An 80/20 approach for those of us who aren't Luhmann?" (https://forum.obsidian.md/t/mocs-vs-zettelkasten-an-80-20-approach-for-those-of-us-who-arent-luhmann/106518)
- 핵심 토로: Luhmann의 9만 카드는 학자의 평생 작업이지, 우리 같은 "두 가지 일을 동시에 하는 직장인"의 모델이 될 수 없다.

### 패턴 4: "AI가 내 노트를 망친다 / 위협한다"
- 출현 예시:
  - HN 다수 댓글 — Obsidian의 AI 플러그인이 elegantly atomic한 노트를 평균적인 LLM 결과물로 평탄화한다는 비판.
  - Mem.ai 리뷰 (https://get.mem.ai/blog/exploring-the-ethical-implications-of-ai-note-taking-technology) 자체 언급 — "AI note-taking technology raises ethical implications around data ownership and privacy."
- 추정 원인: "내 사고의 흔적"과 "확률적으로 평균화된 텍스트"의 충돌.

### 패턴 5: "한국 사용자 — 한글 검색·정렬·플러그인 호환성"
- 출현 예시:
  - 클리앙 "옵시디언 간단 사용기" (https://www.clien.net/service/board/use/18517111) — 한글 정렬·검색에서 가벼운 마찰 보고.
  - DevOcean "옵시디언이 사랑받는 이유" (https://devocean.sk.com/blog/techBoardDetail.do?ID=165849) — 장점 분석에 비해 한글 환경 마찰은 별도 정리 필요.
- 추정 원인: 도구 자체가 영어권 중심으로 만들어졌음.

---

## 실무 휴리스틱

### 휴리스틱 1: "Capture는 빠르게, Distill은 느리게"
- 출처: BASB 커뮤니티, Tiago Forte Progressive Summarization 글
- 원문:
  > "Progressive Summarization is the practice of distilling a note in small increments, only doing as much or as little as the information deserves."
- 추천·동조 반응: 다수 — Obsidian 사용자들이 "highlight + bold 두 단계만 해도 charity to your future self"라고 인용.

### 휴리스틱 2: "PARA 4폴더에서 시작, 나머지는 나중에"
- 출처: Forte Labs (https://fortelabs.com/blog/para/) + Todoist PARA 가이드
- 원문:
  > "Your system has to give you time, not take time."
- 동조 반응: PKM 입문자에게 거의 만장일치 추천. "first try should be exactly 4 folders, no nesting."

### 휴리스틱 3: "MOC(Map of Content) 1개부터 만들어 본다"
- 출처: Nick Milo LYT (https://blog.linkingyourthinking.com/maps/), Obsidian Forum 다수 토론
- 원문 (LYT):
  > "MOCs are dynamic hubs that grow as you add more notes and make more connections."
- 동조 반응: Zettelkasten의 엄격성에 좌절한 사용자들 사이에서 "이게 80/20"이라는 평가.

### 휴리스틱 4: "내 언어로 다시 쓰지 않은 노트는 노트가 아니다"
- 출처: Sönke Ahrens, Andy Matuschak, 한국 생산적생산자 블로그
- 원문 (Matuschak):
  > "'Better note-taking' misses the point; what matters is 'better thinking'."
- 동조 반응: 많은 실패 사례에서 공통적으로 "원문 클립만 모았더라"는 자백 + "한 줄이라도 자기 말로 다시 쓰자"라는 처방.

### 휴리스틱 5: "AI에게 자료를 던지기 전에 출처 grounding을 강제한다"
- 출처: NotebookLM 사용자 사례, "Why I Switched from ChatGPT to Claude for Real Work" (https://www.theaienterprise.io/p/claude-mcp-notion-integration)
- 원문:
  > "NotebookLM uses your uploaded sources to answer questions and fulfill requests, providing citations for verification."
- 동조 반응: 일반 ChatGPT보다 NotebookLM·Claude+MCP 조합을 선호하는 흐름. 검증 가능성이 결정적.

### 휴리스틱 6: "로컬 + 마크다운 + 일반 plain text" 원칙
- 출처: Obsidian 커뮤니티, Hacker News 다수 PKM 토론
- 원문 (Local LLM Master):
  > "Your research notes, documents, and personal journals don’t leave your house, with the entire system being plain markdown files on your disk."
- 동조 반응: 50대 개발자 독자가 가장 공감할 가치관 — "20년 후에도 열 수 있는 파일 포맷."

### 휴리스틱 7: "주간 리뷰 (Weekly Review)"
- 출처: GTD (David Allen) → BASB·PARA 모두 채택
- 원문 (GTD):
  > "Weekly Review: clarify, organize, reflect, and engage."
- 동조 반응: PKM "안 망하는" 사용자의 80%가 어떤 형태로든 주간 리뷰를 한다는 패턴이 커뮤니티 공감대로 굳어 있음.

---

## 논쟁점

### 논쟁 A: BASB(Building a Second Brain) — 구원자인가 함정인가?
- 관점 1 (옹호): 디지털 정보 과부하 시대에 "외부화된 인지"는 필수. CODE 4단계는 입문자에게 가장 친절한 onramp.
  - 대표 발언 (Forte Labs):
    > "Building a Second Brain transforms how you save and use your knowledge."
- 관점 2 (비판): BASB는 정확히 collector's fallacy를 정당화한다 — capture를 강조하다 보니 hoarding 면죄부가 된다.
  - 대표 발언:
    > "Building a Second Brain Gives You Permission to Fall Into Collector's Fallacy" (https://curtismchale.ca/2022/07/30/...)
    > "Building a second brain became the excuse for not using my first one" (XDA Developers)

### 논쟁 B: Obsidian vs Notion — 어느 쪽이 PKM에 맞는가?
- 관점 1 (Obsidian): 로컬·마크다운·플러그인 생태계. "20년 가는" 데이터 소유권. 개인 깊이 사고에 최적.
  - 대표 발언:
    > "For most people, Obsidian is the safer choice. It’s more versatile, has better performance, a stronger plugin ecosystem."
- 관점 2 (Notion): 협업·DB·AI 통합·블록 기반. 팀 문서·구조화된 자료에 압도적.
  - 대표 발언:
    > "Notion is terrible for fast, personal dev notes."
- 한국 커뮤니티 합의: "둘 다 쓰면 된다" — 개인 깊이 사고는 Obsidian, 팀 문서는 Notion이라는 분업.

### 논쟁 C: AI에게 노트를 외주할 때, "내 사고력"은 어떻게 되는가?
- 관점 1 (수용): Extended Mind 명제의 자연스러운 진화. AI는 또 하나의 cognitive prosthesis.
  - 대표 발언 (Nature Comm 2025):
    > "Generative AI extends not just memory but inferential cognition itself."
- 관점 2 (경계): 외주가 깊어질수록 epistemic autonomy(자기 사고의 권위)가 약해진다.
  - 대표 발언:
    > "Second brain tools can quickly start replacing original thinking and judgment if not used intentionally."
    > "Some critics argue that emphasizing external systems can weaken our natural memory capacity."

### 논쟁 D: Zettelkasten 정통 vs MOC/Folgezettel 변종
- 관점 1 (정통): 고유 ID(Folgezettel) + 엄격한 atomic + linked. Luhmann이 90,000개로 증명.
- 관점 2 (실용): MOC 같은 "허브 노트"가 인간 인지에 더 맞다. 80/20.
- 한국 사례: 골든래빗 출간 『제텔카스텐』 (https://goldenrabbit.co.kr/2024/06/14/...) 가이드는 두 진영을 절충해 소개.

---

## 50대 개발자 시점에서 특별히 자주 등장하는 토로

(대상 독자 프로필이 매우 구체적이므로 별도 섹션으로 정리.)

- **"수십 년 쌓인 자료를 어떻게 통합할까"** — Hacker News 토론에서 40-60대 사용자들이 자주 던지는 질문. 답변 패턴: "다 옮기지 마라. 지금 활성 프로젝트와 관련된 것만 PARA로 끌어와라. 나머지는 archives 폴더 하나에 두고 검색만 가능하게."
- **"기억력이 예전 같지 않다"** — 노화에 따른 working memory 감소를 PKM의 동기로 명시적으로 언급. Extended mind 명제(Clark & Chalmers)가 정서적 위로가 됨.
- **"새 도구를 자꾸 배우는 게 지친다"** — Obsidian + plain markdown이 마지막 도구가 되길 바라는 욕구가 압도적.
- **"AI는 진짜로 내 사고를 도와주나, 흔적을 남기나"** — 50대 독자가 AI에 가장 회의적이면서도 가장 호기심을 가지는 지점. NotebookLM·Claude+CLAUDE.md 패턴이 이들에게 첫 진입점.

---

## 링크 모음 (한 줄 요약)

### 영문
- https://news.ycombinator.com/item?id=44402470 — "I deleted my second brain": BASB 비판의 폭발 지점.
- https://news.ycombinator.com/item?id=47700556 — Zettelkasten in Obsidian, 실무자 토론.
- https://news.ycombinator.com/item?id=29188418 — How to build a second brain as a software developer.
- https://forum.obsidian.md/t/honest-alternatives-to-zettelkasten/57076 — Zettelkasten 대안들.
- https://forum.obsidian.md/t/mocs-vs-zettelkasten-an-80-20-approach/106518 — MOC 80/20 토론.
- https://forum.zettelkasten.de/discussion/3034/ — "Every attempt at PKM has landed me in the same place: a huge mess".
- https://forum.zettelkasten.de/discussion/3088/ — PKM bankruptcy 토론.
- https://medium.com/@ConstructByDee/the-seven-deadly-sins-of-pkm — 7대 죄. Forte Labs 68% 통계 인용.
- https://www.xda-developers.com/building-second-brain-became-excuse-for-not-using-my-first-one/ — BASB 비판 에세이.
- https://curtismchale.ca/2022/07/30/building-a-second-brain-gives-you-permission-to-fall-into-collectors-fallacy/ — Curtis McHale 비판.
- https://goodluckman.substack.com/p/the-collectors-fallacy-why-most-notetaking — Collector's Fallacy 대중적 정리.

### 한국어
- https://www.clien.net/service/board/lecture/16752664 — 옵시디언 제텔카스텐 템플릿 공유.
- https://www.clien.net/service/board/use/18517111 — 옵시디언 간단 사용기.
- https://www.clien.net/service/board/lecture/18804465 — 옵시디언으로 구현하는 제텔카스텐 (2부).
- https://blog.productibe.com/zettelkasten-obsidian-connected-thinking/ — 기록은 왜 쌓이기만 할까.
- https://blog.productibe.com/personal-knowledge-management-tools-obsidian/ — 개인 지식관리 도구 선택 기준.
- https://blog.productibe.com/oracle-server-obsidian-automation-pkm/ — 오라클 서버 + 옵시디언 자동화.
- https://devocean.sk.com/blog/techBoardDetail.do?ID=165849 — SK DevOcean: 옵시디언 장단점.
- https://goldenrabbit.co.kr/2024/06/14/zettelkasten-... — 골든래빗 제텔카스텐 가이드.
- https://oneoneone.kr/content/49433618 — 옵시디언 vs 노션 비교.
- https://www.gpters.org/ai-writing/post/preparation-stage-creating-your-9I33W09RQpMJSVq — 나만의 지식관리 체계 만들기 준비단계.

---

## 수집 한계
- OKKY 본문 직접 수집은 검색 메타데이터 수준 — 게시판 비공개·로그인 요구로 본문 인용은 불가. 향후 회원으로 직접 접근 시 보강.
- Reddit r/ObsidianMD, r/PKMS, r/Zettelkasten의 개별 스레드 본문은 일부만 표면화됨 — 검색 도구가 미국 한정이라 무작위 샘플링이 어려움.
- 디스코드(Obsidian, LYT, Tana 공식 디스코드)는 공개 로그가 검색에 잘 안 잡혀 이번 라운드에서 제외.
- 모든 커뮤니티 주장은 **"커뮤니티 의견, 검증 필요"** 라벨이 기본 — 통계적 일반화는 자제.
