# 15장. 마지막 카드 세 장 — useSyncExternalStore, useImperativeHandle, flushSync

지금까지 1부에서는 상태를 어떻게 모델링할지 살펴봤고, 2부에서는 effect와 ref, 그리고 커스텀 훅을 거치며 React 바깥과 닿는 면을 정돈하는 법을 익혔다. 손에 익은 도구만으로 일상의 99%는 처리된다. `useState`로 시각 상태를 그리고, `useReducer`로 사용자 의도 단위의 변경을 묶고, Context로 멀리 있는 자식과 의미만 공유하고, `useEffect`로 외부 시스템과 동기화하고, `useRef`로 경계 너머의 값을 잠시 보관한다. 이 다섯 장면이 매끄러우면, 대부분의 코드는 지루할 만큼 평온하게 흘러간다.

그런데 가끔 평온한 흐름이 막히는 자리가 있다. 외부에 별도의 store가 살아 있는데 React가 그것을 자기 데이터인 양 다뤄야 할 때. 자식 컴포넌트가 부모에게 단지 "이걸 해 줘"라는 명령형 행동만을 노출해야 할 때. 새로 추가한 항목이 화면에 그려지자마자 그 자리로 즉시 스크롤해야 할 때. 이런 자리는 1~14장의 도구만으로는 어딘가 어긋난다. `useState`를 써 보면 한 박자 늦고, `useEffect`를 써 보면 race condition이 생기고, prop으로 풀어내자니 인터페이스가 너무 넓어진다.

이런 자리를 위해 React는 마지막 카드 세 장을 남겨 두었다. `useSyncExternalStore`, `useImperativeHandle`, `flushSync`. 이 셋은 escape hatch 중에서도 가장 마지막 escape hatch다. 평소에는 손에 들지 않는다. 그러나 정말로 필요한 자리를 만나면, 이 카드들 없이는 코드가 깔끔하게 풀리지 않는다.

이 장에서는 카드 한 장씩 펼쳐 본다. 언제 꺼내는지, 왜 꺼내야 하는지, 그리고 꺼낸 다음에는 어떻게 다시 접어 넣을지를 함께 살펴보자. 끝에는 작은 칸반 앱을 통합 시나리오로 잡고, 1부와 2부에서 익힌 도구들이 어떻게 한 자리에 모여 협력하는지를 마지막으로 정리한다.

## 카드 1 — useSyncExternalStore: React 바깥에 살아 있는 진실과 만날 때

먼저 가장 자주 마주치는 마지막 카드부터 펼쳐 보자. 우리가 다루는 데이터의 99%는 React 안에서 자라난다. `useState`가 그 데이터를 만들고, 컴포넌트 트리 안에서 흐르고, 다시 `setState`로 갱신된다. 그러나 React 바깥에서 살아 움직이는 진실이 있다. 브라우저의 `navigator.onLine`, `window.matchMedia`, `localStorage`, `history` 같은 플랫폼 API가 그렇다. Zustand나 Redux 같은 외부 store도 같은 부류다. 이런 진실들은 React가 만들지 않았고, 그래서 React는 그것이 언제 변하는지 자동으로 알지 못한다.

여기서 흔히 빠지는 함정이 있다. "그러면 `useEffect`로 구독하면 되지 않나?"라는 생각이다. 실제로 많은 코드가 그렇게 작성되어 있다. 한번 살펴보자.

```tsx
// 안티패턴 — 외부 store를 useEffect로 직접 구독
function useOnlineStatus(): boolean {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const updateStatus = () => setIsOnline(navigator.onLine);
    window.addEventListener('online', updateStatus);
    window.addEventListener('offline', updateStatus);
    return () => {
      window.removeEventListener('online', updateStatus);
      window.removeEventListener('offline', updateStatus);
    };
  }, []);

  return isOnline;
}
```

겉으로 보기에 멀쩡하다. 동작도 평범한 환경에서는 잘 한다. 그런데 이 코드는 두 가지 자리에서 조용히 무너진다.

첫째, **서버 사이드 렌더링(SSR) 환경**이다. 서버에는 `navigator`라는 객체가 없다. `useState(navigator.onLine)` 한 줄이 서버에서 즉시 터진다. 둘째, 더 미묘한 자리는 **concurrent rendering**이다. React 18부터 동시성 렌더링이 기본 동작에 포함되었다. 한 트리 안의 어떤 부분은 이미 새 store 값을 본 상태로 렌더되고, 다른 부분은 아직 옛 값을 본 상태로 렌더된다. 이를 **tearing**이라 부른다. UI가 같은 시점에 일관된 모습으로 그려지지 않는 현상이다. 사용자에게는 "어 방금 온라인이라며 아래는 오프라인 표시인데?" 같은 불일치로 다가온다. 디버깅하려고 하면 손에 잘 잡히지 않는다. 찜찜하다.

이 두 문제를 한 번에 해결하기 위해 React 팀이 마련한 카드가 `useSyncExternalStore`다. 이름이 길어 처음에는 부담스러운데, 시그니처를 뜯어 보면 의외로 단순하다.

```tsx
const value = useSyncExternalStore(
  subscribe,        // (onStoreChange) => unsubscribe
  getSnapshot,      // () => current value
  getServerSnapshot // () => SSR value (선택)
);
```

세 인자가 각자 한 가지 일을 한다. `subscribe`는 store가 변할 때 React에게 알려 줄 통로를 마련한다. `getSnapshot`은 지금 이 순간 store의 값을 가져온다. `getServerSnapshot`은 서버에서 렌더할 때 쓸 값을 알려 준다. 이 세 함수가 모이면, React는 알아서 tearing 없는 일관된 렌더를 보장한다.

같은 `useOnlineStatus`를 이번엔 마지막 카드로 다시 써 보자.

```tsx
import { useSyncExternalStore } from 'react';

function subscribe(onStoreChange: () => void): () => void {
  window.addEventListener('online', onStoreChange);
  window.addEventListener('offline', onStoreChange);
  return () => {
    window.removeEventListener('online', onStoreChange);
    window.removeEventListener('offline', onStoreChange);
  };
}

function getSnapshot(): boolean {
  return navigator.onLine;
}

function getServerSnapshot(): boolean {
  return true; // 서버에서는 일단 온라인이라고 가정
}

export function useOnlineStatus(): boolean {
  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}
```

