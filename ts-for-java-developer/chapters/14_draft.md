# 14장. 테스트와 타입 — Vitest·expect-type·Playwright

Spring 프로젝트의 테스트 코드를 짜던 손이 처음으로 TS 프로젝트에서 테스트 파일을 열었다고 해보자. JUnit의 `@Test`는 어디 갔는가. MockK의 `every { ... } returns ...`는 어떤 문법으로 바꿔야 하는가. 그리고 무엇보다 — *타입을 테스트한다*는 이 낯선 개념은 대체 무슨 뜻인가.

Java/Kotlin 생태계에서 테스트 도구 셋은 비교적 명확했다. JUnit 5가 단위·통합 테스트를 책임지고, MockK(또는 Mockito)가 모킹을 맡고, Selenium이나 Playwright가 E2E를 담당했다. AssertJ로 어설션을 읽기 좋게 만들고, jqwik으로 프로퍼티 기반 테스트를 조금 곁들이면 웬만한 테스트 전략이 완성됐다.

TS 생태계는 이 구도와 얼마나 다를까. 놀랍도록 비슷한 부분도 있고, 완전히 다른 영역도 있다. 비슷한 부분은 빠르게 매핑할 수 있다. 다른 부분이 진짜 흥미롭다. 그 중심에 *타입 단위 테스트*가 있다. 런타임이 없어도 타입이 의도한 모양인지 검증할 수 있다는 이 발상은 Java에는 없던 자리다. 4·5장에서 공들여 만든 복잡한 타입이 여기서 검증된다. 12·13장의 컴포넌트와 API가 Vitest, Testing Library, Playwright로 테스트된다.

이 장은 그 전체 지도를 그린다.

---

## 단위 테스트의 자리 — Vitest vs Jest

Java 개발자가 처음 TS 프로젝트를 열면 `package.json`의 `scripts` 항목에서 낯선 이름을 만난다.

```json
{
  "scripts": {
    "test": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

`vitest`가 무엇인가. 2022년부터 빠르게 표준 자리를 차지하고 있는 테스트 러너다. Vite 기반 프로젝트에서는 이제 Jest보다 Vitest를 선택하는 게 합리적 디폴트가 됐다. 왜 그런지 이해하려면 Jest부터 살펴볼 필요가 있다.

**Jest**는 Facebook(현 Meta)이 만든 테스트 프레임워크다. React 프로젝트가 폭발적으로 증가하던 2015~2020년대 초반 사실상 표준이 됐다. 기능이 풍부하다. 단위 테스트·통합 테스트·스냅샷 테스트·코드 커버리지가 하나의 패키지에 들어 있다. 문서도 방대하고 커뮤니티도 크다.

그러나 Jest에는 답답한 구석이 있다. ESM 지원이 오랫동안 실험적이었다. 트랜스파일을 위해 `ts-jest`나 `babel-jest`를 별도로 설치해야 하고, 설정 파일이 복잡해진다. 그리고 느리다. 테스트가 많아질수록 Jest의 속도 문제가 도드라진다.

**Vitest**는 이 문제들을 Vite의 힘으로 해결했다. Vite의 번들러 파이프라인 위에서 돌아가기 때문에 ESM을 기본으로 지원하고, HMR 개념을 테스트에 적용해 변경된 파일과 연관된 테스트만 재실행한다. TypeScript 파일을 별도 설정 없이 직접 실행할 수 있다. 그리고 빠르다. 프로젝트 규모에 따라 다르지만 Jest 대비 수 배에서 수십 배 빠른 실행 속도 보고가 일반적이다.

```typescript
// Vitest 설정 — vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
});
```

설정이 단순하다. `tsconfig.json`을 자동으로 읽고, ESM도 기본 지원한다. Jest처럼 `ts-jest`를 따로 설치할 필요가 없다.

테스트 코드 문법은 Jest와 거의 동일하다. Vitest는 의도적으로 Jest API와 호환되도록 설계했다. Jest에서 Vitest로 마이그레이션하는 비용이 낮은 이유다.

```typescript
// product.test.ts
import { describe, it, expect } from 'vitest';
import { calculateDiscount } from './product';

describe('calculateDiscount', () => {
  it('정회원에게 10% 할인을 적용한다', () => {
    const result = calculateDiscount(10000, 'member');
    expect(result).toBe(9000);
  });

  it('비회원은 할인 없음', () => {
    const result = calculateDiscount(10000, 'guest');
    expect(result).toBe(10000);
  });
});
```

JUnit의 `@Test`와 비교해보자.

---

> **📚 Java/Kotlin 시선 ① — JUnit `@Test` ↔ Vitest `test` / `it`**
>
> **Java/Kotlin (JUnit 5)**
> ```kotlin
> @ExtendWith(MockKExtension::class)
> class CalculateDiscountTest {
>
>     @Test
>     fun `정회원에게 10% 할인을 적용한다`() {
>         val result = calculateDiscount(10000, MemberType.MEMBER)
>         assertThat(result).isEqualTo(9000)
>     }
>
>     @Test
>     fun `비회원은 할인 없음`() {
>         val result = calculateDiscount(10000, MemberType.GUEST)
>         assertThat(result).isEqualTo(10000)
>     }
> }
> ```
>
> **TypeScript (Vitest)**
> ```typescript
> import { describe, it, expect } from 'vitest';
>
> describe('calculateDiscount', () => {
>   it('정회원에게 10% 할인을 적용한다', () => {
>     const result = calculateDiscount(10000, 'member');
>     expect(result).toBe(9000);
>   });
>
>   it('비회원은 할인 없음', () => {
>     const result = calculateDiscount(10000, 'guest');
>     expect(result).toBe(10000);
>   });
> });
> ```
>
> 구조가 놀랍도록 닮았다. `describe`가 JUnit의 테스트 클래스 역할을 하고, `it` 또는 `test`가 `@Test`에 대응한다. 테스트 이름을 문자열로 자유롭게 쓸 수 있다는 점은 Kotlin의 backtick 함수명과 비슷한 자유다. `expect(...).toBe(...)`는 AssertJ의 `assertThat(...).isEqualTo(...)`와 구조가 같다. 다만 Java처럼 테스트 클래스 인스턴스를 생성하거나 어노테이션으로 설정을 주입하는 방식은 없다 — 함수가 first-class이기 때문에 구성이 훨씬 단순하다.

---

### Vitest를 선택해야 하는 시점, Jest를 유지해야 하는 시점

신규 프로젝트라면 Vitest가 합리적 디폴트다. Vite 기반 프론트엔드 프로젝트는 물론이고, Node 백엔드 프로젝트에서도 Vitest는 잘 작동한다. 설정이 단순하고 빠르며 ESM을 자연스럽게 지원한다.

반면 기존 Jest 코드베이스를 유지해야 하는 상황이 있다. 레거시 CJS 기반 코드베이스, 복잡한 Jest 플러그인 생태계에 이미 깊이 의존하는 경우, 또는 팀이 Jest에 익숙해 마이그레이션 비용이 이득보다 클 때다. Jest를 선택했다는 게 틀린 결정이 아니다. 2025년 현재도 Jest는 대규모 프로젝트에서 안정적으로 쓰인다.

```
Vitest를 선택하는 편이 나은 경우:
- 신규 프로젝트 또는 Vite 기반 프로젝트
- ESM 우선 코드베이스
- 빠른 피드백 루프가 중요한 팀
- 설정을 최소화하고 싶을 때

