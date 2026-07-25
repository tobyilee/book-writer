<!-- 검색 시점: 2026-07-25 기준 -->

# 논문 리서치: AI Agent 개발 — 원리·평가·안전성의 학술 근거

대상 독자는 LLM API(chat completion, tool use)는 써봤지만 에이전트를 직접 설계·배포·운영해본 적 없는 백엔드/풀스택 개발자·테크리드다. **학자가 아니라 실무자다.**
따라서 이 문서는 학술 계보 정리가 목적이 아니라, **"어떤 설계 결정이 논문으로 정당화되거나 반박되는가"**를 제공하는 것이 목적이다.

## 이 문서를 읽는 방법 (검증 규율)

- 모든 서지정보(제목·저자·arXiv ID·버전·리비전일)는 arXiv API **제목 검색**으로 해석했다. 기억한 ID로 조회하지 않았다 — 기억 ID는 "존재하는 다른 논문"을 반환해 그럴듯한 오인용을 만들기 때문이다.
- 수치는 **논문 초록 또는 본문에서 직접 확인한 것만** 적었다. 본문 확인한 수치는 `[본문 확인]`, 초록에서 확인한 수치는 `[초록 확인]`으로 표시했다.
- 학회·저널명은 arXiv 메타데이터(`journal_ref`/`comment`)에 명시된 경우만 적었다. 흔히 "ReAct는 ICLR 2023"처럼 인용되지만 메타에 없으면 `발표처 미확인`으로 남겼다. **fact-checker는 이 표시를 신뢰해도 된다** — 미확인은 "아마 맞지만 내가 확인하지 않았다"는 뜻이다.
- arXiv는 리비전마다 수치가 바뀐다. 그래서 각 항목에 v1 발행일과 **최신 리비전일**을 함께 적었다.

---

# 핵심 논쟁 지도

책의 뼈대가 될 6개 논쟁이다. 각 논쟁에서 **양쪽 진영에 실재하는 논문**을 배치했다. 챕터를 쓸 때 "논문에 따르면 X다"가 아니라 "이 논쟁은 아직 안 끝났고, 당신의 상황이 어느 쪽에 가까운지가 결정한다"로 써야 한다.

## 논쟁 1. 멀티에이전트 vs 단일 에이전트

| 진영 | 대표 논문 | 핵심 근거 |
|---|---|---|
| 멀티에이전트가 이득이다 | Du et al., *Improving Factuality and Reasoning in Language Models through Multiagent Debate* (arXiv:2305.14325) | 여러 인스턴스가 토론하면 수학·전략 추론과 사실성이 향상 |
| 이득이 미미하고 실패 모드가 구조적이다 | Cemri et al., *Why Do Multi-Agent LLM Systems Fail?* (arXiv:2503.13657v3, MAST) | "성능 향상이 종종 미미하다". 7개 프레임워크 1600+ 트레이스에서 14개 실패 모드를 3범주(시스템 설계·에이전트 간 정렬·태스크 검증)로 분류 |

**실무 결론 초안:** 멀티에이전트를 쓸 이유는 "정확도 향상"이 아니라 "관심사 분리·컨텍스트 격리"다. 정확도를 근거로 삼으면 MAST가 반박한다.

## 논쟁 2. RAG vs 롱 컨텍스트

| 진영 | 대표 논문 | 핵심 근거 |
|---|---|---|
| 롱 컨텍스트가 검색을 대체한다 | Lee et al., *Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More?* (arXiv:2406.13121, LOFT) | LCLM이 명시적 학습 없이도 SOTA 검색·RAG 시스템에 "맞먹는" 능력 |
| 검색이 여전히 이긴다 (비용까지 보면 압도적) | Xu, Ping et al., *Retrieval meets Long Context LLMs* (arXiv:2310.03025v2, ICLR 2024) | 4K 컨텍스트 + 단순 검색이 16K 파인튜닝 모델과 **비슷한 성능, 훨씬 적은 계산** |
| 롱 컨텍스트는 오히려 품질을 떨어뜨린다 | Yu, Xu, Akkiraju, *In Defense of RAG in the Era of Long-Context LLMs* (arXiv:2409.01666, OP-RAG) | 검색 청크 수를 늘리면 품질이 올랐다가 **떨어지는 역U자 곡선** — 스위트 스팟 존재 |
| 롱 컨텍스트 자체가 위치에 취약하다 | Liu et al., *Lost in the Middle* (arXiv:2307.03172v3, TACL 2023) | 관련 정보가 중간에 있으면 성능이 유의하게 하락. **명시적 롱 컨텍스트 모델도 마찬가지** |

**실무 결론 초안:** 이 논쟁은 "누가 이기나"가 아니라 "무엇을 최적화하나"의 문제다. 정확도만 보면 접전, 비용·지연을 넣으면 검색 쪽으로 기운다. 그리고 컨텍스트에 다 넣는 전략은 Lost-in-the-Middle 세금을 낸다.

## 논쟁 3. self-correction이 작동하는가

| 진영 | 대표 논문 | 핵심 근거 |
|---|---|---|
| 작동한다 | Madaan et al., *Self-Refine* (arXiv:2303.17651v2) / Shinn et al., *Reflexion* (arXiv:2303.11366v4) | Self-Refine: 7개 태스크 평균 **~20% 절대 향상**. Reflexion: HumanEval **pass@1 91%** (GPT-4 80% 대비) |
| 추론에서는 작동하지 않는다 | Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet* (arXiv:2310.01798v2, ICLR 2024) | 외부 피드백 없는 **내재적(intrinsic) self-correction**은 추론에서 실패하고 **때로는 성능이 오히려 하락** |

**실무 결론 초안 (이 책에서 가장 실용적인 한 줄):** 두 진영은 실제로 모순이 아니다. Reflexion은 **외부 환경 피드백**(컴파일러·테스트·게임 결과)이 있고, Huang et al.이 반박한 건 **피드백 없는 자기 성찰**이다. 그래서 설계 규칙은 "리플렉션 루프를 넣어라"가 아니라 **"검증기(테스트·타입체커·스키마 검증)를 먼저 붙여라. 그것 없는 리플렉션은 토큰 낭비이거나 후퇴다."**

## 논쟁 4. 에이전트 벤치마크가 실무를 예측하는가

| 진영 | 대표 논문 | 핵심 근거 |
|---|---|---|
| 벤치마크가 진보를 측정한다 (원논문 측) | Jimenez et al., *SWE-bench* (arXiv:2310.06770v3, ICLR 2024) / Mialon et al., *GAIA* (arXiv:2311.12983) / Zhou et al., *WebArena* (arXiv:2307.13854v4) | 실제 GitHub 이슈·실제 웹사이트·실행 기반 채점으로 현실성 확보 |
| 예측하지 못한다 — 데이터 품질 결함 | Aleithan et al., *SWE-Bench+* (arXiv:2410.06992v2) | 성공 패치의 **32.67%가 해답 유출(solution leakage)**, **31.08%가 약한 테스트**. 걸러내면 SWE-Agent+GPT-4 해결률 **12.47% → 3.97%** |
| 예측하지 못한다 — 평가 설계 결함 | Zhu, Jin et al., *Establishing Best Practices for Building Rigorous Agentic Benchmarks* (arXiv:2507.02825v5, ABC) | 태스크 설정·보상 설계 결함이 성능을 **상대적으로 최대 100%** 과대/과소 평가. "SWE-bench Verified는 테스트 케이스가 불충분하고, TAU-bench는 빈 응답을 성공으로 계산한다" |
| 예측하지 못한다 — 비용·홀드아웃·재현성 결함 | Kapoor, Stroebl et al., *AI Agents That Matter* (arXiv:2407.01502) | 정확도만 보는 좁은 초점 → SOTA 에이전트가 "불필요하게 복잡하고 비싸다". 홀드아웃 세트 부재로 벤치마크 과적합 |
| 신뢰성은 아예 다른 축이다 | Yao, Shinn et al., *τ-bench* (arXiv:2406.12045) | gpt-4o가 태스크 **50% 미만** 성공, 그리고 **pass^8이 retail에서 25% 미만** — 평균 성공률과 일관성은 별개 |

**실무 결론 초안:** 리더보드 숫자를 그대로 자기 시스템의 기대치로 옮기면 안 된다. 그리고 **pass@k(한 번이라도 성공)와 pass^k(k번 모두 성공)를 구분**해야 한다 — 프로덕션이 요구하는 건 후자다.

## 논쟁 5. 프롬프트 인젝션은 원리적으로 막을 수 있는가

| 진영 | 대표 논문 | 핵심 근거 |
|---|---|---|
| 효과적 완화가 없다 (문제 제기 측) | Greshake et al., *Not what you've signed up for* (arXiv:2302.12173v2) | LLM 통합 앱이 **데이터와 명령의 경계를 흐린다**. "이런 신흥 위협에 대한 효과적 완화가 현재 부재하다" |
| 모델을 고치는 방식으로는 안 된다 (실증) | Debenedetti et al., *AgentDojo* (arXiv:2406.13352v3) | 기존 인젝션 공격이 "일부 보안 속성은 깨고 전부는 아니다". **더 유능한 모델이 오히려 공격하기 쉬운 역스케일링 경향** |
| 시스템 설계로 막을 수 있다 | Debenedetti et al., *Defeating Prompt Injections by Design* (arXiv:2503.18813v2, CaMeL) | 제어 흐름/데이터 흐름을 분리해 **AgentDojo 태스크의 77%를 "증명 가능한 보안"으로 해결** (무방어 84% 대비) |
| 설계 패턴화 가능하다 (단, 유틸리티 대가) | Beurer-Kellner et al., *Design Patterns for Securing LLM Agents against Prompt Injections* (arXiv:2506.08837v3) | 인젝션에 "증명 가능한 저항"을 갖는 설계 패턴 집합 + **유틸리티/보안 트레이드오프 명시** |

**실무 결론 초안:** 이 논쟁의 정답은 "프롬프트로 막을 수 있나 → 아니다 / 아키텍처로 막을 수 있나 → 상당히 가능하다, 단 에이전트의 자유도를 깎는 대가로"다. CaMeL의 77% vs 84%가 그 대가의 크기다.

## 논쟁 6. LLM-as-judge를 신뢰할 수 있는가

| 진영 | 대표 논문 | 핵심 근거 |
|---|---|---|
| 신뢰할 만하다 | Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (arXiv:2306.05685v4, NeurIPS 2023 D&B) | GPT-4 판정이 인간 선호와 **80% 초과 일치** — 인간끼리의 일치도와 같은 수준 |
| 순서만 바꿔도 결과가 뒤집힌다 | Wang et al., *Large Language Models are not Fair Evaluators* (arXiv:2305.17926v2) | 응답 등장 순서를 바꾸면 순위를 "해킹"할 수 있음. **ChatGPT를 평가자로 두고 Vicuna-13B가 80개 질의 중 66개에서 승리**하게 만들 수 있었다 |
| 자기 출력을 편애한다 | Panickssery, Bowman, Feng, *LLM Evaluators Recognize and Favor Their Own Generations* (arXiv:2404.13076) | self-recognition 능력과 self-preference 편향 강도 사이 **선형 상관**, 통제 실험으로 인과 주장 |
| 설계하면 쓸 수 있다 | Gu et al., *A Survey on LLM-as-a-Judge* (arXiv:2411.15594v6) | 신뢰성 확보 전략(일관성 개선·편향 완화)과 신뢰성 자체를 평가하는 방법론 정리 |

**실무 결론 초안:** MT-Bench 논문 자체가 position·verbosity·self-enhancement 편향을 인정하고 있다는 게 핵심이다. "judge 쓰지 마라"가 아니라 **"순서 무작위화/양방향 집계 없는 judge 점수는 보고하지 마라"**가 실무 규칙이다.

---

# 축 1. 에이전트 루프의 학술 계보