코드가 짧아진 것이 핵심이 아니다. 핵심은 의미가 또렷해졌다는 점이다. `useEffect`로 짠 코드는 "내가 onLine을 추적하면서 setState를 호출해 React state로 미러링한다"는, 네 단계로 쪼개진 이야기였다. 새 카드는 그것을 한 줄로 줄인다. "React 바깥에 사는 store를 React 트리 안에서 안전하게 읽는다." 의미가 한 줄이면 버그도 한 줄에서만 생긴다.

조금 더 실무에 가까운 예제로 가 보자. 화면 폭에 따라 분기하는 컴포넌트를 만든다고 해 보자. 보통은 `window.matchMedia`를 쓴다.

```tsx
import { useSyncExternalStore } from 'react';

function makeMediaQueryStore(query: string) {
  const mql = window.matchMedia(query);

  return {
    subscribe(onChange: () => void) {
      mql.addEventListener('change', onChange);
      return () => mql.removeEventListener('change', onChange);
    },
    getSnapshot() {
      return mql.matches;
    },
    getServerSnapshot() {
      return false;
    },
  };
}

const mobileStore = makeMediaQueryStore('(max-width: 640px)');

export function useIsMobile(): boolean {
  return useSyncExternalStore(
    mobileStore.subscribe,
    mobileStore.getSnapshot,
    mobileStore.getServerSnapshot,
  );
}
```

여기서 한 가지 작은 트릭이 있다. `subscribe`와 `getSnapshot`은 가능하면 **모듈 스코프나 안정된 참조**여야 한다. 매 렌더마다 새 함수가 들어가면 React는 매번 구독을 새로 거는 걸로 오해할 수 있다. 객체 dependency 함정의 친척이라고 보면 된다. 그래서 위 코드는 `mobileStore`를 모듈 최상단에서 한 번만 만들어 두었다.

외부 상태 라이브러리와의 만남도 같은 모양이다. Zustand 같은 라이브러리가 자체적으로 `useSyncExternalStore`를 내부에서 호출한다. 우리가 `const value = useStore(state => state.value)` 한 줄을 쓸 때, 그 안쪽에서 정확히 같은 카드가 펼쳐진다. 그래서 Zustand는 SSR 환경에서도, concurrent 모드에서도 안정적으로 동작한다. **외부 store가 React와 만나는 자리에는 결국 이 카드가 깔린다**고 기억해 두자.

그렇다면 우리는 언제 직접 `useSyncExternalStore`를 호출할까. 답은 단순하다. **이미 만들어진 외부 store 라이브러리를 쓰는 게 아니라, 직접 외부 시스템을 React에 노출하는 작은 훅을 만들 때**다. `navigator.onLine`처럼 브라우저 API를 감싸거나, 자체 구현한 작은 in-memory store를 React에 연결하거나, `localStorage`의 변경을 다른 탭에서도 감지하는 훅을 만들 때다. 라이브러리 사용자라면 거의 직접 호출할 일이 없고, 라이브러리 작성자라면 이 카드를 자주 만진다.

마지막으로 한 가지 당부. 이 카드를 꺼낸다면 `useEffect`로 구독을 흉내내는 코드는 한 자리에 한 번만 남겨 두자. 같은 외부 store를 어떤 곳에서는 effect로 구독하고 어떤 곳에서는 useSyncExternalStore로 구독하면, 그 사이에 일관성이 뚫린다. 한 store에는 한 진입로만. 잊지 말자.

## 카드 2 — useImperativeHandle: 자식이 부모에게 명령형 API를 빌려줄 때

두 번째 카드로 넘어가자. 가끔 자식 컴포넌트가 부모에게 "이걸 해 줘"라는 동작을 노출해야 하는 상황이 있다. 모달의 `open()`/`close()`, 비디오 플레이어의 `play()`/`pause()`, 입력란의 `focus()`, 리스트 아이템의 `scrollIntoView()` 같은 것들이다. 이 동작들은 본질적으로 **명령형**이다. 선언형으로 다루기에는 어색한 자리가 있다.

물론 대부분의 경우는 선언형으로 충분히 풀린다. 모달이라면 `<Modal isOpen={isOpen} onClose={...} />`로 충분하다. 비디오라면 `<Video isPlaying={isPlaying} />`이 더 깔끔하다. 입력란 focus조차도 `autoFocus` prop이나 ref를 직접 노출하면 된다. 이런 자리에서 굳이 명령형 API를 꺼낼 필요는 없다. 선언형이 가능한 자리에서 명령형으로 가면 결합도가 깊어지고, 부모가 자식의 내부 사정을 너무 많이 알게 된다. 끔찍한 일이다.

그렇다면 `useImperativeHandle`은 언제 등장하는가. 두 가지 자리에서 자연스럽다. 첫째, **선언형으로 표현하면 prop 간의 모순이 생기는 자리**다. 예를 들어 비디오 플레이어를 `isPlaying` prop으로 제어한다고 하자. 사용자가 비디오 컨트롤로 직접 일시정지를 했다면 이제 React state는 `isPlaying = true`인데 실제 비디오는 정지 상태가 된다. 이런 모순을 신경 쓸 시간에 차라리 부모가 명령으로 제어하는 편이 깔끔할 때가 있다. 둘째, **자식의 ref를 그대로 넘기되 그 표면이 너무 넓을 때**다. 자식 안의 `<input>` ref를 부모에게 그대로 노출하면 부모가 `focus()`만 부르려다 의도치 않게 `value`를 직접 바꿀 수도 있게 된다. 표면을 좁혀 줄 필요가 있다.

`useImperativeHandle`은 정확히 이 두 자리를 위한 카드다. 자식이 부모에게 노출할 ref API를 **자식이 직접 정의**하게 해 준다. 부모는 정의된 메서드만 부를 수 있고, 자식 내부의 진짜 DOM에는 손을 못 댄다. 경계가 그어진다.

