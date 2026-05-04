# 2장. JavaScript의 진짜 본성 — 타입을 붙이기 전에 알아야 할 것

Spring으로 백엔드만 짜다가 처음으로 브라우저 콘솔에 코드를 한 줄 넣어본다고 해보자. 별생각 없이 `[] + []`을 입력하고 엔터를 누른다. 결과는 빈 문자열이다. 이번에는 `[] + {}`를 넣어본다. `"[object Object]"`라는 이상한 문자열이 돌아온다. 자, 한 번 더. `{} + []`. 이번에는 `0`이 나온다. 같은 두 피연산자인데 순서를 바꿨더니 결과의 *타입*이 바뀐다. 이쯤 되면 헛웃음이 난다. *"이게 진짜 프로그래밍 언어가 맞나?"*

마음을 좀 가라앉히고, 솔직히 짚어보자. 이 장난 같은 결과들은 누군가 일부러 만든 농담이 아니다. 1995년 5월의 어느 사무실에서, 한 사람이 10일이라는 시간 안에 만들어낸 언어가 30년이 지난 지금 우리 손까지 흘러왔을 뿐이다. 그 10일짜리 언어가 한두 해가 아니라 30년을 살아남았고, 지금은 지구상에서 *가장 많이 실행되는* 코드의 정체다. 그 사실을 무시한 채 *"농담 같은 언어"*로만 보면, 그 위에 얹은 TypeScript도 끝내 손에 잡히지 않는다.

이 장은 TypeScript를 본격적으로 펴기 전에, 그 토대인 JavaScript의 형태를 먼저 보자는 장이다. 객체는 어떻게 생겼는지, `this`라는 단어 하나가 왜 이렇게 많은 얼굴을 가지는지, 단일 스레드로 어떻게 비동기를 돌리는지, 그리고 빈 값을 표현하는 키워드가 왜 두 개나 있는지. 정적 타입 언어로 잔뼈가 굵은 사람일수록 이 토대를 *대충* 넘기고 싶어진다. *"어차피 TS로 가릴 거 아닌가?"* 하는 마음이 든다. 솔직히 자연스러운 마음이다. 하지만 잠시만 참고 함께 들여다보자. 이 장의 내용을 알지 못하면, 앞으로 모든 함정 박스가 *"왜 이런 일이 생기지?"*에서 멈춘다. 알고 보면, 모든 함정의 뿌리가 이 장 어딘가에 있다.

## JS의 짧은 역사 — 10일이 만든 결정들

JavaScript의 탄생 이야기는 이미 너무 많이 회자되어, 설명이 늘 양극단으로 흐른다. 한쪽은 *"10일 만에 만든 언어가 어떻게 제대로일 수 있겠어"* 식의 가벼운 비웃음이고, 다른 한쪽은 *"그래도 결국 살아남았으니 위대하다"* 식의 낭만화다. 둘 다 우리 작업에는 별 도움이 안 된다. 우리에게 필요한 건 사실관계다. *어떤 환경에서, 어떤 결정이 내려졌고, 그 결정의 그림자가 지금까지 어떻게 드리워져 있는가.* 그 정도다.

1995년, 넷스케이프(Netscape)는 곤란한 상황에 있었다. Mosaic의 후계자로 부상한 이 회사의 브라우저에는 *움직이는 페이지*를 만들 수단이 없었다. 마이크로소프트가 같은 시기 Internet Explorer로 뒤를 쫓아오고 있었고, Sun의 Java는 막 등장한 신예로 모두가 들떠 있었다. 넷스케이프는 *"브라우저 안에서 돌아가는 가벼운 스크립팅 언어"*가 필요하다고 판단했다. 한쪽에서는 Sun의 Java를 페이지 안에 끼워 넣자는 의견이 있었고, 다른 쪽에서는 *"디자이너와 비전공자도 쓸 수 있는 더 가벼운 언어가 필요하다"*는 주장이 있었다. 결과적으로 둘 다 했다. Java는 애플릿 형태로 끼워 넣고, 더 가벼운 스크립팅 언어를 새로 만들기로 했다.

그 새 언어 만들기가 브렌던 아이크(Brendan Eich)에게 떨어졌다. 그에게 주어진 시간은 10일이었다. 정확히는, 10일 안에 *프로토타입을 돌아가게 만들어* 시연할 수 있어야 했다. 게다가 위에서 내려온 비공식적 지시가 두 가지 더 있었다. 첫째, *"Java처럼 보여야 한다."* 마케팅상 그래야 했다. 그래서 문법은 C/Java 계열로 잡았다. 중괄호와 세미콜론, `if/for/while`이 같은 모양이다. 둘째, *"하지만 객체 모델은 더 유연해야 한다."* 아이크 본인은 함수형 언어 Scheme의 팬이었고, 거기에 Self 언어의 *프로토타입 기반 객체 모델*에 매료되어 있었다. 그래서 안쪽 모델은 prototype과 일급 함수로 끌고 갔다.

이 결정이 지금까지 남는다. *겉모습은 Java처럼, 속은 Scheme + Self처럼.* 우리가 `class` 키워드를 보고 *"아, Java처럼 객체지향이구나"* 싶다가 막상 `this`가 사라지는 순간 멘붕에 빠지는 이유가 여기 있다. 겉포장과 내용물이 다른 것이다. 누구의 잘못도 아니다. 1995년의 사정이 그랬다.

10일짜리 시연은 통과되었다. 언어의 이름은 처음에 Mocha, 다음에는 LiveScript, 그리고 같은 해 12월 Sun과의 마케팅 협약을 통해 JavaScript로 굳어졌다. 이 이름이 지금까지도 혼란을 만든다. *"자바스크립트는 자바와 무슨 관계인가요?"* 하는 질문을 해마다 신입 개발자에게 받는다. 답은 *"이름 빼고 거의 없다"*이다. C와 C++이 가족이라면, Java와 JavaScript는 *햄과 햄스터*만큼 멀다.

그 다음에 일어난 일들도 짧게만 짚어두자. 1996년 마이크로소프트가 IE 3에 JScript라는 이름의 호환 언어를 넣었다. 두 진영이 서로 다른 방향으로 확장하기 시작하자, 표준화가 필요해졌다. 그 결과가 1997년의 ECMA-262, 즉 *ECMAScript* 표준이다. 그래서 우리가 *"ES2015"*, *"ES2020"*이라고 부르는 것은 모두 이 ECMA 표준의 판본 번호다. 언어의 공식 이름은 ECMAScript이고, JavaScript는 그 구현체의 마케팅 이름인 셈이다. 다만 이 책에서는 관행대로 둘을 섞어 쓰겠다. 누구도 *"엑마스크립트로 짠다"*고 말하지 않으니까.

표준이 잡힌 뒤로도 한참은 조용했다. 2000년대 초반의 IE 6 시대를 기억하는 사람이라면 알 것이다. 그 무렵의 JS는 *알림창 띄우기*와 *폼 검증* 정도의 역할만 했다. 본격적으로 다시 살아난 건 2004년 Gmail, 2005년 Google Maps가 *"브라우저 안에서 진짜 애플리케이션이 돌아간다"*는 것을 보여준 다음부터다. 곧이어 jQuery가 등장해 브라우저 호환성 지옥을 정리했고, 2009년에는 라이언 달(Ryan Dahl)이 V8 엔진을 서버로 끌어내려 Node.js를 만들었다. 이때부터 JS는 브라우저를 떠나 서버, CLI, 데스크톱, 모바일까지 영토를 넓힌다.

