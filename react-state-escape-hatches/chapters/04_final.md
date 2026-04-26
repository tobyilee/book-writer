# 4장. 보존과 리셋 — `key`가 정말로 하는 일

이런 상황을 한 번 상상해보자. 메신저 앱을 만들고 있다. 왼쪽에 친구 목록이 있고, 친구를 클릭하면 오른쪽에 채팅 입력창이 뜬다. 입력창에는 아직 보내지 않은 초고를 그대로 두는 기능까지 넣었다. 사용자는 친구 A에게 보낼 메시지를 한참 쓰다가, 마음이 바뀌어 친구 B를 클릭한다. 그런데 입력창에는 A에게 쓰던 그 초고가 그대로 남아 있다. 사용자가 이걸 알아채지 못하고 그대로 전송 버튼을 누르면? 친구 B는 영문도 모를 메시지를 받게 된다.

코드를 들여다보면 이상한 점은 없다. `selectedContact` 상태가 바뀌었고, `Chat` 컴포넌트는 새 `contact` prop을 받았다. 분명히 새 사람을 위한 채팅 화면이 그려졌어야 한다. 그런데 입력창의 `useState`는 마치 아무 일도 없었다는 듯, 이전 텍스트를 그대로 들고 있다. 난감하다. 분명히 새 컴포넌트가 그려진 것 같은데, React는 같은 컴포넌트로 취급한 모양이다.

이 상황은 React를 한참 써본 개발자도 종종 만난다. 그리고 이 버그를 진단하려면, 평소에 별 의심 없이 지나쳤던 한 가지 질문을 정면으로 마주해야 한다. **React는 어떤 기준으로 "같은 컴포넌트"와 "다른 컴포넌트"를 구분하는가?** 같은 자리에 같은 모양으로 그려졌으면 같은 컴포넌트인가? 아니면 props가 같으면 같은 컴포넌트인가? 그것도 아니면, 이름이 같으면 같은 컴포넌트인가?

답은 처음 들으면 조금 의외다. React가 정체성의 기준으로 삼는 것은 props도, 이름도, 내용도 아니다. **트리에서의 위치**다. 그리고 이 한 줄을 제대로 받아들이는 순간, "왜 이 state가 안 사라지지?", "왜 이 state가 자꾸 사라지지?"라는 두 종류의 골치 아픈 버그가 한꺼번에 정리된다. 이번 장에서는 그 위치라는 개념을 차근차근 풀어보고, 의도적으로 state를 보존하거나 리셋하기 위한 `key`라는 도구를 손에 익혀보자.

## 같은 자리, 같은 컴포넌트, 같은 타입

React가 state를 보존할지 버릴지 결정할 때 보는 것은 정확히 세 가지다. 첫째, 트리에서 **같은 위치**인가. 둘째, **같은 타입의 컴포넌트**인가. 셋째, 이전 렌더에서 그 자리에 무엇이 있었는가.

말로만 하면 추상적이니 코드로 보자.

```tsx
// Counter.tsx — 단순한 카운터 컴포넌트
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount((c) => c + 1)}>
      count: {count}
    </button>
  );
}
```

```tsx
// App.tsx — 같은 컴포넌트를 두 번 그린다
import { useState } from 'react';
import { Counter } from './Counter';

export function App() {
  const [showSecond, setShowSecond] = useState(true);

  return (
    <div>
      <Counter />
      {/* 두 번째 카운터는 토글로 켜고 끌 수 있다 */}
      {showSecond && <Counter />}
      <button onClick={() => setShowSecond((v) => !v)}>
        두 번째 카운터 토글
      </button>
    </div>
  );
}
```

이 화면에서 두 카운터를 각각 3번, 5번 눌러 두 카운터의 값을 다르게 만든 뒤, "두 번째 카운터 토글" 버튼을 눌러 두 번째 카운터를 사라지게 했다가 다시 켜보자. 어떻게 될까?

두 번째 카운터의 값은 0으로 리셋된다. 첫 번째 카운터는 3을 그대로 유지한다. 같은 `Counter` 컴포넌트이고, 같은 코드인데, 왜 한쪽만 살아남고 한쪽은 죽었을까?

이유는 단순하다. 두 번째 카운터는 한 번 트리에서 사라졌다가 다시 들어왔다. React 입장에서는 "그 자리에 있던 컴포넌트가 사라졌으니 state를 같이 버리고, 다시 들어온 건 처음 보는 새 컴포넌트"인 셈이다. 첫 번째 카운터는 트리에서 단 한 번도 빠진 적이 없다. 그래서 같은 자리에 같은 타입의 컴포넌트가 계속 있었고, state는 자연스럽게 보존된다.

