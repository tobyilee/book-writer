# 2장. 무엇을 state에 두고, 무엇을 두지 말 것인가

다음과 같은 상황을 상상해보자. 신입사원 시절에 짠 작은 회원가입 폼이 있다. 처음에는 입력란 두 개에 버튼 하나, 단출했다. 그러던 것이 1년이 지나니 입력란이 일곱 개로 불고, 옆에는 미리보기 영역이 붙고, "전송 중"을 알리는 스피너와 "전송 완료" 토스트가 추가된다. 새 동료가 합류하고 코드를 열어보더니 한 마디 한다. "어, 이 컴포넌트 `useState`가 열한 개나 되네요?" 슬쩍 보면 그렇게 많은가 싶다가도, 세어 보면 정말로 그렇다. `firstName`, `lastName`, `fullName`, `isSending`, `isSent`, `error`, `selectedPlan`, `selectedPlanName`, `selectedPlanPrice`, `agreed`, `validationMessage`. 화면 한 칸에 변수 열한 개라니, 이 정도면 컴포넌트가 비대하다고 느낄 만하다.

찜찜한 점은 단지 개수만이 아니다. 어디선가 한 번씩 `firstName`은 바꿨는데 `fullName`이 그대로라는 버그가 떠다닌다. "전송 중인데 동시에 전송 완료라고 표시되는 잠깐의 깜빡임"을 본 사람도 있다. 선택된 요금제를 바꿨는데 옆 패널의 가격은 한 박자 늦게 갱신된다. 모두 다 따로따로 보면 사소한 결함이다. 하지만 한 데 모아 놓고 보면 한 가지 공통점이 있다. **같은 진실을 두 군데에 기록해 두었기 때문**에 둘이 어긋나는 순간이 생긴다는 것이다.

그렇다면 어떻게 해야 할까? 1장에서 우리는 "상태를 다섯 단계로 모델링하자"는 큰 그림을 그렸다. 그중 두 번째 단계는 **"그 상태들 가운데 본질이 아닌 것을 솎아내라"**였다. 본 장은 바로 이 단계를 깊게 풀어 본다. 어떤 값이 진짜 state여야 하고, 어떤 값은 그저 렌더 도중에 계산되어야 하는지. 어떤 boolean들이 합쳐져서 하나의 enum이 되어야 하는지. 어떤 객체는 통째로 보관할 게 아니라 ID 하나로만 기억해야 하는지. 이 한 장만 넘기고 나도 컴포넌트의 `useState` 개수가 절반 이하로 줄어들고, 그만큼 동기화 버그도 함께 사라지게 된다.

여기서 한 가지 마음을 잡고 가자. 본 장이 다루는 주제는 거창한 새로운 API가 아니다. `useState`라는 가장 기본적인 도구를 두고, **무엇을 그 안에 넣고 무엇을 빼야 하는가**를 따지는 작업이다. 새 도구를 배우는 일보다 기존 도구의 사용 방식을 다듬는 일이다. 그래서 처음 보면 "별 거 아닌데?" 싶어 보인다. 하지만 막상 자기 코드에 적용해 보면 손이 자주 멈춘다. 익숙한 패턴을 한 번씩 바꿔 짜야 하기 때문이다. 그 작업이 어색하더라도, 한 번 두 번 거치면서 손에 붙는다. 그러니 본 장은 **읽기보다 손으로 따라 짜야** 효과가 보이는 장이다. 각 절의 코드를 직접 에디터에 옮겨 보고, 절 끝의 연습 문제를 풀어 보자. 그래야 원칙이 살로 붙는다.

또 한 가지, 본 장의 패턴들은 React에 특별히 묶인 것이 아니다. **함수형 사고**의 일반적인 결론이다. "출력은 입력의 함수다", "같은 입력에는 같은 출력이 나와야 한다", "상태가 적을수록 추론이 쉽다"라는 명제들은 React 이전부터 있어 왔다. React가 한 일은 그 사고를 UI 영역으로 끌어와 컴포넌트라는 단위에 적용한 것뿐이다. 그러니 본 장의 원칙들은 다른 라이브러리·다른 언어에서도 그대로 통한다. Vue에서도, Svelte에서도, Solid에서도, Elm에서도, 심지어 백엔드 도메인 모델 설계에서도 같은 원칙이 작동한다. 그만큼 보편적인 토대다.

## 2.1 진실은 한 군데, Single Source of Truth

먼저 한 가지 원칙부터 단단히 박아 두자. **같은 진실은 두 군데에 두지 말자.** React 공식 문서가 "Single Source of Truth"라고 부르는 그 원칙이다. 말은 거창하지만 현실적인 의미는 단순하다. 어떤 정보 하나가 두 변수에 동시에 저장되어 있다면, 둘이 같다는 보장을 우리가 직접 코드로 강제해야 한다. 그리고 이 강제는 거의 매번 어긋난다. 잊고, 빠뜨리고, 비동기 사이에 끼어든 한 박자에 어그러진다.

그러니 이렇게 자문해보는 습관을 들이자.

- 이 값은 다른 state로부터 **계산할 수 있는가?** 그렇다면 그것은 state가 아니라 **파생값**이다.
- 이 값은 props로 들어오는가? 그렇다면 별도의 state로 복사해 둘 이유가 거의 없다.
- 두 boolean이 동시에 true가 되면 **불가능한 상태**가 되는가? 그렇다면 둘은 본래 하나의 enum이었어야 한다.
- 이 객체 자체가 바뀌었을 때 그 객체를 가리키던 다른 변수도 같이 바뀌어야 하는가? 그렇다면 객체 통째로가 아니라 **ID로** 보관해야 한다.

이 네 가지 질문은 본 장 내내 우리를 따라다닌다. 차례차례 풀어보자.

여기서 한 가지 일러둘 점이 있다. "Single Source of Truth"라는 말은 데이터베이스 세계에서 건너온 어휘다. 한 정보의 출처를 한 군데로 못 박지 않으면 어디는 갱신되고 어디는 안 되어 데이터가 어긋난다는, 정통 RDB 설계의 오래된 교훈이다. React가 이 말을 빌려 온 이유도 같다. 컴포넌트 트리 하나도 작은 데이터베이스다. 어떤 사실 하나를 두 컴포넌트가 동시에 들고 있고 둘 다 그것을 직접 갱신할 수 있다면, 그 둘은 머지않아 어긋난다. 그래서 React 공식 가이드도 "동기화되어야 할 두 state가 보이거든 하나로 합치거나, 한쪽을 다른 쪽으로부터 계산하도록 바꾸라"고 분명히 말한다.

그렇다면 우리는 평소에 어떤 신호를 보고 "지금 진실이 두 군데에 있다"고 알아챌 수 있을까? 경험적으로 자주 나타나는 신호가 몇 있다. 첫째, 한 이벤트 핸들러 안에서 `setA`와 `setB`를 **항상 함께** 호출하고 있다면, 둘은 사실 한 정보의 두 얼굴일 가능성이 높다. 둘째, 코드 리뷰에서 "여기 setX도 같이 호출해줘야 합니다"라는 코멘트가 자주 달린다면, 그것 역시 같은 신호다. 셋째, 디버깅 중에 "어, 이건 왜 이거랑 안 맞지?"라는 말이 한 번이라도 나왔다면, 거의 확실히 어딘가에 진실이 두 벌로 살고 있다. 이 신호들을 만나면 일단 멈추고, 어느 한쪽이 다른 한쪽으로부터 계산될 수는 없는지부터 따져 보자.

## 2.2 fullName 사례 — 파생값을 state로 두면 벌어지는 일

가장 흔한 실수부터 살펴보자. 회원 정보 입력 폼인데 `firstName`, `lastName`, `fullName`을 모두 state로 들고 있는 경우다. 어디선가 본 적이 있을 만한, 그러면서도 처음 작성할 때는 별 고민 없이 짜게 되는 패턴이다.

```tsx
// 안티패턴: 파생 가능한 값을 state로 보관한다
import { useState } from 'react';

function ProfileForm() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  // 의도: firstName + ' ' + lastName 을 캐싱
  // 실제: firstName 과 lastName 의 모든 변경 지점에서 같이 갱신해줘야 한다
  const [fullName, setFullName] = useState('');

  return (
    <form>
      <input
        value={firstName}
        onChange={(e) => {
          setFirstName(e.target.value);
          setFullName(e.target.value + ' ' + lastName); // 잊으면 끝
        }}
      />
      <input
        value={lastName}
        onChange={(e) => {
          setLastName(e.target.value);
          setFullName(firstName + ' ' + e.target.value); // 여기서도 잊으면 끝
        }}
      />
      <p>전체 이름: {fullName}</p>
    </form>
  );
}
```

이 코드의 문제점은 무엇일까? 표면적으로는 잘 동작하는 것처럼 보인다. 실제로 입력란에 글자를 치면 아래쪽 `<p>`에 전체 이름이 갱신된다. 하지만 한번 생각해보자. 만약 어떤 동료가 "외부 API에서 firstName만 받아와서 채우는 자동 완성 기능"을 추가한다면? 그 동료가 `setFirstName(...)`만 부르고 `setFullName(...)`은 잊는다면? 한 박자 동안 이름이 어긋난 채로 화면에 남는다.

게다가 `fullName`을 별도로 들고 있는다는 것은 미묘한 뉘앙스를 풍긴다. 마치 그것이 독립적으로 변할 수 있는 값인 것처럼 코드에 보인다. 하지만 우리의 의도는 그렇지 않았다. `fullName`은 그저 `firstName + ' ' + lastName`이었을 뿐이다. **계산식이 변수의 자리를 차지하고 있다.** 끔찍한 일이다.

해법은 단순하다. 그냥 변수로 빼자.

```tsx
// 권장: 파생값은 렌더 중에 그냥 계산한다
import { useState } from 'react';

function ProfileForm() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  // state가 아니다. 그냥 매 렌더마다 계산되는 지역 변수일 뿐이다.
  const fullName = firstName + ' ' + lastName;

  return (
    <form>
      <input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
      <input value={lastName} onChange={(e) => setLastName(e.target.value)} />
      <p>전체 이름: {fullName}</p>
    </form>
  );
}
```

`useState`가 셋에서 둘로 줄었다. `setFullName` 호출도 사라졌다. 그리고 무엇보다, **두 이름이 어긋날 가능성 자체가 코드에서 사라졌다.** `fullName`은 매 렌더 시점에 두 state로부터 즉석에서 계산된다. `firstName`이 바뀌면 컴포넌트가 다시 렌더되고, 그 렌더 안에서 `fullName`도 자동으로 새로 계산된다. 동기화 따위는 신경 쓸 필요가 없다. 동기화가 일어날 두 변수가 애초에 한쪽으로 줄어들었기 때문이다.

