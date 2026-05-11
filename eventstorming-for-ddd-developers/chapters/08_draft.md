# 8장. Read Model과 프론트엔드 — 화면은 어디서 만들어지나

7장에서 우리는 `OrderPlaced` 이벤트가 Kafka까지 흘러나가는 동맥을 완성했다. 그러면 이제 *반대 방향*을 따라가보자. 고객이 자기 마이페이지에 들어와 "내 주문 목록"을 누른다. 그 순간, *어떤 데이터가 어디서 만들어져 어떻게 화면에 도달하는가*?

답은 사실 우리가 4장에서 잠시 미뤄둔 박스 안에 있다. **Read Model**. 워크숍 벽에서 *초록색*(또는 형광 노랑)으로 그어둔 그 박스. Brandolini가 "결정을 위해 읽는 정보"라고 정의한 그것. 이번 장에서 그 박스가 정말로 *React Query 캐시*와 *Next.js Server Component*로 환생하는 풍경을 본다.

## 8.1 Read Model은 왜 *별도 모델*인가

먼저 한 가지 자문해보자. `Order` Aggregate를 우리가 이미 6장에서 잘 만들어두었는데, *왜* 화면을 위한 별도 모델이 또 필요한가? Repository에서 `findById()`로 꺼내서 JSON으로 직렬화하면 안 되나?

작은 시스템에서는 *그래도 된다*. 다만 시스템이 자라기 시작하면 그 길은 *반드시* 진흙탕에 빠진다. 이유는 셋이다.

**첫째, 화면이 요구하는 데이터의 결이 다르다.** 주문 목록 화면은 *Order 하나당 한 줄*만 필요하다 — 주문번호, 총액, 상태, 대표 상품명. 그러나 Aggregate는 `OrderLine` 컬렉션 전체를 들고 있다. 100개의 Order를 그리려면 *100번의 lazy loading*이 일어나거나, *모든 라인을 통째로* 가져온다. 어느 쪽이든 비효율적이다.

**둘째, 여러 Aggregate가 한 화면에 모인다.** 사용자의 "주문 상세" 화면에는 Order의 정보뿐 아니라 결제 정보, 배송 상태, 상품 이미지가 함께 나와야 한다. 6장에서 우리는 이것들을 *서로 다른 Aggregate*로 잘랐다. 화면을 그리려고 4개의 Aggregate를 *동시에 조회*하면, 그건 사실상 *write 쪽 모델*을 *read 쪽 용도로 끌어다 쓰는* 모양이다. Servienti가 경계한 그 길이 다시 열린다.

**셋째, 읽기와 쓰기의 부하 패턴이 다르다.** 주문 목록 조회는 쓰기보다 *수십 배 자주* 일어난다. 그리고 *수십 ms 단위*의 응답이 필요하다. 같은 모델이 두 패턴을 동시에 책임지면, 결국 둘 다 어색해진다.

이 세 가지 이유가 모이면 결론은 하나다. **read 쪽은 별도 모델이다.** 별도 테이블이거나, 별도 view거나, 별도 서비스거나. 어느 형태든 *write Aggregate와 다른 모델*이다. 이 분리가 CQRS(Command Query Responsibility Segregation)의 핵심이고, EventStorming의 초록 sticky가 *별도로* 그려진 이유다.

Brandolini가 *Modeling Aggregates* 챕터 끝에서 단호하게 짚는다 — "*data to be displayed to a user in order to make a decision* will be a **Read Model**. Aggregates are something else" [B §4831]. 화면에 보이는 것을 *내부 모델 구조 위에 겹쳐 놓으려는* 그 본능을 경계해야 한다.

## 8.2 Read Model의 자리 — 네 가지 선택지

Read Model을 *어디에* 만들 것인가? 선택지는 크게 넷이다.

**선택지 1. 같은 DB의 별도 SELECT/Repository.** Write와 같은 테이블을 읽지만, *읽기 전용 인터페이스*로 분리한다. 6장의 `FindOrderQuery` inbound port가 정확히 이 자리다.

```java
// orders/domain/port/in/FindOrderQuery.java
public interface FindOrderQuery {
    List<OrderSummary> listMyOrders(CustomerId customerId, int page);
    Optional<OrderDetail> findDetail(OrderId orderId);

    record OrderSummary(OrderId id, String displayName, Money total, OrderStatus status, Instant placedAt) {}
    record OrderDetail(...) {}
}
```

가장 단순하고, 첫 단계로 적합하다. write 모델과 같은 DB를 본다.

