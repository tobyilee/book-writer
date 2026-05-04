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
