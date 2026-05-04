# 7장. 배포·운영·보안·CI/CD — 컨테이너 시대의 Node 운영 매뉴얼

Spring Boot 시절을 떠올려 보자. 빌드가 끝나면 손에 떨어지는 산출물은 단 하나, fat jar 한 덩이다. 그걸 운영 서버 어딘가에 던지면 JVM이 받아 든다. JVM 안에 들어가는 순간 클래스로더가 의존성을 묶어 들고, 임베디드 Tomcat이 포트를 열고, 서비스가 살아난다. 이 단순함이 우리에게 익숙한 모양이었다. CI에서 jar 한 개만 잘 만들면 운영의 절반이 끝났다는 직관. 운영 시스템에 굳이 Maven을 깔지 않아도 되고, 의존성 트리를 통째로 들고 가지 않아도 된다는 안심.

그렇다면 Node로 넘어오면 무엇이 달라질까. 처음 운영 서버에 배포할 자리를 잡는 자리에서 우리가 정직하게 마주치는 것은, **fat jar 같은 단일 단위가 없다**는 사실이다. Node 앱 한 덩이가 살아나려면 적어도 세 가지가 한 자리에 모여야 한다. Node 런타임, 우리가 짠 프로젝트 코드, 그리고 `node_modules` 트리. 그중 어느 하나라도 빠지면 앱은 시작조차 안 한다. fat jar의 그 단일성을 Node에서 다시 만들어 내려면 도구가 한 번 바뀐다. 그래서 사실상의 표준 단위가 된 것이 **Docker 이미지**다. "node:20-alpine 위에 우리 코드 올리고, `npm ci`로 `node_modules`를 굳혀 넣은 한 덩이의 이미지" — 이 모양이 우리 시대의 fat jar다.

이 한 가지 사고 전환만 받아 들어도, 이번 장의 절반은 이미 풀린 셈이다. fat jar의 자리에 Docker 이미지가 들어왔다면, 그 이미지를 누가 실행하고 누가 재시작시키고 누가 스케일링하느냐가 다음 질문이다. PM2가 그 자리를 잡을 때도 있고, Docker가 그 자리를 가져갈 때도 있고, Kubernetes가 통째로 떠맡을 때도 있다. 어디에 어느 도구를 쓰는 게 맞는지를 먼저 정리해 두자.

## PM2와 cluster, 그리고 Docker — 어디서 누가 일하는가

Node 운영 도구를 처음 보는 자리에서 가장 헷갈리는 이름이 셋이다. PM2 cluster, Node 표준 라이브러리의 `cluster` 모듈, 그리고 Docker. 셋 모두 "여러 인스턴스를 띄워 부하를 나눈다"라는 비슷한 일을 한다고 들리는데, 막상 같이 쓰면 충돌이 일어난다. 이 자리에서 Spring 출신이 흔히 던지는 질문 — "그럼 도커 안에서 PM2 cluster를 켜는 게 맞는가?" — 에 답하기 위해, 셋의 위치를 먼저 정확히 두자.

Node의 `cluster` 모듈은 표준 라이브러리에 있는 가장 낮은 층이다. 마스터 프로세스가 워커를 코어 수만큼 fork해, 같은 포트를 공유한 채 라운드 로빈으로 요청을 받는다. 단일 호스트에서 멀티 코어를 쓰자는 가장 원초적인 도구다. PM2는 그 위에 운영 친화적인 옷을 입힌 도구다. cluster 모드를 한 줄 명령으로 켜고, 죽으면 자동으로 재시작하고, 메모리 한계에 닿으면 그레이스풀하게 리로드하고, 로그를 한 자리에 모아 준다. PM2 한 가지로 "Node 단독 호스트에서 운영"이 거의 끝난다. Spring으로 치면 systemd + 임베디드 Tomcat의 조합 같은 자리다.

Docker는 그보다 한 층 위에 있다. 호스트와 격리된 한 덩이의 실행 환경을 잡아 주고, 호스트 OS와 무관하게 같은 모양으로 돈다. 그리고 그 위에 Kubernetes가 또 한 층 더 들어온다. 컨테이너를 모아 클러스터로 묶고, 죽으면 다시 띄우고, 부하에 맞춰 스케일링하고, 롤링 업데이트를 책임진다. 이 셋이 한 자리에 모이면 어디까지가 누구의 일이냐가 미묘해진다.

가장 자주 마주치는 함정 한 가지를 짚어 두자. **K8s 안에서 PM2 cluster를 켜고 있다면 거의 늘 잘못 짠 모양이다.** 왜 그럴까. K8s는 이미 재시작·스케일링을 책임지는 층이다. Pod이 죽으면 Deployment 컨트롤러가 다시 띄우고, 트래픽이 늘면 HPA가 Pod 수를 늘린다. 그 위에서 한 Pod 안에 PM2가 또 cluster 모드로 워커 4개를 fork한다면, K8s가 보는 것은 한 개의 Pod일 뿐이다. 한 워커가 메모리 누수로 OOM에 닿아도 PM2는 안에서 조용히 재시작할 뿐 K8s에는 보이지 않는다. 메트릭도 한 Pod 단위로 흐려진다. CPU 1코어 limit을 잡아 둔 Pod 안에서 워커 4개가 코어 4개를 노리며 다툰다.

이 자리에서 우리가 따라야 하는 직관은 **"한 컨테이너 한 프로세스"**다. K8s 안에서는 PM2 cluster를 빼고, Node 앱을 단일 프로세스로 띄운 다음, 더 많은 인스턴스가 필요하면 Pod 수를 늘린다. PM2가 책임지던 재시작·스케일링은 K8s가 그대로 받아 든다. PM2 자체가 의미를 잃는 자리다. 다만 PM2를 K8s 환경에서 아예 못 쓰는 건 아니다. PM2의 `pm2-runtime`을 단일 프로세스 모드로 쓰면, 로그 포맷이나 graceful shutdown 시그널 처리 같은 운영 편의를 가져갈 수 있다. 이때도 cluster 모드는 끄고, 워커 1개로 돌리는 모양을 잡자.

반대로 PM2 cluster가 빛나는 자리는, 컨테이너 없이 EC2 한 대 위에서 그대로 Node 앱을 띄우는 모양이다. 이 자리에서는 K8s가 없으니 PM2가 재시작·스케일링·graceful reload를 모두 책임진다. CPU 코어 8개짜리 호스트에서 `pm2 start app.js -i max`만 하면 워커 8개가 뜬다. 작은 팀에서 컨테이너 인프라 없이 빠르게 띄우는 자리에 손에 잘 맞는다. 다만 운영이 커질수록 결국 컨테이너로 옮겨 가게 되는데, 옮길 때 PM2의 자리가 자연스럽게 작아지는 흐름이라고 기억해 두자. 처음에는 PM2가 모든 일을 하지만, K8s에 들어가는 순간 운영의 본체가 K8s로 넘어간다.

## Dockerfile과 K8s Deployment — 최소 모양

운영 그림을 머리에서만 그리면 어느새 흐릿해진다. 손에 잡히는 모양으로 풀어 보자. Node + NestJS 앱 한 덩이를 컨테이너로 만들고, K8s에 띄우는 가장 작은 정직한 모양이다.

