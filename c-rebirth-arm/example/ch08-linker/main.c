/* 8장. main.c — 다른 두 .o 와 링크되어 한 실행파일이 된다. */
#include <stdio.h>
#include "util.h"

int main(void) {
    greet("aarch64");
    int s = add(3, 4);
    printf("3 + 4 = %d, calls so far = %d\n", s, g_call_count);
    return 0;
}