이 *팽창*이 우리에게 의미하는 바는 분명하다. 1995년의 *"브라우저 안에서 잠깐 도는 스크립트"*용으로 내린 결정들이, 지금은 은행의 트랜잭션 코드와 결제 게이트웨이의 한복판을 책임지고 있다는 뜻이다. 그래서 그 결정들의 무게가 처음 10일과는 비교할 수 없을 만큼 커졌다. TypeScript는 바로 이 *팽창된 JS의 무게*를 감당하기 위해 등장한 도구다. 그 사실을 머리에 넣어두면, 앞으로 우리가 만나는 *"왜 이렇게 했지?"*의 답이 늘 같다. *"그때는 그게 합리적이었다. 지금은 그 위에서 살아남아야 한다."* 자, 그러면 본격적으로 그 결정들을 하나씩 들춰보자.

## 프로토타입이라는 진짜 객체 모델

`class` 키워드부터 시작하자. JavaScript의 `class`는 ES2015(ES6)에 들어왔다. 그 전까지는 객체지향 비슷한 것을 짜고 싶으면 `function`과 `prototype`이라는 단어를 직접 굴려야 했다. 자, 그렇다면 `class`가 들어왔으니 이제 Java처럼 클래스 기반 언어가 된 거 아닌가? 그렇다면 이 책이 굳이 prototype을 다룰 필요가 있을까?

답은 단호하게 *"있다"*이다. 이유는 단순하다. **JS의 `class`는 Java의 `class`가 아니다.** 그것은 prototype 위에 *그럴듯한 옷을 입힌* 문법 설탕(syntax sugar)일 뿐이다. 옷을 입혔다고 안쪽이 바뀐 건 아니다. 우리가 `class`로 짠 코드도 결국 prototype 메커니즘 위에서 돈다. 평소에는 그 사실을 잊고 살 수 있다. 하지만 어느 날 갑자기 *"왜 이 메서드가 이 객체에 있지?"*, *"왜 이 인스턴스의 메서드를 다른 객체에 붙여 넣었더니 동작이 다르지?"* 같은 질문 앞에 서면, 결국 prototype을 알아야 답이 나온다.

직접 보자. 다음은 가장 단순한 클래스 정의다.

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, I am ${this.name}`;
  }
}

const dog = new Animal("Rex");
console.log(dog.greet()); // "Hello, I am Rex"
```

여기까지는 누구나 *"Java처럼 생겼군"* 싶다. 하지만 이 객체의 안쪽을 한 번 들여다보자.

```javascript
console.log(Object.keys(dog));        // ["name"]
console.log(dog.greet);               // [Function: greet]
console.log(dog.hasOwnProperty("greet")); // false
console.log(dog.hasOwnProperty("name"));  // true
```

이게 첫 번째 충격이다. `dog`라는 인스턴스가 분명 `greet()`를 호출할 수 있는데, *그 메서드는 인스턴스의 소유물이 아니다.* `name`은 인스턴스의 자기 속성이지만, `greet`는 그렇지 않다. 그렇다면 `greet`는 어디 있는가? 이름이 prototype이라는 별도의 객체에 있다.

```javascript
console.log(Object.getPrototypeOf(dog) === Animal.prototype); // true
console.log(Animal.prototype.greet);   // [Function: greet]
console.log(Animal.prototype.hasOwnProperty("greet")); // true
```

조금 더 직관적인 단서를 주는 코드를 보자.

```javascript
console.log(dog.__proto__);                    // Animal {}
console.log(dog.__proto__ === Animal.prototype); // true
console.log(dog.__proto__.__proto__);          // [Object: null prototype] {}
console.log(dog.__proto__.__proto__.__proto__); // null
```

이 출력이 핵심이다. JavaScript의 모든 객체는 *prototype 체인*이라는 사슬에 매달려 있다. `dog`는 자기 자신을 가지고 있고, 그 위로 `Animal.prototype`이라는 객체를 부모처럼 올려두고, 그 위에는 `Object.prototype`이 있고, 그 위는 `null`이다. 우리가 `dog.greet()`을 호출하면, 자바스크립트 엔진은 다음 순서로 메서드를 찾는다. 먼저 `dog` 자기 자신을 본다. 없다. 그 위 `Animal.prototype`을 본다. 있다. 그것을 호출한다. 즉, *상속처럼 보이는 것이 사실은 프로퍼티 탐색 알고리즘이다.* 

이 차이가 왜 중요할까? 첫째, 메서드가 인스턴스의 소유가 아니므로, 다른 객체에 *떼다 붙일 수 있다*. 이게 곧이어 보게 될 `this` 문제의 뿌리다. 둘째, 클래스를 정의한 *뒤에도* prototype에 메서드를 추가할 수 있다. Java에서는 상상도 못 할 일이다.

```javascript
Animal.prototype.bark = function () {
  return `${this.name} barks!`;
};

console.log(dog.bark()); // "Rex barks!" — 이미 만든 dog에도 갑자기 bark가 생긴다.
```

이걸 *멍키 패칭(monkey patching)*이라 부른다. 들으면 멋있어 보이지만 실제로는 *지저분한 일을 슬쩍 끼워 넣는 행위*에 가깝다. 라이브러리들이 이걸 함부로 쓰면 어떤 일이 벌어질지 상상해보자. 한 라이브러리가 `Array.prototype`에 `last()`를 추가했는데, 다른 라이브러리도 똑같이 `last()`를 추가했다고 해보자. 두 라이브러리 모두를 의존성에 가진 프로젝트에서는, 어느 라이브러리가 *늦게 로드되는지*에 따라 동작이 바뀐다. 그것도 에러 없이 조용히. 끔찍한 일이다. 그래서 현대 JS 커뮤니티는 *"내장 prototype에는 손대지 말자"*는 강한 합의를 가지고 있다. ECMAScript 표준에 새 메서드(`Array.prototype.findLast` 같은 것)를 추가할 때조차, 기존 라이브러리의 prototype 패치와 충돌하지 않도록 *조사를 거친다*. 그만큼 prototype의 자유도는 양날의 검이다.

> ### 📚 Java/Kotlin 시선 박스 ① — 화살표 함수 vs Kotlin 람다
>
> | Kotlin | TypeScript/JavaScript |
> |---|---|
> | `val add = { a: Int, b: Int -> a + b }` | `const add = (a: number, b: number) => a + b;` |
> | `list.map { it * 2 }` | `list.map(x => x * 2)` |
> | `list.forEach { println(it) }` | `list.forEach(x => console.log(x));` |
>
> 표면만 보면 거의 똑같다. 둘 다 일급 함수이고, 둘 다 콜렉션 메서드 인자로 쉽게 넘어간다. 하지만 한 발만 더 들어가면 이야기가 달라진다.
>
> Kotlin의 람다는 그 자체로 *객체*다. 컴파일되면 `Function1`, `Function2` 같은 함수형 인터페이스의 익명 인스턴스가 된다. 람다 안에서 `this`는 *바깥 스코프의 `this`*를 가리키고, `it`은 단일 인자 람다의 약속된 이름이다. 명확하고 예측 가능하다.
>
> JS의 화살표 함수는 표면이 짧다는 점에선 닮았지만, 더 큰 의미는 *바깥의 `this`를 그대로 가져온다(lexical this)*는 데 있다. 일반 `function`으로 쓴 익명 함수와 구별되는 가장 큰 차이가 이것이다. *왜 굳이 이 구별을 만들었나?* 하는 의문은, 다음 절의 `this` 7가지 얼굴을 보고 나면 자연스럽게 풀린다. 한 줄로 미리 말하면, *일반 함수의 `this`가 너무 자주 사라져서, 사라지지 않는 형태가 따로 필요했다*는 것이 답이다.

자, 그러면 그 *사라지는 `this`*를 직접 만나보자.