Jest를 유지하는 편이 나은 경우:
- 기존 Jest 코드베이스가 크고 안정적
- create-react-app 같은 레거시 scaffolding에 묶여 있을 때
- Jest 전용 플러그인/reporter에 이미 투자했을 때
```

하나 주의할 점이 있다. Vitest와 Jest의 API가 호환된다고 했지만 `vi` 네임스페이스는 `jest` 대신 `vi`를 써야 한다. `jest.fn()`이 `vi.fn()`으로, `jest.mock()`이 `vi.mock()`으로 바뀐다. 마이그레이션에서 대부분의 변경이 여기에 집중된다.

---

## Test Double의 TS화 — `vi.fn`, `vi.mock`, 타입 안전 모킹

MockK를 쓰던 Kotlin 개발자가 처음 `vi.mock`을 만나면 한 가지가 눈에 걸린다. MockK는 타입 안전하다. `mockk<UserRepository>()`라고 쓰면 `UserRepository`의 메서드 시그니처가 즉시 보인다. 타입 시스템이 모킹의 경계를 잡아준다.

`vi.fn()`도 타입 안전하게 쓸 수 있다. 하지만 명시적으로 타입을 주어야 하는 자리가 조금 더 많다.

```typescript
// vi.fn() 기본 — 타입을 명시하지 않으면 any
const mockFetch = vi.fn();

// 타입을 명시하는 방법들
const mockFetch1 = vi.fn<() => Promise<Response>>();

// 또는 함수 타입을 직접
const mockSave = vi.fn<(user: User) => Promise<void>>();

// Mock Return Value
mockSave.mockResolvedValue(undefined);
mockFetch1.mockResolvedValue(new Response('{"id": 1}'));
```

`vi.mock()`은 모듈 전체를 대체한다. Java의 `@MockBean`과 비슷한 역할인데, 동작 방식은 다르다. 모듈 경로를 문자열로 지정하면 해당 모듈의 모든 export가 자동으로 mock 함수로 대체된다.

```typescript
// userService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getUserById } from './userService';
import { db } from './database'; // 이 모듈을 mock할 것

vi.mock('./database'); // 전체 모듈을 mock

describe('getUserById', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('사용자를 조회한다', async () => {
    const mockUser = { id: 1, name: '홍길동', email: 'hong@example.com' };

    // db.findUserById를 스텁으로 교체
    vi.mocked(db.findUserById).mockResolvedValue(mockUser);

    const result = await getUserById(1);

    expect(result).toEqual(mockUser);
    expect(db.findUserById).toHaveBeenCalledWith(1);
    expect(db.findUserById).toHaveBeenCalledTimes(1);
  });
});
```

`vi.mocked()`가 핵심이다. `db.findUserById`를 그냥 쓰면 TypeScript는 그게 mock 함수라는 걸 모른다. `vi.mocked()`로 감싸면 해당 함수가 `MockedFunction` 타입이 되어 `mockResolvedValue`, `toHaveBeenCalledWith` 같은 mock 전용 메서드에 접근할 수 있다.

---

> **📚 Java/Kotlin 시선 ② — MockK ↔ `vi.fn` / `vi.mock`**
>
> **Kotlin (MockK)**
> ```kotlin
> @ExtendWith(MockKExtension::class)
> class UserServiceTest {
>     @MockK
>     lateinit var userRepository: UserRepository
>
>     @InjectMockKs
>     lateinit var userService: UserService
>
>     @Test
>     fun `사용자를 조회한다`() {
>         val mockUser = User(id = 1, name = "홍길동")
>         every { userRepository.findById(1) } returns mockUser
>
>         val result = userService.getUserById(1)
>
>         assertThat(result).isEqualTo(mockUser)
>         verify(exactly = 1) { userRepository.findById(1) }
>     }
> }
> ```
>
> **TypeScript (Vitest)**
> ```typescript
> import { vi, describe, it, expect, beforeEach } from 'vitest';
> import { UserService } from './userService';
> import { UserRepository } from './userRepository';
>
> vi.mock('./userRepository');
>
> describe('UserService', () => {
>   let userService: UserService;
>   let mockRepo: UserRepository;
>
>   beforeEach(() => {
>     mockRepo = new UserRepository() as vi.Mocked<UserRepository>;
>     userService = new UserService(mockRepo);
>   });
>
>   it('사용자를 조회한다', async () => {
>     const mockUser = { id: 1, name: '홍길동' };
>     vi.mocked(mockRepo.findById).mockResolvedValue(mockUser);
>
>     const result = await userService.getUserById(1);
>
>     expect(result).toEqual(mockUser);
>     expect(mockRepo.findById).toHaveBeenCalledWith(1);
>     expect(mockRepo.findById).toHaveBeenCalledTimes(1);
>   });
> });
> ```
>
> 어휘 매핑을 정리하면 이렇다. `@MockK` → `vi.mock()`. `every { ... } returns` → `mockResolvedValue` / `mockReturnValue`. `verify { ... }` → `expect(...).toHaveBeenCalledWith(...)`. `@InjectMockKs`는 TS에 직접 대응물이 없다 — DI가 생성자 기반이면 직접 주입하고, NestJS라면 `Test.createTestingModule()`을 쓴다. MockK의 `coEvery`(코루틴 mock) 개념은 TS에서는 별도 처리가 필요 없다 — `async/await`가 이미 일급이기 때문이다.

---

### 부분 모킹 — `vi.spyOn`

모듈 전체가 아니라 특정 메서드만 감시하거나 교체하고 싶을 때 `vi.spyOn`을 쓴다. MockK의 `spyk`와 비슷한 역할이다.

```typescript
import { vi, describe, it, expect, afterEach } from 'vitest';
import * as emailService from './emailService';

