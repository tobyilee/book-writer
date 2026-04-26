# 11장. Effect — 동기화의 사이클과 Reactive Value

처음 `useEffect`를 배우던 시절 이야기를 한번 해보자. 적지 않은 사람이 이 훅을 처음 만났을 때 들었던 설명이 비슷하다. "옛날에 클래스 컴포넌트 시절에 `componentDidMount`, `componentDidUpdate`, `componentWillUnmount` 같은 게 있었거든요. `useEffect`는 그 셋을 한 번에 합쳐 놓은 거라고 보시면 됩니다." 그럴듯하게 들렸다. 그리고 한동안은 그 머릿속 그림으로 그럭저럭 코드를 짤 수 있었다. 빈 의존성 배열 `[]`을 넣으면 마운트 한 번만 실행되니까 `componentDidMount`처럼, 의존성 배열에 어떤 값을 넣으면 그게 바뀔 때마다 실행되니까 `componentDidUpdate`처럼, 그리고 cleanup 함수를 반환하면 언마운트 직전에 실행되니까 `componentWillUnmount`처럼.

그런데 이상한 일들이 자꾸 생긴다. 어떤 날은 분명 한 번만 실행되어야 할 것 같은 effect가 두 번 실행된다. 또 어떤 날은 cleanup을 안 적었을 뿐인데 채팅 연결이 늘어지다가 메모리 누수가 의심된다는 동료의 보고를 받는다. 또 어떤 날은 의존성 배열에 분명히 변하지 않는 객체를 넣었는데 effect가 무한히 재실행되며 화면이 깜빡거린다. lint가 빨간 줄을 그어 놓고 "이 변수도 의존성에 넣으세요"라고 다그치는데, 넣자니 무한 루프, 안 넣자니 stale closure. 이쯤 되면 슬슬 난감하다. 그리고 이런 상황이 반복되면, "내가 모르는 뭔가가 있구나" 하는 직감이 든다.

좋은 직감이다. 우리가 모르는 게 있긴 하다. 정확히 말하면 — `useEffect`를 라이프사이클 훅으로 바라보는 그 출발점이 잘못되어 있다. 클래스 시절 `componentDidMount`의 후신이라는 설명은, 처음 입문할 때 "어디서 본 듯한 그림"을 그려주기에 편리하긴 했지만, 그게 바로 통증의 출발점이다. React 공식 문서가 어느 시점부터 이 비유를 거의 쓰지 않게 된 것도 같은 이유에서다. Dan Abramov가 자주 인용하는 한 문장이 이 변화를 압축한다. **"It's all about the destination, not the journey."** 그러니까, Effect는 "언제 일어나는가"의 이야기가 아니라 "지금 어떤 외부 상태와 동기화되어야 하는가"의 이야기다.

이 장에서는 그 관점 전환을 함께 해보자. 라이프사이클이라는 어휘를 머릿속에서 살살 빼내고, 그 자리에 **동기화(synchronization)** 라는 단어를 들여놓는다. 그리고 동기화라는 관점에서 Effect를 다시 보면, cleanup이 왜 의무인지, 빈 배열 `[]`이 무엇을 약속하는 것인지, 개발 모드에서 왜 두 번 실행되는지, 의존성 배열을 어떻게 정직하게 적어야 하는지가 한꺼번에 정리된다. 익숙해지는 데 시간이 좀 걸리겠지만, 한번 이 시야가 트이면 그동안 난감했던 패턴들이 거짓말처럼 단정해진다.

## 라이프사이클이 아니라 동기화다

먼저 한 가지 단순한 질문을 던져보자. 컴포넌트 안에서 외부 시스템에 연결을 맺어야 한다고 해보자. 채팅방에 connect, 브라우저 API에 이벤트 리스너 등록, 외부 라이브러리 위젯 인스턴스 생성, 무엇이든 좋다. 우리가 `useEffect` 안에서 이 일을 한다고 해보자. 그러면 우리는 무엇을 약속하고 있는 걸까?

라이프사이클 관점에서 답하자면 이렇다. "이 컴포넌트가 화면에 등장한 다음에 이 일을 한 번 해 줘. 그리고 화면에서 사라질 때 정리해 줘." 듣기에 자연스러운 답이지만, 살짝 비틀어 다른 답을 시도해보자.

동기화 관점의 답은 이렇다. "이 컴포넌트의 현재 props/state가 가리키는 외부 상태에 맞춰서 외부 시스템을 동기화해 줘. 그 props/state가 바뀌면 다시 동기화해 주고, 컴포넌트가 사라지면 마지막 동기화도 해제해 줘." 풀어 쓰면 길지만, 핵심은 한 줄로 줄어든다.

> Effect는 React 외부의 시스템과 컴포넌트의 reactive 상태를 동기화한다.

이 한 문장을 진지하게 받아들이면, 그동안 머릿속에 있던 "마운트 — 업데이트 — 언마운트"라는 세 점이 사라지고, 대신 "**시작(setup) — 중지(cleanup)**"라는 한 쌍의 사이클이 들어선다. 이 사이클은 컴포넌트의 일생 동안 한 번이 아니라 여러 번 반복된다. setup 한 번에 cleanup 한 번. setup이 또 시작되면 cleanup도 또 끝나야 한다. 이게 동기화의 리듬이다.

이 시야를 잡고 나면, 우리가 자주 쓰는 표현 "마운트될 때 한 번 실행"이라는 말이 사실은 적당히 부정확하다는 걸 알게 된다. 정확히 말하면 그건 "이 effect는 reactive value를 하나도 안 읽으니까, 처음 한 번만 동기화하면 되고 그 뒤로는 다시 동기화할 일이 없다"는 약속이다. 약속이 지켜지면 결과적으로 한 번 실행되는 것처럼 보일 뿐이다. 시야의 미묘한 차이로 보이겠지만, 이 차이가 빈 배열을 적는 손가락의 무게를 바꿔놓는다.

## 채팅 연결로 들어가 보자

추상이 길어지면 머리가 무거워진다. 작은 예제로 내려가 보자. 채팅방에 연결하는 컴포넌트가 있다고 해보자. `roomId`가 props로 들어오고, 그 방에 connect한 뒤에 메시지를 받아 표시한다. 떠날 때는 disconnect한다. 너무나 흔한 그림이다.

