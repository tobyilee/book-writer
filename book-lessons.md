# 하네스 학습 루프 — 책별 교훈 (append-only)

## mcp-server-development (2026-07-26, harness v1.9.1)

- **topic:** MCP 서버 개발 (TS/Python/Java, Claude Code 연결, 배포)
- **genre:** tech-book · **챕터 수:** 12 (계획 11 → 리뷰로 12 분할) · **분량 준수:** 본문 계획 대비 −10.1% (전 장 프로필 밴드 내, 이탈 1건은 코드 비중 예외 인정)
- **반복된 style 이슈:** 굵은 리드인 문단(불릿의 산문 위장 — 통권 최다 지적, 편집자 신규 산문에서도 재발), 질문 클로징 번짐, 수평선 표기 흔들림. 병렬 저술 시 클로징/다이어그램/핵심박스 **사전 배정 표**가 배정 위반 0건을 만들었다 — 재사용 가치 높음.
- **반복된 fact 이슈:** ① 레퍼런스의 해석 오류가 두 장에 전파(협상 fallback — `[검증]` 상수 열거에 `[웹]` 해석이 섞임; §9 정정 주석으로 봉합). ② 빠르게 움직이는 주제에서 "SDK 상태를 권고가 아니라 **시점 관측**으로 쓰기" 규칙이 GA 임박(이틀 뒤) 상황에서도 원고를 안 낡게 만들었다. ③ 러닝 예제 명세를 계획에 고정(C-1)한 것이 3언어 병렬 저술의 정합을 지켰고, 와이어 봉투(structuredContent) 같은 세부는 그래도 갈라져 fact-checker 판정이 필요했다.
- **빌드:** build_epub.sh 버그 2건 발견·수정(YAML 이스케이프, mermaid SVG `<p>` → epubcheck RSC-005). mermaid는 PUPPETEER_EXECUTABLE_PATH 필수. **이 수정은 이 worktree에만 있으므로 main 반영 필요.**
- **하네스 백로그:** book-editing 템플릿 백매터 H2 ↔ build_epub.sh --split-level=1 불일치(모든 책에서 재발), 계획 분량 배정이 코드 비중 미반영.
