# Cover Design Log — 《AI 에이전트, 무엇으로 갈리나》

- 제목: AI 에이전트, 무엇으로 갈리나
- 부제: 프레임워크·데이터·평가·런타임 선택 가이드
- 저자: Toby-AI
- 장르: tech-book (도구 서베이 + 의사결정 가이드)
- 톤: "냉정한 결정 가이드" — 감탄하지 않고 갈림길을 짚는다

## 콘셉트 3안 구상

**A. 미니멀리즘 — 분기선 다이어그램 (채택)**
단일 선이 하나의 줄기에서 출발해 여러 갈래로 갈라지는 스키매틱 다이어그램. 그중 하나만
따뜻한 코퍼/앰버 색으로 강조되어 "선택된 경로"를 암시한다. 차분한 다크 네이비 배경,
넉넉한 여백. 책의 핵심 논지("제품이 아니라 축으로 판단하라", "무엇으로 갈리나")를
문자 그대로 시각화한다.

**B. 일러스트형 — 3층 스택 단면도**
런타임 → SDK → 하네스의 3층 구조를 단면도처럼 쌓인 수평 밴드로 표현하고, 그 위에 수직
축 선을 하나 그어 "층을 관통하는 판단 기준"을 암시. 콘셉트 A보다 설명적이지만 정보량이
많아 표지에서는 다소 도식적·산만해질 위험.

**C. 타이포그래피 중심 — 제목 자체를 갈라지게 배치**
"무엇으로", "갈리나" 두 단어를 물리적으로 갈라진 두 줄기로 배치해 제목 자체가 그래픽이
되게 하는 안. 강렬하지만 한글 타이포를 이미지 생성 모델로 만들 수 없어 전량 합성 폰트
배치에 의존해야 하고, 상표성 있는 커스텀 레터링 없이는 A안보다 임팩트가 떨어짐.

**선택: A안.** 이 책은 "축으로 판단하라"는 단일 논지를 반복한다. 분기선 다이어그램은
그 논지를 은유가 아니라 거의 직역에 가깝게 전달하면서도, 로봇·AI 스톡 이미지 클리셰를
전혀 쓰지 않는다. 대상 독자(백엔드/풀스택 개발자, 테크리드)에게도 스키매틱 다이어그램은
친숙한 시각 문법이다.

## 이미지 생성 경로

1. **`gpt-image-bridge` 스킬 사용 (성공).** 배경 아트워크만 생성 — 한글 렌더링 실패를
   피하기 위해 프롬프트에 텍스트를 전혀 넣지 않고 순수 다이어그램만 요청했다.
   - 호출: `~/.claude/skills/gpt-image-bridge/bin/gpt-image-2 "<prompt>" cover_bg.png --size 1024x1536`
   - 결과 해상도: 1024×1536 (모델 기본 세로 비율)

**영어 프롬프트 (배경 전용, 텍스트 없음):**
```
Minimalist editorial book-cover background artwork, vertical portrait composition,
no text no letters no numbers no logos no words anywhere in the image. Deep cold
charcoal-navy background (#12141c fading to #1b2030), subtle flat color, no noisy
gradient. In the lower two-thirds of the frame: a single thin precise straight line
rises from the bottom edge and forks cleanly into three diverging straight lines at
a sharp angle, like a schematic decision diagram or a minimalist circuit-free
branch/fork symbol, rendered as crisp cold white hairline strokes on the dark
background. Two of the three branches fade to a faint thin gray and stop short; one
branch is rendered bold and continues further, marked with a single muted warm
copper/amber accent line, implying a chosen path among options. Extremely minimal
flat vector-like design, geometric precision, generous empty negative space in the
entire top third of the frame and along the very bottom margin for later text
overlay. No robots, no human faces, no brains, no circuit-board texture, no glowing
neon, no generic blue tech gradient, no stock-photo look. Mood: austere, analytical,
calm, confident, cold-blooded decision-making. Sharp lines, high contrast,
print-quality, portrait aspect ratio close to 1:1.6.
```

