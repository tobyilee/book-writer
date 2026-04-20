# Harness Engineering 학습 플랜

> **기반 커리큘럼:** Ralph Loop / Karpathy Loop / 미니 랄프톤 3모듈 강의
> **학습 기간 권장:** 6주 (주당 8~10시간) — 단축 시 4주 / 심화 시 8주
> **최종 산출물:** 본인 도메인에 특화된 미니 랄프톤 1개 (End-to-End 자동화 하네스)

---

## 0. 학습 목표 (Outcome)

이 플랜을 끝내면 다음을 **혼자 할 수 있어야** 한다.

1. **개념 수준**: 프롬프트 엔지니어링 / 에이전트 엔지니어링 / 하네스 엔지니어링 3세대를 구분하고, 하네스가 왜 필요한지 설명할 수 있다.
2. **구조 수준**: GOAL·RULE·Spec·Drift·Permission·Knowledge 6개 레이어를 실제 파일로 분리해 구성할 수 있다.
3. **루프 수준**: Ralph Loop(영속 실행)와 Karpathy Loop(자동 진화) 두 루프 패턴의 차이를 알고, 적합한 상황에 골라 쓸 수 있다.
4. **운영 수준**: Drift·환각·중단·오작동을 감지하는 Observability 레이어를 붙이고, Exit Hook·Guardrail로 안전하게 종료시킬 수 있다.
5. **도메인 수준**: 자신의 업무 도메인 하나를 골라 End-to-End 자동화 하네스를 설계·구현·디버깅할 수 있다.

---

## 1. 사전 요구사항 (Prerequisites)

| 영역 | 최소 수준 | 확인 방법 |
|---|---|---|
| LLM 사용 | ChatGPT / Claude를 1개월 이상 실무 사용 | 직접 코드·문서 생성 경험 |
| 프롬프트 엔지니어링 | system/user/assistant 역할, few-shot, CoT 기본 | 프롬프트 1개 튜닝 경험 |
| CLI / Git | branch, commit, diff, rebase 기본 | 자기 리포 1개 운영 |
| 에디터 | Claude Code / Cursor / Codex CLI 중 1개 | 실제 커밋 1건 이상 |
| 파일 규칙 | YAML, Markdown, JSON 읽고 쓰기 | —  |

> 부족한 항목이 2개 이상이면 Phase 0을 2주로 확장할 것.

---

## 2. 전체 로드맵

```
Phase 0  ─  기초 다지기            (1주)   ─ 읽기 중심
Phase 1  ─  Ralph Loop 뼈대        (1.5주) ─ 강의 모듈 1
Phase 2  ─  Karpathy Loop 진화     (1.5주) ─ 강의 모듈 2
Phase 3  ─  미니 랄프톤 프로젝트   (2주)   ─ 강의 모듈 3
```

각 Phase는 **이론 → 최소 예제 → 실전 과제 → 자기 점검** 순서로 고정.

---

## Phase 0. 기초 다지기 (1주)

### 목표
“하네스가 왜 필요한가”에 대한 관점을 형성한다. 모듈 1을 들어가기 전에 용어 장벽을 제거한다.

### 학습 항목
- 3세대 AI 엔지니어링 개념 정리
  - 1세대: 프롬프트 엔지니어링 (1회성 요청/응답)
  - 2세대: 에이전트 엔지니어링 (도구 사용, 계획-실행 루프)
  - 3세대: 하네스 엔지니어링 (영속 루프·자가 검증·자기 개선)
- 레퍼런스 읽기 (원문 1회 + 요약 1회)
  - Geoffrey Huntley — “Ralph Wiggum as a Software Engineer”
  - Andrej Karpathy — “Software 3.0” / editable asset & scalar metric 개념
  - Anthropic — “Building effective agents”
- 용어 사전 작성 (본인 언어로 1줄씩)
  - GOAL / RULE / Spec / Drift / Permission / Knowledge / Guardrail / Exit Hook / Back-pressure / Observability

### 실습 과제
- `harness-engineering/glossary.md` 작성 — 위 용어를 **자기 문장으로** 정의
- 기존에 자주 쓰는 LLM 작업 1개를 골라 “이걸 하네스로 자동화한다면 GOAL/RULE은?” 한 장 짜리 설계 노트 작성

