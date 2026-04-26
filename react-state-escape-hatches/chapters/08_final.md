# 8장. 도구 선택 — Context, Zustand, Redux, Jotai, 그리고 Server State

신규 프로젝트가 시작된 첫 주 회의실 풍경을 한번 떠올려보자. 화이트보드 앞에 네 명이 앉아 있다. 한 사람이 자신만만하게 말한다. "이번엔 처음부터 Redux 깔고 갑시다. 나중에 커지면 어차피 그쪽으로 가야 하잖아요." 옆에 있던 누군가가 손을 든다. "Redux는 너무 무거워요. 요즘은 Zustand가 가볍다는 평이 많던데요. 1.2KB짜리예요." 그러자 또 다른 사람이 끼어든다. "그러지 말고, 그냥 Context API로 충분하지 않아요? React 안에 이미 들어 있는데 왜 굳이 외부 라이브러리를 또 깝니까." 마지막 한 명이 가만히 듣다가 조용히 묻는다. "그런데, 우리가 다루려는 게 정확히 어떤 데이터죠?"

회의는 결국 한 시간을 넘기고 결론 없이 끝난다. 누군가는 "일단 Redux Toolkit으로 가시죠"라고 정리하고, 누군가는 "저는 Zustand가 익숙해서…"라며 미적거리고, 누군가는 "Context로 시작하고 나중에 바꾸죠"라고 말한다. 흔히 보는 풍경이다. 그리고 솔직히 말하면, 이런 회의에서 어떤 결정이 내려지든 그 결정은 대개 1~2년 뒤에 후회로 돌아온다. 왜 그럴까?

이 회의에서 빠진 질문이 하나 있기 때문이다. **"우리가 다루려는 게 정확히 어떤 데이터인가?"** 그리고 그 질문에 답하기 전까지는, 어떤 라이브러리를 고르든 절반쯤은 틀린 도구를 고르고 있는 셈이다.

이 장에서 함께 풀어볼 문제가 바로 이거다. "Redux냐 Zustand냐 Jotai냐"라는, 제목만 그럴듯하고 답은 늘 안개 속인 그 질문 말고, 그 앞에 놓여 있는 더 본질적인 질문 — "내가 지금 다루는 데이터가 어떤 종류인가, 그리고 그 종류에 어울리는 도구는 무엇인가" — 를 먼저 세워보자. 그 질문을 세우고 나면, 사실 도구 선택은 의외로 명료해진다.

한 가지 더 짚고 시작하자. 이 장은 라이브러리 사용법 책이 아니다. Zustand의 미들웨어 옵션이나 Redux Toolkit의 createEntityAdapter를 어떻게 쓰는지 같은 건 각 라이브러리의 공식 문서가 훨씬 잘 설명한다. 우리가 여기서 다룰 건 그보다 한 층 위에 있다 — **어떤 신호가 보였을 때 어떤 도구로 손이 가야 하는가**, **그 도구의 사상이 우리 문제와 어떻게 맞물리는가**. 이 결정만 정확히 내릴 수 있으면, 사용법은 며칠이면 익는다. 반대로 이 결정이 흐릿하면, 사용법을 아무리 잘 알아도 잘못된 자리에 잘 익은 도구를 끼워 넣고 있게 된다.

또 하나, 이 장은 **2026년 현재의 풍경**을 기준으로 한다. 도구 생태계는 빠르게 변한다. 5년 뒤에는 RSC와 server actions가 클라이언트 상태 관리의 자리를 일부 더 가져갈 수도 있고, 새로운 도구가 떠올랐다 사라질 수도 있다. 그래도 이 장에서 익혀둔 **"신호에서 도구로"**라는 사고 흐름은 도구의 이름이 바뀌어도 그대로 쓸 수 있다. 도구는 갈아치우되, 그 도구를 고르는 안목은 시간이 흘러도 자산으로 남는다.

## "상태 관리 라이브러리"라는 단어가 가린 두 가지

먼저 한 가지 사실부터 분명히 짚고 넘어가자. 우리가 흔히 "상태 관리 라이브러리"라고 부르는 단어 안에는, 사실은 전혀 성격이 다른 두 종류의 데이터가 뒤섞여 있다.

상상해보자. 우리가 만들고 있는 앱에는 이런 데이터들이 흘러다닌다.

- 모달이 열려 있는지, 닫혀 있는지
- 사이드바가 펼쳐졌는지, 접혔는지
- 어떤 탭이 활성화되어 있는지
- 폼에 사용자가 지금 입력하고 있는 텍스트
- 다크 모드인지 라이트 모드인지

이런 데이터의 공통점은 무엇일까? 모두 **사용자가 지금 이 브라우저에서, 이 화면을 어떻게 보고 있느냐**에 관한 정보다. 서버는 모르고, 알 필요도 없다. 페이지를 새로고침하면 사라져도 큰일 나지 않는다. 한 명의 사용자가, 자기 화면 안에서, 자기 의도대로 만들어내는 일시적인 형상이다. 이런 걸 흔히 **클라이언트 상태(Client State)** 혹은 **UI 상태(UI State)** 라고 부른다.

이번에는 다른 종류의 데이터를 보자.

- 게시판의 글 목록
- 사용자 프로필 정보
- 장바구니에 담긴 상품 목록
- 어제 결제한 주문 내역
- 친구가 방금 올린 댓글

이 데이터들의 공통점은 또 무엇일까? 서버 어딘가의 데이터베이스에 진짜 정본이 있고, 우리 앱이 보고 있는 건 그저 그것의 **사본** 일 뿐이라는 점이다. 우리가 보고 있는 동안에도 다른 사용자가 그 글에 댓글을 달 수 있고, 누군가가 상품을 품절시킬 수도 있다. 새로고침해도 사라지면 안 되고 — 사라져 보일 뿐이지 — 잠시 후에 다시 받아와야 한다. 이런 데이터를 **서버 상태(Server State)**라고 부른다.

이 둘은 이름만 다른 게 아니라 **본질이 다른 문제**다. 한번 표로 가지런히 비교해보자.

| 성질 | UI 상태 | 서버 상태 |
|---|---|---|
| 정본의 위치 | 클라이언트(이 브라우저) | 서버 |
| 변경의 주체 | 오직 이 사용자 | 다른 사용자/시스템도 변경 가능 |
| 시간 의존성 | 즉시 반영 | 비동기, 네트워크 지연 |
| 캐시 무효화 | 거의 필요 없음 | 본질적 문제 |
| 새로고침 후 | 보존 안 해도 됨 | 다시 받아와야 함 |
| 낙관적 업데이트 | 의미 없음 | 자주 필요 |
| 재시도/에러 처리 | 거의 없음 | 일상 |

표를 보면 어렴풋이 느껴지지 않는가? 이 둘을 같은 도구로 다루겠다는 발상은, 마치 "망치 하나로 못도 박고 나사도 박자"라는 말과 비슷하다. 가능은 하다. 다만 결과가 끔찍할 뿐이다.

그런데도 우리는 오랫동안 이 둘을 같은 통에 넣고 흔들어왔다. Redux store 안에 `ui` slice와 `posts` slice가 나란히 앉아 있고, Context 안에 사용자가 토글한 다크모드 상태와 서버에서 받아온 사용자 프로필이 같은 객체 안에 들어 있다. 그렇게 시작한 코드가 1년쯤 자라면 어떻게 되는지, 우리는 다 안다. 캐시 무효화 로직을 직접 구현하고, race condition을 막느라 플래그를 여기저기 두고, 낙관적 업데이트는 엄두도 못 내고, 어떤 데이터가 stale인지 아무도 자신 있게 말하지 못하는 상태가 된다. 난감하다.

그러니 도구 이야기를 시작하기 전에, 먼저 이 한 줄을 새겨두자. **"상태 관리 라이브러리"라는 표현은 절반의 진실만 담고 있다. UI 상태와 서버 상태는 다른 문제이고, 다른 도구로 풀어야 한다.**

## 서버 상태는 다르다 — Kent C. Dodds의 단언

Kent C. Dodds가 자주 인용되는 문장이 두 개 있다. 둘은 따로 떨어뜨리면 모순처럼 들리는데, 같이 놓고 읽으면 비로소 의미가 살아난다.

> "React IS your state management library."
>
> "But server cache state is different. Don't try to manage it with the same tools."

