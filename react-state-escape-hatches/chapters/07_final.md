# 7장. 앱이 커져서 상태가 발에 채일 때 — Reducer + Context

6장에서 Context의 매력에 단단히 빠진 동료 한 명이 있다고 해보자. Heading 레벨을 자동으로 따라가게 만드는 예제를 보고 감탄한 그는, 마침내 자기 회사에서 운영하는 칸반 보드 앱에도 Context를 도입했다. 이전까지는 `tasks` 배열과 `dispatch`를 6단계 컴포넌트 트리로 줄줄이 내려보내는 코드였다. 답답했을 만도 하다. 그래서 그는 시원하게 한 번에 정리했다.

```tsx
// 처음엔 이렇게 시작했다 — 매끈해 보인다
const TasksContext = createContext(null);

function TasksProvider({ children }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  return (
    <TasksContext value={{ tasks, dispatch }}>
      {children}
    </TasksContext>
  );
}
```

코드는 단숨에 짧아졌다. 깊은 자식까지 props가 흘러내려가던 자리는 깔끔히 사라졌고, 어떤 컴포넌트든 `useContext(TasksContext)` 한 줄이면 `tasks`와 `dispatch`를 받아 쓸 수 있게 됐다. 그는 만족스럽게 PR을 올렸고, QA에서도 동작 자체에는 문제가 없었다. 그런데 며칠 뒤, 디자이너가 무심코 한 마디를 던졌다. "이상하게 카드를 하나 토글할 때마다 헤더에 있는 시계 컴포넌트가 깜빡거려요." 시계는 `tasks`와는 아무 상관이 없는 컴포넌트다. 단지 `TasksProvider` 안쪽에 들어 있을 뿐인데, 왜 같이 깜빡일까?

이 장의 출발점은 바로 이 의문이다. **5장에서 배운 reducer**가 흩어진 변경 로직을 한 곳으로 모아주는 도구라면, **6장에서 배운 Context**는 그 결과를 깊은 자식까지 한 번에 흘려보내는 통로다. 이 둘이 만나는 자리가 우리가 흔히 말하는 "Reducer + Context 패턴"이고, 작은 토이 앱이 점점 진짜 제품 규모로 커질 때 가장 먼저 손이 가는 구조이기도 하다. 하지만 두 도구를 그냥 합쳐놓기만 해서는 안 된다는 것을 우리는 곧 보게 된다. 자칫하면 **모든 변경이 트리 전체를 흔드는** 비극이 따라온다. 이 비극을 어떻게 피할지, 그리고 어디까지가 이 패턴의 영토인지, 그 경계를 함께 그어보자.

## 5장과 6장이 만나는 자리

5장 끝자락에서 우리는 Tasks 앱의 `setTasks` 호출들을 reducer로 모아 정리했다. 흩어져 있던 핸들러들은 `dispatch({ type: 'added', ... })`처럼 **사용자 의도** 단위로 깨끗해졌고, 무엇이 어떻게 바뀌는지를 한 파일에서 다 읽을 수 있게 됐다. 그 자체로 큰 진전이다. 하지만 진짜 앱이라면 이 reducer로 만들어진 `tasks`는 한 컴포넌트만 쓰지 않는다. 사이드바의 카운트, 헤더의 진행률, 본문의 카드 리스트, 상세 패널의 편집 폼 — 적게 잡아도 네 자리에서 같은 데이터를 읽고 같은 dispatch를 호출하고 싶어진다.

```tsx
// 5장의 결과물 — props로 다 내려보내는 그림
function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  return (
    <Layout>
      <Sidebar tasks={tasks} dispatch={dispatch} />
      <Main tasks={tasks} dispatch={dispatch} />
      <Header tasks={tasks} dispatch={dispatch} />
    </Layout>
  );
}
```

이 코드는 정직하다. 그리고 트리가 두세 단계 깊지 않다면 이대로 두는 편이 낫다. 문제는 `Main` 안에 `TaskBoard`가 있고, 그 안에 `TaskColumn`이, 그 안에 `TaskCard`가, 그 안에 `TaskCheckbox`가 있을 때다. 마지막 체크박스 하나를 위해 `tasks`와 `dispatch`를 다섯 단계 내려보내는 건 — 솔직히 말해 — 번거롭다. 매 단계마다 props 타입을 늘리고, 중간 컴포넌트들은 자기가 쓰지도 않는 값을 단지 통과시키기 위해 받아야 한다. 6장에서 우리가 "props drilling이 진짜 고통일 때만 Context를 꺼내자"고 약속했던 그 자리가, 바로 여기다.

그럼 자연스럽게 이런 그림이 떠오른다. reducer는 어딘가 위쪽 한 곳에 두고, 그 결과인 `tasks`와 dispatch를 Context에 실어 트리 어디서든 읽게 만들자. 이 발상은 옳다. 다만 **어떻게 실어 보내느냐**에 따라 결과가 천지 차이라는 점이 우리가 이번 장에서 짚을 핵심이다.

## 단순 합성의 함정 — `value={{ state, dispatch }}`가 부르는 리렌더 폭발

가장 직관적인 합성은 6장에서 본 동료의 코드와 같다. 하나의 Context를 만들고, `value`로 객체 하나를 통째로 내려보낸다.

