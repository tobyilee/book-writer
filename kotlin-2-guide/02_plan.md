# Kotlin 2.0 ~ 2.3 변경점 안내서 저술 계획 (Round 2)

이 책은 Kotlin 1.9까지 실무에서 써왔지만 2.x 변화의 흐름을 놓친 백엔드/안드로이드/시니어 개발자를 위한 안내서다. 한 번의 점프가 아니라 2.0 → 2.1 → 2.2 → 2.3에 걸쳐 *누적된* deprecation 캐스케이드를 시간 순서대로 따라가며, 각 언어 기능과 빌드 변화가 어떤 흐름으로 진행됐는지를 보여주는 데 중점을 둔다.

> Round 2 갱신 요약: 5·6·7장 순서를 *카테고리적 분리*에 맞춰 재배치(stdlib 풍요 → deprecation 캐스케이드 → context parameters), 9장을 12k → 8k 메타 챕터로 슬림화, 1~8장 마이그레이션 노트를 *한 줄 액션 + 9장 N.M 절 참조* 형식으로 변경, 2장·새 5장 제목을 장면 환기형으로 교체, 1장 끝에 IDE K2 모드 토글 박스 추가. 약한 핵심 질문 5개는 모두 review C6의 강한 대안으로 교체.

---

## 1. 책 제목 후보

### 후보 1. **Kotlin 2.x로 건너가는 길**
- **부제:** 1.9에서 멈춰 있는 코드베이스를 위한 누적 변경 안내서
- **한 문장 컨셉:** Kotlin 2.0부터 2.3까지의 변화를 *한 번의 점프*가 아닌 *시간 순서의 누적*으로 따라잡는 실무 가이드.
- **표지 무드:** 어두운 코발트 배경 위에, 1.9에서 2.3으로 이어지는 다리 실루엣과 K2 로고가 점진적으로 짙어지는 그라디언트.

### 후보 2. **K2 시대의 Kotlin**
- **부제:** 2.0부터 2.3까지, 컴파일러가 바뀌면 무엇이 함께 바뀌는가
- **한 문장 컨셉:** K2 컴파일러를 중심에 두고 언어·빌드·생태계가 어떻게 재정렬됐는지를 풀어내는 책.
- **표지 무드:** 차가운 강철 그레이 톤 위에 FIR(Frontend IR)을 형상화한 노드 그래프. 기술서 정통풍.

### 후보 3. **이미 늦지 않았다: Kotlin 2.x 따라잡기**
- **부제:** 1.9에서 멈춘 시니어를 위한 7번의 마이그레이션 노트
- **한 문장 컨셉:** "이미 한참 뒤처졌다"고 느끼는 개발자에게 *지금 시작해도 늦지 않다*고 말을 거는 동반자형 가이드.
- **표지 무드:** 따뜻한 종이 톤(아이보리)에 손글씨 느낌의 한글 제목, 코드 스니펫 일부가 워터마크처럼 깔린 에세이형 기술서.

**추천:** **후보 1 ("Kotlin 2.x로 건너가는 길")**.

이유는 세 가지다. (1) 책의 핵심 narrative arc가 "한 번의 점프가 아니라 누적 캐스케이드"인데, *건너가는 길*이라는 표현이 이 흐름을 가장 정확히 담는다. (2) 후보 2는 K2를 너무 강조해 언어 기능·생태계 챕터의 무게를 가린다. (3) 후보 3은 따뜻하지만 시니어 독자가 "조롱당한다"고 느낄 위험이 있다. 후보 1은 중립적이면서도 *여정성*을 강조해 Toby 스타일의 청유형 톤("함께 건너가 보자")과 자연스럽게 어울린다.

---

## 2. 책 특성

- **장르:** 기술 안내서 / 실용 가이드 (에세이형 톤을 가미한 기술서)
- **분량:**
  - **챕터 수:** 11개
  - **본문 글자 수:** 약 10만 7천 자 (하단 챕터별 분량 합계 기준)
  - **페이지 추정:** 약 360~390쪽 (한국어 기술서 표준 조판 기준 1쪽당 ≈ 280자)
- **난이도:** 중급. Kotlin 1.9까지의 실무 경험이 전제다. 코루틴, Gradle 빌드 스크립트(Kotlin DSL), sealed class, 제네릭, KMP의 기본 개념을 알고 있다고 가정한다. 컴파일러 내부 구현이나 IR 백엔드를 다룰 때는 *왜 그런 설계가 됐는지*를 짧게 풀어주되, 상세한 구현 분석은 의도적으로 피한다.
- **독자 여정:**

  > 책을 펼치는 독자는 이미 *늦었다는 자각*을 안고 있다. 빌드 로그에 뜨는 deprecation 경고, 동료가 "kotlinOptions 못 쓰지?"라고 던진 한마디, 그리고 GitHub 이슈에서 본 K2라는 단어. 이 책은 그 자각에서 출발해, **(1) "왜 2.x인가"의 큰 그림을 제공하고**, **(2) 언어 기능·빌드·표준 라이브러리의 누적 변화를 시간 순으로 따라가게 하며**, **(3) 자신의 코드베이스를 1.9에서 2.3까지 단계별로 끌어올릴 수 있게 만들고**, **(4) Spring/Ktor/Android Compose/KMP 같은 생태계 영향의 깊이를 가늠하게 한다**. 책을 덮을 때 독자는 "내일 아침 무엇부터 손댈지"가 명확해진다.

---

## 3. 챕터 목록

### 1장. 왜 K2를 더는 미룰 수 없는가 — 1.9에서 멈춘 사람들에게

- **이 변화는 누적 캐스케이드의 *0단계(현 위치 파악)*에 속한다.**
- **핵심 질문:**
  - "내 빌드 로그에 뜨는 deprecation 경고들, 그 끝은 어디일까?"
  - "Kotlin 2.0이 나왔다는 건 알았는데, 왜 그 뒤로도 세 버전이나 더 나왔을까?"
  - "1.9에서 한 번에 2.3으로 점프해야 할까, 아니면 2.0부터 차근차근 짚어야 할까?"
