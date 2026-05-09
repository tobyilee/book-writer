# Spring Batch 6 저술 계획

## 제목 후보

1. **Spring Batch 6, 운영까지 가는 길**
   - 톤: 진중하고 실무 지향. "예제 따라하기"가 아니라 "운영 시스템을 만든다"는 약속.
   - 포지셔닝: 입문자가 첫 잡을 띄우는 것에서 멈추지 않고 K8s 운영·재시작·모니터링까지 한 호흡으로 끌고 가는 책. 카카오페이·우아한형제들 사례를 backbone으로 신뢰성 강조.

2. **직접 짜본 사람을 위한 Spring Batch 6**
   - 톤: 동료처럼 말 거는 친근한 평어체. 독자의 기존 경험을 인정하고 거기서 출발하겠다는 신호.
   - 포지셔닝: "이미 배치 코드를 써봤지만 매번 재시작·재처리·메타 관리에서 막혔던 사람"을 정확히 겨냥. "결국 다시 만들게 되는 인프라가 이미 들어 있다"는 핵심 메시지를 제목에 박는다.

3. **청크와 트랜잭션, 그리고 Spring Batch 6**
   - 톤: 개념 우선·원리 지향. 약간 학구적.
   - 포지셔닝: "프레임워크 사용법"이 아니라 "배치라는 문제 자체"를 먼저 이해시키는 책. chunk-oriented가 왜 트랜잭션 모델인지부터 짚고 들어간다.

**추천: 직접 짜본 사람을 위한 Spring Batch 6**

이유 — 대상 독자(Spring에는 익숙하지만 Spring Batch는 처음, 직접 배치를 짜본 경험 있음)와 책의 핵심 약속(직접 짜다 보면 결국 다시 만들게 되는 인프라가 이미 들어 있다)이 제목 한 줄에 담긴다. 평어체 본문과도 자연스럽게 이어진다. "운영까지 가는 길"은 부제 후보로 살린다 → **"직접 짜본 사람을 위한 Spring Batch 6 — 첫 잡부터 운영까지"**.

---

## 책 특성

- **장르:** 실무서 (에세이형 기술서) — 개념 설명 + 코드 + 운영 노하우 + 한국 실제 사례를 한 호흡으로 묶은 형태
- **분량:** 본문 약 330~370 페이지 (한글 글자 수 약 23만~26만 자, 챕터당 평균 27~30 페이지)
- **난이도:** 중급 — Spring/Spring Boot 기초 가정. JDBC·트랜잭션·JPA 기본 개념 가정. Spring Batch는 처음.
- **독자 여정:**
  - **진입 상태:** "배치는 cron + 직접 짠 코드로 돌리고 있다. 재시작·실패 처리·메타 관리가 매번 골치다. Spring Batch 좋다는데 어디서부터 시작해야 할지 모르겠다."
  - **출구 상태:** "Spring Batch 6으로 잡을 설계하고, 청크 트랜잭션 경계를 의식하며 짜고, 실패한 잡을 안전하게 재시작하고, K8s에서 운영·모니터링한다. 5에서 6으로 마이그레이션도 직접 할 수 있다."
- **핵심 약속 (책 한 줄 약속):** 이 책을 다 읽고 나면 Spring Batch 6으로 production-ready 배치 시스템을 직접 설계·구현·운영할 수 있다. 첫 잡 띄우기 → 청크/트랜잭션 모델 이해 → 실전 유스케이스 → 성능 튜닝 → K8s 운영 → 5→6 마이그레이션까지, 한 사람이 하나의 시스템을 책임지는 데 필요한 모든 결정 트리를 갖춘다.
- **차별화 포인트:**
  1. Spring Batch 6 GA(2025-11-19) 변경점을 정면으로 다루는 한국어 책 (M1~GA, 6.0.1까지 추적)
  2. 카카오페이 정산 사례를 단일 챕터의 backbone으로 활용 — 단순 인용이 아닌 구조 분석
  3. K8s 운영을 1급 시민으로 다룸 (graceful shutdown, recover API, JobRepository 정리)
  4. 5에서 6으로의 마이그레이션을 별도 챕터로 — 실 운영자가 가장 필요로 하는 부분
  5. 한국 커뮤니티의 실제 질문(OOM, @StepScope, 잡 두 번 도는 문제 등)을 챕터 도입부 훅으로 활용

---

## 내러티브 아크

이 책은 **3 막 구조**로 흐른다.

**1막 (1~3장) — "왜 굳이 프레임워크냐"에 답하기.**
독자는 이미 배치 코드를 직접 짜봤다. 그래서 "Spring Batch가 왜 필요한가"를 먼저 납득시켜야 한다. 1장은 배치라는 문제 자체를 다시 정의하고("대량 + 비동기 + 시간 창"), 직접 짠 배치가 결국 부딪히는 문제(재시작·메타·트랜잭션 경계)를 짚는다. 2장은 "그래서 Spring Batch가 무엇을 해주는가"를 청크-트랜잭션-메타데이터 3축으로 설명한다. 3장은 첫 잡을 만들어 본다 — Hello, Spring Batch 단계지만, 이미 청크/트랜잭션 경계를 의식하면서, 그리고 `@StepScope`라는 한국 입문자 1번 함정을 정면으로 다루면서. 이 막을 마치면 독자는 Spring Batch가 자기 문제를 해결하는 도구임을 신체적으로 안다.