### 자기 점검
- [ ] 하네스 엔지니어링이 에이전트 엔지니어링과 어떻게 다른지 1분 말하기 가능
- [ ] Drift를 수치화한다는 말의 의미를 설명 가능
- [ ] Ralph Loop와 Karpathy Loop 중 자기 업무에 맞는 건 무엇인지 직감적 판단 가능

---

## Phase 1. Ralph Loop 기반 루프 구축 (1.5주)

> **강의 매핑:** 모듈 1 · “멈추지 않고 끝까지 가는 하네스 뼈대 짓기”

### 이론 (3일)
1. **Ralph Loop 패턴**
   - 영속 실행 = 같은 프롬프트를 시간축에서 반복 호출
   - “Ralph Wiggum” 은유 — 단순함을 **지속성**으로 이긴다
   - OpenAI Codex / Claude Code 내부에서의 구현 사례
2. **구조 레이어 (Structure)**
   - GOAL 파일: “무엇을 달성해야 하는가”
   - RULE 파일: “무엇을 해도 되고 하면 안 되는가”
   - 컨텍스트 분산 배치 전략 — 왜 한 파일에 몰빵하면 안 되는가 (token dilution, attention decay)
3. **요구사항(Spec) 설계**
   - Spec = 에이전트 활동의 “울타리”
   - 범위(Scope) / 입력/출력 / 성공 기준 / 실패 기준
4. **Drift 명세**
   - Drift = 인간 의도와 AI 결과 간의 오차
   - 수치화: 라인 diff, 테스트 실패율, 스펙 위반 카운트, embedding similarity 등
5. **권한 레이어 (Permission) — 4층 게이트**
   - LLM 레이어: 모델/프롬프트 접근 제한
   - MCP 레이어: 외부 도구 호출 제어
   - DB 레이어: read/write 분리
   - Codebase 레이어: 파일·브랜치 접근 제한
6. **지식 레이어 (Knowledge)**
   - 스킬 레지스트리 = “이 하네스가 쓸 수 있는 스킬 카탈로그”
   - 외부 도구 커넥터 = MCP / 함수 호출 / CLI wrapper

### 실습 (5일)
**실습 프로젝트:** “Markdown 문서 자동 리뷰어” 미니 하네스

| Day | 과제 | 산출물 |
|---|---|---|
| D1 | 전역 규칙 파일 세팅 | `CLAUDE.md` + `AGENTS.md` 최소 버전 |
| D2 | GOAL / RULE 분리 | `goals/review.md` + `rules/style.md` |
| D3 | Ralph Loop 구현 | 같은 프롬프트를 N회 돌려 수렴 확인하는 shell/Python 스크립트 |
| D4 | Spec + Drift 명세 | `spec.md` + `drift.md` (실패 시나리오 최소 3개) |
| D5 | MCP 외부 도구 연동 | read-only / write 권한을 분리한 MCP 설정 `.mcp.json` |

### 자기 점검
- [ ] 동일 프롬프트 반복 호출로 “진전”을 만드는 구조를 설명 가능
- [ ] GOAL과 RULE을 한 파일에 두면 안 되는 이유를 레이어 관점에서 설명 가능
- [ ] MCP 권한 분리를 설계 시점에 고려할 수 있음
- [ ] Drift를 최소 1가지 수치로 정의해봄

### 흔한 함정
- **GOAL에 RULE을 섞는다** → 모델이 제약과 목표를 혼동하면서 규칙 위반 빈도 ↑
- **Loop 종료 조건을 안 넣는다** → 무한 루프로 토큰/비용 폭주. Phase 2의 Exit Hook까지 가기 전엔 반드시 iteration cap를 건다
- **권한 레이어를 코드에 하드코딩** → 설정 파일 한 줄 수정이 코드 리팩터링으로 변함

---

## Phase 2. Karpathy Loop 자동 진화 루프 (1.5주)

> **강의 매핑:** 모듈 2 · “스스로 검증하고 개선하는 하네스 완성”

