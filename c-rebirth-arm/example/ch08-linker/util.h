/* 8장. 헤더에는 선언만, 정의는 .c 한 곳에. */
#ifndef CH08_UTIL_H
#define CH08_UTIL_H

#include <stddef.h>

/* 외부 전역 — 한 번 정의되고 여러 .c가 공유한다. */
extern int g_call_count;

/* 함수 선언(prototype) 셋. 정의는 util.c / extern_global.c 에서. */
int  add(int a, int b);
void greet(const char *name);
void bump_counter(void);

#endif /* CH08_UTIL_H */