**2막 (4~7장) — 모델을 깊이 이해하고 실전에 쓴다.**
4장은 ItemReader/Processor/Writer 계약을 깊게 판다. 청크 = 트랜잭션이라는 핵심 규칙, chunk size ≠ page size ≠ fetch size 같은 흔한 혼동, Cursor vs Paging 결정 트리, 그리고 청크 모델이 안 맞는 자리를 채우는 **Tasklet의 1할**(파일 압축, 디렉터리 정리, 외부 명령 실행)까지. 5장은 Spring Batch 6의 변경점을 한 챕터로 모은다 — 신규 ChunkOrientedStepBuilder, JobOperator 통합, recover API, graceful shutdown, 그리고 **도메인 모델 record화·primitive long 전환·v5 직렬화 비호환** 같은 메이저 의미 변화까지. 4장 다음에 5장을 두는 이유는, 4장에서 모델을 이해해야 5장의 변경이 왜 필요한지 보이기 때문이다. 6장은 실전 유스케이스 backbone — **카카오페이 정산 사례를 단독 backbone으로 끌고 가는 진짜 사례 챕터**. 나머지 유스케이스 4개는 별도 부록으로 분리하여 본문 챕터의 밀도를 지킨다. 7장은 fault tolerance + 테스트 — Skip/Retry/Restart의 의미, 청크 재처리 모드, 멱등성 설계, outbox 패턴, 그리고 `spring-batch-test`로 잡을 어떻게 테스트할 것인가. 이 막을 마치면 독자는 "어떤 배치든 직접 설계할 수 있고, 테스트할 수 있다"고 느낀다.

**3막 (8~11장) — 운영, 성능, 그리고 마이그레이션.**
8장은 성능과 확장 — chunk size 튜닝, 멀티스레드 step, 파티셔닝, Remote Step. 9장은 모니터링과 옵저버빌리티 — Micrometer, Prometheus, JFR, 그리고 **알람 임계값 설계**까지 PromQL 예시로. 10장은 K8s 운영 — CronJob 패턴, graceful shutdown, recover API, JobRepository 정리(그 정리 잡을 Spring Batch로 짜는 예시까지), CommandLineJobOperator의 K8s CronJob 통합. 11장은 5에서 6으로의 마이그레이션 — 패키지 이동, JobLauncher → JobOperator, **직렬화 호환성 함정과 잡 한 개의 실제 마이그레이션 시나리오를 코드 diff로**. 분량을 30~32쪽으로 확장해 차별화 포인트로 내건 챕터답게 만든다. 이 막을 마치면 독자는 production 시스템 운영자다.

**에필로그(12장)** — **"운영 1년차 회고"** 톤. 안티패턴을 단순히 나열하는 것이 아니라, 시간 축의 회고로 풀어낸다 — 처음엔 모든 잡에 retry 걸었는데 1년 지나니 실패 분류 기준이 바뀌었다, 같은 함정에 두 번 빠지지 않는 법은 결국 자기 패턴북이라는 식. 그 위에 다른 도구(Airflow, Quartz, SCT)와의 4축 결정 표 1개, 다음 학습 로드맵을 얹는다. 토비 스타일 에세이형 마무리에 어울리는 톤.

순서의 핵심: **개념 → 모델 → 6 변경점 → 실전 → 운영 → 마이그레이션 → 회고** 의 흐름이며, 각 챕터 끝에는 다음 챕터로의 자연스러운 다리(예: "이제 청크 모델은 알았다. 그런데 6에서 이게 왜 갈아엎어졌는가?")를 둔다.

---

## 챕터 목록

### 1장. 배치라는 문제, 그리고 우리가 매번 다시 만들던 것
- **핵심 질문:** 배치 처리는 정확히 어떤 문제이고, 직접 짜다 보면 왜 결국 같은 인프라를 다시 만들게 되는가?
- **주요 내용:**
  1. 배치의 정의: 대량 + 비동기 + 시간 창 — 웹 요청 처리와 어떻게 다른가
  2. 실시간 vs 배치의 영구적 트레이드오프 (Lambda·Kappa 아키텍처에서 배치의 자리)
  3. 직접 짠 배치가 부딪히는 5가지 문제: 재시작, 부분 실패, 메타데이터, 트랜잭션 경계, 모니터링
  4. "어디까지 처리됐는지" 추적하는 코드를 직접 짜본 사람의 자기진단
  5. 결제 정산·일말 마감·데이터 마이그레이션·통계 집계·파일 ETL — 우리가 매일 만나는 배치 사례
  6. 이 책의 약속: 그 인프라를 다시 만들지 않게 해주는 도구
- **독자가 얻는 것:** 자기 코드의 어디가 약하고, 왜 프레임워크가 필요한지에 대한 명확한 자기진단
- **챕터 도입부 훅:** "어제 새벽 3시에 배치가 죽었다는 알림을 받고 노트북을 켰다. 어디까지 처리됐는지 확인하려고 DB를 뒤지고, 처리된 ID 목록을 SELECT 해서 NOT IN 절로 다시 돌리는 SQL을 짠다 — 그 SQL이 또 한 시간 걸린다." (OKKY 다수 질문, velog "Spring Batch 삽질기" 시리즈 모티브)
- **예상 분량:** 22 페이지

### 2장. Spring Batch가 약속하는 것 — 청크, 트랜잭션, 메타데이터
- **핵심 질문:** Spring Batch는 정확히 무엇을 해주고, 어떤 모델로 그것을 해주는가?
- **주요 내용:**
  1. Spring Batch의 한 줄 정의: "재실행 안전성 + 메타데이터 + 청크 트랜잭션 경계를 직접 짜지 않게 해주는 프레임워크"
  2. 3-layer 아키텍처: Application / Batch Core / Batch Infrastructure — 왜 이렇게 분리했는가
  3. Job → Step → ItemReader/Processor/Writer의 모델 그림
  4. JobInstance vs JobExecution — 재시작이 가능한 이유 (1:N 관계 도식 포함, 텍스트 도식/ASCII art로 시각화)
  5. JobRepository: 모든 실행 이력의 영구 기억
  6. chunk-oriented vs tasklet — 9 대 1 비중과 그 이유 (tasklet의 실제 자리는 4장에서 다룬다고 예고)
  7. 직접 짠 코드와의 매핑: "내가 짜던 그 부분이 여기로 옮겨진다" (이 시각이 4·5·7장에서도 박스 코너로 이어짐을 예고)
