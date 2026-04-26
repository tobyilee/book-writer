# 3장. 상태를 어디에 둘 것인가 — 끌어올림과 콜로케이션

## 들어가는 이야기 — 두 컴포넌트가 서로의 비밀을 알아야 할 때

상상해보자. FAQ 페이지를 만들고 있다. 질문이 다섯 개쯤 나열돼 있고, 각각은 클릭하면 펼쳐지고 다시 클릭하면 접히는 평범한 아코디언이다. 처음에는 단순했다. `Panel`이라는 컴포넌트를 하나 만들고, 내부에 `isActive`라는 boolean을 `useState`로 들고 있게 했다. 펼치면 true, 접으면 false. 다섯 개를 죽 깔아두니 그럭저럭 동작했다.

그런데 기획자가 다가와 한마디 던진다. "이거, 한 번에 하나만 펼쳐졌으면 좋겠어요. 다른 거 누르면 이전에 열려 있던 건 자동으로 닫히고요." 짧은 한마디지만, 코드 입장에서는 작은 지진이다. 지금까지는 각 패널이 자기 자신의 열림/닫힘만 알면 됐다. 이제는 한 패널이 펼쳐지는 순간, 옆 친구들도 그 사실을 알아야 한다. **두 컴포넌트가 서로의 정보를 공유해야 하는 상황**이 발생한 것이다.

이 한마디 요구가 React 개발자가 가장 자주 부딪히는 순간 중 하나다. 비슷한 일은 도처에서 벌어진다. 폼 입력값을 다른 미리보기 컴포넌트가 실시간으로 보여줘야 한다. 검색창에 친 질의어가 바로 옆 결과 리스트에 반영돼야 한다. 좌측 트리에서 클릭한 노드가 우측 상세 패널에 채워져야 한다. 모두 같은 구조다 — 한 컴포넌트의 상태를 다른 컴포넌트가 봐야 한다.

이때 던져야 할 단 하나의 질문은 분명하다. "그 정보는 어디에 살아야 하는가?" 너무 낮으면 공유가 안 되고, 너무 높으면 앱 전체가 떨린다. 이번 장에서는 그 지점을 찾아가는 두 가지 도구, **끌어올리기(Lifting State Up)**와 **콜로케이션(Colocation)**을 차근차근 살펴보자. 둘은 반대 방향처럼 보이지만, 실은 같은 원칙의 양면이다. **상태는 그것이 필요한 가장 가까운 자리에 있어야 한다.** 멀어도 안 되고 가까워도 안 되는, 딱 그 자리.

---

## 끌어올리기란 무엇인가 — 두 자식의 공통 부모를 찾는 일

상태를 끌어올린다는 말은, 두 컴포넌트가 공유해야 할 정보를 그들의 **공통 부모**에 옮긴다는 뜻이다. 자식들은 더 이상 자기가 그 정보를 들고 있지 않는다. 부모가 들고 있고, props로 받아쓰며, 바꾸고 싶을 때는 부모가 건네준 콜백을 호출한다. 한 단어로 말하면 **단일 진실의 원천(Single Source of Truth)**을 만드는 작업이다.

조금 천천히 가보자. 왜 굳이 부모로 올려야 할까? 두 자식이 서로 직접 통신하면 안 될까? 그렇게 하고 싶은 마음은 이해가 간다. 하지만 React의 데이터 흐름은 단방향이다. 위에서 아래로만 흐른다. 형제끼리는 서로의 내부를 들여다볼 수 없다. 그렇다면 형제가 공유해야 할 정보는 둘이 함께 올려다보는 자리, 즉 공통 부모에 두는 것이 가장 자연스럽다. 부모는 두 자식을 동시에 내려다볼 수 있고, 양쪽에 정보를 뿌려줄 수 있다.

끌어올리기의 절차는 사실 단순하다. 단계별로 나눠서 보자.

1. **공유해야 할 상태가 무엇인지 식별한다.** 아코디언이라면 "지금 어느 패널이 활성화돼 있는가"라는 정보 하나다.
2. **자식 컴포넌트에서 그 상태를 제거한다.** `useState`를 들어내고, 대신 props로 받게 만든다.
3. **공통 부모를 찾아 거기에 `useState`를 둔다.** 두 패널이라면 두 패널을 함께 렌더하는 부모가 자리다.
4. **부모는 자식에게 현재 값과 변경 함수 두 가지를 props로 내려준다.** 보통 `value`와 `onChange`, 혹은 `isActive`와 `onShow` 같은 한 쌍이다.
5. **자식은 자기가 결정해야 할 때 그 콜백을 호출한다.** 자식은 "내가 펼쳐졌으면 좋겠어"라고 부모에게 신호만 보내고, 실제 상태 변경은 부모가 한다.

말로만 하면 와닿지 않으니 코드로 풀어보자. 먼저 끌어올리기 전, 각 패널이 자기 상태를 들고 있는 모습이다.