앞 문장만 들으면 "외부 라이브러리는 필요 없다"는 뜻으로 읽힌다. 실제로 그가 자주 강조하는 입장이다 — Redux가 폭발적으로 인기를 얻은 진짜 이유는 reducer 패턴의 우아함이라기보다는, 단순히 prop drilling을 끊을 방법이 마땅치 않았기 때문이라는 것. 지금은 Context와 useReducer만으로도 그 자리를 거의 다 메울 수 있다. 그러니 작은 앱, 중간 규모 앱에서는 React가 이미 가진 도구로 충분하다. 외부 라이브러리에 너무 빨리 손대지 말자.

여기까지는 익숙하다. 그런데 두 번째 문장이 사실은 더 중요하다. "**그러나 서버 캐시 상태는 다르다.**" 이 말은 무슨 뜻일까?

서버에서 받아온 데이터를 우리가 들고 있을 때, 그건 **상태가 아니라 캐시** 라는 시각이다. 그 데이터의 정본은 서버에 있고, 우리는 그 사본을 잠깐 빌려와 화면에 비추고 있을 뿐이다. 그렇다면 이 데이터를 잘 다룬다는 건 다음과 같은 질문에 답한다는 뜻이다.

- 이 사본은 언제부터 stale한가? (얼마 지나면 다시 받아와야 하나?)
- 사용자가 다른 탭에서 돌아왔을 때 자동으로 갱신해야 하나?
- 같은 데이터를 여러 컴포넌트가 동시에 요청하면 한 번만 fetch해야 하지 않나?
- 페치가 실패하면 몇 번 재시도하나, 백오프는 어떻게 거나?
- 사용자가 "좋아요"를 누르면 일단 화면은 좋아요 상태로 바꿔놓고 서버 응답을 기다려야 하나? 실패하면 어떻게 롤백하나?
- 새 데이터를 POST한 다음, 관련된 쿼리들은 어떻게 invalidate하나?

이 질문들은 useState/useReducer/Context의 영역이 아니다. 이건 **캐시 시스템**의 영역이다. 그리고 캐시 시스템을 직접 구현해본 사람은 안다 — "아, 이거 내가 만들면 안 되는 거구나"라는 깨달음이 오는 데까지 보통 한 번의 거대한 실패가 필요하다는 사실을.

옛날에 우리가 어떻게 이걸 다뤘는지 잠깐 떠올려보자. 흔한 패턴은 이런 모양이었다.

```tsx
function PostList() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    fetch("/api/posts")
      .then((r) => r.json())
      .then((data) => {
        if (!ignore) {
          setPosts(data);
          setLoading(false);
        }
      })
      .catch((e) => {
        if (!ignore) {
          setError(e);
          setLoading(false);
        }
      });
    return () => {
      ignore = true;
    };
  }, []);

  if (loading) return <Spinner />;
  if (error) return <ErrorView error={error} />;
  return <List posts={posts} />;
}
```

이 코드, 어디 한 군데 틀렸다고 콕 집기는 어렵다. race condition을 막느라 `ignore` 플래그도 챙겼고, 로딩과 에러도 분기했다. 그런데 가만히 보자. 다음 질문들에 대해 이 코드는 무엇 하나 답하지 못한다.

- 같은 페이지의 다른 컴포넌트도 `/api/posts`를 본다면? 두 번 fetch한다.
- 사용자가 다른 탭 갔다가 돌아오면? 갱신 안 된다.
- 30초 동안 같은 페이지를 들락날락하면? 매번 다시 받는다.
- 새 글을 POST한 뒤 이 목록을 갱신하려면? 부모에 콜백 두고 setPosts 다시 부르거나 페이지를 새로고침해야 한다.
- 네트워크 끊겼다가 다시 연결되면? 사용자가 직접 새로고침해야 한다.

이걸 useState와 useEffect로 다 짜겠다는 건, 결국 **캐시 라이브러리를 손으로 다시 발명하겠다**는 선언과 같다. 그리고 그렇게 손으로 만든 캐시는 거의 항상 어딘가가 깨져 있다. 미안하지만, 우리가 그걸 잘 만들 만큼 한가하지 않다.

여기서 TanStack Query(예전 이름 react-query)나 SWR 같은 도구가 등장하는 이유가 분명해진다. 이 도구들의 사상은 단순하다. **"서버를 진실의 소유자로 두고, 클라이언트는 그 캐시를 동기화한다."** 컴포넌트는 "나는 이 키에 해당하는 데이터를 보고 싶다"라고 선언만 하고, 실제 fetch·cache·invalidation·retry·revalidation은 라이브러리가 처리한다.

같은 위 코드를 TanStack Query로 다시 써보자.

```tsx
import { useQuery } from "@tanstack/react-query";

function PostList() {
  const { data: posts, isPending, error } = useQuery({
    queryKey: ["posts"],
    queryFn: async () => {
      const r = await fetch("/api/posts");
      if (!r.ok) throw new Error("Failed to fetch posts");
      return r.json() as Promise<Post[]>;
    },
  });

  if (isPending) return <Spinner />;
  if (error) return <ErrorView error={error} />;
  return <List posts={posts} />;
}
```

겉보기에는 단순히 짧아진 것 같지만, 실제로는 그 짧아진 코드가 다음을 모두 공짜로 해준다.

- 같은 `queryKey`를 보는 다른 컴포넌트와 캐시를 공유한다 (중복 fetch 사라짐)
- `staleTime`/`gcTime` 설정에 따라 자동으로 재요청한다
- 윈도우 포커스가 돌아오면 background refetch를 한다
- 네트워크 회복 시 자동 재시도한다
- 실패 시 지수 백오프로 재시도한다
- 새 글 추가 후 `queryClient.invalidateQueries({ queryKey: ['posts'] })` 한 줄로 갱신한다

거의 8줄 vs 30줄의 코드 차이가 아니다. **풀고 있는 문제의 차원이 다르다.** 앞 코드는 "한 컴포넌트가 한 번 데이터를 가져온다"라는 좁은 문제를 풀었고, 뒤 코드는 "이 앱 전체에서 이 데이터의 캐시를 일관되게 관리한다"라는 넓은 문제를 푼다.

그러니 서버 데이터를 다룰 때는 잊지 말자. **이건 UI 상태가 아니라 캐시다. 그리고 캐시는 캐시 도구로 다뤄야 한다.**

## TanStack Query vs SWR — 같은 사상, 다른 결

서버 캐시 도구로 흔히 비교되는 게 TanStack Query와 SWR이다. 둘은 사상이 거의 같다. **"서버를 정본, 클라이언트를 캐시"**라는 한 줄을 둘 다 공유한다. 그러면서도 결이 조금씩 다르다.

**SWR**은 Vercel이 만든 도구로, 이름이 곧 사상이다 — Stale-While-Revalidate. "stale인 데이터를 일단 보여주고, 백그라운드에서 갱신해 자연스럽게 교체한다"는 캐시 전략을 그대로 이름으로 삼았다. 번들이 가볍고(약 4KB대), API가 단출하다. 작은 앱, 단순한 fetch 패턴, "복잡한 캐시 전략은 필요 없고 그냥 잘 갱신만 되면 된다"는 자리에 좋다.

```tsx
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

function PostList() {
  const { data, error, isLoading } = useSWR<Post[]>("/api/posts", fetcher);
  if (isLoading) return <Spinner />;
  if (error) return <ErrorView error={error} />;
  return <List posts={data!} />;
}
```

**TanStack Query**(예전 react-query)는 더 큰 도구다. 번들도 더 무겁다(13KB대). 대신 그만큼 표현력이 넓다 — infinite query, optimistic update의 정교한 제어, 의존성 있는 쿼리, query invalidation의 정밀한 키 매칭, prefetch, suspense 모드, 별도 client 인스턴스로 멀티-탭/멀티-앱 분리, devtools가 표준 등. 복잡한 도메인, 큰 앱, 캐시 전략을 세밀하게 다뤄야 하는 자리에 어울린다.

휴리스틱은 단순하다. **작고 단순하면 SWR, 크고 복잡하면 TanStack Query.** Redux Toolkit을 이미 쓰고 있다면 RTK Query도 자연스러운 선택이다 — 이미 깔린 store 안에서 같은 우산 아래로 풀린다(RTK Query의 표현력은 두 도구의 중간쯤이라고 보면 비슷하다).

어느 쪽을 고르든, 핵심은 **"서버 상태를 클라이언트 상태와 같은 도구로 다루지 않는다"**는 사상 자체다. 도구는 그 사상을 구현하는 수단에 불과하다.

## TanStack Query의 사상 — 최소 예제로 한 컷

도구 자체의 사용법은 공식 문서가 훨씬 잘 설명하니, 여기서는 사상이 드러나는 가장 작은 한 장면만 보고 가자. 글 목록을 받아 화면에 보여주고, 새 글을 추가한 뒤 자동으로 목록이 갱신되도록 만들어볼 거다.

