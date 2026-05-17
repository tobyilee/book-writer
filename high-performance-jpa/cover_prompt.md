# Cover Design Log

**Book:** 느린 JPA에는 이유가 있다 — Vlad의 눈으로 보는 고성능 영속성
**Author:** Toby-AI
**Audience:** JPA/Hibernate 실무 경험이 있는 미드~시니어 백엔드 개발자
**Tone:** 진단·해부. 차분하고 신뢰감 있는 기술서.

## Concepts Considered

- **A (선택):** 미니멀리즘 — 다크 네이비 베이스에 큰 한글 타이포 + 청록 가로 라인 + 어두운 골드 액센트. 코드 에디터의 거터 느낌을 좌측 골드 바로 암시. 가운데 청록 라인을 "긴 라인 → 짧은 라인 4개 → 끝 골드 점"으로 끊어 DB 라운드트립(N+1)을 추상화.
- **B (탈락):** 일러스트형 — 돋보기 또는 서버↔DB 화살표 메타포. 표지 텍스트와 시각적으로 충돌할 위험. 본문이 다루는 메타포의 폭이 넓어 한 가지를 고르면 책의 전체상을 왜곡할 우려.
- **C (탈락):** 타이포그래피 중심 — "느린" 한 글자 강조. 너무 캐주얼하고 책의 진중함과 안 맞음.

**선택 사유:** "차분한 기술서 + 심화서" 톤이라 가이드상 A. 다크 네이비 + 청록 + 어두운 골드 조합으로 코드 에디터의 진중한 분위기를 재현. 시각 메타포는 가운데 라인 패턴 하나로 강하게 압축.

## Version 1 (2026-05-17)

- **Tool:** ImageMagick 7.1.2 (한글 폰트: Pretendard Black/ExtraBold/SemiBold/Medium/Regular)
- **Palette:**
  - Background: `#0E1626` → `#152038` (vertical gradient)
  - Title (white): `#FFFFFF`
  - Teal accent (line & subtitle): `#3DD2C7`, subtitle softened to `#9BD4CC`
  - Gold accent (label/gutter/dot): `#C9A24A`
  - Muted gray: `#8FA0B8`
- **Layout:**
  - 좌측 세로 골드 바 (`80,80 → 96,2480`): 코드 에디터 거터
  - 상단 라벨: `HIGH-PERFORMANCE PERSISTENCE` (ExtraBold 60pt, gold, kerning 8)
  - 메인 타이틀 2줄: `느린 JPA에는` / `이유가 있다` (Black 168pt, white)
  - 청록 강조 라인 (y=880): 가로 1440px 연속 라인 — "보이지 않는 비용" 위의 경계
  - 가운데 N+1 스터터 라인 (y=1080): 긴 라인 → 짧은 라인 다섯 개 → 끝 골드 점 (DB 라운드트립 메타포)
  - 청록 강조 라인 (y=1240): 두 번째 경계
  - 서브타이틀: `Vlad의 눈으로 보는` / `고성능 영속성` (Medium 70pt, teal)
  - 부제 라벨: `JPA · Hibernate · JDBC` (Regular 38pt, muted)
  - 좌하단: `진단과 해부` (Medium 36pt, gold, kerning 8)
  - 우하단: `Toby-AI` (SemiBold 56pt, white)
