# 5장. 흩어진 setState를 한 자리에 모으고 싶을 때 — useReducer

월요일 아침, 동료가 슬랙으로 메시지를 보낸다. "어제 머지한 PR에서 할 일 목록이 가끔 이상하게 동작하는 것 같아요. 새 항목을 추가하면 체크 상태가 풀리는 경우가 있어요." 컴포넌트를 열어 본다. `TaskList.tsx`. 처음에는 단순했던 화면이었는데, 지금은 setTasks가 컴포넌트 안에 열두 군데에 흩어져 있다. 어떤 것은 spread를 쓰고, 어떤 것은 map을 쓰고, 어떤 것은 filter를 쓴다. 누군가 추가한 "기한이 지난 항목 자동 정리" 기능 때문에 setTasks가 useEffect 안에도 들어가 있다. 어디서 무엇이 바뀌는지 추적하는 데에만 30분이 든다.

이런 코드를 마주하면 마음이 답답해진다. "분명 이 컴포넌트는 내가 처음 짤 때만 해도 깔끔했는데, 어쩌다 이렇게 됐을까?" 손은 자꾸 키보드 위에서 멈칫거린다. setTasks를 한 군데 더 추가하자니 "정말 이 자리가 맞나?" 하는 의심이 들고, 기존 setTasks를 고치자니 "여길 고치면 다른 핸들러는 영향이 없을까?"가 걱정된다. 무엇보다 끔찍한 건, 이 코드를 일주일 뒤에 다시 열었을 때의 내 모습이다. 분명 그때의 나는 지금의 나보다 더 모를 것이다.

이쯤 되면 한 번 멈춰서 생각해 볼 만하다. 도대체 왜 이렇게 됐을까? 잘못한 건 우리가 게을러서일까, 아니면 useState라는 도구가 이런 종류의 문제에는 더 이상 어울리지 않게 된 시점일까? 나는 후자라고 본다. 이 장에서 함께 살펴볼 것은 바로 그 임계점, 그리고 그 임계점을 넘었을 때 손에 잡아야 할 도구인 `useReducer`다.

## 흩어진 setState의 증상들

먼저 자기 코드를 점검해 보자. 다음 증상 중 두 개 이상이 한 컴포넌트에서 발견된다면, 그 컴포넌트는 이미 reducer로 옮겨갈 준비가 끝난 것이다.

첫째, **하나의 이벤트 핸들러 안에서 setState 호출이 두세 개씩 묶여 다닌다.** "할 일을 추가했으니 목록도 갱신하고, 입력창도 비우고, 에러 메시지도 지우자"는 식으로 setTasks, setDraft, setError가 한 함수 안에서 줄지어 호출된다. 이 자체가 나쁜 건 아니지만, 같은 의도(=항목 추가)에 따라 함께 움직여야 할 변경들이 시각적으로 흩어져 있다는 신호다.

둘째, **같은 패턴의 갱신 코드가 여러 핸들러에 복제되어 있다.** `handleAdd`, `handleAddFromTemplate`, `handleAddFromImport` 세 곳에 모두 비슷한 spread + 정렬 + 검증 코드가 들어 있다. 한쪽을 고치면 다른 쪽도 고쳐야 한다는 압박감이 생긴다. 이쯤 되면 찜찜하다.

셋째, **setState 안에서 prev를 받아 복잡한 계산을 한다.** `setTasks(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t))` 같은 한 줄짜리 표현식이 핸들러 안에 인라인으로 박혀 있다. 한두 군데일 땐 문제가 없지만 다섯 군데를 넘어가면 그 자체로 한 페이지를 차지한다. 진짜 비즈니스 로직이 그 한 줄들 사이에 묻힌다.

넷째, **버그 리포트가 들어왔을 때 "어디서 task를 바꾸는지" 찾는 데 시간이 든다.** IDE에서 `setTasks(`를 검색해 12개의 매칭 결과를 클릭해 가며 하나씩 읽어야 한다는 뜻이다. 이 컴포넌트의 갱신 로직은 더 이상 한 사람의 머리에 들어오지 않는다.

다섯째, **TypeScript가 도움을 주지 못한다.** task 모양을 바꾸고 싶은데, 어디서 어떻게 task를 만들고 변형하는지가 흩어져 있어 컴파일러도 일관된 확인을 해 주지 못한다. 결국 "고쳐 놓고 직접 12군데를 다 점검"하는 것 외에는 안전망이 없다.

