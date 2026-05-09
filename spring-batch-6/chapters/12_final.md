# 12장. 운영 1년차 회고 — 5번째 잡을 만들 때 보이는 것

이제 첫 잡이 아니라 5번째 잡을 만든다고 해보자. 첫 잡 띄울 때처럼 공식 문서를 처음부터 다시 읽지 않는다. JobBuilder 시그니처도 외울 만큼 익숙해졌고, JobParameters에 식별자를 넣는 일도 자연스럽다. 챕터 9에서 깐 메트릭이 평소 모양으로 그래프에 누적돼 있고, 새벽에 박제된 메타를 손으로 푸는 일은 거의 사라졌다. 그러면서 한 가지가 분명해진다 — **첫 잡을 만들 때 보이지 않던 것들이 5번째 잡을 만들 때는 보인다.**

그 회고를 한 번 적어보고 싶다. 안티패턴을 줄지어 나열하기보다, 시간 축의 회고로 풀어보자. 처음에는 이렇게 했는데 1년 지나니 이렇게 바뀌었다는 식의 이야기. 그 회고 끝에 한 페이지짜리 안티패턴 체크리스트와 다른 도구와의 4축 결정 표, 그리고 다음 학습 로드맵을 얹자.

## 12.1 회고 1 — 처음엔 모든 잡에 retry를 걸었다

처음 fault-tolerant step을 알게 됐을 때, 모든 잡에 retry를 걸어두는 게 안전한 줄 알았다. 어차피 일시적 오류는 생길 수 있고, retry 한 번 더 시도해서 통과하면 좋은 거니까. 잡 정의를 새로 짤 때마다 `.retryLimit(3).retry(Exception.class)`를 거의 반사적으로 넣었다.

1년 지나니 그 반사가 부끄러워진다. **retry는 "일시적 외부 의존 실패"에만 의미가 있다.** 데이터 정합성 실패 — 예를 들어 정산 금액이 음수로 계산되거나, 외래 키가 없는 row를 참조한다거나 — 같은 실패는 retry로 풀리지 않는다. retry해봤자 같은 데이터가 같은 결과를 만든다. 거기에 retry를 걸어두면 같은 실패가 N번 반복돼 메트릭만 더럽혀지고, 진짜 문제 발견은 N번의 retry 시간만큼 늦어진다.

지금은 잡 정의에 retry를 넣을 때 두 가지를 묻는다.

- **이 예외가 일시적인가?** 네트워크 timeout, DB lock contention, 외부 API 5xx — 이런 건 retry 의미 있다.
- **재시도하면 다른 결과가 나올 가능성이 있는가?** 데이터 검증 실패는 다른 결과가 안 나온다.

이 두 질문에 모두 "예"인 예외만 retry 대상에 넣고, 나머지는 즉시 fail + alert로 보낸다. 사람이 들여다봐야 할 자리는 사람이 빨리 보게 만드는 게 맞다. **retry가 알람을 늦추는 도구가 되면 안 된다.**

## 12.2 회고 2 — 처음엔 chunk size를 크게 잡는 게 정의라고 생각했다

성능 튜닝 관련 글을 읽다 보면 "chunk size를 키우면 처리량이 올라간다"는 말이 자주 나온다. 그래서 한동안 chunk size 1,000 정도가 기본값이라고 생각하고 거의 모든 잡에 그 값을 박았다. 처리량이 분명히 올라가니까 만족스러웠다.

그러다 어느 날 야간 배치가 통째로 한 번 실패했다. 청크 999개까지 잘 처리됐는데, 마지막 청크의 한 항목에서 외부 API가 timeout 났다. 청크 = 트랜잭션이라는 규칙대로 그 청크 1,000건이 통째로 롤백됐고, **이미 외부 시스템에 부수효과를 보낸 상태였다.** 그날 새벽 사람이 들어가 외부 시스템과의 정합을 손으로 맞췄다.

그때 깨달은 한 줄이 이렇다. **청크 크기는 트랜잭션 길이고, 트랜잭션 길이는 실패 비용이다.** chunk size 1,000과 chunk size 100의 처리량 차이는 보통 30~40% 수준이지만, 한 청크가 실패했을 때 롤백되는 양은 10배 차이다. 외부 부수효과가 있는 잡이라면 큰 청크가 위험하다. 4장에서 다룬 것처럼, 외부 효과가 있으면 outbox 패턴이 짝을 이뤄야 하고, 그것까지 함께 설계되지 않은 잡에 큰 청크는 시한폭탄이다.

