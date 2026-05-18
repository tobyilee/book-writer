/*
 * 9장. 한 소스에 작은 버그 하나 — off-by-one read of stack array.
 *
 * 같은 파일을 ASan/UBSan/MSan/clang-tidy/clang-format 으로
 * 돌려 보면서 도구가 무엇을 어떻게 잡는지 비교한다.
 *
 * 의도된 버그:
 *   - sum_first_n(arr, 5) 호출인데 sum_first_n 안에서 i<=n 으로 잘못 짜
 *     arr[5] 를 읽는다(스택 배열 길이는 5, 인덱스 0~4 만 유효).
 *
 *   make asan        # ASan 으로 잡아 보기
 *   make ubsan       # UBSan 도 같이
 *   make msan        # MSan (clang 필수, macOS는 제한적)
 *   make clang-tidy  # 정적 분석
 *   make format      # clang-format 검사
 *   make scan        # scan-build (있을 때)
 *   make release     # sanitizer 끄고 빌드 — 침묵하는 걸 확인
 */

#include <stdio.h>

/* 일부러 잘못된 코드: i <= n. 정석은 i < n. */
static int sum_first_n(const int *arr, int n) {
    int s = 0;
    for (int i = 0; i <= n; i++) {     /* off-by-one */
        s += arr[i];
    }
    return s;
}

int main(void) {
    int arr[5] = {1, 2, 3, 4, 5};      /* 합은 15 */
    int s = sum_first_n(arr, 5);
    printf("sum = %d\n", s);
    return 0;
}
