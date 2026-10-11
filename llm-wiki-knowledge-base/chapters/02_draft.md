# 2장. 컨텍스트 윈도우는 용량이지 성능이 아니다

32K 토큰. 2025년 ICML에 발표된 NoLiMa 벤치마크(Modarressi 외, arXiv 2502.05167)에서 입력이 이 길이에 이르자 11개 모델이 짧은 입력에서 내던 점수의 절반 아래로 떨어졌다. GPT-4o는 99.3%에서 69.7%로 내려갔다. 128K 컨텍스트를 표방한 Llama 3.1 70B의 유효 길이는 2K였고, 32K에서는 42.7%를 기록했다. 2026년 10월 기준 Claude의 주요 모델이 100만 토큰 컨텍스트 윈도우를 기본으로 제공한다는 사실 옆에 이 숫자를 놓으면, 앞 장 끝의 질문이 조금 다르게 들린다. 60건을 통째로 넣을 수 있다는 것과, 통째로 넣고 물었을 때 제대로 답한다는 것은 같은 말이 아니다.

### 용량과 성능은 다른 축이다

Anthropic 자신의 문서가 먼저 이 구분을 한다. 2025년 9월 29일 공개한 컨텍스트 엔지니어링 글은 컨텍스트 엔지니어링을 "the set of strategies for curating and maintaining the optimal set of tokens (information)"로 정의하고, 목표를 "finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome"으로 둔다. 가능한 한 작은 고신호 토큰 집합이다. LLM에는 "attention budget"이 있고, 그 예산을 넘기면 "context rot"가 온다는 것이다. 2026년 10월 11일 열람 기준 Claude API 문서는 더 직설적이다. "more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot. This makes curating what's in context just as important as how much space is available." 공간이 얼마나 있느냐만큼 무엇을 넣느냐가 중요하다.

이 책은 이 현상을 **컨텍스트 로트(context rot)**라고 음차해 부른다. 10장에서 만날 **조용한 부패(silent rot)**, 그러니까 위키 내용이 낡아도 아무 신호가 없는 상태와는 다른 현상이어서 둘을 섞지 않으려고 그렇게 한다.

가장 체계적인 측정은 벡터 DB 회사 Chroma가 2025년 7월 14일 낸 기술 보고서 "Context Rot"(Hong·Troynikov·Huber)다. 동료심사를 거치지 않은 벤더 보고서이고 arXiv ID도 없다는 점은 미리 밝혀 둔다. 18개 모델을 8개 입력 길이와 11개 바늘(needle) 위치로 돌린 결과, "their performance grows increasingly unreliable as input length grows." 여기까지는 예상 범위다. 예상 밖은 다음 문장이다. "Surprisingly, we find that structural coherence consistently hurts model performance." 문단이 논리적으로 잘 이어진 긴 문서가, 문장을 뒤섞은 문서보다 바늘 찾기에 더 불리했다. 그리고 "Even a single distractor reduces performance relative to the baseline." 방해 문서 하나만 있어도 성능이 떨어진다. LongMemEval 306문항에서는 모든 모델이 약 300토큰짜리 집중 프롬프트에서 약 113K 토큰짜리 전체 프롬프트보다 높은 점수를 냈다.

이 보고서가 사내 지식 베이스에 주는 교훈을 하나로 압축하면 이렇다. 컨텍스트 윈도우는 용량이지 성능 보증이 아니다. 60건의 소스를 다 넣을 수 있다. 그러나 그 안에서 가격 한 줄을 찾아야 하는 모델에게 나머지 59건은 방해 문서다. 그것도 잘 짜인, 논리적으로 이어진 방해 문서다.

### 네 편의 논문이 같은 방향을 가리킨다

Chroma의 보고서는 2023년부터 쌓여 온 학계 결과의 연장선이다. 네 편만 순서대로 보자. 각각이 위키의 설계 결정 하나와 맞닿는다.

