# 보완 리서치 ④ — 거버넌스·Red-teaming·입출력 안전 도구

> **목적:** 9장 거버넌스 절 1차 자료 **3건 확보**가 집필 제출 조건. 입력 필터 / 출력 감사·red-team / 평가 하네스 / 한국 사례 4축으로 정리.
> **범위:** 공식 문서 + 도구당 1~2개 보충 블로그. 각 도구는 **(a) 어떤 문제 / (b) 통합 형태 / (c) 한 줄 권장 시점** 세 필드로 통일.
> **수집 시점:** 2026-04-17
> **소스 태그:** `[docs:벤더]`, `[repo:조직]`, `[blog:매체]`

---

## 1. 입력 필터 (Input Filters)

사용자 입력이 LLM에 도달하기 **전에** 차단·태깅하는 층. prompt injection·jailbreak·PII 사전 탐지가 주업.

### 1.1 Microsoft Azure Prompt Shields (구 Jailbreak risk detection)

- **출처:** 
  - Concept: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection (Microsoft Learn, 2025-11-21 갱신)
  - Azure Blog: https://azure.microsoft.com/en-us/blog/enhance-ai-security-with-azure-prompt-shields-and-azure-ai-content-safety/
- **(a) 해결하는 문제:**
  - **User Prompt Attacks** — 사용자가 의도적으로 시스템 프롬프트 우회, RLHF 훈련 무효화 시도.
    - 4 하위 유형: 시스템 규칙 변경 시도 / 대화 모조(mockup) 삽입 / 롤플레이 인격 교체 / 인코딩 공격(Base64·암호화).
  - **Document Attacks (간접 프롬프트 인젝션)** — 제3자가 외부 문서·이메일·웹페이지에 숨긴 지시문으로 LLM 세션 탈취.
    - 9 하위 유형: 콘텐츠 조작, 권한 상승, 정보 수집, 가용성 차단, 사기, 악성코드 전파 등.
  - **2025년 Microsoft Build: Spotlighting** — 신뢰/비신뢰 입력을 구분해 간접 인젝션을 더 강하게 차단.
- **(b) 통합 형태:**
  - **HTTP API (Unified API)** — Azure AI Content Safety 리소스로 생성. `POST /contentsafety/text:shieldPrompt` 계열 엔드포인트.
  - Azure OpenAI 콘텐츠 필터와 자동 통합 가능.
  - Python/C#/JS SDK 존재.
  - 실시간(real-time) GA 상태.
- **(c) 한 줄 권장 시점:**
  > Azure를 이미 쓰고 있고, **사용자 입력 + 외부 문서(RAG 소스)** 양쪽에서 들어오는 인젝션을 한 API로 막고 싶을 때.
- **한계:** 주요 언어 8개(영/중/불/독/스페인/이/일/포). 한국어는 공식 훈련 대상 아님 — 국내 서비스는 별도 검증 필요.

### 1.2 Meta Llama Guard (3 / 4)

- **출처:**
  - Repo: https://github.com/meta-llama/PurpleLlama
  - Model cards: `.../Llama-Guard3/8B/MODEL_CARD.md`, `.../Llama-Guard-4-12B` (HuggingFace)
  - Paper: "Llama Guard: LLM-based Input-Output Safeguard" (Meta AI 2023)
- **(a) 해결하는 문제:**
  - **LLM 입력·출력 양방향 분류.** 프롬프트 또는 응답을 받아 safe / unsafe 판정, unsafe면 어떤 카테고리인지 출력.
  - **14개 위험 카테고리** (MLCommons 표준 해저드 분류):
    - S1~S4: 폭력·비폭력 범죄, 성범죄, 아동 착취
    - S5~S8: 명예훼손, 전문 조언 남용, 프라이버시, IP 침해
    - S9~S13: 무기, 혐오표현, 자해, 성적 콘텐츠, 선거
    - S14: 코드 인터프리터 남용
  - Llama Guard 3는 8개 언어 (영/불/독/힌디/이/포/스페인/태국) — **한국어 공식 지원 없음**.