```tsx
type TasksValue = {
  tasks: Task[];
  dispatch: React.Dispatch<TasksAction>;
};

const TasksContext = createContext<TasksValue | null>(null);

export function TasksProvider({ children }: { children: React.ReactNode }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  // 매 렌더마다 새로운 객체 리터럴이 만들어진다
  return (
    <TasksContext value={{ tasks, dispatch }}>
      {children}
    </TasksContext>
  );
}
```

읽기는 깔끔하다. 자식 컴포넌트는 이렇게 쓴다.

```tsx
function TaskCheckbox({ id }: { id: string }) {
  const { tasks, dispatch } = useContext(TasksContext)!;
  const task = tasks.find(t => t.id === id)!;
  return (
    <input
      type="checkbox"
      checked={task.done}
      onChange={() => dispatch({ type: 'toggled', id })}
    />
  );
}
```

문제가 뭘까? 두 가지가 동시에 일어난다.

첫째, `value={{ tasks, dispatch }}`는 매 렌더마다 **새 객체 리터럴**을 만든다. JavaScript의 객체 동일성 규칙상 `{ a: 1 } !== { a: 1 }`이다. React는 Context 값을 비교할 때 `Object.is`로 동일성을 본다. 부모가 어떤 이유로 다시 렌더되면 — 예를 들어 위쪽 어딘가에서 라우팅이 바뀌거나, 시계가 1초마다 갱신되거나 — `tasks`와 `dispatch`가 그대로여도 `value` 객체는 새 참조다. 그러면 Context를 구독하는 **모든** 컴포넌트가 다시 렌더된다. 변한 게 하나도 없는데도.

둘째, 정작 진짜로 `tasks`가 바뀌었을 때도 같은 일이 일어난다. dispatch 한 번으로 트리에 박힌 모든 `useContext(TasksContext)` 호출자가 다시 렌더된다. "그게 당연하지 않나? 내용이 바뀌었으니까." 맞다, 어느 정도까지는 그렇다. 그런데 곰곰이 생각해보자. `tasks`가 바뀌었다고 해서 dispatch만 쓰는 컴포넌트 — 예를 들어 "할 일 추가" 버튼 — 가 다시 렌더돼야 할 이유가 있을까? 그 버튼은 `dispatch({ type: 'added' })`만 호출할 뿐, `tasks`의 내용을 읽지 않는다. 그런데도 같이 렌더된다. 왜냐하면 우리는 둘을 한 객체에 묶어 한 Context로 보내버렸기 때문이다.

좀 더 생생하게 그려보자. 가벼운 카운터로 실험을 해보면 차이가 또렷이 보인다.

```tsx
let renderCount = 0;
function AddButton() {
  renderCount += 1;
  console.log(`AddButton 렌더 횟수: ${renderCount}`);
  const { dispatch } = useContext(TasksContext)!;
  return <button onClick={() => dispatch({ type: 'added' })}>추가</button>;
}
```

`tasks`에 100개의 항목이 있고 그중 하나를 토글했다고 해보자. 이상적으로라면 `AddButton`은 다시 렌더될 이유가 전혀 없다. 그런데 위 구조에서는 `renderCount`가 또박또박 1씩 늘어난다. **dispatch는 그대로지만 value 객체가 새 참조이기 때문**이다. 트리가 작을 땐 눈에 띄지 않는다. 하지만 카드가 수백 개로 늘고, 각 카드 안에 입력 폼이 들어가고, 부모가 다른 이유로 가끔씩 더 자주 렌더되기 시작하면 — "왠지 모르게 앱이 느릿하다"는 사용자의 한 줄 피드백이 결국 도착한다. 난감하다.

여기서 잠깐 멈추고 우리가 풀어야 할 문제를 정리하자. 이 패턴이 잘 굴러가려면 두 가지를 동시에 해결해야 한다.

1. **value 참조를 안정시켜야 한다.** 매 렌더마다 새 객체가 만들어지지 않게 만들어야 한다.
2. **자주 바뀌는 값과 거의 안 바뀌는 값을 분리해야 한다.** dispatch를 쓰는 컴포넌트가 tasks 변경 때문에 같이 흔들리지 않게 해야 한다.

두 번째 통찰이 이 장의 가장 핵심적인 비결이다. 그 비결의 이름이 바로 **"두 Context로 분리하기"**다.

## 두 Context로 분리하기 — State Context와 Dispatch Context

해법은 처음 들으면 사소하게 들린다. "한 Context에 다 묶지 말고, 두 개로 나눠라." 하지만 이 작은 분리가 만들어내는 차이는 결코 사소하지 않다. 함께 코드로 옮겨보자.

