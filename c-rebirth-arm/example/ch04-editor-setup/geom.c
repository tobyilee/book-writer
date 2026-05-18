#include "geom.h"
#include <math.h>

double vec2_length(vec2_t v) {
    return sqrt(v.x * v.x + v.y * v.y);
}

double vec3_length(vec3_t v) {
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

vec2_t vec2_normalize(vec2_t v) {
    double len = vec2_length(v);
    if (len == 0.0) return v;
    return (vec2_t){ v.x / len, v.y / len };
}

vec3_t vec3_normalize(vec3_t v) {
    double len = vec3_length(v);
    if (len == 0.0) return v;
    return (vec3_t){ v.x / len, v.y / len, v.z / len };
}
