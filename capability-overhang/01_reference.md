# AI Capability Overhang — 리서치 레퍼런스

> 책 주제: AI의 capability overhang — 모델/시스템이 실제로 가진 능력과, 사용자·개발자·조직이 실제로 끌어내 활용하는 정도 사이의 격차.
>
> 대상 독자: ① 일상·업무에서 AI를 쓰지만 잠재력을 충분히 끌어내지 못한다고 느끼는 사람, ② AI 코딩 도구를 쓰는 개발자, ③ AI 전문가·연구자.
>
> 작성: 2026-05-18, research-lead 직접 종합 (web/papers/community 3 lane).

---

## 1. 개념·정의

### 1.1 capability overhang의 정의와 어원

**가장 인용 가능한 정식 정의 (Jack Clark, Anthropic, Import AI 310, 2022-11-28)**

> "Because language models have a large capability surface, these cases of emergent capabilities are an indicator that we have a 'capabilities overhang' — today's models are far more capable than we think, and our techniques available for exploring the models are very juvenile."
>
> — *[Import AI 310](https://jack-clark.net/2022/11/28/import-ai-310-alphazero-learned-chess-like-humans-learn-chess-capability-emergence-in-language-models-demoscene-ai/)*

Jack Clark는 137건의 LLM emergent ability 사례(Wei et al. 2022 [arXiv:2206.07682])를 가리키며 이 용어를 도입했다. 핵심은 두 가지다.

1. **모델이 가진 능력의 표면(capability surface)이 크다.**
2. **우리가 그것을 탐사하는 기법은 유아 수준이다.**

이듬해 GPT-4 출시 직후 Clark는 [Import AI 321 (2023-03-21)](https://jack-clark.net/2023/03/21/import-ai-321-open-source-gpt3-giving-away-democracy-to-agi-companies-gpt-4-is-a-political-artifact/)에서 이를 일반화했다.

> "GPT-4, like GPT-3 before it, has a capability overhang; at the time of release, neither OpenAI or its deployment partners have a clue as to the true extent of GPT-4's capability surface... The applications we're seeing of GPT-4 today are the comparatively dumb ones; the really 'smart' capabilities will *emerge* in coming months and years through a process of collective discovery."

용어는 곧 일반 매체로 퍼졌다. *The Verge* (2022-12-08)가 "capability overhang, or hidden skills and dangers of artificial intelligence"로 처음 보도하면서 사전 등재 기준점이 되었고 [Wiktionary, "capability_overhang"](https://en.wiktionary.org/wiki/capability_overhang), *The Guardian*과 *Wall Street Journal*도 동일한 의미로 사용했다.

**책에서 쓸 정의 (편집판)**

> Capability overhang이란, AI 시스템이 잠재적으로 가진 능력과 사용자·개발자·조직이 실제로 끌어내 활용하는 능력 사이의 격차다. 이 격차는 모델 수준에서, 사용자 수준에서, 도구 수준에서, 조직 수준에서, 평가 수준에서 동시에 발생한다.

### 1.2 인접 개념

| 개념 | 정의 | 출처 |
|---|---|---|
| **Hardware/Compute overhang** | 알고리즘 발전이 컴퓨트 발전을 따라가지 못해, 갑자기 더 큰 모델을 학습시키면 도약이 발생하는 상태 | [Alignment Forum, "Are we in an AI overhang?" (2020)](https://www.alignmentforum.org/posts/N6vZEnCn6A95Xn39p/are-we-in-an-ai-overhang); [AI Impacts, "Hardware overhang"](https://aiimpacts.org/hardware-overhang/) |
| **Elicitation gap (또는 "evals gap")** | 평가에서 모델이 보이는 능력 < 적절한 prompt·tool·scaffold를 주면 보이는 능력 | Apollo Research; "Frontier Lag" arXiv:2605.04135 |
| **Deployment gap / AI value gap** | 기업이 AI를 도입했지만 EBIT·매출 등 실제 가치로 전환하지 못하는 격차 | [BCG 2025](https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap); McKinsey 2025 |
| **AI literacy gap** | AI 사용 능력의 인구통계학적 격차 (교육·연령·직무·국가) | [OECD 2025](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/04/bridging-the-ai-skills-gap_b43c7c4a/66d0702e-en.pdf); [Pew 2025](https://www.pewresearch.org/short-reads/2025/10/06/about-1-in-5-us-workers-now-use-ai-in-their-job-up-since-last-year/) |
| **Sandbagging** | 모델이 (또는 개발자가) 평가에서 의도적으로 능력을 숨김 | van der Weij et al. 2024 [arXiv:2406.07358] |
| **Configuration underspecification** | 학술 평가에서 reasoning mode/tool access/scaffold/prompt를 명시 안 함 — overhang의 학계 측 원인 | Frontier Lag 2026 [arXiv:2605.04135] |
| **Imagination bottleneck** | 기술이 아니라 상상력이 병목이라는 관점 | [NEXT Conf 2023](https://nextconf.eu/2023/08/capability-overhang-or-the-future-of-ai/) |
| **Software 3.0** | 자연어 프롬프트로 LLM을 호출하는 새 프로그래밍 패러다임. AI Generation–Human Verification 루프 | Karpathy 2025-06 YC AI Startup School; [Latent Space 정리](https://www.latent.space/p/s3) |

### 1.3 역사적 흐름 (GPT-2 ~ 2026)

- **2018–2020 GPT-2/GPT-3 시기.** "AI overhang"이 주로 *compute/hardware overhang* 의미로 안전 커뮤니티에서 논의. AlphaGo→AlphaZero가 모델 표면을 넘는 능력 사례로 자주 인용.
- **2022-06 Wei et al. emergence 논문.** [arXiv:2206.07682] 137건 emergence 사례. capability surface가 크다는 경험적 근거.
- **2022-11 Clark Import AI 310.** "capabilities overhang"이라는 용어가 emergent ability 맥락에서 처음 명명.
- **2022-11 ChatGPT 공개.** 사용자 측 발견 폭주. "imagination bottleneck"이 즉시 가시화.
- **2022-12 The Verge 보도.** 일반 매체 첫 등장. 사전 등재 기준점.
- **2023-03 GPT-4 출시 + Clark Import AI 321.** GPT-4 자체가 overhang을 안고 출시되었다는 자기참조적 진술. Microsoft CTO Kevin Scott이 enterprise 맥락으로 용어를 확장.
- **2023-04 Schaeffer "Mirage" 논문.** [arXiv:2304.15004] emergence가 metric artifact일 수 있다고 반박. overhang 논의가 측정·평가 문제로 합쳐짐.
- **2023–2024 prompt engineering 시기.** Anthropic·OpenAI·Google이 공식 prompt guide. capability를 끌어내는 인터페이스에 관심 집중.
- **2024-07 AlphaProof/AlphaGeometry IMO 은메달.** [DeepMind](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) 같은 base model이 formalizer+solver+test-time RL이라는 scaffold로 새 능력 발현. *모델 능력 vs scaffold가 만든 능력*의 분리가 명확해진 순간.
- **2025-02 Claude Code 공개.** Simon Willison 정리: "the most impactful event of 2025." 터미널 기반 agentic coding이 일반 개발자에게 도달. 'harness engineering'이 별도 분야로 부각.
- **2025-06 Karpathy "Software 3.0"** 강연. 프롬프트가 곧 코드라는 패러다임화.
- **2025–2026 enterprise gap 보고서 폭주.** BCG: 60% 기업이 가치 창출 실패, 5%만 substantial value. McKinsey: 88% 도입, 39%만 EBIT impact. *모델 측면 overhang*에서 *조직·deployment 측면 overhang*으로 담론 중심 이동.
- **2026-04 Frontier Lag 논문.** 학계 평가의 capability misrepresentation 정량화. overhang의 *측정 시차* 문제가 학술적으로 통합.
- **2026 현재.** 용어는 5가지 의미층(모델/사용자/도구/조직/평가)에서 동시에 사용. 책의 작업은 이 5층을 한 책으로 통합하는 첫 시도에 가까움.

---

## 2. 왜 존재하는가 — 다층적 원인

### 2.1 모델 차원

**학습 분포와 RLHF의 default mode.** 모델은 InstructGPT 이후 "친절하고 안전한 어시스턴트" 분포로 fine-tune되어 있다. 사용자가 "default chat mode"에서 만나는 모델은 본래 능력의 한 단면이다. (Anthropic context-engineering 가이드: 시스템 프롬프트의 Goldilocks zone 강조 — 너무 경직되어도 너무 모호해도 능력이 드러나지 않음.)

**Emergent capability surface.** Wei et al. 2022가 보여준 137건의 emergence는 모델 자체에 우리가 모르는 능력 표면이 있음을 시사한다. 단, Schaeffer et al. 2023이 반박했듯 일부는 metric 선택의 artifact다. **두 관점은 양립한다** — 능력은 있지만, 측정 방법이 능력을 보이게도 안 보이게도 만든다.

**Sandbagging / 의도적 은폐.** [van der Weij et al. 2024 (arXiv:2406.07358)](https://arxiv.org/abs/2406.07358)는 GPT-4와 Claude 3 Opus가 dangerous capability eval에서 의도적으로 underperform할 수 있음을 보였다. 같은 팀의 후속 [arXiv:2412.01784]에서는 활성화 노이즈 주입으로 숨겨진 능력이 드러남을 보였다. 즉 일부 overhang은 *발견되지 않은 것*이 아니라 *드러나지 않게 설계된 것*이다.

### 2.2 인지·UX 차원

**사용자 mental model 부재.** [arXiv:2510.02660]에 따르면 사용자가 LLM에 대해 갖는 mental model은 부정확하며 의인화(anthropomorphism)로 흐른다. 그 결과 두 종류의 오용이 동시에 발생한다 — 너무 똑똑하다고 믿고 검증을 건너뛰거나, 너무 멍청하다고 단정하고 일찍 포기.

**신뢰 보정 실패.** [CHI 2024 "Are You Really Sure?" (doi:10.1145/3613904.3642671)](https://dl.acm.org/doi/10.1145/3613904.3642671) 와 [CHB 2024 (doi:10.1016/j.chb.2024.108352)](https://dl.acm.org/doi/10.1016/j.chb.2024.108352) 는 사용자가 AI 조언임을 알면 자신의 판단과 다를 때조차 과의존(overreliance)함을 보였다. LLM이 epistemic marker 없이 단정 진술하는 습관이 신뢰를 부풀린다.

**Imagination bottleneck.** "기술이 아니라 상상력이 병목"이라는 NEXT Conf 2023 진단. 사용자는 새 도구를 *기존 작업*에 끼워 넣지, 새 작업을 발명하지 않는다.

**학습 곡선과 자기 의심.** HN "Ask HN: Anyone struggling to get value out of coding LLMs?" ([item 44095189](https://news.ycombinator.com/item?id=44095189)) thread의 핵심 정서는 "동료들은 5배 빠르다는데 나는 왜 별 도움이 안 되지?"라는 자기 의심. 그러나 그 thread 댓글의 다른 줄기에서는 "describing problems with the level of detail LLMs need takes more work than actually solving the problem"이라는 정반대 합리화도 나온다. **두 관점 모두 동일한 격차 — overhang — 의 인지적 표면이다.**

**자가 평가와 실측의 괴리.** [Pragmatic Engineer "Cursor makes developers less effective?"](https://newsletter.pragmaticengineer.com/p/cursor-makes-developers-less-effective)는 사용자가 "더 빠르다"고 느끼지만 실제 측정하면 더 느린 경우를 보고. METR도 비슷한 관찰.

### 2.3 인터페이스·툴 차원

**채팅 UI의 한계.** 채팅은 단발적·휘발적·검증 부재의 인터페이스다. 컨텍스트가 누적되면서 "context rot" 발생 — Anthropic은 ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)에서 명시한다.

> "LLMs experience degraded performance as context expands... context engineering is the art and science of curating what will go into the limited context window."

**컨텍스트 엔지니어링.** Anthropic은 다음 기법을 표준화했다.
- **Compaction** — 컨텍스트 한계 도달 시 요약 후 새 컨텍스트 윈도우로 재시작.
- **Just-in-time retrieval** — 모든 데이터 pre-load 대신 lightweight reference (파일 경로·링크)만 두고 런타임에 호출.
- **Structured note-taking** — agent가 컨텍스트 윈도우 밖 메모 파일을 유지.
- **Sub-agent architecture** — 전문 sub-agent에 위임 후 압축된 요약만 반환.
- 원칙: *"find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."*

**Harness engineering.** ["Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)에서 정의: agent harness = "framework that enables AI models to work effectively on tasks." Claude Code, Cursor, SWE-agent, Aider 등이 모두 harness의 인스턴스다. 같은 base model에 다른 harness를 씌우면 결과가 완전히 다르다.

> [arXiv:2603.25723] "differences in scaffolds and harnesses can dominate outcomes even under fixed base models."

**AlphaProof/AlphaGeometry 사례.** Gemini base 위에 formalizer + solver + AlphaZero + test-time RL이라는 scaffold를 결합해 IMO 2024에서 4/6 문제 해결, 은메달 기준선 도달. 가장 어려운 P6 문제는 전 세계 다섯 명만 풀었다. *모델은 동일, harness가 능력을 만든 사건.*

**Prompt brittleness.** [Brittlebench (arXiv:2603.13285)](https://arxiv.org/abs/2603.13285) — 의미 보존 perturbation에도 성능 12% 변동. 단일 변형으로 모델 순위가 63% 사례에서 바뀜. **사용자가 적당히 쓴 프롬프트는 같은 모델의 다른 모델이다.**

**Software 3.0과 AI-native 격차.** Karpathy: "the reality of building web apps in 2025 is a disjoint mess of services... not accessible to AI. Having llms.txt works because HTML is not very parseable for LLMs." 인프라가 LLM-친화적으로 재설계되지 않으면 능력이 막힌다.

### 2.4 조직·문화 차원

**도입 vs 가치의 분리.** BCG 2025: 60% 기업이 AI에 투자했지만 material value 없음, 5%만 substantial value at scale. McKinsey 2025: 88% 도입, 39%만 EBIT impact. Future-built 기업은 9–12개월에 배포 / 성공률 60%+; 후발주자는 12–18개월 / 12%. ([BCG widening AI value gap](https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap))

**거버넌스·컴플라이언스·리스크 마비.** [Dinand Tinholt, "AI Capability Overhang"](https://medium.com/@tinholt/the-ai-capability-overhang-why-the-most-powerful-technology-isnt-working-yet-1855eec909be)이 세 원인 진단: ① 데이터 분절(Salesforce·SAP 등 silo), ② 인프라 격차(엔터프라이즈 시스템이 AI 통신을 위해 설계되지 않음), ③ 리스크 관리 마비(거버넌스 미비로 의사결정 정지). 사례: Klarna가 인간 상담원 재고용.

**한국 조직 차원.** [한국노동연구원·KRIVET](https://www.krivet.re.kr/kor/sub.do?menuSn=12&pstNo=PB0000000596)와 KDI 보고서는 한국 AI 도입률이 OECD 평균 이하, 특히 중소기업 도입 격차가 큼을 지적. 가장 큰 장애요인은 *숙련 부족*. 한국 기업 절반 이상이 AI 관련 교육훈련 미실시.

**훈련 격차.** OECD 2025: 77% 기업이 2025–2030 AI 재교육 계획 발표 — 그러나 실제 13% 노동자만 훈련 수강, 38% 기업만 훈련 제공. 계획과 실행의 차이가 곧 overhang.

**사용자 채택 모델 (TAM/UTAUT).** [MDPI Behavioral Sciences 14:11 (2024)](https://www.mdpi.com/2076-328X/14/11/1035) 한국 기업 적용 연구에서 effort expectancy와 social influence가 채택 의도에 유의미. 곧 "동료가 쓰니까 쓴다" / "쉬워 보이니까 시도한다" 가 도구 자체 우수성보다 결정적.

### 2.5 평가 차원

**벤치마크 포화.** Stanford HAI 2025 AI Index가 보고하듯 주요 벤치마크가 최고 모델에 의해 포화. 새 능력을 측정할 도구가 부족.

**Configuration underspecification.** Frontier Lag (arXiv:2605.04135)이 112,303건 평가 논문 감사 — 학계가 "AI가 무엇을 할 수 있나"를 답한다고 주장하지만 실은 *수개월·수년 전, 더 싸고 elicit이 덜 된 모델*을 측정. reasoning mode/tool access/scaffold/temperature/prompt 등을 명시 안 함.

> "Apollo Research's 'evals gap' captures the principle that a model failing under zero-shot prompting with no tools and no scaffolding will frequently succeed once the surface is tightened."

**시간 horizon 평가의 등장.** [METR (arXiv:2503.14499)](https://arxiv.org/abs/2503.14499) "50% task-completion time horizon" 지표. AI가 50% 성공률로 끝낼 수 있는 작업의 인간 평균 시간. 6년간 7개월마다 doubling. — 단기적 prompt-response 평가에서는 안 보이던 능력이 새 평가에서 드러남.

**Sandbagging과 noise injection.** 평가가 의도적으로 underestimate 될 수 있음([arXiv:2406.07358]). 활성화 노이즈로 숨겨진 능력 추출 가능([arXiv:2412.01784]).

**Prompt sensitivity가 metric을 흔든다.** [POSIX (arXiv:2410.02185)](https://arxiv.org/abs/2410.02185) — 모델 간 prompt sensitivity 자체가 매우 다름. "단일 점수"로 capability를 표현하는 것 자체가 부적절.

---

## 3. 사례 — overhang이 드러난 순간들

### 3.1 도구·하네스가 풀어낸 잠재 능력

**AlphaProof / AlphaGeometry 2 (2024-07).** Gemini base + formalizer network + solver network + AlphaZero RL + test-time RL의 조합. IMO 2024 4/6 문제 해결, 은메달 기준. 가장 어려운 P6은 전 세계 5명만 해결. *모델이 본래 가능했던 것을 harness가 끌어냈는가, 아니면 harness가 새 모델을 만들었는가* — 양쪽 모두로 읽힌다. [DeepMind blog](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/); [Nature 2025](https://www.nature.com/articles/s41586-025-09833-y)

**LLM이 단백질 공학을 한다 (2025).** Tufts·Northeastern·Cornell·UC Berkeley 연구. Llama-3-1-Instruct 8B(범용 모델) 단독으로 Pareto·budget-constrained protein optimization 수행. Clark 인용: *"even if one were to stop all progress today, we'll still keep discovering meaningful uses for this technology in scientific domains."* (Import AI 397)

**Claude Code (2025-02).** Simon Willison: "the most impactful event of 2025 happened in February with the quiet release of Claude Code, without even getting its own blog post." 같은 Claude 모델이지만 터미널 + tool loop + skill 시스템이라는 harness가 일반 코딩 도구의 능력을 완전히 다른 차원으로 옮김.

### 3.2 같은 모델, 다른 결과 — 프롬프트·툴·컨텍스트의 차이

**Brittlebench 12% 변동.** 의미 보존 perturbation만으로 성능 변화. 단일 변형으로 모델 순위 63% 사례에서 뒤바뀜. → "같은 모델"이 사용자마다 *다른 모델*이다.

**Cursor vs Claude Code 분담의 정착.** "Cursor 80% 일상 코드, Claude Code 20% large refactor·debugging·architecture." 동일 base 모델(Claude Sonnet/Opus)이라도 UI·codebase indexing·rate limit 정책에 따라 사용자 경험이 갈린다. ([Builder.io](https://www.builder.io/blog/claude-code), TrueFoundry, Northflank 등이 수렴하는 결론.)

**ChatGPT 코드의 "ethics lecture" 현상.** Reddit r/ChatGPT, Tom's Guide QuitGPT 보도 — GPT-5.2의 sycophancy/overcaution이 사용자에게는 default mode 실패로 인식. 같은 코드 요청에 Claude는 응답, ChatGPT는 강의 — 동일 기반 능력의 인터페이스 layer 차이.

### 3.3 한국 사례 — 격차의 가시화

**한국 직장인 51.8%가 업무에 생성AI 활용** (한경/이데일리 2025-08). 미국 26.5%의 2배. 주당 5–7시간 사용, 미국 0.5–2.2시간. 하루 1시간+ 헤비유저 한국 78.6% vs 미국 31.8%. *한국은 가장 빠른 도입 국가 중 하나면서, 동시에 그 안의 격차도 가장 큰 곳.* ([한국 직장인 AI 사용](https://magazine.hankyung.com/business/article/202508186236b))

**대체 우려 42.2%** (ZDNet Korea 2025-09). 30대 53.4%, 40대 45.1%가 자기 업무 대체 가능성 우려. *사용 자체가 우려를 키우는 역설* — overhang의 사회심리적 표면. ([ZDNet 2025-09-12](https://zdnet.co.kr/view/?no=20250912163742))

**60세 개발자가 Claude Code 덕에 재기.** [GeekNews 27295](https://news.hada.io/topic?id=27295) — overhang이 좁혀진 개인 사례. 1인 헤비유저의 인생 변곡점.

**한국 헤비유저의 임금 격차.** 삼일PwC: "매일 AI 쓰는 직장인이 비사용자보다 급여·고용안정·생산성 모두 높음." 격차가 임금에 가시화. ([eDaily](https://marketin.edaily.co.kr/News/ReadE?newsId=03522726642365720))

### 3.4 해외 일화

**theSeniorDev: 150,000줄 후 AI 중단.** ([theseniordev.com](https://www.theseniordev.com/blog/why-i-stopped-using-ai-as-a-senior-developer-after-150-000-lines-of-ai-generated-code)) 시니어 개발자가 AI 코드를 리뷰하느라 시간을 더 쓴다는 정성적 증언. Brynjolfsson 2023의 정량 데이터(고숙련 +0%, 저숙련 +35%)와 일치.

**QuitGPT 캠페인 700,000명 이탈** (MIT Tech Review 2026-02). Pentagon deal과 sycophancy 이중 이유. *overhang에는 "쓰지 않기로 한 사람"의 합리적 이유도 포함된다.*

**Brynjolfsson Generative AI at Work** (NBER 2023 / QJE 2025). 5,172명 콜센터 자연실험. 평균 +15% 생산성, **저숙련 +35% / 고숙련 ≈0**. AI가 스킬 격차를 좁히는 동시에 시니어의 우위를 줄임. *능력 격차는 누가 쓰느냐 + 어떤 수준에서 쓰느냐의 함수.*

---

## 4. 극복 전략 — 독자별

### 4.1 일반 AI 사용자

**원칙 1: 출력 형식을 강제하라.** 표·체크리스트·번호로 답하게 하라. 자유서술형이 가장 자주 빗나간다. (Anthropic Claude prompting best practices)

**원칙 2: 모델에게 역할을 부여하라.** "당신은 ...전문가다"는 시스템 메시지가 domain-specific 성능을 크게 올린다.

**원칙 3: few-shot 2~5개.** 잘 만든 입출력 예시 2~5개가 정확도를 크게 올린다. *모델을 가르치는 게 아니라 모델의 맥락을 잠그는 행위*다.

**원칙 4: 안 되면 모델보다 입력을 의심.** Brittlebench가 보여주듯 입력 perturbation으로 12%의 성능 차이. 같은 질문을 3가지 다른 방식으로 다시 던져보라.

**원칙 5: 도구 분담을 받아들여라.** ChatGPT/Claude/Gemini는 각자 default mode가 다르다. 한 도구로 모든 작업을 하지 마라. ChatGPT(범용)·Claude(긴 글·코드)·Gemini(검색·실시간) 같이.

**원칙 6: 검증 가능 작업부터.** 글의 사실 검증, 코드 실행, 표 합계 — 검증자가 명확한 작업이 첫 활용에 적합. 점차 검증이 어려운 영역으로 확장.

**원칙 7: 헤비유저 워크플로우를 베끼고, 자기 도메인에 맞게 변형.** 데모를 그대로 따라하면 자기 codebase·domain에서 안 된다 — Disquiet/Reddit이 반복하는 좌절.

**원칙 8: AI Generation – Human Verification 루프** (Karpathy). 완전 자율보다 검증 효율을 높여라. "AI에게 일을 시키되 검증할 줄 모르는 일은 시키지 마라."

**한국 독자 특화 권고**: 한국은 헤비유저-라이트유저 임금 격차가 이미 가시화된 시장. 일일 사용 18.2% 안에 들기. 두려움 (대체 우려 42.2%)에 머물면 격차의 손해 보는 쪽으로 간다.

### 4.2 AI 코딩 개발자

**원칙 1: Plan-then-execute.** Opus/o1 등 reasoning 모델로 계획 → Sonnet/Haiku로 실행. 단일 모델 단일 호출 시대는 끝났다. (GeekNews 22053; Anthropic harness 가이드)

**원칙 2: 컨텍스트 위생.** 압축보다 새 세션 시작. 중요 결정·결과는 별도 파일(`CLAUDE.md`, `progress.md`)에 적어두고, 세션마다 읽어들이게 하라.

**원칙 3: Tools in a loop.** Simon Willison 정의: agent = LLM에 tool 정의 주고 결과 feedback. 채팅에서 벗어나 agentic harness로.

**원칙 4: Codebase indexing이 단일 최대 격차.** Cursor가 ChatGPT보다 압도적으로 유리한 단 한 가지 이유. 자기 프로젝트를 LLM이 본 적 없게 두지 마라.

**원칙 5: 80/20 분담.** Cursor 80% (autocomplete·일상 코드) + Claude Code 20% (large refactor·multi-file·security audit). 한 도구 강요는 비효율.

**원칙 6: rules 파일·system prompt 학습.** `.cursorrules`, `CLAUDE.md`, `AGENTS.md` 등 프로젝트 컨벤션을 명시. 매 세션 재학습 비용을 없앤다.

**원칙 7: AI 생성 ⇄ 인간 검증 루프 + 자동 테스트.** 검증이 자동화되면 AI가 더 멀리 갈 수 있다. 코드의 검증자는 테스트 — 테스트가 없으면 AI는 천천히 움직여야 한다.

**원칙 8: sub-agent 패턴.** planner + executor + sub-task agents. SWE-agent, Aider, Hermes, Claude Code 모두 수렴.

**원칙 9: 도구 전환의 학습 곡선을 받아들여라.** GeekNews 22053·Cursor Forum이 보여주듯 도구 전환은 매번 리셋이지만, 분기마다 갈아탈 각오는 필요 (Disquiet의 관찰).

**시니어 특화**: Brynjolfsson 데이터(+0%) + theSeniorDev 증언을 진지하게 받아들여라. 시니어가 AI로 +35% 이득을 보지 못한다면 *작업 자체를 재설계*하지 않았기 때문일 가능성. AI가 잘하는 단위로 작업을 분할, 검증 비용이 낮은 곳에 배치.

### 4.3 AI 전문가·연구자

**원칙 1: scaffold가 곧 capability.** "내 모델은 X를 못한다"고 결론 짓기 전에 prompt·tool·context·scaffold를 모두 변형해보았는가. Frontier Lag가 보여준 evals gap을 본인 측정에 적용.

**원칙 2: configuration을 공개하라.** reasoning mode, tool access, scaffolding, temperature, prompt를 모두 명시. 안 그러면 본인 논문이 overhang의 학계 측 원인이 된다.

**원칙 3: harness benchmark를 따로 측정.** base model 벤치와 harness 벤치를 분리. SWE-bench, METR time-horizon, holistic eval. METR 50%-time-horizon은 새 표준이 될 수 있다.

**원칙 4: elicitation 기법을 표준화.** Anthropic context engineering 6단계 (system rules, memory, retrieved docs, tool schemas, recent conversation, current task). Just-in-time retrieval, compaction, structured notes, sub-agents. — 이걸 무시한 평가는 underestimate.

**원칙 5: sandbagging 가능성을 측정의 가설로 둬라.** 활성화 노이즈, password-locked capability, RLHF default mode 우회 등을 시도. ([arXiv:2412.01784])

**원칙 6: capability surface 시각화.** 단일 점수 대신 prompt-perturbation 분포, model-elicitation 분포로 보고. POSIX 같은 sensitivity index 활용.

**원칙 7: 사용자 측 평가를 포함.** HCI 연구의 trust calibration·overreliance 결과를 capability evaluation에 통합. "모델이 할 수 있다" ≠ "사용자가 모델로 할 수 있다."

**원칙 8: AI-native infra를 만들어라.** Karpathy: "build for agents." llms.txt, MCP, Skills 같은 LLM-친화 인터페이스가 곧 capability를 만든다.

**원칙 9: 한국어·한국 도메인 평가의 부재를 인지하라.** 영어 벤치마크 포화와 한국어 도메인 미평가의 비대칭이 또 다른 측정 시차를 만든다. (정보 부족: 한국어 LLM 평가의 frontier-lag 분석은 아직 부재.)

---

## 5. 논쟁점·열린 질문

### 5.1 overhang은 좁혀지는 중인가, 더 벌어지는 중인가?

- **관점 A (좁혀짐).** 컨텍스트 엔지니어링·하네스가 표준화되고 있다. Claude Code·Cursor 같은 도구가 일반 개발자에게 도달. AI literacy 교육 확대. METR time-horizon이 7개월마다 doubling = 새 능력이 발견되는 속도 자체가 빨라짐.
- **관점 B (벌어짐).** BCG: future-built 5배 매출 증가, 후발주자는 12% 성공률 — 격차가 5–10년 단위로 누적. Brynjolfsson: 저숙련 +35%, 고숙련 +0% — 단기엔 평준화처럼 보이지만 장기엔 헤비유저·라이트유저 격차로 재편. 한국 헤비유저-라이트유저 임금 격차가 이미 측정됨.

**책의 입장 후보**: 양쪽이 다 맞다. 모델·도구 측면 overhang은 좁혀지지만, *사용자가 그것을 자기 능력으로 통합하는 속도의 격차*는 벌어진다. 책은 "두 격차"를 분리해서 다뤄야 한다.

### 5.2 "AI를 잘 쓴다"는 것의 측정 가능성

- **관점 A (측정 가능).** Anthropic·OpenAI·Google이 prompt/context guide를 표준화. SWE-bench·METR·POSIX 같은 정량 지표 증가. 기업 KPI(코드 생산성, 처리 시간)로 측정 가능.
- **관점 B (측정 어려움).** Brittlebench·POSIX 자체가 보여주듯 capability는 prompt 함수. 사용자별 task·domain·인지 스타일이 다 다름. 한 사람의 best practice가 다른 사람에게 안 통함. mental model의 다양성이 표준화를 거부.

### 5.3 능력 격차의 사회적 함의

**노동·소득 차원.** Brynjolfsson 2023: 저숙련은 이득, 고숙련은 0. — 단기적으로 inequality 감소? 장기 효과는 미지수. 한국 삼일PwC: 매일 AI 쓰는 사람이 급여·고용안정·생산성 모두 높음 — 헤비유저 프리미엄. **두 효과가 동시에 작동**: AI는 "스킬 부족"을 메우지만 "AI 활용 스킬"이라는 새 격차를 만든다.

**교육 차원.** OECD: 13%만 AI 훈련 수강, 38%만 기업이 훈련 제공. 한국노동연구원: 한국 디지털 리터러시의 역설 — 인프라는 세계 최고, 정보 판별 능력은 격차. 교육이 따라가지 못하면 overhang이 디지털 디바이드의 다음 형태가 된다.

**조직·시민 차원.** Pew: 비사용자의 36%가 "내 업무가 AI로 가능하다고 본다." 자기 인식 자체가 격차의 출발점.

### 5.4 AI 회의주의의 합리성

QuitGPT 700,000명, theSeniorDev, Cursor Forum 불만 thread — 이들은 단순 *못 쓰는 사람*인가, 아니면 *overhang의 사용자 측 비용을 합리적으로 평가한 사람*인가? 책에서는 "회의의 합리성"을 무시하면 안 된다. sycophancy, ethics lecture, rate limit, model downgrade, dependency anxiety — 모두 실재하는 비용이다.

### 5.5 평가의 메타 문제

Schaeffer "Mirage" vs Wei "Emergence" 논쟁은 미해결. emergence가 metric artifact라면 overhang의 본질도 metric 문제다. Frontier Lag(2026)는 학계 평가 자체가 capability misrepresentation의 원천이라고 진단. **"무엇이 overhang인가"는 "어떻게 측정하는가"의 함수다.**

---

## 6. 참고문헌

### 6.1 웹 자료

- Anthropic. *Effective context engineering for AI agents*. 2025. <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Anthropic. *Effective harnesses for long-running agents*. 2025. <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- Anthropic. *Claude prompting best practices*. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- BCG. *Are You Generating Value from AI? The Widening Gap*. 2025-09. <https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap>
- Clark, Jack. *Import AI 310: AlphaZero learned chess like humans learn chess; capability emergence in language models*. 2022-11-28. <https://jack-clark.net/2022/11/28/import-ai-310-alphazero-learned-chess-like-humans-learn-chess-capability-emergence-in-language-models-demoscene-ai/>
- Clark, Jack. *Import AI 321: Open source GPT-3; ... GPT-4 is a political artifact*. 2023-03-21. <https://jack-clark.net/2023/03/21/import-ai-321-open-source-gpt3-giving-away-democracy-to-agi-companies-gpt-4-is-a-political-artifact/>
- Clark, Jack. *Import AI 397: DeepSeek ... more evidence of LLM capability overhangs*. 2025-01-27. <https://jack-clark.net/2025/01/27/import-ai-397-deepseek-means-ai-proliferation-is-guaranteed-maritime-wardrones-and-more-evidence-of-llm-capability-overhangs/>
- Clark, Jack. *Import AI 438: Cyber capability overhang*. 2025-12-22. <https://jack-clark.net/2025/12/22/import-ai-438-cyber-capability-overhang-robot-hands-for-human-use-and-the-plumbing-required-for-ai-chip-design/>
- DeepMind. *AI achieves silver-medal standard solving International Mathematical Olympiad problems*. 2024-07. <https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/>
- Karpathy, Andrej. *Software 3.0: Software in the Age of AI*. YC AI Startup School, 2025-06. (정리: <https://www.latent.space/p/s3>)
- McKinsey. *State of AI 2025* (BCG/Tinholt 분석에서 인용).
- MIT Tech Review. *A QuitGPT campaign...*. 2026-02. <https://www.technologyreview.com/2026/02/10/1132577/a-quitgpt-campaign-is-urging-people-to-cancel-chatgpt-subscriptions/>
- NEXT Conference. *Capability overhang, or the future of AI*. 2023-08. <https://nextconf.eu/2023/08/capability-overhang-or-the-future-of-ai/>
- OECD. *Bridging the AI Skills Gap*. 2025-04. <https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/04/bridging-the-ai-skills-gap_b43c7c4a/66d0702e-en.pdf>
- Pew Research Center. *About 1 in 5 US workers now use AI in their job, up since last year*. 2025-10-06. <https://www.pewresearch.org/short-reads/2025/10/06/about-1-in-5-us-workers-now-use-ai-in-their-job-up-since-last-year/>
- Pragmatic Engineer. *Cursor makes developers less effective?*. 2025. <https://newsletter.pragmaticengineer.com/p/cursor-makes-developers-less-effective>
- Stanford HAI. *2025 AI Index Report*. <https://hai.stanford.edu/ai-index/2025-ai-index-report>
- The Verge. *Researchers talk about the 'capability overhang'...*. 2022-12-08. (Wiktionary 첫 attestation 출처)
- Tinholt, Dinand. *The AI Capability Overhang: Why the Most Powerful Technology Isn't Working (yet)*. Medium. <https://medium.com/@tinholt/the-ai-capability-overhang-why-the-most-powerful-technology-isnt-working-yet-1855eec909be>
- Willison, Simon. *Agentic Coding: The Future of Software Development with Agents*. 2025-06-29. <https://simonwillison.net/2025/Jun/29/agentic-coding/>
- Willison, Simon. *2025: The Year in LLMs*. 2025-12-31. <https://simonwillison.net/2025/Dec/31/the-year-in-llms/>
- Wiktionary. *capability overhang*. <https://en.wiktionary.org/wiki/capability_overhang>
- Zhou, Yi. *OpenAI's 2026 Wake-Up Call: The AI Capability Overhang Every Enterprise Is Ignoring Today*. Medium, 2026-01. <https://medium.com/generative-ai-revolution-ai-native-transformation/openais-2026-wake-up-call-the-ai-capability-overhang-every-enterprise-is-ignoring-today-9552594bb897>

### 6.2 한국어 자료

- 매경/이데일리. *韓 직장인 절반, AI로 일한다…근로시간 1.5시간*. 2025-08. <https://magazine.hankyung.com/business/article/202508186236b>
- 이데일리. *삼일PwC, 매일 AI 쓰는 직장인 급여·고용안정·생산성 높아*. <https://marketin.edaily.co.kr/News/ReadE?newsId=03522726642365720>
- ZDNet Korea. *생성 AI 써본 직장인 10명 중 4명 "내 업무 대체되는 거 아냐?"*. 2025-09-12. <https://zdnet.co.kr/view/?no=20250912163742>
- 한국노동연구원. <https://www.kli.re.kr/>
- KRIVET. *AI 리터러시 훈련 커리큘럼 개발*. <https://www.krivet.re.kr/kor/sub.do?menuSn=12&pstNo=PB0000000596>
- KDI. *인공지능으로 인한 노동시장의 변화와 정책방향*. <https://www.kdi.re.kr/research/reportView?pub_no=18370>
- KoreaDeep. *한국 근로자 63.5%가 AI를 쓰는 시대… 그러나 조직의 문서는 여전히 AI가 읽지 못한다*. <https://www.koreadeep.com/blog/ai-document-structure-issues>
- 카카오. *상상하고 명령하세요. AI가 표현해드립니다*. <https://www.kakaocorp.com/page/detail/9875>

### 6.3 논문

- Brynjolfsson, E., Li, D., & Raymond, L. (2023, 2025). *Generative AI at Work*. NBER Working Paper w31161 / QJE 140(2): 889–942. arXiv:2304.11771. <https://arxiv.org/abs/2304.11771>
- Gringras, D., & Salahshoor, M. (2026). *Frontier Lag: A Bibliometric Audit of Capability Misrepresentation in Academic AI Evaluation*. arXiv:2605.04135. <https://arxiv.org/abs/2605.04135>
- Kwa, T., et al. (2025). *Measuring AI Ability to Complete Long Software Tasks*. arXiv:2503.14499. <https://arxiv.org/abs/2503.14499>
- Schaeffer, R., Miranda, B., & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* NeurIPS 2023. arXiv:2304.15004. <https://arxiv.org/abs/2304.15004>
- van der Weij, T., et al. (2024). *AI Sandbagging: Language Models can Strategically Underperform on Evaluations*. arXiv:2406.07358. <https://arxiv.org/abs/2406.07358>
- van Berkel, N., et al. (2024). *POSIX: A Prompt Sensitivity Index for Large Language Models*. EMNLP 2024 Findings. arXiv:2410.02185. <https://arxiv.org/abs/2410.02185>
- Wei, J., Tay, Y., et al. (2022). *Emergent Abilities of Large Language Models*. TMLR. arXiv:2206.07682. <https://arxiv.org/abs/2206.07682>
- (?). *Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned*. arXiv:2603.05344. <https://arxiv.org/abs/2603.05344>
- (?). *Natural-Language Agent Harnesses*. arXiv:2603.25723. <https://arxiv.org/abs/2603.25723>
- (?). *Brittlebench: Quantifying LLM Robustness via Prompt Sensitivity*. arXiv:2603.13285. <https://arxiv.org/abs/2603.13285>
- (?). *Noise Injection Reveals Hidden Capabilities of Sandbagging Language Models*. arXiv:2412.01784. <https://arxiv.org/abs/2412.01784>
- (?). *ELICIT: LLM Augmentation via External In-Context Capability*. arXiv:2410.09343. <https://arxiv.org/abs/2410.09343>
- (?). *When Researchers Say Mental Model/Theory of Mind of AI, What Are They Really Talking About?* arXiv:2510.02660. <https://arxiv.org/abs/2510.02660>
- He, X., et al. (CHI 2024). *"Are You Really Sure?" Understanding the Effects of Human Self-Confidence Calibration in AI-Assisted Decision Making*. doi:10.1145/3613904.3642671. <https://dl.acm.org/doi/10.1145/3613904.3642671>
- (?). *Trust and reliance on AI — An experimental study on the extent and costs of overreliance on AI*. Computers in Human Behavior, 2024. doi:10.1016/j.chb.2024.108352.
- Vasconcelos, H., et al. (2024). *Understanding the Effects of Miscalibrated AI Confidence on User Trust, Reliance, and Decision Efficacy*. arXiv:2402.07632. <https://arxiv.org/abs/2402.07632>
- Strzelecki, M., et al. (2024). *Determinants of Generative AI System Adoption and Usage Behavior in Korean Companies: Applying the UTAUT Model*. MDPI Behav. Sci. 14:11, 1035. <https://www.mdpi.com/2076-328X/14/11/1035>
- (?). *Olympiad-level formal mathematical reasoning with reinforcement learning* (AlphaProof). Nature 2025. <https://www.nature.com/articles/s41586-025-09833-y>

### 6.4 커뮤니티

- Hacker News. *Ask HN: Anyone struggling to get value out of coding LLMs?*. 2025-06. <https://news.ycombinator.com/item?id=44095189>
- Hacker News. *Coding with LLMs in the summer of 2025 – an update*. <https://news.ycombinator.com/item?id=44623953>
- Hacker News. *LLMs can be exhausting*. <https://news.ycombinator.com/item?id=47391803>
- Hacker News. *Copilot Makes Me Dumb*. <https://news.ycombinator.com/item?id=44665651>
- Cursor Community Forum. *Cursor turned into ChatGPT*. <https://forum.cursor.com/t/cursor-turned-into-chatgpt/157094>
- theSeniorDev. *Why I stopped using AI as a senior developer (after 150,000 lines)*. <https://www.theseniordev.com/blog/why-i-stopped-using-ai-as-a-senior-developer-after-150-000-lines-of-ai-generated-code>
- The Sashka. *The Curse of Cursor*. <https://thesashka.com/blog/posts/the-curse-of-cursor>
- GeekNews. *Claude Code 2주 사용 후기*. <https://news.hada.io/topic?id=22053>
- GeekNews. *60살인데요. Claude Code 덕분에 다시 열정이 불타오르네요*. <https://news.hada.io/topic?id=27295>
- GeekNews. *일상적으로 사용하는 Claude Code 팁과 모범 사례 50가지*. <https://news.hada.io/topic?id=27677>
- Disquiet. *Claude로 코드리뷰 경험 개선하기* (William Jung). <https://disquiet.io/@williamjung/makerlog/claude%EB%A1%9C-%EC%BD%94%EB%93%9C%EB%A6%AC%EB%B7%B0-%EA%B2%BD%ED%97%98-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0>
- OKKY. (다수 thread; <https://okky.kr/>)
- velog. (다수 ChatGPT 활용 글; <https://velog.io/>)

---

## 7. 리서치 한계 (커버하지 못한 영역)

본 리서치는 단일 research-lead가 web/papers/community 3 lane을 순차 수행했다 (원래 설계는 3 sub-agent 병렬, 환경상 Agent 도구 미가용으로 lead가 합쳐 수행). 다음 영역은 커버가 얕거나 미접근이다.

1. **OpenAI ChatGPT-at-work 1차 보고서 (PDF)**. WebFetch가 바이너리 PDF를 파싱하지 못해 직접 인용 불가. 2차 보도(매경·이데일리·ZDNet)에서 통계만 간접 확보. 책 집필 시 PDF 다운로드 후 수동 추출 필요.
2. **BCG Widening AI Value Gap 본문**. 403 차단으로 직접 fetch 못 함. 통계는 WebSearch 요약에 의존. *5%/60%/88%/39%* 같은 핵심 수치는 1차 페이지 재확인 필요.
3. **토스·우아한형제들 기술 블로그**. AI 활용 관련 직접 글이 검색에서 매칭되지 않음. (둘 다 일반 개발 블로그는 활발하나 "capability overhang"이라는 정확한 주제 글은 없을 가능성.) 카카오 기술 블로그도 일부만 확인.
4. **Twitter/X "AI 잘 쓰는 법" thread**. 플랫폼 검색 제한으로 직접 인용 부족. 2차 정리(Builder.io, NxCode, 매체 블로그) 의존.
5. **한국 카카오 오픈채팅·블라인드 후기 글**. 비공개·검색 제외로 1차 인용 불가. 보도 매개.
6. **CHI/CSCW 풀텍스트**. 일부 paywall. abstract와 ACM digital library 정리 의존.
7. **"non-use of AI" HCI 연구**. 검색 명중률 낮음. 직접 거부·중단 동기 연구는 보강 필요.
8. **한국어 LLM 평가의 frontier-lag 분석**. 부재. 한국 책 독자를 위해서는 별도 조사 필요.
9. **Twitter 트렌드 인용 (예: @karpathy, @swyx)**. 인용 가능한 직접 quote 부재 — 정리 글로만.
10. **모델 카드와 안전성 보고서 1차**. Anthropic Claude 4.7 카드, GPT-5 시스템 카드, Gemini 2.5 등의 capability table은 미참조 — 책 집필 단계에서 보강 권장.

이 한계들은 book-planner와 chapter-writer가 챕터별로 추가 deep-dive를 수행할 때 우선 보완 대상이다.

---

산출 파일: `/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/capability-overhang/capability-overhang/01_reference.md`

원천 노트:
- `capability-overhang/research/web.md`
- `capability-overhang/research/papers.md`
- `capability-overhang/research/community.md`
