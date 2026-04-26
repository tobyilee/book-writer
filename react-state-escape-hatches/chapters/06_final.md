# 6장. Context — prop drilling이 진짜 고통일 때

작은 회의실에 일곱 명이 한 줄로 서 있다고 상상해보자. 맨 끝 사람에게 전달해야 할 메모가 있다. 그런데 사이에 서 있는 다섯 명은 그 내용에 관심이 없다. 이름도 모르고, 무슨 뜻인지도 모르고, 자기 일과는 아무 상관이 없다. 그런데도 손에서 손으로 메모를 받아 옆 사람에게 넘겨야 한다. 두 번 정도는 괜찮다. 세 번째쯤에는 누군가 한숨을 쉬고, 네 번째쯤에는 메모가 살짝 구겨진다. 다섯 번째에 이르면, 사이에 끼어 있는 사람들이 진심으로 짜증을 낸다. "이거 왜 내가 들고 있어야 하지?"

리액트로 컴포넌트 트리를 짜다 보면, 정확히 이 풍경을 코드로 마주하게 된다. `App`이 사용자 정보를 읽어서 어딘가 깊숙이 숨어 있는 `Avatar`에 내려줘야 하는데, 그 사이에 `Layout`, `Sidebar`, `ProfileSection`, `ProfileCard`, `ProfileHeader` 같은 컴포넌트들이 줄지어 있다. 이 중간 컴포넌트들은 사용자 정보를 쓰지 않는다. 그저 받아서 자식에게 넘겨줄 뿐이다. 이 광경을 한 번이라도 코드로 적어본 사람이라면, "번거롭다"는 말로는 부족한 무언가를 느끼게 된다. 줄을 따라 메모를 7번 패스하는 회의실의 짜증이, 코드 리뷰어의 마음에 그대로 옮겨 앉는다.

이 장에서는 그 짜증을 다룬다. 정확히 말하면, 그 짜증을 어떻게 진단하고, 언제 Context로 끊어내고, 언제는 그냥 두는 것이 나은지를 살펴보자. Context는 분명 강력한 도구다. 그러나 강력한 도구가 늘 그렇듯, 너무 일찍 손을 대면 코드가 오히려 어수선해진다. "Don't reach for context too soon"이라는 말은 그래서 나왔다. 이 말의 진짜 의미를 함께 풀어보자.

## prop drilling은 언제 진짜 고통이 되는가

먼저 한 가지 질문에 솔직하게 답해보자. prop을 두세 단계 내려보내는 것이 그렇게 끔찍한 일인가? 사실 그렇지 않다. 두 단계 깊이의 prop 패스는 코드를 읽는 사람에게 친절한 단서를 남긴다. "이 값은 부모에서 왔고, 자식이 쓴다." 이 흐름이 한눈에 보인다. props로 내려가는 데이터는 추적이 쉽다. 어디서 왔는지, 어디로 가는지가 코드만 봐도 명확하다.

그러니 prop drilling을 무조건 적이라고 치부하지는 말자. 다음과 같은 패턴은 그대로 둬도 충분하다.

```tsx
// 두 단계 정도의 패스 — 별로 고통스럽지 않다
function ProductPage({ product }: { product: Product }) {
  return <ProductDetail product={product} />;
}

function ProductDetail({ product }: { product: Product }) {
  return <ProductImage src={product.imageUrl} alt={product.name} />;
}
```

이 정도는 "drilling"이라고 부르기에도 어색하다. 그런데 다음과 같은 코드를 보면 어떨까?

```tsx
// 정말 고통스러운 패스 — 중간 어디에도 currentUser를 쓰는 곳이 없다
function App({ currentUser }: { currentUser: User }) {
  return <Layout currentUser={currentUser} />;
}

function Layout({ currentUser }: { currentUser: User }) {
  return (
    <div>
      <Sidebar currentUser={currentUser} />
      <Main currentUser={currentUser} />
    </div>
  );
}

function Sidebar({ currentUser }: { currentUser: User }) {
  return <ProfileSection currentUser={currentUser} />;
}

function ProfileSection({ currentUser }: { currentUser: User }) {
  return <ProfileCard currentUser={currentUser} />;
}

function ProfileCard({ currentUser }: { currentUser: User }) {
  return <ProfileHeader currentUser={currentUser} />;
}

function ProfileHeader({ currentUser }: { currentUser: User }) {
  return <Avatar src={currentUser.avatarUrl} />;
}
```

여기에는 `Layout`도 `Sidebar`도 `ProfileSection`도 `ProfileCard`도 `currentUser`를 직접 쓰지 않는다. 그저 받아서 넘긴다. 그런데도 이 다섯 컴포넌트의 타입 정의에 `currentUser: User`가 들어가 있어야 한다. 어느 날 `User` 타입이 바뀌면 다섯 곳을 동시에 수정해야 한다. 새 prop을 하나 더 내려보내야 하면 다섯 곳을 또 손대야 한다. 이쯤 되면 슬슬 찜찜해진다.