여기서 한 가지 마음의 짐을 내려놓자. "렌더할 때마다 문자열을 더하는데 비싸지 않을까?" 하는 걱정 말이다. 결론부터 말하면, 거의 모든 경우에 비싸지 않다. 문자열 두 개를 잇는 일은 한 마이크로초도 들지 않는다. React가 그 컴포넌트를 다시 렌더하기로 결정한 시점이라는 것은 이미 가상 DOM 비교, JSX 평가, 자식 컴포넌트 렌더가 죄다 일어난다는 뜻이다. 그 모든 비용에 비하면 문자열 한 줄 더하는 것은 반올림 오차다. **"파생값을 state로 캐싱하면 빠르겠지"라는 직관은 거의 항상 틀리다.** 오히려 그 캐싱을 유지하느라 추가 `setState`가 발생해 렌더가 한 번 더 일어난다.

그러니 기본 자세를 이렇게 잡자. **파생 가능한 값은 렌더 중에 계산한다.** 그것이 진짜로 비싸다는 증거가 측정으로 확보되었을 때만, 그때서야 캐싱을 고민한다.

여기서 한 가지 미묘한 함정도 같이 짚어두자. "fullName을 state로 보관해야만 외부에서 그 값을 쓸 수 있는 것 아닌가?" 하는 의문이 종종 따라온다. 결론부터 말하면 그렇지 않다. fullName이 필요한 자식 컴포넌트가 있다면 prop으로 그냥 내려주면 된다. 부모에서 `<Greeting fullName={fullName} />`라고 적는 데에 따로 state가 필요하지 않다. 변수는 어디까지나 그 컴포넌트 함수 본체 안의 지역 변수이고, JSX는 그 변수를 참조해 자식에게 내려보낼 뿐이다. 새 props가 내려가면 자식은 자동으로 새 값으로 다시 렌더된다. 흐름이 그대로 유지된다.

또 하나 자주 나오는 질문은 "그러면 useEffect로 fullName을 계산해서 setState하면 안 되는가?"이다. 이건 다음 절에서 다시 다루지만, 미리 한 줄만 답해 두자. **안 된다.** 그것은 위 안티패턴을 더 멀리 돌아가는 길로 다시 걷는 일이다. 한 박자 늦게 갱신되고, 렌더가 한 번 더 일어나며, 그 사이의 빈 화면이 깜빡인다. 끔찍한 일이다.

마지막으로 한 가지 사고 실험을 해 보자. 만약 이 폼에 "fullName이 한 번 채워지면 더 이상 firstName이나 lastName이 바뀌어도 fullName은 잠시 고정한다" 같은 요구가 들어오면 어떻게 될까? 예를 들어 사용자가 한 번 "확정" 버튼을 누른 뒤로는 두 입력란이 자유롭게 바뀌어도 화면에는 확정된 fullName이 그대로 남아 있어야 하는 화면이다. 이 경우엔 fullName이 더 이상 단순 파생값이 아니다. 어느 시점에 **고정된 스냅샷**이고, 그 시점의 의도가 분명하다. 이때는 정말로 별도의 state로 두는 편이 낫다. 다만 그 변수 이름은 `fullName`이 아니라 `confirmedFullName` 같은 식으로 의도를 분명히 드러내는 편이 좋다. **state로 둘 가치가 있는 값은, 다른 값에서 자동으로 계산될 수 없는 별도의 진실을 가진 값**이다. 위 시나리오에서 `confirmedFullName`은 그 시점에 사용자가 "확정했다"는 사실 자체를 표현한다. 단순히 firstName + lastName이 아니라, "사용자가 어느 순간에 본 화면이 무엇이었는가"라는 별도의 진실이다. 그러면 state로 둘 만하다. 이런 식으로 한 변수가 state여야 하는지 아닌지를 가르는 잣대는 결국 "이 값에 별도의 진실이 들어 있는가?"라는 한 가지 질문이다.

## 2.3 useMemo는 언제 필요한가

물론 세상엔 진짜로 비싼 계산도 있다. 만 개짜리 배열을 정렬한다거나, 큰 텍스트 문서에서 마크다운을 파싱한다거나, 복잡한 차트 데이터의 누적합을 구한다거나. 이런 계산까지 매 렌더마다 다시 돌리면 손에 잡힐 만큼 느려진다. 이때 등장하는 것이 `useMemo`다.

```tsx
// 비싼 계산을 캐싱한다 — 다만 정말로 비쌀 때만
import { useMemo, useState } from 'react';

type Item = { id: number; name: string; price: number };

function ExpensiveList({ items, query }: { items: Item[]; query: string }) {
  // items나 query가 바뀌지 않는 한 결과를 재사용한다.
  const filtered = useMemo(() => {
    return items
      .filter((item) => item.name.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => a.price - b.price);
  }, [items, query]);

  return (
    <ul>
      {filtered.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

`useMemo`의 본질은 단순하다. 의존성 배열의 값이 바뀌지 않았으면 이전에 계산해둔 결과를 그대로 쓴다. 그것뿐이다. 그렇다면 모든 파생값에 일단 `useMemo`를 둘러두면 안 될까? 그건 또 그렇지 않다. `useMemo` 자체에도 비용이 있다. 의존성 배열을 비교하고, 캐시를 들고 있고, 메모리를 쓴다. **싼 계산을 `useMemo`로 둘러싸는 것은 손해**다. 캐싱이 이득이 되려면 계산이 캐시 비교 비용보다 명백히 비싸야 한다.

그래서 React 공식 가이드도 권하는 순서가 있다. 먼저 **그냥 변수로** 짠다. 측정해서 느리면 `useMemo`로 감싼다. 미리 두를 필요는 없다. 심지어 React 19부터는 React Compiler가 자동으로 메모이제이션을 처리해 주는 방향으로 가고 있어, 우리가 `useMemo`를 직접 쓸 일이 점점 줄어든다. 그러니 **기본은 그냥 변수, 예외가 useMemo**라고 기억해두자.

그리고 한 가지 더. Effect 안에서 비싼 계산을 하고 그 결과를 다시 state에 넣는 패턴은 거의 항상 잘못된 길이다.

```tsx
// 안티패턴: effect로 파생값을 계산해서 state에 넣는다
function BadExpensiveList({ items, query }: { items: Item[]; query: string }) {
  const [filtered, setFiltered] = useState<Item[]>([]);

  useEffect(() => {
    // 1. items나 query가 바뀌면 effect가 돌고
    // 2. setFiltered가 호출되어 다시 렌더가 일어나고
    // 3. 그제서야 화면이 갱신된다
    setFiltered(items.filter((i) => i.name.includes(query)));
  }, [items, query]);

  return <ul>{filtered.map((i) => <li key={i.id}>{i.name}</li>)}</ul>;
}
```

이 코드는 모든 변경에 **렌더를 두 번** 일으킨다. 처음에는 빈 결과로, 그다음에 effect가 돌아 setState를 부른 뒤에 진짜 결과로. 게다가 첫 렌더 동안 빈 화면이 잠깐 깜빡인다. 끔찍한 일이다. 가운데 단계가 사라지면 끝나는 일이다. **render phase에서 그냥 계산하자. 정말로 비싸면 useMemo로 감싸자. effect에 넣지 말자.** Dan Abramov가 메타 내부 코드베이스에서 샘플링한 결과 약 46%의 useEffect가 불필요했다는 이야기도, 절반 가까이가 바로 이런 종류의 오용이었다는 신호다.

조금 더 솔직히 말하면, 한국 개발 커뮤니티의 useEffect 무한루프 사연 절반이 위와 같은 모양에서 시작된다. effect로 파생값을 만들고, 그 파생값을 또 다른 effect의 의존성에 넣고, 그 결과로 또 setState를 부른다. cascading한 effect의 사슬이 만들어진다. 이쯤 되면 코드를 읽는 사람이 "지금 어떤 setState 다음에 어떤 effect가 도는 건지" 한참 따라가야 한다. 디버깅 지옥이다. 그러니 진실 한 가지를 본 장의 슬로건처럼 외워두자. **계산 가능한 값은 effect로 동기화하지 않는다. 렌더 중에 계산한다.** 이 한 문장만 지켜도 useEffect의 절반이 사라진다.

그리고 한 가지 더, "비싼 계산"이라는 말을 너무 쉽게 쓰지는 말자. 우리 직관은 "이건 비쌀 것 같다"라고 자주 속삭이지만, 실제로 측정해 보면 평범한 노트북에서 1만 개짜리 배열의 filter+sort가 1ms 안쪽이다. 사람의 눈이 인지하는 한계는 보통 16ms — 한 프레임이다. 그 안쪽이라면 캐싱은 사치다. 측정도구는 멀리 있지 않다. Chrome DevTools의 Performance 탭, 또는 React DevTools의 Profiler 탭만 켜도 어느 컴포넌트가 몇 ms 걸리는지 한눈에 보인다. **추측 대신 측정**, 이 한 가지 자세만 익혀도 불필요한 useMemo가 코드에서 쑥쑥 빠진다.

## 2.4 모순 가능한 boolean 두 개 — status enum의 등장

이번엔 다른 종류의 부풀어 오름을 보자. 폼 전송 로직을 짜다 보면 자연스럽게 다음과 같은 코드가 나온다.

```tsx
// 안티패턴: boolean 두 개로 상태를 분할 표시한다
import { useState } from 'react';

function FeedbackForm() {
  const [text, setText] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [isSent, setIsSent] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsSending(true);
    await sendMessage(text);
    setIsSending(false);
    setIsSent(true);
  }

  if (isSent) return <p>고마워요!</p>;
  return (
    <form onSubmit={handleSubmit}>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button type="submit" disabled={isSending}>
        {isSending ? '보내는 중...' : '보내기'}
      </button>
    </form>
  );
}

