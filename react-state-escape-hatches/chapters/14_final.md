# 14장. 커스텀 훅 — 로직을 공유한다, 상태를 공유하지 않는다

어느 날 코드 리뷰 도중에 익숙한 풍경이 다시 보인다고 해보자. `ChatRoom` 컴포넌트에는 `useEffect` 안에서 `connect`/`disconnect` 페어가 들어 있고, `Notifications` 컴포넌트에도 거의 똑같은 모양의 `useEffect`가 들어 있다. `useEffect` 본체는 아주 미세하게 다르지만, 의존성 배열이 무엇이고 정리 함수가 무엇을 정리해야 하는지에 대한 결정 구조는 사실상 동일하다. 한 화면에서는 `roomId`로 채팅 서버에 접속하고, 다른 화면에서는 같은 라이브러리로 알림 채널에 접속한다. 두 군데 모두 `online` 상태를 추적하기 위해 `addEventListener('online', ...)`, `addEventListener('offline', ...)` 짝을 자기 자신만의 방식으로 다시 짜놓고 있다. 컴포넌트가 늘어날 때마다 같은 모양의 `useEffect`가 또 한 벌씩 복사되어 자란다.

이 광경을 보고 있으면 손이 근질거리지 않는가? 누구라도 추출하고 싶어진다. "이거, 그냥 공통 함수로 빼면 되잖아." 하고 무심코 한 줄을 그어버리고 싶다. 그런데 이 충동이 잘못된 방향으로 흐르면 묘한 지옥이 펼쳐진다. 과하게 일반화된 `useEverything` 훅이 만들어지고, 누군가가 그 훅에 옵션 객체를 더하고, 또 누군가가 그 옵션을 분기하고, 결국 호출하는 쪽도 호출당하는 쪽도 무엇을 동기화하려 했는지 잊어버린다. 추출 자체는 좋은 일이다. 그러나 추출의 목적과 시점, 그리고 추출 후에 바뀌는 의미를 분명히 잡아두지 않으면, 잘 만든 줄 알았던 커스텀 훅이 오히려 코드를 옥죈다. 이 장에서는 그 사이의 좁은 길을 함께 걸어보자.

물론 우리는 이미 9장에서 13장까지 effect를 어떻게 다뤄야 하는지를 배웠다. 정직한 의존성을 적자, effect는 동기화로 읽자, event handler가 할 일을 effect로 떠넘기지 말자. 커스텀 훅은 이 모든 원칙을 한 단계 위에서 다시 짚는 도구다. 컴포넌트가 React의 단위라면, 커스텀 훅은 stateful 로직의 단위다. 잘 만들면 "이 컴포넌트가 무엇을 하는가"를 한눈에 보여주는 인덱스가 되고, 잘못 만들면 "이 훅이 도대체 무엇을 하는지 모르겠다"라는 코드 리뷰 코멘트의 출발점이 된다. 그 차이를 만드는 기준이 무엇인지, 차근차근 살펴보자.

## 커스텀 훅이란 결국 무엇인가

먼저 정의에서 출발하자. 커스텀 훅은 거창한 개념이 아니다. **이름이 `use`로 시작하고, 내부에서 다른 훅을 호출하는 함수.** 그게 전부다. React에는 커스텀 훅을 위한 별도의 API가 없다. `createCustomHook`이나 `defineHook` 같은 함수가 있는 게 아니다. 그냥 평범한 자바스크립트 함수인데, 컴포넌트와 똑같은 규칙을 따른다.

```ts
function useOnlineStatus(): boolean {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}
```

이 함수가 커스텀 훅이라고 부를 수 있는 이유는 두 가지다. 하나, 이름이 `use`로 시작한다. 둘, 안에서 `useState`와 `useEffect`라는 다른 훅을 호출한다. 이 두 조건만 갖추면 React 입장에서는 "이건 훅이구나" 하고 인식한다. 렌더링 중에만 호출돼야 하고, 조건문이나 반복문 안에서 호출하면 안 되며, 호출 순서가 매 렌더마다 같아야 한다. 컴포넌트에 적용되는 모든 규칙이 그대로 적용된다.

여기서 한 가지 자주 혼동되는 지점이 있다. 커스텀 훅을 처음 마주한 사람은 종종 이렇게 묻는다. "그렇다면 이 훅을 두 컴포넌트에서 부르면, 두 컴포넌트가 같은 `isOnline` 상태를 공유하는 건가요?" 답은 분명히 "아니오"다. 같은 훅을 부른다고 해서 상태가 공유되는 건 아니다. **로직을 공유할 뿐, 상태는 공유하지 않는다.** 이 한 문장이 이 장 전체를 관통하는 가장 중요한 명제다.

```tsx
function StatusBar() {
  const isOnline = useOnlineStatus(); // 이 컴포넌트만의 isOnline
  return <h1>{isOnline ? '✅ 온라인' : '❌ 오프라인'}</h1>;
}

function SaveButton() {
  const isOnline = useOnlineStatus(); // 또 다른 컴포넌트만의 isOnline
  return <button disabled={!isOnline}>저장</button>;
}
```

`StatusBar`와 `SaveButton`은 둘 다 `useOnlineStatus()`를 부른다. 그런데 두 컴포넌트는 각자 자신만의 `useState` 인스턴스를 갖는다. 같은 회로의 도면을 받아 두 군데에 회로를 따로 깔아놓은 것이라고 비유해도 좋다. 도면(로직)은 한 장이지만, 회로(상태)는 두 개다. 그래서 한쪽의 `isOnline`이 바뀌어도 다른 쪽이 자동으로 바뀌는 일은 없다. 다만 `online`/`offline` 이벤트는 둘 다 듣고 있으니, 실제로 네트워크 상태가 바뀌는 순간에는 두 인스턴스가 동시에 갱신될 뿐이다.

이 점이 왜 중요한가? 만약 진짜로 상태를 공유하고 싶다면, 그건 커스텀 훅의 일이 아니다. 그건 **컨텍스트**나 **상위 컴포넌트로의 끌어올리기**의 일이다. 7장에서 다뤘던 reducer + context 조합이 그 자리다. 커스텀 훅은 같은 모양의 stateful 로직을 여러 컴포넌트가 각자 따로 쓸 수 있게 해주는 도구일 뿐, 데이터를 공유하는 도구가 아니다. 이 경계를 흐릿하게 두면 나중에 "왜 한쪽 화면에서 값을 바꿨는데 다른 화면이 안 바뀌지?" 같은 미스터리 디버깅에 휘말린다. 잊지 말자. 로직은 공유, 상태는 각자.

## 첫 추출 — 두 컴포넌트의 닮은 effect를 묶어보자

이제 추상적인 정의에서 한 걸음 내려와, 실제로 추출이 어떻게 일어나는지 보자. 도입에서 언급한 `ChatRoom`과 `Notifications`을 예로 들어보자. 처음에는 이렇게 생겼다.

```tsx
function StatusBar() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return <h1>{isOnline ? '✅ 온라인' : '❌ 오프라인'}</h1>;
}

function SaveButton() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  function handleSaveClick() {
    console.log('진행률 저장');
  }

  return (
    <button disabled={!isOnline} onClick={handleSaveClick}>
      {isOnline ? '진행률 저장' : '재연결 중...'}
    </button>
  );
}
```

같은 코드가 두 번 보인다. 그것도 거의 한 글자도 다르지 않게. 이 정도라면 추출의 대상이 아주 분명하다. 두 컴포넌트가 똑같이 다루는 stateful 로직 — `isOnline` 상태와 그 상태를 동기화하는 effect — 을 통째로 들어내면 된다. 그렇게 만들어진 게 앞에서 본 `useOnlineStatus`다.

추출 후의 모습은 이렇게 단정해진다.

