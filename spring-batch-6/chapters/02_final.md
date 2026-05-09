# 2장. Spring Batch가 약속하는 것 — 청크, 트랜잭션, 메타데이터

Spring Batch 공식 문서를 처음 열어본 사람이라면 비슷한 경험이 있을 것이다. 첫 페이지를 펴자마자 `Job`, `Step`, `JobInstance`, `JobExecution`, `StepExecution`, `ExecutionContext`, `JobLauncher`, `JobRepository`, `JobOperator`, `ItemReader`, `ItemProcessor`, `ItemWriter`… 이름이 12개쯤 한 번에 쏟아진다. 각 이름의 정의를 한 단락씩 읽고 나면 머리가 멍해진다. 분명 단어 하나하나는 알아들었는데, 이게 다 합쳐서 무슨 그림인지가 안 그려진다.

그렇게 한 시간쯤 헤매다 보면 의문이 든다. 정말 이렇게 많은 개념이 다 필요한가? 혹시 이 12개의 이름이 사실 한두 가지 핵심 질문을 풀기 위한 도구들이 아닌가?

답부터 말하자. 그렇다. Spring Batch의 모든 개념은 사실상 **하나의 질문**에 답한다. **"어디까지 처리됐는지를 어떻게 영구히 기억하느냐."** 이 질문에서 출발해서 12개의 이름을 다시 보면, 각각이 이 질문을 풀기 위한 자리일 뿐이라는 게 보인다. 한번 차근차근 따라가 보자.

## 한 줄 정의 — Spring Batch는 무엇을 해주는가

이 책의 대상 독자는 직접 배치 코드를 짜본 사람이다. 그러니 Spring Batch의 정의도 그 시각으로 다시 쓰자. 공식 문서가 말하는 정의가 아니라, 직접 짜본 사람이 듣고 싶은 정의를.

**Spring Batch는 재실행 안전성과 메타데이터 관리, 그리고 청크 트랜잭션 경계를 직접 짜지 않게 해주는 프레임워크다.**

이 한 줄을 풀면 1장에서 짚은 다섯 가지 문제가 자리를 잡는다.

- **재시작:** Spring Batch가 영구 메타데이터에 진행 위치를 기록해 둔다. 잡이 죽었다가 다시 시작되면 마지막 커밋된 청크 다음부터 자동으로 이어 간다.
- **부분 실패:** Skip / Retry / Restart라는 세 가지 표준 정책으로 나누어진다. 어느 예외를 어떻게 다룰지를 코드 곳곳의 try-catch가 아니라 정책 한 곳에서 결정한다.
- **메타데이터:** 모든 잡 실행 이력이 `JobRepository`라는 표준 저장소에 자동으로 기록된다. 잡마다 다른 `job_log` 테이블을 만들지 않는다.
- **트랜잭션 경계:** 청크 단위 트랜잭션이 프레임워크 차원에서 정의된다. 우리는 청크 사이즈만 결정하면 된다.
- **모니터링:** Micrometer 메트릭이 자동으로 노출된다. 잡 단위·스텝 단위 처리량과 시간이 표준 prefix로 publish된다.

이 다섯 가지가 직접 짜본 사람이 결국 다시 만들게 되던 인프라다. Spring Batch는 그 인프라를 표준 자리에 미리 만들어 둔 도구라고 보면 된다. 우리가 할 일은 자기 도메인 로직(읽고, 변환하고, 쓰는)만 표준 자리에 끼워 넣는 일이 된다.

이제 그 표준 자리들이 어떻게 생겼는지 살펴보자.

## 3-layer 아키텍처 — 왜 이렇게 분리했는가

Spring Batch 공식 레퍼런스는 프레임워크를 세 레이어로 나누어 설명한다.

```
┌────────────────────────────────────────────────┐
│  Application Layer                             │
│  (개발자가 작성하는 Job/Step 정의 + 비즈니스)   │
└────────────────────────────────────────────────┘
                     │ 사용
                     ▼
┌────────────────────────────────────────────────┐
│  Batch Core                                    │
│  (Job, Step, JobLauncher/JobOperator 등)       │
└────────────────────────────────────────────────┘
                     │ 사용
                     ▼
┌────────────────────────────────────────────────┐
│  Batch Infrastructure                          │
│  (Reader/Writer 구현체, Repository, Retry 등)   │
└────────────────────────────────────────────────┘
```

