# 13장. 의존성 배열에 거짓말하지 않기

수요일 오후 네 시쯤이라고 해보자. 지금 막 화면 어딘가에 무난한 useEffect 하나를 적었는데, IDE 옆 줄에 노란 밑줄이 그어진다. `React Hook useEffect has a missing dependency: 'options'. Either include it or remove the dependency array.` 또 그 잔소리다. options를 넣자니 매번 새 객체가 만들어져서 effect가 폭주할 게 뻔하고, 빈 배열을 그대로 두자니 lint가 빨갛게 항의한다. 한 번 해보자, 어쨌든 동작은 한다. 손가락이 자연스럽게 위로 한 줄 올라가고, 익숙한 주문이 적힌다.

```ts
// eslint-disable-next-line react-hooks/exhaustive-deps
useEffect(() => {
  connect(options)
}, [])
```

빨간 줄이 사라진다. 시원하다. 그리고 사흘 뒤, QA에서 "방을 두 번 옮기면 옛날 메시지가 다시 떠요"라는 버그 리포트가 올라온다. 디버거를 붙여서 들여다보면 effect 안에서 읽고 있는 `options.roomId`가 어제 떠난 방 이름 그대로다. 분명히 props는 바뀌었는데, 안에서는 옛날 값을 보고 있다. 어디서 새는지 한참 따라가다가, 드디어 문제의 그 줄에 닿는다. `// eslint-disable-next-line react-hooks/exhaustive-deps`. 사흘 전 내가 적은 그 한 줄짜리 거짓말이다.

조금 억울한 마음이 든다. lint가 너무 까다로워서 어쩔 수 없었다고 핑계를 대고 싶기도 하다. 하지만 이쯤에서 한 번 솔직해져 보자. 그날 우리가 끈 건 lint가 아니다. 우리가 끈 건, Effect와 React 사이에 맺어 두었던 동기화 계약이다. 12장에서 효과적으로 effect를 빼는 법을 살펴봤다면, 이번 장은 정말로 남길 effect들을 어떻게 정직하게 적을 것인가에 대한 이야기다. 의존성 배열이라는, 아주 짧지만 의외로 무거운 그 대괄호 한 쌍을 가운데 두고 살펴보자.

## 의존성 배열은 동기화 계약이다

우선 11장에서 정리한 정의를 한 번 더 끌어다 두는 것이 좋겠다. Reactive value란 컴포넌트 본체에서 선언된 값, 즉 props·state·그것들로부터 파생된 값이다. Effect가 본체 안의 reactive value를 읽고 있다면, 그 effect는 그 값과 동기화되어 있다는 뜻이다. 의존성 배열은 그 동기화 관계를 React에게 일러주는 선언이다. 결국 이런 한 줄로 요약된다.

> 의존성 배열에는 Effect 본문이 읽는 reactive value를 모두 적는다. 더 많지도, 더 적지도 않게.

이 정의에는 세 가지 무게중심이 있다. 첫째, 적는 사람은 lint가 아니라 우리다. lint는 우리 손목을 때려 줄 수는 있어도, 우리가 거짓말을 하기로 작정하면 막아 줄 수 없다. 둘째, "Effect 본문이 읽는 값"이 기준이지, "내가 신경 쓰고 싶은 값"이 기준이 아니다. 셋째, 더 적게 적으면 stale closure가 생기고, 더 많이 적으면 폭주가 생긴다. 양쪽 모두 비용이 있다.

사람들이 자주 빠지는 함정이 여기서 나온다. "이 값은 한 번만 잡으면 되는데, 다시 동기화시키고 싶지 않아서 일부러 뺐어요." 그 마음은 이해할 수 있다. 다만 그건 의존성 배열이 처리할 일이 아니라, 코드를 다르게 짜야 풀리는 문제다. 의존성 배열로 React를 속이는 게 아니라, "이 값은 reactive하지 않게" 코드를 다시 적어야 한다는 뜻이다. 같은 결과처럼 보이지만, 한 쪽은 거짓말이고 다른 한 쪽은 정직한 설계다.

이 차이를 받아들이면, exhaustive-deps lint 경고가 짜증이 아니라 일종의 "지금 네가 무슨 약속을 어기고 있어"라는 알림으로 읽힌다. 그 알림을 죽이는 가장 비싼 방법이 disable 주석이고, 가장 정직한 방법이 코드 수정이다. 이 장에서는 후자가 어떻게 생겼는지를 차근차근 살펴보자.

## lint를 침묵시키는 일의 진짜 비용

lint를 끄는 행위가 왜 위험한지 좀 더 차분히 풀어보자. exhaustive-deps 규칙은 이런 일을 한다. Effect 본문에서 참조되는 reactive value가 무엇인지 정적으로 분석한 다음, 의존성 배열에 누락된 게 있으면 표시한다. 이 규칙은 단순히 "React 팀의 권고"가 아니라, **closure가 stale해지는 정확한 조건**을 포착한다. 의존성에 안 적은 reactive value를 effect 안에서 읽고 있다면, 그 effect가 다음에 언제 다시 실행되든 옛날 렌더의 값이 박힌 채 실행된다. 자바스크립트의 클로저가 그렇게 동작하니까.

그래서 disable 주석은 정확히 이런 약속을 우리가 일방적으로 깨는 행위가 된다.

```ts
// 옛날 roomId가 박힌 채로 영원히 굳어 있는 코드
useEffect(() => {
  const conn = connect(roomId)
  return () => conn.disconnect()
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, [])
```

이 코드는 한 번도 동작한 적이 없는 게 아니다. 첫 마운트에서는 멀쩡히 동작한다. 문제는 그다음에 `roomId`가 바뀌었을 때다. 부모는 새로운 prop을 내려보냈고 화면 위 다른 부분은 새 방을 보여주는데, 이 effect만 옛날 방에 머물러 있다. 사용자는 방을 옮긴 줄 알지만, 메시지 스트림은 어제의 그 방에 그대로 연결되어 있다. 이 미묘한 어긋남은 종종 한참 동안 들키지 않는다. 들킨 뒤에는 디버깅에 며칠을 잃고 나서야 원인을 찾는다.

여기서 한국어 커뮤니티에 자주 도는 한 줄짜리 격언이 떠오른다. "lint를 죽이는 가장 흔한 이유는 그 자리에 있는 코드가 잘못되었기 때문이다." 즉 lint가 못마땅할 때, 우리가 진짜로 해야 할 일은 lint를 침묵시키는 게 아니라 **그 자리의 코드를 lint가 만족할 만한 모양으로 다시 적는 것**이다. 그러면 자연스럽게 의존성도 줄어들고, stale closure 위험도 사라진다. 실제로는 그게 가능한 경우가 거의 대부분이다. 단지 어떻게 적어야 그렇게 되는지를 모를 뿐이다.

이제 그 방법을 살펴보자. 크게 네 가지로 정리할 수 있다. (1) effect가 그 값을 정말 읽고 있는지 다시 따져보기, (2) 함수 의존성을 어디에 두어야 하는지 정리하기, (3) 객체 의존성을 원시값으로 분해하기, (4) 사건과 동기화를 분리하기. 하나씩 가보자.

## 진짜 방법 1 — Effect는 정말 그 값을 읽고 있는가

가장 먼저 던져야 할 질문은 의외로 단순하다. **이 의존성, effect가 정말로 읽고 있는 거 맞나?** 의외로 자주, 우리는 effect가 직접 사용하지도 않는 값을 의존성으로 끌고 있다. 이런 코드를 보자.

```ts
function ChatRoom({ roomId, serverUrl, theme }: Props) {
  useEffect(() => {
    const conn = createConnection(serverUrl, roomId)
    conn.connect()
    return () => conn.disconnect()
  }, [roomId, serverUrl, theme])
}
```

`theme`을 의존성으로 넣어 놓았지만, effect 본문 안에서는 theme을 한 번도 참조하지 않는다. 아마 "테마가 바뀔 수도 있으니까 일단 넣어 둘까" 하는 마음이었을 것이다. 결과는? 사용자가 다크 모드 토글을 누를 때마다 채팅 연결이 끊겼다 다시 맺힌다. 사용자 입장에선 "테마 바꿨더니 채팅이 끊겼어요"라는 끔찍한 일이 된다.

해법은 이 경우엔 너무 단순하다. theme을 의존성에서 빼면 된다. effect가 안 읽는 값은 의존성이 아니다. 우리가 의존성을 줄이고 싶을 때 가장 먼저 따져야 할 게 바로 이거다. lint도 그러라고 한다. exhaustive-deps는 우리한테 "더 넣어"라고만 말하는 게 아니라, "안 읽는 건 빼"라고도 말한다.

비슷한 케이스로, 객체에서 한 필드만 쓰는데 객체 전체를 의존성에 넣은 경우도 있다.

