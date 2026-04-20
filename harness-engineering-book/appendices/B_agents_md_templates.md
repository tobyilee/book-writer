# 부록 B — `AGENTS.md` 템플릿 5종

아래 다섯 템플릿은 3장 원칙의 실제 구현이다. **200줄 이하**, **GOAL / BUILD / TEST / STYLE / DON'T 5섹션**, **실패 로그 공간** — 이 셋을 공통으로 지킨다. 복사해서 자기 레포에 붙이되, 첫 엔트리는 **본인이 지난달 실제로 겪은 실패 한 건**으로 시작하는 편이 낫다. "완성된 채로 받는 `AGENTS.md`"는 3장이 경고한 "LLM이 쓴 `AGENTS.md`"와 결국 같은 자리에 선다.

각 템플릿은 `<ANGLE_BRACKET>` 자리에 자기 레포의 값을 채워 넣는다.

## 1. 소규모 Python 레포용 (≤80줄)

```markdown
# AGENTS.md

## GOAL
이 레포는 `<LIBRARY_NAME>`의 내부 도구 모음이다. **안정성 > 기능 확장**.
공개 API 하위 호환을 깨지 않는다.

## BUILD
- Python 3.11 이상. `uv sync`로 의존성 동기화.
- 로컬 실행: `uv run python -m <MODULE>`

## TEST
- `uv run pytest -q`로 전체 통과. 커버리지 목표 80%.
- 새 기능은 반드시 `tests/` 하위에 1건 이상의 assertion 있는 테스트 동반.
- `expect(True)`, `assert 1 == 1` 등 항진식 테스트 금지 (2026-01 fake test 30건 회귀).

## STYLE
- 포매터는 `ruff format`, 린터는 `ruff check`. CI가 강제.
- 타입 힌트 의무. `mypy --strict` 통과.
- 모듈 네이밍은 snake_case, 클래스는 PascalCase. 기본 관례는 LLM이 이미 안다 — 여기에 나열하지 않는다.

## DON'T
- 신규 라우트에 `/v2/` 프리픽스 금지. (PR #<NN>, 2026-03)
- `schema.prisma` 직접 수정 금지. 반드시 `prisma migrate`. (PR #<NN>, 2026-02)
- 외부 HTTP 요청에 `requests` 대신 `httpx`. timeout 없는 호출 금지. (incident 2026-01)

## 실패 로그 (append-only)
- <YYYY-MM-DD>: <한 줄 실패 요약> — PR #<NN>, 규칙 "<DON'T 항목>" 추가.
```

## 2. 모노레포 루트용 (≤150줄)

```markdown
# AGENTS.md (monorepo root)

## GOAL
이 모노레포는 `<N>`개 서비스의 공용 인프라다. **하위 패키지의 국소 규칙을 존중**하고,
루트 규칙은 "모든 패키지가 따라야 하는 최소 공통분모"만 남긴다.

> 조율 규칙: 편집 중인 파일에 **가장 가까운 `AGENTS.md`**가 이긴다.
> 국소 규칙이 이 루트 규칙을 오버라이드할 수 있다.

## BUILD
- 루트 워크스페이스: `pnpm install` 또는 `bun install`.
- 패키지 빌드: `pnpm --filter <PKG> build`
- 전체 빌드: `pnpm -r build` (CI에서만 권장)

## TEST
- 패키지별 `pnpm --filter <PKG> test`.
- 루트에서 전체: `pnpm -r test` (로컬 2~3분, CI 5~10분).
- `required-tests.txt` 목록은 어떤 하위 패키지도 삭제·수정 금지.

## STYLE
- Prettier + ESLint. 커밋 훅(`lefthook.yml`)이 강제.
- 커밋 메시지: Conventional Commits. 스코프는 패키지명.
- 브랜치 네이밍: `feat/<scope>-<topic>`, `fix/<scope>-<topic>`.

## DON'T
- 루트에서 단일 패키지만의 dep을 설치하지 말 것 — 항상 `--filter <PKG>`.
- 공용 유틸을 `packages/shared/` 바깥에 복제하지 말 것. (PR #<NN>)
- 서비스 간 직접 import 금지. 공용 타입은 `packages/contracts/` 경유. (incident 2026-02)
- `.github/workflows/*.yml`을 에이전트가 직접 수정하지 말 것. PR 리뷰 필요.

## 소유자
- `apps/web/**` — @team-frontend
- `apps/api/**` — @team-backend
- `packages/contracts/**` — @team-platform
- 이 파일 자체 — @team-platform (PR 기반 변경만)

## 실패 로그 (append-only)
- <YYYY-MM-DD>: <요약> — PR #<NN>
```

## 3. 모노레포 하위 패키지용 (≤80줄)

```markdown
# AGENTS.md (apps/api)

## GOAL
이 서비스는 외부 파트너와의 **하위 호환**을 최우선한다. 성능보다 안정성.
루트 `AGENTS.md`의 모든 원칙을 상속하되, 이 파일의 RULE이 우선한다.

## BUILD
- `pnpm --filter @co/api dev`로 로컬 실행.
- 환경변수는 `.env.example`을 복사해 채운다. 비밀은 1Password CLI 경유.

## TEST
- `pnpm --filter @co/api test`
- 계약 테스트: `pnpm --filter @co/api test:contract` (공용 스키마 변경 시 필수).

## STYLE
- 라우트 파일은 `src/routes/**/*.ts`, 파일명은 kebab-case.
- 응답 타입은 반드시 `packages/contracts/`의 Zod 스키마에서 파생.

## DON'T
- 신규 라우트에 `/v2/` 프리픽스 금지. `/v3/` 또는 리소스명. (PR #1203, 2026-03)
- `POST`에 `idempotency-key` 체크 없이 배포 금지. (incident 2026-02)
- DB 스키마 직접 수정 금지 — `prisma migrate`만. (PR #1187)

## 실패 로그 (append-only)
- 2026-03-12: `/v2/orders` 임의 생성으로 파트너 연동 실패 — PR #1203, 규칙 추가.
- 2026-02-28: schema.prisma 직접 수정 → 프로덕션 동기화 실패 — PR #1187.
```