```dockerfile
# syntax=docker/dockerfile:1.6

# 1단계 — 빌드 스테이지
FROM node:20-alpine AS builder
WORKDIR /app

# 의존성 캐시 레이어 — package*.json만 먼저 복사
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# 소스 복사 + 빌드
COPY tsconfig*.json ./
COPY src ./src
RUN npm run build

# 운영 의존성만 다시 산출
RUN npm prune --omit=dev


# 2단계 — 런타임 스테이지
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# 비루트 유저로 실행 — 보안 기본값
RUN addgroup -S app && adduser -S -G app app
USER app

COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/package.json ./package.json

EXPOSE 3000
# tini를 PID 1로 — 시그널 전달과 좀비 프로세스 정리
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/main.js"]
```

이 짧은 Dockerfile에 Spring Boot 출신이 한 번에 받아들이기 어려운 디테일이 몇 가지 들어 있다. 하나씩 짚자. **멀티 스테이지 빌드**는 익숙할 것이다. Spring Boot도 layered jar + 멀티 스테이지로 운영 이미지를 작게 잡는 모양을 권장한다. Node는 그 필요가 더 절실하다. devDependency가 운영 이미지에 흘러들어 가면 이미지 크기가 두세 배로 부풀고, 공격 표면도 따라 커진다. `npm prune --omit=dev`로 운영용 의존성만 남기는 한 줄을 잊지 말자.

`tini`라는 작은 프로세스도 Spring Boot 시절에는 만나기 어려운 이름이다. 컨테이너에서 PID 1로 실행되는 프로세스에는 시그널 처리에 미묘한 책임이 따른다. Node를 그냥 PID 1로 띄우면 SIGTERM이 다른 프로세스에 잘못 전달되거나 좀비 프로세스가 정리 안 되는 함정이 일어난다. tini 같은 init이 PID 1을 가져가고, Node를 자식으로 띄우는 모양이 안전하다. node:20-alpine 베이스 이미지에는 tini가 기본 포함되어 있고, `--init` 플래그 없이도 ENTRYPOINT에서 호출하면 같은 효과를 얻는다. 작은 디테일이지만 graceful shutdown 절에서 다시 만난다.

비루트 유저로 실행하는 한 줄도 빼먹지 말자. Node 컨테이너의 디폴트가 root인 경우가 흔한데, 운영 자리에서는 거의 늘 비루트로 떨궈야 한다. K8s가 `runAsNonRoot: true`를 강제하는 자리도 점점 늘고 있다.

이 이미지를 K8s에 띄우는 Deployment의 최소 모양은 다음과 같다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  labels: { app: orders-api }
spec:
  replicas: 3
  selector:
    matchLabels: { app: orders-api }
  template:
    metadata:
      labels: { app: orders-api }
    spec:
      # SIGTERM 후 기본 30초까지 기다린다 — 진행 중 요청 마무리
      terminationGracePeriodSeconds: 45
      containers:
        - name: app
          image: registry.example.com/orders-api:1.4.2
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: production
          resources:
            requests: { cpu: "200m", memory: "256Mi" }
            limits:   { cpu: "1",    memory: "512Mi" }

          # liveness — "프로세스 자체가 살아 있는가"
          livenessProbe:
            httpGet: { path: /health/live, port: 3000 }
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3

          # readiness — "트래픽을 받을 준비가 되었는가"
          readinessProbe:
            httpGet: { path: /health/ready, port: 3000 }
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 2

          # PreStop — SIGTERM 직전에 readiness만 끊어 트래픽을 빼는 패턴
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 5"]

          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
```

이 한 장에 운영 디테일이 두꺼이 들어가 있다. 핵심만 짚자. **`terminationGracePeriodSeconds`**가 graceful shutdown의 시간 예산이다. K8s가 SIGTERM을 보낸 뒤 이 시간 안에 컨테이너가 스스로 종료하지 않으면 SIGKILL로 강제 종료한다. 디폴트가 30초인데, 진행 중 잡이 길게 도는 워커 컨테이너에서는 60초 ~ 120초까지 늘리는 자리도 흔하다. 이 시간 안에 우리가 짠 graceful shutdown 코드가 다 끝나야 한다.

**liveness vs readiness**는 Spring Actuator를 써 본 사람에게는 익숙할 것이다. liveness는 "프로세스 자체가 살아 있는가"를, readiness는 "트래픽을 지금 받을 준비가 되었는가"를 본다. 이 둘을 한 엔드포인트로 합쳐 두면 사고가 일어난다. 가령 외부 DB가 잠시 끊어졌을 때 readiness가 실패해 트래픽을 빼는 건 맞는 결정이지만, liveness까지 같이 실패해 Pod 자체가 재시작되는 건 과한 행동이다. 두 엔드포인트를 분리해 두자. NestJS에서는 `@nestjs/terminus`가 이 분리를 거의 한 줄로 만들어 준다.

**preStop hook + sleep 5**는 K8s 운영의 미묘한 함정 하나를 풀어 주는 작은 트릭이다. K8s가 Pod 종료를 시작할 때, 두 가지가 거의 동시에 일어난다 — Endpoints에서 Pod를 빼는 일과 컨테이너에 SIGTERM을 보내는 일. 이게 동시면 어떤 부하 분산기는 SIGTERM 받은 Pod에 새 요청을 잠시 더 보낸다. preStop에서 5초 정도 자면 그 사이에 Endpoints 갱신이 전파되어, SIGTERM이 도착하기 전에 새 트래픽이 끊어진다. 작은 디테일인데 운영 사고를 막아 준다.

## Graceful shutdown — Spring과 Node에서 같은 일을 다른 손으로

여기서 한 절을 통째로 빼서 다룰 만한 주제가 있다. **Graceful shutdown.** Spring Boot 2.3 이후로는 한 줄 설정으로 끝나는 일이지만 — `server.shutdown=graceful`을 application.properties에 넣으면 Tomcat/Undertow/Netty/Jetty가 모두 알아서 처리한다 — Node에서는 직접 짜야 한다. 첫 NestJS 프로젝트의 운영 사고 중 의외로 자주 보이는 자리가 여기다. 디플로이를 도는데 진행 중 요청 몇 건이 502로 끊어지고, DB 커넥션이 깨끗이 닫히지 않아 풀이 누수되고, 메시지 큐에서 ack를 돌리지 못한 메시지가 다시 살아나 중복 처리된다.

graceful shutdown의 흐름은 단순하다. **SIGTERM을 받는다 → HTTP 서버를 닫아 새 요청을 막는다 → 진행 중 요청이 끝날 때까지 기다린다 → DB 커넥션과 큐 컨슈머를 닫는다 → 진행 중 백그라운드 잡을 마무리한다 → 프로세스를 끝낸다.** 이 다섯 단계를 모두 시간 예산 안에 끝내야 한다. 코드로 풀면 NestJS에서는 다음 모양이 가장 정직하다.

```ts
// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, { bufferLogs: true });

  // 1. NestJS의 shutdown hook을 켠다
  app.enableShutdownHooks();

  await app.listen(3000);
}
bootstrap();
```

`enableShutdownHooks()` 한 줄이 NestJS에 SIGTERM·SIGINT 같은 종료 시그널을 들으라고 알려 준다. 이게 켜져 있으면, 모듈 안의 어느 프로바이더든 `OnApplicationShutdown` 인터페이스를 구현하면 종료 단계에서 호출된다. 그 위에 우리 손으로 정리할 자리들을 풀어 보자.

```ts
// graceful-shutdown.service.ts
import { Injectable, Logger, OnApplicationShutdown } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { JobQueue } from './job-queue.service';
import { HealthState } from './health-state.service';