먼저 React 19의 새 패턴을 보자. 18까지는 `forwardRef`로 ref를 받아야 했지만, 19부터는 ref가 그냥 prop으로 들어온다. 그래서 코드가 한결 깔끔하다.

```tsx
import { useRef, useImperativeHandle } from 'react';

interface MyInputHandle {
  focus(): void;
  clear(): void;
}

interface MyInputProps {
  ref?: React.Ref<MyInputHandle>;
  placeholder?: string;
}

function MyInput({ ref, placeholder }: MyInputProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus();
    },
    clear() {
      if (inputRef.current) {
        inputRef.current.value = '';
      }
    },
  }), []);

  return <input ref={inputRef} placeholder={placeholder} />;
}
```

여기서 두 가지 ref가 등장한다. `inputRef`는 자식 내부에서 진짜 `<input>` DOM 노드를 가리키는 비공개 ref다. 부모는 이걸 보지 못한다. `ref`는 부모에게서 받은 ref이고, `useImperativeHandle`이 이 ref에 부모가 부를 수 있는 메서드 객체를 매단다. 그 객체에는 `focus`와 `clear`만 있다. 부모가 자식의 `value`를 직접 건드리거나 `select()`를 부르고 싶어도, 노출되지 않은 표면은 만질 수 없다. **자식의 내부가 자식의 손에 머문다.**

부모 쪽 사용 코드를 보자.

```tsx
import { useRef } from 'react';

function Form() {
  const inputHandle = useRef<MyInputHandle>(null);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        inputHandle.current?.clear();
        inputHandle.current?.focus();
      }}
    >
      <MyInput ref={inputHandle} placeholder="이름을 입력하세요" />
      <button type="submit">전송</button>
    </form>
  );
}
```

깔끔하다. 부모는 `focus`와 `clear` 두 동작만 알면 되고, 그 안쪽에서 어떤 DOM 조작이 일어나는지는 자식이 책임진다. 만약 나중에 자식의 내부 구현을 `<input>`이 아니라 contenteditable로 바꿔도, 부모 쪽 코드는 한 줄도 바뀌지 않는다. **인터페이스가 안정되고 구현은 자유롭다.**

조금 더 큰 예제로 가 보자. 모달 컴포넌트가 자기 자신의 표시 상태를 스스로 관리하면서, 부모에게는 `open()`/`close()`만 노출하는 모양이다.

```tsx
import { useState, useRef, useImperativeHandle } from 'react';

interface ModalHandle {
  open(): void;
  close(): void;
}

interface ModalProps {
  ref?: React.Ref<ModalHandle>;
  title: string;
  children: React.ReactNode;
}

function Modal({ ref, title, children }: ModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);

  useImperativeHandle(ref, () => ({
    open() {
      setIsOpen(true);
      dialogRef.current?.showModal();
    },
    close() {
      setIsOpen(false);
      dialogRef.current?.close();
    },
  }), []);

  if (!isOpen) return null;

  return (
    <dialog ref={dialogRef}>
      <h2>{title}</h2>
      {children}
    </dialog>
  );
}

// 사용처
function App() {
  const modalRef = useRef<ModalHandle>(null);

  return (
    <>
      <button onClick={() => modalRef.current?.open()}>열기</button>
      <Modal ref={modalRef} title="확인">
        <p>정말 진행하시겠습니까?</p>
        <button onClick={() => modalRef.current?.close()}>닫기</button>
      </Modal>
    </>
  );
}
```

부모는 `isOpen` 같은 상태를 자기가 들고 있을 필요가 없다. 모달 자신이 자기 표시 상태를 책임진다. 부모는 그저 "열어 줘"라고 말하고, "닫아 줘"라고 말한다. **명령형 API의 좁은 인터페이스가 부모의 인지 부담을 덜어 준다.**

여기서 한 가지 의문이 들 수 있다. "그러면 이걸 props로 풀면 어떻게 되는가? `<Modal isOpen={isOpen} onClose={...} />` 식으로." 좋은 질문이다. 두 방식은 사실 트레이드오프가 있다.

prop 방식은 React의 데이터 흐름에 자연스럽게 녹는다. 모달이 열려 있는지 부모도 알고 자식도 안다. URL의 일부로 표현하기도 쉽고, 테스트하기도 쉽다. 단점은 부모가 모달의 표시 상태를 책임져야 한다는 점이다. 작은 앱에서는 사소하지만, 모달이 여러 개 떠 있고 어떤 것은 어디 깊은 자식에서 열려야 한다면, 그 상태들을 부모까지 끌어올리는 것이 번거롭다.

명령형 핸들 방식은 그 번거로움을 모달 자신에게 다시 내려놓는다. 그러나 대가가 있다. 부모는 모달의 상태를 직접 보지 못한다. "지금 열려 있는가?"를 알려면 또 다른 prop이나 콜백이 필요하다. URL과 동기화하기도 어색하다. 그리고 ref를 통한 결합은 prop을 통한 결합보다 추적이 어렵다.

그래서 권장하는 순서는 이렇다. **먼저 props로 풀어 보자.** 그게 자연스러우면 거기서 멈춘다. 풀어 보고 부모가 너무 많은 상태를 책임지게 되거나, 자식의 내부 메커니즘이 부모에게 새어 나가는 느낌이라면, 그때 `useImperativeHandle`을 꺼낸다. 이 순서를 거꾸로 하면 거의 항상 후회한다.

마지막으로 작은 주의 하나. `useImperativeHandle`의 두 번째 인자로 넘기는 함수는 의존성 배열을 잘 챙겨야 한다. 그 함수가 클로저로 잡고 있는 값이 바뀌어도, 의존성 배열이 비어 있다면 핸들 안의 메서드는 옛 값을 본다. effect의 stale closure와 같은 문제가 여기서도 그대로 나타난다. 의존성 배열을 정직하게 쓰자.

## 카드 3 — flushSync: 다음 페인트 전에 DOM이 갱신되어야 할 때

세 번째 카드는 가장 드물게 등장하지만, 정말 필요한 자리에서 다른 어떤 것으로도 대체되지 않는다. 상황을 가정해 보자. 채팅 앱을 만들고 있다. 새 메시지가 도착하면 메시지 리스트 끝에 추가되고, 자동으로 그 메시지로 스크롤되어야 한다. 코드를 쉽게 짜 보자.