prop drilling이 진짜 고통이 되는 순간은 다음 조건이 모두 맞을 때다.

- **깊이가 깊다.** 4단계 이상이 흔하다.
- **중간 컴포넌트가 그 prop을 쓰지 않는다.** 단순 통과만 한다.
- **그 prop이 곧잘 추가되거나 바뀐다.** 한 번만 쓰고 끝나는 것이 아니라, 새로운 사용자 정보 필드가 자꾸 더해지는 식이다.
- **여러 자식이 같은 값을 쓴다.** `Avatar` 하나만이 아니라, 트리 곳곳에서 `currentUser`를 읽어야 한다.

이 네 가지 조건을 모두 만족하지 않는다면, Context를 꺼내기 전에 한 번 더 멈추는 편이 낫다. 두세 단계의 패스는 견딜 만하고, 오히려 코드 흐름을 명료하게 보여주는 장점도 있다. drilling은 깊고, 무관하고, 자주 바뀌고, 광범위할 때 비로소 진짜 고통이 된다.

조금 더 솔직히 말해보자. drilling이라는 단어가 너무 부정적인 어감이라 우리를 자극하는 면도 있다. "내가 prop drilling을 하고 있다"는 말은 곧 "내가 안티패턴을 쓰고 있다"는 자책처럼 들린다. 그래서 우리는 그 단어를 보자마자 무언가 손을 대려고 한다. 그러나 prop을 명시적으로 내려보내는 행위 자체는 죄가 아니다. 오히려 컴포넌트 인터페이스를 명확하게 만들어 주는 미덕이다. "이 컴포넌트는 어떤 데이터에 의존하는가?"라는 질문에, 컴포넌트의 시그니처를 보면 즉시 답이 나오기 때문이다. drilling이 죄가 되는 순간은 의존하지도 않는 데이터를 끼고 있어야 할 때, 즉 시그니처가 거짓말을 시작할 때다. "이 컴포넌트는 `currentUser`에 의존한다"고 타입이 말하지만 실제로 코드에서는 그저 자식에게 패스하기만 한다면, 그 시그니처는 거짓말이다. 그 거짓말이 다섯 컴포넌트에 걸쳐 반복될 때, 우리는 진짜 고통을 느낀다.

이 관점을 가지면 판단 기준이 한층 또렷해진다. 시그니처가 정직하면 그대로 두자. 시그니처가 거짓말을 하기 시작하면 그때 손을 대자. Context는 거짓말을 거두기 위한 도구지, drilling이라는 단어 자체에 대한 알레르기 반응이 아니다.

## Context의 본질 — "이 트리 안에서 사용할 수 있는 값"

Context를 도입할 마음이 들었다면, 먼저 Context의 본질을 한번 정확히 정리하고 가자. 많은 사람이 Context를 "전역 변수의 리액트 버전" 정도로 이해한다. 이 비유는 절반만 맞다.

Context는 전역이 아니다. **Provider로 감싼 트리의 일부 구간 안에서만 유효한 값**이다. 트리 어디서든 `useContext(MyContext)`를 호출하면, 그 컴포넌트 위쪽에서 가장 가까운 `<MyContext value={...}>`가 제공한 값을 받게 된다. Provider가 트리에 없다면 `createContext`에 적은 기본값이 쓰인다. 즉 Context는 "이 트리 구간 안에서 사용할 수 있는 값"이라는 영역 개념을 가진다.

이 영역 개념이 왜 중요할까? 왜 Provider를 트리 깊숙이 둬서 영향 범위를 좁히라는 조언이 있는지 살펴보자.

```tsx
// Provider를 굳이 App 최상단까지 끌어올리지 않아도 된다
function App() {
  return (
    <Layout>
      <PostsSection>
        <LevelProvider value={1}>
          <Heading>안녕하세요</Heading>
          <Post>
            <Heading>오늘의 이야기</Heading>
          </Post>
        </LevelProvider>
      </PostsSection>
      <CommentsSection>
        {/* 여기는 LevelProvider 영향을 받지 않는다 */}
      </CommentsSection>
    </Layout>
  );
}
```

`LevelProvider`는 `PostsSection` 안에서만 의미가 있다. `CommentsSection`까지 영향을 끼칠 이유가 없다. Provider를 필요한 자리에 가까이 두는 것을 **콜로케이션(colocation)** 이라고 한다. 이렇게 두면 두 가지 좋은 일이 생긴다. 첫째, 영향 범위가 좁아져서 코드를 읽는 사람이 "이 값은 이 영역에서만 쓰이는구나"를 한눈에 본다. 둘째, value가 바뀔 때 리렌더되는 컴포넌트가 그 영역 안으로만 한정된다. 리렌더 비용이 줄어든다.

