# React 고급 — Managing State + Escape Hatches 레퍼런스

> 본 문서는 React 공식 문서(react.dev), 핵심 인물의 블로그(Dan Abramov, Kent C. Dodds, Robin Wieruch), 한국·영어권 커뮤니티(velog, Hacker News, dev.to 등)에서 수집한 자료를 통합·재정리한 책 저술용 레퍼런스다. 대상 독자는 JS/TS와 기본 React UI는 다뤄봤지만 상태 관리 패턴과 escape hatch에 대한 견고한 멘탈 모델은 아직 갖추지 못한 중급 개발자다.

---

## 1. 개념·정의

### 1.1 State 영역 핵심 용어

| 용어 | 정의 | 비고 |
|---|---|---|
| **State (상태)** | 컴포넌트가 시간에 따라 기억해야 하는 데이터. 변경 시 재렌더링을 트리거한다. | `useState`, `useReducer`로 선언 |
| **Snapshot (스냅샷)** | 한 번의 렌더 동안 props·state·effect가 가지는 고정된 값의 묶음. "값은 시간에 따라 변하는 것이 아니라, 매 렌더가 자기만의 값을 갖는다." (Dan Abramov) | useEffect의 stale closure 이해의 출발점 |
| **Props** | 부모가 자식에게 내려보내는 읽기 전용 값. | 컴포넌트의 입력 인자 |
| **Lifting State Up (상태 끌어올리기)** | 두 컴포넌트가 동기화되어야 할 때, state를 가장 가까운 공통 부모로 이동시키는 것. | "Single Source of Truth" 확보 |
| **Single Source of Truth** | 동일 정보의 출처를 단 하나의 컴포넌트에만 두는 원칙. | 동기화 버그 예방의 핵심 |
| **Controlled Component** | 부모 props로부터 값을 받아 표시하고, 변경은 부모에 위임하는 컴포넌트. | 협력에 유리, 보일러플레이트 증가 |
| **Uncontrolled Component** | 자기 자신이 state를 소유하는 컴포넌트. | 사용 간편, 외부 협력에 불리 |
| **Reducer (리듀서)** | `(state, action) => newState` 형태의 순수 함수. 상태 갱신 로직을 한 곳에 모은다. | `useReducer` |
| **Action (액션)** | "무슨 일이 벌어졌는가"를 기술하는 객체. 보통 `{ type, ...payload }`. | 사용자 의도 단위로 작성 |
| **Dispatch** | 액션을 리듀서에 보내는 함수. | `useReducer`가 반환 |
| **Context** | 컴포넌트 트리 하위 어디서든 값을 읽을 수 있게 해주는 메커니즘. | `createContext`, `useContext` |
| **Provider** | Context 값을 트리 일부 구간에 제공하는 컴포넌트. | `<MyContext value={...}>` |
| **Prop Drilling (프롭 드릴링)** | 중간 컴포넌트가 사용하지 않는 데이터를 단지 전달만 하는 안티패턴. | Context 또는 컴포넌트 합성으로 해결 |
| **Key** | 같은 위치의 컴포넌트를 React가 다른 컴포넌트로 인식하게 만드는 식별자. state를 강제로 리셋할 때 사용. | 인덱스 대신 안정된 ID 권장 |
| **Tree Position (트리 위치)** | React가 컴포넌트를 식별하는 기준. 같은 자리에서 같은 타입이면 state가 보존된다. | `key` 변경 시 새 컴포넌트로 취급 |

### 1.2 Escape Hatches 핵심 용어

| 용어 | 정의 | 비고 |
|---|---|---|
| **Ref** | 렌더링과 무관한 값을 보관하는 변경 가능한 컨테이너 (`{ current: ... }`). | 변경해도 재렌더링 없음 |
| **DOM Ref** | 실제 DOM 노드에 접근하기 위한 ref. | focus, scroll, 측정 등 |
| **Effect** | 렌더링 자체가 원인이 되어 실행되는 부수 효과. 외부 시스템과 컴포넌트를 동기화한다. | `useEffect` |
| **Cleanup Function** | Effect가 반환하는 함수. 다음 Effect 실행 직전과 언마운트 시 실행되어 이전 동기화를 정리한다. | 구독 해제, 연결 종료 등 |
| **Reactive Value (반응형 값)** | 컴포넌트 본체에서 선언된 모든 값. props, state, 그것들로부터 파생된 값. Effect 의존성에 반드시 포함되어야 한다. | 외부 상수는 반응형이 아님 |
| **Dependency Array (의존성 배열)** | Effect를 언제 다시 동기화할지 결정하는 반응형 값 목록. | linter가 강제 검증 |
| **Effect Event** | `useEffectEvent`로 만든 비반응형 함수. Effect 안에서 호출되지만 의존성 배열에 들어가지 않는다. | 2026년 시점에 React 카나리/실험 |
| **Custom Hook (커스텀 훅)** | `use`로 시작하는 함수로, 다른 Hook을 호출해 상태 로직을 재사용 가능하게 한 것. 상태 자체가 아니라 로직을 공유한다. | 호출마다 독립된 state |
| **`useImperativeHandle`** | 부모에게 노출할 ref API를 제한할 때 사용. | 자식의 내부 구현 은폐 |
| **`flushSync`** | state 갱신을 동기적으로 즉시 반영해 그 직후 DOM에 접근 가능하게 한다. | `react-dom`에서 import |
| **`useSyncExternalStore`** | React 외부에 있는 store를 안전하게 구독하기 위한 공식 API. | 직접 effect로 구독하는 패턴의 대체 |
| **`useMemo`** | 비싼 계산 결과를 캐싱한다. | Effect로 파생값을 보관하는 패턴 대체 |

