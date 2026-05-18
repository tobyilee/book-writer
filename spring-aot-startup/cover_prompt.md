# Cover Design Log

## Version 1 — 2026-05-18

### Concept
하이브리드: **A (미니멀리즘) + C (타이포그래피 중심)**.
- 다크 네이비 → 거의 검은색으로 가는 방사형 그라데이션. 야간 컴파일·터미널 톤.
- 5단계 비용(JVM·CLASS·FRAMEWORK·JIT·REQUEST)을 Spring 그린 사다리(틱 마크 6개를 잇는 가로 라인)로 추상화. 책의 핵심 격자가 표지에 그대로 박힌다.
- 한글 제목 "토비의 / 스프링 부팅"을 화면의 황금 분할 지점에 굵게(Apple SD Gothic Neo Heavy 150pt).
- 4개 기술 키워드 — `AOT · Native · CRaC · Leyden` — 을 제목 바로 아래 Pretendard Bold 그린으로. 부제목 역할 + 책의 4축 명시.
- 부제 "Java는 왜 느리게 시작하는가" 는 한글로 한 줄.
- 좌상단에 작은 시리즈 마크 `TOBY · SPRING SERIES`.
- 좌하단에 저자 `Toby-AI` + 태그라인 "5단계 비용으로 다시 보는 자바 시작 시간".

### Why this concept
- 토비 시리즈 정공법(무게감·진중함) ↔ 클라우드 시대의 다크 모드/터미널 미감.
- 일러스트형(B)은 GraalVM/CRaC를 직역하는 메타포가 클리셰가 되기 쉬워 회피.
- 사다리는 책의 *주된 사고 도구*인 5단계 비용을 표지에서 미리 선언한다 — 독자가 책을 펴기 전에 책의 격자를 만난다.

### Tool
**ImageMagick 7.1.2** (image gen MCP·외부 API 미사용). 레이어드 합성:
1. `radial-gradient:'#1b2a4e'-'#070a16'` 1600×2560 베이스
2. `#5fa342` 가로 라인 + 그린 액센트 `#7fc068` 종단부
3. 5단계 틱 마크 6개 (마지막 틱만 밝은 그린)
4. 단계 라벨 (Pretendard Light 22pt, `#7888aa`)
5. 제목 두 줄 (Apple SD Gothic Neo Heavy 150pt, `#f5f7fa`)
6. 기술 키워드 행 (Pretendard Bold 56pt, `#7fc068`)
7. 부제 (Apple SD Gothic Neo Regular 64pt, `#d2dcef`)
8. 저자 + 태그라인
9. 시리즈 마크 + 상단 디바이더 라인
10. 메타 strip, PNG compression-level 9, 8-bit depth

### Palette
| 역할 | HEX |
|------|-----|
| 배경 deep | `#070a16` |
| 배경 highlight (radial center) | `#1b2a4e` |
| 본문 본문 텍스트 | `#f5f7fa` |
| 부제 텍스트 | `#d2dcef` |
| 보조 텍스트 (라벨·태그라인) | `#7888aa` |
| Spring 그린 base | `#5fa342` |
| Spring 그린 highlight | `#7fc068` |
| 시리즈 디바이더 | `#2a3a5e` |

### Fonts
- 한글: `Apple SD Gothic Neo` (Heavy/Bold/Regular) — 시스템 기본, 한글 글자균형 우수
- 라틴: `Pretendard` (Bold/Light) — 사용자 로컬 설치본

### Equivalent prompt (for future image-gen reruns)
```
A book cover in portrait format 1600x2560 for a Korean technical
book titled "토비의 스프링 부팅: AOT, Native, CRaC, 그리고 Leyden".
Style: editorial, minimalist, modernist Korean tech-book typography.
Background: deep radial gradient from navy blue (#1b2a4e) at center
to near-black (#070a16) at edges. No noise, no stock-photo textures.

Mid-upper third: a thin horizontal ladder line in Spring green
(#5fa342 → #7fc068 right-end) with six small vertical tick marks,
each labeled below in tiny grey uppercase letters with the five
JVM startup cost stages: JVM, CLASS, FRAMEWORK, JIT, REQUEST.

Center-left: Large Korean title in two lines, bold sans-serif,
near-white. Below it, in Spring green bold sans, four technology
keywords separated by middots: "AOT · Native · CRaC · Leyden".
Below that, the Korean subtitle "Java는 왜 느리게 시작하는가" in
softer near-white.

Top-left: small Spring-green caption "TOBY · SPRING SERIES" above a
short divider line. Bottom-left: author "Toby-AI" in bold near-white,
and a tagline "5단계 비용으로 다시 보는 자바 시작 시간" in muted grey.

No clichés: avoid generic gradients, avoid stock developer photos,
avoid cliché Java coffee imagery, avoid neon glow. Calm, confident,
serious. Korean technical book aesthetic — Toby series identity.
```

### Verification
- [x] 1600 × 2560
- [x] 8-bit sRGB, 269 KB (EPUB friendly)
- [x] 200×320 썸네일에서 제목 "토비의 / 스프링 부팅" 가독
- [x] 저자 `Toby-AI` 표기 존재
- [x] 클리셰 회피 (커피 김·기본 그라데이션·스톡 코드 스크린샷 없음)
- [x] 매니페스트 `cover_image: "cover.png"` 와 일치

### Notes
- 노이즈 텍스처를 처음 넣었더니 PNG가 11 MB로 부풀어 EPUB에 부담. 텍스처 제거 후 깨끗한 그라데이션으로 가니 269 KB.
- 점화 사다리를 1200~1400px 라인(상단 1/3)에 두고, 제목·키워드·부제가 시각적 무게중심(중앙~중하단)에 모이도록 배치 — 표지 썸네일에서도 한눈에 "5단계 사다리 + 한글 제목"이 잡힌다.
- 저자는 이미지 안에 명시했고 EPUB 메타데이터에서도 `Toby-AI`로 일치.

### Re-generation
다음 버전을 만들 때:
- 현재 파일을 `cover_v1.png`로 백업 후 새 빌드
- 콘셉트 변경 요청 시 위 3안에서 다시 시작
