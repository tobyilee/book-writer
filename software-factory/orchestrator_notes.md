# 오케스트레이터 메모 — 편집자 전달용 교차 묶음 정합 항목

## 사실 검수(1~3장)에서 나온 통권 정정 — 전 장에 적용

- Opus 5.5의 680,000줄 마이그레이션은 **초기 테스터 한 명**의 사례다(Anthropic 자체 성과 아님).
- StrongDM 자료는 팀 결성 계기가 된 모델 개선을 설명한다(모델명은 책에 쓰지 않음). "모델에 대해 말하지 않는다"고 쓰지 않는다 — 말하지 않는 것은 지금 팩토리가 무엇으로 돌아가는지다.
- Yegge 8단계는 모두 확인됨(2~4단계 포함). 계획·레퍼런스 §2.1(2)의 "2~4 미확인" 서술은 틀렸다. 어느 장이든 "미확인"이라 쓰면 고친다. 2장 대응표: 책의 2단계 = Yegge Stage 2, 3단계 = Stage 3~6.
- 모델 ID: `claude-opus-5-5`, `claude-fable-5-1`, `gpt-6-sol`, `gpt-6-luna`.
- (13~15장 검수) OpenAI 하네스 엔지니어링(Lopopolo, 2026-02-11): "셋으로 시작해 일곱으로 늘어난 작은 팀". 레퍼런스 §3.2·`research/web.md` 자료 9의 "7명"은 틀린 표현 — 어느 장·서문·에필로그에서 인용하든 정정된 표현을 쓴다. 0줄·약 100만 줄·약 1,500 PR은 맞음.
- Anthropic 자율성 연구의 "에이전트 자기 중단이 사람 개입의 2배 이상"은 **가장 복잡한 작업에서**라는 한정이 붙는다.
- 인간 사보타주 연구: "참가자의 94%"가 놓쳤다(사보타주의 94% 아님).
- (9~12장 검수) PromptPwnd "포천 500 최소 5곳"은 **Aikido 자체 발표**다("2차 보도" 아님) — 참고문헌·레퍼런스 인용 시 Aikido 출처로.
- 참고문헌에 추가: 파이낸셜뉴스 2026-09-09 (AI월드 2026, 이건복 MS 솔루션 어드바이저 발언) https://www.fnnews.com/news/202609091826242004 — `research/*.md`에 없는 신규 출처.
- vibe-coded 앱 감사(arXiv 2606.23130)의 65.77%는 취약점 1,186건 중 비율.
- (4~8장 검수) **`wrangler preview`가 만드는 것은 Workers "Preview"다 — "Version URL"이 아니다.** Cloudflare 문서는 PR 테스트에 Version URL을 쓰지 말라고 한다(Wrangler 4.135.0+). 8장은 고쳐졌다. **9장·부록 A·부록 B·기타 장에 "Version URL"로 쓴 곳을 모두 "Preview(프리뷰)"로 고친다.** (계획·레퍼런스 W47이 두 기능을 섞었다.)
- **`gather` 시크릿 목록에 `CLOUDFLARE_ACCOUNT_ID` 추가**, `factory-build.yml`에 `id-token: write` 추가(claude-code-action의 GitHub App 인증), AWS OIDC 배포 잡도 `id-token: write`. 9장 권한 지도가 이와 맞아야 한다.
- 8장 gh-aw 계획 워크플로에 라벨 필터 `names: ["factory:ready"]` 추가됨.
- 8장: 프리뷰 잡은 `needs: ci`(CI 뒤 실행) — 다른 장이 "CI와 병렬"이라 쓰면 맞춘다.
- Next.js on Workers: Cloudflare는 현재 vinext 권장, OpenNext 어댑터도 문서화(2026-09 기준).
- 7장 헌법 예시·명세에도 "결제·환불"이 있다 → 위 결제 항목과 함께 `gather` 도메인에 맞게 통일.

저술 묶음이 병렬로 쓰였기 때문에 생긴 정합 확인 항목. editor가 통합 시 처리한다.

## 묶음 1 (1~3장) 저술가 보고

