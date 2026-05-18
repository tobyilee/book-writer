#ifndef GEOM_H
#define GEOM_H

/*
 * 2D / 3D 벡터 길이 계산 — 에디터 셋업 검증용 미니 라이브러리.
 *
 * 이 헤더가 clangd로 인덱싱되고, 자동 완성과 "정의로 이동"이
 * 동작하면 VS Code + clangd 셋업이 통과한 것이다.
 */

typedef struct {
    double x;
    double y;
} vec2_t;

typedef struct {
    double x;
    double y;
    double z;
} vec3_t;

double vec2_length(vec2_t v);
double vec3_length(vec3_t v);

/* 정규화: 길이가 0인 입력은 그대로 돌려보낸다(0 벡터). */
vec2_t vec2_normalize(vec2_t v);
vec3_t vec3_normalize(vec3_t v);

#endif /* GEOM_H */
