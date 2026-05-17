# 8장. 시간·순서·분산 ID — 분산 시스템의 가장 어두운 코너

매년 봄과 가을, 트위터에는 같은 모양의 글이 한 번씩 올라온다고 해보자. "DST(서머타임) 전환 새벽 2시에 우리 cron이 두 번 돌았다", 혹은 "0번 돌았다." 글 아래에는 "또 시작이네"라는 댓글이 줄을 잇는다. 매년, 새로운 백엔드 개발자들이 똑같은 함정에 빠진다 — 시간은 단순해 보이지만 분산 시스템에서는 가장 어려운 질문 중 하나다.

"지금 몇 시야?" 같은 질문에 친구는 손목시계를 보고 답한다. 그런데 분산 시스템에서는 그 질문에 누구도 자신 있게 답하지 못한다. 노드마다 시계가 다 미세하게 어긋나 있고, GPS·atomic clock 같은 하드웨어가 없으면 그 어긋남을 안전하게 줄일 방법도 마땅치 않다. 그렇다면 무엇으로 시간을 대신할 것인가 — 그게 이 챕터의 출발점이다.

Lamport가 1978년에 시작한 사고 실험에서부터, Spanner의 TrueTime이 GPS와 원자시계를 데이터베이스 안으로 끌고 들어온 결정, NTP의 slew와 step이 Snowflake ID에 미치는 영향, 그리고 매년 우리를 흔드는 timezone hell까지 — 한 박자씩 짚어 가자. 마지막엔 한국 토스 SLASH 발표가 짚은 실무 디테일과, 흔히 도입되는 분산 lock(특히 Redis Redlock)의 논쟁점도 함께 본다.

## 1. Lamport의 1978년 — 시간을 인과로 다시 정의하기

분산 시스템에서 시간이 어려운 가장 근본 이유는 단순하다. **두 노드의 시계는 절대 정확히 같지 않다.** NTP가 잘 돌고 있어도 수 ms ~ 수십 ms의 어긋남(skew)이 있고, 데이터센터마다·rack마다 그 어긋남의 모양이 다르다. 그렇다면 노드 A에서 일어난 사건과 노드 B에서 일어난 사건의 "순서"는 어떻게 정의할까?

Lamport는 1978년 *Time, Clocks, and the Ordering of Events in a Distributed System*(P4)에서 이 문제를 정면으로 풀었다. 핵심 통찰은 한 줄이다 — **"실제 시간을 포기하자. 인과만 정의하자."**

이걸 happens-before(→) 관계라고 부른다. 한 노드 안에서 A가 B보다 먼저 일어났다면 A → B. 노드 A가 보낸 메시지를 노드 B가 받았다면, A의 send → B의 receive. 그 외의 사건들은 "concurrent" — 동시에 일어났다고 봐도 된다는 뜻이다. 이렇게 인과로 묶이는 사건들 사이에는 부분 순서(partial order)가 생긴다.

논문의 진가는 그 다음에 있다. Lamport는 happens-before를 보존하는 가장 간단한 시계 — **Lamport timestamp**를 제시했다. 각 노드가 카운터를 하나씩 들고, 이벤트가 일어날 때마다 +1, 메시지를 받을 때는 받은 timestamp와 자기 카운터 중 큰 값 + 1로 갱신한다. 이 단순한 규칙이 **"인과적으로 앞선 사건은 timestamp도 작다"는 성질**을 보장한다.

다만 Lamport timestamp의 한계도 분명하다. **timestamp가 작다고 인과적으로 앞선 것은 아니다.** 두 노드의 카운터가 우연히 같은 값이 될 수 있고, "동시"인 사건들의 순서는 임의로 정해진다. 이걸 더 정밀하게 잡으려면 **vector clock** — 각 노드가 N개 카운터를 들고 다니는 자료구조 — 가 필요하다. Vector clock은 인과를 정확히 잡지만, 노드 수에 비례해 메모리·네트워크 비용이 늘어난다. 그래서 production에서는 N이 10개 이하인 경우 외에는 잘 쓰지 않는다.

