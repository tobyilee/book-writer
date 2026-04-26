# 부록 A — React 18 → 19 마이그레이션 노트

## 왜 이 부록이 필요한가

본문은 React 18을 기준으로 썼다. 이유는 단순하다. 멘탈 모델을 흔드는 일과 새 API를 익히는 일을 한꺼번에 하면 둘 다 어설프게 끝난다. 그래서 18의 어휘로 "상태는 함수의 입력이고, Effect는 동기화고, Ref는 경계다"를 먼저 자리잡게 했다. 이제 그 위에 19의 변화를 얹어 보자.

19의 변화 중 일부는 우리가 본문에서 말한 원칙을 *문법 차원에서* 더 깔끔하게 만들어 준다. `forwardRef`가 사라진 자리가 그 대표 예다. 일부는 새로운 패러다임 — Suspense·Server Components와 더 잘 맞물리도록 만들어진 다리다. `use(promise)`, Actions, `useFormState`, `useOptimistic`이 그쪽이다. 그리고 React Compiler는 우리가 그동안 손으로 들고 다니던 `useMemo`/`useCallback`/`React.memo`라는 짐을 점점 내려놓게 만들어 주는 흐름이다.

이 부록은 이 다섯 갈래를 차례로 짚는다. 깊은 튜토리얼은 아니다. *어디가 어떻게 바뀌었고, 무엇을 마이그레이션해야 하며, 무엇은 그대로 두어도 되는가*를 명확히 하는 게 목표다.

## 1. ref-as-prop — `forwardRef` 졸업

10장에서 우리는 `useImperativeHandle`을 다루며 한 가지 잡음을 견뎠다. 자식 컴포넌트가 부모로부터 ref를 받으려면 `forwardRef`로 한 번 감싸야 했다. TypeScript에서는 제네릭 타입 인자를 두 개나 적어야 했고, 디스플레이 네임이 안 잡혀서 React DevTools에 `_c2` 같은 정체불명 이름이 떴다. 익숙해질 수는 있었지만 본질적으로는 *문법적 잡음*이었다.

React 19에서 함수 컴포넌트는 `ref`를 그냥 prop으로 받는다.

**React 18:**

```tsx
import { forwardRef, useImperativeHandle, useRef } from "react";

interface MyInputHandle {
  focus: () => void;
}

interface MyInputProps {
  placeholder?: string;
}

const MyInput = forwardRef<MyInputHandle, MyInputProps>(
  function MyInput({ placeholder }, ref) {
    const realRef = useRef<HTMLInputElement>(null);
    useImperativeHandle(ref, () => ({
      focus() {
        realRef.current?.focus();
      },
    }));
    return <input ref={realRef} placeholder={placeholder} />;
  }
);
```

**React 19:**

```tsx
import { useImperativeHandle, useRef, type Ref } from "react";

interface MyInputHandle {
  focus: () => void;
}

interface MyInputProps {
  placeholder?: string;
  ref?: Ref<MyInputHandle>;
}

function MyInput({ placeholder, ref }: MyInputProps) {
  const realRef = useRef<HTMLInputElement>(null);
  useImperativeHandle(ref, () => ({
    focus() {
      realRef.current?.focus();
    },
  }));
  return <input ref={realRef} placeholder={placeholder} />;
}
```

`forwardRef`라는 래퍼가 사라졌다. props 타입에 `ref?: Ref<...>`를 그냥 한 줄 추가하면 된다. 디스플레이 네임도 함수 이름이 그대로 잡힌다. *이것은 새 기능이 아니라 잡음의 제거다*. 그런 마이그레이션은 환영하지 않을 이유가 없다.

`forwardRef`는 19에서도 deprecated 경고가 뜨는 정도이고, 아직 동작은 한다. 하지만 새 코드는 ref-as-prop으로 쓰고, 기존 코드는 시간 날 때 정리하는 편이 낫다. codemod도 공식 제공된다(`npx codemod@latest react/19/replace-use-form-state`와 같은 식으로 ref-as-prop용 변환도 함께 제공된다 — 사실 확인 필요).

## 2. `use(promise)` — Suspense와 만나는 새 방법

19에서 새로 들어온 `use`는 Hook의 모양을 빌렸지만 규칙이 한 가지 더 느슨하다. *조건문 안에서도 호출할 수 있다*. 그리고 Promise를 인자로 받으면 그 Promise가 resolve되기 전까지 가장 가까운 `<Suspense>` 경계에 "대기 중"이라는 신호를 보낸다.