처음 보면 그냥 흔한 3-layer 분리처럼 보인다. 그런데 이 분리에는 분명한 의도가 있다. 한번 생각해보자. Application은 우리가 짠다. 그러면 Batch Core와 Batch Infrastructure는 누가 짜는가? Spring Batch 팀이 짠다. 즉 **우리가 짜는 코드와 프레임워크가 짜는 코드가 명확한 경계로 나뉘어 있다.**

이게 왜 중요할까? 직접 배치를 짜본 경험을 떠올려보자. 우리는 도메인 로직을 짜다가 어느 순간 트랜잭션 매니저를 직접 다루고, 트랜잭션 매니저를 다루다가 어느 순간 재시작 위치 저장 코드를 짜고, 재시작 코드를 짜다가 어느 순간 메트릭 publish 코드를 짜고 있다. 도메인과 인프라가 같은 클래스 안에 뒤섞이는 것이다. 그러다 인프라가 바뀌면 도메인 코드까지 같이 흔들린다. 끔찍한 일이다.

3-layer 분리는 이 뒤섞임을 막는 약속이다. **내 도메인 로직(Application)은 프레임워크 변경(Core)에 끌려가지 않는다.** Spring Batch 6에서 `JobLauncher`가 `JobOperator`로 통합됐어도, 우리가 짠 ItemReader/ItemWriter 자체는 거의 그대로 동작한다. 인프라의 변경이 도메인 코드를 쓸데없이 휘젓지 않는다는 보장 — 그게 3-layer가 약속하는 것이다.

이 그림을 머릿속에 두고 가자. 우리가 이 책에서 다루는 코드 대부분은 **Application Layer**에 속한다. Batch Core와 Infrastructure는 우리가 직접 만지지 않는다. 가끔 동작 원리를 이해하기 위해 들여다볼 뿐이다.

## Job, Step, 그리고 모델의 그림

이제 모델을 그려보자. Spring Batch에서 일의 단위는 두 단계로 나뉜다.

```
┌───────────────────── Job ─────────────────────┐
│                                               │
│  ┌── Step 1 ──┐  ┌── Step 2 ──┐  ┌── Step 3 ──┐│
│  │ Reader     │  │ Reader     │  │ Tasklet    ││
│  │ Processor  │  │ Processor  │  │            ││
│  │ Writer     │  │ Writer     │  │            ││
│  └────────────┘  └────────────┘  └────────────┘│
│                                               │
└───────────────────────────────────────────────┘
```

- **Job:** 하나의 비즈니스 단위 작업. 예를 들어 "결제 정산 잡", "월말 통계 잡". 추상적인 청사진이다.
- **Step:** Job을 구성하는 단계. 한 Job은 여러 Step으로 나뉠 수 있다. 예를 들어 정산 잡은 "원장 데이터 적재" Step → "정산 계산" Step → "송금 데이터 생성" Step으로 흐를 수 있다.
- **Step 안의 모델:** 두 가지 중 하나. 대부분의 Step은 **chunk-oriented** 모델을 쓴다 — Reader가 한 건씩 읽고, Processor가 변환하고, 청크가 차면 Writer가 쓴다. 청크 모델이 어색한 일은 **tasklet** 모델로 짠다 — 한 덩어리의 단발성 작업.

여기서 한 가지를 분명히 해두자. **chunk-oriented가 9할이고 tasklet은 1할이다.** Spring Batch의 본류는 청크다. 파일 압축, 디렉터리 정리, 외부 셸 명령 같은 일에서만 tasklet을 꺼낸다. 정확히 어떤 자리에서 tasklet을 쓰는지는 4장에서 다시 다룬다. 일단 지금은 "청크가 본류, tasklet은 보조"라는 비중만 머릿속에 박아두자.

## 같은 잡을 두 번 돌릴 수 있는가 — JobInstance와 JobExecution

여기서 중요한 구분이 등장한다. 그리고 이 구분이 Spring Batch 입문자가 가장 자주 헷갈리는 지점이다.

