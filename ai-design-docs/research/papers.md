# 논문 리서치: AI 코딩 에이전트 시대의 설계·문서화 — 명세·도메인 규칙·계약·ADR·추적성·검증 증거를 통제 계층으로

- 슬러그: `ai-design-docs` · 장르: `tech-book`
- 검색 시점: 2026-10-28
- 1차 기준 문서: `research/primary/ai-project-design-guidelines-ko.md` (이하 "가이드", 절 번호 01~14)
- 메타데이터 확인 방법:
  - arXiv ID·저자·제목·최초 게시일·abstract는 arXiv API(`export.arxiv.org/api/query`)로 직접 조회했다.
  - 발표처·DOI·피인용수는 Semantic Scholar Graph API(batch)로 조회했다(2026-10-28 기준, 숫자는 계속 변한다).
  - arXiv에 없는 고전 논문(Gotel 1994, Bainbridge 1983, Tyree 2005, Jansen 2005, Parasuraman 2010, Mäder 2015, Aghajani 2019, Buchgeher 2023, Lee 2025, Cui 2025)은 웹 검색으로 서지와 핵심 수치를 확인했다. 확인 경로는 항목마다 적었다.
- 표기 규칙
  - **[원문]**: abstract 또는 본문(HTML)에서 직접 확인한 수치·문장
  - **[2차]**: 출판사 페이지·학회 페이지·보도 등 2차 출처로 확인한 값
  - **미확인**: 조회했지만 확인하지 못한 값. 본문에 쓰기 전에 fact-checker가 다시 확인해야 한다.
- 인용 블록(>)은 arXiv abstract의 원문 문장이다. 페이지 번호가 아니라 "abstract"로 위치를 적었다.
- 신선도 경고: 2026년 게시 논문 다수는 **프리프린트이고 동료 심사 전**이다. 특히 단독 저자 프리프린트는 표에 "프리프린트(단독 저자)"로 따로 표시했다. 책 본문에서는 "~라는 보고가 있다" 수준으로 쓰고, 단정하지 않는다.

---

## 0. 한눈에 보기 — 책의 주장과 근거 매핑

| 책(가이드)의 주장 | 가장 강한 근거 | 반대·보완 근거 |
|---|---|---|
| "AI가 빠르게 해 준다"는 체감은 믿을 수 없다 → 증거로 판단 (가이드 01, 06 VAL, 14) | METR RCT: 체감 +20% vs 실측 −19% (논문 1) | Google RCT +21%, Microsoft/Accenture 현장실험 +26% (논문 2·3) |
| 속도는 일시적, 품질 부채는 지속 → 검증·관측을 통제 지점에 (가이드 09) | Cursor 도입 DiD: 속도 일시 증가, 경고·복잡도 지속 증가 (논문 6), 에이전트 도입 DiD: 경고 +18%, 인지 복잡도 +39% (논문 7) | 유지보수성 RCT에서 유의한 차이 없음 (논문 5) |
| "테스트 통과 = 정답"이 아니다 (가이드 02, 09 "CI 초록색의 정확한 의미") | SWE-bench "통과" 패치의 29.6%가 정답과 다르게 동작 (논문 11), EvalPlus pass@k 최대 28.9% 하락 (논문 12) | — |
| 컨텍스트 파일은 만능이 아니다. 금지 규칙·실행 가능한 검사로 바꿔라 (가이드 10 "공통 입력 꾸러미", 12) | AGENTS.md가 성공률을 올리지 않고 비용 +20% (논문 17), 규칙 중 이로운 것은 모두 금지형 (논문 20), 오래된 지시 파일을 코드보다 우선 90.1% (논문 21) | 실행 시간 −28.64%, 토큰 −16.58% (논문 18) |
| 틀린 문서는 없는 문서보다 나쁘다 → 원본 하나, 링크로 참조 (가이드 02) | 틀린 문서는 코드 이해를 크게 해치고, 누락은 거의 영향 없음 (논문 27), 오래된 지시 파일 추종 (논문 21) | — |
| 모호한 요구는 AI가 그럴듯하게 채운다 → 미결정 표시·질문 (가이드 04, 10, 14) | 모델은 명세가 충분한지 구분하지 못함, 질문하면 최대 74% 향상 (논문 24) | ClarifyGPT, TiCoder (논문 25·29) |
| 테스트·사후조건을 먼저 → 요구를 실행 가능한 형태로 (가이드 06 AC/TC) | TDD 프롬프트로 성공률 향상 (논문 28), TiCoder pass@1 +45.97%p (논문 29), nl2postcond가 Defects4J 실제 버그 64개 포착 (논문 31) | — |
| AI 리뷰는 독립 검증이 아니다 (가이드 07 "AI 검토를 과신하지 않는 법") | 외부 피드백 없는 자기 교정은 실패 (논문 33·34), 두 모델이 동시에 틀릴 때 60% 같은 답 (논문 35), 판정 모델은 자기·유사 모델 편애 (논문 36·37) | 외부 피드백(테스트·검증기)이 있으면 교정 가능 (논문 34) |
| 결정 근거는 사라진다 → ADR (가이드 08) | 아키텍처 = 설계 결정의 집합, 결정 지식 증발 (논문 40), 추적성이 있으면 24% 빠르고 50% 더 정확 (논문 44) | ADR 채택은 낮고 63%가 처음부터 "accepted" (논문 42) |
| 사람이 최종 결정을 소유 (가이드 10 마지막 문단) | 자동화의 역설 (논문 47), 자동화 편향 (논문 48), AI를 쓰면 보안이 더 나쁜데 더 안전하다고 믿음 (논문 49), 학습 저하 17% (논문 51) | 인지적으로 관여하는 사용 패턴은 학습을 보존 (논문 51) |
| 역할 분리는 쓸모 있지만 만능이 아니다 (가이드 10 PLANNER/DESIGNER/REVIEWER/IMPLEMENTER) | 역할 추가로 실행 가능성 1.0→4.0 (논문 54 MetaGPT 제거 실험), 테스트 설계 에이전트 분리 (논문 56) | MAS 실패의 상당수가 명세·검증 문제 (논문 57), 단일 에이전트로도 비슷 (논문 58·59), 순차 과제에서 −70% (논문 60) |

---

## 1. AI 코딩 생산성·품질 실증 연구

### 논문 1: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity
- 저자·연도: Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (METR), 2025
- 발표처: arXiv 프리프린트 (S2 기준 학회 미등재)
- arXiv: 2507.09089 (v1 2025-07-12) · DOI 10.48550/arXiv.2507.09089
- 피인용수: 229 (S2, 2026-10-28)
- 요약: 숙련 오픈소스 개발자 16명이 자신이 평균 5년 기여한 성숙 저장소에서 246개 과제를 수행했다. 과제마다 AI 허용/금지를 무작위 배정했다(주 도구 Cursor Pro + Claude 3.5/3.7 Sonnet). AI 허용 시 완료 시간이 19% **늘었다**. 개발자 자신은 사전에 24% 단축을 예상했고, 사후에도 20% 단축됐다고 믿었다.
- 핵심 수치 [원문]:
  - 사전 예측 −24%, 사후 체감 −20%, 실측 +19% (느려짐)
  - 경제학 전문가 예측 −39%, ML 전문가 예측 −38%
  - 개발자는 AI 생성물의 44% 미만을 채택했다 (부록 C.1.4)
  - 시간의 약 9%를 AI 출력 검토·정리에, 약 4%를 생성 대기에 썼다 (C.1.4, C.2.9)
  - 56%가 AI 코드를 정리하려고 자주 큰 수정을 했다고 답했다 (C.1.4)
  - 저장소 평균: 약 10년, 약 110만 줄, 별 약 23,000개 (2.1절)
  - 느려짐의 기여 요인 후보: 과도한 낙관, 저장소에 대한 높은 숙련도, 크고 복잡한 저장소, 낮은 AI 신뢰성, **암묵적 저장소 맥락**("AI doesn't pick the right location to make the edits") (3.3절, 표 1)
- 인용할 만한 문장:
  > "Surprisingly, we find that allowing AI actually increases completion time by 19%--AI tooling slowed developers down." (abstract)
- 책 활용: 가이드 06의 "'AI가 검토 완료' 한 문장은 증거를 대체하지 않습니다"를 여는 일화로 쓰기 좋다. **암묵적 저장소 맥락**이 느려짐 요인이라는 점은 "암묵 지식을 문서(domain/·adr/)로 꺼내야 한다"는 책 주장으로 이어진다. 단, 이는 저자들이 "기여 가능성이 있는 요인"으로 든 것이지 인과 증명이 아니다.

#### 논문 1-후속: METR "uplift update" (블로그, 2026-02-24)
- 출처: METR 블로그 `metr.org/blog/2026-02-24-uplift-update/` (동료 심사 논문 아님) [원문: 블로그 직접 조회]
- 표본: 개발자 57명(복귀 10, 신규 47), 저장소 143개, 과제 800+, 2025년 8월 시작(Claude Code·Codex 등 에이전트 도구 확산기)
- 추정치: 복귀 개발자 −18% (CI −38%~+9%), 신규 개발자 −4% (CI −15%~+9%). 두 구간 모두 0을 포함한다. 원 연구 수치는 +19% (CI +2%~+39%)로 블로그에 다시 적혀 있다.
- 주의: "AI 없이 일하기 싫다"는 개발자의 불참, 30~50%의 개발자가 AI 없이 하기 싫은 과제를 제출하지 않음 → 속도 향상을 **과소 추정**하는 선택 편향. 여러 에이전트를 동시에 돌리면 시간 기록이 불안정. METR은 이 결과를 "only very weak evidence"라고 표현했다.
- 책 활용: "느려진다"를 단정하지 말 것. "2025년 초에는 느려졌고, 후반에는 빨라졌을 수 있지만 측정 자체가 어려워졌다"가 정확한 서술이다. **측정이 어려워졌다는 사실 자체**가 "검증 증거를 설계해야 한다"는 책 주장을 강화한다.

### 논문 2: How much does AI impact development speed? An enterprise-based randomized controlled trial
- 저자·연도: Elise Paradis, Kate Grey, Quinn Madison, Daye Nam, Andrew Macvean, Vahid Meimand, Nan Zhang, Ben Ferrari-Church, Satish Chandra (Google), 2024
- 발표처: ICSE-SEIP 2025 (S2 기준) · DOI 10.1109/ICSE-SEIP66354.2025.00060
- arXiv: 2410.12944
- 피인용수: 41
- 핵심 수치 [원문]: Google 정규직 엔지니어 96명 RCT, 복잡한 사내 과제에서 AI 기능 3종 사용 시 과제 시간 약 **21% 단축**. 저자 스스로 "신뢰구간이 크다", "2024년 여름 사내 도구의 효과가 다른 도구·시점으로 옮겨진다고 가정할 수 없다"고 적었다.
- 책 활용: METR과 대비하는 짝. 차이는 과제 성격(사내 표준 과제 vs 오래된 대형 OSS 저장소)과 맥락 친숙도.

