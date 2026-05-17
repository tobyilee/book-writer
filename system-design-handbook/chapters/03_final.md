# 3장. 캐시 — 거의 모든 시스템의 첫 번째 latency 무기

production Redis를 한 번이라도 `FLUSHDB` 해본 적이 있다면, 그 다음 1분 동안 무슨 일이 벌어졌는지 생생하게 떠오를 것이다. DB CPU가 100%를 찍고, p99 latency가 30초로 솟구치고, 알람이 도미노처럼 울린다. 그 와중에 누군가 사색이 된 얼굴로 "혹시 캐시 비웠어요?"라고 묻는다. 우리는 한참 뒤에야 "네"라고 답하고, 그 뒤로 한 시간쯤 회의실에서 무언가를 적게 된다.

캐시는 무기다. 같은 쿼리를 1000번 다시 묻지 않게 해주고, DB와 origin(원본 서비스)이 평소의 1/10 부하로 살게 해준다. 그런데 그 무기를 잘못 잡으면 우리 손에서 폭발한다. 캐시 하나를 비웠다는 단 한 줄의 작업이, 1분 안에 전체 서비스를 멈춰 세울 수 있다. 이 양면성이 캐시라는 부품을 흥미롭게 만든다.

그래서 캐시는 두 모양을 한꺼번에 머릿속에 그려야 다룰 수 있는 부품이다. 한쪽은 **잘 작동할 때의 모양** — 어떤 위치에 어떤 패턴으로 두면 latency가 얼마나 줄어드는지. 다른 한쪽은 **망가질 때의 모양** — thundering herd, cache stampede, 일관성 깨짐 같은 사고가 어떻게 cascading failure로 번지는지. 그 두 모양이 같이 떠올라야 비로소 캐시를 두려움 없이 잡을 수 있다.

## 캐시의 위치 — origin부터 client까지 6단

캐시가 어디에 있느냐는 질문에 대한 가장 흔한 답은 "Redis"다. 그런데 사실 그건 분산 캐시 한 종류일 뿐이고, 시스템 안에는 origin에서 client까지 가는 길에 캐시가 무려 여섯 군데쯤 깔려 있다. 이 6단 지형도를 한 번 그려 보자.

| 단 | 위치 | 대표 도구 | 평균 latency | 보호 대상 |
|----|------|----------|------------|----------|
| 1 | DB internal cache | Postgres buffer pool, MySQL InnoDB buffer pool | 1~10μs | disk IO |
| 2 | App in-process cache | Caffeine, Guava (Java), `lru-cache` (Node) | 100ns~1μs | DB query |
| 3 | 분산 캐시 | Redis, Memcached | 200μs~2ms | DB, upstream service |
| 4 | Reverse proxy cache | NGINX, Varnish | 1~5ms | app server |
| 5 | CDN edge cache | Cloudflare, CloudFront, Akamai | 5~50ms | origin (전 세계 분산) |
| 6 | Client cache | browser HTTP cache, mobile local DB | 0ms (네트워크 자체 안 탐) | 모든 backend |

이 6단을 한 번에 다 깔라는 얘기는 아니다. 시스템마다 어디까지 필요한지가 다르다. 사내 admin 도구는 1·2단만으로 충분하고, B2B SaaS는 보통 1·2·3단까지 깐다. B2C 글로벌 서비스는 4·5·6단까지 다 깔린다. 그런데 어느 단을 깔든 한 가지 원칙은 공통이다 — **caching closer to the user is always cheaper**. 사용자에 가까울수록 적은 자원으로 큰 latency 단축이 일어난다.

그래서 이 책에서 가장 깊이 짚을 단은 2단과 3단이다. CDN(5단)은 7장에서 따로 다루고, DB buffer pool(1단)은 1장에서 이미 잠깐 만났다. 우리가 매일 코드를 짤 때 가장 직접 손대는 두 단이 2단과 3단이고, 사고도 그 두 단에서 가장 자주 난다.

