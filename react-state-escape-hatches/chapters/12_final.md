# 12장. Effect가 필요 없을 때 — 가장 자주 쓰는 안티패턴들

## 들어가는 이야기 — 46%라는 숫자

리액트 코어 팀에서 오래 일했던 댄 아브라모프는 한 인터뷰와 트윗에서 충격적인 숫자를 흘린 적이 있다. 메타 내부의 어느 코드베이스를 표본 삼아 `useEffect` 호출을 하나하나 들여다봤더니, 절반에 가까운 — 대략 46% 정도의 — effect들이 사실은 **필요 없었다**는 이야기였다. 즉 굳이 effect로 짤 필요가 없는 일을 effect로 짜놓고 있었다는 뜻이다. 메타 내부의, 그 리액트를 만든 사람들이 짠 코드의 절반 가까이가 그랬다는 거다.

이 숫자를 처음 들으면 두 가지 반응이 동시에 나온다. 하나는 "그럼 우리 코드는 도대체 몇 퍼센트일까" 하는 등골 서늘함이고, 다른 하나는 "그 정도면 도구 자체가 잘못 설계된 것 아닌가" 하는 의심이다. 실제로 트위터와 한국 커뮤니티에서도 비슷한 논쟁이 자주 벌어진다. 한쪽에서는 "이런 가이드 문서가 길어진다는 것 자체가 API 설계의 흠이다, 결국 사람을 가스라이팅하는 거다"라고 비판하고, 다른 쪽에서는 "이건 도구의 문제가 아니라 사용자가 도구의 의미를 잘못 잡은 거다, useEffect의 이름이 너무 일반적이어서 그렇지 본질은 동기화일 뿐이다"라고 옹호한다.

어느 쪽이든 일리가 있다. 이름이 너무 두루뭉술해서 잘못된 직관을 부르는 건 사실이고, 동시에 사용자의 사고 모델이 흔들리는 것도 사실이다. 하지만 우리가 이 챕터에서 하려는 일은 그 논쟁의 어느 한 편에 서는 게 아니다. 도구를 비판하는 것도 아니고, 도구를 옹호하는 것도 아니다. 그저 **도구 사용을 검정**해보려는 거다. 내 손으로 짠 effect들 중에 어느 것이 진짜 필요한 effect이고 어느 것이 그렇지 않은지를, 직접 가려낼 수 있는 눈을 갖추는 게 목표다.

11장에서 우리는 이미 효과적인 자가 진단 한 줄을 익혔다. "이 effect를 지웠을 때 무엇이 깨지는가?"라는 질문이다. 답이 "외부 세계와 동기화되어 있던 무언가가 어긋난다"라면 그 effect는 진짜 effect다. 그렇지만 답이 "음... 사실 그냥 다음 렌더에서 같은 값이 다시 계산될 텐데"라거나 "어차피 그 핸들러 안에서 같이 처리해도 되는 일인데"라면, 그 effect는 46% 그룹 안에 들어 있을 가능성이 매우 높다.

이 챕터에서 다룰 안티패턴들은 거의 전부 이 한 줄짜리 진단으로 걸러낼 수 있는 것들이다. 다만 패턴을 한 번도 본 적 없으면 알아채는 게 쉽지 않다. 그래서 우리는 흔한 함정 일곱 가지를 두 묶음으로 나누어 차례차례 살펴볼 거다. 묶음 A는 **렌더 중에 풀 수 있는 문제들**이고, 묶음 B는 **이벤트 핸들러로 풀 수 있는 문제들**이다. 그리고 마지막에 4장에서 이미 본격 처방한 prop 변화 리셋 문제를 짧게 회수하고, 한국 커뮤니티에서 자주 보이는 무한 루프 패턴을 빠르게 진단해본 다음 마무리한다.

준비물은 단 하나다. effect를 보면 자동으로 묻게 되는 습관을 기르자. **"이걸 지우면 뭐가 깨지지?"** 이 질문에 분명한 답이 떠오르지 않는다면, 거기에 effect가 있을 자리는 없다.

## 묶음 A — 렌더 중에 풀 수 있는 문제

### 안티패턴 #1. 파생값을 state + effect로 보관하기

가장 자주 보이는, 그리고 가장 알아채기 쉬운 안티패턴부터 살펴보자. 어떤 값이 다른 값으로부터 곧장 계산될 수 있을 때, 그 결과를 굳이 별도의 state로 저장하고 effect로 동기화하는 패턴이다. 예를 들어보자.