이 증상들의 공통점이 보이는가? 바로 **갱신 로직이 한 곳에 모여 있지 않다**는 것이다. 우리는 컴포넌트 본체에 "사용자가 무엇을 했을 때 무엇을 보여 줄지"를 적으러 왔는데, 어느새 "데이터가 어떻게 바뀌어야 하는지"가 그 사이사이에 끼어들어 화면 코드를 흐려 놓았다. 그렇다면 어떻게 해야 할까? 답은 뜻밖에도 단순하다. **갱신 로직을 한 함수로 모으자.** 그 함수가 바로 reducer다.

## useState에서 useReducer로 — 의식 있는 절차

reducer로 옮기는 작업은 무턱대고 시작할 일이 아니다. 잘못 옮기면 useState만도 못한 reducer가 나온다. 의식 있는 순서를 따라가 보자.

먼저, 현재의 useState 기반 코드부터 정직하게 읽는다. 단순화한 버전을 함께 보자.

```tsx
// before — useState로 흩어진 상태 관리
import { useState } from 'react';

type Task = {
  id: number;
  text: string;
  done: boolean;
};

let nextId = 0;

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [draft, setDraft] = useState('');

  // 추가
  function handleAdd() {
    if (!draft.trim()) return;
    setTasks([...tasks, { id: nextId++, text: draft, done: false }]); // (1)
    setDraft(''); // (2)
  }

  // 토글
  function handleToggle(id: number) {
    setTasks(
      tasks.map((t) => (t.id === id ? { ...t, done: !t.done } : t)), // (3)
    );
  }

  // 삭제
  function handleRemove(id: number) {
    setTasks(tasks.filter((t) => t.id !== id)); // (4)
  }

  // 텍스트 수정
  function handleEdit(id: number, text: string) {
    setTasks(
      tasks.map((t) => (t.id === id ? { ...t, text } : t)), // (5)
    );
  }

  return (
    <section>
      <input value={draft} onChange={(e) => setDraft(e.target.value)} />
      <button onClick={handleAdd}>추가</button>
      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <input
              type="checkbox"
              checked={t.done}
              onChange={() => handleToggle(t.id)}
            />
            <input
              value={t.text}
              onChange={(e) => handleEdit(t.id, e.target.value)}
            />
            <button onClick={() => handleRemove(t.id)}>삭제</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
```

이 정도라면 아직 useState로 충분하다고 말하는 사람도 있을 것이다. 일리가 있다. 다만 우리는 일부러 단순한 예제로 시작해서, 같은 구조가 어떻게 reducer로 옮겨가는지를 손으로 익혀 두려 한다. 본 게임은 폼 위저드, 에디터, 칸반 같은 더 큰 상태에서 벌어진다. 그때 가서야 reducer를 처음 써 보면 늦다.

자, 이제 1번부터 5번까지 매겨 둔 setTasks 호출 다섯 군데를 한 함수로 모아 보자. 절차는 다음과 같다.

**1단계: 각 setState 호출이 실제로 "무슨 사용자 의도"였는지 이름을 붙인다.** "추가했다", "토글했다", "삭제했다", "수정했다". 이 이름들이 곧 액션 이름이 된다. **2단계: 그 이름과, 갱신에 필요한 데이터를 한 객체로 묶는다.** 이게 액션 객체다. **3단계: 모든 갱신 로직을 받아 새 상태를 돌려주는 단 하나의 함수를 만든다.** 이게 reducer다. **4단계: useState를 useReducer로 바꾸고, 핸들러는 dispatch만 하게 한다.**

이 절차의 핵심은 *순서*다. 액션 이름을 먼저 정하고 reducer를 짜야지, reducer부터 짜고 거기 맞춰 액션을 비틀면 십중팔구 나쁜 추상이 나온다. 이름은 의도, 페이로드는 데이터 — 이 한 줄을 기억해 두자.

## reducer는 순수 함수다 — 부수효과 금지의 진짜 의미

옮기기 전에 짚고 넘어가야 할 것이 하나 있다. reducer는 `(state, action) => newState` 형태의 **순수 함수**다. 이 단어가 가벼이 들리겠지만 실제로 위반하면 곧 후회한다. 무엇이 순수성을 깨뜨릴까?

- `Math.random()`, `Date.now()`처럼 호출할 때마다 결과가 달라지는 함수.
- `fetch()`, `localStorage.setItem()` 같은 외부 세계 호출.
- 인자로 받은 state나 action을 직접 변형(mutation)하는 코드 — `state.tasks.push(...)`처럼.
- 콘솔 로그도 엄밀히는 부수효과지만 디버깅 목적의 임시 사용은 관용된다.

이런 것들을 reducer 안에 두면 무슨 일이 벌어지나? React는 dev 모드에서 reducer를 두 번 호출해 순수성을 검증한다. 안에 `Date.now()`가 있으면 두 번의 결과가 달라져 미묘한 버그가 생긴다. 더 본질적인 문제는, reducer를 시간여행 디버깅하거나 테스트할 때 같은 입력에 같은 출력이 나오지 않으면 우리가 기대했던 모든 이점이 무너진다는 것이다.