## `this`의 7가지 얼굴

JavaScript에서 가장 많은 신입 개발자가 좌절하는 단어를 하나만 꼽으라면, 거의 확실히 `this`다. Java/Kotlin에서 `this`는 *현재 인스턴스*다. 끝이다. 그 외 다른 의미는 없다. JavaScript에서 `this`는 *호출되는 방식에 따라 매번 달라진다.* 같은 함수를 다른 방식으로 호출하면 `this`가 다른 것을 가리킨다. 처음 듣는 사람에게는 거의 사기처럼 들리지만, 사실이다. 자, 7가지 얼굴을 하나씩 보자.

### 얼굴 1: 일반 함수 호출

가장 단순한 경우다. 함수를 그냥 호출하면 `this`는 무엇을 가리킬까?

```javascript
function whoAmI() {
  return this;
}

console.log(whoAmI());
// 비엄격 모드: 브라우저면 window, Node.js면 global
// 엄격 모드('use strict'): undefined
```

당황스럽다. *"내 함수는 누구의 메서드도 아닌데 왜 `this`가 있지?"* 하는 질문이 자연스럽다. 1995년의 결정 때문이다. JS는 *모든 함수에 `this`가 있게 만들었다*. 비엄격 모드에서는 그 기본값이 전역 객체(브라우저의 `window`, Node의 `global`)였고, 엄격 모드(2009년 ES5에서 등장)에서는 `undefined`로 강제된다. 현대 코드는 거의 모두 엄격 모드를 쓰니, 그냥 *호출되는 함수의 `this`는 `undefined`*라고 외워두면 된다. 괜찮다. 다음 얼굴들이 훨씬 더 어지럽다.

### 얼굴 2: 메서드 호출

이번엔 그 함수를 객체의 속성으로 두고 호출해보자.

```javascript
const obj = {
  name: "object",
  whoAmI() {
    return this;
  }
};

console.log(obj.whoAmI() === obj); // true
console.log(obj.whoAmI().name);    // "object"
```

이게 우리가 흔히 *"`this`는 자기 객체"*라고 알고 있는 모습이다. 메서드로 호출되면, `this`는 *그 메서드를 호출한 점(.) 앞의 객체*가 된다. 핵심은 *호출의 모양*이지, 함수가 *원래 누구 것인지*가 아니다. 다음 코드를 보자.

```javascript
const method = obj.whoAmI;
console.log(method()); // undefined (엄격 모드)
```

같은 함수다. 같은 `obj.whoAmI`다. 그런데 변수에 *저장*만 하고 `obj.` 없이 호출하면, `this`는 사라진다. 자바 출신 개발자에게 이 사실은 처음에 거의 받아들이기 어렵다. *"메서드 참조를 변수에 저장했는데 자기가 누구 것인지를 잊어버린다고?"* 그렇다. 잊어버린다. 호출 시점에 `obj.` 없이 부르는 순간, 그건 *그냥 함수 호출*이 된다. 메서드 호출이 아니라 일반 함수 호출이 되는 셈이다. 그래서 `this`는 얼굴 1로 돌아간다.

### 얼굴 3: 생성자 호출

`new` 키워드로 호출하면 또 달라진다.

```javascript
function Person(name) {
  this.name = name;
}

const alice = new Person("Alice");
console.log(alice.name); // "Alice"
console.log(alice instanceof Person); // true
```

`new`가 붙으면, 자바스크립트 엔진이 *새 빈 객체*를 만들어서 그것을 `this`로 함수에 넘긴다. 그리고 그 객체의 prototype을 `Person.prototype`으로 연결해 반환한다. 즉, `new`는 *"`this`로 새 객체를 깐다"*는 뜻이다. 이걸 잊고 `new` 없이 `Person("Alice")`라고 호출하면 어떻게 될까? 엄격 모드에서는 `this`가 `undefined`이므로 `this.name = name`에서 즉시 TypeError가 난다. 비엄격 모드에서는 *글로벌 객체에 `name` 속성이 슬쩍 추가되는* 끔찍한 일이 벌어진다. 다행히 ES2015 `class`로 정의된 생성자는 `new` 없이 호출하면 무조건 에러를 던진다. 그런 의미에서 `class`는 *조금 더 안전한 옷*이다.

### 얼굴 4: 화살표 함수 (lexical this)

화살표 함수는 자기 `this`를 갖지 않는다. *바깥 스코프의 `this`를 그대로 본다.*

```javascript
const obj = {
  name: "object",
  arrow: () => this,
  method() {
    return this;
  },
};

console.log(obj.arrow());  // undefined (모듈 스코프), 또는 globalThis
console.log(obj.method()); // obj
```

처음 보는 사람은 *"왜 `arrow()`도 메서드처럼 호출했는데 `this`가 `obj`가 아니지?"*라며 당황한다. 이유는 단순하다. 화살표 함수는 *호출 방식에 따라 `this`가 결정되지 않는다*. 정의된 위치의 바깥 `this`를 *닫아서(closure)* 가지고 있을 뿐이다. 위 예의 `arrow`는 모듈의 최상위에서 정의되었으므로, 그 바깥의 `this`(`undefined` 또는 `globalThis`)를 그대로 쓴다.

이 성질이 콜백에서 빛난다. 다음 패턴을 보자.

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }
  startWithFunction() {
    setInterval(function () {
      this.count++; // this는 undefined → TypeError
      console.log(this.count);
    }, 1000);
  }
  startWithArrow() {
    setInterval(() => {
      this.count++; // this는 Counter 인스턴스 → 잘 됨
      console.log(this.count);
    }, 1000);
  }
}
```

`startWithFunction`은 깨진다. 일반 함수가 콜백으로 들어가는 순간, 그 안의 `this`는 *콜백 호출자(여기서는 setInterval의 내부)*에 의해 결정되는데, 거기엔 우리 인스턴스를 알려줄 길이 없다. 화살표 함수로 바꾸면, `startWithArrow` 메서드의 `this`(즉 Counter 인스턴스)를 그대로 닫아 가져가므로 잘 동작한다. *이 패턴 하나가 화살표 함수의 존재 이유다.* 옛날 JS에서는 `var self = this` 같은 임시 변수에 `this`를 저장해 콜백 안에서 쓰던 관행이 있었다. 화살표 함수는 그 관행을 언어 차원에서 흡수한 것이다.

### 얼굴 5: bind / call / apply

`this`를 *명시적으로 지정해서* 함수를 부르고 싶을 때 쓰는 메서드들이다.

```javascript
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const alice = { name: "Alice" };

console.log(greet.call(alice, "Hi", "!"));   // "Hi, Alice!"
console.log(greet.apply(alice, ["Hi", "!"])); // "Hi, Alice!"

const greetAlice = greet.bind(alice, "Hi");
console.log(greetAlice("!"));  // "Hi, Alice!"
console.log(greetAlice("?"));  // "Hi, Alice?"
```

`call`과 `apply`는 즉시 호출하되 첫 인자로 `this`를 강제한다. 둘의 유일한 차이는 *나머지 인자를 펼쳐서 주는가, 배열로 주는가*다. `bind`는 즉시 호출하지 않고 *`this`가 영구적으로 묶인 새 함수를 돌려준다*. ES5 시절 콜백에 메서드를 넘길 때 `this`를 보존하기 위한 표준 기법이 `bind`였다. 지금은 화살표 함수가 더 흔하지만, `bind`는 여전히 *함수를 부분 적용(partial application)*하는 도구로 살아 있다.

### 얼굴 6: 클래스 메서드와 `this`

`class`로 짠 메서드 안의 `this`는 자연스럽게 인스턴스를 가리킨다. 단, *호출 방식이 메서드 호출일 때만*. 다음 예가 잘 보여준다.

```javascript
class Logger {
  constructor(prefix) {
    this.prefix = prefix;
  }
  log(message) {
    console.log(`${this.prefix}: ${message}`);
  }
}

