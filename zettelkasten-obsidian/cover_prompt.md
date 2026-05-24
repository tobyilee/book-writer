# Cover Design Log — 생각의 상자

## 책 정보
- 제목: 생각의 상자
- 부제: 루만의 쪽지 상자에서 Obsidian까지, 연결로 사고하는 법
- 저자: Toby-AI
- 주제: Zettelkasten 방법론 + Obsidian 실천법 (외부화된 사고, 연결로 사고하기, 노트의 가치사슬)
- 분위기: 비학술적·사려 깊고 영감을 주는, 따뜻하면서 지적인
- 대상: 개발자·작가·강사·연구자·창작자·평생학습자

## 콘셉트 3안
- **A 미니멀리즘** — 심볼 하나(상자) + 큰 타이포. 차분.
- **B 일러스트형** — 카드·쪽지가 선으로 연결돼 별자리/네트워크로 창발하는 메타포.
- **C 타이포 중심** — 제목 자체가 그래픽.

## 채택안: A + B 혼합
미니멀한 구도 위에, 상자(Zettelkasten)에서 쪽지 카드가 떠오르며 링크로
연결되어 별자리처럼 창발하는 장면을 추상적으로 렌더링.
"외부화된 사고가 연결로 자라난다"는 책의 핵심 은유를 그대로 시각화.
전구·뇌 클리셰 회피. 따뜻한 종이 톤 + 깊은 잉크 블루 + 뮤트 골드.

## Version 1 (2026-05-25)
- Concept: A+B 혼합 (constellation rising from an open box)
- Tool: ImageMagick 7.1.2 + Python (절차적 노드·링크 생성, `build_cover.py`)
  - 이미지 생성 MCP/외부 API 미연결 → 절차적 벡터 렌더링으로 실제 디자인 표지 생성 (단순 플레이스홀더 아님)
- 폰트: Pretendard (Black=제목, Light=부제, SemiBold=저자) — 모던 한글 산세리프
- 팔레트:
  - 배경 그라데이션: `#10182b` → `#1c2a44` (deep ink blue → midnight)
  - 종이 카드: `#ece3d4` / `#c9bda6` (warm paper)
  - 핵심 링크·악센트: `#c9a25b` (muted gold)
  - 보조 링크: `#5b6b8a` (cool slate)
- 구도:
  - 제목 "생각의 / 상자" — 상단 1/3, Pretendard Black 300pt, 고대비 아이보리(`#f1e8d8`)
  - 부제 — 제목 하단, 골드 66pt 2줄
  - 메타포 — 화면 하단 중앙 열린 상자에서 쪽지 카드 16장이 부채꼴로 떠오르며 골드/슬레이트 링크로 연결 (별자리/네트워크 창발)
  - 저자 "Toby-AI" — 하단 중앙, SemiBold 58pt
  - radial vignette로 가장자리 어둡게 → 중앙 집중
- 재현성: `random.seed(42)` 고정 → 동일 입력 시 동일 표지
- 검증:
  - [x] 해상도 1600×2560 (8-bit sRGB)
  - [x] 썸네일(220×352)에서 제목 가독 확인
  - [x] 저자 표기 존재 (Toby-AI)
  - [x] 클리셰 회피 (전구·뇌 없음, 기본 그라데이션 아님, 의미 있는 메타포)
- Result: cover.png
- Notes: 1차 빌드는 상자가 작고 제목-메타포 간 여백 과다 → 박스 확대(290×188),
  카드 산포 영역 상향(y≥1230), 박스 앵커 0.70→0.74로 조정해 균형 개선.

## 재생성 방법
```bash
cd zettelkasten-obsidian
python3 build_cover.py   # _layer.png 생성
# 이후 위 magick 합성 명령으로 타이포 합성 → cover.png
```
콘셉트 변경 시 build_cover.py의 노드 수(n_cards)·팔레트·박스 형태 수정.
