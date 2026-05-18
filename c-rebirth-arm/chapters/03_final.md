# 3장. Mac에서 C 개발하기 — Apple Silicon Day 0

새로 산 MacBook을 켰다고 상상해보자. 깨끗한 macOS 위에 아직 아무것도 안 깔려 있다. 옆에는 이 책이 펼쳐져 있고, 머리 한구석에는 "12장에서 QEMU 위에 자기 커널을 띄운다"는 약속이 박혀 있다. 한 시간 안에 그 약속의 출발점까지 가려면, 지금부터 무엇을 깔아야 할까?

이게 이 장의 핵심 질문이다. **Apple Silicon Mac을 켜고 한 시간 안에 C 개발 환경이 완성되려면 무엇을 깔고 무엇을 PATH에 올려야 하는가?** 길게 끌고 갈 이야기는 아니다. 핵심 도구를 차례로 깔고, 함정 몇 곳을 피하고, 마지막에 `hello.c`가 sanitizer까지 켜서 통과하는지 확인하면 그날의 의식은 끝이다. 다음 장부터의 모든 예제가 이 한 시간 위에서 빌드된다.

손을 더럽혀보자.

## 첫 줄 — Xcode Command Line Tools

Mac에서 C 개발의 출발점은 의외로 간단하다. 터미널을 열고 한 줄.

```bash
xcode-select --install
```

이 한 줄이 통과하면 Xcode Command Line Tools (CLT)가 깔린다. 안에 무엇이 들어 있느냐.

- **Apple Clang** — `cc`, `clang` 명령. 이게 우리 컴파일러다.
- **lldb** — LLVM 진영의 디버거. Apple Silicon에서 사실상 표준.
- **Make** — `make`. 옛날부터 친한 그 빌드 도구.
- **git** — 버전 관리.
- 그리고 macOS SDK 헤더와 라이브러리.

이 한 줄로 macOS의 C 개발 출발점이 거의 다 잡힌다. **여기까지가 Day 0의 5분이다.** Xcode 본체(GUI 앱)는 깔 필요 없다. 우리가 쓸 일이 별로 없다. CLT만 깔린 상태에서도 베어메탈 챕터까지 거의 다 갈 수 있다.

그런데 한 가지 미묘한 사실을 짚어두자. **Apple Clang은 LLVM 본가보다 조금씩 늦다.** Apple은 자사 SDK와 묶어서 컴파일러를 배포하기 때문에, 최신 C23 기능이 들어오는 시점이 LLVM 본가보다 한 박자 늦다. 보통은 이게 큰 문제가 안 되지만, C23의 최첨단 기능(예: `<stdbit.h>`의 일부)을 적극 쓰고 싶다면 Homebrew의 LLVM을 추가로 까는 편이 낫다. 그 이야기는 잠시 뒤에 하자.

## 두 번째 줄 — Homebrew

다음 도구는 패키지 관리자다. macOS의 사실상 표준 패키지 관리자는 **Homebrew**다. 깔자.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치 스크립트가 알아서 다 해준다. 다만 한 가지를 의식하자. **Apple Silicon Mac에서 Homebrew는 `/opt/homebrew` 접두어를 쓴다.** Intel Mac은 `/usr/local`이다. 이 차이가 PATH·환경 변수 설정에서 자주 함정이 된다.

설치가 끝나면 Homebrew가 친절하게 PATH 설정 한 줄을 알려준다. 보통 `~/.zprofile` 또는 `~/.zshrc`에 다음 한 줄을 추가하라고 한다.

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

이 한 줄이 PATH, MANPATH, INFOPATH를 한꺼번에 설정해준다. 친절하다. 이제 터미널을 새로 열어보자. `brew --prefix`가 `/opt/homebrew`를 돌려준다면 1차 통과다.

여기서 짧게 한 가지 더 짚어두자. **Intel Mac에서 옮겨온 사람이 가장 많이 겪는 통증이 PATH 차이다.** 옛 dotfiles에 `/usr/local/bin`을 박아뒀다면 Apple Silicon에서는 그게 동작하지 않는다. `brew`를 호출했는데 "command not found"가 뜨면, 십중팔구 PATH가 `/opt/homebrew/bin`을 모르고 있는 상황이다. `~/.zshrc`를 한 번 정리해두자. 그게 첫 번째 함정 회피다.