async function sendMessage(text: string): Promise<void> {
  // 데모용 가짜 전송
  return new Promise((resolve) => setTimeout(resolve, 1000));
}
```

표면적으로는 동작한다. 그런데 가만 보면 어딘가 찜찜하다. `isSending`과 `isSent`라는 두 boolean이 표현할 수 있는 조합은 모두 네 가지다.

| isSending | isSent | 의미 |
|---|---|---|
| false | false | 입력 중 |
| true | false | 전송 중 |
| false | true | 전송 완료 |
| **true** | **true** | **????** |

마지막 줄을 보자. 둘 다 true인 상태가 있다. 보내는 중인 동시에 보냈다는 상태? 우리의 도메인엔 그런 상태가 없다. 그런데 코드의 모양은 그 상태를 **표현 가능하게 허용한다.** 누군가 실수로 `setIsSending(true)`만 부르고 `setIsSent(false)`로 되돌리지 않으면, 또는 비동기 사이에 어디선가 두 setState 사이에 다른 분기가 끼어들면, 화면이 잠깐 그 불가능한 상태를 그릴 수 있다. 가능성이 0이 아니라는 점이 중요하다.

이런 패턴이 나올 때마다 자문해보자. **"이 두 boolean을 한 변수로 합칠 수 있지 않을까?"** 대개의 답은 "그렇다"이다. 위 폼은 사실 한 시점에 다음 셋 중 정확히 하나의 상태에 있다.

- `'typing'` — 입력 중
- `'sending'` — 전송 중
- `'sent'` — 전송 완료

그렇다면 변수는 하나여야 한다. 합쳐 보자.

```tsx
// 권장: status enum 한 변수로 합친다
import { useState } from 'react';

type Status = 'typing' | 'sending' | 'sent';

function FeedbackForm() {
  const [text, setText] = useState('');
  const [status, setStatus] = useState<Status>('typing');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('sending');
    await sendMessage(text);
    setStatus('sent');
  }

  if (status === 'sent') return <p>고마워요!</p>;

  // 파생값들 — 렌더 중에 계산한다
  const isSending = status === 'sending';

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={isSending}
      />
      <button type="submit" disabled={isSending}>
        {isSending ? '보내는 중...' : '보내기'}
      </button>
    </form>
  );
}

async function sendMessage(text: string): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, 1000));
}
```

무엇이 좋아졌는가? 우선 **불가능한 상태가 코드에서 표현 불가능해졌다.** `Status` 타입은 세 값 중 하나일 뿐이다. `isSending && isSent`처럼 두 boolean이 동시에 true인 상태는 존재할 수 없다. 둘째, 변경 지점이 명확해졌다. 한 변수에 한 번씩만 setState하면 된다. 셋째, **`isSending`은 다시 파생값**이 되었다. 별도의 state가 아니다. status로부터 매 렌더마다 계산된다.

여기서 잠깐 뉘앙스를 짚어두자. boolean 둘이 모이면 무조건 enum으로 합쳐야 하는가? 그건 아니다. 두 boolean이 **진짜로 독립적**이라면 — 예를 들어 "관리자 권한 여부"와 "이메일 인증 여부"처럼 — 각자 둬도 된다. 합쳐야 할 때는 두 boolean이 **상호 배타적이거나, 정해진 순서로만 변하거나, 동시에 true가 되는 조합이 의미 없을 때**다. 그 조건에 들어맞으면 거의 예외 없이 enum 한 변수로 합치는 편이 낫다. 합치고 나면 자연스럽게 "이 상태에서는 어떤 동작이 가능한가"라는 질문도 또렷해진다. 상태 머신으로 가는 길의 첫걸음이다.

조금 더 욕심을 내 보자. 위 폼은 `'typing' | 'sending' | 'sent'` 셋이었지만, 실제 서비스에서는 한 가지가 더 자주 끼어든다. 바로 **`'error'`** 상태다. 네트워크가 끊겼거나, 서버가 4xx/5xx로 답했거나, 입력값 자체가 거절되었을 때다. 그래서 실무에서는 다음과 같이 한 칸 더 넓힌 enum을 흔히 본다.

```tsx
type Status = 'typing' | 'sending' | 'sent' | 'error';

function FeedbackForm() {
  const [text, setText] = useState('');
  const [status, setStatus] = useState<Status>('typing');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('sending');
    setErrorMessage(null);
    try {
      await sendMessage(text);
      setStatus('sent');
    } catch (err) {
      // 실패하면 다시 typing으로 돌려서 재시도를 허용하거나, error 상태로 못 박는다.
      setStatus('error');
      setErrorMessage(err instanceof Error ? err.message : '알 수 없는 오류');
    }
  }

  // 화면도 status에 따라 분기한다 — 분기의 가짓수가 명확하다.
  if (status === 'sent') return <p>고마워요!</p>;

  const isSending = status === 'sending';

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={isSending}
      />
      <button type="submit" disabled={isSending || text.length === 0}>
        {isSending ? '보내는 중...' : '보내기'}
      </button>
      {status === 'error' && errorMessage && (
        <p role="alert">전송 실패: {errorMessage}</p>
      )}
    </form>
  );
}
```

이 코드를 보면서 한 가지 더 익혀두자. **discriminated union을 쓸 수 있다면 더 좋다.** 위에서는 `errorMessage`를 별도 state로 두었지만, 사실 `errorMessage`는 `status === 'error'`일 때만 의미가 있다. 그렇다면 두 정보를 한 객체로 묶고, status에 따라 객체의 모양 자체가 달라지도록 타입을 구성할 수 있다.

```tsx
type FormState =
  | { kind: 'typing' }
  | { kind: 'sending' }
  | { kind: 'sent' }
  | { kind: 'error'; message: string };
```

이렇게 짜면 TypeScript가 강제해 준다. `state.kind === 'error'`인 분기 안에서만 `state.message`에 접근 가능하다. 다른 분기에서 실수로 `state.message`를 쓰면 컴파일러가 거부한다. **불가능한 상태를 코드 모양 자체에서 표현 불가능하게** 만드는 셈이다. 이쯤 되면 단순한 컨벤션이 아니라 작은 타입 시스템 설계의 시작이다. Elm이 강조하던 "make impossible states impossible"이라는 격언은 React + TypeScript 세계에서도 그대로 살아 있다.

그렇다면 이 enum 방식은 언제 한계를 만나는가? 상태가 일고여덟 개를 넘기 시작하고, 상태 사이의 전이가 그래프처럼 복잡해질 때다. 그쯤 되면 한 변수에 한 enum으로 다 적기는 버겁다. XState 같은 상태 머신 라이브러리, 또는 useReducer로 이행하는 편이 낫다. 다만 그 이야기는 4장에서 본격적으로 다룬다. 본 장에서는 이 한 마디만 마음에 두자. **두 개의 boolean이 보이거든, 그 둘이 사실 하나의 enum이 아니었나 의심하라.**

## 2.5 선택된 객체를 state로 두면 stale 참조가 생긴다

조금 더 까다로운 사례를 보자. 상품 목록과 그중에서 선택된 상품을 함께 보여주는 화면이다. 흔한 첫 시도는 다음과 같다.

```tsx
// 안티패턴: 선택된 객체를 통째로 state에 저장
import { useState } from 'react';

type Product = { id: number; name: string; price: number };

const initialProducts: Product[] = [
  { id: 1, name: '아메리카노', price: 4500 },
  { id: 2, name: '라떼', price: 5000 },
  { id: 3, name: '에스프레소', price: 4000 },
];

function ProductPage() {
  const [products, setProducts] = useState<Product[]>(initialProducts);
  // 객체 자체를 들고 있는다 — 함정의 시작
  const [selected, setSelected] = useState<Product | null>(initialProducts[0]);

  function increasePrice(id: number) {
    setProducts((prev) =>
      prev.map((p) => (p.id === id ? { ...p, price: p.price + 500 } : p))
    );
    // selected는? 가만히 있다.
    // 방금 가격 올린 그 상품이 selected였다면, 화면에 옛 가격이 남는다.
  }

  return (
    <div>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <button onClick={() => setSelected(p)}>{p.name}</button>
            <button onClick={() => increasePrice(p.id)}>가격 +500</button>
          </li>
        ))}
      </ul>
      {selected && (
        <section>
          <h2>{selected.name}</h2>
          <p>{selected.price}원</p>
        </section>
      )}
    </div>
  );
}
```

이 코드의 어디가 문제인가? `selected`에는 어느 시점에 클릭한 상품 **객체의 사본**이 들어가 있다. 그리고 우리는 `products` 배열을 갱신할 때 새 객체를 만든다(불변성 원칙대로). 그러면 `selected`가 가리키는 객체는 갱신된 배열 안의 객체와 더 이상 같은 참조가 아니다. 가격이 4500원에서 5000원으로 바뀌었어도 `selected.price`는 여전히 4500원이다. 한 번 사진을 찍어 둔 것이기 때문이다. **stale 참조**다.

해법은 명확하다. **객체가 아니라 ID로 들고 있자.** 진짜 데이터는 `products` 한 군데에만 두고, "지금 선택된 것이 누구인가"는 ID로만 표시한다. 화면을 그릴 땐 그 ID로 배열에서 찾는다.

```tsx
// 권장: ID로 보관하고 렌더 시 lookup
import { useState } from 'react';

type Product = { id: number; name: string; price: number };

const initialProducts: Product[] = [
  { id: 1, name: '아메리카노', price: 4500 },
  { id: 2, name: '라떼', price: 5000 },
  { id: 3, name: '에스프레소', price: 4000 },
];