지금은 chunk size를 결정할 때 이렇게 본다.

- **순수 RDB → RDB 잡:** 청크 1,000~2,000도 무방. 트랜잭션 롤백이 안전하다.
- **외부 API 동반 잡:** 청크 100~300, outbox 패턴과 짝. 한 청크 실패 비용을 작게.
- **메모리 큰 객체를 다루는 잡:** 청크를 키우면 메모리도 함께 커진다. 50~200으로 보수적.

처리량이 30% 더 빠른 것보다, 야간에 잠을 자는 게 1년 운영자에게는 더 가치가 크다. 작은 차이가 1년의 잠을 결정한다.

## 12.3 회고 3 — 처음엔 Reader/Writer 결정에 너무 많은 시간을 썼다

첫 잡을 만들 때 Reader 결정에만 반나절을 썼다. JdbcCursor냐 JdbcPaging이냐, JpaPaging은 어떤가, Querydsl도 있는데 그건 또 어떻게 다른가. 공식 문서를 뒤지고, 블로그를 비교하고, "어떤 게 더 좋은가"를 찾으려 했다. 결국 한 번에 결정하지 못하고, 일단 간단한 JdbcCursor로 시작했다가 OOM이 한 번 나서 JdbcPaging으로 옮겼다.

1년 지나니 Reader 결정에 30초도 안 쓴다. 패턴 5개가 머릿속에 자리잡았기 때문이다.

| 데이터 출처 | 데이터 크기 | 결정 |
|---|---|---|
| 파일 (CSV/TSV) | - | `FlatFileItemReader` |
| 파일 (JSON) | - | `JsonItemReader` |
| 파일 (XML) | - | `StaxEventItemReader` |
| RDB, 작은 데이터 (수만 건 이내) | 단순 | `JdbcCursorItemReader` |
| RDB, 큰 데이터 (수십만+) | 단순 SQL | `JdbcPagingItemReader` |
| RDB, 큰 데이터 (수십만+) | 복잡 SQL | `QuerydslNoOffsetPagingItemReader` (jojoldu) |

5개면 거의 모든 잡이 풀린다. 이 5개를 외우는 데는 한나절이면 되지만, 외우지 않은 채로 매번 문서를 뒤지면 잡마다 반나절이 사라진다.

Writer 쪽은 더 단순하다.

- **RDB INSERT/UPDATE:** `JdbcBatchItemWriter` (JpaItemWriter는 피한다 — Dirty Checking 비용이 크다)
- **파일 출력:** `FlatFileItemWriter` / `JsonFileItemWriter`
- **외부 API:** 직접 작성 + 멱등 키 + outbox 패턴

이 패턴 카탈로그가 머릿속에 자리잡으면, "잡을 어떻게 짤까"의 사고가 결정 트리에서 바로 출발한다. 처음의 반나절이 30초가 되는 그 차이가, 5번째 잡을 만들 때 첫 잡과 다른 가장 큰 변화 하나다.

## 12.4 회고 4 — 처음엔 메타데이터 테이블을 안 봤다

첫 잡을 띄우고는 잡이 잘 도는 줄로만 알았다. 잡이 끝나면 로그에 "Job: [SimpleJob: [name=...]] completed with the following parameters"가 찍히고, 그게 OK 신호였다. 메타 테이블은 "Spring Batch가 자기 알아서 쓰는 곳" 정도로만 알고 있었다.

1년 지나니 메타 테이블이 운영의 일급 시민이 된다. 잡의 health를 보는 1차 수단이 메트릭이 아니라 SQL이 됐다.

