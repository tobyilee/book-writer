# 10장. Ref — 렌더와 무관한 값을 보관하기

새 페이지에 진입하자마자 검색창에 커서가 깜빡이고 있는 사이트를 본 적이 있을 것이다. 사용자는 별다른 클릭 없이 바로 타이핑을 시작할 수 있다. 작은 디테일이지만 사용 경험이 꽤 다르다. 비슷한 요구사항을 React로 풀어보려고 마음먹었다고 해보자. "컴포넌트가 마운트되면 첫 번째 입력 필드에 자동으로 포커스를 주자." 한 줄짜리 요구다. 그런데 React로 옮겨 적기 시작하면 의외로 손이 멈춘다.

처음 시도는 보통 이렇게 시작된다.

```tsx
function LoginForm() {
  const [focused, setFocused] = useState(false);

  if (!focused) {
    setFocused(true);
    // 어떻게든 input에 focus를 주자
  }

  return <input type="email" placeholder="이메일" />;
}
```

쓰는 도중에 이미 어색하다. `<input>`을 화면에 그리기도 전에 무엇에 포커스를 주겠다는 건가. 그렇다고 `onChange` 같은 이벤트가 발생하지도 않은 시점에 무엇을 매개로 입력 필드를 잡아야 할지도 막막하다. `document.getElementById`로 잡자니 React 안에서 그렇게 직접 DOM을 뒤지는 게 영 찜찜하다. id를 컴포넌트 이름과 일치시키면 같은 컴포넌트를 두 번 그렸을 때 충돌이 난다는 사실도 곧 떠오른다.

조금 더 욕심을 내서 setState로 풀어보려 시도해보자.

```tsx
function LoginForm() {
  const [inputEl, setInputEl] = useState<HTMLInputElement | null>(null);

  // mount 후에 포커스를 주고 싶다
  if (inputEl) {
    inputEl.focus();
  }

  return (
    <input
      type="email"
      ref={(el) => setInputEl(el)}
    />
  );
}
```

화면에 띄워보면 무한 리렌더에 빠진다. 렌더 중에 `inputEl.focus()`를 호출하는 것까지는 어찌어찌 그럴듯해 보이지만, 사실 더 큰 문제는 `setInputEl`을 ref 콜백 안에서 호출했다는 점이다. DOM이 마운트될 때마다 state가 바뀌고, state가 바뀌면 다시 렌더가 일어나고, 다시 렌더가 일어나면 ref 콜백이 또 불리고… 끝이 없다. 게다가 곰곰이 생각해보면 이 input 요소 자체는 화면에 보여주는 데 필요한 정보가 전혀 아니다. 그저 "잡아두었다가 마운트 직후 focus를 호출하기 위한 손잡이"가 필요할 뿐이다.

여기서 우리가 마주친 진짜 문제는 이거다. **렌더에는 영향을 주지 않으면서, 렌더 사이에 살아남는 값**이 필요하다. state는 렌더에 영향을 주는 값이고, 일반 변수는 렌더 사이에 살아남지 않는다. 그 사이의 어딘가, 정확히 그 자리에 들어가는 도구가 `useRef`다.

이 장에서는 그 어딘가가 어디인지 살펴보자. ref가 정확히 무엇이고, state와는 무엇이 다르며, 언제 꺼내야 하고 언제 꺼내면 안 되는지 정리해보자. ref는 React가 의도적으로 마련해 둔 escape hatch — "비상구"다. 비상구는 평소엔 닫혀 있어야 하지만, 정말 필요한 순간에는 망설임 없이 열 수 있어야 한다. 그 두 감각을 함께 길러보자.

## ref가 뭐길래

`useRef`가 돌려주는 것은 단 하나의 프로퍼티 `current`를 가진 평범한 객체다. 코드로 적으면 거의 우습도록 단순하다.

```tsx
import { useRef } from "react";

function Demo() {
  const countRef = useRef(0);

  // countRef는 { current: 0 } 모양의 객체다
  console.log(countRef.current); // 0

  return <button onClick={() => countRef.current++}>증가</button>;
}
```

이 객체에는 두 가지 약속이 걸려 있다.

첫째, **렌더 사이에 살아남는다.** 컴포넌트가 다시 렌더되어도 같은 객체가 유지된다. `countRef.current`에 적어둔 값은 다음 렌더에서도 그대로 읽을 수 있다. 일반 변수처럼 함수가 끝날 때 사라지지 않는다.

둘째, **`current`를 바꿔도 React에게 알리지 않는다.** state를 바꾸면 React는 "그렇다면 새 화면을 그려야겠군" 하고 리렌더를 예약한다. ref는 그렇지 않다. 값을 바꿔도 화면은 그대로다. React는 ref가 바뀌었다는 사실을 감지조차 하지 않는다.

이 두 가지를 한 줄로 요약하면 이렇다. **ref는 렌더 사이에 살아있지만 렌더에는 영향을 주지 않는 값이다.** 이 정의 한 줄을 머릿속에 새겨두자. ref와 관련된 거의 모든 결정이 이 정의에서 자연스럽게 도출된다.

state와 비교해서 표로 정리해보면 차이가 더 또렷해진다.

| 관점 | state | ref |
| --- | --- | --- |
| 렌더 사이 보존 | O | O |
| 변경 시 리렌더 | O (예약) | X |
| 변경 방식 | setter 호출 (불변) | `current` 직접 대입 (가변) |
| 읽는 시점 | 렌더 어디서나 안전 | 이벤트 핸들러나 effect에서 |
| 주된 용도 | 화면에 보여줄 값 | 화면 뒤에 숨겨둘 값 |

## state인지 ref인지를 가르는 한 줄

매번 헷갈린다면 다음 질문 하나만 자신에게 던져보자.

> 이 값이 **화면에 보여야** 하는가? 그리고 이 값이 바뀌었을 때 **화면이 다시 그려져야** 하는가?

둘 다 "예"라면 state다. 둘 다 "아니오"라면 ref다. 두 답이 갈린다면, 아마 설계가 어딘가 꼬여 있을 가능성이 크니 잠시 멈추고 다시 들여다보는 편이 낫다.

