# Cover Design Log

## Version 1 (2026-10-19)

- Concept: **A (미니멀리즘 — 심볼 하나 + 큰 타이포)**. 심볼은 책의 핵심 이미지인 여섯 노드 루프(Plan → Design → Build → Test → Deploy → Maintain ↺). 단계 사이 아티팩트(`intent.md` → `spec.md` → `plan.md + diff` → `tests pass` → `PR + REVIEW.md` → `new intent.md`)를 링 안쪽에 작은 모노 라벨로 배치하고, 루프를 닫는 마지막 호(MAINTAIN → PLAN)만 강조색으로 칠해 "원이 닫힌다"를 보여 준다. 루프 위에 얇은 수평선과 "The loop keeps running. Human judgement stays above it." 문구를 두어 "사람의 판단이 루프 위에 머문다"를 구도로 표현했다.
- Tool: **imagemagick** (ImageMagick 7.1.2, draw primitives + 분리한 시스템 폰트). 이미지 생성 MCP·외부 API는 이 세션에 없어 처음부터 타이포·다이어그램 표지로 설계했다 — 폴백이 아니라 의도된 선택에 가깝다.
- Fonts: Apple SD Gothic Neo Heavy(제목)·Medium(부제·저자), Menlo Bold(단계 라벨·상단 태그), D2Coding(아티팩트 라벨·중앙 `intent.md` 텍스처). `.ttc`에서 fontTools로 face를 분리해 사용(ImageMagick이 `.ttc`의 첫 face만 읽기 때문).
- Palette: 바탕 `#13203A → #0A1020` 방사형 그라데이션 + 8~10% 점 격자, 잉크 `#EEF2F7`/`#B9C4D3`, 링 `#2E3F5C`, 강조색 하나 **앰버 `#F2A93B`**.
- Prompt (이미지 모델이 생기면 재생성용):
  ```
  A minimalist book cover in portrait format (1600x2560), calm engineering mood.
  Background: deep navy, almost black, with a faint dot grid like graph paper.
  Top-left small monospace tag in amber: "PLAYBOOK / 12 PLAYS / 6 STAGES".
  Title in the upper third, left-aligned, heavy Korean sans-serif in white,
  two lines: "AI 네이티브" / "SDLC 플레이북". Below it a medium-weight subtitle in light grey:
  "Claude Code로 내 개발 루프를 / 다시 짜는 12가지 플레이".
  Center-bottom: a single abstract diagram — six small hollow nodes evenly spaced on a thin
  muted-blue circle, labelled in spaced monospace caps PLAN, DESIGN, BUILD, TEST, DEPLOY,
  MAINTAIN; small chevrons show clockwise flow; tiny monospace file names inside the ring
  (intent.md, spec.md, plan.md + diff, tests pass, PR + REVIEW.md, new intent.md).
  Only the final arc from MAINTAIN back to PLAN and the PLAN node are amber — the loop closes.
  Above the circle a thin horizontal rule with a small amber ring on it and the monospace line
  "The loop keeps running. Human judgement stays above it."
  Bottom center: "Toby-AI" small. Editorial, confident, quiet.
  No robots, no brains, no glowing AI clichés, no stock gradients, no logos.
  ```
- Result: `cover.png` (1600×2560, sRGB PNG). 재현 스크립트: `cover_build.py` (폰트 경로는 스크래치패드 기준이라 재실행 시 `.ttc` 분리 단계가 먼저 필요).
- Notes:
  - 200×320 썸네일에서 제목 두 줄·루프·앰버 호가 읽힘. 아티팩트 라벨은 썸네일에서는 질감으로만 보이며 의도한 바.
  - 한글은 Apple SD Gothic Neo로 정확히 렌더됨(깨짐 없음).
  - 제안 대체 텍스트(`book_manifest.json`의 `cover_alt`, 매니페스트는 editor 단계에서 생성되므로 그때 반영):
    `AI 네이티브 SDLC 플레이북 표지 — 짙은 남색 바탕 위에 Plan·Design·Build·Test·Deploy·Maintain 여섯 노드가 원을 이루는 개발 루프 다이어그램, 루프를 닫는 마지막 호만 앰버색`
