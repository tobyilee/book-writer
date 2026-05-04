# 왜 TypeScript는 이렇게 생겼는가

> Java/Kotlin 베테랑이 "왜 이렇게 만들었는가"를 손에 쥐고 나면, TypeScript는 낯선 언어가 아니라 자기 도구가 된다.

- **저자:** Toby-AI
- **버전:** v1.0.0
- **발행일:** 2026-05-04
- **언어:** 한국어
- **분량:** 약 15장 + 4부록 / 본문 약 938,520 자

---

## 이 책은 무엇인가

월요일 아침, 10년 넘게 Spring으로 백엔드를 짜온 개발자가 처음으로 TypeScript 코드베이스를 열었다. `class`도 있고 `interface`도 있는데 `implements`가 없다. `pom.xml` 대신 `package.json`이 있고, 그 옆에 `tsconfig.json`, `vite.config.ts`, `.eslintrc.cjs`가 함께 있다. 빌드 책임이 한 화면에서 다섯 군데로 흩어져 있다. "며칠이면 적응하지"라고 생각했지만, 문법을 익히는 것과 언어가 *왜 그렇게 생겼는가*를 이해하는 것은 전혀 다른 일이다.

이 책은 그 *왜*에 답한다. TypeScript가 Java나 Kotlin과 다르게 생긴 이유는 자란 토양이 정반대이기 때문이다. 구조적 타이핑이 명목 타이핑보다 도메인 안전성이 헐거운 이유, 점진적 타입 시스템이 `any`라는 탈출구를 필요로 하는 이유, 컴파일이 끝나면 타입이 통째로 사라지는 이유 — 이 질문들에 논문과 설계 문서에 근거한 답을 내놓는다.

단순한 문법 소개서가 아니다. 타입 시스템의 원리에서 시작해, 실제 한국 현장에서 쓰이는 CLI·데스크톱·웹 프론트엔드·웹 백엔드·풀스택 영역까지 TypeScript가 살아가는 전 영역을 걷는다. Java/Kotlin 백엔드 경력이 깊을수록 이 책이 더 유용해지도록 설계되었다. 각 챕터마다 Java/Kotlin 코드와 TypeScript 코드를 나란히 놓고, 비슷해 보이는 자리에서 무엇이 다른지, 그 이유가 무엇인지를 솔직하게 말한다.

이 책은 언어 학습서와 생태계 전환 가이드의 하이브리드다. 읽고 나면 두 언어 생태계를 자유롭게 오가는 개발자가 되어 있을 것이다.

---

## 누구를 위한 책인가

**이 책의 정중앙 독자는 Java/Spring 또는 Kotlin을 수년 이상 써온 백엔드·풀스택 개발자로서, TypeScript는 처음이거나 표면적으로만 써본 사람이다.**

진입 상태는 이렇다. 정적 타입과 객체지향은 깊이 익숙하다. IDE가 빨간 줄을 그어주면 고칠 줄 안다. DI, 인터페이스, sealed class, checked exception이 자연스럽다. 그런데 TypeScript는 왜 `implements` 없이도 타입이 맞는지 직관적으로 이해가 안 된다. `any`가 왜 있는지 모르겠다. 빌드 도구가 왜 이렇게 많은지 막막하다.

출구 상태는 이렇다. TypeScript가 *점진적·구조적·의도적으로 unsound한 컴파일타임 도구*라는 것을 손에 쥔다. 제네릭·conditional·`infer`·매핑·템플릿 리터럴 타입으로 도메인의 결을 표현할 수 있다. 기존 JS 코드베이스를 점진적으로 TS로 옮길 수 있다. CLI·데스크톱·웹 어디서든 TypeScript로 작업할 수 있다. AI 시대에 사람이 타입 시스템을 검토해야 하는 이유를 안다.

TypeScript 문법을 이미 아는 사람에게는 *왜 그렇게 생겼는가*의 답이 새롭게 보일 것이다. 이제 막 시작하는 사람에게는 처음부터 올바른 멘탈 모델을 잡을 기회가 된다.

---

## 무엇을 얻게 되는가

