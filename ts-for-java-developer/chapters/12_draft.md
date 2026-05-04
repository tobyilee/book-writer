# 12장. 웹 프론트엔드 — React + TS의 핵심, 그리고 다른 reactivity 모델의 위치

Spring MVC 프로젝트를 수년째 운영해온 개발자가 처음으로 React 코드베이스를 열었을 때의 표정을 상상해보자. Thymeleaf 템플릿 대신 JSX가 있고, `@Controller`와 `@GetMapping` 대신 컴포넌트 함수가 있다. "이 함수가 뷰인가, 컨트롤러인가?" 하는 질문이 자연스럽게 나온다. 둘 다이기도 하고 둘 다 아니기도 하다 — 이 애매함이 React의 설계다.

그리고 TypeScript를 얹으면 또 다른 질문이 생긴다. 이 컴포넌트에 들어오는 `props`의 타입은 어디서 선언하는가? 버튼 클릭 이벤트의 타입은 무엇인가? `useRef`가 반환하는 것은 `null`일 수도 있는데, 그 타입은 어떻게 다루는가? 이런 질문들은 TypeScript를 처음 쓰는 사람이 아니라, **Java/Kotlin에서 온 시니어 개발자**가 React에서 처음 마주치는 질문이다.

12장은 이 질문들에 정면으로 답한다. React가 한국 시장 프론트엔드의 압도적 표준이라는 현실을 반영해, React와 TypeScript가 만나는 지점을 충분한 깊이로 파고든다. Vue·Svelte·Solid는 별도의 절에서 비교 관점으로만 다룬다 — 언제 만나는지, 왜 다른지, 그 정도로.

---

## React + TypeScript의 시작: 컴포넌트를 타입으로 생각하기

React 컴포넌트를 Java 관점에서 가장 가깝게 비유하면 "데이터를 받아서 뷰를 반환하는 순수 함수"에 가깝다. Spring MVC의 `@Controller`가 HTTP 요청을 받아 `ModelAndView`를 반환하듯, React 컴포넌트는 `props`를 받아 JSX를 반환한다. 물론 `useState`와 `useEffect`가 들어오면 부수효과(side effect)가 생기지만, 기본 개념은 그렇다.

TypeScript와 함께 쓸 때 컴포넌트의 핵심은 **`props`의 타입을 명확하게 선언하는 것**이다. 이 선언이 있어야 컴포넌트를 사용하는 쪽에서 어떤 데이터를 넘겨야 하는지 컴파일 타임에 알 수 있다.

### Props 타이핑: 가장 기본적인 자리

```tsx
// 가장 단순한 형태
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

`interface`로 props의 모양을 선언하고, 함수 매개변수에서 구조 분해 할당으로 받는다. `disabled?: boolean`의 `?`는 선택적 필드를 나타내며, 기본값 `= false`를 지정할 수 있다. 이 정도는 어렵지 않다.

그런데 여기서 자주 실수하는 지점이 있다. `type`과 `interface` 중 무엇을 써야 할까? 결론부터 말하면 **props 정의에는 둘 다 쓸 수 있고, 기능 차이는 거의 없다**. 다만 커뮤니티 관례상 컴포넌트 props는 `interface`를, 유니온·교차·조건부 타입이 필요할 때는 `type`을 쓰는 경향이 있다. 팀에서 일관성을 유지하는 편이 낫다.

### `PropsWithChildren`: 자식 요소를 받는 컴포넌트

```tsx
import { type PropsWithChildren } from 'react';

interface CardProps {
  title: string;
  className?: string;
}

// PropsWithChildren<T>는 T & { children?: ReactNode }와 같다
function Card({ title, className, children }: PropsWithChildren<CardProps>) {
  return (
    <div className={className}>
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  );
}
```

`PropsWithChildren<T>`은 `@types/react`가 제공하는 유틸리티 타입이다. `T & { children?: ReactNode }`를 직접 쓰는 것과 동일하지만, 의도를 더 명확하게 전달한다. React 17 이전에는 함수형 컴포넌트의 타입으로 `React.FC<Props>`를 쓰면 `children`이 자동으로 포함됐지만, React 18부터 `React.FC`에서 `children`이 빠졌다. 지금은 `PropsWithChildren`을 명시적으로 쓰거나, `children: ReactNode`를 직접 선언하는 편이 낫다.

> **📚 Java/Kotlin 시선 박스 ① — Spring MVC + Thymeleaf ↔ React 컴포넌트**
>
> Spring MVC에서 컨트롤러는 비즈니스 로직을 처리하고, Thymeleaf 템플릿은 그 결과를 렌더링한다. 두 역할은 분리되어 있다. React에서는 이 두 역할이 **컴포넌트 함수 안에 함께** 있다. `useState`로 상태를 관리하는 것은 컨트롤러가 할 일이고, JSX를 반환하는 것은 뷰가 할 일인데, React에서는 같은 함수 안에 있다.
>
> 이를 "우려 혼합(mixing concerns)"이라고 비판할 수도 있지만, React의 설계 철학은 다르다 — **"관련된 것"은 함께 있어야 한다**. 버튼의 클릭 핸들러는 버튼 렌더링 코드와 함께 있는 것이 맞다는 관점이다. Thymeleaf의 `th:click`과 컨트롤러의 `@PostMapping` 사이의 매핑보다, JSX 안의 `onClick`이 더 직접적이다.
>
> Spring의 `Model` 객체에 데이터를 담아 뷰로 전달하는 것이 `props`에 해당하고, Thymeleaf의 `${변수명}` 표현식이 JSX의 `{변수명}`에 해당한다. 렌더링 결과물로 HTML이 나온다는 점은 동일하다.

### Generic 컴포넌트: 타입 매개변수를 받는 컴포넌트

컴포넌트도 제네릭이 될 수 있다. 리스트를 렌더링하는 컴포넌트를 생각해보자. `string` 리스트, `User` 리스트, `Product` 리스트를 각각 별도 컴포넌트로 만드는 것은 번거롭다. 제네릭을 쓰면 하나로 처리할 수 있다.

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

// TSX 파일에서 제네릭 화살표 함수를 쓸 때 주의
// <T,> 형태의 trailing comma가 필요한 경우가 있다 (JSX 파서와의 충돌 방지)
function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// 사용 예
interface User {
  id: string;
  name: string;
  email: string;
}

function UserList({ users }: { users: User[] }) {
  return (
    <List
      items={users}
      keyExtractor={(user) => user.id}
      renderItem={(user) => <span>{user.name} — {user.email}</span>}
    />
  );
}
```