**선택지 2. DB View / Materialized View.** 쿼리가 복잡해지기 시작하면, 그 복잡도를 *DB 안*으로 밀어 넣는다. PostgreSQL의 materialized view는 *별도 저장된* 결과를 가지므로 조회가 빠르다. 다만 갱신 트리거를 챙겨야 한다.

**선택지 3. 별도 read-side 테이블 + projection.** Domain Event를 받아서 *별도 테이블*에 read 형태로 미리 적어둔다. 화면이 그 테이블만 본다. 가장 *완전한 CQRS*이고, 가장 빠르다. 다만 *projection 코드*를 따로 유지해야 한다.

**선택지 4. Kafka Streams / 별도 read service.** 여러 모듈/서비스의 이벤트를 *한 군데에 모아서* 읽기 전용 view를 만든다. 마이크로서비스 아키텍처가 본격화된 단계에서 등장한다.

선택의 가이드라인은 다시 단순하다 — *필요해질 때까지 미루자*.

처음 출발하는 팀은 **선택지 1**으로 충분하다. write와 같은 DB를 읽되, port만 분리해두자. 같은 모듈 안의 `FindOrderQuery`가 그대로 화면에 응답한다. 한 화면에 여러 Aggregate가 모여야 한다면, *Application Service*가 여러 query port를 조합한다.

쿼리가 느려지거나 화면 응답이 늦어지기 *시작할 때*, **선택지 2** 또는 **선택지 3**으로 옮긴다. 그 시점이 오기 전에 미리 분리하면, *복잡도만* 사고 *이득은* 못 본다. 일찍 만든 read service는 거의 항상 *재설계*된다.

## 8.3 Domain Event를 받아 projection으로 — 선택지 3의 자세한 그림

선택지 3을 한번 자세히 살펴보자. 도메인 이벤트가 흐르는 모듈에서, 그 이벤트를 받아 read 테이블을 *유지*하는 모양이다.

```java
// orders/adapter/out/read/OrderReadProjection.java
@Component
@RequiredArgsConstructor
class OrderReadProjection {

    private final OrderSummaryRepository readRepo;

    @ApplicationModuleListener
    @Transactional
    void on(OrderPlaced event) {
        OrderSummaryRow row = new OrderSummaryRow();
        row.setOrderId(event.orderId().value());
        row.setCustomerId(event.customerId().value());
        row.setTotal(event.totalAmount().amount());
        row.setStatus("PLACED");
        row.setPlacedAt(event.occurredAt());
        readRepo.save(row);
    }

    @ApplicationModuleListener
    @Transactional
    void on(OrderPaid event) {
        readRepo.findById(event.orderId().value())
            .ifPresent(row -> row.setStatus("PAID"));
    }

    @ApplicationModuleListener
    @Transactional
    void on(OrderShipped event) {
        readRepo.findById(event.orderId().value())
            .ifPresent(row -> {
                row.setStatus("SHIPPED");
                row.setShippedAt(event.occurredAt());
            });
    }
}
```

이 projection이 *살아 있는* 데이터를 만든다. write 쪽 Aggregate가 무언가를 할 때마다, 이벤트가 흐르고, projection이 자기 read 테이블을 *갱신*한다. 화면은 *오직 이 테이블*만 본다. 단순한 SELECT 하나로 모든 게 끝난다.

여기서 한 가지 짚어두자. 이 projection은 *eventually consistent*다. write 트랜잭션이 commit된 직후, projection 트랜잭션이 *별도로* 실행된다. 그 사이 *몇 ms 동안* read 테이블은 옛 상태다. 사용자가 주문 직후 마이페이지를 *0.1초 안에* 새로고침하면, 자기 새 주문이 *아직 안 보일 수 있다*.

이게 문제인가? 대부분의 도메인에서는 *문제가 아니다*. 다만 *문제가 되는 자리*는 명확히 알아야 한다. "주문 완료 페이지"는 결제 직후 *반드시* 해당 주문이 보여야 한다. 그런 자리에서는 *write 쪽 query port*를 그대로 호출하거나, 화면에 *낙관적 갱신*을 한 번 끼워 넣는다. 두 전략은 잠시 뒤 React Query 절에서 자세히 본다.

## 8.4 Read Model을 화면까지 — Next.js App Router와 RSC

이제 그 read model이 *화면*까지 가는 길을 따라가보자. 최근의 React 생태계에서 가장 자연스러운 길은 Next.js App Router의 **React Server Components (RSC)**다.

RSC가 무엇을 약속하는가? *서버에서만 실행되는 컴포넌트*다. SQL을 직접 호출하든, HTTP로 backend를 부르든, *서버 안*에서 데이터를 가져와 markup을 만든다. 클라이언트에는 *완성된 HTML*과 *최소한의 JavaScript*만 흘러나간다. CQRS의 read side projection이 *그대로* RSC가 되는 그림이 자연스럽다.