결과: 배경 밑동에서 하나의 흰 선이 올라오다가 세 갈래로 갈라지고, 그중 한 갈래만
코퍼/앰버 색으로 강조되어 이어지는 다이어그램. 상단 1/3과 하단부에 텍스트를 얹을
여백이 의도대로 확보됨. 클리셰(로봇·뇌·회로기판·파랑 그라데이션) 전혀 없음.

## 한글 텍스트 합성 (ImageMagick)

이미지 모델의 한글 렌더링 신뢰도가 낮아 제목·부제·저자명은 전량 ImageMagick으로
후합성했다.

- **폰트:** `/System/Library/Fonts/AppleSDGothicNeo.ttc` (시스템 기본 폰트, 직접 경로
  지정). `fc-list`로는 Bold/Heavy 등 named face가 조회되지만, 이 ImageMagick 빌드는
  fontconfig 이름 매칭이나 `.ttc[index]` 문법을 지원하지 않아 (`unable to read font`
  오류) 기본 face(Regular)만 사용 가능했다. 제목은 `-stroke white -strokewidth 1.5`로
  획을 두껍게 만드는 파우폭스(faux-bold) 기법으로 굵기를 보완.
- **캔버스 합성 순서:**
  1. gpt-image-2 배경(1024×1536)을 `-resize 1600x2400!`로 정확히 스케일(가로세로
     비율이 정확히 1.5625배로 일치해 왜곡 없음)
  2. `-gravity North -background "srgb(19,22,34)" -extent 1600x2560`으로 하단에
     160px 여백 추가 (다이어그램 배경색과 동일한 색으로 이음매 없이 확장 — 다이어그램의
     세로선이 정확히 이 확장 경계(y=2400)에서 끝나, 하단 확장 영역은 완전히 비어
     저자명 배치에 안전함을 픽셀 단위로 확인)
  3. 제목 2줄 + 부제 1줄을 상단 여백(다이어그램 최상단 갈래 끝 y≈508px 이전, 클리어
     존 0~480px)에 배치
  4. 저자명 "Toby-AI"를 하단 확장 여백에 배치

**최종 합성 명령:**
```bash
FONT="/System/Library/Fonts/AppleSDGothicNeo.ttc"
magick cover_canvas.png \
  -gravity North \
  -font "$FONT" -pointsize 108 -fill white -stroke white -strokewidth 1.5 \
  -annotate +0+130 "AI 에이전트," \
  -annotate +0+270 "무엇으로 갈리나" \
  -stroke none \
  -font "$FONT" -pointsize 38 -fill "#e8935a" \
  -annotate +0+420 "프레임워크 · 데이터 · 평가 · 런타임 선택 가이드" \
  -gravity South \
  -font "$FONT" -pointsize 42 -fill "#c9cdd6" \
  -annotate +0+130 "Toby-AI" \
  cover_final.png
```

부제 색상(`#e8935a`)은 배경 다이어그램의 강조선(코퍼/앰버, 실측 RGB 약 238,145,75)과
동일 계열로 맞춰 타이포와 그래픽이 한 시스템처럼 보이게 했다.

## 검증

- `magick identify ai-agent-development/cover.png` → `PNG 1600x2560 1600x2560+0+0 8-bit sRGB`
  (요구 해상도 정확히 일치)
- `file` 명령으로 유효한 PNG(RGBA, non-interlaced) 확인
- 250×400 축소 썸네일을 직접 렌더링해 확인 — 제목 2줄과 부제가 축소 상태에서도
  선명하게 읽힘, "Toby-AI" 저자 표기도 하단에서 식별 가능
- 다이어그램 세로선의 실제 종료 y좌표(2399)를 픽셀 샘플링으로 확인해 저자명 텍스트
  (y≈2470 부근)와 겹치지 않음을 수치로 검증
- 제목·부제 상단 배치가 배경 다이어그램의 최상단 갈래 끝(y≈508)보다 위에 위치해
  겹침 없음을 픽셀 스캔으로 확인

## Result

`cover.png` — 1600×2560, gpt-image-bridge 배경 + ImageMagick 한글 타이포 합성.