## Cache-aside vs read-through vs write-through vs write-back — 4가지 패턴

캐시와 origin 사이의 데이터 흐름을 어떻게 묶느냐에 따라 4가지 표준 패턴이 갈린다. AWS Caching Whitepaper가 가장 깔끔하게 정리한다.

> A cache-aside cache is updated after the data is requested. A read-through cache updates itself. (AWS, *Database Caching Strategies Using Redis*)

이 한 줄 안에 핵심 차이가 다 들어 있다. 한 번씩 짚어 보자.

### 패턴 1. Cache-aside (가장 흔한 default)

app이 직접 캐시를 들고 있는 가장 단순한 모양이다.

```
read:
  data = cache.get(key)
  if data is None:
      data = db.query(key)
      cache.set(key, data, ttl=300)
  return data

write:
  db.update(key, value)
  cache.delete(key)  # 또는 cache.set(key, value)
```

읽을 때는 캐시를 먼저 보고, 없으면 DB에서 채워 캐시에 박는다. 쓸 때는 DB를 먼저 쓰고, 캐시는 invalidate(삭제) 또는 update한다. 이 모양이 가장 흔한 이유는 단순하기 때문이다. app만 알면 되고, 캐시 layer는 그냥 멍청한 key-value store로 두면 된다.

대신 두 가지 함정이 있다. **첫째, cache miss 시점에 DB로 부하가 몰린다.** 캐시가 없으면 모든 read가 DB로 간다. 둘째, **write 시점에 캐시와 DB 사이의 일관성이 깨질 수 있다.** DB는 업데이트됐는데 캐시 invalidate가 실패하면? 또는 그 사이 다른 요청이 옛 값을 캐시에 다시 박으면? 이 경계의 모양을 그려 두는 게 중요하다.

### 패턴 2. Read-through (캐시가 origin을 알고 있다)

```
read:
  return cache.get_or_load(key, loader=lambda: db.query(key))
```

캐시 자체가 loader 함수를 알고 있어서, miss가 나면 알아서 origin에서 채워 온다. 코드가 더 깔끔하지만, 캐시 layer가 origin에 대한 의존성을 직접 갖는 단점이 있다. AWS DAX(DynamoDB Accelerator), 일부 Hibernate L2 cache 구현이 이 모양이다.

### 패턴 3. Write-through (쓸 때마다 캐시도 같이)

```
write:
  cache.set(key, value)
  db.update(key, value)
```

쓸 때 캐시와 DB를 같이 쓴다. 일관성은 좋아지지만, **write가 두 군데로 가니 write latency가 늘고, 절대 안 읽힐 값까지 캐시에 쓴다.** read-heavy + write-light + 일관성 중요 시스템에 적합하다.

### 패턴 4. Write-back / Write-behind (쓸 때는 캐시만, 나중에 DB)

```
write:
  cache.set(key, value, dirty=True)
  # background worker가 일정 주기로 DB에 sync
```

write latency가 가장 짧다. 그런데 dirty data가 캐시에 있을 때 캐시 노드가 죽으면 **데이터가 사라진다.** Redis cluster의 일부 운영 모드가 이 모양을 흉내내지만, 진짜 write-back은 좀처럼 안 쓴다. 너무 위험하다.

> 💡 이 4가지 패턴을 한 줄로 요약하면 이렇다.
> - Cache-aside = 일반적, 단순, 일관성은 약함
> - Read-through = 코드 깔끔, 캐시 layer가 origin 알아야 함
> - Write-through = 일관성 좋음, write 비쌈
> - Write-back = write 빠름, 데이터 손실 위험
>
> 처음 시스템 짤 때는 거의 cache-aside로 시작하고, 일관성이 절박해질 때만 write-through로 옮기는 편이 낫다.

## Redis vs Memcached — 무엇을 어떻게 가르나