const logger = new Logger("INFO");
logger.log("hello");                   // "INFO: hello"

const detached = logger.log;
detached("hello");                     // TypeError: Cannot read 'prefix' of undefined

setTimeout(logger.log, 1000, "hello"); // 마찬가지로 TypeError
setTimeout(() => logger.log("hello"), 1000); // 잘 됨
setTimeout(logger.log.bind(logger), 1000, "hello"); // 잘 됨
```

위 코드의 두 번째와 세 번째 줄을 잘 보자. 메서드를 *떼어내는 순간* `this`가 사라진다. 그래서 React 클래스 컴포넌트 시절에는 `this.handleClick = this.handleClick.bind(this)`를 생성자에 도배하던 시기가 있었다. 끔찍하게 번거로웠다. 지금은 *클래스 필드 + 화살표 함수*로 그 보일러플레이트를 줄인다.

```javascript
class Logger {
  constructor(prefix) {
    this.prefix = prefix;
  }
  log = (message) => {
    console.log(`${this.prefix}: ${message}`);
  };
}

const logger = new Logger("INFO");
const detached = logger.log;
detached("hello"); // "INFO: hello" — 잘 동작한다
```

`log`를 *메서드*가 아니라 *값이 화살표 함수인 인스턴스 필드*로 정의했다. 화살표 함수의 `this`는 정의된 위치(`Logger`의 인스턴스)에 묶이므로, 이제는 떼어내도 `this`가 사라지지 않는다. 다만 트레이드오프가 있다. 메서드는 prototype에 한 번만 정의되어 모든 인스턴스가 공유하지만, 클래스 필드 화살표 함수는 *인스턴스마다 별도의 함수 객체*가 만들어진다. 인스턴스가 수만 개 만들어지는 핫패스라면 메모리 차이가 의미 있게 난다. 일반 애플리케이션 코드에서는 무시해도 되는 차이지만, 알고는 있자.

### 얼굴 7: 콜백 안에서의 `this`

마지막 얼굴은 *콜백을 받는 함수가 명시적으로 `this`를 지정해줄 때*다. DOM의 `addEventListener`가 대표적이다.

```javascript
button.addEventListener("click", function (event) {
  console.log(this);          // button 자체
  console.log(event.target);  // button (대부분의 경우)
});