같은 Job 정의를 가지고 있어도, 실행할 때마다 그게 다른 비즈니스 의미를 가질 수 있다. "결제 정산 잡"이라는 한 가지 청사진이 있어도, **2026년 5월 7일 정산**과 **2026년 5월 8일 정산**은 다른 일이다. 두 실행이 같은 일이라고 보면 5월 8일 잡을 돌릴 때 "이미 5월 7일에 같은 잡이 끝났는데 또 돌리려 하네"라며 거부될 수도 있고, 두 실행이 다른 일이라고 보면 그게 자연스럽게 이어진다.

Spring Batch는 이 구분을 명시적으로 한다.

- **JobInstance:** 같은 Job이지만 비즈니스 의미가 다른 실행 단위. **JobParameters**로 식별된다.
- **JobExecution:** JobInstance를 실제로 돌린 한 번의 시도. 같은 인스턴스가 실패해서 다시 돌면 JobExecution이 늘어난다.

그림으로 그리면 이렇다.

```
Job: "결제 정산 잡"
│
├── JobInstance #1 (date=2026-05-07)
│   │
│   ├── JobExecution #101  (시도 1, FAILED)
│   ├── JobExecution #102  (시도 2, FAILED — 컨테이너 OOM)
│   └── JobExecution #103  (시도 3, COMPLETED)
│
├── JobInstance #2 (date=2026-05-08)
│   │
│   └── JobExecution #104  (시도 1, COMPLETED)
│
└── JobInstance #3 (date=2026-05-09)
    │
    └── JobExecution #105  (시도 1, STARTED)
```

이 1:N 관계가 **재시작이 가능한 이유**다. JobInstance가 동일하면 Spring Batch는 이전 JobExecution들의 상태를 가져와서, 마지막으로 커밋된 청크 다음부터 다시 돈다. 즉 5월 7일 잡이 두 번 실패하고 세 번째에 성공한 위 그림에서, 두 번째 시도는 첫 번째 시도가 멈춘 자리에서 이어지고, 세 번째 시도는 두 번째 시도가 멈춘 자리에서 이어진다. 매번 처음부터 다시 도는 것이 아니다.

반면 같은 Job이라도 JobParameters가 다르면 별개의 JobInstance가 된다. 그래서 5월 8일 잡과 5월 9일 잡은 서로 영향을 주지 않는다.

여기서 한국 입문자가 자주 빠지는 함정 하나를 미리 짚자. **JobParameters를 잘못 설계하면 잡이 두 번째 실행부터 거부당한다.** "이미 동일한 인스턴스가 끝났다"는 메시지를 받게 된다. 5월 7일에 한 번 돌렸는데 5월 8일에 같은 파라미터로 돌리려고 하면 거부된다는 뜻이다. 매일 도는 잡이라면 일자(date)를 JobParameter에 넣어 인스턴스를 매일 새로 만들어야 한다. 이걸 모르면 "잡이 한 번만 도는 이상한 현상"으로 시간을 한참 쓰게 된다. 3장에서 첫 잡을 만들 때 직접 이 함정을 체험해볼 것이다.

## JobRepository — 모든 이력의 영구 기억

이제 의문이 하나 생긴다. JobInstance와 JobExecution이 매번 어디에 저장되는가? 이게 메모리에만 있다면 잡이 죽는 순간 같이 사라져서 재시작이 불가능해진다. 그래서 Spring Batch는 **JobRepository**라는 영구 저장소를 둔다.

JobRepository는 추상 인터페이스고, 기본 구현은 RDB(JDBC)다. Spring Batch 6부터는 MongoDB도 1급 시민으로 지원한다. 어떤 저장소를 쓰든 동일한 정보가 영구히 기록된다.

기록되는 핵심 테이블은 다음과 같다 (JDBC 기준).

| 테이블 | 무엇을 기록하는가 |
|---|---|
| `BATCH_JOB_INSTANCE` | JobInstance — 어떤 Job이 어떤 파라미터로 돌았는가 |
| `BATCH_JOB_EXECUTION` | JobExecution — 그 인스턴스의 N번째 시도, 시작·종료 시각, 상태 |
| `BATCH_JOB_EXECUTION_PARAMS` | 그 시도에 쓰인 JobParameters |
| `BATCH_JOB_EXECUTION_CONTEXT` | Job 단위 ExecutionContext (key-value 상태) |
| `BATCH_STEP_EXECUTION` | StepExecution — 각 스텝의 시도, commit 수, rollback 수, skip 수 |
| `BATCH_STEP_EXECUTION_CONTEXT` | Step 단위 ExecutionContext |

