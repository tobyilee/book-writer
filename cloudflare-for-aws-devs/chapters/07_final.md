# 7장. 데이터 1 — KV와 D1, 워크로드 패턴으로 골라 쓰기

DynamoDB로 세션을 굴리고 있었다고 해보자. on-demand 청구서가 매달 우편처럼 꼬박꼬박 도착하고, GSI를 두어 사용자 ID와 만료 시각으로 동시에 조회하고 있다. 어느 날 팀에서 누군가 묻는다. "이거, 그냥 Cloudflare KV로 옮기면 같은 게 되지 않아요?" 솔깃하다. KV는 글로벌 분산이고, 무료 plan에서도 꽤 넉넉하고, 4장의 매핑 표에서도 분명히 "DynamoDB ↔ KV"라는 줄을 봤다. 옮기면 안 될까?

그런데 잠깐. 4장에서 우리는 그 줄에 작은 가시 하나를 박아 두었다. *DynamoDB 한 줄 매핑은 거짓말이다.* DynamoDB로 하던 일이 사용자 패턴에 따라 KV로도, D1으로도, Durable Objects로도 갈라진다고 분명히 적었다. 그리고 5장에서 우리는 5축 결정 트리를 세웠다 — 일관성·런타임·글로벌성·요청 패턴·컴플라이언스. 그 두 도구를 손에 쥔 채로 이 장에 들어왔다.

자, 그렇다면 이번 장에서 풀어야 할 질문은 무엇인가. *KV와 D1을 어디서부터 어디까지 믿어야 하는가.* 어떤 워크로드를 KV에 맡기면 나중에 후회하지 않고, 어떤 워크로드를 D1에 얹으면 production을 견디는가. 두 제품의 본질을 이해하지 못하면 6개월 뒤에 우리는 KV 위에 secondary index를 흉내내려고 코드를 비비 꼬고 있거나, D1 한 DB가 10GB 한도에 부딪쳐 야간에 sharding 전략을 그리고 있을 것이다. 둘 다 끔찍한 일이다.

이 장에서는 KV와 D1을 워크로드 패턴별로 어디에 어떻게 자리 잡게 할지, 그리고 둘 중 어느 쪽에도 답이 아닐 때 무엇을 해야 하는지를 정리해 보자. 6장에서 만든 사용자 API 한 벌은 이미 KV에 세션을 두고 있다. 이 장에서는 그 위에 D1과 Drizzle을 얹어 사용자 프로필을 진화시켜 보겠다.

## KV — 본질부터 다시 그리자

KV의 본질은 한 줄로 요약할 수 있다. *글로벌 분산 key-value 저장소, 그리고 eventually consistent.* 마지막 부분이 핵심이다. 우리가 한 PoP에서 값을 쓰면, 다른 PoP에서 그 값을 읽을 수 있게 되기까지 *최대 60초*가 걸린다. 평균은 훨씬 짧지만 SLA로 약속되는 숫자는 60초다.

DynamoDB도 eventually consistent 모드가 기본이라 비슷해 보일 수 있다. 그런데 DynamoDB는 옵션으로 strongly consistent read를 켤 수 있고, 같은 region 안에서는 거의 즉시 일관성이 보장된다. KV는 다르다. *strongly consistent 모드 자체가 없다.* 글로벌 분산이 KV의 정체성이고, 그 대가로 일관성을 늦췄다.

여기에 또 하나의 제약이 붙는다. **per-key 1 write/s.** 한 키에 1초에 한 번 이상 쓰면 그 너머의 쓰기는 거부되거나 마지막 것만 살아남는다. 카운터를 KV에 두면 안 된다는 뜻이다. 서로 다른 사용자의 세션을 각자의 키에 저장하는 건 괜찮지만, "전체 활성 사용자 수"를 한 키에 담아 매 요청마다 증가시키려고 하면 KV는 거기서 무너진다.

마지막 제약이 가장 무겁다. **secondary index도, range query도 없다.** 키 하나로 값 하나를 꺼낸다. 그게 전부다. `list()`로 prefix 기반 나열은 되지만, "30일 이내에 만료되는 세션을 모두 찾아라" 같은 쿼리는 못 한다. DynamoDB의 GSI를 기대하고 옮기면 거의 반드시 사고가 난다.