TypeScript가 `items`의 타입으로부터 `T`를 추론하므로 `<List<User> ...>`처럼 명시적으로 타입을 넣지 않아도 된다. 추론이 작동하지 않는 경우에만 명시한다.

`.tsx` 파일에서 화살표 함수로 제네릭을 쓸 때 `<T>` 대신 `<T,>`나 `<T extends unknown>`을 써야 할 때가 있다. JSX 파서가 `<T>`를 JSX 태그로 오해하기 때문이다. 이것은 처음 보면 난감하다 — 문법 오류처럼 보이지만 의도적인 회피 패턴이다.

---

## `forwardRef`: 가장 많이 얼버무려지는 자리

`forwardRef`는 많은 학습서에서 짧게 넘어가거나 타입을 생략한 채 소개한다. 하지만 실무에서 컴포넌트 라이브러리를 만들거나, 폼 요소에 외부에서 `ref`를 주입해야 할 때 이 함수를 제대로 이해하지 못하면 꽤 난감한 상황에 처한다. 한 번 정확히 풀어보자.

### `ref`가 왜 필요한가

React의 선언형 패러다임에서는 DOM에 직접 접근하는 것을 가급적 피한다. 하지만 불가피하게 필요할 때가 있다 — 포커스 관리, 텍스트 선택, 애니메이션 트리거, 외부 라이브러리 연동 같은 경우다. 이때 `useRef`를 사용한다.

```tsx
import { useRef, useEffect } from 'react';

function SearchBox() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // 마운트 시 자동 포커스
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} type="search" placeholder="검색어 입력" />;
}
```

`useRef<HTMLInputElement>(null)`에서 타입 매개변수 `HTMLInputElement`는 중요하다. `inputRef.current`가 `HTMLInputElement | null` 타입임을 TypeScript에게 알려주는 것이다. `null`로 초기화하는 이유는 컴포넌트가 마운트되기 전에는 DOM 요소가 아직 존재하지 않기 때문이다.

### `forwardRef`의 타입 완전 해부

`forwardRef`가 필요한 상황은 부모 컴포넌트에서 자식 컴포넌트 내부의 DOM 요소에 직접 `ref`를 연결하고 싶을 때다. 예를 들어 커스텀 `Input` 컴포넌트를 만들었는데, 이를 사용하는 쪽에서 `inputRef`로 포커스를 제어하고 싶다면 어떻게 해야 할까?

```tsx
import { forwardRef, useImperativeHandle, useRef } from 'react';

// 1단계: props 타입과 ref 타입을 별도로 정의
interface InputProps {
  label: string;
  placeholder?: string;
  className?: string;
}

// forwardRef<RefType, PropsType>
// 제네릭 순서 주의: ref 타입이 먼저, props 타입이 나중
const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, placeholder, className }, ref) {
    return (
      <div>
        <label>{label}</label>
        <input
          ref={ref}
          placeholder={placeholder}
          className={className}
        />
      </div>
    );
  }
);

// displayName은 React DevTools에서 컴포넌트 이름이 표시되도록 돕는다
// forwardRef로 감싸면 이름이 사라지는 경우가 있어 명시하는 편이 낫다
Input.displayName = 'Input';

// 사용 예
function LoginForm() {
  const usernameRef = useRef<HTMLInputElement>(null);

  const focusUsername = () => {
    usernameRef.current?.focus();
  };

  return (
    <form>
      <Input ref={usernameRef} label="사용자명" placeholder="아이디 입력" />
      <button type="button" onClick={focusUsername}>
        아이디 필드 포커스
      </button>
    </form>
  );
}
```

`forwardRef<RefType, PropsType>`에서 제네릭 순서가 직관적이지 않게 느껴질 수 있다. ref 타입(`HTMLInputElement`)이 props 타입(`InputProps`)보다 앞에 온다. 이 순서를 반대로 쓰면 타입 오류가 난다 — 처음 접하면 찜찜한 자리다.

### `useImperativeHandle`: ref를 통해 명령형 인터페이스 노출하기

`forwardRef`와 짝을 이루는 `useImperativeHandle`은 부모에게 노출할 메서드를 선택적으로 제한할 때 쓴다. DOM 요소 전체를 그대로 노출하는 것이 아니라, 의도적으로 정의한 인터페이스만 내보내는 방식이다.

```tsx
interface VideoPlayerHandle {
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
}

interface VideoPlayerProps {
  src: string;
  autoPlay?: boolean;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, VideoPlayerProps>(
  function VideoPlayer({ src, autoPlay }, ref) {
    const videoRef = useRef<HTMLVideoElement>(null);

    useImperativeHandle(ref, () => ({
      play() {
        videoRef.current?.play();
      },
      pause() {
        videoRef.current?.pause();
      },
      seek(time: number) {
        if (videoRef.current) {
          videoRef.current.currentTime = time;
        }
      },
    }));

    return <video ref={videoRef} src={src} autoPlay={autoPlay} />;
  }
);

// 사용 예
function VideoController() {
  const playerRef = useRef<VideoPlayerHandle>(null);

  return (
    <div>
      <VideoPlayer ref={playerRef} src="/video/demo.mp4" />
      <button onClick={() => playerRef.current?.play()}>재생</button>
      <button onClick={() => playerRef.current?.pause()}>일시정지</button>
    </div>
  );
}
```

`useRef<VideoPlayerHandle>(null)`에서 타입이 `VideoPlayerHandle`이다. `HTMLVideoElement` 전체가 아니라 우리가 정의한 인터페이스만 외부에 노출된다. 부모는 `play()`, `pause()`, `seek()`만 호출할 수 있고, `videoRef.current?.volume = 0` 같은 다른 DOM 조작은 할 수 없다. 캡슐화가 강제된다. Java 개발자라면 이 패턴이 낯설지 않을 것이다 — 인터페이스를 통한 추상화다.

---

## 이벤트 핸들러의 타입: `React.MouseEvent`와 `ChangeEvent`의 결

이벤트 핸들러를 타이핑할 때 처음에는 그냥 `() => void`로 쓰거나 `any`로 도망치고 싶은 유혹이 생긴다. 하지만 이벤트 객체에 접근해야 할 때 타입이 없으면 금방 곤란해진다.

### 기본 이벤트 타입

```tsx
// 클릭 이벤트
function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
  // event.currentTarget은 HTMLButtonElement
  console.log(event.currentTarget.id);
  event.preventDefault();
}

// 인라인에서는 타입 추론이 자동으로
function ClickButton() {
  return (
    <button
      onClick={(e) => {
        // e: React.MouseEvent<HTMLButtonElement, MouseEvent>
        // 자동 추론되므로 타입 명시 불필요
        console.log(e.clientX, e.clientY);
      }}
    >
      클릭
    </button>
  );
}
```

