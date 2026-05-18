# 6장. 메모리 관리 — 직접 사 와서 직접 돌려준다

Java에서 `new String("hello")`라고 적던 시절을 떠올려 보자. 우리가 그 객체를 다 쓰고 나면 어떻게 됐는가? **아무것도 안 했다.** 변수가 더 이상 그 객체를 가리키지 않으면, JVM의 가비지 컬렉터가 어느 한가한 시점에 와서 회수했다. 우리가 굳이 신경 쓸 일이 아니었다.

Python에서 `obj = SomeClass()`라고 적던 시절은 어땠는가? 비슷했다. 참조 카운팅이 0이 되는 순간 정리됐고, 가끔 순환 참조가 남으면 generational GC가 와서 청소했다. 역시 우리 일이 아니었다.

이제 그 안락한 동네에서 정말로 떠난다. C에서는 **메모리를 직접 사 와서 직접 돌려줘야 한다.** 빌려 와서 돌려주지 않으면 누수다. 두 번 돌려주면 시스템이 비명을 지른다. 돌려준 뒤에도 계속 들고 있으면 use-after-free라는 가장 무서운 사고가 난다.

C 입문자가 첫 몇 주에 부딪히는 통증의 90%가 이 메모리 관리에서 온다. 그러나 좋은 소식이 있다 — 패턴이 정해져 있다. 그 패턴 몇 가지만 손에 익히면 사고 빈도가 급격히 떨어진다. 그리고 우리에겐 9장에서 본격 다룰 ASan이라는 든든한 안전망이 있다. 이 챕터는 그 패턴과 안전망을 함께 짚는다.

## 스택과 힙 — 두 동네의 차이

먼저 메모리의 지형부터 살피자. C 프로그램이 메모리를 잡는 곳은 크게 두 동네다.

**스택.** 함수가 호출될 때마다 그 함수의 지역 변수가 자리 잡는 동네다. 함수가 끝나면 그 자리는 자동으로 사라진다. 빠르고 단순하다. 우리가 `int x = 42;`라고 함수 안에 적으면 `x`는 스택에 잡힌다.

```c
void foo(void) {
    int local = 10;       // 스택에 잡힌다
    char buf[256];        // 256바이트도 스택에 잡힌다
    // foo가 끝나면 local과 buf는 자동으로 사라진다
}
```

스택의 매력은 명료함이다. **사라질 시점이 함수의 종료라는 한 점으로 정해져 있다.** 따로 정리할 필요가 없다. 다만 한계가 있다 — 크기가 작다(보통 1~8MB). 그리고 함수가 끝나면 사라지니까, 함수 바깥으로 그 자리의 데이터를 그대로 들고 나가려고 하면 위험하다.

다음 코드를 보자. 옛 시절에 한 번씩 빠지던 함정이다.

```c
int *bad(void) {
    int x = 42;
    return &x;          // 끔찍한 일이다 — 사라질 자리의 주소를 반환
}

int main(void) {
    int *p = bad();
    printf("%d\n", *p); // UB. 운에 따라 42일 수도, 쓰레기일 수도, segfault일 수도
}
```

`bad`가 끝나면 `x`의 자리는 회수된다. 그 자리의 주소를 들고 나간 `p`는 댕글링 포인터다. 컴파일러가 친절히 경고를 띄워 주지만(`-Wreturn-stack-address`), 그 경고를 무시하고 빌드되긴 한다. 표준은 그저 "이건 UB다"라고 적어 둔다.

**힙.** 함수의 수명에 묶이지 않은 동네다. 우리가 `malloc`으로 사 와서, 다 쓰면 `free`로 돌려주는 자리. 큰 데이터를 잡을 때, 함수 경계를 넘어 살아남아야 할 데이터를 잡을 때 쓴다. 빠르기는 스택보다 느리고, 관리 책임이 우리에게 있다.

```c
int *good(void) {
    int *p = malloc(sizeof *p);
    if (!p) return NULL;
    *p = 42;
    return p;            // 호출자가 free 책임을 진다
}

int main(void) {
    int *p = good();
    if (p) {
        printf("%d\n", *p);   // 42
        free(p);
    }
}
```