```tsx
type ChatRoomProps = { roomId: string };

function ChatRoom({ roomId }: ChatRoomProps) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId]);

  return <h1>{roomId} 방에 오신 걸 환영합니다</h1>;
}
```

여기서 우리가 한 일을 동기화의 어휘로 옮겨 보자. 우리는 React에게 이렇게 말한 것이다. "지금 `roomId`가 'general'이면 'general' 방에 connect되어 있어야 한다. 만약 props가 바뀌어 `roomId`가 'travel'이 되면, 'general'에서 disconnect하고 'travel'에 connect되어 있어야 한다. 컴포넌트가 사라지면 마지막으로 disconnect되어 있어야 한다."

setup은 connect, cleanup은 disconnect다. 이 한 쌍이 `roomId`라는 reactive value를 따라 같이 움직인다. `roomId`가 'general'에서 'travel'로 바뀌면, React는 자동으로 이전 동기화를 cleanup으로 정리한 다음 새 동기화를 setup으로 다시 시작한다. 우리가 명령형으로 "값이 바뀌었으니 재연결해"라고 적은 게 아니다. 그저 "지금 props에 맞는 동기화를 유지해 달라"고 선언했고, React가 그 사이클을 알아서 굴려준다.

cleanup이 왜 의무인지가 여기서 분명해진다. cleanup이 없으면 어떻게 될까? `roomId`가 'general'에서 'travel'로 바뀌었을 때, React는 새 connect를 호출한다. 이전 'general' 연결은? 어디에서도 끊지 않는다. 끊어 줄 사람이 없으니까. 두 개의 연결이 동시에 살아 있게 되고, props가 또 바뀌면 세 개가 된다. 메모리, 소켓, 서버 자원이 슬그머니 새기 시작한다. 이게 잘 보이지 않아서 더 끔찍한 종류의 버그다. 한참 뒤에 운영팀에서 "왜 이 사용자만 동시 접속 수가 자꾸 늘어 있죠?"라는 보고가 올라온 다음에야 알아차리는, 그런 버그.

여기서 한 가지 정리해두자. cleanup은 "언마운트 정리"가 아니라 **"다음 동기화가 시작되기 전의 정리"** 다. 언마운트는 그저 그 cleanup이 마지막으로 한 번 더 호출되는 특수한 경우일 뿐이다. 잊지 말자. cleanup이 setup만큼 무겁다. setup만 적고 cleanup을 비워두는 건, 마치 문을 열기만 하고 닫는 함수를 안 만들어둔 것과 같다. 한 번 정도는 괜찮을지 몰라도, 사이클이 반복되는 순간 — 그러니까 동기화의 리듬이 한 번이라도 다시 돌면 — 그게 바로 누수가 된다.

## Effect의 라이프사이클은 컴포넌트의 라이프사이클이 아니다

이쯤에서 한 번 멈추고 짚어두고 싶은 게 있다. 우리는 자주 "컴포넌트가 마운트될 때, 컴포넌트가 언마운트될 때"라는 말을 쓴다. 그래서 Effect도 컴포넌트의 일생을 따라 시작하고 끝나는 거라고 막연히 생각하기 쉽다. 그런데 위 예제를 보고 나면 그 그림이 흔들린다. 컴포넌트는 한 번 화면에 올라와서 한 번 사라질 뿐이지만, 그 안의 Effect는 그 사이에 여러 번 시작되고 여러 번 중지된다. `roomId`가 다섯 번 바뀌면, 동기화 사이클도 다섯 번 돈다. 그러니까 — **Effect의 라이프사이클은 컴포넌트의 라이프사이클이 아니다.**

이걸 좀 더 또렷하게 보기 위해, 같은 채팅방을 한 단계 키워 보자. 이번에는 `serverUrl`도 props로 받는다.

```tsx
type ChatRoomProps = { roomId: string; serverUrl: string };

function ChatRoom({ roomId, serverUrl }: ChatRoomProps) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId, serverUrl]);

  return <h1>{roomId} 방 ({serverUrl})</h1>;
}
```

이제 동기화가 두 개의 reactive value, 즉 `roomId`와 `serverUrl`에 달려 있다. 둘 중 어느 하나만 바뀌어도 동기화 사이클이 한 번 돈다. cleanup으로 이전 연결을 끊고, setup으로 새 연결을 연다. 컴포넌트는 그 사이 내내 화면에 올라와 있다. 즉, 컴포넌트의 라이프사이클은 한 번이지만 — Effect의 라이프사이클은 그 안에서 여러 번 굴러간다.

이걸 머리로 받아들이는 데 약간의 시간이 든다. 익숙해지기 전까지는 자꾸 "이 컴포넌트가 처음 mount될 때 한 번"이라는 식으로 생각이 미끄러진다. 그래서 다음 한 줄을 명함처럼 들고 다니는 편이 낫다.

> 각 Effect는 자기만의 시작·중지 사이클을 가진다. 그 사이클은 그 Effect가 동기화하는 reactive value들에 의해 정해진다. 컴포넌트의 일생과는 별개다.

이 한 줄을 받아들이면, "왜 이 effect가 또 실행되지?"라고 당황할 일이 줄어든다. 답은 단순하다. effect가 의존하는 reactive value 중 무엇인가가 바뀌었기 때문이다. 동기화 사이클이 한 번 더 돌아야 하니까. 그게 전부다.

## Reactive Value — 무엇이 reactive하고 무엇이 그렇지 않은가

여기서 자연스럽게 다음 질문이 따라온다. **그런데 reactive value가 정확히 뭐지?** 이게 깔끔하게 정리되지 않으면 의존성 배열을 적을 때마다 손이 떨린다. 너무 많이 넣으면 폭주, 적게 넣으면 stale.

정의는 의외로 단순하다.

> 컴포넌트 본체에서 선언되거나, 그 본체로 흘러 들어오는 모든 값은 reactive하다.

