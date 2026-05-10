# Cover Design Log — 잊지 않는 기술

## Concept Brainstorm

세 가지 안을 검토함.

- **A (선택). 미니멀리즘 + 심볼:** 딥 네이비 그라디언트 위에 고전 아치형 주랑(portico) 실루엣, 키스톤 위로 골드 노드가 별자리/신경망처럼 뻗어나감. 상단 1/3에 큰 한글 타이포. "고대 기억의 궁전 + 현대 AI 네트워크"의 메타포가 한 장면에 응축.
- **B. 일러스트형:** 기억의 궁전 외관과 디지털 격자가 합성된 풍경 일러스트. 톤이 강해지지만 자기계발서/판타지 느낌으로 흐를 위험.
- **C. 타이포그래피 중심:** 제목 글자 자체가 아치 형태를 만들고 일부가 노드/연결선으로 변형. 한글 자모로 그래픽을 짜면 가독성 위험.

→ 교양 과학서 톤 + 시중의 자기계발성 기억법 책과 차별화하려는 목적에 가장 잘 맞는 **콘셉트 A**를 선택.

## Version 1 (2026-05-10)

- **Concept:** A (Minimalism + classical arch + neural constellation)
- **Tool:** Python PIL (Pillow). 외부 이미지 생성 API/MCP가 가용하지 않아 vector-style 합성으로 직접 렌더. 한글 타이포 안정성·재현성 우선.
- **Resolution:** 1600 × 2560 (1.6:1, EPUB 표준 비율)
- **Palette:**
  - 배경: 딥 네이비 (#0F122A → #20184) 세로 그라디언트 + 비네팅
  - 포인트: 워밊 골드/앰버 (#D4A860, dim #8C6E3C)
  - 타이포: 워밎 화이트 (#F5F0E8), 라벤더 부제 (#B4A5C8)
- **Composition:**
  - 상단 1/3: 작은 라벨 "MEMORY · 기억 설계" + 좌우 골드 horizontal rule
  - 상단~중앙: 타이틀 2줄 — "잊지 않는"(흰색) / "기술"(골드, 강조). Heavy weight 220pt, AppleSDGothicNeo Heavy.
  - 타이틀 아래: 부제 "기억의 궁전부터 AI 카드까지" (라벤더, 64pt) + 짧은 골드 룰
  - 중·하단: 4기둥 + 아치 + 키스톤 형태의 고전 주랑 실루엣 (골드 윤곽선)
  - 아치 키스톤 위쪽: 18개 골드 노드가 별자리/신경망처럼 위로 뻗어나가며 가는 골드 라인으로 연결, 가벼운 글로우와 가우시안 블러
  - 배경: 상단 0~65% 영역에 희미한 별점 180개로 텍스처
  - 하단 180px: 저자 "Toby-AI" (Medium 48pt, 흰색)
- **Image generation prompt (참고용 — 외부 모델로 재생성 시 영문 프롬프트):**
  ```
  A minimalist Korean book cover, portrait 1600x2560.
  Background: deep navy to dark purple vertical gradient with soft vignette,
  faint star particles in upper half. Center-lower: a classical Greco-Roman
  portico silhouette with four slim columns and an arched top, rendered as
  thin warm gold outlines (no fill, no photorealism). At the keystone of the
  arch, a soft golden glow. Above the arch, a sparse neural-network
  constellation: ~18 small gold nodes connected by thin gold lines, fanning
  upward like memory pathways or stars. Top third: title in bold modern
  Korean sans-serif, "잊지 않는" in warm white, "기술" in gold, two lines.
  Below title: subtitle "기억의 궁전부터 AI 카드까지" in muted lavender.
  Small gold rule. Bottom: small "Toby-AI" in white. Editorial, intellectual,
  slightly mystical, like a thoughtful science non-fiction cover. No stock
  photography, no generic tech gradient, no busy ornament.
  ```

## Verification Checklist

- [x] 해상도 1600 × 2560 (PNG, 8-bit RGB)
- [x] 썸네일(≈250×400) 축소 후에도 제목·부제 읽힘 — 확인 완료
- [x] 저자 표기 "Toby-AI" 하단 명시
- [x] 클리셰 회피: 일반적 테크 그라디언트 ✗, 스톡사진 톤 ✗, 자기계발서식 굵은 빨간 띠 ✗
- [x] EPUB 비율 1.6:1 충족

## 재생성·A/B 포인트

- 콘셉트 변경 요청 시: B(풀 일러스트), C(타이포 그래픽)부터 다시 시작
- 같은 콘셉트 내 조정: 재생성 스크립트 `_make_cover.py`의 색·노드 수·아치 비율·폰트 크기 인자만 변경
- 외부 이미지 모델(MCP/DALL-E 계열) 가용해지면 위 영문 프롬프트로 v2 생성 후 비교
