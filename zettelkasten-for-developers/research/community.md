# 커뮤니티 리서치: 개발자 커뮤니티에서의 Zettelkasten·Obsidian 실제 사용 경험

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "노트를 쌓기만 하고 다시 안 본다" — Collector's Fallacy
- 출현 예시:
  - Nori Parelius 블로그 (https://www.noriparelius.com/post/goodbye-zettelkasten/) — "My Zettelkasten felt like a black hole that I was feeding, but getting nothing back from it."
  - Zettelkasten Forum (https://forum.zettelkasten.de/discussion/172/the-collector-s-fallacy) — "pressing the 'copy' button is immediately rewarded with copied paper" (수집 행위 자체가 보상을 줘서 학습 착각을 만든다)
  - HN 47700556 — Bccdee: "It feels like the type of infrastructure envy that leads engineers to spin up a k8s cluster to serve a static website."
- 추정 원인: 캡처는 쉽고 가공은 어려운 비대칭. 도구가 풍부할수록 수집 한계비용이 0으로 수렴해 가공 작업이 밀린다. 검증 필요.

### 패턴 2: "플러그인 셋업에 더 많은 시간을 쓴다" — Tinkering Trap
- 출현 예시:
  - XDA Developers (https://www.xda-developers.com/if-had-to-start-using-obsidian-again-do-differently-from-the-start/) — "spending hours browsing the community plugins and installing anything that looked even remotely useful"
  - Obsidian Forum, "Obsidian Plugins You Don't Need" — 80%의 사용자가 코어 기능만으로 충분한데 외부 플러그인 의존성에 시간을 빼앗긴다는 다수 의견
- 추정 원인: 개발자 본능이 "최적화"를 향하지만 노트 시스템에서 그 본능은 산출(글쓰기)을 늦춘다. 검증 필요.

### 패턴 3: "atomic note 한 개를 어디까지 쪼개야 하는가" — 파편화 불안
- 출현 예시:
  - Nori Parelius — "My ideas more and more fragmented and difficult to express."
  - Zettelkasten Forum 다수 스레드 — "이 두 노트를 합쳐야 하나? 분리해야 하나?" 끝없는 메타 토론
- 추정 원인: 원자성의 정의가 명확하지 않음. Bob Doto는 "한 노트 = 하나의 주장(claim)"으로 정의하지만, Ahrens는 "한 아이디어"로 더 모호하게 정의.

### 패턴 4: "처음 수개월 동안 효과가 안 느껴진다"
- 출현 예시:
  - 클리앙 한국 사용자 후기 (https://www.clien.net/service/board/lecture/16752664) — "활용의 효과를 느끼기까지 시간이 오래 걸리고, 노트가 상당히 축적되어야 제대로 된 효과가 나타난다"
  - HN 38711029 — 다수가 "수백 개 노트가 쌓이기 전에는 그래프 뷰가 의미 없다"고 토로
- 추정 원인: 네트워크 효과 — 연결의 가치는 노드 수의 제곱에 비례. 임계점(보통 200~500 노트) 전에는 ROI가 거의 0.

### 패턴 5: "모바일에서 캡처가 너무 느리다"
- 출현 예시:
  - Obsidian Forum (https://forum.obsidian.md/t/a-workflow-to-quickly-capture-ideas-on-mobile/55207) — Obsidian 모바일 앱 cold start가 4~6초 → 아이디어 휘발
  - 다수 사용자가 Drafts(iOS) / Fleeting Notes(Android)를 별도 캡처용으로 사용 후 동기화
- 추정 원인: Obsidian 모바일은 vault 인덱싱 비용 때문에 즉시성이 떨어짐.

## 실무 휴리스틱

### 휴리스틱 1: "Daily Notes를 3~4주 습관으로 잡은 후에 플러그인을 추가하라"
- 출처: Sébastien Dubois (https://www.dsebastien.net/the-must-have-obsidian-plugins-for-2026/), Bryan Jenks 다수 영상
- 원문:
  > "Add Templater and Dataview after your basic daily notes habit is solid—usually after 3-4 weeks of consistent daily notes, rather than starting with all plugins at once."
- 추천 동조 반응: HN, Reddit 다수 스레드에서 "그렇게 했어야 했다"는 후회담 반복.

### 휴리스틱 2: "한 시간 캡처하면 두 시간 가공하라"
- 출처: Zettelkasten Forum, Bryan Jenks
- 원문:
  > "For every hour of reading, it can take up to double the time to take proper notes."
- 함의: 캡처 시간을 하루 30분으로 제한하면 가공 1시간을 확보할 수 있다.

### 휴리스틱 3: "atomic note 제목은 API처럼 짓는다 (Andy Matuschak)"
- 출처: https://notes.andymatuschak.org/Evergreen_notes
- 원문:
  > "Evergreen note titles are like APIs."
- 의미: 제목만 보고도 무슨 주장인지 알 수 있어야 한다. "OAuth 정리" (×) → "OAuth refresh token은 access token보다 긴 수명을 가진다 (×)" — 후자처럼 주장 형태로 쓰라.

### 휴리스틱 4: "Inbox만 폴더로, 나머지는 flat"
- 출처: Matt Giaro (5,000+ 노트 운영자), groepl Starter Kit
- 원문:
  > "Start with a FLAT structure. Ditch folders... [but] it could be beneficial to have big categories to separate fleeting notes (the inbox) from permanent notes."
- 추천 동조 반응: r/ObsidianMD에서 가장 자주 추천되는 출발점.

### 휴리스틱 5: "외부 캡처 앱 + Obsidian = 마찰 최소화"
- 출처: Obsidian Forum 다수, https://www.fleetingnotes.app/
- 패턴: iOS는 Drafts → Shortcuts → vault inbox.md에 append. Android는 Fleeting Notes / Zettel Notes 앱.

## 논쟁점

### 논쟁 A: MOC(Map of Content) vs 순수 Zettelkasten
- 출처: https://forum.obsidian.md/t/mocs-vs-zettelkasten-an-80-20-approach-for-those-of-us-who-arent-luhmann/106518
- 관점 1 (80/20 MOC파, Nick Milo의 LYT 진영): 순수 Zettelkasten은 학자용. 실무자는 MOC로 80% 효과를 얻을 수 있다.
  - 대표 발언: "linking too much can create unnecessary noise"
- 관점 2 (순수 Zettelkasten파, Bob Doto): MOC는 보조 도구일 뿐, 핵심은 노트 사이의 의미 있는 연결. MOC에 의존하면 thinking이 아니라 organizing이 된다.
  - 대표 발언: "we're establishing relationships between ideas in an effort to make meaning and establish depth"
- 책에 어떻게 담을까: "양쪽 다 정답이 아니다. 단, MOC는 임계점(200+ 노트) 이전에는 불필요하다"는 절충안.

### 논쟁 B: AI가 Zettelkasten의 본질을 해치는가
- 출처: https://forum.zettelkasten.de/discussion/2658/, https://forum.zettelkasten.de/discussion/3454/ai-augmented-zettelkasten
- 관점 1 (AI 회의론): 노트를 쓰는 행위 자체가 사고이고, AI에게 맡기면 그 사고가 사라진다.
  - 대표 발언: "Using AI for thinking activities is like using a motorcycle during training for a marathon"
- 관점 2 (AI 활용론): AI는 캡처·요약·검색 단계에 쓰고, 사고와 연결은 사람이 한다. NotebookLM이 좋은 예.
  - 대표 발언: "Use AI to expand understanding or refine grammar when writing in a non-native language"
- 관점 3 (Hacker News bad_username): "raw, unstructured notes work excellently with LLM agents using search" — AI 시대엔 오히려 정교한 조직화가 불필요할지 모른다는 반-Zettelkasten 입장.
- 책에 어떻게 담을까: 3관점 모두 보존. "AI 시대의 Zettelkasten"이라는 챕터에서 의도적 분업(AI는 캡처, 사람은 영구 노트)을 제안.

### 논쟁 C: PARA vs Zettelkasten (Tiago Forte vs Sönke Ahrens)
- 출처: https://forum.zettelkasten.de/discussion/72/, https://zettelkasten.de/posts/building-a-second-brain-and-zettelkasten/
- 관점 1: PARA는 자료 관리, Zettelkasten은 사고 도구. 둘은 충돌하지 않는다.
  - 대표 발언: "BASB is a system for resource management while the Zettelkasten Method is a method for working with ideas themselves."
- 관점 2: PARA는 검색·범주에 의존해 확장성이 없다. 1만 개 노트에서 PARA는 무너진다.
  - 대표 발언: "BASB relies on categories and global search which don't scale, whereas the Zettelkasten Method uses breadcrumbs and structure notes with links."
- 책에 어떻게 담을까: PARA는 프로젝트 관리에, Zettelkasten은 학습·글쓰기에 분리해 쓰라고 권하는 절충안.

### 논쟁 D: Obsidian이 너무 무거워졌다 vs 강력해졌다
- 출처: https://www.xda-developers.com/obsidians-reliance-on-plugins/
- 관점 1: 플러그인 의존이 심해서 abandoned plugin 리스크와 보안 리스크가 누적된다.
  - 대표 발언: "The plugin model creates problems that compound over time: breakage, abandonment, security risks."
- 관점 2: 마크다운 파일은 어차피 vendor lock-in이 없으니 문제 없다. Logseq나 Foam으로 언제든 옮길 수 있다.
  - 대표 발언 (HN DocTomoe): "recreating Obsidian's linking functionality would take a few hours for motivated developers"

### 논쟁 E: Obsidian vs Logseq (개발자 관점)
- 출처: https://dev.to/dev_tips/obsidian-notion-logseq-the-note-taking-stack-that-doesnt-suck-for-devs-2cf7
- Obsidian 우위: 글 쓰기에 자연, 플러그인 1,500+, 그래프 뷰, 마크다운 호환성
- Logseq 우위: 완전 오픈소스(AGPL), 블록 단위 인용, 일일 노트 중심 워크플로우
- 책에 어떻게 담을까: "글을 쓰려면 Obsidian, 데일리 로깅 위주면 Logseq" 단순 가이드라인 제시

## 한국 커뮤니티 특이 패턴

### 패턴 K1: "유료 동기화 회피 → GitHub 동기화 보편화"
- 출처: https://clarit7.github.io/obsidian_sync_setting/, velog 다수
- 한국 사용자는 Obsidian Sync(월 $4) 대신 Obsidian Git + Private GitHub 조합이 표준.
- iOS는 Working Copy(유료 1회) + Shortcuts. Android는 Termux + cron.

### 패턴 K2: "토비 같은 시니어 개발자가 자기 stack 공개"
- 출처: 송요창 Medium, Jay's Blog (otzslayer.github.io)
- 일감 트래킹 + 학습 노트 + 회고를 한 vault에 통합한 한국형 사례 다수.

### 패턴 K3: "AI 코딩 시대의 옵시디언 부각"
- 출처: 디지털투데이 2024 보도, 청년개발자신문 2026 보도
- 한국에서는 옵시디언이 "AI에게 컨텍스트를 주는 도구"로 재발견됨. MCP/Claude Code 연동이 한국 개발자 사이에서 빠르게 퍼지는 중.

## 성공 패턴 (다수의 베테랑이 공유하는 진단)

1. **첫 노트는 "왜 이 노트가 존재하는가"로 시작한다** — Bryan Jenks
2. **Permanent note는 일주일 후에도 같은 의미로 읽혀야 한다** — Andy Matuschak
3. **글쓰기 마감이 있는 사람만 Zettelkasten의 진짜 가치를 안다** — Bob Doto, Sönke Ahrens 모두 합의
4. **백링크 패널을 항상 띄워둔다** — Obsidian의 가장 저평가된 기능 (HN 다수)
5. **태그는 "유형"에 (#permanent, #fleeting), 링크는 "내용"에** — 커뮤니티 표준 분업

## 실패 패턴

1. 시작부터 PARA + Zettelkasten + Johnny Decimal 등 여러 시스템을 병행
2. 플러그인 30개 이상 깔고 셋업에 한 달 사용
3. 책 한 권을 통째로 옮겨 적기 (Literature note ≠ 발췌집)
4. 백링크 없는 노트가 vault의 80% 이상
5. 모바일에서 캡처를 시도하다 포기 (Obsidian 직접 → 결국 메모앱으로 회귀)

## 수집 한계
- 한국 디스코드/오픈채팅 비공개 채널 미접근
- Reddit 본문은 검색 결과 스니펫만 수집, 직접 fetch 미수행 (Reddit API 제한)
- GitHub Discussions의 obsidian-tasks·dataview 별도 fetch 미수행
- 영어 비중이 압도적 (영어 80% / 한국어 20%)