분산 캐시 후보로 가장 자주 거론되는 둘이 Redis와 Memcached다. "Redis"라고 답하는 사람이 90%이지만, Memcached도 여전히 유효한 도구다. 두 선택지의 trade-off를 한 표로 정리하자.

| 차원 | Redis | Memcached |
|------|-------|-----------|
| 자료구조 | string, hash, list, set, sorted set, stream, bitmap, geo | string only |
| persistence | RDB snapshot + AOF (선택) | 없음 (in-memory only) |
| eviction | allkeys-lru, allkeys-lfu, volatile-lru, allkeys-random, ... 6개 정책 | LRU only |
| replication | primary-replica, Cluster mode (sharding 내장) | 없음 (client-side sharding) |
| persistence 옵션 | RDB + AOF, durable cache 가능 | 순수 cache |
| 성능 (단일 노드) | 매우 빠름, 자료구조 op 풍부 | 더 빠름 (단순함) |
| 메모리 효율 | overhead 있음 | 효율 좋음 |
| pub/sub, scripting | Lua scripting, pub/sub, transaction | 없음 |
| 분산 lock, rate limit | Redlock(논쟁), counter, ... 도구로 활용 가능 | 어려움 |

이 표를 보면 두 도구의 위치가 자연스럽게 드러난다. **Memcached는 "순수 캐시"이고, Redis는 "캐시이자 자료구조 서버"다.** 한 줄 캐시만 필요하면 Memcached가 더 빠르고 메모리도 적게 쓴다. 하지만 sorted set으로 leaderboard를 만들거나, list로 작업 큐를 흉내내거나, pub/sub으로 가벼운 메시징을 하거나, Lua로 atomic operation을 짜야 한다면 Redis로 가는 편이 낫다.

한국 백엔드에서는 거의 Redis가 표준이다. 데이터 구조의 풍부함, persistence option, Sentinel·Cluster의 운영 성숙도, 한국 운영 도구·문서의 양 등 이유는 많다. 새 시스템이라면 일단 Redis로 시작해서, 메모리 효율이 정말 부족할 때만 Memcached 검토하는 편이 낫다.

> 한 가지 주의 사항. Redis는 **single-threaded**다. (정확히는 background thread가 일부 있지만, command 실행은 한 스레드.) 그래서 `KEYS *`, `SMEMBERS bigset` 같은 O(N) 명령은 1초 이상 걸릴 수 있고, 그동안 다른 모든 요청이 막힌다. production에서 `KEYS`를 치지 말자 — 이 한 가지 규칙만으로 한국 백엔드에서 흔한 Redis 사고의 절반을 막을 수 있다. 대신 `SCAN`을 쓰자.

## Cache stampede — 같은 키를 1000개의 요청이 동시에 미스할 때

이제 가장 자주 망가지는 모양을 보자. **cache stampede** 또는 **thundering herd**라 부르는 현상이다. 영어로는 "성난 떼"라는 뜻인데, 한 번 겪어 보면 그 이름이 왜 붙었는지 절감하게 된다.

상황을 가정해 보자. 우리 서비스에 "지금 인기 상품 Top 10"이라는 캐시 키가 있다고 하자. 5분마다 갱신되도록 TTL이 300초로 박혀 있다. 1초에 1000개 요청이 이 캐시를 본다. 평소에는 1000개 모두 캐시 hit으로 끝나서, DB로 가는 부담은 거의 0이다.

그런데 0초에 캐시가 만료되는 순간 무슨 일이 벌어질까? 1초에 1000개 요청이 동시에 캐시 miss를 받는다. 1000개 요청이 모두 DB에 같은 쿼리를 던진다. DB는 평소 1초에 0~1개 받던 쿼리를 1000개 받는다. 첫 번째 요청이 결과를 받아와 캐시에 박을 때까지 다른 999개도 같은 쿼리를 처리하느라 DB는 CPU 100%로 비명을 지른다.

