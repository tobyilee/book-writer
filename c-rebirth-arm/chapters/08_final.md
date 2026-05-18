# 8장. 헤더와 링커 — 컴파일 사이클을 다시 이해하기

Java로 매일 일하던 사람이 C 프로젝트에 손을 댔다고 상상해 보자. `Vec`이라는 작은 자료구조를 짜서 `vec.c`에 정의하고, 헤더 `vec.h`에 함수 시그니처를 적고, `main.c`에서 가져다 썼다. 다 됐다고 생각하고 `clang main.c`를 쳤더니, 처음 보는 에러가 뜬다.

```
Undefined symbols for architecture arm64:
  "_vec_push", referenced from:
      _main in main-7d1c2f.o
ld: symbol(s) not found for architecture arm64
clang: error: linker command failed with exit code 1
```

`vec.h`를 include 했는데, 왜 함수를 못 찾는다는 걸까? Java에서는 import 한 줄이면 컴파일러가 알아서 다 찾아 줬다. Python은 import 시점에 그냥 다른 파일을 끌어와 실행한다. 그런데 C는 다르다. 컴파일러가 보는 세계와 링커가 보는 세계가 별개로 굴러간다. 한쪽이 알고 있다고 해서 다른 쪽이 알고 있다는 보장이 없다.

여기서 잠시 한숨이 나온다. 좀 번거롭다. 그런데 이 번거로움이 사실은 C가 다른 언어들과 가장 다르게 일하는 자리다. 한 번 익히면 평생 쓰는 모델이고, 베어메탈로 가는 길에서는 이게 안 잡혀 있으면 한 발짝도 못 나간다. 이 장에서 빌드 사이클의 네 단계, 헤더의 정체, 링커의 일, 그리고 함수 호출의 실제 메커니즘(AArch64 ABI)을 한 번에 손에 잡자.

## 네 단계 — 한 번 펼쳐 두면 평생 쓴다

`clang hello.c -o hello`는 한 줄이지만, 그 한 줄 뒤에서는 네 단계가 차례로 돈다.

```
.c  ── 전처리(preprocess) ──▶  .i
.i  ── 컴파일(compile)     ──▶  .s
.s  ── 어셈블(assemble)    ──▶  .o
.o  ── 링크(link)          ──▶  실행 파일
```

평소에는 한 번에 돌리지만, 한 단계씩 따로 돌려 볼 수도 있다. 그 한 번이 빌드 모델을 머릿속에 박는 가장 빠른 길이다. 짧은 hello.c로 한 번 해 보자.

```bash
$ clang -E hello.c -o hello.i      # 전처리만
$ wc -l hello.c hello.i
      5 hello.c
    900 hello.i
```

다섯 줄짜리 hello.c가 전처리를 거치니 900줄짜리 hello.i가 된다. 무슨 일이 일어났을까? `#include <stdio.h>` 한 줄이 그 자리에 stdio.h의 모든 내용을 텍스트로 펼쳐 넣은 것이다. 헤더 안에 들어 있던 다른 `#include`도 재귀적으로 펼쳐진다. 매크로도 모두 풀린다. 전처리기는 컴파일러가 보기 전에 텍스트를 손질하는 단계라는 점, 그래서 **`#include`는 사실상 텍스트 치환**이라는 점을 이 한 번으로 손에 잡자.

다음 단계는 컴파일러가 그 텍스트를 어셈블리로 옮기는 단계다.

```bash
$ clang -S hello.c -o hello.s
```

`.s` 파일을 열어 보면 AArch64 어셈블리가 들어 있다. 이 단계까지가 "컴파일러가 일하는 영역"이다. 그다음 단계는 어셈블러가 그 어셈블리를 기계어로 옮긴다.

```bash
$ clang -c hello.c -o hello.o      # 어셈블까지
```

`hello.o`는 오브젝트 파일이다. 안에는 실제 명령어 비트와 심볼 테이블이 들어 있다. 그런데 이게 그대로 실행되지는 않는다. `printf` 같은 외부 함수의 주소가 비어 있기 때문이다. 그 빈자리를 채워 넣는 단계가 마지막 — 링크다.

