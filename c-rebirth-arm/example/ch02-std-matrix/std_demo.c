/*
 * std_demo.c — 2장. 어떤 표준에서도 통하는 공통분모
 *
 * C89부터 C23까지 다섯 표준 모두에서 빌드되어야 한다.
 * 같은 코드가 어디서나 도는 모습을 보면서, 표준 매트릭스 빌드의 출발점을 잡는다.
 */

#include <stdio.h>

static int square(int x) {
    return x * x;
}

int main(void) {
    int total = 0;
    int i;
    for (i = 1; i <= 5; i++) {
        total += square(i);
    }
    printf("sum of squares 1..5 = %d\n", total);
    printf("compiled with __STDC_VERSION__ = %ld\n",
#ifdef __STDC_VERSION__
           (long)__STDC_VERSION__
#else
           0L  /* C89에는 __STDC_VERSION__이 없을 수 있다 */
#endif
    );
    return 0;
}