- **(b) 통합 형태:**
  - **HuggingFace Transformers 모델** — 8B, 12B, 11B-Vision 체크포인트. int8 양자화 호환.
  - Llama 3.1 레퍼런스 구현에 기본 포함.
  - Llama Recipes (GitHub) 참고 구성.
- **(c) 한 줄 권장 시점:**
  > 온프렘·프라이빗 환경에서 **입출력 양쪽을 자체 모델로 분류**하고 싶고, MLCommons 분류체계로 감사 로그를 남겨야 할 때.

### 1.3 Rebuff (protectai/rebuff)

- **출처:** https://github.com/protectai/rebuff · LangChain 블로그: https://blog.langchain.com/rebuff/
- **(a) 해결하는 문제:**
  - **프롬프트 인젝션 전용** 탐지. 4계층 방어:
    1. **Heuristics** — 규칙 기반 패턴 매칭.
    2. **LLM-based detection** — LLM이 메타 프롬프트로 판정.
    3. **Vector DB** — 과거 공격 임베딩 저장·재식별.
    4. **Canary tokens** — 시스템 프롬프트 유출 탐지.
- **(b) 통합 형태:**
  - **Python SDK** `pip install rebuff`, `RebuffSdk` 클래스.
  - **JavaScript SDK** 별도 제공.
  - 자체 호스팅 서버(Node.js + Supabase + Pinecone/Chroma + OpenAI).
  - 신 Python SDK는 Playground API 의존 제거, 완전 로컬 실행.
- **(c) 한 줄 권장 시점:**
  > Python/JS 애플리케이션에 **가볍게 인젝션 탐지만** 달고 싶을 때, 그리고 카나리 토큰으로 시스템 프롬프트 유출까지 감시하고 싶을 때.
- **한계:** **2025-05-16 아카이브 (read-only)**. 자체 명시: "100% 보호는 불가능". 적극 유지보수되는 프로젝트가 아니므로 9장에서는 "참고용 레퍼런스"로 소개하되 **프로덕션 채택은 PyRIT/Promptfoo/Prompt Shields 선호** 권장.

---

## 2. 출력 감사 · Red-teaming

### 2.1 NVIDIA garak — LLM 취약점 스캐너

- **출처:** https://github.com/NVIDIA/garak · https://garak.ai · arXiv 2406.11036 · Databricks 블로그: https://www.databricks.com/blog/ai-security-action-applying-nvidias-garak-llms-databricks
- **(a) 해결하는 문제:**
  - **LLM의 취약점 점검 도구 (penetration testing의 LLM 버전).**
  - 커버하는 취약점: 할루시네이션, 데이터 유출, 프롬프트 인젝션, 허위정보, 독성(toxicity) 생성, jailbreak 등.
  - **적응형 프로브** — `atkgen.Tox`처럼 타겟 응답을 보고 새 공격 케이스를 자동 생성.
- **(b) 통합 형태:**
  - **CLI + Python 라이브러리.** `garak --target_type huggingface --target_name gpt2 --probes encoding` 형태.
  - 타겟: HuggingFace 모델, OpenAI/Anthropic API, REST 엔드포인트.
  - 구조화된 리포트(취약점별 실패율) 출력.
- **(c) 한 줄 권장 시점:**
  > 배포 전 **"우리 모델이 알려진 공격 카테고리에 얼마나 뚫리는가"를 재현 가능한 수치로** 내고 싶을 때. CI에 붙이기 쉬움.

### 2.2 Microsoft PyRIT — Python Risk Identification Toolkit

- **출처:** https://github.com/microsoft/PyRIT · MS Security Blog 2024-02-22 · arXiv 2410.02828
- **(a) 해결하는 문제:**
  - **생성형 AI의 체계적 red-teaming 프레임워크.** Microsoft AI Red Team이 실제 100+ 작전에서 사용.
  - 모델·플랫폼 독립. 멀티모달 모델에도 적용.
  - 다회차 공격 전략 내장: **Crescendo, TAP, Skeleton Key**.
  - 콘텐츠 해악 / 심리사회적 위험 / 데이터 유출 등 표준 평가 시나리오 세트.
- **(b) 통합 형태:**
  - **Python 라이브러리 (오픈소스, 91% Python).**
  - GUI (human-led red-teaming, 팀 공동 추적).
  - 타겟: OpenAI, Azure, Anthropic, Google, HuggingFace, 커스텀 HTTP/WebSocket, Playwright 웹앱.