```tsx
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

type Post = { id: number; title: string };

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000 }, // 30초 동안은 fresh로 본다
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <PostList />
      <NewPostForm />
    </QueryClientProvider>
  );
}

function PostList() {
  const { data, isPending, error } = useQuery({
    queryKey: ["posts"],
    queryFn: async (): Promise<Post[]> => {
      const r = await fetch("/api/posts");
      if (!r.ok) throw new Error("fetch failed");
      return r.json();
    },
  });

  if (isPending) return <p>불러오는 중…</p>;
  if (error) return <p>에러: {error.message}</p>;
  return (
    <ul>
      {data.map((p) => (
        <li key={p.id}>{p.title}</li>
      ))}
    </ul>
  );
}

function NewPostForm() {
  const qc = useQueryClient();
  const mutation = useMutation({
    mutationFn: async (title: string) => {
      const r = await fetch("/api/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });
      if (!r.ok) throw new Error("save failed");
      return r.json() as Promise<Post>;
    },
    onSuccess: () => {
      // 정본이 바뀌었으니 캐시를 무효화 — 자동 refetch
      qc.invalidateQueries({ queryKey: ["posts"] });
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        const title = (e.currentTarget.elements.namedItem("title") as HTMLInputElement).value;
        mutation.mutate(title);
      }}
    >
      <input name="title" />
      <button type="submit" disabled={mutation.isPending}>
        등록
      </button>
    </form>
  );
}
```

이 코드의 핵심을 몇 가지로 짚어보자.

첫째, **컴포넌트는 "어떻게"가 아니라 "무엇을"만 말한다.** `useQuery`는 "나는 `posts`라는 키의 데이터를 보고 싶다"는 선언이고, "어떻게 가져오나, 캐시에 있으면 재사용할까, 언제 stale로 볼까"는 라이브러리가 정한다. Effect의 동기화 사상이 그대로 캐시 도구로 옮겨와 있다고 봐도 좋다.

둘째, **mutation은 정본을 바꾸고, 캐시는 invalidation으로 따라온다.** 새 글이 들어가면 우리는 직접 `setPosts([...posts, newPost])`를 부르지 않는다. 정본(서버)을 바꾸고 "이 키의 캐시는 이제 의심스러우니 다시 봐라"라고 신호를 보낸다. 클라이언트는 어디까지나 그 캐시의 사본일 뿐이다.

셋째, **queryKey가 의존성 배열의 역할을 한다.** Effect에서 의존성 배열이 동기화 계약이었던 것처럼, 여기서는 queryKey가 캐시 키이자 동기화 계약이다. 키가 같으면 같은 데이터, 키가 다르면 다른 데이터.

이 세 줄이 머리에 박히면, 사실 TanStack Query의 나머지 기능들(infinite query, optimistic update, prefetching, suspense 모드 등)은 모두 이 사상의 자연스러운 확장으로 읽힌다. 그러니 서버에서 데이터를 받아오는 자리에 useState + useEffect 패턴이 보인다면, 일단 한 번 멈춰서 이렇게 자문해보자. **"이 데이터, 정말 클라이언트 상태인가? 사실은 캐시 아닌가?"**

물론 모든 fetch를 무조건 TanStack Query로 옮기라는 말은 아니다. "이 화면 한 번 들어왔을 때 한 번만 받아오고 끝"인 정말 단발성 데이터라면 useEffect로 충분할 수 있다. 다만 그런 경우조차 보통은 라이브러리로 옮기는 편이 비용이 더 작다는 게 경험칙이다.

## UI 상태로 좁혀서 — Context+Reducer가 어디까지 가는가

서버 상태를 분리해놓고 나면, 이제 우리 손에 남는 건 진짜 UI 상태뿐이다. 모달 열림, 사이드바 토글, 위저드 단계, 다크모드, 로컬 폼 입력값 같은 것들. 이 자리에서야 비로소 "Redux냐 Zustand냐 Context냐"라는 질문이 의미를 가진다.

그리고 이 자리에서 다시 한번 Kent C. Dodds의 입장을 떠올려보면 결론이 의외로 단순하다. **대부분의 UI 상태는 useState + useReducer + Context로 충분하다.** 7장에서 우리가 익힌 reducer + 두 개의 분리된 Context 패턴 — `TasksContext`와 `TasksDispatchContext` — 가 사실 꽤 멀리 간다. 작은 앱은 거의 끝까지 이걸로 갈 수 있다. 솔직히 말해, 하루에도 수십 번씩 "Redux 깔까?" 하는 분위기 속에서 이 사실은 자주 잊힌다.

그렇다면 Context+Reducer는 어디서 멈추는가? 7장 끝에서 우리는 그 답을 살짝 보았다. **value가 자주 바뀌고, 그 value를 보는 컨슈머가 많아지면 Context는 모든 컨슈머를 깨운다.** 같은 Context를 구독하는 50개의 컴포넌트가 있을 때, 그중 한 컴포넌트만 쓰는 한 필드가 1초에 10번 바뀐다고 해보자. 50개가 1초에 10번씩 다시 렌더된다. 대부분은 결과가 같지만, React는 그걸 미리 알 수 없으니 일단 호출은 한다. 큰 트리에서는 이게 체감되는 비용이 된다.

이 한계를 코드로 한번 재현해보자. 7장 후반의 Tasks 앱을 살짝 비틀어, "마지막 수정 시각" 필드 하나를 추가했다고 해보자.

```tsx
// 7장 스타일: state 전체를 한 Context로 내려보낸다
type TasksState = {
  tasks: Task[];
  lastModifiedAt: number; // 어떤 변경이든 일어나면 이 값이 갱신된다
};

const TasksStateContext = createContext<TasksState | null>(null);

function TasksProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(tasksReducer, initialState);
  return (
    <TasksStateContext.Provider value={state}>
      <TasksDispatchContext.Provider value={dispatch}>
        {children}
      </TasksDispatchContext.Provider>
    </TasksStateContext.Provider>
  );
}

function TaskTitle({ id }: { id: number }) {
  // 이 컴포넌트는 단지 한 task의 title만 본다
  const { tasks } = useContext(TasksStateContext)!;
  const title = tasks.find((t) => t.id === id)?.title;
  return <span>{title}</span>;
}
```

이 구조에서 `lastModifiedAt`이 1초마다 갱신된다고 해보자. `tasks` 배열 자체는 안 바뀌었더라도, 우리가 `value={state}`로 내려보낸 객체 참조가 매번 새로워지므로 — 그리고 Context는 참조 동등성으로 변경을 판단하므로 — `TaskTitle`을 포함한 모든 컨슈머가 다시 렌더된다. `title`은 그대로인데도 말이다.

이게 바로 **selective subscription의 부재**가 만드는 비용이다. Context는 "구독" 도구라기보다는 "전달" 도구다. 받는 쪽이 "나는 이 객체 안에서 이 필드 하나만 보겠다"라고 약속할 길이 표준 API에는 없다(useContextSelector 같은 외부 제안이 있긴 하지만, 2026년 현재까지 표준은 아니다).

물론 우회법은 있다. Context를 잘게 쪼개는 것 — `TasksContext`, `LastModifiedAtContext`, `SelectedIdContext`처럼 자주 변하는 영역과 그렇지 않은 영역을 분리해 Provider를 따로 두는 패턴이다. 이게 실용적으로 꽤 멀리 간다. 다만 이걸 다섯 개, 열 개씩 만들고 있는 자기 자신을 발견할 때쯤엔, 이런 의심이 들기 시작한다. **"내가 지금 selective subscription을 손으로 발명하고 있는 건 아닐까?"**

그 의심이 들었다면, 그게 바로 외부 라이브러리로 넘어갈 신호다.

## selective subscription이 필요해지는 신호

신호를 정리하고 가자. 외부 상태 관리 라이브러리를 도입하기 직전, 우리가 보통 보게 되는 풍경은 이렇다.

- 자주 바뀌는 필드와 거의 안 바뀌는 필드가 한 Context 안에 섞여 있다
- 한 컴포넌트는 객체에서 한 필드만 보지만, 부모 객체가 바뀌면 무조건 다시 렌더된다
- 성능 핫스팟에서 React DevTools Profiler를 켜보면 "왜 이게 다시 렌더됐지?" 싶은 컴포넌트가 줄지어 있다
- Context를 쪼개고 또 쪼개는데, 이쯤 되면 차라리 store를 하나 두는 게 나아 보인다
- 파생 상태(`selectedTaskTitle = tasks.find(t => t.id === selectedId)?.title`) 같은 것이 여러 곳에서 중복 계산된다

