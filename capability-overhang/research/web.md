# 웹 리서치: AI Capability Overhang

리서치 일자: 2026-05-18. research-lead가 직접 수행 (Agent 도구 미가용 환경).

## 자료 1: Jack Clark, "Import AI 310" (2022-11-28)
- 출처: https://jack-clark.net/2022/11/28/import-ai-310-alphazero-learned-chess-like-humans-learn-chess-capability-emergence-in-language-models-demoscene-ai/
- 저자·날짜: Jack Clark (Anthropic 공동창업자), 2022년 11월 28일
- 핵심 주장: 137건의 LLM emergent ability 사례가 "capabilities overhang"의 증거다. 모델은 우리가 아는 것보다 훨씬 능력이 크고, 우리가 가진 탐사 기법이 유아 수준이다.
- 인용 가능한 구절: "Because language models have a large capability surface, these cases of emergent capabilities are an indicator that we have a 'capabilities overhang' — today's models are far more capable than we think, and our techniques available for exploring the models are very juvenile."
- 관련 섹션: 1.1 정의·어원, 1.3 역사적 흐름

## 자료 2: Jack Clark, "Import AI 321" (2023-03-21)
- 출처: https://jack-clark.net/2023/03/21/import-ai-321-open-source-gpt3-giving-away-democracy-to-agi-companies-gpt-4-is-a-political-artifact/
- 핵심 주장: GPT-4는 GPT-3가 그랬듯 capability overhang을 안고 출시되었다. OpenAI 자신도 출시 시점에 모델 능력의 전모를 모른다.
- 인용: "GPT-4, like GPT-3 before it, has a capability overhang; at the time of release, neither OpenAI or its deployment partners have a clue as to the true extent of GPT-4's capability surface." / "The applications we're seeing of GPT-4 today are the comparatively dumb ones; the really 'smart' capabilities will *emerge* in coming months and years through a process of collective discovery."
- 관련 섹션: 1.1, 1.3, 3 사례

## 자료 3: Jack Clark, "Import AI 397" (2025-01-27)
- 출처: https://jack-clark.net/2025/01/27/import-ai-397-deepseek-means-ai-proliferation-is-guaranteed-maritime-wardrones-and-more-evidence-of-llm-capability-overhangs/
- 핵심 주장: Llama-3-1-Instruct 8B 같은 표준 모델이 단백질 공학을 수행해냈다. 더 이상 progress가 멈춰도 LLM의 잠재 능력 발굴은 계속될 것이다.
- 인용: "This paper is another demonstration of the significant utility of contemporary LLMs, highlighting how even if one were to stop all progress today, we'll still keep discovering meaningful uses for this technology in scientific domains."
- 관련 섹션: 3 사례

## 자료 4: Wiktionary "capability overhang"
- 출처: https://en.wiktionary.org/wiki/capability_overhang
- 정의: "Capabilities and potential applications of existing artificial intelligence systems that have not yet been discovered."
- First attestation: The Verge, 2022-12-08
- 관련 섹션: 1.1

## 자료 5: Alignment Forum "Are we in an AI overhang?" (2020-07)
- 출처: https://www.alignmentforum.org/posts/N6vZEnCn6A95Xn39p/are-we-in-an-ai-overhang
- 인접 개념: hardware overhang / compute overhang. "you have had the ability to build transformative AI for quite some time, but you haven't because no-one's realised it's possible."
- 관련 섹션: 1.2 인접 개념

## 자료 6: Dinand Tinholt (Medium), "The AI Capability Overhang"
- 출처: https://medium.com/@tinholt/the-ai-capability-overhang-why-the-most-powerful-technology-isnt-working-yet-1855eec909be
- 핵심: Kevin Scott(Microsoft CTO)의 "F1 자동차를 주차장에서만 모는" 비유. 데이터 분절·인프라 격차·리스크 마비를 원인으로 진단. Klarna가 인간 상담원 재고용한 사례. 생성AI 이니셔티브 42% 폐기율(이전 17%).
- 관련 섹션: 1.2, 2.4 조직 차원, 3 사례

## 자료 7: NEXT Conf, "Capability overhang, or the future of AI" (2023-08)
- 출처: https://nextconf.eu/2023/08/capability-overhang-or-the-future-of-ai/
- 핵심: "imagination is the bottleneck" — 기술이 아니라 상상력이 병목.
- 관련 섹션: 2.2 인지·UX 차원