```tsx
// 끌어올리기 전 — 각 Panel이 isActive를 자기 안에 가지고 있다.
// 문제: 한 패널이 열려도 다른 패널은 그 사실을 모른다.
type PanelProps = { title: string; children: React.ReactNode };

function Panel({ title, children }: PanelProps) {
  // 각 인스턴스마다 독립된 isActive를 가진다.
  const [isActive, setIsActive] = React.useState(false);

  return (
    <section>
      <h3>{title}</h3>
      {isActive ? (
        <p>{children}</p>
      ) : (
        <button onClick={() => setIsActive(true)}>펼치기</button>
      )}
    </section>
  );
}

function Accordion() {
  return (
    <>
      <Panel title="React란?">선언형 UI 라이브러리다.</Panel>
      <Panel title="Hook이란?">함수 컴포넌트에서 상태와 효과를 다루는 도구다.</Panel>
    </>
  );
}
```

기획자의 요구가 들어오기 전까지는 이 코드에 아무 문제가 없다. 각 패널이 자율적이고, 부모는 패널이 어떻게 동작하는지 신경 쓸 필요도 없다. 그런데 "한 번에 하나만"이라는 요구가 들어오는 순간, 이 자율성이 갑자기 부담이 된다. 패널 A가 열렸을 때 패널 B가 열려 있는지 알 수 없으니, 닫으라고 시킬 수도 없다.

이제 끌어올려보자. 무엇을 옮길까? "지금 어느 패널이 활성인가"라는 정보가 핵심이다. 이걸 부모인 `Accordion`으로 옮기고, 패널은 자기가 활성인지를 props로 받게 바꾸자.

```tsx
// 끌어올리기 후 — Accordion이 activeIndex를 들고, 각 Panel은 props로 받는다.
type PanelProps = {
  title: string;
  isActive: boolean;        // 부모가 결정해서 내려준다.
  onShow: () => void;       // 자식은 "보여달라"고 신호만 보낸다.
  children: React.ReactNode;
};

function Panel({ title, isActive, onShow, children }: PanelProps) {
  return (
    <section>
      <h3>{title}</h3>
      {isActive ? <p>{children}</p> : <button onClick={onShow}>펼치기</button>}
    </section>
  );
}

function Accordion() {
  // 한 번에 한 패널만 활성. -1이면 전부 닫힘.
  const [activeIndex, setActiveIndex] = React.useState<number>(-1);

  return (
    <>
      <Panel
        title="React란?"
        isActive={activeIndex === 0}
        onShow={() => setActiveIndex(0)}
      >
        선언형 UI 라이브러리다.
      </Panel>
      <Panel
        title="Hook이란?"
        isActive={activeIndex === 1}
        onShow={() => setActiveIndex(1)}
      >
        함수 컴포넌트에서 상태와 효과를 다루는 도구다.
      </Panel>
    </>
  );
}
```

코드가 길어진 것처럼 보이지만, 실제로는 책임이 깨끗하게 분리됐다. `Panel`은 "내가 활성이면 본문을, 아니면 버튼을 보여준다"는 일만 한다. `Accordion`은 "어느 패널을 활성으로 둘 것인가"를 결정한다. 한 번에 하나만 열리는 동작은 `setActiveIndex(i)` 한 줄로 자연스럽게 구현됐다 — 새 인덱스가 들어오면 이전 인덱스는 자동으로 비활성이 되니까.

여기서 한 가지 짚고 넘어가자. 끌어올린 `Panel`은 더 이상 자기 상태를 갖지 않는다. 부모가 모든 걸 결정한다. 이렇게 부모가 자식의 상태를 완전히 손에 쥔 컴포넌트를 React 세계에서는 **Controlled Component(제어 컴포넌트)**라 부른다. 반대로 자기 상태를 자기가 들고 있는 원래 모습은 **Uncontrolled Component(비제어 컴포넌트)**다. 이 구분, 다음 절에서 좀 더 들여다보자.

---

## Controlled vs Uncontrolled — 누가 진실의 소유자인가

Controlled, Uncontrolled라는 용어는 React 입문자에게 가장 자주 헷갈리는 단어 쌍 중 하나다. `<input type="text" />` 이야기로 좁혀서 자주 등장하다 보니, 마치 폼 입력 전용 개념처럼 오해되기도 한다. 하지만 본질은 훨씬 일반적이다. 이 두 단어는 **상태의 소유권**에 대한 질문이다.

질문 하나를 던져보자. "이 컴포넌트가 보여주는 정보의 진짜 주인은 누구인가?" 자기 자신이라면 Uncontrolled다. 부모라면 Controlled다. 그게 전부다.

좀 더 구체적으로 보자. Uncontrolled 컴포넌트는 자기 안에 `useState`를 두고, 외부에는 결과만 통보한다. 사용하기 편하다. 부모는 별다른 신경 없이 그냥 갖다 쓰면 된다.

```tsx
// Uncontrolled 입력 — 자기 자신이 진실의 소유자다.
function NameInput({ onSubmit }: { onSubmit: (name: string) => void }) {
  const [name, setName] = React.useState("");
  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(name); }}>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <button type="submit">제출</button>
    </form>
  );
}
```

이 컴포넌트는 부모 입장에서 "그냥 갖다 붙이면 알아서 동작하는" 블랙박스다. 부모는 결과만 받으면 된다. 편하다. 그러나 **부모가 입력값을 실시간으로 알고 싶은 순간**, 이 편리함이 갑자기 벽이 된다. 미리보기를 옆에 띄우고 싶다? 입력 도중 글자 수를 카운트하고 싶다? 다른 컴포넌트와 동기화하고 싶다? 모두 이 블랙박스 안쪽을 봐야 가능한 일이고, 부모는 들여다볼 수 없다.