## 세 번째 줄 — 모던 LLVM과 빌드 도구

Apple Clang은 기본 도구로 충분하다. 다만 깊이 들어가다 보면 추가 도구가 필요해진다. 한 줄로 다 깔자.

```bash
brew install llvm gcc cmake ninja pkg-config
```

각각이 무엇을 가져오는지 살펴보자.

- **llvm** — Homebrew의 모던 LLVM. Apple Clang보다 신선한 clang, 그리고 `clangd`(LSP 서버), `clang-tidy`(정적 분석), `clang-format`(포매터), `scan-build`(정적 분석), `lld`(링커)까지 한 묶음. 4장에서 IDE 셋업의 핵심이 된다.
- **gcc** — 진짜 GCC. macOS에서 `gcc` 명령은 사실 Apple Clang에 대한 심볼릭 링크다. 진짜 GCC를 부르려면 `gcc-14`(버전 명시)로 부른다. 이 함정은 잠시 뒤에 좀 더 짚자.
- **cmake** — 현대적 빌드 시스템 생성기. `compile_commands.json`을 만들어줘서 IDE와 LSP의 출발점이 된다.
- **ninja** — CMake가 생성하는 빌드 파일을 실행하는 백엔드. Make보다 빠르다.
- **pkg-config** — 라이브러리 메타데이터 도구. 외부 라이브러리를 링크할 때 도움.

**한 가지 주의.** Homebrew의 LLVM은 PATH 충돌을 피하려고 "keg-only"로 깔린다. 자동으로 PATH에 들어가지 않는다는 뜻이다. 그래서 Apple Clang을 안 쓰고 Homebrew LLVM을 우선시하려면 `~/.zshrc`에 다음 줄을 박아둬야 한다.

```bash
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/llvm/lib"
export CPPFLAGS="-I/opt/homebrew/opt/llvm/include"
```

이걸 박아두면 `clang` 명령이 Homebrew LLVM의 신선한 clang을 가리킨다. 안 박아두면 Apple Clang이 그대로 우선이다. **둘 다 동작하는 답이다.** 다만 어느 쪽을 기본값으로 정했는지 자기가 알고는 있자. 안 그러면 "어제는 됐는데 오늘은 안 되네" 하는 미궁에 빠진다.

이 책의 호스트 챕터(Ch1~Ch10)는 둘 다 통과한다는 가정을 한다. 굳이 Homebrew LLVM이 필요한 자리는 C23의 일부 최신 기능이거나 `clang-format` 같은 부가 도구가 필요할 때 정도다.

### Apple Clang과 Homebrew LLVM, 어느 쪽을 기본값으로?

여기서 한 가지 질문이 따라온다. **두 컴파일러가 다 깔렸을 때 어느 쪽을 기본값으로 정할까?** 정답이 정해진 문제는 아니다. 다만 권장은 있다.

**Apple Clang을 기본값으로 두는 편이 낫다.** 이유는 셋이다. 첫째, Apple이 자기 SDK·시스템 라이브러리와의 정합성을 가장 잘 맞춰준다 — Mach-O 링킹, macOS SDK 헤더 경로, 코드 서명 등이 자연스럽다. 둘째, 호스트에서 도구를 쓰다 보면 다른 사람이 만든 Makefile이 `clang`/`cc`를 그냥 부르는 경우가 많은데, 그 자리에 Apple Clang이 들어와 있는 게 잡음을 줄인다. 셋째, C23의 거의 모든 일반적 기능은 Apple Clang 16 이상에서도 이미 동작한다 — 우리가 이 책에서 다루는 범위에서는 큰 차이가 없다.

Homebrew LLVM은 보조 도구로 두자. **새 표준의 최첨단 기능을 시도해보고 싶을 때**나 **`clangd`, `clang-tidy`, `clang-format` 같은 부속 도구의 최신 버전이 필요할 때** 명시적으로 부르면 된다. 예를 들면 이런 식이다.

```bash
/opt/homebrew/opt/llvm/bin/clang -std=c23 ...
```

또는 Homebrew LLVM 경로를 PATH 맨 앞에 일시적으로 올려두고 작업한다.

```bash
PATH="/opt/homebrew/opt/llvm/bin:$PATH" clang --version
```