@Injectable()
export class GracefulShutdownService implements OnApplicationShutdown {
  private readonly logger = new Logger('Shutdown');

  constructor(
    private readonly prisma: PrismaService,
    private readonly queue: JobQueue,
    private readonly health: HealthState,
  ) {}

  async onApplicationShutdown(signal?: string): Promise<void> {
    this.logger.log(`Shutdown signal: ${signal ?? 'unknown'}`);

    // 1. readiness만 먼저 false — K8s가 트래픽을 빼게 한다
    this.health.setReady(false);

    // 2. NestJS 자체가 HTTP 서버를 닫는 일은 자동
    //    (enableShutdownHooks가 app.close()로 흐른다)

    // 3. 큐 컨슈머 정지 — 진행 중 메시지는 ack까지 마무리
    await this.queue.drain({ timeoutMs: 20_000 });
    this.logger.log('Queue drained');

    // 4. DB 커넥션 정리
    await this.prisma.$disconnect();
    this.logger.log('Prisma disconnected');

    this.logger.log('Graceful shutdown complete');
  }
}
```

이 코드의 흐름이 곧 운영의 기억이다. 첫째, **readiness를 먼저 false로 떨어뜨린다.** 이게 가장 빠르게 K8s에 "이 Pod에 새 트래픽 보내지 말아 달라"고 알리는 손짓이다. 둘째, NestJS의 `app.close()`가 흐르며 HTTP 서버가 새 요청을 받지 않는다. Express/Fastify의 `server.close()`가 안에서 호출되어 진행 중 요청이 끝날 때까지 기다린다. 셋째, 큐 컨슈머가 새 메시지를 받지 않게 멈추고, 이미 받은 메시지는 ack를 돌릴 때까지 기다린다. 넷째, Prisma 커넥션 풀을 닫는다. 이 순서를 뒤섞으면 자잘한 사고가 난다. DB를 먼저 끊고 HTTP를 닫으면 진행 중 요청이 DB 에러로 흐르고, HTTP를 안 닫고 큐만 닫으면 큐 의존 요청이 깨진다.

PM2 환경이라면 한 가지 더 기억해 두자. **PM2의 디폴트는 SIGINT를 보내고 1.6초 후 SIGKILL이다.** 1.6초가 지나면 우리 graceful shutdown 코드가 끝나든 말든 PM2는 프로세스를 강제로 죽인다. 이 디폴트가 운영 환경에 너무 짧으면 `kill_timeout` 옵션을 ecosystem.config.js에서 늘려 주자. 기본 1600ms를 30000ms로 잡아 두면 K8s의 `terminationGracePeriodSeconds` 30초와 짝이 맞는다.

```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'orders-api',
    script: 'dist/main.js',
    instances: 1,           // K8s 안에서는 1, 단독 호스트에서는 'max'
    exec_mode: 'fork',      // K8s 안에서는 fork, 단독 호스트에서는 'cluster'
    kill_timeout: 30000,    // SIGINT 후 30초까지 대기
    listen_timeout: 10000,  // 시작 대기
    wait_ready: true,       // process.send('ready')를 기다린다
  }],
};
```

Spring Boot 2.3+의 `server.shutdown=graceful`이 한 줄로 끝나던 자리를 우리는 코드 한 페이지로 풀어 냈다. 처음에는 손이 무거워 보인다. 그러나 한 번 손에 익으면 이 명시성에 정직한 보상이 따른다. 어느 단계에서 무엇이 닫히는지가 코드에 보이고, 큐와 DB의 종료 순서를 우리가 직접 결정할 수 있다. Spring의 `@PreDestroy`가 가끔 일으키던 미묘한 함정 — 어떤 빈이 어떤 순서로 종료되는지가 흐릿한 자리 — 가 NestJS에서는 코드에 명시된다. 마법을 빼고 정직성을 들이는 트레이드오프다.

## 로깅 — Pino를 첫날부터 깔자

운영의 다음 자리는 로그다. Spring 시절의 우리 손에는 Logback이 있었다. logback-spring.xml에 appender 한 자리를 잡고, MDC에 trace_id를 넣고, JSON encoder로 stdout에 흘리고, fluentd나 Filebeat이 받아 ELK로 보냈다. 이 그림이 거의 그대로 Node로 옮겨 온다. 도구 이름만 바뀐다.

Node 진영의 두 강자는 **Pino**와 **Winston**이다. Spring 출신이 첫 번째로 받는 질문은 "어느 쪽을 디폴트로 깔까"인데, 답은 거의 항상 Pino 쪽이다. 숫자를 보자. 1만 라인 로그를 찍는 데 Pino는 ~115ms, Winston은 ~270ms 걸린다. 초당 처리량으로 환산하면 Pino가 ~50,000 logs/sec, Winston이 ~10,000 logs/sec쯤 된다. 다섯 배 차이다. 그것도 동기 호출 기준이고, Pino는 포매팅·전송을 워커 스레드로 분리하는 transport 모델이라 hot path에서 더 가볍다. Winston이 못 짠 게 아니라, Pino가 처음부터 "JSON을 stdout으로 가장 빠르게 쏘는 일"에 최적화되어 있다는 뜻이다. 컨테이너 시대의 로깅 모델 — "stdout으로 흘리고 인프라가 받는다" — 과 손이 잘 맞는 도구다.

Winston은 transport가 다양해서 Slack·이메일·Loggly 같은 외부로 직접 흘리고 싶을 때 골라드는 자리가 있다. 다만 이 시대에는 Slack 알림은 alerting 시스템에 맡기고 로그는 stdout 한 자리로 모으는 모양이 표준이라, Winston의 그 다양성이 빛나는 자리가 점점 줄어든다. 별 이유가 없으면 첫날부터 Pino를 깔자.

NestJS에서 Pino를 들이는 모양은 가장 일반적인 `nestjs-pino` 패키지 한 줄로 끝난다.

```ts
// app.module.ts
import { Module } from '@nestjs/common';
import { LoggerModule } from 'nestjs-pino';
import { randomUUID } from 'crypto';

