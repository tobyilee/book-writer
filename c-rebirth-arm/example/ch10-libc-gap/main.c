/* main.c — vec과 map을 사용해보는 데모.
 *
 * AddressSanitizer를 켜서 빌드하면 누수·use-after-free·범위 밖 접근이
 * 모두 잡힌다. `make` 한 줄에 ASan이 켜져 있으니 안심하고 만져 보자.
 */
#include "map.h"
#include "vec.h"

#include <assert.h>
#include <stdio.h>

static void demo_vec(void)
{
    printf("[vec] 동적 배열에 1..10을 밀어 넣어 본다.\n");
    vec_t *v = vec_create();
    assert(v);

    for (int i = 1; i <= 10; i++) {
        int rc = vec_push(v, i * i);
        assert(rc == 0);
    }

    printf("[vec] len=%zu, cap=%zu\n", vec_len(v), vec_cap(v));
    for (size_t i = 0; i < vec_len(v); i++) {
        int ok = 0;
        int val = vec_get(v, i, &ok);
        assert(ok);
        printf("[vec]   v[%zu] = %d\n", i, val);
    }

    /* 범위 밖 접근은 ASan이 아니라 vec_get 자체가 막아 준다 */
    int ok = 1;
    (void)vec_get(v, 999, &ok);
    assert(!ok);
    printf("[vec] out-of-range get은 ok=0으로 안전하게 거절된다.\n");

    vec_destroy(v);
    printf("[vec] vec_destroy 완료.\n\n");
}

static void demo_map(void)
{
    printf("[map] 단어 카운터를 만들어 본다.\n");
    map_t *m = map_create();
    assert(m);

    const char *words[] = {
        "apple", "banana", "apple", "cherry", "banana", "apple",
        "durian", "elder", "fig", "grape", "grape", "honeydew",
        "iceberg", "jackfruit", "kiwi", "lemon", "mango", "nectarine",
    };
    const size_t n = sizeof words / sizeof words[0];

    for (size_t i = 0; i < n; i++) {
        int count = 0;
        map_get(m, words[i], &count);
        map_put(m, words[i], count + 1);
    }

    printf("[map] 고유 단어 수 = %zu\n", map_len(m));

    int apple = 0, banana = 0, cherry = 0, missing = 0;
    assert(map_get(m, "apple", &apple) && apple == 3);
    assert(map_get(m, "banana", &banana) && banana == 2);
    assert(map_get(m, "cherry", &cherry) && cherry == 1);
    assert(!map_get(m, "missing", &missing));
    printf("[map]   apple=%d banana=%d cherry=%d missing(있나)=%s\n",
           apple, banana, cherry,
           map_get(m, "missing", &missing) ? "yes" : "no");

    /* 삭제 후 사슬이 깨지지 않는지 확인 */
    assert(map_del(m, "apple"));
    assert(!map_get(m, "apple", &apple));
    assert(map_get(m, "banana", &banana) && banana == 2);
    printf("[map] apple 삭제 후에도 banana는 멀쩡하다.\n");

    map_destroy(m);
    printf("[map] map_destroy 완료.\n");
}

int main(void)
{
    demo_vec();
    demo_map();
    printf("\n전부 통과. ASan이 침묵하면 누수도 없다는 뜻이다.\n");
    return 0;
}