기억해 두자. **Lamport의 통찰은 "벽시계를 포기하자, 인과만 잡자"였다.** 이 시각 하나가 그 후 50년의 분산 시스템 이론을 지탱한다.

### Lamport timestamp가 부족한 자리 — 한 사례

Lamport timestamp만으로는 잡지 못하는 자리를 짧게 그려 보자. 노드 A에서 카운터가 5일 때 이벤트 X가 생기고, 노드 B에서 카운터가 5일 때 이벤트 Y가 생긴다. 두 사건은 인과적으로 무관하다. 그런데 Lamport timestamp만 보면 둘 다 5라서 "동시"라고 묶이거나, tie-breaker로 임의 순서가 매겨진다. 이게 진짜 인과적으로 동시인지, 아니면 그냥 카운터가 우연히 같은 값이 된 건지 — Lamport timestamp는 구별하지 못한다.

vector clock은 이 차이를 잡는다. 노드 A의 timestamp는 (A:5, B:0), 노드 B의 timestamp는 (A:0, B:5). 두 vector를 비교하면 어느 한쪽이 다른 쪽을 dominate하지 않는다 — 그래서 진짜 "concurrent"라고 판정할 수 있다. 정확하지만, 노드 수에 비례해 비용이 늘어난다는 함정이 따라온다. 메모리도, 네트워크도, 비교 연산도 모두 N에 비례한다. 그래서 production에서는 노드 수가 작거나 conflict 해소가 정말 중요한 자리(Dynamo의 vector clock, version vector)에만 쓰인다.

## 2. Hybrid Logical Clock — 두 세계의 타협

Lamport는 인과를 잡았고, NTP는 (불완전하나마) 벽시계를 동기화한다. 그런데 production에서는 둘 다 필요할 때가 많다. "사건의 인과적 순서가 맞아야 하는 동시에, 시계도 사람이 읽을 수 있게 사람의 시간과 가까워야 한다." 이 두 요구를 함께 만족하려는 게 **Hybrid Logical Clock (HLC)**다.

HLC는 단순하게 말하면 "Lamport timestamp의 카운터 자리에 NTP의 physical timestamp를 끼워 넣는다"는 발상이다. 각 노드는 (physical time, logical counter) 쌍을 timestamp로 쓴다. 보통은 physical time이 카운터처럼 작동하다가, NTP가 어긋나거나 같은 ms 안에 여러 이벤트가 발생하면 logical counter가 +1씩 늘며 차이를 보정한다.

CockroachDB가 HLC를 골랐다. 이유는 분명하다 — **GPS·atomic clock 같은 특수 하드웨어 없이도 글로벌 분산 SQL DB가 작동해야 했기 때문**이다. HLC는 commodity hardware + NTP만으로 굴러간다. 대신 uncertainty가 더 크다. NTP의 skew가 클수록 HLC의 정확도도 떨어진다.

HLC가 작동하는 모습을 한 줄로 그려 보자. 노드 A의 physical time이 100, logical counter가 0인 상태(100, 0). 같은 ms 안에 이벤트가 또 일어나면 (100, 1), (100, 2)로 logical counter만 늘어난다. 노드 A가 (100, 2) timestamp가 박힌 메시지를 노드 B로 보내고, 노드 B의 physical time이 마침 99 (NTP가 살짝 어긋남)였다면? 노드 B는 받은 (100, 2)와 자기 (99, 0) 중 큰 것 + 1로 갱신해 (100, 3)을 쓴다. 이렇게 **physical time이 비정상이어도 인과는 깨지지 않는다**는 보장을 만들어 낸다. 우아하다.

그렇다면 GPS와 atomic clock을 직접 데이터베이스 안에 박아 넣으면 어떻게 될까? 그게 Spanner의 답이다.

## 3. TrueTime — GPS와 원자시계를 DB 안으로

Google이 2012년 OSDI에 발표한 *Spanner: Google's Globally-Distributed Database*(P5)는 분산 DB 영역에 한 가지 충격적인 결정을 던졌다. **"우리 데이터센터마다 GPS 안테나와 atomic clock을 설치해, 시계 자체를 데이터베이스의 일부로 만든다."**