@Module({
  imports: [
    LoggerModule.forRoot({
      pinoHttp: {
        level: process.env.LOG_LEVEL ?? 'info',
        // correlation id — 요청마다 부여
        genReqId: (req) =>
          (req.headers['x-request-id'] as string) ?? randomUUID(),
        customProps: (req) => ({
          // OpenTelemetry trace context — instrumentation-pino가 자동 주입하지만
          // 명시적으로 한 번 더 적어 둔다
          traceId: req['otelTraceId'],
          spanId: req['otelSpanId'],
        }),
        // 운영에서는 절대 pino-pretty를 켜지 말 것
        // JSON을 그대로 흘려 fluentd/Loki가 파싱하게
        transport: process.env.NODE_ENV !== 'production'
          ? { target: 'pino-pretty', options: { singleLine: true } }
          : undefined,
        redact: ['req.headers.authorization', 'req.headers.cookie', '*.password'],
      },
    }),
  ],
})
export class AppModule {}
```

이 짧은 설정에 운영의 손맛이 들어간다. 첫째, **correlation id**다. Logback + MDC에서 `MDC.put("traceId", id)`로 한 줄씩 넣던 그 자리가, Pino에서는 `genReqId`로 들어온다. 요청마다 UUID를 발급하거나 들어온 `X-Request-ID` 헤더를 그대로 쓴다. 같은 요청에서 흘러나오는 모든 로그 라인에 같은 id가 박혀, 추후 ELK/Loki에서 한 요청을 통째로 따라가기 쉽다.

둘째, **OpenTelemetry trace context 자동 주입**이다. `@opentelemetry/instrumentation-pino`를 한 번 켜 두면, 우리가 `logger.info({ orderId }, 'order placed')`라고 쓴 한 줄에도 `traceId`와 `spanId`가 자동으로 박혀 나온다. Logback의 `%X{traceId}` 패턴 한 줄로 풀던 일이, Node에서는 instrumentation 한 줄로 끝난다.

셋째, **redact**. Authorization 헤더나 비밀번호 필드가 로그에 흘러나가는 사고는 첫 번째 운영 사고로 거의 단골이다. Pino의 `redact` 옵션은 JSON path 기준으로 필드를 가린다. 첫날부터 깔아 두자.

운영에서 한 가지 더 기억할 자리는 **로그 파싱이 가능한 형태로 흘리는 것**이다. 개발 자리에서 보기 좋다고 pino-pretty 같은 transport를 운영에 켜 두면, 아까운 trace_id가 사람용 텍스트에 묻혀 fluentd가 파싱을 못 한다. 운영 환경에서는 항상 JSON을 그대로 stdout으로 흘리고, 사람용 가독성은 Loki/Kibana가 받아 든다. 이게 컨테이너 시대 로깅의 기본 모양이다.

OpenTelemetry instrumentation을 같이 깔아 두면 어떻게 되는지 한 단락만 더 보자. `@opentelemetry/sdk-node`와 `@opentelemetry/auto-instrumentations-node`를 깔고 startup에 한 번 init하면, HTTP·Express·NestJS·Prisma·ioredis 거의 전부가 자동으로 trace를 만든다. Datadog/New Relic/Dynatrace 같은 APM은 그 OTel 표준 위에 자기 backend를 받아 든다. Spring의 Micrometer + Actuator + 각 APM 에이전트가 풀던 자리를, Node에서는 OpenTelemetry SDK 한 묶음이 받아 든다. 사고 모형이 거의 같다 — auto-instrumentation으로 90%를 잡고, 도메인 로직은 직접 span을 쳐서 잡는다.

```ts
// otel.ts — Node 부팅 가장 처음에 require
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'orders-api',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.APP_VERSION,
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV,
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations({
    // pino 로그에 trace context를 자동 주입
    '@opentelemetry/instrumentation-pino': { enabled: true },
    // fs는 너무 잡음이 많아 보통 끈다
    '@opentelemetry/instrumentation-fs': { enabled: false },
  })],
});

sdk.start();

process.on('SIGTERM', () => sdk.shutdown().finally(() => process.exit(0)));
```

이 한 파일을 `node -r ./otel.ts dist/main.js` 식으로 가장 먼저 require하게 띄우면, Express 라우트 하나하나가 trace로 묶이고 Pino 로그에 `traceId`가 박힌다. Spring의 Micrometer Tracing이 풀던 자리를 한 페이지가 받아 든다.

## 헬스 체크 — liveness와 readiness를 분리하자

K8s Deployment YAML에 이미 두 엔드포인트를 적어 두긴 했지만, 그 안에서 어떤 일이 도는지를 NestJS 코드로 풀어 두자. Spring Actuator의 `/actuator/health`가 풀던 자리를, NestJS에서는 `@nestjs/terminus`가 그대로 받아 든다.

```ts
// health.controller.ts
import { Controller, Get } from '@nestjs/common';
import {
  HealthCheck, HealthCheckService,
  HttpHealthIndicator, MemoryHealthIndicator,
  PrismaHealthIndicator,
} from '@nestjs/terminus';
import { PrismaService } from './prisma.service';
import { HealthState } from './health-state.service';

@Controller('health')
export class HealthController {
  constructor(
    private readonly health: HealthCheckService,
    private readonly prismaIndicator: PrismaHealthIndicator,
    private readonly memory: MemoryHealthIndicator,
    private readonly http: HttpHealthIndicator,
    private readonly prisma: PrismaService,
    private readonly state: HealthState,
  ) {}

  // liveness — "프로세스 자체가 살아 있는가"만 본다
  @Get('live')
  @HealthCheck()
  liveness() {
    return this.health.check([
      // 메모리 한계만 본다 — DB가 끊어졌다고 Pod 재시작은 과하다
      () => this.memory.checkHeap('heap', 400 * 1024 * 1024),
    ]);
  }