function ProductPage() {
  const [products, setProducts] = useState<Product[]>(initialProducts);
  // ID만 보관한다. 선택된 상품의 실제 데이터는 products 한 군데에만 산다.
  const [selectedId, setSelectedId] = useState<number | null>(1);

  // 매 렌더마다 새로 찾는다. 진짜 진실은 products 안에 있다.
  const selected = products.find((p) => p.id === selectedId) ?? null;

  function increasePrice(id: number) {
    setProducts((prev) =>
      prev.map((p) => (p.id === id ? { ...p, price: p.price + 500 } : p))
    );
    // selected는 따로 갱신할 필요가 없다. find가 다음 렌더에서 새 객체를 집어 온다.
  }

  return (
    <div>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <button onClick={() => setSelectedId(p.id)}>{p.name}</button>
            <button onClick={() => increasePrice(p.id)}>가격 +500</button>
          </li>
        ))}
      </ul>
      {selected && (
        <section>
          <h2>{selected.name}</h2>
          <p>{selected.price}원</p>
        </section>
      )}
    </div>
  );
}
```

다시 한번 핵심 원칙으로 돌아오자. **같은 진실을 두 군데 두지 말자.** 상품 데이터의 진실은 `products` 배열 한 군데에 있다. "지금 선택된 것이 누구인가"는 그 진실로부터 가리키는 **포인터**일 뿐이다. 포인터는 객체 사본이 아니라 ID여야 한다. 그래야 원본이 바뀌었을 때 자동으로 따라간다.

배열의 인덱스를 쓰는 변형도 가능하다. 다만 인덱스는 항목 순서가 바뀌면 가리키는 대상이 달라지므로, 정렬·필터·추가·삭제가 일어나는 리스트라면 ID가 더 안전하다. 인덱스는 정말로 "위치 자체"가 의미일 때만 쓰자. 예를 들어 "다섯 번째 슬라이드"는 인덱스가 자연스럽지만, "장바구니에서 선택된 상품"은 ID가 자연스럽다.

조금 더 일반화해 보자. **state에는 가능한 한 작은 단위의 식별자만 두자.** 진짜 데이터는 한 군데에 모아 두고, 그 데이터를 가리키는 손가락만 state로 분산시키는 모양이다. 이 원칙이 효력을 발휘하는 장면은 의외로 많다. 채팅 앱에서 "현재 열려 있는 대화방"은 `Room` 객체가 아니라 `roomId: string`이다. 칸반 보드에서 "지금 드래그 중인 카드"는 `Card` 객체가 아니라 `draggingCardId: string`이다. 폼 마법사에서 "지금 보고 있는 단계"는 한 객체가 아니라 `currentStepId: 'profile' | 'address' | 'review'`다. 화면이 그릴 때마다 식별자로 진짜 객체를 찾아서 쓴다. 진짜 객체의 모양이 변하면 다음 렌더에 자동으로 따라간다.

여기서 자주 따라오는 걱정 한 가지를 미리 풀어두자. "매 렌더마다 `find`를 부르는데 느리지 않을까?" 결론은, 거의 항상 충분히 빠르다. 100~1000개짜리 배열에서 `find`는 마이크로초 단위에서 끝난다. 정말로 큰 컬렉션 — 1만 개 이상 — 이고 그 안에서 한 항목을 찾는 빈도가 매우 높다면, ID를 키로 하는 `Map<id, item>`을 동시에 들고 가는 방식으로 한 번 더 정규화할 수 있다. 그 이야기는 14장에서 다시 꺼낸다.

또 하나 짚을 점은 "선택된 객체"라는 발상 자체가 이미 진실의 위치를 흐린다는 사실이다. 사용자가 "선택"한 결과는 사실 한 가지 정보다. **누가 선택되었는가?** 그것은 한 줄짜리 답으로 끝나는 질문이다. 굳이 이 답을 객체 사본으로 펼쳐 들 이유가 없다. ID 한 자리만 차지하는 짧은 답이 우리가 원하는 모양이다.

반대 방향에서 한 가지 더 자주 보는 함정도 짚어 두자. "원본 데이터가 비동기로 갱신되니까, 선택된 항목은 미리 캐시해 둬야 한다"라는 발상이다. 보통 데이터는 서버에서 주기적으로 다시 받아 오고, 그 사이에 사용자가 선택을 유지한다고 가정해 본다. 이때 선택된 객체를 통째로 들고 있으면 새 데이터가 와도 옛 데이터가 화면에 머문다. 누군가는 이걸 "안정성"이라고 부르고 싶을 수 있다. 하지만 그건 안정성이 아니라 **stale 데이터를 화면에 남기는 버그**다. 진짜로 옛 데이터를 보여주고 싶다면, 그건 별도 의도이고 별도 코드 경로다. 그 경우엔 보통 "최근 선택 시점에 본 데이터"를 명시적으로 스냅샷으로 보관하는 패턴을 따로 만든다. 디폴트는 어디까지나 ID로 가리키고, 화면은 가장 최신 데이터를 비춘다.

## 2.6 prop을 state로 미러링하지 말자

비슷한 함정이 props에서도 일어난다. 부모로부터 받은 props 값을 자식이 자기 state로 복사해 두는 패턴이다.

```tsx
// 안티패턴: prop을 state로 미러링한다
import { useState } from 'react';

function ColorBadge({ color }: { color: string }) {
  // color가 처음 들어온 값에서 멈춘다. 부모가 prop을 바꿔도 반영되지 않는다.
  const [innerColor, setInnerColor] = useState(color);
  return <span style={{ background: innerColor }}>{innerColor}</span>;
}
```

이 코드의 문제는 분명하다. `useState(color)`는 **첫 렌더에만** `color`를 초깃값으로 사용한다. 그 이후 부모가 `color` prop을 바꾸어 내려보내도 `innerColor`는 옛날 값에 그대로 묶여 있다. 컴포넌트 모양만 보면 "color를 받아서 표시한다"인데, 실제로는 "처음 받은 color에서 영영 안 바뀐다." 모양과 동작이 어긋난 코드다. 가장 디버깅하기 어려운 종류의 버그가 여기서 나온다.

해법은 두 갈래다. 첫째, **그냥 prop을 직접 쓰자.** state로 옮길 이유가 없다.

```tsx
// 권장: prop을 그대로 쓴다
function ColorBadge({ color }: { color: string }) {
  return <span style={{ background: color }}>{color}</span>;
}
```

둘째, 의도가 정말로 "처음 들어온 값을 초깃값으로 삼고 그 뒤로는 자식이 독립적으로 관리한다"라면, **이름에 그 의도를 담자.**

```tsx
// 의도가 "초깃값"임을 이름으로 드러낸다
function ColorPicker({ initialColor }: { initialColor: string }) {
  const [color, setColor] = useState(initialColor);
  return (
    <input
      type="color"
      value={color}
      onChange={(e) => setColor(e.target.value)}
    />
  );
}
```

이름이 `color`가 아니라 `initialColor`다. 호출하는 쪽에서도 "이건 초깃값이고, 그 뒤로는 내부에서 관리되는 것이구나" 알아챌 수 있다. 이름 하나가 코드의 의도를 가르는 칸막이가 된다. 잊지 말자, **변수 이름은 가장 싼 문서**다.

여기서 한 단계 더 나아간 사례도 살펴보자. 가끔은 prop이 바뀔 때 일부 state만 리셋하고 일부는 유지하고 싶을 때가 있다. 예를 들어, 채팅 컴포넌트에서 상대가 바뀌면 입력 중이던 초고만 비우고, "내 프로필 정보"는 그대로 유지하고 싶다면? 첫 시도로 `useEffect`로 prop 변화를 감지해 setState를 호출하는 코드를 떠올리기 쉽다.

```tsx
// 안티패턴: prop 변경을 effect로 감지해 state를 리셋한다
function Chat({ contact }: { contact: Contact }) {
  const [draft, setDraft] = useState('');

  useEffect(() => {
    setDraft(''); // prop이 바뀌면 초고를 비운다
  }, [contact.id]);

  return <textarea value={draft} onChange={(e) => setDraft(e.target.value)} />;
}
```

이 코드의 문제는 한 박자 늦은 깜빡임이다. 새 contact의 화면이 한 프레임 동안 옛 draft 텍스트와 함께 그려진 다음, effect가 돌면서 다시 한 번 빈 화면으로 그려진다. 두 번 렌더된다는 비용도 비용이지만, 사용자 입장에서 잠시 잘못된 화면이 보인다는 점이 더 큰 문제다.

그럼 어떻게 해야 할까? React가 권장하는 정공법은 **`key` prop으로 컴포넌트 자체를 새 컴포넌트로 인식시키는 것**이다.

```tsx
// 권장: key가 바뀌면 React가 컴포넌트를 처음부터 다시 만든다
function ChatPage({ contact }: { contact: Contact }) {
  return <Chat key={contact.id} contact={contact} />;
}

function Chat({ contact }: { contact: Contact }) {
  // key가 바뀌면 이 useState는 처음부터 다시 초기화된다.
  const [draft, setDraft] = useState('');
  return <textarea value={draft} onChange={(e) => setDraft(e.target.value)} />;
}
```

`key`는 보통 리스트 항목의 식별자로 쓰지만, 이렇게 단일 컴포넌트의 리셋 트리거로도 쓸 수 있다. React 입장에서 `key`가 바뀐 컴포넌트는 이전과 같은 자리에 있어도 **다른 컴포넌트**로 취급된다. 그래서 안의 모든 state, 모든 effect가 처음부터 다시 시작된다. 깔끔하다. 다만 이 방법은 컴포넌트의 모든 state를 리셋한다는 점에 유의하자. "일부만 리셋"이 정말 필요하다면 그건 또 다른 패턴이 필요하다 — 그 이야기는 4장에서 다시 만난다.

prop 미러링의 다른 변종으로 자주 보는 것이 **"controlled처럼 쓰면서 uncontrolled로 짠" 컴포넌트**다. 부모가 props로 값을 내려주는데, 자식은 자기 state로 그 값을 들고 있고, onChange로 부모에게 알려주는 모양이다. 결과적으로 **두 군데에서 같은 값을 따로따로 들고 있는** 모양이 된다. 부모가 외부 사정으로 값을 바꾸면 자식이 모르고, 자식이 입력을 받으면 부모는 알지만 자기 카피가 한 박자 뒤늦게 반영된다. 이 패턴이 보이면 둘 중 하나를 골라야 한다. **완전히 controlled로** 가서 자식에게서 state를 빼거나, **완전히 uncontrolled로** 가서 부모에게서 state를 빼고 ref로 값을 읽거나. 어중간한 중간은 거의 항상 후회한다.

## 2.6.5 한 걸음 더 — 실전에서 자주 만나는 변형들

원칙은 익혔으니, 이제 실전에서 자주 만나는 변형 몇 개를 짚어 두고 가자. 머릿속의 원칙이 코드와 만나는 자리는 늘 미묘한 변형이고, 그 변형마다 함정이 한 번씩 숨어 있다.

**변형 1: 정렬 키와 정렬된 결과를 둘 다 들고 있는 패턴.** 리스트 화면에서 정렬 옵션을 바꿀 수 있게 해 두면, 보통 처음 짤 때는 다음과 같이 짜게 된다.

```tsx
// 안티패턴: sortKey와 sortedItems를 둘 다 state로
function SortedList({ items }: { items: Item[] }) {
  const [sortKey, setSortKey] = useState<'name' | 'price'>('name');
  const [sortedItems, setSortedItems] = useState<Item[]>(items);

  // 정렬할 때마다 setState — 잊으면 화면과 정렬키가 어긋난다
  function handleSort(key: 'name' | 'price') {
    setSortKey(key);
    setSortedItems([...items].sort((a, b) => /* ... */ 0));
  }
  // ...
}
```

여기서 `sortedItems`는 `items`와 `sortKey`로부터 계산 가능한 파생값이다. 별도 state일 이유가 없다.

```tsx
// 권장: 정렬 결과는 매 렌더마다 파생한다
function SortedList({ items }: { items: Item[] }) {
  const [sortKey, setSortKey] = useState<'name' | 'price'>('name');
  // 정렬이 비싸면 useMemo로 감싼다. 작으면 그냥 변수.
  const sortedItems = [...items].sort((a, b) =>
    sortKey === 'name' ? a.name.localeCompare(b.name) : a.price - b.price
  );
  return (
    <div>
      <button onClick={() => setSortKey('name')}>이름 순</button>
      <button onClick={() => setSortKey('price')}>가격 순</button>
      <ul>{sortedItems.map((it) => <li key={it.id}>{it.name}</li>)}</ul>
    </div>
  );
}
```

**변형 2: 검색 쿼리와 검색 결과를 둘 다 state로 두는 패턴.** 같은 함정이다. 쿼리 문자열만 state로 두고, 결과는 매 렌더에 filter로 파생하면 된다. 디바운싱이 필요하면 쿼리 자체에 디바운스를 거는 패턴(예: `useDeferredValue`)이 있다. 결과를 별도 state로 들고 있다가 effect로 채우는 코드는 거의 항상 안티패턴이다.

**변형 3: "선택된 탭"을 객체로 들고 있는 패턴.** 탭이 다음과 같다고 해 보자.

```tsx
const tabs = [
  { id: 'overview', title: '개요' },
  { id: 'detail', title: '세부' },
  { id: 'review', title: '리뷰' },
] as const;
type TabId = (typeof tabs)[number]['id'];
```

흔한 첫 시도는 `useState(tabs[0])`이다. 이 경우엔 함정이 비교적 약하다. 탭 정의가 정적이라면 stale 참조 문제가 거의 없다. 그래도 정공법은 ID만 두는 것이다. `useState<TabId>('overview')`. 이렇게 하면 탭 정의가 나중에 동적으로 바뀌어도 자동으로 따라간다. 그리고 직렬화(예: URL 파라미터로 저장)할 때 그냥 문자열 한 자리면 끝이다. **ID는 직렬화 친화적**이라는 부수 효과까지 따라온다.

**변형 4: 폼 검증 메시지를 state로 들고 있는 패턴.** "비밀번호가 8자 이상이어야 합니다" 같은 메시지를 별도 state로 두는 코드가 흔하다. 이것 역시 보통은 파생값이다. 입력값으로부터 검증 함수가 메시지를 만들어 낼 수 있다. effect로 메시지를 채울 필요가 없다.

```tsx
function PasswordField() {
  const [password, setPassword] = useState('');
  // 파생값 — 매 렌더에 즉석에서 계산된다
  const errorMessage = validatePassword(password);

  return (
    <div>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {errorMessage && <p role="alert">{errorMessage}</p>}
    </div>
  );
}