TrueTime API는 단순하다. `TT.now()`를 호출하면 단순한 timestamp가 아니라 `[earliest, latest]` 구간을 돌려준다. "현재 시간은 이 두 값 사이 어딘가에 있다"는 보장이다. 그 구간의 폭이 uncertainty ε인데, Google 발표 기준 ε는 보통 약 3ms 정도다 (외부 벤치마크가 없어 검증 필요).

이 작은 ε이 외부 일관성(external consistency)이라는 강력한 성질을 만들어 낸다. Spanner는 commit을 끝내기 전에 ε 만큼 기다린다 — "commit wait." 한 트랜잭션 T1이 timestamp `t1`로 commit되고 ε 동안 기다린 뒤, 다른 트랜잭션 T2가 시작하면 T2의 timestamp는 반드시 `t1`보다 크다. 즉 **글로벌하게 "시간상 나중에 commit된 트랜잭션은 timestamp도 나중"**이라는 강한 성질이 보장된다. 이게 글로벌 strong consistency의 비결이다.

DDIA를 다 읽었다고 해도, 동료가 어느 날 "우리 결제 시스템은 strong consistency가 필요한가?"라고 물으면 막힌다. 답은 책 안에 있지만, 책의 단어와 우리 회사의 단어가 다르기 때문이다. Spanner의 3ms commit wait이 우리에게 던지는 질문은 결국 한 줄이다 — "당신 시스템의 그 한 작업, 3ms를 더 기다려도 괜찮은가? 그 대가로 글로벌하게 인과가 보장되는가?"

대부분의 한국 백엔드 시스템은 이 질문에 "기다리지 않아도 된다"고 답한다 — 그래서 우리는 HLC나 Lamport timestamp나, 더 단순하게는 single-leader RDB의 transaction order만으로도 충분히 살 수 있다. 다만 **무엇을 양보했는지 알고 양보하는 것**이 시니어와 그렇지 않은 사람의 차이다.

## 4. NTP slew vs step — Snowflake ID가 죽는 자리

이제 한 박자 내려와서, 실무에서 매일 만지는 자리를 들여다보자. NTP(Network Time Protocol)는 시스템 시계를 외부 source(보통 stratum 1·2 서버)와 맞춰 주는 표준 도구다. 문제는 그 "맞추는 방식"에 두 가지가 있다는 것이다.

- **Slew (천천히 조정).** 시계가 어긋났을 때 단번에 점프하지 않고, 일정 시간 동안 조금씩 빠르게/느리게 흘려서 맞춘다. cron·timer·monotonic counter가 안전하다.
- **Step (한 번에 점프).** 시계가 너무 많이 어긋났을 때 (보통 0.5초 이상) 단번에 새 값으로 바꾼다. 빠르지만, 시계가 역행할 수 있다.

기본 NTP 데몬은 차이가 작으면 slew, 크면 step하는 hybrid를 쓴다. 문제는 step이 일어났을 때다. 시계가 역행하면 — 예컨대 03:00:01에서 02:59:59로 점프하면 — 그 사이에 만들어진 timestamp들이 같은 값 또는 역순이 된다.

이 함정은 Snowflake ID 같은 timestamp-prefix 분산 ID 생성기를 정면으로 흔든다. Twitter의 Snowflake ID 구조를 잠깐 풀어 보면 이해가 쉽다.

```
| 1 bit | 41 bit               | 10 bit       | 12 bit             |
| unused | timestamp (ms 단위) | machine ID  | per-ms sequence    |
```

41bit가 약 69년치 millisecond를 표현하고, 10bit machine ID로 1024개 노드, 12bit sequence로 같은 ms 안에 4096개 ID를 만들 수 있다. **충돌이 안 나는 비결은 시계가 단조 증가한다는 가정**이다. 시계가 1초 역행하면 그 1초 동안 같은 timestamp prefix + 같은 sequence 조합이 다시 나올 수 있어 **ID 충돌**이 발생한다. 운이 나쁘면 production DB의 primary key가 깨진다 — 한 번 겪고 나면 NTP 모니터링이 일상 도구가 된다.