```tsx
// TasksContext.tsx
import { createContext, useReducer, type Dispatch, type ReactNode } from 'react';

// 1) 도메인 타입
export type Task = { id: string; text: string; done: boolean };

export type TasksAction =
  | { type: 'added'; id: string; text: string }
  | { type: 'changed'; task: Task }
  | { type: 'deleted'; id: string }
  | { type: 'toggled'; id: string };

// 2) reducer — 5장의 결과물 그대로 가져왔다
function tasksReducer(tasks: Task[], action: TasksAction): Task[] {
  switch (action.type) {
    case 'added':
      return [...tasks, { id: action.id, text: action.text, done: false }];
    case 'changed':
      return tasks.map(t => (t.id === action.task.id ? action.task : t));
    case 'deleted':
      return tasks.filter(t => t.id !== action.id);
    case 'toggled':
      return tasks.map(t =>
        t.id === action.id ? { ...t, done: !t.done } : t
      );
    default: {
      // 모든 케이스를 다뤘는지 컴파일 타임에 확인
      const _exhaustive: never = action;
      throw new Error(`알 수 없는 액션: ${JSON.stringify(_exhaustive)}`);
    }
  }
}

// 3) 두 Context — 의도적으로 둘로 나눈다
export const TasksStateContext = createContext<Task[] | null>(null);
export const TasksDispatchContext = createContext<Dispatch<TasksAction> | null>(null);

// 4) Provider — 안에서 reducer를 호출하고 두 Context로 각각 흘려보낸다
const initialTasks: Task[] = [];

export function TasksProvider({ children }: { children: ReactNode }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  return (
    <TasksStateContext value={tasks}>
      <TasksDispatchContext value={dispatch}>
        {children}
      </TasksDispatchContext>
    </TasksStateContext>
  );
}
```

이게 전부다. `value` 자리에 객체 리터럴 대신 **참조가 안정된 값 두 개**가 들어간다. `tasks`는 `useReducer`가 반환하는 값으로, **state가 진짜로 바뀐 dispatch 직후에만** 새 참조가 된다. `dispatch`는 — 잠시 후 따로 짚겠지만 — useReducer가 컴포넌트 평생 동안 **같은 함수 참조**를 보장한다. 즉, 더는 매 렌더마다 새 객체가 만들어지는 일이 없다.

자식이 쓰는 모습을 보자.

```tsx
function TaskCheckbox({ id }: { id: string }) {
  const tasks = useContext(TasksStateContext)!;
  const dispatch = useContext(TasksDispatchContext)!;
  const task = tasks.find(t => t.id === id)!;
  return (
    <input
      type="checkbox"
      checked={task.done}
      onChange={() => dispatch({ type: 'toggled', id })}
    />
  );
}

function AddButton() {
  // dispatch만 구독한다 — state Context는 아예 건드리지 않는다
  const dispatch = useContext(TasksDispatchContext)!;
  return (
    <button onClick={() => dispatch({ type: 'added', id: crypto.randomUUID(), text: '' })}>
      추가
    </button>
  );
}
```

`AddButton`을 다시 보자. 이 컴포넌트는 `TasksDispatchContext`만 구독한다. dispatch 참조는 평생 안 바뀐다. 그러므로 `tasks`가 아무리 자주 바뀌어도 — 카드 100개를 토글하든 1000개를 추가하든 — `AddButton`은 **다시 렌더되지 않는다**. 시계 컴포넌트가 1초마다 갱신돼서 부모를 새로 그려도, dispatch context의 값이 그대로라면 React는 이 자식의 재렌더를 건너뛴다.

거꾸로 `TaskCheckbox`는 `tasks`를 봐야 하니 state Context를 구독하고, 그 결과로 tasks가 바뀔 때마다 다시 렌더된다. 이건 의도된 동작이다. 화면에 표시할 정보가 바뀌었으니 다시 그리는 게 맞다.

핵심은 이거다. **"누가 무엇에 의존하는가"를 두 Context의 분리로 정확히 표현한 것이다.** 우리는 더 이상 React에게 "전부 묶어 보낼 테니 알아서 잘 처리해줘"라고 부탁하지 않는다. 대신 "이건 자주 바뀌는 데이터, 저건 평생 안 바뀌는 함수"라고 명시적으로 알려주는 것이다.

## 왜 dispatch는 안정적인가 — useReducer의 약속

위에서 "`dispatch` 참조는 평생 안 바뀐다"고 한 마디로 넘겼는데, 이건 React에 처음 발을 들인 사람에게는 뜬금없게 들릴 수도 있다. 잠깐 멈추고 이 약속의 정체를 들여다보자.

`useReducer(reducer, initialArg)`는 두 값을 묶어 반환한다. 첫 번째는 현재 state, 두 번째가 dispatch다. React는 `useReducer`가 반환하는 dispatch 함수에 대해 한 가지를 보장한다. **컴포넌트 인스턴스가 살아있는 동안 항상 같은 참조다.** 같은 약속이 `useState`의 setter 함수에도 적용된다. 우리가 직접 만든 일반 함수 — 예를 들어 `function handleAdd() { ... }` — 와는 사정이 다르다. 일반 함수는 매 렌더마다 새로 만들어진다. 그래서 그 함수를 Context에 실어 보내면 매번 다른 참조가 된다.

이 차이는 dispatch를 별도 Context로 떼어내는 결정의 근거가 된다. **이미 React가 안정성을 보장해주는 값을 우리가 굳이 흔들 필요는 없다.** dispatch만 구독하는 컴포넌트는 dispatch의 안정성 덕분에 "원하지 않는 재렌더"가 정확히 0이 된다.