그럼 ID 생성이나 타임스탬프 같은 건 어디서 만들어야 할까? **호출하는 쪽, 즉 핸들러에서 만들어 액션의 페이로드로 넣어 준다.** 이렇게 하면 reducer는 받은 값을 그저 합치기만 하면 된다.

```tsx
// 좋지 않은 예 — reducer 안에서 ID 생성
function reducer(state: State, action: Action): State {
  if (action.type === 'added') {
    return {
      ...state,
      tasks: [...state.tasks, { id: Date.now(), text: action.text, done: false }],
      // ↑ Date.now()가 reducer 안에 있다. 매 호출마다 다른 결과.
    };
  }
  // ...
}

// 더 나은 예 — 호출 측에서 만들어 페이로드로 전달
function handleAdd() {
  dispatch({ type: 'added', id: nextId(), text: draft });
}
```

이 작은 차이가 테스트, 시간여행 디버깅, dev 모드 더블 인보케이션에서의 안전성을 모두 좌우한다. 잊지 말자. **reducer에 부수효과를 절대 두지 않는다.** 부수효과는 컴포넌트 본체나 이벤트 핸들러, 혹은 정 필요하면 effect로 보내자.

## 액션을 데이터로 표현하기 — TS discriminated union

이제 본격적으로 reducer를 만들어 보자. TypeScript의 discriminated union을 쓰면 액션을 안전한 데이터 구조로 모델링할 수 있다.

```tsx
// state와 action 타입 정의
type Task = {
  id: number;
  text: string;
  done: boolean;
};

type State = {
  tasks: Task[];
  draft: string;
};

type Action =
  | { type: 'draft/changed'; text: string } // 입력창 변경
  | { type: 'task/added'; id: number; text: string } // 새 항목 추가
  | { type: 'task/toggled'; id: number } // 완료 상태 토글
  | { type: 'task/edited'; id: number; text: string } // 텍스트 수정
  | { type: 'task/removed'; id: number }; // 항목 삭제
```

여기서 `type` 필드가 바로 *판별자*(discriminant)다. TypeScript는 `action.type`을 읽고 나면 그 분기 안에서는 해당 타입의 페이로드만 안전하게 접근할 수 있게 해 준다. 즉 `case 'task/toggled'` 안에서는 `action.text`에 접근하려 하면 컴파일 에러를 낸다 — 그 액션엔 text가 없기 때문이다. 이 안전망이 reducer 작성을 매우 든든하게 만든다.

이 타입을 두고 reducer를 작성해 보자.

```tsx
function tasksReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'draft/changed':
      return { ...state, draft: action.text };

    case 'task/added':
      return {
        ...state,
        draft: '', // 추가 후 입력창 비우기
        tasks: [
          ...state.tasks,
          { id: action.id, text: action.text, done: false },
        ],
      };

    case 'task/toggled':
      return {
        ...state,
        tasks: state.tasks.map((t) =>
          t.id === action.id ? { ...t, done: !t.done } : t,
        ),
      };

    case 'task/edited':
      return {
        ...state,
        tasks: state.tasks.map((t) =>
          t.id === action.id ? { ...t, text: action.text } : t,
        ),
      };

    case 'task/removed':
      return {
        ...state,
        tasks: state.tasks.filter((t) => t.id !== action.id),
      };

    default:
      // 모든 케이스를 다뤘는지 컴파일 시점에 검증
      const _exhaustive: never = action;
      return state;
  }
}
```

마지막의 `_exhaustive: never` 패턴을 눈여겨보자. 만약 액션 유니온에 새 변형을 추가하고 reducer의 switch에 case를 빠뜨리면, TypeScript가 "Type 'X' is not assignable to type 'never'"라고 알려 준다. 즉 reducer가 갱신 로직의 *완전한 카탈로그*가 되도록 컴파일러가 강제해 주는 셈이다. 우리는 이런 안전망을 적극 활용하는 편이 낫다.

이제 컴포넌트를 옮겨 보자.

```tsx
// after — useReducer로 모은 상태 관리
import { useReducer } from 'react';

let nextId = 0;
const initialState: State = { tasks: [], draft: '' };

export function TaskList() {
  const [state, dispatch] = useReducer(tasksReducer, initialState);
  const { tasks, draft } = state;

  function handleAdd() {
    if (!draft.trim()) return;
    dispatch({ type: 'task/added', id: nextId++, text: draft });
  }

  return (
    <section>
      <input
        value={draft}
        onChange={(e) =>
          dispatch({ type: 'draft/changed', text: e.target.value })
        }
      />
      <button onClick={handleAdd}>추가</button>
      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <input
              type="checkbox"
              checked={t.done}
              onChange={() => dispatch({ type: 'task/toggled', id: t.id })}
            />
            <input
              value={t.text}
              onChange={(e) =>
                dispatch({
                  type: 'task/edited',
                  id: t.id,
                  text: e.target.value,
                })
              }
            />
            <button onClick={() => dispatch({ type: 'task/removed', id: t.id })}>
              삭제
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
```

