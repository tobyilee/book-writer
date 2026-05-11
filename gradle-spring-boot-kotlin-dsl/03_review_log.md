# 1차 리뷰 (Phase 3)

## 종합 평가

전반적으로 **잘 짜인 계획서**다. 18장 5부 구조가 "사고 모델 → 단일 모듈 → 멀티 모듈 → 빌드를 도구로 → 운영"으로 흘러가는 서사 축이 또렷하고, `shop` 가상 앱이 각 챕터마다 한 단계씩 자라는 트래킹이 잘 박혀 있다. 레퍼런스 §1~§16의 거의 모든 영역이 챕터에 매핑되며, "Maven 출신 보호"와 "함정 우선" 원칙이 박스 시스템으로 본문에 녹아 들어 있는 점이 강점이다. 9.5 신문법(Configuration Cache, lazy Property, precompiled Settings accessor 등)을 별도 마이그레이션 챕터로 격리하지 않고 1~14장 본문 표준으로 다루기로 명시한 점도 정확한 선택이다.

다만 **세 군데에서 구조적 약점**이 있다. (1) 9장(bootJar 함정)이 책의 클라이맥스 중 하나로 박혀 있지만, 8장(모듈 쪼개기)과 사이에 한 호흡 더 두지 않고 바로 점프해서 독자가 "왜 갑자기 사고가 일어나지?"의 자연스러운 발생 맥락을 충분히 못 느낄 수 있다. (2) Part IV의 13장(Configuration Cache)이 12장(커스텀 plugin)을 받아 진행되는데, 12장의 분량(9,500자) + 13장(9,500자)이 연달아 가장 무거운 두 챕터로 배치되어 독자 피로 위험이 있다. (3) 17장 마이그레이션이 책 거의 끝(15·16장 직후)에 와 있어, 회사 빌드를 9.x로 올려야 하는 절박한 독자에겐 너무 늦게 만나게 된다.

또한 **레퍼런스 §15의 실무 페인포인트 9개 중 일부**(특히 §15.10 "IDE sync가 오래 걸리는 문제", §15.6 "Native 빌드 시간이 너무 길다"의 운영 처방, §15.1 "implementation vs api" 구분 논리)가 챕터 본문에 어디로 흡수되는지 명시되지 않았다. 커버리지 매핑 표(§8)에 §15 실무 페인포인트가 빠져 있다.

---

## 영역별 피드백

### 1. 커버리지

- **[Should] §15 실무 페인포인트 매핑 누락.** 계획서 §8 커버리지 체크리스트가 레퍼런스 §1~§14만 매핑하고 §15(실무 페인포인트 10개)는 매핑하지 않았다. §15.1(implementation vs api)는 5장에 들어가야 하고, §15.6(Native 빌드 시간 완화) §15.10(IDE sync)은 어느 챕터에 배치되는지 본문 명시가 필요하다.
  - **수정 제안:** 5장 주요 내용에 "§15.1 implementation/api 구분 논리와 java-library 플러그인 조건" 명시. 15장 함정 박스에 "§15.6 Native 빌드 시간 완화 (CI 별도 job, buildpack layer cache 영속화)" 추가. 13장 끝부분에 "§15.10 IDE sync는 Configuration Cache로 가속되지 않음 — Isolated Projects 영역" 함정 박스로 흡수.

- **[Should] Dependency Insight / Profile / `--scan` CLI 도구가 빠져 있다.** 레퍼런스에는 명시 안 됐지만, 실무 독자가 빌드 디버깅 시 가장 먼저 닿는 도구다. `./gradlew dependencyInsight --dependency slf4j`, `./gradlew :app:dependencies --configuration runtimeClasspath`, `./gradlew build --profile`, `./gradlew build --scan`.
  - **수정 제안:** 5장(Version Catalog와 BOM) 끝에 "의존성 그래프 디버깅 — `dependencyInsight` 한 박스"로 흡수. 또는 14장(CI)에 `--scan` 부분에 묶어서. 단, 별도 챕터로 빼지는 말 것 — 분량 폭주.

- **[Nice-to-have] Resolution strategy 본문 매핑이 없다.** 레퍼런스 §4.4의 `configurations.all { resolutionStrategy.eachDependency { ... } }` 패턴은 현장에서 슬쩍 자주 등장한다(특정 transitive 강제 다운그레이드 등).
  - **수정 제안:** 5장 끝부분 "함정 박스: BOM으로 못 잡는 transitive는 resolutionStrategy로 마지막 처방"으로 한 페이지.

