# Paper Research: 바이브 코딩하는 홈 베이커

수집 목적: 학술 인용보다, 본문 한 문장으로 녹여 쓸 수 있는 "정확한 사실 카드".

---

## 1. AI 시대 지식노동의 시간 사용

### 1-1. Peng et al., "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot" (arXiv:2302.06590, 2023)
- 통제 실험: 95명 개발자, JavaScript HTTP 서버 작성을 Copilot 사용군과 비사용군으로 무작위 배정.
- 핵심 결과: Copilot 사용군이 task를 **55.8% 더 빨리** 완료.
- 효과는 경험이 적은 개발자, 업무량이 많은 개발자, 더 나이 든 개발자에게 더 컸다.
- 본 책 활용: "도구가 시간을 압축한다 — 압축된 시간만큼 다른 시간이 비어 있게 된다."
- 인용 후보: "The treatment group, with access to the AI pair programmer, completed the task 55.8% faster."

### 1-2. METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity" (arXiv:2507.09089, 2025)
- 통제 실험: 16명의 숙련 OSS 개발자, 246개의 실제 이슈를 무작위로 "AI 사용 가능/불가" 배정. AI 조건에서는 주로 Cursor Pro + Claude 3.5/3.7 Sonnet 사용.
- 핵심 결과: AI를 쓰면 task 완료가 평균 **19% 더 느렸다**.
- 인지 vs 현실의 괴리: 시작 전 개발자들은 24% 빨라질 거라 예측, 끝난 뒤에도 20% 빨라졌다고 추정. 실제는 -19%.
- 본 책 활용: "우리는 시간을 절약했다고 *느끼면서* 더 많은 시간을 쓴다 — 그 잉여의 시간이 빵 굽기로 흘러간다." 또는 "AI는 빨라지게 하지 않는다. 다만 일이 다른 모양이 되게 한다."
- 인용 후보: "Developers forecast a 24% reduction; the actual effect was a 19% increase."

### 1-3. Gloria Mark, "The Cost of Interrupted Work: More Speed and Stress" (CHI 2008)
- 핵심 발견: 한 번 끊긴 작업으로 다시 돌아오는 데 평균 **23분 15초**.
- 같은 날 안에 끊긴 작업의 81.9%는 다시 재개되지만, 그 사이 평균 23분 15초의 공백.
- 평균 사람은 하루에 12.2개의 "working sphere"를 다루며, 약 10분 29초마다 sphere를 바꾼다. 한 사건에 평균 **3분 5초** 머문다.
- 후속 연구(Mark 2014~2020)는 한 화면에서의 평균 주의 지속 시간이 44~50초까지 떨어졌음을 보고.
- 본 책 활용: "AI에게 task를 던지고 빵 반죽으로 가는 것은 — 23분이라는 그 회복 시간을 발효 시간 안에 숨기는 일이다." 또는 "주의가 44초밖에 가지 않는 시대에, 30분 폴딩 간격은 거의 종교적이다."

### 1-4. Baird et al., "Inspired by Distraction: Mind Wandering Facilitates Creative Incubation" (Psychological Science, 2012)
- 실험: 어려운 문제를 잠시 보여준 뒤 (a) 무리 없는 단순 과제 (b) 인지부하 큰 과제 (c) 휴식 (d) 즉시 풀기 — 네 조건 비교.
- 결과: **단순 과제(undemanding task)** 조건에서 창의적 해법이 가장 많이 나왔다. 단순 휴식보다 더 좋았다.
- 본 책 활용: 이게 책의 핵심 학술 근거다 — "AI에게 코드를 위임하고 단순한 손작업(반죽 폴딩, 설거지, 산책)에 잠시 들어가는 것이, 그저 쉬는 것보다 더 좋은 인큐베이션이다."
- 인용 후보: "Engaging in an undemanding task during an incubation period led to substantial improvements in performance on previously encountered problems."
- 한계: 후속 연구에서 같은 결과를 항상 재현하지는 못함. → "확인된 효과 + 논쟁 중" 문맥으로 사용.

