# 표지 디자인 기록 — 검증 세금

## 콘셉트 채택
**Option B (The 19% Gap) + Option A subtle hybrid (tax-slip serial mark).**

타이포그래피 중심. 거대한 `19%` 수치가 화면 상단을 지배하고, 그 아래 *예측 / 체감 / 실측* 3행 데이터로 인지·실측의 갈라짐(취소선 처리)을 시각화한다. 책의 제목 `검증 세금`이 하단을 묵직하게 받치고, 부제·저자명이 위계를 따른다. 우하단의 `NO. 001 / v1` 작은 모노 마크는 Option A의 *세금 영수증* 메타포를 은근하게 호출한다.

### 채택 사유 (1줄)
계획 §1이 *"제목만으로 클릭을 부른다"*고 못박았고, 시니어 개발자/EM/CTO 독자층은 일러스트보다 정직한 타이포 커버에 반응한다(O'Reilly, Pragmatic 류 셔블링).

## 색상 팔레트
| 역할 | HEX | 의미 |
|------|-----|------|
| 배경 | `#F2EDE4` | bone white — 영수증 종이 톤 |
| 본문 | `#0e0e0e` ~ `#1a1a1a` | ink black — 진단의 권위 |
| 보조 | `#5a4a3a` | sepia/소토(부제·라벨) |
| 강조 | `#7a1f24` | oxblood — 통증·경고 |
| 흐림 | `#9a9a9a` | 취소선·메타데이터 |

## 타이포그래피
- 제목 `검증 세금`: Apple SD Gothic Neo Heavy, 400pt
- 거대 수치 `19%`: Apple SD Gothic Neo Heavy, 880pt, oxblood
- 부제: Noto Sans KR, 58pt, 2행
- 본문 라벨: Noto Sans KR Regular, 32pt
- 측정값: Menlo (mono), 36~42pt — 데이터의 *측정성*을 시각화
- 저자 `Toby-AI`: Noto Sans KR, 44pt + `지음` 26pt
- 우하단 메타 `NO. 001 / v1`: Menlo, 22pt, light grey

## 생성 방법
- **도구:** ImageMagick 7.1.2 (로컬 합성, 단일 `magick` 커맨드)
- **이유:** Korean 한글 글리프는 image-gen 모델(SD/DALL-E/Imagen)에서 자주 깨진다. 타이포 중심 디자인이라 type-perfect 결과가 필수 → 로컬 합성이 가장 안전.
- **폴백 없음:** ImageMagick이 1차 선택이었고, 정상 작동.

## 입력 텍스트 (변경 시 주의)
```
상단 라벨   : "AI  코딩  시대  ·  엔지니어링  에세이"
거대 수치   : "19%"
데이터 행   :
  본인 예측    −24%        (취소선)
  본인 체감    −20%        (취소선)
  측정 결과    + 19%   느려졌다   (oxblood)
제목        : "검증 세금"
부제        : "AI 코딩 시대,"
              "빨라진 줄 알았던 19%의 진실"
저자        : "Toby-AI"  /  "지음"
메타        : "NO. 001  /  v1"
```

## 재생성 가이드
- 다른 콘셉트 시도 시: Option A(영수증 일러스트), Option C(저울/모래시계), Option D(콕핏 계기판) 중 선택
- 제목·부제만 바꿔 동일 레이아웃 재사용 가능 — 위 magick 커맨드의 annotate 텍스트만 교체
- 저자 변경 시: `Toby-AI` 와 `NO. 001 / v1` 두 곳을 동시 수정
- 색상 톤 변경 (예: 더 차가운 톤): oxblood `#7a1f24` → deep blue `#1f3a7a`, sepia `#5a4a3a` → cool grey `#5a5a64`

## 산출 사양
- **경로:** `/Users/tobylee/workspace/ai/book-writer/ai-coding-cognitive-prosthesis/cover.png`
- **해상도:** 1600 × 2560 (1.6:1, EPUB 표준)
- **포맷:** PNG, 16-bit/color RGBA, non-interlaced
- **파일 크기:** ~291 KB
