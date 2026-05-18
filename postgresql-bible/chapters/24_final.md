# 24장. 클라우드 PostgreSQL — 벤더 매트릭스와 의사결정

매니지드 PostgreSQL을 고르는 일이 식당 메뉴를 고르는 일처럼 쉬워 보일 때가 있다. 콘솔에서 클릭 몇 번이면 인스턴스가 뜨고, 콘솔이 친절하니 운영도 친절할 것 같고, 영업 담당이 와서 보여주는 슬라이드에는 멋진 그래프가 잔뜩 있다. 그런데 그 그래프 옆에 가격표가 같이 있고, 가격표 옆에는 작게 별표가 있고, 별표를 따라가면 "다음의 익스텐션은 지원되지 않습니다" 한 줄이 적혀 있다. 그리고 그 한 줄이 6개월 뒤 우리의 주말을 망친다.

식당에서도 그렇다. 사진만 보고 고른 점심은 며칠은 만족스럽지만, 매주 가야 하는 회사 근처 점심집을 정할 때는 사진보다 재료를 봐야 한다. 어디서 무엇을 가져오는지, 어떤 기름을 쓰는지, 회전이 빠른지, 단골에게 어떻게 대하는지. 매니지드 PostgreSQL도 똑같다. 사진은 마케팅 페이지이고, 재료는 우리가 18장부터 23장까지 차근차근 살펴본 것들이다. VACUUM이 어떻게 도는지, HA가 어떻게 페일오버하는지, 익스텐션이 어디까지 얹히는지, 풀링과 모니터링은 어떻게 붙는지, 그리고 튜닝의 손잡이를 우리가 잡고 있는지.

매니지드 서비스의 진짜 가치는 우리가 모르는 무언가를 대신 해 주는 데 있는 게 아니다. 우리가 아는 무언가를 우리 대신 손쉽게, 안전하게 해 주는 데 있다. 그러니 우리가 모르는 채로 결정을 내리면, 좋은지 나쁜지조차 판단할 수 없다. 그게 이 챕터의 출발점이다. 벤더가 무엇을 약속하는지가 아니라, 그 약속이 우리가 알고 있는 PostgreSQL의 어디를 건드리는지를 살펴보자.

이번 장은 종합편이다. 그래서 인용도 많고, 가지치기도 많다. 그래도 마지막에 의사결정 트리 하나를 손에 쥐고 나가자. 여러분의 워크로드와 팀 상황을 넣으면, 적어도 어떤 벤더를 1순위로 평가해야 하는지가 떨어지는 트리를 함께 만들어보자.

## 24.1 AWS RDS for PostgreSQL — 표준 매니지드의 표준

먼저 가장 표준적인 카드부터 펴 보자. AWS RDS for PostgreSQL이다. RDS는 매니지드 PostgreSQL의 사실상 최저공통분모다. 다른 벤더를 평가할 때도 머릿속에서 무의식적으로 "RDS와 비교했을 때"라는 기준선을 긋고 비교하게 된다. 그 기준선이 무엇이고, 어디가 RDS의 모서리인지를 먼저 알아두자.

### RDS가 우리에게 주는 것

RDS는 본질적으로 *그대로의 커뮤니티 PostgreSQL을* AWS가 관리해 주는 서비스다. 인스턴스를 띄우면 그 안에 도는 PostgreSQL은 우리가 17장에서 다뤘던 그 PostgreSQL이고, 18장에서 진땀 흘리며 다뤘던 그 VACUUM이 같은 알고리즘으로 돈다. 페이지 구조도 같고, MVCC도 같고, WAL도 같다. 그러니 마이그레이션 후의 행동 예측이 가장 쉽다. 이게 RDS의 최대 강점이다. 우리가 17장의 마이그레이션 챕터에서 익혔던 모든 행동 양식이 그대로 통한다. EXPLAIN 결과가 갑자기 이상해지지 않고, autovacuum의 패턴이 갑자기 낯설어지지 않는다.

AWS는 그 위에 자동 백업, multi-AZ 동기 standby, 자동 minor upgrade 옵션, RDS Proxy(21장에서 보았던 풀링), Performance Insights(23장에서 보았던 모니터링), 그리고 IAM 통합을 얹어 준다. 우리가 21장에서 PgBouncer를 직접 띄우며 고민했던 풀링과 모니터링의 상당 부분이 AWS의 자체 도구로 대체된다. 이것을 강점으로 보아도 좋고, 자유도가 떨어진다고 보아도 좋다. 어느 쪽으로 볼지는 팀의 성향과 워크로드에 달려 있다.

### RDS의 모서리 — 손이 닿지 않는 곳들

RDS의 첫 번째 모서리는 **superuser 권한이 없다**는 점이다. 우리는 `rds_superuser`라는, 슈퍼유저처럼 보이지만 실제로는 일부 권한이 제한된 역할을 받는다. `CREATE EXTENSION`은 가능한 익스텐션 목록 안에서만 되고, `pg_hba.conf`를 직접 수정할 수 없고, 파일시스템 접근이 차단된다. 22장에서 보았던 보안 측면에서는 이것이 안전망이 되지만, 어떤 익스텐션은 superuser가 아니면 동작하지 않는다. 평가 단계에서 [지원 익스텐션 목록](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)을 반드시 확인해야 한다.

두 번째 모서리는 **minor upgrade 정책**이다. AWS는 *유지보수 윈도우*라는 시간대에 자동으로 minor 업그레이드를 수행할 수 있다(설정에 따라). 좋게 보면 보안 패치가 자동으로 들어와 우리가 22장에서 봤던 CVE 추적의 부담이 가벼워진다. 나쁘게 보면, 우리가 통제하지 못하는 시간대에 데이터베이스가 한 번 재시작된다. 동기 standby 덕분에 다운타임은 짧지만, *연결이 한 번 끊긴다*는 사실은 변하지 않는다. 21장에서 짚어 두었던 *재연결 전략과 풀러의 페일오버 동작*이 RDS에서도 그대로 의미를 갖는다. 풀러 뒤에 둔 애플리케이션이 connection reset에 강한지, 트랜잭션 중간에 끊겨도 멱등하게 재시도할 수 있는지를 먼저 점검해 두는 편이 낫다.

세 번째 모서리는 **로그와 메트릭의 노출 범위**다. RDS는 PostgreSQL 로그를 CloudWatch Logs로 빼 준다. Performance Insights가 활성 세션을 시각화해 준다. 여기까지는 좋다. 그런데 23장에서 보았던 `pg_stat_statements`의 깊은 분석이나, `auto_explain`으로 모은 plan을 외부 도구(Grafana, Datadog)로 흘려보내는 일은 약간의 추가 설정이 필요하다. AWS 자체 도구로 끝낼 거면 편리하고, 자체 옵저버빌리티 스택을 가진 회사라면 RDS의 로그/메트릭을 자기 스택으로 끌어오는 파이프를 짜야 한다. 어느 쪽이든 가능하지만, "기본값으로 잘 된다"고 가정하면 곤란하다.

네 번째 모서리는 **storage I/O 모델**이다. RDS는 EBS gp3 또는 io1/io2 기반이다. 즉 *블록 스토리지*다. IOPS와 throughput을 설정할 수 있고, 비용은 IOPS·throughput·용량 각각으로 계산된다. 대량 쓰기 워크로드에서 우리가 19장에서 다뤘던 WAL 쓰기가 EBS의 throughput 한계에 부딪히면 latency가 튀기 시작한다. 평소에는 보이지 않다가 트래픽이 두 배가 되는 날 갑자기 튀어나오는, 가장 찜찜한 종류의 한계다. 사전에 `pg_stat_io`(17 신규)로 backend별 I/O를 관측하고, EBS metric으로 throughput 한계 대비 여유를 보아 두자.

### RDS는 누구에게 답인가

RDS가 가장 잘 어울리는 경우는 명확하다. *기존 PostgreSQL 운영 패턴을 그대로 옮기고 싶을 때, 그리고 AWS 생태계 안에 있을 때*. 17장의 마이그레이션 챕터에서 살펴본 패턴, 18장의 VACUUM 운영, 20장의 HA 구성, 23장의 튜닝, 이 모든 것이 RDS에서 최소한의 행동 변경으로 그대로 통한다. "PostgreSQL을 매니지드로 옮기되, 거의 똑같이 운영하고 싶다"가 RDS의 슬로건이다.

반대로 RDS가 답이 아닐 가능성이 높은 경우도 있다. 첫째, *익스텐션을 정말 깊게 쓰는* 워크로드 — 15장에서 다뤘던 익스텐션 생태계 중 RDS가 지원하지 않는 것을 1개라도 쓰고 있다면, RDS는 출발선부터 막힌다. 둘째, *대규모 쓰기 처리량*이 필요해 EBS의 한계가 보이는 워크로드 — 여기서는 다음 절의 Aurora로 자연스럽게 옮겨가게 된다.

## 24.2 Aurora PostgreSQL 깊이 분석

Aurora PostgreSQL은 매니지드 PostgreSQL 시장에서 가장 많은 오해를 부른 제품이다. AWS 측의 마케팅 문구는 "PostgreSQL 호환"이고, 그래서 많은 팀이 "그러면 RDS의 더 빠른 버전이군"이라고 생각하고 옮긴다. 그리고 옮긴 뒤에 *진짜 PostgreSQL이 아니다*는 점에서 비롯되는 자잘한 의외성에 부딪힌다. 다른 어느 벤더보다 한 절을 통째로 할애할 가치가 있는 이유다. 4꼭지로 나눠 깊이 들여다보자.

