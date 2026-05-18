/*
 * 의도된 메모리 누수.
 *
 *   make leak && ./leak
 *
 * macOS Apple Silicon의 ASan은 LSan 모듈을 포함하지 않아서
 * "free 안 한 채로 끝나는" 종료 누수는 본 도구로 잡히지 않는다.
 * 대신 두 가지 보조 수단을 본문에서 소개한다 —
 *   (a) macOS 내장 `leaks --atExit -- ./leak`
 *   (b) Linux/QEMU 측 ASan + LSan
 * Apple 클랜의 출력에는 "detect_leaks is not supported"로 보인다.
 * 여기서는 의도된 누수 코드 패턴 자체를 익히는 데 집중한다.
 */

#include <stdio.h>
#include <stdlib.h>

static int *make_box(int v) {
    int *box = malloc(sizeof *box);
    if (!box) return NULL;
    *box = v;
    return box;
}

int main(void) {
    /* 100개 박스를 만들지만 free는 한 번도 안 한다. */
    for (int i = 0; i < 100; ++i) {
        int *b = make_box(i);
        (void)b;          /* 일부러 버린다 — 이게 누수다 */
    }
    printf("100개 박스를 만들고 단 한 번도 free하지 않았다.\n");
    printf("macOS에선 `leaks --atExit -- ./leak`이 잔량을 일러바친다.\n");
    return 0;
}