그렇다면 어떤 값이 Context에 어울릴까? 경험에서 추려본 후보를 살펴보자.

- **테마(라이트/다크)** — 자주 바뀌지 않고, 트리 전체가 영향을 받는다.
- **로그인 사용자 정보** — 한 세션에서 한 번 정해지면 거의 안 바뀐다.
- **로케일/언어 설정** — 마찬가지.
- **라우팅 정보** — 라우터 라이브러리가 내부적으로 Context를 쓴다.
- **트리 깊이 같은 구조 정보** — `LevelContext`처럼, 자기 위치를 자식에게 알려주는 용도.

공통점이 보일 것이다. **정적이거나 준정적인 값**, 그리고 **트리의 여러 자식이 동시에 필요로 하는 값**. 이 두 조건에 맞을 때 Context는 빛난다. 반대로 1초에 수십 번 바뀌는 마우스 좌표나, 매 키 입력마다 갱신되는 폼 값을 Context에 넣으면 어떻게 될까? 잠시 후에 그 끔찍한 결과를 살펴보자.

여기서 한 가지 짚어두자. "정적"이라는 말이 "절대 변하지 않는다"라는 뜻은 아니다. 로그인 사용자 정보도 로그아웃하면 바뀌고, 테마도 사용자가 토글하면 바뀐다. 그러나 그 빈도가 분당 수십 번이 아니다. 한 세션에 몇 차례, 길어야 한 자릿수 정도다. 이 정도 빈도라면 모든 consumer가 한 번씩 다시 그려져도 사용자가 알아채지 못한다. 그래서 "준정적"이라는 표현이 더 정확하다. **변화가 드물고, 변화 시점이 사용자 행동에 묶여 있는 값.** 이런 값이 Context의 가장 좋은 손님이다.

반대편 극단도 살펴보자. 마우스 좌표, 스크롤 위치, 매 키 입력의 입력란 값. 이런 값은 자주 바뀐다. 매우 자주 바뀐다. 그리고 종종 한 컴포넌트만 그 값을 정말로 필요로 한다. 트리 깊은 곳에 있는 50개 컴포넌트가 그 값을 동시에 보고 있을 이유가 별로 없다. 이런 값은 Context에 들어갈 자격이 없다. 가까운 곳에 두자. 정 멀리서 봐야 한다면, selective subscription을 가진 도구를 쓰자.

## createContext, Provider, useContext — 기본 사용법

이제 본격적으로 코드를 써보자. `LevelContext`를 예로 든다. `Section` 컴포넌트가 자기 위에 있는 `Section`의 level을 받아 +1 해서 자식에게 내려주고, `Heading`은 그 level을 읽어 적절한 HTML 태그(`h1`~`h6`)를 출력하는 시나리오다. prop drilling으로 풀려면 `Section`마다 `level` prop을 손으로 적어야 한다. Context로 풀면 `Section`이 알아서 자기 위 level을 읽고, +1해서 다시 내린다.

```tsx
// LevelContext.tsx
import { createContext, useContext, ReactNode } from "react";

// 1. Context 생성. 기본값은 0(아직 어떤 Section에도 들어가지 않은 상태)
const LevelContext = createContext<number>(0);

// 2. Section: 자기 위 level을 읽고, +1해서 Provider로 다시 내린다
export function Section({ children }: { children: ReactNode }) {
  const level = useContext(LevelContext);
  return (
    <section className="section">
      <LevelContext value={level + 1}>{children}</LevelContext>
    </section>
  );
}

// 3. Heading: 현재 level을 읽고 그에 맞는 태그를 출력한다
export function Heading({ children }: { children: ReactNode }) {
  const level = useContext(LevelContext);
  switch (level) {
    case 0:
      throw new Error("Heading은 반드시 Section 안에 있어야 합니다");
    case 1:
      return <h1>{children}</h1>;
    case 2:
      return <h2>{children}</h2>;
    case 3:
      return <h3>{children}</h3>;
    case 4:
      return <h4>{children}</h4>;
    case 5:
      return <h5>{children}</h5>;
    default:
      return <h6>{children}</h6>;
  }
}
```

사용하는 쪽은 이제 깔끔하다.

```tsx
function Page() {
  return (
    <Section>
      <Heading>제목</Heading>
      <Section>
        <Heading>부제목</Heading>
        <Section>
          <Heading>소제목</Heading>
        </Section>
      </Section>
    </Section>
  );
}
```

`Section`을 중첩할수록 `Heading`이 자동으로 `<h1>`, `<h2>`, `<h3>`로 바뀐다. `level` prop을 손으로 적은 곳은 어디에도 없다. 중간 컴포넌트가 prop을 통과시킬 의무에서 해방됐다. drilling 7단계가 사라졌다.

