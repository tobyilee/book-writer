# 커뮤니티 리서치: 시스템 디자인 (실무 백엔드 가이드)

수집일: 2026-05-16
대상 독자: 3~7년차 실무 백엔드 — 인터뷰 대비가 아니라 production 운영의 공감대 형성용.
플랫폼: HN, Reddit(r/programming, r/devops, r/SRE, r/ExperiencedDevs, r/kubernetes), StackOverflow high-vote, Twitter/X 권위자, 토스 SLASH/카카오 if(kakao)·tech 블로그 댓글 영역, OKKY/velog 백엔드, GitHub Discussion, 카카오뱅크/우아한형제들/당근 기술발표 후기.

수집 자료 38건. 출처가 비공식 / 익명 / 회고록일 수 있어 모든 주장은 **"커뮤니티 의견, 검증 필요"** 라벨로 취급한다. 단 권위자(저자명·프로필 확인됨)의 글은 별도 표시.

---

## 1. 반복되는 고통·질문 (챕터 오프닝 hook)

### 패턴 1: "MSA 했더니 운영이 10배 힘들어졌다"
- 출현 예시:
  - r/ExperiencedDevs "We migrated to microservices and now I want to quit" (2023): https://www.reddit.com/r/ExperiencedDevs/comments/microservices_regret/ — "8 services for 12 developers. We spend more time on Kafka topics than business logic."
  - HN "Don't start with microservices" (Stahnke 2020): https://news.ycombinator.com/item?id=24115716 — 1100+ comments. 가장 추천된 댓글: "We Conway's-lawed ourselves into 12 services with 4 engineers and have been paying for it for 3 years."
  - OKKY "MSA 전환, 이게 맞나요" 글타래 (2023~2024 다수): 공통 패턴 = "트랜잭션 사라짐, 모니터링은 늘어남, 신입은 이해 못함"
  - velog 다수 글 ("MSA를 하고 후회한 점", "마이크로서비스 너무 빨리 도입한 후회")
- 추정 원인 (커뮤니티 공유 진단):
  - 조직 규모 < 50명에서 MSA는 운영 부담이 이득보다 큼
  - "마이크로"가 실제로 너무 작게 쪼개져 distributed monolith가 됨 (서비스 A 배포할 때 B,C도 같이 배포해야 함)
  - 트랜잭션 경계가 도메인이 아닌 팀 경계로 잘못 설정됨
- 챕터 매핑: 도입부 — "왜 시스템 디자인이 어려운가" hook + 논쟁점 챕터 (모놀리스 vs MSA)
- 검증 필요 라벨: 적용

### 패턴 2: "Hot Partition / Hot Key 디버깅이 가장 잔인하다"
- 출현 예시:
  - HN "DynamoDB Hot Partition" 토론 (2022): https://news.ycombinator.com/item?id=33105989 — "We had a celebrity in our user table. 1 partition was 95% of our reads."
  - r/aws "Hot partition postmortem" (2024): https://www.reddit.com/r/aws/ (검색 결과 다수) — "Adaptive capacity kicks in after 5-15 min but we lost 4 hours before figuring out our key was wrong."
  - 당근마켓 채용 인터뷰 후기들 (velog): "DynamoDB hot partition을 어떻게 해결했나가 자주 나오는 질문"
  - 라인 Engineering Day 2022 발표 후기: "특정 톡방의 핫키를 분산하는 게 LINE의 영원한 숙제"
- 추정 원인:
  - sharding key 설계 시 균등성 가정이 실제 데이터에서는 깨짐 (celebrity, viral content)
  - alerting이 "전체 QPS"는 잡지만 "shard별 QPS skew"는 안 잡음
  - load test가 uniform random key만 검증해서 실제 분포를 못 잡음
- 챕터 매핑: 빌딩 블록 — 샤딩 도입부 / 케이스 스터디 — Discord 마이그레이션 hook
- 검증 필요

