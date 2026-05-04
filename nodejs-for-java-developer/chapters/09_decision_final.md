# 9장. 결정과 설득 — 팀과 커리어에 Node를 들이는 법

8장을 닫고 자리로 돌아왔다고 해보자. 손에는 도표 한 장이 쥐어져 있다. 어디부터 잘라낼지, 어떤 경계에 BFF를 둘지, Strangler Fig 라우터는 어디에 세울지가 거기 적혀 있다. 결정은 했다. 그런데 막상 노트북을 열고 다음 한 줄을 적으려니 손이 멈춘다. 결정을 했다고 해서 일이 시작되는 것은 아니더라. 그 결정이 팀에게, 임원에게, 운영조에게 전달되어야 비로소 첫 커밋이 만들어진다. 그리고 그 전달은 우리가 평소에 짜는 코드보다 훨씬 더 까다로운 작업이다.

1장에서 한 단락을 닫으며 이런 말을 했었다. "도구만 바뀌었을 뿐, 우리가 다루는 동시성 문제 자체는 같다." 9장은 그 문장을 조직과 커리어 차원으로 옮겨오는 자리다. 우리가 Spring에서 풀던 백엔드 문제는 Node에서도 같은 모양으로 살아 있다. 다만 이번에는 그 문제를 풀 도구를 한 개 늘리겠다고 팀에 설득해야 하고, 새로 들어오는 동료에게 가르쳐야 하고, 코드 리뷰에서 익숙하지 않은 함정들을 짚어내야 하고, 후퇴해야 할 신호가 보이면 정직하게 인정할 수 있어야 한다. 본인 커리어 차원에서도 두 번째 런타임을 갖는다는 게 시장에서 어떤 의미인지를 한 번쯤 정리해두는 편이 낫다.

이번 장의 톤은 이 책의 다른 장과 약간 다르다. 코드를 더 적게 보고, 사람을 더 많이 본다. 기술 결정은 결국 사람의 결정이라는 사실을 8장이 끝나는 지점에서 정직하게 받아들였다면, 9장은 그 사실을 가지고 자기 조직 안에서 어떻게 움직일지를 같이 그려보는 자리다.

## 한 페이지로 답하는 "왜 Node인가" — 임원·팀원·운영조에게 다른 언어로

기술 선택 회의가 잡혔다고 해보자. 30분 슬롯이고, 발표자는 본인이다. 슬라이드 한 장에 "왜 Node인가"를 답해야 한다. 회의실에는 세 부류가 앉아 있다. 임원은 사업 위험과 기회를 본다. 팀원은 자기가 내일부터 무엇을 배워야 하는지를 본다. 운영조는 새벽에 페이저가 울릴 때 본인이 어떤 화면을 보게 될지를 본다. 같은 결정에 대해 셋 모두 다른 질문을 가지고 들어온다. 한 페이지로 답한다는 말은, 한 메시지를 셋에게 같은 톤으로 들이민다는 뜻이 아니다. 한 결정의 세 가지 얼굴을 같은 종이 위에 정직하게 풀어낸다는 뜻이다.

임원에게는 사례와 수치로 시작하자. PayPal이 같은 페이지를 Java로도 짜고 Node로도 짜본 뒤 RPS 2배, 응답 시간 35% 감소, 코드량 33% 감소를 손에 쥐었다는 이야기. LinkedIn이 모바일 백엔드를 Rails에서 Node로 바꾸며 서버 30대를 3대로 줄였다는 이야기. Netflix가 UI 서버 시작 시간을 40분에서 1분 미만으로 끌어내렸다는 이야기. 한국 사례로 줌인터넷이 Spring Boot에서 Node로 옮기며 같은 하드웨어에서 TPS 약 40% 상승, 메모리 50% 이상 감소, 백엔드 코드 1,608줄에서 472줄로 71% 축소를 얻었다는 이야기. 당근마켓이 푸시알림 마이크로서비스 한 조각을 Node로 분리해 초당 1,500 RPS를 누락 없이 처리했다는 이야기. 이 다섯 줄짜리 사례 묶음이 임원에게는 가장 강한 한 단락이 된다. "이미 잘 알려진 회사들이 비슷한 모양의 결정을 내렸고, 그들이 본 수치가 우리가 기대할 수 있는 범위의 윗부분이다. 우리는 그중 어떤 경계에 같은 결정을 적용할지를 골랐다."

다만 임원 슬라이드에는 후퇴 사례 한 줄도 같이 둬야 한다. Uber가 2018년에 Node 기반 RTAPI를 신규 권장 스택에서 제외한 이야기, 그리고 그 이유가 "신규 엔지니어 온보딩 비용이 컸다"는 것. 이 한 줄을 빼면 발표는 영업이 되고, 영업으로 들어간 결정은 6개월 뒤 부메랑으로 돌아온다. 임원은 위험을 같이 인정하는 발표를 더 신뢰한다. "감당한다, 단 조건이 있다"라는 한 줄이 1장의 의심에 대한 우리의 정직한 대답이 되어줄 것이다.

팀원에게는 학습 곡선과 일상이 어떻게 바뀌는지를 보여줘야 한다. Spring에서 쓰던 패턴이 NestJS에서 거의 같은 모양으로 살아 있다는 점 — `@Controller`는 그대로 `@Controller`, `@Bean`은 `@Injectable`, IoC 컨테이너는 NestJS 모듈, 인터셉터·필터·가드·파이프가 Spring의 같은 자리에 매칭된다는 점. 직방 김동영의 회고가 "구조가 매우 유사해 적응이 빨랐다"라고 정리해 둔 그 부분이 팀원의 가장 큰 걱정 — "내가 새로 배워야 하는 게 얼마나 많은가"에 대한 가장 솔직한 답이 된다. 단, 다른 점도 같이 일러줘야 한다. Hibernate의 자동 dirty checking 같은 마법은 Prisma에 없다. `@Transactional` 어노테이션 한 줄이 트랜잭션을 자동으로 열어주던 그 편안함은 `prisma.$transaction(...)`이라는 명시적 호출로 바뀐다. 이 두 가지가 적응 첫 주의 가장 큰 충격 포인트일 거라는 점을 미리 말해두자.