```tsx
function ChatList() {
  const [messages, setMessages] = useState<Message[]>([]);
  const listRef = useRef<HTMLUListElement>(null);

  function handleSend(text: string) {
    const newMessage: Message = { id: crypto.randomUUID(), text };
    setMessages([...messages, newMessage]);

    // 막 추가한 메시지로 스크롤하고 싶다
    listRef.current?.lastElementChild?.scrollIntoView();
  }

  return (
    <ul ref={listRef}>
      {messages.map(m => <li key={m.id}>{m.text}</li>)}
    </ul>
  );
}
```

직관적으로 보면 멀쩡해 보인다. 그런데 실행해 보면 새 메시지가 아니라 **이전 마지막 메시지로** 스크롤한다. 난감하다. 왜 그럴까?

답은 React의 배치 업데이트에 있다. `setState`는 호출 즉시 DOM을 업데이트하지 않는다. 같은 이벤트 안에서 발생한 여러 `setState`를 모아 두었다가, 이벤트 핸들러가 끝난 후 한 번에 다시 렌더하고 DOM을 갱신한다. 그래서 `setMessages` 다음 줄에서 `listRef.current?.lastElementChild`를 읽으면, 그건 아직 **이전 렌더의 마지막 자식**이다. 새 메시지는 아직 DOM에 들어가지 않았다.

이 자리에서 펼치는 마지막 카드가 `flushSync`다. `react-dom`에서 import한다. 이름 그대로, 안쪽의 setState를 동기적으로 즉시 flush해서 DOM을 갱신한 다음 다음 줄로 넘어간다.

```tsx
import { flushSync } from 'react-dom';

function ChatList() {
  const [messages, setMessages] = useState<Message[]>([]);
  const listRef = useRef<HTMLUListElement>(null);

  function handleSend(text: string) {
    const newMessage: Message = { id: crypto.randomUUID(), text };

    flushSync(() => {
      setMessages([...messages, newMessage]);
    });
    // 여기서는 새 메시지가 이미 DOM에 들어가 있다
    listRef.current?.lastElementChild?.scrollIntoView();
  }

  return (
    <ul ref={listRef}>
      {messages.map(m => <li key={m.id}>{m.text}</li>)}
    </ul>
  );
}
```

깔끔하게 동작한다. `flushSync` 콜백 안의 `setMessages`가 끝나는 순간 React는 즉시 다시 렌더하고, DOM을 갱신하고, 그제야 다음 줄로 넘어간다. 이제 `lastElementChild`는 정확히 새로 추가된 메시지 노드를 가리킨다.

비슷한 자리는 또 있다. 모달을 열자마자 안의 입력란에 focus를 주는 경우. 새 항목을 추가한 후 그 입력란을 측정해서 위치를 잡는 경우. 트리 노드를 펼친 직후 그 노드의 높이를 재서 애니메이션을 시작하는 경우. 모두 **"setState 후 즉시 DOM이 갱신된 상태에서 측정/조작이 필요하다"**는 공통점을 가진다.

```tsx
import { flushSync } from 'react-dom';

function Tree({ items }: { items: TreeItem[] }) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const itemRefs = useRef<Map<string, HTMLLIElement>>(new Map());

  function handleExpand(id: string) {
    flushSync(() => {
      setExpanded(prev => new Set(prev).add(id));
    });
    // 펼쳐진 직후의 높이를 재서 애니메이션을 건다
    const node = itemRefs.current.get(id);
    if (node) {
      const height = node.getBoundingClientRect().height;
      node.style.setProperty('--final-height', `${height}px`);
      node.classList.add('animate-expand');
    }
  }

  // ...
}
```

자, 이쯤에서 한 가지 강한 당부를 해야 한다. **`flushSync`는 비싸다.** 안쪽의 setState가 호출될 때마다 React가 자기 일을 멈추고 동기적으로 렌더 사이클을 돌린다. 다른 업데이트와 묶일 수 있었을 작업이 강제로 분리된다. concurrent rendering의 우선순위 조정 능력이 그 자리에서 멈춘다. 자주 쓰면 그 자체로 성능 비용이 된다.

그래서 `flushSync`는 **정말로 다음 페인트 전에 DOM이 갱신되어야 하는 자리에만** 쓴다. 측정이 필요하거나 focus나 스크롤처럼 사용자가 즉시 인지할 수 있는 자리. 그리고 그 호출은 가능하면 한 핸들러 안에서 한 번이어야 한다. 만약 한 흐름 안에서 `flushSync`가 두세 번 등장하고 있다면, 그건 흐름을 다시 들여다봐야 한다는 신호다. 보통 이런 자리는 ref callback이나 layout effect로 더 깔끔하게 풀린다.

한 가지 더. `flushSync`를 React 이벤트 핸들러 안이 아닌 곳에서 부르면, 예를 들어 `setTimeout` 콜백 안에서 부르면, 동작은 하되 React가 경고를 띄울 수 있다. 그건 "이 자리는 정말 필요한 자리인가?"를 다시 묻는 신호로 받아들이는 편이 낫다.

## 세 카드의 공통점 — "마지막 카드"라 부르는 이유

세 카드를 한 번씩 펼쳐 보았다. 이제 잠깐 멈춰서 이들의 공통점을 살펴보자. 왜 우리는 이 셋을 묶어 "마지막 카드"라 부르는가?

**첫째, 셋 모두 React의 평소 모델을 잠깐 비켜선다.** `useSyncExternalStore`는 React가 만들지 않은 데이터의 진실을 React에 끌어들인다. `useImperativeHandle`은 선언형 모델 대신 명령형 API의 작은 창을 자식에게 허락한다. `flushSync`는 비동기 배치라는 React의 기본 정책을 잠깐 멈춘다. 셋 다 React의 기본 흐름에서 한 발 비켜선 자리다. 그래서 이들을 사용하면 React의 기본 보호막에서도 한 발 비켜선다. tearing이 알아서 막히고, 인터페이스가 알아서 좁혀지고, 우선순위가 알아서 조정되는 마법이 그 자리에서 약해진다. 직접 책임져야 한다.