이게 thundering herd다. 그리고 단 한 키가 아니라 **여러 인기 키가 비슷한 시각에 동시 만료**되는 패턴이 가장 끔찍하다. 카카오 if(kakao) 2021 발표(검증 필요)에서 비슷한 결의 회고가 등장한다 — "single key TTL 동시 만료가 가장 무섭다"는 결. 새벽 0시·1시·5분 정각처럼 의외로 한국 백엔드의 일상 어디에든 깔려 있는 자리다.

같은 결의 사고가 한 가지 더 있다. **cache flush 직후의 cold cache(차가워진 캐시 — 데이터가 비어 있는 상태).** 운영자가 디버깅 중에 `FLUSHDB`나 `FLUSHALL`을 친 직후, 모든 키가 한 번에 사라진다. 그 다음 1분 동안 모든 요청이 cache miss로 origin에 직격탄을 날린다. Cloudflare 사내 블로그의 한 일화가 그대로다 — "We cleared our Redis to fix a bug and brought down origin for 20 minutes."

그렇다면 어떻게 막을까? 세 가지 패턴이 한국·해외 백엔드에서 정착되어 있다.

### 방어 1. Jittered TTL — 만료 시각을 랜덤으로 흩어 놓는다

가장 단순한 방어다. TTL을 그냥 300초로 박지 말고, "300초 + 0~60초 사이 랜덤"으로 박는다.

```python
import random

def set_with_jitter(cache, key, value, base_ttl=300, jitter=60):
    ttl = base_ttl + random.randint(0, jitter)
    cache.set(key, value, ttl=ttl)
```

이 한 줄이 모든 키의 만료 시각을 한 번에 몰리지 않게 흩어 놓는다. 우아한형제들이 배민 캐시 운영에서 "jittered TTL + lazy refresh"를 정착시킨 이유가 이거다. 가장 쉽고 효과가 큰 1차 방어선이다.

### 방어 2. Singleflight / Request Coalescing — 같은 키 요청을 하나로 합친다

같은 키에 대해 동시에 들어온 요청들을 한 번의 origin 호출로 묶는 패턴이다. Go의 `golang.org/x/sync/singleflight`이 표준 구현이다.

```go
var group singleflight.Group

func GetTopProducts(ctx context.Context) ([]Product, error) {
    v, err, _ := group.Do("top-products", func() (any, error) {
        // 이 함수는 같은 키에 대해 동시에 한 번만 실행됨
        return db.QueryTopProducts(ctx)
    })
    if err != nil { return nil, err }
    return v.([]Product), nil
}
```

캐시가 miss 났을 때, 100개의 요청이 모두 같은 key의 loader를 호출하더라도 group이 한 번만 실행하고 나머지는 그 결과를 공유한다. Java 진영에서는 Caffeine의 `LoadingCache.get(key, loader)`이 기본으로 이 모양을 보장한다. Discord의 chat 메시지 캐싱에서도 같은 패턴이 쓰인다 — request coalescing.

### 방어 3. Probabilistic Early Expiration — 만료 전에 미리 갱신한다

Vasilis Vasilakos의 2015년 논문 "Optimal Probabilistic Cache Stampede Prevention"이 제안한 우아한 방법이다. 핵심 아이디어는 이렇다.

> 만료에 가까워질수록 확률적으로 미리 갱신해 두면, 동시 만료가 일어날 확률이 거의 0이 된다.

수식으로는 이렇다. expiry time `t_e`, 현재 시각 `t_now`, 갱신에 걸리는 시간(beta로 표현)을 알 때, 다음 조건이 참이면 갱신한다.

```
delta * beta * ln(random()) >= t_e - t_now
```

복잡해 보이지만, 직관은 단순하다. "만료 직전에 가까울수록, 확률적으로 누군가 한 명이 미리 갱신하게 만든다." 모든 요청이 정확히 만료 시각에 동시에 miss를 받지 않게 흩어 놓는다.

