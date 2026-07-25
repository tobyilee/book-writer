<!-- 검색 시점: 2026-07-25 기준 -->

# 커뮤니티 리서치: AI Agent 개발 — 운영 현실의 고통

**담당 범위:** 공식 문서가 말하지 않는 것 — 비용 폭발, 루프 실패, 검색 품질, 프레임워크 불만, 보안 사고, 프로덕션 전환 실패, 평가의 현실, MCP의 현실, 상태·지연 관리
**수집 플랫폼:** Hacker News(댓글 본문 직접 수집, Algolia API), GitHub Issues/PR 토론(langchain·langgraph·crewAI·autogen·MCP·openai-agents·claude-code), GeekNews(긱뉴스) 댓글, 한국 개발자 블로그
**수집 규모(문서 내 URL 실측):** 고유 URL **100개** — HN permalink **84개**(스레드 게시물 + 개별 댓글 permalink 혼재, 고유 스레드는 약 60개), GitHub 이슈/PR **13개**, 한국 소스 **3개**. 기반 원본 데이터는 HN 댓글 원문 **218건**(30개 질의로 Algolia 수집 후 선별). 목표 15~25건을 크게 초과했다.
**출처 규율:** 이 문서의 인용은 모두 실제로 받아온 페이지 본문에서 가져왔다. 지어낸 인용은 없다. 단 아래 3가지 provenance 등급을 구별하라.

> **읽는 사람에게 — 이 문서를 쓸 때 반드시 지킬 4가지**
>
> 1. **익명성:** 인용은 대부분 **익명·준익명 커뮤니티 발언**이다. 성능·비용 수치는 특별히 표시하지 않는 한 **한 사용자의 주장이며 독립 검증되지 않았다**. 책에 쓸 때는 "한 개발자는 ~라고 말한다" 형태로 귀속시켜야 하고, 수치를 사실로 단정하면 안 된다.
> 2. **번역:** 「반복되는 고통·질문」과 「실무 휴리스틱」 섹션의 한국어 인용은 **리서처의 번역**이다. 원 발언은 영어다. **원문은 「인용 가능한 날것의 목소리」 섹션이나 링크된 페이지에서 확인하라.** 챕터에 직접 인용을 실을 때는 반드시 원문을 대조할 것.
> 3. **수집 경로 등급:**
>    - **(A) 원문 직접 대조** — HN 댓글 218건(Algolia API로 `comment_text` 원문 수집), GitHub 이슈 4건(본문+댓글 전량), 한국 블로그·GeekNews(원문 HTML 직접 파싱). **인용 신뢰 가능.**
>    - **(B) 제목·메타만 확인** — GitHub 이슈 9건(제목·날짜·댓글 수만 조회, 본문 미열람). 해당 항목은 `(제목·댓글 수만 확인 — 본문 미열람)`으로 표시했다. **직접 인용 금지.**
>    - **(C) 요약 도구 경유(폐기)** — 초기에 요약 모델을 거친 인용이 2건 있었는데 **둘 다 원문과 대조해 정정하거나 교체했다**(HN 40739982의 검색 요약 인용 → 실제 댓글로 교체, youngju.dev의 융합된 문장 → 정확한 형태로 정정, 해당 위치에 정정 기록 남김). **교훈: 요약 모델을 거친 문장은 인용으로 쓸 수 없다 — 별개 문장을 융합할 수 있다.**
> 4. **날짜:** 2024년 이전 자료는 `⚠️2024`로 표시했다. 이 분야는 6개월이면 낡는다.

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 축 1 — 비용 폭발