- **주요 내용:**
  - "이 책은 한 번의 점프 안내서가 아니다"라는 선언. 2.0 → 2.1 → 2.2 → 2.3에 걸쳐 *누적되는* 변화의 모양 미리보기.
  - JetBrains가 검증에 쓴 1,000만 줄·1만 8천 명·8만 프로젝트 규모와 그 의미.
  - 2.0이 단순히 "더 빠른 컴파일러"가 아니라 IDE 하이라이팅·플러그인 생태계·KMP 일관성의 기반이라는 사실.
  - 1.9에서 멈춰 있는 코드가 시간이 지날수록 *어떻게* 부서지는지의 체감 사례 (kotlinOptions 2.2부터 컴파일 에러, context receivers 2.3에서 제거 등).
  - 책의 진행 순서와 각 장 미리보기. 독자가 자기 상황에 맞는 챕터로 점프할 수 있는 *2~3가지 추천 동선*.
  - **[박스] IDE의 K2 모드 활성 절차 — 책 펼치는 그날 첫 행동** (한 페이지)
    - IntelliJ IDEA: `Settings → Languages & Frameworks → Kotlin → Enable K2 mode` 토글, 2024.2 이후 stable, 2025.1부터 기본값. 해제하려면 같은 경로에서 비활성화.
    - Android Studio: `Settings → Experimental → Enable K2 mode for Kotlin` (Iguana/Jellyfish 이후), 또는 `Help → Edit Custom Properties...`에 `idea.kotlin.plugin.use.k2=true`. velog @lifeisbeautiful의 한국어 후기 인용.
    - 토글 직후 *어떤 시그널을 봐야 하는지*: 하이라이팅 속도(1.8×), 자동완성(1.5×), Gradle sync 후 빨간 줄 *증가/감소* 패턴. *증가*하면 새 5장의 deprecation 노트, *감소*하면 새 7장의 context parameter 노트로 점프할 동선 안내.
- **1.9 vs 2.x 비교 포인트:**
  - 빌드 로그에서 1.9 vs 2.0 같은 모듈을 빌드했을 때 출력되는 경고/에러 라인의 *길이* 비교. 무미건조한 수치가 아니라 "한 화면을 채우는 deprecation 메시지"라는 시각적 충격을 준다.
- **예상 분량:** 약 8,000자
- **마이그레이션 노트(1줄 액션):** 자기 프로젝트의 측정 baseline을 모은다 — 컴파일 시간, 의존 라이브러리 목록, kapt/KSP 사용처. 자세한 절차는 9장 9.0절(사전 점검) 참조.

---

### 2장. 1.9 빌드는 통과했는데, K2는 왜 빨간 줄을 그어왔을까

*— 컴파일러가 처음으로 IDE와 같은 트리를 보기까지*

- **이 변화는 누적 캐스케이드의 *1단계(2.0 컴파일러 교체)*에 속한다.**
- **핵심 질문:**
  - "1.9 빌드는 통과했는데 2.0에서 갑자기 `open val a: Int`가 빨간 줄이 됐다 — 컴파일러가 무엇을 *새로 보기 시작했길래* 이걸 잡아내게 됐을까?"
  - "IDE는 코드를 한 모양으로 보고 컴파일러는 또 다른 모양으로 봤다고 해보자. 그 *두 시선*이 어긋날 때 우리가 겪었던 *알 수 없는 빨간 줄*은 어디서 왔던 걸까?"
  - "K2가 평균 2배 빨라졌다는데, 그럼 *내* 프로젝트도 그럴까?"
- **주요 내용:**
  - K1 → K2 아키텍처: PSI + BindingContext가 만든 *암묵적 의존*과 그 한계 (어휘 진입장벽 낮추기 위해 비유 먼저, 용어는 뒤에 따라붙임).
  - FIR(Frontend Intermediate Representation)이라는 단일 자료구조가 가져온 정렬: IDE-컴파일러-멀티플랫폼 일관성.
  - JetBrains 공식 벤치마크 (Anki +94%, Exposed +80%, 분석 단계 376% 등) 정직하게 인용.
  - **상충 관점**: Slack의 Zac Sweers가 측정한 −17% 회귀. 두 관점을 *나란히* 두고 "평균은 상승, 분산은 크다"는 결론.
  - 자기 프로젝트에서 K2 효과를 *직접 측정하는 법*: `kotlin.build.report.output=file`, clean vs incremental, ABI 변경 vs 미변경.
  - K2가 새로 *거르는* 컴파일 에러 — *본문에는 핵심 4가지*만 풀고(open property 즉시 초기화, star-projected setter, Java `int @Nullable []`, smart cast 정합성), 나머지 3가지는 **부록 A 표 형태**로 압축.
- **1.9 vs 2.x 비교 포인트:**
  - `open val a: Int` 패턴: K1 통과 → K2 에러. 동일 클래스를 1.9 / 2.0에서 빌드했을 때의 메시지 비교.
  - Java `int @Nullable []` 결과를 받는 코드: `dataService.fetchData()[0]` (1.9 OK) vs `dataService.fetchData()?.get(0)` (2.0 강제).
- **예상 분량:** 약 10,000자
- **마이그레이션 노트(1줄 액션):** "내 프로젝트의 K2 회귀 위험"을 1시간 안에 가늠한다 (kapt 의존, IR-기반 컴파일러 플러그인 사용처, lint K2 UAST 가능 여부). 체크리스트 본체는 9장 9.1절 참조.

---

### 3장. smart cast, data object, enumEntries — 2.0이 *조용히* 바꿔놓은 일상

- **이 변화는 누적 캐스케이드의 *1단계(2.0 컴파일러 교체와 동시 도입)*에 속한다.**
- **핵심 질문:**
  - "K2 안에서 smart cast가 똑똑해졌다는데, 정확히 어디서부터 *말이 통하기 시작했을까?*"
  - "리플렉션 한 번 부를 때마다 GC가 일을 더 하고 있었다면, 똑같은 한 줄을 어떻게 *비용 없는 한 줄*로 다시 적을 수 있을까?"
  - "sealed 계층의 마지막 케이스를 `object`로 두던 코드, 이제는 어떻게 다듬어야 깔끔할까?"