Redis 자체적으로 이걸 해주진 않지만, app 단에서 한 줄 추가로 구현할 수 있다. 한국 백엔드에서는 토스·우아한형제들이 이 패턴을 일부 hot key에 적용한다는 사례가 발표에 등장한다.

### 방어 정리 — 어느 방어선부터 깔까

세 방어선 중 어느 것부터 깔아야 하는가? 보통 다음 순서가 합리적이다.

1. **jittered TTL을 모든 캐시에 default로 깔자.** 한 줄짜리 코드 변경으로 가장 큰 효과.
2. **hot key 또는 long-running loader가 있는 곳에 singleflight를 추가하자.** request coalescing 효과가 크다.
3. **만료 패턴이 정말 critical하다면 probabilistic early expiration까지 검토하자.** 코드 복잡도가 늘지만 가장 견고하다.

이 셋을 다 깔아도 막을 수 없는 사고가 하나 더 있다. cache layer 자체가 멈출 때. Redis primary가 죽거나 Cluster의 한 shard가 split-brain에 빠지면, 그 사이 모든 요청이 origin으로 직격탄을 날린다. 이 경우엔 캐시 패턴이 아니라 **circuit breaker**가 답이다 — 캐시가 일정 시간 응답이 없으면 origin 호출 자체를 차단해 cascade를 막는다. 이 패턴은 10장 멱등성·재시도·서킷 브레이커 챕터에서 자세히 다룬다.

## Eviction — 메모리가 가득 찰 때 무엇을 버릴 것인가

캐시는 본질적으로 **유한한 메모리**다. 새 데이터를 넣으려면 옛 데이터를 버려야 한다. 어느 키를 버릴지 결정하는 정책이 eviction이다. Redis는 6가지 정책을 제공하는데, 자주 헷갈리니 한 번 정리하자.

| 정책 | 무엇을 버리는가 | 언제 쓰나 |
|------|----------------|---------|
| `noeviction` | 안 버림, write 실패 시킴 | 캐시가 손실되면 데이터 자체가 사라지는 경우 (사실상 storage 용도) |
| `allkeys-lru` | 모든 키 중 가장 안 쓰인(LRU) 것 | 일반 캐시. 가장 무난한 default |
| `allkeys-lfu` | 모든 키 중 가장 적게 쓰인(LFU) 것 | 일부 키만 극단적으로 hot한 access 패턴 |
| `allkeys-random` | 무작위 | 모든 키가 거의 균등하게 쓰일 때 |
| `volatile-lru` | TTL 있는 키 중 LRU | TTL 없는 키는 절대 안 버려야 할 때 |
| `volatile-ttl` | TTL이 가장 빨리 만료되는 키 | 만료가 의미 있는 데이터일 때 |

가장 무난한 default는 `allkeys-lru`다. 대부분의 access 패턴은 "최근에 쓴 게 곧 또 쓰일" 가능성이 높다는 LRU 가정에 부합한다. 그런데 access 패턴이 명확히 다르면 LFU가 더 좋을 수 있다. 예를 들어 인기 상품 Top 100 같은 키는 매우 자주 쓰이는데, 잠깐 안 쓰였다고 LRU로 밀려나면 다음 access에서 cache miss가 난다. 이런 경우 LFU가 적합하다.

`noeviction`을 default로 두면 끔찍한 일이 일어난다. Redis가 메모리 한계에 도달하면 모든 write가 OOM 에러로 실패한다. session·rate-limit·queue를 Redis로 쓰는 시스템이라면, 어느 날 갑자기 로그인이 안 되고 API가 5xx로 떨어지는 사고가 날 수 있다. 그래서 `maxmemory-policy`는 항상 `allkeys-lru` 또는 `allkeys-lfu`로 시작하는 편이 낫다.