```tsx
// 안티패턴: 파생값을 state + effect로 동기화
function UserList({ users }: { users: User[] }) {
  const [activeUsers, setActiveUsers] = useState<User[]>([]);
  const [count, setCount] = useState(0);

  // 🚨 users가 바뀔 때마다 effect로 다시 계산해서 state에 저장
  useEffect(() => {
    const filtered = users.filter((u) => u.active);
    setActiveUsers(filtered);
    setCount(filtered.length);
  }, [users]);

  return (
    <div>
      <p>활성 사용자 {count}명</p>
      <ul>
        {activeUsers.map((u) => (
          <li key={u.id}>{u.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

언뜻 보기엔 깔끔해 보인다. `users`가 바뀌면 effect가 돌고, 거기서 활성 사용자만 걸러내서 `activeUsers`에 넣고, 개수도 같이 갱신한다. 동기화가 잘 되어 있는 것처럼 느껴진다.

하지만 잠깐 멈춰서 생각해보자. 여기서 `activeUsers`와 `count`는 **언제 어떤 모습이어야 하는가?** 답은 단순하다. "지금 받은 `users`로부터 계산되는 그 값"이다. `users`가 바뀌면 같이 바뀌어야 하고, `users`가 그대로면 같이 그대로다. 즉 `users`로부터 직접 결정되는 종속변수일 뿐이다.

종속변수에 별도의 저장 공간을 마련하면 무슨 일이 벌어지는가? 첫째, **렌더가 한 번 더 일어난다.** 부모가 새로운 `users`를 내려보내면 `UserList`가 한 번 렌더되고, 그 직후에 effect가 돌아 `setActiveUsers`와 `setCount`를 호출하고, 그러면 또 한 번 렌더된다. 사용자에게 보이는 첫 번째 렌더에는 **이전의 `activeUsers`와 새 `users`가 섞여 있다.** 화면이 한 프레임이라도 어긋난 상태로 깜박일 수 있다. 둘째, 두 state를 따로 관리하니 둘 사이의 정합이 어긋날 가능성이 늘 도사린다. 셋째, 코드를 읽는 사람은 "이 `count`가 정확히 무엇의 개수지?"라고 한 번 더 묻게 된다. 굳이 의문을 만들 필요가 없는데도 만들어버린 셈이다.

처방은 너무 간단해서 허무할 정도다. **렌더 중에 그냥 계산하자.**

```tsx
// 바른 패턴: 렌더 중에 직접 계산
function UserList({ users }: { users: User[] }) {
  // 종속변수는 변수다. state가 아니다.
  const activeUsers = users.filter((u) => u.active);
  const count = activeUsers.length;

  return (
    <div>
      <p>활성 사용자 {count}명</p>
      <ul>
        {activeUsers.map((u) => (
          <li key={u.id}>{u.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

state가 두 개 사라졌고, effect가 사라졌고, 의존성 배열이 사라졌다. 코드가 짧아졌고, 이상하게도 더 정확해졌다. 왜냐하면 `users`로 화면이 그려지는 모든 순간에 `activeUsers`와 `count`는 자동적으로 그 `users`와 정확히 일치하기 때문이다. 어긋날 수 있는 틈이 아예 닫혀 있다.

여기서 흔히 나오는 반론 하나를 미리 막아두자. "그래도 매번 `filter`를 호출하면 비효율적이지 않나?" 라는 질문이다. 이 반론은 자주 등장하는데, 두 가지 단계로 답하자. 첫째, **거의 모든 경우에 그 비용은 무시해도 된다.** 사용자 100명이든 1000명이든 `filter` 한 번 도는 비용은 0.1ms 안쪽이다. 그게 신경 쓰일 정도라면 이미 거기엔 다른 문제가 있을 가능성이 더 높다. 둘째, **정말로 무거운 계산이라면 그건 useMemo의 자리다.** 그리고 useMemo 역시 effect와 다르게 렌더 중에 계산을 끝낸다. 잠시 후 자세히 본다.

기억해두자. 이 글에서 지금부터 100번쯤 반복할 명제 하나를 미리 던져둔다. **종속변수는 변수로, 독립변수만 state로.**

### 안티패턴 #2. 비싼 계산을 effect + state로

방금 언급한 비싼 계산 이야기를 본격적으로 풀어보자. 여기 거대한 데이터를 정렬하고 필터링하는 화면이 있다고 해보자.

```tsx
// 안티패턴: 비싼 계산을 effect로 옮기기
function Dashboard({ rows, query }: { rows: Row[]; query: string }) {
  const [filtered, setFiltered] = useState<Row[]>([]);

  // 🚨 비싼 계산이라서 effect에 넣었다고 한다. 그런데 정말?
  useEffect(() => {
    const result = expensiveFilterAndSort(rows, query);
    setFiltered(result);
  }, [rows, query]);

  return <Table data={filtered} />;
}
```

겉으로는 "무거운 계산은 effect로 빼야 화면이 안 멈춘다"라는 그럴듯한 이유로 짠 코드다. 그런데 잠시 생각해보자. effect는 **렌더가 끝난 다음에** 돈다. 즉 화면은 이미 한 번 그려졌다 — 정확히는 `filtered`가 비어 있거나 이전 값인 채로 한 번 그려진 것이다. 그 다음에 effect가 돌면서 새 `filtered`를 만들고 set을 호출하면, 다시 렌더가 트리거되고 거기서 비로소 옳은 값으로 화면이 그려진다.

잠깐. 그러면 effect로 옮긴 게 도움이 됐는가? 무거운 계산은 어차피 메인 스레드에서 돌고 있다 — 단지 그 계산이 첫 렌더 **다음에** 돌 뿐이다. 화면이 안 멈추는 게 아니라, 화면을 한 번 잘못 그려놓고 그 뒤에 멈추는 거다. 사용자 입장에서는 "한 번 깜박이고 → 잠깐 멈췄다가 → 새 결과가 뜬다"가 된다. 더 나빠졌다고 봐도 된다.

처방은 두 가지다. 첫째, 정말로 가벼운 계산이면 안티패턴 #1처럼 **그냥 렌더 중에 계산하자.** 둘째, 측정해봤더니 진짜로 무거운 계산이라면, **`useMemo`가 그 자리에 있다.** useMemo는 effect와 달리 렌더 중에 계산이 끝나며, 의존성이 바뀌지 않은 동안에는 같은 값을 그대로 반환한다.

```tsx
// 바른 패턴: useMemo로 렌더 중에 캐싱
function Dashboard({ rows, query }: { rows: Row[]; query: string }) {
  // 의존성이 바뀌지 않은 동안에는 캐시된 결과를 그대로 쓴다.
  const filtered = useMemo(
    () => expensiveFilterAndSort(rows, query),
    [rows, query],
  );

  return <Table data={filtered} />;
}
```

여기서 한 가지 주의해야 할 게 있다. **useMemo를 반사적으로 두르지는 말자.** "useMemo는 비싼 계산을 위한 도구다"라는 한 문장 정의는 가벼운 곳에 두면 손해가 더 크다. useMemo 자체에도 의존성 비교 비용과 클로저 보존 비용이 있고, 무엇보다 코드가 무거워 보인다. 일반적인 합의는 이렇다. **먼저 측정한다.** 개발자 도구의 Profiler나 `console.time`으로 그 계산이 실제로 사람이 인지할 만큼 — 대개 16ms 이상 — 걸리는지 확인하고, 그 다음에 useMemo를 도입하자.

여담으로, React Compiler가 보편화되면 이 고민의 상당 부분이 사라질 거라고들 말한다. 자동으로 메모이제이션을 깔아주기 때문이다. 그렇지만 그 시점에도 effect는 effect의 자리에 있고, useMemo의 자리는 useMemo가 차지한다. 자동화는 결정의 노동을 줄여줄 뿐, 결정의 의미를 바꾸지는 않는다.

### 안티패턴 #5. cascading effects (A → state → B → state → A)

이제 더 무서운 패턴으로 가보자. effect가 state를 갱신하고, 그 state가 다른 effect를 깨우고, 그 effect가 또 다른 state를 갱신하는 — **사슬처럼 이어진 effect 체인**이다.

```tsx
// 안티패턴: 4단계 effect 사슬
function ProductView({ productId }: { productId: string }) {
  const [product, setProduct] = useState<Product | null>(null);
  const [price, setPrice] = useState(0);
  const [tax, setTax] = useState(0);
  const [total, setTotal] = useState(0);

  // 1단계: productId로 product 가져오기
  useEffect(() => {
    fetchProduct(productId).then(setProduct);
  }, [productId]);

  // 2단계: product가 바뀌면 price 갱신
  useEffect(() => {
    if (product) setPrice(product.basePrice);
  }, [product]);

  // 3단계: price가 바뀌면 tax 갱신
  useEffect(() => {
    setTax(price * 0.1);
  }, [price]);

  // 4단계: price나 tax가 바뀌면 total 갱신
  useEffect(() => {
    setTotal(price + tax);
  }, [price, tax]);

  return <PriceTag total={total} />;
}
```

코드를 처음 보는 사람은 이게 왜 안 좋은지 단번에 알아채기 어렵다. 각 effect가 한 가지 일만 하니까, 책임이 잘 분리된 것처럼 보이기까지 한다. 그렇지만 실제로 일어나는 일을 추적해보면 난감하다.

`productId`가 바뀐다. → 1단계 effect가 돈다 → fetch가 끝나고 `setProduct` → 렌더 → 2단계 effect가 돈다 → `setPrice` → 렌더 → 3단계 effect가 돈다 → `setTax` → 렌더 → 4단계 effect가 돈다 → `setTotal` → 렌더. 한 번의 trigger에 렌더가 다섯 번 일어난다. 그 사이사이의 화면은 모두 **반쯤 갱신된 상태**다. price는 새 값인데 tax와 total은 여전히 옛 값인 프레임이 잠깐 보이는 거다.

게다가 사슬이 길어질수록 **무한 루프의 위험**이 기하급수적으로 커진다. 어느 단계에서 객체나 배열을 새로 만들어 set하면, 그 객체의 참조가 매번 달라져서 다음 단계 effect가 끝없이 다시 깨어난다. 한국 커뮤니티에서 자주 보이는 "useEffect가 무한 루프 도는데요" 질문의 70%는 이 사슬형 구조에서 비롯된다.

이런 사슬을 어떻게 펴야 할까? 핵심은 단순하다. **종속변수들끼리는 사슬을 만들지 말고, 한 곳에서 한꺼번에 계산하자.** 위 예시에서 `price`, `tax`, `total`은 전부 `product`의 종속변수다. 따로따로 effect로 동기화할 게 아니라, 그냥 함수로 한 줄에 끝낼 일이다.

```tsx
// 바른 패턴: 종속변수는 함께, 사슬은 평탄화
function ProductView({ productId }: { productId: string }) {
  // 진짜 effect 하나만 남는다 — 외부(서버)와의 동기화.
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchProduct(productId).then((p) => {
      if (!cancelled) setProduct(p);
    });
    return () => {
      cancelled = true;
    };
  }, [productId]);

  if (!product) return <Skeleton />;

  // 나머지는 전부 렌더 중 계산.
  const price = product.basePrice;
  const tax = price * 0.1;
  const total = price + tax;

  return <PriceTag total={total} />;
}
```

state가 네 개에서 한 개로 줄었다. effect가 네 개에서 한 개로 줄었다. 그 한 개도 진짜 effect다 — 외부 세계(서버)와의 동기화. 렌더 횟수도 정확히 두 번으로 줄었다 (productId 변경 시 한 번, fetch 응답 시 한 번). 그리고 `price`, `tax`, `total`은 같은 렌더 안에서 일관된 값으로 계산된다 — 한 프레임도 어긋날 수 없다.

이 사슬 평탄화 작업은 보고만 있으면 별 거 아닌 것 같지만, 실제로 손에 들고 해보면 **전체 컴포넌트의 사고 모델이 통째로 정리되는 경험**이 된다. effect의 사슬 안에 숨어 있던 진짜 의존 관계가 드러나기 때문이다. 잊지 말자. effect가 effect를 부르는 구조가 보이면, 거의 항상 그건 effect로 풀 일이 아니다.

## 묶음 B — 이벤트 핸들러로 풀 수 있는 문제

여기까지가 "렌더 중에 풀 수 있는 문제"였다. 이번에는 다른 묶음으로 넘어가자. 렌더의 결과로 풀 게 아니라, **사용자의 행동에 반응해서 풀 일**이다. 이쪽 안티패턴들은 패턴이 좀 다르다. 흐름은 늘 비슷하다. 사용자가 뭘 했다 → state가 바뀌었다 → 그 state 변화에 반응해서 effect가 돌고 거기서 진짜 작업이 일어난다. 이 사이에 한 단계가 너무 많다는 게 핵심이다.

### 안티패턴 #4. 사용자 이벤트(구매, POST 등)를 effect로

쇼핑몰의 구매 버튼을 짠다고 해보자.

```tsx
// 안티패턴: 사용자 이벤트를 effect로 우회
function CheckoutButton({ cart }: { cart: Cart }) {
  const [isPurchasing, setIsPurchasing] = useState(false);

  // 🚨 사용자가 클릭해서 isPurchasing이 true가 되면 effect로 fetch
  useEffect(() => {
    if (isPurchasing) {
      fetch("/api/purchase", {
        method: "POST",
        body: JSON.stringify(cart),
      })
        .then(() => alert("구매 완료"))
        .finally(() => setIsPurchasing(false));
    }
  }, [isPurchasing]);

  return (
    <button onClick={() => setIsPurchasing(true)} disabled={isPurchasing}>
      구매
    </button>
  );
}
```

이 코드는 — 안타깝게도 — 실제로 꽤 자주 보인다. 작성자의 의도는 짐작이 간다. "fetch는 사이드 이펙트니까 effect로 빼야 한다"라는 막연한 규칙을 마음에 품은 채로 짠 코드다. 그렇지만 잠깐, 이 fetch는 도대체 **누구의 사이드 이펙트인가?**

사용자가 버튼을 누른 그 순간 — 그게 사이드 이펙트의 **원인**이다. 렌더의 결과로 일어나는 일이 아니다. 어떤 prop이나 state가 외부 세계와 동기화되어야 해서 일어나는 일도 아니다. **그 클릭 한 번에 한 번** 일어나야 하는 일이다. 그렇다면 그 fetch가 있어야 할 자리는 자명하다. 클릭 핸들러 안이다.

```tsx
// 바른 패턴: 핸들러 안에서 직접 실행
function CheckoutButton({ cart }: { cart: Cart }) {
  const [isPurchasing, setIsPurchasing] = useState(false);

  const handleClick = async () => {
    setIsPurchasing(true);
    try {
      await fetch("/api/purchase", {
        method: "POST",
        body: JSON.stringify(cart),
      });
      alert("구매 완료");
    } finally {
      setIsPurchasing(false);
    }
  };

  return (
    <button onClick={handleClick} disabled={isPurchasing}>
      구매
    </button>
  );
}
```

코드가 더 짧아졌고, 무엇보다 **버그가 한 무더기 사라졌다.** 안티패턴 쪽 코드를 다시 보자. 만약 어떤 이유로 `isPurchasing`이 다른 곳에서 다시 true가 되면? 다시 fetch가 나간다. 만약 컴포넌트가 마운트될 때 어떤 상황으로 `isPurchasing`이 true로 시작되면? 그 fetch가 의도와 다른 시점에 나간다. 사용자의 클릭과 fetch 사이에 state라는 매개를 끼워 넣었더니, **fetch가 클릭이 아닌 다른 원인으로도 나갈 수 있는 길**이 열려버린 거다.

여기에서 끌어낼 일반 원리 하나를 짚고 가자. **사용자의 행동으로 일어나는 일은 핸들러에 있어야 한다. effect에 두면 그 행동의 의도가 흐려진다.** 이건 fetch뿐 아니라 모든 종류의 외부 호출에 적용된다. 결제, 삭제, 분석 이벤트 발사, 토스트 알림, 페이지 이동 — 사용자 클릭에 의한 것이라면 클릭 핸들러에 두는 게 맞다.

물론 예외도 있다. 페이지가 로드되자마자 자동으로 데이터를 가져와야 하는 경우 같은 거다. 그건 사용자 행동이 아니라 컴포넌트의 lifecycle에 동기화되는 작업이니, effect의 자리다. 우리가 가려내려는 건 어디까지나 "사용자가 시킨 일을 굳이 effect로 우회하는" 패턴이다.

### 안티패턴 #7. 자식 → 부모 통신을 effect로

부모와 자식 사이에 데이터를 흘려보내야 할 때, 자식의 effect를 통해 알리는 패턴도 자주 보인다.

```tsx
// 안티패턴: 자식이 effect로 부모에 알리기
function ChildForm({ onChange }: { onChange: (value: string) => void }) {
  const [value, setValue] = useState("");

  // 🚨 value가 바뀔 때마다 effect로 부모에 알린다.
  useEffect(() => {
    onChange(value);
  }, [value, onChange]);

  return <input value={value} onChange={(e) => setValue(e.target.value)} />;
}

function Parent() {
  const [parentValue, setParentValue] = useState("");
  return (
    <>
      <ChildForm onChange={setParentValue} />
      <p>현재 값: {parentValue}</p>
    </>
  );
}
```

언뜻 합리적으로 보이지만, 실제로 일어나는 흐름을 따라가보자. 사용자가 input에 한 글자를 친다. → `setValue` → 자식 렌더 → effect 등록 → 자식 렌더 끝 → effect 실행 → `onChange(value)` 호출 → `setParentValue` → 부모 렌더 → 자식 다시 렌더. 한 번의 키 입력에 렌더가 세 번 일어난다.

게다가 더 큰 문제는, **이 코드는 자식의 state와 부모의 state라는 두 개의 진실을 만든다는 거다.** 자식은 자기 안에 `value`를 따로 들고 있고, 부모는 자기대로 `parentValue`를 들고 있다. 두 개가 같은 값이라는 보장은 effect를 신뢰할 때만 성립한다. 만약 부모가 다른 경로로 `parentValue`를 바꾸면 둘은 어긋난다. 진실의 출처가 두 군데로 갈라져 있다는 건 늘 찜찜한 상태다.

처방은 두 가지 중 하나다. 첫째, **이벤트가 일어난 그 자리에서 같이 부모에 알리자.**

```tsx
// 바른 패턴 1: 같은 이벤트에서 부모도 함께 갱신
function ChildForm({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  // 자식은 value를 안 갖는다. 부모가 진실의 출처다.
  return <input value={value} onChange={(e) => onChange(e.target.value)} />;
}

function Parent() {
  const [parentValue, setParentValue] = useState("");
  return (
    <>
      <ChildForm value={parentValue} onChange={setParentValue} />
      <p>현재 값: {parentValue}</p>
    </>
  );
}
```

state를 끌어올렸다 (lifting state up). 자식은 더 이상 자기 state를 갖지 않고, 그저 부모가 준 `value`를 보여주고 입력이 들어오면 부모에게 알리기만 한다. 진실의 출처는 부모 한 군데로 모인다.

둘째, 자식이 자체 state를 가져야 할 이유가 분명하면 — 예를 들어 자식의 내부 검증 로직이 있어서 — **handleChange 안에서 자식 state와 부모 callback을 같이 호출**하자.

```tsx
// 바른 패턴 2: 자식 state도 두면서, 같은 이벤트에서 부모도 함께
function ChildForm({ onChange }: { onChange: (v: string) => void }) {
  const [value, setValue] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value;
    setValue(next);
    onChange(next); // 같은 이벤트에서 부모에게도 알린다.
  };

  return <input value={value} onChange={handleChange} />;
}
```

핵심은 같다. **"부모에 알려야 하는 사건"이 일어나는 그 자리에서 알리자.** 굳이 state를 한 번 갈아끼우고 effect로 우회해서 알릴 이유가 없다.

이 패턴은 자식 → 부모뿐 아니라 형제 컴포넌트끼리, 혹은 컴포넌트 → 외부 store끼리에도 그대로 적용된다. 이벤트를 받은 그 자리에서 관련된 모든 곳에 알리자. effect는 "내가 받은 prop이 외부 세계와 동기화되어야 해서" 도는 거지, "내 state 변화를 다른 곳에 광고하기 위해서" 도는 게 아니다.

### 안티패턴 #6. 앱 초기화를 effect로

앱이 시작될 때 한 번만 해야 할 일들이 있다. 분석 라이브러리 초기화, 어떤 전역 설정 로딩, 외부 SDK 부착 같은 거다. 이걸 어디에 두어야 할까?

```tsx
// 안티패턴: 마운트 시 한 번만 도는 effect로 초기화
function App() {
  useEffect(() => {
    // 🚨 마운트 시 한 번만 돈다... 정말?
    initAnalytics();
    loadGlobalConfig();
    attachExternalSDK();
  }, []);

  return <Routes />;
}
```

빈 의존성 배열을 보고는 "마운트 시 한 번"이라고 읽는 직관에 의지한 코드다. 그런데 React 18부터 — 특히 개발 모드의 Strict Mode에서 — effect는 **마운트 → 언마운트 → 마운트** 시퀀스로 두 번 도는 게 기본 동작이 됐다. 즉 `initAnalytics()`가 두 번 호출될 수 있다. 운이 나쁘면 중복 등록이 되고, 더 운이 나쁘면 한 번 정리됐다가 다시 부착되면서 기묘한 상태에 빠진다.

여기서 핵심 질문은 그거다. **이 일은 컴포넌트의 lifecycle에 묶여 있는가?** 분석 라이브러리 초기화는 컴포넌트와 무관하다. 앱 전체에 단 한 번만 일어나면 된다. 그렇다면 React tree 안에 있을 일이 아니다.

```tsx
// 바른 패턴 1: 모듈 최상단에서 한 번만
// app/init.ts
initAnalytics();
loadGlobalConfig();
attachExternalSDK();

// app/main.tsx
import "./init"; // import 시점에 한 번만 실행된다.

function App() {
  return <Routes />;
}
```

JS 모듈은 정의상 한 번만 평가된다. 모듈 최상단에 적은 코드는 React 렌더와 무관하게 정확히 한 번 실행된다. 컴포넌트와 무관한 초기화 작업이라면 이 자리가 가장 정직한 자리다.

만약 모듈 최상단이 부담스럽다면 — 예를 들어 SSR에서 서버에서도 평가될까 봐 걱정된다면 — `didInit` 가드를 두는 방식도 있다.

```tsx
// 바른 패턴 2: didInit 가드로 한 번만 보장
let didInit = false;

function App() {
  if (!didInit) {
    didInit = true;
    initAnalytics();
    loadGlobalConfig();
    attachExternalSDK();
  }

  return <Routes />;
}
```

렌더 중에 한 번만 실행되도록 명시적으로 가드한다. effect의 두 번 실행에 휘둘리지 않고, 사람이 봐도 의도가 분명하다.

핵심을 다시 정리하자. 빈 배열의 useEffect는 "마운트 시 한 번"의 의미가 아니다. 그건 "지금 이 effect는 의존하는 reactive value가 없다"라는 의미다. 한 번만 실행되어야 하는 진짜 lifecycle 작업은 React 바깥에 둘 자리가 있다. **lifecycle 흉내를 내려고 effect를 쓰지 말자.** 11장에서 봤던 진단을 회수하자면, 'componentDidMount의 useEffect 번역'은 거의 항상 잘못된 번역이다.

## 회수 박스 — 안티패턴 #3. prop 변화 리셋

남은 한 가지를 짧게 회수하자. 자식 컴포넌트가 부모로부터 받은 prop이 바뀔 때, 자기 내부 state를 그 prop에 맞춰 리셋하려는 패턴이다.

```tsx
// 안티패턴: prop 미러링 + effect로 리셋
function ProfileEditor({ user }: { user: User }) {
  const [name, setName] = useState(user.name);

  // 🚨 다른 user가 들어오면 폼을 리셋하고 싶다.
  useEffect(() => {
    setName(user.name);
  }, [user]);

  return <input value={name} onChange={(e) => setName(e.target.value)} />;
}
```

이 패턴은 4장에서 본격적으로 처방했다. 짧게만 회수하면, 두 가지 답이 있다.

첫째, **`key` prop으로 컴포넌트 자체를 통째로 리셋하는 방법.** 이게 보통 가장 자연스럽다.

```tsx
// 바른 패턴 1: key로 컴포넌트를 갈아끼운다
function ParentScreen({ user }: { user: User }) {
  return <ProfileEditor key={user.id} user={user} />;
}

function ProfileEditor({ user }: { user: User }) {
  const [name, setName] = useState(user.name);
  return <input value={name} onChange={(e) => setName(e.target.value)} />;
}
```

`user.id`가 바뀌면 React가 `ProfileEditor`를 새 인스턴스로 다시 만들어준다. state도 자연스럽게 초기화된다. effect 한 줄 없이 리셋이 끝난다.

둘째, **렌더 중 setState 패턴.** 이건 좀 더 미묘한 도구다.

```tsx
// 바른 패턴 2: 렌더 중 prev 비교로 리셋
function ProfileEditor({ user }: { user: User }) {
  const [name, setName] = useState(user.name);
  const [prevUserId, setPrevUserId] = useState(user.id);

  if (user.id !== prevUserId) {
    setPrevUserId(user.id);
    setName(user.name);
  }

  return <input value={name} onChange={(e) => setName(e.target.value)} />;
}
```

렌더 중에 prop의 변화를 감지하고 그 자리에서 set을 호출한다. React는 이 패턴을 정식으로 인정한다 — 렌더 중 같은 컴포넌트의 setState는 안전하다고 본다. effect의 한 박자 늦은 동기화 대신, 즉시 같은 렌더 안에서 정합을 잡는다.

이 두 패턴 사이의 선택은 4장의 처방을 다시 보면 된다. 핵심은 단 하나, **prop으로 자식 state를 리셋하려고 effect를 쓰지 말자.** 더 좋은 도구가 두 개나 있다.

## 사고 함정 — componentDidMount 흉내내기

마지막으로 살짝 사고 함정 하나를 더 짚자. 11장에서 한 번 진단했지만 다시 회수할 가치가 있다.

오래 React를 쓴 사람이라면 — 클래스 컴포넌트 시절을 거쳤다면 — `componentDidMount`, `componentDidUpdate`, `componentWillUnmount`라는 lifecycle 함수의 모양에 익숙하다. 그래서 함수 컴포넌트로 옮겨오면서 이런 번역을 자연스럽게 하게 된다.

- `componentDidMount` → `useEffect(() => { ... }, [])`
- `componentDidUpdate` → `useEffect(() => { ... })`
- `componentWillUnmount` → `useEffect(() => { return () => { ... } }, [])`

이 번역은 **표면적으로는 맞지만, 사고 모델로는 틀렸다.** useEffect의 본질은 lifecycle에 hook을 거는 게 아니라, **prop과 state로부터 파생되는 외부 동기화**를 선언하는 것이다. 어떤 reactive value가 바뀌면 그에 맞춰 외부 세계의 상태도 바뀌어야 한다는 동기화 계약이다.

componentDidMount 흉내를 내려고 하면 자꾸 잘못된 effect들이 만들어진다. "마운트 시 한 번만 fetch"가 사실은 "내가 보고 있는 productId가 바뀌면 다시 fetch"여야 했고, "마운트 시 한 번만 초기화"가 사실은 React 바깥에 있을 일이었다. **lifecycle을 떠올리지 말고 동기화를 떠올리자.** 이 한 번의 사고 전환이, 이 챕터에서 본 안티패턴의 절반을 자동으로 막아준다.

## 결정 트리 — "이 effect를 지우면 무엇이 깨지는가?"

이쯤에서 자가 점검 도구를 한 번 더 정리해두자. 이 챕터에서 본 모든 안티패턴은 다음 한 줄짜리 결정 트리로 90% 걸러낼 수 있다.

```
이 effect를 지운다고 가정해보자. 무엇이 깨지는가?

├─ "다음 렌더에서 어차피 같은 값이 다시 계산될 텐데..." 
│  → #1, #2, #5. 렌더 중 계산 또는 useMemo로.
│
├─ "사용자 클릭/제출에서 일어나야 하는 일인데..."
│  → #4, #7. 핸들러로 옮긴다.
│
├─ "마운트 시 한 번만 하고 싶은데..."
│  → #6. 모듈 최상단 또는 didInit 가드.
│
├─ "prop이 바뀌면 자식 state를 리셋하고 싶은데..."
│  → #3. key prop 또는 렌더 중 setState (4장 회수).
│
└─ "외부 세계(서버, DOM, 구독, 타이머)와의 진짜 동기화가 끊긴다."
   → 이건 effect다. 다음 장에서 의존성 배열을 정직하게 쓰는 법을 본다.
```

이 트리를 머릿속에 넣어두면, 코드 리뷰에서든 본인 코드에서든 effect를 보면 자동으로 가지를 따라가게 된다. 마지막 가지에 도달하지 않은 effect는 거의 다 안티패턴이다.

## 빠른 진단 — 한국 커뮤니티의 무한 루프 패턴 셋

마지막으로 한국 커뮤니티(OKKY, velog 댓글, 카카오톡 단톡방)에서 자주 보이는 "useEffect 무한 루프" 신고 셋을 빠르게 진단해보자.

**패턴 1.** "객체를 의존성으로 넣었더니 무한 루프 도네요."

```tsx
useEffect(() => {
  fetchData(options);
}, [options]); // options는 매번 새 객체.
```

진단: `options`가 부모에서 매 렌더마다 새로 만들어진다. 참조가 매번 바뀌니 effect가 매 렌더마다 돈다. → 부모에서 useMemo로 안정화하거나, options의 primitive 필드만 의존성에 넣거나, 더 좋게는 이게 정말 effect로 풀 일인지 묶음 A·B로 다시 진단하자. 자세한 처방은 13장.

**패턴 2.** "effect 안에서 set을 하니까 또 effect가 돌고 또 set 하고..."

```tsx
useEffect(() => {
  setItems([...items, newItem]); // 🚨
}, [items]);
```

진단: 이건 거의 100% 안티패턴 #5(cascading) 또는 #1(파생값)이다. → effect 자체가 잘못된 도구다. 핸들러나 렌더 중 계산으로 옮긴다.

**패턴 3.** "함수를 의존성으로 넣었더니 무한이네요."

```tsx
useEffect(() => {
  doSomething(callback);
}, [callback]); // callback은 매번 새 함수.
```

진단: 패턴 1과 같은 종류다. callback이 매 렌더마다 새 함수면 effect도 매 렌더마다 돈다. → useCallback, 또는 ref로 안정화. 그 전에 이게 정말 effect의 자리인지 한 번 더 묻자. 13장에서 본격 처방.

이 세 가지 패턴은 표면 증상은 다르지만 **뿌리는 같다.** 의존성 배열에 거짓말을 했거나, 처음부터 effect로 풀 일이 아니었거나, 둘 중 하나다.

## 핵심 정리

이 챕터의 요지를 한 줄씩 모아두자. 코드를 짤 때 머릿속에서 자동으로 떠오르게 만드는 게 목표다.

1. 메타 내부 표본의 약 46%가 불필요한 useEffect였다. 우리도 절반은 그럴 가능성이 높다.
2. effect를 보면 늘 묻자. "이걸 지우면 뭐가 깨지지?" 답이 분명하지 않으면 그 effect는 없어도 된다.
3. **종속변수는 변수로, 독립변수만 state로.** 다른 값에서 계산되는 값을 별도 state로 두지 말자.
4. 비싼 계산이라도 effect보다 useMemo의 자리다. 그것도 측정 후에.
5. effect가 effect를 부르는 사슬이 보이면, 거의 항상 그건 effect로 풀 일이 아니다 — 한 곳에서 한꺼번에 계산하자.
6. 사용자 행동으로 일어나는 일은 핸들러에 둔다. effect로 우회하지 말자.
7. 자식이 부모에 알릴 일은 같은 이벤트에서 함께 알리거나, state를 끌어올린다. effect로 광고하지 말자.
8. 컴포넌트와 무관한 초기화는 React 바깥(모듈 최상단, didInit 가드)에 둔다.
9. prop으로 자식 state를 리셋하려면 key prop을, 또는 렌더 중 setState를. effect는 마지막 선택지조차 아니다 (4장 회수).
10. componentDidMount 흉내를 내려고 effect를 쓰지 말자. lifecycle이 아니라 동기화를 생각하자.
11. 무한 루프의 뿌리는 둘 중 하나다 — 의존성 배열에 거짓말, 또는 애초에 effect의 자리가 아니었던 것.
12. effect는 "외부 세계와의 동기화"라는 단 하나의 자리에만 두자. 그 자리에 도달하지 않은 effect는 모두 안티패턴이다.

## 연습 문제

지금까지의 내용을 손에 익히려면 직접 손으로 고쳐봐야 한다. 네 가지 연습을 준비했다.

**[기초] 1. 파생 state effect 제거하기**

다음 코드를 effect와 state를 줄여 다시 쓰자.

```tsx
function OrderSummary({ items }: { items: Item[] }) {
  const [subtotal, setSubtotal] = useState(0);
  const [tax, setTax] = useState(0);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const s = items.reduce((acc, i) => acc + i.price, 0);
    setSubtotal(s);
  }, [items]);

  useEffect(() => {
    setTax(subtotal * 0.1);
  }, [subtotal]);

  useEffect(() => {
    setTotal(subtotal + tax);
  }, [subtotal, tax]);

  return <div>총 {total}원</div>;
}
```

힌트: 이 셋은 전부 `items`의 종속변수다. state도 effect도 한 줄도 필요 없다.

**[기초] 2. 클릭 → state → effect → fetch 사슬을 핸들러 한 줄로**

```tsx
function DeleteButton({ id }: { id: string }) {
  const [shouldDelete, setShouldDelete] = useState(false);

  useEffect(() => {
    if (shouldDelete) {
      fetch(`/api/items/${id}`, { method: "DELETE" }).then(() =>
        setShouldDelete(false),
      );
    }
  }, [shouldDelete, id]);

  return <button onClick={() => setShouldDelete(true)}>삭제</button>;
}
```

힌트: shouldDelete state가 정말 필요한가? 클릭 핸들러에서 직접 fetch를 호출하면 어떻게 될까?

**[중급] 3. prop 미러링을 key 리셋으로 전환**

```tsx
function ProductDetail({ product }: { product: Product }) {
  const [editName, setEditName] = useState(product.name);
  const [editPrice, setEditPrice] = useState(product.price);

  useEffect(() => {
    setEditName(product.name);
    setEditPrice(product.price);
  }, [product]);

  return (
    <form>
      <input value={editName} onChange={(e) => setEditName(e.target.value)} />
      <input
        value={editPrice}
        onChange={(e) => setEditPrice(Number(e.target.value))}
      />
    </form>
  );
}
```

힌트: 이 컴포넌트의 부모에서 `<ProductDetail key={product.id} ... />`로 바꾸면 어떻게 될까? 그렇게 하면 안쪽 effect는 필요 없어진다.

**[도전] 4. 4단계 effect 사슬을 reducer + 핸들러로 평탄화**

```tsx
function ShoppingCart() {
  const [items, setItems] = useState<Item[]>([]);
  const [count, setCount] = useState(0);
  const [subtotal, setSubtotal] = useState(0);
  const [discount, setDiscount] = useState(0);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    setCount(items.length);
  }, [items]);

  useEffect(() => {
    setSubtotal(items.reduce((s, i) => s + i.price * i.qty, 0));
  }, [items]);

  useEffect(() => {
    setDiscount(subtotal > 100000 ? subtotal * 0.05 : 0);
  }, [subtotal]);

  useEffect(() => {
    setTotal(subtotal - discount);
  }, [subtotal, discount]);

  // ... 추가/삭제 핸들러
}
```

힌트: state는 `items` 하나면 충분하다. `count`, `subtotal`, `discount`, `total`은 전부 렌더 중 계산. 그리고 추가/삭제 같은 사용자 행동은 핸들러에서 `items`만 갱신하면 된다. reducer를 도입하면 더 깔끔해진다.

이 네 문제를 직접 풀어보면, **effect 코드가 줄어들수록 코드가 더 정확해지는 경험**을 한 번씩 하게 될 거다. 이 감각이 일단 몸에 붙으면 그 다음부터는 자동이다.

## 마무리 — 13장으로의 다리

이 챕터에서 우리는 effect의 절반을 지웠다. 좀 더 정확히는, "지워도 되는 effect"를 가려내는 눈을 길렀다. 묶음 A의 패턴들은 렌더 중 계산과 useMemo로, 묶음 B의 패턴들은 이벤트 핸들러로, 회수 박스의 패턴은 key 리셋으로 옮겼다. 그러고 나서 남은 effect들은 — 이제 정말 — **외부 세계와의 동기화**라는 한 가지 자리에만 머물게 됐다.

그렇다면 이제 그 살아남은 effect들에 대해, 다음 단계의 질문을 해야 한다. 그 effect의 의존성 배열은 정직한가? 거기에 들어가야 할 reactive value가 빠져 있지는 않은가? 빠져 있다면 그건 어떤 종류의 거짓말인가? 빠져 있어도 괜찮은 것처럼 보이는 그 한 줄이, 사실은 어떤 동기화 계약을 깨고 있는가?

13장에서는 그 질문을 본격적으로 다룬다. linter의 exhaustive-deps에 짜증이 났던 그 모든 순간들 — 거기엔 사실 어떤 진실이 숨어 있는지 살펴보자. 의존성 배열은 hack이 아니라 동기화 계약이다. 그 계약을 정직하게 쓰는 법을 익히면, 11장과 12장에서 쌓은 사고 모델이 비로소 단단한 코드로 굳어진다.

남은 effect만이라도 제대로 쓰자. 그게 이 책 2부의 마지막 약속이다.
