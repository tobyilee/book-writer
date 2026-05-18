# C 재학습 — Apple Silicon에서 ARM Kernel까지 저술 계획

## 제목 후보

1. **다시, C — Apple Silicon에서 ARM 커널까지**
   - 톤: 회귀와 재발견의 감정. "다시"라는 부사가 독자의 과거 경험을 인정하고, 부제가 출발지(Mac)와 도착지(ARM 커널)를 한 줄로 약속한다.
   - 포지셔닝: 회상-여정형 종합 바이블. 입문자가 아니라 "한 번 떠났다 돌아온 사람"을 정확히 부른다.

2. **C, 두 번째 만남 — K&R 이후 30년, 자기 커널을 굽기까지**
   - 톤: 인문적·에세이 가까운 톤. K&R이라는 고유명사를 정면에 내걸어 책의 대상 독자(옛 C 경험자)를 노골적으로 호출한다.
   - 포지셔닝: 재학습 여정의 정서까지 챙기는 에세이형 기술서. "굽다"라는 동사가 베어메탈의 손맛을 암시한다.

3. **모던 C 바이블 — C23, Apple Silicon, ARM 베어메탈**
   - 톤: 카탈로그적·레퍼런스적. 부제가 책의 세 축을 정확히 나열해 "한 권으로 끝낸다"는 무게감을 약속한다.
   - 포지셔닝: 종합 레퍼런스로서의 묵직한 책상 위 한 권. 검색해서 찾아 펴는 책에 가깝다.

**추천: 1번 — 다시, C — Apple Silicon에서 ARM 커널까지**

이유는 셋이다. 첫째, 대상 독자가 "한 번 떠난 사람"이라는 사실이 모든 챕터의 어조를 결정한다. "재학습"이라는 단어를 입에 안 올리고도 "다시"라는 한 음절로 그 정서가 전달된다. 둘째, 부제가 출발 환경(Mac, Apple Silicon)과 도착 지점(ARM 커널)을 명시해 책의 범위에 대한 약속을 한 줄로 끝낸다. 셋째, 토비 문체의 청유형·동반자적 어조와 가장 잘 어울리는 호흡을 가진 제목이다. 2번은 너무 감성적이라 종합 바이블의 무게를 깎고, 3번은 정확하지만 차갑다. 1번은 둘 사이의 중간점에 있다.

---

## 책 특성

- **장르:** 기술서 (재학습용 종합 바이블 + 베어메탈 입문서의 하이브리드). 단순 입문서가 아니라 "다른 언어 전문가의 C 복귀 여정 가이드"라는 좁고 명확한 포지션을 노린다.
- **분량:** 약 290~330쪽, 한글 약 17만 5천~21만 자. 15장 구성. 챕터 평균 약 1만 1천~1만 3천 자 (약 18~22쪽). Ch12·Ch13처럼 코드 비중이 높은 챕터는 글자 수는 적어도 페이지는 두꺼워지고, Ch15(작별 챕터)는 6천 자로 가장 짧게 잡았다.
- **난이도:** 중상. 변수·반복문·함수 같은 1세대 프로그래밍 기초 설명은 일체 생략한다. Java/JS/Python 중 하나 이상에서 실무 경험이 있는 개발자를 가정하고, 그 멘탈 모델과 C의 거리를 좁히는 데 지면을 쏟는다.
- **독자 여정 (한 문장 요약):** "K&R 시절의 흐릿한 C 기억" → "2026년 표준의 지도" → "Apple Silicon 위 모던 개발 환경" → "포인터·UB·메모리·링커라는 C의 본질" → "Sanitizer·정적 분석·퍼징이라는 안전망" → "freestanding과 베어메탈의 다리" → "QEMU에서 첫 'Hello, ARM!'" → "Raspberry Pi 4에서 자기 손으로 부팅한 작은 커널".

| 단계 | 진입 상태 | 출구 상태 |
|------|----------|----------|
| Part I (Ch1~2) | "C를 다시 잡으면 뭘 잃었고 뭐가 변했는지 헷갈린다" | "2026년 C 지도가 손에 잡힌다. C17/C23 중 무엇을 고를지 결정한 상태" |
| Part II (Ch3~4) | "vi 시절 도구만 알고 모던 셋업이 막막하다" | "Apple Silicon에서 clang/lldb/CMake/IDE가 한 줄에 동작한다" |
| Part III (Ch5~7) | "포인터·UB가 다시 무섭다" | "다섯 개의 포인터 시나리오와 UB·strict aliasing의 함정을 손에 익혔다" |
| Part IV (Ch8~10) | "표준 라이브러리만으로 어디까지 가나" | "헤더·링커·sanitizer·퍼저·libc 한계를 일상 도구로 쓴다" |
| Part V (Ch11~15) | "베어메탈이 신비롭게 느껴진다" | "QEMU virt 보드와 Raspberry Pi 4에서 자기 커널이 부팅된다. 다음 걸음(인터럽트·MMU·태스크 스위치·시스템 콜)이 보인다" |

---

## 내러티브 아크

이 책은 다섯 막의 여정으로 짜여 있다. 각 막은 독자의 감정 상태를 한 단계씩 끌어올린다.

**1막 (Ch1~2) — 추억 되살리기.** 첫 장은 환영 인사다. "왜 지금 다시 C인가"라는 질문을 던지고, 독자가 자기 손에 K&R 책을 들고 있던 시절을 떠올리게 한다. 그러나 곧장 현실로 데려온다 — 그 시절의 C와 지금의 C는 다르다. Ch2에서 C89부터 C23까지의 표준 변천을 한 장의 지도로 정리하고, "어떤 표준을 골라야 하나"라는 실용적 질문에 답을 준다. 이 두 장이 끝나면 독자는 "내가 무엇을 잃었고 무엇이 변했는지" 알게 된다.

**2막 (Ch3~4) — 환경 재정비.** 이론은 잠시 미루고 손을 더럽힌다. Ch3에서 Apple Silicon Mac에 Xcode CLT, Homebrew, LLVM, GCC, 크로스 컴파일러, QEMU를 깐다 ("Day 0"). Ch4는 vi에서 모던 IDE로 갈아타는 이야기다. VS Code + clangd를 기본값으로 추천하되 Neovim·CLion·Zed를 각각 누구에게 어울리는지 솔직하게 평한다. 2막이 끝나면 독자는 `hello.c`를 sanitizer까지 켜서 빌드·실행할 수 있다.

**3막 (Ch5~7) — C의 본질 재점검.** 본격적인 학습 구간이다. Ch5는 멘탈 모델 전환(Java/Python의 GC·예외와 C의 거리)을 도입에서 짧게 박은 뒤, 포인터를 다섯 시나리오로 손에 다시 익힌다. Ch6는 메모리 관리 — 스택·힙·malloc/free·누수·이중 해제·use-after-free까지. Ch7은 가장 무서운 손님, UB와 strict aliasing — 그리고 베어메탈로 가는 다리인 `<stdint.h>` 고정폭 정수·비트 조작·엔디언을 한 절로 묶는다. "Java는 ArrayIndexOutOfBoundsException을 던지는데 C는 침묵한다"는 정서적 충격을 정직하게 다룬다. 3막이 끝나면 독자는 자기가 쓴 C 코드가 왜 갑자기 망가질 수 있는지 직관이 생기고, MMIO 레지스터 조작에 필요한 비트 손이 미리 풀려 있다.