---

## 2. craft work · flow · 손노동의 인지·정서

### 2-1. Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience* (1990) + 후속 연구
- flow의 세 핵심 조건: (1) 명확한 목표 (2) 즉각적 피드백 (3) 도전과 기량의 균형.
- 도전이 너무 높으면 좌절, 너무 낮으면 권태 — 한가운데 좁은 "flow 채널"이 있다.
- 사워도우는 정확히 이 조건을 충족: 매 회마다 명확한 단계 목표(폴딩, 정형, 스코어링), 반죽의 끈기와 부피로 즉각 피드백, 가수율을 높일수록 자연스럽게 도전이 올라간다.
- 메타분석(Fong et al., 2014, *J. Happiness Studies*): challenge-skill balance는 flow의 가장 일관된 예측자.
- 본 책 활용: "사워도우는 flow의 교과서적 활동이다. 코딩도 그랬다 — AI 이전에는." 흐름을 빵에서 다시 회복하는 모티프.

### 2-2. Margaret Wilson, "Six Views of Embodied Cognition" (Psychonomic Bulletin & Review, 2002)
- 인용수 4,500+ 의 고전 리뷰. 인지가 "신체화되어 있다"는 6가지 주장을 정리·평가.
- 본 책에 가장 유용한 두 명제: (1) "cognition is situated"(인지는 상황에 박혀 있다) (3) "we off-load cognitive work onto the environment"(우리는 인지 부하의 일부를 환경에 떠넘긴다).
- 본 책 활용: "반죽이 손가락에게 발효의 진행 상황을 알려준다. 이건 비유가 아니라, 인지를 환경에 떠넘기는 행위다." / "코딩에서 우리는 인지를 IDE와 LSP에 떠넘긴다. 이제 LLM에도. 그렇다면 비어 있는 인지의 자리에 무엇을 둘 것인가."

### 2-3. Richard Sennett, *The Craftsman* (Yale, 2008)
- 핵심 주장 1: "일을 그 자체를 위해 잘하고자 하는 욕망(desire to do a job well for its own sake)"이 craftsmanship의 본질.
- 핵심 주장 2: 머리와 손, 추상지식과 체화된 기술 사이의 대립은 *거짓 대립*이다. "intelligent hand"라는 개념.
- 핵심 주장 3: "재료가 되받아친다(the material pushes back)" — 저항·놀라움·안내. 숙련은 이 저항과의 만남에서만 생긴다.
- 핵심 주장 4: 숙련에는 ~10,000시간이 필요하며, "기량은 불규칙하게, 때로는 우회로를 거쳐 자란다(skill builds by moving irregularly, and sometimes by taking detours)".
- 본 책 활용: AI 코딩에서는 "저항"이 줄어든다 — 컴파일러도 LLM도 부드럽게 도와준다. 반면 사워도우 반죽은 끝까지 되받아친다. 그 저항이 craftsman을 만든다는 Sennett의 명제는 이 책의 가장 강력한 입론 도구.
- 인용 후보:
  > "The desire to do a job well for its own sake."
  > "Skill builds by moving irregularly, and sometimes by taking detours."
  > "The material pushes back."

### 2-4. Matthew Crawford, *Shop Class as Soulcraft* (2009) — 학술 외 인접 자료
- 핵심: 지식노동 우대 교육은 "생각과 행동의 분리"라는 잘못된 전제 위에 있다.
- 인용 후보: "Manual work is psychically satisfying and is often cognitively demanding, more so than, say, management consulting, because it can't be reduced to abstract rules."
- 본 책에서 Sennett과 짝으로 쓰면 효과적.

---

## 3. 발효의 미생물학·화학 — 본문에 쓸 한 줄 사실들

