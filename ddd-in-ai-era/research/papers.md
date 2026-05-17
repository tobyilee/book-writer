# 논문 리서치: AI 에이전틱 코딩 시대의 DDD

> 수집 기간: 2026-05-17
> 수집자: research-lead (paper 갈래)
> 대상 독자: DDD를 알고 AI 코딩 도구를 도입 중인 시니어 개발자·테크 리드·아키텍트

## 논문 1: Automating Domain-Driven Design — Experience with a Prompting Framework

- 저자·연도: Tobias Eisenreich, Husein Jusic, Stefan Wagner, 2026
- arXiv: 2603.26244
- 요약 (3~5문장):
  DDD 활동을 LLM 프롬프팅으로 자동화하는 프레임워크를 제안하고, 실제 기업(FTAPI) 요구사항으로 검증한다. DDD를 다섯 단계로 분해: (1) ubiquitous language 수립, (2) event storming 시뮬레이션, (3) bounded context 식별, (4) aggregate 설계, (5) 기술 아키텍처 매핑. 1-3 단계는 실용적 산출물(용어집, 컨텍스트 맵)을 안정적으로 만들었지만, 4-5 단계는 앞 단계의 오류가 누적·증폭되어 실용성이 떨어졌다. 결론: 프레임워크는 "협업하는 sparring partner"로 우수하지만, 아키텍처 전문성을 **대체할 수 없고 보강한다.**
- 핵심 수치·결과:
  - DDD 5단계 중 처음 3단계는 신뢰성 있게 작동, 뒷 2단계는 누적 오류로 실패.
- 인용할 만한 문장:
  - "Later steps show how minor errors or inaccuracies can propagate and accumulate."
  - "LLMs can enhance, but not replace, architectural expertise."
- 독자에게 어떻게 전달할지 제안: "AI가 ubiquitous language·event storming까지는 함께 굴려준다. 그 위에 사람이 aggregate를 책임진다"는 분업 경계의 실증 근거로 인용.

## 논문 2: Leveraging Generative AI for Enhancing Domain-Driven Software Design

- 저자·연도: Götz-Henrik Wiegand, Filip Stepniak, Patrick Baier, 2026
- arXiv: 2601.20909 (Proceedings of the Upper-Rhine Artificial Intelligence Symposium 2024)
- 요약 (3~5문장):
  도메인 메타모델 생성을 부분 자동화하기 위해 생성형 AI(특히 도메인 특화 JSON 산출)를 활용한다. Code Llama를 4-bit 양자화 + LoRA로 컨슈머 GPU에서 fine-tune했다. 단순 프롬프트로 구문적으로 정확한 JSON 객체를 일관되게 생성, post-processing이 거의 필요 없었다. 자원 제약 환경에서도 DDD 워크플로에 통합 가능함을 보여준 사례.
- 핵심 수치·결과:
  - 컨슈머 GPU + 4-bit quantization으로도 "high performance, minimal post-processing" 달성.
- 인용할 만한 문장:
  - "AI-driven automation can improve efficiency and reduce resource requirements in software design while maintaining practical usability."
- 독자에게 어떻게 전달할지 제안: "도메인 메타모델 같은 정형 산출물은 LLM이 잘한다" — tactical pattern 일부 자동화 사례 제시용.

## 논문 3: Domain-Driven Design in Software Development — A Systematic Literature Review on Implementation, Challenges, and Effectiveness

- 저자·연도: Ozan Özkan, Önder Babur, Mark van den Brand, 2023
- arXiv: 2310.01905
- 요약 (3~5문장):
  2006-2023 동안의 36편 동료 평가 논문을 분석한 systematic review. 학계 58.3%, 산업 36.1%, 협업 5.6%. 마이크로서비스 적용 사례가 44%로 1위. DDD가 microservices 환경에서 모듈성·유지보수성·확장성 개선에 효과적이었음을 정량적으로 보여주지만, 9가지 주요 implementation 장애물도 명확히 식별. 17편이 평가 지표를 보고하지 않음 — DDD 효과성에 대한 정량적 근거가 여전히 부족.
- 핵심 수치·결과:
  - 36편 중 마이크로서비스가 44%
  - 17편이 평가 지표 없음 (47%)
  - 9가지 implementation 장애물: 설계 복잡성 관리, 최적 마이크로서비스 경계 식별, 도메인 모델 복잡성, 프레임워크 통합 난점, 비즈니스-기술 간 커뮤니케이션 갭, model-code gap, 개발자 경험·온보딩 영향, 논쟁적 기술 토론, 도메인 전문가 부족.