예를 들어보자. 검색창에 사용자가 타이핑하는 글자, 카운터 숫자, 모달의 열림 여부, 폼의 유효성 메시지 — 이런 건 다 화면에 보이고, 바뀌면 화면이 갱신되어야 한다. 모두 state다. 반면 디바운스 타이머 ID, 외부 차트 라이브러리의 인스턴스 핸들, 마지막 스크롤 위치를 캐시해 두고 비교하는 용도의 값, 이전 prop 값 — 이런 건 화면에 직접 그려지지도 않고, 바뀐다고 해서 화면이 새로 그려져야 할 이유도 없다. 모두 ref다.

판단이 모호한 흔한 사례 하나를 짚어보자. "어떤 텍스트를 input에 보여줘야 하지만, **타이핑할 때마다 부모를 리렌더하기는 싫다.** 그러면 ref로 관리하면 되지 않을까?"

여기서 멈춰서 자문해보자. 그 텍스트는 화면에 보이는가? 보인다. 그리고 사용자가 글자를 칠 때마다 화면이 갱신되어야 하는가? 그렇다. 매번 다음 글자가 input에 나타나야 한다. 그렇다면 답은 state다. "리렌더가 싫어서 ref로 둔다"는 발상은 본말이 전도된 것이다. 이 부분은 뒤에서 한 번 더 짚어보겠다.

## DOM 노드를 잡고 싶을 때

가장 흔한 사용 사례부터 보자. 처음 던졌던 자동 포커스 문제를 ref로 풀어보면 이렇게 깔끔해진다.

```tsx
import { useEffect, useRef } from "react";

function LoginForm() {
  // HTMLInputElement이거나 아직 마운트되지 않아 null일 수 있다
  const emailRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    // 마운트 직후, ref.current에는 실제 DOM 노드가 들어있다
    emailRef.current?.focus();
  }, []);

  return (
    <form>
      <input ref={emailRef} type="email" placeholder="이메일" />
      <input type="password" placeholder="비밀번호" />
      <button type="submit">로그인</button>
    </form>
  );
}
```

세 가지가 한꺼번에 일어난다. JSX의 `ref={emailRef}`로 React에게 "이 input의 DOM 노드를 emailRef.current에 꽂아달라"고 부탁한다. React는 마운트 시점에 이 부탁을 들어준다. 그리고 우리는 effect 안에서, 즉 화면이 그려진 다음 시점에서 `emailRef.current.focus()`를 호출한다. 무한 리렌더는 일어나지 않는다. ref를 바꾸지도 않았고, focus 호출이 React를 거치지도 않았다.

타입은 처음에 약간 헷갈릴 수 있다. `useRef<HTMLInputElement | null>(null)`처럼 적는 이유는 단순하다. 첫 렌더에서는 아직 DOM이 만들어지기 전이라 `current`가 `null`이다. 그래서 타입에 `null`을 명시적으로 포함시켜둔다. 사용할 때 `current?.focus()`처럼 옵셔널 체이닝을 쓰는 것도 같은 이유다. 화면에 input을 그리지 않은 시점에 focus를 호출하면 런타임 에러가 나니까, 타입 시스템에 그 사실을 미리 알려두는 편이 안전하다.

DOM ref가 빛을 발하는 자리는 비슷한 패턴이 반복된다. **focus, scroll, measure**. 이 세 단어를 외워두자.

- focus — 원하는 입력에 커서를 둔다.
- scroll — 특정 요소를 화면에 보이게 끌어당긴다.
- measure — 요소의 실제 크기·위치를 잰다.

세 가지 모두 React의 선언적 데이터 흐름으로는 직접 표현하기 까다롭다. focus는 어떤 prop을 통해 "지금 너에게 포커스를 줘라"라고 말할 수 없고, scroll도 마찬가지다. 측정값은 DOM이 실제로 그려진 뒤에야 알 수 있다. 모두 명령형(imperative) 동작이고, 그래서 ref라는 비상구가 마련된 것이다. 다음은 측정의 예다.

```tsx
import { useEffect, useRef, useState } from "react";

function MeasuredBox() {
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (!boxRef.current) return;
    const rect = boxRef.current.getBoundingClientRect();
    setSize({ width: rect.width, height: rect.height });
  }, []);

  return (
    <div ref={boxRef} style={{ padding: 24, background: "#eef" }}>
      <p>이 박스의 크기를 측정하자.</p>
      <p>
        가로 {size.width.toFixed(0)}px, 세로 {size.height.toFixed(0)}px
      </p>
    </div>
  );
}
```

요소가 그려진 다음에 측정값을 읽고, 그 결과를 화면에 보여주기 위해 state로 옮긴다. ref가 "잡고 측정하는 도구"라면, state는 "그 결과를 화면에 반영하는 통로"다. 두 도구가 한 함수 안에서 자연스럽게 협력하는 모습이다.

## React 19, ref가 그저 prop이 되었다

조금 더 큰 그림으로 넘어가보자. 위 예제처럼 자기 컴포넌트 안의 `<input>`이나 `<div>`에 ref를 붙이는 건 쉽다. 그런데 자식이 커스텀 컴포넌트라면 어떨까? 가령 우리가 만든 `<TextField>` 컴포넌트 안의 진짜 input에 부모가 ref를 꽂고 싶다면?

React 18까지는 이 자리에서 잠깐 숨을 골라야 했다. `forwardRef`라는 별도 헬퍼로 자식을 감싸야만 부모가 보낸 ref가 자식 안의 DOM 노드에 닿을 수 있었다. props에는 자유롭게 값을 전달할 수 있는데 ref만 따로 의식해야 한다는 게, 솔직히 말해 좀 어색했다. "왜 ref만 특별 대우냐"는 질문이 자연스럽게 나왔다.

React 19부터는 그 어색함이 사라졌다. 함수 컴포넌트도 **`ref`를 그냥 prop처럼 받는다.** `forwardRef`로 감쌀 필요가 없다.

