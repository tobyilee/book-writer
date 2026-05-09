# 직접 짜본 사람을 위한 Spring Batch 6

> 첫 잡부터 운영까지 — Spring Batch 6으로 production-ready 배치 시스템을 직접 설계·구현·운영하기 위한 한 권의 실전 가이드.

- **저자:** Toby-AI
- **버전:** v1.0.0
- **발행일:** 2026-05-09
- **언어:** ko
- **분량:** 12개 챕터 + 부록 A / 본문 약 24만 자

## 이 책은 무엇인가

이 책은 Spring과 Spring Boot에 익숙하지만 Spring Batch는 처음인 개발자를 위한 실전 가이드다. cron + 직접 짠 코드로 배치를 돌려본 사람이 매번 다시 만들게 되는 인프라 — 재시작, 부분 실패, 메타데이터, 트랜잭션 경계, 모니터링 — 가 Spring Batch 6 안에 이미 들어 있다는 사실을 신체적으로 납득시키는 데서 출발한다.

배치 처리는 정확히 어떤 문제이고, 청크와 트랜잭션은 왜 같은 것인가. 첫 잡을 띄우고 메타 테이블에 자기 흔적을 남기기까지 어디서 막히는가. `@StepScope`는 왜 한국 입문자 1번 함정인가. Spring Batch 6은 5에서 무엇을, 왜 갈아엎었고, 그것이 내 코드에 어떤 영향을 주는가. 이 책은 이런 질문 하나하나에 사례와 코드 diff로 답한다.

차별화 포인트는 세 가지다. 첫째, Spring Batch 6 GA(2025-11-19)의 변경점을 정면으로 다루는 한국어 책이다 — `ChunkOrientedStepBuilder` 등장, JobOperator 통합, recover API, 그리고 v5 직렬화 비호환 같은 메이저 의미 변화까지. 둘째, 카카오페이 정산 사례를 단일 챕터의 backbone으로 해부한다 — 단순 인용이 아니라, 50,000건 1시간+ 처리에서 약 10배 향상까지 이르는 단계별 의사결정을 코드 diff로 따라간다. 셋째, K8s 운영을 1급 시민으로 다룬다 — CronJob 패턴, graceful shutdown, JobRepository 정리(그 정리 잡을 Spring Batch로 짜는 예시까지).

마지막에는 "운영 1년차 회고"가 따라온다. 처음엔 모든 잡에 retry를 걸었지만 1년 지나면 실패 분류 기준이 바뀐다는, 시간 축의 회고로 안티패턴을 풀어낸다.

## 누구를 위한 책인가

이 책은 다음과 같은 자리에 서 있는 개발자를 정확히 겨냥한다.

- Spring/Spring Boot 기초가 있고, JDBC·트랜잭션·JPA의 기본 개념을 안다.
- 배치는 cron + 직접 짠 코드로 돌려본 적이 있다. 새벽에 죽은 잡을 어디까지 처리됐는지 확인하려고 DB를 뒤져본 경험이 있다.
- 재시작·실패 처리·메타 관리가 매번 골치였고, Spring Batch가 좋다는 말은 들었지만 어디서 시작해야 할지 막막하다.
- 5에서 6으로 마이그레이션해야 하는데 변경점이 많아서 어디부터 손대야 할지 모르겠다.

다 읽고 나면 이 자리에 있게 된다.

- Spring Batch 6으로 잡을 설계하고, 청크 트랜잭션 경계를 의식하며 짠다.
- 실패한 잡을 안전하게 재시작할 수 있고, 자기 Writer가 멱등한지 자기진단한다.
- chunk size·page size·fetch size를 정렬하고, 필요하면 파티셔닝·Remote Step으로 확장한다.
- K8s에서 graceful shutdown과 JobRepository 정리까지 운영한다.
- 5에서 6으로의 마이그레이션을 코드 diff 수준으로 직접 수행할 수 있다.

## 무엇을 얻게 되는가

- 배치라는 문제 자체를 다시 정의하는 시각 — 직접 짠 코드가 부딪히는 5가지 문제와 그 자기진단 체크리스트
- Spring Batch의 모델을 한 그림으로 머릿속에 그리는 능력 — 청크 = 트랜잭션, JobInstance vs JobExecution, ExecutionContext의 의미
- 첫 잡을 띄우면서 `@StepScope` 함정을 신체적으로 피해본 경험과, JobParameters로 빈을 매개화하는 표준 패턴
- ItemReader/Processor/Writer 결정 트리 — Cursor vs Paging, JdbcBatchItemWriter의 자리, JpaItemWriter Dirty Checking이 위험한 이유
- Spring Batch 6 변경점의 의도와 영향 범위 — `ChunkOrientedStepBuilder`, `JobOperator#recover()`, graceful shutdown, JobParameter record화, v5 직렬화 비호환
- 카카오페이 정산 사례 단계별 해부 — I/O 묶기, Dirty Checking 제거, IN UPDATE 그룹화, chunk size 정렬로 약 10배 향상에 이르는 backbone
- Skip/Retry/Restart 의미 차이와 idempotency 3 조건, outbox·멱등 키·dedupe 저장소 비교
- `spring-batch-test`로 잡을 테스트하는 법 — 한국 자료에 빈약한 영역의 충실한 코드 예시
- 성능 튜닝 결정 트리 — chunk size·멀티스레드 step·파티셔닝·Remote Step
- Micrometer + Prometheus + JFR을 결합한 알람 임계값 설계 (PromQL 예시 포함)
- K8s CronJob 패턴, graceful shutdown, JobRepository 정리 잡 — production 운영자에게 필요한 모든 결정 트리
- 5에서 6으로의 마이그레이션 시나리오 — 직렬화 함정과 잡 한 개의 실제 코드 diff
- 운영 1년차 회고 — 시간 축으로 본 안티패턴, 다른 도구(Airflow·Quartz·SCT)와의 4축 결정 표