- **[Critical] Spring Boot 4.0 신규 동작 변경점 (3.x → 4.x) 매핑 모호.** 레퍼런스 §17.7에 "Spring Boot Gradle Plugin 4.0의 신규 동작 변경점 — Migration 가이드 풀텍스트 별도 검증 필요"라고 명시됐는데, 계획서에는 6장 "마이그레이션 노트: Spring Boot 4.0의 동작 변경점" 한 줄만 있다. Spring Boot 3.5 → 4.0 마이그레이션을 책에서 어디까지 다루는지 독자에게 약속이 모호하다.
  - **수정 제안:** 6장 핵심 질문에 "Spring Boot 3.x 빌드를 그대로 4.0으로 올릴 때 무엇이 바뀌는가" 한 줄 추가. 또는 17장에 "Spring Boot 3.x → 4.x 마이그레이션 보조" 섹션 명시. 책 표지에 "Spring Boot 4.0" 명시한 이상 명확한 답이 필요.

### 2. 내러티브 아크

- **[Critical] 8장 → 9장 점프가 너무 빠르다.** 8장이 "단일 모듈 → 4모듈 분리"인데, 8장에서 모듈을 쪼개자마자 9장에서 곧바로 `bootJar` 함정으로 점프한다. 독자 입장에서는 "8장에서 다 잘 됐는데 왜 9장에서 갑자기 사고?"가 어색하다.
  - **수정 제안:** 8장 끝에 "이제 빌드해보면 `app`이 `domain`을 못 가져온다 — 다음 장의 미스터리"로 cliffhanger를 만들고, 9장 도입을 "8장의 마지막 명령이 왜 실패했는지부터"로 잇는다. 또는 8장의 `이 챕터에서 자라는 앱 상태`에 "정상 빌드가 아직 안 된다 — 9장의 함정에 걸려 있다"는 한 줄을 명시.

- **[Should] 10장 Convention Plugin 도입 시점은 자연스러운데, 그 직전 8장에서 `subprojects {}` 안티패턴을 "다음 장에서 처방"으로 미루는 게 두 장에 걸쳐 끌린다.** 8장 → 9장 → 10장이 모두 "안티패턴 경고 + 다음 장에서"로 이어지는 모양새. 독자는 두 챕터 분량 동안 "그래서 어떻게 해?"를 기다린다.
  - **수정 제안:** 8장은 `subprojects {}` 경고를 박스 한 줄로 그치고, 9장 끝에 "이제 빌드는 되지만 4개 파일이 거의 똑같다 — 10장에서 정리한다"로 잇기. 두 장 연속 cliffhanger보다 한 번에 한 미스터리.

- **[Should] 17장 마이그레이션이 너무 늦게 등장.** 회사 빌드를 9.x로 올려야 하는 절박한 독자(레퍼런스 §17 한계에 명시된 핵심 페르소나)는 책의 17장까지 기다리기 힘들다. 17장은 "이 책을 끝낸 후 회사 빌드를 옮기는 가이드"로 의도된 것으로 보이지만, 8.x 빌드를 갖고 책을 시작하는 독자에게 1장 직후 짧은 마이그레이션 체크리스트가 있으면 좋다.
  - **수정 제안:** 1장 끝에 "이 책은 9.5 기준이다. 8.x를 쓰는 독자는 17장의 마이그레이션 체크리스트를 먼저 훑고 와도 좋다"는 한 줄 + 17장 마이그레이션 step-by-step의 핵심 5개 처방을 1장 끝의 박스로 미리보기. 또는 17장 자체를 Part I의 보너스 챕터(0장처럼)로 옮기는 것도 검토 가능 — 다만 본문 흐름상 17장의 현 위치가 자연스러우니, 1장에 미리보기 박스만 추가가 더 합리적.

### 3. 챕터 간 균형