button.addEventListener("click", (event) => {
  console.log(this);          // 바깥 스코프의 this (대개 undefined)
  console.log(event.target);  // button
});
```

DOM은 *전통적 관행*에 따라, 일반 함수 콜백을 받으면 그 안의 `this`로 *이벤트가 발생한 요소*를 넘긴다. 화살표 함수를 쓰면 그 관행은 무시되고 lexical this가 적용된다. *어느 쪽이 옳은가?* 하는 질문은 의미가 없다. *어느 쪽을 의도했는가*가 의미 있는 질문이다. 이벤트 요소가 필요하면 일반 함수 또는 `event.currentTarget`을 쓰고, 외부 컴포넌트의 상태가 필요하면 화살표 함수를 쓴다. *일관된 선택이라면 어느 쪽이든 괜찮다.*

자, 7가지를 다 봤다. 머리가 어지러운가? 자연스러운 반응이다. 그래서 한국 커뮤니티에 가장 자주 올라오는 푸념 중 하나가 *"`this`만 안 만나면 JS는 할 만하다"*는 말이다. 이 사실을 뼈에 새겨두는 데 도움이 될 함정 박스를 하나 두자.

> ### 🚧 함정 박스 — `this`가 사라진다 (커뮤니티 패턴 3)
>
> **증상**
>
> ```javascript
> class UserService {
>   constructor() {
>     this.users = [];
>   }
>   load() {
>     fetch("/api/users")
>       .then(function (res) { return res.json(); })
>       .then(function (data) {
>         this.users = data; // TypeError: Cannot set 'users' of undefined
>       });
>   }
> }
> ```
>
> *Java라면 `this.users = data;`가 당연히 동작한다.* JS에서는 깨진다. 그 깨짐의 정체는 *콜백 함수 안의 `this`가 인스턴스가 아니다*라는 사실이다.
>
> **원인**
>
> `then(function (data) { ... })`의 `function`은 일반 함수다. 일반 함수가 콜백으로 호출되면 그 안의 `this`는 *호출자가 지정한 것* 또는 엄격 모드에서는 `undefined`다. Promise는 콜백을 그냥 호출하므로 `this`는 `undefined`다. *호출 방식에 따라 `this`가 결정된다*는 JS의 본성이 정확히 이 자리에 함정을 만든다.
>
> **처방**
>
> 처방은 셋 중 하나다.
>
> 1. **화살표 함수로 바꿔라.** 가장 단순하고 표준적이다.
>    ```javascript
>    .then((data) => {
>      this.users = data;
>    });
>    ```
> 2. **`bind`로 묶어라.** 콜백을 외부에서 받아온다면 어쩔 수 없을 때.
>    ```javascript
>    .then(handleData.bind(this));
>    ```
> 3. **`self` 임시 변수.** 옛 코드에서 자주 보이는 ES5 시대의 처방. 새 코드에는 가급적 쓰지 말자.
>    ```javascript
>    const self = this;
>    fetch(...).then(function (data) { self.users = data; });
>    ```
>
> 권유는 단순하다. *콜백 안에서 `this`를 쓸 일이 있으면 화살표 함수가 기본*이다. 일반 함수가 필요한 자리(이벤트 요소를 받고 싶은 경우 등)는 명확히 의도된 곳뿐이다.

> ### 📚 Java/Kotlin 시선 박스 ② — `this` 바인딩 vs Java 메서드 참조
>
> Java에서 `list.forEach(System.out::println)`이라고 쓰면, `System.out`은 메서드 참조의 *수신자*로 영구히 묶인다. 그 메서드 참조 객체를 어디로 옮기든, 그게 어떻게 호출되든, *`println`을 호출하는 객체는 항상 `System.out`이다*. 이 묶임은 자바 컴파일러가 보장한다.
>
> JS의 메서드 참조는 그렇지 않다. `const f = obj.method;`는 *`obj`와의 연결이 없는 그냥 함수 참조*다. 그래서 `f()`라고 부르면 `obj`는 사라진다. 자바의 메서드 참조처럼 동작하게 만들고 싶으면 직접 묶어야 한다. `const f = obj.method.bind(obj);` 또는 `const f = (...args) => obj.method(...args);` 같은 식이다.
>
> 이 차이의 뿌리는 결국 *언어 모델*이다. Java에서 메서드는 *클래스의 멤버*이고 메서드 참조는 *수신자가 결합된 함수형 인터페이스 인스턴스*다. JS에서 메서드는 *그냥 객체의 함수형 속성*이고, 함수 자체에는 어떤 객체에도 영구히 묶일 의무가 없다. 한쪽은 강한 결합을 기본으로 잡았고, 다른 쪽은 자유로운 연결을 기본으로 잡았다. 둘 다 그 나름의 일관성이 있다. 어느 쪽이 옳다고 말할 일은 아니다. *각자의 게임 규칙을 알자.*

이제 한 번 숨을 돌리자. `this`의 7가지 얼굴은 한 번에 다 외울 필요가 없다. 다만 *"호출 방식이 `this`를 결정한다"*는 한 문장만 머리에 박아두자. 이 문장 하나가 앞으로 만나는 모든 `this` 관련 함정의 자물쇠 열쇠다.

## 이벤트 루프 — 단일 스레드로 비동기를 돌리는 법

다음 토대는 동시성 모델이다. Java 백엔드 개발자는 동시성 하면 곧장 *스레드*를 떠올린다. `ExecutorService`로 풀을 만들고, `synchronized`로 임계 구역을 보호하고, `CompletableFuture`로 비동기를 잇는다. 멀티 스레드 위에서 자라온 사람의 본능이다.

자바스크립트는 그 본능을 정면으로 거스른다. **JavaScript는 단일 스레드로 돈다.** 메인 스레드 하나가 모든 것을 처리한다. 그런데도 fetch 요청 100개를 동시에 날리고, 그 결과를 모아 화면에 그릴 수 있다. 어떻게 가능한 일일까?

답은 *이벤트 루프*다. 이름부터 들여다보자. 이벤트 루프는 *해야 할 일이 든 큐(queue)를 끊임없이 빙빙 돌면서 하나씩 꺼내 실행하는* 구조다. 한 번에 하나씩 처리한다는 점에서 단일 스레드다. 하지만 *오래 걸리는 작업(I/O, 타이머, 네트워크 등)을 환경에 위임해두고, 결과가 도착하면 큐에 넣어 처리*함으로써 동시성을 흉내 낸다. 이걸 *비동기 단일 스레드 모델*이라고 부른다.

직접 확인해보자.

```javascript
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
```

이 코드의 출력 순서는 무엇일까? *"1, 2, 3, 4 순서대로?"* *"1, 4, 2, 3?"* *"1, 4, 3, 2?"* 정답은 마지막이다. **1, 4, 3, 2**.

왜 그럴까? 이벤트 루프의 큐는 사실 *둘로 나뉘어 있다*. 하나는 **마이크로태스크 큐(microtask queue)**, 다른 하나는 **매크로태스크 큐(macrotask queue)**다. Promise의 콜백은 마이크로태스크에 들어가고, `setTimeout`/`setInterval`/`setImmediate`/I/O 콜백은 매크로태스크에 들어간다. 그리고 이벤트 루프의 규칙은 단순하다.

1. 현재 실행 중인 동기 코드(콜 스택)가 다 비워질 때까지 기다린다.
2. 콜 스택이 비면, *마이크로태스크 큐를 모두 비울 때까지* 하나씩 꺼내 실행한다.
3. 마이크로태스크가 다 처리되면, *매크로태스크 큐에서 하나*만 꺼내 실행한다.
4. 그 매크로태스크가 또 마이크로태스크를 만들었다면, 다음 매크로태스크로 넘어가기 전에 새로 생긴 마이크로태스크들을 또 다 비운다.
5. 1번으로 돌아간다.

이 규칙을 위 코드에 적용해보자. `console.log("1")`이 동기 코드로 즉시 실행된다. 그 다음 `setTimeout`은 콜백을 매크로태스크 큐에 등록만 하고 넘어간다. 그 다음 `Promise.resolve().then`은 콜백을 마이크로태스크 큐에 등록만 하고 넘어간다. 그 다음 `console.log("4")`가 동기로 실행된다. 여기까지 출력은 *1, 4*. 이제 콜 스택이 비었으니, 이벤트 루프는 마이크로태스크 큐를 들여다본다. *3*이 출력된다. 그 다음 매크로태스크 큐로 가서 *2*가 출력된다. 끝.

조금 더 복잡한 경우를 보자.

```javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => {
  console.log("C");
  Promise.resolve().then(() => console.log("D"));
});
setTimeout(() => console.log("E"), 0);
console.log("F");
```

출력은? **A, F, C, D, B, E**.

A, F는 동기다. 그 다음 마이크로태스크 큐에 C가 있으니 C를 꺼낸다. C가 실행되는 도중 새 마이크로태스크 D가 등록된다. *마이크로태스크 큐는 비워질 때까지 계속 처리*되므로, 매크로태스크로 넘어가기 전에 D를 마저 처리한다. 그 다음에야 매크로태스크 큐로 가서 B, 그 다음 E.

이 규칙이 어떤 함의를 갖는지 조금만 음미해보자. **`setTimeout(fn, 0)`은 *지금 당장*이 아니라 *현재 동기 코드와 모든 마이크로태스크가 끝난 다음*에 실행된다.** 그래서 *"지금 잠깐 양보하고 다음 틱에 처리하자"*는 패턴에 종종 쓰인다. 하지만 더 큰 함의는 따로 있다. **마이크로태스크는 매크로태스크를 *굶길 수 있다*.** Promise 안에서 또 Promise를 만들고 그 안에서 또 Promise를 만들면, 마이크로태스크 큐가 영원히 비지 않을 수 있다. 그러면 매크로태스크는 영영 차례가 안 온다. UI가 멈추고, 타이머가 안 도는 *이상한 멈춤*이 발생한다. 이 시나리오는 잘 짠 코드에서는 잘 안 생기지만, 라이브러리가 무한 재귀에 빠졌을 때 가끔 본다.

자, 그러면 *오래 걸리는 작업*은 어떻게 처리할까? 답은 *환경에 위임한다*. 브라우저든 Node.js든, *호스트 환경*은 자바스크립트 엔진(V8 같은) 외에 별도의 스레드를 가지고 있다. fetch 요청, 파일 I/O, 타이머 같은 것은 호스트가 자기 스레드에서 처리한 뒤, 결과 콜백을 큐에 넣는다. 자바스크립트 엔진은 큐에서 꺼내 *자기 단일 스레드*에서 실행한다. 즉, *동시에 일어나는 일은 환경의 몫, 결과를 가지고 무엇을 할지는 JS의 몫*이다. CPU를 많이 쓰는 작업(이미지 변환, 큰 JSON 파싱 등)을 메인 스레드에서 돌리면 *모든 것이 멈춘다*. 그래서 그런 작업은 Web Worker(브라우저)나 Worker Threads(Node)로 보낸다. 이때조차도 메모리 공유는 매우 제한적이다. 데이터는 직렬화해서 보낸다.

> ### 📚 Java/Kotlin 시선 박스 ③ — 이벤트 루프 vs NIO/Reactor
>
> Java 진영에서 비동기를 진지하게 다룬 사람은 `Thread per request` 모델의 한계를 안다. 요청마다 스레드 하나를 잡으면, 동시 요청 수가 스레드 풀의 크기에 묶인다. 그래서 등장한 것이 NIO와 Reactor 패턴이다. *이벤트 루프 한 개가 여러 connection을 다중화*하고, 백엔드 작업은 별도의 워커 풀에서 처리한다. Netty, Vert.x, Project Reactor가 이 위에 서 있다.
>
> 이 모델의 핵심 직관이 정확히 JavaScript의 그것이다. *I/O는 이벤트 루프가 비동기로 처리하고, CPU 작업은 워커가 한다.* 다만 차이가 있다. Java의 Reactor는 *선택지의 하나*다. 전통적 스레드 모델과 공존한다. JS는 *유일한 모델*이다. 다른 길이 없다. 그래서 JS 라이브러리는 *모든 API가 비동기로 설계되어 있다*. 처음부터 끝까지 일관된 모델 위에 서 있다는 점이, JS 비동기의 강점이자 함정이다. 강점은 *예측 가능성*. 함정은 *동기 코드를 무심코 끼워 넣었을 때 모든 것이 멈춘다는 사실*이다.
>
> 한 가지 더 짚어두자. Java의 `CompletableFuture.thenApply`는 *콜백이 어느 스레드에서 실행될지가 모호하다*. `thenApplyAsync`로 명시하지 않으면, 호출 스레드인지 풀의 스레드인지가 상황에 따라 달라진다. JS의 Promise는 그런 모호함이 없다. *모든 콜백은 마이크로태스크 큐를 거쳐 메인 스레드에서 실행된다.* 단순함의 위안이 여기 있다.

## 빈 값이 두 개라는 사실 — null과 undefined

다음 함정으로 가자. Java에서 빈 값은 `null` 하나다. Kotlin에서는 `null`을 표현할 수 있는지를 타입 차원에서 분리(`String?`)했지만, 빈 값 자체는 여전히 `null`이다. JavaScript에는 빈 값이 둘이다. **`null`과 `undefined`.**

처음 들으면 *"왜 두 개나 필요해?"* 하는 의문이 든다. 합리적이다. 사실 둘은 *역사적 사고*에 가깝다. 하지만 30년 넘게 쓰여 온 결과, 두 값은 미묘하게 *다른 의미*를 가지게 되었다. 정리하면 이렇다.

- **`undefined`**: *값이 아직 할당되지 않았다*는 뜻. 변수를 선언만 하고 값을 안 줬을 때, 함수의 인자가 안 들어왔을 때, 객체의 없는 속성에 접근했을 때 모두 `undefined`다. *시스템이 알려주는 빈 값*이라고 생각하자.
- **`null`**: *프로그래머가 의도적으로 빈 값을 넣었다*는 뜻. 일부러 *"여기는 비어 있다"*고 표시하는 값이다.

직접 보자.

```javascript
let a;
console.log(a);                  // undefined — 시스템이 알려주는