좀 더 풀어 쓰면 이렇다. props는 reactive하다. 부모가 다른 값을 내려주면 바뀐다. state도 reactive하다. setState로 바뀐다. props/state로부터 함수 본문에서 계산한 값(`const fullName = first + ' ' + last`)도 reactive하다. 컴포넌트 안에서 `useMemo`로 만든 값도 reactive하다. 결국 컴포넌트가 다시 렌더될 때 다른 값이 될 가능성이 있는 모든 값이 reactive하다.

반대로 non-reactive value는 무엇인가? 컴포넌트 본체 바깥에 있는 값들이다. 모듈 스코프에 선언된 상수(`const API_URL = '...'` 같은 것), 함수 외부에서 import한 값, 그리고 — 약간 결이 다른 친구이지만 — `ref.current`. ref는 reactive value가 아니다. ref가 바뀌어도 컴포넌트는 다시 렌더되지 않으니까. 10장에서 함께 본 그 ref의 비반응성이, 여기서 의존성 배열의 어휘로 다시 등장한다.

이 분류가 왜 중요할까? 의존성 배열의 의미가 이걸로 결정되기 때문이다.

> 의존성 배열은 "이 Effect가 어떤 reactive value들과 동기화되어야 하는가"의 선언이다.

이 문장을 곱씹어보자. 의존성 배열은 lint가 강제로 채워주는 귀찮은 칸이 아니다. 의존성 배열은 우리 코드의 의미적 약속이다. 우리는 그 배열에 적은 값들이 바뀔 때마다 동기화 사이클이 한 번 돌아야 한다고 React에게 약속한 셈이다. 그 약속이 정직하면 React는 그대로 굴려준다. 정직하지 않으면 — stale closure나 누수나 무한 루프 같은 형태로 청구서가 돌아온다.

그래서 의존성 배열을 보는 시야를 이렇게 바꿔두자. **lint가 적어주는 게 아니다. lint는 우리가 해야 할 약속을 옆에서 검증해줄 뿐이다.** Effect가 본문에서 읽고 있는 reactive value의 진짜 목록 — 그게 의존성 배열이어야 한다. 본문에서 `roomId`를 읽으면서 의존성에서는 빼버리는 건, 그 약속을 어기는 행위다. 의존성에 넣지 않으려면, 본문에서 읽지 않는 형태로 코드를 다시 짜야 한다. 둘 중 하나다. 거짓말은 답이 아니다.

### 빈 배열 `[]`이 정말로 의미하는 것

이 시야에서 보면, 그동안 무심코 적던 빈 배열 `[]`이 새로 보인다. 그건 그저 "한 번만 실행"이라는 명령이 아니다. 빈 배열은 우리가 이렇게 약속했다는 뜻이다.

> 이 Effect는 어떤 reactive value도 읽지 않는다. 그래서 컴포넌트가 살아 있는 동안 다시 동기화할 필요가 없다.

이 약속이 지켜지면, 결과적으로 effect가 마운트 시점에 한 번 setup되고 언마운트 시점에 한 번 cleanup된다. 그래서 사람들 머릿속에 "빈 배열은 마운트 한 번"이라는 직관이 자리 잡는 것이다. 결과는 맞다. 하지만 출발점이 다르다. **결과로서 한 번**과 **명령으로서 한 번**은 다른 코드를 쓰게 만든다.

명령으로 본 사람은 빈 배열에 만족하고 거기서 멈춘다. 약속으로 본 사람은 한 번 더 묻는다. "이 effect 본문이 정말로 어떤 reactive value도 안 읽고 있나?" 만약 본문에서 `userId`를 읽고 있는데 의존성은 빈 배열이라면, 약속이 깨진 거다. 이 effect는 처음 받은 `userId`로 영원히 동기화된 채로 살게 된다. props가 바뀌어도 모르는 척한다. stale closure가 거기서 태어난다.

그래서 빈 배열을 적기 전에는 한 번 더 본문을 훑어보는 편이 낫다. "정말로 reactive value를 안 읽고 있는가?" 그 질문에 깔끔하게 그렇다고 답할 수 있을 때만 빈 배열을 안심하고 적자. 그 외의 경우는, 거의 항상, 거짓말이거나 설계가 잘못된 거다.

## 개발 모드에서 두 번 실행된다 — 그 의도와 의미

여기서 많은 사람이 한 번씩 데이는 지점을 짚어보자. 개발 환경, 그러니까 React StrictMode가 켜져 있는 상태에서 Effect는 마운트 시점에 setup → cleanup → setup의 순서로 두 번 호출된다. 처음 이걸 본 개발자는 보통 두 가지 반응 중 하나를 보인다. (1) "버그인가?" 하고 의심하거나, (2) "두 번 실행되니까 한 번만 실행되도록 가드를 넣자"고 생각하거나.

둘 다 잘못된 반응이다. 그런데 이게 왜 잘못된 반응인지를 아는 데에는 우리가 지금까지 정리한 동기화 시야가 결정적인 역할을 한다.

React가 개발 모드에서 effect를 두 번 호출하는 건 버그가 아니라 의도된 검사다. 무엇을 검사하는 걸까? **cleanup이 정말로 setup을 정확히 되돌리는가**, 그래서 setup → cleanup → setup을 했을 때 처음 setup만 한 것과 결과적으로 같아지는가, 이 한 가지를 검사한다. 동기화 사이클이 두 번 돌았을 때도 외부 시스템이 깔끔하게 한 번만 동기화된 것처럼 보여야 — 그게 정상적인 동기화의 정의니까.

채팅 예제로 다시 돌아가 보자. 우리가 connect/disconnect 쌍을 적었다면, StrictMode에서 일어나는 일은 이렇다. connect, disconnect, connect. 결과적으로 connect 한 번 살아 있는 상태. 외부에서 보면 정상이다. 만약 우리가 cleanup을 빼먹었다면? connect, connect. 두 개의 연결이 살아 있는 상태. 즉시 보인다. StrictMode가 우리에게 알람을 울려준 셈이다.

그래서 StrictMode의 더블 인보케이션은 "고쳐야 할 동작"이 아니라 **"우리 코드의 동기화 정직성을 검사하는 도구"** 다. 두 번 실행되는 게 거슬려서 가드를 넣어 한 번만 실행되도록 만드는 건, 체온계가 가리키는 빨간 눈금을 가리려고 체온계 위에 검은 테이프를 붙이는 격이다. 열은 그대로 있다.