### 1.3 멘탈 모델 핵심 어휘

- **선언형(Declarative) UI**: "어떻게 바꿀지"가 아니라 "각 상태에서 어떤 모습이어야 하는지"를 기술한다. React의 핵심 패러다임.
- **명령형(Imperative) UI**: 단계별로 DOM을 직접 조작하는 방식. 복잡도가 커지면 깨지기 쉽다.
- **Synchronization (동기화)**: Effect의 본질. 라이프사이클 이벤트가 아니라 "외부 시스템을 현재 props·state에 맞춘다"는 관점.
- **Server State / Client (UI) State**: Kent C. Dodds가 강조하는 구분. 서버에서 온 데이터(캐시) vs UI 자체의 일시적 상태. 같은 도구로 다루면 안 된다.
- **Colocation (콜로케이션)**: 상태를 그것을 쓰는 곳 가까이 둔다. 끌어올렸다가 필요 없어지면 다시 내린다(Lift, then Drop).

---

## 2. 주요 관점

### 2.1 React 팀의 공식 멘탈 모델

1. **상태는 UI를 결정하는 함수의 입력이다 (`UI = f(state)`).**
   - 디자이너가 "타이핑 중", "전송 중", "성공", "실패" 화면을 그리듯이, 모든 시각 상태를 먼저 식별하고 그 사이를 잇는 트리거를 모델링한다.

2. **렌더는 스냅샷이다.**
   - 매 렌더는 자기 자신의 props/state/effect를 캡처한다. 함수 안의 변수가 "나중에 바뀐다"는 직관은 틀렸다.

3. **state는 트리 위치에 묶인다.**
   - 같은 자리·같은 타입이면 보존, 다른 타입이면 파괴. `key`로 식별을 강제 변경할 수 있다.

4. **Effect는 "외부 시스템과의 동기화"다.**
   - 라이프사이클(mount/update/unmount)이 아니라 "동기화 시작 ↔ 동기화 중지"의 사이클로 생각한다. 그래서 cleanup이 본질적으로 중요하다.

5. **Ref는 escape hatch다.**
   - 평소엔 React 데이터 흐름 안에 머무르고, 외부 세계(브라우저 API, 비-React 라이브러리, 타이머 ID 등)와 만나는 경계에서만 꺼낸다.

6. **"You might not need an Effect."**
   - 렌더 중에 계산 가능한 값은 Effect로 동기화하지 않는다. 사용자 이벤트로 일어나는 일은 Effect가 아니라 이벤트 핸들러로 처리한다. Dan Abramov가 메타 내부에서 샘플링한 결과 약 46%의 useEffect가 불필요했다(HN 토론).

### 2.2 Dan Abramov 관점 (overreacted.io)

- "Every render has its own props, state, and effects." 함수 컴포넌트의 클로저는 마법이 아니라 그저 그 시점의 값을 기억한 것뿐이다.
- "It's all about the destination, not the journey." Effect는 "언제 일어나는가"가 아니라 "지금 어떤 상태와 동기화되어야 하는가"를 기술한다.
- "useReducer is the cheat mode of Hooks." 의존성 사슬을 끊는 수단 — 현재 state를 직접 읽지 않고 dispatch로 의도만 전달한다.
- 의존성 배열은 hack이 아니라 동기화 계약이다. 거짓말하면(생략하면) 즉시 stale closure 버그가 생긴다.

### 2.3 Kent C. Dodds 관점

- **"React IS your state management library."** 외부 라이브러리에 너무 빨리 손대지 마라.
- **Server cache state vs UI state**: 합쳐서 다루는 순간 잘못된 도구로 잘못된 문제를 푼다. 서버 캐시는 `react-query`/TanStack Query, UI 상태는 `useState`/`useReducer`/Context.
- **Lift, then Drop**: 필요할 때만 끌어올리고, 더 이상 필요 없어지면 다시 내려라.
- Context는 prop drilling이 진짜 고통일 때만 쓴다. Provider를 트리 깊숙이 두어 영향 범위를 좁혀라(콜로케이션).
- "Don't reach for context too soon!"

### 2.4 Robin Wieruch 관점