가장 단순한 모양을 살펴보자.

```tsx
// app/orders/page.tsx — Server Component
import { ordersApi } from '@/lib/orders-api';

export default async function OrdersPage() {
  const orders = await ordersApi.listMyOrders();   // 서버에서 backend 호출

  return (
    <div>
      <h1>내 주문</h1>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            <a href={`/orders/${order.id}`}>
              {order.displayName} — {order.total.formatted} — {order.status}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

`async function`을 컴포넌트로 쓴다는 게 처음에는 *어색하다*. 그러나 이 한 줄이 시사하는 바는 크다 — *fetch가 컴포넌트 트리에 자연스럽게 녹는다*. 별도 `useEffect`, 별도 loading state, 별도 client-side data fetching 코드 없이, 서버에서 *동기적으로* 데이터를 가져와 그대로 markup이 된다.

`ordersApi.listMyOrders()`가 어떻게 생겼나? Spring backend의 query endpoint를 부르는 가벼운 함수다.

```ts
// lib/orders-api.ts
import { cookies } from 'next/headers';

const API_BASE = process.env.BACKEND_URL!;

export const ordersApi = {
  async listMyOrders(): Promise<OrderSummary[]> {
    const session = cookies().get('session')?.value;
    const res = await fetch(`${API_BASE}/orders/me`, {
      headers: { 'X-Session': session ?? '' },
      next: { revalidate: 30, tags: ['orders'] },   // ← Next.js fetch 캐시
    });
    if (!res.ok) throw new Error('주문 조회 실패');
    return res.json();
  },
};
```

`next: { revalidate: 30, tags: ['orders'] }`가 핵심이다. Next.js가 이 fetch 결과를 *서버 쪽 캐시*에 저장한다. 같은 페이지가 다음 요청에서 다시 그려질 때, 30초 동안은 *backend를 다시 부르지 않는다*. 캐시된 응답이 그대로 흐른다.

`tags: ['orders']`는 *명시적인 무효화*를 위한 표식이다. 사용자가 새 주문을 하면, 그 요청 끝에 `revalidateTag('orders')`를 호출해 이 캐시를 *통째로* 날린다. 다음 페이지 요청은 *신선한 데이터*를 본다.

이 두 줄(`revalidate`와 `tags`)이 Next.js가 *서버 쪽 read model 캐시*를 제공하는 방식이다. 우리가 backend에 별도 캐싱을 구축하지 않아도, frontend가 *한 겹의 read 캐시*를 더 가지고 있는 셈이다.

## 8.5 React Query — 클라이언트 측의 read model 캐시

RSC만으로 모든 화면이 끝나면 좋겠지만, 현실은 그렇지 않다. *인터랙티브한* 컴포넌트가 필요한 자리가 있다. 무한 스크롤, 필터, 모달 안의 검색, 낙관적 갱신. 이런 자리에서는 *클라이언트 컴포넌트*가 필요하고, 그 컴포넌트는 *자기만의 캐시*가 필요하다.

여기서 등장하는 게 **TanStack Query**(예전 React Query)다. 한 줄로 요약하자면 — *서버 상태 캐시*. 우리가 다루는 read model이 결국 "서버에 있는 상태의 *지역적 복사본*"이라는 관점이다.

```tsx
// app/orders/[id]/order-actions.tsx — Client Component
'use client';

import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';