- **주요 내용:**
  - **smart cast 7가지 새 시나리오** (분리된 Boolean, OR 묶음, inline lambda 안의 mutable, 함수 타입 프로퍼티, try/catch/finally, 증감 연산자). 각각에 짧은 코드.
  - **data object** (1.9 beta → 2.0 Stable): `toString()`이 `EndOfFile@7a4f` 대신 `"EndOfFile"`로 떨어지는 차이.
  - **enumEntries\<T\>()** (2.0 Stable): 호출마다 새 배열을 만들지 않는다. reflection 기반 코드의 GC 부담이 어떻게 줄어드는지.
  - **AutoCloseable** (2.0 Stable, 공용): KMP에서 `use { }`를 *공통* 코드에서 쓸 수 있다.
  - 이 변화들이 왜 "조용히" 들어왔는지 — 코드 수정 없이도 K2 활성만으로 *행동이 바뀌는* 지점들을 짚는다.
- **1.9 vs 2.x 비교 포인트:**
  - smart cast: `val isCat = animal is Cat; if (isCat) animal.purr()` — 1.9는 unresolved reference, 2.0은 통과.
  - `enumValues<T>()` vs `enumEntries<T>()`: 내부적으로 어떤 객체가 매번 생성되는지 (간단한 메모리 비교 표).
- **예상 분량:** 약 11,000자
- **마이그레이션 노트(1줄 액션):** smart cast 강화로 *죽은 분기*가 된 `else throw IllegalState(...)` 패턴을 IDE 인스펙션으로 일괄 정리하고, `extraWarnings.set(true)`로 새 경고를 모은다. 자세한 절차는 9장 9.2절 참조.

---

### 4장. 2.1이 던진 세 장의 카드 — guard `when`, multi-dollar, non-local break

- **이 변화는 누적 캐스케이드의 *2단계(2.1 Preview → 2.2 Stable 졸업 코스)*에 속한다.**
- **핵심 질문:**
  - "1.9 시절 `is X -> if (cond) ... else ...`로 중첩되던 sealed 분기, 이제 어떻게 펼칠 수 있을까?"
  - "JSON Schema나 Bash heredoc을 문자열로 다룰 때 백슬래시로 도배되던 코드, 정말 깨끗해질 수 있을까?"
  - "lambda 안에서 `continue`를 쓰고 싶어 `?: run { ...; null }`로 우회하던 그 패턴, 이제는 작별할 수 있을까?"
- **주요 내용:**
  - **guard `when`** (KEEP-71140, 2.1 Preview → 2.2 Stable): `is Animal.Cat if !animal.mouseHunter -> ...`. opt-in 단계의 `-Xwhen-guards`와 2.2 이후의 무플래그 사용.
  - **multi-dollar interpolation** (KEEP-2425, 2.1 Preview → 2.2 Stable): `$$"""..."""`로 단일 `$`를 리터럴로 보존. JSON Schema 작성 사례.
  - **non-local break/continue** (KEEP-1436, 2.1 Preview → 2.2 Stable): inline lambda 안에서 `continue`. 1.9 시절의 우회 패턴 비교.
  - **sealed exhaustiveness 개선** (2.1 Stable): `else` 없이도 통과. 한국 커뮤니티의 *"왜 이걸 2.1에 와서야"* 정서를 인용해 공감대를 형성.
  - **`@SubclassOptInRequired`**: 라이브러리 작성자가 *상속* 시점에만 opt-in을 강제할 수 있는 이유와 효용.
  - 세 카드(guard·multi-dollar·non-local)가 모두 2.1 Preview → 2.2 Stable 코스를 똑같이 밟았다는 *패턴* 자체가 Kotlin 진화 방식의 메시지임을 짚기.
- **1.9 vs 2.x 비교 포인트:**
  - guard `when`: 1.9 중첩 `if-else` 버전 vs 2.2 guard 버전.
  - multi-dollar: JSON Schema 문자열 1.9 escape 지옥(`\$schema`) vs 2.2 `$$"""..."""`.
- **예상 분량:** 약 10,000자
- **마이그레이션 노트(1줄 액션):** Preview 기능을 *프로덕션 / 사이드 / 라이브러리* 중 어디까지 들일지 선을 긋고, opt-in 플래그 격리 패턴을 한 모듈로 좁혀둔다. 자세한 절차는 9장 9.2절 참조.

---

### 5장. build.gradle에서 한 줄씩 사라지는 의존성들 — 2.3까지의 stdlib

- **이 변화는 누적 캐스케이드의 *3단계(2.0 ~ 2.3에 걸친 표준 라이브러리 흡수)*에 속한다.**
- **핵심 질문:**
  - "라이브러리 의존성 트리에 *왜 여기에 Apache Commons가 끼어 있지?*라는 줄 하나가 박혀 있다고 해보자. Kotlin 2.2가 그 줄을 지워줄 수 있을까?"
  - "`kotlinx-datetime`을 따로 의존하던 코드, 이제 *표준 라이브러리* 만으로 살아남을 수 있을까?"
  - "UUID v7가 표준에 들어왔다는 건, 우리에게 어떤 새 *기본값*을 권하는 신호일까?"
