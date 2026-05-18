/*
 * c23_only.c — 2장. C23에서만 빌드되는 기능 모음
 *
 * `nullptr` 키워드와 `_BitInt(N)`을 동시에 시연한다.
 * 이 파일을 `-std=c17` 이하로 빌드하면 컴파일 에러가 난다. 그 사실 자체가 교재다.
 *
 * 빌드:
 *   make c23-only         # C23으로만 빌드 (성공)
 *   make c23-only-as-c17  # 일부러 C17로 빌드 시도 (의도된 실패)
 */

#include <stdio.h>

/* `_BitInt(N)`은 임의 폭 정수를 만든다. 임베디드의 비트 필드에 직격이다. */
typedef _BitInt(8) byte_t;

static void greet(const char *who) {
    /* C23부터 `nullptr`이 정식 키워드다. NULL이 아니라 nullptr을 쓸 수 있다. */
    if (who == nullptr) {
        printf("(이름 없는 손님)\n");
        return;
    }
    printf("hello, %s\n", who);
}

int main(void) {
    greet("c23");
    greet(nullptr);

    byte_t b = 127;
    printf("_BitInt(8) 최댓값을 담은 변수: %d\n", (int)b);
    return 0;
}