**4막 (Ch8~10) — 도구와 한계.** 안전망을 만드는 구간이다. Ch8은 헤더·링커·빌드 사이클·ABI — 다른 언어 출신이 가장 낯설어하는 단계다(여기서 AArch64 ABI 다리를 미리 놓아 베어메탈 챕터의 부담을 줄인다). Ch9는 ASan/UBSan을 정점에 둔 빌드 매트릭스 챕터 — 정적 분석·포매터·libFuzzer는 그 정점을 보완하는 위성으로 배치한다. Ch10은 표준 라이브러리의 빈자리를 네 절(문자열 / 컨테이너 부재 / POSIX vs C 표준 / libc 이식성)로 직시한다. 4막이 끝나면 독자는 sanitizer가 잡은 버그를 일상적으로 보고, 자기 만든 동적 배열·해시맵의 한계를 알고, 함수 호출의 실제 메커니즘이 손에 잡힌다.

**5막 (Ch11~15) — 베어메탈로의 도약과 작별.** 이 책의 정점과 결말이다. Ch11은 호스트와 베어메탈의 차이 — freestanding 모드, `printf`가 없는 세계, 직접 부트스트랩을 짜는 의미를 한 챕터에 담는다. Ch12에서 QEMU virt 보드에 "hello, aarch64"를 찍는다 — 네 파일(`boot.S` + `kernel.c` + `linker.ld` + `Makefile`)이 어떻게 협력해서 첫 글자에 도달하는지 큰 그림을 잡는다. Ch13은 그 부팅을 한 줄씩 해부한다 — `boot.S`의 한 명령씩, 링커 스크립트의 한 섹션씩, `.bss` 클리어·스택 포인터·primary core 선택·AArch64 ABI까지. Ch14는 진짜 하드웨어 — Raspberry Pi 4 SD카드 부팅·UART 케이블·실제 시리얼 출력. Ch15는 짧은 작별 챕터로 다음 걸음(인터럽트·MMU·태스크 스위치·시스템 콜)으로의 길라잡이다.

이 다섯 막은 정서적으로도 일관된 아크를 이룬다 — "낯설다 → 정비됐다 → 떨린다 → 안전하다 → 해냈다". 챕터 사이에서 갑자기 난이도가 점프하지 않도록, 4막의 안전망이 5막의 위험한 영역(베어메탈)으로 가는 준비를 미리 끝낸다.

---

## 챕터 목록

### 1장. 다시 C를 만나기 전에 — 추억과 현재 사이

- **핵심 질문:** "왜 지금, 다시 C인가? 내가 K&R 시절에 알던 C와 지금의 C는 무엇이 같고 무엇이 다른가?"
- **주요 내용:**
  - 옛 C 경험자가 Java/JS/Python에 머무는 동안 C가 어떻게 진화했는지 — C99·C11·C23의 큰 변화를 5분 안에
  - "왜 지금 C인가" — OS·임베디드·인터프리터 런타임·게임 코어가 여전히 C인 현실, 그리고 ARM 커널 자작이라는 목표가 왜 C로 시작되는지
  - "Rust로 그냥 가지 그래" 질문에 대한 솔직한 답 — 양자택일이 아니라 기반과 도구의 관계
  - K&R 시대에 알던 것 중 지금도 유효한 것·이제 깨진 것 (예: `void f()`의 의미 변화, `realloc(ptr,0)` 등)
  - 이 책의 약속 — 15장 끝에 독자가 어디 서 있을지 (Raspberry Pi 4 부팅 화면과 다음 단계 4개 미리 보기)
- **예제 프로젝트:** `example/ch01-hello-2026/` — `hello.c` 한 파일과 `Makefile`. C89 스타일로 한 번, C23 스타일로 한 번 빌드해 두 결과를 비교한다 (`-std=c89`, `-std=c23 -Wall -Wextra`).
- **독자가 얻는 것:** "지금이 다시 시작할 때"라는 확신과 15장 여정의 지도.
- **예상 분량:** 약 1만 자 (16~18쪽).

### 2장. 표준의 미로 — C89에서 C23까지

- **핵심 질문:** "여덟 개의 C 표준 중 나는 어떤 것을 골라야 하는가? `-std=c17`과 `-std=c23` 중 무엇이 내 길인가?"
- **주요 내용:**
  - 표준 타임라인 (K&R → C89 → C99 → C11 → C17 → C23) — 핵심 추가 기능을 한 표로
  - C99의 변화 (`long long`, `<stdbool.h>`, VLA, `//` 주석), C11의 변화 (`_Generic`, atomics, threads), C23의 큰 변화 (`bool`/`true`/`false`/`nullptr` 키워드화, `typeof`, `_BitInt(N)`, `[[attribute]]`, `#embed`, `constexpr`)
  - C23 채택의 함정 — `realloc(ptr,0)` UB화, 빈 괄호 함수 선언 의미 변화
  - 실전 권장 — 신규 프로젝트는 `-std=c23 -Wall -Wextra -Wpedantic`, 의존 라이브러리는 C11/C17 가정
  - GNU 확장 (`-std=gnu23`)이 베어메탈에서 왜 사실상 표준인지 (인라인 어셈블리·`__attribute__`·linker script 조합)
- **예제 프로젝트:** `example/ch02-std-matrix/` — 같은 코드를 `-std=c89`, `-std=c99`, `-std=c11`, `-std=c17`, `-std=c23` 다섯 가지로 빌드하는 Makefile. C23 전용 기능 (`nullptr`, `_BitInt(8)`)을 쓰는 짧은 데모와 그것이 C17에서는 안 됨을 보여준다.
- **독자가 얻는 것:** 표준 지도와 "내 프로젝트의 `-std=` 한 줄"에 대한 결정.
- **예상 분량:** 약 1만 1천 자 (18~20쪽).

### 3장. Mac에서 C 개발하기 — Apple Silicon Day 0

- **핵심 질문:** "Apple Silicon Mac을 켜고 한 시간 안에 C 개발 환경이 완성되려면 무엇을 깔고 무엇을 PATH에 올려야 하는가?"
- **주요 내용:**
  - Xcode Command Line Tools — `xcode-select --install` 한 줄로 Apple Clang·lldb·make·git
  - Apple Clang vs Homebrew LLVM — 버전 격차, 어느 쪽을 기본값으로?
  - Homebrew 셋업과 `/opt/homebrew` 접두어 — Intel Mac과의 차이를 처음에 명시
  - 베어메탈 크로스 컴파일러 (`aarch64-elf-gcc`, `arm-none-eabi-gcc`)와 QEMU 설치 — Ch12 준비를 미리 끝낸다
  - `cc`·`clang`·`gcc`의 이름 함정 (Apple은 `gcc`도 사실 Clang) + PATH 정리 (`~/.zshrc`)
  - 정합성 점검: sanitizer 켠 `hello.c`가 빌드·실행되면 80% 통과 (sanitizer 자체 설명은 Ch9에서 본격)
- **예제 프로젝트:** `example/ch03-day0-setup/` — `check_env.sh` (clang·lldb·cmake·ninja·qemu·aarch64-elf-gcc 버전 일괄 출력)와 `hello.c` (`-fsanitize=address,undefined`로 빌드, Ch9에서 본격). `make check`로 환경 점검, `make run`으로 실행.
- **독자가 얻는 것:** 손에 잡히는 환경. 다음 챕터부터 모든 예제가 빌드된다는 확신.
- **예상 분량:** 약 1만 2천 자 (20쪽).

