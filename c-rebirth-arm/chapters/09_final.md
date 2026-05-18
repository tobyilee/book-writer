# 9장. 안전망 — Sanitizer를 중심에 둔 빌드 매트릭스

새벽 두 시, 며칠째 잡히지 않던 버그가 마침내 손에 잡혔다고 하자. off-by-one 한 줄이었다. 길이가 5인 배열에서 `i <= n`이라고 적은 그 작은 실수 하나가, 운영 환경에서는 다른 변수의 값을 한 번씩 망가뜨려 왔다. 디버거를 띄워도 재현이 안 됐고, printf를 박아 두면 그날따라 잘 돌았다. 답을 알고 나니 허무하다. 그리고 한 가지 의문이 따라온다 — **이걸 처음부터 잡아 줄 수 있는 도구가 있지 않을까?**

있다. 그것도 한 줄이면 된다. 빌드 명령에 `-fsanitize=address`를 끼우는 그 한 줄이다. AddressSanitizer라는 손님이 우리 코드의 모든 메모리 접근을 감시해 주는데, off-by-one 한 줄이 닿는 그 순간 정확히 어느 파일 몇 번째 줄에서 무슨 일이 벌어졌는지를 빨갛게 알려 준다. 7장에서 우리는 C가 침묵하는 모습을 정직하게 봤다. 이번 장에서는 그 침묵을 깨는 도구들 — sanitizer, 정적 분석, 포매터, 퍼저 — 을 한자리에 모아 빌드 매트릭스를 짠다. 정점에는 ASan과 UBSan을 둔다. 나머지는 그 정점을 보완하는 위성이다.

이 장이 끝나면 "어떤 빌드에서 무엇을 켜는가"라는 매트릭스가 머릿속에 박힌다. 그리고 책 이후의 모든 예제 빌드가 그 매트릭스 위에서 돈다.

## §1. 정점 — ASan과 UBSan

먼저 도구 한 쌍부터 손에 익히자. AddressSanitizer(이하 ASan)와 UndefinedBehaviorSanitizer(이하 UBSan). 둘은 형제고, 같이 켜는 게 정석이다. 한 쌍이 잡아 주는 버그의 카탈로그가 길다.

| 도구 | 잡는 버그 |
|------|---------|
| ASan | heap-buffer-overflow, stack-buffer-overflow, global-buffer-overflow, use-after-free, use-after-return, use-after-scope, double-free, 메모리 누수(leak) |
| UBSan | signed-integer-overflow, NULL 역참조, alignment 위반, 잘못된 시프트(음수, 폭 초과), enum 범위 초과, 배열 경계 초과(런타임), 잘못된 enum 변환, ... |

7장에서 본 손님들이 거의 다 들어 있다. 이 둘을 켜고 빌드하는 한 줄은 다음과 같다.

```bash
$ clang -std=c17 -g -O1 \
        -fsanitize=address,undefined \
        -fno-omit-frame-pointer \
        bug.c -o bug
```

옵션 하나씩 풀어 두자. `-fsanitize=address,undefined`가 ASan과 UBSan을 동시에 켠다. `-g`는 디버그 정보를 박아서 진단 메시지에 파일과 줄 번호가 정확히 나오게 한다. `-O1`은 약간의 최적화 — `-O0`은 ASan의 진단이 더 정확하지만 실행이 너무 느려진다. `-fno-omit-frame-pointer`는 스택 추적을 정확하게 유지하기 위한 짝꿍 옵션이다. 이 다섯 줄짜리 옵션 묶음이 책의 기본 디버그 빌드다.

### off-by-one을 사라지지 않게 잡아 보자

예제 `example/ch09-sanitizers/bug.c`에 의도적인 off-by-one을 심어 뒀다.

```c
static int sum_first_n(const int *arr, int n) {
    int s = 0;
    for (int i = 0; i <= n; i++) {   /* off-by-one */
        s += arr[i];
    }
    return s;
}

int main(void) {
    int arr[5] = {1, 2, 3, 4, 5};    /* 합은 15 */
    int s = sum_first_n(arr, 5);
    printf("sum = %d\n", s);
}
```