  // readiness — "트래픽을 지금 받을 준비가 되었는가"
  @Get('ready')
  @HealthCheck()
  readiness() {
    if (!this.state.isReady()) {
      // graceful shutdown 시작했으면 즉시 not ready
      return this.health.check([() => Promise.reject({ ready: false })]);
    }
    return this.health.check([
      () => this.prismaIndicator.pingCheck('database', this.prisma),
      () => this.http.pingCheck('payment', 'https://payment.example.com/health'),
    ]);
  }
}
```

분리의 직관을 코드 위에서 다시 보자. liveness는 외부 의존성을 거의 안 본다. 메모리 누수처럼 "프로세스가 정말로 망가져 재시작 외에 답이 없는 자리"만 잡는다. readiness는 외부 의존성을 본다. DB가 끊어졌으면 트래픽을 빼야 하지만, Pod 재시작은 과한 행동이다. 이 분리를 일찍 잡지 않으면 운영 사고가 일어난다 — DB가 1분 끊어지자 Pod 50개가 동시에 재시작되어, 회복 후에도 cold start로 5분간 트래픽을 못 받는 그 흐름.

`HealthState` 같은 작은 토글 서비스를 둬 두면, graceful shutdown 시작 시점에 readiness만 끊는 일이 깔끔하게 된다. 앞에서 본 `GracefulShutdownService`가 `state.setReady(false)`만 부르면, 다음 readiness probe에서 503이 나가고 K8s가 트래픽을 뺀다.

## 서버리스의 운영 — Lambda 콜드 스타트의 자리

운영 그림에서 컨테이너만 보다가 자칫 빠뜨리기 쉬운 자리가 있다. **서버리스, 특히 AWS Lambda.** Spring Boot 출신이 처음 Lambda에 손대면 가장 먼저 만나는 벽이 콜드 스타트다. JVM이 부팅하고 Spring Context가 자라기까지 3 ~ 10초가 걸린다. SnapStart를 켜야 1.5초, 잘 다듬으면 180ms까지 떨어진다.

Node는 그 자리에서 정직하게 빛난다. 전형적인 콜드 스타트가 200ms 이하다. 같은 동기 사용자 API를 Lambda 위에 올렸을 때, Node는 Spring 대비 압도적으로 운영 친화적이다. 들쭉날쭉한 트래픽의 BFF, API Gateway 뒤의 사용자 페이지, 짧고 격렬한 이벤트 핸들러 — 이런 자리에서 Node + Lambda 조합은 거의 늘 좋은 결정이다. 앞서 본 사례들 중에서도 동기 사용자 API의 Lambda 적합도가 가장 높았던 자리가 PayPal·LinkedIn·Netflix BFF였다.

다만 Node + Lambda에도 운영 디테일이 있다. 콜드 스타트가 200ms라고 해도, 그게 누적되면 사용자 체감으로는 큰 차이를 만든다. 대표 패턴 두 가지를 짚어 두자.

첫째, **Provisioned Concurrency.** "워커 N개를 미리 데워 둬, 트래픽이 와도 콜드 스타트가 안 일어나게 하자"는 결정이다. 비용이 들지만 p99 지연이 절반 이상 줄어든다. 결제 API처럼 응답 지연이 매출과 직결되는 자리에서는 거의 늘 깔아 둔다.

둘째, **init phase 외부화.** Lambda의 init phase(handler 함수 첫 호출 전 모듈 import + 전역 코드 실행 시간)는 콜드 스타트의 본체다. 여기에 무거운 작업을 넣으면 안 된다. Prisma 같은 무거운 ORM 클라이언트의 인스턴스화, AWS SDK 클라이언트 다중 생성, 환경 변수 파싱이 한 번에 다 init phase에 깔리면 200ms가 800ms로 부풀 수 있다. 무거운 클라이언트는 lazy 초기화로 빼고, 모듈 import는 트리 셰이킹이 잘 되는 도구(esbuild)로 줄이자. esbuild 통합은 CI/CD 절에서 다시 만난다.

Spring SnapStart가 풀던 "JVM 워밍업의 고통" 자체가 Node에서는 작아진 자리이고, 그 자리에서 우리가 신경 쓰는 디테일은 결이 다르다. Node에서는 init phase의 한 줄 한 줄이 비용이고, Spring에서는 GC와 JIT 워밍업이 비용이다. 도구가 바뀌었을 뿐, 우리는 여전히 콜드 스타트와 싸우고 있다.

## 보안 — Spring Security의 자리를 누가 받아 드는가

여기까지가 운영 본체였다. 분량의 절반이 넘게 운영 도구를 풀었으니, 이번에는 보안 자리를 들여다보자. Spring 시절의 우리 손에는 Spring Security가 있었다. `WebSecurityConfigurerAdapter`(또는 SecurityFilterChain) 한 자리에 필터 체인을 잡고, 인증 매니저를 끼우고, JWT 필터를 추가하고, `@PreAuthorize`로 메서드 권한을 잡고, OAuth2 Client로 SSO를 붙였다. 이 한 묶음을 NestJS에서 다시 짜야 할 때 가장 먼저 던지는 질문이 있다. "JWT 가드는 어떻게 짜는가."

답은 정직하게 말해, **Spring Security만큼 한 묶음으로 잡혀 있는 도구는 Node에 없다.** 대신 Helmet · Passport.js · `@nestjs/passport` · `@nestjs/throttler` · npm audit · Snyk · Dependabot 같은 도구가 각자의 자리에서 합쳐져 같은 그림을 만든다. 손이 한 번 늘어난다. 다만 손이 늘어난다는 건 우리가 짠 보안 기능이 코드에 보인다는 뜻이기도 하다. Spring Security의 한 자리에 들어가 있던 그 많은 기본값들이 Node에서는 명시적으로 흘러나온다. 마법이 빠진 자리에 정직성이 들어왔다.

먼저 가장 낮은 층, **HTTP 헤더 보안**부터 잡자. Helmet 한 패키지가 그 자리를 받아 든다. NestJS에서는 한 줄이다.

```ts
// main.ts (보안 부분)
import helmet from 'helmet';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        // 정적 자산을 CDN에서 받으면 그 호스트를 화이트리스트에
        imgSrc: ["'self'", 'data:', 'https://cdn.example.com'],
      },
    },
    // HSTS — HTTPS만 받겠다고 브라우저에 알린다
    hsts: { maxAge: 31_536_000, includeSubDomains: true, preload: true },
    // X-Frame-Options, X-Content-Type-Options, Referrer-Policy 등은 디폴트로 적용
  }));

  app.enableCors({
    origin: ['https://app.example.com', 'https://admin.example.com'],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    credentials: true,
    maxAge: 600,
  });

  await app.listen(3000);
}
bootstrap();
```

Helmet은 Spring Security의 `headers()` DSL이 한 자리에 모아 두던 헤더 보안을 한 번에 풀어 준다. CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy 같은 헤더가 디폴트로 잡히고, 우리는 도메인에 맞춰 조금만 다듬는다. 첫날부터 깔자. 안 깔면 사고가 일어나는 자리가 아니라, 사고가 일어났을 때 우리 책임이 분명해지는 자리다.

CORS는 Spring `WebMvcConfigurer.addCorsMappings`(또는 `@CrossOrigin` 어노테이션)이 풀던 자리를 NestJS의 `app.enableCors()`가 거의 그대로 받는다. 화이트리스트 도메인을 적고, 메서드를 적고, credentials를 잡는다. 사고 방식이 같다.

다음은 인증·권한이다. **JWT vs 세션**의 결정이 첫 번째 갈림길이다. Spring Security 시절에는 SecurityContextHolder + HTTP 세션이 디폴트였고, JWT는 `OncePerRequestFilter`를 직접 짜거나 `oauth2-resource-server`로 풀었다. NestJS에서는 거의 모든 신규 프로젝트가 JWT 쪽으로 간다. stateless API 게이트웨이가 시대의 모양이고, 마이크로서비스 사이에서 세션 공유는 비싼 결정이다.

JWT 가드의 모양은 `@nestjs/passport` + `passport-jwt`가 받아 든다.

```ts
// auth/jwt.strategy.ts
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';

interface JwtPayload {
  sub: string;     // userId
  email: string;
  roles: string[];
  iat: number;
  exp: number;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET,
      // 또는 비대칭 키:
      // secretOrKeyProvider: passportJwtSecret({
      //   jwksUri: 'https://auth.example.com/.well-known/jwks.json',
      //   cache: true, rateLimit: true,
      // }),
    });
  }

  async validate(payload: JwtPayload) {
    // 여기서 반환하는 객체가 req.user로 들어간다
    return { id: payload.sub, email: payload.email, roles: payload.roles };
  }
}

// auth/jwt-auth.guard.ts
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}

// auth/auth.module.ts
import { Module } from '@nestjs/common';
import { PassportModule } from '@nestjs/passport';
import { JwtModule } from '@nestjs/jwt';
import { JwtStrategy } from './jwt.strategy';