**둘째, 셋 모두 대안이 있을 가능성이 매우 높다.** `useSyncExternalStore`를 꺼내기 전에 "그 store가 정말 React 바깥에 있어야 하는가?"를 자문해 보자. 답이 "내가 만든 작은 store다"라면, useState로 충분할 수도 있다. `useImperativeHandle`을 꺼내기 전에 "props로 풀 수 있는가?"를 자문해 보자. 답이 "아직 풀 수 있다"면, props 쪽이 거의 항상 더 낫다. `flushSync`를 꺼내기 전에 "layout effect나 ref callback으로 풀 수 있는가?"를 자문해 보자. 답이 "그렇다"면, 그쪽이 비용이 더 적다.

**셋째, 셋 모두 라이브러리 작성자의 도구에 가깝다.** 애플리케이션 코드에서 직접 호출하는 일은 드물다. Zustand나 Redux 같은 외부 store 라이브러리가 `useSyncExternalStore`를 내부에서 쓴다. 디자인 시스템의 dialog/popover 컴포넌트가 `useImperativeHandle`을 내부에서 쓴다. 가상 스크롤 라이브러리나 애니메이션 라이브러리가 `flushSync`를 내부에서 쓴다. 우리가 일반 화면을 만들 때는 그 라이브러리들의 잘 만든 인터페이스만 보면 된다. 직접 이 카드들을 꺼낼 일은 정말 드물어야 한다.

이 세 가지가 합쳐져 "마지막 카드"라는 별명이 생긴다. 평소엔 손에 들지 않는 카드. 들었다면 그 자리는 검증을 받아야 하는 자리. 들고 나서는 잘 정돈해 다시 접어 넣어야 하는 카드.

## 결정 트리 — 카드를 꺼내기 전에 자문하기

세 카드 어느 쪽이든 꺼내기 전에 한 번씩 통과해야 할 질문들이 있다. 머릿속에 도식 하나 그려 두자.

```
[외부 store / 브라우저 API와 만났는가?]
├─ 이미 라이브러리가 있다 (Zustand, Redux, TanStack Query)
│  └─ 그 라이브러리의 훅을 써라. 끝.
├─ 작은 store를 직접 만든다
│  └─ subscribe + getSnapshot + useSyncExternalStore
└─ 그냥 React state면 충분하다
   └─ useState/useReducer

[자식이 부모에게 동작을 노출해야 하는가?]
├─ 선언형 props로 표현 가능 (isOpen, isPlaying...)
│  └─ props로 풀어라. 끝.
├─ 자식의 ref를 그대로 노출해도 무방 (단순 focus)
│  └─ ref를 prop으로 그대로 넘겨라.
└─ 표면을 좁혀야 하고 자식이 상태를 책임진다
   └─ useImperativeHandle로 작은 인터페이스만 노출

[setState 후 즉시 DOM 측정/조작이 필요한가?]
├─ 측정 시점을 다음 렌더로 미뤄도 된다
│  └─ useLayoutEffect로 처리
├─ ref callback에서 처리 가능
│  └─ ref callback 사용
└─ 같은 핸들러 안에서 즉시 갱신된 DOM이 필요
   └─ flushSync (단, 비용 알고)
```

이 트리를 매번 외울 필요는 없다. 한 번만 그려 두면 코드를 짜다가 카드를 꺼내려는 순간 머릿속에서 이 가지들이 떠오를 것이다. 떠오르면 잠깐 멈추고, 한 단계씩 위로 올라가 더 단순한 답이 있는지 확인하자. **가지의 가장 깊은 끝까지 갔을 때만 마지막 카드를 꺼낸다**. 이 습관이 escape hatch를 escape hatch답게 쓰는 자세다.

## 통합 시나리오 — 작은 칸반 앱

마지막으로, 1부와 2부에서 익힌 도구들이 어떻게 한 자리에 모이는지 작은 칸반 앱으로 살펴보자. 칸반은 컬럼들이 있고, 각 컬럼 안에는 카드들이 있다. 카드는 컬럼 사이를 옮겨 다닌다. 새 카드를 추가할 수 있고, 카드의 텍스트를 편집할 수도 있다. 작은 앱이지만 여러 도구가 자연스럽게 만나는 자리다.

먼저 데이터 모델을 잡자. 흔한 실수가 컬럼 안에 카드 배열을 그대로 중첩하는 것이다.

```ts
// 안티패턴 — 깊이 중첩된 state
type Board = {
  columns: Array<{
    id: string;
    title: string;
    cards: Array<{
      id: string;
      text: string;
    }>;
  }>;
};
```

이 모양이 끔찍해지는 순간은 카드를 한 컬럼에서 다른 컬럼으로 옮길 때다. spread 체인이 깊어지고, 어떤 카드가 어디에 있는지 추적하기 위해 매번 컬럼들을 순회해야 한다. 갱신할 때마다 잘못된 카드를 건드릴 위험이 있다. 찜찜하다. 2장에서 미뤄 둔 정규화(lookup table)가 여기서 자기 자리를 찾는다.

```ts
// 정규화된 모델
interface Card {
  id: string;
  text: string;
}

interface Column {
  id: string;
  title: string;
  cardIds: string[]; // 순서를 가진 ID 목록
}

interface Board {
  cards: Record<string, Card>;       // ID -> Card
  columns: Record<string, Column>;   // ID -> Column
  columnOrder: string[];             // 컬럼들의 순서
}
```

세 부분으로 나뉜다. `cards`는 카드 본체들의 lookup table. `columns`는 컬럼 본체들의 lookup table. `columnOrder`는 컬럼들이 화면에 그려질 순서. 컬럼 안에서는 자기에게 속한 카드들의 ID 배열만 들고 있다. 이 모양이라면 카드 이동은 두 컬럼의 `cardIds` 배열만 갱신하면 끝난다. 카드 본체에는 손대지 않는다.

다음으로 사용자 의도 단위의 변경을 reducer로 묶자. 1부에서 익힌 패턴이다.