이 테이블들이 우리가 1장에서 직접 짜다 진력이 났던 그 `job_log`/`step_log` 인프라의 표준 버전이다. 잡마다 다른 컬럼을 가진 들쭉날쭉한 로그 테이블이 아니다. 모든 잡이 같은 스키마에 같은 의미의 정보를 기록한다.

특히 ExecutionContext는 흥미롭다. 이게 재시작의 핵심이다. 예를 들어 `JdbcPagingItemReader`는 마지막으로 읽은 페이지 번호를 ExecutionContext에 저장한다. 잡이 죽었다 다시 시작하면, 같은 JobInstance의 ExecutionContext에서 그 페이지 번호를 읽어와 거기서부터 다시 읽는다. 우리가 1장에서 "처리된 ID를 별도 테이블에 INSERT하고 다음 실행 때 NOT IN으로 제외한다"고 짜던 그 인프라가, 여기서는 ExecutionContext 한 줄로 끝난다.

이 부분에서 처음으로 "직접 짤 때 vs Spring Batch"의 매핑이 명확해진다. 내가 짜던 `processed_ids` 테이블은 Spring Batch의 ExecutionContext가 대신 한다. 내가 짜던 `job_log` 테이블은 BATCH_JOB_EXECUTION이 대신 한다. 내가 짜던 잡 두 번 도는 거 막는 코드는 JobInstance 동일성 검사가 대신 한다. 이런 매핑이 앞으로 책 전체를 통해 이어질 것이다.

## chunk-oriented 모델의 핵심 — 청크 = 트랜잭션

이제 청크 모델로 들어가자. 이게 Spring Batch의 본류이고, 4장에서 깊게 다룰 주제다. 여기서는 한 가지 핵심 규칙만 머릿속에 박아 두자.

**청크 = 트랜잭션이다.**

이 한 줄이 모든 것의 출발점이다. 풀어 쓰면 이렇다.

- Reader가 한 건씩 읽는다. `read()`가 `null`을 반환할 때까지.
- Processor가 한 건씩 변환한다. 이 변환된 결과들이 청크 안에 누적된다.
- 청크 사이즈만큼 누적되면 Writer가 그 청크를 한 번에 쓴다.
- 그리고 트랜잭션이 커밋된다.
- 다음 청크로 넘어간다.

이 흐름을 그림으로 그리면 이렇다.

```
┌──── Step의 한 청크 (size=3) ─────────┐
│                                     │
│  TX BEGIN                           │
│    read() → item1                   │
│    process(item1) → result1         │
│    read() → item2                   │
│    process(item2) → result2         │
│    read() → item3                   │
│    process(item3) → result3         │
│    write([result1, result2, result3])│
│  TX COMMIT                          │
│                                     │
└─────────────────────────────────────┘
        (다음 청크가 같은 방식으로 반복)
```

청크 안의 한 건이 실패하면 어떻게 되는가? **청크 전체가 롤백된다.** 트랜잭션이 청크 단위이기 때문이다. 그래서 우리의 Writer는 하나의 청크를 두 번 받아도 동일한 결과가 나오도록 설계되어야 한다(멱등). 그렇지 않으면 retry나 restart가 위험해진다.

여기서 한국 커뮤니티에서 자주 등장하는 혼동 하나를 미리 짚어두자. **chunk size, page size, fetch size는 다 다른 개념이다.** 이름이 비슷해서 같은 것으로 오해하기 쉽다.

- **chunk size:** 트랜잭션 1건당 처리할 항목 수.
- **page size:** Paging Reader가 한 페이지에 가져올 행 수.
- **fetch size:** JDBC 드라이버가 네트워크 라운드트립 1회당 가져올 행 수.

이 셋의 관계와 권장값은 4장에서 본격적으로 다룬다. 일단 지금은 "셋이 다르다"는 것만 기억해두자.

## tasklet의 자리 — 9 대 1 비중에서 1할의 의미