### 논문 3: The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers
- 저자·연도: Kevin Zheyuan Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, Tobias Salz, 2025
- 발표처: Management Science · DOI 10.1287/mnsc.2025.00535 [2차: INFORMS 페이지·SSRN 4945566]
- 핵심 수치 [2차: 출판사 abstract 기반]: Microsoft·Accenture·익명 Fortune 100 기업의 현장 RCT 3건, 개발자 4,867명 통합. AI 코딩 도우미 접근으로 **완료 과제 수 26.08% 증가**(표준오차 10.3%). 개별 실험은 잡음이 크다고 저자가 명시.
- 미확인: 경력별 이질성(주니어에서 효과가 크다는 보도)은 본문에서 확인하지 못했다.
- 책 활용: "생산성은 측정 단위(과제 수 vs 과제 시간 vs 품질)에 따라 결론이 갈린다"를 보여 주는 사례.

### 논문 4: The Impact of AI on Developer Productivity: Evidence from GitHub Copilot
- 저자·연도: Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer, 2023
- 발표처: arXiv 프리프린트 · arXiv 2302.06590
- 피인용수: 863
- 핵심 수치 [원문]: JavaScript로 HTTP 서버 구현 과제, Copilot 사용 그룹이 **55.8% 빠르게** 완료.
- 책 활용: 업계가 자주 인용하는 "55%"의 출처. 단일·소규모 그린필드 과제였다는 맥락을 함께 적어야 한다.

### 논문 5: Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability
- 저자·연도: Markus Borg, Dave Hewett, Nadim Hagatulah, Noric Couderc, Emma Söderberg, Donald Graham, Uttam Kini, Dave Farley, 2025
- 발표처: ICSME 2025 Registered Report (원칙적 게재 승인, arXiv 코멘트 기준) · arXiv 2507.00788
- 핵심 수치 [원문]: 참가자 151명(95%가 현업 개발자). 1단계에서 AI 유무로 기능 추가, 2단계에서 **다른 개발자가 AI 없이** 그 코드를 발전시킴. 2단계에서 완료 시간·코드 품질에 유의한 차이 없음. 1단계 관찰 결과로 AI 사용 시 완료 시간 중앙값 30.7% 감소, 습관적 AI 사용자는 55.9% 단축 추정.
- 인용할 만한 문장:
  > "Future work should examine risks such as code bloat from excessive code generation and cognitive debt as developers offload more mental effort to assistants." (abstract)
- 책 활용: 균형 잡기용. "AI 코드가 곧 유지보수 지옥"은 과장이다. 문제는 코드 한 조각의 품질보다 **누적·맥락·검증 공백**이라는 책의 논지로 연결.

### 논문 6: Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects
- 저자·연도: Hao He, Courtney Miller, Shyam Agarwal, Christian Kästner, Bogdan Vasilescu, 2025
- 발표처: MSR 2026 · DOI 10.1145/3793302.3793349
- arXiv: 2511.04427
- 피인용수: 40
- 요약 [원문]: Cursor 도입 GitHub 프로젝트와 매칭한 비도입 프로젝트를 이중차분(DiD)으로 비교. 도입 후 개발 속도가 **크고 유의하지만 일시적으로** 증가했고, 정적 분석 경고와 코드 복잡도는 **크고 지속적으로** 증가했다. 패널 GMM 분석에서 경고·복잡도 증가가 장기 속도 저하의 주요 요인이었다.
- 인용할 만한 문장:
  > "Our study identifies quality assurance as a major bottleneck for early Cursor adopters and calls for it to be a first-class citizen in the design of agentic AI coding tools and AI-driven workflows." (abstract)
- 책 활용: 가이드 09 "문서를 개발의 통제 지점에 연결"의 핵심 근거. "품질 보증을 일급 시민으로"라는 저자 표현이 책 메시지와 그대로 겹친다.

### 논문 7: AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development
- 저자·연도: Shyam Agarwal, Hao He, Bogdan Vasilescu, 2026
- 발표처: MSR 2026 · DOI 10.1145/3793302.3793589
- arXiv: 2601.13597
- 핵심 수치 [원문]: AIDev 데이터셋 기반 시차 DiD. 에이전트가 프로젝트의 **첫 AI 도구**일 때만 크고 앞쪽에 몰린 속도 증가. 이미 AI IDE를 쓰던 저장소는 증가가 작거나 짧다. 품질 위험은 모든 조건에서 지속: 정적 분석 경고 약 **18%**, 인지 복잡도 약 **39%** 증가.
- 책 활용: "에이전트를 도입하면 기술 부채가 지속적으로 쌓인다 — 속도 이득이 사라진 뒤에도." 가이드 14 "흔한 실패" 표의 실증 근거.

### 논문 8: The Rise of AI Teammates in Software Engineering (SE) 3.0 / AIDev: Studying AI Coding Agents on GitHub
- 저자·연도: Hao Li, Haoxiang Zhang, Ahmed E. Hassan, 2025 / 2026
- 발표처: arXiv 2507.15003 (2025) / MSR 2026 데이터 논문 arXiv 2602.09185 · DOI 10.1145/3793302.3797249
- 핵심 수치 [원문]:
  - 2025판: 에이전트 5종(OpenAI Codex, Devin, GitHub Copilot, Cursor, Claude Code)의 PR 456,000+건, 저장소 61,000개, 개발자 47,000명. 에이전트 PR은 사람보다 빠르지만 **수락 빈도가 낮다**("trust and utility gap"). 한 개발자가 3년치 PR을 3일에 제출한 사례. 에이전트 PR은 구조적으로 더 단순.
  - 2026판: 에이전트 PR 932,791건, 저장소 116,211개, 개발자 72,189명. 별 100개 이상 저장소 2,807곳의 33,596건 정제 부분집합.
- 책 활용: "에이전트 PR은 이미 현실 규모"라는 장 도입부. 데이터셋 자체가 아래 9~10번 연구의 토대다.

### 논문 9: On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub
- 저자·연도: Miku Watanabe, Hao Li, Yutaro Kashiwa, Brittany Reid, Hajimu Iida, Ahmed E. Hassan, 2025
- 발표처: ACM TOSEM (S2 기준) · DOI 10.1145/3798166
- arXiv: 2509.14745
- 피인용수: 115
- 핵심 수치 [원문]: Claude Code로 만든 PR 567건(OSS 157개 프로젝트). 리팩터링·문서·테스트에 주로 사용. **83.8%가 최종 병합**, 병합된 PR 중 **54.9%는 수정 없이** 통합, 나머지 45.1%는 사람의 추가 수정 필요 — 특히 버그 수정, 문서, **프로젝트별 표준 준수**.
- 책 활용: "프로젝트별 표준 준수"에서 사람 손이 가장 많이 간다는 점 → 가이드 10의 "공통 입력 꾸러미"와 guides/ 문서의 가치.

### 논문 10: 에이전트 PR 후속 연구 묶음 (MSR 2026 마이닝 챌린지 등, AIDev 기반)
아래는 모두 AIDev 데이터를 쓴 짧은 논문이다. 숫자는 abstract에서 확인했다 [원문].
- **Trust but Verify? Uncovering the Security Debt of Autonomous Coding Agents** — A H M Nazmus Sakib, Dipayan Banik, Murtuza Jadliwala, 2026, KDD 2026 AgenticSE 워크숍, arXiv 2607.12428. PR 4,022건·파일 변경 16,112건 분석. 에이전트 PR의 **38.9%에 보안 스멜 1개 이상**, 그중 82.3%가 공급망 무결성 문제, 치명 등급의 99.6%가 하드코딩 자격 증명. 유출된 실제 비밀의 **67.6%는 사람이 넣었고**, 기존 자동·사람 리뷰가 **81.1%를 통합 전 놓쳤다**. 저자는 "개발자 경계심 저하 가능성"을 제기.
- **These Aren't the Reviews You're Looking For: How Humans Review AI-Generated Pull Requests** — Kacper Duma 외, 2026, EASE 2026, arXiv 2605.02273. AI 생성 PR 대부분은 **리뷰를 받지 않고**, 리뷰되더라도 AI 에이전트가 주도. 사람의 관여는 독립 평가보다 "에이전트 조종" 형태.
- **Not All Agents Are Equal** — Obada Kraishan, 2026, arXiv 2609.17598 (프리프린트, 단독 저자). PR 37,623건. 되돌림률: Codex 6.1% vs 사람 11.5% vs Devin 14.5%. 에이전트 코드 전체로는 보안 스멜이 사람보다 적음(OR 0.63). Claude Code PR은 첫 사람 리뷰까지 중앙값 12.6시간.
- **Toward Instructions-as-Code: Understanding the Impact of Instruction Files on Agentic Pull Requests** — Ali Arabat, Mohammed Sayagh, 2026, MSR 2026, DOI 10.1145/3793302.3793601, arXiv 2606.13449. 프로젝트 148개·에이전트 PR 15,549건, 지시 파일 생성 전후 비교. 병합률이 20%p 이상 오른 프로젝트 27.7%, 내린 프로젝트 26.35% — **지시 파일이 자동으로 좋은 결과를 내지 않는다**. 병합률이 오른 프로젝트는 더 길고 절·하위 절로 잘 구조화된 파일을 가졌다(탐색적 관찰).
- **Do Autonomous Agents Contribute Test Code?** — Sabrina Haque, Sarvesh Ingale, Christoph Csallner, 2026, arXiv 2601.03556. 테스트 포함 PR은 시간이 갈수록 늘고 더 크며 오래 걸리지만 병합률은 비슷.
- **To What Extent Does Agent-generated Code Require Maintenance?** — Shota Sawada 외, 2026, EASE 2026, arXiv 2605.06464. AI 생성 파일의 유지보수는 덜 빈번하고, 유지보수 대부분을 **사람이** 수행.
- 책 활용: "리뷰 지표를 사람의 감독으로 읽으면 안 된다", "보안 규칙은 문서가 아니라 통제로" (아래 논문 22와 연결).

### 논문 11: Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study
- 저자·연도: You Wang, Michael Pradel, Zhongxin Liu, 2025
- 발표처: ICSE 2026 (S2 기준) · DOI 10.1145/3744916.3764576
- arXiv: 2503.15223
- 피인용수: 85
- 핵심 수치 [원문]: SWE-bench Verified에서 도구 3종의 "그럴듯한" 패치 분석. 검증 메커니즘 약점으로 패치의 **7.8%가 개발자 테스트를 실패하는데도 정답 처리**. 차등 테스트(PatchDiff)로 **29.6%가 정답 패치와 다르게 동작**. 동작이 다른 패치의 28.6%는 확실히 오답. 보고된 해결률이 **6.2%p 부풀려짐**.
- 인용할 만한 문장:
  > "However, because testing is rarely exhaustive, a patch may pass the tests but nevertheless fail to match the developers' expectations." (abstract)