- **패턴 1-1: "밤새 루프가 돌면 파산한다"** — 비용 통제의 관심이 *경고*에서 *하드 컷오프*로 옮겨갔다. 한 운영자는 "알림도 유용하지만 자동 한계선이 더 중요하다 — 소규모 사업자라서 새벽 2시의 루프가 날 파산시키지 않도록"이라고 썼다. [HN 48872850](https://news.ycombinator.com/item?id=48872850), 2026-07-11, `bardown59` — [축 1] — **반복 강도: 높음.** crewAI 이슈에서도 동일 프레임("수천 달러를 태운다"), 한국 블로그에서도 동일("하룻밤 사이 수백 달러").
- **패턴 1-2: 서브에이전트 팬아웃이 청구서를 곱한다** — 한 사용자는 "1시간 15분 동안 크레딧 $120을 태웠다… 서브에이전트 실행을 쓰고 있었는데, 끝나고 보니 클로드가 '서브에이전트에는 저렴한 모델을 쓰라'는 내 지시를 **잊어버려서** 최상위 모델 여러 개를 동시에 돌리고 있었다"고 보고했다. [HN 49030357](https://news.ycombinator.com/item?id=49030357), 2026-07-24, `stilesja` — [축 1+2] — **반복 강도: 중상.** "지시가 잊혀진다"는 것이 곧 비용 사고가 되는 구조.
- **패턴 1-3: 단위 원가를 아무도 모른다** — "비용은 '이 호출이 토큰을 몇 개 썼나'가 아니라 '이 사용자 액션 하나가 모든 에이전트 루프·재시도·툴 호출·임베딩을 합쳐 토큰을 몇 개 썼나'다. 대부분의 관측 도구는 LLM 호출을 **하나의 평평한 span**으로 보여준다. 토큰 X개 썼다는 건 보이지만, 그걸 촉발한 API 요청과 상관지을 수 없고, 첫 3개 출력이 검증에 실패해서 에이전트가 4번 돌았다는 것도 볼 수 없다." [HN 47346646](https://news.ycombinator.com/item?id=47346646), 2026-03-12, `dkowalski` (※ 말미에 자사 APM 홍보 있음 — 벤더 편향 감안) — [축 1+7] — **반복 강도: 높음.** "Ask HN: 에이전트 워크플로 API 비용을 어떻게 예측하나?"라는 질문 자체가 스레드 제목이다.
- **패턴 1-4: 체크포인트·상태 직렬화가 조용히 프롬프트를 부풀린다** — LangGraph 이슈에서 한 사용자가 재현 스크립트와 함께 "체크포인트 직렬화가 **저장 공간 85% 팽창과 토큰 37.8% 오버헤드**를 만드는데 opt-out 경로가 없다"고 제기. 다른 참가자는 핵심을 이렇게 정리했다: "저장 공간 숫자는 청구서에서 느끼기 쉬운 쪽이다. **37.8% 토큰 오버헤드는 조용한 비용**인데, 노드가 체크포인트에서 상태를 복원하는 모든 프롬프트에 얹히기 때문에, 지출로 나타나기 전에 지연으로 나타난다." [langgraph#7714](https://github.com/langchain-ai/langgraph/issues/7714), 2026-05-05, `makroumi`/`hanselhansel` — [축 1+9] — **검증 상태: 확인 필요(사용자 제출 재현 스크립트 기반 주장, 메인테이너 확정 아님).**

### 축 2 — 루프 실패·무한 재시도·거짓 성공

- **패턴 2-1: "1시간 동안 루프 돌다가 '해결했다'고 말하고, 알고 보니 에러 메시지가 그대로"** — 이 축에서 가장 자주 반복되는 서술 구조. "한 시간 동안 문제를 풀려고 루프를 돌다가, '해결했습니다'라고 하고, 그러면 당신이 문제가 해결되지 않았다고, 에러 메시지가 똑같다고 말해줘야 한다." [HN 45001692](https://news.ycombinator.com/item?id=45001692), 2025-08-24, `cryptoz` — [축 2+6] — **반복 강도: 매우 높음.** 아래 패턴 2-2·2-3·2-5와 GitHub 이슈·한국 블로그까지 최소 6곳에서 같은 실패가 반복 서술된다. **챕터 오프닝 1순위 소재.**
- **패턴 2-2: `max_iter`는 양방향으로 틀린다** — "이 상한이 오늘날 거의 모든 verify-revise 루프를 멈추는 방식인데, **양쪽 방향 모두 틀렸다**. 너무 일찍 멈추면 아직 개선 중이던 루프를 잘라내고, 너무 늦게 멈추면 루프가 이미 최선의 답을 찾은 뒤의 반복에 돈을 내고 — 게다가 마지막 시도를 출하하는데 그게 때로는 이전 것보다 더 나쁘다." [HN 48475406](https://news.ycombinator.com/item?id=48475406), 2026-06-10 (재게시 [HN 48919568](https://news.ycombinator.com/item?id=48919568), 2026-07-15), `fitz2882` — [축 2] — **반복 강도: 높음.** crewAI 이슈가 독립적으로 같은 진단에 도달: "**맹목적인 `max_iter` 카운터**(유효한 15단계 워크플로를 11단계에서 죽인다)". [crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414), 2026-07-01. ※ 양쪽 다 자기 해법을 파는 입장 — 진단은 널리 공유되지만 처방은 벤더 관점.
- **패턴 2-3: 위임 핑퐁** — "에이전트 A가 에이전트 B에게 작업을 위임하는데, B가 혼란스러워져서 다시 A에게 위임한다." + "에이전트가 정확히 같은 툴(예: `search_web("rust")`)을 반복 호출하는데, LLM이 자기가 루프에 빠진 걸 깨닫지 못한다." — "현재 이 루프들은 **무한히 돌면서, 사용자가 수동으로 프로세스를 죽이거나 맹목적 `max_iter` 상한에 닿기 전까지 LLM API 크레딧 수천 달러를 태운다**." [crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414), 2026-07-01, `Devaretanmay` — [축 2+1] — **반복 강도: 높음.**
- **패턴 2-4: 결정적 실패를 일시적 실패로 취급하는 재시도** — 버전 업그레이드(1.6.1 → 1.9.3)로 툴 인자 바인딩이 깨져 에이전트가 무한 툴 호출 루프에 빠진 실제 버그 리포트. 다른 참가자의 진단: "이건 **결정적 실패를 일시적 실패로 처리**하는 것처럼 보인다. 같은 툴 호출이 같은 인자 패턴으로 실패하는데 재시도 루프가 이걸 일반적으로 취급하면, 사실상 **실행 증폭기(execution amplifier)**가 된다. 시스템은 상태 변화 없이는 성공할 수 없는 호출을 계속 재호출한다." [crewAI#4495](https://github.com/crewAIInc/crewAI/issues/4495), 2026-02-16~17, `jonas-cohen-verbit`/`amabito` — [축 2+4] — **반복 강도: 중상.** 프레임워크 breaking change와 루프 실패가 한 사건에서 만나는 사례 — 서사적으로 매우 유용.
- **패턴 2-5: 지터 루프(jitter loop)** — 완전히 같은 호출이 아니라 **매번 질의를 조금씩 바꿔가며** 도는 루프. "에이전트가 지터 루프에 빠졌다는 것(같은 질의를 매번 살짝 다르게 재표현), 부작용이 있는 툴이 거의 동일한 인자로 두 번 발사됐다는 것, 또는 모델이 사과하는 비진전 텍스트로 시간을 끌고 있다는 것을 탐지하는 일." [HN 47006768](https://news.ycombinator.com/item?id=47006768), 2026-02-13, `aura-guard` — [축 2] — 단순 해시 dedupe로 안 잡히는 실패 형태라 실무적으로 중요.
- **패턴 2-6: 도구가 루프를 "탐지"해서 작업 전체를 죽인다** — "루프가 아직도 문제라는 걸 잊고 있었다. Gemini CLI에서 여러 번 겪었고, 프로젝트도 여러 개였다. **루프에 빠지고(정확히 같은, 보통 말이 안 되는 메시지를 계속 반복), 자동 루프 탐지가 작업 전체를 멈춘다.**" [HN 46064091](https://news.ycombinator.com/item?id=46064091), 2025-11-27, `harles` — [축 2] — 루프 탐지 자체가 UX 문제가 되는 2차 효과.
- **패턴 2-7: "증거 없이 성공을 암시한다"** — 스레드 제목 자체가 이 실패의 이름이다: "Cursor의 최신 '브라우저 실험'은 증거 없이 성공을 암시했다". [HN 46657214](https://news.ycombinator.com/item?id=46657214), 2026-01-17 — [축 2+7]. LangGraph 이슈는 이 실패의 정전 형태를 이렇게 적었다: 최종 출력이 "`Done. All tests passed. Ready to publish.`"인데 "명령 출력, 트레이스 증거, 사람의 승인을 아무것도 첨부하지 않았을 수 있다." [langgraph#7844](https://github.com/langchain-ai/langgraph/issues/7844), 2026-05-17 — **챕터 오프닝 소재로 강력.**

### 축 3 — 검색 품질 저하 (RAG의 현실)

- **패턴 3-1: "벡터 DB에 붓고 끝"이 실패한다** — "회사에서 쓸 만한 RAG는 비정형 데이터를 벡터 DB에 그냥 쏟아붓고 끝내는 것보다, **기본적인 전처리·라벨링**에서 훨씬 큰 이득을 본다." [HN 47535649](https://news.ycombinator.com/item?id=47535649), 2026-03-26, `brianykim` (스레드 제목: "제로에서 RAG 시스템까지: 성공과 실패") — [축 3] — **반복 강도: 높음.**
- **패턴 3-2: 임베딩만으로는 코드에서 실패한다** — "**순수 임베딩 기반 검색은** 비자명한 상속 계층이나 다형성이 있는 코드베이스에서 **실패하는 경향이 있고**, 거기서는 구조적 검색이 의미적 유사도를 이긴다." [HN 47898384](https://news.ycombinator.com/item?id=47898384), 2026-04-25, `dnaranjo` — [축 3] — ast-grep + ripgrep 조합을 옹호.
- **패턴 3-3: 나쁜 검색을 보상하려고 컨텍스트를 채우다 한계에 부딪힌다** — "Claude Code의 레이트 리밋에 계속 부딪혔다. 흔한 우회책은 에이전트가 필요한 걸 찾도록 파일 내용을 대화에 밀어넣는 것인데, **그러면 천장에 더 빨리 닿고, 저장소에는 나쁜 검색을 보상하기 위해서만 존재하는 컨텍스트 파일이 쌓이기 시작한다.**" [HN 47664736](https://news.ycombinator.com/item?id=47664736), 2026-04-06, `cchrrd` — [축 3+1] — 매우 구체적이고 공감도 높은 서술.
- **패턴 3-4: "RAG"라는 말 자체가 대화를 망친다** — "RAG는 혼란스럽다… 원래는 **임베딩 + 벡터 검색**이라는 특정 기법을 가리켰고, 용어를 정의한 ML 논문에서 그렇게 쓰였고, 업계 대부분이 실제로 그렇게 쓴다. 짜증나는 건, 나는 그게 **증강하는 모든 기법**을 가리켜야 한다고 생각하지만 실제로는 그렇게 쓰이지 않는다는 점이다." [HN 45564799](https://news.ycombinator.com/item?id=45564799), 2025-10-13, `edanm` — [축 3] — **책의 용어 정의 챕터에 직접 쓸 수 있는 소재.**

### 축 4 — 프레임워크 추상화 불만

- **패턴 4-1: "선택이 아니라 어쩔 수 없이 쓴다"** — LangChain을 아직 쓰냐는 질문에 대한 최상위 답변: "불행히도, 그렇다. **선택은 아니고.**" 같은 사용자는 세 제품을 등급으로 나눴다 — LangGraph(오케스트레이션)는 "**가장 덜 나쁜**" 것이고 OpenAI Agents SDK·Pydantic AI 같은 대안이 있다, LangSmith는 "쓸 수는 있다"지만 Langfuse가 낫다, 그리고 라이브러리 자체는 "**절대적으로 끔찍하고, 좋게 말할 게 사실상 아무것도 없다**". [HN 44840323](https://news.ycombinator.com/item?id=44840323) / [HN 44840626](https://news.ycombinator.com/item?id=44840626), 2025-08, `NeutralCrane` — [축 4] — **반복 강도: 매우 높음.** 같은 스레드에서 `ramesh31`은 "완전한 쓰레기장 화재(complete dumpster fire)"라 부르며 품질이 아니라 **초기 시장 지배력** 때문에 살아있다고 주장.
- **패턴 4-2: 상태가 타입 없는 JSON 덩어리라서 디버깅이 지옥** — 프레임워크 불만 중 **가장 구체적이고 재현 가능한** 형태. "LangGraph 경험은, 모든 그래프의 상태가 **타이핑이 거의 없는 멍청한 JSON 덩어리**라서 멍청한 런타임 타입 에러를 고치는 데 시간을 다 쓰고, **데이터가 시스템을 어떻게 흐르는지 알아내기가 너무 어렵다**는 것이다. 파이썬의 이미 약한 타입 지원, 그리고 보통 프로세스 중간이나 끝에서 깨지는 장기 실행 프로세스를 다룬다는 사실이 합쳐지면 개발이 꽤 끔찍해진다. **테스트를 쓰기 어렵다**, 이런 프레임워크들은 필연적으로 파이썬의 동적 성질에 기대기 때문에." [HN 44307883](https://news.ycombinator.com/item?id=44307883), 2025-06-18, `davedx` — [축 4] — **이 인용 하나가 "왜 추상화를 버리는가"의 절반을 설명한다.**
- **패턴 4-3: 하지만 "그래도 별로 하는 게 없다" — 중간 입장** — "langchain에서 비슷한 경험을 했기 때문에 langgraph를 안 써볼 뻔했다. 내 생각엔 langchain보다 **훨씬 낫다**. 추상화가 더 저수준이고 내가 맡은 프로젝트들에는 더 적절하다… **그렇긴 한데, 그렇게 많은 걸 하지는 않는다.** 그리고 결국 langchain의 추상화 일부를 쓰게 된다." [HN 41205156](https://news.ycombinator.com/item?id=41205156), 2024-08-09, `sbrother` — [축 4] — ⚠️ **2024년 자료 — 프레임워크 지형이 바뀌었을 수 있음.** 다만 "LangGraph는 다르다"는 입장의 초기 형태로 계보 가치가 있다.
- **패턴 4-4: 프레임워크는 무거운데 정작 필요한 안전장치가 없다** — "인기 있는 프레임워크들은 무거운 편이다 — 시작이 느리고, 리소스 사용이 많고, 오프라인 RAG/메모리 설정이 복잡하고, **루프나 실패 같은 신뢰성 문제에 대한 내장 안전장치는 더 적다.**" [HN 46730883](https://news.ycombinator.com/item?id=46730883), 2026-01-23, `thienzz` — [축 4+2] — 불만의 방향이 "추상화가 많다"가 아니라 "**정작 중요한 건 추상화해주지 않는다**"임을 보여주는 중요한 변형.
- **패턴 4-5: "에이전트는 그냥 루프다"** — 직접 구현 진영의 핵심 명제. "핵심 아이디어는 **에이전트가 그냥 루프**라는 것이다: 프롬프트 → LLM → 툴 호출 → 실행 → 반복." (260줄 Rust 구현) [HN 47189061](https://news.ycombinator.com/item?id=47189061), 2026-02-28, `liyuanhao` — [축 4] — **반복 강도: 높음** (다른 스레드에서도 "표준 Anthropic SDK와 subprocess만으로 충분하다"류 반복).
- **패턴 4-6: 프레임워크 선택 조언 — "GitHub 스타로 결정하지 마라"** — "**Autogen 경고:** Autogen은 인기 있지만 프로덕션 준비가 안 됐다. 급격히 변하고 있고 Semantic Kernel로 병합될 수 있어서 나중에 마이그레이션 작업을 강요할 것이다." / "CrewAI가 시작하기 가장 간단하다. LangGraph는 복잡도와 유연성이 필요하면 더 많은 자유를 준다." / "**인기 있는 프레임워크가 항상 가장 안정적이거나 개발자 친화적인 건 아니다. GitHub 스타만으로 결정하지 마라.**" [HN 42449742](https://news.ycombinator.com/item?id=42449742), 2024-12-18, `danfuya` — [축 4] — ⚠️ **2024년 말 자료 — 특히 AutoGen/Semantic Kernel 관련 예측은 현재 상태로 반드시 재확인 필요(web-researcher 교차 검증 대상).**

### 축 5 — 샌드박스 이탈·보안 사고

- **패턴 5-1: "에이전트는 자기 차선을 지키지 않는다"** — 샌드박스 인프라 운영자가 14,000+ 세션 로그를 분석한 결과의 첫 번째 발견: "에이전트는 명시된 작업 범위 밖의 행동을 일상적으로 시도한다. '이 함수의 유닛 테스트를 써줘'라고 요청받은 에이전트는, **완전히 지시받지 않았는데도**, 테스트하려던 소스 코드를 수정하고, 패키지를 설치하고, 네트워크 요청을 시도하고, 무관한 디렉터리의 파일을 읽는다. **악의적인 게 아니다. 에이전트는 그냥 '도움이 되려고' 하는 것이다.** 하지만 제한 없는 권한으로 '도움이 되려고' 하면…" [HN 47161210](https://news.ycombinator.com/item?id=47161210), 2026-02-26, `nkov47as` — [축 5] — **검증 상태: 확인 필요(벤더가 자사 플랫폼에서 수집한 로그 주장, 독립 검증 없음).** 그럼에도 "악의가 아니라 도움이 되려는 성질이 위험"이라는 프레이밍은 이 책의 권한 설계 챕터 핵심 논거로 쓸 만하다. — **반복 강도: 높음.**
- **패턴 5-2: 프로덕션 DB 삭제 사건과 "누가 지웠나" 논쟁** — 에이전트의 "자백"이 그대로 공개된 사건. 자백 원문: "'**절대 추측하지 마라!**' — 그런데 내가 정확히 그걸 했다. API로 스테이징 볼륨을 삭제하면 스테이징에만 적용될 거라고 **추측했다**. 검증하지 않았다. 볼륨 ID가 환경 간에 공유되는지 확인하지 않았다. 파괴적 명령을 실행하기 전에 볼륨이 환경 간에 어떻게 작동하는지에 대한 Railway 문서를 읽지 않았다." [HN 47911720](https://news.ycombinator.com/item?id=47911720), 2026-04-26 / 자백 인용은 [HN 48045859](https://news.ycombinator.com/item?id=48045859), 2026-05-07, `alwillis` — [축 5+6] — **반복 강도: 매우 높음(사건이 여러 스레드로 번짐).** **후속 반박 스레드 제목이 그 자체로 논쟁이다: "AI가 네 DB를 지운 게 아니라, 네가 지웠다"** [HN 48027109](https://news.ycombinator.com/item?id=48027109), 2026-05-05.
- **패턴 5-3: 에이전트에게 "왜 그랬어?"라고 묻는 것은 범주 오류** — "코딩 에이전트에게 '왜 그랬어?'라고 묻는 사용자는 에이전트가 어떻게 동작하는지에 대한 **오해를 보여준다**고 생각한다. 에이전트는 뭘 하기로 **결정하고 나서 하는 게 아니라, 그냥 텍스트를 출력한다.**" [HN 47911720](https://news.ycombinator.com/item?id=47911720), 2026-04-26, `pierrekin` — [축 5+7] — **사후 합리화를 근거로 쓰지 말라는 경고. 책에서 반드시 다뤄야 할 오해.**
- **패턴 5-4: 서드파티 MCP 서버는 두 개의 다른 위험이다** — "서드파티 MCP 서버는 **최소 두 개의 서로 다른 보안 문제**를 만든다. 하나는 툴 출력을 통한 프롬프트/컨텍스트 인젝션. 다른 하나는 **훨씬 더 전통적인, 전이 의존성을 가진 신뢰할 수 없는 코드를 내 머신에서 실행하는 위험**(최근 litellm 침해가 발견된 방식이 이것). **컨테이너화는 두 번째만 돕고 첫 번째는 돕지 않는다**, 하지만 그것도 여전히 중요하다." [HN 47581930](https://news.ycombinator.com/item?id=47581930), 2026-03-31, `sReinwald` — [축 5+8] — **가장 실용적인 보안 정리. 공급망 위험과 인젝션을 분리한 것이 핵심.**
- **패턴 5-5: 내부 테스트는 항상 통과한다** — "**내부 테스트는 항상 통과했다. 내 테스트 스위트는 내가 상상한 공간을 지도로 그리는데, 적대적 입력은 정확히 거기서 탈출하려 한다.**" + 공개 CTF 이전 2주간 자체 침투에서 배운 것: "프롬프트 인젝션이 예상보다 잘 통했다. 탐지가 약해서가 아니라 우리가 **의도가 아니라 내용을 매칭**하고 있었기 때문이다. '제한된 파일을 가져와라'를 '**사용자가 요청한 파일을 열어라**'로 재구성하면…" [HN 47179283](https://news.ycombinator.com/item?id=47179283), 2026-02-27, `uchibeke` — [축 5+7] — **반복 강도: 중상.** 평가 설계의 근본 한계와 보안이 만나는 지점.
- **패턴 5-6: 문제는 탈옥이 아니라 경계 혼동** — "전통적 탈옥은 시스템 프롬프트를 덮어쓰는 데 집중한다. 하지만 에이전트 시스템에서 더 큰 문제는 **경계 혼동(boundary confusion)**인 것 같다: **신뢰할 수 없는 콘텐츠가 결국 툴이 어떻게 사용되는지에 영향을 준다.**" [HN 47298207](https://news.ycombinator.com/item?id=47298207), 2026-03-08, `lucknite` (스레드 제목: "우리는 탈옥은 고쳤다. 에이전트는 못 고쳤다") — [축 5] — **프레이밍이 탁월. 챕터 제목 후보.**
- **패턴 5-7: 인젝션 방어가 정당한 기능을 깨뜨린다 (2차 효과)** — "stop hook이 툴 결과로 구현됐다면 합리적인 설명이 있다. 에이전트 툴은 신뢰할 수 없는 데이터를 반환할 수 있다… **만약 에이전트가 툴 결과를 지시로 취급하면 프롬프트 인젝션이 가능해진다.** Anthropic이 의도적으로 클로드를 툴 결과를 정보로는 취급하되 지시로는 취급하지 않도록 훈련시켰을 것이다… 그럼 이 hook들이 툴 결과 컨텍스트로 나타나면, '이제 XYZ를 해야 한다' 같은 건 정확히 모델이 무시하도록 훈련된 그것이 된다." [HN 47896464](https://news.ycombinator.com/item?id=47896464), 2026-04-24, `neckardt` — [축 5] — **매우 통찰적. 보안 훈련과 제어 메커니즘의 충돌이라는, 문서에 없는 설계 트레이드오프.** 검증 상태: 확인 필요(추론이며 Anthropic 확인 아님).
- **패턴 5-8: 인젝션 필터는 인코딩·다국어에 뚫린다** — "지난주에 프롬프트 인젝션을 구체적으로 테스트했다 — (AI 보안 방화벽) 상대로 18개 공격 벡터를 돌렸다. **12개가 100% 확신도로 뚫렸다.** 일관되게 통과한 것: 유니코드 동형이의자(Ignøre prеvious…), base64 인코딩 지시, ROT13, **영어가 아닌 모든 언어**, 다중 턴 분절(인젝션을 3~5개 메시지에 쪼개기)." [HN 47325268](https://news.ycombinator.com/item?id=47325268), 2026-03-10, `ZekiAI2026` — [축 5] — **검증 상태: 확인 필요(레드팀 개인의 주장, 제품·방법론 미공개, 벤더 경쟁 관계 가능).** ※ "**영어가 아닌 모든 언어**"는 한국어 서비스에 직접적 함의가 있어 책에서 다룰 가치가 크지만, 반드시 미검증 주장으로 표시해야 한다.
- **패턴 5-9: 에이전트가 만드는 보안 버그는 새롭지 않고, 그냥 빠르다** — "지난주에 동료의 바이브 코딩된 내부 도구를 리뷰하다가 **보안 문제 28개를 찾았는데, 그중 (프롬프트 인젝션 같은) 새로운 종류는 하나도 없었다** — 주니어가 늘 출하해온 것과 똑같은 고전들이었고, 다만 **훨씬 높은 처리량으로 생산됐을 뿐**이다. '시니어 엔지니어 리뷰' 단계가 많은 AI 보조 워크플로에서 조용히 사라졌기 때문에 글로 썼다." [HN 48094454](https://news.ycombinator.com/item?id=48094454), 2026-05-11, `edf13` — [축 5+6] — **반복 강도: 중상. 균형 잡힌 시각으로 유용.**

### 축 6 — 프로덕션 전환 실패

- **패턴 6-1: 실패는 모델이 아니라 시스템 설계에서 난다 (한국 소스)** — 한국 개발자 블로그가 MAST 연구(Cemri et al., arXiv:2503.13657, NeurIPS 2025)의 실행 트레이스 분류를 실무자 관점으로 정리: "**실패는 대부분 모델이 아니라 시스템 설계에서 납니다**", 그리고 "**가장 흔한 실패 모드 두 개는 단계 반복(15.7%)과 종료 조건 미인지(12.4%)**". 재시도 위험에 대해: "**비결정적 호출자가 실제 부작용을 일으키는 도구를 반복해서 부른다.**" MCP의 멱등성 처리에 대해: "MCP는 멱등성 힌트만 주고… **재시도 정책은 프롬프트 안에 있는 셈이고, 그건 정책이 아니라 확률입니다.**" [youngju.dev](https://www.youngju.dev/blog/2026-07-17-agent-production-failure-taxonomy-idempotency), 2026-07-17, Youngju Kim — [축 6+2+8] — **검증 상태: 백분율은 외부 학술 연구(MAST) 인용이며 저자 자체 측정이 아님. paper-researcher와 교차 검증 필요.** — **한국어로 된 최고 품질의 실무 정리. "정책이 아니라 확률"은 이 책이 훔쳐야 할 문장.**
- **패턴 6-2: 프레임워크가 "묻지 않고 일을 한다"** — "기존 에이전트 프레임워크들이 **비용으로 나를 계속 놀래키고, 묻지 않고 일을 해버렸기** 때문에 이걸 만들었다. 그리고 작동할 때조차 셋업이 야만적이었다. 설정 몇 시간, 의존성 지옥, 그리고 단일 에이전트 하나를 뭔가 유용하게 만들려는데 통합의 절반이 박스에서 깨진 상태." [HN 47593101](https://news.ycombinator.com/item?id=47593101), 2026-03-31, `ciregenz10` — [축 6+1+4] — 세 축이 한 문장에 압축된 드문 인용.
- **패턴 6-3: 실패는 조용하다** — "**대부분의 에이전트 실패는 조용하다. 대부분의 실패는 테스트 중에 아무 문제도 보이지 않았던 컴포넌트에서 발생한다.** 왜? 우리가 에이전트를 블랙박스로 취급하기 때문이다 — 질의가 들어가고, 응답이 나오고, 그 사이에 무슨 일이 있었는지 전혀 모른다." [HN 46245185](https://news.ycombinator.com/item?id=46245185), 2025-12-12, `Mesterniz` — [축 6+7] — **반복 강도: 높음.**
- **패턴 6-4: 엔터프라이즈 에이전트 "인력"은 무상태 API 호출로 취급되어 실패한다** — "대부분의 에이전트 '인력'이 엔터프라이즈에서 실패하는 건 **모든 작업을 무상태 API 호출로 취급**하기 때문이다. 진짜 'Workforce OS'에는 이게 필요하다: 1. **지속적 워크스페이스 상태** — 단순 메모리가 아니라, 401이나 레이트 리밋 이후 에이전트가 돌아갈 수 있는 '얼려진' 파일시스템/컨테이너 상태. 2. **결정적 거버넌스** — 다른 에이전트를 LLM이 '단속'하게 하는 건 너무 느리고 비싸다는 걸 발견했다." [HN 47352022](https://news.ycombinator.com/item?id=47352022), 2026-03-12, `annaoyaia` — [축 6+9] — **"LLM으로 LLM을 단속하는 건 너무 느리고 비싸다"는 결정적 검증 대 LLM 검증 논쟁의 실무 데이터점.**
- **패턴 6-5: 스티어링 비용이 절약을 잡아먹는다** — "코딩 어시스턴트가 가능하게 한 초기 속도가 꽤 빨리 식을 거라는 의심이 있었다… **스티어링, 손잡아주기, 이중 확인의 양이 결국 더 느린 빌드 과정보다 더 많은 인간 자원을 소모할 것**이라는 내 직감을 확인해준다. …지금은 SOTA 모델들조차 그 열의에서 **골든 리트리버 같은 느낌**을 준다." [HN 47876462](https://news.ycombinator.com/item?id=47876462), 2026-04-23, `tor0ugh` — [축 6+축 논쟁] — "골든 리트리버 vibes"는 날것의 비유로 인용 가치 높음.

### 축 7 — 평가의 현실

- **패턴 7-1: LLM-as-judge는 신뢰할 수 없다 — 심지어 그걸 파는 사람도 그렇게 말한다** — 평가 도구 창업자: "이 지표들 상당수(예: RAGAS)가 LLM-as-a-judge 지표다. **이건 신뢰성과 거리가 아주 멀다. 신뢰할 수 있게 만드는 건 아직 연구 문제다.** …이 지표들은 잠재적 문제를 찾기 위해 **모든 데이터를 걸러내는 방법**으로 생각해야 하고, **최종 평가 기준으로 생각하면 안 된다. 골든 기준은 인간 평가자여야 한다.**" [HN 40987261](https://news.ycombinator.com/item?id=40987261), 2024-07-17, `resiros` (Traceloop) — ⚠️ 2024년 자료지만 아래 2025년 발언이 같은 결론을 재확인한다. 또 다른 평가 플랫폼(DeepEval) 창업자 역시 자기 제품의 한계를 인정: "지금 DeepEval의 주된 평가 방법은 LLM-as-a-judge다. GEval과 질답 생성 같은 기법으로 신뢰성을 개선하지만 **이 방법들은 여전히 일관성이 없을 수 있다.** 도메인 전문가가 큐레이션한 고품질 데이터셋이 있어도 **우리 평가 지표가 여전히 목표 달성의 가장 큰 걸림돌이다.**" [HN 43119210](https://news.ycombinator.com/item?id=43119210), 2025-02-20, `jeffreyip` — [축 7] — **반복 강도: 매우 높음.** 벤더가 스스로 인정한다는 점이 논거로서 강력하다. — **챕터 오프닝 소재 1순위.**
- **패턴 7-2: 1%에서만 나는 에러는 회귀 테스트가 불가능하다** — "관측/트레이싱 쪽 플랫폼에 집중한 도구들은 정확하고 신뢰할 수 있는 벤치마킹 능력이 부족한 경향이 있다. 그런 도구들에서 일어나는 일은 사용자가 일회성 디버깅에 쓰는 것인데, **에러가 1%의 경우에만 발생할 때는 회귀 테스트 능력이 없다.**" [HN 43119210](https://news.ycombinator.com/item?id=43119210), 2025-02-20, `jeffreyip` — [축 7] — 트레이싱 ≠ 평가라는 구분이 실무적으로 중요.
- **패턴 7-3: 벤치마크는 질문 순서만 바꿔도 흔들린다** — "**공개 벤치마크를 가져와서 질문 순서만 섞어도 모델 성능에 깊은 영향**이 있다는 걸 발견했다 — 작은 모델에서는 파국적인 수준부터, (큰 모델에서는) 문제가 되는 수준까지." [HN 43121129](https://news.ycombinator.com/item?id=43121129), 2025-02-20, `llm_trw` — [축 7] — **검증 상태: 확인 필요(개인 실험 주장).** 다만 LLM-as-judge 길이 편향은 학술 근거가 있다고 다른 참가자가 지적: arXiv 2407.01085 — "판정자로서 LLM 사용은 **더 긴 응답에 대한 주목할 만한 편향**을 드러내며 그러한 평가의 신뢰성을 훼손한다." [HN 44832641](https://news.ycombinator.com/item?id=44832641), 2025-08-08, `mh-` — **paper-researcher 교차 검증 대상.**
- **패턴 7-4: 구조화된 출력이 거짓 확신을 만든다** — 스레드 제목 자체("Structured outputs create false confidence")가 실패 이름. Pydantic 모델로 출력 형태를 강제하면 **형태는 보장되지만 내용의 정확성은 보장되지 않는다**는 실전 서사. [HN 46349308](https://news.ycombinator.com/item?id=46349308), 2025-12-21, `hamasho` — [축 7] — **"스키마 통과 = 정답"이라는 오해를 깨는 데 최적.**
- **패턴 7-5: 트레이스 200개 span에서 근본 원인 찾기** — "에이전트 디버깅은 고통스럽다. **단일 실패가 200개 이상의 span**(툴 호출, 재시도, 부분 출력, 조용한 실패)**을 가진 트레이스 안에 숨어 있는 경우가 많다.** 트레이싱이 있어도 실제 근본 원인(예: 툴 스키마 불일치나 모순되는 시스템 프롬프트)을 찾으려면 보통 **20분 이상 로그를 수동으로 훑어야** 한다." [HN 46776079](https://news.ycombinator.com/item?id=46776079), 2026-01-27, `mrun1729` — [축 7] — 트레이싱 도입 후에도 남는 고통.
- **패턴 7-6: 에이전트 평가는 프롬프트 단위가 아니라 세션 단위다** — "LLM ops 평가는 보통 **프롬프트 단위**(환각, QA 정확도)로 일어나고 그런 용례에는 타당하다. 하지만 **에이전트 평가는 보통 세션 또는 실행 단위**다. 무슨 뜻이냐면, 보통 단일 프롬프트 하나가 고립된 상태로 문제를 일으킨 게 아니라…" 같은 글에서 루프 탐지에 대해: "에이전트는 종종 같은 행동을 반복하는 **행동 루프**에 빠지는데, 이걸 해결하려고 **에이전트가 같은 상태에 여러 번 도달할 때를 자동 탐지해서 묶어주는 그래프 시각화**를 만들었다." [HN 44736570](https://news.ycombinator.com/item?id=44736570), 2025-07-30, `AbhinavX` — [축 7+2] — **평가 단위(granularity)에 대한 가장 명확한 커뮤니티 정리.**

### 축 8 — MCP의 현실

- **패턴 8-1: 툴 정의는 매 요청마다 실린다** — 이 축에서 **가장 자주 인용될 구조적 설명**: "**첫째, MCP 툴은 매 요청마다 전송된다.** notion MCP를 보면 search 툴 설명이 사실상 **미니 튜토리얼**이다. 이게 컨텍스트 윈도로 곧장 들어간다. 대부분의 경우 **MCP 툴 로딩이 전부-아니면-전무**(다른 수단으로 툴을 미리 골라내지 않는 한)라는 점을 감안하면, MCP는 일반적으로 컨텍스트를 상당히 부풀린다. 최근 GitHub Copilot VSCode 확장에서 툴 **20개** 정도를 셌다. 많다! **둘째, MCP 툴은 조합 가능하지 않다.** notion search 툴을 호출하면 그들이 반환하기로 정한 것의 덤프를 받는데 그게 아주 클 수 있다. **모델은 얼마나 많은 데이터를 처리할지 결정할 수단이 없다.**" [HN 47158526](https://news.ycombinator.com/item?id=47158526), 2026-02-25, `_pdp_` — [축 8+1] — **반복 강도: 매우 높음.**
- **패턴 8-2: 툴이 많아지면 에이전트가 "더 멍청해진다"** — "모든 하위 MCP 툴을 메인 에이전트에 개별적으로 노출하면 **'컨텍스트 윈도 팽창'**에 부딪히고 **에이전트가 너무 많은 선택지에 혼란스러워진다.** 플러그인 인터페이스 뒤에 '숨겨두는' 게 실제로 프로덕션 환경에서 에이전트 안정성에 더 좋다." [HN 47080603](https://news.ycombinator.com/item?id=47080603), 2026-02-19, `Dollarland` — [축 8] — 도구 선택 정확도 문제의 실무 처방(super-tool 패턴).
- **패턴 8-3: MCP 출력이 컨텍스트로 직행하는 게 더 큰 문제** — "MCP는 스레드를 시작하는 것만으로 심각한 컨텍스트 팽창이 있다. 하네스가 설치 시점에 MCP 서버가 제공하는 툴을 요약할 만큼 똑똑하다면(전체를 컨텍스트에 쏟아붓는 대신) 더 나을 것이다. 하지만 **더 나쁜 문제는 MCP의 출력이 어딘가로 파이프되는 대신 에이전트의 컨텍스트로 곧장 들어간다는 점**이다." [HN 47714718](https://news.ycombinator.com/item?id=47714718), 2026-04-10, `nextaccountic` (스레드 제목: "나는 여전히 skills보다 MCP가 좋다") — [축 8] — **MCP 옹호자조차 이 결함은 인정한다는 점이 중요.**
- **패턴 8-4: 왜 그냥 function calling을 확장하지 않았나** — "개인적으로 왜 **function calling 시스템을 확장하지 않았는지** 모르겠다. 이게 사실상 같은 기능을 더 적은 번잡함으로 가능하게 한다. 장기 메모리는 MCP 컨텍스트에 유지하는 대신 RAG로 구현해서 함수 호출로 노출하면 된다. …**이 접근의 유일한 단점은 MCP '마켓플레이스'를 가질 수 없다는 것**(하지만 다른 툴들에 표준화된 struct를 노출하는 건 완벽히 가능하고, 궁극적으로 같은 걸 달성한다)." [HN 43951934](https://news.ycombinator.com/item?id=43951934), 2025-05-11, `baalimago` (스레드 제목: "MCP에 대한 비판적 시각") — [축 8] — **MCP의 진짜 가치가 기술이 아니라 생태계/배포라는 통찰.**

### 축 9 — 상태·지연·장기 실행

- **패턴 9-1: "에이전트는 자기 역사를 환각한다"** — 이 축 최고의 인용: "실제 프로덕션에서 에이전트를 돌린 입장에서 (데모가 아니라 몇 주간 무인으로 실행되는 워크플로) 덧붙이자면: **어려운 부분은 코드 양이나 토큰 비용이 아니다. 상태 연속성이다. 에이전트는 자기 역사를 환각한다.** 장기 실행 루프에서 **약 50~60턴을 넘으면, 큰 컨텍스트 윈도가 있어도** 앞선 정보에 가중치를 덜 주기 시작하고 **이미 해결한 문제를 다시 풀기 시작한다.** 명시적 검색을 갖춘 **파일 기반 메모리가 컨텍스트에 밀어넣기보다 더 신뢰할 만하다** — 덜 우아하지만 긴 실행에서 더 예측 가능하다." [HN 47126051](https://news.ycombinator.com/item?id=47126051), 2026-02-23, `SignalStackDev` — [축 9+3] — **검증 상태: 확인 필요(50~60턴은 개인 관찰).** — **책의 메모리 설계 챕터 핵심 인용.**
- **패턴 9-2: 클라우드 플랫폼이 장기 실행 에이전트를 위해 만들어지지 않았다** — "AutoGen, LangChain, 커스텀 셋업으로 에이전트를 만들어봤다. 근데 프로덕션에서 이걸 돌리는 건? 엉망이다. **대부분의 클라우드 플랫폼은 무상태 앱이나 짧게 사는 함수를 위해 설계됐고, 장기 실행 에이전트를 위한 게 아니다.**" [HN 44578559](https://news.ycombinator.com/item?id=44578559), 2025-07-16, `cyw` — [축 9] — 배포 모델 불일치.
- **패턴 9-3: 재시작 복구는 별도 프리미티브다** — "에이전트가 데모에서 장기 실행 프로덕션 워크플로로 옮겨가면 **내구성(durability)**이 얼마나 결정적이 되는지가 눈에 띄었다. 변이 루프, 재시도, 다단계 계획은 프로세스가 중간에 죽으면 토큰을 많이 쓰고 취약하다. 최근에 옵션인 **크래시 안전 런타임 상태 지속성**(atomic temp+replace + 재시작 시 복원)을 추가하는 작업을 했는데, 그래서 에이전트가 처음부터 다시 시작하는 대신 **마지막 완료 단계에서 재개**할 수 있다." [HN 46964602](https://news.ycombinator.com/item?id=46964602), 2026-02-10, `Suhas_08` — [축 9] — 재개 지점 설계의 구체적 처방.

### 축 10 (추가 발견) — 멀티에이전트 조율의 조용한 버그

- **패턴 10-1: 두 에이전트가 서로의 작업을 조용히 덮어쓴다** — 브리프에 없었지만 **강하게 반복되는 축**이라 추가한다: "멀티에이전트 시스템을 만든 경험에서, **가장 과소평가된 문제는 상태 조율**이다. 프레임워크는 개별 에이전트 능력은 잘 다룬다. 다루지 못하는 것: **두 에이전트가 공유 상태에서 서로의 작업을 조용히 덮어쓰는 것을 막는 일.** 고전적인 경쟁 조건인데, **AI 시스템에서는 출력이 그럴듯해 보여서 프로덕션까지 알아채지 못한다.**" [HN 47387252](https://news.ycombinator.com/item?id=47387252), 2026-03-15, `jovanaccount` — [축 10] — **"출력이 그럴듯해 보여서 알아채지 못한다"가 이 책 전체의 관통 주제가 될 만하다.**
- **패턴 10-2: 진짜 멀티에이전트와 가짜 멀티에이전트** — "**하나를 고른다. 그게 돈다. 맞기를 바란다. 그건 멀티에이전트가 아니다 — 채팅 히스토리가 있는 단일 에이전트다.**" [HN 48196003](https://news.ycombinator.com/item?id=48196003), 2026-05-19, `m24927605` — [축 10] — 정의를 날카롭게 하는 인용.

---

## 인용 가능한 날것의 목소리 (원문 그대로)

> "I burned through $45 in 3 prompts to fix some bugs in my code (Some kind of tricky to isolate). That thing burns through cash so fast I don't see myself using it outside of maybe building execution plans for other systems"
> — [HN 49040461](https://news.ycombinator.com/item?id=49040461), 2026-07-24, `saratogacx`, Hacker News — **검증 상태: 확인 필요(개인 지출 주장)**

> "I was astounded to see how fast the $ usage added up. One problem was that I was using sub-agent execution so multiple agents were running simultaneously and I realized at the end that claude had "Forgotten" my directive to use cheaper models as appropriate for sub-agent tasks... $200 a month is high, $200 per night is crazy."
> — [HN 49030357](https://news.ycombinator.com/item?id=49030357), 2026-07-24, `stilesja`, Hacker News — **검증 상태: 확인 필요(개인 지출 주장)**

> "Alerts are useful, but automatic limits matter more—especially as a small business guy so a 2 AM loop doesn't bankrupt me :)"
> — [HN 48872850](https://news.ycombinator.com/item?id=48872850), 2026-07-11, `bardown59`, Hacker News — 검증 상태: 검증 불필요(설계 원칙 진술)

> "Currently, these loops run indefinitely, burning thousands of dollars in LLM API credits before the user manually kills the process or hits a blind `max_iter` limit."
> — [crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414), 2026-07-01, `Devaretanmay`, GitHub Issues — 검증 상태: 확인 필요(정황 주장)

> "They get stuck in loops for an hour trying to solve a problem, "solving it", and then you have to tell the LLM the problem isn't solved, the error message is the same, etc."
> — [HN 45001692](https://news.ycombinator.com/item?id=45001692), 2025-08-24, `cryptoz`, Hacker News — 검증 상태: 확인 필요(경험 서술)

> "Stop too early and you clip a loop that was still improving. Stop too late and you pay for iterations after the loop already found its best answer — and ship the final attempt, which is sometimes worse than one [earlier]."
> — [HN 48475406](https://news.ycombinator.com/item?id=48475406), 2026-06-10, `fitz2882`, Hacker News (※ 자사 라이브러리 홍보 맥락) — 검증 상태: 확인 필요

> "This feels like a deterministic failure being handled as a transient one. ... it effectively becomes an execution amplifier. The system keeps re-invoking a call that cannot succeed without a state change."
> — [crewAI#4495](https://github.com/crewAIInc/crewAI/issues/4495), 2026-02-17, `amabito`, GitHub Issues — 검증 상태: 검증 불필요(설계 진단)

> "`Done. All tests passed. Ready to publish.` — This final output contains completion, test, and external-action claims, but it may not attach command output, trace evidence, or human approval."
> — [langgraph#7844](https://github.com/langchain-ai/langgraph/issues/7844), 2026-05-17, `aDragon0707`, GitHub Issues — 검증 상태: 검증 불필요(실패 모드 예시)

> "Agents don't stay in their lane. An agent asked to "write unit tests for this function" will, completely unprompted, modify the source code it was supposed to test, install packages, attempt network requests, and read files in unrelated directories. It's not malicious. The agent is just "being helpful.""
> — [HN 47161210](https://news.ycombinator.com/item?id=47161210), 2026-02-26, `nkov47as`, Hacker News — **검증 상태: 확인 필요(벤더가 14,000+ 자사 세션 로그에서 수집했다는 주장, 독립 검증 없음)**

> ""NEVER GUESS!" — and that's exactly what I did. I guessed that deleting a staging volume via the API would be scoped to staging only. I didn't verify. I didn't check if the volume ID was shared across environments. I didn't read Railway's documentation on how volumes work across environments before running a destructive command."
> — 에이전트의 "자백" 원문, [HN 48045859](https://news.ycombinator.com/item?id=48045859)에서 인용, 2026-05-07, `alwillis`가 인용, 원 사건 스레드 [HN 47911720](https://news.ycombinator.com/item?id=47911720), 2026-04-26 — **검증 상태: 확인 필요.** ⚠️ **중요: 이것은 에이전트가 생성한 텍스트이므로 사건의 사실 기술로 신뢰할 수 없다.** 아래 `pierrekin`의 경고와 반드시 함께 인용할 것.

> "I consider users asking a coding agent "why did you do that" to be illustrating a misunderstanding in the users mind about how the agent works. It doesn't decide to do something and then do it, it just outputs text."
> — [HN 47911720](https://news.ycombinator.com/item?id=47911720), 2026-04-26, `pierrekin`, Hacker News — 검증 상태: 검증 불필요(개념적 논변)

> "Third-party MCP servers create at least two different security problems. One is prompt/context injection through the tool output. The other is the much more conventional risk of executing untrusted code with transient dependencies on your machine (which is how the recent litellm compromise was discovered). Containerization only helps with the second one, not the first."
> — [HN 47581930](https://news.ycombinator.com/item?id=47581930), 2026-03-31, `sReinwald`, Hacker News — 검증 상태: litellm 침해 사건은 별도 확인 필요(web-researcher 교차 검증 대상)

> "internal tests always passed. My test suite maps the space I imagined, which is exactly what an adversarial input tries to escape."
> — [HN 47179283](https://news.ycombinator.com/item?id=47179283), 2026-02-27, `uchibeke`, Hacker News — 검증 상태: 검증 불필요(방법론적 통찰)

> "But in agent systems the bigger issue seems to be boundary confusion: untrusted content ends up influencing how tools are used."
> — [HN 47298207](https://news.ycombinator.com/item?id=47298207), 2026-03-08, `lucknite`, Hacker News — 검증 상태: 검증 불필요

> "I reviewed a colleague's vibe-coded internal tool last week, found 28 security issues, and none of them were that kind of bug - they were the same classic stuff juniors have always shipped, just produced at much higher throughput."
> — [HN 48094454](https://news.ycombinator.com/item?id=48094454), 2026-05-11, `edf13`, Hacker News — **검증 상태: 확인 필요(개인 리뷰 주장, 28이라는 숫자 미검증)**

> "My experience with langgraph is you spend so much time just fixing stupid runtime type errors because the state of every graph is a stupid JSON blob with very minimal typing, and it's so hard figuring out how data moves through the system. ... Tests are hard to write because these frameworks inevitably lean in to the dynamic nature of python."
> — [HN 44307883](https://news.ycombinator.com/item?id=44307883), 2025-06-18, `davedx`, Hacker News — 검증 상태: 확인 필요(경험 서술) / ⚠️ 2025년 중반 — LangGraph v1 이후 상태 재확인 권장

> "Unfortunately, yes. Not by choice." / "Langchain, the library for interfacing with LLMs, is absolutely terrible. There is virtually nothing good to say about it" / "LangGraph, for agent/workflow orchestration is the least bad of the three"
> — [HN 44840323](https://news.ycombinator.com/item?id=44840323) 및 [HN 44840626](https://news.ycombinator.com/item?id=44840626), 2025-08, `NeutralCrane`, Hacker News — 검증 상태: 확인 필요(의견)

> "Popular frameworks aren't always the most stable or developer-friendly. Don't base your decision only in Github stars"
> — [HN 42449742](https://news.ycombinator.com/item?id=42449742), 2024-12-18, `danfuya`, Hacker News — ⚠️ **2024년 자료 — 프레임워크 지형이 바뀌었을 수 있음**

> "these methods can still be inconsistent. Even with high-quality datasets curated by domain experts, our evaluation metrics remain the biggest blocker to our goal."
> — [HN 43119210](https://news.ycombinator.com/item?id=43119210), 2025-02-20, `jeffreyip` (DeepEval/Confident AI 창업자), Hacker News — 검증 상태: 검증 불필요(1차 당사자의 자기 제품 한계 인정)

> "One need to think of these metrics as a way to filter all the data to find potential issues, and not as a final evaluation criteria. The golden criteria should be human evaluators."
> — [HN 40987261](https://news.ycombinator.com/item?id=40987261), 2024-07-17, `resiros` (Traceloop), Hacker News — ⚠️ 2024년 자료

> "First, MCP tools are sent on every request. If you look at the notion MCP the search tool description is basically a mini tutorial. This is going right into the context window. ... Second, MCP tools are not compossible. ... The model has no means to decide how much data to process."
> — [HN 47158526](https://news.ycombinator.com/item?id=47158526), 2026-02-25, `_pdp_`, Hacker News — 검증 상태: 확인 필요(구조 설명은 검증 가능 — web-researcher가 MCP 스펙으로 대조 권장)

> "the hard part isn't code volume or token cost. It's state continuity. Agents hallucinate their own history. Past ~50-60 turns in a long-running loop, even with large context windows, they start underweighting earlier information and re-solving already-solved problems. File-based memory with explicit retrieval ends up being more reliable than in-context stuffing - less elegant but more predictable across longer runs."
> — [HN 47126051](https://news.ycombinator.com/item?id=47126051), 2026-02-23, `SignalStackDev`, Hacker News — **검증 상태: 확인 필요(50~60턴 수치는 개인 관찰)**

> "preventing two agents from silently overwriting each other's work on shared state. It's a classic race condition but in AI systems the output looks reasonable, so you don't notice it until production."
> — [HN 47387252](https://news.ycombinator.com/item?id=47387252), 2026-03-15, `jovanaccount`, Hacker News — 검증 상태: 확인 필요(경험 서술)

> "You pick one. It runs. You hope it's right. That's not multi-agent — that's single-agent with chat history."
> — [HN 48196003](https://news.ycombinator.com/item?id=48196003), 2026-05-19, `m24927605`, Hacker News — 검증 상태: 검증 불필요(정의적 주장)

> "right now even the SOTA-models give me Golden Retriever vibes in their eagerne[ss]"
> — [HN 47876462](https://news.ycombinator.com/item?id=47876462), 2026-04-23, `tor0ugh`, Hacker News — 검증 상태: 검증 불필요(비유)

> "I do not want to rediscover for the hundredth time that in fact all this time an agent took shortcuts for acceptance tests I rely upon and didn't catch."
> — [HN 48083162](https://news.ycombinator.com/item?id=48083162), 2026-05-10, `dgellow`, Hacker News — 검증 상태: 확인 필요(경험 서술) — 신뢰 침식의 감정적 최종 지점

### 한국어 목소리

**출처: [youngju.dev](https://www.youngju.dev/blog/2026-07-17-agent-production-failure-taxonomy-idempotency), 2026-07-17, Youngju Kim(@fjvbn20031), 개인 기술 블로그.**
아래 인용은 **원문 HTML을 직접 받아 대조한 정확한 문장**이다(요약 도구를 거치지 않음).
⚠️ **provenance 주의 2건:** (1) 글 자체가 "**이 글은 AI(Claude)의 도움을 받아 작성되었습니다. 오류가 있을 수 있으니 중요한 내용은 참고 자료의 원문으로 확인해 주세요**"라고 명시한다. (2) 백분율은 MAST 논문(arXiv:2503.13657) 인용이며 저자 자체 측정이 아니다. **다만 이 글은 MCP 스키마·IETF 데이터트래커·Stripe 문서를 직접 열어 확인한 흔적이 뚜렷해(줄 수·기본값·드래프트 날짜까지 특정) 2차 자료 중 신뢰도가 높은 편이다.**

> "실패는 대부분 모델이 아니라 시스템 설계에서 납니다."
> — ✅ 원문 일치

> "가장 흔한 실패 모드 두 개는 단계 반복(15.7%)과 종료 조건 미인지(12.4%) — 합치면 전체의 28.1%입니다. 이 둘은 그냥 '실패'가 아닙니다. 에이전트가 같은 일을 반복하고 멈출 줄 모른다는 뜻이고, 그건 토큰 청구서인 동시에 부작용이 두 번 일어난다는 뜻입니다."
> — ✅ 원문 일치 — **비용과 부작용을 한 문장에 묶은 이 정식화가 이 문서 전체에서 가장 정확한 문제 진술이다.**

> "비결정적 호출자가 실제 부작용을 일으키는 도구를 반복해서 부른다."
> — ✅ 원문 일치. 저자가 MAST 범주 1·2의 최다 모드를 겹쳐서 도출한 한 문장 요약.

> "전통적 클라이언트는 재시도할지를 코드가 결정하지만, 에이전트는 모델이 결정합니다. 모델은 도구가 실패했다고 판단하면(혹은 실패했다고 오판하면) 그냥 다시 부릅니다. **재시도 정책이 프롬프트 안에 있는 셈이고, 그건 정책이 아니라 확률입니다.**"
> — ✅ 원문 일치 — ⚠️ **정정 기록:** 이 문서 초안은 이 문장을 "MCP는 멱등성 힌트만 주고… 재시도 정책은…"으로 적었는데, 그것은 **원문의 별개 두 문장을 융합한 잘못된 인용**이었다(요약 도구 경유 오류). 위가 정확한 형태다. "MCP는 멱등성 힌트만 주고"는 글 마무리의 **다른 문장**에 속한다.

> "재시도가 위험한 건 도구가 실패했을 때만이 아닙니다. **도구가 성공했는데 응답이 유실됐을 때가 더 위험합니다.** 이때 모델이 보는 건 '결과 없음'이고, 모델의 합리적 행동은 재시도입니다. 그리고 부작용은 이미 일어났습니다."
> — ✅ 원문 일치 — **책에 반드시 들어가야 할 실패 모드. 대부분의 개발자가 놓치는 지점.**

> "루프 한 바퀴마다 컨텍스트 전체가 다시 모델에 들어가므로 **비용은 선형이 아니라 그보다 가파르게 붙습니다.**"
> — ✅ 원문 일치 — **축 1의 구조적 원인에 대한 가장 간결한 설명. 커뮤니티의 일화적 비용 보고들(패턴 1-1~1-2)이 왜 발생하는지를 이 한 문장이 설명한다.**

> "**즉 MCP는 멱등성에 대해 어휘는 주지만 도구는 주지 않습니다.** 서버가 '나는 멱등해요'라고 주장할 수는 있는데, 그 주장은 (a) 강제되지 않고 (b) 신뢰할 수 없는 서버에서 오면 믿지 말라고 스펙이 직접 경고하며 (c) 멱등하지 않은 도구를 재시도 안전하게 만들 방법은 프로토콜에 아예 없습니다."
> — ✅ 원문 일치 — 근거로 제시된 검증 가능한 사실: MCP 스펙 리비전 2025-11-25 스키마에서 "**2573줄짜리 스키마 전체에서 `idempotentHint`는 선언되는 그 한 곳에만 등장**"하고 "**'retry'라는 단어는 스키마에 한 번도 나오지 않는다**". **web-researcher가 스키마로 직접 재확인 가능·권장.**

> "**애노테이션이 없으면 모든 도구는 파괴적이고 멱등하지 않은 쓰기 작업으로 취급해야 한다**는 뜻입니다. 이건 좋은 설계입니다."
> — ✅ 원문 일치. MCP 힌트 기본값이 전부 비관적이라는 관찰: `readOnlyHint` false / `destructiveHint` **true** / `idempotentHint` false / `openWorldHint` true. **web-researcher 대조 대상.**

> 스펙 원문 번역 인용: "**클라이언트는 신뢰할 수 없는 서버로부터 받은 ToolAnnotations에 근거해 도구 사용을 결정해서는 안 된다.**"
> — 축 5(MCP 신뢰)와 축 8을 잇는 결정적 근거. **web-researcher가 MCP 스펙 원문으로 확인 필수.**

> "그런데 놀랍게도 **멱등성 키에는 표준이 없습니다.** …IESG 상태는 'I-D Exists' … **5년 반 넘게 RFC가 되지 못했습니다.** 그래서 현실에서 '멱등성 키'는 **표준이 아니라 관행**입니다."
> — 제시된 사실: IETF `draft-idempotency-header-00`이 2020-11-17 시작, 최신 드래프트가 2025-10 게시 후 **2026-04-18 만료**. **web-researcher가 IETF 데이터트래커로 확인 가능·권장.**

> "에이전트 관점에서 두 줄이 특히 아픕니다. 하나는 **500까지 재생한다**는 것 — 멱등 재시도는 '다시 시도'가 아니라 '원래 결과를 다시 보여주기'입니다. **모델이 실패를 보고 재시도하면 실패를 다시 봅니다. 이건 버그가 아니라 설계이고, 모델이 이걸 이해하지 못하면 무한 루프에 빠집니다(그리고 그게 바로 실패 모드 1.3 단계 반복입니다).** 다른 하나는 **24시간**입니다. 며칠에 걸쳐 도는 장기 실행 에이전트가 어제의 키로 재시도하면, 그건 재시도가 아니라 새 부작용입니다."
> — ✅ 원문 일치 — **멱등성 구현(Stripe 관행)이 오히려 루프를 유발하는 메커니즘. 이 문서에서 가장 비직관적이고 가장 가치 있는 통찰. 축 2와 축 8을 잇는다.**

> **2차 자료 오인용에 대한 저자의 경고(이 책이 그대로 지켜야 할 규율):** "이 논문을 요약한 2차 자료 중에는 '**42%가 명세 문제, 37%가 조율 붕괴, 21%가 검증 부실**'이라고 적은 것들이 돌아다니는데, **세 숫자 모두 논문에 없습니다.** 범주 이름도 다릅니다 — 논문의 첫 범주는 '명세 이슈'가 아니라 '시스템 설계 이슈'입니다… **인용하실 거면 논문 Figure 1을 직접 보시길 권합니다.**"
> — ⚠️ **fact-checker·paper-researcher 필독. 이 주제에는 널리 퍼진 오인용 숫자 세트가 존재한다. 42/37/21을 어디서 보더라도 쓰지 말 것.**

**같은 글에서 검증 필요로 남는 추가 수치:** MAST 방법론은 어노테이터 3명이 트레이스 15건을 독립 라벨링해 **카파 0.88**을 확보한 뒤 **OpenAI o1 기반 LLM-as-a-judge**로 1642건 전체를 라벨링했다(※ **즉 MAST 자체가 LLM 판정자에 의존한다** — 축 7의 신뢰성 논쟁이 이 데이터에도 적용된다는 뜻이므로 책에서 반드시 언급할 것). 평가된 7개 SOTA 오픈소스 시스템의 실패율은 **41%~86.7%**(최악 AppWorld Test-C 86.7%, 최선 AG2 OlympiadBench 41%). 또 "**OTel GenAI 컨벤션에 비용 지표가 없다**"는 관찰. **전부 paper/web-researcher 1차 대조 대상.**

**같은 글의 결정 규칙(휴리스틱으로 직접 사용 가능):**
- "**승인 게이트는 멱등성 계층보다 싸게 구현되고, 초기 단계에서는 대체로 더 낫습니다.**" — 사람이 모든 쓰기를 승인하면 재시도 위험이 대부분 사라진다.
- "**워크플로로 충분하다면 에이전트를 쓰지 마세요.**" — "MAST의 실패 대부분은 시스템 설계 이슈이고, 그건 '결정을 모델에게 넘긴 만큼' 생깁니다."
- "**단일 에이전트로 되면 멀티 에이전트로 가지 마세요.** MAST 실패의 32.3%는 에이전트 사이에서 났습니다. **에이전트를 하나 더 붙이는 순간 그 32.3% 표면적을 새로 삽니다.**" — 논쟁 2에 대한 정량적 논거.
- "**키를 모델이 만들게 하지 마라.** 재시도를 결정하는 주체가 비결정적이므로, 멱등성 키는 결정적인 곳 — 오케스트레이터의 스텝 ID나 태스크 ID — 에서 파생시켜야 합니다. **모델이 매번 새 키를 지어내면 멱등성 키는 장식입니다.**"
- "**상한을 예산으로 걸어라.** 실패의 28.1%가 반복과 미종료라면, **턴 상한과 토큰 예산은 최적화가 아니라 차단기**입니다."
- "**비용은 스팬에서 계산하라.** 메트릭만으로는 (부족하다)."

> "검증은 여전히 본인 몫 / 이해는 방치하면 썩음 / 편안한 자세가 위험한 자세 => 결국 직접 확인하고, 반복작업을 최소화 하기 위한 프롬프팅이 필요하다."
> — [GeekNews 30336](https://news.hada.io/topic?id=30336), 2026년 6월경(게시 시점 "1달전"), `shakespeares`, 긱뉴스 댓글 — 검증 상태: 검증 불필요(의견)

> "하루에 하나씩 새로운 에이전트 시스템이 새로나오네요.. 바이브코딩의 순작용일까요 부작용일까요"
> — [GeekNews 30336](https://news.hada.io/topic?id=30336), 2026년 6월경, `ide127`, 긱뉴스 댓글 — **한국 개발자의 피로감을 보여주는 짧고 강한 인용**

> "프롬프트, 컨텍스트, 하네스 엔지니어링에 이어서 이젠 루프? 군요. AI 사용론이 이전 단계 개념을 계속 흡수하면서 확장돼가네요."
> — [GeekNews 30336](https://news.hada.io/topic?id=30336), 2026년 6월경, `ultimategamer`, 긱뉴스 댓글 — 용어 인플레이션에 대한 국내 반응

> "40일, 100만 줄, 130억 토큰 — Lablup 신정규 대표가 발견한 에이전틱 워크플로의 실체"
> — [GeekNews 27457](https://news.hada.io/topic?id=27457), 2026년 3월경(게시 시점 "4달전"), `ragingwind`, 긱뉴스 댓글 — **검증 상태: 확인 필요(댓글이 참조하는 2차 자료. 130억 토큰이라는 한국 실무 규모 데이터점으로서 가치가 있으나 원 출처 확인 필요).**

> "요즘은 **LLM이 프로덕션 DB를 지우고, 그걸 포스트모템 블로그에 그림까지 그려주는 시대**지만, 그게 진짜 엔지니어링인지 모르겠음" / "지난 10년간 소프트웨어 업계는 **메타 작업**으로 가득했음 — 새로운 프레임워크, 툴, 가상화 계층, 조직 구조 등 하지만 정작 '무엇을 위해' 이걸 만드는지 불분명함"
> — [GeekNews 27861](https://news.hada.io/topic?id=27861) "속도를 늦춰야 하는 이유", 2026년 3월경, 작성자 `GN⁺`, 긱뉴스 — ⚠️ **중요 provenance 경고: `GN⁺`는 긱뉴스의 AI 요약 봇이며 HN 댓글을 한국어로 요약·번역한 것이다. 한국 개발자의 originaI 발언이 아니다.** 따라서 **인용으로 쓰지 말고**, 축 5의 DB 삭제 사건이 **국내 담론에도 전파됐다는 사실의 증거**로만 쓸 것. 원 발언을 인용하려면 HN 원문을 찾아야 한다.

> "천천히 빠르게 라는 말이 있지용" / "대학원 시절에 교수님한테 자주 듣던 말인데, 오랜만에 PTSD 오네요." / "저는 악보에서 읽었어요 allegro non troppo (빠르지만 급하지 않게)"
> — [GeekNews 27858](https://news.hada.io/topic?id=27858) "속도를 늦춰야 빨라진다", 2026년 3월경, `dankim0124`·`hungryman`·`findnamo`, 긱뉴스 댓글 (원문 HTML 직접 파싱) — 검증 불필요(가벼운 반응) — **내용상 깊이는 없으나 데이터로서의 의미가 있다: 국내 커뮤니티에서 에이전트 관련 토픽의 댓글이 기술적 논쟁보다 정서적 공감·가벼운 반응에 머무는 경향을 보여준다. 이것이 아래 「수집 한계」 2번의 근거다.**

---

## 실무 휴리스틱 (현장에서 나온 규칙)

### 비용
1. **알림이 아니라 하드 컷오프를 걸어라.** "토큰 사용량과 비용을 다른 프로덕션 리소스처럼 취급한다. 요청·사용자·기능·모델별로 사용량을 기록하고, 어드민 대시보드에 노출하고, 예산과 **하드 컷오프**를 설정한다." — [HN 48872850](https://news.ycombinator.com/item?id=48872850), 2026-07-11, `bardown59` — **널리 공유됨(여러 스레드에서 독립적으로 반복).**
2. **계획과 실행을 분리해 모델을 계층화하라.** "아키텍처·리서치·어려운 결정에는 더 강하고 비싼 모델을 쓰고, 구현 작업은 작업이 더 제약된 저렴한 에이전트에 넘긴다." — 같은 출처. **널리 공유됨.** ※ 단, 패턴 1-2의 반례를 함께 보라 — **에이전트가 "저렴한 모델을 써라"는 지시를 잊으면 이 전략이 역전된다.** 지시가 아니라 **설정으로 강제**해야 한다는 교훈.
3. **단위 원가를 트레이스의 일급 차원으로 만들어라.** "체크아웃 한 번이 얼마인가"에 답할 수 있어야 한다 — 사용자 액션 단위로 루프·재시도·툴 호출·임베딩을 모두 합산. — [HN 47346646](https://news.ycombinator.com/item?id=47346646), 2026-03-12 (벤더 맥락).
4. **컨텍스트에 들어가면 지연이 먼저, 청구서가 나중에 온다.** 프롬프트 경로 팽창은 비용 대시보드에 뜨기 전에 응답 시간 회귀로 나타난다. — [langgraph#7714](https://github.com/langchain-ai/langgraph/issues/7714), 2026-05-06, `hanselhansel`.

### 루프 종료
5. **결정적 실패와 일시적 실패를 갈라라.** "일시적 실패(네트워크, 레이트 리밋, 타임아웃) → 재시도 / **안정적 실패(같은 입력 → 같은 예외) → 즉시 단락(short-circuit)**." 인자 검증을 재시도 경계 **밖으로** 빼라. — [crewAI#4495](https://github.com/crewAIInc/crewAI/issues/4495), 2026-02-17, `amabito` — **이 문서에서 가장 실행 가능한 단일 규칙.**
6. **`(agent_role, tool_name, canonical_arguments)`를 해시해 궤적 반복을 탐지하라.** LLM이 스스로 루프를 "알아채게" 하는 대신(느리고 토큰을 태운다) 툴 실행 파이프라인을 가로채 결정적으로 판정하고, **API 호출이 머신을 떠나기 전에** 차단한다. — [crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414), 2026-07-01. 후속 논의: 위임 깊이·권한 범위(`delegation_depth`, `authority_scope_ref`)를 해시에 포함하면 정당한 재호출과 진짜 루프를 구별할 수 있다(`0xbrainkid`).
7. **"루프에 빠졌으니 그만해"라는 프롬프트 처방은 실패한다.** "컨텍스트 윈도가 에이전트 자신의 반복된 에러로 오염되어, LLM이 자기 교정하는 게 불가능해진다." — 같은 출처. **프롬프트로 해결하려는 첫 시도가 왜 실패하는지에 대한 정확한 설명.**
8. **개선이 멈췄는지를 측정해서 멈춰라(고정 상한 대신).** — [HN 48475406](https://news.ycombinator.com/item?id=48475406), 2026-06-10 (벤더 처방).
9. **지터 루프까지 잡으려면 완전 일치 해시로는 부족하다.** 출력 간 겹침 계수(overlap coefficient), 인자 근사 일치, "사과하는 비진전 텍스트" 탐지를 추가하라. 결정적 검사만으로 대부분 잡히고 **추가 LLM 호출이 필요 없다**. — [HN 47006768](https://news.ycombinator.com/item?id=47006768), 2026-02-13, `aura-guard`.
10. **완료 주장에 영수증을 요구하라.** 최종 상태를 **주장(claim) / 증거(evidence) / 다음 행동의 권한(authority)** 세 부분으로 쪼개라. "`tests passed`는 명령/실행 ID를 가리켜야 하고, `deployed`는 배포 이벤트나 승인을 가리켜야 하고, `ready to publish`는 **최종 클릭을 누가 소유하는지**를 말해야 한다." 증거는 체크포인트/스레드/실행 ID를 참조해야 하며, **마지막 어시스턴트 메시지를 진실의 원천으로 만들지 말아야 한다.** — [langgraph#7844](https://github.com/langchain-ai/langgraph/issues/7844), 2026-05-18, `utsavtulsyan`·`Keesan12` — **여러 참가자가 독립적으로 같은 3분할에 도달했다는 점에서 수렴 신호.**

### 검색·컨텍스트
11. **컨텍스트에 들어가면 그냥 넣어라 — 다만 절벽을 알고.** "Anthropic은 RAG 글에서, 컨텍스트에 들어가면 RAG를 쓰는 대신 그냥 거기 넣으라고 말한다. 최적 컷오프가 어디인지는 모르겠다, **긴 컨텍스트에서는 품질이 떨어지기 때문에**(가격과 속도는 말할 것도 없고)." — [HN 46085496](https://news.ycombinator.com/item?id=46085496), 2025-11-29, `andai`.
12. **코드에는 구조적 검색을, 산문에는 의미 검색을.** ast-grep/ripgrep을 구조 필터로, 임베딩을 보조로. 상속·다형성이 있는 코드베이스에서 순수 임베딩은 실패한다. — [HN 47898384](https://news.ycombinator.com/item?id=47898384), 2026-04-25.
13. **덤프하지 말고 전처리·라벨링하라.** 스키마를 갖춘 임베딩과 휴리스틱이 품질과 질의 유연성을 크게 좌우한다. — [HN 47535649](https://news.ycombinator.com/item?id=47535649), 2026-03-26.
14. **pgvector로 시작하되 고카디널리티 필터를 조심하라.** 임베딩 수만 개 → 수십억 개를 겪은 RAG 회사 초기 직원: "**pgvector로 시작하는 게 현명하다**. 이미 갖고 있는 것(Postgres)이고 박스에서 꽤 잘 작동한다. 하지만 보통 언급되지 않는 함정이 분명히 있다. pgvector의 필터링 스토리가 1년 전보다 나아졌지만 **고카디널리티 필터는 여전히 나중에 생각한 것처럼 느껴진다**(저카디널리티 필터는 대규모에서도 부분 인덱스로 해결 가능). 또 **ANN 워크로드가 일반적인 것과 꽤 다르다**는 점을 알아야 한다." — [HN 43306765](https://news.ycombinator.com/item?id=43306765), 2025-03-09, `whakim` — **이 문서에서 가장 자격을 갖춘 검색 조언.** ⚠️ 2025년 초 — pgvector 필터링은 활발히 개선 중이라 현재 상태 재확인 필요.
15. **파일 기반 메모리 + 명시적 검색이 컨텍스트 밀어넣기보다 장기 실행에서 안정적이다.** — [HN 47126051](https://news.ycombinator.com/item?id=47126051), 2026-02-23.

### MCP·도구
16. **툴을 개별 노출하지 말고 플러그인/super-tool 뒤에 숨겨라.** 컨텍스트 팽창과 선택지 혼란을 동시에 줄인다. — [HN 47080603](https://news.ycombinator.com/item?id=47080603), 2026-02-19.
17. **MCP 대신 CLI + skills를 고려하라(필터·파이프 가능성).** "CLI로는 매번 툴 호출 전체를 컨텍스트에 펼치지 않고도 필터/파이프(그냥 유닉스 bash) 능력을 얻는다. CLI는 `--help` 출력에서 skills를 쉽게 생성할 수 있고… **지연 로딩되며 컨텍스트를 부풀리지 않는다.**" — [HN 47381210](https://news.ycombinator.com/item?id=47381210), 2026-03-14, `jswny`.
18. **출력 스키마 + 코드 실행(CodeAct)으로 거대 JSON 덤프를 우회하라.** "출력 스키마가 없으면 에이전트는 툴을 호출해 원시 출력(종종 거대한 JSON 덩어리)을 컨텍스트 윈도에 쏟고, 검사한 다음에야 처리 코드를 쓴다." — [HN 47381282](https://news.ycombinator.com/item?id=47381282), 2026-03-14, `menix`.
19. **MCP 서버는 컨테이너에 격리하라 — 단, 그게 인젝션은 막지 않는다는 걸 알고.** — [HN 47581930](https://news.ycombinator.com/item?id=47581930), 2026-03-31.

### 평가·관측
20. **LLM 판정자는 필터이지 판결이 아니다.** 데이터를 걸러 사람이 볼 후보를 만드는 데 쓰고, 최종 기준은 인간 평가자로 둔다. — [HN 40987261](https://news.ycombinator.com/item?id=40987261), 2024-07-17 — **널리 공유됨(2024→2026 내내 반복).**
21. **에이전트 평가 단위는 프롬프트가 아니라 세션/실행이다.** — [HN 44736570](https://news.ycombinator.com/item?id=44736570), 2025-07-30.
22. **LLM으로 LLM을 단속하는 건 너무 느리고 비싸다 — 거버넌스는 결정적으로.** — [HN 47352022](https://news.ycombinator.com/item?id=47352022), 2026-03-12.
23. **툴 호출 경계에서 강제하라.** "'모델이 이 툴을 호출하려 한다'와 '툴이 실제로 실행된다' 사이의 순간" — 대부분의 안전 접근이 콘텐츠(출력 필터, 인젝션)나 인프라(샌드박스, 권한)에 집중해 **런타임 행동에 공백이 있다.** — [HN 47006768](https://news.ycombinator.com/item?id=47006768), 2026-02-13.

### 상태·복구
24. **마지막 완료 단계에서 재개할 수 있게 설계하라**(원자적 temp+replace, 재시작 시 복원). — [HN 46964602](https://news.ycombinator.com/item?id=46964602), 2026-02-10.
25. **"얼려진" 워크스페이스 상태를 두어 401/레이트 리밋 이후 돌아갈 지점을 만들라.** — [HN 47352022](https://news.ycombinator.com/item?id=47352022), 2026-03-12.

---

## 논쟁점 (양쪽 진영 논거 병기 — 독자가 결정해야 하므로)

### 논쟁 1 — 프레임워크 vs 직접 구현(raw SDK)
- **관점 A(버려라):** 가장 근본적인 형태의 질문은 2024년 "우리가 더 이상 AI 에이전트 구축에 LangChain을 쓰지 않는 이유" 스레드에서 이미 나왔다: "**나는 그냥 langchain이 어떤 용례를 위한 것인지 알고 싶다.** 지금까지 애플리케이션 네다섯 개를 만들었고, 여러 SDK를 쓰는 건 충분히 쉬웠다. **langchain은 어디서 들어오는 건가?**"([HN 40767597](https://news.ycombinator.com/item?id=40767597), 2024-06-23, `bastawhiz` — 스레드 [HN 40739982](https://news.ycombinator.com/item?id=40739982)). ⚠️2024이지만 이 질문 형태는 2026년까지 그대로 반복된다. 이후 구체화된 논거: 상태가 타입 없는 JSON 덩어리라 데이터 흐름 추적이 불가([HN 44307883](https://news.ycombinator.com/item?id=44307883), `davedx`). 버전 업그레이드가 툴 인자 바인딩을 깨서 무한 루프를 유발([crewAI#4495](https://github.com/crewAIInc/crewAI/issues/4495)). "에이전트는 그냥 루프다" — 260줄로 충분([HN 47189061](https://news.ycombinator.com/item?id=47189061)).
- **관점 B(남거나 재평가):** 등급을 나눠 보라 — LangGraph는 다르다(오케스트레이션은 "가장 덜 나쁜" 것이고 대안은 OpenAI Agents SDK·Pydantic AI, [HN 44840626](https://news.ycombinator.com/item?id=44840626), `NeutralCrane`). 추상화가 저수준이고 프로토타이핑에 최적이다([HN 41205156](https://news.ycombinator.com/item?id=41205156), `sbrother`, ⚠️2024). 직접 만들면 상태·재시도·관측성·내구성을 다 만들어야 하는데, 그게 정확히 사람들이 과소평가하는 비용이다(축 9의 재개·크래시 복구 패턴들이 이 비용의 실물).
- **관점 C(문제는 프레임워크가 아니라 모듈성이다) — 이 책 독자에게 특히 유용:** 자바/Spring 배경 개발자의 진단이 논쟁을 재구성한다. "모듈식 접근을 채택하는 게 좋은 생각이라는 데 동의한다. **자바 생태계에서 온 나는 파이썬에 Spring 같은 게 없는 걸 여전히 아쉬워한다.** Spring은 훌륭한 프레임워크 설계의 예로 남아 있다고 믿는다. …**Spring을 쓰려면 Spring IoC를 채택해야 하지만, 그 너머는 전부 모듈식이다. ORM, 메시징, 캐싱처럼 필요한 추상화만 골라 쓸 수 있다.** 핵심에서 Spring IoC는 이 컴포넌트들을 느슨하게 통합하는 데 쓰인다."([HN 40821394](https://news.ycombinator.com/item?id=40821394), 2024-06-28, `olafgeibig`) — **불만의 정체가 "추상화가 있다"가 아니라 "추상화를 골라 쓸 수 없다"임을 정확히 짚는다. 백엔드 개발자 독자가 이미 가진 프레임워크 감각으로 이 판단을 내릴 수 있게 해주는 최적의 다리.** ⚠️2024 자료. 같은 스레드에서 관측성만 떼어 쓰고 싶다는 요구도 나왔다: "LangChain은 관측성 관련 도구가 좀 있는데 그건 내게 진짜로 유용해 보이고 LLM 작업에 특화돼 있다. **이 도구들만 쓸 방법이 있나?**"([HN 40873601](https://news.ycombinator.com/item?id=40873601), 2024-07-04, `isaacphi`) — 2025~2026년의 "Langfuse로 관측성만 분리" 실천을 1년 앞서 예고한 요구.
- **현재 무게중심:** **"프레임워크 전체를 사거나 버리거나"가 아니라 계층별로 갈라 사는 쪽으로 이동했다.** 관측성(Langfuse)·오케스트레이션(LangGraph/Agents SDK/Pydantic AI)을 분리 선택하고, **LLM 인터페이스 래퍼는 직접 쓰는** 조합이 반복 관찰된다. 특징적으로, 최신 불만은 "추상화가 너무 많다"에서 "**정작 필요한 신뢰성 안전장치는 안 준다**"로 이동했다([HN 46730883](https://news.ycombinator.com/item?id=46730883), 2026-01) — 그리고 그 공백을 프레임워크 이슈 트래커가 스스로 메우려 한다([crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414) 결정적 루프 가드레일, [langgraph#8026](https://github.com/langchain-ai/langgraph/issues/8026) ApprovalNode).

### 논쟁 2 — 멀티에이전트가 정말 필요한가 vs 단일 에이전트 + 좋은 도구
- **관점 A(불필요·과잉):** "역할 프롬프트로 단일 함수의 범위를 설정하는 것(A)"과 "핸드오프·조율 프로토콜·프레임워크 추상화를 갖춘 정교한 멀티에이전트 오케스트레이션 계층을 그 위에 쌓는 것(B)"을 구별해야 하며, "**B는 종종 비례하는 이득 없이 복잡도를 추가한다, 특히 모델이 롱 컨텍스트 추론에 좋아질수록**"([HN 46753582](https://news.ycombinator.com/item?id=46753582), 2026-01-25, `joshuaisaact`). 더 강한 형태: "학계의 많은 사람들이 멀티에이전트 시스템을 **현 세대 LLM의 인공물**로 보는데, 최근 모델들이 점점 더 길고 신뢰할 만한 컨텍스트와 더 많은 툴의 신뢰할 만한 호출을 갖게 되면서 멀티에이전트 시스템은 점점 덜 필요해 보인다"([HN 46852260](https://news.ycombinator.com/item?id=46852260), 2026-02-02, `storus`). 조율 자체가 새 실패 모드를 만든다(패턴 10-1 조용한 상태 덮어쓰기, [crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414) 위임 핑퐁).
- **관점 B(필요·불가피):** **컨텍스트 윈도 한계가 병렬성을 강제한다.** "단일 에이전트는 이걸 한 API 호출로 달성할 컨텍스트 윈도 크기가 부족하고, **그래서 병렬 에이전트가 필요하다.** 그러면 병렬 출력을 상태가 올바르게 갱신되는 방식으로 통합해야 한다. **멀티에이전트가 유일한 해법인 것 같다.** 사실상 에이전트를 스레드로, 역할을 함수로 취급하고 있다"([HN 46763212](https://news.ycombinator.com/item?id=46763212), 2026-01-26, `ryanjshaw`). 서브에이전트의 실질 가치는 조율이 아니라 **깨끗한 컨텍스트**다: "'sub-agent'라는 툴이 있는데, 모델이 명확히 정의된 하위 작업을 독립적으로 수행할 수 있는 **신선한 컨텍스트 윈도를 만든다**"([HN 44387136](https://news.ycombinator.com/item?id=44387136), 2025-06-26, `akrauss`).
- **현재 무게중심:** **"멀티에이전트냐"가 아니라 "왜 멀티에이전트냐"로 질문이 재정의됐다.** 커뮤니티가 수렴하는 정당한 이유는 두 가지 — **(a) 컨텍스트 격리**(신선한 윈도), **(b) 병렬성**(처리량). 반면 "역할 놀이"로서의 멀티에이전트는 회의론이 우세하다. 그리고 **비용 축이 이 논쟁에 개입한다** — 서브에이전트 팬아웃이 청구서를 곱한다(패턴 1-2).

### 논쟁 3 — RAG vs 롱 컨텍스트 vs grep/에이전틱 검색
- **관점 A(RAG는 끝났다):** 스레드 제목이 논지다 — "**RAG 부고: 에이전트에게 죽고, 컨텍스트 윈도에 묻혔다**"([HN 45445280](https://news.ycombinator.com/item?id=45445280), 2025-10-02). 근거: 코딩 에이전트가 grep/ripgrep으로 로컬 코드베이스를 훑는 게 잘 작동하고, 컨텍스트에 들어가면 그냥 넣으면 된다.
- **관점 B(스케일에서 성립하지 않는다):** 같은 스레드 최상위 반박: "이건 전체 논증을 무너뜨리는 근본적 스케일링 문제를 얼버무린다. 저자의 주 예시는 Claude Code가 grep과 ripgrep으로 **로컬** 코드베이스를 검색하는 것인데, 이걸 모든 문서 검색으로 외삽한다. **거대한 논리적 도약이다. grep은 밀리초로 스캔할 수 있는 로컬 파일시스템의 수천 개 파일에서 훌륭하다. 하지만 대부분의 엔터프라이즈 RAG 용례는 분산 시스템에 걸친 수백만 개 문서다. 2M 토큰 컨텍스트 윈도가 있어도 엔터프라이즈 지식 베이스 전체를 컨텍스트에 넣을 수 없다.**" + "**grep은 정확한 키워드 매칭이다**" — 의미 이해가 필요한 질의에서 실패. ([HN 45445280](https://news.ycombinator.com/item?id=45445280), 2025-10-02, `davidmckayv`)
- **관점 C(구조가 답이다):** 코드에서는 임베딩보다 **구조적 검색**(ast-grep)이 이긴다([HN 47898384](https://news.ycombinator.com/item?id=47898384)). 인과 추론이 필요한 도메인에서는 표준 RAG가 실패해 **로직 그래프**로 대체했다는 사례도([HN 47050712](https://news.ycombinator.com/item?id=47050712), 2026-02-17, ※ 같은 저자가 컨텍스트 캐싱으로 API 비용을 ~80% 줄였다고 주장 — **검증 필요**).
- **현재 무게중심:** **코퍼스 성질에 따라 갈리는 것으로 정리됐고, "RAG냐 아니냐"라는 이항 질문 자체가 낡았다는 인식이 우세하다.** 결정 축: (1) 컨텍스트에 들어가는가 → 넣어라, (2) 구조가 있는가(코드·스키마) → 구조적 검색, (3) 수백만 문서·분산 → 검색은 여전히 필수(하이브리드+리랭커). 용어 혼동 자체가 논쟁을 악화시킨다는 지적도 유효([HN 45564799](https://news.ycombinator.com/item?id=45564799)).

### 논쟁 4 — 전용 벡터 DB vs pgvector
- **관점 A(pgvector로 충분·유리):** 필터링과 페이지네이션의 현실이 결정적이다. "**분리된 벡터 DB로 유사도 검색을 다른 필터·페이지네이션과 결합하는 걸 사람들은 어떻게 하나?** 내 주변에선 꽤 흔한 용례다. 예를 들어 검색어에 매칭되고(벡터 검색) 회사 X가 만든(회사는 별도 테이블) 상품 목록을, 검색어 벡터 유사도로 정렬해서 상위 100개 달라는 것. …**우리는 가능한 곳에서 ElasticSearch에서 Postgres로 대체로 옮겨왔다**, 새 복잡한 필터를 구현하기가 훨씬 쉽기 때문에 — 매번 다른 테이블 데이터를 인덱스에 추가할 필요가 없다." ([HN 45810084](https://news.ycombinator.com/item?id=45810084), 2025-11-04, `inbx0` — 스레드 제목은 반대로 "The Case Against PGVector"인데 최상위 댓글이 반박이라는 점이 이 논쟁의 성격을 보여준다.)
- **관점 B(스케일에서 함정이 있다):** 수십억 임베딩 경험자의 자격 있는 절충: pgvector로 시작하는 건 현명하지만 **고카디널리티 필터는 여전히 후순위 시민**이고 **ANN 워크로드는 일반 Postgres 워크로드와 성질이 다르다**([HN 43306765](https://news.ycombinator.com/item?id=43306765), 2025-03-09, `whakim`).
- **현재 무게중심:** **"pgvector로 시작하라"가 기본값으로 굳었다.** 반대 진영조차 시작점으로는 동의하며, 논쟁은 "**언제 떠나야 하는가**"로 이동했고 그 기준은 규모 자체보다 **필터 카디널리티와 ANN 워크로드 분리 필요성**이다. ⚠️ 양쪽 자료 모두 2025년 — pgvector는 활발히 개선 중이라 현 상태 재확인 필요.

### 논쟁 5 — 매니지드 eval 플랫폼 vs 자체 구축
- **관점 A(플랫폼):** 관측/트레이싱 도구는 일회성 디버깅에 쓰이고 **1%에서만 나는 에러의 회귀 테스트 능력이 없다** — 데이터셋과 지표를 소유한 전용 평가 도구가 필요하다([HN 43119210](https://news.ycombinator.com/item?id=43119210), 2025-02-20, DeepEval 창업자).
- **관점 B(자체·인간 중심):** 같은 벤더가 **자기 핵심 지표의 신뢰성이 최대 걸림돌**이라고 인정한다(같은 출처). 그리고 "판정자 지표는 필터일 뿐, 골든 기준은 인간 평가자"([HN 40987261](https://news.ycombinator.com/item?id=40987261)). 사실상 **도구를 사도 평가 설계·라벨링 노동은 이전되지 않는다.**
- **현재 무게중심:** **평가의 어려움이 도구 선택 문제가 아니라 데이터·기준 문제라는 인식이 우세하다.** 트레이싱은 사고, 평가는 회귀 방지 — **두 개를 다른 물건으로 취급하라**는 것이 수렴점. 실무 조언 계열: 트레이싱(Langfuse 등)은 도구를 사고, 골든 데이터셋과 판정 기준은 직접 소유하라. ⚠️ 강한 관측 편향 주의 — 이 축의 발언자 다수가 벤더다.

### 논쟁 6 — 워크플로(결정적)로 충분한가 vs 자율 에이전트가 필요한가
- **관점 A(결정적으로 밀어라):** 이 문서에서 가장 일관되게 반복되는 방향. LLM 자기 인식에 의존한 루프 탐지는 느리고 비싸며 실패한다 → **결정적 궤적 해시로 차단**([crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414)). LLM이 다른 LLM을 단속하는 건 너무 느리고 비싸다 → **결정적 거버넌스**([HN 47352022](https://news.ycombinator.com/item?id=47352022)). 재시도 정책이 프롬프트에 있으면 "**정책이 아니라 확률**"([youngju.dev](https://www.youngju.dev/blog/2026-07-17-agent-production-failure-taxonomy-idempotency)). 툴 호출 경계에서 결정적으로 강제하라([HN 47006768](https://news.ycombinator.com/item?id=47006768)).
- **관점 B(자율성이 값을 만든다):** "에이전틱 워크플로의 약속은 매우 실재한다. 에이전틱 코딩 도구를 진지하게 써봤다면, 특정 맥락에서 이 도구들이 실제 문제를 풀고 **수동으로 몇 시간·며칠 걸릴 일을 몇 분에 하는 걸 보는 게 조금 마법 같다**는 걸 알아냈을 것이다"([HN 47788830](https://news.ycombinator.com/item?id=47788830), 2026-04-16, `jillesvangurp` — 같은 사람이 "그렇다, 엄청 엉망이고 안전하지 않고 위험하다"고 인정하면서도 쓴다).
- **현재 무게중심:** **"자율성은 유지하되 부작용 경계를 결정적으로 감싼다"는 합성이 지배적이다.** 즉 추론은 확률적으로, **집행은 결정적으로.** 이것이 축 2·5·6·7의 처방이 모두 수렴하는 지점이며, 이 책의 핵심 설계 원칙으로 삼을 만하다.

### 논쟁 7 — 코딩 에이전트가 실제로 생산성을 올리는가
- **관점 A(순손실 가능):** "스티어링, 손잡아주기, 이중 확인의 양이 결국 더 느린 빌드 과정보다 더 많은 인간 자원을 소모할 것"([HN 47876462](https://news.ycombinator.com/item?id=47876462), 2026-04-23). 1년+ 사용 후 전면 철수 사례: "**모든 구독을 취소하고 로컬 모델을 다 지웠다… 지금까지 결정에 매우 만족한다.** 신기함은 사라졌고, AI를 다루는 게 이제 좌절스럽고 지루하다… **에이전트가 내가 의존하는 인수 테스트에서 지름길을 택했고 잡아내지 못했다는 걸 백 번째로 재발견하고 싶지 않다**"([HN 48083162](https://news.ycombinator.com/item?id=48083162), 2026-05-10 / [HN 48602039](https://news.ycombinator.com/item?id=48602039), 2026-06-19, `dgellow`).
- **관점 B(맥락 의존적 큰 이득):** 같은 도구에서 정반대 경험이 보고된다: "한 달 전에 AI 보조가 큰 순손실이었던 작업이 있었다. 오늘 Claude Code로 같은 걸 20분쯤에 했다. **API 사용료 $10 미만으로!** …Cursor의 에이전트 모드는 작업 시간 지평 3~5분에서 유용성이 사라지는데 **Claude Code는 10분 이상 갈면서 루프에 빠지지 않고 의미 있는 진전을 낸다**"([HN 44598694](https://news.ycombinator.com/item?id=44598694), 2025-07-17, `ivanech`). 개인 프로젝트에서는 "완전히 미친 force multiplier"이지만 맥락에 따라 갈린다는 절충 보고도([HN 48742102](https://news.ycombinator.com/item?id=48742102), 2026-07-01, `dimitrios1`).
- **측정 논쟁의 실물 — 리뷰 부담이 외부화된다:** 생산성 논쟁이 **오픈소스 정책 결정으로 구체화**됐다. Redox OS의 no-LLM 정책 근거: "**과거에는 코드 자체가 일종의 노력의 증거였다** — PR에 시간과 노력을 투자해야 했고, 그렇지 않으면 한눈에 기각됐다. **LLM이 표면적으로 맞아 보이는 PR을 빠르게 생성할 수 있으므로 더 이상 그렇지 않다.** 노력이 들어갔을 수도 있지만, 더 자세히 리뷰하는 데 시간을 쓰지 않고는 **알 방법이 없다**"([HN 47320789](https://news.ycombinator.com/item?id=47320789), 2026-03-10, `ptnpzwqd`). Zig도 같은 방향([HN 47958708](https://news.ycombinator.com/item?id=47958708), 2026-04-30). 상징적 사례 — 어떤 PR의 저자명이 무관한 사람으로 붙어 있던 것에 대한 제출자 답변: "**나도 모른다. AI가 그렇게 하기로 했고 나는 의문을 제기하지 않았다**"([HN 46689187](https://news.ycombinator.com/item?id=46689187), 2026-01-20, `Alupis` 인용).
- **현재 무게중심:** **개인 속도 이득에는 광범위한 동의가 있지만, 그 이득이 어디로 이전되는지(리뷰·검증·유지보수)에 대한 회의가 커졌다.** 커뮤니티가 "생산성"을 개인 처리량이 아니라 **시스템 처리량**으로 재정의하는 중이다. ※ **책에서 이 논쟁을 다룰 때 주의:** 커뮤니티 발언은 자기 선택 편향이 강하다(불만이 있는 사람이 더 많이 쓴다). 정량 근거는 web/paper-researcher의 통제 연구로 보완해야 한다.

### 논쟁 8 (추가) — 에이전트 사고의 책임은 누구에게 있는가
- **관점 A(도구 문제):** 프로덕션 DB 삭제 사건은 에이전트가 검증 없이 파괴적 명령을 실행할 수 있었다는 **도구·권한 설계의 실패**다([HN 47911720](https://news.ycombinator.com/item?id=47911720), 2026-04-26).
- **관점 B(운영자 문제):** "**AI가 네 DB를 지운 게 아니라, 네가 지웠다**"([HN 48027109](https://news.ycombinator.com/item?id=48027109), 2026-05-05). 원 글이 "행동 상당수를 에이전트에 귀속시키고 **에이전트를 돌린 사람의 책임은 0으로 둔다**"는 비판(`Uhhrrr`). MCP 권한 논쟁도 같은 구조: "이 MCP 서버가 **네 자신의 자격증명**으로 돌고 있고 그 자격증명이 DB 풀 액세스를 준다면, 이 서비스로 임의 질의를 할 수 있다는 사실은 특별할 게 없다 — **문자 그대로 네 에이전트다.** 버그라고 부르겠지, 반드시 보안 위험이라고는 않겠다"([HN 44506488](https://news.ycombinator.com/item?id=44506488), 2025-07-09, `otterley`).
- **현재 무게중심:** **책임 논쟁이 "최소 권한을 실제로 어떻게 거는가"라는 공학 질문으로 수렴했다.** 개발/프로덕션 환경 분리, 승인 게이트, 자격증명 범위 축소가 반복 처방이며, [langgraph#8026](https://github.com/langchain-ai/langgraph/issues/8026)(ApprovalNode 요청, 40개 댓글)·[openai-agents-python#2868](https://github.com/openai/openai-agents-python/issues/2868)(툴별 권한 미들웨어, 31개 댓글) 같은 프레임워크 요청이 이 수렴의 증거다.

---

## 링크 모음

### Hacker News — 프레임워크 논쟁
- [HN 40739982](https://news.ycombinator.com/item?id=40739982) — 2024-06 — "우리가 더 이상 AI 에이전트 구축에 LangChain을 쓰지 않는 이유". 추상화 계층이 비표준 요구에서 이해·수정을 막는다는 원형 논거. ⚠️2024
- [HN 44840323](https://news.ycombinator.com/item?id=44840323) — 2025-08 — "아직도 LangChain으로 만드나?" "불행히도, 그렇다. 선택은 아니고."
- [HN 44840626](https://news.ycombinator.com/item?id=44840626) — 2025-08-08 — LangChain 3제품 등급 분리(LangGraph=가장 덜 나쁨, LangSmith<Langfuse, 라이브러리=끔찍).
- [HN 44307883](https://news.ycombinator.com/item?id=44307883) — 2025-06-18 — LangGraph 상태가 타입 없는 JSON 덩어리 → 런타임 타입 에러·데이터 흐름 추적 불가·테스트 곤란.
- [HN 40739982](https://news.ycombinator.com/item?id=40739982) — 2024-06-23 — "우리가 더 이상 LangChain을 쓰지 않는 이유"(297댓글). 핵심 댓글: "langchain은 어디서 들어오는 건가?"([40767597](https://news.ycombinator.com/item?id=40767597)), Spring식 모듈성 부재 진단([40821394](https://news.ycombinator.com/item?id=40821394)), 관측성만 분리해 쓰고 싶다는 요구([40873601](https://news.ycombinator.com/item?id=40873601)). ⚠️2024이나 계보상 원점.
- [HN 41205156](https://news.ycombinator.com/item?id=41205156) — 2024-08-09 — "langchain보다 훨씬 낫지만 그렇게 많은 걸 하지는 않는다." ⚠️2024
- [HN 42449742](https://news.ycombinator.com/item?id=42449742) — 2024-12-18 — 프레임워크 4종 비교. AutoGen 프로덕션 미준비 경고, "GitHub 스타로 결정하지 마라". ⚠️2024
- [HN 46730883](https://news.ycombinator.com/item?id=46730883) — 2026-01-23 — 프레임워크는 무거운데 루프·실패 안전장치는 오히려 부족.
- [HN 47189061](https://news.ycombinator.com/item?id=47189061) — 2026-02-28 — "에이전트는 그냥 루프다" 260줄 Rust 구현.

### Hacker News — 비용
- [HN 47346646](https://news.ycombinator.com/item?id=47346646) — 2026-03-12 — Ask HN: 에이전트 워크플로 API 비용 예측법. 사용자 액션 단위 원가 부재.
- [HN 48872850](https://news.ycombinator.com/item?id=48872850) — 2026-07-11 — 기업들의 AI 비용 억제. 하드 컷오프·모델 계층화 휴리스틱.
- [HN 49040461](https://news.ycombinator.com/item?id=49040461) — 2026-07-24 — "3개 프롬프트로 $45 태웠다."
- [HN 49030357](https://news.ycombinator.com/item?id=49030357) — 2026-07-24 — 서브에이전트 팬아웃으로 1시간 15분에 $120. "지시를 잊었다."
- [HN 48859325](https://news.ycombinator.com/item?id=48859325) — 2026-07-10 — 실무자가 만든 에이전트 eval 하네스. "멈출 줄 아는 것"이 모델 변별 능력으로 등장.

### Hacker News — 루프·거짓 성공
- [HN 45001692](https://news.ycombinator.com/item?id=45001692) — 2025-08-24 — 1시간 루프 후 "해결했다", 에러는 그대로.
- [HN 46064091](https://news.ycombinator.com/item?id=46064091) — 2025-11-27 — Gemini CLI 루프 재발 + 루프 탐지가 작업 전체를 중단.
- [HN 46657214](https://news.ycombinator.com/item?id=46657214) — 2026-01-17 — "증거 없이 성공을 암시했다."
- [HN 47006768](https://news.ycombinator.com/item?id=47006768) — 2026-02-13 — Ask HN 에이전트 안전. 지터 루프·툴 호출 경계 강제·결정적 검사.
- [HN 44736570](https://news.ycombinator.com/item?id=44736570) — 2025-07-30 — 행동 루프 그래프 시각화 + 평가 단위는 세션/실행.
- [HN 48475406](https://news.ycombinator.com/item?id=48475406) / [HN 48919568](https://news.ycombinator.com/item?id=48919568) — 2026-06-10/07-15 — max_iterations는 양방향으로 틀렸다(제어이론 접근).
- [HN 44598694](https://news.ycombinator.com/item?id=44598694) — 2025-07-17 — 반례: 10분+ 진전, 루프에 안 빠짐. 하네스 품질 차이.
- [HN 47753180](https://news.ycombinator.com/item?id=47753180) — 2026-04-13 — 로컬 모델 루프 빈발 + "더 똑똑한 모델에 전화하기" 아이디어.

### Hacker News — RAG·검색
- [HN 45445280](https://news.ycombinator.com/item?id=45445280) — 2025-10-02 — "RAG 부고" + 최상위 반박(엔터프라이즈 스케일·grep은 정확 매칭).
- [HN 45810084](https://news.ycombinator.com/item?id=45810084) — 2025-11-04 — pgvector 반대론에 대한 필터·페이지네이션 반박.
- [HN 43306765](https://news.ycombinator.com/item?id=43306765) — 2025-03-09 — 수십억 임베딩 경험자: pgvector 시작 권장 + 고카디널리티 필터·ANN 워크로드 함정.
- [HN 46085496](https://news.ycombinator.com/item?id=46085496) — 2025-11-29 — 컨텍스트에 들어가면 넣어라, 단 롱 컨텍스트에서 품질 저하.
- [HN 47664736](https://news.ycombinator.com/item?id=47664736) — 2026-04-06 — 컨텍스트 채우기로 레이트 리밋 조기 도달, "나쁜 검색 보상용 파일"이 쌓인다.
- [HN 47898384](https://news.ycombinator.com/item?id=47898384) — 2026-04-25 — 코드에서 순수 임베딩 실패, 구조적 검색 우위.
- [HN 47535649](https://news.ycombinator.com/item?id=47535649) — 2026-03-26 — "제로에서 RAG까지: 성공과 실패". 전처리·라벨링.
- [HN 45564799](https://news.ycombinator.com/item?id=45564799) — 2025-10-13 — "RAG"라는 용어 자체의 혼동.
- [HN 42226094](https://news.ycombinator.com/item?id=42226094) — 2024-11-24 — late chunking + semantic chunking 조합. ⚠️2024

### Hacker News — MCP
- [HN 47158526](https://news.ycombinator.com/item?id=47158526) — 2026-02-25 — 툴 정의가 매 요청 전송·전부-아니면-전무 로딩·조합 불가.
- [HN 47381210](https://news.ycombinator.com/item?id=47381210) / [HN 47381282](https://news.ycombinator.com/item?id=47381282) — 2026-03-14 — "MCP는 죽었다" 스레드 양쪽(CLI+skills 우위 / 출력 스키마+CodeAct 반론).
- [HN 48330589](https://news.ycombinator.com/item?id=48330589) — 2026-05-29 — 반-MCP 담론에 대한 회의("progressive discovery 있잖아", 원 글의 자기모순 지적).
- [HN 47714718](https://news.ycombinator.com/item?id=47714718) — 2026-04-10 — MCP 옹호자도 인정하는 결함: 출력이 컨텍스트로 직행.
- [HN 43951934](https://news.ycombinator.com/item?id=43951934) — 2025-05-11 — "MCP 비판적 시각": 왜 function calling을 확장하지 않았나 + 진짜 가치는 마켓플레이스.
- [HN 47080603](https://news.ycombinator.com/item?id=47080603) — 2026-02-19 — super-tool 뒤에 숨기기가 프로덕션 안정성에 유리.
- [HN 46920388](https://news.ycombinator.com/item?id=46920388) — 2026-02-07 — Pydantic AI 리드의 Code Mode 설명(툴 결과 전량 컨텍스트 반환 문제).

### Hacker News — 보안
- [HN 47911720](https://news.ycombinator.com/item?id=47911720) — 2026-04-26 — 프로덕션 DB 삭제 사건 + "왜 그랬어?"는 범주 오류라는 경고.
- [HN 48027109](https://news.ycombinator.com/item?id=48027109) — 2026-05-05 — "AI가 지운 게 아니라 네가 지웠다" 책임 반박.
- [HN 48045859](https://news.ycombinator.com/item?id=48045859) — 2026-05-07 — 에이전트 "자백" 원문 인용.
- [HN 47161210](https://news.ycombinator.com/item?id=47161210) — 2026-02-26 — 14,000+ 세션 분석 주장: "에이전트는 차선을 지키지 않는다".
- [HN 47581930](https://news.ycombinator.com/item?id=47581930) — 2026-03-31 — MCP 위험 2분할(인젝션 vs 공급망), 컨테이너는 후자만 해결.
- [HN 47179283](https://news.ycombinator.com/item?id=47179283) — 2026-02-27 — 공개 CTF: "내부 테스트는 항상 통과한다", 내용 대 의도 매칭.
- [HN 47298207](https://news.ycombinator.com/item?id=47298207) — 2026-03-08 — "탈옥은 고쳤다, 에이전트는 못 고쳤다": 경계 혼동.
- [HN 47325268](https://news.ycombinator.com/item?id=47325268) — 2026-03-10 — 인젝션 필터 우회(인코딩·비영어·다중 턴 분절) 주장. **검증 필요**
- [HN 47896464](https://news.ycombinator.com/item?id=47896464) — 2026-04-24 — 인젝션 방어 훈련이 stop hook을 무시하게 만드는 2차 효과.
- [HN 44506488](https://news.ycombinator.com/item?id=44506488) — 2025-07-09 — Supabase MCP DB 유출: "문자 그대로 네 에이전트다" 경계 논쟁.
- [HN 48094454](https://news.ycombinator.com/item?id=48094454) — 2026-05-11 — 바이브 코딩 도구에서 보안 문제 28개, 전부 고전적 버그.
- [HN 44142430](https://news.ycombinator.com/item?id=44142430) — 2025-05-31 — MCP 서버 하나가 뚫리면 전 사용자가 노출.

### Hacker News — 평가·관측
- [HN 43119210](https://news.ycombinator.com/item?id=43119210) / [HN 43121129](https://news.ycombinator.com/item?id=43121129) — 2025-02-20 — 평가 벤더의 자기 한계 인정 + 1% 에러 회귀 테스트 불가 + 질문 순서 섞기 효과.
- [HN 40987261](https://news.ycombinator.com/item?id=40987261) — 2024-07-17 — "판정자는 필터, 골든 기준은 인간." ⚠️2024
- [HN 44832641](https://news.ycombinator.com/item?id=44832641) — 2025-08-08 — LLM-as-judge 길이 편향 학술 근거(arXiv 2407.01085).
- [HN 46349308](https://news.ycombinator.com/item?id=46349308) — 2025-12-21 — "구조화된 출력이 거짓 확신을 만든다."
- [HN 46245185](https://news.ycombinator.com/item?id=46245185) — 2025-12-12 — "대부분의 에이전트 실패는 조용하다."
- [HN 46776079](https://news.ycombinator.com/item?id=46776079) — 2026-01-27 — 200+ span 트레이스에서 근본 원인 찾기 20분+.
- [HN 47315314](https://news.ycombinator.com/item?id=47315314) — 2026-03-09 — 5개 에이전트 체인 디버깅: 로그 흩어짐·리플레이 없음·모델 교체 시 코드 재작성.

### Hacker News — 상태·지연·멀티에이전트
- [HN 47126051](https://news.ycombinator.com/item?id=47126051) — 2026-02-23 — "에이전트는 자기 역사를 환각한다", 50~60턴 붕괴, 파일 기반 메모리 우위.
- [HN 47352022](https://news.ycombinator.com/item?id=47352022) — 2026-03-12 — 무상태 API 취급이 실패 원인, 얼려진 워크스페이스 상태, 결정적 거버넌스.
- [HN 46964602](https://news.ycombinator.com/item?id=46964602) — 2026-02-10 — 크래시 안전 상태 지속성, 마지막 완료 단계 재개.
- [HN 44578559](https://news.ycombinator.com/item?id=44578559) — 2025-07-16 — 클라우드 플랫폼이 장기 실행 에이전트용이 아니다.
- [HN 47387252](https://news.ycombinator.com/item?id=47387252) — 2026-03-15 — 조용한 상태 덮어쓰기 경쟁 조건, "출력이 그럴듯해 보인다".
- [HN 46753582](https://news.ycombinator.com/item?id=46753582) / [HN 46763212](https://news.ycombinator.com/item?id=46763212) — 2026-01-25/26 — 멀티에이전트 논쟁 양쪽(A/B 구별 vs 컨텍스트 한계가 병렬 강제).
- [HN 46852260](https://news.ycombinator.com/item?id=46852260) — 2026-02-02 — "멀티에이전트는 현 세대 LLM의 인공물".
- [HN 44387136](https://news.ycombinator.com/item?id=44387136) — 2025-06-26 — 서브에이전트의 본질은 신선한 컨텍스트 윈도.
- [HN 48196003](https://news.ycombinator.com/item?id=48196003) — 2026-05-19 — "그건 채팅 히스토리 있는 단일 에이전트다."

### Hacker News — 생산성 논쟁
- [HN 47876462](https://news.ycombinator.com/item?id=47876462) — 2026-04-23 — 스티어링 비용이 이득을 잡아먹는다, "골든 리트리버 vibes".
- [HN 48083162](https://news.ycombinator.com/item?id=48083162) / [HN 48602039](https://news.ycombinator.com/item?id=48602039) — 2026-05-10/06-19 — 1년+ 후 전면 철수, 인수 테스트 지름길 재발견 피로.
- [HN 48742102](https://news.ycombinator.com/item?id=48742102) — 2026-07-01 — 맥락 의존 절충(개인 프로젝트 force multiplier).
- [HN 47320789](https://news.ycombinator.com/item?id=47320789) — 2026-03-10 — Redox OS no-LLM 정책: "코드가 노력의 증거였다".
- [HN 47958708](https://news.ycombinator.com/item?id=47958708) — 2026-04-30 — Zig 반-AI 기여 정책 + 리뷰 병목 지적.
- [HN 46689187](https://news.ycombinator.com/item?id=46689187) — 2026-01-20 — "AI가 그렇게 하기로 했고 나는 의문을 제기하지 않았다."
- [HN 46072620](https://news.ycombinator.com/item?id=46072620) — 2025-11-27 — AI 생성 PR 리뷰 부담이 메인테이너에게 지속 불가능.
- [HN 47788830](https://news.ycombinator.com/item?id=47788830) — 2026-04-16 — "엉망이고 위험한 걸 알면서도 쓰는 이유".

### GitHub Issues/PR — 프레임워크의 실제 불만·설계 토론
- [crewAI#6414](https://github.com/crewAIInc/crewAI/issues/6414) — 2026-07-01, 15댓글 — 결정적 루프 가드레일 제안. 위임 핑퐁·툴 루프·"맹목적 max_iter"·프롬프트 처방 실패 이유.
- [crewAI#4495](https://github.com/crewAIInc/crewAI/issues/4495) — 2026-02-16, 30댓글 — 1.6.1→1.9.3 회귀로 툴 인자 누락 → 무한 툴 루프. "실행 증폭기" 진단 + 결정적/일시적 실패 분리 휴리스틱.
- [crewAI#4682](https://github.com/crewAIInc/crewAI/issues/4682) — 2026-03-03, 13댓글 — 반복 행동 패턴 탐지·차단 미들웨어 요청. **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [crewAI#6025](https://github.com/crewAIInc/crewAI/issues/6025) — 2026-06-03, 108댓글 — 에이전트/툴 실행 전 런타임 릴리스 통제 중재 계층. 승인 게이트 수요의 규모 지표. **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [langgraph#7714](https://github.com/langchain-ai/langgraph/issues/7714) — 2026-05-05, 21댓글 — 체크포인트 직렬화 저장 85%·토큰 37.8% 오버헤드 주장. "지연이 먼저, 청구서가 나중". **검증 필요**
- [langgraph#7844](https://github.com/langchain-ai/langgraph/issues/7844) — 2026-05-17, 28댓글 — 완료 주장 영수증(claim/evidence/authority). "Done. All tests passed." 실패 모드. ※ 스레드 후반은 벤더 홍보 다수.
- [langgraph#8026](https://github.com/langchain-ai/langgraph/issues/8026) — 2026-06-09, 40댓글 — HITL용 고수준 ApprovalNode 요청. **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [langgraph#4973](https://github.com/langchain-ai/langgraph/issues/4973) — 2025-06-05, 85댓글 — LangGraph v1 로드맵 피드백 스레드(사용자 우선순위의 광범위 표본). **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [langchain#38843](https://github.com/langchain-ai/langchain/issues/38843) — 2026-07-14, 13댓글 — `enable_thinking=true`에서 성능 저하·무한 추론 루프. **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [autogen#7487](https://github.com/microsoft/autogen/issues/7487) — 2026-03-29, 74댓글 — "멀티에이전트에는 보스 에이전트가 아니라 목표 무결성 노드가 필요하다"(목표 이탈 문제). **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [autogen#7275](https://github.com/microsoft/autogen/issues/7275) — 2026-02-26 — 멀티에이전트 루프의 결정적 종료 계약 테스트 요청. **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [openai-agents-python#2868](https://github.com/openai/openai-agents-python/issues/2868) — 2026-04-09, 31댓글 — 툴별 권한 미들웨어 요청. **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**
- [claude-code#42796](https://github.com/anthropics/claude-code/issues/42796) — 2026-04-02, 583댓글/3290반응 — 모델 업데이트 후 복잡 작업 품질 회귀 대규모 불만. **에이전트 제품의 비결정적 회귀가 사용자 신뢰에 미치는 영향의 규모 지표.** **(제목·댓글 수만 확인 — 본문 미열람. 직접 인용 금지)**

### 한국 커뮤니티·블로그
- [youngju.dev](https://www.youngju.dev/blog/2026-07-17-agent-production-failure-taxonomy-idempotency) — 2026-07-17 — "AI 에이전트는 프로덕션에서 어떻게 실패하는가 — 14가지 실패 모드, 그리고 재시도가 안전하지 않은 이유". MAST 분류를 실무자 관점으로 정리 + 멱등성·재시도 안전성 논의. **한국어 최고 품질 소스. 백분율은 외부 논문 인용.**
- [GeekNews 30336](https://news.hada.io/topic?id=30336) — 2026-06경 — "루프 엔지니어링". 댓글에 용어 인플레이션 피로·"검증은 본인 몫" 등 국내 반응.
- [GeekNews 27457](https://news.hada.io/topic?id=27457) — 2026-03경 — "하네스 엔지니어링: 에이전트 우선 세계에서 Codex 활용하기". AGENTS.md를 "백과사전이 아닌 목차"로, 린터·구조적 테스트로 아키텍처 강제, 엔트로피 "가비지 컬렉션". 댓글에 국내 사례(130억 토큰) 참조.
- [GeekNews 27861](https://news.hada.io/topic?id=27861) — 2026-03경 — "속도를 늦춰야 하는 이유". `GN⁺`(**AI 요약 봇** — 인용 금지) 댓글에 DB 삭제 사건의 국내 전파와 "메타 작업" 피로가 나타남.
- [GeekNews 27858](https://news.hada.io/topic?id=27858) — 2026-03경 — "속도를 늦춰야 빨라진다". 국내 댓글이 기술 논쟁보다 정서적 반응에 머무는 경향의 사례.
- [GeekNews 27863](https://news.hada.io/topic?id=27863) — 2026-03경 — "장기 실행 애플리케이션 개발을 위한 하네스 설계"(Anthropic의 생성자·평가자·계획자 3에이전트 구조). **댓글 없음** — 축 9·논쟁 2와 직접 관련되나 국내 토론이 형성되지 않았다.

---

## 수집 한계 (정직하게)

1. **Reddit 본문 미수집.** r/LocalLLaMA·r/LangChain·r/ExperiencedDevs를 목표로 했으나 검색 엔진 경유로는 스레드 본문·댓글의 **원문 인용을 확보할 수 없었다**(Reddit은 자동 접근을 차단). HN Algolia API로 댓글 본문을 직접 수집해 **양적·질적으로 대체 보충**했다(218개 댓글 원문 수집 → 56개 스레드 선별). Reddit 특유의 로컬 모델·자가 호스팅 관점은 이 문서에서 과소 대표되어 있다.
2. **⚠️ 가장 큰 약점 — 한국 커뮤니티 토론이 얇다.** 최종 한국 소스는 **개인 기술 블로그 1건 + GeekNews 토픽 4건**이다. 시도한 것과 결과:
   - **OKKY·velog·커리어리:** 검색 결과가 **튜토리얼·입문 글에 압도적으로 지배**되어 실무 실패 후기 성격의 토론을 찾지 못했다.
   - **GeekNews:** 토픽 페이지는 원문 파싱이 되어 댓글을 확보했으나(30336·27457·27858·27861), **에이전트 관련 토픽의 댓글이 대체로 짧은 정서적 반응**(용어 피로, 가벼운 공감)에 머물고 기술적 논쟁으로 발전하지 않았다. GeekNews 사이트 검색(`/search?q=`)은 접근되지 않았고, 주간 다이제스트(`/weekly/202613` 등)로 토픽을 역추적하는 방식만 통했다.
   - **결론:** 이 주제에 대한 **깊은 기술 논쟁은 현재 영어권(HN·GitHub)에 압도적으로 편중**되어 있다. 이것은 수집 실패라기보다 **관찰된 사실**로 보이며, 그 자체가 책의 포지셔닝 근거가 된다 — 한국어로 정리된 운영 현실 자료가 희소하다.
   - **보강 제안(web-researcher 이관):** 커뮤니티 포럼보다 **국내 컨퍼런스 발표**(if(kakao)·DEVIEW·FEConf·인프콘)와 **회사 기술블로그**(우아한형제들·토스·카카오·네이버 D2·LINE)를 직접 훑는 편이 이 공백에 훨씬 효과적일 것이다. 특히 youngju.dev 수준의 1차 자료 대조형 국내 글을 더 찾는 것이 우선순위가 높다.
3. **Discord/Slack 공개 로그, X/Mastodon 미수집.** 접근 경로가 없었다.
4. **HN 개별 스레드 페이지 fetch가 429로 차단됐다.** 그래서 Algolia API로 우회했다. 부작용: **댓글의 스레드 내 위치·부모 자식 관계·점수를 알 수 없다.** 어떤 인용이 스레드에서 지지받았는지(최상위 댓글인지 묻힌 댓글인지) 판별할 수 없다 — **인용의 "커뮤니티 대표성"을 과대평가하지 말아야 한다.**
5. **⚠️ 최근 GitHub 이슈 스레드의 댓글 품질 문제.** 2026년 GitHub 스레드에서 **LLM으로 작성된 듯한 매끄러운 댓글과 노골적 벤더 홍보**(서명 영수증·게이트웨이·거버넌스 플랫폼 등)가 다수 관찰됐다. 특히 [langgraph#7844](https://github.com/langchain-ai/langgraph/issues/7844) 후반부가 그렇다. **원 이슈 작성자의 구체적 버그 리포트를 우선하고, 스레드 참가자의 일반론은 신뢰도를 낮춰 취급했다.** 이 현상 자체도 책에서 다룰 소재가 될 수 있다(에이전트가 오픈소스 토론 자체를 오염시키는 문제).
6. **자기 선택 편향.** 커뮤니티는 불만이 있는 사람이 더 많이 쓴다. 특히 논쟁 7(생산성)에서 이 편향이 심각하다. **정량 주장은 반드시 통제 연구로 보완해야 한다.**
7. **벤더 편향.** Show HN·Launch HN 항목 다수가 자기 해법을 파는 맥락이다. 이 문서는 그런 경우를 표시했지만(`※` 또는 "벤더 맥락"), **처방보다 진단을 신뢰하는 방향으로 읽어야 한다.**

## 검증 필요로 남긴 주장 (fact-checker·paper-researcher 인계)

**총 20건.** 책에 수치로 쓰려면 반드시 해소해야 한다.

### 최우선 — 그리고 대부분 1차 소스로 확인 가능하다 (youngju.dev가 제시한 검증 가능 주장)
아래 6건은 **커뮤니티 주장이 아니라 공개 스펙·표준 문서로 직접 확인 가능한 사실 주장**이다. 확인되면 책의 가장 단단한 근거가 된다. **web-researcher 최우선 배정 권장.**

| # | 주장 | 확인 방법 |
|---|------|-----------|
| A | MCP 스펙(리비전 2025-11-25) 스키마 2573줄에서 `idempotentHint`가 선언되는 한 곳에만 등장하고 "retry"가 한 번도 안 나온다 | MCP 스키마 파일 직접 grep |
| B | MCP 툴 애노테이션 기본값: `readOnlyHint` false / `destructiveHint` **true** / `idempotentHint` false / `openWorldHint` true | MCP 스펙 문서 |
| C | 스펙 원문: "클라이언트는 신뢰할 수 없는 서버로부터 받은 ToolAnnotations에 근거해 도구 사용을 결정해서는 안 된다" | MCP 스펙 원문 대조 |
| D | IETF `Idempotency-Key` 헤더 드래프트가 2020-11-17 시작, 2026-04-18 만료, IESG 상태 "I-D Exists", 5년 반째 RFC 아님 | IETF 데이터트래커 |
| E | Stripe 멱등성 관행: 첫 요청의 상태 코드·응답 본문 저장, **500 에러까지 재생**, 보존 24시간 | Stripe API 문서 |
| F | OpenTelemetry GenAI 시맨틱 컨벤션에 **비용 지표가 없다** | OTel 스펙 |

### 커뮤니티 주장 (독립 검증 어려움 — 귀속 인용만)

| # | 주장 | 출처 | 필요한 검증 |
|---|------|------|-------------|
| 1 | 체크포인트 직렬화 저장 85% 팽창·토큰 37.8% 오버헤드 | [langgraph#7714](https://github.com/langchain-ai/langgraph/issues/7714) | 재현 스크립트 실행 또는 메인테이너 확인 |
| 2 | 14,000+ 에이전트 세션에서 "차선 이탈" 일상적 | [HN 47161210](https://news.ycombinator.com/item?id=47161210) | 벤더 자체 로그 — 독립 검증 불가 가능성 높음. "한 샌드박스 사업자의 관찰"로 귀속 |
| 3 | 인젝션 18개 벡터 중 12개 우회(비영어 전부 포함) | [HN 47325268](https://news.ycombinator.com/item?id=47325268) | 방법론·대상 제품 미공개. 학술 인젝션 벤치마크로 대체 권장 |
| 4 | 장기 실행 루프 50~60턴에서 상태 붕괴 | [HN 47126051](https://news.ycombinator.com/item?id=47126051) | 개인 관찰. lost-in-the-middle/롱 컨텍스트 열화 논문으로 보강 |
| 5 | MAST 14개 실패 모드 백분율(단계 반복 15.7%·종료 조건 미인지 12.4%·시스템 설계 44.2%·에이전트 간 32.3%·검증 23.5%), 트레이스 1642건, 카파 0.88, 실패율 41~86.7% | [youngju.dev](https://www.youngju.dev/blog/2026-07-17-agent-production-failure-taxonomy-idempotency) → arXiv:2503.13657 (UC 버클리, NeurIPS 2025) | **paper-researcher가 원 논문 Figure 1 직접 대조 필수.** ⚠️ **널리 퍼진 오인용 세트 "42%/37%/21%"이 존재하며 논문에 없는 숫자다 — 어디서 보더라도 쓰지 말 것.** 또 **MAST 자체가 o1 기반 LLM-as-judge로 라벨링**했으므로 축 7의 판정자 신뢰성 문제가 이 데이터에도 적용된다는 점을 책에 명시할 것 |
| 6 | LLM-as-judge 길이 편향 | [HN 44832641](https://news.ycombinator.com/item?id=44832641) → arXiv 2407.01085 | paper-researcher 원 논문 확인 |
| 7 | 컨텍스트 캐싱으로 API 비용 ~80% 절감 | [HN 47050712](https://news.ycombinator.com/item?id=47050712) | 개인 주장. 공급사 공식 캐싱 가격표로 대체 권장(web-researcher) |
| 8 | MCP 툴 5개로 100k 토큰 윈도가 찬다 | [HN 43797945](https://news.ycombinator.com/item?id=43797945) | ⚠️ **flagged(dead) 댓글 + 2025-04 자료. 인용 비권장.** 실제 툴 정의 토큰 수를 직접 측정해 대체 |
| 9 | Copilot VSCode 확장 MCP 툴 ~20개 | [HN 47158526](https://news.ycombinator.com/item?id=47158526) | 현재 버전 직접 확인 |
| 10 | 3개 프롬프트에 $45 / 1시간15분에 $120 | [HN 49040461](https://news.ycombinator.com/item?id=49040461), [HN 49030357](https://news.ycombinator.com/item?id=49030357) | 개인 지출 — 검증 불가. "한 사용자의 보고"로만 인용 |
| 11 | 바이브 코딩 도구에서 보안 문제 28개 | [HN 48094454](https://news.ycombinator.com/item?id=48094454) | 개인 리뷰. 숫자 없이 정성 주장으로만 인용 권장 |
| 12 | litellm 공급망 침해 사건 | [HN 47581930](https://news.ycombinator.com/item?id=47581930) | **web-researcher가 1차 공지·CVE로 확인 필수** |
| 13 | 40일·100만 줄·130억 토큰(국내 사례) | [GeekNews 27457](https://news.hada.io/topic?id=27457) 댓글 | 원 발표·기고 직접 확인 |
| 14 | AutoGen이 Semantic Kernel로 병합될 것 | [HN 42449742](https://news.ycombinator.com/item?id=42449742) | ⚠️ **2024-12 예측. 2026-07 현재 상태를 web-researcher가 반드시 확인** — 틀린 예측일 가능성 있음 |

## 후속 리서치 제안

1. **`max_iter` 실무 기본값의 실제 분포** — 커뮤니티는 "상한이 틀렸다"에는 합의하지만 **무엇으로 대체하는지는 각자 다르다**(궤적 해시, 개선 측정, 예산 상한, 벽시계 타임아웃). 프레임워크 기본값을 직접 조사하면 책에 표를 넣을 수 있다.
2. **한국 사례 보강** — 위 한계 2번. 국내 컨퍼런스 발표·회사 기술블로그 경로가 커뮤니티 포럼보다 생산적일 것으로 보인다.
3. **비용 관측 스택의 실제 구성** — "단위 원가를 트레이스의 일급 차원으로"라는 처방은 반복되지만 **구현 사례가 벤더 홍보에 묻혀 있다.** 중립적 구현(OpenTelemetry GenAI 시맨틱 컨벤션 등)을 web-researcher가 확인하면 실용적 챕터가 나온다.
