# 웹 리서치: Zettelkasten을 Obsidian으로 일상에 적용하는 방법 (개발자 대상)

## 자료 1: Introduction to the Zettelkasten Method (zettelkasten.de)
- 출처: https://zettelkasten.de/introduction/
- 저자·날짜: Sascha Fast, 운영 중 (장기 업데이트)
- 신뢰성: 최상 (분야 정전 사이트)
- 핵심 주장: Zettelkasten은 "외부 사고 파트너(communication partner)"로서, 노트 사이의 의미 있는 연결이 가치를 만든다. 폴더가 아니라 링크와 인덱스(엔트리 포인트)가 노트를 surfable하게 만든다.
- 인용 가능한 구절:
  > "He used his register as the place to start, serving as purely a list of entry points, not a tag list."
- 관련 섹션: 1, 2

## 자료 2: Niklas Luhmann's Original Zettelkasten — Two Slip Boxes (Ernest Chiang, 2025)
- 출처: https://www.ernestchiang.com/en/posts/2025/niklas-luhmann-original-zettelkasten-method/
- 저자·날짜: Ernest Chiang, 2025
- 신뢰성: 중상 (Schmidt 논문에 대한 정밀 요약)
- 핵심 주장: Luhmann은 통념과 달리 "두 개"의 슬립박스를 운영했다 — (1) 서지 정보용 카탈로그, (2) 사고 도구. 번호는 위계가 아니라 "사고 흐름의 분기"를 표시한다 (1, 1a, 1a1).
- 인용 가능한 구절:
  > "Luhmann maintained two independent slip box systems, each with different functions and structures."
- 관련 섹션: 1, 2

## 자료 3: How to Take Smart Notes (Sönke Ahrens) — 다수 요약본
- 출처: https://fortelabs.com/blog/how-to-take-smart-notes/, https://aliabdaal.com/book-notes/how-to-take-smart-notes/
- 저자·날짜: Tiago Forte, Ali Abdaal 등 (2018~2024)
- 신뢰성: 중상
- 핵심 주장: 노트는 세 종류 — Fleeting(빠른 캡처), Literature(원전 이해), Permanent(자기 언어로 재구성된 영구 노트). 영구 노트는 출처 맥락 없이도 이해 가능해야 하며, 베끼지 말고 "새로운 무언가"를 만들어야 한다.
- 인용 가능한 구절:
  > "Permanent notes are written in a way that can still be understood even when you have forgotten the context they are taken from."
  > "The aim is not to copy; it's to create something new."
- 관련 섹션: 1, 5(워크플로우)

## 자료 4: A Real Zettelkasten Workflow in Obsidian — Tris Oaten + Bob Doto (Nicole van der Hoeven, 2025)
- 출처: https://nicolevanderhoeven.com/blog/20250625-a-real-zettelkasten-workflow-in-obsidian/
- 저자·날짜: Nicole van der Hoeven, 2025-06
- 신뢰성: 최상 (현역 실무자 + Bob Doto 인터뷰)
- 핵심 주장: 코어 워크플로우만으로 충분하다 — 노트 만들기, [[link]]로 연결, 그래프로 탐색. Templater/Dataview/Calendar는 도움이 되지만 옵션이다. 폴더 위계 없이 flat 구조에서 시작하라.
- 관련 섹션: 3, 5(설치·설정)

## 자료 5: How to Use Obsidian as a Zettelkasten — The Ultimate Tutorial (Matt Giaro)
- 출처: https://mattgiaro.com/obsidian-zettelkasten/
- 저자·날짜: Matt Giaro, 2024
- 신뢰성: 중
- 핵심 주장: 폴더보다 링크가 우선이지만, "받은 편지함(Inbox)" 폴더, "Literature" 폴더처럼 노트 종류를 구분하는 폴더는 유용하다. 5,000+ 노트를 운영한 경험 기반.
- 인용 가능한 구절:
  > "Start with a FLAT structure. Ditch folders."
- 관련 섹션: 3, 4

## 자료 6: Smart Connections (GitHub: brianpetro/obsidian-smart-connections)
- 출처: https://github.com/brianpetro/obsidian-smart-connections, https://smartconnections.app/smart-chat/
- 저자·날짜: Brian Petro, 활발히 업데이트 중 (2024~2026)
- 신뢰성: 최상 (공식 저장소)
- 핵심 주장: AI 임베딩으로 의미적으로 비슷한 노트를 자동 추천하고, 노트와 함께 ChatGPT/Claude/Gemini로 채팅. Smart Chat는 별도 플러그인으로 분리됨. 무료 코어 + Pro 옵션.
- 인용 가능한 구절:
  > "Chat with your notes & see links to related content with AI embeddings. Use local models or 100+ via APIs like Claude, Gemini, ChatGPT & Llama 3."