### 4장. vi를 떠나며 — 모던 에디터·IDE 고르기

- **핵심 질문:** "20년 전 vi 시절에 멈춰 있던 손은 이제 어디로 가야 하는가? VS Code? Neovim? CLion? Zed?"
- **주요 내용:**
  - 후보 6종 비교 (VS Code + clangd, CLion, Xcode, Neovim, Zed, Cursor) — 각각 누구에게 맞는지 솔직한 평
  - 결론을 먼저: VS Code + clangd가 입문 재시작용 표준값
  - VS Code + clangd 셋업 완전 가이드 (clangd, CodeLLDB, CMake Tools, MS C/C++ 익스텐션과의 충돌 회피)
  - `compile_commands.json`을 생성하는 CMake 한 줄 (`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`)
  - Neovim 분기 — vi 근육 기억을 살리고 싶은 독자를 위한 짧은 안내 (clangd LSP·DAP)
  - 디버거 셋업 — lldb 기본 (`break set -n main`, `step`, `print`)
- **예제 프로젝트:** `example/ch04-editor-setup/` — 작은 CMake 프로젝트 (`main.c` + `util.c` + `util.h`). `compile_commands.json`이 자동 생성되고, `.vscode/launch.json`이 lldb로 디버깅을 띄우는 템플릿. Neovim 사용자용 `.lazy.lua` 스니펫도 함께.
- **독자가 얻는 것:** 자기에게 맞는 에디터와 LSP·디버깅이 동작하는 프로젝트 템플릿.
- **예상 분량:** 약 1만 자 (16~18쪽).

### 5장. 포인터를 다시 마주하다 — 메모리의 별명

- **핵심 질문:** "Java의 객체 참조와 C의 포인터는 무엇이 같고 무엇이 다른가? 흐릿한 포인터 기억을 어떻게 다섯 시나리오로 되살릴까?"
- **주요 내용:**
  - **(도입부) 멘탈 모델 전환 — Java/Python의 거리.** 1~2쪽 분량으로 이 챕터의 문턱에 짧은 다리를 놓는다. Java의 GC·`NullPointerException`·`try/catch`, Python의 reference counting·`KeyError`가 C에는 없다는 사실을 7행 비교 표로 정면에 둔다. "C는 침묵한다"는 본 책의 정서적 닻을 여기서 처음 명시적으로 박는다. 레퍼런스 §8(멘탈 모델 전환)의 핵심을 흡수.
  - 변수는 메모리 셀의 별명, 그 셀에는 주소가 있다 — C의 메모리 모델 한 그림
  - 다섯 시나리오로 익히는 포인터: (1) 주소 출력 (2) 포인터로 값 바꾸기 (3) 함수 인자 out 파라미터 (4) 동적 할당 (5) 포인터의 포인터
  - 배열과 포인터의 관계 — `arr[i]`가 `*(arr+i)`인 이유, `sizeof arr`이 함수에 넘기면 왜 망가지는지
  - 함수 포인터 — Java의 람다·Python의 first-class function과의 정신적 거리
  - `const`의 위치 함정 (`const int *p` vs `int * const p` vs `const int * const p`)
- **예제 프로젝트:** `example/ch05-pointer-five/` — 다섯 시나리오 각각의 독립 실행 파일 (`scene1_address`, `scene2_via_pointer`, ... , `scene5_pointer_to_pointer`). 함수 포인터 콜백 데모와 `const` 위치 차이 컴파일 에러 데모도 포함.
- **독자가 얻는 것:** "Java/Python 멘탈 모델에서 C 멘탈 모델로 자리를 옮겼다"는 자각 + "포인터가 다시 자연스러워졌다"는 감각.
- **예상 분량:** 약 1만 4천 자 (24쪽 — 도입부 멘탈 모델 절을 흡수해 1천 자 증가).

### 6장. 메모리 관리 — 직접 사 와서 직접 돌려준다

- **핵심 질문:** "GC가 없는 세계에서 누수·이중 해제·use-after-free는 어떻게 피하는가? 누가 free 할 책임을 어떻게 약속하는가?"
- **주요 내용:**
  - 스택 vs 힙 — 자동 변수의 수명, 함수가 끝나면 사라지는 것, `malloc`으로 얻은 것의 수명
  - `malloc`/`calloc`/`realloc`/`free` 사용 패턴과 `realloc(ptr, 0)`의 C23 함정 (Ch2와 연결)
  - 누수, 이중 해제, use-after-free — 세 가지 통증을 코드로 보고 sanitizer로 잡기 (Ch9에서 본격)
  - 소유권 명시 컨벤션 — `_create`/`_destroy` 페어, `_borrow`/`_owned` 주석, 함수 시그니처의 약속
  - `goto cleanup;` 단일 출구 — 안티패턴이 아니라 정석 관용구라는 점
  - `__attribute__((cleanup))` (GNU 확장) — RAII 비슷한 감각을 C에서
- **예제 프로젝트:** `example/ch06-memory/` — 동적 배열(`vec_t`) 구현 `vec.c`·`vec.h`와 그것을 쓰는 `main.c`. 일부러 누수 있는 버전 `vec_leaky.c`와 고친 버전 `vec_fixed.c`를 함께 두고 Makefile에서 `make leak`(ASan으로 누수 잡기, Ch9에서 본격)/`make fixed`로 비교.
- **독자가 얻는 것:** 메모리 약속을 코드 수준에서 표현하는 습관.
- **예상 분량:** 약 1만 3천 자 (22쪽).

### 7장. 정의되지 않은 동작 — C가 너를 어떻게 배신하는가

- **핵심 질문:** "왜 컴파일러는 내 코드를 통째로 지워버릴 수 있는가? UB와 strict aliasing은 무엇이고, 어떻게 피하는가? 비트 폭과 엔디언은 어디서 함정이 되는가?"
- **주요 내용:**
  - UB의 정의와 컴파일러의 자유 — "이 경로는 실행될 수 없다고 가정"의 무서움
  - 자주 부딪히는 UB 카탈로그: 정수 오버플로(signed), NULL 역참조, 배열 경계 밖 접근, 초기화 안 된 변수 읽기, `volatile` 누락
  - Strict Aliasing — 한 객체를 호환 타입이나 `char` 계열로만 접근, `int*`→`float*` 캐스트 역참조는 금지
  - 안전한 비트 재해석 — `memcpy` 패턴, C23의 `<stdbit.h>` 활용
  - **고정폭 정수와 비트 조작 — `<stdint.h>`, 시프트, 마스크, 엔디언.** 4~5쪽 분량의 한 절. K&R 시절의 `int`/`long` 가정이 64비트에서 어떻게 깨졌는지(레퍼런스 §8.3) → `<stdint.h>`의 `uint8_t`/`uint16_t`/`uint32_t`/`uint64_t`가 모던 C의 기본값인 이유. signed overflow는 UB지만 unsigned는 wrap이 정의된다는 비대칭. 비트 마스크·시프트 관용구(`reg |= (1u << 7)`, `(val >> 12) & 0xFFFu`). 엔디언 검사 (`__BYTE_ORDER__`)와 `__builtin_bswap32`/`htonl`. **이 절이 Ch12 MMIO 레지스터 비트 조작과 Ch13 부팅 코드 어셈블리 읽기에 직접 다리를 놓는다.**
  - `-fno-strict-aliasing`이 진통제일 뿐인 이유 (리눅스 커널이 쓰는 이유 포함)
  - "Java 출신이 가장 충격받는 순간" — UB는 경고도 안 뜬다