그리고 한 가지 덧붙이자. 운영(production) 모드에서는 더블 인보케이션이 없다. 그러니까 StrictMode는 개발 중 cleanup의 부재를 시끄럽게 알려주는 알람이지, 운영 환경의 동작을 바꾸는 장치가 아니다. 알람을 끄지 말고, 알람이 가리키는 곳을 고치자.

## 의존성 배열, 거짓말하지 말자

이 동기화의 시야로 의존성 배열의 흔한 함정을 다시 읽어보면, 대부분의 함정이 거짓말에서 시작된다. 몇 가지 친숙한 패턴을 함께 들여다보자.

### 패턴 A — 의존성 배열에 객체를 넣는다

```tsx
function ChatRoom({ roomId, serverUrl }: { roomId: string; serverUrl: string }) {
  const options = { roomId, serverUrl }; // 매 렌더마다 새 객체

  useEffect(() => {
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [options]); // options는 매 렌더마다 새 참조
  ...
}
```

겉보기에 깔끔해 보인다. 그런데 매 렌더마다 `options`는 새 객체로 다시 만들어진다. 참조 비교 기준으로 보면 매번 "바뀐 값"이다. 그래서 effect는 매 렌더마다 재실행된다. cleanup → setup → cleanup → setup이 끝없이 돈다. 채팅 연결이 매 렌더마다 끊겼다 다시 맺힌다. 끔찍한 일이다.

해결의 방향은 두 가지다. 첫째, 객체 자체를 effect 내부로 옮긴다. 그러면 컴포넌트 본체에서는 더 이상 reactive value `options`가 만들어지지 않는다.

```tsx
useEffect(() => {
  const options = { roomId, serverUrl }; // effect 안에서 만든다
  const connection = createConnection(options);
  connection.connect();
  return () => connection.disconnect();
}, [roomId, serverUrl]);
```

이 형태에서 의존성 배열은 진짜 reactive value인 `roomId`, `serverUrl` 두 원시값으로 정직해진다. 이 둘이 바뀔 때만 동기화 사이클이 돈다. 깔끔하다.

둘째, 객체 비교가 정말 필요하면 `useMemo`로 안정화한다. 다만 이 길은 보통 첫째 길보다 덜 단정하다. effect 안에서 객체를 만드는 게 자연스러우면 그쪽을 선택하는 편이 낫다.

### 패턴 B — 의존성 배열에 함수를 넣는다

객체와 같은 이유로, 컴포넌트 본체에서 만든 함수를 의존성 배열에 넣으면 매 렌더마다 새 참조가 된다. effect가 폭주한다. 해결도 비슷하다. 함수가 effect 외부에서 만들어져야 할 강한 이유가 없다면 effect 내부로 옮긴다. 외부에 두어야 한다면 `useCallback`으로 안정화하되, 그 함수가 의존하는 reactive value들이 결국 effect의 의존성에 따라붙는다는 점을 각오해야 한다. 가장 단정한 길은 — 가능한 한 effect 안에서 정의하는 것이다.

### 패턴 C — 의존성을 빼서 lint를 끈다

```tsx
useEffect(() => {
  // userId를 본문에서 읽음
  fetch(`/users/${userId}`).then(...);
}, []); // eslint-disable-next-line react-hooks/exhaustive-deps
```

이 패턴은 거의 항상 거짓말이다. effect 본문은 `userId`라는 reactive value를 읽고 있는데, 의존성에서는 그 사실을 부정한다. 처음 받은 `userId`로 영원히 굳어진 effect가 된다. 처음에는 잘 굴러가는 것처럼 보이지만, props가 바뀌는 순간 stale 데이터가 화면에 남고 디버깅 지옥이 시작된다.

옳은 길은 두 가지다. (1) 의존성에 정직하게 `userId`를 넣는다. effect가 재실행되는 게 싫다면 cleanup을 정확히 적어 안전하게 사이클이 돌도록 만든다. (2) 그 값이 정말로 동기화의 트리거가 아니라면 — 즉 "값을 알고 싶지만 그 값 때문에 다시 동기화하고 싶진 않다"면 — 다음 절에서 살펴볼 비반응형 영역으로 분리한다. 어느 쪽이든 **lint를 침묵시키는 게 답인 경우는 거의 없다.**

## 비반응형 코드의 분리 — useEffectEvent의 위상

여기까지 따라오면 한 번쯤 이런 상황을 마주친다. effect 안에서 어떤 값을 읽고는 싶은데, 그 값이 바뀐다고 다시 동기화하고 싶진 않은 경우. 가령 채팅방에 connect한 뒤에 보여주는 토스트 메시지의 `theme`. 토스트가 새로 뜰 때 항상 최신 `theme`을 따르고 싶지만, `theme`이 바뀌었다고 채팅 연결을 끊었다 다시 맺을 수는 없다. 불필요한 disconnect/connect만큼 값비싼 일이 없다.

```tsx
function ChatRoom({ roomId, theme }: { roomId: string; theme: string }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on('connected', () => {
      showNotification('Connected!', theme); // 최신 theme이 필요
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, theme]); // theme 때문에 reconnect 발생 — 곤란하다
}
```

`theme`을 의존성에 넣으면 reconnect, 안 넣으면 stale closure로 오래된 `theme`이 토스트에 박힌다. 어느 쪽도 마음에 들지 않는다. 이 난감함을 위해 React는 `useEffectEvent`라는 비반응형 함수 도구를 준비하고 있다. (2026년 시점에는 카나리/실험 기능이라 정식 API가 아닌 점은 기억해두자. 책 시점 이후 정식화될 가능성이 높지만, 도입 전에 한 번 더 공식 문서를 확인하는 편이 낫다.)

```tsx
function ChatRoom({ roomId, theme }: { roomId: string; theme: string }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme); // theme은 항상 최신
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on('connected', () => onConnected());
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // theme은 빠진다
}
```