여기서 가장 중요한 단어는 **"자리"**다. 자바스크립트 코드의 줄 번호도, JSX의 변수 이름도 아니다. React가 머릿속에 그리는 가상 DOM 트리에서의 위치다. 같은 위치에 같은 타입이 계속 있으면, React는 "음, 같은 친구네"라고 판단한다. 위치가 같더라도 타입이 바뀌었거나, 잠깐이라도 사라졌다 돌아오면, "다른 친구네"라고 판단한다.

## 위치가 정체성이다

이 원칙이 처음에는 좀 이상하게 느껴질 수 있다. 같은 컴포넌트를 그렸으면 같은 정체성을 가져야 하는 것 아닌가? 왜 위치가 그렇게 중요할까?

이 질문에 답하기 전에, React가 처한 상황을 한번 생각해보자. React는 매 렌더마다 새로운 JSX 트리를 받는다. 이전 트리와 새 트리를 비교해서 어디가 바뀌었는지 알아내야 한다. 그런데 두 트리의 **각 노드를 무엇으로 매칭**할 것인가?

이름으로 매칭하자니, 같은 컴포넌트를 두 개 이상 쓰는 경우가 너무 흔하다. props로 매칭하자니, props는 매번 바뀌는 것이 정상이다. 그래서 React가 택한 가장 단순하고 빠른 휴리스틱이 바로 **"같은 부모 아래 같은 위치에 같은 타입이 있으면, 같은 노드로 본다"**이다.

이 규칙은 빠르고 단순하다. 그리고 거의 모든 경우에 우리가 원하는 결과를 준다. 같은 자리에 같은 컴포넌트가 계속 있다는 것은 보통 "그게 같은 컴포넌트라는 뜻"이기 때문이다. 사용자 입장에서도 화면의 같은 자리에 같은 모양으로 보이면 자연스럽게 같은 것으로 인식한다.

문제는 우리의 의도와 React의 휴리스틱이 어긋나는 순간에 생긴다. 채팅 입력창의 예시처럼 말이다. 같은 자리에 같은 `Chat` 컴포넌트가 그려져 있으니 React 입장에서는 "같은 친구네"라고 판단한다. 그런데 우리는 "사람이 바뀌었으니 다른 친구"라고 보고 싶다. 이 어긋남을 메우는 도구가 바로 `key`다.

## 트리 구조가 같으면 state는 살아남는다

위치가 정체성이라는 말을 좀 더 단단히 이해해보자. 다음 코드를 살펴보자.

```tsx
// 같은 Counter를 isFancy 조건에 따라 다른 div로 감싼다
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount((c) => c + 1)}>
      count: {count}
    </button>
  );
}

export function App() {
  const [isFancy, setIsFancy] = useState(false);

  return (
    <div>
      {isFancy ? (
        <div className="fancy">
          <Counter />
        </div>
      ) : (
        <div>
          <Counter />
        </div>
      )}
      <label>
        <input
          type="checkbox"
          checked={isFancy}
          onChange={(e) => setIsFancy(e.target.checked)}
        />
        화려하게 보기
      </label>
    </div>
  );
}
```

카운터를 5까지 올려놓고 "화려하게 보기" 체크박스를 켰다 껐다 해보자. count는 5에서 안 움직이고 그대로 유지된다. 왜일까?

JSX만 보면 `isFancy`가 true일 때와 false일 때 코드가 두 갈래로 나뉜다. 하지만 React가 보는 트리 구조는 둘 다 같다. 가장 바깥 `div` 아래의 첫 번째 자식은 `div`이고, 그 안에 `Counter`가 있다. `className`이 바뀌었을 뿐 위치는 동일하다. React는 "같은 자리에 같은 `Counter`가 계속 있구나"라고 판단하고, state를 보존한다.

이번엔 살짝만 비틀어보자.

```tsx
// 한쪽은 div로 감싸고 한쪽은 section으로 감싼다
{isFancy ? (
  <section>
    <Counter />
  </section>
) : (
  <div>
    <Counter />
  </div>
)}
```

같은 카운터인데 부모만 `div`에서 `section`으로 바뀌었다. 결과는? 체크박스를 토글할 때마다 count가 0으로 리셋된다. 부모의 타입이 달라지면 그 아래 트리는 통째로 새로 만든 것으로 취급되기 때문이다.

이 두 코드 차이가 실무에서 골치 아픈 버그의 진원지가 되곤 한다. 디자인을 살짝 바꾸려고 `div`를 `section`으로 바꿨더니, 그 안의 모든 입력 폼이 비워진다. "왜 갑자기 입력값이 사라지지?" 한참 헤매다가 git diff를 보고 한숨이 나온다. 트리 구조는 보이지 않게 정체성을 결정한다는 것을 잊지 말자.

## 다른 정체성이라면 — `key`로 명시적으로 알린다

자, 이제 반대 방향의 문제로 돌아가자. 같은 자리에 같은 타입 컴포넌트가 그려지지만, 우리는 "다른 정체성"으로 다루고 싶을 때 어떻게 할까?

