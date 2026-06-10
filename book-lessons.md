# Book Lessons (append-only)

## 2026-06-10 — 네 겹의 엔지니어링 (agentic-coding-engineering)
- topic: AI Agentic Coding 4대 엔지니어링 (Prompt/Context/Harness/Loop)
- genre: tech-book
- 챕터 수: 9 (0~8)
- 분량 준수도: 최종 전 챕터 배정 밴드 진입. 단 초반 챕터(0·1·2)가 1차 초안에서 배정의 절반 수준 — 분량 보강 패스 1회 필요했음. 차기 책은 저술가 프롬프트에 분량 하한 명시 권장.
- 반복된 style 이슈: bold 과포화(3·4·5장 공통, chars-per-bold 밴드로 수렴시킴), 클로징 줌아웃 cadence 유사(2·4·5장 — 통합 단계에서 변주 처리).
- 반복된 fact 이슈: (1) Anthropic 두 문서 혼동 — "Building Effective Agents"(2024-12) vs "Effective context engineering"(2025-09-29) 인용 귀속 오류 1건. (2) 레퍼런스 자체 과장이 본문·참고문헌으로 2회 전파 시도(Chroma context rot "단조 감소" — 1차 출처는 non-uniform). 1차 출처 대조가 레퍼런스 신뢰보다 우선해야 함. (3) editor의 참고문헌 신규 작성부에서 사실 회귀 재유입 — 통합본 사실 회귀 패스가 실제로 잡아냄(유지 가치 확인).
- 기타: mmdc(mermaid-cli) 미설치 환경에서 다이어그램이 코드 펜스로 남음 → 설치 후 재빌드. mmdc SVG 출력은 epubcheck RSC-005 유발 — PNG 출력 패치 적용(build_epub.sh).

## 2026-06-10 — 네 겹의 엔지니어링 v1.1.0 개정 (agentic-coding-engineering)
- 개정 사유: 독자 피드백 "loop engineering 내용 부족" + 1차 출처 제공(addyosmani.com/blog/loop-engineering, 2026-06-07).
- 교훈: (1) 빠르게 변하는 주제의 신생 용어는 초판 시점에 1차 출처가 없을 수 있다 — 완충 귀속(인물명 미기재)으로 출간하고, 1차 확보 시 실명 귀속으로 승급하는 2단 전략이 유효했다. (2) 챕터 단위 재저술 시 가장 큰 위험은 인접 장과의 귀속·완충 수위 불일치(5장 확정 vs 7장 완충 모순) — fact-checker watchlist 사전 등록 + editor 동기화로 해소. (3) 비용/논쟁 수치의 챕터 분업 경계(5장 포인터, 7장 상술)는 증보 시에도 유지해야 중복이 안 생긴다.
- 프로세스: 부분 재실행(리서치 보강 → 5장만 재저술 → 파급 동기화 → 재수락 → 재빌드)이 전체 재실행 없이 작동. identifier 보존 + version 1.0.0→1.1.0.