핵심은 두 가지다. 첫째, `useEffectEvent`로 만든 함수는 **reactive하지 않다.** 본문에서 어떤 props/state를 읽든, 그것은 effect의 의존성으로 따라붙지 않는다. 둘째, 그 안에서 읽는 값은 **항상 최신 값**이다. effect가 캡처해 둔 옛 값이 아니라, 호출되는 그 시점의 props/state를 본다. 그래서 동기화 사이클은 `roomId`만으로 정직하게 돌고, `theme`은 그 위에 비반응적으로 얹힌다.

이 도구의 위상을 한 줄로 정리하면 — Effect가 "지금 어떤 reactive value와 동기화되어야 하는가"를 적는 자리라면, `useEffectEvent`는 "그 동기화 안에서 호출되지만, 동기화의 트리거가 아닌 동작"을 적는 자리다. 사용 규칙도 까다롭다. 다른 컴포넌트로 넘기지 말 것, 의존성 배열에 넣지 말 것, effect 내부에서만 호출할 것. 규칙을 어기면 비반응성이 깨지면서 미묘한 버그가 새어 나온다. 마음에 안 들면 안 쓰면 된다. 다만 우리가 직면한 "reactive와 non-reactive를 한 effect 안에서 같이 다뤄야 한다"는 종류의 문제에 대해서는, 지금까지 어휘 자체가 부족했다는 점만 짚어두자. `useEffectEvent`는 그 어휘를 만들려는 시도다.

비반응형 영역의 다른 식구들도 잠깐 떠올려두자. 모듈 스코프 상수(`const API_URL = ...`)는 자연스럽게 비반응형이다. ref(`ref.current`)도 비반응형이다. 외부 라이브러리 인스턴스, window 객체, document 객체, 모두 React 바깥의 비반응형 시스템이다. effect는 우리가 가진 reactive 세계와 이 비반응형 외부 사이의 다리다. 그 다리가 어느 쪽으로 무엇을 보내는지를 정직하게 적는 것 — 그게 의존성 배열의 본업이다.

## Race condition — 데이터 페칭과 동기화

지금까지 본 채팅 예제는 setup/cleanup이 비교적 명료한 동기화였다. connect/disconnect, addEventListener/removeEventListener, setInterval/clearInterval. 짝이 깔끔하다. 그런데 effect로 자주 다루는 또 하나의 큰 영역이 있다 — 데이터 페칭. 그리고 여기서는 그 짝이 잘 안 보여서 사람들이 자주 데인다.

상황을 그려보자. 검색창이 있다. 사용자가 'react'를 입력하면 `/search?q=react`로 fetch한다. 결과가 오면 화면에 뿌린다. 자연스럽게 effect로 짜게 된다.

```tsx
function SearchResults({ query }: { query: string }) {
  const [results, setResults] = useState<Result[]>([]);

  useEffect(() => {
    fetch(`/search?q=${encodeURIComponent(query)}`)
      .then((r) => r.json())
      .then((data) => setResults(data));
  }, [query]);

  return <ResultList items={results} />;
}
```

겉보기에 단정해 보인다. 그런데 한 가지 시나리오를 그려보자. 사용자가 빠르게 'r', 're', 'rea', 'reac', 'react'를 친다. effect는 매번 트리거된다. 다섯 번의 fetch가 동시에 떠 있다. 그리고 — 네트워크는 마음대로 늦어진다. 'rea'에 대한 응답이 'react'에 대한 응답보다 늦게 도착할 수도 있다. 그렇게 되면, 가장 최근 query는 'react'인데 화면에는 'rea'에 대한 결과가 뿌려진다. 사용자는 잠깐 어리둥절한다. 반복되면 화면이 깜빡거린다. **이게 바로 race condition이다.**

동기화의 시야로 보면 이 문제도 깔끔하게 정리된다. `query`가 'rea'였을 때의 동기화 사이클은, `query`가 'react'로 바뀌는 순간 cleanup으로 끝나야 한다. 그런데 우리가 cleanup을 안 적었다. 그래서 'rea'의 동기화가 멈추지 않고 살아 있다가 뒤늦게 결과를 들고 와서 최신 동기화를 덮어버린 거다. 답은 단순하다 — cleanup을 적자.

가장 흔한 패턴이 `ignore` 플래그다.

```tsx
useEffect(() => {
  let ignore = false;

  fetch(`/search?q=${encodeURIComponent(query)}`)
    .then((r) => r.json())
    .then((data) => {
      if (!ignore) {
        setResults(data);
      }
    });

  return () => {
    ignore = true;
  };
}, [query]);
```

작동 원리를 한 번 따라가 보자. 'rea'의 effect가 시작되면 `ignore = false`인 클로저를 만든다. 그 사이 `query`가 'react'로 바뀐다. React는 이전 effect의 cleanup을 호출한다. 'rea' 클로저의 `ignore`가 `true`가 된다. 'rea'의 응답이 뒤늦게 도착해도 — `if (!ignore)` 체크에서 막힌다. setResults 호출 안 됨. 'react'의 effect가 새로 시작되어, 'react'의 `ignore`는 여전히 `false`. 'react' 응답이 도착하면 정상적으로 set된다. 동기화가 정직해진다.

조금 더 모던한 길은 `AbortController`다. 응답을 무시하는 정도가 아니라 요청 자체를 취소한다.

```tsx
useEffect(() => {
  const controller = new AbortController();

  fetch(`/search?q=${encodeURIComponent(query)}`, { signal: controller.signal })
    .then((r) => r.json())
    .then((data) => setResults(data))
    .catch((err) => {
      if (err.name === 'AbortError') return; // 정상적인 취소
      throw err;
    });

  return () => {
    controller.abort();
  };
}, [query]);
```

`ignore` 플래그가 "응답이 와도 무시한다"라면, `AbortController`는 "요청 자체를 끊는다"이다. 네트워크 자원까지 아낄 수 있다는 점에서 한 발 낫다. 두 패턴을 함께 익혀 두는 편이 낫다. 어느 쪽이든 핵심은 같다 — **fetch가 들어간 effect에는 cleanup이 있어야 한다.** 그리고 그 cleanup의 일은 "이전 동기화의 효과가 새 동기화를 오염시키지 않게 막는 것"이다.

