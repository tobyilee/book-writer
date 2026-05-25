# Cover Design Record — 「AI에게 맡기고, 함께 자란다」

- **Slug:** growing-with-ai
- **Title:** AI에게 맡기고, 함께 자란다
- **Subtitle:** 코드를 다 써주는 시대에 개발자가 둔해지지 않는 법
- **Author:** Toby-AI
- **Genre:** tech-book (IT 개발서)
- **Target audience:** AI 시대의 중급~시니어 개발자
- **Spec:** 1600 × 2560 (세로, EPUB 권장 1.6:1)

## 무드

두려움에서 출발해 성장·희망으로 도착하는 동반자적 정서. 차갑지 않고 따뜻하되,
개발서답게 단정하고 모던. 서가에서 신뢰감 있게 집어 들 만한 톤.

## 콘셉트 3안

1. **(채택) 미니멀 타이포 + 성장 모티프** — 딥 틸→네이비 세로 그라데이션 배경,
   따뜻한 골드/세이지 악센트. 화면 하단에서 위로 자라나는 가느다란 선:
   코드 들여쓰기 가이드라인(│)이 위로 뻗으며 새싹 잎이 되는 은유.
   큰 제목 + 절제된 여백 + 하단 저자명. 썸네일에서도 제목 가독성 확보.
2. 일러스트형(사람+AI 나란히) — 오버디자인·폴백 렌더 품질 리스크로 제외.
3. 타이포 only — 성장/희망 정서가 약해 제외.

> 클리셰(로봇 손 악수, 뇌 회로)는 의도적으로 배제. 성장 모티프는
> "코드 구조선이 식물로 자라는" 추상 메타포로 대체.

## Image generation prompt (영문, 외부 image-gen 모델용)

> Vertical book cover, 1600x2560, for a modern software-engineering book.
> Calm, trustworthy, hopeful mood — a journey from quiet anxiety to growth.
> Deep teal-to-midnight-navy vertical gradient background, soft and matte,
> not glossy. A single delicate vertical line rises from the lower third of
> the cover — it begins as a thin code indentation guide (like an editor's
> indent rail) and gradually transforms into a slender growing sprout with
> two or three small leaves near the top, rendered in warm sage-green with a
> subtle gold glow. Generous negative space. Minimal, editorial, premium
> typography aesthetic. No robots, no handshakes, no brain circuits, no
> human faces. Quiet, literary tech-book feel. Leave clear space in the upper
> half for a large Korean title and a thin subtitle line below it; author
> name small at the bottom. High contrast title legibility at thumbnail size.
> Flat vector + soft glow, no photographic clutter. Color palette: #0E2A33,
> #14323D, #1B4350 (background), #E9C46A / #F2CC8F (gold accent),
> #A7C4A0 / #88B388 (sage growth), #F4F1EA (off-white text).

## 실제 생성 방법

- 연결된 image-gen MCP/API 없음 → **ImageMagick 타이포그래피 + 벡터 모티프**로 산출.
- 폰트: Pretendard (Black/SemiBold/Light/Medium) — 모던한 한글 본고딕 계열.
- 배경: 수직 그라데이션(딥 틸→네이비) + 미세 노이즈/비네트.
- 성장 모티프: 하단에서 올라오는 들여쓰기 가이드선 → 상단에서 새싹 잎으로 분기 (SVG path).
- 산출: `growing-with-ai/cover.png` (1600×2560, sRGB).

## 재생성/AB 메모

- 색 변주: gold 악센트를 coral(#E76F51)로 → 더 강한 정서 / sage를 강조 → 더 차분.
- 모티프 변주: 단일 새싹 대신 나이테(궤도) 동심원, 혹은 나란한 두 선(사람·AI 병주).