> 💡 운영 팁 — Redis 메모리는 80%를 임계치로 잡자. `maxmemory`를 instance 메모리의 75~80%로 설정하고, 90%를 넘으면 alert을 띄우자. Redis가 메모리 한계에 가까워지면 fragmentation·eviction·persistence가 모두 느려져 latency가 폭증한다.

## Multi-tier cache — L1 in-process + L2 분산

큰 시스템이 되면 분산 캐시(L2) 위에 in-process 캐시(L1)를 한 단 더 깔게 된다. L1은 app 프로세스 안의 메모리고, L2는 Redis다.

```
read:
  data = local_cache.get(key)
  if data is None:
      data = redis.get(key)
      if data is None:
          data = db.query(key)
          redis.set(key, data, ttl=300)
      local_cache.set(key, data, ttl=10)  # 짧게
  return data
```

L1 hit이면 1μs 이내, L2 hit이면 1ms, miss면 100ms+ — 이런 3단 계층이 만들어진다. Java에서는 **Caffeine**이 표준이고, Node에서는 `lru-cache`나 `lru-cache-fp`가 흔하다. Caffeine은 W-TinyLFU 알고리즘으로 LRU보다 hit rate가 높은 것으로 알려져 있다.

L1 캐시의 장점은 두 가지다. **첫째, 가장 빠르다.** Redis는 네트워크 호출이 끼지만 L1은 같은 프로세스 메모리다. 둘째, **Redis 트래픽을 줄여 비용·부하를 낮춘다.** Redis가 1초에 100만 op을 처리한다면, 그 절반을 L1이 흡수해 주는 식이다.

대신 단점도 있다. **일관성이 어려워진다.** Redis는 한 곳이라 invalidate가 정확하지만, L1은 모든 app instance에 다 있다. 한 사용자가 자기 데이터를 수정했는데, 다른 instance의 L1 캐시에는 옛 값이 5~10초 동안 남아 있을 수 있다. 그래서 L1은 **TTL을 매우 짧게(보통 5~30초)** 잡거나, **거의 안 변하는 데이터(설정, lookup 테이블)에만** 쓰는 편이 낫다. 또는 분산 invalidation pub/sub을 깔아 한 instance가 update 시 모든 instance에 invalidate를 broadcast하는 패턴도 있는데 — 일관성 절에서 다시 만난다(Facebook TAO의 두 단계 invalidation). 다만 복잡도가 빠르게 늘어, 신중하게 짚어 보는 편이 낫다.

## 한국 사례 — 카카오·우아한형제들의 캐시 운영 패턴

해외 사례만 봐서는 우리 일상이 잘 안 보인다. 한국 백엔드의 두 가지 대표 발표를 짚어 보자.

### 카카오 if(kakao) 2021 — "트래픽 폭증과 캐시 정책"

카카오톡은 새해·설날·발렌타인데이·어버이날 같은 정기 이벤트에서 평소의 수십 배 트래픽을 받는다. 광고는 점심·퇴근 시간에 spike가 친다. 그러니 캐시 정책의 모양이 매일이 다르다.

발표의 핵심 메시지 중 하나는 "single key TTL 동시 만료가 가장 무서웠다"였다. 단일 hot key가 만료되는 순간 thundering herd가 터지는 패턴을 여러 차례 겪었고, jittered TTL + 일부 hot key는 background refresh로 갱신하는 형태로 정착시켰다. 그리고 한 가지 더 — 캐시 클러스터를 **트래픽 유형별로 분리**해 두었다. 광고 캐시가 폭증해도 메시지 캐시는 영향 받지 않게.

### 우아한형제들 — 배민 캐시 운영 전략

배민 techblog과 우아콘에서 여러 번 다뤄진 패턴이다. 핵심을 한 줄로 줄이면 "hot key는 lazy refresh + jittered TTL"이다.

```java
@Cacheable(value = "popularStores", key = "#regionId")
public List<Store> getPopularStores(Long regionId) {
    // ...
}

// 별도 스케줄러가 만료 직전에 미리 갱신
@Scheduled(fixedDelay = 30000)
public void refreshPopularStores() {
    for (Long regionId : getActiveRegions()) {
        cache.put("popularStores::" + regionId, query(regionId));
    }
}
```