- 인용할 만한 문장:
  - "DDD has effectively improved software systems, with its key concepts."
  - "Practical adoption demands empirical validation, stakeholder collaboration, and stronger academic-industry partnerships."
- 독자에게 어떻게 전달할지 제안: AI 이전부터 DDD가 안고 있던 9개 장애물을 보여주고, AI가 어느 장애를 해결/완화하고 어느 장애는 그대로 두는지 매핑하는 데 활용.

## 논문 4: LLM-Based Multi-Agent Systems for Software Engineering — Literature Review, Vision and the Road Ahead

- 저자·연도: Junda He, Christoph Treude, David Lo, 2024 (v4: 2025)
- arXiv: 2404.04834
- 요약 (3~5문장):
  LLM 기반 멀티 에이전트 시스템(LMA)을 소프트웨어 개발 라이프사이클 단계(요구사항, 코드 생성, QA, 유지보수, 엔드투엔드)별로 분류한 서베이. 멀티 에이전트의 효용: 전문화, 협업 패턴, iterative refinement, workflow 통합. 단일 에이전트 대비 출력 품질 개선을 보고. 후속 연구 과제로 "현재 LMA 시스템은 DDD·BDD·Team Topologies 같은 전문화된 실천법을 충분히 활용하지 못한다"고 명시 — 즉 DDD 통합은 **미개척 영역**.
- 핵심 수치·결과:
  - 단일 에이전트 대비 멀티 에이전트가 정성적 품질 우위 (다수 case study)
- 인용할 만한 문장:
  - "Current LMA systems often do not leverage specialized practices like Domain-Driven Design, Behavior-Driven Development, and Team Topologies." (서베이의 미래 연구 방향)
- 독자에게 어떻게 전달할지 제안: 학계조차 "DDD를 멀티 에이전트에 못 붙이고 있다"고 인정한다는 지점은, 실무자에게 "지금이 차별화 기회"로 읽을 만한 근거.

## 논문 5: An LLM-Assisted Approach to Designing Software Architectures Using ADD

- 저자·연도: 2025 (저자명 미상, arXiv:2506.22688)
- arXiv: 2506.22688
- 요약 (3~5문장):
  Attribute-Driven Design(ADD) 방법론을 LLM이 보조하는 접근. 아키텍트의 의사결정 과정에 LLM을 단계별로 끼워 넣는 패턴 제시. DDD와 직접 매핑되지는 않지만, 동일한 "방법론 + LLM 보조" 패턴의 또 다른 사례.
- 핵심 수치·결과: (상세 미수집)
- 인용할 만한 문장: "LLM-assisted approach to design software architectures."
- 독자에게 어떻게 전달할지 제안: DDD 외에도 같은 패턴이 등장한다는 점에서 "방법론 + AI 보조"의 일반 트렌드 근거.

## 논문 6: Agentic Artificial Intelligence (AI) — Architectures, Taxonomies, and Evaluation of Large Language Model Agents

- 저자·연도: 2026
- arXiv: 2601.12560
- 요약 (3~5문장):
  멀티 에이전트 시스템의 상호작용 패턴(chain, star, mesh, workflow graph)을 분류. CAMEL, AutoGen, MetaGPT, LangGraph, Swarm, MAKER 같은 프레임워크를 비교. CLASSic 평가 차원(cost, latency, accuracy, security, stability)을 제시. DDD 직접 언급은 없지만, 멀티 에이전트 토폴로지는 결국 context map의 한 형태로 해석 가능.
- 인용할 만한 문장: "Places evaluation directly in the architectural space."
- 독자에게 어떻게 전달할지 제안: "에이전트 topology = bounded context 간 context map"이라는 책의 주장을 받쳐주는 근거.

## 논문 7: Agent Skills for Large Language Models — Architecture, Acquisition, Security, and the Path Forward

- 저자·연도: 2026
- arXiv: 2602.12430
- 요약 (3~5문장):
  monolithic LM → modular, skill-equipped agents 전환을 추적. agent skill은 instruction·code·resource의 조합 패키지. 4축: 아키텍처 기반, 스킬 습득, 배포·스케일, 보안. 커뮤니티 기여 스킬 중 **26.1%가 보안 취약점 보유** — 무분별한 스킬 조립의 위험.