운영조에게는 Day 1 운영의 모양을 그려줘야 한다. 콜드 스타트가 200밀리초 이하로 떨어진다는 점, Lambda나 Cloudflare Workers 같은 환경에 부담 없이 들어간다는 점이 우선 운영조의 호기심을 깬다. 다만 graceful shutdown은 Spring Boot 2.3+의 `server.shutdown=graceful`만큼 빌트인이 아니라는 사실, SIGTERM을 받고 HTTP 서버 close, DB·큐 connection close, 진행 중 잡 마무리까지를 직접 적어야 한다는 사실, 컨테이너 안에서는 PM2 cluster를 빼고 Kubernetes에 그 역할을 맡기는 게 보통이라는 점, 헬스체크는 `@nestjs/terminus`로 liveness/readiness를 분리하는 패턴이 표준이라는 점, 로깅은 처음부터 Pino + correlation id + OpenTelemetry로 구조화해야 한다는 점 — 이런 일곱 줄짜리 운영 약속이 운영조의 페이저를 미리 진정시킨다. 7장에서 펼쳐낸 운영 체크리스트가 이 자리에서 발표 자료의 한 페이지로 압축되는 셈이다.

세 부류의 청중에게 다른 언어로 같은 결정을 풀어내는 일이 한 페이지에 다 들어가야 한다. 위쪽에는 임원이 볼 사례 묶음과 후퇴 한 줄, 가운데에는 팀원이 볼 패턴 매핑과 첫 주의 충격 두 가지, 아래쪽에는 운영조가 볼 Day 1 약속 일곱 줄. 이 한 장은 회의 30분이 끝난 뒤에도 책상에 남아 다른 사람의 책상에까지 옮겨다닐 한 장이다. 만들어두면 두고두고 인용된다.

이 발표가 끝나고 나면 자연스럽게 다음 질문이 따라온다. "그래서 내일부터 누가 이걸 짜는데?"

## 채용·온보딩 — 이 책의 장 순서가 그대로 4~6주 학습 플랜이 된다

새 사람이 팀에 들어왔다고 해보자. Spring 5년 경력, NestJS는 이름만 들어봤다. 첫 4~6주를 어떻게 짜야 그 사람이 PR 리뷰에 들어와 의미 있는 코멘트를 달 수 있는 상태로 만들 수 있을까. 마침 이 책의 장 순서가 그대로 한 학습 플랜이 된다.

1주차는 1·2장이다. 첫 사흘은 1장 — Node.js 런타임의 본체가 V8 + libuv라는 사실, 단일 스레드 이벤트 루프가 어떤 단계로 도는지, 비동기 I/O가 OS 비동기 인터페이스로 풀리는 한편 CPU 바운드는 별도 처리가 필요하다는 점을 손으로 만져보게 한다. 손에 익혀야 할 도구는 Node 22 LTS 설치, `nvm` 또는 `volta` 버전 매니저, Chrome DevTools `--inspect` 한 번 붙여서 `setTimeout`이 어느 단계에서 깨어나는지 직접 보기. 그다음 이틀은 2장 — TypeScript의 함정. `Partial`, `Pick`, `Omit`, `Record`, `ReturnType` 같은 유틸리티 타입을 한 번씩 써보고, 구조적 호환의 함정 — 빈 객체가 인터페이스를 만족하는 그 황당한 순간을 한 번 직접 겪게 하자. `var`/`let`/`const`의 클로저 캡처 차이, `==`와 `===`의 차이, `null`과 `undefined`의 두 가지 비어 있음을 짧은 퀴즈로 풀어보면 좋다. 패키지 관리는 `pnpm` 한 번 깔고 `pnpm install`이 `node_modules`에 hoisting을 어떻게 하는지를 보면 충분하다.

2~3주차는 4·5장이다. NestJS 프로젝트를 하나 짜본다. CLI로 `nest new`를 치고, 첫 컨트롤러·서비스·모듈을 만들고, `@Module`의 `providers`/`controllers`/`imports` 배열을 직접 적게 한다. Spring의 컴포넌트 스캔과는 다르다는 첫 충격이 여기서 온다. 가드·인터셉터·파이프·필터를 차례로 한 번씩 작성해보면 Spring의 시큐리티·인터셉터·바인더·예외 핸들러가 같은 자리에 들어와 앉는 모습이 그려진다. 그다음으로 Prisma. `schema.prisma`에서 모델을 그리고, `prisma migrate dev`로 첫 마이그레이션을 돌리고, `findMany`·`findUnique`·`create`·`update`·`delete`를 손에 익힌다. 그리고 두 번째 주차의 가장 중요한 한 시간은 `select`/`include`로 명시적 로딩을 가르치는 시간이다. Hibernate의 lazy loading이 없다는 사례를 직접 만들어보자 — 관계를 `include` 없이 끌어오면 `undefined`가 나오고, `forEach` 안에서 한 건씩 `findUnique`를 부르면 N+1이 그대로 만들어진다는 사실을 SQL 로그로 눈에 보여줘야 한다. 이 한 시간이 일주일 동안 데이는 PR 리뷰 두세 건을 미리 막는다.

4주차는 6·7장이다. 디버깅 도구 한 묶음 — Chrome DevTools Memory 탭, `clinic doctor`, `clinic flame`, `--inspect`, `v8.writeHeapSnapshot()`. JVM 출신이라면 jstack·jmap·VisualVM·JFR·MAT의 자리에 무엇이 들어오는지를 머리로 그릴 수 있어야 한다. 그다음으로 운영. graceful shutdown을 손으로 한 번 짜보고 — `process.on('SIGTERM', ...)`에 HTTP close, DB connection close, 진행 중 잡 마무리를 묶어 적는다. Pino로 구조화 로깅을 깔고, OpenTelemetry SDK로 trace_id를 자동 주입한다. `@nestjs/terminus`로 `/healthz`와 `/readyz`를 분리한다. 이벤트 루프 lag를 `perf_hooks.monitorEventLoopDelay()`로 한 번 측정해 두면 좋다. p99이 50밀리초를 넘는 순간이 어떤 모양인지, 그게 왜 사용자에게 보이는지를 직접 그래프로 보면 추상이 사라진다.

5~6주차는 8장이다. 사이드 프로젝트로 모놀리스 한 조각을 골라 BFF 또는 워커 한 개를 떼어내본다. Strangler Fig의 모양을 손으로 그려보는 단계다. API Gateway 한 개 세우고, 모놀리스 앞에 Node 서비스 한 개를 두고, 1~5%의 트래픽을 mirroring으로 흘려보고, 결과를 비교한다. 5주차에 mirroring을 띄우고 6주차에 1% 카나리, 5%, 25%로 키워가는 패턴이 가장 안전하다. 이 6주가 끝나면 그 사람은 PR 리뷰에 들어와도 코드를 읽을 수 있고, 가장 자주 데이는 함정 다섯 가지를 짚어낼 수 있다.