답은 React가 우리에게 쥐어준 단 하나의 명시적 신호, `key`다.

```tsx
// 친구를 클릭하면 그 친구에 대한 채팅 화면을 띄운다
import { useState } from 'react';

type Contact = { id: string; name: string };

const contacts: Contact[] = [
  { id: 'alice', name: '앨리스' },
  { id: 'bob', name: '밥' },
  { id: 'carol', name: '캐럴' },
];

function Chat({ contact }: { contact: Contact }) {
  // 사용자가 입력 중인 메시지 초고
  const [draft, setDraft] = useState('');
  return (
    <section>
      <h2>{contact.name}에게 보내는 메시지</h2>
      <textarea
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        placeholder="메시지를 입력하세요..."
      />
    </section>
  );
}

export function Messenger() {
  const [selected, setSelected] = useState<Contact>(contacts[0]);

  return (
    <div className="messenger">
      <ul>
        {contacts.map((c) => (
          <li key={c.id}>
            <button onClick={() => setSelected(c)}>{c.name}</button>
          </li>
        ))}
      </ul>
      {/* 핵심: key를 contact.id로 묶어준다 */}
      <Chat key={selected.id} contact={selected} />
    </div>
  );
}
```

핵심은 `<Chat key={selected.id} contact={selected} />` 단 한 줄이다. `key`가 바뀌면 React는 그 자리에 새로운 `Chat` 컴포넌트가 들어왔다고 판단한다. 같은 위치에 같은 타입이지만, `key`가 달라졌으니 정체성이 다르다고 본다는 뜻이다. 그래서 이전 `Chat`은 통째로 폐기되고, 새 `Chat`이 처음부터 마운트된다. 그 안의 `useState('')`도 당연히 처음부터 다시 시작한다. 초고는 깨끗하게 비워진다.

`key`는 리스트 렌더링에서나 쓰는 거 아니냐는 인상을 가진 사람이 많다. 물론 리스트에서 가장 자주 쓰는 게 맞다. 하지만 `key`의 본질은 리스트가 아니라 **"이 자리에 있는 컴포넌트의 정체성을 명시적으로 지정한다"**는 것이다. 단일 자식에도 `key`를 붙일 수 있고, 그 의미는 "이 친구가 누구인지 내가 직접 알려줄게"이다.

`<Chat key={userId} />` 단 한 줄로, 사용자가 바뀔 때마다 폼을 깨끗하게 리셋하는 패턴은 정말 자주 쓰인다. 모달 안에 입력 폼이 있는데 다른 항목으로 모달을 다시 열 때, 탭에 따라 다른 데이터를 편집해야 할 때, 라우트 파라미터에 따라 다른 페이지를 보여줄 때 등등. 외워둘 만한 패턴이다.

## 의도치 않은 보존이라는 함정

위치가 정체성이라는 규칙은 두 방향으로 우리를 골탕 먹인다. 하나는 방금 본 것처럼 **"리셋되어야 할 state가 보존되는"** 경우다. 또 하나는 **"보존되어야 할 state가 리셋되는"** 경우다. 먼저 보존 쪽 함정을 좀 더 살펴보자.

가장 흔한 함정은 조건부 렌더링이다.

```tsx
// 이 코드는 의도와 다르게 동작한다
function App() {
  const [isPlayerA, setIsPlayerA] = useState(true);

  return (
    <div>
      {isPlayerA ? (
        <Counter person="태일러" />
      ) : (
        <Counter person="사라" />
      )}
      <button onClick={() => setIsPlayerA((v) => !v)}>
        다음 플레이어
      </button>
    </div>
  );
}
```

이 코드는 두 플레이어의 점수를 따로 추적하려는 의도로 보인다. 태일러가 5점이었다가 다음 플레이어로 넘기면 사라가 새로 0점부터 시작하길 기대한다. 하지만 실제로는 태일러의 5점이 그대로 사라에게 옮겨간다. 다시 태일러로 돌아오면 그 5점은 또 그대로다. 무슨 일일까?

같은 위치, 같은 `Counter` 타입이라는 점이 정확히 적용된 결과다. JSX의 ternary 양쪽 가지 모두 첫 번째 자식이 `Counter`다. React 입장에서는 "props만 바뀌었네, state는 그대로"라고 판단한다. 사용자 입장에서는 두 사람이 점수 계산기를 공유하는 황당한 상황이 벌어진다.

이 함정을 풀어내는 방법은 두 가지다.

```tsx
// 방법 1: key로 정체성을 명시한다
{isPlayerA ? (
  <Counter key="taylor" person="태일러" />
) : (
  <Counter key="sara" person="사라" />
)}
```

```tsx
// 방법 2: 트리 위치를 다르게 둔다 (둘 다 그리고 하나는 숨김)
<div>
  {isPlayerA && <Counter person="태일러" />}
  {!isPlayerA && <Counter person="사라" />}
</div>
```