여기서 한 가지 약속이 등장한다. **`good`이 malloc한 메모리의 free 책임은 호출자에게 있다.** 이 약속은 코드의 어디에도 명시되어 있지 않지만, C 프로그래머는 함수 이름과 시그니처를 보고 이 약속을 읽어 낸다. 그 약속을 어떻게 더 명료하게 표현할지가 이 챕터의 한 절을 차지한다.

## malloc 가족 — 네 가지 도구

힙 메모리를 다루는 표준 도구는 네 가지다.

**`malloc(n)`** — `n` 바이트를 잡아 첫 주소를 반환한다. 잡은 자리의 내용은 정해지지 않는다(쓰레기 값). 실패하면 NULL을 돌려준다. 항상 NULL 체크.

**`calloc(count, size)`** — `count × size` 바이트를 잡고 **0으로 초기화**한다. 0으로 초기화하는 비용이 약간 있지만, 초기화 실수의 위험이 줄어든다. 새 자료구조를 깔끔히 시작할 때 즐겨 쓴다.

**`realloc(ptr, n)`** — 기존 `ptr`의 메모리 크기를 `n` 바이트로 조정한다. 가능하면 같은 자리에서 늘리거나 줄이고, 안 되면 새 자리로 옮기고 옛 자리를 해제한다. **반환값을 꼭 같은 변수에 다시 받지 말자** — 실패 시 NULL이 돌아오는데, 그러면 원본 포인터를 잃어버려서 메모리 누수가 생긴다. 임시 변수로 받아서 검사한 뒤 대입하는 게 정석이다.

```c
int *tmp = realloc(buf, new_size * sizeof *buf);
if (!tmp) {
    // buf는 살아 있다 — 원하는 대로 처리(누수 방지)
    return -1;
}
buf = tmp;
```

**`free(ptr)`** — 잡은 자리를 돌려준다. NULL을 넘기는 건 안전하다 — 표준이 "아무것도 안 한다"고 명시한다. 그래서 `if (p) free(p)` 같은 검사는 사족이다.

이 네 가지로 거의 모든 일이 처리된다. 다만 옛 C 시절에 흔히 보던 한 가지 관용구가 C23부터 함정으로 바뀌었다. **`realloc(ptr, 0)`**이다.

옛날엔 이게 "메모리를 돌려준다"는 의미로 종종 쓰였다. `realloc(ptr, 0)` ≡ `free(ptr)` 같은 식. 그러나 C23은 이를 명시적으로 UB로 못 박았다. 이게 작은 변경 같지만, 오래된 라이브러리 코드가 조용히 깨질 수 있는 자리다. ACM Queue에 "Catch-23: The New C Standard Sets the World on Fire"라는 비판적 칼럼이 정리해 둔 변화 중 하나가 정확히 이거다. 우리는 이 책에서 `realloc(ptr, 0)`을 절대 쓰지 않는다. 메모리 해제는 `free`로 명시한다.

## 세 가지 통증 — 누수, UAF, double free

이 셋이 C 메모리 관리의 세 가지 큰 통증이다. 한 번씩 코드로 보고 가자. 이 챕터의 예제 디렉터리(`example/ch06-memory/`)에 세 파일이 분리되어 있다 — `leak.c`, `uaf.c`, `ok.c`.

### 누수 — 사 와서 안 돌려준다

```c
// leak.c
static int *make_box(int v) {
    int *box = malloc(sizeof *box);
    if (!box) return NULL;
    *box = v;
    return box;
}

int main(void) {
    for (int i = 0; i < 100; ++i) {
        int *b = make_box(i);
        (void)b;   // 일부러 버린다 — 이게 누수다
    }
}
```

`make_box`는 매번 새 메모리를 잡아 반환한다. 그러나 `main`은 그걸 받자마자 버린다. `free`가 어디에도 없다. 100번의 `malloc`이 그대로 살아남은 채 프로그램이 끝난다.

운영체제는 프로그램이 끝나면 그 프로세스가 쓰던 메모리를 모두 회수해 준다. 그래서 누수 100번 정도로 시스템이 망가지진 않는다. 그러나 장기 실행되는 서버나, 한 함수에서 1초에 수백 번 누수하는 코드는 이야기가 다르다. 메모리가 야금야금 차오르다가 어느 날 OOM(Out of Memory)으로 죽는다. **누수의 무서움은 즉각적이지 않다는 점에 있다.**

이걸 어떻게 잡는가? 두 길이 있다.