- 커스텀 훅은 **반복되는 패턴이 보일 때** 추출한다. 미리 추출하지 마라.
- 다중 값 반환은 객체보다 **배열**이 좋다 — 호출자가 자유롭게 이름 붙일 수 있어서다.
- `use` 접두사 규칙은 강제다. Hook을 호출하지 않는 함수는 `use`를 붙이지 마라.

### 2.5 커뮤니티 비판적 관점 (Hacker News, Reddit)

- "이렇게 긴 문서로 sharp edges를 설명해야 한다면 API 설계가 잘못된 것이다." (HN, billllll)
- linter exhaustive-deps 규칙은 코딩 표준이 아닌 애플리케이션 버그를 강제한다는 비판도 있다(davedx).
- 일부는 Solid.js로 이주하면서 "useEffect 패러다임 자체가 짐"이라고 주장한다.
- **반론**: useEffect는 "앱과 외부 세계 사이의 경계"여야 하며, 도메인 로직이 effect로 옮겨가면 문제가 생긴다(brundolf). 즉 공식 가이드와 실제 사용 패턴 사이의 간극이 핵심 갈등이다.

### 2.6 한국 커뮤니티 신호

- velog/우아한형제들/네이버 D2에서 가장 자주 언급되는 고통: useEffect 무한 루프, 의존성 배열에 객체/배열 넣고 매 렌더마다 재실행, ref와 state 구분 모호.
- "useEffect 남용하지 말자" (HyunGyu) — 암묵적 제어 흐름이 디버깅을 어렵게 만든다는 한국어 정리가 폭넓게 공감대를 얻고 있다.
- "useState vs useRef" 비교 글에서 동일한 입력 폼을 21회 렌더 vs 2회 렌더로 정량 비교한 사례가 있다(velog/skawnkk). 다만 동적 뷰가 필요한 경우엔 ref가 답이 아니라는 점도 함께 지적된다.

---

## 3. 사례 / 코드 패턴

> 이 절은 챕터 예제의 씨앗이다. 각 패턴은 *이름 / 푸는 문제 / 최소 예제 / 흔한 변형* 형태로 정리한다.

### 3.1 다섯 단계로 상태 모델링하기 (Five-Step State Modeling)
- **문제**: 명령형으로 disable/show/hide를 토글하다 보면 상태가 폭발한다.
- **예제**: 퀴즈 폼에서 `'typing' | 'submitting' | 'success'` 한 변수로 모든 분기를 표현.
```js
const [answer, setAnswer] = useState('');
const [error, setError] = useState(null);
const [status, setStatus] = useState('typing');
```
- **변형**: 상태 머신 라이브러리(XState) 도입, 또는 더 단순하게는 enum-like 문자열 + boolean 파생값.

### 3.2 파생값은 렌더 중에 계산하기 (Derive, Don't Store)
- **문제**: `firstName`, `lastName`, `fullName`을 모두 state로 들고 있다가 동기화 실패.
- **해결**:
```js
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const fullName = firstName + ' ' + lastName; // 렌더 중에 계산
```
- **변형**: 비싼 계산이라면 `useMemo`로 캐싱.

### 3.3 모순 가능한 boolean 합치기 (Status Enum)
- **문제**: `isSending`, `isSent` 두 boolean이 동시에 true가 되는 불가능 상태가 발생.
- **해결**: `status: 'typing' | 'sending' | 'sent'` 하나로 합치고 필요 시 파생.

### 3.4 선택은 ID/Index로 저장 (Store ID, Not Object)
- **문제**: 선택된 객체 자체를 state에 두면 원본 리스트가 갱신될 때 stale 참조가 된다.
- **해결**:
```js
const [items, setItems] = useState([...]);
const [selectedId, setSelectedId] = useState(0);
const selectedItem = items.find(item => item.id === selectedId);
```
- **변형**: 다중 선택은 `Set<id>` 사용.

### 3.5 깊이 중첩된 상태 평탄화 (Normalize)
- **문제**: 트리 형태 데이터를 그대로 state에 두면 갱신이 끔찍하다.
- **해결**: ID를 키로 하는 lookup table + `childIds: number[]`로 변환.

### 3.6 상태 끌어올리기 (Lifting State Up)
- **문제**: 두 패널이 서로의 열림/닫힘을 알아야 하는 아코디언.
- **해결**: 부모에 `activeIndex`를 두고 `isActive`, `onShow`를 props로 내림.
- **변형**: 동기화된 인풋(같은 `value`/`onChange`로 두 인풋 묶기), 필터된 리스트(`query`만 부모에 두고 결과는 파생).

### 3.7 `key`로 state 리셋 (Resetting via Key)
- **문제**: 채팅 상대를 바꿔도 입력 중이던 초고가 남는다.
- **해결**: `<Chat key={contact.id} contact={contact} />` — key가 바뀌면 React가 새 컴포넌트로 인식해 state 초기화.
- **변형**: prop이 바뀔 때 일부만 리셋해야 한다면 `[prevX, setPrevX] = useState(x); if (x !== prevX) { setPrevX(x); setSelection(null); }` — 렌더 중 set 패턴.