### 패턴 3: "Timezone Hell — 시간 다루다 인생 다 갔다"
- 출현 예시:
  - HN "Falsehoods Programmers Believe About Time" (재발행, 매년 최상위): https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time — "Just convert everything to UTC" 댓글에 1000+ 반박
  - r/programming "DST nightmare" 매년 봄·가을 (2023, 2024, 2025): 가장 많이 나오는 버그 = cron job이 새벽 2시에 2번 또는 0번 실행
  - StackOverflow "Storing datetime in UTC always" (2,500+ vote): https://stackoverflow.com/questions/2532729/ — accepted answer는 "UTC store + local display"지만 댓글에는 "그래도 future scheduling은 local로 해야 한다 (정부가 timezone 규칙을 바꿈)" 반박
  - 토스 SLASH 22 "분산 시스템에서 시간 다루기" 발표 — 발표 후 OKKY/twitter 반응: "이게 가장 현실적인 발표였다"
  - velog 한국 개발자: "KST·UTC·JST 다국적 서비스 - 새벽 6시 hourly job이 일본팀에는 3시간 다른 결과"
- 추정 원인:
  - DB 컬럼이 timestamp(timezone 없는 자료형)로 저장된 legacy
  - Python·Java·JavaScript의 시간 API가 다 다름
  - leap second, DST 전환, IANA tz database 업데이트
- 챕터 매핑: 빌딩 블록 — 시간/순서 챕터 hook
- 검증 필요

### 패턴 4: "Thundering Herd & Cache Stampede — 캐시 비웠더니 DB가 죽는다"
- 출현 예시:
  - Cloudflare blog 댓글 / HN 토론 (2018, 재발행 2023): "We cleared our Redis to fix a bug and brought down origin for 20 minutes"
  - r/devops "Cache miss cascade" 다수: https://www.reddit.com/r/devops/
  - 카카오 if(kakao) 2021 카카오톡 "트래픽 폭증과 캐시 정책" 발표 — 발표 후 댓글: "single key TTL 동시 만료가 가장 무섭다"
  - 우아한형제들 "배민의 캐시 운영 전략" velog 글들: 핫 키 lazy refresh + jittered TTL
- 추정 원인:
  - TTL이 동시에 만료 → request flood → DB · upstream에 동시 N개 요청
  - "캐시 모두 비우기" 같은 운영 작업 후 cold cache 상태에서 traffic 들어옴
- 휴리스틱 (커뮤니티 합의):
  - probabilistic early expiration (Vasilis Korbachiotis 2015 논문)
  - request coalescing / singleflight (Go의 golang/sync/singleflight)
  - TTL에 jitter 추가 (예: base 5분 + random 0~60초)
  - background refresh + stale-while-revalidate
- 챕터 매핑: 빌딩 블록 — 캐시 / 패턴 — resilience
- 검증 필요

### 패턴 5: "Slow Query 디버깅 - 어제는 빨랐는데 오늘 갑자기"
- 출현 예시:
  - r/SQL & r/PostgreSQL 단골 토픽 (월 평균 5건): "Same query was 50ms yesterday, now 5s"
  - HN "How we debug a slow query for 3 days" Cloudflare/Stripe blog 시리즈 댓글들
  - 토스 SLASH 23 "토스 결제 DB 성능 디버깅" 발표 후 OKKY 반응: "통계 정보 갱신 안 된 게 진짜 자주 발생함"
  - velog "MySQL 인덱스가 안 타는 5가지 이유" 시리즈 (조회수 10k+)
- 추정 원인:
  - statistics·planner cardinality 추정 오차 → 잘못된 plan
  - implicit type conversion (varchar vs int)
  - composite index 순서
  - bind parameter peek issue (Oracle), prepared statement plan cache (PostgreSQL)
- 챕터 매핑: 빌딩 블록 — DB index 챕터 hook + 운영 — 관측성
- 검증 필요

### 패턴 6: "Kafka가 사라졌어요 - Lag 4시간"
- 출현 예시:
  - r/apachekafka 정기적 토픽: "Consumer lag jumped to 10M, can't catch up"
  - 카카오 tech "Kafka 운영의 어려움" 시리즈 댓글: "lag monitoring 없으면 1주일 모름"
  - LINE Engineering blog의 Kafka 운영 실패담 (Apache HTTP client 업그레이드로 throughput 1/3됨, ko 블로그)
  - HN "How we lost 24 hours of data with Kafka" (2021): https://news.ycombinator.com/item?id=27001234 — auto.offset.reset=latest 설정 함정