- 핵심 수치·결과: 커뮤니티 스킬의 26.1%에 취약점.
- 인용할 만한 문장: "Composable packages of instructions, code, and resources that agents load on demand."
- 독자에게 어떻게 전달할지 제안: "에이전트 스킬도 결국 bounded context의 모듈화" — 그리고 거버넌스·보안 책임이 어느 때보다 커진다는 경고.

## 논문 8: Large Language Model Agent — A Survey on Methodology, Applications and Challenges

- 저자·연도: 2025-03
- arXiv: 2503.21460
- 요약 (3~5문장):
  LLM 에이전트의 아키텍처 기반, 협업 메커니즘, 진화 경로를 methodology-centric taxonomy로 정리. 응용 영역과 미해결 도전(평가, 안전, 일반화)을 정리.
- 인용할 만한 문장: "Systematically deconstructs LLM agent systems through a methodology-centered taxonomy."
- 독자에게 어떻게 전달할지 제안: 멀티 에이전트 협업 메커니즘이 DDD의 context mapping 패턴(Customer-Supplier, ACL, Conformist 등)과 자연 매칭됨을 풀어내는 데 인용.

## 논문 9: A Layered Architecture for Developing and Enhancing Capabilities in LLM-Based Software Systems

- 저자·연도: 2024-11
- arXiv: 2411.12357
- 요약 (3~5문장):
  LLM 기반 소프트웨어 시스템 개발을 distinct layer로 조직. capability를 layer에 align하면 효과적·효율적 구현이 가능. Hexagonal/Clean Architecture가 도메인 계층을 격리하는 것과 유사한 사고.
- 인용할 만한 문장: "A layered architecture that organizes LLM software system development into distinct layers."
- 독자에게 어떻게 전달할지 제안: AI 시스템에도 hexagonal/clean-style layering이 적용된다는 점에서 DDD tactical pattern의 보편성 증거.

## 논문 10: Guidelines for Empirical Studies in Software Engineering Involving Large Language Models

- 저자·연도: 2026-03
- arXiv: 2508.15503
- 요약 (3~5문장):
  LLM이 관여하는 SE 연구의 7가지 유형 taxonomy + 8가지 가이드라인. requirement vs recommended practice 구분. 이 분야의 실증 연구가 무엇을 측정해야 하는지를 형식화.
- 인용할 만한 문장: "Eight guidelines for designing and reporting such studies."
- 독자에게 어떻게 전달할지 제안: "AI 코딩 도구의 효과를 측정하려면 어떻게 해야 하나?" 질문에 학계 기준을 인용.

## 논문 11: A Survey on Code Generation with LLM-Based Agents

- 저자·연도: 2025
- arXiv: 2508.00083
- 요약 (3~5문장):
  2022-2025년 6월까지의 LLM 기반 코드 생성 에이전트 시스템적 서베이. 평가 벤치마크, 협업 패턴, 메모리 메커니즘, 도구 사용을 분류.
- 독자에게 어떻게 전달할지 제안: "AI 코딩 에이전트의 현재 지형"을 한 페이지로 보여줄 때 인용.

## 논문 12: LLM-Based Zero-shot Triple Extraction for Automated Ontology Generation from Software Engineering Standards

- 저자·연도: 2025
- arXiv: 2509.00140
- 요약 (3~5문장):
  소프트웨어 엔지니어링 표준 문서에서 LLM이 zero-shot으로 triple을 추출해 ontology를 자동 생성하는 워크플로. 도메인 용어 추출, 관계 추론, 정규화, cross-section alignment.
- 독자에게 어떻게 전달할지 제안: ubiquitous language를 LLM이 **자동으로 뽑아내는** 시대가 실증 단계에 들어섰음을 보여주는 사례.

---

## 리서치 한계 (논문 갈래)

- DDD와 AI 에이전틱 코딩의 **정량적 효과 비교 실험**은 아직 매우 빈약하다. Eisenreich et al.(2026)이 가장 직접적이지만 단일 기업 케이스.
- 한국어 학술 자료 — KCI/DBpia 검색은 별도로 수행하지 못함. 책 저술 시 "국내 학술 자료 미수집"을 한계로 명시할 필요.
- Eric Evans, Vaughn Vernon의 최근 학술 발표는 InfoQ 인터뷰·키노트 형태가 주류이고, peer-reviewed 논문은 없음.