```tsx
function StatusBar() {
  const isOnline = useOnlineStatus();
  return <h1>{isOnline ? '✅ 온라인' : '❌ 오프라인'}</h1>;
}

function SaveButton() {
  const isOnline = useOnlineStatus();

  function handleSaveClick() {
    console.log('진행률 저장');
  }

  return (
    <button disabled={!isOnline} onClick={handleSaveClick}>
      {isOnline ? '진행률 저장' : '재연결 중...'}
    </button>
  );
}
```

코드 분량만 줄어든 게 아니다. 의미가 또렷해졌다. 두 컴포넌트는 이제 "온라인 상태에 의존한다"라는 사실을 코드의 표면에서 외친다. 이전에는 "이 컴포넌트는 `navigator.onLine`을 읽고, `online`/`offline` 이벤트를 구독한다"라는 구현 세부가 컴포넌트 본체에 끼어 있었다. 추출 후에는 그 세부가 `useOnlineStatus`라는 이름 뒤로 숨었고, 남은 본문은 "이 컴포넌트가 무엇을 그리는가"에 집중한다.

이게 커스텀 훅이 가져다주는 가장 큰 효용이다. **추상화의 결과로 컴포넌트가 자기 본분에 충실해진다.** 컴포넌트는 "무엇을 그리는가"를 말하고, 커스텀 훅은 "어떤 stateful 로직을 갖는가"를 말한다. 이 둘이 한 함수 안에 뒤엉켜 있을 때보다, 분리되어 이름을 갖게 됐을 때 코드를 읽는 사람이 훨씬 빨리 이해한다.

## 시그니처 설계 — 입력은 props처럼, 반환은 hook처럼

추출 자체는 어렵지 않다. 어려운 건 추출된 훅의 **시그니처**를 설계하는 일이다. 무엇을 인자로 받고, 무엇을 반환할 것인가? 이 질문에 무신경하면, 처음에는 단순했던 훅이 점점 부어 오른다.

기준은 두 가지로 나누어 보자. 하나, 입력은 컴포넌트의 props처럼 다루자. 둘, 반환은 React 내장 훅의 반환처럼 다루자.

**입력은 props처럼.** props는 컴포넌트 외부에서 컴포넌트 내부로 흘러들어가는 정보다. 컴포넌트는 props를 보고 무엇을 그릴지 결정한다. 마찬가지로 커스텀 훅의 인자는 호출하는 쪽이 알고 있는 외부 정보다. 훅은 그 정보를 가지고 자기 안의 stateful 로직을 동작시킨다.

```ts
function useChatRoom(options: { roomId: string; serverUrl: string }): void {
  useEffect(() => {
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [options.roomId, options.serverUrl]);
}
```

`useChatRoom`은 `roomId`와 `serverUrl`을 입력으로 받는다. 이 둘은 외부 세계에서 결정되는 값이다. 훅 안에서는 이 값이 바뀌면 연결을 끊고 다시 맺는다. 13장에서 정직한 의존성을 외쳤던 그 원칙이 여기에서도 똑같이 작동한다. 입력 값이 의존성 배열에 정확히 반영돼야 하고, 그 외에 외부에서 들어오지 않은 값을 의존성에 슬쩍 끼워 넣어서는 안 된다.

**반환은 hook처럼.** React 내장 훅들은 반환 형태에 일관된 미감이 있다. `useState`는 `[state, setState]` 튜플을 돌려준다. `useReducer`도 `[state, dispatch]` 튜플이다. `useRef`는 객체 하나, `useContext`는 값 하나. 각자 다르지만 공통점은, **호출자가 그 값을 가지고 무엇을 할 수 있는지가 분명하다**는 것이다.

커스텀 훅도 마찬가지다. 단일 값이면 그냥 값을 돌려주자. `useOnlineStatus`는 `boolean` 하나면 충분하다. 두세 가지 값이라면 객체로 묶어서 이름을 붙여주는 편이 낫다.

```ts
function useFormInput(initialValue: string): {
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
} {
  const [value, setValue] = useState(initialValue);
  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setValue(event.target.value);
  }
  return { value, onChange: handleChange };
}
```

`useFormInput`은 `value`와 `onChange`를 함께 반환한다. 호출자는 그걸 input 엘리먼트에 그대로 펼쳐 넣으면 된다.

```tsx
function NameForm() {
  const firstName = useFormInput('');
  const lastName = useFormInput('');

  return (
    <>
      <input {...firstName} placeholder="이름" />
      <input {...lastName} placeholder="성" />
      <p>안녕하세요, {firstName.value} {lastName.value}님</p>
    </>
  );
}
```

여기서 미묘한 선택이 하나 등장한다. 객체로 반환할 것인가, 배열 튜플로 반환할 것인가? 내장 훅들은 대부분 튜플을 쓴다. 호출자가 비구조화 분해할 때 자기 마음대로 이름을 붙일 수 있기 때문이다. 같은 훅을 한 컴포넌트에서 여러 번 부를 일이 많을수록 튜플이 유리하다. 반대로 반환 값이 두세 개를 넘어가거나, 호출자가 일부 값만 골라 쓸 가능성이 높다면 객체가 더 명료하다. 객체는 이름을 통해 의도를 드러내고, 비구조화 분해 시 일부만 꺼내 써도 자연스럽다. 정답은 없다. **호출자가 한 번에 여러 인스턴스를 만들 가능성이 높은가**, **반환 값이 본질적으로 짝(pair)을 이루는가** — 이 두 질문에 답해보고 결정하면 된다.

여기서 한 가지 권장 사항을 덧붙이자. 입력에 옵션 객체를 받게 될 때, 그 객체가 **호출자가 매 렌더마다 새로 만들어 넘기는 객체**가 되지 않도록 신경 써야 한다. `useChatRoom({ roomId, serverUrl })` 같은 호출이 있다고 해보자. 호출자가 매번 새 객체 리터럴을 넘기면, 의존성 배열에 `options`를 그대로 넣었을 때 effect가 매 렌더마다 실행된다. 13장의 객체 deps 함정을 그대로 끌고 들어오는 것이다. 그래서 훅 내부에서는 객체를 통째로 의존성에 넣지 말고, 위 예시처럼 `options.roomId`, `options.serverUrl`을 분해해서 넣는 편이 안전하다. 또는 인자를 객체로 받지 않고 `useChatRoom(roomId, serverUrl)`처럼 평면화하는 것도 한 방법이다. 어느 쪽을 택하든, **훅 내부의 의존성은 원시 값으로 분해해서 다루는 편이 낫다**는 원칙은 변하지 않는다.

## `use*` 접두사 — 이름이 의무인 이유

이쯤에서 한 번 짚고 넘어갈 게 있다. 왜 굳이 `use`로 시작해야 하는가? 그냥 `getOnlineStatus`나 `subscribeOnline`이면 안 되는가?

답은 두 가지 층위로 나뉜다. 하나는 React 자체의 규칙이고, 다른 하나는 도구(lint, 빌드 도구)의 규칙이다. 사실 더 강한 건 두 번째다.

React의 Rules of Hooks를 강제하는 ESLint 플러그인 `eslint-plugin-react-hooks`는 함수 이름을 보고 그 함수가 훅인지 아닌지를 판단한다. 정확히는 다음 두 가지 패턴을 훅 호출로 간주한다. 첫째, `useXxx` 형태로 호출되는 함수. 둘째, 대문자로 시작하는 컴포넌트 함수의 본체에서 직접 호출되는 함수. 이 규칙 덕분에 lint는 "당신은 지금 조건문 안에서 훅을 호출했어요"라거나 "이 effect의 의존성 배열에 빠진 값이 있어요" 같은 경고를 정확히 짚어줄 수 있다.

만약 `getOnlineStatus`라고 이름 짓고 그 안에서 `useState`를 부른다고 해보자. lint 입장에서는 그게 일반 함수처럼 보인다. 그래서 그 함수를 조건문 안에서 호출해도 경고를 내지 못한다. 결과적으로 Rules of Hooks가 침묵 속에서 깨지고, 디버깅하기 어려운 상태 깨짐이 발생할 수 있다. 끔찍한 일이다.