### KV가 빛나는 자리

이런 제약을 받아들이고도 KV가 빛나는 자리는 분명하다. 5장의 결정 매트릭스에서 *Move now*로 묶였던 패턴들 — *read-heavy, eventually consistent로 충분, 단일 키 lookup* — 의 자리다.

- **세션 토큰.** 사용자가 로그인하면 토큰을 KV에 쓴다. 60초 후에 다른 PoP에서도 그 토큰이 보인다. 세션을 60초 안에 같은 토큰으로 두 번 검증하는 시나리오는 거의 없다.
- **Feature flag.** 어드민이 토글을 켜면 60초 후에 모든 PoP에서 그 변경이 반영된다. 광고 캠페인이나 베타 기능 노출에 충분하다.
- **API key·configuration.** 외부 API 키, 라우팅 설정, A/B 테스트 그룹. 자주 바뀌지 않고, 바뀌어도 1분 정도 늦게 적용돼도 무방한 데이터.
- **사용자 설정.** 다크 모드, 언어 선택, 알림 토글 같은 것. 사용자가 바꾼 직후에 다른 디바이스에서 1분 늦게 보이는 건 보통 문제가 안 된다.
- **읽기 캐시.** 외부 API 응답을 5분 TTL로 캐시. 한국 사용자가 일본 PoP을 거치든 미국 PoP을 거치든 거의 같은 캐시 적중률을 본다.

이 다섯 자리는 KV가 가장 안전하게 자리 잡는 곳이다. 6장에서 만든 사용자 API의 세션 저장소는 KV 그대로 두자. 7장이 끝나도 거기는 KV다.

### KV가 무너지는 자리

반대로, 다음 자리에서는 KV가 무너지거나 거짓 약속을 한다. 무너진다는 건 동작 안 한다는 뜻이 아니다. *동작은 하지만 production에서 사고로 이어진다*는 뜻이다.

- **검색·정렬·범위 쿼리가 필요한 자리.** secondary index가 없으니 "활성 사용자 목록을 가입일 순서로" 같은 쿼리는 못 한다. 한 키에 JSON 배열로 다 담아 두고 매번 전체를 읽어 메모리에서 필터링하면 잠깐은 돌지만 데이터가 커지면 끝이다.
- **빈번한 쓰기.** per-key 1 write/s 한도. 카운터·실시간 통계·재고 차감은 KV의 자리가 아니다. 이건 D1 또는 Durable Objects의 영역이다.
- **transactional 일관성이 필요한 자리.** 좌석 예약, 재고 차감, 게임 턴. KV는 atomic compare-and-swap도 트랜잭션도 없다. 두 사용자가 같은 좌석을 동시에 예약하면 둘 다 성공한다.
- **strong consistency가 필요한 자리.** 결제 후 즉시 잔액을 읽어야 하는 시나리오. KV에 잔액을 두고 결제 후 잔액을 읽으면 60초 동안은 옛날 값이 보일 수 있다.

이 네 가지 중 하나라도 해당된다면 KV는 답이 아니다. *솔직히 다른 자리를 찾자.*

### Liftosaur — 정직한 회귀

KV 이야기를 광고처럼 들리지 않게 하려면 한 사례를 마주봐야 한다. 운동 트래킹 앱 *Liftosaur*는 1인 개발자가 만든 서비스인데, 처음에는 Workers + KV 위에 시스템을 올렸다가 결국 Lambda + DynamoDB로 회귀했다. 회귀 사유를 본인이 블로그에 정직하게 남겼다. 그 글을 읽으면 KV가 무너지는 자리가 한 화면에 펼쳐진다.

- **secondary index 부재.** 운동 데이터는 사용자 ID로도 조회하고, 운동 종류로도 조회하고, 날짜 범위로도 조회해야 한다. KV에서는 이 세 가지가 다 단일 키 lookup으로 안 풀린다. DynamoDB라면 GSI 두세 개로 끝나는 일이다.
- **range query 부재.** "최근 7일간의 운동 기록"을 가져오려면 매번 전체를 스캔해야 한다.
- **KV 백업 어려움.** KV는 점진적 백업·복원 도구가 약하다. DynamoDB의 PITR(point-in-time recovery)이나 export to S3에 비교하면 운영적 안전망이 얇다.
- **Node 라이브러리 부재.** 이미지 처리에 필요한 일부 Node 라이브러리가 Workers에서 동작하지 않았고, 1MB 스크립트 한도(당시 기준)에 걸려 의존성을 넣을 수가 없었다. *이건 KV 문제는 아니지만, Workers 위에 워크로드 전체를 올린다는 결정의 일부였다.*