```ts
useEffect(() => {
  fetch(`/api/posts/${user.id}`)
}, [user]) // user.id만 쓰는데 user 전체를 의존성으로 잡았다
```

이 effect는 사용자 객체의 다른 필드 — 예컨대 `user.lastSeenAt` 같은 게 갱신될 때마다 — 까지 따라 다시 실행된다. 우리가 신경 쓰는 건 `user.id`뿐이다. 그러면 의존성도 그렇게 적어 주는 편이 낫다.

```ts
const userId = user.id
useEffect(() => {
  fetch(`/api/posts/${userId}`)
}, [userId])
```

자그마한 차이지만, effect의 동기화 의도가 또렷해졌다. "이 effect는 userId 변화에만 반응한다"는 선언이 코드 한 줄로 분명해졌다는 점이 핵심이다. 의존성을 줄이는 첫걸음은 거의 언제나 이런 정직한 정리에서 시작한다.

## 진짜 방법 2 — 함수 의존성, 안에 둘까 밖에 둘까

다음은 함수다. 컴포넌트 본체에서 선언한 함수도 reactive value다. 매 렌더마다 새로 만들어지는, 새로운 참조를 갖는 함수이기 때문이다. 그래서 effect가 그 함수를 호출하면, lint는 의존성에 그 함수를 적으라고 한다. 그런데 적어 두면 매 렌더마다 의존성이 바뀐 것으로 간주되어 effect가 매번 다시 실행된다. 폭주다. 난감하다.

이런 경우 선택지는 두 가지다. **함수를 effect 안으로 옮기거나**, **함수를 effect 바깥에서 안정화시키거나**. 둘 중 어떤 쪽이 나은지는 함수가 무엇을 하는지에 달려 있다.

먼저 effect 전용 헬퍼라서 굳이 바깥에 둘 필요가 없는 함수라면, effect 안으로 들여보내는 편이 낫다. 다른 곳에서 안 쓰는 함수를 굳이 바깥에 빼 두면 의존성만 늘어난다.

```ts
// 안 좋은 모양
function ChatRoom({ roomId }: { roomId: string }) {
  const createOptions = () => ({ serverUrl: 'wss://chat.example', roomId })
  useEffect(() => {
    const conn = connect(createOptions())
    return () => conn.disconnect()
  }, [createOptions]) // 매 렌더마다 새 함수, 매 렌더마다 effect 재실행
}

// 정직한 모양 — 함수가 effect 전용이면 안에서 정의한다
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const createOptions = () => ({ serverUrl: 'wss://chat.example', roomId })
    const conn = connect(createOptions())
    return () => conn.disconnect()
  }, [roomId])
}
```

옮기고 나면 의존성에서 함수가 사라지고, 그 자리에 함수가 진짜로 읽고 있던 reactive value(`roomId`)만 남는다. effect는 roomId가 바뀔 때만 다시 실행된다. 깔끔하다.

함수를 컴포넌트 바깥, 즉 모듈 스코프로 끌어올릴 수 있는 경우도 있다. 그 함수가 props도 state도 아무것도 안 읽는다면, 그건 사실 reactive value가 아니다. 그러면 컴포넌트 안에 둘 이유가 없다.

```ts
// 모듈 스코프로 끌어올리면 reactive value가 아니다
function buildOptions(roomId: string) {
  return { serverUrl: 'wss://chat.example', roomId }
}

function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const conn = connect(buildOptions(roomId))
    return () => conn.disconnect()
  }, [roomId])
}
```

함수를 어디에 둘지 정하는 기준은 "이 함수가 컴포넌트의 reactive value를 읽고 있는가"다. 안 읽는다면 모듈 스코프로 올리고, 읽는다면 effect 안에 두는 편이 낫다. `useCallback`은 가능하면 마지막 카드로 미루자. useCallback은 함수 정체성을 안정화시켜 주긴 하지만, 그 함수가 의존하는 값이 또 다른 reactive value라면 결국 같은 문제를 한 단계 미루는 데 그친다. 정말 다른 컴포넌트에 함수를 prop으로 내리는데 그쪽이 메모이제이션에 의존하는 경우 정도가 useCallback의 정당한 자리다.

## 진짜 방법 3 — 객체 의존성은 원시값으로 분해한다

이제 객체 차례다. 이게 가장 자주 사람을 헷갈리게 하는 함정이다. 채팅 컴포넌트의 흔한 패턴을 보자.

```ts
function ChatRoom({ roomId }: { roomId: string }) {
  const options = { serverUrl: 'wss://chat.example', roomId }

  useEffect(() => {
    const conn = createConnection(options)
    conn.connect()
    return () => conn.disconnect()
  }, [options]) // 매 렌더마다 새 객체!
}
```

`options`는 매 렌더마다 새 객체 리터럴로 만들어진다. React는 의존성을 `Object.is`로 비교하므로, 매 렌더마다 의존성이 바뀐 것처럼 보이고 effect가 매번 재실행된다. 사용자 입장에서는 키를 한 번 누를 때마다 채팅 연결이 끊어졌다 다시 맺어지는 비참한 광경을 보게 된다. 끔찍한 일이다.

여기서 가장 쉽고 정직한 처방이 **원시값으로 분해**하기다. 객체 자체를 의존성으로 두지 말고, effect가 진짜로 신경 쓰는 필드들을 꺼내서 의존성으로 쓰자.

```ts
function ChatRoom({ roomId }: { roomId: string }) {
  const serverUrl = 'wss://chat.example'

  useEffect(() => {
    const options = { serverUrl, roomId }
    const conn = createConnection(options)
    conn.connect()
    return () => conn.disconnect()
  }, [serverUrl, roomId])
}
```

객체 생성 자체를 effect 안으로 옮기고, 의존성 배열에는 원시값(`serverUrl`, `roomId`)만 남았다. 문자열이나 숫자 같은 원시값은 동등성 비교가 값 단위로 일어나므로, 진짜로 값이 바뀌었을 때만 effect가 다시 돈다. 같은 처방이 props로 받은 객체에도 그대로 통한다.

```ts
// props로 받은 options 객체 — 부모가 매 렌더마다 새로 만들고 있을 수도 있다
function ChatRoom({ options }: { options: ChatOptions }) {
  const { serverUrl, roomId } = options // 분해해서 원시값으로 만든다

  useEffect(() => {
    const conn = createConnection({ serverUrl, roomId })
    conn.connect()
    return () => conn.disconnect()
  }, [serverUrl, roomId])
}
```

이 패턴이 좋은 이유는 단순히 폭주를 막아서가 아니다. **이 effect가 진짜로 동기화하는 게 무엇인지가 코드에 그대로 적혀 있게 되기 때문**이다. "options 객체에 동기화한다"는 모호한 선언 대신, "serverUrl과 roomId에 동기화한다"는 또렷한 선언이다. 6개월 뒤에 이 코드를 다시 보는 동료(또는 미래의 자기 자신)가 무얼 손대도 안전한지를 한눈에 알 수 있다.

여기서 "원시값으로 분해"의 범위를 한 번 더 짚어 두자. 원시값은 문자열·숫자·불리언처럼 값 단위로 비교되는 자료형이다. 객체·배열·함수는 참조로 비교되므로, 분해해서 의존성에 적은 결과가 다시 객체나 배열이라면 문제가 똑같이 재발한다. 예를 들어 `const { tags } = options`처럼 분해했더라도 `tags`가 배열이라면, 부모가 매번 새 배열을 내려보내는 한 같은 폭주가 일어난다. 이런 경우엔 한 단계 더 들어가서, 그 배열의 원시값 표현을 의존성으로 만들거나(`tags.join(',')` 같은 키), 부모쪽에서 안정된 참조를 보장하도록 손을 봐야 한다. "분해"라는 단어를 적당히 외우지 말고, **결국 의존성에 들어가는 값이 원시값인지**까지 확인하는 습관을 들이자.

또 하나 자주 만나는 변형이, 컴포넌트 안에서 객체를 만들지만 effect와 무관한 경우다. 예를 들어 렌더에 쓰는 스타일 객체나, 자식에게 prop으로 내려보내는 옵션 객체 같은 것들. 이런 친구들은 effect 의존성 이야기가 아니라 자식 컴포넌트의 메모이제이션 이야기다. 의존성 배열의 영역과 메모이제이션의 영역을 섞지 말자. 우리가 지금 다루는 건 어디까지나 **`useEffect`의 의존성 배열에 들어가는 값**의 모양이다. 자식의 props 안정성은 그 자식이 정말 메모되어야 할 때, 그때 가서 따로 다룰 일이다.

비슷한 처방이 함수형 setState와도 통한다. 기억해 두자. 의존성으로 들어가는 것의 가짓수를 줄이는 게 목표라면, 자주 등장하는 한 가지 패턴이 더 있다.