**길 1. macOS 내장 `leaks` 명령.** Apple Silicon의 ASan은 LSan 모듈을 포함하지 않아서 누수 자동 탐지가 안 된다. 대신 macOS에 내장된 `leaks`가 그 자리를 메운다.

```bash
make leak-check
# 내부에서 실행:
# leaks --atExit -- ./leak_noasan
```

`leaks --atExit`은 프로그램이 종료될 때 살아남은 힙 객체를 모두 보고한다. 처음 출력에 시스템 라이브러리 잔량이 잔뜩 섞여서 압도되지만, 출력의 끝쪽에 우리 코드가 잡은 자리가 정확히 적혀 있다.

**길 2. Linux 측 ASan + LSan.** 진지하게 누수를 추적하려면 같은 코드를 Linux 컨테이너에서 ASan과 함께 빌드해 돌리는 패턴이 강력하다. ASan은 종료 시점에 자동으로 LSan을 호출해 잔량을 보고한다. 출력 형태도 깔끔하다. CI를 두 OS로 도는 프로젝트라면 Linux 빌드에 누수 검사를 묶어 두자.

### Use-after-free — 돌려준 뒤에도 만진다

세 가지 중 가장 위험한 친구다.

```c
// uaf.c
int main(void) {
    char *msg = malloc(32);
    strcpy(msg, "hello, c");
    printf("before free: %s\n", msg);

    free(msg);

    printf("after  free: %s\n", msg);  // heap-use-after-free
}
```

`free(msg)` 다음에 `msg`는 댕글링 포인터다. 그 자리의 메모리는 이미 운영체제(또는 libc의 메모리 풀)로 돌아갔다. 다시 만지면 무슨 일이 벌어질지 모른다. 운이 좋으면 그 자리에 옛 데이터가 아직 남아 있어 정상 동작하는 것처럼 보이고, 운이 나쁘면 그 자리가 이미 다른 `malloc`에 다시 배정되어 그쪽 데이터를 깨뜨린다.

후자가 정말 끔찍한 일이다. 우리가 망친 곳과 사고가 터지는 곳이 다르다. 디버거로 사고 시점에서 추적하면 우리 코드와 무관해 보이는 자리에서 데이터가 망가져 있다.

다행히 ASan이 이걸 정확히 잡는다.

```bash
make uaf && ./uaf
```

ASan이 켜진 빌드를 돌리면 출력이 이렇게 나온다.

```
=================================================================
==12345==ERROR: AddressSanitizer: heap-use-after-free
READ of size 2 at 0x603000001c30
    #0 ... in printf_common ...
    #1 ... in main uaf.c:26
    ...
freed by thread T0 here:
    #0 ... in free ...
    #1 ... in main uaf.c:22
previously allocated by thread T0 here:
    #0 ... in malloc ...
    #1 ... in main uaf.c:16
```

세 가지가 한눈에 들어온다. **읽으려 한 자리, 그 자리가 언제 해제됐는지, 처음에 언제 잡혔는지.** 세 줄의 콜스택이 사고 추적을 거의 끝내 준다. ASan 없이 이 사고를 추적하려면 디버거로 하루를 잡아도 답이 안 나올 수 있다. 이 한 도구가 우리에게 주는 시간이 어마어마하다.

이걸 예방하는 작은 트릭. **`free` 직후에 포인터를 NULL로 리셋한다.**

```c
free(msg);
msg = NULL;     // 다음에 *msg를 만지면 즉시 segfault
```

UB의 두려운 점이 "조용히 잘못된 데이터를 읽는 것"이라면, NULL 역참조는 즉시 segfault라 차라리 안전하다. 자기 발등에 다친 손이 빨리 드러나니까.

### Double free — 두 번 돌려준다

```c
char *p = malloc(32);
free(p);
free(p);   // 두 번 — UB
```

이것도 ASan이 잡는다. libc 내부에서도 종종 잡지만, 패키지에 따라 동작이 다르다. ASan 빌드에선 항상 잡힌다.

double free를 만드는 가장 흔한 길은 **소유권이 두 군데에 있는 코드**다. 함수 A가 `free`했는데, 함수 B도 그 포인터를 들고 있어서 `free`한다. 두 함수 다 자기가 책임자라고 생각한 것이다. 이게 다음 절의 주제다.