- **ImageMagick command:**

  ```bash
  FONT_DIR="$HOME/Library/Fonts"

  # 1) Gradient base
  magick -size 1600x2560 gradient:'#0E1626-#152038' base.png

  # 2) Gold gutter + teal lines + N+1 stutter pattern
  magick base.png \
    -fill '#C9A24A' -draw "rectangle 80,80 96,2480" \
    \( -size 1440x4 xc:'#3DD2C7' \) -geometry +80+880 -composite \
    \( -size 1440x4 xc:'#3DD2C7' \) -geometry +80+1240 -composite \
    -fill '#3DD2C7' -draw "rectangle 200,1080 380,1096" \
    -fill '#3DD2C7' -draw "rectangle 420,1080 520,1096" \
    -fill '#3DD2C7' -draw "rectangle 560,1080 600,1096" \
    -fill '#3DD2C7' -draw "rectangle 640,1080 680,1096" \
    -fill '#3DD2C7' -draw "rectangle 720,1080 760,1096" \
    -fill '#C9A24A' -draw "rectangle 780,1082 820,1094" \
    base_lined.png

  # 3) Typography composition
  magick base_lined.png \
    -font "$FONT_DIR/Pretendard-ExtraBold.otf" \
    -pointsize 60 -fill '#C9A24A' -kerning 8 \
    -gravity NorthWest -annotate +160+220 "HIGH-PERFORMANCE PERSISTENCE" \
    -font "$FONT_DIR/Pretendard-Black.otf" \
    -pointsize 168 -fill '#FFFFFF' -kerning -2 \
    -gravity NorthWest -annotate +160+360 "느린 JPA에는" \
    -annotate +160+560 "이유가 있다" \
    -font "$FONT_DIR/Pretendard-Medium.otf" \
    -pointsize 70 -fill '#9BD4CC' -kerning 0 \
    -gravity NorthWest -annotate +160+1340 "Vlad의 눈으로 보는" \
    -annotate +160+1440 "고성능 영속성" \
    -font "$FONT_DIR/Pretendard-Regular.otf" \
    -pointsize 38 -fill '#8FA0B8' -kerning 2 \
    -gravity NorthWest -annotate +160+1600 "JPA · Hibernate · JDBC" \
    -font "$FONT_DIR/Pretendard-SemiBold.otf" \
    -pointsize 56 -fill '#E8EEF7' -kerning 4 \
    -gravity SouthEast -annotate +120+180 "Toby-AI" \
    -font "$FONT_DIR/Pretendard-Medium.otf" \
    -pointsize 36 -fill '#C9A24A' -kerning 8 \
    -gravity SouthWest -annotate +160+200 "진단과 해부" \
    cover.png
  ```

- **Result:** `cover.png` (1600×2560, PNG, ~216 KB)
- **Validation:**
  - 해상도 1600×2560 정확
  - 200×320 썸네일에서도 메인 타이틀·서브타이틀·저자명 모두 식별됨
  - 저자 표기 `Toby-AI` 우하단에 명시
  - 클리셰 회피 (스톡 사진 없음, 기본 그라데이션 아님)
- **English prompt equivalent (for future image-gen MCP regeneration):**

  > A minimalist editorial book cover, portrait 1600x2560. Dark navy background
  > (`#0E1626`→`#152038` vertical gradient). Thin vertical gold bar on the left
  > edge evoking a code editor gutter. Upper third: bold Korean title "느린
  > JPA에는 이유가 있다" in heavy white sans-serif (Pretendard Black), two lines,
  > preceded by a small gold tracking-out label "HIGH-PERFORMANCE PERSISTENCE".
  > Center: two horizontal teal (`#3DD2C7`) accent lines bracketing a stuttered
  > teal line pattern — one long segment followed by four short segments and a
  > gold dot, abstractly representing N+1 database round trips. Lower third:
  > teal subtitle "Vlad의 눈으로 보는 고성능 영속성" in medium weight, muted
  > gray label "JPA · Hibernate · JDBC". Bottom-left: small gold caption
  > "진단과 해부". Bottom-right: "Toby-AI" in white semibold. Contemplative,
  > diagnostic, confident. No stock photography, no generic tech gradient, no
  > rocket/gears/cloud clichés.

## Notes

- 메타포: 좌측 골드 거터(에디터) + 가운데 스터터 라인(N+1) — 두 시각 단서로 책의 핵심 주제(영속성 계층의 보이지 않는 비용 진단)를 압축.
- 색 배합은 코드 에디터의 다크 테마(예: Solarized Dark, Dracula의 진중한 변형)와 비슷한 인지 신호를 노려 대상 독자가 "내 책"이라고 느끼게 함.
- 재생성 필요 시: 이 파일의 ImageMagick 블록을 그대로 재실행. 콘셉트 변경 요청 시 B(돋보기 일러스트) 또는 C(타이포 강조) 안으로 분기.