- **[Critical] Part IV 두 챕터가 연달아 가장 무겁다.** 12장(9,500자) + 13장(9,500자)이 연속. 그 직전 11장(8,000자), 직후 14장(8,000자)까지 4장 연속 8,000자+ 분량으로 Part III·IV가 책의 가장 무거운 호흡이 된다. 독자 피로 누적.
  - **수정 제안:** 12장에서 "Plugin + Extension 발행하기" 부분을 짧게 줄이고(외부 Plugin Portal 발행은 Out of Scope에 명시됐으니), Provider/Property API 본질과 `shop.build-info` 한 가지 예에 집중해 8,000자로 축소. 또는 13장에서 Toolchain 부분(레퍼런스 §11.4)을 6장이나 4장으로 옮겨(toolchain은 사실 단일 모듈 단계에서 결정되어야 하는 내용) 분량 분산.

- **[Should] 9장(9,000자)이 "책의 클라이맥스 중 하나"로 의도되어 길게 다루는 건 맞지만, 핵심 내용(함정 재현·해결법 1·해결법 2·실전 비교)이 7개 bullet에 그친다.** 9,000자에 비해 콘텐츠 밀도가 약해 보인다. 이 챕터에 한국어 실제 사고 사례(§6 작성자 메모에 명시) 한두 개와 `./gradlew :app:dependencies` 실제 출력 비교를 넣지 않으면 분량을 못 채우거나 같은 말을 반복하게 될 위험.
  - **수정 제안:** 9장에 "실제 사고 회고" 박스 1개(우아한형제들/카카오 기술블로그 인용) + "독자가 자기 빌드에서 함정을 진단하는 5분 체크리스트" 박스 1개를 추가하거나, 분량을 8,000자로 줄이는 것도 검토.

- **[Nice-to-have] 18장 5,500자는 적당하지만, "독자 회고 + 다음 길 안내"라는 두 역할이 한 챕터에 들어가 양쪽 다 깊이가 얕아질 위험.** Isolated Projects, Develocity, AGP/KMP 안내가 각각 한 박스인데 독자가 흘려 읽고 끝낼 가능성.
  - **수정 제안:** 그대로 두되, 18장의 "다음 길" 부분을 "독자가 자기 회사에서 다음으로 도입할 만한 5가지 선택지 + 각각의 진입 비용 추정"으로 구체화. 5,500자 안에서 "안내"가 아닌 "선택 가이드"로.

### 4. 난이도 곡선

- **[Should] 3장에 lazy Property/Provider, type-safe accessor, eager get vs `tasks.named` 등이 한꺼번에 등장.** 3장은 Part I (입문~중급)인데 lazy Provider/Property는 Part IV의 12장이 본격 다루는 주제다. 3장 독자(아직 멀티 모듈도 안 봤음)에게 "Provider API"라는 단어가 너무 일찍 나온다.
  - **수정 제안:** 3장은 "Kotlin DSL 문법 + Groovy 차이 + type-safe accessor + 큰따옴표"까지만 다루고, "lazy property는 `=` 권장, eager get 피하라"는 박스로 가볍게 언급만. 본격적 Property/Provider API는 12장에서 깊이. 3장 핵심 질문에서 "lazy property"는 빼고 "왜 Kotlin DSL이 Groovy DSL과 미묘하게 다른가"로 좁히기.

- **[Nice-to-have] 5장(BOM·Catalog)이 8,500자로 Part II에서 가장 무겁다.** 5장 자체가 deep dive인 건 동의하지만, Part II 초반(독자가 아직 Maven 사고에서 옮겨오는 중)에서 한 챕터에 declarable configurations 5개 + BOM 두 가지 길 + Catalog + 그 셋의 직교성까지 넣으면 정보량이 많다.
  - **수정 제안:** 5장은 "Catalog와 BOM의 직교성"이라는 핵심 메시지를 굵게 박고, declarable configurations의 디테일(implementation vs api, java-library 조건)은 박스로 격리. 본문 흐름은 "BOM → Catalog → 둘을 같이 쓴다"로 단순화.

- **[Should] 11장(Composite Build) 도입이 자연스럽지만, "외부 라이브러리 co-development" 시나리오는 Spring Boot 백엔드 독자의 실무 빈도가 낮을 수 있다.** 멀티 모듈 + Convention Plugin까지는 백엔드 표준이지만, Composite Build로 외부 lib을 끌어쓰는 건 라이브러리 개발자나 모노레포 운영자의 케이스. 핵심 페르소나가 이걸 당장 쓸 가능성이 낮다.
  - **수정 제안:** 11장의 build-logic included build 부분은 그대로 두되, Composite Build의 "외부 라이브러리 co-development" 시나리오는 분량을 줄이고 "언제 이게 필요한가" 가이드 한 박스로 좁히기. 책의 가상 앱 `shop`이 굳이 외부 lib과 co-development할 필요는 없을 듯.

