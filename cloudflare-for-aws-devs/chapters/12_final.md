# 12장. AI·Workflows·Queues — Step Functions·SQS·`@Scheduled` 너머

이런 상황을 한번 가정해보자. 결제가 끝나면 영수증 PDF를 만들고, 그 PDF를 R2에 올린 뒤 사용자에게 이메일로 보내고, 30분 뒤 후속 안내 메일을 한 번 더 보내는 sequence를 짜야 한다. 익숙한 답은 Step Functions다. ASL JSON 한 덩어리를 그리고, Lambda를 다섯 개 묶고, IAM role 다섯 개를 따로 관리하고, CDK 스택에 얹는다. 코드와 워크플로 정의가 두 곳에 분리돼 있어 디버깅할 때마다 두 화면을 번갈아 봐야 한다. 그러다 누군가 옆에서 묻는다. "근데 그 30분 sleep 동안에도 state transition이 돈으로 잡히지?" 한 달 청구서를 떠올리면 살짝 찜찜하다.

그 찜찜함을 한 번 풀어보자. 같은 sequence를 이번에는 Workers 위에서 짠다고 해보자. 코드 한 파일에 step을 줄줄이 적고, 30분 sleep은 비용 0으로 처리되고, 영수증 발송은 Queue로 분리하고, 매시 정각에 도는 health check는 cron 한 줄로 붙는다. AI Gateway 한 겹을 끼워 OpenAI에 먼저 던져보고 실패하면 Workers AI로 fallback한다. 이 그림이 실제로 가능한지, 가능하다면 어디까지 production에 견디는지가 이 장의 주제다.

이 장은 다섯 파트로 길게 간다. Workflows로 Step Functions의 자리를 다시 채우고, Queues로 SQS의 자리를, Cron Triggers로 Spring `@Scheduled`·EventBridge Scheduler의 자리를 채운다. 그 위에 Workers AI·Vectorize·AI Gateway라는 세 도구를 더 얹어, 작은 RAG 챗봇과 fallback 체인까지 한 사이클을 그린다. 분량이 길지만, 각 파트가 독립적으로 읽혀도 된다. 호흡을 한 번씩 끊으며 따라오자.

---

## Part 1. Workflows — Step Functions를 코드로 다시 그리기

### Step Functions 한 달 청구서를 떠올려 보자

먼저 ASL의 무게부터 짚고 가자. Step Functions로 상태 머신을 짜본 사람이라면 알 것이다. 한 step씩 JSON으로 정의하고, Choice·Parallel·Map·Wait를 조합하고, ResultPath로 입출력을 넘긴다. 표현력은 풍부하다. 그런데 가격 모델이 한 번 거슬린다. **state transition 단위로 과금**된다. Standard workflow는 1,000 transition당 $0.025. 그래서 long-poll, 30분 대기, 사람이 승인할 때까지 기다리는 step도 시간이 길어질수록 비용에 잡힌다 — 정확히는 "transition 횟수"에 잡히지만, 워크플로가 길고 step이 많을수록 그 횟수가 누적된다.

여기에 ASL의 또 한 가지 무게가 있다. 코드와 정의가 분리된다. Lambda 함수 다섯 개의 코드는 TypeScript로 짰는데, 이걸 묶는 워크플로는 별도 JSON에 들어 있다. 디버깅하다 보면 머리가 두 화면을 왔다 갔다 한다. 로컬에서 step 하나를 돌려보려면 Lambda 단위로 돌리거나, AWS Toolkit에서 시뮬레이션하거나, 결국엔 stage에 배포해 놓고 콘솔에서 입력 JSON을 던진다. 익숙해지면 쓸 만하지만, 익숙해지는 데까지의 거리가 멀다.

**Cloudflare Workflows는 이 두 가지 무게를 다른 방식으로 푼다.** 코드와 정의를 한 곳에 둔다. 그리고 외부 대기 시간은 비용에 잡지 않는다. 하나씩 살펴보자.

### Durable execution이 무엇인가

Workflows를 이해하려면 한 단어를 먼저 짚어야 한다. **durable execution**. 우리말로 "영속 실행" 정도가 된다. 무슨 뜻인가? 워크플로 인스턴스가 실행 도중 어딘가에서 죽어도, 다시 살아나서 **다음 step부터** 이어 돌릴 수 있다는 뜻이다. 마지막으로 끝낸 step의 결과는 영속 저장소에 적혀 있고, 새 인스턴스는 그 결과를 읽어 다음 step으로 넘어간다.

Step Functions가 이미 같은 일을 한다. Temporal·AWS Durable Functions·Inngest 같은 도구들도 같은 카테고리다. Workflows는 이 패턴을 Cloudflare 식으로 — V8 isolate 위에서 — 재구현한 것이다. 차이는 **인터페이스**에 있다. ASL JSON 대신 TypeScript 코드 한 파일이다.