```sql
SELECT
    JOB_NAME,
    DATE(START_TIME) AS run_date,
    STATUS,
    SUM(SE.READ_COUNT) AS read_total,
    SUM(SE.WRITE_COUNT) AS write_total,
    SUM(SE.WRITE_SKIP_COUNT) AS skip_total,
    SUM(SE.COMMIT_COUNT) AS commit_total,
    SUM(SE.ROLLBACK_COUNT) AS rollback_total
FROM BATCH_JOB_EXECUTION JE
JOIN BATCH_JOB_INSTANCE JI ON JE.JOB_INSTANCE_ID = JI.JOB_INSTANCE_ID
JOIN BATCH_STEP_EXECUTION SE ON JE.JOB_EXECUTION_ID = SE.JOB_EXECUTION_ID
WHERE JE.START_TIME >= NOW() - INTERVAL '14 days'
GROUP BY JOB_NAME, DATE(START_TIME), STATUS
ORDER BY run_date DESC, JOB_NAME;
```

이 한 쿼리에 잡의 health가 거의 다 들어 있다. `commit_count`와 `rollback_count`의 비율이 평소와 다르면 retry/skip 정책이 어긋난 신호다. `read_count`와 `write_count`의 차이가 갑자기 벌어지면 process에서 필터링이 늘어났거나 뭔가 비정상이다. `skip_count`가 누적되는 추세를 보면 데이터 품질이 어떻게 변하고 있는지 보인다.

이게 운영의 자기진단 도구가 된다. 사고가 나기 전에 조짐을 본다는 건 결국 평소 모양을 안다는 것이고, 평소 모양은 메타 테이블이 가장 정직하게 기록하는 자리다. 메트릭이 손에 익기 전에는, **메타 테이블을 직접 SELECT해 보는 습관**이 가장 빠른 학습이다.

## 12.5 회고 5 — 처음엔 K8s graceful shutdown을 몰랐다

K8s 위에 Spring Batch를 올렸을 때, "잘 돈다"는 신호 한 가지만 있으면 만족했다. CronJob 스케줄로 잡이 뜨고, 처리되고, 끝나고. 잡이 잘 도는 동안에는 graceful shutdown이라는 단어를 들어볼 일이 없었다.

Pod이 두 번 죽고 나서 알았다. 한 번은 노드 재부팅에서, 한 번은 OOMKilled에서. 둘 다 잡이 진행 중에 SIGKILL을 맞았고, 둘 다 JobExecution이 STARTED로 박제됐고, 둘 다 다음 스케줄에서 거부당했다. 새벽에 호출되는 빈도가 한 달에 두세 번이 되자 운영이 운영이 아니게 됐다.

graceful shutdown과 `JobOperator#recover()` 한 쌍을 알게 된 건 그 무렵이었다. 6.0의 두 가지 변경이 정확히 이 통증을 푸는 자리에 있다는 사실이, 책을 한 권 읽고 한 번에 알게 되지는 않는다 — **한 번 죽여보고 나서야 진가가 보인다.** 어떤 이는 책 한 권을 읽기 전에 한 번 죽여보고, 어떤 이는 읽고 나서도 한 번 죽여보고서야 비로소 그 한 줄의 의미를 안다.

지금은 새 잡을 K8s에 띄울 때 10장의 체크리스트 9가지를 반사적으로 적용한다. `concurrencyPolicy: Forbid`, `backoffLimit: 0`, `restartPolicy: Never`, `terminationGracePeriodSeconds: 60`, init container의 자동 recover, JobRepository 정리 잡 — 이 묶음이 첫 줄부터 들어가 있다. 한 번 죽여본 뒤에 만든 패턴북이다.

## 12.6 회고 6 — 같은 함정에 두 번 빠지지 않는 법은 결국 자기 패턴북이다

여기까지 다섯 가지 회고를 쓰면서 한 가지가 분명해졌다. **같은 함정에 두 번 빠지지 않는 가장 확실한 방법은, 빠진 함정을 자기 언어로 적어두는 일이다.** 책에 적힌 안티패턴을 읽는 것과, 자기가 직접 한 번 빠져보고 자기 손으로 적은 메모는 무게가 다르다. 책의 안티패턴은 "그런 일이 있다더라"이지만, 자기 메모는 "그날 새벽에 내가 그랬다"이다.

이 책의 안티패턴을 한 페이지로 압축해두자. 더 이상 펼쳐 설명하지 않는다 — 본문 1장부터 11장까지가 이미 자세하다. 지금 이 페이지는 1년 후에 다시 펼쳐볼 자리다.

### 안티패턴 체크리스트 — 한 페이지

