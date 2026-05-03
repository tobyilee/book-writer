# Part 4. 출시와 그 다음

> *"Rust는 JVM의 대체가 아니라 무기 추가다."*

Part 4는 *기술서를 사람의 책으로 닫는* 자리다. 13장에서 cargo가 JUnit/Mockito/JMH/SpotBugs/Sonar/picocli/OWASP를 *언어 코어 안에서* 어떻게 안고 있는지를 정리하고, 길어진 컴파일 시간 처방, `cargo audit`/`deny`/`vet` 보안 게이트, *내 첫 매크로 만들기*까지 손에 묻힌다. 14장에서 musl + distroless로 *8MB 컨테이너*를 빌드하고, `tracing` + `tracing-opentelemetry`로 *Spring Cloud Sleuth가 하던 일*을 옮긴다. 15장에서 JVM을 *떠나지 않고* Rust를 들이는 다리(JNI / Project Panama / C ABI / 사이드카 패턴)를 깐다 — 8장의 unsafe 절이 본격적으로 회수되는 자리다. 마지막 16장은 *사람과 조직과 커리어*의 자리다. 두 사례("AWS 비용 81% 절감" vs "I Rewrote A Java Microservice In Rust And Lost My Job")의 솔직한 대조, Dropbox Magic Pocket의 그늘, 4~6개월 학습 곡선, 조직 도입의 정치 5가지 권고, 한국 커뮤니티 매듭. 그리고 책의 마지막 한 줄. *"Rust는 JVM의 대체가 아니라 무기 추가다. Spring 다음의 시스템을 손에 쥐자."*

**포함 챕터**

- 13장. 테스트·품질·도구 인프라·CLI — cargo가 IDE·Sonar·JMH·picocli·OWASP를 모두 안고 있다
- 14장. 출시 — 8MB 컨테이너와 OpenTelemetry 관측
- 15장. JVM과 함께 — FFI·JNI·Project Panama·폴리글랏 아키텍처
- 16장. Rust로 가는 길 — 사람·조직·커리어, 그리고 매듭