describe('sendWelcomeEmail', () => {
  afterEach(() => {
    vi.restoreAllMocks(); // spy 원래 구현으로 복원
  });

  it('이메일을 전송한다', async () => {
    const spy = vi.spyOn(emailService, 'sendEmail').mockResolvedValue(true);

    await emailService.sendWelcomeEmail('hong@example.com', '홍길동');

    expect(spy).toHaveBeenCalledWith(
      'hong@example.com',
      expect.stringContaining('환영합니다')
    );
  });
});
```

`vi.restoreAllMocks()`를 `afterEach`에 넣는 패턴이 중요하다. spy를 복원하지 않으면 다음 테스트에서 이전 spy가 살아남아 난감한 상황이 생긴다. 테스트가 격리되지 않으면 원인을 찾기가 끔찍하게 어려워진다. 이 패턴은 잊지 않는 편이 낫다.

---

## 프로퍼티 기반 테스트 — fast-check와 jqwik

"모든 양수 정수에 대해 이 함수가 올바르게 작동하는가"를 검증하고 싶다고 해보자. 예제 기반 테스트라면 몇 가지 케이스를 직접 나열한다. 하지만 빠뜨린 케이스가 있으면? 경계값을 놓치면? 프로퍼티 기반 테스트는 이 문제를 다른 방식으로 접근한다. *입력의 범위를 선언*하고, 프레임워크가 그 범위에서 자동으로 케이스를 생성해 실행한다.

Kotlin에서는 `jqwik`이 이 역할을 한다. TS에서는 `fast-check`가 같은 자리에 있다.

```typescript
import { describe, it } from 'vitest';
import fc from 'fast-check';

describe('sortedArray property', () => {
  it('정렬 후 배열 길이는 변하지 않는다', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted = [...arr].sort((a, b) => a - b);
        return sorted.length === arr.length;
      })
    );
  });

  it('정렬 후 인접 요소는 항상 오름차순이다', () => {
    fc.assert(
      fc.property(fc.array(fc.integer(), { minLength: 2 }), (arr) => {
        const sorted = [...arr].sort((a, b) => a - b);
        for (let i = 0; i < sorted.length - 1; i++) {
          if (sorted[i] > sorted[i + 1]) return false;
        }
        return true;
      })
    );
  });
});
```

`fc.assert`가 수백 개의 랜덤 케이스를 자동으로 생성해 실행한다. 실패하는 케이스를 발견하면 `fast-check`는 가장 작은 반례(shrinking)를 찾아 보여준다. `[1, 0]` 같은 단순한 반례가 복잡한 원래 케이스 대신 나타나는 방식이다.

---

> **📚 Java/Kotlin 시선 ③ — jqwik ↔ fast-check**
>
> **Kotlin (jqwik)**
> ```kotlin
> import net.jqwik.api.*
>
> class SortPropertyTest {
>     @Property
>     fun `정렬 후 배열 길이는 변하지 않는다`(
>         @ForAll list: List<Int>
>     ): Boolean {
>         val sorted = list.sorted()
>         return sorted.size == list.size
>     }
>
>     @Property
>     fun `정렬 후 인접 요소는 항상 오름차순`(
>         @ForAll @Size(min = 2) list: List<@IntRange(min = -100, max = 100) Int>
>     ): Boolean {
>         val sorted = list.sorted()
>         return sorted.zipWithNext().all { (a, b) -> a <= b }
>     }
> }
> ```
>
> **TypeScript (fast-check + Vitest)**
> ```typescript
> import fc from 'fast-check';
> import { describe, it } from 'vitest';
>
> describe('sort property', () => {
>   it('정렬 후 배열 길이는 변하지 않는다', () => {
>     fc.assert(
>       fc.property(fc.array(fc.integer()), (arr) => {
>         return [...arr].sort((a, b) => a - b).length === arr.length;
>       })
>     );
>   });
>
>   it('정렬 후 인접 요소는 항상 오름차순', () => {
>     fc.assert(
>       fc.property(
>         fc.array(fc.integer({ min: -100, max: 100 }), { minLength: 2 }),
>         (arr) => {
>           const sorted = [...arr].sort((a, b) => a - b);
>           return sorted.every((v, i) => i === 0 || sorted[i - 1] <= v);
>         }
>       )
>     );
>   });
> });
> ```
>
> jqwik은 어노테이션으로 입력 범위를 선언하고, `@Property`가 프로퍼티 테스트임을 표시한다. fast-check는 함수형으로 구성된다 — `fc.property(생성기, 검증함수)`. 두 도구 모두 shrinking을 지원하므로 실패 시 최소 반례를 알 수 있다. jqwik의 `@ForAll @Size`같은 제약은 fast-check에서 `fc.array(fc.integer(), { minLength: 2 })`처럼 생성기 옵션으로 표현한다.

---

fast-check는 string, date, uuid, ipV4, emailAddress 같은 다양한 임의값 생성기를 제공한다. 도메인 객체를 생성하는 자체 Arbitrary를 만드는 것도 가능하다.

```typescript
// 도메인 객체 Arbitrary 정의
const userArbitrary = fc.record({
  id: fc.nat(),
  name: fc.string({ minLength: 1, maxLength: 50 }),
  email: fc.emailAddress(),
  age: fc.integer({ min: 0, max: 120 }),
});

