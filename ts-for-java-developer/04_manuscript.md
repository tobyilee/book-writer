# 왜 TypeScript는 이렇게 생겼는가

## 부제
Java/Kotlin 개발자를 위한 언어와 생태계 전환서

## 저자
Toby-AI

---

## 서문 — 이 책이 당신에게 건네는 약속

월요일 아침을 상상해보자. 10년 가까이 Spring으로 백엔드를 짜온 사람이, 오늘은 처음으로 TypeScript 코드베이스를 열어야 한다. 화면에는 `class`도 있고 `interface`도 있는데, 어느 것도 `implements`라고 적히지 않았다. `import`는 패키지 경로가 아니라 `./user-service` 같은 상대 경로다. `pom.xml`은 없고 `package.json`이 있다. 그 옆에 `tsconfig.json`도, `vite.config.ts`도, `.eslintrc.cjs`도 있다. 한 화면에 빌드 책임이 다섯 군데로 흩어져 있다.

"어차피 자바스크립트인데 며칠이면 적응하지." 그 마음이 자연스럽다. 며칠이면 문법은 익는다. 그러나 언어를 *사용하는 것*과 그 언어가 *왜 그렇게 생겼는가*를 이해하는 것은 다른 일이다. 정적 타입을 모국어처럼 써온 개발자에게 후자가 훨씬 까다롭다. TypeScript는 Java나 Kotlin이 자란 토양과 정반대 토양 위에서 자란 언어이기 때문이다.

이 책은 그 *왜*에 답한다.

### 이 책이 지키는 약속 네 가지

**첫 번째, TypeScript 언어의 깊이.** 문법 소개에서 멈추지 않는다. 점진적 타입 시스템이 왜 `any`라는 탈출구를 필요로 하는지, 구조적 타입이 왜 Java의 명목 타입보다 도메인 안전성이 헐거운지, 의도된 unsoundness가 어떤 실용적 이유에서 나왔는지를 논문과 설계 문서에 근거해 풀어낸다. 언어를 *사용하는* 수준을 넘어 *왜 이렇게 만들었는가*를 손에 쥐는 것이 목표다.

**두 번째, JavaScript와의 관계.** TypeScript는 JavaScript 위에 타입을 얹은 도구다. 컴파일이 끝나면 타입은 사라지고, 남는 것은 순수한 JavaScript다. 그 JavaScript가 가진 본성 — `this`의 일곱 가지 얼굴, 프로토타입 체인, 단일 스레드 이벤트 루프, null과 undefined의 이원성 — 이 모든 것이 TypeScript 안에서도 그대로 살아 숨 쉰다. 이 토대를 모르면 타입이 있어도 런타임에서 자꾸 발이 걸린다.

**세 번째, Java/Kotlin과의 정직한 대조.** 각 챕터마다 Java/Kotlin의 코드와 TypeScript의 코드를 나란히 놓는다. 비슷해 보이는 자리에서 무엇이 다른지, 다른 이유가 무엇인지를 솔직하게 말한다. Spring DI와 NestJS DI, `CompletableFuture`와 Promise, sealed class와 discriminated union, checked exception과 Result 타입. 익숙한 개념에서 출발해 낯선 세계로 가는 다리를 놓는다.

**네 번째, CLI에서 풀스택까지 전 영역.** 언어만 알아서는 부족하다. CLI 도구, Electron/Tauri 데스크톱, React 웹 프론트엔드, NestJS/Hono/Express 웹 백엔드, Next.js 풀스택, 테스트 전략까지 — TypeScript가 실제로 살아가는 영역을 모두 걷는다.

### 이 책을 읽으면 좋을 사람

Java/Spring 또는 Kotlin을 수년 이상 써온 백엔드·풀스택 개발자로서, TypeScript는 처음이거나 표면적으로만 써본 사람이 이 책의 정중앙 독자다. TypeScript 문법을 이미 아는 사람에게는 *왜 그렇게 생겼는가*의 답이 새롭게 보일 것이다. 이제 막 TypeScript를 시작하는 사람에게는 처음부터 올바른 멘탈 모델을 잡을 기회가 된다.

### 이 책을 읽는 법 — 직무별 추천 경로

책 전체를 처음부터 끝까지 읽으면 가장 좋다. 하지만 지금 당장 마주한 문제에 따라 어디서부터 읽을지가 다를 수 있다.

**백엔드 시니어 (Java/Spring → TS 백엔드).** 1·2·3장으로 언어 토대를 잡고, 4·5장에서 타입 도구를 손에 익히고, 6장(도메인 모델링)→7장(비동기)→8장(빌드/모듈)→13장(NestJS/Hono)→15장(한국 현장) 순으로 읽자. 프론트엔드도 함께 다룬다면 12장을 추가한다.

**프론트엔드 시니어 (React + TS 본격 도입).** 1·2·3장으로 토대를 쌓고, 4·5장을 반드시 통과한 뒤 12장(React + TS)으로 직행한다. 8장(빌드 도구)과 14장(테스트)을 곁들이면 완성된다.

**풀스택 시니어 (한 사람이 전체를 짜야 하는 스타트업).** 디자인 박스와 함정 박스만 따라가도 빠른 지도가 잡힌다. 한 번 통독한 뒤 자기 직무에 맞는 경로로 다시 들어가자.

**마이그레이션 담당자 (기존 JS 코드베이스를 TS로).** 1·2·3장으로 토대를 잡고, 9장(점진적 마이그레이션)을 정독한 뒤 부록 D(함정 사전)를 옆에 두고 작업하자.

### 박스 안내

이 책의 모든 챕터에는 네 종류의 박스가 반복된다.

- **📚 Java/Kotlin 시선 박스**: 챕터당 최소 두 개. 양쪽 코드를 나란히 놓고 비교한다. 이 박스만 따라가도 전환 경로의 빠른 지도가 보인다.
- **🚧 함정 박스**: 한국 커뮤니티에서 반복 보고된 12개 함정을 증상→원인→처방 구조로 분산 배치했다. 통합본은 부록 D.
- **💡 작가의 한 마디 박스**: 동의하지 않아도 좋다. 동의하지 않는 자리에서 자기 의견이 분명해진다.
- **📖 더 깊이 가려면 박스**: 챕터 끝마다 하나. 1차 자료와 한국어 자료를 함께 안내한다.

### 감사의 말

이 책이 존재하는 이유는 TypeScript를 처음 마주했을 때의 그 찜찜함 때문이다. 왜 컴파일은 통과했는데 런타임에서 터지지? 왜 타입을 적었는데도 헐겁게 느껴지지? 그 질문들이 책 한 권이 되었다. 같은 질문을 품고 커뮤니티에 글을 올려준 모든 개발자들 — 스택 오버플로, 토스 기술블로그, 카카오 기술블로그, 네이버 D2 — 에게 감사한다. 그들의 경험이 이 책의 재료다.

---

## 목차

### 서문

### 1부 — 환상
- 1장. Java 개발자가 TypeScript를 열어보면

### 2부 — 본성
- 2장. JavaScript의 진짜 본성 — 타입을 붙이기 전에 알아야 할 것
- 3장. TypeScript는 무엇이며, 무엇이 아닌가 — 컴파일타임의 환상

### 3부 — 무기
- 4장. 타입을 손에 익히기 — 추론·좁히기·exhaustive를 도구로
- 5장. 타입을 만드는 타입 — 제네릭·conditional·infer·매핑·템플릿 리터럴
- 6장. 이 도메인을 어떻게 모델링할까 — 구조적 타입 위에서 잃지 않는 법
- 7장. 비동기 모델 — Promise·async/await·Observable·AsyncIterator
- 8장. 빌드 도구가 왜 이렇게 많은가 — 모듈·패키지·번들러·런타임의 분열

### 4부 — 전환
- 9장. 기존 JS 코드를 TS로 옮기기 — 점진적 도입의 패턴

### 5부 — 응용
- 10장. CLI를 짓는다 — 명령줄 도구로 TS의 첫 응용
- 11장. 데스크톱 앱 — Electron과 Tauri의 네이티브 경계
- 12장. 웹 프론트엔드 — React + TS의 핵심, 그리고 다른 reactivity 모델의 위치
- 13장. 웹 백엔드와 풀스택 — Express·Fastify·Hono·NestJS·Next·Astro의 여섯 길
- 14장. 테스트와 타입 — Vitest·expect-type·Playwright

### 6부 — 종합
- 15장. 한국 현장의 TypeScript — 함정·논쟁·AI 시대·다음 한 걸음

### 부록
- 부록 A. Java/Kotlin ↔ TypeScript 용어 매핑 사전
- 부록 B. tsconfig 옵션 사전
- 부록 C. TS CLI 한 개 끝까지 짓기 — 워크쓰루
- 부록 D. 한국 개발자 함정 사전 — 12개 인덱스

### 책을 닫으며

---

---

# 1부 — 환상

첫 페이지를 열고 드는 직관은 대부분 절반쯤 맞고 절반쯤 틀린다. "TypeScript는 그냥 JavaScript에 타입 붙인 거 아닌가?" — 이 첫인상이 어디까지 맞고 어디서부터 틀리는지를 1부가 짚는다. 1장은 답을 주는 장이 아니라, 좋은 질문을 손에 쥐어주는 장이다. 지도를 펼치는 것이 1부의 역할이다. 나머지 열네 챕터를 걷기 전에, 먼저 지도의 윤곽을 잡자.

이 부에서 만나는 챕터:
- 1장. Java 개발자가 TypeScript를 열어보면

---

# 1장. Java 개발자가 TypeScript를 열어보면

월요일 아침이라고 상상해보자. 10년 가까이 Spring으로 백엔드를 짜오던 손이 오늘 아침에는 다른 일을 받아 들었다. 사내 어드민 화면을 React로 새로 짠다는데, 코드베이스가 전부 TypeScript라고 한다. "TypeScript? 그거 그냥 자바스크립트에 타입 좀 붙인 거지" — 머릿속에 떠오르는 첫 문장이 이 정도다. Java로 단단한 도메인 모델을 짜오던 사람에게 *타입을 붙였다*는 표현은 친숙하게 들린다. 별거 아닐 것 같다. IntelliJ를 켜고, 클론하고, 한 줄을 읽기 시작한다.

그런데 화면에 펼쳐진 코드가 묘하게 낯설다. `class`도 보이고 `interface`도 보이는데, 어느 클래스도 어떤 인터페이스를 `implements` 한다고 적어놓지 않았다. `import`가 있긴 한데 패키지 경로 같은 게 없고, `./user-service`처럼 상대 경로가 들어 있다. 빌드 도구를 보려고 `pom.xml`을 찾는데 없고 대신 `package.json`이 있다. 그 안을 열어 봤더니 `dependencies`, `devDependencies`, `scripts` 정도는 알겠는데 `tsconfig.json`이라는 게 또 따로 있고, 그 옆에 `vite.config.ts`도 있고, `.eslintrc.cjs`도 있고, `pnpm-workspace.yaml`도 있다. 한숨이 한 번 나온다. 한 화면 안에 빌드 책임이 다섯 군데로 흩어져 있다.

여기서 누군가는 무심코 이렇게 말한다. "그래도 어차피 자바스크립트인데 며칠이면 적응하지." 정말 그럴까? 며칠이면 *문법*은 적응한다. 함수 선언 앞에 `function` 대신 화살표를 쓰고, 세미콜론을 빼고, `let`과 `const`를 구분해서 쓰는 정도는 금방이다. 그러나 *언어*에 적응하는 것과, 그 언어가 만들어진 *이유*를 이해하는 것은 다른 일이다. 그리고 정적 타입을 모국어처럼 써온 개발자에게는, 후자가 훨씬 까다롭다. 왜냐하면 TypeScript는 Java나 Kotlin이 자라난 토양과 정반대 토양 위에서 자란 언어이기 때문이다. 그 토양의 이름은 *동적 자바스크립트*다.

이 책의 1장은 그래서 답을 주는 장이 아니라, 좋은 질문을 받는 장이다. *"TS는 그냥 JS에 타입 붙인 거 아닌가?"* 이 첫인상이 어디까지 맞고 어디서부터 틀리는지, 왜 베테랑 정적 타입 개발자에게 TS를 *처음부터 다시* 배워야 하는지 — 두 질문을 손에 쥐고 다음 페이지로 넘어가자. 답은 책 전체에 흩어져 있다.

## TypeScript의 첫 만남 — 익숙한 듯 낯선 세 줄 정의

가장 친절한 한 줄 정의부터 가져와 보자. TypeScript 공식 문서가 스스로를 어떻게 부르는지 보면 의외로 간결하다.

> *"TypeScript is JavaScript with syntax for types."*

자바스크립트에 타입을 위한 문법을 더한 것. 이 한 줄을 액면 그대로 받으면, Java 개발자의 첫 직관 — *"그냥 JS에 타입 붙인 거"* — 과 정확히 일치한다. 그런데 이 한 줄이 묘한 점이 있다. *"a language"*라고 하지 않고 *"JavaScript with syntax for types"*라고 한다. 새 언어를 만든 게 아니라 기존 언어에 *문법을 더했다*는 뉘앙스다. 이 작은 차이가 책 전체를 관통하는 모든 결정의 출발점이다. 잠깐 멈추고 한 번 더 음미하자. 새 언어가 *아니다*. 

그렇다면 TypeScript의 실체는 정확히 무엇으로 이루어져 있는가? 한 줄 정의를 분해해 보면 세 가지가 묶여 있다.

**(1) 타입 주석 문법.** 변수·함수 인자·반환·객체·제네릭에 콜론을 찍고 타입을 붙이는 문법이다. `let count: number = 0` 같은 모양. 이 문법은 자바스크립트의 합법적 코드 위에 *얹혀* 있고, 컴파일이 끝나면 흔적도 없이 사라진다. Java의 타입 주석이 클래스 파일에 메타데이터로 남는 것과 정반대다.

**(2) 컴파일러 `tsc`.** Microsoft가 제공하는 표준 컴파일러다. 하는 일은 두 가지다. 첫째, 타입 주석을 보고 타입 검사를 한다. 둘째, 검사가 끝나면 타입을 지우고 평범한 자바스크립트로 변환한다. *타입 검사*와 *트랜스파일* — 이 두 일을 한꺼번에 하기 때문에 `tsc`는 느리다. 이 느림이 나중에 Vite, esbuild, swc 같은 빌드 도구가 왜 따로 등장했는지를 결정한다.

**(3) 언어 서비스.** 에디터에 붙어 자동완성·정의로 이동·리팩터링·실시간 에러 표시를 제공하는 *서버*다. VS Code의 그 빠릿한 자동완성, IntelliJ의 강력한 추론 — 모두 이 언어 서비스가 뒤에서 돌아간 결과다. Java 개발자가 IntelliJ에서 누리던 IDE의 똑똑함이 자바스크립트 세계에도 비로소 들어온 셈이다. 사실 많은 사람들이 *언어로서의* TypeScript보다 *언어 서비스로서의* TypeScript에 더 큰 빚을 지고 있다.

이 셋을 합쳐 한 문장으로 다시 적어보자. **TypeScript는 (1) 자바스크립트 위에 얹는 타입 주석 문법과 (2) 그것을 검사하는 컴파일러와 (3) 그것을 에디터에 연결해주는 언어 서비스의 묶음이다.** 이 셋 중 어느 하나라도 빠지면 TypeScript의 실체가 잡히지 않는다. 특히 세 번째 — 언어 서비스 — 의 존재감을 놓치면, *왜 굳이 자바스크립트에 또 한 겹을 얹었는가*라는 질문에 잘 답할 수 없다. 대형 코드베이스에서 *변수 하나의 타입을 마우스만 올려도 안다*는 것이 얼마나 큰 자산인지, 한 번 누려본 사람만 안다.

여기서 잠시 자존심 한 조각을 내려놓자. Java 개발자가 IntelliJ로 누리는 그 일상적 편안함 — 자동완성·refactor → rename·find usages — 을, 자바스크립트 세계는 오랫동안 *부럽게* 바라봐 왔다. TypeScript의 등장은 이 부러움에 대한 정면 응답이었다. *"우리도 그 정도는 누리고 싶다"*는 자바스크립트 진영의 오랜 갈증. 그래서 Anders Hejlsberg — Turbo Pascal·Delphi·C#을 만든 그 사람 — 가 Microsoft에서 TS를 시작했을 때 슬로건이 *"JavaScript that scales."* 였다. 작은 스크립트로는 충분하던 자바스크립트가 *큰 시스템*으로 자라기 위해 무엇이 필요한가 — 이 질문에 대한 답이 TypeScript다.

## "JS의 슈퍼셋"이라는 슬로건과 그 함정

TS를 설명할 때 가장 자주 나오는 표현이 있다. *"TS는 JS의 strict superset이다."* 슈퍼셋. 상위집합. 즉, *모든 합법적 자바스크립트 코드는 합법적 타입스크립트 코드*라는 뜻이다. 이 슬로건이 갖는 무게는 생각보다 크다. 무엇보다도 *기존 자바스크립트 코드를 한 줄도 고치지 않고 그대로 TS 프로젝트에 가져다 쓸 수 있다*는 약속이 여기에 들어 있다. JS 파일 하나를 그대로 두고 확장자만 `.ts`로 바꿔도 컴파일이 통과한다. 약간의 과장을 보태면, *세상의 모든 npm 패키지가 잠재적으로 TS의 일부*라는 의미다.

Java 개발자에게 이 약속이 어떻게 다가오는지 잠깐 멈춰서 생각해보자. Java에는 이런 약속이 없다. Kotlin은 JVM 위에서 Java와 상호 운용되긴 하지만, 그것은 *바이트코드 레벨*의 호환이지 *소스 코드의 슈퍼셋*은 아니다. Kotlin 컴파일러에 `.java` 파일을 던지면 컴파일이 안 된다. 그런데 TS는 그게 된다. `.js` 파일을 `tsc`에 던지면 통과한다. 이 이상한 일이 가능한 이유는 단순하다. *TS는 JS의 슈퍼셋이 되기로 작정하고 설계된 언어*이기 때문이다.

그런데 여기에 함정이 하나 숨어 있다. *"슈퍼셋이라서 안전하다"*가 아니라는 점이다. 슈퍼셋이라는 말은 *JS의 모든 것을 받아들였다*는 뜻이지, *JS의 모든 거친 부분을 길들였다*는 뜻이 아니다. 자바스크립트가 가지고 있는 자유분방함 — `==`와 `===`의 차이, `undefined`와 `null`의 두 종류 빈 값, `this`의 일곱 가지 얼굴, 프로토타입 기반 객체 모델, 단일 스레드 이벤트 루프 — 이 모든 것이 TS 안에서도 *그대로* 살아 숨 쉰다. 타입 주석이 그 위에 얇은 보호막을 씌울 뿐이다. 이 사실을 제대로 이해하지 않으면, TS를 *Java보다 약간 자유로운 정적 언어* 정도로 오해하기 쉽다. 그리고 이 오해는 실제 프로젝트에서 *조용히 비싸게* 청구된다.

또 하나의 함정. *"슈퍼셋"*이라는 말은 *런타임 동작이 같다*는 약속이지 *타입 검사가 만능이다*라는 약속이 *아니다*. TS는 *컴파일 타임에만* 타입을 본다. 런타임의 자바스크립트 엔진은 TS가 무엇을 검사했는지 *전혀 모른다*. JSON으로 들어온 외부 데이터, 서드파티 라이브러리의 응답, 사용자가 폼에 넣은 문자열 — 이 모든 것이 *런타임에는 그냥 자바스크립트 값*이다. TS의 타입 검사는 그 값들이 *우리가 적은 타입대로 흘러갈 거라는 가정* 위에서 돈다. 이 가정이 깨지는 순간, TS는 아무 도움도 주지 못한다.

이 부분을 처음 들으면 찜찜하다. Java 개발자에게 *타입*이라는 단어는 *런타임 안전*과 거의 동의어다. `String`이라고 선언한 변수에는 `Integer`가 들어올 수 없다 — 이것은 컴파일 시에도 막히고, 만약 reflection으로 우회해도 런타임에 `ClassCastException`이 던져진다. *타입은 런타임까지 보장한다*. 그게 Java의 약속이다. TS의 약속은 다르다. TS의 약속은 *컴파일 시점의 도움*까지다. 런타임은 자바스크립트의 영역이다. 그곳까지 책임지지 않는다. 이 차이를 받아들이는 데 시간이 걸린다. 시간이 걸려도 받아들여야 한다. 받아들이지 않으면 매번 *왜 타입을 쓴다고 했는데 런타임에 터지지?*라는 질문을 되풀이하게 된다.

그렇다면 TS는 신뢰할 수 없는 언어인가? 그렇지는 않다. 학계의 측정이 하나 있다. ICSE 2017에 발표된 Gao, Bird, Barr의 연구는 GitHub의 실제 자바스크립트 버그 수정 400건을 분석해, *그중 약 15%는 TypeScript나 Flow가 미리 잡았을 것*이라고 추정했다. 100점짜리는 아니다. 그러나 *공짜로 받는 15%의 안전망*이라는 표현은 정확하다. 게다가 이 15%는 *대형 코드베이스의 리팩터링 시점*에 압도적으로 집중된다. 즉, 코드가 작을 때는 TS의 효용이 작지만, 코드가 자라고 사람이 늘수록 TS가 빛난다. 슬로건이 *"JavaScript that scales"*인 이유가 여기에 있다.

> **📚 Java/Kotlin 시선: JVM 하나에 모인 도구 vs 분산된 JS 생태계**
>
> Java/Kotlin 개발자가 JS/TS 프로젝트를 처음 열고 가장 먼저 받는 충격은 *도구의 분산*이다. Java 진영은 거의 모든 것이 JVM 하나에 응축되어 있다.
>
> ```text
> [Java/Kotlin 진영]
> 언어:   javac / kotlinc
> 런타임: JVM (HotSpot, GraalVM, OpenJ9)
> 빌드:   Gradle / Maven
> 패키지: Maven Central (단일 표준)
> 테스트: JUnit / Kotest
> IDE:    IntelliJ (사실상 표준)
> ```
>
> 한 줄로 표현하면 *"하나의 JVM, 하나의 표준 패키지 저장소, 하나의 IDE."*이다. 학습 곡선이 평탄한 대신, 선택의 자유는 작다.
>
> JS/TS 진영을 같은 형식으로 펼쳐보면 충격이 분명해진다.
>
> ```text
> [TypeScript 진영]
> 언어:    tsc / esbuild / swc / Babel
> 런타임:  Node.js / Bun / Deno
> 빌드:    Vite / Webpack / Turbopack / Rollup / Parcel
> 패키지:  npm (registry) + pnpm / yarn / npm (CLI)
> 테스트:  Vitest / Jest / Playwright / Mocha
> IDE:     VS Code (표준), WebStorm, Neovim, Zed
> ```
>
> 한 칸 한 칸이 다 *경쟁 중인 도구*다. 표준이 *늦게* 정착하는 생태계의 본질적 모습이다. 이 점을 일종의 *결함*으로만 보면 학습이 괴롭다. 그러나 다르게 보면, JS 진영은 *언어 표준(ECMAScript)*과 *도구 생태계*를 일부러 분리해두고 도구는 시장 경쟁에 맡긴 셈이다. 이 분리가 무서운 속도의 혁신을 만들어 낸다 — esbuild는 Go로, swc는 Rust로, Bun은 Zig로 작성되어 각자 *수십 배* 빠른 속도를 가져왔다. JVM 진영은 이 속도의 혁신을 거의 누리지 못했다.
>
> 적응 팁 하나. 처음에는 *모든 도구를 다 익히려 하지 말고*, *VS Code + tsc + Vite + Vitest + pnpm* 정도의 한 묶음을 표준으로 정해 두고 시작하자. 시야가 잡히고 나면 다른 도구로 갈아타는 일은 며칠이면 된다. 첫날부터 *어떤 번들러가 최고인가*를 고민하면 한 발도 못 뗀다.

## 다섯 핵심 모델 — 이름만 호명하고 다음 장으로 넘긴다

지금까지 *TS는 무엇인가*에 대한 한 줄 정의를 분해했다. 그리고 *"슈퍼셋"*이라는 슬로건이 갖는 약속과 함정을 들여다봤다. 이제 한 발 더 나가서, *TS의 타입 시스템 자체*가 Java/Kotlin과 어떻게 다른지를 *이름만* 호명하고 넘어가자. 본격 설명은 3장에 양보한다. 1장의 역할은 *지도를 펼치는 것*이지, 한 칸 한 칸을 채우는 것이 아니다. 다섯 단어를 머리에 올려두면 다음 장들이 훨씬 쉽게 읽힌다.

**첫째, 점진적(gradual).** TS의 타입 시스템은 *전부 정적*이지 않고 *전부 동적*도 아니다. 한 프로그램 안에 *타입이 있는 부분*과 *없는 부분*이 공존할 수 있다. `any`라는 타입이 그 둘 사이의 경계 역할을 한다. 이 설계는 *기존 자바스크립트 코드를 한 줄씩 천천히 TS로 옮길 수 있게 하기 위해서* 의도된 것이다. Java 개발자에게는 이 점이 어색하다. *모 아니면 도*가 아니라 *조금씩*이다. 9장에서 이 점진적 도입의 실제 패턴을 다룬다.

**둘째, 구조적(structural).** TS는 *모양이 같으면 같은 타입*이다. Java는 *이름이 같으면 같은 타입*(nominal)이다. 이 한 단어 차이가 도메인 모델링의 모든 것을 바꾼다. `class Dog implements Animal`이라고 적지 않아도 멤버가 맞으면 `Animal` 자리에 `Dog`가 들어간다. 편하다. 동시에 *타입을 만들었다는 안전함*이 흐릿해진다. `type UserId = string`이 그냥 `string`과 호환된다. 이 헐렁함을 어떻게 메우는가 — *branded type*이라는 처방이 있고, 6장에서 본다.

**셋째, unsound (의도된 비건전성).** 학술적 용어로는 *건전하지 않은 타입 시스템*이다. 즉, *컴파일이 통과해도 런타임에 타입이 안 맞을 가능성이 남아 있다*. Bierman, Abadi, Torgersen의 ECOOP 2014 논문이 이를 정리해 두었고, TS 설계 문서의 **Non-goals** 항목에는 *"Apply a sound or 'provably correct' type system"*이 *명시적으로 거부*되어 있다. *건전성을 일부러 포기*했다는 뜻이다. 왜? *생산성과 점진적 도입*을 위해서다. 이 결정의 합리성을 *Sound Gradual Typing Is Dead?*(Takikawa et al., POPL 2016)가 정량화했다 — 건전성과 점진성을 동시에 요구하면 평균 7배, 최악 100배의 런타임 슬로다운이 발생한다. *이 비용을 치르지 않기로 한 결정*이 TS의 unsound다.

**넷째, erased (지워진다).** TS의 모든 타입 정보는 *컴파일이 끝나면 사라진다*. 결과물은 평범한 자바스크립트다. 런타임에는 타입이 없다. 그러므로 Java처럼 `obj.getClass().getName()`으로 클래스 이름을 꺼내거나, generic의 type parameter를 reflection으로 보거나, `@Annotation`을 reflection으로 읽어내거나 하는 일이 *기본적으로 불가능*하다. 예외가 하나 있다 — `experimentalDecorators` + `emitDecoratorMetadata` + `reflect-metadata` 라이브러리를 켜면 *부분적으로* 메타데이터를 보존할 수 있다. NestJS, TypeORM, class-validator 같은 프레임워크가 이 모드 위에 서 있다. 이 *예외*가 8장과 13장에서 NestJS를 다룰 때 다시 나온다.

**다섯째, TC39 정렬.** TS는 *자바스크립트 언어 표준의 진화에 의도적으로 보조를 맞춘다*. 자바스크립트 표준은 ECMAScript라는 이름으로 TC39라는 위원회가 Stage 0부터 4까지의 프로세스로 진화시킨다. TS는 *TC39가 채택한 것은 받아들이고, 채택하지 않은 것은 가급적 만들지 않는다*는 원칙을 갖고 있다. 그래서 TS 5.0의 새 데코레이터, top-level await, `satisfies` 연산자 같은 것들은 모두 TC39 제안과 정렬되어 있다. 단, 역사적으로 *TC39 이전에 TS가 만든* 몇몇 기능 — `enum`, `namespace`, 옛 데코레이터 — 이 남아 있어 갈등의 씨앗이 된다. 이 갈등이 13장 NestJS의 데코레이터 논쟁으로 이어진다.

다섯 단어. **점진적 / 구조적 / unsound / erased / TC39 정렬.** 외울 필요는 없다. 이 책의 챕터들이 진행되면서 다섯 단어 각각이 어떤 결정과 함정을 만들어 내는지를 자연스럽게 보게 된다. 다만 다음 한 가지는 지금 명심해두자 — *Java의 직관을 그대로 가져오면 다섯 단어 모두에서 발이 걸린다*. 그것이 베테랑 정적 타입 개발자가 TS를 *처음부터 다시* 배워야 하는 이유다. 문법은 며칠이면 익는다. 그러나 이 다섯 가지 결정의 *이유*를 손에 익히는 데에는 책 한 권이 필요하다. 그래서 이 책이 있다.

## 익숙해질 어휘 열 개 — 매핑부터 손에 쥐자

언어를 옮길 때 가장 든든한 친구는 *어휘 매핑*이다. *내가 아는 그 단어가 저쪽에서는 어떤 단어로 불리는가*를 손에 쥐면, 처음 보는 코드도 절반은 이해된다. 그래서 1장의 마지막에서 두 번째 절은 *Java/Kotlin 개발자가 TS 코드를 읽을 때 가장 자주 마주치는 열 개의 단어*를 짝지어 준다. 전체 매핑은 *부록 A*에 표 한 장으로 정리해 두었다. 여기서는 그중 핵심만 *왜 이렇게 짝지었는가*를 곁들여 보자.

**1. JVM ↔ Node.js / Bun / Deno.** Java의 런타임은 JVM 하나로 통일되어 있다. TS의 런타임은 셋이다. **Node.js**는 사실상 표준이다. 11년의 안정성과 가장 깊은 생태계를 가지고 있다. 프로덕션 서버는 거의 Node다. **Bun**은 2022년 등장한 Zig 기반의 통합 도구로 — 런타임·패키지 매니저·번들러·테스트 러너를 한 바이너리에 묶어두었고, 속도가 압도적이다. CLI나 dev tooling은 Bun으로 이미 많이 넘어왔다. **Deno**는 Node의 창시자 Ryan Dahl이 *Node에서 후회하는 것들*을 고치려고 만든 런타임이다. 보안이 기본(allow-net 같은 권한 부여 모델), 표준 라이브러리, TS를 *일급으로* 직접 실행하는 점이 강점이다. Deno 2의 npm 호환으로 게임이 다시 시작됐다. 2025년 현장의 현실적 합의는 *로컬 개발·CLI는 Bun, 프로덕션 서버는 Node, 보안과 표준이 가치 있는 곳은 Deno* 정도다.

**2. JAR / Maven Central ↔ npm 패키지 / npmjs.com.** Java 개발자는 Maven Central이라는 *하나의 표준 패키지 저장소*에 익숙하다. 이름·버전·서명이 깔끔하다. TS는 npm registry라는 단일 저장소를 갖긴 하지만, *trust boundary*가 매우 느슨하다. 누구나 이름만 점유하면 패키지를 올릴 수 있고, *typosquatting*과 공급망 공격의 위험이 상존한다. *작은 패키지 수십 개를 조립해서 큰 시스템을 만든다*는 npm 문화 자체가 Java의 *큰 라이브러리 몇 개를 신중히 고른다*는 문화와 정반대다. 부록 D의 함정 사전에서 자세히 본다.

**3. Gradle / Maven ↔ npm/pnpm + tsc + Vite/esbuild.** Java의 빌드 책임은 Gradle 하나가 거의 전부 진다 — 의존성 해결, 컴파일, 테스트, 패키징, 배포까지. TS의 빌드 책임은 *분산되어 있다*. 의존성은 npm/pnpm이, 타입 검사는 tsc가, 트랜스파일은 esbuild/swc가, 번들링은 Vite/Rollup이, 데브 서버는 또 Vite가 — 도구가 다섯 개다. 처음에는 어지럽다. 그러나 *각 도구가 한 가지를 잘하고, 갈아 끼우기 쉽다*는 장점이 있다. 8장에서 풀어 본다.

**4. Spring DI ↔ NestJS DI.** Java 베테랑이 TS 백엔드로 건너올 때 가장 친숙한 다리가 NestJS다. `@Module`, `@Controller`, `@Injectable`이 Spring의 `@Configuration`, `@RestController`, `@Service`와 거의 *1:1로 대응*한다. 한국 백엔드 개발자가 *"NestJS는 Spring 다시 쓰는 기분"*이라고 푸념하는 동시에 *"그래서 좋다"*라고 말하는 이유가 여기에 있다. 13장에서 NestJS·Express·Fastify·Hono를 비교한다.

**5. `CompletableFuture` / Reactor `Mono` ↔ `Promise` / `async`/`await`.** Java의 `CompletableFuture`나 Reactor의 `Mono`가 단일 비동기 값의 표현이라면, TS의 `Promise`가 정확히 그 자리다. `async`/`await`는 Promise 위의 syntax sugar로, Kotlin coroutine의 `suspend`와 표면적으로 비슷하게 읽힌다. 단, *내부 모델이 같지는 않다* — Kotlin coroutine은 진짜 *suspend point*가 있고 dispatcher 위에서 돈다면, JS의 `async`는 *마이크로태스크 큐*에 콜백을 등록하는 것에 가깝다. 7장에서 자세히.

**6. Reactor `Flux` / RxJava ↔ RxJS의 Observable.** 다중 값 비동기 스트림이 필요할 때 Java가 Reactor를 꺼내듯, TS는 RxJS의 `Observable`을 꺼낸다. 단, RxJS는 *언어 표준이 아니라 라이브러리*다. 모든 곳에서 쓰이지는 않고, Angular 진영에서 가장 짙게 쓰인다. React 진영은 신호(signal) 기반 reactivity와 React Query 같은 데이터 페칭 라이브러리로 더 가벼운 길을 택한다.

**7. Kotlin `sealed class` + `when` ↔ TS *discriminated union* + `switch`.** Kotlin의 `sealed class` + `when` 조합이 *대수적 데이터 타입의 안전한 분기*를 표현한다면, TS는 *discriminated union*으로 같은 일을 한다. `kind: "circle" | "square"` 같은 공통 리터럴 필드가 *판별자*가 되고, `switch`에서 모든 분기를 다루지 않으면 `never` 타입을 통해 컴파일 에러가 난다. *exhaustiveness check*의 메커니즘이 다른 셈이다. Kotlin은 컴파일러가 sealed 계층을 안다. TS는 *판별자 필드*와 *never*의 트릭으로 같은 효과를 만든다. 6장에서 본다.

**8. Java `null` / Kotlin `?.` `!!` ↔ TS `strictNullChecks` + `?.` `??`.** Java의 `null`은 *모든 참조 타입의 잠재적 값*이다 — `NullPointerException`이 명예의 전당을 차지하는 이유다. Kotlin은 nullable 타입(`String?`)과 non-null 타입(`String`)을 *문법적으로 분리*해서 NPE를 거의 박멸했다. TS는 `strict` 옵션(특히 `strictNullChecks`)을 켜면 Kotlin과 매우 비슷한 안전성을 얻는다. `?.`(optional chaining)와 `??`(nullish coalescing)가 Kotlin과 거의 같은 모양으로 작동한다. 단, *주의할 점*이 두 가지다. 첫째, TS에는 *두 종류의 빈 값*(`null`과 `undefined`)이 있다. 둘째, `strictNullChecks`를 *나중에 켜면* 기존 코드 전체가 빨개지므로 처음부터 켜고 시작하는 편이 낫다.

**9. Kotlin `data class` / Java record ↔ TS `interface` / `type` (+ `Object.freeze`).** Kotlin의 `data class`나 Java 16+의 record가 *불변 도메인 객체*의 표현이라면, TS에서는 `interface`나 `type`을 쓴다. 다만 *immutability 강제*는 약하다 — `readonly` 키워드와 `Readonly<T>` 유틸리티 타입이 *컴파일 시점*에는 막아주지만, 런타임에는 평범한 객체로 변환된다. 진짜 불변이 필요하면 `Object.freeze()`를 쓰거나, Effect-ts·Immutable.js 같은 라이브러리를 쓴다. 6장에서 도메인 모델링을 다룰 때 자세히.

**10. `@Valid` + Bean Validation ↔ zod / valibot / class-validator.** Spring에서 `@Valid`와 Bean Validation으로 *컨트롤러 진입점에서 입력 검증*을 했다면, TS에서는 `zod`라는 라이브러리가 그 자리에 있다. 차이가 하나 있다 — zod는 *타입을 정의하면 동시에 런타임 검증 함수가 만들어지고, 검증 함수에서 타입을 추론할 수 있다*. 이 *역방향 추론*이 TS 진영의 표현력을 크게 끌어올린 핵심 패턴이다. Java/Kotlin에는 정확히 같은 자리의 도구가 없다. 6장과 13장에서 *boundary validation* 패턴으로 다시 만난다.

이 열 개를 머리에 올려두면, 앞으로의 챕터들이 훨씬 부드럽게 읽힌다. *부록 A*에는 같은 형식으로 30여 개의 매핑이 표 한 장으로 정리되어 있다. 통째로 외울 필요는 없다. 코드를 읽다가 *"이게 Java로 치면 뭐였지?"*라고 머뭇거리는 순간, 부록 A를 펴자. 그게 그 표의 쓰임새다.

> **📚 Java/Kotlin 시선: Spring DI ↔ NestJS DI 첫 비교**
>
> 한국 Java 베테랑이 TS 백엔드로 건너올 때 가장 자주 만나는 다리가 NestJS다. *얼마나 닮았는지*를 가장 짧은 코드로 보면 한 번에 잡힌다. 같은 *유저 등록 컨트롤러*를 양쪽에서 짜 본다.
>
> ```java
> // Java + Spring Boot
> @RestController
> @RequestMapping("/users")
> public class UserController {
>
>     private final UserService userService;
>
>     public UserController(UserService userService) {
>         this.userService = userService;
>     }
>
>     @PostMapping
>     public ResponseEntity<User> create(@Valid @RequestBody CreateUserDto dto) {
>         return ResponseEntity.ok(userService.create(dto));
>     }
> }
>
> @Service
> public class UserService {
>     public User create(CreateUserDto dto) { /* ... */ }
> }
> ```
>
> ```typescript
> // TypeScript + NestJS
> @Controller('users')
> export class UserController {
>   constructor(private readonly userService: UserService) {}
>
>   @Post()
>   async create(@Body() dto: CreateUserDto): Promise<User> {
>     return this.userService.create(dto);
>   }
> }
>
> @Injectable()
> export class UserService {
>   async create(dto: CreateUserDto): Promise<User> { /* ... */ }
> }
> ```
>
> 데코레이터 이름만 바뀌었지 *구조가 거의 똑같다*. `@RestController` → `@Controller`, `@Service` → `@Injectable`, 생성자 주입은 양쪽 다 *생성자 인자에 의존성을 받아 필드에 보관*한다. NestJS의 `@Module`은 Spring의 `@Configuration`과, exception filter는 `@ControllerAdvice`와 1:1이다. *익숙함의 다리*가 여기서 나온다.
>
> 그러나 *완전히 같지는 않다*는 점도 짚고 가자. NestJS의 데코레이터는 TS의 *legacy `experimentalDecorators` 모드*에 의존하고, 그 위에서 `reflect-metadata` 라이브러리로 메타데이터를 읽는다. TS 5.0이 *새로운 표준 데코레이터*를 채택한 뒤로, NestJS는 *언제 어떻게 갈아탈 것인가*라는 무거운 질문을 안고 있다. *어쩌면 갈아타지 않을 수도 있다*는 시나리오까지 거론된다. 13장에서 이 논쟁을 자세히 다룬다. 지금은 한 가지만 기억해두자 — *NestJS는 Spring과 가장 닮았지만, 그 닮음이 영구히 안전하다는 보장은 없다*.

## 책 사용법 — 어디를 어떻게 읽으면 좋은가

여기까지 읽었다면, 한 가지 솔직한 질문이 떠오를 법하다. *"좋다, TS의 모양은 알겠다. 이 책을 어떻게 읽어야 하지? 처음부터 끝까지 다 읽어야 하나?"*

다 읽으면 좋다. 그러나 *지금 당장 마주한 문제*에 따라 *어디부터* 읽으면 좋은지가 다르다. 책을 도구로 쓰자. 다음의 직무별 추천 경로를 권한다.

**(A) 백엔드를 TS로 짜야 하는 Java/Spring 베테랑.** 이 책의 정중앙을 통과하는 길이다. 권하는 순서는 다음과 같다.
1. **2~3장**(JS의 본성과 TS 타입 시스템의 기초). 여기서 다섯 핵심 모델의 *왜*가 잡힌다.
2. **6장**(도메인 모델링) → **7장**(비동기) → **8장**(빌드/모듈/런타임). Java 백엔드 사고가 직접 부딪히는 세 영역이다.
3. **13장**(웹 백엔드와 풀스택)에서 NestJS를 중심에 두고, Express/Fastify/Hono의 위치를 잡는다.
4. **15장**(한국 현장)에서 *내가 다음에 무엇을 배우면 되는가*를 본다.

프론트엔드를 동시에 다뤄야 한다면 **4~5장**(타입 도구의 정수)과 **12장**(React + TS)을 추가로 읽자. 4~5장을 건너뛰면 React Hooks의 타입이 이상하게 어렵게 느껴진다.

**(B) 프론트엔드 개발자로 React + TS를 본격적으로 다룰 사람.** 이 길은 약간 다르다.
1. **2~3장**으로 토대를 쌓고,
2. **4~5장**(타입 추론·좁히기·exhaustive·제네릭·conditional·infer)을 *반드시* 통과한다. 12장 React가 이 두 장 위에 서 있다.
3. **12장**(React + TS의 핵심).
4. **8장**(빌드 도구)을 가볍게 훑어 Vite·Turbopack·Webpack의 위치를 잡는다.
5. **14장**(테스트)에서 Vitest와 Playwright를 손에 익힌다.

**(C) 기존 JS 코드베이스를 TS로 *마이그레이션*해야 하는 사람.** 이 길은 짧다.
1. **2~3장**으로 토대,
2. **9장**(JS→TS 점진적 도입의 패턴)을 정독,
3. 부록 D의 12개 함정 사전을 옆에 놓고 작업.

**(D) CLI나 데스크톱 앱이 필요한 사람.** **10장**(CLI), **11장**(Electron/Tauri)으로 바로. 단, *그 전에* 2~3장은 거치자. 8장 빌드도 가볍게.

**(E) 풀스택을 한 사람이 다 짜는 신생 스타트업의 시니어.** 거의 전 장을 읽는 길이지만, *디자인 박스만 따라가도* 빠른 지도가 잡힌다. 한 번 통독한 뒤 직무가 결정되면 (A)나 (B)로 다시 들어가자.

이 책의 *디자인 박스*에 대해서도 한 마디. 모든 챕터에 다음 네 종류의 박스가 일관되게 들어 있다.

- **📚 Java/Kotlin 시선 박스**: 챕터당 최소 두 개. 좌(Java/Kotlin) – 우(TS)의 코드 비교다. 이 박스만 따라가도 *Java 베테랑이 새 언어로 가는 가장 빠른 길*이 보인다.
- **🚧 함정 박스**: 호명된 챕터에 하나 이상. *증상 → 원인 → 처방* 구조로, 한국 커뮤니티에서 반복적으로 보고된 12개 함정을 분산 배치했다. 통합본은 부록 D.
- **💡 작가의 한 마디 박스**: 챕터당 한 개(선택). 작가의 목소리가 짙게 드러나는 자리. 동의하지 않아도 좋다 — 동의하지 않는 자리에서 자기 의견이 분명해진다.
- **📖 더 깊이 가려면 박스**: 챕터 끝마다 하나. 그 챕터를 더 깊이 파고 싶은 독자에게 권하는 1차 자료(공식 문서·논문·한국 블로그 한두 개씩).

> **💡 작가의 한 마디 — *어렵지 않다*는 거짓말**
>
> TypeScript 입문서를 펴면 종종 만나는 문장이 있다. *"TypeScript는 어렵지 않습니다. JavaScript에 타입만 붙인 것이니까요."* 이 문장을 만났을 때 가장 위험한 사람은 — 정적 타입을 모국어로 써온 베테랑 개발자다. 왜냐하면 그 사람은 그 문장을 *그대로 믿어버리기* 때문이다. 자바스크립트를 잘 모른다는 사실을 잠시 잊고, *내가 알던 정적 타입의 직관을 그대로 가져다 대면 되는구나*로 넘어가 버린다. 그리고 한 달쯤 지난 어느 날, *왜 컴파일은 통과했는데 런타임에 undefined가 흘러 들어왔는지*를 디버깅하면서 그 문장의 무게를 다시 느낀다.
>
> 솔직하게 말하자. *TS는 어렵다*. 정확히는, *Java/Kotlin 베테랑에게 어렵다*. 문법이 어려워서가 아니다. *언어 뒤에 깔린 결정의 이유들*이 자기가 알던 결정의 이유들과 정반대이기 때문이다. 점진적 타입은 *왜 모 아니면 도가 아닌가*. 구조적 타입은 *왜 이름이 의미가 없는가*. unsound는 *왜 컴파일러가 거짓말을 허용하는가*. erased는 *왜 런타임에 타입이 없는가*. TC39 정렬은 *왜 자기 마음대로 새 문법을 만들지 못하는가*. 다섯 개 모두, *Java라면 절대 그렇게 안 한다*. 그래서 어렵다.
>
> 그리고 어렵기 때문에, *처음부터 다시 배워야 한다*. *이미 다른 언어를 잘 한다*는 사실은 자존심이 아니라 짐이 되기도 한다. 그 짐을 일단 내려놓고, *처음 배우는 사람*의 자세로 1장을 다시 읽기를 권한다. 이 책 전체가 그 자세 위에서 가장 잘 읽힌다.

## 마무리 — 지도를 손에 들고 2장으로

1장이 약속한 것은 *답*이 아니라 *질문과 지도*였다. 그 약속을 지켰는지 잠깐 돌아보자.

받아 든 첫 번째 질문은 *"TS는 그냥 JS에 타입 붙인 거 아닌가?"*였다. 답의 절반은 *맞다* — 한 줄 정의는 정확히 그렇게 되어 있고, 슈퍼셋이라는 약속도 거짓이 아니다. 답의 나머지 절반은 *틀리다* — *컴파일러*와 *언어 서비스*까지가 TS의 실체이고, 슈퍼셋이라는 말이 *런타임 안전*을 보장하지 않으며, *unsound*와 *erased*라는 두 단어가 Java 직관의 발목을 잡는다. 두 번째 질문 *"왜 처음부터 다시 배워야 하는가?"*에 대한 답은 *다섯 핵심 모델*이라는 다섯 단어 안에 들어 있었다. 점진적 / 구조적 / unsound / erased / TC39 정렬. 다섯 모두 Java/Kotlin과 다르다. 문법은 며칠이면 익는다. 다섯 결정의 *이유*를 손에 익히는 데에는 책 한 권이 필요하다. 그래서 이 책이 있다.

그리고 손에 든 *지도*는 두 가지다. 하나는 *어휘 매핑 열 개* — JVM↔Node, JAR↔npm, Spring DI↔NestJS, `CompletableFuture`↔Promise, sealed↔discriminated union, 그리고 다섯 개의 짝. 더 긴 목록은 부록 A에서 만난다. 다른 하나는 *직무별 추천 경로*다. 백엔드 베테랑이라면 2-3-6-7-8-13-15, 프론트엔드라면 2-3-4-5-12-8-14, 마이그레이션이라면 2-3-9 + 부록 D, CLI나 데스크톱이라면 2-3-10이나 11. 책을 *도구로* 쓰자.

자 이제 2장으로 넘어갈 차례다. 2장은 *타입을 붙이기 전의 자바스크립트*를 들여다본다. 다섯 핵심 모델 중 *왜* 점진적이어야 했고 *왜* unsound여야 했는지 — 그 *왜*들의 절반은 자바스크립트 본성에서 나온다. 10일 만에 만들어진 언어가 어떻게 세상을 먹었는지, 프로토타입 기반 객체 모델이 무엇인지, `this`의 일곱 가지 얼굴이 무엇인지, 단일 스레드 이벤트 루프가 ExecutorService와 무엇이 다른지. 모든 TS 결정의 토양을 한 번 짚고 가자. 그래야 3장에서 다섯 핵심 모델을 본격적으로 펼칠 때, 모델 하나하나가 *공중에 뜨지 않고* 지면에 발을 디딘다.

급하지 말자. 1장의 자리를 잘 잡고 천천히 페이지를 넘기면, 책의 나머지 14장과 4개의 부록이 *각각 자기 자리*를 가진 지도가 되어 펼쳐질 것이다.

> **📖 더 깊이 가려면**
>
> 1장의 주제 — *TypeScript의 한 줄 정의와 다섯 핵심 모델의 호명* — 를 더 깊이 파고 싶다면 다음 자료를 권한다.
>
> - **공식 문서**. TypeScript Handbook의 첫 두 장 *The Basics*와 *Everyday Types*. 영어가 부담스럽다면 velopert(김민준)의 *TypeScript Handbook 한국어판*을 함께 보자. (https://www.typescriptlang.org/docs/handbook/2/basic-types.html , https://typescript-kr.github.io/)
> - **TypeScript Design Goals 원문**. Microsoft TypeScript 위키의 한 페이지. *Goals*와 *Non-goals*가 두 칼럼으로 정리되어 있다. *왜 unsound인가*에 대한 가장 짧고 정직한 답이 여기에 있다. (https://github.com/Microsoft/TypeScript/wiki/TypeScript-Design-Goals)
> - **학술 논문**. Bierman, Abadi, Torgersen, *Understanding TypeScript* (ECOOP 2014). TS 타입 시스템의 *의도된 unsoundness*를 6+ 지점에서 정리한 권위 있는 분석. 이론적 토대를 잡고 싶은 독자에게 강력 추천한다.
> - **한국 학습 자원**. 토스 기술블로그의 *JavaScript에서 TypeScript로 바꾸기* 시리즈가 한국 표준 학습 자료 중 하나다. (https://toss.tech/article/typescript-1) 그리고 도서로는 Dan Vanderkam의 *Effective TypeScript* (한국어판: *이펙티브 타입스크립트*, 인사이트). 1장이 끝나고 2장을 본격적으로 들어가기 전에 한 번 통독해두면 시야가 한 단계 넓어진다.
> - **다음 한 걸음**. 이 책의 2장 *JavaScript의 진짜 본성*과 3장 *TypeScript는 무엇이며, 무엇이 아닌가*. 1장의 모든 *질문*에 대한 답이 두 장에 걸쳐 본격적으로 펼쳐진다.

---

# 2부 — 본성

TypeScript를 진정으로 손에 익히려면 그 토대인 JavaScript의 본성을 먼저 알아야 한다. JavaScript는 1995년 10일 만에 만들어진 언어가 30년을 살아남은 결과물이다. 그 결정들 — 프로토타입 기반 객체 모델, `this`의 동적 결합, 단일 스레드 이벤트 루프, `null`과 `undefined`의 이원성 — 은 TypeScript 안에서도 그대로 살아 숨 쉰다. 2장이 그 토대를 짚고, 3장이 TypeScript가 그 위에 어떤 약속을 얹었는지, 그리고 어떤 약속은 하지 않았는지를 정직하게 밝힌다.

이 부에서 만나는 챕터:
- 2장. JavaScript의 진짜 본성 — 타입을 붙이기 전에 알아야 할 것
- 3장. TypeScript는 무엇이며, 무엇이 아닌가 — 컴파일타임의 환상

---

# 2장. JavaScript의 진짜 본성 — 타입을 붙이기 전에 알아야 할 것

Spring으로 백엔드만 짜다가 처음으로 브라우저 콘솔에 코드를 한 줄 넣어본다고 해보자. 별생각 없이 `[] + []`을 입력하고 엔터를 누른다. 결과는 빈 문자열이다. 이번에는 `[] + {}`를 넣어본다. `"[object Object]"`라는 이상한 문자열이 돌아온다. 자, 한 번 더. `{} + []`. 이번에는 `0`이 나온다. 같은 두 피연산자인데 순서를 바꿨더니 결과의 *타입*이 바뀐다. 이쯤 되면 헛웃음이 난다. *"이게 진짜 프로그래밍 언어가 맞나?"*

마음을 좀 가라앉히고, 솔직히 짚어보자. 이 장난 같은 결과들은 누군가 일부러 만든 농담이 아니다. 1995년 5월의 어느 사무실에서, 한 사람이 10일이라는 시간 안에 만들어낸 언어가 30년이 지난 지금 우리 손까지 흘러왔을 뿐이다. 그 10일짜리 언어가 한두 해가 아니라 30년을 살아남았고, 지금은 지구상에서 *가장 많이 실행되는* 코드의 정체다. 그 사실을 무시한 채 *"농담 같은 언어"*로만 보면, 그 위에 얹은 TypeScript도 끝내 손에 잡히지 않는다.

이 장은 TypeScript를 본격적으로 펴기 전에, 그 토대인 JavaScript의 형태를 먼저 보자는 장이다. 객체는 어떻게 생겼는지, `this`라는 단어 하나가 왜 이렇게 많은 얼굴을 가지는지, 단일 스레드로 어떻게 비동기를 돌리는지, 그리고 빈 값을 표현하는 키워드가 왜 두 개나 있는지. 정적 타입 언어로 잔뼈가 굵은 사람일수록 이 토대를 *대충* 넘기고 싶어진다. *"어차피 TS로 가릴 거 아닌가?"* 하는 마음이 든다. 솔직히 자연스러운 마음이다. 하지만 잠시만 참고 함께 들여다보자. 이 장의 내용을 알지 못하면, 앞으로 모든 함정 박스가 *"왜 이런 일이 생기지?"*에서 멈춘다. 알고 보면, 모든 함정의 뿌리가 이 장 어딘가에 있다.

## JS의 짧은 역사 — 10일이 만든 결정들

JavaScript의 탄생 이야기는 이미 너무 많이 회자되어, 설명이 늘 양극단으로 흐른다. 한쪽은 *"10일 만에 만든 언어가 어떻게 제대로일 수 있겠어"* 식의 가벼운 비웃음이고, 다른 한쪽은 *"그래도 결국 살아남았으니 위대하다"* 식의 낭만화다. 둘 다 우리 작업에는 별 도움이 안 된다. 우리에게 필요한 건 사실관계다. *어떤 환경에서, 어떤 결정이 내려졌고, 그 결정의 그림자가 지금까지 어떻게 드리워져 있는가.* 그 정도다.

1995년, 넷스케이프(Netscape)는 곤란한 상황에 있었다. Mosaic의 후계자로 부상한 이 회사의 브라우저에는 *움직이는 페이지*를 만들 수단이 없었다. 마이크로소프트가 같은 시기 Internet Explorer로 뒤를 쫓아오고 있었고, Sun의 Java는 막 등장한 신예로 모두가 들떠 있었다. 넷스케이프는 *"브라우저 안에서 돌아가는 가벼운 스크립팅 언어"*가 필요하다고 판단했다. 한쪽에서는 Sun의 Java를 페이지 안에 끼워 넣자는 의견이 있었고, 다른 쪽에서는 *"디자이너와 비전공자도 쓸 수 있는 더 가벼운 언어가 필요하다"*는 주장이 있었다. 결과적으로 둘 다 했다. Java는 애플릿 형태로 끼워 넣고, 더 가벼운 스크립팅 언어를 새로 만들기로 했다.

그 새 언어 만들기가 브렌던 아이크(Brendan Eich)에게 떨어졌다. 그에게 주어진 시간은 10일이었다. 정확히는, 10일 안에 *프로토타입을 돌아가게 만들어* 시연할 수 있어야 했다. 게다가 위에서 내려온 비공식적 지시가 두 가지 더 있었다. 첫째, *"Java처럼 보여야 한다."* 마케팅상 그래야 했다. 그래서 문법은 C/Java 계열로 잡았다. 중괄호와 세미콜론, `if/for/while`이 같은 모양이다. 둘째, *"하지만 객체 모델은 더 유연해야 한다."* 아이크 본인은 함수형 언어 Scheme의 팬이었고, 거기에 Self 언어의 *프로토타입 기반 객체 모델*에 매료되어 있었다. 그래서 안쪽 모델은 prototype과 일급 함수로 끌고 갔다.

이 결정이 지금까지 남는다. *겉모습은 Java처럼, 속은 Scheme + Self처럼.* 우리가 `class` 키워드를 보고 *"아, Java처럼 객체지향이구나"* 싶다가 막상 `this`가 사라지는 순간 멘붕에 빠지는 이유가 여기 있다. 겉포장과 내용물이 다른 것이다. 누구의 잘못도 아니다. 1995년의 사정이 그랬다.

10일짜리 시연은 통과되었다. 언어의 이름은 처음에 Mocha, 다음에는 LiveScript, 그리고 같은 해 12월 Sun과의 마케팅 협약을 통해 JavaScript로 굳어졌다. 이 이름이 지금까지도 혼란을 만든다. *"자바스크립트는 자바와 무슨 관계인가요?"* 하는 질문을 해마다 신입 개발자에게 받는다. 답은 *"이름 빼고 거의 없다"*이다. C와 C++이 가족이라면, Java와 JavaScript는 *햄과 햄스터*만큼 멀다.

그 다음에 일어난 일들도 짧게만 짚어두자. 1996년 마이크로소프트가 IE 3에 JScript라는 이름의 호환 언어를 넣었다. 두 진영이 서로 다른 방향으로 확장하기 시작하자, 표준화가 필요해졌다. 그 결과가 1997년의 ECMA-262, 즉 *ECMAScript* 표준이다. 그래서 우리가 *"ES2015"*, *"ES2020"*이라고 부르는 것은 모두 이 ECMA 표준의 판본 번호다. 언어의 공식 이름은 ECMAScript이고, JavaScript는 그 구현체의 마케팅 이름인 셈이다. 다만 이 책에서는 관행대로 둘을 섞어 쓰겠다. 누구도 *"엑마스크립트로 짠다"*고 말하지 않으니까.

표준이 잡힌 뒤로도 한참은 조용했다. 2000년대 초반의 IE 6 시대를 기억하는 사람이라면 알 것이다. 그 무렵의 JS는 *알림창 띄우기*와 *폼 검증* 정도의 역할만 했다. 본격적으로 다시 살아난 건 2004년 Gmail, 2005년 Google Maps가 *"브라우저 안에서 진짜 애플리케이션이 돌아간다"*는 것을 보여준 다음부터다. 곧이어 jQuery가 등장해 브라우저 호환성 지옥을 정리했고, 2009년에는 라이언 달(Ryan Dahl)이 V8 엔진을 서버로 끌어내려 Node.js를 만들었다. 이때부터 JS는 브라우저를 떠나 서버, CLI, 데스크톱, 모바일까지 영토를 넓힌다.

이 *팽창*이 우리에게 의미하는 바는 분명하다. 1995년의 *"브라우저 안에서 잠깐 도는 스크립트"*용으로 내린 결정들이, 지금은 은행의 트랜잭션 코드와 결제 게이트웨이의 한복판을 책임지고 있다는 뜻이다. 그래서 그 결정들의 무게가 처음 10일과는 비교할 수 없을 만큼 커졌다. TypeScript는 바로 이 *팽창된 JS의 무게*를 감당하기 위해 등장한 도구다. 그 사실을 머리에 넣어두면, 앞으로 우리가 만나는 *"왜 이렇게 했지?"*의 답이 늘 같다. *"그때는 그게 합리적이었다. 지금은 그 위에서 살아남아야 한다."* 자, 그러면 본격적으로 그 결정들을 하나씩 들춰보자.

## 프로토타입이라는 진짜 객체 모델

`class` 키워드부터 시작하자. JavaScript의 `class`는 ES2015(ES6)에 들어왔다. 그 전까지는 객체지향 비슷한 것을 짜고 싶으면 `function`과 `prototype`이라는 단어를 직접 굴려야 했다. 자, 그렇다면 `class`가 들어왔으니 이제 Java처럼 클래스 기반 언어가 된 거 아닌가? 그렇다면 이 책이 굳이 prototype을 다룰 필요가 있을까?

답은 단호하게 *"있다"*이다. 이유는 단순하다. **JS의 `class`는 Java의 `class`가 아니다.** 그것은 prototype 위에 *그럴듯한 옷을 입힌* 문법 설탕(syntax sugar)일 뿐이다. 옷을 입혔다고 안쪽이 바뀐 건 아니다. 우리가 `class`로 짠 코드도 결국 prototype 메커니즘 위에서 돈다. 평소에는 그 사실을 잊고 살 수 있다. 하지만 어느 날 갑자기 *"왜 이 메서드가 이 객체에 있지?"*, *"왜 이 인스턴스의 메서드를 다른 객체에 붙여 넣었더니 동작이 다르지?"* 같은 질문 앞에 서면, 결국 prototype을 알아야 답이 나온다.

직접 보자. 다음은 가장 단순한 클래스 정의다.

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, I am ${this.name}`;
  }
}

const dog = new Animal("Rex");
console.log(dog.greet()); // "Hello, I am Rex"
```

여기까지는 누구나 *"Java처럼 생겼군"* 싶다. 하지만 이 객체의 안쪽을 한 번 들여다보자.

```javascript
console.log(Object.keys(dog));        // ["name"]
console.log(dog.greet);               // [Function: greet]
console.log(dog.hasOwnProperty("greet")); // false
console.log(dog.hasOwnProperty("name"));  // true
```

이게 첫 번째 충격이다. `dog`라는 인스턴스가 분명 `greet()`를 호출할 수 있는데, *그 메서드는 인스턴스의 소유물이 아니다.* `name`은 인스턴스의 자기 속성이지만, `greet`는 그렇지 않다. 그렇다면 `greet`는 어디 있는가? 이름이 prototype이라는 별도의 객체에 있다.

```javascript
console.log(Object.getPrototypeOf(dog) === Animal.prototype); // true
console.log(Animal.prototype.greet);   // [Function: greet]
console.log(Animal.prototype.hasOwnProperty("greet")); // true
```

조금 더 직관적인 단서를 주는 코드를 보자.

```javascript
console.log(dog.__proto__);                    // Animal {}
console.log(dog.__proto__ === Animal.prototype); // true
console.log(dog.__proto__.__proto__);          // [Object: null prototype] {}
console.log(dog.__proto__.__proto__.__proto__); // null
```

이 출력이 핵심이다. JavaScript의 모든 객체는 *prototype 체인*이라는 사슬에 매달려 있다. `dog`는 자기 자신을 가지고 있고, 그 위로 `Animal.prototype`이라는 객체를 부모처럼 올려두고, 그 위에는 `Object.prototype`이 있고, 그 위는 `null`이다. 우리가 `dog.greet()`을 호출하면, 자바스크립트 엔진은 다음 순서로 메서드를 찾는다. 먼저 `dog` 자기 자신을 본다. 없다. 그 위 `Animal.prototype`을 본다. 있다. 그것을 호출한다. 즉, *상속처럼 보이는 것이 사실은 프로퍼티 탐색 알고리즘이다.* 

이 차이가 왜 중요할까? 첫째, 메서드가 인스턴스의 소유가 아니므로, 다른 객체에 *떼다 붙일 수 있다*. 이게 곧이어 보게 될 `this` 문제의 뿌리다. 둘째, 클래스를 정의한 *뒤에도* prototype에 메서드를 추가할 수 있다. Java에서는 상상도 못 할 일이다.

```javascript
Animal.prototype.bark = function () {
  return `${this.name} barks!`;
};

console.log(dog.bark()); // "Rex barks!" — 이미 만든 dog에도 갑자기 bark가 생긴다.
```

이걸 *멍키 패칭(monkey patching)*이라 부른다. 들으면 멋있어 보이지만 실제로는 *지저분한 일을 슬쩍 끼워 넣는 행위*에 가깝다. 라이브러리들이 이걸 함부로 쓰면 어떤 일이 벌어질지 상상해보자. 한 라이브러리가 `Array.prototype`에 `last()`를 추가했는데, 다른 라이브러리도 똑같이 `last()`를 추가했다고 해보자. 두 라이브러리 모두를 의존성에 가진 프로젝트에서는, 어느 라이브러리가 *늦게 로드되는지*에 따라 동작이 바뀐다. 그것도 에러 없이 조용히. 끔찍한 일이다. 그래서 현대 JS 커뮤니티는 *"내장 prototype에는 손대지 말자"*는 강한 합의를 가지고 있다. ECMAScript 표준에 새 메서드(`Array.prototype.findLast` 같은 것)를 추가할 때조차, 기존 라이브러리의 prototype 패치와 충돌하지 않도록 *조사를 거친다*. 그만큼 prototype의 자유도는 양날의 검이다.

> ### 📚 Java/Kotlin 시선 박스 ① — 화살표 함수 vs Kotlin 람다
>
> | Kotlin | TypeScript/JavaScript |
> |---|---|
> | `val add = { a: Int, b: Int -> a + b }` | `const add = (a: number, b: number) => a + b;` |
> | `list.map { it * 2 }` | `list.map(x => x * 2)` |
> | `list.forEach { println(it) }` | `list.forEach(x => console.log(x));` |
>
> 표면만 보면 거의 똑같다. 둘 다 일급 함수이고, 둘 다 콜렉션 메서드 인자로 쉽게 넘어간다. 하지만 한 발만 더 들어가면 이야기가 달라진다.
>
> Kotlin의 람다는 그 자체로 *객체*다. 컴파일되면 `Function1`, `Function2` 같은 함수형 인터페이스의 익명 인스턴스가 된다. 람다 안에서 `this`는 *바깥 스코프의 `this`*를 가리키고, `it`은 단일 인자 람다의 약속된 이름이다. 명확하고 예측 가능하다.
>
> JS의 화살표 함수는 표면이 짧다는 점에선 닮았지만, 더 큰 의미는 *바깥의 `this`를 그대로 가져온다(lexical this)*는 데 있다. 일반 `function`으로 쓴 익명 함수와 구별되는 가장 큰 차이가 이것이다. *왜 굳이 이 구별을 만들었나?* 하는 의문은, 다음 절의 `this` 7가지 얼굴을 보고 나면 자연스럽게 풀린다. 한 줄로 미리 말하면, *일반 함수의 `this`가 너무 자주 사라져서, 사라지지 않는 형태가 따로 필요했다*는 것이 답이다.

자, 그러면 그 *사라지는 `this`*를 직접 만나보자.

## `this`의 7가지 얼굴

JavaScript에서 가장 많은 신입 개발자가 좌절하는 단어를 하나만 꼽으라면, 거의 확실히 `this`다. Java/Kotlin에서 `this`는 *현재 인스턴스*다. 끝이다. 그 외 다른 의미는 없다. JavaScript에서 `this`는 *호출되는 방식에 따라 매번 달라진다.* 같은 함수를 다른 방식으로 호출하면 `this`가 다른 것을 가리킨다. 처음 듣는 사람에게는 거의 사기처럼 들리지만, 사실이다. 자, 7가지 얼굴을 하나씩 보자.

### 얼굴 1: 일반 함수 호출

가장 단순한 경우다. 함수를 그냥 호출하면 `this`는 무엇을 가리킬까?

```javascript
function whoAmI() {
  return this;
}

console.log(whoAmI());
// 비엄격 모드: 브라우저면 window, Node.js면 global
// 엄격 모드('use strict'): undefined
```

당황스럽다. *"내 함수는 누구의 메서드도 아닌데 왜 `this`가 있지?"* 하는 질문이 자연스럽다. 1995년의 결정 때문이다. JS는 *모든 함수에 `this`가 있게 만들었다*. 비엄격 모드에서는 그 기본값이 전역 객체(브라우저의 `window`, Node의 `global`)였고, 엄격 모드(2009년 ES5에서 등장)에서는 `undefined`로 강제된다. 현대 코드는 거의 모두 엄격 모드를 쓰니, 그냥 *호출되는 함수의 `this`는 `undefined`*라고 외워두면 된다. 괜찮다. 다음 얼굴들이 훨씬 더 어지럽다.

### 얼굴 2: 메서드 호출

이번엔 그 함수를 객체의 속성으로 두고 호출해보자.

```javascript
const obj = {
  name: "object",
  whoAmI() {
    return this;
  }
};

console.log(obj.whoAmI() === obj); // true
console.log(obj.whoAmI().name);    // "object"
```

이게 우리가 흔히 *"`this`는 자기 객체"*라고 알고 있는 모습이다. 메서드로 호출되면, `this`는 *그 메서드를 호출한 점(.) 앞의 객체*가 된다. 핵심은 *호출의 모양*이지, 함수가 *원래 누구 것인지*가 아니다. 다음 코드를 보자.

```javascript
const method = obj.whoAmI;
console.log(method()); // undefined (엄격 모드)
```

같은 함수다. 같은 `obj.whoAmI`다. 그런데 변수에 *저장*만 하고 `obj.` 없이 호출하면, `this`는 사라진다. 자바 출신 개발자에게 이 사실은 처음에 거의 받아들이기 어렵다. *"메서드 참조를 변수에 저장했는데 자기가 누구 것인지를 잊어버린다고?"* 그렇다. 잊어버린다. 호출 시점에 `obj.` 없이 부르는 순간, 그건 *그냥 함수 호출*이 된다. 메서드 호출이 아니라 일반 함수 호출이 되는 셈이다. 그래서 `this`는 얼굴 1로 돌아간다.

### 얼굴 3: 생성자 호출

`new` 키워드로 호출하면 또 달라진다.

```javascript
function Person(name) {
  this.name = name;
}

const alice = new Person("Alice");
console.log(alice.name); // "Alice"
console.log(alice instanceof Person); // true
```

`new`가 붙으면, 자바스크립트 엔진이 *새 빈 객체*를 만들어서 그것을 `this`로 함수에 넘긴다. 그리고 그 객체의 prototype을 `Person.prototype`으로 연결해 반환한다. 즉, `new`는 *"`this`로 새 객체를 깐다"*는 뜻이다. 이걸 잊고 `new` 없이 `Person("Alice")`라고 호출하면 어떻게 될까? 엄격 모드에서는 `this`가 `undefined`이므로 `this.name = name`에서 즉시 TypeError가 난다. 비엄격 모드에서는 *글로벌 객체에 `name` 속성이 슬쩍 추가되는* 끔찍한 일이 벌어진다. 다행히 ES2015 `class`로 정의된 생성자는 `new` 없이 호출하면 무조건 에러를 던진다. 그런 의미에서 `class`는 *조금 더 안전한 옷*이다.

### 얼굴 4: 화살표 함수 (lexical this)

화살표 함수는 자기 `this`를 갖지 않는다. *바깥 스코프의 `this`를 그대로 본다.*

```javascript
const obj = {
  name: "object",
  arrow: () => this,
  method() {
    return this;
  },
};

console.log(obj.arrow());  // undefined (모듈 스코프), 또는 globalThis
console.log(obj.method()); // obj
```

처음 보는 사람은 *"왜 `arrow()`도 메서드처럼 호출했는데 `this`가 `obj`가 아니지?"*라며 당황한다. 이유는 단순하다. 화살표 함수는 *호출 방식에 따라 `this`가 결정되지 않는다*. 정의된 위치의 바깥 `this`를 *닫아서(closure)* 가지고 있을 뿐이다. 위 예의 `arrow`는 모듈의 최상위에서 정의되었으므로, 그 바깥의 `this`(`undefined` 또는 `globalThis`)를 그대로 쓴다.

이 성질이 콜백에서 빛난다. 다음 패턴을 보자.

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }
  startWithFunction() {
    setInterval(function () {
      this.count++; // this는 undefined → TypeError
      console.log(this.count);
    }, 1000);
  }
  startWithArrow() {
    setInterval(() => {
      this.count++; // this는 Counter 인스턴스 → 잘 됨
      console.log(this.count);
    }, 1000);
  }
}
```

`startWithFunction`은 깨진다. 일반 함수가 콜백으로 들어가는 순간, 그 안의 `this`는 *콜백 호출자(여기서는 setInterval의 내부)*에 의해 결정되는데, 거기엔 우리 인스턴스를 알려줄 길이 없다. 화살표 함수로 바꾸면, `startWithArrow` 메서드의 `this`(즉 Counter 인스턴스)를 그대로 닫아 가져가므로 잘 동작한다. *이 패턴 하나가 화살표 함수의 존재 이유다.* 옛날 JS에서는 `var self = this` 같은 임시 변수에 `this`를 저장해 콜백 안에서 쓰던 관행이 있었다. 화살표 함수는 그 관행을 언어 차원에서 흡수한 것이다.

### 얼굴 5: bind / call / apply

`this`를 *명시적으로 지정해서* 함수를 부르고 싶을 때 쓰는 메서드들이다.

```javascript
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const alice = { name: "Alice" };

console.log(greet.call(alice, "Hi", "!"));   // "Hi, Alice!"
console.log(greet.apply(alice, ["Hi", "!"])); // "Hi, Alice!"

const greetAlice = greet.bind(alice, "Hi");
console.log(greetAlice("!"));  // "Hi, Alice!"
console.log(greetAlice("?"));  // "Hi, Alice?"
```

`call`과 `apply`는 즉시 호출하되 첫 인자로 `this`를 강제한다. 둘의 유일한 차이는 *나머지 인자를 펼쳐서 주는가, 배열로 주는가*다. `bind`는 즉시 호출하지 않고 *`this`가 영구적으로 묶인 새 함수를 돌려준다*. ES5 시절 콜백에 메서드를 넘길 때 `this`를 보존하기 위한 표준 기법이 `bind`였다. 지금은 화살표 함수가 더 흔하지만, `bind`는 여전히 *함수를 부분 적용(partial application)*하는 도구로 살아 있다.

### 얼굴 6: 클래스 메서드와 `this`

`class`로 짠 메서드 안의 `this`는 자연스럽게 인스턴스를 가리킨다. 단, *호출 방식이 메서드 호출일 때만*. 다음 예가 잘 보여준다.

```javascript
class Logger {
  constructor(prefix) {
    this.prefix = prefix;
  }
  log(message) {
    console.log(`${this.prefix}: ${message}`);
  }
}

const logger = new Logger("INFO");
logger.log("hello");                   // "INFO: hello"

const detached = logger.log;
detached("hello");                     // TypeError: Cannot read 'prefix' of undefined

setTimeout(logger.log, 1000, "hello"); // 마찬가지로 TypeError
setTimeout(() => logger.log("hello"), 1000); // 잘 됨
setTimeout(logger.log.bind(logger), 1000, "hello"); // 잘 됨
```

위 코드의 두 번째와 세 번째 줄을 잘 보자. 메서드를 *떼어내는 순간* `this`가 사라진다. 그래서 React 클래스 컴포넌트 시절에는 `this.handleClick = this.handleClick.bind(this)`를 생성자에 도배하던 시기가 있었다. 끔찍하게 번거로웠다. 지금은 *클래스 필드 + 화살표 함수*로 그 보일러플레이트를 줄인다.

```javascript
class Logger {
  constructor(prefix) {
    this.prefix = prefix;
  }
  log = (message) => {
    console.log(`${this.prefix}: ${message}`);
  };
}

const logger = new Logger("INFO");
const detached = logger.log;
detached("hello"); // "INFO: hello" — 잘 동작한다
```

`log`를 *메서드*가 아니라 *값이 화살표 함수인 인스턴스 필드*로 정의했다. 화살표 함수의 `this`는 정의된 위치(`Logger`의 인스턴스)에 묶이므로, 이제는 떼어내도 `this`가 사라지지 않는다. 다만 트레이드오프가 있다. 메서드는 prototype에 한 번만 정의되어 모든 인스턴스가 공유하지만, 클래스 필드 화살표 함수는 *인스턴스마다 별도의 함수 객체*가 만들어진다. 인스턴스가 수만 개 만들어지는 핫패스라면 메모리 차이가 의미 있게 난다. 일반 애플리케이션 코드에서는 무시해도 되는 차이지만, 알고는 있자.

### 얼굴 7: 콜백 안에서의 `this`

마지막 얼굴은 *콜백을 받는 함수가 명시적으로 `this`를 지정해줄 때*다. DOM의 `addEventListener`가 대표적이다.

```javascript
button.addEventListener("click", function (event) {
  console.log(this);          // button 자체
  console.log(event.target);  // button (대부분의 경우)
});

button.addEventListener("click", (event) => {
  console.log(this);          // 바깥 스코프의 this (대개 undefined)
  console.log(event.target);  // button
});
```

DOM은 *전통적 관행*에 따라, 일반 함수 콜백을 받으면 그 안의 `this`로 *이벤트가 발생한 요소*를 넘긴다. 화살표 함수를 쓰면 그 관행은 무시되고 lexical this가 적용된다. *어느 쪽이 옳은가?* 하는 질문은 의미가 없다. *어느 쪽을 의도했는가*가 의미 있는 질문이다. 이벤트 요소가 필요하면 일반 함수 또는 `event.currentTarget`을 쓰고, 외부 컴포넌트의 상태가 필요하면 화살표 함수를 쓴다. *일관된 선택이라면 어느 쪽이든 괜찮다.*

자, 7가지를 다 봤다. 머리가 어지러운가? 자연스러운 반응이다. 그래서 한국 커뮤니티에 가장 자주 올라오는 푸념 중 하나가 *"`this`만 안 만나면 JS는 할 만하다"*는 말이다. 이 사실을 뼈에 새겨두는 데 도움이 될 함정 박스를 하나 두자.

> ### 🚧 함정 박스 — `this`가 사라진다 (커뮤니티 패턴 3)
>
> **증상**
>
> ```javascript
> class UserService {
>   constructor() {
>     this.users = [];
>   }
>   load() {
>     fetch("/api/users")
>       .then(function (res) { return res.json(); })
>       .then(function (data) {
>         this.users = data; // TypeError: Cannot set 'users' of undefined
>       });
>   }
> }
> ```
>
> *Java라면 `this.users = data;`가 당연히 동작한다.* JS에서는 깨진다. 그 깨짐의 정체는 *콜백 함수 안의 `this`가 인스턴스가 아니다*라는 사실이다.
>
> **원인**
>
> `then(function (data) { ... })`의 `function`은 일반 함수다. 일반 함수가 콜백으로 호출되면 그 안의 `this`는 *호출자가 지정한 것* 또는 엄격 모드에서는 `undefined`다. Promise는 콜백을 그냥 호출하므로 `this`는 `undefined`다. *호출 방식에 따라 `this`가 결정된다*는 JS의 본성이 정확히 이 자리에 함정을 만든다.
>
> **처방**
>
> 처방은 셋 중 하나다.
>
> 1. **화살표 함수로 바꿔라.** 가장 단순하고 표준적이다.
>    ```javascript
>    .then((data) => {
>      this.users = data;
>    });
>    ```
> 2. **`bind`로 묶어라.** 콜백을 외부에서 받아온다면 어쩔 수 없을 때.
>    ```javascript
>    .then(handleData.bind(this));
>    ```
> 3. **`self` 임시 변수.** 옛 코드에서 자주 보이는 ES5 시대의 처방. 새 코드에는 가급적 쓰지 말자.
>    ```javascript
>    const self = this;
>    fetch(...).then(function (data) { self.users = data; });
>    ```
>
> 권유는 단순하다. *콜백 안에서 `this`를 쓸 일이 있으면 화살표 함수가 기본*이다. 일반 함수가 필요한 자리(이벤트 요소를 받고 싶은 경우 등)는 명확히 의도된 곳뿐이다.

> ### 📚 Java/Kotlin 시선 박스 ② — `this` 바인딩 vs Java 메서드 참조
>
> Java에서 `list.forEach(System.out::println)`이라고 쓰면, `System.out`은 메서드 참조의 *수신자*로 영구히 묶인다. 그 메서드 참조 객체를 어디로 옮기든, 그게 어떻게 호출되든, *`println`을 호출하는 객체는 항상 `System.out`이다*. 이 묶임은 자바 컴파일러가 보장한다.
>
> JS의 메서드 참조는 그렇지 않다. `const f = obj.method;`는 *`obj`와의 연결이 없는 그냥 함수 참조*다. 그래서 `f()`라고 부르면 `obj`는 사라진다. 자바의 메서드 참조처럼 동작하게 만들고 싶으면 직접 묶어야 한다. `const f = obj.method.bind(obj);` 또는 `const f = (...args) => obj.method(...args);` 같은 식이다.
>
> 이 차이의 뿌리는 결국 *언어 모델*이다. Java에서 메서드는 *클래스의 멤버*이고 메서드 참조는 *수신자가 결합된 함수형 인터페이스 인스턴스*다. JS에서 메서드는 *그냥 객체의 함수형 속성*이고, 함수 자체에는 어떤 객체에도 영구히 묶일 의무가 없다. 한쪽은 강한 결합을 기본으로 잡았고, 다른 쪽은 자유로운 연결을 기본으로 잡았다. 둘 다 그 나름의 일관성이 있다. 어느 쪽이 옳다고 말할 일은 아니다. *각자의 게임 규칙을 알자.*

이제 한 번 숨을 돌리자. `this`의 7가지 얼굴은 한 번에 다 외울 필요가 없다. 다만 *"호출 방식이 `this`를 결정한다"*는 한 문장만 머리에 박아두자. 이 문장 하나가 앞으로 만나는 모든 `this` 관련 함정의 자물쇠 열쇠다.

## 이벤트 루프 — 단일 스레드로 비동기를 돌리는 법

다음 토대는 동시성 모델이다. Java 백엔드 개발자는 동시성 하면 곧장 *스레드*를 떠올린다. `ExecutorService`로 풀을 만들고, `synchronized`로 임계 구역을 보호하고, `CompletableFuture`로 비동기를 잇는다. 멀티 스레드 위에서 자라온 사람의 본능이다.

자바스크립트는 그 본능을 정면으로 거스른다. **JavaScript는 단일 스레드로 돈다.** 메인 스레드 하나가 모든 것을 처리한다. 그런데도 fetch 요청 100개를 동시에 날리고, 그 결과를 모아 화면에 그릴 수 있다. 어떻게 가능한 일일까?

답은 *이벤트 루프*다. 이름부터 들여다보자. 이벤트 루프는 *해야 할 일이 든 큐(queue)를 끊임없이 빙빙 돌면서 하나씩 꺼내 실행하는* 구조다. 한 번에 하나씩 처리한다는 점에서 단일 스레드다. 하지만 *오래 걸리는 작업(I/O, 타이머, 네트워크 등)을 환경에 위임해두고, 결과가 도착하면 큐에 넣어 처리*함으로써 동시성을 흉내 낸다. 이걸 *비동기 단일 스레드 모델*이라고 부른다.

직접 확인해보자.

```javascript
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
```

이 코드의 출력 순서는 무엇일까? *"1, 2, 3, 4 순서대로?"* *"1, 4, 2, 3?"* *"1, 4, 3, 2?"* 정답은 마지막이다. **1, 4, 3, 2**.

왜 그럴까? 이벤트 루프의 큐는 사실 *둘로 나뉘어 있다*. 하나는 **마이크로태스크 큐(microtask queue)**, 다른 하나는 **매크로태스크 큐(macrotask queue)**다. Promise의 콜백은 마이크로태스크에 들어가고, `setTimeout`/`setInterval`/`setImmediate`/I/O 콜백은 매크로태스크에 들어간다. 그리고 이벤트 루프의 규칙은 단순하다.

1. 현재 실행 중인 동기 코드(콜 스택)가 다 비워질 때까지 기다린다.
2. 콜 스택이 비면, *마이크로태스크 큐를 모두 비울 때까지* 하나씩 꺼내 실행한다.
3. 마이크로태스크가 다 처리되면, *매크로태스크 큐에서 하나*만 꺼내 실행한다.
4. 그 매크로태스크가 또 마이크로태스크를 만들었다면, 다음 매크로태스크로 넘어가기 전에 새로 생긴 마이크로태스크들을 또 다 비운다.
5. 1번으로 돌아간다.

이 규칙을 위 코드에 적용해보자. `console.log("1")`이 동기 코드로 즉시 실행된다. 그 다음 `setTimeout`은 콜백을 매크로태스크 큐에 등록만 하고 넘어간다. 그 다음 `Promise.resolve().then`은 콜백을 마이크로태스크 큐에 등록만 하고 넘어간다. 그 다음 `console.log("4")`가 동기로 실행된다. 여기까지 출력은 *1, 4*. 이제 콜 스택이 비었으니, 이벤트 루프는 마이크로태스크 큐를 들여다본다. *3*이 출력된다. 그 다음 매크로태스크 큐로 가서 *2*가 출력된다. 끝.

조금 더 복잡한 경우를 보자.

```javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => {
  console.log("C");
  Promise.resolve().then(() => console.log("D"));
});
setTimeout(() => console.log("E"), 0);
console.log("F");
```

출력은? **A, F, C, D, B, E**.

A, F는 동기다. 그 다음 마이크로태스크 큐에 C가 있으니 C를 꺼낸다. C가 실행되는 도중 새 마이크로태스크 D가 등록된다. *마이크로태스크 큐는 비워질 때까지 계속 처리*되므로, 매크로태스크로 넘어가기 전에 D를 마저 처리한다. 그 다음에야 매크로태스크 큐로 가서 B, 그 다음 E.

이 규칙이 어떤 함의를 갖는지 조금만 음미해보자. **`setTimeout(fn, 0)`은 *지금 당장*이 아니라 *현재 동기 코드와 모든 마이크로태스크가 끝난 다음*에 실행된다.** 그래서 *"지금 잠깐 양보하고 다음 틱에 처리하자"*는 패턴에 종종 쓰인다. 하지만 더 큰 함의는 따로 있다. **마이크로태스크는 매크로태스크를 *굶길 수 있다*.** Promise 안에서 또 Promise를 만들고 그 안에서 또 Promise를 만들면, 마이크로태스크 큐가 영원히 비지 않을 수 있다. 그러면 매크로태스크는 영영 차례가 안 온다. UI가 멈추고, 타이머가 안 도는 *이상한 멈춤*이 발생한다. 이 시나리오는 잘 짠 코드에서는 잘 안 생기지만, 라이브러리가 무한 재귀에 빠졌을 때 가끔 본다.

자, 그러면 *오래 걸리는 작업*은 어떻게 처리할까? 답은 *환경에 위임한다*. 브라우저든 Node.js든, *호스트 환경*은 자바스크립트 엔진(V8 같은) 외에 별도의 스레드를 가지고 있다. fetch 요청, 파일 I/O, 타이머 같은 것은 호스트가 자기 스레드에서 처리한 뒤, 결과 콜백을 큐에 넣는다. 자바스크립트 엔진은 큐에서 꺼내 *자기 단일 스레드*에서 실행한다. 즉, *동시에 일어나는 일은 환경의 몫, 결과를 가지고 무엇을 할지는 JS의 몫*이다. CPU를 많이 쓰는 작업(이미지 변환, 큰 JSON 파싱 등)을 메인 스레드에서 돌리면 *모든 것이 멈춘다*. 그래서 그런 작업은 Web Worker(브라우저)나 Worker Threads(Node)로 보낸다. 이때조차도 메모리 공유는 매우 제한적이다. 데이터는 직렬화해서 보낸다.

> ### 📚 Java/Kotlin 시선 박스 ③ — 이벤트 루프 vs NIO/Reactor
>
> Java 진영에서 비동기를 진지하게 다룬 사람은 `Thread per request` 모델의 한계를 안다. 요청마다 스레드 하나를 잡으면, 동시 요청 수가 스레드 풀의 크기에 묶인다. 그래서 등장한 것이 NIO와 Reactor 패턴이다. *이벤트 루프 한 개가 여러 connection을 다중화*하고, 백엔드 작업은 별도의 워커 풀에서 처리한다. Netty, Vert.x, Project Reactor가 이 위에 서 있다.
>
> 이 모델의 핵심 직관이 정확히 JavaScript의 그것이다. *I/O는 이벤트 루프가 비동기로 처리하고, CPU 작업은 워커가 한다.* 다만 차이가 있다. Java의 Reactor는 *선택지의 하나*다. 전통적 스레드 모델과 공존한다. JS는 *유일한 모델*이다. 다른 길이 없다. 그래서 JS 라이브러리는 *모든 API가 비동기로 설계되어 있다*. 처음부터 끝까지 일관된 모델 위에 서 있다는 점이, JS 비동기의 강점이자 함정이다. 강점은 *예측 가능성*. 함정은 *동기 코드를 무심코 끼워 넣었을 때 모든 것이 멈춘다는 사실*이다.
>
> 한 가지 더 짚어두자. Java의 `CompletableFuture.thenApply`는 *콜백이 어느 스레드에서 실행될지가 모호하다*. `thenApplyAsync`로 명시하지 않으면, 호출 스레드인지 풀의 스레드인지가 상황에 따라 달라진다. JS의 Promise는 그런 모호함이 없다. *모든 콜백은 마이크로태스크 큐를 거쳐 메인 스레드에서 실행된다.* 단순함의 위안이 여기 있다.

## 빈 값이 두 개라는 사실 — null과 undefined

다음 함정으로 가자. Java에서 빈 값은 `null` 하나다. Kotlin에서는 `null`을 표현할 수 있는지를 타입 차원에서 분리(`String?`)했지만, 빈 값 자체는 여전히 `null`이다. JavaScript에는 빈 값이 둘이다. **`null`과 `undefined`.**

처음 들으면 *"왜 두 개나 필요해?"* 하는 의문이 든다. 합리적이다. 사실 둘은 *역사적 사고*에 가깝다. 하지만 30년 넘게 쓰여 온 결과, 두 값은 미묘하게 *다른 의미*를 가지게 되었다. 정리하면 이렇다.

- **`undefined`**: *값이 아직 할당되지 않았다*는 뜻. 변수를 선언만 하고 값을 안 줬을 때, 함수의 인자가 안 들어왔을 때, 객체의 없는 속성에 접근했을 때 모두 `undefined`다. *시스템이 알려주는 빈 값*이라고 생각하자.
- **`null`**: *프로그래머가 의도적으로 빈 값을 넣었다*는 뜻. 일부러 *"여기는 비어 있다"*고 표시하는 값이다.

직접 보자.

```javascript
let a;
console.log(a);                  // undefined — 시스템이 알려주는

const obj = {};
console.log(obj.foo);            // undefined — 없는 속성

function f(x) { console.log(x); }
f();                             // undefined — 안 들어온 인자

let b = null;
console.log(b);                  // null — 프로그래머가 의도적으로
```

문제는 *비교*다. `==`와 `===`가 둘을 다르게 다룬다.

```javascript
null == undefined;   // true  (느슨한 동등 비교)
null === undefined;  // false (엄격한 동등 비교)

null == 0;           // false (0과는 비교 안 함, 명시 규정)
undefined == 0;      // false
null < 1;            // true  (이건 또 0으로 변환된다…)
```

이 규칙을 다 외우려고 하지 말자. 그냥 *`==`은 쓰지 말자*가 답이다. **`===`만 쓰자.** 거의 모든 코드 가이드라인이 동의하는 한 줄 권고다. ESLint의 `eqeqeq` 규칙이 기본으로 켜져 있을 정도다. 단, *예외*가 있다. **`x == null`** 한 표현은 살아남았다. 이것이 *`x`가 `null`이거나 `undefined`이거나*를 한 줄로 검사하는 표준 관용구다. 다른 상황에서는 `===`만 쓰자. 이 규칙 하나로 99%의 비교 함정이 사라진다.

또 짚어둘 것이 있다. JS의 *falsy 값들*이다. `if (x) { ... }` 같은 조건문에서 *false로 평가되는* 값의 목록은 다음과 같다.

- `false`
- `0`, `-0`, `0n`(BigInt 0)
- `""`(빈 문자열)
- `null`
- `undefined`
- `NaN`

이게 끝이다. 나머지는 모두 truthy다. *빈 객체 `{}`도 truthy*, *빈 배열 `[]`도 truthy*다. Java/Kotlin 출신은 여기서 종종 발이 걸린다. *"빈 배열이면 false 아닌가?"* 아니다. 그래서 다음 코드가 의도와 다르게 동작한다.

```javascript
const items = [];
if (items) {
  console.log("뭔가 있다"); // 출력된다 — 빈 배열도 truthy
}
```

원했던 의도는 보통 *"items에 원소가 있으면"*이다. 그러면 `items.length > 0`이라고 명시하자. 이런 명시성은 *번거롭게* 느껴질 수 있지만, *찜찜한 동작*보다는 낫다.

`null`과 `undefined`를 한꺼번에 다루는 현대 JS의 두 연산자도 이 자리에서 짚어두자. ES2020부터 들어온 *옵셔널 체이닝(`?.`)과 nullish 병합(`??`)*이다.

```javascript
const user = { profile: null };

console.log(user?.profile?.name);  // undefined (에러 안 남)
console.log(user?.profile?.name ?? "익명"); // "익명"

// ||와 ??의 차이
console.log(0 || "기본값");  // "기본값" (0이 falsy)
console.log(0 ?? "기본값");  // 0      (0은 nullish가 아님)
console.log("" || "기본값"); // "기본값"
console.log("" ?? "기본값"); // ""
```

`??`는 *`null` 또는 `undefined`일 때만* 오른쪽 값을 사용한다. `||`는 *모든 falsy 값*에 대해 오른쪽을 사용한다. 둘은 비슷해 보이지만 명확히 다르다. *"숫자 0이나 빈 문자열은 유효한 값으로 인정하고 싶을 때"*는 `??`를 쓰자. 이 두 연산자의 등장으로 옛날의 `if (x !== null && x !== undefined && x.profile && x.profile.name)` 같은 길고 추한 검사가 사라졌다. JavaScript 진영에서 *드물게 모두가 환영한 문법 추가*였다.

Kotlin과 비교하면 사고방식이 비슷해진다. Kotlin의 `?.`과 `?:`는 사실상 같은 기능을 한다. 다만 Kotlin은 *타입 시스템 차원에서* `String?`과 `String`을 갈라놓고 강제한다. JS에는 그런 강제가 없다. 그래서 *모든 변수가 잠재적으로 nullable*이다. TypeScript의 `strictNullChecks`가 이 약점을 메우러 들어오는 것이지만, 그 이야기는 4장에서 본격적으로 한다.

## 함수가 일급 시민이라는 사실

이번 절은 짧지만 *"왜 JS 라이브러리는 이렇게 생겼나"*에 대한 답이다. 한 단어로 요약하면, **함수가 일급 시민(first-class citizen)이라는 사실**이다.

일급 시민이라는 말은 거창하지만, 뜻은 단순하다. *함수를 변수에 담을 수 있고, 인자로 넘길 수 있고, 반환값으로 받을 수 있다.* 그게 전부다. Java도 람다와 메서드 참조가 들어온 8 이후로는 *비슷한 일을* 할 수 있다. 다만 Java에서는 *함수형 인터페이스*라는 *옷을 입혀서야* 함수를 1급으로 다룰 수 있다. `Function<T, R>`, `Consumer<T>`, `Supplier<T>` 같은 인터페이스의 인스턴스로 함수를 들고 다닌다. JS에서는 그런 옷이 필요 없다. 함수는 그냥 *함수 객체*다. 어떤 타입이라는 의식 없이 변수에 담는다. *이 차이가 라이브러리 설계를 바꾼다.*

예를 들어, Express의 라우터는 다음처럼 생겼다.

```javascript
app.get("/users/:id", (req, res) => {
  res.json({ id: req.params.id });
});
```

`(req, res) => { ... }`라는 *함수를 그냥 인자로 넘긴다*. Spring의 `@RestController + @GetMapping("/users/{id}")` 모델과 비교하면 인상이 매우 다르다. Spring은 *클래스 안의 메서드*가 라우트의 단위다. *애너테이션이 메타데이터를 만들고, 프레임워크가 그 메타데이터를 읽어 라우팅 테이블을 만든다*. JS/TS에서는 *함수 자체를 라우팅 테이블에 등록*한다. 더 직접적이고 더 가볍다. *어느 쪽이 옳은가?* 양쪽 다 일관성이 있다. 다만 *왜 JS 진영에는 NestJS가 따로 등장해야 했는가*에 대한 답이 여기 있다. 함수 등록 모델만으로는 *큰 백엔드*를 짤 때의 구조가 부족하다고 느낀 사람들이, 데코레이터로 Spring 식 구조를 가져왔다. 그게 NestJS다.

함수형 사고가 라이브러리에 미친 또 하나의 영향을 보자. 데이터 변환을 *체인 메서드*로 잇는다.

```javascript
const result = items
  .filter((x) => x.active)
  .map((x) => x.name)
  .filter((name) => name.length > 0)
  .join(", ");
```

Java도 Stream으로 비슷하게 쓴다. `items.stream().filter(...).map(...).collect(...)`. 다만 JS는 *`stream()`으로 진입하지 않아도* 배열에 직접 메서드 체인을 건다. 자료구조 자체가 함수를 받아들이는 메서드를 풍부하게 가지고 있기 때문이다. `forEach`, `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`, `flatMap`, `sort`, `at`, `findLast` 등. 외울 게 많지만, *공통 패턴*이 있다. *대부분의 인자가 콜백 함수*다. 콜백을 받는 메서드가 풍부하다는 것은, 곧 *조합 가능한 작은 단위들로 변환을 짤 수 있다*는 뜻이다.

이 *조합 가능성*이 JS 라이브러리 생태계의 한 모습이다. lodash가 십수 년 동안 사랑받은 이유, RxJS가 복잡해 보이는데도 살아남은 이유, 최근의 Zod 같은 스키마 라이브러리가 *체이닝 API*로 설계된 이유 모두 이 토대 위에 있다. *함수가 일급이라서 가능한 표현력*이다.

여기서 한 가지만 더 강조해두자. *클로저(closure)*다. 일급 함수는 *자기가 정의된 환경의 변수를 그대로 기억한다*. 그게 클로저다. 다음 예가 가장 깔끔하다.

```javascript
function makeCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    get: () => count,
  };
}

const counter = makeCounter();
counter.increment();
counter.increment();
console.log(counter.get()); // 2
```

`makeCounter`는 이미 반환되어 함수 호출이 끝났다. *그런데도* 그 안의 `count`가 살아 있다. `increment`와 `get`이 그 변수를 *닫아 가지고* 있기 때문이다. Java에서는 final 변수만 람다에 캡처할 수 있고, 캡처된 변수를 외부에서 변경하는 게 어색하다. JS의 클로저는 그런 제약이 없다. 동일한 변수를 *여러 함수가 공유하며 읽고 쓴다*. 이 자유로움이 *모듈 패턴*, *프라이빗 변수의 흉내*, *함수형 프로그래밍의 기반* 모두를 지탱한다. TypeScript로 가면 클로저는 그대로 살아남고, 다만 *그 안에서 캡처된 변수의 타입이 추론된다는 점*이 추가될 뿐이다.

## 짚고 넘어가야 할 작은 함정 모음

본문 줄기를 흐트러뜨리지 않으려고 미뤄둔 *잔잔한 함정*들이 있다. 굵직한 것은 다 봤지만, 잔잔한 것들도 챙겨두자. 한국 커뮤니티에서 *"이걸로 한 번 데였다"*는 후기가 자주 올라오는 자리들이다.

**숫자 타입은 하나뿐이다.** Java는 `int`, `long`, `float`, `double`을 구분한다. JS의 숫자는 모두 `number` 한 가지, 정확히는 IEEE 754 배정밀도 부동소수점이다. 그래서 `0.1 + 0.2 === 0.3`이 `false`다. *고전 중의 고전 함정*이다. 정확한 정수 연산이 필요하면 `BigInt`(접미사 `n`)를 써야 한다. `9007199254740993n + 1n`은 정확히 계산된다.

```javascript
console.log(0.1 + 0.2);              // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3);      // false
console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991
console.log(Number.MAX_SAFE_INTEGER + 2); // 9007199254740992 (틀림)
console.log(9007199254740993n + 1n); // 9007199254740994n (정확)
```

**암묵적 타입 변환이 너무 많이 일어난다.** 이 책 첫머리에서 보았던 `[] + []`, `[] + {}`이 그런 사례다. `+` 연산자는 한쪽이 문자열이면 *모두 문자열로 합치고*, 그렇지 않으면 *모두 숫자로 더한다*. 객체에 `+`가 적용되면 우선 `valueOf()`, 그다음 `toString()`을 시도한다. 그 결과 위 같은 *기괴한 출력*이 나온다. 핵심 처방은 단순하다. **타입을 섞지 말자.** 숫자는 숫자끼리, 문자열은 문자열끼리. 변환이 필요하면 `Number(x)`, `String(x)`로 *명시적으로* 한다. TypeScript는 이 패턴 위반을 컴파일타임에 잡아준다. JS만 쓰던 시절에는 ESLint와 코드 리뷰가 마지막 방어선이었다.

**자동 세미콜론 삽입(ASI).** JavaScript는 세미콜론을 *알아서 끼워 넣어준다*. 하지만 그 규칙이 미묘해서 가끔 사고를 친다. 가장 유명한 사례는 `return`이다.

```javascript
function f() {
  return
  {
    foo: "bar",
  };
}

console.log(f()); // undefined — return 다음 줄이 분리되어 객체는 무시됨
```

*"세미콜론을 안 쓰면 깔끔해 보인다"*는 미적 취향이 있는 사람들도 있지만, 이런 함정 때문에 *세미콜론을 명시적으로 쓰는 진영*과 *ASI를 신뢰하고 안 쓰는 진영*이 갈린다. Prettier 같은 포매터가 자동으로 정리해주므로, 팀이 합의하면 어느 쪽이든 괜찮다. 다만 *섞어 쓰지는 말자*.

**`==`의 함정 한 번 더.** 위에서 *"`==`은 쓰지 말자"*고 했지만, 다시 한 번 강조한다. `[] == false`가 `true`다. `[0] == false`도 `true`다. `[] == ![]`도 `true`다(이건 정말 꿈에 나올 정도로 이상하다). 이 모두가 JS의 *느슨한 동등 비교* 규칙 때문이다. 이런 코드를 만나면 *반드시 의도된 것인지* 의심하자. 거의 모두 *실수*다. ESLint의 `eqeqeq` 규칙을 켜자.

**호이스팅(hoisting).** 변수와 함수가 *코드의 위에서 선언된 것처럼 끌어올려져 처리되는* 현상이다. `var` 선언과 `function` 선언이 호이스팅된다. `let`, `const`도 *선언 자체는* 끌어올려지지만, *값에 접근하는 시점*까지는 *Temporal Dead Zone(TDZ)*이라는 영역에 머문다. 새 코드에서는 `var` 대신 `let/const`를 쓰자. 그러면 호이스팅의 가장 끔찍한 부분(*아직 할당 안 된 값을 참조해도 에러 없이 `undefined`가 되는*)을 피할 수 있다.

```javascript
console.log(x); // undefined (var는 undefined로 초기화됨)
var x = 1;

console.log(y); // ReferenceError (let/const는 TDZ)
let y = 1;
```

이 정도다. 다 외울 필요는 없다. *"이런 게 있다"*는 사실만 머리 어딘가에 박아두자. 어느 날 코드가 *기괴하게* 동작할 때 *"아, 그때 본 그 함정 같은데?"* 하고 떠올릴 수 있으면 충분하다.

## 그래서 이 모든 것이 TypeScript와 무슨 관계인가

여기까지 읽으면서 *"이게 다 JavaScript 이야기인데, TypeScript 책에서 왜 이렇게 길게 다루지?"* 하는 의문이 들었을 수 있다. 그 의문에 정직하게 답해보자.

TypeScript는 *기존 JavaScript 위에 타입 정보를 얹어 컴파일타임에 검사하는* 도구다. 이 한 줄을 풀어보면, **TS가 다루는 모든 것은 결국 JS의 그 형태와 그 결정들이다**. TS가 JavaScript를 *고치지* 않는다. *지우지도* 않는다. 컴파일이 끝나면 타입은 사라지고, 우리가 손에 쥐는 것은 *순수한 JS*다. 그 JS가 가진 모든 본성 — `this`의 동적 결합, prototype 체인, 이벤트 루프, `null`과 `undefined`의 이원성, 암묵적 변환, ASI, `==`의 함정 — 이 그대로 살아 있다.

그래서 TypeScript가 어디서는 *놀랍도록 잘 동작하고*, 어디서는 *이상하게 빈틈이 보인다*. 그 이유의 절반은 *TS의 타입 시스템 설계*에 있지만, 나머지 절반은 *JS의 본성*에 있다. 예를 들어보자.

- TS는 `this`의 타입도 추론한다. 하지만 *호출 방식이 `this`를 결정하는 JS의 본성*은 그대로다. 그래서 *콜백을 떼어내는 자리*에서 TS가 `this: void`로 추론하거나, *바인딩이 풀리는 자리*에서 컴파일러가 경고를 내준다. 알지 못하면 *왜 TS가 여기서 갑자기 까칠하지?* 싶은 자리들이다.
- TS는 `null`과 `undefined`를 별도의 타입으로 다룬다(`strictNullChecks`). 둘이 미묘하게 다른 의미를 가진다는 *JS의 약속*을 *타입 시스템이 강제*하는 것이다. Kotlin에서는 둘 중 하나만 있으니 단순한 일이, JS에서는 *둘이 별도의 타입*이라 추가적인 신경이 필요하다.
- TS의 컴파일된 결과물도 결국 단일 스레드의 이벤트 루프 위에서 돈다. async/await는 Promise 위의 syntax sugar고, Promise는 마이크로태스크 큐 위에서 돈다. *단일 스레드라는 사실은 컴파일이 가려주지 못한다.* 그래서 TS로 짠 백엔드도 무거운 동기 작업이 들어가면 똑같이 멈춘다.
- TS의 타입은 prototype 체인을 *모형화*해서 따라간다. 클래스의 메서드가 prototype에 들어간다는 사실, 인스턴스 필드가 자기 속성에 들어간다는 사실을 TS는 안다. 우리가 모르고 *떼어붙이는* 행동을 하면, TS의 타입과 런타임이 어긋난다. 어긋난 자리는 거의 항상 *런타임 에러*로 나온다.

*"그러면 TS는 결국 무력한 것 아닌가?"* 그렇지 않다. TS는 자신의 한계를 정직히 알고 있는 도구다. 무엇을 잡아주고 무엇을 잡아주지 않는지가 *명시적으로* 설계되어 있다. 그 한계의 윤곽이 정확히 *JS의 본성*과 겹친다. 우리가 이 장에서 본 것들이 *TS의 한계의 정체*인 셈이다. 다음 장에서 본격적으로 다룰 *컴파일타임의 환상*이라는 주제는, 이 장에서 본 JS의 본성을 *TS가 어디까지 가려줄 수 있고, 어디서부터는 가려줄 수 없는가*를 정직하게 묻는 자리다.

그래서 이 장의 결론은 단순하다. **JavaScript를 알지 못하면 TypeScript를 끝내 모를 수밖에 없다.** Java에서 *JVM의 동작*을 모르고 자바를 짤 수 있는 사람과, JVM을 *조금이라도 아는* 사람의 코드 품질이 결국 다르듯이, JS의 본성을 외면한 TS와 그 본성 위에서 만들어진 TS는 결국 다른 결과를 낸다. 자, 그러면 그 본성 위에 *어떤 약속*으로 TypeScript가 얹혀 있는지를 다음 장에서 함께 살펴보자.

## 마무리 — 외면하지 말자

이 장에서 본 것들을 한 번에 머리에 다 넣을 필요는 없다. 다만 다음 다섯 가지만은 *기억해두자*.

1. **JavaScript는 1995년의 결정들을 30년째 짊어지고 있다.** 그 결정들 위에 TypeScript가 얹혀 있다. 그 결정들을 *낭만화하지도, 깎아내리지도* 말고, *있는 그대로* 받아들이자.
2. **`class`는 prototype 위의 옷이다.** 옷이 편리하지만, 안쪽 모델이 prototype이라는 사실은 안 바뀐다. 어느 날 `this`가 사라질 때, 그 사실이 답이 된다.
3. **`this`는 호출 방식에 따라 결정된다.** 7가지 얼굴을 다 외우지 말고, *이 한 문장*만 머리에 박아두자. 콜백 안에서 `this`가 필요하면 화살표 함수를, 메서드를 떼어내야 하면 `bind`를.
4. **단일 스레드 + 이벤트 루프 + 마이크로/매크로 큐.** Promise 콜백은 마이크로태스크다. setTimeout은 매크로태스크다. 동기 코드 → 마이크로 비우기 → 매크로 하나, 다시 처음으로. 이 순환을 머리에 그릴 수 있으면 비동기의 절반은 끝났다.
5. **빈 값은 두 개. 비교는 `===`로.** `null`과 `undefined`는 의미가 다르다. `==`은 쓰지 말자. 한 줄 예외는 `x == null`. `??`와 `?.`을 적극 쓰자.

이 다섯 가지가 앞으로 우리가 만나는 *모든 함정*의 뿌리다. 4장의 narrowing이, 7장의 비동기 함정이, 9장의 점진적 마이그레이션이 모두 이 토대 위에서 설명된다. 이 장이 어렵게 느껴졌다면, 그건 자연스럽다. *정적 타입 위에서 자라온 사람에게 JS의 본성은 처음에는 거의 조롱처럼 느껴진다*. 그 거리감을 부정하지 말자. 다만 *이해하려는 노력*은 결국 보상한다. 다음 장에서 그 보상의 모습을 보자.

자, 이제 TypeScript의 약속을 정면으로 들여다볼 차례다. *"TS는 무엇이며, 무엇이 아닌가."* 컴파일타임이 만드는 환상과 그 환상이 정직히 멈추는 자리를, 다음 장에서 함께 살펴보자.

> ### 📖 더 깊이 가려면
>
> - **MDN Web Docs — JavaScript Reference**: <https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference> — `this`, prototype, 이벤트 루프 모두 한국어로 양질의 설명이 있다. 한국 개발자가 *처음 펼쳐야 할* JS 1차 문서.
> - **You Don't Know JS Yet (2nd ed.)** — Kyle Simpson. <https://github.com/getify/You-Dont-Know-JS> — 무료 공개. *"JS를 안다"*는 자존심을 정직하게 부순다. 특히 *Scope & Closures*와 *this & Object Prototypes* 두 권은 이 장의 내용을 깊이 보충한다.
> - **JavaScript: The Good Parts** — Douglas Crockford (오라일리, 2008). 오래되었지만 *"JS의 좋은 부분만 골라 쓰자"*는 사상 자체가 지금까지 영향을 준다. 이 사상이 곧 TypeScript로 진화하는 흐름의 한 갈래다.
> - **velopert(김민준) — JavaScript 입문서**: <https://velog.io/@velopert> — 한국어 표준 자료의 한 갈래. JS 기초의 한국어 설명을 찾는 첫 자리.
> - **이벤트 루프 시각화 — Loupe**: <http://latentflip.com/loupe/> — Philip Roberts의 JSConf EU 2014 발표 *"What the heck is the event loop anyway?"*와 함께 보자. 14분짜리 영상이 *이벤트 루프란 무엇인가*에 대한 가장 빠른 직관을 준다.

---

> 2장에서 살펴본 JavaScript의 본성 — 프로토타입, `this`의 일곱 얼굴, 이벤트 루프, `null`과 `undefined`의 이원성 — 이 모두 TypeScript 안에 그대로 살아있다. 이제 그 토대 위에 TypeScript가 어떤 약속을 얹었는지, 그리고 어떤 약속은 명시적으로 거부했는지를 들여다볼 차례다.

# 3장. TypeScript는 무엇이며, 무엇이 아닌가 — 컴파일타임의 환상

Spring으로 10년을 짜온 개발자가 TS 프로젝트에 처음 합류한 첫째 주를 상상해보자. 동료가 보내준 PR을 열어보니, 요청 본문 타입이 `interface CreateUserRequest`로 깔끔하게 정의되어 있다. 익숙한 풍경이다. 그런데 그 아래 컨트롤러 코드가 이상하다. `req.body`를 그대로 받아 그 인터페이스 타입에 *맞다고 가정하고* 내부 함수에 넘긴다. `@Valid`도 없고, 어떤 검증 호출도 없다.

*"이거… 그냥 통과돼?"* 동료에게 묻는다. *"네, 컴파일 잘 되고 테스트도 통과해요."*

분명 IDE는 빨간 줄 하나 없다. 빌드도 깔끔하다. 그런데 어딘가 찜찜하다. 익숙한 정적 타입의 안전망이 발 밑에 깔려 있다고 믿었는데, 한 발자국 떼어 보니 그 안전망이 *컴파일이 끝나는 순간 사라진다*는 사실이 어렴풋이 손에 잡힌다. *"그럼 이 타입은 도대체 뭐였지? 런타임에는 어디 있는 거지?"*

질문을 정직하게 받아들여야 한다. 이 챕터는 그 질문 두 개에 답한다. 첫째, **TS의 타입 정보는 런타임에 어디로 가는가?** 둘째, ***"Java처럼 안전하다"*는 직관은 어디서 깨지는가?** 이 두 질문에 손에 잡히는 답을 갖고 나면, TS라는 도구가 *어떤 약속을 하고 어떤 약속은 하지 않는지*가 보인다. 그제야 4장 이후의 모든 도구—추론·좁히기·discriminated union·매핑 타입·branded type—를 *왜 그렇게 생겼는지* 이해하면서 손에 익힐 수 있다.

먼저 1장에서 이름만 호명했던 다섯 핵심 모델을 정면으로 풀어보자. 이 다섯이 책의 *언어 철학적 골격*이다. 여기서부터다.

## 다섯 핵심 모델 — TS의 정체를 한 자리에 모으면

TS를 *언어*로 이해한다는 건 결국 다섯 가지 결정의 묶음을 이해한다는 뜻이다. 점진적 타입(gradual), 구조적 타입(structural), 의도된 unsoundness, type erasure, 그리고 ECMAScript 정렬(TC39 alignment). 이 다섯은 따로 있는 게 아니라, *서로가 서로의 이유*다. 하나가 없으면 다른 넷이 성립하지 않는다.

먼저 다섯을 짧게 펼쳐놓고, 그 다음에 하나씩 깊이 들어가보자.

**(1) 점진적 타입 (gradual typing).** 한 프로그램 안에 *타입이 붙은 코드*와 *타입이 붙지 않은 코드*가 공존할 수 있다. `any`라는 탈출구가 그 다리 역할을 한다. `any`는 어떤 타입과도 양방향으로 호환되며, 그 결과 *기존 JS 코드를 깨지 않고 한 파일씩 점진적으로 TS로 옮겨갈 수 있다*. 이 결정이 없었다면 오늘날의 TS는 없다.

**(2) 구조적 타입 (structural typing).** 두 타입이 호환되는지는 *모양*으로 결정된다. `class Dog implements Animal`이라고 적을 필요가 없다. 멤버가 같으면 같은 타입이다. Java/Kotlin의 명목 타입(nominal)에서 온 사람에게 가장 처음 충격을 주는 자리.

**(3) 의도된 unsoundness.** TS는 *완벽한 타입 안전성을 일부러 포기*했다. 함수 매개변수의 bivariance, `any`의 흡수성, 인덱스 시그니처의 허용 범위, 배열의 공변성 등 학자들이 지목한 6+ 개의 자리에서 *틈*을 의도적으로 남겼다. 이유는 *개발자 생산성과 JS 호환성*. 정합성과 생산성 사이의 균형을 *생산성 쪽으로 기울인* 결정이다.

**(4) 타입 소거 (type erasure).** `tsc`가 끝나면 모든 타입이 사라진다. `interface User`도, `type UserId`도, 제네릭 매개변수도, 전부 다. 결과물은 평범한 JS다. Java erasure가 *제네릭 매개변수만* 지운다면, TS erasure는 *모든 타입을* 지운다.

**(5) ECMAScript 정렬 (TC39 alignment).** TS는 자기만의 길을 가지 않는다. 새 문법은 가능한 한 TC39 표준 진행 단계와 정렬한다. `class`, `async/await`, `decorator`, top-level await — 모두 ECMAScript 표준을 따라간다. *"우리는 JS를 대체하는 언어가 아니라, JS가 잘되도록 돕는 도구다"*가 TS의 자기규정이다.

이 다섯이 한 줄로 합쳐지면 이렇게 된다.

> TypeScript는 JavaScript 위에 *타입 주석과 컴파일러*를 얹은 도구다. 타입은 *컴파일 단계에서만 의미가 있고*, 컴파일이 끝나면 *지워진다*. *모양*으로 호환을 판단하며, *의도적으로 안전성의 일부 틈을 허용*해 *기존 JS 코드와 점진적으로 함께 살 수 있게* 한다. 그리고 자기 마음대로 문법을 만들지 않고 *JS 표준을 따라간다*.

이 한 단락이 이 챕터 전체의 요약이다. 하지만 *요약을 외우는 것*과 *그 요약이 코드에서 어떻게 드러나는지를 손으로 만지는 것*은 다르다. 이제부터 다섯을 하나씩, 코드와 함께, *왜 그래야 했는지의 사연*과 함께 풀어보자. 결이 잡히지 않으면 4장부터의 모든 도구가 *추상적 카탈로그*로만 보이게 된다.

## 컴파일과 런타임 — `tsc`가 끝나면 타입은 어디로 가는가

가장 먼저 손에 잡혀야 하는 건 *컴파일과 런타임의 분리*다. 이게 손에 잡히지 않으면 뒤의 어떤 설명도 공중에 뜬다.

다음 TS 코드를 살펴보자.

```ts
interface User {
  id: number;
  name: string;
  isAdmin: boolean;
}

function greet(user: User): string {
  return `Hello, ${user.name}`;
}

const me: User = { id: 1, name: "Toby", isAdmin: false };
console.log(greet(me));
```

한 눈에 봐도 Java/Kotlin 개발자에게 익숙한 모양이다. `interface`로 데이터 형태를 정의하고, 함수 매개변수에 타입을 주고, 변수 선언에서도 타입을 명시했다.

이걸 `tsc`로 컴파일하면 어떻게 될까? 결과 JS 파일을 보면 이렇다.

```js
function greet(user) {
  return `Hello, ${user.name}`;
}

const me = { id: 1, name: "Toby", isAdmin: false };
console.log(greet(me));
```

깜짝 놀랄 일이 없는, *그냥 JS다*. `interface User`는 어디로 갔을까? 사라졌다. `: User`라는 매개변수 주석도 사라졌다. `: string` 반환 타입도 사라졌다. *모든 타입이 지워진* 평범한 JavaScript만 남았다.

여기서 잠깐 멈추자. Java 개발자에게 이건 충격이다. Java에서 `class User { int id; String name; boolean isAdmin; }`을 컴파일하면 *런타임까지 살아남는* `User.class` 파일이 만들어진다. `instanceof User`로 검사할 수 있고, `getClass().getName()`으로 이름을 꺼낼 수 있고, 리플렉션으로 필드를 순회할 수 있다. 타입은 *런타임의 시민*이다.

TS는 다르다. *런타임에는 타입이 없다*. `instanceof User`도 쓸 수 없다 — 왜냐면 `User`는 컴파일이 끝나는 순간 *존재 자체가 지워졌기* 때문이다. 다음 코드는 컴파일 자체가 안 된다.

```ts
function isUser(value: unknown): value is User {
  return value instanceof User; // ❌ 'User'는 타입이지 값이 아닙니다
}
```

타입이 *값이 아니다*. 이 한 문장이 TS를 다루는 모든 코드에서 매일 마주치는 제약이다. 처음에는 난감하다. 익숙해지기까지 한참 걸린다.

### "JS 위에 얹힌 타입 레이어"의 실제 모양

그래서 TS의 핵심 한 줄은 이렇게 다시 풀린다.

> TS = JS 코드 + *컴파일 시점에만 존재하는* 타입 주석 + 그것을 검사하는 컴파일러 `tsc` + 에디터에 붙어 자동완성·리팩토링·진단을 제공하는 *언어 서비스*.

핵심 단어는 *컴파일 시점에만 존재하는*이다. 영어 약어로는 *erased at compile time*이라 부른다. TS의 타입은 *유령*이다. 개발 중에는 든든히 옆에 있는 듯하지만, 빌드 버튼을 누르고 결과물을 열어보면 거기 없다.

이 모델을 한 번 손에 잡으면, 이후 챕터의 많은 결정이 *왜 그래야 했는지* 자연스럽게 풀린다. 예를 들어:

- *왜 외부 API 응답을 zod 같은 라이브러리로 검증해야 하는가?* — 응답 객체의 *모양*은 컴파일러가 검사할 길이 없기 때문이다. 컴파일이 끝난 런타임에 도착한 JSON은 그냥 객체다. TS의 `interface ApiResponse`는 코드의 *주석*에 불과하지, 런타임에서 *강제하는 누군가*가 아니다.
- *왜 NestJS·TypeORM 같은 프레임워크가 `experimentalDecorators` + `emitDecoratorMetadata`를 켜야 하는가?* — DI를 작동시키려면 *런타임에 타입 정보가 살아남아야* 하기 때문이다. 이 두 옵션을 켜면 컴파일러가 일부 타입 메타데이터를 `reflect-metadata` 라이브러리에 *기록*해 살려두지만, 이는 TS의 *기본 동작이 아닌* 특수 모드다. 기본 모드에서는 모든 타입이 지워진다.
- *왜 Java 개발자가 가장 즐겨 쓰는 `instanceof` 패턴이 TS에서는 절반만 작동하는가?* — `instanceof`는 *클래스*에는 쓸 수 있지만 *인터페이스나 타입 별칭*에는 쓸 수 없기 때문이다. TS에서 `class`로 정의한 것만 런타임 시민으로 남는다. `interface`와 `type`은 안 남는다.

### Java erasure와는 차원이 다른 이유 — *제네릭만 vs 모든 타입*

여기서 똑똑한 Java 개발자라면 즉시 반문한다. *"잠깐. Java에도 type erasure 있잖아? `List<String>`이 런타임에는 그냥 `List`잖아?"*

맞다. Java에도 erasure가 있다. 그런데 *지워지는 범위가 완전히 다르다*. 이 차이를 정확히 짚어두지 않으면, 두 언어를 같은 풍경으로 착각하게 된다.

다음 Java 코드를 살펴보자.

```java
class Box<T> {
    private T value;
    public T get() { return value; }
    public void set(T v) { this.value = v; }
}

Box<String> b = new Box<>();
b.set("hello");
String s = b.get();
```

이걸 컴파일해 `javap -c -p Box.class`로 들여다보면 흥미로운 풍경을 본다.

```
class Box {
  private java.lang.Object value;        // ← T가 Object로 erasure
  public java.lang.Object get();         // ← 반환 타입도 Object
  public void set(java.lang.Object);     // ← 매개변수도 Object
}
```

`T`는 사라지고 `Object`로 환원되었다. 이게 Java erasure다. *제네릭 매개변수만* 지워지고, *나머지 타입은 살아남는다*. 클래스 이름 `Box`도 살아남고, 메서드 이름과 시그니처도 살아남고, `String`이라는 클래스도 살아남는다. 그래서 `b instanceof Box`는 작동한다 (*다만* `b instanceof Box<String>`은 안 된다 — 그게 erasure가 지운 부분이다).

이제 TS의 같은 코드를 보자.

```ts
class Box<T> {
  private value: T | undefined;
  get(): T | undefined { return this.value; }
  set(v: T): void { this.value = v; }
}

const b = new Box<string>();
b.set("hello");
const s = b.get();
```

`tsc`로 컴파일한 결과는 이렇다.

```js
class Box {
  value;
  get() { return this.value; }
  set(v) { this.value = v; }
}

const b = new Box();
b.set("hello");
const s = b.get();
```

여기서 *모든 타입이 지워졌다*. 매개변수의 `: T`도, 반환 타입의 `: T | undefined`도, 변수 선언의 `<string>`도, *전부*. 클래스 본체와 메서드 시그니처는 살아남았지만, 그건 *클래스가 JS의 일급 시민이기 때문*이지 *타입이라서가 아니다*. 만약 같은 코드를 `interface Box<T>`로 정의했다면, 컴파일된 JS에는 *Box라는 단어가 한 글자도 남지 않는다*.

차이를 한 줄로 정리하자.

> Java erasure는 *제네릭 매개변수만* 지운다. 클래스·메서드·타입은 런타임에 살아 있다.
> TS erasure는 *모든 타입을* 지운다. 살아남는 건 JS의 *값*과 *클래스*뿐이다.

이 차이는 단순한 구현 디테일이 아니다. *프로그래밍 모델 전체의 결정*이다. Java의 reflection·dynamic proxy·annotation processor 같은 도구는 *런타임에 타입이 살아있기 때문에* 가능했다. TS에서 같은 일을 하려면 *별도의 부속물*(reflect-metadata, decorator metadata, schema 라이브러리)을 끌어와야 한다. 그 부속물이 없으면 TS의 타입은 *코드 리뷰에서만 사는 유령*이다.

기억해두자. **TS의 타입은 컴파일러와 IDE에서만 일한다. 런타임에는 출근하지 않는다.** 이 한 문장을 머리에 박아두면 4장 이후의 모든 도구가 *왜 그렇게 설계되었는지* 자연스럽게 보이기 시작한다.

> **📚 Java/Kotlin 시선 — `instanceof`의 의미가 다르다**
>
> Java/Kotlin에서 `instanceof`(또는 `is`)는 *모든 명목 타입*에 대해 작동한다. `obj instanceof Animal`이면 `Animal` 인터페이스든 클래스든 상관없이 런타임 검사가 가능하다.
>
> ```java
> // Java
> interface Animal { String name(); }
> class Dog implements Animal { ... }
>
> Object x = new Dog();
> if (x instanceof Animal a) {  // ✅ 인터페이스에도 작동
>     System.out.println(a.name());
> }
> ```
>
> TS에서는 다르다. `instanceof`는 *런타임에 살아남은 클래스*에만 작동한다. `interface`나 `type`에는 못 쓴다.
>
> ```ts
> // TypeScript
> interface Animal { name(): string; }
> class Dog implements Animal {
>   name() { return "Rex"; }
> }
>
> const x: unknown = new Dog();
> if (x instanceof Animal) { /* ❌ 'Animal'은 타입이지 값이 아닙니다 */ }
> if (x instanceof Dog)    { /* ✅ Dog는 클래스라 값으로 살아남음 */ }
> ```
>
> 그래서 TS에서 *interface 모양인지*를 런타임에 검사하려면, 직접 *type predicate* 함수를 쓰거나(`function isAnimal(x): x is Animal`), zod 같은 *런타임 스키마*를 거치거나, *공통 리터럴 필드*로 *discriminated union*을 만들어 `switch`로 갈라야 한다. Java/Kotlin에서 무심코 쓰던 `instanceof`의 자리가 TS에서는 *세 갈래로 흩어진다*. 이 갈래를 손에 익히는 게 4장의 절반이다.

## TS Design Goals — 공식 문서가 직접 말하는 *우리는 무엇을 하지 않는다*

TS가 어떤 도구인지를 알고 싶다면, 가장 좋은 방법은 *TS Design Goals* 원문을 한 번 읽어보는 것이다. Microsoft TS 위키에 공개된 이 문서는 짧지만 결정적이다. 핵심을 옮겨보자.

> **Goals (목표):**
> 1. Statically identify constructs that are likely to be errors. *(에러일 가능성이 높은 구성을 정적으로 식별한다.)*
> 2. Provide a structuring mechanism for larger pieces of code. *(큰 코드 조각을 구조화할 수단을 제공한다.)*
> 3. Impose no runtime overhead on emitted programs. *(컴파일된 프로그램에 런타임 오버헤드를 부과하지 않는다.)*
> 4. Align with current and future ECMAScript proposals. *(현재와 미래의 ECMAScript 제안과 정렬한다.)*
>
> **Non-goals (목표가 아닌 것):**
> - Add or rely on run-time type information. *(런타임 타입 정보를 추가하거나 거기 의존하지 않는다.)*
> - Apply a sound or "provably correct" type system. *(완전무결하거나 "증명 가능하게 옳은" 타입 시스템을 적용하지 않는다.)*

이 문서는 *짧은데 무겁다*. 한 줄 한 줄이 책 한 권의 결정을 압축하고 있다. 함께 읽어보자.

먼저 *목표 3*: *컴파일된 프로그램에 런타임 오버헤드를 부과하지 않는다*. 이게 바로 앞 절에서 우리가 본 *모든 타입이 지워진다*의 공식 근거다. TS는 자기 타입 시스템을 위해 *JS 런타임을 한 줄도 더 무겁게 만들지 않겠다*고 약속했다. 그래서 컴파일된 결과물은 항상 *원본 JS와 거의 같은 크기*다.

다음 *목표 4*: *ECMAScript 제안과 정렬한다*. TS는 자기만의 신박한 문법을 만들 수 있는 권한이 충분히 있는데도, 일부러 *TC39 위원회의 결정에 자기 진화를 묶었다*. `async/await`, optional chaining(`?.`), nullish coalescing(`??`), top-level await, 새 데코레이터 — 전부 *ECMAScript 표준이 먼저, TS가 다음*이다. 자기 야망보다 *생태계의 미래*를 우선한 결정이다. 이게 없었다면 TS는 *JS와 갈라선 별종 언어*가 되었을 것이고, 오늘의 채택률은 절반도 안 됐을 것이다.

그리고 결정적으로, *Non-goal 두 줄*이 이 책의 3장 전체를 정당화한다.

*"런타임 타입 정보를 추가하거나 거기 의존하지 않는다."* — 이건 *type erasure*의 공식 선언이다. *우리는 일부러 타입을 런타임에 안 남긴다*. Java처럼 reflection을 위한 메타데이터를 자동으로 심지 않는다. NestJS·TypeORM이 그걸 끌어 쓰려면 *별도의 옵션과 라이브러리*를 명시적으로 가져와야 한다.

*"완전무결하거나 '증명 가능하게 옳은' 타입 시스템을 적용하지 않는다."* — 이게 바로 *의도된 unsoundness*다. TS는 학자들이 *sound*하다고 부를 수 있는 타입 시스템을 *목표로 삼지 않았다*. 왜? 그게 *생산성과 충돌*하기 때문이다.

이 두 줄을 마음에 새겨두자. TS를 비판하는 글의 90%는 *TS가 약속하지 않은 것을 약속했다고 오해한 데서* 나온다. *"왜 TS는 런타임 안전을 보장 안 해주냐"*는 질문은, 마치 *"왜 망치는 못을 안 빼주냐"*는 질문과 같다. 도구는 *자기가 하기로 한 것*만 한다.

> **💡 작가의 한 마디 — 학계가 부러워한 트레이드오프**
>
> 잠깐 멈춰서 생각해보자. TS의 *Non-goals* 두 줄을, 만약 TS 팀이 거꾸로 적었다면 어떻게 됐을까? *"Add and rely on run-time type information. Apply a sound type system."*
>
> 결과는 끔찍하다. TS는 *기존 JS 코드와 호환되지 않는 별종 언어*가 되었을 것이다. *"우리 회사 JS 코드 5만 줄 중 일부만 TS로 옮기고 싶다"*는 시나리오는 불가능했을 것이다. 모든 타입을 *증명 가능하게* 검사하려면 `any` 같은 탈출구는 못 둔다. `any`가 없으면 점진적 도입은 못 한다. 점진적 도입이 없으면 *시장에 도달*하지 못한다. 시장에 도달 못 하면, 학계가 칭찬해주는 *예쁜 타입 시스템*으로 끝난 채 사장된다. Flow가 그랬고, 그 이전 수많은 타입 첨부 시도들이 그랬다.
>
> 학계의 후속 연구 *Sound Gradual Typing Is Dead?*(Takikawa et al. 2016, POPL)는 이 결정이 *왜 옳았는지*를 정량적으로 보여준다. *sound*와 *gradual*을 동시에 요구하면 *평균 7배, 최악 100배*의 런타임 슬로다운이 발생한다. 즉 *완벽하게 안전한 점진적 타입*은 *현실 성능에서 성립 불가능*하다. TS는 이 사실을 학계가 정량화하기 *2년 먼저*, 직관적으로 알아채고 *실용적 길*을 골랐다.
>
> 그래서 TS의 unsoundness를 *허술함*이 아니라 *겸손함*으로 읽어보자. *"우리는 모든 걸 잡진 못한다. 잡을 수 있는 것을 잡고, 못 잡는 건 솔직히 말하겠다."* 이 자세가 학계와 산업 사이의 다리를 놓았다. TS가 *sound를 포기하지 않았다면*, 우리는 지금 이 책을 쓰지도, 읽지도 않고 있을 것이다. 약속하지 않은 것에 실망하는 대신, *약속한 것을 정확히 받아드는* 자세를 챙겨보자. 그게 도구를 *자기 것으로 만드는* 첫 단계다.

## 점진적 타입 — `any`라는 탈출구가 왜 필요했는가

이제 첫 번째 핵심 모델, *점진적 타입(gradual typing)*을 본격적으로 풀어보자.

상황을 가정해보자. 회사에 5년 묵은 JS 코드 30만 줄이 있다. 매일 사용자 트래픽이 흐르고 있다. 어느 날 결정한다. *"이걸 TS로 옮기자."* Java로 치면 *Groovy 30만 줄을 Kotlin으로 옮기는 일*에 가깝다. 한 번에 다 옮긴다? 그건 *프로덕션을 멈추고 6개월 동안 리팩토링만 하겠다*는 선언이다. 끔찍한 일이다. 어떤 회사도 못 한다.

그래서 *점진적 마이그레이션*이 필요하다. *오늘은 1번 파일만, 내일은 2번 파일도, 한 달 뒤에는 30번 파일까지*. 이게 가능하려면 한 가지 조건이 절대적이다. *타입이 붙은 코드와 붙지 않은 코드가 한 프로그램 안에서 섞여 살 수 있어야 한다*. 이걸 학계 용어로 *gradual typing*이라 부르고, Siek과 Taha가 2006년에 그 이론적 토대를 닦았다.

TS의 답은 한 단어다. **`any`**. `any`는 *어떤 타입과도 양방향으로 호환되는* 특수 타입이다. *타입을 모르겠다, 일단 통과시켜라*라는 명시적 신호다.

```ts
// 타입이 붙은 코드
function double(n: number): number {
  return n * 2;
}

// 타입이 없는(any) 함수 호출 — JS에서 옮겨오는 중인 코드라고 가정
function legacyCompute(): any {
  return JSON.parse('{"value": 42}').value;
}

// 양방향 호환
const x: number = legacyCompute();   // ✅ any → number 통과
const y: any = double(10);           // ✅ number → any 통과
const z: string = legacyCompute();   // ✅ any → string도 통과 (!!)
```

마지막 줄을 보자. `legacyCompute()`는 사실 *number*를 반환하는데, `string` 변수에 담아도 컴파일러가 통과시킨다. *왜?* `legacyCompute`의 반환 타입이 `any`라서, 컴파일러는 *모른다고 인정하고 모든 검사를 면제*한다. 이게 `any`의 *흡수성(absorption)*이다. `any`는 *타입 검사 안에 뚫린 구멍*이다. 일단 들어가면 검사 없이 어디로든 흘러간다.

처음 보면 *왜 이런 위험한 걸 두냐* 싶다. 답은 단순하다. *그게 없으면 TS 도입이 불가능하다*. 5년 묵은 JS 30만 줄에 *모든 함수에 타입을 다 붙이고 시작하라*고 요구하면, *아무도 시작하지 않는다*.

### Bierman et al. (2014)이 정리한 *6+ 지점의 의도된 unsoundness*

`any`는 가장 잘 알려진 *틈*이지만, TS에는 그 외에도 의도적으로 남겨둔 *틈*이 여러 개 있다. Bierman, Abadi, Torgersen 세 사람이 2014년 ECOOP에서 발표한 *Understanding TypeScript* 논문이 이를 *6+ 지점*으로 정리해두었다. 한국 개발자가 이 논문을 직접 읽기는 부담스럽지만, 결론은 손에 잡혀야 한다. 가장 중요한 다섯 가지를 풀어보자.

**(1) `any`의 양방향 호환.** 위에서 본 그대로다. `any`는 모든 타입과 호환되며, 검사를 통과시킨다.

**(2) 함수 매개변수의 bivariance(쌍변성).** 보통 OOP 언어에서 함수 매개변수는 *반공변(contravariant)*이어야 안전하다. 즉 *부모 타입을 받는 함수*는 *자식 타입을 받는 함수의 자리*에 들어갈 수 있어야 한다 (그 반대는 안 된다). TS는 기본 모드에서 *양쪽 다 허용*한다. 즉, *자식 타입을 받는 함수*도 *부모 타입을 받는 함수의 자리*에 들어갈 수 있다. 결과적으로 다음 같은 코드가 통과한다.

```ts
class Animal { name: string = ""; }
class Dog extends Animal { bark(): void { console.log("woof"); } }

type AnimalHandler = (a: Animal) => void;

const dogHandler: (d: Dog) => void = (d) => d.bark();

const handler: AnimalHandler = dogHandler;  // ✅ 통과 (bivariance)
handler(new Animal());  // ❌ 런타임에서 d.bark() 호출 → undefined.bark() 폭발
```

`strictFunctionTypes` 옵션을 켜면 이 동작이 *반공변으로 엄격해진다*. 하지만 *기본 모드에서는 통과한다*. 왜? *DOM API를 비롯한 수많은 기존 JS 라이브러리가 이 패턴에 의존*하기 때문이다. 만약 TS가 처음부터 엄격했다면 *jQuery 코드 한 줄도 통과 못 했을 것이다*.

**(3) 인덱스 시그니처의 허용 범위.** 객체에 동적 키로 접근할 때 TS는 비교적 관대하다. `obj[key]`가 *진짜 존재하는지* 검사하지 않는다. `noUncheckedIndexedAccess` 옵션을 켜기 전까지는 *없는 키도 그냥 접근 통과*시킨다.

**(4) 객체 리터럴의 *excess property check*가 변수에 담기면 사라진다.** 직접 객체 리터럴로 함수에 넘기면 *추가 속성을 잡아주지만*, 변수에 한 번 담아 넘기면 *통과한다*. 구조적 타입의 호환 규칙과 일관성을 유지하기 위한 트레이드오프다.

```ts
type Point = { x: number; y: number };

function plot(p: Point) { /* ... */ }

plot({ x: 1, y: 2, z: 3 });  // ❌ 'z'는 알 수 없는 속성

const p = { x: 1, y: 2, z: 3 };
plot(p);  // ✅ 통과 — 변수에 담기면 z는 무시
```

**(5) 배열의 공변성.** 배열은 *공변(covariant)*으로 설계되었다. 즉 `Dog[]`는 `Animal[]`의 자리에 들어갈 수 있다. 이게 안전한가? *읽기만 하면* 안전하다. *쓰기까지 하면* 깨진다. Java도 같은 자리에서 `ArrayStoreException`을 런타임에 던지는데, TS는 *컴파일러가 잡지 않고 통과시키고 런타임에서도 던지지 않는다* — 그냥 *조용히 잘못된 데이터가 흘러간다*.

이런 자리들을 본 학자들은 처음에는 *"TS는 unsound하다"*라고 비판했다. 그런데 시간이 지나면서 *"unsound하지만 합리적이다"*로 평가가 바뀌었다. 그 전환점이 다음에 다룰 *Sound Gradual Typing Is Dead?* 논문이다.

> **🚧 함정 박스 — 묵시적 any와 strict 모드**
>
> **증상:** 함수를 정의했는데, 타입 주석을 빼먹으면 매개변수가 *조용히 `any`로 추론된다*. IDE에서는 빨간 줄이 없다. 빌드도 통과한다. 그런데 그 함수 안에서 *어떤 메서드든 호출이 다 통과해버린다*. 결국 *런타임에 `undefined.foo() is not a function`이라는 폭발이 난다*.
>
> ```ts
> // 묵시적 any가 일어나는 자리
> function process(user) {            // ← user의 타입이 any로 묵시 추론
>   return user.profile.toUpperCase(); // ← 컴파일러는 통과시킴
> }
>
> process({ name: "toby" });   // 런타임 폭발: profile is undefined
> ```
>
> **원인:** TS는 점진적 타입의 정신을 따라 *기본 모드에서는 묵시적 any를 허용*한다. 옛날 JS 파일을 그대로 떠서 TS로 옮기는 시나리오를 위해서다. 그런데 *처음부터 TS로 짜는 신규 코드*에는 이 관대함이 *함정*이 된다. 타입을 적지 않으면 *검사가 사실상 꺼진* 상태로 일하는 셈이다.
>
> **처방:** 신규 프로젝트는 첫 줄부터 `tsconfig.json`에 `"strict": true`를 켜자. 이 한 줄이 다음 7개를 한꺼번에 켠다 — `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `alwaysStrict`. 가장 중요한 게 첫 번째 `noImplicitAny`다. 이게 켜지면 위 코드는 *컴파일 에러*가 나서 *user의 타입을 명시*하라고 강제한다.
>
> 마이그레이션 중인 레거시 코드는 *strict를 한 번에 다 켜기 어렵다*. 그럴 때는 *파일 단위로 점진적*으로 켜는 패턴이 있다 — 9장 마이그레이션 챕터에서 자세히 다룬다. 신규 프로젝트는 *예외 없이 strict로 시작*하는 편이 낫다. 처음에는 빨간 줄이 많아 짜증나지만, 그 짜증이 *런타임 폭발 한 번*보다 백배 싸다. 잊지 말자.

### Sound Gradual Typing Is Dead? — TS의 unsoundness가 합리적이었던 이유

학계가 한동안 풀고 싶어 한 문제가 있었다. *gradual typing을 sound하게(완전무결하게) 만들 수 있는가?* 이론적으로는 답이 있다. *동적 타입 영역과 정적 타입 영역의 경계마다 런타임 검사를 자동으로 끼워 넣으면* 된다. 즉, *any가 number와 만나는 자리에서 "정말 number야?"를 검사*하면 안전해진다.

문제는 *성능*이다. 검사를 어디에 얼마나 넣어야 할까? 모든 함수 호출 경계? 모든 데이터 접근? 모든 객체 통과 지점?

Takikawa, Greenman, Felleisen 등 여섯 명이 2016년 POPL에서 발표한 *Is Sound Gradual Typing Dead?* 논문이 이 질문을 *정량적으로* 풀었다. Racket 언어로 sound gradual typing 시스템을 구현하고, *부분적으로 타입을 붙인 경우의 모든 조합*을 측정했다. 결론은 충격적이었다.

> *부분적으로 타입을 붙인 코드에서, sound gradual typing은 평균 7배, 최악의 경우 100배의 슬로다운을 일으킨다.*

100배다. *디버그 모드보다도 훨씬 느리다*. 즉, *완벽하게 안전한 점진적 타입*을 *현실 코드*에 적용하면 *프로덕션이 멈춘다*.

이 논문이 발표된 게 2016년이다. TS가 *unsound한 길*을 선택한 게 2012년이다. 즉 TS 팀은 *학계가 4년 뒤에야 정량화한 진실*을 *직관적으로 먼저 알아챘다*. *우리가 sound를 포기한 건 게으름이 아니라 *현실*이다*가 사후적으로 증명되었다.

이 사실을 받아들이면 TS의 *틈*들이 다르게 보인다. 그건 *허술함*이 아니라 *비싼 트레이드오프를 정직하게 받아들인 결과*다. *완벽한 안전*과 *현실의 성능*이 충돌할 때, TS는 *현실을 골랐다*. 그 결과 우리는 오늘 *대규모 JS 코드베이스 위에서 부분적으로라도 타입의 안전망*을 받을 수 있게 되었다.

기억해두자. **TS는 *완벽한 검증자*가 아니라 *합리적인 동반자*다.** 모든 버그를 잡아주지는 않지만, 잡을 수 있는 것은 잡아주고, 못 잡는 것은 *드러내준다*. 이 자세가 손에 잡혀야 4장의 *strict 모드 가족*과 6장의 *branded type*, 그리고 9장의 *마이그레이션 전략*이 *왜 그런 모양인지* 보인다.

> **📚 Java/Kotlin 시선 — 타입 안전성의 약속이 다르다**
>
> Java/Kotlin의 타입 시스템은 *런타임 안전성을 약속*한다. `String s = "hello"`라고 선언했다면, 그 변수는 *런타임에도 String이거나, 아니면 ClassCastException으로 폭발*한다. 사이는 없다.
>
> ```kotlin
> // Kotlin
> val list: List<String> = listOf("a", "b", "c")
> val first: String = list[0]
> // first는 런타임에도 String임을 JVM이 보장
> ```
>
> TS는 다르다. TS의 타입 시스템은 *컴파일 시점의 협상*을 약속할 뿐, 런타임 안전성을 약속하지 않는다.
>
> ```ts
> // TypeScript
> const list: string[] = JSON.parse('["a", 1, true]') as string[];
> const first: string = list[0];
> // first는 number(1)일 수 있다 — 런타임에 .toUpperCase() 호출하면 폭발
> ```
>
> 이 차이를 *결함*으로 받아들이면 TS는 매일 답답한 도구다. *설계*로 받아들이면, *어디에 zod·valibot 같은 런타임 검증을 끼워 넣어야 하는지의 지도*가 손에 잡힌다. 외부에서 들어오는 모든 데이터(API 응답, 사용자 입력, 파일, 환경 변수)는 *경계에서 한 번 검증*해 *내부에서는 타입을 신뢰*하는 패턴 — 이걸 *boundary validation*이라 부른다. 13장 백엔드 챕터에서 본격적으로 다룬다.
>
> Java가 *타입을 강제*한다면, TS는 *타입을 합의*한다. 강제는 단단하지만 비용이 크고, 합의는 가볍지만 깨질 수 있다. 어느 쪽이 우월하다기보다, *서로 다른 트레이드오프*다.

## 구조적 타입 — `type UserId = string`이 그냥 `string`이 되는 첫 충격

다음 핵심 모델, *구조적 타입(structural typing)*으로 넘어가자.

상황을 가정해보자. 토스에서 일하는 백엔드 개발자가, Spring으로 짜던 결제 시스템을 NestJS로 옮긴다. Java에서는 `UserId`와 `OrderId`를 *별도의 클래스*로 분리해 *섞이지 않게* 만들었다. 컴파일러가 *UserId를 OrderId 자리에 못 넣게* 막아준다.

```kotlin
// Kotlin
@JvmInline value class UserId(val value: Long)
@JvmInline value class OrderId(val value: Long)

fun fetchOrder(id: OrderId): Order { ... }

val userId = UserId(123L)
fetchOrder(userId)  // ❌ 컴파일 에러 — UserId is not OrderId
```

든든하다. 이게 *명목 타입(nominal typing)*이다. *이름이 다르면 다른 타입*. 클래스 이름이 *타입 정체성의 핵심*이다.

같은 결정을 TS에서 해보자.

```ts
type UserId = string;
type OrderId = string;

function fetchOrder(id: OrderId): Order { ... }

const userId: UserId = "user-123";
fetchOrder(userId);  // ✅ 통과 — 컴파일 에러 없음
```

Spring 출신 개발자에게 이건 *처음 본 충격*이다. 분명 `UserId`와 `OrderId`라는 *다른 이름*을 줬는데, 컴파일러가 둘을 *구분하지 않는다*. *왜?*

TS는 *구조적 타입(structural typing)* 시스템이기 때문이다. 두 타입의 호환성을 *이름*으로 판단하지 않고 *모양*으로 판단한다. `UserId`도 모양이 `string`이고 `OrderId`도 모양이 `string`이라면, *둘은 같은 타입*이다. `type` 별칭은 *별명일 뿐, 새 타입을 만들지 않는다*.

이건 단순한 디자인 선택이 아니다. *JS의 본성*에서 직접 흘러나온 결정이다. JS는 처음부터 *모양 기반 객체*였다. *덕 타이핑(duck typing)* — *오리처럼 걸으면 오리다*. JS 함수는 *전달된 객체에 어떤 메서드가 있는지*만 보고 동작한다. *그 객체가 어떤 클래스의 인스턴스인지*는 신경 쓰지 않는다. TS의 구조적 타입은 *이 JS 본성을 정직하게 타입 시스템으로 끌어올린* 결과다.

### 구조적 타입의 *부드러움* — 한 자리에서 보이는 풍경

구조적 타입이 어떻게 작동하는지 한 자리에서 보자.

```ts
interface Named {
  name: string;
}

class Dog {
  constructor(public name: string, public breed: string) {}
  bark() { console.log("woof"); }
}

class Robot {
  name: string;
  serial: number;
  constructor(name: string, serial: number) {
    this.name = name;
    this.serial = serial;
  }
}

function greet(thing: Named) {
  console.log(`Hello, ${thing.name}`);
}

greet(new Dog("Rex", "Labrador"));         // ✅ name 있음 → 통과
greet(new Robot("R2D2", 42));               // ✅ name 있음 → 통과
greet({ name: "Plain Object" });            // ✅ name 있음 → 통과
greet({ name: "Toby", age: 30 });           // ✅ name 있음, age는 무시 → 통과
```

`Dog`, `Robot`, *그냥 객체 리터럴* 모두 *`name: string` 멤버를 가졌다는 이유 하나로* `Named` 자리에 들어간다. *어디에도 `implements Named`라고 쓴 적이 없는데도*. 멤버가 더 많아도 (`breed`, `serial`, `age`) 상관없다. *필요한 것이 있으면 통과*다.

이게 *부드러움*이다. Java/Kotlin의 명목 타입에서 온 사람에게 처음에는 *너무 헐겁다*는 인상을 준다. 익숙해지기까지 한참 걸린다.

### 부드러움의 댓가 — *도메인 안전성이 새는* 자리

이 부드러움이 좋기만 한 건 아니다. 다시 토스의 결제 시스템으로 돌아가자. `UserId`와 `OrderId`가 *둘 다 string 모양이라서 컴파일러가 구분 못 한다*는 사실은, *진짜 사고로 이어진다*.

```ts
type UserId = string;
type OrderId = string;

function refund(orderId: OrderId): void { ... }
function getCurrentUserId(): UserId { return "user-789"; }

// 어느 날 졸린 개발자가...
const userId = getCurrentUserId();
refund(userId);  // ✅ 컴파일 통과
                 // 💥 런타임에 "user-789"라는 ID로 환불 처리 시도 → 실제로 다른 사용자 환불
```

*컴파일러는 한 마디도 안 해주고 통과시켰다*. 사용자 ID를 주문 환불 함수에 넘긴 명백한 실수인데도. 이게 *구조적 타입의 헐거움이 도메인 안전성을 새게 만드는* 자리다.

찜찜한가? 찜찜해야 한다. 이게 한국 시니어 개발자가 TS를 만났을 때 가장 먼저 걸리는 *두 번째 함정*이다(첫 번째는 *묵시적 any*).

### 처방 — *branded type*으로 명목 흉내 내기

답은 있다. *모양에 가짜 표식을 하나 더 붙여서* 두 타입을 *구조적으로도 구분되게* 만드는 것. 이게 *branded type* 또는 *nominal trick*이라 부르는 패턴이다. 6장 도메인 모델링에서 본격 풀어내지만, 여기서 맛만 보자.

```ts
type UserId = string & { readonly _brand: unique symbol };
type OrderId = string & { readonly _brand: unique symbol };

function refund(orderId: OrderId): void { ... }
function getCurrentUserId(): UserId { return "user-789" as UserId; }

const userId = getCurrentUserId();
refund(userId);  // ❌ 'UserId' is not assignable to 'OrderId'
```

가짜 `_brand` 속성을 *구조에 끼워 넣어* 두 타입의 *모양이 달라지게* 만들었다. 런타임에는 그냥 string이지만, *컴파일 시점에는 다른 타입*으로 취급된다. 토스, Effect-ts, zod 같은 라이브러리가 이 패턴을 *표준화*했다. Kotlin의 `value class`와 비슷한 자리지만, *강제 메커니즘이 다르다*. Kotlin은 *컴파일러가 자동으로* 구분해주고, TS는 *개발자가 명시적으로 표식을 박아야* 한다.

이 패턴이 손에 익으면, *구조적 타입의 헐거움*을 *도메인의 결*에 맞춰 *봉합*할 수 있다. 헐거운 도구를 *헐겁게 쓰지 않는 법*이다. 6장에서 본격 다룬다.

> **📚 Java/Kotlin 시선 — Java 타입 안전성 vs TS 의도된 unsoundness**
>
> Java의 `record User(long id, String name)`은 *명목 타입*이다. *이름이 User라서 User*이고, *모양이 같은 다른 record*가 있어도 *서로 호환되지 않는다*.
>
> ```java
> // Java
> record User(long id, String name) {}
> record Customer(long id, String name) {}
>
> User u = new User(1, "Toby");
> Customer c = u;  // ❌ 컴파일 에러 — incompatible types
> ```
>
> TS의 `interface`/`type`은 *구조적 타입*이다. *모양이 같으면 같은 타입*이다.
>
> ```ts
> // TypeScript
> interface User { id: number; name: string; }
> interface Customer { id: number; name: string; }
>
> const u: User = { id: 1, name: "Toby" };
> const c: Customer = u;  // ✅ 통과 — 모양이 같아서 호환
> ```
>
> 어느 쪽이 더 좋은가? *상황에 따라 다르다*. 명목 타입은 *도메인 분리에 강하고*, 구조적 타입은 *호환성과 유연성에 강하다*. 외부 데이터를 다루는 자리에서 구조적 타입은 *덕 타이핑의 자연스러운 확장*이다 — JSON 응답이 *내가 정의한 인터페이스 모양*이면 그냥 통과시킬 수 있다. 반면 *비즈니스 도메인의 핵심 식별자*들에는 *branded type*으로 명목성을 흉내 내야 사고를 막는다.
>
> 정답은 *둘을 합치는* 것이다. *외부 경계*에서는 구조적 타입의 부드러움을 활용하고, *도메인 내부*에서는 branded type으로 명목성을 강제하자. Java만 써본 사람은 모든 자리에 *명목성을 갖다 박으려* 하는데, 그러면 TS의 부드러움이 주는 이득을 다 잃는다. *어디에 명목성이 필요한지의 결*을 익히는 게 6장의 핵심 학습 곡선이다.

## ECMAScript 정렬 — TS가 자기 길을 가지 않은 이유

다섯 번째 핵심 모델, *ECMAScript 정렬(TC39 alignment)*을 짧게 짚어두자. 이건 다른 넷에 비해 *언어 디자인의 자세*에 가까운 결정이지만, 그래서 더 중요하다.

TS는 충분히 *자기 마음대로 새 문법을 만들* 수 있는 도구다. 컴파일러를 가지고 있으니, *TS만의 키워드와 연산자*를 추가하고 *컴파일러가 알아서 JS로 풀어주는* 길도 가능했다. 실제로 초기 TS는 그랬다. `enum`, `namespace`, `parameter property`(생성자에서 `public`/`private` 한 줄로 필드 선언), legacy `decorator` — 이런 *TS 고유 문법*이 일부 들어 있다.

그런데 시간이 지나면서 TS 팀은 *방향을 바꿨다*. *우리는 ECMAScript에 합류한다*. 새 기능은 가능한 한 *TC39의 표준 진행 단계와 발맞춰* 들어가고, *TS만 가지는 신박한 문법*은 *피하거나 줄인다*. 그래서 다음과 같은 일이 일어났다.

- `class`, `async/await`, `Promise`, `import/export`, `Proxy`, optional chaining(`?.`), nullish coalescing(`??`), top-level await — *모두 ECMAScript 표준이 먼저, TS는 표준을 따라가는 모드*다.
- *데코레이터*는 TS가 일찍 도입한 `experimentalDecorators`(NestJS·TypeORM이 의존)와 *TC39가 다듬어 표준화한 새 데코레이터*가 따로 있다. TS 5.0이 *새 데코레이터로 hard pivot*을 선언했다 — 자기 길을 *고집하지 않고* 표준 쪽으로 옮겨갔다.
- TS만의 신박한 시도는 점점 *위축*되었다. `namespace`는 사실상 *권장하지 않는 문법*이 되었고, `enum`도 *union literal로 대체하라*는 권고가 정착되었다. *모든 게 ECMAScript 표준에 맞춰가는* 방향이다.

왜 이게 중요한가? *생태계 호환성*이다. TS가 자기 길을 갔다면, *TS 코드와 JS 코드가 점점 멀어졌을 것이다*. 그러면 *기존 JS 코드를 점진적으로 옮기는 시나리오*는 깨졌을 것이고, *TS가 곧 죽을* 위험에 노출됐을 것이다. *호환성을 우선시한 자세*가 결국 TS를 살렸다.

이 자세는 책 후반부에서도 반복적으로 보인다. 9장 마이그레이션에서 *왜 `allowJs`가 가능한지*, 8장 모듈/빌드에서 *왜 ESM이 결국 표준으로 자리잡았는지*, 13장 백엔드에서 *왜 Hono가 Web Standards만으로 모든 런타임에서 도는지* — 전부 *ECMAScript 정렬*이라는 한 자세에서 흘러나온 결과다.

## 컴파일타임 vs 런타임 — `instanceof`, `typeof`, `Array.isArray`로 할 수 있는 것

여기까지 다섯 모델을 다 봤다. 이제 *실무에서 매일 마주칠* 손에 잡히는 질문 하나를 다뤄보자. *런타임에 무엇을 할 수 있고 무엇을 할 수 없는가?*

타입이 다 지워진 다음, 우리에게 남은 *런타임 검사 도구*는 단 셋이다.

**(1) `typeof`** — *원시 타입*만 검사할 수 있다.

```ts
function describe(value: unknown): string {
  if (typeof value === "string") return `문자열: ${value}`;
  if (typeof value === "number") return `숫자: ${value}`;
  if (typeof value === "boolean") return `불리언: ${value}`;
  if (typeof value === "function") return `함수`;
  if (typeof value === "undefined") return `없음`;
  if (typeof value === "object") return `객체 또는 null`;  // ← null도 object!
  return `기타`;
}
```

`typeof`는 *7가지 결과*만 반환한다 — `"string"`, `"number"`, `"bigint"`, `"boolean"`, `"undefined"`, `"object"`, `"function"`, `"symbol"`. *클래스나 인터페이스 이름*은 알 수 없다. 그리고 악명 높은 함정 — `typeof null === "object"`다. JS의 *역사적 버그*인데 *고치면 호환성이 깨져* 그대로 두기로 했다. 잊지 말자.

**(2) `instanceof`** — *클래스로 정의된 타입*만 검사할 수 있다.

```ts
class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function handleError(e: unknown) {
  if (e instanceof HttpError) {
    console.log(`HTTP ${e.status}: ${e.message}`);
  } else if (e instanceof Error) {
    console.log(`일반 에러: ${e.message}`);
  } else {
    console.log(`알 수 없는 throw 값: ${e}`);
  }
}
```

`HttpError`처럼 *클래스로 선언한 것*은 런타임에도 살아남아서 `instanceof`가 작동한다. 하지만 *`interface`나 `type`*으로 정의한 건 안 된다 — 컴파일이 끝나면 사라지기 때문이다.

`instanceof`에는 또 한 가지 함정이 있다. *프레임 경계*(iframe, worker, vm context)를 넘어오면 깨진다. 같은 `Array`인데도 *다른 컨텍스트의 Array*면 `arr instanceof Array`가 `false`가 된다. 그래서 표준 라이브러리는 더 신뢰할 수 있는 검사를 따로 제공한다 — 다음에 볼 `Array.isArray()`가 그 예다.

**(3) `Array.isArray()`, `Number.isFinite()`, 직접 만든 *type predicate*** — 더 정밀한 검사가 필요할 때.

```ts
function processItems(value: unknown) {
  if (Array.isArray(value)) {
    // 여기서 value는 any[] (또는 unknown[])로 좁혀진다
    value.forEach((item) => console.log(item));
  }
}

// 직접 만드는 type predicate
function isUser(value: unknown): value is { id: number; name: string } {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value && typeof (value as any).id === "number" &&
    "name" in value && typeof (value as any).name === "string"
  );
}

const data: unknown = JSON.parse('...');
if (isUser(data)) {
  console.log(data.name);  // ✅ data가 좁혀짐
}
```

`isUser` 함수의 반환 타입에 적힌 `value is { ... }`가 핵심이다. 이게 TS 컴파일러에게 *"이 함수가 true를 반환하면, value의 타입은 이 모양이다"*라고 *약속*하는 신호다. 4장에서 *user-defined type predicate*로 본격 다룬다.

이 셋이 우리에게 주어진 *런타임 도구의 전부*다. 그리고 이것만으로는 *복잡한 외부 데이터의 모양*을 검사하기 충분치 않다. 그래서 zod·valibot 같은 *런타임 스키마 라이브러리*가 등장했다. *컴파일러가 못 봐주는 자리*를 *런타임 검증으로 메우는* 패턴 — 6장과 13장에서 표준 처방으로 다룬다.

기억해두자. **TS의 컴파일타임은 부드럽고 똑똑하지만, 런타임에는 무력해진다. 그 경계를 어디에 그을지가 *설계*다.** 이 한 문장이 4장부터의 모든 도구가 *왜 그렇게 생겼는지*의 답이다.

## 마무리 — 우리는 무엇을 손에 쥐었는가

여기까지 왔다면 손에 쥔 게 하나 있다. *TS는 무엇이고, 무엇이 아닌가*에 대한 정직한 지도다.

다섯 핵심 모델을 다시 한번 한 자리에 모아보자. 외우려 하지 말고, *왜 그렇게 되었는지의 사연*과 함께 떠올려보자.

- **점진적 타입 (gradual)** — 타입이 붙은 코드와 붙지 않은 코드가 *함께 살 수 있게*. `any`라는 탈출구가 그 다리다. 이게 없으면 *기존 JS 30만 줄을 옮기는* 시나리오는 불가능했다.
- **구조적 타입 (structural)** — 호환을 *모양*으로 판단한다. JS의 덕 타이핑 본성을 정직하게 타입 시스템으로 끌어올린 결과. *부드럽지만 도메인 안전성은 새기 쉬워*, *branded type*으로 봉합한다.
- **의도된 unsoundness** — 학자들이 *6+ 지점*으로 정리한 의도적 *틈*. `any`의 흡수성, 함수 매개변수의 bivariance, 인덱스 시그니처의 관대함, 배열의 공변성. *완벽한 안전*과 *현실의 성능* 사이에서 *현실*을 골랐다. *Sound Gradual Typing Is Dead?* 논문이 그 결정의 합리성을 사후적으로 정량화했다.
- **타입 소거 (type erasure)** — `tsc`가 끝나면 *모든 타입이 사라진다*. Java erasure가 *제네릭만* 지운다면, TS erasure는 *전부 다* 지운다. 그래서 런타임 검증은 *별도의 도구*가 필요하다.
- **ECMAScript 정렬 (TC39)** — TS는 자기 길을 가지 않는다. 새 문법은 *TC39 표준 진행*과 정렬한다. *호환성*이라는 자세가 결국 TS를 살렸다.

이 다섯이 뼈대다. 4장부터의 모든 도구는 *이 뼈대 위에서 작동*한다. 4장의 *strict 모드 가족*은 *unsoundness의 일부 틈을 메우는 옵션*이다. 4장의 *type predicate*는 *런타임에 살아있는 셋(typeof, instanceof, isArray)을 컴파일타임 좁히기와 잇는* 다리다. 5장의 *제네릭과 conditional, infer*는 *타입이 타입을 만드는* 도구로, *type erasure의 한계 위에서도 표현력을 뽑아내는* 곡예다. 6장의 *branded type, discriminated union, immutability*는 *구조적 타입의 헐거움을 도메인의 결로 봉합*하는 패턴들이다.

3장이 *언어 철학적 골격*이라 했던 이유가 여기 있다. 4·5·6장이 *전술*이라면, 3장은 *전략*이다. 전략을 손에 쥐지 않고 전술을 외우면, 그건 *이유 없는 카탈로그*다. 같은 도구를 *왜 어떤 상황에 쓰는지*의 결을 모른다.

또 한 가지 가져갈 것. **TS를 *비판할 때*도, *옹호할 때*도, *그것이 무엇을 약속했는지*에서 출발하자.** *"왜 TS는 런타임 안전을 보장 안 해주냐"*는 비판은, TS가 *Non-goals*에 적어둔 *애초에 약속하지 않은 것*에 대한 실망이다. *"TS만 쓰면 모든 버그가 사라진다"*는 옹호도 같은 종류의 오해다. TS는 *합리적인 동반자*이지, *완벽한 검증자*가 아니다. 그 자리를 *zod·valibot·테스트 코드·코드 리뷰·관측 도구*가 함께 채운다.

다음 4장에서는 *이 뼈대 위에서 타입을 도구로 손에 익히는* 단계로 들어간다. *TS의 적극적인 추론, narrowing의 다섯 가지 도구, discriminated union과 `never`로 만드는 exhaustiveness, utility 타입 8개, strict 모드 가족*을 본격적으로 풀어낸다. Java의 `var`보다 훨씬 적극적인 추론이 *왜 그렇게 작동하는지*, Kotlin sealed class의 자리를 TS가 *어떻게 다른 결로 채우는지*가 손에 잡힐 것이다. *첫 "오, 이게 표현되는구나"의 쾌감*이 4장에 있다.

5장은 *타입이 타입을 만드는* 단계다. 제네릭·conditional·infer·매핑·템플릿 리터럴 — 한국 시니어가 *"Kotlin sealed class를 다뤄봤지만 TS에 이런 표현력이 있을 줄은 몰랐다"*라고 인정하는 자리. zod·Hono·Prisma·tRPC의 *현실 코드의 타입 마법*이 부품 단위로 분해된다.

6장은 *도메인 모델링*. 구조적 타입의 부드러움을 *도메인의 결*에 맞춰 *봉합*하는 표준 패턴들. branded type, discriminated union, immutability, *에러를 도메인의 일부로* 다루는 자세. checked exception 정신구조에서 온 사람이 TS의 throw·Result·Effect를 어떻게 받아들일지를 정직하게 푼다.

3장에서 잡은 골격이, 4·5·6장에서 *살이 붙는다*. 한 번에 익히려 하지 말자. *돌아오면서, 다시 보면서, 손에 익혀가자*. 그게 언어를 자기 도구로 만드는 길이다.

> **📖 더 깊이 가려면**
>
> - **TypeScript Design Goals** — Microsoft TS Wiki. https://github.com/Microsoft/TypeScript/wiki/TypeScript-Design-Goals — 이 챕터의 1차 자료. 영어 한 페이지 분량이라 직접 읽는 편이 낫다.
> - **TypeScript Handbook — The Basics & Type Compatibility** — https://www.typescriptlang.org/docs/handbook/2/basic-types.html — 구조적 타입의 표준 설명.
> - **Bierman, Abadi, Torgersen (2014) — *Understanding TypeScript*** — ECOOP 2014. *6+ 지점의 의도된 unsoundness*를 학술적으로 정리. PDF는 검색하면 무료로 구할 수 있다.
> - **Takikawa et al. (2016) — *Is Sound Gradual Typing Dead?*** — POPL 2016. *sound + gradual = 7~100배 슬로다운*을 정량화한 논문. 학회 발표 영상이 ACM Digital Library에 있다.
> - **Daniel Rosenwasser — TypeScript 5.0 Release Notes** — https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/ — 새 데코레이터로의 *hard pivot* 결정 발표. ECMAScript 정렬 자세를 가장 잘 보여주는 글.
> - **velopert(김민준) — TypeScript Handbook 한국어판** — https://typescript-kr.github.io/ — 영문 핸드북을 처음 한국어로 정독하는 데 가장 안정적인 길.
> - **토스 기술블로그 — JavaScript에서 TypeScript로 바꾸기** — https://toss.tech/article/typescript-1 — 한국 현장에서 *점진적 타입의 실전*이 어떻게 적용되었는지를 본 시리즈.
> - **이펙티브 타입스크립트** (Dan Vanderkam, 인사이트 번역) — *구조적 타입과 의도된 unsoundness*에 대한 챕터들이 이 책 3장의 자매 자료다.

---

# 3부 — 무기

골격을 알았으니 이제 도구를 손에 익힐 차례다. 3부는 TypeScript의 타입 시스템이 제공하는 실용적 무기들을 한 장씩 꺼내 두드린다. 4장에서 추론과 좁히기와 exhaustive 검사를 익히고, 5장에서는 타입이 타입을 만드는 마법의 부품들을 분해한다. 6장에서 구조적 타입의 헐거움을 도메인의 결에 맞춰 봉합하는 패턴들을 쌓고, 7장에서 비동기 모델의 전모를 Java/Kotlin과 나란히 놓는다. 8장은 빌드 생태계의 분열을 역사적 이유에서 읽고, 그 위에서 의도적인 선택을 내리는 법을 안내한다.

이 부에서 만나는 챕터:
- 4장. 타입을 손에 익히기 — 추론·좁히기·exhaustive를 도구로
- 5장. 타입을 만드는 타입 — 제네릭·conditional·infer·매핑·템플릿 리터럴
- 6장. 이 도메인을 어떻게 모델링할까 — 구조적 타입 위에서 잃지 않는 법
- 7장. 비동기 모델 — Promise·async/await·Observable·AsyncIterator
- 8장. 빌드 도구가 왜 이렇게 많은가 — 모듈·패키지·번들러·런타임의 분열

---


> 3장에서 TypeScript의 다섯 핵심 모델 — 점진적·구조적·unsound·erased·TC39 정렬 — 이 손에 잡혔다. 이제 그 뼈대 위에서 타입을 실제 도구로 쓰는 단계로 들어가자. 컴파일러가 어디까지 추론해주는지, 어떻게 좁혀가는지, 분기를 빠짐없이 다뤘는지를 어떻게 보장하는지 — 4장에서 그 도구들을 직접 두드려보자.

# 4장. 타입을 손에 익히기 — 추론·좁히기·exhaustive를 도구로

이런 상황을 한번 떠올려보자. 우리는 TS 프로젝트에 갓 합류해서 첫 PR을 낸다. 함수 안에서 `unknown` 값을 다루면서 익숙한 대로 `as User`로 캐스팅했다. 컴파일도 통과하고 동작도 잘 한다. 그런데 리뷰어가 한 줄을 단다. *"여기 `as` 대신 `in` 연산자로 좁혀주세요."*

낯설다. Java라면 `instanceof User`로 끝났을 일이다. Kotlin이라면 `when`이 알아서 분기를 막아준다. TS는 왜 굳이 `in`이라는 자바스크립트 연산자를 동원하는가? 그리고 그 한 줄이 정말로 우리 코드의 안전성을 끌어올리는가?

3장에서 우리는 *"타입은 컴파일타임의 환상이고 런타임에는 사라진다"*는 차가운 진실을 받아들였다. 그렇다면 그 환상이 만들어내는 *실용적 도구들*은 어디까지 뻗어 있을까? 추론은 어디서 멈추고, 좁히기는 어디까지 똑똑하며, 분기는 어떻게 빠짐없이 막을 수 있을까? 4장은 그 도구들을 손에 들고 *직접 두드려보는* 자리다. 처음에는 어색해도, 한두 번 두드리고 나면 *"오, 이게 이렇게까지 표현되는구나"* 하는 작은 쾌감이 따라온다. 그 쾌감을 챕터의 동력으로 삼아 보자.

## 추론은 어디까지 알아주는가

먼저 가장 기본적인 도구, 타입 추론부터 시작하자. Java 11에서 `var`가 들어왔을 때 우리는 어색해하면서도 *"드디어 우리도 타입을 안 적어도 되는구나"* 하고 안도했다. Kotlin은 처음부터 `val`/`var`로 추론을 적극 활용한다. TS도 비슷해 보인다. 변수에 값을 할당하면 알아서 타입이 잡힌다.

```typescript
let count = 10;        // number로 추론
let name = "Toby";     // string으로 추론
let scores = [90, 85]; // number[]로 추론
```

여기까지는 Java `var`와 거의 같다. 그런데 한 줄 더 적어보자.

```typescript
const greeting = "hello"; // 타입은 number? string? — 답은 "hello"
```

`const`로 선언하면 추론된 타입이 단순한 `string`이 아니라 **리터럴 타입** `"hello"`다. 즉 *그 정확한 문자열만* 들어갈 수 있는 타입으로 좁아진다. Java에서는 상상하기 어려운 좁힘이다. Java의 `final String greeting = "hello";`도 변수의 *값*은 고정되지만, *타입*은 여전히 `String`이다. TS는 변경 불가능성과 추론을 엮어, 더 좁은 타입을 만들어 낸다.

이게 별 차이가 아닌 것 같다면, 다음 예를 보자.

```typescript
function move(direction: "up" | "down" | "left" | "right") {
  // ...
}

let dir = "up";
move(dir); // 에러: string은 "up" | "down" | ... 에 들어갈 수 없다

const dir2 = "up";
move(dir2); // 통과 — dir2의 타입이 "up"이라 union의 한 멤버에 정확히 맞는다
```

`let`으로 잡으면 타입이 `string`으로 *넓혀지고*(widening), `const`로 잡으면 *좁혀진다*. Java로는 떠올리기 힘든 결정이다. *"왜 이렇게 만들었을까?"* 답은 단순하다. 변수의 가변성을 그대로 타입에 반영하는 게 *실용적이기 때문*이다. 어차피 다시 대입할 수 있는 값이라면 `string`으로 두는 편이 낫고, 다시 대입 못 할 값이라면 그 정확한 리터럴이 더 정보가 많다.

> 📚 **Java/Kotlin 시선 박스 ① — Java `var` ↔ TS 추론**
>
> Java 11의 `var`는 *지역 변수에 한해* 우변의 정적 타입을 받아쓴다. `var name = "Toby";`라고 적으면 `name`의 타입은 무조건 `String`이다. 더 좁아지지 않는다. 함수 매개변수, 필드, 반환 타입에는 `var`를 쓸 수 없다.
>
> TS의 추론은 더 멀리 간다. (1) 변수의 가변성(`let` vs `const`)에 따라 *리터럴 타입까지* 좁힌다. (2) 함수의 *반환 타입*도 본문에서 추론한다. (3) 콜백에 들어가는 함수의 *매개변수 타입*도 문맥(contextual typing)으로 추론한다. 즉 `arr.map(x => x * 2)`에서 `x`의 타입은 명시 없이도 잡힌다.
>
> 트레이드오프도 있다. TS의 추론이 너무 적극적이라 *원하지 않는 타입으로 추론되는* 경우가 생긴다. Java처럼 명시적 선언을 강제하지 않으니 IDE가 추론을 잘못하면 사람이 알아채야 한다. 익숙해지기 전까지는 함수의 반환 타입만큼은 명시하는 편이 안전하다.

### 문맥이 추론을 도와준다

함수의 매개변수 타입이 *호출 위치의 문맥*에서 결정되는 일도 자주 있다. 이걸 contextual typing이라 부른다.

```typescript
const numbers = [1, 2, 3];
numbers.map(n => n * 2);
//          ^ n의 타입은 number — 명시 없이도 잡힌다
```

`Array<number>`의 `map`이 받는 콜백 시그니처가 `(value: number) => U`이기 때문에, `n`의 타입은 `map`이 호출되는 그 자리의 문맥으로부터 흘러 들어온다. Java에서는 `stream.map((Integer n) -> n * 2)`처럼 명시하거나, 아니면 그저 람다 매개변수로 두고 끝내야 한다. TS는 그 *유추의 흐름*이 한 단계 더 깊다.

물론 한계도 있다. 함수를 *분리해 따로 정의*하면 문맥이 끊긴다.

```typescript
const double = n => n * 2; // n은 implicit any — strict 모드에서 에러
numbers.map(double);
```

함수가 호출 위치에서 떨어지는 순간 문맥이 사라지므로, 매개변수에 타입을 명시하거나 함수 자체에 타입을 주어야 한다. 추론은 강력하지만 *전능하지는 않다*. 어디까지 알아주는지 감을 잡고, 그 너머에서는 손으로 도와주는 편이 낫다.

### `as const`로 추론을 *얼리기*

리터럴 좁히기를 더 적극적으로 활용하고 싶을 때가 있다. 객체 안의 값까지 전부 리터럴로 잡고 싶다고 해보자.

```typescript
const config = {
  host: "localhost",
  port: 3000,
  protocol: "http",
};
// 추론 결과: { host: string; port: number; protocol: string }
```

각 값이 `string`/`number`로 *넓혀져* 있다. 만약 `protocol`이 정확히 `"http"`라는 사실을 타입에 보존하고 싶다면 `as const`를 붙인다.

```typescript
const config = {
  host: "localhost",
  port: 3000,
  protocol: "http",
} as const;
// 추론 결과: { readonly host: "localhost"; readonly port: 3000; readonly protocol: "http" }
```

객체 전체가 깊이 readonly가 되고, 값은 전부 리터럴로 *얼려진다*. 이 패턴은 의외로 자주 쓴다. 라우팅 테이블, 권한 키 목록, 상태 머신의 상태 집합 등 *값이 곧 타입의 일부인* 자리에 잘 어울린다.

### `satisfies` — 검증은 받되 좁힘은 잃지 않기

여기서 TS 4.9에 들어온 신선한 도구 하나를 만나야 한다. 바로 `satisfies` 연산자다. Java에도 Kotlin에도 없는 자리라, 처음 보면 *"이건 또 뭔가"* 싶다. 천천히 풀어 보자.

상황을 가정해 보자. 우리는 색상 팔레트를 정의하고 싶다. 키는 미리 정해진 색 이름들 중 하나이고, 값은 RGB 배열이거나 해시 문자열이다. 이렇게 적었다고 해 보자.

```typescript
type Color = "red" | "green" | "blue";
type RGB = readonly [number, number, number];

const palette: Record<Color, string | RGB> = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
};

palette.red.toUpperCase(); // 에러? 통과? — 통과한다. 그러나 런타임에 폭발한다
```

문제가 보이는가? `palette: Record<Color, string | RGB>`로 *주석을 박는 순간*, 컴파일러는 모든 값이 `string | RGB`라는 사실만 안다. *각 키가 어떤 구체 타입인지*는 잊어버린다. 그래서 `palette.red`가 실은 `RGB`인데도 `string | RGB`로 보이고, `.toUpperCase()`가 `string`의 메서드라 통과해 버린다. *런타임에 가서야 폭발한다.* 난감하다.

그렇다고 주석을 빼면? 이번엔 *키가 `Color`의 멤버인지* 검증을 받지 못한다. 오타를 쳐서 `redd: ...`라고 적어도 컴파일러가 잡아주지 못한다.

이 *둘 다 갖고 싶다*는 욕심에 응답한 게 `satisfies`다.

```typescript
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
} satisfies Record<Color, string | RGB>;

palette.red.toUpperCase();  // 에러 — palette.red는 number[]이지 string이 아니다
palette.red[0];             // 통과 — number
palette.green.toUpperCase(); // 통과 — string
```

`satisfies`는 *"이 객체가 저 타입을 만족하는지 검증해 달라. 단, 변수의 추론된 타입은 객체의 *구체 모양 그대로* 둬라"*고 컴파일러에게 부탁한다. 검증은 받되, 좁힘은 잃지 않는다. 이 한 줄짜리 욕심이 TS 4.9가 풀고 싶었던 문제다.

`satisfies`는 작은 도구지만 한번 익히면 자주 손이 간다. 라우팅 테이블의 핸들러 타입을 검증하면서 각 라우트의 응답 타입은 그대로 유지하고 싶을 때, 환경 변수 객체의 키가 정해진 집합인지 검사하면서 각 값의 정확한 리터럴은 보존하고 싶을 때, 모두 같은 패턴이다. 기억해두자. **타입 주석은 검증과 좁힘을 *맞바꾼다*. `satisfies`는 그 맞바꿈을 *피하게* 해 준다.**

> 💡 **작가의 한 마디 — 주석이냐 `satisfies`냐**
>
> 익숙해지면 손가락이 자동으로 결정한다. *값을 보존하고 싶다면 `satisfies`*. *값보다 인터페이스 계약이 중요하다면 그냥 `: Type`*. 함수 시그니처는 거의 항상 후자, 설정 객체와 룩업 테이블은 거의 항상 전자다. 처음 한 달은 의식적으로 둘을 골라 써 보면, 어느 자리에 어느 도구가 어울리는지 감이 잡힌다.

## strict 모드 — 안전망을 켜고 들어가기

타입 추론이 적극적이라는 말은 *추론된 타입을 사람이 신뢰해도 좋다*는 뜻과 같다. 그런데 그 신뢰는 컴파일러가 *까다롭게 검사할 때만* 성립한다. 매개변수 타입을 못 알아내면 `any`로 슬쩍 넘어가는 컴파일러를 신뢰할 수는 없다. 그래서 TS에는 `strict` 모드가 있다.

`tsconfig.json`에 한 줄 적자.

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

이 한 줄이 켜는 검사가 여러 개다. 그중 셋이 특히 핵심이다.

**`noImplicitAny`** — 매개변수나 변수의 타입을 추론할 수 없을 때 *조용히 `any`로 두지 말고* 에러를 내라. 이게 꺼져 있으면 위에서 본 `const double = n => n * 2;` 같은 코드가 통과해 버린다. `n`이 `any`니까 무슨 짓이든 할 수 있고, 무슨 버그든 들어올 수 있다. 끔찍한 일이다.

**`strictNullChecks`** — `null`과 `undefined`를 *모든 타입에 묻혀 다니는 그림자*로 두지 말고 명시적 멤버로 다뤄라. Kotlin의 `null safety`와 의미가 거의 같다. `string`은 `null`이 들어갈 수 없고, `null`을 허용하려면 `string | null`이라고 *적어야* 한다. 이게 꺼져 있으면 `null` 참조 오류가 컴파일 단에서 새 나간다. Java로 넘어온 사람이라면 NPE의 악몽이 떠올라 등이 서늘해질 자리다.

**`strictFunctionTypes`** — 함수 매개변수의 변성(variance)을 *제대로* 검사하라. 끄면 매개변수가 bivariant로 동작해 안전하지 않은 대입이 통과한다. 자세한 내용은 이 장 마지막 절에서 다시 풀자. 일단 *기본으로 켜는 게 좋다*는 정도로 기억해두자.

세 옵션은 `strict: true` 한 줄로 한 번에 켜진다. 한국 커뮤니티에서 *"PR 받자마자 strict 켜라"*는 말이 회자되는 데에는 이유가 있다. strict 없이 자란 코드는 시간이 지날수록 `any`가 곳곳에 박혀서 *나중에 켜기가 더 힘들다*. 신규 프로젝트라면 첫날부터 켜고 시작하자. 기존 프로젝트라면 9장의 점진 마이그레이션 패턴을 활용하면 된다.

> 📖 더 깊이 들어가는 옵션들은 *부록 B. tsconfig 옵션 사전*에 정리해 두었다. Matt Pocock의 "TSConfig Cheat Sheet"가 매우 좋은 출발점이다 — `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`처럼 strict에는 안 들어가지만 *켜면 한 단계 더 안전해지는* 옵션을 잘 정리해 두었다.

## 좁히기 — 컴파일러와 함께 추리하기

이제 4장의 핵심 절로 들어가자. 타입 좁히기, 즉 narrowing이다.

상황을 하나 가정하자. 어떤 함수가 `string | number`를 받는다. 우리는 그 안에서 *문자열일 때만* 길이를 출력하고 싶다.

```typescript
function printLength(value: string | number) {
  console.log(value.length); // 에러 — number에는 length가 없다
}
```

당연히 안 된다. `value`가 *둘 중 하나*라는 사실만 알 뿐, 실제로 어느 쪽인지 모르는 상태다. 어떻게 좁힐까? Java라면 `if (value instanceof String)`을 적었을 것이다. TS에서도 비슷하지만 *`typeof`*를 쓴다.

```typescript
function printLength(value: string | number) {
  if (typeof value === "string") {
    console.log(value.length); // 통과 — value는 이 블록 안에서 string으로 좁혀졌다
  } else {
    console.log(value.toFixed(2)); // value는 number로 좁혀졌다
  }
}
```

`typeof`는 자바스크립트의 런타임 연산자다. 여기에 TS 컴파일러가 *흐름 분석*을 얹어, `if` 블록 안에서 변수의 타입을 *정확히* 좁힌다. Java 14의 패턴 매칭 instanceof와 정신적으로 비슷하지만, TS는 더 일찍부터 더 적극적으로 이 일을 해 왔다. 이 *컴파일러와 함께 하는 추리*가 좁히기의 본질이다.

좁히기에 쓰이는 도구는 여럿이다. 하나씩 살펴보자.

### `typeof` — 원시 타입을 식별

`typeof`는 자바스크립트의 원시 타입 7가지(`"string"`, `"number"`, `"bigint"`, `"boolean"`, `"symbol"`, `"undefined"`, `"object"`, `"function"`) 중 하나를 반환한다. union의 멤버가 *원시 타입*일 때 가장 자주 쓴다.

```typescript
function format(input: string | number | boolean) {
  if (typeof input === "boolean") return input ? "yes" : "no";
  if (typeof input === "number") return input.toFixed(2);
  return input.toUpperCase(); // 여기에서 input은 string으로 좁혀졌다
}
```

위 코드에서 마지막 `return` 시점에 `input`이 `string`으로 좁혀진 것에 주목하자. 앞에서 `boolean`과 `number`를 *쳐냈으니* 남은 가능성은 `string` 하나다. 컴파일러가 이 흐름을 따라간다. 이 *흐름 기반 좁히기*(control flow narrowing)는 이 장에서 우리가 만나는 모든 도구의 공통 기반이다.

### `instanceof` — 클래스 인스턴스를 식별

class 인스턴스를 다룰 때는 Java와 똑같이 `instanceof`를 쓴다.

```typescript
class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function handle(err: Error | HttpError) {
  if (err instanceof HttpError) {
    console.log(err.status); // 통과 — HttpError로 좁혀졌다
  } else {
    console.log(err.message); // 통과 — 그냥 Error
  }
}
```

여기까지는 Java와 거의 같아 보인다. 하지만 *주의해야 한다*. TS는 구조적 타입 시스템이라 `instanceof`로 좁힌 결과가 우리 직관과 다를 수 있고, 무엇보다 *interface로 정의된 타입*에는 `instanceof`를 쓸 수 없다. interface는 컴파일타임에만 존재하니까. 이때 등장하는 게 다음 도구다.

### `in` — 멤버의 *존재*로 식별

interface로 정의된 두 타입을 갈라야 한다고 해 보자.

```typescript
interface Cat { meow(): void; }
interface Dog { bark(): void; }

function speak(animal: Cat | Dog) {
  if ("meow" in animal) {
    animal.meow(); // Cat으로 좁혀졌다
  } else {
    animal.bark(); // Dog로 좁혀졌다
  }
}
```

`in`은 자바스크립트에서 *객체에 그 키가 있는지*를 묻는 연산자다. TS는 이 검사를 타입 좁히기로 활용한다. interface로 정의된 *모양*만 다른 두 타입을 가르는 가장 직관적인 도구다. Java라면 두 타입을 공통 부모 인터페이스로 묶거나 `instanceof`를 동원해야 했을 자리에서, TS는 *멤버의 존재* 하나로 가른다. 이게 구조적 타입 시스템의 *재미*다.

### equality narrowing — 값으로 좁히기

`===`와 `!==`도 좁히기에 쓰인다. union의 멤버가 *리터럴 타입*일 때 특히 강력하다.

```typescript
function move(direction: "up" | "down" | "left" | "right") {
  if (direction === "up") {
    // direction은 "up"으로 좁혀졌다
  } else {
    // direction은 "down" | "left" | "right"로 좁혀졌다
  }
}
```

이 좁힘은 다음 절의 분별 유니온에서 *주연*으로 등장한다.

### type predicate — 사용자 정의 좁힘

표준 도구로는 좁히지 못하는 자리가 있다. 예컨대 *런타임에 객체의 모양을 검사하는* 사용자 정의 함수의 결과를 좁힘에 활용하고 싶을 때다. 이때 쓰는 게 type predicate다. 함수의 반환 타입에 `arg is Type` 형태의 *predicate*를 적는다.

```typescript
interface User {
  id: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "email" in value &&
    typeof (value as any).id === "string" &&
    typeof (value as any).email === "string"
  );
}

function greet(input: unknown) {
  if (isUser(input)) {
    console.log(`Hello, ${input.email}`); // input은 User로 좁혀졌다
  }
}
```

`isUser`가 `true`를 반환하면, 호출 위치에서 `input`의 타입이 `User`로 좁혀진다. *컴파일러는 함수 본문이 진짜로 그 검사를 제대로 하는지 확인하지 않는다* — 우리가 *약속*한 것이다. 그래서 type predicate는 *조심해 작성해야* 한다. 검사가 부실하면 거짓 약속이 되고, 그 거짓 약속은 런타임에 폭발한다. 찜찜한 자리지만, *경계(boundary)*에서 외부 데이터를 받아들일 때 꼭 필요한 도구다.

> 🚧 **함정 박스 — `as` 대신 `is`로 가는 길**
>
> Java에서 넘어온 사람의 첫 본능은 `as User`다. *"아 그냥 캐스팅하면 되잖아"*. 그런데 TS의 `as`는 *컴파일러를 속이는* 행위에 가깝다. 검증 없이 *그렇다고 우기는* 것이고, 우긴 게 사실이 아니면 런타임에 폭발한다.
>
> type predicate는 *우김을 검증으로 바꾸는* 도구다. `as User` 대신 `if (isUser(value))`로 들어가면, (1) 검증 로직이 한 곳에 모이고, (2) 컴파일러가 좁힘을 보장하고, (3) 호출 측은 `as` 없이 안전하게 멤버에 접근한다. 신규 코드를 쓸 때 `as`가 손에 잡히면, *type predicate로 바꿀 수 있는지* 한 번만 더 생각해보자. 거의 모든 자리에서 가능하다.
>
> 그래도 `as`가 정말 필요한 자리도 있다. 5장에서 그 *세 가지 자리*를 정리한다.

> 📚 **Java/Kotlin 시선 박스 ② — Kotlin smart cast ↔ TS narrowing**
>
> Kotlin의 smart cast는 TS narrowing의 직계 친척이다. `if (animal is Cat) { animal.meow() }`에서 `animal`이 `Cat`으로 자동 캐스팅되는 그 장면, TS의 `if (animal instanceof Cat)`과 거의 같다.
>
> 차이는 두 가지다. 첫째, **검사 도구가 더 다양하다.** Kotlin은 `is`/`!is` 중심이지만, TS는 `typeof`, `instanceof`, `in`, `===`, type predicate를 모두 좁힘에 활용한다. interface처럼 *런타임에 존재하지 않는* 타입까지 가를 수 있는 건 `in`과 type predicate 덕분이다.
>
> 둘째, **재할당의 영향이 다르다.** Kotlin에서는 `var`로 선언된 변수를 다른 스레드가 변경할 수 있다는 가정 때문에 smart cast가 막히는 경우가 있다. TS는 단일 스레드 모델이라 변수 재할당만 하지 않으면 좁힘이 유지된다. 다만 *클로저로 변수를 캡처해 비동기로 호출*하면 좁힘이 풀린다는 점은 양쪽 모두 비슷한 함정이다.
>
> 결론은 같다. 캐스팅 대신 *검사*로 좁히고, 좁혀진 변수를 *그 블록 안에서만* 신뢰하자.

## 분별 유니온과 `never` — Kotlin sealed의 TS식 표현

이제 4장의 *진짜 재미*가 시작된다. Kotlin 개발자라면 sealed class에 익숙할 것이다.

```kotlin
sealed class Shape
data class Circle(val radius: Double) : Shape()
data class Square(val side: Double) : Shape()
data class Triangle(val base: Double, val height: Double) : Shape()

fun area(shape: Shape): Double = when (shape) {
    is Circle -> Math.PI * shape.radius * shape.radius
    is Square -> shape.side * shape.side
    is Triangle -> 0.5 * shape.base * shape.height
} // when이 exhaustive — Triangle을 빼먹으면 컴파일 에러
```

세 가지가 이 한 묶음의 마법이다. 첫째, *대안의 집합이 닫혀 있다*(sealed). 둘째, *각 분기에서 자동 캐스팅*된다(smart cast). 셋째, *분기가 빠짐없이 다뤄졌는지를 컴파일러가 보장한다*(exhaustive).

TS에는 sealed class가 없다. 그렇다면 같은 보장을 어떻게 받아낼까? 답이 **분별 유니온(discriminated union)**이다.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius * shape.radius;
    case "square":
      return shape.side * shape.side;
    case "triangle":
      return 0.5 * shape.base * shape.height;
  }
}
```

각 멤버가 공통 리터럴 필드(`kind`)를 가지고, 그 필드의 *값*이 다른 멤버끼리 다르다. 이 필드를 **discriminant**(분별자)라고 부른다. `switch (shape.kind)`로 분기하면, 각 `case` 블록 안에서 `shape`이 해당 모양으로 *자동으로 좁혀진다*. Kotlin의 `is` smart cast와 정신은 같지만, TS는 *값의 같음*으로 좁힌다(equality narrowing).

여기까지는 좋다. 그런데 *exhaustive*는? 위 코드에서 만약 새로운 모양 `Pentagon`을 추가하고 area 함수를 까먹으면 어떻게 될까? *컴파일이 그냥 통과한다.* 함수의 반환 타입이 명시되지 않았다면 `undefined`가 흘러나오고, 명시되어 있다면 *반환이 누락된* 에러가 어디선가 한 줄 뜰지도 모른다. 찜찜하다.

이 자리에 등장하는 게 `never` 타입과 *exhaustiveness check* 패턴이다.

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(x)}`);
}

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius * shape.radius;
    case "square":
      return shape.side * shape.side;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    default:
      return assertNever(shape); // shape이 never가 아니면 컴파일 에러
  }
}
```

`default` 분기에서 `assertNever(shape)`를 호출한다. 이 함수의 매개변수 타입은 `never`다. *모든 `case`를 다뤘다면* 컴파일러는 `default`에 도달한 시점의 `shape`을 `never`로 좁힌다 — 더 이상 가능한 값이 없으니까. `never`는 `never`에 *대입할 수 있으므로* 컴파일 통과.

만약 새 모양 `Pentagon`을 추가하고 `case "pentagon"`을 빼먹는다면? 컴파일러는 `default` 분기에서 `shape`이 `{ kind: "pentagon"; ... }`으로 좁아진 상태임을 알아챈다. 그건 `never`가 아니다. 따라서 `assertNever(shape)`에 *컴파일 에러*가 뜬다. **컴파일러가 우리 대신 빠짐없이 분기했는지 확인해 준다.** Kotlin `when`의 exhaustive와 *동일한 효과*를 다른 도구로 얻은 것이다.

이걸 처음 두드려보면 *"오, 이게 표현되는구나"* 하는 그 감탄이 나온다. 도메인의 *닫힌 대안 집합*을 union 리터럴로 표현하고, 그 위에 `assertNever`를 세워 두면, 새 멤버를 추가했을 때 *고쳐야 할 모든 자리*를 컴파일러가 알려준다. 리팩토링이 두려울 때 가장 든든한 도구다.

> 📚 **Java/Kotlin 시선 박스 ③ — Kotlin sealed/`when` ↔ discriminated union/`switch`**
>
> 정신은 같지만 도구가 다르다. 한 번 표로 정리해두자.
>
> | 측면 | Kotlin | TypeScript |
> |---|---|---|
> | 대안 집합 정의 | `sealed class` + 서브타입 | `type X = A \| B \| C` (union) |
> | 분별 메커니즘 | 클래스 신원 (`is Circle`) | 공통 리터럴 필드 (`kind: "circle"`) |
> | 분기 문법 | `when` 식 | `switch` 문 (또는 `if`/`else if` 체인) |
> | 자동 캐스팅 | smart cast | flow-based narrowing |
> | exhaustive 보장 | `when`이 식이면 자동 | `assertNever(x: never)` 패턴 |
>
> 결정적 차이는 마지막 줄이다. Kotlin은 `when`이 *식*으로 쓰일 때 컴파일러가 알아서 exhaustive를 검사한다. TS는 `assertNever`라는 *작은 안전망 함수*를 사람이 한 번 만들고, `default` 분기에서 호출한다. 한 번만 만들어 두면 프로젝트 전체에서 재사용 가능하다.
>
> 또 하나, **TS의 분별 유니온은 클래스가 필요 없다.** 그저 객체의 *모양*만 정의하면 된다. JSON으로 직렬화/역직렬화도 자연스럽다. 외부에서 들어오는 메시지(예: WebSocket 이벤트, 큐 메시지)를 모델링할 때 sealed class보다 *훨씬 가볍다*는 점은 분명한 장점이다.

### 한 발 더 — 응답 타입 모델링

분별 유니온이 가장 빛나는 자리는 *상태가 분기되는 응답*이다. 가령 비동기 데이터 로딩 상태를 모델링한다고 해 보자.

```typescript
type LoadState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function render<T>(state: LoadState<T>) {
  switch (state.status) {
    case "idle":
      return "(아직 시작 안 함)";
    case "loading":
      return "로딩 중...";
    case "success":
      return `데이터: ${JSON.stringify(state.data)}`;
    case "error":
      return `에러: ${state.error.message}`;
  }
}
```

여기서 `success`일 때만 `data`가 있고, `error`일 때만 `error`가 있다. 잘못된 조합이 *타입 단에서* 차단된다. *"로딩 중인데 데이터가 있다"*는 비논리적인 상태가 아예 표현 불가능해진다. **표현 불가능한 상태를 표현 불가능하게 만든다** — Yaron Minsky의 그 유명한 격언이 분별 유니온의 정신을 한 줄로 요약한다. Kotlin sealed class도 같은 정신이지만, TS는 그걸 *문법 없이 union 하나로* 표현한다. 가볍고, 충분히 강력하다.

## 유틸리티 타입 — 카탈로그가 아니라 *패턴*으로

분별 유니온까지 익혔으니, 이제 도메인 타입을 *재료*로 새 타입을 *조립하는* 도구를 만나자. TS에는 표준 유틸리티 타입이 30개쯤 들어 있다. 외울 필요는 없다. 자주 쓰는 8개의 *언제 쓰는가*만 손에 익히면, 나머지는 그때그때 검색하면 된다. 표로 던지지 말고 *상황별로* 풀어보자.

### `Partial<T>` — 부분 업데이트의 친구

REST API의 `PATCH` 핸들러를 떠올려 보자. 사용자의 일부 필드만 받아 업데이트한다. *전체 User 모양은 필요 없고, 일부만 들어온다.* 이때 쓰는 게 `Partial<T>`다.

```typescript
interface User {
  id: string;
  email: string;
  name: string;
  age: number;
}

function updateUser(id: string, patch: Partial<User>) {
  // patch는 { email?: string; name?: string; age?: number; ... }
}

updateUser("u-1", { name: "Toby" }); // 통과
```

`Partial<User>`는 모든 필드를 *옵셔널*로 만든다. PATCH·폼 부분 입력·설정 객체의 디폴트 병합 등 *완전하지 않은 모양을 다루는 자리*에 가장 자주 쓴다. 한 가지 주의할 점. `Partial`은 한 단계만 파고든다. 깊이 nested된 객체까지 옵셔널로 만들고 싶다면 `DeepPartial<T>` 같은 재귀 헬퍼를 직접 만들거나 라이브러리(예: `type-fest`)를 가져와야 한다.

### `Required<T>` — 옵셔널을 필수로 되돌리기

반대 방향도 있다. 외부에서 받은 옵셔널 투성이 객체를 *내부에서는 모든 필드가 채워진* 상태로 다루고 싶을 때다.

```typescript
interface Config {
  host?: string;
  port?: number;
  timeout?: number;
}

function applyDefaults(input: Config): Required<Config> {
  return {
    host: input.host ?? "localhost",
    port: input.port ?? 3000,
    timeout: input.timeout ?? 5000,
  };
}
```

함수 *경계*에서는 옵셔널을 받되, 내부에서는 *모든 값이 보장된* 타입으로 좁혀 다루는 패턴이다. Java의 빌더 패턴 끝에서 `build()` 호출 후 모든 필드가 채워진다는 *그 보장*을 타입으로 표현한 셈이다.

### `Readonly<T>` — 변경 금지 표지판

객체를 *읽기 전용*으로 만들고 싶을 때 쓴다.

```typescript
interface Point { x: number; y: number; }

const origin: Readonly<Point> = { x: 0, y: 0 };
origin.x = 10; // 에러
```

주의해두자. `Readonly`는 *컴파일타임* 보장이다. 런타임에는 여전히 변경 가능하다(`Object.freeze`가 필요하면 따로 호출해야 한다). 그럼에도 *의도를 표현*하는 데에는 충분히 가치 있다. 함수의 매개변수에 `Readonly<Config>`를 박아두면, 호출자가 *내가 이 객체를 변경하지 않을 것이다*라는 약속을 받는다. Kotlin의 `val`과 `data class`의 `copy` 패턴이 *문화적으로 강제하는* 그 약속을, TS는 타입 한 글자로 박는다.

### `Pick<T, K>` — 필요한 필드만 떼어내기

`User`에서 `id`와 `email`만 필요한 자리가 있다고 하자.

```typescript
type UserSummary = Pick<User, "id" | "email">;
// { id: string; email: string }
```

리스트 화면에 보여줄 *요약 모양*, 캐시 키로 쓸 *식별자 모양* 같은 자리에서 자주 쓴다. 새 인터페이스를 따로 *복사해 적기*보다 `Pick`으로 *유도*하는 편이 낫다. 원본이 바뀌면 따라서 바뀐다.

### `Omit<T, K>` — 필요 없는 필드만 떼기

`Pick`의 반대. 가장 흔한 자리는 *서버에서 ID를 만들기 전*의 모양을 표현할 때다.

```typescript
type NewUser = Omit<User, "id">;

function createUser(input: NewUser): User {
  return { id: generateId(), ...input };
}
```

*"하나만 빼고 다"*가 직관적으로 떠오를 때 `Omit`이다. Java라면 `UserCreateRequest` DTO를 따로 정의해야 했을 자리에서, TS는 `Omit` 한 줄로 끝낸다. 도메인 모델 한 벌로 *변형들*을 모두 유도해 내는 이 패턴이 익숙해지면, DTO가 폭발하는 Java 백엔드의 그 답답함이 새삼 느껴진다.

### `Record<K, V>` — 키와 값의 모양으로 객체 모델링

키 집합이 정해져 있고, 각 키에 같은 모양의 값이 들어가는 객체.

```typescript
type Role = "admin" | "user" | "guest";
type Permissions = Record<Role, string[]>;

const perms: Permissions = {
  admin: ["read", "write", "delete"],
  user: ["read", "write"],
  guest: ["read"],
};
```

`Record`는 *맵 같은 객체*를 모델링하는 가장 기본적인 도구다. 키가 union 리터럴이면 컴파일러가 *모든 키를 채웠는지* 검사해 준다. `guest`를 빼먹으면 컴파일 에러. exhaustive와 정신이 통하는 자리다.

### `ReturnType<T>` — 함수의 반환 타입 추출

이 도구부터는 *제네릭과 conditional이 짜깁기된* 고급 도구다. 자세한 작동은 5장에서 풀고, 여기서는 *언제 쓰는가*만 보자.

```typescript
function fetchUser(id: string) {
  return { id, email: "x@y.com", roles: ["user"] };
}

type FetchUserResult = ReturnType<typeof fetchUser>;
// { id: string; email: string; roles: string[] }
```

함수의 반환 타입을 *별도로 명시하지 않고도* 그 모양을 타입으로 끌어낸다. *함수가 곧 모양의 정의*가 되는 셈이다. 작은 함수에서는 별 가치가 없지만, 라이브러리가 *복잡한 모양을 반환하는* 함수를 노출할 때(예: 빌더의 결과, ORM 쿼리의 결과) 매우 유용하다. 5장에서 zod의 `z.infer`와 함께 다시 만나게 된다.

### `Awaited<T>` — Promise를 풀기

`Promise<User>`에서 `User`를 꺼내고 싶을 때.

```typescript
async function fetchUser(id: string): Promise<User> { /* ... */ return null as any; }

type User = Awaited<ReturnType<typeof fetchUser>>;
// User
```

`ReturnType`으로 함수의 반환 타입을 꺼내면 `Promise<User>`이다. 거기서 한 겹 더 벗기는 게 `Awaited`. 비동기 함수의 *결과 모양*을 타입으로 다룰 때 거의 자동으로 손이 간다. 7장의 비동기 절에서 다시 만난다.

> 💡 **유틸리티 타입을 바라보는 작은 팁**
>
> 8개를 한꺼번에 외우려 들지 말자. *상황을 맞닥뜨릴 때마다* "이런 모양이 필요한데 이미 있는 도구가 없을까?" 하고 손이 가게 만드는 편이 낫다. 처음 한두 달은 `Pick`/`Omit`/`Partial`만 써도 충분하다. `ReturnType`/`Awaited`는 *라이브러리가 복잡한 타입을 반환할 때* 자연스럽게 손이 간다. 한 번 손이 가면 그 다음부터는 고민할 필요가 없다.

## 함수 타입과 bivariance — Java로는 이해 안 되는 자리

마지막으로, 함수 타입의 *변성(variance)*을 짚자. 이 자리는 Java/Kotlin 개발자가 *처음에는 도무지 이해가 안 가는* 곳 중 하나다. 천천히 풀어보자.

먼저 변성이 뭔지 짧게 복습하자. 어떤 타입 `T`가 다른 타입 `U`의 서브타입이라고 하자(예: `Dog`은 `Animal`의 서브타입). 이때 `Container<T>`와 `Container<U>` 사이의 관계가 어떻게 되는가? *공변(covariant)*이라면 `Container<Dog>`이 `Container<Animal>`의 서브타입. *반공변(contravariant)*이라면 그 반대. *불변(invariant)*이라면 둘은 무관.

함수 매개변수의 변성은 *반공변*이 안전하다. 왜? 함수 `(d: Dog) => void`에 `(a: Animal) => void`를 *대입할 수 있는가*를 따져보자. 답은 *그렇다*. `Animal`을 받는 함수는 *모든 Animal*에 대해 동작하므로, *Dog*가 들어와도 당연히 동작한다. 반대는 안 된다. `Dog`만 받는 함수에 `Animal`을 던지면, `Dog`이 아닌 다른 `Animal`이 들어왔을 때 깨진다.

이게 *반공변*이다. Java의 wildcard `? super T`가 같은 정신이다.

그런데 TS는 기본적으로 *bivariant*로 동작한다. 즉 `(d: Dog) => void`에 `(a: Animal) => void`도, `(c: Corgi) => void`도 *둘 다 대입 가능*하다. 후자는 *안전하지 않다*. `Corgi`만 받는 함수에 `Dog`을 일반적으로 던지면 `Corgi`가 아닌 다른 `Dog`이 들어왔을 때 깨진다.

*"왜 이렇게 만들었나?"* 하고 묻고 싶어진다. 답은 *실용성* 때문이다. 자바스크립트 라이브러리들이 이 안전하지 않은 패턴을 워낙 많이 써 왔고, TS가 strict 반공변을 강제하면 *기존 JS 라이브러리의 타입 정의*가 죄다 깨진다. 그래서 의도된 unsoundness 중 하나로 두었다.

다행히 도구는 있다. tsconfig의 `strictFunctionTypes: true`(또는 `strict: true`로 자동 켜짐)를 켜면, 함수 타입에 한해 *반공변*으로 검사한다. 단, *메서드 표기법*(`m(x: T): void`)은 여전히 bivariant로 남고, *함수 표기법*(`m: (x: T) => void`)에서만 strict 반공변이 적용된다. 이 비대칭 또한 *기존 코드를 깨지 않으려는* 타협이다.

```typescript
interface Listener<T> {
  // 메서드 표기 — 여전히 bivariant
  handle(event: T): void;
}

interface Listener2<T> {
  // 함수 표기 — strictFunctionTypes 하에서 반공변
  handle: (event: T) => void;
}
```

실무 결론은 단순하다. 첫째, **`strictFunctionTypes`는 켜라**. 둘째, *함수의 변성에 민감한 자리(콜백, 이벤트 핸들러)*에서는 함수 표기법으로 적자. 이 정도만 지키면, TS의 함수 변성이 우리를 *덜 자주* 배신한다. 깊이 이해하고 싶다면 5장의 제네릭 절에서 variance를 한 번 더 다룬다 — 거기서 Java wildcard와의 매핑을 더 자세히 풀자.

> 💡 **작가의 한 마디 — bivariance에 너무 시달리지 말자**
>
> 솔직히 고백하자면, 함수 변성은 일상 코드에서 발등을 찍는 일이 그렇게 많지 않다. 대부분의 자리는 `strictFunctionTypes`가 알아서 잡아주고, 알아서 못 잡는 자리는 *애초에 우리가 그런 코드를 잘 쓰지 않는* 자리다. 처음에는 *"아, 이런 자리가 있구나"* 정도로 알아두고, 실제로 발등이 찍히면 그때 다시 펼쳐 보자. *언어를 외우려 들기보다, 도구로 두드려 보는 편이 낫다.*

## 마무리 — 처음 두드려본 도구의 손맛

여기까지 두드려본 도구를 정리하자. 추론은 *적극적*이지만 *전능하지 않다*. 좁히기는 `typeof`/`instanceof`/`in`/`===`/type predicate라는 *다섯 도구*를 모두 동원한다. 분별 유니온과 `assertNever`는 Kotlin sealed class와 *같은 정신*을 *다른 도구*로 구현한다. 유틸리티 타입은 *카탈로그가 아니라 패턴*이다 — 상황을 만나면 손이 가게 두자. `satisfies`는 *검증과 좁힘을 동시에* 갖고 싶을 때의 신선한 도구다. 함수 변성은 `strictFunctionTypes`로 막을 수 있는 만큼만 막고, 나머지는 알아두는 정도로 충분하다.

이 챕터를 마치고 났을 때 우리가 손에 든 것은 *문법의 카탈로그*가 아니다. *도메인의 결을 타입으로 표현하는 작은 감각*이다. 새 모양을 추가하면 컴파일러가 *고쳐야 할 모든 자리를 알려주고*, 잘못된 상태 조합은 *애초에 표현이 안 되며*, 외부에서 들어온 `unknown`은 *type predicate를 거쳐야 안으로 들어온다*. 이 감각이 한 번 손에 잡히면, *그다음 코드가 다른 모양으로 흐르기 시작한다.* 그게 4장이 의도한 첫 *쾌감*이다.

다만 이 도구들의 *심층*은 아직 다 펼치지 않았다. 분별 유니온의 멤버 자체를 *다른 타입에서 유도*하고 싶다면? 함수의 매개변수 모양을 *추출*해 새 함수를 합성하고 싶다면? `Partial<T>`처럼 *타입에서 타입을 만드는* 도구를 직접 만들고 싶다면? 이 모든 질문이 5장의 *제네릭과 매핑·조건부 타입* 절로 이어진다. zod의 `z.infer`, Hono의 자동 추론, Prisma의 생성 타입 같은 *마법 같은 부품들*이 그 자리에서 *부품 단위로* 보이기 시작한다.

> 📖 **더 깊이 가려면**
>
> - **타입 단위 테스트가 궁금하다면** → 14장. 타입이 *런타임에 사라지므로* 단위 테스트도 다른 도구가 필요하다. `expect-type`/`tsd`로 *타입 자체*를 단정문으로 검증하는 패턴을 자세히 다룬다. 본 장에서 만든 분별 유니온이 *의도대로 좁혀지는지*를 자동화 테스트로 못 박는 자리.
> - **strict 모드의 모든 옵션을 일별하고 싶다면** → 부록 B. tsconfig 옵션 사전. `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` 같은 *strict 가족 너머의 한 단계*를 정리해 두었다. Matt Pocock의 cheat sheet도 함께 참조하면 좋다.
> - **type predicate vs zod 같은 런타임 검증의 *경계 정책*이 궁금하다면** → 15장의 함정 절. 한국 팀의 *경계 검증(boundary validation)* 패턴이 어떻게 정착되었는지 사례와 함께.
> - **함수 변성을 *진지하게* 파고 싶다면** → 5장의 제네릭 variance 절. `extends`/`infer`와 함께 wildcard 타입의 TS식 표현을 본격적으로 다룬다.

타입을 *문법으로 외우는* 단계는 여기서 졸업이다. 다음 장에서는 *타입을 만드는 타입*의 자리로 넘어가자. 부품이 더 작아지고, 조립의 자유가 더 커진다. 5장에서 만나자.

---

> 4장에서 추론·좁히기·discriminated union·유틸리티 타입을 손에 익혔다. 그런데 zod의 `z.infer`, Hono의 자동 타입 흐름, Prisma의 생성 타입 같은 라이브러리 마법들이 어떻게 작동하는지는 아직 설명이 남아 있다. 그 마법의 부품들 — 제네릭·조건부 타입·infer·매핑·템플릿 리터럴 — 을 분해하는 것이 5장의 약속이다.

# 5장. 타입을 만드는 타입 — 제네릭·conditional·infer·매핑·템플릿 리터럴

zod의 코드를 처음 본 날을 떠올려보자. 누군가 짠 코드 한 줄이 눈에 들어온다.

```ts
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().nonnegative(),
});

type User = z.infer<typeof UserSchema>;
```

여기서 `User`의 마우스 호버 툴팁을 띄우면 IDE는 친절하게 다음을 보여준다.

```ts
type User = {
  id: string;
  email: string;
  age: number;
}
```

스키마는 분명 *값*이었다. 런타임에 검증을 수행하는 일반 객체였다. 그런데 그 값으로부터 `type User = …`라는 타입이 *유도*되어 나온다. 한 번도 타입을 손으로 적은 적이 없다. 처음 본 사람은 잠깐 멍해진다. *"이게 어떻게 되지? 타입은 컴파일타임에만 존재하는 것 아니었나? 값에서 타입을 어떻게 끌어내지?"*

비슷한 충격이 Hono에도 있다. 라우트 하나를 정의했을 뿐인데 클라이언트 쪽에서 응답 타입이 자동으로 채워진다. tRPC는 더 노골적이다. 서버에서 procedure 하나를 만들면 클라이언트가 그 procedure를 *원격 함수처럼* 호출하는데, 인자 타입과 반환 타입이 정확하게 잡힌다. Prisma는 스키마 파일 한 줄을 바꾸면 IDE의 자동완성이 즉시 따라온다.

이 모든 것이 **타입이 타입을 만든다**는 한 문장으로 요약되는 도구들 위에 서 있다. 5장의 약속은 이거다 — 이 마법을 *부품으로 분해*해서, 다음에 zod 코드를 보면 *"아 이래서 이게 됐구나"*가 손에 잡히도록 하자. 곡예를 부리려는 게 아니다. 우리가 *매일 보는 라이브러리*가 어떤 부품으로 조립되어 있는지를 한 단계씩 올라가며 보자는 것이다.

순서는 이렇다. 먼저 **제네릭과 제약**으로 시작한다. 그 위에 `keyof`·`typeof`·`T[K]`라는 세 도구의 합주를 얹는다. 그 다음이 **매핑 타입** — 객체 타입을 함수처럼 변형하는 도구다. 거기서 한 발 더 나가면 **조건부 타입**이 있고, 그 안에 마법의 키워드 **`infer`**가 숨어 있다. 그 다음이 **템플릿 리터럴 타입**이고, 마지막으로 이 모든 것을 합치면 **재귀 조건부 타입**으로 임의의 깊이를 다룰 수 있다. 부품이 다 모이면 zod·Hono·Prisma·tRPC를 분해해보자. 그 뒤에 두 가지 현실 주제를 다룬다 — *타입 단언(`as`)의 윤리*와 *declaration merging*. 둘 다 입사 첫 달에 마주칠 자리다.

호흡이 길다. 5장이 이 책에서 가장 두꺼운 챕터인 이유가 있다 — *깊이*가 약속이니까. 천천히 읽자.

## 5.1 제네릭은 함수다 — `extends`·default·다중 매개변수

제네릭은 자바 개발자에게 친숙한 개념이다. `List<String>`을 처음 본 날, "오, 컬렉션이 자기 안에 어떤 타입이 들어 있는지를 표현할 수 있구나" 했던 그 감각. TS의 제네릭도 출발점은 같다.

```ts
function identity<T>(value: T): T {
  return value;
}

const a = identity("hello"); // a: string
const b = identity(42);      // b: number
```

여기까지는 자바와 거의 같다. `T`라는 타입 매개변수가 있고, 호출 시점에 실제 타입이 채워진다. *"좋아, 이건 안다"* 싶은 자리다. 그런데 한 발만 더 들어가면 분위기가 달라진다.

### 제네릭은 *값을 받는 함수*가 아니라 *타입을 받는 함수*다

자바에서는 제네릭을 보통 *컬렉션의 빈자리*로 받아들인다. `List<T>`에서 `T`는 그 컬렉션이 담을 원소의 타입이다. 그런데 TS에서는 제네릭을 *타입 수준의 함수*로 받아들이는 편이 낫다.

```ts
type Box<T> = { value: T };
```

이 한 줄을 자바 시선으로 읽으면 *"`T`라는 타입 매개변수를 가진 클래스 비슷한 것"*이다. TS 시선으로 다시 읽으면 *"`T`라는 타입을 받아서 `{ value: T }`라는 타입을 *돌려주는* 타입 함수"*다. 같은 것 같지만 사고 모드가 다르다. 후자로 보기 시작하면, 곧 보게 될 매핑 타입이나 조건부 타입이 *낯설지 않다*. 그것들은 모두 *입력 타입을 받아서 출력 타입을 돌려주는 함수*에 불과하니까.

```ts
type StringBox = Box<string>;  // { value: string }
type NumberBox = Box<number>;  // { value: number }
```

함수 호출과 모양이 똑같다. 인자(`string`)를 넣으면 결과(`{ value: string }`)가 나온다. *"제네릭은 함수다"*라는 직관이 여기서 시작한다.

### `extends`로 제약을 건다 — Java/Kotlin에서 익숙한 자리

제네릭의 빈자리에 *아무 타입이나* 들어와도 되는 건 아니다. *"길이가 있는 것만 받겠다"*고 말하고 싶으면 제약을 건다.

```ts
function logLength<T extends { length: number }>(value: T): T {
  console.log(value.length);
  return value;
}

logLength("hello");          // OK
logLength([1, 2, 3]);        // OK
logLength({ length: 7 });    // OK
logLength(42);               // 에러: number에는 length가 없다
```

자바라면 `<T extends HasLength>` 같은 느낌이고, 코틀린이라면 `<T : HasLength>`다. 이름은 다르지만 의도는 같다 — *"이 타입 매개변수는 이런 모양을 만족해야 한다"*. 그런데 TS의 `extends`가 자바·코틀린의 그것과 한 군데에서 결정적으로 다르다 — TS는 **구조적**이다. 어딘가에 `interface HasLength { length: number }`라고 *선언하지 않아도* `{ length: number }` 모양만 만족하면 호환된다. 3장에서 이미 본 그 *구조적 타입*의 정신이 제네릭 제약에도 그대로 적용된다.

조금 더 흥미로운 패턴을 보자. `T extends keyof U`처럼 *다른 타입 매개변수*에 의존하는 제약도 가능하다.

```ts
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

const user = { id: 1, name: "Toby", email: "t@example.com" };
const picked = pick(user, ["id", "name"]);
// picked: { id: number; name: string }
```

여기서 `K extends keyof T`가 핵심이다. *"`K`라는 타입 매개변수는 `T`의 키 중 하나여야 한다"*. 그래서 `pick(user, ["id", "phone"])`이라고 쓰면 컴파일러가 즉시 막는다 — `phone`은 `keyof user`가 아니니까. 자바에서 이 정도의 *키 수준 안전성*을 표현하려면 별도의 `enum` 클래스를 만들거나 reflection을 동원해야 한다. TS는 그것을 타입 매개변수 한 줄로 끝낸다.

### default 타입 매개변수 — 호출자에게 선택권을 주는 패턴

자바 12 즈음부터는 record나 pattern matching이 들어왔지만, 제네릭에 *기본값*을 주는 문법은 (책 집필 시점 기준) 없다. TS에는 있다.

```ts
type ApiResponse<TData = unknown, TError = Error> = {
  data: TData;
  error?: TError;
};

type UserResponse = ApiResponse<User>;        // TError는 Error로 default
type Custom = ApiResponse<User, ApiError>;    // 둘 다 명시
```

이 한 줄은 라이브러리 설계에서 자주 본다. *"보통은 이걸 쓰지만, 필요하면 바꿔라"*는 안내가 타입 수준에 박혀 있는 셈이다. React의 `useState<T = undefined>`, fetch 래퍼의 `Response<TBody = unknown>` 같은 것들이 모두 이 패턴이다.

### 다중 타입 매개변수의 합주

타입 매개변수가 두 개 이상이 되면 *함수가 함수를 받는* 사고가 자연스러워진다.

```ts
function map<T, U>(arr: T[], fn: (item: T) => U): U[] {
  return arr.map(fn);
}

const nums = map(["a", "bb", "ccc"], (s) => s.length);
// nums: number[]
```

`T`는 입력 배열의 원소 타입, `U`는 변환 후의 원소 타입. 호출자가 `(s) => s.length`라고 쓰는 순간 `T = string`, `U = number`가 *추론*된다. 손으로 적지 않아도 컴파일러가 따라온다 — 4장에서 본 *contextual typing*의 연장이다.

여기서 한 가지 짚어두자. 제네릭을 잘 다룬다는 것은 *타입 매개변수의 흐름을 머릿속에 그릴 수 있다*는 뜻이다. 입력에서 어떤 타입이 들어와서, 어떤 변환을 거쳐, 어떤 출력이 나가는지. 자바의 `Function<T, R>`, `BiFunction<T, U, R>`을 떠올려보면 친숙할 것이다. 차이는 — TS에서는 그 흐름이 *수십 단계*로 길어질 수 있고, 우리가 5장 후반부에 보게 될 zod·tRPC가 정확히 그런 길이의 흐름이다.

> ### 📚 Java/Kotlin 시선 박스 ① — Kotlin reified generic ↔ TS의 한계와 우회
>
> 코틀린에는 `inline` 함수와 결합된 `reified` 키워드가 있다. 런타임에 타입 매개변수의 정보를 *보존*해서, 함수 안에서 `T::class`를 직접 호출할 수 있게 해준다.
>
> ```kotlin
> // Kotlin
> inline fun <reified T> Gson.fromJson(json: String): T =
>     this.fromJson(json, T::class.java)
>
> val user: User = gson.fromJson(jsonString)
> ```
>
> 자바는 erasure 때문에 이게 안 된다. `Class<T>` 객체를 명시적으로 받아야 한다.
>
> ```java
> // Java
> User user = gson.fromJson(jsonString, User.class);
> ```
>
> TS는 어느 쪽일까? **자바와 같다**. 더 나아가 자바보다 더 가혹하다. `tsc`가 끝나면 *모든 타입이 사라진다*. `Class<T>` 같은 런타임 메타데이터도 없다. 3장에서 본 *type erasure*가 여기서 다시 발목을 잡는다.
>
> ```ts
> // TS — 작동하지 않는다
> function fromJson<T>(json: string): T {
>   return JSON.parse(json) as T;  // 그냥 캐스팅. 검증 없음.
> }
>
> const user = fromJson<User>("{\"id\": 1}");  // 컴파일은 된다. 런타임은 모른다.
> ```
>
> 그래서 TS 진영에는 *우회 전략 두 가지*가 정착했다.
>
> **첫째, 스키마를 값으로 들고 다닌다.** zod·valibot·io-ts 같은 라이브러리가 그 자리다. 스키마 객체에서 *타입을 유도하고*(컴파일타임), *런타임 검증*을 같은 객체로 한다. 한 번 정의하면 두 자리가 동시에 채워진다.
>
> ```ts
> const UserSchema = z.object({ id: z.number(), name: z.string() });
> type User = z.infer<typeof UserSchema>;            // 컴파일타임
> const user = UserSchema.parse(jsonValue);          // 런타임
> ```
>
> **둘째, 런타임 메타데이터가 필요한 곳은 데코레이터 + reflect-metadata로 채운다.** NestJS·TypeORM·class-validator가 이 길을 갔다. 단, TC39 신규 데코레이터 표준에는 reflect-metadata가 빠져 있어서, 두 진영(legacy vs TC39)이 당분간 갈라져 있다. 13장에서 더 깊이 다룬다.
>
> 정리하면 — *코틀린의 reified는 TS에 없다*. 대신 *값과 타입을 같은 정의에서 끌어내는* zod 패턴이 사실상의 표준이 되었다. *"왜 zod가 이렇게 인기가 많지?"*의 답이 절반은 여기에 있다.

## 5.2 `keyof`·`typeof`·`T[K]` — 세 도구의 합주

제네릭을 도구로 쓰려면 *타입을 조작하는 작은 도구들*이 필요하다. TS에는 그런 도구가 여럿 있는데, 가장 자주 함께 등장하는 셋이 `keyof`·`typeof`·`T[K]`다. 처음 보면 따로따로 도는 도구처럼 느껴지지만, 사실은 *3중주*다 — 같이 쓰일 때 위력이 나온다.

### `keyof T` — 객체 타입의 키를 *유니온으로* 꺼낸다

```ts
type User = {
  id: number;
  name: string;
  email: string;
};

type UserKey = keyof User;
// "id" | "name" | "email"
```

`keyof`는 객체 타입을 받아서 *키들의 유니온*을 돌려주는 연산자다. 자바에는 직접 대응이 없다 — 굳이 비교하자면 *컴파일타임의 reflection*에 가까운데, 자바는 그걸 런타임에 `Field[]`로 한다.

여기서 한 가지 짚자. `keyof T`의 결과는 *문자열 리터럴 유니온*이지, 그냥 `string`이 아니다. `"id" | "name" | "email"`이라는 *세 개의 정확한 값들*의 유니온이다. 이게 곧 5.6의 템플릿 리터럴 타입과 결합되면 굉장한 표현력을 낸다.

### `typeof v` — 값에서 타입을 *유도한다*

3장에서 한 번 등장했지만 5장의 맥락에서 다시 보자. `typeof`는 두 얼굴이 있다. 런타임에는 JS 연산자로 동작해서 `"string"`, `"number"` 같은 문자열을 돌려준다. 컴파일타임에는 TS 연산자로 동작해서 *값의 타입을 추론*한다.

```ts
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retry: 3,
} as const;

type Config = typeof config;
// {
//   readonly apiUrl: "https://api.example.com";
//   readonly timeout: 5000;
//   readonly retry: 3;
// }
```

`as const`가 붙어 있어서 리터럴 타입이 그대로 유지된 점에 주목하자(4장 참조). `typeof config`는 그 *전체 모양*을 타입으로 끌어낸다. 손으로 다시 적을 필요가 없다.

이게 곧 zod의 `z.infer<typeof Schema>` 패턴의 절반이다 — *값(스키마)에서 타입을 끌어내기 위해 `typeof`를 쓰는 자리*. 그러니 우리가 zod의 마법을 분해할 때 가장 먼저 만나는 부품이 바로 이 `typeof`다.

### `T[K]` — indexed access, *키로 값의 타입을 꺼낸다*

자바의 `Map`에서 `map.get("name")`을 하면 값을 꺼낸다. TS의 `T[K]`는 그 *컴파일타임 버전*이다.

```ts
type User = { id: number; name: string; email: string };

type Id = User["id"];        // number
type Name = User["name"];    // string
type IdOrName = User["id" | "name"];  // number | string
```

키 자리에 *유니온*을 넣어도 된다. 그러면 결과도 *유니온*으로 나온다. 깔끔하다.

여기까지가 각자의 얼굴이고, 이제 셋이 합주하는 자리를 보자.

### 합주 — 진짜 위력이 나오는 자리

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Toby", email: "t@example.com" };

const id = getProperty(user, "id");      // id: number
const name = getProperty(user, "name");  // name: string
const oops = getProperty(user, "phone"); // 컴파일 에러
```

이 함수의 시그니처를 천천히 읽어보자. `T`는 객체 타입. `K`는 *그 객체의 키 중 하나*(`extends keyof T`로 제약). 반환 타입은 `T[K]` — *그 키에 해당하는 값의 타입*. 이 한 줄이 *런타임에 키로 값을 꺼낸다*는 동작의 *타입 안전한 일반화*다.

자바라면? 같은 안전성을 얻으려면 *키마다 별도의 메서드*를 만들거나, `Map<String, Object>`에 캐스팅을 끼얹거나, Lombok의 코드 생성에 의존해야 한다. TS는 *세 도구의 합주*로 한 줄에 끝낸다.

이 패턴을 한 번 손에 익혀두면 5장의 나머지가 훨씬 잘 읽힌다. 매핑 타입도, 조건부 타입도, infer도 — 모두 이 *제네릭 제약 + keyof + indexed access*의 변주에 가깝다. *기억해두자.*

## 5.3 매핑 타입 — 객체 타입을 *변형하는 함수*

자바에서 *모든 필드를 nullable로 만든 버전*의 클래스가 필요하다고 해보자. 어떻게 할까? 아마 새 클래스를 *손으로 만든다*. 필드 30개면 30개를 다 적는다. 한 곳을 바꾸면 두 곳을 바꿔야 한다. 끔찍한 일이다.

TS는 이걸 *타입 함수*로 푼다. 매핑 타입(mapped type)이 그 자리다.

```ts
type Partial<T> = {
  [K in keyof T]?: T[K];
};
```

표준 라이브러리에 정의된 `Partial`의 본체다. 한 줄짜리지만 부품이 다 들어 있다.

- `keyof T` — 키들의 유니온
- `[K in keyof T]` — *그 유니온을 순회*
- `?:` — 각 필드를 optional로 만든다
- `T[K]` — 그 키에 해당하는 원래 타입

읽는 법: *"`T`의 모든 키 `K`에 대해, optional이고 타입이 `T[K]`인 필드를 만든다"*. 자바에서 30줄로 적던 걸 TS는 한 줄로 적는다.

```ts
type User = { id: number; name: string; email: string };
type PartialUser = Partial<User>;
// {
//   id?: number;
//   name?: string;
//   email?: string;
// }
```

### modifier — `+`/`-`로 *붙이고 떼기*

매핑 타입의 modifier는 두 가지 — `readonly`와 `?`(optional). 각각 앞에 `+`(붙이기) 또는 `-`(떼기)를 둘 수 있다.

```ts
type Required<T> = {
  [K in keyof T]-?: T[K];   // optional을 떼고 모두 필수로
};

type Mutable<T> = {
  -readonly [K in keyof T]: T[K];   // readonly를 떼서 변경 가능하게
};
```

`Mutable`은 표준에 없지만 자주 직접 만든다. 외부에서 `Readonly<Config>`로 받은 객체를 내부에서 가변 버전으로 다시 받아야 할 때 같은 자리. 한 줄짜리 도구를 자기 코드베이스에 가지고 다니는 셈이다.

`+`는 *기본값*이라 보통 생략한다. `[K in keyof T]+?: T[K]`도 합법이지만, 그냥 `[K in keyof T]?: T[K]`로 적는다.

### key remapping — `as`로 *키 자체를 변형*한다

TS 4.1부터 매핑 타입의 키를 `as`로 다시 적을 수 있게 됐다. 이게 굉장히 유용하다.

```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type User = { id: number; name: string };
type UserGetters = Getters<User>;
// {
//   getId: () => number;
//   getName: () => string;
// }
```

키 자리의 `as`는 *런타임의 타입 단언*이 아니라 *키 변환의 표시*다. 같은 키워드가 두 자리에서 다른 일을 한다 — 헷갈릴 만하지만, 문맥이 다르니 익숙해지면 구분된다.

여기서 `Capitalize`는 5.6에서 만날 *intrinsic string utility*다. 그리고 `string & K`는 키가 `string | number | symbol` 중 *문자열만* 골라내는 트릭이다. 처음 보면 어지럽지만, 5.6까지 가서 다시 보면 자연스럽다.

### *키를 떨어뜨리는* 패턴 — `never`의 조용한 활용

key remapping의 또 다른 쓰임은 *조건에 맞지 않는 키를 떨어뜨리는* 자리다.

```ts
type OmitByValue<T, V> = {
  [K in keyof T as T[K] extends V ? never : K]: T[K];
};

type User = { id: number; name: string; password: string };
type SafeUser = OmitByValue<User, "password" | { password: string }>;
// 타입 V에 맞는 키는 떨어뜨린다.
```

키 자리에 `never`가 들어오면 *그 키는 결과 타입에서 제외*된다. 조건부 타입(다음 절)과 결합된 패턴인데, 한 번 손에 익으면 *"필요 없는 키 빼기"*를 한 줄로 끝낼 수 있다.

이쯤 되면 매핑 타입이 *타입 수준의 `for` 루프 + `if` 분기*처럼 느껴진다. 그게 정확한 직관이다. 자바에서 객체의 모양을 바꾸려면 reflection이나 코드 생성을 동원해야 했지만, TS는 이걸 *타입 시스템 안에서* 한다. 런타임 비용이 0이고, IDE가 즉시 따라온다.

> ### 📚 Java/Kotlin 시선 박스 ② — Java wildcard `? extends`/`? super` ↔ TS variance
>
> 자바 제네릭의 가장 어려운 부분이 변성(variance)이다. `List<? extends Number>`는 *Number의 하위 타입을 담은 List*를 받는다 — *읽기는 되지만 쓰기는 못한다*(producer). `List<? super Integer>`는 *Integer의 상위 타입을 담은 List* — *쓰기는 되지만 읽기는 Object로만*(consumer). PECS — Producer Extends, Consumer Super.
>
> 코틀린은 같은 개념을 `out`/`in` 키워드로 *선언 시점*에 표현한다.
>
> ```kotlin
> interface Producer<out T> { fun produce(): T }
> interface Consumer<in T> { fun consume(item: T) }
> ```
>
> TS는? **변성을 *별도 키워드*로 강제하지 않는다**. 함수 매개변수의 변성은 기본적으로 *bivariant*(양쪽으로 호환) — strict 모드에서 `strictFunctionTypes`를 켜면 *contravariant*(반변)으로 좁혀진다. 4장에서 잠깐 본 그 자리다.
>
> ```ts
> // strictFunctionTypes ON
> type Animal = { name: string };
> type Dog = Animal & { bark(): void };
>
> let f1: (a: Animal) => void = (a) => console.log(a.name);
> let f2: (d: Dog) => void = f1;  // OK — Dog ⊆ Animal이므로 contravariant 호환
> ```
>
> TS 4.7부터는 *명시적 variance annotation*도 들어왔다 — `out`/`in` 키워드를 타입 매개변수 앞에 붙일 수 있다.
>
> ```ts
> interface Producer<out T> { produce(): T; }
> interface Consumer<in T> { consume(item: T): void; }
> ```
>
> 코틀린과 문법까지 같다. 다만 TS의 variance는 *기본이 구조적 추론*이고, `out`/`in`은 *컴파일러에게 힌트를 주거나 의도를 문서화*하는 용도에 가깝다. 자바의 wildcard처럼 *호출자가 매번* `? extends`/`? super`를 적는 모델은 아니다.
>
> 정리: TS의 변성은 자바보다는 코틀린에 가깝지만, 런타임 강제가 없고 unsoundness 자리도 일부 남겨둔다. *변성을 잊고 살아도 일상 코드는 돌아가지만, 라이브러리 설계자라면 `strictFunctionTypes`를 켜고 명시적 `out`/`in`을 쓰는 편이 낫다.* 일반 애플리케이션 개발자가 이 자리에서 발이 걸리는 일은 드물다.

## 5.4 조건부 타입 — `T extends U ? X : Y`

여기서부터가 5장의 *클라이맥스로 가는 길*이다. 조건부 타입(conditional type)은 모양이 단순하다 — *3항 연산자의 타입 버전*이다.

```ts
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<"hello">;  // "yes"
type B = IsString<42>;        // "no"
type C = IsString<boolean>;   // "no"
```

`T extends U`는 *"`T`가 `U`에 할당 가능한가"*라는 질문이다. 그 답에 따라 `X` 또는 `Y`를 돌려준다. 자바·코틀린에는 직접 대응이 없다. 굳이 비교하자면 *컴파일타임에 동작하는 `if`*다.

이 정도만 보면 *"음, 그래서?"* 싶을 수 있다. 조건부 타입의 진짜 힘은 두 가지 자리에서 나온다 — **distributive 동작**과 **`infer` 키워드**.

### distributive — 유니온이 들어오면 *각 멤버에 분배*된다

```ts
type ToArray<T> = T extends any ? T[] : never;

type A = ToArray<string>;            // string[]
type B = ToArray<string | number>;   // string[] | number[]
```

`B`를 보자. `string | number`라는 유니온이 들어왔는데 결과가 `(string | number)[]`이 *아니라* `string[] | number[]`다. 왜 그럴까?

조건부 타입의 *왼쪽*에 *벌거벗은 타입 매개변수*(naked type parameter)가 들어가면, 컴파일러는 유니온의 *각 멤버*에 대해 *따로 조건을 평가*한다. 위 예에서는 `string extends any ? string[] : never`와 `number extends any ? number[] : never`가 각각 평가되고, 결과가 다시 유니온으로 합쳐진다.

이걸 *"distributive conditional type"*이라고 부른다. 처음엔 마법처럼 느껴지지만, *유니온은 본질적으로 분배된다*는 직관을 가지면 자연스럽다.

### distributive를 *끄는* 트릭 — `[T]`로 감싸기

분배가 *원치 않는* 자리도 있다. 그럴 땐 *튜플로 감싸는* 트릭을 쓴다.

```ts
type IsExactlyString<T> = [T] extends [string] ? "yes" : "no";

type A = IsExactlyString<string>;            // "yes"
type B = IsExactlyString<string | number>;   // "no" — 분배되지 않는다
```

`[T]`로 감싸면 더 이상 *벌거벗은 타입 매개변수*가 아니므로 분배가 일어나지 않는다. 작은 트릭이지만 자주 쓰인다 — *"엄격하게 같은가"*를 확인할 때.

### `Exclude`/`Extract` — 표준에 들어 있는 패턴

조건부 + distributive의 가장 흔한 활용이 *유니온에서 일부를 골라내거나 빼는* 자리다. 표준 라이브러리에 이미 있다.

```ts
type Exclude<T, U> = T extends U ? never : T;
type Extract<T, U> = T extends U ? T : never;

type A = Exclude<"a" | "b" | "c", "b">;  // "a" | "c"
type B = Extract<string | number | boolean, string | number>;  // string | number
```

읽는 법은 똑같다. `T extends U ? … : …`인데, distributive가 작동해서 유니온의 각 멤버가 따로 평가된다. `Exclude`는 *맞으면 버리고*, `Extract`는 *맞으면 남긴다*. `never`로 떨어진 멤버는 유니온에서 *조용히 사라진다* — `string | never`는 `string`이니까.

이 두 도구는 실전에서 매우 자주 쓰인다. *"이 유니온에서 string만 골라줘"*, *"이 유니온에서 null과 undefined만 빼줘"*(`NonNullable`이 그것이다) 같은 자리.

```ts
type NonNullable<T> = T extends null | undefined ? never : T;

type A = NonNullable<string | null | undefined>;  // string
```

자바였다면 `Optional<T>`로 감싸거나 `if (x != null)`로 좁혔겠지만, TS는 *타입 자체*에서 null/undefined를 제거하는 도구를 표준으로 제공한다.

여기까지가 조건부 타입의 모양이다. 모양은 단순하다 — `T extends U ? X : Y`. 그런데 이 단순한 모양 안에, 이 책 통틀어 가장 강력한 키워드 하나가 들어 있다. **`infer`**다.

## 5.5 `infer`의 실전 — `ReturnType`·`Awaited`·직접 만드는 도구들

조건부 타입의 *조건 절 안*에서, 컴파일러에게 *"이 자리의 타입을 잡아서 변수에 담아라"*라고 시킬 수 있다. 그 키워드가 `infer`다. 한 줄로 보자.

```ts
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

천천히 읽자.

- `T`가 *함수 타입*인지 본다 — `(...args: any[]) => …`
- 그 *반환 타입* 자리에 `infer R`을 두고 — *"여길 잡아서 `R`이라고 부르자"*
- 잡혔으면 `R`을 돌려주고, 아니면 `never`

```ts
type A = ReturnType<() => number>;             // number
type B = ReturnType<(s: string) => boolean>;   // boolean
type C = ReturnType<string>;                   // never (함수가 아니므로)
```

처음 본 사람은 잠깐 멈춘다. *"잡는다는 게 뭐지? 패턴 매칭 같은 건가?"* 정확히 그렇다. 코틀린의 destructuring이나 Scala의 pattern matching을 떠올리면 된다. *타입의 모양 안에서 특정 자리에 들어오는 타입을 잡아서 변수에 담는* 도구다.

### `Parameters`도 같은 방식

```ts
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

type A = Parameters<(name: string, age: number) => void>;
// [name: string, age: number]
```

이번엔 매개변수 자리를 잡아서 *튜플*로 돌려준다. 함수의 시그니처에서 *입력 부분만* 끌어내는 도구다. 자바·코틀린에는 이런 메타 조작이 없다 — 굳이 비교하자면 reflection으로 `Method.getParameterTypes()`를 호출하는 자리지만, 이건 *컴파일타임*이다.

### `Awaited` — Promise를 *벗기는* 패턴

```ts
type Awaited<T> = T extends Promise<infer U> ? U : T;

type A = Awaited<Promise<string>>;       // string
type B = Awaited<string>;                // string (그냥 통과)
```

`Promise<U>` 모양이면 `U`를 잡아서 돌려준다. *Promise를 한 겹 벗기는 도구*다. 표준 라이브러리에는 더 정교한 버전이 들어 있는데(중첩된 Promise까지 다 벗긴다), 핵심 아이디어는 같다.

이게 `async` 함수의 반환 타입을 다룰 때 자주 쓰인다.

```ts
async function fetchUser(): Promise<User> { /* ... */ }

type FetchedUser = Awaited<ReturnType<typeof fetchUser>>;
// User
```

`typeof fetchUser`로 함수의 타입을 잡고 → `ReturnType`으로 반환 타입(`Promise<User>`)을 꺼내고 → `Awaited`로 한 겹 벗겨서 `User`를 얻는다. *세 도구의 합주*다. 5.2에서 본 *"세 도구가 함께 작동한다"*는 직관이 여기서도 살아 있다.

### 직접 `PromiseValue`를 만들어보자

표준에 있는 도구만 쓰지 말고 직접 만들어보면 감각이 잡힌다.

```ts
type PromiseValue<T> = T extends Promise<infer U>
  ? U extends Promise<any>
    ? PromiseValue<U>   // 중첩된 Promise면 재귀
    : U
  : T;

type A = PromiseValue<Promise<string>>;              // string
type B = PromiseValue<Promise<Promise<number>>>;     // number
type C = PromiseValue<string>;                       // string
```

조건부 타입을 *재귀*로 호출했다. 이게 가능하다는 것 자체가 처음엔 놀랍다. *"타입이 자기 자신을 호출한다고?"* 그렇다. TS 4.1부터 재귀 조건부 타입이 정식으로 지원된다. 5.7에서 더 본다.

### `infer`의 *위치*가 곧 의미다

`infer`의 흥미로운 점은 *어디에 두느냐에 따라 무엇을 잡을지가 결정된다*는 거다.

```ts
// 함수의 첫 번째 인자만 잡기
type FirstArg<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;

// 배열의 원소 타입 잡기
type ElementOf<T> = T extends (infer U)[] ? U : never;

// 객체의 특정 필드 타입 잡기
type IdOf<T> = T extends { id: infer I } ? I : never;

type A = FirstArg<(s: string, n: number) => void>;  // string
type B = ElementOf<number[]>;                        // number
type C = IdOf<{ id: number; name: string }>;        // number
```

세 줄짜리 도구들이지만, 한 번 손에 익으면 *어떤 모양에서든 원하는 자리를 잡아낼 수 있다*. 자바·코틀린에서는 reflection이나 별도의 코드 생성으로 풀어야 했던 문제를 *타입 한 줄*로 끝낸다.

여기까지 오면 zod·tRPC·Hono의 기둥이 거의 다 보인다. 5.8에서 분해할 때 *"아 이건 `infer`구나"*가 즉시 잡힐 것이다.

## 5.6 템플릿 리터럴 타입 — `\`/api/${string}\``

문자열도 타입이 될 수 있다는 건 4장에서 봤다. `"pending"`, `"done"` 같은 *리터럴 타입*. 그런데 TS 4.1부터 한 발 더 나갔다 — *문자열 리터럴을 조립할 수 있는 문법*이 들어왔다.

```ts
type ApiPath = `/api/${string}`;

const path1: ApiPath = "/api/users";    // OK
const path2: ApiPath = "/api/posts/1";  // OK
const path3: ApiPath = "/users";        // 컴파일 에러
```

JS의 템플릿 리터럴(`${...}`)과 모양이 똑같다. 다만 *값*이 아니라 *타입*을 조합한다. `string`이라는 타입을 *문자열 자리*에 끼워 넣은 셈이다.

이 도구의 진짜 위력은 *유니온과 결합될 때* 나온다.

```ts
type Method = "get" | "post" | "put" | "delete";
type Resource = "users" | "posts" | "comments";

type Route = `${Method} /${Resource}`;
// "get /users" | "get /posts" | "get /comments"
// | "post /users" | "post /posts" | "post /comments"
// | ...
// 총 12개 조합
```

`Method`(4개) × `Resource`(3개) = 12개의 *정확한 문자열 유니온*이 자동으로 만들어진다. 손으로 12줄을 적을 일이 없다.

### intrinsic string utility — `Uppercase`·`Lowercase`·`Capitalize`·`Uncapitalize`

TS 4.1과 함께 *내장된 문자열 유틸리티 타입*이 네 개 들어왔다. 이름 그대로다.

```ts
type A = Uppercase<"hello">;       // "HELLO"
type B = Lowercase<"HELLO">;       // "hello"
type C = Capitalize<"hello">;      // "Hello"
type D = Uncapitalize<"Hello">;    // "hello"
```

이게 매핑 타입의 key remapping과 결합되면 *"필드 이름 변환"* 같은 일이 한 줄로 된다. 5.3에서 봤던 `Getters<T>`가 그 자리였다.

```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

이 한 줄을 다시 읽어보자. `keyof T`로 키를 꺼내고, `Capitalize`로 첫 글자를 대문자화하고, ``get${...}``으로 접두사를 붙이고, 새 키 자리에 `as`로 표시한다. 자바에서 Lombok이 어노테이션으로 처리하던 *getter 생성*을, TS는 *타입 한 줄*로 표현한다. 런타임 코드 생성도 아니다 — 컴파일타임에 *타입만* 만든다. 실제 메서드 본체는 별개다(보통 Proxy로 구현).

### 패턴 매칭의 자리

템플릿 리터럴 타입은 `infer`와 결합되면 *문자열 패턴 매칭*이 된다.

```ts
type ExtractRoute<T> = T extends `${string} ${infer Path}` ? Path : never;

type A = ExtractRoute<"GET /users">;       // "/users"
type B = ExtractRoute<"POST /api/posts">;  // "/api/posts"
```

문자열의 *공백 뒤 부분*을 잡아서 돌려주는 도구다. `infer Path`가 정확히 그 자리를 잡아낸다. 처음 보면 *"이걸 타입 시스템이 한다고?"* 싶다. 그렇다, 한다.

이 패턴이 Hono의 라우트 정의나 Express의 path parameter 추출 같은 자리에서 핵심적으로 쓰인다 — 5.8에서 보자.

## 5.7 재귀 조건부 타입 — `DeepReadonly`·`Paths`

5.5에서 잠깐 본 *재귀 조건부 타입*을 본격적으로 쓸 차례다. *임의의 깊이를 가진 자료구조*를 다룰 수 있게 해준다.

### `DeepReadonly` — 모든 중첩 필드를 readonly로

표준 `Readonly<T>`는 *얕은* readonly다 — 1단계만 처리한다.

```ts
type Config = {
  api: { url: string; timeout: number };
  retry: number;
};

type A = Readonly<Config>;
// {
//   readonly api: { url: string; timeout: number };  // 안쪽은 readonly가 아니다
//   readonly retry: number;
// }
```

깊이 들어가서 *모든 중첩 필드*를 readonly로 만들고 싶을 때 직접 만든다.

```ts
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? T[K] extends Function
      ? T[K]
      : DeepReadonly<T[K]>
    : T[K];
};

type A = DeepReadonly<Config>;
// {
//   readonly api: {
//     readonly url: string;
//     readonly timeout: number;
//   };
//   readonly retry: number;
// }
```

핵심은 매핑 타입 안에서 *자기 자신을 재귀 호출*한다는 것. 함수 타입은 빼고(함수도 object라서), 배열·일반 객체에 대해서만 재귀로 들어간다. 이렇게 만들어두면 어떤 깊이의 구조든 한 번에 처리된다.

자바라면? Lombok도 못 한다. 직접 클래스 트리를 다 만들거나 reflection으로 런타임에 freeze해야 한다. *번거로운 일이다.* TS는 타입 한 덩어리로 끝낸다.

### `Paths` — 객체의 경로를 *문자열 유니온으로*

조금 더 야심찬 도구를 만들어보자. *객체의 모든 경로*를 문자열로 표현하는 타입이다.

```ts
type Paths<T> = T extends object
  ? {
      [K in keyof T & string]:
        T[K] extends object
          ? `${K}` | `${K}.${Paths<T[K]>}`
          : `${K}`;
    }[keyof T & string]
  : never;

type Config = {
  api: { url: string; timeout: number };
  retry: number;
};

type P = Paths<Config>;
// "api" | "api.url" | "api.timeout" | "retry"
```

매핑 타입으로 키를 순회하고, 각 키에 대해 *그 키 자체*와 *`키.하위경로`* 형태를 둘 다 만든 뒤, *유니온으로 합친다*. 마지막의 `[keyof T & string]`이 객체의 *값들의 유니온*을 꺼내는 indexed access 트릭이다(5.2의 합주). 재귀 + 매핑 + 인덱스드 액세스 + 템플릿 리터럴이 다 들어 있다.

이런 도구가 실전에서 쓰이는 자리가 *form 라이브러리*다. react-hook-form 같은 곳에서 *필드 경로를 문자열로 받는데 타입은 안전한* 마법이 정확히 이 패턴이다.

```ts
form.setValue("api.url", "https://...");        // OK
form.setValue("api.timeout", 5000);              // OK
form.setValue("api.notExist", "...");           // 컴파일 에러
```

처음 보면 마법 같지만, 부품을 알면 *"아, `Paths<T>`로 키를 끌어내고 indexed access로 값 타입을 잡았구나"*가 보인다. 5.7까지 오면 그 단계다.

### 재귀의 한계 — TS는 *깊이 제한*이 있다

재귀 조건부 타입은 무한히 깊어질 수 없다. TS 컴파일러는 *재귀 깊이 제한*을 걸어둔다(약 50단계). 그 이상으로 가면 *"Type instantiation is excessively deep and possibly infinite"* 에러가 난다.

이건 *기능의 한계가 아니라 안전장치*다. 타입 시스템은 *결정 가능*해야 하니까. 깊은 트리를 다뤄야 한다면 깊이를 *명시적 카운터*로 제한하는 패턴이 정착해 있다.

```ts
type DeepReadonly<T, Depth extends number = 5> =
  Depth extends 0
    ? T
    : { readonly [K in keyof T]: T[K] extends object
        ? DeepReadonly<T[K], Decrement<Depth>>
        : T[K] };
```

이런 자리는 곡예에 가까우니 *현실 코드에서는 거의 안 본다*. 재귀를 쓸 때는 *얕은 깊이로 충분한 자리*에서만 쓰는 편이 낫다 — 라이브러리 설계자가 아니라면 직접 만들 일도 거의 없다. *기억해두자.*

## 5.8 현실 마법의 분해 — zod·Hono·Prisma·tRPC

부품이 다 모였다. 이제 *우리가 매일 보는 코드*를 분해해보자. 5장의 클라이맥스다.

### zod — `z.infer<typeof Schema>`의 부품

처음에 봤던 코드를 다시 본다.

```ts
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().nonnegative(),
});

type User = z.infer<typeof UserSchema>;
// { id: string; email: string; age: number }
```

부품을 하나씩 분해해보자.

**부품 1: 스키마는 *값*이다.** `z.object({...})`는 일반 함수 호출이다. 결과는 *런타임 객체* — `parse()`, `safeParse()` 같은 메서드를 가진 객체다.

**부품 2: 그 객체의 *타입*을 `typeof`로 끌어낸다.** `typeof UserSchema`는 *그 객체의 컴파일타임 모양*을 잡는다. zod 내부적으로 이 타입은 대략 이런 모양이다(아주 단순화한 형태다).

```ts
type ZodObject<Shape> = {
  parse: (input: unknown) => OutputOf<Shape>;
  // ... 그 외 메서드들
};
```

여기서 핵심은 — `ZodObject`가 자기가 *어떤 모양의 객체*를 검증하는지를 *타입 매개변수 `Shape`으로 들고 있다*는 것. 그 정보가 컴파일타임에 살아 있다.

**부품 3: `z.infer<T>`로 그 안의 *출력 타입*을 꺼낸다.** zod의 `infer`는 (대략) 이런 모양이다.

```ts
namespace z {
  type infer<T> = T extends ZodType<infer Output> ? Output : never;
}
```

조건부 타입 + `infer`다. `T`(우리 경우 `typeof UserSchema`)가 `ZodType<...>` 모양이면, 그 *내부의 출력 타입*을 잡아서 돌려준다. 5.5에서 본 패턴 그대로다.

세 부품을 합치면 — *값 → typeof로 타입 추출 → infer로 안쪽 타입 잡기*. 이게 zod의 *마법이 아니라 부품 조합*이다.

조금 더 깊이 들어가보자. zod는 매핑 타입까지 동원한다.

```ts
// 단순화한 zod의 내부
type InferShape<S> = {
  [K in keyof S]: S[K] extends ZodType<infer Out> ? Out : never;
};

const schema = z.object({
  id: z.string(),    // ZodString → ZodType<string>
  age: z.number(),   // ZodNumber → ZodType<number>
});

// InferShape<{ id: ZodString; age: ZodNumber }>
// = { id: string; age: number }
```

매핑 타입(`[K in keyof S]`)으로 객체의 각 필드를 순회하고, 조건부 타입과 `infer`로 *각 필드의 zod 타입에서 출력 타입을 끌어낸다*. 한 단계씩 보면 *5.3 + 5.4 + 5.5의 합*이다. 곡예가 아니다.

이제 *왜 zod의 인기가 폭발적이었는지*가 보인다. *값과 타입을 같은 정의에서 끌어낸다*는 패턴은 자바의 Bean Validation으로는 어림도 없는 표현력이다. 한 번 정의하면 컴파일타임 타입과 런타임 검증이 *같이* 따라온다.

### Hono — 라우트 → RPC 클라이언트의 부품

Hono의 마법을 보자.

```ts
// 서버
const app = new Hono()
  .get("/users/:id", (c) => {
    const id = c.req.param("id");
    return c.json({ id, name: "Toby" });
  });

export type AppType = typeof app;
```

```ts
// 클라이언트
import { hc } from "hono/client";
import type { AppType } from "../server";

const client = hc<AppType>("http://localhost:3000");

const res = await client.users[":id"].$get({ param: { id: "1" } });
const data = await res.json();
// data: { id: string; name: string }   ← 자동 추론
```

서버에서 한 일이라곤 *라우트 정의*뿐이다. 클라이언트는 그 라우트를 *원격 함수처럼 호출*하는데, 인자와 반환 타입이 정확히 맞아 들어간다. *"이게 어떻게 되지?"*

부품을 분해하자.

**부품 1: `Hono` 클래스가 자기 *라우트 정보를 타입 매개변수에 누적*한다.** Hono의 `.get()`, `.post()` 같은 메서드는 호출할 때마다 *반환 타입에 자기를 추가한 새 Hono를 돌려준다*. 단순화하면 이런 모양이다.

```ts
class Hono<Routes = {}> {
  get<Path extends string, Handler>(
    path: Path,
    handler: Handler,
  ): Hono<Routes & { [K in Path]: { get: { response: ReturnType<Handler> } } }> {
    // ...
  }
}
```

매번 새 Hono를 돌려줄 때 *제네릭 매개변수에 라우트 정보를 누적*한다. 메서드 체이닝(`.get().post().put()`)이 끝나면 결과 Hono는 *모든 라우트의 타입 정보*를 자기 안에 들고 있다.

**부품 2: `typeof app`으로 그 누적된 정보를 *통째로 추출*한다.** 5.2에서 본 그 `typeof`다. 이걸 `AppType`이라는 이름으로 export하면 *서버의 라우트 정보*가 *순수 타입*으로 클라이언트에 전달된다.

**부품 3: `hc<AppType>()`이 그 정보로 *프록시 클라이언트*를 만든다.** 클라이언트 쪽 `hc`는 런타임에는 `Proxy` 객체이고, 컴파일타임에는 `AppType`의 *모양을 그대로 따라가는* 타입 함수다. 매핑 타입으로 라우트 키를 순회하고, 각 라우트의 `request`/`response` 타입을 *조건부 + infer*로 끌어낸다.

부품 셋이 합쳐지면 — *서버에서 정의한 라우트의 타입이 클라이언트에 그대로 흐른다*. *런타임 코드 생성도, 빌드 단계의 codegen도 없다*. 순수 타입 시스템 안에서 일어나는 일이다.

이 패턴이 가능한 *근본 이유*가 두 가지다.

첫째, **TS의 타입 시스템이 *튜링 완전*에 가깝다**(공식적으로는 sound가 아니지만 충분히 강력하다). 임의의 변형을 타입 수준에서 표현할 수 있다.

둘째, **TS는 라이브러리 작성자가 *프레임워크 수준의 마법*을 만들 수 있게 설계되었다**. 자바였다면 annotation processor + 코드 생성으로 풀어야 했을 일이 *타입만으로* 가능하다.

### Prisma — 생성된 타입의 형태

Prisma는 조금 다른 자리에 있다 — *codegen*을 쓴다.

```prisma
// schema.prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
}
```

`prisma generate`를 돌리면 `node_modules/.prisma/client/`에 자동 생성된 TS 파일들이 만들어진다. 그 안에 이런 타입들이 들어 있다(아주 단순화한 형태).

```ts
type User = {
  id: number;
  email: string;
  name: string | null;
};

type UserCreateInput = Omit<User, "id"> & {
  // id는 autoincrement이므로 입력에서 제외
};

type UserWhereInput = {
  id?: IntFilter | number;
  email?: StringFilter | string;
  name?: StringNullableFilter | string | null;
};

type UserDelegate = {
  findUnique<T extends UserFindUniqueArgs>(args: T): Promise<...>;
  findMany<T extends UserFindManyArgs>(args: T): Promise<...>;
  // ...
};
```

여기서 흥미로운 자리는 — Prisma가 *타입을 100% 코드 생성*으로 만들지만, 그 *생성된 타입의 모양*이 우리가 5장에서 본 도구의 합이라는 점. `Omit`, 매핑 타입(`Partial`-like 변환), 조건부 타입(`Filter` 변형), `infer`(`include`/`select`로 결과 모양을 좁히는 자리) — 다 들어 있다.

특히 `select`/`include`의 마법이 인상적이다.

```ts
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: { id: true, email: true },
});
// user: { id: number; email: string } | null
//                                       ^^ name이 없다
```

`select`로 골라낸 필드만 *결과 타입에 포함*된다. 이건 `select` 객체의 키를 *조건부 + 매핑 타입*으로 다시 잡아내는 도구가 Prisma 안에 들어 있다는 뜻이다. 단순화하면 이런 모양이다.

```ts
type SelectResult<Model, Select> = {
  [K in keyof Select & keyof Model as Select[K] extends true ? K : never]: Model[K];
};
```

매핑 타입의 key remapping(`as`) + 조건부 타입(`Select[K] extends true`)으로 *true로 고른 키만 결과에 포함*시킨다. 5.3과 5.4의 합이다.

### tRPC — procedure 타입의 추출

마지막으로 tRPC를 보자. Hono와 비슷하지만 *순수 함수 호출 모양*에 더 집중한다.

```ts
// 서버
import { initTRPC } from "@trpc/server";
import { z } from "zod";

const t = initTRPC.create();

const appRouter = t.router({
  user: {
    getById: t.procedure
      .input(z.object({ id: z.number() }))
      .query(({ input }) => {
        return { id: input.id, name: "Toby" };
      }),
  },
});

export type AppRouter = typeof appRouter;
```

```ts
// 클라이언트
import { createTRPCProxyClient } from "@trpc/client";
import type { AppRouter } from "../server";

const client = createTRPCProxyClient<AppRouter>({ /* ... */ });

const user = await client.user.getById.query({ id: 1 });
// user: { id: number; name: string }   ← 자동
```

부품은 Hono와 거의 같다.

- 서버에서 `appRouter`라는 *값*을 만들고
- `typeof appRouter`로 *타입을 추출해서* `AppRouter`로 export
- 클라이언트에서 `createTRPCProxyClient<AppRouter>`로 *그 모양을 따라가는 프록시*를 만든다

내부적으로는 router의 각 procedure에서 *`input`의 zod 스키마*에서 입력 타입을, *`query`/`mutation`의 반환값*에서 출력 타입을 추출한다. 5.5의 `infer`가 정확히 그 자리에서 일한다.

```ts
// 단순화한 tRPC 내부
type ProcedureInput<P> = P extends { _input: infer I } ? I : never;
type ProcedureOutput<P> = P extends { _output: infer O } ? O : never;
```

여기까지 분해하고 나면 *"아, 이게 마법이 아니라 부품 조합이구나"*가 손에 잡힌다. zod·Hono·Prisma·tRPC가 각자 다른 모양으로 같은 도구를 쓴다. 매핑 + 조건부 + `infer` + 템플릿 리터럴. 5.1부터 차근차근 올라온 부품들이다.

이 직관 하나만 남기자. *현실 코드의 마법은 부품의 조합이지 새 마법이 아니다.* 다음에 처음 보는 라이브러리를 만나서 *"이게 어떻게 되지?"* 싶을 때, 그 안에 매핑 타입이 있는지, 조건부 + infer가 있는지, 템플릿 리터럴이 있는지를 의심해보자. *대부분 답이 거기 있다.*

## 5.9 `as`의 윤리 — 쓰지 않고 끝내는 6가지 길

5장의 호흡을 잠시 바꾸자. 도구 이야기를 이어가다가, 한 자리에서 *우리가 매일 마주치는 유혹*에 대해 솔직하게 이야기하고 싶다. *타입 단언(`as`)*이다.

```ts
const data = await fetch("/api/user").then((r) => r.json()) as User;
```

이 한 줄이 *왜* 찜찜한가?

`fetch().json()`의 반환 타입은 `Promise<any>`다. 그걸 `as User`로 *그냥 단언*하면 컴파일러는 입을 다문다 — *"네가 User라고 했으니 User로 알겠다"*. 그런데 런타임에 진짜 `User` 모양이 올지는 *아무도 모른다*. API가 어제까지 `name`을 주다가 오늘부터 `fullName`을 주기로 바꿨을 수도 있다. 컴파일러는 모른다. 거짓말 위에 빌드된 빌딩 같은 자리다.

그래서 커뮤니티에는 *"`as`는 거짓말이다"*라는 강한 입장이 있고, *"필요할 땐 써야 한다"*는 절충 입장이 있다. 둘 다 일리가 있다. 5장의 입장은 *중간*이다. **`as`를 쓰면 죄짓는 건 아니지만, 안 쓸 수 있다면 안 쓰는 편이 낫다.** 그 *안 쓰는 길*을 먼저 보고, 그래도 *써야 하는 자리* 셋을 짚자.

### 안 쓰고 끝내는 6가지 길

**길 1: 사용자 정의 type predicate.** 4장에서 본 도구다. *"이 값이 이 타입인지 확인하는 함수를 만들고 그 결과를 컴파일러가 신뢰하게 한다"*.

```ts
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

const data = await fetch("/api/user").then((r) => r.json());
if (isUser(data)) {
  // data: User
}
```

`as`를 *런타임 검증으로 대체*했다. 검증 함수를 한 번 만들어두면 어디서든 재사용한다. *번거롭다*고 느낄 수 있는데, 그 번거로움이 사실은 *타입 시스템이 보장하지 못하는 자리를 명시*하는 안전장치다.

**길 2: 런타임 스키마(zod·valibot).** 5.8에서 본 자리다. type predicate를 손으로 적는 대신 스키마로 적고, 검증과 타입 추출을 한 객체로 묶는다.

```ts
const User = z.object({ id: z.number(), name: z.string() });

const data = User.parse(await fetch("/api/user").then((r) => r.json()));
// data: User (검증 통과한 결과)
```

`as`가 사라졌다. 외부 입력의 *경계*에서 zod로 검증하면 내부 코드는 *타입을 신뢰*해도 된다. 커뮤니티 합의가 정착한 *boundary validation* 패턴이다.

**길 3: 제네릭으로 흘려 보내기.** *"내가 알아야 하는 타입"*이 아니라 *"호출자가 정해줄 타입"*이라면 제네릭으로 받는 게 낫다.

```ts
// Bad
function unwrap(promise: Promise<unknown>): User {
  return promise as unknown as User;
}

// Good
async function unwrap<T>(promise: Promise<T>): Promise<T> {
  return await promise;
}
```

타입을 *결정하는 책임*을 호출자에게 넘긴다. 함수 본체는 *어떤 타입이 올지 알 필요가 없다*. `as`가 *모름을 숨기는* 도구라면, 제네릭은 *모름을 정직하게 표현하는* 도구다.

**길 4: discriminated union으로 좁히기.** 4장에서 본 분별 유니온을 다시 떠올리자. *"이 값이 어떤 종류인지 `kind` 필드로 표시"*해두면 컴파일러가 자동으로 좁힌다.

```ts
type ApiResult =
  | { kind: "success"; data: User }
  | { kind: "error"; message: string };

function handle(result: ApiResult) {
  if (result.kind === "success") {
    result.data.name;  // OK — User로 좁혀짐
  } else {
    result.message;    // OK — error로 좁혀짐
  }
}
```

`as`로 *어느 분기인지 단언*하지 않아도 된다. 분기 자체가 자기 타입을 *선언*한다.

**길 5: `satisfies` 연산자(TS 4.9+).** 4장에서 본 *"타입을 좁히지 않으면서 만족 여부만 검사하는"* 도구다.

```ts
// Bad
const config = {
  apiUrl: "https://...",
  timeout: 5000,
} as Config;
// config의 구체 타입이 Config로 *넓어진다* (apiUrl: string으로)

// Good
const config = {
  apiUrl: "https://...",
  timeout: 5000,
} satisfies Config;
// config의 타입은 그대로 유지되면서, Config 모양인지 *검사만* 한다
```

`as`가 *넓힘*이라면 `satisfies`는 *검사*다. 리터럴 타입을 잃지 않으면서 호환성만 확인한다. *익혀두면 `as`의 70%를 대체할 수 있다.*

**길 6: 함수 시그니처 다시 보기.** 가장 자주 놓치는 자리다. *"왜 여기서 `as`를 써야 했지?"*를 거꾸로 물어보면, 사실은 *함수 시그니처가 너무 좁거나 너무 넓다*는 답이 나오는 경우가 많다. 시그니처를 다시 잡으면 `as`가 사라진다.

```ts
// Bad
function process(input: unknown) {
  const user = input as User;  // 매번 단언
  // ...
}
const user1 = process(data);  // 호출자도 결과 타입을 모름

// Good
function process<T extends User>(input: T): T {
  // ...
}
const user1 = process(data);  // 호출자가 정확한 타입을 받음
```

타입 설계 한 번에 `as` 다섯 개가 사라진다. *번거로워 보이지만 한 번이다.*

### 그래도 `as`가 필요한 3가지 자리

이 *6가지 길*을 다 시도해도 `as`를 써야 하는 자리가 있다. 셋이다.

**자리 1: 컴파일러가 *추론할 수 없는 형변환*.** 가령 *유니온의 한 분기를 강제로 좁혀야 하는데 좁힐 정보가 코드에 없는* 자리.

```ts
const button = document.querySelector(".submit") as HTMLButtonElement;
button.disabled = true;
```

`querySelector`의 반환 타입은 `Element | null`이다. *우리는 `.submit`이 button임을 알지만 컴파일러는 모른다*. 이런 자리는 솔직하게 `as`로 표시한다. 다만 한 번 더 살펴보자 — `instanceof HTMLButtonElement`로 *체크 후 좁히는 길*이 더 안전한 경우가 많다.

**자리 2: 타입 시스템의 *표현 한계*를 만났을 때.** 라이브러리 작성자라면 가끔 마주치는 자리다. *복잡한 매핑 타입의 결과가 컴파일러에는 너무 일반적으로 잡혀서, 안다는 사실을 단언으로 표시*해야 할 때.

```ts
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;  // 빈 객체에서 시작
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}
```

빈 객체 `{}`는 `Pick<T, K>`가 *아니다*. 우리가 *루프를 다 돌면 그 모양이 된다*는 걸 알지만, 컴파일러는 따라오지 못한다. 이런 자리에서 `as`는 *프로그래머가 책임지는 작은 거짓말*이다. 함수가 작고 검증 가능한 범위에서만 쓰자.

**자리 3: 마이그레이션 중인 *임시 자리*.** 9장에서 다룰 자바스크립트 → 타입스크립트 마이그레이션 도중에는 *모든 자리를 한 번에 정확히 잡을 수 없다*. 임시로 `as`를 쓰고 *주석으로 TODO*를 남긴 뒤, 다음 PR에서 풀어내는 패턴이 합리적이다.

```ts
// TODO: replace with zod schema before v2 release
const user = legacyData as User;
```

*"`as`를 쓰는 것 자체가 죄"*는 아니다. *"왜 썼는지를 설명할 수 있는가, 안 쓸 길을 충분히 시도했는가"*가 기준이다.

> ### 💡 작가의 한 마디 — `as unknown as X`를 줄이는 다섯 가지 길
>
> *`as unknown as X`*. 한 번이라도 손가락이 이 모양으로 움직여본 적 있다면 알 것이다. *컴파일러가 `as X`를 막을 때 `unknown`을 거쳐가는 우회로*다. 두 번 캐스팅하면 컴파일러는 입을 다문다 — *"네가 그렇게까지 말한다면 어쩔 수 없다"*. 절대 그게 *허락*은 아니다. *"코드를 통과시키되 너의 책임"*이라는 *마지막 경고*다.
>
> 이걸 줄이는 다섯 가지 길을 권하고 싶다.
>
> **첫째, 의심하자.** `as unknown as X`가 보이면 *2분만* 멈춰서 묻는다. *"이 자리에 진짜 X가 올 거라는 보장이 어디에 있나?"* 답이 *"내가 그냥 안다"*면 위험 신호다. 답이 *"위에서 zod로 검증했다"*면 안전하다.
>
> **둘째, 경계를 가능한 한 안쪽으로 옮기자.** 외부 입력이 들어오는 자리에서 *한 번* 검증하고, 그 안쪽 코드는 타입을 *신뢰*한다. `as`가 *경계 한 자리*에만 모이면 감당 가능한 위험이 된다. 코드 곳곳에 흩어져 있다면 *어디서 거짓말이 시작됐는지* 알 수 없다.
>
> **셋째, 라이브러리의 타입 정의를 의심하자.** `@types/...`가 너무 넓게 잡혀 있어서 `as`가 필요해지는 경우가 자주 있다. 그런 자리는 *라이브러리에 PR을 보내거나*, 자기 프로젝트에 *type augmentation*(5.10에서 다룬다)으로 좁힌다. *"내 코드가 잘못한 게 아니라 타입 정의가 부족한 거였구나"*가 답인 경우가 의외로 많다.
>
> **넷째, 큰 함수를 쪼개자.** 한 함수에서 `as`가 두 번 이상 나오면 *함수가 너무 많은 일을 한다*는 신호다. 책임을 나누면 각 작은 함수가 *명확한 입출력 타입*을 가지게 되고, 거짓말이 사라진다.
>
> **다섯째, *나중*을 신뢰하지 말자.** *"일단 `as`로 통과시키고 나중에 고쳐야지"*라고 적은 코드는, *나중에 고치지 않는다*. 실험으로 증명된 바가 있다(농담이지만 진짜다). `// TODO: fix this`가 영원히 남는 자리들. *지금* 작은 시도를 한 번 더 해보는 편이 낫다.
>
> *`as`는 도구다.* 도구를 잘 쓴다는 건 *언제 쓰지 않을지를 안다*는 뜻이다. TS의 타입 시스템이 강력해진 만큼, *`as` 없이 끝나는 자리*가 매년 넓어지고 있다. 그 흐름을 타자.

## 5.10 declaration merging과 module augmentation — Express의 `Request.user`

마지막 절이다. *현실에서 가장 자주 보는* 자리 하나를 짚고 챕터를 닫자. **선언 병합(declaration merging)**과 **모듈 보강(module augmentation)**이다.

자바·코틀린에는 이런 개념이 없다. *"같은 이름의 타입을 두 곳에 적으면 컴파일러가 합쳐준다"*는 발상이 어색할 수 있다. 그런데 TS는 *이게 된다*. JS의 동적 본성과 TS의 타입 시스템을 잇는 자리에서 합리적이기도 하다.

### 단순한 declaration merging

```ts
interface User {
  id: number;
  name: string;
}

interface User {
  email: string;
}

// 합쳐진 결과
// interface User { id: number; name: string; email: string }
```

같은 이름의 `interface`를 두 번 적으면 *합쳐진다*. `type`은 안 된다 — `type`은 별칭이지 선언이 아니라서.

자체로는 큰 의미가 없어 보이지만, 이게 *모듈 경계를 넘어서 작동*한다는 게 실전에서 중요하다.

### module augmentation — *남의 모듈*을 확장한다

Express에서 가장 자주 보는 자리다. Express의 `Request` 객체에 *우리가 만든 미들웨어가 추가한 필드*를 타입으로 표현하고 싶다고 해보자.

```ts
// auth.middleware.ts
app.use((req, res, next) => {
  req.user = { id: 1, name: "Toby" };  // 미들웨어가 user를 붙임
  next();
});

// 라우트
app.get("/me", (req, res) => {
  res.json(req.user);  // 컴파일 에러 — req.user가 타입에 없음
});
```

미들웨어가 런타임에 `req.user`를 *붙이는* 건 자유다. JS는 그걸 막지 않는다. 하지만 TS는 *Express의 `Request` 타입*에 `user` 필드가 없다는 것을 안다. 그래서 컴파일 에러가 난다.

이걸 해결하는 *나쁜 방법*은 매번 `(req as RequestWithUser).user`로 캐스팅하는 것이다. 5.9에서 본 바로 그 *피해야 할 자리*다.

*좋은 방법*이 module augmentation이다.

```ts
// types/express.d.ts
import "express";

declare module "express" {
  interface Request {
    user?: { id: number; name: string };
  }
}
```

이 한 파일을 프로젝트 어딘가에 두면, *Express의 `Request` 타입에 `user` 필드가 추가된다*. 합쳐진다. 코드는 자연스럽게 돌아간다.

```ts
app.get("/me", (req, res) => {
  res.json(req.user);  // OK — req.user는 { id: number; name: string } | undefined
});
```

이게 자바·코틀린에는 없는 자리다. 자바였다면 `Request`를 *상속한 새 클래스*를 만들거나, request에 *attribute로 넣고 키로 꺼내거나*(`request.getAttribute("user")`), 아예 *별도의 컨텍스트 객체*를 들고 다녀야 한다. TS는 *원래 타입을 그 자리에서 확장*한다.

### 흔한 실전 패턴들

module augmentation이 자주 쓰이는 자리는 의외로 많다.

**환경변수 타입.** `process.env`를 타입 안전하게 만들고 싶을 때.

```ts
// types/env.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      DATABASE_URL: string;
      JWT_SECRET: string;
      NODE_ENV: "development" | "production" | "test";
    }
  }
}
```

이제 `process.env.DATABASE_URL`이 `string | undefined`가 아니라 그냥 `string`으로 잡힌다. *zod로 한 번 검증한 뒤* 이런 augmentation을 두는 패턴이 흔하다.

**Vite의 `import.meta.env`** 같은 자리도 같은 패턴.

```ts
// vite-env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

**Window 확장.** 글로벌 객체에 라이브러리가 자기를 붙이는 경우가 있다(예: 분석 SDK).

```ts
declare global {
  interface Window {
    gtag: (event: string, ...args: unknown[]) => void;
  }
}
```

각 자리에서 공통점을 보자 — *남이 만든 타입에 우리가 필요한 모양을 덧붙인다*. 자바스크립트의 *open-by-default*한 동적 본성에 *닫힌 타입 시스템*이 적응한 결과다.

### 주의할 자리 — 너무 자주 쓰면 *글로벌 오염*이 된다

module augmentation은 *글로벌 효과*가 있다. 한 곳에서 `Request`에 `user`를 추가하면 프로젝트 전체에서 그 모양이 보인다. 편하지만, *남용하면 어디서 누가 어떤 필드를 추가했는지 추적이 어려워진다*. 끔찍한 일이다.

권장 패턴은 두 가지다.

- **augmentation을 *한 파일에 모은다*.** `types/global.d.ts`나 `types/express.d.ts` 같은 *지정된 자리*에서만 한다. 흩어지지 않게.
- **꼭 필요한 자리에만 쓴다.** 프레임워크가 *진짜로* 동적으로 필드를 붙이는 자리(미들웨어가 추가하는 `req.user` 같은 것)에서만 쓴다. *그냥 새 타입을 만들면 되는 자리*에서는 쓰지 않는다.

이 두 원칙만 지키면 declaration merging은 *현실 코드의 거친 자리*를 매끄럽게 만드는 좋은 도구다.

## 5.11 마무리

5장은 길었다. *깊이*가 약속이었으니 어쩔 수 없다.

지금까지 부품을 하나씩 쌓았다. 제네릭과 제약 → `keyof`/`typeof`/`T[K]`의 합주 → 매핑 타입 → 조건부 타입 → `infer` → 템플릿 리터럴 → 재귀. 그 위에서 zod·Hono·Prisma·tRPC를 분해했다. *현실 코드의 마법은 부품의 조합이지 새 마법이 아니다.* 이게 5장의 한 문장 약속이다.

기억해두자. *제네릭은 함수다*. 입력 타입을 받아서 출력 타입을 돌려주는 함수. 매핑 타입은 *타입 수준의 for 루프*고, 조건부 타입은 *if*고, `infer`는 *패턴 매칭으로 변수에 잡기*다. 이 직관 셋만 남기면 5장의 모든 도구가 한 자리에 정렬된다.

`as`의 윤리 한 절도 함께 기억하자. *쓰면 죄짓는 건 아니지만, 안 쓸 수 있다면 안 쓰는 편이 낫다.* 6가지 길이 있고, 그래도 써야 하는 3가지 자리가 있다. *경계에 모으고, 내부는 신뢰하자.*

declaration merging은 자바·코틀린에 없는 자리지만, *Express·Vite·Node*의 현실 코드를 매끄럽게 만드는 좋은 도구다. 한 파일에 모으고, 꼭 필요할 때만 쓰자.

다음 6장에서는 이 부품들을 *도메인 모델링*에 쓰는 패턴을 본다. branded type·`interface` vs `type`·immutability·*에러를 도메인의 일부로*. 5장이 *부품 사전*이었다면 6장은 *그 부품으로 자기 도메인을 어떻게 표현할까*의 자리다. 결을 잃지 않는 도메인 모델링이라는 약속을 6장이 이어받는다.

> ### 📖 더 깊이 가려면
>
> - **공식 핸드북** — *TypeScript Handbook*의 *Type Manipulation* 섹션 (Generics, Keyof Type Operator, Typeof Type Operator, Indexed Access Types, Conditional Types, Mapped Types, Template Literal Types). 5장의 모든 도구가 1차 자료로 정리되어 있다.
> - **Matt Pocock의 *Total TypeScript*** — *Type Transformations* 워크숍이 5장의 도구를 *문제 풀이로* 익히는 데 가장 효과적인 자료다. 한국어 번역도 일부 있다.
> - **이펙티브 타입스크립트 (Dan Vanderkam)** — *Item 14~22* 가 제네릭과 매핑 타입의 실전 패턴, *Item 27~28*이 `as`와 type guard의 윤리. 한국어 번역본 인사이트 시리즈로 출간.
> - **zod 공식 문서의 *"From Schema to TypeScript"*** — `z.infer<typeof Schema>`의 내부 동작을 라이브러리 작성자 시선에서 정리한 자료. 5.8의 zod 분해를 직접 따라가볼 수 있다.
> - **Hono의 *RPC* 가이드** — Hono의 *type-safe client*가 어떻게 만들어지는지 공식 문서가 단계별로 보여준다. 5.8의 Hono 분해와 짝을 이룬다.
> - **→ 14장에서 `expect-type`으로 *타입 자체를 단위 테스트*하는 패턴을 다룬다.** 5장에서 만든 도구들이 *진짜로 우리가 의도한 모양*을 만들어내는지 *런타임 없이 검증*하는 자리다. 라이브러리 작성자뿐 아니라 큰 프로젝트의 도메인 타입을 다루는 사람도 익혀둘 가치가 있다.

---

> 5장에서 타입이 타입을 만드는 부품들을 손에 넣었다. 이제 그 부품들을 실제 도메인 모델링에 써보자. 구조적 타입 시스템이 가져오는 헐거움 — `UserId`와 `OrderId`가 모두 `string`이라서 섞여도 컴파일러가 침묵한다 — 을 도메인의 결에 맞춰 봉합하는 표준 패턴들이 6장에서 기다린다.

# 6장. 이 도메인을 어떻게 모델링할까 — 구조적 타입 위에서 잃지 않는 법

Java 백엔드를 몇 년 짠 사람이 처음으로 TypeScript 코드베이스에 들어왔다고 상상해보자. 코드를 읽다가 뭔가 찜찜한 순간이 온다.

```ts
function createOrder(userId: string, productId: string, amount: number) {
  // ...
}
```

Java였다면 `UserId`, `ProductId`라는 별도 타입이 있거나, 적어도 `@NotNull @Size(min=36, max=36) String userId`처럼 Bean Validation이 붙어 있었을 것이다. 그런데 TS 코드에는 그냥 `string`이다. *"이게 맞나? 실수로 userId 자리에 productId를 넣으면 어떻게 되지?"*

더 난감한 건 다음을 발견했을 때다.

```ts
const userId = getUserId();
const productId = getProductId();

// 아무도 에러를 안 낸다
createOrder(productId, userId, 100);
```

컴파일러는 침묵한다. `string`과 `string`은 호환된다. 도메인의 안전망이 그냥 뚫려 있다.

이건 TS의 결함이 아니다. **구조적 타입 시스템**이 가져오는 필연적인 헐거움이다. Java가 명목 타입으로 이것을 막는다면, TS는 다른 방법으로 막아야 한다. 그리고 그 방법은 존재한다 — 커뮤니티가 수년에 걸쳐 정착시킨 표준 패턴들이 있다.

이 장에서 살펴볼 것들은 사실 모두 한 주제로 연결된다. **"TS의 구조적 타입 위에서 도메인 안전성을 어떻게 회복하는가."** `interface`와 `type`의 선택, branded type, enum 대신 union literal, immutability 전략 — 이 모든 것이 같은 질문에 대한 답이다. 그리고 마지막에는 그 질문의 가장 중요한 변주를 다룬다. **"에러를 도메인의 일부로 모델링할 수 있는가."** Java에서 checked exception을 통해 해결하려 했던 그것을, TS에서는 어떻게 접근하는지.

---

## 6.1 데이터 구조를 표현하는 두 도구 — `interface`와 `type alias`

도메인 모델링의 첫 번째 질문은 단순하다. 데이터 구조를 어떻게 표현할 것인가.

Java라면 `class`가 있다. Kotlin이라면 `data class`가 있다. TS에는 두 가지가 있다. `interface`와 `type alias`. 그리고 둘 다 있다고 해서 어느 것을 써야 하는지 명확한 합의가 있는 건 아니라서, 처음에 조금 당황스럽다.

### interface — 객체의 형태를 선언한다

```ts
interface User {
  id: string;
  email: string;
  name: string;
}

interface Order {
  id: string;
  userId: string;
  amount: number;
  createdAt: Date;
}
```

자연스럽다. Java의 인터페이스와 비슷하게 생겼고, 객체의 *형태(shape)*를 선언한다. TS에서 `interface`는 주로 이 용도다.

### type alias — 타입에 이름을 붙인다

```ts
type UserId = string;
type Status = "pending" | "fulfilled" | "cancelled";
type Point = { x: number; y: number };
type MaybeUser = User | null;
```

`type`은 어떤 타입 표현식에도 이름을 붙일 수 있다. primitive, union, intersection, 함수 타입, 튜플 타입 — 모두 `type`으로 이름을 붙일 수 있다. `interface`는 그렇지 않다. `interface Status = "pending" | "fulfilled"`는 문법 에러다.

### 둘의 차이 — 가장 중요한 것들만

`interface`와 `type`의 차이를 낱낱이 비교하다 보면 지치기 쉽다. 실무에서 정말 중요한 차이 두 가지만 짚어보자.

**첫째, `type`은 union과 intersection을 직접 표현할 수 있고 `interface`는 아니다.**

```ts
// type만 가능
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
type Shape = Circle | Square | Triangle;
```

**둘째, `interface`는 선언 병합(declaration merging)이 된다.**

```ts
interface Config {
  host: string;
}

// 나중에 같은 이름으로 다시 선언하면 합쳐진다
interface Config {
  port: number;
}

// Config는 이제 { host: string; port: number }
const config: Config = { host: "localhost", port: 3000 };
```

이게 `interface`의 독특한 능력이다. 라이브러리를 *보강(augment)*할 때 쓴다. Express의 `Request` 타입에 `currentUser` 속성을 추가하고 싶다면, `interface`로 그것을 선언하면 자동으로 병합된다. `type`으로는 이걸 할 수 없다.

### 그렇다면 언제 무엇을 쓸까

커뮤니티에서 오래 논쟁이 있었다. 결론은 생각보다 실용적이다.

- **객체 형태를 표현할 때**: 어느 것이든 동작한다. 팀의 스타일을 따르면 된다.
- **union, intersection, 함수 타입에 이름을 붙일 때**: `type`만 가능하니 `type`을 쓴다.
- **라이브러리 확장(augmentation)**: `interface`를 써야 한다.
- **React 컴포넌트 Props, 함수 인자**: `interface`를 쓰는 팀이 많다. 선언 병합 덕분에 나중에 보강하기 쉽다.
- **도메인 모델의 복잡한 대수적 타입**: `type`이 자연스럽다.

"그러니까 뭘 써야 해요?" 라고 묻는다면, 솔직히 말해서 실무에서 그 차이가 문제가 될 일은 생각보다 드물다. 중요한 건 팀 안에서 일관성이다. "객체 형태는 `interface`, 그 외에는 `type`" 이라는 규칙을 정해두면 대부분의 상황이 해결된다.

가끔 처음 TS를 접한 팀에서 "우리 팀은 `interface`만 쓰기로 했어요"라든가 "저희는 `type`으로 통일했어요" 같은 이야기를 한다. 그것도 나쁘지 않다. 하지만 `interface`만 쓰기로 했다면 union을 표현할 때 조금 어색해진다. 예를 들어 `interface Shape`를 만들고 싶은데 `Circle | Square` 형태를 `interface`로는 직접 표현할 수 없어서, 결국 `type`을 꺼내 들게 된다.

한 가지 덧붙이자면, TypeScript 공식 핸드북은 오랫동안 "가능하면 `interface`를 쓰고, 필요한 경우에만 `type`을 써라"는 권고를 유지했다. 그 이유는 IDE의 에러 메시지 표현에서 `interface`가 더 읽기 좋았기 때문이다. 최근 버전에서는 이 차이가 많이 좁혀졌지만, 레거시 코드베이스에서 이 권고를 따른 흔적을 자주 보게 된다. 맥락을 알면 낯설지 않다.

물론 `interface`와 `type`을 *동시에* 쓸 수도 있다. 겁낼 필요 없다. 실제 코드에서는 둘이 섞여 있는 경우가 더 많다.

```ts
interface UserBase {
  id: string;
  email: string;
}

type AdminUser = UserBase & {
  role: "admin";
  permissions: string[];
};

type RegularUser = UserBase & {
  role: "user";
};

type User = AdminUser | RegularUser;
```

`interface`로 기반을 정의하고, `type`으로 변형·조합하는 패턴이다. 두 개가 사이좋게 공존한다.

---

> **📚 Java/Kotlin 시선 — `data class`/`copy()` ↔ TS `interface` + spread**
>
> Kotlin의 `data class`는 도메인 모델링의 핵심이다. 불변 필드, 자동 생성되는 `equals`/`hashCode`/`toString`, 그리고 `copy()`가 있다.
>
> ```kotlin
> data class User(val id: String, val email: String, val name: String)
>
> val user = User("u1", "alice@example.com", "Alice")
> val updated = user.copy(name = "Alicia")
> ```
>
> TS에는 이에 정확히 대응하는 것이 없다. `interface`는 구조만 선언한다. `equals`는 TS/JS에서 `===`가 참조 동등성이라 객체끼리는 직접 비교가 안 된다. `copy()`는 spread로 흉내 낸다.
>
> ```ts
> interface User {
>   id: string;
>   email: string;
>   name: string;
> }
>
> const user: User = { id: "u1", email: "alice@example.com", name: "Alice" };
> const updated: User = { ...user, name: "Alicia" };
> ```
>
> Kotlin의 `copy()`와 거의 같다. 단, 컴파일러가 강제하지 않는다. `{ ...user, nonExistentField: "x" }` 도 에러 없이 동작한다(초과 속성 검사는 리터럴 할당 시점에만 작동). `equals`에 해당하는 깊은 비교가 필요하면 `deep-equal` 같은 라이브러리를 따로 쓰거나, 직접 구현해야 한다.
>
> **결론**: TS의 `interface` + spread가 `data class`의 *흉내*는 낼 수 있지만, 컴파일러 수준의 강제력은 훨씬 약하다. 이것이 TS 도메인 모델링이 Java/Kotlin보다 더 *규율*이 필요한 이유 중 하나다.

---

## 6.2 구조적 타입의 헐거움 — 왜 `type UserId = string`으로는 부족한가

다시 처음의 문제로 돌아오자.

```ts
type UserId = string;
type ProductId = string;

function createOrder(userId: UserId, productId: ProductId) { /* ... */ }

const uid: UserId = "user-123";
const pid: ProductId = "prod-456";

// 이게 통과된다
createOrder(pid, uid);  // userId에 ProductId를, productId에 UserId를 넣었다
```

`type UserId = string`은 그냥 `string`의 별명이다. TS는 구조적으로 호환 여부를 판단하는데, `string`과 `string`은 당연히 호환된다. `UserId`와 `ProductId`는 컴파일러 눈에 아무 차이가 없다.

Java라면 이것이 컴파일 에러다. `UserId`와 `ProductId`가 다른 클래스이기 때문이다. TS에서는 이런 명목 타입이 기본적으로 없다.

그렇다면 어떻게 해야 할까?

### Branded type — 구조적 타입 위에서 명목 타입을 흉내내다

커뮤니티가 수년에 걸쳐 정착시킨 패턴이 있다. **Branded type** 또는 **nominal trick**이라고 부른다.

```ts
type UserId = string & { readonly _brand: unique symbol };
type ProductId = string & { readonly _brand: unique symbol };
```

`unique symbol`이 핵심이다. TS에서 `unique symbol`은 선언마다 고유한 타입을 만든다. 두 `unique symbol`은 서로 다른 타입이다. 그래서 `UserId`와 `ProductId`는 구조적으로 *다른* 타입이 된다.

실제로 실험해보자.

```ts
declare const _userId: unique symbol;
declare const _productId: unique symbol;

type UserId = string & { readonly _brand: typeof _userId };
type ProductId = string & { readonly _brand: typeof _productId };

function createOrder(userId: UserId, productId: ProductId) {
  // ...
}

const uid = "user-123" as UserId;
const pid = "prod-456" as ProductId;

createOrder(uid, pid);   // OK
createOrder(pid, uid);   // 컴파일 에러! Type 'ProductId' is not assignable to type 'UserId'
```

이제 순서가 바뀌면 컴파일러가 잡아낸다.

### 더 짧고 실용적인 선언 방법

`declare const _userId: unique symbol`을 매번 쓰는 건 번거롭다. 더 일반적으로 쓰이는 패턴은 다음과 같다.

```ts
declare const brand: unique symbol;

type Brand<T, B> = T & { readonly [brand]: B };

type UserId = Brand<string, "UserId">;
type ProductId = Brand<string, "ProductId">;
type OrderId = Brand<string, "OrderId">;
type Amount = Brand<number, "Amount">;
```

`Brand<T, B>` 헬퍼 타입 하나로 모든 branded type을 만들 수 있다. `B` 자리에 문자열 리터럴을 넣어서 구분한다.

### Brand를 만드는 함수 — 생성 지점에서 검증

Branded type의 값을 만드려면 타입 단언(`as`)이 필요하다. 그냥 `"user-123" as UserId`라고 쓸 수 있지만, 이러면 아무 값이나 `UserId`로 만들 수 있어서 취지가 반감된다.

더 나은 방법은 생성 함수(constructor function)를 만드는 것이다.

```ts
function makeUserId(value: string): UserId {
  if (!value.startsWith("user-")) {
    throw new Error(`Invalid UserId: ${value}`);
  }
  return value as UserId;
}

function makeOrderAmount(value: number): Amount {
  if (value <= 0 || !Number.isFinite(value)) {
    throw new Error(`Invalid Amount: ${value}`);
  }
  return value as Amount;
}
```

이제 `UserId`를 만들려면 반드시 `makeUserId()`를 통해야 한다. 검증 없이 `"user-123" as UserId`라고 쓸 수는 있지만, 코드 리뷰에서 `as`는 주의 신호다 — 5장에서 다룬 `as`의 윤리가 여기서도 적용된다. 팀 컨벤션으로 "branded type 생성은 반드시 maker 함수를 거칠 것"이라고 정하면 된다.

### zod와의 결합

앞서 5장에서 봤듯이 zod는 스키마로부터 타입을 유도한다. branded type과 자연스럽게 결합된다.

```ts
import { z } from "zod";

const UserIdSchema = z.string().uuid().brand<"UserId">();
const ProductIdSchema = z.string().uuid().brand<"ProductId">();

type UserId = z.infer<typeof UserIdSchema>;
type ProductId = z.infer<typeof ProductIdSchema>;

// 외부 입력을 검증하면서 branded type을 만든다
function parseUserId(input: unknown): UserId {
  return UserIdSchema.parse(input);
}
```

`z.string().uuid().brand<"UserId">()`는 UUID 형식인지 검증하고, branded type으로 만들어 반환한다. 외부 경계에서 검증과 브랜딩이 동시에 이루어진다.

### Effect-ts와 토스의 사례

Effect-ts는 TS 생태계에서 가장 정교한 함수형 프레임워크 중 하나인데, 여기서도 branded type을 핵심 패턴으로 채택한다.

```ts
import { Brand } from "effect";

type UserId = string & Brand.Brand<"UserId">;
const UserId = Brand.nominal<UserId>();

const uid = UserId("user-123");  // 유효한 UserId 생성
```

토스(Viva Republica)도 내부적으로 비슷한 패턴을 쓴다. 금융 도메인에서 `UserId`, `AccountId`, `TransactionId` 같은 식별자가 뒤섞이는 건 실제로 버그를 유발하는 실수다. Branded type은 이것을 컴파일 타임에 막는다.

---

> **🚧 함정 — 구조적 타입의 헐렁함**
>
> `type UserId = string`이라고 선언하는 순간, TS 컴파일러 눈에 `UserId`와 `string`은 완전히 같다. 나아가 `type ProductId = string`도 선언하면 `UserId`와 `ProductId`도 서로 완전히 같다.
>
> ```ts
> type UserId = string;
> type ProductId = string;
>
> const uid: UserId = "u1";
> const pid: ProductId = uid;  // 에러 없음! UserId를 ProductId에 할당 가능
> ```
>
> Java/Kotlin 개발자에게 이건 충격이다. 다른 이름의 타입이 *같은* 타입이라니. 처음에는 "그냥 가독성을 위한 타입 별명이구나" 하고 넘어가지만, 나중에 `createOrder(pid, uid)`처럼 순서가 바뀌어도 컴파일러가 침묵하는 버그를 만나고 나서야 체감한다.
>
> **처방**: Brand type. 도메인 식별자가 섞일 위험이 있는 곳에는 `Brand<string, "UserId">` 형태를 쓰자. 처음에는 번거롭다고 느껴질 수 있지만, 실제 버그를 한 번 겪고 나면 자연스럽게 채택하게 된다. 특히 금융·의료·물류처럼 식별자가 여러 종류 있고 순서 실수가 치명적인 도메인에서는 표준 패턴이다.

---

> **📚 Java/Kotlin 시선 — Kotlin `value class` ↔ Branded type**
>
> Kotlin에는 `value class`(과거 이름 inline class)가 있다. 런타임 오버헤드 없이 명목 타입을 만든다.
>
> ```kotlin
> @JvmInline
> value class UserId(val value: String)
> @JvmInline
> value class ProductId(val value: String)
>
> fun createOrder(userId: UserId, productId: ProductId) { /* ... */ }
>
> val uid = UserId("user-123")
> val pid = ProductId("prod-456")
>
> createOrder(pid, uid)  // 컴파일 에러! Type mismatch
> ```
>
> 둘 다 zero-cost wrapper다. 런타임에는 감싼 값 자체처럼 동작한다(`UserId`는 그냥 `String`으로). 그런데 **강제 메커니즘이 다르다**.
>
> Kotlin `value class`는 언어 수준에서 강제한다. `UserId`와 `ProductId`는 진짜 다른 타입이다. 생성자를 호출하지 않고는 만들 수 없다.
>
> TS branded type은 타입 시스템의 트릭이다. `"user-123" as UserId`라고 쓰면 컴파일러를 속일 수 있다. 강제하려면 팀 컨벤션이 필요하다 — "직접 `as`로 branded type을 만들지 말고, maker 함수를 써라." 코드 리뷰 문화가 보완재가 된다.
>
> 이 차이가 작아 보이지만, 도메인 안전성에 대한 두 언어의 철학적 거리를 보여준다. Kotlin은 언어가 보장하고, TS는 팀이 보장한다.

---

## 6.3 enum의 함정과 union literal의 우위

Java 개발자에게 `enum`은 익숙한 도구다. 그리고 TS에도 `enum`이 있다. 처음에는 반가울 것이다.

```ts
enum OrderStatus {
  Pending = "PENDING",
  Fulfilled = "FULFILLED",
  Cancelled = "CANCELLED",
}
```

그런데 TS의 `enum`은 커뮤니티에서 뜨거운 논쟁의 대상이다. 결론부터 말하면, **많은 TS 전문가들이 `enum` 사용을 자제하고 union literal을 권장한다**. 왜일까.

### TS enum의 문제들

**첫 번째 문제: 런타임 객체가 생성된다.**

TS의 타입은 컴파일 후 지워진다. 그런데 `enum`은 예외다. 컴파일하면 실제 JS 코드가 만들어진다.

```ts
// TS
enum OrderStatus {
  Pending = "PENDING",
  Fulfilled = "FULFILLED",
}

// 컴파일 결과 JS
var OrderStatus;
(function (OrderStatus) {
  OrderStatus["Pending"] = "PENDING";
  OrderStatus["Fulfilled"] = "FULFILLED";
})(OrderStatus || (OrderStatus = {}));
```

이 런타임 코드는 번들에 포함된다. 작은 것처럼 보이지만 tree-shaking이 잘 안 되고, 번들 크기에 미묘하게 영향을 준다.

**두 번째 문제: 숫자형 enum의 역방향 매핑.**

문자열 enum은 그나마 낫지만, 숫자형 enum은 진짜 함정이다.

```ts
enum Direction {
  Up,    // 0
  Down,  // 1
  Left,  // 2
  Right, // 3
}

Direction[0]         // "Up" — 역방향 매핑이 자동 생성된다
Direction["Up"]      // 0
Direction[Direction.Up]  // "Up"
```

숫자형 enum은 키에서 값으로, 값에서 키로 양방향 조회가 된다. 타입 안전성이 약해진다.

```ts
function setDirection(dir: Direction) { /* ... */ }

setDirection(999)  // 에러 없음! 범위 밖의 숫자가 들어가도 통과
```

**세 번째 문제: `const enum`의 ambient 함정.**

`const enum`은 런타임 코드를 안 만들고 인라인으로 치환하지만, 다른 파일에서 `import`해서 쓸 때 `isolatedModules` 모드에서 에러가 난다. Babel, esbuild, swc는 파일을 개별 변환하므로 `const enum`의 인라인을 수행하지 못한다. 실무에서 번들러를 쓰면 `const enum`은 지뢰가 된다.

### union literal — 가볍고 투명하다

같은 것을 union literal로 표현해보자.

```ts
type OrderStatus = "pending" | "fulfilled" | "cancelled";

function processOrder(status: OrderStatus) {
  switch (status) {
    case "pending":
      return "대기 중";
    case "fulfilled":
      return "완료";
    case "cancelled":
      return "취소";
    default:
      const _exhaustive: never = status;  // 놓친 케이스가 있으면 컴파일 에러
      return _exhaustive;
  }
}
```

컴파일 후 남는 런타임 코드가 없다. 그냥 문자열 비교다. Tree-shaking도 자연스럽게 된다.

타입 좁히기도 자연스럽다.

```ts
type Order = {
  id: string;
  status: OrderStatus;
  amount: number;
};

function cancelOrder(order: Order): Order {
  if (order.status !== "pending") {
    throw new Error("pending 상태에서만 취소할 수 있다");
  }
  return { ...order, status: "cancelled" };
}
```

**discriminated union**으로 더 풍부한 상태를 표현할 수 있다.

```ts
type Order =
  | { status: "pending"; id: string; amount: number }
  | { status: "fulfilled"; id: string; amount: number; fulfilledAt: Date }
  | { status: "cancelled"; id: string; amount: number; cancelledAt: Date; reason: string };

function describeOrder(order: Order): string {
  switch (order.status) {
    case "pending":
      return `주문 ${order.id} 대기 중`;
    case "fulfilled":
      return `주문 ${order.id} ${order.fulfilledAt.toLocaleDateString()} 완료`;
    case "cancelled":
      return `주문 ${order.id} 취소 (사유: ${order.reason})`;
  }
}
```

각 상태마다 다른 필드를 가질 수 있다. `fulfilled` 상태에는 `fulfilledAt`이, `cancelled` 상태에는 `cancelledAt`과 `reason`이 있다. TS 컴파일러는 `switch`에서 `status`로 좁히면, 해당 분기에서 그 상태의 고유 필드에 접근할 수 있음을 안다.

이것이 Kotlin의 `sealed class` + `when`에 가장 가까운 TS 패턴이다.

### enum을 완전히 피해야 하는가

꼭 그런 건 아니다. 문자열 enum을 신중하게 쓰면 문제가 없는 경우도 있다. 특히 외부 API와 교환하는 값에 의미 있는 이름을 붙이고 싶을 때, 타입 안전성과 런타임 객체 둘 다 필요한 경우라면 문자열 enum도 선택지다.

단, **새 프로젝트를 시작할 때 디폴트는 union literal**이라고 보는 편이 낫다. 나중에 필요하다면 enum으로 옮기는 건 어렵지 않다.

---

> **📚 Java/Kotlin 시선 — Java `enum class` ↔ union literal**
>
> Java의 `enum`은 강력하다. 메서드, 필드, 생성자를 가질 수 있고, `switch`에서 exhaustive check가 된다(Java 14+ switch expression).
>
> ```java
> public enum OrderStatus {
>     PENDING("대기"),
>     FULFILLED("완료"),
>     CANCELLED("취소");
>
>     private final String label;
>     OrderStatus(String label) { this.label = label; }
>     public String getLabel() { return label; }
> }
>
> // 사용
> String result = switch (status) {
>     case PENDING -> status.getLabel();
>     case FULFILLED -> status.getLabel();
>     case CANCELLED -> status.getLabel();
> };
> ```
>
> Kotlin의 `enum class`도 비슷하다. 거기에 더해 `sealed class`로 각 케이스가 다른 데이터를 가질 수 있다.
>
> ```kotlin
> sealed class Order {
>     data class Pending(val id: String, val amount: Int) : Order()
>     data class Fulfilled(val id: String, val amount: Int, val fulfilledAt: LocalDate) : Order()
>     data class Cancelled(val id: String, val amount: Int, val reason: String) : Order()
> }
>
> fun describe(order: Order) = when (order) {
>     is Order.Pending -> "대기"
>     is Order.Fulfilled -> "완료: ${order.fulfilledAt}"
>     is Order.Cancelled -> "취소: ${order.reason}"
> }
> ```
>
> TS의 discriminated union이 이것을 흉내 낸다. `kind`(또는 `status`, `type`) 필드가 `is` 연산자 역할을 한다. `switch`에서 `never`로 exhaustive check까지 구현하면 Kotlin `when`의 안전성과 거의 같다.
>
> 차이점: TS union의 각 케이스는 메서드를 가질 수 없다. 데이터만 들어 있다. 메서드가 필요하면 함수를 따로 만들어 매칭하는 방식을 쓴다. 이것이 객체지향 스타일과 함수형 스타일의 경계점이기도 하다.

---

## 6.4 불변성 — `readonly`에서 `as const`까지

Java에서 `final`, Kotlin에서 `val`로 불변성을 표현한다. TS에는 여러 도구가 있다. 각각의 역할과 한계를 알아보자.

### `readonly` — 속성을 읽기 전용으로

```ts
interface Config {
  readonly host: string;
  readonly port: number;
}

const config: Config = { host: "localhost", port: 3000 };
config.host = "newhost";  // 컴파일 에러
```

`readonly`는 해당 속성을 수정 못 하게 막는다. Kotlin의 `val`과 같은 수준이다. 단, **얕은(shallow) 불변성**이다.

```ts
interface DeepConfig {
  readonly db: {
    host: string;
    port: number;
  };
}

const config: DeepConfig = { db: { host: "localhost", port: 5432 } };
config.db = { host: "other", port: 5432 };  // 컴파일 에러 — db 자체는 바꿀 수 없다
config.db.host = "other";  // 가능! db.host는 readonly가 아니다
```

`readonly db`는 `db` 속성의 재할당을 막지만, `db` 내부의 `host`나 `port`는 막지 않는다.

### `Readonly<T>` — 모든 속성을 얕게 읽기 전용으로

```ts
interface User {
  id: string;
  email: string;
  name: string;
}

type ReadonlyUser = Readonly<User>;
// { readonly id: string; readonly email: string; readonly name: string }
```

`Readonly<T>`는 T의 모든 속성에 `readonly`를 붙인다. 편리하지만 역시 얕다. 중첩 객체의 내부는 막지 않는다.

### `as const` — 리터럴 타입으로 굳힌다

`as const`는 다르다. 값 전체를 가장 좁은 리터럴 타입으로 굳힌다.

```ts
const config = {
  host: "localhost",
  port: 3000,
  db: {
    name: "mydb",
    pool: 5,
  }
} as const;

// config의 타입은:
// {
//   readonly host: "localhost";
//   readonly port: 3000;
//   readonly db: {
//     readonly name: "mydb";
//     readonly pool: 5;
//   }
// }
```

모든 속성이 `readonly`가 되고, 값이 구체적인 리터럴 타입으로 좁혀진다. `host`의 타입이 `string`이 아니라 `"localhost"` 리터럴이다. 중첩 객체도 재귀적으로 처리된다.

`as const`는 런타임 동작을 바꾸지 않는다. 타입 정보만 바꾼다. 상수 테이블, 설정 객체, 고정된 열거형 데이터를 표현할 때 매우 유용하다.

```ts
const ROUTES = {
  home: "/",
  profile: "/profile",
  settings: "/settings",
} as const;

type Route = typeof ROUTES[keyof typeof ROUTES];
// Route = "/" | "/profile" | "/settings"

function navigate(route: Route) {
  window.location.href = route;
}

navigate("/profile");    // OK
navigate("/unknown");   // 컴파일 에러
```

enum 대신 `as const`로 상수 집합을 만들고, `typeof ROUTES[keyof typeof ROUTES]`로 값 타입을 뽑는 패턴이다. 이것이 enum의 런타임 부담 없이 같은 효과를 낸다.

### `Object.freeze()` — 런타임 불변성

앞의 것들은 모두 컴파일 타임 보호다. 런타임에서도 객체를 정말로 불변으로 만들려면 `Object.freeze()`를 써야 한다.

```ts
const DEFAULTS = Object.freeze({
  timeout: 5000,
  retries: 3,
  host: "localhost",
});

DEFAULTS.timeout = 9999;  // 런타임 에러 (strict mode에서)
                           // 혹은 조용히 무시된다
```

단, `Object.freeze()`도 얕다. 중첩 객체까지 완전히 얼리려면 재귀적으로 적용해야 한다. 그리고 TS 타입 시스템은 `Object.freeze()`의 반환 타입을 `Readonly<T>`로 추론하므로, 타입 수준에서도 보호된다.

### 불변성 도구의 위계 정리

```
Object.freeze()   — 런타임 불변성 (얕음)
as const          — 컴파일 타임, 리터럴로 굳힘, 재귀적 readonly
Readonly<T>       — 컴파일 타임, 얕은 readonly
readonly (속성)   — 컴파일 타임, 개별 속성
```

실무에서 가장 많이 쓰는 건 `readonly`와 `as const`다. 깊은 불변성이 꼭 필요하면 `immer` 같은 라이브러리를 쓰거나, 데이터 구조를 처음부터 완전히 불변 스타일로 설계하는 편이 현실적이다.

---

## 6.5 에러를 도메인의 일부로 — throw에서 Result 패턴까지

이제 이 장의 핵심 주제다.

Java 개발자는 에러를 *예외(exception)*로 다룬다. `try-catch`로 잡고, `throws` 선언으로 상위에 전파하고, checked exception으로 컴파일러가 처리를 강제한다. 에러가 타입 시스템의 일부다.

TS에는 checked exception이 없다. 함수 시그니처만 봐서는 그 함수가 어떤 에러를 던지는지 알 수 없다.

```ts
async function fetchUser(userId: string): Promise<User> {
  // 이 함수가 어떤 에러를 던질 수 있는지 타입이 말해주지 않는다
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}
```

네트워크 에러가 날 수 있다. 404가 올 수 있다. JSON 파싱이 실패할 수 있다. 그런데 시그니처에는 `Promise<User>`만 있다. 호출자는 이것을 알려면 구현을 읽어야 한다.

Java의 checked exception은 이것이 불편해서 함수 시그니처에 `throws IOException`을 강제했다. 물론 Java 개발자들은 이게 번거로워서 `throws Exception`을 달거나 RuntimeException으로 감싸는 편법을 쓰곤 했다. 그래도 *의도*는 좋았다. 에러도 타입의 일부라는 생각.

그렇다면 TS에서는 어떻게 할 수 있을까.

### throw의 현실 — 타입이 없는 에러

먼저 TS에서 `throw`가 어떻게 동작하는지 정확히 이해하자.

```ts
function divide(a: number, b: number): number {
  if (b === 0) throw new Error("Division by zero");
  return a / b;
}

try {
  const result = divide(10, 0);
} catch (e) {
  // e의 타입은 unknown이다 (TS 4.0+, useUnknownInCatchVariables)
  if (e instanceof Error) {
    console.error(e.message);
  }
}
```

`catch` 블록에서 `e`의 타입은 `unknown`이다(TS 4.0 이전에는 `any`였다). 이는 의도적 설계다 — TS는 어떤 값이든 `throw`할 수 있고, 컴파일러는 그게 `Error`라고 가정할 수 없다.

더 중요한 것은, `divide` 함수 시그니처만 봐서는 이 함수가 `throw`할 수 있다는 걸 전혀 알 수 없다는 점이다. `Promise<number>`를 반환하는 함수도 마찬가지다. `reject`될 수 있다는 것도 타입이 표현하지 않는다.

이것은 checked exception에 익숙한 Java 개발자에게는 처음에 좀 당혹스러운 자리다. "에러 처리가 강제되지 않는다고? 그럼 어떻게 신뢰하지?"

### throw는 언제 쓰는 편이 좋을까

`throw`가 나쁜 건 아니다. 단, **어떤 상황에서 쓸지**를 의식적으로 선택하는 편이 낫다.

커뮤니티에서 정착한 실용적 경계는 이렇다.

**Throw를 쓰는 자리:**
- **프로그래밍 오류** — 절대 일어나면 안 되는 상황. `divide(10, 0)`처럼 호출자가 계약을 위반한 경우.
- **시스템 경계(boundary)** — HTTP 요청 핸들러, CLI 진입점처럼 에러를 잡아서 응답으로 변환하는 최상위 레이어.
- **복구 불가능한 상황** — 데이터베이스 연결 자체가 실패한 경우처럼 애플리케이션이 종료되어야 하는 상황.

**Result/Either를 쓰는 자리:**
- **예측 가능한 실패** — 사용자 입력이 유효하지 않다, 아이템이 재고 부족이다, 외부 API가 404를 반환했다.
- **비즈니스 규칙 위반** — 계좌 잔액이 부족하다, 이미 취소된 주문이다.
- **함수형 파이프라인** — 여러 단계의 연산을 체이닝할 때, 중간에 실패가 나면 나머지를 건너뛰고 싶다.

이 두 분류가 명확하게 나뉘는 건 아니다. 팀마다 경계를 다르게 잡는다. 하지만 **비즈니스 로직 안에서 발생하는 예측 가능한 실패는 Result로 표현하는 편이 낫다**는 데는 대체로 합의가 있다.

### Result 타입 직접 만들기

가장 단순한 형태의 Result 타입을 직접 만들어보자.

```ts
type Ok<T> = { ok: true; value: T };
type Err<E> = { ok: false; error: E };
type Result<T, E> = Ok<T> | Err<E>;

function ok<T>(value: T): Ok<T> {
  return { ok: true, value };
}

function err<E>(error: E): Err<E> {
  return { ok: false, error };
}
```

이제 이것을 쓰면:

```ts
type InsufficientFundsError = {
  type: "InsufficientFunds";
  required: number;
  available: number;
};

type TransferError =
  | InsufficientFundsError
  | { type: "AccountNotFound"; accountId: string }
  | { type: "AccountFrozen"; accountId: string };

function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
): Result<{ transactionId: string }, TransferError> {
  // 잔액 확인
  const balance = getBalance(fromAccountId);
  if (balance < amount) {
    return err({
      type: "InsufficientFunds",
      required: amount,
      available: balance,
    });
  }

  // ... 실제 이체 로직
  const txId = executeTransfer(fromAccountId, toAccountId, amount);
  return ok({ transactionId: txId });
}

// 호출하는 쪽
const result = transferFunds("acc-1", "acc-2", 50000);

if (result.ok) {
  console.log("이체 완료:", result.value.transactionId);
} else {
  switch (result.error.type) {
    case "InsufficientFunds":
      console.error(`잔액 부족 (필요: ${result.error.required}, 보유: ${result.error.available})`);
      break;
    case "AccountNotFound":
      console.error(`계좌를 찾을 수 없음: ${result.error.accountId}`);
      break;
    case "AccountFrozen":
      console.error(`동결된 계좌: ${result.error.accountId}`);
      break;
  }
}
```

함수 시그니처만 봐도 어떤 에러가 날 수 있는지 안다. `TransferError`를 보면 `InsufficientFunds`, `AccountNotFound`, `AccountFrozen` 세 경우가 있다는 것을 타입이 표현한다. 그리고 `switch` 문에서 모든 케이스를 처리하지 않으면 컴파일러가 경고한다(exhaustive check를 추가하면).

Java의 checked exception이 지향하던 바가 바로 이것이다. 에러를 *타입 시스템의 일부*로 만드는 것. TS에서는 `throw` 대신 `Result`로 이것을 달성한다.

### neverthrow — 실용적인 Result 라이브러리

직접 만든 Result도 충분하지만, 체이닝이나 변환이 필요해지면 코드가 복잡해진다. `neverthrow`는 이것을 깔끔하게 해결하는 작은 라이브러리다.

```bash
npm install neverthrow
```

```ts
import { ok, err, Result, ResultAsync } from "neverthrow";

type ValidationError = { field: string; message: string };

function validateEmail(email: string): Result<string, ValidationError> {
  if (!email.includes("@")) {
    return err({ field: "email", message: "유효한 이메일 주소가 아닙니다" });
  }
  return ok(email);
}

function validateAge(age: number): Result<number, ValidationError> {
  if (age < 0 || age > 150) {
    return err({ field: "age", message: "나이가 유효 범위를 벗어납니다" });
  }
  return ok(age);
}

// 여러 Result를 조합
function validateUser(
  email: string,
  age: number
): Result<{ email: string; age: number }, ValidationError[]> {
  const emailResult = validateEmail(email);
  const ageResult = validateAge(age);

  // combineWithAllErrors는 모든 에러를 모아서 반환
  return Result.combineWithAllErrors([emailResult, ageResult]).map(
    ([validEmail, validAge]) => ({ email: validEmail, age: validAge })
  );
}

// 체이닝
const result = validateEmail("alice@example.com")
  .map(email => email.toLowerCase())
  .andThen(email => findUserByEmail(email));  // Result를 반환하는 함수
```

`map`은 성공 값을 변환한다(실패면 그대로 통과). `andThen`은 성공 값을 받아서 새 Result를 반환하는 함수를 체이닝한다. 실패가 있으면 나머지 체인을 건너뛴다. 이것이 함수형 프로그래밍의 **Railway-oriented programming** 또는 **monadic chaining**이라고 불리는 패턴이다.

### ResultAsync — 비동기 에러를 타입으로

현실 코드는 대부분 비동기다. `neverthrow`의 `ResultAsync`가 이것을 다룬다.

```ts
import { ResultAsync, errAsync, okAsync } from "neverthrow";

function fetchUser(userId: string): ResultAsync<User, FetchError> {
  return ResultAsync.fromPromise(
    fetch(`/api/users/${userId}`).then(res => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return res.json() as Promise<User>;
    }),
    (e): FetchError => ({
      type: "NetworkError",
      message: e instanceof Error ? e.message : "Unknown error",
    })
  );
}

// 체이닝
const result = await fetchUser(userId)
  .map(user => ({ ...user, displayName: `${user.name} (${user.email})` }))
  .andThen(user => updateLastSeen(user.id).map(() => user));

if (result.isOk()) {
  console.log(result.value.displayName);
} else {
  console.error(result.error.message);
}
```

`ResultAsync.fromPromise`는 Promise를 Result로 감싼다. 두 번째 인자는 catch된 에러를 도메인 에러 타입으로 변환하는 함수다. 이렇게 하면 비동기 흐름 전체가 타입이 있는 에러 경로를 가진다.

### fp-ts Either — 더 학술적인 접근

`fp-ts`는 함수형 프로그래밍의 추상화를 TS로 가져온 라이브러리다. `Either<E, A>`가 Result에 해당한다. `Left(e)`가 실패, `Right(a)`가 성공이다.

```ts
import * as E from "fp-ts/Either";
import { pipe } from "fp-ts/function";

function validateEmail(email: string): E.Either<string, string> {
  return email.includes("@")
    ? E.right(email)
    : E.left("유효하지 않은 이메일");
}

function validateAge(age: number): E.Either<string, number> {
  return age >= 0 && age <= 150
    ? E.right(age)
    : E.left("나이가 범위를 벗어남");
}

const result = pipe(
  validateEmail("alice@example.com"),
  E.chain(email =>
    pipe(
      validateAge(25),
      E.map(age => ({ email, age }))
    )
  )
);
```

`pipe`와 `chain`, `map`으로 흐름을 구성한다. 코드가 처음에는 낯설지만, 한번 익숙해지면 읽기 좋다. 단, `fp-ts`는 학습 곡선이 가파르고 번들 크기도 상당하다. 팀 전체가 함수형 스타일을 선호하는 게 아니라면, `neverthrow`가 더 가볍고 친숙한 선택이다.

### Effect-ts — 더 나아간 선택

Effect-ts는 `fp-ts`를 넘어서 ZIO(Scala)·cats-effect에서 영향을 받은 포괄적인 함수형 프레임워크다. Effect-ts에서는 모든 계산이 `Effect<R, E, A>` — 의존성 R, 에러 E, 성공값 A — 로 표현된다.

```ts
import { Effect, pipe } from "effect";

const getUser = (userId: string): Effect.Effect<User, UserNotFoundError> =>
  Effect.tryPromise({
    try: () => fetchUserFromDb(userId),
    catch: () => new UserNotFoundError(userId),
  });

const program = pipe(
  getUser("user-123"),
  Effect.map(user => user.name),
  Effect.flatMap(name => Effect.log(`사용자: ${name}`))
);

// 실행
Effect.runPromise(program);
```

에러 타입이 `Effect` 시그니처 자체에 포함된다. 코드만 봐도 어떤 에러가 날 수 있는지 안다. Dependency injection도 `R` 타입 인자로 표현된다.

강력하지만 무겁다. 전체 아키텍처가 Effect 모델을 중심으로 조직되어야 한다. 입문하기에는 `neverthrow`가 더 현실적이다.

### Java checked exception과의 비교 — 무엇을 얻고 무엇을 잃는가

솔직하게 비교해보자.

**Java checked exception이 좋은 점:**
- 컴파일러가 처리를 강제한다. `throws IOException`이 있으면 반드시 `try-catch`하거나 다시 `throws`를 선언해야 한다.
- 라이브러리 API만 봐도 어떤 예외가 날 수 있는지 안다.

**Java checked exception의 문제:**
- 개발자들이 결국 `throws Exception`이나 `RuntimeException`으로 감싸서 체크를 회피한다.
- checked exception이 API 계약의 일부가 되어, 라이브러리 내부 구현이 바뀌면 API도 바뀐다.
- 람다·스트림과 궁합이 나쁘다. checked exception을 던지는 함수를 `map()`에 넣으면 번거롭다.

**TS의 throw:**
- 유연하다. 어디서든 던질 수 있고, 잡든 안 잡든 컴파일러는 신경 안 쓴다.
- 타입이 없어서 호출자가 믿고 쓰기 어렵다.

**TS의 Result 패턴:**
- 함수 시그니처에 에러 타입이 포함된다. checked exception의 *정신*을 가져올 수 있다.
- 컴파일러가 강제하지 않는다. 팀이 컨벤션을 지켜야 한다.
- 람다·체이닝과 궁합이 좋다. `map`, `andThen`으로 흐름이 자연스럽다.
- JS/TS 생태계의 많은 라이브러리가 여전히 `throw`를 쓰므로, 경계에서 변환이 필요하다.

결국 **TS에서 Result 패턴은 "언어가 강제하지 않는 checked exception"**이다. 컴파일러의 강제 대신 팀의 컨벤션으로 유지된다. 불완전해 보이지만, Java checked exception도 실제로 그 강제 덕분에 자주 우회되었던 것을 생각하면, 현실에서 차이가 생각만큼 크지 않을 수 있다.

---

> **📚 Java/Kotlin 시선 — Kotlin `Result<T>`/Arrow `Either` ↔ neverthrow**
>
> Kotlin에도 Result 타입이 있다.
>
> ```kotlin
> fun fetchUser(userId: String): Result<User> = runCatching {
>     // 예외가 발생하면 Failure로 감싸진다
>     userRepository.findById(userId) ?: throw UserNotFoundException(userId)
> }
>
> val result = fetchUser("user-123")
> result.fold(
>     onSuccess = { user -> println("사용자: ${user.name}") },
>     onFailure = { e -> println("에러: ${e.message}") }
> )
> ```
>
> Kotlin의 `Result<T>`는 성공/실패를 감싸지만, 에러 타입이 `Throwable`로 고정이다. 어떤 에러인지 타입 수준에서 표현하려면 Arrow 라이브러리의 `Either<E, A>`를 쓴다.
>
> ```kotlin
> import arrow.core.Either
> import arrow.core.right
> import arrow.core.left
>
> sealed class TransferError {
>     data class InsufficientFunds(val required: Int, val available: Int) : TransferError()
>     data class AccountNotFound(val accountId: String) : TransferError()
> }
>
> fun transfer(from: String, to: String, amount: Int): Either<TransferError, String> {
>     val balance = getBalance(from)
>     return if (balance < amount)
>         InsufficientFunds(amount, balance).left()
>     else
>         executeTransfer(from, to, amount).right()
> }
>
> // 체이닝
> val result = transfer("acc-1", "acc-2", 50000)
>     .map { txId -> "완료: $txId" }
>     .flatMap { msg -> sendNotification(msg).map { msg } }
> ```
>
> TS의 `neverthrow`와 개념이 정확히 같다. `Either.right()`가 `ok()`, `Either.left()`가 `err()`다. `map`과 `flatMap`(TS에서는 `andThen`)도 같다.
>
> 차이: Arrow는 성숙한 생태계와 풍부한 추상화를 제공한다. Kotlin의 언어 기능(sealed class, data class, `when`)과도 자연스럽게 결합된다. TS의 `neverthrow`는 훨씬 작고 단순하다 — 그것이 장점이기도 하다. Arrow처럼 포괄적인 도구가 필요하다면 TS 생태계에서는 `fp-ts`나 `Effect-ts`가 그 위치에 있다.

---

## 6.6 에러 타입의 설계 — 도메인 에러를 어떻게 표현할까

Result 패턴을 쓰기로 했다면, 에러 타입을 어떻게 설계할지가 중요하다.

### 단순한 시작 — 문자열 에러

```ts
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return err("Division by zero");
  return ok(a / b);
}
```

빠르고 편하지만, 에러 메시지가 `string`이면 처리 분기를 타입으로 표현할 수 없다. 호출자는 문자열 비교로 분기해야 한다.

### 태그된 에러 — discriminated union 활용

더 나은 방법은 에러를 discriminated union으로 표현하는 것이다.

```ts
type OrderError =
  | { type: "OrderNotFound"; orderId: string }
  | { type: "OrderAlreadyCancelled"; orderId: string; cancelledAt: Date }
  | { type: "InsufficientStock"; productId: string; requested: number; available: number }
  | { type: "PaymentFailed"; reason: string; retryable: boolean };

function processOrder(orderId: string): Result<Order, OrderError> {
  const order = db.findOrder(orderId);
  if (!order) {
    return err({ type: "OrderNotFound", orderId });
  }

  if (order.status === "cancelled") {
    return err({
      type: "OrderAlreadyCancelled",
      orderId,
      cancelledAt: order.cancelledAt!,
    });
  }

  // ... 처리
  return ok(processedOrder);
}

// 호출 측에서 타입 안전하게 처리
const result = processOrder("order-123");

if (!result.ok) {
  switch (result.error.type) {
    case "OrderNotFound":
      return sendNotFound(result.error.orderId);
    case "OrderAlreadyCancelled":
      return sendConflict(`이미 ${result.error.cancelledAt}에 취소됨`);
    case "InsufficientStock":
      return sendBadRequest(`재고 부족: ${result.error.available}개 남음`);
    case "PaymentFailed":
      if (result.error.retryable) {
        return scheduleRetry(orderId);
      }
      return sendPaymentError(result.error.reason);
  }
}
```

에러마다 다른 데이터가 있고, `switch`에서 타입이 좁혀지므로 각 케이스의 고유 필드에 안전하게 접근할 수 있다. Kotlin의 `sealed class`와 거의 같은 표현력이다.

### 에러 계층 — 작게 시작하고 필요하면 합치자

프로그램이 커지면 에러 타입도 많아진다. 계층을 구성하는 방법이 있다.

```ts
// 도메인별 에러
type UserError =
  | { type: "UserNotFound"; userId: string }
  | { type: "UserAlreadyExists"; email: string };

type OrderError =
  | { type: "OrderNotFound"; orderId: string }
  | { type: "InsufficientStock"; productId: string };

// 상위 레벨에서 합치기
type AppError =
  | { domain: "user"; error: UserError }
  | { domain: "order"; error: OrderError }
  | { domain: "system"; error: { message: string; stack?: string } };
```

또는 에러 코드를 namespace로 구분하는 방법도 있다.

```ts
type ErrorCode =
  | `USER_${string}`
  | `ORDER_${string}`
  | `SYSTEM_${string}`;

type AppError = {
  code: ErrorCode;
  message: string;
  metadata?: Record<string, unknown>;
};
```

어떤 방식이든 정답은 없다. 중요한 건 팀 내에서 일관성을 유지하는 것이다.

### boundary에서 throw, 내부에서 Result

앞서 말한 실용적 경계를 코드로 보여주자. HTTP 핸들러가 좋은 예다.

```ts
// 내부 비즈니스 로직 — Result를 사용
function cancelOrder(
  orderId: string,
  userId: string
): Result<Order, OrderError> {
  const order = db.findOrder(orderId);
  if (!order) return err({ type: "OrderNotFound", orderId });
  if (order.userId !== userId) return err({ type: "NotOwner", orderId, userId });
  if (order.status === "cancelled") {
    return err({
      type: "OrderAlreadyCancelled",
      orderId,
      cancelledAt: order.cancelledAt!,
    });
  }

  const updated = db.updateOrder(orderId, { status: "cancelled" });
  return ok(updated);
}

// HTTP boundary — throw/catch로 외부에 전달
app.delete("/orders/:id", async (req, res) => {
  const result = cancelOrder(req.params.id, req.user.id);

  if (result.ok) {
    return res.json({ success: true, order: result.value });
  }

  switch (result.error.type) {
    case "OrderNotFound":
      return res.status(404).json({ error: "주문을 찾을 수 없습니다" });
    case "NotOwner":
      return res.status(403).json({ error: "권한이 없습니다" });
    case "OrderAlreadyCancelled":
      return res.status(409).json({ error: "이미 취소된 주문입니다" });
  }
});
```

비즈니스 로직은 Result로 흐른다. HTTP 핸들러가 boundary다 — 여기서 Result를 HTTP 응답으로 변환한다. 핸들러 자체에서 예상치 못한 `throw`가 난다면(DB 연결 실패 같은), Express의 에러 미들웨어가 잡는다. 이 두 층이 분리되어 있다.

---

## 6.7 도메인 모델 설계 — 모든 것을 합쳐서

지금까지 살펴본 도구들을 모아서 작은 도메인 모델을 설계해보자. 간단한 전자상거래 주문 도메인이다.

### 식별자 타입 정의

```ts
declare const _brand: unique symbol;
type Brand<T, B> = T & { readonly [_brand]: B };

type UserId = Brand<string, "UserId">;
type ProductId = Brand<string, "ProductId">;
type OrderId = Brand<string, "OrderId">;
type Money = Brand<number, "Money">;  // 원화 기준, 정수

function makeUserId(v: string): UserId {
  if (!v || v.trim().length === 0) throw new Error("UserId cannot be empty");
  return v as UserId;
}

function makeMoney(v: number): Result<Money, { type: "InvalidAmount"; value: number }> {
  if (!Number.isInteger(v) || v < 0) {
    return err({ type: "InvalidAmount", value: v });
  }
  return ok(v as Money);
}
```

### 도메인 상태 표현

```ts
type OrderStatus =
  | { status: "pending" }
  | { status: "confirmed"; confirmedAt: Date }
  | { status: "shipped"; confirmedAt: Date; shippedAt: Date; trackingNumber: string }
  | { status: "delivered"; confirmedAt: Date; shippedAt: Date; deliveredAt: Date }
  | { status: "cancelled"; cancelledAt: Date; reason: string };

type OrderItem = {
  readonly productId: ProductId;
  readonly quantity: number;
  readonly unitPrice: Money;
};

type Order = {
  readonly id: OrderId;
  readonly userId: UserId;
  readonly items: ReadonlyArray<OrderItem>;
  readonly totalAmount: Money;
} & OrderStatus;
```

`Order`는 `OrderId`, `UserId`, `items`, `totalAmount`에 더해 `OrderStatus`가 intersection으로 붙어 있다. 상태에 따른 추가 필드가 자동으로 포함된다.

### 도메인 로직

```ts
type OrderDomainError =
  | { type: "EmptyCart" }
  | { type: "OrderNotCancellable"; currentStatus: string }
  | { type: "InvalidQuantity"; productId: ProductId; quantity: number };

function createOrder(
  userId: UserId,
  items: Array<{ productId: ProductId; quantity: number; unitPrice: Money }>
): Result<Order, OrderDomainError> {
  if (items.length === 0) {
    return err({ type: "EmptyCart" });
  }

  const invalidItem = items.find(i => i.quantity <= 0);
  if (invalidItem) {
    return err({
      type: "InvalidQuantity",
      productId: invalidItem.productId,
      quantity: invalidItem.quantity,
    });
  }

  const totalAmount = items.reduce(
    (sum, item) => sum + item.unitPrice * item.quantity,
    0
  ) as Money;

  const order: Order = {
    id: generateOrderId() as OrderId,
    userId,
    items: items.map(i => ({
      productId: i.productId,
      quantity: i.quantity,
      unitPrice: i.unitPrice,
    })),
    totalAmount,
    status: "pending",
  };

  return ok(order);
}

function cancelOrder(
  order: Order,
  reason: string
): Result<Order, OrderDomainError> {
  if (order.status !== "pending") {
    return err({
      type: "OrderNotCancellable",
      currentStatus: order.status,
    });
  }

  const cancelled: Order = {
    ...order,
    status: "cancelled",
    cancelledAt: new Date(),
    reason,
  };

  return ok(cancelled);
}
```

이 도메인 모델의 특징을 정리하면:

1. **식별자 혼용 불가**: `UserId`와 `ProductId`가 섞이면 컴파일 에러.
2. **상태 전이가 타입에 표현됨**: `cancelOrder`는 `pending` 상태에서만 가능하다는 게 `switch`/`if` 안에서 타입이 보증한다.
3. **에러가 타입의 일부**: `OrderDomainError`를 보면 어떤 실패가 가능한지 안다.
4. **불변성**: `readonly`와 `ReadonlyArray`로 직접 수정을 막는다.

완벽하지는 않다. Kotlin의 `data class`나 `sealed class`처럼 컴파일러가 강제해주는 부분이 훨씬 많지 않다. `as Money` 같은 단언이 여전히 필요하다. 하지만 이 정도면 실무에서 도메인 버그를 상당히 컴파일 타임에 잡을 수 있다.

---

## 6.8 실전 패턴 — 조합하면 어떻게 보이는가

실제 서비스 코드에서 이 패턴들이 어떻게 어울리는지 더 완전한 예제로 보자.

### 사용자 등록 유스케이스

```ts
// 도메인 에러
type RegistrationError =
  | { type: "EmailAlreadyExists"; email: string }
  | { type: "WeakPassword"; minLength: number }
  | { type: "InvalidEmail"; email: string }
  | { type: "DatabaseError"; message: string };

// 입력 타입 (외부에서 받은 raw 데이터)
type RegisterInput = {
  email: string;
  password: string;
  name: string;
};

// 검증된 값 타입 (branded)
type ValidatedEmail = Brand<string, "ValidatedEmail">;
type HashedPassword = Brand<string, "HashedPassword">;

// 검증 함수들
function validateEmail(
  email: string
): Result<ValidatedEmail, RegistrationError> {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return err({ type: "InvalidEmail", email });
  }
  return ok(email as ValidatedEmail);
}

function validatePassword(
  password: string
): Result<string, RegistrationError> {
  const MIN_LENGTH = 8;
  if (password.length < MIN_LENGTH) {
    return err({ type: "WeakPassword", minLength: MIN_LENGTH });
  }
  return ok(password);
}

// 서비스 레이어
async function registerUser(
  input: RegisterInput
): Promise<Result<{ userId: UserId }, RegistrationError>> {
  // 검증
  const emailResult = validateEmail(input.email);
  if (!emailResult.ok) return emailResult;

  const passwordResult = validatePassword(input.password);
  if (!passwordResult.ok) return passwordResult;

  // 중복 확인
  const existing = await db.users.findByEmail(emailResult.value);
  if (existing) {
    return err({ type: "EmailAlreadyExists", email: input.email });
  }

  // 저장
  try {
    const hashedPassword = await hashPassword(passwordResult.value) as HashedPassword;
    const userId = await db.users.create({
      email: emailResult.value,
      password: hashedPassword,
      name: input.name,
    });
    return ok({ userId: userId as UserId });
  } catch (e) {
    // 예상치 못한 DB 에러는 Result로 변환
    return err({
      type: "DatabaseError",
      message: e instanceof Error ? e.message : "Unknown database error",
    });
  }
}

// HTTP 핸들러
app.post("/users/register", async (req, res) => {
  const result = await registerUser(req.body);

  if (result.ok) {
    return res.status(201).json({ userId: result.value.userId });
  }

  switch (result.error.type) {
    case "InvalidEmail":
      return res.status(400).json({ field: "email", message: "이메일 형식이 올바르지 않습니다" });
    case "WeakPassword":
      return res.status(400).json({
        field: "password",
        message: `비밀번호는 최소 ${result.error.minLength}자 이상이어야 합니다`,
      });
    case "EmailAlreadyExists":
      return res.status(409).json({ message: "이미 가입된 이메일입니다" });
    case "DatabaseError":
      console.error("DB Error:", result.error.message);
      return res.status(500).json({ message: "서버 오류가 발생했습니다" });
  }
});
```

이 코드를 처음 본 Java/Kotlin 개발자는 낯설게 느낄 수 있다. `Result`를 `if (!emailResult.ok) return emailResult`로 일일이 체크하는 것이 번거롭다고 느낄 수 있다. 사실 그 느낌이 맞다. `neverthrow`의 `andThen` 체이닝을 쓰면 이 보일러플레이트를 줄일 수 있다.

```ts
import { ResultAsync } from "neverthrow";

async function registerUser(
  input: RegisterInput
): ResultAsync<{ userId: UserId }, RegistrationError> {
  return validateEmail(input.email)
    .asyncAndThen(email =>
      validatePassword(input.password).asyncAndThen(password =>
        ResultAsync.fromPromise(
          db.users.findByEmail(email),
          (e): RegistrationError => ({ type: "DatabaseError", message: String(e) })
        ).andThen(existing => {
          if (existing) {
            return err({ type: "EmailAlreadyExists", email: input.email });
          }
          return ResultAsync.fromPromise(
            (async () => {
              const hashed = await hashPassword(password);
              const userId = await db.users.create({ email, password: hashed, name: input.name });
              return { userId: userId as UserId };
            })(),
            (e): RegistrationError => ({ type: "DatabaseError", message: String(e) })
          );
        })
      )
    );
}
```

스타일이 다르다. 어느 쪽이 더 가독성이 좋은지는 팀마다 다를 수 있다. 중요한 건 어떤 스타일이든 **에러 타입이 함수 시그니처에 표현된다**는 점이다.

---

## 6.9 `as const`로 객체를 열거형처럼 쓰기

enum의 대안으로 `as const`를 쓰는 패턴을 조금 더 살펴보자. 실무에서 자주 만나는 패턴이다.

### 상수 맵 패턴

```ts
const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
  CONFLICT: 409,
  INTERNAL_ERROR: 500,
} as const;

type HttpStatusCode = typeof HTTP_STATUS[keyof typeof HTTP_STATUS];
// 200 | 201 | 400 | 401 | 404 | 409 | 500

function sendResponse(status: HttpStatusCode, body: unknown) {
  // ...
}

sendResponse(HTTP_STATUS.OK, { success: true });
sendResponse(200, { success: true });          // 직접 숫자도 허용
sendResponse(999, { success: true });          // 컴파일 에러
```

`HTTP_STATUS`는 런타임에 실제 객체로 존재한다. enum처럼 쓸 수 있으면서 tree-shaking도 되고, 타입도 정확하다.

### 설정 객체 패턴

```ts
const FEATURE_FLAGS = {
  enableNewCheckout: true,
  enableBetaSearch: false,
  maxCartItems: 50,
} as const;

type FeatureFlag = keyof typeof FEATURE_FLAGS;

function isEnabled(flag: FeatureFlag): boolean {
  return FEATURE_FLAGS[flag] as boolean;
}

isEnabled("enableNewCheckout");  // OK
isEnabled("unknownFlag");        // 컴파일 에러
```

---

## 6.10 실무 체크리스트 — 도메인 모델링할 때 물어볼 것들

마지막으로, 새 도메인을 TS로 모델링할 때 체크해볼 질문들을 정리하자.

**식별자 안전성**
- [ ] 여러 종류의 `string` 식별자가 함수에 같이 들어가는가? → Branded type 고려
- [ ] 생성 지점에서 검증이 필요한가? → maker 함수 추가

**상태 표현**
- [ ] 상태마다 다른 필드가 있는가? → discriminated union
- [ ] 상태 전이 규칙이 있는가? → 전이 함수에서 타입으로 표현

**에러 처리**
- [ ] 이 실패가 비즈니스 규칙 위반인가? → Result 패턴
- [ ] 이 실패가 프로그래밍 오류인가? → throw
- [ ] 호출자가 에러를 처리하지 않으면 안 되는가? → Result로 강제

**불변성**
- [ ] 생성 후 바뀌면 안 되는 필드가 있는가? → `readonly`
- [ ] 설정/상수 객체인가? → `as const`
- [ ] 컬렉션이 수정되면 안 되는가? → `ReadonlyArray<T>`

**열거형**
- [ ] 고정된 값의 집합이 필요한가? → union literal 우선
- [ ] 런타임에 열거형 값을 순회해야 하는가? → `as const` 객체
- [ ] 외부 API와 값을 교환하면서 이름이 필요한가? → 문자열 enum 고려

---

> **📖 더 깊이 가려면**
>
> 이 장에서 다룬 branded type, discriminated union, Result 패턴은 도메인 모델링의 기초다. 여기서 한 발 더 나가면 몇 가지 방향이 있다.
>
> **함수형 도메인 모델링**: `fp-ts`와 `Effect-ts`는 이 패턴들을 더 체계화한다. Functor, Applicative, Monad 등의 개념으로 에러 처리 체인을 더 우아하게 구성할 수 있다. 단, 학습 곡선이 가파르다.
>
> **zod와 런타임 검증**: 도메인 모델의 타입을 zod 스키마로 정의하면, 타입 추론과 런타임 검증을 한 곳에서 관리할 수 있다. 외부 경계(API 입력, env 변수)에서 특히 유용하다.
>
> **테스트**: 도메인 타입이 잘 설계되어 있으면 테스트도 더 명확해진다. Result 타입을 반환하는 함수는 `result.ok`와 `result.value` / `result.error`를 단언하는 식으로 깔끔하게 테스트할 수 있다.
>
> → **14장에서 도메인 모델 + Result 패턴의 *타입 단위 테스트*를 다룬다.** 이 장에서 만든 `createOrder`, `cancelOrder`, `registerUser` 같은 함수를 어떻게 테스트하는지, branded type이 테스트에서 어떻게 도움이 되는지를 구체적으로 살펴볼 것이다.

---

## 마무리

이 장에서 살펴본 것들을 정리해보자.

`interface`와 `type alias`는 둘 다 써도 된다. 객체 형태에는 어느 것이든, union이나 intersection에는 `type`, 라이브러리 확장에는 `interface`를 쓰면 된다. 두 개가 공존하는 코드베이스가 더 흔하다.

TS의 구조적 타입 시스템은 도메인 식별자를 자동으로 구분하지 않는다. `UserId`와 `ProductId`가 모두 `string`이면 서로 섞여도 컴파일러가 침묵한다. Branded type이 이것을 해결한다. 토스, Effect-ts, zod 모두 채택한 표준 패턴이다.

TS `enum`은 함정이 있다. 런타임 객체 생성, 숫자형 enum의 역방향 매핑, `const enum`과 번들러의 충돌. 새 코드에서는 union literal을 디폴트로 쓰는 편이 낫다. discriminated union + `never`로 exhaustive check까지 구현하면 Kotlin `sealed class` + `when`과 거의 같은 표현력이 나온다.

불변성은 `readonly`, `Readonly<T>`, `as const`, `Object.freeze()`의 네 도구로 접근한다. 모두 얕은 불변성이라는 한계가 있다. 깊은 불변성이 필요하면 `immer` 같은 라이브러리가 필요하다.

가장 중요한 것은 에러 처리다. TS에는 checked exception이 없다. `throw`는 타입 정보가 없다. 이것이 Java/Kotlin에서 온 개발자에게 처음에는 불안하게 느껴진다. 하지만 `Result<T, E>` 패턴으로 에러를 타입의 일부로 만들 수 있다. `neverthrow`가 이것을 실용적으로 제공한다. 경계에서는 throw, 내부 비즈니스 로직에서는 Result — 이 두 층을 의식적으로 분리하면 코드가 훨씬 명확해진다.

이 모든 것을 처음부터 완벽하게 적용하려고 하면 번거롭다. 기억해두자 — 도구를 점진적으로 도입하는 편이 낫다. 먼저 discriminated union으로 상태를 표현하는 것부터 시작해도 좋다. Branded type은 식별자 혼용으로 버그를 한 번 겪은 뒤에 도입해도 늦지 않는다. Result 패턴은 비즈니스 로직이 복잡해지면서 자연스럽게 필요성을 느끼게 된다.

도메인 모델이 충실하게 설계되면, 그 다음 레이어들이 훨씬 안정적이 된다. 7장에서는 이 도메인 객체들이 비동기 흐름에서 어떻게 움직이는지를 살펴보자. Promise, async/await, 그리고 Java의 `CompletableFuture`·Reactor `Mono`와의 비교가 기다리고 있다.

---

> 6장에서 도메인 모델이 충실하게 설계되었다. 이제 그 도메인 객체들이 비동기 흐름에서 어떻게 움직이는지를 살펴보자. Java의 `CompletableFuture`, Reactor의 `Mono`/`Flux`, Kotlin coroutine의 `suspend` — 이 익숙한 모델들과 TypeScript의 `Promise`·`async/await`·Observable·AsyncIterator를 나란히 놓는다. 7장에서.

# 7장. 비동기 모델 — Promise·async/await·Observable·AsyncIterator

Spring WebFlux로 `Mono<ResponseEntity<UserDto>>`를 체이닝하던 손이, 처음으로 TypeScript 코드를 열었다고 해보자. 눈에 들어오는 건 이런 코드다.

```typescript
fetchUser(id)
  .then(user => enrichProfile(user))
  .then(profile => sendEmail(profile))
  .catch(err => logger.error(err));
```

*"아, 이건 Mono랑 비슷하네."* 직감이 빠른 사람이라면 바로 느낀다. `.then()`이 `.map()`처럼 보이고, `.catch()`가 `.onErrorResume()`처럼 읽힌다. 그 감각은 절반쯤 맞다. 하지만 절반쯤 틀리기도 하다. Mono는 구독(subscribe)하기 전에는 아무것도 실행하지 않는다. 반면 Promise는 만들어지는 순간 바로 실행이 시작된다. Mono에서 에러가 흘러내려가지 않으면 체인이 조용히 멈춘다. Promise에서 에러를 받지 않으면 프로세스 전체가 죽을 수도 있다.

이 장은 Java와 Kotlin의 비동기 모델을 알고 있는 사람이 TypeScript의 비동기 세계에 정확히 착지할 수 있도록 돕는 장이다. 이벤트 루프에서 시작해 Promise의 세 상태, async/await의 본질, 에러가 사라지는 이유, AbortSignal로 취소하는 방법, RxJS Observable, AsyncIterator, 그리고 병렬 패턴까지 차례로 살펴보자. 코드를 읽고 짜는 것뿐만 아니라, 예외가 어디로 갔는지 정확히 추적할 수 있는 수준에 도달하는 것이 목표다.

---

## 이벤트 루프 복습 — "단일 스레드인데 어떻게 비동기를 돌리는가"

2장에서 이벤트 루프의 기본 구조를 다뤘다. 여기서는 Promise와 직접 연관된 부분을 다시 꺼내 보자. 바로 *마이크로태스크 큐(microtask queue)*다.

Java/JVM 세계에서 비동기는 보통 스레드를 더 만드는 방식으로 이뤄진다. `ExecutorService`가 스레드 풀을 관리하고, `CompletableFuture`가 그 스레드 위에서 작업을 예약한다. 스레드는 OS 레벨 자원이고, 블로킹이 일어나면 해당 스레드가 잠들었다가 깨어난다. Reactor의 경우는 전용 스케줄러(`Schedulers.boundedElastic()`)를 두어 논블로킹 IO 결과를 특정 스레드로 라우팅한다.

JavaScript는 다르다. 메인 실행 스레드는 하나뿐이다. 그 하나의 스레드가 *이벤트 루프*라는 메커니즘으로 비동기를 처리한다.

```
┌─────────────────────────────────────────────────────┐
│                   이벤트 루프                        │
│                                                      │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │  Call Stack      │   │  Web APIs / Node APIs  │  │
│  │  (실행 중인 코드) │   │  (타이머, IO, 네트워크) │  │
│  └──────────────────┘   └────────────────────────┘  │
│           ↑                         │                │
│           │                         ▼                │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │  Microtask Queue │ ← │  Macrotask Queue        │  │
│  │  (Promise, queueMicrotask) │  (setTimeout, setInterval, IO) │  │
│  └──────────────────┘   └────────────────────────┘  │
│   콜 스택이 비면 즉시 소진  콜 스택 + 마이크로태스크 후 처리  │
└─────────────────────────────────────────────────────┘
```

이벤트 루프의 동작 순서는 이렇다.

1. **콜 스택이 비어 있는지 확인한다.**
2. **마이크로태스크 큐를 전부 소진한다.** 마이크로태스크 안에서 새 마이크로태스크가 생겨도 그것까지 전부 처리한다.
3. 그 다음에야 **매크로태스크 큐에서 하나**를 꺼내 실행한다.
4. 다시 1로.

Promise가 *마이크로태스크*로 분류된다는 점이 핵심이다. 즉, `setTimeout(fn, 0)`보다 Promise의 `.then()` 콜백이 *먼저* 실행된다.

```typescript
console.log("1: 동기");

setTimeout(() => console.log("4: 매크로태스크"), 0);

Promise.resolve().then(() => console.log("2: 마이크로태스크 첫 번째"));
Promise.resolve().then(() => console.log("3: 마이크로태스크 두 번째"));

console.log("1.5: 동기 계속");

// 출력 순서:
// 1: 동기
// 1.5: 동기 계속
// 2: 마이크로태스크 첫 번째
// 3: 마이크로태스크 두 번째
// 4: 매크로태스크
```

`setTimeout(fn, 0)`이 *"즉시 실행"*처럼 보이지만, 실제로는 마이크로태스크가 전부 빠진 다음에야 실행된다. 이 순서를 이해하지 못하면, 나중에 비동기 코드의 실행 순서가 직관과 다를 때 원인을 찾기 어렵다.

> ### 📚 Java/Kotlin 시선 박스 ④ — `ExecutorService` ↔ 이벤트 루프
>
> | Java `ExecutorService` | JavaScript 이벤트 루프 |
> |---|---|
> | 스레드 풀 기반 | 단일 스레드 기반 |
> | `submit(task)` → 스레드 하나를 점유 | 콜백 → 큐에 등록, 스레드 반환 |
> | 블로킹 IO → 스레드 대기 | 블로킹 IO 없음 (Node.js libuv가 OS에 위임) |
> | 병렬성 = 스레드 수 | 병렬성 = IO 대기 중 다른 태스크 처리 |
> | 오류 → `Future.get()`에서 `ExecutionException` | 오류 → Promise rejection으로 전달 |
>
> Java에서 비동기를 늘리려면 스레드를 더 만든다. Node.js에서 처리량을 늘리려면 *IO를 비동기로 만들고 CPU를 붙잡지 않는다*. CPU 집약적인 작업을 이벤트 루프에서 돌리면 다른 모든 요청이 기다린다 — 이것이 Node.js에서 `worker_threads`나 `cluster`를 쓰는 이유다.
>
> Reactor의 `Schedulers.boundedElastic()`이 IO 스레드 풀을 관리하는 것과, Node.js의 libuv가 OS 비동기 IO를 관리하는 것은 *결과적으로 비슷한 문제를 다른 방식으로 푸는 것*이다. 다만 Node.js는 그 추상화가 언어/런타임 수준에 내장되어 있다.

마이크로태스크 큐가 Promise를 어떻게 굴리는지 이해했으니, 이제 Promise 그 자체를 살펴보자.

---

## Promise — 단일 값을 위한 비동기 컨테이너

### Promise의 세 상태

Promise는 항상 세 상태 중 하나에 있다.

- **Pending(대기)**: 아직 결과가 없다. 초기 상태.
- **Fulfilled(이행)**: 성공적으로 완료되었다. 결과 값을 가진다.
- **Rejected(거부)**: 실패했다. 에러 이유를 가진다.

한 번 Fulfilled 또는 Rejected가 된 Promise는 *다시 상태가 바뀌지 않는다.* 이것을 *settled(정착)* 상태라고 부른다.

```typescript
// Fulfilled Promise 직접 만들기
const fulfilled = Promise.resolve(42);

// Rejected Promise 직접 만들기
const rejected = Promise.reject(new Error("무언가 잘못됨"));

// 직접 제어하기
const manual = new Promise<number>((resolve, reject) => {
  setTimeout(() => {
    const success = Math.random() > 0.5;
    if (success) {
      resolve(100);
    } else {
      reject(new Error("운이 나빴다"));
    }
  }, 1000);
});
```

> ### 📚 Java/Kotlin 시선 박스 ① — `CompletableFuture` ↔ Promise
>
> | Java `CompletableFuture<T>` | TypeScript `Promise<T>` |
> |---|---|
> | `CompletableFuture.completedFuture(v)` | `Promise.resolve(v)` |
> | `CompletableFuture.failedFuture(ex)` | `Promise.reject(err)` |
> | `new CompletableFuture<>()` + `complete(v)` | `new Promise((resolve, reject) => ...)` |
> | `.thenApply(fn)` | `.then(fn)` |
> | `.thenCompose(fn)` | `.then(fn)` (flatMap에 해당) |
> | `.exceptionally(fn)` | `.catch(fn)` |
> | `.handle(fn)` | `.then(ok => ..., err => ...)` 또는 `.finally(fn)` |
> | `future.get()` — 블로킹! | `await promise` — 논블로킹 (이벤트 루프를 양보) |
> | `future.join()` — 블로킹! | `await promise` |
>
> **가장 중요한 차이**: `CompletableFuture`는 `get()`/`join()` 호출 전까지 결과를 *꺼내지 않는다*. 하지만 Promise에서 `await`는 스레드를 블로킹하지 않는다. 이벤트 루프에 제어를 돌려주고, 결과가 준비되면 그 자리부터 다시 실행한다.
>
> **또 하나의 차이**: `CompletableFuture`는 명시적으로 실행기(`Executor`)를 지정하지 않으면 ForkJoinPool을 사용한다. Promise는 항상 이벤트 루프 위에서 마이크로태스크로 실행된다. "어느 스레드"라는 개념 자체가 없다.

### then/catch/finally 체이닝

Promise의 체이닝은 *각 단계가 새 Promise를 반환한다*는 원칙 위에 선다.

```typescript
fetch("https://api.example.com/users/1")
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();  // 이것도 Promise를 반환한다
  })
  .then(user => {
    console.log("사용자:", user.name);
    return user;
  })
  .catch(err => {
    console.error("에러 발생:", err.message);
    // catch도 값을 반환하면 체인이 이어진다
    return null;
  })
  .finally(() => {
    console.log("요청 완료 — 성공이든 실패든");
    // finally는 값을 반환해도 체인에 영향을 주지 않는다
  });
```

`.then(onFulfilled, onRejected)`처럼 두 번째 인자를 쓸 수도 있지만, `.catch(onRejected)`를 따로 쓰는 편이 읽기 훨씬 낫다. 두 인자 형태는 이전 단계의 에러만 잡고, 같은 `.then()` 안의 `onFulfilled`에서 발생한 에러는 잡지 못하기 때문에 더 안전하지도 않다.

한 가지 짚어두어야 할 점이 있다. `.then()` 안에서 *값을 반환하는 것*과 *Promise를 반환하는 것*은 체이닝에서 다르게 동작하지 않는다. 값을 반환하면 자동으로 `Promise.resolve(값)`으로 감싸진다. 이것이 바로 `.thenCompose()`를 따로 둔 Java와의 결정적인 차이다.

```typescript
// 이 두 코드는 체이닝에서 동일하게 동작한다
promise
  .then(v => v + 1)          // 숫자를 반환 → Promise<number>로 자동 래핑
  .then(v => Promise.resolve(v + 1));  // Promise를 반환 → 그대로 사용
```

> ### 📚 Java/Kotlin 시선 박스 ② — Reactor `Mono`/`Flux` ↔ Promise/Observable
>
> | Reactor `Mono<T>` | TypeScript `Promise<T>` |
> |---|---|
> | `Mono.just(v)` | `Promise.resolve(v)` |
> | `Mono.error(ex)` | `Promise.reject(err)` |
> | `.map(fn)` | `.then(fn)` (동기 변환) |
> | `.flatMap(fn)` | `.then(fn)` (비동기 변환, fn이 Promise 반환) |
> | `.onErrorResume(fn)` | `.catch(fn)` |
> | `.doFinally(fn)` | `.finally(fn)` |
> | `.subscribe()` — **구독해야 실행** | Promise는 **생성 즉시 실행** |
>
> **가장 큰 차이**: Reactor는 *콜드 스트림(cold stream)* 기반이다. `Mono`를 만들어도 `.subscribe()`하지 않으면 아무것도 실행되지 않는다. Promise는 생성자(`new Promise(executor)`)가 호출되는 순간 executor 함수가 *즉시* 실행된다. 이미 실행이 시작된 비동기 작업을 나타내는 것이다.
>
> ```typescript
> // Promise는 new 하는 순간 콘솔에 출력된다
> const p = new Promise(resolve => {
>   console.log("지금 바로 실행!");  // subscribe 없이도 출력됨
>   resolve(42);
> });
> ```
>
> Reactor로 오래 일한 사람에게 이 차이는 처음에 꽤 난감하다. "왜 이미 실행이 됐지?"라는 순간이 온다. `Promise.resolve(값)`은 이미 Fulfilled된 Promise를 반환하는 팩토리일 뿐이고, `new Promise(executor)`는 executor를 *즉시* 호출한다는 점을 기억해두자.
>
> | Reactor `Flux<T>` | RxJS `Observable<T>` |
> |---|---|
> | `Flux.just(1, 2, 3)` | `of(1, 2, 3)` |
> | `Flux.fromIterable(list)` | `from(list)` |
> | `.map(fn)` | `.pipe(map(fn))` |
> | `.filter(fn)` | `.pipe(filter(fn))` |
> | `.flatMap(fn)` | `.pipe(mergeMap(fn))` |
> | `.subscribe(onNext, onError, onComplete)` | `.subscribe({next, error, complete})` |
> | `Flux`는 Spring 통합 내장 | RxJS는 별도 라이브러리 |
>
> `Flux`와 RxJS `Observable`은 개념적으로 매우 가깝다. 둘 다 여러 값의 스트림이고, 콜드 스트림이며(구독해야 실행), `subscribe()`로 데이터를 소비한다. 연산자 이름만 달라서 불편할 뿐, 마음 구조는 같다.

---

## async/await — Promise 위의 문법 설탕

`async/await`는 ES2017(ES8)에 들어온 문법이다. Promise 체이닝을 동기식 코드처럼 읽히게 해준다. 핵심은 단 하나다. **`async` 함수는 항상 Promise를 반환한다. `await`는 Promise가 settled될 때까지 해당 async 함수의 실행을 일시 중단하고 이벤트 루프에 제어를 돌려준다.**

```typescript
// Promise 체이닝 스타일
function fetchUserProfile(userId: number): Promise<Profile> {
  return fetchUser(userId)
    .then(user => fetchPermissions(user.id))
    .then(permissions => buildProfile(user, permissions))  // 이런, user 스코프 문제!
    .catch(err => {
      throw new Error(`프로필 로드 실패: ${err.message}`);
    });
}

// async/await 스타일 — 훨씬 읽기 쉽다
async function fetchUserProfile(userId: number): Promise<Profile> {
  try {
    const user = await fetchUser(userId);
    const permissions = await fetchPermissions(user.id);  // user가 스코프에 있다
    return buildProfile(user, permissions);
  } catch (err) {
    throw new Error(`프로필 로드 실패: ${(err as Error).message}`);
  }
}
```

위 두 코드는 *기능적으로 동일하다*. `async/await`는 컴파일러가 Promise 체이닝으로 변환해주는 문법 설탕이다. 표면은 동기 코드처럼 생겼지만, `await` 시점에 이벤트 루프에 제어를 넘긴다.

### async 함수의 반환 타입

`async` 함수는 항상 `Promise<T>`를 반환한다. 안에서 `return 42`를 써도 실제 반환 타입은 `Promise<number>`다.

```typescript
async function greet(): Promise<string> {
  return "안녕하세요";  // 자동으로 Promise.resolve("안녕하세요") 가 된다
}

async function fail(): Promise<never> {
  throw new Error("실패");  // 자동으로 Promise.reject(new Error("실패")) 가 된다
}
```

TypeScript에서는 반환 타입을 명시하는 편이 낫다. 그래야 함수 내부에서 실수로 다른 타입을 반환할 때 컴파일러가 잡아준다.

> ### 📚 Java/Kotlin 시선 박스 ③ — Kotlin coroutine `suspend` ↔ async/await
>
> 표면적으로 Kotlin의 `suspend fun`과 TypeScript의 `async function`은 매우 비슷해 보인다.
>
> ```kotlin
> // Kotlin
> suspend fun fetchUser(id: Int): User {
>     val response = httpClient.get("/users/$id")  // suspend point
>     return response.body<User>()
> }
> ```
>
> ```typescript
> // TypeScript
> async function fetchUser(id: number): Promise<User> {
>     const response = await fetch(`/users/${id}`);  // await point
>     return response.json();
> }
> ```
>
> 둘 다 비동기 코드를 동기처럼 읽히게 한다. 둘 다 중간에 실행을 일시 중단하고 제어를 반환한다. 하지만 근본적인 차이가 있다.
>
> | 비교 | Kotlin `suspend` | TypeScript `async/await` |
> |---|---|---|
> | 컴파일 결과 | CPS(Continuation Passing Style) 변환 — suspend point마다 상태 머신 | Promise 체이닝으로 변환 |
> | 스케줄러 | `CoroutineDispatcher`로 선택 가능 (`Dispatchers.IO`, `Dispatchers.Main`) | 항상 이벤트 루프의 마이크로태스크 |
> | 취소 | `Job.cancel()` — 협조적 취소, suspend point마다 취소 확인 | `AbortController` — 라이브러리별 구현 필요 |
> | 구조적 동시성 | `CoroutineScope` — 부모가 취소되면 자식도 취소 | 없음 (직접 관리) |
> | `suspend` 전파 | `suspend`는 호출 스택을 따라 전파 | `async`는 선택적 — `await` 없이도 호출 가능 |
>
> Kotlin의 구조적 동시성(Structured Concurrency)은 JS에는 없다. `CoroutineScope`가 취소되면 그 안에서 실행 중인 모든 자식 코루틴도 자동으로 취소된다. TypeScript에서는 이것을 `AbortController`로 직접 구현해야 한다. (AbortSignal 절에서 자세히 다룬다.)
>
> 또 하나의 차이: `suspend fun`을 호출하려면 코루틴 컨텍스트가 필요하다 — `launch`, `async`, `runBlocking` 안에서만 호출할 수 있다. TypeScript에서 `async function`은 어디서든 호출할 수 있다. 다만 결과를 `await`하지 않으면 Promise가 공중에 떠 있게 된다 — 이것이 에러 처리의 함정으로 이어진다.

### await를 빠뜨리면 생기는 일

Java에서 `future.get()`을 빠뜨리면 그냥 Future 객체가 변수에 들어가고, 결과를 꺼내지 못한다. TypeScript에서 `await`를 빠뜨리면 비슷한 일이 일어나지만, 에러 처리가 걸린 경우 훨씬 더 난감한 결과를 낳는다.

```typescript
async function saveUser(user: User): Promise<void> {
  try {
    await db.save(user);
    console.log("저장 완료");
  } catch (err) {
    console.error("저장 실패:", err);
  }
}

// await를 깜빡했다
async function handler(): Promise<void> {
  saveUser(user);  // await 없음 — Promise를 만들고 즉시 다음 줄로 간다
  console.log("이미 다음 줄로 넘어왔다");
  // saveUser 내부의 에러가 catch에서 잡히지 않는다
  // 에러는 Unhandled Rejection이 된다
}
```

TypeScript와 ESLint의 `@typescript-eslint/no-floating-promises` 규칙이 이런 실수를 잡아준다. 프로젝트에 ESLint를 쓴다면 이 규칙을 켜두는 편이 낫다.

---

## 에러 흐름 — try/catch가 잡는 것과 못 잡는 것

비동기 에러 처리는 TypeScript에서 가장 많은 개발자가 발을 헛디디는 영역이다. 솔직하게 말하면, 이 부분은 Java/Kotlin보다 훨씬 더 주의가 필요하다.

> ### 🚧 함정 박스 — 비동기 에러는 어디로 가는가
>
> **Case 1: async 함수 안의 throw — 잘 잡힌다**
>
> ```typescript
> async function fetchData(): Promise<string> {
>   throw new Error("뭔가 잘못됨");
> }
>
> async function main() {
>   try {
>     const data = await fetchData();
>   } catch (err) {
>     console.log("잡혔다:", (err as Error).message);  // ✅ 잡힌다
>   }
> }
> ```
>
> **Case 2: `.then()` 체인 안의 throw — 잘 잡힌다**
>
> ```typescript
> fetchData()
>   .then(data => {
>     throw new Error("then 안에서 에러");
>   })
>   .catch(err => {
>     console.log("잡혔다:", err.message);  // ✅ 잡힌다
>   });
> ```
>
> **Case 3: await 없는 Promise — 잡히지 않는다** ⚠️
>
> ```typescript
> async function main() {
>   try {
>     fetchData();  // await 없음
>   } catch (err) {
>     console.log("잡힌다고 생각하겠지만");  // ❌ 잡히지 않는다
>   }
> }
>
> // fetchData()의 에러는 Unhandled Rejection이 된다
> ```
>
> **Case 4: setTimeout 콜백 안의 throw — 잡히지 않는다** ⚠️
>
> ```typescript
> async function main() {
>   try {
>     setTimeout(() => {
>       throw new Error("타이머 콜백 에러");
>     }, 100);
>   } catch (err) {
>     console.log("절대 여기 오지 않는다");  // ❌ 잡히지 않는다
>   }
> }
>
> // setTimeout 콜백은 다른 이벤트 루프 tick에서 실행된다
> // try/catch 블록이 이미 끝난 이후이므로 잡을 수 없다
> ```
>
> **Case 5: Promise 생성자 외부의 throw — 잡히지 않는다** ⚠️
>
> ```typescript
> // 이건 Promise가 아니다 — 일반 예외
> function badFunction() {
>   const p = new Promise((resolve, reject) => {
>     resolve(42);
>   });
>   throw new Error("Promise 밖에서 던짐");  // 동기 예외
>   return p;
> }
>
> // 이것은 잡힌다 — 동기 예외니까
> try {
>   badFunction();
> } catch (err) {
>   console.log("동기 예외라 잡힌다");  // ✅ 잡힌다
> }
> ```
>
> **핵심 규칙**: `await`된 Promise 안의 에러는 try/catch로 잡힌다. `await`하지 않은 Promise의 에러는 잡히지 않는다. `setTimeout`/`setInterval` 콜백 안의 에러는 async/await와 무관하게 잡히지 않는다.

### Unhandled Rejection — 조용히 사라지거나 프로세스를 죽인다

`await`하지 않은 Promise에서 에러가 나면 어떻게 될까? 브라우저에서는 `unhandledrejection` 이벤트가 발생한다. Node.js에서는 버전에 따라 동작이 달랐다.

- **Node.js 14 이전**: 경고만 출력하고 계속 실행 (조용히 넘어감)
- **Node.js 15+**: 기본적으로 **프로세스 종료**

프로세스가 죽는다. 운영 환경이라면 찜찜함을 넘어서 실제 장애다.

```typescript
// Node.js에서 Unhandled Rejection 전역 처리
process.on("unhandledRejection", (reason, promise) => {
  console.error("처리되지 않은 Promise 거부:", reason);
  // 이 시점에 로깅을 하고 프로세스를 안전하게 종료할 수 있다
  process.exit(1);
});

// 브라우저에서
window.addEventListener("unhandledrejection", (event) => {
  console.error("처리되지 않은 거부:", event.reason);
  event.preventDefault();  // 브라우저 기본 에러 처리 막기
});
```

Java의 `Future.get()`과 비교해보면 어떻게 다를까? Java에서 `Future.get()`을 호출하지 않으면 `ExecutionException`이 그냥 묻힌다 — 하지만 적어도 스레드는 계속 살아있고 다른 코드는 돌아간다. Node.js에서는 Unhandled Rejection이 *프로세스 자체를 죽일 수 있다*는 점이 다르다. 그래서 더 주의가 필요하다.

실무에서 권장하는 패턴은 세 가지다.

```typescript
// 패턴 1: void 연산자로 의도적으로 무시함을 명시
void somePromise().catch(logger.error);

// 패턴 2: 항상 await, catch 붙이기
async function safeWrapper() {
  try {
    await riskyOperation();
  } catch (err) {
    logger.error("안전하게 로깅", err);
  }
}

// 패턴 3: 전역 핸들러 + 구조적 종료
process.on("unhandledRejection", (reason) => {
  logger.fatal("미처리 거부", { reason });
  // 그레이스풀 셧다운 후 종료
  gracefulShutdown().then(() => process.exit(1));
});
```

---

## AbortSignal과 취소 — 잊혀지는 자리

많은 학습서가 `AbortController`를 `fetch` 예제로 잠깐 소개하고 넘어간다. 하지만 Java/Kotlin 개발자에게 취소 패턴은 매우 중요하다. Spring WebFlux에서는 구독 해제(`dispose()`)를 Reactor가 관리해준다. Kotlin에서는 `Job.cancel()`이 있다. TypeScript에서는 `AbortController`가 그 역할을 한다 — 하지만 훨씬 더 명시적으로 직접 구현해야 한다.

### AbortController와 AbortSignal 기본

```typescript
// AbortController: 취소 신호를 보내는 주체
const controller = new AbortController();

// AbortSignal: 취소 신호를 받는 토큰
const signal = controller.signal;

// 5초 후 자동 취소
const timeoutId = setTimeout(() => controller.abort("5초 타임아웃"), 5000);

try {
  const response = await fetch("https://api.example.com/data", { signal });
  
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  
  const data = await response.json();
  clearTimeout(timeoutId);  // 성공 시 타임아웃 해제
  return data;
} catch (err) {
  if (err instanceof DOMException && err.name === "AbortError") {
    console.log("요청이 취소되었습니다:", controller.signal.reason);
  } else {
    throw err;
  }
}
```

`abort()` 메서드를 호출하면 `signal.aborted`가 `true`가 되고, `signal.reason`에 취소 이유가 저장된다. `fetch`는 이 신호를 감지해 요청을 중단하고 `AbortError`를 던진다.

### AbortSignal.timeout — 내장 타임아웃

Node.js 17+ / 최신 브라우저에서는 더 간단한 방법이 생겼다.

```typescript
// 3초 타임아웃을 가진 signal 직접 생성
const response = await fetch("https://api.example.com/data", {
  signal: AbortSignal.timeout(3000)
});
```

`AbortSignal.timeout(ms)`는 지정된 시간 후 자동으로 abort되는 signal을 반환한다. `AbortController`를 따로 만들고 타임아웃을 관리하는 보일러플레이트가 사라진다.

### 커스텀 함수에서 AbortSignal 지원하기

`fetch`뿐만 아니라 자신이 만드는 함수에도 `AbortSignal`을 지원할 수 있다.

```typescript
async function downloadWithProgress(
  url: string,
  onProgress: (loaded: number, total: number) => void,
  signal?: AbortSignal
): Promise<Blob> {
  const response = await fetch(url, { signal });
  
  if (!response.body) throw new Error("스트림 없음");
  
  const contentLength = Number(response.headers.get("Content-Length") ?? 0);
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let loaded = 0;
  
  while (true) {
    // 취소 신호 확인
    if (signal?.aborted) {
      reader.cancel();
      throw new DOMException("다운로드 취소됨", "AbortError");
    }
    
    const { done, value } = await reader.read();
    
    if (done) break;
    
    chunks.push(value);
    loaded += value.length;
    onProgress(loaded, contentLength);
  }
  
  return new Blob(chunks);
}

// 사용 예
const controller = new AbortController();

downloadButton.addEventListener("click", async () => {
  try {
    const blob = await downloadWithProgress(
      "/large-file.zip",
      (loaded, total) => updateProgressBar(loaded / total),
      controller.signal
    );
    saveFile(blob);
  } catch (err) {
    if (err instanceof DOMException && err.name === "AbortError") {
      showMessage("다운로드가 취소되었습니다");
    } else {
      showError(err);
    }
  }
});

cancelButton.addEventListener("click", () => {
  controller.abort("사용자가 취소");
});
```

### AbortSignal.any — 여러 신호 합치기

Node.js 20+ / 최신 브라우저에서는 `AbortSignal.any(signals)`로 여러 신호를 OR 조건으로 합칠 수 있다.

```typescript
// 타임아웃 또는 사용자 취소 중 하나가 먼저 오면 취소
const userController = new AbortController();
const combinedSignal = AbortSignal.any([
  userController.signal,
  AbortSignal.timeout(30_000)
]);

const data = await fetch(url, { signal: combinedSignal });
```

Java/Kotlin 비교 관점에서 정리하면 이렇다.

| 취소 메커니즘 | TypeScript | Java/Kotlin |
|---|---|---|
| 취소 토큰 | `AbortSignal` | Kotlin `Job`, Reactor `Disposable` |
| 취소 발동 | `AbortController.abort()` | `Job.cancel()`, `dispose()` |
| 타임아웃 | `AbortSignal.timeout(ms)` | Kotlin `withTimeout`, Reactor `timeout()` |
| 구조적 취소 | 직접 구현 | Kotlin CoroutineScope 자동 전파 |
| 취소 확인 | `signal.aborted` 체크 | Kotlin `isActive`, `ensureActive()` |

Kotlin의 구조적 동시성에 익숙한 사람이라면 TypeScript의 취소 모델이 좀 번거롭게 느껴질 수 있다. 맞다. JS 생태계에는 Kotlin처럼 언어 수준에서 취소를 보장하는 메커니즘이 없다. `signal`을 함수 시그니처로 전달하고, 각 비동기 함수가 그것을 *협조적으로* 체크해야 한다. 이 점은 솔직히 Kotlin이 앞선 부분이다.

---

## Observable (RxJS) — 여러 값의 스트림

Promise는 *단 하나*의 값(또는 에러)을 표현한다. 하지만 클릭 이벤트, 웹소켓 메시지, 센서 데이터 스트림처럼 *시간에 걸쳐 여러 값이 흘러오는* 상황은 어떻게 처리할까?

이 문제를 위해 나온 것이 RxJS의 `Observable`이다.

### Observable의 기본 구조

```typescript
import { Observable, Subject, interval, fromEvent } from "rxjs";
import { map, filter, take, debounceTime, switchMap } from "rxjs/operators";

// Observable 직접 만들기
const countdown$ = new Observable<number>(subscriber => {
  let count = 3;
  const id = setInterval(() => {
    subscriber.next(count--);  // 값 발행
    if (count < 0) {
      clearInterval(id);
      subscriber.complete();   // 완료
    }
  }, 1000);
  
  // cleanup 함수 — unsubscribe 시 실행됨
  return () => {
    clearInterval(id);
    console.log("cleanup 완료");
  };
});

// 구독
const subscription = countdown$.subscribe({
  next: value => console.log(`카운트다운: ${value}`),
  error: err => console.error("에러:", err),
  complete: () => console.log("완료!")
});

// 나중에 구독 해제
setTimeout(() => subscription.unsubscribe(), 2500);
```

`$` 접미사는 RxJS 커뮤니티의 관행이다 — Observable임을 나타낸다.

### 실전 패턴 — 자동완성 검색

Observable의 진가가 드러나는 예제를 보자. 입력창의 자동완성 — 사용자가 타이핑할 때마다 API를 호출하되, 이전 요청을 취소하고 입력이 멈춘 후에만 검색하는 패턴이다.

```typescript
import { fromEvent } from "rxjs";
import { debounceTime, distinctUntilChanged, switchMap, catchError } from "rxjs/operators";
import { from, EMPTY } from "rxjs";

const searchInput = document.getElementById("search") as HTMLInputElement;

const search$ = fromEvent(searchInput, "input").pipe(
  map(event => (event.target as HTMLInputElement).value),
  debounceTime(300),          // 300ms 동안 입력이 없을 때만 통과
  distinctUntilChanged(),     // 이전과 같은 값이면 무시
  switchMap(query => {        // 이전 요청 취소하고 새 요청 시작
    if (!query.trim()) return EMPTY;  // 빈 검색어 무시
    return from(
      fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
    ).pipe(
      catchError(err => {
        console.error("검색 에러:", err);
        return EMPTY;  // 에러 시 빈 결과
      })
    );
  })
);

const sub = search$.subscribe(results => {
  renderResults(results);
});

// 컴포넌트 해제 시
// sub.unsubscribe();
```

`switchMap`이 핵심이다. 이전 Observable을 자동으로 취소(unsubscribe)하고 새 것으로 교체한다. Reactor의 `Flux.switchMap()`과 정확히 같은 개념이다.

### Hot vs Cold Observable

Reactor에서 `Flux`와 `ConnectableFlux`의 차이를 아는 사람이라면 이 개념이 친숙할 것이다.

- **Cold Observable**: 구독할 때마다 새 실행이 시작된다. 각 구독자가 전체 스트림을 받는다. (Reactor의 `Mono`/`Flux` 기본 동작과 유사)
- **Hot Observable**: 이미 진행 중인 스트림에 구독자가 *참여*한다. 구독 시점 이후의 값만 받는다. (웹소켓, 이벤트, `Subject`)

```typescript
import { Subject } from "rxjs";

// Subject는 Hot Observable이자 Observer다
const subject$ = new Subject<string>();

// 첫 번째 구독자
subject$.subscribe(v => console.log("구독자 A:", v));

subject$.next("첫 번째 값");  // A만 받는다

// 두 번째 구독자 — 이후부터만 받는다
subject$.subscribe(v => console.log("구독자 B:", v));

subject$.next("두 번째 값");   // A와 B 모두 받는다
subject$.next("세 번째 값");   // A와 B 모두 받는다
subject$.complete();
```

### RxJS의 주요 연산자 맵

Reactor를 쓰던 개발자라면 연산자 이름이 다를 뿐, 개념은 같다.

| Reactor | RxJS | 설명 |
|---|---|---|
| `map()` | `map()` | 동기 변환 |
| `flatMap()` | `mergeMap()` | 비동기 변환, 순서 보장 없음 |
| `concatMap()` | `concatMap()` | 비동기 변환, 순서 보장 |
| `switchMap()` | `switchMap()` | 이전 취소, 새 것으로 교체 |
| `filter()` | `filter()` | 조건부 통과 |
| `take(n)` | `take(n)` | n개만 받고 완료 |
| `takeUntil(signal)` | `takeUntil(notifier$)` | 신호 오면 완료 |
| `debounce()` | `debounceTime(ms)` | 입력 안정화 |
| `zip()` | `zip()` | 쌍으로 합치기 |
| `combineLatest()` | `combineLatest()` | 최신 값 조합 |
| `shareReplay()` | `shareReplay()` | 멀티캐스트 |

---

## AsyncIterator와 `for await...of`

RxJS Observable은 강력하지만 별도 라이브러리다. ECMAScript 표준도 비동기 스트림을 다루는 방법을 정의했는데, 바로 **AsyncIterator**다.

### AsyncIterator 프로토콜

```typescript
// AsyncIterator를 구현하는 객체는 이 인터페이스를 따른다
interface AsyncIterator<T> {
  next(): Promise<{ done: boolean; value: T }>;
  return?(value?: any): Promise<{ done: boolean; value: any }>;
  throw?(e?: any): Promise<{ done: boolean; value: any }>;
}

interface AsyncIterable<T> {
  [Symbol.asyncIterator](): AsyncIterator<T>;
}
```

실제로 직접 만들 일은 적고, `async generator`로 만드는 것이 훨씬 편하다.

### async generator — AsyncIterator를 쉽게 만들기

```typescript
// async generator 함수는 AsyncIterator를 반환한다
async function* readLines(url: string): AsyncGenerator<string> {
  const response = await fetch(url);
  if (!response.body) throw new Error("스트림 없음");
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  
  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        if (buffer) yield buffer;  // 마지막 줄
        break;
      }
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";  // 미완성 줄은 버퍼에 남긴다
      
      for (const line of lines) {
        yield line;  // 완성된 줄마다 yield
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// for await...of로 소비
async function processLogFile(url: string) {
  let errorCount = 0;
  
  for await (const line of readLines(url)) {
    if (line.includes("ERROR")) {
      errorCount++;
      console.log("에러 발견:", line);
    }
  }
  
  console.log(`총 에러 수: ${errorCount}`);
}
```

`for await...of`는 AsyncIterator를 소비하는 문법이다. 각 iteration마다 `await`가 내장되어 있다.

### Node.js Streams와 AsyncIterator

Node.js의 Readable 스트림은 AsyncIterator 프로토콜을 구현한다. 파일을 라인 단위로 읽는 것이 매우 자연스러워졌다.

```typescript
import { createReadStream } from "fs";
import { createInterface } from "readline";

async function processLargeFile(filePath: string): Promise<void> {
  const fileStream = createReadStream(filePath);
  const rl = createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });
  
  let lineNumber = 0;
  
  // readline이 AsyncIterator를 구현하므로 for await...of 사용 가능
  for await (const line of rl) {
    lineNumber++;
    
    if (line.trim() === "") continue;
    
    await processLine(lineNumber, line);
  }
  
  console.log(`총 ${lineNumber}줄 처리 완료`);
}
```

Java에서 `Files.lines(path)` + `Stream.forEach()`로 처리하던 것과 유사한 패턴이다. 다만 Java는 동기 스트림이고, 이것은 비동기다.

### AsyncIterator vs Observable

둘 다 여러 값의 스트림이지만 차이가 있다.

| 비교 | AsyncIterator | RxJS Observable |
|---|---|---|
| 표준 여부 | ECMAScript 표준 | 별도 라이브러리 |
| Pull vs Push | **Pull** — 소비자가 요청 | **Push** — 생산자가 능동적으로 발행 |
| 배압(backpressure) | 자연스럽게 지원 | `operators`로 제어 필요 |
| 에러 처리 | try/catch | `.catchError()` |
| 완료 | `done: true` | `complete()` |
| 연산자 | 없음 (직접 구현) | 풍부한 연산자 생태계 |
| 적합한 상황 | 순차 처리, 파일/DB | 이벤트, 실시간, 복잡한 스트림 |

간단한 순차 처리나 파일/DB 스트리밍이라면 AsyncIterator로 충분하다. 복잡한 이벤트 조합이나 실시간 데이터 처리라면 RxJS가 낫다.

---

## 병렬 패턴 — Promise.all/allSettled/race/any 4종

비동기 작업을 *병렬로* 실행하고 결과를 모아야 할 때는 Promise 정적 메서드 4개를 쓴다. Java의 `CompletableFuture.allOf()`, `Future`의 `invokeAll()`에 해당하는 도구들이다.

### Promise.all — 전부 성공해야 한다

```typescript
// 세 API를 병렬로 호출하고 전부 완료되면 결과 반환
async function fetchDashboardData(userId: number) {
  const [user, orders, notifications] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchNotifications(userId),
  ]);
  
  return { user, orders, notifications };
}
```

하나라도 실패하면 Promise.all 전체가 즉시 거부된다. 나머지 Promise는 취소되지 않고 계속 실행되지만, 그 결과는 무시된다. Java의 `CompletableFuture.allOf()`와 비슷하지만, 타입 추론이 튜플로 정확하게 된다는 점이 더 편하다.

타입 추론이 어떻게 되는지 보자.

```typescript
// TypeScript는 Promise.all의 타입을 정확히 추론한다
const result = await Promise.all([
  fetchUser(1),        // Promise<User>
  fetchOrders(1),      // Promise<Order[]>
  Promise.resolve(42), // Promise<number>
]);

// result의 타입은 [User, Order[], number] — 튜플!
const [user, orders, count] = result;
// user: User, orders: Order[], count: number
```

### Promise.allSettled — 성패 무관하게 전부 기다린다

`Promise.all`과 달리, 하나가 실패해도 나머지를 기다린다. 각 결과가 `fulfilled` 또는 `rejected` 상태로 온다.

```typescript
async function fetchMultipleExchangeRates(currencies: string[]) {
  const results = await Promise.allSettled(
    currencies.map(currency => fetchExchangeRate(currency))
  );
  
  const rates: Record<string, number> = {};
  const failures: string[] = [];
  
  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      rates[currencies[index]] = result.value;
    } else {
      failures.push(currencies[index]);
      console.warn(`환율 조회 실패: ${currencies[index]}`, result.reason);
    }
  });
  
  if (failures.length > 0) {
    console.warn(`${failures.length}개 통화 조회 실패`);
  }
  
  return rates;
}
```

일부 실패가 허용되는 상황 — 여러 소스에서 데이터를 가져오되, 일부 소스가 죽어도 나머지로 처리하는 경우 — 에 적합하다.

### Promise.race — 가장 빠른 하나

여러 Promise 중 가장 먼저 settled되는 것을 쓴다. 성공이든 실패든 상관없다.

```typescript
// 타임아웃 구현 — AbortSignal 없이
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error(`${ms}ms 타임아웃`)), ms)
  );
  
  return Promise.race([promise, timeout]);
}

// 또는 AbortSignal로 더 깔끔하게
const result = await withTimeout(fetchData(), 5000);
```

단, `Promise.race`는 "패한" Promise를 취소하지 않는다. 단지 결과를 무시할 뿐이다. 타임아웃 같은 경우에 `Promise.race` + `AbortSignal`을 함께 쓰면 실제 요청도 취소할 수 있다.

```typescript
async function fetchWithTimeout<T>(
  promiseFactory: (signal: AbortSignal) => Promise<T>,
  ms: number
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(`${ms}ms 초과`), ms);
  
  try {
    return await promiseFactory(controller.signal);
  } finally {
    clearTimeout(timeoutId);
  }
}

// 사용
const user = await fetchWithTimeout(
  signal => fetchUser(userId, signal),
  3000
);
```

### Promise.any — 하나라도 성공하면 된다

`Promise.race`와 비슷하지만, 성공한 것을 기다린다. 모두 실패해야 거부된다.

```typescript
// 여러 CDN에서 파일을 받고 가장 빠른 것을 쓴다
async function fetchFromFastestCDN(path: string): Promise<Response> {
  const cdnUrls = [
    `https://cdn1.example.com${path}`,
    `https://cdn2.example.com${path}`,
    `https://cdn3.example.com${path}`,
  ];
  
  try {
    return await Promise.any(
      cdnUrls.map(url => fetch(url))
    );
  } catch (err) {
    // AggregateError — 모든 Promise가 거부됨
    if (err instanceof AggregateError) {
      throw new Error(`모든 CDN 실패: ${err.errors.map(e => e.message).join(", ")}`);
    }
    throw err;
  }
}
```

`Promise.any`가 모두 실패하면 `AggregateError`가 던져진다. 이것은 모든 에러를 `errors` 배열에 담는다.

### 4종 비교 요약

```typescript
const p1 = delay(100).then(() => "A");    // 100ms 후 성공
const p2 = delay(200).then(() => { throw new Error("B 실패"); });  // 200ms 후 실패
const p3 = delay(300).then(() => "C");    // 300ms 후 성공

// Promise.all — 하나라도 실패하면 전체 실패
await Promise.all([p1, p2, p3]);
// → 200ms 후 Error("B 실패")로 거부

// Promise.allSettled — 전부 기다리고 상태 반환
await Promise.allSettled([p1, p2, p3]);
// → 300ms 후 [
//     { status: "fulfilled", value: "A" },
//     { status: "rejected", reason: Error("B 실패") },
//     { status: "fulfilled", value: "C" }
//   ]

// Promise.race — 가장 빠른 것 (성공/실패 무관)
await Promise.race([p1, p2, p3]);
// → 100ms 후 "A"

// Promise.any — 가장 빠른 성공
await Promise.any([p1, p2, p3]);
// → 100ms 후 "A" (p2가 실패해도 p1이 성공했으므로)
```

---

## 실전 패턴 — 재시도, 쓰로틀링, 동시성 제한

Promise 4종을 조합하면 실무에서 자주 쓰는 패턴들을 만들 수 있다.

### 재시도 (Retry with Exponential Backoff)

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxAttempts: number;
    initialDelay: number;
    backoffFactor: number;
    signal?: AbortSignal;
  }
): Promise<T> {
  const { maxAttempts, initialDelay, backoffFactor, signal } = options;
  let lastError: Error;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    if (signal?.aborted) {
      throw new DOMException("재시도 취소됨", "AbortError");
    }
    
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      
      if (attempt < maxAttempts) {
        const delay = initialDelay * Math.pow(backoffFactor, attempt - 1);
        console.warn(`시도 ${attempt} 실패, ${delay}ms 후 재시도:`, err);
        
        await new Promise<void>((resolve, reject) => {
          const id = setTimeout(resolve, delay);
          signal?.addEventListener("abort", () => {
            clearTimeout(id);
            reject(new DOMException("대기 중 취소됨", "AbortError"));
          }, { once: true });
        });
      }
    }
  }
  
  throw lastError!;
}

// 사용
const data = await withRetry(
  () => fetchData(url),
  { maxAttempts: 3, initialDelay: 1000, backoffFactor: 2 }
);
```

### 동시성 제한 (Concurrency Limiting)

100개의 URL을 동시에 모두 fetch하면 서버에 과부하가 걸린다. N개씩 제한해서 처리하자.

```typescript
async function* chunks<T>(arr: T[], size: number): AsyncGenerator<T[]> {
  for (let i = 0; i < arr.length; i += size) {
    yield arr.slice(i, i + size);
  }
}

async function fetchWithConcurrencyLimit<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  concurrency: number
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let index = 0;
  
  async function worker() {
    while (index < items.length) {
      const currentIndex = index++;
      results[currentIndex] = await fn(items[currentIndex]);
    }
  }
  
  // concurrency개의 워커를 동시에 실행
  await Promise.all(
    Array.from({ length: concurrency }, () => worker())
  );
  
  return results;
}

// 사용 — 5개씩 병렬로 처리
const results = await fetchWithConcurrencyLimit(
  urls,
  url => fetch(url).then(r => r.json()),
  5
);
```

Reactor에서 `Flux.flatMap(fn, 5)`로 동시성을 제한하던 것과 같은 효과다.

### 쓰로틀링과 디바운싱 (직접 구현)

RxJS 없이 Promise로 구현한다.

```typescript
// Debounce — 마지막 호출 후 delay ms 지나야 실행
function debounce<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let pendingResolve: ((value: ReturnType<T>) => void) | null = null;
  let pendingReject: ((reason: any) => void) | null = null;
  
  return function (...args: Parameters<T>): Promise<ReturnType<T>> {
    if (timeoutId) clearTimeout(timeoutId);
    
    return new Promise((resolve, reject) => {
      pendingResolve = resolve as any;
      pendingReject = reject;
      
      timeoutId = setTimeout(async () => {
        try {
          const result = await fn(...args);
          pendingResolve?.(result);
        } catch (err) {
          pendingReject?.(err);
        }
      }, delay);
    });
  };
}

const debouncedSearch = debounce(searchAPI, 300);
```

---

## 타입스크립트로 비동기 타입 다루기

### Promise 타입 추론

TypeScript는 Promise의 타입 매개변수를 잘 추론한다.

```typescript
// 추론 가능 — 명시 불필요
async function fetchUser(id: number) {
  const response = await fetch(`/users/${id}`);
  return response.json() as Promise<User>;
}
// 반환 타입: Promise<User>

// 명시 권장 — 인터페이스 계약이 있을 때
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/users/${id}`);
  const data: unknown = await response.json();
  
  // 런타임 검증 (zod 등)
  return UserSchema.parse(data);
}
```

### `Awaited<T>` 유틸리티 타입

Promise에서 타입을 꺼낼 때 `Awaited<T>`를 쓴다.

```typescript
type FetchResult = Awaited<ReturnType<typeof fetchUser>>;
// FetchResult = User

// 중첩 Promise도 평탄화
type Unwrapped = Awaited<Promise<Promise<string>>>;
// Unwrapped = string
```

### 에러 타입 처리

TypeScript의 catch 블록에서 `err`의 타입은 `unknown`이다. Java처럼 예외 타입을 선언할 수 없다.

```typescript
try {
  await riskyOperation();
} catch (err) {
  // err는 unknown — 타입 좁히기가 필요하다
  
  if (err instanceof Error) {
    console.error(err.message);
    console.error(err.stack);
  } else if (typeof err === "string") {
    console.error(err);
  } else {
    console.error("알 수 없는 에러:", err);
  }
}
```

커스텀 에러 클래스를 만들면 더 구조적으로 처리할 수 있다.

```typescript
class ApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly requestId?: string
  ) {
    super(message);
    this.name = "ApiError";
    // Node.js에서 스택 트레이스 보정
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ApiError);
    }
  }
}

class NetworkError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message, { cause });
    this.name = "NetworkError";
  }
}

async function apiCall<T>(url: string): Promise<T> {
  let response: Response;
  
  try {
    response = await fetch(url);
  } catch (err) {
    throw new NetworkError("네트워크 오류", err instanceof Error ? err : undefined);
  }
  
  if (!response.ok) {
    throw new ApiError(
      `API 오류: ${response.statusText}`,
      response.status,
      response.headers.get("X-Request-ID") ?? undefined
    );
  }
  
  return response.json();
}

// 사용 시 타입 좁히기
try {
  const user = await apiCall<User>("/users/1");
} catch (err) {
  if (err instanceof ApiError) {
    console.error(`API ${err.statusCode}:`, err.message);
    if (err.statusCode === 401) redirectToLogin();
  } else if (err instanceof NetworkError) {
    console.error("네트워크:", err.message, err.cause);
    showOfflineMessage();
  } else {
    throw err;  // 알 수 없는 에러는 다시 던진다
  }
}
```

### Result 타입 패턴

예외를 던지는 대신 Result 타입을 반환하는 패턴도 점점 많이 쓰인다. Kotlin의 `Result<T>`와 유사하다.

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeApiCall<T>(url: string): Promise<Result<T>> {
  try {
    const data = await apiCall<T>(url);
    return { ok: true, value: data };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err : new Error(String(err)) };
  }
}

// 사용 — 예외 없이 분기 처리
const result = await safeApiCall<User>("/users/1");

if (result.ok) {
  console.log("사용자:", result.value.name);
} else {
  console.error("실패:", result.error.message);
}
```

Effect-ts나 neverthrow 같은 라이브러리가 이 패턴을 더 정교하게 구현해준다.

---

## 실전 예제 — API 클라이언트 구현

지금까지 배운 모든 것을 통합한 실전 예제다. 재시도, 타임아웃, 취소, 에러 처리를 모두 갖춘 API 클라이언트를 만들어보자.

```typescript
interface RequestConfig {
  method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  body?: unknown;
  headers?: Record<string, string>;
  signal?: AbortSignal;
  timeout?: number;
  retries?: number;
}

interface ApiClientOptions {
  baseUrl: string;
  defaultTimeout: number;
  defaultRetries: number;
  onError?: (err: Error, url: string) => void;
}

class ApiClient {
  constructor(private readonly options: ApiClientOptions) {}
  
  async request<T>(path: string, config: RequestConfig = {}): Promise<T> {
    const {
      method = "GET",
      body,
      headers = {},
      signal,
      timeout = this.options.defaultTimeout,
      retries = this.options.defaultRetries,
    } = config;
    
    const url = `${this.options.baseUrl}${path}`;
    
    // 타임아웃과 사용자 취소 신호 합치기
    const signals: AbortSignal[] = [AbortSignal.timeout(timeout)];
    if (signal) signals.push(signal);
    const combinedSignal = AbortSignal.any(signals);
    
    return withRetry(
      async () => {
        const response = await fetch(url, {
          method,
          headers: {
            "Content-Type": "application/json",
            ...headers,
          },
          body: body ? JSON.stringify(body) : undefined,
          signal: combinedSignal,
        });
        
        if (!response.ok) {
          const errorBody = await response.text().catch(() => "");
          throw new ApiError(
            `${method} ${path} 실패: ${response.statusText}`,
            response.status,
            response.headers.get("X-Request-ID") ?? undefined
          );
        }
        
        if (response.status === 204) return undefined as T;
        return response.json() as Promise<T>;
      },
      {
        maxAttempts: retries,
        initialDelay: 500,
        backoffFactor: 2,
        signal: combinedSignal,
      }
    );
  }
  
  get<T>(path: string, config?: RequestConfig): Promise<T> {
    return this.request<T>(path, { ...config, method: "GET" });
  }
  
  post<T>(path: string, body: unknown, config?: RequestConfig): Promise<T> {
    return this.request<T>(path, { ...config, method: "POST", body });
  }
}

// 사용
const api = new ApiClient({
  baseUrl: "https://api.example.com",
  defaultTimeout: 10_000,
  defaultRetries: 3,
});

// 취소 가능한 요청
const controller = new AbortController();
const user = await api.get<User>("/users/1", { signal: controller.signal });

// 5초 후 취소
setTimeout(() => controller.abort("페이지 벗어남"), 5000);
```

---

## 비동기 테스트 패턴 맛보기

비동기 코드 테스트의 핵심은 *Promise를 반환하거나 async를 쓰는 것*이다. 자세한 내용은 14장에서 다루지만, 기본 패턴만 짚어두자.

```typescript
import { describe, it, expect, vi } from "vitest";

describe("fetchUserProfile", () => {
  it("성공 시 프로필을 반환한다", async () => {
    // Arrange
    vi.spyOn(global, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ id: 1, name: "Alice" }))
    );
    
    // Act
    const profile = await fetchUserProfile(1);
    
    // Assert
    expect(profile.name).toBe("Alice");
  });
  
  it("API 실패 시 에러를 던진다", async () => {
    vi.spyOn(global, "fetch").mockResolvedValue(
      new Response(null, { status: 404 })
    );
    
    await expect(fetchUserProfile(1)).rejects.toThrow(ApiError);
  });
  
  it("타임아웃 시 AbortError가 발생한다", async () => {
    vi.spyOn(global, "fetch").mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 10_000))  // 느린 응답
    );
    
    const fetchWithShortTimeout = () =>
      fetchWithTimeout(signal => fetchUserProfile(1, signal), 100);
    
    await expect(fetchWithShortTimeout()).rejects.toThrow();
  });
});
```

> **📖 더 깊이 가려면**
>
> 비동기 코드 테스트 패턴 — fake timer, mock vs stub, async error 검증, Promise.all 테스트 — 은 14장에서 자세히 다룬다. 특히 `vi.useFakeTimers()`로 setTimeout을 제어하는 방법과, msw(Mock Service Worker)로 fetch를 인터셉트하는 패턴이 실무에서 자주 쓰인다.

---

## 마무리

비동기 모델은 TypeScript를 배우면서 가장 시간이 걸리는 부분 중 하나다. Java/Kotlin의 비동기 모델이 이미 머릿속에 자리 잡혀 있어서, 겉으로 비슷해 보이는 Promise가 실제로는 다르게 동작할 때 혼란이 온다. 특히 두 가지를 꼭 기억해두자.

**첫째, Promise는 생성 즉시 실행된다.** Mono처럼 구독 전에 멈춰있지 않는다. `await`를 빠뜨리면 Promise가 허공을 떠다니고, 그 안의 에러가 Unhandled Rejection이 된다. Node.js 15+에서는 그것이 프로세스 종료로 이어진다.

**둘째, try/catch는 만능이 아니다.** `await`된 비동기 코드의 에러는 잡힌다. `setTimeout` 콜백이나 `await`하지 않은 Promise의 에러는 잡히지 않는다. 이 규칙을 체화하면 비동기 에러 디버깅이 훨씬 빨라진다.

취소 패턴은 Kotlin만큼 매끄럽지 않다. 하지만 `AbortController`와 `AbortSignal`을 꼼꼼히 전달하면 실용적인 수준의 취소는 충분히 구현된다. 번거롭더라도 시간이 지남에 따라 익숙해진다.

Observable과 AsyncIterator는 필요할 때 꺼내는 도구다. 단순한 비동기 요청은 Promise와 async/await로 충분하다. 이벤트 스트림이나 실시간 데이터가 필요해지면 그때 RxJS를 꺼내도 늦지 않다.

다음 장에서는 모듈 시스템과 빌드 도구로 넘어간다. CommonJS와 ESM이 공존하는 혼란스러운 세계, `tsconfig.json`의 핵심 옵션들, 그리고 빌드 파이프라인을 어떻게 구성하는지 살펴보자. 비동기 코드를 짤 줄 알게 되었다면, 이제 그 코드를 배포 가능한 형태로 묶는 법을 알아야 한다.

---

> 7장에서 비동기 모델의 전모를 익혔다. 이제 그 코드를 실제로 빌드하고 배포하는 환경으로 눈을 돌리자. `package.json`, `tsconfig.json`, `vite.config.ts`, `.eslintrc.cjs` — 왜 Spring의 `build.gradle` 하나와 달리 설정 파일이 이렇게 많은가. 그 역사적 이유와 의도적 선택의 지형도를 8장에서 펼쳐보자.

# 8장. 빌드 도구가 왜 이렇게 많은가 — 모듈·패키지·번들러·런타임의 분열

Spring 프로젝트를 새로 시작한다고 상상해보자. `build.gradle`을 열고 의존성을 적는다. Gradle이 Maven Central에서 JAR를 가져오고, 컴파일하고, 테스트하고, WAR를 만들어준다. 하나의 도구가 이 모든 과정을 담당한다. 설정 파일 하나, 명령어 하나, 신뢰할 수 있는 중앙 저장소 하나.

그런데 TypeScript 프로젝트를 처음 마주했을 때의 광경은 어떤가. `package.json`, `tsconfig.json`, `.eslintrc.js`, `vite.config.ts`, `.babelrc`… 파일만 해도 다섯 개가 넘는다. 패키지 매니저로는 npm인지 yarn인지 pnpm인지 결정해야 하고, 빌드 도구는 tsc인지 esbuild인지 swc인지 Vite인지 Turbopack인지 골라야 한다. 런타임도 Node.js인지 Bun인지 Deno인지 묻는다. 그리고 모듈 시스템이 CommonJS인지 ESM인지, 혹은 두 가지를 동시에 지원해야 하는지를 결정해야 하는데, 이게 무슨 뜻인지조차 처음엔 알 수가 없다.

*"Gradle 한 줄이면 끝나는 빌드를 왜 5개 파일에 나눠 놓느냐."*

이 분노는 정당하다. 그러나 분노한 채로 도구를 쓰면 계속 당하기만 한다. 역사적 이유를 알면 선택이 달라진다. JavaScript는 처음부터 빌드 도구 없이 시작했고, 후행 도구들이 각자 다른 시점에 다른 문제를 풀려다 지금의 풍경이 만들어졌다. 이 챕터는 그 역사적 이유를 차근차근 풀고, 지금 내 프로젝트에서 어떤 조합을 의도적으로 고를 수 있는지를 함께 생각해본다.

---

## JS에는 원래 빌드 도구가 없었다

1995년 JavaScript가 Netscape 브라우저에서 처음 실행됐을 때, 그것은 HTML 파일 안에 `<script>` 태그로 집어넣는 몇 줄짜리 코드였다. 빌드 단계 같은 건 없었다. 브라우저가 스크립트 태그를 만나면 그냥 실행했다.

모듈 시스템도 없었다. 파일을 나눠서 `import`할 방법이 표준으로 존재하지 않았다. 큰 프로젝트를 만들고 싶으면 `<script>` 태그를 여러 개 적고 순서에 의존했다. 어느 파일이 먼저 로드돼야 하는지, 전역 변수가 충돌하지 않는지를 개발자가 머릿속으로 관리했다. 이 구조에서 수만 줄짜리 프로젝트를 만드는 건 고통스러운 일이었다.

2009년 Ryan Dahl이 Node.js를 만들었다. 브라우저 밖에서 JS를 실행하는 런타임이었다. 그런데 Node.js는 서버 사이드 프로그램이었고, 서버 프로그램에는 모듈 시스템이 필요했다. 파일을 나눠서 재사용하고, 의존성을 관리해야 했다. 그래서 Node.js 팀은 **CommonJS(CJS)**라는 모듈 시스템을 만들었다. `require`로 가져오고 `module.exports`로 내보내는 방식이다.

```javascript
// math.js (CJS)
function add(a, b) {
  return a + b;
}
module.exports = { add };

// index.js (CJS)
const { add } = require('./math');
console.log(add(1, 2)); // 3
```

이것이 CJS의 탄생이다. 2009년이었고, ECMAScript 표준에 모듈 시스템이 들어오기 6년 전의 일이다.

그 사이에 브라우저 진영에서도 모듈 문제를 해결하려는 시도들이 이어졌다. AMD(Asynchronous Module Definition), UMD(Universal Module Definition) 같은 포맷들이 등장했다. 이것들은 표준이 아니었고, 각자의 방식으로 모듈을 정의했다.

2015년 ES6(ECMAScript 2015)에 드디어 **ESM(ECMAScript Modules)**이 표준으로 들어왔다. `import`와 `export`를 쓰는, 지금 우리가 아는 그 문법이다.

```javascript
// math.ts (ESM)
export function add(a, b) {
  return a + b;
}

// index.ts (ESM)
import { add } from './math.js';
console.log(add(1, 2)); // 3
```

이제 표준이 생겼으니 CJS는 사라져야 할까? 그렇지 않았다. Node.js 생태계 전체가 CJS 위에 올라가 있었다. npm에는 수십만 개의 CJS 패키지가 쌓여 있었다. 브라우저도 ESM을 완전히 지원하기까지 몇 년이 더 걸렸다. Node.js가 ESM을 공식 지원하기 시작한 건 v12(2019년)였고, 완전히 안정화된 건 v14/v16 이후의 일이다.

그 결과가 지금이다. CJS와 ESM이 공존하는 생태계. 이것이 "모듈 시스템이 둘"이라는 상황의 역사적 이유다.

---

## CJS와 ESM의 비대칭

두 모듈 시스템은 단순히 문법이 다른 게 아니다. 작동 방식이 근본적으로 다르다. 이 차이가 왜 중요한지를 이해해야 함정을 피할 수 있다.

**CJS는 동기적(synchronous)이다.** `require`를 호출하면 그 자리에서 파일을 로드하고 실행한 뒤 반환한다. 파일 시스템 I/O가 완료될 때까지 기다린다.

**ESM은 비동기적으로 로드되고 정적으로 분석된다.** `import` 문은 파일 최상위에만 올 수 있고(동적 import() 제외), 빌드 도구나 런타임이 실행 전에 의존성 그래프 전체를 파악할 수 있다. 이 정적 분석 덕분에 tree-shaking(사용하지 않는 코드 제거)이 가능하다.

이 차이가 만들어내는 비대칭이 있다.

**ESM에서 CJS 패키지를 가져오는 것은 가능하다.** Node.js가 CJS 모듈을 ESM으로 감싸서 처리한다.

```typescript
// ESM 파일에서 CJS 패키지 사용 (가능)
import lodash from 'lodash'; // lodash는 CJS
```

**CJS에서 ESM 패키지를 `require`로 가져오는 것은 불가능하다.** ESM은 비동기적이어서 동기적인 `require`로 로드할 수 없다. 동적 `import()`만 가능하다.

```javascript
// CJS 파일에서 ESM 전용 패키지 사용 (require 불가)
// const { foo } = require('pure-esm-package'); // 에러!

// 동적 import()로만 가능
async function main() {
  const { foo } = await import('pure-esm-package');
}
```

이 비대칭이 실제로 개발자를 괴롭히는 방식을 살펴보자. `node-fetch` v3는 ESM only로 전환했다. 만약 내 프로젝트가 CJS라면 `node-fetch` v3를 `require`로 가져올 수 없다. v2를 계속 써야 하거나, 프로젝트 전체를 ESM으로 전환해야 하거나, `node-fetch` 대신 `axios` 같은 CJS 친화적 대안을 써야 한다. `chalk` v5도 마찬가지였다. 많은 유틸리티 패키지들이 ESM only로 이주하면서, CJS 프로젝트 유지자들은 버전 업그레이드의 벽에 부딪혔다.

이 상황이 바로 커뮤니티가 "패턴 5 — CJS/ESM 혼란"이라 부르는 함정이다.

---

> **🚧 함정 박스 ① — CJS/ESM 혼란 (패턴 5)**
>
> **증상**: `require is not defined`, `Cannot use import statement in a module`, `ERR_REQUIRE_ESM` 같은 에러가 뒤섞여 나온다. 어떤 패키지는 import가 되는데 어떤 건 안 된다.
>
> **원인**: 프로젝트의 모듈 모드와 패키지의 모듈 모드가 일치하지 않는다. `package.json`에 `"type": "module"`이 없으면 기본값은 CJS다. 파일 확장자가 `.mjs`면 ESM, `.cjs`면 CJS로 강제된다.
>
> **처방**:
> 1. 내 프로젝트의 모듈 모드를 먼저 결정하자. 신규 프로젝트라면 ESM(`"type": "module"`)을 추천한다.
> 2. `tsconfig.json`의 `"module"` 옵션과 `"moduleResolution"` 옵션이 프로젝트 모드와 일치해야 한다. ESM 프로젝트라면 `"module": "NodeNext"`, `"moduleResolution": "NodeNext"`가 현재(2025년 기준) 안전한 조합이다.
> 3. ESM에서 상대 경로 `import`에는 `.js` 확장자를 명시해야 한다 — TS 소스가 `.ts`라도 컴파일 결과가 `.js`이므로, 임포트 경로는 `.js`로 적는 것이 ESM 표준이다.
>
> ```typescript
> // ESM 프로젝트에서 올바른 상대 경로 import
> import { add } from './math.js'; // .js 명시 (TS 파일이어도)
> ```

---

### `package.json`의 `"type"` 필드 — 한 줄이 모든 것을 바꾼다

Node.js는 `.js` 파일을 어떤 모듈 시스템으로 해석할지를 결정하는 규칙을 `package.json`의 `"type"` 필드에 둔다.

```json
{
  "name": "my-package",
  "type": "module"
}
```

`"type": "module"`이 있으면 해당 패키지 내의 `.js` 파일은 ESM으로 처리된다. 이 필드가 없거나 `"type": "commonjs"`이면 CJS가 기본값이다.

이 한 줄의 존재 여부가 같은 `.js` 파일의 실행 방식을 완전히 바꾼다. 동일한 파일이 한 프로젝트에서는 ESM으로, 다른 프로젝트에서는 CJS로 실행되는 것이다.

확장자로 모드를 명시하는 방법도 있다.

| 확장자 | 모듈 모드 |
|--------|-----------|
| `.mjs` | 항상 ESM |
| `.cjs` | 항상 CJS |
| `.js`  | `package.json`의 `"type"` 설정에 따름 |
| `.mts` | TS 소스, 컴파일 시 `.mjs` 생성 |
| `.cts` | TS 소스, 컴파일 시 `.cjs` 생성 |
| `.ts`  | `package.json`의 `"type"` 설정에 따름 |

### ESM에서 `__dirname`이 없는 이유

CJS에 익숙한 개발자가 ESM으로 전환할 때 자주 마주치는 또 다른 당혹스러움이 있다. `__dirname`이 없다.

```javascript
// CJS에서는 자동으로 제공
console.log(__dirname); // /Users/user/project/src

// ESM에서는 정의되지 않음 — ReferenceError!
console.log(__dirname); // ReferenceError: __dirname is not defined
```

왜일까? `__dirname`은 Node.js가 CJS 모듈을 로드할 때 자동으로 주입하는 변수다. ESM에는 이 주입 메커니즘이 없다. ESM은 `import.meta.url`을 통해 현재 파일의 URL을 가져오는 방식을 쓴다.

```typescript
// ESM에서 __dirname 대체
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log(__dirname); // /Users/user/project/src
```

Node.js v21.2부터는 `import.meta.dirname`을 직접 쓸 수 있어서 이 번거로움이 많이 줄었다. 하지만 LTS 버전을 쓰는 프로덕션 환경에서는 여전히 위 패턴을 쓰는 경우가 많다.

---

## Dual Package Hazard — 한 패키지가 두 형태로 배포되는 이유

라이브러리를 만든다면, CJS 사용자도 내 패키지를 쓸 수 있어야 하고 ESM 사용자도 쓸 수 있어야 한다. 그래서 많은 패키지가 두 가지 형태로 배포한다. 이것을 **듀얼 패키지(dual package)**라고 부른다.

`package.json`의 `"exports"` 필드가 이를 지원한다.

```json
{
  "name": "my-lib",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  }
}
```

이 설정이 있으면, ESM으로 `import`할 때는 `.mjs` 파일을, CJS로 `require`할 때는 `.cjs` 파일을 사용한다. TypeScript에게 타입 정보는 `.d.ts`로 제공한다.

그런데 여기서 **Dual Package Hazard**가 발생한다. CJS 버전과 ESM 버전이 각자의 내부 상태를 가지게 된다는 것이다. 예를 들어 싱글턴 패턴을 구현한 라이브러리가 있다면, CJS 버전의 싱글턴과 ESM 버전의 싱글턴이 서로 다른 인스턴스가 된다. 한 프로젝트에서 두 버전이 동시에 로드되면(직접 import + 다른 패키지를 통한 간접 import) 예상치 못한 버그가 생길 수 있다.

이 문제를 완전히 피하려면 ESM only로 배포하거나, 듀얼 패키지를 제공할 때 두 진입점이 같은 상태를 공유하도록 설계해야 한다. 실제로 많은 라이브러리가 ESM only로 전환하는 이유 중 하나가 이 hazard를 피하기 위함이다.

---

## 모듈 해석 알고리즘 — Node.js는 파일을 어떻게 찾는가

`import './math.js'`를 쓸 때, Node.js는 이 파일을 어떻게 찾을까? 그냥 해당 경로에 있는 파일을 찾는다고 생각하기 쉽지만, 실제로는 꽤 복잡한 알고리즘이 작동한다.

**CJS의 모듈 해석**은 다음 순서로 파일을 찾는다:

1. 정확한 파일이 있으면 그 파일
2. `.js`, `.json`, `.node` 확장자를 붙여서 찾기
3. 디렉터리라면 `index.js`(또는 `package.json`의 `"main"` 필드)를 찾기
4. `node_modules`로 올라가며 반복

**ESM의 모듈 해석**은 더 엄격하다. 파일 경로는 정확해야 한다. 확장자를 생략할 수 없고, 인덱스 파일 자동 탐색도 기본적으로 없다.

TypeScript는 여기에 자체적인 해석 계층을 추가한다. `tsconfig.json`의 `"moduleResolution"` 옵션이 이것을 제어한다.

| `moduleResolution` 값 | 의미 |
|----------------------|------|
| `Classic` | 초기 TS의 레거시 방식. 사용하지 말자. |
| `Node10` | CJS 방식의 Node.js 해석. 과거 기본값. |
| `Node16` / `NodeNext` | ESM과 CJS를 모두 지원하는 최신 Node.js 해석. 권장. |
| `Bundler` | Vite 같은 번들러 사용 시. 확장자 생략 허용. |

### `exports` 필드와 Conditional Exports

Node.js 12부터 `package.json`에 `"exports"` 필드를 쓸 수 있다. 이 필드는 패키지의 공개 API를 명시하고, 조건에 따라 다른 파일을 제공하는 **conditional exports**를 지원한다.

```json
{
  "name": "my-utils",
  "exports": {
    ".": {
      "node": {
        "import": "./dist/node/index.mjs",
        "require": "./dist/node/index.cjs"
      },
      "browser": "./dist/browser/index.mjs",
      "default": "./dist/index.mjs"
    },
    "./string": "./dist/string.js",
    "./number": "./dist/number.js"
  }
}
```

이 설정을 통해 Node.js 환경인지 브라우저 환경인지에 따라, ESM인지 CJS인지에 따라 다른 파일을 제공할 수 있다. TypeScript 4.7부터는 이 conditional exports를 이해하는 `"moduleResolution": "NodeNext"`가 지원됐다.

`"exports"` 필드가 있으면 내부 경로 접근이 차단된다. 예전에는 `import 'my-lib/internal/helper'`처럼 패키지 내부 파일에 직접 접근하는 관행이 있었는데, `"exports"`를 쓰면 공개하지 않은 경로는 접근 자체가 불가능해진다. 이것이 장점이기도 하고, 기존 코드가 있다면 깨질 수 있는 부분이기도 하다.

---

> **📚 Java/Kotlin 시선 박스 ① — JPMS의 실패 ↔ ESM의 늦은 정착**
>
> ```java
> // Java JPMS (Java Platform Module System) — module-info.java
> module com.example.myapp {
>     requires java.sql;
>     exports com.example.myapp.api;
> }
> ```
>
> ```json
> // JavaScript ESM — package.json exports 필드
> {
>   "exports": {
>     ".": "./dist/index.mjs",
>     "./api": "./dist/api.mjs"
>   }
> }
> ```
>
> Java 9에서 JPMS(Project Jigsaw)가 도입됐지만, 실제 현장에서 쓰이는 곳은 극히 드물다. Spring, Hibernate 같은 주요 프레임워크들이 아직 JPMS를 완전히 지원하지 않고, 기존 코드베이스를 모듈화하는 비용이 크다. Java 생태계는 결국 패키지 단위(JAR + Maven coordinate)로 의존성을 관리하고, JPMS는 JDK 내부 모듈화에만 실질적 효과를 냈다.
>
> JS는 반대 방향이었다. 패키지 시스템(npm)은 2010년부터 강건하게 작동했지만, **언어 표준 모듈 시스템**은 2015년까지 존재하지 않았다. JPMS는 이론적으로 완성됐지만 생태계가 외면했고, ESM은 늦게 왔지만 생태계가 결국 수용했다. "모듈 표준은 언어보다 먼저 태어날 수도 없고, 너무 늦게 태어나도 문제"라는 교훈을 두 언어가 서로 다른 방향에서 보여준다.

---

## npm·yarn·pnpm — 패키지 매니저의 세 갈래

패키지 매니저 이야기를 하기 전에 먼저 Maven Central과 npm의 신뢰 경계 차이를 짚고 가자.

Maven Central에 패키지를 올리려면 GPG 서명이 필요하다. 검증 과정이 있다. 패키지 소유권이 있고, 기업 도메인이면 추가 검증이 필요하다. 생태계 전체의 신뢰 수준이 비교적 높다.

npmjs.com은 다르다. 계정만 만들면 누구나 패키지를 올릴 수 있다. GPG 서명이 기본 요건이 아니다. 이 낮은 진입 장벽이 생태계의 풍요로움(100만 개 이상의 패키지)을 만들었지만, 동시에 신뢰 경계가 흐릿하다.

악의적 패키지, 타이포스쿼팅(비슷한 이름의 가짜 패키지), 기존 인기 패키지의 소유권 이전 후 악성 코드 삽입 같은 공격이 실제로 발생했다. `left-pad` 사태(2016년 — 한 개발자가 자신의 패키지를 npm에서 삭제하자 수천 개 프로젝트가 빌드에 실패한 사건)는 npm 생태계의 과도한 의존성 분산 문제를 드러냈다.

이것이 Java 개발자가 JS 생태계에 처음 왔을 때 이상하게 느끼는 지점이다. `is-odd`, `is-array` 같은 한두 줄짜리 유틸리티가 독립 패키지로 수십만 회 다운로드되는 문화. 그리고 그 패키지들의 신뢰 수준을 개발자가 직접 판단해야 한다는 부담.

---

> **📚 Java/Kotlin 시선 박스 ② — Maven Central 서명 ↔ npm 신뢰 경계**
>
> | 항목 | Maven Central | npm |
> |------|---------------|-----|
> | 퍼블리시 요건 | GPG 서명 + 검증 | 계정 생성 후 즉시 가능 |
> | 패키지 삭제 | 불가(버전 yank만 가능) | 72시간 내 삭제 가능 |
> | 소유권 이전 | 공식 프로세스 필요 | 소유자가 임의 이전 가능 |
> | 보안 감사 | Sonatype 등 third-party | npm audit (취약점 DB 기반) |
>
> 실무에서 신뢰도를 판단하는 기준으로 쓸 수 있는 지표: 주간 다운로드 수, 최근 커밋 날짜, 메인테이너 수, GitHub Stars, `package.json`의 의존성 수. 의존성이 많은 패키지는 공격 표면이 크다. `npm audit`을 CI에 포함해 알려진 취약점을 자동으로 검사하는 것이 좋다.

---

### npm — 기본값이자 역사

npm(Node Package Manager)은 2010년 Node.js와 함께 등장했다. 지금도 Node.js를 설치하면 자동으로 따라온다. 가장 큰 레지스트리이고, `package.json` 형식을 정의했다.

`node_modules` 폴더의 구조가 npm의 고유한 특성이다. 각 패키지는 자신의 의존성을 자신의 `node_modules` 안에 둔다. 중복을 줄이기 위해 호이스팅(hoisting) — 가능한 한 상위 `node_modules`로 올리기 — 을 한다.

```
project/
  node_modules/
    express/
    lodash/        ← express와 my-app 모두 사용 → 호이스팅
    express/
      node_modules/
        debug/     ← express가 쓰는 특정 버전
```

이 구조가 때로는 **유령 의존성(Phantom Dependency)** 문제를 만든다. `package.json`에 명시하지 않은 패키지를 코드에서 `require`할 수 있다. A 패키지가 B에 의존하고, B가 C를 쓴다면, 호이스팅으로 인해 C가 루트 `node_modules`에 올라올 수 있고, 내 코드에서 C를 직접 `require`해도 동작한다. 그런데 나중에 A가 C 의존성을 끊으면, 내 코드가 갑자기 깨진다.

### yarn — Facebook이 만든 대안

2016년 Facebook이 yarn을 발표했다. npm의 두 가지 문제를 해결하려 했다. 느린 설치 속도, 그리고 동일한 의존성 구조를 보장하지 못하는 문제(같은 `package.json`에서 `npm install`을 두 번 해도 다른 버전이 설치될 수 있었다).

yarn은 `yarn.lock` 파일로 정확한 버전을 고정했고, 병렬 다운로드로 속도를 높였다. 이후 npm도 `package-lock.json`을 도입했다. 이제 npm도 lockfile로 버전을 고정한다.

yarn v2("Berry")는 `node_modules` 자체를 없애는 **PnP(Plug'n'Play)** 방식을 시도했다. 각 패키지를 zip으로 묶어 캐시에 두고, 로더가 직접 찾아가는 방식이다. 설치가 빠르고 디스크 사용량이 줄지만, 기존 도구들과 호환성 문제가 생겼다. 현재 yarn v3/v4는 PnP와 전통 `node_modules` 중 선택할 수 있다.

yarn이 선호되는 환경은 여전히 존재한다. 일부 대규모 프론트엔드 프로젝트, 특히 React Native 프로젝트에서 yarn이 권장된다. Meta가 yarn을 만들었고 React Native도 Meta가 만들었으니, 생태계 정합성이 있다. 그러나 신규 프로젝트에서 yarn보다 pnpm을 선택하는 팀이 늘고 있다.

### pnpm — 디스크 효율의 왕

pnpm(2017년)은 가장 영리한 접근을 했다. 전역 저장소(content-addressable store)에 패키지를 한 번만 저장하고, 프로젝트의 `node_modules`는 **심볼릭 링크(symlink)** + **하드 링크**로 연결한다.

```
~/.pnpm-store/
  v3/
    files/
      aa/
        aabbcc...  ← 실제 파일 (내용 기반 주소)

project/
  node_modules/
    .pnpm/
      express@4.18.0/
        node_modules/
          express/ → ~/.pnpm-store/.../express/
    express/ → ./node_modules/.pnpm/express@4.18.0/node_modules/express/
```

같은 패키지를 여러 프로젝트에 설치해도 실제 파일은 저장소에 하나만 있다. 하드 링크로 참조하기 때문에 디스크 사용량이 드라마틱하게 줄어든다. 그리고 엄격한 `node_modules` 구조 덕분에 유령 의존성 문제도 없다. `package.json`에 명시한 패키지만 직접 접근할 수 있다.

카카오가 모노레포에 pnpm을 도입한 사례가 한국 커뮤니티에서 자주 인용된다. 수십 개 패키지를 가진 대규모 프로젝트에서 설치 속도와 디스크 효율이 특히 두드러진다.

### workspace — 모노레포의 기반

npm, yarn, pnpm 모두 **workspace** 기능을 지원한다. 여러 패키지를 하나의 저장소(monorepo)에서 관리할 수 있게 해준다.

```json
// package.json (루트)
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

```
my-monorepo/
  packages/
    core/
      package.json  { "name": "@my/core" }
    ui/
      package.json  { "name": "@my/ui", "dependencies": { "@my/core": "workspace:*" } }
  apps/
    web/
      package.json  { "name": "@my/web" }
```

workspace를 쓰면 `@my/core`를 npm에 올리지 않아도 `@my/ui`에서 의존성으로 참조할 수 있다. 로컬 패키지 간의 의존성을 npm 레지스트리 없이 처리한다.

`pnpm workspace:*`는 "로컬 workspace에서 현재 버전을 쓴다"는 뜻이다. 배포 시에는 실제 버전으로 교체된다.

---

## 빌드 도구의 역할 분담 — 왜 분리되어 있나

이제 빌드 도구 이야기로 들어가자. Java 개발자를 가장 혼란스럽게 만드는 지점이 여기다.

Gradle은 하나지만, TypeScript 생태계에서는 왜 tsc, esbuild, swc, Vite, Turbopack이 각자 다른 역할을 하는가? 이것은 도구 과잉이 아니다. 각자가 다른 시점에 다른 문제를 풀려다 생겨난 것이다.

역할을 먼저 명확히 나눠보자.

| 역할 | 설명 | 주요 도구 |
|------|------|-----------|
| **타입 체크** | TS 타입 오류를 검사한다 | tsc |
| **트랜스파일** | TS/최신 JS를 구버전 JS로 변환한다 | tsc, esbuild, swc, Babel |
| **번들** | 여러 파일을 하나(또는 몇 개)로 묶는다 | Vite, Webpack, esbuild, Rollup, Turbopack |
| **개발 서버** | HMR(Hot Module Replacement)로 빠른 개발 피드백 | Vite, Turbopack |
| **최소화(minify)** | 프로덕션 배포 시 코드 크기를 줄인다 | esbuild, Terser |

**tsc의 위치.** TypeScript 컴파일러(`tsc`)는 타입 체크와 트랜스파일을 동시에 할 수 있다. 하지만 문제가 있다. tsc는 TypeScript로 작성되어 있어서 Node.js 위에서 돌아가는데, 대규모 프로젝트에서는 느리다. 특히 트랜스파일(타입 지우고 JS 생성)은 실제로 타입 체크만큼 언어를 이해할 필요가 없는데도 tsc는 전체 과정을 다 수행한다.

구체적으로 말하면, tsc가 하는 일은 크게 두 가지다. 첫째, 프로그램 전체를 분석해 타입 오류를 찾는다. 둘째, 타입 주석을 제거하고 JS 코드를 생성한다. 두 번째 작업만 놓고 보면, 사실 TS 파일을 JS 파일로 바꾸는 것은 파싱과 출력의 문제고, 타입 추론의 복잡한 과정이 필요하지 않다. 그런데 tsc는 두 작업을 항상 함께 수행한다.

**Babel의 역할.** esbuild나 swc보다 먼저, **Babel**이 이 역할을 했다. Babel은 2014년에 ES6+ 문법을 구버전 JS로 변환하는 트랜스파일러로 등장했다. 나중에 TypeScript 플러그인이 추가됐다. Babel은 타입 체크를 전혀 하지 않고 타입 주석을 그냥 제거한다. 덕분에 빠르지만, 타입 오류를 잡을 수 없다. Create React App이 내부적으로 Babel을 썼고, 많은 오래된 프로젝트가 아직 Babel 기반이다.

**esbuild의 등장.** Figma의 Evan Wallace가 2020년에 Go로 만든 esbuild는 트랜스파일을 목표로 했다. 타입 체크를 하지 않는 대신 TS 파일을 매우 빠르게 JS로 변환한다. 속도 차이는 극적이다. esbuild 공식 벤치마크에 따르면 수천 모듈 규모에서 Webpack/Rollup 대비 10~100배 빠른 결과를 보인다. Go의 병렬 처리 모델과 공유 메모리 접근이 속도의 원천이다.

esbuild는 번들링도 한다. 여러 파일을 하나로 묶고, tree-shaking으로 사용하지 않는 코드를 제거한다. Vite가 개발 환경에서 esbuild를 트랜스파일러로 쓰고, 프로덕션 빌드에는 Rollup을 쓰는 이유는 Rollup의 번들 최적화(코드 스플리팅, 더 정교한 tree-shaking)가 esbuild보다 아직 섬세하기 때문이다.

**swc의 등장.** Vercel이 지원하는 Donny Wong의 swc(Speedy Web Compiler)는 Rust로 만들었다. 마찬가지로 타입 체크 없는 트랜스파일에 집중한다. Next.js v12부터 Babel 대신 swc를 기본 트랜스파일러로 채택했다. Rust의 메모리 안전성과 멀티스레딩 덕분에 빠르고, Babel 플러그인과의 호환성도 일부 유지해 기존 생태계와의 연결이 esbuild보다 부드럽다.

그렇다면 표준적인 분리 패턴은 이렇다.

```bash
# 타입 체크 (느리지만 정확)
tsc --noEmit

# 빌드 (빠르지만 타입 체크 없음)
esbuild src/index.ts --bundle --outfile=dist/index.js
```

`--noEmit` 옵션은 JS 파일을 생성하지 않고 타입 체크만 하라는 뜻이다. CI 파이프라인에서 타입 오류를 잡고, 실제 빌드는 esbuild나 swc로 빠르게 한다.

이 패턴의 실제 운용을 package.json 스크립트로 보면 이렇다.

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "build": "esbuild src/index.ts --bundle --platform=node --outfile=dist/index.js",
    "ci": "pnpm typecheck && pnpm build && pnpm test"
  }
}
```

CI에서는 `typecheck`를 먼저 돌려 타입 오류를 잡은 뒤 빌드한다. 로컬 개발 중에는 `build`만 자주 실행하고, 커밋 전에 `typecheck`를 돌리는 식으로 운용하면 개발 루프가 빠르게 유지된다.

**Vite의 포지션.** Vite는 개발 환경과 프로덕션 빌드를 모두 다루는 도구다. 개발 환경에서는 ESM을 기반으로 한 **네이티브 모듈 서버**를 운영한다. 브라우저가 ESM을 직접 가져올 수 있으므로, 변경된 모듈만 다시 전송해 HMR을 매우 빠르게 한다.

Webpack 시대의 개발 서버는 모든 파일을 번들링해서 메모리에 올린 뒤 서빙했다. 파일 하나를 수정하면 전체 번들을 다시 만들었다. 프로젝트가 커질수록 HMR이 느려지는 이유가 여기에 있다. Vite는 이 문제를 근본적으로 다르게 접근했다. 개발 환경에서는 번들링 자체를 하지 않는다. 브라우저가 `import`를 만날 때마다 개발 서버에 요청하고, Vite는 해당 파일만 즉시 반환한다. 파일 하나를 수정하면 그 파일과 그것에 의존하는 파일만 다시 변환된다.

프로덕션 빌드 시에는 내부적으로 Rollup을 사용해 최적화된 번들을 만든다. 내부 트랜스파일에는 esbuild를 쓴다. 그래서 Vite는 사실 번들러 + 개발 서버이고, 트랜스파일은 esbuild에, 프로덕션 번들 최적화는 Rollup에 위임하는 구조다.

**Rollup.** Vite 뒤에 숨어있지만 실제로 프로덕션 번들을 만드는 핵심 도구다. Rollup은 ES 모듈 기반 번들러로, 라이브러리 배포에 특히 강하다. CJS와 ESM을 동시에 출력하고, 정교한 tree-shaking과 코드 스플리팅을 제공한다.

**Turbopack.** Vercel이 만든 Rust 기반 번들러로, Next.js 15부터 기본 번들러로 통합되고 있다. Webpack과 API 호환성을 목표로 하면서 속도를 대폭 개선했다. Webpack이 자바스크립트로 작성됐고 단일 스레드로 동작한 것과 달리, Turbopack은 Rust와 병렬 처리로 대규모 Next.js 프로젝트의 HMR 속도를 크게 높였다. 2025년 기준으로는 Next.js 생태계에서 주로 쓰이고, 독립적인 범용 번들러로서의 채택은 진행 중이다.

**Webpack — 레거시이자 기반.** Webpack을 언급하지 않고 번들러 이야기를 끝내는 건 공정하지 않다. 2012년에 등장한 Webpack은 오랫동안 번들링의 사실상 표준이었다. Create React App, Angular CLI, Vue CLI 모두 Webpack을 썼다. 지금도 대규모 기업 프로젝트에서 Webpack 기반 설정을 유지하는 곳이 많다. Webpack의 설정 복잡도는 악명 높지만, 그만큼 정교한 제어가 가능하다는 뜻이기도 하다. 새로 시작하는 프로젝트라면 Vite나 Turbopack을 선택하는 편이 낫지만, 기존 Webpack 프로젝트를 무조건 마이그레이션할 필요는 없다.

---

> **📚 Java/Kotlin 시선 박스 ③ — Gradle 한 도구 ↔ npm + tsc + esbuild + Vite 분산**
>
> ```groovy
> // build.gradle — 하나의 파일에서 전부
> plugins {
>   id 'java'
>   id 'org.springframework.boot' version '3.2.0'
> }
>
> dependencies {
>   implementation 'org.springframework.boot:spring-boot-starter-web'
>   testImplementation 'org.springframework.boot:spring-boot-starter-test'
> }
> ```
>
> ```bash
> # TypeScript 프로젝트의 흔한 조합
> # 패키지 매니저: pnpm
> # 타입체크: tsc --noEmit
> # 번들러/개발서버: Vite (내부적으로 esbuild 사용)
> # 테스트: Vitest (Vite 기반)
>
> pnpm install
> pnpm exec tsc --noEmit        # 타입 체크
> pnpm exec vite build          # 프로덕션 빌드
> pnpm exec vitest              # 테스트
> ```
>
> Gradle이 하나의 도구로 전부 하는 건, Gradle 자체가 의존성 관리·컴파일·테스트·패키징의 표준 단계를 정의했기 때문이다. JS 생태계에는 이런 표준 단계 정의가 없었다. 각 문제가 생길 때마다 커뮤니티가 도구를 만들었다. Gradle 플러그인 생태계가 Gradle 위에서 작동하듯, JS 빌드 도구들도 점점 서로 위에 쌓이는 구조가 되고 있다. Vite가 esbuild 위에 있고, Vitest가 Vite 위에 있는 것처럼.

---

## tsconfig — 왜 옵션이 이렇게 많은가

`tsconfig.json`을 처음 열면 한숨이 나온다. 옵션이 수십 개다. `strict`, `target`, `lib`, `module`, `moduleResolution`, `outDir`, `rootDir`, `baseUrl`, `paths`, `declaration`, `sourceMap`, `noEmit`, `skipLibCheck`… 이것들이 다 무슨 뜻이고, 어떻게 조합해야 하는가.

일단 왜 이렇게 많은지 이해하자. TypeScript는 다양한 환경에서 쓰인다. Node.js 백엔드, 브라우저 프론트엔드, 모노레포의 라이브러리, Deno, Bun… 각 환경마다 다른 표준 라이브러리가 있고, 다른 모듈 시스템을 써야 하고, 다른 타깃 JS 버전이 필요하다. 이 다양성을 하나의 설정 파일에서 제어하다 보니 옵션이 많아졌다.

이 챕터에서 100개 옵션을 나열하는 것은 부록 B의 역할이다. 여기서는 **카테고리를 이해**하고, **왜 이런 옵션이 생겼는가**를 알아보자. 카테고리를 알면 처음 보는 옵션도 어느 그룹인지 짐작할 수 있다.

### 카테고리 1 — 타입 엄격도 계열 (`strict` 가족)

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict: true`는 하나의 옵션이 아니라 여러 옵션의 묶음이다.

| 옵션 | 기본값 | 의미 |
|------|--------|------|
| `strictNullChecks` | false | `null`/`undefined`를 별도 타입으로 취급 |
| `noImplicitAny` | false | 타입 추론 불가 시 `any` 대신 오류 |
| `strictFunctionTypes` | false | 함수 매개변수 공변성/반변성 엄격 적용 |
| `strictPropertyInitialization` | false | 클래스 프로퍼티 초기화 강제 |
| `noImplicitThis` | false | `this`가 `any`면 오류 |
| `useUnknownInCatchVariables` | false | catch 변수를 `unknown`으로 처리 |

Java/Kotlin 개발자는 이 옵션들을 켜는 게 자연스럽다. 정적 타입 언어에서 null 안전성과 명시적 타입은 당연한 것이기 때문이다. `strict: true`로 시작하는 것을 권장한다.

왜 기본값이 false냐고? 기존 JS 코드베이스를 점진적으로 TS로 전환하는 경우, 처음부터 strict를 켜면 수천 개의 오류가 터진다. 점진적 도입을 위해 기본은 느슨하게, 필요한 옵션을 하나씩 켜는 설계다.

### 카테고리 2 — 출력 타깃 계열 (`target`, `lib`)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM"]
  }
}
```

`target`은 컴파일 결과 JS의 ECMAScript 버전을 결정한다. `"ES2022"`로 지정하면 화살표 함수, `async/await`, optional chaining 등 ES2022까지의 문법을 그대로 출력한다. 구버전 브라우저를 지원해야 한다면 `"ES5"`로 낮출 수 있다. 낮출수록 코드가 길어지고(폴리필·변환 증가), 높을수록 현대적인 코드가 나온다.

`lib`은 타입 체크 시 사용 가능한 전역 타입을 지정한다. `"DOM"`이 있으면 `document.querySelector()` 같은 브라우저 API의 타입을 알 수 있다. `"DOM"`이 없으면 `document`가 존재하지 않는 타입이 된다. Node.js 백엔드라면 `"DOM"`을 뺀다.

### 카테고리 3 — 모듈 계열 (`module`, `moduleResolution`)

앞서 모듈 해석 알고리즘에서 설명했다. `module`은 출력 코드의 모듈 형식(CJS, ESM 등), `moduleResolution`은 import 경로를 어떻게 해석할지를 결정한다.

신규 Node.js 프로젝트(ESM)라면 이 조합을 추천한다:

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  }
}
```

Vite 기반 프론트엔드라면:

```json
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Bundler"
  }
}
```

### 카테고리 4 — 출력 경로 계열 (`outDir`, `rootDir`, `declaration`)

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

`outDir`은 컴파일 결과 파일의 위치, `rootDir`은 소스 파일의 루트. `declaration: true`는 `.d.ts` 타입 선언 파일을 생성한다. 라이브러리를 만들어 배포할 때 필수다. `sourceMap: true`는 디버깅 시 컴파일된 JS에서 원본 TS 소스를 찾을 수 있게 한다.

### 카테고리 5 — 호환성·편의 계열

`skipLibCheck: true`는 `node_modules`의 `.d.ts` 파일을 타입 체크하지 않는다. 서드파티 라이브러리의 타입 정의 파일에 오류가 있어도 무시하는 것이다. 엄밀히는 좋지 않은 옵션이지만, 실무에서는 거의 필수적으로 켜게 된다. 어떤 패키지의 `.d.ts`가 다른 패키지의 타입과 충돌하는 경우가 많기 때문이다.

왜 이런 충돌이 생기는가? 두 패키지가 서로 다른 버전의 TypeScript에서 생성된 `.d.ts`를 가지고 있거나, `@types/node`의 버전이 맞지 않거나, 라이브러리가 자체 타입 정의에 실수를 한 경우다. `skipLibCheck: true`는 이 문제들을 모두 우회한다. 이상적이지 않지만 현실적인 선택이다.

`esModuleInterop: true`는 CJS 모듈을 ESM 방식으로 편하게 import할 수 있게 한다.

```typescript
// esModuleInterop 없이
import * as React from 'react'; // CJS 모듈

// esModuleInterop 있으면
import React from 'react'; // 더 자연스러운 default import
```

`isolatedModules: true`는 각 파일을 독립적으로 트랜스파일할 수 있어야 한다는 제약이다. esbuild, swc, Babel은 파일을 하나씩 처리하는 방식이라, TypeScript의 프로젝트 전체 분석이 필요한 기능(const enum, namespace 등)을 지원하지 못한다. `isolatedModules: true`로 설정하면 이런 기능을 쓸 때 tsc가 미리 경고한다. esbuild나 swc로 빌드하는 프로젝트에서는 이 옵션을 켜는 편이 낫다.

`verbatimModuleSyntax: true`는 TypeScript 5.0에서 추가된 옵션이다. import 문을 트랜스파일 시 어떻게 처리할지를 명확히 한다. 타입만 가져오는 import는 `import type`으로 명시하지 않으면 오류가 난다. 이 옵션은 `isolatedModules`와 `importsNotUsedAsValues`를 통합한 것으로, 번들러 기반 프로젝트에서 더 정확한 트리-쉐이킹을 돕는다.

```typescript
// verbatimModuleSyntax: true 환경에서는 타입 전용 import를 명시해야 한다
import type { User } from './types'; // OK
import { User } from './types';      // 오류 — User가 타입만이라면
```

### Matt Pocock의 tsconfig cheat sheet

TypeScript 커뮤니티에서 Matt Pocock의 tsconfig cheat sheet는 "무엇을 켜야 하는가"에 대한 실용적인 출발점으로 인정받는다. 그의 권장 기반 설정은 이렇다(신규 Node.js 라이브러리 기준):

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

이 설정이 "왜 이 값인지"에 대한 이유는 각 카테고리 설명에서 이미 풀었다. 옵션을 외울 필요는 없다. 카테고리를 이해하면 낯선 옵션이 나왔을 때 부록 B에서 찾아볼 수 있다.

---

> **🚧 함정 박스 ② — tsconfig 지옥 (패턴 6)**
>
> **증상**: 에디터에서는 오류가 없는데 빌드하면 오류가 난다. 빌드는 되는데 런타임에 `Cannot find module`이 나온다. `paths` 별칭을 설정했는데 빌드 결과물에서 경로가 변환되지 않는다.
>
> **원인 ①** — tsconfig가 여러 개인 경우(에디터용, 빌드용, 테스트용이 각각 다른 설정을 가짐). 에디터는 `tsconfig.json`을 보지만, tsc는 다른 파일을 본다.
>
> **원인 ②** — `paths` 별칭은 tsc가 타입 해석 시 쓰는 것이지, 빌드 결과물에 반영되지 않는다. `@/utils` 같은 별칭을 빌드 결과물에서도 쓰려면 번들러(Vite, esbuild)에도 별도로 설정해야 한다.
>
> **원인 ③** — `module`과 `moduleResolution`이 런타임 환경과 맞지 않는다.
>
> **처방**:
> - `tsc --showConfig`로 실제로 어떤 설정이 적용되는지 확인한다.
> - tsconfig를 상속(`extends`)으로 관리한다. 기본 설정을 `tsconfig.base.json`에 두고, 에디터용·빌드용·테스트용이 각자 `extends`로 가져온다.
> - `paths` 별칭은 번들러 설정에도 반드시 함께 등록한다.
>
> ```json
> // tsconfig.json (에디터용 = 루트)
> {
>   "extends": "./tsconfig.base.json",
>   "include": ["src", "test"]
> }
>
> // tsconfig.build.json (빌드용)
> {
>   "extends": "./tsconfig.base.json",
>   "exclude": ["test"],
>   "compilerOptions": {
>     "noEmit": false,
>     "outDir": "./dist"
>   }
> }
> ```

---

## 런타임 세 갈래 — Node, Bun, Deno

빌드 도구 이야기와 함께 런타임 선택도 빠지지 않는다. 2025년 기준으로 세 가지 JS/TS 런타임이 공존한다. 미래의 산업적 의미는 15장에서 다루고, 여기서는 지금 어떻게 쓰이는지만 살펴보자.

### Node.js — 사실상의 표준

2009년 Ryan Dahl이 만든 Node.js는 오늘날도 서버 사이드 JS의 기본값이다. LTS(Long Term Support) 버전이 있고, 기업들이 의존한다. 생태계가 가장 크다. npm의 100만 개 이상 패키지 대부분이 Node.js에서 동작한다.

Node.js의 가장 큰 특징은 **이벤트 루프 기반의 단일 스레드 비동기 모델**이다. Java의 멀티스레드 모델과 달리, Node.js는 기본적으로 하나의 스레드에서 이벤트 루프가 돌아간다. I/O 작업(네트워크, 파일)은 비동기로 처리하고, 콜백이나 Promise로 결과를 받는다. CPU 집약적 작업에는 Worker Threads를 쓰거나 별도 프로세스로 분리한다.

TS 지원은 직접적이지 않다. TS 파일을 실행하려면 `ts-node`나 `tsx` 같은 도구를 써서 먼저 JS로 변환해야 한다. Node.js v22부터 `--experimental-strip-types` 플래그로 TS를 직접 실행할 수 있게 됐지만, 아직 실험적 기능이다.

```bash
# ts-node로 실행 (느림, 완전한 타입 체크 후 실행)
npx ts-node src/index.ts

# tsx로 실행 (esbuild 기반, 훨씬 빠름 — 타입 체크 없이 트랜스파일만)
npx tsx src/index.ts

# Node.js v22+ 실험적 (타입 주석 제거만, 타입 체크 없음)
node --experimental-strip-types src/index.ts
```

개발 환경에서 파일 변경을 감지해 자동 재시작하려면 이렇게 쓴다.

```bash
# tsx watch 모드 — 파일 저장 시 자동 재실행
tsx watch src/index.ts

# Node.js 내장 watch 모드 (v18+, tsx 필요)
node --watch --experimental-strip-types src/index.ts
```

LTS 정책은 Java의 LTS와 비슷하다. 짝수 버전(18, 20, 22)이 LTS가 되고, 3년간 지원을 받는다. 홀수 버전(19, 21, 23)은 Current 버전으로 새 기능을 포함하지만 6개월만 지원된다. 프로덕션 서버에서는 LTS 버전을 쓰는 편이 안전하다. Node.js 18의 EOL(End of Life)이 2025년 4월이었고, 20이 현재 Active LTS, 22가 2025년 10월부터 Active LTS가 된다.

Node.js에서 TypeScript를 쓰는 실제 운영 방식은 대체로 이렇다. 개발 중에는 `tsx watch`로 빠른 반복을 하고, 빌드 시에는 `tsc --noEmit`으로 타입을 검사한 뒤 esbuild나 tsc로 JS를 생성한다. Docker 이미지에는 컴파일된 JS만 올려서 Node.js로 실행한다. TypeScript는 빌드 도구일 뿐, 런타임에는 존재하지 않는다.

### Bun — 통합과 속도

2023년 Jarred Sumner가 만든 Bun은 "빠름"을 가장 강조한다. Zig로 작성됐고, JS 엔진으로 JavaScriptCore(Safari의 JS 엔진)를 쓴다.

Bun의 두드러진 특징은 TS를 직접 실행할 수 있다는 것이다.

```bash
# Bun은 TS 파일을 바로 실행
bun run src/index.ts
```

트랜스파일을 내부에서 처리하기 때문에 별도 도구가 필요 없다. 패키지 설치도 Bun 자체가 처리한다. `bun install`이 npm install보다 훨씬 빠르다.

```bash
# Bun으로 패키지 설치 (npm보다 수 배 빠름)
bun install

# Bun으로 빌드 (esbuild 내장)
bun build ./src/index.ts --outfile ./dist/index.js

# 단일 실행 파일 생성
bun build --compile ./src/index.ts --outfile my-app
```

`bun build --compile`은 TS 소스를 플랫폼별 단일 실행 파일로 만든다. Java의 GraalVM native-image와 비슷한 위치다.

현장 실무에서 Bun은 어디서 쓰이는가? **로컬 개발과 CLI 도구**에서 채택이 빠르다. 설치와 실행이 빠르고, TS 파일을 바로 실행할 수 있어서 개발 루프가 짧아진다. 프로덕션 서버에서는 아직 신중한 시각이 많다. Bun의 long-running 프로세스에서 edge case나 메모리 leak이 보고된 사례들이 있었고(커뮤니티 휴리스틱 9), 기업의 LTS 의존 문화가 빠른 전환을 막는다.

### Deno — 보안과 표준

2018년 Ryan Dahl이 Node.js를 돌아보며 "다시 만든다면"을 현실로 만든 게 Deno다. 아이러니하게도 Node.js의 창시자가 Node.js의 설계 실수를 반성하며 만든 런타임이다.

Deno의 특징들:
- **보안 기본(secure by default)**: 파일 시스템, 네트워크, 환경 변수 접근을 기본으로 차단하고, 실행 시 명시적으로 허용해야 한다. Node.js는 프로세스 권한 내에서 뭐든 할 수 있다.
- **TS 일급 지원**: 설치 없이 TS 파일을 직접 실행한다.
- **표준 라이브러리**: Deno가 관리하는 표준 라이브러리가 있다. Node.js는 표준 라이브러리가 최소화되어 있어 서드파티 패키지에 의존하는 것과 대조된다.
- **URL import**: 초기에는 npm 대신 URL로 직접 모듈을 import했다. Deno 2부터는 npm 호환성이 크게 강화됐다.

```typescript
// Deno — TS 직접 실행
deno run src/index.ts

// 네트워크 접근 허용
deno run --allow-net src/server.ts

// npm 패키지 사용 (Deno 2)
import express from 'npm:express';
```

Deno는 어디서 쓰이는가? **보안이 중요한 환경**과 **표준 준수가 가치 있는 곳**에서 선택된다. Cloudflare Workers, Deno Deploy 같은 엣지 런타임과 잘 어울린다. Hono 프레임워크가 Deno를 첫 번째 지원 런타임 중 하나로 두고 있다.

한국 커뮤니티에서 Deno는 "재미있지만 프로덕션은 아직"이라는 신중한 시각이 우세하다(커뮤니티 한국 시각 5). 일본 커뮤니티(Hono 저자 Yusuke Wada가 일본인이다)의 적극성과 대비되는 보수적 정서다.

### 2025년 기준 현장 합의

로컬 개발과 CLI 도구에서는 Bun이 빠른 속도로 채택되고 있다. 프로덕션 서버는 Node.js LTS가 여전히 기본값이다. 보안과 표준이 중요한 엣지 환경에서는 Deno의 자리가 있다.

어떤 런타임을 골라야 하는지는 프로젝트 성격에 따라 다르다. 중요한 건 선택의 이유를 갖는 것이다. "그냥 다 Node.js"도, "최신 트렌드를 쫓아 Bun"도 좋은 이유가 될 수 없다.

---

## Monorepo와 TypeScript의 함정

프로젝트가 커지면 하나의 저장소에 여러 패키지를 넣는 **monorepo** 구성을 고려하게 된다. 카카오의 "TypeScript Monorepo with pnpm" 글, 당근의 "한 모노레포에서 1000명이 일하는 법" 글이 한국 커뮤니티에서 표준 학습 자료로 인용된다.

monorepo의 구조 예시를 보자.

```
my-monorepo/
  packages/
    core/           ← 비즈니스 로직
    ui/             ← UI 컴포넌트
    utils/          ← 공통 유틸리티
  apps/
    web/            ← Next.js 웹 앱
    admin/          ← 관리자 페이지
    api/            ← NestJS API 서버
  package.json      ← workspace 설정
  pnpm-workspace.yaml
```

이 구조에서 TypeScript에 특유한 함정이 있다.

### IDE 폭주 — tsconfig.references 없이 쓰면 안 된다

monorepo에서 TypeScript 서버(에디터가 타입 정보를 제공하는 백그라운드 프로세스)는 각 패키지의 소스를 모두 읽으려 한다. `apps/web`이 `packages/ui`를 사용한다면, TypeScript 서버는 `packages/ui`의 모든 TS 파일도 읽고 분석한다. 패키지가 많아질수록 메모리 사용량과 CPU 사용률이 폭발한다. VSCode나 IntelliJ가 느려지거나 멈추는 것이다. 이것이 "패턴 12 — monorepo IDE 폭주"다.

해결책은 **Project References**다. TypeScript의 `tsconfig.references` 기능을 써서 각 패키지가 독립적으로 컴파일되고, 의존하는 패키지는 이미 컴파일된 결과(`.d.ts`)를 참조하도록 한다.

```json
// apps/web/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist"
  },
  "references": [
    { "path": "../../packages/ui" },
    { "path": "../../packages/utils" }
  ]
}
```

```json
// packages/ui/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "composite": true,    ← project references 사용 시 필수
    "declaration": true
  }
}
```

`composite: true`는 이 패키지가 다른 패키지에서 참조될 수 있음을 선언한다. `tsc --build`(또는 `tsc -b`) 명령을 쓰면 변경된 패키지만 다시 빌드한다.

이렇게 설정하면 TypeScript 서버는 `packages/ui`를 소스 전체가 아니라 컴파일된 `.d.ts`로 참조한다. IDE 성능이 극적으로 개선된다.

### Turborepo와 캐싱

패키지가 많은 monorepo에서 `tsc -b`만으로는 부족하다. 의존성 그래프를 따라 빌드 순서를 결정하고, 변경된 것만 다시 빌드하고, 병렬로 실행 가능한 것은 동시에 실행하는 오케스트레이션 레이어가 필요하다. Vercel이 만든 **Turborepo**가 이 역할을 한다.

```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

`"dependsOn": ["^build"]`는 이 패키지의 `build` 태스크 전에, 의존하는 모든 패키지의 `build`가 먼저 완료되어야 한다는 뜻이다. `^`는 "내가 의존하는 것들(upstream)"을 뜻하는 Turborepo의 컨벤션이다. `"dependsOn": ["build"]`처럼 `^` 없이 쓰면 "같은 패키지의 build 태스크 먼저"라는 뜻이 된다.

Turborepo의 핵심 기능은 **캐싱**이다. 같은 입력(소스 파일, 환경 변수, 설정)에서는 같은 출력이 나온다는 원칙으로, 이전에 실행한 결과를 캐시에 저장한다. 다음 실행 때 입력이 동일하면 실행하지 않고 캐시를 복원한다.

```bash
# 처음 실행 — 모든 패키지 빌드
turbo run build
# >>> packages/utils: cache miss, executing
# >>> packages/core: cache miss, executing
# >>> apps/web: cache miss, executing

# 변경 없이 다시 실행 — 캐시 히트
turbo run build
# >>> packages/utils: cache hit, replaying output
# >>> packages/core: cache hit, replaying output
# >>> apps/web: cache hit, replaying output
```

로컬 캐시뿐 아니라 **리모트 캐시**도 지원한다. Vercel 계정으로 무료로 쓸 수 있고, self-hosted 옵션(ducktape, turborepo-remote-cache)도 있다. 리모트 캐시를 활성화하면 팀원 A의 빌드 결과를 팀원 B가, CI 서버가 공유해 쓸 수 있다. "처음 CI에서 빌드됐으면 내 로컬에서는 캐시"가 가능해진다.

**Nx.** Turborepo의 경쟁자이자 더 오래된 대안이다. Turborepo보다 기능이 많다 — 코드 generator, workspace graph 시각화, affected 분석(변경된 파일에 의존하는 패키지만 빌드). 학습 곡선이 가파르지만 대규모 모노레포에서 강력하다. Nrwl이 만들었고, Angular 생태계에서 특히 많이 쓰인다.

도구 선택 기준으로는 이렇게 생각해볼 수 있다. 심플한 설정을 원하고 빌드 캐싱이 주목적이라면 Turborepo, 풍부한 기능과 codegen이 필요하다면 Nx. 두 도구를 혼합해 쓰는 것도 가능하다.

---

> **🚧 함정 박스 ③ — Monorepo IDE 폭주 (패턴 12)**
>
> **증상**: monorepo 설정 후 VSCode가 느려지고, TypeScript 서버가 수 GB의 메모리를 먹는다. "TypeScript server is initializing..." 상태가 오래 지속된다.
>
> **원인**: 각 패키지의 `tsconfig.json`에 `references`를 설정하지 않았다. TypeScript 서버가 전체 소스를 단일 프로젝트로 분석한다.
>
> **처방**:
> 1. 루트에 `tsconfig.json`을 두되, `files: []`로 소스를 포함하지 않고 각 패키지 참조만 나열한다.
>
> ```json
> // 루트 tsconfig.json — IDE가 전체 프로젝트를 파악하지만 각 패키지는 독립적으로 컴파일
> {
>   "files": [],
>   "references": [
>     { "path": "packages/core" },
>     { "path": "packages/ui" },
>     { "path": "apps/web" }
>   ]
> }
> ```
>
> 2. 각 패키지의 `tsconfig.json`에 `"composite": true`와 `"references"` 를 설정한다.
>
> 3. `tsc --build --watch`로 변경된 패키지만 증분 컴파일한다.
>
> **추가 팁**: VSCode의 경우 워크스페이스에 `*.code-workspace` 파일을 추가하고, 각 패키지 폴더를 별도 루트로 등록하면 TypeScript 서버가 각 패키지 기준으로 동작한다.

---

## 각 도구를 의도적으로 고르기

이 모든 것을 정리하면, 프로젝트의 성격에 따라 도구 조합을 의도적으로 선택할 수 있다.

### 시나리오 1 — 작은 Node.js 백엔드 (혼자 또는 소팀)

```json
// package.json
{
  "name": "my-api",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc --noEmit && node --loader ts-node/esm src/index.ts",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "tsx": "^4.0.0",
    "@types/node": "^20.0.0"
  }
}
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src"]
}
```

소팀 Node.js 백엔드에서는 이 조합이 무난하다. `tsx`로 개발 중 빠른 TS 실행, `tsc --noEmit`으로 타입 체크, 프로덕션은 esbuild나 tsc로 빌드.

### 시나리오 2 — Vite 기반 프론트엔드

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "Bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  },
  "include": ["src"]
}
```

Vite 기반 React 프로젝트라면 `vite create`가 이와 유사한 tsconfig를 생성한다. `"moduleResolution": "Bundler"`가 Vite가 처리하는 방식과 정렬된다. `"noEmit": true`는 tsc가 JS를 생성하지 않고 타입 체크만 한다는 뜻이다. 빌드는 Vite가 한다.

### 시나리오 3 — 공개 라이브러리

```json
// package.json
{
  "name": "@myorg/utils",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.mts",
        "default": "./dist/index.mjs"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "typecheck": "tsc --noEmit"
  }
}
```

라이브러리라면 CJS와 ESM 양쪽을 지원하는 편이 좋다. `tsup`(esbuild 기반의 라이브러리 빌드 도구)이 이 작업을 편하게 해준다. `--dts` 옵션으로 `.d.ts` 파일도 함께 생성한다.

### 시나리오 4 — pnpm workspace monorepo

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

```json
// 루트 package.json
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "typecheck": "turbo run typecheck"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.0.0"
  }
}
```

```json
// 루트 tsconfig.json (에디터용)
{
  "files": [],
  "references": [
    { "path": "packages/core" },
    { "path": "packages/ui" },
    { "path": "apps/web" }
  ]
}
```

```json
// tsconfig.base.json (공유 기본 설정)
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

이 구조가 카카오, 당근 같은 대규모 팀에서 쓰이는 패턴의 골격이다.

---

## 전체 그림을 한눈에

지금까지 살펴본 도구들의 관계를 정리하면 이렇다.

```
소스 코드 (.ts)
    ↓
[타입 체크]
  tsc --noEmit         → 오류 목록
    ↓ (오류 없음)
[트랜스파일 / 번들]
  CLI/라이브러리:  tsc, esbuild, swc, tsup
  프론트엔드:     Vite (내부: esbuild + Rollup)
  Next.js:        Turbopack (또는 Webpack)
    ↓
출력 (.js, .d.ts, .js.map)
    ↓
[런타임]
  서버:     Node.js LTS
  빠른 개발: Bun
  엣지/보안: Deno
```

이 흐름이 머릿속에 있으면 낯선 설정 파일이 나왔을 때 "이건 어느 단계의 설정인가"를 먼저 물을 수 있다. tsconfig는 타입 체크와 tsc 트랜스파일 단계, vite.config.ts는 번들링 단계, package.json은 패키지 관리와 모듈 모드, 그리고 각 실행 명령어는 어느 도구를 어느 단계에서 쓰는가를 정의한다.

---

## 한국 팀의 현장 — 어떤 조합이 많이 쓰이나

구체적인 한국 기업 사례를 보자.

**카카오**는 pnpm workspaces 기반 monorepo를 운영한다. Turborepo를 빌드 파이프라인에 사용하고, 패키지별 `tsconfig.json`에 project references를 설정한 사례를 기술 블로그에서 공유했다. 초기에는 IDE 성능이 심각하게 느렸고, project references 도입 후 TypeScript 서버가 소모하는 메모리가 크게 줄었다는 경험이 담겼다.

**당근**은 monorepo와 디자인 시스템 TS화 과정에서 공통 컴포넌트 패키지를 분리하고, 각 앱에서 참조하는 구조를 가져갔다. IDE 성능 문제를 project references로 해결한 경험도 공유됐다. 1,000명 규모의 팀이 한 monorepo에서 일하면서 빌드 파이프라인과 패키지 경계를 어떻게 설계했는지의 노하우가 한국 커뮤니티에서 자주 인용된다.

**토스**의 경우 JavaScript에서 TypeScript로 마이그레이션한 후기 시리즈가 공개돼 있다. 마이그레이션 자체는 9장에서 다루지만, 빌드 도구 관점에서 보면 점진적 마이그레이션 중에 CJS와 ESM이 뒤섞이는 상황, tsconfig strict 설정을 단계적으로 켜나가는 과정이 담겨 있다.

이 사례들이 공통으로 시사하는 것은, 규모가 커질수록 도구를 추가하는 게 아니라 **도구 간의 경계를 명확히** 하는 것이 중요하다는 점이다. tsc는 타입 체크, Turborepo는 태스크 오케스트레이션, pnpm은 패키지 관리와 workspace — 각자의 역할을 명확히 하고 중복을 줄이는 것이 monorepo 관리의 핵심이다.

### 중소 규모 팀을 위한 현실적인 시작점

대기업의 monorepo 사례가 항상 정답은 아니다. 5명짜리 팀이 처음부터 Turborepo + pnpm workspace + project references 전부를 설정하면 설정 자체가 프로젝트보다 커질 수 있다. 규모에 맞는 현실적인 진입을 생각해보자.

**작은 팀(1~10명), 단일 앱**: 단일 `package.json`, `tsconfig.json` 하나, pnpm(또는 npm). 빌드는 tsc 또는 Vite. 이것으로 충분하다.

**중간 팀(10~50명), 공유 라이브러리 필요**: pnpm workspace 도입. 공통 코드를 `packages/`로 분리. tsconfig.references 설정. Turborepo는 아직 선택사항.

**큰 팀(50명+), 여러 앱과 패키지**: Turborepo + pnpm workspace + project references. CI 리모트 캐시로 빌드 시간 관리.

단계를 건너뛰지 않는 편이 낫다. 중간 단계 없이 작은 팀이 큰 팀의 도구 스택을 가져오면 유지보수 부담이 팀 규모를 초과한다. 그게 더 난감한 상황이다.

---

## 분노에서 이해로

처음의 분노로 돌아가보자. "Gradle 한 줄이면 끝나는 빌드를 왜 5개 파일에 나눠 놓느냐."

이제 이 분노의 역사적 이유를 안다.

JavaScript는 처음부터 빌드 도구 없이 태어났다. 모듈 시스템도 없었다. 2009년에 서버 사이드로 가면서 CJS가 생겼고, 2015년에서야 ESM이 표준이 됐다. 그 사이에 수십만 개의 패키지가 CJS로 쌓였다. 타입 체크는 TypeScript가 2012년에 가져왔고, 트랜스파일 속도 문제는 2020년에 esbuild가 풀었다. 번들링 문제는 Webpack이 수년 먼저 풀었고, 개발 서버 속도 문제는 Vite가 2021년에 달리 풀었다.

각 도구는 각자의 시간에 각자의 문제를 풀었다. Gradle처럼 처음부터 통합 도구가 있었다면 하나로 해결됐겠지만, JS 생태계는 그런 출발점이 없었다. 분산된 것은 무질서가 아니라, 분산된 시점과 분산된 목적의 결과다.

그렇다면 지금 이 분산이 수렴하는 방향은 어디인가? 흥미롭게도, 도구들이 조금씩 통합의 방향으로 움직이고 있다.

Bun은 패키지 매니저 + 번들러 + 런타임 + 테스트 러너를 하나로 묶으려 한다. Deno 2는 npm 호환성을 추가하면서 표준 라이브러리 + 런타임 + 타입 체크를 하나에 담으려 한다. Microsoft는 TypeScript 컴파일러 자체를 Go로 재작성하는 "TypeScript Native" 프로젝트로 tsc의 속도 문제를 근본적으로 해결하려 한다. Node.js는 `--experimental-strip-types`로 TS를 직접 실행하는 방향으로 움직인다.

이 수렴이 완전히 이뤄지면 언젠가 JS 생태계의 빌드 도구 풍경이 단순해질 수도 있다. 하지만 그게 언제가 될지는 아무도 모른다. 생태계가 느리게 바뀌는 이유는, 수십만 개의 기존 패키지와 수백만 개의 기존 프로젝트가 현재의 도구들 위에서 돌아가고 있기 때문이다.

찜찜하지 않다고는 못하겠다. "왜 진작에 표준이 안 됐냐"는 아쉬움은 당연하다. 하지만 지금은 도구의 역할 분담이 비교적 명확해졌고, 어떤 조합을 선택할지 의도를 가지고 결정할 수 있다. 역사를 알면 도구가 겹쳐 보이지 않는다. 그리고 의도적인 선택은 나중에 설정 파일이 왜 이렇게 생겼는지 팀원에게 설명할 수 있는 근거가 된다.

### 실무에서 자주 틀리는 선택들

이해를 마무리하기 전에, 이 챕터의 내용을 돌아보며 현장에서 자주 잘못 선택하는 패턴들을 짚어두자.

**"tsc가 느리니 esbuild만 쓰면 된다"** — 틀렸다. esbuild는 타입 체크를 하지 않는다. 타입 오류가 있어도 빌드가 된다. tsc --noEmit은 반드시 CI에 있어야 한다. 빌드 속도와 타입 안전성은 별개의 문제다.

**"monorepo가 좋다니까 바로 도입하자"** — 팀 규모와 코드 공유 필요성을 먼저 따져봐야 한다. 3명 팀에서 모든 앱이 독립적으로 배포된다면 monorepo의 이점보다 설정 부담이 더 크다.

**"ESM으로 전환하면 다 해결된다"** — ESM으로 전환하면 CJS 전용 패키지와의 호환 문제가 생길 수 있다. 의존성을 먼저 파악하고, ESM 지원 여부를 확인해야 한다.

**"tsconfig 기본값을 그대로 쓴다"** — 기본값은 하위 호환성을 위해 느슨하게 설정돼 있다. `strict: true`, `moduleResolution: NodeNext`, `skipLibCheck: true` 정도는 프로젝트 시작 시 명시적으로 설정하는 편이 낫다.

**"런타임은 어차피 Node.js니까 신경 안 써도 된다"** — 맞는 말이다. 하지만 로컬 개발에서 Bun이나 tsx를 쓰면 피드백 루프가 빨라진다. 런타임을 의식하지 않아도 되는 시대가 되더라도, 어떤 런타임이 어디에 있는지 아는 것은 트러블슈팅에서 중요하다.

---

## 마무리

이 챕터에서 살펴본 것들을 기억해두자.

CJS와 ESM은 역사적 이유로 공존한다. 신규 프로젝트는 ESM을 선택하는 편이 낫다. `package.json`의 `"type": "module"` 한 줄, tsconfig의 `"module": "NodeNext"` 설정이 출발점이다.

패키지 매니저 중 pnpm은 디스크 효율과 엄격한 의존성 관리 면에서 monorepo에 특히 적합하다. workspace 기능은 세 패키지 매니저 모두 지원하지만, pnpm의 구현이 가장 성숙하다.

빌드 도구는 역할을 나눠 이해하자. tsc는 타입 체크, esbuild/swc는 빠른 트랜스파일, Vite는 개발 서버 + 프론트엔드 번들, Turbopack은 Next.js 생태계. 타입 체크와 빌드를 분리하는 패턴(`tsc --noEmit` + esbuild)이 실무의 표준이다.

tsconfig 옵션은 카테고리로 이해하자. strict 계열, 타깃 계열, 모듈 계열, 출력 계열. 구체적인 옵션 사전은 부록 B에서 찾아볼 수 있다.

monorepo에서는 `tsconfig.references`와 `composite: true`를 반드시 설정하자. 이 두 줄이 IDE 폭주를 막는다. Turborepo는 태스크 파이프라인과 캐싱으로 빌드 시간을 줄여준다.

런타임은 2025년 기준 Node.js가 기본값, Bun이 개발 도구로 빠른 채택, Deno가 보안·표준 환경에서의 선택지다. 프로덕션 서버는 아직 Node.js LTS가 안전한 선택이다.

---

> **📖 더 깊이 가려면**
>
> - **부록 B** — tsconfig 옵션 사전. 이 챕터에서 호명한 옵션들의 전체 목록과 카테고리별 설명.
> - Node.js 공식 문서 ES Modules 섹션 — `package.json`의 `"exports"` 필드 conditional exports 명세.
> - Matt Pocock의 Total TypeScript — tsconfig cheat sheet. https://www.totaltypescript.com/tsconfig-cheat-sheet
> - 카카오 기술블로그 — "TypeScript Monorepo with pnpm". https://tech.kakao.com/
> - pnpm 공식 문서 workspaces 섹션. https://pnpm.io/workspaces
> - Turborepo 공식 문서. https://turbo.build/repo

---

다음 9장에서는 이 모든 도구 설정이 이미 JS로 작성된 코드베이스 위에 올라가야 하는 상황을 다룬다. 입사 첫째 날, 기존 JS 코드베이스를 TypeScript로 옮기라는 지시를 받았다면 어디서부터 시작해야 하는가. `allowJs`, `@ts-check`, codemod, `.d.ts` 직접 작성, 그리고 점진적 strict 강화까지 — 마이그레이션의 현실적인 로드맵을 함께 그려보자.

---

# 4부 — 전환

이론은 충분히 쌓였다. 이제 현실의 가장 고통스러운 질문 — "이미 돌아가고 있는 JavaScript 코드베이스를 어떻게 TypeScript로 바꾸는가" — 에 답할 차례다. 항공기 엔진을 비행 중에 교체하는 작업이다. 멈추지 않으면서 바꾸는 법, 점진적으로 안전망을 조여가는 법, 팀 전체가 함께 가는 법. 4부는 이론이 아니라 로드맵이다.

이 부에서 만나는 챕터:
- 9장. 기존 JS 코드를 TS로 옮기기 — 점진적 도입의 패턴

---


> 8장에서 빌드 도구의 분열을 이해하고, ESM/CJS 공존 환경에서의 의도적 선택을 손에 넣었다. 그런데 이 모든 도구 설정이 이미 JavaScript로 작성된 코드베이스 위에 올라가야 한다면 어떻게 할까. 입사 첫날, 기존 JS 코드베이스를 TypeScript로 옮기라는 지시를 받은 상황. 9장이 그 현실적 로드맵을 함께 그린다.

# 9장. 기존 JS 코드를 TS로 옮기기 — 점진적 도입의 패턴

오늘 출근했더니 PM이 슬랙으로 이런 메시지를 보냈다고 상상해보자.

> "아, 그리고 신규 입사하셨으니 JS 코드베이스 TS 전환 태스크 맡겨도 될까요? 일단 검토부터만이요 :smile:"

검토부터만. 그 "일단"이 담고 있는 무게를 우리는 안다. 코드베이스는 3만 줄짜리 레거시 Express 서버다. 파일 수는 217개. `.js` 확장자가 단 하나의 예외도 없이 붙어 있다. `require`와 `module.exports`가 온 파일에 가득하다. 타입 주석 따위는 없다. JSDoc조차 없다. 그냥 날것의 JavaScript다.

어디서부터 시작해야 할까?

이 질문은 단순히 "TS를 어떻게 쓰는가"의 문제가 아니다. "기존에 움직이는 시스템을 멈추지 않고 어떻게 바꾸는가"의 문제다. 항공기 엔진을 비행 중에 교체하는 작업과 비슷하다. 그래서 이 챕터는 이론이 아니라 로드맵이다. 입사 첫째 달의 가장 절박한 질문에 손에 잡히는 답을 주려 한다.

---

## 마이그레이션의 세 길

기존 JS 코드베이스를 TS로 옮기는 방법에는 크게 세 가지 길이 있다. 각각 비용과 리스크가 다르고, 팀과 코드베이스의 상황에 따라 최적의 선택이 달라진다.

### 첫 번째 길: 한 번에 전부 (Big Bang)

첫 번째는 가장 직관적인 접근이다. 모든 `.js` 파일을 한꺼번에 `.ts`로 바꾸고, `tsconfig.json`을 세팅하고, 컴파일 에러를 몽땅 잡아낸다. 그런 다음 PR을 올린다.

이 방법이 현실에서 잘 통하는 경우는 딱 하나다. 코드베이스가 소규모이고, 팀이 TS에 능숙하고, 전환 기간 동안 새 기능 개발을 완전히 멈출 수 있을 때다.

조건이 셋 다 맞아야 한다.

현실에서는? 대부분의 경우 셋 중 하나도 충족되지 않는다. 코드베이스는 크고, 팀원은 TS를 처음 만지고, 제품 로드맵은 멈추지 않는다. Big Bang 전환을 시도했다가 3개월 만에 포기하고 반쯤 전환된 코드베이스를 남긴 사례는 한국 개발 커뮤니티에서도 심심찮게 들린다. 난감한 일이다.

그래서 첫 번째 길은 작은 사이드 프로젝트나, 이미 개발이 완료되어 변경이 거의 없는 유틸리티 모듈처럼 격리된 서브시스템에만 권장하는 편이 낫다.

### 두 번째 길: 새 파일만 TS (Strangler Fig)

두 번째는 실용적인 접근이다. 기존 `.js` 파일은 그대로 두고, 앞으로 새로 만드는 파일만 `.ts`로 작성한다. 이름은 마틴 파울러의 Strangler Fig 패턴에서 빌려왔다. 오래된 나무를 서서히 감아 올라가는 덩굴처럼, 새 TS 코드가 기존 JS 코드를 점진적으로 대체한다.

`tsconfig.json`에서 `allowJs: true`를 켜면 `.ts` 파일이 `.js` 파일을 `import`할 수 있다. 이렇게 하면 두 세계가 평화롭게 공존한다. 새로운 API 엔드포인트는 TS로, 오래된 레거시 핸들러는 일단 JS로 놔둔다.

이 방법의 장점은 리스크가 낮다는 것이다. 기존 코드에 손대지 않으니 회귀 가능성이 최소화된다. 단점은 속도가 느리다는 것이다. 코드베이스가 큰 경우, 두 언어가 수년간 공존할 수도 있다. 어떤 팀에는 그게 괜찮다. 어떤 팀에는 안 된다.

Strangler Fig의 중요한 변형이 있다. 기존 JS 파일을 새로운 기능 추가나 버그 수정이 필요할 때마다 그 파일만 TS로 전환하는 것이다. "건드린 파일은 TS로 졸업" 룰을 팀 내에서 약속하면, 자연스럽게 코드베이스 전체가 TS 방향으로 기운다. 개발 속도를 유지하면서 마이그레이션을 병행하는 현실적인 접근이다.

### 세 번째 길: `allowJs` + `checkJs`로 점진 (Gradual)

세 번째는 가장 섬세한 접근이다. `.js` 파일을 `.ts`로 바꾸지 않고도 타입 체크를 받는 방법이다. TS 컴파일러가 JS 파일도 분석해준다.

`tsconfig.json`에 두 가지 옵션을 추가한다.

```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true
  }
}
```

`allowJs`는 "TS 컴파일러야, JS 파일도 같이 처리해"라는 뜻이다. `checkJs`는 "처리할 때 타입 검사도 해"라는 뜻이다. 이 두 옵션을 켜면 `.js` 파일에서도 타입 오류를 잡아준다.

파일 단위로 점진 적용하고 싶다면 `// @ts-check` 주석 한 줄로 해결할 수 있다.

```javascript
// @ts-check

/** @type {string} */
const greeting = 42; // 오류: Type 'number' is not assignable to type 'string'
```

파일 맨 위에 `// @ts-check`를 추가하면 그 파일에서만 타입 체크가 활성화된다. 팀이 준비된 파일부터 하나씩 추가하는 방식으로 접근할 수 있어, 전체 코드베이스에 한꺼번에 충격을 주지 않는다.

세 번째 길의 진짜 강점은 JSDoc으로 타입을 표현할 수 있다는 것이다. 파일은 `.js`로 유지하면서, 주석 형태로 타입 정보를 붙인다. TS 컴파일러는 이 JSDoc을 읽고 타입 체크를 수행한다.

```javascript
// @ts-check

/**
 * @param {string} name
 * @param {number} age
 * @returns {string}
 */
function createGreeting(name, age) {
  return `안녕, ${name}! 나이는 ${age}살이군요.`;
}
```

"이게 의미가 있어?"라고 물을 수 있다. 생각보다 훨씬 강력하다. IDE에서 자동 완성이 되고, 함수 시그니처가 문서처럼 보이고, 잘못된 인자를 넘기면 에러가 뜬다. `.js` 파일을 그대로 두면서도 TS의 안전망을 상당 부분 얻는다.

토스 테크 블로그의 "JavaScript에서 TypeScript로 바꾸기" 시리즈는 이 세 번째 길이 실제로 한국 현장에서 얼마나 자주 채택되는지를 잘 보여준다. (출처: toss.tech, 사실 확인 필요 — 시리즈 정확한 내용은 원문 참조) 핵심 메시지는 "한 번에 다 바꾸려 하지 말고, 체계를 잡아라"다.

---

> **Java/Kotlin 시선 ① — Kotlin-Java 혼재 프로젝트 ↔ TS/JS 혼재**
>
> Spring 프로젝트에 Kotlin을 도입할 때를 떠올려보자. 처음에는 새 서비스 클래스만 Kotlin으로 작성한다. 기존 Java 클래스는 그대로 둔다. Kotlin 파일이 Java 클래스를 `import`하고, Java 클래스가 Kotlin 함수를 호출한다. 두 언어는 JVM 위에서 아무 문제 없이 공존한다.
>
> TS/JS 혼재도 정확히 같은 그림이다. `allowJs: true`를 켜면 `.ts` 파일이 `.js` 파일을 `import`할 수 있고, 빌드도 함께 된다. Kotlin 도입 때처럼 새 파일만 TS로 작성하고, 기존 JS는 점진적으로 교체해나가면 된다.
>
> 한 가지 차이가 있다. Kotlin-Java 혼재에서는 컴파일러가 두 언어의 타입 정보를 완벽히 교환한다. TS-JS 혼재에서는 `.js` 쪽의 타입 정보가 불완전하다. `checkJs`를 켜거나 JSDoc을 써야 TS가 JS 파일의 내부를 이해한다. 그렇지 않으면 `.js` 모듈에서 온 값은 전부 `any`로 취급된다.
>
> ```typescript
> // utils.js (JSDoc 없음)
> function add(a, b) { return a + b; }
> module.exports = { add };
>
> // app.ts
> import { add } from './utils'; // add: any
> const result = add("hello", "world"); // 오류 없음 — 찜찜하다
> ```
>
> JSDoc을 붙이거나 `.ts`로 전환하거나, 아니면 `*.d.ts` 파일을 따로 작성해야 한다. 이에 대해서는 뒤에서 자세히 다룬다.

---

## `allowJs` · `checkJs` · `@ts-check`의 실전

세 번째 길을 택했다면, 이 세 가지 도구를 어떻게 조합하는지 좀 더 구체적으로 알아보자.

### tsconfig.json에서 범위 제어하기

`checkJs: true`를 켜면 프로젝트의 모든 `.js` 파일에 타입 체크가 적용된다. 처음에는 오류가 수백 개 쏟아질 수 있다. 겁먹지 말자. `include`와 `exclude`로 적용 범위를 제어할 수 있다.

```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "strict": false
  },
  "include": ["src/**/*"],
  "exclude": ["src/legacy/**"]
}
```

`src/legacy/` 폴더는 일단 제외한다. 나머지 영역부터 천천히 타입 오류를 잡아나간다.

특정 파일에서 `checkJs`를 끄고 싶다면 파일 맨 위에 `// @ts-nocheck`를 붙인다. 전체 적용 중에 예외를 두는 방법이다.

```javascript
// @ts-nocheck
// 이 파일은 아직 마이그레이션 준비 안 됨
const legacyConfig = require('./old-config');
```

반대로 `checkJs: false` 상태에서 특정 파일만 체크하려면 `// @ts-check`를 쓴다. 파일 단위 점진 적용의 핵심 도구다.

### JSDoc으로 타입을 표현하는 기술

`@ts-check` 환경에서 타입을 표현하는 데 JSDoc은 생각보다 강력하다. 기본 타입부터 복잡한 제네릭까지 표현할 수 있다.

```javascript
// @ts-check

/** @type {Map<string, number>} */
const scores = new Map();

/**
 * @template T
 * @param {T[]} arr
 * @param {(item: T) => boolean} predicate
 * @returns {T[]}
 */
function filter(arr, predicate) {
  return arr.filter(predicate);
}

/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} name
 * @property {number} age
 */

/** @param {User} user */
function greetUser(user) {
  console.log(`안녕하세요, ${user.name}님!`);
}
```

`@typedef`로 타입 별칭도 만들 수 있다. 별도 `.d.ts` 파일에 타입을 정의하고 `@import`로 가져올 수도 있다.

```javascript
// @ts-check
/** @import { User } from './types.d.ts' */

/** @param {User} user */
function greetUser(user) { /* ... */ }
```

JSDoc이 `.ts` 파일의 타입 주석보다 장황한 것은 사실이다. 하지만 파일을 `.ts`로 바꾸지 않아도 되니, 기존 빌드 시스템이나 도구 체인에 영향을 주지 않는다. 프론트엔드·백엔드 모두 이 방식을 중간 단계로 활용하고, 안정화가 되면 `.ts`로 전환하는 흐름이 자연스럽다.

---

## strict 단계 도입 전략 — 언제 무엇을 켤까

마이그레이션의 가장 큰 실수 중 하나는 처음부터 `"strict": true`를 켜고 시작하는 것이다. 오류가 폭발하고, 팀원이 지쳐서 `any`를 도배하기 시작한다. 마이그레이션이 목적인지 `any` 제거가 목적인지 헷갈린다.

단계별로 접근하는 편이 낫다.

### 0단계: 타입 없이 컴파일만

```json
{
  "compilerOptions": {
    "allowJs": true,
    "noEmit": true,
    "strict": false
  }
}
```

먼저 타입 오류를 신경 쓰지 않고 TS 컴파일러가 코드베이스를 읽을 수 있게만 한다. `noEmit: true`로 파일은 출력하지 않는다. 이 단계에서 모듈 해석 오류나 문법 오류만 잡는다.

### 1단계: `noImplicitAny` 먼저

```json
{
  "compilerOptions": {
    "noImplicitAny": true
  }
}
```

`noImplicitAny`는 타입이 추론되지 않아 `any`가 되는 상황을 오류로 만든다. 가장 기본적이고, 가장 많은 버그를 미리 잡아준다. 이 옵션부터 켜고 오류를 하나씩 잡아나가는 것이 가장 좋다.

대표적인 오류 유형은 두 가지다.

```typescript
// 오류 1: 함수 파라미터 타입 없음
function processData(data) { // Parameter 'data' implicitly has an 'any' type
  return data.length;
}

// 오류 2: 객체 프로퍼티가 나중에 추가됨
const config = {};
config.port = 3000; // Property 'port' does not exist on type '{}'
```

첫 번째는 파라미터에 타입을 붙이면 된다. 두 번째는 객체의 타입을 처음부터 명시해야 한다.

`noImplicitAny` 오류를 다 잡으면 코드베이스의 타입 안전성이 눈에 띄게 올라간다. 이 단계에서 기존에 존재하던 버그가 드러나는 경우도 많다.

### 2단계: `strictNullChecks`

```json
{
  "compilerOptions": {
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

`strictNullChecks`는 `null`과 `undefined`를 타입 시스템에서 분리한다. Java의 `Optional<T>`가 타입 수준에서 강제하는 것과 비슷한 효과다.

이 옵션을 켜면 기존 코드에서 null 참조 버그가 될 가능성이 있는 지점들이 컴파일 타임에 드러난다.

```typescript
// strictNullChecks 활성화 후
function findUser(id: string): User | null {
  return db.find(id) ?? null;
}

const user = findUser("123");
console.log(user.name); // 오류: Object is possibly 'null'
```

타입 체크가 없었을 때는 런타임에 `TypeError: Cannot read properties of null`로 터졌을 코드다. 이제 컴파일 시점에 잡힌다.

`strictNullChecks`는 `noImplicitAny`보다 오류가 더 많이 나온다. 하지만 이 오류들이 실제 잠재적 버그다. 잡아낼수록 코드가 견고해진다고 생각하면 그나마 덜 찜찜하다.

### 3단계: 전체 `strict`

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict: true`는 여러 옵션의 묶음이다.

- `noImplicitAny`
- `strictNullChecks`
- `strictFunctionTypes`
- `strictBindCallApply`
- `strictPropertyInitialization`
- `noImplicitThis`
- `useUnknownInCatchVariables`
- `alwaysStrict`

1단계와 2단계를 거쳐 왔다면 이 단계에서 나오는 추가 오류는 상대적으로 적다. 여기서 잡히는 오류들은 함수 타입의 공변성·반공변성 문제, `this` 바인딩 문제, 클래스 프로퍼티 초기화 누락 등이다.

`strictFunctionTypes`가 잡는 오류를 예로 보자. 콜백 함수 파라미터의 타입이 더 좁은 타입을 받도록 선언되어 있을 때다.

```typescript
// strictFunctionTypes 활성화 전에는 통과했던 코드
type EventHandler = (event: MouseEvent) => void;
const handler: EventHandler = (event: Event) => { // 이제 오류
  console.log(event.target);
};
```

`Event`는 `MouseEvent`보다 넓은 타입이다. 함수 파라미터는 반공변(contravariant)이어야 안전한데, `strictFunctionTypes` 없이는 이 검사가 느슨했다. 켜고 나면 이런 종류의 타입 불일치가 드러난다.

`strictPropertyInitialization`은 클래스 프로퍼티가 생성자에서 초기화되지 않는 경우를 잡는다.

```typescript
class UserService {
  private db: Database; // 오류: Property 'db' has no initializer
  
  constructor() {
    // db가 초기화되지 않음
  }
}

// 올바른 처리 방법들:
class UserService {
  // 방법 1: 생성자에서 초기화
  private db: Database;
  constructor(db: Database) {
    this.db = db;
  }
  
  // 방법 2: 확정 할당 단언 (정말로 나중에 할당한다는 보증)
  private db!: Database; // !는 "내가 책임진다"는 신호
  
  // 방법 3: 선택적 프로퍼티로 표현
  private db?: Database;
}
```

NestJS처럼 DI 컨테이너가 주입해주는 경우엔 `!` 단언을 흔히 쓴다. 하지만 남용하면 `strictPropertyInitialization`을 켠 의미가 희석된다. 가능하면 생성자 주입 방식을 쓰는 편이 낫다.

3단계까지 완료하면 마이그레이션의 핵심이 끝났다고 볼 수 있다. 그 다음부터는 `noUnusedLocals`, `noUnusedParameters`, `exactOptionalPropertyTypes` 같은 추가 옵션을 상황에 따라 켜볼 수 있다.

`exactOptionalPropertyTypes`는 꽤 까다롭다. 선택적 프로퍼티(`age?: number`)에 `undefined`를 명시적으로 넣는 것과 프로퍼티 자체가 없는 것을 구분한다. 켜면 기존 코드에서 예상치 못한 오류가 많이 나올 수 있다. 팀이 TS에 충분히 익숙해진 후에 도입하는 편이 좋다.

### 단계별 도입의 실전 타임라인

각 단계를 얼마나 빠르게 진행할 수 있는지는 코드베이스 크기와 팀 규모에 따라 다르다. 대략적인 기준을 제시하면 이렇다.

| 코드베이스 규모 | 0단계 | 1단계 | 2단계 | 3단계 |
|---|---|---|---|---|
| 소규모 (5,000줄 이하) | 1일 | 1주 | 2주 | 1개월 |
| 중규모 (5만 줄 이하) | 1주 | 1개월 | 2개월 | 4개월 |
| 대규모 (5만 줄 이상) | 2주 | 2개월 | 4개월 | 6개월+ |

이 숫자는 "전담 인력이 마이그레이션만 집중할 때"가 아니라, "기존 개발과 병행할 때"를 기준으로 한다. 전담 팀을 만들 수 있다면 절반으로 줄일 수 있다.

단계를 너무 빨리 넘어가려 하지 말자. 1단계 오류가 100개가 넘는데 2단계를 켜는 건 팀을 지치게 만든다. 각 단계에서 오류 수를 제로로 만든 후에 다음 단계로 가는 게 심리적으로도 기술적으로도 옳다.

---

## 자동 codemod — 도구에 기댈 수 있는 부분

17만 줄짜리 코드베이스를 손으로 하나씩 전환하는 건 끔찍한 일이다. 자동화 도구에 기댈 수 있는 부분이 있다.

### ts-migrate (Airbnb)

Airbnb가 만든 `ts-migrate`는 JS 파일을 TS 파일로 변환하는 codemod 도구다. 다음과 같이 사용한다.

```bash
npx ts-migrate-full .
```

이 명령어 하나로 프로젝트의 모든 `.js` 파일을 `.ts`로 바꾸고, `any`로 타입을 채워 컴파일 오류가 없는 상태를 만든다. 여기서 중요한 포인트가 있다 — "컴파일 오류가 없는" 상태를 만드는 것이지, "타입이 올바른" 상태를 만드는 게 아니다.

변환 후 코드를 보면 이런 모양이 많다.

```typescript
// ts-migrate가 생성한 코드
function processUser(user: any) {
  return user.name + " " + user.age;
}
```

`any`가 가득 찼다. 하지만 컴파일은 된다. 이제부터 사람이 `any`를 하나씩 구체적인 타입으로 바꿔나가는 작업이다. ts-migrate는 그 시작점을 만들어주는 도구다.

### jscodeshift

Facebook이 만든 `jscodeshift`는 AST(추상 구문 트리) 기반 코드 변환 도구다. ts-migrate처럼 전용 변환을 하는 게 아니라, 코드를 AST로 파싱하고 변환하는 프레임워크다.

```bash
npx jscodeshift -t ./transform.ts src/**/*.js
```

`transform.ts`에 변환 로직을 직접 작성해야 해서 진입 장벽이 높다. 대신 커스텀 변환이 자유롭다. 예를 들어, 특정 함수 이름이 바뀌었을 때 코드베이스 전체에서 자동으로 업데이트하는 용도로 쓰기 좋다.

### ts-morph

`ts-morph`는 TypeScript Compiler API를 더 사용하기 쉽게 감싼 라이브러리다. 코드를 파싱하고, 타입 정보를 활용하고, 수정하고, 저장하는 작업을 JavaScript/TypeScript로 작성할 수 있다.

```typescript
import { Project } from "ts-morph";

const project = new Project({
  tsConfigFilePath: "tsconfig.json",
});

// 모든 함수 파라미터에 타입 정보가 없으면 any를 붙임
for (const sourceFile of project.getSourceFiles()) {
  for (const func of sourceFile.getFunctions()) {
    for (const param of func.getParameters()) {
      if (!param.getTypeNode()) {
        param.setType("any");
      }
    }
  }
}

project.saveSync();
```

ts-migrate보다 세밀한 제어가 가능하다. 사내 코딩 컨벤션에 맞는 커스텀 변환을 만들 때 ts-morph가 좋은 선택지가 된다.

### 도구의 한계를 알고 써야 한다

자동 codemod 도구들의 공통 한계를 기억해두자.

첫째, **의미를 이해하지 못한다.** 코드의 구조를 바꾸지, 코드의 의도를 파악하지 않는다. `any`를 붙이는 것이 올바른 타입으로 바꾸는 것이 아니라는 걸 도구는 모른다.

둘째, **런타임 동작을 보장하지 않는다.** 변환 후 테스트가 반드시 필요하다. 자동 변환이 예상치 못한 방식으로 코드를 바꿀 수 있다.

셋째, **60%만 자동화할 수 있다.** 이 부분은 뒤에서 Kristensen-Møller의 연구와 함께 더 깊이 다룬다.

자동 codemod는 시작점을 만들어주는 도구다. 마이그레이션을 완료해주는 도구가 아니다. 그 사실을 PM에게도 명확히 전달해두자.

---

## DefinitelyTyped — 외부 라이브러리에 타입 입히기

TS로 전환하다 보면 이런 오류를 자주 만난다.

```
Could not find a declaration file for module 'express'.
'/node_modules/express/index.js' implicitly has an 'any' type.
Try `npm install @types/express` if it exists or add a new declaration (.d.ts) file containing `declare module 'express';`
```

TS로 작성되지 않은 라이브러리, 즉 타입 정의가 없는 라이브러리를 가져올 때 생기는 오류다. 해결 방법은 메시지가 친절하게 알려준다.

```bash
npm install -D @types/express
npm install -D @types/node
npm install -D @types/lodash
```

`@types/` 접두사가 붙은 패키지들이 바로 DefinitelyTyped다. Microsoft가 관리하는 타입 정의 저장소로, 수천 개의 JS 라이브러리에 대한 타입 정의를 담고 있다. 커뮤니티가 기여하고 유지한다.

설치하면 해당 라이브러리를 import할 때 자동 완성, 타입 체크, 문서 정보가 모두 IDE에서 표시된다.

```typescript
import express, { Request, Response } from 'express';

const app = express();

app.get('/user', (req: Request, res: Response) => {
  const id = req.query.id; // string | string[] | ParsedQs | ParsedQs[] | undefined
  res.json({ id });
});
```

타입 정의가 있으니 `req.query.id`의 타입을 IDE가 알려준다. 잘못된 프로퍼티를 접근하면 컴파일 오류가 난다.

요즘은 많은 라이브러리가 직접 타입 정의를 포함한다. `npm install zod`를 하면 타입 정의가 자동으로 함께 온다. `package.json`에 `"types"` 또는 `"typings"` 필드가 있으면 별도 `@types/` 패키지가 필요 없다.

그렇다면 어떤 라이브러리가 `@types/*`가 필요하고, 어떤 라이브러리는 필요 없을까? IDE의 오류 메시지가 가장 정직한 안내자다. 오류가 나면 그때 설치하면 된다.

---

> **Java/Kotlin 시선 ② — Kotlin-Java Interop ↔ DefinitelyTyped + d.ts**
>
> Kotlin에서 Java 라이브러리를 쓸 때를 생각해보자. Java 메서드의 null 가능성 정보가 Kotlin에서 플랫폼 타입(`T!`)으로 보인다. `@NotNull`, `@Nullable` 애노테이션이 있으면 Kotlin이 이를 인식해 `T`나 `T?`로 처리한다. Kotlin-Java interop은 타입 정보를 최대한 끌어오려 하지만, 결국 Java 원본의 타입 정보 품질에 의존한다.
>
> TS-JS 상황에서 `@types/*`는 이 역할을 한다. JS 라이브러리에 타입 정보를 입힌다. `@NotNull`과 `@Nullable` 대신 `.d.ts` 파일이다.
>
> 차이도 있다. Kotlin-Java interop은 JVM 위에서 두 언어가 런타임에 직접 대화한다. TS의 `@types/*`는 컴파일 타임 전용이다. 런타임에는 타입 정보가 전혀 없다 — 타입은 사라진다(type erasure). 그래서 `@types/express`를 설치해도 실제로 실행되는 코드는 원래의 JS express 그대로다. 타입 정의는 오직 개발자와 컴파일러의 대화를 위한 것이다.
>
> ```typescript
> // @types/express 설치 후
> import express from 'express'; // 타입 정보 있음, IDE 자동완성 완비
>
> // 런타임에는?
> // → 그냥 node_modules/express/index.js가 실행됨
> // → 타입 정보는 컴파일 후 모두 삭제됨
> ```

---

## `*.d.ts` 직접 작성 — 타입이 없을 때의 대응

`@types/*` 패키지가 없는 라이브러리도 있다. 오래되었거나, 마이너하거나, 회사 내부 모듈이거나. 이때는 직접 `.d.ts` 파일을 작성해야 한다.

### 라이브러리에 타입 정의가 없을 때

가장 간단한 대응은 모듈 선언을 빈 채로 두는 것이다.

```typescript
// src/types/legacy-lib.d.ts
declare module 'legacy-lib';
```

이렇게 하면 import할 때 오류가 사라지고, 모든 값은 `any`가 된다. 임시방편이다. 찜찜하지만 일단 컴파일을 통과시키는 방법이다.

제대로 하려면 실제 API를 반영한 타입을 작성해야 한다.

```typescript
// src/types/legacy-lib.d.ts
declare module 'legacy-lib' {
  export interface Options {
    host: string;
    port: number;
    timeout?: number;
  }

  export function connect(options: Options): Connection;

  export interface Connection {
    send(data: string): Promise<void>;
    close(): void;
  }
}
```

작성할 때 라이브러리의 실제 JS 소스 코드나 README를 보면서 API를 따라 작성한다. 완벽하지 않아도 된다. 자주 쓰는 함수부터 타입을 붙이고, 나머지는 나중에 채운다.

### 사내 모듈 Augmentation

회사 내부에서 만든 공용 모듈이 있다고 하자. 원래 JS로 작성되었고 타입이 없다. 이 모듈을 TS 프로젝트에서 사용할 때, 원본을 건드리지 않고 타입을 입히는 방법이 있다. module augmentation이다.

```typescript
// src/types/internal-utils.d.ts
declare module '@company/internal-utils' {
  export function formatDate(date: Date, format: string): string;
  export function parseId(raw: string): number;
  
  export interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
  }
}
```

기존 모듈의 타입을 보강할 수도 있다. 예를 들어 Express의 `Request` 객체에 사내 인증 정보를 추가하는 경우다.

```typescript
// src/types/express.d.ts
import 'express';

declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        roles: string[];
      };
    }
  }
}
```

이렇게 하면 이후 모든 Express `req` 객체에서 `req.user`를 타입 안전하게 쓸 수 있다. 미들웨어에서 `req.user`를 설정하고, 라우터에서 `req.user?.id`를 읽을 때 타입 오류가 나지 않는다.

---

## 마이그레이션 중의 양면 운영

마이그레이션은 하루아침에 끝나지 않는다. 몇 주, 몇 달, 때로는 1년 이상이 걸린다. 그동안 JS와 TS가 같은 코드베이스에서 공존한다. 이 양면 운영 기간을 어떻게 관리하느냐가 마이그레이션의 성패를 가른다.

### PR 리뷰의 기준 통일

가장 먼저 팀 내에서 합의해야 할 것은 PR 리뷰 기준이다. "TS 파일에는 `any` 금지, JS 파일은 지금은 OK"처럼 명확한 기준이 없으면 리뷰 때마다 팀원 간에 마찰이 생긴다.

권장하는 방식은 이렇다.

- **신규 `.ts` 파일**: `any` 사용 최소화. 리뷰어가 대안 타입을 제안한다.
- **기존 `.js` 파일을 TS로 전환한 파일**: 전환 시점에서 `any`는 허용하되, TODO 주석을 달아 추적한다.
- **건드리지 않은 `.js` 파일**: 타입 기준 리뷰 없음.

```typescript
// TODO(migration): any 제거 필요 — user 타입 확인 후 교체
function processUser(user: any) {
  return user.name;
}
```

`TODO` 주석을 달아두면 나중에 `grep -r "TODO(migration)"` 로 전체 현황을 파악할 수 있다. CI에 이런 TODO의 수를 추적하는 스크립트를 붙여두는 팀도 있다.

### CI에 점진 strict 강화 전략 심기

CI에 두 가지 타입 체크를 동시에 돌리는 패턴을 추천한다.

```json
// package.json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "typecheck:strict": "tsc --noEmit --strict"
  }
}
```

`typecheck`은 현재 tsconfig 기준으로 통과해야 한다. PR이 이걸 깨면 머지 불가다.

`typecheck:strict`는 현재 통과 여부와 상관없이 결과만 기록한다. 처음에는 strict 오류가 수백 개다. 매 PR마다 이 숫자가 줄어드는지 추적한다. 줄어드는 방향으로 팀이 나아가고 있다는 신호가 된다.

어느 시점이 되면 `typecheck:strict`도 통과하게 된다. 그때 tsconfig에서 `"strict": true`를 정식으로 켜고, `typecheck:strict` 스크립트를 `typecheck`으로 승격시킨다.

```yaml
# .github/workflows/ci.yml
- name: Type Check
  run: npm run typecheck

- name: Strict Type Check (Tracking)
  run: npm run typecheck:strict || true  # 실패해도 CI를 막지 않음
  # 오류 수를 추적하고 싶다면 출력을 파싱해 메트릭으로 저장
```

이 패턴의 장점은 팀 전체가 현재 위치를 객관적으로 볼 수 있다는 것이다. "우리 코드베이스의 strict 오류가 이번 스프린트에 47개 줄었다"는 수치는 동기부여가 된다.

### 혼재 코드베이스에서 IDE 경험 유지

JS와 TS가 섞인 환경에서 IDE가 느려지거나 자동 완성이 제대로 작동하지 않으면 개발자 경험이 나빠진다. 특히 프로젝트가 큰 경우 TS 언어 서버(tsserver)가 모든 파일을 처리하려다 폭주하는 일이 생긴다. 개발하다가 자동 완성이 5초씩 걸리기 시작하면 정말 난감하다.

이를 예방하는 설정이 있다.

```json
{
  "compilerOptions": {
    "allowJs": true,
    "maxNodeModuleJsDepth": 1
  }
}
```

`maxNodeModuleJsDepth`는 `node_modules` 안의 JS 파일을 어느 깊이까지 분석할지 제어한다. 기본값이 너무 크면 tsserver가 수만 개의 파일을 분석한다.

VS Code에서는 `.vscode/settings.json`에 다음을 추가하면 특정 폴더를 IDE 분석에서 제외할 수 있다.

```json
{
  "typescript.tsdk": "./node_modules/typescript/lib",
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true
  }
}
```

카카오나 당근 같은 모노레포 환경에서는 `tsconfig.references`를 활용해 프로젝트를 논리 단위로 분리하는 것도 IDE 성능 유지에 중요하다. (이 주제는 8장 모듈·빌드 챕터에서 더 깊이 다뤘다.)

### 브랜치 전략과 마이그레이션 PR

마이그레이션 PR은 일반 기능 PR과 성격이 다르다. 리뷰어가 타입 변경이 올바른지 판단하려면 맥락이 필요하다. 몇 가지 관례를 만들면 리뷰 마찰을 줄일 수 있다.

**파일 단위 PR**: 파일 하나, 또는 밀접하게 연관된 파일 묶음을 하나의 PR로 올린다. 한 PR에 파일 50개를 올리면 리뷰어가 무엇을 봐야 할지 모른다.

**"타입만 추가" PR 레이블**: 런타임 동작 변경이 없는 순수 타입 추가 PR임을 레이블로 표시한다. 리뷰어가 로직 변경 없이 타입만 검증하면 된다는 걸 알면 리뷰 속도가 빨라진다.

**변환 전후 diff 설명**: PR 설명에 "이 파일의 before/after" 를 간단히 적어준다.

```markdown
## 변환 내용
- `user-service.js` → `user-service.ts`
- `UserService` 클래스에 생성자 파라미터 타입 추가
- `getUser()` 반환 타입 `Promise<User | null>` 명시
- `any` 2개 → 구체 타입으로 교체 (주석 참조)

## 런타임 변경
없음. 타입 주석만 추가.

## 테스트
기존 테스트 전부 통과 확인.
```

이런 설명 하나가 리뷰 사이클을 반으로 줄인다. "왜 이렇게 바꿨지?"라는 질문이 줄어드니까.

### 마이그레이션 대시보드 만들기

규모가 큰 마이그레이션이라면 진행 상황을 팀 전체가 볼 수 있는 대시보드를 만드는 것도 좋다. 복잡한 도구가 필요 없다. CI에서 매 빌드마다 지표를 출력하는 스크립트 하나면 충분하다.

```bash
#!/bin/bash
# scripts/migration-status.sh

JS_FILES=$(find src -name "*.js" -not -path "*/node_modules/*" | wc -l | tr -d ' ')
TS_FILES=$(find src -name "*.ts" -not -name "*.d.ts" -not -path "*/node_modules/*" | wc -l | tr -d ' ')
TOTAL=$((JS_FILES + TS_FILES))
TS_PERCENT=$((TS_FILES * 100 / TOTAL))

ANY_COUNT=$(grep -r ": any" src --include="*.ts" | wc -l | tr -d ' ')
TS_IGNORE=$(grep -r "@ts-ignore" src | wc -l | tr -d ' ')

echo "=== Migration Status ==="
echo "JS files remaining: $JS_FILES"
echo "TS files done: $TS_FILES / $TOTAL ($TS_PERCENT%)"
echo "any count: $ANY_COUNT"
echo "@ts-ignore count: $TS_IGNORE"
echo "========================"
```

이 스크립트를 CI에 붙여두면 매 PR마다 현황이 찍힌다. PR 코멘트로 자동 게시하면 더 좋다. "이번 PR로 TS 비율이 47%에서 49%로 올랐습니다"라는 문구 하나가 팀 사기에 긍정적인 영향을 준다.

숫자가 가시화되면 마이그레이션이 추상적인 기술 부채 해소가 아니라, 구체적인 진척으로 느껴진다. 그것이 중단되지 않는 마이그레이션의 비결 중 하나다.

---

> **함정 박스 — 마이그레이션 중 `any` 폭증 통제**
>
> **증상**: 마이그레이션을 시작하고 몇 주 후, 코드베이스 전체에 `any`가 가득하다. 컴파일은 되는데 타입 안전성은 마이그레이션 전과 다를 게 없다.
>
> **원인**: `noImplicitAny`를 끄고 시작했거나, ts-migrate 이후 생성된 `any`를 방치했거나, 리뷰 기준이 없어 "일단 `any`로 때우자"는 관행이 자리 잡았다.
>
> **처방**: 세 가지를 동시에 적용한다.
>
> 1. **ESLint `@typescript-eslint/no-explicit-any` 규칙 켜기**: `any` 사용 시 경고를 낸다. 바로 `error`로 올리면 충격이 크니 `warn`으로 시작해서 점차 `error`로 강화한다.
>
>    ```json
>    // .eslintrc.json
>    {
>      "rules": {
>        "@typescript-eslint/no-explicit-any": "warn"
>      }
>    }
>    ```
>
> 2. **`any` 카운트 추적 스크립트 CI에 추가**: 매 PR마다 `any` 사용 횟수를 측정하고, 이전 대비 증가하면 경고를 낸다. 줄어드는 방향으로 팀이 움직이고 있는지 가시화한다.
>
>    ```bash
>    # CI 스크립트
>    ANY_COUNT=$(grep -r ": any" src/ | wc -l)
>    echo "Current any count: $ANY_COUNT"
>    ```
>
> 3. **`any`에 TODO 주석 의무화 + 기한 명시**: `// any: 2024-Q3 전에 제거 예정`처럼 기한을 붙이면 "언젠가 고치지"가 "이번 분기 안에 고친다"로 바뀐다.
>
> 기억해두자 — `noImplicitAny`는 나중에 켜기가 매우 어렵다. 처음에 끈 채로 마이그레이션을 시작하면 영영 못 켜는 코드베이스가 된다는 걸 수많은 팀이 경험으로 배웠다. 고통스러워도 초기에 켜는 편이 훨씬 낫다.

---

## Kristensen-Møller (2017) — 60%의 한계와 나머지 40%

Erik Kristensen과 Anders Møller의 2017년 논문 "TypeWright: Refactoring JavaScript to TypeScript"는 마이그레이션의 자동화 가능성에 대한 가장 중요한 학술적 답을 준다. 결론은 단순하다. **약 60%만 자동 추론 가능하다.**

이 숫자가 뜻하는 게 무엇인지 구체적으로 풀어보자.

### 자동화가 가능한 60%

타입 추론이 가능한 60%는 어떤 경우인가?

**리터럴 값으로부터 추론**: `const x = 42`는 `number`다. `const name = "Alice"`는 `string`이다. 초기화 값이 있는 변수는 대부분 자동 추론된다.

**함수 반환 타입 추론**: 함수 본문이 명확하면 반환 타입을 추론할 수 있다.

```typescript
function add(a: number, b: number) {
  return a + b; // 반환 타입 number 자동 추론
}
```

**라이브러리 사용 패턴으로 추론**: `@types/express`가 있으면 `req`, `res`의 타입을 자동으로 알 수 있다.

**배열과 객체 리터럴 추론**: `[1, 2, 3]`은 `number[]`, `{ name: "Alice" }`는 `{ name: string }`으로 추론된다.

이런 경우들은 자동화 도구가 잘 처리한다. 코드 패턴을 분석해 타입을 생성하거나, 기존 타입 정보로부터 전파한다.

### 자동화가 불가능한 40%

나머지 40%는 사람의 판단이 필요하다.

**동적으로 생성된 객체**: JS는 런타임에 객체의 구조를 바꿀 수 있다. 어떤 경우에 어떤 프로퍼티가 있는지 정적 분석으로는 알 수 없다.

```javascript
// 이 함수의 반환 타입을 자동으로 알기 어렵다
function createConfig(env) {
  const config = { host: 'localhost' };
  if (env === 'production') {
    config.ssl = true;           // 이 프로퍼티는 특정 조건에서만 생긴다
    config.sslCert = '/cert.pem';
  }
  return config;
}
```

자동 도구는 이 함수의 반환 타입을 `{ host: string }` 또는 `{ host: string, ssl: boolean, sslCert: string }`으로 잘못 추론할 수 있다. 실제로는 `{ host: string } | { host: string, ssl: boolean, sslCert: string }`이거나, discriminated union으로 설계를 바꾸는 게 더 나을 수 있다.

**외부 데이터 경계**: 네트워크 응답, 파일 읽기, 사용자 입력 — 이 데이터들의 타입은 런타임에야 알 수 있다. 컴파일러는 이 데이터가 "실제로 어떤 모양인지"를 알 수 없다.

```typescript
const response = await fetch('/api/user');
const data = await response.json(); // any
```

`data`의 실제 타입은 서버 API 명세를 봐야 안다. 자동 도구가 이걸 알 방법이 없다.

**암묵적 도메인 지식**: 코드에 주석도 없고, 함수 이름만 있다. 이 함수가 무엇을 반환하는지, 파라미터로 어떤 값이 들어오는지는 비즈니스 문맥을 알아야 한다.

```javascript
function processOrder(order) {
  // 이 order가 어떤 모양인지는 도메인을 알아야 한다
  validatePayment(order.payment);
  updateInventory(order.items);
}
```

`order`의 타입은 결제 시스템, 재고 시스템, 주문 도메인 전체를 이해해야 정확히 정의할 수 있다. 자동 도구는 `order.payment`와 `order.items`에 접근한다는 사실만 알 뿐이다.

**타입 설계 결정**: `string`으로 쓸지, `branded type`으로 만들지, discriminated union으로 묶을지 — 이런 결정은 코드 품질과 유지보수성에 영향을 주는 설계 판단이다. 자동화는 가장 단순한 타입을 선택한다. 더 나은 설계는 사람이 판단해야 한다.

### 나머지 40%를 처리하는 전략

자동 도구가 채운 60%를 기반으로, 나머지 40%를 사람이 채울 때 효율적인 방법이 있다.

**도메인 전문가와 함께**: 레거시 코드를 오래 만진 사람이 있다면, 그 사람과 함께 앉아서 핵심 타입을 정의하는 세션을 진행한다. 코드를 분석하는 게 아니라, 도메인을 이해하는 대화다.

**테스트를 타입의 명세로**: 기존 테스트 코드가 있다면, 테스트 입력값과 예상 출력값에서 타입을 역으로 추출할 수 있다. 테스트는 개발자가 코드가 어떻게 동작해야 한다고 생각하는지의 기록이다.

**`unknown`으로 표시하고 점진 해소**: `any` 대신 `unknown`을 쓰면 타입을 확인하기 전에 사용할 수 없어 컴파일러가 체크를 강제한다. 나중에 하나씩 구체화하면서 `unknown`을 실제 타입으로 교체한다.

```typescript
// any: 언제든 써버릴 수 있어서 위험
function parseConfig(raw: any) {
  return raw.port; // 오류 없음, 하지만 위험
}

// unknown: 타입 확인 전에 쓸 수 없어 안전
function parseConfig(raw: unknown) {
  if (typeof raw === 'object' && raw !== null && 'port' in raw) {
    return (raw as { port: number }).port;
  }
  throw new Error('Invalid config');
}
```

60%는 자동화할 수 있다. 나머지 40%는 시간이 걸린다. 그 40%가 사실 코드베이스에서 가장 중요한 부분이다 — 도메인의 핵심 로직, 비즈니스 규칙, 외부 경계. 자동화가 어렵다는 것은 그만큼 중요하다는 신호이기도 하다.

---

> **작가의 한 마디**
>
> 마이그레이션 프로젝트를 여러 번 경험하고 나서 얻은 한 가지 확신이 있다. **마이그레이션은 도구의 문제가 아니라 의지의 문제다.**
>
> ts-migrate든 jscodeshift든 ts-morph든, 도구를 쓰면 시작점이 생긴다. 그 이후는 팀이 꾸준히 나아가느냐의 문제다. 마이그레이션이 중단되는 경우를 보면 도구가 부족해서가 아니다. "일단 `noImplicitAny` 끄고 시작하자"는 타협이 쌓이고, "strict는 나중에 켜자"는 미루기가 반복되고, 새 기능 개발에 치여 마이그레이션 PR이 밀리다가 결국 "레거시는 레거시로 남기자"가 된다.
>
> 60%는 자동화 도구가 채운다. 그런데 진짜 마이그레이션이 끝났다고 말할 수 있는 시점은 나머지 40%, 즉 도메인 핵심 타입이 제자리를 찾았을 때다. 그 40%는 오직 사람의 시간과 판단으로만 채울 수 있다.
>
> 그러니 "어디서부터 시작하냐"보다 더 중요한 질문이 있다. "언제 멈추지 않겠다는 약속을 팀이 할 수 있느냐". 도구는 시작을 도와줄 수 있다. 하지만 끝내는 건 사람이다.

---

## 한국 기업의 마이그레이션 사례

이론을 알았으니, 한국 현장에서 실제로 어떻게 했는지를 보자. 세 회사의 마이그레이션 접근이 각각 다르다. 각자의 상황에서 최선을 선택했고, 그 선택의 이유를 살펴보면 우리 자신의 선택에 참고가 된다.

### 토스 — "JavaScript에서 TypeScript로 바꾸기" 시리즈

토스 테크 블로그의 이 시리즈는 한국 개발자들이 TS 마이그레이션을 공부할 때 가장 먼저 찾는 자료 중 하나다. (출처: toss.tech, 실제 시리즈 내용은 원문 참조 권장)

토스의 접근은 한 마디로 "체계부터 잡고 시작하자"였다. 파일을 하나씩 옮기기 전에, 먼저 `tsconfig.json`을 팀이 합의한 설정으로 만들고, ESLint 규칙을 정하고, 리뷰 기준을 문서화했다. 인프라를 먼저 세우고 나서 마이그레이션을 시작한 것이다.

토스 사례에서 주목할 점은 `@ts-check`를 활용한 중간 단계다. 파일을 `.ts`로 바꾸기 전에, `.js` 상태에서 먼저 JSDoc으로 타입을 붙이고 `@ts-check`로 검증하는 단계를 거쳤다. 이 과정에서 타입이 잘못된 부분, 예상치 못한 데이터 흐름을 미리 발견했다.

왜 이렇게 했을까? 파일을 `.ts`로 바꾸면 팀 전체의 워크플로우가 바뀐다. 빌드 스크립트, CI, import 경로 등 영향 범위가 넓다. `@ts-check`를 중간 단계로 쓰면 타입 정보는 얻으면서도 인프라 변경은 최소화할 수 있다. 전환의 리스크를 나눈 것이다.

또 하나의 교훈은 "any를 남기지 말자는 약속"이었다. 자동 도구로 파일을 변환하면 `any`가 가득 찬다. 토스 팀은 마이그레이션한 파일은 그 PR에서 `any`를 최소화하거나 TODO를 달아 추적한다는 팀 약속을 만들었다. 오늘의 `any`는 내일의 기술 부채가 된다는 것을 경험으로 알았기 때문이다.

이 시리즈가 유독 한국 커뮤니티에서 많이 읽히는 이유는 "우리가 어떤 결정을 왜 했는지"를 솔직하게 적었기 때문이다. 성공 자랑이 아니라 실패에서 배운 것, 팀 내 갈등, 타협의 기록이 있다. 마이그레이션이 기술적 문제만이 아니라 조직적 문제임을 이 시리즈는 솔직히 보여준다.

### 카카오 — pnpm 모노레포 + TS 동시 전환

카카오의 TS 도입 사례는 단순한 언어 전환이 아니었다. TS를 도입하면서 동시에 monorepo 구조를 pnpm workspace 기반으로 재편했다. (출처: tech.kakao.com, 실제 내용은 원문 참조 권장)

왜 두 가지를 동시에 했을까? 역설적이지만, 더 큰 변화 안에 묶어서 하는 게 오히려 저항이 적었다. 모노레포 전환 자체가 코드 구조를 크게 바꾸는 작업이다. 이 기회에 모든 패키지를 TS로 새로 작성했다. 기존 JS 코드를 TS로 마이그레이션하는 게 아니라, 모노레포 패키지들을 처음부터 TS로 만들어 그 안으로 기능을 이전하는 접근이었다.

이는 "두 번째 길"(Strangler Fig)의 극단적인 버전이다. 새로운 구조(모노레포)를 TS로 만들고, 기존 코드를 조금씩 이전한다. 기존 코드를 직접 바꾸는 대신 새로운 집을 먼저 짓고 이사하는 방식이다.

이 방법의 위험은 "새 집"이 완성되기 전에 두 코드베이스를 동시에 유지해야 한다는 것이다. 카카오처럼 팀 규모가 크고, 모노레포 전환 자체에 충분한 투자를 할 수 있을 때 유효한 선택이다. 소규모 팀이 이 방식을 따라 하다가 두 코드베이스를 동시에 유지하는 부담에 짓눌리는 경우도 있으니, 규모에 맞는 전략인지 먼저 따져봐야 한다.

`tsconfig.references`의 활용도 주목할 만하다. 모노레포의 각 패키지가 독립된 tsconfig를 가지고, 패키지 간 의존성을 `references`로 선언한다.

```json
// packages/api/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist"
  },
  "references": [
    { "path": "../shared" },
    { "path": "../types" }
  ]
}
```

이렇게 하면 IDE의 TS 언어 서버가 전체 코드베이스를 한꺼번에 분석하지 않고, 패키지 단위로 증분 분석한다. 수천 개의 파일이 있어도 IDE가 버텨내는 이유가 이것이다. `composite: true`는 `tsconfig.references`를 쓸 때 반드시 함께 켜야 하는 옵션이다. 이 옵션이 없으면 `references`를 선언해도 증분 빌드가 작동하지 않는다.

카카오 사례의 진짜 교훈은 "TS 마이그레이션"과 "코드 구조 개선"을 분리하지 않았다는 점이다. 어차피 구조를 바꿔야 했다면, 그 기회를 TS 전환과 묶어서 "한 번의 고통"으로 처리했다. 두 번 아프지 않으려는 선택이었다.

### 우아한형제들 — 점진적 strict 강화와 GraphQL TS 통합

우아한형제들(배달의민족)은 프론트엔드 TS 도입에서 독특한 접근을 택했다. (출처: techblog.woowahan.com, 실제 내용은 원문 참조 권장)

가장 특징적인 것은 단계적 strict 강화를 팀 OKR로 관리한 점이다. "이번 분기까지 `strictNullChecks` 켜기", "다음 분기까지 strict 오류 200개 이하로 줄이기"처럼, 마이그레이션 목표를 엔지니어링 OKR에 명시적으로 넣었다.

이렇게 했을 때의 장점은 경영진 가시성이다. 개발팀 내부의 기술 부채 해소가 아니라, 조직 전체가 인지하는 목표가 된다. 개발팀이 혼자 해결해야 하는 과제가 아니라, 팀이 함께 추진하는 방향이 된다. 마이그레이션이 중단되지 않는 구조적 이유를 만든 것이다.

"기술 부채를 갚는다"는 말은 너무 추상적이다. 경영진 입장에서는 당장 유저에게 보이지 않는 작업에 개발자 시간을 쓰는 게 납득하기 어렵다. 반면 "이번 분기 strict 오류 0개 달성"은 숫자다. 달성 여부를 확인할 수 있고, 달성하면 팀원 모두가 공유하는 성취가 된다. 마이그레이션을 지속 가능하게 만드는 조직적 기술이다.

또 하나는 GraphQL 코드 생성과의 결합이다. 우아한형제들은 GraphQL을 적극 사용하고, GraphQL 스키마에서 TS 타입을 자동 생성하는 파이프라인을 구축했다. API 응답 타입이 서버 스키마에서 자동으로 생성되므로, 프론트엔드 개발자가 직접 타입을 작성할 필요가 없다.

```graphql
# GraphQL 스키마
type User {
  id: ID!
  name: String!
  email: String
}
```

```typescript
// 자동 생성된 TS 타입 (graphql-code-generator)
export type User = {
  __typename?: 'User';
  id: string;
  name: string;
  email?: string | null;
};
```

이 접근은 "60% 한계"의 외부 데이터 경계 문제를 우회한다. 사람이 직접 API 응답 타입을 작성하는 대신, 스키마에서 자동 생성한다. 스키마가 단일 진실 공급원이 된다.

GraphQL을 쓰지 않는 팀이라면 OpenAPI(Swagger) 스펙에서 TS 타입을 생성하는 방법도 있다. `openapi-typescript` 같은 도구가 스펙 YAML/JSON을 읽어서 TS 타입을 자동으로 만들어준다.

```bash
npx openapi-typescript https://api.example.com/openapi.json -o src/types/api.ts
```

REST API를 쓰는 팀이라면 이 방법으로 "외부 데이터 경계의 40%"를 상당 부분 자동화할 수 있다. 서버가 OpenAPI 스펙을 정확하게 유지한다는 전제 아래서지만, 그 전제를 만족하면 프론트엔드 타입을 수동으로 유지할 필요가 없다.

---

## 세 사례에서 공통으로 배울 것

세 회사의 접근이 다 다르지만, 공통된 패턴이 있다.

**첫째, 인프라를 먼저 세웠다.** tsconfig, ESLint, CI 체크, 리뷰 기준. 파일을 바꾸기 전에 팀이 같은 기준으로 움직일 수 있는 토대를 만들었다. 기준 없이 시작한 마이그레이션은 팀원마다 다른 방향으로 나아가다가 흩어진다.

**둘째, `any`를 의도적으로 관리했다.** 방치하지 않았다. 추적하고, 기한을 정하고, 줄이는 방향을 유지했다. "나중에 고치자"가 습관이 되면 마이그레이션이 끝났다고 해도 `any`가 가득한 코드베이스가 남는다.

**셋째, 마이그레이션을 팀의 목표로 만들었다.** 개인의 선의가 아니라, 팀의 약속과 구조로 만들었다. 숫자로 표현할 수 있는 목표, 달성하면 모두가 아는 성취. 그래서 중단되지 않았다.

---

## 마이그레이션 로드맵 — 손에 잡히는 첫 달의 계획

다시 처음으로 돌아가자. PM이 "JS 코드베이스를 TS로 옮기는 태스크 맡겨도 될까요?"라고 했다.

이제 어떻게 대답하면 될까? 아래가 입사 첫 달의 현실적인 로드맵이다.

### 1주차: 현황 파악

```bash
# 파일 수 파악
find . -name "*.js" -not -path "*/node_modules/*" | wc -l
find . -name "*.ts" -not -path "*/node_modules/*" | wc -l

# any 현황 (이미 일부 TS가 있다면)
grep -r ": any" src/ | wc -l
grep -r "@ts-ignore" src/ | wc -l
```

코드베이스의 규모와 현재 TS 적용 수준을 숫자로 파악한다. 이 숫자가 PM에게 드릴 현황 보고의 기반이다.

기존 `tsconfig.json`이 있다면 어떤 strict 옵션이 켜져 있는지 확인한다. 아무것도 없다면 처음부터 세팅하는 기회다.

### 2주차: 인프라 세팅

팀과 합의해서 `tsconfig.json`을 만들거나 개선한다.

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "lib": ["ES2020"],
    "allowJs": true,
    "checkJs": false,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strict": false,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

`noImplicitAny`와 `strictNullChecks`는 처음부터 켜는 게 좋다. `strict: true`는 나중에. 지금 중요한 건 기준을 세우는 것이다.

`esModuleInterop: true`는 CommonJS 모듈을 default import로 가져올 수 있게 해준다. 이게 없으면 `import express from 'express'`가 오류가 나서 `import * as express from 'express'`로 써야 한다. 레거시 코드베이스에서는 이 옵션을 켜야 기존 import 패턴과 충돌이 없다.

`skipLibCheck: true`는 `node_modules` 안의 `.d.ts` 파일에서 오류가 나도 무시한다. `@types/*` 패키지끼리 충돌하거나, 오래된 타입 정의에 내부 불일치가 있을 때 컴파일을 막지 않도록 하는 옵션이다. 마이그레이션 초기에는 켜두는 편이 낫고, 안정화된 후에 끄면서 잠재적 타입 정의 충돌을 점검해볼 수 있다.

ESLint에 `@typescript-eslint` 룰셋을 추가한다.

```bash
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

```json
// .eslintrc.json
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

처음에 `no-explicit-any`를 `warn`으로 시작하는 게 좋다. `error`로 올리면 기존 코드를 전혀 손대지 않은 파일에서도 오류가 쏟아질 수 있다. 경고로 두고 점차 줄여나가다가, 어느 시점에 `error`로 승격하는 흐름이 자연스럽다.

CI에 `tsc --noEmit` 체크를 추가한다. PR이 타입 오류를 만들면 머지할 수 없게 한다.

### 3주차: 파일럿 전환

전체 코드베이스 중 가장 독립적이고 작은 모듈 하나를 골라 `.ts`로 전환한다. 유틸리티 함수 모음이나, 외부 의존성이 적은 헬퍼 파일이 좋다.

이 파일을 전환하면서 팀이 어떤 부분에서 막히는지, `@types/*`가 어떤 게 필요한지, 사내 모듈에 타입이 없으면 어떻게 처리할지를 경험으로 익힌다.

파일럿이 성공하면, 그 경험을 팀 내에 공유한다. 전환 가이드 문서를 만들면 더 좋다.

### 4주차: 로드맵 제시

파일럿 경험을 바탕으로 전체 로드맵을 PM에게 제시한다.

```
마이그레이션 로드맵 (초안)

1단계 (1~2개월): 인프라 완성
   - tsconfig, ESLint, CI 설정 완료
   - 핵심 유틸리티 모듈 전환 완료
   - @types/* 의존성 정리

2단계 (3~4개월): 신규 파일 100% TS
   - 모든 신규 파일은 .ts로 작성 (팀 약속)
   - noImplicitAny 오류 제로 유지

3단계 (5~8개월): 레거시 점진 전환
   - 변경이 생기는 파일은 그 PR에서 TS로 전환
   - 월 단위 any 카운트 추적

4단계 (9~12개월): strict 완성
   - strict: true 켜기
   - 전체 파일 .ts 전환 완료
```

12개월이라고 하면 PM이 놀랄 수 있다. 하지만 현실적인 숫자다. 3개월 만에 끝낸다고 약속하고 실패하는 것보다, 12개월 계획을 세우고 착실히 나아가는 게 낫다. 그리고 잘 설계된 마이그레이션은 6개월 만에 끝날 수도 있다.

---

## 마무리

점진적 마이그레이션은 한 번에 결판 나는 작업이 아니다. 체계를 세우고, 팀이 합의하고, 꾸준히 나아가는 과정이다.

가장 중요한 세 가지를 기억해두자.

**하나, 첫날부터 `noImplicitAny`는 켜라.** 나중에 켜기는 지금 켜기보다 열 배 힘들다.

**둘, `any`를 방치하지 말라.** 오늘의 `any` TODO가 6개월 후의 기술 부채다.

**셋, 마이그레이션은 팀의 목표여야 한다.** 혼자 하는 숙제가 아니라, 팀이 함께 추진하는 방향이 되어야 중단되지 않는다.

60%는 도구가 해준다. 나머지 40%는 사람이 해야 한다. 그 40%가 사실 당신 회사 코드베이스의 가장 중요한 핵심이다. 시간을 들여 제대로 타입을 정의할 가치가 있다.

---

다음 10장에서는 마이그레이션이 끝난 TS 코드로 무엇을 만들 수 있는지를 살펴본다. CLI 도구 — 명령줄에서 돌아가는 개발자 도구를 TypeScript로 처음부터 짜는 이야기다.

---

> **더 깊이 가려면**
>
> - **TypeScript Handbook — "Migrating from JavaScript"**: 공식 마이그레이션 가이드. `allowJs`/`checkJs` 설정의 레퍼런스.
> - **토스 테크 블로그 — "JavaScript에서 TypeScript로 바꾸기" 시리즈**: 한국어로 된 가장 실용적인 마이그레이션 후기. toss.tech에서 시리즈 검색.
> - **Kristensen & Møller (2017) — "TypeWright: Refactoring JavaScript to TypeScript"**: 자동 마이그레이션의 한계를 학술적으로 분석. ESEC/FSE 2017.
> - **ts-migrate GitHub**: Airbnb의 codemod 도구. `github.com/airbnb/ts-migrate`
> - **Matt Pocock — "Total TypeScript" Migration Guide**: 실전 중심의 마이그레이션 패턴. totaltypescript.com
> - **이펙티브 타입스크립트 (Dan Vanderkam, 인사이트 번역)**: 아이템 41~45가 마이그레이션 전략을 깊게 다룬다.

---

# 5부 — 응용

언어를 알고, 생태계를 이해하고, 마이그레이션 전략도 손에 쥐었다. 이제 TypeScript가 실제로 살아가는 영역들을 걷는다. CLI 도구, 데스크톱 앱, 웹 프론트엔드, 웹 백엔드, 풀스택, 테스트 — 각 영역이 TypeScript를 어떻게 쓰는지, Java/Kotlin 개발자가 그 영역에 처음 발을 디딜 때 무엇에 익숙하고 무엇이 낯선지를 정직하게 안내한다.

이 부에서 만나는 챕터:
- 10장. CLI를 짓는다 — 명령줄 도구로 TS의 첫 응용
- 11장. 데스크톱 앱 — Electron과 Tauri의 네이티브 경계
- 12장. 웹 프론트엔드 — React + TS의 핵심, 그리고 다른 reactivity 모델의 위치
- 13장. 웹 백엔드와 풀스택 — Express·Fastify·Hono·NestJS·Next·Astro의 여섯 길
- 14장. 테스트와 타입 — Vitest·expect-type·Playwright

---


> 9장에서 점진적 마이그레이션의 로드맵을 손에 넣었다. 이제 TypeScript가 실제로 어떤 모양으로 현장에 사는지를 살펴볼 차례다. 가장 진입 장벽이 낮고, 타입 시스템의 혜택이 즉각적으로 보이는 영역부터 시작하자 — CLI 도구. Java에서 picocli나 Spring Shell로 만들던 것을, TypeScript로 처음 짜면 어떤 모양이 되는가.

# 10장. CLI를 짓는다 — 명령줄 도구로 TS의 첫 응용

사내 DevOps 팀에서 어느 날 이런 요청이 온다고 상상해보자. "REST API 호출해서 배포 현황을 터미널에 보기 좋게 뿌려주는 도구 하나만 만들어줘요. 매번 curl이랑 jq 조합하기가 너무 번거롭거든요." Java 베테랑이라면 잠깐 고민할 것이다. Spring Shell을 쓸까? picocli를 붙일까? 그런데 이 도구를 TypeScript로 만들어야 한다면? 처음엔 찜찜하다. JS 진영에 터미널 도구 생태계가 제대로 갖춰져 있기는 한 건지, 타입은 제대로 흐르는지, 빌드하면 실행 파일이 나오기는 하는지.

결론부터 말하자면 — 갖춰져 있다. 생각보다 훨씬 정교하게. 그리고 Java에서 GraalVM native-image로 단일 바이너리를 뽑아본 경험이 있다면, Bun이 그것을 얼마나 더 간단하게 해내는지 보고 놀랄 수도 있다.

1장부터 9장까지는 언어와 타입 시스템을 해부했다. 10장부터는 그 언어가 *현장에서 어떤 모양으로 사는지*를 살펴본다. 첫 번째 현장은 CLI다. 가장 진입 장벽이 낮고, 타입 시스템의 혜택이 즉각적으로 보이며, 배포도 단순하다. CLI부터 시작하는 것은 자연스러운 선택이다.

---

## CLI 시장의 지형도

Java 진영에서 CLI 프레임워크를 고를 때는 선택지가 비교적 좁다. picocli는 GraalVM native-image와 잘 어울리고, Spring Shell은 Spring Boot 생태계와 묶여 있다. 선택의 무게가 무겁다.

JS/TS 진영은 다르다. 선택지가 많고, 각각이 다른 철학을 가진다. 가볍게 쓸 것인지, 체계적으로 구조화할 것인지, 엔터프라이즈급 확장성이 필요한지에 따라 세 가지 층위로 나뉜다.

### commander.js — 가장 가벼운 층

commander.js는 Express를 만든 TJ Holowaychuk의 작품이다. Express처럼 chain API를 기반으로 하고, 학습 곡선이 거의 없다.

```typescript
import { Command } from 'commander';

const program = new Command();

program
  .name('my-tool')
  .description('사내 배포 현황 조회 도구')
  .version('1.0.0');

program
  .command('status')
  .description('현재 배포 상태를 조회한다')
  .option('-e, --env <environment>', '환경 지정', 'production')
  .option('--json', 'JSON 형식으로 출력')
  .action(async (options) => {
    // options.env: string
    // options.json: boolean | undefined
    await showStatus(options.env, options.json ?? false);
  });

program.parse();
```

여기서 `options.env`와 `options.json`의 타입은 commander.js의 제네릭이 추론해준다. `--json` 플래그를 정의했으니 `boolean`, `--env <environment>`를 정의했으니 `string`. 5장에서 다룬 타입 좁히기가 이 맥락에서 제 역할을 한다.

commander.js의 장점은 단순함이다. Vercel CLI, Vue CLI 등 GitHub에서 다운로드 수 기준 상위권 CLI 도구 다수가 commander.js를 기반으로 한다. 기능이 필요 이상으로 많지 않고, 번들 크기가 작으며, 문서가 명확하다.

단점도 단순함에서 온다. 플러그인 시스템이 없고, 서브커맨드가 많아지면 파일을 어떻게 나눌지 스스로 설계해야 한다. 도구가 작을 때는 무결점이지만, 커질수록 번거롭다.

### yargs — 풍부한 기능의 층

yargs는 commander보다 기능이 훨씬 많다. 미들웨어, shell completion 자동 생성, i18n(다국어 지원), .yargs 설정 파일 로드까지 내장하고 있다.

```typescript
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

yargs(hideBin(process.argv))
  .command(
    'status <environment>',
    '배포 상태 조회',
    (yargs) => {
      return yargs
        .positional('environment', {
          describe: '대상 환경',
          type: 'string',
          choices: ['development', 'staging', 'production'] as const,
        })
        .option('json', {
          type: 'boolean',
          description: 'JSON 출력',
        });
    },
    async (argv) => {
      // argv.environment: "development" | "staging" | "production"
      // argv.json: boolean | undefined
      await showStatus(argv.environment, argv.json ?? false);
    }
  )
  .demandCommand(1)
  .parse();
```

`choices: ['development', 'staging', 'production'] as const`를 쓰면 `argv.environment`의 타입이 `string`이 아니라 `"development" | "staging" | "production"` 유니온으로 좁혀진다. 5장의 *타입을 만드는 타입*이 여기서 살아난다. 잘못된 값이 들어오면 yargs가 런타임에 잡아주고, 컴파일 타임에도 타입이 보장된다.

학습 곡선은 commander보다 가파르다. API가 풍부한 만큼 조합이 복잡해진다. 그리고 shell completion처럼 고급 기능은 직접 연결하는 설정이 필요해 처음에는 난감하게 느껴질 수 있다.

### oclif — 엔터프라이즈급 프레임워크 층

oclif는 Salesforce/Heroku가 만든 CLI 프레임워크다. Heroku CLI와 Salesforce CLI가 oclif 위에 올라가 있다. 프레임워크라는 이름이 어색하지 않다 — 규칙과 구조가 있다.

oclif에서는 커맨드 하나가 클래스 하나다.

```typescript
import { Command, Flags, Args } from '@oclif/core';

export default class StatusCommand extends Command {
  static description = '배포 상태를 조회한다';

  static args = {
    environment: Args.string({
      description: '대상 환경',
      required: true,
      options: ['development', 'staging', 'production'],
    }),
  };

  static flags = {
    json: Flags.boolean({
      char: 'j',
      description: 'JSON 형식으로 출력',
    }),
    timeout: Flags.integer({
      description: '타임아웃 (초)',
      default: 30,
    }),
  };

  async run(): Promise<void> {
    const { args, flags } = await this.parse(StatusCommand);
    // args.environment: string
    // flags.json: boolean
    // flags.timeout: number
    await showStatus(args.environment, flags.json, flags.timeout);
  }
}
```

클래스 기반이어서 Java 개발자에게 익숙하다. Spring의 `@Controller`처럼, 각 커맨드를 독립 클래스로 분리하고 oclif가 자동으로 라우팅한다.

플러그인 시스템이 특히 강력하다. 외부 패키지를 플러그인으로 설치하면 커맨드가 추가된다. Heroku CLI가 `heroku plugins:install`로 확장되는 방식이 이 모델이다. 자동 help 생성, 스냅샷 기반 테스트, 단일 실행 파일 빌드도 내장이다.

단점은 무게감이다. 작은 사내 도구에 oclif를 붙이면 과한 느낌이다. 프레임워크가 강제하는 파일 구조와 규칙이 있어, 기존 코드와 통합이 어색할 수 있다.

---

> **Java/Kotlin 시선 박스 ①: Spring Shell·picocli vs commander/oclif**
>
> | 기준 | Java 진영 | JS/TS 진영 |
> |------|-----------|-----------|
> | 가벼운 선택 | picocli (애노테이션 기반, GraalVM 친화) | commander.js (chain API, 번들 최소) |
> | 풍부한 기능 | Spring Shell (자동완성·REPL·Spring 통합) | yargs (미들웨어·completion·i18n) |
> | 엔터프라이즈 프레임워크 | Spring Shell + Spring Boot 풀스택 | oclif (클래스 기반·플러그인 시스템) |
> | 클래스 기반 커맨드 | picocli `@Command` 클래스 | oclif `Command` 상속 |
> | 타입 안전 인자 파싱 | picocli `@Option(type=...)` | commander/yargs/oclif 제네릭 추론 |
>
> 결정적 차이는 *생태계 결합도*다. Spring Shell은 Spring 컨텍스트를 올리고 시작하므로 JVM 워밍업이 필요하다. commander/oclif는 Node.js(또는 Bun)에서 바로 뜨고, 런타임 의존성이 훨씬 가볍다.

---

## 인자 파싱과 타입 — flag·positional·subcommand의 결

CLI 도구를 설계할 때 자주 만나는 질문이 있다. flag, positional 인자, subcommand — 이 셋을 어떻게 구분하고, 타입을 어떻게 좁힐 것인가.

### flag의 타입 좁히기

flag는 `--이름 값` 또는 `--이름` 형태다. commander와 yargs 모두 `string`, `boolean`, `number` 세 기본 타입을 지원한다.

```typescript
// commander.js 예시
program
  .option('--port <number>', '포트 번호', (v) => parseInt(v, 10), 3000)
  .option('--format <format>', '출력 형식')
  .option('--verbose', '상세 출력');

program.action((options) => {
  // options.port: number (parseInt로 변환)
  // options.format: string | undefined
  // options.verbose: boolean
});
```

`parseInt`를 명시적으로 파서로 넘기면 `options.port`가 `string`이 아니라 `number`로 좁혀진다. 이 패턴이 5장의 *타입 좁히기*와 맞물린다 — 파서 함수가 타입 변환의 게이트키퍼 역할을 한다.

### positional 인자의 타입

positional은 위치로 결정되는 인자다. `git commit -m "msg"`에서 `commit`이 subcommand고, `my-tool deploy production`에서 `production`이 positional이다.

```typescript
// yargs에서 positional의 choices로 유니온 타입 좁히기
yargs.command(
  'deploy <environment> [service]',
  '배포 실행',
  (yargs) =>
    yargs
      .positional('environment', {
        type: 'string',
        choices: ['dev', 'staging', 'prod'] as const,
        demandOption: true,
      })
      .positional('service', {
        type: 'string',
        // 선택적 — undefined 가능
      }),
  async (argv) => {
    // argv.environment: "dev" | "staging" | "prod"
    // argv.service: string | undefined
    const env = argv.environment; // 유니온 타입
    if (env === 'prod') {
      await confirmBeforeDeploy();
    }
    await deploy(env, argv.service);
  }
);
```

`as const`가 없으면 `argv.environment`는 `string`이다. `as const`를 붙이면 `"dev" | "staging" | "prod"`가 된다. `if (env === 'prod')` 분기가 타입적으로 의미 있어진다. 이 좁히기 패턴이 CLI 도구에서 반복적으로 쓰인다.

### subcommand 트리와 타입

subcommand가 중첩될 때 타입을 어떻게 유지할지는 조금 더 설계가 필요하다. commander에서는 `program.command('deploy').command('rollback')` 식으로 중첩한다. 이때 각 subcommand의 `action` 콜백이 독립적으로 타입을 가지므로, 타입 정보가 subcommand 경계에서 분리된다. 실수가 끼어들 틈이 줄어드는 구조다.

oclif에서는 커맨드 클래스 파일 구조가 subcommand를 결정한다. `src/commands/deploy/rollback.ts`를 만들면 자동으로 `my-tool deploy rollback` 커맨드가 된다. 파일 시스템이 곧 커맨드 트리다. 인식하기 쉬운 구조고, 새 팀원이 코드 구조만 보고도 커맨드 트리를 파악할 수 있다.

---

## 인터랙티브 입력 — prompt는 라이브러리로 해결한다

Java에서 사용자 입력을 받으려면 `Scanner`로 stdin을 읽거나, Spring Shell의 REPL 모드를 쓴다. 인터랙티브 UI(선택 메뉴, 비밀번호 입력, 체크박스)는 직접 ANSI 코드를 조합하거나 별도 라이브러리가 필요하다.

TS/JS 진영에서는 `inquirer`와 `prompts`가 이 역할을 한다.

### inquirer — 사실상 표준

```typescript
import inquirer from 'inquirer';

const answers = await inquirer.prompt([
  {
    type: 'list',
    name: 'environment',
    message: '배포 환경을 선택하세요:',
    choices: ['development', 'staging', 'production'],
  },
  {
    type: 'confirm',
    name: 'confirmed',
    message: '정말 배포하시겠습니까?',
    default: false,
    when: (answers) => answers.environment === 'production',
  },
  {
    type: 'password',
    name: 'token',
    message: 'API 토큰을 입력하세요:',
    mask: '*',
  },
]);

// answers.environment: string
// answers.confirmed: boolean | undefined
// answers.token: string
```

`when` 조건으로 이전 답변에 따라 질문을 동적으로 표시할 수 있다. `production`을 선택했을 때만 확인 질문을 보여주는 식이다. 실무에서 자주 쓰이는 패턴이다.

타입은 `answers` 객체에 flat하게 담긴다. inquirer v9부터는 TypeScript를 더 깊이 지원해 `prompt` 제네릭 타입 매개변수로 결과 타입을 명시할 수 있다. 하지만 질문 배열의 복잡성 때문에 타입 추론이 완전하지 않은 경우도 있다 — 이 부분은 여전히 개선 중이다.

### prompts — 가볍고 현대적인 대안

`prompts`는 inquirer보다 가볍고 API가 단순하다. 각 질문을 독립적으로 await하거나, 배열로 묶어 한 번에 실행할 수 있다.

```typescript
import prompts from 'prompts';

const { environment } = await prompts({
  type: 'select',
  name: 'environment',
  message: '환경을 선택하세요',
  choices: [
    { title: '개발', value: 'development' },
    { title: '스테이징', value: 'staging' },
    { title: '운영', value: 'production' },
  ],
});
```

Ctrl+C를 눌렀을 때의 동작 제어, 유효성 검사, 이전 답변 기반 동적 choices 등 실무에 필요한 기능을 갖추고 있다. CI 환경에서 stdin이 TTY가 아닐 때 자동으로 기본값을 사용하는 옵션도 있다.

그렇다면 둘 중 어느 것을 선택하면 좋을까? inquirer는 기능이 풍부하고 생태계가 크다. 오랫동안 널리 쓰여 왔고, 플러그인(fuzzy search, autocomplete)도 많다. prompts는 더 가볍고 번들 크기가 작다. 작은 도구를 빠르게 만들 때는 prompts, 복잡한 인터랙션이 필요하거나 기존 팀 코드베이스가 inquirer 기반이라면 inquirer가 자연스럽다.

---

## 출력의 미학 — 터미널을 아름답게

CLI 도구의 첫인상은 출력이다. 텍스트를 그냥 `console.log`로 찍으면 기능은 되지만, 사용자가 읽기 불편하다. TS 진영에는 출력을 풍부하게 만드는 도구들이 잘 갖춰져 있다.

### chalk — 색상과 스타일

```typescript
import chalk from 'chalk';

console.log(chalk.green('✓ 배포 성공'));
console.log(chalk.red.bold('✗ 오류 발생'));
console.log(chalk.yellow('⚠ 경고: 스테이징 환경입니다'));
console.log(chalk.blue.underline('https://example.com/deploy/123'));

// 조건부 색상
const status = isSuccess ? chalk.green('성공') : chalk.red('실패');
console.log(`배포 상태: ${status}`);
```

chalk는 터미널이 색상을 지원하는지 자동 감지한다. CI 환경이나 파이프로 출력을 넘길 때는 자동으로 색상 코드를 제거한다. 사용자가 `NO_COLOR` 환경 변수를 설정했을 때도 존중한다.

### ora — 스피너와 진행 표시

비동기 작업이 긴 경우 사용자는 기다리면서 불안하다. 아무 피드백이 없으면 "멈춘 건가?"라고 느낀다.

```typescript
import ora from 'ora';

const spinner = ora('배포 중...').start();

try {
  await deployService();
  spinner.succeed('배포가 완료되었습니다');
} catch (error) {
  spinner.fail('배포에 실패했습니다');
  throw error;
}
```

`spinner.succeed()`는 스피너를 체크마크로 바꾸고, `spinner.fail()`은 X 마크로 바꾼다. `spinner.warn()`은 경고 아이콘이다. 각각 자동으로 색상도 적용된다.

### cli-table3 — 표 형식 출력

REST API 응답처럼 구조화된 데이터를 보여줄 때 표가 훨씬 읽기 쉽다.

```typescript
import Table from 'cli-table3';

const table = new Table({
  head: ['서비스', '버전', '상태', '마지막 배포'],
  colWidths: [20, 10, 10, 25],
  style: {
    head: ['cyan'],
    border: ['grey'],
  },
});

deployments.forEach((d) => {
  table.push([
    d.service,
    d.version,
    d.status === 'healthy' ? chalk.green(d.status) : chalk.red(d.status),
    d.deployedAt,
  ]);
});

console.log(table.toString());
```

chalk와 조합해서 셀 안에 색상을 넣을 수 있다. 헤더 색상, 테두리 스타일도 설정 가능하다.

### boxen — 강조 박스

중요한 메시지를 눈에 띄게 강조할 때 사용한다.

```typescript
import boxen from 'boxen';

console.log(
  boxen(
    `${chalk.green.bold('배포 성공!')}\n\n` +
      `환경: ${chalk.cyan('production')}\n` +
      `버전: ${chalk.cyan('v2.4.1')}\n` +
      `URL: ${chalk.blue.underline('https://app.example.com')}`,
    {
      padding: 1,
      margin: 1,
      borderStyle: 'round',
      borderColor: 'green',
    }
  )
);
```

배포 완료 후 최종 결과를 박스로 감싸면 긴 로그 속에서도 눈에 바로 들어온다.

---

## 단일 실행 파일 빌드 — Java 베테랑이 흥미로워할 자리

사내 CLI 도구를 만들었다. 이제 배포가 문제다. Node.js가 설치된 환경이라면 `npx`로 바로 쓸 수 있지만, 그렇지 않은 환경이라면? 또는 실행 속도가 중요한 자동화 파이프라인에 쓸 도구라면? Java 베테랑이라면 GraalVM native-image를 떠올릴 것이다. TS 진영에는 그에 상응하는 도구가 있다.

### pkg와 nexe — 역사적 접근

초기에는 `pkg`(Vercel)와 `nexe`가 이 역할을 했다. 아이디어는 단순하다. Node.js 실행 파일과 애플리케이션 코드를 하나의 바이너리로 묶는다.

```bash
# pkg 사용 예
npx pkg my-cli.js --targets node18-linux-x64,node18-macos-x64,node18-win-x64
```

결과로 Linux, macOS, Windows 각각에서 실행 가능한 바이너리가 생성된다. Node.js 없이도 실행된다. 아이디어는 맞지만, 생성 바이너리가 수십~수백 MB에 달한다. Node.js 런타임 전체를 품기 때문이다. 배포하기 번거롭고, 시작 시간도 빠르지 않다. 2024년 기준 pkg는 사실상 유지보수가 멈춘 상태다.

### Bun compile — 현재의 선택

Bun은 `bun build --compile`로 TypeScript 소스를 단일 실행 파일로 만든다. 크로스 컴파일도 지원한다.

```bash
# 현재 플랫폼용 바이너리 빌드
bun build --compile ./src/cli.ts --outfile my-tool

# 크로스 컴파일 — macOS에서 Linux 바이너리 빌드
bun build --compile --target=bun-linux-x64 ./src/cli.ts --outfile my-tool-linux
```

결과 바이너리는 Bun 런타임과 앱 코드를 함께 담지만, Bun 자체가 Zig로 작성된 매우 효율적인 런타임이라 바이너리 크기가 pkg 대비 훨씬 작다. 그리고 시작 시간이 빠르다 — 이 부분이 Java 베테랑이 놀라는 지점이다.

### Deno compile

Deno도 `deno compile`로 단일 실행 파일을 지원한다.

```bash
# Deno 컴파일
deno compile --allow-net --allow-env ./src/cli.ts -o my-tool

# 크로스 컴파일
deno compile --target x86_64-unknown-linux-gnu ./src/cli.ts -o my-tool-linux
```

Deno의 강점은 보안 모델이다. `--allow-net`, `--allow-env`처럼 권한을 명시적으로 선언한다. 컴파일된 바이너리도 이 권한 제약을 그대로 유지한다. 배포 후 "이 CLI가 네트워크에 무언가를 전송하지 않을까?"라는 찜찜함을 줄여준다.

---

> **Java/Kotlin 시선 박스 ②: GraalVM native-image vs Bun/Deno compile**
>
> Java 베테랑이 가장 흥미로워할 비교다. GraalVM native-image와 Bun/Deno compile은 *비슷한 목적*을 *다른 방식*으로 해결한다.
>
> | 기준 | GraalVM native-image | Bun `--compile` | Deno `compile` |
> |------|---------------------|-----------------|----------------|
> | **빌드 시간** | 수 분 (AOT 분석) | 수 초 | 수 초 |
> | **시작 시간** | 수 ms (JVM 없음) | ~10ms 내외 | ~15ms 내외 |
> | **바이너리 크기** | 10~30 MB (일반 CLI) | 40~80 MB | 60~100 MB |
> | **플랫폼 지원** | Linux/macOS/Windows (크로스 컴파일은 복잡) | Linux/macOS/Windows (크로스 컴파일 내장) | Linux/macOS/Windows (크로스 컴파일 내장) |
> | **런타임 의존성** | 없음 (완전 정적) | 없음 | 없음 |
> | **리플렉션 제한** | 있음 — 설정 파일 필요 | 없음 | 없음 |
> | **동적 클래스 로딩** | 제한적 | 해당 없음 (JS 모델) | 해당 없음 |
> | **빌드 복잡도** | 높음 (Graal 설치, reflect config) | 낮음 (명령 한 줄) | 낮음 (명령 한 줄) |
>
> GraalVM native-image의 장점은 JVM 생태계 자산을 그대로 가져온다는 것이다. 기존 Java/Kotlin 라이브러리를 그대로 쓸 수 있다. 단점은 리플렉션과 동적 클래스 로딩에 제약이 있어, Spring 같은 복잡한 프레임워크를 native-image로 굽는 것이 생각보다 험하다. 설정 파일을 손으로 튜닝해야 하는 순간이 찾아온다.
>
> Bun/Deno compile은 빌드가 단순하다. 명령 한 줄이다. JS/TS의 동적 특성이 리플렉션 같은 AOT 분석 문제를 거의 만들지 않는다. 바이너리 크기는 GraalVM보다 크지만, 시작 시간은 둘 다 충분히 빠르다. CLI 도구 수준에서 시작 시간 10ms vs 50ms는 체감하기 어렵다.
>
> picocli + GraalVM native-image 조합을 써봤다면 알겠지만, reflect-config.json 씨름이 만만치 않다. Bun compile은 그 씨름이 없다. Java 베테랑이 처음 `bun build --compile`을 써보면 "이렇게 쉬운 거야?"라고 느끼는 경우가 많다.

---

## 인자 파싱의 타입 심화 — 5장이 CLI에서 살아나는 방식

5장에서 다룬 *타입을 만드는 타입* — mapped type, conditional type, `infer` — 이 CLI 인자 파싱에서 어떻게 실제로 쓰이는지 살펴보자.

### 커맨드 옵션을 타입으로 모델링하기

CLI 도구가 커지면 옵션 정의와 사용 코드가 분산된다. 옵션을 한 곳에서 정의하고 타입을 재사용하는 패턴이 유용하다.

```typescript
// 옵션 스키마를 별도 타입으로 정의
interface DeployOptions {
  environment: 'development' | 'staging' | 'production';
  service?: string;
  dryRun: boolean;
  timeout: number;
}

// commander에서 파싱 후 타입 단언 (책임 있는 사용)
function parseDeployOptions(options: Record<string, unknown>): DeployOptions {
  const env = options.environment;
  if (env !== 'development' && env !== 'staging' && env !== 'production') {
    throw new Error(`잘못된 환경: ${env}`);
  }
  return {
    environment: env,
    service: typeof options.service === 'string' ? options.service : undefined,
    dryRun: options.dryRun === true,
    timeout: typeof options.timeout === 'number' ? options.timeout : 30,
  };
}
```

5장의 타입 가드 패턴이 여기서 역할을 한다. `options.environment`가 세 가지 값 중 하나인지 런타임에 검증하면서 동시에 타입도 좁힌다.

### zod로 CLI 인자 검증하기

더 체계적인 접근은 zod 스키마로 인자를 검증하는 것이다.

```typescript
import { z } from 'zod';

const DeployOptionsSchema = z.object({
  environment: z.enum(['development', 'staging', 'production']),
  service: z.string().optional(),
  dryRun: z.boolean().default(false),
  timeout: z.number().int().positive().default(30),
});

type DeployOptions = z.infer<typeof DeployOptionsSchema>;
// { environment: "development" | "staging" | "production";
//   service?: string;
//   dryRun: boolean;
//   timeout: number; }
```

`z.infer`로 스키마에서 타입을 추출하면 타입과 검증이 항상 동기화된다. 스키마를 바꾸면 타입도 자동으로 바뀐다. 5장에서 말한 *타입의 단일 출처(single source of truth)*가 이 패턴이다.

commander 파싱 결과를 zod로 검증하는 흐름은 다음과 같다.

```typescript
program
  .command('deploy')
  .option('-e, --environment <env>', '배포 환경')
  .option('-s, --service <service>', '서비스 이름')
  .option('--dry-run', '실제 배포 없이 계획만 출력')
  .option('--timeout <seconds>', '타임아웃', '30')
  .action(async (rawOptions) => {
    // zod로 파싱 + 검증 + 기본값 적용
    const options = DeployOptionsSchema.parse({
      ...rawOptions,
      timeout: rawOptions.timeout ? parseInt(rawOptions.timeout, 10) : 30,
    });
    // options는 DeployOptions 타입으로 안전하게 좁혀짐
    await runDeploy(options);
  });
```

`DeployOptionsSchema.parse()`가 실패하면 `ZodError`가 던져지고, commander가 이를 잡아 오류 메시지를 출력한다. 컴파일 타임과 런타임, 두 겹의 보호막이다.

---

## 출력 심화 — 구조화된 데이터를 어떻게 표현할 것인가

CLI 도구가 REST API를 호출하고 결과를 보여줄 때, 데이터를 어떻게 표현할지가 사용자 경험의 핵심이다. 기본 텍스트 출력, JSON, 표 형식 중 어느 것이 적절한지는 사용 맥락에 따라 다르다.

### 기계가 읽는 출력 vs 사람이 읽는 출력

CLI 도구를 설계할 때 중요한 원칙 하나는 *기계 출력과 사람 출력을 분리하는 것*이다. 파이프라인에서 쓰이는 도구라면 JSON을 stdout으로, 메시지는 stderr로 내보내야 한다.

```typescript
const isJsonMode = process.env.CI === 'true' || options.json;
const isTTY = process.stdout.isTTY;

if (isJsonMode || !isTTY) {
  // 기계가 읽는 출력 — JSON, 색상 없음
  console.log(JSON.stringify(result, null, 2));
} else {
  // 사람이 읽는 출력 — 색상, 표, 스피너
  const table = formatAsTable(result);
  console.log(table);
}
```

`process.stdout.isTTY`는 출력이 터미널로 가는지(true) 파이프로 가는지(false)를 알려준다. chalk는 이를 자동으로 감지하지만, 표나 스피너 같은 복잡한 출력은 수동으로 분기해야 한다.

### 진행 상황 표시 패턴

여러 서비스를 순차적으로 배포할 때 전체 진행 상황을 보여주는 패턴이다.

```typescript
import ora from 'ora';
import chalk from 'chalk';

async function deployAll(services: string[]): Promise<void> {
  const results: Array<{ service: string; success: boolean; message: string }> = [];

  for (const service of services) {
    const spinner = ora(`배포 중: ${chalk.cyan(service)}`).start();
    try {
      await deployService(service);
      spinner.succeed(`${chalk.cyan(service)} 배포 완료`);
      results.push({ service, success: true, message: '완료' });
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류';
      spinner.fail(`${chalk.cyan(service)} 배포 실패: ${message}`);
      results.push({ service, success: false, message });
    }
  }

  // 최종 요약
  const succeeded = results.filter((r) => r.success).length;
  const failed = results.length - succeeded;
  console.log(
    boxen(
      `완료: ${chalk.green(succeeded)}개 성공, ${chalk.red(failed)}개 실패`,
      { padding: 1, borderStyle: 'round' }
    )
  );
}
```

스피너가 하나씩 완료되거나 실패로 바뀌면서 전체 흐름이 눈에 보인다. 실패한 서비스만 다시 실행하는 `--retry-failed` 플래그를 추가하는 것도 자연스러운 확장이다.

---

## 배포 — npm publish, Homebrew, GitHub Releases

CLI 도구를 만들었으면 배포해야 한다. Java 진영에서는 JAR를 넘기거나 Homebrew formula를 작성하거나 Docker 이미지로 배포한다. TS CLI의 배포 경로는 더 다양하다.

### npm publish — 가장 기본적인 경로

npm 레지스트리에 배포하면 `npx`로 바로 쓸 수 있다. Node.js가 설치된 환경이라면 추가 설치 없이 사용할 수 있다는 장점이 크다.

`package.json`에 몇 가지를 설정해야 한다.

```json
{
  "name": "my-deploy-tool",
  "version": "1.0.0",
  "bin": {
    "my-tool": "./dist/cli.js"
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  }
}
```

`bin` 필드가 커맨드 이름과 실행 파일을 연결한다. `npm install -g my-deploy-tool`을 하면 `my-tool` 커맨드로 쓸 수 있다. `npx my-deploy-tool`은 설치 없이 직접 실행한다.

TS 소스가 `src/cli.ts`에 있다면, 빌드 결과인 `dist/cli.js`가 배포된다. TS 소스 자체를 배포하는 경우(`ts-node`로 실행하거나 Bun이 직접 실행하는 방식)도 있지만, 이 경우 소비자 환경에 `ts-node`나 Bun이 설치되어 있어야 해 불편하다.

### 단일 바이너리 배포 — GitHub Releases

Bun이나 Deno로 컴파일한 단일 바이너리는 Node.js 설치 없이 실행된다. GitHub Actions으로 크로스 컴파일해 GitHub Releases에 올리는 패턴이 일반적이다.

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: bun-linux-x64
            artifact: my-tool-linux-x64
          - os: macos-latest
            target: bun-darwin-arm64
            artifact: my-tool-macos-arm64
          - os: windows-latest
            target: bun-windows-x64
            artifact: my-tool-windows-x64.exe

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun build --compile --target=${{ matrix.target }} src/cli.ts --outfile ${{ matrix.artifact }}
      - uses: softprops/action-gh-release@v1
        with:
          files: ${{ matrix.artifact }}
```

이 워크플로로 태그를 푸시하면 Linux, macOS(ARM), Windows 바이너리가 자동으로 GitHub Release에 첨부된다. 사용자는 플랫폼에 맞는 바이너리를 다운받아 바로 실행한다.

### Homebrew formula

macOS 사용자를 위한 Homebrew tap을 만들면 `brew install`로 설치하게 할 수 있다.

```ruby
# Formula/my-tool.rb
class MyTool < Formula
  desc "사내 배포 현황 조회 도구"
  homepage "https://github.com/myorg/my-tool"
  version "1.0.0"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/myorg/my-tool/releases/download/v1.0.0/my-tool-macos-arm64"
      sha256 "..." # 빌드 시 계산한 sha256
    else
      url "https://github.com/myorg/my-tool/releases/download/v1.0.0/my-tool-macos-x64"
      sha256 "..."
    end
  end

  def install
    bin.install Dir["my-tool*"].first => "my-tool"
  end
end
```

Homebrew는 macOS 개발자에게 익숙한 설치 방법이다. Java CLI 도구를 Homebrew로 배포해본 경험이 있다면 동일한 과정이다.

---

## 라이브러리 선택 가이드 — 어느 조합이 좋을까

지금까지 각 라이브러리를 살펴봤다. 실제 프로젝트에서 어느 조합을 선택할지에 대한 판단 기준을 정리해보자.

### 도구 크기에 따른 선택

작은 사내 도구(5개 미만 커맨드, 팀 내부 배포)라면 commander.js + chalk + ora 조합이 충분하다. 오버엔지니어링 없이 빠르게 만들 수 있다. zod로 인자를 검증하면 타입 안전성도 확보된다.

중간 규모의 도구(10개 내외 커맨드, 조직 내 배포)라면 yargs를 고려할 만하다. shell completion 자동 생성이 유용하고, 미들웨어로 공통 로직(인증 토큰 로드, 로깅)을 처리할 수 있다.

엔터프라이즈 수준의 CLI(여러 팀이 플러그인으로 확장, 외부 배포)라면 oclif가 맞다. Heroku CLI 수준의 확장성이 필요할 때다. 처음에는 번거롭게 느껴지지만, 팀이 여럿이 되고 플러그인이 늘어나면 oclif의 구조가 빛을 발한다.

### 배포 목적에 따른 선택

Node.js가 있는 개발자 환경에서만 쓰이는 도구라면 npm publish로 충분하다. `npx`가 편하다.

Node.js가 없는 환경이거나, 시작 시간이 중요하거나, 최종 사용자가 Node.js를 모르는 경우라면 Bun compile로 단일 바이너리를 만드는 편이 낫다.

보안이 특별히 중요한 도구 — 예를 들어 프로덕션 환경에 접근하는 배포 도구 — 라면 Deno compile과 Deno의 권한 모델이 안전망을 하나 더 제공한다.

### 인터랙션 수준에 따른 선택

인터랙션이 거의 없는 자동화 도구라면 prompts/inquirer 없이 flag만으로 설계하는 편이 낫다. CI/CD 파이프라인에서 쓰일 도구에 interactive prompt를 넣으면 난감하다.

인터랙션이 있더라도 간단한 경우(환경 선택, 확인 메시지)는 prompts로 충분하다. 복잡한 위자드 형식의 인터랙션이 필요하다면 inquirer의 풍부한 타입과 플러그인을 활용하자.

---

## CLI 프로젝트 구조와 TypeScript 설정

Java 프로젝트는 Maven/Gradle의 표준 디렉터리 구조가 있다. `src/main/java`, `src/test/java` — 어느 프로젝트를 열어도 같은 구조다. TS CLI 프로젝트는 관례가 덜 강제되어 있어, 처음에는 어떻게 파일을 배치할지 난감하다.

사실 크게 고민할 필요 없다. commander 기반의 소~중형 프로젝트라면 아래 구조가 잘 작동한다.

```
my-tool/
├── src/
│   ├── cli.ts          # 진입점 — program 정의, 커맨드 등록
│   ├── commands/
│   │   ├── status.ts   # status 커맨드 로직
│   │   ├── deploy.ts   # deploy 커맨드 로직
│   │   └── rollback.ts # rollback 커맨드 로직
│   ├── lib/
│   │   ├── api.ts      # API 클라이언트
│   │   ├── config.ts   # 설정 로드/저장
│   │   └── output.ts   # 출력 유틸리티 (chalk, ora, table)
│   └── types/
│       └── index.ts    # 공유 타입 정의
├── dist/               # 컴파일 결과 (gitignore)
├── tsconfig.json
├── package.json
└── README.md
```

`src/cli.ts`는 얇게 유지하는 편이 낫다. 커맨드를 등록하고 `program.parse()`를 호출하는 역할만 한다. 실제 로직은 `src/commands/` 아래로 분리한다.

### tsconfig.json 설정

CLI용 `tsconfig.json`은 라이브러리나 프론트엔드와 조금 다르다.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

`"module": "NodeNext"`와 `"moduleResolution": "NodeNext"`가 중요하다. Node.js 18 이상의 ESM 환경을 타깃으로 한다면 이 설정이 맞다. CommonJS를 유지해야 한다면 `"module": "CommonJS"`, `"moduleResolution": "Node"`로 설정한다.

`declaration: true`는 라이브러리로 배포할 때 필요하다. 사내 도구라면 생략해도 되지만, 타입 정의 파일이 있으면 도구 사용자가 IDE에서 타입 힌트를 받을 수 있어 유용하다.

### package.json의 bin 필드와 실행 방식

CLI 진입점 파일(`dist/cli.js`)에는 shebang 줄이 필요하다.

```typescript
// src/cli.ts 맨 윗줄
#!/usr/bin/env node

import { Command } from 'commander';
// ...
```

TS 소스의 shebang은 tsc가 그대로 복사해 `dist/cli.js`에 남긴다. `chmod +x dist/cli.js`로 실행 권한을 주거나, `package.json`의 `postbuild` 스크립트에서 처리한다.

```json
{
  "scripts": {
    "build": "tsc",
    "postbuild": "chmod +x dist/cli.js",
    "dev": "ts-node src/cli.ts",
    "dev:bun": "bun run src/cli.ts"
  }
}
```

개발 중에는 `ts-node src/cli.ts` 또는 `bun run src/cli.ts`로 바로 실행한다. 빌드 없이 TS를 직접 실행하는 것이 개발 루프를 빠르게 한다. Bun은 별도 설정 없이 TS를 실행하므로 개발 편의성이 특히 좋다.

---

## 에러 처리와 종료 코드 — 자동화 파이프라인의 약속

Java에서 프로세스 종료 코드는 `System.exit(code)`로 명시한다. CLI 도구가 성공하면 0, 실패하면 0이 아닌 값을 반환하는 것이 Unix 관례다. 이 관례를 지키지 않으면 CI/CD 파이프라인이 오류를 감지하지 못한다. 번거로운 문제가 된다.

Node.js/Bun에서는 `process.exit(code)`로 동일하게 처리한다.

```typescript
// 전역 에러 핸들러
process.on('uncaughtException', (error) => {
  console.error(chalk.red('예상치 못한 오류가 발생했습니다:'), error.message);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  console.error(chalk.red('처리되지 않은 Promise 거부:'), reason);
  process.exit(1);
});
```

commander는 `.exitOverride()`로 `process.exit()` 호출을 가로챌 수 있다. 테스트에서 유용한 패턴이다.

### 커스텀 에러 클래스

CLI 도구에서 자주 쓰는 패턴은 사용자에게 보여줄 오류와 내부 오류를 분리하는 것이다.

```typescript
// 사용자에게 보여주는 오류 — 스택 트레이스 없이
export class UserFacingError extends Error {
  constructor(
    message: string,
    public readonly exitCode: number = 1
  ) {
    super(message);
    this.name = 'UserFacingError';
  }
}

// API 오류 — 자세한 메시지 포함
export class ApiError extends UserFacingError {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly responseBody?: unknown
  ) {
    super(`API 오류 (${statusCode}): ${message}`, 1);
    this.name = 'ApiError';
  }
}
```

진입점에서 이를 처리한다.

```typescript
async function main(): Promise<void> {
  try {
    await program.parseAsync(process.argv);
  } catch (error) {
    if (error instanceof UserFacingError) {
      console.error(chalk.red(`오류: ${error.message}`));
      process.exit(error.exitCode);
    }
    // 예상치 못한 오류는 스택 트레이스와 함께
    console.error(chalk.red('내부 오류가 발생했습니다:'));
    console.error(error);
    process.exit(1);
  }
}

main();
```

`UserFacingError`는 스택 트레이스 없이 깔끔한 메시지만 보여준다. `ApiError`는 HTTP 상태 코드를 품어 로깅이나 디버깅에 쓴다. 이 패턴이 Java의 checked exception vs unchecked exception 구분과 비슷한 역할을 한다 — 사용자가 직접 처리해야 하는 오류와 프로그램 버그로 인한 오류를 분리한다.

### 종료 코드 관례

Unix CLI의 관례적인 종료 코드는 다음과 같다.

| 종료 코드 | 의미 |
|---------|------|
| 0 | 성공 |
| 1 | 일반 오류 |
| 2 | 잘못된 인자 사용 |
| 126 | 명령을 실행할 수 없음 |
| 127 | 명령을 찾을 수 없음 |
| 130 | Ctrl+C로 중단 (128 + SIGINT) |

도구마다 커스텀 코드를 정의하는 경우도 있다. 예를 들어 배포 검사 도구라면 "취약점 발견" 종료 코드를 별도로 정의해 파이프라인이 이를 구분할 수 있게 한다.

---

## CLI 도구 테스트 — 어떻게 테스트할 것인가

Java에서 picocli나 Spring Shell을 테스트하는 방식은 잘 정립되어 있다. TS CLI 테스트는 어떻게 할까?

### 커맨드 로직의 단위 테스트

가장 중요한 원칙은 *커맨드 로직을 순수 함수로 분리하는 것*이다. commander의 `action` 콜백 안에 모든 로직을 넣으면 테스트하기 난감하다.

```typescript
// commands/status.ts — 로직을 함수로 분리
export async function fetchDeploymentStatus(
  environment: string,
  apiToken: string
): Promise<DeploymentStatus[]> {
  const response = await fetch(`https://api.example.com/deployments?env=${environment}`, {
    headers: { Authorization: `Bearer ${apiToken}` },
  });
  if (!response.ok) {
    throw new ApiError('배포 상태 조회 실패', response.status);
  }
  return response.json() as Promise<DeploymentStatus[]>;
}

export function formatStatusTable(statuses: DeploymentStatus[]): string {
  const table = new Table({ head: ['서비스', '버전', '상태'] });
  statuses.forEach((s) => table.push([s.service, s.version, s.status]));
  return table.toString();
}

// cli.ts에서는 얇게 연결만
program
  .command('status')
  .option('-e, --env <env>', '환경', 'production')
  .action(async (options) => {
    const token = process.env.API_TOKEN ?? '';
    const statuses = await fetchDeploymentStatus(options.env, token);
    console.log(formatStatusTable(statuses));
  });
```

이렇게 분리하면 `fetchDeploymentStatus`와 `formatStatusTable`을 독립적으로 테스트할 수 있다.

```typescript
// commands/status.test.ts (Vitest 사용)
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchDeploymentStatus, formatStatusTable } from './status';

describe('fetchDeploymentStatus', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('성공 응답을 파싱한다', async () => {
    const mockData = [
      { service: 'api', version: 'v1.2.3', status: 'healthy' },
    ];
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockData,
    }));

    const result = await fetchDeploymentStatus('production', 'test-token');
    expect(result).toEqual(mockData);
  });

  it('API 오류 시 ApiError를 던진다', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
    }));

    await expect(fetchDeploymentStatus('production', 'invalid')).rejects.toThrow('API 오류');
  });
});
```

### E2E 테스트 — 실제 CLI 실행 검증

커맨드 로직 단위 테스트 외에, 실제 CLI 바이너리를 실행해 통합 테스트를 하는 방법도 있다.

```typescript
// test/e2e/cli.test.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

describe('CLI E2E', () => {
  it('--help 플래그가 올바르게 출력된다', async () => {
    const { stdout } = await execAsync('node dist/cli.js --help');
    expect(stdout).toContain('사내 배포 현황 조회 도구');
    expect(stdout).toContain('status');
    expect(stdout).toContain('deploy');
  });

  it('잘못된 환경 인자로 종료 코드 1을 반환한다', async () => {
    await expect(
      execAsync('node dist/cli.js status --env invalid-env')
    ).rejects.toMatchObject({
      code: 1,
    });
  });
});
```

E2E 테스트는 빌드 후 실행해야 해서 느리지만, commander/yargs의 파싱 로직 자체에서 오는 문제를 잡아낸다. CI에서는 단위 테스트 후 빌드하고, 빌드 후 E2E를 실행하는 순서가 자연스럽다.

---

## 타입이 CLI에서 흐르는 방식 — 종합

1장부터 9장에서 배운 타입 시스템이 CLI 도구에서 실제로 쓰이는 패턴을 정리해보자.

**1장의 점진적 타입 도입**이 CLI에서는 이렇게 나타난다. `any`로 시작한 options 객체를 점차 구체적 타입으로 좁혀간다. 처음에는 `commander`가 주는 그대로 쓰다가, 검증이 필요해지면 zod 스키마를 붙이는 흐름이다.

**5장의 유니온 타입과 타입 좁히기**가 CLI에서는 `choices`와 타입 가드로 나타난다. `environment: 'development' | 'staging' | 'production'`을 선언하면 이후 코드에서 잘못된 환경에 접근하는 버그를 컴파일 타임에 잡는다.

**5장의 `z.infer`와 mapped type**이 CLI에서는 스키마에서 타입을 추출하는 패턴으로 나타난다. 스키마 정의 하나로 검증과 타입 두 역할을 동시에 한다.

**7장의 에러 처리 패턴**이 CLI에서는 `try/catch` + spinner fail 패턴으로 나타난다. `error instanceof Error`로 타입을 좁히고, 의미 있는 오류 메시지를 사용자에게 보여준다.

이 맥락에서 CLI는 TypeScript 타입 시스템의 *응용 교실*이다. 실제 사용자가 있고, 실제 오류가 있으며, 타입이 버그를 막는 효과가 직접 보인다.

---

## TS CLI의 현장 — 실제 채택 사례

어떤 팀이 실제로 TS로 CLI를 만들고 있는지 살펴보면 지형도가 보다 선명해진다.

Vercel CLI는 Node.js + TS 기반이다. 수백만 명이 매일 쓰는 도구를 commander.js와 유사한 접근으로 만들었다. 복잡한 서브커맨드 트리와 인터랙티브 프롬프트를 함께 갖추고 있다.

Heroku CLI와 Salesforce CLI는 oclif의 레퍼런스 구현이다. Salesforce는 외부 개발자가 플러그인을 만들 수 있는 생태계를 oclif로 구축했다. 플러그인이 수백 개에 달한다.

Vue CLI, Create React App — 프론트엔드 프로젝트 초기화 도구들이 모두 Node.js + TS 기반이다. Vite의 `create-vite`는 Bun으로 직접 실행도 된다.

GitHub CLI는 Go로 만들어졌지만, npm 생태계 CLI 도구의 다수가 commander.js를 쓴다. 이 사실이 commander의 생태계 지배력을 보여준다.

사내 도구 수준에서는 어떨까? 배포 파이프라인을 제어하는 CLI, 인프라 관리 스크립트, 데이터 마이그레이션 도구 — 이런 것들이 Java 팀에서도 점차 TS로 만들어지고 있다. Node.js나 Bun이 설치된 개발 환경에서 `npx`로 바로 실행할 수 있다는 편의성, 그리고 프론트엔드 코드와 타입 정의를 공유할 수 있다는 이점이 크다.

---

## 결정 지점 — 어떤 라이브러리로 짤 것인가

지금쯤 자기 사내 도구를 어떤 라이브러리로 만들지 결정할 수 있어야 한다. 판단 기준을 한 번 더 정리해보자.

**commander.js를 고르는 시나리오:** 처음 TS CLI를 만들어보는 경우. 커맨드 수가 적고 팀 내부에서만 쓰는 경우. 번들 크기와 빌드 복잡도를 최소화하고 싶은 경우.

**yargs를 고르는 시나리오:** shell completion이 필요한 경우. 미들웨어로 공통 로직을 처리해야 하는 경우. 다국어 지원이 필요한 경우.

**oclif를 고르는 시나리오:** 여러 팀이 플러그인으로 커맨드를 추가해야 하는 경우. Heroku CLI 수준의 확장성이 목표인 경우. 팀이 크고 커맨드 수가 수십 개 이상인 경우.

**Bun compile을 고르는 시나리오:** Node.js가 없는 환경에 배포해야 하는 경우. 시작 시간이 중요한 자동화 파이프라인에서 쓰는 경우. npm 없이 단일 바이너리로 배포하고 싶은 경우.

**Deno compile을 고르는 시나리오:** 보안이 특별히 중요한 도구. 권한 제어가 필요한 경우. Deno 생태계를 이미 쓰고 있는 경우.

---

## 마무리

CLI는 TypeScript가 현장에서 어떻게 쓰이는지를 가장 직접적으로 보여주는 영역이다. 언어의 복잡성을 가리지 않으면서도, 타입 시스템의 혜택이 즉각적으로 느껴진다. 인자를 파싱하고, 결과를 출력하고, 오류를 처리하는 과정에서 1장부터 9장까지 배운 모든 것이 실제로 작동하는 모습을 볼 수 있다.

기억해두자 — commander.js로 시작해서 yargs나 oclif로 넘어가는 것은 언제든 가능하다. 반대로 처음부터 oclif를 선택했다가 작은 도구에는 과하다고 느끼는 경우도 있다. 처음에는 commander로 가볍게 시작하는 편이 낫다. 필요해지면 바꾸면 된다.

Java에서 GraalVM native-image 씨름을 해봤다면, Bun compile의 단순함이 상쾌하게 느껴질 것이다. picocli의 애노테이션 방식에 익숙하다면, oclif의 클래스 기반 커맨드가 자연스럽게 느껴질 것이다. Spring Shell의 REPL 모드를 좋아했다면, inquirer의 인터랙티브 프롬프트가 그 역할을 대신한다.

지형도는 이제 충분히 그려졌다. 실제로 손으로 짓는 것이 남아 있다.

---

> **더 깊이 가려면**
>
> 이 장은 지형도와 분석에 집중했다. 실제로 REST API를 호출해 결과를 표로 보여주는 CLI를 처음부터 끝까지 짓는 워크쓰루는 **부록 C**에서 다룬다. commander.js + chalk + cli-table3 + ora 조합으로, 설계 결정 지점마다 "왜 이렇게 했는가"를 짚으며 진행한다. 전체 동작하는 코드와 step-by-step 커밋은 GitHub repo `toby-ai/ts-cli-walkthrough`에 있다.
>
> → 부록 C. TS CLI 한 개 끝까지 짓기 — 워크쓰루

---

11장에서는 같은 TypeScript 코드가 데스크톱 애플리케이션에서 어떤 모양으로 사는지를 살펴본다. Electron이 VS Code와 Slack을 가능하게 한 비결, Tauri가 Rust 백엔드로 바이너리 크기를 1/10로 줄이는 방법, 그리고 두 선택의 트레이드오프를 Java 개발자의 시선으로 분석한다.

---

> 10장에서 TypeScript로 CLI를 짓는 지형을 걸었다. 이제 한 단계 더 나아가, 웹 기술로 데스크톱 앱을 만드는 영역으로 발을 내딛자. Electron과 Tauri — 둘 다 TypeScript로 UI를 짜고, 둘 다 크로스 플랫폼을 지원한다. 그런데 선택은 생각보다 간단하지 않다. 11장에서 그 선택의 근거를 함께 쌓는다.

# 11장. 데스크톱 앱 — Electron과 Tauri의 네이티브 경계

사내 도구 하나를 만들어야 하는 상황을 상상해보자. 백엔드는 Java Spring으로 잘 돌아가고 있고, 이미 React로 웹 UI도 있다. 그런데 팀장이 한 마디 한다. "이거, 데스크톱 앱으로 만들 수 없어요? 파일 시스템 접근이 필요해서." 웹 API만으로는 부족한 순간이다. 브라우저 보안 정책이 파일 시스템을 막고 있고, 알림(notification)도 마음대로 쓸 수 없다.

이 순간, TypeScript 개발자에게 주어진 선택지는 두 가지다. Electron과 Tauri. 둘 다 TypeScript로 UI를 짜고, 둘 다 Windows·macOS·Linux를 지원한다. 그런데 선택은 생각보다 간단하지 않다. 이 챕터는 그 선택의 근거를 함께 쌓아간다.

그리고 데스크톱 이야기를 마무리하면서, 모바일로 자연스럽게 발을 내딛는다. React Native라는 이름은 들어봤을 것이다. 토스가 쓰고, 당근이 쓰고, 쿠팡이츠가 쓴다. 그런데 TypeScript 시각에서 React Native를 들여다본 한국어 자료는 빈약하다. 이 챕터가 그 자리를 채우는 것을 책임으로 삼는다.

---

## Electron — 웹의 힘으로 데스크톱을 정복한 방식

### 왜 VS Code는 Electron을 선택했는가

2015년, Microsoft는 VS Code를 Electron으로 만들기로 했다. 그 결정은 지금도 논쟁거리다. 전 세계 개발자가 매일 쓰는 에디터가 Chromium을 품고 있다는 사실이 여전히 불편한 사람들이 있다. 메모리를 500MB 넘게 쓴다는 푸념도 빠지지 않는다.

하지만 그 결정을 무모한 선택이라고 보기는 어렵다. Electron의 핵심 제안은 간단하다. **"웹 개발자가 이미 아는 기술로 데스크톱 앱을 만들 수 있게 한다."** HTML, CSS, JavaScript — 그것으로 충분하다. 네이티브 UI 툴킷을 새로 배울 필요가 없다. Java로 치면 JavaFX나 Swing을 배울 필요 없이 Spring MVC 지식으로 데스크톱을 만드는 셈이다.

> 📚 **Java/Kotlin 시선 — JavaFX/Swing ↔ Electron/Tauri: 배포 모델의 차이**
>
> JavaFX와 Swing은 JVM 위에서 네이티브 UI 컴포넌트(또는 커스텀 렌더링)를 직접 그린다. 배포는 JAR이고, JVM이 설치되어 있어야 한다. GraalVM native-image로 독립 실행 파일을 만들 수 있지만 제약이 많다.
>
> Electron은 Chromium + Node.js 런타임 전체를 앱과 함께 묶어서 배포한다. 최종 사용자는 Java를 설치할 필요가 없다. 대신 바이너리가 크다 — 기본 Hello World가 150MB 내외. Tauri는 이 문제를 OS의 내장 WebView를 쓰는 방식으로 해결한다 (뒤에서 자세히).
>
> Spring 개발자가 "배포 단위"라는 개념을 바꿔 생각해야 한다. JAR이 아니라 설치 파일(.dmg, .exe, .AppImage)이 최종 산출물이다.

VS Code 외에도 Slack, Discord, Notion, Figma, 그리고 국내 팀들의 사내 도구 다수가 Electron으로 만들어진다. 카카오와 네이버의 일부 내부 도구도 Electron을 쓴다. 이미 React·Vue 기반 웹 코드베이스가 있는 팀에게는 재사용 비율이 높고, 웹 개발자 채용 시장이 넓다는 점이 Electron 선택의 실용적 이유가 된다.

그렇다면 Electron의 구조를 제대로 이해해보자. 제대로 알지 않으면 나중에 찜찜한 코드를 쓰게 된다.

### 메인 프로세스와 렌더러 프로세스 — 두 세계의 공존

Electron 앱은 두 종류의 프로세스로 나뉜다.

**메인 프로세스(Main Process)**는 Node.js 환경이다. 파일 시스템, 운영체제 API, 창 관리, 시스템 트레이 — 네이티브 기능은 전부 여기서 다룬다. 앱이 시작되면 메인 프로세스가 먼저 실행되고, `BrowserWindow`를 만들어 렌더러를 띄운다.

**렌더러 프로세스(Renderer Process)**는 Chromium 환경이다. 각 `BrowserWindow`마다 별도의 렌더러가 생긴다. 여기서는 React, Vue, Svelte — 어떤 웹 프레임워크든 쓸 수 있다. DOM에 접근하고, CSS를 입히고, 사용자와 상호작용한다.

두 프로세스는 별개의 프로세스이기 때문에 메모리를 공유하지 않는다. 직접 함수를 호출할 수 없다. 그렇다면 어떻게 소통할까? 바로 **IPC(Inter-Process Communication)**다.

```typescript
// 메인 프로세스: main.ts
import { app, BrowserWindow, ipcMain } from 'electron'
import * as fs from 'fs/promises'

app.whenReady().then(() => {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,   // 보안: 렌더러와 Node.js를 격리
      nodeIntegration: false,   // 보안: 렌더러에서 Node.js 직접 접근 금지
    },
  })

  // 렌더러로부터 파일 읽기 요청을 받는다
  ipcMain.handle('read-file', async (event, filePath: string) => {
    const content = await fs.readFile(filePath, 'utf-8')
    return content
  })

  win.loadFile('index.html')
})
```

```typescript
// 렌더러 프로세스: renderer.ts (React 컴포넌트 안에서)
const content = await window.electronAPI.readFile('/path/to/file.txt')
```

```typescript
// preload.ts — 두 세계의 다리
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  readFile: (filePath: string) => ipcRenderer.invoke('read-file', filePath),
})
```

여기서 `contextBridge`가 중요하다. 과거 Electron 앱들은 렌더러에서 직접 `ipcRenderer`를 import해 썼다. 그런데 그러면 렌더러가 Node.js API에 직접 접근할 수 있어서 보안 구멍이 생긴다. 악의적인 스크립트가 렌더러에 주입되면 파일 시스템을 마음대로 읽을 수 있다. `contextBridge`는 이 위험을 차단한다. 메인과 렌더러 사이에 선택적으로 노출할 API만 골라서 내보내는 것이다.

### IPC 타이핑 — 타입이 경계를 넘을 수 있는가

자, 이제 TypeScript 개발자로서 진짜 고민이 시작된다. 위의 코드를 보면 `ipcMain.handle('read-file', ...)` 에서 채널 이름이 문자열이다. 렌더러에서 `ipcRenderer.invoke('read-file', filePath)` 를 호출할 때도 문자열이다. 채널 이름을 오타 내도 컴파일 에러가 없다. 인자 타입이 맞지 않아도 컴파일 에러가 없다.

이것은 꽤 난감한 상황이다. TypeScript를 쓰는 이유가 뭔가? 타입 안전성 아닌가. 그런데 IPC 경계에서는 타입이 사라진다.

다행히 이 문제를 해결하는 패턴들이 있다. 가장 직접적인 방법은 **타입 브릿지**를 수동으로 만드는 것이다.

```typescript
// ipc-types.ts — 메인/렌더러가 공유하는 IPC 계약
export interface IpcChannels {
  'read-file': {
    request: [filePath: string]
    response: string
  }
  'write-file': {
    request: [filePath: string, content: string]
    response: void
  }
  'get-app-version': {
    request: []
    response: string
  }
}

// 타입 안전한 ipcMain.handle 래퍼
type IpcMainTyped = {
  handle<K extends keyof IpcChannels>(
    channel: K,
    handler: (
      event: Electron.IpcMainInvokeEvent,
      ...args: IpcChannels[K]['request']
    ) => Promise<IpcChannels[K]['response']>
  ): void
}

// 타입 안전한 ipcRenderer.invoke 래퍼
type IpcRendererTyped = {
  invoke<K extends keyof IpcChannels>(
    channel: K,
    ...args: IpcChannels[K]['request']
  ): Promise<IpcChannels[K]['response']>
}
```

이렇게 하면 채널 이름을 오타 내면 컴파일 에러가 난다. 인자 타입이 맞지 않아도 컴파일 에러가 난다. `IpcChannels` 인터페이스가 메인과 렌더러 사이의 계약서 역할을 한다.

**electron-trpc**는 이 개념을 한 단계 더 밀어붙인 라이브러리다. 13장에서 다룰 tRPC의 아이디어 — "API 스펙을 공유하면 클라이언트 타입이 자동으로" — 를 Electron IPC에 적용한다.

```typescript
// electron-trpc를 쓴 예
import { initTRPC } from '@trpc/server'
import { createIPCHandler } from 'electron-trpc/main'

const t = initTRPC.create()
const router = t.router({
  readFile: t.procedure
    .input(z.object({ filePath: z.string() }))
    .query(async ({ input }) => {
      return fs.readFile(input.filePath, 'utf-8')
    }),
  writeFile: t.procedure
    .input(z.object({ filePath: z.string(), content: z.string() }))
    .mutation(async ({ input }) => {
      await fs.writeFile(input.filePath, input.content)
    }),
})

export type AppRouter = typeof router

// 메인 프로세스에서 핸들러 등록
createIPCHandler({ router, windows: [win] })
```

```typescript
// 렌더러에서
import { createTRPCProxyClient } from '@trpc/client'
import { ipcLink } from 'electron-trpc/renderer'
import type { AppRouter } from '../main/router'

const trpc = createTRPCProxyClient<AppRouter>({
  links: [ipcLink()],
})

// 완전한 타입 안전성 — AppRouter에서 자동 추론
const content = await trpc.readFile.query({ filePath: '/path/to/file.txt' })
const _: string = content  // 타입이 string으로 잘 추론된다
```

`AppRouter` 타입 하나를 메인과 렌더러가 공유하는 것으로 IPC 경계의 타입 안전성이 완성된다. 채널 이름도 없고, 인자 타입도 명시할 필요 없다. tRPC가 5장에서 배운 "타입을 만드는 타입" 기술로 내부적으로 다 처리한다. 정말 우아한 해법이다.

### Electron의 비용 — 솔직하게 직면해야 한다

Electron을 쓰면 반드시 마주하는 현실적인 불편함이 있다. 외면하면 나중에 더 난감하다.

**바이너리 크기.** 단순한 앱도 배포 파일이 150~200MB에 달한다. Chromium과 Node.js 런타임을 통째로 들고 다니기 때문이다. 사용자가 앱을 다운로드할 때 무거움을 느낀다. 자동 업데이트도 그만큼 느리다.

**메모리 사용량.** 빈 Electron 앱이 100MB 이상 메모리를 쓴다. 사내 도구라면 괜찮을 수 있지만, 여러 앱을 동시에 쓰는 사용자 환경에서는 부담이다. Slack이 메모리를 많이 먹는다는 불평은 Electron이 구조적으로 안고 가는 비용이다.

**보안 모델.** `nodeIntegration: true` 로 설정한 오래된 Electron 앱들이 많다. 이 설정은 렌더러에서 Node.js API 직접 접근을 허용해서, XSS 취약점이 있으면 공격자가 파일 시스템에 접근할 수 있다. 신규 프로젝트라면 `contextIsolation: true`, `nodeIntegration: false`, `contextBridge` 사용이 필수다.

그렇다면 이런 비용 없이 비슷한 것을 만들 수 있을까? Tauri가 그 질문에 대한 답이다.

---

## Tauri — Rust 백엔드와 네이티브 WebView의 만남

### Tauri가 Electron과 다른 결정적 지점

Tauri는 2022년 v1이 나오고 2024년 10월 v2가 GA(General Availability) 상태가 됐다. Electron과 목표는 같다 — TypeScript로 크로스 플랫폼 데스크톱 앱 만들기. 그런데 접근 방식이 완전히 다르다.

Electron은 Chromium을 앱에 번들한다. Tauri는 **OS 내장 WebView**를 쓴다. macOS는 WKWebView, Windows는 WebView2(Edge 기반), Linux는 WebKitGTK. 이미 OS에 있는 것을 쓰니까 배포 바이너리에 브라우저를 넣을 필요가 없다.

그 결과가 놀랍다. 같은 기능의 Hello World 앱 기준으로 Electron은 150~200MB, Tauri는 1~5MB다. 약 1/10에서 1/50 수준이다.

Electron의 메인 프로세스가 Node.js라면, Tauri의 백엔드는 **Rust**다. 여기서 Java 백엔드 개발자가 흥미로운 질문을 할 수 있다. "Rust라면 학습 곡선이 급하지 않나요? TypeScript 코드만 쓰고 싶은데."

좋은 소식이 있다. Tauri의 기본 명령들(파일 읽기, 경로 접근 등)은 이미 Rust로 만들어져 있고, TS에서 그냥 호출하면 된다. 커스텀 기능이 필요할 때만 Rust를 직접 쓴다. 그리고 그 경계, 즉 TS에서 Rust 함수를 호출하는 방식이 Tauri의 가장 흥미로운 부분이다.

### `invoke` — TS에서 Rust를 호출하는 방법

Tauri의 IPC는 Electron보다 훨씬 단순하다. 렌더러(프론트)에서 `invoke` 하나로 Rust 함수를 호출한다.

```rust
// src-tauri/src/lib.rs — Rust 백엔드
use tauri::command;

#[command]
fn read_file(file_path: String) -> Result<String, String> {
    std::fs::read_to_string(&file_path)
        .map_err(|e| e.to_string())
}

#[command]
fn greet(name: String) -> String {
    format!("안녕하세요, {}님!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_file, greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```typescript
// 프론트엔드 (TypeScript)
import { invoke } from '@tauri-apps/api/core'

// 이렇게 호출한다
const content = await invoke<string>('read_file', { filePath: '/path/to/file.txt' })
const greeting = await invoke<string>('greet', { name: '토비' })
```

여기서 찜찜한 부분이 보이는가? `invoke<string>('read_file', { filePath: '...' })` 에서 `'read_file'`이 문자열이다. `{ filePath: '...' }` 의 타입도 수동으로 맞춰야 한다. Electron의 순수 IPC 방식과 같은 문제 — 경계에서 타입이 약해진다.

### tauri-specta — Rust 타입을 TypeScript로 내보내기

이 문제를 해결하는 도구가 **tauri-specta**다. Specta는 Rust 타입을 TypeScript 타입으로 자동 생성하는 라이브러리다. tauri-specta는 이것을 Tauri `invoke` 바인딩에 적용한다.

```rust
// Cargo.toml에 specta, specta-typescript, tauri-specta 추가

use specta::Type;
use specta_typescript::Typescript;
use tauri_specta::{collect_commands, ts};

#[derive(Debug, serde::Serialize, serde::Deserialize, Type)]
pub struct FileReadResult {
    pub content: String,
    pub size: u64,
}

#[tauri::command]
#[specta::specta]
fn read_file(file_path: String) -> Result<FileReadResult, String> {
    let content = std::fs::read_to_string(&file_path)
        .map_err(|e| e.to_string())?;
    let size = content.len() as u64;
    Ok(FileReadResult { content, size })
}

fn main() {
    // 타입 내보내기 (개발 시에만 실행)
    #[cfg(debug_assertions)]
    ts::export(
        collect_commands![read_file, greet],
        "../src/bindings.ts"  // TS 파일로 자동 생성
    ).unwrap();

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_file, greet])
        .run(tauri::generate_context!())
        .unwrap();
}
```

이렇게 하면 `src/bindings.ts` 파일이 자동 생성된다.

```typescript
// 자동 생성된 bindings.ts
import { invoke } from "@tauri-apps/api/core"

export interface FileReadResult {
  content: string
  size: number
}

export const commands = {
  readFile: async (filePath: string): Promise<FileReadResult> => {
    return await invoke<FileReadResult>("read_file", { filePath })
  },
  greet: async (name: string): Promise<string> => {
    return await invoke<string>("greet", { name })
  },
}
```

```typescript
// 프론트엔드에서 사용
import { commands } from './bindings'

// 완전한 타입 안전성 — Rust 타입이 TS 타입으로
const result = await commands.readFile('/path/to/file.txt')
console.log(result.content)  // string
console.log(result.size)     // number
```

이것은 5장에서 다룬 "타입을 만드는 타입" 개념의 언어 간 확장이다. Rust의 `#[derive(Type)]`과 `#[specta::specta]`가 런타임에 타입 정보를 수집하고, 빌드 시 TypeScript 타입 파일로 토해낸다. TS→JS의 타입 소거와 반대 방향 — Rust 타입이 TS 타입으로 *생성*된다.

이제 채널 문자열을 잘못 쓸 일이 없다. `commands.readFile` 이 IDE에서 자동완성되고, 인자 타입이 맞지 않으면 컴파일 에러가 난다.

> 📚 **Java/Kotlin 시선 — Java JNI ↔ Tauri `invoke` / React Native Bridge**
>
> Java에서 네이티브 코드(C/C++)를 호출하는 방법이 JNI(Java Native Interface)다. JNI는 악명 높다. 선언부를 직접 매핑해야 하고, 타입 안전성이 없으며, 잘못 쓰면 JVM 크래시다. JNA(Java Native Access)가 조금 낫지만 여전히 번거롭다.
>
> Tauri의 `invoke`는 JSON 직렬화를 통해 TS↔Rust 경계를 넘는다. JNI처럼 메모리 레벨 매핑은 없고, tauri-specta로 타입 계약을 자동 생성할 수 있다. React Native의 JSI(Java Script Interface)도 비슷한 위치 — JS와 C++ 사이의 브릿지를 타입 안전하게 만드는 문제를 푼다 (이 챕터 뒷절에서 자세히).

### Tauri v2의 추가된 것들

Tauri v2(2024년 10월 GA)에서 달라진 것이 있다. 가장 눈에 띄는 것은 **모바일 지원**이다. v2는 iOS와 Android 앱도 같은 코드베이스로 빌드할 수 있다. 다만 v2의 모바일 지원은 아직 성숙 단계이고, React Native 생태계에 비하면 작다. "같은 Rust 코어, 플랫폼별 WebView"라는 아이디어는 매력적이지만, 실전에서 부딪히는 플랫폼별 차이 처리는 아직 커뮤니티가 쌓아가는 중이다.

또 v2의 **보안 모델**이 강화됐다. 메인 설정 파일(`tauri.conf.json`)에서 명시적으로 허용한 API만 프론트에서 접근할 수 있다. Electron에서 `contextBridge`로 수동 관리하던 것을 Tauri는 설정으로 처리한다.

```json
// tauri.conf.json
{
  "plugins": {
    "fs": {
      "scope": {
        "allow": ["$APPDATA/**", "$DOWNLOAD/**"],
        "deny": ["$HOME/.ssh/**"]
      }
    }
  }
}
```

파일 시스템 접근 범위를 명시적으로 선언한다. 공격자가 렌더러에 스크립트를 주입해도 선언된 범위 밖에는 접근할 수 없다.

---

## Electron vs Tauri — 선택의 기준

솔직하게 정리해보자. 둘 중 어느 것이 낫다는 절대적 답은 없다. 상황에 따라 다르다. 다음 표가 그 판단의 기준이 된다.

| 기준 | Electron | Tauri v2 |
|------|----------|-----------|
| **바이너리 크기** | 150~200MB | 1~10MB |
| **메모리 사용** | 100MB+ (기본) | 30~80MB (WebView 공유) |
| **렌더링 엔진** | Chromium (번들, 일관성 ↑) | OS 내장 WebView (플랫폼별 차이 있음) |
| **백엔드 언어** | Node.js (JS/TS) | Rust (학습 곡선 있음) |
| **생태계 성숙도** | 매우 성숙 (10년+) | 성장 중 (v2 2024년) |
| **TS 타입 안전성** | electron-trpc, 수동 브릿지 | tauri-specta 자동 생성 |
| **보안 기본값** | 설정 필요 (contextBridge) | 설정 기반 명시적 허용 |
| **Windows 최소 지원** | Windows 7+ (구버전 Chromium) | Windows 10+ (WebView2) |
| **개발자 경험** | 성숙한 도구, 많은 예제 | 빠르게 개선 중 |
| **한국 사례** | 카카오·네이버 사내 도구 다수 | 토스 일부 신규 시도 |

**Electron이 더 나은 경우:**
- 팀에 Rust 경험자가 없고 빠르게 만들어야 할 때
- 기존 웹 코드베이스를 최대한 재활용하고 싶을 때
- Windows 구버전 지원이 필요할 때
- 생태계와 레퍼런스가 중요할 때

**Tauri가 더 나은 경우:**
- 바이너리 크기와 메모리가 중요한 도구일 때
- 팀에 Rust 역량이 있거나 배울 준비가 됐을 때
- 보안이 핵심인 앱(비밀번호 관리, 기업 보안 도구 등)
- 최신 기술 스택을 채택할 여건이 될 때

사내 도구라면 Electron이 빠른 선택일 수 있다. 외부 배포 소비자 앱이라면 Tauri의 작은 바이너리와 빠른 시작이 사용자 경험에서 차이를 만든다.

### 카카오·네이버 사내 도구 Electron 패턴

한국 대기업 개발 조직에서 Electron 선택은 꽤 실용적인 이유로 이뤄진다. 대부분의 팀이 이미 React 기반 웹 프론트엔드 코드를 갖고 있다. 사내 도구를 웹 앱으로 만들려다 보면 사내 파일 공유 시스템 접근, 시스템 알림, 트레이 아이콘 같은 기능이 브라우저에서는 제한된다. Electron은 이 갭을 최소한의 추가 학습으로 메운다.

카카오의 일부 내부 메신저 확장 도구, 네이버의 일부 개발자 도구가 이런 패턴으로 만들어진다고 알려져 있다. 공개 자료가 제한적이기는 하지만, 기술블로그와 개발자 발표에서 Electron 채택 사례를 종종 볼 수 있다.

흥미로운 점은 "사내 도구는 바이너리 크기보다 빠른 개발이 우선"이라는 조직의 실용적 판단이다. 사용자가 수천 명이 넘지 않는 사내 도구라면 200MB 바이너리도 큰 문제가 아니다. 대신 웹 팀이 추가 기술 없이 바로 기여할 수 있다는 게 더 큰 가치다.

---

## 모바일과 멀티 플랫폼 — TypeScript 시각의 모바일

### 한국 시장에서 React Native가 의미하는 것

당근마켓의 중고 거래 화면 일부, 토스의 일부 화면, 쿠팡이츠의 배달 화면 일부. 이 앱들이 완전한 네이티브(Swift/Kotlin)만으로 만들어진 건 아니다. React Native로 만들어진 화면이 섞여 있다. 그것이 지금 한국 모바일 개발의 현실이다.

"일부"라는 표현이 중요하다. 보통 "RN 부분 도입"은 이런 식이다. 메인 화면, 결제 화면, 지도 화면 같이 성능이 중요하거나 네이티브 API를 많이 쓰는 곳은 Swift/Kotlin. 이벤트 페이지, 정보 화면, 쿠폰 화면 같이 자주 바뀌고 복잡한 네이티브 기능이 없는 곳은 React Native. 그리고 React Native는 이 "자주 바뀌는 화면"에서 큰 강점을 발휘한다. OTA(Over-The-Air) 업데이트로 앱 스토어 심사 없이 바로 업데이트할 수 있다.

이 챕터가 모바일 앱 개발 전반을 다루는 건 아니다. TypeScript 시각에서 "React Native의 타입 경계가 어디인가"를 보는 것이 이 절의 목표다. 한국어 자료에서 이 시각이 특히 빈약하다.

### React Native + TypeScript의 기본 구조

React Native는 기본적으로 JavaScript로 동작한다. TypeScript는 완벽하게 지원된다. Expo를 쓰면 처음부터 TypeScript 프로젝트로 시작할 수 있다.

```bash
# Expo로 TS 프로젝트 시작
npx create-expo-app@latest my-app --template blank-typescript
```

```typescript
// App.tsx
import React, { useState } from 'react'
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native'

interface CounterProps {
  initialCount?: number
  label: string
}

function Counter({ initialCount = 0, label }: CounterProps) {
  const [count, setCount] = useState(initialCount)

  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <TouchableOpacity onPress={() => setCount(c => c + 1)}>
        <Text style={styles.button}>+1</Text>
      </TouchableOpacity>
      <Text style={styles.count}>{count}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  label: { fontSize: 18, marginBottom: 10 },
  button: { fontSize: 24, color: 'blue' },
  count: { fontSize: 32, fontWeight: 'bold' },
})

export default function App() {
  return <Counter label="카운터" initialCount={0} />
}
```

웹 React와 거의 같다. `View`가 `div`, `Text`가 `span`, `TouchableOpacity`가 `button`에 대응한다. 그리고 `props`는 TypeScript 인터페이스로 타입을 정의한다.

**`@types/react-native`**는 React Native의 공식 TypeScript 타입 정의를 제공한다. 다만 최근 React Native는 자체적으로 TypeScript 타입을 포함하고 있어서, 별도 `@types/react-native`를 설치하지 않아도 되는 경우가 늘고 있다.

> 📚 **Java/Kotlin 시선 — Android Jetpack Compose ↔ React Native (UI 선언 모델)**
>
> Android 개발을 Kotlin + Jetpack Compose로 해봤다면 React Native의 선언형 UI가 낯설지 않을 것이다. Jetpack Compose도 같은 패러다임 — 상태가 바뀌면 UI가 재계산된다.

```kotlin
// Compose
@Composable
fun Counter(label: String, initialCount: Int = 0) {
    var count by remember { mutableStateOf(initialCount) }
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = label)
        Button(onClick = { count++ }) { Text("+1") }
        Text(text = count.toString(), fontSize = 32.sp)
    }
}
```

```tsx
// React Native (TypeScript)
function Counter({ label, initialCount = 0 }: CounterProps) {
  const [count, setCount] = useState(initialCount)
  return (
    <View>
      <Text>{label}</Text>
      <TouchableOpacity onPress={() => setCount(c => c + 1)}>
        <Text>+1</Text>
      </TouchableOpacity>
      <Text>{count}</Text>
    </View>
  )
}
```

> 선언형 UI라는 패러다임은 같다. 차이는 렌더링 엔진 — Compose는 Canvas에 직접 그리고, React Native는 JS 로직을 실행하고 그 결과로 iOS/Android 네이티브 컴포넌트를 조작한다. 그래서 성능 특성이 다르고, 네이티브 API 접근 방식도 다르다.

### Expo SDK의 타입 모델

Expo는 React Native 위에 올라가는 SDK다. 카메라, 위치 정보, 파일 시스템, 알림 같은 네이티브 기능을 TS 인터페이스로 깔끔하게 제공한다.

```typescript
import * as Location from 'expo-location'
import * as FileSystem from 'expo-file-system'
import { Camera, CameraType } from 'expo-camera'

// 위치 정보 요청 — 타입이 명확하다
async function getCurrentLocation(): Promise<Location.LocationObject> {
  const { status } = await Location.requestForegroundPermissionsAsync()
  if (status !== 'granted') {
    throw new Error('위치 권한이 없습니다')
  }
  return Location.getCurrentPositionAsync({})
}

// 파일 작업
async function saveUserData(data: string): Promise<void> {
  const fileUri = FileSystem.documentDirectory + 'user-data.json'
  await FileSystem.writeAsStringAsync(fileUri, data)
}

// 카메라 권한 확인
async function requestCameraPermission(): Promise<boolean> {
  const { status } = await Camera.requestCameraPermissionsAsync()
  return status === 'granted'
}
```

`Location.LocationObject`, `Camera.requestCameraPermissionsAsync` — 네이티브 API가 TypeScript 타입으로 표현된다. 물론 내부적으로는 Expo SDK가 iOS Swift / Android Kotlin 코드를 감싸고 있지만, TypeScript 코드를 쓰는 개발자는 그 경계를 직접 다루지 않아도 된다.

이것이 Expo의 핵심 가치다. 네이티브 개발 없이 모바일 기능을 TS로 쓸 수 있는 추상화 레이어. 물론 이 추상화가 필요한 기능을 지원하지 않거나, 성능이 중요한 케이스에서는 한계가 온다. 그때 "네이티브 모듈"을 직접 만드는 길이 있다. 그리고 그 경계를 다루는 기술이 React Native의 신 아키텍처 — JSI와 Fabric이다.

### JSI/Fabric 신 아키텍처 — 타입 경계의 핵심

React Native의 구 아키텍처는 JavaScript 쓰레드와 네이티브 쓰레드가 **비동기 브릿지**로 소통했다. JS 코드가 버튼을 눌렀다고 알리면, 직렬화된 메시지가 브릿지를 건너 네이티브 쓰레드에 도착하고, 네이티브가 처리한 결과가 다시 브릿지를 건너 JS로 돌아왔다. 이 과정이 비동기이기 때문에 빠른 스크롤이나 복잡한 애니메이션에서 버벅임이 생겼다.

**JSI(JavaScript Interface)**는 이 브릿지를 제거한다. C++로 구현된 인터페이스 레이어로 JS 엔진(Hermes)과 네이티브 코드(C++/Swift/Kotlin)가 직접 동기적으로 소통한다. 직렬화가 없다. 복사가 없다. JS에서 네이티브 객체를 직접 참조할 수 있다.

**TurboModule**은 이 JSI를 활용해 네이티브 모듈을 만드는 새로운 방식이다. 그리고 여기서 TypeScript가 핵심 역할을 한다.

```typescript
// NativeCalculator.ts — TurboModule 타입 정의
import type { TurboModule } from 'react-native'
import { TurboModuleRegistry } from 'react-native'

export interface Spec extends TurboModule {
  // 이 스펙이 실제로 iOS .mm 파일과 Android .kt 파일로 코드 생성된다
  add(a: number, b: number): Promise<number>
  multiply(a: number, b: number): number  // 동기 메서드도 가능
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeCalculator')
```

이 `Spec` 인터페이스가 단순한 타입 정의가 아니다. **codegen**이라는 과정이 이 TypeScript 파일을 읽어서 C++, Objective-C, Kotlin 파일을 자동 생성한다.

```
NativeCalculator.ts (TypeScript)
    ↓ codegen
NativeCalculator.h (C++ 헤더)
NativeCalculatorSpec.mm (iOS/ObjC)
NativeCalculatorSpec.kt (Android/Kotlin)
```

```objc
// 자동 생성된 NativeCalculatorSpec.mm (iOS)
// (실제로는 더 복잡하지만 원리 설명용)
@interface RCTNativeCalculator : NSObject <NativeCalculatorSpec>
@end

@implementation RCTNativeCalculator
- (void)add:(double)a b:(double)b resolve:(RCTPromiseResolveBlock)resolve reject:(RCTPromiseRejectBlock)reject {
    resolve(@(a + b));
}
- (double)multiply:(double)a b:(double)b {
    return a * b;
}
@end
```

이것이 핵심이다. TypeScript의 `Spec` 인터페이스가 iOS Objective-C 코드와 Android Kotlin 코드의 시그니처를 강제한다. TypeScript에서 `add(a: number, b: number): Promise<number>` 라고 선언하면, 네이티브 구현도 반드시 그 계약을 지켜야 한다. 지키지 않으면 codegen이 컴파일 에러를 낸다.

이것은 5장의 "타입을 만드는 타입"이 언어 경계를 넘는 가장 극적인 예다. TypeScript 타입이 C++, Objective-C, Kotlin의 코드를 생성한다. Tauri에서 Rust 타입이 TypeScript 타입으로 흘러내려갔다면, TurboModule codegen에서는 TypeScript 타입이 네이티브 코드로 흘러내려간다. 방향이 반대다.

**Fabric**은 UI 레이어의 신 아키텍처다. React 컴포넌트 트리(JS)가 C++ 레이어(Shadow Tree)와 동기적으로 연결된다. 애니메이션과 제스처가 JS 쓰레드를 거치지 않고 직접 네이티브 레이어에서 처리될 수 있다. 결과적으로 60fps(또는 120fps) 애니메이션이 훨씬 안정적으로 돌아간다.

> 🔑 **TurboModule codegen과 Tauri specta의 평행**
>
> 두 기술이 비슷한 문제를 다른 방향에서 푼다.
>
> - **tauri-specta**: Rust 타입 → TypeScript 타입 (Rust가 원천)
> - **RN TurboModule codegen**: TypeScript 타입 → 네이티브 코드 (TypeScript가 원천)
>
> 두 경우 모두 "언어 경계에서 타입 계약을 자동으로 만든다"는 목표는 같다. 수동으로 양쪽을 맞추는 번거로움과 실수를 없애는 것이다.

### 한국 기업의 RN 부분 도입 — 현재진행형

토스, 당근, 쿠팡이츠의 RN 도입은 "우리 앱 전체를 RN으로 다시 짠다"가 아니었다. 그보다는 훨씬 실용적인 접근이었다.

**토스**는 금융 앱의 특성상 결제나 생체인증 화면은 네이티브로 유지하면서, 자주 바뀌는 이벤트 화면이나 일부 정보 화면을 RN으로 만든다. OTA 업데이트 덕분에 마케팅팀이 원하는 이벤트 화면을 앱 스토어 심사 없이 빠르게 바꿀 수 있다.

**당근**은 디자인 시스템을 공유하는 방식으로 웹·앱·데스크톱 플랫폼 간 일관성을 추구한다. RN 컴포넌트와 웹 React 컴포넌트가 같은 디자인 토큰을 참조하고, TypeScript로 props 타입을 공유한다.

**쿠팡이츠**는 배달 화면처럼 지도와 실시간 업데이트가 많은 부분은 네이티브, 메뉴 탐색이나 주문 내역 같은 콘텐츠 중심 화면은 RN으로 나누는 패턴을 쓴다.

이 패턴의 공통점은 "경계를 의식적으로 설계한다"는 것이다. 어느 화면이 RN이고 어느 화면이 네이티브인지, 어느 기능이 Expo SDK로 충분하고 어느 기능이 TurboModule이 필요한지. 이 경계 설계가 잘못되면 성능 문제와 유지보수 지옥이 기다린다.

### React Native vs 네이티브 개발 — 결정 표

Electron vs Tauri와 평행하게, React Native vs 네이티브 iOS/Android 개발의 트레이드오프도 표로 보자.

| 기준 | React Native (+ Expo) | 네이티브 (Swift/Kotlin) |
|------|----------------------|------------------------|
| **시작 시간** | 빠름 (한 코드베이스로 iOS/Android) | 플랫폼별로 따로 개발 |
| **바이너리 크기** | 더 크다 (JS 번들 포함) | 작다 |
| **성능** | 충분히 좋음, 구 아키텍처는 한계 있음 | 최상 |
| **애니메이션** | 신 아키텍처(Fabric)로 크게 개선 | 최상 |
| **네이티브 API 접근** | Expo SDK 또는 TurboModule 필요 | 직접 |
| **OTA 업데이트** | 가능 (JS 번들만 교체) | 불가 (앱 스토어 심사 필요) |
| **팀 구성** | JS/TS 개발자가 모바일 참여 가능 | iOS/Android 전문 개발자 필요 |
| **TS 지원** | 완전 지원, TurboModule codegen | Swift 자체 타입, Kotlin 자체 타입 |
| **한국 채택** | 토스·당근·쿠팡이츠 부분 도입 | 대부분의 한국 앱 메인 화면 |

**React Native가 더 나은 경우:**
- iOS와 Android를 동시에 만들어야 하는데 팀이 작을 때
- 자주 바뀌는 콘텐츠 화면 (OTA의 강점)
- 웹 React 팀이 모바일에도 기여해야 할 때
- 디자인 시스템을 웹과 공유하고 싶을 때

**네이티브가 더 나은 경우:**
- 결제, 생체인증 등 보안이 핵심인 화면
- 고성능 애니메이션, 게임, 카메라 실시간 처리
- 플랫폼 최신 API를 즉시 써야 할 때
- 앱의 핵심 가치가 플랫폼 특유 경험일 때

기억해두자. React Native는 "네이티브 대신"이 아니라 "네이티브와 함께"다. 잘 쓰는 팀은 경계를 의식적으로 설계하고 있다.

---

## 데스크톱과 모바일의 공통점 — TypeScript가 서는 자리

이 챕터를 관통하는 하나의 질문이 있다. **TypeScript의 정적 타입이 네이티브 경계까지 얼마나 닿을 수 있는가?**

Electron에서는 `contextBridge`와 `ipcMain.handle`의 문자열 채널이 경계다. electron-trpc가 그 경계를 넘어 `AppRouter` 타입을 공유한다.

Tauri에서는 `invoke('rust_command', args)` 가 경계다. tauri-specta가 그 경계를 넘어 Rust 타입을 TypeScript 타입으로 변환한다.

React Native에서는 JS 쓰레드와 네이티브 쓰레드 사이의 브릿지가 경계다. TurboModule codegen이 그 경계를 넘어 TypeScript `Spec` 인터페이스를 iOS/Android 네이티브 코드로 변환한다.

세 경우 모두 "경계를 수동으로 관리하면 타입이 없다"는 문제가 있었고, "타입 계약을 자동으로 생성하면 경계도 안전해진다"는 해법이 있었다. 도구 이름이 다를 뿐이다.

그리고 이것은 5장에서 배운 "타입을 만드는 타입"이 가장 극적으로 쓰이는 곳이다. 단순히 `Array<T>`를 `ReadonlyArray<T>`로 바꾸는 게 아니라, 한 언어의 타입 정보를 다른 언어의 코드로 뽑아내는 일이다.

---

## 마무리

데스크톱과 모바일 영역에서 TypeScript는 "웹의 언어"가 UI 레이어를 담당하고, 네이티브 경계에서 타입 계약을 자동으로 잇는 방식으로 자리를 잡았다.

Electron과 Tauri 중 어느 것을 선택할지는 팀의 역량, 앱의 성격, 배포 환경에 따라 다르다. "Electron은 낡았다, Tauri가 미래다"라는 단순한 결론보다는, 두 도구가 서로 다른 트레이드오프를 가진다는 것을 이해하고 선택하는 편이 낫다. Electron의 생태계 성숙도와 낮은 진입 장벽은 여전히 가치 있다.

React Native와 Expo는 TypeScript 개발자가 모바일에 기여하는 가장 현실적인 길이다. JSI/Fabric의 신 아키텍처와 TurboModule codegen은 TS 타입 계약이 네이티브 코드까지 닿는 방식을 계속 정교하게 만들고 있다. 토스, 당근, 쿠팡이츠의 RN 도입은 완성된 이야기가 아니라 현재진행형이다.

한 가지만 기억해두자. 경계를 의식하라. 웹과 데스크톱의 경계, JS와 네이티브의 경계, TypeScript와 Rust/C++의 경계. 그 경계에서 타입이 사라지지 않도록 도구를 선택하고 패턴을 설계하는 것 — 그것이 이 챕터가 말하려는 핵심이다.

다음 12장에서는 웹 프론트엔드로 초점을 옮긴다. React + TypeScript가 컴포넌트 props·이벤트·ref·상태를 타입의 결로 어떻게 표현하는지, 그리고 Vue·Svelte·Solid가 어떻게 다른 reactivity 모델로 같은 문제를 푸는지 살펴보자.

---

> 📖 **더 깊이 가려면**
>
> - **Electron 공식 문서** — Process Model, Security, contextBridge: https://www.electronjs.org/docs/latest/tutorial/process-model
> - **Tauri v2 공식 문서** — Concepts, invoke, Plugins: https://v2.tauri.app/
> - **tauri-specta** — Rust→TS 타입 내보내기: https://github.com/oscartbeaumont/specta (tauri-specta 패키지 포함)
> - **electron-trpc** — Electron + tRPC 조합: https://github.com/jsonnull/electron-trpc
> - **React Native 신 아키텍처** — JSI, TurboModules, Fabric: https://reactnative.dev/docs/the-new-architecture/landing-page
> - **Expo 공식 문서** — SDK 타입, EAS Build: https://docs.expo.dev/
> - **React Native TurboModule codegen** — https://reactnative.dev/docs/native-modules-intro (새 아키텍처 섹션)

---

> 11장에서 데스크톱 앱의 네이티브 경계를 다뤘다. 이제 웹 프론트엔드로 눈을 돌리자. 한국 시장에서 React는 프론트엔드의 압도적 표준이다. Spring MVC 프로젝트를 운영해온 개발자가 처음으로 React 코드베이스를 열었을 때 — "이 함수가 뷰인가, 컨트롤러인가?" — 그 질문에서 시작해, TypeScript와 React가 만나는 핵심 지점들을 12장에서 함께 걸어보자.

# 12장. 웹 프론트엔드 — React + TS의 핵심, 그리고 다른 reactivity 모델의 위치

Spring MVC 프로젝트를 수년째 운영해온 개발자가 처음으로 React 코드베이스를 열었을 때의 표정을 상상해보자. Thymeleaf 템플릿 대신 JSX가 있고, `@Controller`와 `@GetMapping` 대신 컴포넌트 함수가 있다. "이 함수가 뷰인가, 컨트롤러인가?" 하는 질문이 자연스럽게 나온다. 둘 다이기도 하고 둘 다 아니기도 하다 — 이 애매함이 React의 설계다.

그리고 TypeScript를 얹으면 또 다른 질문이 생긴다. 이 컴포넌트에 들어오는 `props`의 타입은 어디서 선언하는가? 버튼 클릭 이벤트의 타입은 무엇인가? `useRef`가 반환하는 것은 `null`일 수도 있는데, 그 타입은 어떻게 다루는가? 이런 질문들은 TypeScript를 처음 쓰는 사람이 아니라, **Java/Kotlin에서 온 시니어 개발자**가 React에서 처음 마주치는 질문이다.

12장은 이 질문들에 정면으로 답한다. React가 한국 시장 프론트엔드의 압도적 표준이라는 현실을 반영해, React와 TypeScript가 만나는 지점을 충분한 깊이로 파고든다. Vue·Svelte·Solid는 별도의 절에서 비교 관점으로만 다룬다 — 언제 만나는지, 왜 다른지, 그 정도로.

---

## React + TypeScript의 시작: 컴포넌트를 타입으로 생각하기

React 컴포넌트를 Java 관점에서 가장 가깝게 비유하면 "데이터를 받아서 뷰를 반환하는 순수 함수"에 가깝다. Spring MVC의 `@Controller`가 HTTP 요청을 받아 `ModelAndView`를 반환하듯, React 컴포넌트는 `props`를 받아 JSX를 반환한다. 물론 `useState`와 `useEffect`가 들어오면 부수효과(side effect)가 생기지만, 기본 개념은 그렇다.

TypeScript와 함께 쓸 때 컴포넌트의 핵심은 **`props`의 타입을 명확하게 선언하는 것**이다. 이 선언이 있어야 컴포넌트를 사용하는 쪽에서 어떤 데이터를 넘겨야 하는지 컴파일 타임에 알 수 있다.

### Props 타이핑: 가장 기본적인 자리

```tsx
// 가장 단순한 형태
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

`interface`로 props의 모양을 선언하고, 함수 매개변수에서 구조 분해 할당으로 받는다. `disabled?: boolean`의 `?`는 선택적 필드를 나타내며, 기본값 `= false`를 지정할 수 있다. 이 정도는 어렵지 않다.

그런데 여기서 자주 실수하는 지점이 있다. `type`과 `interface` 중 무엇을 써야 할까? 결론부터 말하면 **props 정의에는 둘 다 쓸 수 있고, 기능 차이는 거의 없다**. 다만 커뮤니티 관례상 컴포넌트 props는 `interface`를, 유니온·교차·조건부 타입이 필요할 때는 `type`을 쓰는 경향이 있다. 팀에서 일관성을 유지하는 편이 낫다.

### `PropsWithChildren`: 자식 요소를 받는 컴포넌트

```tsx
import { type PropsWithChildren } from 'react';

interface CardProps {
  title: string;
  className?: string;
}

// PropsWithChildren<T>는 T & { children?: ReactNode }와 같다
function Card({ title, className, children }: PropsWithChildren<CardProps>) {
  return (
    <div className={className}>
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  );
}
```

`PropsWithChildren<T>`은 `@types/react`가 제공하는 유틸리티 타입이다. `T & { children?: ReactNode }`를 직접 쓰는 것과 동일하지만, 의도를 더 명확하게 전달한다. React 17 이전에는 함수형 컴포넌트의 타입으로 `React.FC<Props>`를 쓰면 `children`이 자동으로 포함됐지만, React 18부터 `React.FC`에서 `children`이 빠졌다. 지금은 `PropsWithChildren`을 명시적으로 쓰거나, `children: ReactNode`를 직접 선언하는 편이 낫다.

> **📚 Java/Kotlin 시선 박스 ① — Spring MVC + Thymeleaf ↔ React 컴포넌트**
>
> Spring MVC에서 컨트롤러는 비즈니스 로직을 처리하고, Thymeleaf 템플릿은 그 결과를 렌더링한다. 두 역할은 분리되어 있다. React에서는 이 두 역할이 **컴포넌트 함수 안에 함께** 있다. `useState`로 상태를 관리하는 것은 컨트롤러가 할 일이고, JSX를 반환하는 것은 뷰가 할 일인데, React에서는 같은 함수 안에 있다.
>
> 이를 "우려 혼합(mixing concerns)"이라고 비판할 수도 있지만, React의 설계 철학은 다르다 — **"관련된 것"은 함께 있어야 한다**. 버튼의 클릭 핸들러는 버튼 렌더링 코드와 함께 있는 것이 맞다는 관점이다. Thymeleaf의 `th:click`과 컨트롤러의 `@PostMapping` 사이의 매핑보다, JSX 안의 `onClick`이 더 직접적이다.
>
> Spring의 `Model` 객체에 데이터를 담아 뷰로 전달하는 것이 `props`에 해당하고, Thymeleaf의 `${변수명}` 표현식이 JSX의 `{변수명}`에 해당한다. 렌더링 결과물로 HTML이 나온다는 점은 동일하다.

### Generic 컴포넌트: 타입 매개변수를 받는 컴포넌트

컴포넌트도 제네릭이 될 수 있다. 리스트를 렌더링하는 컴포넌트를 생각해보자. `string` 리스트, `User` 리스트, `Product` 리스트를 각각 별도 컴포넌트로 만드는 것은 번거롭다. 제네릭을 쓰면 하나로 처리할 수 있다.

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

// TSX 파일에서 제네릭 화살표 함수를 쓸 때 주의
// <T,> 형태의 trailing comma가 필요한 경우가 있다 (JSX 파서와의 충돌 방지)
function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// 사용 예
interface User {
  id: string;
  name: string;
  email: string;
}

function UserList({ users }: { users: User[] }) {
  return (
    <List
      items={users}
      keyExtractor={(user) => user.id}
      renderItem={(user) => <span>{user.name} — {user.email}</span>}
    />
  );
}
```

TypeScript가 `items`의 타입으로부터 `T`를 추론하므로 `<List<User> ...>`처럼 명시적으로 타입을 넣지 않아도 된다. 추론이 작동하지 않는 경우에만 명시한다.

`.tsx` 파일에서 화살표 함수로 제네릭을 쓸 때 `<T>` 대신 `<T,>`나 `<T extends unknown>`을 써야 할 때가 있다. JSX 파서가 `<T>`를 JSX 태그로 오해하기 때문이다. 이것은 처음 보면 난감하다 — 문법 오류처럼 보이지만 의도적인 회피 패턴이다.

---

## `forwardRef`: 가장 많이 얼버무려지는 자리

`forwardRef`는 많은 학습서에서 짧게 넘어가거나 타입을 생략한 채 소개한다. 하지만 실무에서 컴포넌트 라이브러리를 만들거나, 폼 요소에 외부에서 `ref`를 주입해야 할 때 이 함수를 제대로 이해하지 못하면 꽤 난감한 상황에 처한다. 한 번 정확히 풀어보자.

### `ref`가 왜 필요한가

React의 선언형 패러다임에서는 DOM에 직접 접근하는 것을 가급적 피한다. 하지만 불가피하게 필요할 때가 있다 — 포커스 관리, 텍스트 선택, 애니메이션 트리거, 외부 라이브러리 연동 같은 경우다. 이때 `useRef`를 사용한다.

```tsx
import { useRef, useEffect } from 'react';

function SearchBox() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // 마운트 시 자동 포커스
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} type="search" placeholder="검색어 입력" />;
}
```

`useRef<HTMLInputElement>(null)`에서 타입 매개변수 `HTMLInputElement`는 중요하다. `inputRef.current`가 `HTMLInputElement | null` 타입임을 TypeScript에게 알려주는 것이다. `null`로 초기화하는 이유는 컴포넌트가 마운트되기 전에는 DOM 요소가 아직 존재하지 않기 때문이다.

### `forwardRef`의 타입 완전 해부

`forwardRef`가 필요한 상황은 부모 컴포넌트에서 자식 컴포넌트 내부의 DOM 요소에 직접 `ref`를 연결하고 싶을 때다. 예를 들어 커스텀 `Input` 컴포넌트를 만들었는데, 이를 사용하는 쪽에서 `inputRef`로 포커스를 제어하고 싶다면 어떻게 해야 할까?

```tsx
import { forwardRef, useImperativeHandle, useRef } from 'react';

// 1단계: props 타입과 ref 타입을 별도로 정의
interface InputProps {
  label: string;
  placeholder?: string;
  className?: string;
}

// forwardRef<RefType, PropsType>
// 제네릭 순서 주의: ref 타입이 먼저, props 타입이 나중
const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, placeholder, className }, ref) {
    return (
      <div>
        <label>{label}</label>
        <input
          ref={ref}
          placeholder={placeholder}
          className={className}
        />
      </div>
    );
  }
);

// displayName은 React DevTools에서 컴포넌트 이름이 표시되도록 돕는다
// forwardRef로 감싸면 이름이 사라지는 경우가 있어 명시하는 편이 낫다
Input.displayName = 'Input';

// 사용 예
function LoginForm() {
  const usernameRef = useRef<HTMLInputElement>(null);

  const focusUsername = () => {
    usernameRef.current?.focus();
  };

  return (
    <form>
      <Input ref={usernameRef} label="사용자명" placeholder="아이디 입력" />
      <button type="button" onClick={focusUsername}>
        아이디 필드 포커스
      </button>
    </form>
  );
}
```

`forwardRef<RefType, PropsType>`에서 제네릭 순서가 직관적이지 않게 느껴질 수 있다. ref 타입(`HTMLInputElement`)이 props 타입(`InputProps`)보다 앞에 온다. 이 순서를 반대로 쓰면 타입 오류가 난다 — 처음 접하면 찜찜한 자리다.

### `useImperativeHandle`: ref를 통해 명령형 인터페이스 노출하기

`forwardRef`와 짝을 이루는 `useImperativeHandle`은 부모에게 노출할 메서드를 선택적으로 제한할 때 쓴다. DOM 요소 전체를 그대로 노출하는 것이 아니라, 의도적으로 정의한 인터페이스만 내보내는 방식이다.

```tsx
interface VideoPlayerHandle {
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
}

interface VideoPlayerProps {
  src: string;
  autoPlay?: boolean;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, VideoPlayerProps>(
  function VideoPlayer({ src, autoPlay }, ref) {
    const videoRef = useRef<HTMLVideoElement>(null);

    useImperativeHandle(ref, () => ({
      play() {
        videoRef.current?.play();
      },
      pause() {
        videoRef.current?.pause();
      },
      seek(time: number) {
        if (videoRef.current) {
          videoRef.current.currentTime = time;
        }
      },
    }));

    return <video ref={videoRef} src={src} autoPlay={autoPlay} />;
  }
);

// 사용 예
function VideoController() {
  const playerRef = useRef<VideoPlayerHandle>(null);

  return (
    <div>
      <VideoPlayer ref={playerRef} src="/video/demo.mp4" />
      <button onClick={() => playerRef.current?.play()}>재생</button>
      <button onClick={() => playerRef.current?.pause()}>일시정지</button>
    </div>
  );
}
```

`useRef<VideoPlayerHandle>(null)`에서 타입이 `VideoPlayerHandle`이다. `HTMLVideoElement` 전체가 아니라 우리가 정의한 인터페이스만 외부에 노출된다. 부모는 `play()`, `pause()`, `seek()`만 호출할 수 있고, `videoRef.current?.volume = 0` 같은 다른 DOM 조작은 할 수 없다. 캡슐화가 강제된다. Java 개발자라면 이 패턴이 낯설지 않을 것이다 — 인터페이스를 통한 추상화다.

---

## 이벤트 핸들러의 타입: `React.MouseEvent`와 `ChangeEvent`의 결

이벤트 핸들러를 타이핑할 때 처음에는 그냥 `() => void`로 쓰거나 `any`로 도망치고 싶은 유혹이 생긴다. 하지만 이벤트 객체에 접근해야 할 때 타입이 없으면 금방 곤란해진다.

### 기본 이벤트 타입

```tsx
// 클릭 이벤트
function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
  // event.currentTarget은 HTMLButtonElement
  console.log(event.currentTarget.id);
  event.preventDefault();
}

// 인라인에서는 타입 추론이 자동으로
function ClickButton() {
  return (
    <button
      onClick={(e) => {
        // e: React.MouseEvent<HTMLButtonElement, MouseEvent>
        // 자동 추론되므로 타입 명시 불필요
        console.log(e.clientX, e.clientY);
      }}
    >
      클릭
    </button>
  );
}
```

인라인 이벤트 핸들러에서는 TypeScript가 대상 요소의 타입을 자동으로 추론한다. `<button onClick={(e) => ...}>`에서 `e`의 타입은 자동으로 `React.MouseEvent<HTMLButtonElement, MouseEvent>`가 된다. 별도의 핸들러 함수를 만들 때만 타입을 명시해야 한다.

### `ChangeEvent`: 폼 요소의 핵심

```tsx
// input 값이 바뀔 때
function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
  const value = event.target.value; // string
  console.log(value);
}

// textarea
function handleTextarea(event: React.ChangeEvent<HTMLTextAreaElement>) {
  const value = event.target.value;
}

// select
function handleSelect(event: React.ChangeEvent<HTMLSelectElement>) {
  const value = event.target.value;
}

// 실제 컴포넌트에서의 사용
function SearchForm() {
  const [query, setQuery] = React.useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      // e는 React.ChangeEvent<HTMLInputElement>로 자동 추론
    />
  );
}
```

`event.target`과 `event.currentTarget`의 차이를 기억해두자. `currentTarget`은 이벤트 핸들러가 붙어 있는 요소이고, `target`은 이벤트가 실제로 발생한 요소다. 이벤트 버블링이 있을 때 둘이 다를 수 있다. 폼 입력값을 읽을 때는 대개 `event.target.value`를 쓴다.

### 이벤트 핸들러 props의 타입

부모 컴포넌트에서 자식 컴포넌트로 이벤트 핸들러를 prop으로 전달할 때의 타입 선언이다.

```tsx
interface SearchInputProps {
  value: string;
  // React.ChangeEventHandler<HTMLInputElement>는
  // (event: React.ChangeEvent<HTMLInputElement>) => void 와 동일
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  onSubmit: (query: string) => void;
  onKeyDown?: React.KeyboardEventHandler<HTMLInputElement>;
}

function SearchInput({ value, onChange, onSubmit, onKeyDown }: SearchInputProps) {
  const handleKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
    if (e.key === 'Enter') {
      onSubmit(value);
    }
    onKeyDown?.(e);
  };

  return (
    <input
      value={value}
      onChange={onChange}
      onKeyDown={handleKeyDown}
    />
  );
}
```

`React.ChangeEventHandler<T>`는 `(event: React.ChangeEvent<T>) => void`의 별칭이다. 타입 이름이 길어지는 것을 피하고 싶을 때 쓴다. `React.MouseEventHandler`, `React.KeyboardEventHandler` 등도 같은 방식으로 정의되어 있다.

---

## `useState`와 `useReducer`의 타입: 추론과 명시의 균형

### `useState`의 타입 추론

```tsx
// 타입 추론이 작동하는 경우 — 명시할 필요 없음
const [count, setCount] = useState(0);          // number
const [name, setName] = useState('');            // string
const [isLoading, setIsLoading] = useState(false); // boolean

// 타입 추론이 부족해 명시가 필요한 경우
const [user, setUser] = useState<User | null>(null);
// null로 초기화하면 타입이 null로 추론되어 User를 할당할 수 없게 된다
// null로 시작하지만 나중에 User가 들어올 것이라는 의도를 명시해야 한다

// 배열
const [items, setItems] = useState<string[]>([]);
// []만 쓰면 never[]로 추론될 수 있다
```

`useState<User | null>(null)` 패턴은 매우 자주 쓰인다. API에서 데이터를 불러오기 전에는 `null`, 불러온 후에는 `User` 타입이 되는 상황이다. 초기값으로 `null`을 넣으면 TypeScript는 타입을 `null`로 추론하고, 나중에 `User` 객체를 `setUser`로 넣으려 하면 타입 오류가 난다. 제네릭으로 타입을 명시해야 한다.

### 복잡한 상태는 `useReducer`

상태가 여러 필드로 구성되어 있고 업데이트 로직이 복잡할 때는 `useReducer`가 낫다. 이 패턴은 Java의 상태 기계(state machine)나 Redux 스타일을 알고 있다면 친숙하다.

```tsx
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
  isLoading: boolean;
}

// discriminated union으로 액션 타입 정의
type CartAction =
  | { type: 'ADD_ITEM'; payload: Omit<CartItem, 'quantity'> }
  | { type: 'REMOVE_ITEM'; payload: { id: string } }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'CLEAR_CART' };

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existing = state.items.find(item => item.id === action.payload.id);
      if (existing) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        };
      }
      const newItem: CartItem = { ...action.payload, quantity: 1 };
      return {
        ...state,
        items: [...state.items, newItem],
        total: state.total + action.payload.price,
      };
    }
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload.id),
      };
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'CLEAR_CART':
      return { items: [], total: 0, isLoading: false };
    default:
      // TypeScript exhaustiveness check
      // CartAction에 새로운 type을 추가하면 여기서 컴파일 오류
      const _exhaustive: never = action;
      return state;
  }
}

function Cart() {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    total: 0,
    isLoading: false,
  });

  return (
    <div>
      {state.items.map(item => (
        <div key={item.id}>
          {item.name} × {item.quantity}
          <button onClick={() => dispatch({ type: 'REMOVE_ITEM', payload: { id: item.id } })}>
            제거
          </button>
        </div>
      ))}
    </div>
  );
}
```

`CartAction`을 discriminated union으로 정의하면 `switch`의 `default` 브랜치에서 `never` 타입 체크가 작동한다. 나중에 `CartAction`에 새로운 액션 타입을 추가했는데 `cartReducer`에서 처리하지 않으면 컴파일 오류가 발생한다. 5장에서 다룬 exhaustiveness check가 여기서 살아난다. 이 패턴은 Kotlin의 `sealed class` + `when`과 정확히 같은 역할을 한다.

---

## `useEffect`의 cleanup과 dependency 타입 안전

`useEffect`는 React에서 부수효과(데이터 패치, 이벤트 리스너, 타이머)를 다루는 hook이다. TypeScript와 함께 쓸 때 특히 주의해야 하는 지점 몇 가지를 살펴보자.

### cleanup 함수의 타입

```tsx
import { useEffect, useState } from 'react';

function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    // cleanup: 반환값이 () => void이어야 한다
    return () => {
      clearInterval(id);
    };
  }, []); // 빈 배열 = 마운트/언마운트 시만 실행

  return <div>{count}초 경과</div>;
}
```

`useEffect`의 콜백 함수는 `() => void | (() => void)`를 반환해야 한다. cleanup 함수를 반환하거나, 아무것도 반환하지 않거나 둘 중 하나다. `async` 함수를 직접 `useEffect`에 전달하면 안 된다 — `async` 함수는 항상 `Promise`를 반환하는데, `useEffect`는 `Promise`를 cleanup 함수로 처리하지 못하기 때문이다.

```tsx
// 잘못된 패턴 — TypeScript도 경고한다
useEffect(async () => {
  const data = await fetchData();
  setData(data);
}, []);

// 올바른 패턴
useEffect(() => {
  let cancelled = false;

  async function loadData() {
    const data = await fetchData();
    if (!cancelled) {
      setData(data);
    }
  }

  loadData();

  return () => {
    cancelled = true;
  };
}, []);
```

두 번째 패턴에서 `cancelled` 플래그를 쓰는 이유는 컴포넌트가 언마운트된 후 비동기 작업이 완료되어 상태를 업데이트하려 할 때를 막기 위해서다. AbortController를 쓸 수도 있다 — 취소 가능한 fetch 요청을 만들 때 더 깔끔하다.

```tsx
useEffect(() => {
  const controller = new AbortController();

  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(data => setData(data))
    .catch(err => {
      if (err.name !== 'AbortError') {
        setError(err);
      }
    });

  return () => controller.abort();
}, []);
```

### dependency 배열의 함정

`useEffect`의 두 번째 인수인 dependency 배열에 어떤 값을 넣어야 하는지는 TypeScript가 직접 강제하지는 않는다 — `eslint-plugin-react-hooks`의 `react-hooks/exhaustive-deps` 규칙이 담당한다. 하지만 타입과 무관하게, dependency를 잘못 관리하면 찜찜한 버그가 생긴다.

```tsx
// 함수를 dependency에 넣을 때의 문제
function DataFetcher({ userId }: { userId: string }) {
  const [data, setData] = useState<Data | null>(null);

  // 이 함수가 렌더링마다 새로 생성되면 useEffect가 무한 루프에 빠진다
  async function fetchUserData() {
    const result = await fetchUser(userId);
    setData(result);
  }

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]); // 매 렌더링마다 새 함수 참조 → 무한 루프

  return <div>{data?.name}</div>;
}

// 해결: useCallback으로 함수를 메모이제이션
function DataFetcherFixed({ userId }: { userId: string }) {
  const [data, setData] = useState<Data | null>(null);

  const fetchUserData = useCallback(async () => {
    const result = await fetchUser(userId);
    setData(result);
  }, [userId]); // userId가 바뀔 때만 새 함수 참조

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  return <div>{data?.name}</div>;
}
```

`useCallback`의 타입은 전달하는 함수의 타입을 그대로 추론한다. 명시적으로 넣을 필요는 없지만, 복잡한 경우에는 반환 타입을 명시하는 편이 낫다.

---

## 커스텀 Hook: 로직의 타입화된 캡슐

커스텀 hook은 React의 강력한 추상화 메커니즘이다. 여러 컴포넌트에서 공유되는 상태 로직을 별도 함수로 추출할 수 있다. Java에서 서비스 클래스나 리포지토리로 비즈니스 로직을 분리하는 것과 비슷한 목적이다 — 하지만 형태는 전혀 다르다.

### 기본 커스텀 Hook

```tsx
// useLocalStorage: localStorage와 동기화되는 상태
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.error(`localStorage 읽기 실패 [${key}]:`, error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`localStorage 쓰기 실패 [${key}]:`, error);
    }
  };

  return [storedValue, setValue] as const;
  // as const가 없으면 반환 타입이 (T | ...)[]로 추론되어
  // setStoredValue를 함수로 쓸 수 없게 된다
}

// 사용
function Settings() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
  const [language, setLanguage] = useLocalStorage('language', 'ko');

  return (
    <div>
      <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
        테마 전환 (현재: {theme})
      </button>
    </div>
  );
}
```

`as const`의 역할이 여기서 중요하다. `[storedValue, setValue]`를 반환하면 TypeScript는 이를 `Array<T | ((value: T | ((val: T) => T)) => void)>`로 추론한다. 배열의 첫 번째 요소가 상태 값인지 세터인지 구분하지 못한다. `as const`를 붙이면 `readonly [T, (value: ...) => void]` 튜플로 추론되어 각 위치의 타입이 고정된다.

### Generic Hook: 타입이 흐르는 추상화

```tsx
// useAsync: 비동기 함수의 상태를 관리하는 hook
interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

function useAsync<T>(
  asyncFn: () => Promise<T>,
  deps: React.DependencyList = []
) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    isLoading: true,
  });

  useEffect(() => {
    let cancelled = false;

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    asyncFn()
      .then(data => {
        if (!cancelled) {
          setState({ data, error: null, isLoading: false });
        }
      })
      .catch(error => {
        if (!cancelled) {
          setState({ data: null, error, isLoading: false });
        }
      });

    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}

// 사용 예
interface Post {
  id: number;
  title: string;
  body: string;
}

function PostDetail({ postId }: { postId: number }) {
  const { data: post, isLoading, error } = useAsync<Post>(
    () => fetch(`/api/posts/${postId}`).then(r => r.json()),
    [postId]
  );

  if (isLoading) return <div>로딩 중...</div>;
  if (error) return <div>오류: {error.message}</div>;
  if (!post) return null;

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
    </article>
  );
}
```

`useAsync<Post>(...)` — 제네릭 타입 매개변수를 명시하면 `state.data`의 타입이 `Post | null`로 고정된다. 물론 `asyncFn`의 반환 타입으로부터 추론되므로 명시하지 않아도 되는 경우가 많다.

---

## Suspense와 Server Components의 타입 측면

React 18에서 Suspense가 데이터 패칭에 정식으로 활용되기 시작했고, React 19에서는 Server Components가 안정화됐다. 이 두 기능의 깊은 런타임 동작은 13장 풀스택 절에서 다루지만, **타입 측면**에서 알아둬야 할 것이 있다.

### Suspense와 `lazy`의 타입

```tsx
import { Suspense, lazy } from 'react';

// lazy는 default export인 컴포넌트를 반환하는 Promise를 받는다
const HeavyChart = lazy(() => import('./HeavyChart'));
// 타입: React.LazyExoticComponent<typeof HeavyChart>

function Dashboard() {
  return (
    <Suspense fallback={<div>차트 로딩 중...</div>}>
      <HeavyChart data={[1, 2, 3]} />
    </Suspense>
  );
}
```

`lazy`로 불러오는 모듈은 반드시 `default export`여야 한다. named export만 있는 컴포넌트는 `lazy`로 직접 불러올 수 없다 — 래핑이 필요하다.

### Server Component의 타입 규칙 (Next.js App Router 기준)

Server Component는 `async` 컴포넌트가 될 수 있다. 이것이 Client Component와의 가장 큰 타입 차이다.

```tsx
// Server Component — async 함수로 정의 가능
// app/users/page.tsx
async function UsersPage() {
  // 서버에서 직접 데이터 패치 (useState, useEffect 없음)
  const users = await fetchUsers();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// Client Component — 'use client' 지시자 필요, async 불가
'use client';
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

Server Component에 props를 전달할 때, **함수는 전달할 수 없다**. 서버와 클라이언트 사이의 경계에서 함수는 직렬화할 수 없기 때문이다. TypeScript가 이를 컴파일 타임에 완전히 잡아주지는 않지만, Next.js의 타입 체크 레이어가 일부 잡아준다. 이 부분의 타입 경험은 아직 성숙 중이다 — RSC 깊은 내용은 13장에서 다룬다.

---

## 폼과 검증: React Hook Form + zod로 Bean Validation 재현하기

폼 처리는 프론트엔드의 가장 번거로운 영역 중 하나다. 입력값 관리, 유효성 검증, 에러 표시, 제출 처리를 각각 따로 구현하면 코드가 금방 복잡해진다. Spring의 Bean Validation + `@Valid`가 이 번거로움을 많이 줄여줬던 것처럼, React 생태계에는 **React Hook Form + zod**라는 조합이 있다.

> **📚 Java/Kotlin 시선 박스 ② — Bean Validation + DTO ↔ zod schema**
>
> Spring에서 폼 데이터를 다룰 때는 DTO 클래스를 만들고 Bean Validation 어노테이션을 붙인다.
>
> ```java
> public class SignUpRequest {
>     @NotBlank(message = "이메일은 필수입니다")
>     @Email(message = "올바른 이메일 형식이어야 합니다")
>     private String email;
>
>     @Size(min = 8, message = "비밀번호는 8자 이상이어야 합니다")
>     private String password;
>
>     @NotBlank(message = "이름은 필수입니다")
>     private String name;
> }
> ```
>
> 컨트롤러에서 `@Valid`를 붙이면 Spring이 검증을 실행하고, 실패 시 `BindingResult`에 오류를 담는다.
>
> zod + React Hook Form은 같은 역할을 한다. zod schema가 DTO + Bean Validation 어노테이션의 역할이고, `resolver`가 `@Valid`의 역할이다. 핵심 차이는 **타입이 schema에서 자동 파생된다는 것** — `z.infer<typeof schema>`로 TypeScript 타입을 별도로 선언할 필요 없이 schema가 단일 진실 원천이 된다.

### React Hook Form의 기본 타입 패턴

```tsx
import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1단계: zod schema 정의 — 이것이 단일 진실 원천
const signUpSchema = z.object({
  email: z
    .string()
    .min(1, '이메일은 필수입니다')
    .email('올바른 이메일 형식이어야 합니다'),
  password: z
    .string()
    .min(8, '비밀번호는 8자 이상이어야 합니다')
    .regex(/[A-Z]/, '대문자를 포함해야 합니다')
    .regex(/[0-9]/, '숫자를 포함해야 합니다'),
  name: z
    .string()
    .min(1, '이름은 필수입니다')
    .max(50, '이름은 50자 이하여야 합니다'),
  agreeToTerms: z.boolean().refine(val => val === true, {
    message: '이용약관에 동의해야 합니다',
  }),
});

// 2단계: schema에서 TypeScript 타입 파생
// 별도의 interface를 선언할 필요 없다 — schema가 단일 진실 원천
type SignUpFormValues = z.infer<typeof signUpSchema>;
// {
//   email: string;
//   password: string;
//   name: string;
//   agreeToTerms: boolean;
// }

// 3단계: useForm에 타입 연결
function SignUpForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<SignUpFormValues>({
    resolver: zodResolver(signUpSchema),
    defaultValues: {
      email: '',
      password: '',
      name: '',
      agreeToTerms: false,
    },
  });

  // SubmitHandler<T>는 (data: T) => void | Promise<void>
  const onSubmit: SubmitHandler<SignUpFormValues> = async (data) => {
    // data는 SignUpFormValues 타입 — 검증이 통과한 데이터
    // zod가 런타임에 검증하고 변환했으므로 타입이 보장된다
    try {
      await registerUser(data);
      reset();
    } catch (error) {
      console.error('회원가입 실패:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">이메일</label>
        <input
          id="email"
          type="email"
          {...register('email')}
          // register는 name, ref, onChange, onBlur를 spread
          // 'email' 문자열은 SignUpFormValues의 key만 허용 — 오타를 컴파일 타임에 잡는다
        />
        {errors.email && (
          <span role="alert">{errors.email.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="password">비밀번호</label>
        <input
          id="password"
          type="password"
          {...register('password')}
        />
        {errors.password && (
          <span role="alert">{errors.password.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="name">이름</label>
        <input
          id="name"
          {...register('name')}
        />
        {errors.name && (
          <span role="alert">{errors.name.message}</span>
        )}
      </div>

      <div>
        <input
          id="agreeToTerms"
          type="checkbox"
          {...register('agreeToTerms')}
        />
        <label htmlFor="agreeToTerms">이용약관에 동의합니다</label>
        {errors.agreeToTerms && (
          <span role="alert">{errors.agreeToTerms.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '가입 중...' : '회원가입'}
      </button>
    </form>
  );
}
```

`register('email')`에서 `'email'` 문자열은 `SignUpFormValues`의 키로 제한된다. `register('emali')`처럼 오타를 치면 컴파일 오류가 발생한다. 5장에서 다룬 `z.infer`가 여기서 실용적으로 작동하는 것이다 — schema 하나가 런타임 검증과 컴파일 타임 타입 안전을 동시에 제공한다.

### 중첩 객체와 배열을 포함하는 복잡한 폼

```tsx
const orderSchema = z.object({
  customer: z.object({
    name: z.string().min(1, '고객명은 필수입니다'),
    email: z.string().email('이메일 형식이 올바르지 않습니다'),
    phone: z.string().regex(/^010-\d{4}-\d{4}$/, '010-XXXX-XXXX 형식으로 입력하세요'),
  }),
  items: z.array(
    z.object({
      productId: z.string().min(1),
      quantity: z.number().int().positive('수량은 1 이상이어야 합니다'),
    })
  ).min(1, '최소 1개 이상의 상품을 선택해야 합니다'),
  deliveryAddress: z.string().min(10, '배송지 주소를 상세히 입력해주세요'),
  specialRequest: z.string().optional(),
});

type OrderFormValues = z.infer<typeof orderSchema>;

function OrderForm() {
  const { register, control, handleSubmit, formState: { errors } } = useForm<OrderFormValues>({
    resolver: zodResolver(orderSchema),
  });

  // 배열 필드는 useFieldArray hook으로 관리
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  });

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <input {...register('customer.name')} placeholder="고객명" />
      {/* 중첩 경로도 점 표기법으로 접근 — 타입 안전 */}
      {errors.customer?.name && <span>{errors.customer.name.message}</span>}

      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
            type="number"
          />
          <button type="button" onClick={() => remove(index)}>제거</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ productId: '', quantity: 1 })}>
        상품 추가
      </button>
    </form>
  );
}
```

`register('customer.name')`의 점 표기법 경로도 타입 체크된다. `OrderFormValues`의 구조에 없는 경로를 쓰면 컴파일 오류가 난다. 폼 코드를 리팩토링할 때 schema를 바꾸면 모든 `register` 호출 오류가 한꺼번에 표시된다 — 빠진 곳이 없는지 걱정할 필요가 없다.

---

## 전역 상태: Zustand·Jotai·Redux Toolkit의 타입 모델

전역 상태 관리는 React 생태계에서 논쟁이 많은 영역이다. `useState`와 Context API만으로 충분한 경우도 있고, 앱이 커지면 전용 라이브러리가 필요해진다. 세 가지 주요 선택지를 타입 측면에서 비교해보자.

### Zustand: 가장 단순한 타입 모델

```tsx
import { create } from 'zustand';

// 스토어 타입을 인터페이스로 정의 — 상태와 액션을 함께
interface BearStore {
  bears: number;
  fish: number;
  increaseBears: () => void;
  eatFish: () => void;
  reset: () => void;
}

const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  fish: 10,
  increaseBears: () => set((state) => ({ bears: state.bears + 1 })),
  eatFish: () => set((state) => ({ fish: state.fish - 1 })),
  reset: () => set({ bears: 0, fish: 10 }),
}));

// 컴포넌트에서 선택자(selector)로 구독
function BearCounter() {
  // 필요한 상태만 구독 — 리렌더링 최소화
  const bears = useBearStore((state) => state.bears);
  const increaseBears = useBearStore((state) => state.increaseBears);

  return (
    <div>
      <span>곰 {bears}마리</span>
      <button onClick={increaseBears}>곰 추가</button>
    </div>
  );
}
```

Zustand의 타입 모델은 단순하다. `create<StoreType>()`에 타입을 한 번 넣으면 이후 `set`, `get` 콜백에서 모두 추론된다. Redux의 action type, reducer, selector를 각각 따로 정의해야 하는 복잡함이 없다.

### Jotai: 원자(atom) 기반의 타입 추론

```tsx
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// 기본 atom — 타입은 초기값에서 추론
const countAtom = atom(0); // Atom<number>
const textAtom = atom(''); // Atom<string>

// 파생 atom (읽기 전용)
const doubledCountAtom = atom(
  (get) => get(countAtom) * 2
); // Atom<number>

// 읽기/쓰기 파생 atom
const normalizedTextAtom = atom(
  (get) => get(textAtom).trim().toLowerCase(),
  (_get, set, newValue: string) => set(textAtom, newValue)
);

// 비동기 atom
const userAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  const response = await fetch(`/api/users/${userId}`);
  return response.json() as Promise<User>;
}); // Atom<Promise<User>>

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const doubled = useAtomValue(doubledCountAtom);
  const setCountOnly = useSetAtom(countAtom); // setter만 구독 — 리렌더링 없음

  return (
    <div>
      <span>{count} (두 배: {doubled})</span>
      <button onClick={() => setCount(c => c + 1)}>증가</button>
    </div>
  );
}
```

Jotai는 React의 `useState`와 비슷한 API를 유지하면서 전역으로 확장한다. 타입 추론이 자연스럽고, Context의 Provider 없이도 전역 공유가 된다.

### Redux Toolkit: 가장 정형화된 타입 패턴

```tsx
import { createSlice, type PayloadAction, configureStore } from '@reduxjs/toolkit';
import { useDispatch, useSelector, type TypedUseSelectorHook } from 'react-redux';

interface UserState {
  currentUser: User | null;
  isAuthenticated: boolean;
  preferences: {
    theme: 'light' | 'dark';
    language: 'ko' | 'en';
  };
}

const initialState: UserState = {
  currentUser: null,
  isAuthenticated: false,
  preferences: {
    theme: 'light',
    language: 'ko',
  },
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<User>) {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
    },
    logout(state) {
      state.currentUser = null;
      state.isAuthenticated = false;
    },
    setTheme(state, action: PayloadAction<'light' | 'dark'>) {
      state.preferences.theme = action.payload;
    },
  },
});

const store = configureStore({
  reducer: {
    user: userSlice.reducer,
  },
});

// 타입 안전한 dispatch와 selector hook 생성 — 재사용을 위해 별도 파일로
type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

const useAppDispatch = () => useDispatch<AppDispatch>();
const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// 컴포넌트에서 사용
function UserProfile() {
  const dispatch = useAppDispatch();
  const { currentUser, isAuthenticated } = useAppSelector(state => state.user);

  if (!isAuthenticated || !currentUser) return null;

  return (
    <div>
      <span>{currentUser.name}</span>
      <button onClick={() => dispatch(userSlice.actions.logout())}>
        로그아웃
      </button>
    </div>
  );
}
```

| | Zustand | Jotai | Redux Toolkit |
|---|---|---|---|
| **보일러플레이트** | 적음 | 매우 적음 | 많음 |
| **타입 복잡도** | 낮음 | 낮음 | 중간 |
| **DevTools** | 있음 | 있음 | 강력함 |
| **적합한 규모** | 소~중 | 소~대 | 중~대 |
| **Java 비유** | 서비스 싱글톤 | Context + Provider | Spring ApplicationContext + Bean |
| **한국 현장** | 신규 스타트업 선호 | 실험적 사용 | 기존 코드베이스 많음 |

작은 앱에는 Zustand, Context API도 충분하다. Redux Toolkit은 대규모 팀에서 일관된 패턴이 필요할 때 가치를 발휘한다. "어떤 것이 최선"이 아니라 팀과 규모에 맞는 선택을 하는 편이 낫다.

---

## 컴포넌트 라이브러리: 외부 props 타입과 조합 패턴

직접 UI 컴포넌트를 모두 만들 필요는 없다. Radix UI, shadcn/ui, Mantine, Chakra UI 같은 라이브러리가 접근성(accessibility)과 상호작용을 미리 구현해둔 컴포넌트를 제공한다.

### 외부 컴포넌트 props 확장

```tsx
import { type ButtonHTMLAttributes } from 'react';

// Radix UI 버튼의 props를 확장하는 패턴
// 또는 표준 HTML 요소의 props를 확장할 때
interface AppButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
}

function AppButton({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  children,
  disabled,
  className,
  ...htmlProps  // 나머지 HTML 버튼 속성들
}: AppButtonProps) {
  const classes = buildClasses(variant, size, className);

  return (
    <button
      {...htmlProps}
      disabled={disabled || isLoading}
      className={classes}
    >
      {isLoading && <Spinner />}
      {leftIcon && <span className="icon">{leftIcon}</span>}
      {children}
    </button>
  );
}
```

`ButtonHTMLAttributes<HTMLButtonElement>`를 `extends`하면 `onClick`, `type`, `form`, `aria-*` 등 표준 버튼 속성을 모두 받을 수 있다. 컴포넌트 API를 추가하면서 HTML 요소의 속성을 모두 지원하고 싶을 때 자주 쓰는 패턴이다.

### ComponentPropsWithoutRef: 라이브러리 컴포넌트 props 재사용

```tsx
import { type ComponentPropsWithoutRef } from 'react';

// 기존 컴포넌트의 props를 가져와서 일부만 덮어쓰기
type InputWithLabelProps = ComponentPropsWithoutRef<'input'> & {
  label: string;
  error?: string;
};

// shadcn/ui 컴포넌트 props 확장
import { Button } from '@/components/ui/button';
type ExtendedButtonProps = ComponentPropsWithoutRef<typeof Button> & {
  trackingId: string;
};
```

`ComponentPropsWithoutRef<'input'>`은 `InputHTMLAttributes<HTMLInputElement>`와 비슷하지만, 더 일반적인 패턴이다. `typeof Button`처럼 컴포넌트 자체를 타입 인수로 넣으면 해당 컴포넌트의 props 타입을 가져올 수 있다.

### CSS 타이핑: 짧게

Tailwind CSS를 쓸 때는 대부분 문자열 클래스 이름을 사용하므로 별도의 타입 선언이 크게 필요하지 않다. `clsx`나 `cn` (shadcn/ui 관례) 함수로 조건부 클래스를 조합한다. CSS-in-JS(Emotion, styled-components)를 쓸 때는 `CSSObject` 타입이 prop의 타입 안전을 제공한다. 디자인 토큰을 TypeScript로 정의하면 색상·간격·폰트 크기가 타입으로 관리된다.

---

## Vue·Svelte·Solid의 자리: 비교 관점에서

React가 한국 시장에서 압도적이라는 것은 사실이지만, 다른 프레임워크를 전혀 모르고 지내기는 어렵다. 레거시 코드베이스에서, 또는 특정 팀의 선택으로 이미 다른 프레임워크를 쓰고 있을 수 있다.

> **🚧 함정 박스 — reactivity 모델은 프레임워크마다 다르다**
>
> React에서 이직한 개발자가 Vue 코드베이스에 처음 들어갔을 때 가장 먼저 하는 실수는 React의 멘탈 모델을 그대로 가져오는 것이다. "상태가 바뀌면 컴포넌트 함수 전체가 다시 실행된다" — 이것이 React의 모델이다. Vue, Svelte, Solid는 이 모델이 전혀 다르다. 프레임워크를 바꿀 때 가장 먼저 revisit해야 하는 것이 바로 이 reactivity 모델이다.
>
> 반대 방향도 마찬가지다. Vue·Svelte에서 React로 오면 `ref`, `reactive`, `$:`가 없어서 불편하다. 그 불편함은 React가 덜 발전해서가 아니라, 설계 철학이 다르기 때문이다.

### Vue 3: Proxy 기반 reactivity

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface User {
  id: number
  name: string
  email: string
}

// ref: 원시값의 reactive 래퍼
const count = ref(0) // Ref<number>
const user = ref<User | null>(null) // Ref<User | null>

// computed: 파생 값 (의존성 자동 추적)
const displayName = computed(() => user.value?.name ?? '익명')

// watch: 값 변화에 반응
watch(count, (newVal, oldVal) => {
  console.log(`${oldVal} → ${newVal}`)
})

// .value로 접근 — React의 직접 접근과 다른 자리
count.value++
</script>

<template>
  <div>
    <p>{{ displayName }}</p>
    <p>{{ count }}</p>
    <button @click="count++">증가</button>
  </div>
</template>
```

Vue 3의 Composition API는 React Hooks와 표면적으로 비슷해 보이지만 동작 방식이 다르다. Vue는 JavaScript Proxy를 사용해 객체 접근을 가로채고, 값이 바뀔 때 구독된 컴포넌트만 업데이트한다. React처럼 컴포넌트 함수 전체를 다시 실행하지 않는다. `ref`의 `.value`로만 접근해야 하는 것이 React 개발자에게 처음에는 어색하다.

TypeScript 지원은 Vue 3 + `<script setup lang="ts">`로 잘 통합된다. `defineProps<T>()`, `defineEmits<T>()` 같은 컴파일러 매크로가 타입 안전한 props·events를 제공한다.

### Svelte 5: 컴파일 타임 reactivity (runes)

```svelte
<script lang="ts">
  // Svelte 5의 runes — 컴파일러가 처리한다
  let count = $state(0)        // 상태
  let doubled = $derived(count * 2)  // 파생 값

  // $effect는 useEffect와 비슷하지만 의존성 배열이 없다
  // Svelte 컴파일러가 어떤 상태를 읽는지 추적한다
  $effect(() => {
    console.log('count 변경:', count)
  })

  interface User {
    id: number
    name: string
  }

  let users: User[] = $state([])

  async function loadUsers() {
    const res = await fetch('/api/users')
    users = await res.json()
  }
</script>

<p>{count} (두 배: {doubled})</p>
<button onclick={() => count++}>증가</button>
```

Svelte의 가장 큰 차이는 **컴파일러가 reactivity를 처리한다**는 점이다. React처럼 런타임 라이브러리(`react`, `react-dom`)를 배포 번들에 포함할 필요가 없다. Svelte 컴파일러가 `$state`, `$derived`, `$effect` rune을 실제로 동작하는 JavaScript로 변환한다. 번들 크기가 작고 성능이 좋은 이유다.

TypeScript는 `lang="ts"` 하나로 지원된다. Svelte 5는 runes를 TypeScript와 함께 쓸 때 자연스럽게 타입이 추론된다.

### SolidJS: 가상 DOM 없는 signal

```tsx
import { createSignal, createEffect, createMemo, For } from 'solid-js'

interface Item {
  id: number
  text: string
}

function Counter() {
  // signal: [getter, setter] 쌍
  const [count, setCount] = createSignal(0)
  const doubled = createMemo(() => count() * 2)  // 파생 signal

  createEffect(() => {
    // count()를 읽으면 이 effect가 count에 구독됨
    console.log('count:', count())
  })

  return (
    <div>
      <p>{count()} (두 배: {doubled()})</p>
      {/* Solid에서는 값에 접근할 때 함수 호출 — React와 다름 */}
      <button onClick={() => setCount(c => c + 1)}>증가</button>
    </div>
  );
}
```

SolidJS는 JSX를 사용하지만 React와 전혀 다르게 동작한다. **컴포넌트 함수는 한 번만 실행된다**. React의 "상태가 바뀌면 컴포넌트 함수가 다시 실행된다"는 모델이 없다. 대신 signal의 getter(`count()`)를 JSX 안에서 호출하면 그 DOM 노드가 signal에 직접 구독된다. 값이 바뀌면 그 DOM 노드만 업데이트된다. 가상 DOM 없이 fine-grained reactivity를 구현한다.

성능 벤치마크에서 최상위를 기록하지만, 한국 시장에서의 채택률은 매우 낮다. 학습과 실험 목적으로 관심을 받고 있다.

> **📚 Java/Kotlin 시선 박스 ③ — Android Jetpack Compose ↔ React**
>
> Jetpack Compose를 알고 있다면 React의 재구성(recomposition) 모델과 비교하면 흥미롭다.
>
> Compose에서 상태가 바뀌면 해당 상태를 읽는 Composable 함수가 다시 실행된다(recomposition). React에서 상태가 바뀌면 해당 컴포넌트 함수와 하위 트리가 다시 실행된다(re-render). 기본 동작이 비슷하다.
>
> Compose의 `remember { mutableStateOf(0) }`는 React의 `useState(0)`에 대응하고, `LaunchedEffect`는 `useEffect`에 대응한다. `derivedStateOf`는 `useMemo`와 비슷하다.
>
> 핵심 차이는 Compose는 **smart recomposition** — 상태를 실제로 읽는 Composable만 재실행한다. React는 기본적으로 컴포넌트 트리 전체를 다시 실행하고 `React.memo`, `useMemo`, `useCallback`으로 최적화한다.
>
> SolidJS의 signal 모델은 Compose의 smart recomposition과 더 가깝다. 함수를 다시 실행하지 않고 signal을 읽는 DOM 노드만 업데이트한다.

### 한국 시장에서 언제 만나는가 — 결정 표

| 프레임워크 | 한국 시장 현황 | 만날 수 있는 상황 |
|---|---|---|
| **React** | 압도적 표준 | 거의 모든 신규 프론트 프로젝트 |
| **Vue 3** | 카카오·네이버 일부, 게임 회사 일부 | 2015~2020년 시작한 프로젝트 |
| **Vue 2** | 레거시 다수 | 마이그레이션 대상 |
| **Svelte** | 매우 드묾 | 개인 프로젝트, 일부 실험적 도입 |
| **SolidJS** | 거의 없음 | 학습·벤치마크 목적 |
| **Astro** | 드묾 | 콘텐츠 사이트, 기술 블로그 — 13장에서 다룬다 |

Vue 프로젝트를 만났을 때는 Composition API (`setup`) 기반인지 Options API 기반인지 먼저 확인하는 편이 낫다. Options API는 Vue 2 스타일이고 TypeScript 통합이 불편하다. `<script setup lang="ts">`가 보이면 Composition API + TypeScript의 현대적 방식이다.

다른 reactivity 모델로 이전이 필요할 때는 먼저 **멘탈 모델을 비운다**. React의 "렌더 = 함수 재실행"을 Vue·Solid에 그대로 가져오면 이해가 꼬인다. 각 프레임워크의 공식 문서 첫 장부터 다시 읽는 것이 가장 빠른 길이다.

---

## 마무리

React와 TypeScript가 만나는 지점은 생각보다 세밀하다. `forwardRef`의 제네릭 순서, `useRef`의 초기값 `null`이 갖는 의미, `as const`가 튜플 반환에 미치는 영향 — 이 작은 것들이 실무에서 막히는 자리다. 문서를 한 번 읽고 넘어갔을 때는 이해한 것 같지만, 처음 직접 컴포넌트 라이브러리를 설계할 때 다시 막히는 것이 이런 지점들이다.

`z.infer`가 폼 검증에서 단일 진실 원천이 되는 패턴, `useReducer`의 discriminated union이 Kotlin `sealed class`와 같은 역할을 하는 것, `forwardRef`로 캡슐화된 명령형 인터페이스를 노출하는 `useImperativeHandle` — 이 패턴들은 Java/Kotlin에서 온 개발자에게 낯설지 않은 개념이 TypeScript·React 방언으로 표현된 것이다.

Vue·Svelte·Solid가 다른 reactivity 모델을 갖고 있다는 것을 알고 있으면, 그 코드베이스를 처음 열었을 때 당황하지 않는다. 가상 DOM이 없어서가 아니라, 컴포넌트 함수가 한 번만 실행된다는 사실을 알고 있으면 Solid 코드가 이해된다. `.value`를 통해 접근해야 한다는 것을 알면 Vue의 `ref`가 낯설지 않다.

기억해두자 — 컴포넌트의 props 타입은 컴포넌트의 공개 계약이다. 이 계약을 명확하게 선언하는 것이 팀원과의 소통이고, 미래의 자신과의 소통이다.

---

> **📖 더 깊이 가려면**
>
> - React 컴포넌트의 테스트: Vitest + Testing Library + expect-type 패턴은 **14장**에서 자세히 다룬다. 컴포넌트의 타입이 올바른지를 타입 레벨에서 검증하는 `expect-type`의 활용, Testing Library의 쿼리 타입, Mock Service Worker를 통한 API 모킹 타입까지.
>
> - Next.js App Router의 Server Components·Server Actions 깊이: **13장** 풀스택 절에서 다룬다. RSC의 타입 경계, Server Actions의 `use server` 지시자, Astro의 Islands Architecture도 13장에서.
>
> - React Hook Form 공식 문서의 TypeScript 통합 가이드: https://react-hook-form.com/ts
>
> - zod 공식 문서 (schema 조합·변환): https://zod.dev
>
> - Total TypeScript의 React + TypeScript 패턴 시리즈: https://www.totaltypescript.com

---

> 12장에서 React + TypeScript의 핵심을 익혔다. 이제 서버 쪽으로 넘어오자. Spring 백엔드를 5년 넘게 짜온 개발자에게 "이번 프로젝트는 Node.js 백엔드로 갑니다"라는 말이 날아온다. NestJS, Hono, Express, Fastify, Next.js, Astro — 여섯 가지 길이 있다. 각 길의 철학이 다르고, 어느 길이 어떤 팀에 맞는지가 다르다. 13장에서 그 지형을 함께 걷자.

# 13장. 웹 백엔드와 풀스택 — Express·Fastify·Hono·NestJS·Next·Astro의 여섯 길

Spring 백엔드를 5년 넘게 짜온 개발자라고 해보자. 그에게 "이번 프로젝트는 Node.js 백엔드로 갑니다"라는 말이 날아온다. 손에 익은 `@RestController`, `@Service`, `@Repository` 패턴은 어디 갔나. `ApplicationContext`가 알아서 주입해주던 의존성은 이제 누가 관리하나. 처음에는 낯설고 막막하다. 그런데 NestJS 공식 문서를 열어본 순간 — 어, 이거 Spring 아닌가? `@Module`, `@Controller`, `@Injectable`, `@Inject`. 눈에 익은 어휘들이 줄지어 나온다.

그렇다면 NestJS는 정말 "Spring의 TS판"인가? 아, 거의 맞다. 하지만 "거의"라는 단어가 굉장히 중요하다. 모양이 비슷해서 자신감을 갖고 뛰어들었다가 예상 밖의 자리에서 발이 걸리면 그때의 당혹감이 더 크다. 이 챕터는 그 "거의"의 안쪽을 정직하게 들여다보는 챕터다.

동시에 이 챕터는 NestJS 한 가지만 이야기하지 않는다. Spring 베테랑이 익숙함을 찾아 NestJS로 첫 발을 딛는 길 외에, 전혀 다른 철학으로 설계된 Hono라는 길이 있다. 타입이 라우트 정의 시점부터 자동으로 흘러나와 RPC 클라이언트까지 자동 생성되는 그 마법 — 5장의 "타입을 만드는 타입"이 현실 코드에서 어떻게 살아남는지가 여기서 드러난다. 그리고 Express와 Fastify는 여전히 현장의 표준으로 버티고 있으며, Next.js를 비롯한 풀스택 메타프레임워크는 "백엔드와 프론트엔드의 경계"라는 오래된 질문을 새로 제기하고 있다.

여섯 길을 걸어보자. 어떤 길이 당신 팀에 맞는지 — 그 판단을 이 챕터에서 가져갈 수 있길 바란다.

---

## NestJS — Spring 베테랑의 환영

### 1:1 대응이 진짜인 자리

솔직히 말하면, NestJS의 첫인상은 Spring 개발자에게 상당히 친절하다. 단순히 느낌이 비슷한 게 아니라 실제로 1:1 대응이 성립하는 영역이 넓다. 코드를 나란히 놓고 보는 게 가장 빠르다.

---

📚 **Java/Kotlin 시선 ① — Spring `@RestController` ↔ NestJS `@Controller`**

```java
// Spring
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserDto> createUser(@RequestBody @Valid CreateUserRequest req) {
        return ResponseEntity.status(201).body(userService.create(req));
    }
}
```

```typescript
// NestJS
@Controller('users')
export class UserController {
    constructor(private readonly userService: UserService) {}

    @Get(':id')
    getUser(@Param('id') id: string): Promise<UserDto> {
        return this.userService.findById(id);
    }

    @Post()
    @HttpCode(201)
    createUser(@Body() req: CreateUserDto): Promise<UserDto> {
        return this.userService.create(req);
    }
}
```

데코레이터 이름, 파라미터 추출 방식, 의존성 주입 — 패턴이 거의 동일하다. Spring 백엔드 경험자라면 이 코드를 처음 봐도 뜻을 읽는 데 10초도 걸리지 않는다. NestJS가 Spring·Angular의 설계 철학을 의도적으로 차용했다는 점은 공식 문서에도 명시되어 있다.

서비스 계층과 주입 방식도 마찬가지다.

```java
// Spring
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public UserDto findById(Long id) { ... }
}
```

```typescript
// NestJS
@Injectable()
export class UserService {
    constructor(
        @InjectRepository(User)
        private readonly userRepository: Repository<User>
    ) {}

    findById(id: string): Promise<UserDto> { ... }
}
```

`@Service` ↔ `@Injectable`. `@Autowired` ↔ 생성자 주입. 구조가 1:1이다. 심지어 `@Module`이 Spring의 `@Configuration`+`@ComponentScan` 역할을 한다는 것까지.

```typescript
@Module({
    imports: [TypeOrmModule.forFeature([User])],
    controllers: [UserController],
    providers: [UserService],
    exports: [UserService],       // ← 이 줄이 핵심 차이점
})
export class UserModule {}
```

---

### Spring과 다른 의외의 자리

1:1 대응이 안심을 주다가, 막상 실제 코드를 짜면 생각지 못한 곳에서 발이 걸린다. 이런 자리를 미리 알아두면 입사 첫 달의 시행착오를 상당히 줄일 수 있다.

**첫 번째: 모듈 명시 등록 vs Spring component scan**

Spring에서는 `@ComponentScan`이 지정된 패키지 아래를 자동으로 스캔해서 `@Component`, `@Service`, `@Repository`를 가진 클래스를 찾아 빈으로 등록한다. 별도로 "이 서비스를 이 컨트롤러에 연결하겠다"고 선언할 필요가 없다. 패키지 구조만 맞으면 자동이다.

NestJS는 다르다. 모든 프로바이더는 해당 모듈의 `providers` 배열에 명시적으로 등록해야 한다. 그리고 모듈 밖에서 쓰려면 `exports` 배열에도 추가해야 한다. 처음에 이게 번거로워 보인다. 그런데 사실 이 명시성이 장점이다 — 의존성 그래프가 모듈 파일만 봐도 보인다.

---

📚 **Java/Kotlin 시선 ② — Spring component scan ↔ NestJS Module 재구성**

```java
// Spring — @ComponentScan 범위 안에 있으면 자동 등록
@SpringBootApplication  // @ComponentScan 포함
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// UserService가 같은 패키지 트리에 있으면 자동 발견됨
@Service
public class UserService { ... }
```

```typescript
// NestJS — 모듈에 명시적으로 등록해야 함
@Module({
    providers: [UserService],   // 이 줄이 없으면 DI 컨테이너에 없음
    controllers: [UserController],
    exports: [UserService],     // 다른 모듈이 쓰려면 이 줄도 필요
})
export class UserModule {}

// AppModule에서 UserModule을 imports에 넣어야 함
@Module({
    imports: [UserModule, AuthModule],
})
export class AppModule {}
```

Spring 베테랑이 처음 NestJS에서 만나는 난감한 에러 중 하나가 "Nest can't resolve dependencies of the XService"다. 열심히 `@Injectable()`을 붙였는데 왜? 라며 30분을 날린다. 답은 항상 모듈 `providers` 배열에 등록을 빠뜨렸거나, 다른 모듈의 서비스를 `exports`하지 않았기 때문이다.

---

**두 번째: Module re-export 모델**

NestJS의 모듈은 다른 모듈을 imports한 뒤 그것을 다시 exports할 수 있다. 이걸 module re-export라고 한다.

```typescript
@Module({
    imports: [TypeOrmModule.forFeature([User, Post])],
    providers: [UserService, PostService],
    exports: [
        UserService,
        TypeOrmModule,  // ← TypeOrmModule 자체를 re-export
    ],
})
export class CoreModule {}

// CoreModule을 import하는 모듈은 TypeOrmModule도 같이 받는다
@Module({
    imports: [CoreModule],  // UserService와 TypeOrmModule이 함께 들어옴
})
export class FeatureModule {}
```

Spring에는 이런 개념이 없다. Spring에서는 빈이 애플리케이션 컨텍스트 전체에 공유된다. NestJS에서는 모듈 경계가 DI 스코프를 나눈다 — 그래서 "어느 모듈이 어떤 모듈을 볼 수 있는가"를 모듈 파일을 보면 명시적으로 알 수 있다는 이점이 생긴다.

**세 번째: Exception Filter의 결**

Spring에서는 `@ControllerAdvice` + `@ExceptionHandler`로 전역 예외를 처리한다. NestJS에는 `ExceptionFilter`가 있다. 원리는 비슷하지만 등록 방식이 다르다.

```typescript
// NestJS Exception Filter
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
    catch(exception: HttpException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const status = exception.getStatus();

        response.status(status).json({
            statusCode: status,
            message: exception.message,
            timestamp: new Date().toISOString(),
        });
    }
}

// 등록 방식 세 가지
// 1. 컨트롤러 레벨
@UseFilters(new HttpExceptionFilter())
export class UserController {}

// 2. 메서드 레벨
@Get(':id')
@UseFilters(HttpExceptionFilter)
getUser(@Param('id') id: string) {}

// 3. 전역 (main.ts)
app.useGlobalFilters(new HttpExceptionFilter());
```

Spring의 `@ControllerAdvice`는 클래스 하나로 모든 컨트롤러에 적용된다. NestJS는 전역·모듈·컨트롤러·메서드 네 단계 스코프를 선택할 수 있다. 세밀하지만, 처음에는 "어디에 등록해야 하는 거지?" 하는 당혹감이 있다.

**네 번째: Pipe vs Filter — Guard까지**

Spring에는 `HandlerInterceptor`, `OncePerRequestFilter`, `@PreAuthorize` 같은 인터셉터/필터/보안 어노테이션이 있다. NestJS에는 이를 대응하는 개념이 다섯 가지로 나뉜다.

| NestJS 개념 | 역할 | Spring 대응 |
|---|---|---|
| Guard | 인증·인가 — 요청을 허용할지 결정 | `@PreAuthorize` / Security Filter |
| Pipe | 입력 변환·검증 | `@Valid` + Converter |
| Interceptor | 요청·응답 가로채기 | `HandlerInterceptor` |
| Exception Filter | 예외를 HTTP 응답으로 변환 | `@ExceptionHandler` / `@ControllerAdvice` |
| Middleware | Express 미들웨어와 동일 | Servlet Filter |

Spring에서 하나의 개념(`Filter`, `Interceptor`)이 하던 일을 NestJS가 다섯으로 분리했다고 이해하면 된다. 실수하기 쉬운 자리는 "이 로직은 Guard인가 Interceptor인가"다 — 인가(authorization)는 Guard, 로깅·응답 가공은 Interceptor로 가는 편이 낫다.

**다섯 번째: Provider Scope**

Spring의 빈은 기본이 싱글톤이다. NestJS도 기본은 싱글톤이다 — 여기까진 같다. 그런데 NestJS는 `REQUEST` 스코프와 `TRANSIENT` 스코프를 지원한다.

```typescript
// REQUEST 스코프 — 각 요청마다 새 인스턴스
@Injectable({ scope: Scope.REQUEST })
export class RequestScopedService {}

// TRANSIENT 스코프 — 주입될 때마다 새 인스턴스
@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}
```

함정이 있다. `REQUEST` 스코프 프로바이더를 싱글톤 프로바이더에 주입하면 싱글톤이 REQUEST 스코프 프로바이더를 고정 참조하게 되어 의도대로 동작하지 않는다. 이런 scope propagation 문제는 Spring에도 존재하지만, NestJS에서는 에러 메시지가 덜 친절한 편이라 디버깅이 번거롭다.

---

🚧 **함정 박스 — 데코레이터 두 종류 혼동**

**증상**: `@Inject()`, `@Injectable()` 같은 데코레이터를 쓰는데 "Experimental support for decorators is a feature that is subject to change"라는 경고가 뜨거나, tsconfig 설정을 아무리 건드려도 런타임 에러가 난다. 또는 새 프로젝트에 NestJS를 설치했는데 `reflect-metadata`를 import하지 않으면 동작하지 않는다.

**원인**: TypeScript의 데코레이터는 현재 두 종류가 공존한다.
- **Legacy 데코레이터** (`experimentalDecorators: true`): NestJS·TypeORM·class-validator가 의존하는 구버전. 런타임 메타데이터를 쓰기 위해 `emitDecoratorMetadata: true`와 `reflect-metadata` 라이브러리가 함께 필요하다.
- **TC39 Stage 3 데코레이터** (TS 5.0+): ECMAScript 표준 제안에 정렬된 신버전. 메타데이터 reflection API가 별도 제안(Decorator Metadata)으로 분리되어 있으며, NestJS가 의존하는 `reflect-metadata`와 호환되지 않는다.

TS 5.0 릴리즈 노트는 명시적으로 "we've decided to make a hard pivot to the new decorators proposal"이라고 선언했다. 그런데 NestJS는 여전히 legacy 데코레이터를 사용한다. 새 표준으로의 마이그레이션이 NestJS 아키텍처 전체를 바꾸는 작업이기 때문이다.

**처방**: NestJS 프로젝트라면 tsconfig에서 반드시 `"experimentalDecorators": true`와 `"emitDecoratorMetadata": true`를 유지하고, `main.ts` 또는 진입 파일 최상단에 `import 'reflect-metadata'`를 두어야 한다. 새 TC39 데코레이터와 혼용하지 말 것. 새 프로젝트에서 NestJS를 도입할 때는 `@nestjs/cli`가 생성하는 기본 tsconfig를 그대로 쓰는 편이 안전하다.

---

### Spring 시니어가 처음 만났을 때 헷갈리는 5가지

이 다섯 가지를 미리 알면 입사 첫 달이 달라진다.

**① 모듈 등록 빠뜨리기** — "Nest can't resolve dependencies" 에러의 99%는 `providers`나 `exports`에 빠진 항목이 있어서다. 에러가 나면 먼저 모듈 파일을 보자.

**② 순환 의존성** — A 모듈이 B 모듈을 import하고 B 모듈이 A 모듈을 import하면 NestJS가 시작 시 에러를 낸다. `forwardRef(() => BModule)` 패턴으로 해결하지만, 이게 필요해졌다는 것은 모듈 분리가 잘못됐다는 신호이기도 하다. Spring에서는 같은 상황에 `@Lazy`를 쓰거나 구조를 재설계했을 것이다.

**③ `async` 프로바이더와 초기화 순서** — 비동기로 초기화해야 하는 프로바이더(예: DB 커넥션 확인)는 `useFactory`와 `async/await`를 조합한 async provider 패턴을 써야 한다. Spring의 `@PostConstruct`나 `InitializingBean`과 비슷하지만, 실수로 `async`를 빠뜨리면 초기화 전에 요청이 들어와 난감한 상황이 생긴다.

**④ Guard와 Interceptor의 실행 순서** — Middleware → Guard → Interceptor(before) → Pipe → Controller → Interceptor(after) → Exception Filter 순서다. Spring의 Filter → Interceptor(preHandle) → Controller → Interceptor(postHandle) → Filter(after) 순서와 비슷하지만 이름과 계층이 달라 헷갈린다. Pipe가 Guard 이후에 실행된다는 점 — 즉, 인가가 먼저 통과된 후에 입력 검증이 된다는 점 — 이 의외로 중요하다.

**⑤ `@Param()`, `@Body()`, `@Query()` 데코레이터 타입** — NestJS의 `@Param('id')`는 항상 `string`을 반환한다. Spring의 `@PathVariable Long id`처럼 자동 형변환이 없다. `parseInt(id)`를 직접 하거나, `ParseIntPipe`를 함께 쓰는 패턴을 알아야 한다.

```typescript
// 타입 변환을 Pipe에 위임하는 패턴
@Get(':id')
getUser(@Param('id', ParseIntPipe) id: number): Promise<UserDto> {
    return this.userService.findById(id);
}
```

---

### NestJS의 legacy decorator 미래 — 어디로 가는가

솔직히 이 부분은 커뮤니티에서도 의견이 갈린다. NestJS가 TC39 신규 표준 데코레이터로 마이그레이션할 수 있을까?

기술적 난관이 있다. 신규 데코레이터 표준은 `reflect-metadata`가 제공하는 런타임 메타데이터 API와 호환되지 않는다. NestJS의 DI 컨테이너, class-validator의 `@IsString()`, TypeORM의 `@Column()`은 모두 이 메타데이터에 의존한다. 메타데이터 reflection을 위한 별도 TC39 제안(Decorator Metadata)이 있지만, 아직 표준이 완전히 자리를 잡지 않았다.

낙관론자는 "결국 이전한다, 시간 문제"라고 말한다. 비관론자는 "구조 전체를 바꿔야 하는데, NestJS가 그 비용을 감당하려면 결국 다른 아키텍처로 가야 한다"고 말한다. 2025년 현재의 현실적인 답은: **NestJS는 당분간 legacy 데코레이터 위에 머문다.** `experimentalDecorators` 모드는 TS 팀이 유지하겠다고 밝혔으므로, 기존 NestJS 코드베이스는 그대로 동작한다. 신규 프로젝트에 NestJS를 도입할 때 이 점을 인지하고 선택하는 편이 낫다.

---

### DI 컨테이너 비교 — NestJS vs InversifyJS vs tsyringe

NestJS가 아닌 환경에서 DI가 필요할 때는 선택지가 있다.

| | NestJS | InversifyJS | tsyringe |
|---|---|---|---|
| 철학 | 프레임워크 내장 DI | 독립 DI 컨테이너 | 경량 DI 컨테이너 |
| Spring 비유 | Spring DI + 프레임워크 | Guice | Dagger (가벼운 쪽) |
| 데코레이터 | legacy `experimentalDecorators` | legacy | legacy |
| 메타데이터 | `reflect-metadata` 의존 | `reflect-metadata` 의존 | `reflect-metadata` 의존 |
| 학습 곡선 | 가파름 (모듈 체계 이해 필요) | 중간 | 완만 |
| 사용 맥락 | 백엔드 풀프레임워크 | 복잡한 독립 앱, CLI | 간단한 DI 필요 시 |

InversifyJS는 Spring보다 Guice에 가깝다 — 바인딩을 명시적으로 선언하고, 컨테이너에서 해결(resolve)하는 패턴이다. Spring의 자동 와이어링에 비하면 조금 더 명시적이고, NestJS의 모듈 체계보다 가볍다. Express나 Fastify와 함께 DI만 붙이고 싶을 때 선택지가 된다.

---

## Hono — 타입이 흐르는 Web Standards 서버

### 5장의 마법이 현실이 되는 자리

5장에서 `infer`, mapped types, 조건부 타입을 배울 때 "이게 실제로 어디에 쓰이는 거지?"라는 의문이 생겼다면, Hono가 그 답 중 하나다. Hono의 라우터는 라우트 정의 시점부터 응답 타입이 자동으로 추론되어 흐른다 — 그리고 그 타입을 바탕으로 RPC 클라이언트가 자동으로 만들어진다.

어떻게 동작하는지 부품 단위로 분해해보자.

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// 라우트 정의 — 이 시점에서 타입 정보가 캡처됨
const routes = app
    .get('/users/:id', async (c) => {
        const id = c.req.param('id')  // string으로 추론됨
        const user = await findUser(id)
        return c.json({ id: user.id, name: user.name })
        //      ↑ 반환 타입이 자동 추론됨
    })
    .post('/users',
        zValidator('json', z.object({
            name: z.string(),
            email: z.string().email(),
        })),
        async (c) => {
            const body = c.req.valid('json')
            // body의 타입이 { name: string, email: string }으로 추론됨
            const user = await createUser(body)
            return c.json(user, 201)
        }
    )

export type AppType = typeof routes
// AppType에 모든 라우트의 입력·출력 타입이 인코딩되어 있음
```

이 `AppType`이 핵심이다. 각 라우트의 URL 패턴, HTTP 메서드, 요청 바디 타입, 응답 타입이 모두 타입 레벨에서 인코딩된다. 5장에서 본 매핑 타입과 조건부 타입이 내부적으로 이 정보를 추출한다.

### RPC 클라이언트 자동 생성

`AppType`을 클라이언트 코드로 가져오면 타입 안전한 HTTP 클라이언트가 자동으로 생성된다.

```typescript
// 클라이언트 코드 (프론트엔드 또는 다른 서비스)
import { hc } from 'hono/client'
import type { AppType } from './server'  // 타입만 가져옴 — 런타임 코드 없음

const client = hc<AppType>('http://localhost:3000')

// 이 시점에서 타입 추론이 완전히 동작함
const response = await client.users[':id'].$get({
    param: { id: '123' },
})

const data = await response.json()
// data의 타입: { id: string, name: string }
// ↑ 서버의 c.json({ id, name }) 반환 타입에서 자동 유도됨

// 존재하지 않는 라우트를 쓰면 컴파일 에러
const wrong = await client.posts.$get()  // ← 에러: 'posts' 라우트 없음
```

이게 왜 새로운가? 기존의 REST API 연동 방식을 생각해보자. 서버에서 API 스펙을 OpenAPI로 뽑고, 클라이언트에서 그 스펙을 바탕으로 SDK를 생성하거나 직접 타입을 작성한다. 서버가 응답 타입을 바꾸면 클라이언트도 직접 수정해야 한다. 그 간극에서 버그가 난다.

Hono의 RPC 모델은 그 간극을 없앤다. 서버와 클라이언트가 같은 타입 정보를 공유하기 때문에, 서버에서 응답 타입이 바뀌면 클라이언트에서 즉시 컴파일 에러가 난다. 타입이 계약이 되는 순간이다.

---

📚 **Java/Kotlin 시선 ⑤ — Spring WebFlux ↔ Hono async**

```java
// Spring WebFlux — Reactor 기반 비동기
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{id}")
    public Mono<UserDto> getUser(@PathVariable String id) {
        return userService.findById(id)
            .map(user -> new UserDto(user.getId(), user.getName()));
    }
}
```

```typescript
// Hono — async/await 기반, Web Standards Fetch API
app.get('/users/:id', async (c) => {
    const id = c.req.param('id')
    const user = await userService.findById(id)
    return c.json({ id: user.id, name: user.name })
})

// c.req, c.res가 Web Standards의 Request, Response를 따름
// Spring의 ServerRequest/ServerResponse와 개념은 비슷하지만
// Web Standards이므로 Cloudflare Workers, Deno, Bun에서도 동일하게 동작함
```

Spring WebFlux는 Reactor(`Mono`/`Flux`) 위에서, Hono는 표준 Promise 위에서 비동기를 처리한다. 두 모델 모두 비동기 요청을 블로킹 없이 처리하지만, 표현 방식이 다르다. Hono의 `async/await`는 Kotlin coroutine의 `suspend`와 표면적으로 가깝다 — 동기 코드처럼 읽힌다.

핵심 차이는 **Web Standards 기반**이다. Hono의 `c.req`는 Web Standards `Request` 객체, `c.res`는 `Response` 객체다. 이 표준은 브라우저·Node.js·Bun·Deno·Cloudflare Workers에서 동일하다. 코드 한 벌을 여러 런타임에 배포할 수 있다는 뜻이다.

---

### 전 런타임 동작 — Adapter 모델

Hono가 "Web Standards 기반"을 강조하는 이유가 여기 있다. Node.js의 `http` 모듈 API, Bun의 내장 서버 API, Cloudflare Workers의 실행 환경은 각각 다르다. 하지만 모두 Web Standards의 `Request`/`Response`를 지원한다. Hono는 이 공통 분모 위에 서 있기 때문에 런타임마다 어댑터 한 줄만 바꾸면 된다.

```typescript
// Node.js
import { serve } from '@hono/node-server'
serve({ fetch: app.fetch, port: 3000 })

// Bun
export default app  // Bun이 fetch 핸들러를 자동 인식

// Cloudflare Workers
export default app  // Workers 환경에서 동일하게 동작

// Deno
Deno.serve(app.fetch)
```

서버 코드 자체(`app.get(...)` 부분)는 바뀌지 않는다. 이 패턴은 Spring Boot가 내장 톰캣·제티·언더토우를 바꾸는 방식과 비슷하게 느껴지지만, 실제로는 더 가볍다 — 프레임워크가 플랫폼 추상화 계층 없이 표준 API 위에 바로 서 있기 때문이다.

### tRPC와의 차이점

Hono RPC와 tRPC를 비교하는 질문이 자주 나온다. 두 가지 모두 타입 안전한 API를 만드는 도구지만 철학이 다르다.

| | Hono RPC | tRPC |
|---|---|---|
| 전송 방식 | 표준 HTTP (GET, POST, DELETE...) | HTTP POST 기반 (또는 WebSocket) |
| REST 호환 | 완전 호환 — OpenAPI 스펙 자동 생성 가능 | REST가 아님 — tRPC 클라이언트 필요 |
| 적합한 상황 | 외부 공개 API, 모바일 클라이언트 있는 경우 | 동일 타입 코드베이스 내 웹 풀스택 |
| 런타임 | Web Standards 기반 전 런타임 | Node.js 중심 |
| 학습 곡선 | 낮음 (일반 라우터와 비슷) | 중간 (procedure, router 개념 필요) |

외부에 API를 열어야 하거나 모바일 클라이언트가 있다면 Hono RPC가 낫다 — REST 호환이기 때문이다. 단일 Next.js 풀스택 앱에서 프론트엔드와 백엔드만 연결한다면 tRPC가 더 자연스럽다. T3 스택이 tRPC를 기본 선택으로 두는 이유다.

---

## Express + Fastify — 여전히 현장의 표준

### Express: 왜 여전히 1위인가

JetBrains Developer Ecosystem 2024 기준으로 Node.js 백엔드 프레임워크 점유에서 Express가 여전히 1위다. 2010년에 나온 프레임워크가 2025년에도 1위라는 것이 어떤 의미인가.

답은 관성이 아니라 신뢰다. Express는 수천만 개의 npm 패키지가 "Express 미들웨어"로 만들어져 있다. 새 인증 라이브러리, 새 파일 업로드 라이브러리, 새 로깅 솔루션 — 대부분이 Express 미들웨어를 먼저 만든다. 이 생태계 규모는 단기간에 따라잡기 어렵다.

Express 자체는 매우 미니멀하다. 라우팅, 미들웨어 체인, 요청/응답 객체. 그 이상은 직접 선택한다.

```typescript
import express from 'express'
import { Request, Response, NextFunction } from 'express'

const app = express()
app.use(express.json())

// 기본 라우트 — 타입 추론이 제한적
app.get('/users/:id', async (req: Request, res: Response) => {
    const id = req.params.id  // string
    // req.params, req.query, req.body 모두 타입이 느슨하다
    // 이 느슨함이 Express TS 사용의 찜찜한 자리
    const user = await findUser(id)
    res.json(user)
})

// 미들웨어 패턴
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    console.error(err.stack)
    res.status(500).json({ message: err.message })
})

app.listen(3000)
```

Express의 TS 지원에서 찜찜한 부분이 있다. `req.body`는 기본적으로 `any`다. `req.params`는 `string` 딕셔너리지만, 라우트 URL에 정의한 파라미터 이름과 연결되지 않는다. 이 느슨함을 보완하려면 제네릭을 명시하거나, zod로 검증하거나, 별도의 미들웨어 레이어를 만들어야 한다.

```typescript
// 타입을 조금 더 안전하게 쓰는 패턴
import { z } from 'zod'

const userParamSchema = z.object({ id: z.string() })
const createUserSchema = z.object({
    name: z.string(),
    email: z.string().email(),
})

app.post('/users', async (req: Request, res: Response) => {
    const body = createUserSchema.parse(req.body)
    // 이제 body가 { name: string, email: string }으로 좁혀짐
    const user = await createUser(body)
    res.status(201).json(user)
})
```

Express 4.x는 오랫동안 유지보수 중이었고, 2024년에 Express 5.x가 정식 릴리즈됐다. Promise 기반 라우터, 비동기 에러 핸들러 자동 처리 등이 개선됐지만, 큰 아키텍처 변화는 없다.

### Fastify: Express의 후계자 지위

Fastify는 Express의 느슨한 타입과 성능 문제를 직접 겨냥하며 설계됐다. Node.js 코어 팀원인 Matteo Collina가 주도하며 만든 이 프레임워크는 두 가지 방향에서 Express보다 강하다.

**첫째, JSON Schema 기반 검증과 직렬화.** Fastify는 라우트 스키마를 JSON Schema로 정의하면 요청 검증과 응답 직렬화를 동시에 처리한다. 응답 직렬화를 스키마 기반으로 하기 때문에 JSON 생성 성능이 크게 좋다.

```typescript
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from '@sinclair/typebox'

const fastify = Fastify().withTypeProvider<TypeBoxTypeProvider>()

fastify.get('/users/:id', {
    schema: {
        params: Type.Object({ id: Type.String() }),
        response: {
            200: Type.Object({
                id: Type.String(),
                name: Type.String(),
                email: Type.String(),
            }),
        },
    },
}, async (request, reply) => {
    const { id } = request.params
    // id가 string으로 정확히 추론됨 — TypeBox 스키마에서 유도
    const user = await findUser(id)
    return user  // 응답 스키마에 맞게 직렬화됨
})
```

TypeBox를 쓰면 JSON Schema와 TS 타입을 동시에 정의할 수 있다. 검증·직렬화·타입 추론이 단일 소스에서 나온다. 이 패턴은 zod + Hono의 방향과 비슷하지만, Fastify는 표준 JSON Schema를 기반으로 해서 OpenAPI 스펙 자동 생성이 더 자연스럽다.

**둘째, 플러그인 시스템.** Fastify의 플러그인은 캡슐화된 스코프를 가진다. Express의 `app.use()`가 전역 미들웨어를 쌓는 방식과 달리, Fastify 플러그인은 자신의 스코프에서만 동작하는 데코레이터·훅·플러그인을 등록할 수 있다. NestJS의 모듈과 비슷한 캡슐화 개념이다.

두 프레임워크를 어떻게 고르는가. 기존 Express 생태계(미들웨어, 레거시 코드)와의 호환이 최우선이라면 Express를 유지하는 편이 낫다. 새 프로젝트이고 타입 안전과 성능이 중요하다면 Fastify가 더 나은 선택이다. NestJS는 Fastify를 HTTP 어댑터로 쓸 수 있다 — `@nestjs/platform-fastify`로 바꾸면 NestJS의 DI·모듈 체계를 유지하면서 Fastify의 성능을 얻는다.

---

📚 **Java/Kotlin 시선 ④ — Bean Validation `@Valid` ↔ zod**

```java
// Spring — 클래스 필드에 어노테이션으로 검증 규칙 선언
public class CreateUserRequest {
    @NotBlank
    @Size(max = 100)
    private String name;

    @Email
    @NotNull
    private String email;

    @Min(0) @Max(150)
    private int age;
}

@PostMapping("/users")
public ResponseEntity<UserDto> createUser(
    @RequestBody @Valid CreateUserRequest req,
    BindingResult result
) {
    if (result.hasErrors()) {
        throw new ValidationException(result.getAllErrors());
    }
    ...
}
```

```typescript
// TS — zod 스키마가 타입 정의와 검증 규칙을 동시에 표현
import { z } from 'zod'

const createUserSchema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150),
})

type CreateUserRequest = z.infer<typeof createUserSchema>
// { name: string, email: string, age: number }

// Express에서 직접 검증
app.post('/users', async (req, res) => {
    const result = createUserSchema.safeParse(req.body)
    if (!result.success) {
        return res.status(400).json({ errors: result.error.flatten() })
    }
    const user = await createUser(result.data)
    res.status(201).json(user)
})
```

Bean Validation은 클래스에 검증 어노테이션을 달고 Spring이 런타임에 실행한다 — 런타임 메타데이터 의존이다. zod는 스키마 객체를 직접 호출하는 방식이다. `z.infer<typeof schema>`가 타입을 유도하는 것이 5장의 조건부 타입이 현실에서 쓰이는 핵심 사례다. NestJS에서는 `class-validator`와 `class-transformer`로 Spring과 더 비슷한 패턴을 쓸 수 있지만, 커뮤니티의 방향은 zod 쪽으로 기울고 있다.

---

## 풀스택 메타프레임워크 — 철학의 지형도

### Next.js와 RSC — 서버가 돌아온다

Next.js App Router와 React Server Components(RSC)의 등장은 "프론트엔드와 백엔드의 경계"라는 오래된 구분을 다시 흔들고 있다. 어떻게?

기존 SPA 모델을 생각해보자. 프론트엔드는 정적 파일로 배포하고, 백엔드 API를 호출해 데이터를 가져온다. BFF(Backend for Frontend) 패턴이 필요해지면 별도 서버를 두거나 API Gateway를 끼워 넣는다.

Next.js App Router에서는 컴포넌트 자체가 서버에서 실행될 수 있다.

```typescript
// app/users/[id]/page.tsx — 서버 컴포넌트 (기본)
// 이 파일은 서버에서 실행됨 — DB 직접 호출 가능
async function UserPage({ params }: { params: { id: string } }) {
    // DB를 직접 호출한다 — API 레이어 없음
    const user = await db.user.findUnique({
        where: { id: params.id },
    })

    if (!user) notFound()

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    )
}
```

```typescript
// app/users/[id]/actions.ts — Server Action
'use server'  // 이 지시어가 있으면 서버에서만 실행됨

export async function updateUser(id: string, data: UpdateUserData) {
    // 폼 제출 → 서버 함수 직접 호출 — fetch 없음
    await db.user.update({ where: { id }, data })
    revalidatePath(`/users/${id}`)
}

// 클라이언트 컴포넌트에서 사용
'use client'
import { updateUser } from './actions'

function EditUserForm({ userId }: { userId: string }) {
    return (
        <form action={updateUser.bind(null, userId)}>
            {/* 폼이 서버 함수를 직접 호출 */}
        </form>
    )
}
```

Server Actions는 PHP의 `<form action="process.php">`와 비슷하게 느껴지기도 한다. 실제로 Dan Abramov는 "서버 우선 개발의 부활"이라고 표현했다. 이 방식이 BFF를 사라지게 만드는가?

단일 웹 클라이언트만 있는 서비스라면 Next.js 풀스택으로 BFF를 대체할 수 있다. 그러나 모바일 앱이 있거나, 파트너 API를 열어야 하거나, 여러 클라이언트가 같은 API를 써야 한다면 여전히 별도 API 서버가 필요하다. 풀스택 메타프레임워크는 "웹 한정"의 해법이다 — 이 제약을 인지하고 선택하는 편이 낫다.

### React Router 7 (구 Remix) — Web Standards의 길

React Router 7은 Remix가 React Router와 통합되면서 나온 메타프레임워크다. Next.js와 다른 철학을 가진다.

| | Next.js App Router | React Router 7 |
|---|---|---|
| 데이터 패턴 | Server Components + Server Actions | loader/action 패턴 |
| 표준 준수 | React 전용 (RSC) | Web Standards (FormData, Response) |
| 서버 렌더링 | RSC 우선 | SSR/SSG 선택 |
| 데이터 뮤테이션 | Server Actions | `action` 함수 |
| 캐싱 전략 | 복잡 (세 종류) | 단순 |

React Router 7의 loader/action 패턴은 Web Standards(`Request`, `Response`, `FormData`)를 직접 다루기 때문에, 브라우저 폼의 동작 방식에 충실하다. Spring MVC의 controller 메서드가 `HttpServletRequest`를 직접 다루는 방식과 닮았다.

```typescript
// React Router 7 — route loader
export async function loader({ params }: LoaderFunctionArgs) {
    const user = await db.user.findUnique({
        where: { id: params.id },
    })
    if (!user) throw new Response('Not Found', { status: 404 })
    return { user }
}

// route action — 폼 제출 처리
export async function action({ request, params }: ActionFunctionArgs) {
    const formData = await request.formData()
    const name = formData.get('name') as string
    await db.user.update({
        where: { id: params.id },
        data: { name },
    })
    return redirect(`/users/${params.id}`)
}
```

### SvelteKit · Solid Start — 다른 reactivity의 풀스택

SvelteKit은 Svelte의 컴파일 타임 reactivity 위에 서버 렌더링·파일 기반 라우팅·폼 액션을 얹는다. 코드가 간결하고 번들이 작다는 것이 강점이다. Solid Start는 fine-grained reactivity(signal 기반) 위의 풀스택이다. 한국 시장에서 두 프레임워크의 비중은 아직 높지 않다 — 업무에서 만날 확률이 낮다. 하지만 기술적 방향의 다양성을 파악하는 차원에서 인지하는 것이 낫다.

### Astro — 콘텐츠 사이트 풀스택의 자리

Astro는 12장에서 잠깐 언급되었지만, 여기 13장이 더 자연스러운 자리다. Astro의 핵심 개념인 Islands Architecture는 reactivity 모델이 아니라 **콘텐츠 사이트 풀스택 hydration 전략**이기 때문이다.

아이디어는 단순하다. 콘텐츠 중심 사이트(블로그, 문서, 마케팅 페이지)의 대부분은 정적 HTML로 충분하다. 인터랙티브한 부분은 극히 일부 — 검색 바, 댓글 폼, 슬라이더. Islands Architecture는 이 "극히 일부"에만 JS를 hydrate하고, 나머지는 정적 HTML로 낸다.

```astro
---
// Astro 컴포넌트 — 서버에서만 실행되는 부분
import { getPost } from '../lib/posts'
const post = await getPost(Astro.params.slug)
---

<html>
<body>
    <!-- 정적 콘텐츠 — JS 없음 -->
    <h1>{post.title}</h1>
    <article>{post.content}</article>

    <!-- 인터랙티브 섬(Island) — React 컴포넌트를 hydrate -->
    <CommentForm client:load postId={post.id} />
    {/*         ↑ client:load로 이 컴포넌트만 JS를 실행 */}
</body>
</html>
```

Astro는 React, Vue, Svelte, Solid 컴포넌트를 동시에 섞어 쓸 수 있다. 다양한 라이브러리의 컴포넌트를 하나의 페이지에서 쓸 수 있는 "프레임워크 불가지론자"다.

어떤 상황에서 Astro를 쓰는가. 콘텐츠가 주인공이고 인터랙션이 보조인 사이트 — 기술 문서, 블로그, 마케팅 사이트, 전자상거래 상품 페이지. Next.js나 React Router는 SPA를 서버에서 렌더링하는 방향이라면, Astro는 "기본이 정적"인 방향이다. 성격이 다른 도구를 비교하는 것은 큰 의미가 없다.

---

### T3 스택 — 타입 안전 모노레포의 사실상 표준

T3 스택은 공식 프레임워크가 아니라, Theo Browne이 정착시킨 실전 조합이다. Next.js + tRPC + Prisma + Tailwind + zod. 이 다섯 도구가 함께 쓰일 때 어떻게 타입이 흐르는지를 보면 13장 전체 주제와 연결된다.

```
[데이터베이스] → Prisma 스키마
    → Prisma Client 타입 자동 생성
    → tRPC router에서 사용
    → tRPC client에서 자동 추론
    → React 컴포넌트에서 타입 안전하게 사용
    → zod로 입력 검증
    → Tailwind로 스타일
```

각 레이어의 타입이 다음 레이어로 자동으로 흐른다. 어느 레이어에서도 타입을 손으로 다시 정의하지 않는다. 이것이 T3 스택의 핵심 가치다.

```bash
# create-t3-app으로 프로젝트 생성
npm create t3-app@latest

# 생성되는 구조
├── src/
│   ├── server/
│   │   ├── api/
│   │   │   └── routers/
│   │   │       └── user.ts    # tRPC router
│   │   └── db.ts              # Prisma client
│   ├── app/
│   │   └── ...                # Next.js App Router
│   └── trpc/
│       ├── client.tsx         # tRPC client (자동 타입 추론)
│       └── server.ts          # tRPC server
```

```typescript
// server/api/routers/user.ts — tRPC router
export const userRouter = createTRPCRouter({
    getById: publicProcedure
        .input(z.object({ id: z.string() }))
        .query(async ({ input, ctx }) => {
            return ctx.db.user.findUnique({
                where: { id: input.id },
            })
        }),
    create: protectedProcedure
        .input(z.object({
            name: z.string().min(1),
            email: z.string().email(),
        }))
        .mutation(async ({ input, ctx }) => {
            return ctx.db.user.create({ data: input })
        }),
})

// 클라이언트 컴포넌트에서 — 타입이 자동 추론됨
const { data: user } = api.user.getById.useQuery({ id: '123' })
// user: Prisma의 User 타입 | null | undefined — 자동 추론
```

한국의 신생 스타트업과 핀테크 팀 사이에서 T3 스택 채택 사례가 늘고 있다. 빠른 개발 속도와 타입 안전성을 동시에 챙기고 싶은 팀에게 합리적인 시작점이다.

---

## ORM — 데이터베이스와 타입의 경계

### Prisma, Drizzle, TypeORM의 세 길

ORM을 선택하는 것은 데이터베이스를 TS와 어떻게 연결할지의 철학을 선택하는 것이다.

---

📚 **Java/Kotlin 시선 ③ — JPA `@Entity` ↔ Prisma schema**

```java
// JPA — 클래스와 어노테이션으로 엔티티 정의
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    @OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
    private List<Post> posts;
}
```

```prisma
// Prisma — 스키마 파일에서 모델 정의
model User {
    id    String  @id @default(cuid())
    name  String  @db.VarChar(100)
    email String  @unique

    posts Post[]

    createdAt DateTime @default(now())
    updatedAt DateTime @updatedAt
}
```

```typescript
// 스키마에서 자동 생성되는 Prisma Client 사용
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// 쿼리 — 반환 타입이 자동 추론됨
const user = await prisma.user.findUnique({
    where: { id: userId },
    include: { posts: true },
})
// user: (User & { posts: Post[] }) | null — 자동 추론

// 생성
const newUser = await prisma.user.create({
    data: { name: '홍길동', email: 'hong@example.com' },
})
```

JPA는 Java 클래스가 엔티티 정의이자 ORM 매핑이다. Prisma는 별도 스키마 파일(`schema.prisma`)이 소스이고, 거기서 TS 타입과 DB 마이그레이션 파일이 자동 생성된다. "스키마가 단일 진실의 원천"이라는 원칙이 있다. JPA의 `@Column(nullable = false)` ↔ Prisma의 `name  String` (nullable이면 `String?`). JPA의 `@OneToMany` ↔ Prisma의 `posts Post[]`.

---

**Drizzle — 타입-퍼스트 ORM**

Drizzle은 Prisma와 다른 방향에서 설계됐다. 스키마를 TypeScript 코드로 정의한다 — 별도 스키마 파일이 없다.

```typescript
// Drizzle — 스키마를 TS 코드로 정의
import { pgTable, serial, varchar, text, timestamp } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
    id: serial('id').primaryKey(),
    name: varchar('name', { length: 100 }).notNull(),
    email: text('email').notNull().unique(),
    createdAt: timestamp('created_at').defaultNow(),
})

// 쿼리 — SQL에 가까운 문법
const result = await db
    .select({
        id: users.id,
        name: users.name,
    })
    .from(users)
    .where(eq(users.email, 'hong@example.com'))
    .limit(1)

// result: { id: number, name: string }[] — 선택한 필드만 추론
```

Drizzle의 강점은 타입 추론이 선택한 컬럼에만 정확히 적용된다는 것이다. `select({ id: users.id, name: users.name })`이면 반환 타입에 `email`이 없다. Prisma에서 `select`를 명시하면 비슷한 결과를 얻지만, 문법이 덜 직관적이다.

또 다른 강점: SQL과 가까운 문법이다. Spring Data JPA의 JPQL보다 원시 SQL에 더 가깝다. ORM의 추상화 레이어를 얇게 유지하고 싶거나, 복잡한 쿼리를 TS로 표현하고 싶을 때 Drizzle이 낫다.

**TypeORM — 자바스러운, 그러나 레거시의 그늘**

TypeORM은 Java의 JPA에 가장 가깝다. 클래스에 `@Entity`, `@Column`, `@ManyToOne`을 달고, 리포지토리 패턴으로 쿼리한다.

```typescript
// TypeORM — JPA와 구조가 비슷
@Entity('users')
export class User {
    @PrimaryGeneratedColumn('uuid')
    id: string

    @Column({ length: 100 })
    name: string

    @Column({ unique: true })
    email: string

    @OneToMany(() => Post, post => post.user)
    posts: Post[]
}

// 리포지토리 패턴
const userRepository = dataSource.getRepository(User)
const user = await userRepository.findOne({
    where: { id: userId },
    relations: ['posts'],
})
```

Spring 경험자에게 TypeORM이 가장 친숙하다. 그러나 TypeORM은 NestJS와 마찬가지로 legacy 데코레이터에 의존한다. 그리고 활발한 개발이 예전만 못하다는 커뮤니티의 평이 있다 — 이슈가 오래 방치되거나 PR이 느리게 머지되는 경우가 많다. 새 프로젝트라면 Prisma나 Drizzle을 먼저 고려하는 편이 낫다. 기존 TypeORM 코드베이스가 있다면 유지하는 것이 합리적이다.

---

## 두 철학의 비교 — 어떤 팀에 어떤 선택인가

이 챕터를 마무리하기 전에, 두 가지 근본적으로 다른 철학을 한 단락으로 정리해두자.

**데코레이터 메타데이터 진영** (NestJS, TypeORM, class-validator, InversifyJS): 클래스와 데코레이터로 의도를 선언하고, 런타임에 메타데이터를 읽어 동작한다. Spring에서 온 사람에게 자연스럽다. 엔터프라이즈 패턴(DI, AOP, Exception 계층)이 표준으로 제공된다. 단점은 legacy 데코레이터 의존과 `reflect-metadata`, 그리고 무거운 추상화 레이어다.

**Web Standards 진영** (Hono, Fastify, Remix, zod, Drizzle): 표준 API(`Request`, `Response`, `FormData`)와 타입 추론에 기댄다. 런타임 메타데이터가 없고, 타입이 컴파일타임에만 살아있다. TS의 본성과 정합하고, 여러 런타임에서 동작한다. 단점은 엔터프라이즈 패턴을 스스로 조립해야 한다는 것이다.

어떤 팀에 어떤 선택이 맞는가. 몇 가지 질문으로 좁혀보자.

- **팀원 대부분이 Spring 경험자고 빠른 온보딩이 우선인가?** → NestJS. 학습 곡선이 가장 짧다.
- **외부 공개 API, 모바일 클라이언트, 다중 클라이언트가 있는가?** → Express/Fastify/Hono + 분리된 API. Next.js 풀스택은 적합하지 않다.
- **단일 웹 앱, 빠른 MVP, 타입 안전 모노레포가 필요한가?** → T3 스택(Next + tRPC + Prisma). 타입이 DB에서 UI까지 흐른다.
- **Cloudflare Workers, Deno, Bun 같은 Edge 환경을 고려하는가?** → Hono. 전 런타임에서 동작한다.
- **마이크로서비스, 이벤트 기반, 큰 엔터프라이즈 아키텍처인가?** → NestJS가 가장 성숙한 생태계를 제공한다.

---

💡 **작가의 한 마디 — 풀스택은 답이 아니라 선택지다**

Next.js App Router와 Server Actions의 등장 이후 "풀스택이 답"이라는 분위기가 생겼다. 하지만 모바일 앱이 있는 회사, 파트너 API를 열어야 하는 서비스, 여러 팀이 각자의 클라이언트를 만드는 조직에서는 여전히 백엔드와 프론트엔드의 분리가 정답이다.

풀스택 메타프레임워크는 "웹 한정"의 해법이다. 그 제약을 인지하고 선택하는 것과, 유행에 따라 선택하는 것 사이에는 큰 차이가 있다. 지금 팀이 만드는 제품이 웹만 있는가, 아니면 앞으로 모바일이 들어올 가능성이 있는가 — 이 질문 하나만 제대로 해도 아키텍처 선택이 훨씬 명확해진다.

---

## 데이터 검증 경계 — 짧게

zod와 valibot에 대해서는 5장과 12장에서 이미 깊게 다뤘다. 여기서는 백엔드 맥락에서 한 줄만 짚는다.

외부에서 들어오는 모든 데이터 — API 요청 바디, URL 쿼리 파라미터, 환경 변수, 외부 API 응답 — 는 런타임 검증이 필요하다. 내부 코드끼리의 타입 신뢰는 `as`나 타입 단언 없이도 가능하지만, 외부 경계를 넘어오는 데이터는 TS 컴파일러가 보장할 수 없다. 이것이 논쟁 D(타입 단언 vs zod)의 사실상 합의다 — "외부 경계만 검증한다."

valibot은 zod와 비슷한 스키마 API를 갖지만 번들 크기가 훨씬 작다(트리 쉐이킹 친화). Edge 환경이나 번들 크기가 민감한 Cloudflare Workers에서는 valibot이 낫다.

---

## 마무리

Spring 베테랑이 이 챕터를 읽고 가져갈 것이 두 가지 있다.

하나는 NestJS에 대한 자신감이다. 모양이 비슷하다는 것은 진짜다. 그리고 다른 자리들 — 모듈 명시 등록, module re-export, Provider 스코프, Guard/Pipe/Filter의 분리 — 도 이제 예상 가능한 자리가 됐다. 헷갈릴 때 이 챕터의 다섯 가지 함정으로 돌아오자.

다른 하나는 Hono와 Web Standards 진영의 방향이다. 타입이 라우트 정의에서 클라이언트까지 자동으로 흐르는 것이 어떻게 가능한지 — 5장에서 배운 타입 마법이 현실 코드에서 어떻게 살아나는지 — 를 눈으로 봤다. 이 방향이 앞으로 Node.js 백엔드 생태계에서 더 넓어질 가능성이 높다.

프레임워크는 많고 선택은 어렵다. 하지만 선택의 기준 — 팀의 배경, 클라이언트의 다양성, 런타임 환경 — 이 명확하면 선택이 명확해진다. 도구를 고르는 사람이 도구에 휘둘리지 않는다.

---

📖 **더 깊이 가려면**

- **NestJS 공식 문서** (docs.nestjs.com): 모듈 체계와 DI, Guard/Pipe/Filter 상세 설명. "Fundamentals" 섹션은 Spring 경험자에게 가장 유용하다.
- **Hono 공식 문서** (hono.dev): RPC 섹션과 `hc` 클라이언트 사용법. Cloudflare Workers 배포 가이드.
- **Total TypeScript** (Matt Pocock): Hono의 타입 추론 내부 작동 방식을 파헤치는 글들. Hono 소스를 따라가며 5장의 타입 도구들이 어떻게 조합되는지 볼 수 있다.
- **Prisma 공식 문서** (prisma.io): 스키마 정의, 마이그레이션, 타입 추론 패턴.
- **T3 Stack 문서** (create.t3.gg): T3 스택의 각 컴포넌트 선택 이유와 통합 패턴.
- **이동욱(향로) 기술블로그** (jojoldu.tistory.com): NestJS와 Spring의 차이를 한국어로 가장 잘 정리한 자료 중 하나.
- **라인·쿠팡 NestJS 도입 사례** (각사 기술블로그): Spring 조직이 NestJS를 도입할 때의 실제 결정 과정과 함정.

→ **14장에서는 NestJS·Hono·tRPC의 *타입 수준 계약 테스트*와 *Playwright E2E*를 자세히 다룬다.** 이 챕터에서 만든 라우터와 서비스 코드가 어떻게 Vitest로 검증되는지, RPC 클라이언트의 타입이 E2E 시나리오와 어떻게 연결되는지 — 테스트와 타입이 만나는 자리다.

---

> 13장에서 백엔드와 풀스택의 여섯 길을 걸었다. 코드를 짜는 것만큼 중요한 것이 코드가 올바른지 검증하는 것이다. Java/Kotlin에서는 JUnit + MockK + Playwright가 표준이었다. TypeScript에서는 무엇이 그 자리를 차지하는가. 그리고 Java에는 없는 *타입 자체를 테스트하는* 이 발상은 무엇인가. 14장에서.

# 14장. 테스트와 타입 — Vitest·expect-type·Playwright

Spring 프로젝트의 테스트 코드를 짜던 손이 처음으로 TS 프로젝트에서 테스트 파일을 열었다고 해보자. JUnit의 `@Test`는 어디 갔는가. MockK의 `every { ... } returns ...`는 어떤 문법으로 바꿔야 하는가. 그리고 무엇보다 — *타입을 테스트한다*는 이 낯선 개념은 대체 무슨 뜻인가.

Java/Kotlin 생태계에서 테스트 도구 셋은 비교적 명확했다. JUnit 5가 단위·통합 테스트를 책임지고, MockK(또는 Mockito)가 모킹을 맡고, Selenium이나 Playwright가 E2E를 담당했다. AssertJ로 어설션을 읽기 좋게 만들고, jqwik으로 프로퍼티 기반 테스트를 조금 곁들이면 웬만한 테스트 전략이 완성됐다.

TS 생태계는 이 구도와 얼마나 다를까. 놀랍도록 비슷한 부분도 있고, 완전히 다른 영역도 있다. 비슷한 부분은 빠르게 매핑할 수 있다. 다른 부분이 진짜 흥미롭다. 그 중심에 *타입 단위 테스트*가 있다. 런타임이 없어도 타입이 의도한 모양인지 검증할 수 있다는 이 발상은 Java에는 없던 자리다. 4·5장에서 공들여 만든 복잡한 타입이 여기서 검증된다. 12·13장의 컴포넌트와 API가 Vitest, Testing Library, Playwright로 테스트된다.

이 장은 그 전체 지도를 그린다.

---

## 단위 테스트의 자리 — Vitest vs Jest

Java 개발자가 처음 TS 프로젝트를 열면 `package.json`의 `scripts` 항목에서 낯선 이름을 만난다.

```json
{
  "scripts": {
    "test": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

`vitest`가 무엇인가. 2022년부터 빠르게 표준 자리를 차지하고 있는 테스트 러너다. Vite 기반 프로젝트에서는 이제 Jest보다 Vitest를 선택하는 게 합리적 디폴트가 됐다. 왜 그런지 이해하려면 Jest부터 살펴볼 필요가 있다.

**Jest**는 Facebook(현 Meta)이 만든 테스트 프레임워크다. React 프로젝트가 폭발적으로 증가하던 2015~2020년대 초반 사실상 표준이 됐다. 기능이 풍부하다. 단위 테스트·통합 테스트·스냅샷 테스트·코드 커버리지가 하나의 패키지에 들어 있다. 문서도 방대하고 커뮤니티도 크다.

그러나 Jest에는 답답한 구석이 있다. ESM 지원이 오랫동안 실험적이었다. 트랜스파일을 위해 `ts-jest`나 `babel-jest`를 별도로 설치해야 하고, 설정 파일이 복잡해진다. 그리고 느리다. 테스트가 많아질수록 Jest의 속도 문제가 도드라진다.

**Vitest**는 이 문제들을 Vite의 힘으로 해결했다. Vite의 번들러 파이프라인 위에서 돌아가기 때문에 ESM을 기본으로 지원하고, HMR 개념을 테스트에 적용해 변경된 파일과 연관된 테스트만 재실행한다. TypeScript 파일을 별도 설정 없이 직접 실행할 수 있다. 그리고 빠르다. 프로젝트 규모에 따라 다르지만 Jest 대비 수 배에서 수십 배 빠른 실행 속도 보고가 일반적이다.

```typescript
// Vitest 설정 — vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
});
```

설정이 단순하다. `tsconfig.json`을 자동으로 읽고, ESM도 기본 지원한다. Jest처럼 `ts-jest`를 따로 설치할 필요가 없다.

테스트 코드 문법은 Jest와 거의 동일하다. Vitest는 의도적으로 Jest API와 호환되도록 설계했다. Jest에서 Vitest로 마이그레이션하는 비용이 낮은 이유다.

```typescript
// product.test.ts
import { describe, it, expect } from 'vitest';
import { calculateDiscount } from './product';

describe('calculateDiscount', () => {
  it('정회원에게 10% 할인을 적용한다', () => {
    const result = calculateDiscount(10000, 'member');
    expect(result).toBe(9000);
  });

  it('비회원은 할인 없음', () => {
    const result = calculateDiscount(10000, 'guest');
    expect(result).toBe(10000);
  });
});
```

JUnit의 `@Test`와 비교해보자.

---

> **📚 Java/Kotlin 시선 ① — JUnit `@Test` ↔ Vitest `test` / `it`**
>
> **Java/Kotlin (JUnit 5)**
> ```kotlin
> @ExtendWith(MockKExtension::class)
> class CalculateDiscountTest {
>
>     @Test
>     fun `정회원에게 10% 할인을 적용한다`() {
>         val result = calculateDiscount(10000, MemberType.MEMBER)
>         assertThat(result).isEqualTo(9000)
>     }
>
>     @Test
>     fun `비회원은 할인 없음`() {
>         val result = calculateDiscount(10000, MemberType.GUEST)
>         assertThat(result).isEqualTo(10000)
>     }
> }
> ```
>
> **TypeScript (Vitest)**
> ```typescript
> import { describe, it, expect } from 'vitest';
>
> describe('calculateDiscount', () => {
>   it('정회원에게 10% 할인을 적용한다', () => {
>     const result = calculateDiscount(10000, 'member');
>     expect(result).toBe(9000);
>   });
>
>   it('비회원은 할인 없음', () => {
>     const result = calculateDiscount(10000, 'guest');
>     expect(result).toBe(10000);
>   });
> });
> ```
>
> 구조가 놀랍도록 닮았다. `describe`가 JUnit의 테스트 클래스 역할을 하고, `it` 또는 `test`가 `@Test`에 대응한다. 테스트 이름을 문자열로 자유롭게 쓸 수 있다는 점은 Kotlin의 backtick 함수명과 비슷한 자유다. `expect(...).toBe(...)`는 AssertJ의 `assertThat(...).isEqualTo(...)`와 구조가 같다. 다만 Java처럼 테스트 클래스 인스턴스를 생성하거나 어노테이션으로 설정을 주입하는 방식은 없다 — 함수가 first-class이기 때문에 구성이 훨씬 단순하다.

---

### Vitest를 선택해야 하는 시점, Jest를 유지해야 하는 시점

신규 프로젝트라면 Vitest가 합리적 디폴트다. Vite 기반 프론트엔드 프로젝트는 물론이고, Node 백엔드 프로젝트에서도 Vitest는 잘 작동한다. 설정이 단순하고 빠르며 ESM을 자연스럽게 지원한다.

반면 기존 Jest 코드베이스를 유지해야 하는 상황이 있다. 레거시 CJS 기반 코드베이스, 복잡한 Jest 플러그인 생태계에 이미 깊이 의존하는 경우, 또는 팀이 Jest에 익숙해 마이그레이션 비용이 이득보다 클 때다. Jest를 선택했다는 게 틀린 결정이 아니다. 2025년 현재도 Jest는 대규모 프로젝트에서 안정적으로 쓰인다.

```
Vitest를 선택하는 편이 나은 경우:
- 신규 프로젝트 또는 Vite 기반 프로젝트
- ESM 우선 코드베이스
- 빠른 피드백 루프가 중요한 팀
- 설정을 최소화하고 싶을 때

Jest를 유지하는 편이 나은 경우:
- 기존 Jest 코드베이스가 크고 안정적
- create-react-app 같은 레거시 scaffolding에 묶여 있을 때
- Jest 전용 플러그인/reporter에 이미 투자했을 때
```

하나 주의할 점이 있다. Vitest와 Jest의 API가 호환된다고 했지만 `vi` 네임스페이스는 `jest` 대신 `vi`를 써야 한다. `jest.fn()`이 `vi.fn()`으로, `jest.mock()`이 `vi.mock()`으로 바뀐다. 마이그레이션에서 대부분의 변경이 여기에 집중된다.

---

## Test Double의 TS화 — `vi.fn`, `vi.mock`, 타입 안전 모킹

MockK를 쓰던 Kotlin 개발자가 처음 `vi.mock`을 만나면 한 가지가 눈에 걸린다. MockK는 타입 안전하다. `mockk<UserRepository>()`라고 쓰면 `UserRepository`의 메서드 시그니처가 즉시 보인다. 타입 시스템이 모킹의 경계를 잡아준다.

`vi.fn()`도 타입 안전하게 쓸 수 있다. 하지만 명시적으로 타입을 주어야 하는 자리가 조금 더 많다.

```typescript
// vi.fn() 기본 — 타입을 명시하지 않으면 any
const mockFetch = vi.fn();

// 타입을 명시하는 방법들
const mockFetch1 = vi.fn<() => Promise<Response>>();

// 또는 함수 타입을 직접
const mockSave = vi.fn<(user: User) => Promise<void>>();

// Mock Return Value
mockSave.mockResolvedValue(undefined);
mockFetch1.mockResolvedValue(new Response('{"id": 1}'));
```

`vi.mock()`은 모듈 전체를 대체한다. Java의 `@MockBean`과 비슷한 역할인데, 동작 방식은 다르다. 모듈 경로를 문자열로 지정하면 해당 모듈의 모든 export가 자동으로 mock 함수로 대체된다.

```typescript
// userService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getUserById } from './userService';
import { db } from './database'; // 이 모듈을 mock할 것

vi.mock('./database'); // 전체 모듈을 mock

describe('getUserById', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('사용자를 조회한다', async () => {
    const mockUser = { id: 1, name: '홍길동', email: 'hong@example.com' };

    // db.findUserById를 스텁으로 교체
    vi.mocked(db.findUserById).mockResolvedValue(mockUser);

    const result = await getUserById(1);

    expect(result).toEqual(mockUser);
    expect(db.findUserById).toHaveBeenCalledWith(1);
    expect(db.findUserById).toHaveBeenCalledTimes(1);
  });
});
```

`vi.mocked()`가 핵심이다. `db.findUserById`를 그냥 쓰면 TypeScript는 그게 mock 함수라는 걸 모른다. `vi.mocked()`로 감싸면 해당 함수가 `MockedFunction` 타입이 되어 `mockResolvedValue`, `toHaveBeenCalledWith` 같은 mock 전용 메서드에 접근할 수 있다.

---

> **📚 Java/Kotlin 시선 ② — MockK ↔ `vi.fn` / `vi.mock`**
>
> **Kotlin (MockK)**
> ```kotlin
> @ExtendWith(MockKExtension::class)
> class UserServiceTest {
>     @MockK
>     lateinit var userRepository: UserRepository
>
>     @InjectMockKs
>     lateinit var userService: UserService
>
>     @Test
>     fun `사용자를 조회한다`() {
>         val mockUser = User(id = 1, name = "홍길동")
>         every { userRepository.findById(1) } returns mockUser
>
>         val result = userService.getUserById(1)
>
>         assertThat(result).isEqualTo(mockUser)
>         verify(exactly = 1) { userRepository.findById(1) }
>     }
> }
> ```
>
> **TypeScript (Vitest)**
> ```typescript
> import { vi, describe, it, expect, beforeEach } from 'vitest';
> import { UserService } from './userService';
> import { UserRepository } from './userRepository';
>
> vi.mock('./userRepository');
>
> describe('UserService', () => {
>   let userService: UserService;
>   let mockRepo: UserRepository;
>
>   beforeEach(() => {
>     mockRepo = new UserRepository() as vi.Mocked<UserRepository>;
>     userService = new UserService(mockRepo);
>   });
>
>   it('사용자를 조회한다', async () => {
>     const mockUser = { id: 1, name: '홍길동' };
>     vi.mocked(mockRepo.findById).mockResolvedValue(mockUser);
>
>     const result = await userService.getUserById(1);
>
>     expect(result).toEqual(mockUser);
>     expect(mockRepo.findById).toHaveBeenCalledWith(1);
>     expect(mockRepo.findById).toHaveBeenCalledTimes(1);
>   });
> });
> ```
>
> 어휘 매핑을 정리하면 이렇다. `@MockK` → `vi.mock()`. `every { ... } returns` → `mockResolvedValue` / `mockReturnValue`. `verify { ... }` → `expect(...).toHaveBeenCalledWith(...)`. `@InjectMockKs`는 TS에 직접 대응물이 없다 — DI가 생성자 기반이면 직접 주입하고, NestJS라면 `Test.createTestingModule()`을 쓴다. MockK의 `coEvery`(코루틴 mock) 개념은 TS에서는 별도 처리가 필요 없다 — `async/await`가 이미 일급이기 때문이다.

---

### 부분 모킹 — `vi.spyOn`

모듈 전체가 아니라 특정 메서드만 감시하거나 교체하고 싶을 때 `vi.spyOn`을 쓴다. MockK의 `spyk`와 비슷한 역할이다.

```typescript
import { vi, describe, it, expect, afterEach } from 'vitest';
import * as emailService from './emailService';

describe('sendWelcomeEmail', () => {
  afterEach(() => {
    vi.restoreAllMocks(); // spy 원래 구현으로 복원
  });

  it('이메일을 전송한다', async () => {
    const spy = vi.spyOn(emailService, 'sendEmail').mockResolvedValue(true);

    await emailService.sendWelcomeEmail('hong@example.com', '홍길동');

    expect(spy).toHaveBeenCalledWith(
      'hong@example.com',
      expect.stringContaining('환영합니다')
    );
  });
});
```

`vi.restoreAllMocks()`를 `afterEach`에 넣는 패턴이 중요하다. spy를 복원하지 않으면 다음 테스트에서 이전 spy가 살아남아 난감한 상황이 생긴다. 테스트가 격리되지 않으면 원인을 찾기가 끔찍하게 어려워진다. 이 패턴은 잊지 않는 편이 낫다.

---

## 프로퍼티 기반 테스트 — fast-check와 jqwik

"모든 양수 정수에 대해 이 함수가 올바르게 작동하는가"를 검증하고 싶다고 해보자. 예제 기반 테스트라면 몇 가지 케이스를 직접 나열한다. 하지만 빠뜨린 케이스가 있으면? 경계값을 놓치면? 프로퍼티 기반 테스트는 이 문제를 다른 방식으로 접근한다. *입력의 범위를 선언*하고, 프레임워크가 그 범위에서 자동으로 케이스를 생성해 실행한다.

Kotlin에서는 `jqwik`이 이 역할을 한다. TS에서는 `fast-check`가 같은 자리에 있다.

```typescript
import { describe, it } from 'vitest';
import fc from 'fast-check';

describe('sortedArray property', () => {
  it('정렬 후 배열 길이는 변하지 않는다', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted = [...arr].sort((a, b) => a - b);
        return sorted.length === arr.length;
      })
    );
  });

  it('정렬 후 인접 요소는 항상 오름차순이다', () => {
    fc.assert(
      fc.property(fc.array(fc.integer(), { minLength: 2 }), (arr) => {
        const sorted = [...arr].sort((a, b) => a - b);
        for (let i = 0; i < sorted.length - 1; i++) {
          if (sorted[i] > sorted[i + 1]) return false;
        }
        return true;
      })
    );
  });
});
```

`fc.assert`가 수백 개의 랜덤 케이스를 자동으로 생성해 실행한다. 실패하는 케이스를 발견하면 `fast-check`는 가장 작은 반례(shrinking)를 찾아 보여준다. `[1, 0]` 같은 단순한 반례가 복잡한 원래 케이스 대신 나타나는 방식이다.

---

> **📚 Java/Kotlin 시선 ③ — jqwik ↔ fast-check**
>
> **Kotlin (jqwik)**
> ```kotlin
> import net.jqwik.api.*
>
> class SortPropertyTest {
>     @Property
>     fun `정렬 후 배열 길이는 변하지 않는다`(
>         @ForAll list: List<Int>
>     ): Boolean {
>         val sorted = list.sorted()
>         return sorted.size == list.size
>     }
>
>     @Property
>     fun `정렬 후 인접 요소는 항상 오름차순`(
>         @ForAll @Size(min = 2) list: List<@IntRange(min = -100, max = 100) Int>
>     ): Boolean {
>         val sorted = list.sorted()
>         return sorted.zipWithNext().all { (a, b) -> a <= b }
>     }
> }
> ```
>
> **TypeScript (fast-check + Vitest)**
> ```typescript
> import fc from 'fast-check';
> import { describe, it } from 'vitest';
>
> describe('sort property', () => {
>   it('정렬 후 배열 길이는 변하지 않는다', () => {
>     fc.assert(
>       fc.property(fc.array(fc.integer()), (arr) => {
>         return [...arr].sort((a, b) => a - b).length === arr.length;
>       })
>     );
>   });
>
>   it('정렬 후 인접 요소는 항상 오름차순', () => {
>     fc.assert(
>       fc.property(
>         fc.array(fc.integer({ min: -100, max: 100 }), { minLength: 2 }),
>         (arr) => {
>           const sorted = [...arr].sort((a, b) => a - b);
>           return sorted.every((v, i) => i === 0 || sorted[i - 1] <= v);
>         }
>       )
>     );
>   });
> });
> ```
>
> jqwik은 어노테이션으로 입력 범위를 선언하고, `@Property`가 프로퍼티 테스트임을 표시한다. fast-check는 함수형으로 구성된다 — `fc.property(생성기, 검증함수)`. 두 도구 모두 shrinking을 지원하므로 실패 시 최소 반례를 알 수 있다. jqwik의 `@ForAll @Size`같은 제약은 fast-check에서 `fc.array(fc.integer(), { minLength: 2 })`처럼 생성기 옵션으로 표현한다.

---

fast-check는 string, date, uuid, ipV4, emailAddress 같은 다양한 임의값 생성기를 제공한다. 도메인 객체를 생성하는 자체 Arbitrary를 만드는 것도 가능하다.

```typescript
// 도메인 객체 Arbitrary 정의
const userArbitrary = fc.record({
  id: fc.nat(),
  name: fc.string({ minLength: 1, maxLength: 50 }),
  email: fc.emailAddress(),
  age: fc.integer({ min: 0, max: 120 }),
});

it('사용자 직렬화-역직렬화는 항등 변환이다', () => {
  fc.assert(
    fc.property(userArbitrary, (user) => {
      const json = JSON.stringify(user);
      const parsed = JSON.parse(json);
      return parsed.id === user.id && parsed.email === user.email;
    })
  );
});
```

매일 쓰는 도구는 아니지만, 파싱·직렬화·알고리즘·유틸리티 함수에 경계값 케이스가 많을수록 fast-check는 가치를 발휘한다.

---

## 컴포넌트 테스트 — Testing Library + Vitest

12장에서 React 컴포넌트를 만들었다면 그 컴포넌트를 어떻게 테스트해야 할까. 전통적인 컴포넌트 테스트는 렌더링된 HTML 구조를 쿼리하거나 내부 state를 직접 확인하는 방식이었다. 하지만 이 방식은 구현 세부사항에 의존해서, 리팩토링을 하면 테스트가 깨지는 경우가 많다.

Testing Library는 다른 철학을 제안한다. *사용자가 실제로 보고 상호작용하는 방식으로 테스트하라.* 화면에 보이는 텍스트, 레이블, 역할(role)로 요소를 찾고, 클릭·타이핑 같은 실제 사용자 동작으로 테스트한다. 구현이 바뀌어도 사용자 경험이 같다면 테스트도 통과해야 한다는 원칙이다.

```typescript
// LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('이메일과 비밀번호를 입력하고 로그인 버튼을 누르면 onLogin이 호출된다', async () => {
    const mockOnLogin = vi.fn<(email: string, password: string) => Promise<void>>();
    mockOnLogin.mockResolvedValue(undefined);

    render(<LoginForm onLogin={mockOnLogin} />);

    const emailInput = screen.getByLabelText('이메일');
    const passwordInput = screen.getByLabelText('비밀번호');
    const loginButton = screen.getByRole('button', { name: '로그인' });

    await userEvent.type(emailInput, 'hong@example.com');
    await userEvent.type(passwordInput, 'secret123');
    await userEvent.click(loginButton);

    await waitFor(() => {
      expect(mockOnLogin).toHaveBeenCalledWith('hong@example.com', 'secret123');
    });
  });

  it('이메일 형식이 잘못되면 에러 메시지를 보여준다', async () => {
    const mockOnLogin = vi.fn();
    render(<LoginForm onLogin={mockOnLogin} />);

    await userEvent.type(screen.getByLabelText('이메일'), 'not-an-email');
    await userEvent.click(screen.getByRole('button', { name: '로그인' }));

    expect(screen.getByText('올바른 이메일 주소를 입력해주세요.')).toBeInTheDocument();
    expect(mockOnLogin).not.toHaveBeenCalled();
  });
});
```

`getByLabelText`, `getByRole`이 핵심이다. CSS 선택자나 컴포넌트의 내부 구조가 아니라 접근성 트리(accessibility tree)를 통해 요소를 찾는다. 이렇게 하면 리팩토링이 자유로워진다. 내부 구현을 아무리 바꿔도 `이메일` 레이블이 붙은 입력 필드가 남아 있고 `로그인` 버튼이 남아 있으면 테스트는 통과한다.

`userEvent`가 `fireEvent`보다 선호된다. `fireEvent.click`은 단순히 click 이벤트를 발생시키지만, `userEvent.click`은 실제 브라우저처럼 mouseenter, mousedown, mouseup, click 이벤트를 순서대로 발생시킨다. 더 현실적이다.

Vitest에서 Testing Library를 쓰려면 jsdom 또는 happy-dom 환경을 설정해야 한다.

```typescript
// vitest.config.ts — 브라우저 환경 추가
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom', // 또는 'happy-dom'
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom'; // toBeInTheDocument() 같은 커스텀 매처 추가
```

`@testing-library/jest-dom`이 `toBeInTheDocument()`, `toHaveValue()`, `toBeVisible()` 같은 DOM 특화 매처를 추가한다. 이것 없으면 컴포넌트 테스트가 상당히 번거로워진다.

---

## 타입 단위 테스트 — TS만의 영역

이제 이 장의 핵심 주제로 들어간다. 솔직히 말하면, 이 절을 처음 보는 Java 개발자는 고개를 갸웃거릴 수 있다.

*타입을 테스트한다는 게 무슨 뜻인가?*

---

> **💡 작가의 한 마디 — 타입을 테스트한다는 발상이 어색하다면**
>
> Java에는 이 개념이 없다. JUnit은 런타임에서 값을 검증한다. 컴파일 타임의 타입 정확성은 컴파일러가 암묵적으로 보장한다고 가정하기 때문에, 별도로 "이 변수의 타입이 `String`이 맞는가"를 테스트하지 않는다.
>
> TS는 다르다. 4·5장에서 살펴봤듯 TS의 타입 시스템은 매핑 타입, 조건부 타입, `infer`, 템플릿 리터럴 타입으로 복잡한 타입을 프로그래밍한다. `z.infer<typeof UserSchema>`가 어떤 타입을 뽑아내는가, Hono의 라우트 핸들러에서 응답 타입이 자동 추론되는가, 유틸리티 타입 `ExtractRouteParams<'/users/:id'>` 가 `{ id: string }`을 맞게 만들어내는가 — 이것들은 런타임으로 검증할 수 없다. 타입은 컴파일 타임에만 존재하기 때문이다.
>
> 그래서 "타입이 의도한 모양인가"를 컴파일 타임에 검증하는 도구가 생겼다. `expect-type`, `tsd`, `// @ts-expect-error` 가 그것이다. 이것은 Java에 없던 완전히 새로운 테스트의 자리다. 낯설게 느껴지는 건 당연하다 — 진짜로 새로운 개념이기 때문이다.

---

### `// @ts-expect-error` — 가장 단순한 시작

타입 테스트의 가장 기본적인 형태는 `// @ts-expect-error` 주석이다. 이 주석이 붙은 줄에서 컴파일러 에러가 발생해야 한다. 만약 에러가 발생하지 않으면 오히려 `@ts-expect-error` 자체가 에러가 된다.

```typescript
// 이 타입 단언은 틀린 것이어야 한다
const x: number = 'hello';
// @ts-expect-error
const y: string = 42;  // number를 string에 할당하면 에러가 나야 함

// 유틸리티 함수의 타입 안전성을 확인할 때
function greet(name: string): string {
  return `안녕하세요, ${name}님`;
}

// @ts-expect-error — 숫자를 넘기면 에러가 나야 한다
greet(42);

// 에러가 안 나면 @ts-expect-error 자체가 에러가 된다
// @ts-expect-error  ← 이 줄 아래에 에러가 없으면 컴파일 에러
greet('홍길동'); // 이건 정상 호출 — @ts-expect-error가 여기서 에러를 낸다
```

`// @ts-ignore`와 혼동하지 않는 편이 낫다. `@ts-ignore`는 에러를 무조건 억제하고, 실제로 에러가 없어도 조용하다. `@ts-expect-error`는 에러가 있어야 정상이고, 에러가 없으면 오히려 문제다. 타입 테스트 목적이라면 항상 `@ts-expect-error`를 써야 한다.

### `expect-type` — 타입의 단위 테스트 라이브러리

`expect-type`은 타입을 검증하는 전용 라이브러리다. 런타임에서 아무것도 하지 않는다. 오직 컴파일 타임에 타입 관계를 검증한다.

```typescript
import { expectTypeOf } from 'expect-type';

// 기본 타입 검증
expectTypeOf(42).toBeNumber();
expectTypeOf('hello').toBeString();
expectTypeOf(null).toBeNull();

// 함수 반환 타입 검증
function add(a: number, b: number): number {
  return a + b;
}
expectTypeOf(add).returns.toBeNumber();
expectTypeOf(add).parameters.toEqualTypeOf<[number, number]>();

// 복잡한 타입 검증
type ExtractId<T> = T extends { id: infer U } ? U : never;

expectTypeOf<ExtractId<{ id: number; name: string }>>().toEqualTypeOf<number>();
expectTypeOf<ExtractId<{ name: string }>>().toEqualTypeOf<never>();
```

이게 왜 필요한가. 5장에서 `conditional type`과 `infer`로 복잡한 타입 변환 유틸리티를 만들었다고 해보자. 그 유틸리티가 실제로 의도한 타입을 만들어내는지 어떻게 확인하는가. 런타임 테스트로는 알 수 없다. 타입은 런타임에 존재하지 않기 때문이다. `expectTypeOf`로 확인하는 것이 유일한 방법이다.

```typescript
// 실제 사례 — 복잡한 유틸리티 타입 검증
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [P in keyof T]: DeepReadonly<T[P]> }
  : T;

type Config = {
  server: {
    host: string;
    port: number;
  };
  db: {
    connections: { host: string; port: number }[];
  };
};

type ReadonlyConfig = DeepReadonly<Config>;

// 의도한 타입이 맞는지 검증
expectTypeOf<ReadonlyConfig>().toMatchTypeOf<{
  readonly server: {
    readonly host: string;
    readonly port: number;
  };
  readonly db: {
    readonly connections: readonly { readonly host: string; readonly port: number }[];
  };
}>();

// 변경이 불가능한지도 검증
expectTypeOf<ReadonlyConfig['server']['host']>().toBeString();

// 잘못된 타입 할당이 에러를 내는지 확인
// @ts-expect-error
const cfg: ReadonlyConfig = { server: { host: 'localhost', port: 3000 }, db: { connections: [] } };
// cfg.server.host = 'other'; // 이게 에러여야 한다
```

### `tsd` — `.test-d.ts` 파일로 타입 테스트 분리

`tsd`는 타입 테스트를 별도 `.test-d.ts` 파일에 작성하는 방식을 제안한다. 라이브러리를 만드는 경우에 특히 유용하다. 라이브러리의 공개 API 타입이 의도한 대로 동작하는지 배포 전에 검증할 수 있다.

```typescript
// index.test-d.ts
import { expectType, expectError } from 'tsd';
import { createUser, UserCreateInput, User } from './index';

// 정상 케이스
expectType<User>(createUser({ name: '홍길동', email: 'hong@example.com' }));

// 에러 케이스 — 필수 필드 누락
expectError(createUser({ name: '홍길동' })); // email 없으면 에러여야 함

// 에러 케이스 — 잘못된 타입
expectError(createUser({ name: 42, email: 'hong@example.com' })); // name은 string이어야 함
```

`npm test`를 실행하면 `tsd`가 이 파일을 TypeScript 컴파일러로 검사한다. `expectError` 안에서 에러가 나지 않으면 테스트가 실패한다.

라이브러리를 직접 만들 계획이 없다면 `tsd`보다 `expect-type`이 더 편하다. `expect-type`은 Vitest 테스트 파일 안에서 바로 쓸 수 있어 별도 설정이 필요 없다.

### Vitest와 함께 — 타입 테스트를 일반 테스트와 함께 실행

Vitest 1.x부터는 `expectTypeOf`가 내장되어 있다. `expect-type`을 별도 설치하지 않아도 된다.

```typescript
// userTypes.test.ts
import { describe, it, expectTypeOf } from 'vitest';
import type { User, UserCreateInput } from './types';
import { createUser } from './userService';

describe('User 타입', () => {
  it('createUser는 User를 반환한다', () => {
    expectTypeOf(createUser).returns.toMatchTypeOf<User>();
  });

  it('UserCreateInput에는 id가 없다', () => {
    expectTypeOf<UserCreateInput>().not.toHaveProperty('id');
  });

  it('User의 id는 number이다', () => {
    expectTypeOf<User['id']>().toBeNumber();
  });
});
```

이 테스트는 런타임에서 아무것도 실행하지 않는다. 하지만 `vitest run`을 실행하면 컴파일 타임에 타입 관계를 검증하고, 실패하면 테스트가 실패한다.

타입이 복잡해질수록 이런 테스트의 가치가 커진다. Hono의 라우트 타입 추론이 제대로 동작하는지, zod 스키마에서 뽑은 타입이 예상대로인지 — 이것들을 런타임 테스트로는 확인할 수 없다.

```typescript
// Hono RPC 타입 검증 예시
import { Hono } from 'hono';
import { hc } from 'hono/client';
import { expectTypeOf } from 'vitest';

const app = new Hono().get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id, name: '홍길동' });
});

const client = hc<typeof app>('/');

// RPC 클라이언트 응답 타입 검증
expectTypeOf(client.users[':id'].$get).toBeFunction();
```

---

## E2E 테스트 — Playwright와 Selenium의 거리

Selenium을 써본 Java 개발자라면 Playwright를 처음 보는 순간 편안함을 느낄 것이다. 개념 자체는 비슷하다. 브라우저를 자동화해서 실제 사용자 흐름을 검증한다. 하지만 Playwright는 훨씬 현대적이다.

---

> **📚 Java/Kotlin 시선 ④ — Selenium ↔ Playwright**
>
> **Java (Selenium WebDriver)**
> ```java
> @Test
> public void testLogin() {
>     WebDriver driver = new ChromeDriver();
>     try {
>         driver.get("http://localhost:3000/login");
>         driver.findElement(By.id("email")).sendKeys("hong@example.com");
>         driver.findElement(By.id("password")).sendKeys("secret123");
>         driver.findElement(By.cssSelector("button[type='submit']")).click();
>
>         // 페이지 이동 기다리기
>         new WebDriverWait(driver, Duration.ofSeconds(10))
>             .until(ExpectedConditions.urlContains("/dashboard"));
>
>         String welcomeText = driver.findElement(By.className("welcome")).getText();
>         assertEquals("홍길동 님, 환영합니다!", welcomeText);
>     } finally {
>         driver.quit();
>     }
> }
> ```
>
> **TypeScript (Playwright)**
> ```typescript
> import { test, expect } from '@playwright/test';
>
> test('로그인 성공 후 대시보드로 이동한다', async ({ page }) => {
>   await page.goto('/login');
>
>   await page.getByLabel('이메일').fill('hong@example.com');
>   await page.getByLabel('비밀번호').fill('secret123');
>   await page.getByRole('button', { name: '로그인' }).click();
>
>   await expect(page).toHaveURL('/dashboard');
>   await expect(page.getByText('홍길동 님, 환영합니다!')).toBeVisible();
> });
> ```
>
> 차이가 분명하다. Selenium은 명시적인 대기(WebDriverWait)를 직접 관리해야 한다. Playwright는 기본적으로 자동 대기(auto-waiting)를 지원한다. 요소가 나타날 때까지, 클릭할 수 있을 때까지, 네트워크가 안정화될 때까지 자동으로 기다린다. 그리고 `getByLabel`, `getByRole` — Testing Library와 같은 철학이다. 접근성 기반으로 요소를 찾는다.
>
> 또 한 가지. Playwright는 Chromium, Firefox, WebKit(Safari) 세 엔진을 하나의 API로 지원한다. Selenium은 드라이버를 브라우저마다 관리해야 한다. Playwright의 브라우저 설치는 `npx playwright install` 한 줄로 끝난다.

---

Playwright의 설정 파일이 어떻게 생겼는지 살펴보자.

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,        // 모든 테스트 병렬 실행
  forbidOnly: !!process.env.CI, // CI에서 test.only() 금지
  retries: process.env.CI ? 2 : 0, // CI에서 실패 시 재시도
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry', // 재시도 시 추적 기록
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  webServer: {
    command: 'npm run build && npm run preview',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

`webServer` 옵션이 편리하다. E2E 테스트 실행 전에 개발 서버나 프리뷰 서버를 자동으로 시작하고, 테스트가 끝나면 종료한다. Java에서 Testcontainers로 서버를 띄우는 것과 비슷한 편의다.

### Page Object Model — 구조화된 E2E 테스트

E2E 테스트가 많아지면 코드 중복이 심해진다. "이메일 입력 → 비밀번호 입력 → 로그인 버튼 클릭" 흐름이 여러 테스트에서 반복된다. Page Object Model(POM) 패턴으로 이 중복을 해소할 수 있다.

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('이메일');
    this.passwordInput = page.getByLabel('비밀번호');
    this.loginButton = page.getByRole('button', { name: '로그인' });
    this.errorMessage = page.getByTestId('error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

// e2e/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('로그인', () => {
  test('성공적으로 로그인한다', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('hong@example.com', 'secret123');

    await expect(page).toHaveURL('/dashboard');
  });

  test('잘못된 비밀번호로 로그인 시 에러', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('hong@example.com', 'wrong');

    await expect(loginPage.errorMessage).toBeVisible();
    await expect(loginPage.errorMessage).toContainText('이메일 또는 비밀번호가 올바르지 않습니다');
  });
});
```

Page Object가 TypeScript의 클래스와 자연스럽게 맞다. `Locator` 타입이 명확하고, IDE 자동완성이 잘 작동한다. 테스트 코드가 비즈니스 흐름 중심으로 읽힌다.

### Cypress와의 비교

Playwright 말고 Cypress도 많이 쓰인다. 2018년경 Selenium의 대안으로 등장해 개발자 경험을 크게 개선했다. 둘을 비교하면 이렇다.

```
Playwright의 장점:
- Microsoft 지원, TypeScript 일급 지원
- Chromium + Firefox + WebKit 동시 지원
- 더 빠른 실행 (특히 병렬 실행)
- 네트워크 인터셉트, API 모킹 내장
- 자동 대기가 더 정교함

Cypress의 장점:
- 실시간 리로드 개발 경험 (테스트 작성 시 즉각 피드백)
- GUI 기반 디버거가 직관적
- 컴포넌트 테스트 지원 (Vitest + Testing Library와 경쟁)
- 한국 커뮤니티 자료가 Playwright보다 많음(2024년 기준)
```

신규 프로젝트라면 Playwright를 선택하는 편이 낫다. Microsoft의 지원, TypeScript 친화성, 세 브라우저 엔진 지원이 강점이다. 기존 Cypress 코드베이스가 있다면 마이그레이션 비용을 따져보고 결정해야 한다.

---

## API 계약 테스트 — 타입 수준의 계약

13장에서 Hono와 tRPC를 다뤘다. 이 도구들의 강점 중 하나가 서버와 클라이언트 사이의 타입 수준 계약이다. 그 계약을 테스트로 검증하는 패턴을 살펴보자.

### Hono RPC + Vitest

Hono의 RPC 클라이언트는 서버 라우트 정의에서 타입을 자동으로 추론한다. 클라이언트에서 잘못된 요청을 보내면 컴파일 타임에 에러가 난다. 이 타입 계약 자체를 테스트할 수 있다.

```typescript
// server/routes/users.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const UserCreateSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export const userRoutes = new Hono()
  .post('/users', zValidator('json', UserCreateSchema), async (c) => {
    const body = c.req.valid('json');
    // body의 타입은 자동으로 { name: string; email: string }
    const user = await createUser(body);
    return c.json(user, 201);
  })
  .get('/users/:id', async (c) => {
    const id = Number(c.req.param('id'));
    const user = await findUser(id);
    if (!user) return c.json({ error: 'Not Found' }, 404);
    return c.json(user);
  });
```

```typescript
// server/routes/users.test.ts
import { describe, it, expect } from 'vitest';
import { testClient } from 'hono/testing';
import { userRoutes } from './users';

describe('User API', () => {
  const client = testClient(userRoutes);

  it('POST /users — 사용자를 생성한다', async () => {
    const res = await client.users.$post({
      json: { name: '홍길동', email: 'hong@example.com' },
    });

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.name).toBe('홍길동');
  });

  it('POST /users — 잘못된 이메일은 400을 반환한다', async () => {
    const res = await client.users.$post({
      // @ts-expect-error — email 형식 오류: 타입 수준에서도 에러
      json: { name: '홍길동', email: 'not-an-email' },
    });
    // 런타임 검증도 실패해야 함
    expect(res.status).toBe(400);
  });
});
```

`testClient`가 편리하다. 실제 HTTP 서버를 띄우지 않고 Hono 앱을 직접 호출한다. 빠르고, 네트워크 의존이 없다. 그리고 `client.users.$post({ json: ... })`에서 `json`의 타입이 서버 스키마와 연동되어 있어, 잘못된 값을 넘기면 컴파일 타임에 에러가 난다.

### tRPC + Vitest

tRPC는 한 걸음 더 나아간다. 별도 스키마나 코드 생성 없이 순수 TypeScript 타입으로 서버와 클라이언트를 연결한다.

```typescript
// server/router.ts
import { initTRPC } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.create();

export const appRouter = t.router({
  user: t.router({
    getById: t.procedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input }) => {
        return { id: input.id, name: '홍길동', email: 'hong@example.com' };
      }),
    create: t.procedure
      .input(z.object({ name: z.string(), email: z.string().email() }))
      .mutation(async ({ input }) => {
        return { id: 1, ...input };
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

```typescript
// server/router.test.ts
import { describe, it, expect } from 'vitest';
import { createCallerFactory } from '@trpc/server';
import { appRouter } from './router';
import { expectTypeOf } from 'vitest';

const createCaller = createCallerFactory(appRouter);

describe('tRPC user router', () => {
  const caller = createCaller({});

  it('user.getById — 사용자를 반환한다', async () => {
    const user = await caller.user.getById({ id: 1 });
    expect(user.id).toBe(1);
    expect(user.name).toBe('홍길동');
  });

  it('user.getById — 반환 타입 검증', async () => {
    const user = await caller.user.getById({ id: 1 });
    // 런타임 값 검증
    expect(typeof user.id).toBe('number');
    // 타입 수준 검증
    expectTypeOf(user).toMatchTypeOf<{ id: number; name: string; email: string }>();
  });

  it('user.create — 사용자를 생성한다', async () => {
    const user = await caller.user.create({
      name: '김철수',
      email: 'kim@example.com',
    });
    expect(user.name).toBe('김철수');
  });
});
```

`createCaller`가 HTTP 없이 라우터를 직접 호출한다. 테스트가 빠르고 간단하다. `expectTypeOf`로 반환 타입까지 검증하면 런타임과 컴파일 타임을 동시에 커버한다.

---

## CI에서의 typecheck — `tsc --noEmit`을 테스트 스텝으로

테스트 파이프라인에서 놓치기 쉬운 스텝이 있다. TypeScript 타입 검사를 별도 CI 스텝으로 명시적으로 추가하는 것이다.

Vitest는 TypeScript를 esbuild로 트랜스파일해서 실행한다. 빠르지만, 타입 검사를 하지 않는다. 타입 에러가 있어도 Vitest는 그냥 실행한다. 마찬가지로 Vite로 빌드할 때도 기본적으로 타입 검사를 하지 않는다.

```bash
# 이 명령은 타입 에러를 잡아준다
tsc --noEmit
```

`--noEmit` 옵션은 컴파일된 JS 파일을 생성하지 않고 타입 검사만 한다. 이 명령을 CI 파이프라인에 별도 스텝으로 추가해야 한다.

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      # 타입 검사 — 별도 스텝
      - name: TypeScript 타입 검사
        run: npx tsc --noEmit

      # 단위 테스트
      - name: Vitest 단위 테스트
        run: npx vitest run

      # E2E 테스트
      - name: Playwright E2E 테스트
        run: npx playwright install --with-deps && npx playwright test
```

이 세 스텝이 모두 통과해야 PR이 머지될 수 있어야 한다. `tsc --noEmit`이 없으면 타입 에러가 있는 코드가 CI를 통과해버리는 찜찜한 상황이 생긴다.

`package.json`에도 스크립트를 명확히 정의해두는 편이 낫다.

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "ci": "npm run typecheck && npm run test:run && npm run test:e2e"
  }
}
```

`npm run ci`가 타입 검사, 단위 테스트, E2E 테스트를 순서대로 실행한다. 로컬에서도 PR을 올리기 전에 이 명령을 한 번 돌려보는 습관을 들이면 좋다.

### 타입 검사 성능 개선

대규모 프로젝트에서 `tsc --noEmit`이 느리게 느껴질 수 있다. 몇 가지 방법이 있다.

**`tsc --incremental --noEmit`** — 이전 빌드 결과를 캐시해 변경된 파일만 다시 검사한다. `tsconfig.json`에 `"incremental": true`를 추가하면 `.tsbuildinfo` 파일을 생성해 캐시를 유지한다.

```json
// tsconfig.json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo",
    "noEmit": true
  }
}
```

**`project references`** — 13장 모노레포 섹션에서 언급한 프로젝트 참조를 쓰면 하위 패키지를 독립적으로 타입 검사할 수 있다. 변경이 없는 패키지는 캐시된 결과를 쓴다.

**2025년 이후: TypeScript Native** — Microsoft가 2025년 발표한 Go 언어로 재작성된 TypeScript 컴파일러(코드명 TypeScript Native 또는 TypeScript Go)는 기존 대비 10배 빠른 속도를 목표로 한다. 이것이 안정화되면 `tsc --noEmit`의 속도 문제는 자연스럽게 해소될 가능성이 높다.

---

## 테스트 전략 전체 그림

테스트 도구들을 나열했으니 어떻게 조합할지 전략을 정리하자. Java/Spring 프로젝트에서 테스트 피라미드를 설계하듯, TS 프로젝트에서도 레이어를 나눈다.

```
         /\
        /E2E\          ← Playwright (소수, 핵심 사용자 흐름)
       /------\
      /통합 테스트\      ← Vitest + Hono testClient / tRPC caller (중간)
     /------------\
    /  컴포넌트 테스트 \  ← Vitest + Testing Library (React 컴포넌트)
   /------------------\
  /    단위 테스트      \  ← Vitest (많음, 빠름)
 /----------------------\
/     타입 단위 테스트    \  ← expectTypeOf, @ts-expect-error (복잡한 타입마다)
/------------------------\
     typecheck
     tsc --noEmit          ← CI에서 항상
```

타입 단위 테스트는 피라미드의 별도 레이어라기보다 기반이다. 복잡한 타입 유틸리티를 만들 때마다 함께 작성하는 게 바람직하다. `expectTypeOf`는 코드 비용이 낮다 — 런타임이 없고, 빠르고, 단 두 줄로 타입 계약을 명문화할 수 있다.

현실적인 선택을 정리하면 이렇다.

```
신규 프로젝트 기준 추천 스택:
- 타입 검사: tsc --noEmit (CI 필수 스텝)
- 단위·통합 테스트: Vitest
- 타입 단위 테스트: Vitest의 expectTypeOf (또는 expect-type)
- 컴포넌트 테스트: Vitest + Testing Library
- E2E: Playwright
- 프로퍼티 기반: fast-check (필요한 경우)
```

---

## 🚧 함정 박스 — 타입 테스트의 흔한 실수들

**함정 1: `@ts-expect-error`와 `@ts-ignore` 혼동**

증상: 타입 에러를 억제하려고 `@ts-ignore`를 썼는데, 실제로 에러가 없는 코드에도 붙어있어 아무런 의미 없이 남아 있다.

원인: `@ts-ignore`는 에러 유무와 관계없이 다음 줄을 무조건 무시한다. `@ts-expect-error`는 에러가 있어야 하고, 에러가 없으면 오히려 컴파일 에러를 낸다.

처방: 타입 에러를 의도적으로 검증할 때는 `@ts-expect-error`를 써야 한다. 임시로 에러를 억제할 때만 `@ts-ignore`를 쓰되, 주석으로 이유를 명시하는 편이 낫다.

**함정 2: vi.fn() 타입이 any로 추론됨**

증상: `vi.fn()`으로 만든 mock 함수가 `MockedFunction<any>`가 되어 매개변수나 반환 타입이 전혀 검증되지 않는다.

원인: 타입 매개변수를 명시하지 않으면 any로 추론된다.

처방:
```typescript
// 나쁜 예
const mockSave = vi.fn();

// 좋은 예
const mockSave = vi.fn<(user: User) => Promise<void>>();
// 또는
const mockSave: MockedFunction<(user: User) => Promise<void>> = vi.fn();
```

**함정 3: vi.mock() 경로가 절대 경로여야 하는 경우**

증상: `vi.mock('./userRepository')`가 작동하지 않거나, mock이 적용되지 않는다.

원인: `vi.mock()`의 경로 해석은 tsconfig의 `paths` 별칭을 항상 인식하지는 않는다. `vi.mock('@/repository/user')`처럼 별칭 경로를 쓰면 실패하는 경우가 있다.

처방: `vite.config.ts`의 `resolve.alias`와 `vitest.config.ts`의 설정을 일치시켜야 한다. 또는 mock 경로를 상대 경로로 명시한다.

**함정 4: E2E 테스트에서 auto-waiting을 믿지 못해 불필요한 sleep 추가**

증상: `await page.waitForTimeout(2000)` 같은 하드코딩된 대기가 테스트 곳곳에 있다. 테스트가 느리고 불안정하다.

원인: Playwright의 auto-waiting을 이해하지 못하거나, 특정 조건에서 신뢰하지 못할 때.

처방: `page.waitForTimeout`보다 `expect(locator).toBeVisible()`, `page.waitForURL()`, `page.waitForResponse()` 같은 조건 기반 대기를 써야 한다. 조건 기반 대기는 조건이 충족되면 즉시 다음으로 넘어가서 빠르다.

---

## 마무리

Java/Kotlin 개발자가 TS 테스트 생태계에서 마주치는 가장 큰 변화는 두 가지다.

하나는 *도구 선택의 자유*다. JUnit은 사실상 단일 표준이었다. TS에서는 Vitest와 Jest, Playwright와 Cypress 사이에서 팀이 선택을 해야 한다. 2025년 현재 기준으로 신규 프로젝트에는 Vitest + Playwright 조합이 합리적 디폴트다. 레거시 코드베이스라면 Jest를 유지하는 게 현실적일 수 있다.

다른 하나는 *타입 단위 테스트*라는 새로운 레이어다. `expectTypeOf`, `@ts-expect-error` — Java에는 없던 이 도구들은 처음엔 낯설지만, 복잡한 타입 유틸리티를 만들수록 그 가치가 분명해진다. 4·5장에서 공들여 만든 `DeepReadonly`, `ExtractRouteParams`, `z.infer` 같은 타입들이 실제로 의도한 모양인지 검증하는 방법은 `expectTypeOf`뿐이다.

기억해두자. `tsc --noEmit`을 CI 필수 스텝으로 두는 것, `vi.fn()`에 타입을 명시하는 것, `@ts-expect-error`로 타입 에러를 명시적으로 검증하는 것 — 이 세 가지 습관이 TS 테스트의 기반이다.

15장에서는 한국 현장에서 TS를 쓰다 마주치는 함정들을 더 넓은 시각으로 살펴본다. 이 장에서 다룬 테스트 패턴들, 그리고 4~13장의 모든 내용이 실제 팀에서 어떻게 충돌하고 어떻게 합의점을 찾는지 — 한국 개발자들의 생생한 경험으로 마지막 장을 채운다.

---

> **📖 더 깊이 가려면**
>
> - **Vitest 공식 문서** — https://vitest.dev/ : 설정 옵션, 고급 mocking 패턴, 스냅샷 테스트
> - **Testing Library 철학** — https://testing-library.com/docs/guiding-principles : "사용자가 소프트웨어를 사용하는 방식과 유사한 방식으로 테스트하라"의 원칙
> - **expect-type** — https://github.com/mmkal/expect-type : 타입 테스트 API 전체
> - **Playwright 공식 문서** — https://playwright.dev/ : Page Object Model, 네트워크 인터셉트, 병렬 실행 고급 설정
> - **fast-check 공식** — https://fast-check.io/ : Arbitrary 정의, shrinking 원리, 실전 예제
> - **Matt Pocock - Total TypeScript** — https://www.totaltypescript.com/ : 타입 단위 테스트를 포함한 고급 TS 타입 패턴의 현재 최고 자료 (영문)
> - **Hono testClient** — https://hono.dev/docs/guides/testing : Hono 앱을 HTTP 없이 테스트하는 패턴

---

# 6부 — 종합

모든 장을 걸었다. 이제 마지막 한 걸음 — 지금까지 쌓은 모든 것을 한국 현장의 현실에 대조해 보는 시간이다. 어디서 미끄러지는지, 어떤 논쟁이 아직 결론 나지 않았는지, AI가 코드를 짜는 시대에 사람이 서야 할 자리가 어디인지, 이 책을 덮은 다음 어디로 걸어가야 하는지. 15장은 새로운 개념을 쌓는 장이 아니라, 지도를 손에 쥐고 방향을 확인하는 장이다.

이 부에서 만나는 챕터:
- 15장. 한국 현장의 TypeScript — 함정·논쟁·AI 시대·다음 한 걸음

---


> 14장에서 테스트 전략의 전모를 익혔다. 이제 마지막 장이다. 지금까지 걸어온 길에서 한국 현장이 어디에서 자주 미끄러지는지를 지도로 그리고, 업계의 미결 논쟁들을 균형 있게 정리하고, 이 책을 덮은 다음 어디로 더 깊이 들어갈 수 있는지를 안내하는 자리. 15장으로 마무리하자.

# 15장. 한국 현장의 TypeScript — 함정·논쟁·AI 시대·다음 한 걸음

입사 첫날을 떠올려보자. 이력서에 Spring Boot 5년, Kotlin 3년을 써서 냈는데, 팀 리드가 슬랙으로 링크 하나를 보내온다. "프론트도 같이 봐야 해서요, TypeScript 리포지터리예요." 당연히 열어본다. 코드를 스크롤하는 동안 눈이 미묘하게 흔들린다. `any`가 여기저기 널려 있고, `tsconfig.json`은 옵션이 수십 개다. 익숙한 `@RestController`, `@Service`, `@Autowired`는 없고, 예외 처리가 어디서 이루어지는지 당장 눈에 들어오지 않는다. 무엇보다 이상한 건, 분명히 타입이 있는데도 런타임에서 `TypeError: Cannot read properties of undefined`가 튀어나온다는 점이다.

"타입이 있으면 안전한 거 아닌가?" — 이 질문을 처음 품는 순간이 Java/Kotlin 개발자가 TypeScript를 진지하게 배우기 시작하는 순간이다. 타입이 있어도 안전하지 않을 수 있다는 사실, 그리고 그 이유를 이해하는 것이 이 책 전체의 뼈대였다.

이 책은 그 질문에서 출발했다. 1장에서 TS가 JS의 슈퍼셋이라는 말의 진짜 의미를 짚었다. 언어 스펙이 아니라 타입 체커를 씌운다는 것, 그리고 그 타입 체커가 런타임에는 존재하지 않는다는 것. 2장에서 구조적 타입 시스템의 작동 원리를 파헤쳤다. Java의 명목적 타입과 달리 TypeScript는 형태(shape)가 같으면 같다고 보고, 그 관대함이 어디서 독이 되는지를 봤다. 3장에서는 타입 좁히기와 discriminated union으로 런타임 안전성을 타입 레벨로 끌어올리는 패턴을 익혔다. 4장에서 제네릭이 Java 제네릭과 어떻게 닮고 어떻게 다른지를 비교했다. 5장에서 유틸리티 타입과 타입 연산으로 반복 없이 타입을 조합하는 법을 배웠다. 6장에서 비동기와 에러 — TypeScript 생태계에서 가장 조용히 실수가 쌓이는 영역 — 를 다뤘다. 7장은 this의 함정, 8장은 모듈 시스템과 빌드 도구, 9장은 의존성 주입과 IoC 컨테이너, 10장은 마이그레이션 전략, 11장은 TS를 도구로 실행하는 CLI와 런타임 환경, 12장은 프론트엔드 프레임워크, 13장은 풀스택과 백엔드 프레임워크, 14장은 테스트 전략이었다.

이제 마지막 장이다. 마지막 장의 역할은 새로운 개념을 쌓는 것이 아니다. 지금까지 걸어온 길에서 한국 현장이 어디에서 자주 미끄러지는지를 지도로 그리고, 업계에서 아직 결론이 나지 않은 논쟁들을 균형 있게 정리하고, AI가 TS 코드를 짜는 시대에 사람이 서야 할 자리를 짚고, 이 책을 덮은 다음 어디로 더 깊이 들어갈 수 있는지를 안내한다. 지도와 닫음의 챕터다.

---

## 한국 현장의 함정 — 다섯 가지 카테고리

Java/Kotlin 배경의 개발자가 TypeScript에서 실수를 저지르는 패턴은 무작위가 아니다. 반복된다. 수십 명의 선배가 이미 같은 자리에서 미끄러졌고, 같은 PR 코멘트를 받았고, 같은 밤샘 디버깅을 했다. 그 자리를 미리 알면 최소한 "아, 이게 그 함정이구나" 하고 잠시 멈출 수 있다. 지뢰를 제거하는 것도 가능하지만, 지뢰가 어디 있는지를 아는 것이 먼저다.

리서치와 커뮤니티 경험을 통해 수집한 함정은 12개다. 각 함정의 상세 증상과 처방은 **부록 D**에서 다룬다. 여기서는 큰 카테고리 다섯 개로 묶어 위치를 표시한다. 지도를 그리는 것이 목적이므로, 세부 지형보다 지형의 이름과 대략적인 위치를 먼저 알아두자.

---

### 카테고리 1: 타입 통제의 실패 — `any`의 전염과 구조적 타입의 헐렁함

첫 번째이자 가장 흔한 카테고리는 타입 자체를 잃어버리는 실수다. 타입이 있는 언어를 쓰면서 타입을 잃어버린다는 말이 모순처럼 들리겠지만, TypeScript에서는 충분히 가능한 일이다.

`any`는 TypeScript가 제공하는 공식적인 탈출구다. "이 값의 타입은 신경 쓰지 않겠다"는 선언이다. 타입 추론이 막혔을 때, 서드파티 라이브러리의 타입 정의가 부정확할 때, 마이그레이션 중에 일단 통과시키고 싶을 때 `any`를 쓴다. 문제는 `any`가 전염된다는 것이다.

상황을 그려보자. 동료가 API 응답을 파싱하는 함수 하나에 `any`를 붙였다. 반환 타입이 `any`다. 그 반환값을 받는 변수도 자동으로 `any`가 된다. 그 변수를 인자로 받는 함수도, 그 함수가 돌려주는 값도, 그 값을 사용하는 컴포넌트의 props도 전부 `any`로 오염된다. 처음에는 파일 하나였는데, 한 달 후에는 프로젝트 절반이 `any`의 바다가 되어 있다. 어느 시점부터는 타입 체커가 사실상 꺼진 것과 다름없다. 그런데 IDE는 아무 빨간 줄도 그어주지 않는다. `any`는 "모든 타입과 호환된다"는 선언이기 때문이다.

팀 전체가 `strict: true`를 켜지 않은 채 개발하다 보면 이 상황이 더 빨리 온다. `strict` 모드 없이는 `noImplicitAny`가 꺼져 있어서, 타입 추론이 `any`로 귀결될 때 경고 없이 통과한다. 2장에서 프로젝트를 시작하자마자 `strict: true`를 켜라고 강하게 권한 이유가 여기에 있다.

구조적 타입의 헐렁함은 다른 종류의 함정이다. Java나 Kotlin에서 `UserId`와 `OrderId`는 서로 다른 클래스다. 컴파일러가 두 타입을 혼동하면 바로 에러를 낸다. TypeScript의 구조적 타입 시스템에서는 둘 다 `number`라면, 혹은 둘 다 `{ value: number }` 형태라면, 두 타입은 서로 호환된다. `createOrder(userId: OrderId)`에 `UserId` 값을 넣어도 컴파일러가 통과시킨다.

이를 막으려면 branded type 패턴이 필요하다. `type UserId = number & { readonly __brand: 'UserId' }`처럼 구조에 유일한 식별자를 붙이는 방식이다. 5장에서 이 패턴을 다뤘다. 그런데 실무에서 branded type을 프로젝트 초기부터 전면 도입하는 팀은 드물다. "나중에 필요해지면 하면 되지"라는 판단이 앞선다. 대부분은 버그가 터지고 원인을 추적하다 "어, 여기서 UserId를 OrderId 자리에 넣었네"를 발견한 뒤에야 패턴을 도입한다.

이 카테고리에 속하는 함정은 **부록 D의 함정 1번(묵시적 any와 strict 모드)**과 **함정 2번(구조적 타입의 헐렁함과 branded type)**이다. 두 함정 모두 코드베이스 초기 설정 단계에서 결정이 난다. 나중에 고치려면 전체 코드를 뒤집어야 한다. 처음 설정에 주의를 기울이는 편이 백배 낫다.

타입 통제 실패의 세 번째 축이 있다. `this` 바인딩의 유실이다. Java와 Kotlin에서 `this`는 항상 현재 클래스 인스턴스를 가리킨다. TypeScript에서도 클래스 메서드 안에서는 마찬가지지만, 메서드를 변수에 담거나 콜백으로 넘기는 순간 `this`가 사라진다.

```typescript
class PaymentService {
  private readonly fee = 0.03;

  calculateFee(amount: number): number {
    return amount * this.fee; // this.fee = 0.03
  }
}

const service = new PaymentService();
const calc = service.calculateFee; // 메서드를 변수에 담음
calc(1000); // TypeError: Cannot read properties of undefined (reading 'fee')
```

`calc`를 직접 호출하면 `this`가 `undefined`다. 이벤트 핸들러나 타이머 콜백에 클래스 메서드를 그대로 넘기면 이 함정에 빠진다. 해결은 화살표 함수로 메서드를 정의하거나 `bind(this)`를 쓰는 것이다. 7장에서 다뤘다. 이 함정은 **부록 D의 함정 3번(`this`가 사라진다)**이다.

---

> **📚 Java/Kotlin 시선 — 입사 첫째 주에 자주 헷갈리는 다섯 가지**
>
> Spring/Kotlin 시니어가 TypeScript 코드베이스에 처음 합류할 때, 가장 자주 "응?" 하는 순간들을 구체적으로 정리해보자. 이 목록을 보고 "맞아, 나도 그랬어"가 아니라 "아, 이런 게 있구나"로 읽을 수 있다면 더 좋다.
>
> **① `@Autowired` 대신 생성자 주입인데 DI 컨테이너가 안 보인다**
>
> NestJS는 `@Injectable()` 데코레이터와 모듈의 `providers` 배열로 DI를 구성한다. Spring의 component scan처럼 클래스패스를 전체 스캔하지 않는다. 모듈에 명시적으로 등록하지 않은 클래스는 주입되지 않는다. "왜 주입이 안 되지?" 하며 한 시간 이상 헤매는 경우가 많다. 9장의 NestJS 모듈 구조를 다시 보면 도움이 된다.
>
> **② `interface`와 `type alias`가 둘 다 있는데 언제 뭘 써야 하는가**
>
> Java에서 `interface`는 계약이고 `class`는 구현이다. TypeScript에서 `interface`와 `type alias`는 많은 경우 교환 가능하지만 미묘하게 다르다. 선언 병합(declaration merging)은 `interface`에서만 된다. 즉, 같은 이름의 `interface`를 두 번 선언하면 하나로 합쳐지는 것이 TypeScript의 의도된 기능이다. 라이브러리 타입 확장에 이 기능이 쓰인다. 처음 보면 당황스럽다.
>
> **③ `null`과 `undefined`가 둘 다 있다**
>
> Java는 null 하나다. TypeScript는 `null`과 `undefined` 두 개다. `strictNullChecks`를 켜면 둘을 명시적으로 구분해야 한다. 함수가 값을 반환하지 않으면 `undefined`를 반환한다. 객체 속성이 선택적(`?`)이면 `undefined`다. 외부에서 명시적으로 "없음"을 전달할 때는 `null`을 쓰는 패턴이 있지만, 코드베이스마다 다르다. "이게 왜 `undefined`야, `null` 아니고?" — 이 질문을 첫 주에 세 번 이상 하게 된다.
>
> **④ `enum`이 있는데 왜 union literal을 쓰라고 하는가**
>
> TypeScript의 `enum`은 Java의 `enum`과 비슷해 보인다. 그런데 수치 열거형(numeric enum)에는 역방향 매핑이라는 함정이 있다. `Direction.UP`의 값이 `0`이고, 동시에 `Direction[0]`이 `"UP"`이 된다. 이 역방향 매핑이 예상치 못한 동작을 만들기도 한다. 커뮤니티의 합의는 `type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT'` 형태의 string literal union을 쓰는 것이다. 처음엔 낯설지만, 실제로 더 예측 가능하고 타입 추론이 잘 된다.
>
> **⑤ `catch (e)`의 `e`는 타입이 없다**
>
> Java에서 `catch (IOException e)`는 `e`의 타입이 `IOException`으로 명시된다. TypeScript에서 `catch (e)`의 `e`는 `unknown` 타입이다(`useUnknownInCatchVariables: true`가 기본인 `strict` 모드에서). `e.message`를 바로 쓰면 컴파일 에러가 난다. `instanceof Error`로 좁혀야 한다. 처음엔 번거롭다고 느껴지지만, 예외가 반드시 `Error` 인스턴스인 것은 아니라는 사실을 인지하고 나면 오히려 안전한 습관이 생긴다. `throw "something went wrong"` 같은 코드를 라이브러리 어딘가가 쓸 수도 있기 때문이다.

---

### 카테고리 2: 비동기와 에러 — 조용히 사라지는 예외들

Java Spring의 예외 처리는 편안하다. `@ControllerAdvice`와 `@ExceptionHandler`를 조합하면 어디서 예외가 터지든 중앙에서 잡힌다. 개별 컨트롤러가 예외를 직접 처리하지 않아도 된다. 스프링 프레임워크가 스택 추적을 로깅하고, 적절한 HTTP 응답을 만들어 돌려준다.

TypeScript/Node.js 생태계에서 이것을 당연하게 기대하면 난감한 상황이 생긴다.

NestJS를 쓴다면 exception filter가 Spring의 `@ControllerAdvice`와 비슷한 역할을 한다. 그런데 Express나 Hono, Fastify를 쓴다면 이 구조를 직접 만들어야 한다. 그리고 만들지 않으면, 예외가 어디선가 터졌는데 HTTP 응답은 그냥 502나 503으로 나가거나, 더 나쁜 경우 응답 자체가 없이 커넥션이 끊어진다.

`async/await`의 에러가 특히 조용하다. `async` 함수 안에서 `throw`된 예외는 그 함수가 반환하는 Promise를 reject 상태로 만든다. 이 Promise를 `await`하지 않으면, 예외는 아무도 잡지 않은 채 공중에 뜬다. 코드를 살펴보자.

```typescript
async function processPayment(orderId: string): Promise<void> {
  // 뭔가 잘못됐을 때 throw
  throw new Error("결제 실패");
}

// await 없이 호출하면?
function handleRequest() {
  processPayment("order-123"); // await 없음
  console.log("여기까지는 실행된다");
}
```

`handleRequest()`를 실행하면 "여기까지는 실행된다"가 출력된다. 그리고 Promise는 어디서도 잡히지 않는다. Node.js 버전에 따라 조용히 무시되거나, `UnhandledPromiseRejectionWarning`을 출력하거나, 프로세스가 종료된다. 어느 쪽이든 원하는 동작이 아니다.

Java의 checked exception이 답답하게 느껴졌던 개발자도, 이 경험을 하고 나면 솔직해진다. "그래도 checked exception은 잊기 어렵게 만들어놨구나." TypeScript에서는 `async` 함수를 호출할 때 `await`를 빠뜨리는 순간 에러가 공중에 뜬다. IDE나 컴파일러가 경고해주지 않는다. ESLint의 `@typescript-eslint/no-floating-promises` 규칙을 켜면 이 실수를 잡을 수 있다. 켜자.

또 다른 함정은 `async` 함수 내부의 콜백이다.

```typescript
async function processItems(items: string[]): Promise<void> {
  items.forEach(async (item) => {
    await doSomething(item); // 이 await는 forEach의 콜백 안에만 적용된다
  });
  // forEach 자체는 Promise를 기다리지 않는다
}
```

`forEach`에 `async` 콜백을 넘기면 각 콜백이 Promise를 반환하지만, `forEach` 자체는 그 Promise들을 기다리지 않는다. 결과적으로 `processItems`가 반환된 시점에 `doSomething`이 아직 실행 중일 수 있다. 이런 상황에서 `for...of`나 `Promise.all`을 써야 한다.

```typescript
// 순차 처리
async function processItems(items: string[]): Promise<void> {
  for (const item of items) {
    await doSomething(item);
  }
}

// 병렬 처리
async function processItemsParallel(items: string[]): Promise<void> {
  await Promise.all(items.map((item) => doSomething(item)));
}
```

이 카테고리의 함정은 **부록 D의 함정 4번(비동기 에러의 실종)**이다. 6장에서 이 패턴들을 더 깊이 다뤘다.

비동기와 에러 카테고리에서 특히 한국 현장에서 자주 등장하는 추가 패턴이 있다. NestJS를 쓰는 팀에서 TypeORM이나 Prisma 트랜잭션을 다룰 때다. Spring의 `@Transactional`은 선언적으로 트랜잭션 경계를 설정한다. TypeORM에서는 `QueryRunner`를 직접 관리하거나 `dataSource.transaction()` 콜백을 써야 한다. Prisma는 `prisma.$transaction()` 콜백 방식이다. 이 콜백 안에서 `async` 작업이 여러 개 있을 때 하나라도 `await`를 빠뜨리면 트랜잭션이 커밋된 뒤에야 에러가 감지되거나, 에러가 아예 감지되지 않는다.

```typescript
// 위험한 패턴 — Prisma 트랜잭션 안에서 await 누락
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  // await를 빠뜨렸다
  tx.order.create({ data: { userId: user.id, ...orderData } }); // 트랜잭션 밖에서 실행될 수 있다
});

// 안전한 패턴
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  await tx.order.create({ data: { userId: user.id, ...orderData } });
});
```

Spring의 `@Transactional`에 익숙한 개발자가 이 차이를 인지하지 못하면, 데이터 정합성 버그가 프로덕션에서 조용히 발생한다. 에러가 나지 않기 때문에 더 찾기 어렵다.

---

### 카테고리 3: 도구 분열 — CJS/ESM, tsconfig 지옥, monorepo IDE 폭주

TypeScript 생태계에서 가장 찜찜한 영역을 꼽자면 도구 설정이다. Java Maven이나 Gradle에서는 빌드 설정이 상대적으로 단순하다. `pom.xml`이나 `build.gradle`에 의존성을 선언하고 플러그인을 붙이면 대부분 돌아간다. TypeScript는 다르다.

**CommonJS와 ESM의 공존**부터 이야기하자. Node.js가 오랫동안 CommonJS(`require()`/`module.exports`) 방식으로 모듈을 불러왔다. ECMAScript 표준은 ESM(`import`/`export`)을 정의했고, Node.js가 뒤늦게 지원했다. 문제는 수십만 개의 npm 패키지가 여전히 CommonJS 기반이라는 점이다. 순수 ESM 패키지는 CommonJS 환경에서 `require()`로 불러올 수 없다. 반대 방향도 마찬가지다.

`package.json`에 `"type": "module"`을 추가하면 Node가 해당 패키지를 ESM으로 취급한다. 그런데 이 한 줄이 기존에 잘 돌아가던 CommonJS 코드를 깨트린다. `ERR_REQUIRE_ESM` 에러가 나온다. 이 에러를 처음 보는 순간 멍해진다. 에러 메시지가 원인을 알려주긴 하지만, 해결 방법은 여러 개고 각각 트레이드오프가 있다.

상황을 더 복잡하게 만드는 것이 `tsconfig.json`이다. TypeScript 컴파일러 옵션은 70개가 넘는다. 그 중에서 `target`, `module`, `moduleResolution`의 조합이 핵심이다.

- `target`: 컴파일된 JS가 어떤 ECMAScript 버전을 지향하는가
- `module`: 생성될 모듈 코드가 CommonJS인가 ESM인가 등
- `moduleResolution`: 모듈 이름을 파일 시스템에서 어떻게 찾는가

이 세 옵션의 조합이 어긋나면 기묘한 상황이 생긴다. 코드는 런타임에 동작하는데 IDE가 빨간 줄을 그어놓거나, IDE는 통과했는데 빌드가 깨지거나, 빌드까지 통과했는데 런타임에서 모듈을 못 찾는 에러가 난다. Matt Pocock의 tsconfig cheat sheet가 한국 개발자들 사이에서 필수 북마크가 된 이유가 여기에 있다. 수십 개의 옵션 중에서 현재 상황(Node.js 서버인지, 브라우저 번들인지, 라이브러리인지)에 맞는 조합이 정해져 있다는 것을 알면 훨씬 단순해진다.

Node.js 서버(ESM)를 위한 최소 설정을 예로 들면:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "strict": true
  }
}
```

`module`과 `moduleResolution`을 `Node16`으로 맞추면 Node.js의 ESM 동작 방식을 TypeScript가 정확히 이해한다. 이 설정 없이는 `.js` 확장자를 import 경로에 붙여야 하는 이유를 IDE가 이해하지 못한다.

monorepo를 도입하면 한 단계 더 복잡해진다. 여러 패키지가 각자의 `tsconfig.json`을 가지면서 서로를 참조할 때, TypeScript의 project references(`tsconfig.references`) 기능을 써야 IDE의 언어 서버가 각 패키지의 경계를 올바르게 인식한다. 이것 없이 수십 개의 패키지를 monorepo에 놓으면 IDE의 TypeScript 서버가 모든 파일을 하나의 거대한 프로젝트로 인식하려 들고, 메모리와 CPU를 폭주시킨다. 에디터가 느려지거나 멈추는 증상이 나온다.

카카오의 "TypeScript Monorepo with pnpm" 기술블로그 글과 당근의 "한 모노레포에서 1000명이 일하는 법"이 한국 학습의 표준 레퍼런스가 된 것은 이 문제가 그만큼 보편적이기 때문이다. 같은 문제로 고생하는 개발자들이 많았고, 그 경험을 글로 남긴 팀들이 있다.

이 카테고리의 함정은 **부록 D의 함정 5번(CJS/ESM 혼란), 함정 6번(tsconfig 지옥), 함정 12번(monorepo IDE 폭주)**이다. 8장에서 이 영역을 다뤘다.

---

### 카테고리 4: 직무 비대칭 — 백엔드는 Spring, 프론트는 TS

이것은 순수한 기술 문제가 아니다. 한국 IT 시장의 구조에서 오는 문제다. 그러나 그 구조가 기술 선택과 학습 경로에 직접 영향을 미친다.

한국 IT 대기업과 SI 업계에서 백엔드는 Java/Spring이 압도적으로 지배한다. 채용 공고를 보면 "Node.js 백엔드" 또는 "NestJS"를 찾는 공고는 Spring 백엔드 대비 한 자릿수 비율이다. 반면 신규 채용 공고에서 TS Node.js 백엔드 비율은 빠르게 늘고 있다. 신생 스타트업, 핀테크, 플랫폼 기업(토스, 당근, 라인, 쿠팡 일부 팀)에서는 이미 Node.js 백엔드가 표준이 된 곳도 있다.

프론트엔드는 이야기가 다르다. TypeScript 없이 프론트엔드 개발자 채용 공고를 낸다는 것은 이미 몇 년째 상상하기 어려운 일이 됐다. "TypeScript 안 쓰면 면접 컷"이라는 말이 정설로 굳어졌다.

이 비대칭이 만드는 문제가 있다.

첫째, 백엔드 Java 시니어가 풀스택 또는 프론트 역할을 겸해야 하는 상황에 놓인다. TS를 주요 기술로 깊이 배우기보다, "일단 돌아가는" 수준에서 사용하게 된다. `any`로 때우고, 에러 처리를 대충 하고, 타입이 실제로 안전한지 확인하지 않는다. 이 태도가 팀 코드베이스 전체의 품질을 갉아먹는다.

둘째, 프론트엔드 TS 시니어가 백엔드 역할을 맡으면, NestJS의 모듈 DI 구조, TypeORM 또는 Prisma의 트랜잭션 처리, 인프라와 배포 관리에서 Spring 경험 없이 혼란스러워한다. TS를 잘 쓴다고 NestJS의 아키텍처를 자동으로 이해하지는 않는다. Java/Spring의 아키텍처 개념이 배경에 있어야 NestJS가 왜 그렇게 설계됐는지가 보인다.

셋째, 팀 내에서 백엔드(Java)와 프론트(TS) 개발자 간의 기술 언어가 달라진다. 백엔드는 Spring MVC, 서블릿 컨텍스트, JPA의 개념으로 이야기하고, 프론트는 React 렌더 사이클, 상태 관리, 번들 최적화 언어로 이야기한다. 두 팀이 같은 테이블에 앉아도 서로 다른 문제를 보고 있는 경우가 많다. API 설계 회의가 이 간극의 가장 뚜렷한 현장이다.

이 책이 Java/Kotlin 개발자를 독자로 설정한 이유가 이 비대칭에 있다. 백엔드 강자의 지식과 직관을 TypeScript 전환에서 최대한 살릴 수 있도록, 공통점과 차이점을 명확히 보여주는 것이 이 책의 목표였다.

---

> **📚 Java/Kotlin 시선 — 한국 채용시장 비대칭 분석**
>
> | 구분 | 백엔드 | 프론트엔드 |
> |------|--------|------------|
> | 지배 기술 | Java/Spring | TypeScript + React |
> | Node.js/TS 서버 비율 | 신생 스타트업·핀테크·플랫폼 한정 | — |
> | TypeScript 필수 여부 | 선택 (증가 중) | 사실상 필수 |
> | NestJS 채용 현황 | 점진 증가 (라인플러스, 쿠팡 일부, 토스) | — |
> | 학습 동기 | 풀스택 전환, 사이드 프로젝트, 경력 다변화 | 취업·이직 직결 |
> | 주요 학습 레퍼런스 | NestJS 공식 문서, Spring 비교 글, 이 책 | React 공식, velopert, 토스 블로그 |
> | 코드 리뷰 갈등 | "`any` 쓰지 말라"는 프론트 리뷰어 vs "왜?"라는 백엔드 PR 작성자 | — |
>
> 이 비대칭은 단순히 시장 정보로 그치지 않는다. 팀 온보딩 설계, 코드 리뷰 기준, 기술 세미나 주제 선택에서도 이 차이를 인식해야 한다. 백엔드 시니어에게 React Hook의 의존성 배열을 설명하는 방식과, 프론트 시니어에게 NestJS 모듈 등록 방식을 설명하는 방식은 다르다. 이 책이 "Java/Kotlin 개발자를 위한"이라는 부제를 달고 있는 것은 그런 맥락에서다. 배경에 따라 무엇이 낯설고 무엇이 익숙한지가 달라진다. 낯선 것을 낯설다고 인정하는 것이 배움의 시작이다.

---

### 카테고리 5: 학습 자원 미스매치 — 깊이가 빠진 한국어 자료

다섯 번째 카테고리는 기술 문제가 아니라 학습 자원의 문제다. "어디서 배우느냐"가 "무엇을 배우느냐"를 결정한다.

TypeScript의 한국어 학습 자원은 양적으로는 충분하지만, 깊이의 편차가 크다. 기초 문법과 기본 사용법을 다루는 자료는 넘친다. "인터페이스 쓰는 법", "제네릭 기초", "tsconfig 설명" 같은 내용은 검색하면 수십 개가 나온다. 그런데 "왜 TypeScript의 타입 시스템이 이렇게 설계됐는가", "구조적 타입과 명목적 타입의 트레이드오프는 무엇인가", "점진적 타입 시스템의 이론적 배경은 무엇인가"를 한국어로 체계적으로 설명한 단일 자료는 드물다.

결과적으로 많은 개발자가 "어떻게 쓰는가"는 알지만 "왜 이렇게 작동하는가"를 모른다. 이 공백이 실무에서 원인 불명의 타입 에러를 만날 때 드러난다. 에러 메시지가 나오는데 왜 나오는지 이해하지 못한다. 해결책을 검색해 복사-붙여넣기 하고 되면 넘어간다. 패턴을 이해하지 못했으니 다음 번에 비슷한 상황이 오면 또 같은 과정을 반복한다.

이 책이 그 빈자리를 채우려 했다. "TypeScript는 이렇게 쓰세요"가 아니라 "TypeScript는 왜 이렇게 생겼는가"를 설명하는 것이 이 책의 약속이었다. 그 약속이 얼마나 이루어졌는지는 독자가 판단할 몫이다.

이 카테고리의 함정은 **부록 D의 함정 8번(런타임 선택 불안)**과 **함정 7번(빌드 도구 피로)**에서 구체적으로 드러난다. "선택지가 너무 많아서 뭘 골라야 할지 모르겠다"는 상태가 학습 자원 미스매치의 가장 흔한 증상이다.

한 가지 덧붙이자. 학습 자원 미스매치가 가장 치명적으로 드러나는 순간이 있다. 공식 문서와 실무 사이의 간극이다. TypeScript 공식 핸드북은 언어 기능을 잘 설명하지만, "실제 프로젝트에서 `tsconfig.json`을 어떻게 세팅하는가", "monorepo에서 패키지 사이의 타입을 어떻게 공유하는가", "Next.js App Router와 서버 액션의 타입을 어떻게 설계하는가"를 체계적으로 설명하지 않는다. 이 간극을 한국어로 채운 자료가 드물다. 결국 영어 블로그, GitHub 이슈, Stack Overflow 답변을 조합해서 퍼즐을 맞추는 과정을 거친다. 이 과정이 번거롭다. 시간이 오래 걸린다. 그리고 각자가 파편적으로 배운 내용이 팀 안에서 충돌하면 "왜 이렇게 설정했어요?"라는 질문이 나온다.

이 간극을 줄이는 가장 실용적인 방법은 팀 위키에 "우리 프로젝트의 TypeScript 설정 결정 기록"을 남기는 것이다. `tsconfig.json`의 각 옵션을 왜 이렇게 설정했는지, 빌드 도구를 왜 이것을 골랐는지를 짧게라도 문서화해두면 온보딩 비용이 크게 줄어든다.

---

## 일곱 개의 논쟁 — 결론이 없는 것들을 균형 있게 보는 법

기술 논쟁에서 한쪽 입장만 옳은 경우는 거의 없다. 맥락이 결론을 바꾼다. 팀 규모, 프로젝트 수명, 기존 스택, 팀원의 배경, 서비스 특성이 모두 "어떤 선택이 낫다"를 결정한다. 여기서는 TypeScript 생태계에서 현재 진행 중인 일곱 개의 논쟁을 정리한다. 강요가 아니라 지도다. 각 논쟁에서 어느 입장이 맞는지는 각자의 맥락에서 판단해야 한다. 이 책은 그 판단에 필요한 정보를 제공하는 것까지만 책임진다.

---

### 논쟁 A: TypeScript는 JS의 올바른 길인가, 또 다른 복잡성 레이어인가

이 논쟁은 TypeScript 생태계의 근본적인 정당성 논쟁이다. "TS를 써야 하는가"가 이미 정착된 팀에서는 한가한 질문처럼 들리겠지만, 설득해야 하는 사람이 있거나 규모가 작은 팀에서 도입을 고민할 때 다시 나오는 질문이다.

**관점 1 — 옹호:** JS만으로 큰 시스템을 짜본 개발자들은 대부분 TS 없이는 어렵다고 말한다. 함수 하나의 시그니처를 보고 "이 함수가 뭘 받아서 뭘 돌려주는가"를 알 수 있다는 것은 협업의 질을 바꿔놓는다. 코드를 작성한 지 6개월이 지난 뒤에도 타입이 문서 역할을 해준다. Stack Overflow 개발자 설문에서 TypeScript는 수년째 "admired" 비율 상위에 있고, GitHub Octoverse에서의 성장세도 같은 방향을 가리킨다. 시장이 이미 답을 냈다는 입장이다.

**관점 2 — 회의:** 결국 빌드 단계가 추가되고, `tsc`는 대규모 코드베이스에서 느리고, TypeScript의 타입 시스템은 엄밀한 의미에서 sound하지 않다. `any`를 허용하고, 구조적 타입이 과도하게 관대하고, 런타임에 타입 정보가 없다. 진짜 해법은 TC39를 통해 ECMAScript 표준 자체에 타입이 들어오는 것이라고 주장한다. "Type Annotations as Comments" 제안이 그 방향이다. 이 제안이 표준이 되면 TypeScript 없이도 타입 주석을 JS에 직접 쓸 수 있게 된다.

**중간 입장:** TS 5.x와 새로 발표된 Go 재작성 버전(TypeScript Native)으로 도구 측 단점이 줄어들면 회의론의 근거가 약해진다. 완벽하지 않지만, 현재로서는 JS 대규모 시스템에서 최선의 균형이다. "안 쓰는 것보단 낫다"로 수렴하는 것이 한국 커뮤니티의 솔직한 결론이다.

**남은 공백:** JS 표준에 타입이 들어오는 날이 실제로 온다면, TypeScript의 위치는 어떻게 달라질까. 타입 소거(type stripping) 방향과 타입 체크 방향 중 어느 것이 표준이 될 것인가. TC39 제안 동향을 주시할 필요가 있다.

이 논쟁에서 한 가지만 짚고 넘어가자. TypeScript 회의론자들이 흔히 드는 반례가 있다. "타입이 있어도 런타임에서 `undefined`가 나온다. 그럼 타입이 무슨 소용인가?" 이 질문에 대한 정직한 답은 이렇다. TypeScript의 타입은 "이 코드가 절대 안전하다"를 보장하지 않는다. 대신 "이 특정 종류의 실수를 컴파일 타임에 잡는다"를 제공한다. 범위가 제한적이지만, 그 범위 안에서는 실질적이다. 타입이 없는 대규모 JS 코드베이스에서 리팩터링을 해본 사람은 그 차이를 몸으로 안다. 함수 시그니처가 바뀌었을 때 어디가 깨지는지를 컴파일러가 알려주는 것과 런타임에서 발견하는 것의 차이다.

---

### 논쟁 B: Bun/Deno는 Node.js를 대체할 수 있는가

이 논쟁은 2024~2025년 Node.js 생태계에서 가장 뜨거운 주제 중 하나다. 11장에서 런타임 선택을 다뤘는데, 여기서는 산업적 전망을 본다.

**관점 1 — Bun 옹호:** Bun은 Node.js 생태계 호환성을 거의 완전히 끌어왔다. 속도는 압도적이다. 번들링, 테스트 러너, 패키지 매니저를 모두 내장해서 별도 도구 없이 TS 개발이 가능하다. CLI 도구와 개발 툴링 시장에서는 이미 Bun 채택이 상당히 진행됐다. `bun run index.ts`로 TypeScript 파일을 직접 실행할 수 있다는 편리함은 한번 경험하면 돌아가기 어렵다.

**관점 2 — Node.js 잔류:** 11년이 넘는 안정성, 깊은 npm 생태계, 기업의 LTS 의존 사이클은 쉽게 바뀌지 않는다. Bun의 long-running 서버 환경에서의 edge case와 메모리 관련 보고가 있다. 프로덕션 전환 비용이 크고, 무엇보다 "Bun이 프로덕션에서 안정적이다"는 신뢰가 Node.js만큼 쌓이지 않았다.

**관점 3 — Deno의 길:** 보안 모델이 독보적이다. 명시적 권한 없이는 파일 시스템, 네트워크, 환경 변수에 접근할 수 없다. 표준 라이브러리가 내장돼 있어 npm 의존성을 최소화할 수 있다. Deno 2의 npm 호환으로 기존 생태계를 사용할 수 있게 됐다. "보안이 중요한 환경"에서는 Deno가 설득력 있다.

**현재 합의:** 2025년 기준 실용적 분업이 정착되고 있다. 로컬 개발과 CLI 도구는 Bun, 프로덕션 서버는 Node.js, 보안과 표준이 중요한 환경은 Deno. 한국 커뮤니티는 "재미있어 보이지만 프로덕션은 아직"이라는 신중한 정서가 지배적이다. 일본 커뮤니티(Hono 저자가 일본인이다)의 적극성과 비교하면 대비가 뚜렷하다.

**남은 공백:** Bun이 프로덕션 안정성을 공식적으로 보증하는 시점, 그리고 기업이 LTS 수준의 신뢰를 언제 줄 수 있는가. 이 질문이 해소되는 속도가 생태계 이행 속도를 결정한다.

---

### 논쟁 C: NestJS는 새 TC39 데코레이터로 이전할 수 있는가

이 논쟁은 한국 NestJS 사용자에게 특히 예민하다. 라인플러스, 쿠팡, 다수의 핀테크 스타트업이 NestJS를 프로덕션에서 쓰고 있기 때문이다. 새 데코레이터 표준으로 이전하는 문제는 기술적 선택이 아니라 프로덕션 안정성의 문제다.

배경을 정리하자. TypeScript 데코레이터는 두 가지다. 하나는 오래된 `experimentalDecorators` 모드(NestJS, TypeORM, class-transformer가 쓴다), 다른 하나는 TC39에서 표준화된 새 데코레이터(TS 5.0에서 도입). TypeScript 5.0 릴리즈 노트는 명확하게 썼다: "We've decided to make a hard pivot to the new decorators proposal." 새 데코레이터가 공식 방향이다.

**관점 1 — 낙관:** NestJS는 결국 새 데코레이터로 이전한다. 메인테이너들이 그 방향을 인지하고 있고, 시간 문제다. TypeScript 자체가 `experimentalDecorators` 모드를 유지하겠다고 했으니 당장 급박하지 않다.

**관점 2 — 비관:** 문제는 메타데이터 기반 reflection이다. `reflect-metadata` 라이브러리가 새 TC39 데코레이터 표준에 포함되지 않았다. NestJS의 DI 컨테이너는 `reflect-metadata`로 클래스 생성자 파라미터의 타입을 읽어서 주입할 의존성을 결정한다. 이 메커니즘 없이는 DI가 작동하지 않는다. 새 표준 데코레이터로 이전하려면 DI 모델 자체를 재설계해야 한다. 이것은 단순한 마이그레이션이 아니라 프레임워크의 근본을 바꾸는 작업이다.

**공식 입장:** TS는 `experimentalDecorators` 모드를 당분간 유지하겠다고 했다. 즉, NestJS는 지금 당장 breaking change를 강요받지 않는다. 하지만 "당분간"이 얼마나 긴지는 알 수 없다.

**현재 합의:** 신규 프로젝트에서 NestJS를 시작한다면 `experimentalDecorators: true`로 가도 괜찮다. 당장 마이그레이션 계획을 세울 필요는 없지만, NestJS의 공식 이슈 트래커와 로드맵을 팔로우하면서 동향을 주시하는 것이 현명하다.

**남은 공백:** NestJS가 새 데코레이터로 공식 마이그레이션 가이드를 제공하는 시점. 이 책 집필 시점 이후에 상황이 바뀔 수 있으므로, 최신 상태를 반드시 확인하자.

---

### 논쟁 D: `as` vs 타입 가드 vs zod — 어디서 어디까지 검증하는가

타입 단언(`as`)을 쓸 것인가, 타입 가드를 쓸 것인가, zod로 런타임 검증을 할 것인가. 이 질문은 TypeScript를 쓰는 거의 모든 팀에서 한 번씩은 토론이 된다. 팀 컨벤션을 정하지 않으면 코드베이스 내에 세 가지 스타일이 섞여서 일관성이 사라진다.

**관점 1 — `as` 실용주의:** 타입 단언은 개발자가 컴파일러에게 "내가 이 타입을 보장한다"고 말하는 도구다. 책임지고 쓰면 된다. API 응답의 타입을 정확히 아는 상황에서 `response as UserResponse`는 합리적이다. 모든 데이터를 런타임에서 검증하는 것은 과잉이다.

**관점 2 — zod 강경파:** 타입 단언은 컴파일러를 속이는 거짓말이다. `as UserResponse`라고 써도 실제 런타임 데이터가 `UserResponse` 형태인지 보장할 수 없다. API가 스펙을 어기거나, 버전이 바뀌거나, 백엔드 팀이 필드를 추가/삭제하면 런타임 에러가 난다. 외부 입력은 무조건 런타임에서 검증해야 한다.

**관점 3 — boundary validation (사실상 합의):** 이 논쟁에는 실용적 합의가 가장 잘 정착되어 있다. 외부 경계(API 응답, 환경 변수, 폼 입력, 설정 파일, 파일 파싱)에서는 zod나 valibot으로 검증하고, 내부 로직에서는 타입을 신뢰한다. Theo, Colin McDonnell(zod 저자) 등이 정착시킨 이 패턴이 커뮤니티 표준이다.

구체적으로 보면 이렇다.

```typescript
import { z } from 'zod';

const UserResponseSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
});

type UserResponse = z.infer<typeof UserResponseSchema>;

// API 경계에서 검증
async function fetchUser(id: string): Promise<UserResponse> {
  const raw = await api.get(`/users/${id}`);
  return UserResponseSchema.parse(raw); // 실패 시 ZodError
}

// 내부에서는 타입 신뢰
function formatUserName(user: UserResponse): string {
  // user는 검증된 데이터 — 여기서 as를 쓸 필요 없다
  return `${user.email} (${user.role})`;
}
```

경계에서 한 번 검증하면 내부에서는 타입을 믿을 수 있다. `as`로 경계를 넘기는 것은 "내가 검증한다"는 책임 선언이다. zod로 검증하는 것은 "런타임에서도 확인한다"는 실행이다. 팀의 패턴을 명확히 정해두면 논쟁이 줄어든다.

**남은 공백:** zod의 번들 크기(약 14kb gzipped)가 프론트엔드에서 부담이 될 수 있다. valibot(더 가볍다), arktype(TS 타입과 더 강하게 통합) 같은 경량 대안이 성숙하는 속도를 지켜봐야 한다.

이 논쟁에서 Java/Kotlin 개발자에게 특히 흥미로운 관점이 있다. Spring의 `@Valid`와 Bean Validation(`@NotNull`, `@Email`, `@Size`)이 하는 역할을 TypeScript에서는 zod가 한다고 볼 수 있다. Spring에서 `@RequestBody`에 `@Valid`를 붙이면 컨트롤러에 도달하기 전에 검증이 이루어진다. TypeScript/NestJS에서는 `ValidationPipe`와 `class-validator` 데코레이터가 비슷한 역할을 한다. 그런데 `class-validator`는 데코레이터 기반이라 `experimentalDecorators`가 필요하고, 클래스를 써야 한다. zod는 클래스 없이 스키마 객체로 동작한다. NestJS 팀 내에서도 `class-validator` vs zod가 논쟁 주제가 되는 이유다. 기존 Spring 스타일에 익숙하다면 `class-validator`가 편하고, 함수형 스타일을 선호한다면 zod가 더 자연스럽다. 어느 쪽이 "옳다"가 아니라 팀의 코딩 스타일과 정렬이 관건이다.

---

### 논쟁 E: monorepo의 적정 규모는 어디인가

**관점 1 — monorepo first:** 팀이 하나여도 monorepo가 낫다. 코드 공유, refactor 추적, atomic commit, 일관된 린트/테스트 설정이 훨씬 쉽다. "내가 공유 라이브러리를 수정했는데 그게 어느 앱에 영향 미치는지"를 monorepo 내에서 즉시 알 수 있다.

**관점 2 — polyrepo first:** 소규모 팀에서 Turborepo, Nx, pnpm workspace를 설정하고 관리하는 것은 과한 도구다. 필요성을 느끼기 전에 monorepo를 도입하면 설정 복잡도만 늘어난다. polyrepo로 시작했다가 필요할 때 합치는 것이 낫다.

**도구 스펙트럼:** 세 가지 주요 도구가 스펙트럼을 이룬다.

- **pnpm workspace:** 가장 가볍다. 의존성 호이스팅 최적화, symlink 기반 패키지 공유. 도구 자체의 설정이 단순하다.
- **Turborepo:** 빌드 캐싱과 원격 캐시(Remote Cache)가 핵심 기능이다. 대규모 monorepo에서 빌드 시간을 극적으로 줄인다.
- **Nx:** 가장 풍부한 generator와 plugin 생태계. 의존성 그래프 시각화, 영향 분석, 커스텀 task 등 기능이 많다. 그만큼 학습 곡선도 있다.

**현재 합의:** 프로젝트 초기에는 pnpm workspace로 가볍게 시작하고, 빌드 속도가 병목이 되면 Turborepo를 추가하는 것이 실용적인 경로다. Nx는 팀이 충분히 크고 generator가 실질적으로 필요할 때 도입하는 편이 낫다. 한국에서는 카카오, 당근, 토스의 monorepo 사례가 표준 레퍼런스다.

**남은 공백:** monorepo 도입이 팀의 CI/CD 파이프라인, 특히 PR 단위 배포 전략에 미치는 영향. "어느 패키지가 바뀌었을 때 어느 앱만 재배포한다"는 판단을 자동화하는 것이 실제 운영에서 가장 어렵다.

---

### 논쟁 F: 풀스택 메타프레임워크의 부상 — 모바일이 있는 회사는 어떻게 하는가

Next.js App Router의 Server Components와 Server Actions, React Router 7, SvelteKit, Solid Start가 "프론트가 백엔드를 흡수한다"는 시나리오를 현실로 만들고 있다. BFF(Backend for Frontend)가 Server Actions로 대체되고, API 레이어가 사라지는 구조다.

**관점 1 — 풀스택 옹호:** 타입이 서버와 클라이언트를 관통한다. 서버에서 데이터를 가져오는 코드와 클라이언트에서 렌더링하는 코드가 같은 타입 시스템 아래에 있다. BFF를 별도로 운영할 필요가 없다. 개발 속도가 올라가고, 타입 불일치 버그가 줄어든다.

**관점 2 — 분리 유지:** 모바일 앱, 데스크톱 클라이언트, 다른 웹 서비스 등 다중 소비자 환경에서 API는 별도여야 한다. Next.js 풀스택은 "웹만 있는 서비스"를 위한 해법이다. iOS, Android 앱이 동시에 있는 회사에서 Server Actions로 API를 대체하면 모바일 팀이 소비할 방법이 없다.

**관점 3 — server-first 반동:** SPA(Single Page Application)가 과잉 적용됐다는 반성이 있다. Astro의 Islands 아키텍처, HTMX의 서버 사이드 렌더링 부활이 또 다른 방향이다. "자바스크립트를 최소화하자"는 움직임이 server-first 진영을 만들었다.

**한국 현장:** Spring + REST API + React/Vue가 여전히 표준이다. Next.js 풀스택은 신생 스타트업과 핀테크에 한정되고, 모바일 앱을 운영하는 회사라면 REST API를 유지하는 편이 현실적이다. 토스, 당근, 쿠팡이츠처럼 모바일과 웹이 함께 있는 서비스에서는 Server Actions가 API를 완전히 대체하기 어렵다.

**남은 공백:** tRPC, GraphQL 같은 타입-안전 API 레이어가 "풀스택으로 이전하지 않고도 서버-클라이언트 간 타입 안전성을 보장하는" 방향으로 성숙하고 있다. 이 방향이 한국 현장에서 얼마나 빠르게 채택될지.

---

### 논쟁 G: TypeScript 컴파일러는 어디로 가는가 — TS Native, Node strip-types, Bun

이것은 개발 경험(Developer Experience)의 미래에 관한 논쟁이다. 8장에서 현재의 도구 풍경을 다뤘다면, 여기서는 방향을 본다.

**현재의 문제:** `tsc`는 TypeScript로 작성되어 있어 대규모 코드베이스에서 느리다. 대안인 esbuild와 swc는 타입 체크를 수행하지 않는다. 빠른 트랜스파일과 엄밀한 타입 체크 중에서 하나를 선택해야 하는 상황이 지속됐다. 현재 많은 프로젝트가 "빌드는 esbuild/swc로 빠르게, 타입 체크는 tsc로 별도 실행"하는 두 단계 방식을 쓴다.

**관점 1 — TypeScript Native(Go 재작성):** Microsoft가 2025년 발표한 Go로 재작성한 TypeScript 컴파일러가 게임 체인저다. 목표는 10배 이상의 성능 향상이다. 빠른 빌드와 엄밀한 타입 체크를 동시에 얻을 수 있다면, 두 단계 빌드의 필요성이 사라진다. Go는 병렬 처리와 메모리 효율에서 TypeScript/JavaScript보다 유리하다.

**관점 2 — Node.js `--experimental-strip-types`:** Node.js 자체가 TypeScript를 직접 실행하는 방향이다. Node 22에서 `--experimental-strip-types` 플래그로 TS 파일을 실행할 수 있게 됐다. 타입 주석을 제거(strip)하고 JS로 실행하는 방식이라 타입 체크는 수행하지 않는다. 하지만 빌드 단계 없이 `node index.ts`로 실행할 수 있다는 것만으로 개발 경험이 달라진다.

**관점 3 — Bun의 네이티브 실행:** Bun은 처음부터 TypeScript를 직접 실행하는 런타임이다. `bun run file.ts`가 바로 된다. 타입 체크는 별도로 해야 하지만, 런타임이 TS를 1급 시민으로 취급한다는 점에서 개발 흐름이 단순해진다.

**현재 합의:** 세 방향이 동시에 진행 중이다. TS Native가 GA(General Availability)되면 `tsc`의 속도 문제는 해결된다. Node의 `strip-types`는 타입 체크를 포기하는 대신 빌드 단계를 없앤다. Bun은 개발 환경에서는 이미 충분히 쓸 만하다. 어느 방향이 주류가 될지는 각 방향이 프로덕션 안정성을 어떻게 증명하느냐에 달려 있다.

**남은 공백:** TypeScript Native가 언제 안정 버전으로 출시되는가, 기존 `tsc` 기반 설정이 자동으로 호환되는가. 이 질문에 대한 답이 나오면 생태계 전체의 빌드 설정이 크게 단순해질 것이다.

**한국 현장 시각:** 논쟁 G는 한국 개발자에게 조금 다른 무게감을 갖는다. 한국의 대형 서비스들은 빌드 시간이 개발 생산성에 미치는 영향을 이미 체감하고 있다. 토스, 카카오, 우아한형제들처럼 수백 개의 패키지로 이루어진 monorepo를 운영하는 팀에서 `tsc`의 느린 빌드는 매일 마주치는 실용적 문제다. TypeScript Native가 실제로 10배 빠르다면, 이 팀들의 CI/CD 파이프라인 시간이 크게 줄어든다. 단순한 언어 구현 이야기가 아니라, 수십 명의 개발자가 매일 기다리는 시간의 합산이다. 그래서 이 논쟁이 한국 테크 블로그에서 유독 관심을 받는다.

---

## AI 시대의 TypeScript — 사람이 서야 할 자리

Claude, GitHub Copilot, Cursor가 TypeScript 코드를 작성하는 것이 일상이 됐다. 코드 한 페이지를 1초도 안 되어 생성하고, 함수 시그니처를 보고 구현을 완성하고, 에러 메시지를 붙여넣으면 원인과 수정 방향을 설명한다. 이 사실은 두 가지 질문을 동시에 던진다.

"왜 AI는 TypeScript 코드를 비교적 잘 생성하는가?" 그리고 "AI가 잘못 가는 자리는 어디인가?"

이 절을 쓰는 이유는 단순히 "AI가 TS를 잘 짜니까 안 배워도 된다"고 결론 내리려는 게 아니다. 정반대다. AI가 TS 코드를 생성하는 방식의 구조적 이유를 이해하면, 어디에서 AI를 믿고 어디에서 검토를 강화해야 하는지가 분명해진다. TypeScript를 깊이 이해한 사람만이 AI가 생성한 TS 코드의 품질을 정확하게 판단할 수 있다. 역설적으로 AI 시대에 "언어를 제대로 아는 것"의 가치가 더 높아졌다.

---

### 왜 AI는 TypeScript를 비교적 잘 다루는가

TypeScript가 AI에게 친화적인 이유는 구조에 있다.

**첫째, 타입이 컨텍스트를 제공한다.** 함수 시그니처에 다음과 같이 써 있다면:

```typescript
async function processPayment(
  userId: UserId,
  amount: Money,
  currency: Currency,
): Promise<Result<PaymentReceipt, PaymentError>>
```

AI는 이 함수가 무엇을 받고 무엇을 돌려줘야 하는지를 타입에서 직접 읽는다. `UserId`, `Money`, `Currency`가 branded type이라면 도메인 의미론도 읽힌다. `Result<T, E>` 패턴이 있다면 성공과 실패를 명시적으로 다뤄야 한다는 것도 안다. 타입이 상세할수록 AI가 생성하는 구현의 품질이 올라간다.

Java의 타입도 비슷한 역할을 하지만, TypeScript의 구조적 타입 시스템과 유틸리티 타입은 함수 시그니처에 더 많은 정보를 담는다. discriminated union, conditional type, mapped type이 그 자체로 "어떤 형태의 데이터를 어떻게 다루는가"를 AI에게 알려주는 명세가 된다.

**둘째, 생태계 패턴이 명확하다.** zod 스키마, React 컴포넌트의 props 타입, NestJS 모듈 구조, Express 미들웨어 시그니처 — 이 패턴들이 학습 데이터에 충분하게 있어서 AI는 "여기에 뭐가 들어가야 한다"를 높은 확률로 맞춘다. 특히 TypeScript의 패턴은 자주 반복되고, 구조가 예측 가능하다. 구조적 타입 시스템의 예측 가능성이 AI의 코드 생성과 잘 맞는다.

**셋째, 컴파일러가 즉각적인 피드백을 준다.** AI가 생성한 코드가 타입 체크를 통과하지 못하면, 에러 메시지를 AI에게 다시 넣어서 수정을 요청하는 루프가 자연스럽게 돌아간다. 자기 교정 루프(self-correction loop)가 작동하기 좋은 환경이다. 타입 에러가 없는 코드를 만드는 데 AI가 꽤 효과적인 이유 중 하나다.

---

### AI가 잘못 가는 자리

그러나 AI도 틀린다. 그것도 특정 패턴으로 반복해서 틀린다. 이 패턴을 알아두면 리뷰할 때 집중해야 할 곳이 보인다.

**`any`로의 도주:** 타입 추론이 복잡해지거나, 제네릭 조합이 어려워지거나, 서드파티 라이브러리의 타입 정의가 불완전할 때, AI는 `any`를 선택하는 경향이 있다. "일단 동작하게 만드는 것"이 목표라면 `any`가 가장 쉬운 탈출구다. 그런데 이 코드가 코드베이스에 들어오면 타입 안전성의 균열이 시작된다.

AI에게 명시적으로 "any는 사용하지 말 것"을 요청하는 것도 하나의 방법이다. 또는 코드 리뷰에서 `any`의 존재를 먼저 확인하는 습관을 들이는 편이 낫다. ESLint의 `@typescript-eslint/no-explicit-any` 규칙으로 자동 검출도 가능하다.

**branded type 무시:** AI는 `UserId`와 `OrderId`가 둘 다 `string`이라면 그냥 `string`으로 통일하는 경향이 있다. 도메인 모델의 의미론적 구분을 유지하는 것은 사람의 판단이 필요한 영역이다. AI에게 "UserId는 branded type을 써줘"라고 명시하지 않으면, 구조적으로 동등한 타입을 뭉개버리는 코드를 받게 된다.

**외부 데이터 검증 누락:** API 응답을 받아서 TS 타입으로 처리하는 코드를 AI가 생성할 때, 런타임 검증 없이 `as` 단언만 붙이는 경우가 많다. boundary validation 패턴을 명시하지 않으면 AI는 실용주의적 지름길을 택한다. "API 응답은 zod로 검증한 뒤 사용할 것"을 명시하면 훨씬 나은 코드가 나온다.

**tsconfig 옵션의 가정:** AI는 종종 `strict: true`가 켜진 환경을 가정하지 않거나, 반대로 현재 프로젝트에 없는 엄격한 옵션을 가정한다. 생성된 코드가 현재 프로젝트의 tsconfig와 어긋나는 경우가 생긴다. "이 프로젝트의 tsconfig는 X를 켜고 있다"는 컨텍스트를 제공하면 정확도가 올라간다.

**에러 경로의 단순화:** AI는 성공 경로를 먼저 작성하고 에러 경로를 단순화하는 경향이 있다. Promise의 rejection이 모두 처리되는지, null/undefined 케이스가 빠짐없이 다뤄지는지를 검토해야 한다. 특히 `noUncheckedIndexedAccess: true`가 켜진 환경에서 AI가 생성한 배열 접근 코드는 `undefined` 가능성을 무시하는 경우가 많다.

---

### zod 스키마를 프롬프트의 일부로 쓰는 패턴

실무에서 AI 코드 생성의 품질을 높이는 패턴 하나를 소개하자. AI에게 코드 생성을 요청할 때, zod 스키마를 프롬프트에 포함시키면 타입의 경계를 더 명확히 이해한다.

```typescript
// 프롬프트에 이 스키마를 포함한다
const UserSchema = z.object({
  id: z.string().brand<'UserId'>(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
  profile: z.object({
    name: z.string().min(1),
    bio: z.string().nullable(),
  }),
});

type User = z.infer<typeof UserSchema>;
```

이 스키마를 컨텍스트로 제공하면, AI는 `User` 타입의 제약 조건(branded id, email 형식, 제한된 role 값, Date 타입, nullable bio)을 프롬프트에서 직접 읽는다. "User를 받아서 처리하는 서비스 메서드를 구현해줘"라는 요청에 훨씬 정확한 코드가 나온다. 스키마가 없을 때보다 `bio`의 nullable 처리, `role`에 따른 분기, `createdAt`의 날짜 포맷 처리를 더 정확하게 다룬다.

이 패턴의 확장으로, 현재 프로젝트의 타입 정의 파일을 프롬프트에 첨부하는 것도 효과적이다. AI가 "이미 있는 타입과 어떻게 통합되는가"를 이해한 채로 코드를 생성한다.

---

### AI에게 tsconfig 컨텍스트를 명시하는 휴리스틱

AI에게 코드 생성을 요청할 때 프롬프트에 다음을 포함하면 생성 코드의 품질이 올라간다.

```
이 프로젝트의 tsconfig 설정:
- strict: true (strictNullChecks, strictFunctionTypes, strictBindCallApply 포함)
- noUncheckedIndexedAccess: true (배열/객체 인덱스 접근 시 T | undefined)
- exactOptionalPropertyTypes: true (옵셔널 속성에 명시적 undefined 금지)
- noImplicitReturns: true (모든 코드 경로가 반환값을 가져야 함)

코딩 컨벤션:
- any 사용 금지
- 외부 데이터(API 응답, env, 폼)는 zod로 검증
- 내부 로직에서 타입 단언(as)은 최소화
- async 함수 호출 시 항상 await 또는 void 명시
```

이 정도의 컨텍스트를 주면, AI는 `arr[0]`의 결과가 `T | undefined`임을 인지하고, 옵셔널 속성에 `undefined`를 명시적으로 쓰지 않으며, `any` 대신 타입 가드나 조건부 타입을 선택하고, `async` 함수 호출에 `await`를 붙인다.

단, 이 컨텍스트를 매번 직접 입력하는 것은 번거롭다. Cursor의 `.cursorrules` 파일, 또는 팀의 코딩 어시스턴트 설정에 이 내용을 템플릿화해두면 자동으로 포함된다.

---

### AI 시대에 사람이 검토해야 할 자리

AI 코드 생성을 활용하는 팀에서 코드 리뷰의 성격이 바뀐다. "이 코드를 어떻게 더 낫게 쓸까"보다 "이 코드가 안전한가"를 먼저 확인하는 방향으로 무게가 이동한다. TypeScript 코드에서 AI가 생성한 부분을 리뷰할 때 집중해야 할 항목들을 정리해두자.

**타입 경계의 무결성:** 외부 입력이 들어오는 지점에 런타임 검증이 있는가. `as`로 때우고 있는가, zod 파싱이 있는가. API 엔드포인트, 환경 변수 파싱, 폼 제출 핸들러, 파일 읽기가 특히 주의 대상이다.

**`any`의 존재와 정당성:** `any`가 있다면 그것이 불가피한 위치인가, 아니면 AI가 포기해서 쓴 것인가. `any`가 있다면 왜 있는지 주석이 있는가. ESLint `@typescript-eslint/no-explicit-any`로 자동 검출한다.

**도메인 의미론의 보존:** branded type이 제거되거나 희석되지 않았는가. `UserId`와 `OrderId`가 그냥 `string`으로 통일됐는가. 도메인 언어가 타입에 그대로 반영됐는가.

**에러 경로의 완결성:** `async` 함수의 rejection이 모두 처리되는가. Promise가 `await` 없이 floating되지 않는가. try/catch에서 에러 타입이 `unknown`으로 올바르게 처리되는가.

**엣지 케이스 커버리지:** AI가 짠 코드에는 엣지 케이스 테스트가 빠지는 경향이 있다. `null`, `undefined`, 빈 배열, 음수 값, 매우 긴 문자열, 특수 문자를 포함한 테스트가 있는가.

**tsconfig 정합성:** 현재 프로젝트 tsconfig에서 에러가 나지 않는가. 특히 `noUncheckedIndexedAccess`가 켜진 환경에서 배열 접근이 올바르게 처리됐는가.

AI는 코드를 빠르게 생성하는 강력한 도구다. 하지만 도구는 사용자의 판단을 대체하지 않는다. TypeScript를 깊이 이해한 사람만이 AI가 생성한 TS 코드의 품질을 판단할 수 있다. 이 책을 읽는 이유가 여기에 있다.

Java/Kotlin 개발자에게 AI 코드 검토에서 특히 주의해야 할 패턴이 하나 더 있다. AI는 종종 Java/Spring 스타일의 코드를 TypeScript로 직역한다. 클래스 기반 설계, 서비스-리포지터리 레이어 분리, 인터페이스와 구현 클래스 분리 등이다. 이 패턴들이 TypeScript에서 반드시 나쁜 것은 아니지만, TypeScript 생태계가 더 자연스럽게 다루는 방식과 다를 수 있다. 특히 함수형 패턴과 클로저가 TypeScript에서는 클래스보다 더 간결하게 같은 역할을 하는 경우가 많다. AI가 "Java 스타일"로 TypeScript를 짜고 있다면, "이게 TypeScript다운 방식인가"를 한 번 더 물어보자.

---

## 학습 자원 지도 — 다음으로 가는 길

책을 덮은 다음, 어디로 더 깊이 들어갈 수 있는가. 신뢰할 수 있는 자원들을 정리해두자. 유행처럼 나왔다 사라지는 블로그 글이 아니라, 시간이 지나도 가치가 있는 1차 자원들이다.

---

### 한국어 자원

**velopert(김민준) — TypeScript Handbook 한국어판**

TypeScript 공식 핸드북의 한국어 번역과 함께, 개인 velog에 실무 중심의 글을 꾸준히 올린다. 입문 이후 기초를 다시 점검하기 좋다. 한국어로 TypeScript를 처음 배우는 개발자 대부분이 이 자료로 시작한다. `https://typescript-kr.github.io/`

**토스 기술블로그 — JavaScript에서 TypeScript로 바꾸기 시리즈**

토스의 실제 마이그레이션 경험을 담았다. 수만 줄의 실제 코드베이스를 어떻게 전환했는지, 어떤 판단을 했는지를 솔직하게 썼다. "이론은 알겠는데 실제로는 어떻게 하는 거지?"라는 질문에 답한다. `https://toss.tech/`

**카카오 기술블로그 — TypeScript Monorepo with pnpm**

pnpm workspace 기반 monorepo 구성의 실무 레퍼런스다. `tsconfig.references` 설정, 패키지 간 의존성 관리, IDE 성능 유지 방법이 구체적으로 나와 있다. monorepo를 도입하려는 팀이라면 반드시 읽어야 한다. `https://tech.kakao.com/`

**당근 기술블로그 — 한 모노레포에서 1000명이 일하는 법**

대규모 monorepo 운영 경험이 담겼다. 팀이 커지면서 생기는 빌드 전략, 패키지 경계 설계, IDE 성능 관리의 실제 판단들이 실용적이다.

**이펙티브 타입스크립트 (Dan Vanderkam 저, 인사이트 번역)**

"어떻게 쓰는가"보다 "왜 이렇게 작동하는가"를 설명하는 책이다. 타입 시스템의 원리, 실무에서 자주 만나는 오류의 근원, 더 나은 타입 설계를 위한 구체적 아이템들이 담겼다. 타입을 어떻게 써야 할지 막막할 때 펼치면 방향이 잡힌다. 한국어로 구할 수 있는 TypeScript 깊이 있는 책 중 현재 최선의 선택이다.

---

### 영어 자원

**Total TypeScript — Matt Pocock**

실무 중심의 TypeScript 심화 학습 플랫폼이다. tsconfig cheat sheet, 제네릭 패턴, conditional type과 infer의 실용 예제, branded type 활용, 타입 좁히기 심화가 체계적으로 정리돼 있다. 무료 콘텐츠만으로도 상당한 깊이를 커버한다. `https://www.totaltypescript.com/`

**Effective TypeScript (2nd ed., 2024) — Dan Vanderkam**

한국어판의 원본이다. 2판에서 최신 TS 기능이 대거 추가됐다. 한국어판이 1판 기준이라면 원서 2판을 함께 보는 편이 낫다. 특히 Item 38~44에서 타입 좁히기, 조건부 타입, infer를 다루는 방식이 깊다.

**Programming TypeScript — Boris Cherny**

타입 시스템을 바닥부터 쌓아 올리는 구성이다. 타입 추론의 알고리즘, 공변성과 반변성의 원리, 클래스와 타입의 관계를 이론적으로 설명한다. "왜 이 제네릭이 이렇게 작동하는가"를 이해하고 싶다면 이 책이다.

**Type-Level TypeScript**

타입 수준 프로그래밍을 다룬다. 타입 자체를 계산하는 기법 — conditional type, infer, 재귀 타입, mapped type의 고급 활용 — 을 체계적으로 배운다. TypeScript의 타입 시스템이 일종의 프로그래밍 언어라는 사실을 실감하게 된다. `https://type-level-typescript.com/`

---

### 다음 책·다음 주제

**Effective TypeScript → Type-Level TypeScript → Programming TypeScript** 순서가 실용적인 심화 경로다. 이펙티브 TS로 원리를 잡고, Type-Level TS로 타입 연산을 익히고, Programming TS로 이론적 배경을 완성하는 흐름이다.

**RxJS 깊이:** 반응형 프로그래밍 패러다임이 TypeScript와 만나는 지점이다. 이벤트 스트림, 옵저버블 패턴, 연산자 파이프라인을 타입-안전하게 다루는 방법은 별도의 학습이 필요하다. Angular를 쓰는 팀이라면 사실상 필수다.

**NestJS 깊이:** DI 원리, interceptor, guard, middleware의 동작 방식, TypeORM 또는 Prisma와의 통합, 새 데코레이터 마이그레이션 동향. NestJS를 프로덕션에서 운영한다면 공식 문서와 이슈 트래커를 직접 파야 한다. `https://docs.nestjs.com/`

**TypeScript 컴파일러 API:** TS 컴파일러를 도구로 사용하는 방법이다. codemod 작성, 커스텀 lint 규칙, 코드 생성 도구를 만들 때 필요하다. 네이버 D2의 컴파일러 API 활용 사례가 한국어 레퍼런스다. `https://d2.naver.com/`

**zod/valibot 생태계:** 런타임 검증 라이브러리가 빠르게 발전하고 있다. zod v4의 API 개선, valibot의 경량 설계, arktype의 TS 타입 통합 방식 차이를 이해하면 boundary validation 전략을 팀 맥락에 맞게 선택할 수 있다.

**Prisma와 타입-안전 ORM:** TypeORM과 달리 Prisma는 스키마에서 타입을 생성한다. 데이터베이스 스키마와 TypeScript 타입이 하나의 소스에서 나오는 방식은 Spring의 JPA와 크게 다르다. 이 차이를 이해하면 백엔드 TypeScript 개발의 타입 안전성 전략이 달라진다.

**tRPC와 타입-안전 API:** REST API를 설계할 때 백엔드가 OpenAPI 스펙을 작성하고 프론트가 그것을 기반으로 클라이언트를 생성하는 방식이 있다. tRPC는 이 워크플로를 없애고, 백엔드 라우터의 타입을 직접 프론트엔드에서 임포트해 사용한다. 서버-클라이언트 간 타입 불일치 버그가 구조적으로 불가능해진다. REST API가 필요한 환경(모바일, 외부 파트너)과 함께 사용하기 어렵다는 제약이 있지만, 웹 전용 풀스택 프로젝트에서는 생산성이 크게 오른다. Spring의 Feign Client가 API 스펙을 공유하는 방식과 철학은 비슷하지만 구현 방식은 완전히 다르다.

---

> **📖 더 깊이 가려면**
>
> 이 책에서 함정의 큰 지형을 그렸다면, 각 함정의 세부 지형은 따로 찾아볼 수 있다.
>
> **→ 부록 D에서 한국 개발자 함정 사전 12개 상세를 다룬다.** 각 함정마다 증상, 원인, 처방을 정리하고, 본문에서 더 깊이 다룬 챕터와 페이지를 안내한다.
>
> - *이펙티브 타입스크립트* Item 7(타입이 값들의 집합이라고 생각하기), Item 38(타입 좁히기), Item 45(any 사용은 최소화하기)는 이 챕터에서 다룬 함정의 이론적 배경을 제공한다.
>
> - *Total TypeScript*의 "Solving TypeScript Errors" 섹션은 실무에서 막히는 타입 에러 패턴별 해결책을 다룬다.
>
> - NestJS 새 데코레이터 마이그레이션 동향은 `https://github.com/nestjs/nest` 이슈 트래커에서 실시간으로 확인하자. 이 책 집필 이후 상황이 달라질 수 있다.

---

## 마무리 — 도구의 경계를 아는 것이 도구를 잘 쓰는 것이다

책 한 권이 끝났다. 1장에서 15장까지, TypeScript가 왜 이렇게 생겼는지를 Java/Kotlin 개발자의 시선으로 해체하고 재조립했다.

걸어온 길을 한번 돌아보자.

TypeScript의 타입은 컴파일 타임에만 존재한다. 런타임에서 타입은 사라진다. 이 사실이 이 책의 출발점이었다. Java나 Kotlin의 타입은 런타임 객체에 붙어 있다. 리플렉션으로 `getClass()`를 호출하면 타입 정보가 나온다. TypeScript는 다르다. 컴파일되면 타입 정보는 증발한다. 남는 것은 JS 값뿐이다. 이 차이를 이해하면 "타입이 있는데 왜 런타임 에러가 나는가"의 답이 보인다.

구조적 타입 시스템이 명목적 타입 시스템과 어떻게 다른지, 그 차이가 실무에서 어디서 틈새를 만드는지를 봤다. Java에서 `UserId`와 `OrderId`가 다른 클래스이기 때문에 컴파일러가 혼동을 막아주는 것이 당연하게 느껴졌다면, TypeScript에서 그 기대가 배반당하는 순간이 온다. branded type 패턴이 그 배반을 막는 방어다.

비동기의 에러가 어디로 사라지는지, `async/await`이 Java의 `CompletableFuture`와 무엇이 같고 무엇이 다른지를 살폈다. Java의 checked exception이 불편하다고 느꼈다면, TypeScript에서 `await`를 빠뜨려 에러가 공중에 뜨는 경험을 하고 나면 생각이 달라진다. 명시적 강제와 묵시적 자유 사이의 트레이드오프를 다시 생각하게 된다.

모듈 시스템의 역사적 혼란이 왜 생겼고, 2025년 현재 어느 방향으로 정착하는지를 추적했다. CommonJS와 ESM의 공존은 당분간 계속된다. 그 혼란을 피하는 가장 좋은 방법은 프로젝트 초기에 모듈 방식을 명확히 결정하고 tsconfig를 정렬하는 것이다.

데코레이터가 두 종류로 갈라진 이유와 그 갈림길이 NestJS에 어떤 긴장을 만드는지를 봤다. Spring의 `@Autowired`와 NestJS의 `@Injectable()`이 비슷해 보이지만 메커니즘이 다르다는 것, 그 메커니즘이 새 데코레이터 표준으로 이전할 때 왜 문제가 되는지를 이해했다.

React의 타입 철학이 Vue, Svelte, Solid와 어떻게 다른지, 그 차이가 컴포넌트 설계에서 어떻게 나타나는지를 비교했다. 한국 시장에서 React가 압도적이라는 현실을 인정하면서도, 다른 프레임워크를 만날 때 "이 프레임워크의 reactivity 모델은 어디가 다른가"를 볼 수 있는 눈을 만들려 했다.

풀스택의 경계가 어디까지 확장됐고, 한국 현장에서 그 경계가 어디 있는지를 짚었다. Spring + REST + React가 여전히 표준인 한국 시장에서 Next.js 풀스택이나 tRPC가 어떤 의미를 갖는지를 실용적으로 봤다.

14장에서 테스트 전략을 다뤘다. TypeScript 코드를 테스트하는 것이 Java와 어떻게 다른지, `vitest`와 `jest`의 차이, 타입 수준에서 테스트하는 `tsd`와 `expect-type`의 역할, 그리고 모킹(mocking)이 Java의 Mockito와 어떻게 닮고 어떻게 다른지를 살폈다. 특히 TypeScript에서 인터페이스가 런타임에 존재하지 않기 때문에 Mockito 스타일의 `mock(SomeInterface.class)` 패턴을 그대로 쓸 수 없다는 점, 대신 구조적 타입의 특성을 활용해 테스트용 객체를 훨씬 간단히 만들 수 있다는 점이 핵심 차이였다.

그리고 이 마지막 장에서 함정의 지형을 그리고, 논쟁의 위치를 표시하고, AI 시대의 역할을 생각했다.

---

### TypeScript를 잘 쓴다는 것이 무엇인가

책을 닫기 전에 이 질문을 한 번 더 생각해보자. "TypeScript를 잘 쓴다"는 것이 무엇을 의미하는가.

타입 에러가 하나도 없는 코드를 짜는 것인가? 아니다. `as any`를 모든 곳에 쓰면 에러가 없어지지만, 그것은 타입 체커를 속인 것이다. `strict: true` 아래에서 타입 에러 없이 코드를 짜는 것인가? 가깝지만 아직 충분하지 않다. 컴파일 타임 오류가 없어도 런타임 버그는 얼마든지 있을 수 있다.

TypeScript를 잘 쓴다는 것은 타입 시스템과 협력하는 법을 안다는 것이다. 다시 말해 두 가지를 동시에 안다는 뜻이다.

**타입 시스템이 보장해주는 것:** 컴파일 타임에 선언된 타입이 일치하는 것. 함수가 선언된 인자 타입을 받고 선언된 반환 타입을 돌려주는 것. 구조적으로 호환되지 않는 값을 넣으면 컴파일러가 잡아주는 것.

**타입 시스템이 보장해주지 않는 것:** 런타임에 외부에서 들어온 데이터가 선언된 타입과 실제로 일치하는 것. `as` 단언이 진실인 것. 모든 `async` 에러가 잡히는 것. `null` 병합 연산자 없이 객체 속성에 안전하게 접근하는 것.

이 두 가지 경계를 안다면, 타입 시스템이 보장해주는 영역에서는 컴파일러를 믿고, 보장해주지 않는 영역에서는 런타임 검증과 방어적 코딩으로 직접 채운다. 이 판단을 자연스럽게 하는 사람이 TypeScript를 잘 쓰는 사람이다.

Java/Kotlin에서 건너온 개발자에게 이 경계를 이해하는 것이 특히 중요하다. Java는 런타임에도 타입 정보가 살아 있다. 클래스 계층, 인터페이스 구현, 리플렉션이 모두 런타임에서 타입 기반으로 동작한다. TypeScript는 다르다. 컴파일 타임에 타입을 검사하고, 런타임에서는 타입이 없다. 이 차이를 몸에 새기는 것이 TypeScript를 진짜 이해하는 것이다.

흥미로운 역설이 있다. TypeScript를 잘 이해할수록 타입을 덜 쓰게 된다. 필요한 곳에만, 적절한 방식으로 타입을 쓴다. 모든 변수에 타입을 명시하는 것이 아니라, 타입 추론이 충분한 곳에서는 추론에 맡기고, 추론이 틀릴 가능성이 있는 경계에서만 명시한다. "타입을 많이 쓸수록 TypeScript를 잘 쓰는 것"이라는 오해가 있는데, 정반대다. 필요한 곳에 정확하게 쓰는 것이 잘 쓰는 것이다.

이 감각이 쌓이는 데는 시간이 필요하다. 코드를 짜고, 타입 에러를 만나고, 원인을 추적하고, 더 나은 방법을 찾는 과정이 반복되면서 쌓인다. 이 책이 그 과정을 조금 더 빠르게, 조금 덜 고통스럽게 만들었으면 하는 것이 저자의 바람이다.

---

지금 이 책을 읽고 있는 당신이 어떤 상황에 있든, 한 가지는 분명하다. TypeScript를 배우기로 결심하는 것은 기술 스택 하나를 추가하는 일이 아니다. 타입 시스템을 다르게 생각하기로 결심하는 일이다. Java/Kotlin의 명목적 타입에서 TypeScript의 구조적 타입으로 세계관을 확장하는 일이다. 컴파일 타임 안전성이 런타임까지 보장하지 않는다는 사실을 받아들이고, 그 간격을 어떻게 채울지를 설계하는 일이다.

이 전환이 처음에는 낯설다. 당연하다. 10년 넘게 Java나 Kotlin으로 사고하던 사람이 TypeScript의 구조적 타입을 처음 만나면 "이게 왜 이렇게 동작하지?"를 여러 번 되묻는다. 그 질문이 멈추는 순간이 TypeScript가 자기 것이 되는 순간이다.

그 순간이 오면, 이 책을 다시 한번 펼쳐보자. 처음 읽을 때와 다른 것이 보일 것이다.

---

AI가 코드를 써주는 시대에 역설적으로 "언어의 원리를 이해하는 것"의 가치가 올라간다. AI가 `any`를 쓴 이유를 이해하려면 `any`가 무엇인지 알아야 한다. AI가 branded type을 뭉갠 이유를 알아채려면 구조적 타입이 무엇인지 알아야 한다. AI가 생성한 `async` 함수에서 rejection이 처리됐는지 판단하려면 비동기 에러의 전파 방식을 알아야 한다.

원리를 모르면 AI가 틀렸을 때 틀린 줄 모른다. 원리를 알면 AI가 만든 코드를 더 빠르게, 더 정확하게 검토할 수 있다. AI는 생산성 도구다. 하지만 그 도구를 제대로 쓰려면 당신이 TypeScript를 제대로 알아야 한다.

---

> **저자의 마지막 한 마디**
>
> TS는 도구다. 도구의 경계를 안다는 것이 도구를 잘 쓴다는 뜻이다. 그 경계가 AI 시대에도 변하지 않는다.
>
> TypeScript의 타입은 컴파일 타임에만 있다. 런타임에서 외부에서 들어오는 데이터는 타입 시스템 밖에서 온다. 이 경계를 아는 사람이 `any`를 언제 쓰면 안 되는지 알고, 경계에서 검증해야 하는 이유를 알고, AI가 생성한 코드에서 무엇을 봐야 하는지 안다.
>
> 책을 덮고, 지금 당장 코드를 한 줄 써보자. `strict: true`를 켜고, `any`를 하나 지우고, 타입 가드를 하나 써보자. 그 한 줄이 이 책이 드리는 마지막 선물이다.


---

# 부록

TypeScript를 Java/Kotlin 관점에서 다루다 보면 "저건 나중에 찾아봐야지" 하고 지나치는 개념이 생긴다. 부록은 그 '나중'을 위한 자리다. 본문을 읽다가 막힐 때, 혹은 코드를 짜다가 뭔가 찜찜할 때 펼쳐보면 된다.

---

# 부록 A. Java/Kotlin ↔ TypeScript 용어 매핑 사전

본문을 읽다가 낯선 TypeScript 용어가 나왔을 때, 혹은 반대로 "Java에서 이 개념이 TS에서는 뭐라고 부르지?"라는 물음이 생겼을 때 펼쳐보자. 이 부록은 처음부터 끝까지 통독하는 자료가 아니다. 찜찜한 용어가 생겼을 때 빠르게 확인하는 자리다.

표는 카테고리별로 정리했다. 항목 수가 많아 보이지만 Java/Kotlin 경험이 있다면 대부분 직관적으로 매핑된다. 다만 표만 보면 놓치기 쉬운 미묘한 차이가 있는 핵심 항목 — `interface`, `data class`, `sealed class`, `Mono`/Promise, 데코레이터 기반 DI, `Result<T>` 등 — 에는 별도로 1~2단락 해설을 달았다. 표를 보고 "아, 그거구나" 하다가 해설로 넘어오면 된다.

부록 B(tsconfig 옵션 사전), 부록 C(CLI 워크쓰루), 부록 D(함정 인덱스)는 이 부록 뒤에 이어진다.

---

## 1. 언어 기본

### 표 — 언어 기본 매핑

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| `interface` (Java) | `interface` (TS) | 모양 정의는 같지만 nominal vs structural — 아래 해설 참조 |
| `class` (nominal) | `class` (structural) | TS `class`도 구조적 호환 적용 |
| `abstract class` | `abstract class` | 거의 동일. TS는 abstract method에 구현부 없어야 |
| `enum` (Java) / `enum class` (Kotlin) | `enum` 또는 union literal | TS `enum`은 런타임 객체 생성; union literal 선호 — 아래 해설 참조 |
| `sealed class` (Kotlin) | discriminated union | `kind` 필드 + 타입 좁히기 — 아래 해설 참조 |
| `data class` (Kotlin) / `record` (Java 16+) | `interface` / `type` + spread | TS에 구조적 동등성·copy() 내장 없음 — 아래 해설 참조 |
| `value class` / `inline class` (Kotlin) | branded type (관용) | 제로 비용 래퍼. TS는 언어 지원 없고 패턴으로 구현 |
| `null` (Java) | `null` / `undefined` | TS는 둘을 구분. `strictNullChecks` 켜면 명시 필요 |
| `Optional<T>` (Java) | `T \| null` / `T \| undefined` | TS는 타입 유니언으로 표현. Optional 클래스 없음 |
| `?.` (null safety, Kotlin) | `?.` (optional chaining) | 의미 동일. TS는 `??` nullish coalescing도 지원 |
| `!!` (null 단언, Kotlin) | `!` (non-null assertion) | `value!`로 null/undefined를 강제 배제. 남용 주의 |
| `var` (Kotlin 가변) / `val` (불변) | `let` (가변) / `const` (불변) | Java `var`는 타입 추론 키워드; TS `var`는 쓰지 말자 |
| `final` (Java 필드) | `readonly` (TS) | 클래스 필드, 인터페이스 프로퍼티에 `readonly` |
| `when` (Kotlin) | `switch` + type narrowing | TS `switch`는 타입 좁히기와 결합해 exhaustive check |
| `instanceof` | `instanceof` / type guard | TS는 `instanceof` 외에 사용자 정의 타입 가드도 활용 |
| `is` (Kotlin, 스마트 캐스트) | type predicate (`x is T`) | `function isFoo(x: unknown): x is Foo` 패턴 |
| 스마트 캐스트 (Kotlin) | narrowing (TS) | `if (typeof x === "string")` 이후 TS가 자동 좁히기 |
| generics `<T>` | generics `<T>` | 문법 비슷하지만 TS는 variance annotation 제한적 |
| `? extends T` (Java wildcard) | `extends` in conditional types | TS에는 use-site variance 없음; declaration-site `in`/`out` (TS 4.7+) |
| `in`/`out` variance (Kotlin) | `in`/`out` (TS 4.7+) | 선언부 variance annotation. TS 4.7부터 지원 |
| `Nothing` (Kotlin) | `never` | 도달 불가 타입. exhaustive check에 활용 |
| `Any` (Kotlin) / `Object` (Java) | `unknown` / `any` | `unknown`이 안전한 최상위 타입; `any`는 타입 검사 포기 |
| `Unit` (Kotlin) / `void` (Java) | `void` / `undefined` | 반환 없는 함수. TS `void`는 `undefined`와 미묘하게 다름 |
| `typealias` (Kotlin) | `type` alias | `type UserId = string`. TS는 structural이라 런타임 구분 없음 |
| `companion object` (Kotlin) | `static` 또는 namespace | TS `class`는 `static` 지원. namespace 패턴도 가능 |
| `object` singleton (Kotlin) | module-level const / singleton 패턴 | TS에 언어 레벨 singleton 없음 |
| extension function (Kotlin) | prototype 확장 (권장 안 함) / 모듈 함수 | TS에 확장 함수 없음; 모듈 함수로 대체 |
| `infix` fun (Kotlin) | 없음 (라이브러리 체이닝으로 대체) | — |
| destructuring (Kotlin `val (a, b) = ...`) | destructuring (`const { a, b } = ...`) | 배열·객체 모두 지원. TS는 타입 자동 추론 |
| spread `*list` (Kotlin vararg) | `...args` (rest/spread) | 함수 인자·배열·객체 spread |
| `lazy` (Kotlin) | lazy init 패턴 (getter 캐싱 등) | TS 언어 레벨 없음 |
| `@JvmField`, `@JvmStatic` | 해당 없음 | JVM interop 전용 |

---

### 해설 — interface: 모양은 같지만 철학이 다르다

Java와 TypeScript 모두 `interface` 키워드를 쓴다. 하지만 의미가 제법 다르다. Java `interface`는 **명목 타입(nominal type)** 시스템 위에 있다. `class Dog implements Animal`이라고 명시해야만 `Dog`가 `Animal`로 취급된다. 선언이 없으면 모양이 똑같아도 호환되지 않는다.

TypeScript `interface`는 **구조적 타입(structural type)** 위에 있다. `Animal`이 `name: string`을 요구한다면, `name: string`이 있는 객체는 `implements Animal`을 쓰지 않아도 `Animal`로 통한다. Java 출신에게 이건 처음엔 신선하고, 나중엔 찜찜하다. `type UserId = string`을 만들어도 그냥 `string`과 구분이 되지 않는 것처럼, 모양이 같으면 같은 타입으로 취급된다는 뜻이기 때문이다. 도메인 안전성이 필요하면 **branded type** 패턴(`string & { readonly _brand: unique symbol }`)을 써야 한다.

TypeScript `interface`에는 Java에 없는 특징이 하나 더 있다. **선언 병합(declaration merging)**이다. 같은 이름의 `interface`를 두 번 선언하면 자동으로 합쳐진다. 서드파티 라이브러리의 `interface`에 필드를 추가할 때 유용하지만, 의도치 않게 합쳐지면 난감한 상황이 생길 수 있으니 주의해두자.

```typescript
// 선언 병합 예시
interface Window {
  myCustomProp: string;
}
// 이제 Window에는 myCustomProp이 있다 (전역 확장 패턴)
```

`interface`와 `type` alias는 많은 경우 교환 가능하지만, 선언 병합이 필요하거나 클래스가 `implements`할 때는 `interface`가 낫고, 유니언·튜플·조건부 타입을 표현할 때는 `type`이 필요하다.

---

### 해설 — enum: TS enum보다 union literal을 쓰는 편이 낫다

Kotlin `enum class`는 풍부하다. 각 상수에 프로퍼티를 붙이고, 메서드도 정의할 수 있다. Java `enum`도 마찬가지다. TypeScript `enum`은 언뜻 비슷해 보이지만 런타임에 실제 객체를 만들어낸다. 이게 번거로운 이유가 있다.

```typescript
enum Direction { Up, Down, Left, Right }
// 컴파일 후 런타임에 {0: 'Up', Up: 0, ...} 객체가 생성된다
```

tree-shaking이 잘 안 되고, const enum은 또 다른 복잡성을 낳는다. 그래서 TS 커뮤니티에서는 **union literal**을 선호한다.

```typescript
type Direction = "Up" | "Down" | "Left" | "Right";
```

가볍고 tree-shaking 친화적이며, 타입 좁히기도 자연스럽다. 다만 Kotlin `enum class`처럼 각 항목에 메서드를 붙이거나 반복(iteration)이 필요하다면 `const` 배열과 `typeof`를 조합하거나, 별도 맵 구조를 쓰는 편이 낫다. enum과 union literal의 선택은 팀 컨벤션 문제이기도 하니, 처음 시작할 때 합의해두자.

---

### 해설 — data class / record: copy()는 직접 써야 한다

Kotlin `data class`는 편리하다. `equals()`, `hashCode()`, `toString()`, `copy()`가 자동으로 생성된다. Java 16+의 `record`도 비슷하다. TypeScript에는 이에 대응하는 언어 내장 기능이 없다.

불변 값 객체는 보통 `interface` 또는 `type`으로 모양을 정의하고, 복사할 때는 spread 연산자를 쓴다.

```typescript
interface Point { readonly x: number; readonly y: number; }

const p1: Point = { x: 1, y: 2 };
const p2: Point = { ...p1, y: 10 };  // Kotlin의 p1.copy(y = 10)에 해당
```

`equals()`에 해당하는 깊은 동등성 비교는 기본 제공이 없다. `JSON.stringify` 비교, lodash `isEqual`, 또는 직접 구현이 필요하다. `Object.freeze()`로 얕은 불변성을 강제할 수 있지만, 중첩 객체는 별도 처리가 필요하다. `Readonly<T>` 유틸리티 타입은 컴파일 타임 불변성을 타입 레벨에서만 보장한다. 런타임에 실제 변경을 막으려면 `Object.freeze()`를 써야 한다.

---

### 해설 — sealed class / discriminated union: `never`로 완전성을 검증하자

Kotlin `sealed class`는 컴파일러가 하위 클래스를 모두 알기 때문에 `when`에서 exhaustive check를 강제한다. 빠진 케이스가 있으면 컴파일 에러다.

TypeScript의 대응은 **discriminated union**이다. 공통 `kind` 필드(또는 `type`, `tag` 등 이름은 자유)로 각 케이스를 구별한다.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle": return Math.PI * s.radius ** 2;
    case "rect":   return s.width * s.height;
    default:
      const _exhaustive: never = s;  // 새 케이스가 생기면 여기서 컴파일 에러
      return _exhaustive;
  }
}
```

`never` 트릭을 빠뜨리면 새로운 variant를 추가했을 때 컴파일러가 놓친다. 기억해두자 — discriminated union을 쓸 때는 `default: never` 패턴을 습관으로 만드는 편이 낫다.

Kotlin `when`처럼 TS `switch`도 타입 좁히기가 일어난다. `case "circle"` 분기 안에서 `s`는 자동으로 `{ kind: "circle"; radius: number }` 타입이 된다. 스마트 캐스트와 같은 역할이다.

---

## 2. 빌드 / 패키징

| Java / Kotlin / JVM | TypeScript / Node | 비고 |
|---|---|---|
| JVM | Node.js / Bun / Deno (런타임) | 단일 표준 JVM과 달리 런타임이 여럿 |
| Maven / Gradle | npm / pnpm / yarn | 빌드 책임이 여러 도구로 분산 |
| `pom.xml` / `build.gradle` | `package.json` | 의존성·스크립트·메타정보 |
| Maven Central / JCenter | npmjs.com (npm registry) | 의존성 trust boundary가 JVM 대비 매우 느슨 |
| JAR / WAR / EAR | npm 패키지 (`node_modules`) | 바이너리 배포 아닌 소스 배포가 기본 |
| `groupId:artifactId:version` (GAV) | `패키지명@버전` | `lodash@4.17.21` 형식 |
| `compile` scope | `dependencies` | 런타임 필요 의존성 |
| `test` scope | `devDependencies` | 빌드·테스트 전용 의존성 |
| `provided` scope | `peerDependencies` | 호스트 환경이 제공하는 의존성 (플러그인 등) |
| `optional` dependency | `optionalDependencies` | 설치 실패해도 무방 |
| `mvn install` / `gradle build` | `npm install` / `pnpm install` | 로컬 의존성 설치 |
| `mvn clean package` | `npm run build` | 빌드 스크립트 실행 |
| `mvnw` / `gradlew` (wrapper) | `npx` | 버전 고정 실행기. `npx tsc` 등 |
| `settings.gradle` (멀티 프로젝트) | `pnpm workspaces` / `npm workspaces` | 모노레포 루트 설정 |
| Turborepo / Nx (TS 생태계) | Turborepo / Nx | 모노레포 빌드 캐싱·태스크 오케스트레이션 |
| `javac` | `tsc` (TypeScript compiler) | 타입 체크 + 트랜스파일. 느림 |
| — | `esbuild` / `swc` | 트랜스파일 전용. 10~100배 빠름. 타입 체크 안 함 |
| — | `vite` | 프론트엔드 dev server + 번들러. esbuild 기반 |
| `.gitignore` | `.gitignore` + `.npmignore` | npm publish 시 배포 제외 목록 |
| `MANIFEST.MF` | `package.json` `"main"` / `"exports"` | 패키지 진입점 정의 |
| JPMS (`module-info.java`) | `"exports"` in `package.json` | 공개 API 제한. ESM 환경에서 |
| OSGi bundle | ESM + `package.json exports` | JS는 모듈 표준 정착이 늦었음 |
| `lock file` (없음) | `package-lock.json` / `pnpm-lock.yaml` | 재현 가능 빌드를 위한 잠금 파일 |
| GraalVM native-image | `bun build --compile` / `deno compile` | 단일 실행 파일 생성 |

---

## 3. 런타임 / 도구

| Java / JVM | TypeScript / Node 생태계 | 비고 |
|---|---|---|
| JVM (HotSpot) | Node.js (V8 + libuv) | V8은 JIT 포함. libuv가 이벤트 루프 |
| JIT 컴파일 | V8 JIT (Turbofan/Maglev) | 런타임 최적화 |
| GC (G1, ZGC, Shenandoah) | V8 GC (Orinoco) | TS/JS 개발자가 GC를 직접 튜닝하는 일은 드물다 |
| 스레드 (`Thread`, `ExecutorService`) | Worker Threads (Node) / 이벤트 루프 | JS는 기본 단일 스레드. 병렬은 Worker로 |
| 스레드풀 (`ForkJoinPool`) | `worker_threads` 모듈 | CPU 집약 작업 시 |
| `System.out.println` | `console.log` | — |
| `System.err.println` | `console.error` | stderr로 출력 |
| JVM 옵션 (`-Xmx`, `-Xms`) | `NODE_OPTIONS=--max-old-space-size=...` | 힙 크기 조정 |
| `java -jar app.jar` | `node dist/app.js` | 실행 |
| JVM 시작 시간 (~수백 ms~수 초) | Node 시작 시간 (~수십 ms) | Bun은 더 빠름 |
| Java 에이전트 (`javaagent`) | Node `--require` / `--import` | 부트스트랩 훅 |
| JMX / Micrometer | OpenTelemetry (SDK), `prom-client` | 관측 가능성 |
| HotSpot / GraalVM | Node.js / Bun / Deno | 실행 엔진 선택지 |
| **Bun** | — | Zig 작성. TypeScript 직접 실행, 빠른 install, 내장 테스트러너 |
| **Deno** | — | TypeScript 일급, 보안 기본(권한 명시), 표준 라이브러리 내장 |
| `jshell` (REPL) | `node` REPL / `bun` REPL | 대화형 실행 |
| Kotlin scripting (`.kts`) | `ts-node` / `bun run file.ts` | TypeScript 파일 직접 실행 |

---

## 4. 비동기

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| `Future<T>` | `Promise<T>` | 단일 비동기 값. JS 표준 |
| `CompletableFuture<T>` | `Promise<T>` + `.then()` / `async/await` | `thenCompose` → `then`, `thenApply` → `then` |
| `Mono<T>` (Reactor) | `Promise<T>` | 단일 값 비동기 스트림 |
| `Flux<T>` (Reactor) | `Observable<T>` (RxJS) | 여러 값 스트림. 아래 해설 참조 |
| `suspend` fun (Kotlin coroutine) | `async` / `await` | 표면 문법 유사. 내부 동작은 다름 |
| Kotlin `Flow` | `AsyncIterator` / `ReadableStream` / Observable | 지연 스트림. 선택지가 여럿 |
| `CoroutineScope` / `CoroutineContext` | — (언어 레벨 없음) | JS는 이벤트 루프가 암묵적 컨텍스트 |
| `Dispatchers.IO` / `Dispatchers.Default` | libuv I/O (암묵적) / Worker Threads | I/O는 이벤트 루프, CPU는 Worker |
| `async { }` block (Kotlin) | `async function` | 비동기 함수 정의 |
| `await` (Kotlin) | `await` | 값 꺼내기 |
| `runBlocking` (Kotlin) | `await Promise` at top level (ESM), `bun run` | 동기 컨텍스트에서 비동기 실행 |
| `try/catch` for exception | `try/catch` | `async/await`에서 예외 잡기 |
| `onErrorResume`, `onErrorReturn` | `.catch()` | Promise 에러 복구 |
| `timeout` operator (Reactor) | `AbortController` + `AbortSignal` | fetch 등 취소 패턴 |
| `zip`, `flatMap` (Reactor) | `Promise.all`, `Promise.allSettled` | 병렬 실행 |
| checked exception | — (JS에 없음) | 아래 해설 참조 |

---

### 해설 — Mono/Flux vs Promise/Observable: 즉시 실행 vs 지연 실행

Java Reactor의 `Mono`/`Flux`와 TypeScript의 `Promise`/`Observable`(RxJS)은 겉으로 비슷해 보이지만 중요한 차이가 있다.

**Promise는 만드는 순간 실행이 시작된다.** `new Promise((resolve) => { /* 이미 실행 중 */ })`. 구독자가 없어도 돈다. 이건 Java의 `CompletableFuture`와 같은 동작이다. 반면 Reactor `Mono`는 구독하기 전까지 아무것도 하지 않는다 — cold publisher다.

RxJS `Observable`도 cold다. `subscribe()`를 호출해야 실행이 시작된다. 이 차이를 모르고 `Observable`을 `Promise`처럼 쓰면 난감한 상황이 생긴다. 함수를 정의만 해두고 실행은 되지 않는다.

```typescript
// Promise: 선언 즉시 fetch 실행
const p = fetch("https://api.example.com/data");

// Observable: subscribe() 전까지 실행 없음
const obs = new Observable((subscriber) => {
  fetch("https://api.example.com/data").then(r => subscriber.next(r));
});
// obs를 아무도 구독하지 않으면 fetch는 일어나지 않는다
```

현실 TS 코드에서 RxJS는 Angular 프로젝트 외에는 점차 드물어졌다. `async/await` + `AbortController`로 대부분의 시나리오를 커버하고, 복잡한 스트림 조합은 React Query나 SWR 같은 라이브러리가 흡수했다. Reactor 숙련자라면 RxJS가 편할 수 있지만, 팀 전체가 배워야 한다면 `async/await`을 먼저 익히는 편이 낫다.

---

## 5. DI / 프레임워크

| Java / Kotlin (Spring) | TypeScript (NestJS / 기타) | 비고 |
|---|---|---|
| `@Component` | `@Injectable()` (NestJS) | 의존성 주입 대상 등록 |
| `@Service` | `@Injectable()` | NestJS는 역할별 데코레이터 구분 없음 |
| `@Repository` | `@Injectable()` + TypeORM Repository | ORM 레이어는 별도 |
| `@Controller` (MVC) | `@Controller()` (NestJS) | HTTP 요청 처리 |
| `@RestController` | `@Controller()` + `@Get()`/`@Post()` 등 | 아래 해설 참조 |
| `@Configuration` | `@Module()` (NestJS) | 모듈 구성 선언 |
| `@Bean` | `@Module({ providers: [...] })` | Provider 등록 |
| `@Autowired` | 생성자 주입 (NestJS 권장) | NestJS는 생성자 주입 자동 처리 |
| component scan (Spring) | `@Module({ imports: [...] })` 명시 등록 | NestJS는 자동 스캔 없음 — 아래 해설 참조 |
| `ApplicationContext` | NestJS `ModuleRef` | 런타임 컨테이너 접근 |
| `@Scope(prototype)` | `{ scope: Scope.REQUEST }` | 요청별 인스턴스 |
| `@Value("${...}")` | `@Inject(CONFIG)` + ConfigModule | 환경변수 주입 |
| `@Profile` | — (조건부 모듈 구성) | 환경별 모듈 분기 |
| `@ExceptionHandler` | `@Catch()` + ExceptionFilter (NestJS) | 전역 예외 처리 |
| `@ControllerAdvice` | APP_FILTER (전역 ExceptionFilter) | 전역 예외 핸들러 |
| `@Aspect` (AOP) | Interceptor (NestJS) | 횡단 관심사 |
| `@Transactional` | TypeORM DataSource.transaction() | 선언적 트랜잭션 없음 (라이브러리 의존) |
| `HandlerInterceptor` | NestJS `Interceptor` | 요청/응답 전후 처리 |
| `Filter` (Servlet) | NestJS `Guard` / `Middleware` | 인증·인가 |
| Guice / Dagger | tsyringe / InversifyJS | 더 가벼운 DI 컨테이너. Spring보다 Guice에 가까움 |
| legacy `experimentalDecorators` | legacy decorator mode (NestJS 현재) | TS 5.0+ 신규 표준 데코레이터와 다름 |
| TC39 표준 데코레이터 (TS 5.0+) | 신규 decorator proposal | NestJS는 당분간 legacy 유지 |

---

### 해설 — @RestController vs @Controller: Spring의 통합을 NestJS는 나눈다

Spring `@RestController`는 `@Controller + @ResponseBody`의 합성이다. JSON 응답이 기본이다. NestJS `@Controller()`는 라우트 prefix를 지정하고, 메서드별로 `@Get()`, `@Post()` 등을 붙인다. JSON 직렬화는 기본이다.

```typescript
// NestJS
@Controller('users')
export class UsersController {
  @Get(':id')
  findOne(@Param('id') id: string): UserDto {
    return this.usersService.findOne(+id);
  }
}
```

Spring `@RequestMapping`은 NestJS에서 `@Controller('prefix')` + 메서드 데코레이터(`@Get()`, `@Post()`)로 나뉜다. Spring `@PathVariable`은 `@Param()`, `@RequestBody`는 `@Body()`, `@RequestParam`은 `@Query()`로 대응한다.

---

### 해설 — component scan vs Module 명시 등록: NestJS는 자동 스캔을 하지 않는다

Spring의 component scan은 패키지를 뒤져 `@Component` 계열 클래스를 자동으로 빈 컨테이너에 등록한다. 편리하지만 규모가 커지면 "이 빈이 어디서 왔나"가 불투명해질 수 있다.

NestJS는 다르다. 모든 provider는 `@Module({ providers: [UserService, AuthService] })`처럼 **명시적으로 등록**해야 한다. 다른 모듈에서 쓰려면 `exports`에도 적어야 한다. 처음엔 번거롭다. 하지만 의존 관계가 명확해지고, 어디서 무엇이 주입되는지 추적하기 쉬워진다. Spring DI에 익숙한 사람이 NestJS 코드를 처음 봤을 때 "왜 이렇게 verbose한가" 싶은 부분이 바로 이 지점이다. 의도적인 선택이라고 이해해두자.

---

## 6. 검증 (Validation)

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| Bean Validation (`javax.validation` / `jakarta.validation`) | zod / valibot / ArkType | 스키마 우선 설계 |
| `@Valid` | `z.parse()` / `schema.parse()` | 요청 유효성 검증 |
| `@NotNull` | `z.string()` (nullable 제외) | null 불허 |
| `@NotBlank` | `z.string().min(1)` | 빈 문자열 불허 |
| `@Size(min=, max=)` | `z.string().min().max()` | 길이 범위 |
| `@Email` | `z.string().email()` | 이메일 형식 |
| `@Pattern(regexp=)` | `z.string().regex()` | 정규식 |
| `@Min` / `@Max` | `z.number().min().max()` | 숫자 범위 |
| `@Positive` | `z.number().positive()` | 양수 |
| `@Future` / `@Past` | 커스텀 refine | zod `.refine()` 활용 |
| `ConstraintValidator` (커스텀) | `.refine()` / `.transform()` | 복잡한 검증 로직 |
| `@Valid` on nested | `z.object({ nested: z.object({...}) })` | 중첩 검증 |
| Hibernate Validator | zod (가장 광범위) | 커뮤니티 사실상 표준 |
| class-validator (NestJS용) | zod / valibot | NestJS는 class-validator 전통적 선택 |
| `@Validated` groups | `z.discriminatedUnion` / 분기 스키마 | 그룹 검증은 zod에 직접 해당 없음 |

---

## 7. 테스트

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| JUnit 5 | Vitest / Jest | Vitest가 신규 프로젝트 권장. Jest는 기존 표준 |
| `@Test` | `test()` / `it()` | 테스트 함수 |
| `@BeforeEach` / `@AfterEach` | `beforeEach()` / `afterEach()` | 훅 |
| `@BeforeAll` / `@AfterAll` | `beforeAll()` / `afterAll()` | 전체 훅 |
| `@Nested` | `describe()` 중첩 | 테스트 그룹화 |
| `@Disabled` | `test.skip()` | 테스트 비활성화 |
| `@ParameterizedTest` | `test.each()` | 파라미터 테스트 |
| `Assertions.assertEquals` | `expect(a).toBe(b)` | 동등성 검증 |
| `assertThrows` | `expect(() => fn()).toThrow()` | 예외 검증 |
| `assertDoesNotThrow` | `expect(() => fn()).not.toThrow()` | — |
| Mockito | `vi.mock()` (Vitest) / `jest.mock()` | 모킹 |
| `@Mock` / `@InjectMocks` | `vi.fn()` / 수동 주입 | Vitest에 자동 어노테이션 없음 |
| `when().thenReturn()` | `vi.fn().mockReturnValue()` | 목 반환값 설정 |
| `verify()` | `expect(fn).toHaveBeenCalled()` | 호출 검증 |
| MockK (Kotlin) | `vi.mock()` | Kotlin 스타일 목 |
| jqwik (property-based) | fast-check | 속성 기반 테스트. 아래 해설 참조 |
| AssertJ | 없음 (Vitest expect 체이닝) | fluent assertion |
| `@SpringBootTest` | Vitest + supertest | 통합 테스트 |
| RestAssured | supertest / `fetch` + Vitest | HTTP 통합 테스트 |
| WireMock / MockServer | `msw` (Mock Service Worker) | API 목 서버 |
| Selenium / Playwright (Java) | Playwright (TS) | E2E 테스트. TS Playwright가 더 자연스러움 |
| Testcontainers (Java) | Testcontainers (Node) | 실제 DB·서비스 컨테이너 |
| `expect-type` | `expectTypeOf()` (Vitest) | 타입 수준 테스트 — 타입이 맞는지 확인 |

---

## 8. 에러 처리

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| checked exception | 없음 | TS에 checked exception 없음 — 아래 해설 참조 |
| unchecked exception (RuntimeException) | `throw new Error(...)` | JS/TS의 모든 throw는 unchecked |
| `try / catch / finally` | `try / catch / finally` | 동일 |
| `Exception` 계층 | `Error` 계층 (`TypeError`, `RangeError` 등) | 내장 Error 서브클래스 |
| `throws` 선언 | 없음 | 함수 시그니처에 throw 명시 불가 |
| `Throwable` | `unknown` (catch 변수 타입) | TS 4.0+ catch `e`는 `unknown` — `e as Error` 필요 |
| `Result<T>` (Kotlin) | `neverthrow` / `fp-ts` / `Effect-ts` | 아래 해설 참조 |
| `Either<E, A>` (Arrow/Vavr) | `Result<T, E>` (neverthrow) | 실패를 타입으로 표현 |
| `try { } catch (e: SpecificException)` | `catch (e) { if (e instanceof SpecificError) }` | TS catch는 타입 명시 불가 |
| `@ExceptionHandler` (Spring) | NestJS ExceptionFilter | 전역 예외 처리 |
| `ResponseStatusException` | `HttpException` (NestJS) | HTTP 에러 응답 |

---

### 해설 — checked exception vs throw: TS에는 컴파일러 강제가 없다

Java의 checked exception은 사랑받지 못하지만, 적어도 함수가 어떤 예외를 던질 수 있는지 **컴파일러가 강제로 알린다**. TypeScript에는 이 기능이 없다. 모든 throw는 unchecked이며, 함수 시그니처에 "이 함수는 DatabaseError를 던질 수 있다"고 표현하는 방법이 없다.

그래서 많은 팀이 **Result 패턴**을 채택한다. 예외를 던지는 대신 성공/실패를 타입으로 표현하는 것이다.

```typescript
// neverthrow 라이브러리 예시
import { ok, err, Result } from "neverthrow";

function divide(a: number, b: number): Result<number, "division-by-zero"> {
  if (b === 0) return err("division-by-zero");
  return ok(a / b);
}

const result = divide(10, 0);
if (result.isOk()) {
  console.log(result.value);
} else {
  console.log("실패:", result.error);
}
```

`neverthrow`, `fp-ts`, `Effect-ts` 등이 이 패턴을 라이브러리로 제공한다. `Effect-ts`는 함수형 프로그래밍 전반을 제공하며 Kotlin Arrow와 유사한 위치다. 팀에 따라 호불호가 갈린다 — "너무 복잡하다"는 팀과 "이게 맞다"는 팀으로. 처음엔 `neverthrow` 정도가 진입 장벽이 낮은 편이다.

외부 I/O 경계(DB 호출, HTTP 요청, 파일 읽기)에서는 `try/catch`를 쓰고, 내부 도메인 로직에서는 Result 패턴을 쓰는 절충도 자주 쓰인다.

---

## 9. 타입 시스템 심화

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| 제네릭 `<T>` | 제네릭 `<T>` | 문법 유사 |
| 상한 경계 `<T extends Foo>` | `<T extends Foo>` | 동일 |
| 하한 경계 `<T super Foo>` | 없음 (conditional type으로 우회) | TS에 직접 대응 없음 |
| wildcard `<?>` | `unknown` / `any` | TS에 use-site wildcard 없음 |
| 공변 `out T` (Kotlin) | `out T` (declaration-site, TS 4.7+) | 읽기 전용 위치 |
| 반변 `in T` (Kotlin) | `in T` (declaration-site, TS 4.7+) | 쓰기 전용 위치 |
| reified generics (Kotlin inline) | 없음 | TS generics는 런타임 소거 |
| `Class<T>` | 없음 (structural이라 불필요한 경우 많음) | 런타임 타입 토큰 |
| `instanceof` 타입 체크 | `instanceof` / type predicate / `typeof` | |
| sealed 계층 + when | discriminated union + switch/narrowing | |
| `Nothing` | `never` | 하위 타입. exhaustive check |
| `Any?` / `Object` | `unknown` | 모든 타입의 상위. 사용 전 narrowing 필요 |
| conditional type | `T extends U ? X : Y` | Java에 없음. TS 고유 강점 |
| mapped type | `{ [K in keyof T]: ... }` | Java에 없음. 타입을 변환 |
| template literal type | `` `prefix_${T}` `` | Java에 없음. 문자열 타입 조합 |
| `infer` | `infer R` in conditional types | 타입에서 타입을 추출 |
| `typeof` (Java reflection) | `typeof value` / `ReturnType<typeof fn>` | 값에서 타입 추출 |
| `keyof T` | `keyof T` | 객체 키의 유니언 타입 |
| `Partial<T>` | `Partial<T>` | 모든 필드 optional |
| `Required<T>` | `Required<T>` | 모든 필드 required |
| `Readonly<T>` | `Readonly<T>` | 모든 필드 readonly |
| `Record<K, V>` | `Record<K, V>` | 키–값 맵 타입 |
| `Pick<T, K>` | `Pick<T, K>` | 일부 필드만 선택 |
| `Omit<T, K>` | `Omit<T, K>` | 일부 필드 제외 |
| `ReturnType<F>` | `ReturnType<typeof fn>` | 함수 반환 타입 추출 |
| `Parameters<F>` | `Parameters<typeof fn>` | 함수 인자 타입 추출 |
| `Awaited<T>` | `Awaited<T>` | Promise의 resolved 타입 추출 |

---

## 10. 모듈 시스템

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| `import com.example.Foo` | `import { Foo } from "./foo"` | 경로 기반 (상대·절대) |
| `package` 선언 | 없음 | TS는 파일 자체가 모듈 |
| `public` / `private` (클래스) | `export` / 미export | 파일 레벨 export 제어 |
| JPMS `exports` | `package.json "exports"` | 패키지 공개 API |
| CJS (`require()`) | CommonJS (Node 기본 레거시) | `"type": "commonjs"` or `.cjs` |
| ESM (`import`) | ESM (`"type": "module"`) | 현재 표준. 혼용 시 주의 |
| `import static` | `import { fn }` (named import) | — |
| wildcard `import *` | `import * as ns from "..."` | namespace import |
| default `import` | `import Foo from "..."` | default export |
| 순환 의존성 금지 | 순환 import 가능하지만 권장 안 함 | 런타임 undefined 가능성 |
| `package-info.java` | `index.ts` (barrel export) | 모듈 진입점 관용 |
| `tsconfig.paths` | `tsconfig "paths"` | 경로 alias (`@/` 등) |
| `tsconfig.references` | `tsconfig.references` | 모노레포 프로젝트 참조 (IDE 성능) |

---

## 마무리

이 사전은 살아있는 문서다. TypeScript 생태계는 빠르게 움직이기 때문에, 특히 런타임 선택(Node/Bun/Deno)과 데코레이터 표준화 부분은 1~2년 사이에도 바뀔 수 있다. 표의 "비고" 란에 "당분간"이나 "현재 기준"이라고 적힌 항목들은 그 변화가 빠른 영역이다.

본문에서 개념을 따라가다 이 부록으로 돌아올 때마다, "아, Java에서는 이걸 이렇게 불렀지"라는 연결고리가 생겼으면 좋겠다. 낯선 용어가 익숙한 이름을 달고 있을 때, 전환의 속도는 훨씬 빨라진다.

다음으로는 **부록 B — tsconfig 옵션 사전**이 이어진다. `strict`가 사실 하나의 옵션이 아니라 여러 옵션의 묶음이라는 것, `moduleResolution`이 왜 이렇게 많은 값을 가지는지, 현실적인 tsconfig 템플릿 다섯 가지가 거기서 기다리고 있다.


---

# 부록 B. tsconfig 옵션 사전

`tsconfig.json`을 처음 펼쳤을 때의 당혹감을 기억하는가. 옵션이 수십 개, 어떤 블로그 포스트는 `strict: true` 하나만 켜라 하고, 어떤 스택 오버플로 답변은 열 개 넘게 붙여넣으라 한다. 각 옵션이 무슨 뜻인지는 공식 문서에 있지만, *왜 이런 옵션이 존재하는지*, *내 프로젝트에서는 언제 켜야 하는지*는 문서가 잘 말해주지 않는다.

이 부록은 그 빈틈을 채우려는 자리다. 카탈로그가 아니라 *판단 근거*를 제공한다. 8장에서 카테고리만 훑고 넘어간 옵션들을 여기서 본격적으로 풀어보자.

## 왜 옵션이 100개 넘는가

TypeScript가 처음 공개된 건 2012년이다. 당시 목표는 하나였다. "JavaScript에 타입을 얹자." 그런데 JS가 돌아가는 환경이 하나가 아니었다. 브라우저마다 지원하는 ES 버전이 달랐고, Node.js는 따로 진화하고 있었다. CommonJS가 먼저였고 ESM 표준은 2015년에야 들어왔다. 이후 모노레포가 유행하고, React의 JSX가 등장하고, 번들러마다 모듈 해석 방식이 달랐다. 데코레이터 제안은 TC39에서 몇 년간 표류하다 결국 Stage 3을 통과했는데, 그 사이에 NestJS가 구버전 데코레이터를 기반으로 생태계를 쌓았다.

새 환경이 생길 때마다 TypeScript 팀은 옵션을 추가했다. 기존 옵션을 삭제하면 이미 옵션을 쓰고 있는 프로젝트가 깨진다. 그래서 옵션은 계속 쌓였다. 2025년 기준 `compilerOptions`에 들어올 수 있는 옵션은 100개가 넘는다. 레거시 옵션도 일부 남아 있다.

이 부록은 실무에서 자주 마주치는 옵션에 집중한다. 특정 프레임워크나 환경에서만 쓰이는 엣지 케이스 옵션은 짧게 다루거나 넘어간다. 레거시로 분류된 옵션은 "쓰지 말자"는 한 마디로 처리한다.

## 이 부록을 쓰는 법

세 가지 방식으로 활용할 수 있다.

**프로젝트 시작 시:** 맨 마지막 절의 템플릿 5개부터 보자. 내 상황과 가장 가까운 템플릿을 가져다 쓰고, 이 부록으로 돌아와 "왜 이 옵션인가"를 확인한다.

**에러가 났을 때:** 처음 보는 에러 메시지에 옵션 이름이 포함돼 있다면, 해당 카테고리 절로 바로 가서 찾아보자.

**리뷰 할 때:** 동료의 PR에서 `tsconfig.json`이 바뀌었다면, 바뀐 옵션이 어느 카테고리인지, 그 팀이 왜 켰는지 추측해볼 수 있다.

---

## 2.1 strict 계열 — 가장 중요한 옵션 묶음

TypeScript를 쓰는 이유가 타입 안전성이라면, strict 계열 옵션은 그 약속을 실현하는 핵심이다. 이 옵션들 없이는 TypeScript가 "타입이 있는 JavaScript"가 아니라 "빨간 줄이 별로 없는 JavaScript"에 머문다.

### 왜 이렇게 세분화됐는가

`strict: true` 하나면 될 것을 왜 개별 옵션으로 나눴을까? 역사적 이유가 있다. 기존 JavaScript 프로젝트를 TypeScript로 점진적으로 전환할 때, 처음부터 모든 strict 옵션을 켜면 수천 개의 오류가 터진다. 그래서 팀이 하나씩 순서대로 켤 수 있도록 세분화됐다. "오늘은 `noImplicitAny`만 켜고, 다음 스프린트에 `strictNullChecks`를 켜자"는 식으로.

신규 프로젝트에서는 처음부터 `strict: true`를 켜는 편이 낫다. 전환 중인 기존 프로젝트에서는 개별 옵션을 하나씩 켜며 오류를 처리하는 단계적 접근이 현실적이다.

| 옵션 | 기본값 | `strict`에 포함 | 의미 | 언제 켜는가 |
|------|--------|-----------------|------|-------------|
| `strict` | `false` | — | 아래 strict 계열 옵션 전체를 켠다 | 신규 프로젝트에서 항상 |
| `noImplicitAny` | `false` | ✓ | 타입 추론이 불가능한 경우 `any`로 암묵적 처리 대신 오류를 낸다 | `strict`로 켜지지만, 전환 중 프로젝트에서 먼저 켤 후보 1순위 |
| `strictNullChecks` | `false` | ✓ | `null`과 `undefined`를 모든 타입의 부분집합이 아니라 별도 타입으로 취급한다 | 항상. 이걸 안 켜면 null 참조 오류를 런타임에 만난다 |
| `strictFunctionTypes` | `false` | ✓ | 함수 타입의 매개변수를 반변성(contravariance)으로 검사한다 | `strict`로 자동 적용 |
| `strictBindCallApply` | `false` | ✓ | `bind`, `call`, `apply` 호출 시 인자 타입을 검사한다 | `strict`로 자동 적용 |
| `strictPropertyInitialization` | `false` | ✓ | 클래스 생성자에서 초기화하지 않은 프로퍼티를 오류로 잡는다 | `strict`로 자동 적용. DI 프레임워크(NestJS)에서 주입받는 필드에 `!` 단언이 필요해진다 |
| `noImplicitThis` | `false` | ✓ | `this`의 타입이 `any`로 추론되는 경우 오류를 낸다 | `strict`로 자동 적용 |
| `useUnknownInCatchVariables` | `false` | ✓ | catch 블록의 에러 변수 타입을 `any` 대신 `unknown`으로 설정한다 | `strict`로 자동 적용. 6장 에러 처리 패턴과 연계된다 |
| `alwaysStrict` | `false` | ✓ | 모든 소스 파일에 `"use strict"`를 삽입하고 strict 모드로 파싱한다 | `strict`로 자동 적용 |

`strictFunctionTypes`의 반변성 이야기를 잠깐 해보자. 아래 코드를 보면 직관적으로 이상하지 않을 수 있다.

```typescript
type Handler = (event: MouseEvent) => void;
type GeneralHandler = (event: Event) => void;

let handler: Handler;
let generalHandler: GeneralHandler;

// strictFunctionTypes 없이는 이게 허용된다
handler = generalHandler; // GeneralHandler는 Handler보다 넓은 타입을 받는다
```

`MouseEvent`는 `Event`의 하위 타입이다. 함수의 반환 타입은 공변적이지만, 매개변수 타입은 반변적이어야 타입 안전하다. `handler = generalHandler`는 직관적으로 "더 일반적인 핸들러를 쓰니까 괜찮겠지"라고 느껴지지만, `handler`를 `MouseEvent`만 올 것으로 가정하는 코드에 `generalHandler`를 넣으면 타입 불일치가 생긴다. `strictFunctionTypes`가 이를 잡는다.

### strictPropertyInitialization과 NestJS의 찜찜함

NestJS를 쓰면 `strictPropertyInitialization`이 찜찜한 상황을 만든다. 의존성 주입으로 받는 서비스를 클래스 프로퍼티로 선언할 때, 생성자 파라미터가 아니라 필드로 쓰면 초기화가 안 된 것처럼 보인다.

```typescript
@Injectable()
export class UserService {
  // strictPropertyInitialization이 켜져 있으면:
  // "Property 'userRepository' has no initializer..." 오류
  @InjectRepository(User)
  private userRepository: Repository<User>; // 오류!

  // 해결: 확정 할당 단언(!)을 쓴다
  @InjectRepository(User)
  private userRepository!: Repository<User>; // OK — "이건 반드시 초기화된다" 단언
}
```

`!`(확정 할당 단언)은 "TypeScript야, 이 프로퍼티는 런타임에 분명히 값이 있을 것이다. 나를 믿어"라는 신호다. NestJS의 DI 시스템이 생성자 이전에 주입을 보장하므로 이 단언은 정당하다. 하지만 남용하면 TypeScript의 안전망이 구멍 난다. DI 프레임워크를 쓸 때만 제한적으로 허용하는 것이 좋다.

---

## 2.2 모듈·해석 계열 — ESM/CJS 혼재의 함정

8장에서 CJS와 ESM의 역사적 분열을 길게 다뤘다. 그 분열이 tsconfig에서 가장 복잡하게 드러나는 곳이 바로 이 계열 옵션들이다. 조합을 잘못 고르면 8장 함정 박스에서 다룬 "에디터는 오류 없음, 런타임은 `Cannot find module`" 상황을 만나게 된다.

| 옵션 | 기본값 | 의미 | 언제 켜는가 |
|------|--------|------|-------------|
| `module` | 상황에 따름 | 출력 JS의 모듈 형식을 지정한다 (`CommonJS`, `ESNext`, `NodeNext`, `Preserve` 등) | Node.js ESM → `NodeNext`. 번들러 사용 → `ESNext` 또는 `Preserve`. CJS 유지 → `CommonJS` |
| `moduleResolution` | 상황에 따름 | import 경로를 어떻게 파일로 해석할지를 결정한다 | `module: NodeNext` → `moduleResolution: NodeNext`. 번들러 → `Bundler`. 레거시 → 쓰지 말자 |
| `target` | `ES3` | 출력 JS의 ECMAScript 버전을 지정한다 | Node.js 최신 LTS → `ES2022`. 구버전 브라우저 지원 필요 → `ES2015` 이하. 번들러가 알아서 한다면 → `ES2022` 이상 |
| `lib` | `target`에 따라 자동 설정 | 타입 체크 시 사용 가능한 전역 타입 집합을 지정한다 | 브라우저 앱 → `["ES2022", "DOM", "DOM.Iterable"]`. Node.js 백엔드 → `["ES2022"]`. DOM 타입 필요 없을 때 `DOM`을 빼면 `document` 등을 쓸 때 오류가 난다 |
| `esModuleInterop` | `false` | CJS 모듈을 `import defaultExport from '...'` 형태로 가져올 수 있게 허용한다 | 거의 항상 `true`. CJS 패키지(React, lodash 등)를 default import 문법으로 쓰려면 필요하다 |
| `allowSyntheticDefaultImports` | `esModuleInterop`과 연동 | default export가 없는 모듈에서도 default import 문법을 허용한다 (타입 체크만 영향, 런타임은 `esModuleInterop`이 처리) | `esModuleInterop: true`이면 자동으로 켜진다 |
| `resolveJsonModule` | `false` | `.json` 파일을 import할 수 있게 한다 | JSON 설정 파일이나 데이터를 TS에서 직접 import할 때 켠다 |
| `allowImportingTsExtensions` | `false` | `.ts`, `.tsx` 확장자를 import 경로에 명시할 수 있게 한다 | 번들러 환경에서만 의미 있다. `noEmit: true` 또는 `emitDeclarationOnly: true`와 함께 써야 한다 |
| `verbatimModuleSyntax` | `false` | 타입 전용 import를 반드시 `import type`으로 명시하게 강제한다 | TS 5.0 이후 번들러 프로젝트에서 권장. `isolatedModules`와 `importsNotUsedAsValues`를 대체한다 |
| `isolatedModules` | `false` | 각 파일을 독립적으로 트랜스파일할 수 없는 기능 사용 시 오류를 낸다 | esbuild, swc, Babel로 빌드하는 프로젝트에서 켠다. `const enum`, 네임스페이스 재내보내기 등을 막는다 |
| `skipLibCheck` | `false` | `node_modules`의 `.d.ts` 파일을 타입 체크하지 않는다 | 실무에서는 거의 항상 `true`. 서드파티 라이브러리 타입 정의의 충돌을 우회한다 |

### module과 moduleResolution의 관계

이 두 옵션이 헷갈리는 이유는 이름이 비슷하지만 역할이 다르기 때문이다. `module`은 **출력 코드**의 형식을 결정하고, `moduleResolution`은 **소스 코드에서 import할 때** 파일을 어떻게 찾을지를 결정한다.

Node.js ESM 프로젝트라면 이 조합이 맞다:

```json
{
  "module": "NodeNext",
  "moduleResolution": "NodeNext"
}
```

`NodeNext`는 Node.js의 ESM 규칙을 따른다. 상대 경로 import에 확장자(`.js`)를 명시해야 하고, `package.json`의 `"exports"` 필드를 이해하고, `.mts`/`.cts` 파일도 처리한다.

번들러(Vite, webpack, esbuild)를 쓰는 브라우저 앱이라면:

```json
{
  "module": "ESNext",
  "moduleResolution": "Bundler"
}
```

`Bundler`는 "번들러가 알아서 파일을 찾아줄 것이다"는 선언이다. 확장자 생략이 허용되고, `package.json`의 `"exports"` 필드를 이해하면서도 Node.js ESM의 엄격한 규칙은 적용하지 않는다. Vite, Bun 등의 도구가 이 값을 권장한다.

### target의 의미와 lib의 관계

`target`을 올리면 출력 코드가 현대적이 된다. `"ES2022"`로 지정하면 async/await, optional chaining, nullish coalescing 같은 문법이 그대로 출력된다. 구버전 환경으로 낮출 필요가 없다면 `"ES2022"` 이상을 쓰는 편이 낫다.

`lib`는 타입 체크 시 "이 환경에 어떤 전역 API가 있는가"를 알려주는 목록이다. `"DOM"`이 들어있어야 `document.querySelector()`가 타입을 가진다. Node.js 백엔드에서 `"DOM"`을 넣으면 브라우저 전용 API를 실수로 쓸 때 오류를 못 잡는다. 반대로 브라우저 앱에서 `"DOM"`을 빼면 DOM API 사용 시 오류가 난다.

`lib`를 명시하지 않으면 `target`에서 자동으로 유추된다. `"target": "ES2022"`이면 `"lib": ["ES2022"]`와 같다. DOM이 필요하면 명시해야 한다.

### esModuleInterop의 태생

CJS 모듈에는 default export라는 개념이 없다. `module.exports = React`처럼 쓴 것은 "모듈 자체가 React다"는 의미고, ESM의 `export default React`와 다르다. `esModuleInterop` 없이는 CJS React를 `import React from 'react'`가 아니라 `import * as React from 'react'`로 가져와야 했다.

`esModuleInterop: true`는 TypeScript가 CJS 모듈을 default export가 있는 것처럼 다루는 헬퍼를 생성하도록 한다. 실제로 컴파일된 코드에 `__importDefault` 같은 헬퍼가 삽입된다. `importHelpers: true`와 함께 쓰면 이 헬퍼를 `tslib` 패키지에서 가져와 코드 중복을 줄일 수 있다.

---

## 2.3 출력 계열 — 어디에 무엇을 내보낼 것인가

타입 체크가 목적이라면 파일을 출력할 필요가 없다. 라이브러리라면 `.d.ts` 파일도 내보내야 한다. 이 카테고리는 빌드 결과물의 형태를 결정한다.

| 옵션 | 기본값 | 의미 | 언제 켜는가 |
|------|--------|------|-------------|
| `outDir` | 없음 | 컴파일된 JS 파일의 출력 디렉터리를 지정한다 | 소스와 출력을 분리할 때. `"./dist"`가 관례 |
| `rootDir` | 소스 파일의 공통 루트 자동 설정 | 소스 파일의 루트 디렉터리를 명시한다 | `outDir`을 쓸 때 함께 쓴다. 없으면 소스 구조를 TypeScript가 유추해 예상치 못한 디렉터리 구조가 나올 수 있다 |
| `declaration` | `false` | `.d.ts` 타입 선언 파일을 생성한다 | npm 패키지를 배포하는 라이브러리에서 필수. `composite: true`이면 자동으로 켜진다 |
| `declarationMap` | `false` | `.d.ts.map` 파일을 생성해 원본 TS 소스로의 이동을 지원한다 | 라이브러리 소비자가 IDE에서 "정의로 이동"을 눌렀을 때 `.d.ts`가 아니라 원본 `.ts`로 이동할 수 있게 한다 |
| `sourceMap` | `false` | `.js.map` 파일을 생성한다 | 디버깅 시 컴파일된 JS에서 원본 TS를 추적할 때. 대부분의 프로젝트에서 켜둔다 |
| `inlineSourceMap` | `false` | 소스맵을 별도 파일 대신 JS 파일 안에 Base64 인코딩으로 삽입한다 | 파일 배포보다 단일 파일 배포가 편한 경우. `sourceMap`과 함께 쓸 수 없다 |
| `removeComments` | `false` | 출력 JS에서 주석을 제거한다 | 프로덕션 번들에서 파일 크기를 줄일 때. 번들러가 이미 처리한다면 굳이 켜지 않아도 된다 |
| `noEmit` | `false` | 파일을 전혀 출력하지 않는다 | 타입 체크만 하고 빌드는 다른 도구(esbuild, swc)에 맡길 때. `tsc --noEmit`과 같은 효과 |
| `emitDeclarationOnly` | `false` | JS 파일은 생성하지 않고 `.d.ts` 파일만 생성한다 | 트랜스파일은 번들러가 하고 타입 선언만 tsc로 만들 때. 라이브러리 개발에 유용 |
| `importHelpers` | `false` | async/await, spread 등의 변환 헬퍼를 `tslib` 패키지에서 가져온다 | `target`이 낮아서 폴리필이 많이 삽입될 때. `tslib`을 의존성에 추가해야 한다 |
| `downlevelIteration` | `false` | `for...of`, 스프레드, 구조분해를 더 정확하게(하지만 코드가 커지게) 변환한다 | `target: ES5` 등 낮은 환경에서 `Symbol.iterator` 기반 순회를 정확히 동작시킬 때 |

### noEmit vs emitDeclarationOnly

이 두 옵션은 목적이 다르다.

`noEmit: true`는 tsc를 타입 체커로만 쓸 때 선택한다. "나는 빌드는 Vite에게 맡기고, tsc로는 오류만 확인하겠다"는 선언이다. CI에서 `tsc --noEmit`으로 타입 오류를 잡고, 실제 빌드는 번들러가 한다.

`emitDeclarationOnly: true`는 "JS 파일은 번들러가 만들지만, 타입 선언 파일(`.d.ts`)은 tsc가 만들어야 한다"는 상황에서 쓴다. 라이브러리 개발에서 흔한 패턴이다.

```json
// 라이브러리 tsconfig.json
{
  "compilerOptions": {
    "declaration": true,
    "emitDeclarationOnly": true,  // .d.ts만 생성
    "outDir": "./dist"
  }
}
```

```json
// package.json 빌드 스크립트
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "build:types": "tsc --emitDeclarationOnly",
    "build:js": "esbuild src/index.ts --bundle --outfile=dist/index.js",
    "build": "pnpm build:types && pnpm build:js"
  }
}
```

---

## 2.4 호환성·JSX 계열

JavaScript 코드를 TypeScript로 섞어 쓰는 마이그레이션 시나리오, 그리고 React 등에서 쓰는 JSX 처리 옵션들이다.

| 옵션 | 기본값 | 의미 | 언제 켜는가 |
|------|--------|------|-------------|
| `allowJs` | `false` | `.js`, `.jsx` 파일을 TypeScript 프로젝트에서 함께 컴파일한다 | JS → TS 점진적 마이그레이션 시. 9장 마이그레이션 패턴 참조 |
| `checkJs` | `false` | `allowJs`로 포함된 JS 파일에도 타입 검사를 적용한다 | JS 파일에도 타입 힌트를 주고 싶을 때. `allowJs`가 켜져 있어야 한다 |
| `maxNodeModuleJsDepth` | `0` | `node_modules`에서 JS 파일을 검색할 최대 깊이를 설정한다 | `allowJs`와 함께 서드파티 JS 패키지에도 타입 추론을 시도할 때. 기본 `0`은 `node_modules` JS를 무시한다 |
| `jsx` | `"preserve"` (JSX 파일) | JSX 문법을 어떻게 처리할지를 지정한다 | React 프로젝트 → `"react-jsx"` (React 17+) 또는 `"react"` (구형). Next.js, Vite가 자동 설정하는 경우 많음 |
| `jsxImportSource` | `"react"` | `jsx: "react-jsx"` 사용 시 JSX 팩토리를 가져올 패키지를 지정한다 | Preact → `"preact"`. Solid.js → `"solid-js/h"`. |
| `jsxFactory` | `"React.createElement"` | `jsx: "react"` (구형) 사용 시 JSX를 변환할 함수를 지정한다 | React 17 이전 방식이나 Vue JSX 등 커스텀 팩토리를 쓸 때 |

### JSX 옵션의 역사

React 17 이전에는 JSX를 쓰려면 모든 파일에 `import React from 'react'`가 있어야 했다. JSX가 `React.createElement(...)` 호출로 변환되기 때문이다. `jsx: "react"` + `jsxFactory: "React.createElement"` 조합이 이 동작이다.

React 17부터 "새 JSX 변환"이 들어왔다. 자동으로 필요한 헬퍼를 가져오므로 `import React`를 직접 쓸 필요가 없어졌다. `jsx: "react-jsx"` + `jsxImportSource: "react"` 조합이 이를 지원한다. Vite의 React 템플릿이 이 설정을 기본으로 쓴다.

`jsx: "preserve"`는 JSX를 변환하지 않고 그대로 출력한다. 번들러(Vite, esbuild)가 JSX 변환을 담당하는 경우 tsc는 타입 체크만 하고 JSX는 건드리지 않도록 이 값을 쓴다.

---

## 2.5 검사 강도 추가 — strict를 넘어서

`strict: true`로 기본 안전망을 쳤다면, 이 카테고리의 옵션들은 한 단계 더 들어가는 선택지다. 팀의 코드 품질 기준이 높다면 하나씩 켜볼 만하다. 다만 기존 코드에 적용하면 오류가 꽤 나올 수 있다. 찬찬히 살펴보자.

| 옵션 | 기본값 | 의미 | 언제 켜는가 |
|------|--------|------|-------------|
| `noUnusedLocals` | `false` | 사용하지 않는 지역 변수를 오류로 잡는다 | 코드 품질에 민감한 팀. 다만 에디터의 경고와 중복될 수 있다 |
| `noUnusedParameters` | `false` | 사용하지 않는 함수 매개변수를 오류로 잡는다 | `_`로 시작하는 매개변수명은 예외 처리된다 (`_event` 등) |
| `exactOptionalPropertyTypes` | `false` | 옵셔널 프로퍼티에 `undefined`를 명시적으로 할당하는 것을 막는다 | `strict` 이상의 엄격함을 원할 때. 기존 코드에서 켜면 오류가 많이 나온다 |
| `noUncheckedIndexedAccess` | `false` | 배열 인덱스나 객체 키로 접근한 값에 `undefined` 가능성을 추가한다 | 배열 경계 오류를 타입 레벨에서 잡고 싶을 때. 상당히 엄격해진다 |
| `noImplicitOverride` | `false` | 부모 클래스의 메서드를 오버라이드할 때 `override` 키워드를 강제한다 | 클래스 계층이 복잡한 프로젝트. Java/Kotlin의 `@Override`와 유사한 역할 |
| `noPropertyAccessFromIndexSignature` | `false` | 인덱스 시그니처가 있는 타입에서 점 표기법 접근을 막는다 (`obj.key` 대신 `obj["key"]`를 요구) | 인덱스 시그니처와 명시적 프로퍼티를 명확히 구분하고 싶을 때 |
| `noFallthroughCasesInSwitch` | `false` | switch 문에서 `break` 없이 다음 case로 넘어가는 것을 오류로 잡는다 | 의도치 않은 fallthrough를 방지하고 싶을 때. 대부분의 프로젝트에서 켜두는 편이 낫다 |

### noUncheckedIndexedAccess — 배열이 위험한 이유

Java에서 배열 경계를 벗어나면 `ArrayIndexOutOfBoundsException`이 런타임에 난다. TypeScript의 기본 동작은 배열 인덱스 접근의 결과 타입이 항상 원소 타입이라고 가정한다. 즉 `string[]`에서 `arr[999]`를 하면 결과가 `string`이지, `string | undefined`가 아니다.

```typescript
const arr = ['a', 'b', 'c'];
const item = arr[999]; // 기본: 타입이 string (하지만 런타임엔 undefined)

// noUncheckedIndexedAccess: true이면
const item = arr[999]; // 타입이 string | undefined
if (item) {
  console.log(item.toUpperCase()); // 이제 안전하다
}
```

이 옵션을 켜면 코드가 더 안전해지지만, 배열에 접근할 때마다 `undefined` 가능성을 처리해야 한다. `for...of`나 `forEach`로 순회하는 코드에는 영향 없고, 인덱스로 직접 접근하는 코드에만 영향을 준다.

### exactOptionalPropertyTypes — 옵셔널의 두 얼굴

```typescript
type Config = {
  port?: number;  // number | undefined
};

const config: Config = {
  port: undefined  // exactOptionalPropertyTypes 없이는 허용
};
```

`exactOptionalPropertyTypes: true`이면 `port?: number`는 "port가 없거나(키 자체가 없음), port가 있으면 number"라는 의미가 된다. `port: undefined`를 명시적으로 할당하는 것은 키가 존재하되 값이 undefined인 상태로, 이를 오류로 잡는다. 미묘하지만 직렬화 관련 코드에서 차이가 난다.

---

## 2.6 monorepo·project references 계열

모노레포를 구성할 때 TypeScript의 Project References를 제대로 활용하지 않으면 IDE가 느려지고 빌드가 비효율적이 된다. 8장의 "monorepo IDE 폭주" 함정이 이 카테고리의 옵션들을 제대로 안 쓸 때 발생하는 증상이다.

| 옵션 | 기본값 | 의미 | 언제 켜는가 |
|------|--------|------|-------------|
| `composite` | `false` | 이 tsconfig가 다른 프로젝트에서 참조될 수 있음을 선언한다 | 모노레포에서 다른 패키지가 이 패키지를 `references`로 가리킬 때 필수 |
| `incremental` | `false` | 증분 빌드 정보를 `.tsbuildinfo` 파일에 저장해 다음 빌드를 빠르게 한다 | 빌드가 느릴 때 단독으로 켤 수 있다. `composite: true`이면 자동으로 켜진다 |
| `tsBuildInfoFile` | `.tsbuildinfo` | 증분 빌드 정보 파일의 위치를 지정한다 | `incremental` 또는 `composite` 사용 시 파일 위치를 커스텀할 때 |
| `references` | 없음 | 이 프로젝트가 의존하는 다른 tsconfig들의 목록 | 모노레포에서 패키지 간 의존성을 TS 레벨에서 선언할 때 |
| `paths` | 없음 | `import '@/utils'` 같은 경로 별칭을 정의한다 | 상대 경로를 줄이고 싶을 때. 단, 빌드 결과에 반영되지 않으므로 번들러에도 같은 설정이 필요하다 |
| `baseUrl` | 없음 | `paths`를 해석하는 기준 디렉터리를 설정한다 | `paths`와 함께 쓴다. 보통 프로젝트 루트 (`"."`) |

### composite, references, incremental의 관계

세 옵션이 함께 작동하는 방식을 이해하면 모노레포 설정이 훨씬 명확해진다.

**`composite: true`** — 이 패키지는 다른 패키지가 `.d.ts`로 참조한다는 선언이다. 켜면 `declaration: true`와 `incremental: true`가 자동으로 켜진다.

**`references`** — 내가 의존하는 다른 패키지의 tsconfig를 가리킨다. `tsc --build`(-b)를 실행하면 의존성 그래프를 따라 필요한 것만 다시 컴파일한다.

**`incremental: true`** — 빌드 정보를 저장해 변경된 파일만 다시 컴파일한다. `composite`이 자동으로 켜주지만, 단독 프로젝트에서도 빌드 속도를 높이려면 단독으로 켤 수 있다.

```json
// packages/ui/tsconfig.json — 참조되는 쪽
{
  "compilerOptions": {
    "composite": true,      // 다른 패키지에서 참조 가능
    "declaration": true,    // .d.ts 생성 (composite이 자동 켬)
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

```json
// apps/web/tsconfig.json — 참조하는 쪽
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist"
  },
  "references": [
    { "path": "../../packages/ui" },
    { "path": "../../packages/utils" }
  ]
}
```

이 구조에서 `tsc -b apps/web`을 실행하면, `packages/ui`와 `packages/utils`가 먼저 컴파일되고 나서 `apps/web`이 컴파일된다. `packages/ui`가 변경되지 않았다면 `.d.ts`를 재사용한다.

### paths 별칭의 함정

`paths` 옵션은 실무에서 자주 쓰이지만, 오해를 낳기도 한다. TypeScript는 `paths`를 타입 체크 시 경로 해석에만 쓴다. 실제 컴파일된 JS에는 별칭이 그대로 남는다.

```typescript
// 소스
import { formatDate } from '@/utils/date';

// 컴파일된 JS (paths 변환 없음!)
import { formatDate } from '@/utils/date'; // 런타임에 이 경로를 찾을 수 없다!
```

`@/utils/date`라는 경로를 런타임에서 찾으려면 번들러나 모듈 로더에도 같은 별칭을 등록해야 한다.

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')  // tsconfig paths와 동일하게
    }
  }
});
```

이걸 빠뜨리면 에디터는 오류 없음, 런타임은 `Cannot find module '@/utils/date'`가 된다. 8장 함정 박스 ②의 원인 중 하나가 바로 이것이다.

---

## 2.7 기타 — 레거시와 중요 옵션들

| 옵션 | 기본값 | 의미 | 언제 켜는가 |
|------|--------|------|-------------|
| `forceConsistentCasingInFileNames` | `false` | 파일 이름의 대소문자를 일관되게 유지하도록 강제한다 | 항상 켜는 편이 낫다. macOS(대소문자 무시 파일 시스템)에서 개발해도 Linux 환경에서 `Cannot find module` 오류가 나는 것을 방지한다 |
| `useDefineForClassFields` | `target`에 따라 다름 | 클래스 필드를 `Object.defineProperty`로 초기화한다 (TC39 표준 동작) | `target: ES2022` 이상이면 자동으로 `true`. 레거시 데코레이터(`experimentalDecorators`)와 충돌할 수 있다 |
| `experimentalDecorators` | `false` | TC39 Stage 2 시절의 레거시 데코레이터를 활성화한다 | NestJS, Angular, TypeORM 등 레거시 데코레이터 기반 프레임워크를 쓸 때 필수. TS 5.0 이후의 표준 데코레이터와 다르다 |
| `emitDecoratorMetadata` | `false` | 데코레이터에 타입 메타데이터를 런타임에 포함한다 (`reflect-metadata` 필요) | NestJS의 DI, TypeORM의 엔티티 매핑 등. `experimentalDecorators: true`와 함께 써야 한다 |

### forceConsistentCasingInFileNames — 작지만 중요한 옵션

macOS에서 개발하고 Linux에서 배포하는 팀은 이 옵션의 중요성을 한 번쯤 경험으로 배운다. macOS의 HFS+ 파일 시스템은 대소문자를 무시한다(`UserService.ts`와 `userService.ts`를 같은 파일로 본다). 그래서 `import { UserService } from './userservice'`가 macOS에서는 잘 동작한다.

Linux의 ext4 파일 시스템은 대소문자를 구분한다. 배포하면 `Cannot find module './userservice'`가 터진다. 이런 난감한 상황을 방지하는 것이 `forceConsistentCasingInFileNames: true`다.

### experimentalDecorators와 useDefineForClassFields의 충돌

이 두 옵션이 함께 있을 때 문제가 생기는 이유를 이해해두면 NestJS 프로젝트에서 헤매지 않는다.

TC39 표준 클래스 필드(`useDefineForClassFields: true`)는 `Object.defineProperty`로 필드를 초기화한다. 레거시 데코레이터(`experimentalDecorators`)는 프로퍼티 기술자를 수정하는 방식으로 동작하는데, `Object.defineProperty` 방식과 충돌한다.

NestJS가 권장하는 설정에서 `target: ES2021` 이하를 쓰거나 `useDefineForClassFields: false`를 명시하는 이유가 여기에 있다. NestJS 공식 문서의 tsconfig를 그대로 쓰는 편이 이 충돌을 피하는 가장 안전한 방법이다.

### emitDecoratorMetadata와 reflect-metadata

`emitDecoratorMetadata: true`를 켜면 TypeScript가 데코레이터가 적용된 클래스의 타입 정보를 런타임 메타데이터로 삽입한다. NestJS가 `@Inject()` 데코레이터로 어떤 타입의 의존성을 주입해야 하는지를 런타임에 알 수 있는 것이 이 덕분이다.

단, 이 기능은 `reflect-metadata` 패키지를 `import 'reflect-metadata'`로 애플리케이션 진입점에서 로드해야 동작한다. NestJS 앱에서 `main.ts` 최상단에 항상 이 import가 있는 이유다.

---

## 3. 현실의 tsconfig 템플릿 5개

이론은 충분하다. 지금부터는 복사해 바로 쓸 수 있는 템플릿을 시나리오별로 제공한다. 각 옵션 옆의 주석이 "왜 이 값인가"를 설명한다.

### 템플릿 1 — npm 라이브러리 (publish용)

TypeScript로 작성해 npm에 배포하는 라이브러리다. 사용자가 어떤 환경(Node.js, Bun, 번들러)에서 쓸지 모르므로 최대한 호환성 있게 설정한다.

```json
{
  "compilerOptions": {
    // 타입 안전
    "strict": true,

    // 출력 타깃 — Node.js 18 LTS 이상을 지원 대상으로
    "target": "ES2022",
    "lib": ["ES2022"],

    // 모듈 — NodeNext로 CJS/ESM 모두 처리
    // package.json의 exports 필드와 맞춰 듀얼 패키지로 배포할 수 있다
    "module": "NodeNext",
    "moduleResolution": "NodeNext",

    // 출력 — 라이브러리는 .d.ts와 소스맵 필수
    "declaration": true,        // 소비자가 타입을 사용할 수 있도록
    "declarationMap": true,     // 소비자가 "정의로 이동"할 때 원본 TS로 이동
    "sourceMap": true,          // 디버깅 지원
    "outDir": "./dist",
    "rootDir": "./src",

    // 번들러 없이 tsc가 직접 빌드하므로 noEmit 사용 안 함
    "emitDeclarationOnly": false,

    // 서드파티 타입 충돌 방지 — 실무 필수
    "skipLibCheck": true,

    // CJS import 문법 편의
    "esModuleInterop": true,

    // 대소문자 일관성
    "forceConsistentCasingInFileNames": true,

    // esbuild, swc로 빌드하는 소비자를 위해
    "isolatedModules": true,

    // 코드 품질
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

라이브러리를 CJS와 ESM 두 형태로 배포(듀얼 패키지)할 때는 별도 `tsconfig.cjs.json`과 `tsconfig.esm.json`을 만들고, 각각 `"module": "CommonJS"`와 `"module": "ESNext"`로 두 번 빌드하는 방법이 일반적이다.

### 템플릿 2 — Vite + React 앱 (브라우저)

Vite가 번들링과 트랜스파일을 담당하고, tsc는 타입 체크만 한다. Vite의 기본 React 템플릿(`pnpm create vite --template react-ts`)이 생성하는 설정을 기반으로 한다.

```json
{
  "compilerOptions": {
    // 타입 안전
    "strict": true,

    // 타깃 — Vite가 트랜스파일하므로 모던하게
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],  // 브라우저 앱이므로 DOM 포함

    // 모듈 — 번들러에게 맡긴다
    "module": "ESNext",
    "moduleResolution": "Bundler",  // Vite 번들러 기반

    // JSX — React 17+ 새 변환
    "jsx": "react-jsx",

    // Vite가 빌드하므로 tsc는 타입 체크만
    "noEmit": true,

    // Vite가 파일을 독립적으로 처리하므로 필수
    "isolatedModules": true,

    // .ts 확장자 없이 import 허용 (번들러가 처리)
    // "allowImportingTsExtensions": true,  // noEmit과 함께만 사용 가능

    // 경로 별칭 — vite.config.ts의 resolve.alias와 동일하게
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    },

    // 서드파티 타입 충돌 방지
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,

    // 코드 품질
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]  // vite.config.ts용 별도 config
}
```

Vite 프로젝트는 보통 `tsconfig.node.json`을 별도로 둔다. `vite.config.ts` 자체는 Node.js 환경에서 실행되므로, 브라우저 앱 설정(`DOM`, `ESNext`)과는 다른 설정이 필요하다.

```json
// tsconfig.node.json — vite.config.ts와 빌드 스크립트용
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

### 템플릿 3 — 모노레포 (composite + project references)

pnpm workspace를 쓰는 모노레포다. 루트의 `tsconfig.base.json`을 각 패키지가 상속한다.

```json
// tsconfig.base.json (루트, 공통 설정)
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

```json
// packages/core/tsconfig.json (공통 비즈니스 로직 패키지)
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,     // 다른 패키지가 이 패키지를 참조할 수 있다
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"]
}
```

```json
// packages/ui/tsconfig.json (UI 컴포넌트 패키지 — React)
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],  // base의 lib를 오버라이드
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "references": [
    { "path": "../core" }  // core에 의존한다
  ]
}
```

```json
// apps/web/tsconfig.json (Next.js 웹 앱)
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "jsx": "preserve",          // Next.js가 JSX를 처리한다
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "noEmit": true,             // Next.js가 빌드를 담당한다
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src", "next-env.d.ts"],
  "references": [
    { "path": "../../packages/ui" },
    { "path": "../../packages/core" }
  ]
}
```

모노레포 루트에서 `tsc -b`를 실행하면 의존성 그래프를 따라 필요한 패키지만 재컴파일한다. Turborepo를 함께 쓰면 캐싱까지 활용해 훨씬 빠르다.

### 템플릿 4 — Node.js 백엔드

Express, Hono, Fastify 같은 Node.js 백엔드 서버다. ESM으로 구성하는 현대적인 설정이다.

```json
{
  "compilerOptions": {
    // 타입 안전
    "strict": true,

    // Node.js 20 LTS 이상 대상
    "target": "ES2022",
    "lib": ["ES2022"],  // DOM 없음 — 서버 앱

    // ESM 기반 Node.js 앱
    // package.json에 "type": "module" 필요
    "module": "NodeNext",
    "moduleResolution": "NodeNext",

    // 출력
    "outDir": "./dist",
    "rootDir": "./src",
    "sourceMap": true,    // 프로덕션 디버깅 지원

    // tsc가 직접 빌드 (esbuild로 대체하면 noEmit: true + emitDeclarationOnly: true)
    // "noEmit": false,  // 기본값

    // 서드파티 타입 충돌 방지
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,

    // 각 파일 독립 처리 가능 여부 — esbuild로 빌드 시 true
    "isolatedModules": true,

    // 코드 품질
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

esbuild로 빌드하고 tsc를 타입 체크에만 쓴다면 `"noEmit": true`로 바꾸고 `package.json` 스크립트를 다음처럼 구성한다.

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "build": "esbuild src/index.ts --bundle --platform=node --target=node20 --outfile=dist/index.js",
    "dev": "tsx watch src/index.ts",
    "ci": "pnpm typecheck && pnpm build && pnpm test"
  }
}
```

Node.js 백엔드에서 ESM을 쓸 때 주의할 점이 있다. 상대 경로 import에 `.js` 확장자를 명시해야 한다. TypeScript 소스 파일이 `.ts`여도 컴파일 결과는 `.js`이므로, import 경로에 `.js`를 쓴다.

```typescript
// 올바른 ESM 상대 경로 import
import { UserService } from './user.service.js';  // .js 명시

// 잘못된 방식 (CJS에서는 됐지만 ESM에서는 안 됨)
import { UserService } from './user.service';     // 확장자 없음 — NodeNext에서 오류
```

### 템플릿 5 — NestJS (데코레이터 + 메타데이터)

NestJS는 레거시 데코레이터와 `reflect-metadata`에 의존한다. 다른 템플릿과 다른 점들이 있다.

```json
{
  "compilerOptions": {
    // 타입 안전
    "strict": true,

    // NestJS는 Node.js 대상 — CJS가 더 안정적이다
    "target": "ES2021",       // ES2022가 아닌 이유: useDefineForClassFields 충돌 회피
    "lib": ["ES2021"],
    "module": "CommonJS",     // NestJS 생태계는 여전히 CJS가 기본
    "moduleResolution": "Node10",  // CJS 방식의 해석

    // 출력
    "outDir": "./dist",
    "sourceMap": true,
    "removeComments": true,   // 프로덕션 배포 시 주석 제거

    // 레거시 데코레이터 — NestJS, TypeORM 필수
    "experimentalDecorators": true,

    // 런타임 타입 메타데이터 — NestJS DI가 의존
    "emitDecoratorMetadata": true,

    // useDefineForClassFields와 experimentalDecorators 충돌 방지
    // target: ES2021 이하이면 자동으로 false지만 명시적으로 선언
    // "useDefineForClassFields": false,  // 필요 시 명시

    // 서드파티 타입 충돌 방지
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,

    // 코드 품질
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true  // 상속 구조가 복잡하므로 override 명시 강제
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "test", "**/*.spec.ts"]
}
```

NestJS 앱의 `main.ts` 진입점에는 반드시 `reflect-metadata` import가 먼저 와야 한다.

```typescript
// main.ts — NestJS 앱 진입점
import 'reflect-metadata';   // emitDecoratorMetadata 동작을 위해 반드시 먼저

import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();
```

NestJS가 ESM으로 전환하는 작업은 2025년 기준으로 진행 중이다. 공식 지원이 완전히 안정화되기 전까지는 CJS 기반으로 유지하는 편이 안전하다. 만약 ESM으로 전환한다면 `module: NodeNext`, `moduleResolution: NodeNext`로 바꾸고, ESM과 레거시 데코레이터의 호환성 이슈를 별도로 확인해야 한다.

---

## 마무리 — tsconfig는 선택의 기록이다

tsconfig는 단순한 컴파일러 설정 파일이 아니다. "이 프로젝트가 어떤 환경을 대상으로 하는가", "얼마나 엄격한 타입 검사를 원하는가", "빌드는 누가 담당하는가"에 대한 팀의 선택을 기록한 문서다.

처음엔 템플릿을 가져다 쓰는 게 맞다. Matt Pocock의 tsconfig cheat sheet, 프레임워크 공식 문서의 권장 설정, 이 부록의 템플릿들이 출발점이다. 그 다음은 각 옵션이 왜 거기 있는지를 이해하는 것이다. 이해 없이 복사한 설정은 에러가 날 때 어디를 봐야 할지 모르게 만든다.

한 가지 당부를 덧붙이자면, tsconfig를 공유할 때는 `extends`를 활용하는 편이 낫다. `tsconfig.base.json`에 공통 옵션을 두고, 목적별 파일(`tsconfig.build.json`, `tsconfig.test.json`)이 필요한 부분만 오버라이드한다. 전체를 복사해 붙이면 나중에 변경점을 추적하기가 번거롭다.

이 부록에서 모든 옵션을 외울 필요는 없다. "이 옵션이 어떤 카테고리에 속하는가"를 안다면, 처음 보는 옵션도 어렵지 않다. 타입 안전성이라면 strict 계열, 모듈 관련이라면 module/moduleResolution, 출력 파일이라면 outDir/declaration 계열을 먼저 살펴보면 된다.

tsconfig 때문에 하루를 날렸던 경험이 있다면, 이 부록이 그 다음 번의 낭비를 줄여주길 바란다.


---

# 부록 C. TS CLI 한 개 끝까지 짓기 — 워크쓰루

REST API 하나를 호출해 결과를 표로 찍어주는 도구를 만든다고 해보자. 기획 회의에서 "그냥 curl이랑 jq 쓰면 안 돼요?"라는 질문이 나왔다면, 이미 도구가 필요한 시점이 온 것이다. curl + jq 조합은 강력하지만 사람마다 옵션을 외우는 방식이 다르고, 팀 전체가 공유하기가 번거롭다. 이름을 붙이고, 타입을 달고, 배포 가능한 형태로 만드는 순간 그 도구는 *팀의 자산*이 된다.

10장이 CLI 생태계의 *지형도*였다면, 부록 C는 *한 개를 끝까지 짓는 결정의 흐름*이다. 어느 라이브러리를 고를지, tsconfig에서 어느 옵션을 왜 켜는지, 에러를 어떻게 다룰지, 배포 채널을 어디로 삼을지 — 각 결정 지점에서 "왜 이 선택인가"를 함께 살펴보자.

**전체 동작하는 코드와 step-by-step 커밋은 `toby-ai/ts-cli-walkthrough` GitHub repo에 있다.** 이 부록에서는 결정 지점과 핵심 패턴만 다룬다. 코드를 복사해 붙여넣기보다 repo를 clone해서 각 커밋을 따라가는 편이 훨씬 더 많이 남는다.

---

## Step 1. 프로젝트 셋업 — "왜 Bun인가"

### Node.js를 두고 Bun을 선택하는 이유

처음 프로젝트를 열 때 첫 번째 결정이 기다린다. Node.js인가, Bun인가.

Node.js를 쓰면 안정성은 보장된다. 생태계가 가장 크고, 팀원 대부분이 이미 익숙하다. 그런데 CLI 개발 흐름에서 번거로운 지점이 있다. TypeScript를 실행하려면 `ts-node`나 `tsx` 같은 래퍼가 필요하고, 단일 실행 파일을 만들려면 `pkg`나 `nexe` 같은 별도 도구가 또 필요하다. 개발·빌드·배포 파이프라인이 도구 여럿으로 분산된다.

Bun은 이 세 가지를 하나로 합친다.

- **TS 직접 실행**: `bun run src/cli.ts`가 그냥 동작한다. `ts-node` 설치 불필요.
- **단일 실행 파일 빌드**: `bun build --compile`로 명령 한 줄에 끝난다.
- **빠른 패키지 설치**: `bun install`이 npm보다 몇 배 빠르다. 워크플로 반복 속도가 달라진다.

물론 선택지가 하나는 아니다. Node.js + esbuild + `pkg` 조합도 동작한다. 하지만 CLI 하나를 빠르게 짓고 싶은 상황이라면 Bun이 *도구 여러 개를 외울 필요 없이 하나로 충분한* 선택이다.

> Deno도 비슷한 통합 환경을 제공한다. 차이는 보안 모델이다. Deno는 권한을 명시적으로 선언해야 한다(`--allow-net`, `--allow-env`). 배포할 도구가 어떤 권한을 쓰는지 선언 자체가 문서가 되는 장점이 있다. 보안 감사가 중요한 도구라면 Deno가 안전망 하나를 더 준다. 이번 워크쓰루는 Bun을 기준으로 진행하지만, 전체 코드는 `toby-ai/ts-cli-walkthrough` repo에서 Deno 버전도 브랜치로 제공한다.

### tsconfig — 1줄씩 결정

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "verbatimModuleSyntax": true,
    "outDir": "dist"
  }
}
```

다섯 줄이지만 각각 이유가 있다.

**`target: "ES2022"`** — Bun이 최신 ECMAScript를 지원하므로 굳이 낮출 이유가 없다. ES2022에는 `at()`, `Object.hasOwn()`, private class fields(`#field`)가 포함된다.

**`module: "NodeNext"` + `moduleResolution: "NodeNext"`** — 이 둘은 항상 짝으로 간다. NodeNext는 `.js` 확장자를 import path에 명시하도록 강제한다. 찜찜하게 느껴질 수 있다 — "`.ts` 파일인데 왜 `.js`로 import해야 하지?" — 하지만 이것이 ESM의 실제 동작 방식이다. TS가 `.ts`를 컴파일하면 `.js`가 나오고, Node.js는 `.js`를 찾는다. 이 강제가 없으면 런타임에 "Cannot find module" 에러가 나와 당황스러운 상황이 생긴다.

**`strict: true`** — 10개 내외의 엄격한 검사를 한꺼번에 켠다. 처음에는 에러가 쏟아져 난감하지만, 이 고통이 후반부의 `as` 남용을 막는다. 처음부터 켜두는 편이 나중에 켜는 것보다 훨씬 낫다.

**`verbatimModuleSyntax: true`** — `import type`을 명시하도록 강제한다. 타입만 가져오는 import는 런타임에 사라져야 하므로, `import type { Foo } from './foo'`처럼 명시하면 번들러가 정확히 무엇을 제거할지 알 수 있다. 8장의 CJS/ESM 경계 이야기가 여기서 실전으로 살아난다.

### 디렉터리 구조

```
my-cli/
├── src/
│   ├── cli.ts          # 진입점 — Commander 정의, subcommand 등록
│   ├── commands/
│   │   └── prs.ts      # pr list 커맨드 로직
│   ├── lib/
│   │   ├── api.ts      # HTTP 클라이언트 + zod 검증
│   │   └── output.ts   # chalk, cli-table3, ora 유틸리티
│   └── types/
│       └── index.ts    # 공유 타입 (z.infer로 도출)
├── bin/                # shebang 래퍼 (npm publish용)
├── dist/               # 컴파일 결과 (.gitignore)
├── tsconfig.json
└── package.json
```

`src/types/index.ts`에 공유 타입을 몰아두는 것은 처음에는 과한 느낌이다. 하지만 커맨드가 두세 개만 되어도 타입이 여러 파일에 분산되면 수정할 때 번거롭다. 처음부터 한 곳에 모아두는 습관이 낫다.

---

## Step 2. 인자 정의 — "commander인가, oclif인가"

### 규모 감각이 먼저다

Commander와 oclif 중 무엇을 선택할지는 도구의 규모 감각에서 출발한다.

**commander를 선택할 때**: 커맨드가 열 개 미만이고, 팀 내부에서만 쓰고, 플러그인 시스템이 필요 없다. chain API가 간결해서 파일 하나에서도 전체 구조를 읽을 수 있다.

**oclif를 선택할 때**: 커맨드가 많고, 외부 팀이 플러그인으로 확장할 수 있어야 하고, Heroku CLI처럼 체계적인 구조가 필요하다. 클래스 기반이어서 Java/Spring에서 온 개발자에게 익숙한 면이 있다.

이번 워크쓰루는 사내 도구이므로 commander를 선택한다. 다음 두 가지를 기준으로 선택했다는 점을 기억해두자 — *"지금 규모에 맞는가"*, *"커져도 감당할 수 있는가"*.

### subcommand, flag, positional — 세 가지의 자리

```typescript
// src/cli.ts
import { Command } from 'commander';

const program = new Command();

program
  .name('my-cli')
  .description('사내 PR 조회 도구')
  .version('1.0.0');

program
  .command('prs')
  .description('PR 목록을 조회한다')
  .option('-r, --repo <repo>', '저장소 이름 (owner/repo 형식)')
  .option('-s, --state <state>', 'PR 상태 (open | closed | all)', 'open')
  .option('--json', 'JSON 형식으로 출력')
  .action(async (options) => {
    const parsed = PrListOptionsSchema.parse(options);
    await listPrs(parsed);
  });

program.parse();
```

여기서 `-s, --state <state>`가 *flag*, `prs`가 *subcommand*다. positional 인자(`my-cli prs owner/repo` 처럼 위치로 전달)는 flag보다 입력이 간편하지만, 인자가 두 개 이상이 되면 순서 혼동이 생기기 쉽다. "어느 게 repo고 어느 게 state지?"라는 질문이 생긴다면 positional보다 flag가 낫다.

### z.infer로 인자 타입 좁히기

5장에서 다룬 `z.infer` 패턴이 여기서 실전으로 쓰인다. commander가 파싱한 raw 객체를 zod 스키마로 검증하면 타입과 검증이 항상 동기화된 상태를 유지한다.

```typescript
// src/types/index.ts
import { z } from 'zod';

export const PrListOptionsSchema = z.object({
  repo: z.string().regex(/^[\w.-]+\/[\w.-]+$/, 'owner/repo 형식이어야 합니다'),
  state: z.enum(['open', 'closed', 'all']).default('open'),
  json: z.boolean().default(false),
});

export type PrListOptions = z.infer<typeof PrListOptionsSchema>;
// { repo: string; state: "open" | "closed" | "all"; json: boolean }
```

스키마가 타입의 *단일 출처*다. `state`의 허용 값을 바꾸고 싶으면 스키마 한 곳만 바꾸면 타입도 자동으로 따라온다. commander 파싱 결과가 스키마를 통과하지 못하면 명확한 에러 메시지와 함께 실패한다. 에러 메시지도 `z.string().regex(..., '이 메시지')` 안에 담을 수 있다.

> **전체 코드는 `toby-ai/ts-cli-walkthrough` repo의 `step-02` 커밋에서 확인할 수 있다.** 여기서는 핵심 패턴만 보여준다.

---

## Step 3. HTTP 호출과 zod 검증 — 외부 경계에서 한 번만

### fetch, axios, ky — 결정 지점

세 가지 선택지가 있다.

**fetch (내장)**: Bun과 최신 Node.js에는 fetch가 내장되어 있다. 추가 의존성이 없다. 하지만 에러 처리가 조금 번거롭다 — HTTP 4xx/5xx는 `throw`가 아니라 `response.ok`로 확인해야 한다. 팀이 이미 fetch 패턴에 익숙하다면 충분한 선택이다.

**axios**: 요청/응답 인터셉터, 자동 JSON 변환, 타임아웃 설정이 편하다. 하지만 번들 크기가 크고, 최근에는 fetch 기반으로의 이주가 활발하다. 기존 팀 코드베이스가 axios라면 맞추는 편이 낫다.

**ky**: fetch 위의 얇은 래퍼다. HTTP 에러를 자동으로 throw하고, 재시도 로직이 내장되어 있다. axios보다 번들이 작고, fetch보다 인체공학적이다. 새로 짓는 CLI라면 ky가 균형점이다.

이번 워크쓰루는 ky를 선택한다. 결정의 근거는 간단하다 — 새 프로젝트, 외부 API 호출, 재시도 필요, 번들 크기 관심.

### 외부 경계에서만 검증한다

6장에서 다룬 합의가 여기서 살아난다 — *"외부 경계만 검증한다."* API 응답은 런타임까지 타입을 알 수 없는 영역이다. 컴파일러가 보장해주지 못하는 자리에 zod가 선다.

```typescript
// src/lib/api.ts
import ky from 'ky';
import { z } from 'zod';

const PrSchema = z.object({
  number: z.number(),
  title: z.string(),
  state: z.enum(['open', 'closed']),
  user: z.object({
    login: z.string(),
  }),
  created_at: z.string().datetime(),
  html_url: z.string().url(),
});

const PrListSchema = z.array(PrSchema);
export type Pr = z.infer<typeof PrSchema>;

export async function fetchPrs(repo: string, state: string): Promise<Pr[]> {
  const data = await ky
    .get(`https://api.github.com/repos/${repo}/pulls`, {
      searchParams: { state, per_page: 30 },
      headers: {
        Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      },
    })
    .json();

  return PrListSchema.parse(data);
}
```

API 응답이 `PrListSchema`를 통과하지 못하면 즉시 실패한다. 통과하면 그 이후의 모든 코드는 `Pr` 타입이 보장된다. 이 경계 이후에는 `as`나 `unknown` 캐스팅이 필요 없다. 한 번 검증한 데이터를 다시 검증하는 것은 번거롭기도 하고 의미도 없다 — *외부 경계에서 한 번, 그 이후는 신뢰한다.*

### 에러 처리 — Result 패턴이냐 throw냐

두 가지 선택이 있다.

**throw 방식**: 직관적이고 기존 TS 코드와 어울린다. 문제는 caller가 에러를 잡는다는 보장이 없다. 실수로 `try/catch` 없이 호출하면 에러가 조용히 올라간다.

**Result 패턴**: `{ ok: true, data: T } | { ok: false, error: Error }` 형태의 유니온을 반환한다. caller가 `if (!result.ok)` 분기를 강제하게 되어 에러 처리를 잊기 어렵다. 6장의 Result 패턴이다.

이번 워크쓰루에서는 API 레이어는 throw, 최상위 커맨드 핸들러에서 `try/catch`로 일괄 처리하는 방식을 선택한다. 두 방식이 섞이면 어느 함수가 throw하고 어느 함수가 Result를 반환하는지 파악하기 어려워진다. 팀이 어느 방식을 선택하든, 일관성이 핵심이다.

> **전체 ky 설정, 재시도 로직, ZodError 처리 패턴은 `toby-ai/ts-cli-walkthrough` repo의 `step-03` 커밋에 있다.**

---

## Step 4. 예쁜 출력 — 사람을 위한 출력과 기계를 위한 출력

### chalk + cli-table3 조합

```typescript
// src/lib/output.ts
import Table from 'cli-table3';
import chalk from 'chalk';
import type { Pr } from './api.js';

export function printPrsAsTable(prs: Pr[]): void {
  const table = new Table({
    head: [
      chalk.cyan('#'),
      chalk.cyan('제목'),
      chalk.cyan('작성자'),
      chalk.cyan('상태'),
      chalk.cyan('생성일'),
    ],
    colWidths: [6, 50, 20, 10, 20],
    style: { border: ['grey'] },
  });

  for (const pr of prs) {
    const stateColor = pr.state === 'open' ? chalk.green : chalk.red;
    table.push([
      String(pr.number),
      pr.title.length > 47 ? pr.title.slice(0, 44) + '...' : pr.title,
      pr.user.login,
      stateColor(pr.state),
      new Date(pr.created_at).toLocaleDateString('ko-KR'),
    ]);
  }

  console.log(table.toString());
}
```

chalk는 터미널이 색상을 지원하는지 자동으로 감지한다. CI 환경이나 파이프로 출력을 넘길 때는 색상 코드를 자동으로 제거한다. `NO_COLOR` 환경 변수도 존중한다. 색상 제거를 직접 구현할 필요가 없다.

### `--json` 플래그 — 기계를 위한 출력

파이프라인에서 이 도구의 출력을 다른 도구에 넘긴다고 해보자. 색깔 붙은 표가 아니라 파싱 가능한 JSON이어야 한다.

```typescript
// src/commands/prs.ts
export async function listPrs(options: PrListOptions): Promise<void> {
  const spinner = ora('PR 목록을 가져오는 중...').start();

  try {
    const prs = await fetchPrs(options.repo, options.state);
    spinner.stop();

    if (options.json || !process.stdout.isTTY) {
      // 기계 출력 — JSON, stderr에는 아무것도 없음
      console.log(JSON.stringify(prs, null, 2));
    } else {
      // 사람 출력 — 표, 색상
      printPrsAsTable(prs);
      console.log(chalk.grey(`\n총 ${prs.length}개`));
    }
  } catch (error) {
    spinner.fail('PR 목록 조회에 실패했습니다');
    throw error;
  }
}
```

`process.stdout.isTTY`가 `false`면 출력이 파이프로 가고 있다는 뜻이다. 이때는 `--json` 플래그 없이도 JSON을 출력하는 편이 낫다. `my-cli prs -r owner/repo | jq '.[] | .title'`이 그냥 동작하도록.

### ora 스피너 — 기다리는 사용자를 위해

API 호출이 수 초 걸릴 때 아무 피드백이 없으면 "멈춘 건가?"라는 불안이 생긴다. ora의 스피너가 이 불안을 없애준다. `spinner.succeed()`, `spinner.fail()`, `spinner.warn()`이 스피너를 결과 아이콘으로 교체한다. 이 세 가지만 알면 대부분의 상황을 커버한다.

> **전체 출력 유틸리티 코드는 `toby-ai/ts-cli-walkthrough` repo의 `step-04` 커밋에 있다.**

---

## Step 5. 에러 처리 — `as`를 쓰지 않고 좁히는 패턴들

### 5장 "*as*의 윤리"가 여기서 실전이다

5장에서 다룬 원칙을 기억해보자 — `as`는 컴파일러를 침묵시키는 것이지 실제 타입을 보장하는 것이 아니다. CLI에서 에러를 처리할 때 이 원칙이 가장 자주 시험된다.

```typescript
// 찜찜한 방식 — as로 강제 캐스팅
catch (error) {
  console.error((error as Error).message); // error가 Error가 아닐 수도 있다
}
```

`catch` 블록의 `error`는 `unknown` 타입이다. `as Error`로 단언하면 컴파일러는 침묵하지만, 실제로 `error`가 문자열이거나 null이면 런타임에 터진다.

`as` 없이 좁히는 패턴들을 살펴보자.

**패턴 1 — instanceof 좁히기**

```typescript
catch (error) {
  if (error instanceof Error) {
    // 여기서 error는 Error 타입
    console.error(chalk.red(`오류: ${error.message}`));
  } else {
    console.error(chalk.red('알 수 없는 오류가 발생했습니다'));
  }
}
```

가장 명확하다. `Error`의 하위 클래스(`ZodError`, `HTTPError` 등)도 같이 잡힌다.

**패턴 2 — 타입 가드 함수**

```typescript
function isErrorLike(value: unknown): value is { message: string } {
  return (
    typeof value === 'object' &&
    value !== null &&
    'message' in value &&
    typeof (value as { message: unknown }).message === 'string'
  );
}

catch (error) {
  const message = isErrorLike(error) ? error.message : String(error);
  console.error(chalk.red(`오류: ${message}`));
}
```

`ZodError`처럼 `Error`를 상속하지 않는 에러도 처리할 수 있다.

**패턴 3 — 에러 종류별 분기**

```typescript
import { ZodError } from 'zod';
import { HTTPError } from 'ky';

catch (error) {
  if (error instanceof ZodError) {
    // API 응답이 스키마를 통과하지 못한 경우
    console.error(chalk.red('API 응답 형식이 예상과 다릅니다'));
    console.error(chalk.grey(error.issues.map((i) => `  ${i.path.join('.')}: ${i.message}`).join('\n')));
    process.exit(1);
  }

  if (error instanceof HTTPError) {
    // HTTP 4xx/5xx
    const status = error.response.status;
    if (status === 401) {
      console.error(chalk.red('인증 실패 — GITHUB_TOKEN 환경 변수를 확인하세요'));
      process.exit(1);
    }
    console.error(chalk.red(`HTTP ${status} 오류`));
    process.exit(1);
  }

  // 예상하지 못한 에러
  throw error;
}
```

에러를 *종류별로 분기*하는 것이 핵심이다. 사용자에게 보여줄 에러(인증 실패, 잘못된 입력)와 개발자가 디버그할 에러(예상치 못한 예외)를 구분한다.

### Unix 종료 코드 관례

CLI 도구가 종료할 때 종료 코드가 있다. 파이프라인에서 앞 도구의 성공 여부를 뒤 도구가 알 수 있는 방법이다.

| 코드 | 의미 |
|------|------|
| `0` | 성공 |
| `1` | 일반 오류 (실행은 됐지만 뭔가 잘못됨) |
| `2` | 사용 오류 (잘못된 인자, 잘못된 옵션) |

`process.exit(1)`과 `process.exit(2)`를 상황에 맞게 구분하자. "이 도구를 어떻게 써야 하는지 몰라서 실패"는 2, "쓰는 방법은 맞는데 실행 중 오류"는 1이다. 스크립트에서 `if my-cli prs ...; then` 분기를 쓰는 사람이 있다면 이 구분이 의미 있다.

> **에러 처리 전체 패턴과 에러 클래스 계층 예시는 `toby-ai/ts-cli-walkthrough` repo의 `step-05` 커밋에 있다.**

---

## Step 6. 단일 바이너리 빌드 — "언제 의미 있나"

### Bun compile vs Deno compile vs pkg

세 선택지를 비교해보자.

| 기준 | Bun compile | Deno compile | pkg (역사적) |
|------|-------------|--------------|-------------|
| 빌드 명령 | `bun build --compile` | `deno compile` | `npx pkg` |
| 크로스 컴파일 | 내장 (`--target` 옵션) | 내장 (`--target` 옵션) | 내장 |
| 바이너리 크기 | 40~80 MB | 60~100 MB | 수백 MB |
| 시작 시간 | ~10ms 내외 | ~15ms 내외 | 느림 |
| Node.js 의존성 | 없음 | 없음 | 없음 |
| 유지보수 상태 | 활발 | 활발 | 사실상 종료 |

pkg는 역사적 언급이다. 바이너리가 수백 MB에 달하고 2024년 기준 유지보수가 멈춘 상태다. 새 프로젝트에서 쓸 이유가 없다.

### Bun compile 실전

```bash
# 현재 플랫폼용 바이너리
bun build --compile ./src/cli.ts --outfile my-cli

# 크로스 컴파일 — macOS에서 Linux 바이너리 빌드
bun build --compile --target=bun-linux-x64 ./src/cli.ts --outfile my-cli-linux

# Apple Silicon
bun build --compile --target=bun-darwin-arm64 ./src/cli.ts --outfile my-cli-macos-arm64

# Windows
bun build --compile --target=bun-windows-x64 ./src/cli.ts --outfile my-cli-windows.exe
```

Java 베테랑이 picocli + GraalVM native-image 조합을 써봤다면 reflect-config.json 씨름이 기억날 것이다. Bun compile에는 그 씨름이 없다. "이렇게 쉬운 거야?"라는 반응이 나오는 순간이다.

### 언제 단일 바이너리가 의미 있나

단일 바이너리가 항상 정답은 아니다. 선택 기준을 정리해보자.

**단일 바이너리가 맞는 경우:**
- 최종 사용자가 개발자가 아닌 경우 (Node.js 없어도 실행)
- CI/CD 파이프라인에서 런타임 설치 없이 즉시 실행해야 할 때
- 시작 시간이 중요한 자동화 도구
- Homebrew나 GitHub Releases로 배포할 때

**npm publish가 맞는 경우:**
- 주요 사용자가 Node.js 또는 Bun이 있는 개발자
- `npx`로 바로 쓸 수 있으면 충분
- 패키지가 자주 업데이트되어 자동 최신 버전 이점이 큰 경우

사내 배포를 포함한 대부분의 CLI 도구는 npm publish로 충분하다. 단일 바이너리가 *추가 가치*를 주는 경우에만 선택하는 편이 낫다.

> **GitHub Actions 크로스 컴파일 워크플로 전체 버전은 `toby-ai/ts-cli-walkthrough` repo의 `step-06` 커밋에 있다.**

---

## Step 7. 배포 — 채널 선택의 결정 지도

### npm publish — 가장 기본적인 경로

npm으로 배포하면 `npx my-cli`가 바로 동작한다. `package.json`에 두 가지를 반드시 챙기자.

```json
{
  "name": "my-cli",
  "version": "1.0.0",
  "bin": {
    "my-cli": "./dist/cli.js"
  },
  "files": ["dist"],
  "scripts": {
    "build": "bun build ./src/cli.ts --outdir dist",
    "prepublishOnly": "bun run build"
  }
}
```

`bin` 필드가 커맨드 이름과 실행 파일을 연결한다. `dist/cli.js` 첫 줄에 shebang이 있어야 한다.

```javascript
#!/usr/bin/env node
```

Bun으로 빌드했더라도 npm을 통해 배포되는 경우 Node.js 환경에서 실행될 수 있다. `#!/usr/bin/env bun`은 Bun이 없는 환경에서 실패한다. Bun 전용 배포가 아니라면 Node.js 호환 shebang을 쓰는 편이 낫다.

**스코프드 패키지 이름** (`@myorg/my-cli`)은 npm 계정이 없어도 내부 레지스트리(Verdaccio, GitHub Packages, npm private)로 배포할 수 있다. 회사 내부 도구라면 스코프드 패키지가 적절하다.

### GitHub Releases — 단일 바이너리 배포

GitHub Actions 워크플로를 한 단락으로 정리하면 다음과 같다. 태그를 푸시하면 자동으로 세 플랫폼 바이너리가 Release에 첨부된다.

```yaml
# .github/workflows/release.yml
on:
  push:
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: bun-linux-x64
            artifact: my-cli-linux-x64
          - os: macos-latest
            target: bun-darwin-arm64
            artifact: my-cli-macos-arm64
          - os: windows-latest
            target: bun-windows-x64
            artifact: my-cli-windows-x64.exe
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun build --compile --target=${{ matrix.target }} src/cli.ts --outfile ${{ matrix.artifact }}
      - uses: softprops/action-gh-release@v1
        with:
          files: ${{ matrix.artifact }}
```

Release에 첨부된 바이너리를 사용자가 직접 다운로드해 실행한다. `chmod +x`가 필요한 경우도 있다. 이 불편을 줄이려면 Homebrew tap을 함께 제공하는 편이 낫다.

### Homebrew tap — macOS 사용자를 위해

Homebrew는 macOS 개발자에게 가장 자연스러운 설치 방법이다. tap 레포를 만들고 formula를 작성하면 `brew install myorg/tap/my-cli`가 가능해진다.

```ruby
# Formula/my-cli.rb
class MyCli < Formula
  desc "사내 PR 조회 도구"
  homepage "https://github.com/myorg/my-cli"
  version "1.0.0"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/myorg/my-cli/releases/download/v1.0.0/my-cli-macos-arm64"
      sha256 "..." # 빌드 결과물의 sha256
    else
      url "https://github.com/myorg/my-cli/releases/download/v1.0.0/my-cli-macos-x64"
      sha256 "..."
    end
  end

  def install
    bin.install Dir["my-cli*"].first => "my-cli"
  end
end
```

`sha256`은 빌드 후 `shasum -a 256 my-cli-macos-arm64`로 구한다. 버전이 올라갈 때마다 formula도 업데이트해야 한다는 것이 번거롭다. GitHub Actions에서 formula를 자동으로 업데이트하는 워크플로를 추가하면 이 번거로움을 줄일 수 있다.

### 배포 채널 결정 표

어느 채널이 언제 맞는지를 정리하면 다음과 같다.

| 상황 | 권장 채널 |
|------|-----------|
| 팀 내부, 개발자만 사용, Node.js 있음 | npm private 레지스트리 또는 npm publish (스코프드) |
| 조직 전체, 비개발자 포함, 설치 간편해야 함 | GitHub Releases (단일 바이너리) + Homebrew tap |
| 오픈소스, 외부 사용자, 생태계 통합 | npm publish (공개) + GitHub Releases |
| CI/CD 파이프라인 내 도구 | GitHub Releases 바이너리 + Actions에서 직접 다운로드 |

하나를 고르는 것보다 조합이 현실적이다. npm publish로 개발자 사용자를 커버하고, GitHub Releases로 비개발자와 파이프라인을 커버하는 식이다.

> **formula 자동 업데이트 워크플로, npm publish 설정 전체, 내부 레지스트리 설정 예시는 `toby-ai/ts-cli-walkthrough` repo의 `step-07` 커밋에 있다.**

---

## 마무리 — 결정의 흐름을 다시 한 번

일곱 단계를 돌아보면, 각 단계가 하나의 질문에 답한 것이었다.

1. **셋업**: Node.js인가 Bun인가 → 도구 통합의 단순함이 기준
2. **인자 정의**: commander인가 oclif인가 → 도구의 규모 감각이 기준
3. **HTTP 호출**: fetch인가 axios인가 ky인가 → 재시도·에러 처리 필요 여부가 기준
4. **출력**: 사람용 출력인가 기계용 출력인가 → TTY 감지와 `--json` 플래그로 분기
5. **에러 처리**: `as`인가 타입 가드인가 → 컴파일러를 침묵시키지 않는 방향이 기준
6. **빌드**: npm인가 단일 바이너리인가 → 최종 사용자 환경이 기준
7. **배포**: 어느 채널인가 → 사용자 유형과 설치 편의가 기준

각 결정에는 옳고 그름이 없다. 팀의 규모, 도구의 목적, 사용자의 환경에 따라 다른 답이 나온다. 중요한 것은 결정의 근거를 팀이 공유하는 것이다. 반년 뒤에 새 팀원이 합류해서 "왜 이걸 썼죠?"라는 질문을 했을 때 근거를 설명할 수 있으면 충분하다.

### 본문과의 cross-reference

이 워크쓰루는 본문 곳곳과 연결되어 있다.

- **1장** — tsconfig의 각 옵션이 왜 존재하는지, TS가 JS 위에 어떤 층을 더하는지 (Step 1 배경)
- **5장** — 타입 좁히기, `z.infer`, `as`의 윤리 (Step 2·3·5 핵심 도구)
- **6장** — zod로 외부 경계 검증, Result 패턴 (Step 3 boundary validation)
- **8장** — ESM, `moduleResolution: NodeNext`의 의미 (Step 1 tsconfig)
- **10장** — CLI 생태계 전체 지형도 (이 워크쓰루의 출발점)

각 장을 다시 펼칠 때 이 워크쓰루의 어느 단계와 연결되는지 생각해보면 개념이 한 번 더 자리를 잡는다.

### "GitHub repo에서 더 깊이 가려면"

`toby-ai/ts-cli-walkthrough` repo에는 이 부록에서 다루지 못한 것들이 있다.

- **테스트**: 커맨드 핸들러 단위 테스트, API 클라이언트 모킹 (14장과 연결)
- **설정 파일**: `~/.config/my-cli/config.json` 읽고 쓰기, `xdg-basedir` 패턴
- **업데이트 알림**: 새 버전이 있을 때 사용자에게 알리는 `update-notifier` 패턴
- **Shell completion**: commander에서 bash/zsh/fish completion 파일 생성
- **통합 테스트**: 실제 바이너리를 실행해 stdout/stderr/exit code를 검증하는 패턴
- **Deno 버전**: 동일한 CLI의 Deno compile + 권한 모델 버전

repo의 각 브랜치와 커밋 메시지가 이 부록의 단계 번호와 매핑되어 있다. `step-01`부터 순서대로 따라가거나, 관심 있는 단계만 골라서 볼 수 있다.

CLI 하나를 끝까지 짓는 과정에서 언어의 이쪽저쪽이 연결된다. 타입이 어떻게 흐르는지, 에러가 어디서 막히는지, 배포가 어떻게 이루어지는지. 책을 덮고 나서 뭔가 하나를 직접 만들어보고 싶다면 — CLI가 가장 진입 장벽이 낮고, 결과가 가장 즉각적이다. 망설이지 말고 짓자.


---

# 부록 D. 한국 개발자 함정 사전 — 12개 인덱스

실무에서 이런 순간이 온다. 분명히 타입을 붙였는데 런타임에서 예외가 터진다. IDE는 아무 경고도 안 했는데 빌드가 깨진다. 동료 코드를 리뷰하다가 뭔가 찜찜하지만 정확히 뭐가 문제인지 설명하기 어렵다. 그럴 때 이 부록을 꺼내 들자.

## 이 부록의 자리

본문 15개 챕터에는 각 주제가 호명되는 자리마다 "🚧 함정 박스"를 두었다. 12개 함정 각각의 깊이 있는 풀이 — 왜 이렇게 설계됐는지, 어떤 상황에서 발화하는지, 처방이 어떻게 작동하는지 — 는 그 자리에서 충분히 다뤘다.

부록 D는 다른 역할을 한다. *증상이 먼저 보일 때* 빠르게 함정 이름을 찾고, 본문의 깊이 풀이로 곧장 건너갈 수 있는 **빠른 참조 카드**다.

**사용법**: 실무에서 이상한 낌새가 느껴지면 아래 12개 증상을 훑어보자. 비슷한 증상을 찾으면 "더 깊이" 화살표를 따라가 본문 함정 박스로 점프한다. 본문을 읽을 시간이 없을 때는 "핵심 처방" 한 단락만 읽고 일단 적용해도 좋다.

---

## D.1. 묵시적 `any`와 strict 모드

**증상**: 타입을 붙였다고 생각했는데 IDE 자동완성이 작동하지 않거나, `any`를 쓰지 않았음에도 타입 에러가 런타임까지 흘러내려온다.

**원인**: TypeScript의 기본 설정은 `strict: false`다. 이 모드에서는 함수 매개변수에 타입을 생략하면 `any`로 추론하고, `strictNullChecks`도 꺼져 있어 `null`과 `undefined`가 모든 타입에 섞여 들어간다. Java에서 타입이 붙어 있으면 컴파일러가 책임지는 데 익숙한 개발자는 "TS는 왜 이러나"라는 생각이 든다. 사실 이것은 TS가 나쁜 게 아니라 설정이 느슨한 것이다. 기존 JS 코드를 점진적으로 TS로 올릴 때 충격을 줄이기 위해 의도적으로 느슨하게 설계된 기본값이다.

**핵심 처방**: 새 프로젝트라면 `tsconfig.json`에 `"strict": true`를 첫 번째 줄에 넣는 편이 낫다. 이미 운영 중인 프로젝트라면 `"strict": true`를 넣은 뒤 `// @ts-nocheck`를 파일 단위로 붙여 가며 점진적으로 정리해나가는 방식이 현실적이다. 묵시적 `any`는 코드베이스 전체에 조용히 퍼지기 전에 `"noImplicitAny": true` 하나만으로도 잡을 수 있다.

**더 깊이**: → 3장 "🚧 함정 박스: 묵시적 any와 strict 모드" / 부록 B의 `strict` 플래그 계열 항목

---

## D.2. 구조적 타입의 헐렁함

**증상**: `UserId`와 `OrderId`를 각각 `string`으로 선언했는데, 함수에 `UserId` 자리에 `OrderId`를 넣어도 컴파일러가 아무 말도 하지 않는다. 도메인 경계가 타입으로 보호되지 않는 느낌이라 찜찜하다.

**원인**: TypeScript는 구조적 타입 시스템(structural typing)이다. 두 타입이 같은 *모양*이면 호환된다. `type UserId = string`과 `type OrderId = string`은 실제로 둘 다 `string`이므로 서로 바꿔 써도 컴파일러 입장에서는 문제가 없다. Java의 명목 타입(nominal typing) — 이름이 달라야 다른 타입 — 에서 온 개발자에게는 직관과 어긋나는 동작이다. 대규모 도메인 코드에서 이 헐렁함이 쌓이면 타입이 형식적 장식이 되고 만다.

**핵심 처방**: **branded type** 패턴을 사용하는 편이 낫다. `type UserId = string & { readonly _brand: unique symbol }` 형태로 선언하면 구조적으로 다른 타입이 되어 서로 할당이 차단된다. 토스·Effect-ts 등이 이 패턴을 표준화했다. `unique symbol`을 쓰면 같은 파일 안에서도 두 branded type은 절대 같아지지 않는다.

**더 깊이**: → 6장 "🚧 함정 박스: 구조적 타입의 헐렁함 → branded type" / §2.2 구조적 타입 vs 명목 타입

---

## D.3. `this`가 사라진다

**증상**: 클래스 메서드를 콜백으로 넘겼더니 `this`가 `undefined`가 되어 있다. 메서드 안에서 `this.someField`를 접근하면 런타임 에러가 터진다.

**원인**: JavaScript에서 `this`는 호출 방식에 따라 결정된다. 메서드를 `obj.method()` 식으로 직접 호출하면 `this`가 `obj`가 되지만, 콜백으로 넘기면 — `setTimeout(obj.method, 0)`, `addEventListener('click', obj.handler)`, 배열의 `map(obj.process)` — 메서드가 "분리"된다. 분리된 함수는 `this`를 잃는다. Java의 인스턴스 메서드 참조는 항상 객체와 함께 묶여 있어서 이런 일이 없다. 이 차이를 모르면 나중에야 찾기 어려운 버그를 만들게 된다.

**핵심 처방**: 화살표 함수로 메서드를 정의하는 방식(`handleClick = () => { ... }`)이 가장 간단하다. 화살표 함수는 `this`를 정의 시점의 렉시컬 컨텍스트로 고정한다. 또는 콜백 전달 시 `obj.method.bind(obj)`를 쓰거나, 래퍼 화살표 함수 `() => obj.method()`로 감싸는 방법도 있다. TypeScript 4.0 이후로는 `this` 매개변수를 명시적으로 선언해 컴파일러가 `this` 바인딩 오류를 잡아주도록 할 수 있다.

**더 깊이**: → 2장 "🚧 함정 박스: `this`가 사라진다" / §2.3 비동기 모델

---

## D.4. 비동기 에러는 어디로 가는가

**증상**: `try/catch`로 감쌌는데도 예외가 잡히지 않는다. 또는 `Promise`가 reject됐는데 콘솔에 아무것도 안 보이다가 나중에 프로세스가 죽는다.

**원인**: `async/await`과 일반 콜백 안에서의 예외는 전파 경로가 다르다. `async` 함수 안에서 `throw`된 에러는 반환된 `Promise`가 reject되는 방식으로 전파되므로, 그 `Promise`에 `.catch()`가 없거나 `await`을 빠뜨리면 에러가 조용히 사라진다. `unhandledRejection` 이벤트로 Node가 경고하거나(Node 버전에 따라 프로세스 종료), 아무 소리도 없이 기능이 멈춰버리는 두 가지 나쁜 결과 중 하나가 온다. Java의 `@ControllerAdvice`처럼 전역 예외 핸들러가 기본 제공되지 않는다는 점이 이 문제를 더 위험하게 만든다.

**핵심 처방**: `await`을 붙이지 않은 `Promise` 호출이 코드베이스 어딘가에 있지 않은지 늘 경계하는 편이 낫다. ESLint의 `@typescript-eslint/no-floating-promises` 규칙이 이를 정적으로 잡아준다. 전역 에러 핸들러로는 `process.on('unhandledRejection', handler)`를 항상 등록해두는 습관이 중요하다. NestJS를 쓴다면 `ExceptionFilter`가 이 역할을 한다.

**더 깊이**: → 7장 "🚧 함정 박스: 비동기 에러는 어디로 가는가" / §2.3 비동기 모델

---

## D.5. CJS/ESM 혼란

**증상**: `require is not defined`, `Cannot use import statement in a module`, 또는 A 패키지는 잘 되는데 B 패키지를 추가하자마자 모듈 관련 에러가 터진다.

**원인**: JavaScript에는 모듈 시스템이 두 개다. CommonJS(`require`/`module.exports`)와 ECMAScript Modules(`import`/`export`). `package.json`의 `"type": "module"` 필드 한 줄이 파일 전체의 동작을 뒤바꾼다. ESM에서 CJS 패키지를 가져오는 것은 가능하지만, CJS 환경에서 ESM 전용 패키지를 `require`로 가져오는 것은 막혀 있다. 문제는 npm 생태계의 많은 패키지가 최근 ESM 전용으로 전환했다는 점이다. `chalk`, `node-fetch`, `got` 등이 주요 사례다. 이 전환은 난데없이 기존 CJS 프로젝트를 깨뜨린다.

**핵심 처방**: 새 프로젝트라면 처음부터 ESM으로 시작하는 편이 낫다. `package.json`에 `"type": "module"`을 선언하고 `tsconfig.json`에서 `"module": "NodeNext"`, `"moduleResolution": "NodeNext"`로 맞추면 일관된 ESM 환경이 된다. 기존 CJS 프로젝트에서 ESM 전용 패키지를 써야 한다면 `import()`를 동적으로 호출하는 방법이 있지만, 코드가 복잡해져 난감하다.

**더 깊이**: → 8장 "🚧 함정 박스 ①: CJS/ESM 혼란" / §2.4 모듈/패키지

---

## D.6. tsconfig 지옥

**증상**: `tsc` 빌드는 성공하는데 Jest에서 에러가 난다. IDE에서는 빨간 줄이 없는데 CI 빌드가 실패한다. `tsconfig.json` 파일이 여러 개라 어떤 파일이 어떤 상황에 쓰이는지 모르겠다.

**원인**: TypeScript 프로젝트는 보통 목적에 따라 `tsconfig.json`을 여러 개로 나눈다. 빌드용, 테스트용, IDE용이 서로 다른 설정을 가지는 게 합법적이다. 그런데 이 설정들이 일관성 없이 뒤섞이면 "내 로컬에서는 되는데 CI에서는 안 돼요" 상황이 온다. `paths`, `baseUrl`, `rootDir`, `outDir`이 서로 맞지 않거나, `include`/`exclude` 범위가 의도와 다를 때 특히 그렇다. tsconfig 옵션은 100개가 넘어서 처음 보는 사람은 어디서부터 시작해야 할지 막막하다.

**핵심 처방**: Matt Pocock의 "tsconfig Cheat Sheet"를 기준점으로 삼는 편이 낫다. 가장 중요한 옵션은 `strict`, `module`, `moduleResolution`, `target`, `outDir`, `rootDir` 여섯 가지다. 나머지는 하나씩 필요할 때 추가하자. 프로젝트 루트에 `tsconfig.base.json`을 두고 목적별 파일이 이를 `extends`하는 패턴이 혼란을 가장 많이 줄여준다. 부록 B에 전체 옵션 사전이 있다.

**더 깊이**: → 8장 "🚧 함정 박스 ②: tsconfig 지옥" / 부록 B tsconfig 옵션 사전

---

## D.7. `Date` 객체와 시간대

**증상**: 서버에서 날짜를 제대로 저장했는데 한국 사용자에게 보이는 날짜가 하루 앞뒤로 어긋난다. 또는 `new Date('2025-01-01')`이 환경마다 다른 시각을 가리킨다.

**원인**: JavaScript `Date` 객체는 내부적으로 UTC 타임스탬프(Unix epoch milliseconds)를 저장하지만, 출력과 파싱은 로컬 시스템 시간대에 따라 달라진다. `new Date('2025-01-01')`처럼 날짜만 있는 ISO 8601 문자열은 UTC 자정으로 파싱되는데, 한국 서버(KST = UTC+9)에서 이를 로컬 시각으로 출력하면 1월 1일 오전 9시가 된다. 그런데 일자만 출력하면 맞지만, 클라이언트 브라우저가 다른 시간대에 있으면 또 달라진다. 이 불일치가 예약 시스템, 정산 시스템, 이벤트 스케줄러에서 매우 골치 아픈 버그를 만든다.

**핵심 처방**: 날짜·시각을 다루는 모든 로직에서 시간대를 명시적으로 처리하는 편이 낫다. 외부 입력은 항상 UTC로 받아 저장하고, 출력할 때만 KST로 변환한다. 라이브러리는 `date-fns-tz` 또는 `luxon`을 사용하면 시간대 처리가 명확해진다. 2024년 이후 주요 브라우저와 Node.js 22+에서는 `Temporal` API가 표준으로 들어오고 있어 이 문제가 언어 수준에서 해결되는 방향이다.

**더 깊이**: → 15장 "한국 현장의 함정 큰 카테고리 — 타입 통제" / §5.6 표준 학습 자원

---

## D.8. `as` 단언의 남용

**증상**: 빌드는 통과하는데 런타임에서 `undefined is not a function` 같은 에러가 난다. 코드에 `as` 키워드가 많이 눈에 띈다.

**원인**: `as` 타입 단언은 컴파일러에게 "내가 책임질 테니 이 값을 이 타입으로 봐"라고 선언하는 것이다. 컴파일러는 반박하지 않는다. 따라서 실제 값이 단언한 타입과 다를 때 에러를 잡아주지 않는다. 빌드는 녹색이지만 런타임은 폭발하는 상황이 여기서 온다. 특히 외부 API 응답, JSON 파싱 결과, 레거시 코드 연결부에서 `as` 단언이 "일단 돌아가게 하는" 임시방편으로 남용되는 경향이 있다. 찜찜하지만 바쁠 때 눈 감고 쓰는 게 `as`다.

**핵심 처방**: 경계 지점 — API 응답, 환경 변수, 사용자 입력 — 에서는 `as` 대신 `zod` 같은 런타임 검증 라이브러리로 데이터를 파싱하는 편이 낫다. `z.parse()`는 스키마와 맞지 않으면 즉시 예외를 던지므로 거짓된 안도감을 주지 않는다. 내부 로직에서 타입이 이미 보장된 값에 한해 `as`를 쓰는 것은 합리적이지만, 그 경우에도 왜 단언이 안전한지 주석으로 남기는 습관이 중요하다. `as`를 쓰면 그 순간 타입 시스템의 책임이 내 손으로 넘어온다는 사실을 기억해두자.

**더 깊이**: → 5장 "`as`의 윤리" 절 / §4 논쟁 D: 타입 단언 vs 타입 가드 vs 런타임 검증

---

## D.9. 데코레이터 두 종류의 혼동

**증상**: NestJS 코드를 따라했는데 "Decorators are not valid here" 에러가 난다. 또는 새 TS 버전에서 `experimentalDecorators` 경고가 뜬다. 인터넷 예제들이 서로 다른 문법을 쓰고 있어 어느 것이 맞는지 모르겠다.

**원인**: TypeScript의 데코레이터는 현재 *두 종류*가 공존한다. 하나는 `experimentalDecorators: true`로 켜는 **레거시 데코레이터**로, NestJS·TypeORM·class-validator가 이 위에서 동작한다. 다른 하나는 TypeScript 5.0부터 기본 지원하는 **TC39 Stage 3 신규 표준 데코레이터**다. 두 데코레이터는 문법이 비슷해 보이지만 동작 방식이 다르고, 특히 `reflect-metadata`를 이용한 타입 메타데이터는 신규 표준에 포함되어 있지 않다. 이 때문에 NestJS는 당분간 레거시 모드에 머물 수밖에 없고, 새 TS로 마이그레이션하려는 프로젝트에서 충돌이 발생한다.

**핵심 처방**: NestJS·TypeORM 등 레거시 데코레이터 기반 프레임워크를 쓰는 프로젝트는 `tsconfig.json`에 `"experimentalDecorators": true`를 유지하는 편이 현실적이다. 신규 TS 5.x 데코레이터를 쓰는 라이브러리와 레거시 기반 프레임워크를 같은 프로젝트에서 섞지 않도록 주의해야 한다. NestJS 공식 로드맵을 주기적으로 확인해 신규 표준 마이그레이션 시점을 파악해두는 것도 중요하다.

**더 깊이**: → 13장 "🚧 함정 박스: 데코레이터 두 종류 혼동" / §2.7 DI/프레임워크 철학 / §4 논쟁 C: 데코레이터 표준화

---

## D.10. 마이그레이션 중 `any` 폭증

**증상**: JS에서 TS로 마이그레이션하는 과정에서 `any` 타입이 코드베이스 전체로 급속도로 퍼진다. 타입을 붙였는데 오히려 `any`가 더 많아진 느낌이 든다.

**원인**: 대규모 JS 코드베이스를 TS로 올릴 때 흔히 쓰는 전략이 "일단 `.ts`로 바꾸고 `as any`로 에러를 막은 다음 나중에 정리하겠다"는 것이다. 문제는 `any`가 전염성이 강하다는 점이다. `any` 타입의 값을 다른 변수에 할당하거나 함수에 넘기면, 그 결과 타입도 `any`가 된다. 이 과정이 반복되면 수십 개의 파일에 `any`가 퍼져 나간다. Kristensen·Møller(2017) 연구에 따르면 JS→TS 자동 추론이 가능한 비율은 약 60%다. 나머지 40%는 개발자가 직접 타입을 붙여야 하는데, 그 자리에 `any`로 막아두면 마이그레이션이 사실상 완료되지 않는 것이다.

**핵심 처방**: `strict: true`와 `noImplicitAny: true`를 켠 상태에서 파일 단위로 마이그레이션하는 방식이 `any` 폭증을 막는 가장 효과적인 방법이다. 한 파일을 올릴 때 `any`를 쓰지 않는 것을 원칙으로 삼고, 정말 추론이 어려운 부분만 `// @ts-ignore`나 `unknown`을 임시로 쓰며 그 이유를 주석으로 남기는 편이 낫다. ESLint의 `@typescript-eslint/no-explicit-any` 규칙을 경고로 켜두면 폭증을 시각적으로 추적할 수 있다.

**더 깊이**: → 9장 "🚧 함정 박스: 마이그레이션 중 `any` 폭증 통제" / §5.3 any 통제의 정치학

---

## D.11. 프론트 reactivity 모델 혼동

**증상**: React 프로젝트에서 상태가 변했는데 화면이 업데이트 안 된다. 또는 "왜 re-render가 이렇게 많이 일어나지"라는 상황에서 Vue나 Svelte로 바꿨더니 동작 방식이 완전히 달라 혼란스럽다.

**원인**: 프론트엔드 프레임워크마다 reactivity — 상태 변화를 화면에 반영하는 메커니즘 — 의 모델이 다르다. React는 "불변 상태 + 명시적 `setState` + 가상 DOM diffing"이고, Vue 3는 "Proxy 기반 자동 추적"이며, Svelte 5는 "컴파일 타임 signal(runes)"이고, SolidJS는 "런타임 signal + 가상 DOM 없음"이다. 한 모델에 익숙해지면 다른 모델의 코드를 볼 때 같은 TS 문법인데 동작이 다르다는 사실에 충격을 받는다. 특히 React의 불변성 원칙(배열을 직접 mutate하면 안 됨)을 모르고 Vue 스타일로 직접 수정하면 React에서 화면이 멈춘다.

**핵심 처방**: 프레임워크를 바꿀 때는 "TypeScript 코드 작성법"이 아니라 "이 프레임워크의 reactivity 모델"을 먼저 배우는 편이 낫다. 한국 시장에서는 React가 압도적이므로 React의 불변 상태 + Hooks 모델을 기준으로 익히고, 다른 프레임워크는 비교 관점에서 배우는 전략이 효율적이다. 12장의 각 프레임워크 비교 절에서 reactivity 모델 차이를 명시적으로 정리했으니 함께 읽어보자.

**더 깊이**: → 12장 "🚧 함정 박스: 프론트 reactivity 모델이 프레임워크마다 다름" / §3.4 웹 — 프론트엔드 프레임워크

---

## D.12. monorepo IDE 폭주

**증상**: 코드를 저장할 때마다 VS Code가 버벅인다. TypeScript 언어 서버가 CPU를 100% 쓰며 돌아가 편집이 불편하다. 프로젝트가 커질수록 점점 나빠진다.

**원인**: monorepo에서 여러 패키지가 하나의 TypeScript 언어 서버 인스턴스에 의해 분석될 때 발생하는 문제다. TypeScript 언어 서버는 프로젝트 전체를 메모리에 올려두고 변경 시마다 재분석한다. 수백만 줄의 코드가 있는 monorepo에서 이 방식은 메모리와 CPU 사용이 폭발적으로 늘어난다. `tsconfig.references`와 project references를 사용하지 않으면 IDE가 모든 패키지를 단일 프로젝트로 보기 때문이다. 카카오·당근 등 국내 대형 monorepo 사례에서 이 문제는 반드시 나온다.

**핵심 처방**: `tsconfig.references`를 사용해 패키지 간 의존성을 명시하는 것이 핵심이다. 각 패키지에 자체 `tsconfig.json`을 두고, 루트 `tsconfig.json`의 `references` 배열에 등록하면 IDE는 변경된 패키지만 재분석한다. VS Code의 경우 "TypeScript: Select TypeScript Version"에서 작업공간 버전을 명시적으로 선택해두는 것도 도움이 된다. Turborepo나 Nx를 쓴다면 각 도구의 TS 통합 가이드를 함께 따르는 편이 낫다.

**더 깊이**: → 8장 "🚧 함정 박스 ③: monorepo IDE 폭주" / §4 논쟁 E: monorepo 적정 규모

---

## 마무리 — 함정은 도구를 알게 만드는 자리

12개 함정을 쭉 읽다 보면 공통된 패턴이 보인다. 대부분은 "TypeScript가 나쁘다"가 아니라 "TypeScript가 의도적으로 느슨하게 설계된 부분"에서 비롯된다. strict 모드를 기본값으로 두지 않은 것, `any`를 허용하는 것, 구조적 타입으로 경계를 열어둔 것 — 이 모든 선택은 기존 JS 코드와의 점진적 통합을 위한 현실적 절충이었다. 그 절충의 대가가 이 12개 함정이다.

함정에 빠져본 경험은 도구를 피상적으로 아는 것과 실제로 이해하는 것 사이의 거리를 좁힌다. 에러 메시지를 처음 봤을 때의 당혹감, 원인을 찾아가는 과정, 처방이 왜 작동하는지 깨닫는 순간 — 그 순간들이 TypeScript를 진짜로 배우는 경로다. 함정을 피하는 것이 목표가 아니라, 함정을 통해 도구의 본성을 아는 것이 목표다.

15장의 "AI 시대의 TS" 절에서는 한 가지 더 덧붙였다. AI가 짠 코드에서 이 12개 함정이 얼마나 자주 나타나는지, 그리고 사람이 리뷰할 때 어떤 함정을 특별히 주목해야 하는지다. LLM은 문법적으로 완벽한 TS 코드를 쓰지만, `as` 단언을 남발하거나 `strict` 설정을 확인하지 않고 예제를 제시하는 경우가 많다. 이 부록의 12개 체크리스트는 AI 보조 코딩 시대에도 사람이 놓치지 말아야 할 관문이다. 15장으로 넘어가 그 이야기를 마저 읽어보자.


---

## 책을 닫으며

이 책을 끝까지 읽었다면, 당신은 TypeScript를 단순히 "JavaScript에 타입 붙인 것"이라고 보는 시선을 이미 넘어섰다. 구조적 타이핑이 왜 그렇게 설계됐는지, 타입 좁히기가 어떻게 컴파일러와 대화하는 방식인지, 비동기 모델이 JVM 스레드 모델과 어떻게 다르게 생겼는지 — 이 질문들이 이제는 낯설지 않을 것이다.

하지만 책은 여정의 시작일 뿐이다. TypeScript는 살아있는 언어다. 매년 새 버전이 나오고, 커뮤니티가 관용구를 다듬고, 도구가 진화한다. 이 책이 닦아놓은 기초 위에서 계속 쌓아가길 바란다.

### 다음 걸음

읽고 나서 바로 써봐야 배운다. 다음 중 하나를 골라 시작해보자.

- **직접 마이그레이션:** 지금 팀의 Express 프로젝트 하나를 9장 로드맵대로 TS로 옮겨본다. 오류 메시지가 선생이다.
- **타입 체조 연습:** [type-challenges](https://github.com/type-challenges/type-challenges) 저장소의 `easy` 문제 10개를 풀어본다. 5장에서 배운 조건부 타입이 실전 수준으로 굳어진다.
- **생태계 탐색:** NestJS를 Kotlin/Spring 대비로 읽어보자. 데코레이터와 DI 컨테이너가 어떻게 Java 생태계의 관용구를 TS로 이식했는지 보인다.
- **공식 문서 병행:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)을 이 책과 교차해서 읽으면, 공식 설명이 훨씬 빠르게 흡수된다.

### 감사 인사

Java와 TypeScript를 함께 고민하는 모든 개발자에게. 두 세계를 오가는 불편함이 곧 깊이가 된다.

---

*왜 TypeScript는 이렇게 생겼는가*
버전 1.0.0 | 2026-05-04
저자: Toby-AI

