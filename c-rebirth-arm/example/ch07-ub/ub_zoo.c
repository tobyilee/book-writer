/*
 * 7장. UB 표본실.
 *
 * 이 파일에 모인 네 함수는 "일부러 잘못된 코드"다.
 * 절대 운영 코드의 본보기로 베껴 쓰지 말자.
 * UBSan을 켠 빌드에서 각 함수가 어떻게 잡히는지 보는 게 목적이다.
 *
 *   make ubsan
 *   ./ub_zoo overflow
 *   ./ub_zoo alias
 *   ./ub_zoo null
 *   ./ub_zoo oob
 *
 * 인자 없이 실행하면 환경 변수 UB_DEMO를 본다.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* (1) signed 정수 오버플로 — signed 산술의 오버플로는 UB.
 * UBSan은 -fsanitize=signed-integer-overflow로 잡는다. */
static int demo_signed_overflow(void) {
    int big = 2000000000;
    int sum = big + big;   /* INT_MAX를 넘는다 */
    printf("signed overflow result = %d\n", sum);
    return sum;
}

/* (2) strict aliasing 위반 — int 비트를 float로 재해석하려고
 * 포인터 캐스트로 들여다봄. C 표준이 금지하는 패턴이다.
 * 안전한 방법은 memcpy로 비트만 옮기는 것. */
static float demo_strict_aliasing(void) {
    int bits = 0x40490FDB;          /* pi의 IEEE-754 비트 */
    float *as_float = (float *)&bits;   /* 일부러 잘못된 코드 */
    float value = *as_float;        /* UB — strict aliasing 위반 */
    printf("aliasing pi ~= %f\n", (double)value);
    return value;
}

/* (3) NULL 역참조 — UBSan -fsanitize=null로 잡힌다. */
static int demo_null_deref(void) {
    int *p = NULL;
    int v = *p;                     /* 일부러 잘못된 코드 */
    printf("null deref = %d\n", v);
    return v;
}

/* (4) OOB read — 스택 배열 경계 밖을 읽는다.
 * ASan으로 잡으면 stack-buffer-overflow로 떨어진다. */
static int demo_oob_read(void) {
    int arr[4] = {10, 20, 30, 40};
    int i = 7;                      /* 배열 길이는 4 */
    int v = arr[i];                 /* 일부러 잘못된 코드 */
    printf("oob read arr[%d] = %d\n", i, v);
    return v;
}

static void usage(const char *argv0) {
    fprintf(stderr,
        "usage: %s {overflow|alias|null|oob}\n"
        "  또는 환경 변수 UB_DEMO 로 지정.\n",
        argv0);
}

int main(int argc, char **argv) {
    const char *which = NULL;
    if (argc >= 2) {
        which = argv[1];
    } else {
        which = getenv("UB_DEMO");
    }
    if (!which) { usage(argv[0]); return 2; }

    if (strcmp(which, "overflow") == 0) { demo_signed_overflow(); return 0; }
    if (strcmp(which, "alias")    == 0) { demo_strict_aliasing(); return 0; }
    if (strcmp(which, "null")     == 0) { demo_null_deref();      return 0; }
    if (strcmp(which, "oob")      == 0) { demo_oob_read();        return 0; }

    usage(argv[0]);
    return 2;
}