```bash
$ clang hello.o -o hello           # 링크
```

링커가 `hello.o`와 시스템의 C 런타임 라이브러리(libc, libSystem)를 묶어 실행 파일을 만든다. 이게 비로소 우리가 `./hello`로 실행할 수 있는 바이너리다.

자, 그렇다면 처음의 그 미스터리한 에러로 돌아가 보자. `Undefined symbols for architecture arm64: _vec_push` — 이건 정확히 **링크 단계**에서 떨어진 에러다. 컴파일러는 헤더의 선언만 보고 "그 함수가 어딘가에 있다"고 가정하고 `.o`를 만들었다. 그런데 링커가 모든 `.o`를 모아 봐도 `vec_push`의 정의가 들어 있는 `.o`가 없다. 그래서 항의한다. 해결책은 단순하다 — `vec.c`도 같이 빌드 줄에 넣어 주면 된다.

```bash
$ clang main.c vec.c -o app
```

또는 `.o`로 한 번씩 만들어 둔 뒤 묶는다.

```bash
$ clang -c main.c -o main.o
$ clang -c vec.c  -o vec.o
$ clang main.o vec.o -o app
```

이 분리 컴파일이 C의 표준 작업 모델이다. 큰 프로젝트일수록 이 모델의 가치가 커진다. 한 파일만 고치면 그 파일만 다시 컴파일하면 되기 때문이다.

## 헤더 — 약속의 자리

이제 헤더의 역할을 정확히 잡아 두자. 헤더가 텍스트 치환된다는 사실은 알았는데, 그래서 거기에 **무엇을 적어야** 하는가?

답은 한 줄로 줄일 수 있다. **헤더에는 "약속"만, 정의는 `.c`에.** 약속이 곧 선언이다.

```c
/* util.h — 약속만 적힌다 */
#ifndef CH08_UTIL_H
#define CH08_UTIL_H

extern int g_call_count;            /* 변수의 존재만 약속 */
int  add(int a, int b);             /* 함수의 시그니처만 약속 */
void greet(const char *name);

#endif
```

```c
/* util.c — 그 약속의 실체가 한 곳에서 살아간다 */
#include <stdio.h>
#include "util.h"

int g_call_count = 0;               /* 정의 — 메모리가 잡힌다 */

int add(int a, int b) { return a + b; }
void greet(const char *name) { printf("hello, %s\n", name); }
```

```c
/* main.c — 약속만 보고 가져다 쓴다 */
#include "util.h"

int main(void) {
    greet("aarch64");
    int s = add(3, 4);
    /* g_call_count 도 헤더의 약속을 통해 쓸 수 있다 */
    return 0;
}
```

선언과 정의의 분리, 이게 C 사고방식의 척추다. 헤더는 "이 함수가 있다, 시그니처는 이렇다, 이 변수가 어디엔가 있다"고 약속만 한다. 그 약속의 짝은 어딘가의 `.c` 파일에 **딱 한 번** 있어야 한다. 두 번 있으면 링커가 "다중 정의(multiple definition)"라며 운다. 한 번도 없으면 위에서 본 "정의되지 않은 심볼"로 운다.

### 이중 포함 방지 — 약속도 두 번 펼치면 사고

`#include`가 텍스트 치환이라는 사실에서 한 가지 부작용이 따라온다. 같은 헤더가 두 번 펼쳐지면 같은 선언이 두 번 나오게 되고, 그게 에러로 떨어진다. 이걸 막는 두 가지 관용구가 있다.

```c
/* 방식 (1) — include guard */
#ifndef CH08_UTIL_H
#define CH08_UTIL_H
/* 헤더 내용 */
#endif

/* 방식 (2) — pragma once (사실상 표준이지만 표준 외) */
#pragma once
```