먼저 sanitizer 없이 빌드해서 어떻게 침묵하는지 보자.

```bash
$ make release
$ ./bug_release
sum = -292896528
```

15가 아니라 `-292896528`이 찍혔다. 답이 한참 어긋났는데도 에러 한 줄 없이 끝났다. 운영 코드에서 이걸 찾는 데 며칠씩 걸리는 이유가 이 침묵이다. 그렇다면 ASan을 켜고 같은 코드를 돌리면?

```bash
$ make asan
$ ./bug_asan
=================================================================
==75089==ERROR: AddressSanitizer: stack-buffer-overflow on address ...
READ of size 4 at 0x... thread T0
    #0 0x... in sum_first_n bug.c:27
    #1 0x... in main bug.c:34
Address 0x... is located in stack of thread T0 at offset 24 in frame
    #0 0x... in main bug.c:31
This frame has 1 object(s):
    [32, 52) 'arr' (line 32) <== Memory access at offset 24 ...
```

탄식이 나온다. 파일 이름, 줄 번호, 어떤 배열의 어느 오프셋이 어떤 크기로 잘못 접근됐는지가 한눈에 들어온다. `sum_first_n` 27번 줄, `arr`이라는 길이 20바이트(`int[5]`)의 스택 객체, 그 객체의 오프셋 24를 4바이트로 읽으려 했다. 답이 명확하다 — 27번 줄의 `i <= n`을 `i < n`으로 바꾸면 끝이다.

ASan은 이걸 어떻게 잡았을까? 비밀은 **redzone**이다. ASan은 모든 스택 배열과 힙 할당의 양 끝에 빨간 띠(독약 칠한 메모리)를 둘러 둔다. 정상 코드는 그 띠를 건드릴 일이 없지만, 경계 밖으로 한 칸이라도 나가면 띠를 밟는다. 띠를 밟는 그 순간 ASan의 보고가 떨어진다. 비용은 메모리가 두세 배, 실행이 1.5~2배 정도 느려지는 것. 개발 빌드에는 충분히 감당할 만한 비용이다.

### UBSan은 어떤 자리를 잡는가

UBSan은 7장의 카탈로그를 그대로 따라간다. signed 오버플로, NULL 역참조, 잘못된 시프트. 7장 예제(`example/ch07-ub/`)에서 `./ub_zoo overflow`를 돌리면 이렇게 떨어진다.

```
ub_zoo.c:25:19: runtime error: signed integer overflow:
  2000000000 + 2000000000 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior
```

정확히 그 줄, 그 연산. UBSan은 컴파일러가 UB로 못 박은 동작 하나하나에 런타임 체크를 끼워 둔다. 그래서 그 동작이 실제로 일어나는 순간 발각된다. 오버헤드가 ASan보다도 작아서(미미한 수준), 일상 빌드에 켜 두는 데 무리가 없다.

ASan과 UBSan을 함께 켜면 7장의 다섯 손님 중 strict aliasing 하나를 빼고 나머지가 다 잡힌다. 그래서 이 한 쌍이 **이 책의 모든 예제 빌드의 기본값**이다. 다른 모든 도구는 이 정점을 보완하는 위치에 있다.

### `ASAN_OPTIONS`와 `__asan_default_options`

ASan은 환경 변수로 행동을 조절할 수 있다. 가장 자주 쓰는 한 줄이 누수 검사다.

```bash
$ ASAN_OPTIONS=detect_leaks=1 ./bug_asan
```

macOS의 Apple Clang은 `detect_leaks`가 기본 꺼져 있다(Linux는 켜져 있다). 한 줄 짧게 켜고 끄는 것보다 매번 켜 두고 싶다면 소스에 다음 함수를 박아 두는 길이 있다.

```c
const char *__asan_default_options(void) {
    return "detect_leaks=1:strict_string_checks=1:halt_on_error=0";
}
```