### 3.8 useReducer로 상태 로직 모으기
- **문제**: 이벤트 핸들러마다 `setTasks([...tasks, ...])`가 흩어져 있어 디버깅이 어렵다.
- **해결**: `tasksReducer(tasks, action)`에 모든 변경을 모으고, 핸들러는 `dispatch({ type: 'added', ... })`만 한다.
- **변형**: `useImmerReducer`로 mutate 스타일 코드 작성.

### 3.9 Context로 prop drilling 끊기
- **문제**: `Section` → `Post` → `Heading`으로 level을 6단계 내려야 한다.
- **해결**: `LevelContext` 만들고, `Section`이 자기 위 level + 1을 Provider로 내려준다. `Heading`이 `useContext`로 직접 읽는다.
- **변형**: 테마, 로그인 사용자, 라우트 등.

### 3.10 Reducer + Context 조합 (Scaling Pattern)
- **문제**: 큰 앱에서 reducer state를 깊은 자식까지 보내야 하고, dispatch도 마찬가지.
- **해결**: `TasksContext`(state)와 `TasksDispatchContext`(dispatch)를 분리하고 `TasksProvider`로 감싸 `useTasks()`, `useTasksDispatch()` 커스텀 훅으로 노출.

### 3.11 Ref로 리렌더 없는 값 보관 (debounce timer ID)
- **문제**: 디바운스 버튼을 여러 개 만들었더니 모듈 스코프 변수 `timeoutID`가 충돌.
- **해결**: 컴포넌트마다 `const timeoutRef = useRef(null);`로 격리.

### 3.12 DOM Ref로 focus/scroll/measure
- **문제**: 입력란에 자동 포커스, 리스트 끝으로 스크롤 등.
- **해결**: `<input ref={inputRef} />` → `inputRef.current.focus()`. React 19부터 함수 컴포넌트도 `ref`를 prop처럼 받을 수 있다.
- **변형**: 동적 리스트는 ref callback + Map; 측정 후 즉시 스크롤하려면 `flushSync`로 동기 갱신.

### 3.13 Effect로 외부 시스템 동기화 (chat connection)
- **문제**: 방을 바꾸면 이전 연결을 끊고 새 연결을 시작해야 한다.
- **해결**:
```js
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);
```
- **포인트**: cleanup이 의무. 개발 모드에서는 두 번 실행되며 재동기화 안전성을 강제 검증한다.

### 3.14 Effect 안에서 fetch + race condition 방지
- **문제**: 빠르게 query를 바꾸면 늦게 도착한 응답이 최신 응답을 덮어쓴다.
- **해결**: `let ignore = false; ... return () => { ignore = true; }` 패턴.
- **변형**: 실무에선 TanStack Query / SWR로 옮기는 것이 표준.

### 3.15 useEffectEvent로 비반응형 코드 분리
- **문제**: theme이 바뀌어도 chat 연결을 다시 맺지 말아야 하지만, theme을 dependency에 넣자니 reconnect가 발생.
- **해결**:
```js
const onConnected = useEffectEvent(() => {
  showNotification('Connected!', theme);
});
useEffect(() => {
  const c = createConnection(serverUrl, roomId);
  c.on('connected', () => onConnected());
  c.connect();
  return () => c.disconnect();
}, [roomId]);
```

### 3.16 의존성에서 객체/함수 제거 (Move Inside)
- **문제**: `const options = { serverUrl, roomId }`를 dependency로 넣으면 매 렌더마다 객체가 새로 만들어져 effect가 매번 재실행.
- **해결**: 객체 생성을 effect 내부로 옮기거나, 원시값(`roomId`, `serverUrl`)을 의존성에 넣는다.

### 3.17 setState 함수형 업데이트로 의존성 끊기
- **문제**: `setMessages([...messages, m])`은 messages가 dependency가 되어 재실행 유발.
- **해결**: `setMessages(prev => [...prev, m])` — 이제 messages는 dependency 아님.

### 3.18 useSyncExternalStore로 브라우저 API 구독
- **문제**: `online/offline` 이벤트를 effect로 구독하면 SSR/concurrent 환경에서 미묘한 버그.
- **해결**:
```js
function useOnlineStatus() {
  return useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
}
```

### 3.19 Custom Hook으로 로직 재사용 (useFormInput, useChatRoom, useDelayedValue 등)
- **문제**: 같은 effect/state 패턴이 컴포넌트마다 반복.
- **해결**: `use` 접두사 함수로 추출. **상태가 아니라 로직이 공유된다** — 호출마다 독립된 state.
```js
function useFormInput(initialValue) {
  const [value, setValue] = useState(initialValue);
  return { value, onChange: e => setValue(e.target.value) };
}
```

### 3.20 useImperativeHandle로 ref API 제한
- **문제**: 자식 컴포넌트의 모든 DOM API를 노출하고 싶지 않다.
- **해결**:
```js
function MyInput({ ref }) {
  const realRef = useRef(null);
  useImperativeHandle(ref, () => ({
    focus() { realRef.current.focus(); }
  }));
  return <input ref={realRef} />;
}
```