반대로, 안에서 어떤 훅도 호출하지 않는 함수에 `use`를 붙이는 것도 똑같이 위험하다.

```ts
// 나쁜 예: 훅을 부르지 않으면서 use 접두사를 쓴다
function useFormatDate(date: Date): string {
  return new Intl.DateTimeFormat('ko-KR').format(date);
}
```

이 함수는 그냥 순수 함수다. 어떤 훅도 부르지 않는다. 그런데 이름이 `useFormatDate`다. lint는 이 함수를 훅으로 간주하고, 호출자가 컴포넌트 본체 바깥에서 부르면 경고를 띄운다. "훅을 컴포넌트나 다른 훅 안에서만 호출해야 합니다"라고. 정작 이 함수는 훅이 아닌데도 말이다. 이 헷갈림은 코드베이스 전체로 번진다. 다른 개발자가 이 함수를 보고 "아, 안에서 뭔가 stateful한 게 일어나겠구나" 하고 잘못 추측하기도 한다. 잊지 말자. **훅을 부르면 `use`, 그렇지 않으면 절대 `use`를 붙이지 않는다.** 이 둘은 서로 양방향의 의무다.

이름 한 줄에 너무 큰 무게를 싣는 것 아닌가 싶을 수도 있다. 하지만 React가 별도의 타입 시스템 없이 함수의 정체를 식별하는 유일한 단서가 이름이다. 그러니 이 약속을 어기는 순간, lint는 무력해지고 동료들의 신뢰도 무너진다. 약속의 무게는 코드를 함께 읽는 사람의 수만큼 커진다.

## 추출하면서 자주 하는 실수들

추출은 쉽다. 잘 추출하기는 어렵다. 신참 시절의 자신이든, 지금의 자신이든, 누구나 한 번쯤 다음과 같은 실수를 저지른다.

**너무 일찍 추출한다.** 한 군데에서밖에 안 쓰는 로직을 미리 훅으로 빼는 경우다. "나중에 또 쓸지도 모르니까"라는 생각에서 출발한다. 그런데 "나중에"는 대개 오지 않는다. 와도 모양이 조금 다른 채로 온다. 그러면 결국 훅을 한 번 더 일반화해야 하고, 일반화는 성급한 추상화의 흔한 결과물이다. 호출처가 하나라면, 그 로직은 컴포넌트 본문에 그대로 두는 게 낫다. **두 번째 호출처가 생겼을 때**, 그때 비로소 추출의 명분이 생긴다. 이 기준은 Robin Wieruch가 자신의 글에서 반복적으로 강조하는 원칙이기도 하다. "Don't extract too early. Wait for the second use case."

**너무 일반화한다.** 한 번 추출한 훅에 자꾸 옵션을 더하는 경우다. `useChatRoom(roomId, serverUrl)`이 처음에는 깔끔했는데, 누군가가 "선택적으로 인증 토큰도 받게 해주세요"를 더하고, 또 누군가가 "재연결 전략을 옵션으로 넘기게 해주세요"를 더한다. 어느 순간 시그니처가 거대해지고, 실제 호출처는 절반 이상의 옵션을 사용하지 않는 채로 기본값에 의존하고 있다. 이때쯤 되면 훅을 보는 사람은 이 훅이 자기 화면에서 무엇을 하는지 한눈에 짚을 수 없다. **옵션이 다섯 개를 넘어가기 시작하면, 두 개의 훅으로 쪼개거나, 호출자가 콜백을 제공하는 방식으로 바꿀 시점이다.**

**훅 안에 훅을 한 겹 더 감싼다.** 이른바 "hooks of hooks". `useFetch`가 있고, `useUserFetch`가 그것을 감싸고, `useCurrentUserFetch`가 또 그것을 감싸는 식이다. 각 층이 하는 일이 명확하면 괜찮다. 그러나 대부분의 경우 중간 층은 단순히 인자를 한두 개 더 채워주는 것 외에는 하는 일이 없다. 이러면 호출 추적이 끔찍하게 어려워진다. 어느 층에서 어떤 의존성이 추가됐는지, 어디에서 메모리가 누수되는지 따라가기 위해 세 단계의 정의로 넘나들어야 한다. **합성은 좋지만, 합성을 위한 합성은 피하자.** 한 층의 훅은 한 층의 의미를 가져야 한다. 의미를 추가하지 않는 래퍼는 그저 호출 비용일 뿐이다.

**라이프사이클 래퍼.** 클래스 컴포넌트 시절을 그리워하는 사람들이 종종 만든다. `useMount`, `useUnmount`, `useUpdate` 같은 이름. 처음에는 친숙해 보인다. "마운트될 때 한 번 실행해주세요"라는 의도를 노골적으로 표현하니까. 그런데 이 이름은 effect의 진짜 의미를 흐린다. effect는 "마운트될 때 실행되는 코드"가 아니라 "외부 시스템과 동기화하는 코드"다. 만약 어떤 effect가 마운트 때만 실행돼야 한다면, 그건 아마도 동기화가 아니라 일회성 초기화일 가능성이 높고, 그렇다면 effect가 아닌 다른 자리에 두어야 할 코드다. `useMount`라는 이름은 이 구분을 가려버린다. 그래서 이런 라이프사이클 래퍼는 만들지 않는 편이 낫다. **effect는 effect로 두고, "왜 이 의존성으로 동기화하는가"를 의존성 배열로 표현하자.** 이름이 그 사유를 어림짐작으로 가리지 않게 하자.

## 추출 전에 시도해 볼 것 — 컴포넌트 합성과 children

커스텀 훅을 만들기 전에 한 번쯤 멈춰서 생각해 볼 것이 있다. **이걸 정말 훅으로 빼야 하는가, 아니면 컴포넌트 합성으로도 풀리는가?**

같은 모양의 코드가 두 군데에 있다고 해서 무조건 훅이 답은 아니다. 어떤 경우에는 그 공통점을 새로운 컴포넌트로 묶는 게 더 깔끔하다.

```tsx
// 추출 후보 1: 커스텀 훅
function useTooltip() {
  const [visible, setVisible] = useState(false);
  return {
    visible,
    onMouseEnter: () => setVisible(true),
    onMouseLeave: () => setVisible(false),
  };
}

// 추출 후보 2: 컴포넌트 합성
function Tooltip({ children, label }: { children: React.ReactNode; label: string }) {
  const [visible, setVisible] = useState(false);
  return (
    <span
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      {visible && <span className="tooltip">{label}</span>}
    </span>
  );
}
```

같은 stateful 로직을 두 가지 방법으로 풀 수 있다. 어느 쪽이 더 나은가? 답은 "어떤 모양의 재사용이 일어날 것인가"에 달려 있다.

만약 호출자가 자기만의 마크업 안에 이 동작을 끼워 넣어야 한다면 — 예를 들어 자기만의 `<button>`이나 `<a>`에 동일한 hover 동작을 붙이고 싶다면 — 커스텀 훅이 어울린다. 호출자가 마크업의 형태를 자유롭게 결정할 수 있어야 하니까. 반대로, 마크업이 거의 항상 동일하다면 — 예를 들어 항상 `<span>` 안에 들어가고 항상 `.tooltip` 클래스가 붙는다면 — 그냥 컴포넌트로 묶는 편이 낫다. 컴포넌트는 마크업의 모양과 동작을 한꺼번에 캡슐화한다.

children을 통한 합성도 강력한 대안이다. 컴포넌트가 자식 노드를 받아서 그 자식들을 자기만의 방식으로 배치하거나 동작시키는 패턴 말이다. 이 패턴은 props drilling을 피하고 컨텍스트와도 잘 어울린다. 커스텀 훅이 stateful 로직의 재사용에 강하다면, children 합성은 마크업과 행동의 재사용에 강하다.