@Module({
  imports: [
    PassportModule.register({ defaultStrategy: 'jwt' }),
    JwtModule.register({
      secret: process.env.JWT_SECRET,
      signOptions: { expiresIn: '15m' },
    }),
  ],
  providers: [JwtStrategy],
  exports: [JwtModule, PassportModule],
})
export class AuthModule {}
```

Spring Security의 `JwtAuthenticationFilter`가 풀던 자리를, Passport 전략 한 클래스가 그대로 받아 든다. Bearer 토큰 추출 → 시크릿/JWKS로 서명 검증 → payload 파싱 → `validate()`에서 user 객체 산출. 그 user 객체가 `req.user`에 들어가 가드 통과 후 컨트롤러에서 그대로 쓸 수 있다. Spring Security 출신에게는 흐름이 거의 같다.

가드를 컨트롤러에 적용하는 모양도 익숙하다.

```ts
@Controller('orders')
@UseGuards(JwtAuthGuard, RolesGuard)
export class OrdersController {
  @Get()
  @Roles('user')
  findMine(@Req() req) {
    return this.ordersService.findByUser(req.user.id);
  }

  @Delete(':id')
  @Roles('admin')
  delete(@Param('id') id: string) {
    return this.ordersService.delete(id);
  }
}

// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  canActivate(ctx: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<string[]>('roles', [
      ctx.getHandler(), ctx.getClass(),
    ]);
    if (!required?.length) return true;
    const { user } = ctx.switchToHttp().getRequest();
    return required.some((r) => user.roles?.includes(r));
  }
}
```

Spring Security의 **`@PreAuthorize("hasRole('ADMIN')")`**이 한 줄로 풀던 권한이, NestJS에서는 `@Roles('admin')` + `RolesGuard` 두 자리로 갈라진다. 메타데이터 데코레이터가 메서드에 달리고, 가드가 그 메타데이터를 읽어 결정한다. 손이 한 번 늘긴 하지만, 한 번 짜 두면 도메인 권한 표현식까지 자유롭게 늘릴 수 있다. Spring SpEL 표현식의 자리에 우리 손으로 짠 가드가 들어온다.

OAuth는 Passport.js의 어댑터가 받아 든다. `@nestjs/passport` + `passport-google-oauth20`(또는 `passport-github2`, `passport-azure-ad` 등) 한 묶음으로, Google·GitHub·회사 SSO를 거의 같은 모양으로 붙인다. Spring Security OAuth2 Client의 `application.yml` 한 자리가 풀던 일을, Passport 전략 한 클래스가 받는다. 사고 모형이 거의 같다 — provider 등록 → callback URL → 사용자 정보 fetch → 우리 시스템의 user 모델로 매핑.

다음은 **Rate Limiting**이다. Spring 진영의 Bucket4j나 Resilience4j RateLimiter가 풀던 자리를 NestJS에서는 `@nestjs/throttler`가 받아 든다. Express만 쓰는 자리에서는 `express-rate-limit`이 같은 자리다.

```ts
// app.module.ts (rate limit 부분)
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';

@Module({
  imports: [
    ThrottlerModule.forRoot([
      { name: 'short', ttl: 1000, limit: 10 },     // 초당 10건
      { name: 'long',  ttl: 60_000, limit: 200 },  // 분당 200건
    ]),
  ],
  providers: [
    { provide: APP_GUARD, useClass: ThrottlerGuard },
  ],
})
export class AppModule {}