여기서 잠깐 짚을 점이 두 가지 있다. 첫째, 리액트 19부터는 `<MyContext.Provider>` 대신 `<MyContext>`로 바로 쓸 수 있다. 코드가 한결 가벼워졌다. 둘째, `createContext<number>(0)`처럼 제네릭으로 타입을 지정하는 방식이 타입스크립트에서는 표준이다. 기본값을 어떻게 정할지가 곧 다음 절의 주제다.

조금 더 자세히 동작 원리를 따라가 보자. `useContext(LevelContext)`가 호출되면, 리액트는 그 컴포넌트 위쪽으로 트리를 거슬러 올라가며 가장 가까운 `<LevelContext value={...}>`를 찾는다. 발견하면 그 `value`를 반환한다. 발견하지 못하면 `createContext`에 넘긴 기본값을 반환한다. 이 과정이 컴포넌트가 렌더될 때마다 일어난다. 그래서 새 Provider가 트리에 끼어들거나 빠지면, 그 아래 consumer는 다음 렌더에서 바로 새 값을 본다.

그리고 `Section`이 자기 자신도 `useContext`를 호출하고 있다는 점에 주목해보자. 부모 `Section`이 1을 내려줬다면, 자식 `Section`은 그 1을 읽고 +1해서 2를 다시 내린다. 즉 같은 Context가 트리를 따라 자기 자신을 점진적으로 변형해 가는 셈이다. 이런 식으로 "트리 깊이"라는 위치 정보를 자식에게 자연스럽게 전달할 수 있다. drilling이라면 매 `Section`이 부모로부터 받은 `level`을 +1해서 자식에게 다시 prop으로 내려야 했는데, Context가 그 무거운 짐을 가져갔다.

## 기본값(default value)을 어떻게 정할 것인가

`createContext`에 넘기는 값이 무엇이어야 할지를 두고 의외로 자주 망설인다. 두 가지 큰 길이 있다.

**길 1. `null` 또는 `undefined`로 만들고, 훅에서 가드한다.** 가장 자주 보이는 패턴이다. "Provider 없이 이 값을 쓰는 것은 버그"라고 단언할 때 적합하다.

```tsx
// AuthContext.tsx
import { createContext, useContext, ReactNode, useState } from "react";

interface AuthValue {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// 기본값은 null. Provider 밖에서 쓰면 즉시 에러
const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  async function login(email: string, password: string) {
    const result = await api.login(email, password);
    setUser(result.user);
  }

  function logout() {
    setUser(null);
  }

  return (
    <AuthContext value={{ user, login, logout }}>{children}</AuthContext>
  );
}

// 커스텀 훅으로 가드를 한곳에 모은다
export function useAuth(): AuthValue {
  const value = useContext(AuthContext);
  if (value === null) {
    throw new Error("useAuth는 AuthProvider 안에서만 사용할 수 있습니다");
  }
  return value;
}
```

이 패턴의 장점은 명확하다. Provider를 깜빡 잊고 `useAuth`를 호출하면, 컴포넌트 어디서 호출했든 즉시 에러 메시지가 뜬다. 디버깅이 쉽다. 반환 타입에 `null`이 없으니 호출하는 쪽에서 매번 가드할 필요도 없다.

**길 2. 의미 있는 디폴트를 준다.** "Provider가 없어도 그럭저럭 돌아가야 한다"고 판단할 때 쓴다. 예를 들어 테마는 라이트가 기본이라고 정해두면, 굳이 Provider를 두지 않아도 컴포넌트가 어색하지 않게 동작한다.

```tsx
// ThemeContext.tsx
import { createContext, useContext, ReactNode, useState } from "react";

type Theme = "light" | "dark";

interface ThemeValue {
  theme: Theme;
  toggle: () => void;
}

// 의미 있는 디폴트. Provider 없이도 light로 동작
const ThemeContext = createContext<ThemeValue>({
  theme: "light",
  toggle: () => {
    // 디폴트에서는 아무 일도 하지 않는다. 실 환경에서 Provider가 덮어쓴다
  },
});

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light");
  const toggle = () => setTheme((t) => (t === "light" ? "dark" : "light"));
  return <ThemeContext value={{ theme, toggle }}>{children}</ThemeContext>;
}

export const useTheme = () => useContext(ThemeContext);
```

길 1과 길 2 중 어느 것이 옳을까? 정답은 없다. 의도에 따라 다르다. **로그인 사용자 정보처럼 "Provider 없이는 의미를 잃는" 데이터는 길 1**이 낫다. **테마, 로케일처럼 "기본값으로도 멀쩡히 굴러가는" 데이터는 길 2**가 잘 어울린다. 한 가지 잊지 말자. 길 2로 갈 거라면 디폴트의 콜백이 호출되더라도 끔찍한 일이 벌어지지 않게 안전하게 만들어두는 편이 낫다. 위 코드의 `toggle: () => {}`처럼 빈 함수로라도 채워두자.