그러니 추출의 충동이 들 때 한 번만 더 자문해보자. "이 공통점은 stateful 로직인가, 마크업인가, 아니면 둘 다인가?" stateful 로직이 본질이라면 훅, 마크업이 본질이라면 컴포넌트, 둘 다라면 둘을 같이 쓰자. 도구가 하나뿐인 사람은 모든 문제를 못으로 본다는 격언이 여기에서도 그대로 통한다.

## Wieruch의 추출 기준 — 두 번 이상, 의도가 또렷할 때

추출 시점을 좀 더 구체적으로 잡아보자. Robin Wieruch는 자신의 글에서 커스텀 훅 추출의 기준을 두 가지로 압축한다. 하나는 사용처의 수, 다른 하나는 의도의 명료함이다.

**사용처가 둘 이상일 때 추출하자.** 이건 일반적인 DRY 원칙의 응용이다. 한 번 쓰는 코드는 그 자리에 두자. 두 번째 사용처가 등장하는 순간 — 그것도 미세하게 다른 모습이 아니라 거의 똑같은 모습으로 등장하는 순간 — 비로소 공통점이 무엇인지가 분명해진다. 한 번만 쓰일 때 추출하면, 그 추출은 공통점이 아니라 가정에 기반한다. 가정은 자주 빗나간다.

**의도가 또렷해질 때 추출하자.** 이건 좀 더 미묘한 기준이다. 같은 코드가 두세 군데에 있어도, 그것이 "왜 같은가"를 한마디로 설명하기 어렵다면 아직 추출하지 말자. "이 두 effect는 둘 다 외부 이벤트를 구독하는데, 한쪽은 정리할 때 cleanup을 하고 다른 쪽은 안 한다" 같은 어정쩡한 공통점은 좋은 훅이 되지 못한다. 좋은 훅은 한 줄로 설명된다. "온라인 상태를 추적하는 훅", "폼 입력 값을 관리하는 훅", "디바운싱된 값을 만드는 훅". 이름과 설명이 맞아 떨어질 때, 그제서야 그 추상화가 자기 자리를 잡았다고 할 수 있다.

이 두 기준을 함께 적용하면, 추출은 자연스럽게 늦춰진다. 코드가 두 번 등장할 때까지 기다리고, 그 둘이 정말로 같은 의도를 표현하는지 확인하고, 그 의도에 한 줄짜리 이름을 붙일 수 있는지 자문한다. 이 절차를 통과한 추출은 거의 실패하지 않는다. 통과하지 못한 추출은 시간이 지나며 군살로 남는다.

## 통합 시나리오 — 정규화된 트리, 커스텀 훅, reducer가 만나는 자리

지금까지 단편적인 예시들을 봤다. 이제 한 호흡 더 길게 가서, 이 책 전반에서 미뤄왔던 주제들이 어떻게 한 자리에서 만나는지 살펴보자. 2장에서 정규화된 트리에 대해 이야기하면서 "댓글의 댓글의 댓글"을 어떻게 평탄한 구조로 풀지 다뤘다. 5장에서 reducer를 보여주면서 "복잡한 상태 전이는 dispatch로 풀자"라고 했고, 7장에서는 reducer + context로 동일한 상태를 여러 컴포넌트가 안전하게 읽고 쓰는 길을 열었다. 이제 이 셋이 한 자리에 모인다.

상황을 가정해보자. 우리는 댓글 트리를 갖고 있다. 댓글에는 답글이 달리고, 답글에도 답글이 달린다. 전통적으로는 트리 구조 그대로 들고 있겠지만, 우리는 정규화된 형태를 택한다.

```ts
type CommentId = string;

interface Comment {
  id: CommentId;
  authorId: string;
  body: string;
  childIds: CommentId[];
}

interface CommentsState {
  byId: Record<CommentId, Comment>;
  rootIds: CommentId[];
}

type CommentsAction =
  | { type: 'add'; parentId: CommentId | null; comment: Comment }
  | { type: 'edit'; id: CommentId; body: string }
  | { type: 'remove'; id: CommentId };

function commentsReducer(state: CommentsState, action: CommentsAction): CommentsState {
  switch (action.type) {
    case 'add': {
      const { parentId, comment } = action;
      const byId = { ...state.byId, [comment.id]: comment };
      if (parentId === null) {
        return { byId, rootIds: [...state.rootIds, comment.id] };
      }
      const parent = state.byId[parentId];
      if (!parent) return state;
      byId[parentId] = { ...parent, childIds: [...parent.childIds, comment.id] };
      return { ...state, byId };
    }
    case 'edit': {
      const target = state.byId[action.id];
      if (!target) return state;
      return {
        ...state,
        byId: { ...state.byId, [action.id]: { ...target, body: action.body } },
      };
    }
    case 'remove': {
      const { [action.id]: _removed, ...rest } = state.byId;
      // 부모의 childIds에서도 제거하고, 루트에서도 제거한다.
      const byId: Record<CommentId, Comment> = {};
      for (const [id, comment] of Object.entries(rest)) {
        byId[id] = {
          ...comment,
          childIds: comment.childIds.filter((cid) => cid !== action.id),
        };
      }
      return {
        byId,
        rootIds: state.rootIds.filter((id) => id !== action.id),
      };
    }
    default:
      return state;
  }
}
```

여기까지는 5장의 reducer 패턴을 그대로 따랐다. 이제 이 reducer를 컴포넌트 트리 어디서나 쓸 수 있게 컨텍스트로 묶는 자리는 7장에서 본 패턴이다. 그런데 한 가지 불편한 게 있다. 컴포넌트가 이 컨텍스트를 쓰려면 매번 `useContext(CommentsStateContext)`와 `useContext(CommentsDispatchContext)` 두 줄을 써야 한다. 그리고 단일 댓글을 읽고 싶을 때도 매번 `state.byId[id]`를 직접 꺼내야 한다. 이런 자잘한 반복이 호출처마다 흩어지면, "이 컴포넌트는 무엇을 하는가"라는 본문에 잡음이 낀다. 이 잡음을 걷어낼 수 있는 자리가 바로 커스텀 훅이다.

```tsx
const CommentsStateContext = createContext<CommentsState | null>(null);
const CommentsDispatchContext = createContext<React.Dispatch<CommentsAction> | null>(null);

export function CommentsProvider({ children, initial }: {
  children: React.ReactNode;
  initial: CommentsState;
}) {
  const [state, dispatch] = useReducer(commentsReducer, initial);
  return (
    <CommentsStateContext.Provider value={state}>
      <CommentsDispatchContext.Provider value={dispatch}>
        {children}
      </CommentsDispatchContext.Provider>
    </CommentsStateContext.Provider>
  );
}

function useCommentsState(): CommentsState {
  const state = useContext(CommentsStateContext);
  if (state === null) {
    throw new Error('useCommentsState는 CommentsProvider 안에서 호출해야 한다');
  }
  return state;
}

function useCommentsDispatch(): React.Dispatch<CommentsAction> {
  const dispatch = useContext(CommentsDispatchContext);
  if (dispatch === null) {
    throw new Error('useCommentsDispatch는 CommentsProvider 안에서 호출해야 한다');
  }
  return dispatch;
}

export function useComment(id: CommentId): Comment | undefined {
  const state = useCommentsState();
  return state.byId[id];
}

export function useCommentChildren(id: CommentId | null): Comment[] {
  const state = useCommentsState();
  const childIds = id === null ? state.rootIds : state.byId[id]?.childIds ?? [];
  return childIds
    .map((cid) => state.byId[cid])
    .filter((c): c is Comment => c !== undefined);
}

export function useCommentsActions() {
  const dispatch = useCommentsDispatch();
  return useMemo(() => ({
    add: (parentId: CommentId | null, comment: Comment) =>
      dispatch({ type: 'add', parentId, comment }),
    edit: (id: CommentId, body: string) =>
      dispatch({ type: 'edit', id, body }),
    remove: (id: CommentId) =>
      dispatch({ type: 'remove', id }),
  }), [dispatch]);
}
```