- **트랜잭션 미설계.** 청크 = 트랜잭션이라는 규칙을 모르고 짠 잡. 부분 처리·이중 처리에 당한다. (4·6장)
- **메모리 폭주(OOM).** Reader가 모든 데이터를 한 번에 들고 있다. PagingReader/CursorReader/Querydsl no-offset reader 중 하나로 강제. (4장)
- **비멱등 Writer + retry.** 같은 청크를 두 번 받으면 결과가 달라진다. UPSERT/dedupe key/outbox 중 하나는 거의 필수. (7장)
- **cursor + 외부 API 동기 호출.** DB 락이 길게 잡혀 다른 잡과 충돌. Paging Reader 또는 reader/processor 분리. (7·8장)
- **멀티스레드 step + stateful Reader.** 데이터 손실/중복. restartability 원하면 Partitioning으로. (8장)
- **JobParameters 식별자 누락.** "이미 동일 인스턴스가 있다"고 거부당함. 일자/run.id 식별자 필수. (3장)
- **`@StepScope` 누락.** JobParameters를 빈에 주입하려면 늦은 빈 생성이 필수. NPE의 1번 원인. (3·4장)
- **자동 실행 충돌.** Spring Boot 자동 실행 + 수동 launch가 겹쳐 잡이 두 번 돈다. `spring.batch.job.enabled=false` 또는 `spring.batch.job.name`. (3장)
- **graceful shutdown 미설계.** Pod 종료 시 STARTED 박제. 6.0 graceful shutdown + recover()로 해결. (10장)
- **메타데이터 무한 누적.** 보존 기간 정리 잡 없으면 BATCH_* 테이블이 수천만 행. 정리 잡 등록(보존 기간 90~180일). (10장)

이 10가지가 1년차에 한 번씩은 만나는 함정이다. 이 페이지에 자기 함정을 한두 개 더 추가해 자기 패턴북으로 만들자. 그게 5년차에 도움이 된다.

## 12.7 다른 도구와의 4축 결정 표 — 잡 하나의 신뢰성 vs 잡들 사이의 오케스트레이션

운영 1년차에 한번쯤은 누군가 묻는다 — "Airflow 안 쓰고 왜 Spring Batch?" 또는 그 반대. 처음엔 답하기 모호한 질문이었지만, 둘을 다 써보거나 비교해보면 둘이 보완적이라는 사실이 분명해진다. 각자 다른 자리를 잡는다.

다른 도구와의 위치를 4축으로 정리한 표 하나로 답하자.

| 도구 | 잡 1개 신뢰성 | 잡들 사이 DAG | 스케줄링 | 단발성 작업 |
|---|---|---|---|---|
| **Spring Batch** | ★★★★★ | ★ | ★★ (Spring + cron) | ★★ |
| **Quartz** | ★★ | ★ | ★★★★★ | ★★ |
| **Airflow** | ★★ | ★★★★★ | ★★★★ | ★★ |
| **Spring Cloud Task** | ★★★ | ★★ | ★★ | ★★★★★ |
| **Spring Cloud Data Flow** | ★★★★ (Batch 위) | ★★★★ | ★★★★ | ★★★★ |

핵심 한 줄.

- **Spring Batch:** "잡 1개의 내부 신뢰성"에 강하다. 청크 트랜잭션, 재시작, 메타데이터, fault-tolerance.
- **Quartz:** 단순 스케줄링 엔진. cron 이상의 시간 표현, 클러스터 모드. 잡 내부의 신뢰성은 직접 짜야 한다.
- **Airflow:** "잡들 사이의 DAG 오케스트레이션"에 강하다. 시각화, 의존성, 백필. 잡 1개 내부 신뢰성은 사용자 코드 영역.
- **Spring Cloud Task:** 단발성 작업(한 번 돌고 끝나는 컨테이너)에 특화. Spring Batch 잡을 Task로 감싸 K8s에서 1회성 실행.
- **Spring Cloud Data Flow:** Batch + Task를 운영 UI/DAG로 묶어주는 상위 레이어.

**Spring Batch와 Airflow는 보완적이다.** Airflow가 잡들 사이의 흐름을 지휘하고, 각 잡 내부는 Spring Batch가 책임진다는 모양이 흔하다. 둘 중 하나만 쓰는 것보다 둘을 짝지어 쓰는 모양이 많은 운영에서 자연스럽다.

