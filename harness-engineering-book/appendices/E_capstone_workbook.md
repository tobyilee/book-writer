# 부록 E — 캡스톤 워크북 (2주 프로그램)

본문 12장은 포스트모템 한 페이지로 마감된다. 그 한 페이지를 쓰며 "조금 더 깊게 태우고 싶다"는 독자를 위해 이 부록을 분리해 두었다. **2주짜리 end-to-end 프로젝트**로, 평일 저녁 30분~2시간과 주말 반나절이면 완주가 가능하다. 전적으로 옵셔널이다. 포스트모템 1장만 들고 책을 덮어도 이 책의 완독 조건은 충족된다는 점을 먼저 못 박아둔다.

## 0. 주제 선정 가이드

2주 안에 "증거가 commit되는" 프로젝트를 고르려면 Karpathy 3요소가 모두 확보되는 주제여야 한다. 아래 일곱 후보 중 자기 직무에 가까운 하나를 고르자.

1. **코드 리뷰 보조** — editable asset: PR 본문과 review 코멘트. scalar: 리뷰어가 남긴 수정 제안 수 대비 에이전트가 맞춘 비율. time-box: PR 1건당 5분.
2. **테스트 자동 보강** — asset: `tests/`. scalar: 커버리지 델타 + required_tests 통과 guard. time-box: 모듈당 3분.
3. **번역 파이프라인** — asset: 번역 초안 마크다운. scalar: 역번역 BLEU 또는 검증 질문 일치율. time-box: 문서당 2분.
4. **데이터 분석 레포트** — asset: Jupyter/SQL 스크립트. scalar: 사전 정의된 KPI가 기대치 ±5% 안에 있는지. time-box: 레포트당 4분.
5. **티켓 분류** — asset: 분류 프롬프트 YAML. scalar: hold-out 세트 정확도. time-box: 티켓당 0.5초.
6. **배포 체크리스트 자동화** — asset: PR 템플릿. scalar: 체크리스트 항목 대비 자동 통과 수. time-box: PR당 2분.
7. **본인 직무 특화** — 위 여섯에 매핑이 안 된다면, 1장 실습의 루브릭으로 Karpathy 3요소 충족 여부를 먼저 점검한다. 세 요소 중 time-box가 안 나오면 자동화 대상이 아니다. 주제를 바꾸는 편이 낫다.

## 1. 필수 산출물 7종

2주 끝에 이 일곱 파일이 본인 레포에 커밋되어 있어야 한다. 하나라도 비어 있으면 워크북은 미완으로 본다.

1. **`AGENTS.md` (≤200줄, 5섹션)** — 부록 B 템플릿 중 주제에 가까운 것을 시작점으로. 실패 로그에 1건 이상.
2. **루프 스크립트** — `harness/run.sh` 또는 `.py`. Ralph든 ReAct든 Plan-and-Execute든 편한 것으로. exit hook 3종 포함.
3. **Generator–Critic 또는 back-pressure 루프** — critic 프롬프트와 rubric, 또는 `required_tests.txt` + 회귀 가드.
4. **위협 모델 1페이지** — `docs/threat-model.md`. 인젝션 재현 1건 + 훅 차단 3패턴 + 잔여 리스크 2줄.
5. **훅·approval 정책** — `.claude/hooks/*.sh` 또는 `.codex/policy.yaml`. bypass 모드에서도 실제로 차단됨을 로그로 증명.
6. **CI 통합** — `.github/workflows/harness.yml` 1건. iteration cap = CI timeout, 감사 로그 artifact 업로드.
7. **감사 로그 스키마 + 1일치 샘플** — 10장 스키마대로 JSONL. 24시간 운영 로그 1회 수집.
8. **(번외) 비용 시뮬레이터** — 라우터 전/후 월 예산 추정 스프레드시트. 이 번외가 있으면 `[연쇄 4시간]` 완주로 본다.

## 2. Day 1 ~ Day 14 일정 템플릿

아래는 평일 저녁 30~90분, 주말 2~4시간을 전제로 한 표준 일정이다. 자기 페이스에 맞춰 조정하되, Day 7 중간 점검과 Day 14 포스트모템은 옮기지 말자.

