# 부록 C — 참고문헌과 학습 경로

이 책의 본문과 부록 B에서 인용한 자료를 한 곳에 모아 두었다. 같은 자료를 두 번 안내하지 않으려고, 본문 인용 위치(챕터 매핑)도 함께 적었다. 끝부분에는 이 책 다음으로 갈 학습 경로를 단계별로 제안한다.

---

## 1. 공식 자료 (react.dev) — 챕터 매핑

react.dev는 이 책 전반의 1차 골격이다. 각 항목은 본문에서 정면으로 다룬 챕터를 함께 표기했다. 모든 링크는 2026-04-26 기준 접근 가능을 확인했다.

- **Managing State 허브** — `https://react.dev/learn/managing-state`
  본문 1부 전체의 출발점. 1장에서 인용.
- **Reacting to Input with State** — `https://react.dev/learn/reacting-to-input-with-state`
  "다섯 단계로 상태 모델링하기"의 1차 출처. 1·2장.
- **Choosing the State Structure** — `https://react.dev/learn/choosing-the-state-structure`
  파생값/모순 boolean/선택은 ID로 — 2장의 핵심 골격.
- **Sharing State Between Components** — `https://react.dev/learn/sharing-state-between-components`
  상태 끌어올리기. 3장.
- **Preserving and Resetting State** — `https://react.dev/learn/preserving-and-resetting-state`
  트리 위치와 `key`. 4장.
- **Extracting State Logic into a Reducer** — `https://react.dev/learn/extracting-state-logic-into-a-reducer`
  useReducer 도입. 5장.
- **Passing Data Deeply with Context** — `https://react.dev/learn/passing-data-deeply-with-context`
  Context 기본. 6장.
- **Scaling Up with Reducer and Context** — `https://react.dev/learn/scaling-up-with-reducer-and-context`
  state/dispatch context 분리. 7장.
- **Escape Hatches 허브** — `https://react.dev/learn/escape-hatches`
  2부 전체의 출발점. 9장.
- **Referencing Values with Refs** — `https://react.dev/learn/referencing-values-with-refs`
  10장.
- **Manipulating the DOM with Refs** — `https://react.dev/learn/manipulating-the-dom-with-refs`
  10장 후반부.
- **Synchronizing with Effects** — `https://react.dev/learn/synchronizing-with-effects`
  Effect를 "동기화"로 재정의. 11장.
- **You Might Not Need an Effect** — `https://react.dev/learn/you-might-not-need-an-effect`
  책의 절정. 12장.
- **Lifecycle of Reactive Effects** — `https://react.dev/learn/lifecycle-of-reactive-effects`
  Reactive Value 정의. 11·13장.
- **Separating Events from Effects** — `https://react.dev/learn/separating-events-from-effects`
  `useEffectEvent`. 13장과 부록 A.
- **Removing Effect Dependencies** — `https://react.dev/learn/removing-effect-dependencies`
  의존성 다섯 가지 처방. 13장.
- **Reusing Logic with Custom Hooks** — `https://react.dev/learn/reusing-logic-with-custom-hooks`
  커스텀 훅. 14장.

react.dev의 학습 트랙은 이 책의 진행과 거의 그대로 겹친다. 본문을 읽다 막힐 때 해당 페이지의 sandbox 예제를 직접 만져보자. 텍스트와 인터랙션은 다른 근육을 쓴다.

---

## 2. 권장 블로그/글 (영문권)

본문 곳곳에서 짧게 인용한 권위자 글을 모았다. 한 편을 골라 깊이 읽고 싶다면, 굵게 표시한 두 편을 우선 추천한다.

- **Dan Abramov, "A Complete Guide to useEffect"** — `https://overreacted.io/a-complete-guide-to-useeffect/`
  useEffect 멘탈 모델의 결정판. 11·13장의 사상적 기반. 한 번은 정독을 권장한다.
- Dan Abramov, "useEffect 완벽 가이드" 한국어 번역(rinae.dev) — `https://rinae.dev/posts/a-complete-guide-to-useeffect-ko/`
  영어가 부담스러운 독자를 위한 번역.
- **Kent C. Dodds, "Application State Management with React"** — `https://kentcdodds.com/blog/application-state-management-with-react`
  "React IS your state management library" 입장의 원전. 8장의 도구 선택 휴리스틱이 여기서 출발했다.
- Kent C. Dodds, "How to Test Custom React Hooks" — `https://kentcdodds.com/blog/how-to-test-custom-react-hooks`
  14장 커스텀 훅 테스트의 보조 자료.
- Kent C. Dodds, "The State Reducer Pattern with React Hooks" — `https://kentcdodds.com/blog/the-state-reducer-pattern-with-react-hooks`
  reducer 패턴의 한 가지 발전형. 5장 보강.