function validatePassword(value: string): string | null {
  if (value.length === 0) return null; // 입력 전엔 메시지 없음
  if (value.length < 8) return '비밀번호는 8자 이상이어야 합니다';
  if (!/[A-Z]/.test(value)) return '대문자를 1개 이상 포함해야 합니다';
  return null;
}
```

이 패턴은 상태가 한 자리로 줄어드는 것보다 더 큰 이득을 안긴다. 검증 함수가 **순수 함수**로 분리되어 단위 테스트하기 쉬워진다. UI 코드와 검증 규칙이 한 데 엉켜 있던 것을 떼어낸 셈이다. 가벼운 리팩토링 한 번이 코드의 품질을 한 단계 올리는 자주 보는 모범 사례다.

**변형 5: 카운트와 마지막 항목을 둘 다 state로 두는 패턴.** "메시지 수"와 "마지막 메시지"를 따로 들고 있다가, 둘이 어긋나는 일도 흔하다. 메시지 배열 하나만 state로 두고, 수와 마지막 항목은 모두 파생하면 깔끔하다.

```tsx
const [messages, setMessages] = useState<Message[]>([]);
// 둘 다 파생값 — 별도 state가 아니다
const messageCount = messages.length;
const lastMessage = messages[messages.length - 1];
```

이런 변형들을 보면 한 가지가 분명해진다. **state는 가능한 한 적은 수의 "최소 정보"여야 한다.** 그 최소 정보로부터 화면이 필요로 하는 모든 것이 계산될 수 있어야 한다. 이 발상을 어디서 본 적이 있는가? 그렇다, 정보 이론의 **최소 부호화** 발상과 같은 결이다. 모든 정보를 가장 짧은 표현으로 압축하면, 그 표현을 다루는 비용이 가장 낮다. 우리의 state도 같은 모양을 추구한다. 가장 짧게, 가장 적게, 그러면서도 화면 전체를 파생할 수 있을 만큼.

여기서 한 가지 자기점검을 해 보자. 지금 작업 중인 컴포넌트의 useState 목록을 한 번 죽 적어 보자. 그리고 각 항목을 두고 묻자. **"이 값을 지우면 다른 값으로부터 다시 만들어 낼 수 있는가?"** 답이 "예"인 것이 절반쯤 있다면, 그 컴포넌트는 본 장의 권유로부터 가장 큰 이득을 볼 차례다. 한 번 정리하고 나면, 그다음부터는 비슷한 패턴이 보이는 즉시 손이 먼저 움직이게 된다.

## 2.7 깊은 트리는 평탄화 가능하다 — 한 단락 예고

여기까지 오면 한 가지 더 큰 그림자가 어른거린다. "그러면 댓글 트리처럼 답글이 답글을 다는 깊이 4단계, 5단계 중첩된 데이터는?" 이 질문은 정당하다. 우리가 살펴본 모든 사례는 평면적인 객체 한두 개짜리였다. 트리 구조는 다른 차원의 까다로움이 있다. 어떤 한 노드를 갱신하려면 부모, 부모의 부모, 그 위까지 모든 경로의 객체를 새로 만들어야 한다. spread 연산자가 다섯 번 중첩된다. 끔찍한 일이다.

그래서 React 생태계에는 오래된 처방이 하나 있다. **정규화(normalization)**다. 트리를 ID를 키로 하는 **lookup table** 한 장과, 노드마다 `childIds: number[]`로 자식을 가리키는 **포인터의 모양**으로 펼친다. 이렇게 하면 모든 노드가 평면 한 장에 모이고, 갱신은 단 한 노드만 새로 만들면 끝난다. Redux나 normalizr 같은 도구가 오래전부터 권해 온 모양이고, 지금도 큰 데이터를 다루는 화면이라면 거의 표준에 가깝다.

다만 이 책에서 정규화는 **14장 통합 시나리오**에서 본격적으로 다룰 예정이다. 본 장에서 다 풀기엔 분량이 부담스럽고, 무엇보다 정규화는 단독 기법이라기보다 "선택은 ID로", "원본은 한 군데", "갱신은 불변하게"라는 본 장의 원칙들이 모여서 자연스럽게 도달하는 결과다. 지금은 이 한 마디만 마음에 두고 가자. **깊은 트리도 평탄한 평면으로 펼칠 수 있다.** 본 장에서 익힌 "ID로 가리키기"는 그 평면화의 가장 단순한 한 조각이다. 14장에 가서 우리는 같은 원칙을 트리 전체에 적용하게 된다.

미리 한 번만 모양을 슬쩍 보여주고 가자. 댓글 트리를 정규화하면 다음과 같은 모양이 된다.

```tsx
// 정규화된 댓글 데이터 — 14장에서 본격적으로 다룬다
type CommentMap = {
  [id: string]: {
    id: string;
    text: string;
    authorId: string;
    childIds: string[]; // 답글의 ID만 들고 있다
  };
};