또 하나 짚을 게 있다. 길 1에서 만든 `useAuth` 훅은 단순한 가드 그 이상의 의미가 있다. `useContext`를 직접 노출하지 않고 커스텀 훅으로 한 번 감싸면, **Context의 정체를 호출하는 쪽으로부터 숨길 수 있다.** 어느 날 인증 상태를 Context에서 Zustand store로 옮기고 싶어졌다고 상상해보자. `useAuth`로 감싸 놓았다면, 훅 내부 구현만 바꾸면 된다. 호출하는 쪽 코드는 그대로다. 그러나 `useContext(AuthContext)`를 컴포넌트마다 직접 부르고 있었다면, 모든 호출 자리를 손봐야 한다. 작은 차이 같지만 리팩터링의 자유도를 크게 가른다. 그래서 어느 길로 가든 **Context는 커스텀 훅 뒤에 숨기자.** 이 한 가지 습관이 코드를 오래 건강하게 한다.

## Provider 합성 — 여러 Context를 어떻게 쌓는가

앱이 자라면 Context가 하나로 끝나지 않는다. 인증, 테마, 로케일, 라우팅, 토스트 메시지, 분석 도구, 피처 플래그… 다섯 개, 일곱 개를 넘어가는 일이 흔하다. 이걸 그대로 쌓으면 어떻게 될까?

```tsx
// 가독성이 무너지기 시작한다
function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <LocaleProvider>
          <RouterProvider>
            <ToastProvider>
              <FeatureFlagProvider>
                <AnalyticsProvider>
                  <Routes />
                </AnalyticsProvider>
              </FeatureFlagProvider>
            </ToastProvider>
          </RouterProvider>
        </LocaleProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}
```

들여쓰기가 오른쪽으로 한참 밀린다. "Provider 지옥(provider hell)"이라는 별명까지 있다. 이걸 좀 정돈해보자.

**방법 1. 합성 컴포넌트로 묶기.** 가장 단순하고 가장 자주 쓰는 방법이다.

```tsx
// AppProviders.tsx
function AppProviders({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        <LocaleProvider>
          <RouterProvider>
            <ToastProvider>
              <FeatureFlagProvider>
                <AnalyticsProvider>{children}</AnalyticsProvider>
              </FeatureFlagProvider>
            </ToastProvider>
          </RouterProvider>
        </LocaleProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}

// App.tsx
function App() {
  return (
    <AppProviders>
      <Routes />
    </AppProviders>
  );
}
```

`App`이 깔끔해졌다. 들여쓰기 지옥은 `AppProviders`로 옮겨갔지만, 거긴 그래도 된다. Provider를 모아두는 자리이니까.

**방법 2. 배열로 줄여 묶기.** 더 욕심이 난다면 배열을 풀어 합성하는 작은 헬퍼를 둘 수도 있다.

```tsx
// composeProviders.tsx
import { ComponentType, ReactNode } from "react";

type ProviderComp = ComponentType<{ children: ReactNode }>;

export function composeProviders(...providers: ProviderComp[]): ProviderComp {
  return ({ children }) =>
    providers.reduceRight(
      (acc, Provider) => <Provider>{acc}</Provider>,
      children as ReactNode,
    ) as ReturnType<ProviderComp>;
}

// 사용
const AppProviders = composeProviders(
  AuthProvider,
  ThemeProvider,
  LocaleProvider,
  RouterProvider,
  ToastProvider,
  FeatureFlagProvider,
  AnalyticsProvider,
);
```

이렇게 하면 새 Provider 하나를 추가할 때 배열에 한 줄만 더하면 된다. 다만 이 방법에는 한 가지 함정이 있다. 각 Provider가 props를 받지 못한다. props가 필요한 Provider라면 한 번 감싸는 함수를 따로 만들어야 한다. 그래서 대부분은 방법 1로 충분하다.

방법을 떠나서 한 가지는 분명히 해두자. **Provider의 순서가 의미를 가질 때**가 있다. 예를 들어 `AnalyticsProvider`가 내부에서 `useAuth`를 쓴다면, `AnalyticsProvider`는 반드시 `AuthProvider`보다 안쪽에 있어야 한다. 이런 의존성을 주석으로라도 짧게 적어두자. 새 사람이 들어와서 순서를 바꿨다가 끔찍한 디버깅 늪에 빠지는 일을 막자.

## Context를 쓰기 전에 시도해볼 대안 — 컴포넌트 합성