그리고 한 가지 더, 의외로 자주 들어오는 질문이 있다. "그러면 dispatch 안에서 호출되는 reducer 함수도 매번 같은 걸 호출하나? 아니면 새로 만들어진 reducer가 호출되나?" 답은 명확하다. **dispatch가 호출되면 React는 가장 최근 렌더에서 넘긴 reducer를 사용해 다음 state를 계산한다.** 즉, reducer 자체는 매 렌더마다 새로 만들어진 함수일 수 있어도, dispatch가 그것을 어떻게 찾아 쓰는지는 React 내부의 일이라 우리가 신경 쓸 필요가 없다. 우리는 dispatch 참조가 안정적이라는 사실만 믿고 가져다 쓰면 된다.

여기까지 이해했다면, 이제 자연스러운 다음 질문이 생긴다. "그럼 state context의 value 참조는 안 흔들리나? `tasks` 배열이 매 렌더마다 새로 만들어지진 않나?" 좋은 질문이다. 결론부터 말하면, **`useReducer`가 반환하는 state는 reducer가 새 값을 만들어 반환했을 때만** 새 참조가 된다. reducer가 동일한 객체를 그대로 반환하면 — 예를 들어 `default` 분기에서 `return tasks`로 빠져나오면 — React는 이전과 같은 참조를 계속 들고 있다. 즉, dispatch가 일어나도 reducer가 "변할 게 없다"고 판단해 같은 참조를 돌려주면 useContext도 같은 값을 보고 자식 렌더를 건너뛴다.

다만 한 가지 주의가 있다. reducer 안에서 무심코 `return [...tasks]`처럼 **변하지 않았는데도 새 배열을 만들어 반환**하면, 그 순간 참조가 흔들려 모든 state context 구독자가 헛걸음을 한다. 그래서 reducer를 작성할 때 "변경이 없는 액션은 같은 state를 그대로 반환한다"는 원칙을 잊지 말자. 5장에서 짚었던 "사용자 의도 단위로 액션을 작성하라"는 조언과 같은 결의 이야기다.

## custom Provider component로 보일러플레이트 감추기

여기까지 오면 이미 핵심 패턴은 다 갖춰졌다. 그런데 호출부에서 매번 두 Context를 따로 import해서 두 번 `useContext`를 호출하는 건 — 솔직히 — 약간 거슬린다. 게다가 Context를 만든 곳, reducer를 둔 곳, Provider를 export하는 곳이 한 파일이라면 사용자에게 굳이 내부 구조를 보여줄 이유가 없다. 우리가 깔끔히 감싸 노출해주는 편이 낫다.

이 단계에서 **custom Provider component**라는 이름이 등장한다. 거창해 보이지만 본질은 단순하다. **Provider를 한 단계 더 감싸 reducer 호출까지 그 안에 숨기고, 외부에는 `<TasksProvider>` 한 컴포넌트만 노출하는 것**이다. 이미 위에서 자연스럽게 그렇게 작성하고 있었다는 점을 눈치챘을지 모른다. 다시 한 번 또렷이 정리하면 이런 구조다.

```tsx
// TasksProvider — 외부에는 이것만 노출한다
export function TasksProvider({ children }: { children: ReactNode }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  return (
    <TasksStateContext value={tasks}>
      <TasksDispatchContext value={dispatch}>
        {children}
      </TasksDispatchContext>
    </TasksStateContext>
  );
}
```

밖에서 보면 `App`은 그저 이렇게 쓴다.

```tsx
function App() {
  return (
    <TasksProvider>
      <Layout>
        <Sidebar />
        <Main />
        <Header />
      </Layout>
    </TasksProvider>
  );
}
```

깨끗하다. `App`은 reducer가 어떻게 생겼는지, Context가 몇 개로 쪼개져 있는지 알 필요가 없다. 그저 "이 트리 안쪽에서는 Tasks 도메인이 살아 있다"는 사실만 알면 된다. 이게 우리가 이 패턴에서 얻고 싶은 **캡슐화의 효과**다. 내부 구조가 바뀌어도 — 예를 들어 reducer를 immer 기반으로 갈아 끼우거나, Context를 셋으로 더 쪼개거나 — `App`의 코드는 한 줄도 바뀌지 않는다.

여기서 한 가지 욕심을 내본다면, Provider 안에 흔히 따라오는 부수적인 일들도 같이 둘 수 있다는 점이다. 예를 들어 앱이 처음 마운트될 때 localStorage에서 초기값을 복원한다든지, 변경이 일어날 때마다 외부로 동기화한다든지. 이런 코드를 `App.tsx`로 끌어 올리면 다시 prop drilling 비슷한 통로가 생긴다. Provider 안에 두면 도메인의 모든 책임이 한곳에 머문다.

```tsx
export function TasksProvider({ children }: { children: ReactNode }) {
  // 초기값을 lazy initializer로 안전하게 복원한다
  const [tasks, dispatch] = useReducer(tasksReducer, [], () => {
    try {
      const raw = localStorage.getItem('tasks');
      return raw ? (JSON.parse(raw) as Task[]) : [];
    } catch {
      return [];
    }
  });

  // 변경이 있을 때만 직렬화한다
  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  return (
    <TasksStateContext value={tasks}>
      <TasksDispatchContext value={dispatch}>
        {children}
      </TasksDispatchContext>
    </TasksStateContext>
  );
}
```

