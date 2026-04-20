# 부록 C — 체크리스트 모음

체크리스트는 본문의 장식이 아니다. 회의에 들어갈 때, PR을 올릴 때, 보안팀과 마주 앉을 때 **한 장 뽑아 옆에 두는** 운영 도구다. 각 리스트는 8~15문항으로 단출하게 유지했다. 10문항이 넘는 체크리스트는 대개 체크하지 않는다.

각 절 끝의 `(→ N장)`은 본문 근거 장을 가리킨다.

## 1. 도구 선택 체크리스트 (→ 2장)

- [ ] **거버넌스 제약을 먼저 본다.** OSS·온프레미스·에어갭 강제가 있는가? Yes면 Aider 루트, 아니면 계속.
- [ ] **기존 툴체인 이탈 비용을 계산했다.** 팀이 이미 Cursor·Cline에 익숙한가? 전환 비용이 기능 이득보다 큰가?
- [ ] **훅·서브에이전트·관측성 필요성 확인.** 필요하면 Claude Code, 불필요하면 경량 옵션.
- [ ] **OS 샌드박스·비동기 자율성이 필요한가.** 회의 중 1~30분 태스크를 돌릴 것인가? Yes면 Codex.
- [ ] **팀 인원 × 1인당 일일 세션 × 세션당 토큰 ≈ 월 예산**으로 추정치를 내봤다.
- [ ] **선택 근거 1페이지**를 `decisions/tool-choice.md`에 커밋했다.
- [ ] **6개월 뒤 재검토 일정**을 캘린더에 넣었다.

## 2. `AGENTS.md` 품질 체크리스트 (→ 3장)