`halt_on_error=0`은 첫 에러에서 죽지 않고 계속 실행하라는 뜻이다. 한 번의 실행으로 여러 버그를 한꺼번에 보고 싶을 때 쓴다. `detect_stack_use_after_return=1`은 함수가 리턴한 뒤의 지역 변수 주소를 누가 또 쓰는지를 잡는다. 옵션 목록은 LLVM 문서에 정리되어 있다.

### 7장·6장의 버그와 잇기

이 절을 마무리하기 전에 한 가지 짚어 두자. 7장 UB 예제, 6장 메모리 예제(누수, double free, use-after-free) — 이 모두가 이 한 쌍의 sanitizer로 잡힌다. 예제 디렉터리들의 `Makefile`이 모두 `-fsanitize=address,undefined`를 기본값으로 두고 있는 이유가 그거다. 우리가 일부러 심어 둔 버그가 도구의 도움 없이는 침묵하다가, 도구가 켜진 순간 즉시 발각되는 — 그 손맛을 책 전체에서 반복해서 보게 될 것이다.

### 워크플로 둘 — 어떻게 일상에 들이는가

도구가 손에 잡혔다면 일상에 들이는 두 가지 워크플로를 권한다.

**워크플로 (a) — 새 코드를 짤 때.** 처음부터 ASan 빌드로 짠다. `make` 디폴트 타깃을 ASan으로 두고, 코드를 한 줄 고칠 때마다 그 빌드로 돌린다. 미세한 메모리 사고가 일어나면 바로 그 자리에서 잡힌다. 디버거를 띄울 필요도 거의 없다. 진단 메시지가 워낙 친절해서 그 한 화면이 디버거 세션을 대체한다.

**워크플로 (b) — 옛 코드에 들어갈 때.** 레거시 코드베이스를 받아 처음 ASan을 켜면 한 가지 일이 일어난다. 그동안 침묵 속에 살던 사고들이 줄줄이 떨어진다. 좀 난감하다. 그러나 그게 정상이다. 한 번에 다 고치려 들지 말고, 가장 자주 도는 코드 경로 — 메인 진입점, 핵심 자료구조, 자주 호출되는 함수 — 부터 ASan을 통과시킨다. 작은 디렉터리부터 시작해 점차 범위를 넓혀 가는 패턴이 일을 가볍게 만든다.

## §2. 정점의 형제들 — TSan과 MSan

ASan/UBSan과 같은 sanitizer 가족에 두 명이 더 있다. ThreadSanitizer(TSan)과 MemorySanitizer(MSan).

**TSan(`-fsanitize=thread`).** 데이터 레이스를 잡는다. 두 스레드가 같은 메모리를 한쪽이라도 atomic 보호 없이 쓰면 레이스가 잡힌다. 오버헤드는 큰 편 — 5~15배. 멀티스레드 코드를 짤 때 필수에 가까운 도구지만, 이 책의 범위는 베어메탈로 가는 단일 스레드 코드 위주라 본격 사용은 하지 않는다. 호스트에서 멀티스레드 모듈을 다룰 일이 생기면 그때 다시 꺼낸다.

**MSan(`-fsanitize=memory`).** 초기화 안 된 메모리 읽기를 잡는다. 7장에서 본 손님 중 하나다. 그런데 한 가지 짜증나는 사실이 있다. **MSan은 macOS에서 제한적으로만 동작한다.** Apple Clang은 보통 MSan을 빼고 빌드되어 오고, Homebrew LLVM에서도 macOS에서는 운영 환경 라이브러리(libSystem)의 초기화 추적이 어려워 잡음이 많다. 한 가지 우회로는 Linux 컨테이너 안에서 MSan 빌드를 따로 돌리는 것이다. 책 범위에서는 깊이 들어가지 않는다.

이 두 형제가 자기 자리가 분명하다는 점을 알아 두자. 정점은 ASan과 UBSan이다.

## §3. macOS의 빈자리 — valgrind 부재

