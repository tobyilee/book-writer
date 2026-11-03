# 책 산출 교훈

## 2026-11-03 — insider-braze-marketing (tech-book, 14장)
- topic: Insider One·Braze CRM 마케팅 입문서 (주니어 마케터 대상, SaaS 제품 기능 상세)
- 반복된 사실 이슈: 벤더 기능명 리네이밍(Sirius AI→Agent One, Sage AI→BrazeAI), 카카오 채널 지원 범위(알림톡 미확인·친구톡 종료는 대행사 안내뿐), Canvas 진입 방식 명칭, 공식 문서끼리 수치 상충(Predictive Churn 3 vs 5). 한국 법규는 law.go.kr 원문이 JS 렌더라 미확보 → 미러·2차 자료로 약화 서술.
- 수락 게이트 BLOCK 사유: (f) 약속 이행 — Braze 자체 분석/리포트·Global Control Group 미서술(리서치 원장 공백에서 기인). 교훈: 제품 비교서는 리서치 브리프에 "분석·리포트·전역 대조군" 영역을 명시할 것.
- 운영 메모: 병렬 fact-checker가 단일 factcheck_log.md를 동시에 쓰지 않도록 묶음별 로그 파일 → 오케스트레이터 병합. 규제 장(9장)은 보강 리서치 완료 후 저술 착수.
- 챕터 수: 14 / 분량 준수도: 산문 114,655자(계획 116,000자), 장별 중앙값 대비 84~121%, 플래그 0.
- 빌드: pandoc·epubcheck·mmdc 미설치 → 사용자 허용 하에 scratchpad 사본으로 빌드. epubcheck(Java)는 LANG/JAVA_TOOL_OPTIONS UTF-8 없으면 한글 파일명을 못 찾음, mmdc는 PUPPETEER_EXECUTABLE_PATH에 ~/.cache/puppeteer chrome-headless-shell 지정 필요. 결과: epubcheck 0 errors, mermaid 11개 렌더.