이렇게 정리하면, 컴포넌트는 "내가 읽고 싶은 부분"과 "내가 호출하고 싶은 액션"만 짚으면 된다.

```tsx
function CommentItem({ id }: { id: CommentId }) {
  const comment = useComment(id);
  const children = useCommentChildren(id);
  const { edit, remove } = useCommentsActions();

  if (!comment) return null;
  return (
    <article>
      <p>{comment.body}</p>
      <button onClick={() => edit(id, prompt('수정', comment.body) ?? comment.body)}>
        수정
      </button>
      <button onClick={() => remove(id)}>삭제</button>
      <div style={{ paddingLeft: 16 }}>
        {children.map((child) => (
          <CommentItem key={child.id} id={child.id} />
        ))}
      </div>
    </article>
  );
}

function CommentList() {
  const roots = useCommentChildren(null);
  return (
    <section>
      {roots.map((c) => <CommentItem key={c.id} id={c.id} />)}
    </section>
  );
}
```

`CommentItem`은 트리 구조를 모른다. 자기 자식이 누구인지를 `useCommentChildren(id)`에 묻고, 자기가 어떤 댓글인지를 `useComment(id)`에 묻는다. 그러면서도 정작 트리는 정규화된 평면 구조로 저장돼 있고, 모든 변경은 reducer 한 곳에서 일관되게 처리된다. 이 조합이 바로 우리가 2장, 5장, 7장에 걸쳐 흘려두었던 갈래들이 만나는 지점이다.

여기서 커스텀 훅이 한 일은 무엇인가? 커스텀 훅은 새로운 기능을 더하지 않았다. 단지 컨텍스트와 reducer로 이미 가능했던 일을, 호출자가 한 줄로 표현할 수 있도록 **얼굴**을 만들어줬을 뿐이다. `useComment(id)`라는 이름은 그 자체로 의도를 말한다. "이 컴포넌트는 id로 식별되는 댓글 하나를 읽고 싶어 한다." `useCommentsActions()`는 또 말한다. "이 컴포넌트는 댓글에 대한 행위를 일으키고 싶어 한다." 이름이 명사이고, 동사이고, 의도다.

## 정직한 의존성, 훅 안에서도 그대로 적용된다

13장에서 강조한 "정직한 의존성"이라는 원칙을 한 번 더 상기하자. effect의 의존성 배열은 거짓말을 하면 안 된다. effect 본문 안에서 읽는 모든 반응성 값은 의존성 배열에 정확히 들어가야 한다. 이 원칙이 커스텀 훅 안으로 들어와도 한 글자도 바뀌지 않는다. 오히려 더 까다롭게 적용된다고 봐도 좋다. 왜냐하면 커스텀 훅은 호출자가 어떤 값을 어떤 형태로 넘겨줄지 모르기 때문이다. 호출자가 매 렌더마다 새 객체 리터럴을 만들어 넘긴다면? 호출자가 인라인 함수를 그대로 옵션에 넣는다면? 훅 안에서 적당히 의존성 배열에 통째로 넣으면, 그 효과는 매 렌더마다 효과가 다시 실행되는 끔찍한 결과로 돌아온다.

상황을 가정해보자. 외부 라이브러리에서 카메라 위젯을 띄우는 코드가 있다고 하자. 한 번 켜면 끄지 말고 유지해야 하고, 줌이나 위치 같은 옵션이 바뀌면 위젯에 그 변경을 반영해야 한다. 처음 손에 잡히는 대로 짜면 보통 이런 모양이 된다.

```tsx
// 위험한 시작
function CameraView({ position, zoom }: { position: { x: number; y: number }; zoom: number }) {
  const options = { position, zoom };
  useEffect(() => {
    const widget = createCameraWidget(options);
    widget.attach();
    return () => widget.detach();
  }, [options]); // 매 렌더마다 새 객체. effect가 매번 다시 실행된다.

  return <div id="camera" />;
}
```

`options`는 컴포넌트 본문에서 매 렌더마다 새 객체로 만들어진다. 의존성 배열에 그대로 넣으면 React는 매 렌더마다 새 객체로 보고 effect를 다시 실행한다. 위젯이 매 렌더마다 attach/detach를 반복한다. 끔찍한 일이다. 13장에서 이 문제를 객체 분해로 풀었다. 같은 해법이 커스텀 훅에서도 그대로 통한다. 다만 훅에 가둬두면 호출자가 이 함정을 의식할 필요조차 없게 만들 수 있다.

```ts
// 훅 안에서 의존성을 정직하게 분해한다
function useCameraWidget(options: { position: { x: number; y: number }; zoom: number }): void {
  const { position, zoom } = options;
  const x = position.x;
  const y = position.y;
  useEffect(() => {
    const widget = createCameraWidget({ position: { x, y }, zoom });
    widget.attach();
    return () => widget.detach();
  }, [x, y, zoom]);
}
```

훅 내부에서 옵션 객체를 원시 값으로 분해하고, 그 원시 값들만 의존성에 넣는다. 호출자는 이제 안심하고 객체 리터럴을 넘겨도 된다. 호출자의 무지를 훅이 감싸 안는 셈이다. 이런 게 좋은 추상화다. 호출자가 빠지기 쉬운 함정을 훅이 한 번에 차단해 준다. 그래서 호출처는 다시 평온해진다.

```tsx
function CameraView({ position, zoom }: { position: { x: number; y: number }; zoom: number }) {
  useCameraWidget({ position, zoom });
  return <div id="camera" />;
}
```

이 패턴이 보여주는 또 다른 미덕은, **외부 시스템과의 동기화 정책을 훅 한 곳에 모아 둔다**는 점이다. 위젯을 어떻게 만들고, 언제 detach해야 하고, 어떤 값이 바뀔 때 다시 만들어야 하는지를 호출자가 매번 결정하지 않는다. 훅이 한 번 결정해두면 모든 호출처가 같은 정책을 공유한다. 정책의 일관성. 이게 추상화의 또 다른 효용이다.

여기서 한 가지 작은 권고 사항을 더하자. 훅의 인자가 콜백 함수일 때는 13장에서 본 `useEffectEvent`(또는 ref 트릭) 같은 도구를 함께 쓸 일이 많다. 호출자가 매 렌더마다 새 함수를 넘겨도 effect가 다시 실행되지 않게 하려면, 훅 안에서 그 콜백을 ref에 담아두고 본문에서 ref.current를 호출하는 방식이 자주 쓰인다. 자세한 내용은 13장의 정리로 미루자. 다만 잊지 말아야 할 점은, **호출자의 함수가 매 렌더마다 새 참조여도 정상 작동하도록 훅을 설계해 두자**는 것이다. 그러지 않으면 사용자는 매번 `useCallback`으로 콜백을 감싸야 하고, 그 부담이 호출처를 다시 무겁게 만든다. 훅은 호출자에게 짐을 떠넘기지 않을 때 가장 빛난다.

## 자주 쓰는 커스텀 훅 카탈로그

추상적인 이야기를 한참 했으니, 이제 실전에서 손에 익혀두면 좋은 커스텀 훅들을 몇 가지 살펴보자. 이들은 거의 모든 React 프로젝트에서 한 번쯤은 직접 만들거나 라이브러리에서 가져다 쓰는 단골들이다.

### useDebouncedValue

검색창을 만들어 보자. 사용자가 한 글자 입력할 때마다 서버에 요청을 보내면 끔찍한 일이다. 보통은 마지막 입력으로부터 일정 시간이 지난 뒤에야 요청을 보낸다. 이 디바운싱 로직을 매번 컴포넌트 본문에 넣자니 번거롭다. 한 번 훅으로 빼두면 아주 깔끔해진다.

```ts
function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(id);
  }, [value, delayMs]);

  return debounced;
}
```

호출하는 쪽은 짧고 명료하다.