## 자료 8: Anthropic, "Effective context engineering for AI agents" (2025)
- 출처: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 정의: "context engineering is the art and science of curating what will go into the limited context window from that constantly evolving universe of possible information."
- 기법: just-in-time retrieval, compaction, structured note-taking, sub-agent architectures.
- 인용: "find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."
- "context rot": 컨텍스트가 커지면 성능이 떨어지는 현상. attention budget이 유한.
- 관련 섹션: 2.3 인터페이스·툴 차원, 4.2/4.3 극복 전략

## 자료 9: Anthropic, "Effective harnesses for long-running agents"
- 출처: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 정의: agent harness — "framework that enables AI models to work effectively on tasks."
- 패턴: initializer agent + coding agent, init.sh, progress files, git logs.
- 관련 섹션: 2.3, 4.2

## 자료 10: BCG, "Are You Generating Value from AI? The Widening Gap" (2025-09)
- 출처: https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap
- 핵심 수치: 88% of companies use AI in some function but only ~39% see EBIT impact (McKinsey). 60% generate no material value despite investment, only 5% create substantial value at scale (BCG). Future-built leaders: 9-12개월 배포, 성공률 60%+ vs 후발주자 12%. (※ WebFetch 403, WebSearch 요약 인용.)
- 관련 섹션: 2.4, 5 논쟁점

## 자료 11: Pew Research, "About 1 in 5 US workers now use AI in their job" (2025-10-06)
- 출처: https://www.pewresearch.org/short-reads/2025/10/06/about-1-in-5-us-workers-now-use-ai-in-their-job-up-since-last-year/
- 21% use AI at work (2024년 16% → 2025년 21%). Bachelor+ 28% vs ≤some college 16%. 비사용자의 36%는 "내 업무가 AI로 가능"이라고 답함.
- 관련 섹션: 2.2, 5 사회적 함의

## 자료 12: Stanford HAI, "2025 AI Index Report"
- 출처: https://hai.stanford.edu/ai-index/2025-ai-index-report
- 광범위한 채택·격차·교육·평가 지표 (총괄 참조). 다른 자료에서 인용된 통계의 1차 출처.
- 관련 섹션: 2.5 평가 차원, 5

## 자료 13: OECD, "Bridging the AI Skills Gap" (2025-04)
- 출처: https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/04/bridging-the-ai-skills-gap_b43c7c4a/66d0702e-en.pdf
- 핵심: 77%의 기업이 2025–2030년 AI 재교육 계획. 13% 노동자만 AI 훈련 수강. 38% 기업만 AI 훈련 제공.
- 관련 섹션: 2.4, 4.1

## 자료 14: ZDNet Korea, "생성 AI 써본 직장인 10명 중 4명 '내 업무 대체되는 거 아냐?'" (2025-09-12)
- 출처: https://zdnet.co.kr/view/?no=20250912163742
- 핵심 수치: 전체 AI 서비스 사용률 64.7%, 매일 사용 18.2% (20대 24.6%, 30대 28.8%). ChatGPT 72.9% / Gemini 34.9% / Claude 4.9%. "업무 도움 됨" 61.3%, 실제 활용 45.4%. 대체 우려 42.2%. 30대(53.4%) · 40대(45.1%) 우려 최고.
- 관련 섹션: 2.2, 4.1, 5

## 자료 15: 매경/이데일리, "韓 직장인 절반, AI로 일한다…근로시간 1.5시간"
- 출처: https://magazine.hankyung.com/business/article/202508186236b
- 핵심: 한국 근로자 51.8% 업무에 생성형 AI 활용 (미국 26.5%의 2배). 한국 주당 5–7시간 사용, 미국 0.5–2.2시간. 하루 1시간+ 헤비유저 한국 78.6% vs 미국 31.8%.
- 인구통계 격차: 남성 55.1% vs 여성 47.7% / 청년층(18–29) 67.5% vs 장년층(50–64) 35.6% / 대학원졸 72.9% vs 대졸 이하 38.4%. 전문직 69.2% / 관리직 65.4% / 사무직 63.1%.
- 관련 섹션: 2.2, 3, 5