방법 1이 보통 더 명료하다. 두 가지가 같은 자리에 들어오지만 다른 정체성임을 코드로 직접 선언하기 때문이다. 방법 2는 위치 자체를 분리해서 우회한다.

또 다른 흔한 함정은 같은 타입이지만 의미가 다른 컴포넌트를 같은 자리에 그리는 경우다. 예컨대 `EditUserForm`이 `userId` prop에 따라 다른 사용자를 편집한다고 해보자.

```tsx
// userId가 바뀌면 폼 안의 입력값을 비워야 하는데...
function EditUserForm({ userId }: { userId: string }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  // 서버에서 userId로 사용자 정보를 가져와서 채워주는 로직 (생략)
  return (
    <form>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
    </form>
  );
}
```

부모에서 이 컴포넌트를 `<EditUserForm userId={selectedId} />`로 그리면, `selectedId`가 바뀌어도 `name`과 `email` state는 그대로 살아남는다. 사용자 A를 편집하다가 B로 바꿨는데 입력란에 A의 정보가 남아 있다면, 사용자에게 의도치 않은 데이터가 노출되거나 잘못 저장될 수 있다. 끔찍한 일이다.

처방은 같다. `<EditUserForm key={selectedId} userId={selectedId} />`. 한 줄이 모든 것을 해결한다.

여기서 잠깐 이런 의문이 들 수 있다. `useEffect`로 `userId` 변화에 반응해서 state를 비우면 되지 않을까?

```tsx
// 안티패턴: effect로 prop 변화에 반응해 state를 리셋
useEffect(() => {
  setName('');
  setEmail('');
}, [userId]);
```

물론 동작은 한다. 하지만 권장하지 않는다. 왜냐하면 effect는 렌더가 끝난 다음에 실행되기 때문이다. 사용자는 한 프레임 동안 이전 값이 남아 있는 화면을 본다. 그다음 effect가 실행되어 state가 비워지면, 다시 한 번 렌더가 일어난다. 즉, **한 박자 늦게 깜빡이는** 화면을 보게 된다. 미묘하지만 거슬리고, 가끔은 자식 컴포넌트로 이전 값이 props로 잠깐 흘러들어가 다른 effect를 잘못 트리거하기도 한다.

`key`로 리셋하면 이런 일이 없다. 왜냐하면 `key`가 바뀐 시점에 React가 이전 컴포넌트를 통째로 unmount하고 새 컴포넌트를 mount하기 때문이다. 사용자는 처음부터 깨끗한 새 화면을 본다. 한 박자 늦은 깜빡임은 없다. **prop 변화에 effect로 반응해서 state를 리셋하는 패턴은, `key`로 옮겨서 끝내는 편이 낫다.** 이 점은 11장에서도 다시 짧게 언급할 텐데, 본격적인 처방은 여기서 마무리짓자.

물론 모든 경우를 `key`로 풀 수는 없다. prop이 바뀔 때 일부 state만 리셋하고 일부는 보존하고 싶다면 어떻게 할까? 그럴 때는 다음 패턴을 쓴다.

```tsx
// 렌더 중 set 패턴 — prop 변화에 일부 state만 리셋
function ItemList({ items }: { items: Item[] }) {
  const [selection, setSelection] = useState<string | null>(null);
  const [prevItems, setPrevItems] = useState(items);

  // items 참조가 바뀌면 selection만 비운다 (다른 state는 그대로)
  if (items !== prevItems) {
    setPrevItems(items);
    setSelection(null);
  }

  return (
    <ul>
      {items.map((item) => (
        <li
          key={item.id}
          className={selection === item.id ? 'selected' : ''}
          onClick={() => setSelection(item.id)}
        >
          {item.label}
        </li>
      ))}
    </ul>
  );
}
```

이 패턴은 처음 보면 꽤 낯설다. 렌더 중에 `setState`를 호출한다고? 무한 루프 나는 거 아냐? 다행히 이 형태는 React가 공식적으로 인정하는 패턴이다. 렌더 중에 set한 값이 같은 렌더 사이클 안에 반영되어 한 번의 렌더로 끝난다. effect로 처리할 때처럼 깜빡임이 없다는 뜻이다. 단, 조건이 있다. **외부 상태가 아니라 자기 자신의 state를 갱신할 때만**, 그리고 **무한 루프를 만들지 않도록 조건을 명확히 걸 때만** 써야 한다.

이 패턴은 일종의 미세 조정 도구다. 대부분의 경우는 그냥 `key`로 해결하는 편이 단순하고 명료하다. 진짜로 일부만 리셋해야 할 때만 꺼내 쓰자.

## 의도치 않은 리셋이라는 함정

이번엔 반대 방향의 함정으로 가보자. 보존되어야 할 state가 자꾸 리셋되는 경우다. 두 가지 흔한 원인을 살펴보자.