```tsx
import { use, Suspense } from "react";

interface User {
  id: string;
  name: string;
}

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // 여기서 일시 중단된다
  return <h1>{user.name}</h1>;
}

function Page() {
  const userPromise = fetchUser("123");
  return (
    <Suspense fallback={<p>로딩 중...</p>}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

본문에서 우리는 race condition을 막기 위해 `let ignore = false`를 넣는 패턴을 익혔다. `use(promise)` + Suspense는 그 패턴이 풀던 문제의 결을 다르게 푼다 — *데이터를 기다리는 일을 컴포넌트 트리 자체가 표현*하게 한다. 그래서 "지금 로딩 상태를 어디에 둘까"라는 익숙한 질문이 거의 사라진다.

다만 한 가지만 짚고 가자. `use(promise)`를 effect 없이 컴포넌트 본체에서 직접 부르되, Promise는 *컴포넌트 바깥에서* 만들거나 안정된 캐시에서 받아 와야 한다. 본체에서 매번 `fetch(...)`를 새로 부르면 매 렌더마다 새 Promise가 만들어져 무한 Suspense에 빠진다. 보통은 React Server Components에서 prop으로 내려받거나, TanStack Query 같은 캐시 레이어에서 꺼낸다. 이 부록의 범위를 넘어서니, 이 정도 신호만 들고 다음 책으로 넘기자.

## 3. Actions / `useFormState` / `useOptimistic` — 폼 처리의 새 표준

폼 처리는 React에서 오래도록 보일러플레이트가 많은 영역이었다. 제출 중 상태, 에러, 성공 메시지, 낙관적 UI… 매 폼마다 `useState` 네 개와 `try/catch`를 손으로 쓰던 자리다.

19에서는 이 영역에 세 가지 표준이 추가됐다.

### 3.1 Action — `<form action={...}>`에 함수를 직접 넘긴다

```tsx
async function submitComment(formData: FormData) {
  await api.post("/comments", { text: formData.get("text") });
}

function CommentForm() {
  return (
    <form action={submitComment}>
      <textarea name="text" />
      <button type="submit">등록</button>
    </form>
  );
}
```

`<form>`이 동기적인 onSubmit 핸들러가 아니라 *비동기 함수*를 받을 수 있게 됐다. submit이 진행 중이면 React가 그 사실을 안다. 그래서 다음 두 훅이 의미를 가진다.

### 3.2 `useActionState` — 서버 응답을 상태로

(주의: 19 초기에는 `useFormState`라는 이름으로 들어왔다가 `useActionState`로 이름이 정리됐다. react-dom의 `useFormState`는 호환을 위해 남아 있다.)

```tsx
import { useActionState } from "react";

interface CommentState {
  ok: boolean;
  error?: string;
}

async function submitComment(
  prev: CommentState,
  formData: FormData
): Promise<CommentState> {
  try {
    await api.post("/comments", { text: formData.get("text") });
    return { ok: true };
  } catch (e) {
    return { ok: false, error: (e as Error).message };
  }
}

function CommentForm() {
  const [state, formAction, isPending] = useActionState(submitComment, {
    ok: false,
  });
  return (
    <form action={formAction}>
      <textarea name="text" />
      <button type="submit" disabled={isPending}>
        {isPending ? "등록 중..." : "등록"}
      </button>
      {state.error && <p>{state.error}</p>}
    </form>
  );
}
```

본문에서 익힌 `'idle' | 'submitting' | 'success' | 'error'` enum을 손으로 만들지 않아도, `isPending`과 reducer 형태의 상태가 자동으로 따라온다. *우리가 익힌 멘탈 모델을 React가 문법으로 흡수한 것*이라고 보면 정확하다.

### 3.3 `useOptimistic` — 낙관적 UI

```tsx
import { useOptimistic } from "react";

interface Comment {
  id: string;
  text: string;
  pending?: boolean;
}