- **주요 내용:**
  - **Base64 4종** (2.2 Stable): `Default`, `UrlSafe`, `Mime`, `Pem`. JVM에서 `output.encodingWith(Base64.Default)` 같은 스트림 통합.
  - **HexFormat** (2.2 Stable): `93.toHexString()` → `"5d"`. minLength·removeLeadingZeros로 세밀 제어.
  - **`kotlin.uuid.Uuid`** (2.0.20 Experimental → 2.3 강화): `Uuid.parse`, `random()`, `generateV4()`, `generateV7()`, `generateV7NonMonotonicAt(instant)`, `parseOrNull(...)`. JVM 측 `java.util.UUID`와의 양방향 변환.
  - **`kotlin.time.Clock` & `Instant`** (2.1.20 Experimental → 2.3 Stable): `kotlinx-datetime`이 표준 라이브러리에 흡수된 의미. `Clock.System.now()` 사용법.
  - **`kotlin.concurrent.atomics`** (2.1.20 Experimental, KMP 공용): `AtomicInt`, `AtomicLong`, `AtomicBoolean`, `AtomicReference`. JVM `j.u.c.atomic`과의 `asJavaAtomic()` / `asKotlinAtomic()` 변환.
  - **`AutoCloseable`** (2.0 Stable, 공용)이 KMP 라이브러리 작성에서 어떻게 코드 양을 줄이는지.
  - 이 변화들이 *외부 의존을 줄이는 방향*으로 정렬돼 있다는 메시지: KMP에서 *공통 코드 비율*이 자연스럽게 늘어나는 흐름. 챕터 끝에 *build.gradle에서 사라진 줄들* 미니 표를 둔다 (`commons-codec`, `kotlinx-datetime`, `j.u.c.atomic` 직접 의존 등).
- **1.9 vs 2.x 비교 포인트:**
  - `java.util.Base64.getEncoder()` (1.9 JVM 한정) vs `Base64.Default.encode(bytes)` (2.2, 공용).
  - `kotlinx-datetime`의 `Clock.System.now()` 의존 (1.9~2.1) vs 표준 라이브러리 `kotlin.time.Clock.System.now()` (2.3 Stable).
- **예상 분량:** 약 9,000자
- **마이그레이션 노트(1줄 액션):** Experimental 마크가 붙은 stdlib API는 *모듈 단위 opt-in*으로 격리해 들이고, 의존성 한 줄이 사라질 때마다 PR을 작게 끊어 올린다. 자세한 절차는 9장 9.3절·9.4절 참조.

---

### 6장. 컴파일 에러로 변한 deprecation들 — kotlinOptions의 마지막 1년

- **이 변화는 누적 캐스케이드의 *3단계(2.0 warn → 2.2 error 동기화 deprecation)*에 속한다.**
- **핵심 질문:**
  - "어제까지 경고였던 `kotlinOptions { }`가 오늘은 빨간 줄을 그어버린다면, 그 1년 사이에 무슨 일이 있었나?"
  - "Kotlin은 보통 deprecation을 2년 이상 끄는데, 왜 이 항목은 이렇게 빠르게 에러로 갔을까?"
  - "`kotlin-android-extensions`와 `withJava()`처럼 비슷한 운명을 따라간 *동기화된 deprecation*들은 또 무엇일까?"
- **주요 내용:**
  - **kotlinOptions {} 의 캐스케이드** — 1.9 deprecated → 2.0~2.1 warn → **2.2 컴파일 에러**. 사내 convention plugin이 늦게 대응해 빌드가 한 번에 멈추는 사례 (레퍼런스 §10.5).
  - **`kotlin-android-extensions`** — 1.9 deprecated → 2.2 제거. `kotlin-parcelize` + view binding 마이그레이션.
  - **Apple `ios()` / `watchos()` / `tvos()` shortcut** — 1.9 warn → 2.1 error → 2.2 removed. 명시 타깃으로의 강제 이주.
  - **`KotlinCompilation.source()`** — 2.0 error → 2.3 removed. `defaultSourceSet.dependsOn(...)` 패턴.
  - **Ant 빌드 시스템** — 2.2 deprecate → 2.3 완전 제거.
  - **누적 deprecation 표** (1.9 → 2.3) 한 페이지 시각화. 이 표가 책 전체에서 가장 많이 펼쳐질 페이지가 되도록 설계.
  - **롤백 안전망**: `compilerOptions { languageVersion.set(KotlinVersion.KOTLIN_1_9) }`로 K1 시맨틱 유지하는 법과 그 한계.
  - **[박스] KAPT4 캐스케이드** — 2.1 alpha (`kapt.use.k2=true` opt-in) → 2.1.20 default → 2.2.20에서 `kapt.use.k2` 자체 deprecated. 1.9 시니어 다수가 kapt 의존자라는 점에서 별도 한 페이지로 따로 본다.
- **1.9 vs 2.x 비교 포인트:**
  - `kotlinOptions { jvmTarget = "17" }` (1.9 warn) vs `kotlin { compilerOptions { jvmTarget.set(JvmTarget.JVM_17) } }` (2.2부터 강제).
  - `@Parcelize`: `kotlin-android-extensions` 시절 vs `kotlin-parcelize` 시절 plugin 블록 비교.
- **예상 분량:** 약 11,000자
- **마이그레이션 노트(1줄 액션):** 사내 buildSrc / convention plugin이 latest Kotlin을 따라가도록 CI에 `--warning-mode=fail`을 박아 *경고가 에러로 변하기 전에* 잡는다. 자세한 절차는 9장 9.3절 참조.

---

### 7장. context receivers의 묘비명, context parameters의 첫걸음

- **이 변화는 누적 캐스케이드의 *3단계(2.0.20 deprec → 2.2 신규 도입 → 2.3 제거)*에 속한다.**
- **핵심 질문:**
  - "`-Xcontext-receivers`로 즐겁게 쓰던 코드가 2.3에서 사라진다면, 우리는 무엇을 잃고 무엇을 얻는가?"
  - "context parameter에 *이름*을 강제한 결정은 옳았을까? scope pollution은 정말 그만한 대가였을까?"
  - "arrow-kt의 `Raise<E>.()` 같은 receiver-heavy 라이브러리는 어떻게 마이그레이션해야 할까?"
- **주요 내용:**
  - **context receivers의 짧은 역사**: 2.0.20 deprecate 시작 → 2.3 제거 예정.
  - **context parameters (KEEP-367)** 의 동기: scope pollution, callable reference 모호성, IDE 추적성.
  - **이름 강제**의 trade-off: `users.log(...)`의 명시성 vs 함수 본문의 verbosity.
  - **문법**: `context(users: UserService) fun outputMessage(...) { ... }`, `context(_: UserService) { ... }`, type matching으로 해소되는 디스패치.
  - **1.x → 2.2 마이그레이션 4가지 길**: (a) IntelliJ 인스펙션, (b) `context(receiver)` → `context(name: Receiver)`, (c) 단순 파라미터로 강등, (d) extension으로 강등.
  - **현 시점의 한계** (2.2.0): class·constructor 불가, callable reference 2.3에서 도입.
  - **bridge functions 패턴**: arrow-kt 같은 라이브러리가 *dual API* 기간을 두는 이유.