이렇게 명시적으로 부르면 어느 컴파일러가 도는지 헷갈리지 않는다. 단순한 게 좋다.

## 네 번째 줄 — 베어메탈 크로스 컴파일러

이제 가장 중요한 한 줄이다. **베어메탈 챕터를 위한 준비를 미리 끝내자.**

```bash
brew install aarch64-elf-gcc arm-none-eabi-gcc
```

두 개를 한 번에 깔았다. 각각이 무엇인가.

- **aarch64-elf-gcc** — 64비트 ARM 베어메탈용 크로스 컴파일러. Cortex-A 계열(Raspberry Pi 4의 Cortex-A72 포함)을 타깃으로 한다. ELF 바이너리를 만든다.
- **arm-none-eabi-gcc** — 32비트 ARM 임베디드용. Cortex-M 계열(STM32 같은 마이크로컨트롤러)을 타깃으로 한다.

여기서 가장 자주 부딪히는 함정 하나를 짚어두자. **`aarch64-elf` ≠ `aarch64-apple-darwin`.**

이게 무슨 소리인가. Apple Silicon Mac 자체가 AArch64 ARM이다. 그래서 Apple Clang의 기본 타깃이 `arm64-apple-darwin`(macOS용 Mach-O 바이너리)이다. 한쪽도 ARM이고 다른 한쪽도 ARM이지만 — 바이너리 포맷이 다르다. macOS는 Mach-O를 쓰고, 베어메탈/Linux는 ELF를 쓴다. 베어메탈 ARM 코드를 빌드하려면 ELF를 만들 줄 아는 컴파일러가 필요하고, 그게 `aarch64-elf-gcc`다.

이 사실을 안 짚으면 12장에서 한 번은 막힌다 — Apple Clang으로 그냥 빌드했더니 ELF가 아닌 Mach-O가 나와서 QEMU가 못 읽는 식의 일이다. **지금 미리 한 번 새겨두자.** 같은 ARM이라도 누구를 위한 ARM이냐가 다르다.

`aarch64-elf-gcc`가 깔렸는지 확인해보자.

```bash
aarch64-elf-gcc --version
```

버전 정보가 뜨면 통과다. 안 뜨면 Homebrew 설치가 PATH에 들어왔는지부터 보자.

## 다섯 번째 줄 — 에뮬레이터와 디스어셈블러

베어메탈 코드를 실제 보드에 굽기 전에, 에뮬레이터로 먼저 돌려보는 게 사실상 표준이다. 그 에뮬레이터가 QEMU다.

```bash
brew install qemu binutils
```

- **qemu** — 다양한 아키텍처를 에뮬레이트해주는 도구. `qemu-system-aarch64`로 64비트 ARM 시스템을 통째로 시뮬레이션한다. 12장에서 우리가 만들 첫 커널이 이 위에서 돈다.
- **binutils** — `objdump`, `nm`, `readelf` 등 바이너리 분석 도구. ELF 파일을 분해해서 들여다볼 때 결정적.

`qemu-system-aarch64 --version` 한 줄로 통과 확인. 보통은 QEMU 9.0 이상이 깔린다(현재 시점). Raspberry Pi 4 머신 모델(`raspi4b`) 지원이 9.0(2024-04)부터 들어왔으니, 그 이상 버전이면 14장의 raspi4 에뮬레이션까지 한 번에 잡힌다.

## `cc`, `clang`, `gcc`의 이름 함정

깔 거 다 깔았으면 이제 함정 정리를 좀 더 깊게 해두자. macOS의 컴파일러 이름이 어딘가 헷갈리는데, 그 함정을 짧게 풀어두자.

```bash
which cc clang gcc
```

이걸 두드려보면 보통 이런 결과가 나온다.

```
/usr/bin/cc
/usr/bin/clang
/usr/bin/gcc
```

세 명령이 모두 `/usr/bin`에 있다. 다 다른 컴파일러일까? 아니다. **`/usr/bin/gcc`는 사실 Apple Clang이다.** `gcc --version` 한 번 두드려보자. "Apple clang version ..."이라고 자기 정체를 솔직하게 밝힌다. macOS는 옛날부터 GCC를 빼고 Clang을 그 자리에 앉혔는데, 호환성을 위해 `gcc`라는 이름을 그대로 남겨뒀다. 이게 이름 함정의 출발점이다.

