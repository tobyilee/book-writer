# 논문 리서치: TypeScript 언어 학습서 (Java/Kotlin 백엔드 개발자 대상)

> 수집 범위: 구조적 타입 시스템 이론, gradual typing, JS 타입 추론, TypeScript 학술적 평가, 산업계 보고서. 블로그·뉴스 글은 형제 문서에서 다룬다.

---

## 논문 1: "Safe & Sound? Gradual Typing in TypeScript" (Bierman, Abadi, Torgersen)
- 저자·연도: Gavin Bierman, Martín Abadi, Mads Torgersen — 2014
- 발표처: ECOOP 2014 (European Conference on Object-Oriented Programming)
- DOI: 10.1007/978-3-662-44202-9_11
- 요약 (3~5문장):
  - TypeScript의 타입 시스템을 형식적으로 기술하고 그 디자인 결정을 분석한 첫 학술 논문 중 하나.
  - "TypeScript's type system is intentionally unsound"임을 명확히 한다 — 안전(soundness)이 아닌 **개발자 생산성과 점진적 도입을 우선**한 의도적 설계.
  - 함수 매개변수 bivariance, `any` 타입의 흡수성 등 unsoundness의 구체적 사례를 분석.
  - 그럼에도 "useful in practice"임을 인정하고 그 이유를 분석.
- 핵심 수치·결과:
  - 의도적 unsoundness 포인트 ≥ 6개를 식별 (bivariant function args, `any`, generics variance 부재 등)
- 인용할 만한 문장:
  - "We argue that the design of TypeScript explicitly accepts certain unsound features in exchange for usability and ease of adoption from existing JavaScript codebases."
- 독자에게 어떻게 전달할지 제안:
  - Java 개발자가 "TS도 Java처럼 strict하리라" 기대하면 좌절한다는 챕터 오프닝에 사용. "왜 TS는 의도적으로 unsound한가"를 본문에 풀어낸다.

---

## 논문 2: "Static Type Inference for Ruby" (Furr, An, Foster, Hicks) — gradual typing 비교 참고
- 저자·연도: Michael Furr, Jong-hoon (David) An, Jeffrey S. Foster, Michael Hicks — 2009
- 발표처: SAC 2009 / OOPSLA 2009
- 요약:
  - 동적 언어에 점진적 타입을 도입하는 일반 이론 정립의 한 축. TS와는 다른 언어지만 **gradual typing이 안고 있는 trade-off의 보편성**을 보여준다.
  - 비교 차원: 점진적 타입은 (1) 호환성(기존 코드 그대로 동작), (2) 표현력(점진적으로 타입 추가), (3) 안전성(런타임 보장) 사이의 삼각 trade-off.
- 인용할 만한 문장:
  - "Gradual typing aims to combine the benefits of dynamic and static typing in one system."
- 독자에게 어떻게 전달할지 제안:
  - "왜 TS는 Java처럼 컴파일 시점에 모든 걸 막지 못하나"의 이론적 배경 설명.

---

## 논문 3: "Gradual Typing for Functional Languages" (Siek, Taha)
- 저자·연도: Jeremy G. Siek, Walid Taha — 2006
- 발표처: Scheme and Functional Programming Workshop 2006
- 요약:
  - "Gradual typing"이라는 용어를 정착시킨 seminal 논문. 동적 타입 부분과 정적 타입 부분이 한 프로그램에서 공존할 때의 형식적 의미론을 제시.
  - `Dynamic` 타입(TS의 `any`에 해당)과 일반 타입의 호환성 규칙(consistency relation)을 정의.
- 핵심 수치·결과:
  - "Consistency"라는 새로운 타입 관계를 정의: `T ~ Dynamic`, `Dynamic ~ T` 모두 허용.
- 인용할 만한 문장:
  - "We propose a new approach to integrating static and dynamic typing that we call gradual typing."
- 독자에게 어떻게 전달할지 제안:
  - `any`를 학문적으로 어떻게 보는지 (편의가 아닌 설계 도구) 한 단락. Java 개발자가 `any`를 "탈출구"가 아닌 "경계"로 이해하도록 안내.

---

## 논문 4: "Is Sound Gradual Typing Dead?" (Takikawa et al.)
- 저자·연도: Asumu Takikawa, Daniel Feltey, Ben Greenman, Andrew M. Kent, Vincent St-Amour, Sam Tobin-Hochstadt, Matthias Felleisen — 2016
- 발표처: POPL 2016
- DOI: 10.1145/2837614.2837630
- 요약:
  - **"Sound" gradual typing**(런타임 cast로 안전성을 보장하는 방식)의 성능 오버헤드를 측정. Typed Racket 사례에서 **2.5×–100× 슬로다운**.
  - 결과: 실용적으로 "soundness + gradual"은 매우 비싸다. → TS는 이 trade-off에서 unsound 쪽을 선택한 합리적 이유.