- **예제 프로젝트:** `example/ch07-ub-zoo/` — UB 표본실. `signed_overflow.c`, `null_deref.c`, `oob_read.c`, `aliasing_int_float.c`, `volatile_missing.c` 다섯 개. 각 파일이 어떻게 깨지는지 sanitizer로 잡아 보이는 Makefile (`make safe`로 sanitizer 켜고 (Ch9에서 본격), `make unsafe`로 끄고 비교). **추가로 `bits_demo/` 하위에 고정폭 정수·시프트·마스크·엔디언 검사 데모(`bit_field.c`, `endian_probe.c`).**
- **독자가 얻는 것:** UB에 대한 두려움이 아니라 도구로 잡을 수 있다는 자신감 (Ch9에서 본격) + 비트 폭과 엔디언이 손에 잡히는 감각 (Ch12 MMIO의 사전 준비).
- **예상 분량:** 약 1만 4천 자 (24쪽 — 비트 조작 절을 흡수해 1천 자 증가).

### 8장. 헤더와 링커 — 컴파일 사이클을 다시 이해하기

- **핵심 질문:** "`.c`가 어떻게 `.o`가 되고, 어떻게 한 실행파일로 묶이는가? Python·Java 출신에게 가장 낯선 단계는 무엇인가? 그리고 함수 호출이 실제로 어떻게 일어나는가?"
- **주요 내용:**
  - 전처리 → 컴파일 → 어셈블 → 링크 — 네 단계와 각 단계의 산물 (`.i`/`.s`/`.o`/실행파일)
  - `#include`는 텍스트 치환 — 이중 포함 방지 (`#ifndef`/`#define`/`#endif`, `#pragma once`)
  - 선언 vs 정의 — 헤더에는 선언, `.c`에는 정의. `extern`의 의미, `static`의 두 얼굴 (파일 스코프 vs 함수 내 영속 변수)
  - 정적 라이브러리(`.a`)와 동적 라이브러리(`.dylib`/`.so`) — Mac의 `.dylib` 사정
  - 빌드 시스템 사다리 — Make → CMake → Ninja, Meson의 위치, IDE 친화성
  - **함수 호출의 실제 — ABI와 calling convention.** 2~3쪽 분량의 한 절. 스택 프레임이 어떻게 쌓이고, 인수가 어디에 실리고, 리턴 주소가 어디 보관되는지를 한 그림으로. x86-64 System V와 AArch64 PCS(Procedure Call Standard) 두 ABI의 인수 전달 레지스터를 정면 비교 (X0~X7로 처음 8개 정수/포인터 인수, X8 indirect result, X29 frame pointer, X30 link register). `objdump -d`로 hello 함수의 프롤로그·에필로그를 한 명령씩 읽기. **이 절이 Ch12·Ch13에서 X0~X7이 갑자기 튀어나오지 않게 미리 다리를 놓는다.**
  - `compile_commands.json` — clangd·정적 분석 도구의 공통 진입점 (Ch4·Ch9와 연결)
- **예제 프로젝트:** `example/ch08-build-cycle/` — 같은 코드를 (a) 단일 `.c` 한 줄 빌드, (b) Makefile로 다중 `.c` 분할 빌드, (c) CMake로 정적 라이브러리 + 실행 파일 분리 빌드 세 방식으로 보여주는 디렉토리. 각 단계 산물 (`.i`/`.s`/`.o`)을 남기는 `make stages` 타깃. **추가로 `abi_peek/` 하위에 인수 6개·8개·9개를 받는 함수를 `objdump -d`로 디스어셈블해 X0~X7 사용과 스택 인수 폴백을 보이는 작은 데모.**
- **독자가 얻는 것:** 빌드 에러 메시지를 읽을 줄 아는 눈 + 함수 호출의 실제 메커니즘에 대한 손 감각 (Ch11·Ch12·Ch13의 사전 준비).
- **예상 분량:** 약 1만 3천 자 (22쪽 — ABI 절을 흡수해 1천 자 증가).

### 9장. 안전망 — Sanitizer를 중심에 둔 빌드 매트릭스

- **핵심 질문:** "C가 침묵해 버리는 버그를 도구가 어떻게 잡아 주는가? 일상 개발 빌드에 무엇을 켜 두어야 하는가? 그리고 ASan/UBSan을 왜 책의 안전망 중심에 두는가?"
- **구성 원칙:** 도구 10개를 균등하게 다루지 않는다. **ASan과 UBSan을 정점에 두고, 나머지 도구는 그 정점을 보완하는 위성으로 배치하는 "빌드 매트릭스" 중심 챕터.** 독자가 챕터를 덮으면 "어떤 빌드에서 무엇을 켜는가"라는 매트릭스가 머릿속에 박힌다.
- **주요 내용 (절 구조):**
  - **§1. 정점 — ASan + UBSan (5~6쪽).** 책 전체 예제 빌드의 기본값. 잡는 버그 카탈로그(heap/stack/global buffer overflow, use-after-free/return/scope, signed overflow, NULL 역참조, alignment 위반), 오버헤드(2~3배 메모리·1.5~2배 속도), `-fsanitize=address,undefined -fno-omit-frame-pointer -g` 정합 옵션 묶음, 환경 변수(`ASAN_OPTIONS=detect_leaks=1`)와 `__asan_default_options`. Ch6·Ch7 버그를 실제로 잡는 워크플로 두 개를 끝까지 따라간다.
  - **§2. 정점의 형제들 — TSan과 MSan (1~2쪽).** TSan은 멀티스레드 코드에서, MSan은 macOS에서 제한적이라는 사실을 짧게. 본 책 범위에서 본격 사용하지 않는다고 명시.
  - **§3. macOS에서 valgrind 부재라는 빈자리 (1쪽).** sanitizer + `leaks --atExit` + Instruments 세 갈래로 메우는 법.
  - **§4. 정적 분석 비교 표 — clang-tidy·scan-build·cppcheck·GCC `-fanalyzer` (3~4쪽).** 한 테이블로 정리: 무엇을 잡는가, 어떤 빌드에 끼울 수 있는가, false positive 성향, CI 통합 난이도. clang-tidy `cert-*`/`bugprone-*` 카테고리 시연(MISRA·CERT 짧은 박스 1쪽 포함). 워크플로 두 개를 끝까지 — (a) Pre-commit hook에서 clang-tidy, (b) CI에서 scan-build 리포트.
  - **§5. clang-format으로 스타일 일원화 (반쪽).** `.clang-format` 프리셋(LLVM/Google/자가 정의)을 짧게.
  - **§6. libFuzzer 미니 튜토리얼 (2~3쪽).** `-fsanitize=fuzzer,address` 한 줄로 시작 → fuzz target 작성 → corpus 디렉토리 만들기 → 크래시 재현 → coverage 시각화. ASan과 결합되는 이유를 다시 짚는다.
  - **§7. 권장 빌드 매트릭스 (2~3쪽).** 본 책의 모든 예제가 따르는 5열 매트릭스 한 표 — Debug-ASan(개발), Debug-UBSan(개발), Release(`-O2 -DNDEBUG`), CI-Static(scan-build + clang-tidy), Bare-metal(`-ffreestanding`, sanitizer 끔, Ch11 예고). CMake와 Make 양쪽 템플릿 제시.