여기에 한 가지 단서를 곁들여 두자. 8장에서 함께 정리한 대로, 실무에서는 데이터 페칭을 effect로 직접 짜는 패턴 자체가 점점 줄어들고 있다. TanStack Query, SWR, RSC + Server Actions 같은 도구가 race condition, 캐싱, retry, dedup을 한꺼번에 해결해준다. 그러니까 위 패턴들은 "effect로 직접 짤 때 정직하게 짜는 법"이지 "이렇게 짜는 게 권장 패턴"이 아니다. 직접 짤 일이 있다면 위 패턴을 정확히 손에 익혀두고, 그게 익숙해지는 만큼 — "이걸 왜 매번 직접 짜고 있지?"라는 질문이 자연스럽게 떠오른다. 그 질문이 떠오르면 도구를 들이는 시점이다.

## "componentDidMount" 흉내내기 — 가장 흔한 안티패턴

이 장의 처음에 잠깐 짚었던 이야기로 돌아오자. `useEffect`를 라이프사이클의 잔재로 바라보면, 가장 자주 등장하는 안티패턴이 하나 있다 — **"이 effect는 마운트될 때 딱 한 번만 실행되도록 해야 해"**라는 강박. 그리고 그 강박이 만들어내는 흔한 코드들이 있다.

### `useRef`로 mount 여부 추적하기

```tsx
function MyComponent() {
  const didInit = useRef(false);

  useEffect(() => {
    if (didInit.current) return;
    didInit.current = true;

    initializeApp(); // 진짜로 한 번만
  }, []);
}
```

저자가 의도한 그림은 이렇다. "StrictMode에서 두 번 실행되는 게 거슬리니까, 처음 한 번만 진짜로 실행되도록 가드를 걸자." 그런데 이 코드가 풀고 있는 진짜 문제가 무엇이냐고 물으면, 답이 미끄러진다. `initializeApp`이 정말로 한 번만 실행되어야 하는 종류의 일이라면 — 이건 effect의 일이 아니다. 모듈 스코프 코드의 일이다.

```tsx
// 모듈 최상단
let initialized = false;
function initOnce() {
  if (initialized) return;
  initialized = true;
  initializeApp();
}

function MyComponent() {
  useEffect(() => {
    initOnce();
  }, []);
}
```

혹은 그냥 모듈 import 시점에 `initializeApp()`을 호출해도 된다. 컴포넌트와 무관한 부수효과를 컴포넌트 안으로 끌어들이지 말자. effect의 의미는 "외부 시스템과 이 컴포넌트의 reactive 상태를 동기화하라"이지, "어딘가에서 한 번만 무엇을 해라"가 아니다. 후자는 effect의 자리가 아니다.

`didInit` 가드는 그래서 일종의 코드 냄새다. 왜 가드를 끼우고 있는지 한 번 자문해보자. 답이 "StrictMode 때문에"라면, 그건 가드를 떼고 cleanup을 정확히 적어 동기화를 정직하게 돌리는 게 옳은 길이다. 답이 "이건 정말 한 번만 일어나야 한다"라면, 그건 effect 바깥의 자리다.

### `useMount` 같은 라이프사이클 래퍼

비슷한 동기로 사람들이 만들곤 하는 게 `useMount(fn)`, `useUnmount(fn)`, `useUpdateEffect(fn, deps)` 같은 커스텀 훅이다. 보기엔 깔끔해 보인다. 클래스 시절의 `componentDidMount`로 돌아간 것처럼 안락하기까지 하다. 그런데 이런 래퍼는 effect의 의미를 흐린다. 우리가 effect를 동기화로 보겠다는 시야 자체를 무너뜨린다.

`useMount`를 부르는 손은 "이 일은 컴포넌트가 처음 화면에 올 때 한 번 일어나면 된다"고 말한다. 그러면 자연히 cleanup도 안 적게 되고, "다시 동기화"라는 어휘 자체가 사라진다. 시간이 지나면 그 effect가 사실은 어떤 reactive value와 연결되어 있어야 한다는 사실이 묻힌다. 그게 묻히는 순간, 우리는 이 장에서 본 라이프사이클의 함정 한가운데로 돌아간다.

그래서 React 공식 문서도 명시적으로 권한다 — `useMount` 같은 래퍼는 만들지 말자. effect를 "이 시점에 일어난다"는 어휘로 다시 줄세우지 말자. 그 시점이 아니라, 그 동기화가 무엇과 연결되어 있는지를 묻자. 답이 "아무 reactive value와도 연결되어 있지 않다"이면 빈 배열로 끝. 답이 "사실 X와 연결되어 있다"이면 X를 의존성에 넣고 cleanup을 적자. 그게 전부다.

## 진짜 어려운 cleanup — 외부 라이브러리와 third-party 위젯

여기까지 정리하고 나면 effect의 풍경이 꽤 단정해 보인다. 그런데 실무에는 단정하지 못한 풍경도 있다. 특히 cleanup이 진짜로 까다로운 경우 — 외부 라이브러리 인스턴스나 third-party 위젯을 다룰 때 — 한 번은 데이게 된다.

예를 들어 어떤 차트 라이브러리가 이런 모양의 API를 가지고 있다고 해보자.

```tsx
const chart = new ChartLib(domNode, options);
chart.render();
// dispose? destroy? 어디 갔지?
```

라이브러리에 따라 어떤 친구는 `chart.destroy()`를 제공하고, 어떤 친구는 `chart.dispose()`라고 부르고, 어떤 친구는 — 제일 끔찍한 건 — 아예 정리 메서드가 없거나, 있어도 내부 이벤트 리스너를 다 떼주지 않는다. cleanup을 진심으로 적고 싶어도 적을 게 없는 상황이 생긴다.

이런 경우의 권장 절차를 정리해두자. 첫째, 라이브러리 문서에서 "destroy/dispose/cleanup" 류의 함수를 가장 먼저 찾는다. 둘째, 그게 없으면 라이브러리가 DOM에 추가했을 법한 노드와 이벤트 리스너를 수동으로 정리할 길을 모색한다. 셋째, 그래도 답이 없으면 — 그 라이브러리 자체를 의심하는 편이 낫다. 정리 API가 없는 라이브러리는 SPA에서 메모리 누수의 잠재 원천이다. 대안을 찾을 가치가 있다.

