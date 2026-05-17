# Phase 3 — 계획 리뷰 로그

## 리뷰어 총평

레퍼런스 흡수도와 내러티브 아크는 우수. 다만 다음 4개 Critical 이슈로 인해 마이너~메이저 경계의 재구성 필요.

## Critical (반드시 반영)

1. **Projection을 독립 챕터로 신설**. §2.10 + §2.11 + 권고 #10. 4장(N+1) 직후 또는 6장(트랜잭션) 직후 배치. 9장의 Projection bullet은 이쪽으로 이동.
2. **5장 ↔ 6장 순서 재고**. 1차 캐시 = 트랜잭션 스코프인데 트랜잭션 정의 없이 캐시 챕터 진입은 백트래킹. 대안 A: 4 → 6(트랜잭션·OSIV) → 5(캐시) → 7(락). 대안 B: 5장을 "트랜잭션과 캐시"로 통합.
3. **Bytecode enhancement 절 추가**. 레퍼런스 §2.5에 명백한데 현재 부재. 3장 또는 8장에 절로.
4. **9장 정체성을 좁혀라**. 9장은 모니터링·관찰·진단에 한정. 안티패턴 회수는 마지막 절 또는 짧은 interlude. Projection은 신설 챕터로.

## Should (반영 권장)

5. 2장 Statement caching을 절로 승격 (§2.6).
6. 8장을 분리: 대량 write vs 깊은 read는 정반대 워크로드.
7. 10장 분리: "운영 기능"(Audit/Soft Delete/Multi-tenancy/Stored Procedure) + "Hibernate 6/7과 다음 세계".
8. 1장에 Vlad의 64 트랜잭션 수치(149/272/128)와 USL 그래프 충격 제시.
9. 7장에 MySQL InnoDB gap lock 절.
10. 6장에 `enable_lazy_load_no_trans` 안티패턴 명시 절.

## Nice-to-have

11. 챕터 제목 미세 조정: 3장 "왜 똑같은 엔티티가 다르게 동작하는가". 5장 "캐시는 정말 답인가".
12. 각 챕터 끝 "내 코드 체크리스트" 명시 (책의 약속 회수 구조).
13. 권고 6(컬럼 타입)·권고 14(샤딩/스케일) 회수 지점 명시.
14. §3.4 JPAB 표준 벤치·§3.5 ORM Battle 2025 인용 자리 명시.

## 최종 권고

(b) 마이너 수정 후 진행 — Critical 4개는 마이너의 한계선. 챕터를 10장 → 11~12장으로 확장 권장.

---

## v2 개정 반영 결과 (2026-05-17)

플래너가 피드백 14개 항목 전체를 검토하여 다음과 같이 반영했다. 최종 구조: **12장**(본문).

### Critical (4/4 전체 반영)

1. **Projection 독립 챕터 신설 → 5장** "가져오는 형태도 다시 본다 — Projection과 query 선택". §2.10 + §2.11 + 권고 #10이 자기 자리를 갖는다. 위치는 *N+1 직후*로 결정 — "fetch를 줄였으면 가져오는 형태도 다시 봐야 한다"는 흐름의 자연스러움 + 6장(트랜잭션·OSIV)에서 "OSIV를 끄는 결단" 후 "EntityGraph + DTO Projection으로 보강"이라는 회수 다리를 깔기 위함.
2. **5장 ↔ 6장 순서 뒤집기.** 트랜잭션(6장) → 캐시(7장)로 재배치. 백트래킹 제거.
3. **Bytecode enhancement 절을 3장에 추가.** `hibernate-enhance-maven-plugin`의 세 옵션(`enableLazyInitialization`/`enableDirtyTracking`/`enableAssociationManagement`)을 식별자·equals와 같은 자리(엔티티 설계)에서 다룬다.
4. **11장 정체성 좁히기.** 관찰·진단 도구에 집중. 안티패턴 카탈로그는 마지막 절 회수로 짧게, 36개 체크리스트 회수가 새 비중을 차지. Projection은 5장으로 빠져나갔다.

### Should (6/6 전체 반영)

5. **Statement caching 정식 절 승격 (2장).** PG `prepareThreshold` / MySQL prepStmtCache / Oracle defaultRowPrefetch / `StatementInspector`.
6. **8장 분리 → 9장(배치·대량 write) + 10장(페이지네이션·깊은 read).** 정반대 워크로드를 각각 풀어낼 공간 확보.
7. **10장 분리 권고 (운영 기능 / 미래)**는 *한 챕터 안의 두 절 구조*로 흡수: **12.1 운영 기능** (Audit/Soft Delete/Multi-tenancy/Stored Procedure) + **12.2 다음 세계** (H6/H7/Jakarta Data/jOOQ/Reactive). 챕터를 13으로 늘리면 각 절이 얇아지는 부작용 + 책 닫음(12.3)이 마지막 챕터에서 일관되게 일어나야 한다는 판단으로 통합 유지.
8. **1장에 64-tx 충격 도입.** 149/272/128ms + USL 그래프를 첫 페이지에.
9. **8장에 MySQL InnoDB gap lock 명시 절.** next-key lock 메커니즘, `@Lock` + LIMIT 사고 사례, RC로 내리는 트레이드오프.
10. **6장에 `enable_lazy_load_no_trans` 안티패턴 명시 절.** *어떤 상황에서도 켜지 않는다*가 결론.

### Nice-to-have (4/4 전체 반영)

11. **챕터 제목 미세 조정** — 7장 "캐시는 정말 답인가" (리뷰어 제안 채택). 3장은 식별자/equals/bytecode enhancement 세 축을 균형 있게 드러내는 "엔티티를 잘 빚는다는 것 — 식별자, equals, 그리고 bytecode enhancement"로.
12. **각 챕터 끝 체크리스트 3개 형식 명시.** 책 도입부에서 "책의 약속"으로 선언, 11장에서 36개를 한 표로 회수하는 구조.
13. **권고 #6(컬럼 타입) → 3장 마지막 절, 권고 #14(샤딩/스케일) → 9장 마지막 절** 회수 지점 명시.
14. **JPAB.org 표준 벤치 → 5장(projection vs entity throughput), ORM Battle 2025 → 12.2(jOOQ 절)** 인용 자리 명시.

### 분량 변화

10장 198,000자 → 12장 **229,000자** (≈ 280p → 330p). 본문만 약 +31,000자. Projection 신설(+18,000) + Statement caching 절 확장(+2,000) + bytecode enhancement 절(+2,000) + 페이지네이션 분리(±0, 기존 배치 챕터 안의 페이지네이션 부분이 독립 챕터로 풀어짐) + MySQL gap lock 절(+1,500) + enable_lazy_load_no_trans 절(+1,000) + 36개 체크리스트 회수 표(+1,500) + 12장 운영 기능 절 보강(+5,000) 등. 책 한 권을 받칠 정석 분량(330~370p).

### 비반영 / 보류 항목

- 없음. 리뷰 피드백 14개 항목 모두 본 v2에서 흡수했다.

### 다음 단계

- v2 계획을 다시 plan-reviewer가 검토할 필요가 있다면 챕터 5(신설)·11(좁힘)·12(통합)의 정합성, 그리고 책 분량이 24~25만 자로 늘어난 점에 대한 적정성 검토를 받는 것을 권한다. 본 플래너 판단으로는 추가 라운드 없이 chapter-writer로 진입 가능.

