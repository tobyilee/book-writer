#include "geom.h"
#include <stdio.h>

int main(void) {
    vec2_t a = { 3.0, 4.0 };
    vec3_t b = { 1.0, 2.0, 2.0 };

    printf("|a| = %.3f\n", vec2_length(a));   /* 기대: 5.000 */
    printf("|b| = %.3f\n", vec3_length(b));   /* 기대: 3.000 */

    vec2_t na = vec2_normalize(a);
    printf("a/|a| = (%.3f, %.3f)\n", na.x, na.y);
    return 0;
}
