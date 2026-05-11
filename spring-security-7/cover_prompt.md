# Cover Design Notes — 토비의 Spring Security 7

## 최종 선정 콘셉트: **"Layered Vault"**

심층 레퍼런스 도서의 무게감을 타이포그래피 중심 디자인으로 표현. 화려한 일러스트를 배제하고, 보안 도메인의 핵심 메타포(방패 + 키홀 + 필터 체인)를 미니멀하게 통합.

## 검토했던 3안

1. **Layered Vault (채택)** — 다크 네이비 배경 + 중앙 방패-키홀 모노그램 + 필터 체인 모티프 + 강한 타이포. 정통 기술서의 무게감을 가짐.
2. **Filter Chain Visualization** — 화면 전체를 가로지르는 필터 체인 다이어그램. 너무 도식적이라 표지로는 약함.
3. **Cryptographic Grid** — 회로 패턴과 비대칭 키 메타포. 시각적 흥미는 있으나 진부함 우려.

## 디자인 요소

### 컬러 팔레트
- 배경: `#1a1f3a → #0a0d1f` (딥 인디고 → 거의 검정 네이비, 세로 그라데이션)
- 메인 텍스트: `#ffffff` (제목), `#c8d0e8` / `#a8b2d0` / `#8892b8` (보조)
- 액센트: `#6DB33F` (Spring Green) — "7", 방패 외곽선, 필터 체인 게이트, "DEEP REFERENCE" 태그
- 구분선: `#3a4570` (저자명 위 가는 구분선)

### 시각 모티프
1. **방패 + 키홀**: 보안 도서의 정통 상징. 외곽선만 굵게(stroke 6) 처리해 무겁지 않게.
2. **필터 체인 게이트**: 방패 아래 5개의 수직 바 + 양옆 연결선. Spring Security의 FilterChainProxy 메타포.
3. **수평 구분선**: 부제 위·저자명 아래에 짧은 그린 라인 — 레퍼런스 도서다운 정돈된 인상.

### 타이포그래피 (Pretendard 패밀리)
- "토비의" — Medium 60pt, 톤다운 컬러로 부드럽게 (시리즈 식별자 역할)
- "Spring Security" — Black 175pt, 두 줄
- "7" — Black 240pt, Spring Green. 표지의 시각적 앵커
- 부제 — Medium 42pt + Regular 36pt, 두 줄로 줄바꿈
- "Toby-AI" — Bold 44pt
- "DEEP REFERENCE" — Regular 28pt, Spring Green, 트래킹 강조
- "v1.0 · 2026" — Regular 24pt, 톤다운

## 레이아웃 (1600 × 2560)

```
[상단]   토비의 (시리즈 마크)
[상중]   방패 + 키홀 모노그램 (그린)
         ┃┃┃┃┃ 필터 체인 게이트
[중앙]   Spring
         Security
         7 (그린 액센트)
[중하]   ─── (그린 구분선)
         내부 아키텍처부터 Zero Trust·Passkeys·MFA까지
         Spring Boot 4 기반 심층 레퍼런스
[하단]   Toby-AI
         DEEP REFERENCE
         ─────────────
         v1.0 · 2026
```

## 생성 방법

ImageMagick 7 (`magick`) 사용. 이미지 생성 MCP는 미사용 — 타이포그래피 기반 디자인이 의도된 콘셉트이고, 결정론적 생성으로 재현성 확보.

## 재생성 가이드

- 톤 변경 시 `#1a1f3a-#0a0d1f` 그라데이션 부분만 교체 (예: 딥 그린 톤 → `#0e2a1f-#04140d`)
- 액센트 컬러는 Spring 공식 그린 `#6DB33F` 고정 권장
- 폰트 변경 시 Pretendard 대신 Apple SD Gothic Neo로 폴백 가능

## 산출 경로

`/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/springsecurity7/spring-security-7/cover.png` (1600×2560, ~234KB PNG)