it('사용자 직렬화-역직렬화는 항등 변환이다', () => {
  fc.assert(
    fc.property(userArbitrary, (user) => {
      const json = JSON.stringify(user);
      const parsed = JSON.parse(json);
      return parsed.id === user.id && parsed.email === user.email;
    })
  );
});
```

매일 쓰는 도구는 아니지만, 파싱·직렬화·알고리즘·유틸리티 함수에 경계값 케이스가 많을수록 fast-check는 가치를 발휘한다.

---

## 컴포넌트 테스트 — Testing Library + Vitest

12장에서 React 컴포넌트를 만들었다면 그 컴포넌트를 어떻게 테스트해야 할까. 전통적인 컴포넌트 테스트는 렌더링된 HTML 구조를 쿼리하거나 내부 state를 직접 확인하는 방식이었다. 하지만 이 방식은 구현 세부사항에 의존해서, 리팩토링을 하면 테스트가 깨지는 경우가 많다.

Testing Library는 다른 철학을 제안한다. *사용자가 실제로 보고 상호작용하는 방식으로 테스트하라.* 화면에 보이는 텍스트, 레이블, 역할(role)로 요소를 찾고, 클릭·타이핑 같은 실제 사용자 동작으로 테스트한다. 구현이 바뀌어도 사용자 경험이 같다면 테스트도 통과해야 한다는 원칙이다.

```typescript
// LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('이메일과 비밀번호를 입력하고 로그인 버튼을 누르면 onLogin이 호출된다', async () => {
    const mockOnLogin = vi.fn<(email: string, password: string) => Promise<void>>();
    mockOnLogin.mockResolvedValue(undefined);

    render(<LoginForm onLogin={mockOnLogin} />);

    const emailInput = screen.getByLabelText('이메일');
    const passwordInput = screen.getByLabelText('비밀번호');
    const loginButton = screen.getByRole('button', { name: '로그인' });

    await userEvent.type(emailInput, 'hong@example.com');
    await userEvent.type(passwordInput, 'secret123');
    await userEvent.click(loginButton);

    await waitFor(() => {
      expect(mockOnLogin).toHaveBeenCalledWith('hong@example.com', 'secret123');
    });
  });

  it('이메일 형식이 잘못되면 에러 메시지를 보여준다', async () => {
    const mockOnLogin = vi.fn();
    render(<LoginForm onLogin={mockOnLogin} />);

    await userEvent.type(screen.getByLabelText('이메일'), 'not-an-email');
    await userEvent.click(screen.getByRole('button', { name: '로그인' }));

    expect(screen.getByText('올바른 이메일 주소를 입력해주세요.')).toBeInTheDocument();
    expect(mockOnLogin).not.toHaveBeenCalled();
  });
});
```

`getByLabelText`, `getByRole`이 핵심이다. CSS 선택자나 컴포넌트의 내부 구조가 아니라 접근성 트리(accessibility tree)를 통해 요소를 찾는다. 이렇게 하면 리팩토링이 자유로워진다. 내부 구현을 아무리 바꿔도 `이메일` 레이블이 붙은 입력 필드가 남아 있고 `로그인` 버튼이 남아 있으면 테스트는 통과한다.

`userEvent`가 `fireEvent`보다 선호된다. `fireEvent.click`은 단순히 click 이벤트를 발생시키지만, `userEvent.click`은 실제 브라우저처럼 mouseenter, mousedown, mouseup, click 이벤트를 순서대로 발생시킨다. 더 현실적이다.

Vitest에서 Testing Library를 쓰려면 jsdom 또는 happy-dom 환경을 설정해야 한다.

```typescript
// vitest.config.ts — 브라우저 환경 추가
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom', // 또는 'happy-dom'
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom'; // toBeInTheDocument() 같은 커스텀 매처 추가
```

`@testing-library/jest-dom`이 `toBeInTheDocument()`, `toHaveValue()`, `toBeVisible()` 같은 DOM 특화 매처를 추가한다. 이것 없으면 컴포넌트 테스트가 상당히 번거로워진다.

---

## 타입 단위 테스트 — TS만의 영역

이제 이 장의 핵심 주제로 들어간다. 솔직히 말하면, 이 절을 처음 보는 Java 개발자는 고개를 갸웃거릴 수 있다.

*타입을 테스트한다는 게 무슨 뜻인가?*

---

> **💡 작가의 한 마디 — 타입을 테스트한다는 발상이 어색하다면**
>
> Java에는 이 개념이 없다. JUnit은 런타임에서 값을 검증한다. 컴파일 타임의 타입 정확성은 컴파일러가 암묵적으로 보장한다고 가정하기 때문에, 별도로 "이 변수의 타입이 `String`이 맞는가"를 테스트하지 않는다.
>
> TS는 다르다. 4·5장에서 살펴봤듯 TS의 타입 시스템은 매핑 타입, 조건부 타입, `infer`, 템플릿 리터럴 타입으로 복잡한 타입을 프로그래밍한다. `z.infer<typeof UserSchema>`가 어떤 타입을 뽑아내는가, Hono의 라우트 핸들러에서 응답 타입이 자동 추론되는가, 유틸리티 타입 `ExtractRouteParams<'/users/:id'>` 가 `{ id: string }`을 맞게 만들어내는가 — 이것들은 런타임으로 검증할 수 없다. 타입은 컴파일 타임에만 존재하기 때문이다.
>
> 그래서 "타입이 의도한 모양인가"를 컴파일 타임에 검증하는 도구가 생겼다. `expect-type`, `tsd`, `// @ts-expect-error` 가 그것이다. 이것은 Java에 없던 완전히 새로운 테스트의 자리다. 낯설게 느껴지는 건 당연하다 — 진짜로 새로운 개념이기 때문이다.

---

### `// @ts-expect-error` — 가장 단순한 시작

타입 테스트의 가장 기본적인 형태는 `// @ts-expect-error` 주석이다. 이 주석이 붙은 줄에서 컴파일러 에러가 발생해야 한다. 만약 에러가 발생하지 않으면 오히려 `@ts-expect-error` 자체가 에러가 된다.

```typescript
// 이 타입 단언은 틀린 것이어야 한다
const x: number = 'hello';
// @ts-expect-error
const y: string = 42;  // number를 string에 할당하면 에러가 나야 함

// 유틸리티 함수의 타입 안전성을 확인할 때
function greet(name: string): string {
  return `안녕하세요, ${name}님`;
}

// @ts-expect-error — 숫자를 넘기면 에러가 나야 한다
greet(42);

// 에러가 안 나면 @ts-expect-error 자체가 에러가 된다
// @ts-expect-error  ← 이 줄 아래에 에러가 없으면 컴파일 에러
greet('홍길동'); // 이건 정상 호출 — @ts-expect-error가 여기서 에러를 낸다
```

`// @ts-ignore`와 혼동하지 않는 편이 낫다. `@ts-ignore`는 에러를 무조건 억제하고, 실제로 에러가 없어도 조용하다. `@ts-expect-error`는 에러가 있어야 정상이고, 에러가 없으면 오히려 문제다. 타입 테스트 목적이라면 항상 `@ts-expect-error`를 써야 한다.