## 소유권 약속 — 코드 수준에서 표현하기

C에는 Rust의 borrow checker도, C++의 RAII도 없다. **소유권은 약속이다.** 그 약속을 코드의 어디에 적어 두느냐가 중요하다.

이 책에서 권하는 컨벤션 몇 가지를 짚는다.

### `_create`/`_destroy` 페어

자료구조마다 만드는 함수와 없애는 함수의 이름을 짝지어 둔다.

```c
typedef struct vec vec_t;
vec_t *vec_create(size_t cap);
void   vec_destroy(vec_t *v);
```

이 한 페어가 약속의 출발점이다. **`_create`로 받은 건 반드시 `_destroy`로 돌려준다.** 함수 이름이 곧 짝짓는 표시다.

이 챕터 예제의 `ok.c`가 이 패턴을 따른다.

```c
typedef struct {
    size_t  len;
    size_t  cap;
    int    *data;
} ivec_t;

static ivec_t *ivec_create(size_t cap) {
    ivec_t *v = malloc(sizeof *v);
    if (!v) return NULL;
    v->data = malloc(cap * sizeof *v->data);
    if (!v->data) { free(v); return NULL; }
    v->len = 0;
    v->cap = cap;
    return v;
}

static void ivec_destroy(ivec_t *v) {
    if (!v) return;
    free(v->data);
    free(v);
}
```

`ivec_create`는 두 단계 malloc을 한다 — 구조체와 데이터 배열. 중간에 두 번째 malloc이 실패하면? **이미 잡은 첫 번째를 풀어 주고 반환한다.** 이 한 줄(`free(v); return NULL`)이 빠지면 부분 실패 누수가 생긴다. 이런 부분 실패 경로가 C 메모리 관리의 가장 까다로운 자리다.

### `_owned` vs `_borrow` 주석

함수 시그니처에 보통 컨벤션으로 명시한다.

```c
// 호출자가 owns. 함수 안에서 보관·복사하지 않는다.
void process(const item_t *borrowed);

// 함수가 새로 만든다. 호출자가 free 책임.
item_t *item_create(void);

// 호출자가 넘긴다. 함수가 free 책임을 진다.
void take_and_destroy(item_t *owned);
```

이런 패턴이 코드 베이스에 일관되게 깔리면, 함수 시그니처만 봐도 "누가 free하는지"가 보인다. 이 책의 예제에서도 이 컨벤션을 의식적으로 따른다.

### `goto cleanup` — 안티패턴이 아니다

Java나 Python에선 `try/finally`로 청소 코드를 묶는다. C에는 없다. 그러나 흔히 만나는 패턴이 있다 — `goto cleanup`이다.

```c
int do_work(void) {
    int rc = -1;
    char *buf  = NULL;
    FILE *fp   = NULL;

    buf = malloc(4096);
    if (!buf) goto cleanup;

    fp = fopen("data.txt", "r");
    if (!fp) goto cleanup;

    if (fread(buf, 1, 4096, fp) == 0) goto cleanup;

    rc = 0;   // 성공

cleanup:
    if (fp)  fclose(fp);
    free(buf);   // free(NULL)은 안전
    return rc;
}
```

이걸 처음 보면 "`goto`는 나쁘다"는 옛 가르침이 떠올라 망설여진다. 그러나 **단일 출구로 청소 코드를 모으는 이 패턴은 안티패턴이 아니라 C의 정석 관용구다.** 리눅스 커널, libc, 거의 모든 시스템 C 코드가 이 패턴을 쓴다. 이유는 단순하다 — 함수 중간에서 일찍 반환할 때마다 같은 청소 코드를 반복해 적으면 한 곳을 빼먹기 쉽다. `goto cleanup` 한 곳에 모아 두는 게 훨씬 안전하다.

다만 두 가지 규칙. 첫째, **`goto`는 함수 안에서, 앞쪽 라벨로만 점프한다.** 뒤로 점프하거나 함수 경계를 넘는 건 금지다. 둘째, **`free(NULL)`이 안전하다는 사실을 활용한다.** 변수를 NULL로 초기화해 두면 cleanup 라벨에서 일괄 `free`가 안전하다.

### `__attribute__((cleanup))` — GNU 확장의 RAII 흉내

GNU C(GCC와 Clang이 모두 지원)의 확장 기능 하나가 매력적이다. **`__attribute__((cleanup(fn)))`**.

