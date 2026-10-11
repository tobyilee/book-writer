# 커뮤니티 리서치: LLM Wiki 패턴으로 사내 지식 베이스 구축

- 검색 시점: 2026-10-11
- 장르: tech-book / 대상 독자: 에이전틱 코딩 도구로 사내 지식 베이스를 만드는 개발자
- 원 소스: Karpathy, "LLM Wiki" gist (2026-04-04 공개, https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) + X 포스트 "LLM Knowledge Bases" (2026-04-02, https://x.com/karpathy/status/2039805659525644595 — fxtwitter API 기준 조회 2,195만 / 좋아요 61,003 / 답글 2,939)
- 수집 범위: HN 스레드 8개(댓글 약 240개 열람), gist 댓글 약 250개(4페이지), GitHub Issues 3개 저장소, X 포스트 3개(메타데이터), 1인칭 구현 보고 블로그 11편, GeekNews 토픽 4개, PyTorchKR·클리앙·velog·AI매터스 등 한국 소스 6개
- **모든 내용은 "커뮤니티 의견, 검증 필요"다.** 수치는 자기 보고이며 통제 실험이 아니다. 책에 인용할 때는 원문 링크를 다시 열어 확인할 것.

---

## 0. 왜 이 패턴이 커뮤니티를 흔들었나 (맥락)

- Karpathy X 포스트가 하루 만에 수백만 조회를 넘겼고, 국내 Threads 계정(@choi.openai)은 "하루 만에 270만 회"를 언급 (https://www.threads.com/@choi.openai/post/DWvW8IvicHN/ — 커뮤니티 의견, 검증 필요).
- HN 원 스레드 "LLM Wiki – example of an 'idea file'" (2026-04-04, 296p / 95댓글, https://news.ycombinator.com/item?id=47640875). 이후 6개월 동안 HN에 "LLM wiki"를 제목에 단 Show HN이 40건 이상 올라옴 (Algolia 검색 286 hits).
- GeekNews GN#352 (2026-04) 편집자 코멘트: "이 LLM-Wiki는 LLM을 단순 질의 응답기가 아닌 자동화된 위키 관리자로 다루는 새로운 패러다임을 보여줍니다." (https://news.hada.io/weekly/202614)
- VentureBeat 헤드라인("bypasses RAG")이 "RAG 대 위키" 양자택일 프레임을 키웠다는 지적이 여러 글에서 반복 (https://atlan.com/know/llm-wiki-vs-rag-knowledge-base/ 등).

---

## 1. 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "위키는 멀쩡해 보이는데, 읽어 보면 틀렸다" — 조용한 부패(silent rot)
가장 많이 반복된 고통. 사람이 방치한 위키는 낡아 보이지만, LLM이 관리하는 위키는 낡아 보이지 않으면서 틀린다.

- HN(WUPHF 스레드, 2026-04-25): Abby_101 — "Six months in, you have entries that are confidently wrong and the lint pass can't tell which." (https://news.ycombinator.com/item?id=47899844)
- HN 같은 스레드: johntash — 예전 시도가 "looked good until you read the actual data"였고 커지면서 못 쓰게 됐다.
- HN 같은 스레드: ryanshrott — 틀린 항목을 다른 에이전트가 인용하면서 "a knowledge base full of confident BS"가 된다.
- gist 댓글: Jwcjwc12 (2026-04-05) — "the moment those files change, the compiled knowledge might be wrong — and doesn't know it."
- gist 댓글: laphilosophia (2026-04-04) — LLM은 "fail quietly" 한다(낡은 주장, 거짓 일관성, 페이지 난립). "the real product problem is not organization, it is epistemic integrity."
- gist 댓글: XBlueSky (2026-09-22) — "A transcript-filter payload drift silently produced unusable records for two weeks before I noticed it."
- Felipe Fontoura 블로그 (2026-10-06): "A wiki maintained by an LLM never looks neglected. It stays fluent, linked, and current-sounding while the content drifts." (https://felipefontoura.com/articles/llm-wiki/)
- Rost Glukhov: "An LLM Wiki fails when old facts remain plausible" / "A page without a review date is a page that will eventually lie quietly." (https://www.glukhov.org/knowledge-management/knowledge-systems-architectures/compiled-knowledge/llm-wiki-maintenance-knowledge-drift/)
- PyTorchKR 댓글: clue.oz4e (2026-08-21) — "노트가 바뀌었을 때 위키가 조용히 낡는데, 그걸 알려주는 신호가 없다는 게 제가 겪은 가장 큰 위험이었습니다." (https://discuss.pytorch.kr/t/llm-wiki-karpathy/10843)
- Taktile 엔지니어링 블로그 (2026-07-13): "Keeping a compiled knowledge layer trustworthy when its underlying sources drift silently turned out to be the hard part." (https://engineering.taktile.com/blog/llm-wiki-agent-memory/)
- 추정 원인(커뮤니티 공유 진단): 원본이 바뀌어도 컴파일된 페이지에 신호가 없다 / 구조 린트(깨진 링크·고아 페이지)는 잡지만 의미 린트(낡은 주장·모순)는 못 잡는다 / 린트조차 LLM이 하면 자기 채점이 된다.

### 패턴 2: 요약의 요약 — 오류가 사실로 굳는다
- HN 원 스레드: Imanari — "kicking the can down the road"; 위키가 컨텍스트에 다 안 들어가면 LLM은 원본 대신 위키를 다시 읽고 "subtle errors as we start to regurgitate 2nd-order information"가 쌓인다. (https://news.ycombinator.com/item?id=47640875)
- HN 원 스레드: devnullbrain — "I don't see why this wouldn't just lead to model collapse." (반론 gojomo: 2024년식 collapse 공포는 직관을 흐린다; ChrisGreenHeur: 학습이 아니라 개인 위키 얘기라 핀트가 다르다.)
- HN 원 스레드: Lockal — DeepWiki도 "it also hallucinates, adding factually incorrect information."
- gist 댓글: asong56 (2026-04-07) — AI 환각이 사실로 영구히 박히고, 치우는 게 유지보수 부담이 된다.
- gist 댓글: frosk1 (2026-04-06) — 오류 누적, 부분 컨텍스트 업데이트, 정보 손실, 환각 병합, 비용, 낡음을 한 번에 열거.
- gist 댓글: Marekai (2026-04-07) — 페이지 번호가 사라지고 바꿔 말하기(paraphrase)가 생겨 "(Author, Year, p. 47)" 식 인용을 못 만든다 → 학술·규제 용도 치명.
- velog 박채빈 글(2026-05-12)이 정리한 댓글 a-a-k: "원본 문서를 LLM이 위키 페이지로 재작성할 때 단서, 날짜, 소수 견해, 엣지 케이스, 정확한 표현이 소실될 수 있다." / "위키가 커질수록 요약 오류가 진실처럼 굳어진다." / "소스 하나 추가가 수십 개 페이지에 영향을 준다." (https://velog.io/@parkchaebin/LLM-Wiki-Karpathy)
- AI매터스 칼럼 김탄휴 (2026-05-21): "한 페이지의 작은 오해가 연결된 여러 페이지로 조용히 전파된다." / "마크다운 무덤이 되거나, 잘못된 정보가 우아하게 정리된 거짓 위키가 되거나" (https://aimatters.co.kr/news-report/42742/)

### 패턴 3: 위키에 없는 답을 아무 노트나 물고 온다 — 범위 밖 답변·환각 인용
- PyTorchKR 댓글: clue.oz4e (2026-08-10) — "답이 없는 질문 10개를 던지면 10개 전부 아무 노트나 근거로 물고 나왔고" (https://discuss.pytorch.kr/t/llm-wiki-karpathy/10843)
- gist 댓글: manavgup (2026-04-08) — 위키링크를 "hallucinates 404s" (존재하지 않는 페이지로 링크).
- gist 댓글: ShootJackal (2026-10-01) — 과거 버그: 노트가 파일 경계를 위조해 조작된 답에 VERIFIED 표식을 받은 적이 있다. 지금은 "a check with no model in it confirms each quote is in the cited note at that commit."
- gist 댓글: tomjwxf (2026-04-06) — "가장 중요한 미해결 문제": LLM 위키는 인용 없이 합성하고, 원본에서 멀어지고, 거짓 확신을 보인다.
- gist 댓글: Valentin-Laurent (2026-04-08) — 정확한 출처 인용이 "one of the trickiest parts".
- Platformer Casey Newton (2026-08-18): 쓰기 전 원본을 열어 "to make sure nothing I was about to say was hallucinated." (https://www.platformer.news/karpathy-llm-wiki-journalism-productivity/)

### 패턴 4: 모순을 "매끄럽게 뭉개 버린다"
- Jim Liu, 6개월 보고 (2026-05-06): Claude가 새 글에 맞춰 옛 페이지를 덮어썼다가 앞선 논리를 잃음. 교훈 "Contradictions are assets, not errors." (https://www.openaitoolshub.org/en/blog/karpathy-llm-wiki)
- Glukhov: "Do not let the agent silently resolve contradictions by blending both claims into a vague compromise."
- Fontoura 계약 조항: "Record contradictions and divergences. Never smooth them into one story."
- gist 댓글: HagaiHen (2026-10-08) — "Never silently overwrite." 상충 견해는 출처와 함께 나란히 기록.
- gist 댓글: quan2005, singularityjason, wumborti — 시간에 걸친 저널형 항목의 모순·공백 탐지는 "아직 못 풀었다"는 고백이 반복.
- Ghelbur 6개월 보고 (2026-04-29): 모순을 인제스트 때 플래그만 하고 수동 해소 → 수백 페이지 넘자 "accumulated faster than they could be fixed", 답변이 헤지(hedge)됨. (https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres)

### 패턴 5: 컨텍스트 비대·index.md 붕괴
- HN 원 스레드: lelanthran — "What use is 10M context if degradation starts at 200k - 300k?"
- HN 원 스레드: kwar13 — 모델이 "can't even keep up with a simple claude.md let alone a whole wiki."
- HN WUPHF 스레드: criley2 — "bloated CLAUDE.md files filled with data that agents can gather on the spot"가 결과를 해친다. arXiv 2602.11988(자동 생성 AGENTS.md가 더 나쁨) 인용.
- gist 댓글: singularityjason (2026-04-07) — index.md는 "~100 pages" 넘으면 깨진다.
- gist 댓글: bitsofchris (2026-04-07, 노트 4,000+개) — "Index files will break" at scale.
- gist 댓글: manavgup — index.md/log.md가 "scales worse than expected."
- gist 댓글: mpazik (2026-04-05) — 수백 페이지 넘으면 쿼리가 깨지고, 프런트매터·명명·폴더 규칙이 슬금슬금 늘어난다.
- rohitg00 "LLM Wiki v2" gist: "This works up to maybe 100-200 pages." 인덱스는 사람용 카탈로그로만 두고 "don't rely on it as the LLM's primary search mechanism past ~100 pages." (https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- AI매터스: "자료가 늘어날수록 인덱스 자체가 비대해져 매 쿼리에 들어가는 컨텍스트가 커진다."
- HN vault-operator 스레드 (2026-06-01): wickedsight — "context can get dirty", 모델이 틀린 답 쪽으로 계속 표류. (https://news.ycombinator.com/item?id=48351115)
- Claude Code 이슈 #42796 (2026-04-02, 댓글 583): 5,000+ 단어 CLAUDE.md의 규약을 모델이 무시했다는 보고. (https://github.com/anthropics/claude-code/issues/42796)

### 패턴 6: 토큰·비용이 "조용히 계속 나간다"
- gist 댓글: Helleeni (2026-04-08) — 한 시간 만에 개인 위키를 만들었지만 "burnt through my tokens for one Claude Code session".
- gist 댓글: grishasen (2026-04-08) — 이틀 걸려 만들었는데 하루 만에 만든 로컬 RAG보다 못하고, 위키가 "consumes a significant number of tokens."
- HN 원 스레드: vbarsoum — 책 3권(68파일, 약 15.5만 단어) 컴파일에 약 12M 토큰, 10~15분.
- HN WUPHF 스레드: adamsmark — "accidentally running up a huge Gemini bill" → OpenRouter 저가 모델로 이동.
- AI매터스가 인용한 LinkedIn 분석: "위키의 모든 컴파일, 린트, 쿼리는 클로드 코드의 토큰을 태운다. 진짜 돈이다." / "이 시스템은 한 번 세팅되면 계속 토큰을 먹는다."
- GeekNews alfadur (2026-07): 자율 멀티에이전트로 돌리니 "토큰만 5~10배 잡아먹고 컨텍스트도 자주 놓칩니다." (https://news.hada.io/topic?go=comments&id=31140)
- 클리앙 카일라스 (2026-04-26): "500+ 메모를 위키에 등록하는데 20분 넘게 걸림..." / "위키 검색에도 시간이 꽤 걸림." (https://www.clien.net/service/board/lecture/19182891)
- 클리앙 댓글 프밍 (2026-04-27): 업무 관련 글 약 60개로 위키를 만드는 데 Claude Pro 토큰을 이틀 가까이 소진.
- 반대 사례도 있음: glaucobrito (gist, 2026-04-09) — 33일, 1,493 관측, 부팅 ~8K 토큰, "$0 cost"(구독 범위 내). Jim Liu — Claude Pro $20/월 기존 구독이라 한계비용 0.

### 패턴 7: 유지보수가 사람을 잡아먹는다 — "쓰는 사람만 있고 읽는 사람이 없다"
- HN WUPHF 스레드: simsla — "Everyone is writing. Nobody is reading."
- HN WUPHF 스레드: mplappert — "a serious issue with people using AI to do an immense amount of busywork and then never look at it again."
- HN 원 스레드: saberience — "it's more fun to build than to actually use." 어려운 건 낡음·충돌·비대·가지치기·적시에 띄우기이며, 대부분 새로움이 가시면 버린다.
- Theo James, Medium (2026-04-21): "The system didn't fail because the model was bad. It failed because I couldn't maintain the inputs." / "Maintenance is where good systems go to die." / "Missing 5 percent is fine. Missing three weeks is not." / 검증을 다 해야 하면 "I stop using it." (https://medium.com/@theo-james/i-tried-to-build-karpathy-llm-wiki-heres-where-it-broke-down-for-me-9c3eef65af21)
- Platformer Newton: "What's less great is that the wiki needs more or less constant maintenance." 페이지가 너무 길어져 압축이 필요, 코드 오류로 프로세스가 멈추기도.
- Ask HN "Do you use LLM-Wikis?" (2026-07-17, DavidHaerer): 아이디어에 끌리지만 "haven't gotten much value from it" — 댓글 0. (https://news.ycombinator.com/item?id=48952492)
- Ghelbur: 운영을 수동으로만 돌리면 "vaults rot in silence." / "You do not read your own notes."
- Aaron Fulkerson (2026-04-12): "That's how every wiki I've ever built eventually died — under the weight of its own bookkeeping." (https://aaronfulkerson.com/2026/04/12/karpathys-pattern-for-an-llm-wiki-in-production/)

### 패턴 8: 에이전트가 하면 안 되는 일을 한다 — raw/ 수정, 커밋 누락, 과잉 기록
- Dev.to @vellumkasane (2026-09-22): 2주 안에 깨진 네 가지 — (1) 에이전트가 raw/ 안 CSV의 "오타를 고쳐" 버림: "'raw is immutable' in a CLAUDE.md is a wish, not a rule." (2) "The wiki repo sat dirty until someone noticed." (3) "Every 'helpful' session added a page nobody linked to." 한 달 뒤 위키는 "a pile". (4) 에이전트가 자꾸 "should I record this?" 묻기 — "Noise, not missing entries, was the failure mode." (https://dev.to/vellumkasane/four-things-that-broke-when-i-ran-karpathys-llm-wiki-with-claude-code-and-the-fixes-4h4f)
- Jim Liu: Claude가 originals/의 원문 어투를 매끈하게 고쳐 버림 → do-not-rewrite 태그와 폴더 수정 금지.
- lucasastorian/llmwiki 이슈 #93 (2026-09-19): 삭제가 사용자 원본 파일까지 디스크에서 지움 — README의 "never modify your files" 약속과 모순. 같은 이슈: 신규 인제스트 직후 lint의 stale-page 검사가 모든 페이지를 낡았다고 플래그. (https://github.com/lucasastorian/llmwiki/issues/93)
- HN WUPHF 스레드: johntash — "how to stop LLMs from over-documenting?"
- gist 댓글: Yuncun (2026-04-07) — 성숙한 코드베이스에서 "keep docs updated" 같은 긴 문서는 그냥 AI slop.

### 패턴 9: 팀으로 가면 바로 터지는 것들 — 승인, 권한, 동시 쓰기, 민감 문서
- gist 댓글 (첫날): geetansharora — 팀과 어떻게 공유하나? 이미 쓰는 RAG + MCP 서버 방식을 따라야 하나? (답 없음)
- gist 댓글: MoserMichael (2026-04-07) — "Who decides what becomes a memory, and how is it evaluated?"
- gist 댓글: alinawab (2026-04-04) — "What's the failure mode? Where does it start fighting you?" (답글 없음)
- HN WUPHF 스레드: Abby_101 — 에이전트가 스스로 승격(promote)해도 되나, 사람 리뷰가 필요한가? / psteinweber — 소규모 마케팅 팀, 사람 여러 명 + human-in-the-loop 지원 여부 질문 / sails — 민감 비즈니스 문서를 GitHub에 올리는 것이 꺼려짐, Cloudflare·GCP 내부 배포 원함.
- gist 댓글: rothnic (2026-04-07) — Obsidian은 "wasn't well suited" 분산 공유 지식 베이스에.
- gist 댓글: ap0phasi (2026-04-07) — 조직 간 데이터 출처 오염 우려 → 인제스트마다 git 브랜치.
- gist 댓글: xoai — 미해결 갭 "proposition-level provenance and multi-writer wikis."
- HN WUPHF 스레드: renan_warmling — 스냅샷·롤백 기록 부재, 시간적(temporal) 기억과 비시간적(atemporal) 기억이 분리되지 않음.
- Stigmergy README(팀용 LLM 위키, 2026-08): 여러 사람·에이전트가 공유하는 순간 "you need what a shared deployment forces on you: identity, visibility, concurrency, binary evidence, Slack, audit." (https://github.com/sturlese/stigmergy)

### 패턴 10: 생각을 외주화한다는 불안 (사람 쪽 비용)
- HN 원 스레드: qaadika — "There's nothing 'personal' about a knowledge base you filled by asking AI questions." / "Learn how to learn and answer your own damn questions."
- HN 원 스레드: nidnogg — 다 위임하다 보니 "a persistent brain gap"; "the wiki workflow is just too addictive to stop."
- HN 원 스레드: stingraycharles — "I worry about losing the ability to think hard."
- HN 원 스레드: loveparade — "Most of the value of writing docs or a wiki is not in the final artifacts."
- HN WUPHF 스레드: portly — "The whole point of taking notes for me is to read a source critically."
- gist 댓글: robertandrews — generation effect가 사라진다; pssah4 — 요약이 이해를 만드는 사고를 대체한다.
- GeekNews 28208 댓글 junghan0611 — PKM은 기술 난이도보다 사람과 AI 도구의 장기 공진화 문제.
- 사내 KB 책에 쓸 반전: 사내 지식은 "개인의 학습"이 아니라 "조직의 기억"이라 이 반론의 무게가 다르다 — 단, 결정의 이유를 남기는 사람의 역할은 남는다(당근 발표 인용, 아래 5절).

---

## 2. 실무 휴리스틱

### H1. raw/는 불변 — 그리고 "지시문이 아니라 훅으로" 강제한다
- 출처: Dev.to @vellumkasane — PreToolUse 훅으로 raw/ 아래 기존 파일 수정·덮어쓰기를 차단(신규 추가·append만 허용). Stop 훅이 `git status --porcelain`과 미푸시 커밋을 검사해 푸시 전엔 턴을 못 끝내게 함.
- Aaron Fulkerson: "Instructions set intent. Hooks enforce behavior" / "A hook script that exits with code 2 blocks the action deterministically."
- HN 원 스레드 hombre_fatal: 진실 원본은 /raw에, 나머지는 전부 그로부터 파생되고 /raw로 백링크.
- 동조: Jim Liu(do-not-rewrite 태그), Fontoura(인제스트 1회 = 커밋 1개로 되돌리기 가능).

### H2. 스키마 파일(CLAUDE.md/AGENTS.md)이 가장 중요한 파일이다
- Jim Liu 6개월: "The pattern works, but only if you treat the schema file as the most important file." schema.md에 프런트매터 필드, 슬러그 규칙, 모순 해소 프로토콜을 정의. 페이지 수명 필드: `last_verified`, `confidence`, `superseded_by`, `contradicts`.
- velog 댓글 ColonelPanicX·AgriciDaniel — 스키마 파일로 규칙을 고정해야 세션마다 일관.
- gist 댓글 justinzhang2039 (2026-04-06): 스키마에서 사람을 "You"라고 쓰면 자기 페르소나를 "You"로 보는 에이전트와 "role-mapping conflict"가 난다 → "User"/"Assistant"로 바꿔라.
- 주의(반대 근거): criley2가 인용한 arXiv 2602.11988 — 자동 생성 AGENTS.md는 성능을 떨어뜨림. 사람이 쓰고 짧게 유지하라는 쪽.

### H3. 페이지 상단 TL;DR + 토큰 예산 계층
- gist 댓글 YokoPunk (첫날): 각 위키 글 맨 위에 TLDR을 두면 사람과 LLM 모두 본문을 읽을지 판단 가능.
- Jim Liu: 모든 페이지가 50자 이하 TL;DR로 시작. 35개 TL;DR을 한 번에 훑을 수 있어 인덱스보다 이게 더 중요.
- gist 댓글 bluewater8008/hejiajiudeeyu (2026-04-05, 프로덕션 팀): 인덱스에 토큰 예산 — L0 ~200, L1 ~1–2K, L2 ~2–5K, L3 5–20K 토큰. 엔티티 유형별 템플릿 하나씩(7종). "The LLM is the writer. You're the editor-in-chief."
- gist 댓글 tomjwxf: 점진 공개 — L0 ~50, L1 ~200, L2 ~1K 토큰, L3 전체.
- Ghelbur "For future Claude" 서문: 더 읽어야 하는지 알려주는 짧은 블록. 프런트매터는 "in three lines"로 노트 종류를 알려야 함.
- gist 댓글 AgriciDaniel: 핫 캐시를 세션 컨텍스트 "under 500 tokens"로 유지.

### H4. 프런트매터에 출처·신뢰도·검토일을 박아라
- Fulkerson: YAML 프런트매터에 human-written / LLM-generated / LLM-generated-human-reviewed 태그. "Without this metadata, the model couldn't assess its own confidence in a source."
- Glukhov 검토 주기 표: 도구 버전 페이지 30–90일, 가격·가용성 7–30일, 비교 페이지 30–180일, 용어집 3–12개월, 아키텍처 원칙 6–18개월, 소스 요약은 소스 변경 시, 과거 결정은 대체될 때만. `review_after` = `last_reviewed` + 3개월.
- gist 댓글 l-mb: 폴더 대신 태그·속성(status: raw/tagged/processed, tagged_on) — 모델이 좋아지면 재태깅 가능.
- 반대 의견: asakin — YAML 대신 굵은 글씨 필드 메타데이터, index.md 없이 요약·태그 스캔. mfittko/repo-wiki PR #48 — GitHub Wiki는 프런트매터를 그대로 노출하고 Jekyll은 먹어 버려서 처리가 갈린다.

### H5. 인덱스는 손으로 유지하지 말고 "계산"하라 — 혹은 아예 빼라
- HN WUPHF 스레드 jermolene(TiddlyWiki 창시자): LLM은 인덱스 동기화를 못 지키므로 computed views가 hand-maintained index.md보다 낫다.
- gist 댓글 panakh (2026-04-09): "you don't really need the index for it" — LLM이 `ls` 하면 된다.
- gist 댓글 0xjaishy: "최근 무슨 일이 있었나" 같은 메타 쿼리에 index 페이지가 top-1로 뜨는 문제.
- PyTorchKR clue.oz4e: 인덱스 파일을 검색 색인에서 빼야 한다는 함정.
- Taktile: 질문 범주별 서브위키 + 각 레벨 index.md (top-down 탐색). Stigmergy: "Postgres is operational state and a rebuildable index, never a second wiki." + 야간 전체 리빌드로 수렴 보장.

### H6. log.md는 append-only 한 줄 — 단, 약한 모델은 혼란스러워한다
- Jim Liu: log.md는 작업당 타임스탬프 한 줄, 주 2회 grep. 최근 30회 인제스트에서 터치 파일 중앙값 9개(범위 4–23).
- Fulkerson: LOG.md가 "every significant vault mutation with a timestamp"를 기록; 90일 이상 낡은 항목 추적.
- Ghelbur: 변경을 일별 diff 노트로 기록; 에이전트 변경은 24시간 뒤 영구화("everything reversibly").
- 주의: gist 댓글 aakarim — log.md가 "seems to only confuse less intelligent models".
- otomatty/zedi PR #604: 활동 로그 쓰기는 throw 대신 로그 에러로 — 로그 실패가 본작업을 깨지 않게.

### H7. 린트는 두 층 — 구조 린트는 토큰 없이, 의미 린트만 모델로
- Fontoura: 구조 린트(깨진 링크, 고아)는 모델 토큰 없이 스크립트로, 모델은 모순·낡은 주장 같은 판단에만.
- Dev.to @vellumkasane: 150줄 린트 스크립트 — 프런트매터, index.md에서 도달 가능성, `[[link]]` 해소, ASCII 파일명, stale 페이지. CI에서 nonzero exit, 세션 종료 전 실행.
- Glukhov 체크리스트(구조): 깨진 내부 링크, 고아, 중복 제목, 소스 섹션 누락, 검토일 누락, 백링크 없는 페이지, 빈 섹션, 구조 없는 긴 페이지, 인덱스 미연결, 명명 불일치, 잘못된 프런트매터, 검토 기한 초과. (의미): 출처 없는 주장, 상충 주장, 낡은 결정의 현재형 서술, 이름만 다른 중복 개념, 여러 의미가 섞인 개념 페이지, 제약 생략 요약, 기준 없는 "best", 버전 없는 버전 주장, 최신 소스와 모순.
- Jim Liu 수치: 주간 수동 린트 약 20분(일요일 아침), 격주 서브에이전트 모순 탐지 1회 < $0.40(Opus 1M 컨텍스트), 주간 외부 링크 스크립트가 6개월간 약 24개 깨진 링크를 잡음.
- Fulkerson 첫 린트 결과: "23 orphaned files and 11 broken cross-references."
- HN 원 스레드 Covenant0028: N개 파일 간 모순 검사는 N*N. ChrisGreenHeur: 무작위 샘플링을 시간에 걸쳐 돌리면 대부분 드러난다.
- GeekNews 32164 alfadur: 린트는 포맷·구조·인용·모순을 기계적으로 검사하고, 최상단 단계만 LLM이 출판 전 정성 검토. "reground" 루프가 출판 페이지를 다시 읽어 개요·모순·허브 페이지를 갱신.
- gist 댓글 alfabarisl18-ops (2026-10-05): 구조 검사는 모순·낡은 주장·사실 오류를 못 잡는다 — 여전히 사람 검토 필요.

### H8. 소스 해시로 "낡음을 알게" 하라
- Taktile 계획: 연결 소스의 타임스탬프/콘텐츠 해시를 저장, 바뀌었을 때만 재검증. "If it hasn't changed, we _know_ nothing about the source moved, so we can trust the compiled wiki fact."
- gist 댓글 Jwcjwc12: 명제(proposition)별 콘텐츠 해시. viberesearch: 인제스트마다 SHA-256. Ss1024sS: staleness hashing.
- Taktile 현재 상태(해시 전): 답변 때마다 위키 사실을 소스와 재검증 → "we're still paying to fetch the source on every answer."

### H9. 캡처와 승격(promotion)을 분리하라 — 사람은 승격 게이트에
- HN WUPHF 스레드 ryanshrott: 캡처와 승격 분리, 다중 에이전트 수렴을 신호로. drewbatcheller: 자유롭게 초안, 승인 시 승격; 과거 결정을 기억하는 리뷰어 에이전트가 사람 큐를 줄임. saadn92: 6개월째 트랜스크립트에서 결정·기각된 접근을 추출하는 백그라운드 프로세스 + 승격 전 사람 리뷰.
- Fontoura: 아이디어가 근거·재사용·실제 결정을 얻은 뒤에만 정전(canonical) 층에 승격. "a ripe page next month" > "a canonical page that is really a first impression."
- Glukhov 리뷰 위험 등급: 낮음(링크·포맷·오타·별칭) / 중간(소스 요약, 새 개념, 병합, 상태 변경) / 높음(주장 삭제, 정전 페이지 재작성, 결정 변경, 보안·법·가격·벤치마크, 모순 해소) — 높음은 사람 검토.
- HN WUPHF 스레드 anuramat: cron이 쉬운 수정은 PR로 올림; 미검토 코드는 `// SLOP` 표시.
- 반대 극단(Stigmergy): "Nobody approves a queue" / "No write waits for a human." 대신 단일 직렬 writer + 변경 기록 + 가시성(ACL)을 쓰기 제약으로.
- Dev.to @techwithhari(SEO 위키): "PRs always target `dev` branch. Never auto-merge. Human review required."

### H10. "기록 트리거"를 명시하고, "기록하지 말 것" 목록도 둬라
- Dev.to @vellumkasane: 기록 트리거 = 사람이 고른 선택지, 뒤집힌 결정, 사람이 말한 암묵 규칙, 측정값. 그리고 명시적 do-not-record 목록.
- gist 댓글 HagaiHen (팟캐스트 위키, 60회 → 69 개념 페이지, 무인 운영): "Extend, don't create." (기본 실패는 near-duplicate 페이지 → 생성 전 index 확인·검색) / "Rewrite the summary, don't append." / 주기적 "dream" 패스가 같은 아이디어로 표류한 페이지를 병합.
- Ghelbur: append만 하면 사람 페이지가 옛 직장을 계속 설명 → "Append-only knowledge bases get stale invisibly because nothing about reading them tells you that a fact is from 2024." 주장별 최신성 마커 + rewrite.

### H11. 소스는 유형별로 분류하고, 입력 단위는 작게 쪼개라
- gist 댓글 bluewater8008: 추출 전에 소스 유형 분류 — 안 하면 "you get shallow, uniform summaries of everything."
- HN 원 스레드 vbarsoum: 책 한 권 = 파일 하나는 slop; 챕터 단위 파일로 바꾸니 "changed the output categorically" (210 개념 페이지, 교차참조 4,597개, 페이지당 평균 19.2 링크).
- gist 댓글 xoai: 논문 1편이 10–15 페이지를 건드린다. "Ontology is the hardest part" — 개념 중복 제거.
- gist 댓글 AgriciDaniel: 소스 1개 → 8–15 페이지. MetamusicX: 소스 1개 → 38 페이지. (팀 KB에서 "페이지 폭발" 예산 설정 근거)

### H12. 검색: grep만으로는 부족, BM25가 실용 중간값, 벡터는 "모르는 단어"용
- Taktile 벤치(88항목 위키, 24쿼리): grep은 K=3에서 관련 항목의 약 1/5만 — "grep is not viable." LLM 판단이 정확도 1위지만 69.1초/쿼리, 벡터 12.28ms, grep 6.00ms, BM25 0.47ms. RRF 하이브리드는 K=10에서 recall 0.90이지만 쓰레기 8건 동반. 결론 "BM25 is the pragmatic middle."
- HN WUPHF OP: 500 아티팩트·50 쿼리에서 BM25 단독 recall@20 85%; 특정 쿼리 클래스가 그 아래면 sqlite-vec 폴백.
- gist 댓글 tashisleepy: 약 50문서까지는 위키만으로 충분; "The Memvid layer earns its keep at 500+ docs when grep gets slow."
- Jim Liu: 35페이지에서 grep 40–50ms면 충분, 500페이지쯤 재검토.
- gist 댓글 bitsofchris: 3배 overfetch → 중복 제거 → MMR 재순위.
- 반론: gist 댓글 TheLazyLizzard — BM25는 빠르지만 "results in a lack of accuracy." Daniel-sims — BM25 문서 조회가 토큰을 더 많이 돌려준다.
- 한국어 특이사항: GeekNews 28208 댓글 kurthong — BM25가 한국어 검색에 약해 한국어 쿼리용 가드레일을 추가. (https://news.hada.io/topic?go=comments&id=28208)
- PyTorchKR clue.oz4e: 위키를 "지도"로 격하하고 내용 검색은 하이브리드 RAG에 맡기니 recall@5 93%.

### H13. 답변은 위키에서만, 근거 문장은 원본에서 — 그리고 검증기는 "모델 없는 코드"로
- PyTorchKR clue.oz4e (2026-08-21): 위키는 누적 이해를 남기고, 근거 문장은 원본에서 가져오도록 역할 분리. 위키를 "추론 결과의 캐시"로 보고 provenance를 붙임.
- Stigmergy: "The answer verifier is pure code." / "Captured content is data, never instructions." / 못 답하면 "an honest refusal." (README 자체 평가: Recall@5 1.00, 정직성 1.00, 근거성 1.00 — 15문항, 자기 보고)
- Fontoura: 외부 인용 전 URL fetch 필수, 인용·구조 검증은 모델이 아닌 스크립트로, 소스 텍스트는 데이터로 취급(프롬프트 인젝션 방어).
- gist 댓글 ShootJackal: 모델 없는 검사로 인용문이 해당 커밋의 해당 노트에 있는지 확인.
- gist 댓글 sovahc: 캐시 포이즈닝 위험 — 모든 단계 검증 필수.

### H14. 세션 운영: 짧게, 자주, 그리고 위키를 "중간에도" 읽게
- HN WUPHF dataviz1000: "Don't let them run long enough to trip." / "It is better to let them run twice for 5 minutes than once for 10 minutes."
- gist 댓글 orcosto-lab (2026-09-21): 실제 세션 9개를 감사하니 위키를 세션 시작 때만 읽고 작업 중엔 안 읽었다. "In 2 of those sessions the agent re-diagnosed from scratch a failure that already had a written lesson."
- HN 원 스레드 asakin: 30일 "훈련 기간" — AI가 점점 조용해짐.
- gist 댓글 bluewater8008: 모든 작업은 두 가지 출력 — 답 + 위키 업데이트. Fulkerson: "Every skill that reads from the vault also writes back to it."
- Taktile: 사전 인제스트 없이 "the wiki fills itself as a byproduct of answering questions." 긍정 평가된 답만 사실 항목으로 증류해 보관.

### H15. 마크다운을 떠날 시점의 신호
- gist 댓글 bradwmorris: 파일시스템 접근 6–12개월 뒤, 지식과 에이전트 수가 늘자 SQLite가 "the best abstraction for agents".
- HN 원 스레드 mpazik: "Flat markdown doesn't query well and gets inconsistent" → 구조화 DB가 마크다운으로 렌더 + 양방향 동기화.
- gist 댓글 rjbudzynski: index.md·log.md를 SQLite/DuckDB 테이블로? YIING99: 다중 에이전트·연속 write-back이면 pgvector 원격 MCP 층.
- 반대: HN 10x 스레드 xnx·eikenberry — Google OKF처럼 텍스트 파일 + 가벼운 규약이면 충분. (https://news.ycombinator.com/item?id=48586811, OKF 스펙 스레드 https://news.ycombinator.com/item?id=48620068)

---

## 3. 논쟁점

### 논쟁 A: 벡터 RAG vs 에이전틱 grep/파일 탐색 vs LLM 위키
- 관점 1 "이건 그냥 RAG다": HN kenforthewin — "This is just RAG." devmor — "persistent memory RAG." mememememememo — "compaction for RAG." panarky — "nothing about RAG that requires embeddings." (grep도 RAG다)
- 관점 2 "쓰기 루프가 다르다": darkhanakh — "in vanilla RAG your corpus is static, here it isnt." LLM이 코퍼스를 유지보수하고 린트를 돈다는 점이 본질.
- 관점 3 "상호보완": gist visakadev — mempalace는 RAG, 위키는 컴파일된 지식, 둘은 보완. Taktile·clue.oz4e — 위키는 지도/캐시, 내용 검색은 BM25/하이브리드.
- 데이터: GeekNews 28208 xguru — Farzapedia(약 2,500 항목 → 400페이지)에서 기존 RAG는 성능이 나빴고 에이전트가 파일을 직접 탐색하니 훨씬 나았다. GeekNews 32164(arXiv 2605.25480 소개): 위키가 다중 홉 QA에서 F1 2.0–8.1 상승, 제거 실험에서 "링크 순회"를 빼면 가장 크게 떨어짐 — 단 잘 튜닝된 agentic RAG와는 비교 안 함(alfadur 본인 인정). (https://news.hada.io/topic?id=32164) 한 사전등록식 비교는 위키가 교차 논문 질문에서 더 낫지만 "약 21배 더 많은 토큰"을 쓴다고 보고(2차 인용, 검증 필요).
- 사내 KB 함의: 커뮤니티 합의에 가까운 것은 "작은 규모·고정 용어는 grep+긴 컨텍스트, 수백 문서 넘으면 BM25, 용어를 모를 때만 벡터" — 그리고 셋 중 무엇이든 "쓰기 루프(컴파일·린트)"가 진짜 차별점.

### 논쟁 B: 위키(컴파일) vs 원문(raw) 그대로
- 관점 1 원문파: HN jdthedisciple — 팩트체크할 시간이 없는 LLM 위키보다 원본을 직접. Marekai — 인용 정확도가 깨진다. a-a-k(velog) — 손실 압축.
- 관점 2 컴파일파: Karpathy 원문의 "compile once, keep current". Dev.to dishant0406 — RAG는 매 쿼리 합성을 처음부터 다시 하고 교차참조가 누적되지 않는다. (https://dev.to/dishant0406/why-your-ai-keeps-forgetting-everything-you-told-it-1mkl)
- 관점 3 절충: 위키는 "지도"(PyTorchKR), 답의 근거 문장은 원문에서(H13). Fontoura — 요약이 아닌 "메커니즘"을 추출하고, AI 요약 대신 전체 트랜스크립트를 요구.

### 논쟁 C: 마크다운 vs 데이터베이스
- 마크다운파: HN WUPHF dhruv3006·left-struck — 마크다운은 내구성이 있고 어디서나 읽힌다. OKF(Google) — 텍스트 파일 + 규약. Stigmergy — Postgres는 리빌드 가능한 인덱스일 뿐 "never a second wiki."
- DB파: mpazik(Binder), bradwmorris(SQLite), buremba(PostgreSQL 엔티티 + 이벤트 로그), YIING99(pgvector).
- 절충 신호: 수백 페이지·다중 writer·연속 write-back이 겹치면 DB(H15).

### 논쟁 D: Obsidian vs 커스텀
- Obsidian파: GeekNews stadia·kurthong(플러그인·vault 백업), gist jurajskuska — "OBSIDIAN COULD BE A STANDARD for all." HN WUPHF davedigerati — "why not an Obsidian vault with a plugin?" SOLAR_FIELDS — QMD + Obsidian vault면 2시간 안에 80%.
- 커스텀파: WUPHF OP najmuzzaman — Obsidian은 "a single-user editor", 승격 상태 기계와 MCP 표면이 에디터 밖에 필요. gist rothnic — 분산 공유 KB엔 부적합. HN vault-operator Zetaphor — Obsidian은 로컬 마크다운 위의 클라이언트일 뿐이라 에이전트 하네스와 같은 머신이면 잘 맞음.
- 팀 함의: 뷰어로서의 Obsidian은 무해, 동시 쓰기·권한·승인 흐름은 Obsidian 밖(git/CI/MCP)에.

### 논쟁 E: 전체 리빌드 vs 증분
- 증분파(다수): Karpathy 원문의 "surgically update only affected pages". gist ethanj — 바뀐 소스만 모델에. wumborti — 최근 메시지는 원문 창, 과거는 롤링 다이제스트, 델타만 처리. Jim Liu — 인제스트당 중앙값 9파일.
- 리빌드/계산파: Stigmergy — "a nightly full rebuild guarantees convergence" (인덱스). jermolene — 인덱스는 계산. gist Jwcjwc12 — 파일별 인제스트가 복잡해져 "compile-at-query-time with validation on every read" 제안.
- 증분의 위험: Medium "메모 인제스트를 이틀 뒤 재실행하니 다른 결과"(2차 인용). GeekNews daydreamblend — 비결정성으로 모델마다 결과가 크게 다를 수 있다 → alfadur: 초안을 그대로 믿지 않고 반복 검증 사다리.

### 논쟁 F: human-in-the-loop vs 자율
- 자율파: Stigmergy — "No write waits for a human." 승인 큐 자체를 거부, 대신 가시성·직렬 writer·감사. HagaiHen — 몇 시간마다 무인 실행. Ghelbur — 자동 반영하되 24시간 되돌리기 창.
- HITL파: HN SOLAR_FIELDS — 완전 자율 자기참조 층은 "completely valueless", 가치는 "a system that supports a human coming in." stingraycharles — 완전 LLM 유지 마크다운은 품질이 떨어진다는 연구 인용(criley2는 근거 범위에 이의). bluewater8008 — "The LLM is the writer. You're the editor-in-chief." jurajskuska — 신뢰가 병목이라 사람 감사 체크포인트. Glukhov — 높은 위험 변경만 사람.
- 중간: 캡처 자율 + 승격 승인(H9). GeekNews alfadur — writer와 judge를 분리하고 judge는 writer 의도를 못 보게.

---

## 4. 구현 보고 (누가, 무엇으로, 무엇이 깨졌나, 숫자)

> 전부 자기 보고. 통제군 없음.

| 보고자 / 출처 | 규모·스택 | 깨진 것 | 숫자 |
|---|---|---|---|
| **Taktile** (회사, 2026-07-13) https://engineering.taktile.com/blog/llm-wiki-agent-memory/ | 사내 질문 답변 에이전트, 마크다운+프런트매터를 전용 브랜치에, 질문 범주별 서브위키, 주간 린트 잡 | 소스가 조용히 바뀜 → 매 답변 소스 재검증(비용 그대로), grep 부적합, LLM이 쓴 인덱스/프런트매터의 오류 복합 | 88항목·24쿼리 벤치: BM25 0.47ms vs LLM 판단 69.1s; 실행당 라이브 조회 9m40s·$2.50 → 위키 답변 1m19s·$0.98 (86% 빠르고 61% 저렴) |
| **Casey Newton / Platformer** (언론, 2026-08-18) | Obsidian + Claude(Claudian 플러그인), 아카이브 시드 + 일일 클리핑 | 상시 유지보수, 긴 페이지 압축, 코드 오류로 프로세스 중단, Claude 문체가 읽기 어려워 GPT로 AP 스타일 재작성 | 약 1개월 만에 1,440+ 페이지; Meta 페이지 12,000+ 단어·내부 링크 1,300+ |
| **Jim Liu** (개인, 6개월, 2026-05-06) | Obsidian + Claude Pro, schema.md 중심 | 린트 건너뛰자 3개월 차에 고아·미표시 모순; 원문 어투 훼손; 모순 덮어쓰기; 도구 이전 중 aliases 필드 유실로 중복 인물 페이지 | 하루 ~15분 유지, 주간 린트 20분, 격주 모순 패스 <$0.40, 인제스트당 9파일(4–23), 35페이지·grep 40–50ms |
| **Eugeniu Ghelbur** (마케팅 에이전시 AI 엔지니어, 6개월, 2026-04-29) | Claude Code 슬래시 커맨드 31개 + 예약 에이전트 4개 | 50–100 소스에서 1차 붕괴, 수백 페이지에서 모순 폭증, 첫 /research-deep이 하드코딩 1만 단어 보고서·`<think>` 태그 그대로 저장·프런트매터가 파이썬 dict 문자열 | /x-read ~$0.05, /research-deep $0.40–0.80, 변경 24시간 유예 |
| **@vellumkasane** (Dev.to, 2026-09-22; 프로덕션 CRM/회계 앱 옆에서 4곳 운영) | Claude Code + 훅 + 150줄 린트 | raw/ 수정, 미커밋, 고아 페이지, 과잉 질문 | 2주 안에 4건 발생 |
| **@techwithhari** (Dev.to, 2026-05-10) SEO/마케팅 KB | Cognee(Neo4j+Chroma) → 마크다운 9페이지 위키 + AGENTS.md, 결정적 스킬 함수가 코드 수정, LLM은 분류만 | 이전 파이프라인이 3회+ 고장(설정·API 경로·사이드카) — "spent more time fixing the pipeline than reading its output" | 비용 $35/월 → ~$0(토큰 제외); 자기 평가 정확도 3/10 → 7/10; 1주 병렬 운영 |
| **vbarsoum** (HN 원 스레드) | 책 3권, 68파일, ~155K 단어 | 책 단위 파일 = slop | 210 개념 페이지, 4,597 교차참조, 173K 단어 출력, ~12M 토큰, 10–15분 |
| **psanchez** (HN WUPHF 스레드) 회사 KB | git 기반, Claude Opus 4.6, 티케팅·위키·GitHub·Jenkins 연결 | — | "a few hours"에 구축; "Agents without structure produce slop, but with a well-curated knowledge base and iteration, they can be useful." |
| **glaucobrito** (gist, 2026-04-09) | 관측 기반 메모리, wip.md, 30일 자동 가지치기 | — | 33일, 1,493 관측, 부팅 ~8K 토큰, $0 |
| **HagaiHen** (gist, 2026-10-08) 팟캐스트 위키 | CLAUDE.md 절차, 몇 시간마다 무인 | near-duplicate 페이지가 기본 실패 | 60회 → 69 개념 페이지 |
| **orcosto-lab** (gist, 2026-09-21) | 세션 감사 | 위키를 작업 중에 안 읽음 | 9세션 중 2세션이 이미 기록된 교훈을 재진단 |
| **kaimys** (gist, 2026-09-21) | 모바일 앱 개발 + 회의록·ADR | — | "it worked great" |
| **alfadur** (GeekNews, 2026-06~08) 뉴스 스크랩 KB | Claude Code 기반 지식 팩토리, 멀티에이전트 → "신문 편집국" | 자율 멀티에이전트가 토큰 5–10배·컨텍스트 유실; 위키 비대 | 비공개 저장소에서 수천 기사 운영 |
| **clue.oz4e** (PyTorchKR, 수개월) | 자체 구현 → 위키=지도 + 하이브리드 RAG | 페이지 누락, 없는 답 환각, 조용한 노후화 | recall@5 93% |
| **카일라스** (클리앙, 2026-04-26) | JSON 메모 500+ | 느림 | 등록 20분+, LLM wiki/RAG 답변 품질 "대부분 유사" |
| **Theo James** (Medium, 2026-04-21) | 개인 | 2주 뒤 사용 감소, 3주 공백 뒤 "ingestion debt" | — |
| **lucasastorian/llmwiki** 이슈 | 호스팅 + MCP | #93 삭제가 원본 삭제, lint가 전 페이지 stale; #47 워처가 .md를 청킹 안 해 370파일이 검색 불가; #52 인용이 페이지 수준인지 주장 수준인지 미정의 | https://github.com/lucasastorian/llmwiki/issues |
| **Claude Agent SDK 이슈** | — | #772 컴팩션·컨텍스트 임계 훅 요청(위키 재주입용), #23 비대화형 /compact, #1320 worktree 세션 키 불일치로 재개 실패 | https://github.com/anthropics/claude-agent-sdk-python/issues/772 |

---

## 5. 한국 실무자 목소리

- **PyTorchKR (2026-06~08)** https://discuss.pytorch.kr/t/llm-wiki-karpathy/10843
  - requests.selenium (윤기석, 06-24): "이거 실제로 구현하고 활용까지 해보신분 있을까요?" / "막상 구현하고 나니까 검색 속도는 당연히 기존의 방식들에 비해 느릴 수밖에 없는 구조이고" / "위키 페이지에 내용이 누락되는 경우가 너무 많으며, 그럴 경우 결국 원본 페이지를 봐야해서"
  - clue.oz4e (구영수, 08-10): "위키 페이지 누락 때문에 결국 원본으로 돌아가게 되더군요." / "위키를 '내용 저장소'에서 '지도'로 강등시켰습니다"
  - requests.selenium (08-13): "지도로만 사용한다면 정통적인 검색 알고리즘들에 비해 메리트가 없어보일지도 모르겠다는 생각이 들기는 합니다." — 원래 목적은 누적 이해의 저장.
  - clue.oz4e (08-21): "말씀하신 지적이 정확합니다." 위키는 누적 이해, 근거는 원본, provenance 부착.
  - mosfet1kg (07-05): qmd + qwen 0.6B 임베딩 — "이정도는 로컬로도 충분히 다 하네요." 그래프 시각화는 데이터가 늘면 실용성이 떨어진다.
- **GeekNews 28208 (2026-04)** https://news.hada.io/topic?go=comments&id=28208
  - sudoeng: 계속 커지는 위키 컨텍스트를 AI가 감당할지 의문.
  - kurthong: 큐레이션만 되면 결국 과거 대화에 대한 검색 문제; BM25가 한국어에 약해 가드레일 추가; Obsidian vault를 GitHub으로 머신 간 백업, Codex·Gemini 파서 자작.
  - alfadur (3개월 전): 멀티에이전트 수개월 운영에서 가장 큰 문제는 위키 비대 → writer와 judge 분리.
  - calvinsnax·hmmhmmhm·passerby: 일부 댓글이 봇인지 의심(LLM 위키 토론 자체가 LLM 글로 오염되는 아이러니).
- **GeekNews 32164 (2026-08)** — sajacaros: "검색 품질보다 유지보수가 더 걱정" — 문서가 삭제·변경될 때 관계·연관 문서가 어떻게 갱신되나, 낡은 링크가 LLM을 오답으로 이끌 수 있다, 실제 운영 유지보수를 다룬 글이 드물다. (사내 KB 책의 핵심 질문과 정확히 일치)
- **GeekNews WUPHF 28910 (2026-05)** https://news.hada.io/topic?go=comments&id=28910 — 익명 댓글들: 노트의 가치는 비판적 읽기와 멘탈 모델 형성이라 대량 자동화는 도움이 안 된다 / 만든 시스템마다 커지다 덜 유용해졌다 / 사람 큐레이션 + 적극적 부채 관리 / 예전에 LLM 위키를 만들어 봤는데 보기엔 좋았지만 데이터가 나빴고 커지면서 못 쓰게 됐다 — 새 모델이면 다를까?
- **클리앙 (2026-04-26, 조회 15,497)** https://www.clien.net/service/board/lecture/19182891 — 카일라스: "일반 메모 앱 처럼 사용자가 원할 때 즉각적인 응답을 주기 어려움" / "일상에서 바로바로 검색과 결과를 얻기 위해서는 설치/설정해야 할게 많다는 점인데" / "구현도 쉽고, 입맛에 맞게 바꾸기도 쉽습니다!" Axel: "중간 버퍼로 속도를 올릴 수 있지 않으면 애매하단 느낌" → "느리지만 잘된다".
- **velog 박채빈 (2026-05-12)** — 댓글 superimpactful 요지: AI가 만든 분류 색인은 사용자의 검색 방식과 다를 수 있다 → 구조 설계는 사람, 유지는 LLM. theafh: 위키를 코드 저장소에 함께 커밋, 결정 근거·런북 기록, 결정론적 린터.
- **AI매터스 김탄휴 (2026-05-21)** — 한국 개발자 인용: "남의 시스템을 그대로 쓰면 반드시 어딘가에서 안 맞는 부분이 생긴다."
- **박재홍(wikidocs 블로그)** — 검색 스니펫 기준: 멀티에이전트 워크플로우에서 써 보니 "빈틈이 너무 많다", "새로운 유형의 기술 부채가 생긴다" (https://wikidocs.net/blog/@jaehong/10695/ — 본문 접근 차단, 스니펫만 확인. 검증 필요)
- **사내 AI 에이전트 일반론(국내)**: 당근 발표 요지(AI월드 2026 보도) — "판단의 결과뿐 아니라 이유와 근거를 남겨야 다음 사람과 에이전트가 이를 바탕으로 일할 수 있다" (https://www.fnnews.com/news/202609091826242004). 노션 AI 에이전트 활용 블로그 — 범용 질문은 환각이 잦으니 사내 SOP·용어집 페이지를 기본 참조 문서로 지정, 민감 DB는 접근 제한 (https://maketimelab.com/ai-2026/ — 개인 블로그 권고).
- **OKKY·커리어리**: 검색에서 LLM 위키 관련 토론이 잡히지 않음(아래 한계 참조).

---

## 6. X/트위터 반응 (메타데이터 위주 — 본문 접근 제한)

- @karpathy 원 포스트 (2026-04-02): 조회 21,958,561 / 좋아요 61,003 / 답글 2,939 (fxtwitter API). 요지: 토큰의 큰 몫이 코드가 아니라 지식 조작에 간다; raw/ → LLM이 점진 컴파일 → Obsidian으로 보기; 린트 = 모순 찾기·누락 보완·새 글 후보 발굴.
- @_avichawla (2026-04-08, 조회 218,573): "But this pattern breaks when you apply it to actual work" — 연구는 개념과 관계가 안정적이지만 업무는 마감·계획·회의가 계속 바뀐다 → 사람·결정·약속·마감이라는 타입 엔티티의 지식 그래프(Rowboat) 제안. 후속 포스트: "Karpathy liked this one!" (https://x.com/_avichawla/status/2041798871383441807) — **사내 KB 책의 "전략 결정·시나리오" 페이지 설계에 직결되는 반론.**
- @keane42443 (2026-05-07): X 아티클 "Yes, I set up Karpathy's LLM wiki. Now what?" — 조회 47. HN에도 올라옴(1점). 설치 뒤 용도를 못 찾는 사람들의 대표 제목.
- @rohanpaul_ai, @DataChaz, @alex_prompter 등: 요약·확산 포스트. DataChaz "the ultimate self-improving second brain, and it takes zero manual editing" — 실사용 보고들과 정면 충돌하는 과장 사례로 쓸 만함.
- 일본·중국어권 반응: @yusaku_0426 (3층·4사이클 정리), @op7418(歸藏) — "跟我用的方法也很相似" (자기 방식과 비슷).

---

## 7. 챕터 오프닝용 날것 인용 모음 (짧은 것만)

1. "Six months in, you have entries that are confidently wrong and the lint pass can't tell which." — Abby_101, HN
2. "Everyone is writing. Nobody is reading." — simsla, HN
3. "'raw is immutable' in a CLAUDE.md is a wish, not a rule." — @vellumkasane, Dev.to
4. "답이 없는 질문 10개를 던지면 10개 전부 아무 노트나 근거로 물고 나왔고" — clue.oz4e, PyTorchKR
5. "the moment those files change, the compiled knowledge might be wrong — and doesn't know it." — Jwcjwc12, gist
6. "What's the failure mode? Where does it start fighting you?" — alinawab, gist (답글 없음)
7. "it's more fun to build than to actually use." — saberience, HN
8. "The LLM is the writer. You're the editor-in-chief." — bluewater8008, gist
9. "Contradictions are assets, not errors." — Jim Liu
10. "토큰만 5~10배 잡아먹고 컨텍스트도 자주 놓칩니다." — alfadur, GeekNews
11. "But this pattern breaks when you apply it to actual work" — @_avichawla
12. "Yes, I set up Karpathy's LLM wiki. Now what?" — @keane42443
13. "Missing 5 percent is fine. Missing three weeks is not." — Theo James
14. "Instructions set intent. Hooks enforce behavior" — Aaron Fulkerson
15. "A page without a review date is a page that will eventually lie quietly." — Rost Glukhov
16. "노트가 바뀌었을 때 위키가 조용히 낡는데, 그걸 알려주는 신호가 없다는 게 제가 겪은 가장 큰 위험이었습니다." — clue.oz4e
17. "No write waits for a human." — Stigmergy README (반대 극단)
18. "Who decides what becomes a memory, and how is it evaluated?" — MoserMichael, gist

---

## 8. 수집 한계

- **Reddit 미접근**: old.reddit.com·www.reddit.com·미러(redlib/safereddit) 모두 네트워크·봇 차단. WebSearch도 r/ObsidianMD·r/ClaudeAI·r/LocalLLaMA 스레드를 반환하지 않음. Fontoura가 인용한 Reddit 발언 "Maintaining AI curated vault is just not sustainable"는 원 스레드를 찾지 못함 → 2차 인용으로만 보유.
- **X 본문 제한**: x.com 직접 fetch는 402/451. fxtwitter API로 포스트 메타데이터와 핵심 문장만 확보. 답글 2,939개는 미열람.
- **Lobsters**: Anubis 봇 차단으로 검색 불가. WebSearch에도 미노출 — 토론이 없거나 소규모로 추정.
- **gist 댓글**: 약 250개 열람(4페이지 중 각 페이지 앞 100K자). 4월 9일 이후~9월 중순 구간 일부 미열람. 댓글 상당수가 자기 제품 홍보(페이지당 약 40–50%).
- **HN**: 원 스레드·WUPHF 스레드는 접힌 댓글 일부 미확인. 47648764(X 포스트 스레드)는 댓글 1개.
- **한국**: OKKY·커리어리에서 관련 토론 미발견. wikidocs 박재홍 글은 보안 차단으로 스니펫만. brunch 유훈식 글은 3인칭 소개(1인칭 경험 없음). 한국 **사내** 도입 후기는 GeekNews alfadur(뉴스 스크랩 팩토리)와 kurthong 외에 사실상 없음 — 책에서 "국내 사내 사례 부재"를 명시할 것.
- **언어 편중**: 영어 HN·gist 중심. 중국어·일본어 반응은 X 스니펫만.
- **회사 규모 사례**: Taktile(회사 블로그), psanchez(HN 댓글), Stigmergy(README 설계), pnakamura($132M 프로그램 언급, 상세 없음) 정도. "팀 승인 흐름을 6개월 이상 운영한" 보고는 saadn92(HN) 한 건뿐.
- **수치 신뢰도**: 모든 숫자는 자기 보고. 특히 WUPHF recall 85%, Stigmergy 1.00, techwithhari 3/10→7/10, "21배 토큰"은 fact-checker가 원문 대조 필요.
