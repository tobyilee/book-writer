# Cover Design Record — 나노챗 해부학

## 선택한 컨셉
**컨셉 1: 신경망의 분해도(exploded view).** GPT 블록 하나를 부품(Embedding · RMSNorm · Self-Attention(Q/K/V/RoPE) · MLP · residual ⊕) 단위로 공중에 띄운 자동차 카탈로그 스타일의 분해도. 1점 투시로 깊이감 확보.

컨셉 2(흐릿한 코드 배경 + 굵은 타이포)는 썸네일 가독성이 떨어져 탈락. 분해도는 책의 정체성(`8K LOC를 부품 단위로 해부`)을 즉시 드러낸다.

## 사용 도구
**SVG 직접 설계 → `rsvg-convert`로 PNG 렌더.** 외부 이미지 생성 MCP/API 없이 결정론적 출력. 시스템에 ImageMagick은 없었지만 `librsvg`가 설치되어 있어 SVG → PNG 1600×2560 변환에 사용. 한글은 시스템 폰트(Pretendard, Apple SD Gothic Neo)와 JetBrains Mono를 SVG `font-family`로 참조.

## 디자인 사양

### 팔레트
- 베이스: `#F8F6F1` (오프 화이트, 페이퍼 그라데이션으로 `#FAF8F3` → `#F4F1E8`)
- 강조 1: `#1E3A5F` (딥 블루 — 제목·다이어그램 선·코드 띠)
- 강조 2: `#D4A52A` (머스타드 옐로 — 라벨 도트, 액센트, ReLU² · Q/K/V 박스, 코너 마크)
- 보조: `#7A7A7A` (그레이 — 부제·캡션·우상단 메타)

### 타이포
- 메인 타이틀: Pretendard Black 200pt, letter-spacing -12 (자간 좁힘)
- 부제 한글: Pretendard Medium 42pt
- 부제 영문: JetBrains Mono Italic 32pt
- 코드 라인: JetBrains Mono Medium 32pt (반전, 흰색 on 딥 블루)
- 다이어그램 라벨: JetBrains Mono 20–26pt + Pretendard Light 한글 캡션

### 레이아웃
- 상단 1/3 (y 120–800): 시리즈 라벨, 제목 2줄, 부제 2줄
- 중앙 1/2 (y 900–2120): GPT 블록 분해도 (residual stream 점선이 vertical spine)
- 하단 (y 2240–2400): 강조 코드 라인 + 캡션 + 저자 + 푸터

### 분해도 부품 (위에서 아래로)
1. Token Embedding (`wte[input_ids]`) — `EMB · 어휘 → 벡터`
2. RMSNorm — `NORM · 정규화`
3. Causal Self-Attention (Q/K/V/RoPE 4개 서브 박스) — `ATTN · 문맥 응시`, `QKV · 질의·열쇠·값`
4. ⊕ residual
5. RMSNorm (두 번째)
6. MLP (Linear↑ → ReLU² → Linear↓) — `MLP · 사고 회로`
7. ⊕ residual
8. `× N layers` 인디케이터

## 산출
- `cover.png` (1600 × 2560, PNG, ~190 KB)
- `cover.svg` (소스, 재생성·A/B 테스트용으로 보존)

## 재생성 명령
```bash
cd nanochat-llm-book && rsvg-convert -w 1600 -h 2560 -f png -o cover.png cover.svg
```

## A/B 대안 메모
- 컨셉 2(흐릿한 코드 배경)는 보류. 만약 시리즈 다음 권에서 변주가 필요하면 이쪽을 시도.
- 머스타드 옐로 액센트의 강도가 부담스러우면 `#D4A52A` → `#C9A14A`로 한 단계 차분하게 톤다운 가능.
- 분해도를 isometric(완전 측면)으로 바꾸면 더 도감 느낌이 강해지지만 현재 1점 투시 정도가 친근함과 정밀함 사이의 균형으로 적절.