- 책 활용: 가이드 02 "테스트가 통과한다고 문서와 다른 동작을 자동 승인하지 않습니다"의 직접 근거.

### 논문 12: Is Your Code Generated by ChatGPT Really Correct? (EvalPlus)
- 저자·연도: Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, Lingming Zhang, 2023
- 발표처: NeurIPS 2023 · arXiv 2305.01210
- 피인용수: 2,460
- 핵심 수치 [원문]: HumanEval 테스트를 80배 늘린 HumanEval+로 26개 LLM 재평가 → pass@k **최대 19.3~28.9% 하락**. 테스트 부족이 모델 순위까지 뒤바꿈.
- 책 활용: "수용 기준 하나에 테스트 하나"로는 부족하다 → 가이드 06의 AC-CAN-01~05(정상·실패·중복·지연·권한) 구성 논리.

### 논문 13: SWE-bench 및 오염·누수 비판
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan, ICLR 2024, arXiv 2310.06770, 피인용 4,603. 12개 Python 저장소의 실제 이슈 2,294개. 당시 최고 Claude 2가 1.96% 해결 [원문].
- **SWE-Bench+: Enhanced Coding Benchmark for LLMs** — Reem Aleithan, Haoran Xue, Mohammad Mahdi Mohajer, Elijah Nnorom, Gias Uddin, Song Wang, 2024, arXiv 2410.06992 (프리프린트). SWE-Agent+GPT-4 성공 패치의 **32.67%가 해법 누수**(이슈·댓글에 답이 있음), **31.08%가 약한 테스트로 인한 의심 패치**. 걸러내면 해결률 12.47% → 3.97%. 이슈의 94% 이상이 모델 지식 마감일 이전 생성 [원문].
- **The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason** — Shanchao Liang, Spandan Garg, Roshanak Zilouchian Moghaddam, 2025, arXiv 2506.12286 (S2: ICSE SEIP 계열, DOI 10.1145/3786583.3786882 — 정확한 트랙명 미확인). 이슈 설명만으로 버그 파일 경로 식별 정확도 **최대 76%**, SWE-bench 밖 저장소에서는 최대 53%. 5-gram 연속 일치 SWE-bench 최대 35% vs 다른 벤치마크 최대 18% → 암기·오염 의심 [원문].
- **Agentless: Demystifying LLM-based Software Engineering Agents** — Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang, 2024, arXiv 2407.01489. SWE-bench Lite에서 문제 일부가 정답 패치를 포함하거나 이슈 설명이 불충분·오도적임을 수작업 분류로 확인 → SWE-bench Lite-S 구성 [원문]. (다중 에이전트 비교는 6장 참조)
- **SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?** — Xiang Deng 외(Scale AI), 2025, arXiv 2509.16941. 41개 저장소의 1,865개 문제, 공개·보류·상용 세트로 분할한 오염 저항형 설계, 모든 과제를 사람이 검증하고 "해결 가능하도록 충분한 맥락을 보강" [원문]. 후속으로 2026년 9~10월 "SWE-Bench Pro Verified"(arXiv 2609.08149)·"SWE-Bench Pro V2"(arXiv 2610.24206)가 보상 해킹·과제 품질 문제(오도하는 문제 설명, 잘못 범위 잡힌 테스트)를 다시 지적 — 상세 수치 미확인.
- 책 활용: "벤치마크 점수는 당신 저장소의 증거가 아니다." SWE-bench Pro가 과제에 "해결 가능하도록 맥락을 보강"해야 했다는 사실 자체가 **명세 품질이 해결 가능성을 좌우한다**는 책 주장의 방증.

---

## 2. 에이전트 컨텍스트 파일(AGENTS.md / CLAUDE.md / 규칙 파일) 실증 연구

### 논문 14: On the Use of Agentic Coding Manifests: An Empirical Study of Claude Code
- 저자·연도: Worawalan Chatlatanagulchai, Kundjanasith Thonglek, Brittany Reid, Yutaro Kashiwa, Pattara Leelaprute, Arnon Rungsawang, Bundit Manaskasemsak, Hajimu Iida, 2025
- 발표처: PROFES 2025 · DOI 10.1007/978-3-032-12089-2_40 · arXiv 2509.14744
- 핵심 수치 [원문]: 242개 저장소의 CLAUDE.md 253개. 얕은 계층(주 제목 1개 + 하위 절 몇 개), 내용은 **운영 명령, 기술 구현 메모, 상위 아키텍처**가 지배.

### 논문 15: Agent READMEs: An Empirical Study of Context Files for Agentic Coding
- 저자·연도: Worawalan Chatlatanagulchai, Hao Li, Yutaro Kashiwa, Brittany Reid, Kundjanasith Thonglek, Pattara Leelaprute, Arnon Rungsawang, Bundit Manaskasemsak, Bram Adams, Ahmed E. Hassan, Hajimu Iida, 2025
- 발표처: ACM TOSEM (S2 기준) · DOI 10.1145/3840295 · arXiv 2511.12884
- 피인용수: 43
- 핵심 수치 [원문]: 1,925개 저장소의 컨텍스트 파일 2,303개. 정적 문서가 아니라 **설정 코드처럼 잦고 작은 추가로 진화**하며 읽기 어렵다. 지시 유형 16종 중 테스트 절차 75.9%, 구현 세부 70.8%, 아키텍처 68.1%. **보안 14.8%, 성능 14.5%** — 비기능 요구는 거의 명시되지 않음.
- 인용할 만한 문장:
  > "These findings indicate that while developers use context files to make agents functional, they provide few guardrails to ensure that agent-written code is secure or performant, highlighting the need for improved tools and practices." (abstract)
- 책 활용: 가이드 04 "비기능 요구사항도 관찰 가능한 문장으로"의 현장 공백 데이터. 한국 독자에게 "당신의 CLAUDE.md에 보안·성능 절이 있는가?" 체크 질문으로.

### 논문 16: Context Engineering for AI Agents in Open-Source Software
- 저자·연도: Seyedmoein Mohsenimofidi, Matthias Galster, Christoph Treude, Sebastian Baltes, 2025
- 발표처: MSR 2026 · DOI 10.1145/3793302.3793350 · arXiv 2510.21413
- 핵심 수치 [원문]: OSS 466개 프로젝트의 AGENTS.md 채택 예비 연구. **정해진 내용 구조가 아직 없음**, 맥락 제공 방식이 서술형·처방형·금지형·설명형·조건형으로 다양.
- 관련 후속 [원문]: **Harness Engineering for Agentic AI Coding Tools: An Exploratory Study** — Matthias Galster 외, 2026, arXiv 2602.14690 (AIware 2026 논문 기반 확장판). 설정 메커니즘 8종 식별, GitHub 저장소 2,853개 분석. 컨텍스트 파일이 지배적이고 흔히 유일한 메커니즘, Skills·Subagents 채택은 드묾, Skills는 실행 스크립트보다 정적 지시에 의존.
- 관련 후속 [원문]: **An Exploratory Study of Agent Plans for Agentic AI Coding Tools in Open-Source Software** — Muhammad Auwal Abubakar 외, ESEM 2026 (Emerging Results), arXiv 2608.04661. 저장소 36,710개 선별 → 10개 저장소의 plan 파일 85개만 발견(매우 드묾). 계획 파일은 구현 단계, 구체 파일·위치, 테스트·검증 정보를 주로 담음.
- 책 활용: 가이드 02 "폴더보다 중요한 것은 원본의 책임"의 대비 사례 — 업계는 아직 컨텍스트 파일 구조에 합의가 없다. plan/ 문서를 저장소에 남기는 관행이 드물다는 점은 가이드 02의 plan/ 위치 제안과 대비된다.

### 논문 17: Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?
- 저자·연도: Thibaud Gloaguen, Niels Mündler-Sasahara, Mark Niklas Müller, Veselin Raychev, Martin Vechev, 2026
- 발표처: arXiv 프리프린트 · arXiv 2602.11988
- 피인용수: 33
- 요약 [원문]: SWE-bench Lite(300개)에 LLM 생성 컨텍스트 파일을 붙인 조건과, 개발자가 커밋한 컨텍스트 파일이 있는 저장소 12개의 138개 이슈로 만든 새 벤치마크 **CTXbench**에서 평가. 에이전트·모델: Claude Code(Sonnet-4.5), Codex(GPT-5.2, GPT-5.1 mini), Qwen Code(Qwen3-30b-coder).
- 핵심 수치 [원문, HTML 본문]:
  - LLM 생성 파일 vs 없음: 해결률 −0.5%(SWE-bench, p=0.87), −2%(CTXbench, p=0.37). 유의하지 않음
  - 개발자 작성 파일 vs 없음: +2.4%(CTXbench, p=0.21). 유의하지 않음
  - 개발자 작성 vs LLM 생성: 개발자 작성이 평균 **7%p 높음**(p=0.038)
  - 비용: LLM 생성 파일로 약 20%(SWE-bench)·23%(CTXbench) 증가, 개발자 작성 파일은 최대 19%
  - 파일에 `uv`를 언급하면 인스턴스당 약 1.6회 사용, 언급 없으면 0.01회 미만 → **지시는 잘 따름**
  - 저장소 개요(overview)는 도움이 안 됨. LLM 생성 파일의 95~100%가 개요를 포함
- 인용할 만한 문장:
  > "Specifically, we find that while instructions in the context files are well followed by coding agents, repository overviews, although popular and recommended by model providers, are not helpful." (abstract)
  > "We conclude that while context files are useful for specifying non-standard coding practices, any attempts to improve performance should be rigorously evaluated before deployment." (abstract)
- 책 활용: 이 책의 중심 근거 중 하나. **"AI가 만든 AGENTS.md를 그대로 쓰지 말라 — 사람이 쓴 비표준 관행·금지 규칙이 가치를 만든다."** 가이드 10 "모든 문서를 무조건 넣기보다 필요한 원본과 관련 연결만 포함합니다"와 정확히 맞물린다.