```ts
import { WorkflowEntrypoint, WorkflowEvent, WorkflowStep } from "cloudflare:workers";

type Params = { orderId: string; email: string };

export class ReceiptWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const { orderId, email } = event.payload;

    const order = await step.do("verify-order", async () => {
      return await this.env.DB.prepare("SELECT * FROM orders WHERE id = ?")
        .bind(orderId).first();
    });

    const pdfUrl = await step.do("render-receipt-pdf", async () => {
      const pdf = await renderReceiptPdf(order);
      const key = `receipts/${orderId}.pdf`;
      await this.env.R2.put(key, pdf);
      return `https://files.toby-shop.example/${key}`;
    });

    await step.do("send-receipt-email", async () => {
      await this.env.MAIL_QUEUE.send({ to: email, kind: "receipt", url: pdfUrl });
    });

    await step.sleep("wait-30-minutes", "30 minutes");

    await step.do("send-followup-email", async () => {
      await this.env.MAIL_QUEUE.send({ to: email, kind: "followup", orderId });
    });
  }
}
```

코드를 한 줄씩 살펴보자. `step.do(name, async () => { ... })` — 이 한 묶음이 한 step이다. 이름과 동작 함수를 같이 넘긴다. 함수가 끝나고 반환된 값은 영속 저장소에 적힌다. 인스턴스가 도중에 죽어도, 다시 살아날 때 이 step은 적힌 결과를 그대로 읽고 다음으로 넘어간다. 즉 **`step.do` 안의 코드는 멱등(idempotent)이거나, 이미 끝난 step은 다시 실행되지 않는다는 가정 위에 짜야 한다.** 기억해두자 — 한 step 안에서 같은 부수효과를 두 번 만들면 안 된다. 결제·이메일·외부 API 호출 같은 위험한 부수효과는 step 단위로 깔끔히 떨어뜨리자.

`step.sleep("wait-30-minutes", "30 minutes")` — 이게 이번 장의 주연 중 하나다. 30분을 기다린다. 그 30분 동안 워커가 살아 있을까? 그렇지 않다. 인스턴스는 잠들어 있다가, 30분 뒤에 다음 step부터 다시 살아난다. **그 30분 동안 CPU는 0이고, 비용도 0에 가깝다.** Step Functions였다면 state transition이 누적되는 자리에서 Workflows는 가격이 사실상 사라진다. long-poll·승인 대기·후속 알림 같은 시나리오가 많을수록 가격 격차가 커진다.

`step.waitForEvent` 같은 API도 있다 — 외부에서 특정 이벤트가 도착할 때까지 기다리는 step이다. 사람이 승인할 때까지, webhook이 도착할 때까지, 또 다른 워크로드가 신호를 보낼 때까지 기다린다. 이 자리도 마찬가지로 비용 0이다.

### Step Functions ↔ Workflows 한 페이지 매핑

머리에 그림 하나로 박아두자.

| 개념 | Step Functions | Workflows |
|---|---|---|
| 정의 형식 | ASL JSON | TypeScript 코드 |
| step 정의 | `Task` state | `step.do(name, fn)` |
| 분기 | `Choice` state | 그냥 `if` |
| 병렬 | `Parallel` state | `Promise.all([step.do(...), step.do(...)])` |
| 반복 | `Map` state | `for` 루프 + `step.do` |
| 대기 | `Wait` state | `step.sleep("...", "30 minutes")` |
| 외부 이벤트 | Task token | `step.waitForEvent` |
| 과금 | state transition 수 | 실행 중 CPU time만 |

ASL의 표현력 중 한 가지가 사라졌다는 점은 짚어야 한다. **AWS 서비스 통합**이다. Step Functions에는 200+ AWS 서비스 액션이 ASL 안에서 직접 호출 가능한 형태로 들어 있다. SNS publish, S3 putObject, DynamoDB UpdateItem 같은 호출을 Lambda 없이 한 줄로 적을 수 있다. Workflows에는 그런 통합이 없다 — 외부 호출은 step 안에서 SDK·fetch로 직접 적는다. 코드 한 줄이 늘어난다고 보면 된다. 다만 Bindings가 빛나는 자리이기도 하다. R2·D1·KV·Queue·Service binding이 `this.env.X`로 그대로 쓰이니, "AWS 서비스 통합 200개"는 없어도 Cloudflare 안에서의 통합은 매끄럽다.

### Workflows를 어떻게 시작하나

`wrangler.toml`에 한 묶음 적어주면 된다.

```toml
name = "toby-shop-jobs"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[workflows]]
name = "receipt-workflow"
binding = "RECEIPT"
class_name = "ReceiptWorkflow"
```

이제 다른 Worker에서 이 워크플로를 시작하려면 한 줄이다.

```ts
const instance = await env.RECEIPT.create({
  params: { orderId: "ord-1234", email: "user@example.com" },
});
console.log("workflow id:", instance.id);
```

대시보드에 가면 인스턴스 목록·각 step의 상태·실패 step의 stack trace가 보인다. 실패한 step은 자동 재시도된다 — backoff 정책도 step 단위로 설정 가능하다. 어떤 step에서 retry exhaust가 나면 인스턴스 자체가 멈추고, 우리가 이어서 처리할 수 있는 상태로 남는다.

retry 정책을 한 step에 붙이려면 두 번째 인자로 옵션 객체를 넘기면 된다.

```ts
await step.do(
  "send-receipt-email",
  {
    retries: { limit: 5, delay: "10 seconds", backoff: "exponential" },
    timeout: "1 minute",
  },
  async () => {
    await this.env.MAIL_QUEUE.send({ to: email, kind: "receipt", url: pdfUrl });
  }
);
```

이 옵션이 Step Functions의 `Retry` 필드와 1:1로 대응한다. 차이는 — 한 곳에 코드와 retry 정책이 함께 있다는 것뿐이다. 디버깅할 때 두 화면을 왔다 갔다 하지 않아도 된다.

### 가격 모델 비교 — 30분 sleep이 왜 게임 체인저인가

이 자리에서 한 번 숫자로 짚자. 위 영수증 sequence를 한 달에 100,000건 처리한다고 해보자. 한 sequence에 step 5개, 그 중 한 개가 30분 sleep이다.

**Step Functions Standard 가정.** 한 sequence가 약 8번의 state transition을 만든다(Task entry/exit, Wait entry/exit 포함). 100,000건 × 8 transition = 800,000 transition. 1,000 transition당 $0.025로 계산하면 월 $20 정도. 작아 보이는가? 그러면 sequence를 길게 만들고, sleep을 늘리고, 재시도를 늘려보자. transition은 그만큼 누적된다. 그리고 sleep 동안 state는 영속 저장소에 머물러 있다 — Step Functions는 그 저장 자체에 또 비용을 잡지는 않지만, 같은 state machine이 동시에 수만 개 떠 있는 시나리오에서는 운영 한도를 신경 써야 한다.

**Workflows 가정.** 한 sequence의 실제 CPU 시간은 sleep을 빼면 수백 ms 안쪽이다. CPU time × 요청 수 모델이라 — sleep 30분은 비용에 잡히지 않는다. 같은 100,000건이라도 청구서는 일반 Workers 호출 100,000건 + step storage 비용 일부에 가깝다. 정확한 단가는 공식 페이지에서 확인해야 하지만, **체감으로 한 자릿수 낮은 자리**에 있다.

이 가격 격차가 sleep이 길고 재시도가 많은 워크로드에서 폭이 가장 크다. 인간 승인 대기 30분, webhook 도착 대기 1시간, 후속 알림 24시간 같은 sequence라면 Workflows의 가격 모델이 분명한 우위를 잡는다. 반대로 sleep 없이 빠르게 끝나는 짧은 sequence라면 격차가 작다 — 그쪽은 가격보다 "코드와 정의가 한 곳에 있다"는 멘탈 모델 이득이 더 크다.

### 무너지는 자리 — Workflows의 한계

이 책이 광고서가 아닌 이상, 무너지는 자리도 함께 짚자.

- **AWS 서비스 통합 자체가 깊은 워크플로**는 옮기는 비용이 만만치 않다. ASL의 `arn:aws:states:::dynamodb:updateItem.waitForTaskToken` 같은 깊은 통합 시나리오는 Workflows에서 그대로 옮길 등가물이 없다. Step Functions에 묶인 이력이 길수록 옮기는 일이 부담스럽다.
- **거대한 batch**는 부적합이다. Workflows는 짧은 multi-step orchestration에 어울린다. 30분짜리 ETL을 한 step에 욱여넣는 일은 잘못된 자리다. 그쪽은 ECS/Fargate 또는 Spring Batch가 그대로 더 잘 푼다 (5장 결정 프레임을 다시 펼쳐 보자).
- **lock-in**도 정직하게. Workflows의 `step.do`·`step.sleep` API는 Cloudflare 고유다. Temporal로 옮긴다면 비슷한 멘탈이지만 코드는 다시 짜야 한다. 다만 "ASL JSON에 lock-in되는 것"과 "TypeScript 함수에 lock-in되는 것"의 무게는 다르다. 코드는 결국 함수다 — 옮기기는 어렵지만, 구조 자체는 portable한 모양으로 남는다.

---

## Part 2. Queues — SQS의 자리를 채우다

### 큐는 왜 필요한가, 다시 한 번

이런 자리를 떠올려 보자. 우리가 방금 짠 `ReceiptWorkflow`의 `send-receipt-email` step. 이메일 발송은 외부 SMTP 또는 Resend·SendGrid 같은 외부 API를 부른다. 잠깐 외부 API가 흔들리면? 워크플로의 step.do가 실패하고, 자동 retry된다. 그래도 안 되면 워크플로 인스턴스가 그 자리에서 멈춘다. 이메일 한 통 때문에 결제 후 sequence 전체가 멈추는 그림은 살짝 끔찍하다.

그래서 옛날부터 답이 정해져 있었다. 메일은 **큐**에 넣고, 큐에서 따로 도는 consumer가 하나씩 빼서 발송한다. SQS를 써본 사람이라면 익숙한 그림이다. producer는 메시지를 던지고, consumer는 polling 또는 push로 받아 처리한다. 처리 실패하면 retry, 그래도 안 되면 dead-letter queue로 격리.

Cloudflare Queues는 이 모델을 그대로 옮겨온 도구다. 다만 Cloudflare 식으로 한 겹 가볍다. 어떻게 가볍냐면 — **producer와 consumer가 둘 다 Worker**다. polling을 우리가 짤 필요가 없다. SQS 콘솔에서 "이 큐를 trigger로 묶어 Lambda를 호출"하던 단계가 Queues에서는 wrangler 설정 한 줄로 끝난다.

### Producer와 consumer 한 사이클

producer Worker는 한 줄이면 된다.

```ts
await env.MAIL_QUEUE.send({
  to: "user@example.com",
  kind: "receipt",
  url: "https://files.toby-shop.example/receipts/ord-1234.pdf",
});
```

`env.MAIL_QUEUE`는 `wrangler.toml`에 producer binding으로 적어둔 이름이다.

```toml
[[queues.producers]]
binding = "MAIL_QUEUE"
queue = "mail-outbound"
```

consumer Worker는 별도 모듈이다. 같은 큐를 consumer로 등록한다.

```toml
[[queues.consumers]]
queue = "mail-outbound"
max_batch_size = 25
max_batch_timeout = 5
max_retries = 3
dead_letter_queue = "mail-dlq"
```

코드는 이런 모양이다.

```ts
export default {
  async queue(batch: MessageBatch<MailJob>, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      try {
        await sendMail(msg.body, env);
        msg.ack();
      } catch (err) {
        msg.retry({ delaySeconds: 30 });
      }
    }
  },
};
```

코드 한 줄씩 살펴보자. `batch.messages`는 한 번에 여러 메시지를 받아 처리할 수 있는 묶음이다. `max_batch_size: 25`이면 최대 25건을 한 호출에서 다룬다 — Worker invocation 비용이 한 번으로 묶이니, 처리량이 높을수록 단가가 떨어진다. `msg.ack()`는 성공 처리, `msg.retry({ delaySeconds: 30 })`은 30초 뒤 다시 시도. `max_retries`만큼 실패하면 자동으로 dead-letter queue(`mail-dlq`)로 넘어간다.

DLQ 자체도 또 하나의 Queue다. 따로 consumer를 붙여 슬랙 알림·운영자 inbox로 흘려보내거나, 정해진 주기로 다시 꺼내 재처리할 수 있다.

### SQS와 비교 — 어디가 같고 어디가 다른가

| 기준 | SQS | Cloudflare Queues |
|---|---|---|
| 메시지 본문 한도 | 256KB (SQS Standard) | 128KB |
| 보존 기간 | 최대 14일 | 기본 4일 |
| ordering | 기본 X (FIFO 큐 별도) | 기본 X, partial ordering 옵션 |
| 가격 | 요청 수 + payload | 작업 수 (operation) |
| consumer | Lambda trigger 또는 polling | Worker queue handler |
| egress | AWS 안에서는 무료, 밖으로 나가면 비용 | 무료 |
| dead-letter queue | 지원 | 지원 |
| retry/visibility timeout | 지원 | 지원 |

Queues 가격 감각을 한 줄로 잡자면 — 쓰기·읽기·삭제를 합친 "operation" 단위 과금이고, 무료 plan 한도 안에서 hobby·MVP에 충분하다. 정확한 단가 표는 공식 페이지에서 확인하자 (Cloudflare는 가격 모델이 자주 미세 조정된다).

본문 한도가 SQS보다 작다는 점은 한 번 짚어야 한다. 128KB. 큰 payload는 R2에 올리고, Queue에는 R2 key만 던지는 패턴으로 풀면 된다. 사실 SQS도 256KB를 넘으면 같은 패턴(S3에 본문 저장 + 메시지에 key 포함)을 써왔다. 한도 차이가 멘탈을 크게 흔들지는 않는다.

그리고 한 가지 더 — **strict global ordering은 보장하지 않는다.** Queues는 partial ordering 옵션을 제공하지만, "전 세계에서 보낸 순서대로 정확히"를 약속하지 않는다. 결제 처리·은행 거래 같은 strong ordering이 진짜 필요한 자리라면 SQS FIFO가 더 정직한 선택이고, 더 깊이 가면 Durable Objects 안에 큐를 직접 그리는 패턴이 있다 (8장에서 다룬 actor 모델 기억하자). 일반적인 작업 큐 — 이메일·이미지 변환·webhook fan-out — 에는 Queues의 ordering 모델로 충분하다.

### Batch consume와 throughput 한 번 더

batch 사이즈를 어떻게 잡을지가 한 번 더 짚을 자리다. `max_batch_size: 25`가 기본 권장에 가깝다. 한 번 호출에서 25건을 처리하면 Worker invocation 비용이 25분의 1로 떨어진다. SMTP 호출 같은 외부 의존이 있는 작업이라면 한 batch 안에서 `Promise.allSettled`로 동시에 던지는 패턴이 자연스럽다.

```ts
async queue(batch: MessageBatch<MailJob>, env: Env) {
  const results = await Promise.allSettled(
    batch.messages.map((msg) => sendMail(msg.body, env))
  );

  results.forEach((r, i) => {
    const msg = batch.messages[i];
    if (r.status === "fulfilled") {
      msg.ack();
    } else {
      msg.retry({ delaySeconds: 30 });
    }
  });
}
```

`max_batch_timeout: 5` — 큐에 메시지가 25건이 차지 않더라도 5초가 지나면 그 시점까지 모인 메시지를 묶어 호출한다. throughput이 작은 자리에서 latency가 너무 길어지지 않게 잡는 안전장치다.

DLQ로 빠진 메시지를 어떻게 다룰지도 한 번 정해두자. 흔한 패턴 두 가지다.

첫째, **DLQ도 또 하나의 consumer를 붙여 슬랙·이메일로 알림 + 운영자 대시보드에 적기**. 사람이 한 번 보고 손으로 재시도할지 폐기할지 정한다. 결제·이메일 같은 자리에 어울린다.

둘째, **DLQ에서 정해진 주기로 다시 메인 큐로 복귀**. cron trigger가 매시 정각에 DLQ를 비우며 메인 큐로 다시 던지는 패턴. 일시적 외부 장애가 풀리고 나서 자동으로 따라잡는 자리에 어울린다.

어느 쪽이든 — DLQ를 만들어 두고 끝이 아니라 **DLQ 자체에도 후속 절차가 있어야 한다**. DLQ에 메시지가 쌓이는데 아무도 안 보는 상황은 끔찍한 일이다. 그건 큐를 안 쓰는 것보다 더 위험하다.

### Workflow와 Queue를 같이 쓰면

이 자리에서 한 가지 분명히 해두자. **Workflows와 Queues는 경쟁이 아니라 짝꿍이다.** Workflows는 "이 sequence를 한 멘탈로 추적하고 싶다"는 자리에 어울린다. Queues는 "이 작업 단위를 fire-and-forget으로 떠넘기고 싶다"는 자리에 어울린다. 결제 sequence 자체는 Workflow로 그리고, 그 안에서 이메일 발송이라는 외부 의존이 강한 한 부분만 Queue로 떼어내는 그림이 가장 깔끔하다.

이 그림을 정리하면 우리의 영수증 sequence는 이렇게 흐른다.

```
[결제 webhook] → ReceiptWorkflow.create()
                     │
                     ├─ verify-order (D1 SELECT)
                     ├─ render-receipt-pdf (R2 put)
                     ├─ send-receipt-email → MAIL_QUEUE.send()
                     │                            │
                     │                            └─ MailWorker (consumer, retry, DLQ)
                     ├─ sleep 30 minutes (비용 0)
                     └─ send-followup-email → MAIL_QUEUE.send()