- [ ] **200줄 이하**다.
- [ ] **5섹션 구조** (GOAL / BUILD / TEST / STYLE / DON'T)를 따른다.
- [ ] **LLM이 쓰지 않았다.** 사람이 실패를 겪고 직접 적었다.
- [ ] **DON'T 항목마다 PR 번호 또는 날짜**가 붙어 있다. 실패 없는 규칙은 없다.
- [ ] **모노레포라면 path-scoped로 분산**됐다. 루트에 몰려있지 않다.
- [ ] **"LLM이 이미 아는 관례"는 싣지 않았다.** React 함수형 컴포넌트 같은 것.
- [ ] **실패 로그 append-only 섹션**이 있다.
- [ ] **소유자(CODEOWNERS 또는 상단 주석)**가 명시됐다.
- [ ] **분기 재검토 일정**이 `DON'T`에 붙은 규칙별로 있다.
- [ ] **A/B 실험으로 효과 측정을 시도**해봤다(결과가 노이즈여도 기록).

## 3. 루프 설계 체크리스트 (→ 4장)

- [ ] **Karpathy 3요소가 충족**됐다: editable asset 하나, scalar metric 하나, time-box 하나.
- [ ] **적합 matrix의 좌상단**(스크립트 판별 가능 + 판단 의존 낮음)에 태스크가 찍히는가? 아니면 ReAct·Plan-and-Execute로 옮긴다.
- [ ] **PLAN과 BUILD가 분리**됐다. 같은 프롬프트에 섞지 않았다.
- [ ] **exit hook 최소 3종**: `MAX_ITERATIONS`, `MAX_TOKENS`, 델타 정체.
- [ ] **Back-pressure는 외부 검증**(테스트·린터·타입체커)이다. LLM 자체 판단이 아니다.
- [ ] **실패 모드 이름** (Overcooking / Undercooking / Completion promise / Context pollution)으로 최근 사고를 분류할 수 있다.
- [ ] **iteration당 비용 로그**를 기록한다. 토큰·시간·개입 횟수.
- [ ] **Completion promise 탐지**: 모델이 "완료"를 선언하면 외부 검증으로만 인정한다.

## 4. 검증 파이프라인 체크리스트 (→ 6장)

- [ ] **Generator와 Critic이 분리**됐다. 세션도 프롬프트도 rubric도.
- [ ] **Critic 모델 급이 Generator와 같거나 그 이상**이다.
- [ ] **LLM-as-judge는 pairwise-with-swap**만 쓴다. 절대 점수 의사결정 금지.
- [ ] **swap inconsistent 비율이 30%를 넘으면** 그 judge는 신뢰하지 않는다.
- [ ] **CoVe 검증 단계는 독립 세션**에서 실행된다. 컨텍스트 carry-over 없음.
- [ ] **Critic rubric 5~7개**가 명시됐다. "느낌상 괜찮다" 금지.
- [ ] **결정적 외부 검증**(pytest·ruff·mypy·tsc)이 배포 게이트다.
- [ ] **`required_tests.txt`**는 에이전트가 수정할 수 없다.
- [ ] **새 테스트가 기존을 깨면 루프 중단.** git diff로 자동 감지.

## 5. 위협 모델 체크리스트 (→ 9장)

**기본 방어 (필수 7문항)**

- [ ] **샌드박스 안에 비밀이 없다.** 1Password CLI `op run` 같은 one-shot injection 패턴.
- [ ] **`PreToolUse` 훅**이 `rm -rf /`, `git push --force`, secret key 패턴을 차단한다.
- [ ] **간접 인젝션 재현 리포트**가 있다. README에 공격 페이로드 심고 방어 검증.
- [ ] **MCP 서버는 신뢰할 수 있는 출처**만 사용. npm/pypi 공급망 검사 통과.
- [ ] **감사 로그**에 `input_hash`·`output_hash`·`actor`·`session_id`·`policy_version` 필드가 있다.
- [ ] **관리자 정책(managed policy)**이 최상위 경계를 잠근다.
- [ ] **비상 런북 1페이지**가 있다.

**SOC2 / ISO27001 매핑 (추가 5문항)**

- [ ] **CC 6.1 (논리적 접근 통제):** actor/session별 권한 경로가 로그에서 재구성 가능.
- [ ] **CC 7.2 (시스템 운영 이상 감지):** 훅 deny·예산 초과·세션 실패가 알람과 연결.
- [ ] **CC 8.1 (변경 관리):** 정책 파일 변경이 PR 기반, `policy_version`으로 추적.
- [ ] **GDPR Art. 32 (적절한 보안):** PII 필드 redaction이 로그 파이프라인에 박혀 있다.
- [ ] **ISO 27002 A.8.28 (시큐어 코딩):** AI PR에 대한 코드 리뷰 프로세스가 사람 리뷰와 동일 강도.

## 6. CI·비용 체크리스트 (→ 10장)

- [ ] **`MAX_THINKING_TOKENS`가 팀 표준값**으로 `.github/workflows/*.yml`에 고정.
- [ ] **iteration cap = CI timeout**. 둘이 함께 걸려 있다.
- [ ] **라우터**(Haiku↔Opus 최소 이분)가 붙어 있다.
- [ ] **감사 로그 JSONL**이 CI artifact로 업로드된다.
- [ ] **월 예산 50%·80%·100% 알람**이 Slack 또는 PagerDuty로 연결됐다.
- [ ] **worktree 격리**로 main에 직접 쓰지 않는다.
- [ ] **merge 전 human gate**가 있다. 대화 이력이 아니라 diff 기준.
- [ ] **재시도 정책**: 최대 2회, iteration 총량 합산.
- [ ] **관측 대시보드**(Grafana 등)에 비용·tokens·exit_reason이 시간축으로 올라가 있다.

## 7. 캡스톤 제출 체크리스트 (→ 12장, 부록 E)

**필수 7문항 (본문 12장)**

- [ ] **Pareto 플롯 1장**이 `decisions/harness-postmortem-v1.md`에 커밋.
- [ ] **manual baseline 점**이 플롯 위에 있다.
- [ ] **개입률(intervention rate)**이 overlay로 찍혀 있다.
- [ ] **실패 3개**가 한 줄씩 요약됐다.
- [ ] **다음에 다르게 할 것 3개**가 적혔다.
- [ ] **4가지 의심 신호** 중 어느 것도 켜지지 않았음을 확인했다. 또는 켜졌다면 그 결론을 기록했다.
- [ ] **commit SHA**가 서문의 달력 약속 자리에 붙었다.

**심화 워크북 (부록 E 진입 시 추가)**

- [ ] **산출물 7종** — `AGENTS.md` / 루프 스크립트 / Generator–Critic 또는 back-pressure / 위협 모델 1p / 훅·approval 정책 / CI 통합 / 감사 로그 샘플 — 이 레포에 모두 있다.
- [ ] **동료 재현 테스트**: 30분 안에 세팅이 끝나는가.
- [ ] **Pareto 플롯 v2**가 10 iteration × 3 seed 기반으로 다시 그려졌다.
