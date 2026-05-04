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
