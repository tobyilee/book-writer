---
name: web-research
description: Search the general web (blogs, articles, official docs, tutorials) for topic-relevant content and compile findings with full citations. Use when the user asks to "웹 리서치", "블로그 자료 모아줘", "공식 문서 뒤져줘", "search the web for", "find articles on", or when gathering secondary material outside academic/community sources.
---

# Web Research

주제 관련 일반 웹 자료(블로그, 기사, 공식 문서, 튜토리얼)를 수집한다. 논문과 커뮤니티는 별도 에이전트가 맡으므로 중복 수집하지 않는다.

## 절차

1. **검색 키워드 설계** — 주제에서 3~5개 키워드 조합 생성 (한국어 + 영어)
2. **검색 실행** — 우선순위:
   - Firecrawl 스킬 (가능 시) — 전문 추출·인덱싱에 강함
   - WebSearch 도구 → 상위 결과 링크 수집
   - WebFetch 도구 → 각 페이지 본문 가져오기
3. **소스 평가** — 신뢰성 등급 매기기
   - 최상: 공식 문서, 기술 저널, 확인된 저자 블로그
   - 중: 커뮤니티 블로그, 포털 기술 아티클
   - 하: 출처 불명 나열형 아티클, 날짜 없는 글 (가능하면 제외)
4. **추출** — 각 자료에서 핵심 주장, 인용 가능한 구절, 수치 발췌
5. **저장** — `_workspace/{slug}/research/web.md`

## 수집 가이드

- **목표 건수:** 8~15건 (주제 폭에 따라 조정)
- **다양성:** 한 사이트 최대 2건, 한 저자 최대 2건
- **최신성:** 최근 3년 내 자료 비중을 높이되, 고전 레퍼런스도 1~2건 포함
- **언어 비율:** 대상 독자가 한국이면 한국어 60~70%, 글로벌이면 영어 70%+
- **인용 원문 보존:** 요약하지 말고 구절을 그대로 가져와 따옴표 처리

## 출력 형식

```markdown
# 웹 리서치: {주제}

## 자료 1: {제목}
- 출처: {URL}
- 저자·날짜: {...}
- 신뢰성: {최상/중/하}
- 핵심 주장: {2~3문장}
- 인용 가능한 구절:
  > "..."
- 관련 섹션: (레퍼런스 문서 어느 섹션에 쓸지 힌트)

## 자료 2: ...

## 수집 한계
- 접근 실패한 자료: ...
- 의도적으로 제외한 소스 유형: ...
```

## 실패 대응

- 검색 결과 빈약 → 키워드 변형 (동의어, 영문 번역, 약어 ↔ 풀네임) 후 재시도
- 특정 페이지 접근 실패 → 해당 자료 제외, 로그에 기록
- Firecrawl·WebSearch 모두 실패 → 캐시된 아카이브(archive.org) 활용 시도