이런 풍경이 한두 군데가 아니라 곳곳에서 보이기 시작했다면, 그제서야 라이브러리 선택의 회의를 열어도 늦지 않다. 그 전까지는 Context+Reducer가 답인 경우가 훨씬 많다는 사실을 잊지 말자.

다만 한 가지만 더. selective subscription이 필요한 풍경처럼 보였는데, 자세히 들여다보면 사실은 **서버 상태**였던 경우가 절반쯤 된다. "캐시를 잘 다루지 못해서 발생하는 리렌더"인지, "정말 UI 상태인데 selective subscription이 부족해서 생기는 리렌더"인지를 먼저 가려야 한다. 전자라면 라이브러리는 Zustand가 아니라 TanStack Query고, 후자라면 비로소 Zustand 같은 도구가 답이다.

## Zustand — 함수형 store와 hook 단위 selective subscription

Zustand의 사상은 한 줄로 요약된다. **"단일 store를 만들고, 컴포넌트는 그 store에서 자기가 관심 있는 조각만 selector로 꺼내 구독한다."** Redux의 단일 store 정신을 가져오되, 보일러플레이트(action type 상수, action creator, mapStateToProps 등)를 거의 다 걷어내고, 구독 단위를 hook으로 끌어내린 도구라고 보면 된다.

가장 작은 예제를 보자.

```tsx
import { create } from "zustand";

type CounterState = {
  count: number;
  increment: () => void;
  reset: () => void;
};

const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((s) => ({ count: s.count + 1 })),
  reset: () => set({ count: 0 }),
}));

function CountValue() {
  // 이 컴포넌트는 count만 본다 — count가 바뀔 때만 다시 렌더된다
  const count = useCounterStore((s) => s.count);
  return <span>{count}</span>;
}

function CountButtons() {
  // 이 컴포넌트는 액션만 본다 — 액션은 안 바뀌니 거의 다시 렌더되지 않는다
  const increment = useCounterStore((s) => s.increment);
  const reset = useCounterStore((s) => s.reset);
  return (
    <>
      <button onClick={increment}>+1</button>
      <button onClick={reset}>리셋</button>
    </>
  );
}
```

코드를 한번 음미해보자. `create`는 store를 만들어 hook으로 돌려준다. 컴포넌트는 그 hook에 selector를 넣어 자기가 관심 있는 슬라이스를 꺼낸다. selector가 반환하는 값이 같으면(얕은 비교) 다시 렌더되지 않는다. **이게 Context로는 표준 API로 못 했던 일이다.** Provider도 필요 없다 — store가 모듈 변수이니 어디서든 hook 호출만으로 접근한다.

여러 슬라이스를 한 번에 뽑아야 한다면 `useShallow`를 곁들이면 된다.

```tsx
import { useShallow } from "zustand/react/shallow";

const { count, increment } = useCounterStore(
  useShallow((s) => ({ count: s.count, increment: s.increment }))
);
```

복잡한 도메인은 어떻게 다루는지 한 컷만 더 보자. 7장의 Tasks 앱을 Zustand로 옮겨놓으면 대략 이런 모양이 된다.

```tsx
type Task = { id: number; title: string; done: boolean };

type TasksState = {
  tasks: Task[];
  lastModifiedAt: number;
  add: (title: string) => void;
  toggle: (id: number) => void;
  remove: (id: number) => void;
};

let nextId = 1;
const useTasksStore = create<TasksState>((set) => ({
  tasks: [],
  lastModifiedAt: Date.now(),
  add: (title) =>
    set((s) => ({
      tasks: [...s.tasks, { id: nextId++, title, done: false }],
      lastModifiedAt: Date.now(),
    })),
  toggle: (id) =>
    set((s) => ({
      tasks: s.tasks.map((t) => (t.id === id ? { ...t, done: !t.done } : t)),
      lastModifiedAt: Date.now(),
    })),
  remove: (id) =>
    set((s) => ({
      tasks: s.tasks.filter((t) => t.id !== id),
      lastModifiedAt: Date.now(),
    })),
}));

function TaskTitle({ id }: { id: number }) {
  // tasks 전체가 아니라 이 task의 title만 구독한다
  const title = useTasksStore((s) => s.tasks.find((t) => t.id === id)?.title);
  return <span>{title}</span>;
}
```

`lastModifiedAt`이 1초에 한 번 바뀌어도, `TaskTitle`은 자기가 본 selector 결과(즉 그 한 task의 title)가 바뀌었을 때만 다시 렌더된다. 이게 우리가 Context에서는 한참 우회로를 그려야 했던 일을 hook 한 줄로 풀어주는 이유다.

다만 거저 얻는 건 없다. Zustand에는 Zustand의 그늘이 있다.

- store가 모듈 변수이므로 SSR이나 테스트 환경에서 매 요청/매 테스트마다 새 store가 필요할 때 별도 패턴(`createStore` + Context)이 따라온다
- selector를 잘못 짜면 selective subscription의 이점이 사라진다 — 매번 새 객체를 만들어 반환하면 얕은 비교가 무용지물이다(그래서 `useShallow`가 필요하다)
- 시간여행 디버깅, action 단위 trace 같은 Redux DevTools식 워크플로는 별도 미들웨어로 붙여야 한다

이 그늘들이 다 무시할 만하다는 건 아니다. 하지만 작은-중간 규모 앱에서, 그리고 "selective subscription이 진짜 필요해진" 자리에서 Zustand는 보통 가장 비용 대비 효과가 좋은 선택지다.

## Jotai — bottom-up atom 모델이라는 다른 사상

Zustand가 "store를 하나 두고 그 안에서 슬라이스를 꺼낸다"는 top-down 발상이라면, Jotai는 정반대다. **"작은 원자 단위 상태(atom)를 여기저기 정의하고, 그 atom들 사이의 의존성으로 파생 상태를 만든다."** Recoil의 사상을 더 가볍게 다듬은 모델이라고 보면 비슷하다.

```tsx
import { atom, useAtom, useAtomValue } from "jotai";

const countAtom = atom(0);
const doubledAtom = atom((get) => get(countAtom) * 2);

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>;
}

function Doubled() {
  const doubled = useAtomValue(doubledAtom);
  return <span>{doubled}</span>;
}
```

여기서 핵심은 `doubledAtom`이다. 이건 값이 아니라 **계산식** 이다. `countAtom`이 바뀌면 자동으로 재계산되고, `doubledAtom`을 구독한 컴포넌트만 다시 렌더된다. atom은 자기 의존성 그래프를 알기 때문에, 어떤 atom이 바뀌면 그 atom에 의존하는 atom들과 그것들을 구독한 컴포넌트들만 깨운다.

이 모델은 다음과 같은 자리에서 빛난다.

- 폼처럼 **개별 필드 단위의 독립적 상태가 많은** 화면 — 각 필드를 atom으로 두고, "전체가 valid한가"를 파생 atom으로 둔다
- 그래프 에디터, 차트 빌더처럼 **셀/노드 단위로 상태가 잘게 쪼개지고 의존성이 그래프 형태인** 도메인
- 거대한 단일 store에 다 욱여넣으면 selector가 복잡해지지만, atom으로 쪼개면 자연스럽게 풀리는 경우

반대로 Jotai가 안 어울리는 자리도 있다. 하나의 큰 도메인 객체(예: 카트 전체)를 한 덩어리로 다루고 싶은 경우다. 그건 단일 store(Zustand나 Redux Toolkit)가 더 직관적이다.

Zustand와 Jotai는 경쟁자라기보다는 **사상이 다른 도구**다. 도메인의 모양을 보고 고르자. 큰 객체가 변하는 모양이면 Zustand가 자연스럽고, 잘게 쪼개진 셀들이 서로 의존하는 모양이면 Jotai가 자연스럽다.

## Redux Toolkit — 여전히 가치 있는 자리

Redux는 죽지 않았다. 다만 자리가 분명해졌을 뿐이다. 현대의 Redux는 거의 항상 Redux Toolkit(RTK)를 가리키고, 옛날의 보일러플레이트(switch문 reducer, action type 상수, action creator를 따로따로 손으로 쓰던 시절) 대부분은 사라졌다. `createSlice` 한 줄에 reducer와 action이 함께 정의된다.