진짜 GCC를 부르고 싶다면 Homebrew로 깐 `gcc-14`(또는 깔린 버전) 명령을 명시적으로 써야 한다.

```bash
gcc-14 --version
```

이게 진짜 GCC다. 일반적인 호스트 개발에서는 굳이 진짜 GCC를 부를 일이 적다. Apple Clang으로 충분하다. 그러나 두 컴파일러의 동작 차이를 비교해보고 싶을 때는 `gcc-14`로 부르면 된다. **`gcc`라는 이름이 진짜 GCC를 부르는 게 아니라는 사실 — 이걸 모르고 있으면 한 번은 어지러워진다.**

비슷한 종류로 `cc`도 그냥 Apple Clang의 다른 이름이다. 옛 Makefile에서 `cc`라고 적어두면 Mac에서는 자동으로 Apple Clang이 통과한다는 게 그래서다. 우리도 이 책의 Makefile들에서 종종 `CC ?= clang` 같은 식으로 적어둘 텐데, 그건 사용자가 `make CC=gcc-14`로 부르고 싶을 때 길을 열어두기 위함이다.

## 정합성 점검 — Day 0의 마지막 의식

도구를 다 깔았으면 마지막으로 한 가지 의식이 남았다. **모든 게 진짜로 동작하는지 확인하기.** 이게 Day 0의 마지막 30초다.

이번 장의 예제 디렉토리(`example/ch03-day0-setup/`)에 두 가지가 들어 있다.

첫 번째는 `check_env.sh`라는 환경 점검 스크립트다. `make check` 한 줄이면 깔린 도구 목록과 버전을 한 화면에 보여준다.

```
--- 호스트 도구 ---
  [ok ] clang                  : Apple clang version 21.0.0 ...
  [ok ] lldb                   : lldb-2100.0.16.4
  [ok ] make                   : GNU Make 3.81
  [ok ] git                    : git version 2.49.0
  ...

--- 베어메탈 / 에뮬레이션 ---
  [ok ] aarch64-elf-gcc        : ...
  [ok ] qemu-system-aarch64    : QEMU emulator version ...

--- LLVM 도구 ---
  [ok ] clangd                 : ...
  [ok ] clang-tidy             : ...
  ...

--- Homebrew 접두어 ---
  HOMEBREW_PREFIX = /opt/homebrew
```

`[ok]` 표시가 줄줄이 뜨면 통과다. `[--]` 표시가 보이면 그 도구가 아직 깔려 있지 않다는 뜻이다. 빠진 게 있어도 스크립트는 멈추지 않고 끝까지 다 본다. 어떤 도구가 안 깔려 있는지 한눈에 보는 게 목적이라서 그렇다. 필요해진 시점에 `brew install`로 채우면 된다.

두 번째는 `triple.c`라는 작은 파일이다. `make run` 한 줄이면 빌드되어 실행되고, **지금 이 컴파일러가 자기를 어떻게 부르고 있는지** 화면에 그대로 보여준다.

```
--- compiler self-report ---
  toolchain         : clang 21.0.0
  __VERSION__       : Apple LLVM 21.0.0 ...
  __STDC_VERSION__  : 201710

--- target identity ---
  __aarch64__       : 1 (AArch64, 64-bit ARM)
  __x86_64__        : 0
  __APPLE__         : 1 (Apple platform — Mach-O)
  __linux__         : 0

--- byte order ---
  endianness        : little (Apple Silicon / ARM 기본)
```

별것 아닌 출력처럼 보일 수 있다. 그러나 이 한 화면에 몇 가지 진실이 적혀 있다. **컴파일러가 자기 정체를 안다.** `__clang__`, `__aarch64__`, `__APPLE__`, `__BYTE_ORDER__` 같은 매크로가 그 정보를 우리 코드에 내려준다. 베어메탈 챕터에 가면 우리는 이 매크로들을 적극 활용한다 — "이 코드를 호스트에서 빌드 중인가, 베어메탈로 크로스 컴파일 중인가"를 매크로로 분기해야 할 자리가 자주 나온다. 미리 손에 익혀두는 편이 낫다.