### 3.21 flushSync로 동기 DOM 업데이트
- **문제**: 새 todo를 추가하고 즉시 그 항목으로 스크롤하고 싶은데, setState가 비동기여서 ref가 아직 갱신 전.
- **해결**:
```js
flushSync(() => setTodos([...todos, newTodo]));
listRef.current.lastChild.scrollIntoView();
```

---

## 4. 흔한 실수 & 안티패턴

| # | 안티패턴 | 왜 나쁜가 | 올바른 해법 |
|---|---|---|---|
| 1 | 파생값을 state로 보관 (`fullName`을 useState로) | 동기화 실패 발생 가능, set을 빠뜨리면 stale | 렌더 중에 계산 |
| 2 | 비싼 계산을 effect에서 하고 결과를 state에 저장 | 두 번 렌더, 계산-set-rerender 사이클 | `useMemo` |
| 3 | prop이 바뀔 때 effect로 state 리셋 | 한 박자 늦은 깜빡임, 코드 분산 | `key` prop, 또는 렌더 중 `if (x !== prev) setX(...)` |
| 4 | 사용자 이벤트로 일어나는 일을 effect에 넣기 (구매, POST) | 컴포넌트가 마운트되거나 prop 바뀔 때마다 의도 없이 발사 | 이벤트 핸들러로 이동 |
| 5 | 여러 effect를 cascading하게 연결 (A → state → B → state → A) | 무한 루프, 디버깅 지옥 | 한 핸들러 안에서 모두 계산 |
| 6 | 앱 초기화를 effect로 (개발 모드에서 두 번 실행) | 인증 토큰 두 번 로드 같은 부작용 | 모듈 최상단 코드 또는 `didInit` 가드 |
| 7 | 자식 → 부모 통신을 effect로 (`useEffect(() => onChange(value))`) | 두 번 렌더, 무한 루프 가능 | 같은 이벤트에서 부모 상태도 함께 갱신, 또는 fully controlled |
| 8 | 의존성 배열에 객체/함수 넣기 | 매 렌더마다 참조가 새로워져 effect 폭주 | 객체를 effect 안에서 생성, 원시값 분해, `useCallback` |
| 9 | linter `exhaustive-deps` suppress | stale closure 보장 | 코드를 바꿔서 의존성을 진짜로 없애라 |
| 10 | useState로 prop 미러링 (`useState(props.color)`) | prop 변경이 무시됨 | prop 그대로 사용, 또는 의도라면 `initialColor` 네이밍 |
| 11 | 컴포넌트 안에서 컴포넌트 정의 | 매 렌더마다 새 타입 → 모든 state 파괴 | 최상단 또는 모듈 스코프에 정의 |
| 12 | 깊이 중첩된 state를 그대로 다루기 | 갱신 시 spread 체인 폭발 | 정규화, 또는 Immer |
| 13 | 렌더 중에 ref 읽기/쓰기 | 예측 불가, commit 전엔 null | 이벤트 핸들러나 effect에서만 |
| 14 | React가 관리하는 DOM 자식을 직접 추가/제거 | React 재조정과 충돌 | React 데이터 흐름으로 표현, 정말 필요하면 항상 비어있는 영역에만 |
| 15 | 의존성 누락으로 stale state 읽기 | 무한 디버깅 | dependency 정직하게, 못 빼면 함수형 setState나 `useEffectEvent` |
| 16 | useEffect로 fetch하고 cleanup ignore 안 두기 | race condition으로 오래된 응답이 최신을 덮음 | `let ignore = false; ... return () => { ignore = true; }` |
| 17 | 외부 store 수동 구독 (addEventListener를 effect로) | concurrent / SSR에서 tearing | `useSyncExternalStore` |
| 18 | 모든 state를 Redux/Context에 몰아넣기 | 모든 변경이 트리 전체 리렌더, 콜로케이션 상실 | 가까운 곳에 두고, 정말 글로벌인 것만 위로 |
| 19 | 서버 캐시를 useState/Context로 다루기 | 캐시 무효화·재시도·낙관적 업데이트 직접 구현 → 항상 깨짐 | TanStack Query / SWR |
| 20 | `useEffectEvent`를 다른 컴포넌트에 넘기거나 dependency에 넣기 | 설계 의도 위반, 미묘한 버그 | effect 내부에서만 호출 |
| 21 | `key`로 array index 사용 | 항목 순서 변경 시 state가 엉뚱한 곳에 묶임 | 안정된 ID |

---

## 5. 논쟁점