채용 공고를 쓸 때도 이 6주 플랜이 그대로 가이드가 된다. JD에 "Spring/Java 백엔드 경험 + Node/TypeScript는 6주 안에 따라잡을 수 있다"라고 써두면, Spring 출신 시니어가 자기 시장 가치를 줄이지 않으면서 들어올 수 있다는 신호가 된다. 처음부터 NestJS+Prisma 경력자만 찾겠다고 하면 풀이 작아진다. 차라리 Spring 경력 + 학습 의지로 풀을 넓히고, 6주 플랜을 입사 첫 사이클로 약속해주는 편이 합리적이다.

## PR 리뷰에서 자주 데이는 다섯 가지 함정

7장에서는 운영의 축으로 graceful shutdown, 구조화 로깅, OpenTelemetry, 헬스체크, 이벤트 루프 lag 모니터를 다뤘다. 9장에서는 다른 축이다. 코드 리뷰 시점에서 Spring 출신이 자주 놓치는 다섯 가지 함정. 이 다섯 가지가 PR에 섞여 들어왔을 때 잡아내지 못하면 운영에서 새벽 페이저로 돌아온다.

**첫 번째 함정 — 이벤트 루프를 막는 코드.** Spring에서는 한 요청이 하나의 스레드를 점유하고 그 스레드 안에서 1~2초 정도의 동기 작업을 해도 옆 요청이 별로 영향받지 않았다. Node에서는 같은 코드가 전체 프로세스의 모든 요청을 잠시 멈추게 한다. PR에서 가장 자주 보이는 모양은 네 가지다. `crypto.pbkdf2Sync` 같은 동기 crypto 호출, 수십 메가바이트짜리 응답에 대한 `JSON.parse`, 검증되지 않은 정규식 패턴(특히 `(a+)+$`처럼 backtracking이 폭주하는 모양), 그리고 `fs.readFileSync` 같은 동기 파일 I/O. 리뷰에서 이런 줄을 만나면 "이 함수가 호출되는 빈도와 입력 크기"를 묻는 한 줄 코멘트를 달자. 빈도가 높거나 입력이 임의 크기면 비동기 버전으로 바꾸거나, CPU 바운드라면 `worker_threads`나 별도 마이크로서비스로 빼는 결정을 같이 의논해야 한다.

```typescript
// 이런 모양은 일단 눈에 띄어야 한다
import * as crypto from 'crypto';
import * as fs from 'fs';

export function hashPasswordSync(password: string, salt: string): string {
  // 동기 pbkdf2는 이벤트 루프를 잡아둔다. 모든 요청에 영향이 간다.
  return crypto.pbkdf2Sync(password, salt, 100_000, 64, 'sha512').toString('hex');
}

export function loadConfig(path: string) {
  // 부팅 1회면 괜찮지만, 요청 경로 안이라면 매 요청마다 이벤트 루프가 멈춘다.
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

// 같은 일을 비동기로
export async function hashPassword(password: string, salt: string): Promise<string> {
  return new Promise((resolve, reject) => {
    crypto.pbkdf2(password, salt, 100_000, 64, 'sha512', (err, key) => {
      if (err) return reject(err);
      resolve(key.toString('hex'));
    });
  });
}
```

`pbkdf2Sync`나 `readFileSync` 같은 이름은 검색이 쉽다. 팀 ESLint 규칙에 `no-sync` 또는 `n/no-sync`를 켜두는 것도 한 가지 안전망이다. 다만 ESLint가 다 잡지는 못한다. 정규식 backtracking이나 큰 `JSON.parse`는 사람이 봐야 한다. PR에서 정규식이 등장하면 입력 길이 가드 한 줄을 같이 요청하자.

**두 번째 함정 — `await` 누락.** Java의 `Future`나 `CompletableFuture`는 깜빡 잊고 `.get()`을 안 부르면 컴파일이 통과해도 결과가 안 나오니까 비교적 빨리 발견됐다. Node의 Promise는 더 조용히 새어나간다. 가장 흔한 모양 셋이 있다. `forEach` 안에서 `await`를 쓰면 콜백 함수의 Promise가 그냥 버려진다. 함수가 Promise를 반환하는데 호출 측에서 `await` 없이 부르면 에러가 잡혀도 어디로 갔는지 모른다. 그리고 `try/catch`가 동기적으로만 감싸고 있으면 비동기 throw는 그 catch에 안 잡힌다.

```typescript
// 이 셋이 PR에서 가장 자주 보이는 모양이다

// 함정 A: forEach + async — 콜백의 Promise는 버려진다
async function sendNotificationsBad(userIds: number[]) {
  userIds.forEach(async (id) => {
    await pushClient.send(id);  // 여기서 throw가 나도 외부 catch에 안 잡힌다
  });
  // 함수가 즉시 끝난다. 푸시는 백그라운드에서 누락되거나 순서가 섞인다.
}

// 같은 일을 안전하게
async function sendNotificationsOk(userIds: number[]) {
  await Promise.all(userIds.map((id) => pushClient.send(id)));
  // 또는 동시성을 제한하고 싶으면 p-limit 같은 라이브러리로 묶는다
}

// 함정 B: 반환된 Promise를 await 안 함
async function chargeAndLog(orderId: number) {
  paymentService.charge(orderId);  // await 빠짐. 결제가 끝나기 전에 다음 줄이 실행된다
  logger.info({ orderId }, 'charged');
}

// 함정 C: try/catch가 동기적으로만 감쌈
function chargeWrong(orderId: number) {
  try {
    paymentService.charge(orderId);  // Promise를 반환만 하고 await 없음
  } catch (e) {
    // 비동기 throw는 여기 안 들어온다. unhandledRejection으로 새어나간다.
    logger.error({ e, orderId }, 'charge failed');
  }
}
```

방어선 두 개를 깔자. 첫째, `tsconfig.json`의 `"strict": true`와 ESLint의 `@typescript-eslint/no-floating-promises`, `@typescript-eslint/await-thenable`을 켠다. 이 둘이 위 세 함정의 70%쯤은 자동으로 잡는다. 둘째, 프로세스 시작 시점에 `process.on('unhandledRejection', (e) => { logger.fatal(e); process.exit(1); })`를 걸어두자. 새어나간 Promise가 조용히 무시되지 않고 운영 알림으로 떠야 한다.

**세 번째 함정 — Prisma `select`/`include` 누락으로 만들어진 N+1 또는 `undefined` 접근.** Hibernate 출신은 관계가 lazy로 자동 로드된다는 가정을 몸에 가지고 있다. Prisma는 그렇지 않다. 명시적 `include`/`select`가 없으면 관계 필드는 결과에 들어오지 않는다. 그리고 그 사실을 잊고 `order.items.length`를 호출하면 `undefined`가 나온다. 또는 `for-of` 안에서 한 건씩 `findUnique`를 부르면 그게 곧 N+1이다. PR 리뷰에서 가장 자주 보이는 모양은 이렇다.