### 5. 9.5 안정성 상태 반영

- **[정확하게 잘 반영됨]** Configuration Cache는 11장(아님)···13장 본문에 표준으로, Daemon JDK 17+/KGP 2.0+는 1장에, settings 수준 plugin은 8장·17장에, precompiled Settings plugin accessor는 3장·17장에, Wrapper retries는 14장·17장에 분산되어 있다. 17장 마이그레이션이 "9.x 신문법을 가져오는 곳"이 아니라 "옛 빌드를 9.x로 옮길 때 무엇이 깨지는가"로 명확하게 의도되어 있어 정합성 좋음.

- **[Should] 단, Isolated Projects의 위치가 모호.** 13장에 "Configuration Cache는 IDE sync는 가속하지 않는다 (그건 Isolated Projects 영역)"로 한 번 언급, 18장에 "다음 길"로 한 번 더. 9.x incubating 단계라 본문 표준으로 다룰 순 없지만, 13장의 cliffhanger와 18장의 정리 사이 연결을 명시적으로 박아둘 가치가 있다.
  - **수정 제안:** 13장 함정 박스에 "Isolated Projects는 9.x incubating — 18장에서 다시 본다"는 한 줄 추가. 18장 Isolated Projects 부분에 "13장에서 만난 IDE sync 문제의 답이 될 영역"으로 회수.

### 6. 함정 우선 원칙

- **[잘 반영됨]** 함정 박스가 1·3·4·5·7·8·9·10·13·15·16장에 명시되어 있고, "함정 모음 챕터"로 격리되지 않고 본문 차원에서 다뤄진다. bootJar 함정은 챕터 하나(9장)로 격상, BOM vs Catalog 선택은 5장 본문에, Configuration Cache 호환은 13장 본문에. 원칙 충실.

- **[Should] 누락된 함정 후보 3가지.**
  1. **`outputs.upToDateWhen { false }` 함정** — 커스텀 task 작성 시 흔히 빠지는 안티패턴(매번 실행되게 만들어 Build Cache 무효). 레퍼런스 §10.1의 "최소 하나의 출력이 없으면 task는 항상 실행"과 연결.
     - **수정 제안:** 12장 함정 박스에 한 줄 추가.
  2. **`./gradlew build --refresh-dependencies`의 잘못된 사용** — 부분 갱신이라고 오해해서 매번 사용하는 사례가 흔하다. lockfile/verification metadata와 충돌.
     - **수정 제안:** 16장 함정 박스에 한 줄.
  3. **`io.spring.dependency-management`와 `platform()`을 동시에 적용했을 때의 충돌** — 두 메커니즘이 같은 BOM을 두 번 적용해서 우선순위가 모호해지는 사례.
     - **수정 제안:** 5장 함정 박스에 "이 두 가지를 동시에 적용하지 마라" 한 줄.

### 7. Maven 출신 보호

- **[잘 반영됨]** 4장 전체가 1:1 매핑 다리, 2장·5장에 Maven 비교 박스, 10장의 마지막 비교 박스("parent pom vs Convention Plugin")까지 자연스러운 페이드아웃. 핵심 페르소나(Maven 출신) 보호 충실.

- **[Should] 1장에 Maven 출신 독자가 책 도입에서 만나는 첫 박스가 없다.** 1장은 "왜 다시 짜야 하는가"의 동기 부여 챕터인데, Maven 출신 독자가 "내가 왜 이걸 읽어야 하지?"의 답을 가장 빠르게 받아야 할 곳이다.
  - **수정 제안:** 1장 도입부에 "Maven에서 옮겨온 분께" 한 페이지(또는 박스) 추가. "당신이 알던 phase는 task graph로, dependencyManagement는 platform/BOM으로, parent pom은 Convention Plugin으로 — 정확한 매핑은 4장에서. 일단 이 책을 끝내면 Maven으로 안 돌아간다는 약속"의 톤. 4장은 핵심 페르소나의 첫 번째 도착지이므로, 1장에서 4장으로 빠르게 연결할 미끼가 필요.

### 8. Kotlin DSL 정합성