이쯤에서 한 발짝 물러나 보자. drilling이 고통스럽다고 해서 곧장 Context로 직행하는 것이 정말 최선일까? 사실 첫 번째 후보는 따로 있다. 바로 **컴포넌트 합성(composition)** 이다.

다시 처음의 시나리오를 떠올려보자. `App`이 `currentUser`를 가지고 있고, 트리 깊숙이 있는 `Avatar`가 그걸 써야 한다. 그런데 만약 `Avatar`를 만드는 책임을 `App`에 두고, 만들어진 `Avatar`를 `children`으로 깊은 곳까지 흘려보내면 어떨까?

```tsx
// 합성으로 푸는 길
function App({ currentUser }: { currentUser: User }) {
  return (
    <Layout sidebar={<ProfileHeader avatar={<Avatar src={currentUser.avatarUrl} />} />}>
      <Main />
    </Layout>
  );
}

function Layout({
  sidebar,
  children,
}: {
  sidebar: ReactNode;
  children: ReactNode;
}) {
  return (
    <div>
      <Sidebar>{sidebar}</Sidebar>
      {children}
    </div>
  );
}

function Sidebar({ children }: { children: ReactNode }) {
  return <aside>{children}</aside>;
}

function ProfileHeader({ avatar }: { avatar: ReactNode }) {
  return <header>{avatar}</header>;
}
```

`Layout`도 `Sidebar`도 `ProfileHeader`도 `currentUser`를 받지 않는다. 그저 ReactNode를 자리에 끼울 뿐이다. `currentUser`는 가장 위쪽에서 한 번만 읽혀서, `Avatar` 안에 박혀 내려간다. drilling이 사라졌고, Context도 쓰지 않았다.

이 방법의 장점은 분명하다. **타입 추적이 단순하다.** `currentUser`는 `App`에서만 보인다. 어디서 왔는지 한눈에 잡힌다. 또한 `Sidebar`나 `ProfileHeader`가 다른 자식을 받을 여지를 가진 채로 남는다. 재사용성이 올라간다.

물론 합성이 만능은 아니다. `Avatar`가 트리에 여러 군데 박혀 있고, 모든 자리마다 `currentUser`를 읽어야 한다면, `App`에서 `Avatar`를 7개 만들어 7군데에 끼워 넣는 짓을 해야 한다. 이쯤 되면 Context가 더 깔끔하다. **합성으로 풀 수 있다면 합성을 먼저, 합성이 어색해질 때 Context를.** 이 순서를 기억해두자.

또 한 가지 후보는 **데이터를 트리 더 가까이로 옮기는 것**이다. `currentUser`가 정말 `App` 최상단에 있어야 할까? 어쩌면 `ProfileSection` 근처에서 한 번에 가져와도 충분하다. 데이터를 위로 끌어올린 뒤 다시 내리는 패턴(3장에서 다룬 끌어올리고 다시 내림)이 너무 광범위해졌다면, 끌어올리지 말고 가까이 두는 편이 낫다.

## Context의 한계 — 모든 consumer가 리렌더된다

여기까지는 Context의 매끈한 면을 봤다. 이제 어두운 면을 보자. Context에는 **selective subscription**이 없다. 무슨 뜻인가? Provider의 `value`가 바뀌면, **그 Context를 읽는 모든 컴포넌트가 리렌더된다.** value의 일부만 바뀌었더라도 마찬가지다. 같은 객체의 어느 한 필드만 바뀌었더라도, 객체 참조가 새로 만들어졌다면 모든 consumer가 깨어난다.

다음과 같은 코드를 보자.

```tsx
// 폼 값을 Context에 넣었다 — 끔찍한 결과가 기다리고 있다
interface FormValue {
  name: string;
  email: string;
  message: string;
  setName: (v: string) => void;
  setEmail: (v: string) => void;
  setMessage: (v: string) => void;
}

const FormContext = createContext<FormValue | null>(null);

function FormProvider({ children }: { children: ReactNode }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  // 매 입력마다 새 객체가 만들어진다
  return (
    <FormContext value={{ name, email, message, setName, setEmail, setMessage }}>
      {children}
    </FormContext>
  );
}
```

`name` 입력란에 글자를 한 자 칠 때마다 어떤 일이 벌어지는지 따라가 보자. `setName`이 호출돼서 `name`이 바뀐다. `FormProvider`가 리렌더된다. value 객체가 새로 만들어진다(이전과 다른 참조). Context를 읽는 모든 컴포넌트가 리렌더된다. `name` 입력란뿐 아니라, `email` 입력란도, `message` 입력란도, 폼과 무관해 보이는 사이드바의 `currentUserBadge`도. 키 한 번 누를 때마다 화면 절반이 다시 그려진다. 사용자는 입력이 묘하게 끊긴다고 느낀다.

