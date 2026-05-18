/* vec.c — 자기 만든 동적 배열 구현
 *
 * 정책: capacity 두 배 증가, realloc 실패는 호출자에게 -1로 전달.
 */
#include "vec.h"

#include <stdlib.h>
#include <string.h>

struct vec_t {
    int   *data;
    size_t len;
    size_t cap;
};

vec_t *vec_create(void)
{
    vec_t *v = malloc(sizeof *v);
    if (!v) return NULL;
    v->data = NULL;
    v->len = 0;
    v->cap = 0;
    return v;
}

void vec_destroy(vec_t *v)
{
    if (!v) return;
    free(v->data);
    free(v);
}

size_t vec_len(const vec_t *v) { return v ? v->len : 0; }
size_t vec_cap(const vec_t *v) { return v ? v->cap : 0; }

static int vec_grow(vec_t *v)
{
    size_t new_cap = (v->cap == 0) ? 4 : v->cap * 2;
    int *new_data = realloc(v->data, new_cap * sizeof *new_data);
    if (!new_data) return -1;
    v->data = new_data;
    v->cap = new_cap;
    return 0;
}

int vec_push(vec_t *v, int value)
{
    if (!v) return -1;
    if (v->len == v->cap) {
        if (vec_grow(v) != 0) return -1;
    }
    v->data[v->len++] = value;
    return 0;
}

int vec_get(const vec_t *v, size_t idx, int *out_ok)
{
    if (!v || idx >= v->len) {
        if (out_ok) *out_ok = 0;
        return -1;
    }
    if (out_ok) *out_ok = 1;
    return v->data[idx];
}

int vec_set(vec_t *v, size_t idx, int value)
{
    if (!v || idx >= v->len) return -1;
    v->data[idx] = value;
    return 0;
}