- **[잘 반영됨]** 모든 챕터가 Kotlin DSL 기본, Groovy DSL은 차이가 있을 때만 박스. 12장 커스텀 plugin은 Kotlin으로 구현. 일관성 좋음.

- **[Should] 8장·10장의 convention plugin에서 string-receiver(`"implementation"(platform(...))`)가 등장하는데, 이게 왜 string인지(precompiled plugin은 java plugin이 아직 적용 안 된 시점이라 type-safe accessor가 없음)를 본문에서 짚어줘야 한다.** Kotlin DSL의 타입 안전성을 강조해온 책에서 갑자기 string-receiver가 등장하면 독자가 혼란.
  - **수정 제안:** 10장 본문에 "왜 여기서 string?" 박스 한 페이지 — type-safe accessor의 작동 원리(plugin 적용 순서에 따라 노출) 정리.

### 9. 챕터 핵심 질문의 날카로움

- **[Should] 1장 핵심 질문이 두루뭉술.** "왜 이제 끝내야 하는가"는 동기 부여형 질문이라 답이 모호하다.
  - **수정 제안:** "이 책을 다 읽고 나면 build.gradle.kts를 어디까지 만질 수 있게 되는가?" 같은 출구 상태를 묻는 질문, 또는 "Spring Boot 개발자가 알아야 할 Gradle은 의존성 추가 그 이상으로 무엇이 있는가?"의 구체형으로 좁히기.

- **[Should] 18장 핵심 질문도 모호.** "이 책 이후에 더 멀리 가려면"은 안내문이지 질문이 아니다.
  - **수정 제안:** "이 책에서 다루지 않은 영역 중 당신 회사 빌드에 가장 먼저 적용할 만한 것은 무엇인가?" 같은 의사결정형으로.

- **[Nice-to-have] 5장 핵심 질문은 "각각 어떤 역할인가"인데, 답이 "Catalog는 declaration, BOM은 resolution, 둘 다 쓴다"로 명확하다.** 좋다.

- **[Nice-to-have] 9장 핵심 질문은 "왜 일어나는가"인데, 좀 더 액션 지향적으로 "library 모듈에서 빈 jar가 나오는 사고를 어떻게 진단하고 어떻게 막는가?"로 바꿔도 됨.

- **[잘 됨]** 4장·7장·8장·11장·12장·13장의 핵심 질문은 한 문장으로 좁혀져 있고 답이 명확하다.

### 10. 분량 vs 스코프

- **[Should] 18장에 모든 걸 다 담는다는 야망이 약점이 될 수 있다.** 5,500자에 "회고 + Isolated Projects + Develocity + AGP/KMP + Tooling API + 커뮤니티 + 1장 약속 회수" 7가지를 담으면 각 1페이지씩이라 깊이가 얕다.
  - **수정 제안:** "회고 + 1장 약속 회수" + "다음으로 도입할 만한 3가지(Isolated Projects, Develocity, Native 운영 심화)"로 좁히기. AGP/KMP는 Out of Scope에서 이미 언급했으니 18장에서 한 줄 회수만.

- **[Nice-to-have] 7장(테스트 분리) + 16장(보안) 둘 다 7,500자인데, 16장의 verification·locking·content filtering 세 영역이 7,500자에 들어가면 각 2,500자. 9장(bootJar 함정 단일 주제 9,000자)과의 분량 균형이 어색.** 16장이 너무 압축적일 수 있다.
  - **수정 제안:** 16장 분량을 8,500자로 조정하거나, content filtering을 5장(repositories 설정 부근)으로 일부 옮겨 16장은 verification + locking에 집중.

### 11. 빠진 챕터/박스 후보

- **[Should]** `./gradlew dependencyInsight` / `./gradlew :app:dependencies` 디버깅 도구 — 1번 영역 피드백 참조.

- **[Should]** `./gradlew --scan`을 처음 만나는 곳 — 14장에 묶여 있지만, 5장(의존성 갈등 디버깅)이나 13장(Configuration Cache 위반 진단)에서도 미리 한 번 언급할 만하다.

- **[Should]** Project property vs system property vs ext 변수 차이 — 12장에 `providers.systemProperty` 등이 등장하니, 그 직전 또는 그 안에서 "이 셋의 차이"를 박스로 정리.