기본 캐시는 TTL 5분 + jitter, 그리고 인기 keys는 별도 스케줄러가 매 30초 background refresh를 돌린다. 사용자 요청은 항상 hit하고, 갱신은 보이지 않는 곳에서 일어난다.

이 패턴이 가능한 이유는 **"인기 keys"가 미리 알려져 있기 때문**이다. 모든 keys를 백그라운드로 갱신할 수는 없다. hit rate 분석 도구로 상위 N개를 골라 그 키들만 별도 워크플로로 묶는다. 이런 운영 관점의 디테일이 발표에서 강조되는 이유다.

## Callback 예고 — 17장 피드 시스템의 fanout cache

캐시는 17장 피드·타임라인 챕터에서 다시 만난다. Twitter·Instagram이 fanout-on-write로 home timeline을 만들 때, 각 사용자의 timeline 자체가 Redis 안의 sorted set으로 캐시된다. follower가 1만 명인 셀럽 한 명의 트윗 한 개가 만 개의 cache write를 만든다. 이 패턴을 "fanout cache"라 부르며, 단순 read-cache와는 다른 의사결정이 필요하다.

그 챕터에서는 어떤 key를 어떤 size로 어떻게 TTL 박는지, 셀럽 예외(fanout-on-read)는 어떻게 가르는지를 깊게 본다. 지금 챕터에서 배운 패턴(jittered TTL, singleflight, eviction)이 그 위에 그대로 얹힌다. **빌딩 블록이 곧 패턴의 재료가 된다는 사실**이 책 전체를 통해 반복되는 메시지다.

## 일관성 — "캐시는 결국 stale data를 견디는 layer다"

캐시를 깐다는 결정은 곧 **"일관성을 일부 양보하겠다"는 결정**이다. DB에 새 값이 쓰였는데 캐시는 아직 옛 값을 들고 있을 수 있다. 이 시차를 얼마나 견딜 수 있느냐가 캐시 도입 자격의 첫 번째 질문이다.

가장 흔한 패턴은 TTL 기반이다. "5분이면 stale data가 사라진다"는 약속으로 일관성을 흉내낸다. 90%의 도메인은 5분 stale을 견딜 수 있다. 인기 상품 목록, 카테고리, 메뉴 — 이런 데이터는 5분 늦어도 큰 문제가 없다.

그런데 견딜 수 없는 도메인이 있다. **결제 정보, 잔고, 권한, 재고**. 이런 데이터를 캐시한다는 결정은 매우 신중해야 한다. 잔고가 stale이면 사용자가 이미 다 쓴 돈을 또 쓸 수 있다. 권한이 stale이면 해고된 사용자가 한동안 접근 가능하다. 재고가 stale이면 0개 남은 상품을 100명에게 팔게 된다. 끔찍한 일이다.

이 경우 두 가지 선택지가 있다. **첫째, 캐시 자체를 깔지 않는다.** 잔고는 매번 DB에서 읽는다. 둘째, **invalidation을 강력하게 한다.** write 시 캐시를 동기로 invalidate하고, 캐시 invalidate가 실패하면 write도 롤백한다. 그러면 결국 캐시 layer가 critical path에 들어와, 캐시 장애가 곧 service 장애가 된다. 이 trade-off를 짊어질 만한 도메인이라면 그렇게 하는 편이 낫고, 아니라면 차라리 캐시를 안 까는 편이 낫다.