```typescript
// 함정: Hibernate 가정으로 짜인 코드
async function listOrdersBad(userId: number) {
  const orders = await prisma.order.findMany({ where: { userId } });
  // include 없음 → orders[i].items는 undefined
  return orders.map((o) => ({
    id: o.id,
    itemCount: o.items.length,  // TypeError: Cannot read properties of undefined
  }));
}

// 또 다른 함정: for-of + findUnique = N+1
async function enrichOrdersBad(orderIds: number[]) {
  const result = [];
  for (const id of orderIds) {
    const order = await prisma.order.findUnique({ where: { id } });
    const customer = await prisma.user.findUnique({ where: { id: order!.userId } });
    result.push({ ...order, customer });
  }
  // orderIds.length * 2회 쿼리. 100건이면 200회 왕복.
  return result;
}

// 같은 일을 한 번에
async function listOrdersOk(userId: number) {
  return prisma.order.findMany({
    where: { userId },
    include: { items: true },  // 명시적 include — 한 번에 가져온다
  });
}

async function enrichOrdersOk(orderIds: number[]) {
  return prisma.order.findMany({
    where: { id: { in: orderIds } },
    include: { user: true },
  });
  // 1회 쿼리. JOIN으로 처리.
}
```

Prisma는 결과 타입을 `include` 여부에 따라 다르게 생성한다. 그 점이 함정을 막는 1차 방어선이다. 코드에서 `o.items`라고 쓰는 순간 타입 오류가 떠야 정상이다. 다만 `as` 캐스팅으로 타입을 우회한 PR에서는 그 방어선이 무너진다. 이건 곧장 네 번째 함정과 이어진다.

**네 번째 함정 — 타입 안전 우회.** Java도 `(Foo) obj` 캐스트로 컴파일러를 속일 수 있다. TypeScript는 더 쉽다. `obj as Foo`로 한 줄이면 끝난다. 그리고 더 위험한 건 구조적 호환의 함정이다. 빈 객체 `{}`가 어떤 인터페이스든 만족하는 상황 — 모든 필드가 옵션이거나, 인터페이스 자체에 필드가 없는 경우 — 가 의외로 많다. 외부 API 응답을 검증 없이 `as ExternalUser`로 단정하는 패턴은 가장 자주 만나는 PR 함정이다.

```typescript
// 함정: 외부 응답을 검증 없이 단정
async function getUserUnsafe(id: number): Promise<User> {
  const res = await fetch(`https://external.api/users/${id}`);
  return (await res.json()) as User;  // 외부 응답이 정말 User 모양이라는 보장이 없다
}

// 함정: any 또는 ! 비검증
async function processPayment(payload: any) {
  const amount = payload.order!.amount;  // payload.order가 undefined면 런타임 폭발
  // ...
}

// 같은 일을 안전하게 — Zod 스키마로 런타임 검증
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  name: z.string(),
});
type User = z.infer<typeof UserSchema>;

async function getUserSafe(id: number): Promise<User> {
  const res = await fetch(`https://external.api/users/${id}`);
  return UserSchema.parse(await res.json());  // 모양이 다르면 여기서 throw
}
```

PR 리뷰에서는 세 가지 신호를 의식적으로 찾자. `as` 캐스팅, `any` 타입, `!` (non-null assertion). 이 셋이 등장한 줄은 모두 "왜 이 우회가 필요했는지"를 묻고, 가능하면 Zod·io-ts·class-validator 같은 런타임 검증으로 바꾸자. 4장에서 다뤘던 `class-validator` + NestJS `ValidationPipe`가 입력 경계의 표준 답이다. 출력 경계나 외부 API 응답에서는 Zod가 가볍고 좋다. `tsconfig.json`의 `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`를 켜두면 자잘한 함정을 컴파일러가 더 많이 잡는다.

**다섯 번째 함정 — 예외 전파의 모양.** Java의 checked exception이 그리워지는 자리다. Java에서는 `throws SQLException`이 메서드 시그니처에 박혀 있어, 어디서 어디로 예외가 흐르는지 컴파일러가 따라가준다. TypeScript에는 그 장치가 없다. 비동기 throw는 더 조용히 새어나간다. 그리고 NestJS·Express에는 에러 미들웨어/필터가 따로 있는데, 이 자리를 안 만들어두면 Promise rejection이 결국 `process.on('unhandledRejection')`까지 가서 프로세스 자체가 죽는다.

```typescript
// 함정: try/catch 누락 + 에러 미들웨어 미구성
@Controller('orders')
export class OrdersController {
  @Post()
  async create(@Body() dto: CreateOrderDto) {
    const order = await this.ordersService.create(dto);
    // create 안에서 DB 락 충돌이 나면 어디로 가는가?
    return order;
  }
}

// NestJS는 기본 ExceptionFilter가 있지만, 도메인 예외를 HTTP로 매핑하려면 직접 짜야 한다
@Catch(DomainConflictError)
export class DomainConflictFilter implements ExceptionFilter {
  catch(exception: DomainConflictError, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    response.status(409).json({
      statusCode: 409,
      message: exception.message,
      code: exception.code,
    });
  }
}