- **[Should]** `wrapper` task의 `--distribution-type=bin` 처방이 14장에 묶여 있지만, 1장이나 4장(첫 빌드 시점)에서 더 일찍 만나야 함. `./gradlew` 처음 쓰는 독자가 200MB+ all distribution을 받는 함정에 일찍 빠진다.
  - **수정 제안:** 1장 또는 4장에 wrapper distribution-type 박스 한 줄.

- **[Nice-to-have]** `gradle.properties`의 표준 키들(`org.gradle.caching`, `org.gradle.parallel`, `org.gradle.configuration-cache`, `org.gradle.jvmargs`)을 한 곳에 정리한 부록 또는 13장 끝의 정리 표.

### 12. 책 제목

- **[Should] 1번 추천이 합리적이지만, 부제가 너무 길어 한 줄로 읽히지 않는다.** "Gradle 9.5와 Kotlin DSL로 키우는 Spring Boot 빌드" — 18자 + 12자 + 키워드. 매대용·검색용으로는 좋으나 EPUB 표지에선 두 줄로 갈라질 가능성. "키우는"이라는 동사가 3번 부제 "자라나는 빌드"의 핵심 메시지(앱이 자란다)와 약하게 충돌하는 것도 미세한 약점.
  - **수정 제안:**
    - 옵션 A: **부제 단축** — "Spring Boot × Gradle 9.5 × Kotlin DSL 실전 가이드". 키워드 3개를 ×로 묶어 검색·매대 최적. "키우는"은 책 표지에서 빼고 1장 본문에서 회수.
    - 옵션 B: **1번과 3번 혼합** — "빌드를 다시 짠다 — Spring Boot × Gradle 9.5 × Kotlin DSL로 자라나는 빌드". 길지만 메시지와 키워드 모두 살림.
    - 옵션 C: **그대로 유지** — 매대 시인성보다 메시지 우선이면 1번 그대로.

- **[Nice-to-have] 2번 후보 "build.gradle.kts를 진지하게"는 톤이 솔직해서 매력적이지만, "진지하게"가 약간 자기 비하 톤(독자가 그동안 안 진지했다는 함의)이라 핵심 페르소나(Maven 출신)에게는 약간 불편할 수 있다.** 추천 1번이 더 안전.

### 13. logline

- **[Should] 현재 logline은 정보가 많고 정확하지만 한 호흡에 읽히지 않는다.** "Spring Boot 백엔드 개발자가 build.gradle.kts 몇 줄짜리 빌드에서 멀티 모듈, 커스텀 플러그인, Configuration Cache, Native 이미지까지 자기 빌드를 도구로 키워가는 여정을 Kotlin DSL · Gradle 9.5 기준으로 풀어낸 실전 가이드." — 한 문장에 키워드 7개. 카탈로그식.
  - **수정 제안:**
    - 단축 A: **"build.gradle.kts에 의존성 몇 줄만 추가하던 Spring Boot 개발자가 멀티 모듈·커스텀 플러그인·Native까지 자기 빌드를 도구로 키우는 여정. Gradle 9.5 · Kotlin DSL 기준."** — 두 문장으로 끊어 호흡 회복. Configuration Cache는 본문에서 만나도록 logline에서 빼고 "도구로 키우는"으로 압축.
    - 단축 B: **"빌드 스크립트의 소비자에서 생산자로. Spring Boot 백엔드 개발자가 Gradle 9.5와 Kotlin DSL로 자기 빌드를 다시 짜는 18단계."** — "소비자 → 생산자"는 계획서 Part IV 도입에 등장하는 표현(재활용 가능). 가장 압축적.

---

## 우선순위 수정 사항 (Top 5)

1. **[Critical] 8장 → 9장 cliffhanger 연결 명시.** 8장 끝에 "정상 빌드가 안 된다 — 9장의 미스터리" 박스, 9장 도입을 8장 끝의 실패 명령에서 잇기. 멀티 모듈 분리 → bootJar 함정의 점프가 너무 빠르다.

2. **[Critical] Spring Boot 3.x → 4.x 마이그레이션 약속 명시.** 6장 또는 17장에 "Spring Boot 4.0 동작 변경점" 단순 한 줄을 넘어 "3.x → 4.x 옮길 때 무엇이 깨지는가" 섹션 명시. 책 표지에 Spring Boot 4.0을 박은 이상 핵심 페르소나의 절박한 질문에 답을 줘야 한다.