```ts
// 의존성에 messages가 들어와서 새 메시지가 올 때마다 effect 재실행
useEffect(() => {
  const conn = createConnection(serverUrl, roomId)
  conn.on('message', (m) => setMessages([...messages, m]))
  conn.connect()
  return () => conn.disconnect()
}, [serverUrl, roomId, messages])

// 함수형 업데이트로 messages 의존성을 끊는다
useEffect(() => {
  const conn = createConnection(serverUrl, roomId)
  conn.on('message', (m) => setMessages((prev) => [...prev, m]))
  conn.connect()
  return () => conn.disconnect()
}, [serverUrl, roomId])
```

`setMessages(prev => [...prev, m])`로 적으면, 더 이상 `messages`라는 reactive value를 effect 본문이 읽지 않는다. 따라서 의존성에서 빼도 거짓말이 아니다. 정직하게 줄어든 것이다. 이런 자그마한 어휘 차이 하나가, 폭주하는 effect를 멈추는 정확한 도구가 된다.

## 진짜 방법 4 — 사건과 동기화를 분리하자

여기까지 정리해도 풀리지 않는 한 종류의 문제가 남는다. **Effect가 어떤 값을 읽긴 하는데, 그 값이 바뀐다고 해서 다시 동기화하고 싶지는 않은 경우**다. 가장 자주 인용되는 예가 채팅 + 테마다.

```ts
function ChatRoom({ roomId, theme }: { roomId: string; theme: 'light' | 'dark' }) {
  useEffect(() => {
    const conn = createConnection(roomId)
    conn.on('connected', () => {
      showNotification('Connected!', theme) // theme을 읽는다
    })
    conn.connect()
    return () => conn.disconnect()
  }, [roomId, theme])
}
```

`showNotification`은 theme을 봐야 알림창 색을 맞출 수 있다. 그래서 effect 안에서 theme을 읽는다. lint는 정직하게 "theme을 의존성에 넣으세요"라고 한다. 넣었다. 그런데 사용자가 다크모드 토글을 누르는 순간, 채팅이 끊겼다 다시 맺힌다. 우리가 원한 건 "다음에 connected 이벤트가 발생할 때만 최신 theme이 알림창에 반영"이지, "지금 당장 다시 연결"이 아니다.

이 어긋남을 React 팀은 "사건(event)과 동기화(synchronization)의 혼선"이라고 부른다. 우리가 적은 코드 안에는 두 가지 다른 종류의 일이 같이 들어 있다. 하나는 동기화 — `roomId`에 맞춰 연결을 유지하는 일. 다른 하나는 사건 — connected가 발생했을 때 알림을 띄우는 일. 이 두 가지를 한 effect에 묶어 두면 의존성 배열이 둘의 요구를 동시에 만족시키지 못한다.

이 갈등을 풀려고 React 팀이 실험적으로 도입한 어휘가 `useEffectEvent`다. 이름 그대로 "effect 안에서 호출하지만, reactive하지는 않은 함수"를 만든다. 사건처럼 동작하지만, effect의 동기화 사이클에는 끼지 않는다.

```ts
import { experimental_useEffectEvent as useEffectEvent } from 'react'

function ChatRoom({ roomId, theme }: { roomId: string; theme: 'light' | 'dark' }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme) // 항상 최신 theme을 본다
  })

  useEffect(() => {
    const conn = createConnection(roomId)
    conn.on('connected', () => onConnected())
    conn.connect()
    return () => conn.disconnect()
  }, [roomId])
}
```

`onConnected`는 의존성에 적지 않는다. 적으면 안 된다. effect event는 reactive하지 않게 설계된 어휘이고, 의존성에 적는 순간 그 의도가 깨진다. effect는 이제 `roomId` 하나에만 동기화된다. theme이 바뀌면? 다음 번 connected가 발생할 때 `onConnected` 안에서 자연스럽게 최신 theme이 읽힌다. 사건과 동기화가 분리되었다.

여기서 한 가지 짚고 가야 할 점이 있다. 2026년 시점에도 `useEffectEvent`는 여전히 React 카나리에서 실험 중인 API다. 안정 채널에서는 import 경로가 `experimental_useEffectEvent` 같은 이름으로만 노출되고, 라이브러리에 따라서는 아직 사용이 권장되지 않는다. 이 어휘를 도입한다면 두 가지를 함께 결정하자.

> **이 책의 입장:** `useEffectEvent`는 "사건과 동기화는 다르다"는 어휘를 분명하게 만들어 준다는 점에서 가치 있다. 단, lint 침묵용 만능 도구로 쓰면 안 된다. 그건 disable 주석을 좀 길게 적은 것에 지나지 않는다. 또한 안정화 전에 도입한다면, 팀이 "이건 실험 API이므로 구체적인 동작이 바뀔 수 있다"는 점을 알고 가야 한다. 안정 채널이 필요한 프로젝트라면, 다음 절에서 살펴볼 ref 패턴을 먼저 검토하는 편이 낫다.

이 입장에 어떤 사람들은 동의하지 않는다. HN 같은 곳을 돌아다녀 보면 "useEffectEvent는 근본 문제를 우회하는 패치일 뿐"이라는 비판도 나온다. 다른 한편에는 "reactive와 non-reactive를 분리하는 어휘는 어차피 필요했고, 이걸 명시적으로 할 수 있게 된 게 차라리 낫다"는 옹호도 있다. 둘 다 일리가 있다. 다만 우리에게 중요한 건 한 가지다 — 그게 어떤 도구든, **lint를 끄지 않고 정직하게 의도를 표현하기 위한 도구**여야 한다는 점이다.

useEffectEvent 박스를 닫기 전에, 자주 빠지는 오용 사례를 두 가지만 짚어 두자. 첫째, **effect event 함수를 다른 컴포넌트에 prop으로 넘기지 말자.** effect event는 정의된 컴포넌트의 effect 안에서만 호출되도록 설계되어 있다. 자식에게 넘기면 자식 입장에서는 그게 reactive인지 아닌지가 모호해지고, 자식의 effect 의존성에 적었다가 안 적었다가 하는 혼란이 생긴다. 둘째, **effect event를 의존성 배열에 적지 말자.** lint도 적지 말라고 한다. 적는 순간 effect event의 정체성이 깨진다. 이 두 줄짜리 약속을 어기지 않으면, useEffectEvent는 사건과 동기화의 어휘를 또렷하게 만들어 주는 깔끔한 도구로 자리한다.

## useEffectEvent 없이 풀고 싶다면 — ref+effect 패턴

실험 API에 의존하기 부담스러운 환경이라면 어떻게 할까. 같은 효과를 얻을 수 있는 보수적인 패턴이 하나 있다. ref에 최신 값을 따로 보관해 두는 방식이다.

```ts
function ChatRoom({ roomId, theme }: { roomId: string; theme: 'light' | 'dark' }) {
  const themeRef = useRef(theme)

  // 매 렌더마다 ref를 최신 값으로 갱신한다 (commit 단계에서)
  useEffect(() => {
    themeRef.current = theme
  })

  useEffect(() => {
    const conn = createConnection(roomId)
    conn.on('connected', () => {
      showNotification('Connected!', themeRef.current) // ref로 읽으면 reactive가 아니다
    })
    conn.connect()
    return () => conn.disconnect()
  }, [roomId])
}
```

원리는 단순하다. ref는 reactive value가 아니다. 10장에서 살펴봤듯, ref는 바뀌어도 컴포넌트가 리렌더되지 않고, 그래서 의존성 배열에 적지 않아도 lint가 잔소리하지 않는다. 매 렌더마다 별도의 effect로 `themeRef.current`를 최신 theme으로 갱신해 두면, 채팅 effect는 connected가 발생한 시점에 ref를 통해 최신 theme을 가져갈 수 있다.

이 패턴이 매력적인 만큼, 잊지 말아야 할 트레이드오프가 있다. 첫째, **읽는 시점**이 중요하다. ref는 commit 이후에 갱신된다. 따라서 렌더 중에 ref를 읽으면 한 박자 옛날 값이 나올 수 있다. 우리가 보는 케이스에선 connected 콜백이 비동기적으로 호출되므로 안전하지만, 동기 경로에서 같은 ref를 쓰려고 하면 미묘하게 어긋날 수 있다. 둘째, ref가 "사실상 imperative escape hatch"라는 점을 받아들이고 써야 한다. 데이터 흐름을 ref로 우회하기 시작하면, 어디서 어떤 시점에 어떤 값을 읽고 있는지가 명확하지 않은 코드가 만들어지기 쉽다. 그래서 ref+effect 패턴은 "꼭 필요한 곳에만, 그것도 사건 콜백 내부에서만" 쓰는 편이 낫다.

