# 표지 디자인 기록 — 왜 TypeScript는 이렇게 생겼는가

생성일: 2026-05-04
도구: Python Pillow 12.0.0 (ImageMagick 미설치로 Pillow 사용)
출력: cover.png (1600 × 2560 px, PNG)

---

## 선택한 콘셉트: 미니멀리즘 기하학형

### 콘셉트 3안 비교

| 안 | 방향 | 이유 |
|----|------|------|
| **1 (채택)** | 짙은 남색 배경 + 기하학 도형(전환 흐름) + 큰 한글 제목 | 진지하고 절제된 기술서 톤. "왜?"를 물음표 시각 요소로 표현 |
| 2 | TS 파란색 단색 배경 + 타이포그래피 중심 (제목만) | 지나치게 단순 — 부제 정보가 묻힐 우려 |
| 3 | 흑백 + 코드 스니펫 배경 워터마크 | 개발자 감성이나 출판 썸네일 가독성이 떨어질 위험 |

---

## 디자인 상세

### 색상 팔레트

| 역할 | 색상 | HEX |
|------|------|-----|
| 배경 | 짙은 남색 | #0A0E1C |
| TS 블루 (악센트) | TypeScript 공식 색 | #3178C6 |
| TS 블루 라이트 | TS 원 텍스트 | #64AAF0 |
| Java/Kotlin 호박색 | 전환 출발점 강조 | #E89628 |
| 제목 | 흰색 | #FFFFFF |
| 부제/저자 | 연회색 | #B4B9C8 |
| 그리드 (배경) | 극도 어두운 남색 | #141C32 |

### 레이아웃 (위 → 아래)

1. **상단 TS 블루 바** (8px) — 브랜드 악센트
2. **배경 그리드** — 80px 간격 미묘한 격자, 기술서 감각
3. **전환 흐름 도형** (y≈920) — Java/Kotlin 원(호박) → 점선 화살표 + "?" → TypeScript 원(파랑)
4. **수평 구분선** (TS 블루)
5. **메인 타이틀 2줄** (y≈1200)
   - "왜 TypeScript는" — AppleSDGothicNeo ExtraBold 110pt
   - "이렇게 생겼는가" — 동일
6. **부제** — "Java/Kotlin 개발자를 위한 언어와 생태계 전환서" 42pt Medium
7. **저자명** — "Toby-AI" 하단 중앙
8. **하단 TS 블루 바** (8px) — 상단과 대칭

### 폰트

| 용도 | 폰트 | 인덱스 | 크기 |
|------|------|--------|------|
| 메인 제목 | AppleSDGothicNeo.ttc | 7 (ExtraBold) | 110pt |
| 부제 | AppleSDGothicNeo.ttc | 3 (Medium) | 42pt |
| 저자 | AppleSDGothicNeo.ttc | 2 | 38pt |
| 도형 레이블 | AppleSDGothicNeo.ttc | 6/3 | 24-36pt |
| 모노 레이블 | Menlo.ttc | 0 | 28pt |

---

## 재생성 / A/B 테스트 메모

- 부제 폰트를 더 밝게(WHITE) 바꾸면 대비가 강해진다
- 배경을 #0D1117(GitHub Dark)로 바꾸면 GitHub 친화적 톤
- 전환 도형 대신 TypeScript 로고 SVG를 래스터화해 삽입하면 브랜드 인지도 향상
- 이미지 생성 API(DALL-E/gpt-image-1) 사용 시 권장 프롬프트:
  > "Minimalist book cover for a technical programming book titled '왜 TypeScript는 이렇게 생겼는가' (Why does TypeScript look like this?). Dark navy blue background (#0A0E1C), TypeScript blue (#3178C6) accent bars at top and bottom. Center: two circles connected by a dashed arrow — left circle in amber/orange representing Java/Kotlin, right circle in blue representing TypeScript, with a white question mark between them symbolizing inquiry. Large white Korean title text at center, smaller gray subtitle below. Clean geometric minimalism. Portrait 1600x2560."