### 논문 18: On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents
- 저자·연도: Jai Lal Lulla, Seyedmoein Mohsenimofidi, Matthias Galster, Jie M. Zhang, Sebastian Baltes, Christoph Treude, 2026
- 발표처: arXiv 프리프린트(5쪽 단편) · arXiv 2601.20404
- 핵심 수치 [원문]: 저장소 10개, PR 124건, AGENTS.md 유무 비교. 있을 때 실행 시간 중앙값 **−28.64%**, 출력 토큰 **−16.58%**, 과제 완료 행동은 비슷.
- 책 활용: 논문 17과 짝. "정확도는 안 오르고 비용은 오른다"(17) vs "효율은 오른다"(18). 결론이 갈리는 이유 = 과제 표본·측정 지표 차이. 책에서는 **"컨텍스트 파일의 효과는 측정해서 확인하라"**는 메시지로 정리.

### 논문 19: Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories
- 저자·연도: Prakhar Khatri, 2026
- 발표처: arXiv 프리프린트(단독 저자) · arXiv 2607.27250
- 핵심 수치 [원문]: Claude Code·Codex, 저장소 3개의 실제 과제 17개, 평가 실행 288회. 컨텍스트 전략이 정확도를 측정 가능하게 바꾸지 못함(동등성 검정으로 10~15%p 이내). 실패 원인은 저장소 지식 부족이 아니라 **구현 기술**(기능 설계, 패턴 선택, 정확한 연결). 실제 AGENTS.md가 아깝게 실패한 사례를 통과로 바꾼 적이 없음. 과제 난이도 경계가 에이전트마다 다름(Spearman ρ=0.75) → 선행 연구 결과가 엇갈리는 이유 후보.

### 논문 20: Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and Persistent Configuration for Coding Agents
- 저자·연도: Xing Zhang, Guanghui Wang, Yanwei Cui, Wei Qiu, Ziyuan Li, Bing Zhu, Peiyang He, 2026
- 발표처: arXiv 프리프린트 · arXiv 2604.11088
- 핵심 수치 [원문]: 규칙 파일 679개(규칙 25,532개) 수집, Claude Code(Claude Opus 4.6)로 SWE-bench Verified에서 에이전트 실행 5,000회 이상.
  - **무작위 규칙도 전문가 규칙만큼 성능을 올림**(둘 다 판별 부분집합에서 +13.8%p) → 내용보다 "맥락 점화(priming)" 효과
  - 개별적으로 이로운 규칙은 **모두 금지형**("do not refactor unrelated code"), 해로운 규칙은 **모두 긍정 지시형**("follow code style")
  - 규칙 0~50개에서 통과율 안정
- 인용할 만한 문장:
  > "...they yield a clear principle for safer agent configuration: constrain what agents must not do, rather than prescribing what they should." (abstract)
- 책 활용: 가이드 10 프롬프트 4 "금지: 범위 밖 리팩터링, 테스트 삭제로 통과 만들기, 미실행 검증 주장"이 왜 금지형으로 쓰였는지를 설명하는 근거. 단, 무작위 규칙도 효과가 있다는 결과는 "규칙 내용이 무엇이든 효과"라는 해석 위험이 있으므로 함께 제시한다.

### 논문 21: Stale Instruction Files Override the Code in Coding Agents: A One-Sentence Fix
- 저자·연도: Xiaonan Xu, Wenjing Wu, 2026
- 발표처: arXiv 프리프린트(SN Computer Science 투고) · arXiv 2610.30571 (게시 2026-10-22, 매우 최신)
- 핵심 수치 [원문]: 지시 파일이 기존 코드와 다른 관례를 요구하는 Python 프로젝트 40개(예: logging 대신 print), Claude Code·Codex CLI 320회 실행.
  - 지시 파일과 코드가 충돌할 때 **90.1%가 오래된 지시 파일을 따름**
  - Claude Code는 80회 중 79회 충돌을 **지적하고도** 파일을 따름
  - Codex CLI는 80회 중 20회 기존 코드를 파일에 맞게 다시 쓰고, 그중 17회에서 프로젝트 테스트가 실패
  - 사용자 지시 파일에 "기존 코드를 우선하라"는 한 문장 추가 → 코드를 따르는 비율 4.2% → 91.4%, 테스트 통과율 89.4% → 100%
- 인용할 만한 문장:
  > "We attribute the behaviour to how agents receive the two sources: the instruction file reaches the model as an instruction and the code as tool output, which models are trained to rank lower." (abstract)
- 책 활용: 가이드 12 "문서가 오래됐는지는 수정 날짜만이 아니라 실제 변경과의 불일치로 판단합니다"와 가이드 02 "하나의 결정에는 하나의 권위 있는 원본"의 강력한 사례. **오래된 문서는 에이전트에게 '지시'로 들어가 코드보다 우선한다** → 원본 책임과 갱신 경로가 왜 필수인지. 동료 심사 전이므로 "최근 보고" 수준으로 인용.

### 논문 22: 컨텍스트 파일과 실행 가능한 통제 — 보조 연구 묶음
- **When "Do Not" Is Not Deny: Security Rules in CLAUDE.md vs Built-In Controls** — Ting Yan, 2026, arXiv 2608.23550 (프리프린트, 단독 저자). 공개 CLAUDE.md 481개의 보안 규칙 중 Claude Code 내장 통제(권한 규칙·모드·샌드박스)와 대응하는 것은 **약 4~16%**, 가장 엄격한 기준 4.4%(95% CI 2.6~6.7%). 저자 표현: CLAUDE.md는 "write-only channel" — 규칙을 써도 강제되는지 피드백이 없다 [원문].
- **ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files** — Reshabh K Sharma, 2026, arXiv 2603.00822 (프리프린트, 단독 저자). 자연어 지시를 AST 질의·셸 심(shim)·아키텍처 검증기로 컴파일. SWE-bench Lite 300개에서 제약 준수 **88.3%** vs 프롬프트만 67.0% vs LLM 반성 50.3%, 피드백 비용 3.4배 감소 [원문].
- **Instruction Adherence in Coding Agent Configuration Files: A Factorial Study of Four File-Structure Variables** — Damon McMillan, 2026, arXiv 2605.10039 (프리프린트, 단독 저자). Claude Code 세션 1,650회. 파일 크기·지시 위치·파일 구조·인접 파일 모순 모두 **검출 가능한 효과 없음**. 가장 큰 효과는 세션 내부: 함수를 하나 더 생성할 때마다 준수 오즈 약 5.6% 감소(OR 0.944, 비단조) [원문].
- **Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding** — Kushal Chakrabarti, 2026, arXiv 2608.11095 (프리프린트, 단독 저자). 저장소 1,867개의 지시 수명 247,694개. 지시 파일은 생애 동안 **+226%** 커지고 커밋당 순 +4.9개 지시가 늘며, 오래된 지시일수록 삭제되지 않음. 원인: 지시의 **근거(rationale)가 사라지면 삭제가 위험**해짐. "프롬프트 주석"으로 근거를 남기면 과잉 지시를 대부분 제거 [원문].
- **Package Hallucination Attacks on Coding Agents through Prompt Injection in Rule Files** — Yupu Wang, Zhengyuan Jiang, Reachal Wang, Neil Zhenqiang Gong, 2026, arXiv 2610.09264. 공유 규칙 파일에 악성 프롬프트를 넣어 의존성을 공격자 패키지로 바꾸게 하는 공격 [원문, 수치 미확인].
- 책 활용:
  - "do not"은 deny가 아니다 → 가이드 09 "자동 검사와 사람의 검토를 분담" 표에 "문서 규칙 → 실행 가능한 검사로 승격" 행을 추가하는 논거.
  - CLAUDE.md가 커지기만 하는 이유가 "근거 상실"이라는 분석은 **ADR이 왜 필요한가**를 에이전트 시대 언어로 다시 말해 준다(가이드 08). 매우 좋은 장 연결 고리.

---

## 3. 요구공학·명세·테스트 주도 생성과 LLM

### 논문 23: Large Language Models (LLMs) for Requirements Engineering (RE): A Systematic Literature Review
- 저자·연도: Mohammad Amin Zadenoori, Jacek Dąbrowski, Waad Alhoshan, Liping Zhao, Alessio Ferrari, 2025
- 발표처: arXiv 프리프린트 · arXiv 2509.11446 · 피인용 59
- 핵심 [원문]: 2023~2024년 1차 연구 74편. 과거 NLP4RE가 결함 탐지·분류 중심이었다면 LLM 연구는 **도출·검증** 중심. 대부분 GPT 계열, zero/few-shot, 통제 환경 평가, **산업 적용·복잡한 워크플로 통합은 제한적**.
- 보조 서베이: Andreas Vogelsang, Jannik Fischbach, "Using Large Language Models for Natural Language Processing Tasks in Requirements Engineering: A Systematic Guideline", 2024, arXiv 2402.13823.
- 책 활용: "LLM으로 요구사항 쓰기"에 관한 학계 증거가 아직 실험실 수준이라는 현실 고지.

### 논문 24: Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering
- 저자·연도: Sanidhya Vijayvargiya, Xuhui Zhou, Akhila Yerukola, Maarten Sap, Graham Neubig, 2025
- 발표처: ICLR 2026 (arXiv 코멘트 기준) · arXiv 2502.13069 · 피인용 53
- 핵심 수치 [원문]: SWE-bench Verified의 명세 부족 변형 Ambig-SWE. 모델은 **명세가 충분한 지시와 부족한 지시를 구분하지 못함**. 명세가 부족할 때 상호작용하면 비상호작용 대비 **최대 74%** 성능 향상.
- 인용할 만한 문장:
  > "Making unwarranted assumptions to compensate for the missing information and failing to ask clarifying questions can lead to suboptimal outcomes, safety risks due to tool misuse, and wasted computational resources." (abstract)
- 책 활용: 가이드 14 "AI가 그럴듯하게 채운 빈칸을 확정"의 직접 근거. 에이전트는 스스로 "모르는 것"을 묻지 않으므로 **미결정 목록을 사람이 명시**해야 한다(가이드 04 "결정과 미결정", 가이드 10 프롬프트 1 "확인되지 않은 수요·숫자·정책은 추정이라고 표시하라").

### 논문 25: ClarifyGPT / HumanEvalComm / ClarifyCodeBench — 명확화 질문 연구 묶음
- **ClarifyGPT: Empowering LLM-based Code Generation with Intention Clarification** — Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang, Chenxue Wang, Shichao Liu, Qing Wang, 2023, arXiv 2310.10996 (FSE 2024 게재로 알려져 있으나 S2에서 확인 못 함 → 발표처 미확인). 모호성 탐지 → 질문 → 요구 정제. GPT-4 Pass@1 MBPP-sanitized 70.96% → 80.80%, 4개 벤치마크 평균 GPT-4 68.02% → 75.75% [원문].
- **HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent** — Jie JW Wu, Fatemeh H Fard, ACM TOSEM 2025, DOI 10.1145/3715109, arXiv 2406.00215. 문제 설명을 불일치·모호·불완전 3유형으로 변형해 모델이 질문하는지 측정 [원문].
- **ClarifyCodeBench** — Zheng Fang 외, 2026, arXiv 2607.00711 (프리프린트). 코드 생성 능력이 강하다고 요구 명확화 능력이 강하지 않음("Capability Decoupling"), 추론을 늘려도 모호성 식별은 거의 개선되지 않음, 모호성 밀도가 높아지면 명확화 성능 급락 [원문].
- 책 활용: "추론 모델을 쓰면 알아서 물어볼 것"이라는 기대에 대한 반증.