```

Workflow가 큰 흐름을 영속적으로 잡고, Queue가 외부 의존이 깊은 한 작업의 retry·DLQ를 책임진다. 각자 잘하는 자리에 둔다.

### 무너지는 자리 — Queues의 한계

- **strict global ordering** 미보장. 진짜로 순서가 중요한 워크로드는 SQS FIFO 또는 DO 안의 큐 패턴으로 가는 편이 낫다.
- **본문 128KB 한도**. R2 + key 패턴으로 우회 가능하지만, 한 번 짚어두자.
- **per-queue throughput 한도**가 있다. 초당 수천 건 수준에서는 충분하지만, 초당 수십만 건이 필요한 워크로드라면 Cloudflare 영업과 한도 상향을 협의하거나, 큐를 분할 운영하는 패턴이 필요하다.
- **producer/consumer가 같은 Cloudflare 안**이라는 가정. AWS Lambda를 그대로 두고 그 Lambda가 Cloudflare Queue를 consume하려면 Workers 한 겹을 더 둬야 한다 (HTTP pull API도 있지만, 그쪽은 polling 모델로 회귀한다).

---

## Part 3. Cron Triggers — `@Scheduled`의 자리

### 매시 정각에 도는 코드 한 줄

이런 그림을 가정해보자. 매시 정각에 외부 health check를 한 번 돌고, 5xx가 일정 비율을 넘으면 슬랙으로 알림을 쏘는 작은 작업. Spring을 써왔다면 손이 자연스럽게 `@Scheduled(cron = "0 0 * * * *")` 한 줄로 간다. AWS에서는 EventBridge Scheduler에 Lambda를 묶거나, EventBridge rule을 cron 표현식으로 잡아 Lambda를 trigger한다.

Cloudflare에서는 이 자리를 **Cron Triggers**가 받는다. `wrangler.toml`에 한 묶음 적어주면 된다.

```toml
[triggers]
crons = ["0 * * * *", "*/15 * * * *"]
```

cron 표현식 두 개. 첫 번째는 매시 정각, 두 번째는 15분마다. 이 한 줄이 EventBridge rule + IAM role + Lambda permission + ARN 문자열을 한꺼번에 대신한다.

코드 쪽은 Worker의 `scheduled` handler에 적는다.

```ts
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    if (event.cron === "0 * * * *") {
      ctx.waitUntil(runHealthChecks(env));
    } else if (event.cron === "*/15 * * * *") {
      ctx.waitUntil(syncFeed(env));
    }
  },

  async fetch(request: Request, env: Env) {
    return new Response("ok");
  },
};
```

`event.cron`이 어떤 trigger가 발화했는지 알려준다. `ctx.waitUntil(...)`은 응답 후에도 비동기 작업을 끝까지 마치도록 하는 한 줄 — 9장·10장에서 이미 만났다. 한 Worker가 여러 cron을 갖되 분기 처리를 한 곳에서 하는 패턴이 깔끔하다.

### `@Scheduled` ↔ Cron Trigger 매핑

| 개념 | Spring `@Scheduled` | EventBridge Scheduler | Cron Trigger |
|---|---|---|---|
| 정의 위치 | 코드 어노테이션 | IaC + 콘솔 | `wrangler.toml` |
| cron 형식 | Spring cron (6필드) | UNIX cron (5/6필드) | UNIX cron (5필드) |
| 실행 환경 | JVM 안 | Lambda invocation | Worker invocation |
| 다중 schedule | 메서드마다 | rule마다 | 한 Worker에 N개 |
| 분기 | 메서드별 자동 | rule input으로 | `event.cron` 분기 |
| timezone | JVM TZ | timezone 옵션 | UTC 기본 |

기억해둘 한 가지 — **Cron Trigger의 cron 표현식은 UTC 기준**이다. 한국 시각으로 매일 오전 9시에 도는 보고서를 짜고 싶다면 `0 0 * * *` (UTC 0시 = KST 9시) 식으로 변환해 적자. 익숙해지면 자연스럽지만, 처음에는 한 번 헷갈린다.

또 하나 — 단일 invocation에 CPU time 한도가 적용된다. 보고서 한 통 돌리는 정도라면 충분하지만, 큰 batch ETL을 cron 한 방에 욱여넣는 일은 적합하지 않다. 그쪽은 Workflows로 step을 쪼개거나, ECS Fargate에 두는 편이 낫다.

### 실습 — 매시 health check + Queue 알림

위 코드를 한 사이클로 묶어보자. 매시 정각에 외부 endpoint 5개를 health check하고, 실패가 있으면 `ALERT_QUEUE`로 흘려보낸다. consumer는 슬랙·이메일 등으로 fan-out한다.

```ts
async function runHealthChecks(env: Env) {
  const targets = [
    "https://api.toby-shop.example/health",
    "https://admin.toby-shop.example/health",
    // ...
  ];

  const results = await Promise.allSettled(
    targets.map((url) => fetch(url, { signal: AbortSignal.timeout(5000) }))
  );

  const failures = results
    .map((r, i) => ({ url: targets[i], result: r }))
    .filter(({ result }) => result.status === "rejected" || (result.value as Response).status >= 500);

  if (failures.length > 0) {
    await env.ALERT_QUEUE.send({
      kind: "health-check-failure",
      failures: failures.map((f) => f.url),
      timestamp: new Date().toISOString(),
    });
  }
}
```

이 작은 함수 한 묶음이 Spring의 `@Scheduled` + RestTemplate + `@Async` 알림 발송을 사실상 다 흡수한다. JVM도 띄우지 않고, 서버도 켜둘 필요가 없다. Worker가 매시 정각에 깨어나서 5초 내외로 도는 한 사이클이다.

### 무너지는 자리 — Cron Trigger의 한계

- **timezone**이 UTC 기본이다. 한국 시각으로 오전 9시 같은 표현을 쓰려면 우리가 변환해야 한다 (EventBridge Scheduler에는 timezone 옵션이 있어 이쪽이 살짝 편하다).
- **CPU time 한도**가 적용된다. 큰 batch ETL은 적합하지 않다 — Workflows로 쪼개거나 ECS에 두자.
- **재시도 모델이 Queue·Workflow보다 가볍다.** 한 invocation이 실패해도 다음 cron까지 재시도가 자동으로 일어나지는 않는다. 중요한 작업이라면 cron handler 안에서 Queue·Workflow를 trigger하고, 그쪽에 retry를 맡기는 편이 낫다.
- **execution log**가 짧다. Workers Logs·Logpush로 따로 흘려보내야 한 달 전 cron이 돌았는지 안 돌았는지를 추적할 수 있다.

---

## Part 4. Workers AI — Bedrock 옆자리

### Edge inference라는 한 줄짜리 약속

세 개의 도구(Workflows·Queues·Cron)로 비동기·orchestration·스케줄의 빈자리를 채웠다. 이제 살짝 결이 다른 영역으로 넘어가자. AI다.

Workers AI는 이 책에서 가장 신영역이고, 가장 빠르게 변하는 자리다. 한 줄로 그 본질을 잡자면 — **Cloudflare GPU 인프라 위에서 LLM·임베딩·이미지 모델을 edge에서 부른다.** Bedrock과 비슷한 카탈로그를 갖되, Cloudflare PoP 가까이에서 inference가 실행된다는 점이 다르다.

코드는 한 줄이다.

```ts
const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
  messages: [
    { role: "system", content: "You answer concisely." },
    { role: "user", content: "Explain edge computing in one sentence." },
  ],
});
```

`env.AI`는 Workers AI binding이다. `wrangler.toml`에 한 줄.

```toml
[ai]
binding = "AI"
```

이 binding 한 줄이 Bedrock의 IAM role + endpoint + boto3 init + region 설정을 다 흡수한다. 모델 ID(`@cf/meta/llama-3.1-8b-instruct`)만 넘기면 된다. 카탈로그에는 Llama 계열, Mistral, Stable Diffusion, BGE 임베딩 등이 있다. 모델 카탈로그는 자주 추가되고 가끔 사라지기도 하니, 정확한 목록은 공식 페이지를 확인하자.

### Bedrock vs Workers AI — 의사결정 표

| 기준 | Bedrock | Workers AI |
|---|---|---|
| 위치 | AWS region 내 | Cloudflare PoP edge |
| 모델 카탈로그 | Anthropic Claude, Cohere, Mistral, Titan, Llama, Nova 등 풍부 | Llama, Mistral, BGE, SDXL 등 (카탈로그 좁음) |
| 과금 단위 | 토큰 단위 (모델별) + 일부 캐시 할인 | Neuron 단위 ($0.011/1k Neurons, 일 10k 무료) |
| latency | region 내 호출, 사용자 위치에 따라 RTT 누적 | edge 가까이, 글로벌 균일 |
| Enterprise feature | VPC endpoint, Knowledge Bases, Model evaluation, Guardrails | 가벼움. AI Gateway가 일부 보완 |
| Anthropic Claude | 직접 호출 가능 | 직접 호출은 없음 (AI Gateway로 우회) |
| 통합 | AWS 안에서 IAM·VPC·CloudWatch 매끄러움 | Bindings로 R2·D1·Vectorize·Queue와 매끄러움 |

선택 기준을 한 줄로 잡자면 — **latency-critical edge 호출과 간편함은 Workers AI**, **컴플라이언스·VPC 격리·풍부한 enterprise feature는 Bedrock**이다. Anthropic Claude 같은 특정 모델을 production에서 써야 한다면, Bedrock이 그대로 정답이고, Workers AI가 닿지 못하는 자리다 (AI Gateway를 한 겹 끼워 우회는 가능하다 — 다음 파트에서 본다).

### Neuron 단위 과금 한 번 더

가격 모델이 Bedrock과 다르다는 점은 짚고 가야 한다. Bedrock은 모델별로 입력 토큰 단가·출력 토큰 단가가 다르다. Workers AI는 **Neuron**이라는 단위로 추상화돼 있다. Llama 3.1 8B의 1k 토큰이 몇 Neuron인지는 모델별 환산 표가 공식 페이지에 있다 (정확한 수치는 자주 갱신되므로 직접 확인하자).

이 Neuron 추상화가 좋은 점은 — **모델을 바꿔도 가격 멘탈이 한 단위로 잡힌다.** 단점은 모델별 진짜 비용 비교가 한 번 더 환산을 거쳐야 보인다는 것. hobby·MVP에서는 일 10k Neurons 무료 한도가 꽤 후하다. 작은 RAG 챗봇 정도라면 무료 한도 안에서 충분히 굴러간다.

### 무너지는 자리 — Workers AI의 한계

- **모델 라인업이 Bedrock보다 좁다.** Anthropic Claude·Cohere Command 같은 자리는 Workers AI에는 없다 (2026년 5월 기준). 이런 모델이 production 핵심이라면 Bedrock 또는 직접 OpenAI·Anthropic 호출 + AI Gateway 조합이 더 정직하다.
- **enterprise feature가 가볍다.** VPC endpoint, Knowledge Bases, Guardrails 같은 자리는 Bedrock 쪽이 두텁다.
- **GPU 단위 큰 모델은 부적합**할 수 있다. 70B+ 대형 모델·custom fine-tuned 모델 위주라면 Workers AI보다는 SageMaker·Bedrock 쪽이 맞다.
- **카탈로그 자체가 빠르게 변한다.** 작년에 있던 모델이 사라지거나, 같은 모델의 endpoint 이름이 바뀌기도 한다. production에서는 한 번 모델을 고정한 뒤 변경 시 회귀 테스트를 한 번 돌려야 한다.

이 한계를 인정하고 보면, Workers AI는 "모든 AI 호출을 여기서 다 한다"가 아니라 "edge 가까이에서 빠른 응답이 필요한 작은 작업을 가볍게 굴린다" 자리에 가장 잘 맞다. 임베딩 생성·간단한 분류·짧은 응답 생성 — 이쪽이 sweet spot이다. 큰 LLM 호출은 다음 파트의 AI Gateway를 통해 외부 모델로 흘려보내는 패턴이 더 현실적이다.

### Streaming 응답 한 번 더

LLM 호출에서 한 가지 더 짚고 가자. **streaming 응답**이다. 사용자가 챗봇에 질문을 던지면, 응답이 한 번에 떨어지기보다 토큰 단위로 흘러내리는 편이 체감이 좋다. Workers AI는 이 패턴을 표준 `ReadableStream`으로 그대로 받쳐준다.

```ts
const stream = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
  messages: [{ role: "user", content: question }],
  stream: true,
});