비교하면 이렇다. `useEffectEvent`는 어휘가 더 또렷하다 — "이건 사건 함수, 의존성으로 안 들어감"이라고 함수 선언 단계에서 선언된다. ref+effect는 어휘가 약간 우회적이다 — "이건 ref이고, ref는 reactive가 아니다"라는 것을 독자가 추론해야 한다. 그렇지만 ref 패턴은 안정 채널에서 그대로 동작하고, 어디에 가져가도 변하지 않는다. 둘 중 어떤 쪽을 고를지는, 팀이 카나리 채택을 어디까지 받아들이느냐에 달려 있다.

## 사건은 effect의 일이 아니다

사건과 동기화의 이야기를 한 번 더 짚어 두자. `useEffectEvent`나 ref 패턴이 필요한 건 어디까지나 **외부 시스템 콜백(connected, message 도착 등) 안에서 최신 값을 읽고 싶은 경우**다. 사용자 사건 — 클릭, 폼 제출, 키보드 입력 — 은 effect의 일이 아니다. 그건 그냥 이벤트 핸들러의 일이다.

12장에서도 짚었지만, 이 구분이 흐려지는 순간 useEffect에 별 일이 다 들어가기 시작한다. 예를 들어 이런 코드를 한 번쯤 본 적이 있을 것이다.

```ts
// 사용자가 'Buy' 버튼을 누르면 일어나야 하는 일을 effect에 적은 사례
function ProductPage({ product, navigate }) {
  useEffect(() => {
    if (product.isInCheckout) {
      submitOrder(product) // 결제가 두 번 이상 일어날 수도 있는 끔찍한 코드
    }
  }, [product])
}
```

이건 stale closure나 의존성 배열의 문제가 아니다. 사건을 effect에 잘못 둔 것이다. "결제하기"는 사용자가 버튼을 누른 그 순간 한 번 일어나야 하는 사건이다. effect는 외부 시스템과의 동기화를 맡는 자리이지, 사용자 의도를 해석하는 자리가 아니다. 이런 코드는 의존성 배열을 어떻게 손봐도 깨끗해지지 않는다. 자리를 옮겨야 한다.

```ts
function ProductPage({ product }) {
  function handleBuy() {
    submitOrder(product)
  }
  return <Button onClick={handleBuy}>Buy</Button>
}
```

의존성 배열의 문제가 안 풀릴 때, 한 번쯤은 근본을 의심해 보자. 혹시 이 일이 effect 안에 있어서는 안 되는 일은 아닌가? 사건이라면 핸들러로 빼고, 비싼 계산이라면 useMemo로 옮기고, 파생값이라면 그냥 렌더 중에 계산하자. 12장의 결론을 한 번 더 끌어다 두면 — 가장 좋은 의존성 배열은 적지 않아도 되는 의존성 배열이다.

## non-reactive 값은 의존성에 넣지 않는다

여기까지 따라오면 의존성 배열의 윤곽이 어느 정도 잡혔을 것이다. 그런데 한 가지 자주 헷갈리는 포인트가 더 남아 있다. **non-reactive value는 의존성에 적지 않는다.** 이건 lint도 적으라고 안 한다. 적으면 오히려 의도를 흐린다.

대표적으로 세 종류다.

- 모듈 스코프 상수: `const API_URL = '...'` 같은 것. 컴포넌트 본체 바깥에서 한 번 정해진 값은 reactive value가 아니다.
- ref: 10장에서 본 그 ref. ref가 바뀌어도 컴포넌트가 리렌더되지 않으니, ref는 reactive하지 않다. effect 안에서 `ref.current`를 읽거나 쓰는 건 자연스러운 일이지만, ref 자체를 의존성에 적지는 말자.
- `useEffectEvent`로 만든 사건 함수: 앞서 본 그 친구. effect event는 일부러 reactive하지 않게 설계된 함수다. 의존성에 적는 건 설계 의도를 어기는 일이고, 적는 순간 effect가 매 렌더마다 실행되거나 미묘한 버그가 따라붙는다.

이걸 한 줄로 잡고 가자.

> **의존성 배열에는 reactive value만 적는다. non-reactive value는 적지 않는다. 그게 effect와 React 사이의 정직한 계약이다.**

## 케이스 스터디 — 실무에서 마주치는 세 장면

원칙은 정리되었으니, 실전 무대에 한 번씩 올려 보자. 세 가지 장면을 골랐다. 모두 한 번쯤은 실제로 마주칠 모양들이다.

### 장면 1. 검색 인풋 + 디바운스 fetch

검색창에 글자를 칠 때마다 추천어를 띄워 주고 싶다고 해보자. 처음에 적은 코드는 아마 이런 모양일 것이다.

```ts
function SearchBox({ apiKey }: { apiKey: string }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<string[]>([])

  useEffect(() => {
    const fetchOptions = { apiKey, headers: { 'X-Client': 'web' } }
    let ignore = false
    const timer = setTimeout(async () => {
      const r = await fetch(`/api/suggest?q=${query}`, fetchOptions)
      const json = await r.json()
      if (!ignore) setResults(json.items)
    }, 300)
    return () => {
      ignore = true
      clearTimeout(timer)
    }
  }, [query, fetchOptions]) // 잠깐, fetchOptions가 의존성에 들어갔다
}
```

이 코드의 문제는 두 가지다. 첫째, `fetchOptions`는 매 렌더마다 새 객체로 만들어지는데 의존성에 그대로 들어가 있다. 둘째, 사실 우리가 진짜로 동기화하고 싶은 건 `query`와 `apiKey`뿐이다. `headers`처럼 안 변하는 자리는 effect 안에서 매번 새로 만들어도 상관없다.

정직하게 다시 적자.

```ts
function SearchBox({ apiKey }: { apiKey: string }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<string[]>([])

  useEffect(() => {
    let ignore = false
    const timer = setTimeout(async () => {
      const r = await fetch(`/api/suggest?q=${query}`, {
        headers: { 'X-Client': 'web', Authorization: `Bearer ${apiKey}` },
      })
      const json = await r.json()
      if (!ignore) setResults(json.items)
    }, 300)
    return () => {
      ignore = true
      clearTimeout(timer)
    }
  }, [query, apiKey])
}
```

객체를 effect 안으로 들여보냈고, 의존성에는 진짜 reactive value 두 개(`query`, `apiKey`)만 남았다. 이제 키 입력 한 번에 effect 한 번. 디바운스 타이머는 cleanup으로 깔끔히 정리되고, race condition 방지를 위한 ignore 플래그도 살아 있다. 이게 우리가 그리고 싶었던 그림이다.

여기서 욕심을 내서 한 발 더 갈 수도 있다. `fetch + race condition + 디바운스`라는 조합 자체가 한 코드베이스에서 여러 번 등장한다면, 이건 14장에서 살펴볼 커스텀 훅 추출의 자연스러운 후보다. `useDebouncedFetch(query)` 같은 모양으로 묶을 수 있는지를 머릿속에 한 줄로 적어 두고 다음 장으로 가져가자.

### 장면 2. 외부 위젯 인스턴스를 React props에 따라 제어하기

지도 위젯, 비디오 플레이어, 차트 라이브러리처럼 비-React 객체를 제어해야 하는 경우는 흔하다. 흔히 이런 모양으로 시작한다.

```ts
function VideoPlayer({ src, isPlaying }: { src: string; isPlaying: boolean }) {
  const ref = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    const player = createPlayer(ref.current!, { src, autoplay: false })
    if (isPlaying) player.play()
    return () => player.dispose()
  }, [src, isPlaying])
}
```

문제는 `isPlaying`이 의존성에 들어가 있는 탓에 토글 한 번에 플레이어 인스턴스 자체가 매번 dispose되었다 다시 만들어진다는 점이다. 한 번씩 덜컹거리고 마는 게 아니라, 그 위에 쌓인 자막·볼륨·재생 위치 같은 게 전부 초기화된다. 끔찍한 일이다.

이 effect는 사실 두 가지 일을 같이 하고 있다. (1) `src`에 맞춰 플레이어 인스턴스를 유지하는 일. (2) `isPlaying`에 맞춰 재생 상태를 토글하는 일. 두 개의 동기화 사이클이 한 effect에 묶여 있다. 풀어 주자.

```ts
function VideoPlayer({ src, isPlaying }: { src: string; isPlaying: boolean }) {
  const ref = useRef<HTMLVideoElement>(null)
  const playerRef = useRef<ReturnType<typeof createPlayer> | null>(null)

  // (1) src에 맞춰 플레이어 인스턴스 자체를 동기화
  useEffect(() => {
    const player = createPlayer(ref.current!, { src, autoplay: false })
    playerRef.current = player
    return () => {
      playerRef.current = null
      player.dispose()
    }
  }, [src])

  // (2) isPlaying에 맞춰 재생 상태만 토글 — 인스턴스는 그대로
  useEffect(() => {
    const player = playerRef.current
    if (!player) return
    if (isPlaying) player.play()
    else player.pause()
  }, [isPlaying])
}
```