Linux에서 C를 만지던 사람이 macOS로 옮겨오면 한 도구가 그립다 — valgrind. 메모리 누수를 잡는 클래식한 도구다. 그런데 valgrind는 Apple Silicon에서 사실상 동작하지 않는다. M1 출시 이후 포팅 작업이 더디게 진행 중이고, 2026년 5월 시점에도 정식 지원과는 거리가 멀다. 좀 난감한 일이다.

다행히 그 빈자리를 메우는 세 갈래의 길이 있다.

**1) ASan + UBSan 조합.** 위에서 본 그 한 쌍이 valgrind가 잡는 일의 대부분을 더 빠르게, 더 정확하게 잡는다. 누수 검사도 위의 `detect_leaks=1`로 켤 수 있다. 사실상 첫 번째 선택지다.

**2) `leaks` 명령.** macOS에 내장되어 있다. `leaks --atExit -- ./a.out`이라고 치면 프로세스가 끝날 때 누수가 있는지 한 번 점검해 준다. ASan을 켜고 빌드할 수 없는 자리(외부 바이너리를 받아 누수만 확인하고 싶은 자리 등)에서 가볍게 쓰기 좋다.

**3) Instruments.** Xcode에 동봉된 GUI 프로파일러다. Allocations, Leaks, Time Profiler 같은 템플릿이 있다. 깊이 들어갈 자리는 아니지만, 메모리 사용 패턴을 시각적으로 보고 싶을 때 한 번씩 꺼내 쓸 만하다.

세 갈래를 다 알 필요는 없다. **ASan + UBSan이 90%다.** 나머지 둘은 그 90%의 빈자리를 메우는 보조 도구로 알아 두자.

## §4. 정적 분석 — 컴파일러가 직접 코드를 읽는다

여기까지가 런타임에 잡는 도구였다. 이번엔 컴파일 시점에 코드를 직접 읽어 의심스러운 자리를 찾아내는 도구로 가자. 정적 분석이라고 부른다. 네 가지가 가장 자주 거론된다.

### 비교 표 한 장으로

| 도구 | 무엇을 잡나 | 입력 | False Positive | CI 통합 |
|------|------------|------|----------------|---------|
| **clang-tidy** | 코딩 스타일, bug-prone 패턴(`bugprone-*`), CERT 규칙(`cert-*`), 가독성(`readability-*`) | `compile_commands.json` | 중간 (체크 종류별 차이 큼) | 매우 좋음. CMake에서 `CMAKE_C_CLANG_TIDY` 한 줄. |
| **scan-build** | 경로 추적 기반 분석. NULL 역참조 가능 경로, 누수 가능 경로 등 | 빌드 명령 가로채기 (`scan-build make`) | 낮음~중간 | HTML 리포트 생성. CI에선 그 리포트를 아티팩트로. |
| **cppcheck** | 외부 도구, 자기만의 패턴 라이브러리 | 그냥 소스 파일 | 중간 | 가능하지만 clang-tidy와 보완적 위치. |
| **GCC `-fanalyzer`** | GCC 10+ 옵션, 컴파일러에 내장된 분석 | 빌드 그 자체에 `-fanalyzer` 추가 | 낮음~중간 | GCC를 쓰는 빌드라면 켜 두는 게 무난. |

각 도구가 같은 코드를 보지만 다른 자리를 잡는다. clang-tidy는 패턴 매칭에 강하고, scan-build는 경로 추적이 강하고, cppcheck는 둘의 중간 어딘가, GCC `-fanalyzer`는 컴파일러가 만든 IR을 분석한다. 한 도구만 고른다면 **clang-tidy**가 무난한 출발점이다. LLVM에 묶여 따라오고, IDE 통합이 좋고, CMake 한 줄로 CI에 끼울 수 있다.

### clang-tidy 짧은 시연

`example/ch09-sanitizers/`에 `.clang-tidy` 설정을 둬 뒀다.