return new Response(stream, {
  headers: { "content-type": "text/event-stream" },
});
```

`stream: true` 한 줄이 전부다. 반환되는 값이 `ReadableStream`이라 그대로 Response에 얹어 SSE(Server-Sent Events)로 흘려보낼 수 있다. Worker는 이 stream이 끝날 때까지 살아 있되, CPU 시간은 토큰을 가공하는 짧은 순간만 잡힌다. 외부 모델 응답을 기다리는 시간은 — 이미 익숙해졌듯이 — 비용 0이다.

같은 일을 Lambda에서 하려면 Function URL의 streaming 모드를 켜고 별도 응답 형식을 맞춰야 한다. Workers는 Web standards 그대로다. fetch handler 안에서 stream을 반환하면 끝. 이 작은 차이가 챗봇·코파일럿·코드 어시스턴트 같은 자리에서 코드 한 페이지를 줄여준다.

---

## Part 5. Vectorize + AI Gateway — fallback 체인까지

### Vectorize — 글로벌 벡터 검색

작은 RAG 챗봇을 짠다고 해보자. 자기 회사 문서 1,000개를 임베딩해 벡터 DB에 저장하고, 사용자 질문이 들어오면 가까운 문서 5개를 찾아 LLM에 함께 던진다. 익숙한 그림이다. 벡터 DB 자리에 OpenSearch k-NN을 써도 되고, RDS에 pgvector를 얹어도 되고, Pinecone·Weaviate 같은 SaaS를 써도 된다. AWS에서는 최근에는 Knowledge Bases for Bedrock이 OpenSearch Serverless를 뒤에 두고 같은 일을 한 번 더 추상화한다 — 다만 region 단위 운영, IAM·VPC endpoint 한 줄, 그리고 매니지드 비용이 한 겹씩 따라온다.

Cloudflare에서는 이 자리를 **Vectorize**가 받는다. 한 줄로 잡자면 — **글로벌 분산 벡터 DB**다. 인덱스를 하나 만들고, 임베딩을 upsert하고, 쿼리 벡터로 nearest neighbor를 부른다. Workers·AI Gateway와 binding 하나로 매끄럽게 묶인다.

```ts
// 임베딩 저장
const embedding = await env.AI.run("@cf/baai/bge-small-en-v1.5", {
  text: ["edge computing reduces latency"],
});