```ts
type BoardAction =
  | { type: 'card-added'; columnId: string; text: string }
  | { type: 'card-edited'; cardId: string; text: string }
  | { type: 'card-moved'; cardId: string; toColumnId: string; toIndex: number }
  | { type: 'column-added'; title: string };

function boardReducer(state: Board, action: BoardAction): Board {
  switch (action.type) {
    case 'card-added': {
      const id = crypto.randomUUID();
      const card: Card = { id, text: action.text };
      const column = state.columns[action.columnId];
      return {
        ...state,
        cards: { ...state.cards, [id]: card },
        columns: {
          ...state.columns,
          [action.columnId]: {
            ...column,
            cardIds: [...column.cardIds, id],
          },
        },
      };
    }
    case 'card-edited': {
      const card = state.cards[action.cardId];
      return {
        ...state,
        cards: {
          ...state.cards,
          [action.cardId]: { ...card, text: action.text },
        },
      };
    }
    case 'card-moved': {
      const { cardId, toColumnId, toIndex } = action;
      // 어느 컬럼에 있는지 찾아서 떼어내고
      const fromColumnId = Object.values(state.columns).find(
        c => c.cardIds.includes(cardId)
      )!.id;
      const fromColumn = state.columns[fromColumnId];
      const newFromIds = fromColumn.cardIds.filter(id => id !== cardId);

      // 같은 컬럼 안 이동인지 다른 컬럼인지 분기
      if (fromColumnId === toColumnId) {
        const newIds = [...newFromIds];
        newIds.splice(toIndex, 0, cardId);
        return {
          ...state,
          columns: {
            ...state.columns,
            [toColumnId]: { ...fromColumn, cardIds: newIds },
          },
        };
      }

      const toColumn = state.columns[toColumnId];
      const newToIds = [...toColumn.cardIds];
      newToIds.splice(toIndex, 0, cardId);

      return {
        ...state,
        columns: {
          ...state.columns,
          [fromColumnId]: { ...fromColumn, cardIds: newFromIds },
          [toColumnId]: { ...toColumn, cardIds: newToIds },
        },
      };
    }
    case 'column-added': {
      const id = crypto.randomUUID();
      const column: Column = { id, title: action.title, cardIds: [] };
      return {
        ...state,
        columns: { ...state.columns, [id]: column },
        columnOrder: [...state.columnOrder, id],
      };
    }
  }
}
```

action들이 사용자 의도 단위라는 점에 주목하자. "카드가 추가됐다", "카드가 편집됐다", "카드가 옮겨졌다", "컬럼이 추가됐다". reducer 안에서는 정규화된 모양 덕분에 갱신이 단순하다. 깊은 spread가 없다.

이 reducer를 Context로 트리 깊은 곳까지 흘리자. 7장에서 익힌 패턴이다. state와 dispatch를 두 개의 Context로 분리해 두면, dispatch만 받는 자식은 state가 바뀌어도 리렌더되지 않는다.

```tsx
import { createContext, useContext, useReducer } from 'react';

const BoardStateContext = createContext<Board | null>(null);
const BoardDispatchContext = createContext<React.Dispatch<BoardAction> | null>(null);

export function BoardProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(boardReducer, initialBoard);

  return (
    <BoardStateContext.Provider value={state}>
      <BoardDispatchContext.Provider value={dispatch}>
        {children}
      </BoardDispatchContext.Provider>
    </BoardStateContext.Provider>
  );
}

export function useBoard(): Board {
  const ctx = useContext(BoardStateContext);
  if (!ctx) throw new Error('useBoard must be used inside BoardProvider');
  return ctx;
}

export function useBoardDispatch(): React.Dispatch<BoardAction> {
  const ctx = useContext(BoardDispatchContext);
  if (!ctx) throw new Error('useBoardDispatch must be used inside BoardProvider');
  return ctx;
}
```

이제 카드 컴포넌트는 자기 ID로 자기 데이터만 lookup해 가져간다. 다른 카드의 변경은 자기에게 영향을 주지 않는다.

```tsx
function CardItem({ id }: { id: string }) {
  const board = useBoard();
  const card = board.cards[id];
  const dispatch = useBoardDispatch();

  function handleEdit(text: string) {
    dispatch({ type: 'card-edited', cardId: id, text });
  }

  return (
    <li>
      <input
        value={card.text}
        onChange={(e) => handleEdit(e.target.value)}
      />
    </li>
  );
}
```

여기까지가 1부에서 익힌 도구들의 자리다. 정규화된 데이터, reducer, 두 개의 Context. 이제 2부의 도구들이 어디에 들어오는지 살펴보자.

새 카드를 추가하면 그 카드 자리로 즉시 스크롤하고 입력란에 focus를 주고 싶다. 이것이 우리가 본 `flushSync`의 자리다.

```tsx
import { flushSync } from 'react-dom';

function ColumnView({ columnId }: { columnId: string }) {
  const board = useBoard();
  const column = board.columns[columnId];
  const dispatch = useBoardDispatch();
  const listRef = useRef<HTMLUListElement>(null);

  function handleAdd() {
    flushSync(() => {
      dispatch({ type: 'card-added', columnId, text: '' });
    });
    // 새 카드가 DOM에 들어간 직후
    const lastInput = listRef.current?.querySelector<HTMLInputElement>('li:last-child input');
    lastInput?.focus();
    lastInput?.scrollIntoView({ block: 'nearest' });
  }

  return (
    <section>
      <h2>{column.title}</h2>
      <ul ref={listRef}>
        {column.cardIds.map(id => <CardItem key={id} id={id} />)}
      </ul>
      <button onClick={handleAdd}>+ 카드 추가</button>
    </section>
  );
}
```

만약 칸반 앱에 모달로 카드 상세 편집 기능이 있다면, 그 모달에 `useImperativeHandle`을 쓸 수 있다. 부모는 `modalRef.current?.open()` 한 줄로 모달을 연다. 모달의 표시 상태는 모달 자신이 책임진다. 부모는 카드 ID만 넘겨 주면 된다.