- **예제 프로젝트:** `example/ch09-safety-net/` — Ch6·Ch7의 버그 있는 코드를 위 빌드 매트릭스 5열로 도는 통합 디렉토리. `make asan`, `make ubsan`, `make release`, `make tidy`, `make scan`, `make fuzz` 타깃. `.clang-format`·`.clang-tidy` 설정과 `Makefile.matrix`(5열 한 번에 도는 메타 타깃). libFuzzer 시연은 `fuzz/` 하위에 fuzz target + seed corpus.
- **독자가 얻는 것:** "ASan + UBSan을 켜는 게 책의 기본값"이라는 머슬 메모리 + "어떤 빌드에 어떤 도구를 끼우는가"라는 매트릭스 시각.
- **예상 분량:** 약 1만 6천 자 (28쪽 — 빌드 매트릭스 중심 재구성으로 4천 자 증가). 분량 흡수원: Ch15 슬림화(8천 → 6천 자, -2천)와 Ch1·Ch10의 자연 증분으로 매트릭스 전체 균형 유지.

### 10장. 표준 라이브러리의 빈자리 — string·io·container 한계와 대안

- **핵심 질문:** "C 표준 라이브러리에 왜 List·Map·정규식·네트워킹이 없는가? 그 빈 자리를 무엇으로 메워야 하는가?"
- **구성 원칙:** 산만함을 피하기 위해 네 절로 명확히 분리한다 — **문자열의 한계 / 컨테이너 부재 / POSIX vs C 표준 / libc 이식성**. 각 절이 독립된 문제 정의·정석·예제·다음 걸음을 갖는다.
- **주요 내용 (절 구조):**
  - **§1. 문자열의 한계 (4~5쪽).** C 표준 라이브러리의 의도된 작음을 한 문단으로 짚고 시작. NUL 종결 문자열의 진실 — `strlen` O(n), `strcpy` 버퍼 오버플로, `strncpy`/`snprintf`/`strlcpy`/`memccpy` 정석. C23의 안전 보강 — `memset_explicit`, `strdup`, `<stdckdint.h>` checked arithmetic. 함정 데모: `strncpy` non-NUL termination이 어떻게 사고로 이어지는가.
  - **§2. 컨테이너 부재 — 자작 패턴 (3~4쪽).** `vec`(동적 배열) 한 스케치(capacity 두 배 증가, `realloc` 실패 처리). `map`(해시테이블, FNV-1a + open addressing) 한 스케치. 매크로 기반 제네릭 컨테이너의 가능성과 함정.
  - **§3. POSIX vs C 표준 — 의존성 사다리 (2~3쪽).** 표준 라이브러리만으로 갈 곳, POSIX(`sys/socket.h`·`pthread.h`·`fork`)로 갈 곳, 외부 라이브러리(uthash·sds·libcurl)로 갈 곳. Mac은 BSD 계열 POSIX, 리눅스는 GNU 확장이 더 풍부하다는 점.
  - **§4. libc 구현체 차이 — 이식성 부담 (2~3쪽).** GNU libc·musl·Apple libSystem이 미묘하게 다른 이유. `strlcpy`/`strlcat`이 어디는 있고 어디는 없는 사정. `_GNU_SOURCE`·`_POSIX_C_SOURCE` 매크로의 의미. CI에서 두 플랫폼을 모두 도는 전략 한 가지.
- **예제 프로젝트:** `example/ch10-libc-gap/` — 안전한 문자열 처리 미니 라이브러리 (`safestr.c`/`safestr.h` — `safestr_copy`, `safestr_concat`, `safestr_format`)와 해시맵 미니 구현 (`map.c`/`map.h`). 단위 테스트는 직접 짠 간단한 `assert` 기반 러너. 함정 데모(`strncpy` non-NUL termination, signed overflow). **§4용으로 `portability/` 하위에 `strlcpy` polyfill과 `_POSIX_C_SOURCE` 매크로 데모.**
- **독자가 얻는 것:** "표준 라이브러리만으로 어디까지 가는지" 손에 잡히는 감각 + 자작 도구 패턴 + 이식성 함정의 지도.
- **예상 분량:** 약 1만 3천 자 (22쪽 — 절 구조 명확화로 1천 자 자연 증가).

### 11장. 베어메탈로 가는 다리 — Freestanding C와 호스트 없는 세계

- **핵심 질문:** "호스트 OS가 없는 환경에서 C는 무엇을 잃고, 무엇이 남는가? `-ffreestanding`의 의미는?"
- **주요 내용:**
  - Hosted vs Freestanding — C 표준이 정의하는 두 환경, `main()`이 진입점이 아닐 수도 있다는 의미
  - Freestanding에서 안전한 헤더만 골라 쓰기 — `<stddef.h>`, `<stdint.h>`, `<stdbool.h>`, `<limits.h>`, `<float.h>`, `<stdarg.h>`, `<iso646.h>`
  - 표준 라이브러리 없음 → `printf` 없음, `malloc` 없음, `errno` 없음 — 다 직접
  - 런타임 초기화의 책임 — `.bss` 클리어, `.data` 복사, 스택 포인터 초기화는 누가?
  - 컴파일러 옵션 — `-ffreestanding -nostdlib -nostartfiles -mgeneral-regs-only`
  - 베어메탈에서 sanitizer(Ch9에서 본격)가 왜 안 통하는지 — 런타임이 libc 의존이기 때문. 호스트 측 단위 테스트 전략으로 우회
  - C++을 사실상 못 쓰는 이유 — `new`/`delete`/RTTI/예외가 런타임 요구
- **예제 프로젝트:** `example/ch11-freestanding/` — 호스트에서 `-ffreestanding -nostdlib`로 빌드되는 짧은 `tiny.c` (자체 `mini_strlen`·`mini_memcpy`·`mini_putc` 구현). `_start` 진입점을 직접 정의해 `main` 없이 실행되는 데모(macOS는 어렵지만 Linux/QEMU에서는 가능 — 책에서는 베어메탈 ARM 빌드로 검증). Ch12의 골격 미리보기.
- **독자가 얻는 것:** "호스트 없는 세계에 들어갈 준비" — Ch12 첫 부팅 직전의 마음가짐.
- **예상 분량:** 약 1만 1천 자 (18쪽).

### 12장. 첫 AArch64 커널 — QEMU에서 "Hello, ARM!"