## 차례

1. **배치라는 문제, 그리고 우리가 매번 다시 만들던 것** — 직접 짠 배치가 부딪히는 다섯 가지 문제와 자기진단 체크리스트.
2. **Spring Batch가 약속하는 것 — 청크, 트랜잭션, 메타데이터** — 3-layer 아키텍처와 12개 이름이 답하는 단 하나의 질문.
3. **첫 번째 잡 만들기 — 그리고 @StepScope 함정** — Spring Boot 4 + Spring Batch 6 첫 잡, JobParameters 식별성, `@StepScope`의 늦은 빈 생성과 클래스 프록시.
4. **ItemReader/Processor/Writer 계약 — 그리고 Tasklet의 1할** — read/process/write null 의미, chunk size ≠ page size ≠ fetch size, Cursor vs Paging 결정 트리, Tasklet이 어울리는 자리.
5. **Spring Batch 6의 변경점 — 무엇이, 왜 달라졌는가** — `ChunkOrientedStepBuilder`, JobOperator 통합, recover API, graceful shutdown, JobParameter record화, v5 직렬화 비호환.
6. **실전 유스케이스 — 카카오페이 정산 사례 해부** — I/O 묶기 → Dirty Checking 제거 → IN UPDATE 그룹화 → chunk size 정렬, 단계별 기여도와 약 10배 향상.
7. **Fault Tolerance와 테스트 — Skip/Retry/Restart와 멱등성** — idempotency 3 조건, outbox·멱등 키·dedupe 비교, `spring-batch-test`로 잡을 어떻게 테스트할 것인가.
8. **성능과 확장 — 파티셔닝, 멀티스레드, Remote Step** — chunk size 튜닝, 멀티스레드 step, 파티셔닝, Remote Step 결정 트리.
9. **모니터링과 옵저버빌리티 — Micrometer, JFR, 알람 설계** — Prometheus 메트릭, JFR로 잡 내부를 보는 법, PromQL 알람 임계값 설계.
10. **K8s 운영 — CronJob, Graceful Shutdown, JobRepository 정리** — CronJob 패턴, recover API의 K8s 결합, JobRepository 정리 잡을 Spring Batch로 짜기.
11. **5에서 6으로 마이그레이션 — 직렬화 함정과 실전 시나리오** — 패키지 이동, JobLauncher → JobOperator, 직렬화 비호환 대응, 잡 한 개의 코드 diff.
12. **운영 1년차 회고 — 5번째 잡을 만들 때 보이는 것** — 시간 축으로 본 안티패턴, Airflow·Quartz·SCT와의 4축 결정 표, 다음 학습 로드맵.

**부록 A. 유스케이스 패턴 카탈로그** — 대용량 일괄 처리, ETL/마이그레이션, 통계·집계, 파일 ETL을 결정 트리 카드와 핵심 코드 스니펫으로 묶은 빠른 참조.

## 저자 소개

Toby-AI는 한국어 기술서 저술을 위해 설계된 AI 저자 페르소나다. Toby-AI Book Writing Harness v1.2.0의 다단 파이프라인 — 리서치 조율, 저술 계획, 계획 리뷰, 토비 문체 챕터 저술, 스타일 가디언, 통합 편집, 표지 디자인, EPUB 빌드 — 을 거쳐 한 권의 책을 산출한다. 이 책은 Spring Batch 공식 레퍼런스, Spring Batch 6 What's New, 카카오페이·우아한형제들 같은 한국 production 사례, OKKY·velog·GitHub Discussion 등 한국 커뮤니티의 실제 질문을 1차 자료로 삼아 저술됐다.

## 책 정보

- 파일: `직접-짜본-사람을-위한-Spring-Batch-6-v1.0.0.epub`
- 형식: EPUB 3 (ko)
- 라이선스: CC BY-NC-SA 4.0 (저작자표시·비상업적이용·동일조건변경허락 4.0 국제)
- 식별자: `urn:uuid:spring-batch-6-toby-ai-v1.0.0`
- 빌드: Toby-AI Book Writing Harness v1.2.0
