---
name: plan-review
description: Critically review a book plan against the reference document and audience fit. Check coverage, narrative flow, audience alignment, chapter balance, and redundancy. Use when reviewing a book outline, auditing a chapter structure, or giving structured feedback on a writing plan. Triggers on "계획 리뷰", "아웃라인 평가", "review the plan", "critique the outline".
---

# Plan Review

저술 계획을 5축으로 비판하고 구체적 수정 제안을 돌려준다. 칭찬 금지, 근거 없는 비판도 금지.

## 5축 검토

| 축 | 질문 | 빨간불 신호 |
|----|------|------------|
| 커버리지 | 주제 핵심 쟁점 중 빠진 게 있는가? | 레퍼런스의 한 챕터 분량 내용이 한 단락으로 축소됨 |
| 내러티브 흐름 | 챕터 순서가 자연스러운가? | 난이도 급등/급감, 맥락 없이 주제 점프 |
| 독자 적합도 | 대상 독자 수준에 맞는가? | 입문자용인데 2장부터 고급 개념 가정 |
| 챕터 균형 | 분량·밀도가 고른가? | 한 챕터가 다른 챕터의 3배 이상 |
| 중복·공백 | 같은 내용이 여러 장에? | 인접 장의 주요 내용 70% 이상 겹침 |

## 절차

1. **읽기** — `02_plan.md` + `01_reference.md`를 순서대로
2. **대조** — 레퍼런스의 각 섹션이 계획의 어느 장에 매핑되는지 표로 정리
3. **5축 평가** — 각 축마다 문제 3개 이내로 압축 (과다 지적 금지)
4. **우선순위 부여** — Critical / Should / Nice
5. **구체적 제안** — 문제 진단뿐 아니라 어떻게 고칠지까지
6. **전달** — `SendMessage`로 `book-planner`에게

## 리뷰 메시지 포맷

```markdown
## 리뷰 라운드 {N}

### Critical (반드시 반영)
- [챕터 {NN}] 문제: {...}
  - 근거: 레퍼런스 섹션 {X} 또는 독자 관점 {Y}
  - 제안: {구체적 수정 방향}

### Should (반영 권장)
- ...

### Nice (여유 있으면)
- ...

### 전체 평
{한 단락 — 강점과 전반적 방향성}
```

## 합의 유연성

- 최대 2회 왕복까지 피드백
- 저자가 설득력 있게 반박하면 물러설 것
- 평행선 지속 → 최종 의견과 저자 결정을 모두 `03_review_log.md`에 기록, 팀 해체

## 금지 사항

- "좋네요" 같은 공허한 긍정
- 근거 없는 취향 비판 ("이 제목은 별로예요")
- 저자가 의도적으로 선택한 전개를 모르고 통째로 바꾸자는 제안
- 전체 재작성 요구 (심각한 경우에만, 근거 상세히)