그래서 Controlled로 바꾼다. 자기 안의 상태를 들어내고, 부모가 결정한 값을 props로 받아 그저 화면에 비춘다. 변경 요청은 콜백으로 위임한다.

```tsx
// Controlled 입력 — 부모가 진실의 소유자다.
type NameInputProps = {
  value: string;
  onChange: (next: string) => void;
};

function NameInput({ value, onChange }: NameInputProps) {
  return <input value={value} onChange={(e) => onChange(e.target.value)} />;
}

// 부모가 상태를 들고 있고, 입력과 미리보기에 동시에 흘려준다.
function NameForm() {
  const [name, setName] = React.useState("");
  return (
    <>
      <NameInput value={name} onChange={setName} />
      <p>안녕하세요, {name || "친구"}님!</p>
    </>
  );
}
```

`NameInput`은 이제 자기 의지가 없다. 부모가 시키는 대로 비춰주고, 사용자가 뭔가 치면 그대로 부모에게 전달한다. 거의 거울에 가깝다. 이 거울 같은 단순함 덕분에, 같은 `name`을 미리보기, 글자 수, 검증 메시지, 다른 필드와의 동기화 등 어디에든 자유롭게 흘려보낼 수 있다.

요약하면 이렇다. **Uncontrolled는 자율적이지만 협력에 불리하다. Controlled는 외부에 종속적이지만 협력에 강하다.** 어느 쪽이 더 좋다는 절대적 답은 없다. 누가 그 정보의 주인이어야 하는가에 따라 갈린다.

여기서 흔한 함정 하나를 짚자. 한 컴포넌트를 Controlled와 Uncontrolled를 어정쩡하게 섞어놓는 일이 있다. 예컨대 `value` props가 들어오면 그걸 쓰고, 안 들어오면 내부 상태를 쓰는 식이다. 라이브러리를 만들 때는 의도적으로 그렇게 하기도 하지만, 일반 앱 코드에서 이 양다리는 디버깅을 정말 난감하게 만든다. **한 컴포넌트는 한 가지 모드로만 살게 하는 편이 낫다.** 둘 다 지원해야 한다면 명시적으로 두 컴포넌트로 쪼개거나, 적어도 props 타입에 그 의도를 분명히 드러내자.

---

## 끌어올리기 절차를 손에 익혀보자 — 동기화된 두 입력

아코디언만으로는 끌어올리기의 진짜 맛이 잘 안 난다. 좀 더 흔한 사례로 넘어가자. **두 입력이 같은 값을 보여줘야 하는 경우**다. 예컨대 회원가입 폼에서 닉네임을 한 번 입력했더니, 미리보기 카드에도 같은 닉네임이 즉시 반영돼야 한다고 해보자. 또는 좀 더 재미있는 예로, 섭씨와 화씨를 동시에 표시하는 온도 입력기. 한쪽을 바꾸면 다른 쪽이 즉시 환산돼 따라온다.

이 패턴은 React 공식 튜토리얼에도 나오는 고전이다. 처음에는 두 인풋을 각자 자기 상태를 들고 만들기 쉽다.

```tsx
// 끌어올리기 전 — 두 인풋이 따로 살고 있어, 한쪽 변경이 다른 쪽에 반영되지 않는다.
function CelsiusInput() {
  const [c, setC] = React.useState("");
  return (
    <label>
      섭씨 <input value={c} onChange={(e) => setC(e.target.value)} />
    </label>
  );
}

function FahrenheitInput() {
  const [f, setF] = React.useState("");
  return (
    <label>
      화씨 <input value={f} onChange={(e) => setF(e.target.value)} />
    </label>
  );
}
```

여기에 "섭씨와 화씨가 서로 동기화돼야 한다"는 요구가 들어오면, 자기 상태에 갇혀 있는 두 인풋은 협력할 방법이 없다. 끌어올리자. 무엇을 올릴까? 두 인풋이 공유할 단 하나의 진실은 결국 **온도값과 그 단위**다. 둘 다 부모로 옮긴다.

```tsx
// 끌어올린 후 — 부모가 (값, 단위)를 단일 진실로 가진다.
type Scale = "c" | "f";

function toCelsius(f: number) { return ((f - 32) * 5) / 9; }
function toFahrenheit(c: number) { return (c * 9) / 5 + 32; }

function tryConvert(value: string, convert: (n: number) => number): string {
  const n = parseFloat(value);
  if (Number.isNaN(n)) return "";
  // 소수 셋째 자리에서 반올림. 사용자가 보기에 깔끔하다.
  return (Math.round(convert(n) * 1000) / 1000).toString();
}

type TemperatureInputProps = {
  scale: Scale;
  value: string;
  onChange: (next: string) => void;
};

function TemperatureInput({ scale, value, onChange }: TemperatureInputProps) {
  return (
    <label>
      {scale === "c" ? "섭씨" : "화씨"}
      <input value={value} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}

function Calculator() {
  // 단 하나의 진실: "어떤 단위로 입력됐고, 그 값은 무엇인가".
  const [temperature, setTemperature] = React.useState("");
  const [scale, setScale] = React.useState<Scale>("c");

  const celsius = scale === "f" ? tryConvert(temperature, toCelsius) : temperature;
  const fahrenheit = scale === "c" ? tryConvert(temperature, toFahrenheit) : temperature;

  return (
    <>
      <TemperatureInput
        scale="c"
        value={celsius}
        onChange={(v) => { setScale("c"); setTemperature(v); }}
      />
      <TemperatureInput
        scale="f"
        value={fahrenheit}
        onChange={(v) => { setScale("f"); setTemperature(v); }}
      />
      <p>{parseFloat(celsius) >= 100 ? "물이 끓는다." : "아직 끓지 않았다."}</p>
    </>
  );
}
```