방식 (1)이 표준이다. 어디서나 동작하고, 옛 코드에도 다 들어 있다. 방식 (2)는 모든 모던 컴파일러가 지원하지만 ISO 표준에는 없다. 작은 프로젝트라면 (2)도 무난하고, 라이브러리로 배포할 거라면 (1)이 안전하다. 둘을 섞어 두는 자리도 많다 — 가드 안에 `#pragma once`까지 같이 넣는 패턴이다. 약간 보험을 드는 셈이다.

### `static`의 두 얼굴

C에서 가장 헷갈리는 키워드 하나만 고르라면 단연 `static`이다. 두 얼굴을 가졌기 때문이다.

```c
/* (1) 파일 스코프의 static — 내부 링키지 */
static int helper(int x) { return x * 2; }
static int file_local = 0;
```

이 `static`은 "이 심볼은 이 파일 안에서만 보인다"는 의미다. 같은 이름의 함수를 다른 파일에서 또 정의해도 충돌이 안 난다. 라이브러리 작성에서 내부 함수를 외부에 노출하지 않으려는 패턴이다. 거꾸로 말하면, **헤더 파일에 함수 정의를 적으면서 `static`을 빼면 같은 함수가 여러 `.o`에 박혀 링커가 운다**. 헤더에 함수 본문을 넣고 싶다면 `static inline`이 정석이다.

```c
/* 헤더에 짧은 함수 본문을 두고 싶을 때 — static inline */
static inline int clamp(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}
```

```c
/* (2) 함수 내부의 static — 영속 변수 */
int next_id(void) {
    static int counter = 0;     /* 함수 호출 사이에 살아남는다 */
    return ++counter;
}
```

이 `static`은 완전히 다른 얼굴이다. 함수 안에 있는데도 그 변수는 함수가 끝나도 사라지지 않는다. 다음 호출 때 그대로 그 자리에 있다. Java의 정적 필드와 비슷한 정서지만, 스코프는 함수 안에 갇혀 있다. 작은 캐시, 카운터, 한 번만 초기화하면 되는 상태에 자주 쓰인다.

두 얼굴이 모두 `static`이라는 같은 키워드 아래 있다는 사실이 C 입문자에게는 매번 잠깐 멈칫하게 만든다. 그런 자리를 만나면 "지금 이 static은 어느 얼굴인가?"를 한 번 자문해 두자.

### `extern`의 역할

`extern`은 헤더에서 변수를 약속할 때 쓰는 키워드다. 위 `util.h`에서 `extern int g_call_count;`로 적은 자리다. 함수는 기본이 외부 링키지라서 `extern`을 안 붙여도 무방하지만(붙여도 동일), 변수는 다르다. **헤더에 그냥 `int g_call_count;`라고 적으면 그 자체가 정의가 되어** 그 헤더를 include 하는 파일마다 같은 변수가 정의된다. 그게 링커에서 "multiple definition"으로 떨어진다.

```c
/* 잘못된 예 — 헤더에 직접 정의 */
int g_call_count;       /* 이건 정의다. include한 .c마다 정의가 생긴다 */

/* 맞는 예 — 헤더에는 선언, 정의는 한 .c에 */
extern int g_call_count;    /* util.h: "어딘가에 있다" 약속만 */
/* util.c: int g_call_count = 0; — 진짜 정의는 한 곳 */
```

C 입문자가 한 번씩 발이 걸리는 자리다. 한 번 데이고 나면 다시는 잊지 않는다.

## 정적 라이브러리와 동적 라이브러리

분리 컴파일이 익숙해지면 다음 자연스러운 질문이 생긴다 — 자주 쓰는 `.o`들을 매번 빌드 줄에 넣지 말고 묶어 두면 안 될까? 그게 정적 라이브러리(`.a`)다.

```bash
$ clang -c vec.c -o vec.o
$ clang -c str.c -o str.o
$ ar rcs libmyutil.a vec.o str.o
```

`libmyutil.a`는 그냥 `.o`들을 한 봉투에 묶어 둔 것이다. 쓰는 쪽에서는 이렇게 한다.

```bash
$ clang main.c -L. -lmyutil -o app
```