await env.VECTORIZE.upsert([
  {
    id: "doc-1",
    values: embedding.data[0],
    metadata: { source: "intro.md", chunk: 0 },
  },
]);

// 검색
const queryEmbedding = await env.AI.run("@cf/baai/bge-small-en-v1.5", {
  text: ["how does edge work"],
});

const matches = await env.VECTORIZE.query(queryEmbedding.data[0], {
  topK: 5,
  returnMetadata: true,
});
```

`env.AI`로 임베딩을 만들고, `env.VECTORIZE`에 저장·검색한다. 두 binding이 Cloudflare 안에서 한 호흡으로 묶인다. 같은 일을 AWS에서 하려면 Bedrock embedding API → OpenSearch ingest → IAM role 두 개 → VPC endpoint 같은 세팅이 필요하다. Cloudflare 식으로는 binding 두 줄이다.

한도 한 번 짚자. 인덱스당 5M vector, 계정당 50k namespace까지 (2026 5월 기준). hobby·MVP에 충분한 규모이고, 중급 production까지는 무난히 견딘다. **다만 hybrid search(keyword + vector)는 미지원**이다. 큰 검색 시스템·복잡한 BM25+vector 결합이 필요한 자리라면 OpenSearch를 그대로 두는 편이 낫다.

다른 옵션과 비교 표 한 번 그려두자.

| 기준 | Vectorize | pgvector (RDS·Neon) | OpenSearch k-NN |
|---|---|---|---|
| 위치 | edge 글로벌 분산 | 기존 Postgres 안 | 별도 클러스터 |
| 운영 부담 | 매니지드, binding 한 줄 | 기존 RDS 운영에 흡수 | 별도 클러스터 운영 |
| Workers 통합 | binding 즉시 | Hyperdrive 경유 | HTTP fetch |
| 트랜잭션 | 없음 | RDB 트랜잭션 안에서 함께 | 없음 |
| 한도 | 5M vec/index | DB 단일 스케일 | 클러스터 스케일 |
| Hybrid search | 미지원 | extension 조합 가능 | 기본 지원 |

선택은 자기 워크로드를 펼쳐 보면 답이 나온다. **이미 RDS를 쓰고 vector도 RDB 트랜잭션에 묶이길 원한다면 pgvector**, **이미 OpenSearch에 full-text가 있고 vector를 한 번 더 얹는 거라면 OpenSearch**, **새 RAG·검색 시스템을 글로벌하게 가볍게 깐다면 Vectorize**. 5장의 결정 매트릭스를 한 번 더 펼쳐 자기 자리를 찾자.

### AI Gateway — AWS에 정확한 등가물이 없는 자리

이제 이 장에서 가장 흥미로운 도구로 가자. **AI Gateway**다. AWS에 정확한 등가물이 없다. Bedrock도, SageMaker도 같은 자리를 채우지 않는다. 직접 구축하거나, Portkey 같은 외부 SaaS를 쓰는 게 일반적이었다.

AI Gateway가 무엇인가. 한 줄로 — **LLM 요청을 가로채는 프록시**다. 70+ 모델, 12+ provider(OpenAI, Anthropic, Google, Cohere, Workers AI, Bedrock 등)를 단일 endpoint로 묶는다. 그 위에 다음을 얹는다.

- **캐싱**. 같은 prompt에 같은 응답이 짧은 시간 안에 반복되면 캐시 hit. 최대 90% 지연 감소·비용 절감.
- **rate limit**. provider별·앱별·사용자별로 제한.
- **retries**. 일시적 장애 시 자동 재시도.
- **fallback**. OpenAI가 죽으면 Anthropic으로, 둘 다 죽으면 Workers AI로.
- **observability**. 토큰 수·비용·latency를 한 대시보드에서.

이 다섯 가지가 한 제품에 묶여 있다는 점이 핵심이다. 자체 구축하면 다섯 개 인프라를 따로 운영해야 한다.

### OpenAI → Anthropic → Workers AI fallback 체인

코드로 한 번 그려보자. AI Gateway endpoint를 하나 만들고, OpenAI 호환 SDK로 호출하면 된다. 호출 URL만 AI Gateway로 바꾸면, 그 뒤로는 우리가 설정한 라우팅·fallback이 자동으로 적용된다.

```ts
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: env.OPENAI_API_KEY,
  baseURL: `https://gateway.ai.cloudflare.com/v1/${env.CF_ACCOUNT_ID}/${env.GATEWAY_NAME}/openai`,
});