```yaml
---
Checks: >
  -*,
  bugprone-*,
  clang-analyzer-*,
  cert-*,
  readability-magic-numbers,
  readability-misleading-indentation
```

`-*`로 일단 모두 끄고 필요한 카테고리만 켜는 패턴이다. `bugprone-*`이 가장 실용적이다 — 흔히 사고로 이어지는 패턴을 잡는다. `cert-*`는 CERT C 보안 코딩 규칙 기반이고, `readability-*`는 가독성 향상.

빌드하고 돌려 보자.

```bash
$ clang-tidy bug.c -- -std=c17 -Wall -Wextra
```

`--` 뒤가 컴파일 옵션이다. clang-tidy는 코드를 컴파일러처럼 파싱한 뒤 체크를 돌려야 하기 때문에 컴파일 옵션을 알아야 한다. CMake에서는 `compile_commands.json` 한 파일로 그 정보를 자동 공급한다.

### MISRA·CERT — 한 박스 메모

자동차·항공·의료 같은 안전 critical 영역에서는 코딩 규칙이 더 엄격해진다. **MISRA C**가 자동차 진영에서 사실상 표준이고, **CERT C**가 보안 진영에서 자주 인용된다. 두 규칙 셋 모두 "이런 패턴은 피해라" 류의 항목 수백 개로 구성되어 있다. 일반 애플리케이션 개발에서 전부 지킬 필요는 없지만, clang-tidy의 `cert-*` 체크를 켜 두는 것만으로도 일정 부분 자동 점검이 들어온다. 깊이 들어가야 할 분야가 정해진 독자라면 별도 학습이 필요한 영역이다.

### 두 가지 워크플로

정적 분석을 매번 손으로 돌리면 잊어버린다. 두 가지 자리에 끼워 두는 게 정석이다.

**(a) Pre-commit hook.** 커밋 직전에 변경된 파일만 clang-tidy로 빠르게 점검한다. 한 번에 코드베이스 전체를 돌리지 않으니 시간이 짧고, 새 버그가 들어오는 시점에 발각된다.

```bash
# .git/hooks/pre-commit (실행 권한 부여)
#!/bin/sh
changed=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.c$' || true)
[ -z "$changed" ] && exit 0
clang-tidy $changed -p build || exit 1
```

**(b) CI에서 scan-build.** PR이 올라올 때 scan-build를 한 번 돌려 HTML 리포트를 아티팩트로 첨부한다.

```bash
$ scan-build --html-title="PR #123" cmake --build build
```

리뷰어가 그 리포트를 다운로드해 PR과 같이 본다. False positive가 섞여 있어도, "어디를 한 번 더 봐야 하나"를 잡아 주는 가이드로는 충분히 가치 있다.

### 정적 분석을 처음 켤 때의 마음가짐

옛 코드베이스에 정적 분석을 처음 켜면 ASan을 처음 켰을 때와 비슷한 일이 벌어진다. 경고가 수백 개씩 쏟아진다. 이때 두 가지 함정에 빠지기 쉽다. 첫째, **모든 경고를 한 번에 다 고치려는 함정.** 분량이 압도해서 결국 도구를 꺼 버린다. 둘째, **경고 자체를 끄려는 함정.** `// NOLINT`를 마구 박아 도구를 무용지물로 만든다. 둘 다 결과가 좋지 않다.

권하는 자세는 이렇다 — 새로 추가되는 코드에만 정적 분석을 강제하는 것. CI 게이트가 "변경된 파일에 새 경고가 생기면 막는" 식으로 동작하면 된다. 기존 경고는 그 자리에 둔 채 점차 줄여 가는 식이다. 코드베이스가 자기 속도로 정돈된다. 처음부터 빨간색 0개를 노리지 말자.

## §5. clang-format — 스타일 일원화

여기서 잠깐 호흡을 가다듬자. 도구라기보다는 자동화에 가까운 자리, clang-format이다. 코드 스타일을 한 줄로 통일해 주는 도구다.

```yaml
# .clang-format
---
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
AlwaysBreakAfterReturnType: None
```