export function OrderActions({ orderId }: { orderId: string }) {
  const queryClient = useQueryClient();

  const { data: order } = useQuery({
    queryKey: ['orders', orderId],
    queryFn: () => fetchOrder(orderId),
    staleTime: 10_000,   // 10초 동안은 신선하다고 간주
  });

  const cancelMutation = useMutation({
    mutationFn: () => cancelOrder(orderId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders', orderId] });
      queryClient.invalidateQueries({ queryKey: ['orders'] });   // 목록도
    },
  });

  if (!order) return <div>로딩 중…</div>;

  return (
    <div>
      <p>현재 상태: {order.status}</p>
      {order.status === 'PLACED' && (
        <button
          onClick={() => cancelMutation.mutate()}
          disabled={cancelMutation.isPending}
        >
          주문 취소
        </button>
      )}
    </div>
  );
}
```

이 코드에서 한 가지 짚어두자. `queryKey: ['orders', orderId]`는 *read model의 식별자*다. 같은 키를 가진 query는 같은 캐시 entry를 공유한다. 만약 이 주문 상세 페이지가 *여러 탭에서 동시에* 열려 있어도, 한 곳에서 `invalidateQueries`를 부르면 *모든 인스턴스*가 다시 fetch한다.

`staleTime: 10_000`은 *재요청을 막는 보호막*이다. 10초 안에 같은 query가 다시 호출되면(예: 사용자가 탭을 빠르게 이동하면), 캐시된 값을 그대로 쓴다. 이게 없으면 사소한 리렌더링마다 backend를 두드린다.

`useMutation`의 `onSuccess` 콜백이 *진짜 read model의 갱신 트리거*다. 주문 취소가 성공하면 — 두 가지 캐시(`['orders', orderId]`와 `['orders']` 목록)를 *무효화*한다. 다음에 어느 컴포넌트가 그 query를 쓰면, *fresh 데이터*를 받는다.

## 8.6 Domain Event는 어떻게 화면까지 흐르나

여기서 처음 자문이 다시 돌아온다. 워크숍에서 본 그 주황색 sticky `OrderPlaced`가, 정말로 *화면 캐시까지* 어떻게 흐르나?

흐름을 정리해보자.

```
[사용자가 주문 버튼 클릭]
     ↓
[mutation: placeOrder]
     ↓
[backend: PlaceOrderService] @Transactional
     ↓
[Order.place() → registerEvent(OrderPlaced)]
     ↓
[DB commit]
     ↓
[OrderReadProjection.on(OrderPlaced)]                ← read 테이블 갱신
     ↓
[mutation 응답]
     ↓
[onSuccess: queryClient.invalidateQueries(['orders'])]   ← 클라 캐시 무효화
     ↓
[다음 렌더: 주문 목록을 다시 fetch]
     ↓
[backend가 새로운 read row 반환]
     ↓