- 관련 섹션: 5(AI 도구)

## 자료 7: Connect Claude AI with Obsidian (DEV Community)
- 출처: https://dev.to/sroy8091/connect-claude-ai-with-obsidian-a-game-changer-for-knowledge-management-25o2
- 저자·날짜: Suman Roy, 2024
- 신뢰성: 중
- 핵심 주장: Obsidian MCP Tools를 통해 Claude Desktop이 직접 vault에 접근 가능. Smart Connections 외에 Claude를 통합하는 또 다른 경로.
- 관련 섹션: 5

## 자료 8: I started using NotebookLM with Obsidian (XDA Developers)
- 출처: https://www.xda-developers.com/using-notebooklm-with-obsidian/
- 저자·날짜: XDA Developers, 2025
- 신뢰성: 중
- 핵심 주장: NotebookLM은 "분석", Obsidian은 "조직화"에 강점. 둘은 정반대 문제를 푼다. Google Drive 동기화로 vault → NotebookLM 자동 인덱싱 가능.
- 인용 가능한 구절:
  > "NotebookLM is great at analyzing materials and letting you interact with them but provides minimal organizational tools, while Obsidian is one of the best personal knowledge management tools."
- 관련 섹션: 5

## 자료 9: How I Use NotebookLM With Obsidian (wanderloots, 2025)
- 출처: https://wanderloots.xyz/digital-garden/tutorials/how-i-use-notebook-lm-with-obsidian-practical-note-taking-ai/
- 저자·날짜: wanderloots, 2025
- 신뢰성: 중
- 핵심 주장: NotebookLM에 원본 자료 업로드 → 질문으로 가공 → 답변을 atomic note로 분해해 Obsidian에 영구 저장하는 워크플로우.
- 관련 섹션: 5

## 자료 10: Andy Matuschak — Evergreen Notes
- 출처: https://notes.andymatuschak.org/Evergreen_notes
- 저자·날짜: Andy Matuschak, 진행 중
- 신뢰성: 최상
- 핵심 주장: 영구 노트(evergreen notes)의 5원칙 — 원자적, 개념 중심, 밀집 링크, 위계보다 연관, 자신을 위해 작성. Zettelkasten과 큰 틀은 같지만 spaced repetition 통합·공개 노트라는 두 차이가 있다.
- 인용 가능한 구절:
  > "Evergreen note titles are like APIs."
  > "Prefer associative ontologies to hierarchical taxonomies."
- 관련 섹션: 1, 2

## 자료 11: Misconceptions About Permanent & Evergreen Notes (Bob Doto)
- 출처: https://writing.bobdoto.computer/misconceptions-about-the-relationship-between-permanent-and-evergreen-notes/
- 저자·날짜: Bob Doto, 2024
- 신뢰성: 최상 (현역 실무자, A System for Writing 저자)
- 핵심 주장: Evergreen note ≠ permanent note. Evergreen은 지속적으로 갱신·재작성, permanent는 "더 이상 손대지 않는 완성형"이라는 차이 — 같은 슬립박스라도 두 작업 방식이 충돌할 수 있다.
- 관련 섹션: 2

## 자료 12: Bryan Jenks — Comprehensive Obsidian Zettelkasten Workflow (2021)
- 출처: https://www.bryanjenks.dev/blog/my-2021-comprehensive-obsidian-zettelkasten-workflow, https://www.youtube.com/watch?v=wB89lJs5A3s
- 저자·날짜: Bryan Jenks, 2021
- 신뢰성: 최상 (영상 50만 회 이상, 커뮤니티 정전)
- 핵심 주장: 입력 종류별(논문·기사·유튜브·팟캐스트·책)로 처리 워크플로우를 분리. Zotero, Raindrop.io, Airr를 캡처 단계에 사용하고, Obsidian은 가공·연결만 담당.
- 관련 섹션: 3, 5(워크플로우)

## 자료 13: Best Obsidian Plugins for 2026 (Sébastien Dubois)
- 출처: https://www.dsebastien.net/the-must-have-obsidian-plugins-for-2026/
- 저자·날짜: Sébastien Dubois, 2026
- 신뢰성: 중상
- 핵심 주장: 플러그인 추천 — Templater, Dataview, Periodic Notes, Excalidraw, Smart Connections, QuickAdd. "Daily notes 습관을 3~4주 만든 후" 플러그인을 추가하라는 단계적 도입 권장.
- 관련 섹션: 3, 5

