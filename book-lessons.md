# Book lessons (harness learning loop)

One record per book run. Appended by the orchestrator at completion.

## 2026-10-19 — AI 네이티브 SDLC 플레이북 (ai-native-sdlc-playbook)

- topic: Claude Academy course "The AI-native SDLC playbook" → Korean book for developers already using Claude Code
- genre: tech-book · harness v2.0.0 · delegation_mode production · 14 chapters · book v1.0.0
- 반복된 사실 이슈: (1) 코스 서술 vs 현행 Claude Code 문서 drift 11건 — "구버전 주의" 박스 배정이 효과적이었음; (2) 리서처 요약이 비교 대상을 생략한 수치 2건(한국어 토큰 1.45배 = 신/구 토크나이저 비교, Bainbridge "70년 전" = 43년) — 레퍼런스 합성 단계에서 수치의 비교 대상·연도 계산을 명시하면 저술가 오류를 줄임; (3) 계획의 "인용 금지" 지시가 출처 미확인 전제였는데 fact-checker가 공식 출처를 찾은 경우(7x 토큰) — 계획 지시는 "출처 확인 전까지 금지"로 쓰는 편이 맞음; (4) `/cost`→`/usage` 별칭처럼 코스 발행 후 바뀐 명령은 fact-checker 웹 확인에서만 잡힘.
- 수락 게이트: 라운드 1 ACCEPT(비차단 11건, 그중 1건은 대소문자 grep 오탐), 라운드 2 ACCEPT.
- 분량 준수도: 합계 127,385자 / 계획 114,000자 (+11.7%). 저술가 4명 모두 공통 규약 6요소를 채우면서 목표를 15~40% 초과 → editor가 ±15%로 압축, 11장(코드 4블록·그림 2)은 +22%로 수락. 교훈: 6요소 공통 규약을 붙이는 장은 계획 목표를 처음부터 1.2배로 잡거나 요소 수를 줄일 것.
- 1차 자료 캡처: 코스 14레슨을 오케스트레이터가 직접 `research/primary/`에 저장하고 리서처들에게 "코스는 다시 수집하지 말고 코스가 참조만 하는 것을 채워라"로 브리프한 것이 리서치 품질·fact-check 대조에 결정적이었음.
