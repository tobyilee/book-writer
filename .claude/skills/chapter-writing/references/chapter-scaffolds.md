# 챕터 스캐폴드 → 이전됨

하네스 v1.3.0부터 챕터 스캐폴드는 장르 프로필로 이관되었다. 기술서 5종 스캐폴드는 **tech-book 프로필**로 옮겨졌고, 장르별 스캐폴드가 새로 추가되었다.

→ **`profiles/{genre}/scaffolds.md`** (프로젝트 루트 기준)
- `profiles/tech-book/scaffolds.md` — 개념 도입형·문제 해결형·사례 분석형·비교 대조형·종합 정리형 (기존 내용)
- `profiles/narrative/scaffolds.md` — 3막·씬·챕터 유형 (소설)
- `profiles/practical/scaffolds.md` — 레시피·여행 코스·기법·가이드 (실용서)
- `profiles/essay/scaffolds.md` — 일화-성찰·몽타주·변증 (에세이)

활성 장르는 `{slug}/book_manifest.json`의 `genre`로 결정된다. 없으면 기본값 `tech-book`. 프로필 구조는 `profiles/_registry.md` 참조.