type CommentsState = {
  byId: CommentMap;
  rootIds: string[];
};
```

여기서 한 노드를 갱신하려면 어떻게 하는가? `byId[targetId]` 한 자리만 새 객체로 바꾸면 끝이다. 트리 깊이와 무관하게 단 한 객체만 새로 만들면 충분하다. 자식을 추가하려면 부모의 `childIds`에 새 ID 하나를 push하고, `byId`에 새 항목 하나를 등록한다. 노드 사이의 관계는 **참조가 아니라 ID로** 표현되니, 깊이가 아무리 깊어도 갱신은 평면적인 작업이 된다. spread 다섯 번 중첩이 없다. 본 장에서 본 ID 보관 기법이 한 단계 위에서 다시 등장한 셈이다.

다만 이 모양에는 비용도 따른다. 데이터를 화면에 그릴 때 매번 ID로 자식을 찾아 들어가야 하고, 직렬화·역직렬화 시에 평면-트리 변환 코드를 한 번 거쳐야 한다. 그래서 모든 데이터를 미리 정규화할 필요는 없다. 갱신 빈도가 낮고 깊이도 얕은 데이터라면 그냥 트리 모양으로 두는 편이 더 단순하다. **정규화는 도구이지 의무가 아니다.** 14장에서 우리는 어떤 신호가 보일 때 정규화를 도입하면 좋은지, 그 트레이드오프와 함께 본격적으로 다루게 된다.

## 2.7.5 잠시, "그러면 useEffect는 언제 쓰는 건가?"

본 장을 따라오면서 눈치챘을 것이다. **본 장이 권한 거의 모든 패턴이 useEffect를 빼라고 말한다.** 파생값은 effect로 채우지 말고, 검증 메시지도 effect로 만들지 말고, prop 변경에 따른 state 리셋도 effect로 하지 말라고 한다. 그럼 useEffect는 언제 쓰는 도구인가?

답은 단순하다. **외부 시스템과 동기화할 때.** React 공식 가이드의 표현을 그대로 빌리면, useEffect는 "컴포넌트를 외부 시스템과 동기화"하기 위한 escape hatch다. 외부 시스템이란 React가 모르는 모든 것이다. 브라우저 API(setTimeout, addEventListener, IntersectionObserver 등), 비-React 라이브러리(차트, 지도, 비디오 플레이어), 네트워크(WebSocket, SSE), 서드파티 SDK(분석, 결제) 같은 것들이다. 이런 것들과 React state를 맞추려면 어쩔 수 없이 effect가 필요하다.

그런데 여기서 자주 헷갈리는 한 가지가 있다. **fetch는 어느 쪽인가?** 네트워크니까 외부 시스템이지만, 그 결과를 화면에 그리는 것이라면 결국 React 안에서 흐름을 다루는 것이다. 결론부터 말하면, 단순한 fetch는 effect로 짜도 되지만 그것보다 훨씬 더 좋은 도구가 이미 있다 — TanStack Query, SWR 같은 서버 상태 라이브러리다. 캐시 무효화, 재시도, 낙관적 업데이트, race condition 방지 같은 것들을 모두 처리해 준다. 이 이야기는 9장 "서버 상태와 클라이언트 상태"에서 본격적으로 다룬다.

그러면 본 장의 권유와 escape hatch 챕터(2부)의 권유가 자연스럽게 이어진다. **첫째, effect를 쓰기 전에 그게 정말 외부 시스템과의 동기화인지 자문하자.** 둘째, 외부 시스템 동기화가 맞다면 그걸 effect로 짜는 데에 망설이지 말자. 셋째, 외부 시스템이 자주 다루는 것이라면 그 패턴을 추상화한 라이브러리(TanStack Query 같은)를 쓰는 편이 거의 항상 낫다. 이 세 단계를 마음에 두면 useEffect를 둘러싼 대부분의 안개가 걷힌다.

## 2.8 1장의 다섯 단계 — "비본질 제거"라는 단계의 정체

여기서 잠깐 1장과 다리를 놓아두자. 1장에서 우리는 React 공식 가이드의 "다섯 단계 상태 모델링"을 따라 걸었다. 다시 정리하면 이렇다.

1. 모든 시각 상태를 식별한다.
2. **무엇이 그 상태들을 변하게 하는지 따져 본다.**
3. 메모리에 보관할 state를 `useState`로 표현한다.
4. **본질이 아닌 state를 제거한다.**
5. 트리거를 처리할 이벤트 핸들러를 연결한다.

본 장이 자세히 다룬 단계가 어느 단계인가? 정확히 **4번, "본질이 아닌 state를 제거한다"** 단계다. 우리가 살펴본 네 가지 패턴은 모두 그 단계의 구체적인 도구였다.

- **fullName 사례** → 다른 state로부터 계산 가능한 값은 본질이 아니다. 빼자.
- **status enum** → 모순 가능한 boolean 조합은 사실 한 변수의 분해된 모양이다. 합치자.
- **ID로 보관** → 객체 사본은 진실의 복제다. 진실은 한 군데, 나머지는 포인터로.
- **prop 미러링 금지** → props는 이미 부모가 들고 있는 진실이다. 두 번 보관하지 말자.

이 네 가지를 의식적으로 적용하기 시작하면, 컴포넌트가 처음 짤 때보다 훨씬 가벼워진다는 것을 곧 느끼게 된다. `useState`의 개수가 줄고, 갱신해야 할 변수의 개수가 줄고, 동기화해야 할 짝의 개수가 줄어든다. 디버깅이 쉬워지고, 새 동료가 코드를 열어봤을 때 짚어낼 점이 줄어든다. 그것이 "본질이 아닌 것을 솎아낸다"의 실제 효용이다.

조금 더 큰 그림에서 이 단계를 보자. React 공식 가이드의 다섯 단계는 한 줄로 요약하면 "**state는 가능한 한 적게**"라는 한 가지 원칙의 절차적 풀이다. 적게 두면 어긋날 짝이 줄고, 어긋날 짝이 줄면 버그가 살 자리가 줄고, 버그가 줄면 우리가 디버거를 켜는 시간이 줄어든다. 그 절약된 시간이 새 기능을 짜는 시간으로 흐른다. 좋은 상태 설계가 결국 좋은 개발 속도로 이어지는 이유가 그것이다. 반대로 state를 많이 두면 두 박자, 세 박자 어긋난 화면이 곳곳에서 새어 나오고, 그것을 메우느라 개발자는 setX 호출을 한 줄 더 적는다. 그 한 줄이 다음 어긋남의 씨앗이 된다. 끔찍한 일이다.

그러니 코드 리뷰 때 한 가지 질문만 추가해 보자. **"이 useState는 정말로 필요한가? 다른 state로부터 계산할 수 없는가?"** 이 질문 하나만 매번 던져도, 팀 전체의 컴포넌트가 한 단계씩 가벼워진다. 본 장의 핵심을 한 줄로 압축하면 그 한 가지 질문이다.

## 2.8.5 자주 받는 질문 몇 가지

본 장의 원칙들을 적용하다 보면 자주 따라오는 질문 몇 개가 있다. 미리 답해 두자.

**Q. "그래도 매 렌더마다 계산하면 결국 느려지지 않을까요?"**
A. 거의 항상 그렇지 않다. React는 우리가 생각보다 자주 렌더한다. 부모가 다시 렌더되면 자식도 다시 렌더된다. 그래서 컴포넌트 함수 본체는 자주 호출되는 자리이고, JS 엔진은 그 호출을 매우 빠르게 처리한다. 단순한 계산식 한 줄, 배열 filter 한 번 정도는 수십~수백 마이크로초로 끝난다. 사용자가 인지할 수 없는 시간이다. 정말로 느려지는 자리는 1) 큰 배열에 대한 무거운 계산, 2) 큰 트리의 매 렌더 — 이 두 가지인데, 둘 다 useMemo·React.memo·가상화 같은 별도 도구로 다룬다. **기본은 그냥 계산이고, 도구는 측정 후에 골라서** 적용하자.

**Q. "useState 하나에 큰 객체를 넣으면 나쁜가요? 차라리 여러 useState로 쪼개는 게 좋을까요?"**
A. 정답은 "도메인이 결정한다"이다. 한 번의 사용자 의도로 함께 바뀌는 값들이라면 한 객체로 모으는 편이 낫다. 예를 들어 `{ x, y }` 좌표는 거의 항상 같이 변하니까 한 state에 넣는다. 반대로 서로 독립적으로 변하는 값들은 따로 두는 편이 낫다. "전송 중 여부"와 "입력 텍스트"는 같이 변하는 짝이 아니니, 둘을 한 객체에 넣을 이유가 약하다. 다만 한 객체에 너무 많이 넣어 모양이 복잡해지면 useReducer로 옮겨갈 시점이다. 이 경계는 4장에서 다시 다룬다.

**Q. "useState의 초깃값으로 함수 호출을 쓰면 매 렌더마다 계산되나요?"**
A. 그렇지 않다. `useState(expensiveCompute())`는 매 렌더마다 `expensiveCompute()`가 호출된다(결과는 첫 렌더 외에는 무시되지만, 호출 자체는 일어난다). 비싸다면 `useState(() => expensiveCompute())`처럼 함수를 넘기자. 이걸 lazy initializer라고 부른다. 첫 렌더 때 단 한 번만 호출된다. 자주 쓰지는 않지만 알아 두면 좋다.

**Q. "fullName을 컨트롤드 컴포넌트(`<input value={fullName} />`)로 만들고 싶으면 어떻게 해야 하나요?"**
A. 그러면 fullName은 더 이상 firstName + lastName의 단순 파생이 아니다. **사용자가 직접 입력할 수 있는 별도의 진실**이 된다. 그땐 본 장의 원칙대로 fullName을 진짜 state로 둬야 한다. 다만 그 경우엔 firstName과 lastName 둘은 더 이상 별도 state로 둘 필요가 없다 — fullName 한 자리만 있으면 된다. 다시 말해, **무엇이 사용자가 직접 입력하는 진실인지를 가른 다음 그 진실 한 가지만 state로 둔다.** firstName과 lastName을 동시에 받아야 한다면 그 둘이 진실이고, fullName은 파생값이다. 반대로 fullName을 한 칸으로 받는 화면이라면 fullName이 진실이고, firstName/lastName은 (필요하다면) 파생값이다. **state의 모양은 UX가 결정한다.**

**Q. "useState 다섯 개로 짜다가 useReducer로 옮겨야 할 시점은 언제인가요?"**
A. 일반적으로 **한 액션이 여러 state를 동시에 갱신하는 경우가 셋 이상** 보이거나, **이벤트 핸들러 두 개에서 같은 종류의 갱신이 반복**되면 reducer로 옮겨갈 때다. 정확한 기준은 4장에서 다시 풀지만, 미리 한 줄만 답해 두자. **"같은 의도가 흩어져 있다"**는 신호가 reducer가 필요한 신호다.

**Q. "객체 state를 갱신할 때 spread를 쓰지 않고 mutate하면 안 되나요?"**
A. 안 된다. React는 참조 비교로 변화를 감지한다. mutate하면 참조가 그대로라 React가 변화를 모르고, 화면이 갱신되지 않는다. 항상 새 객체를 만들어 setState에 넘겨야 한다. spread가 번거롭다면 Immer 같은 라이브러리로 mutate처럼 적되 내부적으로는 새 객체를 만드는 패턴을 쓸 수 있다.

이쯤에서 본 장의 큰 그림을 한 번 더 짚고 가자. 우리가 다룬 모든 패턴은 결국 **"진실을 한 군데에 모은다"**라는 한 가지 원칙의 다양한 얼굴이었다. 파생값은 진실이 아니다 → 빼라. 두 boolean이 한 진실의 두 얼굴이다 → 합쳐라. 객체 사본은 진실의 복제다 → ID로 가리켜라. prop은 부모의 진실이다 → 미러링하지 마라. 다섯 가지 다른 권유가 사실 한 원칙의 다섯 가지 적용 사례다. 이 한 원칙을 단단히 잡아 두면, 본 장의 모든 코드 패턴이 자연스럽게 따라온다.

## 2.9 핵심 정리

본 장의 요지를 한눈에 모아 두자.

1. **같은 진실을 두 군데 두지 말자.** 그것이 모든 동기화 버그의 뿌리다.
2. **다른 state나 props로부터 계산 가능한 값은 state가 아니다.** 그냥 변수로 빼자.
3. **렌더 중 계산은 거의 항상 충분히 빠르다.** "캐싱하면 빠르겠지"라는 직관은 의심하자.
4. **`useMemo`는 측정해서 느렸을 때만 두르자.** 기본은 그냥 변수다.
5. **Effect로 파생값을 계산해서 state에 넣지 말자.** 두 번 렌더되고, 한 박자 깜빡인다.
6. **모순 가능한 boolean 두 개는 거의 항상 enum 하나로 합쳐진다.** 불가능한 상태는 코드에서 표현 불가능해야 한다.
7. **선택은 객체가 아니라 ID(또는 index)로 보관하자.** 원본이 바뀌면 따라가야 한다.
8. **prop을 state로 미러링하지 말자.** 정말 초깃값으로만 쓸 거라면 이름을 `initialX`로 바꾸자.
9. **깊은 트리는 평탄화 가능하다.** 본격적인 정규화는 14장에서 만난다.
10. **컴포넌트의 `useState` 개수가 늘어날 때마다 한 번씩 자문하자.** "이 중 본질이 아닌 것은 어느 것인가?"

이 정리를 책상 옆에 적어 두고 코드 리뷰 때 펼쳐 보는 것도 한 방법이다. 동료의 PR을 볼 때 useState가 다섯 개 이상 모이면, 위 열 개 항목을 한 번씩 짚어 보자. 거의 항상 적어도 하나 이상 줄일 자리가 보인다. "여기 useState 두 개를 합칠 수 있어요"라고 코멘트 하나 다는 것이 코드 품질에 가장 빠르게 기여하는 길이다. 화려한 새 기능보다, 안 쓰는 한 줄을 지우는 일이 더 큰 가치를 만들 때가 많다.

## 2.9.5 한 컴포넌트 처음부터 끝까지 — 종합 사례

원칙들을 따로따로 풀어 봤으니, 마지막으로 그것들이 한 컴포넌트 안에서 어떻게 동시에 작동하는지 봐 두자. 다음은 본 장의 모든 안티패턴이 한 자리에 모인 컴포넌트다. 한 줄씩 따라가며 어디가 본 장의 권유와 어긋나는지 짚어 보자.

```tsx
// 안티패턴 다섯 가지가 모인 컴포넌트
import { useEffect, useState } from 'react';