`-L.`은 "라이브러리를 현재 디렉터리에서 찾아라", `-lmyutil`은 "`libmyutil.a` 또는 `.dylib`/`.so`를 찾아 묶어라"라는 뜻이다. 링커가 라이브러리 안의 `.o` 중에서 main이 실제로 참조하는 심볼이 들어 있는 것만 끌어다 실행 파일에 정적으로 박는다. 그래서 결과 실행 파일은 라이브러리 없이도 동작한다.

동적 라이브러리는 다르다. macOS에서는 `.dylib`, Linux에서는 `.so`, Windows에서는 `.dll`이다.

```bash
$ clang -dynamiclib -fPIC vec.c str.c -o libmyutil.dylib
$ clang main.c -L. -lmyutil -o app
```

링크 시점에는 라이브러리의 심볼 테이블만 보고 "여기에 그 함수가 있다"는 참조만 박아 둔다. 실제 코드는 실행 시점에 OS의 동적 로더가 메모리에 올린다. 같은 라이브러리를 여러 프로그램이 공유할 수 있어 메모리가 절약되고, 라이브러리만 따로 업데이트할 수도 있다. 대신 실행 파일이 라이브러리 없이는 동작하지 않는다.

작은 베어메탈 프로젝트에서는 어차피 라이브러리 자체를 안 쓴다 — 모든 코드가 한 ELF에 정적으로 묶인다. 그러나 호스트에서는 둘의 차이를 알아 두면 빌드 에러 메시지가 한결 친근해진다.

## 빌드 시스템 — Make에서 CMake까지

지금까지의 `clang -c` 줄들을 매번 손으로 치는 건 번거롭다. 그래서 빌드 시스템이 있다. 한 단계씩 올라가 보자.

**Make.** 가장 오래되고 가장 보편적이다. 베어메탈 튜토리얼 90%가 Make로 짜여 있다. 규칙은 단순하다 — "이 파일을 만들려면 이 입력이 필요하고, 이 명령으로 만들어라."

```make
app: main.o util.o
	clang main.o util.o -o app

%.o: %.c
	clang -c $< -o $@
```

`%.o: %.c`는 패턴 규칙이다. 어떤 `*.o`든 같은 이름의 `*.c`에서 만들어진다. `$<`는 첫 입력(`.c`), `$@`는 출력(`.o`). 베어메탈 코드에서 이 패턴 한두 줄이면 충분한 경우가 많다.

**CMake.** 큰 프로젝트, 여러 플랫폼, IDE 통합이 들어오면 Make는 점점 무거워진다. CMake가 그 빈자리에 들어온다. 더 추상화된 언어로 빌드를 적고, CMake가 알아서 Make나 Ninja의 빌드 파일을 생성한다.

```cmake
cmake_minimum_required(VERSION 3.20)
project(myapp C)
set(CMAKE_C_STANDARD 17)
add_executable(app main.c util.c)
```

이 짧은 네 줄이 Make로는 거의 같은 일을 하는 빌드를 만들어 낸다. 그리고 IDE 친화적이다. 한 가지 옵션을 더 켜자.

```bash
$ cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
$ ninja -C build
```

`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`이 키 포인트다. CMake가 빌드와 동시에 `build/compile_commands.json`이라는 파일을 만들어 둔다. 이 파일에 모든 소스의 정확한 컴파일 명령이 들어 있다. clangd, clang-tidy, scan-build 같은 정적 분석 도구들이 모두 이 파일을 입력으로 받는다. 4장에서 본 VS Code + clangd 셋업이 이 파일 없이는 작동하지 않는다는 점, 이 자리에서 한 번 더 짚어 두자.

**Ninja.** Make보다 빠른 빌드 실행기다. 직접 손으로 쓰지는 않고, CMake나 Meson이 생성해 주는 빌드 백엔드로 쓴다. `cmake -G Ninja -B build`로 지정한다. 큰 프로젝트에서는 Make 대비 빌드가 눈에 띄게 빠르다.