| Day | 주제 | 산출물 | 예상 시간 | 본문 참조 |
|---|---|---|---|---|
| 1 | 주제 확정 + baseline 측정 | `harness-notes.md`에 baseline 1줄 | 60분 | 서문, 1장 |
| 2 | `AGENTS.md` v1 작성 (5섹션 골격) | `AGENTS.md` 초안 | 90분 | 3장 |
| 3 | 루프 스크립트 뼈대 + editable asset 지정 | `harness/run.sh` (exit 없이) | 60분 | 4장 |
| 4 | exit hook 3종 + scalar metric 계산 | 첫 iteration 로그 | 90분 | 4장, 5장 |
| 5 | Pareto 2축 플롯 첫 스케치 | `harness/pareto_v0.png` | 60분 | 5장 |
| 6 | Generator–Critic 또는 back-pressure 추가 | critic 프롬프트 또는 `required_tests.txt` | 120분 | 6장 |
| 7 | **중간 점검** — v1 시연 (동료 1인 대상 10분) | 피드백 3줄 | 60분 | 전반 |
| 8 | 인젝션 재현 + 훅 1개 | `docs/threat-model.md` 초안 | 120분 | 9장 |
| 9 | 훅 3패턴 완성 + bypass 증명 로그 | 훅 스크립트 commit | 90분 | 9장 |
| 10 | CI workflow 작성 + iteration cap | `.github/workflows/harness.yml` | 120분 | 10장 |
| 11 | 라우터 + 감사 로그 JSONL | 1일치 샘플 로그 | 90분 | 10장 |
| 12 | 10 iteration × 3 seed 측정 | metrics_log.csv 최종 | 180분 | 5장, 6장 |
| 13 | Pareto 플롯 v2 + 팀 공유 | `decisions/pareto-v2.md` | 90분 | 5장, 12장 |
| 14 | **포스트모템 1페이지** + commit SHA 서문에 회수 | `decisions/harness-postmortem-v1.md` | 120분 | 12장 |

Day 7 중간 점검은 팀원·친구·지금의 자신에게 말로 설명하는 10분을 확보하는 자리다. 설명이 막히면 어느 산출물이 부족한지 드러난다. 거기서 멈추는 편이 낫다.

## 3. 동료 재현 테스트 (Day 12~13에 수행)

자신의 레포를 초기화 상태로 돌려 "30분 안에 처음부터 돌려볼 수 있는가"를 실측한다. 통과 조건은 셋이다.

- **README 한 장으로 모든 전제 도구 설치 가능.**
- **한 번의 `./harness/run.sh`로 1 iteration이 성공.**
- **CI가 PR 하나에서 녹색으로 도는 모습을 동료가 눈으로 확인.**

실패하면 그 자체가 Day 13·14의 재료다. 허술한 곳이 드러난 것이지 워크북이 실패한 것은 아니다.

## 4. 심화 실습 아카이브

본문이 `[연쇄 4시간]` 또는 옵셔널로 분류한 과제들을 워크북에서 정식으로 깔끔하게 돌려보는 자리. 산출물은 각 본문 장의 "체크포인트" 형식을 따르되 분량은 확장한다.

### 4.1 6장 CoVe 구현 (Day 11~12 옵션)

본인 도메인 질문 10개로 다음을 수행한다.

1. Baseline 답변 10건 생성 (단일 세션).
2. CoVe 4단계: draft → 검증 질문 2~4개 → **새 세션**에서 각 검증 질문 독립 답변 → 최종 답 합성.
3. 사실 오류 수·토큰·시간을 baseline vs CoVe로 비교. 독립 세션 증거(새 API 호출 로그, 빈 시스템 프롬프트)를 함께 남긴다.

### 4.2 6장 10×3 seed back-pressure (Day 12)

본문 6장 본격 실습이 `3 iteration × 1 seed`로 축소돼 있었다. 여기서 **10 iteration × 3 seed**로 확장하자.

- 같은 editable asset에 서로 다른 3개 seed를 준다.
- 각 seed에서 10 iteration을 돌려 성공/실패/사유를 기록.
- 30개 iteration의 성공률·실패 사유 히스토그램·비용 분포를 `reports/backpressure_10x3.md`에 정리.
- seed 간 표준편차가 크다면 exit hook이 덜 단단하다는 신호다.

### 4.3 10장 full workflow (Day 10~11)

본문 10장의 `[연쇄 4시간]`을 캡스톤 인프라로 승격한다.

- `.github/workflows/harness-on-pr.yml`에 Haiku→Opus cascade 라우팅을 엮는다.
- 매 iteration의 감사 로그 JSONL을 artifact로 업로드.
- 주간 예산 50% 도달 시 Slack webhook 또는 workflow log `::warning::` 알람.
- 실제로 알람이 한 번 발동하는 PR을 하나 만들어본다 (iteration cap을 일부러 낮춰서).

## 5. 제출 체크리스트 (Day 14 최종)

부록 C의 "캡스톤 제출 체크리스트"를 다시 열어 7개 필수 항목과 3개 심화 항목을 모두 체크한다. 전부 체크됐다면 **이 책의 완독이 아니라 "완주"를 기록한 것**이다. 포스트모템의 commit SHA를 서문의 달력 자리에 붙이고, 한 달 뒤 같은 플롯을 다시 그려볼 일정을 캘린더에 꽂자. 하네스의 진짜 평가는 점 하나가 아니라 점 두 개가 찍힌 뒤에 시작된다.

워크북이 부담스럽다면 Day 1 하나만 해도 좋다. 서문의 baseline이 한 줄 추가되는 것만으로도, 책을 덮은 뒤의 자기 하네스가 다음 달에 바뀔 기반이 생긴다.