### 이론 (3일)
1. **Karpathy Loop 3요소**
   - Editable asset: 루프마다 수정 가능한 대상 (코드·문서·프롬프트)
   - Scalar metric: 개선을 판단할 단일 수치 (테스트 통과율, lint 에러 수, latency 등)
   - Time-box: 루프 당 허용 시간/토큰 한도 — 수렴 실패 시 강제 종료
2. **Task Classifier · Model Router**
   - 작업 분류 → 난이도/도메인별 최적 모델 라우팅
   - 예: 요약 = Haiku, 코드 생성 = Opus, 검증 = Sonnet
3. **설계 모델 ⇄ 검증 모델 자동 반복**
   - Generator ↔ Critic 2역할 분리
   - Exit Hook: scalar metric이 N회 연속 개선 없음 → 종료
4. **Guardrail**
   - 샌드박스: 위험 작업을 격리 실행 (docker / worktree / ephemeral DB)
   - 위험 작업 차단: `rm -rf`, `git push --force`, 프로덕션 DB write 등 deny-list
5. **검수 자동화 (Back-pressure)**
   - Test / Lint / Type checker가 루프의 **압력원**
   - Failing test가 있으면 루프가 전진하지 못하게 설계
6. **관측 레이어 (Observability)**
   - 환각 검증: 출처 없는 주장 감지 / 허위 파일 경로 탐지
   - 로그 스냅샷: 각 iteration의 input/output/metric 기록
   - 모니터링: 실시간 metric 그래프, drift 알람

### 실습 (5일)
**실습 프로젝트:** Phase 1의 문서 리뷰어를 **자동 진화형**으로 업그레이드

| Day | 과제 | 산출물 |
|---|---|---|
| D1 | Task Classifier + 작업 분해 | `classifier.py` 또는 YAML 라우팅 규칙 |
| D2 | Generator ↔ Critic 루프 + Exit Hook | `loop.py` (메트릭 수렴 시 종료) |
| D3 | Guardrail | sandbox 디렉터리 격리 + deny-list |
| D4 | Test/Lint 연결 | CI 스크립트 또는 `pre-commit` 훅 |
| D5 | **⭐ 특별 세션 매핑** | Polysona 아키텍처 해부 요약 — 아키텍처 다이어그램 1장 재현 |

### 자기 점검
- [ ] editable asset / scalar metric / time-box 3요소를 본인 프로젝트에 대응시킬 수 있음
- [ ] Generator–Critic 분리가 왜 단일 모델 자기검증보다 강한지 설명 가능
- [ ] Guardrail이 막지 못하는 상황 1개를 식별할 수 있음 (완벽한 방어는 없다는 감각)
- [ ] 환각 검증 규칙을 최소 2개 정의해봄

### 흔한 함정
- **scalar metric을 여러 개 둔다** → 방향을 잃는다. 하나로 수렴시키고, 다른 건 guard로 내려라
- **Critic이 Generator보다 약하다** → Critic을 동급 이상으로 써야 진짜 압력이 된다
- **Guardrail을 붙이고 끝낸다** → 관측 없이 guardrail만 있으면 왜 막혔는지 모른다

---

## Phase 3. 미니 랄프톤 — 내 도메인 맞춤 하네스 구축 (2주)

> **강의 매핑:** 모듈 3 · “내 도메인 맞춤 하네스 직접 구축”

### 이론 (2일)
- Ralph Loop + Karpathy Loop 결합 전략 — 언제 어느 쪽을 바깥 루프로 둘지
- End-to-End 에이전트 워크플로우: 기획 → 실행 → 검증 → 배포
- IaAC (Infra as Agentic Code) 개념 — 인프라까지 에이전트가 다루는 설계
- Self-Improving CI/CD — 파이프라인이 스스로 실패 원인을 분석·수정

### 메인 프로젝트 (10일)
**과제:** 자신이 **실제로 반복 수행하는 업무 1개**를 End-to-End 자동화하는 하네스를 만든다.

#### 주제 선정 가이드 (택1)
1. 개인 블로그/뉴스레터 자동 발행 파이프라인
2. 기술 문서 자동 번역·교정 하네스
3. 코드 리뷰 보조 하네스 (PR diff → 리뷰 코멘트 자동 생성·검증)
4. 데이터 분석 레포트 자동 생성 (쿼리→그래프→해석)
5. 테스트 자동 작성·실행·수정 루프
6. 본인 직무 특화 주제 (강사와 협의)