이 네 가지가 모여 결국 Lambda + DynamoDB로 돌아갔다. 본인이 블로그에서 강조한 결론은 분명하다 — *KV를 DynamoDB의 대체재로 보지 말라.* 사용 패턴이 secondary index나 range query에 의존한다면, KV가 아니라 DynamoDB나 D1로 가야 한다.

이 사례를 어떻게 받아들이면 좋을까. 두 가지로 나눠 보자. 첫째, *5축 결정 트리를 미리 돌렸다면 옮기지 않았을 것이다.* 일관성 축에서 secondary index 필요성이 보였을 테고, 런타임 축에서 1MB 한도와 Node 라이브러리 부재가 빨간불을 켰을 것이다. 둘째, *옮긴 뒤 회귀하는 것도 정직한 결정이다.* 6개월 운영해 보고 무너지는 자리를 확인했다면, 자존심을 굽히고 후퇴할 줄 아는 게 더 큰 용기다.

이 책의 핵심 약속을 한 번 더 떠올려 보자 — *Cloudflare를 도입하지 말고, 자기 아키텍처에 올바른 자리를 내주자.* Liftosaur는 KV가 자기 워크로드의 올바른 자리가 아니었다는 걸 운영 비용을 치르고 배웠다. 우리는 그 학습을 빌릴 수 있다.

### KV 코드 한 사이클

본질을 봤으니 손으로 한 번 만져 보자. 6장의 사용자 API에 KV 세션 저장소가 이미 있다고 가정하자. `wrangler.toml`에 KV 바인딩을 선언하고, Hono 미들웨어에서 토큰을 읽고 쓰는 한 사이클이다.

먼저 `wrangler.toml`.

```toml
name = "toby-shop-api"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[kv_namespaces]]
binding = "SESSIONS"
id = "your-kv-namespace-id"
preview_id = "your-preview-id"
```

`binding = "SESSIONS"`가 핵심이다. 이 한 줄이 코드 안에서 `env.SESSIONS`로 들어오는 핸들이 된다. 4장에서 살펴봤듯 Bindings는 Spring의 `@Autowired`와 IAM role을 한 추상으로 묶은 것이다. 별도의 SDK 클라이언트도, IAM 정책도 없다.

이제 Hono 핸들러.

```ts
import { Hono } from "hono";

type Bindings = { SESSIONS: KVNamespace };

const app = new Hono<{ Bindings: Bindings }>();

// 로그인 — 세션 토큰 발급
app.post("/auth/login", async (c) => {
  const { userId } = await c.req.json<{ userId: string }>();
  const token = crypto.randomUUID();
  await c.env.SESSIONS.put(
    `session:${token}`,
    JSON.stringify({ userId, createdAt: Date.now() }),
    { expirationTtl: 60 * 60 * 24 * 7 }, // 7일 TTL
  );
  return c.json({ token });
});

// 세션 검증 미들웨어
app.use("/me/*", async (c, next) => {
  const token = c.req.header("authorization")?.replace("Bearer ", "");
  if (!token) return c.text("unauthorized", 401);
  const raw = await c.env.SESSIONS.get(`session:${token}`);
  if (!raw) return c.text("expired", 401);
  c.set("session", JSON.parse(raw));
  await next();
});

app.get("/me", async (c) => c.json(c.get("session")));

export default app;
```

세 가지를 짚어 두자. 첫째, `expirationTtl`. KV는 키마다 TTL을 줄 수 있다. 7일 후에는 자동으로 사라진다. DynamoDB의 TTL과 똑같은 모델인데, KV에서는 옵션 한 줄로 끝난다. 둘째, `put`/`get`/`list`라는 단순한 API. SQL도, 인덱스도, 트랜잭션도 없다. *그래서 빠르고, 그래서 제약된다.* 셋째, `put` 직후 다른 PoP에서 `get`을 부르면 60초 동안은 못 찾을 수 있다는 사실. 같은 PoP에서 같은 사용자가 같은 요청을 보내는 시나리오는 보통 문제가 안 되지만, 다중 region·다중 디바이스에서는 이걸 잊지 말자.