**Meson.** Python 기반의 더 모던한 빌드 시스템. GNOME, systemd 같은 큰 프로젝트에서 채택되어 있다. CMake보다 문법이 깔끔하다는 평이지만 생태계가 더 작다. 책 범위에서는 Make와 CMake 두 가지가 손에 잡혀 있으면 충분하다.

## 함수 호출의 실제 — AArch64 ABI

여기서 한 단계 더 깊이 들어가자. `add(3, 4)`라고 함수를 부를 때, **3과 4는 어떻게 add에 전달되는가?** 그 답이 ABI(Application Binary Interface)다. 컴파일러가 짠 코드가 OS, 어셈블리, 라이브러리와 호환되려면 모두가 같은 약속을 따라야 한다. AArch64에는 그 약속이 명문화되어 있다 — Arm Procedure Call Standard for the Arm 64-bit Architecture, 줄여서 AAPCS64 또는 PCS.

ARM의 PCS가 정한 인자 전달 규약은 다음과 같다.

| 레지스터 | 용도 |
|---------|------|
| `X0`~`X7` | 처음 8개의 정수/포인터 인자. 함수 리턴 값도 X0(때로 X1까지). |
| `X8` | 간접 리턴 결과 — 큰 구조체를 리턴할 때 호출자가 결과 공간 포인터를 여기 싣는다. |
| `X9`~`X15` | 임시 레지스터 — 호출자가 보존할 책임(caller-saved). |
| `X19`~`X28` | 호출자가 의지하는 레지스터 — 피호출자가 보존할 책임(callee-saved). |
| `X29` | 프레임 포인터(FP). |
| `X30` | 링크 레지스터(LR) — `bl` 명령으로 함수를 호출하면 리턴 주소가 여기에 저장된다. |
| `SP` | 스택 포인터. 16바이트 정렬을 유지해야 한다. |

이 표가 의미하는 바를 한 문장으로 풀면 — **AArch64에서는 처음 8개의 정수/포인터 인자가 레지스터로 전달된다.** 그보다 많은 인자, 또는 큰 구조체는 스택에 실린다.

x86-64(System V ABI)와 비교하면 차이가 보인다. x86-64는 처음 6개 인자를 RDI, RSI, RDX, RCX, R8, R9에 싣는다. 즉 인자 레지스터의 수도, 이름도 다르다. 그래서 같은 C 코드가 두 아키텍처에서 컴파일되면 같은 의미지만 다른 어셈블리가 나온다. ABI는 "같은 C를 다른 모습으로 옮기는" 약속이다.

### `objdump`로 직접 들여다보기

말로만 봐서는 손에 안 잡힌다. 짧은 함수를 한 번 디스어셈블해 보자.

```c
/* add.c */
int add(int a, int b) {
    return a + b;
}
```

```bash
$ clang -O1 -c add.c -o add.o
$ objdump -d add.o
```

(macOS의 `objdump`는 LLVM 도구로, Homebrew의 `binutils` 또는 LLVM 본가에서 따라온다.)

대략 이런 어셈블리가 나온다.

```
_add:
    add  w0, w1, w0       ; w0 = w1 + w0
    ret                   ; X30(LR)으로 점프
```

흥미로운가? 첫 인자 `a`는 W0(X0의 하위 32비트)에 들어와 있고, 둘째 인자 `b`는 W1에 있다. `add` 명령 하나가 두 값을 더해 W0에 다시 쓴다. 그리고 `ret`은 LR(X30)에 들어 있는 주소로 점프한다 — 호출자가 `bl _add`로 부르며 LR에 저장해 둔 자리다. 함수 호출의 가장 단순한 모습이 이 두 줄에 들어 있다.

조금 더 복잡한 함수로 가 보자.

```c
/* add9.c — 인자가 9개 */
int add9(int a, int b, int c, int d, int e, int f, int g, int h, int i) {
    return a + b + c + d + e + f + g + h + i;
}
```

