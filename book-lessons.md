# 하네스 학습 루프 — 책별 교훈 (append-only)

## 『같은 이름, 다른 동작 — Claude Code 사용자를 위한 OpenAI Codex 완전 정리』 (2026-08-02)

- **topic:** OpenAI Codex 사용법 완전 정리 (learn.chatgpt.com /codex/* 148 URL 전수, Claude Code 경험자 관점)
- **genre:** tech-book · **챕터 수:** 12 · **분량 준수도:** 총량 102,019자 / 계획 108,000자 (-5.5%, 장별 ±10% 이탈 0건 — 미달분은 근거 없는 자리를 채우지 않은 규율 준수의 결과로 4.5 게이트가 판정)
- **반복된 fact 이슈:** ❌ 6건 중 5건이 "옮기기"(인용)가 아니라 **"세기·요약하기·회수하기"(2차 가공)**에서 발생 — 총량 집계(95개/네 가지/행 누락), 링크 target vs 셀 문자열, 장 간 전파 오염(외부 표준 인용이 다음 장에서 제품 동작으로 흡수), 인용 미세 변조(버전 표기 삭제). 대응 규율 FR-9·10·16·18·19 신설 후 **파별 ❌ 추이 2→3→1→0으로 수렴** — 실패 패턴의 규율 승격 + 파일 전파가 실제로 작동.
- **반복된 style 이슈:** 수사 대구("A가 아니라 B다") 파 1 41회 → 파 4 14회, 대시형 소절 제목 파 2 5~6/7 → 파 3·4 0~1/7 — **오케스트레이터 중계 없이 style_guide_active.md 파일 전파만으로 통권 tic 교정 실증.**
- **하네스 개선 후보 1 (구조 공백):** 부속(서문·에필로그·참고문헌)은 editor 단계에서 처음 쓰이므로 `style_guide_active.md` 누적 규약이 editor에게 전파되는 지점이 없다 — 이번 editor 스타일 Critical 3건 전부가 부속에서 발생. editor 지시에 "style_guide_active.md 필독"을 스킬 레벨로 명문화할 것.
- **하네스 개선 후보 2 (환경):** puppeteer 캐시 Chrome이 손상된 환경(Frameworks 부재)에서 build_epub.sh 자동 탐지가 손상본을 잡음 — 시스템 Chrome 폴백 순위를 올리거나 dlopen 검증 추가 검토. 이 머신에서는 `PUPPETEER_EXECUTABLE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` 명시 필요.
- **리서치 교훈:** WebFetch는 이 문서 사이트(learn.chatgpt.com)에서 표·설정 키를 소실시키고 문단을 합성한 인용을 만들 수 있음 — URL 뒤 `.md`를 붙인 원문 마크다운 수집 + astro-island JSON 디코딩이 정답. 원문 무손실 캐시(`research/codex-docs-raw/`)가 fact-checker 판정의 최종 기준으로 매우 유효했음.
- **레퍼런스 자체 오류 경계:** 리서치 종합 문서가 시제 오류("이미 지난 날짜")를 만들 수 있고, 저술가가 레퍼런스를 재독하며 정정을 되돌릴 위험이 있다 — 계획 단계 확정 판정을 fact_rules_active.md에 시드해 봉인하는 패턴이 유효.