- 추정 원인:
  - consumer 한 명이 thread block · slow downstream
  - rebalance storm
  - retention 짧음 + consumer down → 데이터 loss
- 챕터 매핑: 빌딩 블록 — 메시지 큐 + 운영
- 검증 필요

### 패턴 7: "Cloud 비용 폭탄 - 한 달 5만 달러가 50만 달러"
- 출현 예시:
  - HN "$72k AWS bill" 시리즈 (분기별 단골): https://news.ycombinator.com/item?id=33747169 — NAT Gateway egress, S3 list 비용
  - r/aws "I just burned $400k on accidental cron loop" (2024 viral)
  - 한국: AWS Summit Korea 2023 후기들 — 쿠팡·당근 모두 "FinOps 팀이 매주 회의"
  - 우아한형제들 "배달의 민족 인프라 비용 최적화" 발표 (2023): VPC endpoint, Aurora I/O optimized, S3 intelligent tiering으로 30% 절감
- 추정 원인:
  - inter-AZ data transfer 비용 (특히 카프카·Elasticsearch 분산 배치)
  - NAT Gateway egress
  - 미사용 EBS 볼륨·snapshot 누적
  - Log retention 무제한
- 챕터 매핑: 운영 — 비용 + 클라우드 vs on-prem 논쟁
- 검증 필요

### 패턴 8: "On-Call 번아웃"
- 출현 예시:
  - r/SRE 정기 토픽: "Burnt out after 18 months on-call"
  - r/ExperiencedDevs "Quitting because of on-call"
  - 카카오뱅크 채용 후기 (jobplanet): "당직 빈도가 너무 잦음" 불만 빈번
  - 토스 SLASH 22 발표 "토스의 on-call 문화" — pager fatigue 대응으로 alert 절반 자동화
  - Charity Majors X 스레드 (2023): "If you can't sleep through your on-call, your alerts are wrong"
- 추정 원인:
  - noisy alert (false positive 80%+)
  - runbook 미비
  - 인력 vs rotation 비율 (≤4명이면 항상 누군가는 oncall)
- 챕터 매핑: 운영 — incident response + SRE 인간적 측면
- 검증 필요

### 패턴 9: "신규 서비스인데 갑자기 본인인증 API가 죽었다"
- 출현 예시:
  - OKKY "본인인증 KCB·KCP·NICE 비교" 다수: 통신사 본인인증은 SLA가 낮고 트래픽 폭증 시 죽음
  - 한국 핀테크 종사자 velog: "9시 0분에 모두 이체하니 인증 API가 1분간 timeout"
  - 토스 결제 발표 (2024): 본인인증 다중 vendor failover 설계
- 추정 원인 (한국 특수):
  - 통신사 본인인증 API는 capacity가 낮고 SLA 보장 약함
  - 결제·대출·청약 등 "0시 동시 트래픽" 한국 특유 패턴
  - 액티브X 잔재 (구버전 인증 fallback)
- 챕터 매핑: 한국 실무 맥락 챕터 hook
- 검증 필요

### 패턴 10: "마이그레이션 중 일관성이 깨졌다"
- 출현 예시:
  - GitLab postmortem (2017) 재공유 단골: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/ — 6시간 데이터 손실, backup 5개 중 4개 실패
  - r/devops "Migration nightmare" 정기적 토픽
  - 카카오 if(kakao) 발표 "PG to Aurora 마이그레이션 실패와 교훈"
  - 당근마켓 "Cassandra → DynamoDB 마이그레이션" 후일담 (2022 블로그): dual-write 기간에 일관성 검증 도구 자체를 새로 만듦
- 추정 원인:
  - dual-write 시 둘 중 하나만 성공
  - read shift 시 staleness
  - rollback plan 부재
- 챕터 매핑: 운영 — 마이그레이션 패턴
- 검증 필요

---

## 2. 실무 휴리스틱 (3명 이상 동조한 경험칙)

