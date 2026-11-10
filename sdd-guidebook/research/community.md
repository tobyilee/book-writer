# 커뮤니티 리서치: AI 코딩 에이전트와 SDD 실전 (실습서용 보강)

- 조사일: 2026-11-10 (WebSearch·WebFetch·`gh` CLI)
- 장르: tech-book / 슬러그: sdd-guidebook
- 범위: `research/sdd-report.md` 7절(의견 연대표·찬반·한일 커뮤니티·인프런·경험칙)과 8절(실패·회복 사례)은 다시 쓰지 않는다. 이 문서는 그 빈칸만 채운다.
  1. 실제 스펙 파일이 보이는 실무 워크스루 (리뷰 전후, 에이전트가 틀린 점)
  2. 도구 없는 SDD (평범한 마크다운, 인터뷰 프롬프트, AGENTS.md/CLAUDE.md + SPEC.md + 체크리스트)
  3. 도구를 매일 쓸 때의 함정 (스펙 비대, 리뷰 피로, 드리프트, 토큰 비용)과 사람들이 고친 방법
  4. 한국 개발자 실사용 글
- 중복 제외: 보고서 참고 문헌에 이미 있는 URL(Scott Logic, Marmelab, Böckeler, Asana, Kurly, KIM Jongwan velog, sammy velog, GeekNews 23074·24400, Matsen, Incomplete Developer, irr123, Spec Kit #1191 등)은 새 항목으로 쓰지 않았다.
- 표기: 모든 수치와 주장은 **커뮤니티 의견, 검증 필요**다. 별도 표시가 없으면 작성자 1인의 자기 보고다. 인용은 짧은 구절만 남기고 나머지는 요지로 옮겼다. 출처 번호는 문서 끝 `C1~C32` 목록을 따른다.

---

## A. 실물 스펙이 보이는 워크스루

실습 장(5장 "실제 스펙 예시")에 그대로 옮겨 쓸 수 있는 사례들이다. "리뷰 전 → 리뷰 후"가 숫자나 줄 번호로 남아 있는 것을 우선 골랐다.

### A1. 한 문장 SPEC.md가 157줄이 되기까지 (인터뷰 프롬프트) [C2]
- 누가: Radek Sienkiewicz (VelvetShark), 2026-01-02. 기법의 출처는 Claude Code 팀 엔지니어 Thariq의 X 게시물이며, 사흘 만에 조회 130만 이상과 북마크 1만 이상을 받았다고 저자는 적는다.
- 리뷰 전: `SPEC.md`에 한 문장 ("북마크를 저장하고 검색하는 CLI 도구").
- 과정: Claude에게 SPEC을 읽고 `AskUserQuestion` 도구로 깊게 인터뷰한 뒤 결과를 파일에 쓰라고 지시. 질문 32개.
- 리뷰 후: 157줄. 절은 기술 스택, 데이터 모델, 명령, 출력 형식, 저장 형식, 첫 실행 동작, **비목표(non-goals)**.
- 구현: **새 세션**에서 "Implement @SPEC.md". 약 5분 만에 `bm add`와 `bm list`가 스펙대로 동작.
- 수치: 질문은 보통 20~30개, 복잡한 기능은 40~60개. 32개 중 약 3분의 1은 저자가 생각하지 못한 질문. 저자는 작업의 90%에 이 기법을 쓴다고 말한다.
- 재사용 형태: `~/.claude/commands/interview.md` 슬래시 명령. frontmatter에 허용 도구(AskUserQuestion, Read, Glob, Grep, Write, Edit)와 모델 지정. 덮어쓰기 전에 스펙 개요를 확인받는다.
- 저자가 밝힌 한계: 요구사항이 이미 분명하거나 변경이 작으면 과하다. 비목표를 넣어야 에이전트가 샛길로 빠지지 않는다.

### A2. 열 줄짜리 메모 → 질문 50개 → MVP 2시간 [C3]
- 누가: Charles McGuinness, 2025-12-29, "Stop Writing Specs for AI".
- 대조군: 한 문단 스펙으로 바로 바이브 코딩. 결과 앱은 위치를 40마일 떨어진 곳으로 잡아 기온이 틀렸고(52°F 대신 40°F), 챗봇이 예보를 가렸고, 구형 모델(gpt-4o-mini)을 썼다.
- SDD 경로: 프롬프트 3개 (① 스펙 인터뷰: 한 번에 질문 하나, 답마다 파일 갱신 ② 스펙의 빈틈을 묻고 `projectplan.md`에 태스크 목록 작성 ③ 태스크 순서대로 구현, 애매하면 멈추고 질문, 태스크마다 커밋).
- 수치: 질문 약 50개(권장 25~100개), 질문마다 선택지 2~3개. 인터뷰 약 1시간 + 구현 약 1시간.
- 책에 쓸 지점: 대조군 실패가 "스펙에 없던 결정(위치, 모델, 레이아웃)을 에이전트가 임의로 채운" 사례라서, 인터뷰가 무엇을 막는지 보여 주기 좋다.

### A3. SPEC.md 54행과 112행: 검사 세션이 찾은 결함 [C4]
- 누가: Ray, 2026-09-21, "30일 바이브 코딩" 시리즈 8일차 (가계부 앱 `money-note`).
- 흐름: ① 인터뷰 세션 (코드 쓰지 말 것, 질문 하나씩, 요구가 구체화되면 SPEC.md로 정리) ② `/clear` 뒤 **검사관 세션**: "만들 것"이 테스트 가능한지, "만들 것"과 "안 만들 것"이 충돌하는지, 본문에 나온 기능이 "만들 것"에서 빠졌는지만 보고하고 파일은 고치지 않음 ③ 사람이 쟁점마다 결정, AI가 SPEC.md 갱신 + **Decision Log** 절 추가 ④ 세 검사가 모두 "없음"일 때만 확정.
- 스펙 절: 동기, 사용자(1인), 유형(지출만, 수입은 10일차로 미룸), 필드(금액·분류·날짜·메모), 저장(로컬, 동기화 없음), 통계(월 합계·분류별 비율), 만들 것 / 안 만들 것(로그인·예산 알림·클라우드 동기화) / 수용 기준.
- 리뷰가 잡은 결함 두 개:
  - **SPEC.md:112** 월 이동은 무제한인데 "이번 달로 돌아가기"가 없음. 2019년에서 돌아오려면 ▶를 80번 넘게 눌러야 함 → 버튼 추가, 수용 기준 갱신.
  - **SPEC.md:54** 예시 데이터의 `date: "2026-08-07"`과 `createdAt: 1754534400000`(= 2025-08-07)이 1년 어긋남. 저자는 이런 샘플이 테스트와 시드로 복사된다고 경고 → 예시 수정.
- 책에 쓸 지점: "리뷰 전/후"를 **줄 번호**로 보여 주는 드문 사례다. 검사를 다른 세션에 맡기고 "보고만, 수정 금지"로 묶는 패턴은 도구 없이 할 수 있는 스펙 리뷰의 표준형으로 쓸 수 있다.

### A4. plan.md에 인라인 주석을 1~6회 달고 나서야 구현 [C5][C6]
- 누가: Boris Tane, 2026-02-11. Claude Code를 약 9개월 주 도구로 씀. GeekNews 번역(2026-02-23) 86점, 댓글 4개.
- 산출물: `research.md`(코드베이스를 "깊이" 읽고 쓴 보고서, 채팅 요약이 아니라 파일) → `plan.md`(접근법, 변경 코드 조각, 수정할 파일 경로, 트레이드오프) → plan 안의 체크리스트(단계·태스크, 에이전트가 완료 표시).
- 리뷰 방식: 저자가 plan.md에 직접 주석을 단다. 예: "PUT이 아니라 PATCH여야 한다"처럼 두 단어에서 한 문단까지. 수정 요청마다 끝에 `don't implement yet`를 붙인다. 이것이 없으면 에이전트가 계획이 충분하다고 판단하는 순간 코드를 쓰기 시작한다고 한다.
- 에이전트가 틀린 점 (research를 건너뛸 때): 기존 캐시 층 무시, ORM 관례 무시, 기존 엔드포인트 로직 중복. 계획 없이 시작하면 그럴듯하지만 틀린 초기 가정 위에 쌓아 올려 되돌리는 데 15분쯤 든다.
- 구현 중 교정: "still cropped", "wider" 같은 짧은 지시와 스크린샷. 방향이 틀리면 패치하지 않고 git 변경을 버린 뒤 범위를 좁혀 다시 시작.
- HN 댓글(GeekNews 번역 요약)에 나온 숫자: 계획을 1,500줄 이하 단위로 나눔, 3만 LOC 앱에 10만 줄짜리 계획, API 환각 루프로 30분에 $20 소모. 한국 댓글은 아래 D절.

### A5. spec.md → prompt_plan.md → todo.md (도구 없는 SDD의 원형) [C1]
- 누가: Harper Reed, 2025-02-16. 한국어판이 저자 블로그에 있다.
- 산출물: `spec.md`(브레인스토밍 결과, 개발자에게 넘길 수 있는 수준), `prompt_plan.md`(추론 모델이 쓴 단계별 코드 생성 프롬프트, 앞 단계 위에 쌓이고 마지막에 연결까지, 고아 코드 금지, TDD 변형 있음), `todo.md`(세션을 넘어 상태를 유지하는 체크리스트).
- 브레인스토밍 프롬프트의 핵심: 한 번에 질문 하나, 앞 답에 이어서. 끝나면 요구사항·아키텍처·데이터 처리·오류 처리·테스트 계획을 묶는다.
- 브라운필드 변형: 프로젝트 전체가 아니라 태스크마다 계획. repomix로 코드를 `output.txt`에 묶고, mise 태스크로 리뷰·이슈·누락 테스트·README 생성.
- 수치: 계획 단계 약 15분.
- 저자가 밝힌 한계: 앞서 나가기 쉽다(계획 문서와 테스트로 붙잡음), 팀으로 쓰기 어렵다(봇 충돌, 병합 지옥).
- 책에 쓸 지점: 2025년 초에 이미 "도구 없는 SDD" 3파일 구성이 있었다는 역사적 기준점. 7절 연대표(2025-07 Kiro부터 시작)보다 앞선다.

### A6. 연구 문서와 계획 문서를 나누고, 계획을 PR에 접어 넣기 [C8]
- 누가: Hartley Brody, 2026-03-09, "Markdown is the new source code".
- 파일: `.scratch/research/<시스템명>.md`(기존 패턴 기술, 갱신 시각 포함, 기능 간 재사용) / `.scratch/plan/{기능 요약}.md`(초기 프롬프트와 의도 절, 생성 날짜, 예상 LOC, 하단에 결정·변경 요약, 구현 후 구현 요약).
- 리뷰: 연구 문서가 내 이해와 맞는지 먼저 확인 → 계획에 인라인 주석(질문, 범위 축소, 선택지 결정) → 같은 채팅에서 반영·요약 → 새 채팅에서 구현 → 테스트보다 수동 확인 먼저 → **계획 문서를 PR 본문의 `<details>` 블록에 첨부**.
- 고친 문제: 계획 중 구현을 시작함 → 명시적으로 금지 / 앱 코드와 테스트 사이를 오가며 루프 → 첫 패스는 테스트를 건너뛰고 나중에 검토 / 덜 명세된 곳을 추측 → 모호한 점과 선택지를 목록으로 내게 함 / 재시작 시 진행 유실 → 계획 문서를 진실의 원천으로 계속 갱신. 계획이 PR 하나에 크면 쪼개게 한다.
- 스킬 4개로 묶음: `/research`, `/plan-create`, `/plan-update`, `/plan-implement`.

### A7. Spec Kit 195개 태스크, 그러나 압축은 코드 생성에만 [C24]
- 누가: Alejandro Wurm (OrangeLoops), 2026-05-19. NestJS 백엔드 + Expo/React Native 앱.
- 산출: 태스크 195개(백엔드 94, 프론트 101). 프론트는 백엔드의 OpenAPI 계약을 서비스 층 기준으로 씀.
- 시간: 백엔드 약 1시간 6분(세션 컨텍스트 약 95% 사용), 프론트 약 1시간(12단계 중 8단계만 기록, 타이밍 파일이 덮어써짐), 디자인 적용 약 4시간, **테스트·버그 수정·시드·시니어 리뷰·안정화 4일**. 총 2주 미만, 사내 기준 추정은 2명 6주.
- 에이전트가 틀린 점: 생성된 클라이언트가 기본 템플릿의 인증 토큰 헤더 동작을 옮기지 않아 UNAUTHORIZED 반복. Figma 적용에서 배치는 따라 했지만 폰트 굵기·색·간격은 놓침. 저장소가 둘이라 세션 사이 맥락을 사람이 옮겨야 했음.
- 저자 처방: 디자인을 스펙에 넣기, 스타일을 매번 명시, 결합된 저장소는 모노레포나 명시적 맥락 다리, **지표 기록은 에이전트가 편집하는 작업 공간 밖에** 두기, 사람 리뷰와 QA 시간을 따로 재기.
- 책에 쓸 지점: "코드 생성 시간"과 "출시 가능한 소프트웨어 시간"이 다르다는 숫자. 타이밍 파일을 에이전트가 덮어쓴 일화는 "측정 파일도 스펙 경계 밖에"라는 교훈으로 쓸 수 있다.

### A8. 코드 없는 라이브러리: 스펙 + 테스트만 배포 [C12]
- 누가: Drew Breunig. `whenwords`(2026-01, 상대 시간 포맷 라이브러리)와 2026-03-04 "SDD Triangle" 강연 정리.
- 구성: 마크다운 스펙 + 언어 중립 YAML 적합성 테스트 약 750개 + 에이전트에 붙여 넣을 `install.md`. 구현 코드는 없다. GitHub 별 1,000개 이상.
- 실제로 일어난 일: 외부 PR 하나가 스펙의 반올림 규칙을 어기는 **테스트**를 찾아냈다. 스펙·테스트·코드 세 꼭짓점이 서로를 검증한다는 저자 주장의 실례.
- 저자 교훈: 스펙과 테스트는 비싸다. 기존 테스트 스위트가 가장 따기 쉬운 열매다. 세 꼭짓점을 계속 맞춰 보라(git diff, 커버리지, 스펙 변경 이력, 스펙을 우회한 버그 수정, 에이전트 트레이스). 커밋 시 결정을 추출해 승인하게 하는 PoC 도구 Plumb을 냈고, "스킬은 제안일 뿐"이라 체크포인트여야 한다고 본다.

### A9. 한국어 예시: 테스트와 타입을 스펙으로 [C28]
- 누가: 달레(Dale Seo), 2026-03-21.
- 스펙 파일: `discount.test.ts`(쿠폰 할인 뒤 등급 할인, 합산 50% 상한, 가격 0원, 음수 할인율 오류), `types.ts`(`CartItem`, `Cart`, `CartService`), `CLAUDE.md` 개발 워크플로 절(타입 정의 → 스텁 → Red → Green → Refactor → 커밋 순서 강제).
- 예시 값: 10,000원, 쿠폰 10%, 등급 5% → 8,550원. 합산이 50%를 넘으면 5,000원으로 제한.
- 팁: 입출력이 분명한 비즈니스 로직에만 스펙을 쓰고 UI·인프라는 자연어 프롬프트. CI에서 타입 체크와 테스트를 필수 관문으로.
- 책에 쓸 지점: 한국 독자에게 익숙한 원화 예시라 "테스트를 스펙으로" 실습에 바로 쓸 수 있다.

---

## B. 도구 없는 SDD: 사람들이 실제로 쓰는 최소 키트

### B1. 공통 구성 (여러 출처에서 반복)

| 구성 요소 | 하는 일 | 사례 |
|---|---|---|
| 인터뷰 프롬프트 | 한 번에 질문 하나, 선택지 제시, 끝나면 파일에 기록 | Reed `spec.md` [C1], VelvetShark 32문항 [C2], McGuinness 50문항 [C3], Ray [C4], Vincent "질문 하나씩, 가능하면 객관식" [C7] |
| 비목표 / 안 만들 것 | 범위 폭발과 샛길 차단 | VelvetShark non-goals [C2], Ray "안 만들 것" [C4] |
| 결정 기록 | 왜 그렇게 정했는지 남김 | Ray Decision Log [C4], Brody 결정·변경 요약 [C8], redism `decisions.md` [C29] |
| 연구 문서 | 구현 전 기존 코드 이해를 파일로 검증 | Tane `research.md` [C5], Brody `.scratch/research/` [C8] |
| 계획 + 체크리스트 | 단계별 태스크, 진행 상태를 파일에 | Reed `todo.md` [C1], Tane plan 안 체크리스트 [C5], McLeod `docs/DEVELOPMENT_PLAN.md` [C9], Dzombak `IMPLEMENTATION_PLAN.md` 3~5단계 [C11] |
| 구현 금지 가드 | 계획 승인 전 코드 작성 차단 | Tane `don't implement yet` [C5], Brody [C8], Vincent ESC 두 번으로 되감기 [C7] |
| 세션 분리 | 인터뷰·검사·구현을 다른 컨텍스트에서 | VelvetShark 새 세션 구현 [C2], Ray 검사관 세션 [C4], Vincent 3세션(브레인스토밍·설계자·구현자) [C7], McLeod 계획 점검용 새 세션 [C9] |
| 짧은 규칙 파일 | CLAUDE.md/AGENTS.md는 규칙만, 길게 쓰지 않음 | Dzombak 번역 댓글 "100줄 미만이 최선" [C11], Reddit 752줄 → 약 40줄 [C20], McLeod 강조 남발 금지 [C9] |

McLeod는 체크리스트 원칙을 "The checklist is the state of the work."라는 한 문장으로 요약한다 [C9]. 진행 상태가 대화가 아니라 파일에 있으니 새 세션이 길을 잃지 않는다는 뜻이다.

### B2. 세션을 몇 개로 나누는가 (실측 숫자)
- **Jesse Vincent (2025-10-05)** [C7]: 3세션. 브레인스토밍(설계를 200~300단어 절로 나눠 절마다 확인) → 설계자 세션(계획 리뷰, 불일치 표시) → 구현자 세션(태스크 3~4개씩, 계획에서 벗어나지 말 것). 구현자는 `/compact` 대신 `/clear`. 설계자는 체크포인트로 되감아 앞 구현에 끌리지 않게 리뷰. PR 뒤 CodeRabbit 리뷰는 "이 리뷰어를 채용할지" 판정하는 접두 프롬프트로 걸러서 받음. 같은 코드베이스에서 프로젝트 3~4개 병렬.
- **Sam McLeod (2025-04 작성, 2026-07 개정)** [C9]: 계획이 작고 사용량이 약 40~50K 토큰 미만일 때만 같은 세션을 이어 감. 200K 모델은 약 160K, 1M 모델은 250~300K 아래로 유지.
- **Ray** [C4]: 인터뷰 세션 → `/clear` → 검사 세션(보고만) → 결정 반영 → 재검사.

### B3. 리뷰 피로를 줄인 장치
- 설계 절을 200~300단어로 끊고 절마다 확인 (Vincent) [C7]. 에이전트가 끝났다고 생각하면 긴 글을 쏟아내고 사람은 읽지 않게 된다는 관찰에서 나온 규칙.
- 계획에 주석 달기 → 같은 채팅에서 반영 → 변경 요약 받기 (Tane, Brody) [C5][C8]. 전체를 다시 읽지 않고 변경분만 본다.
- 검사 질문 3개를 정해 두고 "없음"이 나올 때까지 반복 (Ray) [C4].
- 리뷰는 새 세션에서, 내 코드라고 말하지 말고 "동료의 PR"로 제시, 새 버그가 안 나올 때까지 같은 리뷰 프롬프트 반복 (Nolan Lawson, 2025-12-22) [C10]. 내 코드라고 하면 에이전트가 아첨한다.

### B4. 반대 쪽 실천: 스펙을 거의 안 쓰는 사람 [C13]
- Peter Steinberger, "Just Talk To It"(2025-10). 6월까지는 SDD를 했지만, 큰 스펙을 쓰고 몇 시간 돌리는 방식을 옛 사고방식으로 본다. 새 세션이 파일을 다시 읽느라 작업마다 10분쯤 더 든다고 추정한다.
- 대신: Codex와 대화로 기능을 구체화. 까다로운 기능만 Codex가 스펙을 쓰고 다른 모델(GPT-5-Pro)이 리뷰, 쓸 만한 제안만 반영. UI는 모호하게 시작해 브라우저를 보며 반복.
- 책에 쓸 지점: "도구 없는 SDD"의 가장 가벼운 끝. 스펙을 쓸지 말지를 작업 난이도로 정한다는 점에서 9절 사다리의 바닥층과 맞물린다.

---

## C. 도구를 매일 쓸 때의 함정과 고친 방법

### 패턴 C1. 스펙 비대와 과잉 산출: 에이전트가 일 대신 글을 만든다
- 출현 예시:
  - Spec Kit 이슈 #75 (2025-09-08, 댓글 26개, 제목 "SpecKit creates the illusion of work") [C14]: 프로젝트 구조를 무시하고 파일을 새로 만들고, 기존 구조에 테스트 하나 추가하면 될 일에 쓸모없는 테스트 수백 개를 생성하고, 수 KB 지시문을 분석하느라 본질을 잃는다는 보고. 같은 스레드에서 한 사용자는 하루 종일 돌린 뒤 Claude를 다시 끌어오는 데 시간을 많이 썼고, 다른 사용자(비영어권이라고 밝힘)는 `tasks.md`에 적힌 버튼 문구와 다른 문구로 구현했다고 썼다.
  - Kiro (fikuri, 2025-09-13) [C22]: 초기 단계 기능에 단위·통합·E2E 테스트를 과잉 생성했고 다수 실패. 한 번에 2,000줄 이상 생성.
- 고친 방법:
  - 작은 변경에는 쓰지 않고, 큰 변경에서는 plan 단계를 따로 다듬은 뒤 넘김 (#75 댓글) [C14].
  - 기능이 확정 전이면 설계 스펙에서 테스트를 빼라고 스티어링 파일에 적고, 스티어링을 폴더·파일 단위로 범위 지정 (fikuri) [C22].
  - 스펙 크기 기준 (AWS Japan SA 稲田, 2026-06-02, 제조사 측 권고) [C23]: 요구사항 7~10개, 요구사항당 수용 기준 3~7개, 메인 태스크 10~14개(하위 포함 30~40개). 요구사항 15개 초과, 독립 화면·엔드포인트 여러 개, 한 문장 설명 불가 중 하나면 스펙을 나눈다. Quick Plan이 예상보다 많은 태스크를 만들면 Requirements-First로 바꿔 단계별로 검토. 버그픽스 스펙에는 "바꾸면 안 되는 동작"을 명시.

### 패턴 C2. 토큰과 사용 한도: 비용은 답변이 아니라 셋업에서 샌다
- 출현 예시:
  - Reddit r/GithubCopilot (u/boolean_autocrat, 2025-10 무렵 게시, 미러 스냅샷 2026-04-24) [C20]: Spec Kit + Copilot + Sonnet 4.6, Nuxt 4 + FastAPI 모노레포. `/plan`이나 `/implement`마다 파일 20개 이상을 읽고 grep을 여러 번 돌린 뒤에야 출력.
  - Kiro 무료 등급 50 요청을 2시간 세션 한 번에 소진, 왕복 20개 메시지면 한도 소진, 훅 실행마다 요청 1회 차감 (fikuri) [C22].
  - Medium(IT Chronicles) 비교: OpenSpec 91,729토큰 대 Spec Kit 181,040토큰(약 97% 증가), 원인으로 장황한 헌법과 다단계 절차 지목 [C21]. (원문은 403으로 읽지 못함. 검색 스니펫 기준, 단일 실험.)
- 고친 방법:
  - **항상 읽히는 지시 파일을 752줄 → 약 40줄로 줄이고** 세부 규칙은 해당 에이전트가 쓸 때만 읽는 파일로 옮김. 시스템·도구 컨텍스트가 33.3k → 21.7k 토큰, 세션당 약 11.6k(약 35%) 절감 [C20].
  - 안 통한 것: Serena MCP 코드 인덱싱. `/plan` 전체 실행에서 Serena 호출 0회. 저자 해석은 Spec Kit 에이전트가 심볼 조회가 아니라 파일 전체 맥락을 원한다는 것 [C20].
  - 계획은 다른 모델로, 구현만 Claude로 (Spec Kit #75 댓글: 토큰 절약을 위해 계획·스펙은 Gemini CLI, 구현은 Claude Code) [C14].

### 패턴 C3. 드리프트: 기능 001의 스펙을 기능 009가 낡게 만든다
- 출현 예시:
  - Spec Kit #620 (2025-09-27, 댓글 16개) [C15]: 기능 001 "이메일+비밀번호 로그인" 스펙이 몇 달 뒤 기능 009 "2단계 인증"으로 부분적으로 낡는다. 원본을 고칠지, 이력으로 두고 링크할지 묻는다. 댓글에서는 구현된 기능들을 "마일스톤 스펙"으로 압축하는 `/speckit.compact` 아이디어가 나오고, 한 사용자는 그것이 바로 OpenSpec의 핵심 기능이라고 답한다.
  - Spec Kit #4164 (2026-08-17) [C18]: 에이전트가 spec.md·plan.md·tasks.md에서 **비슷한 문구를 grep해** 관련 작업을 찾는다. 문구가 바뀌면("결제 시 청구" → "확인 모달 표시") 기존 요구사항을 못 찾고 새 요구사항을 추가한다. 같은 동작에 살아 있는 줄이 둘, 또는 서로 모순되는 줄이 둘 생긴다. `/speckit.analyze`는 컨텍스트에 올라온 것만 보므로 결과가 깨끗하게 나온다.
  - Spec Kit #4065 (2026-08-12) [C17]: `FR-###`, `T###`, `CHK###`를 촘촘한 연번으로 매기라는 템플릿 때문에 하나를 끼우면 뒤 번호가 다 밀리고, plan·checklist·PR 코멘트의 참조가 조용히 다른 항목을 가리킨다. 50개 태스크 파일의 10번째에 하나를 넣으면 40줄과 모든 의존 참조를 다시 써야 해 토큰도 두 번 든다. 제안자는 결국 프리셋 대신 개인 포크를 유지하기로 하고 PR을 닫았다.
  - OpenSpec #821 (2026-03-10) [C19]: `/opsx:apply` 뒤 로컬 테스트에서 버그를 찾으면 코드, `spec.md`, `design.md`, `tasks.md`를 고치라고 사람이 매번 따로 지시해야 한다. 원인이 구현인지 스펙인지 먼저 판정하는 `/opsx:repair`를 제안.
  - GeekNews 25949 댓글 (googol) [C27]: 처음엔 생산성이 뚜렷이 올랐지만, 모든 코드를 스펙으로 쓸 수 없고 직접 고칠 때마다 코드와 스펙을 함께 갱신해야 해서 오히려 생산성이 떨어졌다.
- 고친 방법:
  - 스펙은 오래 유지하지 않고 **변경 단위 계획으로만 쓴 뒤 PR에 첨부** (Brody) [C8]. 유지 비용 자체를 없앤다.
  - 사람이 손으로 관리하는 링크는 `parent` 하나만 두고 `children`은 스크립트로 계산해 어긋날 수 없게 함 (redism) [C29].
  - 버그를 고칠 때 "구현이 틀렸나, 스펙이 틀렸나"를 먼저 묻는 절차 (OpenSpec #821 제안) [C19].
  - 번호는 블록 단위로 미리 할당하고, 요구사항 목록은 grep 대신 스크립트가 관리하는 인벤토리로 (#4065, #4164 제안, 2026-11 기준 미채택) [C17][C18].

### 패턴 C4. "완료"라고 했지만 돌지 않는다
- 출현 예시:
  - GPTers "SDD 하네스" (엔라인) [C25]: 타입 체크·빌드·테스트만 통과하면 완료를 선언. 실제 부팅하면 DI 해석 실패, Logger 순환 참조, Prisma 어댑터 초기화 오류, 런타임 Provider 오류.
  - Nolan Lawson [C10]: SQL 최적화가 빨라졌다고 측정 없이 주장. 벤치마크와 `EXPLAIN`을 요구하자 오히려 느렸다.
- 고친 방법:
  - 완료 조건에 **앱 부팅 스모크 테스트**(`main.js` 실행, 기동 로그 확인)를 넣고, 모든 기능에 `*.spec.ts` 필수 [C25].
  - 리뷰어 에이전트의 쓰기 권한을 도구 수준에서 제거(검증자가 코드를 직접 고치던 문제) [C25].
  - 백엔드·프론트 충돌은 공유 타입을 먼저 정의하고 프론트는 계약 기준으로 Hook·Mock부터 [C25].
  - 성능 주장에는 벤치마크를 붙이게 하고 변형 3개를 같은 벤치마크로 비교 [C10].

### 패턴 C5. 질문했는데 고쳐 버린다
- Spec Kit #737 (2025-10-04) [C16]: `/implement` 중 "이 태스크 순서를 바꿔야 할까?"라고 물으면 답 대신 코드를 고친다. "스펙에서 놓친 게 있나?"라고 물으면 저자가 원하지 않는 항목까지 찾아 추가한다.
- 고친 방법: 질문할 때는 Copilot Ask 모드로 전환(댓글). 원작성자는 이것이 UX로 해결할 문제라고 반박. 도구 없는 쪽에서는 "보고만, 수정 금지" 검사 세션(Ray) [C4]과 `don't implement yet` 가드(Tane) [C5]가 같은 문제의 해법이다.

### 패턴 C6. 검수 단계를 만들어 놓고 안 쓴다
- GPTers (황금호랑이, 2026-08-05) [C26]: 반년 가까이 SpecKit으로 개발. 검수 스킬은 만들기 전용(`clarify`, `checklist`)과 만든 뒤 전용(`analyze`, `converge`)으로 나뉘는데, 앞의 둘을 거의 안 썼다. 반년간의 신뢰가 사실 검수 단계 위에 서 있었고 그 절반을 건너뛰고 있었다는 자각.
- 진단: AI 결과물 문제 8가지를 두 축으로 분류. 결과물(맥락 오염, 할루시네이션, 지시 무시, 평균 수렴) / 운영(컨텍스트 휘발성, 지식 사일로, 모델 종속성, 토큰 비용).
- 고친 방법: 맥락·결정·제약을 채팅이 아니라 스펙·계획·노트 파일로 남겨 Git으로 공유. 스펙 전 대화에서 "우리 규칙"을 먼저 명시해 평균적인 방식으로 끌려가지 않게 함. 검수 질문 8개와 재사용 프롬프트 3개(스펙 전 대화, 결과물 4종 검수, 세션 맥락 고정).
- 책에 쓸 지점: "검수할 수 있는 건 파일뿐"이라는 요지가 도구 없는 SDD 장의 결론 문장 후보.

### 패턴 C7. 스펙은 다음 할 일을 말해 주지 않는다
- GeekNews 35168 OpenGoal (tekart, 2026-10-11) [C30]: OpenSpec과 Superpowers로 명세 기반 개발을 했지만 "지금 무엇을 해야 하나"는 스펙에 없어서 Notion에 목표 문서를 따로 뒀고, 프로젝트 밖이라 관리가 번거로웠다.
- 고친 방법: `docs/`에 파일 하나가 질문 하나에 답하는 3파일. `ROADMAP.md`(전체에서 현재 위치), `CONTEXT.md`(이 프로젝트는 무엇인가), `GOAL.md`(지금 할 일). CLI·훅·MCP 없이 순수 마크다운.

---

## D. 한국 개발자 실사용 (보고서 7.9절에 없는 것만)

| 출처 | 날짜 | 형태 | 실사용 내용 | 근거 강도 |
|---|---|---|---|---|
| GeekNews 26907 댓글 [C6] | 2026-02-23 | Boris Tane 번역의 댓글 | pcj9024: 계획 파일을 저장소 안에 두고 실행 결과도 저장하게 했더니 컨텍스트가 잘 유지됨. naka98: 채팅으로만 협업하면 작업 분해·진척·결정 기록이 흐려짐. geekbini: 다른 CLI 에이전트에도 적용 가능 | 댓글 일화 |
| GeekNews 22425 댓글 [C11] | 2025-08-09 | Dzombak 번역의 댓글 | 2시간 들여 12단계 문서를 쓰고 구현을 맡겨 6~10시간 절약(자기 추정). CLAUDE.md 100줄 미만 유지가 최선, 세부는 하위 폴더로. TDD-Guard 훅으로 한 번에 테스트 하나만 통과시키게 강제. 반론: 회사 대형 웹앱에서는 실패했고, 문서 기반 방식이 중요한 것을 잊거나 없는 것을 지어냄 | 댓글 일화, 일부 번역된 HN 댓글 섞임 |
| GeekNews 25949 댓글 [C27] | 2026-01-19 | Osmani 번역(110점)의 댓글 | googol: 초기 생산성 상승 → 코드와 스펙 동시 갱신 부담으로 하락 (C3 패턴) | 댓글 일화 |
| GPTers, 엔라인 [C25] | 날짜 미표기(조회 시 "5달 전") | 자작 하네스 | `/plan → /spec → /task → /play → /review → /commits` 명령 + 백엔드·프론트·리뷰어 페르소나 + 규칙 스킬. 실패 6종과 해법 표 (C4 패턴). 정량 수치 없음, 본문의 "명령 8개"와 나열된 6개가 어긋남 | 1인 보고 |
| GPTers, 황금호랑이 [C26] | 2026-08-05 | 반년 SpecKit 회고 | 검수 단계 절반 건너뜀 자각, 문제 8분류, 재사용 프롬프트 3개 (C6 패턴) | 1인 보고, 수치 없음 |
| 달레(Dale Seo) 블로그 [C28] | 2026-03-21 | 튜토리얼 | 테스트·타입·CLAUDE.md TDD 순서를 스펙으로. 원화 할인 예시 (A9) | 튜토리얼, 실패 사례는 Böckeler 인용 |
| redism gist "claudie-workflow" [C29] | 2026-04-16 | 개인 SDD 프레임워크 설계 노트 (한국어) | 파일 11개: `decisions.md`, `constitution.md`, `rtm.md`(추적성), `l0-l4.md`(L0 비전 ~ L4 테스트), `data-dictionary.md`(새 세션의 용어 오해 방지) 등. 스펙 상태를 planned/done/discarded로 단순화. 목표는 자기 승인·검증 없는 완료 선언·리뷰 관문 건너뛰기를 **구조적으로** 막는 것(프롬프트만으로는 부족하다고 판단). 문서 자체에 결정 045와 어긋나는 낡은 문장이 남아 있음 = 드리프트의 실물 | 1차 산출물, 실험 단계 |
| `jh941213/my-cc-harness` [C32] | 2026-01-21 생성, 2026-10-28 갱신, 별 125 (2026-11-10 조회) | 한국어 플러그인 | 의도 → 설계 → 계획 → 구현 → 검증 → 리뷰 → 출시 → 학습 루프를 Claude Code·Codex·Copilot CLI에서 돌림. `spec`, `spec-verify` 스킬 포함 | 저장소 메타데이터만 확인 |
| GeekNews 35168 OpenGoal [C30] | 2026-10-11 | Show형 소개 | OpenSpec·Superpowers 사용 뒤 "다음 할 일" 공백 → 3파일 목표 관리 (C7 패턴) | 제작자 소개 |
| GeekNews 29552 Superpowers 사용기 [C31] | 2026-05-16 | 뉴스레터 요약 (24점) | 실사용 기록보다 기능 소개에 가까움. 댓글에서 Superpowers(TDD 강제) + Compound(매뉴얼 자동 갱신) 조합 추천, Ouroboros와 차이 질문 | 약함, 오프닝 소재로만 |

관찰(추론): 한국 실사용 글은 2026년 들어 "도구 하나 소개"에서 "자작 하네스·검수 회고"로 옮겨 가는 중이다. GPTers 두 글, redism, jh941213, OpenGoal이 모두 기성 도구 위에 자기 층을 얹거나 직접 만든 사례다. 대기업 기술 블로그(우아한형제들·토스·카카오·네이버·당근)의 SDD 전용 글은 이번에도 찾지 못했다. 보고서 7.9절의 같은 관찰과 일치한다.

---

## E. 논쟁점 (양쪽 보존)

### 논쟁 1: 스펙을 먼저 쓸까, 바로 대화할까
- 먼저 쓴다: Tane는 계획 승인 전에는 코드를 쓰게 하지 않는다 [C5]. Reed, Vincent, McGuinness, VelvetShark 모두 인터뷰 → 파일 → 새 세션 구현 [C1][C2][C3][C7].
- 바로 대화한다: Steinberger는 큰 스펙과 컨텍스트 리셋이 작업마다 10분쯤 더한다고 보고, 까다로운 기능에만 스펙을 쓴다 [C13]. VelvetShark도 요구가 분명하거나 작은 변경이면 인터뷰가 과하다고 인정한다 [C2].
- 접점: 양쪽 다 "작업 난이도로 스펙 여부를 정한다". 갈리는 지점은 기본값이다.

### 논쟁 2: 스펙을 계속 유지할까, 변경이 끝나면 버릴까
- 유지: Spec Kit #620의 참여자들은 하나로 합친 최신 스펙이 필요하다고 본다 [C15]. redism은 추적성(rtm)과 상태 이력을 설계한다 [C29].
- 버림 또는 PR에 첨부: Brody는 계획을 기능 전용으로 두고 PR에 접어 넣는다 [C8]. googol은 유지 비용이 생산성을 갉아먹었다고 말한다 [C27].
- 접점: 연구 문서(기존 시스템 설명)는 재사용하고 계획 문서는 일회용으로 쓰는 Brody의 분리가 중간 해법 후보다 [C8].

### 논쟁 3: 산문 스펙이냐, 실행 가능한 테스트냐
- 테스트가 스펙: 달레는 테스트와 타입을 스펙으로 삼는다 [C28]. Breunig의 whenwords는 테스트 750개가 사실상 계약이다 [C12].
- 산문도 필요: 같은 whenwords에서 외부 PR이 스펙 규칙을 어기는 **테스트**를 찾아냈다. 테스트도 틀린다는 반례다 [C12]. Ray의 결함 두 개(돌아가기 버튼 누락, 예시 날짜 오류)는 테스트 이전 단계의 산문 리뷰가 잡았다 [C4].

---

## F. 챕터 오프닝 후보 소재

| 소재 | 쓸 만한 장 | 출처 |
|---|---|---|
| 한 문장 SPEC.md가 질문 32개를 거쳐 157줄이 되고, 새 세션에서 5분 만에 동작 | 도구 없는 SDD 시작 장 | [C2] |
| 2019년에서 이번 달로 돌아오려면 ▶를 80번 넘게 눌러야 하는 스펙 | 스펙 리뷰 장 | [C4] |
| 예시 데이터의 날짜와 타임스탬프가 1년 어긋나 테스트·시드로 번질 뻔함 | 스펙 리뷰 장, 예시 작성법 | [C4] |
| "PUT이 아니라 PATCH" 한 줄 주석, 주석 1~6회 왕복 | 계획 리뷰 장 | [C5] |
| 지시 파일 752줄 → 40줄, 세션당 11.6k 토큰 절감 | 토큰 비용·규칙 파일 장 | [C20] |
| 로그인 스펙(001)을 2단계 인증 스펙(009)이 낡게 만듦 | 드리프트 장 | [C15] |
| 문구 하나 바꿨더니 같은 요구사항이 두 줄로 살아남음 | 드리프트 장, 도구 한계 | [C18] |
| 빌드·테스트는 통과했는데 부팅하자 DI 오류 | 검증·완료 조건 장 | [C25] |
| 반년 쓴 검수 단계의 절반을 건너뛰고 있었다 | 회고·운영 장 | [C26] |
| 코드 생성은 2시간, 안정화는 4일 | 기대치 조정 장 | [C24] |
| 코드 없이 스펙과 테스트만 배포한 라이브러리 | SDD 개념 장 | [C12] |

---

## 수집 한계

- 수집 건수: 32건 (블로그·튜토리얼 13, GitHub 이슈 6, GeekNews 토픽과 댓글 6, GPTers 2, Reddit 1, 개인 저장소·gist 2, 제조사 측 1, 검색 스니펫만 확인 1).
- 접근 실패: Medium 계열(Prezi Engineering 회고, Spec Kit 대 OpenSpec 동일 앱 비교, IT Chronicles 토큰 비교)은 403 또는 접근 거부로 본문을 읽지 못했다. C21 수치는 검색 스니펫 기준이다. i-boss "CCFM" 글(SPEC.md를 길게 쓰자 중간을 누락했다는 시행착오), LinkedIn "Spec 파일 3개부터" 글, velog `@link_dropper` `/spec` 명령 글은 403·504로 본문 미확인이라 본문에 넣지 않았다. forge.lthn.ai의 TASK_PROTOCOL(완료 표시 태스크 6개 이상이 실제로는 70~85%만 됐다는 2026-01 교훈)은 인증서 만료로 원문 확인 실패, 검색 요약만 있어 본문에서 뺐다.
- 언어 편중: 영어권 1인 블로그가 다수다. 한국어 1차 사례는 GPTers·GeekNews 댓글·개인 저장소에 몰려 있고, 회사 기술 블로그 사례는 없다. 일본은 보고서 7.11절이 충분해 새로 찾지 않았다.
- 근거 수준: 통제 비교는 하나도 없다. 수치는 모두 자기 보고다(VelvetShark 평균 질문 수, Dzombak 댓글 6~10시간 절약, OrangeLoops 6주 대 2주 등). 제조사 측 권고(C23 스펙 크기 기준)는 그렇게 표시했다.
- 신선도: GitHub 이슈 상태와 별 수는 2026-11-10 조회 기준이다. Spec Kit #4065·#4164의 제안은 조회 시점에 채택되지 않았다.

---

## 출처

- [C1] Harper Reed, "My LLM codegen workflow atm", 2025-02-16. https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/ (한국어판 https://harper.blog/ko/2025/02/16/my-llm-codegen-workflow-atm/)
- [C2] Radek Sienkiewicz (VelvetShark), "Stop prompting Claude Code - let it interview you", 2026-01-02. https://velvetshark.com/stop-prompting-claude-code-let-it-interview-you
- [C3] Charles McGuinness, "Stop Writing Specs for AI", 2025-12-29. https://mcguinnessai.substack.com/p/vibe-specing
- [C4] Ray, "30 Days of Vibe Coding, Day 8: Turning Ideas into a Spec", 2026-09-21. https://israynotarray.com/en/ai/2026/09/21/write-spec-md-with-claude-code/
- [C5] Boris Tane, "How I Use Claude Code", 2026-02-11. https://boristane.com/blog/how-i-use-claude-code/
- [C6] GeekNews 26907 "Claude Code 활용 방식: 계획과 실행의 분리" (C5 번역과 댓글), 2026-02-23. https://news.hada.io/topic?id=26907
- [C7] Jesse Vincent, "How I'm using coding agents in September, 2025", 2025-10-05. https://blog.fsck.com/2025/10/05/how-im-using-coding-agents-in-september-2025
- [C8] Hartley Brody, "Markdown is the new source code", 2026-03-09. https://blog.hartleybrody.com/markdown-research-planning/
- [C9] Sam McLeod, "My Plan, Document, Act, Review flow for Agentic Software Development", 2025-04-28 (2026-07 개정). https://smcleod.net/2025/04/my-plan-document-act-review-flow-for-agentic-software-development/
- [C10] Nolan Lawson, "How I use AI agents to write code", 2025-12-22. https://nolanlawson.com/2025/12/22/how-i-use-ai-agents-to-write-code/
- [C11] GeekNews 22425 "Claude Code로 좋은 결과 얻기" (Chris Dzombak 글 번역과 댓글), 2025-08-09. https://news.hada.io/topic?id=22425 / 원문 https://www.dzombak.com/blog/2025/08/getting-good-results-from-claude-code/
- [C12] Drew Breunig, "The Spec-Driven Development Triangle", 2026-03-04. https://www.dbreunig.com/2026/03/04/the-spec-driven-development-triangle.html / whenwords 소개 (Simon Willison, 2026-01-10) https://simonwillison.net/2026/Jan/10/a-software-library-with-no-code/
- [C13] Peter Steinberger, "Just Talk To It - the no-bs Way of Agentic Engineering", 2025-10 (Simon Willison 링크 2025-10-14). https://steipete.me/posts/just-talk-to-it
- [C14] github/spec-kit 이슈 #75 "SpecKit creates the illusion of work, generating a bunch of text", 2025-09-08. https://github.com/github/spec-kit/issues/75
- [C15] github/spec-kit 이슈 #620 "How to keep specs consistent and up-to-date with spec-kit?", 2025-09-27. https://github.com/github/spec-kit/issues/620
- [C16] github/spec-kit 이슈 #737 "spec-kit should answer questions, not 'fix' them.", 2025-10-04. https://github.com/github/spec-kit/issues/737
- [C17] github/spec-kit 이슈 #4065 "Stable, block-allocated identifiers (FR/SC/T/CHK)", 2026-08-12. https://github.com/github/spec-kit/issues/4065
- [C18] github/spec-kit 이슈 #4164 "Stop grep-based spec alignment, structured IDs + context packs", 2026-08-17. https://github.com/github/spec-kit/issues/4164
- [C19] Fission-AI/OpenSpec 이슈 #821 "Add /opsx:repair command", 2026-03-10. https://github.com/Fission-AI/OpenSpec/issues/821
- [C20] Reddit r/GithubCopilot, u/boolean_autocrat, "Spec-driven development with Spec-Kit is eating my tokens alive. What actually works?" (미러 스냅샷 2026-04-24, 게시는 그보다 199일 전). https://reddit.sentinel-team.org/posts/1sus656/snapshots/2026-04-24T23%3A20%3A04.257979Z
- [C21] IT Chronicles (Medium), "Spec Driven Development Is Wasting Tokens" (본문 미확인, 검색 스니펫). https://medium.com/it-chronicles/is-your-safe-choice-burning-your-budget-1cfddf8782e4
- [C22] fikuri, "Kiro: the good, bad and ugly part in my personal experience", 2025-09-13. https://dev.to/fikuri/kiro-the-good-bad-and-ugly-part-in-my-personal-experience-1neh
- [C23] 稲田 大陸 (AWS Japan SA), "進化し続ける Kiro の仕様駆動開発を一度立ち止まって整理する", builders.flash 2026-06-02 (제조사 측). https://aws.amazon.com/jp/builders-flash/202606/organize-kiro-sdd-evolution/
- [C24] Alejandro Wurm (OrangeLoops), "Spec-Driven Development with AI: A Spec Kit + Claude Code Case Study", 2026-05-19. https://orangeloops.com/2026/05/spec-driven-development-with-ai-a-spec-kit-claude-code-case-study/
- [C25] 엔라인 (GPTers), "Claude Code로 간단 'SDD 하네스' 만들기", 날짜 미표기. https://www.gpters.org/dev/post/creating-simple-sdd-harness-O0tS9jEK2cYtqmK
- [C26] 황금호랑이 (GPTers 23기 AI결과물검수 스터디), "[Claude Code + SpecKit] AI로 개발한 프로그램으로 지속 운영 가능할까?", 2026-08-05. https://www.gpters.org/nocode/post/can-program-developed-ai-UGafnfTxUVMDget
- [C27] GeekNews 25949 "AI 에이전트를 위한 좋은 스펙 작성법" (Addy Osmani 글 번역과 댓글), 2026-01-19. https://news.hada.io/topic?id=25949
- [C28] 달레(Dale Seo), "스펙 주도 개발: 바이브 코딩을 넘어 AI 에이전트와 일하는 법", 2026-03-21. https://daleseo.com/spec-driven-development/
- [C29] redism, "claudie-workflow Step 003 설계 v2" (gist), 2026-04-16. https://gist.github.com/redism/657cd03200eede5df4b2943569984d4d
- [C30] tekart, "OpenGoal: 마크다운만으로 AI 코딩 에이전트의 현재 목표를 관리하는 명세 기반 하네스", GeekNews 35168, 2026-10-11. https://news.hada.io/topic?id=35168
- [C31] pentaxzs, "Github 19만스타에 빛나는 Claude Code 플러그인 Superpowers 사용기", GeekNews 29552, 2026-05-16. https://news.hada.io/topic?id=29552
- [C32] jh941213/my-cc-harness (GitHub 저장소, 2026-01-21 생성, 2026-11-10 조회 별 125). https://github.com/jh941213/my-cc-harness
