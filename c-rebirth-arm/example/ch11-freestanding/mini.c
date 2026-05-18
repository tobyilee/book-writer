/* mini.c — freestanding 작은 표준 함수들의 구현.
 *
 * 주의 1) 컴파일러가 memcpy/memset를 "내장 함수"로 인식해
 *       다른 코드의 빈 자리에서 자동으로 부르는 일이 있다.
 *       그래서 베어메탈 빌드에서는 보통 -fno-builtin을 같이 켜거나,
 *       이 함수들을 외부에서 콜할 수 있게 정의만 해 둔다 (지금 코드).
 *
 * 주의 2) freestanding 코드는 stdlib을 호출하지 않는다.
 *       오직 <stddef.h>, <stdint.h>, <stdbool.h> 같은
 *       타입·매크로 정의 헤더만 안전하다.
 */
#include "mini.h"

void *mini_memset(void *dest, int value, size_t n)
{
    unsigned char *p = (unsigned char *)dest;
    unsigned char  v = (unsigned char)value;
    for (size_t i = 0; i < n; i++) p[i] = v;
    return dest;
}

void *mini_memcpy(void *dest, const void *src, size_t n)
{
    unsigned char       *d = (unsigned char *)dest;
    const unsigned char *s = (const unsigned char *)src;
    for (size_t i = 0; i < n; i++) d[i] = s[i];
    return dest;
}

int mini_memcmp(const void *a, const void *b, size_t n)
{
    const unsigned char *x = (const unsigned char *)a;
    const unsigned char *y = (const unsigned char *)b;
    for (size_t i = 0; i < n; i++) {
        if (x[i] != y[i]) return (int)x[i] - (int)y[i];
    }
    return 0;
}

size_t mini_strlen(const char *s)
{
    size_t n = 0;
    while (s[n] != '\0') n++;
    return n;
}

int mini_strcmp(const char *a, const char *b)
{
    while (*a && (*a == *b)) { a++; b++; }
    return (int)(unsigned char)*a - (int)(unsigned char)*b;
}

size_t mini_u64_to_dec(uint64_t value, char *buf, size_t cap)
{
    if (cap == 0) return 0;
    if (value == 0) {
        if (cap < 2) return 0;
        buf[0] = '0';
        buf[1] = '\0';
        return 1;
    }

    /* 거꾸로 쌓아서 뒤집기 */
    char tmp[21];
    size_t i = 0;
    while (value > 0 && i < sizeof tmp) {
        tmp[i++] = (char)('0' + (value % 10));
        value /= 10;
    }
    if (i + 1 > cap) return 0; /* NUL 자리도 못 잡으면 실패 */

    size_t out = 0;
    while (i > 0) buf[out++] = tmp[--i];
    buf[out] = '\0';
    return out;
}