**Lost in the Middle**(Liu 외, arXiv 2307.03172, TACL 2023). 관련 정보가 입력의 앞이나 끝에 있을 때 성능이 가장 높고, "significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models." 20개 문서를 주는 설정에서 정답 문서가 맨 앞이면 75.8%, 중간(인덱스 9)이면 53.8%, 맨 끝이면 63.2%였다. 이 세 수치는 논문 부록 표에서 읽어 낸 계산값이지 논문 본문의 문장은 아니다. 문서를 하나도 주지 않은 closed-book이 56.1%였으니, 정답이 한가운데 묻힌 20문서는 아무것도 안 준 것과 거의 같았다는 뜻이다. 하나 더. "Using more than 20 retrieved documents only marginally improves reader performance." 2023년 모델 기준이라는 한계는 분명하다. 그래도 "어디에 두느냐가 중요하다"는 발견은 이후 연구에서 되풀이 확인된다. 위키로 옮기면 이렇다. 데스크가 읽을 페이지는 적어야 하고, 답에 필요한 문장은 페이지 맨 위에 있어야 한다. 4장의 TL;DR 규약이 여기서 나온다.

**Same Task, More Tokens**(Levy 외, arXiv 2402.14848, ACL 2024). 같은 추론 과제에 무관한 텍스트를 덧붙여 길이만 늘렸다. 500토큰을 넘으면서부터 유의하게 떨어지기 시작해 3,000토큰에서 전체 평균 정확도가 0.92에서 0.68이 됐다. 논문의 표현으로는 "a notable degradation in LLMs' reasoning performance at much shorter input lengths than their technical maximum." 기술적 최대치보다 훨씬 짧은 곳에서 추론이 흔들린다. 위키로 옮기면, 페이지는 짧고 밀도 있게, 한 페이지에 한 주제다. 가격 페이지 아래에 가격 변경 이력을 열 줄쯤 붙여 두고 싶은 유혹을 참아야 하는 이유이기도 하다.

**RULER**(Hsieh 외, arXiv 2404.06654, COLM 2024). "While these models all claim context sizes of 32K tokens or greater, only half of them can maintain satisfactory performance at the length of 32K." 표기 컨텍스트와 유효 컨텍스트는 다르다. 모델 카드의 숫자를 설계 가정으로 삼지 말자는 뜻이다.

**NoLiMa**(Modarressi 외, arXiv 2502.05167, ICML 2025). 이 장을 연 그 논문이다. 숫자보다 설계가 중요하다. NoLiMa는 질문과 정답 문장 사이에 글자 그대로 겹치는 어휘가 없도록 만들었다. 질문의 단어를 본문에서 찾기만 하면 되는 바늘 찾기와 달리, 모델이 뜻을 연결해야 찾을 수 있는 바늘이다. 어휘가 겹칠 때는 긴 입력에서도 꽤 버티던 모델들이, 겹치지 않자 무너졌다. 대부분 모델의 유효 길이가 2K 이하였고 GPT-4o가 8K였다. 위키로 옮기면 이것은 뜻밖의 설계 근거가 된다. 김보라가 "톤앤매너"라고 묻는데 브랜드 가이드에는 "보이스 가이드라인"이라고 쓰여 있다면, 긴 원문 속에서 모델은 그 연결을 놓치기 쉽다. 위키의 개념 페이지는 질문의 언어와 페이지의 언어를 미리 맞춰 둔다. 용어 정규화 페이지와 동의어 항목이 괜히 있는 것이 아니다.

국내 실무에서도 같은 관찰이 있다. LY Corporation의 엔터프라이즈 LLM 서비스 구축기는 Databricks 연구를 인용해 "GPT-4나 Llama-3.1 같은 모델에서도 컨텍스트가 특정 구간(32K~64K 토큰)을 넘어가면 RAG 성능이 하락하기 시작했습니다"라고 적었다(글의 발행일이 페이지에 표시되어 있지 않다 — 사실 확인 필요). HN의 lelanthran은 같은 말을 한 줄로 했다. "What use is 10M context if degradation starts at 200k - 300k?"

### 반대편 기준 — "200K 토큰이면 통째로"