방어법은 분명하다 — **slew만 쓰자**. NTP 데몬에서 step을 비활성화하거나, chrony 같은 모던 도구를 써 step 임계값을 매우 작게 잡는다. 그리고 ID 생성기 코드에 "마지막 timestamp보다 작으면 wait" 로직을 박아 둔다. 잠깐의 추가 latency가 ID 충돌보다는 백 배 낫다.

이 함정이 부록 A의 tribal knowledge 18선 중 첫 번째 항목으로 박힌 데는 이유가 있다. 만나본 사람과 만나보지 못한 사람이 새벽 alert에서 보이는 차이가 크기 때문이다. **NTP는 시계를 맞추지만, 잘못 설정된 NTP는 시계를 무기로 만든다** — 기억해 두자.

## 5. 분산 ID 한 자리에 모아 보기 — Snowflake·ULID·UUIDv7

분산 시스템에서 ID를 어떻게 만들지는 의외로 자주 마주치는 질문이다. RDB의 auto-increment는 single-leader가 아니면 못 쓰고, UUIDv4 같은 random ID는 정렬 가능성이 없어 인덱스 친화적이지 않다. 그렇다면 어떤 선택지가 있을까?

**Snowflake (Twitter, 2010).** 64-bit를 1(reserved) + 41(timestamp ms) + 10(machine ID) + 12(per-ms sequence)로 자른다. 약 3.5조 개의 ID를 시간 순으로 만들어 낸다. 정렬 가능 + 분산 + DB 인덱스 친화적이라는 세 가치를 한 자리에 잡았다. 단 NTP의 step에 취약하다는 함정이 따라온다.

**ULID (2016, Alizain Feerasta).** 128-bit. 앞 48-bit는 millisecond timestamp, 뒤 80-bit는 random. UUID와 동일한 크기이면서 시간 순서를 보장한다. Snowflake보다 충돌 방어가 강하고(80-bit random), machine ID 관리가 필요 없다.

**UUIDv7 (RFC 9562, 2024년 표준화).** 128-bit. ULID와 거의 같은 구조지만 UUID 표준 안에서 정의됐다. 기존 UUID 인프라(라이브러리·DB 컬럼 타입·문자열 표현)를 그대로 쓰면서 시간 정렬을 얻을 수 있다. 2024년 이후 새 프로젝트의 default로 자리 잡는 중이다.

세 가지를 짧은 비교 표로 정리해 보자.

| 축 | Snowflake | ULID | UUIDv7 |
|---|---|---|---|
| 크기 | 64-bit | 128-bit | 128-bit |
| Timestamp 정밀도 | 1ms | 1ms | 1ms |
| Machine ID 필요? | 필요 (10bit) | 불필요 (random) | 불필요 (random) |
| 표준 | Twitter 내부 + 사실상 | 커뮤니티 spec | RFC 9562 (공식) |
| DB 인덱스 친화도 | 매우 높음 | 높음 | 높음 |
| 문자열 표현 | 16진수 (긴 숫자) | 26자 Crockford base32 | 36자 UUID (표준) |
| NTP step 취약도 | 매우 높음 | 낮음 | 낮음 |

회의 자리에서 가장 자주 듣는 질문은 "그래서 뭐 쓸까?"다. 우리 답은 단순하다 — **64-bit가 꼭 필요하지 않다면(저장 비용·네트워크 비용 어쩌면 5% 차이가 진짜 critical하지 않다면) UUIDv7이 가장 안전한 default다.** 이유는 세 가지. ① 공식 RFC. ② UUID 인프라 그대로. ③ NTP step에 강하다. Snowflake는 machine ID 관리·NTP 모니터링이라는 두 운영 비용을 짊어진다는 점을 항상 기억해 두자.

## 6. Timezone Hell — 매년 봄·가을 반복되는 함정