1. `gather`는 2장에서 처음 소개된다(가상 예제라는 한 문단 + `api/`·`web/`·`jobs/` 구조). 4장이 다시 전체 소개하면 한쪽을 줄인다.
2. 3장이 `gather`의 첫 역할 배정을 정한다 — 설계자 Claude Fable 5.1, 빌더 Claude Opus 5.5 + Claude Code, 리뷰어 GPT-6 Sol + Codex, 워커 GPT-6 Luna·Muse Spark·Grok. 규칙: 빌더와 리뷰어는 항상 다른 벤더. 8장 교차 리뷰 잡이 이와 맞는지 확인.
3. 3장의 `roles.yml`은 일반 예시(‘gather’ 파일 아님). 8장이 워크플로에 `--model`을 직접 쓰더라도 충돌 아님.
4. 1~3장은 `##` 절 + `###` 소절 구조. 2장 자기 점검 질문은 `###` 없는 `##`. 다른 묶음의 헤딩 구조와 통일 필요.
5. 3장 산문 ~8,900자(계획 7,500) — 중앙값 밴드 안이므로 유지 결정.

## 묶음 4 (13~15장·부록) 저술가 보고

1. **`gather`의 결제:** 13·14장이 "결제·환불"을 상시 사람 영역으로 쓴다(계획 10·14장 기준). 계획의 `gather` 명세(모임·예약·리마인더)에는 결제가 없다. 1~12장이 결제를 소개하지 않으면 "권한·개인정보"로 바꾸거나 앞 장에 결제를 한 줄 도입.
2. **13장 신규 이름:** 라벨 `factory:veto`·`factory:needs-decision`, 파일 `docs/decisions.md`(13장)·`docs/lighting-map.md`(14장). 8장이 정의한 `factory:*` 라벨 체계와 일치 확인.
3. **13장 Actions YAML:** `jobs`·`runs-on`·`steps` 키, `--max-turns 10`은 저술가 선택값.
4. **교차 참조:** 13~15장은 계획상 소재 배치(5장 외부 상태, 6장 중단 출구, 8장 `STOP_IF`·Auto-fix, 11장 하네스 오너, 12장 tokenmaxxing)에 기대고 있다. 최종 장에 실제로 있는지 확인.
5. **Mermaid:** 저술 환경에 `mmdc`가 없어 미렌더. 빌드 단계 확인 대상.

## 묶음 3 (9~12장) 저술가 보고

1. **8장 의존:** 9장은 8장이 다음을 세웠다고 가정한다 — `factory:ready` 라벨과 계획 코멘트를 다는 계획 에이전트, 8장 끝의 최소 보안선 언급, Cloudflare Version URL 프리뷰·AWS OIDC 배포, addyosmani/factory의 스킬 정본 + Codex 어댑터 구조. 8장 final과 대조해 맞춘다.
2. **`gather` 신규 이름:** `gather-harness`(11장, 팀 공유 하네스), `gather-platform`(12장, 중앙 Caller–Executor 저장소 — 12장이 둘의 차이를 설명). 10장이 3부 시작에서 8인 팀과 저장소 3분할을 도입한다.
3. **용어 표기 추가 후보:** "lethal trifecta(치명적 삼박자)" → 이후 "치명적 삼박자"(14장에서도 통일). Parasuraman & Riley는 계획대로 오용(misuse)·불용(disuse)·남용(abuse). 토스는 블로그 제목을 따라 "저점 높이기"(계획은 "저점 올리기") — 하나로 통일.
4. 9장 산문 ~10,050자(중앙값 118%) — 플래그 밖, 필요 시 editor가 다듬음.
5. 대조 확인된 공유 이름: `gather-scenarios`, `reservation-cancel.md`, 사람 게이트 1/2, 역할 명세 소유자·당직자.

## 묶음 2 (4~8장) 저술가 보고 — `gather` 정전 이름 목록 (9·13·14장 대조 기준)