균형을 위해 반대편도 보자. 같은 Anthropic이 2024년 9월 19일 Contextual Retrieval 글에서 이렇게 썼다. "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material)," 검색 없이 전체를 프롬프트에 넣고 프롬프트 캐싱을 쓰라. 이 기준은 2024년 기준이고 Claude 3 세대 실험에서 나왔다. 그 뒤 같은 회사가 2025년과 2026년 문서에서 컨텍스트 로트를 말한다. 모순일까? 시점과 모델 세대가 다르고, 무엇보다 두 주장은 양립한다. 작으면 통째로 넣고 캐싱하라. 그래도 컨텍스트 로트는 존재한다. 이 책은 둘을 이렇게 병기한다.

페이지원의 출발점 60건은 아마 200K 안에 들어간다. 그러니 첫 주에 데스크를 "소스 전부를 시스템 프롬프트에 붙인 챗봇"으로 띄워 보는 것은 정직한 실험이다. 8장은 실제로 거기서 출발한다. 찜찜한 것은 여섯 달 뒤다. 300건이 되면 200K를 넘길 가능성이 크고, 넘기기 전에도 가격 한 줄을 찾는 질문에 나머지 299건이 방해 문서로 작동한다. 캐싱이 비용은 줄여 주지만 공간은 줄여 주지 않는다는 점도 기억해 두자. 2026년 10월 11일 열람 기준 Claude API 문서는 이렇게 못 박는다. "Cached prompt prefixes still occupy the context window: prompt caching changes what you pay for those tokens, not whether they count."

이 두 기준 사이에서 설계자가 할 일은 분명해진다. 지금 규모에서 통째로가 되는지는 실험으로 확인하되, 설계는 통째로가 안 되는 날을 기준으로 한다.

### 기억의 계보 — `raw/`와 `wiki/`의 분리는 어디서 왔나

Karpathy의 gist는 참고문헌 없이 쓰였지만, `raw/`와 `wiki/`를 가르는 발상에는 학술적 조상이 있다. 셋을 시간순으로 보면 위키의 부품 하나하나가 어느 연구의 어느 부품에 대응하는지 보인다.

**Generative Agents**(Park 외, arXiv 2304.03442, UIST 2023 — 발표처는 Semantic Scholar 표기 기준). 가상 세계의 에이전트가 겪은 일을 전부 memory stream에 기록하고, 그 기록에서 주기적으로 reflection, 그러니까 합성 통찰을 만든다. 원본 기록과 합성 통찰의 분리가 `raw/`와 `wiki/` 분리의 선조다. 일기(raw)와 주간 회고(reflection)라고 생각하면 이해하기 쉽다. 검색 점수는 recency·importance·relevance의 가중합이고(가중치 모두 1, min-max 정규화), recency는 시간마다 0.995씩 감쇠한다. 하루 지나면 0.995^24 ≈ 0.89다. 성찰은 최근 사건의 importance 합이 임계치를 넘으면 발동하는데, 논문의 구현에서는 150이었다. 위키의 린트가 "주기적으로"라는 느슨한 규칙 대신 "얼마나 많은 것이 들어왔는가"라는 트리거를 가질 수도 있다는 힌트다.

**MemGPT**(Packer 외, arXiv 2310.08560, 2023 프리프린트). 운영체제의 가상 메모리 비유를 LLM에 가져왔다. 컨텍스트 윈도우는 RAM처럼 작고, 그 밖에 큰 저장소가 있고, 모델이 스스로 페이지를 넣고 뺀다. 위키에 대입하면 `index.md`가 working context, 개별 페이지가 archival storage, `log.md`가 recall storage다. 결과도 선명하다. 대화 기억 검색(DMR) 정확도가 GPT-4 단독 32.1%에서 MemGPT 92.5%로, GPT-4 Turbo는 35.3%에서 93.4%로 올랐다. "MemGPT's performance is unaffected by increased context length." 컨텍스트를 늘려서 얻은 성능이 아니다. 무엇을 컨텍스트에 둘지 관리해서 얻은 성능이다.