```tsx
import { configureStore, createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { Provider, useDispatch, useSelector } from "react-redux";

type Task = { id: number; title: string; done: boolean };

const tasksSlice = createSlice({
  name: "tasks",
  initialState: [] as Task[],
  reducers: {
    added: {
      reducer(state, action: PayloadAction<Task>) {
        state.push(action.payload); // Immer 덕분에 mutate처럼 써도 된다
      },
      prepare(title: string) {
        return { payload: { id: Date.now(), title, done: false } };
      },
    },
    toggled(state, action: PayloadAction<number>) {
      const t = state.find((t) => t.id === action.payload);
      if (t) t.done = !t.done;
    },
  },
});

export const { added, toggled } = tasksSlice.actions;
export const store = configureStore({
  reducer: { tasks: tasksSlice.reducer },
});

type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

function TaskList() {
  const tasks = useSelector((s: RootState) => s.tasks);
  const dispatch = useDispatch<AppDispatch>();
  return (
    <ul>
      {tasks.map((t) => (
        <li key={t.id} onClick={() => dispatch(toggled(t.id))}>
          {t.done ? "✔ " : ""}
          {t.title}
        </li>
      ))}
    </ul>
  );
}
```

Zustand에 비해 코드가 길어 보이는 건 사실이다. 그런데도 RTK가 여전히 큰 자리를 지키는 이유가 있다.

첫째, **시간여행 디버깅**. Redux DevTools에서 모든 action을 timeline으로 보고, 임의의 시점으로 state를 되돌리고, action을 다시 재생할 수 있다. 복잡한 위저드, 다단계 폼, 복잡한 도메인 로직을 디버깅할 때 이건 진짜 무기다. Zustand로도 미들웨어를 붙이면 비슷하게 갈 수 있지만, RTK는 표준 워크플로다.

둘째, **팀 표준과 학습 곡선의 평탄함**. 큰 팀에서 50명, 100명이 같이 일할 때 "여기서는 이렇게 한다"라는 단일 패턴이 있다는 것 자체가 자산이다. RTK는 그 패턴이 매우 명확하다. 새로 합류한 사람도 createSlice 몇 개 보면 패턴을 파악한다.

셋째, **미들웨어 생태계**. redux-saga, redux-observable 같은 복잡한 비동기 흐름 제어, redux-persist 같은 영속화, listener middleware 등이 풍부하다. 정말 복잡한 동기화 로직(예: 결제 흐름, 멀티스텝 트랜잭션, 외부 시스템과의 양방향 동기화)에서 이게 빛난다.

넷째, **RTK Query**. RTK 안에는 사실 우리가 앞에서 본 TanStack Query와 유사한 데이터 페칭 도구가 들어 있다. RTK를 이미 쓰는 팀에서는 별도 라이브러리 없이 서버 캐시 문제까지 같은 우산 아래에서 풀 수 있다(다만 캐시 도구의 표현력만 보면 여전히 TanStack Query가 더 넓다는 평이 일반적이다).

요약하자면 Redux Toolkit은 **대규모 팀, 복잡한 도메인, 시간여행 디버깅이 필요한 자리**에서 여전히 가장 안정적인 선택지다. 작은 앱에서 "나중에 커질 거니까 일단 깔자"라는 이유로 끌어들이면, 보일러플레이트는 거의 없어졌다지만 그래도 Zustand보다는 묵직하다는 점에서 후회할 가능성이 있다.

## 잠깐 — 같은 자리 다른 도구들 한눈에

여기서 한 호흡 쉬어가자. 지금까지 본 네 도구를 같은 표 위에 올려보면, 각자가 어디서 빛나고 어디서 흐려지는지가 더 또렷해진다.

| 도구 | 사상 한 줄 | 구독 단위 | Provider 필요 | 공식 DevTools | 어울리는 자리 | 어울리지 않는 자리 |
|---|---|---|---|---|---|---|
| Context+Reducer | "React가 이미 가진 prop drilling 해결" | Provider 단위(전체) | 필요 | 없음 | 자주 안 변하는 글로벌, 작은 앱의 단순 공유 | 자주 변하는 큰 객체, selective subscription 필요 |
| Zustand | "단일 store + selector hook" | selector 결과 | 불필요(모듈) | 미들웨어로 추가 | 작은-중간 앱의 자주 변하는 UI 상태 | 그래프형 의존성, 엔터프라이즈 표준 강제 |
| Jotai | "atom 단위의 의존성 그래프" | atom 단위 | 보통 한 번 | 미들웨어로 추가 | 셀/노드 단위 도메인, 폼·에디터 | 큰 단일 객체 도메인 |
| Redux Toolkit | "단일 store + 표준화된 패턴 + 시간여행" | selector 결과 | 필요(Provider) | 표준(Redux DevTools) | 큰 팀, 복잡한 미들웨어, 시간여행 | 작은 앱, 빠르게 시제품 만들 때 |

표를 가만히 보면 한 가지가 또 보인다. 네 도구 어디에도 "서버 상태"라는 칸이 없다는 점이다. 의도적이다. **서버 상태는 이 표 위가 아니라 표 옆에 따로 놓이는 도구(TanStack Query/SWR/RTK Query)의 자리**이기 때문이다. 자꾸 강조하게 되는데, 이 자리만 정확히 잡으면 사실 도구 회의의 절반은 끝난다.

그리고 여기 적힌 "구독 단위" 칸을 다시 한번 음미해보자. Context는 Provider가 흔들리면 그 아래가 다 흔들리고, Zustand/Redux는 selector가 좁혀주는 만큼 좁혀지고, Jotai는 atom 단위로 처음부터 좁혀져 있다. **결국 selective subscription의 "단위가 어디까지 작아질 수 있는가"가 도구마다 다르다는 게 본질**이고, 그 단위가 우리 화면의 리렌더 비용을 결정한다.

## 사례로 보는 도구 매칭 — 익숙한 화면 다섯 가지

추상적인 트리만 보면 "그래서 내 화면에는?"이 잘 안 떠오를 수 있다. 흔히 만나는 다섯 가지 화면을 가지고 도구를 직접 매핑해보자. 이걸 읽고 나면 각자의 프로젝트에 적용하기가 한결 수월해질 거다.

**사례 1 — 대시보드의 KPI 카드 + 차트.** 카드와 차트는 모두 서버에서 받아오는 집계 데이터를 보여준다. 5분에 한 번 자동 갱신, 사용자가 탭 다녀오면 갱신, 같은 데이터를 여러 카드가 공유. 누가 봐도 **TanStack Query**의 자리다. UI 상태라고 부를 만한 건 "어떤 기간을 보고 있나(7일/30일/90일)" 정도인데, 이건 URL query string으로 두면 새로고침에도 살아남고 deep link도 된다. 라이브러리 한 줄 들이지 않아도 풀린다.

**사례 2 — 멀티스텝 결제 위저드.** 단계, 입력값, 약관 동의, 카드 정보 마스킹 표시, "이전 단계로 돌아가도 입력 보존" 같은 요건. 정본은 마지막에 한 번 서버로 가는 결제 호출 한 번뿐, 그 사이의 모든 데이터는 클라이언트가 들고 있다. 단계가 많고 분기가 복잡하다면 **useReducer**로 시작하고, 시간여행 디버깅이 가치가 있다 싶으면 그제야 **Redux Toolkit**으로 옮겨가는 식이 자연스럽다. Zustand로 가도 되지만, 위저드 특유의 "어떤 action 시퀀스로 이 상태가 만들어졌나"를 디버깅하는 자리에서는 RTK가 의외로 빛난다.

**사례 3 — 카탈로그 검색 페이지(필터 + 결과 리스트).** 결과 리스트는 서버 상태(**TanStack Query**), 필터/정렬/페이지네이션 파라미터는 — 새로고침에 살아남아야 하니까 — URL query string. 여기서 흔히 하는 실수가 필터 상태를 Redux/Context에 두고 URL과 별도로 동기화하는 것이다. 두 정본이 생기면 동기화 버그의 시작점이다. **URL 자체를 정본으로 두자.** TanStack Query의 queryKey에 그 파라미터를 넣으면 "필터 바뀌면 자동으로 새 쿼리"까지 거저 따라온다.

**사례 4 — 협업 칸반 보드.** 카드 위치, 컬럼, 멤버, 라벨 — 모두 서버 정본. 게다가 다른 사용자가 동시에 편집한다(WebSocket 푸시). 서버 상태 도구가 본격적으로 빛나는 자리다. **TanStack Query** + WebSocket 이벤트로 invalidation을 트리거하는 패턴이 표준이다. UI 상태로 분류되는 건 "지금 드래그 중인 카드 ID", "열려 있는 카드 모달" 정도인데, 이 자리가 selective subscription이 의미를 갖는 자리다 — 카드를 드래그하는 동안 1초에 60번 좌표가 바뀌는데, 이걸 Context 통째로 흔들면 트리 전체가 깨어난다. 드래그 좌표 같은 건 **Zustand**(혹은 Jotai의 atom)로 두고, 그 좌표를 정말 보는 컴포넌트만 깨우자.

