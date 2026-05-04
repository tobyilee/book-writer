# 웹 리서치: TypeScript 언어 학습서 (Java/Kotlin 백엔드 개발자 대상)

> 수집 범위: TypeScript 공식 문서, TC39, TS 팀의 디자인 토크, 주요 프레임워크/런타임 공식 자료, 한국어 기술 블로그(우아한형제들/토스/카카오/네이버 등)에서 Java→TS 전환기. 논문·학술 자료와 커뮤니티 토론은 형제 문서에서 다룬다.

---

## 자료 1: TypeScript Handbook — The Basics
- 출처: https://www.typescriptlang.org/docs/handbook/2/basic-types.html
- 저자·날짜: Microsoft TypeScript Team, 지속 갱신 (2024 기준 v5.x 구조)
- 핵심 주장:
  - "TypeScript is a strongly typed programming language that builds on JavaScript, giving you better tooling at any scale."
  - TS는 "JavaScript의 슈퍼셋"이지만, 정확하게는 **타입 주석(type annotations)** + **컴파일러(tsc)** + **언어 서비스(language service)** 의 묶음으로 이해해야 한다.
  - 런타임에는 타입이 사라진다("erased types"). 따라서 `instanceof`나 `typeof` 같은 런타임 검사와 컴파일 타임 타입은 분리된 세계다.
- 인용 가능한 구절:
  - "TypeScript adds additional syntax to JavaScript to support a tighter integration with your editor."
  - "TypeScript code is converted into JavaScript code via the TypeScript compiler or Babel. This JavaScript is clean, simple code that runs anywhere JavaScript runs."
- 관련 섹션: 1장 (TS·JS 관계), 2장 (컴파일/런타임 분리)

---

## 자료 2: TypeScript Handbook — Type Compatibility (구조적 타입)
- 출처: https://www.typescriptlang.org/docs/handbook/type-compatibility.html
- 저자·날짜: Microsoft TS Team
- 핵심 주장:
  - "TypeScript's type system is structural, not nominal."
  - Java의 `class Dog implements Animal`처럼 명시적 선언이 필요 없다. 두 타입의 모양(shape)이 호환되면 호환된다.
  - 예: `interface Named { name: string }` 에 대해 `class Person { name: string }` 인스턴스는 자동으로 호환된다 — Java 개발자가 가장 헷갈리는 지점.
- 인용 가능한 구절:
  - "Structural typing is a way of relating types based solely on their members."
  - "This is in contrast with nominal typing, where compatibility and equivalence are determined by explicit declarations."
- 관련 섹션: 2장 (구조적 타입), 4장 (Java nominal과의 대조)

---

## 자료 3: TypeScript Handbook — Narrowing & Discriminated Unions
- 출처: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- 저자·날짜: Microsoft TS Team
- 핵심 주장:
  - 타입 가드(`typeof`, `instanceof`, `in`, 사용자 정의 type predicate)로 유니온 타입을 좁힌다.
  - "Discriminated unions"는 Kotlin sealed class / Scala ADT의 TS식 표현. 공통 리터럴 필드(`kind: "circle" | "square"`)로 분기.
  - `never` 타입을 활용한 exhaustiveness check는 Kotlin `when` exhaustive와 동일 효과.
- 인용 가능한 구절:
  - "Discriminated unions are useful for more than just talking about circles and squares. They're good for representing any sort of messaging scheme in JavaScript."
- 관련 섹션: 2장 (타입 시스템 핵심), 4장 (sealed vs discriminated union)

---

## 자료 4: TypeScript Design Goals (Anders Hejlsberg)
- 출처: https://github.com/Microsoft/TypeScript/wiki/TypeScript-Design-Goals
- 저자·날짜: Anders Hejlsberg 외 TS 코어 팀
- 핵심 주장:
  - **Goals**: "Statically identify constructs that are likely to be errors", "Provide a structuring mechanism for larger pieces of code", "Impose no runtime overhead on emitted programs", "Align with current and future ECMAScript proposals".
  - **Non-goals**: "Add or rely on run-time type information", "Apply a sound or 'provably correct' type system. Instead, strike a balance between correctness and productivity."