// 컨트롤러 단에서 한 번 더 강제 — 결제 API는 더 빡빡하게
@Controller('payments')
export class PaymentsController {
  @Throttle({ short: { ttl: 1000, limit: 2 } })  // 초당 2건만
  @Post()
  create(/* ... */) {}
}
```

Bucket4j의 토큰 버킷 알고리듬과 사고 방식이 거의 같다. 윈도 안에서 N번까지 허용하고, 초과하면 429를 돌려준다. Redis 기반의 분산 throttler를 쓰면 여러 인스턴스에서 같은 한도를 공유한다 — `@nestjs/throttler` + `nestjs-throttler-storage-redis` 조합이다. Spring의 분산 RateLimiter 사고와 결이 같다.

마지막으로 **의존성 취약점 스캔**이다. Spring 진영의 OWASP `dependency-check` Maven 플러그인이 풀던 자리를, Node에서는 세 도구가 분담한다. **`npm audit`**은 표준 라이브러리 격으로, npm registry의 advisory DB와 lock 파일을 비교해 취약점을 알려 준다. **Snyk**은 그 위에 자동 수정 PR과 정책 관리·라이선스 검사 같은 운영 친화 기능을 얹은 SaaS다. **Dependabot**은 GitHub의 봇으로, 취약 의존성에 대해 자동으로 PR을 만들어 올린다.

운영 자리에서는 셋을 같이 쓰는 모양이 흔하다. CI에서 `npm audit --audit-level=high`로 PR 단계에서 막고, Snyk이나 Dependabot이 자동 PR을 올리고, 사람이 그 PR을 승인하는 흐름. CI 통합은 다음 절(CI/CD)에서 한 번 더 만난다.

이 보안 한 묶음이 첫 NestJS 프로젝트의 첫 주에 다 들어가 있어야 하는 자리다. Helmet, CORS, JWT 가드, Roles 가드, Throttler, npm audit. 일곱 가지가 안 깔린 채로 운영에 들어가는 일은 없게 하자. Spring Security가 한 자리에 모아 두던 그 안전망을 우리 손으로 일곱 자리에 분산해 짠 셈이지만, 짜 두면 코드에 보인다. 이 명시성을 보안의 보상으로 받자.

## CI/CD — Maven `verify`가 펼쳐 놓은 자리를 다시 짜다

운영의 마지막 자리, CI/CD를 짚자. Spring 시절의 우리 손에는 Maven이나 Gradle이 있었다. `mvn clean verify`나 `./gradlew build` 한 줄에 dependency resolution → compile → unit test → integration test → static analysis → 패키징까지가 다 묶여 있었다. 한 명령에 한 단계. 자료가 잘 정리된 도구의 강점이다.

Node로 오면 그 한 줄이 명시적인 체이닝으로 펼쳐진다. `npm ci && npm run lint && npm test && npm audit && npm run build` 같은 모양이다. 같은 일을 하는데, 단계가 코드에 보인다. 손이 늘어난 만큼 우리가 짠 파이프라인의 모양도 보인다. 그 펼쳐진 모양을 GitHub Actions YAML에 풀면 다음 한 장이 된다.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  build-test-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'  # 또는 'npm', 'yarn'

      - run: corepack enable
      - run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm run lint

      - name: Type check (tsc, no emit)
        run: pnpm exec tsc --noEmit

      - name: Test
        run: pnpm run test:cov

      - name: Audit
        run: pnpm audit --audit-level=high

      - name: Snyk scan
        uses: snyk/actions/node@master
        env: { SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }} }
        with: { args: --severity-threshold=high }

      - name: Build (esbuild)
        run: pnpm run build  # tsup 또는 esbuild

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to registry
        uses: docker/login-action@v3
        with:
          registry: registry.example.com
          username: ${{ secrets.REG_USER }}
          password: ${{ secrets.REG_PASS }}

      - name: Build & push multi-arch image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            registry.example.com/orders-api:${{ github.sha }}
            registry.example.com/orders-api:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

이 한 장을 한 줄씩 풀어 두자. **`actions/setup-node@v4`의 `cache: 'pnpm'`**은 Spring 진영의 Maven dependency cache와 사고 방식이 같다. lockfile 해시를 키로 의존성 캐시를 잡고, lockfile이 안 바뀌었으면 install 단계가 거의 즉시 끝난다. 처음부터 안 깔면 매 PR마다 `pnpm install`이 1분씩 도는 끔찍한 일이 일어난다. Maven `~/.m2`의 자리가 GitHub Actions cache로 옮겨 온 셈이다.

**`tsc --noEmit`**으로 타입 체크와 빌드를 분리하는 모양도 한 번 짚자. tsc 한 도구에 다 맡기면 빌드가 분 단위로 늘 수 있다. 체크는 tsc로, 실제 컴파일은 esbuild·SWC로 갈라 두는 게 시대의 모양이다. **esbuild는 Go로 짠 번들러**고, SWC는 Rust로 짠 컴파일러다. 둘 다 tsc 대비 30 ~ 50배 빠르다고 알려진다. 작은 NestJS 프로젝트도 tsc 1분에서 esbuild 5초로 쉽게 떨어진다. 큰 모노레포에서는 그 차이가 사람 시간을 직접 줄인다.

esbuild를 NestJS 프로젝트에 깔 때 자주 쓰는 모양은 `tsup` 같은 래퍼다. 가장 작은 설정은 다음 한 자리다.

```ts
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/main.ts'],
  outDir: 'dist',
  target: 'node20',
  platform: 'node',
  format: ['cjs'],
  bundle: true,
  splitting: false,
  sourcemap: true,
  clean: true,
  // NestJS의 동적 import를 깨뜨리지 않게 일부는 외부로
  external: ['@nestjs/microservices', '@nestjs/websockets', 'class-transformer/storage'],
});
```

`pnpm run build` 한 명령이 dist에 main.js 한 덩이를 떨군다. tsc만으로 풀던 빌드가 십수 배 빨라진다. Spring 진영의 incremental compile 만큼 빠른 자리를 우리도 받아 들인 셈이다.

**멀티 아키텍처 Docker 이미지**도 시대의 자리다. 개발자 노트북은 ARM64(Apple Silicon)인데 운영 클러스터는 amd64이거나, 그 반대인 자리가 늘었다. `docker buildx` + QEMU 한 묶음이면 amd64/arm64 두 이미지를 한 번에 산출해 같은 태그로 푸시한다. Spring Boot Buildpacks가 풀던 자리와 사고 방식이 같다. 한 이미지가 두 아키텍처를 모두 받아 든다.

**자동 보안 스캔의 CI 통합**도 위 YAML에 같이 들어가 있다. `pnpm audit --audit-level=high`가 PR 단계에서 한 번 막고, Snyk action이 한 번 더 막는다. 두 도구가 보는 advisory DB가 약간 달라 두 번 거르는 자리다. Spring 진영의 OWASP `dependency-check` Maven 플러그인이 한 자리에서 풀던 일을, Node에서는 두 도구로 갈라 둔다. 손이 늘긴 했지만 한 번 더 안전망이 두꺼워진 셈이다.

마지막으로 한 가지 더 짚자. **Maven의 `verify`가 한 명령에 묶었던 단계들이 Node에서는 명시적 체이닝으로 풀린다**고 했다. 손이 한 번 늘어난다는 단점은 분명하지만, 보상도 분명하다. 어느 단계에서 무엇이 도는지가 YAML에 보인다. Maven plugin 안의 어떤 페이즈에 어떤 goal이 묶여 있는지를 머릿속에 들고 있어야 했던 그 자리가, Node에서는 줄 단위로 코드에 흐른다. CI 사고가 났을 때 어디를 봐야 하는지가 거의 늘 분명하다. 마법을 빼고 정직성을 들이는 트레이드오프, 이번 장에서 다섯 번째 만나는 모양이다.

## 첫날부터 깔 자리, 정리

여기까지가 운영의 본체였다. 한 챕터에 너무 많은 도구가 들어왔으니, 우리가 첫 NestJS 프로젝트의 첫 주에 깔아 둬야 할 자리들을 산문으로 한 번 풀고 닫자.

먼저 프로세스 자리. **graceful shutdown 코드를 첫날에 깔자.** SIGTERM 받으면 readiness false → HTTP close → 큐 drain → DB 끊기 → exit. NestJS에서 `enableShutdownHooks()` + `OnApplicationShutdown` 인터페이스 한 묶음이면 한 페이지로 끝난다. Spring Boot의 `server.shutdown=graceful`이 한 줄이던 자리에서 손이 늘어나는 만큼, 우리 손으로 명시적으로 단계를 짠다.

다음으로 관측 자리. **구조화 로깅을 첫날에 깔자.** Pino + correlation id + OpenTelemetry trace context 자동 주입. 1만 라인 100ms 안쪽으로 도는 빠른 도구를 처음부터 들이자. `pino-pretty`를 운영에 켜는 함정만 피하면 된다. JSON을 stdout으로 그대로 흘리는 게 컨테이너 시대의 디폴트다. Logback + MDC가 풀던 자리를 Pino + OTel이 그대로 받아 든다.

**OpenTelemetry SDK도 첫날에 켜자.** Datadog/New Relic/Dynatrace 어느 backend로 보낼지는 나중에 결정해도, OTel SDK + auto-instrumentation을 일찍 깔아 두면 backend는 갈아 끼우는 자리가 된다. Spring의 Micrometer + Actuator가 풀던 자리다.

**liveness와 readiness를 분리해 두자.** `@nestjs/terminus`로 두 엔드포인트를 따로 짠다. liveness는 메모리 같은 프로세스 자체만 보고, readiness는 외부 의존성을 본다. K8s 시대의 운영 안전망이다. Spring Actuator의 `/actuator/health/liveness`와 `/actuator/health/readiness`를 그대로 옮긴 모양이다.

**이벤트 루프 lag 모니터링을 깔자.** `@nestjs/terminus`의 readiness에 lag 임계값(예: 200ms)을 넣어 두면, lag이 튀는 순간 readiness가 빠진다. 이벤트 루프를 막는 코드(sync 파일 I/O, 큰 JSON.parse, 정규식 backtracking)는 1장에서 본 그 함정이다. 운영 자리에서 직접 잡아 둘 자리다.

보안 자리. **Helmet + CORS를 첫날에 깔자.** HTTP 헤더의 안전망이다. **JWT 가드 + Roles 가드를 첫날에 짜자.** stateless API 시대의 인증·권한이다. **Throttler를 첫날에 켜자.** 분당 200건, 초당 10건 같은 디폴트 한도가 있어야 한 사용자의 폭주가 시스템 전체를 안 흔든다. **`npm audit`을 CI에 깔자.** PR 단계에서 high 이상 취약점을 막는다.

빌드·배포 자리. **multi-arch 이미지를 첫날에 산출하자.** `docker buildx`로 amd64/arm64를 한 번에. 노트북과 운영 클러스터의 아키텍처가 다른 시대의 디폴트다. **Snyk 또는 Dependabot 자동 PR을 깔자.** 의존성 패치가 사람의 손이 닿기 전에 PR로 올라와 있는 모양이다.

이 열 자리를 산문으로 풀었으니, 손에 닿게 한 번 더 표로 정리해 두자.

| 자리 | 첫날에 깔 도구 | Spring 시절의 자리 |
|---|---|---|
| graceful shutdown | NestJS `enableShutdownHooks` + `OnApplicationShutdown` | `server.shutdown=graceful` |
| 구조화 로깅 | Pino + correlation id + nestjs-pino | Logback + MDC |
| 분산 트레이싱 | OpenTelemetry SDK + auto-instrumentation | Micrometer Tracing |
| liveness / readiness | `@nestjs/terminus` (분리) | Spring Actuator (분리) |
| 이벤트 루프 lag | terminus의 lag indicator | (해당 없음 — JVM은 GC) |
| HTTP 헤더 보안 | Helmet | Spring Security `headers()` |
| 인증·권한 | `@nestjs/passport` JWT + Roles 가드 | Spring Security + `@PreAuthorize` |
| Rate Limiting | `@nestjs/throttler` | Bucket4j / Resilience4j |
| 의존성 스캔 | `npm audit` + Snyk + Dependabot | OWASP dependency-check |
| 멀티 아키텍처 이미지 | `docker buildx` + QEMU | Spring Boot Buildpacks |

이 표 한 장이 7장 한 챕터의 운영 결론이다. Spring 시절에 손에 익은 자리들이 거의 빠짐없이 Node 도구로 매핑된다. 도구 이름이 한 번씩 바뀐 것뿐이다. **우리가 풀고 있는 운영 문제 자체는 같다.** graceful shutdown은 graceful shutdown이고, MDC는 correlation id이고, Actuator는 Terminus다. 직관이 그대로 통한다는 사실이 이 챕터의 가장 큰 보상이다.

## 마무리 — 운영의 모양은 같다, 도구가 바뀌었을 뿐

7장은 fat jar 한 덩이를 던지던 운영의 그림이 Docker 이미지 + K8s Deployment 한 장으로 옮겨 가는 자리에서 시작했다. PM2와 cluster와 Docker의 위치를 정리했고, K8s 안에서 PM2 cluster를 빼야 하는 이유를 봤고, Dockerfile과 K8s Deployment의 최소 모양을 한 페이지에 잡았다. Graceful shutdown을 NestJS의 `enableShutdownHooks` + `OnApplicationShutdown`으로 풀었고, Spring Boot 2.3+의 한 줄이 우리 손에서는 한 페이지가 되는 트레이드오프를 정직하게 봤다.

로그 자리에서는 Pino를 첫날에 깔자고 했다. Winston의 다섯 배. 컨테이너 시대의 stdout 모델과 손이 잘 맞는 도구. correlation id와 OpenTelemetry trace context를 한 묶음으로 들이고, redact로 비밀번호 사고를 막고, 운영에서는 pino-pretty를 끄고. Logback + MDC가 풀던 그림이 그대로 옮겨 온다. APM은 OpenTelemetry SDK 위에 Datadog이든 Dynatrace든 골라 끼우는 모양으로 잡혔다. Micrometer가 풀던 자리다. Terminus가 Actuator를 받았고, liveness와 readiness를 분리했다.

보안 자리에서는 Spring Security 한 묶음이 NestJS의 일곱 자리로 풀려 나가는 모양을 봤다. Helmet, CORS, JWT 전략, Roles 가드, Throttler, npm audit, Dependabot. 손이 한 번 늘긴 했지만, 우리가 짠 보안 기능이 코드에 보이는 보상을 받았다. CI/CD 자리에서는 Maven `verify` 한 줄이 npm 명령 다섯 줄로 펼쳐지는 모양을 봤다. esbuild·SWC가 tsc의 분 단위 빌드를 초 단위로 떨어뜨렸고, `docker buildx`가 멀티 아키텍처 이미지를 한 번에 만들었다. Snyk과 Dependabot이 의존성 PR을 자동으로 올렸다.

이 모든 도구가 한 자리에 모이는 그림은, 결국 같은 일을 다른 손으로 다시 짠 것이다. **Spring Boot fat jar 한 덩이의 단순함이 사라진 자리에, Docker 이미지 한 장의 명시성이 들어왔다.** 우리가 풀고 있는 문제는 같다 — 들어오는 요청을 잘 처리하고, 죽어 가는 프로세스를 우아하게 닫고, 사고를 빠르게 발견하고, 사용자 권한을 정확히 검증하고, 의존성 취약점을 일찍 잡는 일. Spring 시절의 직관이 거의 그대로 통하는 자리이고, 도구의 이름이 한 번씩 바뀐 것뿐이다. 이 챕터의 보상이다.

다만 솔직히 말해 두자. 이 모든 운영 자리가 첫 NestJS 프로젝트에 한 번에 들어가지는 않는다. 첫 운영의 어느 한 자리에서는 늘 사고가 일어난다. 우리가 첫 graceful shutdown을 짜다가 큐 drain 단계에서 timeout이 부족했고, readiness 분리를 안 해 둬서 DB 1분 끊김에 Pod 50개가 동시에 재시작했고, JWT 시크릿을 환경 변수에 잘못 박아 둬서 토큰 검증이 무너졌다. 이 사고들이 하나씩 학습이 되고, 다음 프로젝트에서는 첫날부터 들이는 자리로 자란다. 운영은 늘 그런 식으로 손에 붙는다.

도구가 바뀌었다고 해서 우리가 운영 백엔드 개발자가 아닌 게 아니다. 컨테이너 시대의 도구를 손에 들고도, 우리는 여전히 graceful shutdown을 신경 쓰고, 로그에 trace_id를 박고, 헬스 체크를 분리하고, JWT를 검증하고, 의존성 스캔을 CI에 건다. **도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다.** 이 책의 처음부터 우리가 들고 온 메시지가, 운영 자리에서 가장 정직하게 다시 한 번 확인되는 챕터다.

이제 한 걸음 더 나아가자. 우리가 도구를 손에 익혔으니, 그 도구를 들고 어디서 어디로 옮겨 갈 것인가 — 가 다음 질문이다. 8장은 책의 절정이다. PayPal, LinkedIn, Netflix, Walmart, Uber, 그리고 당근마켓. 우리가 1·3·4·6·7장에서 짧게 만났던 사례들이, 결정 차원에서 한 자리에 모인다. Spring 모놀리스의 어디부터 잘라 NestJS 서비스를 옆에 둘 것인가, 어떤 신호가 보이면 멈춰야 하는가. Strangler Fig 패턴이 5단계로 풀리고, anti-corruption layer가 들어오고, BFF부터 시작하라는 권고가 코드 한 페이지로 잡힌다. 7장에서 우리가 손에 익힌 운영 도구는, 8장의 마이그레이션을 떠받치는 토대다. 운영을 못 짜는 팀은 마이그레이션을 못 한다. 다음 장으로 넘어가자.