**사례 5 — 디자인 툴/그래프 에디터.** 노드, 엣지, 셀, 속성 패널, 선택 상태, 임시 변형. 셀끼리 서로 의존하고("이 셀의 합은 저 셀들의 합"), 어떤 노드가 바뀌면 그 노드와 그것에 의존하는 것들만 다시 그리고 싶다. **Jotai**의 사상이 가장 자연스럽게 들어맞는 자리다. atom 그래프 자체가 도메인 모델이 되고, useAtomValue가 셀 단위 구독을 그대로 표현한다. 같은 일을 Zustand로 못 할 건 없지만, selector를 매번 깊게 짜야 해서 코드가 무거워지기 쉽다.

이 다섯 사례에서 공통적으로 보이는 흐름이 있다. 거의 항상 **서버 상태부터 떼어내고**, **남은 UI 상태의 모양을 본 뒤에**, 도구를 고른다는 점이다. 그리고 도구가 하나로 안 끝나는 경우도 자주 있다. 칸반 사례처럼 한 화면에 TanStack Query와 Zustand가 같이 사는 게 자연스러운 일이다.

## 마이그레이션 시나리오 — 이미 잘못 끼워졌다면

지금까지는 신규 프로젝트의 화이트보드를 가정했지만, 솔직히 우리 대부분은 신규 프로젝트보다 기존 프로젝트를 만진다. 이미 누군가가 첫 주 회의에서 결정한 도구가 있고, 그 도구가 1~2년 굴러왔다. 어딘가는 잘 굴러가고, 어딘가는 안 굴러간다. 어떻게 손대야 할까?

먼저 한 가지 원칙을 박아두자. **잘 굴러가는 자리는 굳이 옮기지 말자.** "이게 진짜 정답"이라고 옮기다가 일주일치 작업이 만들어지고, 그 작업이 끝나도 사용자가 체감하는 건 거의 없다. 우리가 옮겨야 하는 건 **통증이 있는 자리**다. 통증의 모양은 보통 정해져 있다.

**통증 1 — "캐시 무효화가 손에 잡히지 않는다."** 새 글을 등록하면 어떤 화면은 갱신되고 어떤 화면은 안 된다. 누가 어디서 setPosts를 다시 부르는지 추적하기 어렵다. 콜백을 props로 내리고 또 내리는 사슬이 길어졌다. 이건 거의 100% **서버 상태인데 클라이언트 도구로 다루고 있다**는 신호다. 그 slice 하나만 떼어 TanStack Query로 옮기자. 한꺼번에 옮길 필요는 없다. 가장 통증이 큰 한 도메인부터.

**통증 2 — "Profiler에서 같은 컴포넌트가 1초에 수십 번 다시 렌더된다."** 보통 Context value가 자주 바뀌고 컨슈머가 많은 자리다. 먼저 **Provider를 쪼개는** 우회법으로 시작하자(자주 변하는 영역과 안 변하는 영역 분리). 쪼갰는데도 안 풀리거나, 쪼개는 게 너무 복잡해지면 그제야 **Zustand**로 옮길 시점이다. 옮길 때도 전체를 한 번에 들어내지 말고, 그 자주 변하는 슬라이스만 store로 옮기자. Context는 안 변하는 글로벌의 자리로 남겨두면 된다.

**통증 3 — "Redux store가 너무 커져서 새 사람이 못 따라온다."** 자주 듣는 호소다. 여기서도 가장 먼저 할 일은 **store 안의 slice를 클라이언트 상태/서버 상태로 분류하는 것**이다. 보통 절반쯤은 서버 상태였다는 발견이 따라오고, 그것만 RTK Query 혹은 TanStack Query로 옮겨도 store가 눈에 띄게 가벼워진다. 그러고도 남은 부분이 정말 큰 클라이언트 상태(예: 복잡한 도메인 에디터)라면, 그건 RTK를 유지할 가치가 있다. 줄이는 게 목적이지 없애는 게 목적이 아니다.

**통증 4 — "도구가 너무 많아져서 새 합류자가 어디에 무엇이 있는지 모른다."** 반대 방향의 통증이다. 한 앱 안에 Redux, Zustand, Jotai, Context, TanStack Query, SWR이 다 살고 있다. 이쯤 되면 도구 자체보다 **컨벤션**의 문제다. 팀 차원에서 "서버 상태는 X, 큰 UI 상태는 Y, 글로벌 상수는 Z"로 한 번 정리하고, 점진적으로 정리해 나가자. 한 번에 다 정리하지 않아도 된다.

마이그레이션의 비용은 생각보다 작다 — 단, 위 원칙을 지킬 때만이다. **한 번에 한 도메인, 통증이 있는 자리부터, 점진적으로.** "전부 갈아엎는다"는 의지로 시작한 마이그레이션이 끝까지 가는 경우를 거의 보지 못했다.

## 의사결정 트리 — 신호에서 도구로

이제 각 도구의 사상을 다 보았으니, 머리에 넣을 결정 트리를 한 페이지로 그려보자. 이 트리는 외울 게 아니라 **사고의 흐름** 으로 익혀야 한다.

**0단계 — 이게 정말 클라이언트 상태인가?**
- 서버에서 받아온 데이터다 → **TanStack Query / SWR**. 이 분기가 가장 먼저다.
- 클라이언트에서 만들어지는 일시적 화면 상태다 → 1단계로.

**1단계 — 이 상태를 누가 쓰는가?**
- 한 컴포넌트만 쓴다 → **useState** (또는 useReducer).
- 부모-자식 몇 단계만 쓴다 → **props로 내려줘라**. 끌어올리고, 안 쓰게 되면 다시 내려라(Lift, then Drop).
- 트리의 여러 깊은 자리에서 쓴다 → 2단계로.

**2단계 — 얼마나 자주 바뀌는가?**
- 거의 안 바뀐다(theme, locale, 로그인 사용자) → **Context**. Provider를 영향 범위에 맞춰 트리 안쪽에 두자.
- 자주 바뀌고, 컨슈머가 많다 → 3단계로.

**3단계 — 도메인의 모양은?**
- 하나의 큰 객체가 통째로 변하는 모양, 작은-중간 규모 앱 → **Zustand**.
- 작은 셀들이 서로 의존하는 그래프형 도메인 → **Jotai**.
- 큰 팀, 복잡한 비동기 흐름, 시간여행 디버깅이 가치가 있는 규모 → **Redux Toolkit**.

이 트리에서 가장 중요한 건 **0단계**라는 사실을 다시 한번 강조하자. 0단계를 건너뛰고 1~3단계에서 도구를 고르면, 어떤 도구를 골라도 결국 잘못된 자리에 잘못된 도구를 끼우는 결과가 된다. 그러니 도구 회의에 들어가기 전에, 화이트보드에 우리 앱의 상태들을 다 적어놓고 한 번 분류부터 해보자.

```
서버 상태:                 UI 상태:
- 글 목록                  - 사이드바 열림/닫힘
- 사용자 프로필             - 다크모드
- 댓글                     - 폼 입력값
- 알림                     - 위저드 단계
- 장바구니(서버 저장형)      - 모달 스택
```

이렇게 두 칸으로 나누고 나면, 왼쪽 칸은 TanStack Query가 가져가고 오른쪽 칸만 가지고 1~3단계 트리를 적용하면 된다. 이 한 번의 분류만으로도 회의의 절반은 정리된다.

## 흔한 잘못된 결정들

도구 선택에서 우리가 자주 빠지는 함정 몇 가지를 짚어보자. 하나씩 거울처럼 자기 코드에 비춰보자.

**함정 1 — "나중에 커질 거니까 처음부터 Redux."**
신규 프로젝트의 첫 주에 가장 흔히 듣는 말이다. 그런데 정말 커진 프로젝트들 중 상당수가, 막상 까보면 Redux store의 절반은 사실 **서버 상태였다.** 그 절반은 Redux 도구로 풀기에 적합하지 않은 문제였다. 게다가 안 컸을 가능성도 절반쯤 있다. 미래의 규모를 가정한 도구 선택은 거의 항상 비싸게 끝난다. **현재의 통증에 맞춰 고르고, 통증이 보이면 그때 옮기자.** 이행 비용은 생각보다 작다.