### `expect-type` — 타입의 단위 테스트 라이브러리

`expect-type`은 타입을 검증하는 전용 라이브러리다. 런타임에서 아무것도 하지 않는다. 오직 컴파일 타임에 타입 관계를 검증한다.

```typescript
import { expectTypeOf } from 'expect-type';

// 기본 타입 검증
expectTypeOf(42).toBeNumber();
expectTypeOf('hello').toBeString();
expectTypeOf(null).toBeNull();

// 함수 반환 타입 검증
function add(a: number, b: number): number {
  return a + b;
}
expectTypeOf(add).returns.toBeNumber();
expectTypeOf(add).parameters.toEqualTypeOf<[number, number]>();

// 복잡한 타입 검증
type ExtractId<T> = T extends { id: infer U } ? U : never;

expectTypeOf<ExtractId<{ id: number; name: string }>>().toEqualTypeOf<number>();
expectTypeOf<ExtractId<{ name: string }>>().toEqualTypeOf<never>();
```

이게 왜 필요한가. 5장에서 `conditional type`과 `infer`로 복잡한 타입 변환 유틸리티를 만들었다고 해보자. 그 유틸리티가 실제로 의도한 타입을 만들어내는지 어떻게 확인하는가. 런타임 테스트로는 알 수 없다. 타입은 런타임에 존재하지 않기 때문이다. `expectTypeOf`로 확인하는 것이 유일한 방법이다.

```typescript
// 실제 사례 — 복잡한 유틸리티 타입 검증
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [P in keyof T]: DeepReadonly<T[P]> }
  : T;

type Config = {
  server: {
    host: string;
    port: number;
  };
  db: {
    connections: { host: string; port: number }[];
  };
};

type ReadonlyConfig = DeepReadonly<Config>;

// 의도한 타입이 맞는지 검증
expectTypeOf<ReadonlyConfig>().toMatchTypeOf<{
  readonly server: {
    readonly host: string;
    readonly port: number;
  };
  readonly db: {
    readonly connections: readonly { readonly host: string; readonly port: number }[];
  };
}>();

// 변경이 불가능한지도 검증
expectTypeOf<ReadonlyConfig['server']['host']>().toBeString();

// 잘못된 타입 할당이 에러를 내는지 확인
// @ts-expect-error
const cfg: ReadonlyConfig = { server: { host: 'localhost', port: 3000 }, db: { connections: [] } };
// cfg.server.host = 'other'; // 이게 에러여야 한다
```

### `tsd` — `.test-d.ts` 파일로 타입 테스트 분리

`tsd`는 타입 테스트를 별도 `.test-d.ts` 파일에 작성하는 방식을 제안한다. 라이브러리를 만드는 경우에 특히 유용하다. 라이브러리의 공개 API 타입이 의도한 대로 동작하는지 배포 전에 검증할 수 있다.

```typescript
// index.test-d.ts
import { expectType, expectError } from 'tsd';
import { createUser, UserCreateInput, User } from './index';

// 정상 케이스
expectType<User>(createUser({ name: '홍길동', email: 'hong@example.com' }));

// 에러 케이스 — 필수 필드 누락
expectError(createUser({ name: '홍길동' })); // email 없으면 에러여야 함

// 에러 케이스 — 잘못된 타입
expectError(createUser({ name: 42, email: 'hong@example.com' })); // name은 string이어야 함
```

`npm test`를 실행하면 `tsd`가 이 파일을 TypeScript 컴파일러로 검사한다. `expectError` 안에서 에러가 나지 않으면 테스트가 실패한다.

라이브러리를 직접 만들 계획이 없다면 `tsd`보다 `expect-type`이 더 편하다. `expect-type`은 Vitest 테스트 파일 안에서 바로 쓸 수 있어 별도 설정이 필요 없다.

### Vitest와 함께 — 타입 테스트를 일반 테스트와 함께 실행

Vitest 1.x부터는 `expectTypeOf`가 내장되어 있다. `expect-type`을 별도 설치하지 않아도 된다.

```typescript
// userTypes.test.ts
import { describe, it, expectTypeOf } from 'vitest';
import type { User, UserCreateInput } from './types';
import { createUser } from './userService';

describe('User 타입', () => {
  it('createUser는 User를 반환한다', () => {
    expectTypeOf(createUser).returns.toMatchTypeOf<User>();
  });

  it('UserCreateInput에는 id가 없다', () => {
    expectTypeOf<UserCreateInput>().not.toHaveProperty('id');
  });

  it('User의 id는 number이다', () => {
    expectTypeOf<User['id']>().toBeNumber();
  });
});
```

이 테스트는 런타임에서 아무것도 실행하지 않는다. 하지만 `vitest run`을 실행하면 컴파일 타임에 타입 관계를 검증하고, 실패하면 테스트가 실패한다.

타입이 복잡해질수록 이런 테스트의 가치가 커진다. Hono의 라우트 타입 추론이 제대로 동작하는지, zod 스키마에서 뽑은 타입이 예상대로인지 — 이것들을 런타임 테스트로는 확인할 수 없다.

```typescript
// Hono RPC 타입 검증 예시
import { Hono } from 'hono';
import { hc } from 'hono/client';
import { expectTypeOf } from 'vitest';

const app = new Hono().get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id, name: '홍길동' });
});

const client = hc<typeof app>('/');

// RPC 클라이언트 응답 타입 검증
expectTypeOf(client.users[':id'].$get).toBeFunction();
```

---

## E2E 테스트 — Playwright와 Selenium의 거리

Selenium을 써본 Java 개발자라면 Playwright를 처음 보는 순간 편안함을 느낄 것이다. 개념 자체는 비슷하다. 브라우저를 자동화해서 실제 사용자 흐름을 검증한다. 하지만 Playwright는 훨씬 현대적이다.

---