`list()`로 prefix 기반 나열도 가능하다.

```ts
const result = await c.env.SESSIONS.list({ prefix: "session:" });
for (const key of result.keys) {
  // key.name, key.expiration
}
```

다만 이걸 매 요청마다 부르면 비용이 무섭게 올라간다. KV의 `list`는 고운 검색이 아니라 *prefix scan*이다. 쓰임을 가려야 한다.

자, KV는 여기까지. 이제 D1으로 넘어가자.

## D1 — SQLite at edge, 그리고 그 한계

D1의 본질은 한 마디로 *SQLite를 글로벌 edge에 펼친 것*이다. SQL 쿼리, JOIN, CTE, 트랜잭션, prepared statement 전부 된다. 기존 RDS Postgres에 익숙한 개발자라면 손에 익은 도구를 거의 그대로 들 수 있다.

다만 두 가지 제약이 있다.

**첫째, 1 DB 최대 10GB.** 작은 SaaS의 사용자 데이터, 게시물, 주문 내역에는 충분하지만, 대규모 로그·이벤트 스트림을 D1에 다 담겠다는 발상은 위험하다. 한도에 가까워지면 sharding 전략을 미리 그려야 하는데, sharding을 하느니 처음부터 Postgres + Hyperdrive(10장)로 가는 편이 낫다.

**둘째, sustained write 500~2k/s.** D1의 read replica는 자동으로 글로벌 PoP에 분산되지만, write는 primary 한 곳에서 받는다. 초당 수천 건 이상의 쓰기가 지속되는 워크로드 — 게임 텔레메트리, IoT 센서 데이터, 실시간 분석 — 는 D1의 자리가 아니다. *이건 D1을 비난하는 게 아니다. 모델이 그렇게 설계된 것이다.* 비교를 위해 다른 SQLite 계열인 Turso는 1~5k/s, 본격 RDB인 PostgreSQL/MySQL은 10k~50k/s 수준이다.

이 두 한도 안에 들어오는 워크로드라면 D1은 Workers와 가장 자연스럽게 짝이 맞는 데이터 저장소다. Workers Paid plan에는 일 250억 row read, 5천만 row write, 5GB storage가 기본 포함된다. 작은 SaaS 한 개를 다 운영하고도 비용 청구서가 거의 안 보일 수준이다.

### D1이 빛나는 자리, 무너지는 자리

5장의 결정 매트릭스에서 *사용자 facing CRUD API*가 *Move later*로 묶였던 걸 떠올려 보자. D1이 바로 그 자리의 첫 번째 후보다.

- **빛나는 자리.** 사용자 프로필·주소·권한, 상품 카탈로그 메타데이터, 주문 내역(write 부담이 크지 않은 작은 이커머스), 블로그 게시물, 댓글, 작은 SaaS의 거의 모든 관계형 데이터.
- **무너지는 자리.** 초당 수천 건 이상의 쓰�기가 들어오는 워크로드(IoT, 게임 telemetry), 한 DB가 10GB를 명백히 넘을 데이터(대규모 분석 로그), cross-region 트랜잭션이 필요한 워크로드, 강한 region lock이 필요한 워크로드.

마지막 두 가지는 KV에도 해당되는 함정이다. *KV·D1 모두 cross-region 트랜잭션을 지원하지 않는다.* 한국 D1과 유럽 D1을 한 트랜잭션 안에서 다루는 건 불가능하다. 그게 필요하다면 Durable Objects(8장) 또는 외부 분산 DB로 가야 한다.

### RDS Postgres에 익숙한 개발자의 시각에서

RDS를 5년 굴려 본 개발자가 D1을 만나면 무엇이 같고 무엇이 다른가. 한 페이지로 정리해 보자.