```tsx
function SearchBox() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebouncedValue(query, 300);

  useEffect(() => {
    if (!debouncedQuery) return;
    let cancelled = false;
    fetch(`/api/search?q=${encodeURIComponent(debouncedQuery)}`)
      .then((r) => r.json())
      .then((data) => { if (!cancelled) console.log(data); });
    return () => { cancelled = true; };
  }, [debouncedQuery]);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="검색어"
    />
  );
}
```

`useDebouncedValue`의 시그니처는 매우 단정하다. 입력 값과 지연 시간을 받고, 디바운싱된 값을 돌려준다. 호출자는 이 훅이 `setTimeout`을 다루는지, `useEffect`로 정리하는지를 신경 쓰지 않는다. 그냥 "300ms 늦은 query를 주세요"라고 말하면 된다. 좋은 추상화의 표본이다.

### useLocalStorage

브라우저의 `localStorage`에 값을 저장하면서, 동시에 React 상태처럼 다루고 싶을 때가 있다. 사용자 설정, 마지막으로 본 페이지, 다크 모드 토글 같은 것들. 이걸 매번 손으로 짜면 어김없이 같은 코드가 반복된다.

```ts
function useLocalStorage<T>(
  key: string,
  initialValue: T,
): [T, (value: T | ((prev: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;
    try {
      const raw = window.localStorage.getItem(key);
      return raw !== null ? (JSON.parse(raw) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    setStoredValue((prev) => {
      const next = typeof value === 'function' ? (value as (p: T) => T)(prev) : value;
      try {
        window.localStorage.setItem(key, JSON.stringify(next));
      } catch {
        // 저장 실패는 조용히 무시한다.
      }
      return next;
    });
  }, [key]);

  return [storedValue, setValue];
}
```

여기에는 몇 가지 유의할 점이 숨어 있다. 첫째, SSR을 고려해 `typeof window === 'undefined'` 가드를 둔다. 둘째, 초기 값은 lazy initializer로 한 번만 읽는다. `useState(JSON.parse(...))`로 매번 파싱하는 일은 피하고 싶으니까. 셋째, `setValue`는 `useCallback`으로 묶어서, 호출자가 이 함수를 effect의 의존성으로 사용해도 매 렌더마다 effect가 다시 실행되는 일이 없게 한다. 이런 디테일을 한번 훅에 가둬두면, 호출처에서는 그냥 `useState`처럼 쓰면 된다.

```tsx
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
  return (
    <button onClick={() => setTheme((t) => (t === 'light' ? 'dark' : 'light'))}>
      현재 테마: {theme}
    </button>
  );
}
```

호출자는 `useLocalStorage`가 안에서 무엇을 하는지 모른다. 그냥 `useState`처럼 쓰는데, 새로고침해도 값이 살아 있다. 이게 추상화의 힘이다. 다만 한 가지 솔직한 한계도 짚어 두자. 위 구현은 같은 키를 다른 컴포넌트가 따로 부르면 그 둘 사이에 동기화가 일어나지 않는다. 이건 도입에서 강조한 명제 — "로직은 공유, 상태는 공유 안 함" — 가 그대로 나타나는 사례다. 만약 진짜 동기화가 필요하다면, 그건 또 다른 기법(예: `storage` 이벤트를 듣거나, useSyncExternalStore를 쓰거나)으로 풀어야 한다. 그건 다음 장의 영역이다.

### useFormInput

폼 입력은 프론트엔드에서 끊임없이 반복되는 패턴이다. `value`, `onChange`, 가끔 `onBlur`까지. 이걸 매 input마다 손으로 쓰는 일은 번거롭다.

```ts
function useFormInput(initialValue: string) {
  const [value, setValue] = useState(initialValue);
  const onChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value);
  }, []);
  const reset = useCallback(() => setValue(initialValue), [initialValue]);

  return { value, onChange, reset, setValue };
}
```

호출자는 여러 입력을 자기 마음대로 만들고, 각각의 input에 spread로 풀어 넣는다.

```tsx
function SignupForm() {
  const email = useFormInput('');
  const nickname = useFormInput('');

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    console.log({ email: email.value, nickname: nickname.value });
    email.reset();
    nickname.reset();
  }

  return (
    <form onSubmit={handleSubmit}>
      <input {...email} placeholder="이메일" />
      <input {...nickname} placeholder="닉네임" />
      <button type="submit">가입</button>
    </form>
  );
}
```

여기서 다시 한 번 강조해 두자. `email`과 `nickname`은 같은 훅을 부른 결과지만 **각자의 상태**다. 한쪽 input에 글자를 쳐도 다른 쪽 input은 그대로다. 이게 모든 커스텀 훅이 작동하는 방식이다.

### useChatRoom

도입에서 잠깐 언급했던 채팅방 연결 훅도 카탈로그에 넣어두자. 이건 effect 정리(cleanup)와 의존성 처리의 모범을 보여주는 사례이기도 하다.

```ts
type ChatConnection = {
  connect: () => void;
  disconnect: () => void;
};

declare function createConnection(options: { roomId: string; serverUrl: string }): ChatConnection;

function useChatRoom(options: { roomId: string; serverUrl: string }): void {
  const { roomId, serverUrl } = options;
  useEffect(() => {
    const connection = createConnection({ roomId, serverUrl });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, serverUrl]);
}
```

`useChatRoom`이 보여주는 가장 중요한 디테일은 의존성이다. `options` 객체를 통째로 의존성에 넣지 않고, 안에서 분해해서 `roomId`와 `serverUrl`만 의존성으로 둔다. 13장에서 본 객체 deps의 함정을 정확히 회피하는 방식이다. 호출자는 그냥 `useChatRoom({ roomId, serverUrl: 'https://...' })`로 부르고, 이 훅이 내부적으로 그 값을 분해해 정직한 의존성을 만든다.

호출처는 보면 더 평온하다.

```tsx
function ChatRoom({ roomId }: { roomId: string }) {
  useChatRoom({ roomId, serverUrl: 'https://chat.example.com' });
  return <h1>{roomId} 방에 오신 걸 환영합니다</h1>;
}
```

이 컴포넌트는 더 이상 connect/disconnect를 모른다. 이름만 봐도 무엇을 하는지 알 수 있고, 의존성 처리는 훅에 위임돼 있다. 처음에 보았던 두 컴포넌트의 복붙을 떠올리면, 거리감이 확실히 느껴진다.

### useOnlineStatus

이 절을 마치며 도입에서 시작했던 `useOnlineStatus`를 한 번 더 보자. 카탈로그의 다른 훅들과 같은 형태로 정리할 수 있다.

```ts
function useOnlineStatus(): boolean {
  const [isOnline, setIsOnline] = useState(() =>
    typeof navigator !== 'undefined' ? navigator.onLine : true,
  );

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}
```

다섯 개의 훅을 모아놓고 보면 공통점이 보인다. **시그니처가 짧다. 하는 일이 한 줄로 설명된다. 외부 의존성이 분명하다.** 좋은 커스텀 훅의 미감은 대체로 이런 모양으로 정리된다.

## 합성의 기쁨과 한계

같은 카탈로그의 훅들을 조합해 더 큰 의미를 만들 수 있다. `useDebouncedValue`와 `useLocalStorage`를 합성해서 "디바운싱된 값을 localStorage에 저장하기"를 한 줄로 표현해 볼 수 있다.

```tsx
function PersistedSearch() {
  const [query, setQuery] = useLocalStorage('lastSearch', '');
  const debouncedQuery = useDebouncedValue(query, 300);

  useEffect(() => {
    if (!debouncedQuery) return;
    console.log('검색:', debouncedQuery);
  }, [debouncedQuery]);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="검색"
    />
  );
}
```

