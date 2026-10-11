# 웹 리서치: Karpathy "LLM Wiki" 패턴으로 만드는 회사 지식베이스 (Claude Agent SDK / Claude API 활용)

- 검색 시점: 2026-10-11
- 장르: tech-book / 대상 독자: Claude Code 등 에이전틱 코딩 도구를 쓰는 소프트웨어 개발자(한국어 독자)
- 범위: 공식 문서·릴리스 노트·엔지니어링 블로그·튜토리얼·GitHub 저장소·기술 뉴스. 논문(arXiv 등)과 커뮤니티 토론(HN/Reddit 상세)은 다른 리서처 담당 — 여기서는 웹 글에 인용된 범위까지만 적는다.
- 인용 규칙: 인용문은 원문 그대로(따옴표). 요약은 "핵심 주장"에만. 모든 자료에 발행일·"{버전}/{연도} 기준"을 적는다. 버전·API·수치는 공식 1차 소스를 우선했다.
- 신선도 주의: Claude 모델명·가격·SDK 버전은 2026-10 기준이며 빠르게 바뀐다. fact-checker는 본문 집필 시점에 공식 문서를 재확인할 것.

---

## A. 1차 소스: Karpathy의 gist와 그 반응

### 자료 1: LLM Wiki (karpathy gist, 원문 전문 확보)
- 출처: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (raw: https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/)
- 저자·날짜: Andrej Karpathy. gist 생성 2026-04-04(gist 페이지 메타, Revisions: 1). 2차 자료들은 "4월 2일 게시"로 적기도 함(Platformer/HackerNoon) — 트윗 vs gist 일자 혼동 가능, 본문에서는 "2026년 4월 초"로 쓰는 것이 안전. 별/포크 5,000+ (2026-10-11 기준).
- 신뢰성: 최상 (1차 소스; 본문 1,959단어, 로컬 저장본 확인)
- 핵심 주장: RAG는 질문마다 원문에서 지식을 다시 꺼내므로 축적이 없다. 대신 LLM이 raw 소스를 읽고 **영속적이고 상호 링크된 마크다운 위키**를 점진적으로 짓고 유지한다. 사람은 소싱·탐색·질문, LLM은 요약·교차참조·파일링·북키핑. 세 계층(raw sources / wiki / schema)과 세 연산(ingest / query / lint), 두 특수 파일(index.md / log.md). 의도적으로 추상적인 "idea file"이며, 에이전트에게 붙여 넣어 각자 구체화하라는 문서.
- 인용 가능한 구절 (원문 그대로):
  > "This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you."

  > "Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation."

  > "Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources."

  > "The knowledge is compiled once and then *kept current*, not re-derived on every query."

  > "**the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read."

  > "You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions."

  > "In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

  > "**Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do."

  > "**Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth."

  > "**The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely."

  > "**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain."

  > "**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages."

  > "Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision."

  > "**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. [...] The important insight: **good answers can be filed back into the wiki as new pages.**"

  > "**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search."

  > "**index.md** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. [...] When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure."

  > "**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep \"^## \\[\" log.md | tail -5` gives you the last 5 entries."

  > "A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. [qmd](https://github.com/tobi/qmd) is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool)."

  > "Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context."

  > "**Dataview** is an Obsidian plugin that runs queries over page frontmatter. If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists."

  > "The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free."

  > "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. [...] Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero."

  > "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

  > "The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. [...] The part he couldn't solve was who does the maintenance. The LLM handles that."

  > "This document is intentionally abstract. It describes the idea, not a specific implementation. [...] Everything mentioned above is optional and modular — pick what's useful, ignore what isn't."
- 관련 섹션: 1장(패턴 원전·용어 정의), 아키텍처 3계층, 연산 3종, index/log 규약, "~100 소스/수백 페이지" 스케일 한계(검색 도구 도입 시점), 팀 위키 활용 사례, Memex 역사 배경.

### 자료 2: gist 댓글란 — 파생 프로젝트와 비판 (2026-09~10 구간)
- 출처: 자료 1과 동일 gist의 Comments (offset 100000 이후 부분만 읽음; 앞부분 댓글은 미확인)
- 저자·날짜: 다수. 2026-09-29 ~ 2026-10-08
- 신뢰성: 중 (1차 댓글이지만 홍보성 댓글 섞임)
- 핵심 주장: 파생 구현이 계속 등장(Caspian UI 버전, Obelyth Cortex, IWE 연동, podcast-wiki 등). 가장 날카로운 비판은 "나중에 위키가 말해주는 걸 믿을 수 있느냐"와 "중복 페이지 생성"이라는 운영 실패.
- 인용 가능한 구절:
  > ShootJackal (2026-10-01, Obelyth Cortex v2.0.2): "The hard part of an LLM-maintained wiki is trusting what it tells you later."

  > HagaiHen (2026-10-08, podcast-wiki): "Extend, don't create. The default failure is near-duplicate pages." / "69 concept pages from 60 episodes so far, running unattended every few hours."

  > bg-numarqe (2026-10-05): "Karpathy's got the right idea — knowledge should compound instead of getting re-derived every session."
- 메모: 이 구간에는 Karpathy 본인의 답글 없음. 댓글란 앞부분(4~9월)은 미수집.
- 관련 섹션: 신뢰·검증 문제, 중복 페이지 방지 규칙("확장 우선"), 무인 스케줄 실행 사례.

### 자료 3: Casey Newton, "An LLM wiki changed how I work" (Platformer)
- 출처: https://www.platformer.news/karpathy-llm-wiki-journalism-productivity/
- 저자·날짜: Casey Newton, 2026-08-18
- 신뢰성: 중~최상 (유명 저널리스트의 1인칭 실사용기, 수치 포함)
- 핵심 주장: 기자가 Platformer 아카이브 전체를 시드로 Karpathy식 위키를 운용. 한 달 남짓 만에 1,440+ 페이지. 타임라인·개념 페이지가 취재에 실질 도움. 단점은 "거의 상시 유지보수"와 Claude의 압축적 문체.
- 인용 가능한 구절 (기사에서 발췌된 표현):
  > Karpathy 트윗 인용(2026-04): "Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest."

  > 규모: "More than 1,440 wiki pages." / Meta 페이지 "more than 12,000 words" · "more than 1,300 links to other wiki pages."

  > 유지보수: 위키는 "more or less constant maintenance"가 필요하고, Claude의 "hyper-compressed, borderline-unreadable house style" 때문에 스타일 재작성이 필요했다. 추천하기엔 "too specific" / "too clunky".
- 설정 메모: Claude Fable 5로 Karpathy식 위키 프롬프트 작성 → Ghostty 터미널에서 실행 → Obsidian 볼트 + Web Clipper + Claudian 플러그인으로 질의. (기사 요약, 인용 아님)
- 관련 섹션: 실사용 사례(페이지 수·링크 수 실측), 운영 비용(유지보수·문체 관리), 사람이 원문 재확인하는 human-in-loop 습관.

### 자료 4: GeekNews — "LLM-Wiki - LLM을 활용하여 개인 지식저장소 구축 하기"
- 출처: https://news.hada.io/topic?id=28208
- 저자·날짜: GN 요약(게시자 미표시), 2026-04경("6달전" 표시). 댓글 sudoeng(6달전), alfadur(3달전), kurthong(6달전)
- 신뢰성: 중 (뉴스 요약 + 커뮤니티 댓글; HN 의견은 GN⁺ 2차 요약)
- 핵심 주장: 한국어 요약이 원문 구조를 정확히 옮김. 댓글의 주된 우려는 (1) 위키 규모 폭증, (2) LLM이 위키를 반복 재작성하며 생기는 품질 누적 저하("모델 붕괴").
- 인용 가능한 구절:
  > "Andrej Karpathy가 최근 자신은 코드보다 개인 지식 저장소 구축에 토큰을 더 많이 쓰고 있다며, 이 LLM 기반 위키를 생성하기 위한 아이디어 가이드 파일을 공개"

  > "새 소스를 추가할 때 LLM이 내용을 읽고 기존 위키에 통합·교차 참조하며, 단일 소스 처리 시 10~15개 위키 페이지를 업데이트할 수 있음"

  > "위키 유지 관리의 핵심 장벽이었던 북키핑 비용을 LLM이 거의 0에 가깝게 낮춤으로써, 사람들이 포기하던 위키 관리 문제를 해결"

  > HN 의견(GN⁺ 요약): "이 접근이 결국 모델 붕괴(model collapse)로 이어질 것 같음." / "위키를 유지하려면 LLM이 매번 원본 대신 위키를 다시 읽어야 하고, 그 과정에서 2차 오류가 누적됨" / 회사 프로젝트 적용 결과 "새로운 형태의 기술 부채"

  > sudoeng: "ai가 점점 쌓여가는 위키 컨텍스트를 감당할 수 있을지는 아직 잘 모르겠네요."

  > alfadur: "Wiki 규모가 급격하게 불어나는 게 제일 큰 문제더라고요."