비교해 보자. before에선 setTasks가 다섯 군데, setDraft가 두 군데에 흩어져 있었다. after에선 모든 갱신 로직이 `tasksReducer` 한 함수에 모여 있다. 컴포넌트 본체는 "사용자가 무엇을 했는지"만 dispatch로 외친다. 디버깅할 때도 reducer 한 곳만 열면 된다. 그리고 reducer는 외부 의존성이 없는 순수 함수이므로 단위 테스트가 매우 쉽다.

```tsx
// 테스트 예시 — reducer만 따로 검증
import { describe, it, expect } from 'vitest';

describe('tasksReducer', () => {
  it('새 항목을 추가하고 draft를 비운다', () => {
    const before: State = { tasks: [], draft: '우유 사기' };
    const after = tasksReducer(before, {
      type: 'task/added',
      id: 1,
      text: '우유 사기',
    });
    expect(after.tasks).toHaveLength(1);
    expect(after.tasks[0]).toMatchObject({ id: 1, text: '우유 사기', done: false });
    expect(after.draft).toBe('');
  });

  it('토글은 done 값을 뒤집는다', () => {
    const before: State = {
      tasks: [{ id: 1, text: 'A', done: false }],
      draft: '',
    };
    const after = tasksReducer(before, { type: 'task/toggled', id: 1 });
    expect(after.tasks[0].done).toBe(true);
  });
});
```

reducer가 순수 함수라는 약속을 지킨 덕분에, 컴포넌트 트리도, 가짜 DOM도, 모킹도 필요 없이 그저 함수 호출만으로 갱신 로직을 검증할 수 있다. 이것이 reducer로 옮기는 두 번째 큰 이득이다.

## "이름은 의도, 페이로드는 데이터" — 액션 명명 원칙

reducer를 처음 써 보는 사람이 가장 자주 빠지는 함정이 있다. 액션을 *세터의 이름*으로 짓는 것이다. 예를 들어 이런 식이다.

```tsx
// 안티패턴 — 사용자 의도가 아니라 setter 이름을 그대로 옮긴 액션
type Action =
  | { type: 'SET_TASKS'; tasks: Task[] }
  | { type: 'SET_DRAFT'; draft: string }
  | { type: 'SET_TASK_DONE'; id: number; done: boolean };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_TASKS':
      return { ...state, tasks: action.tasks };
    case 'SET_DRAFT':
      return { ...state, draft: action.draft };
    case 'SET_TASK_DONE':
      return {
        ...state,
        tasks: state.tasks.map((t) =>
          t.id === action.id ? { ...t, done: action.done } : t,
        ),
      };
  }
}
```

이런 reducer는 useState만도 못하다. 왜 그럴까? 이유는 명확하다. **사용자 의도가 사라지고 변수 할당만 남기 때문이다.** "할 일을 추가한다"는 의도는 어디 갔는가? 그 의도가 호출 측 코드인 `handleAdd`에 다시 흩어진다. reducer는 그저 "tasks를 통째로 바꾸는 통로"가 되어 버린다. 결국 갱신 로직은 다시 핸들러에 흩어지고, reducer는 실내 인테리어만 바꾼 useState가 되고 만다.

올바른 명명은 "사용자 의도 단위"다. 다음 두 가지 원칙을 지키자.

첫째, **액션 이름은 도메인 사건이어야 한다.** "추가됐다", "토글됐다", "보관함에 들어갔다", "공유됐다" 같은 것이다. setter 이름이 아니라 사건 이름이다. 이름만 봐도 reducer를 모른 채로 "무엇이 일어났는지" 짐작이 가야 한다. 우리는 보통 `'영역/사건'` 형태로 적는다 — `'task/added'`, `'cart/checkedOut'`, `'wizard/stepAdvanced'`. 영역 슬래시 표기는 큰 reducer에서 사건들을 그룹지어 보기 쉽게 해 준다.

둘째, **페이로드는 그 사건을 표현하는 최소한의 데이터다.** 사건이 일어난 결과로 어떤 상태가 되어야 하는지 reducer가 알아서 계산하게 둔다. 호출자는 "이미 계산된 새 tasks 배열"을 넘기지 않는다. "id가 5인 항목이 토글됐다"만 넘긴다. 계산은 reducer의 일이다.

