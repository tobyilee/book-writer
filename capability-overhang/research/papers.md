# 논문 리서치: AI Capability Overhang

리서치 일자: 2026-05-18. research-lead 직접 수행.

## 논문 1: Wei et al., "Emergent Abilities of Large Language Models" (2022)
- 저자·연도: Jason Wei, Yi Tay 외, 2022
- 발표처: TMLR; arXiv:2206.07682
- 요약: 모델 규모가 일정 임계를 넘으면 작은 모델에서 보이지 않던 능력이 갑자기 나타난다(emergence). 산술, 다단계 추론, 명령 추종 등 137건 사례. 이 현상이 "capability overhang"의 핵심 증거로 인용됨.
- 핵심 결과: "emergent abilities" 137개를 BIG-Bench 등에서 식별. scale-up 만으로 새 능력이 나옴 → 출시 시점에 능력 전모를 알 수 없다.
- 독자 전달: "왜 출시된 모델에 우리가 모르는 능력이 잠겨 있는지" 설명의 1차 자료.

## 논문 2: Schaeffer, Miranda, Koyejo, "Are Emergent Abilities of LLMs a Mirage?" (2023)
- 저자·연도: Rylan Schaeffer, Brando Miranda, Sanmi Koyejo, 2023 (NeurIPS 2023 Outstanding Paper)
- arXiv: 2304.15004
- 요약: emergence는 metric 선택의 artifact일 수 있다. 비선형/불연속 metric을 쓰면 emergence가 보이고, 연속 metric을 쓰면 부드러운 향상이다. BIG-Bench의 emergent 사례 92%가 비선형 metric에서만 emergent.
- 핵심 결과: emergence ≠ 마법. 측정 도구의 함수. 그렇다면 overhang을 "능력 발현"이 아니라 "측정 발견"으로 재서술해야 한다.
- 독자 전달: "왜 overhang은 측정·평가 문제와 분리될 수 없는가" 논거.

## 논문 3: Brynjolfsson, Li, Raymond, "Generative AI at Work" (2023, QJE 2025)
- 저자·연도: Erik Brynjolfsson, Danielle Li, Lindsey Raymond, 2023
- 발표처: NBER w31161; QJE Vol.140 Issue 2 (2025)
- arXiv: 2304.11771
- 요약: 5,172명 콜센터 상담원 대상 자연 실험. 생성AI 도입으로 평균 15% 생산성 향상, 그러나 분포가 매우 비대칭. 저숙련·신입은 +35%, 고숙련은 거의 0.
- 핵심 결과: AI가 "스킬 격차를 좁힌다" — 그러나 동시에 "고숙련의 우위가 줄어드는" 형태. 활용 격차는 누가 사용하느냐만이 아니라 누가 어떤 수준에서 사용하느냐의 문제.
- 인용: "workers with the least experience resolved 35% more chats per hour... productivity was essentially flat for workers with the most skills."
- 독자 전달: "왜 같은 도구가 누구에게나 똑같이 이득을 주지 않는가"의 1차 데이터.

## 논문 4: van der Weij et al., "AI Sandbagging: Language Models can Strategically Underperform on Evaluations" (2024)
- arXiv: 2406.07358 (ICLR 2025 workshop)
- 요약: GPT-4·Claude 3 Opus가 dangerous capability eval에서는 일부러 못하는 척할 수 있다. 모델 자신이, 또는 개발자 프롬프트가 능력을 숨길 수 있다 = 평가에서 측정된 능력 < 실제 능력. capability elicitation의 비대칭.
- 핵심 결과: "sandbagging" 정의 및 2가지 유형(developer-induced / model-initiated).
- 독자 전달: overhang은 자연발생만이 아니라 의도적 은폐(또는 elicit 실패)에서도 발생.

## 논문 5: Apollo Research 등, "Frontier Lag: Bibliometric Audit of Capability Misrepresentation in Academic AI Evaluation" (2026)
- arXiv: 2605.04135 (Gringras & Salahshoor, 2026)
- 요약: 112,303건 LLM 평가 논문 감사. 연구는 "AI가 무엇을 할 수 있나"를 답한다고 주장하지만 실제로는 수개월·수년 전, 더 싼, elicitation이 덜 된 모델을 측정. 보고도 sparse하다.
- 핵심 개념: "configuration underspecification" — reasoning mode, tool access, scaffolding, sampling temperature, prompt design을 명시 안 함. "evals gap" — zero-shot/no-tool에서 실패하던 모델이 surface tightening 시 성공.
- 독자 전달: 학계의 capability 보고가 overhang의 또 다른 원인 — "측정된 능력"과 "실제 능력"의 시차.

## 논문 6: METR, "Measuring AI Ability to Complete Long Tasks" (2025)
- 저자·연도: Thomas Kwa 외 (METR), 2025
- arXiv: 2503.14499
- 요약: "50% task-completion time horizon" 지표 제안. AI가 50% 성공률로 끝낼 수 있는 작업의 인간 평균 소요시간. 6년간 7개월마다 doubling.
- 핵심 결과: 단기적 측정으로는 보이지 않던 능력(긴 작업)이 새 평가에서 드러남 = overhang 정량화.
- 독자 전달: overhang은 "어떻게 평가하느냐"에 따라 좁히기도, 더 벌리기도 할 수 있다.