청크 모델이 본류라고 했지만, 모든 일이 청크 모델에 맞는 것은 아니다. 한번 상상해보자. "S3에 올라온 압축 파일을 다운받아서 풀고, 어제 날짜 폴더를 정리하고, 새 파일을 적재 디렉터리로 옮긴다"는 일이 있다고 해보자. 이게 청크 모델로 어울릴까?

어색하다. 이건 한 덩어리의 일이지 항목 단위 반복이 아니다. 압축 파일 한 개를 "읽어서, 변환해서, 쓴다"는 청크 모델로 풀려고 하면 작위적인 모양이 나온다. 그래서 Spring Batch는 이런 일을 위해 tasklet 모델을 따로 둔다.

**tasklet은 한 덩어리의 단발성 작업을 위한 자리다.** 청크 모델로 풀면 어색해지는 일들. 파일 압축·해제, 디렉터리 정리, 외부 셸 명령 실행, FTP 다운로드, 단발성 알림 발송 같은 것. tasklet의 구체적인 사용법과 결정 기준은 4장의 마지막에서 자세히 다룬다.

여기서 강조하고 싶은 건 비중이다. **본류는 chunk-oriented다.** 한 시스템 안의 잡 10개를 보면 9개는 청크 모델이고 1개가 tasklet 모델이라고 생각하면 대략 맞는다. tasklet이 일찍부터 등장하면 "이게 그래도 청크보다 단순해 보이니 다 이걸로 짜자"는 유혹이 생기는데, 그건 좋지 않다. 청크 모델의 트랜잭션·재시작·메트릭 인프라를 포기하는 셈이기 때문이다.

## ExecutionContext — 재시작이 정말로 자동인 이유

방금 표에 등장한 ExecutionContext가 어떤 자리인지 한 절로 풀어두자. 1장에서 우리가 가장 골치 아파했던 게 "어디까지 처리됐는지" 추적하는 인프라였다. 처리된 ID를 별도 테이블에 INSERT하고, 다음 실행에 NOT IN으로 제외하는 그 코드 말이다. 그게 ExecutionContext에 어떻게 옮겨졌는지를 보면, Spring Batch의 약속이 무엇인지가 가장 분명하게 드러난다.

ExecutionContext는 한 줄로 말하면 **"잡(혹은 스텝)이 자기 진행 상태를 영구히 보관할 수 있는 key-value 저장소"**다. JobExecution에 붙어 있는 것 하나, StepExecution에 붙어 있는 것 하나, 두 종류가 있다.

```
JobExecution (id=103)
├── ExecutionContext { "globalProgress": "phase2-completed" }
│
├── StepExecution (id=201, step=loadStep)
│   └── ExecutionContext { "JdbcPagingItemReader.read.count": 23000,
│                          "JdbcPagingItemReader.page": 46 }
│
└── StepExecution (id=202, step=processStep)
    └── ExecutionContext { ... }
```

이 key-value가 청크 트랜잭션이 커밋될 때마다 함께 BATCH_*_EXECUTION_CONTEXT 테이블에 영구 저장된다. 청크 트랜잭션이 롤백되면 ExecutionContext의 변경도 함께 롤백된다. 즉 **데이터 처리와 진행 상태가 한 트랜잭션 안에 묶여 있다.** 이게 결정적이다. 한 트랜잭션 안에 묶여 있어야 "데이터는 처리됐는데 진행 상태는 기록 안 됨" 또는 "진행 상태는 기록됐는데 데이터는 롤백됨" 같은 모순 상태가 생기지 않는다.

내장 Reader들은 자기 진행 위치를 ExecutionContext에 자동으로 넣어둔다. `JdbcPagingItemReader`는 마지막으로 읽은 페이지 번호를, `FlatFileItemReader`는 마지막으로 읽은 라인 번호를 저장한다. 잡이 죽었다 같은 JobInstance로 다시 시작하면, Spring Batch가 ExecutionContext에서 그 값을 읽어와 Reader에게 "여기서부터"라고 신호를 준다. 우리가 직접 짤 때 별도 테이블 만들어 INSERT/SELECT 하던 인프라가, 여기서는 보이지 않는 자리에 기본 동작으로 들어와 있는 것이다.