```tsx
import { useEffect, useRef } from "react";
import type { ComponentPropsWithoutRef, Ref } from "react";

// React 19 — ref가 다른 prop과 동일하게 들어온다
type TextFieldProps = ComponentPropsWithoutRef<"input"> & {
  ref?: Ref<HTMLInputElement>;
};

function TextField({ ref, ...rest }: TextFieldProps) {
  return <input ref={ref} {...rest} />;
}

function LoginForm() {
  const emailRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  return (
    <form>
      <TextField ref={emailRef} type="email" placeholder="이메일" />
      <TextField type="password" placeholder="비밀번호" />
    </form>
  );
}
```

`TextField`는 `ref`를 받아서 그대로 내부 `<input>`에 전달한다. 그게 전부다. 별도 헬퍼도, 별도 타입 마법도 없다. 부모에서 보면 그냥 자기 컴포넌트의 `<input>`에 ref를 붙이는 것과 거의 똑같이 쓴다. ref가 props 시스템에 비로소 합류한 셈이다.

여기서 한 가지 짚어둘 점. React 18 코드를 React 19로 옮기는 과정에서, 기존의 `forwardRef`를 굳이 다 걷어낼 필요는 없다. 당분간은 두 방식이 함께 동작한다. 다만 새로 작성하는 컴포넌트라면 ref를 그냥 prop으로 받는 편이 깔끔하다. forwardRef는 점차 사라지는 길로 접어들었다고 보자.

## 같은 자리에 여러 개를 꽂아야 한다면 — callback ref

지금까지 본 건 `useRef`로 만든 객체를 `ref={someRef}`처럼 꽂는 방식이었다. ref에는 또 한 가지 모양이 있다. 함수를 직접 넣는 방식, 즉 **callback ref**다.

```tsx
<input ref={(node) => {
  // node가 마운트 직후 들어오고, 언마운트 직전에 null이 들어온다
}} />
```

이 함수는 노드가 DOM에 붙는 순간 그 노드를 인자로 받아 호출되고, 노드가 떨어져 나가는 순간 `null`을 받아 다시 호출된다. mount/unmount 시점을 정확히 잡고 싶을 때 매우 유용하다.

대표적인 쓸모가 동적인 리스트의 ref 모음이다. 항목 개수가 변하는 리스트에서 각 항목의 DOM을 따로 보관하고 싶다고 해보자. `useRef`로 객체 하나를 만들어 두고 그 안에 Map을 넣어 관리하면 깔끔하다.

```tsx
import { useRef } from "react";

type Item = { id: string; label: string };

function ScrollableList({ items }: { items: Item[] }) {
  // id별 DOM 노드를 저장할 Map
  const nodesRef = useRef<Map<string, HTMLLIElement>>(new Map());

  function scrollTo(id: string) {
    nodesRef.current.get(id)?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <div>
      <nav>
        {items.map((item) => (
          <button key={item.id} onClick={() => scrollTo(item.id)}>
            {item.label}로 이동
          </button>
        ))}
      </nav>
      <ul>
        {items.map((item) => (
          <li
            key={item.id}
            ref={(node) => {
              const map = nodesRef.current;
              if (node) {
                map.set(item.id, node);
              } else {
                map.delete(item.id);
              }
              // React 19부터는 위 콜백에서 cleanup 함수를 반환할 수도 있다
            }}
          >
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

리스트가 어떻게 변하든 — 항목이 추가되든 사라지든, 순서가 뒤바뀌든 — 각 항목의 ref 콜백이 정확한 시점에 불려서 Map을 갱신한다. 화면 밖에서 사라진 항목은 자동으로 빠져나가고, 새로 들어온 항목은 새로 등록된다. `useRef` 객체 하나만으로는 이런 동적 등록·해제가 깔끔하지 않은데, callback ref가 그 자리를 자연스럽게 메워준다.

React 19에 와서 callback ref에는 한 가지 작은 보너스가 생겼다. 콜백에서 cleanup 함수를 반환할 수 있다. 즉 `useEffect`처럼 "이 노드가 살아있는 동안만 작동시킬 코드"를 노드별로 묶어두기가 한층 자연스러워졌다. 무한 스크롤 트리거나 외부 위젯 부착 같은 패턴에서 이 점이 빛을 발한다. 연습 문제에서 다시 만나게 될 테니 일단 머리 한쪽에 두자.

## DOM 말고도 ref에 어울리는 것들

지금까지는 DOM 노드를 잡는 ref 이야기만 했다. 그런데 ref의 진짜 영역은 그것보다 훨씬 넓다. **렌더 사이에 살아있어야 하지만 화면에는 보이지 않는 모든 값**이 ref의 자리다. 몇 가지 흔한 사례를 짚어보자.

### 타이머·인터벌 ID — 디바운스 버튼

검색어 입력에 디바운스를 걸어본 사람이라면 한 번쯤 모듈 스코프에 `let timeoutId` 같은 변수를 두는 유혹에 시달려봤을 것이다. 그러나 그 컴포넌트가 화면에 두 개 그려지는 순간, 모듈 스코프 변수는 두 인스턴스가 공유하면서 서로 타이머를 덮어써 버린다. 컴포넌트마다 격리된 저장소가 필요하다. 그게 정확히 ref가 잘하는 일이다.

```tsx
import { useRef } from "react";

function DebouncedButton({
  onClick,
  delay = 300,
}: {
  onClick: () => void;
  delay?: number;
}) {
  // setTimeout 반환 값은 환경에 따라 number(브라우저)거나 NodeJS.Timeout일 수 있다
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  function handleClick() {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }
    timerRef.current = setTimeout(() => {
      onClick();
      timerRef.current = null;
    }, delay);
  }

  return <button onClick={handleClick}>저장</button>;
}
```

`timerRef.current`는 화면에 그려지지 않는다. 사용자가 봐야 할 값도 아니다. 그런데 클릭 사이에 살아있어야 하고, 두 번째 클릭에서는 첫 번째 타이머를 취소해야 한다. ref가 정확히 들어맞는다.

### 이전 값(previous value) 캐시

prop이 바뀐 순간을 감지해서 무엇을 한 번만 해야 한다든가, 두 값을 비교해야 한다면 "직전 값"을 어딘가 보관해야 한다. ref가 좋은 자리다.

```tsx
import { useEffect, useRef } from "react";