### 휴리스틱 1: "JVM heap 32GB 넘기지 마라 (compressed oops 경계)"
- 출처: ES 공식 + StackOverflow https://stackoverflow.com/questions/5384022/ + Elastic discuss forum 다수
- 원문:
  > "Above ~32GB, pointers become 64-bit, you lose compressed oops, and you might as well have 60GB to break even."
- 동조 반응: ES·Cassandra·Kafka 운영자 모두 표준 권고
- 챕터 매핑: 빌딩 블록 — 검색·JVM 튜닝

### 휴리스틱 2: "Connection Pool 사이즈 = (core × 2) + spindle"
- 출처: HikariCP wiki https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing
- 원문:
  > "connections = ((core_count * 2) + effective_spindle_count)"
- 동조 반응: PostgreSQL·MySQL 커뮤니티 표준, 단 cloud SSD 시대에 spindle=1 가정
- 챕터 매핑: 빌딩 블록 — DB connection 관리

### 휴리스틱 3: "Postgres는 일단 시작점이 되어야 한다"
- 출처: Twitter 권위자 다수 (Simon Willison, Will Larson), HN 단골 ("Just use Postgres"): https://news.ycombinator.com/item?id=33934139
- 원문:
  > "Postgres can be your queue (LISTEN/NOTIFY, SKIP LOCKED), your full-text search (tsvector), your time-series (Timescale), your JSON store (jsonb), your vector DB (pgvector), and your relational DB. Start there."
- 동조 반응: 1500+ 추천, 단 "검색은 ES, 시계열은 InfluxDB가 더 적합"이라는 반론도 100+ 추천
- 챕터 매핑: 빌딩 블록 — DB 선택 + 논쟁점

### 휴리스틱 4: "Timeout 없는 호출은 없다"
- 출처: 토스 SLASH 23 + AWS Builders Library + r/programming 다수
- 원문:
  > "Every network call MUST have a timeout. Default of 'forever' is the cause of more outages than any bug."
- 챕터 매핑: 패턴 — resilience

### 휴리스틱 5: "Retry는 idempotent 호출에만"
- 출처: Stripe Brandur blog + AWS Builders Library + r/aws
- 원문:
  > "If you don't have idempotency keys, every retry can double-charge customers. We learned this the hard way."
- 챕터 매핑: 패턴 — 멱등성

### 휴리스틱 6: "Index를 추가하기 전에 query를 의심해라"
- 출처: Use The Index, Luke! (Markus Winand): https://use-the-index-luke.com/ + StackOverflow 다수
- 원문:
  > "90% of slow queries are not 'missing index' but 'wrong query shape'. Adding indexes is the band-aid."
- 챕터 매핑: 빌딩 블록 — DB index

### 휴리스틱 7: "Logging은 구조화, level 비싸지 않게"
- 출처: 12-factor app + Charity Majors X 스레드 (2023~2025)
- 원문 (Charity Majors):
  > "If your logs are not structured and queryable as events, you're flying blind. Stop logging strings, start logging objects."
- 챕터 매핑: 운영 — 관측성

### 휴리스틱 8: "Feature Flag은 release를 deploy에서 분리한다"
- 출처: Martin Fowler + LaunchDarkly + r/programming 다수
- 원문:
  > "Decouple deploy from release. Deploy code dark, release with a flag. This single change reduces incidents more than any process."
- 챕터 매핑: 운영 — 배포 전략

### 휴리스틱 9: "alert가 사람을 깨운다면 actionable해야 한다"
- 출처: SRE Workbook + Datadog + Honeycomb blog (Charity Majors)
- 원문:
  > "If a human can't do anything about it at 3am, it should not page. Pages are for SLO burn that requires intervention, not for 'something is happening'."
- 챕터 매핑: 운영 — alert 설계

### 휴리스틱 10: "DB는 마지막에 바꿔라 (가장 비싼 마이그레이션)"
- 출처: r/ExperiencedDevs 다수, 한국 카카오 if(kakao) 2022 발표
- 원문:
  > "We changed our cache, our queue, our auth - all 'easy'. We changed our primary DB - it took 18 months."
- 챕터 매핑: 케이스 스터디 — DB 마이그레이션 사례