### 5.1 Context vs Redux vs Zustand vs Jotai
- **2026 시점 대세**: Zustand가 작은-중간 앱의 기본값(약 1.2KB, ~20M weekly downloads). Redux Toolkit은 엔터프라이즈에서 유지. Context는 "자주 안 변하는 글로벌 데이터"에 한정해 쓰는 분위기.
- **Kent Dodds 입장**: 대부분의 앱은 Context + useReducer로 충분. Redux의 인기는 reducer 패턴이 아니라 prop drilling 해결이었다.
- **반론**: Context는 value가 바뀌면 모든 consumer가 리렌더 — 빈번히 바뀌는 state라면 Zustand/Jotai의 selective subscription이 낫다.
- **결론적 휴리스틱**: 안 변하는 것 → Context, 작은 앱의 변하는 것 → Zustand, 대규모/팀 표준 필요 → Redux Toolkit, 원자 단위 의존성 → Jotai.

### 5.2 Server State는 별개인가?
- 거의 합의 형성: **별개다.** 서버 상태는 비동기, 공유, 외부에서 변경됨, 캐시 무효화 필요. UI 상태와는 다른 도구가 필요.
- TanStack Query(13.4KB) vs SWR(4.2KB) — 기능 vs 번들 크기 트레이드오프.
- 이걸 모르고 Redux에 fetch 결과를 다 때려박으면 reinventing query cache — 거의 항상 깨진다.

### 5.3 useEffect 남용 vs "you might not need an effect"
- 메타 내부 표본에서 약 46% 불필요(Dan Abramov, HN). 즉 react-dev조차 자주 잘못 쓴다.
- 비판: 이런 가이드 문서가 길게 필요하다는 사실 자체가 API 설계의 흠이다.
- 옹호: useEffect는 "외부 시스템과의 경계"용이며, 도메인 로직이 effect로 흘러들어간 게 문제의 근원이다.
- 실무 영향: 한 80K LOC 코드베이스에서 한 달 28개 버그 중 7개가 hooks 의존성 관련(HN/batmansmk).

### 5.4 Ref의 정당한 사용 vs 회피
- **정당**: focus/scroll/measure, 비-React 위젯 제어, 타이머/연결 ID 보관, 이전 값 추적.
- **회피해야**: 렌더 결과에 영향 주는 값을 ref에 두기, "리렌더 줄이려고" useState 대신 useRef.
- 한국 커뮤니티 정량 비교: 입력 폼에서 ref 21회 → 2회 렌더로 줄였지만, 동적 검색 제안 같은 경우엔 그대로 useState여야 한다는 단서가 자주 따라붙는다.

### 5.5 useReducer vs useState 경계선
- "여러 핸들러에 흩어진 비슷한 갱신 + 디버깅 가치"가 임계점.
- 작은 폼은 useState가 더 명확. 협업 가능한 task list/cart/wizard는 reducer가 깔끔.
- 반대로 reducer가 너무 잘게 쪼개진 action을 만들면 useState만 못한 경우도 자주 본다 — "사용자 의도 단위로" 액션을 작성해야 한다.

### 5.6 useEffectEvent의 위상
- 2026년 시점에도 실험적/카나리. linter silencer로 쓰기에는 의도와 다름.
- 일부 개발자는 "근본 문제를 우회하는 패치"라고 본다(HN). 다른 이들은 "reactive vs non-reactive 분리는 필요했던 어휘"라며 환영.

### 5.7 Custom Hook은 언제 추출하나
- Wieruch: "두 번 이상 같은 패턴이 보이면."
- 공식 문서: `useMount` 같은 라이프사이클 래퍼는 만들지 마라 — Effect의 동기화 의미를 흐린다.
- 추출보다 먼저 시도해야 할 것: 컴포넌트 합성, JSX를 children으로 넘기기.

---

## 6. 연습 문제 시드 (20+개)

### Basic
1. (Managing State) `'idle' | 'loading' | 'error' | 'success'` 단일 enum으로 데이터 페치 UI를 모델링하라. 두 boolean이 모순될 가능성을 제거.
2. (Managing State) `firstName`/`lastName`/`fullName` 폼에서 redundant state를 제거하고 fullName을 파생값으로 바꿔라.
3. (Managing State) Counter 두 개를 부모 컴포넌트에서 동기화시켜라(같은 값을 공유).
4. (Managing State) 아코디언에서 한 번에 한 패널만 열리게 만들어라 — `activeIndex` 끌어올리기.
5. (Escape Hatches) 입력란에 자동 focus가 가도록 mount 시 ref로 focus를 호출하라.
6. (Escape Hatches) `setInterval`로 타이머를 만들고 cleanup이 누락된 코드를 고쳐라.
7. (Escape Hatches) 디바운스 버튼에서 모듈 스코프 변수 대신 `useRef`로 격리시켜라.

