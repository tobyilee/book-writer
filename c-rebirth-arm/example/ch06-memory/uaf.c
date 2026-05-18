/*
 * 의도된 use-after-free.
 *
 *   make uaf && ./uaf
 *
 * ASan이 켜져 있으면 read-after-free를 정확한 콜스택과 함께
 * 잡아 준다. 끄고 돌리면 어떤 운명을 만날지는 모른다 — 옆 메모리가
 * 우연히 살아 있어 보이거나, segfault로 죽거나.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *msg = malloc(32);
    if (!msg) return 1;

    strcpy(msg, "hello, c");
    printf("before free: %s\n", msg);

    free(msg);

    /* 여기서부터 msg는 댕글링 포인터다. 절대 만지면 안 되지만
     * 일부러 만져 본다 — ASan이 이걸 잡는지 확인하기 위해. */
    printf("after  free: %s\n", msg);   /* heap-use-after-free */
    return 0;
}