function ChatRoom({ roomId }: { roomId: string }) {
  const prevRoomIdRef = useRef<string | null>(null);

  useEffect(() => {
    if (prevRoomIdRef.current !== null && prevRoomIdRef.current !== roomId) {
      console.log(
        `방 변경: ${prevRoomIdRef.current} → ${roomId}`,
      );
    }
    prevRoomIdRef.current = roomId;
  }, [roomId]);

  return <div>현재 방: {roomId}</div>;
}
```

이 코드는 외울 만한 패턴이다. effect 본문에서 이전 값을 비교하고, 마지막에 현재 값을 갱신한다. 직전 값을 화면에 그릴 일은 없으니, state로 둘 이유가 없다.

### 외부 라이브러리 인스턴스 — WebSocket, 차트, 지도

WebSocket 연결, IntersectionObserver, 외부 차트 라이브러리 인스턴스, Mapbox 같은 지도 객체. 이런 것들은 한 컴포넌트 라이프 동안 한 번 만들어두고 유지하는 게 자연스럽다. 매 렌더마다 새로 만들면 끔찍한 일이 벌어진다 — 연결이 끊기고 다시 맺히고, 메모리가 줄줄 새고, 차트가 깜빡인다.

```tsx
import { useEffect, useRef } from "react";

function Chat({ url }: { url: string }) {
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.addEventListener("message", (event) => {
      console.log("메시지 도착", event.data);
    });

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [url]);

  function send(text: string) {
    socketRef.current?.send(text);
  }

  return <button onClick={() => send("안녕")}>인사 보내기</button>;
}
```

`socketRef.current`는 화면에 보이지 않는다. 사용자에게 노출되는 정보는 메시지 목록 같은 별도 state다. 하지만 컴포넌트가 살아있는 동안 같은 소켓을 계속 잡고 있어야 하니, ref가 그 자리를 맡는다. 11장에서 effect의 "외부 시스템 동기화" 관점을 다룰 때 이 패턴을 좀 더 깊이 들여다볼 텐데, 그때 다시 만나게 될 친구다.

## 렌더 중에 ref.current를 건드리지 말자

여기까지 왔으면 ref가 만능 도구처럼 보이기 시작한다. 그런데 정확히 그 시점에 가장 흔한 함정 하나가 도사리고 있다. **렌더 함수 본문에서 ref.current를 읽거나 쓰지 말자.** 이 한 줄은 외워둘 가치가 있다.

왜 그럴까? React에서 렌더 함수는 순수해야 한다. 같은 props·state가 들어오면 같은 결과를 내야 하고, 외부 세계에 흔적을 남기지 않아야 한다. `ref.current`는 외부 세계의 일부다. 게다가 React가 렌더를 두 번 호출할 수도, 중간에 멈출 수도 있다(동시성 모드). 렌더 본문에서 `ref.current = 1`처럼 쓰면, 그 호출이 화면에 반영될지 버려질지 알 수 없다.

또 하나의 이유는 타이밍이다. DOM ref는 마운트가 **끝난** 다음에야 채워진다. 렌더 함수는 마운트가 **일어나기 전에** 실행된다. 그러니 렌더 본문에서 `ref.current.focus()`를 부른다 한들 `current`는 아직 null이다.

쓸 수 있는 자리는 명확하다. **이벤트 핸들러**와 **effect 본문**. 이 두 자리는 React가 렌더를 한 차례 마치고 화면을 그린 뒤의 시점이고, ref가 안전하게 채워진 뒤다.

```tsx
function Counter() {
  const countRef = useRef(0);

  // 안 됨 — 렌더 본문에서 쓰지 말자
  // countRef.current++;

  // 됨 — 이벤트 핸들러 안에서
  function handleClick() {
    countRef.current++;
    console.log(countRef.current);
  }

  // 됨 — effect 본문에서
  useEffect(() => {
    countRef.current = 0;
  }, []);

  return <button onClick={handleClick}>증가</button>;
}
```

렌더 본문에서는 ref를 만들고 받기만 하자. 읽고 쓰는 건 그 다음 시점들의 일이다.

여기에 자매 안티패턴이 하나 더 있다. **React가 관리하는 DOM 자식을 직접 추가하거나 제거하지 말자.** 가령 `containerRef.current.innerHTML = "..."`이나 `containerRef.current.removeChild(...)`로 React가 그려둔 자식을 손대는 식이다. React는 자기가 그린 가상 DOM과 실제 DOM이 일치한다고 가정하고 재조정을 한다. 그 가정이 깨지면 다음 렌더에서 React가 화면을 어떻게 망가뜨릴지 예측할 수 없다. ref로 DOM을 잡는 건 좋지만, **React가 손대지 않는 영역**에 한해서다. 차트 라이브러리에 빈 div를 내어주고 그 안을 라이브러리가 알아서 채우게 하는 건 괜찮다. React의 자식 트리를 ref로 가로채서 직접 헤집는 건 끔찍한 일이다.

## "ref가 useState보다 빠르다"는 흔한 오해

한국어로 useRef를 검색하면 종종 마주치는 비교가 있다. 같은 입력 폼을 useState로 만들면 21번 렌더되는데, useRef로 바꾸면 2번만 렌더되더라 — 이 정량 비교가 캡처 이미지로 자주 돌아다닌다. 이걸 보고 "그래, useRef가 빠르네. 입력 폼은 ref로 짜자"라고 결론을 내리고 싶은 유혹이 든다. 잠깐 멈춰서 그 비교의 전제를 들여다보자.

그 비교는 **정적인 입력 폼**, 그러니까 입력값이 form 제출 시점에만 의미가 있고 타이핑 도중에는 화면에 아무런 변화가 일어날 필요가 없는 폼을 가정한다. 그런 좁은 시나리오에서라면 ref가 21번의 렌더를 2번으로 줄이는 게 맞다. 하지만 그 가정이 살짝만 흔들려도 결론은 무너진다.

가령 같은 입력 폼에 다음 요구가 추가됐다고 해보자. "사용자가 글자를 칠 때마다 글자 수 카운터를 표시한다." 또는 "이메일 형식이 어긋나면 즉시 빨간색 안내 메시지를 띄운다." 또는 "타이핑할 때마다 자동완성 제안을 갱신한다."

이 순간 각 키 입력은 화면을 갱신해야 한다. 카운터 숫자, 빨간 안내, 자동완성 박스 — 모두 입력값에 따라 즉시 변해야 한다. 즉 입력값이 화면에 보여야 한다. 그러면 답은 **state다**, 무조건. 이때 useRef로 우회하면 키를 칠 때마다 ref만 갱신될 뿐 화면은 그대로다. 사용자는 자기가 무엇을 친 건지 알 길이 없다.

여기서 얻을 교훈은 단순하다. **"리렌더를 줄이기 위해" useRef를 쓰는 건 목적과 수단이 뒤바뀐 일이다.** ref는 "리렌더가 필요 없는 값"을 두는 자리지, "리렌더를 회피하기 위한 트릭"이 아니다. 두 표현은 비슷해 보여도 전혀 다르다. 첫 번째는 "이 값은 화면에 보일 필요가 없으니 ref가 자연스럽다"는 결론이고, 두 번째는 "이 값은 화면에 보여야 하지만 리렌더 비용이 아까우니 ref로 숨기자"는 결론이다. 후자는 거의 항상 잘못된 길이다.

성능이 정말 문제라면 그 자리에서 우리가 할 일은 ref로의 우회가 아니라 다른 도구들이다. 입력 컴포넌트의 분리, `React.memo`로 형제 트리 격리, 상태를 가까운 부모로 끌어내리기(co-location). 이 도구들이 손에 익기 전에 ref부터 꺼내드는 건 코드를 어둡게 만든다. 정량 비교 글을 마주칠 때마다 그 비교의 **전제**가 자기 상황에 맞는지부터 확인해보자.

## 모듈 스코프 변수 vs ref — 컴포넌트마다 격리되는 이유

ref가 흔히 빛을 발하는 자리에서 한 번 더 멈춰서 들여다볼 만한 주제가 있다. 모듈 스코프 변수와 ref의 차이다. 처음 React를 만진 개발자라면 이런 질문을 한 번쯤 해볼 만하다. "디바운스 타이머 ID 하나 보관하려고 굳이 useRef를 써야 하나? 그냥 파일 맨 위에 `let timeoutId: number | null = null` 한 줄 적으면 안 되나?" 답을 길게 풀어보자.

코드로 두 방식을 나란히 놓으면 차이가 단숨에 드러난다.

```tsx
// 방식 1 — 모듈 스코프 변수
let timeoutId: ReturnType<typeof setTimeout> | null = null;