눈여겨볼 지점이 두 개 있다. 첫째, 부모는 두 인풋의 값을 따로 들고 있지 않다. **하나의 값과, 그 값이 어느 단위로 입력됐는가**만 들고 있다. 다른 단위로 표시할 때는 그 자리에서 환산한다. 이건 2장에서 익힌 "파생값은 state로 두지 말고 렌더 중에 계산하라"는 원칙이 그대로 적용된 예다.

둘째, 자식 입장에서 보면 둘 다 똑같은 모양이다. `value`를 받고 `onChange`를 부른다. 누가 `value`를 만드는지, 어떻게 환산되는지는 자식이 알 필요가 없다. 자식의 책임이 좁아질수록 컴포넌트는 재사용 가능해진다. 같은 `TemperatureInput`을 다른 화면에서 다른 부모와 조합해도 잘 동작할 것이다.

자, 여기서 한 걸음 떨어져서 보자. 끌어올리기를 통해 우리가 얻은 게 뭘까? 두 가지다. **(1) 진실이 한 곳에 모였다 — 더 이상 두 인풋의 값이 어긋날 수 없다.** **(2) 자식 컴포넌트들이 단순해졌다 — 자기 상태를 관리할 필요가 없으니, 그저 받은 대로 보여준다.** 좋은 거래다.

---

## 검색창과 필터된 리스트 — 어디까지 끌어올릴 것인가

또 하나의 흔한 사례. 검색창에 친 질의어로 아래의 결과 리스트를 필터링하고 싶다. 직관적으로 떠올리면 "검색창에 query state, 결과 리스트에 filtered state, 두 개 다 둬야 하지 않나?" 싶다. 하지만 잠깐 멈추자. 우리가 부모로 끌어올려야 할 단 하나의 진실은 무엇일까?

답은 **`query`만**이다. 필터된 결과는 `query`와 원본 리스트로부터 매번 만들어지는 파생값이지, 별도의 진실이 아니다. 굳이 state로 들고 있을 이유가 없다. 그러면 코드가 어떻게 되는지 보자.

```tsx
type Item = { id: number; name: string };

type SearchInputProps = {
  query: string;
  onQueryChange: (next: string) => void;
};

function SearchInput({ query, onQueryChange }: SearchInputProps) {
  return (
    <input
      type="search"
      placeholder="검색..."
      value={query}
      onChange={(e) => onQueryChange(e.target.value)}
    />
  );
}

function ResultList({ items }: { items: Item[] }) {
  if (items.length === 0) return <p>결과가 없다.</p>;
  return (
    <ul>
      {items.map((it) => <li key={it.id}>{it.name}</li>)}
    </ul>
  );
}

function SearchPage({ source }: { source: Item[] }) {
  // 끌어올린 단 하나의 진실: 사용자가 친 질의어.
  const [query, setQuery] = React.useState("");

  // 결과는 매 렌더마다 파생. 별도 state로 두지 않는다.
  const filtered = React.useMemo(
    () => source.filter((it) => it.name.toLowerCase().includes(query.toLowerCase())),
    [source, query]
  );

  return (
    <section>
      <SearchInput query={query} onQueryChange={setQuery} />
      <ResultList items={filtered} />
    </section>
  );
}
```

`useMemo`는 어디까지나 비싼 계산을 캐싱하는 도구일 뿐, 의미상으로는 그냥 매 렌더에서 다시 만드는 값이다. 실제로 리스트가 작으면 `useMemo`도 필요 없다. 그냥 `source.filter(...)` 한 줄이면 된다. 어쨌든 핵심은 — **결과 리스트는 state가 아니다.** 잊지 말자. 2장에서 다뤘듯, 두 가지 정보를 동시에 들고 있으면 둘이 어긋날 가능성이 생긴다. 어긋날 수 없게 만드는 가장 좋은 방법은, 둘 중 하나를 아예 두지 않는 것이다.

여기서 한 가지 더. 끌어올리기를 처음 익힌 사람들은 종종 과도하게 끌어올린다. "혹시 나중에 필요할지 모르니까" 싶어 미리 부모로 다 옮기는 식이다. 그 마음 충분히 이해가 간다. 하지만 그 과욕이 다음 절에서 보게 될 비극의 출발점이다.

---

## 너무 높이 끌어올렸을 때의 비극 — Prop Drilling과 리렌더 폭풍