물론 모든 Provider가 이렇게 무거워야 한다는 뜻은 아니다. 다만 이 자리가 **도메인 부수효과의 자연스러운 거주지**라는 점을 기억해두자. localStorage 동기화, 분석 이벤트 발사, 초기 데이터 페치 트리거 같은 것들이 여기서 한 번만 살면, 자식 컴포넌트가 자기들의 책임에 집중할 수 있다.

## useStore() / useDispatch() — 사용처를 한 줄로

Provider는 깨끗해졌지만, 사용하는 쪽에서 매번 `useContext(TasksStateContext)!`라고 쓰는 건 여전히 거슬린다. 게다가 null 처리는 매번 손으로 해야 한다. 이런 반복은 custom hook으로 감추는 편이 낫다. 같은 파일에 두 줄짜리 hook 둘을 추가하자. 이름은 흔히 도메인을 따라간다 — Tasks 도메인이라면 `useTasks`, `useTasksDispatch`다. 일반화된 이름인 `useStore`, `useDispatch`로 부르는 팀도 많다. 어느 쪽이든 좋다.

```tsx
import { useContext } from 'react';

export function useTasks(): Task[] {
  const tasks = useContext(TasksStateContext);
  if (tasks === null) {
    // Provider 밖에서 호출했다면 즉시 알 수 있게 하자
    throw new Error('useTasks는 <TasksProvider> 안에서만 호출해야 한다');
  }
  return tasks;
}

export function useTasksDispatch(): Dispatch<TasksAction> {
  const dispatch = useContext(TasksDispatchContext);
  if (dispatch === null) {
    throw new Error('useTasksDispatch는 <TasksProvider> 안에서만 호출해야 한다');
  }
  return dispatch;
}
```

이렇게 두면 호출부가 정말 깨끗해진다.

```tsx
function TaskCheckbox({ id }: { id: string }) {
  const tasks = useTasks();
  const dispatch = useTasksDispatch();
  const task = tasks.find(t => t.id === id)!;
  return (
    <input
      type="checkbox"
      checked={task.done}
      onChange={() => dispatch({ type: 'toggled', id })}
    />
  );
}
```

겉으로 보기엔 import 한 줄과 호출 한 줄을 줄였을 뿐이지만, 얻은 게 또 있다. 첫째, **Provider 밖에서 사용하는 실수를 즉시 잡아낸다.** 위 hook들은 Context 값이 `null`이면 명확한 에러를 던진다. 그렇지 않으면 자식 컴포넌트는 어디선가 `task is undefined` 같은 둘째, 셋째 단계의 흐릿한 에러를 보게 되는데, 그건 디버깅이 정말 끔찍한 일이다. 둘째, **Context의 정체가 외부에 새지 않는다.** 사용하는 쪽은 `useTasks()`라는 이름만 안다. 내일 이 도메인이 Zustand로 옮겨가도, hook의 시그니처만 보존된다면 호출부는 한 줄도 바뀌지 않는다. 이게 우리가 흔히 말하는 **도구 교체 비용을 낮추는 추상화**다.

요약하면, 한 도메인을 다루는 한 파일은 보통 이런 모양이 된다.

```tsx
// 도메인 타입 → reducer → 두 Context → custom Provider → 두 custom hook
```

순서를 외우려 애쓸 필요는 없다. 이 다섯 조각이 한 파일에 가지런히 모여 있을 때, 이 도메인은 외부에서 보면 하나의 박스처럼 다뤄진다는 점이 중요하다.

## Provider 안에서 reducer를 호출하는 위치

지금까지 우리는 `TasksProvider` 안에서 `useReducer`를 호출했다. 별 생각 없이 그렇게 했지만, 한 번쯤 짚어둘 만한 결정이다. reducer를 어디에서 호출할지에 따라 state의 **수명**과 **공유 범위**가 바뀐다.

만약 reducer를 `App`의 최상단에서 호출하고 그 결과를 props로 `TasksProvider`에 넘긴다면, state는 `App` 인스턴스의 수명을 따른다. `App`이 살아 있는 한 사라지지 않고, `App`이 다시 마운트되면 초기화된다. 한편 `TasksProvider` 안에서 호출하면 state는 그 Provider 인스턴스의 수명을 따른다. Provider가 트리 어디에 위치하느냐가 곧 "이 도메인 데이터가 살아있는 영역"을 정의한다.

이 차이는 두 가지 실용적 결정으로 이어진다. 첫째, **Provider를 트리의 어디에 둘 것인가**. 6장에서 우리가 강조했던 "Provider를 트리 깊숙이 두어 영향 범위를 좁힌다"는 원칙이 여기서도 그대로 유효하다. 어떤 페이지에서만 쓰는 Tasks라면 `App` 최상단이 아니라 그 페이지 컴포넌트 안에 두자. 그러면 다른 페이지로 이동했을 때 자연스럽게 정리된다. 둘째, **여러 Provider를 트리 어디서든 새로 띄울 수 있다**. 같은 `TasksProvider`를 한 화면에서 두 번 마운트하면, 두 트리 영역은 각자 자기만의 tasks를 가진다. 나란히 보이는 두 칸반 보드를 만든다고 했을 때, 별도 Provider만 두 번 두면 끝이다.