### 첫 번째: 배열 인덱스를 `key`로 쓰는 경우

리스트를 그릴 때 `key`로 무엇을 쓸지 고민해본 적이 있을 것이다. 데이터에 안정적인 id가 있다면 그것을 쓰는 게 정답이다. 그런데 id가 마땅치 않을 때 무심코 배열 인덱스를 쓰곤 한다.

```tsx
// 안티패턴: 인덱스를 key로 쓴다
function TodoList({ todos }: { todos: Todo[] }) {
  return (
    <ul>
      {todos.map((todo, index) => (
        <TodoItem key={index} todo={todo} />
      ))}
    </ul>
  );
}
```

리스트 항목이 추가되거나 삭제되거나 순서가 바뀌지 않는 한, 이 코드는 별 문제가 없어 보인다. 하지만 사용자가 두 번째 항목을 삭제하면 어떻게 될까? 원래 인덱스 0, 1, 2였던 항목들이 삭제 후엔 인덱스 0, 1이 된다. 즉, **세 번째 항목이 갑자기 인덱스 1이 되어 두 번째 항목 자리로 밀려들어온다**. React 입장에서는 "어, 인덱스 1번 자리의 키 1은 그대로네"라고 판단한다. 그래서 이전 두 번째 항목의 state(예: 입력 중이던 내용, 펼침 상태)가 새로 옮겨온 세 번째 항목에 그대로 남는다.

사용자 입장에서는 세 번째 할 일을 클릭했는데 두 번째 할 일에서 입력하던 텍스트가 따라온 것처럼 보인다. 찜찜하다 못해 황당한 버그다.

처방은 단순하다. **항목 자체에 안정적인 식별자를 부여하고, 그것을 key로 쓰자.**

```tsx
// 처방: 안정적인 id를 key로 쓴다
function TodoList({ todos }: { todos: Todo[] }) {
  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </ul>
  );
}
```

서버에서 받아오는 데이터라면 보통 `id` 필드가 있다. 클라이언트에서 즉석으로 만든 항목이라면 `crypto.randomUUID()`나 `Date.now()` 같은 것으로 한 번만 부여해두면 된다. 한 번 정해진 id는 리스트가 어떻게 바뀌어도 따라다닌다.

배열 인덱스를 `key`로 써도 괜찮은 경우가 있긴 하다. 리스트가 끝까지 정적이고, 항목이 추가·삭제·재정렬되지 않으며, 각 항목에 의미 있는 자체 state도 없다면 인덱스 key가 큰 문제를 일으키지 않는다. 하지만 이 조건들을 다 만족한다고 자신할 수 있는 경우가 생각보다 적다. 안전하게 가려면 항상 안정적인 id를 쓰는 편이 낫다. **stable id의 무게는 결코 가볍지 않다.** 잊지 말자.

### 두 번째: 컴포넌트 안에 컴포넌트를 정의하는 경우

이건 좀 더 미묘하지만 한번 만나면 식은땀이 나는 함정이다.

```tsx
// 안티패턴: 컴포넌트 안에 컴포넌트를 정의한다
function ParentComponent() {
  const [value, setValue] = useState('');

  // 매 렌더마다 새로 만들어지는 컴포넌트
  function InnerInput() {
    const [localValue, setLocalValue] = useState('');
    return (
      <input
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value)}
      />
    );
  }

  return (
    <div>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <InnerInput />
    </div>
  );
}
```

`ParentComponent`의 `value` 입력란에 글자를 한 자 한 자 칠 때마다 어떤 일이 일어날까? `value`가 바뀌면 `ParentComponent`가 리렌더된다. 리렌더되면 `InnerInput` 함수가 **다시 정의된다**. 즉, 매 렌더마다 새로운 함수 객체가 만들어진다. React 입장에서는 이전 렌더의 `InnerInput`과 이번 렌더의 `InnerInput`이 **다른 컴포넌트 타입**이다. 같은 자리에 다른 타입이 들어왔으니, 이전 `InnerInput`은 unmount되고 새 `InnerInput`이 mount된다.

결과? 사용자가 `InnerInput`에 글자를 칠 때마다 부모가 리렌더되고, 그때마다 `InnerInput`이 통째로 리셋된다. 사용자는 한 글자도 입력할 수 없다. 또는 이상하게 한 글자만 남고 사라지는 화면을 본다. 디버깅이 정말 힘들다. 코드를 아무리 봐도 "아니 매 글자마다 왜 리셋되지?" 싶고, `console.log`를 찍어봐도 props는 잘 들어가는데 state만 쓱 사라진다.

처방은 간단하다. **컴포넌트 정의는 항상 모듈 최상위에 두자.**

```tsx
// 처방: 컴포넌트는 모듈 최상위에서 한 번만 정의한다
function InnerInput() {
  const [localValue, setLocalValue] = useState('');
  return (
    <input
      value={localValue}
      onChange={(e) => setLocalValue(e.target.value)}
    />
  );
}

function ParentComponent() {
  const [value, setValue] = useState('');
  return (
    <div>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <InnerInput />
    </div>
  );
}
```