훅들이 서로를 모른다는 점에 주목하자. `useDebouncedValue`는 자기가 받는 값이 어디서 오는지 신경 쓰지 않는다. 그냥 값을 받고, 시간이 지난 다음 그 값을 돌려준다. `useLocalStorage`도 마찬가지다. 자기가 돌려주는 값이 어디로 흘러가는지 모른다. 두 훅이 서로 결합하지 않은 채로 한 컴포넌트에서 만나, 호출자가 의미를 만든다. 이게 합성의 묘미다.

물론 합성이 깊어질수록 한계도 드러난다. 한 컴포넌트에서 다섯 개, 열 개의 커스텀 훅을 부르기 시작하면, 각 훅의 의존성과 부수효과가 어떻게 상호작용할지 머릿속에 그리기가 어려워진다. 특히 어떤 훅이 다른 훅의 출력을 입력으로 받는 사슬이 길어지면, 한 번의 렌더에서 어떤 순서로 무엇이 일어나는지 추적하기 위해 신중하게 코드를 따라가야 한다. 이때 도움이 되는 원칙이 있다. **각 커스텀 훅은 자기가 받는 입력에만 의존하고, 자기 외부에 있는 가변 상태에 손을 대지 말자.** 이 원칙을 지키는 동안에는 합성이 안전하다. 깨는 순간, 합성은 연쇄적인 부수효과의 미궁이 된다.

## 커스텀 훅을 만들면 안 되는 경우

마지막으로 솔직한 이야기 하나. 커스텀 훅이 항상 옳은 답은 아니다. 다음과 같은 경우에는 만들지 않는 편이 낫다.

**한 곳에서만 쓰는 일회성 로직.** 이미 강조했듯, 추출은 두 번째 사용처가 등장한 다음에 결정하자. 한 컴포넌트에만 쓰는 effect를 굳이 훅으로 빼면, 호출처는 가벼워지지만 훅의 정의 파일은 무거워진다. 그리고 그 훅은 영영 한 군데에서만 쓰인다. 이건 추상화가 아니라 분산이다. 로직이 컴포넌트와 떨어진 다른 파일에 있어서, 무언가를 이해하기 위해 두 파일을 오가야 한다.

**훅을 부르지 않는 함수.** 안에서 `useState`도 `useEffect`도 다른 어떤 훅도 부르지 않는다면, 그건 그냥 함수다. `formatDate(date)`나 `slugify(title)`나 `clamp(value, min, max)`처럼 평범한 헬퍼 함수로 두자. 앞서 본 것처럼 `use` 접두사는 lint와 다른 사람의 기대를 만든다. 그 기대를 배신하지 말자.

**라이프사이클 래퍼와 일반화 만능 훅.** `useMount`, `useUnmount`, `useEverything({ ...옵션30개 })` 같은 류. 이런 훅은 표면적으로는 친절해 보이지만, 사용처에서 정작 무엇이 일어나는지를 가린다. 그 결과 디버깅 비용이 부풀고, 새 멤버가 코드를 읽을 때 멈춰서 "이 훅이 뭐 하는 훅이지?" 하고 정의로 점프해야 한다. 좋은 훅은 점프할 필요 없이 이름만으로 의도가 통한다.

**상태 공유가 진짜 목적인 경우.** 여러 컴포넌트가 정말로 같은 데이터를 보고 같이 갱신해야 한다면, 그건 컨텍스트의 자리고 reducer의 자리지 커스텀 훅이 단독으로 풀 일이 아니다. 7장의 패턴을 떠올려 보자. 커스텀 훅은 그 위에 얹는 얼굴이지, 그 자리를 대체하는 도구가 아니다.

이런 신중한 절제가 있어야 커스텀 훅이 제 자리를 지킨다. 너무 일찍, 너무 자주 만들면 추상화의 비용만 늘어난다. 적당한 시점에, 분명한 의도로, 짧은 시그니처로 — 이 세 가지를 지키는 동안에는 커스텀 훅이 코드베이스를 가볍게 한다.

## 핵심 정리

이 장에서 다룬 내용을 한 호흡으로 정리해 보자.

1. 커스텀 훅은 이름이 `use`로 시작하고, 안에서 다른 훅을 호출하는 평범한 함수다. 별도의 API가 아니다.
2. 같은 훅을 두 번 호출해도 상태는 따로 갖는다. **로직은 공유, 상태는 공유하지 않는다**가 출발점이다.
3. 두 컴포넌트가 똑같은 stateful 로직을 가질 때 추출하자. 한 곳에서만 쓰는 로직은 컴포넌트 본문에 두는 편이 낫다.
4. 입력은 props처럼, 반환은 hook처럼 설계하자. 단일 값이면 값 하나, 짝을 이루면 튜플, 의미가 강하면 객체를 쓰자.
5. 옵션 객체를 인자로 받을 때는 의존성 배열에 객체를 통째로 넣지 말고, 분해해서 원시 값으로 넣자.
6. `use` 접두사는 의무다. 훅을 부르면 반드시 `use`로 시작하고, 훅을 부르지 않는 함수에는 절대 `use`를 붙이지 말자.
7. 너무 일찍 추출하지 말자. 두 번째 사용처가 생기고, 한 줄로 의도를 설명할 수 있을 때가 적기다.
8. 너무 일반화하지 말자. 옵션이 다섯 개를 넘어가면 두 개의 훅으로 쪼개거나, 콜백 기반으로 바꿀 시점이다.
9. 라이프사이클 래퍼(`useMount`, `useUnmount`)는 만들지 말자. effect의 동기화 의미를 가린다.
10. 추출 전에 컴포넌트 합성과 children으로 풀 수 있는지 한 번 자문해 보자. stateful 로직이 본질이라면 훅, 마크업이 본질이라면 컴포넌트다.
11. 정규화된 상태 + reducer + context의 세 가지를 한 자리에 모을 때, 커스텀 훅은 호출처가 의도를 한 줄로 표현할 수 있게 해주는 얼굴이 된다.
12. 좋은 커스텀 훅은 시그니처가 짧고, 외부 의존성이 분명하며, 이름만 봐도 무엇을 하는지 알 수 있다.

## 연습 문제

### [기초] 두 컴포넌트의 중복 effect를 `useOnlineStatus`로 추출하기

두 컴포넌트에 같은 모양의 `useEffect`가 들어 있다. 이를 `useOnlineStatus` 커스텀 훅으로 추출해 두 컴포넌트의 본문을 가볍게 만들어 보자.

```tsx
// 시작 코드
function StatusBar() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  return <h1>{isOnline ? '✅ 온라인' : '❌ 오프라인'}</h1>;
}

function SaveButton() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  return (
    <button disabled={!isOnline} onClick={() => console.log('저장')}>
      {isOnline ? '저장' : '재연결 중'}
    </button>
  );
}
```

**미션:** `useOnlineStatus(): boolean`을 만들고, 두 컴포넌트에서 그것을 호출해 본문을 두 줄로 줄이자. 두 컴포넌트의 `isOnline`이 서로 독립적인 상태인지도 콘솔로 확인해 보자.

### [중] `useDebouncedValue` 직접 구현 + 검색 컴포넌트에 적용

이번에는 본문에서 본 `useDebouncedValue<T>`를 직접 손으로 만들어 보자. 그리고 검색창에 적용해, 입력 후 300ms가 지나야 가짜 API 요청이 나가도록 하자.

```tsx
// 빈 자리를 채워 보자
function useDebouncedValue<T>(value: T, delayMs: number): T {
  // TODO: useState + useEffect + setTimeout/clearTimeout
}

function SearchBox() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebouncedValue(query, 300);

  useEffect(() => {
    if (!debouncedQuery) return;
    console.log('가짜 API 요청:', debouncedQuery);
  }, [debouncedQuery]);

  return (
    <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="검색어" />
  );
}
```

**미션:** 빠르게 타자를 쳐도 콘솔 출력은 마지막 입력으로부터 300ms 뒤에 한 번만 일어나야 한다. `delayMs`가 바뀔 때도 정상 동작하는지 확인해 보자.