- **(c) 한 줄 권장 시점:**
  > **다회차 공격**(단발 jailbreak가 아니라 대화가 흘러가며 무너지는 케이스)까지 자동화해 돌리고 싶을 때, 그리고 사내 보안팀이 공동 추적 UI가 필요할 때.

### 2.3 Promptfoo Red Team

- **출처:** https://www.promptfoo.dev/docs/red-team/ · GitHub: https://github.com/promptfoo/promptfoo
- **(a) 해결하는 문제:**
  - **20+ 취약점 카테고리 자동 생성·검증:** 프롬프트 인젝션, jailbreak, PII/프라이버시 유출, 독성, SQL/shell 인젝션, 간접 인젝션, 무단 데이터 접근.
  - 공격 전략: base64 인코딩, DAN/Skeleton Key 템플릿 래핑, indirect injection payload 삽입.
  - **OWASP LLM Top 10** 프리셋 지원.
- **(b) 통합 형태:**
  - **CLI + YAML 설정 파일.** 
  - **CI/CD 친화** — GitHub Actions에서 정기 실행 가능.
  - OpenAI·Anthropic에서 사내 채택.
- **(c) 한 줄 권장 시점:**
  > **선언형 config(YAML)로 red-team 스위트를 관리**하고, PR마다 CI가 "이번 프롬프트 변경으로 새로 뚫린 공격이 있는가"를 보게 만들고 싶을 때.

### 2.4 NVIDIA NeMo Guardrails (보너스 — garak과 짝)

- **출처:** https://github.com/NVIDIA-NeMo/Guardrails · https://developer.nvidia.com/nemo-guardrails · arXiv 2310.10501
- **(a) 해결하는 문제:**
  - **프로그래머블 가드레일 툴킷.** 5종 rail: input / dialog / retrieval / execution / output.
  - Dialog rails가 차별점 — **대화 흐름 자체를 Colang DSL로 정의**해 off-topic/금지 영역 진입을 다회차로 막음.
- **(b) 통합 형태:**
  - **Python 패키지 (Apache 2.0).** OpenAI/Azure/Anthropic/HF/NVIDIA NIM 지원.
- **(c) 한 줄 권장 시점:**
  > 챗봇이 **여러 턴에 걸쳐 주제를 이탈하거나 정책을 우회하는 것**까지 막고 싶고, 가드레일 정책을 코드로 버전 관리하고 싶을 때.

---

## 3. 평가 하네스 (Safety-relevant Evaluation)

### 3.1 HELM Safety (Stanford CRFM)

- **출처:** https://crfm.stanford.edu/helm/safety/latest/ · arXiv 2211.09110 · Repo: https://github.com/stanford-crfm/helm
- **(a) 해결하는 문제:**
  - **LLM의 다차원 평가 오픈 프레임워크.** 16개 핵심 시나리오 × 7개 지표 (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency).
  - **Safety 서브셋**은 toxicity·bias·harmful behaviors 전용 시나리오를 포함.
  - 모델별 원본 prompt·completion을 **공개** — 재현·감사 가능.
- **(b) 통합 형태:**
  - **Python 프레임워크.** `pip install crfm-helm` → CLI로 벤치마크 실행.
  - 자체 모델·API를 `Client`로 등록해 돌림.
- **(c) 한 줄 권장 시점:**
  > "우리 모델이 toxicity·bias에서 공개 대형 모델 대비 어느 위치인가"를 **공개된 동일 조건**으로 비교하고 싶을 때.

### 3.2 MT-Bench (safety 한계와 쓰임새)

- **출처:** arXiv 2306.05685 · LMSYS · Awesome-LLM-Safety 벤치마크 리스트
- **(a) 해결하는 문제:**
  - **다회차 대화 품질 평가.** 80개 2-turn 문제, 8개 카테고리 (Writing, Roleplay, Info Extraction, Reasoning, Math, Coding, Knowledge).
  - **LLM-as-a-Judge** — GPT-4 판정이 사람과 80%+ 일치.