두 effect로 분리하고 나면 의존성 배열도 정직하다. `[src]`는 진짜로 src에만 동기화하고, `[isPlaying]`은 진짜로 재생 토글만 한다. ref는 두 effect 사이에 살아 있는 인스턴스를 들고 있는 다리 역할을 한다. 이게 10장에서 본 ref가 13장에서 다시 등장하는 자리다 — 비-React 시스템과의 경계에서 reactive하지 않게 가져가야 하는 값을 보관하는 도구.

### 장면 3. 사용자 사건이 effect로 새 들어왔을 때

마지막은 가장 흔한, 그러나 가장 자주 놓치는 함정이다. 다음 코드는 한참 동안 잘 돌다가 결제가 한 번씩 두 번 일어나는 끔찍한 버그를 일으켰다.

```ts
function CheckoutPage({ cart, navigate }: Props) {
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    if (submitted) {
      submitOrder(cart) // 결제!
      navigate('/thanks')
    }
  }, [submitted, cart, navigate])
}
```

submit 버튼 핸들러가 `setSubmitted(true)`를 부르고, 그러면 effect가 결제를 일으킨다. 얼핏 잘 돌아 보인다. 그런데 `cart`가 한 번씩 같은 항목으로 다시 만들어지면(부모가 새 배열로 내려보내면) effect가 한 번 더 실행되고, 결제도 한 번 더 일어난다. 의존성 배열에 거짓말한 적도 없는데 왜 이런 일이 벌어질까?

답은 단순하다. 이건 동기화가 아니다. 이건 **사건**이다. "결제하기"는 사용자가 버튼을 누른 그 순간 한 번 일어나야 하는 일이고, 그 어떤 reactive value의 변화에도 다시 일어나서는 안 된다. effect는 외부 시스템과 동기화하는 자리이지, 사용자의 의도를 한 번만 실행하는 자리가 아니다. 자리를 옮기자.

```ts
function CheckoutPage({ cart, navigate }: Props) {
  async function handleSubmit() {
    await submitOrder(cart)
    navigate('/thanks')
  }
  return <Button onClick={handleSubmit}>결제하기</Button>
}
```

핸들러로 옮기는 순간 `submitted`라는 state도 사라지고, effect도 사라진다. 의존성 배열을 어떻게 손볼지 고민할 필요 자체가 없어졌다. 의존성 배열의 가장 좋은 모양은, 적지 않아도 되는 모양이다. 이 12장의 결론이 13장에서 다시 메아리치는 자리가 바로 여기다.

세 장면 모두에서 우리가 한 일은 같다. effect가 진짜로 동기화하는 게 무엇인지를 또렷이 만들고, 사건은 핸들러로 빼고, 비-React 인스턴스는 ref로 들어 두고, 객체는 분해하거나 안으로 옮긴다. 이 동작이 손가락에 익으면, 의존성 배열은 더 이상 우리를 짜증나게 만드는 대상이 아니라, 우리가 적은 코드의 의도를 검증해 주는 동료가 된다.

## stale closure가 정확히 어떻게 만들어지는가

이쯤에서 한 번, "stale closure"라는 단어가 정확히 무엇을 말하는지를 손가락으로 짚어 보자. 어휘가 흐릿하면 코드가 정확해지지 않는다.

리액트는 매 렌더에서 컴포넌트 함수를 처음부터 다시 호출한다. 그때마다 props·state·그것에서 파생된 모든 변수는 **그 렌더만의 독립된 지역 변수**로 만들어진다. 11장에서 살펴본 대로, 같은 이름의 `roomId`라도 첫 번째 렌더의 `roomId`와 두 번째 렌더의 `roomId`는 서로 다른 지역 변수다. 단지 이름이 같을 뿐이다.

useEffect로 넘긴 setup 함수도 그 렌더의 클로저 안에서 만들어진다. 그 함수는, 만들어진 그 시점의 지역 변수들을 머릿속에 봉인한 채로 미래의 어느 순간에 실행된다. 만약 그 시점 이후에 React가 effect를 한 번도 다시 실행하지 않는다면, 봉인된 그 옛날 값은 영원히 그 자리에 갇힌다. 두 번째, 세 번째 렌더가 일어나든 말든 — 그 함수가 다시 만들어지지 않는 한 — 안에서는 첫 번째 렌더의 `roomId`만 보인다. 이게 stale closure다. 어렵지 않다. 그저 자바스크립트의 클로저가 정직하게 동작하고 있을 뿐이다.

이 그림을 받아들이면, 의존성 배열의 의미가 한 번 더 또렷해진다. 의존성 배열은 React에게 이렇게 말하는 도구다. **"여기 적힌 값이 바뀌면, 이 effect를 다음 렌더의 새 클로저로 다시 만들어 다오."** 그래서 의존성에 거짓말을 하면, React는 새 클로저를 안 만들고, 우리는 옛 클로저에 박힌 옛 값을 계속 보게 된다.

작은 코드로 한 번 더 짚어 보자.

```ts
function Counter({ step }: { step: number }) {
  const [n, setN] = useState(0)
  useEffect(() => {
    const id = setInterval(() => {
      setN(n + step) // 첫 렌더의 n=0, step=1이 봉인됨
    }, 1000)
    return () => clearInterval(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
}
```

이 카운터는 1초마다 화면에 1만 띄우고 더 이상 자라지 않는다. 왜? interval 콜백이 첫 렌더의 `n`(0)과 `step`(1)을 봉인한 채로 1초마다 `setN(0 + 1)`을 호출하니까. n은 영원히 0 → 1만 왕복한다. lint를 끈 그 한 줄이 정확히 만들어 낸 풍경이다.

여기서 얻는 처방은 두 갈래다. 의존성을 정직하게 적어 매 렌더마다 새 setup으로 다시 만들도록 두든가 — interval처럼 그게 비싼 경우엔 함수형 setState로 의존성을 끊든가. 둘 다 우리가 이미 본 도구다. 다만 stale closure가 어디서 어떻게 생기는지를 한 번 시각화하고 나면, 같은 도구를 적을 때의 손가락의 무게가 달라진다. "lint를 만족시키려고" 적는 게 아니라, "옛날 값이 박히지 않게" 적는 것이다. 같은 코드, 다른 의도다.

## 의존성 배열을 운영 관점에서 본다 — 팀과 코드리뷰

지금까지 우리가 살핀 건 한 컴포넌트 안에서의 정직함이다. 그런데 실무는 거기서 끝나지 않는다. 같은 코드베이스에서 여러 사람이 effect를 적는다. 그래서 의존성 배열에 대한 약속을 **팀 단위로** 가져가는 게 실용적이다. 몇 가지 운영 차원의 권고를 정리해 두자.

첫째, **`react-hooks/exhaustive-deps` 규칙을 error 레벨로 두는 편이 낫다.** warning으로만 두면 시간이 흐를수록 노란 줄이 쌓이고, 그 줄들 사이에서 진짜 위험한 케이스가 묻힌다. error로 두면 빌드가 깨지고, 깨지는 순간 정직하게 다시 적든지 명시적으로 disable 하든지를 매번 결정하게 된다. 결정을 미루지 않는 것 자체가 운영의 핵심이다.

둘째, **`eslint-disable-next-line` 한 줄에는 짧은 이유 주석이 같이 붙어야 한다.** 코드리뷰 규칙으로 못박아 두자. 단순히 disable만 적는 PR은 머지하지 말고, 옆에 "왜 이걸 끌 수 밖에 없는가"가 적혀 있는지를 본다. 6개월 뒤에 누군가 그 자리를 다시 만났을 때, 그 한 줄이 며칠을 살려 준다.

```ts
// 라이브러리 인스턴스(externalRef.current)는 모듈 스코프 객체로
// 사실상 reactive하지 않다. 의존성에 넣으면 매 렌더 재초기화 발생.
// 라이브러리 v3.2 이후로는 이 자리가 안정 — 2026-08 검토.
// eslint-disable-next-line react-hooks/exhaustive-deps
```

이런 형태가 그나마 정직한 disable의 모양이다. 끌 거면 끄는 사람이 책임을 지자. 책임을 진다는 건 결국, 미래의 디버거가 잡고 들어갈 끈을 코드 옆에 남겨 두는 일이다.

셋째, **PR 리뷰 체크리스트에 "이 effect의 의존성에 객체/함수가 들어가 있나?"를 한 줄 넣자.** 이걸 사람이 매번 일일이 확인하는 건 비현실적이지만, 항목으로 들어 있다는 사실 자체가 한 번씩 손가락을 멈추게 한다. 한 번 멈추는 것만으로도 폭주성 effect의 절반 이상이 사전에 잡힌다.