type Product = { id: number; name: string; price: number };

function BadCart({ products, initialDiscountRate }: {
  products: Product[];
  initialDiscountRate: number;
}) {
  const [items] = useState(products);
  const [selected, setSelected] = useState<Product | null>(null); // 1. 객체로 보관
  const [discountRate, setDiscountRate] = useState(initialDiscountRate); // 2. prop 미러링
  const [total, setTotal] = useState(0); // 3. 파생값을 state로
  const [discountedTotal, setDiscountedTotal] = useState(0); // 3. 또 파생값
  const [isCheckingOut, setIsCheckingOut] = useState(false); // 4. 모순 가능 boolean
  const [isCheckedOut, setIsCheckedOut] = useState(false);

  useEffect(() => {
    // 5. 파생값 계산을 effect로
    const t = items.reduce((sum, it) => sum + it.price, 0);
    setTotal(t);
    setDiscountedTotal(t * (1 - discountRate));
  }, [items, discountRate]);

  async function checkout() {
    setIsCheckingOut(true);
    await fakeCheckout();
    setIsCheckingOut(false);
    setIsCheckedOut(true);
  }

  // ... 렌더링
  return null;
}
async function fakeCheckout() { return new Promise((r) => setTimeout(r, 500)); }
```

자, 다섯 가지 안티패턴을 모두 짚었는가? 차례대로다. (1) 선택된 상품을 객체로 들고 있어 stale 참조의 위험이 있다. (2) `initialDiscountRate`라는 prop을 state로 미러링해 부모의 변경이 반영되지 않는다(다만 이름이 `initial`이니, 의도가 정말 "초기값"이라면 상관 없다 — 의도부터 분명히 하자). (3) `total`과 `discountedTotal`은 둘 다 `items`와 `discountRate`로부터 계산 가능한 파생값이다. (4) `isCheckingOut`과 `isCheckedOut`은 동시에 true가 될 수 있는 모순 가능 boolean이다. (5) 그 파생값을 effect로 채우니 매 변경에 두 번 렌더되고 첫 렌더에는 0이 그대로 보인다.

이 다섯을 한 번에 고치면 어떻게 될까?

```tsx
// 권장: 다섯 안티패턴을 모두 정리한 모양
import { useState } from 'react';

type Product = { id: number; name: string; price: number };
type CheckoutStatus = 'idle' | 'checking-out' | 'done';

function GoodCart({ products, discountRate }: {
  products: Product[];
  discountRate: number;
}) {
  // (1) 선택은 ID로
  const [selectedId, setSelectedId] = useState<number | null>(null);
  // (4) 모순 가능 boolean → enum
  const [status, setStatus] = useState<CheckoutStatus>('idle');

  // (2) prop은 그대로 쓴다 — 별도 state로 미러링하지 않는다
  // (3, 5) 파생값은 매 렌더에 그냥 계산
  const total = products.reduce((sum, it) => sum + it.price, 0);
  const discountedTotal = total * (1 - discountRate);
  const selected = products.find((p) => p.id === selectedId) ?? null;

  async function checkout() {
    setStatus('checking-out');
    await fakeCheckout();
    setStatus('done');
  }

  if (status === 'done') return <p>결제가 완료되었습니다.</p>;

  const isCheckingOut = status === 'checking-out'; // 파생값

  return (
    <div>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <button onClick={() => setSelectedId(p.id)}>{p.name}</button>
          </li>
        ))}
      </ul>
      {selected && <p>선택: {selected.name} ({selected.price}원)</p>}
      <p>합계: {total}원</p>
      <p>할인 적용: {discountedTotal}원</p>
      <button onClick={checkout} disabled={isCheckingOut}>
        {isCheckingOut ? '결제 중...' : '결제하기'}
      </button>
    </div>
  );
}
async function fakeCheckout() { return new Promise((r) => setTimeout(r, 500)); }
```

useState가 다섯 개에서 두 개로 줄었다. useEffect는 사라졌다. 모순 가능한 boolean 두 개는 한 enum으로 합쳐졌다. 객체 사본은 ID 한 자리로 줄었다. prop 미러링은 사라졌다. 그러면서도 화면에 보이는 것은 똑같다. 오히려 동기화 버그가 살 자리가 없으니 더 안정적이다.

이 두 코드를 비교해 보면 본 장이 권한 변화의 크기를 한눈에 느낄 수 있다. **한 컴포넌트에서 useState가 절반 이하로 줄고, useEffect가 사라지고, 동기화 코드가 사라진다.** 이런 변화는 한 컴포넌트만의 이득이 아니다. 그 컴포넌트를 호출하는 부모, 그것을 디버깅하는 동료, 그 코드를 6개월 뒤에 다시 만나는 우리 자신 모두에게 이득이다. 좋은 코드는 늘 그렇게 여러 사람에게 동시에 이득을 안긴다.

## 2.10 연습 문제

직접 손으로 짜 보지 않으면 이 원칙들은 살로 붙지 않는다. 세 문제를 풀어 보자. 처음 두 문제는 본 장의 주요 기법을 그대로 적용하면 풀린다. 마지막은 한 단계 도전적이다.

### 연습 2-1. firstName / lastName / fullName 리팩토링 [기초]

다음 코드는 안티패턴 폼이다. `fullName`을 별도 state로 들고 있어, `firstName` 또는 `lastName`을 바꿀 때마다 setFullName을 잊지 말아야 한다. 누군가가 외부 함수에서 `setFirstName`만 호출하는 시나리오를 떠올리며, **fullName을 파생값으로 바꾸는** 리팩토링을 해보자.

```tsx
// 시작 코드 (이걸 고쳐 보자)
import { useState } from 'react';

export function NameForm() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [fullName, setFullName] = useState('');

  return (
    <div>
      <input
        value={firstName}
        onChange={(e) => {
          setFirstName(e.target.value);
          setFullName(e.target.value + ' ' + lastName);
        }}
        placeholder="이름"
      />
      <input
        value={lastName}
        onChange={(e) => {
          setLastName(e.target.value);
          setFullName(firstName + ' ' + e.target.value);
        }}
        placeholder="성"
      />
      <p>전체 이름: {fullName || '(아직 비어 있음)'}</p>
    </div>
  );
}
```

체크 포인트:
- `useState` 개수가 셋에서 둘로 줄었는가?
- `onChange` 핸들러가 한 줄짜리로 단순해졌는가?
- 외부에서 `firstName`만 갱신해도 `fullName`이 자동으로 따라오는가?

### 연습 2-2. 상품 리스트 + 선택된 상품을 ID로 [중간]

상품 리스트 화면을 짜 보자. 사용자는 상품을 클릭해 선택하고, 다른 어딘가에서 "재고 보충" 버튼으로 모든 상품의 가격을 1000원씩 올린다. 다음 시작 코드는 선택된 상품을 객체 통째로 들고 있어, 가격을 올린 뒤에도 선택 패널엔 옛 가격이 남는 버그가 있다. **ID로 보관하도록 리팩토링하자.**

```tsx
// 시작 코드 (버그 포함)
import { useState } from 'react';

type Product = { id: number; name: string; price: number };

const initial: Product[] = [
  { id: 101, name: '키보드', price: 89000 },
  { id: 102, name: '마우스', price: 32000 },
  { id: 103, name: '모니터', price: 280000 },
];

export function Shop() {
  const [products, setProducts] = useState<Product[]>(initial);
  const [selected, setSelected] = useState<Product | null>(initial[0]);

  function bumpAllPrices() {
    setProducts((prev) => prev.map((p) => ({ ...p, price: p.price + 1000 })));
    // selected는 그대로다. 버그.
  }

  return (
    <div>
      <button onClick={bumpAllPrices}>전체 가격 +1000</button>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <button onClick={() => setSelected(p)}>
              {p.name} ({p.price}원)
            </button>
          </li>
        ))}
      </ul>
      {selected && (
        <section>
          <h3>선택됨</h3>
          <p>{selected.name}: {selected.price}원</p>
        </section>
      )}
    </div>
  );
}
```

목표:
- `selected` 자리를 `selectedId: number | null`로 바꾼다.
- 렌더 중에 `products.find(p => p.id === selectedId)`로 실제 객체를 가져온다.
- `bumpAllPrices`가 선택 패널의 가격에도 즉시 반영되는지 확인한다.

### 연습 2-3. `Set<id>`로 다중 선택 [도전]

이번엔 다중 선택 리스트다. 사용자가 체크박스로 여러 상품을 선택할 수 있고, 한 번에 수십~수백 개를 토글할 수 있다. 단순히 `selectedIds: number[]` 배열을 쓰면 "이 상품이 선택되어 있나?"라는 검사가 매번 O(n)이 되어 큰 리스트에서 답답해진다. **`Set<number>`로 바꿔서 O(1) 검사가 되도록 짜 보자.** 단, React state로서 Set을 다룰 때의 함정을 기억하자 — Set을 그 자리에서 mutate하면 React가 변경을 감지하지 못한다.

```tsx
// 출발점 — 여기서 시작해 완성하자
import { useState } from 'react';

type Product = { id: number; name: string };

const sample: Product[] = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  name: `상품 ${i + 1}`,
}));

