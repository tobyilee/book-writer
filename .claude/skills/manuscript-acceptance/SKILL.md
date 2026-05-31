---
name: manuscript-acceptance
description: Whole-book acceptance gate run by a fresh-context reviewer before EPUB build (Phase 4.5). Cross-reads the integrated manuscript against the plan and escalation logs, scans for forbidden leftover markers, checks terminology/cross-reference/promise integrity, and emits {slug}/05_acceptance.md with per-criterion PASS/BLOCK + routing. Genre-agnostic; complements (does not replace) per-chapter fact/continuity loops. Triggers on "수락 검수", "통권 검수", "manuscript acceptance", "최종 통과 게이트".
---

# Manuscript Acceptance

통합 원고(`04_manuscript.md`)가 표지·EPUB 빌드(Phase 5)로 넘어가기 전, **책 전체**를 한 번에 검수하는 마지막 게이트다. editor가 쓴 원고를 editor 본인이 승인하면 self-approve가 되므로, 이 절차는 **fresh context**(`manuscript-reviewer`)가 수행한다. 챕터 단위 fact/continuity 루프를 다시 돌리지 않고, **통권 단위 문제와 잔여 미결**만 본다.

> **장르 무관.** tech-book·narrative·practical·essay 모두에서 Phase 4.5로 실행된다. 장르마다 존재하는 로그가 다르므로(essay엔 factcheck/continuity 로그가 없을 수 있음), 없는 로그가 대상인 기준은 N/A PASS로 처리하고 이유를 한 줄 남긴다.

## 입력

- `{slug}/04_manuscript.md` — 검수 대상 통합 원고
- `{slug}/02_plan.md` — 챕터 완비·약속 대조 기준
- `{slug}/factcheck_log.md` — (tech-book) (c) 대조
- `{slug}/continuity_log.md` — (narrative) 잔여 모순·미회수 복선 대조
- `{slug}/style_log.md` — style 잔여 이슈·미합의 대조
- `{slug}/book_manifest.json` — `logline`/`description` 약속 대조
- `{slug}/length_report.md` — (있으면) 분량 균형 (a)

## 수락 기준 체크리스트 (실행형)

| ID | 기준 | 어떻게 확인하나 | 판정 BLOCK 시 |
|----|------|----------------|--------------|
| (a) | 챕터 완비·분량 균형 | `02_plan.md`의 챕터 목록 ↔ 원고의 `# N장` 헤딩을 1:1 대조. 누락·초과 확인. `length_report.md`(있으면)로 챕터 분량 편차 점검(한 장이 평균의 ½ 미만/2배 초과면 플래그) | 해당 챕터 → Phase 4 (최대 1라운드) |
| (b) | 미해소 마커 0건 | 원고 전체를 grep으로 훑어 금지 마커 검출 (아래 절차) | **HARD STOP** → 사용자 |
| (c) | 사실 미결 해소 | `factcheck_log.md`에서 "미해소"/"재확인"/`❌`/`🕒` 잔여 항목, 특히 suspect citation(arXiv ID·인용·URL)이 닫혔거나 사용자 승인됐는지 확인 | **HARD STOP** → 사용자 |
| (d) | 용어 통일 + 챕터 간 변주 | 핵심 용어의 표기 흔들림(영/한, 축약/풀) 통권 점검. 오프닝·클로징·말버릇(tic)이 챕터마다 같은 틀로 반복되는지 점검 | 해당 챕터 → Phase 4 (최대 1라운드) |
| (e) | 상호 참조 무결성 | "앞서 N장에서 ~"/"N장에서 다룬" 류 콜백을 모두 찾아, 실제 그 장에 그 내용이 있는지 대조. 끊긴·잘못된 번호 검출 | 해당 챕터 → Phase 4 (최대 1라운드) |
| (f) | 약속 이행 | 매니페스트 `logline`/`description`이 약속한 범위·대상·핵심 약속을 원고가 실제로 다루는가 | editor 보강 / 미달 시 사용자 |
| (g) | front/back matter 완비 | 서문·목차·콜로폰(`## 판권`)·에필로그·(tech-book/essay면) 참고문헌이 모두 있는가 | editor 보강 |

## 절차

1. **준비** — `genre`와 슬러그를 확인하고, 위 입력 중 존재하는 로그를 파악한다. 없는 로그가 대상인 기준은 N/A로 미리 표시.
2. **마커 스캔 (b)** — 원고에서 금지 마커를 grep한다. 0건이어야 한다.
   ```bash
   grep -nE "\(사실 확인 필요\)|\[리서치 공백\]|\[미완성\]" {slug}/04_manuscript.md
   ```
   - 한 건이라도 나오면 (b) **BLOCK = HARD STOP**. 줄 번호와 원문을 `05_acceptance.md`에 기록.
3. **챕터 완비·분량 (a)** — 플랜의 챕터 목록과 원고 `# N장` 헤딩을 대조.
   ```bash
   grep -nE "^# [0-9]+장" {slug}/04_manuscript.md
   ```
   - 누락/초과 챕터가 있으면 (a) BLOCK. `length_report.md`(있으면)로 분량 편차 플래그.