넷째, **`useEffectEvent`/카나리 API 도입은 팀 의사결정 사항으로 분리해 두자.** 누군가 한 명이 멋지다고 가져오면, 다른 사람이 똑같이 따라 적기 시작하고, 어느 날 안정 채널 도입 시점에 import 경로가 한꺼번에 깨진다. 도입한다면 "어디까지가 권장 사용 영역인가"를 짧은 문서 한 페이지로 합의하고 가자. 안 도입한다면, ref+effect 패턴을 표준으로 두고 일관성을 유지하자. 어느 쪽이든 "한 코드베이스에 두 개의 표준"이 같이 살아 있는 상황만은 피하는 편이 낫다.

다섯째, **의존성 배열 관련 버그 1건이 잡히면 한 번 회고하자.** 지난 한 달간 우리가 fix한 버그 중 의존성 누락이나 객체 deps로 인한 케이스가 몇 개나 있었는지를 거칠게 세어 보면, 의외로 작지 않은 비율이라는 걸 알게 된다. 한국 커뮤니티에서도 80K LOC 정도의 중간 규모 코드베이스에서 한 달간 잡힌 28개 버그 중 7개가 hooks 의존성 관련이었다는 보고가 돌았다. 이게 우리 팀에도 비슷한 비율로 일어나고 있다면, 그건 lint 규칙이 너무 까다롭다는 신호가 아니라, 우리 코드의 동기화 표현 방식 자체에 손볼 데가 있다는 신호다.

이 다섯 가지를 종합하면, 의존성 배열은 한 줄짜리 대괄호가 아니라 팀의 약속이라는 점이 분명해진다. 정직한 한 사람이 lint와 싸우는 게 아니라, 팀이 함께 정직한 표현 방식을 합의하고 가는 것이다. 그러면 disable 주석은 자연스럽게 줄어들고, 줄어든 만큼 며칠을 잃을 일도 줄어든다.

## 그래서 lint exhaustive-deps는 옳은가 — 짧은 논쟁 정리

마지막으로 한 번 짚고 가자. 이 lint 규칙 자체에 대한 비판이 없는 것은 아니다. davedx 같은 일부 개발자는 "이 규칙은 코딩 표준이 아니라 애플리케이션 버그를 강제한다"고 비판한다. 즉, 아주 좁은 의미의 closure 안전성을 강제하느라 도리어 사용자 입장에선 의도와 다른 동작을 유발한다는 주장이다. 그 입장에 공감 가는 자리도 있다. 실제로 lint를 만족시키려고 의존성을 채우다 보면, "다시 동기화하고 싶지 않은데 어쩔 수 없이 들어가야 하는" 값이 자꾸 끼어들고, 그래서 사용자가 보는 결과가 어색해지는 경우가 있다.

다만 그 갈등의 진짜 원인은 lint가 아니다. 갈등의 진짜 원인은 — 이 장에서 줄곧 이야기한 — **사건과 동기화의 혼선**이다. lint는 정확하게 "이 값을 effect 본문이 읽고 있다"라는 사실을 알려 줄 뿐이고, "다시 동기화할지 말지"는 우리가 코드 구조로 결정해야 하는 일이다. 그 결정 도구가 객체 분해, 함수형 setState, useEffectEvent, ref+effect, 그리고 — 가장 자주 — 핸들러로 자리 옮기기다. lint가 까다롭다고 느껴지는 자리는, 거의 언제나 우리가 결정을 미루고 있던 자리다.

그래서 이 책의 결론은 단순하다. **lint exhaustive-deps는 옳다.** 단, 그 lint를 만족시키려고 코드를 비뚤어지게 적는 건 옳지 않다. lint를 켜 두고, 도구 상자에 있는 다섯 가지 처방으로 정직하게 다시 적자. 정 안 되는 자리에서만 disable 하되 옆에 이유를 적어 두자. 이 정도가 2026년 시점에 가장 균형 잡힌 자세라 본다.

## 자주 만나는 함정 다섯 가지

여기까지 정리한 원칙이 실전에서 어떻게 어그러지는지를, 자주 보는 다섯 가지 함정으로 묶어 두자.

**함정 1. lint disable로 의존성을 가리기.** 가장 흔하면서도 가장 비싼 함정이다. 그날은 시원하지만, 며칠 뒤 stale closure로 돌아온다. lint가 짜증난다면 disable 대신 코드를 다시 적자.

**함정 2. effect 안에서 안 읽는 값을 의존성에 넣기.** "안전하게 다 넣어 두자"라고 생각하기 쉽지만, 이건 안전이 아니라 폭주의 원인이다. effect가 진짜 읽는 값만 적자.

**함정 3. 객체/함수를 그대로 의존성에 넣기.** 매 렌더마다 새 참조라서 effect가 매번 재실행된다. 객체는 원시값으로 분해하고, 함수는 effect 안으로 옮기거나 모듈 스코프로 끌어올리자.

**함정 4. setState 안에 옛 state를 직접 박기.** `setMessages([...messages, m])`처럼 적으면 messages가 의존성에 들어가야 한다. `setMessages(prev => [...prev, m])`로 적으면 messages는 의존성이 아니다. 함수형 업데이트는 의존성 끊기 도구로도 유용하다.

**함정 5. 사건과 동기화를 한 effect에 묶어 두기.** "이 값은 읽긴 하지만 다시 동기화하고 싶지는 않다"는 충돌이 일어나면, 그건 사건을 effect 안에 잘못 둔 신호다. `useEffectEvent`나 ref 패턴으로 사건을 분리하자. 또는 — 그게 정말 사용자 사건이라면 — 핸들러로 옮기자.

다섯 가지 모두 공통점이 있다. 의존성 배열을 거짓말로 메우지 말고, **의존성 배열이 정직하게 짧아지도록 코드를 다시 적자**는 메시지다. 거짓말은 외상이고, 외상은 언젠가 갚는다.

## 핵심 정리

이번 장에서 짚어 두면 좋은 것들을 다시 모아 두자.

1. 의존성 배열은 lint가 정해 주는 게 아니라, **Effect가 본문에서 읽는 reactive value의 진짜 목록**이다.
2. lint를 끄는 일은 React와의 동기화 계약을 일방적으로 어기는 일이다. 거짓말의 대가는 stale closure이고, 그 청구서는 보통 며칠 뒤에 도착한다.
3. 의존성을 줄이고 싶다면 가장 먼저 묻자. **이 effect가 진짜로 그 값을 읽고 있는가?** 안 읽는 값은 의존성이 아니다.
4. 함수가 의존성에 들어와 폭주한다면, 함수를 effect 안으로 옮기거나 모듈 스코프로 끌어올리자. `useCallback`은 마지막 카드다.
5. 객체를 그대로 의존성에 넣지 말고, **원시값으로 분해**해서 의존성에 적자. effect의 동기화 의도가 코드에 또렷이 드러난다.
6. `setState(prev => ...)` 함수형 업데이트는 의존성을 끊는 정직한 도구다. lint 침묵용이 아니라 어휘로 쓰자.
7. **사건과 동기화는 다르다.** Effect 안에서 최신 값을 읽되 재동기화는 원치 않는다면, `useEffectEvent` 또는 ref+effect 패턴으로 분리하자.
8. `useEffectEvent`는 2026년 시점에도 실험 API다. 어휘로는 가치 있지만, lint 침묵용 만능 도구로 쓰면 안 된다.
9. ref+effect 패턴은 안정 채널에서 동일한 효과를 얻는 보수적 대안이다. 단, ref가 imperative escape hatch라는 점을 인정하고 쓰자.
10. **non-reactive value는 의존성에 적지 않는다.** 모듈 스코프 상수, ref, effect event 함수가 그렇다.
11. 사용자 사건은 effect의 일이 아니다. 클릭·제출·키 입력은 핸들러의 자리다. 자리를 잘 잡으면 의존성 배열도 자연스럽게 짧아진다.
12. 의존성 배열의 가장 좋은 모양은, 거짓말이 필요 없을 만큼 코드가 정직해진 모양이다. 짧은 배열은 결과지, 목표가 아니다.

## 한 페이지 체크리스트 — 의존성 배열 검토용

이 장의 내용을 한 장으로 압축한, 코드리뷰 시점에 옆에 두고 쓸 수 있는 체크리스트를 정리해 두자. 자기 PR을 머지하기 전에, 또는 동료의 effect 코드를 검토할 때 한 번씩 이 일곱 줄을 따라가 보자.