- **핵심 질문:** "내가 짠 코드가 호스트 OS 없이 CPU 위에서 직접 도는 첫 순간을 어떻게 만들어내는가? 네 개의 파일(`boot.S` + `kernel.c` + `linker.ld` + `Makefile`)이 어떻게 협력해서 첫 글자에 도달하는가?"
- **챕터 약속 (Ch13과의 명시적 분리):** **Ch12는 "큰 그림 — 네 파일이 첫 글자에 어떻게 도달하는가". Ch13은 "한 줄씩 해부 — 왜 그렇게 짰는가".** 같은 코드 베이스를 두 번 보지만, Ch12는 동작하는 그림을 손에 넣는 게 목적이라 모든 줄을 설명하지 않는다. 큰 구조와 데이터 흐름만 짚고, 한 명령씩 들어가는 깊이는 Ch13에 약속한다. 이 분리를 챕터 도입에서도 독자에게 명시한다.
- **주요 내용:**
  - 목표: QEMU `-M virt -cpu cortex-a72`에 `kernel.elf`를 올려 시리얼에 `hello, aarch64` 출력
  - **네 파일 큰 그림 한 장 — `boot.S`(진입과 스택 설정) → `kernel.c`(`uart_putc`로 글자 보내기) → `linker.ld`(섹션 배치) → `Makefile`(빌드 흐름). 데이터 흐름을 한 그림으로.**
  - PL011 UART의 MMIO 주소 (`0x09000000`)와 `volatile` 포인터로 한 글자 보내기 (Ch7의 고정폭 정수·비트 조작 절을 다시 호출)
  - 최소 `kernel.c` 작성 — `uart_putc`/`uart_puts`/`kernel_main` (코드 보여주되 모든 줄 설명은 Ch13에)
  - 최소 `boot.S` 작성 — `_start` 진입점, primary core 선택, 스택 포인터 설정, `kernel_main` 호출 (구조만, 명령별 해부는 Ch13)
  - 최소 `linker.ld` — `.text.boot` 맨 앞에 두는 이유 (한 문단)
  - `aarch64-elf-gcc`로 빌드, QEMU 실행, 시리얼에 글자가 나오는 순간 — **"이 한 줄이 통과하면 이 책의 7할이 완성된다"는 정점.**
- **예제 프로젝트:** `example/ch12-hello-aarch64/` — `boot.S`, `kernel.c`, `linker.ld`, `Makefile`. `make`로 `kernel.elf` 생성, `make run`이 `qemu-system-aarch64 -M virt -cpu cortex-a72 -nographic -kernel kernel.elf` 실행. `make debug`는 QEMU `-s -S`로 띄우고 lldb 원격 디버깅 (gdb 호환 프로토콜) 가이드. 레퍼런스 §7.5 골격을 그대로 빌드 가능한 형태로.
- **독자가 얻는 것:** **이 책 최대의 보상 — 내 코드가 OS 없이 ARM CPU 위에서 직접 동작하는 첫 경험.** 동작은 손에 잡혔으니, 다음 챕터에서 한 줄씩 들어갈 마음의 준비.
- **예상 분량:** 약 1만 3천 자 (22쪽, 코드 비중 큼 — Ch13에 한 줄 해부를 양보해 1천 자 감소).

### 13장. 부트 흐름 해부 — `startup.S`부터 `main`까지

- **핵심 질문:** "Ch12에서 글자가 화면에 찍히기까지 그 짧은 시간에 무슨 일이 벌어졌는가? `boot.S`의 한 줄, 링커 스크립트의 한 섹션을 모두 설명할 수 있는가?"
- **챕터 약속 (Ch12와의 명시적 분리):** **Ch12에서 본 코드를 이번에는 한 줄씩, 한 섹션씩 해부한다.** "왜 이 명령이 여기에 있는가", "왜 링커 스크립트가 이 섹션을 맨 앞에 두는가"에 답한다. Ch12가 동작이라면 Ch13은 이유.
- **주요 내용:**
  - AArch64 부팅 직후의 CPU 상태 — Exception Level (EL2/EL1), 캐시·MMU 비활성, 모든 일반 레지스터 미정의
  - `mpidr_el1`의 비트 의미 — primary core를 어떻게 골라내는가 (Ch7의 비트 조작 절이 여기서 직접 쓰인다)
  - `.bss` 0 클리어와 `.data` 복사 — 왜 필요한가, 어디서 해야 하는가
  - 스택 포인터 초기화 — `stack_top` 심볼이 메모리 어디에 위치하는지를 링커 스크립트에서 정해 준다
  - 링커 스크립트 깊게 — `ENTRY`, `SECTIONS`, `KEEP`, VMA vs LMA, 정렬 (`. = ALIGN(8)`)
  - `objdump -d kernel.elf`로 만든 ELF를 한 명령씩 읽어 보기
  - AArch64 ABI 함수 호출 규약 — X0~X7 인수, X29 frame pointer, X30 link register, 어셈블리에서 C로 콜할 때 (Ch8 ABI 절을 여기서 다시 호출 — 호스트 측 ABI 직관이 베어메탈에서 어떻게 그대로 쓰이는지)
  - EL2 → EL1 전환 코드 (필요한 경우)
- **예제 프로젝트:** `example/ch13-boot-anatomy/` — Ch12의 `boot.S`를 (1) 가장 단순한 버전, (2) `.bss` 클리어 추가 버전, (3) EL2 → EL1 전환 추가 버전 세 단계로 분할. 각 단계가 빌드되고 동작함을 확인 (`make stage1`, `make stage2`, `make stage3`). `objdump -d`/`readelf -a` 출력 비교 스크립트도 포함.
- **독자가 얻는 것:** 부팅 코드의 각 줄을 설명할 수 있는 자신감.
- **예상 분량:** 약 1만 3천 자 (22쪽 — Ch12에서 양보받은 한 줄 해부를 흡수해 1천 자 증가).

### 14장. 진짜 ARM — Raspberry Pi 4에서 부팅하기

- **핵심 질문:** "QEMU에서 동작한 커널을 진짜 Raspberry Pi 4 보드에서 부팅하려면 무엇이 바뀌어야 하는가?"
- **주요 내용:**
  - Raspberry Pi 4 부트 흐름 — GPU 펌웨어가 `config.txt`/`kernel8.img` 읽기, 메모리 0 (또는 0x80000)에 적재, primary core가 점프
  - QEMU `-M raspi4b` vs 실제 보드 — 9.0 이후 QEMU의 `raspi4b` 머신, 그러나 GPU·일부 주변 장치 차이
  - Mini UART (BCM2711의 GPIO14/15) — PL011과 다른 주소·다른 초기화 절차
  - SD카드 부팅 워크플로 — `bootcode.bin`·`start4.elf`·`fixup4.dat`·`config.txt` 구성, `kernel8.img` 위치
  - UART-USB 어댑터로 PC 시리얼 모니터 (`screen /dev/cu.usbserial-XXXX 115200` 또는 `minicom`)
  - 디버그 시 차이 — QEMU에서 동작하던 코드가 실제 보드에서 멈춘다면 어디부터 보는가
- **예제 프로젝트:** `example/ch14-raspi4-bootkit/` — Ch12 코드를 Pi 4 보드에 맞게 조정 (`boot_raspi.S`, `kernel_raspi.c`, `linker_raspi.ld`, `config.txt`). `make qemu`는 QEMU `raspi4b`로 검증, `make image`는 SD카드 이미지(`.img`)를 만들어 `dd`로 굽는 명령 가이드. 인쇄용 PDF 핀배치도 첨부.
- **독자가 얻는 것:** **두 번째 정점 — 손에 잡히는 보드 위에서 자기 코드가 부팅한다.**
- **예상 분량:** 약 1만 3천 자 (22쪽).

### 15장. 다음 걸음 — 인터럽트·MMU·태스크 스위치로 가는 길