### [도전] 정규화된 댓글 트리 + `useReducer` + 커스텀 훅 통합

본문의 통합 시나리오를 그대로 손으로 다시 만들어 보자.

**미션:**
1. `Comment`, `CommentsState`, `CommentsAction`, `commentsReducer`를 정의한다.
2. `CommentsProvider`로 reducer와 context를 묶는다.
3. `useComment(id)`, `useCommentChildren(id)`, `useCommentsActions()` 세 개의 커스텀 훅을 노출한다.
4. `CommentItem`과 `CommentList`를 만들어, 트리 구조를 정규화된 평면 상태에서 그려낸다.
5. 댓글 추가/수정/삭제 버튼을 붙이고, 한 자리에서 변경이 어떻게 트리 전체에 반영되는지 확인한다.

**확인할 점:** 컴포넌트 어디에서도 `state.byId`를 직접 만지지 않는지, 모든 변경이 `useCommentsActions`를 거치는지, 자식 컴포넌트가 부모의 트리 구조를 모르고도 자기 일을 할 수 있는지를 자문해 보자.

### [도전] 커스텀 훅 안에서 다른 커스텀 훅 호출하기 — 합성의 한계 탐색

이번에는 약간 다른 도전이다. `useDebouncedLocalStorage<T>(key, initial, delayMs)`라는 훅을 만들어, **localStorage에 저장은 디바운싱돼서 일어나되, 화면에 표시되는 값은 즉시 갱신되는** 동작을 구현해 보자.

```tsx
function useDebouncedLocalStorage<T>(
  key: string,
  initial: T,
  delayMs: number,
): [T, (value: T | ((prev: T) => T)) => void] {
  // TODO: useState + useDebouncedValue + useEffect로 localStorage에 저장
}
```

**미션:**
1. 화면에 표시되는 `value`는 사용자가 입력한 직후 즉시 바뀐다.
2. 그러나 `localStorage.setItem` 호출은 마지막 변경으로부터 `delayMs`가 지난 뒤에만 일어난다.
3. 새로고침을 했을 때 마지막에 저장된 값이 살아남는다.

**자문할 점:** 이 훅을 만들면서 `useDebouncedValue`와 `useLocalStorage`를 어떻게 조립했는가? 하나의 훅 안에서 두 훅을 호출하는 게 자연스럽게 느껴졌는가, 아니면 어딘가 어색한 부분이 있었는가? 만약 어색하다면, 그 어색함이 "추상화의 한계"인지 "조합의 잘못된 방향"인지 한 번 더 들여다보자. 본문에서 강조한 "한 층의 훅은 한 층의 의미를 가진다"라는 원칙과 비교해 어떤가?

### [도전] 같은 문제를 (a) 커스텀 훅, (b) children 합성으로 풀어 비교하기

마우스가 올라간 동안에만 자식 노드를 드러내는 `Reveal` 동작을 만들어 보자. 이를 두 가지 방식으로 풀고 비교해 본다.

(a) **커스텀 훅 방식:** `useHover()`를 만들어, `{ hovered, hoverProps }` 형태로 반환한다. 호출자가 자기 마크업에 `hoverProps`를 펼쳐 넣어 사용한다.

(b) **컴포넌트 합성 방식:** `<Reveal>...</Reveal>`이라는 컴포넌트를 만들어, 안의 `children`을 hover 상태에 따라 보여주거나 숨긴다.

**미션:** 두 방식 모두 제대로 동작하도록 만들고, 사용처 코드를 비교해 보자. 어느 쪽이 더 짧은가? 어느 쪽이 더 다양한 상황에 적용 가능한가? 만약 같은 hover 동작을 `<button>`이 아니라 `<a>`나 `<div>`에도 적용하고 싶다면, 두 방식 중 어느 쪽이 더 자연스러운가?

## 한 번 더 짚고 가자 — 커스텀 훅을 보는 세 가지 시선

이 장의 내용을 머리에 담아두기 위해 마지막으로 세 가지 시선을 정리해 두자.

**첫 번째 시선, 의미의 시선.** 커스텀 훅은 "이 컴포넌트가 어떤 stateful 의미를 갖는가"에 이름을 붙이는 도구다. `useOnlineStatus`라고 쓰면 컴포넌트가 온라인 상태에 의존한다고 외친다. `useChatRoom`이라고 쓰면 채팅방 연결의 라이프사이클을 관리한다고 외친다. 이름을 통해 의미가 바깥으로 드러난다. 이 시선이 있으면 추출의 기준은 단순해진다. **새로운 의미를 만들 수 있을 때 추출하자**. 의미가 명확하지 않은 추출은 단지 코드 줄 수만 줄이고, 본문의 명료함은 깎아 먹는다.

**두 번째 시선, 정책의 시선.** 커스텀 훅은 "이 stateful 로직이 어떻게 동작해야 하는가"에 정책을 부여한다. `useChatRoom`은 어떤 값이 바뀔 때 재연결해야 하는지를 결정한다. `useDebouncedValue`는 어떤 시점에 값을 갱신해야 하는지를 결정한다. 이 정책이 한 자리에 모여 있으면, 호출자는 그 정책에 의문을 품지 않고 자기 일에 집중할 수 있다. 만약 정책이 호출처마다 흩어져 있다면, 같은 라이브러리를 쓰는 두 컴포넌트가 미묘하게 다르게 동작한다. 미묘하게 다른 동작은 디버깅을 두 배로 어렵게 만든다. 잊지 말자, 한 곳에 정책을 모아두는 것 자체가 가치다.

**세 번째 시선, 경계의 시선.** 커스텀 훅은 컴포넌트와 외부 시스템 사이의 경계 역할을 한다. 외부에서 오는 신호(이벤트, 타이머, WebSocket, 위젯)를 React의 렌더 모델에 맞춰 정돈해 컴포넌트에게 전달한다. 반대 방향으로는 컴포넌트의 의도를 외부 시스템이 받아들일 형태로 변환한다. 이 경계가 깔끔하게 그어져 있으면, 외부 시스템이 바뀌어도 컴포넌트 본문은 그대로 둘 수 있다. 라이브러리 마이그레이션도 훅 안에서 끝난다. 이 시선이 있으면, 커스텀 훅은 "잘 정돈된 escape hatch"라는 자기 본래의 자리를 찾는다.

이 세 시선을 머릿속에 두면, "커스텀 훅을 만들어야 하나, 말아야 하나"라는 망설임이 줄어든다. 의미를 만들 수 있는가, 정책을 모을 수 있는가, 경계를 그을 수 있는가. 이 셋 중 적어도 둘을 만족할 때, 추출은 거의 실패하지 않는다.

## 마무리 — 다음 장으로의 다리

여기까지 왔으면 우리는 escape hatch라는 단어가 더는 무섭지 않다. 9장부터 13장까지 effect를 다루는 법을 익혔고, 이번 장에서는 그 effect를 포함한 stateful 로직을 어떻게 모아 이름 붙일지 살펴봤다. 커스텀 훅은 escape hatch들을 곱게 갈무리해 컴포넌트 본문에서 떼어내는 칼이다. 그러나 이 칼도 마지막 모서리는 다듬지 못한다. 외부 시스템의 상태를 React의 렌더와 정확히 정합시키는 일, DOM 노드를 직접 명령형으로 다루어야 하는 드문 순간, 동기적 우선순위가 정말로 필요한 한 줌의 케이스 — 이런 자리는 커스텀 훅으로도, 일반 effect로도 잘 풀리지 않는다.

마지막으로, 손에 잘 쥐어지지 않던 escape hatch API들을 정리하자. 다음 장에서는 `useSyncExternalStore`, `useImperativeHandle`, `flushSync` 이 세 카드를 마지막으로 펼쳐 보겠다. 왜 마지막인지, 언제 꺼내는지, 그리고 꺼내고 나서 어떻게 다시 잘 접어 넣을지를 함께 살펴보자.