상태를 끌어올리는 일은 분명 강력하지만, 거기에는 대가가 따른다. **상태가 위로 올라갈수록 그 영향권에 들어가는 컴포넌트의 수가 커진다.** 부모가 상태를 들고 있다는 말은, 그 상태가 바뀔 때마다 부모가 다시 렌더된다는 뜻이고, 부모가 렌더되면 그 아래 자식들도 차례로 다시 렌더된다는 뜻이다.

작은 폼에서는 이게 문제가 안 된다. 부모가 입력 필드 몇 개의 변경에 따라 다시 렌더되어도 시각적인 차이는 없다. 그러나 한 번 상상해보자. 누군가 회사 대시보드의 최상단 `App` 컴포넌트에 모든 상태를 끌어올렸다고 해보자. 사이드바 토글, 모달 열림 여부, 테이블 페이지 번호, 검색창 입력값까지 전부. 사용자가 검색창에 한 글자만 쳐도 `App` 전체가 다시 렌더된다. 그 아래에는 거대한 차트, 무거운 테이블, 복잡한 메뉴가 잔뜩 매달려 있다. **앱 전체가 한 글자에 떨린다.** 좀 끔찍한 일이다.

리렌더만 문제가 아니다. 더 일상적인 고통은 **prop drilling**이다. 상태가 5단계 위에 있는데 그걸 쓰는 컴포넌트는 5단계 아래에 있다고 해보자. 그 사이의 네 컴포넌트는 자기와 아무 상관도 없는 props를 그저 통과시키는 일만 한다. `<Layout>`은 `currentUser`를 받아서 `<MainArea>`에 넘기고, `<MainArea>`는 또 `<Section>`에, `<Section>`은 다시 `<Header>`에 넘긴다. 중간 컴포넌트들의 시그니처가 자기 일과 상관없는 prop들로 도배된다. 한 줄 추가할 때마다 네 곳을 손대야 한다. 번거롭다. 정말 번거롭다.

이 두 비극이 모두 같은 원인에서 나온다. **상태를 필요 이상으로 높이 올린 것.** 그래서 우리는 끌어올림과 짝을 이루는 반대 기술을 함께 익혀야 한다. 바로 **콜로케이션**이다.

---

## "Lift, then Drop" — 필요 없으면 다시 내린다

Kent C. Dodds는 "State Colocation will make your React app faster"라는 글에서 이 원칙을 또렷하게 정리했다. **상태는 그것을 사용하는 컴포넌트와 가장 가까운 곳에 둬라.** 그리고 그가 덧붙인 한 문장이 이 장의 후반부를 관통한다.

> "Lift state only as high as necessary. If lifted too high, push it back down."

말 그대로다. 필요한 만큼만 끌어올리고, 너무 높이 올라간 것 같으면 다시 내려라. 이걸 두 단계 절차로 외워두자. **Lift, then Drop.** 일단 끌어올린다. 그리고 시간이 지나 정말 그 위치가 옳았는지 점검한다. 사용처가 줄어들었거나, 처음부터 한 컴포넌트만 그 상태를 쓰고 있었다면, 도로 그 컴포넌트로 내려준다.

콜로케이션이 왜 중요한지를 두 가지 측면에서 살펴보자.

**첫째, 성능이다.** 상태가 낮은 곳에 있으면 그 변경의 영향권이 좁다. 검색창 입력값이 검색창 컴포넌트 안에만 있다면, 그 한 글자에 떨리는 것도 검색창과 그 직접 자식뿐이다. 위에 있는 사이드바, 차트, 테이블은 미동도 하지 않는다. 같은 코드, 같은 기능인데 체감 성능이 달라진다.

**둘째, 가독성이다.** 코드를 읽는 사람은 보통 어떤 컴포넌트를 보고 있을 때 그 컴포넌트의 동작이 궁금하다. 그 동작에 영향을 주는 상태가 같은 파일, 같은 함수 안에 있으면 한 화면 안에서 이해가 끝난다. 상태가 5단계 위에 있다면 머릿속이 곧장 거기로 점프해야 한다. 별것 아닌 것 같지만, 이런 점프가 쌓이면 코드 베이스 전체의 인지 비용이 무거워진다.

콜로케이션의 실천은 단순한 규칙으로 환원된다. **이 상태를 진짜로 쓰는 컴포넌트가 누구인지 세보자.** 정확히 한 군데라면, 그 한 군데로 내려라. 두 군데 이상이고 그 둘의 공통 부모가 명확하다면, 그 공통 부모까지만 올려라. 더 이상은 아니다.

작은 예를 보자. 큰 페이지 안 어딘가에 "더 보기" 토글이 있다고 해보자. 처음에는 `Page`에서 관리하고 있었다.

```tsx
// Before — 토글 상태가 너무 높이 올라가 있다.
function Page() {
  const [showDetails, setShowDetails] = React.useState(false);
  // ... 페이지의 다른 거대한 영역들 ...
  return (
    <>
      <Header />
      <BigChart />
      <BigTable />
      <DetailsToggle
        show={showDetails}
        onToggle={() => setShowDetails((v) => !v)}
      />
      {showDetails && <Details />}
    </>
  );
}
```

