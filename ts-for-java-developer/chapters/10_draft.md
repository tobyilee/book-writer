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