직접 무언가를 ExecutionContext에 넣을 수도 있다. 예를 들어 "1단계에서 계산한 정산 총액을 2단계가 검증에 쓴다"면, 1단계 Step의 listener에서 그 값을 ExecutionContext에 저장하고, 2단계 Step에서 꺼내 쓴다. 이게 잡 흐름의 상태 공유 표준 자리다.

여기까지가 "재시작이 가능한 이유"의 진짜 모습이다. JobInstance 동일성 + ExecutionContext 자동 저장·복원 = 재시작 친화. 이 구조가 잘 작동하려면 한 가지 전제가 있다 — **Writer는 같은 청크를 두 번 받아도 결과가 같아야 한다(멱등).** 4장과 7장에서 이 전제가 무엇을 요구하는지를 더 자세히 다룬다. 일단 지금은 "ExecutionContext가 진행 위치를 자동으로 영구 저장한다"는 한 줄을 머릿속에 박아두자.

## 직접 짠 코드와의 매핑 — 내가 짜던 그 부분이 여기로 옮겨진다

이제 잠시 멈추고, 1장에서 직접 짜던 코드와 Spring Batch의 모델을 매핑해보자. 같은 일이 어디로 옮겨지는지를 명시적으로 적어두면, 12개의 이름이 더 친숙해진다.

| 직접 짤 때 | Spring Batch에서는 |
|---|---|
| 처리된 ID를 `processed_ids` 테이블에 INSERT | ExecutionContext에 진행 위치 저장 (Reader가 자동) |
| 잡 시작 시 `processed_ids`를 NOT IN으로 제외 | 같은 JobInstance의 ExecutionContext에서 자동 복원 |
| `job_log` 테이블에 시작·종료 시각 기록 | BATCH_JOB_EXECUTION에 자동 기록 |
| `step_log` 테이블에 단계별 처리 건수 기록 | BATCH_STEP_EXECUTION에 자동 기록 |
| 같은 잡 두 번 막는 별도 락 테이블 | JobInstance 동일성 검사 (JobParameters 기반) |
| 청크 단위 try-commit-catch-rollback 직접 작성 | chunk-oriented Step이 트랜잭션을 자동 관리 |
| 처리 건수·실패 건수 메트릭 publish 코드 | Micrometer 메트릭 자동 publish |

이 매핑은 이 책 전체를 통해 박스 코너로 다시 등장한다. 4장에서 Reader/Writer를 다룰 때, 5장에서 6의 변경점을 다룰 때, 7장에서 fault tolerance를 다룰 때, 매번 "내가 짜던 그 부분이 여기로 옮겨진다"는 시각으로 짚어볼 것이다.

이 시각이 중요한 이유는 단순하다. Spring Batch를 처음 보는 사람은 "이걸 다 새로 배워야 하나?"라는 부담을 느낀다. 그런데 사실 우리는 이미 이 인프라를 자기 식으로 짜본 적이 있다. 그러니까 새로 배우는 게 아니라, **우리가 이미 알고 있는 그 인프라가 표준 자리에 어떻게 들어가 있는지를 확인하는 일**이다. 이 시각으로 보면 학습 부담이 훨씬 가벼워진다.

## JobLauncher와 JobOperator — 그리고 Spring Batch 6의 통합

마지막으로 잡을 실제로 시작하는 자리에 대해 짚자. 누군가가 "이 잡을 시작해라" 하고 트리거를 걸어줘야 잡이 돈다. 그 트리거 자리가 `JobLauncher`다.

전통적으로 Spring Batch는 두 개의 인터페이스를 분리해 두었다.

- `JobLauncher`: 잡을 시작한다.
- `JobExplorer`: 잡 실행 이력을 조회한다.
- `JobOperator`: stop/restart 같은 운영 제어를 한다.

5.x까지는 이 셋을 따로 빈으로 등록해야 했다. 그런데 자세히 보면 셋은 결국 같은 `JobRepository` 위에서 동작한다. 그래서 굳이 분리할 이유가 약해진 것이다.

Spring Batch 6은 이걸 정리한다. **`JobOperator`가 `JobLauncher`와 `JobExplorer`의 역할을 흡수한다.** 6.x부터는 `JobOperator` 하나만 주입받으면 launch/explore/control을 다 할 수 있다. 한 가지 인터페이스가 한 가지 책임을 하는 게 아니라 한 가지 인터페이스가 잡 운영의 모든 진입점이 되는 셈이다.

