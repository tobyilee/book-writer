# Cover Design — 개발자를 위한 학습의 기술

## 책 정보
- 제목: 개발자를 위한 학습의 기술
- 부제: 새 기술을 빠르게 흡수하는 시스템
- 저자: Toby-AI
- 대상 독자: 주니어~시니어 개발자 (새 기술/프레임워크/도메인 흡수가 필요한 모든 직군)
- 톤: 진중한 실무 자기계발서, O'Reilly·인사이트 출판사 매대 톤

## 콘셉트 3안

### A안 (채택) — 절제된 타이포 + 미세 노드 그래프
- 차분한 다크 네이비 배경 (#0F1729)
- 한국어 굵은 산세리프 (Apple SD Gothic Neo Bold)
- 강조색: 앰버 노랑 (#F5A524) — 부제 + 강조 라인 1줄
- 배경에 미세한 라인 그래프(노드 + 연결선) — 학습 회로 메타포, 채도 낮춰 배경 텍스처 수준
- 제목이 표지의 50% 이상, 부제는 작게 위, 저자는 하단

### B안 — 사다리 모티프
- 다크 모노톤에 단계적으로 올라가는 추상 사다리/계단
- 타이포 중심이지만 모티프가 더 강함

### C안 — 마인드맵 한 장
- 가운데 굵은 점 → 방사형 미세 라인
- 너무 추상적이라 메시지 약함, 패스

## 채택 근거
A안: 회로/노드 모티프가 "학습은 시스템이다" 메시지와 정확히 맞물리고, 타이포 우선이라 썸네일에서도 제목이 살아남음. O'Reilly·인사이트 톤에 가장 가까움.

## 색 팔레트
- Background: #0F1729 (deep navy)
- Title text: #F5F7FA (off-white)
- Subtitle text: #F5A524 (amber)
- Accent line: #F5A524
- Graph nodes/lines: #1F2A44 ~ #2C3A5C (배경보다 살짝 밝은 톤, 텍스처)
- Author text: #8B95A8 (muted)

## 타이포그래피
- 제목: Apple SD Gothic Neo Bold, 약 200pt, 2줄 분리 ("개발자를 위한" / "학습의 기술")
- 부제: Apple SD Gothic Neo Medium, 약 60pt, 앰버 컬러
- 저자: Apple SD Gothic Neo Light, 약 50pt
- 라벨: "PRACTICAL GUIDE" 같은 영문 small caps 배지 상단 (선택)

## 산출
- 파일: cover.png (1600x2560, 5:8 책 비율)
- 생성 방법: Python + PIL/Pillow (이미지 생성 MCP 미가용으로 fallback)
- 폰트: /System/Library/Fonts/AppleSDGothicNeo.ttc

## 재생성 시 변경 후보
- 강조색을 전기 블루(#3B82F6)나 네온 그린(#10B981)으로 교체 가능
- 노드 그래프 대신 사다리/계단 라인으로 교체 (B안)
- 영문 부제 추가 ("The System for Learning Faster")
