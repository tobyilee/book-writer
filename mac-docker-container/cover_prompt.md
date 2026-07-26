# Cover Design Log — 로컬에서는 잘 됐는데요

## 입력
- 제목: 로컬에서는 잘 됐는데요
- 부제: Apple Silicon 맥에서 컨테이너 이미지를 만들고, 배포하고, 쿠버네티스까지
- 저자: Toby-AI
- 장르: tech-book
- 대상 독자: 자바·스프링 백엔드 개발자, Apple Silicon 맥 사용자, 컨테이너를 어깨너머로 써본 정도
- 톤 요구사항: 차분하고 정확한 기술서. 밈처럼 가볍지 않게. 자조적인 제목과 균형을 맞추기 위해 시각은 절제.

## 콘셉트 3안

- **A. 미니멀리즘 — 경계·층위 다이어그램(채택)**: 서로 다른 크기의 둥근 사각 프레임 3개를 중첩시켜 "맥 안의 VM, VM 안의 컨테이너"라는 책의 핵심 은유를 기하학적으로 그린다. 가장 안쪽 프레임만 미세하게 회전·이동시켜 "같은 것이 두 곳에서 다르게 보이는 어긋남"을 시각화한다.
- **B. 일러스트형 — 컨테이너/선박 메타포**: 브리프에서 명시적으로 지양 대상으로 지정(Docker 마케팅 이미지의 상투구). 채택하지 않음.
- **C. 타이포그래피 중심**: 제목 자체를 그래픽화. 이 책은 제목이 길고 부제도 있어 타이포만으로 위계를 세우면 정보 밀도가 높아져 산만해질 위험이 있다고 판단, 보조 요소로만 사용(실제로는 A안에 타이포 위계를 결합).

**최종 채택: A안 기반 + 절제된 타이포 위계**. 중첩 프레임(경계·층위)과 안쪽 프레임의 미세한 회전/오프셋(어긋남)으로 시각 방향에서 요청된 두 축을 모두 구현했다.

## 제작 경로

1. **1차 시도 — 이미지 생성(gpt-image-bridge, codex exec 경유 gpt-image-2)**: 텍스트 없는 배경 그래픽(중첩 프레임 모티프)만 생성 요청. 백그라운드로 실행했으나 조율자의 지시("무한정 기다리지 말고, 지연 시 순수 ImageMagick으로 완성하라")에 따라 프롬프트 완료를 기다리지 않고 프로세스를 종료(pkill)했다. **이 경로는 완주하지 못했다** — 실패라기보다 시간 예산상 중단.
2. **2차 경로(채택) — 순수 ImageMagick 합성**: 배경 그라데이션 + MVG(Magick Vector Graphics)로 그린 3중 둥근 사각 프레임(바깥: 옅은 슬레이트 그레이 정렬, 중간: 카퍼/앰버 정렬, 안쪽: 크림 앰버, 4도 회전 + 중심 오프셋으로 의도적 미스얼라인) + 한글 타이틀/부제/저자명 텍스트를 `magick`으로 직접 레이어링. 조율자의 판단대로, 생성 이미지 없이도 이 책의 절제된 톤과 "경계·어긋남" 모티프를 정확하게 구현할 수 있었고, 한글 렌더링 리스크도 원천적으로 없앴다.

### 사용한 명령 (핵심 단계)