그리고 한 가지 더, 이런 외부 인스턴스를 effect로 다룰 때는 가능하면 생성과 폐기를 effect 한 쌍 안에 가둔다. 인스턴스를 ref에 보관하고 한쪽 effect에서 만들어 다른 쪽 effect에서 정리하는 식의 흩뿌리는 방식은, 동기화의 의미가 깨진다. 한 쌍의 setup/cleanup 안에 인스턴스의 일생이 들어가도록 묶자.

```tsx
useEffect(() => {
  const chart = new ChartLib(domNode, options);
  chart.render();
  return () => {
    chart.destroy();
  };
}, [domNode, options]); // options는 안정화된 형태여야 한다
```

`options`가 매 렌더마다 새 객체로 만들어지는 패턴 A의 함정이 여기서도 등장한다. 차트가 매 렌더마다 destroy → 재생성된다는 건 시각적으로 끔찍한 깜빡임으로 즉시 보인다. 객체를 effect 안으로 옮기거나, 원시값으로 분해하거나, `useMemo`로 안정화하자. 이런 외부 인스턴스 동기화는 실수의 비용이 크기 때문에, 의존성 배열의 정직성을 평소보다 한 단계 더 깐깐하게 살피는 편이 낫다.

## 이 장의 핵심 정리

머리가 무거워지기 전에 이 장을 한 번에 단단히 묶어두자. 다음 정리들은 이후 12장과 13장에서 끊임없이 다시 호출될 어휘들이다. 한 번에 외울 필요는 없다. 다음 장으로 넘어가기 전에 차분히 한 번씩 짚어보자.

1. **Effect는 라이프사이클이 아니라 동기화다.** "Effect는 React 외부의 시스템과 컴포넌트의 reactive 상태를 동기화한다"라는 한 줄을 명함처럼 들고 다니자. mount/update/unmount의 어휘는 머릿속에서 살살 빼낸다.
2. **Effect의 단위는 setup/cleanup 한 쌍이다.** setup만 있고 cleanup이 없는 effect는, 한 쌍이 깨진 effect다. 거의 항상 누수의 시작이다.
3. **cleanup은 "언마운트 정리"가 아니라 "다음 동기화 시작 전의 정리"다.** 언마운트는 마지막 cleanup이 호출되는 특수한 경우일 뿐이다.
4. **Effect의 라이프사이클은 컴포넌트의 라이프사이클이 아니다.** 컴포넌트는 한 번 마운트되고 한 번 언마운트되지만, 그 사이 effect는 의존성에 따라 여러 번 시작·중지된다. 각 effect는 자기만의 사이클을 가진다.
5. **Reactive value는 컴포넌트 본체에서 선언되거나 흘러 들어오는 모든 값이다.** props, state, 그것들로부터 본문에서 만든 값, `useMemo`로 만든 값 — 전부 reactive다.
6. **Non-reactive value는 컴포넌트 본체 바깥의 값이다.** 모듈 스코프 상수, import한 함수, `ref.current`, 외부 라이브러리 인스턴스 — 이들은 의존성 배열에 들어가지 않는다.
7. **의존성 배열은 "이 effect가 어떤 reactive value와 동기화되는가"의 선언이다.** lint가 채워주는 칸이 아니라 우리가 적는 약속이다.
8. **빈 배열 `[]`은 "이 effect는 어떤 reactive value도 안 읽는다"의 약속이다.** 결과로 한 번 실행되는 것이지, 명령으로 한 번 실행하는 게 아니다.
9. **lint를 침묵시키는 게 답인 경우는 거의 없다.** `eslint-disable`을 쓰기 전에 한 번 더 의심하자. 거의 항상 거짓말이다.
10. **StrictMode의 더블 인보케이션은 cleanup의 정직성을 검사하는 알람이다.** 가드로 두 번 실행을 막지 말고, cleanup이 setup을 정확히 되돌리도록 코드를 정리하자.
11. **의존성 배열에 객체나 함수를 직접 넣지 말자.** 매 렌더마다 새 참조가 되어 effect가 폭주한다. 객체는 effect 안으로 옮기거나 원시값으로 분해하고, 함수도 가능하면 effect 안에서 정의한다.
12. **fetch가 들어간 effect에는 반드시 cleanup이 있어야 한다.** `ignore` 플래그나 `AbortController`로 race condition을 막는다. 그리고 — 가능하면 TanStack Query/SWR/RSC 같은 도구로 옮기자.
13. **`useEffectEvent`는 "동기화 안에서 호출되지만 동기화 트리거가 아닌 동작"의 자리다.** (2026년 시점 카나리/실험.) 다른 컴포넌트로 넘기지 말고, 의존성 배열에 넣지 말고, effect 내부에서만 호출한다.
14. **`useMount`/`useUnmount` 같은 라이프사이클 래퍼는 만들지 말자.** effect의 동기화 의미를 흐린다. "어떤 시점에 일어나는가"가 아니라 "어떤 reactive value와 동기화되는가"를 묻는 어휘를 지키자.
15. **외부 라이브러리 인스턴스의 생성과 폐기는 한 쌍의 effect 안에 가두자.** ref에 보관해 흩뿌리는 패턴은 동기화의 의미를 깨뜨린다. 정리 API가 없는 라이브러리는 의심의 대상이다.

## 연습 문제

다음 네 문제를 손으로 한 번씩 풀어보자. 머리로 푸는 게 아니라, 에디터를 열고 진짜로 코드를 적어보는 게 핵심이다. StrictMode가 켜진 환경(`<StrictMode>` 래핑)에서 동작을 확인하면 더 좋다.

### [기초] 1. 타이머 cleanup 누락 진단 + 수정

다음 코드는 매초 카운트를 1씩 올리는 의도다. StrictMode에서 실행해보면 어떤 일이 벌어지는지 관찰하고, 무엇이 문제인지 동기화의 어휘로 설명한 다음 고쳐보자.

```tsx
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setInterval(() => {
      setCount((c) => c + 1);
    }, 1000);
  }, []);

  return <p>{count}</p>;
}
```

힌트: setup은 무엇이고, cleanup은 무엇이어야 하는가? 쌍이 맞는가? StrictMode에서 setup이 두 번 호출되었을 때 결과적으로 어떤 상태여야 정직한가?