그리고 한 가지 더 — **"두 단계 invalidation"** 패턴이 있다. Facebook의 TAO 시스템이 정착시킨 패턴인데, write는 두 단계로 처리한다. (1) DB에 쓰고, (2) Kafka에 invalidate 이벤트를 발행한다. invalidate consumer가 모든 캐시 instance(L1·L2)에서 그 키를 지운다. 이렇게 하면 일관성이 좀 더 강해지지만, 캐시 invalidation의 latency가 늘고 시스템 복잡도가 커진다. 한국에서는 카카오 일부 광고 시스템, 네이버 일부 추천 시스템이 비슷한 패턴을 쓴다고 알려져 있다.

이 모든 trade-off의 결론은 한 가지다 — **"이 데이터를 캐시할 자격이 있는가"를 도메인별로 묻는 습관을 기르자.** 모든 데이터를 default로 캐시하면 빠르긴 하지만, 어느 날 stale data가 사고로 번진다. 도메인별로 stale 허용 시간을 미리 정해 두는 편이 낫다.

## 운영 모니터링 — 캐시 대시보드 7가지

마지막으로, 캐시를 production에서 운영하는 동안 항상 띄워두면 좋은 지표 7가지를 정리하자.

| # | 지표 | 의미 | 위험 임계 |
|---|------|------|----------|
| 1 | hit ratio (hits / (hits + misses)) | 캐시 효용 | 90% 미만이면 패턴 재검토 |
| 2 | latency p50·p99 | 캐시 응답 분포 | p99가 p50의 10배 이상이면 slow command 의심 |
| 3 | memory usage (%) | 메모리 압박 | 80% 넘으면 ramp-up 검토 |
| 4 | evictions / sec | 메모리 부족으로 강제 만료 | 0이 정상, 0보다 크면 의심 |
| 5 | network bandwidth | I/O 포화 | 80% 넘으면 의심 |
| 6 | connected_clients | 연결 수 | 비정상 증가 시 connection leak 의심 |
| 7 | slow log count | O(N) 명령 발생 | 0 외에 한 건이라도 보이면 즉시 확인 |

이 7가지를 한 화면에 띄워 두면, 새벽에 alert가 울려도 어느 지표를 가장 먼저 봐야 하는지가 명확해진다. 특히 **hit ratio**는 캐시 전체의 건강 척도다. hit ratio가 평소 95%였는데 갑자기 70%로 떨어졌다면, 누군가 캐시를 비웠거나, 캐시 layer가 부분 장애 상태이거나, 또는 access 패턴이 바뀐 것이다. 어느 쪽이든 즉각적인 조사가 필요하다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 캐시라는 무기의 양면이 손에 잡혀 있다. 4가지 패턴(cache-aside·read-through·write-through·write-back), Redis와 Memcached의 갈림, eviction 정책, multi-tier 계층, 그리고 망가질 때의 모양 — thundering herd·cold cache·stale data. 한국 백엔드의 카카오·우아한형제들 발표에서 정착된 jittered TTL + lazy refresh + 트래픽 격리 패턴까지가 한 묶음이다.

기억해두자. 캐시는 가장 흔하게 깔지만, 가장 자주 우리를 배신하는 부품이다. "왜 캐시를 깔까"보다 "캐시를 까는 자격이 우리 도메인에 있는가"를 먼저 묻는 편이 낫다. 그리고 한 번 깔았다면, 잘 작동할 때의 모양만큼 망가질 때의 모양도 머릿속에 그려두자. 새벽 한 시에 그 그림이 우리를 살린다. 그리고 그 그림이 머릿속에 자동으로 펼쳐질 때, 우리는 "캐시를 안다"고 말할 자격이 있는 백엔드 개발자가 되어 있다.

다음 장에서는 캐시와 함께 비동기 시스템의 양대 부품인 메시지 큐를 살펴본다. Kafka·RabbitMQ·SQS의 trade-off를 한 장의 표로 그리는 작업, 그리고 "lag가 4시간"이라는 sound조차 낯설지 않게 만드는 운영 함정들을 짚어 보자. 그곳에서도 우리는 같은 질문을 마주하게 된다 — "이 부품을 도입할 자격이 우리 팀에 있는가."
