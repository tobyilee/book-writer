# 코드로 짓는 CPU — 동반 예제 코드

이 프로젝트는 *코드로 짓는 CPU: Kotlin으로 SAP-1에서 8비트 RISC까지* (Toby-AI 저, CC BY-NC-SA 4.0)의
모든 Kotlin 예제를 담은 Gradle Kotlin DSL 멀티모듈 프로젝트입니다.

---

## 시작하기

### 요구사항

| 도구 | 버전 |
|------|------|
| JDK | 17+ (toolchain 자동 다운로드) |
| Kotlin | 2.0.20 (Gradle이 관리) |
| Gradle wrapper | 8.7 (별도 설치 불필요) |

### 빌드 & 테스트

```bash
# 전체 빌드 + 테스트
./gradlew build

# 특정 챕터만
./gradlew :chapter-06:build

# 테스트만
./gradlew test

# 특정 챕터 실행 (application 플러그인이 적용된 챕터)
./gradlew :chapter-06:run
```

---

## 챕터 매트릭스

| # | 제목 | 핵심 클래스 | 실행 커맨드 |
|---|------|-------------|-------------|
| 01 | 컴퓨터는 왜 이런 모습인가 | (개념 챕터, 코드 없음) | — |
| 02 | fetch-decode-execute를 Kotlin 30줄로 | `MiniCpu` | `./gradlew :chapter-02:run` |
| 03 | SAP-1의 청사진과 첫 모듈 | `Clock`, `ProgramCounter`, `Instruction` | `./gradlew :chapter-03:test` |
| 04 | 레지스터와 8비트 산술 | `Register`, `Alu` | `./gradlew :chapter-04:test` |
| 05 | overflow라는 무덤 | `AluFlags` | `./gradlew :chapter-05:test` |
| 06 | 메모리·버스·컨트롤러 — SAP-1이 처음 돌아가는 순간 | `Ram`, `Bus`, `Controller`, `Sap1` | `./gradlew :chapter-06:run` |
| 07 | 어셈블러와 디스어셈블러 | `Lexer`, `Assembler`, `Disassembler` | `./gradlew :chapter-07:run` |
| 08 | 16바이트의 한계 — SAP-2는 왜 다시 설계되었는가 | `Sap2Core`, `RegisterFile` | `./gradlew :chapter-08:test` |
| 09 | 조건 분기·서브루틴·I/O | `Jump`, `Stack`, `IoPort`, `HelloDemo` | `./gradlew :chapter-09:run` |
| 10 | 마이크로코드와 디버거 | `MicroRom`, `Debugger`, `DebuggerCli` | `./gradlew :chapter-10:run` |
| 11 | 같은 Fibonacci, 네 가지 어셈블리 | (어셈블리 비교, `comparison/` 참조) | — |
| 12 | RISC의 약속 — 1980년대의 격렬한 논쟁 | (개념 챕터, 코드 없음) | — |
| 13 | 우리의 8비트 RISC를 설계하다 | `Isa`, `Assembler`, `Cpu`, `Risc8Demo` | `./gradlew :chapter-13:run` |
| 14 | instruction-accurate에서 cycle-accurate로 | `CycleAccurate`, `CycleDemo`, `CpuBenchmark` | `./gradlew :chapter-14:run` |
| 15 | 여기서 어디로 — 컴퓨터 전체로 가는 다리 | (마무리 챕터, 코드 없음) | — |

---

## 누적 스냅샷 정책

각 챕터 폴더(`chapter-NN/`)는 해당 챕터까지의 **모든 코드를 누적한 완전 동작 스냅샷**입니다.
챕터 6 폴더에는 1~6장의 모든 구현체가 들어 있어 그 폴더 하나만으로도 SAP-1을 완전히 실행할 수 있습니다.
패키지 네임스페이스(`sap.chXX`, `risc8.chXX`)가 챕터별로 격리되므로 빌드 충돌 없이
각 챕터를 독립적으로 실행하고 테스트할 수 있습니다.

---

## 라이선스

이 예제 코드는 책 본문과 동일하게 **CC BY-NC-SA 4.0** 라이선스를 따릅니다.
자세한 내용은 <https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko>를 참조하세요.