const obj = {};
console.log(obj.foo);            // undefined — 없는 속성

function f(x) { console.log(x); }
f();                             // undefined — 안 들어온 인자

let b = null;
console.log(b);                  // null — 프로그래머가 의도적으로
```

문제는 *비교*다. `==`와 `===`가 둘을 다르게 다룬다.

```javascript
null == undefined;   // true  (느슨한 동등 비교)
null === undefined;  // false (엄격한 동등 비교)

null == 0;           // false (0과는 비교 안 함, 명시 규정)
undefined == 0;      // false
null < 1;            // true  (이건 또 0으로 변환된다…)
```

이 규칙을 다 외우려고 하지 말자. 그냥 *`==`은 쓰지 말자*가 답이다. **`===`만 쓰자.** 거의 모든 코드 가이드라인이 동의하는 한 줄 권고다. ESLint의 `eqeqeq` 규칙이 기본으로 켜져 있을 정도다. 단, *예외*가 있다. **`x == null`** 한 표현은 살아남았다. 이것이 *`x`가 `null`이거나 `undefined`이거나*를 한 줄로 검사하는 표준 관용구다. 다른 상황에서는 `===`만 쓰자. 이 규칙 하나로 99%의 비교 함정이 사라진다.

또 짚어둘 것이 있다. JS의 *falsy 값들*이다. `if (x) { ... }` 같은 조건문에서 *false로 평가되는* 값의 목록은 다음과 같다.

- `false`
- `0`, `-0`, `0n`(BigInt 0)
- `""`(빈 문자열)
- `null`
- `undefined`
- `NaN`

이게 끝이다. 나머지는 모두 truthy다. *빈 객체 `{}`도 truthy*, *빈 배열 `[]`도 truthy*다. Java/Kotlin 출신은 여기서 종종 발이 걸린다. *"빈 배열이면 false 아닌가?"* 아니다. 그래서 다음 코드가 의도와 다르게 동작한다.

```javascript
const items = [];
if (items) {
  console.log("뭔가 있다"); // 출력된다 — 빈 배열도 truthy
}
```

원했던 의도는 보통 *"items에 원소가 있으면"*이다. 그러면 `items.length > 0`이라고 명시하자. 이런 명시성은 *번거롭게* 느껴질 수 있지만, *찜찜한 동작*보다는 낫다.

`null`과 `undefined`를 한꺼번에 다루는 현대 JS의 두 연산자도 이 자리에서 짚어두자. ES2020부터 들어온 *옵셔널 체이닝(`?.`)과 nullish 병합(`??`)*이다.

```javascript
const user = { profile: null };

console.log(user?.profile?.name);  // undefined (에러 안 남)
console.log(user?.profile?.name ?? "익명"); // "익명"

// ||와 ??의 차이
console.log(0 || "기본값");  // "기본값" (0이 falsy)
console.log(0 ?? "기본값");  // 0      (0은 nullish가 아님)
console.log("" || "기본값"); // "기본값"
console.log("" ?? "기본값"); // ""
```

`??`는 *`null` 또는 `undefined`일 때만* 오른쪽 값을 사용한다. `||`는 *모든 falsy 값*에 대해 오른쪽을 사용한다. 둘은 비슷해 보이지만 명확히 다르다. *"숫자 0이나 빈 문자열은 유효한 값으로 인정하고 싶을 때"*는 `??`를 쓰자. 이 두 연산자의 등장으로 옛날의 `if (x !== null && x !== undefined && x.profile && x.profile.name)` 같은 길고 추한 검사가 사라졌다. JavaScript 진영에서 *드물게 모두가 환영한 문법 추가*였다.

Kotlin과 비교하면 사고방식이 비슷해진다. Kotlin의 `?.`과 `?:`는 사실상 같은 기능을 한다. 다만 Kotlin은 *타입 시스템 차원에서* `String?`과 `String`을 갈라놓고 강제한다. JS에는 그런 강제가 없다. 그래서 *모든 변수가 잠재적으로 nullable*이다. TypeScript의 `strictNullChecks`가 이 약점을 메우러 들어오는 것이지만, 그 이야기는 4장에서 본격적으로 한다.

## 함수가 일급 시민이라는 사실

이번 절은 짧지만 *"왜 JS 라이브러리는 이렇게 생겼나"*에 대한 답이다. 한 단어로 요약하면, **함수가 일급 시민(first-class citizen)이라는 사실**이다.

일급 시민이라는 말은 거창하지만, 뜻은 단순하다. *함수를 변수에 담을 수 있고, 인자로 넘길 수 있고, 반환값으로 받을 수 있다.* 그게 전부다. Java도 람다와 메서드 참조가 들어온 8 이후로는 *비슷한 일을* 할 수 있다. 다만 Java에서는 *함수형 인터페이스*라는 *옷을 입혀서야* 함수를 1급으로 다룰 수 있다. `Function<T, R>`, `Consumer<T>`, `Supplier<T>` 같은 인터페이스의 인스턴스로 함수를 들고 다닌다. JS에서는 그런 옷이 필요 없다. 함수는 그냥 *함수 객체*다. 어떤 타입이라는 의식 없이 변수에 담는다. *이 차이가 라이브러리 설계를 바꾼다.*

예를 들어, Express의 라우터는 다음처럼 생겼다.

```javascript
app.get("/users/:id", (req, res) => {
  res.json({ id: req.params.id });
});
```

`(req, res) => { ... }`라는 *함수를 그냥 인자로 넘긴다*. Spring의 `@RestController + @GetMapping("/users/{id}")` 모델과 비교하면 인상이 매우 다르다. Spring은 *클래스 안의 메서드*가 라우트의 단위다. *애너테이션이 메타데이터를 만들고, 프레임워크가 그 메타데이터를 읽어 라우팅 테이블을 만든다*. JS/TS에서는 *함수 자체를 라우팅 테이블에 등록*한다. 더 직접적이고 더 가볍다. *어느 쪽이 옳은가?* 양쪽 다 일관성이 있다. 다만 *왜 JS 진영에는 NestJS가 따로 등장해야 했는가*에 대한 답이 여기 있다. 함수 등록 모델만으로는 *큰 백엔드*를 짤 때의 구조가 부족하다고 느낀 사람들이, 데코레이터로 Spring 식 구조를 가져왔다. 그게 NestJS다.

함수형 사고가 라이브러리에 미친 또 하나의 영향을 보자. 데이터 변환을 *체인 메서드*로 잇는다.

```javascript
const result = items
  .filter((x) => x.active)
  .map((x) => x.name)
  .filter((name) => name.length > 0)
  .join(", ");