인라인 이벤트 핸들러에서는 TypeScript가 대상 요소의 타입을 자동으로 추론한다. `<button onClick={(e) => ...}>`에서 `e`의 타입은 자동으로 `React.MouseEvent<HTMLButtonElement, MouseEvent>`가 된다. 별도의 핸들러 함수를 만들 때만 타입을 명시해야 한다.

### `ChangeEvent`: 폼 요소의 핵심

```tsx
// input 값이 바뀔 때
function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
  const value = event.target.value; // string
  console.log(value);
}

// textarea
function handleTextarea(event: React.ChangeEvent<HTMLTextAreaElement>) {
  const value = event.target.value;
}

// select
function handleSelect(event: React.ChangeEvent<HTMLSelectElement>) {
  const value = event.target.value;
}

// 실제 컴포넌트에서의 사용
function SearchForm() {
  const [query, setQuery] = React.useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      // e는 React.ChangeEvent<HTMLInputElement>로 자동 추론
    />
  );
}
```

`event.target`과 `event.currentTarget`의 차이를 기억해두자. `currentTarget`은 이벤트 핸들러가 붙어 있는 요소이고, `target`은 이벤트가 실제로 발생한 요소다. 이벤트 버블링이 있을 때 둘이 다를 수 있다. 폼 입력값을 읽을 때는 대개 `event.target.value`를 쓴다.

### 이벤트 핸들러 props의 타입

부모 컴포넌트에서 자식 컴포넌트로 이벤트 핸들러를 prop으로 전달할 때의 타입 선언이다.

```tsx
interface SearchInputProps {
  value: string;
  // React.ChangeEventHandler<HTMLInputElement>는
  // (event: React.ChangeEvent<HTMLInputElement>) => void 와 동일
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  onSubmit: (query: string) => void;
  onKeyDown?: React.KeyboardEventHandler<HTMLInputElement>;
}

function SearchInput({ value, onChange, onSubmit, onKeyDown }: SearchInputProps) {
  const handleKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
    if (e.key === 'Enter') {
      onSubmit(value);
    }
    onKeyDown?.(e);
  };

  return (
    <input
      value={value}
      onChange={onChange}
      onKeyDown={handleKeyDown}
    />
  );
}
```

`React.ChangeEventHandler<T>`는 `(event: React.ChangeEvent<T>) => void`의 별칭이다. 타입 이름이 길어지는 것을 피하고 싶을 때 쓴다. `React.MouseEventHandler`, `React.KeyboardEventHandler` 등도 같은 방식으로 정의되어 있다.

---

## `useState`와 `useReducer`의 타입: 추론과 명시의 균형

### `useState`의 타입 추론

```tsx
// 타입 추론이 작동하는 경우 — 명시할 필요 없음
const [count, setCount] = useState(0);          // number
const [name, setName] = useState('');            // string
const [isLoading, setIsLoading] = useState(false); // boolean

// 타입 추론이 부족해 명시가 필요한 경우
const [user, setUser] = useState<User | null>(null);
// null로 초기화하면 타입이 null로 추론되어 User를 할당할 수 없게 된다
// null로 시작하지만 나중에 User가 들어올 것이라는 의도를 명시해야 한다

// 배열
const [items, setItems] = useState<string[]>([]);
// []만 쓰면 never[]로 추론될 수 있다
```

`useState<User | null>(null)` 패턴은 매우 자주 쓰인다. API에서 데이터를 불러오기 전에는 `null`, 불러온 후에는 `User` 타입이 되는 상황이다. 초기값으로 `null`을 넣으면 TypeScript는 타입을 `null`로 추론하고, 나중에 `User` 객체를 `setUser`로 넣으려 하면 타입 오류가 난다. 제네릭으로 타입을 명시해야 한다.

### 복잡한 상태는 `useReducer`

상태가 여러 필드로 구성되어 있고 업데이트 로직이 복잡할 때는 `useReducer`가 낫다. 이 패턴은 Java의 상태 기계(state machine)나 Redux 스타일을 알고 있다면 친숙하다.

```tsx
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
  isLoading: boolean;
}

// discriminated union으로 액션 타입 정의
type CartAction =
  | { type: 'ADD_ITEM'; payload: Omit<CartItem, 'quantity'> }
  | { type: 'REMOVE_ITEM'; payload: { id: string } }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'CLEAR_CART' };

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existing = state.items.find(item => item.id === action.payload.id);
      if (existing) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        };
      }
      const newItem: CartItem = { ...action.payload, quantity: 1 };
      return {
        ...state,
        items: [...state.items, newItem],
        total: state.total + action.payload.price,
      };
    }
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload.id),
      };
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'CLEAR_CART':
      return { items: [], total: 0, isLoading: false };
    default:
      // TypeScript exhaustiveness check
      // CartAction에 새로운 type을 추가하면 여기서 컴파일 오류
      const _exhaustive: never = action;
      return state;
  }
}

function Cart() {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    total: 0,
    isLoading: false,
  });

  return (
    <div>
      {state.items.map(item => (
        <div key={item.id}>
          {item.name} × {item.quantity}
          <button onClick={() => dispatch({ type: 'REMOVE_ITEM', payload: { id: item.id } })}>
            제거
          </button>
        </div>
      ))}
    </div>
  );
}
```

`CartAction`을 discriminated union으로 정의하면 `switch`의 `default` 브랜치에서 `never` 타입 체크가 작동한다. 나중에 `CartAction`에 새로운 액션 타입을 추가했는데 `cartReducer`에서 처리하지 않으면 컴파일 오류가 발생한다. 5장에서 다룬 exhaustiveness check가 여기서 살아난다. 이 패턴은 Kotlin의 `sealed class` + `when`과 정확히 같은 역할을 한다.

---

## `useEffect`의 cleanup과 dependency 타입 안전

`useEffect`는 React에서 부수효과(데이터 패치, 이벤트 리스너, 타이머)를 다루는 hook이다. TypeScript와 함께 쓸 때 특히 주의해야 하는 지점 몇 가지를 살펴보자.

### cleanup 함수의 타입

```tsx
import { useEffect, useState } from 'react';

function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    // cleanup: 반환값이 () => void이어야 한다
    return () => {
      clearInterval(id);
    };
  }, []); // 빈 배열 = 마운트/언마운트 시만 실행

  return <div>{count}초 경과</div>;
}
```