```bash
MAGICK=/opt/homebrew/bin/magick
FONT="/System/Library/Fonts/AppleSDGothicNeo.ttc"

# 1. 배경 그라데이션 (짙은 차콜 네이비, 배너 시청 시 표시 아티팩트 방지용 미세 노이즈 포함)
$MAGICK -size 1600x2560 gradient:'#0f1119-#1b2233' -depth 8 \
  -attenuate 0.06 +noise Uniform -blur 0x0.4 bg.png

# 2. 3중 프레임 (frames.mvg — push/pop graphic-context로 각각 다른 색·굵기·회전)
$MAGICK -size 1600x2560 xc:none -draw "@frames.mvg" frames.png

# 3. 합성
$MAGICK bg.png frames.png -gravity NorthWest -compose over -composite comp1.png

# 4. 타이포 (제목 2행 크게 → 부제 2행 작게 → 저자명 하단)
$MAGICK comp1.png \
  -gravity North -font "$FONT" -fill "#f5f1e8" \
  -pointsize 168 -annotate +0+230 "로컬에서는" \
  -pointsize 168 -annotate +0+430 "잘 됐는데요" \
  -fill "#9aa6bb" -pointsize 46 \
  -annotate +0+700 "Apple Silicon 맥에서 컨테이너 이미지를 만들고," \
  -annotate +0+765 "배포하고, 쿠버네티스까지" \
  -gravity South -fill "#c9a877" -pointsize 44 \
  -annotate +0+150 "Toby-AI" \
  cover.png
```

`frames.mvg` 내용:

```
push graphic-context
  stroke "#3d4759"
  stroke-width 3
  fill none
  stroke-opacity 0.55
  translate 800,1650
  roundrectangle -470,-470 470,470 65,65
pop graphic-context

push graphic-context
  stroke "#b9793f"
  stroke-width 6
  fill none
  stroke-opacity 0.92
  translate 800,1650
  roundrectangle -350,-350 350,350 48,48
pop graphic-context

push graphic-context
  stroke "#ecc190"
  stroke-width 7
  fill none
  translate 830,1625
  rotate 4
  roundrectangle -230,-230 230,230 32,32
pop graphic-context
```

## 검증

- 해상도: 1600×2560 PNG (요구 규격 충족), 8-bit sRGB, alpha off
- 폰트: `/System/Library/Fonts/AppleSDGothicNeo.ttc` (family 기본 face — bold에 가까운 굵기로 렌더링됨을 육안 확인)
- 한글 렌더링 육안 확인: 제목 "로컬에서는 잘 됐는데요", 부제 전체, "Toby-AI" 전부 정상 렌더 — 두부 글자(□□□) 없음
- 썸네일(200×320) 축소 확인: 주제목 두 줄이 선명하게 판독됨. 부제는 작아 읽기 어렵지만 이는 의도된 위계(주제목 크게/부제 작게)이며 브리프의 필수 조건은 주제목 판독 가능 여부였음
- 배경 그라데이션에서 미리보기 상 밴딩처럼 보이는 가로줄이 관찰되었으나, `magick` `-crop 1x1` 픽셀 샘플링으로 실제 RGB 값이 완전히 매끄럽게(1레벨씩) 변화함을 확인 — 실제 파일 결함이 아니라 뷰어의 리사이즈 렌더링 아티팩트로 판단

## 타협·한계

- 이미지 생성(gpt-image-2) 배경 그래픽 시도는 시간 예산 때문에 완주하지 못하고 중단했다. 결과물은 생성 이미지가 전혀 섞이지 않은 100% ImageMagick 산출물이다.
- 폰트는 시스템 AppleSDGothicNeo.ttc의 기본 face만 사용했다 — ttc 내 특정 웨이트(Heavy 등)를 명시적으로 지정하는 것은 이 ImageMagick 빌드에서 실패했다(`AppleSDGothicNeo.ttc,N` 인덱스 문법 미지원). 기본 face가 이미 충분히 굵어 제목 가독성에는 문제없음.
- `cover_alt` 후보 텍스트: "짙은 남색 배경 위에 3중 둥근 사각 프레임이 중첩된 표지. 가장 안쪽 프레임만 미세하게 기울어져 어긋나 있으며, 위에는 제목 '로컬에서는 잘 됐는데요'와 부제, 하단에 저자명 Toby-AI가 있다."

## Version 1 (2026-07-26)

- Concept: A (미니멀리즘, 경계·층위 + 어긋남)
- Tool: ImageMagick (gradient + MVG 도형 + annotate 텍스트), 이미지 생성 시도는 중단
- Result: cover.png (1600×2560)
- Notes: 성공. 재생성 시 프레임 색상/회전각(`frames.mvg`)이나 타이포 포인트사이즈만 조정하면 됨.