### 논문 26: Requirements are All You Need: From Requirements to Code with LLMs
- 저자·연도: Bingyang Wei, 2024 · arXiv 2406.10101 (프리프린트, 단독 저자, 사례 연구)
- 요약 [원문]: 잘 구조화된 요구 문서에서 기능 요구 추출 → 객체지향 모델 → 단위 테스트 → 코드 순으로 단계적 프롬프트("Progressive Prompting"). 웹 프로젝트 사례 연구로 시연. 정량 평가 없음.
- 책 활용: "명세 → 설계 → 테스트 → 코드" 순서의 개념적 선례 정도로만. 근거 강도 낮음.

### 논문 27: Testing the Effect of Code Documentation on Large Language Model Code Understanding
- 저자·연도: William Macke, Michael Doyle (MITRE), 2024
- 발표처: Findings of NAACL 2024 · arXiv 2404.03114
- 핵심 [원문]: **"틀린" 문서는 LLM의 코드 이해를 크게 방해**하지만, 불완전하거나 없는 문서는 유의한 영향이 없어 보임.
- 인용할 만한 문장:
  > "We show that providing an LLM with "incorrect" documentation can greatly hinder code understanding, while incomplete or missing documentation does not seem to significantly affect an LLM's ability to understand code." (abstract)
- 책 활용: 가이드 02 "피해야 할 중복"(spec·UX·plan이 서로 다른 취소 규칙)의 위험을 정량적으로 뒷받침. **"문서를 많이"가 아니라 "틀린 문서를 없게"**. 논문 21(오래된 지시 파일)과 한 쌍으로 쓰면 강하다. 단, 모델이 오래된 세대(2023~2024)라는 한계 명시.

### 논문 28: Test-Driven Development for Code Generation
- 저자·연도: Noble Saji Mathews, Meiyappan Nagappan, 2024
- 발표처: ASE 2024 · DOI 10.1145/3691620.3695527 · arXiv 2402.13521 · 피인용 96
- 핵심 [원문]: GPT-4·Llama 3에 문제 설명과 함께 **테스트를 제공**하면 MBPP·HumanEval에서 일관되게 성공률이 높아짐. (abstract에 정확한 %p 없음 → 수치는 본문 확인 필요, 미확인)
- 책 활용: 가이드 06 SLICE-CAN-01 "계약·실패 가짜 서버 작성 → 상태·권한·원자성 테스트 → 접수 API" 순서의 근거.

### 논문 29: LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation (TiCoder)
- 저자·연도: Sarah Fakhoury, Aaditya Naik, Georgios Sakkas, Saikat Chakraborty, Shuvendu K. Lahiri, 2024
- 발표처: IEEE TSE 50(9):2254–2268 · DOI 10.1109/TSE.2024.3428972 · arXiv 2404.10100 · 피인용 176
- 핵심 수치 [원문]: 테스트를 통한 의도 명확화("부분적 형식화") 워크플로. 사용자 15명 혼합 연구에서 AI 코드를 **올바르게 평가할 가능성이 유의하게 높고**, 과제 유발 **인지 부하가 유의하게 낮음**. 4개 LLM·2개 데이터셋에서 사용자 상호작용 5회 이내 pass@1 **평균 절대 +45.97%p**.
- 책 활용: "테스트는 명세다" — 가이드 06의 Given/When/Then 수용 기준을 에이전트에게 먼저 주는 이유. 인지 부하 감소는 5장(인간 요인)과도 연결.

### 논문 30: Clover: Closed-Loop Verifiable Code Generation
- 저자·연도: Chuyue Sun, Ying Sheng, Oded Padon, Clark Barrett, 2023
- 발표처: SAIV 2024 (S2 기준) · arXiv 2310.17807 · 피인용 106
- 핵심 수치 [원문]: 코드·docstring·형식 주석(Dafny) 3자 간 일관성 검사. CloverBench에서 올바른 사례 수용률 **최대 87%**, 적대적 오답은 **거짓 양성 0**. 기존 사람 작성 데이터셋 MBPP-DFY-50에서 잘못된 프로그램 6개 발견.
- 책 활용: "문서·계약·코드가 서로를 검증한다"는 가이드 02·05의 추적성 사상을 형식 검증 쪽에서 보여 주는 사례. 독자 대부분이 Dafny를 쓰지 않으므로 "일관성 검사"라는 아이디어만 전달.

### 논문 31: Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions? (nl2postcond)
- 저자·연도: Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, Shuvendu K. Lahiri, 2024
- 발표처: FSE 2024 (PACMSE) · DOI 10.1145/3660791 · arXiv 2310.01831 · 피인용 145
- 핵심 [원문]: 자연어 의도 → 실행 가능한 사후조건(assertion). 생성된 사후조건은 대체로 정확하고 오답 코드를 판별. **Defects4J의 실제 과거 버그 64개 포착**.
- 책 활용: 가이드 05 "불변식"(INV-CAN-02 "검증된 환불 성공 전에는 CANCELLED로 전이하지 않습니다")을 assertion으로 바꾸는 실천의 근거. "도메인 규칙을 실행 가능한 형태로" 절에 적합.

### 논문 32: We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs
- 저자·연도: Joseph Spracklen, Raveen Wijewickrama, A H M Nazmus Sakib, Anindya Maiti, Bimal Viswanath, Murtuza Jadliwala, 2024/2025
- 발표처: USENIX Security 2025 · arXiv 2406.10279 · 피인용 139
- 핵심 수치 [원문]: LLM 16종, 코드 샘플 576,000개(Python·JavaScript). 환각 패키지 비율 평균 **상용 모델 최소 5.2%, 오픈소스 21.7%**, 고유 환각 패키지명 **205,474개**.
- 책 활용: 가이드 09 "코드 CI"·"출시 게이트"에 의존성 검증이 들어가야 하는 이유. ADR "외부 의존성" 결정(가이드 08)과 연결.

### 논문 33: Large Language Models Cannot Self-Correct Reasoning Yet
- 저자·연도: Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, Denny Zhou, 2023
- 발표처: ICLR 2024 · arXiv 2310.01798 · 피인용 1,395
- 핵심 [원문]: 외부 피드백 없이 자기 능력만으로 교정하는 "내재적 자기 교정"은 추론에서 어렵고, **교정 후 성능이 오히려 떨어지기도** 한다.
- 인용할 만한 문장:
  > "...our research indicates that LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction." (abstract)

### 논문 34: When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs
- 저자·연도: Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, Rui Zhang, 2024
- 발표처: TACL 12:1417–1440 · DOI 10.1162/tacl_a_00713 · arXiv 2406.01297 · 피인용 408
- 핵심 [원문, 3가지 결론]: (1) 자기 교정에 특별히 적합한 과제를 빼면 **프롬프트된 LLM의 피드백으로 성공한 선행 연구가 없음**, (2) **신뢰할 수 있는 외부 피드백**을 쓸 수 있는 과제에서는 잘 작동, (3) 대규모 미세조정으로 가능.
- 책 활용 (33+34): 가이드 07 "다른 AI 역할의 반박은 누락 탐지에 유용하지만 독립적인 현실 검증은 아닙니다"의 학술 근거. 핵심 문장으로 정리: **"AI는 테스트·컴파일러·계약 검사 같은 외부 신호가 있을 때만 스스로 고친다."** → 검증 명령을 입력 꾸러미에 넣는 이유(가이드 10).

### 논문 35: Correlated Errors in Large Language Models
- 저자·연도: Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg, 2025
- 발표처: ICML 2025 · arXiv 2506.07962 · 피인용 71
- 핵심 수치 [원문]: LLM 350개 이상 평가. 한 리더보드 데이터셋에서 **두 모델이 모두 틀릴 때 60% 확률로 같은 오답**. 공유 아키텍처·제공사가 상관을 키우지만, **더 크고 정확한 모델일수록** 아키텍처·제공사가 달라도 오류 상관이 높음. LLM-as-judge 평가와 채용에서 하류 효과 확인.
- 인용할 만한 문장:
  > "We find substantial correlation in model errors -- on one leaderboard dataset, models agree 60% of the time when both models err." (abstract)

### 논문 36: Great Models Think Alike and this Undermines AI Oversight
- 저자·연도: Shashwat Goel, Joschka Struber, Ilze Amanda Auzina, Karuna K Chandra, Ponnurangam Kumaraguru, Douwe Kiela, Ameya Prabhu, Matthias Bethge, Jonas Geiping, 2025
- 발표처: ICML 2025 (S2 기준) · arXiv 2502.04313 · 피인용 75
- 핵심 [원문]: 오류 겹침 기반 유사도 지표 CAPA 제안. LLM 판정자는 **자신과 비슷한 모델을 편애**. 능력이 높아질수록 **모델 오류가 서로 비슷해지는 추세** → 상관된 실패 위험.

### 논문 37: LLM Evaluators Recognize and Favor Their Own Generations
- 저자·연도: Arjun Panickssery, Samuel R. Bowman, Shi Feng, 2024
- 발표처: NeurIPS 2024 · arXiv 2404.13076 · 피인용 962
- 핵심 [원문]: GPT-4·Llama 2는 자기 출력을 구분하는 능력이 있고, 자기 인식 능력과 **자기 선호 편향**의 강도가 선형 상관.
- 책 활용 (35~37): 가이드 07 "같은 잘못된 가정을 공유할 수 있습니다"를 정량으로. "구현 에이전트와 리뷰 에이전트를 다른 모델로 바꾸면 독립 검증이 된다"는 흔한 믿음도 논문 35·36 결과로 약해진다(큰 모델일수록 오류가 비슷). 결론: **위험에 맞는 증거 종류(실행 실험·사용자 관찰·책임자 승인)를 고르라**는 가이드 07 문장으로 착지.

### 논문 38: Can LLMs Replace Manual Annotation of Software Engineering Artifacts?
- 저자·연도: Toufique Ahmed, Premkumar Devanbu, Christoph Treude, Michael Pradel, 2024 · arXiv 2408.05534 (MSR 2025 게재로 알려졌으나 S2 미조회 → 발표처 미확인)
- 핵심 [원문]: 10개 주석 과제 중 일부에서 LLM 대체가 사람 간 일치도에 근접. **모델-모델 일치도**를 "이 과제를 LLM에 맡겨도 되는가"의 예측 지표로 제안.
- 책 활용: AI 리뷰를 전면 부정하지 않는 균형 근거. "어떤 검토는 AI로, 어떤 검토는 사람으로" 분담표(가이드 09)에 근거 부여.