```c
static inline void free_charp(char **p) {
    free(*p);
}

#define cleanup_free __attribute__((cleanup(free_charp)))

void example(void) {
    cleanup_free char *buf = malloc(1024);
    if (!buf) return;

    // ... 사용 ...

    return;  // buf가 자동으로 free된다
}
```

스코프를 벗어나는 순간 컴파일러가 `free_charp(&buf)`를 호출해 준다. RAII의 작은 사촌이다. 표준 C는 아니지만 GCC·Clang에서 동작하고, systemd 같은 큰 코드 베이스가 일관되게 쓴다.

베어메탈 코드에서는 이 확장이 특히 유용하다 — 표준 라이브러리 없이도 동작하는 정리 메커니즘이라서. 다만 표준 C 코드의 이식성을 우선하는 프로젝트라면 `goto cleanup` 쪽이 더 안전한 기본값이다.

### 한 가지 더 — 누가 메모리를 잡는가에 따른 패턴

소유권을 다루다 보면 비슷한 코드가 두 가지 모양새로 나뉜다. 잠깐 짚고 가자.

**패턴 A — 호출자가 버퍼를 잡고, 함수가 채운다.**

```c
int read_line(char *buf, size_t cap);
// 호출:
char buf[256];
int n = read_line(buf, sizeof buf);
```

호출자가 모든 메모리를 책임진다. 함수는 빌려 받은 자리를 채우고 끝낸다. 메모리 관리가 한 곳에 모인다는 점에서 깔끔하다. 다만 크기를 미리 알아야 한다는 한계가 있다.

**패턴 B — 함수가 새로 잡아 호출자에게 넘긴다.**

```c
char *read_line_alloc(void);
// 호출:
char *line = read_line_alloc();
if (line) { /* ... */ free(line); }
```

크기가 가변일 때 자연스럽다. 그러나 `free` 책임이 호출자로 넘어가는 약속이 명확해야 한다.

라이브러리를 설계할 때 두 패턴을 한 함수에 섞지 말자. 호출자가 버퍼를 넘기는데 함수도 안에서 따로 malloc해 채워 주면 소유권이 두 곳으로 갈라져서 사고가 난다. 한 함수는 한 약속만.

## 정상 동작 예제 — 한 바퀴

이 챕터 예제의 `ok.c`를 한 바퀴 돌아 보자. 동적 배열(`ivec_t`)을 만들고, 값을 채우고, 정리한다.

```c
int main(void) {
    ivec_t *v = ivec_create(4);
    if (!v) return 1;

    for (int i = 0; i < 10; ++i) {
        if (ivec_push(v, i * i) != 0) {
            ivec_destroy(v);
            return 1;
        }
    }

    printf("len=%zu, cap=%zu, last=%d\n", v->len, v->cap, v->data[v->len-1]);
    ivec_destroy(v);
    return 0;
}
```

이 코드의 약속을 한 줄씩 짚자.

- `ivec_create(4)`로 받은 `v`는 **이 함수가 소유한다.** 정상 종료 시 `ivec_destroy`로 돌려준다.
- 중간에 `ivec_push`가 실패하면? **그래도 `v`는 살아 있다.** 그래서 `ivec_destroy(v)`로 돌려주고 나간다. 부분 성공 상태에서도 청소가 누락되지 않는다.
- `ivec_push`가 내부에서 `realloc` 실패를 만나면 `-1`을 돌려주지만, **`v->data`는 그대로 살아 있다.** realloc 패턴의 정석을 따랐기 때문이다.

이게 책 한 권을 들어 알려 줄 만한 코드는 아니다. 그러나 이 단순한 30줄에 "소유권은 누구에게 있는가", "실패 경로에서도 청소를 보장하는가"라는 두 질문이 명시적으로 답해져 있다는 점이 중요하다.

ASan을 켜고 돌려도 깨끗하다.

```bash
make ok && ./ok
# len=10, cap=16, last=81
# ok: 모든 malloc에 짝 free가 있었다.
```

`malloc`이 정확히 두 번(`ivec_create`에서 구조체, 데이터 배열). 그 다음 `realloc`이 몇 번(배열 확장). `free`가 두 번(`ivec_destroy`에서 데이터, 구조체). 짝이 맞는다.