특히 한 가지 짚어두자. **Apple Silicon Mac은 자기가 이미 `__aarch64__` 위에서 도는 ARM 시스템이다.** 그래서 호스트에서 빌드한 코드도 ARM 명령어로 생성된다. 12장에서 우리가 베어메탈 ARM 코드를 빌드할 때도 같은 ARM이지만, 다른 점은 두 가지다 — (1) 바이너리 포맷이 Mach-O가 아닌 ELF, (2) 표준 라이브러리 가정이 없는 freestanding 모드. 그 차이만 정확히 알면 베어메탈은 호스트와 그리 멀지 않다. 그 거리감을 줄이는 출발점이 바로 이 `triple.c`다.

## lldb를 한 번 만나두자

도구를 깔았으니 디버거도 짧게 한 번 만나두자. Mac에서 C를 디버깅한다면 사실상 표준은 **lldb**다. LLVM 진영의 디버거고, Apple이 Xcode와 묶어서 배포한다. gdb는 Apple Silicon에서 코드 서명 문제로 손이 많이 가니, 처음 시작하는 사람이라면 lldb로 가는 편이 무난하다.

간단한 시연 한 번 해보자. `Ch1`의 `hello.c`를 디버그 심볼과 함께 빌드한다.

```bash
clang -std=c17 -g -O0 hello.c -o hello
```

그리고 lldb로 띄운다.

```bash
lldb ./hello
```

프롬프트가 뜨면 친구 몇 명만 알아두자.

```
(lldb) break set -n main          # main 진입에 브레이크포인트
(lldb) run                         # 실행
(lldb) next                        # 다음 줄 (step over)
(lldb) step                        # 함수 안으로 들어가기 (step in)
(lldb) print x                     # 변수 x 출력
(lldb) frame variable              # 현재 프레임의 모든 변수
(lldb) backtrace                   # 콜 스택
(lldb) continue                    # 계속 실행
(lldb) quit                        # 종료
```

gdb를 써본 경험이 있다면 명령 이름이 다를 뿐 같은 풍경이다. `break set`은 gdb의 `break`, `next`는 그대로 `next`, `print`도 그대로다. 한 번 띄워서 `main`에 멈춰보고, `print` 한 줄로 변수 값을 들여다보고, `continue`로 끝까지 가보자. 그 짧은 의식 한 번이면 디버거가 도구 상자에 들어왔다고 봐도 좋다.

VS Code에서 lldb를 GUI로 쓰고 싶다면 **CodeLLDB**라는 익스텐션이 표준이다. 4장에서 본격적으로 다루겠지만, 미리 깔아둬도 손해 볼 일은 없다.

## sanitizer 켠 hello.c — 다음 챕터로의 다리

마지막으로 한 가지 더 해보자. 모던 C 개발의 진짜 검증은 sanitizer가 켜진 상태에서 hello가 통과하느냐다. 9장에서 본격적으로 다룰 도구지만, Day 0의 마지막 의식으로 짧게 만나보자.

```bash
clang -std=c17 -Wall -Wextra -Wpedantic \
      -fsanitize=address,undefined -g \
      hello.c -o hello && ./hello
```

이 한 줄이 무엇을 하는가.

- `-std=c17` — 표준 명시.
- `-Wall -Wextra -Wpedantic` — 경고 트리오.
- **`-fsanitize=address,undefined`** — AddressSanitizer(메모리 오류 감지)와 UndefinedBehaviorSanitizer(UB 감지)를 켠다. C가 침묵해버리는 버그를 도구가 잡아 준다.
- `-g` — 디버그 심볼. 에러 메시지에 줄 번호가 나오게 한다.

`hello, c17`이 화면에 찍히면 통과다. 별다른 에러가 안 떴다는 건 sanitizer 런타임도 같이 잘 깔렸다는 뜻이고, **Apple Silicon Mac의 C 개발 환경이 80% 완성됐다는 신호**다. 베어메탈로 가는 발판은 이미 갖춰진 셈이다.

9장에서 sanitizer의 본격적인 활용을 다룰 때, 이 단순한 한 줄이 어떻게 메모리 오버플로와 use-after-free와 정수 오버플로를 잡아내는지 손으로 보게 될 것이다. 지금은 이 환경 위에서 빌드가 통과한다는 것만 확인하자. 그게 Day 0의 마지막 의식이다.

## 한 시간이 지난 자리에서

여기까지 따라왔다면 한 시간이 채 안 걸렸을 것이다. 깔린 게 무엇이냐 정리해보자.

