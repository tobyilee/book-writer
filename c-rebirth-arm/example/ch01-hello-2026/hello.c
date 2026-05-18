/*
 * hello.c — 1장. 같은 인사를 두 시대로 빌드해보기
 *
 * 이 한 파일을 `-std=c89`로 한 번, `-std=c23`으로 한 번 빌드해본다.
 * 같은 코드가 두 표준에서 어떻게 받아들여지는지 비교하는 게 목적이다.
 *
 * 빌드:
 *   make c89     # C89 스타일로 빌드 (옛날 스타일)
 *   make c23     # C23 스타일로 빌드 (모던 스타일 + 경고 가득)
 *   make both    # 두 표준 모두 빌드
 *   make clean   # 산출물 정리
 */

#include <stdio.h>

int main(void) {
    /* K&R 시절에도 통하고, C23에서도 그대로 통하는 가장 단순한 인사. */
    printf("hello, c — %s\n",
#if __STDC_VERSION__ >= 202311L
           "2026 (C23)"
#elif __STDC_VERSION__ >= 201710L
           "2018 (C17)"
#elif __STDC_VERSION__ >= 201112L
           "2011 (C11)"
#elif __STDC_VERSION__ >= 199901L
           "1999 (C99)"
#else
           "1989 (C89/ANSI)"
#endif
    );
    return 0;
}