### 논문 39: 보조 — 긴 맥락과 정보 위치
- **Lost in the Middle: How Language Models Use Long Contexts** — Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang, TACL 2024, DOI 10.1162/tacl_a_00638, arXiv 2307.03172, 피인용 5,704. 관련 정보가 입력 처음·끝에 있을 때 성능이 가장 높고 **중간에 있으면 크게 떨어짐** [원문].
- 주의: 2023년 모델 기준이다. 논문 22의 McMillan(2026)은 지시 위치 효과를 검출하지 못했다. 책에서는 "모든 문서를 다 넣으면 오히려 묻힐 수 있다"는 직관 수준으로만 쓰고, 최신 모델에서 같은 크기라고 단정하지 않는다.

---

## 4. 설계 결정 기록(ADR)·설계 근거·추적성·문서 부채

### 논문 40: Software Architecture as a Set of Architectural Design Decisions
- 저자·연도: Anton Jansen, Jan Bosch, 2005
- 발표처: WICSA 2005 (5th Working IEEE/IFIP Conference on Software Architecture, Pittsburgh) [2차: ICSA 학회 아카이브]
- DOI: 미확인
- 핵심 [2차]: 아키텍처를 컴포넌트·커넥터가 아니라 **설계 결정의 집합**으로 본다. 결정의 근거·제약·대안이 기록되지 않으면 사라지는 문제를 다룸. 이 문제를 흔히 "설계 결정 지식의 증발(knowledge vaporization)"이라 부르며 Bosch(2004, "Software Architecture: The Next Step", EWSA)와 이 논문에서 유래한 개념으로 인용된다 — 단, **"vaporization"이라는 정확한 표현이 이 논문 원문에 있는지는 미확인**.
- 책 활용: 가이드 08 "결정은 남기고 아이디어는 승격합니다"의 고전적 뿌리. 본문에서 "증발"이라는 단어를 쓸 때는 "흔히 그렇게 부른다"로 쓰고 원문 인용 형식은 피한다.

### 논문 41: Architecture Decisions: Demystifying Architecture
- 저자·연도: Jeff Tyree, Art Akerman, 2005
- 발표처: IEEE Software 22(2):19–27 · IEEE Xplore 문서 1407822 [2차]
- 핵심 [2차]: 주요 아키텍처 결정을 문서화해 근거를 모든 이해관계자에게 보이게 하자는 주장과 결정 기록 템플릿 제안.
- 참고: ADR이라는 경량 형식은 Michael Nygard의 2011년 블로그 글 "Documenting Architecture Decisions"에서 대중화되었다(논문 아님, web-researcher 영역).

### 논문 42: ADR 채택 실증
- **Using Architecture Decision Records in Open Source Projects—An MSR Study on GitHub** — Georg Buchgeher, Stefan Schöberl, Verena Geist, Bernhard Dorninger, Philipp Haindl, Rainer Weinreich, IEEE Access 11:63725–63740, 2023, DOI 10.1109/ACCESS.2023.3287654 [2차: JKU 연구 포털·DOAJ]. ADR 채택은 **여전히 낮지만 해마다 증가**. ADR 저장소의 약 절반은 기록이 1~5개뿐(시도만 하고 정착 못 함). 체계적으로 쓰는 저장소에서는 2명 이상이 장기간 함께 기록. 대부분 Nygard 템플릿 사용.
- **Architecture Decision Records Adoption Impact and Developer Engagement in Open Source** — Enio Garcia de Santana Junior 외, ICSA 2026 [2차: 학회 프로그램 페이지]. ADR 5,800개 중 **약 63%가 처음부터 "accepted" 상태로 생성** — ADR이 담아야 할 숙의 과정을 건너뜀. 전체 저자 목록·DOI 미확인.
- 책 활용: 가이드 08 "Draft → Accepted → Superseded" 상태 전이가 현실에서 지켜지지 않는다는 데이터. "ADR을 쓰는 것"과 "결정을 숙의하는 것"은 다르다.

### 논문 43: LLM과 설계 근거·ADR 생성
- **Can LLMs Generate Architectural Design Decisions? An Exploratory Empirical Study** — Rudra Dhar, Karthik Vaidhyanathan, Vasudeva Varma, ICSA 2024, DOI 10.1109/ICSA59870.2024.00016, arXiv 2403.01709, 피인용 72. ADR의 Context가 주어졌을 때 Decision 생성: zero-shot GPT-4는 관련성 있고 정확한 결정을 만들지만 **사람 수준에는 못 미침** [원문].
- **Using LLMs in Generating Design Rationale for Software Architecture Decisions** — Xiyu Zhou, Ruiyin Li, Peng Liang, Beiqi Zhang, Mojtaba Shahin, Zengyang Li, Chen Yang, ACM TOSEM 2025, DOI 10.1145/3785010, arXiv 2504.20781. 아키텍처 문제 100개(SO 50, GitHub 이슈 25, 토론 25), LLM 5종·프롬프트 전략 3종. 전문가 근거 대비 정밀도 **0.267~0.278**, 재현율 **0.627~0.715**, F1 0.351~0.389. 전문가가 언급하지 않은 논거 중 64.45~69.42%는 유용, 4.12~4.87%는 정확성 불확실, **1.59~3.24%는 오도 가능** [원문].
- 후속(참고): DRAFT-ing Architectural Design Decisions using LLMs (Dhar 외, 2025, arXiv 2504.08207), GADR(회의록에서 ADR 추출, 2026, arXiv 2608.17694), 커밋에서 설계 결정 추출(ECSA 2026 워크숍, arXiv 2609.03721).
- 책 활용: "AI에게 ADR 초안을 쓰게 하라. 단, 결정은 사람이 한다." 재현율은 높고 정밀도는 낮다 = **대안 목록 뽑기에는 좋고, 결론으로는 위험**. 가이드 10 DESIGNER 역할("규칙·상태·계약의 대안과 비용을 제안", 금지 "미결정 정책을 확정 규칙처럼 작성하기")과 정확히 일치.

### 논문 44: Do developers benefit from requirements traceability when evolving and maintaining a software system?
- 저자·연도: Patrick Mäder, Alexander Egyed, 2015 (온라인 2014)
- 발표처: Empirical Software Engineering 20(2):413–441 · DOI 10.1007/s10664-014-9314-z [2차: JKU 연구 포털·GI 디지털 라이브러리·altmetric]
- 핵심 수치 [2차]: 피험자 71명의 통제 실험, 두 제3자 시스템(GanttProject, iTrust)에서 실제 유지보수 과제 수행. 추적성이 있을 때 **평균 24% 빠르고, 정답 솔루션을 평균 50% 더 많이** 만듦.
- 책 활용: 가이드 05 "추적성을 위한 연결 REQ → POL → API → AC"와 가이드 06의 8단계 추적 경로에 대한 **가장 직접적인 정량 근거**. AI 이전 연구이지만, 에이전트도 "변경 영향 찾기"를 해야 한다는 점에서 그대로 적용 가능하다는 논리로 연결(이 연결은 저자 주장이 아니라 책의 추론임을 명시).

### 논문 45: 추적성의 고전과 LLM 추적
- **An Analysis of the Requirements Traceability Problem** — Orlena C. Z. Gotel, Anthony C. W. Finkelstein, ICRE 1994, pp. 94–101, IEEE CS Press [2차: UCL Discovery]. 실무자 100명 이상 실증 연구 기반. 추적성 문제를 **명세 이전(pre-RS)**과 이후(post-RS)로 나누고, 추적성 문제 대부분이 **명세 이전 추적성 부족**(요구가 어디서 왜 왔는가) 때문이라고 결론.
  - 책 활용: 가이드 08 "brainstorming → ADR·domain·spec 승격" 절. 아이디어 메모에 "채택됨 + 대상 링크"를 남기는 행위가 바로 pre-RS 추적성.
- **Natural Language Processing for Requirements Traceability** — Jin L. C. Guo, Jan-Philipp Steghöfer, Andreas Vogelsang, Jane Cleland-Huang, 2024, arXiv 2405.10845 (NLP4RE 핸드북 장). 추적 링크 복구·유지 과제 개관 [원문].
- **Prompts Matter: Insights and Strategies for Prompt Engineering in Automated Software Traceability** — Alberto D. Rodriguez, Katherine R. Dearstyne, Jane Cleland-Huang, 2023, arXiv 2308.00229. LLM으로 추적 링크 예측 [원문, 정량 수치 abstract에 없음].
- 책 활용: "추적 링크를 사람이 다 만들 필요는 없다. 다만 ID 체계는 사람이 정한다."

### 논문 46: 문서 문제의 분류 — Software Documentation Issues Unveiled
- 저자·연도: Emad Aghajani, Csaba Nagy, Olga Lucero Vega-Márquez, Mario Linares-Vásquez, Laura Moreno, Gabriele Bavota, Michele Lanza, 2019
- 발표처: ICSE 2019 [2차: ICSE 2019 프로그램 페이지]
- 핵심 [2차]: 메일링 리스트·Stack Overflow·이슈·PR의 문서 관련 산출물 **878개**를 분석해 문서 이슈 분류 체계 구축. 후속 ICSE 2020 논문("Software documentation: the practitioners' perspective")에서 실무자 146명 설문으로 검증.
- 미확인: 분류 체계의 범주 수.
- 책 활용: "문서 문제는 '없음'보다 '틀림·낡음·불일치'가 더 문제"라는 관점의 배경 자료. 논문 27과 함께.

---

## 5. 인간 요인 — 자동화 편향·과의존·탈숙련·인지 부하·신뢰 보정

### 논문 47: Ironies of Automation
- 저자·연도: Lisanne Bainbridge, 1983
- 발표처: Automatica 19(6):775–779 [2차]
- 핵심 [2차]: 자동화는 사람의 문제를 없애기보다 키울 수 있다. 자동화가 발전할수록 남은 사람 역할(이상 감지·개입)이 더 중요해지지만, 그 능력은 자동화 때문에 쇠퇴한다.
- 책 활용: 가이드 10 마지막 문단 "AI 역할을 나누더라도 이 책임이 자동으로 이전되지는 않습니다"의 고전적 배경.

### 논문 48: Complacency and Bias in Human Use of Automation: An Attentional Integration
- 저자·연도: Raja Parasuraman, Dietrich H. Manzey, 2010
- 발표처: Human Factors 52(3):381–410 · DOI 10.1177/0018720810376055 [2차: SAGE·TU Berlin 저장소]
- 핵심 [2차]: 자동화 안주(complacency)와 자동화 편향(automation bias)은 주의(attention) 메커니즘으로 통합 설명된다. 초보·전문가 모두에서 나타나고 단순 연습으로 쉽게 없어지지 않음. 불완전한 보조 도구에서 누락 오류와 실행 오류를 모두 만든다.
- 책 활용: "전문가라서 괜찮다"는 반론에 대한 답.