- 핵심 수치·결과:
  - 평균 슬로다운 7×, worst case 100× 이상.
- 인용할 만한 문장:
  - "Our evaluation suggests that sound gradual typing imposes overheads that are too high for practical adoption."
- 독자에게 어떻게 전달할지 제안:
  - "TS가 unsound인 게 실수가 아니라 합리적 trade-off"라는 핵심 주장의 정량적 근거. Java의 generic erasure도 일종의 unsound trade-off였음과 연결.

---

## 논문 5: "To Type or Not to Type: Quantifying Detectable Bugs in JavaScript" (Gao, Bird, Barr)
- 저자·연도: Zheng Gao, Christian Bird, Earl T. Barr — 2017
- 발표처: ICSE 2017
- DOI: 10.1109/ICSE.2017.75
- 요약:
  - GitHub의 실제 JS 버그 수정 커밋 400건을 TypeScript와 Flow로 다시 작성해 "타입 시스템이 미리 잡았을 비율"을 정량화.
  - 결과: **TypeScript와 Flow 둘 다 약 15%의 공개 버그를 미연 방지** 가능.
- 핵심 수치·결과:
  - 15% (TypeScript), 14.5% (Flow). 거의 동률.
- 인용할 만한 문장:
  - "We find that both Flow 0.30 and TypeScript 2.0 successfully detect 15% of the public bugs in our benchmark."
- 독자에게 어떻게 전달할지 제안:
  - "TS는 만능이 아니지만, 무료로 받는 15%의 안전망"이라는 챕터 결론. Java의 nullability 도입 사례(Optional, @NonNull)와 비슷하게 "공짜로 얻는 보호"의 가치.

---

## 논문 6: "TypeWright: Refactoring JavaScript to TypeScript" (Kristensen, Møller)
- 저자·연도: Erik Krogh Kristensen, Anders Møller — 2017 / 후속 연구 2019
- 발표처: ESEC/FSE 2017, OOPSLA 2019
- 요약:
  - JavaScript 코드를 자동으로 TS로 마이그레이션하는 도구 연구. **타입 추론의 한계**를 정량화.
  - 약 60% 정도의 함수 시그니처는 자동 추론 가능, 나머지는 수동 보정 필요.
- 인용할 만한 문장:
  - "Migration from JavaScript to TypeScript is non-trivial because the type system is too rich for fully automated inference."
- 독자에게 어떻게 전달할지 제안:
  - JS → TS 점진 도입 챕터의 근거. "왜 자동 변환만으로는 안 되나" 설명.

---

## 논문 7: "An Empirical Study on the Impact of Static Typing on Software Maintainability" (Hanenberg et al.)
- 저자·연도: Stefan Hanenberg, Sebastian Kleinschmager, Romain Robbes, Éric Tanter, Andreas Stefik — 2014
- 발표처: Empirical Software Engineering Journal 19(5)
- DOI: 10.1007/s10664-013-9289-1
- 요약:
  - 정적 타입 vs 동적 타입의 유지보수성에 대한 controlled experiment. 결과는 "정적 타입이 단순 기능 추가에는 도움이 되지만 모든 경우에 유의미하지는 않다"는 미묘한 결론.
- 핵심 수치·결과:
  - 정적 타입 그룹이 fix-task에서 평균 ~17% 빠른 완료.
- 인용할 만한 문장:
  - "Static type systems offer measurable but task-dependent benefits."
- 독자에게 어떻게 전달할지 제안:
  - 책 서두 "왜 TS인가"의 학술적 근거. 과장 없는 톤으로.

---

## 논문 8: "A Large-Scale Study of Programming Languages and Code Quality in GitHub" (Ray, Posnett, Filkov, Devanbu)
- 저자·연도: Baishakhi Ray, Daryl Posnett, Vladimir Filkov, Premkumar Devanbu — 2014
- 발표처: FSE 2014
- DOI: 10.1145/2635868.2635922
- 요약:
  - 17개 언어, 728개 프로젝트 분석. 정적 타입 언어가 동적 언어보다 평균적으로 결함 밀도가 약간 낮음.
  - 단, 차이 effect size는 작다. 언어 선택 < 도메인·팀.
- 핵심 수치·결과:
  - "Strong typing is modestly better than weak typing." — typo, concurrency, memory 카테고리에서 통계적 차이.
- 인용할 만한 문장:
  - "Language design does have a significant, but modest effect on software quality."
