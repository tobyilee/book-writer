# Book Lessons

## 2026-09-26 — 배포는 검증이다 (cicd-github-aws-cloudflare)
- topic: GitHub·AWS·Cloudflare CI/CD + AI 코딩 팁 / genre: tech-book / 챕터 12 / harness v2.0.0
- 반복된 사실 이슈: 합성 레퍼런스(01_reference.md) 자체의 오류가 여러 장으로 전파됨 — Cloudflare Worker Previews 격리 범위·버전 롤백 범위, 논문 요약 수치(P-47 "22"). 레퍼런스가 "미확인"으로 둔 항목(GitHub OIDC immutable sub)이 실제로는 1차 출처로 확인됨. 옵션·필드명(wrangler·codex-action·claude-code-action)은 레퍼런스에 없어 fact-checker 웹 2차가 필수였음(7~9장 마커 14개).
- 수락 게이트 BLOCK 사유: (g) 참고문헌이 내부 작업 파일(community.md 패턴 번호)·공정 메모를 가리킴, URL 누락 → 1회 조치로 PASS.
- 분량 준수도: 105,695 / 108,000자(−2%). 1장 목표가 계획 내부에서 7,000(배정표) vs 9,000(상세)로 불일치.
- 기타: 에필로그·참고문헌이 `##`라 split-level=1에서 12장 파일에 흡수됨 → `#`로 승격. 빌드 머신에 pandoc/epubcheck/mmdc 미설치였음.
