# 저술가 인계 메모 (editor·manuscript-reviewer 참고)

오케스트레이터가 각 저술가 반환값에서 추린 통권 정합성 항목. 러닝 예시 정전은 `02_plan.md`가 우선이고, 아래는 저술 중 새로 정해진 세부다.

## 4~6장 묶음이 정한 정전 세부

- 가격 페이지 경로: `wiki/strategy/pro-plan-pricing.md` (type: fact, `valid_from: 2026-01-01`, `valid_to: null`, `review_after: 2026-03-30`, `owner: people/han-seojin`). 10장에서 `valid_to`가 `2026-08-31`로 바뀐다고 4장이 예고.
- 결정 페이지 경로: `wiki/decisions/2026-06-vertical-expansion-go.md`(status: reversed) / `wiki/decisions/2026-08-12-expansion-hold.md` / 가격 인상 `wiki/decisions/2026-08-20-pro-plan-price-increase.md` / 일본 진출 `status: pending`.
- 프런트매터 필드: title, type(fact|decision|howto|scenario|brand|person|concept), tldr(≤50자), origin(human|llm|llm-reviewed), confidence, sources, last_verified, review_after, valid_from, valid_to, superseded_by, contradicts, owner, tags. 결정 페이지 추가: status(decided|pending|reversed), decided_on, decided_by, supersedes.
- `log.md` 접두어: `## [YYYY-MM-DD] 연산 | 대상`, 연산은 ingest·query·lint·promote.
- 디렉터리: `raw/{notion,slack,pdf,web,_unsorted}/`, `raw/_manifest.jsonl`, `raw/CLAUDE.md`, `wiki/{index.md,log.md,glossary.md,brand,strategy,howto,scenarios,decisions,people}/`, `scripts/{lint_wiki.py,build_index.py}`, `.claude/{rules/decisions.md, skills/{ingest,query,lint}}`. 링크는 표준 마크다운 상대 경로, 파일명 ASCII.
- 6장 답변 프롬프트: 세션 중 `wiki/`에 쓰지 않고 `[환류 후보]` 마커만. 훅 구현(PreToolUse raw/ 차단, Stop 미커밋 차단)은 8장으로 넘김.
- 5장 오프닝 노션 페이지 수: 정전(35)을 우선 — 계획 본문의 "40"과 다름. editor는 35로 통일.

## 7~9장 묶음

- 29,000원 답변(8장 오프닝·9장 콜백)은 4장 v1 가격 페이지 기준. 9장 오프닝에 "10장에서 다시 본다" 복선 한 줄.
- 8장 코드 모델 ID는 `claude-sonnet-5-5` 상수(레퍼런스에 ID 문자열 없음 → fact-checker 확인 대상).
- 7장 전환 기준표 "맞는 규모" 열은 gist 1차(~100 sources)와 커뮤니티 경험치를 "gist: / 경험치:"로 병기.
- 사용한 API/SDK 시그니처는 01_reference.md 6.4·6.6·6.7·6.8·4.2·8.6절 범위만. `Stop` 훅은 코드 없이 요지만.

## editor가 확인할 교차 항목

- 9·10·12장이 4장의 가격 페이지 경로·결정 페이지 경로·프런트매터 필드명을 그대로 쓰는지.
- 12장 아키텍처 그림의 디렉터리가 4장 디렉터리와 일치하는지.
- 12장 결정 체크리스트가 1~11장 각 장의 클로징 결정과 일치하는지.

## fact-checker 메모 (editor 참고문헌 반영)

- 3장에서 1차 대조 완료된 식별자 2건을 참고문헌에 추가: arXiv 2605.25480 (Ming·Li·Wu·Que, "Retrieval as Reasoning", 2026-05, preprint) / arXiv 2605.18490 (Cochran, 2026-05, v3 2026-10-02, preprint). 01_reference.md §15.6의 "2차 인용만(미대조)" 표기는 이제 1차 확인됨.
- 7장에서 arXiv 2605.15184 (PwC "Is Grep All You Need?", 2026-05-14) 1차 확인됨.
- 5장: Google Docs 공식 마크다운 내보내기 존재 확인(2024-07 Workspace Updates, Drive API `text/markdown`) — 01_reference.md 16.1의 "미확인"은 해소됨.

## 10~12장 묶음

- 10장이 계획(9,000)보다 큼(산문 공백 포함 ~14,800). 8·4장도 계획보다 큰 편 — editor가 통권 비율로 판단. 줄일 후보: "자율이냐, 사람이냐"·"비결정성, 그리고 증분과 리빌드" 소절.
- 10장 저술 시 9장 초안이 없었음 → editor가 9→10 전환(Stigmergy "No write waits for a human." 콜백)을 한 번 확인.
- 12장 결정 목록 15항목(4·5·6·9장은 2항목씩). 12장 오프닝 "40문항 중 34문항"은 11장 "골든셋 40문항, 거부 8문항"과 맞춤. 골든셋 씨앗 6문항은 8장 끝 문구 그대로.
- 12장 4주 계획의 "끝났다는 기준"·"멈춰야 할 신호"는 저술가 설계값(레퍼런스 수치 아님).