`useEffect`의 콜백 함수는 `() => void | (() => void)`를 반환해야 한다. cleanup 함수를 반환하거나, 아무것도 반환하지 않거나 둘 중 하나다. `async` 함수를 직접 `useEffect`에 전달하면 안 된다 — `async` 함수는 항상 `Promise`를 반환하는데, `useEffect`는 `Promise`를 cleanup 함수로 처리하지 못하기 때문이다.

```tsx
// 잘못된 패턴 — TypeScript도 경고한다
useEffect(async () => {
  const data = await fetchData();
  setData(data);
}, []);

// 올바른 패턴
useEffect(() => {
  let cancelled = false;

  async function loadData() {
    const data = await fetchData();
    if (!cancelled) {
      setData(data);
    }
  }

  loadData();

  return () => {
    cancelled = true;
  };
}, []);
```

두 번째 패턴에서 `cancelled` 플래그를 쓰는 이유는 컴포넌트가 언마운트된 후 비동기 작업이 완료되어 상태를 업데이트하려 할 때를 막기 위해서다. AbortController를 쓸 수도 있다 — 취소 가능한 fetch 요청을 만들 때 더 깔끔하다.

```tsx
useEffect(() => {
  const controller = new AbortController();

  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(data => setData(data))
    .catch(err => {
      if (err.name !== 'AbortError') {
        setError(err);
      }
    });

  return () => controller.abort();
}, []);
```

### dependency 배열의 함정

`useEffect`의 두 번째 인수인 dependency 배열에 어떤 값을 넣어야 하는지는 TypeScript가 직접 강제하지는 않는다 — `eslint-plugin-react-hooks`의 `react-hooks/exhaustive-deps` 규칙이 담당한다. 하지만 타입과 무관하게, dependency를 잘못 관리하면 찜찜한 버그가 생긴다.

```tsx
// 함수를 dependency에 넣을 때의 문제
function DataFetcher({ userId }: { userId: string }) {
  const [data, setData] = useState<Data | null>(null);

  // 이 함수가 렌더링마다 새로 생성되면 useEffect가 무한 루프에 빠진다
  async function fetchUserData() {
    const result = await fetchUser(userId);
    setData(result);
  }

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]); // 매 렌더링마다 새 함수 참조 → 무한 루프

  return <div>{data?.name}</div>;
}

// 해결: useCallback으로 함수를 메모이제이션
function DataFetcherFixed({ userId }: { userId: string }) {
  const [data, setData] = useState<Data | null>(null);

  const fetchUserData = useCallback(async () => {
    const result = await fetchUser(userId);
    setData(result);
  }, [userId]); // userId가 바뀔 때만 새 함수 참조

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  return <div>{data?.name}</div>;
}
```

`useCallback`의 타입은 전달하는 함수의 타입을 그대로 추론한다. 명시적으로 넣을 필요는 없지만, 복잡한 경우에는 반환 타입을 명시하는 편이 낫다.

---

## 커스텀 Hook: 로직의 타입화된 캡슐

커스텀 hook은 React의 강력한 추상화 메커니즘이다. 여러 컴포넌트에서 공유되는 상태 로직을 별도 함수로 추출할 수 있다. Java에서 서비스 클래스나 리포지토리로 비즈니스 로직을 분리하는 것과 비슷한 목적이다 — 하지만 형태는 전혀 다르다.

### 기본 커스텀 Hook

```tsx
// useLocalStorage: localStorage와 동기화되는 상태
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.error(`localStorage 읽기 실패 [${key}]:`, error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`localStorage 쓰기 실패 [${key}]:`, error);
    }
  };

  return [storedValue, setValue] as const;
  // as const가 없으면 반환 타입이 (T | ...)[]로 추론되어
  // setStoredValue를 함수로 쓸 수 없게 된다
}

// 사용
function Settings() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
  const [language, setLanguage] = useLocalStorage('language', 'ko');

  return (
    <div>
      <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
        테마 전환 (현재: {theme})
      </button>
    </div>
  );
}
```

`as const`의 역할이 여기서 중요하다. `[storedValue, setValue]`를 반환하면 TypeScript는 이를 `Array<T | ((value: T | ((val: T) => T)) => void)>`로 추론한다. 배열의 첫 번째 요소가 상태 값인지 세터인지 구분하지 못한다. `as const`를 붙이면 `readonly [T, (value: ...) => void]` 튜플로 추론되어 각 위치의 타입이 고정된다.

### Generic Hook: 타입이 흐르는 추상화

```tsx
// useAsync: 비동기 함수의 상태를 관리하는 hook
interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

function useAsync<T>(
  asyncFn: () => Promise<T>,
  deps: React.DependencyList = []
) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    isLoading: true,
  });

  useEffect(() => {
    let cancelled = false;

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    asyncFn()
      .then(data => {
        if (!cancelled) {
          setState({ data, error: null, isLoading: false });
        }
      })
      .catch(error => {
        if (!cancelled) {
          setState({ data: null, error, isLoading: false });
        }
      });

    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}

// 사용 예
interface Post {
  id: number;
  title: string;
  body: string;
}

function PostDetail({ postId }: { postId: number }) {
  const { data: post, isLoading, error } = useAsync<Post>(
    () => fetch(`/api/posts/${postId}`).then(r => r.json()),
    [postId]
  );

  if (isLoading) return <div>로딩 중...</div>;
  if (error) return <div>오류: {error.message}</div>;
  if (!post) return null;

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
    </article>
  );
}
```

`useAsync<Post>(...)` — 제네릭 타입 매개변수를 명시하면 `state.data`의 타입이 `Post | null`로 고정된다. 물론 `asyncFn`의 반환 타입으로부터 추론되므로 명시하지 않아도 되는 경우가 많다.

---

## Suspense와 Server Components의 타입 측면

React 18에서 Suspense가 데이터 패칭에 정식으로 활용되기 시작했고, React 19에서는 Server Components가 안정화됐다. 이 두 기능의 깊은 런타임 동작은 13장 풀스택 절에서 다루지만, **타입 측면**에서 알아둬야 할 것이 있다.

### Suspense와 `lazy`의 타입

```tsx
import { Suspense, lazy } from 'react';

// lazy는 default export인 컴포넌트를 반환하는 Promise를 받는다
const HeavyChart = lazy(() => import('./HeavyChart'));
// 타입: React.LazyExoticComponent<typeof HeavyChart>

function Dashboard() {
  return (
    <Suspense fallback={<div>차트 로딩 중...</div>}>
      <HeavyChart data={[1, 2, 3]} />
    </Suspense>
  );
}
```

`lazy`로 불러오는 모듈은 반드시 `default export`여야 한다. named export만 있는 컴포넌트는 `lazy`로 직접 불러올 수 없다 — 래핑이 필요하다.