이 점은 의외로 우리에게 큰 자유를 준다. **state는 항상 전역이어야 한다는 강박이 사라진다.** Context는 전역 store가 아니라 "이 트리 영역의 공유 데이터"를 표현하는 도구라는 본래의 자리로 돌아온다.

## 중첩 Provider 합성과 도메인 분리

앱이 더 자라면 Tasks 하나만으로는 끝나지 않는다. 사용자 정보, 테마, 알림, 모달 상태, 폼 워크플로우 — 도메인이 늘어난다. 이때 **모든 도메인을 한 거대한 Provider에 욱여넣는 충동**이 슬그머니 고개를 든다. "어차피 다 글로벌이니까 하나로 만들면 깔끔하지 않나?" 결과는 정반대다. 도메인이 섞인 Provider는 한 도메인의 변경이 다른 도메인 구독자들까지 흔든다. 우리가 이번 장 초반에 두 Context로 분리한 이유와 같은 문제가, 도메인 단위에서 다시 일어난다.

해법도 같다. **도메인마다 별도의 Provider를 두고 합성한다.** 두 개를 합치는 모습은 이렇게 자연스럽다.

```tsx
function App() {
  return (
    <ThemeProvider>
      <UserProvider>
        <TasksProvider>
          <Layout>
            <Header />
            <Main />
          </Layout>
        </TasksProvider>
      </UserProvider>
    </ThemeProvider>
  );
}
```

각 Provider는 자기 도메인만 책임진다. `Theme`이 바뀌어도 `Tasks` 구독자는 흔들리지 않는다. `Tasks`를 dispatch해도 `User` 구독자에게는 아무 일도 일어나지 않는다. 도메인 사이의 **렌더 경계**가 Provider 단위로 자연스럽게 그어진다.

여기서 한 가지 안티패턴을 의식적으로 피하자. 어떤 팀은 중첩이 보기 싫다는 이유로 Provider들을 한 줄로 합치는 헬퍼를 만든다.

```tsx
// 안티패턴은 아니지만, 의미가 흐려질 수 있다
function AppProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <UserProvider>
        <TasksProvider>{children}</TasksProvider>
      </UserProvider>
    </ThemeProvider>
  );
}
```

이 자체가 나쁜 건 아니다. 다만 Provider의 위치가 곧 도메인의 영향 범위를 결정한다는 점을 잊고, 무조건 최상단에 모든 Provider를 끌어모으는 습관이 들면 곤란해진다. **어떤 Provider는 페이지 단위에, 어떤 Provider는 모달 단위에, 어떤 Provider만 앱 전역에** — 이런 식의 위계를 의식적으로 그리는 편이 낫다. 6장에서 말한 콜로케이션이 도메인 단위에서도 그대로 통한다는 뜻이다.

도메인을 어떻게 나눌지 기준을 잡는 데 고민이 된다면, 두 가지 신호를 보면 도움이 된다. 첫째, **함께 바뀌는가**. 한 핸들러 안에서 둘이 같이 바뀌는 일이 잦다면 같은 도메인일 가능성이 높다. 둘째, **함께 사라지는가**. 한쪽 화면이 사라질 때 다른 쪽도 같이 정리되어야 한다면, 둘은 한 Provider 아래 살 수 있다. 두 신호가 모두 약하다면, 의심하지 말고 도메인을 갈라두자.

## Context를 "전역 store"로 쓰지는 말자

여기까지 따라왔다면 Reducer + Context 조합이 꽤 강력해 보일 것이다. 실제로 그렇다. 작은-중간 규모의 UI 상태에서 이 패턴은 외부 라이브러리 없이도 충분히 잘 굴러간다. Kent C. Dodds가 자주 강조하는 "React IS your state management library"라는 말은 바로 이런 자리에서 가장 잘 통한다.

그렇다면 한 가지 의문이 자연스럽게 따라온다. "이걸로 모든 상태를 덮을 수 있는 거 아닌가? Redux나 Zustand 같은 외부 라이브러리는 왜 따로 쓰지?" 이 질문에 답하려면 Context가 갖지 않은 능력 하나를 똑똑히 짚어둬야 한다. 바로 **selective subscription의 부재**다.

selective subscription이란 "이 store의 이 일부만 구독하고, 거기에 속하지 않는 변경에는 반응하지 않겠다"고 선언할 수 있는 능력이다. Zustand의 `useStore(state => state.someSlice)`나 Redux의 `useSelector` 같은 API가 그 자리를 차지한다. selector가 반환한 값이 이전과 같으면 — 얕은 비교 또는 사용자 정의 비교로 — 구독자는 다시 렌더되지 않는다.