```

Java도 Stream으로 비슷하게 쓴다. `items.stream().filter(...).map(...).collect(...)`. 다만 JS는 *`stream()`으로 진입하지 않아도* 배열에 직접 메서드 체인을 건다. 자료구조 자체가 함수를 받아들이는 메서드를 풍부하게 가지고 있기 때문이다. `forEach`, `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`, `flatMap`, `sort`, `at`, `findLast` 등. 외울 게 많지만, *공통 패턴*이 있다. *대부분의 인자가 콜백 함수*다. 콜백을 받는 메서드가 풍부하다는 것은, 곧 *조합 가능한 작은 단위들로 변환을 짤 수 있다*는 뜻이다.

이 *조합 가능성*이 JS 라이브러리 생태계의 한 모습이다. lodash가 십수 년 동안 사랑받은 이유, RxJS가 복잡해 보이는데도 살아남은 이유, 최근의 Zod 같은 스키마 라이브러리가 *체이닝 API*로 설계된 이유 모두 이 토대 위에 있다. *함수가 일급이라서 가능한 표현력*이다.

여기서 한 가지만 더 강조해두자. *클로저(closure)*다. 일급 함수는 *자기가 정의된 환경의 변수를 그대로 기억한다*. 그게 클로저다. 다음 예가 가장 깔끔하다.

```javascript
function makeCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    get: () => count,
  };
}

const counter = makeCounter();
counter.increment();
counter.increment();
console.log(counter.get()); // 2
```

`makeCounter`는 이미 반환되어 함수 호출이 끝났다. *그런데도* 그 안의 `count`가 살아 있다. `increment`와 `get`이 그 변수를 *닫아 가지고* 있기 때문이다. Java에서는 final 변수만 람다에 캡처할 수 있고, 캡처된 변수를 외부에서 변경하는 게 어색하다. JS의 클로저는 그런 제약이 없다. 동일한 변수를 *여러 함수가 공유하며 읽고 쓴다*. 이 자유로움이 *모듈 패턴*, *프라이빗 변수의 흉내*, *함수형 프로그래밍의 기반* 모두를 지탱한다. TypeScript로 가면 클로저는 그대로 살아남고, 다만 *그 안에서 캡처된 변수의 타입이 추론된다는 점*이 추가될 뿐이다.

## 짚고 넘어가야 할 작은 함정 모음

본문 줄기를 흐트러뜨리지 않으려고 미뤄둔 *잔잔한 함정*들이 있다. 굵직한 것은 다 봤지만, 잔잔한 것들도 챙겨두자. 한국 커뮤니티에서 *"이걸로 한 번 데였다"*는 후기가 자주 올라오는 자리들이다.

**숫자 타입은 하나뿐이다.** Java는 `int`, `long`, `float`, `double`을 구분한다. JS의 숫자는 모두 `number` 한 가지, 정확히는 IEEE 754 배정밀도 부동소수점이다. 그래서 `0.1 + 0.2 === 0.3`이 `false`다. *고전 중의 고전 함정*이다. 정확한 정수 연산이 필요하면 `BigInt`(접미사 `n`)를 써야 한다. `9007199254740993n + 1n`은 정확히 계산된다.

```javascript
console.log(0.1 + 0.2);              // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3);      // false
console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991
console.log(Number.MAX_SAFE_INTEGER + 2); // 9007199254740992 (틀림)
console.log(9007199254740993n + 1n); // 9007199254740994n (정확)
```

**암묵적 타입 변환이 너무 많이 일어난다.** 이 책 첫머리에서 보았던 `[] + []`, `[] + {}`이 그런 사례다. `+` 연산자는 한쪽이 문자열이면 *모두 문자열로 합치고*, 그렇지 않으면 *모두 숫자로 더한다*. 객체에 `+`가 적용되면 우선 `valueOf()`, 그다음 `toString()`을 시도한다. 그 결과 위 같은 *기괴한 출력*이 나온다. 핵심 처방은 단순하다. **타입을 섞지 말자.** 숫자는 숫자끼리, 문자열은 문자열끼리. 변환이 필요하면 `Number(x)`, `String(x)`로 *명시적으로* 한다. TypeScript는 이 패턴 위반을 컴파일타임에 잡아준다. JS만 쓰던 시절에는 ESLint와 코드 리뷰가 마지막 방어선이었다.

**자동 세미콜론 삽입(ASI).** JavaScript는 세미콜론을 *알아서 끼워 넣어준다*. 하지만 그 규칙이 미묘해서 가끔 사고를 친다. 가장 유명한 사례는 `return`이다.

```javascript
function f() {
  return
  {
    foo: "bar",
  };
}

console.log(f()); // undefined — return 다음 줄이 분리되어 객체는 무시됨
```

*"세미콜론을 안 쓰면 깔끔해 보인다"*는 미적 취향이 있는 사람들도 있지만, 이런 함정 때문에 *세미콜론을 명시적으로 쓰는 진영*과 *ASI를 신뢰하고 안 쓰는 진영*이 갈린다. Prettier 같은 포매터가 자동으로 정리해주므로, 팀이 합의하면 어느 쪽이든 괜찮다. 다만 *섞어 쓰지는 말자*.

**`==`의 함정 한 번 더.** 위에서 *"`==`은 쓰지 말자"*고 했지만, 다시 한 번 강조한다. `[] == false`가 `true`다. `[0] == false`도 `true`다. `[] == ![]`도 `true`다(이건 정말 꿈에 나올 정도로 이상하다). 이 모두가 JS의 *느슨한 동등 비교* 규칙 때문이다. 이런 코드를 만나면 *반드시 의도된 것인지* 의심하자. 거의 모두 *실수*다. ESLint의 `eqeqeq` 규칙을 켜자.

**호이스팅(hoisting).** 변수와 함수가 *코드의 위에서 선언된 것처럼 끌어올려져 처리되는* 현상이다. `var` 선언과 `function` 선언이 호이스팅된다. `let`, `const`도 *선언 자체는* 끌어올려지지만, *값에 접근하는 시점*까지는 *Temporal Dead Zone(TDZ)*이라는 영역에 머문다. 새 코드에서는 `var` 대신 `let/const`를 쓰자. 그러면 호이스팅의 가장 끔찍한 부분(*아직 할당 안 된 값을 참조해도 에러 없이 `undefined`가 되는*)을 피할 수 있다.

```javascript
console.log(x); // undefined (var는 undefined로 초기화됨)
var x = 1;