이 문제를 다루는 길은 몇 가지가 있다.

**길 1. Context를 잘게 쪼갠다.** state와 dispatch를 분리하면 한쪽만 바뀌어도 다른 쪽 consumer는 잠잠하다. 7장에서 본격적으로 다루는 reducer + Context 패턴이 정확히 이 길을 간다.

**길 2. value를 메모이즈한다.** `useMemo`로 객체 참조를 안정화하면, 정말 값이 바뀐 경우에만 재생성된다. 다만 이건 "value 객체가 새로 만들어지는" 문제만 해결할 뿐, "값이 바뀌었을 때 모든 consumer가 리렌더된다"는 본질은 그대로다.

**길 3. Context를 아예 안 쓴다.** 자주 바뀌는 값이라면 Context가 어울리지 않는다. Zustand, Jotai 같은 상태 라이브러리는 selective subscription을 기본으로 제공한다. "이 컴포넌트는 store의 `name` 필드만 본다"고 선언하면, 그 필드가 바뀔 때만 리렌더된다. 빈번히 바뀌는 글로벌 상태라면 이 도구가 더 알맞다.

**Context는 정적이거나 준정적인 값에 쓰자.** 자주 바뀌는 값을 Context에 던지지 말자. 이 한 문장이 Context를 둘러싼 가장 흔한 사고를 막아준다.

## "Context로 너무 많이 던지지 말자"

도구가 강력하면 자꾸 손이 간다. Context도 그렇다. prop을 두 번만 패스해도 "이거 Context로 빼는 게 낫지 않을까?" 같은 마음이 슬며시 든다. 이 충동에 한 번 항의해두자.

Context를 남용하면 어떤 일이 벌어질까?

**첫째, 데이터 흐름이 보이지 않는다.** prop은 코드를 읽으면 어디서 왔는지 따라갈 수 있다. Context에 들어간 값은 정의된 자리에서 한 번, 쓰는 자리에서 한 번씩 등장하고 그 사이는 보이지 않는다. 디버깅할 때 "이 값이 왜 이래?"라는 질문에 답하기 위해 Provider를 찾아 거슬러 올라가야 한다.

**둘째, 컴포넌트가 환경에 묶인다.** Context를 쓰는 컴포넌트는 그 Context Provider가 있는 트리 안에서만 동작한다. 스토리북이나 테스트 환경에서 그 컴포넌트를 단독으로 띄우려면, 매번 Provider를 따로 마련해줘야 한다. 컴포넌트의 휴대성이 떨어진다.

**셋째, 리렌더 폭격이 슬그머니 자란다.** 처음에는 한 컴포넌트에서만 쓰던 Context가, 점점 곳곳에서 쓰인다. 그러다 어느 날 자주 바뀌는 값이 그 안에 끼어든다. 그 순간부터 앱 전체가 잔잔히 무거워진다. 누구도 즉시 알아채지 못한다. 한참 후에 프로파일러를 켜고 나서야 "어, 왜 이걸 다 다시 그리지?" 하고 놀란다.

이런 위험을 감안한 휴리스틱을 정리해보자.

- prop drilling이 4단계 이상이고, 중간 컴포넌트가 그 prop을 쓰지 않으면 Context 후보다.
- 그 전에 **컴포넌트 합성**으로 풀 수 있는지 먼저 확인하자.
- Context에 넣을 값은 **자주 바뀌지 않는 값**이어야 한다. 1초에 한 번 이상 바뀌는 값이라면 다시 한번 의심하자.
- Provider는 가능하면 **트리의 깊은 자리**에 두자. 영향 범위를 좁히자.
- 자주 바뀌는 값이 정말 글로벌하게 필요하다면, Context 대신 **selective subscription**을 가진 상태 라이브러리를 고려하자.

이 휴리스틱은 절대적인 규칙이 아니다. 팀과 앱의 사정에 따라 한두 줄은 흔들릴 수 있다. 다만 "drilling이 보이면 즉시 Context"라는 본능적 반응만은 한 번 멈춰두자.

## 핵심 정리