기본 스타일을 LLVM/Google/Mozilla/Microsoft/WebKit 같은 프리셋 중에서 고르고, 그 위에 자기 프로젝트의 변형(들여쓰기 폭, 줄 길이 등)을 적는다. 그러면 한 줄로 정렬이 끝난다.

```bash
$ clang-format -i src/*.c          # 파일을 직접 고친다
$ clang-format --dry-run --Werror src/*.c   # CI에서 형식 위반을 에러로
```

스타일 논쟁을 처음부터 끝내 버리는 방법이다 — 사람이 다투지 말고 도구가 정한 대로 가자. 작은 팀에서도 큰 효과가 있다. 한 번 셋업하고 잊을 수 있다.

## §6. libFuzzer — 도구가 입력을 만들어 코드를 두드린다

이제 가장 흥미로운 도구로 가 보자. 퍼저(fuzzer)다. 사람이 테스트 케이스를 한 줄씩 손으로 적는 게 아니라, 도구가 무작위에 가까운 입력을 끊임없이 만들어 코드를 두드린다. 그 두드림이 크래시를 일으키면 그 입력을 저장한다. 이게 보안 취약점 발견의 가장 효과적인 방법 중 하나로 자리 잡았다.

LLVM에 동봉된 **libFuzzer**가 입문하기 가장 좋다. 한 줄짜리 플래그로 시작하고, ASan과 결합되어 "크래시 + 메모리 에러"를 동시에 잡는다.

### 6단계로 끝나는 미니 튜토리얼

**1) Fuzz target 함수 작성.**

```c
/* fuzz_target.c */
#include <stdint.h>
#include <stddef.h>
#include "myparser.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    myparser_parse(data, size);   /* 우리 코드가 무작위 입력을 받는다 */
    return 0;
}
```

libFuzzer는 `LLVMFuzzerTestOneInput`이라는 정확한 시그니처의 함수를 찾는다. 그 함수가 호출되는 횟수와 입력의 모양이 도구의 손에 달렸다.

**2) 빌드.**

```bash
$ clang -fsanitize=fuzzer,address -g \
        -I include \
        fuzz_target.c myparser.c -o fuzz_app
```

`-fsanitize=fuzzer,address`가 핵심이다. ASan과 같이 켜 두면 크래시 외에도 메모리 에러까지 잡는다.

**3) Corpus 디렉터리 만들기.**

```bash
$ mkdir corpus
$ echo "hello" > corpus/seed1
$ echo "{\"a\":1}" > corpus/seed2
```

corpus는 도구가 시작점으로 쓰는 "씨앗 입력"들의 모음이다. 잘 짠 씨앗이 있으면 fuzzing이 훨씬 빠르게 흥미로운 코드 경로에 도달한다.

**4) 돌리기.**

```bash
$ ./fuzz_app corpus
```

libFuzzer가 corpus의 입력들을 변형하면서 끊임없이 새 입력을 만들어 우리 파서에 던진다. 한 번에 수천 번씩, 도구의 손이 빠르다.

**5) 크래시 재현.**

크래시가 발생하면 `crash-deadbeef...`라는 이름의 파일이 현재 디렉터리에 떨어진다. 그 파일이 크래시를 일으킨 입력이다. 디버거에 그 입력을 한 번 더 넣어 보면 같은 크래시가 재현된다.

```bash
$ ./fuzz_app crash-deadbeef
```

**6) Coverage 시각화 (선택).**

`-fprofile-instr-generate -fcoverage-mapping`을 추가로 켜고 빌드한 뒤 fuzzing을 돌리면, 코드의 어느 줄이 얼마나 자주 닿았는지를 시각화할 수 있다. 닿지 않은 분기가 있다면 그 분기에 도달하는 입력을 corpus에 추가해 fuzzing을 더 깊게 끌고 갈 수 있다.

### ASan과 결합되는 이유