- Robin Wieruch, "React: How to create a Custom Hook" — `https://www.robinwieruch.de/react-custom-hook/`
  "두 번 이상 보이면 추출"의 출처. 14장.
- Robin Wieruch, "React Hooks Tutorial" — `https://www.robinwieruch.de/react-hooks/`
  훅 전반 입문 보강.

---

## 3. 한국어 자료

한국 커뮤니티의 글은 같은 문제를 한국어 사용 환경에서 어떻게 부르는지 익히기 좋다. 본문에서는 짧게 인용했지만 원문이 짚는 결은 직접 읽어야 잡힌다.

- "useEffect를 남용하지 말자" (HyunGyu) — `https://gusrb3164.github.io/web/2021/12/29/less-use-useeffect/`
  12장의 한국어 동지. "암묵적 제어 흐름이 디버깅을 어렵게 한다"는 진단이 인상적이다.
- "useRef의 새로운 발견 (useState와 비교)" (velog/skawnkk) — `https://velog.io/@skawnkk/useState-vs-useRef`
  입력 폼 21회 → 2회 렌더 정량 비교. 10장과 부록 B Q19에서 인용.
- "React useEffect 무한 루프 탈출하기" (velog/summereuna) — `https://velog.io/@summereuna/리액트-useEffect-무한-루프-탈출하기`
  의존성 함정의 한국어 정리. 13장 보강.
- "React useEffect 실수 TOP3 정리 + useEffectEvent" (beam307, 2026) — `https://beam307.github.io/2026/02/08/use-effect/`
  최신 동향 포함. 13장과 부록 A.
- "useEffect hook에 대해 더 알아보자" (Yohan) — `https://yohanpro.com/posts/react/use-effect/`
  11장 보강용 입문 자료.
- "React.useEffect — 일반적인 문제와 해결" (freeCodeCamp 한국어) — `https://www.freecodecamp.org/korean/news/react-useeffect-hug-hook-ilbanjeogin-munjewa-geu-haegyeol-bangbeob/`
  체크리스트 형식의 한국어 정리. 11·12·13장 통합 복습용.
- "useState vs useRef" (theteams/휴먼스케이프) — `https://www.theteams.kr/teams/6500/post/73410`
  실무 시각의 비교. 10장 보강.
- "useRef는 처음이라 — 개념부터 활용 예시까지" (mnxmnz) — `https://mnxmnz.github.io/react/what-is-use-ref/`
  10장 입문 자료.
- "리액트 useReducer로 상태 업데이트 로직 분리하기" (vlpt 김민준) — `https://react.vlpt.us/basic/20-useReducer.html`
  5장의 한국어 보조.

---

## 4. 영어 커뮤니티 / 산업 동향

도구 선택 챕터(8장)와 부록 B의 6군에서 끌어온 자료다. 트렌드를 점검할 때 다시 들춰보자.

- Hacker News, "You Might Not Need an Effect" 토론 — `https://news.ycombinator.com/item?id=35270877`
  Dan Abramov의 "메타 내부 표본 약 46%가 불필요" 발언이 나오는 스레드. 12장과 부록 B Q25.
- Hacker News, "Common Beginner Mistakes with React" — `https://news.ycombinator.com/item?id=35108672`
  실무 보고들의 광범위한 채집.
- TanStack Query, "Does TanStack Query replace Redux/MobX?" — `https://tanstack.com/query/v4/docs/framework/react/guides/does-this-replace-client-state`
  서버 상태와 UI 상태를 가르는 공식 입장. 8장.
- "State of React State Management in 2026" (PkgPulse) — `https://www.pkgpulse.com/blog/state-of-react-state-management-2026`
  Zustand 대세화의 통계. 8장과 부록 B Q12.
- "Redux vs Zustand vs Context API in 2026" (Sparkle Web) — `https://medium.com/@sparklewebhelp/redux-vs-zustand-vs-context-api-in-2026-7f90a2dc3439`
- "React State: Redux vs Zustand vs Jotai (2026)" (inhaq) — `https://inhaq.com/blog/react-state-management-2026-redux-vs-zustand-vs-jotai.html`
- "TanStack Query vs SWR vs Apollo Client 2026" (PkgPulse) — `https://www.pkgpulse.com/blog/tanstack-query-vs-swr-vs-apollo-2026`
- "React Query vs SWR in 2026" (dev.to/whoffagents) — `https://dev.to/whoffagents/react-query-vs-swr-in-2026-what-i-actually-use-and-why-3362`

---

## 5. 더 깊이 들어가고 싶은 사람을 위한 다음 학습 경로