3. **[Critical] Part IV 분량 분산 (12장 + 13장 연속 9,500자 두 챕터).** 12장의 Plugin Portal 발행 부분을 줄이거나, 13장의 Toolchain 부분을 4장이나 6장으로 옮겨 분량 분산. 책의 가장 어려운 부분에서 독자 피로 누적 위험.

4. **[Should] 3장에서 lazy Property/Provider API를 빼고 12장으로 미루기.** 3장(Part I 입문~중급)에서 "Provider/Property API"가 너무 일찍 등장하면 독자가 무엇을 잡아야 할지 모른다. 3장은 "Kotlin DSL 문법 + Groovy 차이 + 큰따옴표 함정"으로 좁히고, lazy Property API는 12장 본문 표준으로.

5. **[Should] 1장에 Maven 출신 독자를 위한 첫 미끼 박스 + wrapper distribution-type 한 줄 추가.** 핵심 페르소나가 1장 도입에서 "내가 왜 이 책을 끝까지 읽어야 하는가"의 답을 받아야 한다. 4장이 첫 도착지이므로 1장에서 4장으로 연결.

---

## 잘된 점 (유지해야 할 것)

- **`shop` 가상 앱 + 챕터별 폴더 컨벤션 (`ch01/` ~ `ch16-security/`).** 코드 저장소가 챕터의 트랙이 된다는 약속이 책 전체에 신뢰성을 준다. GitHub 레포 구조까지 미리 박아둔 점이 강점.

- **5부 구조의 의미 부여.** 각 부의 "끝에서 독자가 자기 회사 빌드를 한 단계 위로 올릴 수 있다"는 약속이 명시되어 있다. 단순 챕터 분할이 아니라 독자 여정 단계로 설계.

- **9.5 신문법을 본문 표준으로 + 9.0 이전 차이는 마이그레이션 노트 박스.** 책이 "9.5 책"으로 정확히 포지셔닝됨. 17장 마이그레이션이 "옛 빌드를 9.x로"라는 별도 역할로 명확.

- **Part I·II에서 Maven 비교 박스 적극 활용 → Part III 이후 페이드아웃** 의 의도적 설계. 10장 "parent pom vs Convention Plugin"이 마지막 비교 박스라는 명시는 독자가 Gradle 사고로 옮긴 시점을 책 자체가 추적한다는 신호.

- **9장 bootJar 함정을 챕터 하나로 격상.** 책 전체의 차별점이 될 수 있는 부분. 핵심 페르소나가 실제로 막혔던 지점을 책의 클라이맥스로 박은 결정.

- **Out of Scope를 10개나 명시.** 독자 기대치 관리가 분명. Plugin Portal 발행, AGP, KMP, Develocity 운영을 명확히 빼는 결정이 분량 폭주를 막는다.

- **§7 작성자 셀프 체크 표.** 설계 원칙 5개를 챕터에 매핑한 자기 검증. 다음 라운드에서 추가 원칙(예: "F. 9.5 안정성 반영", "G. 함정 우선")이 들어와도 같은 형식으로 확장 가능.

---

## 종합 권고

저자에게: 이 계획서의 골격은 단단하고, 18장이 한 권의 책으로서 호흡한다. 가장 먼저 손을 댄다면 **(1) 8장 → 9장 cliffhanger 연결 + (2) Part IV 두 무거운 챕터의 분량 분산 + (3) 1장 도입의 Maven 출신 미끼 박스** 세 가지다. 이 셋은 모두 챕터 자체를 재배열하지 않고 챕터 안의 박스/도입부/일부 내용을 옮기는 수준이라 비용이 낮으면서 책의 호흡을 크게 개선한다.

Spring Boot 4.0 약속(3.x → 4.x)은 책의 표지 키워드와 직결되므로 6장 또는 17장에 명확한 섹션을 박아두는 것이 핵심 페르소나의 신뢰를 얻는 길이다. 3장의 lazy Property API 조기 노출 문제는 작은 수정이지만 입문 독자의 진입 장벽을 의외로 크게 낮춘다.

13개 영역 중 8개는 "잘 반영됨"이거나 "Nice-to-have" 수준이라 큰 손을 댈 필요가 없다. 골격을 흔들지 말고, 위 Top 5만 손보면 다음 단계(챕터 저술)로 넘어갈 준비가 충분하다.