1. **의존성 배열에 적힌 항목이 effect 본문에서 정말로 쓰이는가?** — 안 쓰는 값은 빼자. 의도가 명확해진다.
2. **effect 본문에서 읽는 값 중에 의존성 배열에 빠진 게 있는가?** — 있다면 빼지 말고 적자. 빼고 싶다면 코드 구조를 바꿔서 본문에서 안 읽도록 만들자.
3. **객체나 배열이 의존성에 들어 있는가?** — 들어 있다면 원시값으로 분해하거나, 객체 생성을 effect 안으로 들여보내자. props로 받은 객체라면 분해해서 원시값으로 풀자.
4. **함수가 의존성에 들어 있는가?** — effect 전용 헬퍼라면 effect 안으로, props/state 안 읽는 함수라면 모듈 스코프로. useCallback은 prop으로 자식에게 넘길 때만 정당하다.
5. **`setState([...arr, m])` 같은 자리에서 의존성이 늘어났는가?** — `setState(prev => ...)`로 함수형 업데이트로 바꾸면 의존성을 끊을 수 있다.
6. **"읽긴 하지만 다시 동기화하고 싶지 않은 값"이 있는가?** — 사건과 동기화의 혼선이다. `useEffectEvent`(실험) 또는 ref+effect 패턴으로 분리하자. 사용자 사건이라면 핸들러로 옮기자.
7. **`eslint-disable-next-line react-hooks/exhaustive-deps`가 적혀 있는가?** — 이유가 옆에 두 줄로 적혀 있는지 확인하자. 없다면 disable을 풀거나 이유를 적자. disable은 단독으로 머지되면 안 된다.

이 일곱 줄이 한 번씩 통과하면, 그 effect는 거의 정직하다고 봐도 된다. 그 외에 신경 쓸 자리는 race condition cleanup(이미 12장에서 살핀 `let ignore = false` 패턴) 정도이고, 그건 의존성 배열의 영역이라기보다 effect의 cleanup 영역이다. 두 영역을 머릿속에서 깔끔히 분리해 두자.

체크리스트를 한 줄로 줄이면 이렇다. **의존성 배열은 effect 본문이 읽는 reactive value의 진짜 목록이다. 그 목록에 거짓말하지 말고, 거짓말하고 싶어지는 자리에서 코드를 다시 적자.** 이 한 줄이 손가락에 박히면, 13장은 완성이다.

## 연습 문제

### [기초] disable 주석으로 가린 effect 진단하기

다음 코드는 한참 동안 잘 동작하다가, 사용자가 채팅방을 옮기면 옛 방의 메시지가 새 방에 잠깐 끼어드는 버그를 보였다.

```ts
function ChatRoom({ roomId, serverUrl }: { roomId: string; serverUrl: string }) {
  useEffect(() => {
    const conn = createConnection(serverUrl, roomId)
    conn.connect()
    return () => conn.disconnect()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
}
```

(a) 이 코드의 의존성 배열이 거짓말하고 있는 정확한 부분을 적어 보자. (b) disable 주석 없이 동일한 의도를 정직하게 표현하도록 수정해 보자. (c) 만약 "한 번만 연결하고 다시는 재연결하지 말아 달라"가 진짜 요구라면, 이 컴포넌트의 설계 자체에서 무엇을 다시 의심해 봐야 할까?

### [중] 객체 의존성을 원시값으로 분해하기

다음 컴포넌트는 키 입력이 일어날 때마다 채팅 연결이 다시 맺어지는 폭주를 보인다.

```ts
function ChatRoom({ roomId }: { roomId: string }) {
  const options = { serverUrl: 'wss://chat.example', roomId }
  useEffect(() => {
    const conn = createConnection(options)
    conn.connect()
    return () => conn.disconnect()
  }, [options])
}
```

(a) 폭주의 정확한 원인을 한 문장으로 설명해 보자. (b) `options`를 원시값으로 분해해 의존성 배열을 정직하게 만들어 보자. (c) 같은 컴포넌트를 호출하는 부모가 `options` 객체를 prop으로 내려보내는 형태였다면, 어떻게 바꿔 적어야 할까?

### [도전] 채팅 + theme — useEffectEvent로 사건과 동기화 분리하기

다음 요구사항이 주어진다. roomId가 바뀌면 연결을 다시 맺는다. 단, theme이 바뀐다고 해서 연결을 다시 맺어서는 안 된다. theme 변경은 다음 connected 알림에 색만 반영되면 충분하다.

```ts
function ChatRoom({ roomId, theme }: { roomId: string; theme: 'light' | 'dark' }) {
  // 여기에 작성
}
```

(a) `useEffectEvent`(실험 API)를 사용해 위 요구를 정직하게 표현하는 코드를 작성해 보자. (b) 작성 후, 의존성 배열에 적힌 항목과 적히지 않은 항목을 한 줄씩 이유와 함께 설명해 보자. (c) 만약 effect event를 의존성 배열에 적었다면, 어떤 일이 벌어지는가?

### [도전] useEffectEvent 없이 같은 효과 내기 — ref+effect 패턴

같은 요구를 `useEffectEvent` 없이, 안정 채널에서 동작하는 ref+effect 패턴으로 구현해 보자.

```ts
function ChatRoom({ roomId, theme }: { roomId: string; theme: 'light' | 'dark' }) {
  // ref로 latest theme을 보관하는 패턴으로 작성
}
```

(a) `themeRef`를 매 렌더에서 갱신하는 별도 effect와, 채팅 연결을 관리하는 effect를 분리해서 적자. (b) connected 콜백이 호출되는 시점에 `themeRef.current`가 가지는 값이 무엇인지 차근차근 짚어 보자. (c) 이 패턴이 `useEffectEvent`에 비해 어떤 트레이드오프를 가지는지를 두 가지 이상 적어 보자(어휘의 또렷함, 안정 채널 호환성, ref escape hatch의 비용 등).

### [응용·해설] 위 네 문제를 풀고 나면 보이는 공통 패턴

네 문제를 다 풀었다면, 풀이 과정에서 우리가 반복해서 같은 단계를 밟고 있었다는 걸 눈치챘을 것이다. (1) 먼저 effect 본문에서 어떤 reactive value를 읽는지를 손가락으로 따라가며 적어 본다. (2) 그중 객체나 함수가 있으면 원시값으로 분해하거나 안으로 옮긴다. (3) "이건 읽기는 하는데 다시 동기화하고 싶지 않다"는 값이 남으면 사건/동기화 분리를 시도한다. (4) 마지막에 의존성 배열에 적힌 값들을 다시 한 번 훑어, 진짜로 그 값이 바뀌었을 때 effect를 다시 돌리는 게 의도와 맞는지를 확인한다.

이 네 단계가 곧 이 장에서 우리가 들고 갈 휴리스틱이다. 어느 effect를 만나든 이 순서로 점검해 보자. 짧은 effect라면 머릿속에서 한 번에 끝나고, 긴 effect라면 종이 위에 한 번 적어 보면서 풀어도 좋다. 손가락이 disable 주석으로 가기 전에 이 네 단계가 한 번씩만 돌아가도, 거짓말은 거의 들어설 자리를 잃는다.

### [응용] disable 사냥 — 본인 코드베이스에서

본인이 다루고 있는 React 코드베이스에서 `eslint-disable-next-line react-hooks/exhaustive-deps`를 grep으로 모두 찾아 보자. 각각에 대해 다음 표를 채우자.

| 위치 | 가린 의존성 | 가린 이유(추정) | 정직하게 다시 적기 |
|---|---|---|---|

가능한 한 disable 없이 다시 적어 보고, 끝까지 끌 수 없는 한두 사례에 대해서는 "왜 이 케이스만 끌 수밖에 없었는지"를 두세 문장으로 코드 옆에 주석으로 남기자. 미래의 자기 자신이 그 자리를 다시 만났을 때 사흘을 잃지 않도록.

## 자주 받는 질문들

이 장의 내용을 동료들에게 전달하다 보면, 거의 매번 비슷한 질문이 따라온다. 미리 정리해 두자.

**Q1. exhaustive-deps lint를 아예 꺼 놓고 작업하면 안 되나요? 너무 까다롭습니다.**
정중히 권유한다 — 끄지 말자. lint를 끄는 건 closure 안전성 검사 자체를 끄는 일이고, 그 검사 없이 effect를 정직하게 적기란 사람의 손가락만으로는 거의 불가능하다. 까다롭다고 느껴지는 자리에서, 우리가 진짜로 해야 할 일은 lint를 끄는 게 아니라 코드를 lint가 만족할 모양으로 다시 적는 일이다. 이 장의 다섯 가지 처방 중 하나가 거의 언제나 그 자리를 풀어 준다.

**Q2. 의존성에 함수만 들어가도 폭주하던데, useCallback을 어디에나 둘러야 하나요?**
useCallback은 "다른 컴포넌트에 prop으로 함수를 내려보내고, 그쪽이 메모이제이션에 의존할 때" 정도가 정당한 자리다. 같은 컴포넌트 안에서 effect만 호출하는 함수라면, useCallback을 두르는 것보다 함수를 effect 안으로 옮기는 편이 훨씬 깔끔하다. useCallback은 의존성을 한 단계 미루는 도구일 뿐, 의존성을 없애는 도구가 아니라는 점을 기억하자.