이걸 디스어셈블하면 첫 8개 인자(a~h)는 W0~W7에 들어와 있는 게 보이고, 9번째(i)는 스택에서 읽어 오는 명령(`ldr w8, [sp]` 같은)이 등장한다. 레지스터로 못 다 보내는 인자가 스택을 거치는 그 모습이다.

### 프롤로그와 에필로그

지역 변수가 있는 함수는 보통 이런 모양의 prologue·epilogue를 갖는다.

```
_func:
    stp  x29, x30, [sp, #-16]!   ; FP와 LR을 스택에 저장, SP -= 16
    mov  x29, sp                  ; 새 FP = SP
    ...본문...
    ldp  x29, x30, [sp], #16     ; FP와 LR 복원, SP += 16
    ret
```

`stp`(store pair)와 `ldp`(load pair)가 두 레지스터를 한 번에 다룬다. FP(X29)와 LR(X30)을 스택에 보관해 두는 이유는 — 본문에서 다른 함수를 또 부를 수도 있는데, `bl` 명령이 LR을 덮어쓰기 때문이다. 살리려면 미리 저장해 둬야 한다. 이게 호출이 중첩되어도 각 함수가 자기 리턴 주소를 잃지 않는 메커니즘이다.

베어메탈 코드에서 `boot.S`를 보면 이 패턴이 그대로 등장한다. `_start`가 `bl kernel_main`으로 C 함수를 부르기 전에 스택 포인터를 잡아 두는 그 한 줄, 그게 PCS가 요구하는 약속을 지키려는 손짓이다. Ch12에서 그 줄을 처음 만날 때, 이 절을 떠올리자. 갑자기 등장하는 레지스터가 아니라 이미 인사 나눈 친구가 된다.

### 왜 이걸 호스트에서 미리 봐 두는가

호스트 코드에서 우리는 ABI를 거의 의식하지 않는다. 컴파일러가 알아서 해 준다. 그러나 베어메탈에서는 두 자리에서 ABI가 정면으로 보인다.

첫째, **어셈블리에서 C 함수를 부르는 자리.** `bl kernel_main`이 그것이다. 그전에 스택을 잡아 두지 않으면 `kernel_main`이 자기 지역 변수를 어디 잡을지 모른다. PCS는 SP가 16바이트 정렬되어 있어야 한다고 못 박았다 — 그래서 어셈블리에서 SP를 16의 배수 주소로 맞추는 자리가 등장한다.

둘째, **인터럽트 벡터에서 핸들러를 호출하는 자리.** 이건 15장의 영역이지만, 인터럽트는 임의의 시점에 들어오기 때문에 caller-saved 레지스터(X9~X15)를 핸들러가 직접 보존해 줘야 한다. 그게 컨텍스트 저장 코드의 본업이다.

호스트에서 ABI를 한 번 손에 잡아 두면, 베어메탈에서 이 두 자리가 자연스럽게 풀린다. 그래서 이 절은 11~13장으로 가는 다리다.

## `compile_commands.json` — 도구들의 공통 입구

마지막으로 한 가지, 모던 C 개발에서 빠질 수 없는 파일 하나를 잡고 가자. `compile_commands.json`이다.

이 파일은 JSON 배열인데, 한 항목이 한 `.c` 파일의 정확한 컴파일 명령을 담는다.

```json
[
  {
    "directory": "/path/to/project",
    "command": "clang -std=c17 -Wall -Iinclude -c main.c -o main.o",
    "file": "main.c"
  },
  {
    "directory": "/path/to/project",
    "command": "clang -std=c17 -Wall -Iinclude -c util.c -o util.o",
    "file": "util.c"
  }
]
```

이게 왜 중요할까? clangd가 자동완성을 정확하게 하려면 그 파일이 **정확히 어떤 플래그로 컴파일되는지** 알아야 한다. 같은 `.c` 파일이라도 `-DFOO=1`이 켜져 있느냐 아니냐에 따라 매크로 분기가 다르고, `-I` 옵션에 따라 헤더 경로가 다르다. clangd가 이 정보를 모르면 자동완성과 에러 표시가 어긋난다. 그 정보를 한 곳에 정리해 두는 게 `compile_commands.json`이다.

