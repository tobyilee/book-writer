/* mini.h — freestanding C에서 직접 만들어 쓰는 작은 표준 함수들.
 *
 * 호스트 환경에서는 string.h 한 줄이면 끝나는 일이지만,
 * `-ffreestanding -nostdlib`로 빌드하는 베어메탈 환경에서는
 * 누군가 직접 짜야 한다 — 그 "누군가"가 우리다.
 */
#ifndef MINI_H
#define MINI_H

#include <stddef.h>
#include <stdint.h>

/* 한 바이트로 dest 영역을 채운다. memset과 동일한 의미.
 * 베어메탈 부팅 직후 .bss를 0으로 미는 데 쓰인다. */
void *mini_memset(void *dest, int value, size_t n);

/* src에서 dest로 n바이트를 복사. memcpy와 동일.
 * 두 영역이 겹치면 결과는 미정의. */
void *mini_memcpy(void *dest, const void *src, size_t n);

/* a와 b의 앞 n바이트를 비교. memcmp와 동일.
 * 같으면 0, a가 크면 양수, b가 크면 음수. */
int   mini_memcmp(const void *a, const void *b, size_t n);

/* NUL 종결 문자열의 길이. strlen과 동일 — O(n). */
size_t mini_strlen(const char *s);

/* 두 문자열 비교. strcmp와 동일.
 * NUL을 만날 때까지 한 바이트씩 비교, 같으면 0. */
int    mini_strcmp(const char *a, const char *b);

/* 부호 없는 정수를 10진수 문자열로 출력 버퍼에 쓴다.
 * buf는 최소 21바이트 (uint64_t의 최대 자릿수 + NUL) 권장.
 * 리턴값: 쓴 바이트 수 (NUL 제외). */
size_t mini_u64_to_dec(uint64_t value, char *buf, size_t cap);

#endif