- **(b) 통합 형태:** FastChat 레포의 평가 스크립트, JSON 질문셋.
- **(c) 한 줄 권장 시점:**
  > **다회차 대화의 helpfulness를 빠르게 비교**하고 싶을 때. 단 safety 전용이 아니므로 HELM Safety / garak와 **병행** 권장.
- **한계 (9장 본문에 명시할 중요 포인트):** 
  > "MT-bench 논문은 helpfulness를 강조하지만, safety는 주로 생략한다(honesty and harmlessness are crucial... with anticipation that similar methods can be used by modifying the default prompt)." — MT-Bench **단독으로 안전 판단 금지**. adversarial 변형 벤치마크(MTJ-Bench 등)와 조합.

---

## 4. 한국 사례

### 4.1 카카오 Safeguard by Kanana (국내 기업 최초 오픈소스 AI 가드레일)

- **출처:** 
  - 공식 발표: https://www.kakaocorp.com/page/detail/11567
  - 기술블로그: 카카오 AI 가드레일 모델, Kanana Safeguard 시리즈를 소개합니다 · coco.bol 외 · https://tech.kakao.com/posts/705
  - HuggingFace 오픈소스 배포 (Apache 2.0)
- **(a) 해결하는 문제:**
  - **3종 모델로 역할 분담:**
    - `Kanana-Safeguard` — 혐오/괴롭힘/성/범죄/아동착취/자해 (S1~S6).
    - `Kanana-Safeguard Siren` — 법적 민감 요청: 성인인증, 전문 조언, 개인정보 노출, IP 이슈 (I1~I4).
    - `Kanana-Safeguard Prompt` — 적대적 공격: **프롬프트 인젝션(A1), 프롬프트 리킹(A2)**.
  - **한국어 + 한국 문화** 자체 데이터셋으로 학습 — 영어권 도구의 한국어 미흡 문제 해소.
- **(b) 통합 형태:**
  - HuggingFace 모델 (Apache 2.0). Llama Guard와 유사한 방식으로 입출력에 삽입.
  - 카카오 본사 서비스(Kanana, AI Shopping Mate)에 실제 배포.
- **(c) 한 줄 권장 시점:**
  > **한국어 서비스**에서 영어권 도구(Llama Guard, Prompt Shields)의 한국어 성능이 불확실할 때, 또는 한국 문화·법제 맥락(성인인증·전문직 조언 경계)까지 잡고 싶을 때.
- **9장 본문 활용 포인트:** "국내 기업 최초로 AI 가드레일 도구를 오픈소스로 공개" — **한국어 독자에게 가장 설득력 있는 근거**.

### 4.2 LY Corporation (LINE 계열) — "별도 가드레일이 왜 필요한가"

- **출처:** 안전은 기본, 비용 절감은 덤: AI 서비스에 별도 가드레일이 필요한 이유 · 한종우(Applied ML Dev) · 2025-01-22 · https://techblog.lycorp.co.jp/ko/safety-and-cost-saving-why-separate-guardrails-are-necessary
- **(a) 해결하는 문제 — 문제 제기의 구조:**
  - **시스템 프롬프트에 안전 규칙을 몰아 넣는 방식**의 3가지 취약점:
    1. **Position Bias** — "정보가 콘텍스트의 한가운데로 들어갈수록 정확도가 대략 U자 곡선을 그리며" 감소.
    2. **False Positive 증폭** — 유해 쿼리 거절률뿐 아니라 **무해 쿼리 거절률**도 같이 올라감.
    3. **Micro-perturbation 민감도** — "**출력을 JSON/CSV/XML로 써 달라'와 같이 출력 형식 관련해 단 한 줄만 수정해도 전체 예측 중 최소 10% 이상이 다른 답으로 바뀌었습니다**".
  - **3계층 방어 모델:** 입력 필터링·jailbreak 탐지 / 모델 safety FT·컨텍스트 제약 / 출력 검증·할루시네이션 탐지.
  - **경제성 근거:** 카스케이드 필터링(싼 모델이 먼저 걸러냄)로 **"최대 98%까지 추론 비용을 절감"** (FrugalGPT 인용).