## ReAct: Synergizing Reasoning and Acting in Language Models
- 저자·연도: Shunyu Yao; Jeffrey Zhao; Dian Yu; Nan Du; Izhak Shafran; Karthik Narasimhan; Yuan Cao (2022)
- 출처: arXiv:2210.03629v3 / 발표처 미확인 (arXiv 메타에 학회 명시 없음)
- URL: https://arxiv.org/abs/2210.03629
- 발행·최종 리비전일: v1 2022-10-06 / v3 2023-03-10
- 축 태그: [축 1]
- 한 줄 요지: 추론(reasoning) 트레이스와 행동(acting)을 인터리빙해 서로를 보정하게 만드는 프롬프팅 패러다임.
- 실무자에게 의미하는 것: 오늘 당신이 쓰는 거의 모든 에이전트 루프(think → tool call → observe → think)의 조상이다. 중요한 함의는 **"생각"이 장식이 아니라 도구 호출의 오류를 잡는 채널이라는 점** — 그래서 tool 결과를 그냥 다음 프롬프트에 붙이지 말고 모델이 관찰을 해석하는 단계를 남겨야 한다. 반대로 이 패턴은 매 스텝마다 전체 히스토리를 재전송하므로 토큰 비용이 스텝 수에 대해 2차적으로 늘어난다 — ReWOO(아래)가 그 지점을 공격한다.
- 인용 가능한 구절·수치: 초록에 벤치마크 수치가 요약되어 있지 않아, 이 항목에서는 수치를 인용하지 않는다. 계보·개념 인용용으로만 쓸 것.
- 한계·반박: 스텝별 재전송 비용 → ReWOO(arXiv:2305.18323). 그리고 "생각을 시키면 좋아진다"는 일반 통념은 To CoT or not to CoT(arXiv:2409.12183)가 태스크 종류별로 제한한다.

## Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- 저자·연도: Jason Wei; Xuezhi Wang; Dale Schuurmans; Maarten Bosma; Brian Ichter; Fei Xia; Ed Chi; Quoc Le 외 1인 (2022)
- 출처: arXiv:2201.11903v6 / 발표처 미확인 (arXiv 메타에 학회 명시 없음)
- URL: https://arxiv.org/abs/2201.11903
- 발행·최종 리비전일: v1 2022-01-28 / v6 2023-01-10
- 축 태그: [축 1]
- 한 줄 요지: 중간 추론 단계를 예시로 넣으면 복잡 추론 성능이 크게 오르고, 이 능력은 충분히 큰 모델에서 창발한다.
- 실무자에게 의미하는 것: 에이전트 프롬프트에 "단계별로 생각하라"를 넣는 관행의 뿌리다. 하지만 **원논문의 주장 범위가 산술·상식·기호 추론이라는 점**을 기억해야 한다 — 이후 연구가 이 범위를 실제로 좁혔다.
- 인용 가능한 구절·수치 [초록 확인]: "prompting a 540B-parameter language model with just eight chain of thought exemplars achieves state of the art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier."
- 한계·반박: To CoT or not to CoT (arXiv:2409.12183v3) — CoT 이득이 수학·논리에 집중되고 다른 태스크에서는 훨씬 작다.

## To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning
- 저자·연도: Zayne Sprague; Fangcong Yin; Juan Diego Rodriguez; Dongwei Jiang; Manya Wadhwa; Prasann Singhal; Xinyu Zhao; Xi Ye 외 2인 (2024)
- 출처: arXiv:2409.12183v3 / ICLR 2025 (arXiv comment 명시)
- URL: https://arxiv.org/abs/2409.12183
- 발행·최종 리비전일: v1 2024-09-18 / v3 2025-05-07
- 축 태그: [축 1]
- 한 줄 요지: CoT 100편 이상 메타분석 + 직접 실험 결과, CoT의 이득은 주로 수학·논리 태스크에 한정된다.
- 실무자에게 의미하는 것: **CoT를 전역 기본값으로 켜두는 것은 비용 낭비일 수 있다.** 이 논문의 가장 실용적인 발견은 MMLU에서 등호(=)가 등장하지 않는 문항이면 CoT 없이 직접 답해도 정확도가 거의 같다는 것이다. 즉 "추론 토큰을 태울 가치가 있는 요청"을 라우팅으로 골라내는 설계가 정당화된다. 그리고 기호 실행이 필요한 경우엔 CoT보다 **도구(심볼릭 솔버)를 붙이는 게 낫다**는 것도 이 논문이 지지한다.
- 인용 가능한 구절·수치 [초록 확인]: "a quantitative meta-analysis covering over 100 papers using CoT and ran our own evaluations of 20 datasets across 14 models" / "On MMLU, directly generating the answer without CoT leads to almost identical accuracy as CoT unless the question or model's response contains an equals sign" / "Much of CoT's gain comes from improving symbolic execution, but it underperforms relative to using a symbolic solver."
- 한계·반박: 원조 CoT(arXiv:2201.11903). 또한 이 논문은 프롬프트 기반 CoT를 다루므로, 학습된 추론 모델(reasoning model)에 그대로 일반화하면 안 된다.

## Reflexion: Language Agents with Verbal Reinforcement Learning
- 저자·연도: Noah Shinn; Federico Cassano; Edward Berman; Ashwin Gopinath; Karthik Narasimhan; Shunyu Yao (2023)
- 출처: arXiv:2303.11366v4 / 발표처 미확인
- URL: https://arxiv.org/abs/2303.11366
- 발행·최종 리비전일: v1 2023-03-20 / v4 2023-10-10 (comment: "v4 contains a few additional experiments")
- 축 태그: [축 1]
- 한 줄 요지: 가중치를 갱신하지 않고 **언어적 피드백**을 에피소딕 메모리에 축적해 다음 시도를 개선한다.
- 실무자에게 의미하는 것: 재시도 루프를 "그냥 다시 호출"이 아니라 **"실패 원인을 텍스트로 요약해 다음 시도의 컨텍스트에 넣기"**로 설계하라는 근거. 파인튜닝 없이 배포된 시스템에서 적용 가능하다는 게 핵심 매력이다. 단, 다음 항목(Huang et al.)과 함께 읽어야 한다 — Reflexion의 피드백 원천에는 **외부 환경 신호(컴파일러·테스트)가 포함**된다.
- 인용 가능한 구절·수치 [초록 확인]: "Reflexion achieves a 91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%."
- 한계·반박: Huang et al. (arXiv:2310.01798v2) — 외부 피드백 없는 자기 교정은 추론에서 실패.

## Self-Refine: Iterative Refinement with Self-Feedback
- 저자·연도: Aman Madaan; Niket Tandon; Prakhar Gupta; Skyler Hallinan; Luyu Gao; Sarah Wiegreffe; Uri Alon; Nouha Dziri 외 8인 (2023)
- 출처: arXiv:2303.17651v2 / 발표처 미확인
- URL: https://arxiv.org/abs/2303.17651
- 발행·최종 리비전일: v1 2023-03-30 / v2 2023-05-25
- 축 태그: [축 1]
- 한 줄 요지: 같은 LLM 하나가 생성자·피드백 제공자·수정자를 모두 맡아 반복 개선한다. 추가 학습 데이터 없음.
- 실무자에게 의미하는 것: 구현 비용이 거의 없는 품질 개선 레버(프롬프트 3개면 끝). 다만 **비용이 호출 횟수에 선형으로 붙는다** — 개선폭 대비 호출 예산을 재보는 게 실무 판단이다.
- 인용 가능한 구절·수치 [초록 확인]: "We evaluate Self-Refine across 7 diverse tasks ... improving by ~20% absolute on average in task performance."
- 한계·반박: Huang et al. (arXiv:2310.01798v2)이 정면 반박 대상으로 삼는 계열이다. 태스크 종류(생성 품질 vs 추론 정답)에 따라 결과가 갈린다는 점이 이 논쟁의 핵심.

## Large Language Models Cannot Self-Correct Reasoning Yet
- 저자·연도: Jie Huang; Xinyun Chen; Swaroop Mishra; Huaixiu Steven Zheng; Adams Wei Yu; Xinying Song; Denny Zhou (2023)
- 출처: arXiv:2310.01798v2 / ICLR 2024 (arXiv comment 명시)
- URL: https://arxiv.org/abs/2310.01798
- 발행·최종 리비전일: v1 2023-10-03 / v2 2024-03-14
- 축 태그: [축 1]
- 한 줄 요지: **내재적(intrinsic) self-correction** — 외부 피드백 없이 자기 능력만으로 자기 답을 고치는 것 — 은 추론 태스크에서 작동하지 않으며 성능이 떨어지기도 한다.
- 실무자에게 의미하는 것: 이 책에서 가장 값비싼 착각을 방지하는 논문이다. "LLM에 한 번 더 물어보면 알아서 고친다"는 가정에 기반한 리트라이 루프는 **비용만 늘리고 정확도를 낮출 수 있다.** 설계 규칙: 리플렉션 루프를 넣기 전에 **판정할 수 있는 외부 신호**(단위 테스트, 타입 체커, JSON 스키마 검증, DB 상태 비교, HTTP 상태 코드)를 먼저 확보하라. 신호가 없으면 루프를 넣지 말고 사람에게 올려라.
- 인용 가능한 구절·수치 [초록 확인]: "our research indicates that LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."
- 한계·반박: Reflexion(arXiv:2303.11366v4)·Self-Refine(arXiv:2303.17651v2). 주의 — 이 논문의 범위는 **추론(reasoning)**이다. 생성물 문체 개선 같은 태스크로 확대 해석하면 과잉 일반화다.

## Toolformer: Language Models Can Teach Themselves to Use Tools
- 저자·연도: Timo Schick; Jane Dwivedi-Yu; Roberto Dessì; Roberta Raileanu; Maria Lomeli; Luke Zettlemoyer; Nicola Cancedda; Thomas Scialom (2023)
- 출처: arXiv:2302.04761v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2302.04761
- 발행·최종 리비전일: v1 2023-02-09 (리비전 없음)
- 축 태그: [축 1]
- 한 줄 요지: 어떤 API를 언제 호출하고 어떤 인자를 넘길지를 자기지도(self-supervised) 방식으로 학습시킨다.
- 실무자에게 의미하는 것: 오늘의 function calling / tool use API의 학술 뿌리. 실무 함의는 **"도구는 모델의 약점을 메우는 것"**이라는 프레이밍이다 — 산술, 사실 조회, 최신 정보처럼 훨씬 작고 단순한 시스템이 더 잘하는 일을 모델에게 시키지 말고 도구로 넘겨라. API 몇 개당 시연 몇 개로 충분했다는 점은 도구 스펙(설명·인자)의 품질이 곧 호출 정확도라는 오늘의 경험칙과 이어진다.
- 인용 가능한 구절·수치 [초록 확인]: "LMs can teach themselves to use external tools via simple APIs and achieve the best of both worlds" / 도구 목록: "a calculator, a Q&A system, two different search engines, a translation system, and a calendar."
- 한계·반박: 이 논문은 파인튜닝 접근이고, 현재 실무는 프롬프트/스키마 기반 function calling이 지배적이다. 계보 인용용으로 쓰고 "지금 이렇게 하라"의 근거로 쓰지 말 것.

## ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models
- 저자·연도: Binfeng Xu; Zhiyuan Peng; Bowen Lei; Subhabrata Mukherjee; Yuchen Liu; Dongkuan Xu (2023)
- 출처: arXiv:2305.18323v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2305.18323
- 발행·최종 리비전일: v1 2023-05-23 (리비전 없음)
- 축 태그: [축 1] [축 5]
- 한 줄 요지: 관찰(도구 결과)을 기다리지 않고 계획 전체를 먼저 세운 뒤 실행함으로써 중복 프롬프트 재전송을 없앤다.
- 실무자에게 의미하는 것: **에이전트 비용 구조를 바꾸는 아키텍처 결정**이다. ReAct형 인터리빙은 스텝마다 히스토리를 다시 넣지만, plan-then-execute는 계획을 한 번만 만든다. 비용·지연이 문제라면 "루프를 더 잘 프롬프트하기"보다 이 구조 전환이 훨씬 큰 레버다. 트레이드오프는 명확하다 — 계획을 미리 굳히면 중간 관찰에 따른 적응력을 잃는다.
- 인용 가능한 구절·수치 [초록 확인]: "ReWOO achieves 5x token efficiency and 4% accuracy improvement on HotpotQA, a multi-step reasoning benchmark." / "offloads reasoning ability from 175B GPT3.5 into 7B LLaMA."
- 한계·반박: 관찰 의존적 분기가 많은 태스크에서는 불리하다. 논문 자체가 "도구 실패 시나리오에서의 견고함"을 별도로 주장한다는 점에서, 이 트레이드오프를 저자들도 인식하고 있다.

## Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- 저자·연도: Shunyu Yao; Dian Yu; Jeffrey Zhao; Izhak Shafran; Thomas L. Griffiths; Yuan Cao; Karthik Narasimhan (2023)
- 출처: arXiv:2305.10601v2 / NeurIPS 2023 (arXiv comment: "NeurIPS 2023 camera ready version")
- URL: https://arxiv.org/abs/2305.10601
- 발행·최종 리비전일: v1 2023-05-17 / v2 2023-12-03
- 축 태그: [축 1]
- 한 줄 요지: 사고 단위를 노드로 두고 탐색·백트래킹·자기 평가를 하는 트리 탐색으로 CoT를 일반화한다.
- 실무자에게 의미하는 것: 탐색을 붙이면 효과가 극적일 수 있다는 증거(4% → 74%). 하지만 그 효과가 나온 태스크는 Game of 24·크로스워드처럼 **정답 검증이 값싼 탐색형 문제**다. 당신의 태스크에 값싼 검증기가 없다면 트리 탐색은 비용만 곱해진다. 이건 논쟁 3의 결론과 같은 원리다 — **검증기 유무가 모든 것을 가른다.**
- 인용 가능한 구절·수치 [초록 확인]: "in Game of 24, while GPT-4 with chain-of-thought prompting only solved 4% of tasks, our method achieved a success rate of 74%."
- 한계·반박: 노드 수에 비례하는 비용. Kapoor et al. *AI Agents That Matter*(arXiv:2407.01502)의 "SOTA 에이전트가 불필요하게 복잡하고 비싸다"는 비판이 이 계열을 직접 겨냥한다.

## MemGPT: Towards LLMs as Operating Systems
- 저자·연도: Charles Packer; Sarah Wooders; Kevin Lin; Vivian Fang; Shishir G. Patil; Ion Stoica; Joseph E. Gonzalez (2023)
- 출처: arXiv:2310.08560v2 / 발표처 미확인
- URL: https://arxiv.org/abs/2310.08560
- 발행·최종 리비전일: v1 2023-10-12 / v2 2024-02-12
- 축 태그: [축 1]
- 한 줄 요지: OS의 계층적 메모리(가상 메모리·페이징)를 은유로 삼아, 제한된 컨텍스트 창 위에 **가상 컨텍스트 관리** 계층을 올린다.
- 실무자에게 의미하는 것: 백엔드 개발자에게 가장 잘 통하는 은유다 — 컨텍스트 창은 RAM이고, 외부 저장소는 디스크이고, 필요한 것은 페이징 정책이다. 실무 함의는 **"메모리 기능"을 벡터DB 하나로 뭉뚱그리지 말고 계층(작업 메모리 / 소환 가능한 장기 저장 / 요약 압축)으로 쪼개고, 무엇을 언제 올릴지의 정책을 명시적으로 쓰라는 것**이다. 그 정책이 곧 에이전트 동작의 재현성을 결정한다.
- 인용 가능한 구절·수치 [초록 확인]: "we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory."
- 한계·반박: 초록에 정량 비교 수치가 요약되어 있지 않다 — 수치 인용은 하지 말 것. 아키텍처 은유·설계 원리 인용용.

## Improving Factuality and Reasoning in Language Models through Multiagent Debate
- 저자·연도: Yilun Du; Shuang Li; Antonio Torralba; Joshua B. Tenenbaum; Igor Mordatch (2023)
- 출처: arXiv:2305.14325v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2305.14325
- 발행·최종 리비전일: v1 2023-05-23 (리비전 없음)
- 축 태그: [축 1]
- 한 줄 요지: 여러 LLM 인스턴스가 여러 라운드에 걸쳐 서로의 답과 근거를 반박·수렴시키면 수학·전략 추론과 사실성이 개선된다.
- 실무자에게 의미하는 것: 멀티에이전트 찬성 진영의 대표 근거. 실무 관점의 함의는 **"토론의 이득은 관점 다양성에서 오지 사람 수에서 오지 않는다"** — 같은 프롬프트로 같은 모델을 3개 띄우는 건 토론이 아니라 샘플링이다. 그리고 라운드 수 × 에이전트 수만큼 비용이 곱해진다는 걸 잊으면 안 된다.
- 인용 가능한 구절·수치 [초록 확인]: "multiple language model instances propose and debate their individual responses and reasoning processes over multiple rounds to arrive at a common final answer" / "improves the factual validity of generated content, reducing fallacious answers and hallucinations."
- 한계·반박: MAST(arXiv:2503.13657v3) — 멀티에이전트 시스템의 벤치마크 이득이 종종 미미하고, 실패가 구조적이다.

## Why Do Multi-Agent LLM Systems Fail? (MAST)
- 저자·연도: Mert Cemri; Melissa Z. Pan; Shuyi Yang; Lakshya A. Agrawal; Bhavya Chopra; Rishabh Tiwari; Kurt Keutzer; Aditya Parameswaran 외 5인 (2025)
- 출처: arXiv:2503.13657v3 / 발표처 미확인 (comment: "ArXiv v3")
- URL: https://arxiv.org/abs/2503.13657
- 발행·최종 리비전일: v1 2025-03-17 / v3 2025-10-26
- 축 태그: [축 1]
- 한 줄 요지: 7개 멀티에이전트 프레임워크의 트레이스를 주석해 **14개 실패 모드 / 3범주 분류 체계(MAST)**를 만들었다.
- 실무자에게 의미하는 것: 이 책에서 멀티에이전트 챕터의 뼈대로 쓸 논문이다. 세 범주가 그대로 설계 체크리스트가 된다 — (i) 시스템 설계 문제(역할·종료 조건·프로토콜), (ii) 에이전트 간 정렬 실패(정보 전달 누락·목표 드리프트), (iii) **태스크 검증 실패**(아무도 결과가 맞는지 확인하지 않음). 세 번째가 특히 중요하다: 논쟁 3·4와 같은 결론으로 수렴한다. 그리고 "멀티에이전트로 바꾸면 정확도가 오른다"는 기대를 걷어내는 근거로 쓸 것.
- 인용 가능한 구절·수치 [초록 확인]: "Despite enthusiasm for Multi-Agent LLM Systems (MAS), their performance gains on popular benchmarks are often minimal." / "MAST-Data, a comprehensive dataset of 1600+ annotated traces collected across 7 popular MAS frameworks" / "We develop MAST through rigorous analysis of 150 traces ... validated by high inter-annotator agreement (kappa = 0.88). This process identifies 14 unique modes, clustered into 3 categories: (i) system design issues, (ii) inter-agent misalignment, and (iii) task verification."
- 한계·반박: Du et al.(arXiv:2305.14325). 또한 주석 파이프라인 자체가 LLM-as-a-Judge를 쓴다는 점(논쟁 6과 연결) — 저자들은 인간 주석과의 높은 일치도로 방어한다.

## Lost in the Middle: How Language Models Use Long Contexts
- 저자·연도: Nelson F. Liu; Kevin Lin; John Hewitt; Ashwin Paranjape; Michele Bevilacqua; Fabio Petroni; Percy Liang (2023)
- 출처: arXiv:2307.03172v3 / TACL 2023 (arXiv comment: "Accepted for publication in Transactions of the Association for Computational Linguistics (TACL), 2023")
- URL: https://arxiv.org/abs/2307.03172
- 발행·최종 리비전일: v1 2023-07-06 / v3 2023-11-20
- 축 태그: [축 1] [축 3]
- 한 줄 요지: 관련 정보가 입력의 처음이나 끝에 있을 때 성능이 가장 높고 **중간에 있으면 유의하게 떨어진다** — 명시적 롱 컨텍스트 모델도 마찬가지다.
- 실무자에게 의미하는 것: 컨텍스트 설계에 직접 작용하는 결과다. 세 가지 실천 규칙이 나온다 — (1) 검색 결과를 관련도 순으로 그냥 붙이지 말고 **가장 중요한 것을 앞이나 끝에 배치**하라, (2) "컨텍스트 창이 크니 다 넣자"는 전략에는 정확도 세금이 붙는다, (3) 그래서 리랭킹은 검색 품질 문제이기 이전에 **배치 문제**다.
- 인용 가능한 구절·수치 [초록 확인]: "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."
- 한계·반박: 2023년 모델 세대에서의 결과다. 🕒 2026년 모델에도 동일 크기로 적용된다고 단정하면 안 되며, 본문에서 "이 현상이 완화되었는지는 당신의 모델로 직접 측정하라"로 처리해야 한다. (측정 방법 자체를 논문이 제공한다 — key-value 검색 태스크.)

---

# 축 3. RAG·검색의 학술 근거

## Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- 저자·연도: Patrick Lewis; Ethan Perez; Aleksandra Piktus; Fabio Petroni; Vladimir Karpukhin; Naman Goyal; Heinrich Küttler; Mike Lewis 외 4인 (2020)
- 출처: arXiv:2005.11401v4 / NeurIPS 2020 (arXiv comment: "Accepted at NeurIPS 2020")
- URL: https://arxiv.org/abs/2005.11401
- 발행·최종 리비전일: v1 2020-05-22 / v4 2021-04-12
- 축 태그: [축 3]
- 한 줄 요지: 파라메트릭 메모리(사전학습 seq2seq)와 **비파라메트릭 메모리**(밀집 벡터 인덱스)를 결합하는 범용 레시피. "RAG"라는 용어의 출처.
- 실무자에게 의미하는 것: RAG의 원래 동기가 "컨텍스트 창이 작아서"가 아니라 **지식 갱신 가능성과 출처 추적(provenance)**이었다는 점이 중요하다. 이건 논쟁 2에 직접 작용한다 — 롱 컨텍스트가 정확도에서 RAG를 따라잡아도, "무엇을 근거로 답했는지 보여주고, 문서를 지우면 답도 바뀌게 만드는" 요구는 여전히 검색 계층을 요구한다. 규제·감사·삭제권이 있는 도메인이면 이게 결정적이다.
- 인용 가능한 구절·수치 [초록 확인]: "providing provenance for their decisions and updating their world knowledge remain open research problems" / "we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline."
- 한계·반박: 2020년 아키텍처(파인튜닝된 seq2seq)이며 오늘의 "임베딩 + 프롬프트 삽입" 방식과 다르다. 계보·동기 인용용으로 쓸 것.

## ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT
- 저자·연도: Omar Khattab; Matei Zaharia (2020)
- 출처: arXiv:2004.12832v2 / SIGIR 2020 (arXiv comment: "Accepted at SIGIR 2020")
- URL: https://arxiv.org/abs/2004.12832
- 발행·최종 리비전일: v1 2020-04-27 / v2 2020-06-04
- 축 태그: [축 3]
- 한 줄 요지: 질의와 문서를 독립적으로 인코딩한 뒤 값싼 **late interaction** 단계에서 세밀한 유사도를 계산해, 크로스인코더의 표현력과 사전계산의 효율을 함께 얻는다.
- 실무자에게 의미하는 것: "임베딩 하나로 문서 하나를 요약하는 것"과 "질의-문서 쌍을 매번 함께 넣는 것" 사이에 **중간 지점이 존재한다**는 근거. 검색 품질이 부족한데 리랭커를 전 문서에 돌릴 수는 없는 상황(대부분의 실무 상황)에서 아키텍처 선택지를 넓혀 준다. 그리고 이 논문의 수치는 리랭킹 비용 논의에 그대로 쓸 수 있다.
- 인용 가능한 구절·수치 [초록 확인]: "ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query."
- 한계·반박: 2020년 결과이고 비교 기준선이 당시 BERT 계열이다. 🕒 저장 공간 오버헤드(토큰별 벡터)가 실무 제약인데 초록에서 정량 확인되지 않았다 — 그 수치는 인용하지 말 것.

## Retrieval meets Long Context Large Language Models
- 저자·연도: Peng Xu; Wei Ping; Xianchao Wu; Lawrence McAfee; Chen Zhu; Zihan Liu; Sandeep Subramanian; Evelina Bakhturina 외 2인 (2023)
- 출처: arXiv:2310.03025v2 / ICLR 2024 (arXiv comment: "Published at ICLR 2024")
- URL: https://arxiv.org/abs/2310.03025
- 발행·최종 리비전일: v1 2023-10-04 / v2 2024-01-23
- 축 태그: [축 3]
- 한 줄 요지: "검색 증강 vs 롱 컨텍스트 중 무엇이 나은가, 둘을 합칠 수 있는가"를 정면으로 실험 — 답은 **"합쳐라, 그리고 검색은 컨텍스트 길이와 무관하게 이득이다"**.
- 실무자에게 의미하는 것: 논쟁 2에서 가장 실무적으로 유용한 논문이다. 두 결과가 설계 결정을 직접 정당화한다 — (1) **4K + 검색 ≈ 16K 파인튜닝**이므로 컨텍스트를 늘리는 데 돈을 쓰기 전에 검색을 개선하는 게 비용 효율적이다, (2) 컨텍스트를 이미 32K로 늘렸어도 **검색을 얹으면 또 오른다** — 즉 검색과 롱 컨텍스트는 대체재가 아니라 보완재다.
- 인용 가능한 구절·수치 [초록 확인]: "we find that LLM with 4K context window using simple retrieval-augmentation at generation can achieve comparable performance to finetuned LLM with 16K context window via positional interpolation on long context tasks, while taking much less computation." / "our best model, retrieval-augmented Llama2-70B with 32K context window, outperforms GPT-3.5-turbo-16k and Davinci003 in terms of average score on nine long context tasks."
- 한계·반박: LOFT(arXiv:2406.13121)가 반대 방향 증거. 그리고 모델 세대가 Llama2·GPT-3.5 시절이다 🕒 — 절대 수치가 아니라 **"검색이 컨텍스트 확장과 직교하는 이득을 준다"는 구조적 결론**만 옮기는 게 안전하다.

## Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More? (LOFT)
- 저자·연도: Jinhyuk Lee; Anthony Chen; Zhuyun Dai; Dheeru Dua; Devendra Singh Sachan; Michael Boratko; Yi Luan; Sébastien M. R. Arnold 외 11인 (2024)
- 출처: arXiv:2406.13121v1 / 발표처 미확인 (comment: "29 pages")
- URL: https://arxiv.org/abs/2406.13121
- 발행·최종 리비전일: v1 2024-06-19 (리비전 없음)
- 축 태그: [축 3] [축 4]
- 한 줄 요지: 최대 수백만 토큰 컨텍스트를 요구하는 벤치마크(LOFT)를 만들어 보니, LCLM이 **명시적으로 학습받지 않았는데도** SOTA 검색·RAG 시스템에 맞먹었다. 단 합성적(compositional) 추론에서는 여전히 약했다.
- 실무자에게 의미하는 것: "롱 컨텍스트가 RAG를 삼킨다" 진영의 가장 방법론적으로 단단한 근거. 하지만 실무 독자가 가져갈 것은 두 개의 조건부다 — (1) 조인·집계 같은 **SQL형 합성 추론**은 여전히 컨텍스트에 다 넣는 방식으로 안 된다, (2) **프롬프팅 전략이 성능을 크게 좌우한다**는 발견은 곧 "컨텍스트에 다 넣기"가 튜닝 없는 공짜 승리가 아니라는 뜻이다. 여기에 비용 축(수백만 토큰 × 요청 수)을 더하면 실무 결론은 대체로 하이브리드다.
- 인용 가능한 구절·수치 [초록 확인]: "Our findings reveal LCLMs' surprising ability to rival state-of-the-art retrieval and RAG systems, despite never having been explicitly trained for these tasks. However, LCLMs still face challenges in areas like compositional reasoning that are required in SQL-like tasks. Notably, prompting strategies significantly influence performance."
- 한계·반박: Xu, Ping et al.(arXiv:2310.03025v2), OP-RAG(arXiv:2409.01666). 초록에 비용 비교가 없다 — LOFT를 근거로 "롱 컨텍스트가 더 싸다"고 쓰면 안 된다.

## In Defense of RAG in the Era of Long-Context Language Models (OP-RAG)
- 저자·연도: Tan Yu; Anbang Xu; Rama Akkiraju (2024)
- 출처: arXiv:2409.01666v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2409.01666
- 발행·최종 리비전일: v1 2024-09-03 (리비전 없음)
- 축 태그: [축 3]
- 한 줄 요지: 극단적으로 긴 컨텍스트는 **관련 정보에 대한 집중을 희석**시킨다. 검색 청크의 순서를 보존하는 OP-RAG를 쓰면 훨씬 적은 토큰으로 더 좋은 답을 얻는 스위트 스팟이 존재한다.
- 실무자에게 의미하는 것: 이 논문의 **역U자 곡선**이 실무에서 가장 자주 필요한 그림이다. "top-k를 늘리면 좋아지겠지"라는 직관이 왜 어느 지점부터 배신하는지를 설명해 준다. 그래서 RAG 튜닝의 첫 실험은 임베딩 모델 교체가 아니라 **k를 스윕해서 자기 데이터의 정점을 찾는 것**이어야 한다. 그리고 청크를 관련도 순이 아니라 **원문 순서대로** 넣는 것이 하나의 독립 변수라는 점도 실전 팁이다.
- 인용 가능한 구절·수치 [초록 확인]: "With OP-RAG, as the number of retrieved chunks increases, the answer quality initially rises, and then declines, forming an inverted U-shaped curve. There exist sweet points where OP-RAG could achieve higher answer quality with much less tokens than long-context LLM taking the whole context as input."
- 한계·반박: LOFT(arXiv:2406.13121)가 반대편. 이 논문은 v1만 있고 리비전이 없으며 발표처가 미확인이므로, **동료평가 지위를 주장하지 말고** "역U자 곡선"이라는 관찰과 방법 아이디어만 인용하는 게 안전하다.

## From Local to Global: A Graph RAG Approach to Query-Focused Summarization (GraphRAG)
- 저자·연도: Darren Edge; Ha Trinh; Newman Cheng; Joshua Bradley; Alex Chao; Apurva Mody; Steven Truitt; Dasha Metropolitansky 외 2인 (2024)
- 출처: arXiv:2404.16130v2 / 발표처 미확인
- URL: https://arxiv.org/abs/2404.16130
- 발행·최종 리비전일: v1 2024-04-24 / v2 2025-02-19
- 축 태그: [축 3]
- 한 줄 요지: 일반 RAG는 "이 코퍼스의 주요 테마가 뭐냐" 같은 **전역(global) 질문에 실패**한다. LLM으로 엔티티 지식 그래프를 만들고 커뮤니티 요약을 미리 생성해 이 격차를 메운다.
- 실무자에게 의미하는 것: GraphRAG를 도입할지 판단하는 기준을 명확히 준다 — **질문이 "찾기(lookup)"인가 "종합(sensemaking)"인가.** 사용자 질문이 대부분 특정 사실 검색이면 GraphRAG는 과잉이다. 반대로 "이 티켓들에서 반복되는 문제가 뭐냐" 같은 요약형 질문이 주력이면 일반 RAG는 구조적으로 답할 수 없다. 비용 논쟁의 핵심은 인덱싱 단계에서 **LLM으로 그래프와 커뮤니티 요약을 미리 생성**한다는 점이다 — 즉 질의 시점 비용을 인덱스 구축 비용으로 옮기는 거래다.
- 인용 가능한 구절·수치 [초록 확인]: "RAG fails on global questions directed at an entire text corpus, such as 'What are the main themes in the dataset?'" / "For a class of global sensemaking questions over datasets in the 1 million token range, we show that GraphRAG leads to substantial improvements over a conventional RAG baseline for both the comprehensiveness and diversity of generated answers."
- 한계·반박: 인덱싱 비용의 정량값이 초록에 없다 — "GraphRAG는 N배 비싸다" 류의 수치를 이 논문 근거로 쓰면 안 된다. 미확인 항목에 기록했다. 또한 평가 축이 comprehensiveness·diversity(LLM 판정 성향의 지표)라는 점은 논쟁 6과 함께 읽어야 한다.

---

# 축 4-1. 평가 방법론과 그 타당성 논쟁 (이 책에서 가장 중요한 파트)

## AI Agents That Matter
- 저자·연도: Sayash Kapoor; Benedikt Stroebl; Zachary S. Siegel; Nitya Nadgir; Arvind Narayanan (2024)
- 출처: arXiv:2407.01502v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2407.01502
- 발행·최종 리비전일: v1 2024-07-01 (리비전 없음)
- 축 태그: [축 4]
- 한 줄 요지: 현재 에이전트 벤치마크·평가 관행의 네 가지 결함 — (1) 정확도만 보는 좁은 초점, (2) 모델 개발자와 응용 개발자의 평가 요구 혼동, (3) 부실한 홀드아웃 세트, (4) 표준화·재현성 결여.
- 실무자에게 의미하는 것: 이 책의 평가 챕터가 서 있어야 할 자리를 정해 주는 논문이다. 네 가지가 각각 실무 지침으로 번역된다 — (1) **정확도와 비용을 함께 보고하라.** 논문의 핵심 주장은 정확도만 최적화한 결과 SOTA 에이전트가 "불필요하게 복잡하고 비싸다"는 것이고, 심지어 커뮤니티가 **정확도 향상의 원인을 잘못 짚었다**는 것이다 — 더 정교한 스캐폴딩 때문인 줄 알았던 향상이 그냥 더 많은 호출(=더 많은 돈) 때문일 수 있다. (2) 당신은 응용 개발자다 — 모델 순위표가 아니라 **당신 워크로드에서의 성능**이 필요하다. (3) 홀드아웃 없는 벤치마크에서의 점수는 과적합이다. (4) 평가 스크립트·시드·버전을 고정하지 않으면 다음 주에 재현되지 않는다.
- 인용 가능한 구절·수치 [초록 확인]: "there is a narrow focus on accuracy without attention to other metrics. As a result, SOTA agents are needlessly complex and costly, and the community has reached mistaken conclusions about the sources of accuracy gains." / "many agent benchmarks have inadequate holdout sets, and sometimes none at all. This has led to agents that are fragile because they take shortcuts and overfit to the benchmark in various ways." / "there is a lack of standardization in evaluation practices, leading to a pervasive lack of reproducibility."
- 한계·반박: 구체적 비용-정확도 파레토 수치는 초록에 없다 — 본문 미확인. 미확인 항목에 기록했다.

## Establishing Best Practices for Building Rigorous Agentic Benchmarks (ABC 체크리스트)
- 저자·연도: Yuxuan Zhu; Tengjun Jin; Yada Pruksachatkun; Andy Zhang; Shu Liu; Sasha Cui; Sayash Kapoor; Shayne Longpre 외 17인 (2025)
- 출처: arXiv:2507.02825v5 / 발표처 미확인 (comment: "39 pages, 15 tables, 6 figures")
- URL: https://arxiv.org/abs/2507.02825
- 발행·최종 리비전일: v1 2025-07-03 / v5 2025-08-07
- 축 태그: [축 4]
- 한 줄 요지: 널리 쓰이는 에이전트 벤치마크들의 **태스크 설정·보상 설계에 실제 결함**이 있고, 그 결함이 성능을 상대 기준 최대 100%까지 과대/과소 평가하게 만든다. 이를 잡는 체크리스트(ABC)를 제시.
- 실무자에게 의미하는 것: 논쟁 4의 가장 강력한 무기다. 구체적 사례가 특히 아프다 — **"TAU-bench는 빈 응답을 성공으로 계산한다"**. 실무 번역: 자기 사내 eval을 만들 때 가장 흔한 버그는 모델이 아니라 **채점기**에 있다. 그래서 eval을 만든 직후 해야 할 일은 (a) 일부러 빈 응답/무작위 응답을 넣어 채점기가 실패로 잡는지 확인, (b) 통과한 케이스를 사람이 직접 표본 검토하는 것이다. 이 논문이 CVE-Bench에 체크리스트를 적용해 과대평가를 33% 줄였다는 것 자체가 "채점기 감사"의 투자 수익률이다.
- 인용 가능한 구절·수치 [초록 확인]: "For example, SWE-bench Verified uses insufficient test cases, while TAU-bench counts empty responses as successful. Such issues can lead to under- or overestimation of agents' performance by up to 100% in relative terms." / "When applied to CVE-Bench, a benchmark with a particularly complex evaluation design, ABC reduces the performance overestimation by 33%."
- 한계·반박: 체크리스트 자체의 검증은 저자들의 사례 연구에 의존한다. 그리고 v5까지 리비전된 최근 논문이므로 인용 시 버전을 명시할 것.

## SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- 저자·연도: Carlos E. Jimenez; John Yang; Alexander Wettig; Shunyu Yao; Kexin Pei; Ofir Press; Karthik Narasimhan (2023)
- 출처: arXiv:2310.06770v3 / ICLR 2024 (arXiv comment 명시, OpenReview: https://openreview.net/forum?id=VTF8yNQM66)
- URL: https://arxiv.org/abs/2310.06770
- 발행·최종 리비전일: v1 2023-10-10 / v3 2024-11-11
- 축 태그: [축 4]
- 한 줄 요지: 실제 GitHub 이슈와 그에 대응하는 PR로 만든 2,294개 소프트웨어 엔지니어링 문제. 코드베이스를 수정해 이슈를 해결해야 하고, 채점은 테스트 실행 기반.
- 실무자에게 의미하는 것: 코딩 에이전트 이야기의 기준점. 실무자가 반드시 알아야 할 것은 **v1 시점의 최고 성능이 1.96%였다는 사실**이다 — 이 숫자와 오늘의 리더보드 숫자 사이의 격차가 곧 "리더보드 숫자를 자기 코드베이스 기대치로 옮기면 안 되는 이유"의 크기다. 그리고 이 벤치마크의 설계에서 배울 것: **채점을 사람이나 LLM이 아니라 테스트 실행으로 했다.** 사내 eval도 가능한 한 실행 가능한 판정으로 만들어야 한다.
- 인용 가능한 구절·수치 [초록 확인]: "an evaluation framework consisting of $2,294$ software engineering problems drawn from real GitHub issues and corresponding pull requests across $12$ popular Python repositories." / "The best-performing model, Claude 2, is able to solve a mere $1.96$% of the issues." (**주의: v1(2023-10) 시점 수치다. 현재 성능이 아니다.** 🕒)
- 한계·반박: SWE-Bench+(arXiv:2410.06992v2)가 해답 유출·약한 테스트를 지적. ABC(arXiv:2507.02825v5)는 SWE-bench Verified의 테스트 케이스가 불충분하다고 지적.

## SWE-Bench+: Enhanced Coding Benchmark for LLMs
- 저자·연도: Reem Aleithan; Haoran Xue; Mohammad Mahdi Mohajer; Elijah Nnorom; Gias Uddin; Song Wang (2024)
- 출처: arXiv:2410.06992v2 / 발표처 미확인
- URL: https://arxiv.org/abs/2410.06992
- 발행·최종 리비전일: v1 2024-10-09 / v2 2024-10-10
- 축 태그: [축 4]
- 한 줄 요지: SWE-bench에서 성공한 패치들을 수동 검사한 결과, **3분의 1가량이 이슈 본문·코멘트에 답이 적혀 있던 경우(해답 유출)**이고 또 3분의 1가량은 테스트가 부실해 통과한 경우였다. 걸러내면 해결률이 3분의 1 미만으로 떨어진다.
- 실무자에게 의미하는 것: 이 책에서 벤치마크 회의주의를 가르치는 데 가장 효과적인 단일 자료다. 요지는 "SWE-bench가 나쁘다"가 아니라 **"실제 데이터로 만든 벤치마크에도 지름길이 남아 있고, 지름길은 점수를 3배 부풀릴 수 있다"**는 것. 사내 eval 설계 지침으로 직결된다 — (1) 태스크 설명에 정답이 새어 있는지 검사하라, (2) **테스트가 실제로 오답을 잡는지** 확인하라(변이 테스트/의도적 오답 주입), (3) 모델 지식 컷오프 이후 데이터를 홀드아웃으로 확보하라.
- 인용 가능한 구절·수치 [초록 확인]: "32.67% of the successful patches involve cheating as the solutions were directly provided in the issue report or the comments. We refer to as solution leakage problem." / "31.08% of the passed patches are suspicious patches due to weak test cases" / "When we filtered out these problematic issues, the resolution rate of SWE-Agent+GPT-4 dropped from 12.47% to 3.97%." / "over 94% of the issues were created before LLM's knowledge cutoff dates, posing potential data leakage issues."
- 한계·반박: 분석 대상이 당시 리더보드 상위였던 SWE-Agent+GPT-4 한 조합이며, 유출 판정은 수동 스크리닝이다. 원논문 측(SWE-bench)은 이후 Verified 등 정제 세트를 내놓았으나 ABC는 그 Verified에도 테스트 불충분 문제를 지적한다.

## GAIA: a benchmark for General AI Assistants
- 저자·연도: Grégoire Mialon; Clémentine Fourrier; Craig Swift; Thomas Wolf; Yann LeCun; Thomas Scialom (2023)
- 출처: arXiv:2311.12983v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2311.12983
- 발행·최종 리비전일: v1 2023-11-21 (리비전 없음)
- 축 태그: [축 4]
- 한 줄 요지: 사람에게는 개념적으로 쉽지만 AI에게는 어려운 실세계 질문 466개(추론·멀티모달·웹 브라우징·도구 사용). 300개는 답을 비공개로 유지해 리더보드용 홀드아웃으로 삼았다.
- 실무자에게 의미하는 것: **벤치마크 철학이 뒤집힌 사례**로 인용 가치가 크다. "사람에게 더 어려운 문제"를 쫓지 않고 "사람은 쉽게 하는데 AI는 못 하는 문제"를 골랐다. 실무 번역: 사내 eval을 만들 때 어려운 엣지 케이스만 모으는 함정에 빠지기 쉽지만, 정작 사업을 망치는 건 **사람이면 당연히 하는 일을 에이전트가 못 하는 경우**다. 그리고 답 300개를 비공개로 남긴 설계는 Kapoor et al.이 지적한 홀드아웃 문제에 대한 모범 답안이다.
- 인용 가능한 구절·수치 [초록 확인]: "we show that human respondents obtain 92% vs. 15% for GPT-4 equipped with plugins." / "we devise 466 questions and their answer. We release our questions while retaining answers to 300 of them to power a leader-board." (**2023-11 시점 모델 수치다** 🕒)
- 한계·반박: 15%는 GPT-4+플러그인 시절이다. 현재 성능 근거로 절대 쓰지 말 것. 인용 가치는 **인간-AI 격차의 구조**와 홀드아웃 설계에 있다.

## WebArena: A Realistic Web Environment for Building Autonomous Agents
- 저자·연도: Shuyan Zhou; Frank F. Xu; Hao Zhu; Xuhui Zhou; Robert Lo; Abishek Sridhar; Xianyi Cheng; Tianyue Ou 외 4인 (2023)
- 출처: arXiv:2307.13854v4 / 발표처 미확인
- URL: https://arxiv.org/abs/2307.13854
- 발행·최종 리비전일: v1 2023-07-25 / v4 2024-04-16
- 축 태그: [축 4]
- 한 줄 요지: 실제로 동작하는 4개 도메인 웹사이트(이커머스·포럼·협업 개발·CMS)로 재현 가능한 환경을 만들고, **기능적 정확성**으로 채점한다.
- 실무자에게 의미하는 것: 브라우저 에이전트를 검토할 때의 현실 감각. 그리고 방법론적으로 배울 점이 두 개다 — (1) 평가를 **최종 상태의 기능적 정확성**으로 채점했다(텍스트 유사도가 아니라), (2) 환경을 셀프호스팅 가능하게 만들어 재현성을 확보했다. 실제 사이트에 붙여 평가하면 사이트가 변해서 어제 결과를 재현할 수 없다 — 이건 사내 에이전트 eval에서 정확히 같은 문제로 나타난다.
- 인용 가능한 구절·수치 [초록 확인]: "our best GPT-4-based agent only achieves an end-to-end task success rate of 14.41%, significantly lower than the human performance of 78.24%." (**v1~v4 시점 모델 기준** 🕒)
- 한계·반박: 모델 세대가 지났다. 격차의 구조(사람 78% vs 에이전트 14%)와 환경 설계 원칙만 인용하고 절대 수치를 현재 상태로 제시하지 말 것.

## τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
- 저자·연도: Shunyu Yao; Noah Shinn; Pedram Razavi; Karthik Narasimhan (2024)
- 출처: arXiv:2406.12045v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2406.12045
- 발행·최종 리비전일: v1 2024-06-17 (리비전 없음)
- 축 태그: [축 4]
- 한 줄 요지: 사용자(LLM 시뮬레이션)와의 동적 대화 + 도메인 정책 준수를 평가한다. 채점은 대화 종료 시점의 **DB 상태를 목표 상태와 비교**. 그리고 여러 시행에서의 일관성을 재는 **pass^k** 지표를 제안한다.
- 실무자에게 의미하는 것: 이 책의 신뢰성 챕터에 가장 필요한 논문이다. 세 가지를 준다 — (1) **pass@k와 pass^k의 구분**. 프로덕션은 "8번 중 한 번 성공"이 아니라 "8번 다 성공"을 요구한다. 논문의 수치가 그 격차를 보여준다: 평균 성공률은 50% 미만이지만 retail에서 pass^8은 25% 미만이다. 즉 **에이전트의 진짜 문제는 평균 실력이 아니라 분산이다.** (2) 채점을 최종 DB 상태 비교로 하는 설계 — 사내 eval에 그대로 이식 가능하다. (3) "정책 준수"를 능력과 별개 축으로 평가한다는 발상 — 환불 규정, 권한 규칙 같은 것을 지키는지는 태스크 성공과 다른 문제다.
- 인용 가능한 구절·수치 [초록 확인]: "We also propose a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials." / "even state-of-the-art function calling agents (like gpt-4o) succeed on <50% of the tasks, and are quite inconsistent (pass^8 <25% in retail)." / "Our findings point to the need for methods that can improve the ability of agents to act consistently and follow rules reliably."
- 한계·반박: ABC(arXiv:2507.02825v5)가 **"TAU-bench는 빈 응답을 성공으로 계산한다"**고 직접 지적한다. 이 쌍은 책에 그대로 쓸 가치가 있다 — 신뢰성을 측정하려 만든 벤치마크에도 채점 결함이 있었다는 이야기니까. 또한 사용자를 LLM이 시뮬레이션한다는 점은 실제 사용자 행동과의 격차를 남긴다.

## OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
- 저자·연도: Tianbao Xie; Danyang Zhang; Jixuan Chen; Xiaochuan Li; Siheng Zhao; Ruisheng Cao; Toh Jing Hua; Zhoujun Cheng 외 9인 (2024)
- 출처: arXiv:2404.07972v2 / 발표처 미확인 (comment: "51 pages, 21 figures")
- URL: https://arxiv.org/abs/2404.07972
- 발행·최종 리비전일: v1 2024-04-11 / v2 2024-05-30
- 축 태그: [축 4]
- 한 줄 요지: 실제 OS(Ubuntu·Windows·macOS) 환경에서 임의 앱을 쓰는 369개 태스크. 각 태스크마다 **초기 상태 설정과 실행 기반 채점 스크립트**를 갖춰 재현성을 확보했다.
- 실무자에게 의미하는 것: 컴퓨터 사용(computer use) 에이전트의 현실. 그리고 실패 원인이 구체적이라 유용하다 — **GUI 그라운딩과 조작 지식**이 병목이라는 것. 실무 번역: 화면을 보고 클릭하는 방식은 원리적으로 취약하므로, **API가 존재하면 GUI 대신 API를 쓰라**는 설계 원칙이 정당화된다. GUI 자동화는 API가 없을 때의 최후 수단이다. 그리고 "태스크별 초기 상태 설정 + 실행 기반 채점 스크립트"는 사내 eval 하네스 설계의 좋은 템플릿이다.
- 인용 가능한 구절·수치 [초록 확인]: "we create a benchmark of 369 computer tasks" / "While humans can accomplish over 72.36% of the tasks, the best model achieves only 12.24% success, primarily struggling with GUI grounding and operational knowledge." (**2024-04/05 시점 모델 기준** 🕒)
- 한계·반박: 모델 세대 경과. 절대 수치가 아니라 **격차의 구조와 실패 원인(GUI 그라운딩)**을 인용할 것.

## Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- 저자·연도: Lianmin Zheng; Wei-Lin Chiang; Ying Sheng; Siyuan Zhuang; Zhanghao Wu; Yonghao Zhuang; Zi Lin; Zhuohan Li 외 5인 (2023)
- 출처: arXiv:2306.05685v4 / NeurIPS 2023 Datasets and Benchmarks Track (arXiv comment 명시)
- URL: https://arxiv.org/abs/2306.05685
- 발행·최종 리비전일: v1 2023-06-09 / v4 2023-12-24
- 축 태그: [축 4]
- 한 줄 요지: 강한 LLM을 심판으로 쓰는 방법론을 정립하고, MT-bench(멀티턴 문항)와 Chatbot Arena(크라우드소싱 대결)로 인간 선호와의 일치도를 검증했다.
- 실무자에게 의미하는 것: LLM-as-a-judge를 쓸 근거이면서 동시에 **한계 목록의 출처**다. 이 논문에서 가져갈 실무 규칙은 저자들이 직접 나열한 편향들이다 — **position(순서), verbosity(길수록 좋게 봄), self-enhancement(자기 출력 편애)**, 그리고 제한된 추론 능력. 그래서 judge를 붙일 때의 최소 위생은 (1) A/B 순서를 무작위화하거나 양방향 모두 돌려 집계, (2) 길이를 통제하거나 최소한 길이와 점수의 상관을 모니터링, (3) 평가 대상과 심판을 다른 모델로. 80% 일치도는 "인간끼리도 그 정도"라는 기준선과 함께 제시해야 정직하다.
- 인용 가능한 구절·수치 [초록 확인]: "We examine the usage and limitations of LLM-as-a-judge, including position, verbosity, and self-enhancement biases, as well as limited reasoning ability, and propose solutions to mitigate some of them." / "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans." / "The MT-bench questions, 3K expert votes, and 30K conversations with human preferences are publicly available."
- 한계·반박: Wang et al.(arXiv:2305.17926v2) 순서 편향의 크기, Panickssery et al.(arXiv:2404.13076) 자기편애의 인과. 그리고 GPT-4 시절 결과다 🕒.

## Large Language Models are not Fair Evaluators
- 저자·연도: Peiyi Wang; Lei Li; Liang Chen; Zefan Cai; Dawei Zhu; Binghuai Lin; Yunbo Cao; Qi Liu 외 2인 (2023)
- 출처: arXiv:2305.17926v2 / 발표처 미확인
- URL: https://arxiv.org/abs/2305.17926
- 발행·최종 리비전일: v1 2023-05-29 / v2 2023-08-30
- 축 태그: [축 4]
- 한 줄 요지: 후보 응답의 **등장 순서만 바꿔도** 품질 순위를 조작할 수 있다. 완화책으로 다중 근거 생성, 순서 균형 집계, 사람 개입 캘리브레이션을 제안.
- 실무자에게 의미하는 것: 이 논문의 수치는 강력한 경고다 — 순서를 조작해서 Vicuna-13B가 ChatGPT를 80개 질의 중 66개에서 이기게 만들 수 있었다. 실무 번역: **순서를 무작위화하지 않은 judge 결과는 데이터가 아니라 노이즈다.** 그리고 저자들의 완화책 중 "순서 균형 집계(Balanced Position Calibration)"는 구현이 사실상 무료다 — A/B와 B/A를 둘 다 돌려 평균 내면 끝이다. 사내 eval 하네스에 처음부터 넣어야 하는 기능이다.
- 인용 가능한 구절·수치 [초록 확인]: "the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context. This manipulation allows us to skew the evaluation result, making one model appear considerably superior to the other, e.g., Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator."
- 한계·반박: 평가자 모델이 ChatGPT/GPT-4 세대다 🕒. 최신 모델에서 편향 크기가 줄었는지는 별도 측정이 필요하며, 그 측정 자체가 실무 과제라는 게 이 책의 논점이 될 수 있다.

## LLM Evaluators Recognize and Favor Their Own Generations
- 저자·연도: Arjun Panickssery; Samuel R. Bowman; Shi Feng (2024)
- 출처: arXiv:2404.13076v1 / 발표처 미확인
- URL: https://arxiv.org/abs/2404.13076
- 발행·최종 리비전일: v1 2024-04-15 (리비전 없음)
- 축 태그: [축 4]
- 한 줄 요지: LLM은 자기 출력을 알아보는(self-recognition) 능력이 있고, 그 능력의 강도와 **자기편애(self-preference) 편향의 강도 사이에 선형 상관**이 있다. 통제 실험으로 인과 방향을 지지.
- 실무자에게 의미하는 것: 아주 구체적인 설계 금지 사항 하나를 준다 — **생성 모델과 심판 모델을 같게 두지 마라.** 특히 파이프라인에서 흔한 패턴, 즉 GPT로 생성하고 GPT로 채점하는 구성은 자기편애로 점수를 부풀린다. 이건 reward modeling, self-refine 루프, 그리고 앞서 본 MAST의 LLM 주석 파이프라인에도 동일하게 적용되는 우려다. 실무 대응: 심판을 다른 계열 모델로 두거나, 최소한 교차 심판(모델 A가 채점한 결과와 모델 B가 채점한 결과의 일치도)을 보고하라.
- 인용 가능한 구절·수치 [초록 확인]: "LLMs such as GPT-4 and Llama 2 have non-trivial accuracy at distinguishing themselves from other LLMs and humans. By fine-tuning LLMs, we discover a linear correlation between self-recognition capability and the strength of self-preference bias; using controlled experiments, we show that the causal explanation resists straightforward confounders."
- 한계·반박: GPT-4/Llama 2 세대 🕒. 편향의 절대 크기 수치는 초록에 없다 — "N% 부풀린다"고 쓰면 안 된다.

## A Survey on LLM-as-a-Judge
- 저자·연도: Jiawei Gu; Xuhui Jiang; Zhichao Shi; Hexiang Tan; Xuehao Zhai; Chengjin Xu; Wei Li; Yinghan Shen 외 8인 (2024)
- 출처: arXiv:2411.15594v6 / 발표처 미확인
- URL: https://arxiv.org/abs/2411.15594
- 발행·최종 리비전일: v1 2024-11-23 / v6 2025-10-19
- 축 태그: [축 4]
- 한 줄 요지: "신뢰할 수 있는 LLM-as-a-Judge 시스템을 어떻게 만드는가"를 중심 질문으로, 일관성 개선·편향 완화·시나리오 적응 전략과 **심판의 신뢰성 자체를 평가하는 방법론**을 정리한다.
- 실무자에게 의미하는 것: 논쟁 6의 "설계하면 쓸 수 있다" 진영. 실무자에게 가장 중요한 프레이밍은 **심판도 평가 대상이라는 것**이다. 사내 eval에 judge를 붙이면 그 judge의 인간 일치도를 측정하는 작은 라벨 세트를 함께 만들어야 한다 — 안 그러면 측정하지 않은 측정 도구로 시스템을 판단하게 된다. 리비전이 v6(2025-10)까지 있어 이 문서의 자료 중 비교적 최신 상태다.
- 인용 가능한 구절·수치 [초록 확인]: "ensuring the reliability of LLM-as-a-Judge systems remains a significant challenge that requires careful design and standardization" / "We explore strategies to enhance reliability, including improving consistency, mitigating biases, and adapting to diverse assessment scenarios. Additionally, we propose methodologies for evaluating the reliability of LLM-as-a-Judge systems, supported by a novel benchmark designed for this purpose."
- 한계·반박: 서베이이므로 특정 완화책의 효과 크기를 이 논문 근거로 인용하면 안 된다.

---

# 축 4-2. 안전성·프롬프트 인젝션

## Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection
- 저자·연도: Kai Greshake; Sahar Abdelnabi; Shailesh Mishra; Christoph Endres; Thorsten Holz; Mario Fritz (2023)
- 출처: arXiv:2302.12173v2 / 발표처 미확인
- URL: https://arxiv.org/abs/2302.12173
- 발행·최종 리비전일: v1 2023-02-23 / v2 2023-05-05
- 축 태그: [축 4]
- 한 줄 요지: **간접(indirect) 프롬프트 인젝션**을 정의하고 위협 모델을 세운 논문. 공격자가 LLM에 직접 접근하지 않고, 검색될 만한 데이터에 명령을 심어 원격으로 애플리케이션을 조작한다.
- 실무자에게 의미하는 것: 이 책 보안 챕터의 출발점이다. 핵심 통찰 한 줄이 모든 것을 규정한다 — **"LLM 통합 애플리케이션은 데이터와 명령의 경계를 흐린다."** 백엔드 개발자에게 이건 익숙한 문제의 새 형태다: SQL 인젝션이 데이터를 쿼리로 오인하게 만드는 것이었다면, 프롬프트 인젝션은 데이터를 지시로 오인하게 만든다. 차이는 **SQL에는 파라미터 바인딩이라는 원리적 해결책이 있지만 프롬프트에는 없다**는 것 — 그래서 방어가 프롬프트 레벨이 아니라 아키텍처 레벨(권한·격리)로 올라가야 한다. 논문이 나열하는 영향(데이터 절취, 웜, 정보 생태계 오염)은 위협 모델링 워크숍의 체크리스트로 쓸 수 있다.
- 인용 가능한 구절·수치 [초록 확인]: "We argue that LLM-Integrated Applications blur the line between data and instructions." / "We show how processing retrieved prompts can act as arbitrary code execution, manipulate the application's functionality, and control how and if other APIs are called." / "Despite the increasing integration and reliance on LLMs, effective mitigations of these emerging threats are currently lacking."
- 한계·반박: "효과적 완화가 부재하다"는 2023년 진술이다 🕒. CaMeL(arXiv:2503.18813v2)과 Design Patterns(arXiv:2506.08837v3)가 이후 아키텍처 기반 방어를 제시했으므로, 이 문장을 현재 상태로 인용하면 안 된다 — **"문제 제기 시점의 진단"으로 명시할 것.**

## InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents
- 저자·연도: Qiusi Zhan; Zhixiang Liang; Zifan Ying; Daniel Kang (2024)
- 출처: arXiv:2403.02691v3 / ACL 2024 Findings (arXiv comment: "36 pages, 6 figures, 13 tables (ACL 2024 Findings)")
- URL: https://arxiv.org/abs/2403.02691
- 발행·최종 리비전일: v1 2024-03-05 / v3 2024-08-04
- 축 태그: [축 4]
- 한 줄 요지: 도구 통합 에이전트의 간접 인젝션 취약성을 재는 벤치마크. 공격 의도를 **사용자 직접 피해**와 **개인정보 유출** 두 유형으로 분류했다.
- 실무자에게 의미하는 것: 위협 모델을 두 축으로 쪼갠 게 실무적으로 유용하다 — 방어 설계가 달라지기 때문이다. 직접 피해(잘못된 송금, 파일 삭제)는 **쓰기 권한 제한과 승인 게이트**로 막고, 유출은 **송신 채널 제한(egress control)**으로 막는다. 하나의 "인젝션 방어"로 뭉치면 둘 다 놓친다. 그리고 24%라는 숫자는 경영진 설명용으로 충분히 아프다: 방어 없는 ReAct 에이전트는 네 번 중 한 번 공격당한다.
- 인용 가능한 구절·수치 [초록 확인]: "InjecAgent comprises 1,054 test cases covering 17 different user tools and 62 attacker tools." / "We evaluate 30 different LLM agents and show that agents are vulnerable to IPI attacks, with ReAct-prompted GPT-4 vulnerable to attacks 24% of the time." / "the attacker instructions are reinforced with a hacking prompt, shows additional increases in success rates, nearly doubling the attack success rate on the ReAct-prompted GPT-4."
- 한계·반박: 2024년 모델 기준 🕒. 또한 이 벤치마크는 방어 없는 기본 설정 취약성 측정에 초점이 있어, 방어 효과 비교는 AgentDojo가 더 낫다.

## AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
- 저자·연도: Edoardo Debenedetti; Jie Zhang; Mislav Balunović; Luca Beurer-Kellner; Marc Fischer; Florian Tramèr (2024)
- 출처: arXiv:2406.13352v3 / 발표처 미확인
- URL: https://arxiv.org/abs/2406.13352 (본문 HTML: https://arxiv.org/html/2406.13352v3)
- 발행·최종 리비전일: v1 2024-06-19 / v3 2024-11-24 (comment: "Updated version after fixing a bug in the Llama implementation and updating the travel suite")
- 축 태그: [축 4]
- 한 줄 요지: 정적 테스트 세트가 아니라 **공격·방어를 계속 추가할 수 있는 확장 가능 환경**. 현실적 태스크 97개와 보안 테스트 케이스 629개를 갖췄다.
- 실무자에게 의미하는 것: 이 책 보안 챕터의 **수치 근거**가 여기 있다. 세 가지가 결정적이다.
  1. **도구 필터링이 놀랍도록 효과적이다.** 논문 본문: 단순 도구 필터 방어가 공격 성공률을 7.5%까지 낮췄다. 실무 번역 — 인젝션 방어의 1순위는 정교한 프롬프트 가드가 아니라 **"이 태스크에 필요한 도구만 노출하기"**다. 사용자가 이메일을 읽기만 하면 되는 요청에 send_email 도구를 붙여 두지 마라. 이건 최소 권한 원칙의 재발견이고, 구현 비용이 거의 없다.
  2. 논문 본문이 도구 격리의 **한계**도 명시한다 — 사용자 태스크가 읽기 권한만 요구하고 공격자 태스크가 쓰기를 요구할 때 잘 통하고, 그렇지 않으면 실패한다. 즉 은탄환이 아니다.
  3. **더 유능한 모델이 오히려 공격하기 쉬운 역스케일링 경향**이 관측됐다. 실무 번역 — 모델을 업그레이드하면 보안이 개선될 거라는 기대는 근거가 없다. 보안은 모델 축이 아니라 시스템 축의 문제다.
- 인용 가능한 구절·수치 [본문 확인, v3]:
  - "Our simple tool filtering defense is particularly effective, lowering the attack success rate to 7.5%." (§4.3 "Prompt Injection Defenses", Figure 9 논의부 — 직전 절 제목을 본문 덤프에서 확인)
  - "This defense is effective for a large number of the test cases in our suite, where the user task only requires read-access to a model's state (e.g., reading emails), while the attacker's task requires write-access (e.g., sending emails)." (같은 절)
  - "We find that more capable models tend to be easier to attack, a form of inverse scaling law" (§4.1 "Performance of Baseline Agents and Attack", Figure 6(a) 논의부 — 직전 절 제목을 본문 덤프에서 확인)
  - 초록 [초록 확인]: "We populate the environment with 97 realistic tasks ..., 629 security test cases, and various attack and defense paradigms from the literature." / "state-of-the-art LLMs fail at many tasks (even in the absence of attacks), and existing prompt injection attacks break some security properties but not all."
  - 표적 공격 성공률로 본문 표에 등장한 값: 57.7% (±2.0) — "Important message" 공격. (v3 기준. 표의 다른 셀 값은 이 문서에서 교차 확인하지 않았으므로 인용하지 말 것.)
- 한계·반박: CaMeL(arXiv:2503.18813v2)이 같은 환경에서 더 강한 보장을 주장한다. 모델 세대 경과 🕒. **주의: 이 논문의 수치는 v3 기준이며, v1과 v3 사이에 Llama 구현 버그 수정이 있었다** — 버전을 반드시 명시할 것.

## Defeating Prompt Injections by Design (CaMeL)
- 저자·연도: Edoardo Debenedetti; Ilia Shumailov; Tianqi Fan; Jamie Hayes; Nicholas Carlini; Daniel Fabian; Christoph Kern; Chongyang Shi 외 2인 (2025)
- 출처: arXiv:2503.18813v2 / 발표처 미확인 (comment: "Updated version with newer models and link to the code")
- URL: https://arxiv.org/abs/2503.18813
- 발행·최종 리비전일: v1 2025-03-24 / v2 2025-06-24
- 축 태그: [축 4]
- 한 줄 요지: LLM을 신뢰하지 않는 전제에서, 신뢰된 질의로부터 **제어 흐름과 데이터 흐름을 명시적으로 추출**해 신뢰할 수 없는 데이터가 프로그램 흐름에 영향을 주지 못하게 하고, **capability** 개념으로 무단 데이터 흐름을 통한 유출을 막는다.
- 실무자에게 의미하는 것: "설계로 막을 수 있다" 진영의 대표 논문이며, 백엔드 개발자에게 가장 이해하기 쉬운 방어 모델이다. 핵심은 **모델을 고치지 않고 모델 주변에 시스템 계층을 두른다**는 것 — "underlying models are susceptible to attacks"인 상태에서도 보안을 유지한다는 게 논문의 주장이다. 실무 설계 원칙 두 개로 번역된다: (1) 도구 호출 순서(제어 흐름)를 신뢰할 수 없는 데이터가 바꾸지 못하게 하라 — 즉 계획을 신뢰 경계 안에서 확정하고 그 밖의 데이터는 값으로만 흘려라. (2) 도구 호출 시점에 **capability 기반 정책을 강제**하라 — 어떤 출처의 데이터가 어떤 채널로 나갈 수 있는지를 코드로 규정하라. 그리고 77% vs 84%라는 숫자가 이 접근의 **대가**를 정직하게 보여준다. 보안을 위해 기능의 일부를 포기하는 거래이고, 그 크기를 인용할 수 있다는 게 이 논문의 실무적 가치다.
- 인용 가능한 구절·수치 [초록 확인]: "we propose CaMeL, a robust defense that creates a protective system layer around the LLM, securing it even when underlying models are susceptible to attacks." / "CaMeL explicitly extracts the control and data flows from the (trusted) query; therefore, the untrusted data retrieved by the LLM can never impact the program flow." / "We demonstrate effectiveness of CaMeL by solving $77\%$ of tasks with provable security (compared to $84\%$ with an undefended system) in AgentDojo."
- 한계·반박: Greshake et al.의 "원리적 완화 부재" 진단에 대한 응답이지만, 보장 범위가 **정책으로 표현 가능한 속성**에 한정된다. 그리고 개발자가 정책을 직접 써야 하므로 정책 작성 오류가 새로운 실패 지점이 된다. 발표처 미확인이므로 동료평가 지위를 주장하지 말 것.

## Design Patterns for Securing LLM Agents against Prompt Injections
- 저자·연도: Luca Beurer-Kellner; Beat Buesser; Ana-Maria Creţu; Edoardo Debenedetti; Daniel Dobos; Daniel Fabian; Marc Fischer; David Froelicher 외 6인 (2025)
- 출처: arXiv:2506.08837v3 / 발표처 미확인
- URL: https://arxiv.org/abs/2506.08837
- 발행·최종 리비전일: v1 2025-06-10 / v3 2025-06-27
- 축 태그: [축 4]
- 한 줄 요지: 인젝션에 "증명 가능한 저항"을 갖는 에이전트 설계 패턴들을 원칙적으로 정리하고, **유틸리티-보안 트레이드오프**를 분석하며 사례 연구로 적용 가능성을 보인다.
- 실무자에게 의미하는 것: 이 책 보안 챕터의 **구조**를 그대로 제공할 수 있는 자료다. 개별 방어 기법 나열이 아니라 패턴 카탈로그이므로, 독자가 자기 시스템에 맞는 패턴을 고르는 방식으로 쓸 수 있다. 그리고 논문이 트레이드오프를 정면으로 다룬다는 점이 중요하다 — 실무자가 결국 하게 되는 질문은 "안전한가"가 아니라 **"이 에이전트의 자유도를 얼마나 깎아야 안전해지는가"**이기 때문이다. 검색 시점(2026-07) 기준 비교적 최신 자료다.
- 인용 가능한 구절·수치 [초록 확인]: "we propose a set of principled design patterns for building AI agents with provable resistance to prompt injection. We systematically analyze these patterns, discuss their trade-offs in terms of utility and security, and illustrate their real-world applicability through a series of case studies."
- 한계·반박: 초록에 정량 결과가 없다 — **효과 크기 수치를 이 논문 근거로 인용하면 안 된다.** 수치가 필요하면 AgentDojo(7.5%)나 CaMeL(77% vs 84%)을 쓸 것. 개별 패턴명·정의는 본문 미확인이므로 미확인 항목에 기록했다.

## AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents
- 저자·연도: Maksym Andriushchenko; Alexandra Souly; Mateusz Dziemian; Derek Duenas; Maxwell Lin; Justin Wang; Dan Hendrycks; Andy Zou 외 6인 (2024)
- 출처: arXiv:2410.09024v3 / ICLR 2025 (arXiv comment: "Accepted at ICLR 2025")
- URL: https://arxiv.org/abs/2410.09024
- 발행·최종 리비전일: v1 2024-10-11 / v3 2025-04-18
- 축 태그: [축 4]
- 한 줄 요지: 명시적으로 악의적인 에이전트 태스크 110개(증강 포함 440개), 11개 위해 범주. **거부하는지**만이 아니라 탈옥된 에이전트가 **다단계 태스크를 수행할 능력을 유지하는지**까지 측정한다.
- 실무자에게 의미하는 것: 안전 정렬이 에이전트 문맥에서 왜 약한지를 보여준다. 세 발견이 각각 아프다 — (1) 선도 모델들이 탈옥 없이도 악의적 에이전트 요청에 **놀랍도록 순응적**이었다, (2) 단순한 범용 탈옥 템플릿을 에이전트용으로 적응시키는 것으로 충분했다, (3) 탈옥 후에도 **일관되고 유해한 다단계 행동**과 능력이 유지됐다. 실무 번역: 모델 제공자의 안전 정렬을 자기 시스템의 보안 통제로 계산하지 마라. 에이전트가 실제 부작용(송금·삭제·발송)을 낼 수 있다면 통제는 도구 계층과 권한 계층에 있어야 한다 — 모델의 거부 성향이 아니라.
- 인용 가능한 구절·수치 [초록 확인]: "The benchmark includes a diverse set of 110 explicitly malicious agent tasks (440 with augmentations), covering 11 harm categories including fraud, cybercrime, and harassment." / "(1) leading LLMs are surprisingly compliant with malicious agent requests without jailbreaking, (2) simple universal jailbreak templates can be adapted to effectively jailbreak agents, and (3) these jailbreaks enable coherent and malicious multi-step agent behavior and retain model capabilities."
- 한계·반박: 2024-10~2025-04 시점 모델 기준 🕒. 어떤 모델이 얼마나 순응적이었는지의 개별 수치는 초록에 없다 — 인용하지 말 것.

---

# 축 5. 실행환경·비용 (있는 만큼만)

## Firecracker: Lightweight Virtualization for Serverless Applications
- 저자·연도: Alexandru Agache; Marc Brooker; Andreea Florescu; Alexandra Iordache; Anthony Liguori; Rolf Neugebauer; Phil Piwonka; Diana-Maria Popa (Amazon Web Services, 2020)
- 출처: **17th USENIX Symposium on Networked Systems Design and Implementation (NSDI '20)**, February 25–27, 2020, Santa Clara, CA (논문 PDF에서 직접 확인). arXiv 논문 아님.
- URL: https://www.usenix.org/conference/nsdi20/presentation/agache (PDF: https://www.usenix.org/system/files/nsdi20-paper-agache.pdf)
- 발행일: 2020-02 (NSDI '20 proceedings)
- 축 태그: [축 5]
- 한 줄 요지: "강한 보안 = 높은 오버헤드(VM), 낮은 오버헤드 = 약한 보안(컨테이너)"라는 전통적 트레이드오프를 거부하고, 서버리스에 특화한 microVM 모니터로 둘을 동시에 얻는다.
- 실무자에게 의미하는 것: 에이전트가 생성한 코드를 실행해야 하는 순간(코드 인터프리터, 자동 스크립트 실행) 격리 선택지의 근거가 된다. 핵심 함의는 **VM 격리가 "너무 느려서 못 쓴다"는 통념이 이미 낡았다**는 것이다 — 125ms 부팅과 5MB 오버헤드면 요청당 하나씩 띄우는 것이 현실적이다. 그래서 신뢰할 수 없는 코드를 컨테이너에서 돌리는 결정을 "성능상 어쩔 수 없었다"로 정당화할 수 없다. 그리고 이 논문이 보여주는 설계 방법론도 배울 게 있다 — **기능을 덜어냄으로써**(BIOS 없음, 임의 커널 부팅 없음, PCI·레거시 장치 에뮬레이션 없음, VM 마이그레이션 없음) 공격면과 오버헤드를 함께 줄였다. 에이전트 샌드박스 설계도 같은 방향이어야 한다: 도구를 더하는 게 아니라 덜어내는 것이 보안이다.
- 인용 가능한 구절·수치 [본문 확인]: "With the provided minimal Linux guest kernel configuration, it offers memory overhead of less than 5MB per container, boots to application code in less than 125ms, and allows creation of up to 150 MicroVMs per second per host." (§1 Introduction) / "The traditional view is that there is a choice between virtualization with strong security and high overhead, and container technologies with weaker security and minimal overhead. This tradeoff is unacceptable to public infrastructure providers, who need both strong security and minimal overhead." (Abstract) / "It does not offer a BIOS, cannot boot arbitrary kernels, does not emulate legacy devices nor PCI, and does not support VM migration." (§1.1 "Specialization" — 직전 절 제목을 PDF 텍스트에서 확인)
- 한계·반박: 2020년 논문이고 대상이 AWS Lambda/Fargate 워크로드다 🕒 — LLM 에이전트 샌드박스에 대한 직접 측정이 아니다. **에이전트용 격리 성능 수치로 제시하면 과잉 일반화**이고, "microVM 격리의 비용이 이 정도 규모다"라는 참조점으로만 써야 한다.

---

# 실무 결론 요약 (챕터 저술용)

논문 38편에서 반복적으로 수렴하는 설계 원칙 6개다. 각각을 뒷받침하는 논문이 서로 다른 축에서 나왔다는 점이 이 원칙들의 강도다.

1. **검증기 없는 루프는 넣지 마라.** 리플렉션·트리 탐색·멀티에이전트 토론이 효과를 본 사례에는 전부 값싼 외부 판정 신호가 있었다. 없는 경우 성능이 떨어지기도 한다. (근거: Huang et al. 2310.01798 / ToT 2305.10601 / MAST 2503.13657의 "task verification" 실패 범주)
2. **정확도만 보고하지 마라 — 비용과 분산을 함께 보라.** (근거: AI Agents That Matter 2407.01502 / τ-bench의 pass^k 2406.12045)
3. **채점기를 먼저 감사하라.** 벤치마크 결함의 상당수는 모델이 아니라 보상 설계에 있었고, 점수를 3배까지 왜곡했다. (근거: SWE-Bench+ 2410.06992 / ABC 2507.02825)
4. **judge를 쓰면 순서를 무작위화하고 심판과 피심판을 분리하라.** (근거: 2305.17926 / 2404.13076 / MT-Bench 2306.05685가 자체 인정한 편향 목록)
5. **인젝션 방어는 프롬프트가 아니라 권한에서 시작하라.** 가장 효과가 컸던 단순 방어는 도구 노출 최소화였고, 모델을 키우는 것은 오히려 역효과 경향이 있었다. (근거: AgentDojo 2406.13352 / CaMeL 2503.18813 / AgentHarm 2410.09024)
6. **컨텍스트는 크기가 아니라 배치와 예산의 문제다.** 검색과 롱 컨텍스트는 대체재가 아니고, 청크를 더 넣는 것은 어느 지점부터 해가 된다. (근거: 2310.03025 / 2409.01666 / Lost in the Middle 2307.03172)

---

# 수집 한계

1. **축별 배분은 의도적으로 불균등하다.** 총 **38편**. 브리프의 우선순위(축 4 평가 방법론이 최우선, 축 5는 있는 만큼만)에 따라 축 4에 18편(평가 12 + 안전성 6), 축 1에 13편, 축 3에 6편, 축 5에 1편을 배정했다. 축 5는 LLM 에이전트 특화 비용·지연 연구를 학술 소스에서 충분히 확보하지 못했다 — 아래 "커버 못 한 영역" 참조.

2. **수치는 대부분 초록 기준이다.** 본문(HTML/PDF)까지 내려가 원문 문장을 확인한 것은 AgentDojo(arXiv:2406.13352v3)와 Firecracker(NSDI '20) 두 편뿐이다. 나머지는 초록에 명시된 수치만 인용했고, 초록에 없는 수치는 아예 적지 않았다. 각 항목의 `[초록 확인]`/`[본문 확인]` 표시로 구분했다.

3. **발표처(학회·저널)를 확인하지 못한 논문이 많다.** arXiv 메타데이터의 `journal_ref`/`comment`에 명시된 경우만 적었고, 나머지는 `발표처 미확인`으로 남겼다. 통념상 유명한 학회 발표 논문(예: ReAct, Toolformer)도 메타에 없으면 미확인으로 처리했다. **"~에서 발표된"이라는 서술을 쓰려면 fact-checker가 별도 확인해야 한다.**

4. **모델 세대 경과 위험이 크다.** 🕒 표시한 항목의 벤치마크 절대 수치는 GPT-4/Claude 2/Llama 2 세대 기준이다. 검색 시점은 2026-07-25이므로, 이 수치들을 "현재 에이전트의 성능"으로 제시하면 사실 오류가 된다. 챕터에서는 반드시 "{논문 발행 시점} 기준" 또는 "이 논문 실험 당시" 같은 시점 한정어와 함께 써야 한다. **격차의 구조와 방법론적 교훈은 시간에 강건하지만, 절대 점수는 그렇지 않다.**

5. **arXiv 버전 의존성.** arXiv 논문의 수치는 리비전마다 바뀔 수 있다. 특히 AgentDojo는 v1→v3에서 Llama 구현 버그 수정이 있었다고 저자들이 comment에 명시했다. 모든 항목에 v1 발행일과 최신 리비전일을 함께 적었으므로, fact-checker는 인용 시 버전을 명시해야 한다.

6. **동료평가 지위를 확인하지 못한 논문에는 권위를 부여하지 않았다.** OP-RAG(2409.01666), CaMeL(2503.18813), Design Patterns(2506.08837) 등 발표처 미확인 논문은 "제안·관찰"로 인용하고 "확립된 결과"로 쓰지 않도록 각 항목의 한계 필드에 적어 두었다.

7. **비학술 소스는 의도적으로 제외했다.** dual-LLM 패턴이나 프롬프트 인젝션 초기 논의처럼 원 출처가 블로그인 내용은 이 문서에 넣지 않았다. 그 대신 같은 아이디어를 형식화한 동료평가/arXiv 논문(CaMeL, Design Patterns)으로 대체했다. 블로그 기반 자료는 web-researcher·community-researcher 담당이다.

8. **논문 수가 브리프 목표(15~30편)를 8편 초과한다(38편) — 의도된 초과이며 근거는 아래와 같다.** 1차 수집은 43편이었고, 가장 약한 5편을 실제로 덜어냈다: 서베이 3편(메모리 서베이 arXiv:2404.13501, 에이전트 지형도 서베이 arXiv:2309.07864, Agentic RAG 서베이 arXiv:2501.09136 — 모두 자체 실증 수치가 없고 스냅샷이 오래됨), AgentBench(arXiv:2308.03688 — 인용 가능한 유일한 수치가 LaTeX 매크로 미렌더링으로 사용 불가), RAG Best Practices(arXiv:2407.01219 — 구체 권장값이 전부 본문 미확인).
   30편까지 더 줄이지 **않은** 이유: 브리프 §3의 A~E가 명시적으로 요구하는 주제가 약 28개이고(ReAct·CoT와 그 비판·Reflexion 계열과 그 반박·Toolformer·ReWOO·tree-of-thought·MemGPT·멀티에이전트 양쪽·lost-in-the-middle·원조 RAG·ColBERT·GraphRAG·RAG vs 롱컨텍스트 양쪽·judge 방법론과 편향·에이전트 벤치마크 6종·벤치마크 타당성 비판·pass^k·인젝션 위협모델·설계 기반 방어 양쪽·AgentDojo류·탈옥·샌드박스), 여기에 "논쟁마다 양쪽 진영 배치"(6논쟁 × 2 = 12슬롯)를 더하면 30편 안에서 두 요구를 동시에 만족시킬 수 없다. **커버리지 요구를 우선했다.** 추가 축소가 필요하면 다음 순서를 권한다: OSWorld → GAIA → ColBERT. **논쟁 지도 12개 슬롯을 점유한 논문(총 24편)은 덜어내면 안 된다** — 덜어내면 논쟁이 한쪽 진영만 남아 이 문서의 핵심 기능이 무너진다.

## 커버 못 한 영역

- **에이전트 추론 비용·지연의 학술 분석 [축 5]:** 캐싱·배칭·KV 캐시 재사용의 에이전트 워크로드 특화 연구를 확보하지 못했다. 비용 관련 학술 근거는 현재 ReWOO(토큰 효율 5배)와 AI Agents That Matter(비용-정확도 공동 최적화 주장) 두 편에 의존한다. 이 축은 web-researcher의 1차 문서(프로바이더 프라이싱·프롬프트 캐싱 문서)로 메우는 게 적절하다.
- **샌드박스 격리의 에이전트 특화 성능·보안 연구 [축 5]:** Firecracker는 서버리스 대상 연구이지 에이전트 코드 실행 대상 연구가 아니다. gVisor 등 다른 격리 기술과의 정량 비교, 그리고 에이전트 워크로드에서의 측정은 확보하지 못했다.
- **평가 데이터 구축·라벨링 방법론 [축 4]:** rubric·체크리스트 기반 평가의 방법론 논문과 human preference와의 상관을 정량화한 연구를 별도로 확보하지 못했다. 현재는 MT-Bench의 80% 일치도와 LLM-as-a-Judge 서베이로 대체하고 있다.
- **오염(contamination) 탐지 방법론 자체:** SWE-Bench+가 보고한 "94% 이상이 지식 컷오프 이전 생성"이라는 데이터 유출 관찰은 확보했지만, 오염 탐지·정량화 방법론을 정면으로 다룬 논문은 넣지 못했다.
- **MetaGPT / ChatDev 계열 원논문:** 멀티에이전트 역할 분담 계열의 개별 시스템 논문은 시간 배분상 해석하지 않았다. 멀티에이전트 논쟁은 Du et al.(찬)과 MAST(반)로 구성했고, MAST가 7개 프레임워크를 포괄 분석하므로 개별 시스템 논문의 공백이 논쟁 구성을 훼손하지는 않는다. 필요하면 후속 보강 대상.
- **LLM+P, Plan-and-Solve, MCTS 결합 계열:** 계획 수립 계보에서 ReWOO와 ToT만 확보했다. 개별 계획 기법 논문은 추가하지 않았다 — 실무 독자에게는 "인터리빙 vs 선계획"의 구조적 대비(ReAct vs ReWOO)가 개별 기법 목록보다 유용하다고 판단했다.
- **하이브리드 검색(BM25 + 임베딩)·청킹 전략의 정량 비교:** 이 영역은 **공백이다.** *Searching for Best Practices in RAG*(arXiv:2407.01219v1, 2024-07-01)를 조합 탐색 자료로 확보했으나 구체 권장값(청킹 크기·리랭커 선택·임베딩 vs BM25)이 전부 본문 미확인이어서 최종 목록에서 제외했다. 청킹·하이브리드 검색의 정량 근거가 챕터에 필요하면 (a) 이 논문 본문을 확인하거나 (b) web-researcher가 확보한 1차 문서·엔지니어링 블로그로 메워야 한다. 현재 이 문서가 청킹에 대해 지지할 수 있는 정량 주장은 OP-RAG(2409.01666)의 역U자 곡선(청크 **수**에 관한 것이고 청크 **크기**에 관한 것이 아니다)뿐이다.
- **AgentBench(arXiv:2308.03688v3, ICLR 2024):** 브리프가 명시한 벤치마크 6종 중 하나지만 최종 목록에서 제외했다. 서지정보는 정상 해석됐으나 초록의 평가 모델 개수가 LaTeX 매크로(`\num`)로 미렌더링 상태라 인용 가능한 정량값이 없었다. 정성 발견("긴 지평 추론·의사결정·지시 따르기가 주된 장애물", "코드 학습의 효과가 태스크별로 엇갈림")은 인용 가치가 있으므로, 필요하면 arXiv:2308.03688v3 본문 확인 후 복원할 것.

# 미확인 항목 목록

fact-checker가 인용을 검증할 때 아래 항목은 **이 문서를 근거로 삼을 수 없다.** 각각 별도 확인이 필요하거나, 챕터에서 사용하지 않아야 한다.

| # | 항목 | 상태 | 조치 |
|---|---|---|---|
| 1 | ReAct(2210.03629)·Toolformer(2302.04761)·CoT(2201.11903)·Reflexion(2303.11366)·Self-Refine(2303.17651)·MemGPT(2310.08560) 등의 **발표 학회명** | arXiv 메타에 명시 없음 → 미확인 | "ICLR 2023에서 발표된 ReAct"처럼 쓰려면 별도 확인. 확인 못 하면 "arXiv:2210.03629"로만 인용 |
| 2 | GraphRAG(2404.16130)의 **인덱싱 비용 정량값** | 초록에 없음, 본문 미확인 | "GraphRAG는 N배 비싸다" 류 수치 인용 금지. 비용 구조(질의 시점 → 인덱스 구축 시점 이동)만 정성 서술 |
| 3 | *AI Agents That Matter*(2407.01502)의 **비용-정확도 파레토 구체 수치** | 초록에 없음, 본문 미확인 | 정성 주장(정확도만 보면 불필요하게 복잡·비싸진다)만 인용 |
| 4 | *Design Patterns for Securing LLM Agents*(2506.08837)의 **개별 패턴명·정의·효과 크기** | 초록에 없음, 본문 미확인 | 패턴 카탈로그가 존재한다는 사실만 인용. 수치가 필요하면 AgentDojo·CaMeL 사용 |
| 5 | AgentDojo(2406.13352v3) **Table 5의 방어별 ASR/유틸리티 쌍** | 본문 표에서 57.7%(±2.0)만 raw 텍스트로 교차 확인. 다른 셀 값은 미확인 | 표 값 인용 금지. 검증된 "도구 필터 → 7.5%"와 "Important message 57.7%(±2.0)"만 사용 |
| 5-a | **7.5% vs 6.84% 불일치 (주의)** | 본문 산문은 "lowering the attack success rate to **7.5%**"(grep으로 원문 확인). 1차 조사 때 요약 도구가 Table 5 값을 **6.84%(±2.0)**로 보고했으나 이 값은 원문 대조로 확인하지 못했다. 산문이 반올림했거나 표와 다른 부분집합을 집계했을 가능성이 있다 | **grep으로 검증된 산문 문장(7.5%)만 인용한다.** fact-checker가 이 논문에서 두 숫자를 발견하더라도 모순이 아니라 여기 기록된 기지의 미확인 사항이다 |
| 6 | ColBERT(2004.12832)의 **저장 공간 오버헤드** 수치 | 초록에 없음 | 인용 금지 |
| 7 | MemGPT(2310.08560)의 **정량 성능 비교 수치** | 초록에 요약되어 있지 않음 | 아키텍처 은유·설계 원리만 인용 |
| 8 | AgentHarm(2410.09024)의 **모델별 순응률 수치** | 초록에 없음 | 정성 발견 3개만 인용 |
| 9 | Firecracker의 **에이전트 워크로드 격리 성능** | 논문은 서버리스 대상. 에이전트 특화 측정 아님 | 참조점으로만 사용. "에이전트 샌드박스가 125ms에 뜬다"로 옮기면 사실 오류 |
| 10 | 🕒 표시 논문들의 **벤치마크 절대 수치가 2026-07 현재도 유효한지** | 전부 미확인 (모델 세대 경과) | 시점 한정어 필수. 현재 성능 주장 금지 |