뭐가 문제일까? `showDetails`가 바뀔 때마다 `Page`가 다시 렌더되고, 그 안의 `Header`, `BigChart`, `BigTable`까지 함께 휘말린다. 그런데 사실 `showDetails`를 쓰는 곳은 `DetailsToggle`과 `Details`뿐이다. 그렇다면 그 둘만 묶는 작은 컴포넌트로 내리자.

```tsx
// After — 토글 상태를 그것을 쓰는 작은 영역으로 내렸다.
function DetailsSection() {
  const [show, setShow] = React.useState(false);
  return (
    <>
      <button onClick={() => setShow((v) => !v)}>
        {show ? "접기" : "더 보기"}
      </button>
      {show && <Details />}
    </>
  );
}

function Page() {
  return (
    <>
      <Header />
      <BigChart />
      <BigTable />
      <DetailsSection />
    </>
  );
}
```

코드가 짧아지고, 의미가 또렷해지고, 토글 한 번에 떨리는 영역도 좁아졌다. **"이 상태가 정말 이 자리에 있어야 하는가?" 한 번씩 자문하는 습관**이 콜로케이션의 출발점이다.

---

## 끌어올림 vs Context — 갈림길에 서서

상태를 어디에 둘 것인가에 대한 답이 단순한 끌어올리기로 늘 풀리는 건 아니다. 가끔은 **공통 부모가 너무 멀리 있다**. 예컨대 테마, 로그인 사용자, 언어 설정처럼 앱 거의 모든 곳에서 쓰이는 정보들. 이들을 끌어올리면 결국 `App` 최상단까지 올라가고, 그 아래 모든 컴포넌트는 자기와 상관없는 props를 끝없이 통과시키게 된다. 이때 등장하는 도구가 **Context**다.

지금 단계에서는 이 정도만 기억해두자. **Context는 "props로 내리기엔 너무 깊지만, 정말로 여러 곳에서 봐야 하는 정보"를 위한 도구다.** Lift, Drop의 다음 단계, 즉 5장과 6장에서 본격적으로 다룬다.

여기서 미리 던질 경고가 하나 있다. Kent C. Dodds가 거듭 강조하는 말이다. **"Don't reach for context too soon."** Context를 너무 빨리 꺼내지 말자. 끌어올리기로 풀 수 있는 문제를 Context로 풀면, 콜로케이션의 가능성이 사라진다. Context로 감싼 영역 안의 모든 컴포넌트는 그 값에 묶이고, 값이 바뀌면 그 영역 전체가 영향을 받는다. **Context는 강력한 도구지만, 가벼운 도구가 아니다.** 가능한 한 끌어올리기와 콜로케이션의 짝패로 풀어보고, 그게 정말 통하지 않을 때만 Context를 검토하자.

---

## children 합성 — 끌어올리지 않고도 공유하는 또 하나의 길

상태 공유가 필요해 보이는데, 가만히 보면 사실 **레이아웃만 공유하는** 경우가 있다. 이때는 끌어올리기가 아니라 **children 합성**이라는 다른 경로를 검토해볼 만하다. 아주 간단한 예를 보자.

```tsx
// Before — Layout이 자식 컴포넌트에 대해 너무 많이 안다.
function Layout({ user }: { user: User }) {
  return (
    <div className="layout">
      <Sidebar user={user} />
      <MainArea user={user} />
    </div>
  );
}
```

`Layout`이 `user`를 받아 두 자식에게 내려준다. 그런데 `Layout`은 사실 `user`라는 게 뭔지 알 필요가 없다. 그저 사이드바 자리와 본문 자리를 가진 레이아웃일 뿐이다. 자식을 직접 받는 형태로 바꿔보자.

```tsx
// After — Layout은 자리만 제공한다. 누가 user를 알지는 호출자가 결정.
function Layout({ sidebar, main }: { sidebar: React.ReactNode; main: React.ReactNode }) {
  return (
    <div className="layout">
      {sidebar}
      {main}
    </div>
  );
}

function Page({ user }: { user: User }) {
  return (
    <Layout
      sidebar={<Sidebar user={user} />}
      main={<MainArea user={user} />}
    />
  );
}
```

`Layout`은 `user`를 모르고도 잘 산다. `user`는 `Page` 안에서 한 번만 다뤄지고, 자식들은 `Page`로부터 직접 받는다. **중간에 끼어 props를 단순 전달만 하는 컴포넌트를 줄여주는 패턴**이다. 이 합성 패턴은 5장에서 더 깊게 다룬다. 지금은 "끌어올리기와 Context 사이에 합성이라는 제3의 길이 있다"는 점만 알아두면 충분하다.

---

## 의사결정 체크리스트 — 상태를 어디에 둘지 정할 때

여기까지 오면, 머릿속에 약간의 혼란이 생길 수 있다. 끌어올려야 하나? 내려야 하나? Context는? 합성은? 정리해두자. 새로운 상태를 만들 때, 또는 기존 상태의 위치가 찜찜할 때, 다음 다섯 질문을 차례로 던져보자.

1. **이 상태를 진짜로 사용하는 컴포넌트는 몇 개인가?**
   - 정확히 한 군데라면, 그 컴포넌트 안에 둔다. 끝.
   - 두 군데 이상이라면 다음 질문으로.