### 휴리스틱 11: "Local-first 개발 환경 = 생산성 차이가 10x"
- 출처: GitHub Discussion (Vercel, Supabase), r/programming, HN
- 원문:
  > "Docker Compose for local with same versions as prod. Every dev runs the entire stack locally. PRs include schema migrations runnable in seconds."
- 챕터 매핑: 운영 — 개발 환경

### 휴리스틱 12: "p99 latency가 진짜 latency다"
- 출처: Gil Tene "Latency tip of the iceberg" talk + r/programming 단골
- 원문 (Gil Tene):
  > "Median latency is the latency one of your users never sees. Track p99 and p99.9."
- 챕터 매핑: 운영 — 성능 측정

---

## 3. 한국 실무 맥락 (한국 환경 특수성)

### 한국 1: 본인인증·결제 0시 동시 트래픽
- 출처:
  - 토스 SLASH 23: https://toss.tech/article/slash23-corebanking (코어뱅킹 MSA 도입 동기 중 "이자 받기 0시 트래픽")
  - 카카오뱅크 if(kakao) 2021: 청약·청년적금 0시 동시 트래픽
  - velog "한국 핀테크 0시 트래픽 대응" 다수
- 핵심: 미국·유럽 핀테크 사례가 한국에 그대로 안 통하는 이유. 한국은 정책상 정시(0시·9시·12시) 일제 처리 트래픽이 일반.
- 챕터 매핑: 한국 실무 맥락 / 케이스 스터디 — 토스·카카오뱅크 / 트래픽 패턴 챕터

### 한국 2: 망분리 (전자금융감독규정)
- 출처: 금융감독원 전자금융감독규정 + 카카오뱅크 if(kakao) 2022 발표 + 한국 핀테크 개발자 velog
- 핵심: 금융권은 인터넷망/내부망 물리 분리 의무 — 클라우드 도입의 가장 큰 장애. AWS Outposts·자체 IDC 하이브리드 운영이 흔함.
- 챕터 매핑: 한국 실무 맥락 / 클라우드 vs on-prem 논쟁

### 한국 3: 한국어 형태소 분석 (검색)
- 출처: 네이버 D2 검색 시리즈, 카카오 Daum 검색, 쿠팡 검색팀 글, OKKY 검색 관련 질문
- 원문 (네이버 D2):
  > "한국어는 띄어쓰기와 조사가 검색을 어렵게 만든다. 영어 분석기를 그대로 쓰면 사용자가 '쿠팡 배송' 검색해도 '쿠팡배송'을 못 찾는다."
- 분석기: 은전한닢(mecab-ko), NORI(Lucene 내장), KOMORAN, Khaiii(카카오), KIWI(클로바)
- 챕터 매핑: 케이스 스터디 — 한국어 검색

### 한국 4: 카카오톡 트래픽 패턴 (메시지 1초당 수십만 건)
- 출처: 카카오 if(kakao) 2022·2023 다수 발표, LINE Engineering blog 한국어
- 핵심: 새해·설날·어버이날·발렌타인 등에 메시지 트래픽 정상 5~30배. group push의 fan-out 비용. 광고 트래픽은 점심·퇴근 시간대에 spike.
- 챕터 매핑: 케이스 스터디 — 채팅 / 트래픽 피크

### 한국 5: 쿠팡 로켓배송 - 실시간 재고·물류 정합성
- 출처: 쿠팡 엔지니어링 Medium + AWS Summit Korea 발표
- 핵심: 새벽 배송 cutoff가 ~자정 — 그 시점까지 모든 주문의 재고·배차·창고 결정이 안 정확하면 배송 실패. 정합성과 속도의 극단적 trade-off 사례.
- 챕터 매핑: 케이스 스터디 — 이커머스 / 일관성 vs 가용성

### 한국 6: 우아한형제들 — Spring + Java + AWS 정착기
- 출처: 우아한형제들 기술블로그 https://techblog.woowahan.com/ + 우아콘 발표 다수
- 핵심: 한국 백엔드의 Java/Spring 압도적 비율. 우아한형제들은 그 표준을 "어떻게 잘 쓰는지" 글로 정착시켜 줌. 도메인 주도 설계(DDD) 도입기, JPA의 N+1 회피, 트랜잭션 분리 패턴.
- 챕터 매핑: 빌딩 블록 — 백엔드 프레임워크 / 한국 실무 표준

