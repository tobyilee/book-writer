/* map.h — 작은 해시맵 (string key → int value)
 *
 * 충돌 해결: open addressing + linear probing.
 * 해시: FNV-1a 32비트.
 * load factor 0.75를 넘으면 두 배로 리해시.
 *
 * 키 소유권: map_put이 키 문자열을 내부에서 strdup한다. 호출자의
 * 원본 키는 map과 독립적으로 살아 있다 (또는 죽어도 된다).
 */
#ifndef MAP_H
#define MAP_H

#include <stdbool.h>
#include <stddef.h>

typedef struct map_t map_t;

map_t *map_create(void);
void   map_destroy(map_t *m);

size_t map_len(const map_t *m);

/* 키-값 삽입 (덮어쓰기 허용). 성공 0, 실패 -1. */
int    map_put(map_t *m, const char *key, int value);

/* 키로 값 찾기. 있으면 true 리턴하며 *out_value 채움. 없으면 false. */
bool   map_get(const map_t *m, const char *key, int *out_value);

/* 키 삭제. 있었으면 true, 없었으면 false. */
bool   map_del(map_t *m, const char *key);

#endif
