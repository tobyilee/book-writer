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