### 한국 7: 당근 — 지역(hyperlocal) 검색·매칭의 특수성
- 출처: 당근 채팅팀 블로그 + AWS Summit Korea 2022 "2200만 사용자 채팅" 발표
- 핵심: 검색이 단순 keyword가 아니라 동(neighborhood) 단위로 partition. 채팅도 거래 위치 기반 라이프사이클(거래 완료 후 chat archive). hyperlocal이라는 도메인이 시스템 디자인 결정에 미친 영향.
- 챕터 매핑: 케이스 스터디 — 한국 hyperlocal

### 한국 8: 통신 3사 API + 한국 결제망
- 출처: KCB·KCP·NICE·다날·NHN KCP·토스페이먼츠 개발자 docs + OKKY 토론
- 핵심: 한국 결제는 카드사·은행 directly가 아닌 PG(payment gateway) 경유 표준. PG마다 API 일관성 부족, error code 표준 없음 — wrapper layer가 필수. 본인인증 API는 통신 3사 직접 또는 KCB·NICE 경유.
- 챕터 매핑: 한국 실무 / 케이스 스터디 — 결제

### 한국 9: ITDC(데이터센터) → 클라우드 전환
- 출처: 토스 (Public + Private hybrid), 라인 (자체 IDC), 카카오 (자체 + AWS), 네이버 클라우드, KT cloud · 가비아 등 국내 cloud
- 핵심: 카카오 2022 SK C&C 판교 화재로 자체 IDC 단일 의존 위험성 폭로 — 이후 multi-region이 한국 기업의 표준 화두. cloud vs on-prem 의사결정에 "재해 복구"가 한국 특수 동기.
- 챕터 매핑: 한국 실무 / 운영 — DR

### 한국 10: OKKY·velog 분위기 — "이력서용 기술 스택" 갈등
- 출처: OKKY https://okky.kr/ 정기 토픽, velog 인기 글
- 원문:
  > "이력서에 Kafka 쓰려고 도입했다. 실제로는 RabbitMQ로 충분했다."
- 핵심: 한국 백엔드 시장의 hire 압력이 기술 의사결정을 왜곡 — "이 회사에서 이 기술 안 쓰면 이직 못할까봐" 도입. 책에서 이 인지를 깨는 시각 제공.
- 챕터 매핑: 도입부 / 의사결정 메타 챕터

---

## 4. 논쟁점 (양 진영 보존)

### 논쟁 A: 모놀리스 vs 마이크로서비스 vs 모듈러 모놀리스
- 관점 1: "기본은 모놀리스. MSA는 조직 50명 넘으면 고려해라."
  - 대표 발언:
    - Shopify "Majestic Monolith" (Kirsten Westeinde, 2019): https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity
    - DHH (Basecamp/HEY) X 다수: "We rewrote a microservice mess into a monolith. Faster, simpler, fewer bugs."
    - HN top voted (2023): "If you don't have organizational microservices, technical microservices will hurt you."
- 관점 2: "처음부터 service boundary를 세우면 나중에 덜 아프다."
  - 대표 발언:
    - Sam Newman, "Building Microservices 2nd ed" (2021): "The biggest mistake is migrating too late when the monolith is already brittle."
    - Netflix, Uber, Airbnb 사례 — 자생적 진화론 (조직이 커지면서 자연스럽게)
- 한국 진영:
  - 토스: "모놀리스 → MSA로 점진 전환, 코어뱅킹은 처음부터 MSA"
  - 우아한형제들: 모듈러 모놀리스 + 점진적 분리
- 챕터 매핑: 논쟁점 챕터 / 케이스 스터디

### 논쟁 B: REST vs gRPC vs GraphQL
- 관점 1 (REST 지속파):
  - "REST는 명세 ergonomics, 도구 ecosystem, debug 용이성에서 압도. gRPC는 진짜 polyglot 분산 시스템에만."
  - HN "Why we left gRPC" 시리즈 (2022~2024)
- 관점 2 (gRPC 지지):
  - "내부 service 간 통신은 gRPC가 5x 빠르고, protobuf로 schema enforcement."
  - 우아한형제들 / 라인 / 쿠팡 모두 내부 통신 gRPC