이제 가장 일상적인 자리다. 한국에서 시스템을 만드는데, 사용자는 미국·일본·유럽에서도 접속한다고 해보자. 시간을 어떻게 저장하고 어떻게 보여줄까? 표준 답은 "DB에는 UTC로 저장, 표시는 사용자 timezone으로." 누구나 들어본 답이다. 그런데 이 한 줄에는 함정이 숨겨져 있다.

### 함정 1: legacy DB의 timestamp(timezone 없는 컬럼)

PostgreSQL이라면 `TIMESTAMP`와 `TIMESTAMPTZ`라는 두 자료형이 있다. 비슷해 보여서 처음에는 별 차이가 없을 거라고 생각하기 쉽다. 그런데 **`TIMESTAMP` (timezone 없음)는 "DB가 시간대를 기억하지 않는다"는 뜻**이다. KST로 넣었는지 UTC로 넣었는지 아무도 모른다. application 어딘가에서 가정이 깨지는 순간 모든 시간 데이터가 무의미해진다 — 끔찍한 일이다. 새 프로젝트라면 거의 항상 `TIMESTAMPTZ`를 쓰자.

### 함정 2: DST (서머타임) 전환

매년 봄과 가을, 미국·유럽·호주의 일부 지역에서 시계가 1시간 앞당겨졌다 다시 되돌아간다. 그 결과 — **새벽 2시가 두 번 등장하거나 한 번도 등장하지 않는다.** 이게 정확히 그 시간에 돌도록 잡혀 있는 cron job을 흔든다. "매일 새벽 2시 5분에 돌아라"라고 한 cron이 그날만 2번 또는 0번 돈다. 매년, 어딘가의 백엔드가 이걸로 알람을 받는다.

방어법은 두 가지. ① cron 표현을 "매일 2시 5분"이 아닌 "1시간 간격" 또는 "UTC 기준 시간"으로 바꾼다. ② DST가 없는 timezone(한국은 그 자체로 DST 없음)에 cron을 둔다. 그래도 미국 사용자에게 보여줄 시간이라면 application 레벨에서 timezone 변환을 해야 하니, 그 한 자리는 잘 테스트해 두자.

### 함정 3: 미래 일정은 local time으로 저장

이건 덜 알려진 함정이다. UTC 저장 + local 표시는 "과거 사건"에만 안전하다. **미래에 일어날 일정(예약·예약된 cron)은 정부가 timezone 규칙을 바꿀 수 있어서, UTC로 변환해서 저장하면 위험하다.** 예컨대 "2027년 3월 8일 새벽 2시에 알람"을 UTC로 저장해 두면, 그 사이에 미국 정부가 DST를 폐지하면 알람이 1시간 어긋난다. 미래 일정은 (`local time`, `timezone name`) 쌍으로 저장하고, 알람 시점에 변환하는 편이 낫다.

### 함정 4: leap second — 매 몇 년에 한 번 1초가 추가된다

마지막 함정 하나만 더. **leap second**는 지구 자전 속도가 미세하게 느려지는 걸 보정하려고 UTC에 1초를 추가하는 작업이다. 2012년·2015년·2016년·2017년이 가장 최근 사례들이고, 이때마다 일부 인터넷 서비스가 흔들렸다. 23시 59분 60초라는 한 번도 안 쓰는 시각이 등장하기 때문이다. 일부 라이브러리는 이걸 처리 못하고 죽고, 어떤 시스템은 시계를 step해서 NTP step 함정에 또 빠진다. 다행히 2035년부터 leap second가 폐지될 예정이라(검증 필요 — IERS 발표), 이 함정은 점차 사라질 거다. 다만 그때까지는 **leap second smearing**(Google·AWS가 채택한 12시간에 걸쳐 부드럽게 1초를 흘리는 기법)을 쓰는 NTP 서버를 골라 두는 편이 낫다.

### 한국 사례 — 토스 SLASH 22 "분산 시스템에서 시간 다루기"

이 timezone hell을 한국 백엔드 시각에서 가장 정직하게 짚은 발표가 있다. **토스 SLASH 22의 "분산 시스템에서 시간 다루기"**다. OKKY와 트위터에서 발표 후 "이게 가장 현실적인 발표였다"는 반응이 자주 인용된다(community 패턴 3).