- **TypeScript 언어의 깊이:** 점진적 타입 시스템이 왜 `any`라는 탈출구를 필요로 하는지, 구조적 타입이 왜 명목 타입보다 도메인 안전성이 헐거운지, 의도된 unsoundness가 어떤 실용적 이유에서 나왔는지를 설계 문서에 근거해 이해한다.
- **JavaScript와의 관계 파악:** `this`의 일곱 가지 얼굴, 프로토타입 체인, 단일 스레드 이벤트 루프, null과 undefined의 이원성 — TypeScript 안에서도 살아있는 JS의 본성을 마주하고, 타입이 있어도 런타임에서 발이 걸리는 이유를 안다.
- **Java/Kotlin과의 정직한 대조:** Spring DI와 NestJS DI, `CompletableFuture`와 Promise, sealed class와 discriminated union, checked exception과 Result 타입 — 익숙한 개념에서 출발해 낯선 세계로 가는 다리를 건넌다.
- **CLI에서 풀스택까지 전 영역 적용:** CLI 도구, Electron/Tauri 데스크톱, React 웹 프론트엔드, NestJS/Hono/Express 웹 백엔드, Next.js 풀스택, Vitest 기반 테스트 전략까지 TypeScript가 실제로 살아가는 영역을 모두 걷는다.

---

## 차례

### 서문

### 1부 — 환상
1. **Java 개발자가 TypeScript를 열어보면** — 정적 타입 개발자가 처음 마주치는 당혹감의 실체, 그리고 이 책이 건네는 약속

### 2부 — 본성
2. **JavaScript의 진짜 본성** — 타입을 붙이기 전에 알아야 할 것: 프로토타입·`this`·이벤트 루프·모듈 분열
3. **TypeScript는 무엇이며, 무엇이 아닌가** — 컴파일타임의 환상: 다섯 핵심 모델(점진적·구조적·unsound·erased·TC39 정렬) 해부

### 3부 — 무기
4. **타입을 손에 익히기** — 추론·좁히기·exhaustive를 도구로: discriminated union, utility 8개, strict 모드 가족
5. **타입을 만드는 타입** — 제네릭·conditional·`infer`·매핑·템플릿 리터럴: 현실 코드의 마법을 부품 단위로 분해
6. **이 도메인을 어떻게 모델링할까** — 구조적 타입 위에서 잃지 않는 법: 에러를 도메인의 일부로
7. **비동기 모델** — Promise·async/await·Observable·AsyncIterator: `CompletableFuture`에서 건너온 개발자를 위한 재교육
8. **빌드 도구가 왜 이렇게 많은가** — 모듈·패키지·번들러·런타임의 분열: tsc·esbuild·Vite·Bun·Deno의 자리

### 4부 — 전환
9. **기존 JS 코드를 TS로 옮기기** — 점진적 도입의 패턴: 토스·카카오·우아한형제들의 실전 사례

### 5부 — 응용
10. **CLI를 짓는다** — 명령줄 도구로 TS의 첫 응용: `commander`·`inquirer`·단일 실행 파일 배포
11. **데스크톱 앱** — Electron과 Tauri의 네이티브 경계, 그리고 React Native·Expo의 모바일 자리
12. **웹 프론트엔드** — React + TS의 핵심, 그리고 다른 reactivity 모델의 위치: props·forwardRef·event·hook 타이핑
13. **웹 백엔드와 풀스택** — Express·Fastify·Hono·NestJS·Next·Astro의 여섯 길: Spring 출신에게 NestJS를 제대로
14. **테스트와 타입** — Vitest·expect-type·Playwright: 타입 안전성을 테스트 레벨까지 끌어올리기

### 6부 — 종합
15. **한국 현장의 TypeScript** — 함정·논쟁·AI 시대·다음 한 걸음

### 부록
- **부록 A.** Java/Kotlin ↔ TypeScript 용어 매핑 사전
- **부록 B.** tsconfig 옵션 사전
- **부록 C.** TS CLI 한 개 끝까지 짓기 — 워크쓰루
- **부록 D.** 한국 개발자 함정 사전 — 12개 인덱스

---

## 저자 소개

Toby-AI는 Java/Kotlin 백엔드 개발자를 위한 기술 전환 콘텐츠를 전문으로 하는 AI 저자 페르소나다. 수백만 건의 기술 문서, 커뮤니티 토론, 논문, 실무 코드베이스를 학습해 특정 독자 집단이 언어 전환 과정에서 반복적으로 마주치는 개념적 장벽을 분석하고, 그 장벽을 허무는 방식으로 콘텐츠를 구성한다.

이 책의 재료는 TypeScript와 JavaScript 공식 설계 문서, Anders Hejlsberg의 인터뷰, 토스·카카오·네이버 D2·우아한형제들의 기술 블로그, 한국어 개발자 커뮤니티에서 반복 보고된 실무 함정들이다. 기술 정확성과 독자 공감을 동시에 추구한다.

---

## 책 정보

- **파일:** `왜-TypeScript는-이렇게-생겼는가-v1.0.0.epub`
- **형식:** EPUB 3 (ko)
- **발행일:** 2026-05-04
- **분량:** 약 471페이지 (본문 약 415p + 부록 약 56p)
- **크기:** 591KB
- **표준 검증:** epubcheck 미설치 (skipped)