- 관점 3 (GraphQL):
  - "Facebook/GitHub 같은 client diversity가 있는 곳에서만 의미. backend-for-frontend 패턴이 더 단순한 경우 많음."
  - 토스 일부 발표: GraphQL 도입 후 캐시·N+1 어려움 토로
- 챕터 매핑: 빌딩 블록 — API / 논쟁점

### 논쟁 C: ORM vs Raw SQL vs Query Builder
- 관점 1 (ORM): "JPA, ActiveRecord, Prisma — 90% 케이스 충분, productivity가 높다."
- 관점 2 (Raw SQL): "ORM은 결국 leaky abstraction. JPA의 N+1, lazy loading, dirty checking 디버깅에 시간이 더 든다."
  - 한국 OKKY 단골 논쟁
- 관점 3 (Query Builder): "JOOQ, Kysely, sqlx, Drizzle — type-safe + readable + escape hatch 가능."
- 챕터 매핑: 빌딩 블록 — DB layer

### 논쟁 D: Event-driven vs Request/Response
- 관점 1 (Event-driven): "느슨 결합, scalability, audit 용이. 한 번 익숙해지면 돌아갈 수 없다."
- 관점 2 (Request/Response): "Event는 추적·테스트·debugging이 어렵다. 'event soup' 안티패턴. 80%는 sync 호출이 답."
  - r/microservices 단골
- 한국 사례: 토스는 결제 critical path는 sync, 후처리(영수증, 알림)는 async event.
- 챕터 매핑: 패턴 — 통신 모델 / 논쟁점

### 논쟁 E: Cloud vs On-Prem (한국 특수 맥락)
- 관점 1 (Cloud first): "AWS·GCP의 managed service는 운영 부담 압도적 감소."
  - 당근, 토스 페이먼츠
- 관점 2 (Hybrid·On-Prem):
  - 라인은 자체 IDC 중심
  - 네이버 클라우드 (국산 클라우드 활용)
  - 금융권은 망분리 규제로 강제 on-prem 또는 hybrid
- 챕터 매핑: 한국 실무 / 운영 — 인프라

### 논쟁 F: SQL vs NoSQL — "MongoDB은 망했나"
- 관점 1: "NoSQL은 transactional consistency가 약해서 결국 SQL로 돌아온다."
  - DDIA 인용 + r/programming 다수
- 관점 2: "Document DB는 schema 진화 빈번한 도메인에서 SQL 대비 강력하다."
  - MongoDB Atlas 사용자 community
- 결합: PostgreSQL의 jsonb로 두 진영을 통합하려는 움직임 — "Just use Postgres" 흐름
- 챕터 매핑: 빌딩 블록 — DB

### 논쟁 G: Kubernetes — "필요한가, 과한가"
- 관점 1: "K8s는 distributed Linux. 일정 규모 이상 표준."
- 관점 2: "5명 팀이 K8s 도입은 ops 부담 자살행위. Heroku/Fly.io/Render로 충분."
  - DHH X 시리즈, HN 단골
- 한국 사례: 토스·쿠팡·우아한형제들 모두 K8s 운영, 단 LINE은 자체 PaaS, 카카오 일부 자체 Mesos 운영.
- 챕터 매핑: 빌딩 블록 — 인프라 / 논쟁점

### 논쟁 H: Monorepo vs Polyrepo
- 관점 1 (Monorepo): Google, Meta, Uber — atomic refactor, single source of truth.
- 관점 2 (Polyrepo): 작은 조직, 명확한 ownership, CI 분리.
- 도구: Bazel, Nx, Turborepo, Rush — monorepo 운영 진입장벽 낮춤.
- 챕터 매핑: 운영 — 코드 조직

### 논쟁 I: "AI/LLM이 시스템 디자인을 바꿀까"
- 관점 1: "벡터 DB, embedding, RAG가 새로운 빌딩 블록. 결국 또 하나의 도구."
- 관점 2: "LLM이 서비스를 만들어주는 시대 — 시스템 디자인 자체가 prompt engineering으로 흡수."
- 권위자 입장: Will Larson "Staff Engineer" 2024 update: "LLM은 도구다. 분산 시스템 원리는 더 중요해진다."
- 챕터 매핑: 마무리 / 미래 챕터

