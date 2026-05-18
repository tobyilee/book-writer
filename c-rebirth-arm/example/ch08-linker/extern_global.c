/* 8장. extern_global.c — 헤더의 extern 변수와 bump_counter 정의 한 곳. */
#include "util.h"

/* extern int g_call_count; (헤더) 의 짝.
 * 여기 한 곳에서만 정의되어야 링커가 안 운다. */
int g_call_count = 0;

void bump_counter(void) {
    g_call_count++;
}
