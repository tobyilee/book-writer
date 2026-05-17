# Cover Design Log

## Version 1 (2026-05-18)

- **Concept:** A — 미니멀리즘 (심볼 + 강한 타이포그래피)
- **Tool:** Pillow (Python) + Apple SD Gothic Neo Heavy/Bold
- **Output:** `cover.png` — 1600×2560 PNG

### Design Decisions

- **배경:** 딥 네이비-블랙 그라데이션 (#0d1117 → #0a1c23). 극도로 어두운 톤으로 심화 기술서 무게감 표현.
- **그리드 텍스처:** 80px 간격 미세 격자 — 데이터 구조/시스템 내부 연상. 불투명도 ~5%로 매우 은은하게.
- **메인 심볼:** B+Tree 다이어그램 추상화. 3레벨(루트 1·내부 3·리프 7노드) + 리프 노드를 가로로 연결하는 링크 바(B+Tree 시그니처). 노드 색상: 웜 앰버/골드 (#e8a838) — MySQL/InnoDB 연상.
- **좌측 액센트 바:** 8px 앰버 세로줄 — 정통 기술서 바인딩 느낌.
- **제목:** 2행 분리. "DBA처럼 생각하는"은 밝은 흰색, "스프링 개발자"는 골드 액센트. Apple SD Gothic Neo Heavy 128pt.
- **부제:** "#8eacc4" 쿨블루 — 차분한 보조 텍스트.
- **저자:** 하단 중앙 "Toby-AI", Bold 56pt.
- **금지 항목 준수:** 만화/캐릭터 없음, 공식 로고 없음, 돌고래 색 없음.

### Prompt (English, for image-gen API if needed)

```
A minimalist book cover in portrait format (1600x2560). 
Background: deep navy-black gradient, nearly black, evoking database internals.
Very faint 80px grid texture overlaid (5% opacity) to suggest structured data.
Center symbol: a clean B+Tree diagram — 3 levels, root node at top connected to 3 internal 
nodes, 7 leaf nodes at bottom linked by a horizontal bar. Node fill: warm amber-gold (#e8a838).
Edge lines in dark amber. All nodes are clean circles, no labels inside.
Left edge: a thin 8px vertical amber accent stripe spanning full height.
Typography: Main title "DBA처럼 생각하는 스프링 개발자" in two lines, 
bold Korean sans-serif, white/amber. Subtitle below top title in cool steel-blue.
Small author attribution "Toby-AI" at the very bottom center.
Thin amber horizontal rule below the title. 
Editorial, calm, authoritative. No stock photo. No gradient gimmicks. No characters.
```

### Notes

- Apple SD Gothic Neo Heavy (index 0) 사용 — 한글 렌더링 안정적
- Pillow로 직접 TTC 로딩 → ImageMagick 폴백 불필요
- 재생성 시: `/tmp/gen_cover.py` 수정 후 `/opt/homebrew/bin/python3.13 /tmp/gen_cover.py` 실행
- A/B 테스트 원한다면 Concept B(단면도형) 시도 — InnoDB 레이어 다이어그램 + 선화 스타일