Context는 이런 일을 못 한다. **Context value가 새 참조가 되는 순간, 그 Context를 구독하는 모든 컴포넌트가 무조건 다시 렌더된다.** 우리는 두 Context로 분리하는 트릭으로 큰 한 갈래를 막았지만, 이건 어디까지나 "변경 빈도가 다른 두 덩어리"를 가르는 거친 도구다. 같은 state Context 안에서도 어떤 컴포넌트는 `tasks[0]`만 보고 어떤 컴포넌트는 `tasks.length`만 보는데, 어느 쪽이 바뀌든 둘 다 다시 렌더된다. tasks 배열의 참조가 바뀐 이상 React에게는 그 둘이 같은 변경으로 보인다.

이 한계가 진짜로 발목을 잡기 시작하는 시점은, **자주 바뀌는 큰 state를 큰 트리에 흘려보내야 할 때**다. 마우스 좌표를 글로벌하게 공유한다든지, WebSocket으로 1초에 수십 개의 메시지가 들어와 같은 트리에 박힌 수백 개 컴포넌트가 각각 자기 지분만 읽고 싶을 때다. Context로 풀려 들면 모든 컴포넌트가 매 변경마다 리렌더되고, 그 비용이 — 작은 앱에선 무시할 수 있었지만 — 화면 단위에서 체감되기 시작한다.

이 자리에서 외부 도구가 등장한다. Zustand, Jotai, Redux Toolkit이 각자의 결로 selective subscription을 제공한다. 하지만 이 책의 흐름상 그 결정 트리는 다음 8장에서 따로 다룬다. 지금 단계에서 우리가 챙겨야 할 메시지는 두 가지다.

첫째, **Context는 글로벌 store의 대용품이 아니다.** 글로벌하게 공유되어야 할 데이터 중에서도, **자주 안 바뀌는** 것에 잘 어울린다. 로그인 사용자, 테마, 라우팅 컨텍스트, 기능 플래그 같은 부류다. 이 부류라면 Context + 두 Context 분리로 충분하다 못해 우아하다.

둘째, **Context를 쓰지 말아야 할 자리에 쓰기 시작한 신호**를 알아두자. value가 1초에 여러 번 바뀌는데 구독자가 트리 곳곳에 수십 개씩 흩어져 있다면, 그리고 그중 다수가 value의 일부분에만 관심이 있다면, 거의 분명히 도구 선택을 다시 해야 할 시점이다. 8장에서 이 신호를 좀 더 정량적으로 다듬어볼 것이다.

조금 더 일찍, 그러나 너무 이르지 않은 시점에 — Kent Dodds가 한 말처럼 "Don't reach for context too soon!"이지만, 또한 "Don't refuse to leave context too late!"이기도 하다. 이 둘 사이의 적정 자리를 찾는 게 우리가 다음 장에서 같이 그려볼 결정 트리다.

## 핵심 정리

- **Reducer + Context는 5장과 6장의 자연스러운 만남이다.** reducer로 변경 로직을 모으고, Context로 깊은 자식까지 흘려보낸다.
- **`value={{ state, dispatch }}`처럼 한 Context에 다 묶는 건 함정이다.** 매 렌더마다 새 객체 리터럴이 만들어져, dispatch만 쓰는 컴포넌트까지 같이 리렌더된다.
- **State Context와 Dispatch Context를 분리하자.** 자주 바뀌는 값과 거의 안 바뀌는 값을 두 통로로 가른다. 이 한 번의 분리가 패턴 전체의 성능과 의도 표현을 동시에 살린다.
- **dispatch 참조는 useReducer가 안정성을 보장한다.** 컴포넌트 평생 동안 같은 함수다. 그래서 별도 Context로 떼어내면 dispatch 구독자는 사실상 리렌더가 0이 된다.
- **state context의 value 참조는 reducer가 새 값을 만들 때만 바뀐다.** 변경이 없는 액션에서 같은 배열을 그대로 반환하도록 reducer를 짜자. 무심코 `[...tasks]`를 만들어 흔들지 말자.
- **custom Provider 컴포넌트로 reducer 호출과 두 Context 셋업을 한 박스에 가둔다.** 외부에는 `<TasksProvider>` 한 컴포넌트만 노출한다. 도메인의 부수효과(localStorage, 페치 등)도 이 안에 함께 거주시키자.
- **`useTasks()` / `useTasksDispatch()` 같은 custom hook을 같은 파일에서 노출한다.** Provider 밖 사용을 즉시 에러로 잡아내고, Context의 정체를 외부에 누설하지 않는다. 도구 교체 비용이 낮아진다.
- **도메인마다 별도의 Provider를 만들고 트리에서 합성한다.** 한 도메인의 변경이 다른 도메인 구독자에게 새지 않는다. Provider의 위치는 곧 도메인의 수명과 영향 범위다.
- **Provider를 무조건 최상단에 끌어 모으지 말자.** 페이지 단위, 모달 단위에 둘 수 있는 도메인은 그 자리에 두자. 6장의 콜로케이션 원칙이 도메인 단위로 확장된다.
- **Context는 selective subscription이 없다.** value가 바뀌면 모든 구독자가 리렌더된다. 자주 바뀌는 큰 state를 큰 트리에 흘리는 자리에서는 외부 도구가 필요해진다 — 8장의 주제다.

## 연습 문제

### [기초] 단일 `value`를 두 Context로 분리하기 — 리렌더 측정