- **1.9 vs 2.x 비교 포인트:**
  - `context(Logger) fun foo() = info("bar")` (deprecated context receivers) vs `context(logger: Logger) fun foo() = logger.info("bar")` (2.2 context parameters).
  - 동일한 함수 시그니처를 4가지 마이그레이션 경로(IDE 자동·이름 부여·파라미터 강등·extension 강등)로 변형해보는 *한 페이지 비교*.
- **예상 분량:** 약 11,000자
- **마이그레이션 노트(1줄 액션):** 라이브러리 작성자라면 *dual API*를 한 메이저 사이클(약 1년)만 유지하고 다음 minor에서 정리한다. 단계별 시점 결정은 9장 9.3절 참조.

---

### 8장. 2.3의 신호들 — backing fields, return-value checker, 그리고 그 너머

- **이 변화는 누적 캐스케이드의 *4단계(2.3 Experimental → 2.4 Stable 졸업 후보)*에 속한다.**
- **핵심 질문:**
  - "`_city`와 `city: StateFlow`로 두 줄을 쓰던 그 어색한 패턴, `field = ...` 한 줄로 정말 사라질까?"
  - "Kotlin이 *함수의 반환값을 무시하지 마라*고 컴파일러 차원에서 잔소리를 하기 시작한 이유는 무엇일까?"
  - "2.3 시점의 Experimental 기능들, 그중 어떤 것이 *2.4 Stable*로 살아남을지 어떻게 가늠할까?"
- **주요 내용:**
  - **Explicit backing fields** (Experimental, `-Xexplicit-backing-fields`): `val city: StateFlow<String>; field = MutableStateFlow("")`. 기존 `_city` 패턴이 어떻게 사라지는지.
  - **Unused Return Value Checker** (Experimental, `-Xreturn-value-checker=check`): `@MustUseReturnValues`, 파일 단위 `@file:MustUseReturnValues`. 의도적 무시 관용 `val _ = computeValue()`.
  - **data-flow exhaustiveness for `when`** (2.2.20 Experimental → 2.3 Stable): 앞 분기 데이터 흐름을 인지해 `else` 없이 통과.
  - **expression body의 `return` 허용** (2.2.20 Beta → 2.3 Stable): `fun f(id: String?): String = g(id ?: return "default")`.
  - **suspend function type 오버로드 해소**, **catch 블록의 reified 제네릭** (2.2.20).
  - **`@JvmExposeBoxed`**, **annotations in Kotlin metadata** 같은 *라이브러리 작성자용* Experimental 묶음.
  - 2.3 Stable 졸업 패턴(2.1 Preview → 2.2 Stable, 2.2 Preview → 2.3 Stable)을 통해 *2.4가 가져올 졸업생*을 가늠하는 법.
- **1.9 vs 2.x 비교 포인트:**
  - `_city` + `val city: StateFlow<String> get() = _city.asStateFlow()` (1.9~2.2) vs `val city: StateFlow<String>; field = MutableStateFlow("")` (2.3 Experimental).
  - 함수 반환값을 그냥 흘려보내던 코드가 `@MustUseReturnValues` 도입 후 컴파일 경고/에러로 잡히는 모습.
- **예상 분량:** 약 9,000자
- **마이그레이션 노트(1줄 액션):** 2.3 Experimental은 *후보 모듈 한 곳*에 좁게 들이고 opt-in 어노테이션을 그 안에서 끝낸다. 2.4 Stable 전환 점검은 9장 9.4절 참조.

---

### 9장. 단계별 마이그레이션 플레이북 — 1.9에서 2.3까지 *네 번의 점검*

- **이 변화는 누적 캐스케이드 *전체*를 *시간 순서로 주관*하는 메타 챕터다.** 1~8장의 변화별 노트를 받아 *순서·시그널·롤백 안전망*만 묶는다. 구체 코드는 각 챕터로 점프해 본다.
- **핵심 질문:**
  - "거대한 한 번의 마이그레이션 PR이 아니라, *네 번의 점검*으로 나누어 가는 길은 어떻게 생겼을까?"
  - "각 단계에서 *가장 먼저* 부딪히는 함정은 무엇이고, *가장 늦게* 드러나는 회귀는 무엇일까?"
  - "롤백 안전망을 어디에 깔아두면 *어느 단계에서든 후퇴*할 수 있을까?"
- **주요 내용:**
  - **9.0. 사전 점검** (Sweers 권고): kapt → KSP 결정, `android.lint.useK2Uast=true`, 컴파일러 IR 의존 플러그인 점검 (Anvil 등). 시그널: clean build green / IR 플러그인 K2 호환 매트릭스 통과.
  - **9.1. 1.9 → 2.0** *순서·시그널·롤백 의사결정* — `kotlin = "2.0.x"`, `.gitignore`에 `.kotlin/` 추가, `kotlinOptions` → `compilerOptions`, Compose plugin ID 변경, 2장 4가지 컴파일 에러 흡수, 롤백 안전망 (`languageVersion = 1.9`). *완료 정의*: clean build + 핵심 모듈 incremental green.
  - **9.2. 2.0 → 2.1** — `extraWarnings.set(true)`로 새 경고 수집, K2 KAPT alpha (`kapt.use.k2=true`) 시도, 3장의 죽은 분기 정리, 4장 Preview 기능 도입 결정. *완료 정의*: warning 수 baseline 대비 ±10% 이내 안정화.
  - **9.3. 2.1 → 2.2** *책 전체에서 가장 위험한 단계* — `kotlinOptions` 잔존 점검(컴파일 에러 분기점), context receivers → context parameters (7장 4가지 길), `kotlin-android-extensions` 잔재 제거, JVM default method 변화 점검, `KotlinCompilation.source` 제거, KAPT4 default 전환. *완료 정의*: 6장 누적 deprecation 표의 모든 `error` 해소.
  - **9.4. 2.2 → 2.3** — `-language-version=1.8` 종료, Apple 최소 OS 상향, Intel Mac 시뮬레이터 정리, Compose stack trace mapping 활성, 5장 신규 stdlib API 채택, AGP 9.0+ 이주 (10장 *before/after*). *완료 정의*: `kotlin.experimental.tryNext`로 2.4-EAP 프리뷰까지 통과.
  - **공통 회귀 사례** (4가지 + 1): (a) 이벤트 소싱 람다 직렬화 깨짐 → `@JvmSerializableLambda`, (b) JUnit 5 백틱 한국어 메서드명 + 람다 명명으로 인한 path overflow, (c) Apple iOS framework 캐싱 stale → `./gradlew clean` + Xcode Clean Build, (d) buildSrc + Gradle 8.3 미만 호환, **(e) kotlinx-serialization 회귀** — invokedynamic 람다 직렬화와 serialization 컴파일러 플러그인이 같이 얽힐 때의 ABI 불일치.
  - **build.gradle.kts *full diff 한 페이지*** — 1.9 시절 → 2.3 시점의 한 파일을 *통째로* 비교. 9장의 *물리적 정수*. 이 페이지가 책에서 가장 많이 펼쳐질 한 장이 되도록 설계한다.