### [중] 2. 채팅방 컴포넌트 — `roomId`와 `serverUrl` 동기화

`roomId`와 `serverUrl`을 props로 받는 `<ChatRoom />`을 작성하자. 둘 중 어느 하나가 바뀌면 이전 연결을 끊고 새 연결을 맺어야 한다. setup/cleanup의 쌍이 정확히 맞아 떨어지는지, StrictMode에서도 한 개의 연결만 살아있는지 콘솔 로그로 확인하자.

```tsx
type ChatRoomProps = { roomId: string; serverUrl: string };

declare function createConnection(serverUrl: string, roomId: string): {
  connect(): void;
  disconnect(): void;
};

function ChatRoom({ roomId, serverUrl }: ChatRoomProps) {
  // 여기를 채워보자
  return <h1>{roomId} at {serverUrl}</h1>;
}
```

추가 도전: 부모 컴포넌트에서 `roomId`만 5초 간격으로 자동으로 바꾸는 흐름을 만들어, 콘솔에서 `connect/disconnect` 쌍이 깔끔하게 매칭되는지 눈으로 확인하자.

### [도전] 3. 검색 디바운스 + race condition 방어

검색창과 결과 리스트를 가진 `<SearchBox />`를 만들자. 사용자가 입력할 때마다 fetch를 보내지 말고, 300ms 디바운스를 거는 동시에 race condition으로 오래된 응답이 최신을 덮지 않도록 `AbortController`로 방어하자. effect 안에서 디바운스와 fetch를 동시에 다루는 깔끔한 cleanup의 구조를 직접 그려보자.

```tsx
type Result = { id: string; title: string };

function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Result[]>([]);

  // 여기를 채워보자.
  // 요구사항:
  // 1. query가 바뀌면 300ms 후 fetch
  // 2. 그 사이 query가 또 바뀌면 이전 타이머와 fetch는 모두 취소
  // 3. AbortController로 네트워크 요청 자체를 끊어준다

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ul>{results.map((r) => <li key={r.id}>{r.title}</li>)}</ul>
    </>
  );
}
```

힌트: 디바운스 타이머의 cleanup은 `clearTimeout`, fetch의 cleanup은 `controller.abort()`. cleanup 함수에서 둘 다 호출하자. setup → cleanup이 쌍으로 정직하게 돌아가는지가 채점 포인트다.

### [도전] 4. StrictMode에서 깨지는 코드를 진짜 동기화로 다시 쓰기

다음 코드는 "한 번만 실행"을 강제하기 위해 ref 가드를 끼웠다. 이 코드가 풀려고 하는 진짜 문제가 무엇인지 진단하고, ref 가드 없이 동기화의 어휘로 다시 써보자. 풀이 과정에서 — 이 일이 정말 effect의 자리인지, 모듈 스코프나 다른 곳의 자리인지도 함께 판단해보자.

```tsx
let analyticsInitialized = false;

function App() {
  const didInit = useRef(false);

  useEffect(() => {
    if (didInit.current) return;
    didInit.current = true;

    if (!analyticsInitialized) {
      analyticsInitialized = true;
      initAnalytics(); // 외부 SDK 초기화
    }

    fetch('/api/me')
      .then((r) => r.json())
      .then((user) => trackUser(user.id));
  }, []);

  return <Routes />;
}
```

힌트: `initAnalytics`는 정말 effect의 자리인가? `fetch('/api/me')`는 어디 있어야 하는가 — `useEffect`인가, 라우팅 데이터 로더인가, 아니면 별도의 인증 컨텍스트인가? "ref 가드 없이도 정직한 코드"를 만들어 보자.

## 마무리, 그리고 다음 장으로

긴 장이었다. 한 번에 다 흡수하기보다는, 익숙해질 때까지 가까이 두고 조금씩 다시 들춰보는 편이 낫다. 이 장에서 우리가 한 일은 한 가지로 압축된다. **`useEffect`를 라이프사이클의 어휘에서 동기화의 어휘로 옮긴 것.** 그 시야 위에서 setup/cleanup의 쌍, reactive value의 정의, 의존성 배열의 정직성, StrictMode의 의도, race condition 방어, 비반응형 코드의 분리 — 이 모두가 한 줄기 이야기로 묶였다.

이 시야가 손에 익으면, 사실 그동안 effect로 풀던 일의 상당 부분이 — **애초에 effect의 자리가 아니었다**는 사실이 점점 또렷해진다. 렌더 중에 계산하면 충분한 값을 effect로 동기화하고 있었거나, 사용자 이벤트로 일어나야 할 일을 effect에 끼워 넣고 있었거나, 두 state를 effect로 cascading하게 연결하다가 무한 루프에 빠지고 있었거나. 이런 패턴들이 의외로 흔하다. 메타에서 Dan Abramov가 내부 코드를 표본 조사했을 때 약 절반에 가까운 `useEffect`가 사실은 불필요했다는 이야기 — 그 통계가 그저 자극적인 인용이 아니라 우리 코드에서도 진실일 가능성이 높다.

그러면 자연스러운 다음 질문이 떠오른다.

> Effect를 정확히 쓰는 법을 배웠다. 그렇다면 — 정말 Effect가 필요한가?

다음 12장은 그 질문을 정면으로 다룬다. "You Might Not Need an Effect." Effect가 필요 없는 가장 흔한 안티패턴들을 한 줄로 진단하고, 어떻게 effect 없이 다시 쓸 수 있는지를 구체적인 패턴으로 정리해보자. 그리고 13장에서는 "의존성 배열의 정직성"이라는 이 장의 줄기를 한 단계 더 깊이 들고 들어간다 — 의존성을 빼고 싶을 때, 어떻게 코드를 다시 짜야 빼는 게 정당해지는지.

이 장의 핵심 한 줄을 다시 한 번 가져가자. **Effect는 동기화다. 사이클의 단위는 setup/cleanup의 쌍이다. 의존성 배열은 그 사이클을 트리거하는 reactive value들의 정직한 목록이다.** 이 세 문장을 손가락 끝에 붙여 두면, 다음 두 장은 의외로 가볍다.