**A-MEM**(Xu 외, arXiv 2502.12110, NeurIPS 2025). Zettelkasten 원리다. 새 노트가 들어오면 기존 노트와 링크를 만들 뿐 아니라, 이웃 노트의 문맥 설명과 태그까지 갱신한다. 논문은 이것을 memory evolution이라 부른다. "as new memories are integrated, they can trigger updates to the contextual representations and attributes of existing historical memories." 1장에서 본 "소스 하나가 10~15페이지를 건드린다"의 학술 대응물이 바로 이것이다. 논문이 보고한 토큰 비용 절감은 본문과 표의 수치가 어긋나므로 보수적으로 "최대 약 93%" 수준으로만 적어 둔다.

여기에 분류 체계 하나를 얹으면 그림이 닫힌다. 에이전트 메모리 서베이(Zhang 외, arXiv 2404.13501, 2024)는 메모리 연산을 writing·management·reading 셋으로 나눈다. 수집·린트·질의와 정확히 1:1이다. LLM 위키는 "텍스트 형식의 구조화 메모리에 명시적 관리 연산을 붙인 것"으로 학계 분류 안에 자리 잡는다. 이름이 새로울 뿐 발상은 새롭지 않다는 사실은 안심할 일이다. 검증된 조상이 있다는 뜻이니까.

### 모델을 고치지 말고 위키를 고쳐라

가격이 바뀌었다. 모델에게 새 가격을 "가르칠" 수는 없을까? 지식 편집(knowledge editing) 연구는 정확히 그 질문을 다루고, 그 답은 사내 지식 베이스를 짓는 사람에게 유리하다.

**Editing LLMs**(Yao 외, arXiv 2305.13172, EMNLP 2023). 단일 사실 편집 자체는 잘 된다. ROME·MEMIT의 reliability가 99를 넘는다. 문제는 portability다. 편집한 사실에서 한 단계 추론해야 하는 질문(one-hop)에서 최고 방법도 약 55%(IKE 55.38, MEMIT 52.74)였고, SERAC은 세 항목 모두 20% 미만이었다. "current model editing techniques continue to face challenges in managing the ramifications of an edit." 프로 플랜을 39,000원으로 바꿔 넣어도 "그럼 베이직이랑 차이가 얼마야"로 이어지지 않는다는 뜻이다.

**Ripple Effects**(Cohen 외, arXiv 2307.12976, TACL 2024). 한 사실을 바꾸면 거기 딸린 사실들도 바뀌어야 한다는 파급 효과를 벤치마크로 만들었다. 결과가 흥미롭다. "a simple in-context editing baseline obtains the best scores on our benchmark." 가중치를 건드리는 어떤 방법보다, 바뀐 사실을 컨텍스트에 넣어 주는 단순한 기준선이 가장 좋았다. 위키의 수집이 관련 페이지 10~15개를 함께 고치는 것이 바로 이 파급 처리다. 모델 안에서 못 하는 일을 파일 사이에서 하는 셈이다.

지식 편집 분류(Zhang 외, arXiv 2401.01286, 2024)는 접근을 셋으로 나눈다. 외부 지식에 의존하기, 지식을 모델에 병합하기, 내재 지식을 편집하기. LLM 위키는 첫째 계열의 가장 단순한 구현이다. "가장 단순하다"가 약점처럼 들리면 Ripple Effects의 결과를 다시 보자.

사실에는 유효 기간이 있다. Dhingra 외(arXiv 2106.15110, TACL 2022)는 이렇게 썼다. "Many facts come with an expiration date, from the name of the President to the basketball team Lebron James plays for." 프로 플랜 가격도 그렇다. 29,000원은 2026년 8월 31일까지 참이었고 9월 1일부터 거짓이다. 그러면 위키 페이지에는 사실과 함께 그 사실이 언제부터 언제까지 참인지가 적혀 있어야 한다. 4장의 `valid_from`·`valid_to` 프런트매터가 여기서 나온다.