- **1.9 vs 2.x 비교 포인트:**
  - 위 build.gradle.kts full diff 페이지가 비교 그 자체.
- **예상 분량:** 약 8,000자
- **마이그레이션 노트:** 챕터 자체가 메타 노트이므로 본문 노트 없음. *내일 아침 첫 commit 체크리스트*는 **부록 B로 이전**해 펼쳐 쓰기 좋은 형태로 둔다.

---

### 10장. 생태계의 적응 — Spring, Ktor, Android Compose, KMP

- **이 변화는 누적 캐스케이드의 *전 단계에 걸친 외곽 적응*에 속한다.**
- **핵심 질문:**
  - "Spring Boot Gradle plugin이 KMP 모듈에 닿는 순간 왜 deprecation warning이 쏟아질까?"
  - "어제까지 `kotlinCompilerExtensionVersion = "1.5.14"` 한 줄로 발이 묶였던 우리 빌드가, 2.3에서는 `alias(libs.plugins.compose.compiler)` 한 줄로 끝난다고 해보자. 우리가 *잃은 것*은 정말 없을까?"
  - "AGP 9.0이 `org.jetbrains.kotlin.android` 플러그인을 빌트인으로 흡수한다는 건 안드로이드 빌드 스크립트에 어떤 신호일까?"
- **주요 내용:**
  - **Spring Boot / Ktor**: Spring Boot Gradle plugin의 자동 Application 플러그인 적용으로 인한 KMP 충돌 → *separate subproject* 권고. Ktorfit의 빠른 K2 추격(2.0.0~2.1.0 RC). Ktor IDEA 플러그인의 K2 모드 미호환 이력(IDEA 2024.3 이전). *kotlinx-serialization 컴파일러 플러그인 호환* 한 줄 박스.
  - **Android & Jetpack Compose**: `composeOptions { kotlinCompilerExtensionVersion = ... }` 시대의 종언, `kotlin("plugin.compose") version <kotlin-version>`로의 통합. 2.0.20부터 Strong Skipping Mode 기본값. AGP·Gradle·Xcode 호환 매트릭스 (2.0.21 ~ 2.3.21).
  - **[박스 1] AGP 9.0+ 빌드 스크립트 다이어트** — *before/after 한 페이지*. 1.9 시절 plugins 블록 + composeOptions vs AGP 9.0+ 빌트인 흡수 후의 슬림화된 한 파일.
  - **KMP & kotlinx-coroutines**: 메이저 Kotlin 릴리스 + 1쿼터 시차로 따라오는 coroutines 안정 minor (1.8.0 ~ 1.11.0-rc01) 시간 지도. coroutines 1.11.0-rc01의 Wasm/JS *breaking* (`JsAny` 서브타입만 허용).
  - **Compose Multiplatform**: 2.0 동시 통합, 2.2.20 Wasm Beta, 2.3 Swift Export 기본 활성.
  - **K2 IDE 경험**: IDEA 2024.2 K2 mode stable → 2025.1 기본값. "1.8× faster code highlighting and 1.5× faster code completion".
  - **Lint K2 UAST**: `android.lint.useK2Uast=true` + `android.experimental.lint.version`.
  - **[박스 2] Apollo Kotlin / Anvil의 K2 도입기** — 컴파일러 IR 의존 플러그인이 *어떻게* K2에 적응했는지 한 박스. Apollo 블로그·Sweers preparing-for-k2 인용.
  - **자기 생태계 진단 체크리스트**: 우리 프로젝트가 어느 *조합*에 속하는지 위치 잡는 법. *분산이 진실*이라는 메시지를 스택 조합 진단으로 다시 호명한다.
- **1.9 vs 2.x 비교 포인트:**
  - Compose 모듈의 build.gradle.kts: 1.9 시절(`composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }`) vs 2.3 시점(`alias(libs.plugins.compose.compiler)` + `composeCompiler { featureFlags = ... }`).
  - kotlinx-coroutines 의존 라인이 Kotlin 메이저에 따라 어떻게 따라가는지 1.8.0 → 1.11.0-rc01 표.
- **예상 분량:** 약 11,000자
- **마이그레이션 노트(1줄 액션):** 자기 회사 *기술 스택 조합*을 한 줄로 적고, 그 조합에서 가장 위험한 단계에 9장 N.M 절을 라벨로 붙인다.

---

### 11장. 아직 끝나지 않은 길 — 2.4를 향한 가늠자, 그리고 우리에게 남은 결정