이 두 원칙을 따르지 않으면 reducer는 글로벌 setter의 모음집이 된다. 그러면 우리가 처음에 풀고 싶었던 *흩어진 갱신 로직 모으기* 문제가 다시 돌아온다. 작명은 사소해 보이지만, 이 차이가 코드 운명을 가른다. 잊지 말자. **이름은 의도, 페이로드는 데이터.**

## 사용자 의도 단위 — 잘게 쪼개지 말 것

비슷한 함정 하나를 더 살펴보자. 액션을 너무 잘게 쪼개는 경우다.

```tsx
// 폼 상태에 대한 안티패턴 — 필드별 액션을 모두 만든 reducer
type FormState = { name: string; email: string; agree: boolean };

type FormAction =
  | { type: 'name/changed'; value: string }
  | { type: 'email/changed'; value: string }
  | { type: 'agree/toggled' };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'name/changed':
      return { ...state, name: action.value };
    case 'email/changed':
      return { ...state, email: action.value };
    case 'agree/toggled':
      return { ...state, agree: !state.agree };
  }
}
```

겉보기엔 깔끔해 보이지만, 이 reducer는 같은 사건(=폼 입력)에 대해 세 개의 분기를 가진 셈이다. 필드가 늘어나면 분기도 똑같이 늘어난다. 이럴 땐 **단일 `field/changed` 액션**으로 합치는 편이 깔끔하다.

```tsx
// 더 나은 폼 reducer — 필드 이름을 페이로드에 포함
type FormState = { name: string; email: string; agree: boolean };

type FormAction =
  | { type: 'field/changed'; field: 'name' | 'email'; value: string }
  | { type: 'agree/toggled' }
  | { type: 'form/reset' };

const initialForm: FormState = { name: '', email: '', agree: false };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'field/changed':
      return { ...state, [action.field]: action.value };
    case 'agree/toggled':
      return { ...state, agree: !state.agree };
    case 'form/reset':
      return initialForm;
  }
}
```

여기서 `agree`는 일부러 분리했다. 체크박스의 토글은 의미가 명확한 단일 사건이고, "필드 변경"과는 사용자 의도가 다르기 때문이다. 즉, "사용자 의도가 같으면 묶고, 다르면 가른다"가 기준이다. 무조건 합치거나 무조건 쪼개는 게 아니다.

그렇다면 어떻게 판별할까? 한 가지 좋은 휴리스틱이 있다. **그 사건을 사용자에게 자연어로 설명할 때 한 문장으로 끝나면 한 액션, 두 문장으로 갈리면 두 액션이다.** "이름 필드를 바꿨다" "이메일 필드를 바꿨다"는 같은 종류의 한 문장이다. "약관에 동의했다"는 다른 문장이다. 이 감각을 길러 두면 액션 모델이 한결 깔끔해진다.

## reducer가 과한 경우 — useState가 더 어울릴 때

reducer가 늘 정답은 아니다. 오히려 잘못 쓰면 코드가 더 무거워진다. 다음 경우엔 useState가 낫다.

- **단일 boolean 토글** — 모달 열림/닫힘, 메뉴 펼침/접기. 사용자 의도도 단순하고, 이 값이 다른 값들과 묶여 변하지 않는다면 굳이 reducer로 쌀 필요가 없다.
- **다른 어떤 상태와도 동시에 변하지 않는 단일 값** — 예를 들어 검색창 텍스트만 바뀌는 컴포넌트. setQuery 한 줄이면 된다.
- **값의 변경이 한두 핸들러에서만 일어난다** — 분산되어 있지 않다면 모을 필요 자체가 없다.
- **상태 모양이 단순하고, 확장 계획도 없다** — 미래의 복잡도를 미리 사 두려고 reducer를 쓰지 말자. 필요해질 때 옮겨도 늦지 않다.

다음 표가 결정에 도움이 될 것이다.

| 상황 | 권장 |
|---|---|
| boolean 한 개, 토글만 | useState |
| 검색어, 폼 단일 필드 | useState |
| 두세 개 값이 같은 사건에 함께 움직인다 | useReducer 검토 시작 |
| 핸들러가 4개 이상이고 값을 다르게 갱신한다 | useReducer |
| 복잡한 도메인 사건들(추가/수정/삭제/병합) | useReducer 강추 |
| 시간여행/되돌리기/감사 로그가 필요하다 | useReducer 거의 필수 |