- **헤딩 레벨 불일치:** 4~8장은 `#` 장 제목 + `##` 절. 1~3장은 `##` 절 + `###` 소절. 통권 한 체계로 통일.
- **사람 게이트 3개:** 게이트 1 = 계획/명세 승인(`factory:approved`), 게이트 2 = 머지, 게이트 3 = `api` 프로덕션 환경 승인. 13·14장은 새 게이트를 만들지 말고 이 셋을 재사용.
- **에이전트 지시:** `AGENTS.md` 정본(레포 지도·명령·모듈 경계·하지 말 것·작업 방식·더 읽을 것; 6장 "완료 정의 — 머지 가능" 7항목·"멈추는 법"(`BLOCKED: 이유`), 7장 "명세" 규칙, 8장 `## Code Review Rules`). `CLAUDE.md`는 얇게 `AGENTS.md`를 가리킴. 스킬 `.claude/skills/kotlin-api-conventions/SKILL.md` + Codex 어댑터 `.agents/skills/kotlin-api-conventions/`(8장).
- **훅:** `.claude/settings.json` — PostToolUse `scripts/hooks/after-edit.sh`, PreToolUse `scripts/hooks/guard-paths.sh`(4장: 적용된 마이그레이션 보호; 6장 PROTECTED 목록: `api/src/acceptanceTest/`, `web/e2e/acceptance/`, `jobs/tests/acceptance/`, `.github/workflows/`, `scripts/hooks/`, `scripts/ci/`, `.claude/settings.json`; 7장: 인수 테스트 경로는 `spec/` 브랜치에서만 쓰기 허용).
- **스크립트:** `scripts/dev/check.sh api|web|jobs|all`, `scripts/dev/init.sh [--with-app]`, `scripts/factory/loop.sh`(+ `scripts/factory/prompts/next-item.md`; 종료 코드 0 완료·2 최대 반복·3 무진전 2회·4 예산 초과·5 BLOCKED), `scripts/factory/verify.sh`(일회용 워크트리에서 `codex exec`, PASS/FAIL/CANNOT_VERIFY), `scripts/ci/check-protected-paths.sh`(`BASE_REF`, 7장에서 명세 승인 태그). 로그 `.factory/logs/`, `.factory/costs.log`.
- **문서:** `docs/architecture.md`, `docs/conventions.md`, `docs/metrics.md`, `docs/plans/_template.md`·`reservation-cancel.md`·`waitlist.md`·`cancel-deadline.md`, `docs/progress/waitlist.md`, `docs/specs/reservation-cancel.md`.
- **테스트/패키지:** `api/src/test/kotlin/gather/waitlist/WaitlistPromotionTest.kt`, `WaitlistPropertyTest.kt`; 패키지 `gather.reservation`·`gather.gathering`·`gather.member`·`gather.waitlist`.
- **워크플로:** `ci.yml`(→ `holdout.yml`), `holdout.yml`(`workflow_call`, 입력 `base_url`, 시크릿 `SCENARIOS_DEPLOY_KEY`), `factory-plan.md`→`.lock.yml`(gh-aw, `read-all` + safe-outputs `add-comment`), `factory-build.yml`(claude-code-action), `factory-pr.yml`(ci → review(`contents: read`) → 코멘트 잡(`pull-requests: write`) → 수정 1회 → `factory:reviewed`; 병렬로 preview(`wrangler preview`) → holdout + Playwright E2E → 요약 코멘트; PR 닫힘 시 `wrangler preview delete`), `deploy.yml`(web → Cloudflare, api·jobs → AWS OIDC, 프로덕션 환경 승인 = 게이트 3).
- **비공개 저장소 `gather-scenarios`:** `run.sh --base-url … --summary-only`, 가짜 알림 제공자 서버(디지털 트윈).
- **라벨·브랜치·태그:** `factory:ready` → 계획 코멘트 → `factory:approved`(게이트 1) → `factory:building` → draft PR 또는 `factory:blocked` → `factory:reviewed` → 머지(게이트 2). 브랜치 `factory/issue-N`, `spec/<name>`, `feat/*`. 태그 `spec-approved/<name>`. 8장 예시 이슈 #41, #42(blocked), #43.
- **시크릿:** `ANTHROPIC_API_KEY`, `CODEX_API_KEY`, `CLOUDFLARE_API_TOKEN`, `SCENARIOS_DEPLOY_KEY`. 빌드 잡은 이슈 번호만 프롬프트에 넘기고 나머지는 9장으로 미룸.
- **13장 신규 라벨 대조:** `factory:veto`·`factory:needs-decision`은 위 라벨 체계의 확장으로 자연스러운지 확인하고, 필요하면 8장 흐름과 연결하는 한 줄을 둔다.
- **결제:** 위 `gather` 명세·예시 어디에도 결제가 없다 → 13·14장의 "결제·환불"은 교체(예: "권한·개인정보" 또는 "예약 취소 마감·환불 규정" 중 `gather` 도메인에 이미 있는 것)하거나 앞 장에 도입.