**함정 2 — "Context에 다 때려박기."**
prop drilling이 싫어서 Context를 도입했는데, 어느 순간 Context 한 개에 사용자 정보, 테마, 토스트 메시지, 모달 스택, 사이드바 상태, 마지막 수정 시각, 검색어, 정렬 옵션이 다 들어 있는 풍경. 자주 본다. 이 Context가 한 번 흔들리면 트리 전체가 흔들린다. **자주 안 변하는 것과 자주 변하는 것을 같은 Context에 넣지 말자.** Provider를 쪼개거나, 자주 변하는 영역만 selective subscription 도구로 옮기자.

**함정 3 — "서버 캐시를 useState/Context로."**
앞 절에서 길게 다뤘으니 짧게만. 서버에서 받은 데이터를 useState에 들고 있으면, 결국 캐시 라이브러리를 손으로 다시 발명하게 된다. **재발명 말고 도입하자.** TanStack Query/SWR/RTK Query 중 팀에 맞는 걸 고르면 된다.

**함정 4 — "하나의 도구로 모든 걸 해결."**
"우리는 Redux로 모든 상태를 관리합니다"라거나 "우리는 Zustand로 다 합니다"라는 단호한 선언을 종종 듣는다. 사실은 한 앱 안에 여러 도구가 공존하는 게 자연스럽다. 서버 상태는 TanStack Query, 큰 글로벌 UI 상태는 Zustand, 자주 안 변하는 글로벌(theme, locale)은 Context, 한 컴포넌트의 로컬 상태는 useState — 이렇게 **층마다 적합한 도구**가 다르다. 이게 일관성 없는 게 아니라, **각 문제에 맞는 도구**를 쓰는 거다.

**함정 5 — "이 라이브러리 좋다더라" 기반 선택.**
트위터/블로그/HN 헤드라인 기반으로 도구를 고르고 있다면 잠시 멈추자. 좋은 도구는 많고, 우리 프로젝트에 맞는 도구는 그중 일부다. **신호에서 출발해 도구로 가야지, 도구에서 출발해 신호를 만들어내면 안 된다.** "Zustand 한번 써보고 싶었는데 마침 잘됐다"는 동기는 사이드 프로젝트에서나 즐기자.

**함정 6 — "useEffectEvent 같은 신기한 게 나왔으니 다 갈아엎자."**
도구는 진화한다. RSC, use(promise), useEffectEvent, Suspense 모드 등 새 옵션이 계속 나온다. 그렇다고 매번 잘 돌아가는 코드를 쫓아가며 갈아엎을 필요는 없다. **새 도구는 새 코드에서 먼저 시도하고, 기존 코드는 통증이 생긴 자리에만 점진적으로 적용하자.**

## TypeScript로 본 도구별 타입 감각

마지막으로 짧게 언급하고 갈 게 있다. 도구마다 TypeScript와 만나는 결이 조금씩 다르다는 점이다. 같은 도메인을 표현해도, 도구마다 타입 추론이 자연스러운 자리와 손으로 단언해줘야 하는 자리가 다르다.

**Zustand의 타입 감각.** `create<State>()`에 명시적으로 타입을 박아주면 그 안의 모든 selector가 자동으로 추론된다. 깔끔하다. 다만 미들웨어를 끼우면 `create<State>()(devtools(persist(...)))` 같은 합성에서 제네릭이 다소 번거로워진다 — 공식 문서에 패턴이 정리돼 있으니 그대로 따르면 된다.

```ts
type State = { count: number; inc: () => void };
const useStore = create<State>()((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
}));

const count = useStore((s) => s.count); // number로 자동 추론
```

**Jotai의 타입 감각.** atom의 타입은 초기값으로부터 추론되거나 제네릭으로 박는다. `atom<Task[]>([])`처럼. 파생 atom은 read 함수의 반환 타입으로 추론된다. 셀 단위라 타입이 작게 쪼개져, 타입 표면적이 자연히 좁다.

**Redux Toolkit의 타입 감각.** `createSlice`가 reducer 안의 `state` 타입을 자동으로 좁혀주고, action creator의 payload 타입도 `PayloadAction<T>`로 자연스럽다. 다만 store 단계에서 `RootState = ReturnType<typeof store.getState>` 같은 타입 별칭을 한 번 만들어두는 게 관용이다. `useSelector`와 `useDispatch`도 `useAppSelector`/`useAppDispatch`로 한 번 더 감싸 타입을 박아두는 패턴이 표준이다.

**TanStack Query의 타입 감각.** `useQuery`의 `data` 타입은 `queryFn`의 반환 타입으로 추론된다. 그래서 `queryFn`을 잘 타이핑하는 게 곧 컴포넌트 단의 타입 안정성으로 이어진다. `select` 옵션을 쓰면 selector가 또 한 번 타입 변환을 해준다 — 서버 응답을 화면용 모델로 바꾸는 자리에 이 옵션이 좋다.

여기서 한 가지 당부. **타입을 위해 도구를 고르지는 말자.** 모든 도구가 충분히 잘 타이핑되고, 차이는 미묘한 결의 문제일 뿐이다. 도구는 어디까지나 풀고 있는 문제의 모양에 맞춰 고르고, 타입은 그 도구의 관용을 따라가면 된다.

## "처음 한 주" 결정 워크시트

마지막으로, 이 장을 다 읽고 나서도 막상 신규 프로젝트의 화이트보드 앞에 서면 머리가 다시 안개 속이 된다는 사실을 인정하자. 그래서 한 장짜리 워크시트를 머리에 박아두자. 다음 다섯 줄을 순서대로 채우는 거다.

1. **이 앱이 다루는 데이터를 모두 적어라.** 화면 단위가 아니라 데이터 단위로. 글, 사용자, 댓글, 알림, 다크모드, 사이드바 토글, 검색어, 정렬 옵션, 위저드 단계, …
2. **각 데이터 옆에 정본의 위치를 적어라.** "서버" / "클라이언트" / "URL" / "localStorage" 중 하나.
3. **"서버"인 줄을 묶어라.** 이건 통째로 서버 상태 도구의 자리다(TanStack Query/SWR/RTK Query). 한 도구로 통일.
4. **"URL"인 줄을 묶어라.** 이건 라이브러리 없이 URL query string + history API로 푼다. 새로고침/딥링크에 살아남는다는 보너스가 따라온다.
5. **남은 "클라이언트"/"localStorage" 줄에 결정 트리를 적용하라.** 한 컴포넌트만 쓰면 useState, 몇 단계만 내리면 props, 트리 전반에 걸치고 자주 안 변하면 Context, 자주 변하면 Zustand/Jotai/RTK 중 도메인 모양에 맞는 것.

이 다섯 줄짜리 워크시트가, 회의 한 시간 동안 결론 안 나던 도구 논쟁을 보통 십 분 안에 끝내준다. 더 정확히 말하면, 도구 논쟁이라는 게 **사실은 데이터 분류 작업이었다**는 사실을 드러내준다. 도구는 그 분류의 결과로 자연스럽게 따라온다.

## 자기 점검 — "내가 지금 풀고 있는 문제는 정말 클라이언트 상태인가?"

이 장의 마지막 질문은 결국 한 가지로 수렴한다. 도구를 고르기 전에, 매번 이렇게 자문해보자.

> "내가 지금 useState/useReducer/Context/Zustand로 다루려는 이 데이터, 진짜 클라이언트 상태인가? 사실은 서버 어딘가에 정본이 있고, 우리는 그 사본을 보고 있을 뿐 아닌가?"

이 질문에 정직하게 답하기 시작하면, 다음과 같은 발견들이 따라온다.

- "내 Redux store의 60%는 사실 서버 상태였다."
- "이 Context 안의 사용자 프로필, 사실 새로고침하면 다시 받아와야 하는 거였네."
- "장바구니 — 로그인 사용자의 장바구니는 서버 상태고, 비로그인 사용자의 장바구니는 클라이언트 상태(localStorage 동기)였구나."
- "이 댓글 목록에 useEffect로 fetch해서 useState에 넣고 있는데, 이건 사실상 캐시 문제였다."

이런 발견 하나하나가 우리 코드를 가볍게 만든다. 잘못된 자리에서 잘못된 도구로 풀던 문제가 사라지고, 도구는 자기 자리에서 자기 일을 한다. 이게 도구 선택의 본질이다. **도구는 자기를 위해 고르는 게 아니라, 문제의 모양에 맞춰 고른다.**

## 핵심 정리

이번 장에서 함께 본 것을 정리해두자.