### Intermediate
8. (Managing State) 채팅 앱에서 상대를 바꾸면 작성 중이던 초고가 자동으로 비워지도록 `key`로 리셋하라.
9. (Managing State) Task List를 useState에서 useReducer로 마이그레이션하라. action은 사용자 의도 단위로.
10. (Managing State) 깊이 4단계 중첩된 여행 계획 데이터를 ID 룩업 테이블로 평탄화하고 "방문 완료 토글" 핸들러를 작성하라.
11. (Managing State) 다중 선택 리스트를 `Set<id>`로 구현하라. 큰 리스트에서도 성능이 나오도록.
12. (Managing State) Heading 레벨을 Section 깊이에 따라 자동 증가시키는 LevelContext를 구현하라.
13. (Managing State) reducer + 두 개의 분리된 context(state/dispatch)로 Tasks 앱을 재구성하고 `useTasks`, `useTasksDispatch` 커스텀 훅을 노출하라.
14. (Escape Hatches) chat connection effect에 cleanup을 추가하고 개발 모드 더블 인보케이션 때 발생하는 로그를 분석하라.
15. (Escape Hatches) useEffect로 검색 결과를 fetch하되 race condition 방지를 위해 `ignore` 플래그를 도입하라.
16. (Escape Hatches) `usePointerPosition`과 `useDelayedValue`를 합쳐서 마우스를 따라오는 잔상 효과를 구현하라.
17. (Escape Hatches) `useOnlineStatus`를 직접 effect 구현 → `useSyncExternalStore` 구현으로 리팩터링하라.

### Challenging
18. (Managing State) 폼 위저드(3단계, 뒤로 가기 가능)를 useReducer로 모델링하라. 단계 간 데이터는 보존되지만 "처음부터" 버튼에서는 깔끔히 리셋되어야 한다.
19. (Managing State) 댓글 트리(중첩된 답글)를 정규화된 형태로 다루고, 삭제 시 자식까지 일관되게 제거하라.
20. (Escape Hatches) `flushSync`를 사용해 새 메시지 추가 후 즉시 그 메시지로 스크롤되도록 채팅 UI를 만들어라.
21. (Escape Hatches) `useEffectEvent`로 `theme` 변경 시 reconnect 없이 알림 메시지에 최신 theme이 반영되도록 chat을 구현하라.
22. (Escape Hatches) 외부 비-React 카메라 위젯을 React에서 `isRecording` props에 따라 시작/중지하도록 제어하라(객체 dependency 함정 주의).
23. (Escape Hatches) 커스텀 훅 `useFetch(url)`을 작성하라 — race condition, abort, 로딩/에러 상태 모두 다루고, 마지막에는 "이걸 쓸 바엔 TanStack Query를 써야 하는 이유"를 토론.
24. (Escape Hatches) `useImperativeHandle`로 자식 모달 컴포넌트가 부모에게 `open()`/`close()`만 노출하도록 만들어라. 내부 ref와 어떻게 분리하나?
25. (통합) 작은 칸반 앱: column 추가/삭제, card 드래그, 서버 동기화. UI 상태는 useReducer + Context, 서버 상태는 별도 처리(개념 설계만이라도)로 분리해 작성하라.

---

## 7. 참고문헌

### React.dev 공식 문서
- Managing State 허브: https://react.dev/learn/managing-state
- Reacting to Input with State: https://react.dev/learn/reacting-to-input-with-state
- Choosing the State Structure: https://react.dev/learn/choosing-the-state-structure
- Sharing State Between Components: https://react.dev/learn/sharing-state-between-components
- Preserving and Resetting State: https://react.dev/learn/preserving-and-resetting-state
- Extracting State Logic into a Reducer: https://react.dev/learn/extracting-state-logic-into-a-reducer
- Passing Data Deeply with Context: https://react.dev/learn/passing-data-deeply-with-context
- Scaling Up with Reducer and Context: https://react.dev/learn/scaling-up-with-reducer-and-context
- Escape Hatches 허브: https://react.dev/learn/escape-hatches
- Referencing Values with Refs: https://react.dev/learn/referencing-values-with-refs
- Manipulating the DOM with Refs: https://react.dev/learn/manipulating-the-dom-with-refs
- Synchronizing with Effects: https://react.dev/learn/synchronizing-with-effects
- You Might Not Need an Effect: https://react.dev/learn/you-might-not-need-an-effect
- Lifecycle of Reactive Effects: https://react.dev/learn/lifecycle-of-reactive-effects
- Separating Events from Effects: https://react.dev/learn/separating-events-from-effects
- Removing Effect Dependencies: https://react.dev/learn/removing-effect-dependencies
- Reusing Logic with Custom Hooks: https://react.dev/learn/reusing-logic-with-custom-hooks
- 모두 2026-04-26 기준 접근.

### 권위자 블로그
- Dan Abramov, "A Complete Guide to useEffect": https://overreacted.io/a-complete-guide-to-useeffect/
- Dan Abramov, "useEffect 완벽 가이드 (한국어 번역)": https://rinae.dev/posts/a-complete-guide-to-useeffect-ko/
- Kent C. Dodds, "Application State Management with React": https://kentcdodds.com/blog/application-state-management-with-react
- Kent C. Dodds, "How to Test Custom React Hooks": https://kentcdodds.com/blog/how-to-test-custom-react-hooks
- Kent C. Dodds, "The State Reducer Pattern with React Hooks": https://kentcdodds.com/blog/the-state-reducer-pattern-with-react-hooks
- Robin Wieruch, "React: How to create a Custom Hook": https://www.robinwieruch.de/react-custom-hook/
- Robin Wieruch, "React Hooks Tutorial": https://www.robinwieruch.de/react-hooks/

