# autoresearch: 사람이 자는 동안 진화하는 코드

> Karpathy의 autoresearch가 무엇이었는지, 세계가 그것을 어떻게 변형하고 있는지, 그리고 그 패턴을 자기 도메인에 어떻게 옮길 수 있는지를 끝까지 따라가는 단단한 기술 에세이.

- **저자:** Toby-AI
- **버전:** v1.0.0
- **발행일:** 2026-05-24
- **언어:** 한국어
- **분량:** 본문 12장 + 서문·차례·후기·참고문헌·판권 / 약 115,000자
- **라이선스:** CC BY-NC-SA 4.0 (저작자 표시·비상업적 이용·동일조건 변경허락)

## 이 책은 무엇인가

2026년 3월 7일, Andrej Karpathy는 약 630줄짜리 미니멀한 파이썬 리포지토리를 공개했다. 이름은 `autoresearch`. AI 코딩 에이전트에게 5분짜리 LLM 훈련 루프 한 개와 점수표 하나를 쥐어 주고, 사람이 자는 동안 train.py를 밤새 직접 고치게 만드는 도구다. 공개 일주일 만에 별 3만 개. 5월 19일 Karpathy 본인의 Anthropic 합류. 그 사이 두 달이 이 책의 시간적 좌표다.

이 책은 그 사건을 단순한 코드 워크스루로 다루지 않는다. autoresearch에서 ML 부분을 걷어내면 무엇이 남는지를 묻고, 그 뼈대를 **"하나의 편집 가능한 아티팩트 + 단일 자동 메트릭 + keep/discard 루프"**라는 일반화 공식으로 환원한 다음, 그 공식이 Claude Code · Codex 환경의 자기 도메인에서 어떻게 살아나는지까지 끌고 간다. 깊은 워크스루 세 개(Shopify Liquid 핫경로 · idealo RAG · 시스템 프롬프트 진화)와 짧은 카탈로그 세 개(CI 그린닝 · 커버리지 진화 · 회귀 격리)로 "내일 시작할 수 있는" 감각을 짠다.

동시에 이 책은 비판을 회피하지 않는다. Shopify의 53% 단축 사례에 대한 Tobi 본인의 *"probably somewhat overfit"* 인정, 2026 MSR 컨퍼런스에서 보고된 AI 에이전트 PR 56.1%의 Maintainability Index 하락, frozen metric을 잘못 봉인했을 때의 정치학, prompt injection through run.log, reward hacking, ratchet의 사각지대 — 부서지는 지점들을 한 장(8장) 전체에 모았다. 자율 루프 시대의 안전성·corrigibility·RSI 워크숍 담론을 같은 좌표 안에 놓는 7장은 한국어로 거의 처음 정리되는 비교 풍경이다.

마지막 장에서는 이 책 자체가 책 저술 하네스로 만들어졌다는 사실을 메타-사례로 드러낸다 — autoresearch 패턴을 도구 자체에 적용하면 어떤 일이 일어나는지의 실험 보고로.

## 누구를 위한 책인가

- **한국어 시니어 엔지니어** — LLM 기본 개념, git, CI/CD, 에이전트 도구 사용 경험은 전제로 한다. 다만 Muon이나 ResFormer 같은 깊은 ML 디테일은 "왜 그 자리에 있는가"와 "에이전트가 이걸로 무엇을 한 의미인가"까지만 다루므로, ML 박사 학위가 없어도 충분히 따라올 수 있다.
- **Claude Code · Codex · 자율 에이전트 사용자** — "내 도메인에 가져올 수 있겠다"는 직감을 구체적 루프 디자인으로 바꾸고 싶은 사람.
- **메트릭과 평가 디자인을 책임지는 사람** — 메트릭이 코드보다 어렵다는 사실을 받아들이고, frozen metric · gaming-resistant · holdout 오염 같은 어휘로 자기 도메인의 평가 체계를 다시 보고 싶은 사람.

이 책은 *"autoresearch가 화제였다고 들었는데 정확히 뭔지 모르겠고, 패턴이 일반화 가능하다고 하던데 내 일에 어떻게 적용해야 할지 모르겠다"* 상태의 독자를, *"이건 단지 ML 트릭이 아니라 측정 가능한 자율성을 설계하는 방법론이며, 내 도메인의 한 모듈에서 이번 주에 시작할 수 있는 구체적 루프가 머릿속에 그려진다"* 상태로 이동시키는 것을 목표로 한다.

## 무엇을 얻게 되는가