### 사워도우 starter
1. starter는 50종 이상의 lactic acid bacteria(LAB)와 20종 이상의 효모를 품을 수 있는 작은 생태계다. (Landis et al., *eLife* 2021, "The diversity and function of sourdough starter microbiomes" — pmc.ncbi.nlm.nih.gov/articles/PMC7837699)
2. 그러나 한 starter 안에서는 보통 단 1~3종의 LAB와 1종의 효모가 우점한다 — 거대한 잠재 다양성이 매우 단순한 균형으로 수렴한다.
3. *Saccharomyces cerevisiae*가 fungal ITS read의 50% 이상을 차지하는 starter가 전체의 77%. 우리가 빵에서 만나는 가장 흔한 효모는 맥주 효모와 같은 종이다.
4. *Lactobacillus sanfranciscensis*는 우점하는 곳에서는 다른 LAB(*L. plantarum*, *L. brevis*)와 음의 상관 — 한 종이 자리를 잡으면 다른 종을 밀어낸다.
5. 가장 흔한 동시 출현 짝은 *L. plantarum* + *L. brevis* (500개 starter 중 177개).
6. starter의 정상 향은 요거트 같은 시큼함. 아세톤(매니큐어 리무버) 향이 나면 "굶주림" 신호 — 더 자주 먹여달라는 메시지.

### 발효의 동역학 (Q10 법칙)
7. 효모 발효는 대부분의 효소 반응처럼 Q10 ≈ 2를 따른다 — **온도가 10°C 오를 때마다 속도가 두 배**가 된다(반대로, 10°C 떨어지면 절반).
8. 부엌 평상 범위(18~28°C)에서 5°C 변동이면 발효 시간이 두 배 또는 절반.
9. 4°C 냉장고는 24°C 부엌 대비 약 5배의 발효 시간 — 그래서 12~24시간 콜드 리타드가 가능하다.
10. 같은 효모 dosage라도 도우 온도가 24°C에서 25°C로 1°C만 올라도, 4시간 벌크가 약 3시간 30분으로 짧아질 수 있다.
11. 이 단순한 지수 법칙 하나가 모든 베이커의 일정표를 지배한다 — 본 책의 좋은 모티프: "지수곡선은 코딩만의 것이 아니다."

### 향과 Maillard
12. Maillard 반응은 약 140°C(280°F)에서 빠르게 시작되어 165°C 부근에서 활발하다. (Wikipedia: Maillard reaction)
13. 140°C에서 90분이 pyrazine 형성의 최적 조건 — 이는 빵 crust의 "구운 향"을 만드는 핵심 분자군.
14. **2-acetyl-1-pyrroline**: 갓 구운 빵의 그 정확한 향. 1-pyrroline(아미노산 proline의 Strecker degradation 산물)과 pyruvaldehyde의 반응으로 생긴다. 자스민 쌀, 팝콘에서도 같은 분자가 향을 결정한다.
15. 사워도우는 pH가 낮아 caramelization과 Maillard가 동시에 빠르게 진행 — 그래서 표면이 짙고 향이 복잡해진다.
16. 발효 중 LAB은 lactic acid와 acetic acid를 만든다. lactic은 부드러운 요거트 같은 신맛, acetic은 톡 쏘는 식초 같은 신맛. 콜드 리타드에서 acetic이 우세해진다.
17. 발효 중 효모는 알코올과 ester를 만든다 — 과일·꽃 향. aldehyde·ketone은 버터·맥아·풀 향.
18. 굽기 마지막에 알코올의 대부분은 증발한다. 향만 남는다.

---

## 4. 직접 인용 후보 짧은 문장들

> "The treatment group, with access to the AI pair programmer, completed the task 55.8% faster than the control group." — Peng et al. (arXiv:2302.06590, 2023)

> "Developers forecast that AI would reduce completion time by 24%; in reality, AI increased completion time by 19%." — METR (arXiv:2507.09089, 2025)