- **핵심 질문:** "Hello를 찍었으니, 진짜 OS로 가려면 다음에 무엇을 배워야 하는가?"
- **구성 원칙:** 슬림한 작별 챕터. 8개 토픽을 펑펑 뿌리지 않는다. **다음 단계 4개에 집중하고, 나머지는 마지막 짧은 절에 묶어 노출만 한다.** 책을 덮는 정서를 가져가는 게 우선.
- **주요 내용 (절 구조):**
  - **§1. 다음 단계 4개 — 한 토픽당 약 1쪽씩, 총 4~5쪽 (3천 자 분량).** ① 인터럽트 벡터 테이블·타이머 인터럽트(왜 필요한가 = 멀티태스킹의 출발) ② MMU 페이지 테이블(왜 필요한가 = 프로세스 격리) ③ 컨텍스트 스위치(왜 필요한가 = 동시 실행) ④ 자기 시스템 콜 인터페이스(왜 필요한가 = 사용자 공간과의 경계). 각 단계마다 "어디서 시작하는가" 한 줄 — s-matyukevich raspberry-pi-os lesson 2~7, OSDev wiki, Memfault Interrupt 블로그.
  - **§2. 책에서 못 다룬 영역 — 한 절로 묶기 (1쪽, 1천 자).** 동시성(atomics·메모리 배리어), SIMD/NEON, 디바이스 드라이버, 보안(TrustZone)을 한 문단씩 노출만. 깊이는 다음 책의 몫.
  - **§3. Rust로의 다리 (반쪽, 500자).** `#![no_std]`·`embedded-hal`·`tock OS` 한 줄. C로 만든 같은 일을 Rust로 해보는 것의 의미.
  - **§4. 작가의 권유 (반쪽, 500자).** "여기서 멈춰도 충분히 멀리 왔다. 그러나 계속 가도 좋다" — 책을 덮는 정서적 결말.
- **예제 프로젝트:** `example/ch15-next-steps/` — 인터럽트 벡터 테이블 골격(`vectors.S`)과 타이머 인터럽트 핸들러 한 줄짜리 데모. "다음 책을 위한 스타터 키트". 빌드는 되지만 동작은 학습 과제로 남김.
- **독자가 얻는 것:** "이 책 다음은 어디로?"에 대한 분명한 지도(다음 단계 4개). 책을 덮는 차분한 정서적 마무리.
- **예상 분량:** 약 6천 자 (10~12쪽 — 8천 자에서 슬림화). 절약한 2천 자는 Ch9 보강에 흡수.

---

## 챕터 간 흐름 (한 줄씩)

- Ch1 → Ch2: "내가 알던 C는 변했다"고 인정했으니, 무엇이 변했는지 표준 지도로 본다.
- Ch2 → Ch3: 표준을 정했으니, 그것을 빌드할 도구를 깐다.
- Ch3 → Ch4: 컴파일러는 준비됐으니, 코드를 쓸 에디터를 고른다.
- Ch4 → Ch5: 환경이 갖춰졌으니, Java/Python 멘탈 모델에서 C 멘탈 모델로 자리를 옮기고(Ch5 도입부), 첫째 본질 — 포인터 — 를 다시 익힌다.
- Ch5 → Ch6: 포인터가 손에 들어왔으니, 그 끝에 매달린 메모리를 다룬다.
- Ch6 → Ch7: 메모리를 다뤘으니, 그 다룸이 무너지는 곳 — UB — 와 베어메탈로 가는 다리 — 비트 폭·엔디언 — 를 정면으로 본다.
- Ch7 → Ch8: 코드의 의미와 비트를 다뤘으니, 코드가 실행파일로 묶이는 빌드 사이클과 함수 호출의 실제(ABI)를 본다.
- Ch8 → Ch9: 빌드를 알았으니, 그 빌드에 안전망을 짠다.
- Ch9 → Ch10: 도구로 잡을 수 있게 됐으니, C 표준 라이브러리가 어디까지인지 그 한계를 만난다.
- Ch10 → Ch11: 표준 라이브러리의 빈자리를 봤으니, 표준 라이브러리 자체가 없는 freestanding 세계로 발을 옮긴다.
- Ch11 → Ch12: 마음의 준비가 끝났으니, QEMU에서 첫 "hello"를 찍는다 (네 파일이 어떻게 협력하는가 — 큰 그림).
- Ch12 → Ch13: 글자가 나왔으니, 그 짧은 순간을 한 줄씩, 한 섹션씩 해부한다 (왜 그렇게 짰는가).
- Ch13 → Ch14: 부팅 흐름을 이해했으니, 진짜 보드로 옮긴다.
- Ch14 → Ch15: 보드에서 부팅했으니, 그 다음 길을 본다.

이 흐름의 정서적 곡선은 — **1~2장의 안도(기억 정리), 3~4장의 정비감(환경 셋업), 5~7장의 긴장(본질 재대면 + 비트 손풀기), 8~10장의 통제감(도구 장착 + ABI), 11~14장의 떨림과 환호(베어메탈 첫 부팅), 15장의 차분한 작별**이다.

---

## example/ 프로젝트 구조 — 전체 그림

`example/` 폴더는 책과 함께 배포되며, 15개 챕터의 모든 예제가 한 트리 안에서 빌드 가능하다.

```
example/
├── README.md                          # 전체 예제 사용법, 환경 요구사항 (Ch3 참조)
├── Makefile                           # 최상위. `make all`이 모든 챕터 예제 빌드
├── CMakeLists.txt                     # CMake 사용자용 — 호스트 챕터(Ch1~Ch10)만 묶어 빌드
├── ch01-hello-2026/                   # Ch1. C89 vs C23 동일 코드 비교
│   ├── hello.c
│   └── Makefile                       # `make c89`, `make c23` 두 타깃
├── ch02-std-matrix/                   # Ch2. -std=c89~c23 다섯 빌드 + C23 데모
│   ├── std_demo.c
│   ├── c23_only.c                     # nullptr, _BitInt(8) 등
│   └── Makefile
├── ch03-day0-setup/                   # Ch3. 환경 점검 + hello sanitized
│   ├── check_env.sh
│   ├── hello.c
│   └── Makefile                       # `make check`, `make run`
├── ch04-editor-setup/                 # Ch4. clangd·lldb 템플릿 CMake 프로젝트
│   ├── CMakeLists.txt
│   ├── src/main.c
│   ├── src/util.c
│   ├── include/util.h
│   ├── .vscode/launch.json
│   └── .vscode/settings.json
├── ch05-pointer-five/                 # Ch5. 다섯 시나리오 독립 실행 파일
│   ├── scene1_address.c
│   ├── scene2_via_pointer.c
│   ├── scene3_out_param.c
│   ├── scene4_malloc.c
│   ├── scene5_ptr_to_ptr.c
│   ├── func_ptr_callback.c
│   └── Makefile
├── ch06-memory/                       # Ch6. vec_t 누수/수정 버전 비교
│   ├── vec.h
│   ├── vec_leaky.c
│   ├── vec_fixed.c
│   ├── main.c
│   └── Makefile                       # `make leak`, `make fixed`
├── ch07-ub-zoo/                       # Ch7. UB 표본실 5종
│   ├── signed_overflow.c
│   ├── null_deref.c
│   ├── oob_read.c
│   ├── aliasing_int_float.c
│   ├── volatile_missing.c
│   └── Makefile                       # `make safe`, `make unsafe`
├── ch08-build-cycle/                  # Ch8. 단일/Make/CMake 세 방식
│   ├── one_liner.c
│   ├── multi/...                      # 다중 .c + Makefile
│   ├── cmake_lib/CMakeLists.txt       # 정적 라이브러리 분리
│   └── Makefile                       # `make stages`로 .i/.s/.o 산물 남기기
├── ch09-safety-net/                   # Ch9. ASan/UBSan/tidy/scan/fuzz
│   ├── buggy.c
│   ├── fuzz_target.c
│   ├── .clang-format
│   ├── .clang-tidy
│   └── Makefile                       # asan/ubsan/tidy/scan/fuzz 다섯 타깃
├── ch10-libc-gap/                     # Ch10. safestr + map 미니 라이브러리
│   ├── safestr.h
│   ├── safestr.c
│   ├── map.h
│   ├── map.c
│   ├── test_safestr.c
│   ├── test_map.c
│   └── Makefile                       # `make test`로 전체 테스트
├── ch11-freestanding/                 # Ch11. 호스트 + freestanding 빌드
│   ├── tiny.c                         # mini_strlen, mini_memcpy
│   ├── tiny_start.S                   # _start 진입점
│   └── Makefile                       # host/freestanding 빌드 비교
├── ch12-hello-aarch64/                # Ch12. 정점 — QEMU virt 첫 부팅
│   ├── boot.S
│   ├── kernel.c
│   ├── linker.ld
│   └── Makefile                       # `make run`, `make debug`
├── ch13-boot-anatomy/                 # Ch13. 부팅 코드 3단계 분해
│   ├── stage1_minimal/...
│   ├── stage2_bss_init/...
│   ├── stage3_el_switch/...
│   └── Makefile                       # `make stage{1,2,3}`
├── ch14-raspi4-bootkit/               # Ch14. Raspberry Pi 4 실제 부팅
│   ├── boot_raspi.S
│   ├── kernel_raspi.c
│   ├── linker_raspi.ld
│   ├── config.txt
│   └── Makefile                       # `make qemu`, `make image`
└── ch15-next-steps/                   # Ch15. 인터럽트 벡터 스타터 키트
    ├── vectors.S
    ├── irq_demo.c
    └── Makefile
```