- **이 변화는 누적 캐스케이드 *그 다음 단계(2.4 Stable)*를 향한 가늠이다.**
- **핵심 질문:**
  - "2.3 Experimental 명단 중 어떤 항목이 2.4 Stable로 졸업할 가능성이 높을까?"
  - "Kotlin 2.x의 변화가 우리에게 가르친 *진화 패턴*은 무엇이고, 그 패턴은 어떻게 다음 메이저에 적용될까?"
  - "이제 우리는 1.9를 떠나 2.3에 도달했다. 그렇다면 *내일 아침 첫 commit*은 무엇이어야 할까?"
- **주요 내용:**
  - **2.3 Experimental 졸업생 후보**: explicit backing fields, return-value checker, UUID v7. 2.1→2.2, 2.2→2.3의 패턴으로 졸업 가능성을 가늠.
  - **알려진 미해결**: macosX64/iosX64/tvosX64/watchosX64 2.4 제거, KSP2 미성숙, KotlinConf 2025 발표(있다면) 단서.
  - **이 책이 의도적으로 다루지 않은 영역의 좌표**: KSP2 깊은 내부, Kotlin/Native 컴파일러 디테일, paper-research 학술 논문(거의 없음). 독자가 다음에 어디로 가야 하는지 이정표.
  - **[박스] 사내 도입 정당화용 *대체 자료*** — "국내 대형사 사례 부재"를 인정하는 한 줄 다음에, 결정자 무기로 쓸 수 있는 자료 묶음을 박스로 둔다.
    - GitHub 메이저 OSS의 K2 도입 PR 모음 (Square 진영, Apollo, Anvil, Ktor 등).
    - JetBrains *Customer Story* 페이지 트래킹 (Anki, Exposed 등).
    - KotlinConf 한국어 발표 / 한국 KUG 발표 트래킹.
    - 자기 회사 사례를 *오픈소스 후기로 남기는* 행동 권유.
  - **5가지 큰 그림 다시 정리** (책 시작에 던진 질문들에 대한 답):
    1. K2는 단순 빠른 컴파일러가 아니라 IDE/플러그인 생태계의 기반이다.
    2. 2.x는 한 번의 점프가 아니라 *4단계의 누적 캐스케이드*다.
    3. Preview → Stable의 시간 지도는 *패턴*이지 우연이 아니다.
    4. 빌드 스크립트가 1.9에서 2.3까지 가장 많이 바뀐 *현장*이다.
    5. 자신의 프로젝트로 직접 측정하라 — 평균이 아니라 *분산*이 진실에 가깝다.
  - **마지막 청유**: 이 책을 닫고 IDE를 여는 순간, *언제까지* 어떤 단계를 마칠 것인지 한 줄로 적어보자.
- **1.9 vs 2.x 비교 포인트:**
  - 책 1장에서 보여준 "1.9 → 2.0 빌드 로그" 한 화면을 *2.3 빌드 로그*와 다시 한번 나란히 둠으로써, 책 전체를 한 컷으로 닫음.
- **예상 분량:** 약 9,000자
- **마이그레이션 노트:** 챕터 자체가 마무리이므로, 본문 노트 대신 **부록 B "내일 아침 첫 commit 체크리스트"**로 넘긴다.

---

### 부록 (책 끝)

- **부록 A. K2가 새로 거르는 컴파일 에러 — 7가지 표.** 2장 본문에서 핵심 4가지를 풀고, 나머지 3가지를 포함한 전체 표는 여기서 한 페이지로 펼친다.
- **부록 B. 내일 아침 첫 commit 체크리스트.** 9장 9.0 ~ 9.4 단계별 *오늘·이번 주·이번 분기* 액션을 한 페이지 워크시트로 둔다.
- **부록 C. 누적 deprecation 표 (1.9 → 2.3).** 6장의 표를 책 전체에서 펼쳐 쓰기 좋도록 부록에도 한 번 더 둔다.

---

## 4. 챕터 간 흐름 (Narrative Arc)

이 책은 *호기심 → 직시 → 손쉬운 수확 → 비싼 값 → 미래 → 종합 → 외곽 → 마무리*의 8단 곡선으로 진행된다. Round 1의 "감정 곡선" 가정을 버리고, 시니어 결정자에게 더 잘 작동하는 *카테고리적 분리*로 다시 짰다.

**1장**은 독자가 가진 *늦었다는 자각*을 직시하고 책의 동선을 깐다. 챕터 끝의 IDE K2 모드 토글 박스가 *책을 펼치는 그날의 첫 행동*이 된다. **2장**은 K2 컴파일러라는 가장 큰 변화를 정직한 양면(94% 가속 vs 17% 회귀)으로 보여줘 *무비판적 낙관*도 *과장된 공포*도 갖지 않도록 톤을 잡는다. 여기까지가 호기심·직시 단계다.

**3·4·5장**은 *손도 안 대고 깔끔해진다*의 흐름이다. 3장은 K2 활성만으로 *조용히* 행동이 바뀐 것들(smart cast, data object, enumEntries), 4장은 2.1이 던진 세 장의 카드(guard `when`, multi-dollar, non-local break), 5장은 build.gradle에서 *한 줄씩 사라지는 의존성들*(Base64, kotlin.time, UUID, atomics). 시니어 독자는 이 세 장에서 "쉽게 얻는 것"의 윤곽을 잡는다.

**6·7장**은 그 정반대 — *비용을 치르는 영역*이다. 6장은 deprecation이 컴파일 에러로 변한 1년(kotlinOptions, kotlin-android-extensions, KAPT4 캐스케이드)을, 7장은 context receivers의 묘비명과 context parameters의 첫걸음을 다룬다. 5장과 6장 사이의 톤 전환이 책의 *카테고리 경첩*이다 — "stdlib은 풍요로워졌지만 그 풍요를 받기 위해 빌드 스크립트와 receiver 시그니처는 다시 쓴다." **8장**은 2.3이 보여주는 미래(backing fields, return-value checker)를 짧게 둔다.

**9장**은 책 전체의 종합 — *단계별 마이그레이션 플레이북*이다. 1~8장의 모든 변화를 *시간 순서*로 다시 묶되, 본문은 *순서·시그널·롤백 의사결정*과 *build.gradle.kts full diff 한 페이지*에 집중한다. 구체 코드는 각 챕터를 다시 펼치면 된다. **10장**은 그 액션 플랜을 *생태계 좌표*에 비춘다 — Spring, Ktor, Android Compose, KMP, Apollo·Anvil 도입기. **11장**은 책을 닫으며 미래(2.4)를 가늠하고, *대체 자료 박스*로 결정자에게 마지막 무기를 쥐여준다.

