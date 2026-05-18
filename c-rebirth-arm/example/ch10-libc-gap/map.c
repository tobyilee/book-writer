/* map.c — 작은 해시맵 구현 (open addressing + FNV-1a)
 *
 * 슬롯 상태 세 가지 — EMPTY / OCCUPIED / TOMBSTONE.
 * 삭제는 tombstone으로 표시해서 probing 사슬을 보존한다.
 */
#include "map.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

enum slot_state {
    SLOT_EMPTY = 0,
    SLOT_OCCUPIED,
    SLOT_TOMBSTONE,
};

typedef struct slot_t {
    char           *key;     /* malloc/strdup된 키 */
    int             value;
    enum slot_state state;
} slot_t;

struct map_t {
    slot_t *slots;
    size_t  cap;
    size_t  len;       /* OCCUPIED 슬롯 개수 */
};

#define INITIAL_CAP 8

static uint32_t fnv1a(const char *s)
{
    uint32_t h = 2166136261u;
    while (*s) {
        h ^= (uint8_t)*s++;
        h *= 16777619u;
    }
    return h;
}

static int map_init_slots(map_t *m, size_t cap)
{
    m->slots = calloc(cap, sizeof *m->slots);
    if (!m->slots) return -1;
    m->cap = cap;
    m->len = 0;
    return 0;
}

map_t *map_create(void)
{
    map_t *m = malloc(sizeof *m);
    if (!m) return NULL;
    if (map_init_slots(m, INITIAL_CAP) != 0) {
        free(m);
        return NULL;
    }
    return m;
}

void map_destroy(map_t *m)
{
    if (!m) return;
    for (size_t i = 0; i < m->cap; i++) {
        if (m->slots[i].state == SLOT_OCCUPIED) free(m->slots[i].key);
    }
    free(m->slots);
    free(m);
}

size_t map_len(const map_t *m) { return m ? m->len : 0; }

/* probing으로 키를 찾거나, 비어 있는 첫 슬롯을 돌려준다.
 * 리턴값: 슬롯 인덱스. 키와 일치하는 OCCUPIED를 만나면 그 자리,
 *         아니면 EMPTY/TOMBSTONE 중 가장 먼저 만난 자리.
 *         (TOMBSTONE을 만난 뒤에도 일치 키를 찾기 위해 사슬을 계속 따라간다.)
 */
static size_t map_probe(const slot_t *slots, size_t cap, const char *key)
{
    size_t mask = cap - 1; /* cap은 항상 2의 거듭제곱 */
    size_t i = fnv1a(key) & mask;
    size_t first_free = (size_t)-1;
    for (;;) {
        const slot_t *s = &slots[i];
        if (s->state == SLOT_EMPTY) {
            return (first_free != (size_t)-1) ? first_free : i;
        }
        if (s->state == SLOT_TOMBSTONE) {
            if (first_free == (size_t)-1) first_free = i;
        } else if (strcmp(s->key, key) == 0) {
            return i;
        }
        i = (i + 1) & mask;
    }
}

static int map_resize(map_t *m, size_t new_cap)
{
    slot_t *old = m->slots;
    size_t  old_cap = m->cap;

    slot_t *fresh = calloc(new_cap, sizeof *fresh);
    if (!fresh) return -1;

    m->slots = fresh;
    m->cap = new_cap;
    m->len = 0;

    for (size_t i = 0; i < old_cap; i++) {
        if (old[i].state != SLOT_OCCUPIED) continue;
        size_t j = map_probe(m->slots, m->cap, old[i].key);
        m->slots[j].key = old[i].key;        /* 키 메모리는 그대로 옮긴다 */
        m->slots[j].value = old[i].value;
        m->slots[j].state = SLOT_OCCUPIED;
        m->len++;
    }
    free(old);
    return 0;
}

int map_put(map_t *m, const char *key, int value)
{
    if (!m || !key) return -1;

    /* load factor 0.75 검사 — TOMBSTONE도 점유로 본다고 가정해 보수적으로 */
    if ((m->len + 1) * 4 >= m->cap * 3) {
        if (map_resize(m, m->cap * 2) != 0) return -1;
    }

    size_t i = map_probe(m->slots, m->cap, key);
    if (m->slots[i].state == SLOT_OCCUPIED) {
        m->slots[i].value = value;
        return 0;
    }

    char *dup = strdup(key);
    if (!dup) return -1;
    m->slots[i].key = dup;
    m->slots[i].value = value;
    m->slots[i].state = SLOT_OCCUPIED;
    m->len++;
    return 0;
}

bool map_get(const map_t *m, const char *key, int *out_value)
{
    if (!m || !key) return false;
    size_t i = map_probe(m->slots, m->cap, key);
    if (m->slots[i].state != SLOT_OCCUPIED) return false;
    if (out_value) *out_value = m->slots[i].value;
    return true;
}

bool map_del(map_t *m, const char *key)
{
    if (!m || !key) return false;
    size_t i = map_probe(m->slots, m->cap, key);
    if (m->slots[i].state != SLOT_OCCUPIED) return false;
    free(m->slots[i].key);
    m->slots[i].key = NULL;
    m->slots[i].state = SLOT_TOMBSTONE;
    m->len--;
    return true;
}