### 한국어 커뮤니티
- "useEffect를 남용하지 말자" (HyunGyu): https://gusrb3164.github.io/web/2021/12/29/less-use-useeffect/
- "useRef의 새로운 발견 (useState와 비교)" (velog/skawnkk): https://velog.io/@skawnkk/useState-vs-useRef
- "React useEffect 무한 루프 탈출하기" (velog/summereuna): https://velog.io/@summereuna/리액트-useEffect-무한-루프-탈출하기
- "React useEffect 실수 TOP3 정리 + useEffectEvent" (beam307, 2026): https://beam307.github.io/2026/02/08/use-effect/
- "useEffect hook에 대해 더 알아보자" (Yohan): https://yohanpro.com/posts/react/use-effect/
- "React.useEffect — 일반적인 문제와 해결" (freeCodeCamp 한국어): https://www.freecodecamp.org/korean/news/react-useeffect-hug-hook-ilbanjeogin-munjewa-geu-haegyeol-bangbeob/
- "useState vs useRef" (theteams/휴먼스케이프): https://www.theteams.kr/teams/6500/post/73410
- "useRef는 처음이라 — 개념부터 활용 예시까지" (mnxmnz): https://mnxmnz.github.io/react/what-is-use-ref/
- "리액트 useReducer로 상태 업데이트 로직 분리하기" (vlpt 김민준): https://react.vlpt.us/basic/20-useReducer.html

### 영어 커뮤니티 / 산업
- Hacker News, "You Might Not Need an Effect" 토론: https://news.ycombinator.com/item?id=35270877
- Hacker News, "Common Beginner Mistakes with React": https://news.ycombinator.com/item?id=35108672
- TanStack Query 공식: "Does TanStack Query replace Redux/MobX?": https://tanstack.com/query/v4/docs/framework/react/guides/does-this-replace-client-state
- "State of React State Management in 2026" (PkgPulse): https://www.pkgpulse.com/blog/state-of-react-state-management-2026
- "Redux vs Zustand vs Context API in 2026" (Sparkle Web/Medium): https://medium.com/@sparklewebhelp/redux-vs-zustand-vs-context-api-in-2026-7f90a2dc3439
- "React State: Redux vs Zustand vs Jotai (2026)" (inhaq): https://inhaq.com/blog/react-state-management-2026-redux-vs-zustand-vs-jotai.html
- "TanStack Query vs SWR vs Apollo Client 2026" (PkgPulse): https://www.pkgpulse.com/blog/tanstack-query-vs-swr-vs-apollo-2026
- "React Query vs SWR in 2026" (dev.to/whoffagents): https://dev.to/whoffagents/react-query-vs-swr-in-2026-what-i-actually-use-and-why-3362

---

## 8. 리서치 한계 (커버하지 못한 영역)

- **학술 자료**: 정식 paper-researcher 에이전트를 띄우지 못했다. Flux/Elm architecture, FRP(Functional Reactive Programming), unidirectional data flow에 관한 학술 인용은 본 문서에 들어가지 않았다. 입문서 스타일이라면 큰 문제가 없으나, 책 서두의 "상태 관리 사상사" 챕터에서 Elm/Flux 인용이 필요해질 수 있다.
- **Reddit r/reactjs 직접 발췌**: site:reddit.com 검색이 빈 결과를 반환했다. velog, HN, dev.to, 권위자 블로그로 보강했지만 Reddit 토론의 "오늘 우리가 실제 삽질하는 예시"는 더 가져오면 좋다.
- **GitHub Discussions / 한국 기업 블로그(우아한형제들, 카카오, 네이버 D2, 토스)**: 키워드 검색 결과는 있었지만 본 라운드에선 직접 페이지를 fetch하지 못했다. 챕터 작성 시 사례가 모자라면 보강 필요.
- **코드 인터랙티브 예제**: 본 문서는 텍스트 기반이라 sandbox 링크를 직접 임베드하지 못했다. 챕터 작성 시 React 공식 문서의 sandbox 예제로 이어지는 링크나 codesandbox를 추가하면 학습 효과가 커진다.
- **React 19 이후 변화**: ref가 prop으로 직접 받을 수 있게 된 변화, `use(promise)` API, Server Components와 state의 관계 — 본 문서는 React 19 변화를 부분적으로만 다뤘다. 책 출간 시점 React 버전 합의 후 보강 필요.
- **TypeScript 타이핑**: 모든 예제를 JS로 적었다. 중급 독자라 TS 타입은 챕터 안에서 별도 박스로 다루면 좋다(특히 `useReducer` 액션 유니온, `useRef<HTMLInputElement | null>`, `Dispatch<Action>`).