발표는 한국 결제 시스템에서 만난 구체적 문제들을 짚는다. 일본 트래픽이 섞인 hourly job이 KST 기준과 JST 기준에서 3시간 다른 결과를 내는 사고, leap second(2016년·2017년)가 거래 timestamp에 미친 영향, 그리고 IANA timezone database 업데이트가 production 컨테이너에 안 들어가 있어서 한 국가의 timezone 변경이 반영 안 됐던 사례 등. 영어책에서는 거의 안 다루는 자리들이다.

발표가 짚는 한 가지 메시지를 빌리자면 — **"한국 회사라고 KST만 다룬다고 생각하는 순간이 가장 위험하다."** 결제 회사에는 일본 사용자가 들어오고, 게임 회사에는 글로벌 트래픽이 섞이고, 광고 회사에는 유럽 사용자의 click이 새벽에 쌓인다. timezone을 application 레벨에서 일관되게 다루는 표준 라이브러리(Java의 `ZonedDateTime`, JavaScript의 `Temporal` proposal, Python의 `zoneinfo`)를 처음부터 골라 두자. 익숙해진 뒤 바꾸려 하면 마이그레이션 비용이 만만치 않다.

기억해 두자. **시간은 단순해 보이지만 분산 시스템에서는 가장 비싼 영역이다.** 그리고 한국 백엔드는 한국 기준에 미국·일본·유럽 사용자가 섞이는 일이 흔해서 timezone hell을 한 번 정도는 꼭 거친다. 거치기 전에 한 챕터 펴 두는 정도의 보험을 들어 두는 편이 낫다.

## 7. 분산 lock — Redis Redlock 논쟁

시간 다음의 사촌 주제로 분산 lock도 짧게 짚어 두자. "두 노드가 동시에 같은 자원을 만지면 안 된다"는 요구는 분산 시스템에 흔하다. 카드 결제 idempotency, 재고 차감, leader election. Redis Redlock·ZooKeeper·etcd가 대표 도구다.

**Redis Redlock**은 Salvatore Sanfilippo(antirez)가 제안한 알고리즘이다. N개의 독립 Redis 인스턴스에 lock을 동시에 시도하고, majority가 동의하면 lock 획득. 단순해 보이지만 — Martin Kleppmann이 2016년에 "이 알고리즘은 wall clock에 너무 의존해 안전하지 않다"는 비판을 공개 글로 올리면서 큰 논쟁이 됐다 (검증 필요 — 두 글의 원문을 찾아 읽어 보길 권한다).

Kleppmann의 비판은 두 줄로 요약된다. ① Redlock은 노드 간 시계가 어긋나지 않는다고 가정하는데, NTP step 같은 일이 일어나면 lock이 두 노드에서 동시에 획득될 수 있다. ② 자원 보호의 진짜 안전성을 원한다면 fencing token (단조 증가하는 lock ID)을 자원 쪽에서 검증해야 한다. antirez는 "lease 기반 lock은 어차피 단순 race condition 외에는 안전하지 않다, 그 한계 안에서 Redlock은 충분히 실용적이다"로 반박했다.

결론을 강제로 짓지는 말자. **production에 분산 lock이 정말 필요한지부터 묻는 편이 낫다.** 많은 경우 lock 없이도 풀 수 있다 — 멱등성 키, 단일 leader, optimistic concurrency control. 정말 필요하다면 ZooKeeper나 etcd 같은 합의 기반 도구가 Redis lock보다 안전한 default다. Redis lock을 쓸 때는 "여기 lock이 풀려도 데이터 정합성이 깨지지 않는다"는 자기 검증이 한 줄 필요하다. 결제 같은 critical path에서는 거의 항상 fencing이 함께 가야 한다.

## 8. 의사결정 트리 — 이 데이터에 진짜 시간이 필요한가

여기까지 따라온 우리에게 필요한 도구는 — "이 데이터에 진짜 시간 보장이 필요한가, 아니면 순서만 있으면 되는가"를 묻는 짧은 트리다. 회의 자리에서 한 박자 안에 던질 수 있는 질문 5개로 정리해 보자.