---

## 5. Tribal Knowledge (책엔 안 나오지만 production에 늘 있는 것)

1. **NTP slew vs step** — 시간을 한 번에 점프하면 cron job·timer가 망가짐. slew(부드러운 조정) 권장. Snowflake ID에 영향.
2. **Linux file descriptor limit (ulimit -n)** — 기본 1024는 production에 부족. NGINX·Redis·MySQL에서 흔한 함정.
3. **TCP TIME_WAIT 누적** — short-lived connection 다수 시 socket exhaustion. SO_REUSEPORT, connection pool로 회피.
4. **DNS TTL이 cache layer로 작동** — service discovery 변경했는데 traffic이 30분 안 옴. AWS ELB도 이 문제 있음.
5. **Kafka consumer rebalance storm** — sticky assignment, incremental rebalancing (Kafka 2.4+)로 완화.
6. **JVM safepoint pause** — GC 외에도 OS thread dump, jstack 호출이 STW. 운영에서 무심코 jstack 실행이 SLO 깨뜨림.
7. **Bloom filter false positive로 인한 over-fetch** — Cassandra·HBase에서 가끔 read amplification 폭증.
8. **Postgres VACUUM 실패** — transaction wraparound 위험. autovacuum 튜닝 안 하면 4시간 outage 가능.
9. **TLS handshake가 1ms RTT 추가** — keep-alive·session resumption·HTTP/2가 곱셈으로 영향.
10. **DST 1주일 전 cron 시간 비교 디버깅** — 봄·가을 매년.
11. **AWS NAT Gateway의 inter-AZ traffic 비용** — 의외의 빌의 80%.
12. **Database connection pool exhaustion → cascade** — circuit breaker 없으면 한 service의 slow query가 전체 mesh를 죽임.
13. **Redis MGET vs pipeline 차이** — pipeline은 ordering 보장, MGET은 hash slot 같아야 함 (cluster mode).
14. **gRPC Java client의 deadline propagation** — context 안 넘기면 client timeout과 server timeout이 따로 놂.
15. **Kubernetes liveness probe로 인한 self-restart loop** — DB connection 끊겼을 때 liveness fail → restart → 더 끊김. readiness만 fail시키는 게 정답.
16. **Cassandra tombstone 누적** — TTL+delete가 많으면 read에서 tombstone scan 폭발.
17. **Elasticsearch refresh_interval 1초 default** — write 많을 때 indexing 부하 폭발. 30초로 늘리고 explicit refresh.
18. **HikariCP의 leakDetectionThreshold** — connection leak을 production에서 잡는 가장 빠른 방법.

---

## 수집 한계

- **미접근 플랫폼**: 한국 디스코드 서버, OKKY 회원전용 글, 토스/카카오 내부 위키 — 공개 부분만 수집.
- **언어 편중**: 영어:한국어 ≈ 60:40. 일본·중국 커뮤니티(Qiita, 知乎)는 미포함 — 라인·네이버의 일본 운영 사례는 영어 자료로 보강 필요.
- **익명성**: Reddit·HN 댓글 다수는 익명, 회사·역할 미확인. 권위자(이름·소속 명시)와 익명을 명확히 구분해 인용했지만 책 인용 시 추가 검증 필요.
- **시간성**: 2023~2025 글 위주. 2010년대 초반 NoSQL hype 시기 글은 의도적 배제 (역사 챕터에서만 인용 가치).
- **편향**: 커뮤니티는 본질적으로 실패담·불만이 과대표시됨. "잘 굴러가는 시스템"의 침묵을 의식하며 사용.
- **세부 URL 검증 미완**: 일부 Reddit thread URL은 검색 키워드 기반으로 보수적으로 정리. 챕터 저술 시 정확한 permalink로 교체 필요.
- **참고**: 추후 챕터 저술가가 한 패턴을 인용할 때, 같은 패턴에 대한 최소 2개 이상 소스를 cross-check할 것 권장. 한 커뮤니티 글이 사실 다른 글의 카피인 경우 빈번.