function Comments({ comments }: { comments: Comment[] }) {
  const [optimisticComments, addOptimistic] = useOptimistic(
    comments,
    (state, newText: string): Comment[] => [
      ...state,
      { id: "tmp", text: newText, pending: true },
    ]
  );

  async function submit(formData: FormData) {
    const text = formData.get("text") as string;
    addOptimistic(text);
    await api.post("/comments", { text });
  }

  return (
    <>
      <ul>
        {optimisticComments.map((c) => (
          <li key={c.id} style={{ opacity: c.pending ? 0.5 : 1 }}>
            {c.text}
          </li>
        ))}
      </ul>
      <form action={submit}>
        <textarea name="text" />
        <button type="submit">등록</button>
      </form>
    </>
  );
}
```

낙관적 업데이트를 손으로 쓰던 시절에는 "임시 ID 생성 → 리스트에 추가 → 실패 시 롤백" 같은 로직을 직접 짜야 했다. `useOptimistic`은 그 사이클을 한 훅으로 모은다. 비동기 액션이 끝나거나 실패하면 자동으로 원래 상태로 복귀한다.

이 세 가지를 묶어서 보자. *폼은 이제 declarative하게 쓰는 게 표준*이다. submit 중 상태, 에러, 낙관적 UI를 우리가 손으로 묶지 않는다. 새 코드는 가능한 한 이 모양으로 쓰는 편이 낫다.

## 4. document metadata as JSX — `<title>`, `<meta>`를 그냥 렌더한다

지금까지 `<title>`이나 `<meta>` 같은 document head 메타데이터를 다루려면 `react-helmet`이나 Next.js의 `<Head>`처럼 별도 라이브러리에 의존해야 했다. 19부터는 React가 컴포넌트 본체 안에 적힌 `<title>`, `<meta>`, `<link>`를 자동으로 `<head>`로 호이스팅한다.

```tsx
function ProductPage({ product }: { product: { name: string; desc: string } }) {
  return (
    <article>
      <title>{product.name} — 우리 가게</title>
      <meta name="description" content={product.desc} />
      <link rel="canonical" href={`/p/${product.id}`} />
      <h1>{product.name}</h1>
      <p>{product.desc}</p>
    </article>
  );
}
```

이 한 가지가 작아 보이지만, 라우트마다 메타데이터를 갈아끼우던 코드를 한 단계 단순하게 만든다. 같은 페이지 안에 동일한 `name`의 `<meta>`가 여럿 들어가면 React가 마지막 것으로 합쳐 준다. SSR에서도 동일하게 작동한다.

본문 1부의 "진실은 한 자리에" 원칙이 그대로 적용된다 — 메타데이터의 진실을 그것을 쓰는 컴포넌트 옆에 두면 된다. *콜로케이션의 정신이 head까지 내려온 셈*이다.

## 5. React Compiler — 메모이제이션의 짐을 내려놓는 길

`useMemo`, `useCallback`, `React.memo`. 본문에서 우리가 일부러 깊이 들어가지 않은 영역이다. 이유는 둘이었다. 첫째, 이 도구들은 멘탈 모델보다는 성능 튜닝의 어휘다. 둘째, *어차피 곧 손에서 떠날 일*이라는 신호가 강했다.

React Compiler는 정확히 그 흐름의 끝에 있다. 컴포넌트와 훅 코드를 빌드 타임에 분석해, 필요한 자리에 메모이제이션을 자동으로 삽입한다. 우리가 손으로 적던 `useMemo`/`useCallback`/`React.memo`의 약 80~90%가 더 이상 필요 없어진다(2026년 시점 React 팀 발언 기준 — 사실 확인 필요).

```tsx
// React Compiler가 켜져 있다면, 이렇게 써도
function ProductList({ products, query }: Props) {
  const filtered = products.filter((p) => p.name.includes(query));
  const onClick = (id: string) => {
    /* ... */
  };
  return <List items={filtered} onClick={onClick} />;
}