| 측면 | RDS Postgres | D1 |
|---|---|---|
| **쿼리 언어** | PostgreSQL 방언 | SQLite 방언 (대부분 호환, JSON·CTE 지원) |
| **트랜잭션** | full ACID, savepoint, 분산 트랜잭션 가능 | statement-level transaction, batch transaction |
| **인덱스** | B-tree, hash, GIN, GiST, partial, expression | B-tree, partial, expression (SQLite 표준) |
| **read replica** | 명시적 설정·관리 필요 | 자동 글로벌 분산 |
| **백업** | snapshot + PITR (보통 35일) | 자동 + Time Travel (point-in-time recovery 30일) |
| **연결 모델** | TCP 직접, connection pool 직접 관리(HikariCP) | Workers 바인딩, 풀 관리 불필요 |
| **확장** | vertical (인스턴스 크기) + horizontal (replica) | DB 단위 자동 (단, 1 DB 10GB 한도) |
| **스키마 마이그레이션** | Flyway, Liquibase | wrangler d1 migrations + Drizzle Kit |
| **운영 부담** | 패치·업그레이드·VPC·SG | 거의 없음 |

가장 인상적인 차이는 *연결 모델*이다. Spring + JPA + HikariCP를 운영해 본 사람이라면 connection pool size 튜닝, idle timeout, max lifetime 같은 파라미터들과 씨름한 기억이 있을 것이다. D1에서는 그 모든 게 사라진다. `env.DB.prepare(...)`라고 부르면 그만이다. 풀도, 타임아웃도, 인증도 Workers 런타임이 알아서 한다. *이게 자유롭게 느껴지면 좋고, 통제권을 잃은 듯해 찜찜하면 그것도 정상이다.* 두 감정 모두 합당하다.

### D1 + Drizzle 코드 한 사이클

이제 6장의 사용자 API 위에 D1 + Drizzle을 얹어 보자. 세션은 KV 그대로 두고, 사용자 프로필을 D1에 담는 진화다. Drizzle은 TypeScript 친화적인 ORM 겸 query builder인데, JPA 같은 무거운 마법 없이 SQL과 1:1로 맵핑된다는 점이 깔끔하다.

`wrangler.toml`에 D1 바인딩을 추가하자.

```toml
[[d1_databases]]
binding = "DB"
database_name = "toby-shop"
database_id = "your-d1-database-id"
migrations_dir = "drizzle/migrations"
```

스키마 파일.

```ts
// packages/db/schema.ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  displayName: text("display_name").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
});

export const profiles = sqliteTable("profiles", {
  userId: text("user_id")
    .primaryKey()
    .references(() => users.id),
  bio: text("bio"),
  avatarUrl: text("avatar_url"),
  language: text("language").default("ko"),
});
```

마이그레이션 워크플로우는 Drizzle Kit이 알아서 한다.

```bash
# 스키마 변경 → SQL 마이그레이션 파일 생성
pnpm drizzle-kit generate

# wrangler가 D1에 적용
pnpm wrangler d1 migrations apply toby-shop --remote
```

`drizzle-kit generate`는 스키마 변경을 감지해 `drizzle/migrations/0001_xxx.sql` 같은 파일을 만든다. 그 파일을 `wrangler d1 migrations apply`가 D1에 적용한다. *Flyway·Liquibase에 익숙하다면 거의 같은 멘탈 모델이다 — 형상 변경이 SQL 파일로 떨어지고, 그 파일들이 순서대로 적용된다.* 한 가지 다른 점은 `--local` 플래그로 로컬 SQLite에 먼저 적용해 보고 production에 적용할 수 있다는 것. `wrangler dev --local`이 D1을 로컬 SQLite로 시뮬레이션해 주기 때문에, 로컬에서 마이그레이션 결과를 확인하고 production으로 넘어가는 흐름이 자연스럽다.

이제 Hono 라우터에 사용자 프로필 엔드포인트를 추가하자.