CMake는 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` 한 줄로 이 파일을 만들어 준다. Make로 빌드하는 작은 프로젝트라면 `bear` 같은 도구(`bear -- make`)가 빌드 명령을 가로채 같은 파일을 생성한다. 또는 손으로 한 번 적어 둘 수도 있다 — 예제 `example/ch08-linker/`에 그렇게 적어 둔 한 본보기가 있다.

clangd뿐 아니라 clang-tidy도, scan-build도, libFuzzer 빌드 스크립트도 이 파일을 본다. 그래서 모던 C 워크플로의 사실상 표준 입력이다. Ch4에서 처음 등장했고, Ch9에서 본격적으로 도구들을 묶어 돌릴 때 다시 만난다.

### 한 가지 실용 팁 — lldb로 break 걸어 걸어 들어가기

`compile_commands.json`이 준비되면 디버거 워크플로가 한결 매끄러워진다. 예제(`example/ch08-linker/`)의 `make lldb` 타깃을 따라 한 번 해 보자.

```bash
$ lldb -o "b main" -o "r" ./app
```

`-o` 옵션은 lldb에 명령을 한 줄씩 미리 넣는다. 위 명령은 "main에 break를 걸고, 실행하라"는 뜻이다. lldb가 멈춘 자리에서 `s`로 한 줄씩 들어가 보자. `greet("aarch64")` 호출에 도달하면, 거기서 또 `s`를 누르면 그 함수 안으로 들어간다. 그 자리에서 레지스터를 보면 — `register read x0` — X0에 문자열 "aarch64"의 주소가 들어 있다. PCS의 약속이 이론이 아니라 메모리에 손에 잡히는 사실로 보이는 순간이다.

조금 더 나가면, `disassemble`로 현재 함수의 어셈블리를 볼 수 있고, `frame variable`로 지역 변수를, `frame info`로 호출 스택의 자기 자리를 확인할 수 있다. lldb의 명령은 GDB와 비슷하지만 조금씩 다른 자리가 있다 — Apple Silicon에서는 lldb가 1순위라는 점은 한 번 짚어 두자.

## 챕터를 닫으며

이 장에서 손에 잡은 것들을 정리하자. 네 단계 빌드 사이클(전처리→컴파일→어셈블→링크)과 각 단계의 산물(`.i`/`.s`/`.o`/실행). 헤더의 약속과 `.c`의 정의 분리, 그리고 `static`/`extern`이라는 키워드의 두 얼굴. 정적 라이브러리(`.a`)와 동적 라이브러리(`.dylib`/`.so`)의 차이. Make에서 CMake·Ninja·Meson으로 이어지는 빌드 시스템 사다리. 그리고 함수 호출의 실제 — AArch64 PCS가 정한 `X0`~`X7` 인자 레지스터, X30 링크 레지스터, X29 프레임 포인터의 약속. 마지막으로 `compile_commands.json`이라는 도구들의 공통 입구.

빌드 에러 메시지가 더 이상 무서워지지 않는다는 자신감, 그게 이 장의 가장 큰 자산이다. "Undefined symbols" 에러를 보면 즉시 "어느 `.c`에서 정의가 빠졌는지" 떠올릴 수 있게 됐고, 헤더에 무엇을 적고 무엇을 적지 말아야 하는지 손에 잡혔다. 그리고 함수가 호출될 때 정말로 무슨 일이 일어나는지, 인자가 어떤 레지스터에 실리는지 — 그 모델이 머릿속에 박혔다. 이 모델이 베어메탈에서 그대로 다시 쓰인다.

다음 장으로 가자. 빌드를 알았으니, 그 빌드에 안전망을 짤 차례다. ASan과 UBSan을 정점에 두는 빌드 매트릭스가 어떻게 짜이는지, 그리고 그 매트릭스가 우리의 일상 개발 빌드에 어떻게 들어와 앉는지를 본다.
