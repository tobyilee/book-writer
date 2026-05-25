# Cover Design Log — 브리즈번 홈베이킹

## 책 정보
- 제목: 브리즈번 홈베이킹: 아열대 부엌의 사워도우와 빵
- 부제(표지용): 사워도우 스타터부터 크루아상·밀크식빵 / 한국식 조리빵까지
- 저자: Toby-AI
- 장르: practical (가정 베이킹 실용서)
- 무드: 따뜻하고 식욕 돋우는, 가정적·신뢰감. 브리즈번 아열대의 밝은 자연광. 모던 쿡북 감성.
- 팔레트: 크러스트 브라운 `#4a2a12` / 캐러멜 액센트 `#a85f23` / 크림 `#fbf3e2`, 호주 햇살 골든 `#ffd97a`.

## 콘셉트 3안
- A 미니멀: 심볼 하나 + 큰 타이포
- B 일러스트형: 주제 메타포 이미지 (사워도우 캄파뉴)
- C 타이포그래피 중심
- **채택: B+C 하이브리드** — 스코어링 십자(+)가 새겨진 둥근 사워도우 불(boule)을 히어로로,
  상단 1/3에 볼드 한글 타이포. 썸네일에서도 빵과 제목이 즉시 읽히는 모던 쿡북 레이아웃.

## Version 1 (2026-05-25)
- Concept: B+C 하이브리드
- Tool: ImageMagick 7.1.2 (이미지 생성 MCP/API 미연결 → 벡터+그라데이션 기반 일러스트로 구성)
- Fonts: Pretendard (Black=제목, SemiBold=킥커/저자, Medium=부제). 한글 가독성 확보.
- Result: cover.png (1600×2560, 8-bit sRGB)

### 의도한 생성형 프롬프트 (외부 이미지 모델 사용 시 참고)
```
A warm, appetizing modern cookbook cover, portrait 1600x2560 (1.6:1).
Hero: a freshly baked round sourdough campagne boule, golden-caramel crust
with a clean cross "+" scoring on top, light flour dusting, soft bloom along
the scored edges. Bright subtropical (Brisbane) natural daylight from the upper
right, gentle golden glow. Background: warm cream-to-wheat gradient, airy and clean.
Palette: crust brown, cream, flour white, Australian golden sunlight accent.
Composition: title prominent in the upper third, the loaf centered in the lower
half, small author attribution at the bottom. Editorial, homely, trustworthy.
No cheesy stock photo, no generic tech gradient, no text artifacts.
```

### ImageMagick 구성 (실제 사용)
- 배경: `gradient:'#f7ecd6-#e3bd86'` + 대형 디퓨즈 골든 선글로우(`#fff0c0`, blur 0x260) + 하단 워밍 비네트
- 빵 본체: `radial-gradient:'#f2c27e-#c07d3a'` + Gaussian 노이즈 softlight(크러스트 텍스처) → 0.82 비율 oval 마스크
- 엣지 셰이딩: Distance morphology → pow 3.2 → 워밍 `#8a4d1c` 0.30 강도
- 스코어링: 라이트 블룸선 `#f7dcab`(strokewidth 32) 위에 다크 그루브 `#9c5a26`(9) 십자
- 하이라이트: 좌상단 `#fff6e2` 소프트 원 0.34
- 그림자: 빵 아래 0.34 스케일 타원 blur 0x60, 알파 0.45
- 플라워 더스트: 시드 고정 91개 미세 원(`flour.mvg`), blur 0x0.6
- 타이포: 킥커(SemiBold 52 `#a85f23`) / 제목 2줄(Black 188 `#4a2a12`) / 디바이더 바 `#a85f23` /
  부제 2줄(Medium 50) / 저자 "Toby-AI"(SemiBold 54) + "SUBTROPICAL HOME BAKING"(Medium 34 `#a85f23`)

### 검증
- [x] 해상도 1600×2560
- [x] 200×320 썸네일에서 제목·빵·저자 모두 판독 가능
- [x] 저자 "Toby-AI" 명시 (이미지 내 + EPUB 메타와 일치)
- [x] 클리셰 회피 (스톡사진/기술 그라데이션 없음)
- Notes: 빵이 다소 평면적. 후속 개선 시 크럼(단면) 노출 또는 실제 사진/생성형 이미지로 교체하면
  식욕 자극 강화 가능. 현재 버전은 썸네일 가독성·브랜드 톤 우선.

## 재생성 안내
- "표지 다시" → 현재 cover.png를 cover_v1.png로 백업 후 재생성, 이 로그에 Version 2 append.
- 콘셉트 변경 → 3안부터 재구상.