- prop drilling이 두세 단계 깊이라면 그대로 두는 편이 낫다. 깊이, 중간 컴포넌트의 무관함, 변화의 빈도, 사용 범위가 모두 맞물릴 때 비로소 진짜 고통이 된다.
- Context는 전역 변수가 아니라 "Provider로 감싼 트리 구간 안에서만 유효한 값"이다. 영역 개념을 잊지 말자.
- `createContext`, `<MyContext value={...}>`, `useContext`. 리액트 19부터는 `<MyContext.Provider>`를 쓰지 않아도 된다.
- Context 기본값은 두 길이 있다. `null`+커스텀 훅 가드는 "Provider 없이 쓰면 버그"인 데이터에, 의미 있는 디폴트는 "기본값으로도 동작해야 하는" 데이터에 어울린다.
- 여러 Provider를 쌓아야 한다면 합성 컴포넌트(`AppProviders`)로 묶자. 들여쓰기 지옥을 한곳에 몰아넣자.
- Context를 꺼내기 전에 컴포넌트 합성으로 풀 수 있는지 먼저 시도하자. 합성은 데이터 흐름을 명료하게 유지한다.
- Provider를 트리의 깊은 자리에 두어 영향 범위를 좁히자(콜로케이션). 리렌더 비용도 같이 줄어든다.
- Context에는 selective subscription이 없다. value가 바뀌면 모든 consumer가 리렌더된다. 자주 바뀌는 값을 Context에 던지지 말자.
- Context는 정적이거나 준정적인 값(테마, 사용자, 로케일, 라우팅)에 어울린다. 빈번히 바뀌는 글로벌 상태는 Zustand 같은 selective subscription 도구가 더 알맞다.
- "Don't reach for context too soon"을 마음에 새겨두자. drilling이 보이는 즉시 Context로 도망가는 본능을 한 번씩 멈추자.

## 연습 문제

**[기초] 다크 모드 토글을 Context로**

`ThemeContext`를 만들어 라이트/다크 테마와 토글 함수를 트리 전체에 제공하자. 다음 요건을 만족하자.

- `theme: "light" | "dark"`와 `toggle: () => void`를 한 묶음으로 넣어보자.
- 의미 있는 디폴트(라이트)를 줘서, Provider 없이도 컴포넌트가 멀쩡히 렌더되게 하자.
- `useTheme` 커스텀 훅을 노출하자.
- `App` 어디든 깊은 자리에 있는 `ThemeToggleButton`이 단 두 줄 안에 토글을 호출할 수 있어야 한다. 중간 컴포넌트에 `theme` prop이 등장해서는 안 된다.

**[중급] 인증 정보(user) Context — 로그인/로그아웃 흐름**

`AuthContext`를 만들어 로그인/로그아웃을 처리하자. 다음 요건을 만족하자.

- `user: User | null`, `login(email, password)`, `logout()`을 노출하자.
- 기본값은 `null`로 두고, `useAuth` 훅에서 "AuthProvider 안에서만 사용 가능"하다는 에러를 던지자.
- `LoginForm`, `Header`, `ProfileMenu`, `AdminSection` 네 컴포넌트가 각각 다른 깊이에서 `useAuth`를 호출하도록 트리를 구성해보자.
- 로그인 성공/실패 시 화면 변화를 props 없이 처리할 수 있는지 확인해보자.

**[도전] 자주 바뀌는 값을 Context에 넣었을 때의 리렌더 진단**

다음 안티패턴을 직접 작성해보자. 폼 값(`name`, `email`, `message`)과 setter들을 한 객체로 묶어 `FormContext`에 넣고, 50개의 컴포넌트가 그 Context를 읽는 트리를 만들자.

- React DevTools의 Profiler를 켜고, `name` 입력란에 한 글자를 칠 때 몇 개 컴포넌트가 리렌더되는지 측정해보자.
- 같은 문제를 두 가지 방식으로 고쳐보자. (a) Context를 `NameContext`, `EmailContext`, `MessageContext`로 쪼개기. (b) Zustand 같은 selective subscription 라이브러리로 옮기기.
- 두 방식의 리렌더 횟수를 비교해보고, 각자의 장단점을 짧게 적어보자.

## 마무리

Context는 prop drilling을 끊는 도구가 맞다. 그러나 모든 drilling이 끊어야 할 짜증은 아니다. 두세 단계의 패스는 코드를 읽는 사람에게 친절한 단서를 남기고, 그대로 둬도 충분하다. 4단계 이상에 중간이 무관하고 자주 바뀌는 prop이 보이는 순간, 그때 Context를 꺼내자. 그 전에 컴포넌트 합성으로 풀 수 있는지 한 번 더 시도하자. 그리고 Context에 들어가는 값이 자주 바뀌는 값이 아닌지 한 번 더 확인하자. 이 세 가지 멈춤이 Context를 좋은 도구로 유지해 준다.

그런데 한 가지 의문이 남는다. Context에 값을 던질 때, 단순한 데이터만 던지는 것이 정말 끝일까? 만약 그 안에 **dispatch까지 같이 던진다면** 어떤 일이 벌어질까? state는 한쪽 Context로, dispatch는 다른 쪽 Context로 분리하면, 리렌더 폭격을 피하면서도 큰 앱의 상태를 깔끔하게 다룰 수 있는 길이 열린다. 7장에서는 Reducer와 Context를 한데 묶어, 앱이 커져도 흔들리지 않는 상태 구조를 만드는 패턴을 살펴보자.