위 6단계에서 한 가지를 다시 짚자. `-fsanitize=fuzzer,address`. 왜 ASan과 묶일까? 퍼저가 만든 입력으로 코드가 크래시하지 않더라도, 옆 메모리를 조금씩 갉아먹는 종류의 버그(off-by-one, use-after-free)는 그 자체로는 즉시 죽지 않을 수 있다. ASan이 같이 켜져 있으면 그런 미세한 갉아먹기까지 잡아낸다. 두 도구가 같이 갈 때의 시너지가 그것이다.

베어메탈/freestanding 환경에서는 libFuzzer를 직접 돌리기 어렵다. 런타임이 libc에 의존하기 때문이다. 11장의 freestanding 절에서 다시 만나겠지만, 한 가지 우회로는 — **호스트 측에서 모듈만 빼서 fuzzing**하는 것이다. UART 드라이버 자체는 호스트에서 돌릴 수 없지만, 그 드라이버가 받는 입력을 파싱하는 함수는 호스트에서 fuzzing 가능하다. 그 분리가 fuzzing 가능한 코드와 그렇지 않은 코드의 경계가 된다.

### Fuzz target을 짤 때의 작은 원칙

fuzz target을 짜다 보면 한 가지 손에 익는 원칙이 있다 — **target은 빠르고 결정적이어야 한다**. 한 번의 호출이 길어지면 도구가 그만큼 적은 입력을 시도하게 되고, 비결정적이면 같은 입력으로 같은 결과가 안 나와 크래시 재현이 어렵다. 그래서 fuzz target 안에서는 파일 시스템·네트워크·전역 상태에 손대지 않는 게 정석이다. 입력을 받고, 우리 함수에 한 번 던지고, 끝낸다. 그 단순함이 도구의 손을 빠르게 만든다.

## §7. 권장 빌드 매트릭스 — 책의 모든 예제가 따르는 표 한 장

지금까지 만난 도구들을 한 표로 묶자. 책의 모든 예제는 이 매트릭스 안에서 산다.

| 빌드 | 용도 | 옵션 묶음 | 켜진 도구 |
|------|------|----------|----------|
| **Debug-ASan** | 일상 개발의 기본값 | `-O1 -g -fsanitize=address -fno-omit-frame-pointer` | ASan |
| **Debug-UBSan** | UB 종류를 잡고 싶을 때(보통 ASan과 같이) | `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer` | ASan + UBSan |
| **Release** | 배포·성능 측정 | `-O2 -DNDEBUG -Wall -Wextra` | 없음 (sanitizer 꺼짐) |
| **CI-Static** | PR 점검 | Release 빌드 + `scan-build` + `clang-tidy` | 정적 분석 두 종 |
| **Bare-metal** | 11장 이후 베어메탈 | `-O2 -ffreestanding -nostdlib -nostartfiles -mgeneral-regs-only` | sanitizer 꺼짐(런타임 없음) |

다섯 빌드의 위치가 분명하다. 첫 두 빌드(ASan/UBSan)가 일상 개발의 자리고, 세 번째 Release가 배포의 자리, 네 번째 CI-Static이 PR 게이트, 다섯 번째 Bare-metal이 베어메탈로 가는 자리다. 베어메탈 빌드에서 sanitizer가 꺼지는 이유는 **sanitizer 런타임이 호스트 libc에 의존**하기 때문이다. 베어메탈에는 libc가 없으니 sanitizer가 링크에 실패한다. 이 한 가지가 베어메탈 디버깅이 다른 영역보다 손에 잡기 어려운 이유 중 하나다.

### Make로 짠 매트릭스 템플릿