- 관련 섹션: 한국 독자 반응, 리스크 섹션(2차 오류 누적·규모 폭증), raw 소스 불변 원칙의 근거.

### 자료 5: GeekNews — "Retrieval as Reasoning - LLM Wiki가 RAG보다 나은 이유에 대한 실증 벤치마크"
- 출처: https://news.hada.io/topic?go=comments&id=32164 (원 논문: https://arxiv.org/abs/2605.25480 — 논문 상세는 paper-researcher 담당)
- 저자·날짜: 게시자 alfadur, 2026-08경("2달전" 표시)
- 신뢰성: 중 (논문의 한국어 요약 + 댓글; 수치는 논문 원문으로 대조 필요)
- 핵심 주장: 원문서를 양방향 링크 위키로 "컴파일"하고, 에이전트가 링크를 "순회"하며 답하는 방식이 청크 RAG보다 멀티홉 QA에서 앞선다는 벤치마크. ablation에서 순회 > 구조 > 교정 순으로 중요.
- 인용 가능한 구절:
  > "**컴파일**: 원문서를 양방향 링크가 걸린 위키 페이지로 변환 (검색하는 단위가 청크가 아니라 링크된 페이지)"

  > "멀티홉 QA 세 종류에서 기준 모델들보다 2.0~8.1 F1 앞섬"

  > "순회를 뺐을 때: −11.7 / −13.8 / −12.2 (가장 치명적)" / "위키 구조를 뺐을 때: −6.1 / −7.0 / −6.7" / "Error Book을 뺐을 때: −3.8 / −4.0 / −3.4"

  > 댓글 sajacaros: "검색 성능보다 유지보수가 더 걱정되더라고요."

  > 댓글 daydreamblend: "그런데 LLM이 관리를 하면 RAG보다는 비결정론적이기에 모델마다 성능이 크게 달라질 거 같은데 이 문제는 어떻게 다뤘을지 궁금하네요"
- 관련 섹션: "왜 링크된 페이지가 청크보다 나은가" 근거, 비결정성 리스크. 수치는 (사실 확인 필요: 논문 원문 대조).

### 자료 6: 클리앙 팁과강좌 — LLM 위키 vs RAG 500+ 메모 실측
- 출처: https://www.clien.net/service/board/lecture/19182891
- 저자·날짜: 카일라스, 2026-04-26
- 신뢰성: 중 (개인 실측기, 수치 있음)
- 핵심 주장: 500개 넘는 개인 메모로 LLM 위키와 RAG(NotebookLM)를 비교. 성능은 비슷, 구현은 위키가 단순. 단점은 느림(등록 20분+).
- 인용 가능한 구절:
  > "LLM wiki/RAG 둘 다 500 개가 넘는 메모를 처리하는데 별 부족함이 없었고 대부분 답변도 유사하게 나왔습니다."

  > "RAG 를 Agent 에 붙이기 위해 구현/설정/튜닝을 하는거 보다 LLM 위키를 사용하는 것이 간단하고 효율적"

  > "하지만 느림. 500+ 메모를 위키에 등록하는데 20분 넘게 걸림..."
- 관련 섹션: 한국 실사용 수치(500 메모·20분), 위키 vs RAG 선택 기준.

### 자료 7: GPTers — "AI 사서를 고용했습니다" 클로드 코드로 개인 LLM Wiki 만들기
- 출처: https://www.gpters.org/nocode/post/we-hired-ai-librarian-0l2pOuNs3RSkWFx
- 저자·날짜: 비케이, 2026-05-27
- 신뢰성: 중 (한국 실사용기)
- 인용 가능한 구절:
  > "원본 자료는 건드리지 않고, 클로드가 사서처럼 지식을 정리·연결·유지보수하는 구조입니다."

  > "CLAUDE.md에 명령어 체계를 정의했습니다."

  > "클로드 코드 CLI 환경이 필요합니다 (웹 클로드로는 어려움)"

  > "wiki가 수백 페이지로 커지면 컨텍스트 관리 전략이 필요합니다"

  > "파일명에 특수문자가 섞여있으면 가끔 인코딩 이슈가 있습니다"

  > lint 결과 예시: "sources 경로 오류 4개 자동 수정" / "미처리 raw 파일 1개 발견" / "개념 페이지 stub 6개 제안"
- 관련 섹션: 한국어 파일명 인코딩 함정, lint 산출물의 구체적 형태, 수백 페이지 이후 컨텍스트 전략.

---

## B. 파생 구현 (GitHub)

### 자료 8: lucasastorian/llmwiki — "Open Source Implementation of Karpathy's LLM Wiki"
- 출처: https://github.com/lucasastorian/llmwiki
- 저자·날짜: Lucas Astorian 외. 2026-10-11 기준 ★1.7k, 포크 235, 커밋 185, Apache-2.0. 최종 커밋일 미표시(검색 요약은 "약 62일 전 활동")
- 신뢰성: 최상 (README 1차)
- 핵심 주장: MCP 서버 + 웹앱 + Chrome 확장. 야간 Claude Routine이 캡처물을 위키로 합성. `VaultFS` 추상화로 로컬(SQLite+파일시스템)/호스팅(Postgres+S3) 전환. 파일시스템이 진실의 원천, 검색 인덱스는 파생물. `lint` 도구는 결정론적 검사(인용 해상·dangling link·orphan·stale·frontmatter).
- 인용 가능한 구절:
  > "An autonomous, self-maintaining personal Wikipedia built and maintained by AI."

  > "The filesystem is the source of truth; the index just makes it fast to search."

  > "the wiki becomes a record of not just what you read but what you _thought_ about it."
- 도구 목록(README 요약): `guide`, `read`, `create`, `edit`, `append`, `delete`, `search`(브라우즈·전문검색·인용그래프·stale/uncited 조회), `lint`. 스택: Python 3.11+, Node 20+/Next.js, SQLite/Postgres+S3, Docker Compose, 선택적 LibreOffice·Mistral OCR.
- 관련 섹션: 호스팅 아키텍처(로컬→서버 전환), MCP로 지식 접근, 결정론적 lint 설계.

### 자료 9: Astro-Han/karpathy-llm-wiki — Agent Skills 호환 LLM 위키
- 출처: https://github.com/Astro-Han/karpathy-llm-wiki
- 저자·날짜: Astro-Han. ★2.5k, 커밋 28, MIT. "2026년 4월부터 매일 유지" (README)
- 신뢰성: 최상 (README 1차; 상세 규약은 SKILL.md 안에 있어 미열람)
- 핵심 주장: 패턴을 **Agent Skill 패키지**로 배포. Claude Code·Cursor·OpenCode는 `npx add-skill Astro-Han/karpathy-llm-wiki`, Codex CLI는 `.agents/skills/karpathy-llm-wiki/`에 복사. ingest(raw 수집→triage→생성/갱신/로그), query(인용 포함 답변), lint(index 무결성·링크·건강; 자동수정+보고).
- 디렉터리(README 그대로):
  ```
  your-project/
  ├── raw/          (immutable source material, organized by topic)
  ├── wiki/         (compiled knowledge pages maintained by the LLM)
  │   ├── topic/
  │   ├── index.md  (global table of contents)
  │   └── log.md    (append-only operation log)
  ```
- 관련 섹션: 스킬로 패키징하는 법, 멀티 에이전트 툴 호환(Claude Code/Codex/Cursor).

### 자료 10: julianoczkowski/karpathy-llm-wiki — 단계별 가이드 (Obsidian + Claude Code)
- 출처: https://github.com/julianoczkowski/karpathy-llm-wiki
- 저자·날짜: Julian Oczkowski, ★54, 커밋 3, © 2026
- 신뢰성: 중 (개인 가이드)
- 핵심 주장: 설치 절차(Obsidian 볼트 + `raw` 폴더 + Web Clipper 저장 위치를 `raw`로 + Claude Code 실행 + gist 붙여넣기). 수집은 소스당 5~15분. "수백 문서까지는 잘 되고, 그 이상은 임베딩+벡터DB RAG 권장".
- 인용 가능한 구절 (프롬프트 원문):
  > 설정: "You are my LLM Wiki agent. Build my complete second brain from this file."
  > 수집: "I just added a new file to raw. Please ingest it."
  > 점검: "Run a health check on the wiki" / "Run a lint on the wiki" / "What do I know about [topic]?"