### Server Component의 타입 규칙 (Next.js App Router 기준)

Server Component는 `async` 컴포넌트가 될 수 있다. 이것이 Client Component와의 가장 큰 타입 차이다.

```tsx
// Server Component — async 함수로 정의 가능
// app/users/page.tsx
async function UsersPage() {
  // 서버에서 직접 데이터 패치 (useState, useEffect 없음)
  const users = await fetchUsers();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// Client Component — 'use client' 지시자 필요, async 불가
'use client';
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

Server Component에 props를 전달할 때, **함수는 전달할 수 없다**. 서버와 클라이언트 사이의 경계에서 함수는 직렬화할 수 없기 때문이다. TypeScript가 이를 컴파일 타임에 완전히 잡아주지는 않지만, Next.js의 타입 체크 레이어가 일부 잡아준다. 이 부분의 타입 경험은 아직 성숙 중이다 — RSC 깊은 내용은 13장에서 다룬다.

---

## 폼과 검증: React Hook Form + zod로 Bean Validation 재현하기

폼 처리는 프론트엔드의 가장 번거로운 영역 중 하나다. 입력값 관리, 유효성 검증, 에러 표시, 제출 처리를 각각 따로 구현하면 코드가 금방 복잡해진다. Spring의 Bean Validation + `@Valid`가 이 번거로움을 많이 줄여줬던 것처럼, React 생태계에는 **React Hook Form + zod**라는 조합이 있다.

> **📚 Java/Kotlin 시선 박스 ② — Bean Validation + DTO ↔ zod schema**
>
> Spring에서 폼 데이터를 다룰 때는 DTO 클래스를 만들고 Bean Validation 어노테이션을 붙인다.
>
> ```java
> public class SignUpRequest {
>     @NotBlank(message = "이메일은 필수입니다")
>     @Email(message = "올바른 이메일 형식이어야 합니다")
>     private String email;
>
>     @Size(min = 8, message = "비밀번호는 8자 이상이어야 합니다")
>     private String password;
>
>     @NotBlank(message = "이름은 필수입니다")
>     private String name;
> }
> ```
>
> 컨트롤러에서 `@Valid`를 붙이면 Spring이 검증을 실행하고, 실패 시 `BindingResult`에 오류를 담는다.
>
> zod + React Hook Form은 같은 역할을 한다. zod schema가 DTO + Bean Validation 어노테이션의 역할이고, `resolver`가 `@Valid`의 역할이다. 핵심 차이는 **타입이 schema에서 자동 파생된다는 것** — `z.infer<typeof schema>`로 TypeScript 타입을 별도로 선언할 필요 없이 schema가 단일 진실 원천이 된다.

### React Hook Form의 기본 타입 패턴

```tsx
import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1단계: zod schema 정의 — 이것이 단일 진실 원천
const signUpSchema = z.object({
  email: z
    .string()
    .min(1, '이메일은 필수입니다')
    .email('올바른 이메일 형식이어야 합니다'),
  password: z
    .string()
    .min(8, '비밀번호는 8자 이상이어야 합니다')
    .regex(/[A-Z]/, '대문자를 포함해야 합니다')
    .regex(/[0-9]/, '숫자를 포함해야 합니다'),
  name: z
    .string()
    .min(1, '이름은 필수입니다')
    .max(50, '이름은 50자 이하여야 합니다'),
  agreeToTerms: z.boolean().refine(val => val === true, {
    message: '이용약관에 동의해야 합니다',
  }),
});

// 2단계: schema에서 TypeScript 타입 파생
// 별도의 interface를 선언할 필요 없다 — schema가 단일 진실 원천
type SignUpFormValues = z.infer<typeof signUpSchema>;
// {
//   email: string;
//   password: string;
//   name: string;
//   agreeToTerms: boolean;
// }

// 3단계: useForm에 타입 연결
function SignUpForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<SignUpFormValues>({
    resolver: zodResolver(signUpSchema),
    defaultValues: {
      email: '',
      password: '',
      name: '',
      agreeToTerms: false,
    },
  });

  // SubmitHandler<T>는 (data: T) => void | Promise<void>
  const onSubmit: SubmitHandler<SignUpFormValues> = async (data) => {
    // data는 SignUpFormValues 타입 — 검증이 통과한 데이터
    // zod가 런타임에 검증하고 변환했으므로 타입이 보장된다
    try {
      await registerUser(data);
      reset();
    } catch (error) {
      console.error('회원가입 실패:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">이메일</label>
        <input
          id="email"
          type="email"
          {...register('email')}
          // register는 name, ref, onChange, onBlur를 spread
          // 'email' 문자열은 SignUpFormValues의 key만 허용 — 오타를 컴파일 타임에 잡는다
        />
        {errors.email && (
          <span role="alert">{errors.email.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="password">비밀번호</label>
        <input
          id="password"
          type="password"
          {...register('password')}
        />
        {errors.password && (
          <span role="alert">{errors.password.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="name">이름</label>
        <input
          id="name"
          {...register('name')}
        />
        {errors.name && (
          <span role="alert">{errors.name.message}</span>
        )}
      </div>

      <div>
        <input
          id="agreeToTerms"
          type="checkbox"
          {...register('agreeToTerms')}
        />
        <label htmlFor="agreeToTerms">이용약관에 동의합니다</label>
        {errors.agreeToTerms && (
          <span role="alert">{errors.agreeToTerms.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '가입 중...' : '회원가입'}
      </button>
    </form>
  );
}
```

`register('email')`에서 `'email'` 문자열은 `SignUpFormValues`의 키로 제한된다. `register('emali')`처럼 오타를 치면 컴파일 오류가 발생한다. 5장에서 다룬 `z.infer`가 여기서 실용적으로 작동하는 것이다 — schema 하나가 런타임 검증과 컴파일 타임 타입 안전을 동시에 제공한다.

### 중첩 객체와 배열을 포함하는 복잡한 폼

```tsx
const orderSchema = z.object({
  customer: z.object({
    name: z.string().min(1, '고객명은 필수입니다'),
    email: z.string().email('이메일 형식이 올바르지 않습니다'),
    phone: z.string().regex(/^010-\d{4}-\d{4}$/, '010-XXXX-XXXX 형식으로 입력하세요'),
  }),
  items: z.array(
    z.object({
      productId: z.string().min(1),
      quantity: z.number().int().positive('수량은 1 이상이어야 합니다'),
    })
  ).min(1, '최소 1개 이상의 상품을 선택해야 합니다'),
  deliveryAddress: z.string().min(10, '배송지 주소를 상세히 입력해주세요'),
  specialRequest: z.string().optional(),
});

type OrderFormValues = z.infer<typeof orderSchema>;

function OrderForm() {
  const { register, control, handleSubmit, formState: { errors } } = useForm<OrderFormValues>({
    resolver: zodResolver(orderSchema),
  });

  // 배열 필드는 useFieldArray hook으로 관리
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  });

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <input {...register('customer.name')} placeholder="고객명" />
      {/* 중첩 경로도 점 표기법으로 접근 — 타입 안전 */}
      {errors.customer?.name && <span>{errors.customer.name.message}</span>}

      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
            type="number"
          />
          <button type="button" onClick={() => remove(index)}>제거</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ productId: '', quantity: 1 })}>
        상품 추가
      </button>
    </form>
  );
}
```

`register('customer.name')`의 점 표기법 경로도 타입 체크된다. `OrderFormValues`의 구조에 없는 경로를 쓰면 컴파일 오류가 난다. 폼 코드를 리팩토링할 때 schema를 바꾸면 모든 `register` 호출 오류가 한꺼번에 표시된다 — 빠진 곳이 없는지 걱정할 필요가 없다.

---

## 전역 상태: Zustand·Jotai·Redux Toolkit의 타입 모델

전역 상태 관리는 React 생태계에서 논쟁이 많은 영역이다. `useState`와 Context API만으로 충분한 경우도 있고, 앱이 커지면 전용 라이브러리가 필요해진다. 세 가지 주요 선택지를 타입 측면에서 비교해보자.

### Zustand: 가장 단순한 타입 모델

```tsx
import { create } from 'zustand';

// 스토어 타입을 인터페이스로 정의 — 상태와 액션을 함께
interface BearStore {
  bears: number;
  fish: number;
  increaseBears: () => void;
  eatFish: () => void;
  reset: () => void;
}

const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  fish: 10,
  increaseBears: () => set((state) => ({ bears: state.bears + 1 })),
  eatFish: () => set((state) => ({ fish: state.fish - 1 })),
  reset: () => set({ bears: 0, fish: 10 }),
}));