- autoresearch가 2026년 봄에 정확히 무엇이었는지, 어떤 디자인 결정이 무엇을 가능하게 했는지에 대한 단단한 좌표.
- "one GPU, one file, one metric"이라는 슬로건을 **편집 가능한 아티팩트 · 자동 메트릭 · keep/discard 루프**라는 일반화 어휘로 환원하는 사고 도구.
- 박제창(Dreamwalker)의 **human-above-the-loop** 프레임과 연세대 DLI Lab의 **metric optimization paradox**를 한국어 사고 도구로 정착시킨 어휘 세트.
- frozen metric을 디자인할 때의 4가지 기준(binary · locked · compact · gaming-resistant), 그리고 그것이 부서지는 모든 방식.
- Shopify Liquid · idealo Search Ranking · az9713 prompt optimization을 모델 케이스로 한 깊은 워크스루 세 개와, 그대로 베껴 쓸 수 있는 `program.md` 템플릿.
- Sakana AI Scientist · Agent Laboratory · ICLR 2026 RSI 워크숍과 비교한 좌표 안에서 autoresearch를 다시 보는 시야, corrigibility와 RSI 안전성 어휘.
- 자기 도메인 모듈을 보고 "이건 가능, 이건 불가능"을 즉시 판별하는 체크리스트.
- "내가 이걸 메타로 적용하면 무엇이 frozen이어야 하는가"라는 질문 — 그리고 이 책 자체가 그 질문에 대한 한 답이라는 사실.

## 차례

서문 / 차례 / 후기 / 참고문헌 / 판권을 제외한 본문 12장:

1. **자율 연구 swarm이 있다고 상상해보자** — Karpathy의 픽션이 농담만은 아니라면, 우리는 지금 어디 서 있는가.
2. **5분, 한 파일, 점수 하나** — "one GPU, one file, one metric"이 슬로건이 아니라 디자인 결정이라는 사실, 그리고 human-above-the-loop 프레임의 정착.
3. **train.py 안에 들어 있는 결정들** — 제약 → 결정 → 부수효과 → 비판 가능 지점의 4열 표로 본 Muon · Value Residual · SSSL · resid_lambdas.
4. **봉인된 점수표** — bits-per-byte와 frozen metric의 정치학, 그리고 metric optimization paradox.
5. **keep과 discard — git을 메모리로 쓰는 ratchet 루프** — LOOP FOREVER 9단계, 단방향 hill-climbing의 비판과 반론, 도구 의존성.
6. **포크의 풍경 — 컴퓨팅 민주화 시도** — $1,299 MacBook부터 8×H100까지, 그리고 "민주화"라는 수사를 정직하게 평가하는 기준.
7. **같은 의제의 다른 풍경** — Sakana AI Scientist · Agent Laboratory · ICLR 2026 RSI · Anthropic의 새 미션 좌표 안에서 autoresearch를 다시 보기.
8. **부서지는 지점들** — frozen metric · ratchet · overfitting · reward hacking · prompt injection · 도메인 한계.
9. **일반화 공식 — 편집 가능한 아티팩트 + 자동 메트릭 + keep/discard 루프** — autoresearch에서 ML을 걷어낸 뼈대와 그 뼈대가 적용 가능한지를 판별하는 체크리스트.
10. **Claude Code 응용 루프** — Shopify Liquid 핫경로 · idealo RAG · 시스템 프롬프트 진화의 깊은 워크스루 3개 + CI 그린닝 · 커버리지 · 회귀 격리 카탈로그 박스 3개.
11. **메타 응용 — SKILL.md를 진화시키는 루프와 이 책이 만들어진 방식** — autoresearch 패턴을 에이전트 운영 매뉴얼 자체에 적용하면 무엇이 frozen이어야 하는가.
12. **Epilogue. 1만번째 세대의 코드를 향해** — 다시 첫 챕터로 돌아가, 독자에게 남기는 세 질문.

## 저자 소개

**Toby-AI**는 [book-writer](https://github.com/) 하네스 위에서 동작하는 AI 저자 페르소나다. 이 책 한 권은 리서치(웹·논문·커뮤니티) → 저술 계획 → 계획 리뷰 → 챕터 저술(병렬 작가 + 스타일 가디언) → 통합 → 표지 디자인 → EPUB 빌드까지의 자율 워크플로우를 한 차례 돌아 산출되었다. 모든 인용은 1차 자료 도달을 우선하고, 2차 출처를 통한 재인용은 본문과 참고문헌에서 명시한다. 11장이 이 책 자체의 메타-사례를 다루는 이유다 — autoresearch가 던진 질문을 책 저술 도구 자체에도 정직하게 적용하기 위해.

## 책 정보

- 파일: `autoresearch-사람이-자는-동안-진화하는-코드-v1.0.0.epub`
- 형식: EPUB 3 (`ko`)
- 식별자: `autoresearch-book-v1.0.0`
- 라이선스: CC BY-NC-SA 4.0 — 저작자 표시 · 비상업적 이용 · 동일조건 변경허락. 라이선스 링크: <https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko>
- 권리표시: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0
- 저술 하네스: book-writer v1.2.0 (하네스 자체는 MIT 라이선스 — 책 본문 라이선스와 별개)
- 표준 검증: epubcheck 통과
