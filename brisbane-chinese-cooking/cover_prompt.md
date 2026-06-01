# Cover Design Log

## Version 1 (2026-06-01) — FINAL

- **Concept:** B-variant (Typographic + Cultural Symbol) — 주제 메타포 기반
- **Tool:** ImageMagick 7.1.2 (폴백 — 이미지 생성 MCP/API 미연결)
- **Font:** Apple SD Gothic Neo (AppleSDGothicNeo.ttc), Regular/Bold

### Design Rationale

콘셉트 3안 구상:
- **A (미니멀):** 단색 배경 + 심볼 하나. 차분하지만 요리서 톤이 약함.
- **B (일러스트/심볼 타이포):** 짙은 간장-갈색 배경 + 한국어 대제목 + 중문 화자(火) 워터마크 + 빨간 강조선. 선택안.
- **C (타이포 중심):** 제목 자체를 그래픽으로. 한글 글리프만으론 단독 시각 임팩트 약함 — 기각.

**선택 이유:** 실용 요리서(practical)는 온기 있는 색감 + 중식 정체성 상징(火)이 독자에게 직관적으로 장르를 전달한다. 배경의 짙은 간장갈색(#1C1008)이 "깊고 따뜻한 중식 부엌" 무드를 만들고, 붉은 강조선과 황금색 제목이 에너지를 준다.

### Color Palette

| 역할 | HEX | 설명 |
|------|-----|------|
| 배경 | `#1C1008` → `#180E06` | 깊은 간장-밤 갈색 그라데이션 |
| 대제목 1행 | `#F5EDD8` | 따뜻한 크림 화이트 |
| 대제목 2행 | `#E8A020` | 황금 간장색 |
| 강조선 | `#C0392B` | 중식 홍등 빨강 |
| 강조선 보조 | `#E8A020` | 황금 |
| 부제 | `#F0E0C0` | 따뜻한 아이보리 |
| 영문 서브 | `#9A8878` | 중간 갈회색 |
| 火 워터마크 | `#4A1E0E` | 배경보다 살짝 밝은 딥레드 |
| 저자 | `#C8B090` | 따뜻한 샴페인 |
| 하단 태그라인 | `#C09060` | 황금-베이지 |

### Layout Structure (1600×2560)

```
[상단 강조선 — 빨강 14px + 황금 5px]
[상단 여백 ~310px]
브리즈번           ← 175pt 크림 화이트
중식 키친          ← 175pt 황금색
Brisbane Chinese Kitchen ← 50pt 갈회색
[중간 여백]
──────────────     ← 빨강 선 장식
호주 재료로 차리는   ← 76pt 아이보리
중국요리            ← 76pt 아이보리
火                 ← 340pt 딥레드 워터마크 (배경에 묻히는 톤)
웍 하나로 완성하는 6대 계통 레시피 ← 42pt 태그라인
────  Toby-AI  ──── ← 50pt 저자
[하단 강조선 — 빨강 14px + 황금 5px]
```

### ImageMagick Command Summary

```bash
magick -size 1600x2560 xc:"#1C1008" \
  (gradient overlay #2A1A08→#180E06) \
  (accent lines: red #C0392B 14px + gold #E8A020 5px, top & bottom) \
  (lower panel: #221006 720px) \
  -font AppleSDGothicNeo.ttc \
  [title / subtitle / 火 symbol / tagline / author layers]
  cover.png
```

### Result

- cover.png: 1600×2560 px, PNG, ~193 KB
- 썸네일 가독성: 제목 2행 명확히 읽힘
- 저자 표기: "Toby-AI" 하단 중앙
- 클리셰 여부: 그라데이션 배경이지만 간장갈색 계열로 클리셰 피함

### Notes

- 이미지 생성 API(gpt-image-1 등) 미연결 → ImageMagick 타이포그래피 방식으로 산출
- 재생성 시 이미지 API 연결되면 "wok with steam, soy sauce bottles, fresh vegetables, warm red-brown editorial cookbook cover" 방향으로 일러스트 시도 권장
- 한국어 렌더링은 Apple SD Gothic Neo 직접 경로 지정으로 안정적 처리