// 그리고 마지막 안전망 — 부팅 시 한 번 깔아두자
process.on('unhandledRejection', (reason, promise) => {
  logger.fatal({ reason, promise }, 'unhandledRejection — process exiting');
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  logger.fatal({ err }, 'uncaughtException — process exiting');
  process.exit(1);
});
```

리뷰에서는 두 가지를 보자. 컨트롤러/핸들러 메서드에 `try/catch`가 보이지 않으면, 호출하는 서비스가 던지는 예외가 어디로 가는지를 한 번 추적해보자. 도메인 예외 → HTTP 매핑이 필터로 잡혀 있는지, 그게 글로벌 등록되어 있는지를 확인하자. 그리고 `process.on('unhandledRejection')`/`uncaughtException` 핸들러가 부팅 코드에 박혀 있는지를 보자. 이 셋만 갖춰져 있어도 운영 사고의 8할이 사라진다.

다섯 가지를 한 자리에 정리하면 이렇다. 정리표는 리뷰 코멘트에 인용할 때 쓰자.

| 함정 | 자주 보이는 코드 모양 | 1차 방어선 | 2차 방어선 |
|---|---|---|---|
| 이벤트 루프 블로킹 | `pbkdf2Sync`, 큰 `JSON.parse`, 정규식 backtracking, `readFileSync` | ESLint `no-sync`, 입력 크기 가드 | `clinic doctor`, `monitorEventLoopDelay` |
| `await` 누락 | `forEach + async`, await 없는 호출, 동기 try/catch | `@typescript-eslint/no-floating-promises`, `await-thenable` | `process.on('unhandledRejection')` |
| Prisma N+1·undefined | `include`/`select` 없이 관계 접근, for-of + findUnique | Prisma 생성 타입의 컴파일 오류 | SQL 로그 모니터링, slow query 알림 |
| 타입 우회 | `as`, `any`, `!`로 외부 데이터 단정 | `tsconfig` strict + `noUncheckedIndexedAccess` | Zod/io-ts 런타임 검증, ValidationPipe |
| 예외 전파 | try/catch 없음, 에러 필터 미구성, unhandled 핸들러 없음 | NestJS `ExceptionFilter`, 도메인 예외 매핑 | `unhandledRejection`/`uncaughtException` 핸들러 |

이 표는 리뷰어와 작성자가 같은 언어로 이야기할 수 있는 공용 어휘가 된다. PR 코멘트가 "이 줄은 함정 2번"이라고 한 줄이면 통한다. 6주 학습 플랜을 끝낸 신입에게도 이 표는 첫 분기의 PR 리뷰 가이드가 된다.

## 모놀리스 vs 마이크로서비스 — modular monolith부터 시작하라

여기서 한 가지 결정이 더 남는다. Strangler Fig으로 어디부터 잘라낼지를 8장에서 그렸다면, 잘라낸 그 한 조각의 안쪽 구조는 어떻게 짜야 하는가. 첫날부터 마이크로서비스 다섯 개를 띄워야 하는가, 아니면 모놀리스 안에서 모듈을 잘 나누는 정도로 시작해야 하는가.

Sam Newman과 Martin Fowler의 일반 권고는 일관된다 — modular monolith부터 시작하라는 것. 이 권고가 Node 맥락에서도 그대로 살아 있다. 이유는 두 가지다. 하나, 분산 트랜잭션·관측성·운영 복잡도는 마이크로서비스 수에 거의 정비례해서 늘어난다. 다섯 개 서비스가 되는 순간 OpenTelemetry 분산 trace가 없으면 디버깅이 사실상 불가능해진다. 둘, Uber의 후퇴 사례에서 본 것처럼 신규 엔지니어 온보딩 비용이 빠르게 임계점을 넘는다. 마이크로서비스 일곱 개를 처음 만나는 신입은 첫 한 달 동안 어디부터 읽어야 할지를 모른 채 시간을 흘려보낸다.

Node 진영에서 modular monolith의 가장 자연스러운 모양은 NestJS Monorepo다. 인프랩이 JS+Express+FxJS 조합에서 TypeScript+NestJS Monorepo로 옮길 때 골랐던 그 구조다. 한 레포 안에 여러 NestJS 앱과 공유 라이브러리를 두고, 도메인 경계는 모듈로 나누되 배포 단위는 처음에 한두 개로 묶는다. 필요할 때만 모듈 한 개를 별도 앱으로 빼낸다.

```
apps/
├── api-gateway/         # Strangler Fig 라우터
├── core-api/            # 모놀리스 — 도메인 모듈을 한 묶음으로
│   └── src/
│       ├── orders/      # 주문 도메인 모듈
│       ├── users/       # 사용자 모듈
│       ├── payments/    # 결제 모듈
│       └── inventory/   # 재고 모듈
├── notification-worker/ # BullMQ 워커 — 이미 분리할 가치가 있는 한 조각
└── bff-mobile/          # 모바일 앱 BFF
libs/
├── domain-events/       # 공유 이벤트 타입
├── auth/                # 공유 인증 미들웨어
└── observability/       # OTel·Pino 표준 설정
```

이 구조의 장점은 셋이다. 첫째, 처음에는 `core-api` 한 개만 배포해도 되니까 운영 부담이 작다. 둘째, 도메인 경계가 분명하면 나중에 한 모듈을 별도 앱으로 빼낼 때 코드 이동이 거의 디렉터리 이동 수준에서 끝난다. 셋째, `libs/domain-events`처럼 공유 계약을 한 자리에 두면 분리 후에도 타입 호환이 깨지지 않는다. NestJS CLI의 `nest g app`과 `nest g library` 명령어가 이 구조를 그대로 만들어준다. 빌드 도구로는 `nx`나 `turborepo`가 결합된다. 의존성은 `pnpm` workspace로 묶어 hoisting 문제를 줄인다.

Spring 진영의 비교는 자연스럽다. Spring Boot 멀티 모듈 Gradle 프로젝트가 정확히 같은 자리에 있다. 도메인별 Gradle 모듈을 만들고, 한 `bootJar`로 묶어 배포하다가 필요해지면 모듈 한 개를 별도 `bootJar`로 빼낸다. NestJS Monorepo는 같은 사고를 TypeScript 생태계 모양으로 옮긴 것이다. 익숙해지는 데 일주일이면 충분하다.

분리해도 되는 신호는 단순하다. 한 모듈의 배포 사이클이 다른 모듈과 명백히 달라질 때 — 예를 들어 결제는 보수적으로 일주일에 한 번 배포해야 하지만 사용자 피드는 하루에 다섯 번 나가야 할 때. 또는 한 모듈이 다른 모듈과 명백히 다른 운영 특성을 가질 때 — 예를 들어 실시간 알림 워커가 메인 API와 다른 스케일링 곡선을 가질 때. 이런 신호가 보이지 않는데 서비스를 미리 쪼개두면, 6개월 뒤 분산 모놀리스라는 가장 나쁜 지점에 도달한다. 두 개를 같이 배포해야 한 변경이 끝나는 그런 모양 말이다.

## 후퇴 신호 — 자기 조직을 어떻게 측정할 것인가

들어간 결정만큼 중요한 게 빠져나오는 결정이다. Uber의 2018년 사례가 우리에게 가르쳐주는 가장 정직한 교훈이다 — Node로 시작했다고 해서 Node로 끝나야 하는 건 아니다. 신규 엔지니어 온보딩 비용이 너무 커진 시점에 그들은 권장 스택에서 Node를 제외했다. 이게 실패가 아니다. 같은 결정을 다른 시점·조직·도메인에 다시 점검한 결과일 뿐이다. 우리 조직에도 같은 점검 회로가 있어야 한다.

자기 조직에서 측정할 후퇴 신호 셋을 권한다.

**신호 1 — 신규 엔지니어 온보딩 시간.** 새 사람이 입사 후 첫 PR을 머지하기까지 걸리는 시간을 분기마다 잰다. 6주 학습 플랜을 한 번 돌렸다면 그게 베이스라인이다. 그 시간이 분기마다 늘어나고 있다면 — 예를 들어 첫 분기 6주에서 다음 분기 9주, 그다음 12주로 — 코드베이스가 학습하기 어려워지고 있다는 신호다. Uber가 실제로 본 신호가 이거다. 측정은 단순하다. 입사일과 첫 머지 PR 날짜를 HR 시스템과 GitHub에서 뽑으면 된다. 분기 평균이 한 번이라도 1.5배 이상 뛰면 회의 안건으로 올린다.

**신호 2 — 사내 라이브러리 부채.** 우리만 쓰는 사내 도구·라이브러리·DSL이 공식 생태계와 어긋나 있는 정도. Node 생태계는 빠르게 움직이니까 사내 fork가 메인을 따라가지 못하는 순간이 잘 온다. `libs/`에 있는 패키지의 의존성이 1년 이상 업데이트되지 않은 게 몇 개인지, ESM 마이그레이션이 막혀 있는 모듈이 몇 개인지, 사내에서만 통용되는 데코레이터·HOF·믹스인 패턴이 몇 개인지를 분기마다 센다. NestJS v12의 ESM 풀 마이그레이션이 다가오는 시점에 이 부채는 더 무거워진다. `npm outdated` 한 번 돌리고, `depcheck`로 사용하지 않는 의존성을 추리고, 사내 라이브러리는 README의 마지막 커밋 날짜를 직접 보자. 이 부채가 분기마다 커지고 있다면 도구를 손에 익히는 시간이 비즈니스 시간을 잡아먹기 시작한 것이다.

**신호 3 — 운영 사고 빈도와 모양.** 6장에서 익힌 디버깅 도구로 측정한다. 이벤트 루프 lag p99이 50밀리초를 넘는 빈도가 분기마다 늘어나는가. heap 사용량이 우상향하는 메모리 누수가 한 분기에 몇 번 잡히는가. `unhandledRejection`이 분기당 몇 회 발생하는가. APM 대시보드 한 페이지를 분기 보고로 만들어두자. 사고 자체가 꼭 늘어나는 게 아니라, 같은 모양의 사고가 반복된다면 — 예를 들어 매 분기 새로운 이벤트 루프 블로킹이 새로운 PR로부터 다시 들어온다면 — 코드 리뷰 문화나 학습 커리큘럼에 구멍이 있다는 뜻이다. 이건 6장에서 깐 도구들이 그대로 분기 KPI 패널이 된다는 점에서 자연스러운 회수다.

이 셋을 분기마다 같은 자리에 두고 본다. 한 번 튀는 건 잡음이고, 두 분기 연속이면 회의, 세 분기 연속이면 결정 시점이다. 결정의 모양은 두 가지로 나뉜다. 하나는 "지금 모양을 그대로 두되 학습 커리큘럼·리뷰 문화·라이브러리 갱신을 보강하자"의 보수 결정. 또 하나는 "한 도메인에 대해서는 다른 런타임이 더 맞는다"는 부분 후퇴 결정 — Uber가 RTAPI에 대해 내린 결정이 정확히 이 모양이었다. 후퇴는 부끄러움이 아니다. 시점·조직·도메인의 변화에 정직하게 응답하는 회로가 살아 있다는 증거다.

JVM 도구로 같은 KPI를 측정해본 경험이 있는 사람에게는 익숙한 작업이다. Spring 운영에서 Micrometer + Actuator + Datadog APM으로 보던 패널이 Node 운영에서는 Pino + OpenTelemetry + Datadog/New Relic으로 옮겨오는 것뿐이다. 도구가 바뀌었을 뿐, 측정해야 할 KPI 자체는 같다. 1장의 메시지가 운영 KPI에까지 그대로 살아 있는 셈이다.

## 커리어 신호 — 시니어가 두 번째 런타임을 갖는다는 것

이번 절은 조직 이야기를 잠시 내려놓고 본인 커리어 이야기다. 결정이 조직 안에서만 의미를 가지는 게 아니라 본인의 시장 가치 안에서도 의미가 있다. 정직하게 같이 봐두자.

2025~2026년 시점의 시장 신호는 어느 한 방향으로 강하게 기울어 있다. TypeScript가 GitHub 월간 기여자 기준 1위를 차지하면서 JavaScript와 Python을 제쳤다. Node.js 백엔드 채용 공고의 약 65%가 TypeScript를 요구하거나 선호한다고 표시한다. NestJS는 TypeScript 전용 프레임워크로 자리 잡았다. 한국 시장만 봐도 당근마켓이 5개 언어 폴리글랏에서 Go·TypeScript 양대 스택으로 정리하면서 채용 공고의 그래프가 Rails 대비 TS로 뚜렷하게 기울었다. 줌인터넷·인프랩·직방 같은 회사의 1차 회고가 모두 같은 방향으로 정리된다.

그렇다고 Spring 경력이 평가절하되는 건 아니다. 정반대다. 한국의 빅테크 — 카카오페이·우아한형제들·쿠팡·네이버 본진 — 는 여전히 Spring/Java가 본진이고, 결제·금융 도메인은 어디서나 JVM이 신뢰의 근거로 자리 잡고 있다. 네이버파이낸셜이 Node MSA를 도입하면서도 결제·금융 영역은 Spring을 같이 운영하는 폴리글랏 모델을 골랐다는 점이 그 균형을 잘 보여준다. Spring 시니어의 시장 가치는 떨어지지 않았다. 다만 옆자리에 Node/TS가 한 칸 더 들어왔을 뿐이다.

본인이 Spring 시니어라고 해보자. 두 번째 런타임을 갖는다는 건 어떤 시장 지점에 도달한다는 뜻인가. 셋으로 정리할 수 있다.

첫째, 폴리글랏 조직의 시니어/리드 자리. 당근마켓·네이버파이낸셜·인프랩 같은 회사가 이미 그 모양이다. 한 사람이 Spring 본진과 Node BFF를 동시에 읽고 결정할 수 있는 자리. 시니어 한 명의 연봉이 Spring만 하는 시니어보다 위에 자리 잡는 영역이다. 한국 시장에서 두 진영을 다 경험한 시니어는 흔치 않아서, 채용 측 입장에서는 한 명을 잡으면 두 자리가 한꺼번에 메워지는 효과가 있다.

둘째, BFF·Edge·서버리스 영역의 전문성. Cloudflare Workers, Vercel Edge Functions, AWS Lambda 같은 환경은 Node가 사실상 1급 시민이다. Spring Boot의 GraalVM Native Image와 SnapStart가 빠르게 따라잡고 있지만, 콜드 스타트 200밀리초 이하의 즉응성은 Node 쪽이 자연스럽다. 이 영역의 BFF·Edge 아키텍처를 설계해본 경험은 Spring만 한 시니어가 가지기 어려운 별도의 줄이다.

셋째, 마이그레이션·아키텍처 컨설팅. 같은 결정 — Spring에서 Node로 한 조각을 떼어낼지, 어디에 BFF를 둘지, modular monolith부터 시작할지 — 를 내려본 사람은 점점 드물어진다. 8장에서 본 결정 회로 자체가 시장에서 평가되는 자리에 있다. 사내 컨설팅이든, 외부 어드바이저든, 같은 결정을 다른 팀에 옮겨주는 일은 시니어가 자기 다음 단계로 가져가기 좋은 줄이다.

물론 두 번째 런타임을 갖는다는 게 곧 더 많은 일을 한다는 뜻은 아니다. Spring 깊이는 줄어들 수 있다. 한 사람이 두 진영의 모든 디테일을 같은 깊이로 알 수는 없다. 그래서 한 진영을 본진으로 두고, 다른 진영은 손에 익은 두 번째 도구로 갖는 모양이 가장 흔하다. Spring 본진 + Node 도구든, Node 본진 + Spring 도구든, 어느 쪽이든 같은 자리에 도달한다 — "이 결정은 어느 도구에 맡겨야 하는가"를 본인의 손으로 판단할 수 있는 시니어.

이 책을 여기까지 읽은 본인은 이미 그 자리로 한 발 옮긴 상태다. 1장의 의심 — 단일 스레드 런타임이 정말 우리 일감을 감당할 수 있는가 — 을 가지고 들어왔다면, 9장 이 자리에서 답이 거의 손에 잡혔을 것이다. 감당한다. 단 조건이 있다. 그 조건들이 무엇인지를 1~8장이 한 줄씩 깔아주었다.

## Bun·Deno의 위치 — 2026년 시점에 알아둘 옵션

이 책은 Node를 다룬다. 다만 Node 옆자리에 두 개의 다른 런타임이 빠르게 자라고 있다는 사실은 정직하게 알려두자. Bun과 Deno다. 이 두 개를 두 페이지 안에서 정직하게 위치 지어두자.

**Bun.** Jarred Sumner가 만든 JavaScript 런타임. V8이 아니라 JavaScriptCore(WebKit)를 깔고, 자체 패키지 매니저·번들러·테스트 러너를 묶어둔 단일 바이너리다. 가장 큰 셀링 포인트는 두 가지. 하나, Node API를 거의 호환한다는 점 — `npm install`을 `bun install`로 바꾸기만 해도 Express나 Fastify 앱이 그대로 돈다. 둘, 패키지 설치와 시작 시간이 자릿수 단위로 빠르다. Node 진영에서 빌드·테스트 사이클을 짧게 가져가고 싶은 팀이 CI 파이프라인의 일부 단계에서 Bun을 쓰기 시작했다. 운영에서 메인 런타임으로 쓰는 사례는 아직 신중한 단계지만, 내부 도구·CLI·스크립트·테스트 러너 자리에서는 Node를 빠르게 대체하고 있다.

```bash
# Node와 Bun이 한 자리에서 보여주는 모습 — 같은 일을 다른 도구로
node app.js
bun app.js