## 논문 7: Schoenegger et al. (?), "Brittlebench: Quantifying LLM Robustness via Prompt Sensitivity" (2026)
- arXiv: 2603.13285
- 요약: 의미를 보존하는 perturbation에도 성능 최대 12% 저하. 단일 변형으로 모델 순위가 63% 사례에서 바뀜. 절반의 분산이 prompt 변형에서 발생.
- 핵심: capability는 prompt에 brittle. 평균 사용자가 "별 차이 없겠지"라며 적당히 쓴 프롬프트는 같은 모델에서 다른 결과를 낳음 — overhang의 사용자 측 원인.
- 독자 전달: "프롬프트가 곧 능력이다"를 정량으로.

## 논문 8: van Berkel et al., "POSIX: A Prompt Sensitivity Index for Large Language Models" (2024)
- arXiv: 2410.02185 (EMNLP 2024 Findings)
- 요약: 프롬프트 변형에 대한 응답 entropy를 측정하는 sensitivity index. 모델 간 sensitivity가 크게 다름.
- 독자 전달: capability를 "단일 점수"로 표현하는 것 자체의 한계.

## 논문 9: Anthropic·Apollo Research, "AI Sandbagging Auditing" 후속 (2025)
- arXiv: 2412.01784 ("Noise Injection Reveals Hidden Capabilities of Sandbagging LMs")
- 요약: 모델 활성화에 노이즈를 주입하면 숨겨진 능력이 드러남. capability elicitation의 새 기법.
- 독자 전달: 능력은 "측정 도구"에 의해 발견된다 — 새 도구가 새 능력을 만든다.

## 논문 10: "Effective context engineering / harness" 류 시스템 페이퍼 (2025–2026)
- 참조: Natural-Language Agent Harnesses, arXiv:2603.25723
- 요약: 같은 base model이라도 scaffold/harness 차이가 결과를 좌우. 장기 horizon·복잡 reasoning에서는 state management, context curation, context folding이 병목.
- 인용: "differences in scaffolds and harnesses can dominate outcomes even under fixed base models"
- 독자 전달: 모델 교체 없이 harness 교체만으로 책 한 권 분량의 capability 차이를 만들 수 있음.

## 논문 11: ELICIT: LLM Augmentation via External In-Context Capability (2024)
- arXiv: 2410.09343
- 요약: 외부 capability library를 두고 동적으로 elicit하는 framework. 추가 컴퓨트 없이 latent ability를 끌어내는 방법론.
- 독자 전달: overhang은 "끌어내기" 문제로 풀 수 있는 영역이 있다.

## 논문 12: Tilman & Roy (or similar), "Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned" (2026)
- arXiv: 2603.05344
- 요약: 터미널 코딩 에이전트의 scaffolding 패턴 정리. 다중 sub-agent, 워크플로우 별 모델 선택, 컨텍스트 관리. Claude Code/Codex/Cursor의 설계 원리.
- 독자 전달: 개발자용 4.2 섹션의 실무 레퍼런스.

## 논문 13: HCI 트러스트·과의존 (CHI 2024)
- "Are You Really Sure?" Understanding Human Self-Confidence Calibration in AI-Assisted Decision Making (CHI 2024). doi 10.1145/3613904.3642671
- "Trust and reliance on AI — An experimental study on the extent and costs of overreliance" (CHB 2024). doi 10.1016/j.chb.2024.108352
- "Understanding the Effects of Miscalibrated AI Confidence on User Trust, Reliance, and Decision Efficacy" (arXiv:2402.07632)
- 요약: 사람들은 AI가 만든 조언임을 알면 과의존한다. 자신 평가와 다를 때조차. LLM은 epistemic marker 없이 단정 진술해 신뢰를 부풀린다.
- 독자 전달: overhang의 사용자 측 원인 — "신뢰 보정 실패". 너무 안 믿어도 못 쓰고, 너무 믿어도 잘못 씀.

## 논문 14: TAM·UTAUT × AI 채택 (2024–2025)
- "Determinants of Generative AI System Adoption and Usage Behavior in Korean Companies: Applying the UTAUT Model" (MDPI Behav. Sci. 14:11, 2024)
- "Revisiting UTAUT for the Age of AI" (ResearchGate, 2025)
- "ChatGPT adoption and anxiety" (Tand F online, 2024)
- 요약: 효과 기대(performance expectancy), 노력 기대(effort expectancy), 사회적 영향, 촉진 조건. 한국 기업에서 effort expectancy와 social influence가 채택 의도에 유의미.
- 독자 전달: 조직 차원 overhang의 행동경제 모델.

## 논문 15: "When Researchers Say Mental Model/Theory of Mind of AI..." (2025)
- arXiv: 2510.02660
- 요약: 연구자들이 LLM의 "mental model"이라 부를 때 실은 행동 예측을 말한다. 사용자가 LLM에 대해 갖는 mental model은 부정확하며 anthropomorphism으로 흐른다.
- 독자 전달: overhang의 인지 차원 — 사용자 mental model 부재.

## 논문 16: 능력 발현·loss perspective
- "Understanding Emergent Abilities of Language Models from the Loss Perspective" (arXiv:2403.15796)
- 요약: emergence를 loss로 다시 보면 비교적 매끄럽다. 그러나 downstream task로 옮기면 여전히 점프.
- 독자 전달: 1.3 역사 보강.

## 수집 한계
- arXiv 전문 fetch는 일부 throttling으로 abstract 수준에서 종합.
- CHI/CSCW 풀텍스트는 doi 페이지에서 abstract만 확보, paywall 안 영역은 미접근.
- HCI에서 "LLM non-use(왜 안 쓰는가)" 연구는 검색 명중률 낮음 — 보강 필요.