이 책은 "Managing State + Escape Hatches"라는 두 단원에 의도적으로 시야를 좁혔다. 자연스럽게 따라오는 다음 단계는 세 갈래다.

### 5.1 Suspense → RSC → `use(promise)`

Suspense는 "데이터가 아직 없는 동안의 UI 상태"를 React가 직접 다루도록 어휘를 한 단계 끌어올린다. 학습 순서는 다음이 자연스럽다.

1. **Suspense 기본** — react.dev `https://react.dev/reference/react/Suspense` 부터. 로딩 fallback의 위치를 트리에서 어떻게 잡는지에 익숙해지자.
2. **Server Components** — `https://react.dev/reference/rsc/server-components` 와 Next.js App Router 공식 문서. RSC는 본문이 다룬 "client state"와 다른 차원의 문제 — 데이터의 "어디서 가져오는가"를 컴포넌트 경계로 끌어올린다.
3. **`use(promise)`** — Suspense·RSC 사고가 잡힌 다음에야 의미가 산다. 부록 A에서 미리 보기로만 다뤘던 이유다.

이 갈래의 핵심은 "지금까지 effect로 수동 처리하던 외부 비동기를 React가 직접 어휘로 받는다"는 큰 그림이다. 본문 11·12장에서 답답하게 느꼈던 부분이 자연스럽게 풀린다.

### 5.2 React Compiler 추적

2025–2026 시점에 활발히 움직이는 영역이다. 추적 자료:

- React 팀 공식 블로그(`https://react.dev/blog`) — 컴파일러 관련 RFC와 릴리스 노트.
- React Conf 발표 영상 — 컴파일러 세션은 매년 핵심 트랙에 들어간다.
- Dan Abramov 후속 글들과 React Working Group 토론.

핵심 질문은 "메모화를 컴파일러가 자동으로 처리하면, useMemo·useCallback에 대한 우리의 휴리스틱이 어떻게 바뀌는가"다. 14장에서 짧게 짚은 메모화 판단 기준이 시간이 지나면 단순해질 가능성이 높다.

### 5.3 동시성 모델 깊이 자료

이 책은 동시성 렌더링의 효과(개발 모드 더블 인보케이션, tearing 회피)를 결과 위주로만 다뤘다. 더 깊이 들어가려면:

- "Concurrent Rendering" (react.dev `https://react.dev/learn/keeping-components-pure` 와 후속 페이지들).
- `useTransition`, `useDeferredValue`, `startTransition` 공식 reference.
- Hacker News·React Working Group의 동시성 토론 — "왜 이 모델이 필요한가"의 역사적 맥락.

이 갈래는 본문 11장의 "동기화" 사고를 동시성 시대의 멀티 렌더 가능성과 합쳐 다시 보게 한다.

### 5.4 보강해두면 좋은 영역

본문 리서치 한계(레퍼런스 8절)에서 정직하게 적었던 영역도 다음 학습 후보다. 학술적 기반이 궁금하다면 Flux/Elm architecture와 FRP(Functional Reactive Programming) 관련 1차 자료, 그리고 unidirectional data flow의 역사적 맥락. 한국 기업 사례를 더 보고 싶다면 우아한형제들 기술블로그(`https://techblog.woowahan.com`), 카카오 기술블로그(`https://tech.kakao.com`), 네이버 D2(`https://d2.naver.com`), 토스 기술블로그(`https://toss.tech`)를 키워드 "useEffect", "상태 관리", "Zustand", "TanStack Query"로 훑어보자. 본 라운드 리서치에서 직접 발췌하지 못한 영역이라 독자가 직접 확인하는 편이 정확하다.

---

## 6. 독자에게 권하는 한 마디

자료는 충분하다 못해 넘친다. 부족한 것은 언제나 시간이고, 그래서 우리에게 필요한 건 "지금 이 코드의 결함을 어떤 어휘로 부를지" 하나의 라벨이다. 라벨이 잡히면 검색은 빨라지고, 검색이 빨라지면 학습은 누적된다. 본문에서 익힌 어휘 — 스냅샷, 동기화, Reactive Value, 파생, 콜로케이션, escape hatch — 가 그 라벨이다.

이 부록의 자료를 한꺼번에 읽으려 하지 말자. 다음에 마주칠 한 가지 문제에 대해, 위 표에서 한두 편을 골라 읽는 흐름을 권한다. 그리고 같은 자리에서 헤매는 동료에게 자료를 건넬 때, 부록 B의 Q번호와 이 부록의 링크를 함께 보내주자. 같은 길을 두 번 헤매지 않는 팀이 가장 빨리 자란다.

이제 책의 본문을 닫고, 다음에 만날 코드로 돌아가자. 거기서 다시 만나자.
