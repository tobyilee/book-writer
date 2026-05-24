---
name: continuity-check
description: Maintain a story bible and check narrative chapter drafts for continuity — character facts (appearance, voice, motive), relationships, world rules, timeline, and planted setups (복선). Seeds {slug}/story_bible.md from the plan, flags contradictions, and tracks setup→payoff. Use when keeping a novel consistent across chapters, building a story bible, validating character voice, or tracking 복선. Triggers on "연속성 확인", "스토리 바이블", "복선 추적", "캐릭터 일관성", "continuity check", "story bible".
---

# Continuity Check

소설·서사물을 챕터를 건너뛰며 일관되게 유지한다. 인물·관계·세계관·타임라인·복선을 `story_bible.md`라는 단일 정전(canon)으로 잡고, 각 챕터를 그에 대조한다. 문체가 아니라 **연속성**만 본다.

> **narrative 장르 전용.** `genre`(오케스트레이터 → `{slug}/book_manifest.json`)가 narrative가 아니면 오케스트레이터가 이 단계를 생략한다.

## 절차

1. **활성 장르 확인** — narrative가 아니면 중단
2. **시드** — `story_bible.md`가 없으면 `02_plan.md`에서 인물·설정·타임라인·복선을 뽑아 초기화 (부족하면 1장 초안에서 캐논 추출)
3. **추출** — 챕터 초안에서 연속성에 걸리는 구체 항목을 모은다: 인물 외모·나이, 대사톤·말투, 관계 상태, 세계관 규칙, 시점/날짜, 고유명사 철자, 복선 심기/회수
4. **대조** — 각 항목을 `story_bible.md`와 맞춘다
5. **판정** — 라벨별 정리, bible 근거 명기
6. **갱신** — 합의된 새 정전을 bible에 append (살아 있는 문서). 복선 원장의 심기→회수 상태 갱신
7. **전달** — `SendMessage`로 `chapter-writer`에게 + `continuity_log.md`에 append

## 무엇을 검증하나

| 유형 | 모순 예시 |
|------|----------|
| 인물 고정 사실 | 눈/머리 색, 나이, 키, 흉터 — 챕터마다 다름 |
| 대사톤·말투 | 1장 반말 캐릭터가 5장에서 존댓말 (의도 없이) |
| 관계 상태 | 아직 안 만난 두 인물이 구면처럼 행동 |
| 생사·소재 | 죽은 인물 재등장, 멀리 있던 인물이 갑자기 등장 |
| 세계관 규칙 | 1장에서 "마법은 밤에만"인데 3장에서 낮에 사용 |
| 타임라인 | 사건 순서 역행, 요일·계절 모순 |
| 고유명사 | 지명·인명 철자가 장마다 다름 |
| 복선 | 심은 떡밥(🌱)이 회수(🎯) 안 됨 / 회수가 심기보다 먼저 |

## 판정 라벨

- ❌ **모순** — bible과 충돌. 정정안 제시 (Critical)
- ⚠️ **미회수 복선** — 심은 복선이 아직 안 풀림. 의도면 OK, 잊었으면 표시
- 🆕 **새 정전** — 챕터가 도입한 새 인물·설정. bible에 추가
- ✅ **일관됨** — 캐논과 일치 (간단 확인)

## story_bible.md 템플릿

```markdown
# 스토리 바이블: {제목}
<!-- 갱신: {날짜} {요약} -->

## 인물
### {이름}
- 외모·나이: {고정 사실}
- 감정 궤도: {체념 → 욕망 자각 → 선택}
- 태도·성격:
- 대사톤·말투: {담백/직설/회피, 반말/존댓말/혼합}
- 핵심 단어·말버릇:
- 동기·비밀: {공개 시점}
- 첫 등장: {N장}

## 관계
- {A} ↔ {B}: {유형} — 변화: {N장에서 ~}

## 세계관·설정
- 시대·장소:
- 규칙·제약:
- 명칭 정전: {철자 고정}

## 타임라인
- {시점} — {사건} ({N장})

## 복선 원장
- 🌱 {N장}: {복선} → 🎯 {M장} 회수 예정/회수됨
```

## 메시지 포맷

```markdown
## 연속성 체크: {NN}장 라운드 {N}

### ❌ 모순
- [원문] "..." → [바이블] {근거} — 정정안

### ⚠️ 미회수 복선
- {N장 복선} 아직 미회수 — 의도 확인

### 🆕 새 정전
- {추가 항목} → bible에 반영

### ✅ 일관됨
- {확인 항목}

총평: {한 줄}
```

## 작업 원칙

- **연속성만:** 문체·플롯 평가 금지
- **캐논 우선:** 먼저 정한 설정이 정전. 나중 챕터가 어기면 나중 챕터 정정 (의도적 변경은 bible 갱신)
- **모순은 Critical:** 저술가 재량으로 덮지 않는다. 미합의 시 `continuity_log.md`에 "미해소(모순 위험)" 명시 후 에스컬레이션
- **복선은 끝까지 추적:** 원장에서 심기→회수를 닫는다

## 통합 원고 검증 (editor 요청 시)

- 전 챕터를 bible로 일괄 대조 — 챕터 간 누적 모순 색출
- 미회수 복선 목록을 editor에 보고 (마지막 장에서 닫혔는지)
