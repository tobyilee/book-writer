/* 8장. util.c — 선언된 것들 중 일부를 정의한다. */
#include <stdio.h>
#include "util.h"

int add(int a, int b) {
    bump_counter();
    return a + b;
}

void greet(const char *name) {
    bump_counter();
    printf("hello, %s\n", name);
}
