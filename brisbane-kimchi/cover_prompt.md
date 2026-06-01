# Cover Design Log — 타향에서 담그는 우리 김치

## Version 1 (2026-06-01)

### Concept: B — 일러스트형 (정물 + 캐릭터)

세 가지 안을 검토한 후 B안을 선택했다.

- **A (미니멀):** 배추 실루엣 하나 + 큰 타이포. 깔끔하나 요리책의 정감이 약함.
- **B (일러스트형, 채택):** 스타일라이즈드 배추김치 정물 — 켜켜이 쌓인 배추잎, 고춧가루 양념(붉은 코팅), 파채, 참깨. 둥근 옹기/유리병 느낌의 링으로 감쌈. 브리즈번 햇살 암시를 위해 우상단에 작은 태양 모티프.
- **C (타이포 중심):** 제목 자체가 그래픽. 실용 요리서에는 시각적 음식 단서가 필요해 탈락.

### 설계 의도

- **색상 팔레트:** 아이보리(BG) + 김치레드(#B22222/#CC3C28) + 우드톤(#8B5A2B). 따뜻하고 식욕을 자극하면서 정갈한 요리책 톤.
- **구도:** 상단 1/4 — 한글 제목(타향에서 + 담그는 우리 김치). 중앙 — 배추김치 일러스트. 하단 — 부제/저자. 상·하 붉은 밴드가 프레임 역할.
- **호주 암시:** 우상단 소형 태양 모티프(노란색 방사선). 과하지 않게 배치.
- **타이포:** Noto Sans KR (Variable, 시스템에 설치된 한글 폰트). 제목 첫 줄 다크톤, 둘째 줄(담그는 우리 김치) 김치레드로 강조.

### 생성 방법

- **도구:** Python Pillow (PIL) — 이미지 생성 MCP/외부 API 없음, ImageMagick보다 세밀한 타이포·일러스트 제어 가능.
- **이미지 생성 API 시도 여부:** 별도 API 키 없음 → Pillow 직접 드로잉으로 진행.
- **해상도:** 1600×2560 (EPUB 권장 비율 1:1.6).
- **생성 스크립트:** `gen_cover.py` (산출 후 삭제 예정)

### 영어 이미지 프롬프트 (API 재생성 시 참조)

```
A warm, inviting cookbook cover in portrait format (1600x2560 px).
Background: soft warm ivory (#FCF5E6) with a subtle linen texture.
Center: a stylised illustration of napa cabbage kimchi — layered pale-yellow
cabbage leaves generously coated in vibrant gochugaru paste (deep crimson-red),
topped with green scallion threads and white sesame seeds. The kimchi sits
inside a soft circular frame suggesting a traditional Korean onggi earthenware
crock or a glass mason jar. 

Top section: bold Korean title text "타향에서 담그는 우리 김치" in a clean
sans-serif; first line dark warm-brown, second line in deep kimchi-red.
Below title: subtitle "브리즈번 김치 노트" in a lighter warm-grey.

Upper-right corner: a small stylised sun with short rays in golden yellow,
suggesting bright subtropical Brisbane sunlight — subtle, not dominant.

Top and bottom: deep kimchi-red horizontal bands with a thin wood-brown
accent line, creating an elegant frame. Bottom band contains author credit
"Toby-AI" in cream italic.

Overall style: editorial Korean cookbook cover, warm and homely, food-magazine
quality, no stock-photo aesthetic, no generic gradient. Color palette: ivory,
kimchi-red, wood-brown, cream, warm charcoal.
```

### 결과

- 파일: `cover.png`
- 크기: 1600×2560 px, RGB PNG, ~97 KB
- 검증: 제목 가독성 양호 / 저자 표기(Toby-AI) 하단 크림색으로 명시 / 아이보리+레드+우드 팔레트 준수

### 개선 메모 (재생성 시)

- 실제 이미지 생성 API(DALL-E, Stability)를 사용하면 포토리얼리스틱 배추김치 사진 표지 가능.
- 한글 폰트 두께 조정: 제목 첫 줄 Heavy weight 적용 시 더 강한 존재감.
- 태양 모티프를 왼쪽 상단으로 이동하거나 더 크게 하면 호주 분위기 강화.