## 자주 만나는 함정

마지막으로, 메모리 관리에서 첫 몇 주에 누구나 한 번씩 부딪히는 함정을 모아 둔다.

**malloc 결과를 검사 안 한다.** `malloc`은 실패할 수 있다. 메모리가 모자라거나, 너무 큰 요청이거나, 베어메탈 환경에서는 더 자주. 항상 NULL 검사를 한다.

**malloc 결과를 캐스팅한다.** `(int *)malloc(...)`. 옛 K&R 시절엔 흔했지만, 모던 C에선 권장하지 않는다. `void *`는 어떤 포인터로든 자동 변환되므로 캐스팅이 사족이다. 게다가 캐스팅이 있으면 `#include <stdlib.h>`를 빼먹어도 컴파일이 통과되는 경고가 가려지는 부작용이 있다. C++ 호환성이 정말 절실한 헤더가 아닌 한, 캐스팅은 빼자.

**sizeof를 잘못 쓴다.** `malloc(n * sizeof(int))`보다 `malloc(n * sizeof *p)`가 안전하다. 후자는 `p`의 타입이 바뀌어도 자동으로 맞춰진다. 이게 미묘한 차이 같지만, 코드 베이스가 크면 누적된 효과가 크다.

**구조체 안의 포인터를 잊는다.** `struct user { char *name; ... }`에서 `name`이 `malloc`된 문자열이면, 구조체를 `free`하기 전에 `name`을 먼저 `free`해야 한다. `_destroy` 함수가 그 책임을 진다.

**중첩 컨테이너의 해제 순서.** 동적 배열 안에 동적 문자열이 들어 있다면, 배열을 `free`하기 전에 각 문자열을 먼저 `free`. 컨테이너의 `destroy` 함수가 내부 원소를 어떻게 처리할지를 미리 약속해 둔다.

**stack overflow.** 큰 배열을 함수 안에 그대로 `int buf[1024 * 1024]`처럼 잡으면 스택을 폭주시킨다. 기본 스택 크기가 8MB 안팎인데, 한 함수에서 그 한계를 넘기는 큰 자동 변수는 위험하다. 큰 데이터는 힙으로.

**C99의 VLA(가변 길이 배열).** `int arr[n]`처럼 런타임 크기로 잡는 배열이 C99에 들어왔다. 편해 보이지만 스택에 잡히므로 큰 `n`이 들어오면 스택 오버플로다. 게다가 C11에서 선택 사항이 되어 컴파일러 지원이 일관되지 않다. 실무에서는 VLA를 피하고 명시적인 `malloc`/`alloca`로 대체하는 편이 안전하다.

이 여섯 함정을 머리 한쪽에 두고, ASan을 늘 켜고 작업하면 첫 몇 주의 사고가 절반 이하로 준다. 나머지 절반은 다음 장에서 만날 더 깊은 사고들 — UB와 strict aliasing이 책임진다.

## 마무리

이제 손에 들린 게 셋이다. 첫째, **메모리는 직접 사 와서 직접 돌려준다**는 단순한 원칙. 둘째, **누가 free하는지를 함수 이름과 시그니처로 명시한다**는 컨벤션. 셋째, **`goto cleanup`이라는 정석 관용구**가 안티패턴이 아니라 C의 자연스러운 모양새라는 사실.

여기에 9장에서 본격 다룰 ASan을 더하면, C 메모리 관리의 통증 90%가 일상적인 도구로 처리된다. 옛 K&R 시절에 "C는 무섭다"고 했던 자리의 절반이 사실은 도구의 부재였다. 도구가 있으니 우리는 침착하게 사고를 마주할 수 있다.

다음 장이 그 보강이다. C가 우리를 어떻게 배신하는지 — UB와 strict aliasing이라는 가장 까다로운 손님들을 정면으로 본다. 그리고 그 와중에 베어메탈로 가는 다리 하나를 더 놓는다. **비트 폭, 시프트, 마스크, 엔디언.** 옛 K&R 시절에 `int`와 `long`을 막연하게 쓰던 손이 어떻게 `uint32_t`와 `1u << 7` 같은 정확한 손으로 자라는지. 이 챕터의 메모리 약속이 손에 들어왔다면, 다음 장의 비트 손풀기는 한 단계 더 깊은 자리로 우리를 데려간다.
