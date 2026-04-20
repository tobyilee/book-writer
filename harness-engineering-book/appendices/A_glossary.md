# 부록 A — 용어집

이 책은 용어가 촘촘한 편이다. 한 번 정의한 뒤 뒤 장에서 약어로 부르는 일이 잦으므로, 중간에 막히면 여기로 돌아오는 편이 낫다. 알파벳·가나다 순이 아니라 **주제별 묶음**으로 배치했다. 각 항목 끝의 `(→ N장)`은 본문에서 집중 다룬 장을 가리킨다.

## A. 하네스 구조 — 6-layer 교수법 어휘

이 여섯 어휘는 파일 이름이 아니라 관점의 이름이다. "6-layer 하네스를 쓰자"는 권고를 "파일 여섯 개 만들자"로 읽으면 관리 대상만 는다 (→ 1장, 3장).

- **GOAL** — 하네스가 보호하려는 최종 목표. "무엇을". `AGENTS.md` 상단 한두 줄.
- **RULE** — 목적을 지키기 위한 금지·강제 규칙. "어떻게 하지 말 것." 실패 한 건과 1:1 대응이 원칙.
- **Spec** — 입력/출력/성공·실패 기준. 테스트·타입·스키마로 흩어진다.
- **Drift** — 루프가 길어질수록 초기 지시에서 멀어지는 현상. 파일이 아니라 **측정 대상**.
- **Permission** — 도구·파일 접근 통제. Claude Code settings scope, Codex approval policy.
- **Knowledge** — 재사용 가능한 사실·레시피. Skills, memory bank, notepad.

## B. Karpathy 3요소

Karpathy `autoresearch` 레포에서 온 자가 점검 루브릭. 세 가지 모두 "예"가 나와야 하네스로 자동화할 후보다 (→ 1장, 4장).

- **Editable asset** — 에이전트가 수정 권한을 가진 **단 하나**의 파일/객체. 검색 공간을 해석 가능하게 유지하는 축.
- **Scalar metric** — 개선 여부를 판정할 **단일 숫자**. 인간 판단이 필요 없어야 한다.
- **Time-box** — 평가 사이클의 고정 길이. "5분 훈련 × 시간당 12실험 × 수면 중 100실험" 식의 경제학이 성립해야 한다.

## C. 루프 패턴

네 패턴의 공통 뼈대는 B절의 3요소, 차이는 "작업 유형이 패턴을 고른다"는 한 줄 (→ 4장).

- **Ralph Loop** — `while :; do cat PROMPT.md | claude-code; done`. PLAN/BUILD 분리 + back-pressure가 본체. Huntley의 표현은 무한 루프 찬미가 아니다.
- **ReAct** — Yao et al. 2022, arXiv:2210.03629. Thought → Action → Observation 인터리브.
- **Plan-and-Execute** — 계획 1회 + 실행 N회. LangChain이 대중화.
- **Reflexion** — Shinn et al. 2023, arXiv:2303.11366. 시도 → 자기 비평 → 에피소드 메모리 → 다음 시도.

## D. 운영 어휘

루프가 잘못되는 네 가지 모양과 그 통제 어휘. 이름이 붙어야 대처가 따라온다 (→ 4장, 6장).

- **Back-pressure** — 테스트·린터·타입체커가 루프에 걸어주는 되먹임 압력. LLM 자체 검증은 보조.
- **Exit hook** — 루프 종료 조건. `--max-iterations`, 토큰 상한, 델타 정체.
- **Guardrail** — 모델이 우회할 수 없는 외부 강제 레이어. Claude Code 훅의 `permissionDecision: "deny"`가 대표.
- **Completion promise** — 모델이 "완료"를 선언했는데 실제로는 바뀐 게 없거나 잘못된 상태. LLM 자체 판단을 신호로 쓰면 반복된다.
- **Overcooking** — scalar는 오르는데 품질이 퇴화하는 상태. 루프가 지표를 편법으로 올릴 우회로를 찾은 것.
- **Undercooking** — 반쪽 기능에서 조기 종료. exit hook이 성급히 발동한 결과.
- **Context pollution** — iteration이 갈수록 반응이 둔해지는 상태. Cline 50% 규칙 위반의 증상.

## E. 복합 시스템과 인터페이스

단일 모델 프롬프팅이 아니라 **시스템 설계**라는 관점을 만드는 어휘 (→ 1장, 5장, 8장).

- **Compound AI System** — Zaharia et al. 2024. 단일 모델이 아닌 여러 컴포넌트(RAG, 체인, 평가자, 라우터)가 결합된 시스템. SOTA 결과의 다수가 여기서 나온다.
- **ACI (Agent-Computer Interface)** — Yang et al. 2024, arXiv:2405.15793. "LM은 새로운 종류의 사용자"라는 선언. 사람용 shell/editor가 LM에겐 나쁜 UX일 수 있다.
- **Cascade** — Chen et al. 2023 FrugalGPT, arXiv:2305.05176. 싼 모델이 먼저 답하고, 신뢰도가 낮을 때만 비싼 모델로 승격하는 비용 절감 구조.
- **Test-time compute** — Snell et al. 2024, arXiv:2408.03314. 모델 크기가 아니라 **추론 시간에 배분되는 연산**이 품질을 이긴다는 주장. thinking 모드의 이론적 기반.

## F. 안전·거버넌스 어휘

방어를 모델 내부가 아니라 **아키텍처**로 옮기는 어휘 (→ 9장, 11장).

- **Managed policy** — Claude Code settings scope의 최상위. 조직 관리자가 배포하며 개별 사용자가 덮어쓸 수 없다.
- **Instruction Hierarchy** — Wallace et al. 2024, arXiv:2404.13208. system > developer > user > tool-output의 우선순위 훈련. 충돌 시 상위를 따르도록.
- **Channel separation (StruQ)** — Chen et al. 2024, arXiv:2402.06363. 지시와 데이터를 구조적으로 별도 채널에 실어 인젝션을 원천 차단하는 아키텍처.
- **AI Gateway** — Kong Engineering의 운영 패턴(확인 필요, 단일 출처). 모든 LLM 호출이 단일 프록시를 경유해 감사·rate limit·PII 리댁션을 일관 적용.
- **Indirect prompt injection** — Greshake et al. 2023, arXiv:2302.12173. 에이전트가 **읽게 될 자료**(위키·이슈·README)에 지시를 심어 실행을 유도하는 공격. 사용자 프롬프트를 건드리지 못해도 성립한다.

## G. 측정·회고 어휘

책의 마지막 자리에서 만나는 네 단어. Pareto 플롯이 그려지는 축, 그리고 그 축이 의심스러울 때 발동하는 신호 (→ 5장, 12장).

- **Pareto front (cost × accuracy)** — 5장이 의무화한 2축. 점 하나는 manual baseline, 또 하나는 본인이 구축한 하네스.
- **Intervention rate** — 사람이 루프를 멈추고 개입한 비율. Karpathy Partial Autonomy Slider의 실측 지표. 30%를 넘으면 그 하네스는 자율 시스템이 아니라 보조 도구다.
- **Pairwise-with-swap** — Zheng et al. 2023, arXiv:2306.05685. 같은 쌍을 A/B + B/A로 두 번 돌려 position bias를 감지하는 프로토콜. 불일치 판정은 폐기.
- **Skill-atrophy** — Anthropic 2025. AI 보조 참여자의 코드 이해도 17% 저하. 하네스를 잘 돌릴수록 개발자 본인에게 남는 것이 줄어든다는 세 번째 Contrarian evidence.
