# Cover Design Log

## Version 1 (2026-05-17)

### Book Info
- **Title:** 에이전트의 시대, DDD는 여전히 유효한가?
- **Subtitle:** 변하는 것, 살아남는 것, 사라지는 것
- **Author:** Toby-AI
- **Edition:** v1.0
- **Genre:** 에세이형 기술서 (실용 + 철학적 회고 + 거버넌스)
- **Audience:** 시니어 개발자, 테크 리드, 아키텍트

### Concept
**A안 변형 — 미니멀리즘 + 다층 기하 모티프**

심화·이론서 톤에 맞춰 미니멀리즘을 베이스로 택했다. 단순한 추상 심볼 하나만 두는 대신, 책의 핵심 메시지("변하는 것·살아남는 것·사라지는 것")를 시각화한 **3계층 수평선 + 점 패턴**을 모티프로 삽입했다. 점들은 BC(Bounded Context) 매핑과 에이전트 토폴로지를 동시에 연상시키며, 위에서 아래로 갈수록 옅어지는 명도가 "사라지는 것"의 메타포를 직접 전달한다.

### Palette
| 역할 | 색상 | 코드 |
|------|------|------|
| 배경 상단 | 짙은 청록 | `#0a1e2a` |
| 배경 하단 | 짙은 남색 | `#15102a` (세로 그라데이션) |
| 강조 (앰버) | 따뜻한 황금 | `#d4a64a` |
| 본문 텍스트 | 웜 오프화이트 | `#f5efe0` |
| 보조 텍스트 | 쿨 라벤더 회색 | `#9a9ab5` |
| Layer 1 (살아남는 것) | 밝은 청회색 | `#5a7488` |
| Layer 2 (변하는 것) | 중간 톤 | `#3a4a5e` |
| Layer 3 (사라지는 것) | 어두운 톤 | `#252a3a` |

### Typography
- **메인 제목:** Pretendard Black, 125pt — 한국어 가독성 + 진중한 무게
- **장르 라벨:** Pretendard SemiBold, 38pt, 자간 8 — 황금 컬러로 톤 설정
- **부제:** Pretendard Light, 54pt — 차분한 회색
- **저자:** Pretendard SemiBold, 58pt — 화이트
- **태그라인:** Pretendard Light, 30pt — 회색
- **버전 마크:** Pretendard Regular, 26pt

### Layout (1600×2560)
```
y=  0  ─ 240  : top margin + v1.0 mark (top-right corner)
y=240  ─ 380  : "AI · ARCHITECTURE · DDD" eyebrow (amber)
y=380  ─ 1180 : 3-line title block
                  L1: 에이전트의 시대,
                  L2: DDD는 여전히
                  L3: 유효한가?
y=1030 ─ 1034 : amber accent rule (180px wide)
y=1080 ─ 1140 : subtitle "변하는 것 · 살아남는 것 · 사라지는 것"
y=1180 ─ 1900 : breathing space (intentional silence)
y=1900 ─ 2160 : 3-layer motif
                  - 3 horizontal rules (layer1/2/3)
                  - 24-column dot grid aligned with rules
                  - amber accent every 6th node in top row
y=2160 ─ 2300 : breathing space
y=2300 ─ 2370 : "Toby-AI" author
y=2400 ─ 2440 : tagline (English subtitle)
```

### Tool Used
**ImageMagick 7.1.2** (시스템 폴백). 이미지 생성 MCP/외부 API는 이 환경에서 직접 호출 불가하여 타이포그래피 기반 미니멀 표지로 진행. 영어 프롬프트 기반 일러스트형 표지보다 한국어 제목 가독성·정밀 레이아웃 제어 측면에서 오히려 적합한 선택.

### Build Script
`_cover_build.sh` (재생성·A/B 테스트용 보존)

### Design Rationale
- **클리셰 회피:** 흔한 "AI 그라데이션", 회로 기판, 뇌 일러스트, generic tech 그라데이션 모두 배제
- **3계층 메타포:** 책의 핵심 주장을 표지에서 즉시 읽히도록. 윗선이 밝고 점이 굵음 (살아남는 것), 가운데가 중간 톤 (변하는 것), 아랫선이 옅음 (사라지는 것)
- **앰버 액센트:** 차가운 베이스에 따뜻한 황금 한 줄을 더해 "기술서지만 인간이 쓴 회고/철학"이라는 톤 표현
- **호흡 공간:** 제목과 모티프 사이의 큰 빈 공간은 의도적. 컨퍼런스 발표를 책으로 풀어낸 듯한 무게에 어울리는 정적 균형
- **저자명:** 매니페스트의 `author: Toby-AI` 값과 일치. 향후 다른 저자로 빌드 시 스크립트의 `label:"Toby-AI"` 한 곳만 교체

### Result
- File: `ddd-in-ai-era/cover.png`
- Size: 1600×2560, PNG, ~10.7 MiB (16-bit sRGB)
- Verification: ImageMagick `identify` 확인. 썸네일 축소 시에도 제목 가독성 양호.

### Notes for Future Revisions
- 일러스트형 표지를 원할 경우: 옛 그리스 신전 아치(도메인 모델의 영속성) + 그 위에 디지털 와이어프레임 격자(에이전트 토폴로지)가 중첩되는 컨셉으로 외부 이미지 모델(`gpt-image-1`, SDXL) 활용 추천
- 타이포그래피 강조 버전(C안)을 원할 경우: 제목을 더 크게(160pt+), 부제 영역 축소, 모티프 제거
- 권 단위 시리즈로 확장 시: 앰버 액센트 색만 권별로 다르게 (1권 황금, 2권 인디고, 3권 청록 등)