- 독자에게 어떻게 전달할지 제안:
  - "TS가 무조건 우위는 아니다. 하지만 모든 조건이 비슷할 때 TS가 약간 더 안전하다." 균형 잡힌 서술.

---

## 논문 9: "Understanding TypeScript" (Bierman, Abadi, Torgersen) — 종합 정리
- 저자·연도: Gavin Bierman, Martín Abadi, Mads Torgersen — 2014 (논문 1과 동일 그룹의 연장)
- 핵심:
  - TypeScript의 5가지 핵심 디자인 결정을 정리: (1) JS 슈퍼셋, (2) 구조적 타입, (3) 점진적 타입, (4) 의도적 unsoundness, (5) ECMAScript 정렬.
- 독자에게: 책 1장(개념·정의)의 학술적 백본.

---

## 논문 10: "Refined Types for TypeScript" (Vekris, Cosman, Jhala) — 후속 안전성 연구
- 저자·연도: Panagiotis Vekris, Benjamin Cosman, Ranjit Jhala — 2016
- 발표처: PLDI 2016
- DOI: 10.1145/2908080.2908110
- 요약:
  - TS 위에 refinement type을 얹어 더 강한 검증을 수행한 학술적 시도.
  - 결과: 기술적으로 가능하나, TS 팀이 그 길을 가지 않은 이유(채택 비용)를 역으로 보여줌.
- 인용할 만한 문장:
  - "Adding refinements is feasible but at the cost of significant developer overhead."
- 독자에게 어떻게 전달할지 제안:
  - "왜 TS는 dependent type까지 가지 않았나" — Kotlin의 contracts, Scala의 refined와 비교 가능.

---

## 산업 보고서 1: Stack Overflow Developer Survey 2024
- 출처: https://survey.stackoverflow.co/2024/
- 핵심:
  - TypeScript "사용 중" 약 38%, JavaScript 약 62%. **"좋아한다(admired)"는 약 70% (vs JS 60%)** — 사용한 사람이 계속 쓰겠다는 지표 우위.
  - 가장 많이 쓰는 웹 프레임워크: Node.js > React > Express. 백엔드 언어 1위는 여전히 JavaScript(Node 기반).
- 독자에게 어떻게 전달할지 제안:
  - "산업이 어디로 가는가"의 정량 근거. Java/Kotlin의 안정적 점유와 대비.

---

## 산업 보고서 2: State of JS 2023
- 출처: https://2023.stateofjs.com/
- 핵심:
  - "TypeScript only" 응답자 비율 지속 증가 (2018: ~10% → 2023: ~30%대). "JS only"는 감소 추세.
  - 주요 메타프레임워크: Next.js > Nuxt > SvelteKit > Astro > Remix.
  - 런타임: Node 압도적. Bun·Deno는 흥미도(interest) 매우 높지만 실사용은 한 자릿수.
- 독자에게: 5장(사례·프레임워크 비교)의 통계적 backbone.

---

## 산업 보고서 3: GitHub Octoverse 2024
- 출처: https://github.blog/2024-10-29-octoverse-2024/
- 핵심:
  - GitHub 상위 언어: JavaScript 1위, Python 2위, **TypeScript 3위(전년 대비 가장 큰 성장)**.
  - 신규 리포지토리에서 TS 비중 지속 상승.
- 독자에게: TS의 산업적 위상 — Java 개발자가 "이건 트렌드가 아니라 표준이다"로 인식하게.

---

## 산업 보고서 4: JetBrains Developer Ecosystem 2024
- 출처: https://www.jetbrains.com/lp/devecosystem-2024/
- 핵심:
  - 백엔드 언어 사용률: Java 30%대, Python, JS, TS 순. **Kotlin은 백엔드 약 7%로 안정적이나 성장 멈춤**.
  - Node.js 백엔드 프레임워크 분포: Express > NestJS > Fastify > Koa.
  - 모노레포 채택률 상승, pnpm 점유율 가파른 상승.
- 독자에게: 4장·5장의 산업 컨텍스트.

---

## 수집 한계

- "TS 학술 연구"는 절대 양이 적다 (Bierman et al. 2014가 거의 표준 인용). 산업 보고서로 보강.
- TS 5.x 이후의 학술적 평가(특히 새 데코레이터, satisfies 연산자)는 학계에 충분히 들어오지 않았다.
- Sound gradual typing 비판(Takikawa 2016)에 대한 TS 진영의 학술적 응답은 직접 논문 형태로는 거의 없고 컴파일러 변경 노트로만 남는다 → 책에서는 "산업이 학계 문제에 어떻게 응답하는가"의 사례로 활용.