function DebouncedSearch({ onSearch }: { onSearch: (q: string) => void }) {
  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => onSearch(e.target.value), 300);
  }
  return <input onChange={handleChange} />;
}

// 방식 2 — ref
function DebouncedSearchRef({
  onSearch,
}: {
  onSearch: (q: string) => void;
}) {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => onSearch(e.target.value), 300);
  }
  return <input onChange={handleChange} />;
}
```

화면에 같은 컴포넌트를 한 번만 그리는 한, 두 방식은 똑같이 동작한다. 그러나 같은 컴포넌트를 두 개 동시에 화면에 띄우는 순간 1번 방식은 무너진다. 두 인스턴스가 같은 모듈 스코프 변수 `timeoutId`를 공유하기 때문이다. 첫 번째 인스턴스에 글자를 치는 도중 두 번째 인스턴스에 글자를 치면, 두 번째 인스턴스의 `clearTimeout`이 첫 번째 인스턴스의 타이머를 지워버린다. 검색은 한 곳에서만 발화하고 다른 곳에서는 영영 발화하지 않는다. 디버깅 한참 한 다음에야 원인을 찾는, 정말 난감한 자리다.

ref는 그렇지 않다. `useRef`로 만든 객체는 **컴포넌트 인스턴스마다 새로 만들어진다.** 같은 컴포넌트를 100개 그리면 100개의 ref 객체가 따로 살아간다. 한 인스턴스의 타이머가 다른 인스턴스의 타이머를 건드릴 일이 없다. 컴포넌트마다 격리된 저장소가 필요한 자리에서 ref가 자연스럽게 들어맞는 까닭이다.

조금 더 일반화해서 정리해두자. 모듈 스코프에 가도 안전한 값은 두 종류다. 하나는 **상수**(설정값, 정적 데이터, 함수). 다른 하나는 **앱 전체에서 단 하나만 존재해도 되는 인스턴스**(전역 캐시, 싱글턴 클라이언트). 이 두 경우가 아니라면, 즉 컴포넌트마다 따로 살아남아야 하는 가변 값이라면 ref의 자리다. 이 분류만 머릿속에 둬도 "어디에 둘까?" 헤맬 일이 줄어든다.

## flushSync — ref 갱신을 기다리지 못할 때

DOM ref를 다루다 보면 한 번쯤 만나는 미묘한 자리가 있다. 새 항목을 추가하고, 그 직후 그 항목으로 스크롤하고 싶다. 코드로 적으면 이런 모양이다.

```tsx
import { useRef, useState } from "react";

function TodoList() {
  const [todos, setTodos] = useState<string[]>([]);
  const listRef = useRef<HTMLUListElement | null>(null);

  function add(text: string) {
    setTodos((prev) => [...prev, text]);
    // 새 항목으로 스크롤? — 아직 DOM에 추가되지 않았다
    listRef.current?.lastElementChild?.scrollIntoView();
  }

  return (
    <ul ref={listRef}>
      {todos.map((t, i) => (
        <li key={i}>{t}</li>
      ))}
    </ul>
  );
}
```

처음 보면 잘 동작할 것 같다. 하지만 실제로는 **이전 마지막 항목**으로 스크롤된다. 왜일까? `setTodos`는 비동기 갱신을 예약할 뿐, 그 줄에서 즉시 화면이 다시 그려지지는 않는다. 다음 줄 `listRef.current?.lastElementChild`는 아직 새 항목이 추가되기 전의 DOM을 가리킨다.

이 자리에 들어맞는 도구가 `react-dom`에서 가져오는 `flushSync`다. 이름 그대로, "지금 즉시 DOM까지 반영하라"고 React에게 부탁한다.

```tsx
import { flushSync } from "react-dom";