// 컴포넌트에서 선택자(selector)로 구독
function BearCounter() {
  // 필요한 상태만 구독 — 리렌더링 최소화
  const bears = useBearStore((state) => state.bears);
  const increaseBears = useBearStore((state) => state.increaseBears);

  return (
    <div>
      <span>곰 {bears}마리</span>
      <button onClick={increaseBears}>곰 추가</button>
    </div>
  );
}
```

Zustand의 타입 모델은 단순하다. `create<StoreType>()`에 타입을 한 번 넣으면 이후 `set`, `get` 콜백에서 모두 추론된다. Redux의 action type, reducer, selector를 각각 따로 정의해야 하는 복잡함이 없다.

### Jotai: 원자(atom) 기반의 타입 추론

```tsx
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// 기본 atom — 타입은 초기값에서 추론
const countAtom = atom(0); // Atom<number>
const textAtom = atom(''); // Atom<string>

// 파생 atom (읽기 전용)
const doubledCountAtom = atom(
  (get) => get(countAtom) * 2
); // Atom<number>

// 읽기/쓰기 파생 atom
const normalizedTextAtom = atom(
  (get) => get(textAtom).trim().toLowerCase(),
  (_get, set, newValue: string) => set(textAtom, newValue)
);

// 비동기 atom
const userAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  const response = await fetch(`/api/users/${userId}`);
  return response.json() as Promise<User>;
}); // Atom<Promise<User>>

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const doubled = useAtomValue(doubledCountAtom);
  const setCountOnly = useSetAtom(countAtom); // setter만 구독 — 리렌더링 없음

  return (
    <div>
      <span>{count} (두 배: {doubled})</span>
      <button onClick={() => setCount(c => c + 1)}>증가</button>
    </div>
  );
}
```

Jotai는 React의 `useState`와 비슷한 API를 유지하면서 전역으로 확장한다. 타입 추론이 자연스럽고, Context의 Provider 없이도 전역 공유가 된다.

### Redux Toolkit: 가장 정형화된 타입 패턴

```tsx
import { createSlice, type PayloadAction, configureStore } from '@reduxjs/toolkit';
import { useDispatch, useSelector, type TypedUseSelectorHook } from 'react-redux';

interface UserState {
  currentUser: User | null;
  isAuthenticated: boolean;
  preferences: {
    theme: 'light' | 'dark';
    language: 'ko' | 'en';
  };
}

const initialState: UserState = {
  currentUser: null,
  isAuthenticated: false,
  preferences: {
    theme: 'light',
    language: 'ko',
  },
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<User>) {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
    },
    logout(state) {
      state.currentUser = null;
      state.isAuthenticated = false;
    },
    setTheme(state, action: PayloadAction<'light' | 'dark'>) {
      state.preferences.theme = action.payload;
    },
  },
});

const store = configureStore({
  reducer: {
    user: userSlice.reducer,
  },
});

// 타입 안전한 dispatch와 selector hook 생성 — 재사용을 위해 별도 파일로
type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

const useAppDispatch = () => useDispatch<AppDispatch>();
const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// 컴포넌트에서 사용
function UserProfile() {
  const dispatch = useAppDispatch();
  const { currentUser, isAuthenticated } = useAppSelector(state => state.user);

  if (!isAuthenticated || !currentUser) return null;

  return (
    <div>
      <span>{currentUser.name}</span>
      <button onClick={() => dispatch(userSlice.actions.logout())}>
        로그아웃
      </button>
    </div>
  );
}
```

| | Zustand | Jotai | Redux Toolkit |
|---|---|---|---|
| **보일러플레이트** | 적음 | 매우 적음 | 많음 |
| **타입 복잡도** | 낮음 | 낮음 | 중간 |
| **DevTools** | 있음 | 있음 | 강력함 |
| **적합한 규모** | 소~중 | 소~대 | 중~대 |
| **Java 비유** | 서비스 싱글톤 | Context + Provider | Spring ApplicationContext + Bean |
| **한국 현장** | 신규 스타트업 선호 | 실험적 사용 | 기존 코드베이스 많음 |

작은 앱에는 Zustand, Context API도 충분하다. Redux Toolkit은 대규모 팀에서 일관된 패턴이 필요할 때 가치를 발휘한다. "어떤 것이 최선"이 아니라 팀과 규모에 맞는 선택을 하는 편이 낫다.

---

## 컴포넌트 라이브러리: 외부 props 타입과 조합 패턴

직접 UI 컴포넌트를 모두 만들 필요는 없다. Radix UI, shadcn/ui, Mantine, Chakra UI 같은 라이브러리가 접근성(accessibility)과 상호작용을 미리 구현해둔 컴포넌트를 제공한다.

### 외부 컴포넌트 props 확장

```tsx
import { type ButtonHTMLAttributes } from 'react';