> **📚 Java/Kotlin 시선 ④ — Selenium ↔ Playwright**
>
> **Java (Selenium WebDriver)**
> ```java
> @Test
> public void testLogin() {
>     WebDriver driver = new ChromeDriver();
>     try {
>         driver.get("http://localhost:3000/login");
>         driver.findElement(By.id("email")).sendKeys("hong@example.com");
>         driver.findElement(By.id("password")).sendKeys("secret123");
>         driver.findElement(By.cssSelector("button[type='submit']")).click();
>
>         // 페이지 이동 기다리기
>         new WebDriverWait(driver, Duration.ofSeconds(10))
>             .until(ExpectedConditions.urlContains("/dashboard"));
>
>         String welcomeText = driver.findElement(By.className("welcome")).getText();
>         assertEquals("홍길동 님, 환영합니다!", welcomeText);
>     } finally {
>         driver.quit();
>     }
> }
> ```
>
> **TypeScript (Playwright)**
> ```typescript
> import { test, expect } from '@playwright/test';
>
> test('로그인 성공 후 대시보드로 이동한다', async ({ page }) => {
>   await page.goto('/login');
>
>   await page.getByLabel('이메일').fill('hong@example.com');
>   await page.getByLabel('비밀번호').fill('secret123');
>   await page.getByRole('button', { name: '로그인' }).click();
>
>   await expect(page).toHaveURL('/dashboard');
>   await expect(page.getByText('홍길동 님, 환영합니다!')).toBeVisible();
> });
> ```
>
> 차이가 분명하다. Selenium은 명시적인 대기(WebDriverWait)를 직접 관리해야 한다. Playwright는 기본적으로 자동 대기(auto-waiting)를 지원한다. 요소가 나타날 때까지, 클릭할 수 있을 때까지, 네트워크가 안정화될 때까지 자동으로 기다린다. 그리고 `getByLabel`, `getByRole` — Testing Library와 같은 철학이다. 접근성 기반으로 요소를 찾는다.
>
> 또 한 가지. Playwright는 Chromium, Firefox, WebKit(Safari) 세 엔진을 하나의 API로 지원한다. Selenium은 드라이버를 브라우저마다 관리해야 한다. Playwright의 브라우저 설치는 `npx playwright install` 한 줄로 끝난다.

---

Playwright의 설정 파일이 어떻게 생겼는지 살펴보자.

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,        // 모든 테스트 병렬 실행
  forbidOnly: !!process.env.CI, // CI에서 test.only() 금지
  retries: process.env.CI ? 2 : 0, // CI에서 실패 시 재시도
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry', // 재시도 시 추적 기록
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  webServer: {
    command: 'npm run build && npm run preview',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

`webServer` 옵션이 편리하다. E2E 테스트 실행 전에 개발 서버나 프리뷰 서버를 자동으로 시작하고, 테스트가 끝나면 종료한다. Java에서 Testcontainers로 서버를 띄우는 것과 비슷한 편의다.

### Page Object Model — 구조화된 E2E 테스트

E2E 테스트가 많아지면 코드 중복이 심해진다. "이메일 입력 → 비밀번호 입력 → 로그인 버튼 클릭" 흐름이 여러 테스트에서 반복된다. Page Object Model(POM) 패턴으로 이 중복을 해소할 수 있다.

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('이메일');
    this.passwordInput = page.getByLabel('비밀번호');
    this.loginButton = page.getByRole('button', { name: '로그인' });
    this.errorMessage = page.getByTestId('error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

// e2e/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('로그인', () => {
  test('성공적으로 로그인한다', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('hong@example.com', 'secret123');

    await expect(page).toHaveURL('/dashboard');
  });

  test('잘못된 비밀번호로 로그인 시 에러', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('hong@example.com', 'wrong');

    await expect(loginPage.errorMessage).toBeVisible();
    await expect(loginPage.errorMessage).toContainText('이메일 또는 비밀번호가 올바르지 않습니다');
  });
});
```

Page Object가 TypeScript의 클래스와 자연스럽게 맞다. `Locator` 타입이 명확하고, IDE 자동완성이 잘 작동한다. 테스트 코드가 비즈니스 흐름 중심으로 읽힌다.

### Cypress와의 비교

Playwright 말고 Cypress도 많이 쓰인다. 2018년경 Selenium의 대안으로 등장해 개발자 경험을 크게 개선했다. 둘을 비교하면 이렇다.

```
Playwright의 장점:
- Microsoft 지원, TypeScript 일급 지원
- Chromium + Firefox + WebKit 동시 지원
- 더 빠른 실행 (특히 병렬 실행)
- 네트워크 인터셉트, API 모킹 내장
- 자동 대기가 더 정교함

Cypress의 장점:
- 실시간 리로드 개발 경험 (테스트 작성 시 즉각 피드백)
- GUI 기반 디버거가 직관적
- 컴포넌트 테스트 지원 (Vitest + Testing Library와 경쟁)
- 한국 커뮤니티 자료가 Playwright보다 많음(2024년 기준)
```

신규 프로젝트라면 Playwright를 선택하는 편이 낫다. Microsoft의 지원, TypeScript 친화성, 세 브라우저 엔진 지원이 강점이다. 기존 Cypress 코드베이스가 있다면 마이그레이션 비용을 따져보고 결정해야 한다.

---

## API 계약 테스트 — 타입 수준의 계약

13장에서 Hono와 tRPC를 다뤘다. 이 도구들의 강점 중 하나가 서버와 클라이언트 사이의 타입 수준 계약이다. 그 계약을 테스트로 검증하는 패턴을 살펴보자.

### Hono RPC + Vitest

Hono의 RPC 클라이언트는 서버 라우트 정의에서 타입을 자동으로 추론한다. 클라이언트에서 잘못된 요청을 보내면 컴파일 타임에 에러가 난다. 이 타입 계약 자체를 테스트할 수 있다.

```typescript
// server/routes/users.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const UserCreateSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export const userRoutes = new Hono()
  .post('/users', zValidator('json', UserCreateSchema), async (c) => {
    const body = c.req.valid('json');
    // body의 타입은 자동으로 { name: string; email: string }
    const user = await createUser(body);
    return c.json(user, 201);
  })
  .get('/users/:id', async (c) => {
    const id = Number(c.req.param('id'));
    const user = await findUser(id);
    if (!user) return c.json({ error: 'Not Found' }, 404);
    return c.json(user);
  });
```

```typescript
// server/routes/users.test.ts
import { describe, it, expect } from 'vitest';
import { testClient } from 'hono/testing';
import { userRoutes } from './users';