규모가 작다면 Spring Batch만으로 충분하다. 잡이 10개를 넘기 시작하고 잡 사이의 의존성이 생기면 Airflow나 Spring Cloud Data Flow를 검토할 때다. 그 시점이 자연스럽게 온다 — 첫 잡 띄울 때 미리 걱정할 자리가 아니다.

## 12.8 다음 학습 로드맵 — 이 책 너머

이 책을 다 읽고 1년쯤 운영해본 사람을 위한 다음 학습 주제 셋을 권한다.

**1. Spring Cloud Data Flow.** 잡이 늘기 시작하면 자연스럽게 만나는 상위 레이어. 잡 의존성 그래프, 운영 UI, 잡 launch 화면. 한국 운영 사례가 아직 두텁지 않은 영역이라 자기가 처음으로 한국어 사례를 쓸 수도 있다.

**2. Spring Cloud Task.** 단발성 컨테이너 잡. K8s Job 리소스와 짝이 잘 맞고, Spring Batch 잡을 Task로 감싸 한 번 돌고 끝나는 운영 패턴이 자연스럽다.

**3. 6.0 이후 follow-up 영역.** JFR 운영 사례 누적, MongoDB JobRepository 운영 후기, Spring Boot 4 production 통합 사례. 6.0 GA 직후라 1차 자료가 아직 모이는 중이다. 자기 운영 경험을 기술 블로그로 적기 시작하면, 그게 다음 한국 운영자의 1차 자료가 된다.

이 셋 중 어느 것을 먼저 갈지는 자기 잡의 규모와 성격에 달렸다. 잡이 적고 운영 UI가 절실하면 SCDF가 첫 줄, 단발성 작업이 많으면 Task가 첫 줄, 글을 쓰는 게 즐거우면 follow-up 글이 첫 줄이다.

## 12.9 마지막 한 마디 — 직접 짜본 사람이 1년이 흐른 자리

이 책을 처음 펼쳤을 때, 우리는 직접 배치를 짜본 사람이었다. cron + 직접 짠 코드로 야간 배치를 돌리고 있었고, 재시작·실패 처리·메타 관리에서 매번 골치였고, "어디까지 처리됐는지" 추적하는 SQL을 자기 손으로 짜고 있었다. 그게 1막의 시작점이었다.

1년이 흐른 자리는 어떻게 다른가. 청크 트랜잭션 경계가 자연스럽게 의식되고, JobParameters 식별자가 잡 설계의 1단계로 들어가고, K8s에서 Pod이 죽어도 시스템이 스스로 일어나는 모양을 만들 줄 안다. 5번째 잡을 만들 때 Reader 결정에 30초가 걸리고, 메타 테이블의 SQL이 잡 health 점검 도구가 됐다.

그러면서 한 가지가 분명해졌다 — **결국 다시 만들게 되는 인프라가 이미 들어 있다는 책의 약속은, 직접 짜본 사람에게 가장 정확한 약속이었다.** Spring Batch를 처음 만났을 때의 의문 — "왜 굳이 프레임워크냐" — 의 답은 1년 운영해본 자리에 와 있다. 직접 짜다 보면 결국 같은 인프라를 다시 만들게 되고, 그 인프라를 자기 손으로 만드는 비용보다 이미 들어 있는 도구를 신체적으로 익히는 비용이 훨씬 작다.

새벽 3시에 호출받지 않는 잡을 만드는 일, 평시의 모양이 그래프로 누적되어 어느 날 모양이 변할 때 알아채는 일, 박제된 메타를 손으로 풀지 않는 일 — 이 모든 게 6의 도구가 받쳐주는 자리다. 1년차에 이 자리에 도착했다면, 5년차에는 더 좋은 자리에 가 있을 것이다.

이 책을 덮고 나면 그 다음 잡을 짜는 일이 기다린다. 패턴북에 자기 함정을 하나씩 적어가면서, 자기 운영 경험을 한국 커뮤니티에 한 줄씩 쓰면서. 그게 이 책의 진짜 약속이고, 1년 후 다시 펼칠 책의 모양이다.

5번째 잡을 만들 때, 그리고 50번째 잡을 만들 때 — 부디 잘 자길 바란다.