- **(b) 통합 형태:** 아키텍처 가이드라인 성격의 글. 구체 도구보다 **설계 원칙**을 제공.
- **(c) 한 줄 권장 시점:**
  > 9장에서 "왜 가드레일을 별도 층으로 두는가"를 근거로 들 때 **가장 단단한 한국어 1차 자료**.
- **9장 본문 활용 포인트:** "출력 형식 한 줄 바꿨더니 응답의 10%가 달라졌다"는 수치는 **관측성 필요성의 가장 강한 한국어 인용**. 책의 "프롬프트 바꾸면 성능이 어디로 가는지를 재현 가능하게"(9장 평가 하네스 절)와 직결.

### 4.3 카카오페이증권 — AWS Bedrock Guardrails 프로덕션 적용

- **출처:** 페이증권의 업무도우미 AI봇 · Terra · 2025-01-24 · https://tech.kakaopay.com/post/choonsiri/ (gap③과 이중 활용)
- **(a) 해결하는 문제:**
  - **증권사 보안 요구** — 입력/출력 민감정보 필터링, 민감 문서 "exclude" 라벨링.
  - 직접 인용: *"증권사에서 AI를 도입하며 가장 어려웠던 측면은 아무래도 보안이었습니다"*.
- **(b) 통합 형태:** AWS Bedrock Guardrails (매니지드 서비스).
- **(c) 한 줄 권장 시점:**
  > AWS Bedrock을 이미 쓰는 금융·공공 도메인에서 **기존 인프라 연장선으로 가드레일을 붙이고** 싶을 때.

### 4.4 KISA 「인공지능(AI) 보안 안내서」 (보충)

- **출처:** https://www.kisa.or.kr/2060204/form?postSeq=19&page=1 · 참고 요약: https://peekaboolabs.ai/blog/kisa-ai-security-guide
- **대상:** 생성형 AI를 개발·활용하면서 개인정보를 처리하는 기업·기관, LLM 개발자·이용자.
- **가드레일 구축 전략 5축:** 데이터 검증·정제, 모델 모니터링·로그관리, 안전한 배포·접근 제어, Adversarial Training, 응답 필터링·검증.
- **9장 활용 포인트:** 국내 독자가 "회사 법무팀이 참조할 공식 문서"를 물을 때 **1차 인용**. 규제/컴플라이언스 관점을 가볍게 소개.

### 4.5 Velog — 국내 실무자의 가드레일 개요 (보충)

- **출처:** 가드레일 (in LLM) · 이우철 · 2025-07-26 · https://velog.io/@wclee7/%EA%B0%80%EB%93%9C%EB%A0%88%EC%9D%BC-in-LLM
- **역할:** 9장에서 **국내 개발자가 실제 이 주제를 어떻게 쓰고 있는지**를 보여주는 보조 자료. 입력/출력 가드레일을 2단계로 나누는 설명, 한국어 독자에 친숙.

---

## 5. 참고문헌

**1차 자료(집필 제출 조건 3건 기준 — 대폭 초과달성).**

