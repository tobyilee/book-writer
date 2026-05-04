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