- 관련 섹션: 입문 튜토리얼 절차, 소요시간 기대치, 스케일 분기점("수백 문서").

### 자료 11: HagaiHen/podcast-wiki — 무인 스케줄 수집 + 보안 격리 사례
- 출처: https://github.com/HagaiHen/podcast-wiki
- 저자·날짜: HagaiHen, MIT, 커밋 124 (2026-10)
- 신뢰성: 중 (소규모 저장소이지만 설계가 구체적)
- 핵심 주장: launchd로 6시간마다 headless Claude 실행(`tools/scheduled_ingest.sh`). **신뢰할 수 없는 트랜스크립트를 읽는 headless Claude는 `wiki/` 안에만 쓰고 git 명령을 못 돌리게** 하고, 커밋·푸시는 스크립트가 한다. `/lint-wiki`(깨진 링크·orphan·drift 수정), `/dream`(중복 개념 병합), `tools/lint_wiki.py`(기계적 검사만). 디렉터리: `wiki/{concepts,hubs,episodes,people,shows,takeaways}/ + index.md`.
- 관련 섹션: 야간 배치·무인 수집 설계, 프롬프트 인젝션 대비 권한 격리, 중복 병합 작업.

### 자료 12: tobi/qmd — 마크다운 로컬 하이브리드 검색 (Karpathy가 지명한 도구)
- 출처: https://github.com/tobi/qmd
- 저자·날짜: tobi (Tobias Lütke 계정). ★30.3k, 포크 1.9k, 커밋 781, MIT (2026-10-11 기준)
- 신뢰성: 최상 (README 1차)
- 핵심 주장: "mini cli search engine for your docs, knowledge bases, meeting notes, whatever." BM25 전문검색 + 벡터 검색 + LLM 재순위를 node-llama-cpp/GGUF로 온디바이스 실행. CLI(`qmd search`=BM25, `qmd vsearch`=벡터, `qmd query`=쿼리 확장+하이브리드+재순위, `get`, `multi-get`, `collection`, `context`, `embed`, `update`, `status`)와 MCP 서버(`query`, `get`, `multi_get`, `status`, `metadata`; stdio/HTTP).
- 버전/요건(README 기준): `npm install -g @tobilu/qmd` 또는 `bun install -g @tobilu/qmd`; Node.js 22+ 또는 Bun 1.0+; macOS는 Homebrew SQLite 필요(확장 지원). 자동 다운로드 모델: embeddinggemma-300M(~300MB), qwen3-reranker-0.6b(~640MB), qmd-query-expansion-1.7B(~1.1GB).
- 아키텍처 참고(mintlify 문서 https://mintlify.com/tobi/qmd/architecture/overview): SQLite FTS5(BM25) + sqlite-vec(벡터), ~900토큰 청크 15% 겹침.
- 관련 섹션: "index.md로 부족해질 때" 검색 계층, SQLite FTS5 + sqlite-vec 스택, MCP vs CLI 노출 비교.

### 자료 13: Blake Crosley — Obsidian 볼트용 하이브리드 리트리버 (FTS5 + 벡터 + RRF)
- 출처: https://blakecrosley.com/blog/hybrid-retriever-obsidian
- 저자·날짜: Blake Crosley, 2026 (정확한 일자 미확인)
- 신뢰성: 중 (개인 엔지니어링 글, 실측 수치)
- 핵심 주장: FTS5 BM25 + Model2Vec 벡터 + Reciprocal Rank Fusion. "16,894 files → 49,746 chunks, 83 MB". 권장: FTS5 가상 테이블(BM25만)부터 시작해 RRF는 마지막에. 주의: BM25는 키워드 밀도를 보상하므로 "잘 태깅된 얕은 문서가 깊은 문서를 이길 수 있음".
- 관련 섹션: 단계적 검색 고도화 로드맵(FTS5→벡터→RRF), BM25 편향 경고.

---

## C. Anthropic 공식: 컨텍스트 엔지니어링·검색·캐싱·긴 컨텍스트

### 자료 14: Anthropic Engineering — "Effective context engineering for AI agents"
- 출처: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 저자·날짜: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (기여: Rafi Ayub, Hannah Moran, Cal Rueb, Connor Jennings). 2025-09-29
- 신뢰성: 최상
- 핵심 주장: 컨텍스트 엔지니어링은 프롬프트 엔지니어링의 자연스러운 진화. 주의 예산(attention budget)과 context rot. 에이전트는 경량 식별자(파일 경로 등)만 들고 **just-in-time**으로 로드. Claude Code가 glob/grep로 탐색하는 것이 그 예. 압축(compaction)·구조화 노트(agentic memory)·서브에이전트 분리.
- 인용 가능한 구절:
  > 정의: "the set of strategies for curating and maintaining the optimal set of tokens (information)" (during inference)

  > "finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

  > "LLMs have an 'attention budget'" / "the concept of context rot" (recall accuracy falls as the context window grows)

  > "The right altitude is the Goldilocks zone between two common failure modes."

  > 에이전트는 "maintain lightweight identifiers (file paths, stored queries, web links, etc.)"를 유지하고 런타임에 로드; Claude Code는 "glob and grep"로 "navigate its environment and retrieve files just-in-time."

  > 자율 탐색은 "enables progressive disclosure" — 에이전트가 "incrementally discover relevant context through exploration."

  > "Compaction is the practice of taking a conversation nearing the context window limit..." / "Structured note-taking, or agentic memory, is a technique where the agent regularly writes notes..." / "specialized sub-agents can handle focused tasks with clean context windows."
- 관련 섹션: 왜 index.md + grep가 통하는가(just-in-time·progressive disclosure), 시스템 프롬프트 "고도" 설계, 서브에이전트로 위키 탐색 격리.

### 자료 15: Anthropic — "Introducing Contextual Retrieval"
- 출처: https://www.anthropic.com/news/contextual-retrieval
- 저자·날짜: Anthropic, 2024-09-19 (2024 기준 — 구버전 정보일 수 있음: 수치는 당시 Claude 3 계열 실험)
- 신뢰성: 최상 (수치는 1차)
- 핵심 주장: 청크에 문서 맥락 문장을 붙여 임베딩/BM25 하면 검색 실패율이 크게 준다. 지식베이스가 200K 토큰 이하면 RAG 없이 프롬프트에 통째로 넣고 캐싱하라.
- 인용 가능한 구절:
  > "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material)," — 전체를 프롬프트에 넣을 수 있음

  > "Contextual Embeddings reduced the top-20-chunk retrieval failure rate by 35%" (5.7% → 3.7%)

  > "Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49%" (5.7% → 2.9%)

  > "Reranked Contextual Embedding and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 67%" (5.7% → 1.9%)

  > "the one-time cost to generate contextualized chunks is $1.02 per million document tokens" (800토큰 청크·8k 문서 가정, 2024 가격)

  > "BM25 (Best Matching 25) is a ranking function that uses lexical matching to find precise word or phrase matches."

  > 청크 맥락 프롬프트: "Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else."
- 관련 섹션: "200K 이하면 검색 없이 통째로" 의사결정 기준, 하이브리드(BM25+임베딩) 근거, 위키 페이지에 맥락 요약 붙이기.

### 자료 16: Claude API 문서 — Prompt caching
- 출처: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used."

  > "You can specify a 1-hour TTL at 2x the base input token price."

  > "5-minute cache write tokens are 1.25 times the base input tokens price" / "1-hour cache write tokens are 2 times the base input tokens price" / "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)"

  > 각주: "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price." / "Cache hits and refreshes on Claude Opus 5.5 and Claude Sonnet 5.5 are priced at 0.05x the base input price."

  > 최소 캐시 길이: 512 토큰(Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, Fable 5, Mythos 5, Haiku 5.5) / 1,024 토큰(Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5 등) / 2,048 / 4,096 (구모델). "Shorter prompts cannot be cached, even if marked with `cache_control`."

  > 자동 캐싱: "Instead of placing `cache_control` on individual content blocks, add a single `cache_control` field at the top level of your request body. The system automatically applies the cache breakpoint to the last cacheable block." / "the automatic cache breakpoint uses one of the 4 available breakpoint slots."

  > usage 필드: `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens`
- 관련 섹션: 시스템 프롬프트+index.md+스키마를 캐시 접두사로 고정하는 비용 설계, 1시간 TTL로 야간 배치 수집 비용 절감.

### 자료 17: Claude API 문서 — Context windows (1M 컨텍스트)
- 출처: https://platform.claude.com/docs/en/build-with-claude/context-windows
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "A larger context window allows the model to handle more complex and lengthy prompts, but more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*. This makes curating what's in context just as important as how much space is available."

  > "Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Haiku 5.5, and Claude Mythos Preview have a 1M-token context window. A single request to any of them can generate up to 128k output tokens (`max_tokens`). Other Claude models, including Claude Sonnet 4.5 (deprecated), have a 200k-token context window."

  > "For every model with a 1M-token context window, 1M is the default: you don't need a beta header, and long-context requests are billed at standard pricing, except on Claude Haiku 5.5, where prompts over 100,000 tokens cost more."

  > "Everything in the request counts toward the context window: the system prompt, every message in `messages` (including tool results, images, and documents), and your tool definitions."

  > "Cached prompt prefixes still occupy the context window: prompt caching changes what you pay for those tokens, not whether they count."
- 메모: 2차 블로그들은 "2026-03-13 1M GA(Opus 4.6/Sonnet 4.6)"라고 적으나 1차 문서에서는 날짜 미확인 — 날짜 사용 시 (사실 확인 필요).
- 관련 섹션: "긴 컨텍스트 vs 검색" 선택 기준, 위키 전체를 한 번에 넣는 것의 한계(context rot).

### 자료 18: Claude API 문서 — Citations
- 출처: https://platform.claude.com/docs/en/build-with-claude/citations
- 저자·날짜: Anthropic 공식 문서, GA, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Ground Claude's responses in your source documents. Citations return the exact passages that support each claim, so you can verify answers and surface sources to your users."

  > "All active models support citations."

  > 활성화: document 블록에 `"citations": {"enabled": true}` (title·context 선택 필드)

  > "By default, plain text and PDF documents are automatically chunked into sentences. If you need more control over citation granularity (for example, for bullet points or transcripts), use custom content documents instead."

  > "if you want Claude to be able to cite specific sentences from your RAG chunks, you should put each RAG chunk into a plain text document. Otherwise, if you do not want any further chunking to be done, or if you want to customize any additional chunking, you can put RAG chunks into custom content document(s)."

  > "**Better citation reliability:** Because the API parses citations into the response formats described in the following sections and extracts `cited_text` directly, citations are guaranteed to contain valid pointers to the provided documents."

  > "Enabling citations incurs a slight increase in input tokens because of system prompt additions and document chunking." / "The `cited_text` field is provided for convenience and does not count toward output tokens." / "When passed back in subsequent conversation turns, `cited_text` is also not counted toward input tokens."

  > "Citations cannot be used together with structured outputs. If you enable citations on any user-provided document (`document` blocks or `search_result` blocks) and also include the `output_config.format` parameter [...] the API returns a 400 error."

  > citation 객체 예: `"type": "char_location"`, `"cited_text"`, `"document_index": 0`, `"start_char_index"` (0-indexed)
- 관련 섹션: 답변에 출처 강제하기(API 레벨), `search_result` 블록으로 자체 검색 결과 넘기기, 구조화 출력과의 상충.

### 자료 19: Claude API 문서 — Files API
- 출처: https://platform.claude.com/docs/en/build-with-claude/files
- 저자·날짜: Anthropic 공식 문서, GA(베타 헤더 불필요), 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Upload files once, reference them by file_id in Messages requests, and download outputs created by skills or the code execution tool."

  > "**Uploaded files are accessible to your entire workspace, not scoped to an end user, conversation, or session.** [...] Never accept `file_id` values from end users or other untrusted sources"

  > "If you are building a multi-tenant application on the Files API, create a separate workspace for each tenant. [...] Each organization can have up to 100 workspaces"

  > 한도: "**Maximum file size:** 500 MB per file" / "**Total storage:** 1 TB per organization" / 파일 API 호출 "approximately 500 requests per minute"

  > "Files cannot be modified or renamed after upload. To change a file's content, upload a new file and delete the old one"

  > 만료: `expires_in_seconds` 3,600(1시간)~7,776,000(90일)

  > "Files that are already plain text, such as .csv and .md files, can either be read in this way or uploaded through the Files API with an explicit `text/plain` content type."

  > "The Files API is out of beta and needs no beta header." (구 헤더 `files-api-2025-04-14` 제거 가능; SDK: Python 1.2.0, TypeScript 0.122.0 이후 `client.files`)

  > 과금: "Files API operations are free" / "File content used in Messages requests is priced as input tokens."
- 관련 섹션: 위키 페이지를 Files API로 올릴지 로컬 파일시스템으로 둘지, 멀티테넌트 격리(워크스페이스), 불변 파일 특성.

### 자료 20: Claude API 문서 — Memory tool
- 출처: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준 (tool type `memory_20250818`, Claude 4 이상 전 모델)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "The memory tool lets Claude store and retrieve information across conversations in a directory of memory files. [...] building up knowledge over time without keeping everything in the context window."

  > "The memory tool operates client-side: Claude requests file operations, and your application executes them. You control where and how the data is stored through your own infrastructure."

  > 설정: `{"type": "memory_20250818", "name": "memory"}` — "the `name` must be `memory`" ; 명령: `view`, `create`, `str_replace`, `insert`, `delete`, `rename`; 경로 접두사 `/memories`

  > 자동 주입 시스템 프롬프트: "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE. [...] ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory."

  > "A malicious path such as `/memories/../../secrets.env` can reach files outside the `/memories` directory. Your implementation must validate every path in every command to prevent directory traversal attacks."

  > 멀티세션 패턴: "Work on one feature at a time. Mark a feature complete only after end-to-end verification confirms it works, not when the code is written."
- 관련 섹션: 직접 API로 지을 때 "에이전트 메모리" vs "위키"의 구분, 경로 탐색 보안.

### 자료 21: Anthropic Engineering — "Effective harnesses for long-running agents"
- 출처: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 저자·날짜: Justin Young, 2025-11-26
- 신뢰성: 최상
- 인용 가능한 구절:
  > "each new session begins with no memory of what came before."

  > "an initializer agent that sets up the environment on the first run" / "a coding agent that is tasked with making incremental progress in every session"

  > "the claude-progress.txt file alongside the git history" / "edit this file only by changing the status of a passes field"

  > "leaving the environment in a clean state at the end of a session" — "By 'clean state' we mean the kind of code that would be appropriate for merging to a main branch"

  > "This incremental approach turned out to be critical to addressing the agent's tendency to do too much at once."
- 관련 섹션: 야간 ingest/lint 잡을 "세션 간 상태 파일(log.md)"로 이어가는 설계, 한 번에 한 소스 처리 원칙.

### 자료 22: Anthropic Engineering — "Demystifying evals for AI agents"
- 출처: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 저자·날짜: Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe. 2026-01-09
- 신뢰성: 최상
- 인용 가능한 구절:
  > "An **evaluation** ('eval') is a test for an AI system"

  > Task: "is a single test with defined inputs and success criteria." / "Each attempt at a task is a **trial**." / "A **grader** is logic that scores some aspect of the agent's performance."

  > "**Capability or 'quality' evals** ask, 'What can this agent do well?'" / "**Regression evals** ask, 'Does the agent still handle all the tasks it used to?'"

  > pass@k: "measures the likelihood that an agent gets at least one correct solution in _k_ attempts." / pass^k: "measures the probability that _all k_ trials succeed."

  > "Agent evaluations typically combine three types of graders: code-based, model-based, and human."

  > "20-50 simple tasks drawn from real failures is a great start."

  > "**Eval saturation** occurs when an agent passes all of the solvable tasks, leaving no room for improvement."
- 관련 섹션: 골든 Q&A 세트 설계(20~50개 실패 사례부터), "위키에 없음" 답변도 평가 항목에 포함, 회귀 평가 vs 역량 평가.

### 자료 23: Anthropic Engineering — "Equipping agents for the real world with Agent Skills"
- 출처: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- 저자·날짜: Barry Zhang, Keith Lazuka, Mahesh Murag. 2025-10-16 (2025-12-18 업데이트: Agent Skills 오픈 표준 발표)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "A skill is a directory containing a SKILL.md file"

  > 필수 frontmatter: "`name` and `description`" — 시작 시 모든 설치 스킬의 이 두 필드를 시스템 프롬프트에 preload

  > 3단계 progressive disclosure: (1) name/description 메타데이터 preload → (2) 관련하다고 판단되면 SKILL.md 본문 전체 로드 → (3) SKILL.md가 참조하는 추가 번들 파일을 필요할 때만 열람

  > 파일시스템과 코드 실행 도구가 있는 에이전트는 스킬 전체를 컨텍스트에 읽을 필요가 없으므로 번들 가능한 컨텍스트는 "effectively unbounded."

  > "Agent Skills are supported today across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Developer Platform."
- 메모: 2차 자료의 "SKILL.md 본문 5,000토큰/500줄 이하", "스킬당 메타 ~100토큰"은 이 글에 없음 — 사용 시 (사실 확인 필요).
- 관련 섹션: 위키 스키마(CLAUDE.md)와 스킬의 역할 분담, 위키 운영 절차(ingest/lint/query)를 스킬로 패키징.

---

## D. Claude Code / Agent SDK 공식 문서

### 자료 24: Claude Code 문서 — "How Claude remembers your project" (CLAUDE.md·AGENTS.md·rules·auto memory)
- 출처: https://code.claude.com/docs/en/memory
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준 (일부 기능은 Claude Code v2.1.2xx 이상 요구)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Each Claude Code session begins with a fresh context window. Two mechanisms carry knowledge across sessions: **CLAUDE.md files** [...] **Auto memory**: notes Claude writes itself based on your corrections and preferences"

  > "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."

  > 표: CLAUDE.md "Who writes it: You / What it contains: Instructions and rules" vs Auto memory "Who writes it: Claude / Loaded into: Every session (first 200 lines or 25KB)"

  > "Keep it to facts Claude should hold in every session: build commands, conventions, project layout, 'always do X' rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule instead."

  > "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."

  > "**Consistency**: if two instructions contradict each other, Claude may pick one arbitrarily."

  > "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch [...] Imported files can recursively import other files, with a maximum depth of four hops."

  > "Imports help you organize a long file but don't reduce its context cost, because imported files also load at launch."

  > 위치 표: Managed policy(`/Library/Application Support/ClaudeCode/CLAUDE.md` 등) / User(`~/.claude/CLAUDE.md`) / Project(`./CLAUDE.md` 또는 `./.claude/CLAUDE.md`) / Local(`./CLAUDE.local.md`, gitignore)

  > "CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand."

  > `.claude/rules/`: "Rules can also be scoped to specific file paths, so they only load into context when Claude works with matching files"

  > AGENTS.md: "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it." (v2.1.277+)

  > `/doctor prompt-audit`: "Claude looks for problems such as instructions written for older models, references to files or commands that don't exist, and files that contradict each other." (v2.1.283+)
- 관련 섹션: 위키 스키마 파일 작성 규칙(200줄, 구체적 지시, 모순 제거), 하위 디렉터리 CLAUDE.md로 raw/wiki 별 규칙 분리, AGENTS.md 호환.

### 자료 25: Claude Code 문서 — Best practices (CLAUDE.md 작성·검증·서브에이전트·배치)
- 출처: https://code.claude.com/docs/en/best-practices (구 URL https://www.anthropic.com/engineering/claude-code-best-practices 는 308 리다이렉트)
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."

  > "Keep it concise. For each line, ask: *'Would removing this cause Claude to make mistakes?'* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

  > 포함/제외 표: Include "Bash commands Claude can't guess", "Architectural decisions specific to your project", "Common gotchas" / Exclude "Anything Claude can figure out by reading code", "Information that changes frequently", "File-by-file descriptions of the codebase"

  > "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."

  > "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."

  > "Delegate research with 'use subagents to investigate X'. They explore in a separate context, keeping your main conversation clean for implementation."

  > 비대화 모드: "`claude -p \"your prompt\"`" / "`--output-format json`" / "`--output-format stream-json --verbose`"; 팬아웃 예: `claude -p "Migrate $file ..." --allowedTools "Edit,Bash(git commit *)" --permission-mode dontAsk`

  > "The over-specified CLAUDE.md. If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."

  > MCP 예: "`claude mcp add --transport http notion https://mcp.notion.com/mcp`"
- 관련 섹션: 스키마(CLAUDE.md) 작성 지침, 야간 lint를 `claude -p`로 CI에 거는 법, 위키 검증을 "실행 가능한 체크"로 만드는 원칙.

### 자료 26: Claude Agent SDK — Overview
- 출처: https://code.claude.com/docs/en/agent-sdk/overview
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준. 패키지 버전(1차 확인): PyPI `claude-agent-sdk` 0.2.165 (2026-10-08, Python ≥3.10, `pip install claude-agent-sdk`); npm `@anthropic-ai/claude-agent-sdk` 0.3.296 (2026-10-09, Node ≥18)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript."

  > 비교표: Agent SDK = "A library that runs the Claude Code binary, with Claude Code's capabilities, such as built-in tools, permissions, sessions, and hooks." / Client SDK = "You write the tool loop yourself, or let the client SDK's beta tool runner drive it." / Managed Agents = "A hosted agent harness that runs the agent loop, with sessions in an Anthropic-managed cloud sandbox"

  > 기능표: Built-in tools "Read, write, edit files, run commands, and search the web" / Hooks "Run custom code at key points in the agent lifecycle" / Subagents "Spawn specialized agents for focused subtasks" / MCP "Connect external tools and data sources via the Model Context Protocol" / Sessions "Maintain context across exchanges, resume or fork later" / Skills, commands, and memory "Load automatically from your project's `.claude/` and from `~/.claude/`, same as Claude Code"

  > "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods"
- 관련 섹션: "Agent SDK vs 직접 API" 선택 기준 장, 사내 서비스 인증(API 키).

### 자료 27: Claude Agent SDK — Subagents
- 출처: https://code.claude.com/docs/en/agent-sdk/subagents
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "**Context isolation**: each subagent runs in its own conversation [...] A `research-assistant` subagent can explore dozens of files without any of that content accumulating in the main conversation. The parent receives a concise summary, not every file the subagent read."

  > "**Tool restrictions**: subagents can be limited to specific tools [...] A `doc-reviewer` subagent might only have access to Read and Grep tools, ensuring it can analyze but never accidentally modify your documentation files."

  > AgentDefinition 필드: `description`(필수), `prompt`(필수), `tools`, `disallowedTools`, `model`, `skills`, `memory`('user'|'project'|'local'), `mcpServers`, `maxTurns`, `background`, `omitClaudeMd`, `effort`, `permissionMode`

  > "The only content you pass from parent to subagent is the Agent tool's prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt."

  > 한도 기본값: 깊이 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`=3, 동시 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`=20, 비용 `maxBudgetUsd`/`max_budget_usd` (TS v0.3.219 / Py v0.2.127 이후)

  > "Claude Opus 5 delegates to subagents more readily than earlier models, so the depth, concurrency, and spend limits matter most on queries that run Opus 5."
- Python 예(문서 그대로 일부):
  ```python
  from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
  async for message in query(
      prompt="Review the authentication module for security issues",
      options=ClaudeAgentOptions(
          allowed_tools=["Read", "Grep", "Glob", "Agent"],
          agents={"code-reviewer": AgentDefinition(
              description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
              prompt="...", tools=["Read", "Grep", "Glob"], model="sonnet")},
      )): ...
  ```
- 관련 섹션: 읽기 전용 "wiki-reader" 서브에이전트, ingest용 쓰기 서브에이전트 분리, 비용 상한.

### 자료 28: Claude Agent SDK — Sessions
- 출처: https://code.claude.com/docs/en/agent-sdk/sessions
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "A session is the conversation history the SDK accumulates while your agent works. [...] The SDK writes it to disk automatically so you can return to it later."

  > "Sessions persist the **conversation**, not the filesystem."

  > "**Continue** finds the most recent session in the current directory." / "**Resume** takes a specific session ID. [...] Required when you have multiple sessions (for example, one per user in a multi-user app)" / "**Fork** [...] creates a new session that starts with a copy of the original's history."

  > "Claude Code stores sessions under `~/.claude/projects/<encoded-cwd>/*.jsonl`."

  > "To resume sessions across machines or in serverless environments, mirror transcripts to shared storage with a `SessionStore` adapter."

  > "**Don't rely on session resume.** Capture the results you need [...] as application state and pass them into a fresh session's prompt. This is often more robust than shipping transcript files around."
- 관련 섹션: 사용자별 Q&A 세션 관리, 서버 배포 시 세션 저장소.

### 자료 29: Claude Agent SDK — Hooks
- 출처: https://code.claude.com/docs/en/agent-sdk/hooks
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Hooks are callback functions that run your code in response to agent events, like a tool being called, a session starting, or execution stopping."

  > 이벤트(Python+TS 공통): `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest`, `Notification`; TS 전용 다수(`SessionStart`, `SessionEnd`, `PostCompact`, `InstructionsLoaded`, `FileChanged` 등)

  > PreToolUse 출력: `permissionDecision` ("allow" | "deny" | "ask" | "defer"), `permissionDecisionReason`, `updatedInput`

  > "When multiple hooks or permission rules apply, `deny` takes priority over `defer`, which takes priority over `ask`, which takes priority over `allow`."

  > matcher: "MCP tools use the pattern `mcp__<server>__<action>`"

  > "`SessionStart` and `SessionEnd` can be registered as SDK callback hooks in TypeScript, but aren't available in the Python SDK"
- 예(문서 그대로, `.env` 쓰기 차단):
  ```python
  async def protect_env_files(input_data, tool_use_id, context):
      file_path = input_data["tool_input"].get("file_path", "")
      if file_path.split("/")[-1] == ".env":
          return {"hookSpecificOutput": {"hookEventName": input_data["hook_event_name"],
                  "permissionDecision": "deny", "permissionDecisionReason": "Cannot modify .env files"}}
      return {}
  options = ClaudeAgentOptions(hooks={"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]})
  ```
- 관련 섹션: raw/ 디렉터리 쓰기 금지 훅(불변성 강제), 모든 위키 편집 감사 로그(PostToolUse), 야간 잡 알림.

### 자료 30: Claude Code 문서 — MCP (서버 추가·스코프·.mcp.json)
- 출처: https://code.claude.com/docs/en/mcp
- 저자·날짜: Anthropic 공식 문서, 2026-10-11 열람 기준 (뒷부분 "tool search" 절은 미열람)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Claude Code can connect to hundreds of external tools and data sources through the Model Context Protocol (MCP), an open source standard for AI-tool integrations."

  > `claude mcp add --transport http <name> <url>` / `claude mcp add [options] <name> -- <command> [args...]` (stdio)

  > "HTTP servers are the recommended option for connecting to remote MCP servers." / "The SSE (Server-Sent Events) transport is deprecated."

  > "Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file at your project's root directory." / "For security reasons, Claude Code prompts for approval in interactive sessions before using project-scoped servers from `.mcp.json` files."

  > tool search: "[tool search], which is on by default"
- 관련 섹션: qmd/llmwiki 같은 지식 MCP 서버를 팀 공용 `.mcp.json`으로 배포, Notion MCP 연결.

---

## E. 저장·호스팅·발행·CI

### 자료 31: Quartz (Obsidian 볼트 정적 사이트 발행)
- 출처: https://quartz.jzhao.xyz/
- 저자·날짜: Jacky Zhao. 2026-10-11 기준 "Welcome to Quartz 5" / 푸터 "Created with Quartz v5.0.0"
- 신뢰성: 최상 (공식 문서)
- 인용 가능한 구절:
  > "Quartz is a fast, batteries-included static-site generator that transforms Markdown content into fully functional websites."
- 기능(문서 요약): backlinks, graph view, full-text search, wikilinks·transclusion, Obsidian 호환, LaTeX, popover 미리보기, Docker, i18n. 배포: GitHub Pages, Cloudflare, Netlify, Vercel. **인증/비공개 호스팅은 문서에 없음** — 사내용은 리버스 프록시/SSO 뒤에 두어야 함(별도 확인 필요). 커뮤니티 플러그인 "Private Quartz Publish"는 추측 불가 슬러그 방식(보안 아님).
- 관련 섹션: 사람이 읽는 뷰(Obsidian 로컬 vs Quartz 웹), 접근 제어는 별도 계층.

### 자료 32: Docusaurus vs Quartz vs Obsidian Publish (접근 제어 관점)
- 출처: https://www.wmtips.com/technologies/compare/docusaurus-vs-quartz , https://www.featurebase.app/blog/docusaurus-alternatives (경쟁사 글, 편향 주의)
- 저자·날짜: 2026 (정확 일자 미확인)
- 신뢰성: 하~중 (비교 사이트/벤더 글)
- 핵심 주장: 셋 다 네이티브 인증 없음. Docusaurus는 버전 관리·i18n·플러그인이 강점. 사내 위키는 결국 SSO 프록시(예: Cloudflare Access, oauth2-proxy) 뒤에 배치 — 이 부분은 검색에서 1차 소스 미확보 (사실 확인 필요).
- 관련 섹션: 발행 도구 선택표, 접근 제어는 앱이 아니라 인프라 계층.

### 자료 33: 마크다운 CI 린트 도구들 (markdownlint-cli2 · lychee · mdlint · wiki-lint)
- 출처: lychee-action (https://github.com/lycheeverse/lychee-action; 2.0.2 이전 코드 인젝션 취약점 패치됨), sidequery/mdlint (https://gitblind.noratr.app/sidequery/mdlint — Rust, backlink·wikilink·heading anchor·image 검증), claude-obsidian `wiki-lint` 스킬 (https://tessl.io/registry/skills/github/AgriciDaniel/claude-obsidian/wiki-lint)
- 저자·날짜: 각 저장소, 2026-10 기준
- 신뢰성: 중 (검색 요약 수준; 각 도구 README 직접 확인은 안 함)
- 핵심 주장: 범용 도구(markdownlint=스타일, lychee=외부 URL)는 `[[wikilink]]`·frontmatter를 모른다. 위키 전용 검사(dead/ambiguous link, orphan, 필수 frontmatter, 빈 섹션, stale index)는 mdlint나 wiki-lint 같은 Obsidian 인지 도구 또는 자체 스크립트(podcast-wiki의 `tools/lint_wiki.py`, llmwiki의 `lint` 도구)로. 결정론적 검사(스크립트) + 의미 검사(LLM lint) 2단 구성이 공통 패턴.
- 관련 섹션: "야간 lint 잡" 설계 — 기계적 검사는 CI 스크립트, 의미 모순은 LLM.

### 자료 34: 수집 변환 도구 — Notion Markdown API
- 출처: https://developers.notion.com/reference/retrieve-page-markdown
- 저자·날짜: Notion 공식 API 레퍼런스, 2026-10-11 열람. `Notion-Version: 2026-03-11`
- 신뢰성: 최상
- 인용 가능한 구절:
  > `GET /v1/pages/{page_id}/markdown` — "Retrieve the content of a page rendered as markdown."

  > 응답: `object: page_markdown`, `markdown`(enhanced markdown; `markdown_version=v2`면 Notion-flavored), `truncated`(레코드 한도 ~20,000 블록 또는 권한으로 잘림), `unknown_block_ids`(최대 100개; 다시 같은 엔드포인트에 넘겨 하위 트리 조회)

  > 권한: 연결(integration)에 read content 권한 필요(없으면 403, 접근 불가/없는 페이지 404)
- 보조: TypeScript SDK `notion.pages.retrieveMarkdown({ page_id })`; `include_transcript` 파라미터(2026-02-26 체인지로그; 2차 자료 matthiasfrank.de — 사실 확인 필요); 동일 포맷으로 `POST /v1/pages`·`PATCH /v1/pages/:page_id/markdown`.
- 관련 섹션: Notion → raw/ 수집 파이프라인(API 기반, UI 내보내기 불필요).

### 자료 35: 수집 변환 도구 — PDF/Office → Markdown (Docling vs MarkItDown 등)
- 출처: https://themenonlab.blog/blog/best-open-source-pdf-to-markdown-tools-2026 , https://dev.to/felipe_anyformat/pdf-to-markdown-for-llms-o2e , https://www.file2markdown.ai/blog/docling-vs-markitdown (벤더 글 — 편향 주의)
- 저자·날짜: 2026 (블로그 비교; 소규모 단일 실행 벤치)
- 신뢰성: 중~하
- 핵심 주장: Docling(IBM)은 레이아웃·표가 복잡한 문서에 강하지만 무겁고 GPU 없으면 느림. MarkItDown(Microsoft)은 가볍고 빠르지만 헤딩 구조·표가 깨지고 스캔 PDF는 빈 문자열(OCR 플러그인 미사용 시). Marker(선택적 LLM 패스), PyMuPDF4LLM도 후보. 결론: 자기 문서 샘플로 직접 돌려 보고 결정.
- 관련 섹션: ingest 전처리 도구 선택, "표가 많은 PDF는 Docling, 깨끗한 단일 컬럼은 MarkItDown" 류 휴리스틱(단, 수치 인용 금지).

### 자료 36: 수집 변환 도구 — Slack 내보내기
- 출처: https://github.com/rusq/slackdump
- 저자·날짜: rusq, 2026-10 기준 활동 중
- 신뢰성: 중 (README 요약 수준)
- 핵심 주장: 관리자 권한 없이 공개/비공개 메시지·스레드·파일·사용자 덤프, Standard/Mattermost 내보내기 모드, 뷰어·검색 내장. **마크다운 직접 출력은 미확인** — JSON을 스레드 단위 마크다운으로 바꾸는 변환 스크립트가 필요(토스 글의 "스레드 단위 요약" 원칙과 결합).
- 관련 섹션: Slack → raw/ 파이프라인, 스레드 단위 정규화.

---

## F. 한국 엔지니어링 블로그 — 사내 지식·RAG·에이전트

### 자료 37: 토스 테크 — "LLM은 똑똑한데, 왜 우리 회사 일은 모를까"
- 출처: https://toss.tech/article/llm_context_topic
- 저자·날짜: 김병균 (토스 Node.js Developer), 2026-07-30
- 신뢰성: 최상 (회사 엔지니어링 블로그)
- 핵심 주장: 검색이 찾은 텍스트 조각은 "재료"일 뿐 신뢰할 컨텍스트가 아니다. 문서 최신성·메신저 논의의 최종 결정 여부·문서-코드 일치를 판단하는 컨텍스트 레이어("Topic")가 답변 재료와 함께 **신뢰 상태**(`trusted`, `partly_trusted`, `disputed`, `stale_risk`, `insufficient_evidence`)를 반환한다. 메신저는 스레드 단위로 요약하고 결정/미결을 구분. 문서와 코드가 다를 때 항상 코드가 옳은 건 아니다(문서=목표 상태일 수 있음; 관계 유형 `contradicted_by`).
- 인용 가능한 구절:
  > "이런 질문에는 모델의 추론 능력만으로 답할 수 없어요."

  > "이 조각은 답변을 만드는 재료로는 유용하지만, 그 자체로 신뢰할 수 있는 컨텍스트는 아니에요."

  > "찾은 문서가 최신인지, 사내 메신저에서의 논의가 최종 결정인지, 문서의 설명과 실제 코드가 일치하는지는 검색만으로 판단하기 어려웠어요."

  > "결정된 내용과 결론이 나지 않은 내용을 명시적으로 나눠요."

  > "`insufficient_evidence`도 실패가 아니에요."
- 메모: 평가 수치 없음. 본문의 "0.87", "세 번/두 번"은 예시값.
- 관련 섹션: 위키 페이지 frontmatter에 신뢰 상태·최신성 필드 두기, "위키에 없음/근거 부족" 답변 설계, 결정 vs 논의 구분(최근 전략 결정 수집).

### 자료 38: 토스 테크 — "Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기"
- 출처: https://toss.tech/article/harness-for-team-productivity
- 저자·날짜: 김용성 (토스페이먼츠 Node.js Developer), 2026-02-26
- 신뢰성: 최상 (단, 저자 스스로 "방향성"이라 명시)
- 인용 가능한 구절:
  > "사람이 읽으면: 업무 가이드라인이자 매뉴얼이 되고," / "LLM이 읽으면: 정확한 지시사항이 담긴 시스템 프롬프트가 됩니다."

  > "문서 관리의 패러다임이 '기록'에서 '실행'으로 바뀌는 셈입니다."

  > "Global Layer: 전사 공통 규정 (보안 정책, 기본 코딩 스타일)" / "Domain Layer: 팀/비즈니스별 지식 (결제, 정산, 회원 등 특정 도메인 로직)" / "Local Layer: 특정 레포지토리의 구현 디테일 및 프로젝트 특화 규칙"

  > "잘 관리된 플러그인(프롬프트+코드)들의 집합이 곧 우리 조직의 기술 자산이 되는 셈입니다."

  > "지금까지의 이야기는 대부분 가설이고 방향성입니다."
- 관련 섹션: 회사 지식의 3계층(전사/도메인/로컬)과 위키 디렉터리 설계, "문서가 곧 실행 지시"라는 관점.

### 자료 39: 우아한형제들 — "AI 데이터 분석가 '물어보새' 3부. Agent로 더 넓고 깊은 지식 공유하기"
- 출처: https://techblog.woowahan.com/23273/ (1부: https://techblog.woowahan.com/18144/)
- 저자·날짜: BADA팀, 2025-10-15
- 신뢰성: 최상
- 핵심 주장: 고정 워크플로가 유지보수 불가능해져 ReAct 에이전트로 전환. Wiki는 사용량 기준으로 핵심 문서만 자동 선별, 메타데이터 저장으로 검색 정밀도↑. Atlassian MCP로 실시간 조회 + 연결 실패 시 벡터 스토어 fallback. Langfuse 추적 + G-Eval 자동 평가. BM25s로 검색 속도↑·품질 약 15%↑.
- 인용 가능한 구절:
  > "개발자가 설계한 순서에만 의존했기 때문에 새로운 질문이 등장할 때마다 코드를 수정해야 하는 비효율적이고 유지보수 불가능한 구조로 이어졌습니다."

  > (Anthropic 엔지니어 조언) "LLM에게 믿고 위임하세요."

  > "Wiki 공간별 문서 생성 수와 최근 2주 조회수를 기준으로 핵심 문서만 자동으로 선별해 수집했습니다."

  > "문서 제목, 팀명, 생성일, 라벨 등 메타데이터도 함께 저장하여 검색의 정밀도를 한층 끌어올렸습니다."

  > "Atlassian MCP 서버로 Confluence Wiki·Jira의 최신 정보와 저장하지 않았던 데이터까지 실시간으로 가져올 수 있게 되었습니다."

  > "연결 실패 시에는 자동으로 벡터 스토어 기반 검색으로 전환하는 Fallback 전략을 적용했습니다."

  > "LLM 기반 자동 평가(G-Eval)를 도입했습니다." / 리트리버 테스트에서 "약 15%의 검색 품질 향상을 확인했습니다"

  > "중요한 것은 기술이 아니라 사용자의 문제를 해결하는 일이며, 기술은 문제 해결 과정에서 자연스럽게 발전한다는 점"
- 메모: "BM25s 최대 500배 빠름", "임직원 4명 중 1명 사용"은 요약에서 나온 수치 — 원문 대조 (사실 확인 필요).
- 관련 섹션: 소스 선별 기준(사용량 기반), 메타데이터 frontmatter, 실시간 소스(MCP) + 컴파일된 위키 병행, 평가 파이프라인.

### 자료 40: LY Corporation — "엔터프라이즈 LLM 서비스 구축기 1: 컨텍스트 엔지니어링"
- 출처: https://techblog.lycorp.co.jp/ko/building-an-llm-service-for-enterprise-1-context-engineering
- 저자·날짜: 한우형 (LY Corporation Cloud AI Platform 팀), 발행일 페이지 미표시(2025~2026 추정; 사실 확인 필요)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "'컨텍스트 엔지니어링'은 LLM에게 '필요한 정보만 선별해서 제공하는 것'입니다."

  > "일반 RAG 챗봇: \"서버 접속이 안 되면 네트워크 상태나 VPC ACL을 확인해 보세요\" → 일반론적인 가이드"

  > "처음부터 모든 정보를 제공하는 대신, 사용자의 질문이나 현재 진행 상태에 따라 필요한 정보만 적절히 선택해서 AI에게 제공하는 방식입니다."

  > (Databricks 연구 인용) "GPT-4나 Llama-3.1 같은 모델에서도 컨텍스트가 특정 구간(32K~64K 토큰)을 넘어가면 RAG 성능이 하락하기 시작했습니다."

  > 규모: 제품군 27개, API 260여 개, 문서 수백 페이지; 예: "Redis 클러스터 상태" 질문 시 도구 8개만 제공하고 252개는 제외
- 설계 메모: 응답 가이드라인을 시스템 프롬프트가 아니라 도구 메시지로 주입(강제 지침이 아닌 참고로 인식되게), API 응답에 필드 설명 스키마를 붙이고 YAML 채택(토큰 효율).
- 관련 섹션: 질문별 도구/페이지 선별(progressive disclosure의 한국 사례), 컨텍스트 과적재 수치 근거.

### 자료 41: LY Corporation — "ODW #5: 벡터 DB와 에이전트 스킬로 RAG 시스템 만들기"
- 출처: https://techblog.lycorp.co.jp/ko/building-rag-system-with-vector-db-and-agent-skills
- 저자·날짜: giginet (LY Corporation 모바일 개발자 경험 팀), 발행일 미표시(2026 추정)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "이번 워크숍에서는 이러한 상황을 가정하고 자연어로 작성한 대량의 문서를 AI 에이전트가 효율적으로 참조하는 방법을 모색했습니다."

  > "MCP 도구를 통해 코딩 에이전트(Claude Code)에서 이 DB를 참조하는 과정으로 실습을 진행했습니다."

  > "스킬을 만들어 MCP 도구 이용을 간소화하는 방법을 소개했습니다" / "'SE-0500을 조사해줘'와 같은 최소한의 지시만으로 Swift Evolution 내용을 검색할 수 있게 되었습니다."
- 메모: MCP만으로는 "도구 호출법"만 공유되므로, DB의 컬렉션·ID 형식·메타데이터를 가르치는 스킬을 얹었다는 것이 핵심. `n_results` 축소로 출력 잘림 대응.
- 관련 섹션: MCP(접근) + Skill(사용법 지식)의 조합, ChromaDB 로컬 벡터DB 실습.

### 자료 42: Samsung Tech Blog — "업무 생산성 향상을 위한 Agentic RAG 기반 서비스" (DeepDive)
- 출처: https://techblog.samsung.com/blog/article/76
- 저자·날짜: 송하연 (삼성리서치), 2026-01-29
- 신뢰성: 최상 (단, 본문 대부분 접근 실패 — 도입부만 확보, 재시도 시 Cloudflare 520)
- 인용 가능한 구절:
  > "DeepDive는 삼성리서치에서 개발 중인 사내 AI 서비스로, 검색 증강 생성(RAG, Retrieval-Augmented Generation) 기술을 활용해 방대한 사내 문서의 정보 탐색과 보고서 작성을 자동화합니다."

  > "간단한 질의 응답부터 전문적인 심층 리서치 보고서까지 폭넓게 지원하며"
- 메모: 검색 요약에 따르면 같은 블로그에 "Agentic Search 시스템 구축기: 사내 검색 환경을 재정의하기 위해 우리가 선택한 것들"(2026-02)도 있음 — URL 미확보. 보강 시 우선 대상.
- 관련 섹션: 국내 대기업 사내 RAG→Agentic 전환 사례(보강 필요).

### 자료 43: 기타 한국어 2차 자료 (참고용, 인용은 삼감)
- fastcampus "5분 트렌드 아티클 — LLM 위키" https://fastcampus.co.kr/story_article_llmwiki_2 (2026, 입문 요약)
- brunch "UX/UI 디자인을 위한 옵시디언 LLM Wiki 구축" https://brunch.co.kr/@ghidesigner/488 (2026, 비개발 직군 적용기)
- velog "RAG is dead, long live RAG?! - 2024, 2025, 2026 RAG 트렌드 연대기" https://velog.io/@qlgks1/RAG-is-dead-long-live-RAG-Agentic-Retrieval (2026, 흐름 정리)
- GeekNews WUPHF — "Karpathy 스타일 LLM 위키를 에이전트들이 직접 유지하는 시스템" https://news.hada.io/topic?go=comments&id=28910 (마크다운+Git 기반 에이전트용 위키 레이어)
- 신뢰성: 중~하. 1차 수치 없음.

---

## G. agentic search vs 벡터 RAG — 웹 글 범위

### 자료 44: LatentEval 리서치 노트 — "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search" (PwC 논문 해설)
- 출처: https://latenteval.ai/research/is-grep-all-you-need (논문: https://arxiv.org/abs/2605.15184, 2026-05-14; 논문 자체는 paper-researcher 담당)
- 저자·날짜: LatentEval, 2026-08-03
- 신뢰성: 중 (논문 2차 해설; 수치는 논문 대조 필요)
- 핵심 주장: LongMemEval 116문항, 하네스 4종(Chronos, Claude Code, Codex CLI, Gemini CLI) × 모델 5종. 결과를 인라인으로 돌려주면 grep이 10쌍 전부에서 벡터를 이김; 결과를 파일에 쓰면 5/10에서 역전. 같은 Opus 4.6도 하네스에 따라 93.1% vs 76.7%.
- 인용 가능한 구절:
  > 저자 결론(해설 인용): 하네스를 바꾸면 "shifts the ceiling by roughly as much as swapping retrievers within a fixed harness."

  > 범위 한정: 결론은 "tied to long-memory conversational QA"이며 grep이 일반적으로 "beats" vector라고 주장하지 않음.

  > HN softwaredoug(해설 인용): "grep is fine if you don't care about tokens and you have less than 100k files."
- 주의: 116문항 단일 점추정·신뢰구간 없음, 동일 조건을 76.7%/94.0%로 다르게 적은 표 불일치, v1 프리프린트.
- 관련 섹션: "index.md+grep로 시작, 하이브리드 검색은 필요할 때" 논리의 근거와 한계, 도구 결과 전달 방식(인라인 vs 파일)이 성능을 좌우.

### 자료 45: Dev.to — "RAG Is Not Always the Answer Anymore: How AI Agents Search Code in 2026" 외
- 출처: https://dev.to/nimay_04/rag-is-not-always-the-answer-anymore-how-ai-agents-search-code-in-2026-43m3 , https://dev.to/pueding/is-grep-all-you-need-grep-vs-vector-retrieval-for-agentic-search-534k
- 저자·날짜: 2026
- 신뢰성: 중~하 (커뮤니티 블로그)
- 핵심 주장: Claude Code는 정적 임베딩 대신 grep/ls/cat을 Plan–Act–Observe 루프에서 동적으로 쓴다. 벡터 RAG는 "구조가 약한 산문·표현이 다양한 개념 질문"에 여전히 유리. 숫자 인용은 삼갈 것(illustrative 표기).
- 관련 섹션: 코드베이스 검색 관행이 위키 검색으로 전이된 맥락.

---

## 교차 검증 메모 (fact-checker용)
- "~100 sources, ~hundreds of pages"까지 index.md만으로 충분 — Karpathy gist 원문(자료 1). julianoczkowski는 "수백 문서"(자료 10), 클리앙은 500+ 메모에서 문제없음(자료 6), GN 댓글은 규모 폭증이 최대 문제(자료 4). 수치는 서로 모순되지 않으나 "경험치"임.
- Karpathy 트윗 문구는 Platformer 인용(자료 3) 외 1차 확인 못 함. "100 articles / 400,000 words" 등 2차 블로그의 Karpathy 위키 규모 주장은 **근거 미확인** — 사용 금지.
- 모델명/가격(Fable 5.1, Opus 5.5 등, 캐시 배수 0.025x/0.05x)은 2026-10-11 공식 문서 기준. 본문 집필 시 재확인.
- Agent SDK 버전: PyPI 0.2.165(2026-10-08), npm 0.3.296(2026-10-09). 책에는 "2026년 10월 기준 0.2.x / 0.3.x"로 쓰는 것이 안전.
- Files API: 베타 헤더 불필요(GA). 구 자료의 `anthropic-beta: files-api-2025-04-14` 설명은 구버전 정보일 수 있음.
- Contextual Retrieval 수치(35%/49%/67%, $1.02/M)는 2024-09 실험 — "2024년 기준"으로 못 박을 것.

## 수집 한계
- 접근 실패: youngju.dev "사내 지식베이스를 LLM으로 만든다는 것 — 권한 인지 검색, 신선도, 출시 전 평가셋"(2026-07-31) — 도메인 만료로 파킹 페이지만 반환. Cerebras 사내 지식베이스 원문(2026-07-15 추정) — 공식 URL 미발견, 2차 요약(mer.vin, slite.com)만 존재해 인용 보류. Samsung Tech Blog 본문(article/76) — Cloudflare 520, 도입부만 확보; "Agentic Search 시스템 구축기"(2026-02) URL 미확보. npmjs 페이지 403 → `npm view`로 대체 확인. Karpathy 원 트윗(x.com) 직접 미확인.
- 의도적으로 제외: 출처·날짜 없는 나열형 "2026 가이드" 류(mindstudio, agentpedia, kunalganglani 등), 벤더 홍보성 비교(file2markdown 등은 참고 표시만), 논문 본문(paper-researcher 담당), HN/Reddit 원댓글(community-researcher 담당 — GN⁺ 2차 요약만 기록).
- 미수집 영역: Google Docs → 마크다운 공식 경로(Drive API export MIME `text/markdown` 지원 여부 미확인), Quartz/Docusaurus 사내 인증(SSO 프록시) 1차 문서, Obsidian Web Clipper 공식 문서, 카카오·네이버 D2의 사내 지식베이스 글(검색에서 미노출).