function add(text: string) {
  flushSync(() => {
    setTodos((prev) => [...prev, text]);
  });
  // 이 시점에는 새 항목이 이미 DOM에 들어가 있다
  listRef.current?.lastElementChild?.scrollIntoView();
}
```

`flushSync`는 흔하게 꺼내는 도구는 아니다. 동시성 모드의 이점을 일부 포기하고 동기 갱신을 강제하는 셈이라, 성능 부담이 따라온다. 그래서 평소엔 쓰지 않는 편이 낫다. 다만 "갱신 직후 DOM의 새 상태를 즉시 측정하거나 스크롤해야 한다"는 좁은 시나리오에선 ref와 짝이 되어 깔끔한 해법을 만들어준다. 머리 한쪽에 두자.

## ref와 useEffect cleanup — WebSocket 사례 다시 들여다보기

앞서 살짝 다룬 WebSocket 예제로 돌아가보자. 거기엔 ref와 effect의 협력 관계가 압축되어 있는데, 한 번 더 천천히 풀어볼 가치가 있다.

```tsx
import { useEffect, useRef, useState } from "react";

function ChatRoom({ url }: { url: string }) {
  const socketRef = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    // url이 바뀔 때마다 새 소켓을 열고, 이전 소켓을 정리한다
    const socket = new WebSocket(url);
    socketRef.current = socket;

    function handleMessage(event: MessageEvent<string>) {
      setMessages((prev) => [...prev, event.data]);
    }

    socket.addEventListener("message", handleMessage);

    return () => {
      socket.removeEventListener("message", handleMessage);
      socket.close();
      // 정리 단계에서 ref도 비워두자
      if (socketRef.current === socket) {
        socketRef.current = null;
      }
    };
  }, [url]);

  function send(text: string) {
    socketRef.current?.send(text);
  }

  return (
    <div>
      <ul>
        {messages.map((m, i) => (
          <li key={i}>{m}</li>
        ))}
      </ul>
      <button onClick={() => send("안녕")}>인사 보내기</button>
    </div>
  );
}
```

여기서 짚어볼 만한 점이 세 가지다.

첫째, **소켓 인스턴스는 화면에 보이는 값이 아니다.** 그래서 state가 아니라 ref에 둔다. 사용자에게 보여줄 메시지 목록은 `messages` state에 따로 두고, 화면을 갱신하는 통로 역할을 한다.

둘째, **소켓의 라이프타임은 effect의 라이프타임과 일치한다.** url이 바뀌면 effect가 다시 실행되고, cleanup이 돌면서 이전 소켓이 닫힌다. ref는 그 사이를 잇는 다리 역할이다. 외부 이벤트 핸들러(`send` 같은)에서 "지금 어떤 소켓을 쓰고 있지?"를 물어볼 때 답해주는 자리다.

셋째, **cleanup에서 `socketRef.current === socket` 체크를 했다.** url이 빠르게 두 번 바뀌면 두 effect의 cleanup이 미묘하게 겹칠 수 있다. 이미 새 소켓이 열려 ref에 들어가 있는데, 옛 cleanup이 그걸 null로 덮어쓰면 곤란하다. 이 한 줄짜리 가드가 그런 사고를 막는다. ref와 비동기 라이프타임이 만나면 종종 이런 디테일이 따라붙는다는 점은 기억해두자.

이 패턴이 손에 익으면 외부 시스템 통합 거의 모두에 그대로 응용된다. IntersectionObserver, ResizeObserver, 차트 라이브러리, 지도 객체, 분석 SDK. 모두 같은 모양이다. effect로 사이클을 관리하고, ref로 인스턴스를 잡아둔다. 11장에서 effect의 동기화 모델을 본격적으로 다룰 때 이 모양이 다시 등장한다.

## ref와 컨트롤드/언컨트롤드 입력

폼 입력을 다루는 두 가지 흐름, **컨트롤드(controlled)** 와 **언컨트롤드(uncontrolled)** 도 ref와 깊은 관련이 있다. 둘을 짧게 정리해보자.

컨트롤드 입력은 우리가 흔히 보는 패턴이다.

```tsx
function ControlledForm() {
  const [name, setName] = useState("");
  return (
    <input value={name} onChange={(e) => setName(e.target.value)} />
  );
}
```

값이 state에 살고, 입력은 그 state를 그대로 비춘다. React가 입력의 진실 출처(single source of truth)다. 글자 수를 옆에 띄우거나, 형식 검증을 즉시 보여주거나, 다른 입력값에 따라 활성화 여부를 바꾸는 등 입력값이 화면 곳곳에 영향을 줄 때 자연스러운 방식이다.

언컨트롤드 입력은 그 반대다. DOM이 자기 값을 가지고 있고, 우리는 필요할 때 ref로 잡아내 읽는다.

```tsx
function UncontrolledForm({ onSubmit }: { onSubmit: (name: string) => void }) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit(inputRef.current?.value ?? "");
  }

  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} defaultValue="" />
      <button type="submit">제출</button>
    </form>
  );
}
```

`value` 대신 `defaultValue`만 주고, ref로 잡아두었다가 제출 시점에 한 번 읽는다. 타이핑 도중에 화면에 영향을 주지 않으니 리렌더도 없다. 앞서 본 21회 → 2회 비교가 정확히 이 시나리오를 가리켰다.

둘 중 어느 쪽이 정답일까? **거의 항상 컨트롤드 쪽이 정답이다.** 화면이 입력값에 반응할 일이 조금이라도 생긴다면 — 그리고 실무에서는 그런 요구가 거의 반드시 뒤따라 붙는다 — 컨트롤드여야 한다. 언컨트롤드는 좁은 자리, 즉 "정말로 제출 시점에만 값이 필요한 단순한 폼"이거나 "거대한 폼 라이브러리 내부에서 성능을 위해 의도적으로 끊어두는 경우"에 한정해 쓰는 편이 낫다. 평소엔 컨트롤드를 기본기로 두고, 언컨트롤드는 비상구로 남겨두자.

## 흔한 함정 다섯 가지

ref를 쓰다가 자주 만나는 함정을 한자리에 모아두자. 책상 옆에 적어둘 만한 목록이다.

**함정 1. 렌더 본문에서 ref.current를 만진다.** 앞서 길게 다룬 그 함정. `if (firstRender.current)` 같은 모양이 의외로 자주 보인다. 의도가 뭐든 간에, 렌더는 순수해야 한다. 이런 흐름은 effect로 옮기자.

**함정 2. ref가 아직 채워지기 전에 읽는다.** 첫 렌더에서 `ref.current`는 null이다. 그래서 `useRef<HTMLInputElement | null>(null)`처럼 null을 타입에 포함하고, 사용 시 옵셔널 체이닝을 쓰자. 혹은 effect 안에서만 만지자.

**함정 3. ref 변경을 useEffect 의존성에 넣을 수 있다고 착각한다.** 못 한다. ref가 바뀌어도 React는 아무 알림을 받지 않는다. effect가 다시 실행되지도 않는다. ref가 바뀐 시점을 effect로 잡고 싶다면 보통 callback ref가 더 어울린다. "이 노드가 마운트된 순간"을 잡고 싶다면 callback ref 안에서 직접 처리하자.

**함정 4. 같은 자리에 useRef와 useState를 동시에 쓴다.** 가끔 보이는 패턴이다. "state로도 두고, ref로도 둬서 effect 안에서 최신값을 읽자." 진짜로 그게 필요한 자리는 매우 드물다. 대개는 effect의 의존성 배열을 잘못 잡아둔 결과다. 13장에서 다시 만날 주제니, 손이 가려고 할 때 한 번 멈춰보자.

**함정 5. 리렌더가 무서워서 ref로 도망친다.** 앞서 다룬 정량 비교의 함정. "리렌더 줄이려고 useState 대신 useRef"를 쓰는 발상이 든다면 그 자리가 정말 ref의 자리인지부터 다시 확인하자. 화면에 보여야 하는 값이라면 답은 state다. 성능이 정말 문제라면 그건 컴포넌트 분리, 메모이제이션, co-location의 영역이다.

함정들에 이름을 붙여두면 나중에 코드를 읽다가 "어, 이거 함정 3이네"라고 알아챌 수 있다. 그 알아챔이 곧 회피다.

## useImperativeHandle — 살짝 미리보기

지금까지 본 것처럼 ref는 자식의 DOM을 부모가 직접 잡는 도구였다. 그런데 가끔은 자식이 자기 내부의 모든 DOM API를 부모에게 다 노출하고 싶지 않을 때가 있다. 가령 자식 모달 컴포넌트가 부모에게 "open"과 "close" 두 가지만 호출할 수 있게 해주고, 그 외 DOM 조작은 막고 싶다.

이 자리에 어울리는 도구가 `useImperativeHandle`이다. 자식이 자기가 노출하고 싶은 메서드만 골라서 ref에 묶어두는 훅이다. 살짝 맛만 보면 이런 모양이다.

```tsx
import { useImperativeHandle, useRef } from "react";