**Q3. props로 받은 콜백 함수가 매 렌더마다 새로운데, 의존성에 어떻게 적어야 하나요?**
두 가지 길이 있다. 하나는 부모쪽에서 useCallback으로 그 콜백의 정체성을 안정화시켜 주는 것이다(여기는 정당한 useCallback 자리다). 다른 하나는, 그 콜백이 사실상 사건 함수라면 effect event 또는 ref+effect 패턴으로 의존성에서 빼내는 것이다. 어느 쪽이든 자식에서 disable 주석으로 가리는 건 답이 아니다.

**Q4. interval 안에서 state를 누적해서 갱신해야 하는데, lint가 state도 의존성에 넣으라고 합니다.**
거의 함수형 setState로 풀린다. `setN(prev => prev + 1)`로 적으면 effect 본문이 더 이상 `n`을 직접 읽지 않으므로 의존성에서 빠진다. setInterval/setTimeout 같이 시간차로 동작하는 친구들과 함수형 setState는 거의 단짝이다.

**Q5. 외부 라이브러리가 만들어 준 객체(예: 라이브러리 인스턴스)는 어떻게 다루나요?**
대체로 그 객체는 모듈 스코프 또는 ref에 보관해 reactive하지 않게 만들고, effect 안에서는 그것을 의존성에 적지 않은 채로 호출한다. 이런 자리는 정말로 disable 주석이 필요할 수도 있는 좁은 영역에 해당한다. 단, 그땐 옆에 "왜 이걸 끌 수밖에 없는지"를 두 줄로 적어 두자. 미래의 우리에게 보내는 짧은 편지다.

**Q6. SSR/Next.js 환경에서도 같은 원칙이 통하나요?**
Effect는 클라이언트에서만 실행되므로 SSR 자체의 동작과는 분리된다. 다만 hydration 직후의 첫 effect 실행 시점에 props/state가 어떤 값을 가지고 있는지를 한 번 더 짚어 보는 편이 낫다. 의존성 배열의 정직함은 그대로 통하지만, "첫 마운트에서만 한 번"이라는 가정에 의존하면 hydration mismatch 자리에서 기묘한 풍경을 보게 된다.

**Q7. `useEffectEvent`가 카나리에서 떨어지면 우리 코드가 다 안 돌게 되나요?**
실험 API의 본질이 그렇다. 이름·시그니처·심지어 동작 방식이 안정 채널 도입 전에 바뀔 수 있다. 그래서 이 책에서는 useEffectEvent를 "어휘로는 가치 있다, 단 도입은 팀 의사결정 사항"으로 두자고 권한다. 안정성에 민감한 프로젝트라면 ref+effect 패턴을 표준으로 두고, 카나리는 실험 코드 베이스에서만 시도하는 편이 낫다.

이 일곱 가지 질문에 짧게라도 답할 수 있으면, 의존성 배열에 대한 어휘는 거의 다 갖춘 셈이다. 그리고 짚어 두자 — 이 어휘들을 따로따로 외우는 게 아니라, 이 장에서 함께 본 한 가지 자세, **"의존성 배열에 거짓말하지 않기"** 라는 자세에서 자연스럽게 흘러나오는 것이라는 점이 핵심이다.

## 한 번 더, 어휘를 정렬해 두자

이 장은 작아 보이지만 사용한 어휘가 적지 않다. reactive value, non-reactive value, 동기화 사이클, stale closure, 사건과 동기화, effect event, ref+effect 패턴, 함수형 setState, 원시값 분해, exhaustive-deps. 한 번에 흡수되지 않을 수 있으니, 마지막으로 어휘들을 짧은 한 줄짜리 문장으로 묶어 두자.

- **Reactive value**는 컴포넌트 본체에서 선언된 값(props·state·파생값)이다. effect가 본문에서 읽는다면 의존성에 적어야 한다.
- **Non-reactive value**는 컴포넌트 본체 밖에 사는 값(모듈 상수·ref.current·effect event)이다. 의존성에 적지 않는다.
- **동기화 사이클**은 effect가 자기 의존성에 따라 cleanup-setup을 반복하는 자연 주기다. 컴포넌트의 일생과는 별개다.
- **Stale closure**는 옛 렌더의 지역 변수가 봉인된 함수가 미래에 호출되어 옛 값을 본다는 자바스크립트 클로저 현상의 effect 버전이다. 의존성에 거짓말하면 정확히 이 풍경이 펼쳐진다.
- **사건과 동기화의 분리**는 "값을 읽기는 하지만 그 값에 다시 동기화하고 싶지는 않다"는 갈등을 푸는 어휘다. effect event 또는 ref+effect 패턴이 도구가 된다.
- **함수형 setState**(`setX(prev => ...)`)는 의존성을 끊는 정직한 도구다. lint 침묵용이 아니라 어휘로 쓰자.
- **원시값 분해**는 객체/배열 의존성의 폭주를 막고, effect의 동기화 의도를 코드에 또렷이 적는 도구다.
- **exhaustive-deps**는 closure 안전성의 정적 검사다. 끄지 말고, 만족시키는 방향으로 코드를 다시 적자.

이 어휘 목록을 머리맡에 두고, 다음에 effect 한 덩어리를 적을 때 한 번씩 헤아려 보자. 어떤 자리에서 우리가 어떤 도구를 들고 있는지가 또렷이 보일 것이다. 그러면 의존성 배열의 그 작은 대괄호 한 쌍이, 더 이상 짜증의 자리가 아니라 우리 의도를 비추는 거울이 된다.

## 한 줄짜리 메모 — 동료에게 전달하기

이 장의 내용을 동료에게 한두 줄로 전달해야 한다면, 다음 메모를 그대로 쓰자.

> 의존성 배열은 lint가 정해 주는 게 아니라, **이 effect가 본문에서 읽는 reactive value의 진짜 목록**이다. 거짓말로 메우지 말고, 거짓말이 필요 없도록 코드를 다시 적자. 객체는 분해하고, 함수는 안으로 옮기고, 사건은 핸들러로 빼고, 진짜 사건/동기화 충돌이라면 effect event 또는 ref+effect로 분리한다. lint를 끄는 자리에는 옆에 두 줄짜리 이유를 남기자 — 미래의 우리에게 보내는 짧은 편지다.

이 메모 한 장이 슬랙 채널에 한 번 공유되어 돌면, 의존성 배열로 인한 디버깅 시간이 팀 단위로 줄어든다. 그게 13장의 가장 작은, 그러나 가장 큰 효용이다.

## 마무리 — 다음 장으로의 다리

여기까지 따라오면, 손가락이 자연스럽게 disable 주석으로 향하던 그 짜증의 자리에서, 한 박자만 더 멈추는 습관이 생겼을 것이다. **"이 의존성 정말로 effect가 읽고 있나?"** 한 번 묻고, **"객체/함수가 끼어 있다면 분해하거나 안으로 옮길 수 있나?"** 한 번 더 묻고, 마지막으로 **"이건 동기화가 아니라 사건 아닌가?"** 라고 한 번 더 물어 본다. 이 세 번의 질문을 거치면 의존성 배열은 거의 언제나 정직한 모양으로 짧아진다. 거짓말이 필요해지는 순간은 이제 거의 남지 않는다.

그런데 여기까지 와서 다시 둘러보면, 같은 effect+state 패턴이 여러 컴포넌트에 비슷하게 반복되고 있다는 걸 발견하게 된다. 채팅방마다 연결을 관리하는 effect를 똑같이 적고, 폼마다 입력값과 onChange 짝을 똑같이 적고, 디바운스·온라인 상태·딜레이드 값 같은 것들도 비슷한 모양으로 두 번, 세 번 반복된다. 이쯤 되면 이런 의문이 든다. 이걸 어떻게 한 곳에 묶어 둘 수 있을까? 한 번 쓰고 다른 곳에서도 가져다 쓸 수 있도록 추출하려면 어떻게 해야 할까?

그게 바로 다음 장의 주제다. 14장에서는 **커스텀 훅**으로 가 보자. "두 번 이상 같은 패턴이 보이면 추출한다"는 기준이 어떻게 작동하는지, `use` 접두사가 왜 의미 있는 표지인지, 그리고 — 어쩌면 이게 가장 중요한데 — 커스텀 훅이 **공유하는 것은 로직이지 상태가 아니다**라는 묘한 설계 원칙이 어떻게 흘러가는지를 함께 살펴보자. 정직하게 적힌 effect들을 어떻게 정직하게 묶어 둘 것인가의 이야기다.