**TemporalWiki**(Jang 외, arXiv 2204.14211, EMNLP 2022)는 위키피디아의 두 시점 사이 diff만으로 모델을 계속 학습시키면, 전체 스냅샷으로 학습한 것과 비슷하거나 더 나은 perplexity를 12분의 1 계산 비용으로 얻는다고 보고했다. 학습 맥락의 결과지만, 위키에 옮기면 증분 수집의 근거다. 바뀐 소스만 처리하고 `log.md`를 diff 원장으로 쓴다. 10장의 "전체 리빌드 vs 증분" 논쟁에서 증분 편에 서는 근거 중 하나다.

**FreshLLMs**(Vu 외, arXiv 2310.03214, ACL 2024 Findings — Semantic Scholar 표기 기준). 모델 크기와 무관하게 "all models (regardless of model size) struggle on questions that involve fast-changing knowledge and false premises." 그리고 실용적인 발견 하나. "instructing the LLM to generate concise and direct answers helps reduce hallucination compared to encouraging more verbose answers." 간결하고 직접적인 답을 지시하면 환각이 줄어든다. 6장의 데스크 답변 프롬프트에 "간결하게, 근거 페이지를 명시해"라는 줄이 들어가는 이유다.

### 페이지원에 적용하기 — 근거 번호 목록

이제 이 장의 결과를 페이지원의 설계로 접어 두자. 사내 지식 다섯 유형 가운데 가격·전략 결정·도구 사용법은 FreshLLMs가 말하는 fast-changing 지식이다. 브랜드와 시나리오는 상대적으로 느리다. 그러니 빨리 변하는 유형일수록 페이지를 짧고 밀도 있게, 날짜를 붙여, 질문의 언어로 쓴다. 다음 표는 이 장에서 끌어온 근거가 뒤의 어느 설계 결정을 떠받치는지 묶은 것이다. 이후 장에서 결정을 내릴 때마다 이 표의 행을 다시 가리킬 것이다.

| 설계 결정 | 근거 | 구현하는 장 |
|---|---|---|
| 데스크는 소스 전부가 아니라 페이지 몇 장만 읽는다 | Chroma Context Rot(2025, 비동료심사), Lost in the Middle(arXiv 2307.03172) | 7장 |
| 페이지는 짧고 한 주제, 핵심은 맨 위(TL;DR) | Same Task More Tokens(arXiv 2402.14848), Lost in the Middle | 4장 |
| 모델 카드의 컨텍스트 길이를 설계 가정으로 쓰지 않는다 | RULER(arXiv 2404.06654), NoLiMa(arXiv 2502.05167) | 7·8장 |
| 질문의 언어와 페이지의 언어를 맞추는 용어·동의어 페이지 | NoLiMa | 4·7장 |
| `raw/`(기록)와 `wiki/`(합성) 분리, `index.md`는 작업 컨텍스트 | Generative Agents(arXiv 2304.03442), MemGPT(arXiv 2310.08560) | 4장 |
| 수집 시 관련 페이지를 함께 갱신 | A-MEM(arXiv 2502.12110), Ripple Effects(arXiv 2307.12976) | 5장 |
| 사실에 유효 기간(`valid_from`/`valid_to`) | Dhingra 외(arXiv 2106.15110) | 4·10장 |
| 바뀐 소스만 증분 수집, `log.md`를 diff 원장으로 | TemporalWiki(arXiv 2204.14211) | 5·10장 |
| 답변 프롬프트는 간결하게, 근거 페이지 명시 | FreshLLMs(arXiv 2310.03214) | 6장 |
| 작은 규모에서는 통째로 + 캐싱도 정직한 선택(2024년 기준) | Contextual Retrieval(Anthropic, 2024-09-19) | 8장 |

정직하게 적어 둘 것이 하나 있다. 이 가운데 "LLM이 유지보수하는 위키" 자체를 직접 실험한 동료심사 논문은 없다. 가장 가까운 것이 A-MEM의 Zettelkasten 메모리다. 그래서 이 책의 설계 결정은 전부 인접 연구에서 끌어온 근거에 기댄다. 장마다 어느 근거에 기대는지 밝히는 것은 그 제약을 감추지 않기 위해서다.

모델에게 기억은 없고, 우리가 파일로 남겨 둔 것만큼만, 그것도 모델이 찾아 읽을 수 있는 자리에 있을 때만 있다.