> "It takes an average of 23 minutes and 15 seconds to fully regain deep focus after an interruption." — Gloria Mark (CHI 2008)

> "Engaging in an undemanding task during an incubation period led to substantial improvements in creative performance." — Baird et al. (Psychological Science, 2012)

> "The desire to do a job well for its own sake." — Richard Sennett, *The Craftsman* (2008)

> "Skill builds by moving irregularly, and sometimes by taking detours." — Sennett, 같은 책

> "The material pushes back." — Sennett

> "Manual work is psychically satisfying and is often cognitively demanding, more so than, say, management consulting, because it can't be reduced to abstract rules." — Matthew Crawford, *Shop Class as Soulcraft*

> "Q10 ≈ 2: every 10°C rise roughly doubles the rate of biological reactions." — 일반 효소 동역학 원리, 베이킹에 동일 적용.

> "A single starter typically harbours one to three dominant lactic acid bacteria and a single dominant yeast — a vast potential diversity converging onto a simple balance." — Landis et al., *eLife* 2021 (paraphrase)

---

## 5. 참고 문헌

- Peng, S., et al. (2023). *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot.* arXiv:2302.06590. https://arxiv.org/abs/2302.06590
- METR (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* arXiv:2507.09089. https://arxiv.org/abs/2507.09089 / https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- Mark, G., Gudith, D., & Klocke, U. (2008). *The Cost of Interrupted Work: More Speed and Stress.* CHI 2008. https://ics.uci.edu/~gmark/chi08-mark.pdf
- Mark, G. (2023). *Attention Span: A Groundbreaking Way to Restore Balance, Happiness and Productivity.* (대중서이지만 측정치 인용 출처)
- Baird, B., Smallwood, J., Mrazek, M. D., Kam, J. W. Y., Franklin, M. S., & Schooler, J. W. (2012). *Inspired by Distraction: Mind Wandering Facilitates Creative Incubation.* *Psychological Science*, 23(10), 1117–1122. https://journals.sagepub.com/doi/abs/10.1177/0956797612446024
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience.* Harper & Row.
- Fong, C. J., et al. (2014). *The challenge–skill balance and antecedents of flow: A meta-analytic investigation.* (학술 메타분석)
- Wilson, M. (2002). *Six Views of Embodied Cognition.* *Psychonomic Bulletin & Review*, 9(4), 625–636. https://pages.ucsd.edu/~scoulson/Courses/200/EmbCog_Wilson.pdf
- Sennett, R. (2008). *The Craftsman.* Yale University Press. https://yalebooks.yale.edu/book/9780300151190/the-craftsman/
- Crawford, M. B. (2009). *Shop Class as Soulcraft: An Inquiry into the Value of Work.* Penguin Press. https://www.thenewatlantis.com/publications/shop-class-as-soulcraft
- Landis, E. A., et al. (2021). *The diversity and function of sourdough starter microbiomes.* *eLife*. https://elifesciences.org/articles/61644
- Maillard reaction 일반: https://en.wikipedia.org/wiki/Maillard_reaction
- Schieber & Kerber (2007). *Chemistry of 2-acetyl-1-pyrroline...* (2-acetyl-1-pyrroline 화학) — researchgate.net/publication/7013028

---

## 한계
- AI 코딩의 "비어 있는 시간"을 직접 정량화한 학술 연구는 (2026년 4월 기준) 거의 없다 — METR·Peng은 task 시간을 보지만, "task 사이의 시간"은 측정하지 않는다. 본 책에서는 이 공백을 직접 채우는 일이 곧 책의 입장이다.
- 사워도우 미생물학은 풍부하지만, 가정 베이커의 starter에서 "맛이 깊어지는" 시점에 대한 정량적 시간 곡선 연구는 드물다 — Wikipedia/대중과학지 수준에서 보강.
- Csikszentmihalyi의 flow 이론은 베이킹·요리에서 직접 측정한 연구가 적다. 일반화된 framework로만 사용.