### 24.2.1 "PG 호환"이 정확히 무엇을 의미하는가

Aurora PostgreSQL은 fork다. PostgreSQL의 코드베이스에서 갈라져 나온 변종이라는 뜻이다. 그런데 이 갈라짐의 *깊이*가 어느 정도인지가 핵심이다. The Build의 Christophe Pettus는 [Aurora를 두고 "수정된 스토리지 엔진을 가진 PostgreSQL의 fork"](https://thebuild.com/blog/2026/05/05/managed-postgres-examined-amazon-aurora-postgresql/)라고 정확히 표현했다. 그러면 무엇이 같고, 무엇이 다른가? 한번 짚고 가자.

**같은 것들.** Aurora는 PostgreSQL의 *위층 절반*을 그대로 가져왔다. 파서, 플래너, 익스큐터 — 즉 우리가 8장과 23장에서 다뤘던 SQL 처리의 거의 전부 — 가 같다. 4장에서 보았던 fork 기반 프로세스 모델도 같다. backend 프로세스가 클라이언트 연결마다 떠올라 트랜잭션을 처리한다. 5장의 MVCC 의미론도 같다. 트랜잭션은 자기 시점의 스냅숏을 본다. xmin/xmax 비교 규칙도 같다. 6장의 HOT 업데이트도 같은 알고리즘으로 적용된다. 같은 페이지 안에서 indexed 컬럼이 바뀌지 않은 업데이트는 HOT chain으로 처리된다. 7장의 SSI도 동일하다. `SERIALIZABLE` 트랜잭션이 같은 predicate locking 메커니즘으로 동작한다. SQL 표현이 같고, 함수와 연산자가 같고, JSON 처리가 같다. 9장에서 12장까지 다룬 활용 시나리오의 대부분이 그대로 가능하다.

**다른 것.** 그런데 *아래층 절반*은 다르다. Aurora는 PostgreSQL의 storage 레이어 — 즉 buffer manager 아래, 페이지를 디스크에 쓰는 그 부분 — 를 통째로 갈아 끼웠다. Aurora의 storage는 *분리된 스토리지 노드 군집*이다. WAL(redo log)만 write-ahead로 storage에 흘려보내고, page 자체는 storage 노드 측에서 redo log를 재생해 만들어 둔다. 6개 카피가 3개 AZ에 흩어져 있고, 쓰기는 quorum(6 중 4)으로 확정된다. 읽기는 quorum(6 중 3)으로 확정된다. 이 구조의 결과로 redo log만 네트워크로 흘려보내고 page는 흘려보내지 않으니, *네트워크 대역폭이 크게 줄어든다*. 마케팅 문구에서 자주 보는 "log is the database"라는 표현이 이 뜻이다.

여기까지가 사실관계다. 그러면 이게 우리에게 무슨 차이를 만드는가? 같음과 다름을 구분해서 봐야 한다. 8~16장의 활용 측면은 거의 같다. SQL을 짜는 방식, 인덱스 종류 선택, JSON 처리, 전문 검색의 표현 — 모두 그대로다. 그런데 18~23장의 운영 측면은 다르다. VACUUM이 어디서 어떻게 도는지, replication slot이 어떻게 동작하는지, failover가 어떻게 일어나는지, 백업이 어떻게 잡히는지 — 이 모두가 storage가 다르다는 사실의 영향을 받는다. 활용 챕터를 읽은 독자에게는 Aurora가 친근하게 느껴지지만, 운영 챕터를 읽은 독자에게는 Aurora가 *낯선 동물*로 느껴진다. 이 비대칭이 Aurora의 운영 함정의 진짜 원인이다.

### 24.2.2 Disaggregated storage가 운영에 미치는 실제 영향

이제 가장 흥미로운 부분으로 들어가자. *storage가 다르다*는 사실이 우리의 일상 운영에 어떤 모양으로 나타나는가? 추상적인 아키텍처 설명이 아니라, 18~23장에서 우리가 진땀 흘리며 익혔던 그 운영 작업들이 Aurora에서 어떻게 달리 보이는지를 살펴보자.

**VACUUM의 비용 모델이 달라진다.** 우리가 18장에서 길게 다뤘던 VACUUM은 본질적으로 dead tuple을 식별해 free space로 표시하고, 필요하면 frozen으로 표시하는 작업이다. 페이지를 읽고, 페이지를 쓰는 작업이다. 평범한 PostgreSQL에서는 이 읽기·쓰기가 로컬 buffer pool과 로컬 디스크 사이에서 일어난다. Aurora에서는 어떻게 될까? *VACUUM은 여전히 writer 인스턴스 위에서 돈다*. 그리고 그 결과를 redo log로 storage에 흘려보낸다. Pettus가 명확히 짚어 준 대로, "분산 스토리지가 [vacuum-chasing 문제를] 해결해 주지는 않는다". writer 인스턴스가 작으면, 잦은 update/delete 워크로드에서 똑같은 bloat-and-vacuum-chasing의 굴레에 빠진다.

그러면 무엇이 달라지는가? 두 가지가 달라진다. 첫째, *checkpoint의 의미가 사라진다*. 평범한 PostgreSQL의 checkpoint는 dirty buffer를 디스크로 내려쓰는 일이고, 18장에서 보았듯이 이 과정이 I/O 스파이크를 만든다. Aurora에는 이 checkpoint가 없다. storage 노드가 알아서 redo log를 재생해 page를 구성하기 때문이다. OpenAurora 측정([Wang et al., SIGMOD 2024](https://www.cs.purdue.edu/homes/csjgwang/pubs/SIGMOD24_OpenAurora.pdf))의 한 결론이 정확히 이 점이다: "checkpointing becomes a 'free' operation without additional overhead". 둘째, *VACUUM이 쓰는 페이지의 비용 모델이 다르다*. 평범한 PostgreSQL은 vacuum이 페이지를 dirty로 만들고, 나중에 background writer나 checkpoint가 그것을 디스크로 내린다. Aurora는 vacuum이 redo log를 storage로 보내는 즉시 그것이 "쓰기"로 잡힌다. 즉 Aurora의 IOPS 청구는 vacuum의 활동을 직접 반영한다. 이건 비용 측면에서 의외의 항목이 될 수 있다 — *공격적인 autovacuum 튜닝이 곧 청구서다*. 18장에서 우리가 했던 "autovacuum을 적극적으로 돌리자"라는 조언이 Aurora에서는 약간의 수정이 필요하다. 청구서를 보면서 균형을 잡아야 한다.

**XID wraparound는 어떻게 보이는가.** 18장의 핵심 주제였던 wraparound는 Aurora에서도 그대로 일어난다. MVCC가 같은 알고리즘이고, XID 공간도 같은 32비트이기 때문이다. relfrozenxid가 늘어나는 것을 모니터링해야 하고, autovacuum이 꼭 freeze를 따라잡도록 해야 한다. 다른 점은 *진단 도구의 위치*다. Aurora는 [`postgres_get_av_diag()`](https://aws.amazon.com/blogs/database/prevent-transaction-id-wraparound-by-using-postgres_get_av_diag-for-monitoring-autovacuum/)라는 진단 함수를 제공해 autovacuum이 왜 늦어지는지(long-running transaction, replication slot에 매여 있는 xmin 등)를 한눈에 보여준다. 평범한 PostgreSQL에서는 `pg_stat_activity`와 `pg_replication_slots`를 손으로 짜 맞춰야 알 수 있는 정보를 한 함수로 보여주는 것이다. 운영 도구로서는 좋다. 그래도 *원리는 같다*는 점을 잊지 말자. 18장의 wraparound 시나리오는 Aurora에서도 똑같이 일어난다.

**Replication slot과 logical replication.** Aurora는 logical replication을 지원한다. `wal_level=logical`을 켤 수 있고, publication과 subscription을 만들 수 있다. 그런데 *physical streaming replication*은 외부 PostgreSQL로 보내지 않는다. Aurora의 standby 복제는 storage 레이어가 처리하기 때문에 `pg_basebackup` + WAL streaming 모델이 존재하지 않는다. Pettus가 정확히 짚어 준 결론이 여기서 나온다: "Aurora에서 빠져나오는 건 불가능하지 않지만, `pg_basebackup`과 streaming replication만큼 간단하지는 않다". Aurora를 떠나는 시나리오를 그릴 때, 즉 *lock-in 위험*을 평가할 때 이 점이 핵심이다. logical replication을 통해 외부 PostgreSQL로 데이터를 흘려보낼 수는 있지만, large 객체나 schema 변경 같은 일부 시나리오에서 손이 더 간다.

**17의 failover slot은 어떻게 되는가.** 20장에서 다뤘던 [PostgreSQL 17의 failover slot](https://www.decodable.co/blog/failover-replication-slots-with-postgres-17)은 standby 페일오버 시점에 logical replication slot의 위치가 보존되는 기능이다. Aurora의 standby 페일오버는 storage 레이어에서 일어나므로 *failover slot의 원리가 그대로 적용되지 않는다*. Aurora 자체가 다른 방식으로 logical replication slot의 연속성을 (제한적으로) 보장하지만, 우리가 자체 PostgreSQL에서 17 failover slot으로 누렸던 것을 그대로 기대하기는 어렵다. 평가 단계에서 Aurora의 logical replication 페일오버 동작을 반드시 자신의 워크로드로 검증해야 한다.

**Failover 후의 캐시 콜드 스타트.** 평범한 PostgreSQL의 standby는 primary와 같은 buffer pool을 *읽기 트래픽으로* 데우고 있다. 페일오버가 일어나면 그 데워진 buffer pool 위에서 쓰기가 시작된다. 읽기로 데워진 캐시는 쓰기에 그대로 좋은가? 비슷하지만 같지는 않다. Aurora에서도 이 현상이 일어난다. Pettus의 표현을 빌리면, "promoted reader는 읽기용으로 데워진 캐시를 갖고 있고, hot page를 요구하는 쿼리는 페일오버 직후에 캐시가 다시 채워지는 동안 latency spike를 겪을 수 있다". 20장에서 우리가 HA 페일오버를 다룰 때 짚어 둔 *cache warmup*의 문제는 Aurora에서도 그대로 살아 있다. 페일오버 직후의 latency를 모니터링해 두자.

**파라미터의 손잡이가 줄어든다.** RDS에서도 일부 GUC가 막혀 있지만, Aurora에서는 *그 범위가 더 좁다*. 우리가 23장에서 잡고 흔들었던 손잡이들 — `shared_buffers`, `work_mem`, `effective_io_concurrency`, `random_page_cost`, autovacuum 관련 GUC — 중 일부는 그대로 노출되지만, 일부는 Aurora가 자동으로 관리하거나 권장값을 강제한다. 그래서 23장의 튜닝 기법을 그대로 옮기려고 하면 "왜 이 GUC가 안 보이지?" 하는 의외성을 만난다. 평가 단계에서 [Aurora PostgreSQL의 파라미터 그룹 문서](https://aws.amazon.com/blogs/database/amazon-aurora-postgresql-parameters-part-2-replication-security-and-logging/)를 자신이 흔들고 싶은 손잡이 목록과 대조해 보는 일이 필요하다.

### 24.2.3 OpenAurora SIGMOD 2024 측정 — 실측 vs 마케팅

Aurora의 마케팅 문구는 "PostgreSQL 대비 3배 빠르고 5배 가용성이 높다" 같은 표현이 흔하다. 이 숫자가 어느 정도로 맞는지를 정직하게 보고 싶다면 좋은 자료가 하나 있다. Purdue 대학의 [Wang 그룹이 SIGMOD 2024에 발표한 OpenAurora paper](https://www.cs.purdue.edu/homes/csjgwang/pubs/SIGMOD24_OpenAurora.pdf)다. Aurora의 핵심 아키텍처 — disaggregated storage, redo log shipping, multi-version storage — 를 *오픈소스로 재구현해* PostgreSQL 13 기반으로 만든 프로토타입이고, 그 위에서 *각 설계 결정이 성능에 미치는 영향을 정량적으로 측정*했다. AWS Aurora 자체의 측정은 아니지만, "Aurora의 설계 원리가 갖는 성능 트레이드오프"를 가장 정직하게 보여주는 자료다. 핵심 발견 몇 가지를 풀어 보자.

**쓰기 처리량은 모놀리식의 약 50%다.** 가장 충격적인 — 그리고 가장 정직한 — 발견이다. 모든 최적화를 다 적용한 disaggregated storage 구현이, 같은 워크로드에서 단일 노드 PostgreSQL 대비 *약 50%의 쓰기 처리량*만을 낸다. paper 저자들 본인도 의문을 표한다: 파이프라이닝으로 거의 완전히 회복할 수 있을 것 같은데, 왜 여전히 50%에 머무는가? 일부는 *네트워크 round-trip이 commit path에 들어가기 때문*이고, 일부는 *log shipping의 보장 수준*이 disk 쓰기보다 까다롭기 때문이다. 자, 그러면 Aurora의 마케팅 문구 "3배 빠르다"는 거짓말인가? 그렇지는 않다. 그 비교의 *기준*이 무엇인지가 핵심이다. *single-node PostgreSQL의 동일 인스턴스 사양과 비교한 단순 throughput*에서는 Aurora가 *느릴 수 있다*. 그런데 multi-AZ HA 구성 — 즉 primary + 2 sync standby — 와 비교하면, Aurora의 quorum 기반 쓰기가 더 효율적이고, *훨씬 큰 IOPS 한계*를 가진 storage 위에서 돌기 때문에 처리량의 천장이 더 높다. 비교 대상을 무엇으로 잡느냐의 문제다. *single-node와 비교하면 Aurora는 느리고, multi-AZ HA와 비교하면 Aurora가 빠르다*. 둘 다 사실이다.

**읽기 latency는 buffer pool에 크게 의존한다.** OpenAurora 측정에서 8GB buffer로 80% 캐시 적중률을 확보했을 때, 모놀리식 대비 *읽기 성능 격차는 1.8배 정도*로 좁혀진다. 그런데 *read-after-write* 시나리오 — 즉 방금 쓴 페이지를 곧장 읽는 경우 — 에서는 *18.9%의 추가 오버헤드*가 발생한다. 이유는 명확하다. 방금 쓴 페이지를 storage 노드에서 가져오려면 그 노드가 redo log를 재생해 페이지를 구성해야 하고, 그 재생 자체가 약간의 시간이 걸린다. 이 사실이 우리에게 무엇을 가르쳐 주는가? *Aurora의 워크로드 적합성은 캐시 적중률과 read-after-write 패턴에 크게 좌우된다*. 충분히 큰 메모리를 가진 인스턴스에서 cold read가 적은 워크로드라면 Aurora는 훌륭히 동작한다. 그런데 메모리가 부족해 cold read가 많거나, 방금 쓴 데이터를 곧장 읽는 패턴이 많은 워크로드라면 *latency가 평범한 PostgreSQL보다 나쁠 수 있다*.

**Buffer의 효과는 비대칭이다.** OpenAurora의 또 하나의 발견은, buffer 크기를 늘렸을 때 *읽기는 크게 좋아지지만 쓰기는 거의 좋아지지 않는다*는 점이다. 당연한 결론이지만 정량적으로 확인된 게 가치 있다. 쓰기는 commit 시점에 redo log가 무조건 storage에 도착해야 하기 때문에, 큰 buffer로 도움받을 수 없다. 그래서 *Aurora의 인스턴스 사양을 키울 때, 쓰기 처리량은 거의 늘지 않을 수 있다*. 큰 instance가 비싸진 만큼 쓰기 처리량이 따라오리라는 직관은 Aurora에서는 종종 깨진다.

**Checkpoint는 자유다.** 앞에서도 짚었듯이, multi-version storage의 한 가지 명백한 이점은 *checkpoint overhead가 사라진다*는 점이다. OpenAurora paper의 표현 그대로 "checkpointing becomes a 'free' operation". 평범한 PostgreSQL이 주기적으로 만드는 checkpoint I/O 스파이크가 Aurora에는 없다. 18장에서 우리가 봤던 *bgwriter와 checkpointer 튜닝*의 절반이 Aurora에서는 의미가 없어진다. 작지만 분명한 이점이다.

**그래서 마케팅을 어떻게 읽을까.** 정리하면 이렇다. Aurora의 마케팅 숫자는 *틀린 게 아니라, 어떤 비교에 한해서 맞는다*. 단순한 single-node 비교에서는 Aurora가 느릴 수 있고, multi-AZ HA 구성과 비교하면 Aurora가 훨씬 유리하다. 따라서 평가는 "Aurora가 PostgreSQL보다 빠른가?"가 아니라 "우리가 어차피 multi-AZ HA를 구성할 것이라면, Aurora가 그것을 더 잘 해내는가?"라는 질문으로 다시 짜야 한다. 그 질문으로 다시 짠 비교에서, Aurora는 *대체로* 더 잘 해낸다. 더 잘 해내는 대신 storage 레이어의 운영 특성을 통째로 받아들여야 한다.

### 24.2.4 "Aurora는 진짜 PG인가" — 정직한 결론

여러 절을 거쳐 봤으니, 이제 정직한 결론을 내릴 수 있다. *Aurora는 진짜 PostgreSQL인가?* 

이 질문은 사실 두 개의 질문을 합쳐 놓은 것이다. 첫째, "Aurora의 SQL 행동 양식이 PostgreSQL과 같은가?" 둘째, "Aurora의 운영 특성이 PostgreSQL과 같은가?" 두 질문의 답이 다르다는 게 핵심이다.

첫째 질문, 즉 *SQL 측면*에서는 *진짜에 매우 가깝다*. 우리가 8~16장에서 다뤘던 모든 활용 시나리오 — 트랜잭션 의미론, JSON, 전문 검색, GIS, 벡터, 이벤트 큐, FDW, 분석 — 의 거의 모두가 Aurora에서 같은 코드로 작동한다. 우리가 짠 쿼리, 우리가 만든 인덱스, 우리가 정의한 트리거와 함수, 우리가 쓰는 익스텐션의 대부분이 Aurora로 옮겨도 행동을 유지한다. 이 측면에서 Aurora는 진짜 PostgreSQL이다.

둘째 질문, 즉 *운영 측면*에서는 *진짜와 미묘하게 다르다*. VACUUM의 비용 모델, checkpoint의 의미, replication의 모양, 백업의 흐름, 페일오버의 메커니즘, 파라미터의 노출 범위, 일부 익스텐션의 가용성, 모니터링이 노출하는 메트릭 — 이 모두가 다르다. 우리가 18~23장에서 익힌 운영 노하우가 *대부분 통하되, 일부 디테일에서 의외성을 만든다*. 이 측면에서 Aurora는 진짜 PostgreSQL이 아니다.

그래서 어떤 워크로드에 Aurora가 답인가? *PostgreSQL의 SQL과 익스텐션 생태계를 그대로 활용하면서, multi-AZ HA를 자동으로 받고, 쓰기 처리량의 천장이 높은 storage가 필요한 워크로드*. 더 풀어 쓰면, 대규모 멀티 AZ OLTP 워크로드, 특히 우리가 직접 standby를 운영하기 부담스러워 그 부분을 외주 주고 싶은 팀에게 답이다.

어떤 워크로드에 함정인가? *Aurora가 지원하지 않는 익스텐션을 깊게 쓰는* 워크로드, *VACUUM과 storage 비용의 결합에 민감한* 워크로드, *Aurora를 나중에 떠날 가능성이 있어서 lock-in을 피하고 싶은* 팀, 그리고 *방금 쓴 페이지를 곧장 읽는 패턴*이 많은 워크로드. 마지막 항목은 OpenAurora의 read-after-write 18.9% 오버헤드에서 직접 도출되는 것이다. 캐시 친화적이지 않은 쓰기-읽기 패턴은 Aurora의 약점이다.

한 가지 더, 가장 정직한 한 줄을 보태고 가자. *Aurora가 진짜 PostgreSQL인지의 논쟁은, 우리가 PostgreSQL의 *어디까지를* PostgreSQL이라고 부르는지에 달려 있다*. SQL과 익스텐션까지를 PostgreSQL이라고 부른다면 Aurora는 PostgreSQL이다. 그 아래 storage·HA·운영 도구까지를 포함해 PostgreSQL이라고 부른다면 Aurora는 PostgreSQL의 *변종*이다. 둘 다 정당한 정의다. 우리 팀이 어느 쪽을 PostgreSQL이라고 부르는지를 합의하고 평가에 들어가는 편이 낫다. 합의 없이 평가하면, 6개월 뒤에 "PostgreSQL이라더니"라는 원망이 누군가의 입에서 나온다.

## 24.3 GCP Cloud SQL과 AlloyDB — 표준 매니지드와 HTAP 도전자

AWS 쪽을 길게 봤으니, GCP로 시선을 옮겨 보자. GCP는 두 카드를 들고 있다. *Cloud SQL for PostgreSQL*은 RDS의 GCP 버전이고, *AlloyDB*는 AlloyDB만의 독자적 아키텍처를 가진 도전자다. 두 제품의 위치가 명확하니 차례로 살펴보자.

### Cloud SQL for PostgreSQL — GCP의 RDS

Cloud SQL은 GCP가 운영하는 *표준* 매니지드 PostgreSQL이다. 24.1에서 우리가 RDS에 대해 적었던 거의 모든 문장이 Cloud SQL에도 그대로 적용된다. 코어가 같은 PostgreSQL이고, 자동 백업과 HA standby가 있고, IAM 통합이 있고, 콘솔이 친절하다. 익스텐션은 *지원 목록 안에서만* 가능하고, 파라미터의 일부는 잠겨 있고, superuser 권한이 없다.

GCP 안에서 일하는 팀에게는 Cloud SQL이 가장 자연스러운 선택이다. 한 가지 흥미로운 디테일이 있는데, *GCE 인스턴스에서 Cloud SQL Proxy를 통해 접속*하는 패턴이 사실상 표준이다. 이 Proxy는 21장의 PgBouncer와 결이 다른 도구다 — 풀링이 아니라 *인증과 TLS 터널링*을 제공한다. 그래서 GCP에서는 *PgBouncer를 별도로 띄우거나, Cloud SQL Proxy + 애플리케이션 측 풀러를 조합해서* 풀링을 해결한다. RDS Proxy처럼 매니지드 풀러가 한 단계 더 있는 구성에 비해 손이 한 단계 더 간다고 보아도 좋다.

### AlloyDB — PostgreSQL에 columnar engine을 얹다

이제 흥미로운 카드를 보자. AlloyDB는 GCP가 2022년에 처음 공개한 매니지드 PostgreSQL이다. Aurora처럼 *PostgreSQL 호환*이지만, AlloyDB의 차별 포인트는 *자동 columnar engine*에 있다. 무슨 뜻인지 살펴보자.

평범한 PostgreSQL은 row-oriented 저장 방식이다. 한 row의 모든 컬럼이 페이지 안에 함께 들어 있다. OLTP에는 이 방식이 좋다 — 한 row 전체를 한 번에 읽고 쓰는 일이 흔하기 때문이다. 그런데 *분석 쿼리* — 즉 "이 컬럼의 합계와 평균을 모든 row에 대해 계산하라" 같은 쿼리 — 는 row-oriented 저장 방식에서 매우 비효율적이다. 필요 없는 컬럼까지 페이지에 끼어 들어와 있어서 cache가 더 많은 데이터로 채워지고, 같은 컬럼 값들이 흩어져 있어서 SIMD 같은 벡터 연산의 효율도 떨어진다. 그래서 분석은 *columnar* 저장 방식 — 같은 컬럼의 값들이 한곳에 모이는 — 이 압도적으로 빠르다. 15장에서 우리가 다뤘던 [pg_duckdb나 Hydra columnar 같은 익스텐션](https://motherduck.com/blog/pg-duckdb-release/)이 PostgreSQL 안에 columnar 옵션을 들여오는 시도들이었다.

[AlloyDB의 columnar engine](https://cloud.google.com/blog/products/databases/alloydb-for-postgresql-columnar-engine)은 이걸 *자동으로* 해 준다. 기본 storage는 여전히 row-oriented이지만, AlloyDB가 워크로드 패턴을 분석해 *자주 분석되는 컬럼 부분집합*을 메모리 안의 columnar 형태로 *복제*해 둔다. 같은 데이터의 두 가지 표현 — row와 column — 을 유지하면서, 옵티마이저가 쿼리 종류에 따라 두 표현 중 더 빠른 쪽을 선택한다. 마케팅 문구로는 "분석 쿼리 최대 100배 빠름"이고, 이 숫자가 어느 정도 부풀려져 있는지를 가늠하기는 어렵지만, *분석 쿼리 한정으로 명백한 수십 배의 가속*은 사실로 확인되는 모양이다.

자, 그러면 AlloyDB는 우리의 무엇을 해결해 주는가? *OLTP와 분석을 한 데이터베이스에서 처리하고 싶을 때*의 답이다. 15장에서 우리가 다뤘던 *HTAP(Hybrid Transactional / Analytical Processing)* 시나리오의 자동화된 버전이다. 따로 ETL을 짜서 분석 DB로 옮길 필요 없이, 같은 데이터베이스 안에서 OLTP가 돌고 분석이 돌 수 있다. 단, *진짜로 분석이 많은가*를 자문해야 한다. 분석 쿼리의 비중이 낮으면 columnar engine의 가치는 *비용 대비* 미미하다. AlloyDB는 [Cloud SQL Enterprise Plus 대비 약 39% 비싸다](https://cloud.google.com/alloydb). 39%를 지불해 columnar engine을 얻는 게 가치 있는지는 워크로드에 달려 있다.

### Cloud SQL과 AlloyDB의 운영 면에서의 차이

Cloud SQL과 AlloyDB는 같은 GCP가 운영하지만 *제품 철학이 다르다*. Cloud SQL은 *PostgreSQL을 그대로* 운영하는 데 집중한다. AlloyDB는 *PostgreSQL을 GCP가 재해석한 분산 시스템*이다. 그래서 AlloyDB도 Aurora와 비슷한 종류의 운영 의외성을 갖는다 — VACUUM의 의미, 익스텐션의 가용성, 페일오버의 메커니즘이 vanilla PostgreSQL과 미묘하게 다르다.

GCP를 쓰는 팀에게 우리의 추천은 이런 모양이다. *우선 Cloud SQL로 시작해 보자.* 워크로드가 명백히 OLTP+분석 혼합으로 진화하고, ETL을 따로 짜기 싫고, columnar engine의 39% 프리미엄을 감당할 수 있다면 *그때* AlloyDB를 평가하자. 분석이 별로 없는데 "다들 쓰니까"라는 이유로 AlloyDB를 골랐다가, 1년 뒤 비용 청구서를 보고 후회하는 일은 피하는 편이 낫다.

## 24.4 Azure Database for PostgreSQL — Flexible Server

Azure의 매니지드 PostgreSQL은 *Single Server*와 *Flexible Server* 두 라인이 있었다가, 사실상 Flexible Server로 통합되어 가는 중이다. Single Server는 신규 채택을 권장하지 않는다 — Azure 본인이 그렇게 안내한다. 그러니 Flexible Server 기준으로만 살펴보자.

Flexible Server는 RDS와 Cloud SQL의 Azure 버전이라고 보면 된다. *표준 PostgreSQL*을 매니지드로 운영하고, 자동 백업·HA standby·VNet 통합·Azure AD 인증을 얹어 준다. Aurora나 AlloyDB와 같은 *재해석된 분산 storage*는 없다. 그래서 *예측 가능성*이라는 측면에서는 가장 친근한 매니지드다. 자체 PostgreSQL에서 익힌 모든 노하우가 거의 그대로 통한다.

Azure를 쓰는 팀에게 Flexible Server는 *디폴트 선택*이다. Azure 생태계 안의 다른 서비스(Synapse, Data Factory, Logic Apps)와의 통합이 자연스럽고, Azure Monitor와의 통합으로 모니터링이 평탄하게 풀린다. 익스텐션 지원 범위는 RDS보다 약간 적은 편이지만, 흔히 쓰는 PostGIS·pgvector·pg_partman·pg_stat_statements 정도는 다 들어 있다.

한 가지 짚어 둘 점은 Azure가 *서드파티 PostgreSQL 매니지드와의 통합*이 가장 활발한 쪽이라는 점이다. Azure Marketplace에 Crunchy Bridge가 매끄럽게 올라와 있고, EDB의 Postgres가 정식 매니지드 옵션으로 제공된다. 우리가 *Azure 위에서* PostgreSQL을 매니지드로 돌리되 *Azure 자체 제품이 아닌 옵션*을 검토하고 싶다면, Azure Marketplace를 한번 둘러보는 편이 낫다.

## 24.5 Supabase — PostgreSQL이 풀스택 BaaS의 코어가 되다

이제 결이 완전히 다른 카드를 한 장 펴 보자. Supabase는 PostgreSQL을 *백엔드 풀스택*으로 감싼 BaaS(Backend-as-a-Service)다. Firebase의 PostgreSQL 버전이라고 봐도 좋다. 16장에서 우리가 "DB가 백엔드다"라는 패러다임을 다룰 때 이미 한 번 마주쳤던 그 Supabase다.

### Supabase가 PostgreSQL 위에 얹는 것

Supabase는 PostgreSQL 인스턴스 한 대 위에 다음의 다섯 가지를 얹어 한 묶음으로 판다.

**PostgREST** — 테이블에 대한 자동 REST API. 16장에서 다뤘던 *DB-as-Backend* 패턴의 가장 깔끔한 구현체다. `posts` 테이블을 만들면 `/rest/v1/posts`로 GET/POST/PATCH/DELETE가 즉시 동작한다. 권한은 PostgreSQL의 GRANT와 RLS(22장)로 제어한다.

**pg_graphql** — 같은 데이터를 GraphQL로도 노출한다. REST 대신 GraphQL을 쓰는 프론트엔드 팀이라면 별도 게이트웨이를 깔 필요가 없다.

**Auth** — 사용자 인증과 세션 관리를 매니지드로 해 주는 서비스. 이메일·OAuth·매직 링크 등 흔한 인증 시나리오가 거의 코드 없이 풀린다. 인증된 사용자의 정보를 PostgreSQL의 `auth.users` 테이블로 노출해, RLS 정책에서 `auth.uid()`로 직접 참조할 수 있다.

**Storage** — 파일 업로드/다운로드를 위한 S3 호환 게이트웨이. 메타데이터는 PostgreSQL에 저장되어, RLS로 권한을 똑같이 제어할 수 있다.

**Realtime** — PostgreSQL의 logical replication을 받아 *WebSocket으로 클라이언트에 실시간 푸시*한다. 13장에서 우리가 LISTEN/NOTIFY와 logical replication으로 풀던 *실시간 패턴*의 매니지드 버전이다.

**Edge Functions** — Deno 런타임 기반의 서버리스 함수. DB 트리거나 webhook에서 호출할 수 있다.

이 다섯 가지가 하나의 콘솔에서 통합 관리된다. 그래서 *프론트엔드 + 백엔드 = Supabase + React/Next*만으로 풀스택 SaaS 한 편이 떠오른다. MVP 단계의 스타트업이 Supabase를 사랑하는 이유다.

### Supabase의 강점 — RLS를 진짜로 쓰게 만든다

Supabase의 진짜 가치는 *PostgreSQL의 RLS를 정말로 쓰게 만든다*는 점이다. 22장에서 RLS를 다룰 때 우리가 "이론적으로는 멋진데 실제로는 잘 안 쓰인다"라고 짚어 두었던 그 RLS다. Supabase는 *RLS를 디폴트로 켜 두고, RLS 정책을 만들지 않으면 API가 데이터를 노출하지 않게 막아 둔다*. 이 강제력이 핵심이다. 우리가 자체 운영하면서 RLS를 "나중에 켜야지" 미루다가 영영 안 켜는 패턴이 Supabase에서는 일어나지 않는다.

또 하나의 강점은 *무료 티어가 진짜로 쓸 만하다*는 점이다. 500MB 데이터베이스, 50K MAU(Monthly Active Users) 같은 한도가 초기 사이드 프로젝트에 충분하다. 사이드 프로젝트가 운영체로 발전했을 때의 매끄러운 업그레이드 경로도 잘 닦여 있다.

### Supabase의 모서리

Supabase의 첫 번째 모서리는 *lock-in*이다. PostgREST는 표준 도구라 쉽게 떠날 수 있지만, *Auth, Storage, Edge Functions, Realtime*은 Supabase의 자체 구현이다. 이 네 가지를 깊게 쓴 애플리케이션을 Supabase 밖으로 옮기려면, 동일한 기능을 직접 만들거나 다른 도구로 대체해야 한다. 이건 작은 일이 아니다.

두 번째 모서리는 *PostgreSQL 인스턴스의 크기와 성능 천장*이다. Supabase는 본질적으로 *한 PostgreSQL 인스턴스 위의 풀스택*이다. 쓰기 처리량이 단일 인스턴스의 한계에 부딪히면 — 즉 우리가 23장에서 봤던 그 인스턴스 단위 한계에 부딪히면 — Supabase의 솔루션은 *더 큰 인스턴스*뿐이다. 수평 확장은 read replica 정도다.

세 번째 모서리는 *튜닝의 손잡이*다. Supabase는 PostgreSQL의 GUC를 어느 정도 노출해 주지만, 우리가 23장에서 다뤘던 *깊은 튜닝* — 즉 워크로드별로 fine-tuned된 autovacuum, work_mem, shared_buffers 조정 — 의 손잡이가 자체 운영보다 작다. 표준 워크로드에는 충분하지만, 정말 특이한 패턴의 워크로드에서는 답답할 수 있다.

### Supabase는 누구에게 답인가

Supabase가 가장 빛나는 경우는 *MVP·사이드 프로젝트·중소규모 SaaS*다. *프론트엔드 한 명이 백엔드까지 책임지고 싶을 때*의 답이다. 풀스택 한 명 또는 작은 팀에게는 Supabase가 *생산성의 절대 우위*를 가진다. 또한 *RLS를 정말 잘 쓰고 싶은 멀티테넌트 SaaS*에게도 강하게 추천할 만하다.

반대로, *대규모 트래픽이 예상되는 엔터프라이즈 워크로드*나, *복잡한 익스텐션 조합이 필요한 워크로드*, *자체 옵저버빌리티 스택과 깊게 통합해야 하는 워크로드*에게 Supabase는 답이 아니다. 그런 워크로드는 RDS/Aurora/AlloyDB 라인이 더 맞다.

## 24.6 Neon — 서버리스 PostgreSQL과 branching

Supabase가 *PostgreSQL 위에 풀스택을 얹는* 방향이었다면, Neon은 *PostgreSQL의 storage와 compute를 분리해 서버리스로 만든다*는 다른 방향의 도전이다. Aurora의 disaggregated storage 아이디어를 한 발 더 밀고, 그 위에 *git-style branching*과 *0으로 scale-down*을 얹은 모델이다.

### Compute/storage 분리와 그 함의

Neon의 핵심 아키텍처는 Aurora와 친척이다. *compute*(즉 PostgreSQL backend가 도는 노드)와 *storage*(즉 페이지가 영구 저장되는 노드)가 분리되어 있다. 그런데 Neon은 Aurora보다 한 단계 더 나간다. *compute가 아예 0으로 줄어들 수 있다*. 즉 우리의 PostgreSQL 인스턴스가 트래픽이 없는 동안 *완전히 꺼져 있다가*, 새로운 연결이 들어오는 순간 *몇 초 만에 떠올라* 트래픽을 받는다. 떠올라 있는 동안만 compute 비용이 발생한다.

이 모델의 매력은 *트래픽이 가변적인 워크로드*에 명백하다. 사이드 프로젝트의 DB가 새벽 3시에 트래픽이 없으면 비용이 0에 가깝다. CI 환경에서 100개 PR마다 PostgreSQL 인스턴스를 띄워 테스트한 뒤 끄는 패턴이 비용 부담 없이 가능하다. 트래픽이 예측 불가능한 SaaS의 *DB scale-to-zero*를 진짜로 구현한 거의 유일한 매니지드 PostgreSQL이다.

가격 모델도 이 철학을 따른다. *Compute Unit-hour*(CU-h)당 청구되고, storage는 *저장 용량당*으로 청구된다. 가변 트래픽에서는 인스턴스 기반 청구보다 *훨씬 저렴해질 수 있다*. 반대로 24/7 풀 트래픽 워크로드에서는 인스턴스 기반이 더 저렴할 수도 있다. 평가 단계에서 *우리 워크로드의 idle 시간 비율*을 산정하는 일이 핵심이다.

### Branching — git처럼 데이터베이스를 분기한다

Neon의 진짜 차별 포인트는 *branching*이다. PostgreSQL 인스턴스 한 개에서, *현재 상태를 그대로 복사한* 새 인스턴스를 *몇 초 만에* 만들 수 있다. 그런데 이 복사는 *데이터를 실제로 복사하지 않는다*. copy-on-write로 *원본의 page를 공유*하다가, 분기 이후 수정이 일어난 페이지만 따로 저장한다. 즉 100GB 데이터베이스의 branch를 만드는 데 *100GB만큼의 시간도, 비용도 들지 않는다*.

이 능력이 무엇을 해결해 주는가? *개발 워크플로의 핵심 마찰점*을 풀어 준다.

**CI 환경에서의 통합 테스트.** 모든 PR마다 production 데이터의 사본 위에서 테스트를 돌리고 싶지만, 데이터가 크면 그 사본을 만드는 시간과 비용이 부담이다. Neon에서는 *PR마다 branch를 만들고, 테스트가 끝나면 branch를 지운다*. 시간과 비용이 모두 작다.

**Schema migration의 안전한 리허설.** Schema migration을 production에 쓰기 전에, *production의 정확한 사본 위에서* 한번 돌려보고 싶다. Neon branching이 이걸 일상화한다.

**Feature branch마다 격리된 DB.** 여러 개발자가 같은 schema를 동시에 건드릴 때, 각자 자기 branch의 DB를 가질 수 있다. 모두가 같은 staging DB를 깨뜨리며 싸우는 풍경이 사라진다.

이 워크플로의 가치를 한 번 경험한 팀은 다시 돌아가기 어렵다고들 한다. *git가 코드에 가져온 자유를, Neon이 데이터베이스에 가져왔다*는 표현이 마케팅 문구로 자주 보이는데, 과장이긴 하지만 정신은 맞다.

### Neon의 모서리

Neon의 첫 번째 모서리는 *cold start*다. compute가 0에 가까이 있다가 새 연결이 들어와 떠오를 때, *몇 초의 지연*이 발생한다. 이 지연이 *사용자 경험에 그대로 노출되는* 워크로드 — 즉 실사용자의 첫 요청이 그 cold start에 걸리는 시나리오 — 에서는 문제가 된다. 항상 어느 정도의 트래픽이 있다면 cold start가 거의 일어나지 않지만, 정말로 자주 idle해진다면 *최소 compute을 1로 고정*하는 옵션을 검토해야 한다. 그러면 cold start는 없어지지만 *서버리스의 비용 매력이 약해진다*.

두 번째 모서리는 *Aurora와 마찬가지로 vanilla PostgreSQL과의 미세한 차이*다. Neon은 PostgreSQL을 fork해 storage 레이어를 갈아 끼웠다. 그러니 18~23장의 운영 노하우 중 *storage 의존 부분*은 다르게 동작한다. VACUUM은 여전히 compute 위에서 돌지만 결과는 분리된 storage로 흘러간다. Aurora에서 짚었던 *VACUUM과 storage 비용의 결합*이 Neon에서도 비슷한 모양으로 나타난다.

세 번째 모서리는 *대규모 쓰기 처리량 워크로드에 대한 적합성*이다. Neon의 강점은 *가변 트래픽과 branching*이지, *24/7 풀 쓰기 처리량*은 아니다. Aurora가 multi-AZ HA에서 빛난다면, Neon은 dev/CI와 가변 트래픽 SaaS에서 빛난다.

### Neon은 누구에게 답인가

Neon이 가장 잘 어울리는 경우는 명확하다. *개발 환경과 CI*, *가변 트래픽 SaaS*, *멀티 환경 격리가 중요한 팀*. 그리고 Neon의 branching을 *production이 아닌 곳에서 적극 활용*하는 팀에게는 거의 무적이다.

production을 Aurora나 RDS로 두고 *dev/staging/CI만 Neon으로 두는 하이브리드*도 좋은 패턴이다. branching의 가치만 누리고, production의 안정성은 더 보수적인 선택으로 가져가는 방식이다.

## 24.7 Crunchy Bridge·Tembo·Xata — 모던 매니지드의 세 갈래

이제 *상대적으로 덜 알려진* 모던 매니지드 PostgreSQL을 셋만 더 보자. 각자 다른 철학으로 시장의 빈틈을 노린다. 짧게 살펴보고 가자.

### Crunchy Bridge — 진지한 PostgreSQL 전문가의 매니지드

Crunchy Data는 PostgreSQL 컨설팅 회사로 오래 일해 온, *진짜 PostgreSQL 전문가 집단*이다. PostGIS를 만들어 온 사람들이 있고, PostgreSQL 코어에 커밋하는 사람들이 있다. 그 회사가 만든 매니지드 서비스가 [Crunchy Bridge](https://www.crunchydata.com/products/crunchy-bridge)다.

Crunchy Bridge의 정체성은 *vanilla PostgreSQL을 가장 정직하게 매니지드로 운영*하는 것이다. Aurora나 AlloyDB처럼 storage를 갈아 끼우지 않는다. 그냥 *제대로 운영되는 PostgreSQL*을 판다. HA와 PITR이 기본으로 포함되어 있고, multi-cloud(AWS·GCP·Azure)에 같은 PostgreSQL을 매끄럽게 띄울 수 있다. *익스텐션 지원이 풍부하다* — RDS가 지원하지 않는 일부 익스텐션(PGroonga, pg_search, pgvectorscale 등)도 사용 가능하다.

가격은 $10/월부터 시작해 합리적이고, 콘솔이 깔끔하다. *PostgreSQL의 모든 것을 그대로 쓰면서 매니지드의 편의는 받고 싶다*는 팀에게 RDS의 강력한 대안이다. 특히 *익스텐션을 깊게 쓰는* 워크로드에는 Crunchy Bridge가 RDS보다 훨씬 답에 가깝다.

### Tembo — 익스텐션 마켓플레이스로 PostgreSQL을 재정의하다

Tembo는 한 가지 단순한 신념으로 출발했다. *PostgreSQL의 진짜 가치는 익스텐션 생태계에 있다*. 그래서 Tembo는 *익스텐션을 한 번의 클릭으로 설치할 수 있는 마켓플레이스*를 만들어 두고, *워크로드별로 사전 패키지된 PostgreSQL stack* — 예를 들어 *vector workload용 PostgreSQL*, *time-series workload용 PostgreSQL*, *전문 검색용 PostgreSQL* — 을 한 묶음으로 판다.

K8s operator 기반이라 self-host도 가능하고, 매니지드 클라우드도 제공한다. *익스텐션 생태계를 정말 적극적으로 활용하고 싶은* 팀에게 흥미로운 선택이다. 단, 회사의 규모와 production 검증 사례가 RDS나 Crunchy Bridge에 비해 적다는 점은 평가에 넣어야 한다.

### Xata — 비용당 성능을 무기로

[Xata](https://xata.io)는 PostgreSQL 위에 *비용당 성능* 최적화를 무기로 들고 나온 신생 매니지드다. 마케팅 문구는 *Aurora 대비 가격당 성능 ~80% 우위*를 주장한다. 이 숫자가 어느 정도 부풀려졌는지를 가늠하기는 어렵지만, *비용에 민감한 워크로드*가 한번 PoC해 볼 가치는 있는 선택이다.

Xata는 *트래픽 기반 청구*를 채택해, idle 시간 비용을 낮추는 모델을 가졌다. Neon과 비슷한 방향이지만, Neon이 *branching과 개발 워크플로*에 집중한다면 Xata는 *비용 효율*에 집중한다.

### 세 도전자의 공통 모서리

Crunchy Bridge·Tembo·Xata 셋 모두 공통의 모서리가 하나 있다. *회사의 규모와 생태계 두께*가 AWS·GCP·Azure에 비해 작다는 점이다. 무엇이 문제냐? *서비스 장애 시의 대응*, *24/7 지원의 두께*, *생태계 통합*(다른 매니지드 서비스와의 연동)에서 AWS/GCP/Azure가 한 단계 위다. *enterprise 규모의 production*에 셋 중 하나를 디폴트로 깔기에는 약간의 망설임이 정직한 반응이다.

그래도 셋 다 각자의 강점이 있고, *특정 워크로드*에는 명백히 답이다. 익스텐션 활용도가 핵심이면 Crunchy Bridge나 Tembo, 비용 효율이 핵심이면 Xata를 1순위로 평가에 넣는 편이 낫다.

## 24.8 의사결정 트리 — 우리 워크로드에 무엇이 답인가

자, 이제 카드를 다 펴 봤다. 그러면 우리는 어떻게 골라야 하는가? 단순한 비교표로는 부족하다. *워크로드의 특성*에 따라 같은 벤더가 답이 될 수도 함정이 될 수도 있기 때문이다. 그래서 *의사결정 트리* 한 개를 함께 만들어 보자. 가지치기 순서가 핵심이다 — 어떤 질문을 먼저 묻느냐가 결과를 결정한다.

### 1번째 가지: 마이그레이션의 단순성을 얼마나 중시하는가

가장 먼저 묻는 질문이다. 17장에서 우리가 다뤘던 *MySQL/Oracle에서 PostgreSQL로의 마이그레이션*이 막 진행 중이거나 막 끝난 단계라면, 매니지드 PostgreSQL의 *행동 양식이 vanilla와 얼마나 같은지*가 결정적이다. 마이그레이션 직후에는 *행동 양식의 차이가 곧 추가 디버깅 비용*이기 때문이다.

이 질문에 "매우 중시한다"라고 답한다면, *vanilla PostgreSQL과 가장 가까운* 옵션들이 1순위다. RDS, Cloud SQL, Azure Flexible Server, Crunchy Bridge. 이 네 가지 안에서 *어느 클라우드 위에 있는가*로 좁혀 가자.

"덜 중시한다"라고 답한다면, Aurora/AlloyDB/Neon 같은 *변종 storage*도 후보에 남길 수 있다.

### 2번째 가지: write 처리량의 천장이 얼마나 높아야 하는가

다음 질문이다. 우리 워크로드의 *예상 쓰기 처리량*이 단일 인스턴스의 한계를 위협할 정도로 큰가? 23장에서 우리가 다뤘던 *인스턴스 사양 한계*가 보이는 워크로드인가?

이 질문에 "그렇다"라고 답한다면, *disaggregated storage*를 가진 옵션들이 강해진다. AWS 위라면 Aurora, GCP 위라면 AlloyDB. 두 옵션 모두 vanilla PostgreSQL보다 storage I/O 천장이 높다.

"아니다, 평범한 OLTP 수준이다"라고 답한다면, *vanilla 매니지드*가 비용 대비 더 합리적이다. RDS/Cloud SQL/Azure Flexible/Crunchy Bridge로 충분하다.

### 3번째 가지: 분석 워크로드가 같은 DB 안에 섞이는가

세 번째 질문이다. 15장에서 다뤘던 *OLTP와 분석의 혼합* — 즉 같은 데이터를 트랜잭션 쓰기와 분석 쿼리가 동시에 두드리는 — 시나리오가 우리 워크로드에 있는가? 그리고 그 분석 쿼리가 *별도 ETL로 분리하기 어려운* 종류인가?

이 질문에 "그렇다"라고 답한다면, AlloyDB의 columnar engine이 강력한 후보다. AWS 위라면 RDS + [pg_duckdb](https://github.com/duckdb/pg_duckdb) 또는 RDS + ParadeDB pg_analytics 조합으로 비슷한 효과를 노릴 수 있다.

"아니다, 분석은 별도 데이터 웨어하우스로 옮긴다"라고 답한다면 이 가지는 건너뛰자.

### 4번째 가지: 익스텐션의 깊이는 어느 정도인가

네 번째 질문이다. 우리가 15장의 익스텐션 챕터와 22장의 보안 챕터에서 다뤘던 익스텐션들 — pgvector·pg_partman·pg_cron·PGroonga·pg_search·pgvectorscale·TimescaleDB·PostGIS·pgaudit — 중 *몇 개를 깊이 쓰는가*?

3개 이하의 흔한 익스텐션(pgvector, pg_partman, pg_stat_statements 정도)만 쓴다면, 거의 모든 매니지드가 답이 된다.

5개 이상의 익스텐션, 특히 *RDS가 지원하지 않는 익스텐션*을 쓰고 있다면, *Crunchy Bridge나 Tembo*가 강력한 후보다. 익스텐션 지원이 풍부한 매니지드를 적극 우선해야 한다. *익스텐션을 평가 단계에서 확인하지 않고 매니지드를 결정했다가, 마이그레이션 D-1에 "이 익스텐션이 지원되지 않습니다"를 발견하는 일이 가장 끔찍한 일이다.* 18~23장에서 익힌 모든 운영 노하우가 무력해지는 순간이다.

### 5번째 가지: lock-in을 얼마나 허용할 수 있는가

다섯 번째 질문이다. *3년 뒤에 이 벤더에서 떠날 가능성*이 있는가? 떠나야 한다면 *얼마나 매끄럽게 떠나고 싶은가*?

"lock-in을 절대 받지 않겠다"라고 답한다면, *vanilla PostgreSQL을 그대로* 운영하는 옵션이 답이다. RDS, Cloud SQL, Azure Flexible, Crunchy Bridge. 이 넷은 *pg_basebackup과 logical replication만으로* 다른 곳으로 옮길 수 있다.

"적당히 받겠다, 강점만 얻을 수 있다면"이라고 답한다면, Aurora/AlloyDB/Neon이 후보에 들어온다. 단, *떠나는 시나리오의 디테일*을 평가 단계에서 한번 그려 보자. Aurora를 떠나는 시나리오, Neon을 떠나는 시나리오를 종이에 그려 보는 것만으로도 lock-in의 무게가 느껴진다.

"lock-in 신경 안 쓴다, BaaS의 풀스택이 더 가치 있다"라고 답한다면, Supabase가 후보다.

### 6번째 가지: 가변 트래픽과 dev/CI 워크플로

여섯 번째 질문이다. 우리 워크로드가 *24/7 풀 트래픽*인가, 아니면 *idle 시간이 많은 가변 트래픽*인가? 그리고 *PR마다 branched DB로 테스트*하는 워크플로가 매력적인가?

가변 트래픽이거나 dev/CI에 branching이 필요하다면, *Neon*이 명백한 후보다. 그렇지 않다면 Neon의 가치는 약해진다.

### 7번째 가지: 풀스택 BaaS의 가치

마지막 질문이다. 우리 팀이 *프론트엔드 한 명이 백엔드까지 책임지는* 구조인가? 그리고 *Auth·Storage·Realtime을 별도 도구로 통합하는 일이 부담*인가?

그렇다면 *Supabase*가 강력한 후보다. 그렇지 않다면 Supabase의 가치는 약해진다.

### 가지치기를 적용해 보기

이제 트리를 실제 워크로드에 적용해 보자. 몇 가지 시나리오를 그려 보면 트리의 사용법이 더 분명해진다.

**시나리오 A: 금융 SaaS의 production OLTP.** 마이그레이션 단순성 중시 + 쓰기 처리량 매우 큼 + 분석 분리 + 익스텐션 적당히(pgaudit·pg_partman·pg_stat_statements) + lock-in 적당히 허용. AWS 위라면 *Aurora PostgreSQL*이 1순위, GCP 위라면 *AlloyDB*가 1순위. 익스텐션이 RDS 지원 범위 안이라 통과.

**시나리오 B: 데이터 과학팀이 분석을 같이 돌리는 SaaS.** 마이그레이션 단순성 중시 + 쓰기 처리량 보통 + 분석이 같은 DB에 섞임 + 익스텐션 적당히. GCP 위라면 *AlloyDB*가 1순위. AWS 위라면 *RDS + pg_duckdb*나 *RDS + ParadeDB pg_analytics* 조합도 평가에 넣자.

**시나리오 C: 초기 단계 SaaS, 풀스택 한 명.** 마이그레이션 없음 + 쓰기 처리량 작음 + 분석 분리 + 익스텐션 적당히 + lock-in 허용 + 풀스택 BaaS 가치 큼. *Supabase*가 명백한 1순위.

**시나리오 D: dev/CI에 branching이 강하게 필요한 팀.** Production은 별개로 두고 *dev/staging만 Neon*으로. Production은 RDS나 Aurora로 가져가는 하이브리드 패턴.

**시나리오 E: 익스텐션을 깊게 쓰는 GIS 회사.** 마이그레이션 단순성 중시 + 쓰기 처리량 보통 + 익스텐션 매우 깊음(PostGIS·pgvector·pg_partman·pg_cron·PGroonga 등) + lock-in 적게. *Crunchy Bridge*나 *Tembo*가 1순위. RDS는 일부 익스텐션 미지원으로 배제될 가능성.

**시나리오 F: 비용이 가장 큰 압박인 스타트업.** 트래픽 가변 + branching에 매력 + 비용 민감. *Neon* 또는 *Xata*가 후보.

이렇게 가지치기를 거치고 나면, *추상적인 비교표*보다 훨씬 손에 잡히는 결론이 나온다. 그리고 그 결론을 팀에 공유할 때, *왜 그 답에 도달했는지의 추론 과정*까지 보여줄 수 있다. 이 추론 과정이 팀의 합의를 만든다.

## 24.9 함정 — 평가 단계에서 놓치기 쉬운 것들

마지막 절이다. 의사결정 트리를 거쳐 1순위 벤더를 정했다고 하자. 그래도 *평가 단계에서 한 번 더 확인해야 할 함정* 몇 가지가 있다. 이걸 놓치면, 좋은 결정을 내리고도 잘못된 결과로 끝난다.

### 함정 1: 익스텐션 지원 목록의 D-1 발견

가장 흔하고 가장 끔찍한 함정이다. 매니지드 벤더의 마케팅 페이지는 "다양한 익스텐션 지원"이라고 적혀 있지만, 정확한 *지원 목록*은 깊은 문서 안에 있다. 그 목록을 평가 단계에 확인하지 않고 결정을 내렸다가, *마이그레이션 D-1에 우리가 쓰는 익스텐션이 빠져 있음을 발견*하는 일이 정말로 흔하다.

체크리스트 한 줄을 만들어 두자. 평가 단계에서 *우리가 쓰는 모든 익스텐션의 이름*을 적고, 각 벤더의 지원 목록 페이지에서 *그 이름을 grep해 확인*하자. 단순한 작업이지만, 이 한 번이 D-1의 비명을 막아 준다.

특별히 주의할 익스텐션 몇 가지를 짚자. *PGroonga*(한국어 전문 검색의 거의 유일한 답), *pg_search*(ParadeDB의 BM25 검색), *pgvectorscale*(pgvector를 한 단계 키운 벡터 검색), *pg_partman*(파티셔닝 자동화), *pg_cron*(in-DB 스케줄러), *pgaudit*(컴플라이언스 감사 로그). 이 여섯 가지는 *벤더마다 지원 여부가 갈리는 단골 메뉴*다. 우리 워크로드에 하나라도 있다면 평가 단계의 1순위 체크 항목이다.

### 함정 2: minor upgrade 정책의 자동성과 통제 사이

매니지드 벤더는 *minor upgrade를 자동으로 수행*하는 옵션을 디폴트로 켜 둘 때가 많다. *유지보수 윈도우*라는 시간대 안에 자동으로 재시작하는 모델이다. 좋은 점이 있다 — 22장의 보안 측면에서 CVE 패치가 자동으로 들어와 우리가 챙길 일이 줄어든다. 나쁜 점도 있다 — *우리가 통제하지 못하는 시간*에 데이터베이스가 재시작된다는 점이다.

평가 단계에서 *minor upgrade의 자동 여부, 알림 채널, 연기 가능 기간, 유지보수 윈도우 길이*를 확인해 두자. 그리고 21장에서 우리가 짚어 두었던 *연결 풀러와 애플리케이션의 재연결 동작*이 minor upgrade 시점에 어떻게 보이는지를 *staging에서 한 번 시뮬레이션*해 보자. 풀러 뒤의 앱이 connection reset에 약하다면, minor upgrade가 일어날 때마다 짧은 latency spike나 error spike가 발생한다. 그것이 *허용 가능한가*를 평가하는 과정이 필요하다.

### 함정 3: 비용 모델의 단위가 벤더마다 다르다

매니지드 PostgreSQL의 비용 비교는 *직접 비교가 거의 불가능*하다. 단위가 벤더마다 다르기 때문이다.

- *RDS*는 *인스턴스 시간 + EBS 용량 + EBS IOPS + 데이터 전송*
- *Aurora*는 *인스턴스 시간 + storage 용량 + I/O 요청 수 + 데이터 전송* (I/O 청구가 별도)
- *Cloud SQL*은 *vCPU 시간 + 메모리 시간 + storage 용량 + 데이터 전송*
- *AlloyDB*는 위의 Cloud SQL과 비슷하되 *columnar 메모리* 별도
- *Neon*은 *Compute Unit-hour + storage 용량 + 데이터 전송*
- *Supabase*는 *프로젝트 단위 정액 + 사용량 초과분*
- *Xata*는 *트래픽 단위 청구*

이 단위들 사이의 *직접 비교*는 거의 의미가 없다. 한 워크로드의 한 달 비용을 *우리 워크로드의 실제 패턴*으로 simulate해 보는 일이 유일한 정직한 비교 방법이다. 벤더가 제공하는 *cost calculator*를 사용하되, 입력 파라미터(IOPS·throughput·storage·전송량)를 *과거 6개월의 실제 메트릭*에서 가져오자. 산정해 보면 의외의 결과가 나올 때가 많다 — 단순 인스턴스 시간 비교에서 비싸 보이던 Aurora가 IOPS 청구를 더해 보면 실은 비슷하거나, Neon이 24/7 트래픽에서는 의외로 비싸거나.

특히 *데이터 전송 비용*을 잊지 말자. 같은 리전 안의 EC2-RDS 간 전송은 보통 무료지만, *다른 리전이나 다른 클라우드로의 전송*은 GB당 청구된다. 14장의 CDC나 17장의 마이그레이션 같은 *대량 데이터 이동*이 일어나는 시점에 이 비용이 청구서의 큰 한 줄로 떠오를 수 있다.

### 함정 4: replication slot이 쌓아 두는 WAL

이건 운영의 함정이다. logical replication을 쓰는 환경에서 *replication slot의 consumer가 멈추면*, WAL이 *디스크에 무한히 쌓인다*. 매니지드 PostgreSQL이라고 이 메커니즘이 다르지 않다. 우리가 14장의 CDC 챕터에서 Debezium 같은 consumer를 띄울 때, *consumer 장애의 알림*과 *slot의 lag 모니터링*을 함께 세워 두지 않으면, 어느 새벽 디스크가 가득 차서 PostgreSQL이 멈춘다.

매니지드 벤더의 자동 storage 확장 옵션이 있다면 이 위험이 잠시 미뤄지지만, 결국 어느 한도에 부딪힌다. 그리고 그 한도에 부딪히기 전에 *비용 청구서*가 먼저 사람들을 놀라게 한다. 평가 단계에서 *slot lag 알림*을 어떻게 설정할지를 함께 그려 두자.

### 함정 5: 페일오버 RTO의 마케팅과 실측

벤더의 마케팅은 "RTO 30초"라고 적혀 있을 수 있다. 그런데 *실측*은 워크로드와 시점에 따라 다르다. *진행 중인 큰 트랜잭션이 있을 때*, *connection storm이 일어났을 때*, *cache가 cold할 때*의 RTO는 마케팅 수치보다 길 수 있다.

평가 단계에서 *실제로 페일오버를 한번 트리거*해 보자. 매니지드 벤더 대부분이 *manual failover* 명령을 제공한다. 그 명령을 staging에서 실제 워크로드를 흘리며 한번 눌러 보고, *애플리케이션이 회복하는 데 걸린 시간*을 재 보자. 그 숫자가 *우리의 SLA에 부합하는지*를 검증하는 과정이 평가의 핵심이다.

### 함정 6: 콘솔이 친절한 만큼 의존이 깊어진다

마지막 함정이다. 매니지드 벤더의 콘솔은 친절하다. 모니터링도 친절하고, 알림도 친절하고, 백업도 친절하다. 그런데 이 친절함은 *코드가 아니다*. 즉 우리 인프라의 상태를 *Terraform이나 Pulumi에 코드로 표현*하지 않으면, *콘솔의 클릭으로 만든 상태가 어디에도 기록되지 않는다*. 그 사람이 떠나면 그 상태가 *재현 불가능한 상태*가 된다.

평가 단계에서 *벤더의 IaC 지원*을 확인하자. Terraform provider가 있는지, 모든 설정이 코드로 표현 가능한지, 그리고 *알림과 백업 정책까지 코드로* 관리할 수 있는지. 콘솔의 친절함을 다 받되, *상태는 코드에 두자*. 이 원칙을 평가 단계에서 합의하고 가야 1년 뒤에 *콘솔에서 만들고 잊혀진 무수한 설정*의 늪에 빠지지 않는다.

## 마무리 — 매니지드 결정은 결국 운영의 거울이다

여기까지 왔다. 길었다. 한 벤더의 마케팅 페이지보다 짧지는 않았지만, 그래도 손에 잡히는 결론이 몇 개 남았기를 바란다.

이 챕터의 진짜 결론은 어쩌면 간단하다. *매니지드 PostgreSQL의 선택은 PostgreSQL을 얼마나 잘 아는가의 거울이다*. 우리가 18장의 VACUUM, 19장의 백업, 20장의 HA, 21장의 풀링과 모니터링, 22장의 보안, 23장의 튜닝을 깊이 이해하고 있다면, 어떤 벤더가 어디를 친절하게 해 주는지가 명확히 보인다. 그 이해 없이 매니지드를 고르면, *벤더의 약속*이 *우리의 운영*과 어떻게 맞물리는지를 알 수 없다.

그러니 한 가지를 기억해두자. *매니지드 벤더가 우리를 PostgreSQL에서 해방시켜 주지는 않는다.* 매니지드는 *우리가 알아야 할 것을 줄여 주는 게 아니라, 우리가 직접 해야 할 작업을 줄여 준다*. 알아야 할 것은 여전히 그대로다. 어쩌면 더 많아진다 — vanilla PostgreSQL의 원리에 *그 벤더가 추가로 변형한 부분*까지 알아야 하기 때문이다.

이 챕터의 의사결정 트리를 한 번 적용하고 나면, 적어도 *1순위 벤더와 그 이유*가 정리된다. 그리고 정리된 이유를 팀 안에서 공유하면, 6개월 뒤에 누군가 "왜 그때 이걸 골랐지?"라고 물을 때 답할 수 있다. 답할 수 없는 결정은 답할 수 없는 후회로 돌아온다.

마지막으로 한 가지. 이 챕터에서 다룬 벤더 매트릭스는 *2026년 봄의 상황*이다. 매니지드 PostgreSQL 시장은 빠르게 움직인다. AWS가 새 storage 옵션을 발표할 수도 있고, GCP가 새 columnar 가속을 추가할 수도 있고, Neon이 새 기능을 내놓을 수도 있고, 우리가 들어보지 못한 신생 벤더가 다른 차원에서 도전장을 낼 수도 있다. 의사결정 트리의 *질문들*은 시간이 지나도 유효하다. *답*은 시간에 따라 바뀐다. 트리의 질문을 손에 쥐고, 답을 새로 찾는 일을 한 해에 한 번씩 반복하는 편이 낫다.

자, 다음 장에서는 *한국 회사들*이 PostgreSQL로 어떤 결정을 내렸는지, 그것이 우리에게 어떤 다음 걸음을 가리키는지를 살펴보자. 이번 챕터에서 정리한 의사결정 트리에 *한국 시장의 현실*을 한 겹 덧대는 작업이다. 카카오의 CDC, 카카오스타일의 Bedrock, 당근페이의 Text-to-SQL, SKAI와 비트나인의 한국형 솔루션 같은 사례들이 매니지드 결정과 어떻게 맞물리는지를 함께 보자.
