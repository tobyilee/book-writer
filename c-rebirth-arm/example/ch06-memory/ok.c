/*
 * 정상 동작 예제 — 짝을 맞춰 free 한다.
 *
 *   make ok && ./ok
 *
 * ASan을 켜고 돌려도 깨끗하다.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    size_t  len;
    size_t  cap;
    int    *data;
} ivec_t;

/* _create와 _destroy 페어. 함수 이름이 곧 소유권 약속이다. */
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

static int ivec_push(ivec_t *v, int x) {
    if (v->len == v->cap) {
        size_t ncap = v->cap * 2;
        int *nd = realloc(v->data, ncap * sizeof *nd);
        if (!nd) return -1;        /* 원본은 살아 있다 — 호출자가 처리 */
        v->data = nd;
        v->cap  = ncap;
    }
    v->data[v->len++] = x;
    return 0;
}

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
    printf("ok: 모든 malloc에 짝 free가 있었다.\n");
    return 0;
}