- Xcode CLT — Apple Clang, lldb, Make, git, macOS SDK.
- Homebrew — `/opt/homebrew` 접두어, 다음 모든 패키지의 출발점.
- llvm — Homebrew의 모던 LLVM, clangd, clang-tidy, clang-format.
- gcc — 진짜 GCC (필요할 때만 부른다).
- cmake, ninja, pkg-config — 모던 빌드 도구 일습.
- aarch64-elf-gcc — 64비트 ARM 베어메탈용 크로스 컴파일러.
- arm-none-eabi-gcc — 32비트 ARM 임베디드용.
- qemu, binutils — 에뮬레이터와 디스어셈블러.

이만큼이 깔렸다면 이 책의 모든 챕터를 통과할 수 있다. 호스트 챕터는 Apple Clang으로, 베어메탈 챕터(11~15장)는 `aarch64-elf-gcc` + QEMU로. **다음 챕터부터의 모든 예제가 이 한 시간 위에서 빌드된다.**

그리고 함정 몇 곳을 미리 새겨뒀다. Apple Silicon의 Homebrew 접두어가 `/opt/homebrew`라는 점, `gcc` 이름이 사실 Apple Clang이라는 점, `aarch64-elf`와 `aarch64-apple-darwin`이 같은 ARM이지만 바이너리 포맷이 다르다는 점, sanitizer는 디버그 빌드에 켜두면 든든하다는 점. 이 네 가지를 머리 어디엔가 박아두자.

## 한 가지 보너스 — `~/.zshrc` 정리 한 번

Day 0의 마지막에 사소하지만 큰 도움이 되는 의식 하나를 권한다. `~/.zshrc`를 한 번 정리하는 것이다. 이 책을 따라가면서 추가할 환경 변수가 늘어날 텐데, 출발점에서 한 번 정리해두면 나중에 헷갈리지 않는다. 권장 골격은 이렇다.

```bash
# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# (선택) Homebrew LLVM을 Apple Clang보다 우선
# export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
# export LDFLAGS="-L/opt/homebrew/opt/llvm/lib"
# export CPPFLAGS="-I/opt/homebrew/opt/llvm/include"

# 베어메탈 크로스 컴파일러는 Homebrew가 PATH에 알아서 올려주니 별도 설정 불필요
```

LLVM 라인을 주석으로 비워둔 건 의도다. 일단 Apple Clang을 기본으로 두고, 필요해진 시점에 주석을 풀면 된다. 처음부터 다 켜두면 어디서 어떤 도구가 도는지 혼란스러워진다. **단순한 게 좋다.** 필요해질 때 한 줄씩 추가하는 편이 낫다.

## 마무리

이번 장은 손을 더럽혀가는 챕터였다. 큰 그림보다는 명령 한 줄 한 줄로 환경을 깔았고, 함정을 새겼고, 마지막에 sanitizer 켠 `hello.c`가 통과하는지로 마무리했다. 한 시간 만에 끝나는 의식이지만, 이 한 시간이 다음 12개 챕터의 발판이다.

**기억해두자.**

- **`xcode-select --install`이 출발점이다.** 그 한 줄로 Apple Clang, lldb, Make, git이 한꺼번에 들어온다.
- **Apple Silicon Homebrew는 `/opt/homebrew` 접두어다.** Intel Mac의 `/usr/local`과 다르다는 사실을 머리에 박아두자.
- **`gcc`라는 명령은 사실 Apple Clang이다.** 진짜 GCC를 부르려면 `gcc-14`처럼 버전을 명시한다.
- **`aarch64-elf` ≠ `aarch64-apple-darwin`이다.** 같은 ARM이지만 바이너리 포맷이 다르다. 베어메탈은 ELF, macOS는 Mach-O.
- **sanitizer 켠 `hello.c`가 통과하면 환경의 80%가 잡힌 것이다.** 자세한 활용은 9장에서.

환경이 갖춰졌다. 그렇다면 이제 우리는 어디서 코드를 쓸까? vi 시절의 손가락은 옛 기억 그대로지만, 모던 에디터와 IDE의 풍경은 그 사이에 한 세대 이상 바뀌었다. VS Code? Neovim? CLion? Zed? 다음 장에서는 그 후보들 사이에서 자기에게 맞는 자리를 함께 골라보자.
