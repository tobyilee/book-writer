---
name: research-coordination
description: Coordinate parallel research agents (web, paper, community) and synthesize findings into a unified reference document. Use when collecting background material for a book, whitepaper, or deep-dive article — triggers on "리서치 조율", "여러 소스에서 자료 모아줘", "reference 문서 만들어줘" style requests. De-duplicates, groups by theme, flags conflicts, preserves citations.
---

# Research Coordination

세 명의 리서처를 병렬 스폰하고 결과를 종합해 하나의 레퍼런스 문서를 만드는 조율 스킬이다.

## 절차

1. **리서치 브리프 작성** — 주제, 주요 내용, 대상 독자를 한 문단으로 정리
2. **병렬 스폰** — `Agent` 도구로 3명을 `run_in_background: true`로 호출
   - `web-researcher`, `paper-researcher`, `community-researcher`
   - 각각 `model: "opus"` 명시
   - 슬러그와 브리프를 입력으로 전달
3. **완료 대기** — 세 에이전트 모두 완료될 때까지 대기 (브리지 도구는 자동 알림)
4. **결과 읽기** — 각 에이전트 산출물 읽기
   - `{slug}/research/web.md`
   - `{slug}/research/papers.md`
   - `{slug}/research/community.md`
5. **종합** — 아래 통합 원칙에 따라 `01_reference.md` 작성

## 통합 원칙

- **주제별 재조직:** 소스별로 섞지 말고, "개념", "관점", "사례" 등 주제별로 묶는다
- **중복 제거:** 여러 소스에서 같은 주장이 나오면 대표 소스 하나만 인용
- **상충 병기:** 관점이 다른 자료는 "관점 A / 관점 B"로 나란히 제시
- **출처 보존:** 어떤 주장이 어느 소스에서 왔는지 반드시 표기 (웹 / 논문 / 커뮤니티)
- **커버리지 공백 명시:** 수집하지 못한 영역은 "리서치 한계" 섹션에 솔직히 기재

## 출력 구조

```markdown
# {주제} 레퍼런스

## 1. 개념과 정의
## 2. 핵심 관점들
## 3. 대표 사례
## 4. 논쟁점·상충 관점
## 5. 실무 적용 팁
## 6. 참고문헌 (URL·DOI 포함)
## 7. 리서치 한계
```

## 품질 기준

- 항목당 최소 3개 이상 소스 참조 (가능한 경우)
- 모든 수치·인용은 원문 출처 표시
- 참고문헌은 저자·연도·제목·URL/DOI 형식 통일