// Radix UI 버튼의 props를 확장하는 패턴
// 또는 표준 HTML 요소의 props를 확장할 때
interface AppButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
}

function AppButton({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  children,
  disabled,
  className,
  ...htmlProps  // 나머지 HTML 버튼 속성들
}: AppButtonProps) {
  const classes = buildClasses(variant, size, className);

  return (
    <button
      {...htmlProps}
      disabled={disabled || isLoading}
      className={classes}
    >
      {isLoading && <Spinner />}
      {leftIcon && <span className="icon">{leftIcon}</span>}
      {children}
    </button>
  );
}
```

`ButtonHTMLAttributes<HTMLButtonElement>`를 `extends`하면 `onClick`, `type`, `form`, `aria-*` 등 표준 버튼 속성을 모두 받을 수 있다. 컴포넌트 API를 추가하면서 HTML 요소의 속성을 모두 지원하고 싶을 때 자주 쓰는 패턴이다.

### ComponentPropsWithoutRef: 라이브러리 컴포넌트 props 재사용

```tsx
import { type ComponentPropsWithoutRef } from 'react';

// 기존 컴포넌트의 props를 가져와서 일부만 덮어쓰기
type InputWithLabelProps = ComponentPropsWithoutRef<'input'> & {
  label: string;
  error?: string;
};

// shadcn/ui 컴포넌트 props 확장
import { Button } from '@/components/ui/button';
type ExtendedButtonProps = ComponentPropsWithoutRef<typeof Button> & {
  trackingId: string;
};
```

`ComponentPropsWithoutRef<'input'>`은 `InputHTMLAttributes<HTMLInputElement>`와 비슷하지만, 더 일반적인 패턴이다. `typeof Button`처럼 컴포넌트 자체를 타입 인수로 넣으면 해당 컴포넌트의 props 타입을 가져올 수 있다.

### CSS 타이핑: 짧게

Tailwind CSS를 쓸 때는 대부분 문자열 클래스 이름을 사용하므로 별도의 타입 선언이 크게 필요하지 않다. `clsx`나 `cn` (shadcn/ui 관례) 함수로 조건부 클래스를 조합한다. CSS-in-JS(Emotion, styled-components)를 쓸 때는 `CSSObject` 타입이 prop의 타입 안전을 제공한다. 디자인 토큰을 TypeScript로 정의하면 색상·간격·폰트 크기가 타입으로 관리된다.

---

## Vue·Svelte·Solid의 자리: 비교 관점에서

React가 한국 시장에서 압도적이라는 것은 사실이지만, 다른 프레임워크를 전혀 모르고 지내기는 어렵다. 레거시 코드베이스에서, 또는 특정 팀의 선택으로 이미 다른 프레임워크를 쓰고 있을 수 있다.

> **🚧 함정 박스 — reactivity 모델은 프레임워크마다 다르다**
>
> React에서 이직한 개발자가 Vue 코드베이스에 처음 들어갔을 때 가장 먼저 하는 실수는 React의 멘탈 모델을 그대로 가져오는 것이다. "상태가 바뀌면 컴포넌트 함수 전체가 다시 실행된다" — 이것이 React의 모델이다. Vue, Svelte, Solid는 이 모델이 전혀 다르다. 프레임워크를 바꿀 때 가장 먼저 revisit해야 하는 것이 바로 이 reactivity 모델이다.
>
> 반대 방향도 마찬가지다. Vue·Svelte에서 React로 오면 `ref`, `reactive`, `$:`가 없어서 불편하다. 그 불편함은 React가 덜 발전해서가 아니라, 설계 철학이 다르기 때문이다.

### Vue 3: Proxy 기반 reactivity

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface User {
  id: number
  name: string
  email: string
}

// ref: 원시값의 reactive 래퍼
const count = ref(0) // Ref<number>
const user = ref<User | null>(null) // Ref<User | null>

// computed: 파생 값 (의존성 자동 추적)
const displayName = computed(() => user.value?.name ?? '익명')

// watch: 값 변화에 반응
watch(count, (newVal, oldVal) => {
  console.log(`${oldVal} → ${newVal}`)
})

// .value로 접근 — React의 직접 접근과 다른 자리
count.value++
</script>

<template>
  <div>
    <p>{{ displayName }}</p>
    <p>{{ count }}</p>
    <button @click="count++">증가</button>
  </div>
</template>
```

Vue 3의 Composition API는 React Hooks와 표면적으로 비슷해 보이지만 동작 방식이 다르다. Vue는 JavaScript Proxy를 사용해 객체 접근을 가로채고, 값이 바뀔 때 구독된 컴포넌트만 업데이트한다. React처럼 컴포넌트 함수 전체를 다시 실행하지 않는다. `ref`의 `.value`로만 접근해야 하는 것이 React 개발자에게 처음에는 어색하다.

TypeScript 지원은 Vue 3 + `<script setup lang="ts">`로 잘 통합된다. `defineProps<T>()`, `defineEmits<T>()` 같은 컴파일러 매크로가 타입 안전한 props·events를 제공한다.

### Svelte 5: 컴파일 타임 reactivity (runes)

```svelte
<script lang="ts">
  // Svelte 5의 runes — 컴파일러가 처리한다
  let count = $state(0)        // 상태
  let doubled = $derived(count * 2)  // 파생 값

  // $effect는 useEffect와 비슷하지만 의존성 배열이 없다
  // Svelte 컴파일러가 어떤 상태를 읽는지 추적한다
  $effect(() => {
    console.log('count 변경:', count)
  })

  interface User {
    id: number
    name: string
  }

  let users: User[] = $state([])

  async function loadUsers() {
    const res = await fetch('/api/users')
    users = await res.json()
  }
</script>

<p>{count} (두 배: {doubled})</p>
<button onclick={() => count++}>증가</button>
```

Svelte의 가장 큰 차이는 **컴파일러가 reactivity를 처리한다**는 점이다. React처럼 런타임 라이브러리(`react`, `react-dom`)를 배포 번들에 포함할 필요가 없다. Svelte 컴파일러가 `$state`, `$derived`, `$effect` rune을 실제로 동작하는 JavaScript로 변환한다. 번들 크기가 작고 성능이 좋은 이유다.

TypeScript는 `lang="ts"` 하나로 지원된다. Svelte 5는 runes를 TypeScript와 함께 쓸 때 자연스럽게 타입이 추론된다.