이렇게 하면 `InnerInput` 함수는 모듈 로드 시점에 단 한 번만 정의된다. React가 보는 컴포넌트 타입도 매 렌더마다 동일하다. 같은 자리에 같은 타입이 계속 있으니 state는 자연스럽게 보존된다.

이 안티패턴이 왜 자주 등장하는지도 같이 짚어보자. 보통은 "이 컴포넌트는 부모 안에서만 쓰니까 안에 둬도 되겠지"라는 생각으로 출발한다. 또는 클로저로 부모의 변수에 접근하고 싶어서 안에 두는 경우도 있다. 둘 다 이해할 수 있는 동기지만, 그 대가가 너무 크다.

부모의 변수에 접근하고 싶다면 props로 내려주면 된다. 모듈 최상위에 컴포넌트를 두고, 필요한 값은 prop으로 받자. 한 곳에서만 쓰는 컴포넌트라도 모듈 최상위에 두는 게 리액트 세계의 기본 매너다. **컴포넌트 정의를 함수 안에 두지 말자.** 이것은 단순한 스타일 차원의 권고가 아니라, state를 살리거나 죽이는 진짜 결정이다.

## 위치 정체성 모형을 머리에 그려두기

지금까지 살펴본 함정들을 한 번에 꿰는 정신 모형이 있다. 그것을 정리하고 다음 절로 넘어가자.

React가 매 렌더마다 하는 일을 거칠게 묘사하면 이렇다.

1. 새 JSX 트리를 받는다.
2. 이전 트리와 같은 위치에 있는 노드들을 짝지어 본다.
3. 짝지어진 노드의 타입이 같으면, 그 자리의 state를 보존하고 props만 갱신한다.
4. 타입이 다르거나 짝이 없으면, 이전 노드를 unmount하고 새 노드를 mount한다.

여기서 "위치"는 트리 구조에서의 위치고, 같은 부모 아래 같은 인덱스라는 뜻이다. "타입"은 컴포넌트 함수의 참조 동일성이다. 같은 이름이라도 매 렌더마다 다시 정의되는 함수는 다른 타입이다.

`key`는 이 매칭 규칙에 우리가 직접 끼어드는 도구다. 같은 위치, 같은 타입이지만 `key`가 다르면 React는 다른 노드로 본다. 같은 위치, 같은 타입, 같은 `key`면 React는 같은 노드로 본다.

이 모형을 머리에 두고 보면, 앞서 본 모든 함정이 같은 원리의 다른 얼굴임을 알 수 있다. 채팅 입력창에 이전 사용자 텍스트가 남는 것은 위치가 같고 타입이 같아서다. 인덱스를 key로 썼을 때 항목 state가 옆 항목으로 새는 것은 인덱스가 같으니 위치가 같다고 React가 판단해서다. 컴포넌트 안에 컴포넌트를 정의했을 때 매 글자마다 리셋되는 것은 매 렌더마다 타입이 새로 만들어져서다. 모든 함정의 뿌리는 위치-타입-key 매칭 규칙이라는 단 하나다.

그러니 "왜 이 state가 안 사라지지?"라는 의문이 들면 자문해보자. **같은 위치, 같은 타입, 같은 key인가?** 그렇다면 보존되는 게 정상이다. 리셋하고 싶다면 `key`로 정체성을 다르게 매겨주자. "왜 이 state가 자꾸 사라지지?"라는 의문이 들면 또 자문해보자. **위치가 매 렌더마다 일정한가? 타입이 매 렌더마다 동일한 함수 참조인가? key가 매 렌더마다 안정적인가?** 셋 중 하나라도 무너지면 리셋된다.

## 핵심 정리

지금까지 다룬 내용을 한눈에 정리해두자.