#### 산출물 요구사항
- [ ] `GOAL.md`, `RULES.md`, `SPEC.md`, `DRIFT.md`, `PERMISSIONS.md`, `KNOWLEDGE.md` 6개 파일
- [ ] Ralph Loop 스크립트 (영속 실행 엔트리포인트)
- [ ] Karpathy Loop 스크립트 (Generator/Critic + Exit Hook)
- [ ] Guardrail 설정 (sandbox + deny-list)
- [ ] Observability: iteration별 log JSON + scalar metric 그래프 1장
- [ ] End-to-End 데모 영상 또는 터미널 녹화 (5분 이내)
- [ ] 회고 문서 1장 — 실패한 시도 3개 + 해결책

#### 단계별 일정
| 주차 | 주요 마일스톤 |
|---|---|
| W1 D1–2 | 주제 확정 + GOAL/RULE 초안 |
| W1 D3–5 | Ralph Loop 최소 작동 버전 (MVP) |
| W2 D1–3 | Karpathy Loop 및 Observability 통합 |
| W2 D4 | Guardrail + 배포 레이어 |
| W2 D5 | 데모 + 회고 + 리팩터링 |

### 학습 포인트 (강의와 동일)
- 강사 1:1 피드백이 있으면 적극 활용
- 에러 로그 · Drift 패턴을 **데이터로** 분석 (눈으로 보지 말고 집계)
- 하네스 리팩터링은 한 번 이상 반드시 수행 — 첫 버전은 늘 과설계 or 저설계

### 자기 점검 (최종 검증)
- [ ] 하네스를 **다른 사람이 인수인계 받아 30분 안에 실행** 가능한 수준의 문서
- [ ] 동일 주제를 매뉴얼로 했을 때 대비 시간 절감 수치 제시 가능
- [ ] 최소 1회 실제로 Drift/환각이 감지되고 Exit Hook이 동작한 로그 보유
- [ ] 6개 레이어 파일 중 **어느 한 줄을 수정하면 어떤 행동이 바뀌는지** 모두 설명 가능

---

## 3. 학습 리소스

### 필수
- Geoffrey Huntley, “Ralph Wiggum as a Software Engineer” (원문 블로그)
- Andrej Karpathy, “Software 3.0” 강연 / 관련 트윗 스레드
- Anthropic, “Building effective agents”
- Anthropic MCP 공식 문서
- Claude Code / Cursor / Codex CLI 중 택1의 `CLAUDE.md` / `AGENTS.md` 규약 문서

### 권장
- Simon Willison 블로그 — agent 운영 실전 기록
- LangGraph / CrewAI / AutoGen 1차 자료 (비교용, 모방용 아님)
- 본인 선택 강의 Polysona 아키텍처 자료 (특별 세션)

### 도구
- 에디터: Claude Code 또는 Codex CLI
- 버전관리: git + worktree (sandbox 용)
- Observability: 최소 JSON 로그 + matplotlib/Observable 시각화
- MCP 서버: 최소 1개 (filesystem 또는 fetch) 구성 경험

---

## 4. 진도 관리 템플릿

```
주차:
이번 주 GOAL:
완료한 레이어:
열린 Drift:
다음 주 EXIT 조건:
```

매주 금요일 15분 이내로 위 5줄을 작성한다. 그 이상 쓰면 하네스가 아니라 일기가 된다.

---

## 5. 이 플랜을 언제 수정해야 하는가

- Phase 1을 끝냈는데 Ralph Loop “왜 돌리는지” 감이 안 오면 → Phase 0으로 되돌아가서 레퍼런스 재독
- Phase 2에서 scalar metric을 못 정의하면 → 프로젝트 주제가 너무 광범위. 더 좁혀라
- Phase 3에서 2주차에 MVP도 안 만들어졌다면 → 주제를 절반으로 줄이고 다시 시작. 늘리지 말고 **잘라내라**

> **원칙:** 하네스의 본질은 “완벽한 첫 버전”이 아니라 “지속 가능한 루프”다. 이 플랜 자체도 루프처럼 돌려라.