npm install            # Node + npm
bun install            # Bun — 패키지 설치가 자릿수 단위로 빠르다

jest                   # Node의 테스트 러너
bun test               # Bun 내장 테스트 러너
```

Java 출신이 알아둘 정도는 이 정도다. "Node 호환 런타임으로 빠르게 자라는 중. 메인 런타임으로 옮길 결정은 아직 신중히, 다만 빌드·테스트·CLI 자리에서는 시도해볼 가치가 있다."

**Deno.** Node의 원작자 Ryan Dahl이 Node에서 후회한 결정들을 다시 짠 런타임이다. 철학이 다르다. 기본적으로 모든 권한이 거부되어 있고 — 파일 읽기를 하려면 `--allow-read`를 명시해야 한다 — TypeScript를 1급으로 다루고, ESM과 표준 라이브러리에 무게중심을 둔다. Node와의 호환성은 v2 이후에 빠르게 좋아졌지만, 여전히 npm 생태계 일부와는 거리가 있다. Deno KV·Deno Deploy 같은 자체 플랫폼이 Edge 컴퓨팅과 잘 맞물려 있다. Java 출신이 알아둘 정도는 이렇다 — "보안과 표준을 우선한 설계. Cloudflare Workers·Deno Deploy 같은 Edge 영역에서 자연스럽게 자리 잡고 있다. Node 생태계와 다른 길을 가는 만큼 메인 백엔드의 기본 선택은 아직 아니지만, Edge·보안 민감 도메인에서는 검토할 가치가 있다."

이 책에서 Bun·Deno를 본문 어휘로 더 끌어오지 않은 이유는 단순하다. 2026년 시점에 한국 백엔드 팀이 두 번째 런타임으로 가장 자주 결정하는 대상은 여전히 Node + TypeScript + NestJS·Express·Fastify 조합이다. Bun과 Deno는 그 결정 다음에 오는 다음 결정의 자리에 있다. 본진을 잡고 나서 한 번씩 들여다보는 옵션으로 두자. 책 한 권을 다 읽은 다음 본인이 이 두 런타임의 1년 안 변화를 따로 추적해보는 것을 권한다.

## 다음 한 걸음 — 독자 유형별로 권하는 첫 액션

긴 산문이 끝났다. 책을 덮고 자리로 돌아갈 시점이다. 그 첫 한 걸음을 독자 유형별로 권한다.

**시니어 IC에게.** 다음 사이드 프로젝트를 NestJS + Prisma로 짜자. 일이 끝난 뒤 두 시간씩, 두 주만 투자해도 손에 충분히 들어온다. 모양은 단순하게 — 작은 REST API 한 개, Prisma로 PostgreSQL 한 테이블, Pino로 구조화 로깅, Jest로 단위 테스트 한 묶음. 사이드 프로젝트가 거창할 필요는 없다. 본인이 평소 쓰는 도구의 작은 자동화 — 가계부, RSS 리더, 책 관리, 자기 메모 백엔드 — 정도면 충분하다. 두 주가 끝나면 이 책의 1·2·4·5장이 손에 박혀 있을 것이다. 그 상태에서 6장의 디버깅 도구를 한 번씩 켜보자. `clinic doctor`로 본인 코드를 한 번 진단하고, Chrome DevTools로 heap snapshot을 한 번 찍어보고, `monitorEventLoopDelay`로 lag를 측정해보면, 7·8장의 운영·마이그레이션 어휘가 머리에서 손으로 옮겨온다.

**테크 리드에게.** 팀에서 가장 작은 BFF 한 조각을 골라 PoC로 만들어보자. 모양은 정해져 있다. Strangler Fig의 1단계 — API Gateway 한 개 세우고, 그 뒤에 모놀리스를 두고, 한 페이지의 트래픽만 새 NestJS BFF로 라우팅한다. 페이지 한 개만 옮기면 된다. PayPal이 시작했던 그 모양이다. 두 달 안에 mirroring → 1% canary → 5% → 25% → 100%까지 가는 게 현실적인 일정이다. 이 PoC가 끝나면 팀에는 두 가지 자산이 남는다. 하나는 실제 운영 데이터로 검증된 결정 — "우리 조직에서는 Node가 이런 조건에서 잘 도는구나" 또는 "이런 자리에는 안 맞는구나". 또 하나는 6주 학습 플랜의 첫 졸업생 한 명. 이 한 명이 다음 결정에서 본인의 가장 든든한 동지가 된다.

**아키텍트에게.** Strangler Fig 6개월 로드맵 초안을 그리자. 8장의 결정 시나리오를 본인 조직의 도메인 지도와 겹쳐 그려보면, 첫 6개월이 어떤 모양이 되어야 하는지가 손에 잡힌다. 1개월차 — 도메인 경계 도식화 + Node 6주 학습 플랜의 첫 사이클 시작. 2~3개월차 — 가장 작은 BFF 한 조각의 PoC, modular monolith 구조의 초기 골격(NestJS Monorepo). 4~5개월차 — 두 번째 모듈을 모듈로 추가, 운영 KPI 패널 구축(이벤트 루프 lag, heap 추세, unhandledRejection 카운트, 신규 엔지니어 첫 PR 시간). 6개월차 — 후퇴 신호 첫 회고. 이 회고에서 다음 6개월의 결정을 다시 내린다. 한 번에 큰 결정을 내리는 게 아니라, 6개월씩의 작은 결정을 반복해서 누적하는 모양이다. 이 모양이 Uber의 후퇴를 부끄럽지 않게 받아들일 수 있는 회로다.

세 유형 모두에게 한 가지 공통의 권유가 있다. 첫 한 걸음은 작아야 한다. 사이드 프로젝트는 작은 API 하나, PoC는 페이지 한 개, 로드맵은 6개월 초안 한 장. 9장 전체가 권하는 톤이 그것이다 — 큰 결정을 한 번에 내리지 말고, 작은 결정을 반복해서 누적하자. Node를 들이는 결정도 같은 모양으로 들어가야 그 안에 후퇴 회로가 자연스럽게 살아 있다.

## 닫는 말 — 1장의 의심에 대한 마지막 대답

1장 도입부에서 던졌던 의심을 다시 꺼낸다. "한 개 스레드만 도는 런타임이 어떻게 수만 커넥션을 감당할 수 있는가." 이 질문이 우리를 책 안으로 데리고 들어왔다. 1장에서 V8 + libuv의 구조를 보고, 이벤트 루프가 단계별로 도는 모습을 보고, 비동기 I/O가 OS 비동기 인터페이스로 풀리는 모습을 봤다. 거기서 추상의 가닥을 잡았다.

그 추상이 사례의 수치로 답해진 자리들이 본문 곳곳에 있었다. PayPal의 RPS 2배 + 응답 시간 35% 감소 + 코드 33% 감소. LinkedIn의 서버 30대 → 3대. Netflix의 시작 시간 40분 → 1분 미만. 줌인터넷의 TPS 약 40% 상승 + 메모리 50% 이상 감소 + 코드 71% 축소. 당근마켓의 푸시알림 1,500 RPS 누락 없는 처리. 이 다섯 줄이 1장의 의심에 대한 첫 대답이었다 — "감당한다."

다만 그 대답이 전부가 아니다. Uber의 2018년 후퇴가 같은 자리에 있어야 한다. Node로 시작한 RTAPI가 신규 엔지니어 온보딩 비용 때문에 권장 스택에서 빠진 사례. 이 한 줄이 우리의 정직한 두 번째 대답이다 — "단 조건이 있다."

그 조건들이 무엇인지를 본문이 한 줄씩 깔아주었다. 이벤트 루프를 막지 마라(1장). 타입 안전을 단계적으로 도입하라(2장). 패턴은 비교 가능하다(3장). NestJS는 Spring 패턴을 그대로 받아준다(4장). Prisma의 명시적 트랜잭션·`include`/`select`를 받아들여라(5장). 디버깅 도구의 자리는 JVM과 1:1 매핑된다(6장). graceful shutdown·구조화 로깅·OTel·헬스체크·lag 모니터를 첫날부터 깔아라(7장). BFF부터 시작해 Strangler Fig로 점진 이전하라(8장). PR 리뷰의 다섯 함정을 알고 들어가라, modular monolith부터 시작해라, 후퇴 신호를 분기마다 측정하라(9장). 이 한 줄씩이 모여서 "단 조건이 있다"의 그 조건을 채운다.

그러니까 1장의 의심에 대한 마지막 대답은 이 모양이다 — **감당한다, 단 조건이 있다. 그리고 그 조건은 우리가 Spring에서 이미 길러놓은 백엔드 직관과 거의 같은 모양이다.** 동시성을 어떻게 다루느냐, 운영 사고를 어떻게 측정하느냐, 마이그레이션을 어떻게 점진적으로 하느냐 — 이 질문들의 답은 도구가 바뀌어도 거의 같다. 이름만 바뀐다. `@Transactional`이 `prisma.$transaction`이 되고, `MDC`가 Pino + correlation id가 되고, `@Async`가 `async/await`이 되고, JFR이 `clinic flame`이 된다. 도구만 바뀌었을 뿐, 우리가 다루는 동시성 문제 자체는 같다. 1장 끝에서 박았던 그 한 줄이 9장 끝에서 다시 살아 돌아온다.

이제 책을 덮을 시간이다. 다만 책 한 권은 끝이 아니다. 두 번째 런타임을 갖는다는 게 정확히 어떤 모양인지 — Spring과 Node가 한 팀에서 같이 도는 풍경, JVM의 Project Loom이 같은 동시성 문제를 다른 길로 풀어내는 모습, GraalVM Native Image와 SnapStart가 Spring Boot의 콜드 스타트 약점을 어디까지 메우는가, 그리고 이 모든 것이 우리 정체성에 어떤 의미인가 — 그 한 자리가 에필로그에 남아 있다. 9장이 결단의 자리였다면, 에필로그는 결단 다음의 정체성 자리다. 책장을 한 장만 더 넘기자.
