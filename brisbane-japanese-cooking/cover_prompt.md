# Cover Design — 다시부터 사시미까지

## 책 정보
- 제목: 다시부터 사시미까지
- 부제: 한식 하던 손을 위한 브리즈번 일식 수업
- 저자: Toby-AI
- 장르: practical (일식 쿠킹 가이드)
- 대상: 한식에 능숙한 한국 출신 이민자, 일식 입문
- 비율/해상도: 1600 × 2560 (EPUB 세로, 1.6:1)

## 분위기 키워드
따뜻하고 정갈한 일식 가정요리 · 다시·스시·면·구이 · 한국 이민자 친근함 + 일식 단정함 · 브리즈번(호주) 밝은 자연광 · 쪽빛(indigo)·나무·자연광 색감 · 오버디자인 금지

## 콘셉트 3안

1. **(채택) 미니멀 심볼 + 타이포** — 쪽빛→딥틸 그라데이션 배경에 다시 그릇(원형) 한 점을 중심 심볼로. 상단에 브리즈번 자연광을 암시하는 따뜻한 빛 띠. 큰 한글 제목 + 부제 + 저자. 정갈하고 썸네일에서도 읽힘. 전 장르 안전.
2. 일러스트형 — 도마 위 사시미·차완·젓가락 평면 일러스트. 정보량 많지만 썸네일 가독성·수명에서 불리.
3. 타이포 중심 — 큰 붓글씨 느낌 제목만. 단정하나 "일식 요리" 단서가 약함.

## 채택안: 1번

### 이미지 생성 프롬프트 (영문, 향후 gpt-image-1 / DALL-E 재생성용)
> Minimalist book cover, vertical 1600x2560. Calm indigo-to-deep-teal gradient
> background evoking Japanese dashi broth and restraint. A single warm band of
> Brisbane natural daylight across the upper third. Centered quiet symbol: a
> simple round ceramic dashi bowl seen from above with subtle steam, thin
> concentric rings suggesting broth. Soft wood-tone accent. Generous negative
> space for a large Korean title. Refined, editorial, not busy. Warm + serene
> palette: indigo #1b3a5b, deep teal #14ararar, wood #c8a06a, off-white #f4efe6.
> No text rendered by the model (text composited separately for crisp Korean).

### 생성 방식 (실제)
이미지 생성 MCP/HTTP API가 환경에 연결되어 있지 않아 **ImageMagick 타이포그래피 폴백**으로
제작. 모든 한글 텍스트를 벡터 폰트로 또렷하게 렌더(썸네일 가독성 확보).
- 배경: 쪽빛→딥틸 세로 그라데이션 + 상단 자연광 띠
- 중심 심볼: 다시 그릇(동심원) + 김(steam) 곡선, 나무톤 악센트선
- 폰트: AppleSDGothicNeo (Heavy/Bold) — 한글, Pretendard 보조
- 제목 2줄 + 부제 + 하단 저자 + 장르 캡션

### 재생성/AB 테스트 메모
- 외부 이미지 API 사용 가능 시 위 영문 프롬프트로 배경 아트만 생성 후
  한글 타이포는 동일하게 합성하면 가독성·분위기 둘 다 확보.
- 색을 더 따뜻하게(브리즈번 강조) 하려면 자연광 띠 폭↑, wood 악센트↑.