type ModalHandle = {
  open: () => void;
  close: () => void;
};

function Modal({ ref }: { ref?: React.Ref<ModalHandle> }) {
  const dialogRef = useRef<HTMLDialogElement | null>(null);

  useImperativeHandle(ref, () => ({
    open() {
      dialogRef.current?.showModal();
    },
    close() {
      dialogRef.current?.close();
    },
  }));

  return (
    <dialog ref={dialogRef}>
      <p>안녕</p>
    </dialog>
  );
}

function App() {
  const modalRef = useRef<ModalHandle>(null);

  return (
    <>
      <button onClick={() => modalRef.current?.open()}>열기</button>
      <Modal ref={modalRef} />
    </>
  );
}
```

부모는 `dialog` DOM에 직접 손대지 못한다. 오로지 `open`/`close`만 호출할 수 있다. 자식의 내부 구조가 바뀌어도 부모 코드는 영향을 받지 않는다. 캡슐화가 보존된다.

여기서는 이 정도까지만 살펴보자. `useImperativeHandle`은 사용 빈도가 그리 높지 않고, 잘못 쓰면 명령형 API를 남발하는 길로 이어지기 쉽다. 대부분의 경우 props와 state로 충분하다는 사실을 먼저 체화한 뒤에야 손이 가는 도구다. 자세한 결정 기준과 전체 패턴은 15장에서 본격적으로 다룬다.

## ref를 꺼내기 전에 던질 세 가지 질문

ref는 escape hatch다. 비상구라는 말은, 평소 출입구로 쓰면 안 된다는 뜻이기도 하다. 손이 ref로 향할 때마다 다음 세 질문을 차례로 던져보자.

1. **state로 충분히 풀 수 있는가?** 가장 먼저다. 화면에 보여야 하는 값이라면 state가 정답이다.
2. **prop으로 내려줄 수 있는가?** 자식의 동작을 부모가 결정하고 싶다면, 보통은 prop으로 내려주는 편이 자연스럽다. "지금 열려 있는가"를 prop으로 받아서 자식이 그에 따라 그리도록 하는 식이다. 명령형 호출(`modal.open()`)보다 선언형 prop(`<Modal isOpen />`)이 거의 항상 깔끔하다.
3. **그래도 ref가 필요한가?** focus·scroll·measure처럼 React의 데이터 흐름으로 표현하기 어려운 명령형 동작이거나, 외부 시스템(타이머, 소켓, 차트)을 잡아둘 자리거나, 이전 값을 캐시할 자리라면 그제서야 ref가 답이다.

이 순서대로 자문해보자. 세 번째 질문에서 멈추는 자리만이 ref의 본거지다.

## 핵심 정리

- `useRef`는 `{ current: ... }` 모양의 객체를 돌려준다. **렌더 사이에 살아있지만 렌더에는 영향을 주지 않는 값**이 들어갈 자리다.
- state인지 ref인지는 한 줄로 갈린다. **이 값이 화면에 보여야 하는가?** "예"라면 state, "아니오"라면 ref.
- DOM ref는 **focus·scroll·measure**에 빛을 발한다. effect 안에서 `ref.current`를 만진다는 점만 잊지 말자.
- React 19부터는 함수 컴포넌트도 `ref`를 prop처럼 받는다. `forwardRef`는 이제 신규 코드에서 빼도 좋다.
- callback ref는 노드의 mount/unmount 순간을 잡는 도구다. 동적 리스트의 ref 모음에 잘 어울린다.
- 타이머 ID, 이전 값, WebSocket·차트·지도 인스턴스처럼 **컴포넌트마다 격리되어야 하지만 화면에는 보이지 않는 값**도 ref의 자리다.
- 렌더 본문에서 `ref.current`를 읽거나 쓰지 말자. 이벤트 핸들러와 effect 본문이 안전한 자리다.
- React가 관리하는 자식 DOM을 ref로 직접 헤집지 말자. ref가 잡는 영역은 React가 손대지 않는 자리에 한정하자.
- "ref가 useState보다 빠르다"는 비교는 **정적인 폼이라는 좁은 가정** 위의 결론이다. 입력값이 화면에 즉시 반영되어야 하는 순간 그 결론은 무너진다.
- ref로 손이 가기 전에 자문하자. **state로 풀리지 않는가, prop으로 내려가지 않는가, 그래도 ref가 필요한가.**

## 연습 문제

### 1. (기초) 모달 열림 시 첫 input 자동 focus

다음 모달 컴포넌트는 열렸을 때 첫 번째 input에 자동으로 포커스를 주어야 한다. ref와 effect를 활용해 구현해보자.

```tsx
type Props = {
  open: boolean;
  onClose: () => void;
};