| # | 유형 | 제목 | 제공자 | URL |
|---|------|------|--------|-----|
| 1 | Docs | Prompt Shields in Azure AI Content Safety | Microsoft Learn | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection |
| 2 | Blog | Enhance AI security with Azure Prompt Shields | Microsoft Azure | https://azure.microsoft.com/en-us/blog/enhance-ai-security-with-azure-prompt-shields-and-azure-ai-content-safety/ |
| 3 | Repo + Paper | PurpleLlama / Llama Guard 3·4 Model Cards | Meta AI | https://github.com/meta-llama/PurpleLlama |
| 4 | Repo | Rebuff — Prompt Injection Detector | protectai | https://github.com/protectai/rebuff |
| 5 | Repo + arXiv | garak — LLM vulnerability scanner | NVIDIA | https://github.com/NVIDIA/garak · https://arxiv.org/abs/2406.11036 |
| 6 | Repo + Blog | PyRIT — Python Risk Identification Toolkit | Microsoft | https://github.com/microsoft/PyRIT · https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative-ai-systems/ |
| 7 | Docs + Repo | Promptfoo Red Team Guide | Promptfoo | https://www.promptfoo.dev/docs/red-team/ · https://github.com/promptfoo/promptfoo |
| 8 | Repo + arXiv | NeMo Guardrails | NVIDIA | https://github.com/NVIDIA-NeMo/Guardrails · https://arxiv.org/abs/2310.10501 |
| 9 | Docs + arXiv | HELM (+ Safety subset) | Stanford CRFM | https://crfm.stanford.edu/helm/safety/latest/ · https://arxiv.org/abs/2211.09110 |
| 10 | Paper | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | Zheng et al. 2023 | https://arxiv.org/abs/2306.05685 |
| 11 | 한국 사례 | Safeguard by Kanana (공식 발표) | 카카오 | https://www.kakaocorp.com/page/detail/11567 |
| 12 | 한국 사례 | Kanana Safeguard 시리즈 소개 (기술블로그) | 카카오 tech | https://tech.kakao.com/posts/705 |
| 13 | 한국 사례 | 안전은 기본, 비용 절감은 덤 — 별도 가드레일 근거 | LY Corp · 한종우 | https://techblog.lycorp.co.jp/ko/safety-and-cost-saving-why-separate-guardrails-are-necessary |
| 14 | 한국 사례 | 페이증권 춘시리 AI봇 (Bedrock Guardrails) | 카카오페이 · Terra | https://tech.kakaopay.com/post/choonsiri/ |
| 15 | 한국 사례 | 인공지능(AI) 보안 안내서 | KISA | https://www.kisa.or.kr/2060204/form?postSeq=19&page=1 |

---

## 6. 9장 구성 제안 (집필 가이드)

9장 거버넌스 절을 이 자료들로 **3개 트랙**으로 구성 권장:

1. **"왜 별도 가드레일인가"** — LY Corp 글의 "출력 형식 한 줄 수정에 10%가 바뀐다"를 오프닝. 시스템 프롬프트에 안전 규칙을 몰아 넣지 않는 3가지 이유.
2. **"입력–모델–출력 3계층 구성"** — 각 층에 **"한국어면 먼저 X, 그게 없으면 Y"**의 선택 룰:
   - **입력:** 한국어 서비스 → Kanana Safeguard Prompt, 영어권·다국어 → Prompt Shields / Rebuff / Llama Guard Prompt.
   - **출력:** 한국어 → Kanana Safeguard + Siren, 영어권 → Llama Guard 3/4, Azure Content Safety.
   - **Red-team 주기 점검:** garak(취약점 카탈로그 스캔) + PyRIT(다회차 공격) + Promptfoo(CI 통합).
3. **"어디까지 해야 하는가"** — HELM Safety 서브셋을 기준점, MT-Bench는 helpfulness 보조. KISA 안내서를 컴플라이언스 1차 참조.

---

## 7. 리서치 한계

- **한국어 벤치마크 공란:** 한국어 safety 평가 표준이 없음. HELM·MT-Bench 모두 영어 편향. 국내 기관(KISA/KSIAI)의 평가 리더보드가 공개되어 있지 않아 9장 본문에서도 이 공백을 명시 필요.
- **가격/라이선스 심층비교 미수행:** 각 도구의 요금·라이선스 세부는 이 리서치에서 다루지 않음 (9장 톤이 "의사결정 감각" 위주이므로 계획상 불필요).
- **국내 기업 중 네이버·쿠팡 가드레일 사례:** 공개된 자료에서 충분한 근거 발견 못 함 (HyperCLOVA 관련 발표는 대부분 홍보성). 카카오·카카오페이·LY(LINE) 3개로 한국 사례 커버.
- **동적 공격 기법(Crescendo/Skeleton Key):** PyRIT 문서에서 언급한 다회차 공격의 상세 패턴은 이 리서치에 포함하지 않음. 9장에서 "이런 카테고리가 있다" 수준으로 언급 → 10장 "다음 걸음 — 평가·안전" 분기로 심화 이관.

**집필 제출 조건 충족 여부:**
- 거버넌스 절 1차 자료 3건 → **15건 확보 (대폭 초과)**. 그중 **한국어 1차 자료 5건** (Kanana Safeguard 공식+기술블로그, LY Corp, 카카오페이, KISA)으로 "영어권 도구 복붙" 이미지 회피 가능.
