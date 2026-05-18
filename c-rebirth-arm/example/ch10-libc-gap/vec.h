/* vec.h — 자기 만든 동적 배열 (int 전용)
 *
 * Java의 ArrayList, Python의 list, JS의 Array에 익숙한 손이
 * C에서 같은 감각을 얻기 위해 직접 만드는 가장 작은 컨테이너.
 *
 * 소유권 컨벤션: vec_create()로 얻은 vec_t*는 vec_destroy()로 돌려준다.
 * 함수가 vec_t*를 받는 의미는 "빌려 쓴다(borrow)" — free 책임은 호출자에게.
 */
#ifndef VEC_H
#define VEC_H

#include <stddef.h>

typedef struct vec_t vec_t;

/* 생성 / 파괴 — _create/_destroy 짝 */
vec_t *vec_create(void);
void   vec_destroy(vec_t *v);

/* 길이·용량 */
size_t vec_len(const vec_t *v);
size_t vec_cap(const vec_t *v);

/* 끝에 원소 추가. 실패 시 -1, 성공 시 0. */
int    vec_push(vec_t *v, int value);

/* 인덱스로 읽기. 범위 밖이면 -1 리턴하며 *out_ok = 0. */
int    vec_get(const vec_t *v, size_t idx, int *out_ok);

/* 인덱스로 쓰기. 성공 시 0, 범위 밖이면 -1. */
int    vec_set(vec_t *v, size_t idx, int value);

#endif
