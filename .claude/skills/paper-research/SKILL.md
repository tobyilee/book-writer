---
name: paper-research
description: Search academic sources (arXiv, Google Scholar, Semantic Scholar, ACM, IEEE) for research papers and extract theoretical foundations, methods, empirical findings, and citation-worthy claims. Use when the user asks for "논문 리서치", "학술 자료", "arXiv에서 찾아줘", "papers on", or when a book/article needs rigorous academic backing.
---

# Paper Research

학술 자료에서 이론·방법·실증 결과를 수집한다. 대중 자료나 커뮤니티 토론은 다루지 않는다.

## 절차

1. **검색 전략 수립**
   - 서베이 논문을 먼저 찾는다 (분야 전체 조감에 유리)
   - 그 다음 seminal 논문 (피인용 500+) 2~3편
   - 그 다음 최근 3년 내 주요 논문 3~5편
2. **검색 소스**
   - arXiv (사전 인쇄)
   - Google Scholar (피인용 순)
   - Semantic Scholar API (abstract·링크 조회 유리)
   - 분야별 학회·저널 (ACM, IEEE, ACL 등)
3. **논문 평가**
   - 피인용수, 발표처, 재현성 여부 확인
4. **추출** — 각 논문에서:
   - 핵심 주장 (3~5문장)
   - 방법론 요약 (대상 독자 수준에 맞게 추상화)
   - 수치·실험 결과
   - 인용 가능한 문장 (원문 페이지·섹션 표시)
5. **저장** — `_workspace/{slug}/research/papers.md`

## 가이드

- **목표 건수:** 3~10편
- **최신성·고전 균형:** 7:3 또는 5:5
- **독자 수준 고려:** 비학문 개발자 대상이면 수학적 증명은 축약, 결과와 직관 중심
- **재현성 점검:** 코드·데이터 공개 여부를 체크해 "실제로 써볼 수 있는" 자료 우선

## 출력 형식

```markdown
# 논문 리서치: {주제}

## 논문 1: {제목}
- 저자·연도: {...}
- 발표처: {학회·저널명, 볼륨}
- DOI/arXiv ID: {...}
- 피인용수: {숫자, 조회 시점}
- 요약 (3~5문장):
- 방법론 요약:
- 핵심 수치·결과:
- 인용할 만한 문장:
  > "..." (p.{페이지})
- 독자 전달 방식 제안: {비유·단순화 아이디어}
```

## 실패 대응

- arXiv·Scholar 접근 실패 → Semantic Scholar API 활용
- 논문 전문 접근 불가 → abstract + 공개 프리프린트 기반, 한계 명시
- 서베이 논문 없음 → 분야 리뷰 아티클(예: ACM Computing Surveys)로 대체