```ts
import { Hono } from "hono";
import { drizzle } from "drizzle-orm/d1";
import { eq } from "drizzle-orm";
import { users, profiles } from "@toby-shop/db/schema";

type Bindings = {
  DB: D1Database;
  SESSIONS: KVNamespace;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/users/:id", async (c) => {
  const db = drizzle(c.env.DB);
  const id = c.req.param("id");

  const result = await db
    .select({
      id: users.id,
      email: users.email,
      displayName: users.displayName,
      bio: profiles.bio,
      avatarUrl: profiles.avatarUrl,
    })
    .from(users)
    .leftJoin(profiles, eq(profiles.userId, users.id))
    .where(eq(users.id, id))
    .get();

  if (!result) return c.notFound();
  return c.json(result);
});

app.put("/me/profile", async (c) => {
  const db = drizzle(c.env.DB);
  const session = c.get("session"); // KV 미들웨어에서 주입
  const body = await c.req.json<{ bio?: string; language?: string }>();

  await db
    .insert(profiles)
    .values({ userId: session.userId, ...body })
    .onConflictDoUpdate({
      target: profiles.userId,
      set: body,
    });

  return c.json({ ok: true });
});
```

세 가지를 짚어 두자. 첫째, `drizzle(c.env.DB)`로 D1 바인딩을 Drizzle 인스턴스로 감싼다. 그 인스턴스가 SQL 쿼리를 타입 안전하게 만든다. 둘째, `leftJoin`이 자연스럽게 되고 결과는 `result` 객체에 그대로 들어온다. JPA의 `@OneToOne`·`@ManyToOne` 같은 어노테이션 없이 SQL과 1:1로 매핑된다. 셋째, `onConflictDoUpdate`는 SQLite의 `INSERT ... ON CONFLICT DO UPDATE`. PostgreSQL에서 익숙한 upsert 패턴이 그대로 통한다.

JPA의 `@Transactional` 같은 자동 propagation은 없다. D1에서 트랜잭션을 쓰려면 `db.batch([...])`로 여러 statement를 한 묶음으로 보낸다.

```ts
await db.batch([
  db.insert(users).values({ id, email, displayName, createdAt: new Date() }),
  db.insert(profiles).values({ userId: id, language: "ko" }),
]);
```

이 batch는 atomic하다. 둘 다 성공하거나 둘 다 실패한다. *Spring의 `@Transactional`처럼 메서드 경계에서 자동으로 시작·커밋되는 게 아니라, 코드에서 명시적으로 묶는다.* 처음엔 번거롭게 느껴질 수 있다. 그런데 한두 주 쓰다 보면, 트랜잭션 경계가 코드에 그대로 보이는 게 오히려 명료하다. JPA의 `LazyInitializationException` 같은 함정이 없다.

### Read replica와 Time Travel

D1에는 RDS 운영 경험이 있는 개발자에게 인상적인 두 가지 기본 장치가 있다.

**Read replica는 자동이다.** Workers가 어느 PoP에서 깨어나든 그 PoP에 가장 가까운 D1 read replica에서 읽어 온다. RDS에서 read replica를 한국·일본·유럽에 띄우고, 애플리케이션에서 어느 replica로 보낼지 라우팅하던 일을 D1은 알아서 한다. *그 대신 write는 primary 한 곳으로 모인다.* 이게 sustained write 한도의 이유이기도 하다.

**Time Travel.** D1은 30일 전까지의 어느 시점으로든 데이터베이스를 복원할 수 있다. RDS의 PITR과 멘탈 모델이 같다. 누군가 실수로 `DELETE FROM users` 한 줄을 production에 날렸다면, `wrangler d1 time-travel restore`로 5분 전 상태로 되돌릴 수 있다. 별도 백업 설정도, 비용 추가도 없다. *이게 production을 다루는 안심의 핵심이다.* 운영 경험이 쌓일수록 이 한 줄이 얼마나 무거운 약속인지 알게 된다.

다만 한 가지 주의. Time Travel은 한 D1 인스턴스 안의 시간 복원이다. *cross-region 일관성이나 cross-DB 트랜잭션을 보장하지 않는다.* 두 D1 DB를 같은 시점으로 같이 되돌리려면 별도 코디네이션이 필요하다.

## KV vs D1 의사결정 표 — 다섯 축으로 갈라보자

여기까지 두 제품의 본질을 봤다. 이제 자기 워크로드를 어느 쪽에 둘지 결정하는 표를 한 장 만들어 두자. 5축 결정 트리를 KV·D1 사이의 비교로 좁힌 형태다.