4. **상호 참조 (e)** — 콜백 표현을 모두 뽑아 가리키는 장이 맞는지 확인.
   ```bash
   grep -nE "앞서 [0-9]+장|[0-9]+장에서 (다룬|살펴본|본)" {slug}/04_manuscript.md
   ```
   - 잘못된 번호·끊긴 참조는 (e) BLOCK.
5. **에스컬레이션 로그 교차 읽기 (c)** — `factcheck_log.md`(+ narrative면 `continuity_log.md`, 공통으로 `style_log.md`)에서 잔여 미결을 찾는다.
   ```bash
   grep -nE "미해소|재확인|❌|🕒" {slug}/factcheck_log.md
   ```
   - **재검증을 새로 하지 않는다.** 챕터 루프가 "해소"로 닫은 항목은 신뢰하고, "미해소/재확인"으로 남긴 것만 본다. suspect citation(arXiv ID·인용·URL)은 특히 닫혔는지 확인 — 미검증이면 (c) **HARD STOP**.
   - `continuity_log.md`의 "미해소(모순 위험)"/미회수 복선, `style_log.md`의 미합의 잔여는 통권 영향이 있으면 (d)나 (e)로 흡수해 판정.
6. **용어·변주 (d)** — 통권을 훑어 핵심 용어 표기 흔들림, 오프닝/클로징/tic의 단조 반복을 점검.
7. **약속·부속 자료 (f)(g)** — 매니페스트 `logline`/`description` 대조, 서문·목차·콜로폰·에필로그·참고문헌 존재 확인.
8. **기록 + 평결** — `05_acceptance.md`에 기준 표 + 평결 + 차단 항목별 조치를 쓰고, 라우팅 메시지를 `SendMessage`로 보낸다.

## 라우팅 / 종료 규칙

- **(a)(d)(e) BLOCK** → 문제 챕터를 Phase 4로 되돌린다. **최대 1 라운드**. 1라운드 후에도 미해소면 잔여 항목을 명시하고 오케스트레이터 보고(조건부 통과는 사용자 판단).
- **(b)(c) BLOCK** → **HARD STOP**. Phase 5 진입 금지, 사용자 에스컬레이션. 미해소 마커·사실 오류·suspect citation은 저술가 재량으로 덮지 않는다.
- **(f)(g) BLOCK** → editor 보강 요청. (g)는 보통 1라운드로 닫힘. (f) 본질적 미달은 사용자 판단.
- **전 항목 PASS** → ACCEPT. 오케스트레이터가 Phase 5로 진행.
- 사용자가 (b)(c)를 명시 승인하면 그 사실과 근거를 기록하고 통과 (덮은 게 아니라 사용자 결정임을 명문화).

## 출력 형식

`{slug}/05_acceptance.md`:

```markdown
# 수락 검수: {책 제목}

<!-- 검수: {날짜} · 라운드 {N} · 검수자: manuscript-reviewer (fresh context) -->

## 기준 판정

| ID | 기준 | 판정 | 근거 / 차단 항목별 조치 |
|----|------|------|------------------------|
| (a) | 챕터 완비·분량 균형 | PASS | 플랜 8장 = 원고 8장, 분량 편차 OK |
| (b) | 미해소 마커 0건 | PASS | grep 0건 |
| (c) | 사실 미결 해소 | PASS | factcheck_log 미해소 0건 |
| (d) | 용어 통일 + 챕터 간 변주 | PASS | ... |
| (e) | 상호 참조 무결성 | PASS | 콜백 6건 전부 정합 |
| (f) | 약속 이행 | PASS | logline 범위 충족 |
| (g) | front/back matter 완비 | PASS | 서문·목차·판권·에필로그·참고문헌 확인 |

## 평결

ACCEPT

## 차단 항목별 조치

- (없음)
```

## 작업 원칙

- **fresh context:** editor의 의도를 추측해 봐주지 않는다. 원고·로그가 보여주는 것만으로 판정.
- **보완이지 대체가 아니다:** 챕터 fact/continuity 판정을 다시 돌리지 않는다. 잔여 미결과 통권 단위 문제만.
- **근거 명기:** 모든 BLOCK에 grep 결과·로그 섹션·줄 번호 같은 구체 근거. "느낌"으로 차단하지 않는다.
- **HARD STOP 양보 없음:** (b)(c)는 사용자 승인 없이 통과시키지 않는다. 빌드를 막는 것이 책 신뢰를 지키는 것이다.
- **월권 금지:** 직접 고치지 않는다. 판정하고 라우팅한다.

## 재검수 시

- `05_acceptance.md` 존재 + 재검수 → 새 라운드 append, 이전 차단 항목 해소 여부 먼저 확인 후 새/잔여 항목만 판정
- 일부 챕터만 재작업 → 영향받은 (a)(d)(e)만 재판정, 나머지 이전 PASS 유지