### 논문 49: Do Users Write More Insecure Code with AI Assistants?
- 저자·연도: Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh, 2023
- 발표처: ACM CCS 2023, pp. 2785–2799 · DOI 10.1145/3576915.3623157 · arXiv 2211.03622 · 피인용 494
- 핵심 [원문]: AI 도우미(codex-davinci-002)를 쓴 참가자가 **유의하게 덜 안전한 코드**를 작성했고, 동시에 **자기 코드가 안전하다고 더 믿었다**. AI를 덜 신뢰하고 프롬프트를 적극 다듬은 참가자의 코드가 취약점이 적었다.
- 미확인: 참가자 수(abstract에 없음).
- 책 활용: METR의 "체감과 실측의 괴리"와 같은 구조 — **확신은 증거가 아니다.**

### 논문 50: Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions
- 저자·연도: Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, Ramesh Karri, 2022
- 발표처: IEEE S&P 2022 · arXiv 2108.09293 · 피인용 1,068
- 핵심 수치 [원문]: 고위험 CWE 관련 시나리오 89개, 프로그램 1,689개 생성, **약 40%가 취약**.
- 책 활용: 보안 불변식을 domain/권한 정책으로 명시해야 하는 이유(가이드 05 "권한: 주체 × 자원 × 행위 × 조건"). 2021년 모델 기준이라는 시점 명시 필요.