// 아래처럼 손으로 적은 것과 비슷한 결과가 나온다
function ProductList({ products, query }: Props) {
  const filtered = useMemo(
    () => products.filter((p) => p.name.includes(query)),
    [products, query]
  );
  const onClick = useCallback((id: string) => {
    /* ... */
  }, []);
  return <List items={filtered} onClick={onClick} />;
}
```

지금 시점에 도입할 만한가? 2026년 4월 기준 React Compiler는 안정 버전(stable)에 가깝게 자리잡았고, Next.js 14+, React 19와 묶어 쓸 때 검증된 사례가 충분하다. *새 프로젝트라면 켜고 시작하는 편이 낫다*. 기존 프로젝트라면 한 모듈씩 점진적으로 켜며 측정하면서 들이는 게 안전하다 — 컴포넌트 안에 부수효과(예: 렌더 중 mutate)가 숨어 있다면 컴파일러가 보수적으로 빠진다(opt-out). 그 자리들은 어차피 이 책이 *원래부터 하지 말라고 부탁한* 패턴이다.

기억해 두자. 컴파일러는 우리가 익힌 멘탈 모델을 *대체하지 않는다*. 컴파일러는 좋은 멘탈 모델 위에서 더 잘 작동한다. 파생값을 state에 넣어 둔 코드를 컴파일러가 마법처럼 고쳐 주지는 않는다. 우리가 1부에서 익힌 어휘는 그대로 유효하다.

## 마이그레이션 체크리스트

큰 18 → 19 마이그레이션을 잡았다고 해 보자. 다음 순서를 권한다.

1. **공식 codemod 먼저 돌린다.** `npx codemod@latest react/19/migration-recipe`(또는 동등한 그 시점 권장 명령) 한 번이 ref-as-prop, deprecated API, `useFormState` → `useActionState` 같은 단순 치환을 자동으로 처리한다.
2. **`forwardRef` 자리를 ref-as-prop으로 정리한다.** codemod로 대부분 끝나지만, `useImperativeHandle`을 같이 쓰던 자리는 시그니처를 한 번씩 눈으로 본다.
3. **폼 처리 자리에 `useActionState`/`useOptimistic` 도입을 검토한다.** 모든 폼을 한 번에 갈아엎지 말고, 새로 쓰는 폼부터 새 모양으로 쓴다. 기존 폼은 깨지지 않은 한 그대로 두어도 된다.
4. **document metadata 라이브러리 제거를 검토한다.** `react-helmet`/`react-helmet-async`를 쓰고 있다면, 19의 네이티브 메타데이터로 옮기는 게 의존성 한 묶음을 정리해 준다. 단, 라우터(예: Next.js App Router)가 자체 `metadata` API를 제공한다면 그것을 우선한다.
5. **`use(promise)`는 새 코드부터.** 기존 fetch effect를 일괄로 바꾸려 들지 마라. Suspense 경계 설계가 같이 따라와야 한다. 도입은 페이지 단위로 점진적으로.
6. **React Compiler는 빌드 옵션부터.** Babel 플러그인 또는 SWC 플러그인 형태로 켜고, 한 모듈씩 메모이제이션 코드를 비워 보며 회귀 테스트로 측정한다.
7. **카나리/실험 API에 대한 의존을 끊는다.** 18 시절 `useEffectEvent` 같은 실험 훅을 쓰고 있었다면, 19 안정 버전 기준으로 다시 위상을 확인한다(2026년 시점 여전히 실험 단계 — 본문 9장 참고).
8. **타입 점검.** `@types/react`/`@types/react-dom`을 19용으로 올리고, ref 타입과 `Children`/`Element` 관련 미세 타입 변경을 한 번 훑는다.

## 무엇은 그대로 두어도 되는가

마지막으로, 이 책 전체에서 익힌 것들 중 *19에서도 그대로*인 것들을 짚자. 이 목록이 길다는 사실이, 우리가 18로 책을 쓴 이유를 가장 잘 변호한다.

- `useState`, `useReducer`, Context API: 모양 그대로.
- 상태 끌어올리기, `key`로 리셋, 정규화, single source of truth, lift-then-drop: 모양 그대로.
- `useEffect`의 동기화 모델, cleanup의 의무, 의존성 정직성: 모양 그대로.
- "You might not need an Effect"의 모든 휴리스틱: 모양 그대로. 오히려 Actions/Server Components가 effect의 정당한 자리를 더 좁힌다.
- Custom Hook 추출 규칙(반복이 보일 때, `use` 접두사), Robin Wieruch가 권한 배열 반환: 모양 그대로.
- `useSyncExternalStore`, `flushSync`, `useImperativeHandle`: 그대로 유효. 사용처도 동일.
- TanStack Query/SWR 같은 서버 캐시 라이브러리의 분리 원칙: *오히려 더 강해진다*. RSC와 함께 쓰면 더 자연스럽다.

요약하자면 19는 우리가 익힌 멘탈 모델 *위에* 더 깔끔한 문법과 더 나은 다리를 얹은 버전이다. 새 단어 몇 개를 더 외우면 된다. 그 단어들이 익숙해질 즈음 우리는 또 한 번, 같은 풍경을 더 빠르게 통과하고 있을 것이다.