| 축 | KV에 두자 | D1에 두자 |
|---|---|---|
| **데이터 형상** | 단일 키 lookup이면 충분한 평탄한 데이터 (세션, flag, 설정) | 관계형, JOIN 필요, 다중 인덱스 (사용자, 주문, 상품) |
| **쿼리 패턴** | 키 → 값, 또는 prefix scan | SQL JOIN, 정렬, 범위, GROUP BY, 집계 |
| **일관성 요구** | eventually consistent (≤60초 늦어도 OK) | strong consistency, statement-level transaction |
| **쓰기 빈도** | per-key 1 write/s 이내, key 수는 무제한 | 전체 sustained 500~2k/s 이내 |
| **데이터 크기** | 키당 25MB까지, 총 namespace 무제한 | 1 DB 10GB 한도 |

이 표를 한 워크로드 위에 올려 보고 다섯 축이 모두 한 쪽으로 기울면 거기가 답이다. 만약 *데이터 형상은 KV인데 쿼리 패턴은 D1*처럼 축이 갈라진다면, 잠깐 멈춰서 생각하자. 보통은 워크로드를 더 잘게 쪼개야 답이 나온다. 예를 들어 "사용자 프로필"이 한 덩어리로 보였는데, 사실은 *세션 토큰(KV) + 프로필 마스터(D1)*로 갈라야 자연스럽다.

5장에서 만든 결정 워크시트를 다시 펼쳐서 KV·D1 컴포넌트들을 이 다섯 축 위에 한 번 더 점검해 보자. 한 시간이면 충분하다. 그 한 번의 점검이 6개월 뒤의 회귀 비용을 절반 이상 줄여 준다.

## 둘 다 답이 아닐 때 — 정직한 한계

여기까지 KV가 빛나는 자리와 D1이 빛나는 자리를 봤다. 그런데 5장 결정 트리가 그랬듯, 이 장의 의무도 정직성이다. *KV·D1 모두 답이 아닌 워크로드*가 분명히 있고, 그땐 무엇을 해야 하는가.

**1. 빈번한 쓰기 + 강한 일관성이 동시에 필요한 자리.** 재고 차감, 좌석 예약, 게임 점수판. KV는 일관성이 약하고 D1은 sustained write가 약하다. 이건 *Durable Objects(8장)*의 자리다. actor 모델로 한 객체가 직렬화된 처리를 보장한다.

**2. 초당 수천 건 이상의 sustained write가 필요한 자리.** 로그 ingestion, 텔레메트리, 이벤트 스트림. D1의 500~2k/s를 넘어선다. 이건 *RDS·Aurora 그대로 두고 Hyperdrive(10장)로 앞에 두는 패턴*이 답이다. 또는 외부 ClickHouse·Snowflake로.

**3. 한 DB가 10GB를 명백히 넘을 데이터.** 대규모 분석, 장기 이력. D1은 한도에 가까워진다. 이것도 *Hyperdrive 너머의 Postgres* 또는 분석 전용 DB가 답이다.

**4. cross-region 트랜잭션이 필요한 자리.** 한국과 유럽의 데이터를 한 트랜잭션 안에서 다뤄야 한다면 KV·D1 모두 답이 아니다. *외부 분산 DB(CockroachDB, Spanner) 또는 사가 패턴*으로 풀어야 한다.

**5. 강한 region lock이 요구되는 자리.** 한국 데이터는 한국에만 둬야 하는 컴플라이언스 워크로드. D1 location hint가 일부 도움이 되지만, 글로벌 분산 자체가 모델의 정체성이라 완전한 region lock은 어렵다. 이건 *AWS RDS in ap-northeast-2를 그대로 유지하고 Hyperdrive로 앞에만 두는 패턴*이 가장 깔끔하다.

다섯 가지 모두 *Cloudflare를 쓰지 말라*는 결론이 아니다. *컴퓨트는 Workers, 데이터는 RDS — 하이브리드*가 거의 항상 가능하다는 게 이 책의 핵심 메시지다. 14장에서 이 패턴을 8단계 시퀀스로 풀어낼 텐데, 그 시퀀스의 데이터 부분이 바로 이런 결정의 연속이다. *옮길 데이터와 남길 데이터를 가른다.*

## 이 기술이 무너지는 자리

이 장의 마지막은 정직한 한계로 닫자. KV·D1·둘의 조합이 무너지거나 거짓 안심을 주는 자리들을 한 화면에 모아 두자.