아래 두 버전을 직접 만들어보자. 같은 Tasks 앱이지만, 한 쪽은 `value={{ tasks, dispatch }}` 단일 Context이고, 다른 쪽은 State/Dispatch 두 Context다. dispatch만 구독하는 `AddButton` 컴포넌트에 렌더 카운터를 박아두고, "토글" 액션을 100번 발사했을 때 두 버전의 카운트를 비교하라.

```tsx
let renderCount = 0;
function AddButton() {
  renderCount += 1;
  // ... 같은 본문
}
```

기대 결과: 단일 Context 버전은 카운트가 100 가까이 올라가고, 두 Context 버전은 1에 머문다. 왜 그런지 한 문단으로 설명해보자.

### [기초] 같은 Provider value를 매 렌더 새 객체로 만들었을 때의 부작용 진단

이미 두 Context로 분리한 코드에서, State Context의 value를 다음처럼 의도적으로 매 렌더 새 객체로 감싸보자.

```tsx
<TasksStateContext value={{ tasks }}>
```

`useTasks`도 그에 맞춰 `{ tasks }`를 풀어서 반환하게 고친다. 이 작은 변경으로 어떤 일이 생기는지 React DevTools의 "Highlight updates when components render"로 관찰하라. 단일 Context 시절의 비극이 그대로 부활하는 모습을 두 눈으로 보자.

### [중] 작은 Todo 앱: reducer + context + custom hook 전체 구성

다음 요구를 만족하는 작은 Todo 앱을 처음부터 짜보자.

- 도메인 액션: `added`, `changed`, `toggled`, `deleted`, `cleared`
- `<TodosProvider>`로 reducer와 두 Context를 한 박스에 감춘다
- `useTodos()`, `useTodosDispatch()` custom hook을 노출하고, Provider 밖 호출은 명확한 에러
- localStorage에 변경을 동기화 (Provider 안의 effect)
- "추가 버튼"과 "리스트"와 "체크박스"가 각각 자기에게 필요한 hook만 호출하는지 점검

마지막에, "도메인 외부 코드(`App` 등)에서 reducer나 Context의 정체가 노출되지 않았는지" 한 번 더 검사하라. 새고 있다면 어디서, 왜 새는지 짧게 적어보자.

### [중] 자주 바뀌는 값과 거의 안 바뀌는 값을 두 Context로 분리

이번엔 도메인을 하나 바꿔서, "현재 사용자(거의 안 바뀜)"와 "최근 알림 토스트(자주 바뀜)"가 같이 사는 Provider를 짜보자. 한 Context에 묶었을 때 사용자 정보만 쓰는 컴포넌트가 어떻게 흔들리는지 본 뒤, 두 Context로 갈라 그 흔들림이 사라지는 것을 확인하라. 이 분리의 기준을 한 줄로 자기 언어로 적어두자 — "이 도구가 두 자리에 어울리는 한 문장 사용 설명서" 형태로.

### [도전] 중첩된 두 도메인을 별도 Provider로 — 격리 검증

하나의 화면 안에 두 칸반 보드를 띄워야 한다고 해보자. 두 보드는 같은 reducer 정의를 공유하지만, 각자 독립된 tasks를 가진다. `<TasksProvider>`를 두 번 마운트하는 구조로 짜고, 보드 A를 dispatch했을 때 보드 B의 `useTasks()` 구독자가 리렌더되지 않는지 검증하라.

추가 도전: 한쪽 보드 트리 안에 또 다른 도메인 Provider — 예를 들어 `<NotificationsProvider>` — 를 끼워 넣고, 그 도메인의 변경이 다른 보드와 전혀 무관함을 React DevTools로 확인하라. "Provider의 위치가 곧 영향 범위"라는 문장을 자기 손으로 입증하는 시간이다.

## 다음 장으로 가는 다리

이번 장에서 얻은 가장 중요한 한 가지는, **"Context는 전역 store가 아니다"**라는 명제다. 두 Context로 분리하면 큰 비극은 막지만, selective subscription이 없는 한계는 그대로 남아 있다. 자주 바뀌는 데이터를 큰 트리에 흘려야 하는 자리에서는, Context의 결을 거슬러 작동시키려 애쓰는 것보다 다른 도구의 도움을 받는 편이 낫다.

그렇다면 자연스러운 질문이 따라온다. **언제 Context로 충분한가? 언제 Zustand가 등장해야 하나? Redux Toolkit은 어떤 자리에 어울리나? Jotai는? 그리고 — 이게 사실 가장 중요한데 — 우리가 손에 쥐고 있는 그 데이터, 정말 UI state가 맞는가? 혹시 server state는 아닌가?** 같은 reducer + context 패턴으로 fetch 결과를 다 때려박고 있다면, 우리는 알고 보면 query cache를 직접 다시 만들고 있는 셈이다 — 그리고 그건 거의 항상 깨진다.

8장에서는 이 결정 트리를 함께 그린다. Context의 selective subscription 부재가 실제로 어떤 비용으로 환산되는지, Zustand·Jotai·Redux Toolkit이 그 비용을 어떻게 내려주는지, 그리고 server state가 왜 별도 도구의 영토인지를 차근차근 살펴보자. 이 책에서 가장 실무적인 결정이 모이는 자리이기도 하다. 함께 가보자.