const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: question }],
});
```

`baseURL`을 AI Gateway로 바꿔준 게 사실상 전부다. 우리 코드는 OpenAI를 부르는 평범한 SDK 호출. 그 뒤로 Cloudflare가 다음을 한다.

1. **캐시 확인**. 같은 prompt·같은 모델·TTL 안쪽이면 캐시된 응답을 즉시 돌려준다.
2. **OpenAI 호출 시도**. 성공하면 응답 + 토큰 사용량을 대시보드에 적는다.
3. **실패 시 fallback**. AI Gateway에 fallback rule을 설정해두면, OpenAI 5xx·timeout이 발생했을 때 Anthropic 같은 다른 provider로 자동 재시도한다.
4. **마지막 fallback**. Anthropic도 죽으면 Workers AI Llama 모델로 — 카탈로그가 좁아도 "응답이 없는 것보다는 낫다"는 자리에 어울린다.

fallback rule은 AI Gateway 콘솔이나 API로 정의한다. "primary는 OpenAI, secondary는 Anthropic, tertiary는 Workers AI" 식으로 체인을 짜둔다. 우리 코드는 한 곳만 부른다 — `client.chat.completions.create`. 라우팅은 인프라가 한다.

캐싱도 한 번 더 짚자. AI Gateway의 캐시는 prompt 전체를 key로 잡되, 우리가 cache key를 직접 지정할 수도 있다 — 사용자별 응답이 섞이지 않게 user id를 cache key에 포함하는 패턴이 흔하다. 같은 시스템 prompt + 같은 사용자 질문 + 동일 사용자 → 캐시 hit. TTL은 우리가 정한다. FAQ 같이 응답이 거의 변하지 않는 자리에서 캐시 hit률이 가장 높다 — Cloudflare 자료에 따르면 동일 요청 90%까지 지연 감소가 가능하고, 그만큼 토큰 비용도 깎인다.

rate limit도 한 묶음 짚자. provider별·사용자별·앱별로 분당 호출 수·일당 토큰 수를 잡을 수 있다. 사용자가 우리 챗봇을 악용해 OpenAI 청구서를 폭발시키는 시나리오가 한 번 떠오르면 — 끔찍하다 — 이 한 줄이 중요해진다. 자체 구축이라면 Redis + 토큰 버킷을 직접 짜야 하는 자리가 콘솔에서 한 번에 잡힌다.

이 그림이 왜 정직한가. 한 provider에 lock-in되지 않는다는 뜻이다. OpenAI 가격이 오르면 baseURL은 그대로 둔 채 라우팅을 Anthropic 우선으로 바꾸면 된다. 코드는 손대지 않는다. AWS에서 같은 일을 하려면 자체 게이트웨이를 짜거나, Portkey 같은 외부 SaaS를 한 겹 더 두는 식이다. AI Gateway는 그 한 겹을 Cloudflare 인프라가 직접 제공한다는 점에서 자리가 다르다.

### Bedrock 앞에 AI Gateway를 두는 패턴

한 가지 더. AI Gateway는 **Bedrock도 provider로** 받는다. AWS에 모델이 묶여 있어 옮길 수 없는 회사도, AI Gateway를 앞단에 두면 캐싱·관측·rate limit·fallback의 이득은 그대로 얻는다.

```
[Worker] → [AI Gateway] → [Bedrock (Anthropic Claude)]
                       ↘ [OpenAI (fallback)]
                       ↘ [Workers AI (last resort)]
