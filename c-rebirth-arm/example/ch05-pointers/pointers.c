/*
 * Ch5 — 포인터 다섯 시나리오 한 파일.
 *
 * 함수 단위로 분리해 main에서 차례로 호출한다. 출력을 보면
 * "주소", "포인터를 통한 쓰기", "배열의 감쇠", "함수 포인터",
 * "void *를 거치는 일반 컨테이너" 다섯 그림이 손에 들어온다.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ── 1. 주소 출력: 변수도 메모리 어딘가에 산다 ── */
static void addr_basic(void) {
    int x = 42;
    int *p = &x;

    printf("[1] addr_basic\n");
    printf("    &x      = %p\n", (void *)&x);
    printf("    p       = %p\n", (void *)p);
    printf("    *p      = %d\n", *p);

    *p = 7;                              /* 별명을 통한 쓰기 */
    printf("    after *p=7, x = %d\n\n", x);
}

/* ── 2. 포인터의 포인터: 함수가 새 객체를 만들어 돌려줄 때 ── */
static void make_int(int **out, int seed) {
    *out = malloc(sizeof **out);          /* malloc 결과 캐스팅 안 한다 */
    if (*out) **out = seed * seed;
}

static void pointer_to_pointer(void) {
    int *box = NULL;
    make_int(&box, 9);

    printf("[2] pointer_to_pointer\n");
    if (box) {
        printf("    make_int(9) → %d\n", *box);
        free(box);
    }
    printf("\n");
}

/* ── 3. 배열의 감쇠: 함수 인자로 넘어가면 sizeof가 거짓말한다 ── */
static void show_size(int arr[]) {
    /* 여기서의 arr은 사실 int*. sizeof는 포인터 크기다. */
    printf("    inside show_size, sizeof(arr) = %zu (포인터 크기)\n",
           sizeof arr);
}

static void array_decay(void) {
    int xs[] = { 1, 2, 3, 4, 5 };
    size_t n = sizeof xs / sizeof xs[0];

    printf("[3] array_decay\n");
    printf("    in main, sizeof(xs) = %zu, n = %zu\n", sizeof xs, n);
    show_size(xs);

    /* arr[i] ≡ *(arr + i) */
    printf("    *(xs+2) = %d (== xs[2])\n\n", *(xs + 2));
}

/* ── 4. 함수 포인터: Java 람다, Python 일급 함수의 친척 ── */
static int add(int a, int b) { return a + b; }
static int mul(int a, int b) { return a * b; }

typedef int (*binop_t)(int, int);          /* "두 int 받고 int 돌려주는 함수" */

static int apply(binop_t op, int a, int b) { return op(a, b); }

static void func_pointer(void) {
    printf("[4] func_pointer\n");
    printf("    apply(add, 3, 4) = %d\n", apply(add, 3, 4));
    printf("    apply(mul, 3, 4) = %d\n\n", apply(mul, 3, 4));
}

/* ── 5. void *: 타입을 모르는 일반 컨테이너 자리 ── */
static void copy_blob(void *dst, const void *src, size_t n) {
    /* memcpy를 흉내내는 함수. void*는 어떤 포인터로도 변환된다. */
    unsigned char *d = dst;
    const unsigned char *s = src;
    for (size_t i = 0; i < n; ++i) d[i] = s[i];
}

static void void_pointer(void) {
    int from = 0xC0FFEE;
    int to   = 0;
    copy_blob(&to, &from, sizeof to);

    printf("[5] void_pointer\n");
    printf("    copy_blob 후 to = 0x%X\n\n", to);
}

int main(void) {
    addr_basic();
    pointer_to_pointer();
    array_decay();
    func_pointer();
    void_pointer();
    return 0;
}