이 순서가 중요한 이유는 (1) "쉽게 얻는 것 / 비싸게 치르는 것"의 카테고리적 분리가 시니어 독자의 *결정 부하*를 줄이고, (2) 6·7장 직후에 오는 9장 플레이북이 *방금 본 비용*을 시간 순서로 곧장 묶어주며, (3) 9장이 메타 챕터로 슬림화되면서 1~8장 각자가 *변화별 고유 무게*를 회복하기 때문이다.

---

## 5. 챕터 분량 분포 (Round 2 재배분)

```
1장  8,000자  | 2장 10,000자 | 3장 11,000자 | 4장 10,000자
5장  9,000자  | 6장 11,000자 | 7장 11,000자 | 8장  9,000자
9장  8,000자  | 10장 11,000자 | 11장 9,000자
합계 약 107,000자
```

이전 분포 대비 변경: **2장 12k → 10k**(에러 7가지 → 본문 4 + 부록 A 표), **3장 9k → 11k**(smart cast 7가지를 코드와 함께 풀 여유), **9장 12k → 8k**(메타 챕터로 슬림화), **11장 8k → 9k**(2.4 가늠 + 대체 자료 박스). 5·6·7장은 새 번호 기준으로 9k / 11k / 11k.

후반부 평탄대(이전 5·6·9·10이 11k+로 평균)가 풀렸고, 9장(8k) → 10장(11k) → 11장(9k) 자연 감소 곡선을 얻었다.

---

## 6. 책 전체에 흐르는 핵심 메시지 3가지

1. **K2는 단순히 빠른 컴파일러가 아니라, IDE 하이라이팅·플러그인 생태계·KMP 일관성을 떠받치는 *기반 인프라*다.** 컴파일 시간 ±94%/−17%의 분산보다 더 큰 변화는, 같은 FIR 위에서 IDE와 컴파일러와 멀티플랫폼이 *처음으로 같은 트리를 본다*는 사실이다.

2. **Kotlin 2.x는 *한 번의 점프*가 아니라 *4단계에 걸친 누적 deprecation 캐스케이드*다.** kotlinOptions가 2.0 warn → 2.2 error로, context receivers가 2.0.20 deprec → 2.3 제거로, KAPT4가 2.1 alpha → 2.1.20 default → 2.2.20 deprecated로 흘러온 *시간의 모양*을 이해해야, 1.9에 멈춘 코드를 어느 단계로 끌어올릴지 결정할 수 있다.

3. **벤치마크의 평균이 아닌 *분산*이 진실이고, 마이그레이션의 표준 답안이 아닌 *내 프로젝트의 측정*이 권위다.** Anki +94%와 Slack −17%가 같은 컴파일러에서 나오는 사실, 사내 buildSrc가 2.2 컴파일 에러를 어떻게 맞이하는지의 사례 — 평균 뒤의 *내 케이스*를 직접 확인하지 않으면 어떤 가이드도 무력하다.

---

## 7. 위험 요소 / 의도적 제외

이 책에서 *다루지 않기로* 한 영역과 그 이유.

1. **KSP2 내부 구현 디테일.** KSP2는 책 작성 시점(2026-04)에서 메이저 라이브러리 마이그레이션이 진행 중이고, 내부 API가 아직 안정 단계 아니다. 이 책은 *KSP1 → KSP2 권고 시점*과 *K2 KAPT 디폴트화*까지만 다루고, KSP2 내부 구현은 별도 자료(KSP GitHub, KotlinConf 2025 발표)로 넘긴다.

2. **Kotlin/Native 컴파일러 백엔드와 LLVM 통합 디테일.** 2.3의 Swift Export 향상, 2.2.20의 Native concurrent GC 정도는 다루지만, LLVM IR 매핑이나 K/N 메모리 모델은 이 책의 독자(백엔드/안드로이드/KMP 사용자)에게 *과한 깊이*다.

3. **Compose Multiplatform의 *모든* 안정성 변화.** Compose for iOS, Web의 stability 변천은 Compose Multiplatform 자체 changelog에서 더 정확하다. 이 책은 *Compose 컴파일러와 Kotlin의 결속*까지만 다룬다.

4. **국내 대형 서비스(카카오·우아한형제들·라인·NHN)의 K2 도입 후기.** 검색 가능한 1차 자료가 부족하다는 한계를 인정하고, velog와 Medium-Korean의 개인 후기를 인용하는 선에서 그친다. 11장에서 이 빈틈을 *대체 자료 박스*로 채운다.

5. **학술 논문 인용.** 본 주제는 학술 논문이 거의 존재하지 않는다. KotlinConf / JVMLS 발표와 KEEP 디자인 문서를 학술 트랙의 대체로 사용하며, paper-research 트랙의 부재를 *의도적 누락*으로 인정한다.

6. **YouTrack KT-* 이슈 단위의 회귀 deep-dive.** What's new에 명시된 회귀와 Sweers·DigitalFrontiers가 정리한 사례까지만 다루고, 살아 있는 K2 회귀 이슈의 전체 목록은 책의 분량을 넘는다.

7. **Kotlin 2.4 / 2.5 미래 추정.** 2.3 Experimental 졸업 패턴으로 *가늠*은 하지만, 11장에서 명시적으로 "이는 추정이며 KEEP / KotlinConf 2025의 1차 자료를 따로 확인할 것"을 권한다.

8. **빌드 시스템 *전반* 비교(Bazel, Buck, Pants 등).** Gradle / Maven 위주로 다루고, 그 외 빌드 시스템의 K2 지원은 의도적으로 제외한다.

이 제외 목록은 책의 *약속*이자 *경계*다. 독자가 이 책 한 권으로 모든 답을 얻을 거라 기대하지 않도록, 11장 마지막에 다시 한번 정리한다.
