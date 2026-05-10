# Cover Design — 수집을 지식으로

## 책 정보
- 제목: 수집을 지식으로
- 부제: 50대 개발자를 위한 PKM 다시 짜기
- 저자: Toby-AI
- 장르: 에세이형 기술서 (실전 가이드 + 사고 에세이)
- 대상: 50대 개발자, Google Docs/Obsidian 사용자

## 콘셉트 3안

### 안 1 (채택): 연결의 빛 (Network of Light)
- 다크 네이비(#0E1B2C) 배경에 미니멀한 노드 네트워크
- 흩어진 점들이 서로 연결되며 한 점에서 앰버(#E8B86E) 빛이 피어남
- 좌측 상단·우측 하단으로 자연스럽게 흐르는 구성
- 제목이 중앙에 우직하게 자리 잡고 노드는 배경 레이어로 작동

### 안 2: 정돈된 노트 더미 (Folded Knowledge)
- 다크 그린(#1F3A2E) 배경, 단순화된 종이/카드 더미 실루엣
- 더미 위에서 한 줄기 빛이 솟아오르며 테라코타로 전이
- 좀 더 따뜻한 느낌, 다만 너무 일러스트레이션 같아질 위험

### 안 3: 타이포그래피 단독
- 제목 글자 자체를 그래프 노드처럼 변형
- 색은 안 1과 동일
- 가장 미니멀하지만 50대 독자에게 가독성 위험

→ **안 1 채택**: "수집"이 흩어진 점들, "지식"이 연결된 그래프로 표현 가능. 책의 핵심 메시지(연결·통합)를 시각적으로 직접 전달.

## 영문 프롬프트 (외부 이미지 생성 도구 사용 시 참고용)
```
Minimalist book cover, 1600x2560 portrait format.
Deep navy background (#0E1B2C) with subtle gradient toward darker corners.
A constellation of small dots scattered across the upper-left third —
some isolated, some connected by thin amber lines (#E8B86E),
forming a sparse network graph that suggests "connecting collected fragments
into knowledge." The right-bottom area has a soft amber glow emerging,
as if light is being born from connection.
Clean, intellectual, calm. No clutter, no clichés like brain-icons or lightbulbs.
Korean book title set in large weight at the upper-center,
subtitle smaller below, author name "Toby-AI" at the bottom.
Inspired by The Pragmatic Programmer + Susan Kare minimalism.
```

## 실제 생성 방법
PIL 기반 타이포그래피 + 절차적 노드 그래프로 직접 렌더링.
이미지 생성 API 미연결 환경에서도 안정적인 결과를 얻기 위함.
폰트: AppleSDGothicNeo (한글), 색: 네이비 베이스 + 앰버 포인트.

## 색 팔레트
- 배경 베이스: `#0E1B2C` (deep navy)
- 배경 그라디언트 끝: `#070E18` (near black)
- 포인트 1: `#E8B86E` (amber, 제목·노드 빛)
- 포인트 2: `#C97B5A` (terracotta, 부제 강조)
- 텍스트 보조: `#D8DEE9` (mute white, 부제·저자명)
- 노드 베이스: `#3A5575` (muted blue, 연결 안 된 점들)

## 레이아웃 (1600x2560)
- 0–600px: 노드 네트워크 (좌측 강조, 우측 페이드)
- 600–900px: 메인 제목 "수집을 지식으로" (96pt bold)
- 920–1020px: 구분선 + 부제 "50대 개발자를 위한 PKM 다시 짜기" (44pt)
- 1020–2200px: 호흡 공간 + 미세한 노드 그래프
- 2200–2400px: 앰버 글로우 (연결의 빛이 피어나는 영역)
- 2400–2560px: 저자명 "Toby-AI" (40pt, 우측 정렬)