## 자료 16: 삼일PwC, "매일 AI 쓰는 직장인 급여·고용안정·생산성 높아"
- 출처: https://marketin.edaily.co.kr/News/ReadE?newsId=03522726642365720
- 핵심: 매일 AI 사용 직장인이 비사용자보다 급여·고용안정·생산성 모두 높음. 헤비유저-라이트유저 간 차이가 한국 노동시장에서 가시화.
- 관련 섹션: 5 사회적 함의

## 자료 17: GeekNews / Hada, "Claude Code 2주 사용 후기" (2025)
- 출처: https://news.hada.io/topic?id=22053
- 핵심 인용: "Sonnet 4는 대다수 상황에서 더 빠르고, 긴 맥락+에이전트 작업에 강점". 하이브리드 워크플로우(Opus 계획 + Sonnet 실행). 컨텍스트 관리: 압축 대신 새 채팅 시작, 별도 파일에 메모.
- 반대 의견: "18년차 프로그래머가 대규모 TypeScript 코드에 적용했으나 Cursor보다 느리고 리뷰도 어렵다."
- 관련 섹션: 3, 4.2, 5

## 자료 18: Karpathy, "Software 3.0" 강연 (Y Combinator, 2025-06)
- 출처: https://www.latent.space/p/s3 (요약), 원본 강연
- 핵심: Software 1.0(코드) → 2.0(데이터로 가중치) → 3.0(자연어 프롬프트). "Iron Man suit" 비유 — 자율 로봇이 아닌 전문가 능력 증폭. AI Generation – Human Verification 루프.
- 관련 섹션: 1.2, 2.3, 4

## 자료 19: Simon Willison, "Agentic Coding: The Future of Software Development with Agents" (2025-06)
- 출처: https://simonwillison.net/2025/Jun/29/agentic-coding/
- 핵심: 2025년 가장 큰 사건은 2월 Claude Code 출시. "agents = tools in a loop". 컨텍스트는 공짜가 아니다 — 모든 토큰이 행동을 바꾼다.
- 관련 섹션: 2.3, 4.2

## 자료 20: Disquiet, "Claude로 코드리뷰 경험 개선하기"
- 출처: https://disquiet.io/@williamjung/makerlog/claude%EB%A1%9C-%EC%BD%94%EB%93%9C%EB%A6%AC%EB%B7%B0-%EA%B2%BD%ED%97%98-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0
- 핵심: 한국 시니어 개발자의 Claude를 활용한 코드리뷰 워크플로우 개선 경험.
- 관련 섹션: 4.2

## 자료 21: 한국노동연구원·KRIVET 보고서
- 출처: https://www.krivet.re.kr/kor/sub.do?menuSn=12&pstNo=PB0000000596 (AI 리터러시 커리큘럼)
- 핵심: 한국의 AI 도입률은 OECD 평균 이하, 중소기업 도입 격차 큼. 가장 큰 장애요인은 '숙련 부족'.
- 관련 섹션: 2.4, 4.1, 5

## 자료 22: DeepMind, AlphaProof/AlphaGeometry 2 (IMO 2024 silver)
- 출처: https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/ ; Nature 2025 후속 논문 https://www.nature.com/articles/s41586-025-09833-y
- 핵심: 같은 베이스 모델도 formalizer + solver + AlphaZero + test-time RL 결합으로 IMO 4/6 해결, 은메달 기준선 달성. → 모델 능력 vs scaffold가 만든 능력의 분리.
- 관련 섹션: 3 사례, 2.3 인터페이스·툴 차원

## 자료 23: MIT Tech Review, "QuitGPT 캠페인" (2026-02)
- 출처: https://www.technologyreview.com/2026/02/10/1132577/a-quitgpt-campaign-is-urging-people-to-cancel-chatgpt-subscriptions/
- 핵심: 700,000명 ChatGPT 이탈. 거버넌스·정렬·sycophancy 이유.
- 관련 섹션: 5 논쟁점

## 수집 한계
- OpenAI ChatGPT-at-work PDF (https://cdn.openai.com/pdf/...chatgpt-usage-and-adoption-patterns-at-work.pdf): WebFetch가 PDF 바이너리를 읽지 못해 직접 인용 불가. 다른 보도(매경 등)에서 간접 수치만 확보.
- BCG 본문 페이지: 403. WebSearch 요약 의존.
- 토스·우아한형제들 기술 블로그: 직접 검색에서 매칭 안 됨 (주제 특화 글 부재 가능성). 보강 필요.
- 트위터/X thread: 검색 결과 인용 가능한 직접 quote 부족 (플랫폼 제한).