function NameModal({ open, onClose }: Props) {
  // TODO: open이 true가 되는 순간, 첫 input에 focus
  if (!open) return null;
  return (
    <div role="dialog">
      <input placeholder="이름" />
      <input placeholder="이메일" />
      <button onClick={onClose}>닫기</button>
    </div>
  );
}
```

**힌트.** `useRef<HTMLInputElement | null>(null)`로 첫 input에 ref를 붙이고, `useEffect`에서 `open`이 true가 될 때 `current?.focus()`를 호출하자. 의존성 배열을 어떻게 잡을지 한 번 더 고민해보자.

### 2. (중) 비디오 재생/일시정지를 부모에서 제어 (React 19 ref-as-prop)

`<VideoPlayer src={...} />` 컴포넌트를 만들어서 부모가 ref를 통해 `play()`와 `pause()`를 호출할 수 있도록 하자. forwardRef는 쓰지 않고 React 19의 ref-as-prop 패턴으로 구현하자.

```tsx
type VideoHandle = {
  play: () => void;
  pause: () => void;
};

// TODO: VideoPlayer 컴포넌트 정의
// - props로 src와 ref?: React.Ref<VideoHandle>를 받는다
// - 내부에 <video>와 그 video를 잡는 ref를 둔다
// - useImperativeHandle로 play/pause만 외부에 노출한다

function App() {
  const playerRef = useRef<VideoHandle>(null);
  return (
    <>
      <VideoPlayer src="/sample.mp4" ref={playerRef} />
      <button onClick={() => playerRef.current?.play()}>재생</button>
      <button onClick={() => playerRef.current?.pause()}>정지</button>
    </>
  );
}
```

**생각해볼 거리.** 같은 기능을 prop만으로(`isPlaying` boolean을 내려서) 풀면 어떤 코드가 될까? 두 방식의 장단점을 적어보자. 어느 쪽이 더 React스러운지 자기 답을 가지고 다음 장으로 넘어가자.

### 3. (도전) callback ref로 무한 스크롤 트리거 만들기

리스트의 마지막 요소가 화면에 보이는 순간 다음 페이지를 불러오는 무한 스크롤을 구현하자. 마지막 요소에 callback ref를 달고, 그 안에서 `IntersectionObserver`를 부착하자.

```tsx
type Item = { id: string; title: string };

function InfiniteList({
  items,
  onLoadMore,
}: {
  items: Item[];
  onLoadMore: () => void;
}) {
  // TODO: 마지막 항목에 callback ref를 달고 IntersectionObserver 연결
  return (
    <ul>
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <li
            key={item.id}
            // ref={isLast ? (node) => { ... } : undefined}
          >
            {item.title}
          </li>
        );
      })}
    </ul>
  );
}
```

**힌트.** callback ref 안에서 `node`가 들어오면 새 `IntersectionObserver`를 만들어 `observe`하고, `node`가 `null`이 되면 `disconnect`하자. React 19라면 cleanup 함수를 반환하는 패턴도 시도해볼 만하다. 옵저버 인스턴스 자체를 어디에 보관할지도 고민해보자 — `useRef`에 둘까, callback ref 안에 클로저로 둘까. 답은 한 가지가 아니지만 자기 결정의 이유를 적어두자.

## 다음 장으로 가는 다리

ref로 외부 세계를 한 손에 잡는 법을 익혔다. WebSocket 인스턴스, 차트 핸들, 타이머 ID. 모두 컴포넌트가 살아있는 동안 같은 정체성으로 유지해야 하는 것들이었다. 그런데 이 외부 시스템들과 React 컴포넌트는 서로 다른 라이프사이클을 가진다. 컴포넌트가 다시 그려졌다고 해서 매번 새 소켓을 열 수도 없고, 그렇다고 컴포넌트가 사라졌는데 소켓을 그대로 두면 메모리가 줄줄 샌다. **무엇을, 언제, 어떻게 동기화할 것인가** — 이것이 다음 장의 질문이다.

그리고 이 질문의 답은 우리가 흔히 알고 있던 `useEffect`의 모습과 살짝 다르다. effect는 mount/update/unmount의 라이프사이클이 아니라, **외부 시스템과의 동기화 사이클**이다. 이 작은 관점 전환이 effect를 둘러싼 무한 루프와 의존성 배열의 안개를 한꺼번에 걷어준다. 11장에서 그 안개 속으로 들어가 보자.