1. **이 데이터에 글로벌 strong consistency가 필요한가?** 결제 audit·금융 거래라면 yes — TrueTime 가진 Spanner나 그에 준하는 도구. 거의 모든 경우 no — 다음 질문으로.
2. **인과 순서만 보장되면 충분한가?** 메시지 ordering, audit log라면 yes — Lamport timestamp나 HLC면 충분.
3. **단일 region 안에서만 순서가 필요한가?** 한국 한정 서비스라면 yes — single-leader RDB의 transaction order로 충분. 분산 lock도 필요하지 않을 가능성이 높다.
4. **ID에 시간 prefix가 필요한가?** Yes라면 UUIDv7 default. NTP 모니터링 필요. No라면 UUIDv4면 충분 — random ID가 가장 단순하다.
5. **미래 시점 일정을 다루는가?** Yes라면 (local time, timezone name) 쌍으로 저장. UTC 변환은 알람 시점에. timezone database 업데이트를 자동화한다.

이 5개 질문에 답할 수 있으면 시간이라는 어두운 코너에서 길을 잃지 않는다.

## 9. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 시간이라는 까다로운 영역의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Lamport의 통찰** — 벽시계를 포기하고 인과만 잡자. happens-before가 분산 시스템 50년의 토대다.
- **TrueTime의 결정** — GPS·atomic clock을 데이터베이스 안으로. ε~3ms commit wait이 글로벌 strong consistency의 비용이다. 우리 대부분에게는 과한 도구지만, 무엇을 양보했는지 알고 양보하는 게 중요하다.
- **HLC는 commodity hardware로도 굴러간다.** CockroachDB가 골랐다. TrueTime보다 ε가 크지만, 그 대가로 어떤 데이터센터에서도 작동한다.
- **NTP step은 시계를 역행시킨다.** Snowflake ID의 가장 큰 적이다. slew 권장 + ID 생성기에 wait 로직. 부록 A의 tribal 1번 항목으로 다시 만난다.
- **분산 ID의 모던 default는 UUIDv7.** Snowflake도 좋지만 NTP 운영 비용을 짊어진다는 점, 항상 기억해 두자.
- **Timezone hell은 매년 반복된다.** UTC 저장 + 사용자 timezone 표시 + 미래 일정은 (local, timezone name) 쌍. DST 영향 받는 cron은 호출 표현 자체를 손본다. 토스 SLASH 22 발표가 한국 백엔드의 현실 카탈로그다.
- **분산 lock이 정말 필요한지부터 묻자.** Redlock은 NTP step에 취약하다. critical path라면 fencing token + 합의 기반 도구(ZooKeeper·etcd)가 default다.

다음 장(9장)에서는 보안 — 인증·인가·secret·망분리 — 을 짚는다. 보안은 모든 빌딩 블록 위에 깔리는 통제 평면(control plane)이고, 한국 백엔드에서는 망분리·전자금융감독규정 같은 한국 특유의 맥락이 가장 두드러지는 자리다. 시간이 분산 시스템의 가장 어두운 코너였다면, 보안은 가장 약한 고리다. 옆에 두고 같이 짚어 보자.

---

<!-- frontmatter -->
- 챕터 번호: 8
- 분량 추정: 한국어 약 14,500자 (≈ 20페이지)
- 본문 인용 reference: §2.9 시간/순서/분산 ID · §3.9 분산 ID · §4.12 Spanner · §7.11 TrueTime vs HLC, 패턴 3 Timezone Hell(community), tribal #1 NTP slew/step(community), 0장 callback(검증 필요 라벨·통제 평면), 부록 A callback(tribal 1번), 9장 다음 장 예고
- 계획서와 다르게 간 점: 02_plan §3 8장의 항목 모두 커버. 의사결정 트리 5문항을 명시적으로 박은 점이 02_plan보다 한 단계 구체화. Redlock 논쟁은 검증 필요 라벨로 짧게 다룸 (1차 자료 부족 — reference §9 한계 영역).