1. **React가 state를 보존하는 기준은 트리 위치, 컴포넌트 타입, 그리고 `key`다.** props도 이름도 내용도 아니다.
2. **같은 위치에 같은 타입이 계속 있으면 state는 보존된다.** 이것이 React의 기본 가정이다.
3. **위치가 같더라도 타입이 바뀌면 그 자리의 state는 통째로 사라진다.** 부모 태그를 `div`에서 `section`으로 바꾸는 것만으로도 자식 트리 전체가 새로 마운트된다.
4. **`key`는 같은 위치, 같은 타입에서 정체성을 명시적으로 분리하는 유일한 도구다.** 리스트가 아니어도 쓸 수 있고, 단일 자식에도 의미가 있다.
5. **`<Form key={userId} />` 한 줄이면 사용자가 바뀔 때 폼이 깨끗하게 리셋된다.** 사용자·상대방·항목 식별자가 바뀔 때마다 폼·모달·편집 화면을 리셋해야 한다면 첫 번째 후보는 `key`다.
6. **prop 변화에 effect로 반응해 state를 리셋하지 말자.** 한 박자 늦은 깜빡임이 생긴다. `key`로 옮기는 편이 낫다. 일부만 리셋해야 한다면 렌더 중 set 패턴을 쓰자.
7. **배열 인덱스를 `key`로 쓰지 말자.** 리스트가 정렬되거나 항목이 삭제될 때 state가 옆 항목으로 새는 사고가 난다. 안정적인 id를 쓰자.
8. **컴포넌트 정의는 모듈 최상위에 두자.** 함수 안에 컴포넌트를 정의하면 매 렌더마다 새 타입이 만들어져 state가 매번 리셋된다.
9. **"왜 이 state가 안 사라지지?"는 보통 `key` 누락의 신호다.** "왜 이 state가 자꾸 사라지지?"는 보통 위치·타입·key 안정성이 깨진 신호다. 진단의 출발점은 항상 같다.
10. **위치가 정체성이라는 기본 가정을 의심하지 말고 받아들이자.** 그 위에서 우리는 `key`라는 도구로 의도를 표현한다.

## 연습 문제

### [기초] 채팅 앱 — 대화 상대를 바꾸면 입력창을 비우자

다음 코드는 친구를 바꿔도 입력 중이던 초고가 그대로 남는 버그가 있다. `ChatPanel`의 입력창을 친구가 바뀔 때마다 깨끗하게 비우도록 한 줄만 고쳐보자.

```tsx
type Friend = { id: string; name: string };
const friends: Friend[] = [
  { id: 'a', name: '앨리스' },
  { id: 'b', name: '밥' },
];

function ChatPanel({ friend }: { friend: Friend }) {
  const [draft, setDraft] = useState('');
  return (
    <div>
      <h3>{friend.name}에게</h3>
      <textarea
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
      />
    </div>
  );
}

export function App() {
  const [selected, setSelected] = useState(friends[0]);
  return (
    <div>
      {friends.map((f) => (
        <button key={f.id} onClick={() => setSelected(f)}>
          {f.name}
        </button>
      ))}
      {/* ↓ 이 줄을 한 줄만 고치면 된다 */}
      <ChatPanel friend={selected} />
    </div>
  );
}
```

힌트: `ChatPanel`에 `key={selected.id}`를 추가하자. `useEffect`나 별도의 리셋 로직을 추가하지 않고 단 한 줄로 끝낼 수 있다.

### [중] 탭 UI — 일부는 보존, 일부는 리셋

세 개의 탭(`Profile`, `Settings`, `Notes`)을 가진 화면을 만들어보자. 각 탭은 자체 입력 폼을 가진다. 요구사항은 다음과 같다.

- `Profile` 탭의 입력 내용은 다른 탭으로 갔다 와도 **보존**되어야 한다.
- `Notes` 탭의 입력 내용은 탭을 떠나면 **리셋**되어야 한다 (메모는 일회성).
- `Settings` 탭의 입력 내용은 보존하되, 사용자가 명시적으로 "초기화" 버튼을 누르면 비워져야 한다.

이 세 가지 요구사항을 어떻게 구현할까? 어디에 `key`를 붙이고, 어디에는 안 붙일까? `Settings`의 초기화 버튼은 `key`를 어떻게 활용해 구현할 수 있을까?

힌트: `Profile`은 항상 마운트된 채 두고 CSS로 숨긴다(보존). `Notes`는 활성 탭일 때만 트리에 그린다(리셋). `Settings`는 부모가 들고 있는 `resetCount` 같은 숫자를 `key`로 넘겨서, 초기화 버튼이 그 숫자를 증가시키도록 한다.

```tsx
// 골격 코드
function App() {
  const [tab, setTab] = useState<'profile' | 'settings' | 'notes'>('profile');
  const [settingsResetKey, setSettingsResetKey] = useState(0);

  return (
    <div>
      <nav>{/* 탭 버튼들 */}</nav>

      {/* Profile은 항상 그리고, 활성 탭이 아닐 때만 숨긴다 (보존) */}
      <div hidden={tab !== 'profile'}>
        <Profile />
      </div>

      {/* Settings는 항상 그리지만, key로 명시적 초기화 (조건부 보존) */}
      <div hidden={tab !== 'settings'}>
        <Settings key={settingsResetKey} />
        <button onClick={() => setSettingsResetKey((k) => k + 1)}>
          설정 초기화
        </button>
      </div>

      {/* Notes는 활성 탭일 때만 마운트 (탭 떠나면 리셋) */}
      {tab === 'notes' && <Notes />}
    </div>
  );
}
```

직접 손으로 쳐보면서 각 탭을 오가며 실험해보자. "보존"과 "리셋"의 차이가 정확히 어디서 갈리는지 몸으로 익히는 게 중요하다.

