/*
 * triple.c — 3장. Day 0 환경 점검
 *
 * 지금 이 코드를 컴파일하는 컴파일러가
 *   (1) 어느 타깃(target triple)을 향해 빌드하는가?
 *   (2) Apple 플랫폼인가, ARM인가?
 *   (3) 어떤 표준이 활성화돼 있는가?
 * 를 한 화면에 정리해서 보여준다.
 *
 * 베어메탈 챕터로 갈 때 가장 자주 잘못되는 게 "타깃을 잘못 잡았는지"라서,
 * 호스트 환경에서부터 자기 컴파일러의 자기 인식 정보를 손에 익혀두는 게 좋다.
 */

#include <stdio.h>

#ifdef __VERSION__
#  define COMPILER_VERSION __VERSION__
#else
#  define COMPILER_VERSION "(unknown)"
#endif

int main(void) {
    printf("--- compiler self-report ---\n");

#if defined(__clang__)
    printf("  toolchain         : clang %d.%d.%d\n",
           __clang_major__, __clang_minor__, __clang_patchlevel__);
#elif defined(__GNUC__)
    printf("  toolchain         : gcc %d.%d.%d\n",
           __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__);
#else
    printf("  toolchain         : (unknown)\n");
#endif

    printf("  __VERSION__       : %s\n", COMPILER_VERSION);

#ifdef __STDC_VERSION__
    printf("  __STDC_VERSION__  : %ld\n", (long)__STDC_VERSION__);
#else
    printf("  __STDC_VERSION__  : (not defined, likely C89/C90)\n");
#endif

    printf("\n--- target identity ---\n");

#ifdef __aarch64__
    printf("  __aarch64__       : 1 (AArch64, 64-bit ARM)\n");
#else
    printf("  __aarch64__       : 0\n");
#endif

#ifdef __x86_64__
    printf("  __x86_64__        : 1 (Intel/AMD 64-bit)\n");
#else
    printf("  __x86_64__        : 0\n");
#endif

#ifdef __APPLE__
    printf("  __APPLE__         : 1 (Apple platform — Mach-O)\n");
#else
    printf("  __APPLE__         : 0 (not an Apple host)\n");
#endif

#ifdef __linux__
    printf("  __linux__         : 1\n");
#else
    printf("  __linux__         : 0\n");
#endif

    printf("\n--- byte order ---\n");
#if defined(__BYTE_ORDER__) && defined(__ORDER_LITTLE_ENDIAN__)
    if (__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__) {
        printf("  endianness        : little (Apple Silicon / ARM 기본)\n");
    } else {
        printf("  endianness        : big\n");
    }
#else
    printf("  endianness        : (unknown)\n");
#endif

    printf("\nDay 0 환경 점검이 끝났다. 이 출력이 보였다면 컴파일러는 살아 있다.\n");
    return 0;
}
