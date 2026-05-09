# Cover Design Notes — 직접 짜본 사람을 위한 Spring Batch 6

## 책 정보
- 제목: 직접 짜본 사람을 위한 Spring Batch 6
- 부제: 첫 잡부터 운영까지
- 저자: Toby-AI
- 대상 독자: Spring/Spring Boot 숙련 백엔드 개발자, 배치 처리 입문자
- 분위기: 실용적이고 진중한 기술서. "처음 접하는 사람도 운영까지 갈 수 있다"는 자신감과 안정감.

## 콘셉트 3안

1. **타이포그래피 + 청크 파이프라인** (선정)
   - 다크 네이비 그라데이션 배경
   - READ → PROCESS → WRITE 청크 박스가 가로로 흐르는 파이프라인 모티브 (배치의 핵심 개념)
   - 굵은 흰색 한글/영문 제목 + Spring 그린 부제·언더라인
   - 본문 코드 스니펫 패널(@Bean Job ...)을 표지에 노출 — "직접 짜본 사람을 위한"이라는 핸즈온 톤 강조
   - Spring 리프 모티브를 우하단 배지로 작게 사용

2. **Spring 리프 미니멀** (대안)
   - 중앙에 큰 Spring 잎 실루엣 + 그 위에 격자 그리드(배치 큐 상징)
   - 제목·부제만 위/아래로 배치
   - 더 정적이고 미니멀한 톤. 1안보다 정보량 적음.

3. **터미널/로그 모티브** (대안)
   - 검은 배경 + 형광 그린 텍스트로 잡 실행 로그(`Step 'paymentSettlementStep' completed in 12s`) 같은 표지
   - 운영 친화적 톤이 강하지만 입문자에게는 부담스러울 수 있음.

## 사용한 이미지 생성 방법

- 이미지 생성 MCP/HTTP API 미설치 → Python PIL 폴백
- 폰트:
  - Apple SD Gothic Neo (`/System/Library/Fonts/AppleSDGothicNeo.ttc`) — 한글
  - Helvetica (`/System/Library/Fonts/Helvetica.ttc`) — 영문/숫자
- 스크립트: `spring-batch-6/_make_cover.py` — 재실행 가능
- 색상 팔레트:
  - 배경: `#0C1426` → `#1C2638` 세로 그라데이션
  - Spring 그린: `#6DB33F` (포인트), `#94E273` (밝은 액센트)
  - 화이트 제목: `#F5F5F5`
  - 회색 보조 텍스트: `#AAB4BE`, `#5F6E82`

## 영어 프롬프트 초안 (이미지 생성 모델 사용 시 참고)

```
A professional Korean tech book cover, 1600x2400 portrait, dark navy
gradient background (#0C1426 to #1C2638) with a faint grid overlay.
Top: small uppercase tag "BACKEND · BATCH PROCESSING · SPRING ECOSYSTEM"
in dim gray, with a thin Spring green (#6DB33F) accent line below.
Center: bold white English title "Spring Batch 6" with the Korean
pre-title "직접 짜본 사람을 위한" above it, and the Korean subtitle
"첫 잡부터 운영까지" in Spring green below an underline accent.
Middle band: a horizontal pipeline of nine rounded chunk boxes —
three READ chunks, three PROCESS chunks (highlighted in green), three
WRITE chunks — connected by green arrows, captioned "Chunk-Oriented
Processing".
Below: a code editor panel with traffic-light dots, showing a small
Java snippet defining a Spring Batch Job using JobBuilder, with subtle
syntax highlighting.
Bottom: thin Spring green divider, the author name "Toby-AI" in bold
white Helvetica, "지음" beneath in gray, a small Spring leaf badge in
the bottom-right corner, and the footer "Book Writer Harness v1.0".
Style: O'Reilly / Manning-grade clean, professional, confident, no
clutter, high contrast for thumbnail readability.
```

## 산출
- `spring-batch-6/cover.png` (1600 × 2400, PNG)
- `spring-batch-6/_make_cover.py` (재생성 스크립트)
- `spring-batch-6/cover_prompt.md` (이 파일)

## 재생성 / A/B 테스트

```bash
cd spring-batch-6
python3 _make_cover.py
```

콘셉트를 바꾸고 싶으면 `_make_cover.py`의 색상 상수와 중앙 모티브 함수만
수정하면 된다. 2안(리프 미니멀) / 3안(터미널 로그)으로 전환하려면
파이프라인 블록을 잎 실루엣 / 로그 텍스트 블록으로 교체.