- **독자가 얻는 것:** Spring Batch의 모델을 한 그림으로 머릿속에 그리는 능력
- **챕터 도입부 훅:** "Spring Batch 공식 문서를 처음 열면 Job, Step, JobInstance, JobExecution, ExecutionContext, JobLauncher, JobRepository, JobOperator… 이름이 12개쯤 한 번에 쏟아진다. 그런데 이 모든 게 사실 한 가지 질문에 답한다 — 어디까지 처리됐는지를 어떻게 영구히 기억하느냐." (Spring Batch Reference, Architecture; SK devocean "SpringBatch 코드 설명 및 아키텍처")
- **예상 분량:** 28 페이지

### 3장. 첫 잡 띄우기 — Spring Boot 4 + Spring Batch 6, 그리고 @StepScope의 함정
- **핵심 질문:** 가장 작은 잡을 동작시키려면 무엇을 어디에 어떻게 적어야 하고, 한국 입문자 1번 함정은 어떻게 피하는가?
- **주요 내용:**
  1. Spring Initializr로 프로젝트 생성 (Spring Boot 4 + Spring Batch 6)
  2. application.yml — JobRepository를 위한 DataSource, 스키마 자동 생성, `spring.batch.job.enabled` 설정
  3. 첫 Job: "1부터 100까지 숫자를 콘솔에 출력" — Reader/Processor/Writer 직접 작성
  4. 실행하고 BATCH_JOB_INSTANCE / BATCH_JOB_EXECUTION 테이블 직접 들여다보기
  5. JobParameters로 같은 잡을 두 번 돌릴 수 있게 만들기 — JobInstance 동일성의 의미를 직접 체험
  6. `@EnableBatchProcessing`을 붙이지 말 것 — Spring Boot 자동 구성 권고
  7. 흔한 실수 1: 잡이 두 번 도는 현상, JobParameters 미설계로 "이미 실행됨" 거부
  8. **흔한 실수 2 — `@StepScope` / `@JobScope` 함정 (전용 절):**
     - JobParameters를 빈에 주입하는 사실상 유일한 표준 메커니즘
     - 늦은 빈 생성 의미: 빈 생성 시점이 Step/Job 시작 이후로 미뤄진다
     - NPE의 원인: `@StepScope` 없이 `@Value("#{jobParameters['date']}")` 주입 시 발생하는 BeanCreationException
     - SpEL late binding 작동 원리: ApplicationContext 생성 시점엔 jobParameters가 없다
     - 인터페이스 프록시 vs 클래스 프록시 — Reader/Writer를 인터페이스로 선언하지 않을 때 함정
     - 한국 커뮤니티 빈출 사례 (OKKY #380648 외)
- **독자가 얻는 것:** 작동하는 첫 잡과, 메타데이터 테이블에 자기 흔적을 남겨본 경험, 그리고 `@StepScope` 함정을 신체적으로 피해본 경험
- **챕터 도입부 훅:** "스프링 배치 시작했는데 매번 부팅할 때마다 잡이 한 번 더 돌아요." + "@StepScope 안 붙였더니 NPE가 떠요." (OKKY #268704 자동 실행 충돌 + OKKY #380648 @StepScope 함정 — 한국 입문자 1번 질문 묶음)
- **예상 분량:** 32 페이지

### 4장. ItemReader / Processor / Writer — 청크 모델 깊게 보기, 그리고 Tasklet의 1할
- **핵심 질문:** Reader/Processor/Writer 계약은 정확히 어떻게 되어 있고, chunk size·page size·fetch size는 무엇이 어떻게 다른가? 그리고 청크 모델이 안 맞는 일은 어떻게 처리하는가?
- **주요 내용:**
  1. read() / process() / write() 계약 — null의 의미가 각각 다르다 (입력 종료 vs 필터링)
  2. **청크 = 트랜잭션** — 이 한 줄이 모든 것의 출발
  3. chunk size ≠ page size ≠ fetch size — 그림으로 풀어내는 3개 개념
  4. Cursor vs Paging Reader — 메모리·트랜잭션·재시작 측면 결정 트리
  5. 내장 Reader 라인업: Flat / Jdbc / Jpa / Mongo / Json / Stax
  6. JdbcPagingItemReader 실제 사용법 — 가장 널리 쓰이는 패턴
  7. jojoldu의 QuerydslNoOffsetPagingItemReader — Querydsl + keyset 페이징 한국 표준
  8. Writer 결정 트리: JdbcBatchItemWriter는 좋고, JpaItemWriter Dirty Checking은 왜 위험한가
  9. **Reader/Writer를 JobParameters로 매개화하기 — `@StepScope` 실전 패턴** (3장과 연결: "왜 붙어야 하는가"는 3장, "어떻게 매개화하는가"는 4장)
  10. **Tasklet의 1할 자리 (전용 절):** 파일 압축·해제, 디렉터리 정리, 외부 셸 명령 실행, S3 업로드 단발 작업, FTP 다운로드 — 청크 모델로 풀면 어색해지는 일들. SystemCommandTasklet, MethodInvokingTaskletAdapter 패턴. tasklet과 chunk-oriented step의 비교 표.
  11. 박스 코너: "직접 짰을 때 vs Spring Batch 6 — Reader/Writer 매핑"
- **독자가 얻는 것:** 자기 데이터에 맞는 Reader/Writer를 정확히 고르는 결정 트리, 그리고 청크가 안 맞을 때 tasklet을 꺼내드는 감각
- **챕터 도입부 훅:** "60만 건 처리하는데 OOM이 납니다. ItemReader가 다 들고 있는 것 같아요." (OKKY #1489911 "spring batch OOM 관련 질문" — 한국 커뮤니티 OOM 케이스의 거의 모든 원인이 이 챕터의 내용)
- **예상 분량:** 36 페이지

### 5장. Spring Batch 6, 무엇이 갈아엎어졌나
- **핵심 질문:** 5에서 6으로 무엇이, 왜 변했고, 그것이 내 코드에 어떤 영향을 주는가?
- **주요 내용:**
  1. 출시 타임라인 (M1 2025-07 → GA 2025-11-19 → 6.0.1 2025-12) 과 의존성 baseline (Java 17, Spring Framework 7, Spring Boot 4)
  2. **chunk-oriented 모델 재설계** — `ChunkOrientedTasklet` deprecated, `ChunkOrientedStep` + `ChunkOrientedStepBuilder` 등장 (왜 갈아엎어졌는지 — maxItemCount·throttle·optimistic locking 이슈)
  3. **producer-consumer + bounded queue** 동시성 모델 — 이전 parallel iteration과 무엇이 다른가
  4. `@EnableJdbcJobRepository` / `@EnableMongoJobRepository` 분리 — 왜 갈라졌나
  5. `JobOperator`로의 통합 — JobLauncher / JobExplorer 흡수
  6. **`JobOperator#recover()`** — STARTED 박제 문제의 표준 해결
  7. **Graceful Shutdown** — K8s 운영자에게 가장 중요한 한 줄
  8. JFR 옵저버빌리티, JSpecify null 안정성, 람다 스타일 빌더, 신규 CommandLineJobOperator
  9. fault-tolerance 재구성 — Spring Retry 떼고 Spring Framework 7 retry로
  10. **도메인 모델·JobParameters 재설계 (전용 절 — C2 반영):**
      - 엔티티 ID `Long` → `long` (primitive 전환 — null 불가, 0이 명시적 미할당)
      - JobParameter record화 — `record JobParameter<T>(T value, Class<T> type, boolean identifying)`
      - JobParameters를 `Set<JobParameter>` 기반으로 재설계 (이전 Map 기반)
      - **v5 직렬화 비호환:** v5에서 실패한 JobInstance는 v6에서 재시작 불가 — Java 직렬화 포맷이 변경됨
      - 왜 record로 바뀌었나: 불변성·null safety·JSpecify와의 정합·Jackson 3 직렬화 표준화
      - 영향 범위: 커스텀 Listener·ExecutionContext에 도메인 객체 저장한 코드는 11장 마이그레이션 표를 참조
- **독자가 얻는 것:** 6의 변경 의도를 이해하고, 어떤 변경이 자기 코드에 영향을 주는지 빠르게 판별
- **챕터 도입부 훅:** "5에서 잘 돌던 코드를 6으로 올렸더니 패키지 import가 빨갛다. ChunkOrientedTasklet은 deprecated라고 한다. 왜 멀쩡하던 걸 바꿨을까?" (Spring Batch 6 What's New — 변경 동기 인용)
- **예상 분량:** 40 페이지

### 6장. 실전 backbone — 카카오페이 정산 사례 한 호흡
- **핵심 질문:** 실제 production 정산 시스템은 어떤 단계의 개선을 거쳤고, 그 단계마다 Spring Batch는 어떻게 쓰였는가?
- **주요 내용:**
  1. 정산이라는 도메인의 특수성: 다중 소스 ingest + intelligent matching + mismatch 처리
  2. 출발점 — 50,000건 1시간+ 처리, "쿼리 튜닝하면 됩니다"라는 가설이 왜 틀렸는가
  3. **개선 1단계 — Processor에서 외부 API 단건 호출 → Writer 일괄 처리.** I/O 묶기의 위력. 코드 diff와 트랜잭션 그림
  4. **개선 2단계 — JpaItemWriter Dirty Checking → JdbcBatchItemWriter.** Dirty Checking 비용 분석, JdbcBatchItemWriter의 batch insert가 왜 빠른가
  5. **개선 3단계 — 동일 값 UPDATE 그룹화 + IN 절** (1,000건 → 3건 IN UPDATE, 90%+ 향상). SQL 패턴, 멱등성 검토
  6. **개선 4단계 — chunk size·page size·fetch size 정렬** (8장 본격 튜닝의 예고편)
  7. 약 10배 향상의 분배: 단계별 기여도 분석
  8. 핵심 교훈: "처음부터 병렬 처리보다 현재 구조에서 I/O를 묶는 것이 효율적"
  9. **reconciliation 패턴 — 다중 소스 매칭과 mismatch 격리** (이벤트 소싱과 결합 시 60% 단축 보고 인용)
  10. 박스 코너: "직접 짰을 때 vs Spring Batch 6 — 정산 잡 매핑"
- **독자가 얻는 것:** production 정산 시스템의 단계적 진화를 자기 도메인에 적용할 수 있는 backbone 1개
- **챕터 도입부 훅:** "정산 잡이 5만 건 넘어가면서 1시간을 넘긴다. PM은 왜 이렇게 느리냐고 묻고, 우리는 '쿼리 튜닝하면 됩니다' 라고 말하지만 — 진짜 문제는 쿼리가 아닐지도 모른다." (카카오페이 정산팀 사례 인용 — tech.kakaopay.com)
- **예상 분량:** 22 페이지

> **부록 A로 분리:** 나머지 4가지 유스케이스(대용량 일괄 처리, ETL/마이그레이션, 통계·집계, 파일 ETL — 우아한형제들 주소 DB)는 본문 6장과 분리해 부록 A "유스케이스 패턴 카탈로그"(약 16쪽)로 묶는다. 본문 챕터의 밀도를 지키면서 독자가 자기 도메인에 가장 가까운 패턴을 빠르게 찾아갈 수 있게 한다. 부록은 결정 트리 카드 + 핵심 코드 스니펫 형태.

### 7장. 실패는 일어난다 — Skip, Retry, Restart, 멱등성, 그리고 잡을 어떻게 테스트할 것인가
- **핵심 질문:** 잡은 언젠가 실패한다. Spring Batch는 어떻게 실패에 대응하고, 내 Writer는 어떤 조건을 만족해야 안전하며, 이 모든 것을 어떻게 테스트하는가?
- **주요 내용:**
  1. Skip / Retry / Restart 의 의미 차이와 적용 순서 (retry → skip)
  2. fault-tolerant step 빌드 (6.0): RetryPolicy.builder, SkipPolicy, .faultTolerant()
  3. **Skip 발생 시 청크 재처리 모드** — chunk size = 1로 자동 전환되는 동작 (잘 알려지지 않음)
  4. Restart 안전성 — idempotency 3 조건 (Writer 멱등, Reader ExecutionContext 저장, 외부 부수효과 격리)
  5. STARTED 상태 박제 문제 — 6.0의 `JobOperator#recover()` 한 줄로 해결
  6. SkipListener / JobExecutionListener 패턴 — 실패 항목 별도 테이블/Slack 격리
  7. **외부 부수효과 보호 — outbox / 멱등 키 / dedupe 저장소 (S4 반영, 전용 절):**
     - 멱등 Writer만으로는 부족한 이유: 송금·이메일·푸시는 외부 시스템에 부수효과
     - outbox 패턴: 도메인 트랜잭션과 같은 트랜잭션에 outbox 행 INSERT, 별도 워커가 발행
     - 멱등 키: 외부 호출에 idempotency-key 헤더, 동일 키 재호출 시 외부가 중복 검출
     - dedupe 저장소: 처리 완료 ID를 별도 테이블에 기록, write 전 SELECT로 확인
     - 3가지 비교 표 (정확성·구현 복잡도·외부 의존성) + 송금 잡 시나리오 코드 예시
  8. 안티패턴: 비멱등 Writer + retry 조합의 위험성
  9. **잡을 어떻게 테스트할 것인가 — `spring-batch-test` 전용 절 (추가 토픽 #2 반영):**
     - JUnit 4 deprecated, JUnit 5 표준
     - `JobLauncherTestUtils`로 잡/스텝 단위 실행
     - `MetaDataInstanceFactory`로 JobParameters·StepExecution 픽스처 생성
     - chunk-level 테스트 vs end-to-end 테스트의 분리
     - in-memory JobRepository(H2) vs 통합 테스트용 실제 DB 컨테이너
     - 한국 자료에 빈약한 영역이므로 코드 예시 2~3개를 충실히
- **독자가 얻는 것:** 자기 잡이 어떤 실패에서도 안전하게 재시작 가능한지 자기진단할 수 있는 체크리스트, 그리고 그 안전성을 테스트로 증명하는 법
- **챕터 도입부 훅:** "지난주에 컨테이너가 죽었는데 잡 인스턴스가 STARTED로 박제됐다. 다시 돌리려고 했더니 '이미 실행 중'이라고 거부당해서, 결국 BATCH_JOB_EXECUTION 테이블을 직접 UPDATE 했다. 이게 정말 정답일까?" (GitHub Discussion #4532, OKKY 다수)
- **예상 분량:** 36 페이지

### 8장. 성능과 확장 — 멀티스레드, 파티셔닝, Remote Step
- **핵심 질문:** 잡이 느릴 때 어디서부터 손대야 하고, 수평 확장은 어떤 옵션이 있는가?
- **주요 내용:**
  1. **튜닝 첫 단계는 chunk size·page size·fetch size 정렬** — 권장값과 측정의 중요성 (6장에서 예고된 단계의 본격 펼침)
  2. 청크 크기를 키우는 것이 항상 좋은가 — 트랜잭션 길이, 메모리, 실패 비용 트레이드오프
  3. JDBC Batch 활용 + Connection timeout 회피 (1,000건 단위 분할)
  4. 멀티스레드 step (6.0의 producer-consumer 모델) — 가장 단순한 병렬화, restartability 약화 함정
  5. Partitioning — 입력 N등분, 워커별 독립 데이터, restartability 유지 (실무에서 가장 많이 쓰는 수평 확장)
  6. Remote Chunking — Reader는 master, Writer는 워커 분산 (process 비용이 클 때만 의미)
  7. Remote Step (6.0 신규) — Step 단위 원격 실행
  8. SEDA via Spring Integration — 메시징 기반 스테이지 분리
  9. **결정 트리:** 단일 JVM이면 멀티스레드 → 데이터 분할 가능하면 Partitioning → Process 무거우면 Remote Chunking → Step 단위 분산이면 Remote Step
- **독자가 얻는 것:** 잡이 느릴 때 무엇부터 측정하고 어떤 옵션을 어느 순서로 시도할지에 대한 명확한 결정 트리
- **챕터 도입부 훅:** "잡이 느려서 멀티스레드를 켰더니 처리 결과가 이상해졌다. 데이터가 중복 처리되거나 빠진 항목이 생긴다." (Spring Batch Reference Scalability — stateful Reader + 멀티스레드의 함정)
- **예상 분량:** 30 페이지

### 9장. 모니터링과 옵저버빌리티 — Micrometer, Prometheus, JFR, 그리고 알람 설계
- **핵심 질문:** 운영 중인 잡의 상태를 어떻게 보고, 무엇을 어떤 임계값으로 알람으로 걸어야 하는가?
- **주요 내용:**
  1. Spring Batch + Spring Boot Actuator + Micrometer 기본 구성
  2. **6.0의 변경: ObservationRegistry 빈을 컨텍스트에 등록해야 메트릭이 수집된다** (전역 정적 레지스트리 폐기)
  3. 메트릭 prefix `spring.batch.` — 어떤 메트릭이 기본 노출되나
  4. Job=trace, Step=span 트레이싱 모델
  5. micrometer-registry-prometheus + /actuator/prometheus + Grafana 대시보드 구축
  6. **JFR (Java Flight Recorder) 이벤트** — 6.0 신규, 트랜잭션 경계까지 잡힘 (저수준 흐름 분석에 활용)
  7. **알람 임계값을 어떻게 정하는가 (S2 반영, 전용 절):**
     - 정상 범위 알람 vs 추세 알람 vs 파편적 실패 알람 — 3축 분리
     - 잡 실패율: 절대값 < 5% 같은 절대 임계 + 7일 이동평균 대비 편차
     - Step 평균 처리 시간: 데이터 크기 정규화 후 +30% 이탈 감지
     - Skip 누적 추세: 일별 누적 그래프, 비율 임계
     - PromQL 표현식 예시 2~3개 (rate·increase·histogram_quantile)
     - 카카오페이 도입부 훅("1시간 → 2시간이 됐다")의 답이 이 절
  8. 운영 UI 옵션: Spring Cloud Data Flow 또는 자체 Actuator + Grafana 대시보드 (SCDF는 가볍게 — 12장 다음 학습 주제로 안내)
- **독자가 얻는 것:** 자기 잡의 health를 한 화면에 보고, 이상 신호를 사전에 감지하는 모니터링 체계 + 알람 임계값 설계 결정 트리
- **챕터 도입부 훅:** "잡이 1시간 걸리던 게 어느 날 2시간이 됐다. 데이터가 늘어서인지, 어딘가가 느려져서인지 — 어디서부터 봐야 할까?" (Spring Batch Observability docs)
- **예상 분량:** 28 페이지

### 10장. K8s에서 운영하기
- **핵심 질문:** Kubernetes 환경에서 Spring Batch 6을 production-ready로 돌리려면 무엇을 갖춰야 하는가?
- **주요 내용:**
  1. K8s `CronJob` 으로 스케줄링 — Pod-당-Job 1개 패턴
  2. Pod 그레이스풀 셧다운: terminationGracePeriodSeconds + Spring Batch 6의 graceful shutdown hook
  3. **`JobOperator#recover()`** 를 운영 워크플로우에 통합 — 컨테이너 비정상 종료 자동 복구
  4. **CommandLineJobOperator로 K8s CronJob `command:` 통합 (추가 토픽 #4 반영):** 5장 8번에서 신규 CLI 도구만 언급한 것을 여기서 실전 배치 매니페스트로. Helm 차트 + ConfigMap 패턴
  5. `restartPolicy` / `backoffLimit` 설정과 Spring Batch 재시작 의미의 차이
  6. **JobRepository 정리 잡 — 그 정리 잡을 Spring Batch로 짜는 예시 (추가 토픽 #3 반영):**
     - 메타데이터 테이블이 수천만 행으로 자라기 전에
     - 정리 잡 자체가 Spring Batch 잡인 메타→메타 케이스의 흥미로운 사례
     - JdbcCursorItemReader + JdbcBatchItemWriter로 보존 기간 초과 행 삭제
     - DELETE 트랜잭션 길이 관리 + 외래 키 순서
  7. **`StoppableStep` 인터페이스** (6.0 신규) — 외부 stop 신호에 응답하는 모든 종류의 Step
  8. 단일 Pod = 단일 Job 원칙 — cloud-native 관점의 권고
  9. ConfigMap/Secret으로 JobParameters 관리, Helm 차트 패턴
  10. **K8s 환경에서만 의미 있는 모니터링 결정 (S5 반영):** Pod 단위 메트릭(컨테이너 OOMKilled vs JVM OOM 구분), K8s Event과 JobExecution 상태 매칭, Pod 재기동 시 recover 자동 트리거 패턴 — 일반 모니터링은 9장 참조
  11. 실 운영 체크리스트: graceful shutdown, recover 연결, 정리 잡, K8s-특화 모니터링, 알람
- **독자가 얻는 것:** K8s에서 Spring Batch를 운영하는 표준 패턴과 체크리스트
- **챕터 도입부 훅:** "Pod이 OOM으로 강제 종료됐다. JobExecution은 STARTED로 박제됐고, 다음 스케줄에서 재시작이 거부됐다. — 사람이 매번 DB를 손봐야 하는 운영은 정말 운영이 아니다." (Spring Batch on Kubernetes blog, BootLabs Tech)
- **예상 분량:** 28 페이지

### 11장. Spring Batch 5에서 6으로 — 마이그레이션 실전
- **핵심 질문:** 운영 중인 5 시스템을 어떻게 6으로 안전하게 옮기는가?
- **주요 내용 (S1 반영 — 분량 확장):**
  1. 마이그레이션 전 체크리스트: Java 17+, Spring Framework 7, Spring Boot 4, Jackson 3 호환
  2. **진행 중인 JobInstance를 비우고 올린다** — 5에서 실패한 인스턴스를 6에서 재시작 불가 (5장에서 짚은 직렬화 포맷 차이의 운영 귀결)
  3. 패키지 이동 정리: `org.springframework.batch.*` → `org.springframework.batch.infrastructure.*` 등 (코드 diff 표)
  4. JobLauncher / JobExplorer 주입을 JobOperator로 전환 (코드 diff 2~3개)
  5. `@EnableBatchProcessing` 분리: 공통 + `@EnableJdbcJobRepository` 또는 `@EnableMongoJobRepository`
  6. `@EnableBatchProcessing(modular=true)` deprecated → 컨텍스트 계층 + GroupAwareJob (변환 패턴 예시)
  7. 시퀀스 이름 변경: `BATCH_JOB_SEQ` → `BATCH_JOB_INSTANCE_SEQ` 등 DB 스키마 영향 (Flyway/Liquibase 마이그레이션 SQL 예시)
  8. fault-tolerance 코드 재작성: Spring Retry → Spring Framework 7 retry, RetryPolicy.builder (before/after 코드 diff)
  9. ChunkOrientedTasklet → ChunkOrientedStepBuilder (before/after 코드 diff + 함정)
  10. Jackson 2 사용처 정리 (Jackson 3 기본) — ExecutionContext 직렬화 호환성 검증법
  11. 도메인 모델 영향: 커스텀 Listener의 JobInstance·JobExecution ID 사용처 정리 (`Long` → `long` 박싱/언박싱 NPE 위험)
  12. **잡 한 개의 실제 마이그레이션 시나리오 (전용 절 — S1 핵심):**
      - 가상 잡 1개를 골라 5.x → 6.0 코드 diff 4~5개 단계로 풀기
      - 각 단계마다 메타데이터 정합성 검증 SQL (BATCH_JOB_INSTANCE 행 수, BATCH_JOB_EXECUTION 상태 분포)
      - 롤백 시나리오 (각 단계에서 실패 시 되돌리기)
      - 단계적 마이그레이션 전략: 한 잡씩 → 메타 정합성 검증 → 트래픽 전환
- **독자가 얻는 것:** 운영 중인 시스템을 다운타임 없이 6으로 옮기는 단계별 가이드와 코드 diff 카탈로그
- **챕터 도입부 훅:** "팀에서 6.0 GA가 나왔다는 소식을 들었다. 우리는 5.x로 운영 중이고, 새 기능은 끌리는데 마이그레이션 비용을 모르겠다. 진행 중인 잡들은 어쩌지?" (Spring Batch 6.0 Migration Guide)
- **예상 분량:** 32 페이지

### 12장. 운영 1년차 회고 — 5번째 잡을 만들 때 보이는 것
- **핵심 질문:** 1년 동안 잡을 만들고 운영한 사람의 시야는 어떻게 바뀌고, Spring Batch 다음으로 무엇을 배워야 하는가?
- **주요 내용 (C3 반영 — 회고형 톤으로 재설계):**
  1. **회고 1 — 처음엔 모든 잡에 retry 걸었다.** 1년 지나니 실패 분류 기준이 바뀌었다 — 일시적 외부 의존 실패만 retry, 데이터 정합성 실패는 즉시 alert + 사람 개입. retry 남용의 운영 비용
  2. **회고 2 — 처음엔 chunk size를 크게 잡는 게 정의라고 생각했다.** 그러다 야간 배치 한 번 통째로 실패했을 때 깨달았다 — 청크 크기는 트랜잭션 길이고, 트랜잭션 길이는 실패 비용이다
  3. **회고 3 — 처음엔 Reader/Writer 결정에 너무 많은 시간을 썼다.** 패턴 5개를 알게 되자 30초 만에 결정한다. 그 5개 패턴이 무엇인지
  4. **회고 4 — 처음엔 메타데이터 테이블을 안 봤다.** 1년 지나니 BATCH_STEP_EXECUTION의 commit_count·rollback_count·skip_count로 잡의 health를 본다
  5. **회고 5 — 처음엔 K8s graceful shutdown을 몰랐다.** Pod 두 번 죽이고 알았다 — 책 한 권을 읽기 전에 한 번 죽여보는 사람도 있다는 걸
  6. **회고 6 — 같은 함정에 두 번 빠지지 않는 법은 결국 자기 패턴북이다.** 책의 안티패턴 체크리스트(트랜잭션 미설계 / 메모리 폭주 / 비멱등 Writer / cursor + 외부 API / 멀티스레드 + stateful Reader / JobParameters·@StepScope 미스 / 자동 실행 충돌 / graceful shutdown 미설계 / 메타 누적)는 한 페이지로 통합 — 더 이상 펼쳐 설명하지 않는다, 본문이 자세하다
  7. **다른 도구와의 4축 결정 표 (N4 반영 — 통합 표):**
     - 4축: 스케줄링 / 잡 신뢰성 / DAG 오케스트레이션 / 단발성 작업
     - 비교: Spring Batch / Quartz / Airflow / Spring Cloud Task / SCDF
     - "잡 하나의 내부 신뢰성"(Spring Batch) vs "잡들 사이의 오케스트레이션"(Airflow)은 보완적
  8. **다음 학습 로드맵:** Spring Cloud Data Flow (운영 UI / 잡 의존성 그래프), Spring Cloud Task (단발성 작업), 6.0 이후 follow-up 영역 (JFR 운영 사례, MongoDB JobRepository 후기, Boot 4 통합 사례)
  9. 마지막 한 마디 — 직접 짜본 사람이 Spring Batch를 만난 뒤 1년이 흐른 자리
- **독자가 얻는 것:** 시간 축의 회고를 통한 운영 감각 + 한 페이지 안티패턴 체크리스트 + 4축 결정 표 + 다음 학습 로드맵
- **챕터 도입부 훅:** "이제 첫 잡이 아니라 5번째 잡을 만든다. 패턴이 보이기 시작하고, 같은 함정에 두 번 빠지진 않는다 — 빠진 적 있는 함정에 한해서." (책 전체 회고 톤)
- **예상 분량:** 14 페이지

### 부록 A. 유스케이스 패턴 카탈로그 (S3 반영)
- **목적:** 6장이 카카오페이 정산 backbone에 집중하면서 빠진 4가지 유스케이스를 결정 트리 카드 + 핵심 코드 스니펫 형태로 묶어 본문 밀도를 지킨다
- **포함 유스케이스:**
  1. 대용량 데이터 일괄 처리 — JdbcPagingItemReader + JDBC batch insert + 파티셔닝 (4쪽)
  2. ETL / 데이터 마이그레이션 — chunking + retry/skip + restart로 신뢰성 layer 구축 (4쪽)
  3. 통계·집계 — Step 흐름과 ExecutionContext의 자연스러운 결합 (4쪽)
  4. 파일 ETL — FlatFileItemReader / JsonItemReader / StaxEventItemReader (우아한형제들 주소 DB 사례) (4쪽)
- **형식:** 각 유스케이스마다 "언제 이 패턴인가 → Reader/Writer 결정 → 핵심 코드 30~40줄 → 함정 1~2개" 카드 구조
- **예상 분량:** 16 페이지

---

## 합계 분량

12개 챕터 + 부록 A = **약 364 페이지**
- 1장 22p + 2장 28p + 3장 32p + 4장 36p + 5장 40p + 6장 22p + 7장 36p + 8장 30p + 9장 28p + 10장 28p + 11장 32p + 12장 14p + 부록 A 16p
- 본문 합계 약 348p (목표 330~370 범위 안)
- 부록 포함 364p

## 변경 요약 (라운드 1 리뷰 피드백 반영 결과)

**Critical 4개 — 모두 반영:**
- C1 (`@StepScope` 함정): 3장에 전용 절(8번) 신설 + 4장 9번에 실전 매개화 패턴 + 12장 안티패턴 체크리스트에 추가. 분량 +6쪽
- C2 (5장 도메인 모델 record화·primitive long·v5 직렬화 비호환): 5장 10번에 전용 절 신설. 분량 38→40쪽
- C3 (12장 회고형 재설계): 안티패턴 9개 나열 → "운영 1년차 회고 6개 + 한 페이지 체크리스트"로 톤 전환. 분량 20→14쪽 축소, 6쪽을 11장(+4)·5장(+2)에 분배
- C4 (tasklet 1할 자리): 4장 10번에 전용 절 신설(파일 압축, 디렉터리 정리, SystemCommandTasklet, 비교 표)

**Should 권장 5개 중 5개 모두 반영:**
- S1 (11장 마이그레이션 분량 확장): 26→32쪽, 12번 절에 잡 한 개의 실제 마이그레이션 시나리오를 코드 diff + 메타 정합성 검증 SQL로
- S2 (9장 알람 설계): 7번 전용 절로 분리, PromQL 예시 포함, 26→28쪽
- S3 (6장 유스케이스 5개 압축): 카카오페이 정산 단독 backbone(22쪽)으로 축약 + 나머지 4개를 부록 A "유스케이스 패턴 카탈로그"(16쪽)로 분리
- S4 (7장 outbox 패턴 확장): 7번 전용 절로 outbox·멱등 키·dedupe 비교 표 + 송금 잡 코드 예시
- S5 (10장 모니터링 9장과 분리): 10번을 K8s 환경 특화 결정으로 좁힘 (Pod OOMKilled vs JVM OOM, K8s Event 매칭)

**Nice-to-have 4개 중 3개 반영:**
- N1 (2장 분량 축소): 30→28쪽 (6번·7번 일부를 4장·후속 챕터로 분산 시그널)
- N2 ("직접 짠 코드 vs Spring Batch 6" 박스 코너): 4장·6장에 박스 코너 명시, 5·7장으로도 확장 가능 시그널
- N3 (2장 다이어그램): 4번에 텍스트 도식/ASCII art 명시
- N4 (12장 4축 결정 표 통합): 12장 7번에 단일 통합 표로

**추가 권장 토픽 5개 중 4개 반영:**
- #1 (`@StepScope`): 3장 8번 + 4장 9번 (C1과 동일)
- #2 (테스트 전략): 7장 9번에 `spring-batch-test` 전용 절 신설
- #3 (JobRepository 정리 잡 자체 구현): 10장 6번 본격화
- #4 (CommandLineJobOperator로 K8s CronJob 통합): 10장 4번 본격화
- #5 (reconciliation 패턴): 6장 9번에 흡수 (다중 소스 매칭 + mismatch 격리, 이벤트 소싱 60% 단축 인용)

---

## 리서치 한계 반영

리서치 문서 11절에 적힌 한계를 챕터에 다음과 같이 반영:
- **Spring Cloud Data Flow:** 9장(운영 UI 옵션) + 12장(다음 학습 주제)에서 가볍게 — 깊게 다루지 않음을 명시
- **Reddit/GitHub Discussions 1차 인용 부족:** 챕터 도입부 훅을 OKKY/카카오페이/우아한형제들 등 한국 자료 위주로 구성하여 보완
- **JFR / MongoDB JobRepository 운영 후기 부족:** 9장(JFR), 5장(MongoDB)에서 "신기능 소개 + follow-up 필요" 톤으로 정직하게 표시
- **Boot 4 통합 사례 부족:** 3장과 11장에서 공식 가이드 기반으로만 다루고, "production 사례는 누적 중"임을 명시

## 한국 커뮤니티 인사이트 활용 매핑

각 챕터 도입부 훅과 본문 사례에서 활용한 커뮤니티 자료:
- 1장: OKKY 운영 질문 종합, velog "Spring Batch 삽질기"
- 3장: OKKY #268704 (잡 두 번 도는 문제) + **OKKY #380648 (`@StepScope` 함정)** — 한국 입문자 1번 질문 묶음
- 4장: OKKY #1489911 (OOM)
- 6장: 카카오페이 정산팀 (성능 향상 4단계 backbone), 부록 A는 우아한형제들 (주소 DB)
- 7장: GitHub Discussion #4532 (STARTED 박제), OKKY 다수
- 8장: 멀티스레드 + stateful Reader 함정 — Spring Batch Reference + OKKY
- 10장: Spring Batch on Kubernetes blog
- 11장: Spring Batch 6.0 Migration Guide