### [도전] 잘못된 key 진단하기

다음 코드는 사용자가 인풋에 텍스트를 입력한 다음 "위로" 버튼으로 항목을 정렬하면, 입력값이 엉뚱한 항목으로 옮겨가는 버그가 있다. 버그를 재현해보고 원인을 진단한 뒤, 한 글자만 수정해서 고쳐보자.

```tsx
type Item = { id: string; label: string };

function ItemRow({ item }: { item: Item }) {
  const [note, setNote] = useState('');
  return (
    <li>
      <span>{item.label}</span>
      <input
        value={note}
        onChange={(e) => setNote(e.target.value)}
        placeholder="이 항목에 대한 메모..."
      />
    </li>
  );
}

export function ItemList() {
  const [items, setItems] = useState<Item[]>([
    { id: 'apple', label: '사과' },
    { id: 'banana', label: '바나나' },
    { id: 'cherry', label: '체리' },
  ]);

  function moveUp(index: number) {
    if (index === 0) return;
    const next = [...items];
    [next[index - 1], next[index]] = [next[index], next[index - 1]];
    setItems(next);
  }

  return (
    <ul>
      {items.map((item, index) => (
        <div key={index}>
          <ItemRow item={item} />
          <button onClick={() => moveUp(index)}>위로</button>
        </div>
      ))}
    </ul>
  );
}
```

진단 절차:

1. "사과"의 메모란에 "맛있다"라고 입력한다.
2. "바나나"의 메모란에 "노랗다"라고 입력한다.
3. "바나나"의 "위로" 버튼을 누른다.
4. 어떤 메모가 어디에 붙어 있는지 관찰한다.

기대: "맛있다"는 사과를 따라가야 하고, "노랗다"는 바나나를 따라가야 한다. 실제: 메모가 자리에 그대로 남아 있다. 즉, "맛있다"가 위로 올라온 바나나에 붙어 있고, "노랗다"가 아래로 내려간 사과에 붙어 있다. 끔찍한 일이다.

원인은 명확하다. `key={index}`다. 인덱스는 항목과 함께 움직이지 않고 자리와 함께 움직인다. 그래서 React는 "0번 자리의 컴포넌트는 그대로네, state도 그대로 두자"라고 판단한다. 처방은 한 글자.

```tsx
// 수정 전
<div key={index}>
// 수정 후
<div key={item.id}>
```

`item.id`는 항목 자체를 따라다닌다. 항목이 위로 올라가면 `key`도 같이 위로 올라가고, React는 "어, 같은 컴포넌트가 자리만 바꿨네"라고 판단해 state를 항목과 함께 옮겨준다. 메모는 자기 항목을 따라간다.

도전: 이 패턴을 몸에 익히려면, 자기 코드에서 `key={index}`를 grep으로 찾아 하나씩 점검해보자. 정말로 정적이고 재정렬되지 않는 리스트인가? 항목 자체에 안정적인 id를 부여할 수는 없는가? 거의 모든 경우에 더 나은 답이 있다.

## 다음 장으로

이번 장에서 우리는 React가 state를 보존하고 리셋하는 진짜 규칙을 들여다봤다. 위치, 타입, `key`. 이 세 가지의 매칭이 모든 보존과 리셋의 운명을 결정한다는 것을, 그리고 우리가 직접 끼어들 수 있는 유일한 손잡이가 `key`라는 것을 살펴봤다. 채팅 입력창을 깨끗하게 비우고, 인덱스 키의 함정에서 빠져나오고, 컴포넌트 정의를 모듈 최상위로 끌어올리는 작은 습관들이 모이면, 그 어느 때보다 안정적인 컴포넌트 트리를 갖게 된다.

그런데 여기서 한 발만 더 나아가보자. 컴포넌트 하나의 정체성과 보존은 정리됐지만, 그 안의 state 업데이트 로직은 여전히 이벤트 핸들러마다 흩어져 있다. 큰 폼을 다루다 보면 `setName`, `setEmail`, `setAddress`, `setIsLoading`, `setErrors`가 여기저기 박혀서, 어디서 무엇이 어떻게 바뀌는지 추적하기가 점점 어려워진다. "이 state가 왜 이 시점에 이렇게 바뀌었지?"라는 의문이 한번 들기 시작하면, 핸들러 사이를 한참 헤매게 된다. 난감한 상황이다.

여러 곳에 흩어진 setState를 한 곳으로 모으고 싶다면, 이제 다음 도구가 필요하다. 다음 장에서는 `useReducer`를 살펴보자. "사용자가 무엇을 했는가"를 액션이라는 명시적 개념으로 표현하고, 모든 state 변경을 단 하나의 순수 함수로 모으는 패턴이다. useState와 useReducer 사이의 경계선이 어디에 있고, 어떤 시점에 reducer로 옮겨야 코드가 단정해지는지 함께 풀어보자.