describe('User API', () => {
  const client = testClient(userRoutes);

  it('POST /users — 사용자를 생성한다', async () => {
    const res = await client.users.$post({
      json: { name: '홍길동', email: 'hong@example.com' },
    });

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.name).toBe('홍길동');
  });

  it('POST /users — 잘못된 이메일은 400을 반환한다', async () => {
    const res = await client.users.$post({
      // @ts-expect-error — email 형식 오류: 타입 수준에서도 에러
      json: { name: '홍길동', email: 'not-an-email' },
    });
    // 런타임 검증도 실패해야 함
    expect(res.status).toBe(400);
  });
});
```

`testClient`가 편리하다. 실제 HTTP 서버를 띄우지 않고 Hono 앱을 직접 호출한다. 빠르고, 네트워크 의존이 없다. 그리고 `client.users.$post({ json: ... })`에서 `json`의 타입이 서버 스키마와 연동되어 있어, 잘못된 값을 넘기면 컴파일 타임에 에러가 난다.

### tRPC + Vitest

tRPC는 한 걸음 더 나아간다. 별도 스키마나 코드 생성 없이 순수 TypeScript 타입으로 서버와 클라이언트를 연결한다.

```typescript
// server/router.ts
import { initTRPC } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.create();

export const appRouter = t.router({
  user: t.router({
    getById: t.procedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input }) => {
        return { id: input.id, name: '홍길동', email: 'hong@example.com' };
      }),
    create: t.procedure
      .input(z.object({ name: z.string(), email: z.string().email() }))
      .mutation(async ({ input }) => {
        return { id: 1, ...input };
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

```typescript
// server/router.test.ts
import { describe, it, expect } from 'vitest';
import { createCallerFactory } from '@trpc/server';
import { appRouter } from './router';
import { expectTypeOf } from 'vitest';

const createCaller = createCallerFactory(appRouter);

describe('tRPC user router', () => {
  const caller = createCaller({});

  it('user.getById — 사용자를 반환한다', async () => {
    const user = await caller.user.getById({ id: 1 });
    expect(user.id).toBe(1);
    expect(user.name).toBe('홍길동');
  });

  it('user.getById — 반환 타입 검증', async () => {
    const user = await caller.user.getById({ id: 1 });
    // 런타임 값 검증
    expect(typeof user.id).toBe('number');
    // 타입 수준 검증
    expectTypeOf(user).toMatchTypeOf<{ id: number; name: string; email: string }>();
  });

  it('user.create — 사용자를 생성한다', async () => {
    const user = await caller.user.create({
      name: '김철수',
      email: 'kim@example.com',
    });
    expect(user.name).toBe('김철수');
  });
});
```

`createCaller`가 HTTP 없이 라우터를 직접 호출한다. 테스트가 빠르고 간단하다. `expectTypeOf`로 반환 타입까지 검증하면 런타임과 컴파일 타임을 동시에 커버한다.

---

## CI에서의 typecheck — `tsc --noEmit`을 테스트 스텝으로

테스트 파이프라인에서 놓치기 쉬운 스텝이 있다. TypeScript 타입 검사를 별도 CI 스텝으로 명시적으로 추가하는 것이다.

Vitest는 TypeScript를 esbuild로 트랜스파일해서 실행한다. 빠르지만, 타입 검사를 하지 않는다. 타입 에러가 있어도 Vitest는 그냥 실행한다. 마찬가지로 Vite로 빌드할 때도 기본적으로 타입 검사를 하지 않는다.

```bash
# 이 명령은 타입 에러를 잡아준다
tsc --noEmit
```

`--noEmit` 옵션은 컴파일된 JS 파일을 생성하지 않고 타입 검사만 한다. 이 명령을 CI 파이프라인에 별도 스텝으로 추가해야 한다.

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      # 타입 검사 — 별도 스텝
      - name: TypeScript 타입 검사
        run: npx tsc --noEmit

      # 단위 테스트
      - name: Vitest 단위 테스트
        run: npx vitest run

      # E2E 테스트
      - name: Playwright E2E 테스트
        run: npx playwright install --with-deps && npx playwright test
```

이 세 스텝이 모두 통과해야 PR이 머지될 수 있어야 한다. `tsc --noEmit`이 없으면 타입 에러가 있는 코드가 CI를 통과해버리는 찜찜한 상황이 생긴다.

`package.json`에도 스크립트를 명확히 정의해두는 편이 낫다.

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "ci": "npm run typecheck && npm run test:run && npm run test:e2e"
  }
}
```

`npm run ci`가 타입 검사, 단위 테스트, E2E 테스트를 순서대로 실행한다. 로컬에서도 PR을 올리기 전에 이 명령을 한 번 돌려보는 습관을 들이면 좋다.

### 타입 검사 성능 개선

대규모 프로젝트에서 `tsc --noEmit`이 느리게 느껴질 수 있다. 몇 가지 방법이 있다.

**`tsc --incremental --noEmit`** — 이전 빌드 결과를 캐시해 변경된 파일만 다시 검사한다. `tsconfig.json`에 `"incremental": true`를 추가하면 `.tsbuildinfo` 파일을 생성해 캐시를 유지한다.

```json
// tsconfig.json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo",
    "noEmit": true
  }
}
```

**`project references`** — 13장 모노레포 섹션에서 언급한 프로젝트 참조를 쓰면 하위 패키지를 독립적으로 타입 검사할 수 있다. 변경이 없는 패키지는 캐시된 결과를 쓴다.

**2025년 이후: TypeScript Native** — Microsoft가 2025년 발표한 Go 언어로 재작성된 TypeScript 컴파일러(코드명 TypeScript Native 또는 TypeScript Go)는 기존 대비 10배 빠른 속도를 목표로 한다. 이것이 안정화되면 `tsc --noEmit`의 속도 문제는 자연스럽게 해소될 가능성이 높다.

---

## 테스트 전략 전체 그림

테스트 도구들을 나열했으니 어떻게 조합할지 전략을 정리하자. Java/Spring 프로젝트에서 테스트 피라미드를 설계하듯, TS 프로젝트에서도 레이어를 나눈다.

```
         /\
        /E2E\          ← Playwright (소수, 핵심 사용자 흐름)
       /------\
      /통합 테스트\      ← Vitest + Hono testClient / tRPC caller (중간)
     /------------\
    /  컴포넌트 테스트 \  ← Vitest + Testing Library (React 컴포넌트)
   /------------------\
  /    단위 테스트      \  ← Vitest (많음, 빠름)
 /----------------------\
/     타입 단위 테스트    \  ← expectTypeOf, @ts-expect-error (복잡한 타입마다)
/------------------------\
     typecheck
     tsc --noEmit          ← CI에서 항상
```

타입 단위 테스트는 피라미드의 별도 레이어라기보다 기반이다. 복잡한 타입 유틸리티를 만들 때마다 함께 작성하는 게 바람직하다. `expectTypeOf`는 코드 비용이 낮다 — 런타임이 없고, 빠르고, 단 두 줄로 타입 계약을 명문화할 수 있다.

현실적인 선택을 정리하면 이렇다.

```
신규 프로젝트 기준 추천 스택:
- 타입 검사: tsc --noEmit (CI 필수 스텝)
- 단위·통합 테스트: Vitest
- 타입 단위 테스트: Vitest의 expectTypeOf (또는 expect-type)
- 컴포넌트 테스트: Vitest + Testing Library
- E2E: Playwright
- 프로퍼티 기반: fast-check (필요한 경우)
```

---

## 🚧 함정 박스 — 타입 테스트의 흔한 실수들

**함정 1: `@ts-expect-error`와 `@ts-ignore` 혼동**

증상: 타입 에러를 억제하려고 `@ts-ignore`를 썼는데, 실제로 에러가 없는 코드에도 붙어있어 아무런 의미 없이 남아 있다.

원인: `@ts-ignore`는 에러 유무와 관계없이 다음 줄을 무조건 무시한다. `@ts-expect-error`는 에러가 있어야 하고, 에러가 없으면 오히려 컴파일 에러를 낸다.

처방: 타입 에러를 의도적으로 검증할 때는 `@ts-expect-error`를 써야 한다. 임시로 에러를 억제할 때만 `@ts-ignore`를 쓰되, 주석으로 이유를 명시하는 편이 낫다.

**함정 2: vi.fn() 타입이 any로 추론됨**

증상: `vi.fn()`으로 만든 mock 함수가 `MockedFunction<any>`가 되어 매개변수나 반환 타입이 전혀 검증되지 않는다.

원인: 타입 매개변수를 명시하지 않으면 any로 추론된다.

처방:
```typescript
// 나쁜 예
const mockSave = vi.fn();

// 좋은 예
const mockSave = vi.fn<(user: User) => Promise<void>>();
// 또는
const mockSave: MockedFunction<(user: User) => Promise<void>> = vi.fn();
```

**함정 3: vi.mock() 경로가 절대 경로여야 하는 경우**

증상: `vi.mock('./userRepository')`가 작동하지 않거나, mock이 적용되지 않는다.

원인: `vi.mock()`의 경로 해석은 tsconfig의 `paths` 별칭을 항상 인식하지는 않는다. `vi.mock('@/repository/user')`처럼 별칭 경로를 쓰면 실패하는 경우가 있다.

처방: `vite.config.ts`의 `resolve.alias`와 `vitest.config.ts`의 설정을 일치시켜야 한다. 또는 mock 경로를 상대 경로로 명시한다.

**함정 4: E2E 테스트에서 auto-waiting을 믿지 못해 불필요한 sleep 추가**

증상: `await page.waitForTimeout(2000)` 같은 하드코딩된 대기가 테스트 곳곳에 있다. 테스트가 느리고 불안정하다.

원인: Playwright의 auto-waiting을 이해하지 못하거나, 특정 조건에서 신뢰하지 못할 때.

처방: `page.waitForTimeout`보다 `expect(locator).toBeVisible()`, `page.waitForURL()`, `page.waitForResponse()` 같은 조건 기반 대기를 써야 한다. 조건 기반 대기는 조건이 충족되면 즉시 다음으로 넘어가서 빠르다.

---

## 마무리

Java/Kotlin 개발자가 TS 테스트 생태계에서 마주치는 가장 큰 변화는 두 가지다.

하나는 *도구 선택의 자유*다. JUnit은 사실상 단일 표준이었다. TS에서는 Vitest와 Jest, Playwright와 Cypress 사이에서 팀이 선택을 해야 한다. 2025년 현재 기준으로 신규 프로젝트에는 Vitest + Playwright 조합이 합리적 디폴트다. 레거시 코드베이스라면 Jest를 유지하는 게 현실적일 수 있다.

다른 하나는 *타입 단위 테스트*라는 새로운 레이어다. `expectTypeOf`, `@ts-expect-error` — Java에는 없던 이 도구들은 처음엔 낯설지만, 복잡한 타입 유틸리티를 만들수록 그 가치가 분명해진다. 4·5장에서 공들여 만든 `DeepReadonly`, `ExtractRouteParams`, `z.infer` 같은 타입들이 실제로 의도한 모양인지 검증하는 방법은 `expectTypeOf`뿐이다.

기억해두자. `tsc --noEmit`을 CI 필수 스텝으로 두는 것, `vi.fn()`에 타입을 명시하는 것, `@ts-expect-error`로 타입 에러를 명시적으로 검증하는 것 — 이 세 가지 습관이 TS 테스트의 기반이다.

15장에서는 한국 현장에서 TS를 쓰다 마주치는 함정들을 더 넓은 시각으로 살펴본다. 이 장에서 다룬 테스트 패턴들, 그리고 4~13장의 모든 내용이 실제 팀에서 어떻게 충돌하고 어떻게 합의점을 찾는지 — 한국 개발자들의 생생한 경험으로 마지막 장을 채운다.

---

> **📖 더 깊이 가려면**
>
> - **Vitest 공식 문서** — https://vitest.dev/ : 설정 옵션, 고급 mocking 패턴, 스냅샷 테스트
> - **Testing Library 철학** — https://testing-library.com/docs/guiding-principles : "사용자가 소프트웨어를 사용하는 방식과 유사한 방식으로 테스트하라"의 원칙
> - **expect-type** — https://github.com/mmkal/expect-type : 타입 테스트 API 전체
> - **Playwright 공식 문서** — https://playwright.dev/ : Page Object Model, 네트워크 인터셉트, 병렬 실행 고급 설정
> - **fast-check 공식** — https://fast-check.io/ : Arbitrary 정의, shrinking 원리, 실전 예제
> - **Matt Pocock - Total TypeScript** — https://www.totaltypescript.com/ : 타입 단위 테스트를 포함한 고급 TS 타입 패턴의 현재 최고 자료 (영문)
> - **Hono testClient** — https://hono.dev/docs/guides/testing : Hono 앱을 HTTP 없이 테스트하는 패턴