## 4. 프런트엔드(React/Next.js)용

```markdown
# AGENTS.md (apps/web)

## GOAL
이 앱은 `<PRODUCT_NAME>`의 고객 대면 UI다. **Core Web Vitals**를 예산으로 관리한다.
접근성(WCAG 2.1 AA)은 타협 대상이 아니다.

## BUILD
- `pnpm --filter @co/web dev` (Next.js 14 App Router)
- 프리뷰: Vercel Preview URL이 PR마다 자동 생성.

## TEST
- 유닛: `pnpm --filter @co/web test` (Vitest + RTL)
- E2E: `pnpm --filter @co/web test:e2e` (Playwright)
- 성능 예산: Lighthouse CI, LCP <2.5s, CLS <0.1. CI에서 회귀 시 fail.

## STYLE
- Tailwind + shadcn/ui. 임의 색상 금지, 디자인 토큰만.
- 컴포넌트는 서버 컴포넌트 default. 클라이언트 컴포넌트는 `"use client"` 주석.
- 폼은 react-hook-form + zod. 커스텀 validation 금지.

## DON'T
- `any` 타입 금지 (ESLint error). (incident 2026-02: 타입 우회로 프로덕션 NPE)
- `getServerSideProps` 신규 사용 금지 — App Router `async` 컴포넌트. (deprecation 2026-01)
- `localStorage`에 토큰 저장 금지. (보안 감사 2026-01)
- 이미지는 `next/image`만. `<img>` 태그 직접 사용 금지.
- `aria-label` 누락 버튼 배포 금지. CI a11y 스캔에서 잡힘.

## 실패 로그 (append-only)
- 2026-02-18: `any` 우회 → 런타임 NPE — PR #832, ESLint 규칙 `error`로 격상.
```

## 5. 데이터 파이프라인용

```markdown
# AGENTS.md (data/pipelines)

## GOAL
이 디렉터리는 `<WAREHOUSE>`로 향하는 ETL 파이프라인이다.
**재실행 가능성(idempotency)**과 **원본 보존**이 최우선. 파괴적 변환 금지.

## BUILD
- 오케스트레이션: Airflow 2.9. DAG 파일은 `dags/` 하위.
- 로컬 실행: `airflow dags test <DAG_ID> <RUN_DATE>`
- dbt 모델: `dbt run --select <MODEL>`

## TEST
- dbt 테스트: `dbt test`로 not_null·unique·relationships 자동 검증.
- Great Expectations 계약 테스트: `great_expectations checkpoint run <NAME>`.
- 샘플 데이터로 드라이런. 실 warehouse 쓰기는 CI의 승인된 job에서만.

## STYLE
- DAG는 한 파일당 한 개. 파일명은 DAG_ID와 동일.
- 태스크 이름은 snake_case, DAG ID는 `<domain>_<entity>_<frequency>` (예: `sales_orders_daily`).
- SQL은 dbt 모델 안에만. DAG 파일에 raw SQL 박지 말 것.

## DON'T
- `DROP TABLE`·`TRUNCATE`를 DAG 안에 박지 말 것. staging → swap 패턴만. (incident 2026-01 데이터 손실)
- warehouse에 직접 쓰는 Python operator 금지. dbt·Great Expectations 경유.
- PII 컬럼을 암호화 없이 복사하지 말 것. `columns:pii:true` 태그 누락 시 CI fail.
- `schedule_interval=None`인 DAG를 프로덕션에 병합 금지. (운영 혼선 방지)

## 실패 로그 (append-only)
- 2026-01-22: DROP TABLE 포함 DAG 배포 → 3시간분 데이터 손실 — DAG 템플릿에서 해당 라인 금지.
- 2025-12-10: PII 컬럼 무태그 → 감사 지적 — CI 스캐너 추가.
```

---

다섯 템플릿의 공통 형식을 기억해두자. **GOAL 한 줄, BUILD 한 줄, TEST 한 줄, STYLE 한 줄, DON'T 항목마다 실패 사례 PR/날짜.** 형식이 단순해야 다음 사람이 새 실패를 붙여 넣는다. 복잡한 형식은 얼어붙는다.