마이그레이션 입장에서는 이게 깔끔한 변화다. 5.x 코드의 `JobLauncher` 주입을 `JobOperator`로 바꾸면 되고, 그 외의 동작은 거의 그대로다. 5에서 6으로의 마이그레이션 전체 그림은 11장에서 코드 diff로 자세히 풀어볼 것이다. 여기서는 "Spring Batch 6에서는 JobOperator 하나면 된다"는 것만 기억하자.

그리고 6에서 추가된 `JobOperator#recover()`라는 메서드가 있다. 이게 K8s 운영자에게 매우 큰 의미를 가진다. 컨테이너가 SIGKILL로 갑자기 죽으면 JobExecution이 STARTED 상태로 박제된다. 다시 돌리려고 하면 "이미 실행 중인 인스턴스가 있다"고 거부당한다. 5.x까지는 이 박제 상태를 풀려면 BATCH_JOB_EXECUTION 테이블을 직접 UPDATE해야 했다. 새벽에 사람이 DB를 손보는 끔찍한 일이다. 6에서는 `jobOperator.recover(executionId)` 한 줄이면 된다. 이 한 줄이 K8s 운영의 풍경을 바꾼다. 자세한 운영 시나리오는 7장과 10장에서 다루겠다.

## 12개의 이름을 다시 보기

이제 이 장의 도입부에서 마주쳤던 12개의 이름을 다시 정리해보자. 한 줄씩만 적으면 이렇다.

- **Job:** 비즈니스 단위 작업의 추상 정의.
- **Step:** Job을 구성하는 단계. chunk-oriented 또는 tasklet.
- **JobInstance:** 같은 Job의 비즈니스 의미가 다른 실행 단위. JobParameters로 식별.
- **JobExecution:** JobInstance의 N번째 시도.
- **StepExecution:** Step의 N번째 시도.
- **ExecutionContext:** Job/Step 단위 key-value 상태. 재시작의 핵심.
- **JobRepository:** 모든 이력의 영구 저장소.
- **JobLauncher:** 잡 시작 진입점 (6에서 JobOperator로 통합).
- **JobOperator:** 잡 운영 진입점. launch/explore/control을 다 함.
- **ItemReader:** 청크의 한 건씩을 읽는 자리. `read()` 반환 `null`이 입력 종료.
- **ItemProcessor:** 한 건씩 변환하는 자리. `null` 반환은 필터링.
- **ItemWriter:** 청크 단위로 쓰는 자리. 트랜잭션 1건당 한 번 호출.

12개라고 하면 많아 보이지만, 묶으면 네 그룹이다.

- **정의:** Job, Step (청사진)
- **실행 단위:** JobInstance, JobExecution, StepExecution (그 청사진의 실제 실행)
- **저장:** JobRepository, ExecutionContext (이력의 영구 기억)
- **운영 진입점:** JobOperator (시작·조회·제어)
- **청크 모델:** ItemReader, ItemProcessor, ItemWriter (Step 안의 작업 흐름)

네 그룹이 각자 자기 책임을 가진다. 이 그림이 머릿속에 들어오면, 공식 문서를 다시 펴도 더 이상 헤매지 않는다.

## 마무리

Spring Batch의 모든 개념은 결국 한 질문에 답한다 — **어디까지 처리됐는지를 어떻게 영구히 기억하느냐.** 그 답이 JobInstance·JobExecution이라는 1:N 관계, JobRepository라는 영구 저장소, ExecutionContext라는 상태 보관함, 청크 = 트랜잭션이라는 핵심 규칙으로 분해되어 있는 것이다.

3-layer 아키텍처는 우리 도메인 코드와 프레임워크 인프라를 깔끔히 분리해 둔다. chunk-oriented가 9할의 본류고 tasklet이 1할의 보조다. 그리고 Spring Batch 6은 JobOperator로 통합해 운영 진입점을 단순화했다.

머리로 모델을 그려봤다면, 손으로 만질 차례다. Spring Boot 4 + Spring Batch 6으로 첫 잡을 만들어보고, 메타데이터 테이블에 자기 흔적을 직접 들여다보고, 한국 입문자 1번 함정인 `@StepScope`를 정면으로 통과해보자.