서버 동기화는 어떨까. 5.2 논쟁점에서 본 것처럼, 서버 캐시는 UI 상태와 다른 도구로 다루는 편이 낫다. TanStack Query가 그 자리를 잘 채운다. 그리고 그 안쪽에서 `useSyncExternalStore`가 동작한다. 우리는 직접 호출하지 않지만, 마지막 카드는 그 자리에서 자기 일을 한다.

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useBoardSync() {
  const queryClient = useQueryClient();
  const localBoard = useBoard();

  const serverBoard = useQuery({
    queryKey: ['board'],
    queryFn: fetchBoard,
  });

  const saveBoard = useMutation({
    mutationFn: saveBoardToServer,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board'] });
    },
  });

  // 디바운스해서 서버에 저장 (개념적 예시)
  useDebouncedEffect(() => {
    saveBoard.mutate(localBoard);
  }, [localBoard], 500);

  return { isLoading: serverBoard.isLoading, error: serverBoard.error };
}
```

UI 상태(reducer)와 서버 캐시(TanStack Query)가 한 컴포넌트 안에서 만나지만, 도구는 서로 다르다. 두 도구의 책임이 뒤섞이지 않는다. 이 분리가 칸반 앱이 커져도 깨지지 않는 비결이다.

이 작은 칸반 앱 안에서 우리는 1부의 정규화·reducer·Context를 쓰고, 2부의 ref·flushSync를 쓰고, 그리고 마지막 카드들이 라이브러리 안에서 일하는 모습을 보았다. **각 도구가 자기 자리에서 자기 일만 한다.** 한 도구가 다른 도구의 자리를 침범하지 않는다. 이것이 책 전체에서 우리가 만들고 싶었던 그림이다.

## 핵심 정리

이 장의 내용을 머리에 담아두기 위해 한 번 더 짚자.

1. **`useSyncExternalStore`는 React 바깥에 사는 진실을 React에 안전하게 가져온다.** SSR과 concurrent rendering에서 tearing 없이 동작한다.

2. **`useEffect`로 외부 store를 직접 구독하지 말자.** 평범한 환경에서는 동작하지만, 동시성·SSR에서 미묘한 버그가 새어 나온다.

3. **`subscribe`와 `getSnapshot`은 안정된 참조여야 한다.** 모듈 스코프에 두거나 useCallback으로 감싸자. 매 렌더마다 새 함수면 구독이 매번 다시 걸린다.

4. **`useImperativeHandle`은 자식이 부모에게 명령형 API를 노출하는 카드다.** 그러나 먼저 props로 풀 수 있는지부터 확인하자.

5. **`useImperativeHandle`을 쓸 때는 인터페이스를 좁혀라.** 자식 내부의 진짜 ref와 부모에게 노출되는 핸들을 분리해서, 부모는 정의된 메서드만 부르게 하자.

6. **`flushSync`는 setState 후 즉시 갱신된 DOM이 필요할 때만 쓴다.** 새 항목으로 즉시 스크롤하거나 모달 열고 즉시 focus처럼, 다음 페인트 전에 DOM이 보장되어야 하는 자리다.

7. **`flushSync`는 비싸다.** 자주 쓰면 concurrent rendering의 우선순위 조정 능력이 그만큼 약해진다. 한 핸들러에 한 번 정도가 한계라고 보자.

8. **세 카드 모두 라이브러리 작성자의 도구에 가깝다.** 애플리케이션 코드에서 직접 호출하는 일은 드물어야 한다. 자주 호출되고 있다면 그 자체로 신호다.

9. **마지막 카드를 꺼내기 전에 결정 트리를 머릿속에 한 번 그려 보자.** 가장 깊은 가지의 끝까지 갔을 때만 이 카드들이 진짜로 필요한 자리다.

10. **칸반 같은 작은 앱은 1부와 2부의 도구를 모두 쓴다.** 정규화로 데이터를 다듬고, reducer로 의도를 묶고, Context로 흘리고, ref와 flushSync로 마지막 모서리를 다듬는다. 각 도구가 자기 자리에 머무른다.

## 연습 문제

### [기초] window resize 이벤트를 useSyncExternalStore로

화면 폭에 따라 분기하는 컴포넌트를 만들어 보자. 먼저 `useEffect`와 `useState`로 `useWindowWidth()` 훅을 작성한다. 그 다음 `useSyncExternalStore`로 같은 훅을 다시 작성해 비교한다.

**미션:** 두 구현의 동작이 같은가? 코드 줄 수와 의미의 또렷함은 어떤가? `subscribe`와 `getSnapshot`을 모듈 스코프에 두는 이유를 자기 말로 설명할 수 있는가? 마지막으로, SSR 환경을 가정하고 `getServerSnapshot`이 없을 때 어떤 일이 생길지 머릿속으로 시뮬레이션해 보자.

**힌트:** `window.addEventListener('resize', ...)`를 `subscribe`에서 다루고, `getSnapshot`은 `() => window.innerWidth`다. 함수들을 컴포넌트 안에서 만들면 매 렌더마다 참조가 새로워진다는 점을 잊지 말자.

### [중] 비디오 컴포넌트에 play/pause를 useImperativeHandle로 (ref-as-prop과 비교)

비디오 플레이어 컴포넌트 `VideoPlayer`를 두 가지 방식으로 만들어 보자.

(a) **선언형 props 방식:** `<VideoPlayer src={...} isPlaying={isPlaying} onEnded={...} />`. 부모가 `isPlaying` 상태를 들고 있고, prop이 바뀌면 자식이 effect로 `play()`/`pause()`를 호출한다.

(b) **명령형 핸들 방식:** `<VideoPlayer ref={videoRef} src={...} onEnded={...} />`. 자식이 `useImperativeHandle`로 `play()`, `pause()`, `seek(seconds)` 메서드를 노출한다. 부모는 `videoRef.current?.play()`로 제어한다.

**미션:** 두 방식 모두 만들어 보고 사용처 코드를 비교하자. 사용자가 비디오 컨트롤로 직접 일시정지를 했을 때 두 방식은 어떻게 다르게 동작하는가? "현재 재생 중인지"를 부모가 알아야 한다면, 두 방식 중 어느 쪽이 더 자연스러운가? 만약 비디오 ID를 URL에 동기화해야 한다면 어느 쪽이 쉬운가? 마지막으로, "이 자리는 props가 낫다" 또는 "이 자리는 ref가 낫다"라는 결론을 자기 말로 정리해 보자.

**자문할 점:** ref 방식은 부모가 자식의 내부에 명령을 보낸다. props 방식은 부모와 자식이 같은 데이터를 본다. 두 모델의 차이가 코드 가독성과 유지보수에 어떻게 다르게 영향을 주는가?

### [도전] 동적 항목 추가 + 즉시 스크롤 + flushSync 사용/미사용 비교

채팅 메시지 리스트를 만들어 보자. 새 메시지를 추가하면 자동으로 그 메시지로 스크롤한다.

먼저 `flushSync` 없이 구현해 본다. 단순히 `setMessages`로 추가한 다음 `lastChild?.scrollIntoView()`를 호출한다. 어떤 일이 일어나는가? 그 다음 `flushSync`로 감싸서 다시 구현한다. 이번엔 어떻게 동작하는가?

**미션:** 두 버전을 나란히 두고 동작을 비교하자. `flushSync` 없는 버전이 정확히 어디서 어긋나는지 한 줄로 설명할 수 있는가? 그 다음, `flushSync` 대신 `useLayoutEffect`로 같은 효과를 낼 수 있을까? 시도해 보고, 둘의 차이가 무엇인지 적어 보자.

**도전 단계:** 메시지가 100개씩 빠르게 들어온다고 가정하자(예: WebSocket으로). `flushSync`를 매 메시지마다 호출하면 어떤 비용이 생기는가? 이 자리에서는 `flushSync`를 쓰지 않는 편이 나을 수도 있다 — 왜 그런지, 그리고 어떤 대안이 있는지 자기 말로 정리해 보자.

### [도전] 댓글 트리 정규화 — 삭제 시 자식까지 일관되게 제거

댓글 시스템을 만든다. 댓글은 다른 댓글의 답글이 될 수 있고, 답글에 또 답글이 달릴 수 있다. 깊이는 제한이 없다.

먼저 정규화된 데이터 모델을 설계하자. 힌트는 본문의 칸반 모델과 비슷하다. `comments`는 ID-Comment의 lookup table이고, 각 댓글은 자기 부모의 ID와 자기 자식들의 ID 배열을 갖는다. 또는 부모 ID만 갖고 자식은 부모 ID로 역검색해도 좋다. 두 방식의 트레이드오프를 적어 보자.

**미션:** 정규화 모델을 잡고, 다음 action들을 reducer로 작성하라.
- `comment-added`: 부모 ID 또는 null (최상위)을 받아 새 댓글 추가
- `comment-deleted`: 댓글 ID를 받아 그 댓글과 **모든 자손**을 삭제
- `comment-edited`: ID와 새 텍스트로 본문 수정

삭제 action에서 BFS 또는 재귀로 자손들을 모아 한 번에 제거하자. 그 다음 트리를 렌더하는 컴포넌트를 작성한다 — 이 안에서 `key`는 무엇으로 두어야 안전한가?

**자문할 점:** 만약 정규화 없이 중첩된 객체로 모델링했다면, 깊은 자손 삭제는 얼마나 끔찍해졌을까? 갱신할 때 spread 체인이 얼마나 길어졌을까? 정규화의 이점이 어디서 가장 또렷이 드러나는지 본문과 연결해 정리해 보자.

### [도전] 작은 칸반 앱 통합 설계

본문에서 살펴본 칸반 앱을 직접 작성해 보자. 다음 요구사항을 모두 만족시킨다.

1. 컬럼 추가/삭제, 카드 추가/편집/삭제
2. 카드를 다른 컬럼으로 옮기는 기능 (드래그가 어렵다면 셀렉트 박스로 대체)
3. 새 카드를 추가하면 그 카드의 입력란에 즉시 focus
4. 데이터 모델은 정규화 (lookup table + 순서 배열)
5. UI 상태는 useReducer + 두 개의 Context (state와 dispatch 분리)
6. 서버 동기화는 개념 설계만 — TanStack Query 같은 도구가 어디에 들어가는지 주석으로 표시
7. 모달로 카드 상세 편집을 한다면 `useImperativeHandle` 시도

**자문할 점:** 이 앱을 만들면서 1부와 2부의 어떤 도구가 어떤 자리에 들어갔는지 한 번 짚어 보자. 만약 정규화 없이 시작했다면 카드 이동 코드가 얼마나 어지러워졌을까? Context를 두 개로 분리하지 않았다면 dispatch만 쓰는 자식들도 매번 리렌더되었을까? 본문에서 강조한 "각 도구가 자기 자리에 머무른다"는 말이 이 작은 앱 안에서 어떻게 구현되는지를 자기 코드로 확인해 보자.

## 마무리 — 책을 덮을 시간

여기까지 왔다. 길었다. 처음에 자가 진단 8문항을 풀던 자리에서 시작해, useState의 미세한 결을 살피고, useReducer로 사용자 의도를 묶고, Context로 의미를 흘리고, useEffect로 외부 시스템과 동기화하고, useRef로 경계 너머의 값을 잡고, 커스텀 훅으로 stateful 로직을 갈무리하고, 마지막에는 거의 손에 들지 않는 세 장의 카드까지 펼쳐 보았다. 책 한 권을 통과하면서 우리는 React가 상태와 경계라는 두 단어를 어떻게 다루는지 한 줄씩 익혔다.

이 장이 마지막 본문이다. 그러나 책이 아주 끝난 것은 아니다. 닫는 글에서 한 번 더 머리를 정리하자. **렌더는 스냅샷, Effect는 동기화, Ref는 경계.** 이 세 문장이 책 전체의 요약이다. 그리고 0장에서 풀던 자가 진단 8문항을, 이번엔 답을 손에 쥐고 다시 풀어 본다. 같은 질문이 어떻게 다르게 보이는지 살펴보면, 그 자체로 한 권을 통과한 흔적이 손에 잡힐 것이다.

그 다음 월요일 아침, 우리는 이 책에서 무엇을 가지고 일상으로 돌아갈까. 그것을 정리하기 위해 마지막 한 장을 더 펼쳐 보자.