판단이 애매할 땐 useState로 시작하고, 핸들러가 늘면서 같은 종류의 갱신이 흩어지기 시작할 때 옮기는 편이 낫다. **"옮기는 비용은 늦게 치를수록 줄어든다"가 reducer의 진실**이다. 미리 reducer로 짜 두면 보일러플레이트만 늘리고 머잖아 다시 useState로 회귀하기 십상이다. Dan Abramov가 "useReducer is the cheat mode of Hooks"라고 말한 것의 본뜻은, "필요할 때 꺼낼 수 있는 강한 카드"이지 "처음부터 깔고 시작할 카드"가 아니라는 점이다.

## 불변성 유지 — spread 패턴과 Immer

reducer는 새 state를 *돌려줘야* 한다. 받은 state를 직접 변형하면 안 된다. 그래서 위 예제들에서 우리는 `...state`, `state.tasks.map(...)` 같은 spread/map/filter를 적극 썼다. 이것이 React 외부에서도 통하는 일반적인 *불변 갱신*(immutable update) 패턴이다.

문제는 깊이가 깊어질 때다. 트리 구조 데이터에서 특정 노드 하나만 토글하려면 spread 체인이 끔찍하게 길어진다.

```tsx
// 깊은 중첩에서 불변 갱신은 끔찍해진다
type Travel = {
  rootIds: number[];
  byId: Record<number, { id: number; title: string; visited: boolean; childIds: number[] }>;
};

function reducer(state: Travel, action: { type: 'visited/toggled'; id: number }): Travel {
  return {
    ...state,
    byId: {
      ...state.byId,
      [action.id]: {
        ...state.byId[action.id],
        visited: !state.byId[action.id].visited,
      },
    },
  };
}
```