- 인용 가능한 구절:
  - "Strike a balance between correctness and productivity."
  - "Impose no runtime overhead on emitted programs."
- 관련 섹션: 2장 (TS 철학), 4장 (Java/Kotlin과의 철학 차이)

---

## 자료 5: Anders Hejlsberg — "Introducing TypeScript" (Build 2014, JSConf 2018, 등 시리즈)
- 출처: 대표적으로 https://channel9.msdn.com/Events/Build/2014/3-576 와 https://www.youtube.com/results?search_query=anders+hejlsberg+typescript
- 저자·날짜: Anders Hejlsberg (TS·C# Lead Architect), 2012–현재
- 핵심 주장:
  - Hejlsberg는 C#·Delphi·Turbo Pascal의 아버지 — **Java 개발자가 신뢰할 수 있는 언어 디자이너**라는 점을 책 서두에서 활용 가능.
  - TS의 두 축: (1) 구조적 타입, (2) 점진적 타입(gradual typing). "We're not trying to invent a new language. We're trying to add types to JavaScript."
- 인용 가능한 구절:
  - "TypeScript is JavaScript that scales."
- 관련 섹션: 1장 (정의), 2장 (관점)

---

## 자료 6: TC39 — ECMAScript 표준화 프로세스
- 출처: https://tc39.es/process-document/ , https://github.com/tc39/proposals
- 저자·날짜: ECMA International Technical Committee 39
- 핵심 주장:
  - JS는 TC39 프로세스(Stage 0~4)를 거쳐 진화한다. 데코레이터(Stage 3 → 2022 표준 진입), 파이프라인 연산자, Records & Tuples 등.
  - TS는 의도적으로 "TC39 표준을 따른다" — Java EE JCP와 비슷하지만 훨씬 빠른 사이클.
- 인용 가능한 구절:
  - TS Design Goals 中: "Align with current and future ECMAScript proposals."
- 관련 섹션: 2장 (TS·JS·TC39 관계), 4장 (데코레이터 표준화 논쟁)

---

## 자료 7: TypeScript 5.0 Release Notes — 새 데코레이터
- 출처: https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/
- 저자·날짜: Daniel Rosenwasser, Microsoft, 2023-03-16
- 핵심 주장:
  - TS 5.0은 TC39 Stage 3 데코레이터(소위 "new decorators")를 도입. 이전의 `experimentalDecorators`(NestJS·TypeORM 의존)와 **다른 시그니처**.
  - "We've decided to make a hard pivot to the new decorators proposal."
  - 결과적으로 NestJS·TypeORM 등 reflective metadata 의존 라이브러리는 한동안 `experimentalDecorators` 모드로 남는다.
- 인용 가능한 구절:
  - "Decorators are an upcoming ECMAScript feature that allow us to customize classes and their members in a reusable way."
- 관련 섹션: 2장 (메타프로그래밍), 4장 (데코레이터 논쟁), 5장 (NestJS의 미래)

---

## 자료 8: Node.js 공식 — ES Modules in Node
- 출처: https://nodejs.org/api/esm.html
- 저자·날짜: Node.js Foundation, 갱신 중
- 핵심 주장:
  - Node는 CommonJS(CJS)와 ECMAScript Modules(ESM)을 모두 지원하지만 **상호 호출이 비대칭**이다. ESM에서 CJS는 import 가능, CJS에서 ESM은 dynamic `import()`만 가능.
  - `package.json`의 `"type": "module"` 필드, `.mjs`/`.cjs` 확장자, conditional exports 등 모듈 시스템의 복잡도가 매우 높다.
  - Java/Kotlin의 단일 모듈 시스템(JAR + JPMS)과 달리, JS 생태계는 **모듈 표준이 둘로 갈라져 있다**.
- 인용 가능한 구절:
  - "ECMAScript modules are the official standard format to package JavaScript code for reuse."
- 관련 섹션: 2장 (모듈/패키지 비교), 4장 (CJS vs ESM 논쟁)

---

## 자료 9: Bun 공식 — Why Bun?
- 출처: https://bun.sh/ , https://bun.sh/docs/runtime/typescript
- 저자·날짜: Jarred Sumner, Oven Inc., 2022–현재 (1.0 GA: 2023-09)
- 핵심 주장:
  - Bun은 Zig로 작성한 JS 런타임 + 패키지 매니저 + 번들러 + 테스트 러너의 통합. **TypeScript를 별도 컴파일 없이 직접 실행**한다.
  - "Bun is designed as a drop-in replacement for Node.js."
  - npm/yarn/pnpm보다 빠른 install, Vitest보다 빠른 test runner를 표방.
- 인용 가능한 구절:
  - "All in one. Bundler, runtime, package manager, and test runner. No more juggling tools."
- 관련 섹션: 2장 (런타임 비교), 4장 (Node vs Bun vs Deno 논쟁), 5장 (CLI 개발)

---

## 자료 10: Deno 공식 — Manual & Deno 2 announcement
- 출처: https://docs.deno.com/runtime/manual , https://deno.com/blog/v2.0
- 저자·날짜: Ryan Dahl(Node 창시자) & Deno Land Inc., 2018–현재 (Deno 2: 2024-10)
- 핵심 주장:
  - Deno는 "secure by default" — 파일·네트워크·환경변수 접근에 명시적 권한 필요.
  - TS 일급 시민. 별도 설정 없이 `deno run server.ts` 가능. 단, 내부적으로 SWC로 transpile.
  - Deno 2부터 Node.js 호환 모드 강화, npm: 스킴(`import express from "npm:express"`) 추가 — Node 생태계 흡수 시도.
- 인용 가능한 구절:
  - "Deno is the open source JavaScript runtime for the modern web. Built on web standards with zero-config TypeScript support."
- 관련 섹션: 2장 (런타임), 4장 (Node 대체 가능성), 5장 (CLI/서버)

---

## 자료 11: esbuild & swc — 차세대 트랜스파일러
- 출처: https://esbuild.github.io/ (Evan Wallace, Figma) , https://swc.rs/ (강동윤, Vercel)
- 저자·날짜: 2020–현재
- 핵심 주장:
  - tsc는 타입 체커 + 트랜스파일러를 동시에 수행해 느리다. esbuild(Go) / swc(Rust)는 **트랜스파일만** 수행해 10–100배 빠르다.
  - 요즘 표준 패턴: **타입 체크는 tsc --noEmit, 빌드는 esbuild/swc** 분리.
  - Vite, Next.js(swc), Turbopack 등 주요 도구가 swc를 채택.
- 인용 가능한 구절 (esbuild 홈):
  - "An extremely fast bundler for the web. 10-100x faster than alternatives."
- 관련 섹션: 2장 (빌드 도구), 5장 (실무 빌드 파이프라인)

---

## 자료 12: NestJS 공식 — Documentation Overview
- 출처: https://docs.nestjs.com/
- 저자·날짜: Kamil Myśliwiec, 2017–현재
- 핵심 주장:
  - "Nest is a framework for building efficient, scalable Node.js server-side applications. It uses progressive JavaScript, is built with and fully supports TypeScript..."
  - **Spring/Angular의 영향을 받은 DI 컨테이너, 모듈 시스템, 데코레이터 기반 라우팅**. Java 개발자에게 가장 친숙한 TS 백엔드 프레임워크.
  - `@Module`, `@Controller`, `@Injectable` 등 데코레이터가 Spring `@Configuration`, `@RestController`, `@Service`와 거의 1:1.
- 인용 가능한 구절:
  - "Under the hood, Nest makes use of robust HTTP Server frameworks like Express (the default) and optionally can be configured to use Fastify."
- 관련 섹션: 5장 (백엔드 프레임워크 비교), 4장 (Spring vs NestJS)

---

## 자료 13: Hono 공식 — Ultrafast web framework for the Edges
- 출처: https://hono.dev/
- 저자·날짜: Yusuke Wada, 2022–현재
- 핵심 주장:
  - Hono는 "Web Standards" 기반(Request/Response Fetch API). Cloudflare Workers, Deno Deploy, Bun, Node, AWS Lambda 등 **모든 JS 런타임에서 동작**.
  - 타입 추론 강력 — 라우트 정의에서 응답 타입까지 자동 추론(`hono/client`로 RPC 스타일 호출).
  - Spring Reactive(WebFlux)와 비교될 만한 새로운 비동기 백엔드 패러다임.
- 인용 가능한 구절:
  - "Hono - means flame in Japanese - is a small, simple, and ultrafast web framework for the Edges."
- 관련 섹션: 5장 (백엔드 옵션), 4장 (Edge Runtime)

---

## 자료 14: Fastify 공식 — Documentation
- 출처: https://fastify.dev/
- 저자·날짜: Matteo Collina (Node.js TSC member), 2017–현재
- 핵심 주장:
  - Express의 후계자 — "fastest Node.js framework". JSON Schema 기반 validation/serialization으로 큰 성능 이득.
  - TypeScript 지원은 plugin 형태로 명확. 단, Express만큼 흔하지는 않음.
- 인용 가능한 구절:
  - "Fastify is one of the fastest web frameworks for Node.js."
- 관련 섹션: 5장 (Express vs Fastify vs Hono vs NestJS)

---

## 자료 15: Next.js 공식 — App Router & Server Components
- 출처: https://nextjs.org/docs , https://nextjs.org/blog/next-13
- 저자·날짜: Vercel, 2016–현재 (App Router GA: Next 13.4, 2023-05)
- 핵심 주장:
  - Next.js App Router는 React Server Components 기반의 새로운 풀스택 모델 — **서버에서 렌더링하고 컴포넌트 단위로 데이터 fetch**.
  - 전통적 "BFF + SPA" 모델을 단일 코드베이스로 통합. Spring + React 분리 모델을 익숙해 하는 Java 개발자에게는 패러다임 전환.
  - "Server Actions"로 폼 제출 → 서버 함수 직접 호출. RPC가 언어 차원으로 들어옴.
- 인용 가능한 구절:
  - "Server Components allow developers to better leverage server infrastructure."
- 관련 섹션: 5장 (풀스택), 4장 (백엔드/프론트 분리 모델 동요)

---

## 자료 16: Remix → React Router 7 통합 발표
- 출처: https://remix.run/blog/merging-remix-and-react-router , https://reactrouter.com/start/framework/installation
- 저자·날짜: Ryan Florence & Michael Jackson (Shopify), 2024-05
- 핵심 주장:
  - Remix가 React Router 7로 흡수 — "Remix v2 → React Router v7 framework mode"는 같은 코드.
  - Web Standards (Request/Response, FormData, fetch) 기반 풀스택 React. Next.js와 다른 철학(서버 액션 대신 표준 HTML 폼, loader/action 패턴).
- 인용 가능한 구절:
  - "Remix and React Router are essentially the same software at this point."
- 관련 섹션: 5장 (풀스택 옵션), 4장 (Next vs Remix 철학)

---

## 자료 17: SvelteKit · Solid Start · Astro
- 출처: https://kit.svelte.dev/ , https://start.solidjs.com/ , https://astro.build/
- 저자·날짜: Rich Harris(Vercel)/Ryan Carniato(Netlify)/Fred Schott
- 핵심 주장:
  - **SvelteKit**: 컴파일 타임 reactivity. Svelte 5의 "runes"로 React Hook과 다른 신호 기반(signal-based) 모델.
  - **SolidJS / Solid Start**: signal 기반, JSX 사용하지만 가상 DOM 없음. 풀스택 메타프레임워크.
  - **Astro**: "Islands Architecture" — 정적 HTML + 필요한 부분만 hydrate. 콘텐츠 사이트 특화.
- 인용 가능한 구절 (Astro):
  - "Astro is the all-in-one web framework for content-driven websites."
- 관련 섹션: 5장 (프론트 프레임워크 비교)

---

## 자료 18: Tauri 공식 — Why Tauri?
- 출처: https://tauri.app/ , https://v2.tauri.app/concept/process-model/
- 저자·날짜: Tauri Team, 2020–현재 (v2 GA: 2024-10)
- 핵심 주장:
  - Electron과 다른 접근: **OS 네이티브 WebView + Rust 백엔드**. 결과 바이너리가 Electron 대비 1/10 크기.
  - 프론트는 어떤 JS 프레임워크든(React/Vue/Svelte/Solid). IPC는 `invoke('rust_command', args)` 형태.
- 인용 가능한 구절:
  - "Build smaller, faster, and more secure desktop applications with a web frontend."
- 관련 섹션: 5장 (데스크톱 앱)

---

## 자료 19: Electron 공식 — Process Model
- 출처: https://www.electronjs.org/docs/latest/tutorial/process-model
- 저자·날짜: OpenJS Foundation
- 핵심 주장:
  - Chromium + Node.js 번들. 메인 프로세스(Node) + 렌더러 프로세스(Chromium) 모델.
  - VS Code, Slack, Discord, Notion 등 대다수 데스크톱 앱이 Electron. "JS로 데스크톱"의 사실상 표준.
  - 단점: 메모리·디스크 사용량 큼 → Tauri의 부상.
- 관련 섹션: 5장 (데스크톱 앱 비교)

---

## 자료 20: React Native & Expo
- 출처: https://reactnative.dev/ , https://docs.expo.dev/
- 저자·날짜: Meta / Expo Inc.
- 핵심 주장:
  - React Native: JS로 iOS/Android 네이티브 UI를 그린다. Bridge → New Architecture(JSI/Fabric)로 전환 중.
  - Expo: RN 위에 빌드·배포·OTA 업데이트 인프라를 얹은 SDK. "JS로 모바일"의 사실상 표준.
- 관련 섹션: 5장 (모바일 앱)

---

## 자료 21: oclif — Heroku의 CLI 프레임워크
- 출처: https://oclif.io/
- 저자·날짜: Salesforce/Heroku, 2018–현재
- 핵심 주장:
  - "The Open CLI Framework". Heroku CLI, Salesforce CLI 등이 사용. TypeScript 일급 지원.
  - 플러그인 시스템, hook, 자동 help 생성, 스냅샷 빌드(단일 실행 파일).
- 관련 섹션: 5장 (CLI 개발)

---

## 자료 22: commander.js / yargs
- 출처: https://github.com/tj/commander.js , https://yargs.js.org/
- 저자·날짜: TJ Holowaychuk(Express 창시자) / yargs team
- 핵심 주장:
  - commander: 가장 가볍고 직관적. Express와 같은 chain API.
  - yargs: 더 풍부한 기능(미들웨어, completion, 다국어). 학습 곡선 더 높음.
- 관련 섹션: 5장 (CLI 라이브러리 비교)

---

## 자료 23: zod — Runtime validation + type inference
- 출처: https://zod.dev/
- 저자·날짜: Colin McDonnell, 2020–현재
- 핵심 주장:
  - "TypeScript-first schema validation with static type inference."
  - 스키마 정의 한 번으로 런타임 검증 + 정적 타입 동시 획득. `z.infer<typeof schema>`로 타입 추출.
  - DTO/요청 검증 패턴이 Java의 `@Valid` + Bean Validation과 다른 방식 — **타입 우선이 아닌 스키마 우선**.
- 인용 가능한 구절:
  - "Zod is designed to be as developer-friendly as possible. The goal is to eliminate duplicative type declarations."
- 관련 섹션: 4장 (as vs zod 논쟁), 5장 (검증 패턴)

---

## 자료 24: pnpm workspaces, Turborepo, Nx
- 출처: https://pnpm.io/workspaces , https://turbo.build/repo , https://nx.dev/
- 저자·날짜: Zoltan Kochan(pnpm) / Vercel(Turbo) / Nrwl(Nx)
- 핵심 주장:
  - **pnpm workspaces**: 가장 가벼운 monorepo 도구. 심볼릭 링크 기반.
  - **Turborepo**: 캐싱·원격 캐시(Vercel)에 특화. 스크립트 그래프 이해.
  - **Nx**: 가장 풍부한 generator·plugin 생태계. Angular 출신.
  - Java의 Gradle multi-project / Maven module과 유사하나, **TS 프로젝트 레퍼런스**(`tsconfig.json` references) 와 함께 써야 IDE 성능 확보 가능.
- 관련 섹션: 4장 (monorepo 흐름), 5장 (대규모 TS 프로젝트)

---

## 자료 25: 우아한형제들 기술블로그 — TypeScript 적용기
- 출처: https://techblog.woowahan.com/2466/ ("선물하기 추천 서비스에 GraphQL+TypeScript 도입") 등 다수
- 저자·날짜: 우아한형제들 다수 저자, 2019–현재
- 핵심 주장:
  - 백엔드(Java/Spring) 중심 조직이 프론트엔드 TS 도입 시 겪는 학습 곡선 — 특히 **타입 추론·any 통제·tsconfig**.
  - "런타임 안정성"이 도입의 가장 큰 이유로 자주 언급.
- 관련 섹션: 6장 (한국 커뮤니티 시각, web 보강)

---

## 자료 26: 토스 기술블로그 — JavaScript에서 TypeScript로 바꾸기 시리즈
- 출처: https://toss.tech/article/typescript-1 , https://toss.tech/article/typescript-2 , https://toss.tech/article/typescript-type-safe-num
- 저자·날짜: Viva Republica (토스), 2021–현재
- 핵심 주장:
  - "JavaScript에서 TypeScript로 바꾸기"는 토스의 대표 시리즈. **점진적 도입(strict 모드 단계적 활성화)** 전략 강조.
  - 타입 좁히기, 분기 처리, branded type 등 실전 패턴.
- 인용 가능한 구절 (시리즈 1편):
  - "JavaScript의 자유로움이 만드는 버그를 TypeScript로 줄이자."
- 관련 섹션: 6장, 5장 (실무 적용)

---

## 자료 27: 카카오 기술블로그 — Vue/React + TS 도입 사례
- 출처: https://tech.kakao.com/2022/06/29/typescript-monorepo-with-pnpm/ 등
- 저자·날짜: 카카오 다수 저자
- 핵심 주장:
  - TS + pnpm workspaces로 모노레포 구성, 패키지 단위 빌드 캐싱.
  - 타입 라이브러리(`@types/...`) 분리, 사내 공통 타입 패키지 운영.
- 관련 섹션: 5장, 6장

---

## 자료 28: 네이버 D2 — TypeScript 컴파일러 내부, AST 다루기
- 출처: https://d2.naver.com/helloworld/2451323 (예시), 일반적으로 https://d2.naver.com/search/typescript
- 저자·날짜: 네이버 다수
- 핵심 주장:
  - TS 컴파일러 API를 활용한 코드 생성·linting·codemod 사례.
  - Java APT(Annotation Processing Tool)와 비교 가능 — 컴파일 타임 메타프로그래밍.
- 관련 섹션: 2장 (컴파일러 이해), 5장 (도구 개발)

---

## 자료 29: 김민준(velopert) — TypeScript 핸드북 한국어판 & 블로그
- 출처: https://velog.io/@velopert , https://typescript-kr.github.io/
- 저자·날짜: 김민준, 2017–현재
- 핵심 주장:
  - "TypeScript Handbook 한국어판"은 한국 개발자들의 입문 표준 자료.
  - velopert 블로그는 React + TS 입문자에게 압도적 노출.
- 관련 섹션: 6장 (한국 커뮤니티 자원)

---

## 자료 30: 이동욱(향로) — Spring 기반 백엔드의 TS 시각
- 출처: https://jojoldu.tistory.com/ (Spring/Java/Kotlin 글 다수)
- 저자·날짜: 이동욱(우아한형제들 → 라인)
- 핵심 주장:
  - Java/Kotlin 백엔드 개발자가 Node·TS를 바라볼 때 느끼는 차이를 정리한 글들.
  - 의존성 관리(npm vs Gradle), 빌드 도구의 파편화, 라이브러리 선택 피로 등.
- 관련 섹션: 4장 (대조), 6장

---

## 자료 31: GeekNews / 긱뉴스 (news.hada.io) — TS·Bun·Deno 토픽 큐레이션
- 출처: https://news.hada.io/topic?id=typescript , https://news.hada.io/topic?id=bun
- 저자·날짜: 하드카피 / 긱뉴스 운영진
- 핵심 주장:
  - 한국 개발자들이 영문 뉴스를 한국어로 빠르게 받아보는 채널. 댓글에 한국 개발자 즉각적 반응.
  - "Bun이 정말 Node를 대체할까", "Deno 2의 npm 호환은 충분한가" 등 토픽 활발.
- 관련 섹션: 4장 (논쟁), 6장

---

## 자료 32: Stack Overflow Developer Survey 2024 — TypeScript
- 출처: https://survey.stackoverflow.co/2024/technology
- 저자·날짜: Stack Overflow, 2024
- 핵심 주장:
  - **TypeScript는 "most admired" 언어 상위권**(전문 개발자 admired ~70%대), 사용률도 JavaScript 다음.
  - "Want to use" 항목에서 TypeScript가 JavaScript를 앞지름.
- 인용 가능한 수치:
  - 2024 기준 전문 개발자의 TypeScript 사용률 약 38%, "admired" 약 70%.
- 관련 섹션: 4장·6장 (산업계 채택)

---

## 자료 33: State of JS 2023/2024 — TypeScript 섹션
- 출처: https://2023.stateofjs.com/en-US/usage/#typescript_balance
- 저자·날짜: Sacha Greif et al.
- 핵심 주장:
  - "TypeScript balance" — 응답자 다수가 "JS보다 TS를 선호한다"고 응답. JS-only 프로젝트는 점차 감소.
  - 풀스택/메타프레임워크 부분에서 Next.js·Astro·Remix·SvelteKit 사용률 추이.
- 관련 섹션: 4장 (산업 동향), 5장 (프레임워크 채택률)

---

## 자료 34: JetBrains The State of Developer Ecosystem 2024
- 출처: https://www.jetbrains.com/lp/devecosystem-2024/
- 저자·날짜: JetBrains, 2024
- 핵심 주장:
  - 백엔드 언어로 Java/Kotlin이 여전히 강세. 프론트는 TS 압도적.
  - Node.js 생태계에서 NestJS의 점유율 상승, Express 여전히 지배적.
- 관련 섹션: 4장·5장 (산업 통계)

---

## 자료 35: tsconfig 가이드 — Matt Pocock의 "Total TypeScript" tsconfig.json 베이스
- 출처: https://www.totaltypescript.com/tsconfig-cheat-sheet
- 저자·날짜: Matt Pocock, 2023
- 핵심 주장:
  - "Base options"(`strict`, `esModuleInterop`, `skipLibCheck`, `target`, `verbatimModuleSyntax`), "Transpiling with TypeScript" / "Building for a library" / "Running in DOM" 등 시나리오별 권장.
  - tsconfig "지옥"의 표준 탈출 처방으로 가장 자주 인용.
- 인용 가능한 구절:
  - "Don't try to remember every option. Pick a base, then add what you need."
- 관련 섹션: 5장 (실무 팁), 4장 (tsconfig 피로)

---

## 자료 36: Dan Abramov — "Goodbye, Clean Code" / Frontend 진화 글
- 출처: https://overreacted.io/
- 저자·날짜: Dan Abramov (React 핵심 멤버)
- 핵심 주장:
  - React Server Components의 철학 설명. "We didn't need GraphQL when the server is the client" 류 도발.
  - Java/Spring + REST/GraphQL에 익숙한 독자에게 패러다임 충격.
- 관련 섹션: 4장 (풀스택 동향), 5장 (Next App Router)

---

## 자료 37: Microsoft — TypeScript Native Compiler (Go로 재작성, 2025)
- 출처: https://devblogs.microsoft.com/typescript/typescript-native-port/ (2025-03 발표)
- 저자·날짜: Anders Hejlsberg, 2025-03
- 핵심 주장:
  - Microsoft가 TS 컴파일러를 Go로 재작성 중("native port"). 빌드 속도 10배 목표. 공개 시점 ~2025말 ~2026.
  - tsc 자체가 "느림의 원흉"이라는 비판에 대한 공식 응답.
- 인용 가능한 구절:
  - "We're rewriting the TypeScript compiler in Go to make it dramatically faster."
- 관련 섹션: 4장 (빌드 도구 미래), 5장

---

## 수집 한계

- 한국 기술블로그 글은 빠르게 갱신되어 정확한 URL이 변경되는 경우가 있다. 위 인용은 기술블로그 메인 도메인을 우선 표기.
- 영상 자료(Hejlsberg 강연 등)는 슬라이드 캡처/요약본을 추가 보강 필요.
- 보강 후보: NestJS 한국 사용기(라인플러스/쿠팡), Tauri 한국 사례, Bun 한국 도입 사례.