### SolidJS: 가상 DOM 없는 signal

```tsx
import { createSignal, createEffect, createMemo, For } from 'solid-js'

interface Item {
  id: number
  text: string
}

function Counter() {
  // signal: [getter, setter] 쌍
  const [count, setCount] = createSignal(0)
  const doubled = createMemo(() => count() * 2)  // 파생 signal

  createEffect(() => {
    // count()를 읽으면 이 effect가 count에 구독됨
    console.log('count:', count())
  })

  return (
    <div>
      <p>{count()} (두 배: {doubled()})</p>
      {/* Solid에서는 값에 접근할 때 함수 호출 — React와 다름 */}
      <button onClick={() => setCount(c => c + 1)}>증가</button>
    </div>
  );
}
```

SolidJS는 JSX를 사용하지만 React와 전혀 다르게 동작한다. **컴포넌트 함수는 한 번만 실행된다**. React의 "상태가 바뀌면 컴포넌트 함수가 다시 실행된다"는 모델이 없다. 대신 signal의 getter(`count()`)를 JSX 안에서 호출하면 그 DOM 노드가 signal에 직접 구독된다. 값이 바뀌면 그 DOM 노드만 업데이트된다. 가상 DOM 없이 fine-grained reactivity를 구현한다.

성능 벤치마크에서 최상위를 기록하지만, 한국 시장에서의 채택률은 매우 낮다. 학습과 실험 목적으로 관심을 받고 있다.

> **📚 Java/Kotlin 시선 박스 ③ — Android Jetpack Compose ↔ React**
>
> Jetpack Compose를 알고 있다면 React의 재구성(recomposition) 모델과 비교하면 흥미롭다.
>
> Compose에서 상태가 바뀌면 해당 상태를 읽는 Composable 함수가 다시 실행된다(recomposition). React에서 상태가 바뀌면 해당 컴포넌트 함수와 하위 트리가 다시 실행된다(re-render). 기본 동작이 비슷하다.
>
> Compose의 `remember { mutableStateOf(0) }`는 React의 `useState(0)`에 대응하고, `LaunchedEffect`는 `useEffect`에 대응한다. `derivedStateOf`는 `useMemo`와 비슷하다.
>
> 핵심 차이는 Compose는 **smart recomposition** — 상태를 실제로 읽는 Composable만 재실행한다. React는 기본적으로 컴포넌트 트리 전체를 다시 실행하고 `React.memo`, `useMemo`, `useCallback`으로 최적화한다.
>
> SolidJS의 signal 모델은 Compose의 smart recomposition과 더 가깝다. 함수를 다시 실행하지 않고 signal을 읽는 DOM 노드만 업데이트한다.

### 한국 시장에서 언제 만나는가 — 결정 표

| 프레임워크 | 한국 시장 현황 | 만날 수 있는 상황 |
|---|---|---|
| **React** | 압도적 표준 | 거의 모든 신규 프론트 프로젝트 |
| **Vue 3** | 카카오·네이버 일부, 게임 회사 일부 | 2015~2020년 시작한 프로젝트 |
| **Vue 2** | 레거시 다수 | 마이그레이션 대상 |
| **Svelte** | 매우 드묾 | 개인 프로젝트, 일부 실험적 도입 |
| **SolidJS** | 거의 없음 | 학습·벤치마크 목적 |
| **Astro** | 드묾 | 콘텐츠 사이트, 기술 블로그 — 13장에서 다룬다 |

Vue 프로젝트를 만났을 때는 Composition API (`setup`) 기반인지 Options API 기반인지 먼저 확인하는 편이 낫다. Options API는 Vue 2 스타일이고 TypeScript 통합이 불편하다. `<script setup lang="ts">`가 보이면 Composition API + TypeScript의 현대적 방식이다.

다른 reactivity 모델로 이전이 필요할 때는 먼저 **멘탈 모델을 비운다**. React의 "렌더 = 함수 재실행"을 Vue·Solid에 그대로 가져오면 이해가 꼬인다. 각 프레임워크의 공식 문서 첫 장부터 다시 읽는 것이 가장 빠른 길이다.

---

## 마무리

React와 TypeScript가 만나는 지점은 생각보다 세밀하다. `forwardRef`의 제네릭 순서, `useRef`의 초기값 `null`이 갖는 의미, `as const`가 튜플 반환에 미치는 영향 — 이 작은 것들이 실무에서 막히는 자리다. 문서를 한 번 읽고 넘어갔을 때는 이해한 것 같지만, 처음 직접 컴포넌트 라이브러리를 설계할 때 다시 막히는 것이 이런 지점들이다.

`z.infer`가 폼 검증에서 단일 진실 원천이 되는 패턴, `useReducer`의 discriminated union이 Kotlin `sealed class`와 같은 역할을 하는 것, `forwardRef`로 캡슐화된 명령형 인터페이스를 노출하는 `useImperativeHandle` — 이 패턴들은 Java/Kotlin에서 온 개발자에게 낯설지 않은 개념이 TypeScript·React 방언으로 표현된 것이다.

Vue·Svelte·Solid가 다른 reactivity 모델을 갖고 있다는 것을 알고 있으면, 그 코드베이스를 처음 열었을 때 당황하지 않는다. 가상 DOM이 없어서가 아니라, 컴포넌트 함수가 한 번만 실행된다는 사실을 알고 있으면 Solid 코드가 이해된다. `.value`를 통해 접근해야 한다는 것을 알면 Vue의 `ref`가 낯설지 않다.

기억해두자 — 컴포넌트의 props 타입은 컴포넌트의 공개 계약이다. 이 계약을 명확하게 선언하는 것이 팀원과의 소통이고, 미래의 자신과의 소통이다.

---

> **📖 더 깊이 가려면**
>
> - React 컴포넌트의 테스트: Vitest + Testing Library + expect-type 패턴은 **14장**에서 자세히 다룬다. 컴포넌트의 타입이 올바른지를 타입 레벨에서 검증하는 `expect-type`의 활용, Testing Library의 쿼리 타입, Mock Service Worker를 통한 API 모킹 타입까지.
>
> - Next.js App Router의 Server Components·Server Actions 깊이: **13장** 풀스택 절에서 다룬다. RSC의 타입 경계, Server Actions의 `use server` 지시자, Astro의 Islands Architecture도 13장에서.
>
> - React Hook Form 공식 문서의 TypeScript 통합 가이드: https://react-hook-form.com/ts
>
> - zod 공식 문서 (schema 조합·변환): https://zod.dev
>
> - Total TypeScript의 React + TypeScript 패턴 시리즈: https://www.totaltypescript.com