세 단계만 들어가도 손이 떨린다. 이런 종류의 코드를 한 컴포넌트에 두 개만 써 봐도 다음 사람이 누군가에게 욕을 할 가능성이 매우 높다. 그래서 자주 쓰는 도구가 [Immer](https://immerjs.github.io/immer/)다. Immer는 불변 갱신을 *마치 mutate처럼* 적게 해 준다.

```tsx
// useImmerReducer로 mutate 스타일 — Immer가 내부에서 새 객체를 만든다
import { useImmerReducer } from 'use-immer';

type Action = { type: 'visited/toggled'; id: number };

function reducer(draft: Travel, action: Action) {
  switch (action.type) {
    case 'visited/toggled':
      // 직접 변형처럼 보이지만, Immer가 변경 내역을 추적해 새 객체를 만든다
      draft.byId[action.id].visited = !draft.byId[action.id].visited;
      return; // 명시적으로 새 객체를 돌려주지 않아도 된다
  }
}

function TravelPlan() {
  const [state, dispatch] = useImmerReducer(reducer, initialTravel);
  // ...
}
```

`draft`라는 인자를 mutate해도, 내부적으로 Immer가 변경 내역을 추적해 진짜로는 새 객체를 만들어 돌려준다. 코드가 사람 눈에 훨씬 친절해진다. 다만 의존성을 하나 더 들이는 것이므로 트레이드오프를 따져 봐야 한다.

내 권장은 다음과 같다.

- **state가 평탄하다** — 일반 spread로 쓰자. Immer 도입 비용이 이득보다 크다.
- **state에 1~2단계 중첩이 있다** — 그래도 spread로 버틸 만하다. 단, 헬퍼 함수로 일부 묶자(`updateById(byId, id, patch)`).
- **3단계 이상 중첩 또는 트리 구조다** — 평탄화(normalize)를 먼저 검토하라. 평탄화로도 안 풀리면 Immer를 쓰자.
- **팀 차원에서 Immer를 표준으로 쓴다** — 일관성을 따르자.

평탄화가 늘 가능하지는 않지만, 가능하다면 그 자체로 큰 리워드가 있다. 같은 ID를 가리키는 두 곳에서의 갱신이 자동으로 동기화되고, 트리 깊이에 따른 spread 체인이 사라진다. 4장에서 본 "선택은 ID로 저장하라"의 원칙을 떠올려 보자. 그 원칙의 자연스러운 다음 걸음이 reducer + 평탄화다.

## 함수형 update와 reducer의 관계

useState를 좀 써 본 사람이라면 `setCount(prev => prev + 1)` 같은 함수형 업데이트를 본 적이 있을 것이다. 이 패턴과 reducer는 사실 한 식구다. 함수형 update는 "현재 state에서 새 state로의 변환 함수"를 React에 넘기는 것이고, reducer는 "현재 state와 action을 받아 새 state를 돌려주는 함수"를 React에 넘기는 것이다. 즉 **reducer는 함수형 update의 일반화**다.

이 관점이 왜 중요할까? Effect나 콜백에서 stale closure 문제를 만났을 때, 의존성 배열을 늘리는 대신 *현재 state를 직접 읽지 않게* 코드를 바꿀 수 있기 때문이다. dispatch는 state에 의존하지 않는다. dispatch의 참조는 변하지 않는다. 그래서 "지금 state 값과 무관하게 의도만 보내는" 코드를 짤 수 있다. 이것이 Dan Abramov가 "useReducer는 의존성 사슬을 끊는 cheat mode"라고 말한 진짜 의미다. 7장과 8장에서 effect의 의존성 문제를 다룰 때 다시 만나게 될 것이다. 지금은 이 한 줄만 기억해 두자. **상태를 읽어서 결정하지 말고, 의도를 보내자.**

## 제법 큰 예제 — 위저드 한 입 맛보기

reducer가 진가를 보이는 자리는 작은 폼이 아니라 *상태가 단계적으로 진화하는 화면*이다. 그 단적인 예가 멀티스텝 폼 위저드다. 본격적인 구현은 연습 문제에서 직접 해 보겠지만, 형태만 미리 슬쩍 보자.

```tsx
type WizardState = {
  step: 1 | 2 | 3;
  account: { email: string; password: string };
  profile: { name: string; bio: string };
  prefs: { newsletter: boolean; theme: 'light' | 'dark' };
};

type WizardAction =
  | { type: 'account/changed'; field: 'email' | 'password'; value: string }
  | { type: 'profile/changed'; field: 'name' | 'bio'; value: string }
  | { type: 'prefs/changed'; field: 'newsletter' | 'theme'; value: any }
  | { type: 'step/advanced' }
  | { type: 'step/retreated' }
  | { type: 'wizard/reset' };
```

위저드는 여러 단계의 상태가 한 컴포넌트 안에 누적되고, "다음", "이전", "처음부터" 같은 사건이 분명한 의도 단위로 발생하는 화면이다. 이 정도 복잡도에선 reducer 없이 useState로 짜는 게 차라리 고통스럽다. 한 화면이 다른 화면의 데이터를 읽어야 하고, "처음부터" 버튼은 모든 단계의 데이터를 한 번에 리셋해야 하기 때문이다. reducer라면 `case 'wizard/reset'`에 `return initialState` 한 줄이면 끝이다.

이런 경우엔 reducer가 진정한 가치를 발한다. 갱신 로직이 한 곳에 모이는 것뿐 아니라, "wizard라는 도메인이 가질 수 있는 사건의 카탈로그"가 코드로 표현되는 것이다. 후임 개발자가 이 reducer만 읽어도 "이 위저드에서 무슨 일이 일어날 수 있는지"가 한눈에 들어온다. 그것이 우리가 reducer를 도입하면서 진짜로 얻는 것이다.

## 핵심 정리

- **흩어진 setState 12군데는 보일러플레이트가 아니라 신호다.** 갱신 로직을 한 함수로 모으자. 그 함수가 reducer다.
- **reducer는 `(state, action) => newState` 형태의 순수 함수다.** ID 생성, 타임스탬프, fetch, 직접 mutate는 절대 reducer 안에 두지 말자.
- **부수효과가 필요하면 호출 측 핸들러에서 미리 만들어 페이로드로 넘긴다.** reducer는 합치기만 한다.
- **액션 이름은 사용자 의도, 페이로드는 그 의도를 표현하는 최소한의 데이터.** setter 이름을 그대로 옮긴 `SET_XXX` 액션은 useState만도 못하다.
- **TypeScript discriminated union으로 액션을 모델링하자.** 마지막에 `_exhaustive: never` 가드를 두면 케이스 누락을 컴파일러가 잡아 준다.
- **너무 잘게 쪼갠 액션도, 한 덩어리로 뭉뚱그린 액션도 좋지 않다.** "한 문장으로 설명되면 한 액션, 두 문장으로 갈리면 두 액션"이 한 가지 휴리스틱이다.
- **단일 boolean 토글이나 분산되지 않은 단일 값은 useState가 낫다.** reducer는 cheat mode이지 default mode가 아니다.
- **불변 갱신이 끔찍해질 때는 평탄화를 먼저, 그래도 부족하면 Immer.** 일단 평탄화로 풀리는지부터 따져 보자.
- **함수형 update는 reducer의 작은 형제다.** 의존성 사슬이 골치 아플 땐 "상태를 읽어 결정"하지 말고 "의도만 dispatch"하자.
- **reducer는 단위 테스트가 매우 쉽다.** 컴포넌트 트리도 모킹도 필요 없이 함수 호출만으로 검증된다.

## 연습 문제

### [기초] useState 3개를 useReducer로 합치기

다음 컴포넌트는 카운터, 단계, 메모를 useState 3개로 들고 있다. 핸들러가 흩어져 있다.

```tsx
// 출발점
function Counter() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);
  const [memo, setMemo] = useState('');

  function handleIncrement() {
    setCount(count + step);
    setMemo(`+${step} 적용`);
  }

  function handleReset() {
    setCount(0);
    setMemo('초기화');
  }

  // ...
}
```

이를 useReducer로 옮겨라.
- 액션: `'incremented'`, `'step/changed'`, `'reset'`.
- step은 `'step/changed'` 액션으로만 변경되도록.
- reducer는 한 함수에 모이고, 핸들러는 dispatch만 호출하게.

검증 포인트: reducer가 순수 함수로 작성됐는가? 액션 타입이 discriminated union인가? `_exhaustive: never` 가드가 있는가?

### [중] 폼 상태를 reducer로 — 단일 vs 필드별 액션 비교

다음 폼을 두 가지 방식으로 모두 작성해 보고, 어느 쪽이 더 깔끔한지 비교하라.

```tsx
type FormState = {
  name: string;
  email: string;
  agree: boolean;
};

// 방식 A — 필드별 액션
type ActionA =
  | { type: 'name/changed'; value: string }
  | { type: 'email/changed'; value: string }
  | { type: 'agree/toggled' }
  | { type: 'reset' };

// 방식 B — 단일 change 액션
type ActionB =
  | { type: 'field/changed'; field: 'name' | 'email'; value: string }
  | { type: 'agree/toggled' }
  | { type: 'reset' };
```

질문: 필드가 5개로 늘었을 때 어느 쪽이 변경에 강한가? 사용자가 "이름을 바꿨을 때만 자동완성"을 원한다면 어느 쪽이 적합한가? 나라면 둘 중 어느 쪽을 기본으로 두고 어떨 때 다른 쪽으로 갈까? 답을 직접 적어 보자.

### [도전] 멀티스텝 폼 위저드

3단계로 구성된 회원가입 위저드를 reducer로 만들어라.

요구사항:
- step 1: 계정 정보 입력 (email, password)
- step 2: 프로필 입력 (name, bio)
- step 3: 환경설정 (newsletter 동의 여부, 테마)
- "다음" 버튼: 다음 단계로 진행. step 1에선 email/password 모두 비어 있지 않을 때만.
- "이전" 버튼: 이전 단계로. 이전 단계의 데이터는 그대로 보존.
- "처음부터" 버튼: 모든 데이터 + step을 초기 상태로 리셋.
- 마지막 단계의 "제출" 버튼: 핸들러에서 콘솔로 전체 상태를 출력 (네트워크 호출 흉내).

힌트: state는 `{ step, account, profile, prefs }` 한 객체로 두자. action은 영역/사건 명명 규칙으로(`'account/changed'`, `'step/advanced'`, `'wizard/reset'`). reducer 안에서 분기 검증("email이 비어 있으면 step/advanced 무시")을 할지, 핸들러에서 검증한 뒤 dispatch할지 두 방안을 모두 시도해 보고 차이를 적어 보자.

심화: 제출 직후 5초간 "되돌리기"를 허용하려면 reducer를 어떻게 확장해야 할까? (힌트: `history` 필드)

## 마무리 — 그리고 dispatch는 어떻게 멀리까지 흘려보낼까

reducer는 갱신 로직을 한 곳에 모아 주는 강력한 도구다. 그 결과 컴포넌트는 "사용자가 무엇을 했는지"를 dispatch로 외치는 일에만 집중하게 된다. 우리는 이 장에서 흩어진 setState의 증상을 짚어 보고, useState에서 useReducer로 옮기는 절차를 손에 익히고, reducer가 순수 함수여야 하는 이유와 액션을 사용자 의도 단위로 짓는 원칙을 연습했다. 마지막엔 reducer가 과한 경우와 적절한 경우의 경계도 그려 보았다.

그런데 reducer로 행동을 한 곳에 모았다고 해서 모든 게 풀리는 건 아니다. 새로운 질문이 떠오른다. **이 dispatch는 어디까지 흘려보내야 할까?** 위저드의 한 단계가 아주 깊은 자식 컴포넌트라면? 칸반의 카드가 트리의 5단 아래에 있다면? 그때마다 dispatch를 props로 5단을 내려 보내야 할까? 그렇게 시작하는 prop drilling은 또 다른 형태의 *흩어짐*이다.

다음 6장에서는 그 답을 함께 찾는다. Context를 언제 꺼내고, 언제 너무 빠르게 꺼내선 안 되는지, 그리고 reducer와 Context를 어떻게 깔끔히 결합해 "행동의 카탈로그를 트리 어디서든 dispatch할 수 있는" 구조로 만들어 가는지를 살펴보자. 우리는 이미 reducer라는 카드를 손에 쥐었다. 이제 그 카드를 적절한 거리에 적절히 펼치는 법을 익힐 차례다.