2. **그 둘(또는 그 이상)의 공통 부모는 어디인가?**
   - 가장 가까운 공통 부모가 자리다. 그보다 위로 올리지 마라.
3. **그 상태가 바뀔 때, 정말로 함께 다시 렌더돼야 할 영역이 어디까지인가?**
   - 영향권이 넓을수록 위에 둔 대가가 크다. 좁힐 수 있으면 좁히자.
4. **공통 부모가 너무 멀어 props 전달이 4~5단계 이상 지나가게 되는가?**
   - 그렇다면 children 합성으로 중간 컴포넌트를 우회할 수 있는지 먼저 본다. 그래도 안 되면 Context를 검토한다.
5. **이게 사실 파생값은 아닌가?**
   - 다른 state나 props로부터 매번 계산할 수 있다면 state로 두지 말자. 끌어올림조차 필요 없다.

이 다섯 질문은 시간이 지나도 또 던져야 한다. 처음 끌어올렸을 때 옳았던 위치가 6개월 뒤에는 너무 높아져 있을 수 있다. 사용처가 한 군데로 줄어 있는데도 여전히 부모에 매달려 있을 수 있다. **상태의 자리는 한 번 결정하면 끝나는 것이 아니라, 계속 돌보는 것**이다. 코드 리뷰 때, 리팩토링할 때, 그리고 무엇보다 새 기능을 추가할 때, 한 번씩 자문하는 습관을 들이자.

---

## 흔한 안티패턴 — 모든 state를 위로 올리는 만행

마지막으로 한 가지 흔한 함정을 짚자. 어떤 팀들은 일관성이라는 이름으로 모든 상태를 최상단 가까이 끌어올리는 규칙을 채택한다. 그러면 "상태가 어디 있는지 헤매지 않아도 된다"는 장점은 있다. 그러나 그 대가는 크다.

- 작은 변경 하나에 거대한 영역이 다시 렌더된다.
- 중간 컴포넌트가 자기와 무관한 props로 도배된다.
- 컴포넌트 재사용이 어려워진다 — 다른 자리에 옮기려 해도 부모의 상태에 묶여 있다.
- 파일 한 개가 거대해진다.

이게 바로 콜로케이션이 막아주는 만행이다. **상태에는 영향권이 있고, 영향권은 그것을 진짜로 쓰는 곳까지여야 한다.** 그 이상은 비용이다. 일관성은 분명 미덕이지만, 잘못된 일관성은 그저 모든 자리에 같은 흠을 새기는 일과 다르지 않다.

반대로 너무 콜로케이션에 집착해 두 형제가 공유해야 할 정보를 끝까지 안 끌어올리는 것도 곤란하다. 그러면 형제끼리 신호를 주고받기 위해 effect를 동원하거나, 부모를 우회하는 이상한 패턴이 생긴다. 이 역시 별도의 안티패턴이다(11장에서 본격 처방한다). **끌어올림과 콜로케이션은 둘 다 필요한 짝꿍**이다. 한쪽만 강조하면 균형을 잃는다.

---

## 핵심 정리

지금까지 살펴본 내용을 압축해두자.

1. 두 컴포넌트가 같은 정보를 알아야 할 때, 그 정보는 **두 컴포넌트의 가장 가까운 공통 부모**에 둔다. 이것이 끌어올리기의 본질이다.
2. 끌어올린 상태는 자식에게 **현재 값과 변경 함수** 두 가지로 props를 통해 내려간다. 자식은 변경할 때 콜백을 부른다.
3. **Controlled 컴포넌트**는 자기 상태를 안 가지고 부모가 시키는 대로 비춘다. **Uncontrolled 컴포넌트**는 자기 상태를 가진다. 둘의 차이는 "누가 진실의 소유자인가"이며, 한 컴포넌트가 두 모드를 어정쩡하게 섞으면 디버깅이 난감해진다.
4. 두 컴포넌트가 동기화돼야 한다고 해서 두 개의 state를 둘 필요는 없다. **단 하나의 진실**과 **그것을 변환하는 파생값**으로 표현할 수 있는 경우가 많다.
5. 상태를 너무 높이 끌어올리면 **앱 전체 리렌더**와 **prop drilling**이라는 두 비극이 따라온다. Lift, then Drop을 잊지 말자.
6. **콜로케이션**은 상태를 그것을 사용하는 컴포넌트 가까이 두는 원칙이다. 사용처가 정확히 한 군데라면, 그 자리로 내린다.
7. 끌어올리기로도 풀리지 않을 만큼 멀리 떨어진 컴포넌트들이 정보를 공유해야 한다면 **Context**를 검토한다. 그러나 너무 빨리 꺼내지 말자.
8. **children 합성**은 끌어올리기와 Context 사이의 제3의 길이다. 중간 컴포넌트가 단순 전달만 한다면 합성으로 우회할 수 있다.
9. 새로운 상태를 만들 때마다 다섯 질문을 던지자 — **사용처는 몇 개인가, 공통 부모는 어디인가, 영향권은 어디까지인가, props 전달이 너무 깊어지지는 않는가, 사실 파생값은 아닌가**.
10. 상태의 자리는 한 번 결정하면 끝이 아니라 **계속 돌보는 것**이다. 코드 베이스가 자라면서 자리도 함께 돌봐야 한다.