### 빌드 정책

- **상위 Makefile:** `make all`은 호스트에서 빌드 가능한 모든 챕터 (Ch1~Ch10)를 빌드. `make bare-metal`은 Ch11~Ch15까지 (aarch64-elf-gcc, QEMU 필요). `make qemu-run`은 Ch12·Ch13·Ch14·Ch15를 차례로 QEMU에서 실행. `make clean`은 전체 청소.
- **상위 CMakeLists.txt:** 호스트 챕터만 묶어 IDE 친화적 빌드. `cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`이 `compile_commands.json`을 만들어 Ch4 셋업의 출발점이 된다.
- **챕터 간 의존성 없음:** 각 챕터 디렉토리는 독립적으로 `make`가 동작한다. 독자가 Ch7부터 펴 들어도 그 챕터만 빌드된다.
- **컴파일러 가정:** 호스트 챕터는 Apple Clang 16+ 또는 Homebrew LLVM. 베어메탈 챕터(Ch11~Ch15)는 `aarch64-elf-gcc` (Homebrew). `make check` 한 줄로 환경 정합성을 점검 (Ch3 예제 재사용).
- **검증 자동화:** `tests/run_all.sh`가 모든 호스트 챕터를 빌드·실행하고, QEMU 챕터는 시리얼 출력에 기대 문자열(예: `hello, aarch64`)이 나오는지 timeout과 함께 확인. 책 출간 전 CI에서 회귀 방지.

---

## 검증 체크리스트

- [x] **모든 챕터가 핵심 질문에 답한다** — 15장 각각의 "핵심 질문" 한 줄이 챕터 본문의 결론으로 닫힌다.
- [x] **챕터 순서에 맥이 흐른다** — 위 "챕터 간 흐름" 한 줄 표가 각 챕터 전환의 동기를 명시한다. 난이도 점프 없음 (Ch10 → Ch11은 의도된 분기 — 호스트에서 베어메탈로의 정서적 다리 챕터).
- [x] **대상 독자 수준에 맞다** — 변수·반복문 등 기초 설명 없음. Java/JS/Python 출신 가정의 문장이 자연스럽다 ("Java는 ArrayIndexOutOfBoundsException을 던지지만 C는 침묵한다" 류).
- [x] **레퍼런스의 모든 주요 자료가 배치된다** — §2(표준)→Ch2, §3(본질)→Ch5~Ch7·Ch10, §4(환경)→Ch3·Ch11·Ch12, §5(IDE)→Ch4, §6(안전)→Ch9, §7(베어메탈)→Ch11~Ch14, §8(멘탈 모델 전환)→Ch5 도입부(전용 1~2쪽)·Ch7 비트 조작 절·Ch8 ABI 절, §9(논쟁)→Ch1·Ch2·Ch15에 분산.
- [x] **챕터 간 중복 없음** — 포인터는 Ch5, 메모리는 Ch6, UB는 Ch7, 표준 라이브러리는 Ch10으로 분리. 환경 설치는 Ch3에 집중, 에디터는 Ch4. 부팅 코드는 Ch12(첫 도달) · Ch13(해부) · Ch14(실기) 세 단계로 깊이 차이를 둠.
- [x] **예상 분량 합계가 목표에 부합한다** — 1만+1만1천+1만2천+1만+1만4천+1만3천+1만4천+1만3천+1만6천+1만3천+1만1천+1만3천+1만3천+1만3천+6천 = 약 18만 2천 자. 목표 17만 5천~21만 자 범위 중간대에 안착 (편집 단계에서 압축·확장 여지 모두 확보).
- [x] **example/ 폴더가 빌드 가능하다** — 호스트 챕터는 Apple Clang으로, 베어메탈 챕터는 `aarch64-elf-gcc` + QEMU로 검증 가능. CI 스크립트 골격(`tests/run_all.sh`)을 plan 단계에서 명시.
- [x] **Ch12~Ch14는 실제 부팅된다** — Ch12는 QEMU virt에서 "hello, aarch64" 출력, Ch13은 같은 코드의 3단계 변형이 각각 부팅, Ch14는 QEMU `raspi4b`와 실제 SD카드 이미지에서 부팅. 레퍼런스 §7.5 코드가 Ch12 예제의 골격, Ch13에서 한 줄씩 해부, Ch14에서 보드 차이를 흡수.

---

## 리서치 한계가 챕터 저술에 미치는 영향 (메모)

레퍼런스 §11의 한계 항목을 챕터별로 어떻게 흡수할지 미리 짚어 둔다.

- **학술 논문 부재** → Ch7(UB)와 Ch9(안전망)에서 Regehr 블로그·ACM Queue Catch-23 외에 *Towards Optimization-Safe Systems* 등 1차 논문 보강 필요. 챕터 저술 단계에서 `paper-research` 스킬 호출 권장.
- **BCM2711·Cortex-A72 일차 문서** → Ch14 저술 시 Broadcom 데이터시트와 ARM TRM의 GPIO·UART 레지스터 맵 직접 참조 필요. 차후 정오표 가능성도 있음.
- **C23 컴파일러 지원 매트릭스 최신판** → Ch2 저술 직전 cppreference C compiler support 페이지 + Apple Clang / Homebrew LLVM / GCC 릴리스 노트 교차 확인. 책 발간일 기준 정확성 보장 필요.
- **Cursor·Zed C 워크플로 실측** → Ch4 저술 시 빠르게 변하는 영역이므로 책의 표현을 "2026년 시점"으로 못박는 게 좋음.

위 사항은 챕터 저술가에게 챕터별 보강 포인트로 전달한다.