[화면 갱신]
```

이 흐름이 *완성된 사이클*이다. **워크숍의 sticky 한 장이 시스템의 *한쪽 끝(write)*에서 *반대쪽 끝(view)*까지 흐른다.** 5장부터 8장까지 우리가 잇고 있던 그 다리가, 이 한 사이클로 마무리된다.

여기서 한 가지 알아두자. `invalidateQueries`는 *클라이언트 쪽*의 무효화다. *다른 사용자*의 브라우저에 열린 같은 페이지에는 영향이 없다. 만약 *실시간*으로 다른 사용자에게도 변화가 보여야 한다면, WebSocket이나 Server-Sent Events 같은 *push 채널*을 추가해야 한다. Domain Event가 backend에서 Kafka로 흐른 뒤, 별도 *notification service*가 그 이벤트를 WebSocket으로 다시 흘려보내는 식이다. 이건 도메인에 따라 *반드시 필요한 일은 아니다* — 대부분의 이커머스 시나리오에서는 polling/revalidate로 충분하다.

## 8.7 낙관적 갱신 — *기다리지 않는* 화면

한 가지 더 짚고 가자. 사용자가 "주문 취소" 버튼을 누른 뒤, *backend의 응답을 기다리는 1초*가 어떻게 느껴지나? 불안하고, 답답하다. 화면이 *얼어붙은 듯한* 1초가 사용자 경험을 망친다.

이때 쓰는 패턴이 **낙관적 갱신(optimistic update)**이다. mutation을 부르는 *즉시* 캐시를 *예측된 상태*로 바꿔놓고, 실제 응답이 오면 *확정* 또는 *롤백*한다.

```tsx
const cancelMutation = useMutation({
  mutationFn: () => cancelOrder(orderId),

  onMutate: async () => {
    await queryClient.cancelQueries({ queryKey: ['orders', orderId] });
    const previous = queryClient.getQueryData(['orders', orderId]);

    queryClient.setQueryData(['orders', orderId], (old: Order) => ({
      ...old, status: 'CANCELLING'
    }));

    return { previous };   // 롤백용 백업
  },

  onError: (err, _vars, context) => {
    queryClient.setQueryData(['orders', orderId], context?.previous);
  },

  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['orders', orderId] });
  },
});
```

`onMutate`가 *발사 직전*에 호출된다. 캐시를 *낙관적 상태*로 즉시 바꾼다. 사용자는 클릭 즉시 "CANCELLING"으로 바뀐 화면을 본다. 그 뒤 backend의 응답이 오면, `onSettled`에서 *확정 무효화*가 일어나 *진짜 데이터*로 교체된다. 실패하면 `onError`에서 *백업으로 되돌린다*.

이 패턴이 *기본*은 아니다. 화면이 *너무 빠르다고 거짓말하면* 오히려 신뢰가 깨진다. 다만 *짧은 동작*에 한해서는 사용자 경험을 크게 끌어올린다. 어느 자리에 이 패턴을 쓸지, 팀이 *의식적으로* 결정하는 게 중요하다.

## 8.8 BFF와 GraphQL — 짧은 사이드바

여기서 한 단락만 BFF(Backend for Frontend)와 GraphQL을 짚자. 화면이 *여러 도메인을 동시에* 보여줘야 한다면, frontend가 *여러 backend endpoint를 동시에 호출*해야 한다. 이게 점점 부담스러워지면 BFF가 등장한다 — frontend 전용 backend가 *조합 API*를 제공한다. tRPC, GraphQL, Next.js API routes가 그 자리를 채운다.

다만 한 가지 균형을 잡자. Rodrigo Estrada가 짚는 우려가 있다 — *"When BFF and GraphQL Add More Complexity Than Solutions"*. 도메인 경계가 *흔들리는 시점에* BFF/GraphQL을 들이면, *모든 도메인의 어색함*이 frontend의 schema 한 군데에 모인다. 그게 더 큰 진흙탕이다.

가이드라인은 단순하다 — **BFF는 도메인 경계가 *충분히 단단해진 다음*에 추가하자**. 처음에는 RSC + 직접 fetch + React Query면 충분하다. 화면이 자라고 *조합의 부담*이 보이기 시작할 때, BFF를 *얇게* 추가한다. 큰 GraphQL 게이트웨이는 마지막 선택지다.

## 8.9 한 표로 정리 — sticky 색깔과 frontend의 자기 자리

6장의 표를 frontend까지 확장해서 정리하자.

| 워크숍 sticky | 색깔 | Spring 쪽 | Next.js / React 쪽 |
|---|---|---|---|
| Domain Event | 주황 | `registerEvent()` + Kafka | `revalidateTag()`, `invalidateQueries()` 트리거 |
| Command | 파랑 | `PlaceOrderUseCase` | mutation 함수 |
| Aggregate | 노랑 | `@Entity` Aggregate Root | (도메인 객체, 화면에 *직접* 노출하지 않음) |
| Policy | 라일락 | `@ApplicationModuleListener` | (frontend에 직접 매핑되지 않음) |
| Read Model | 초록 | `FindOrderQuery` + projection | RSC fetch + React Query cache |
| External System | 분홍 | outbound adapter | (Stripe Element 같은 widget이 가끔) |
| Hotspot | 핫핑크 | (코드의 *재모델링 후보*) | (UX 마찰점 = 9장의 한국 사례) |

이 표가 *책의 전 구간*에서 한 줄로 이어지는 매핑이다. 다음에 워크숍에서 sticky를 마주칠 때, *어느 색이 어느 자리에 가는지*가 머릿속에 그려진다. 그게 5~8장이 약속한 다리의 *완성된 모습*이다.

## 마무리 — 화면은 *마지막 호흡*이다

8장이 한 일을 정리하자. Read Model이 왜 별도 모델인지 짚고, 그 자리의 선택지 네 가지를 봤다. Domain Event를 받아 projection을 유지하는 코드를 잡았고, *eventually consistent*의 비용을 명시했다. Next.js App Router의 RSC로 read model을 화면에 *자연스럽게* 흘리는 방식을 익히고, React Query로 클라이언트 측 캐시를 *식별자(`queryKey`) + 무효화 트리거*로 다루는 모양을 손에 익혔다. 낙관적 갱신과 BFF/GraphQL의 *적정 시점*까지 의식적으로 짚었다.

이쯤에서 우리는 *코드의 방*을 통과했다. 5장에서 Pivotal Event로 칼을 들고 들어와, 6장에서 Aggregate를 만들고, 7장에서 이벤트를 시스템의 동맥으로 흐르게 하고, 8장에서 그 동맥이 *화면까지* 도달하는 모습을 봤다. 워크숍의 sticky 한 장 한 장이, IDE의 *명확한 자리*를 가진다.

그러나 코드만 깔끔하게 만들어진다고 *팀의 일*이 바뀌지는 않는다. 워크숍의 핫핑크 sticky(hotspot)는 어떻게 다음 스프린트의 우선순위가 되나? 워크숍을 *원격에서* 돌리려면 무엇이 필요한가? 그리고 facilitator로서 우리가 가장 자주 빠지는 함정은 어디인가? *코드의 방*에서 통과한 우리가, *팀의 방*으로 옮겨가야 할 차례다.

다음 장에서 워크숍의 hotspot이 PR backlog로 옮겨가는 짧은 다리를 건너자.