---

## 연습 문제

손에 익혀야 진짜 이해다. 세 문제를 풀어보자.

### [기초] 두 입력의 합 표시 — 부모로 끌어올리기

다음 코드는 두 입력이 각자 자기 상태를 들고 있다. `App`에서 두 값의 합을 함께 보여주려면 어떻게 바꿔야 할까? 끌어올림을 적용해보자.

```tsx
function NumberInput() {
  const [n, setN] = React.useState(0);
  return (
    <input
      type="number"
      value={n}
      onChange={(e) => setN(Number(e.target.value))}
    />
  );
}

function App() {
  return (
    <>
      <NumberInput />
      <NumberInput />
      {/* 여기서 두 값의 합을 보여주고 싶다. 어떻게 할까? */}
    </>
  );
}
```

**힌트.** 자식의 `useState`를 들어내고 props로 받게 만든다. 부모가 두 숫자를 함께 들고, 합은 파생값으로 계산한다. 두 입력은 형제이므로 둘의 공통 부모는 `App`이다.

### [중] 검색창 + 결과 리스트 — 어디까지 끌어올릴 것인가

상품 리스트에 검색창을 붙이려 한다. 다음 두 가지 후보 설계 중 어느 쪽이 옳을까? 둘의 차이를 직접 코드로 짜보고 비교해보자.

- **설계 A.** `query`와 `filteredProducts`를 모두 부모 state로 둔다. 검색어가 바뀔 때마다 setter로 둘 다 갱신한다.
- **설계 B.** `query`만 부모 state로 두고, `filteredProducts`는 매 렌더에서 `products.filter(...)`로 파생한다.

**힌트.** 설계 A는 두 state가 동기화되지 않을 위험을 안고 있고, 설계 B는 그 위험 자체를 없앴다. 어느 쪽이 콜로케이션 원칙과 더 잘 맞는지 생각해보자. 그리고 한 걸음 더 — 만약 검색 결과가 **이 페이지의 한 컴포넌트에서만 쓰인다면**, `query` state는 진짜로 부모까지 올라가야 할까, 아니면 그 한 컴포넌트 안에 머물러도 될까?

### [도전] 끌어올린 state를 다시 콜로케이션

다음 코드는 처음에는 두 자식이 `count`를 공유해야 했지만, 시간이 지나 한 자식만 `count`를 쓰는 상황으로 바뀌었다. 그런데도 `count`가 여전히 부모에 남아 있다. 이를 발견했다고 가정하고, **Drop**을 적용해보자.

```tsx
function Display({ count }: { count: number }) {
  return <p>현재: {count}</p>;
}

function Controls({ count, onIncrement }: { count: number; onIncrement: () => void }) {
  // 사실 여기는 count를 표시 안 하고, 그저 increment 버튼만 둔다.
  return <button onClick={onIncrement}>+1</button>;
}

function Page() {
  // count는 사실 Display만 보여주고 있다. Controls는 onIncrement만 있으면 된다.
  const [count, setCount] = React.useState(0);
  return (
    <>
      <Display count={count} />
      <Controls count={count} onIncrement={() => setCount((c) => c + 1)} />
    </>
  );
}
```

**힌트.** `Display`와 `Controls`를 묶는 작은 컴포넌트를 만들고, 그 안에서 `count`를 들게 한다. 그렇게 하면 `Page`는 `count`를 몰라도 된다. 한 단계 더 — `Controls`의 `count` prop은 정말 필요한가? 안 쓰는 prop은 시그니처에서 떼어내자. **사용하지 않는 prop은 거짓말이다.** 받는 척 하면서 안 쓰는 것보다, 안 받는 게 정직하다.

---

## 다음 장으로의 다리

이번 장에서는 **상태가 어느 자리에 살아야 하는가**라는 질문을 가지고 끌어올림과 콜로케이션 사이를 오가며 답을 찾아봤다. 그 자리는 너무 낮으면 공유가 안 되고, 너무 높으면 앱이 떨린다. 그 사이의 정확한 지점을 찾아 두는 게 우리의 일이다.

그러면 다음 질문은 자연스럽게 이렇게 이어진다. **자리는 잘 잡아뒀다. 그런데 같은 자리에 다른 사람이 들어오면 어떻게 되는가?** 예컨대 채팅 화면에서 상대를 바꿨더니 이전 상대에게 쓰던 초고가 그대로 남아 있다면? 같은 `<Chat>` 컴포넌트인데, React는 그게 "다른 컴포넌트"라는 걸 어떻게 알까? 알아챌 수 있을까?

여기서 등장하는 것이 React의 정체성 규칙과 `key`라는 프로퍼티다. 4장에서는 끌어올리기와 콜로케이션으로 잘 자리잡은 상태를 **언제 보존하고 언제 리셋해야 하는지**, 그리고 그 결정을 React에게 어떻게 알려야 하는지를 살펴보자. 끌어올리는 법을 알았으니, 반대로 "강제로 처음으로 되돌리는 법"도 손에 익혀야 한다.