```make
CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic -g -fno-omit-frame-pointer
CSTD     = -std=c17

ASAN_FLAGS  = -fsanitize=address $(WARN) $(CSTD)
UBSAN_FLAGS = -fsanitize=address,undefined $(WARN) $(CSTD)
REL_FLAGS   = -O2 -DNDEBUG -Wall -Wextra $(CSTD)

.PHONY: asan ubsan release tidy scan matrix

asan: bug.c
	$(CC) $(ASAN_FLAGS) bug.c -o bug_asan
	./bug_asan

ubsan: bug.c
	$(CC) $(UBSAN_FLAGS) bug.c -o bug_ubsan
	./bug_ubsan

release: bug.c
	$(CC) $(REL_FLAGS) bug.c -o bug_release
	./bug_release

tidy:
	clang-tidy bug.c -- $(CSTD) $(WARN)

scan:
	scan-build $(CC) $(WARN) $(CSTD) -c bug.c

matrix: asan ubsan release
```

`make matrix` 한 줄이 첫 세 빌드를 차례로 돌린다. CI는 거기에 `tidy`와 `scan`을 더한다. 베어메탈은 다른 디렉터리의 다른 Makefile로 분리해 두는 게 깔끔하다.

### CMake로 짠 매트릭스 템플릿

```cmake
cmake_minimum_required(VERSION 3.20)
project(myapp C)
set(CMAKE_C_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(SANITIZE "Enable ASan + UBSan" OFF)
if(SANITIZE)
    add_compile_options(
        -fsanitize=address,undefined
        -fno-omit-frame-pointer -g -O1)
    add_link_options(-fsanitize=address,undefined)
endif()

add_executable(app main.c util.c)
```

빌드 방향은 옵션으로 분기한다.

```bash
$ cmake -B build-asan -DSANITIZE=ON
$ cmake -B build-rel  -DCMAKE_BUILD_TYPE=Release
$ cmake --build build-asan && cmake --build build-rel
```

같은 소스 트리에서 여러 빌드 디렉터리를 둘 수 있다는 게 CMake의 강점이다. ASan 빌드와 Release 빌드를 동시에 띄워 두고 비교해 볼 수 있다.

### 매트릭스를 일상에 들이는 한 가지 습관

좋은 도구는 켜 두지 않으면 없는 것과 같다. 한 가지 습관을 권한다 — **`make` 디폴트 타깃을 `asan`으로 두는 것**.

```make
.DEFAULT_GOAL := asan
```

이 한 줄이면 그냥 `make`라고 쳤을 때 sanitizer 빌드가 돈다. 빌드 시간이 약간 더 걸리지만, 그 약간의 비용이 새벽 두 시의 며칠을 막아 준다. 일상 빌드의 기본값이 sanitizer가 켜진 빌드 — 이게 이 장의 가장 큰 자산이다. 기억해 두자.

## 챕터를 닫으며

이 장에서 만난 손님들을 정리하자. 정점에는 ASan과 UBSan. 그 곁에 TSan/MSan이라는 형제들. macOS의 valgrind 부재를 메우는 세 갈래 — sanitizer, `leaks`, Instruments. 정적 분석 네 도구(clang-tidy, scan-build, cppcheck, GCC `-fanalyzer`)와 두 워크플로(pre-commit, CI). 스타일을 한 줄로 통일하는 clang-format. 도구가 입력을 만드는 libFuzzer. 마지막으로 다섯 빌드의 매트릭스.

매트릭스가 머릿속에 그려졌다면 이 장의 목표는 이루었다. 어떤 빌드에 무엇을 켜는가 — Debug에는 ASan/UBSan, Release에는 깨끗하게, CI에는 정적 분석, 베어메탈에는 sanitizer 끄고. 이 표가 우리 손에 있다면 코드가 무너지는 자리를 손가락으로 짚어 가며 일할 수 있다. C가 침묵하는 사이에 도구가 말을 걸어 주는 — 그게 안전망의 정체다.

이제 도구를 손에 잡았으니, 다음 장에서 C 표준 라이브러리의 빈자리를 정면으로 보자. 문자열의 한계, 컨테이너의 부재, POSIX와 C 표준의 거리, libc 구현체들의 미묘한 차이 — 이 네 자리를 한 절씩 끊어서 짚으면 "표준 라이브러리만으로 어디까지 가는가"의 지도가 손에 들어온다. 자작 도구를 짤 시간이 다가오고 있다.