- **KV의 secondary index 부재.** 가장 자주 만나는 함정이다. DynamoDB GSI를 기대하고 옮기면 거의 반드시 사고가 난다. Liftosaur 사례가 그 증거다. 단일 키 lookup으로 풀 수 없는 쿼리가 보인다면 KV는 답이 아니다.
- **KV의 60초 전파.** 같은 사용자가 한 PoP에서 쓰고 다른 PoP에서 1분 안에 읽는 시나리오라면 옛 값을 볼 수 있다. 멀티 디바이스·멀티 region 사용자가 많은 워크로드에서는 이 함정을 잊지 말자.
- **KV의 per-key 1 write/s.** 카운터·실시간 통계는 KV의 자리가 아니다. Durable Objects로 가자.
- **D1의 10GB 한도.** 작은 SaaS에는 충분하지만, 데이터가 크게 자랄 가능성이 있다면 처음부터 Postgres + Hyperdrive로 시작하는 편이 낫다. 10GB에 가까워진 다음 옮기는 건 거의 항상 야간작업이 된다.
- **D1의 sustained write 500~2k/s.** spike-y 트래픽은 견디지만 sustained 부담은 못 견딘다. write-heavy 워크로드는 RDS·Aurora를 그대로 두고 Hyperdrive로 앞에 두자.
- **둘 다 cross-region 트랜잭션 없음.** 한 트랜잭션이 두 region 데이터를 동시에 다뤄야 한다면 KV·D1 모두 답이 아니다.
- **KV·D1 사이의 트랜잭션 없음.** "세션은 KV, 사용자는 D1"이라는 자연스러운 분리가 한 가지 함정을 함께 가져온다 — *둘을 한 번에 일관되게 갱신하는 트랜잭션이 없다.* 보통은 D1을 source of truth로 삼고 KV를 캐시로 쓰는 패턴이 안전하다.
- **백업·DR의 운영 안전망.** D1의 Time Travel은 30일 PITR이라 든든하지만, KV의 백업·복원은 도구가 약하다. KV에 의존하는 핵심 데이터는 별도 백업 sink(R2 export 등)를 운영적으로 마련해 두자.

이 여덟 가지를 외워 두자. 외운다는 건 모든 케이스에서 거부하라는 뜻이 아니다. *시스템 설계 회의에서 이 여덟 가지가 적용되는지 한 번씩 점검하라*는 뜻이다. 점검 한 번이 6개월 뒤의 회귀를 막는다.

## 마무리 — 다음 장으로

자, 이번 장에서 우리는 무엇을 손에 쥐었나. KV의 본질과 한계, D1의 본질과 한계, 둘 사이의 5축 의사결정 표, 그리고 둘 다 답이 아닐 때 어디로 가야 하는지의 지도. 6장에서 만든 사용자 API는 이제 *세션은 KV, 사용자·프로필은 D1 + Drizzle*로 진화했다. 마이그레이션 한 사이클까지 손으로 돌아봤다. 깃 브랜치로 `ch7-data` 체크포인트를 남겨 두자.

그런데 우리가 아직 만나지 못한 자리가 둘 있다. *빈번한 쓰기 + 강한 일관성*과 *큰 파일·미디어*다. KV·D1 둘 다 답이 아니라고 위에서 미뤄 둔 자리들이다. 다음 장에서 그 두 자리를 채울 두 제품을 만난다 — *Durable Objects*와 *R2*다.

Durable Objects는 actor 모델로 한 객체에 한 인스턴스를 보장하는 묘한 도구다. 채팅방, 재고, 좌석 예약, 실시간 협업 문서가 그 자리다. WebSocket Hibernation API라는 비용 모델을 뒤집는 한 수도 함께 만난다. R2는 S3 호환의 글로벌 객체 저장소인데, *egress free*라는 한 줄이 미디어 워크로드의 청구서를 어떻게 다시 쓰는지 보게 된다.

8장에서는 `toby-shop`에 고객지원 채팅방 Worker를 한 개 더 띄우고, 채팅 메시지는 DO storage에, 첨부 파일은 R2 presigned URL로 받는 한 사이클을 손으로 만들어 보자. 자, 다음 장으로 가보자.
