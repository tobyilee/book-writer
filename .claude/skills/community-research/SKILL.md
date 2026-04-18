---
name: community-research
description: Mine developer/practitioner communities (Reddit, Hacker News, StackOverflow, GitHub Discussions, OKKY, velog, 네이버 카페) for real-world pain points, debates, and field-tested heuristics. Use when the user asks for "커뮤니티 의견", "실무자 목소리", "Reddit·HN 뒤져줘", "현장 경험담 모아줘", or when a book needs authentic pain-point material for chapter openings.
---

# Community Research

커뮤니티에서 **실무자의 날것 목소리**를 모은다. 논문이 이론, 웹이 정리된 지식이라면 커뮤니티는 **현장의 고통과 논쟁**의 원천이다. 이 자료가 곧 책의 "공감 포인트"가 된다.

## 절차

1. **커뮤니티 선택** — 주제·대상 독자에 맞춰 플랫폼 조합:
   - 글로벌: Reddit (서브레딧), Hacker News, StackOverflow, GitHub Discussions
   - 한국: OKKY, velog, 지디넷, 네이버 개발자 카페, 디스코드 공개 채널 로그
2. **검색 실행** — Firecrawl·WebSearch로 토론 페이지 수집
3. **패턴 추출**
   - **반복되는 고통/질문** — 3명 이상이 비슷한 고민을 토로한 패턴
   - **실무 휴리스틱** — 답변 다수 추천 또는 "10년간 써봤는데~" 식 경험담
   - **논쟁점** — 댓글 논쟁이 길게 이어진 주제, 양쪽 관점 보존
4. **검증 라벨링** — 모든 커뮤니티 주장은 "커뮤니티 의견, 검증 필요"로 표시
5. **저장** — `{slug}/research/community.md`

## 수집 가이드

- **목표 건수:** 10~20개 토론·게시글
- **원문 링크 필수:** 추후 인용 시 검증 가능해야 함
- **날것 인용:** 깔끔한 정리보다 "이 부분에서 정말 미칠 것 같다" 같은 감정 섞인 문장을 그대로 보존
- **익명 주장 주의:** 저자 프로필이 없으면 비판적으로 취급

## 출력 형식

```markdown
# 커뮤니티 리서치: {주제}

## 반복되는 고통·질문 (챕터 오프닝 소재)
### 패턴 1: {한 줄 요약}
- 출현 예시:
  - Reddit: {URL} — "...인용..."
  - OKKY: {URL} — "...인용..."
- 추정 원인 (커뮤니티가 공유하는 진단):

## 실무 휴리스틱
### 휴리스틱 1: {요약}
- 출처: {URL}
- 원문:
  > "..."
- 추천·동조 반응:

## 논쟁점
### 논쟁 A: {주제}
- 관점 1: {요약}
  - 대표 발언:
- 관점 2: {요약}
  - 대표 발언:

## 수집 한계
- 미접근 플랫폼: ...
- 언어 편중: ...
```

## 실패 대응

- 특정 플랫폼 접근 실패 → 대체 플랫폼 보충
- 주제가 너무 특수해 토론 적음 → 수량 집착 말고 질적 발췌에 집중, 한계 명시
- 검증되지 않은 주장만 풍성 → 반드시 "검증 필요" 라벨, 웹·논문 자료로 교차 확인 권고
