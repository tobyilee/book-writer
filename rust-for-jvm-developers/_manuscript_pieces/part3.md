# Part 3. 실무 시스템을 만든다

> *"이제 Spring으로 짜던 그 서비스가 Rust로 보인다."*

Part 3은 *손이 코드를 만지는 자리*다. 9장 동시성 기초에서 5장 borrow의 두 줄 규칙이 *멀티스레드 안전성*으로 보상받는 순간을 맛보고, `Arc<Mutex<T>>`가 *공유 가변 상태의 표준 표현형*이라는 사실을 손가락으로 확인한다. 10장에서 async/await와 tokio로 Kotlin Coroutine 다음의 모델을 손에 쥐고, *세 가지 함정*(JoinHandle 누락 / await를 가로지르는 동기 Mutex guard / async 안 blocking 호출)을 미리 박아둔다. 11장 axum에서 *Spring Controller가 Rust로 보이는 순간*이 오고, 7장에서 만든 `AuthError` enum이 `IntoResponse`로 자연스럽게 HTTP 응답에 매핑되는 모양을 본다. 12장에서 sqlx의 *컴파일 타임 검증된 SQL*과 sea-orm의 친숙한 ORM 사이에서 *자기 출신에 맞는 길*을 고르고, 11장의 in-memory 서비스를 PostgreSQL 위로 옮긴다. Part 3이 끝나면 자네는 *Spring으로 짜던 그 서비스 한 채를 Rust로 짤 수 있다*는 자신감에 도달해 있다.

**포함 챕터**

- 9장. 동시성 기초 — 스레드, channel, Mutex, 그리고 `Send`/`Sync`
- 10장. async와 tokio — Spring WebFlux/Kotlin Coroutine 다음의 모델
- 11장. axum으로 첫 HTTP 서비스 — Spring Controller가 Rust로 보이는 순간
- 12장. 데이터베이스 — sqlx로 컴파일 타임 검증된 SQL을, sea-orm으로 친숙한 ORM을