## 자료 14: Using Obsidian as an ADR Tool (Matteo Paoli, Medium)
- 출처: https://medium.com/@mttpla/using-obsidian-as-an-adr-tool-5f63d187de6b
- 저자·날짜: Matteo Paoli, 2024
- 신뢰성: 중
- 핵심 주장: 아키텍처 의사결정 기록(ADR)을 Obsidian + Git에 저장. MADR 템플릿 + Templater 자동화 + 백링크로 결정의 맥락·결과를 연결.
- 관련 섹션: 3(개발자 적용 사례)

## 자료 15: Obsidian-Zettelkasten-Starter-Kit (GitHub: groepl)
- 출처: https://github.com/groepl/Obsidian-Zettelkasten-Starter-Kit
- 저자·날짜: groepl, 활발 업데이트
- 신뢰성: 최상 (스타 1.5k+)
- 핵심 주장: Fleeting/Literature/Permanent 노트 템플릿, MOC 템플릿, 일일 노트 템플릿, Dataview 쿼리를 패키징한 vault 시작 키트.
- 관련 섹션: 3

## 자료 16: 옵시디언+챗GPT로 제텔카스텐 구축하기 (골든래빗, 2024)
- 출처: https://goldenrabbit.co.kr/2024/06/17/obsidian-옵시디언챗gpt로-제텔카스텐-구축하기-오픈ai-사용/
- 저자·날짜: 골든래빗 출판사, 2024-06
- 신뢰성: 중상 (출판사 공식 콘텐츠)
- 핵심 주장: 한국어 환경에서 Smart Connections + OpenAI API 키 설정 가이드. 한국 독자용으로 정리된 보기 드문 자료.
- 관련 섹션: 5, 6

## 자료 17: Obsidian으로 밀려오는 일감 관리하기 (송요창, Medium)
- 출처: https://medium.com/@totuworld/obisidian으로-밀려오는-일감-관리하기-119b51536e73
- 저자·날짜: 송요창 (한국 개발자), 2023
- 신뢰성: 중
- 핵심 주장: 한국 개발자가 일감·이슈 트래킹 + 학습 노트를 Obsidian으로 통합한 실전기. Daily Notes + 이모지 메타데이터 + 백링크.
- 관련 섹션: 6

## 자료 18: AI 코딩 지식 저장소로 뜨는 노트앱 '옵시디언' (디지털투데이, 2024)
- 출처: https://www.digitaltoday.co.kr/news/articleView.html?idxno=656418
- 저자·날짜: 디지털투데이, 2024
- 신뢰성: 중
- 핵심 주장: 한국에서 옵시디언이 "AI 코딩 시대의 지식 저장소"로 부상. MCP로 AI가 vault 직접 참조하는 사례 보도. 요구사항·아키텍처·프롬프트·결과를 폴더로 분리하는 한국형 사례.
- 관련 섹션: 6

## 자료 19: 옵시디언 GitHub 동기화 (clarit7, velog 등 다수)
- 출처: https://clarit7.github.io/obsidian_sync_setting/, https://velog.io/@rethinking21/Obsidian-git
- 저자·날짜: 한국 개발자 블로그, 2023~2024
- 신뢰성: 중
- 핵심 주장: Obsidian Sync(유료) 대신 Obsidian Git 플러그인 + GitHub Private 저장소로 무료 동기화. 모바일은 Working Copy(iOS) / Termux(Android) 결합.
- 관련 섹션: 3, 6

## 자료 20: 세컨드 브레인을 구축하는 제텔카스텐 & 옵시디언 (생산적생산자)
- 출처: https://product.kyobobook.co.kr/detail/S000213922160
- 저자·날짜: 생산적생산자, 2024 (한국어 단행본)
- 신뢰성: 최상
- 핵심 주장: 한국어로 출간된 첫 단행본 수준의 옵시디언+제텔카스텐 가이드. 메모 체계를 영구보관용·키워드·의견·주장·세컨드브레인 5단계로 분류.
- 관련 섹션: 6

## 수집 한계
- YouTube 영상 본문(자막) 추출은 미수행 — 채널 메타정보만 인용
- 한국 디스코드/카톡 오픈채팅 로그는 비공개라 미수집
- 유료 강의 콘텐츠 (Linking Your Thinking by Nick Milo, etc.)는 무료 소개 페이지만 확인