### 논문 51: How AI Impacts Skill Formation
- 저자·연도: Judy Hanwen Shen, Alex Tamkin (Anthropic), 2026
- 발표처: arXiv 프리프린트 · arXiv 2601.20245 · 피인용 47
- 핵심 수치 [원문, HTML 본문]: 참가자 52명(그룹당 26명), 비교적 덜 알려진 Python 비동기 라이브러리 **Trio**를 새로 익히는 무작위 실험. AI 그룹이 27점 만점 퀴즈에서 **4.15점 낮음(17% 차이, Cohen's d=0.738, p=0.010)**. 완료 시간은 유의한 단축 없음. 상호작용 패턴 6종: 저득점(40% 미만) — AI 위임, 점진적 AI 의존, 반복적 AI 디버깅 / 고득점(65% 이상) — 생성 후 이해, 코드+설명 혼합, 개념 질문.
- 인용할 만한 문장:
  > "We find that AI use impairs conceptual understanding, code reading, and debugging abilities, without delivering significant efficiency gains on average." (abstract)
  > "Our findings suggest that AI-enhanced productivity is not a shortcut to competence..." (abstract)
- 책 활용: AI를 감독하려면 감독할 능력이 있어야 한다 → "설계 문서를 직접 쓰는 행위"가 개발자의 이해를 지키는 장치라는 논거. 고득점 패턴("생성 후 이해", "개념 질문")을 실천 팁으로.

### 논문 52: 인지·과의존 보조 연구 묶음
- **The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers** — Hao-Ping (Hank) Lee, Advait Sarkar, Lev Tankelevitch, Ian Drosos, Sean Rintel, Richard Banks, Nicholas Wilson, CHI 2025, DOI 10.1145/3706598.3713778 [2차: Microsoft Research 페이지]. 지식 노동자 **319명**, 실제 사례 **936개**. **GenAI에 대한 신뢰가 높을수록 비판적 사고가 적고**, 자기 능력에 대한 확신이 높을수록 비판적 사고가 많음. 비판적 사고의 성격이 정보 검증·응답 통합·과제 관리(stewardship)로 이동.
- **Explanations Can Reduce Overreliance on AI Systems During Decision-Making** — Helena Vasconcelos, Matthew Jörke, Madeleine Grunde-McLaughlin, Tobias Gerstenberg, Michael Bernstein, Ranjay Krishna, CSCW 2023, DOI 10.1145/3579605, arXiv 2212.06823. 5개 연구(N=731). 과의존은 불가피한 인지 편향이 아니라 **검증 비용 대비 이득의 전략적 선택** — 검증 비용을 낮추면 과의존이 줄어듦 [원문].
  - 책 활용: 이 결과가 책에 특히 중요하다. **"추적 ID·검증 기록 템플릿은 사람의 검증 비용을 낮춰 과의존을 줄이는 장치"**라는 논리를 세울 수 있다(가이드 12 VAL 템플릿).
- **The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers** — James Prather 외, ICER 2024, DOI 10.1145/3632620.3671116, arXiv 2405.17739. 21개 세션 관찰. 이미 할 일을 아는 학생은 가속, 고전하는 학생은 메타인지 어려움이 커지고 **"유능함의 착각(illusion of competence)"**으로 끝남 [원문].
- **Grounded Copilot: How Programmers Interact with Code-Generating Models** — Shraddha Barke, Michael B. James, Nadia Polikarpova, OOPSLA 2023 (PACMPL), DOI 10.1145/3586030, arXiv 2206.15000, 피인용 722. 참가자 20명. 상호작용은 이원적 — **가속 모드**(다음 할 일을 알고 빨리 가기)와 **탐색 모드**(모를 때 선택지 탐색) [원문].
  - 책 활용: 설계 문서가 있으면 "가속 모드"로 쓸 수 있고, 없으면 "탐색 모드"에서 AI가 결정을 대신 내린다. 가이드 07 "스파이크를 잘 쓰는 법"(탐색은 별도로, 결과를 기록)과 연결.
- **Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming** — Hussein Mozannar, Gagan Bansal, Adam Fourney, Eric Horvitz, CHI 2024, arXiv 2210.14306. Copilot 사용 행동 분류 CUPS, 21명. 제안 검증에 드는 시간 비용 가시화 [원문].
- **Investigating and Designing for Trust in AI-powered Code Generation Tools** — Ruotong Wang, Ruijia Cheng, Denae Ford, Thomas Zimmermann, FAccT 2024, DOI 10.1145/3630106.3658984, arXiv 2305.11248. 개발자 17명 인터뷰. 적절한 신뢰 형성의 3대 과제: **기대 설정, 도구 설정, 제안 검증** [원문].
- **Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task** — Nataliya Kosmyna 외(MIT Media Lab), 2025, arXiv 2506.08872 (프리프린트, 동료 심사 전). 에세이 쓰기, 54명(4회차 18명), EEG. LLM 그룹의 뇌 연결성이 가장 약하고 자기 글 인용에 어려움 [원문]. 코딩 연구가 아니므로 "인지 부채"라는 용어 소개 정도로만.
- 책 활용 (5장 전체): 이 책의 "사람이 최종 결정을 소유" 주장은 윤리가 아니라 **공학적 필요**라는 논리. 사람의 판단력이 마모되면 통제 계층 전체가 무너진다.

---

## 6. 다중 에이전트 소프트웨어 개발 — 역할 분리는 도움이 되는가

### 논문 53: ChatDev: Communicative Agents for Software Development
- 저자·연도: Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, Maosong Sun, 2023/2024
- 발표처: ACL 2024 · DOI 10.18653/v1/2024.acl-long.810 · arXiv 2307.07924 · 피인용 1,397
- 핵심 [원문]: 설계·코딩·테스트 단계별 전문 에이전트가 "채팅 체인"으로 대화. 자연어는 시스템 설계에, 프로그래밍 언어는 디버깅에 유리. (abstract에 정량 수치 없음)

### 논문 54: MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework
- 저자·연도: Sirui Hong, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber, 2023
- 발표처: ICLR 2024 (oral) [2차: ICLR 2024 가상 학회 페이지] · arXiv 2308.00352 · 피인용 2,707
- 핵심 [원문]: 표준 작업 절차(SOP)를 프롬프트 순서로 인코딩해 역할별 에이전트가 **중간 산출물(PRD, 설계, API 명세)을 검증**. 순진하게 LLM을 연결하면 "연쇄 환각(cascading hallucinations)"이 생긴다는 문제의식.
- 핵심 수치 [원문, HTML 본문]:
  - HumanEval Pass@1 85.9%, MBPP 87.7% (GPT-4), 실행 피드백이 각각 +4.2%, +5.4%
  - SoftwareDev 실행 가능성(1~4점): ChatDev 2.25 vs MetaGPT 3.75, 사람 수정 비용 2.5 vs 0.83
  - 역할 제거 실험(표 3): Engineer만 1.0 → +Product Manager 2.0 → +PM·Architect 2.5 → 4개 역할 모두 4.0. 단 +Product Manager·Project Manager 조합은 2.0으로, **단조 증가는 아님**
- 책 활용: 가이드 10 역할 분리의 가장 유명한 실증. 단, 효과의 원천이 "역할 수"가 아니라 **"구조화된 중간 문서(PRD·설계·인터페이스 명세)"**라는 해석이 책 주제와 더 맞는다. 이 해석은 저자의 SOP 설명에 근거한 책의 추론임을 밝힌다.

### 논문 55: Self-collaboration Code Generation via ChatGPT
- 저자·연도: Yihong Dong, Xue Jiang, Zhi Jin, Ge Li, 2023
- 발표처: ACM TOSEM · DOI 10.1145/3672459 · arXiv 2304.07590 · 피인용 579
- 핵심 수치 [원문]: 분석가·코더·테스터 3역할 가상 팀. 기본 LLM 에이전트 대비 Pass@1 **상대 29.9~47.1% 향상**.

### 논문 56: AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation
- 저자·연도: Dong Huang, Jie M. Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, Heming Cui, 2023
- 발표처: arXiv 프리프린트 (S2에서 발표처 미확인) · arXiv 2312.13010
- 핵심 수치 [원문]: 프로그래머·**테스트 설계자**·테스트 실행자 에이전트 분리. GPT-4 기준 HumanEval 96.3%, MBPP 91.8% pass@1, 토큰 56.9K·66.3K. 비교 최고 기법은 90.2%·78.9%, 토큰 138.2K·206.5K.
- 책 활용: "구현자와 테스트 작성자를 분리하라"는 실천 근거. 효과의 핵심은 역할 이름이 아니라 **외부 실행 피드백**(논문 34와 같은 결론).

### 논문 57: Why Do Multi-Agent LLM Systems Fail?
- 저자·연도: Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica, 2025
- 발표처: NeurIPS 2025 Datasets and Benchmarks Track [2차: NeurIPS 2025 페이지] · arXiv 2503.13657 · 피인용 802
- 핵심 [원문]: MAS 프레임워크 7종의 주석된 실행 기록 1,600개 이상(NeurIPS 판 abstract는 "1000+"로 표기, 버전 차이). 실패 모드 14종을 3범주로 분류: (i) 시스템 설계 문제, (ii) 에이전트 간 불일치, (iii) 과제 검증. 주석자 일치도 κ=0.88. 출발점은 "MAS의 벤치마크 이득은 흔히 미미하다"는 관찰.
- 실패 모드별 비율 [원문, HTML 본문]: 과제 명세 불이행 11.8%, 역할 명세 불이행 1.5%, 단계 반복 15.7%, 종료 조건 미인지 12.4%, **명확화 질문 실패 6.8%**, 과제 이탈 7.4%, 추론-행동 불일치 13.2%, 조기 종료 6.2%, **검증 없음·불완전 8.2%, 잘못된 검증 9.1%** 등.
- 개입 결과 [원문]: ChatDev에서 역할 명세 개선으로 +9.4% 성공률(동일 프롬프트·GPT-4o), 상위 수준 과제 목표 검증 단계 추가로 ProgramDev에서 **+15.6%**. 그래도 완료율은 "여전히 낮다".
- 인용할 만한 문장:
  > "Despite enthusiasm for Multi-Agent LLM Systems (MAS), their performance gains on popular benchmarks are often minimal." (abstract)
- 책 활용: 다중 에이전트 실패가 **명세 불이행·명확화 실패·검증 부재**에 몰려 있다 = 이 책이 다루는 문서·계약·검증 증거가 바로 그 공백을 채우는 장치. 가이드 10의 역할 카드에 "입력·출력·금지·중단 조건"을 적는 이유.

### 논문 58: Rethinking the Bounds of LLM Reasoning: Are Multi-Agent Discussions the Key?
- 저자·연도: Qineng Wang, Zihao Wang, Ying Su, Hanghang Tong, Yangqiu Song, 2024
- 발표처: ACL 2024 (S2 기준) · arXiv 2402.18272 · 피인용 241
- 핵심 [원문]: **강한 프롬프트를 가진 단일 에이전트가 최고의 다중 에이전트 토론 방식과 거의 같은 성능**. 다중 에이전트 토론이 나은 경우는 프롬프트에 예시(demonstration)가 없을 때뿐.

### 논문 59: Agentless + Single-agent or Multi-agent Systems? Why Not Both?
- **Agentless** (논문 13 참조) — SWE-bench Lite에서 단순한 3단계(위치 찾기·수리·패치 검증) 파이프라인이 당시 오픈소스 에이전트 중 최고 성능 **32.00%(96개 해결)**, 비용 $0.70 [원문]. arXiv 2407.01489, 피인용 561.
- **Single-agent or Multi-agent Systems? Why Not Both?** — Mingyan Gao 외, 2025, arXiv 2505.18286 (프리프린트). **LLM 능력이 오를수록 MAS의 이점이 줄어든다**. MAS·SAS 요청 캐스케이딩으로 정확도 +1.1~12%, 배포 비용 최대 −20% [원문].

### 논문 60: Towards a Science of Scaling Agent Systems
- 저자·연도: Yubin Kim, Ken Gu, Chanwoo Park 외 (Google Research 등), 2025
- 발표처: arXiv 프리프린트 · arXiv 2512.08296 · 피인용 165
- 핵심 수치 [원문]: 6개 벤치마크·5개 아키텍처(단일 1 + 다중 4)·3개 LLM 계열, 260개 구성. 도구·프롬프트·연산량을 표준화해 아키텍처 효과만 분리. 단일 에이전트 대비 상대 성능 변화가 **분해 가능한 금융 추론 +80.8%에서 순차 계획 −70.0%**까지. 단일 에이전트 성능이 일정 수준을 넘으면 조정의 이득이 줄고, **중앙 검증이 없는 구조는 오류를 더 전파**.
- 인용할 만한 문장:
  > "Agent effectiveness depends on alignment between coordination and task structure, and that mismatched coordination degrades the performance." (abstract)
- 책 활용 (6장 종합): 역할 분리는 **과제 구조와 맞을 때만** 이롭다. 책의 결론으로: "역할을 나누는 목적은 에이전트 수를 늘리는 것이 아니라, **결정 한계와 검증 지점을 나누는 것**이다." 가이드 10의 "중앙 검증 = 사람 승인 + 실행 증거"와 연결.

### 보조: LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision and the Road Ahead
- Junda He, Christoph Treude, David Lo, ACM TOSEM, DOI 10.1145/3712003, arXiv 2404.04834, 피인용 413. SDLC 단계별 LMA 적용 체계적 문헌 검토 + 사례 연구 2건 [원문]. 6장 도입부 서베이로 사용.

### 보조: 명세 주도 개발(SDD) 관련 2026 프리프린트 — 근거 강도 낮음, 동향 소개용
- **Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants** — Deepak Babu Piskala, 2026, arXiv 2602.00180 (AIware 2026 투고, 단독 저자, 실무 가이드 성격). 명세 엄밀성 3단계: **spec-first, spec-anchored, spec-as-source** [원문]. 가이드의 위치를 이 3단계로 설명하면 독자 이해에 도움(가이드는 대략 spec-anchored에 해당 — 책의 해석).
- **Spec Kit Agents: Context-Grounded Agentic Workflows** — Pardis Taghavi, Santosh Bhavani, 2026, arXiv 2604.05278. SDD 에이전트가 대형 저장소에서 "context blind"해 **API 환각·아키텍처 위반**을 낸다는 문제 제기. 단계별 저장소 근거 훅으로 LLM-judge 점수 +0.15/5(+3.0%), SWE-bench Lite 58.2% Pass@1 [원문]. 효과 크기가 작다는 점도 함께 전달.
- **Specification-Driven Development Benchmark: Security Knowledge Transition** — Oleg Grynets 외, 2026, arXiv 2606.00167. 명세 주도 생성에서 **기능은 명시되지만 보안은 암묵적**으로 남아 생성 시스템이 권한·소유권 규칙을 놓친다는 문제. 숨은 221개 블랙박스 API 테스트 기준 대표 실패 50(보안 요구 없음) → 42(ASVS) → 36(다층 보안 모델) [원문]. 가이드 05 "권한 계약"과 논문 15의 "보안 14.8%"를 잇는 연결 고리.
- **SWE-AGI** (arXiv 2602.09447), **A Lean and Spec-Driven AI-SDLC for Applied AI Education** (arXiv 2609.24348), **Practical Implementation Report on Introducing Spec-Driven Development Using AI Agents in Software Development PBL** (CSEE&T 2026, arXiv 2608.30572) — 교육·벤치마크 사례. 필요 시 참조.

---

## 7. 회색 문헌(비학술·업계 보고서) — 참고용, 수치는 2차 출처 확인

web-researcher 영역과 겹친다. 학술 논문이 아니므로 본문에서는 "업계 보고서에 따르면"으로 쓴다.

| 출처 | 확인한 수치 | 확인 경로 | 주의 |
|---|---|---|---|
| Google DORA 2024 Accelerate State of DevOps | AI 도입 증가에 따라 전달 처리량 −1.5%, 전달 안정성 −7.2% 추정. 설문 39,000명 이상 | Google Cloud 블로그 발표문, InfoQ [2차] | "도입 25% 증가당"이라는 표현은 2차 분석(RedMonk)의 재진술일 수 있음 |
| Google DORA 2025 State of AI-assisted Software Development | 응답자 약 5,000명, AI 사용 약 90%, AI 코드에 "거의/전혀 신뢰 없음" 약 30%. 처리량과는 양의 관계로 반전, 안정성 문제는 지속. 핵심 메시지 "AI는 증폭기" | Google 블로그·InfoQ·Splunk 요약 [2차] | 안정성 수치 미확인 |
| GitClear 2025 AI Copilot Code Quality | 변경 2억 1,100만 줄(2020~2024). 이동(moved) 코드 24.8%(2021) → 9.5%(2024), 복사·붙여넣기 8.4% → 12.3%, 5줄 이상 중복 블록 포함 커밋 2024년 약 8배 | DevClass·LeadDev 보도 [2차] | AI가 썼다는 줄 단위 증거가 아니라 시기별 추세 |
| Uplevel Data Labs 2024 | Copilot 접근 351명 vs 비접근 434명, PR 사이클 타임 개선 없음, PR 내 버그율 41% 증가 | CIO.com·DevOps.com 보도 [2차] | 실제 사용이 아니라 "접근"을 측정 |

---

## 8. 수집 한계와 미확인 목록

- **미확인 식별자·수치(본문 사용 전 재확인 필요)**
  - Jansen & Bosch 2005 DOI, "knowledge vaporization" 표현의 원문 존재 여부
  - Aghajani 2019 분류 체계 범주 수, DOI
  - Garcia de Santana Junior 외 ICSA 2026의 전체 저자·DOI
  - ClarifyGPT(2310.10996)의 FSE 2024 게재 여부, Ahmed 외(2408.05534)의 MSR 2025 게재 여부, AgentCoder 발표처
  - Mathews & Nagappan(TDD)의 구체 향상 폭(%p)
  - Perry 외(CCS 2023) 참가자 수
  - Cui 외(Management Science) 경력별 이질성 수치
  - SWE-Bench Pro Verified / V2의 상세 수치
  - Liang 외 SWE-Bench Illusion의 정확한 게재 트랙
- **본문 미열람**: 대부분은 abstract + (일부) arXiv HTML 본문 기준. 비arXiv 고전 논문(Gotel, Bainbridge, Tyree, Jansen, Parasuraman, Mäder, Aghajani, Buchgeher)은 전문을 읽지 않고 출판사·학회·기관 저장소 페이지와 2차 요약으로 확인했다.
- **피인용수**: Semantic Scholar 기준(2026-10-28). Google Scholar 수치와 다르다.
- **프리프린트 비중**: 2026년 컨텍스트 파일·SDD 연구 다수가 단독 저자·동료 심사 전이다. 논문 17·20·21은 결과가 강하고 책 논지와 직결되지만 재현 연구가 아직 없다.
- **결과 충돌 정리**: 컨텍스트 파일 효과(정확도 효과 없음 17·19 vs 효율 향상 18 vs 프로젝트별로 갈림 10), 생산성(METR 느려짐 vs Google·Microsoft 빨라짐), 다중 에이전트(MetaGPT·AgentCoder 향상 vs 단일 에이전트 동등 58·59·60). 책에서는 **"효과는 맥락에 따라 다르다 → 당신 저장소에서 측정하라"**로 일관되게 착지한다.
- **다루지 못한 것**: 한국어권 학술 연구(KCI 등)는 검색하지 않았다. 형식 명세(TLA+, Alloy)와 LLM 결합 연구, 계약 테스트(Pact 등)·API 스키마 주도 개발의 LLM 실증 연구는 찾지 못했거나 범위 밖으로 남겼다.