1. **"상태 관리 라이브러리"라는 말은 절반의 진실이다.** UI 상태와 서버 상태는 본질이 다른 문제이고, 다른 도구가 필요하다.
2. **서버 상태는 캐시다.** fetch + cache + invalidation + retry + revalidation은 한 묶음의 문제이고, 이걸 손으로 다시 발명하지 말자.
3. **"React IS your state management library."** 동시에 **"server cache state is different."** 두 문장이 함께 참이다.
4. **TanStack Query/SWR**: 서버를 진실의 소유자로 두고 클라이언트는 캐시 동기화 — 컴포넌트는 "무엇"만 선언, "어떻게"는 라이브러리.
5. **Context**: 자주 안 변하는 글로벌(theme, locale, 로그인 사용자)에 어울린다. selective subscription이 없으니 자주 변하는 큰 객체에는 어울리지 않는다.
6. **Zustand**: 단일 store + hook 단위 selector + 얕은 비교. 작은-중간 규모 앱에서 selective subscription이 필요해진 자리의 표준 후보.
7. **Jotai**: bottom-up atom 모델. 셀들이 서로 의존하는 그래프형 도메인(폼, 에디터, 차트)에 어울린다.
8. **Redux Toolkit**: 시간여행 디버깅, 큰 팀의 단일 패턴, 복잡한 미들웨어 생태계가 필요한 자리. RTK Query를 함께 쓰면 캐시 문제까지 같은 우산.
9. **결정 트리의 0단계는 "이게 서버 상태인가?"다.** 이 분기를 건너뛰면 어떤 도구를 골라도 절반은 틀린다.
10. **함정들**: 미래 규모 가정한 Redux 기본 도입, Context에 자주 변하는 것까지 다 몰아넣기, 서버 캐시를 useState로, 하나의 도구로 모든 것 해결.
11. **한 앱 안에 여러 도구가 공존하는 게 자연스럽다.** 서버 상태는 TanStack Query, 큰 UI 상태는 Zustand, 안 변하는 글로벌은 Context, 로컬은 useState — 각 층에 어울리는 도구.
12. **도구는 신호에서 출발해 고른다.** "Zustand 써보고 싶다"가 아니라 "selective subscription이 필요해졌다"가 출발점이어야 한다.

## 연습 문제

머리로만 알아두면 한 달이면 휘발된다. 손으로 한 번씩 짚어보자.

**[기초] 1.** 7장에서 만든 TasksContext 기반 앱에 `lastModifiedAt` 필드를 추가하고, 1초마다 갱신되도록 setInterval을 걸어보자. React DevTools Profiler로 컴포넌트 리렌더 횟수를 측정한 뒤, 같은 앱을 Zustand로 옮겨 selector로 슬라이스를 분리한 다음 다시 측정하자. 어떤 컴포넌트의 리렌더가 사라졌는가? 사라지지 않은 컴포넌트가 있다면 selector를 어떻게 다시 짜야 하는가?

**[기초] 2.** 작은 카운터 앱을 (a) Context+useReducer, (b) Zustand, (c) Jotai 세 가지로 똑같이 구현하고, 각각의 코드량/구독 단위/리렌더 동작을 비교해보자. 어떤 도구가 어떤 자리에서 더 자연스러운지 자기 말로 한 줄씩 정리해보자.

**[중] 3.** 글 목록을 useState + useEffect로 fetch하던 컴포넌트(이 장 본문의 첫 PostList)를 TanStack Query로 마이그레이션하자. 그다음 같은 페이지에서 같은 데이터를 보는 다른 컴포넌트를 하나 추가했을 때, 네트워크 탭에서 fetch가 한 번만 일어나는지 확인하자. 이어서 새 글을 POST하는 mutation을 추가하고, `invalidateQueries`로 자동 갱신이 되는지 확인하자.

**[중] 4.** 우리 프로젝트(혹은 가상의 칸반 앱)의 모든 상태를 서버 상태/UI 상태 두 칸으로 나눠 적어보자. UI 상태에 대해 본문의 결정 트리를 적용해 어떤 도구가 어울리는지 매핑하자. "원래 Redux/Context에 있던 것 중 사실은 서버 상태였던 것"이 몇 % 정도인가?

**[도전] 5.** 기존 Redux 앱(없으면 가상의 한 화면 시나리오)에서, 사실은 서버 상태였던 slice 하나를 골라 TanStack Query로 분리하자. 분리 전후로 코드량, 캐시 일관성, 새로고침 후 동작, 다른 탭에서 돌아왔을 때의 동작이 어떻게 바뀌는지 정리하자. 분리하면서 발견한 "Redux로 풀려고 손으로 짠 캐시 로직"은 무엇이었는가?

## 한 가지 더 — "도구를 고르는 안목" 자체가 자산이다

이 장을 닫기 전에 짧게 한 가지만 더 짚어두고 가자. 도구 선택은 한 번 하고 끝나는 일회성 결정이 아니다. 우리는 앞으로도 새 프로젝트를 시작할 때마다, 새 화면을 추가할 때마다, 통증이 생긴 자리를 손볼 때마다 이 결정을 반복해 내릴 거다. 그러니 도구 그 자체보다 **그 도구를 고르는 안목**을 손에 익히는 게 길게 보면 더 큰 자산이다.

그 안목의 핵심은 거듭 강조했듯이 단순하다. **데이터의 종류를 먼저 보고, 그다음에 도구를 본다.** 서버 상태인지 클라이언트 상태인지, URL에 담길 만한지 메모리에 머무를 건지, 한 컴포넌트의 일인지 트리 전반의 일인지, 자주 변하는지 거의 안 변하는지. 이 질문 다섯 줄을 마음속에 두고 있는 사람과 그렇지 않은 사람의 코드는, 1년 뒤에 분명히 다른 모양이 된다.

그리고 도구를 결정하고 나서도 한 가지를 잊지 말자. **도구는 종속이 아니다.** 잘못 끼워졌으면 옮기면 된다. 옮기는 비용은 보통 우리가 두려워하는 만큼 크지 않다 — 단, 한 번에 한 도메인씩, 통증이 있는 자리부터, 점진적으로 옮길 때만이다. 도구를 결혼 상대처럼 신중하게 골라야 한다는 압박에서 한 발 떨어져 보자. 도구는 어디까지나 도구다.

## 마무리 — 1부의 끝, 그리고 경계로

여기까지가 React 안에서 데이터가 흐르는 세계다. 우리는 1장에서 "상태가 무엇이고 왜 어려운가"를 바닥부터 짚었고, useState와 useReducer로 단일 컴포넌트의 상태 모델링을 익혔고, 끌어올리기와 key로 컴포넌트 사이의 동기화·리셋을 다뤘고, Context와 Reducer 조합으로 트리 단위 상태 공유의 표준을 익혔고, 마지막으로 이 장에서 그 한계를 넘어 외부 라이브러리들의 자리를 분명히 정리했다. 그리고 그 과정에서 우리는 한 가지 사실을 거듭 마주쳤다. **모든 상태가 같은 종류는 아니다. 그리고 한 종류 — 서버 상태 — 는 사실 React 바깥의 세계와 닿아 있다.**

이게 2부로 이어지는 다리다. 1부에서 우리가 다룬 도구들 — useState, useReducer, Context, Zustand, Jotai, Redux Toolkit — 은 모두 React가 직접 알고 관리하는 데이터의 세계 안에서 작동했다. 하지만 우리 앱은 그 세계 안에서만 살지 않는다. 브라우저 DOM, 타이머, 외부 위젯, WebSocket, 카메라, 지도 라이브러리, 그리고 — 우리가 방금 본 — 서버. 이런 것들은 React가 모르는, 혹은 자기 데이터 흐름 안에서 직접 표현하지 못하는 외부 시스템이다.

서버 상태가 별도 도구로 풀어야 했던 이유도 결국 같은 자리다. **그건 외부 세계의 한 종류였다.** 그리고 그 외부 세계를 React 컴포넌트와 어떻게 만나게 할 것인가, 그 경계에서 어떤 도구가 필요한가 — 이게 2부의 주제다. 우리는 ref와 Effect라는 두 개의 escape hatch를 만나게 될 거다. 이름만 들어도 짐작되듯이, 이건 React의 데이터 흐름에서 잠시 빠져나와 외부와 손을 잡는 자리다.

다음 장은 1부와 2부 사이의 다리 역할을 하는 짧은 전환 챕터다. 거기서 우리는 "경계"라는 단어를 정식으로 도입하고, escape hatch라는 이름이 왜 escape이고 왜 hatch인지 — 그리고 그 자리에서 우리가 무엇을 조심해야 하는지 — 를 함께 이야기해보자. 그러고 나서 2부의 본격적인 도구들로 들어간다.

여기까지 따라온 우리, 이미 React 상태 관리의 멘탈 모델 절반은 단단해졌다. 잠시 숨을 고르고, 경계로 가자.