console.log(y); // ReferenceError (let/const는 TDZ)
let y = 1;
```

이 정도다. 다 외울 필요는 없다. *"이런 게 있다"*는 사실만 머리 어딘가에 박아두자. 어느 날 코드가 *기괴하게* 동작할 때 *"아, 그때 본 그 함정 같은데?"* 하고 떠올릴 수 있으면 충분하다.

## 그래서 이 모든 것이 TypeScript와 무슨 관계인가

여기까지 읽으면서 *"이게 다 JavaScript 이야기인데, TypeScript 책에서 왜 이렇게 길게 다루지?"* 하는 의문이 들었을 수 있다. 그 의문에 정직하게 답해보자.

TypeScript는 *기존 JavaScript 위에 타입 정보를 얹어 컴파일타임에 검사하는* 도구다. 이 한 줄을 풀어보면, **TS가 다루는 모든 것은 결국 JS의 그 형태와 그 결정들이다**. TS가 JavaScript를 *고치지* 않는다. *지우지도* 않는다. 컴파일이 끝나면 타입은 사라지고, 우리가 손에 쥐는 것은 *순수한 JS*다. 그 JS가 가진 모든 본성 — `this`의 동적 결합, prototype 체인, 이벤트 루프, `null`과 `undefined`의 이원성, 암묵적 변환, ASI, `==`의 함정 — 이 그대로 살아 있다.

그래서 TypeScript가 어디서는 *놀랍도록 잘 동작하고*, 어디서는 *이상하게 빈틈이 보인다*. 그 이유의 절반은 *TS의 타입 시스템 설계*에 있지만, 나머지 절반은 *JS의 본성*에 있다. 예를 들어보자.

- TS는 `this`의 타입도 추론한다. 하지만 *호출 방식이 `this`를 결정하는 JS의 본성*은 그대로다. 그래서 *콜백을 떼어내는 자리*에서 TS가 `this: void`로 추론하거나, *바인딩이 풀리는 자리*에서 컴파일러가 경고를 내준다. 알지 못하면 *왜 TS가 여기서 갑자기 까칠하지?* 싶은 자리들이다.
- TS는 `null`과 `undefined`를 별도의 타입으로 다룬다(`strictNullChecks`). 둘이 미묘하게 다른 의미를 가진다는 *JS의 약속*을 *타입 시스템이 강제*하는 것이다. Kotlin에서는 둘 중 하나만 있으니 단순한 일이, JS에서는 *둘이 별도의 타입*이라 추가적인 신경이 필요하다.
- TS의 컴파일된 결과물도 결국 단일 스레드의 이벤트 루프 위에서 돈다. async/await는 Promise 위의 syntax sugar고, Promise는 마이크로태스크 큐 위에서 돈다. *단일 스레드라는 사실은 컴파일이 가려주지 못한다.* 그래서 TS로 짠 백엔드도 무거운 동기 작업이 들어가면 똑같이 멈춘다.
- TS의 타입은 prototype 체인을 *모형화*해서 따라간다. 클래스의 메서드가 prototype에 들어간다는 사실, 인스턴스 필드가 자기 속성에 들어간다는 사실을 TS는 안다. 우리가 모르고 *떼어붙이는* 행동을 하면, TS의 타입과 런타임이 어긋난다. 어긋난 자리는 거의 항상 *런타임 에러*로 나온다.

*"그러면 TS는 결국 무력한 것 아닌가?"* 그렇지 않다. TS는 자신의 한계를 정직히 알고 있는 도구다. 무엇을 잡아주고 무엇을 잡아주지 않는지가 *명시적으로* 설계되어 있다. 그 한계의 윤곽이 정확히 *JS의 본성*과 겹친다. 우리가 이 장에서 본 것들이 *TS의 한계의 정체*인 셈이다. 다음 장에서 본격적으로 다룰 *컴파일타임의 환상*이라는 주제는, 이 장에서 본 JS의 본성을 *TS가 어디까지 가려줄 수 있고, 어디서부터는 가려줄 수 없는가*를 정직하게 묻는 자리다.

그래서 이 장의 결론은 단순하다. **JavaScript를 알지 못하면 TypeScript를 끝내 모를 수밖에 없다.** Java에서 *JVM의 동작*을 모르고 자바를 짤 수 있는 사람과, JVM을 *조금이라도 아는* 사람의 코드 품질이 결국 다르듯이, JS의 본성을 외면한 TS와 그 본성 위에서 만들어진 TS는 결국 다른 결과를 낸다. 자, 그러면 그 본성 위에 *어떤 약속*으로 TypeScript가 얹혀 있는지를 다음 장에서 함께 살펴보자.

## 마무리 — 외면하지 말자

이 장에서 본 것들을 한 번에 머리에 다 넣을 필요는 없다. 다만 다음 다섯 가지만은 *기억해두자*.

1. **JavaScript는 1995년의 결정들을 30년째 짊어지고 있다.** 그 결정들 위에 TypeScript가 얹혀 있다. 그 결정들을 *낭만화하지도, 깎아내리지도* 말고, *있는 그대로* 받아들이자.
2. **`class`는 prototype 위의 옷이다.** 옷이 편리하지만, 안쪽 모델이 prototype이라는 사실은 안 바뀐다. 어느 날 `this`가 사라질 때, 그 사실이 답이 된다.
3. **`this`는 호출 방식에 따라 결정된다.** 7가지 얼굴을 다 외우지 말고, *이 한 문장*만 머리에 박아두자. 콜백 안에서 `this`가 필요하면 화살표 함수를, 메서드를 떼어내야 하면 `bind`를.
4. **단일 스레드 + 이벤트 루프 + 마이크로/매크로 큐.** Promise 콜백은 마이크로태스크다. setTimeout은 매크로태스크다. 동기 코드 → 마이크로 비우기 → 매크로 하나, 다시 처음으로. 이 순환을 머리에 그릴 수 있으면 비동기의 절반은 끝났다.
5. **빈 값은 두 개. 비교는 `===`로.** `null`과 `undefined`는 의미가 다르다. `==`은 쓰지 말자. 한 줄 예외는 `x == null`. `??`와 `?.`을 적극 쓰자.

이 다섯 가지가 앞으로 우리가 만나는 *모든 함정*의 뿌리다. 4장의 narrowing이, 7장의 비동기 함정이, 9장의 점진적 마이그레이션이 모두 이 토대 위에서 설명된다. 이 장이 어렵게 느껴졌다면, 그건 자연스럽다. *정적 타입 위에서 자라온 사람에게 JS의 본성은 처음에는 거의 조롱처럼 느껴진다*. 그 거리감을 부정하지 말자. 다만 *이해하려는 노력*은 결국 보상한다. 다음 장에서 그 보상의 모습을 보자.

자, 이제 TypeScript의 약속을 정면으로 들여다볼 차례다. *"TS는 무엇이며, 무엇이 아닌가."* 컴파일타임이 만드는 환상과 그 환상이 정직히 멈추는 자리를, 다음 장에서 함께 살펴보자.

> ### 📖 더 깊이 가려면
>
> - **MDN Web Docs — JavaScript Reference**: <https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference> — `this`, prototype, 이벤트 루프 모두 한국어로 양질의 설명이 있다. 한국 개발자가 *처음 펼쳐야 할* JS 1차 문서.
> - **You Don't Know JS Yet (2nd ed.)** — Kyle Simpson. <https://github.com/getify/You-Dont-Know-JS> — 무료 공개. *"JS를 안다"*는 자존심을 정직하게 부순다. 특히 *Scope & Closures*와 *this & Object Prototypes* 두 권은 이 장의 내용을 깊이 보충한다.
> - **JavaScript: The Good Parts** — Douglas Crockford (오라일리, 2008). 오래되었지만 *"JS의 좋은 부분만 골라 쓰자"*는 사상 자체가 지금까지 영향을 준다. 이 사상이 곧 TypeScript로 진화하는 흐름의 한 갈래다.
> - **velopert(김민준) — JavaScript 입문서**: <https://velog.io/@velopert> — 한국어 표준 자료의 한 갈래. JS 기초의 한국어 설명을 찾는 첫 자리.
> - **이벤트 루프 시각화 — Loupe**: <http://latentflip.com/loupe/> — Philip Roberts의 JSConf EU 2014 발표 *"What the heck is the event loop anyway?"*와 함께 보자. 14분짜리 영상이 *이벤트 루프란 무엇인가*에 대한 가장 빠른 직관을 준다.