```

이 그림이 14장에서 강조하는 하이브리드 패턴 중 하나다. AWS 안의 모델은 그대로 두고, Cloudflare는 그 앞의 게이트웨이만 채운다. lock-in이 얇아지고, 옮길 자유는 늘어난다.

### 작은 RAG 챗봇 한 사이클

이 장의 모든 도구를 한 줄에 꿰어보자.

1. **문서 임베딩 ingest** (Workflow): R2의 마크다운 문서를 chunk로 쪼개고, 각 chunk를 Workers AI 임베딩 모델로 변환해 Vectorize에 upsert. 한 번에 1,000건이면 step.do로 100개씩 10번 나눠 묶는다.
2. **사용자 질문 처리** (HTTP Worker): 질문을 받으면 임베딩하고 Vectorize에서 top-5 chunk를 찾는다.
3. **LLM 호출** (AI Gateway 경유): top-5 chunk를 context로 넣어 OpenAI에 질문. AI Gateway가 캐시·fallback·관측을 처리한다.
4. **응답 캐시 hit 시** 같은 질문 두 번째에는 ms 단위로 답이 돌아온다 — 90% 비용 절감의 자리가 여기다.
5. **저빈도 분석 작업**은 cron trigger로 매일 새벽 한 번 돌려, "어제 가장 많이 물은 질문 톱10"을 D1에 적어둔다.

이 한 사이클이 우리 누적 프로젝트 `toby-shop`의 어드민 옆에 작은 RAG 챗봇으로 붙는다. Workflow·Queue·Cron·Workers AI·Vectorize·AI Gateway가 한 사이클에 다 등장한다.

### 무너지는 자리 — Vectorize + AI Gateway의 한계

- **Vectorize는 hybrid search 미지원** (2026 기준). BM25 + vector를 함께 써야 하는 검색 시스템이라면 OpenSearch가 더 정직하다.
- **AI Gateway는 신생 영역**이다. provider 추가·rule 문법·대시보드 UI가 자주 변한다. production에서 핵심 경로로 의존한다면, fallback 자체의 fallback도 떠올려두자 — AI Gateway가 잠깐 흔들릴 때 우리 시스템이 어떻게 보일지.
- **캐시 일관성**. AI Gateway 캐시는 LLM 응답을 그대로 캐싱한다. 사용자별·세션별 응답이 섞이지 않게 cache key 설계를 한 번 짚어야 한다 (잘못하면 다른 사용자의 응답이 보일 수 있다 — 끔찍한 일이다).
- **provider별 차이**가 fallback에서 드러난다. OpenAI와 Anthropic은 응답 형식이 다르다. fallback이 일어났을 때 client 코드가 모든 provider 형식을 처리할 수 있어야 한다 — AI Gateway가 어느 정도 정규화를 해주지만, 완벽하지는 않다.

---

## 실습 정리 — 이 장의 결과물

이 장에서 손가락으로 만든 것들을 한 자리에 모으자. `toby-shop` 누적 프로젝트의 12장 체크포인트(`ch12-async-ai`)에 다음이 더해진다.

- **결제 후 영수증 발송 Workflow** — 주문 검증 → 영수증 PDF 렌더 → R2 저장 → 이메일 Queue push → 30분 sleep → 후속 안내 메일. `step.sleep`이 비용 0이라 sequence를 늘려도 한 달 청구서가 흔들리지 않는다.
- **Mail Queue + Dead-letter Queue** — Workflow에서 떼어낸 이메일 발송이 별도 Worker consumer로 돌고, 외부 SMTP 흔들림을 retry·DLQ로 흡수한다.
- **매시 health check Cron + Alert Queue** — `[triggers] crons` 한 줄로 매시 정각에 외부 endpoint 5개를 점검하고 실패를 슬랙으로 fan-out.
- **작은 RAG 챗봇** — Vectorize에 회사 문서 임베딩, AI Gateway 경유 OpenAI → Anthropic → Workers AI fallback 체인. 같은 질문 두 번째에는 캐시 hit으로 응답이 즉각 돌아온다.

이 네 가지가 어드민 옆에 한 사이클로 묶여 있다. `wrangler tail`로 로그를 보면 Workflow 인스턴스가 step별로 진행되는 모습, Queue consumer가 batch로 처리하는 모습, cron 발화 로그, AI Gateway의 cache hit 로그가 함께 흐른다.

## 마무리

이 장이 길었다. 다섯 도구를 한 호흡에 다뤘으니 그럴 수밖에 없다. 한 번에 다 외울 필요는 없다 — 자기 시스템에 어떤 자리가 있는지를 5장의 결정 매트릭스 위에서 다시 펼쳐 보자. Step Functions가 무겁게 느껴졌던 자리에는 Workflows를 떠올리고, SQS 옆자리에는 Queues, `@Scheduled`·EventBridge Scheduler 자리에는 Cron Trigger, Bedrock 옆이나 앞에는 Workers AI·AI Gateway가 들어설 자리가 있다.

기억해두자 — 이 다섯 도구는 따로따로 빛나지 않는다. **함께 묶일 때** 가장 잘 빛난다. Workflow가 큰 흐름을 잡고, Queue가 외부 의존을 흡수하고, Cron이 정기 작업을 켜고, AI Gateway가 LLM 호출을 정돈한다. 한 도구만 도입하면 "또 하나의 SaaS 호출"처럼 보이지만, 다섯이 binding으로 매끄럽게 묶이면 한 멘탈로 잡히는 sequence가 된다.

물론 모든 자리가 매끄럽지는 않다. Workflows는 AWS 서비스 통합 깊은 워크플로를 옮기는 데 부담이 있고, Queues는 strict global ordering을 약속하지 않으며, Workers AI는 모델 라인업이 좁고, AI Gateway는 신생 영역이라 자주 변한다. 이 한계들을 인정하고 자기 자리에 맞을지 가늠하는 일이 5장 결정 프레임의 또 한 번의 적용이다.

다음 장에서는 이 모든 도구를 production에서 굴리는 일의 정직한 무게를 다룬다. **운영과 정직한 한계**다. 비용 모델의 함정, observability 공백, 2025년 두 차례의 outage가 가르쳐 준 것, vendor lock-in을 어떻게 안고 갈지. 이 책이 광고서가 아님을 가장 분명히 드러내는 장이 다음 페이지에서 펼쳐진다.