export function MultiSelectShop() {
  const [products] = useState<Product[]>(sample);
  // 빈 Set으로 시작
  const [selectedIds, setSelectedIds] = useState<Set<number>>(() => new Set());

  function toggle(id: number) {
    // 힌트: 새 Set을 만들어 setSelectedIds로 넣어야 한다.
    // 직접 selectedIds.add(id)하고 setSelectedIds(selectedIds)는 동작하지 않는다 (참조가 같음).
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  return (
    <div>
      <p>선택됨: {selectedIds.size}개</p>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <label>
              <input
                type="checkbox"
                checked={selectedIds.has(p.id)}
                onChange={() => toggle(p.id)}
              />
              {p.name}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

확장 과제:
- "전체 선택" / "전체 해제" 버튼을 추가한다. (전체 선택은 모든 id로 새 Set을 만들면 된다.)
- 선택된 항목만 따로 보여주는 패널을 만든다. 이때 선택된 객체를 별도 state로 두지 않고, `products.filter(p => selectedIds.has(p.id))`로 파생하라.
- 만약 1만 개짜리 리스트라면 어디가 느려질까? `selectedIds.has(p.id)`는 여전히 O(1)이지만, `<li>` 1만 개를 렌더하는 것 자체가 무겁다. 이때 등장하는 가상화(virtualization)는 본 책의 범위 밖이지만, "병목이 어디인가"를 묻는 습관을 들이자.

세 문제를 다 풀고 나면, 본 장의 원칙들이 손에 익었을 것이다. 어떤 값이 state에 들어가야 하고, 어떤 값은 그저 렌더 중에 계산되어야 하는지에 대한 감각이 생긴다.

연습 문제를 풀면서 한 가지 자세를 길러 두자. **풀어 본 코드에 대해 "이 useState 중 하나를 지울 수 있을까?" 한 번씩 묻는 자세**다. 한 번 깔끔하게 풀고 나서 그 결과물을 다시 한 번 들여다보자. 거기 또 줄일 수 있는 useState가 있는가? `useMemo`로 감싼 자리가 정말 필요한가? 한 번 더 묻고 한 번 더 줄이는 사이클을 두세 번 거치면, 그제야 그 컴포넌트가 가장 단순한 모양에 가까워진다. 좋은 코드는 단숨에 나오기보다 그렇게 여러 번 묻고 다듬는 사이에 자라난다.

또 한 가지, 위 세 문제 외에도 자기 코드베이스에서 한 컴포넌트를 골라 같은 잣대로 한 번 정리해 보길 권한다. 매일 출근해 만나는 컴포넌트가 본 장의 권유로부터 가장 큰 이득을 본다. 책의 예제는 깔끔히 정리된 미니어처지만, 실제 코드베이스의 컴포넌트는 다양한 변형이 뒤엉켜 있다. 그 뒤엉킴을 본 장의 잣대로 풀어 보면 — 처음에는 막막해도 — 한 가닥씩 풀어내는 손맛이 손에 익는다. 그 손맛이 본 장이 진짜로 남기고 가는 가르침이다.

## 2.10.5 한 단계 메타 — 왜 이 원칙들이 중요한가

연습 문제를 풀고 나면 한 가지 의문이 들 수 있다. "이 정도 차이가 정말로 그렇게 큰가?" 솔직히 말하면, 한 컴포넌트만 떼어 놓고 보면 큰 차이가 아니다. useState 다섯 개냐 두 개냐, 이게 한 컴포넌트의 운명을 가르는 일은 아니다. 그러나 코드베이스 전체로 시야를 넓혀 보면 이야기가 달라진다.

작은 코드베이스에 컴포넌트가 100개 있다고 해 보자. 그중 절반에서 useState가 평균 두 개씩 줄어들면 useState 100개가 사라진다. 그 100개가 가지던 동기화 짝, 잊을 수 있는 setX 호출, 잘못된 의존성 배열 — 그 모든 잠재 버그의 자리가 한꺼번에 사라진다. 동시에 useEffect도 함께 줄어든다. 그러면 각 컴포넌트의 첫 마운트 직후 깜빡임도 줄어들고, 개발 모드의 더블 인보케이션 때 의심해야 할 자리도 줄어든다. 코드베이스 전체의 **버그 표면적**이 한 단계 작아지는 셈이다.

이 효과는 시간이 갈수록 누적된다. 1년 뒤 새 동료가 합류했을 때, 그 동료가 코드를 읽으며 "왜 이 두 변수가 함께 갱신되어야 하지?" 같은 질문에 막히는 시간이 줄어든다. 새 기능을 추가할 때 "기존 state 중 어느 걸 다시 갱신해야 하지?"라는 점검 시간이 줄어든다. **개발 속도는 결국 인지 부하의 함수**다. 인지 부하를 낮추는 가장 단순한 길이 바로 본 장이 권한 "state를 적게"라는 한 가지 자세다.

그러니 본 장의 원칙을 한 단어로 압축하면 이렇다. **검소함.** state 설계의 검소함. 그것이 본 장이 권하는 자세이고, 책 전체가 처음부터 끝까지 권할 자세다. 다음 장으로 넘어가기 전에 이 한 단어만이라도 마음에 단단히 새겨 두자. **검소한 state 설계가 좋은 React 코드의 첫 걸음이다.**

## 2.11 마무리 — 상태의 모양이 깔끔해졌으면

본 장에서 우리는 한 가지 질문에 답해 왔다. **"무엇을 state에 두고, 무엇을 두지 말 것인가?"** 답을 한 줄로 압축하면 이렇다. **계산할 수 있으면 두지 말고, 합칠 수 있으면 합치고, 가리킬 수 있으면 ID로 가리키자.**

이 원칙들은 그저 모양이 예쁜 코드를 위한 것이 아니다. 매 렌더마다 새로 계산되는 파생값에는 동기화 버그가 살 수 없다. 한 변수에 모인 status enum에는 모순된 조합이 살 수 없다. 한 군데에만 사는 진실은 어긋날 짝이 없다. **버그가 살 수 있는 자리를 코드에서 미리 없애 두는 일**이다. 그것이 좋은 상태 설계의 본령이다.

조금 더 일상적인 언어로 말하면 이렇다. 우리는 컴포넌트를 짤 때 자주 "지금 이 시점에 화면에 보여야 하는 모든 정보"를 떠올린다. 그러고는 그 정보 하나하나를 다 useState로 적기 시작한다. 그것이 비대해지는 첫 발걸음이다. 본 장이 권한 자세는 이렇다. **먼저 다 적는다.** 그다음 그 목록을 한 번 더 훑으면서 묻는다. 이 항목은 다른 항목으로부터 계산할 수 있는가? 이 두 항목은 한 변수로 합쳐질 수 있는가? 이 객체는 ID로 줄어들 수 있는가? 이 prop은 그냥 그대로 쓸 수 있는가? 이 네 가지 질문을 통과한 항목들만 진짜 state로 남긴다. 그 결과 나오는 useState의 수가 처음 적었던 것의 절반쯤 된다면, 그게 바로 본 장이 권하는 모양이다.

이 작업을 한 줄로 요약하는 표현이 React 공식 가이드에 있다. **"Choosing the State Structure"**. state의 구조를 고르는 일이다. 단순히 "useState를 어디에 적느냐"가 아니라, "무엇을 state라는 그릇에 담을 것인가"라는 한 단계 위의 설계 결정이다. 이 설계 결정이 한 컴포넌트의 운명을 가르고, 그것이 모이면 한 코드베이스의 운명을 가른다. 그 정도로 본 장의 주제는 본질적이다. 이름은 단순한데 효과는 길고 멀다.

본 장에서 익힌 잣대가 다른 챕터에서도 거듭 등장할 것이라는 점을 미리 일러두자. 4장에서 useReducer를 다룰 때, 우리는 "action의 종류를 어떻게 가를 것인가"라는 질문을 만난다. 5장에서 Context를 다룰 때, "어디까지를 한 Provider가 책임지는가"를 묻는다. 9장에서 서버 상태를 다룰 때, "캐시는 어디에 사는가"를 묻는다. 모두 다 본질은 같다. **진실의 위치를 정한다.** 본 장이 한 컴포넌트 안에서 익힌 그 잣대가, 책 전체에 걸쳐 점점 더 큰 단위로 적용된다. 그러니 본 장은 책의 토대고, 그 토대 위에 다른 모든 장이 얹힌다.

이 자세를 한 번 익혀 두면, 나중에 더 큰 도구를 만났을 때도 같은 잣대가 통한다. useReducer를 만나면 "action의 종류는 적은가?", Context를 만나면 "이 Provider 아래에서 정말로 모두가 이 값을 알아야 하는가?", 외부 store를 만나면 "이 store가 들고 있는 값이 사실 한 군데로 모일 수 있는 것은 아닌가?" 같은 질문이 자연스럽게 따라 나온다. 도구는 바뀌지만 잣대는 같다. **state는 가능한 한 적게, 진실은 한 군데에.** 이 한 줄이 본 장이 책 전체에 남기는 말이다.

한 가지 더 짚고 가자. 본 장의 권유는 "처음부터 완벽하게 짜라"가 아니다. 처음에는 마음 가는 대로 적되, 한 번 굴려 본 뒤에 한 번씩 정리하자. 일주일에 한 컴포넌트, 한 달에 한 폴더, 그렇게 천천히 다듬어 가자. 어차피 코드는 한 번 적고 끝나는 것이 아니라 여러 번 다시 만나는 것이다. 다시 만날 때마다 한 단계씩 가벼워지면 그것으로 족하다. 한 번에 다 고치려 들면 손이 무겁고, 손이 무거우면 시작이 늦어진다. **작게 시작해서 자주 다듬자.** 그것이 본 장의 마지막 권유다.

자, 그러면 이제 다음 질문으로 넘어가자. 상태의 **모양**은 깔끔해졌다. 그렇다면 그 상태는 **어디에 살아야 할까?** 두 컴포넌트가 같은 정보를 알아야 할 때, 그 정보는 누구의 손에 들려 있어야 하는가? 너무 위로 끌어올리면 멀리 떨어진 컴포넌트까지 함께 리렌더되고, 너무 아래에 두면 다른 컴포넌트에 닿지 않는다. 적당한 자리를 찾는 것 자체가 한 가지 기술이다. Kent C. Dodds가 즐겨 쓰는 표현으로 "Lift, then Drop" — 필요할 때 끌어올리고, 필요 없어지면 다시 내린다. 그 균형 감각을 다음 장에서 함께 익혀 보자. 상태 설계의 두 번째 큰 축이다. **3장 — 상태를 어디에 둘 것인가, 끌어올림과 콜로케이션**에서 그 답을 따라가 본다.
